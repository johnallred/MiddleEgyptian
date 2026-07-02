"""
Generate game material from Entries2.json.

Outputs (under ./game_material/):

  rules.md                     - human-readable rules of play
  deck.json                    - ready-to-prototype starter deck
  words/                       - one JSON file per playable word
    1_sign/  ... 7_plus_sign/    organized by shortest phonetic-spelling length

A "playable word" = a distinct transliteration that appears in
Entries2.json with at least one writing whose signs, after stripping
determinatives and plural markers, are all phonetic (uni/bi/triliteral
per res_signinfo.js).
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Content filtering — see CONTENT_FILTER docs in PROJECT_GUIDE.md
# ---------------------------------------------------------------------------

# Signs that VISUALLY depict sexual anatomy. Exclude from family decks.
FAMILY_BLOCKED_SIGNS = {
    "D27", "D27a", "D27A",   # breast (small/large)
    "D52", "D52a", "D52A",   # phallus
    "D53", "D53a", "D53A",   # liquid issuing from phallus
    "F45", "F45a", "F45A",   # uterus
    "F51", "F51a", "F51A",   # piece of flesh / vulva
}

# Regex of explicit English terms to filter from family-deck glosses.
# Matched as whole-word stems to avoid catching "breastplate", "vaginal" etc.
FAMILY_BLOCKED_GLOSS_PATTERN = re.compile(
    r"\b("
    r"phallus|penis|testic\w*|scrotum|ejaculat\w*|"
    r"vulva|vagina|uterus|pubic|pudenda|"
    r"copulat\w*|intercourse|fornicat\w*|masturbat\w*|"
    r"breast\b|nipple|teat"
    r")\b",
    re.IGNORECASE,
)


def is_family_safe(translit: str, english_glosses: list[str],
                   all_spellings: list[list[str]]) -> bool:
    """True if this word may appear in a family deck."""
    # Sign-based filter: any spelling that uses ONLY non-blocked signs is fine.
    # If EVERY spelling uses at least one blocked sign, exclude the word.
    has_safe_spelling = False
    for sp in all_spellings:
        if not any(s in FAMILY_BLOCKED_SIGNS for s in sp):
            has_safe_spelling = True
            break
    if not has_safe_spelling:
        return False
    # Gloss-based filter
    for g in english_glosses:
        if FAMILY_BLOCKED_GLOSS_PATTERN.search(g or ""):
            return False
    return True


def filter_family_spellings(spellings_annotated: list[dict]) -> list[dict]:
    """Strip any spelling that uses a blocked sign; keep the safe ones."""
    return [sp for sp in spellings_annotated
            if not any(s["sign"] in FAMILY_BLOCKED_SIGNS for s in sp["annotated"])]

DICT_DIR = Path(__file__).parent
ENTRIES = DICT_DIR / "Entries2.json"
SIGN_CLASS_DIR = DICT_DIR / "sign_classification"
OUT_DIR = DICT_DIR / "game_material"
WORDS_DIR = OUT_DIR / "words"

# ----- difficulty tiers and point values -----
POINT_VALUES = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7, 6: 10, 7: 15, 8: 20, 9: 25, 10: 30}
TIER_NAMES = {1: "trivial", 2: "easy", 3: "medium-easy", 4: "medium",
              5: "medium-hard", 6: "hard", 7: "expert"}

# ----- plural / dual / ideogram markers (stripped along with determinatives) -----
GRAMMAR_MARKERS = {"Z1", "Z2", "Z3", "Z2A", "Z2B", "Z2C", "Z2D",
                   "Z3A", "Z3B", "Z4", "Z4A", "Z4B"}

# ----- honorific transposition support (optional advanced rule) -----
# Signs whose presence marks a word as containing a divine or royal
# element. Word cards containing one get "honorific_transposition": true;
# matching sign cards get "honorific": true. All C-category signs
# (anthropomorphic deities) qualify via the prefix check below.
HONORIFIC_SIGNS = {
    "R8", "R8a",                                    # nTr, god-sign
    "N5", "N6",                                     # sun disc (Ra)
    "G7",                                           # falcon on standard
    "A40", "A41", "A42", "A43", "A44", "A45", "A46",  # seated gods/kings
    "M23",                                          # sedge (nsw, king)
    "L2",                                           # bee (bity, king)
    "S1", "S2", "S3", "S4", "S5", "S6", "S7",       # crowns
}


def is_honorific_sign(sign: str) -> bool:
    if sign in HONORIFIC_SIGNS:
        return True
    # All C-category signs are anthropomorphic deities.
    return len(sign) >= 2 and sign[0] == "C" and sign[1].isdigit()

# Size of the shared determinative side pool generated per deck
# (optional advanced rule: determinative bonus).
DET_SIDE_DECK_UNIQUE = 24
DET_SIDE_DECK_TOP_COPIES = 8   # this many most-used dets get 2 copies


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NP = re.compile(r"^(Aa|AA)(\d+)([A-Za-z]?)$")
_NS = re.compile(r"^([A-Z])(\d+)([A-Za-z])$")


def norm_sign(s: str) -> str:
    m = _NP.match(s)
    if m:
        return "Aa" + m.group(2) + m.group(3).lower()
    m = _NS.match(s)
    if m:
        return m.group(1) + m.group(2) + m.group(3).lower()
    return s


def safe_filename(translit: str) -> str:
    """Make a transliteration safe for use as a filename."""
    s = translit.strip()
    s = s.replace("/", "-or-")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[<>:\"|?*\\]", "", s)
    s = re.sub(r"\.\.+", ".", s)
    s = s.strip("._-")
    if not s:
        s = "_unnamed"
    return s[:100]  # cap length


def dn(md):
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return v


SRC_NAMES = {0: "Lexicon", 1: "Dickson", 2: "Vygus", 4: "Faulkner",
             "0": "Lexicon", "1": "Dickson", "2": "Vygus", "4": "Faulkner"}


# ---------------------------------------------------------------------------
# Load sign reference data
# ---------------------------------------------------------------------------


def load_sign_data():
    with open(SIGN_CLASS_DIR / "signs_by_phonetic_class.json") as f:
        by_class = json.load(f)
    phonetic = {}  # sign -> {"class": ..., "mnemonic": ..., "description": ...}
    for cls, signs in by_class.items():
        for sign, info in signs.items():
            phonetic[sign] = {
                "class": cls,
                "mnemonic": info.get("primary_mnemonic", ""),
                "description": info.get("description", ""),
            }
    with open(SIGN_CLASS_DIR / "signs_logogram.json") as f:
        logograms = json.load(f)
    with open(SIGN_CLASS_DIR / "signs_determinative.json") as f:
        determinatives = json.load(f)
    return phonetic, logograms, determinatives


# ---------------------------------------------------------------------------
# Build the playable-word index from Entries2.json
# ---------------------------------------------------------------------------


def build_word_index(entries, phonetic_signs, determinatives):
    """
    Returns: {translit: {
        "spellings": [(tuple_of_signs, sign_count), ...],
        "english_glosses": [str, ...],
        "primary_pos_core": str,
        "all_pos_cores": [str, ...],
        "sources": [str, ...],
        "raw_sign_lists": [list_of_signs, ...],  # original including determinatives
    }}
    """
    index = defaultdict(lambda: {
        "spellings_set": set(),
        "english_glosses": [],
        "english_seen": set(),
        "pos_counter": Counter(),
        "sources": set(),
        "raw_writings": set(),
    })

    for e in entries:
        translit = (e.get("Transliteration") or "").strip()
        if not translit:
            continue
        gs = (e.get("GardinerSigns") or "").split()
        if not gs:
            continue
        normalized = [norm_sign(s) for s in gs]
        # Strip determinatives + grammar markers, keep phonetic order
        stripped = [s for s in normalized
                    if s not in determinatives and s not in GRAMMAR_MARKERS]
        if not stripped:
            continue
        # Must be ALL phonetic after stripping for this writing to count
        if not all(s in phonetic_signs for s in stripped):
            continue

        rec = index[translit]
        rec["spellings_set"].add(tuple(stripped))
        rec["raw_writings"].add(tuple(normalized))

        for t in e.get("Translations") or []:
            gloss = (t.get("translation") or "").strip()
            if gloss:
                # Use first comma-bounded gloss, normalized
                head = gloss.split(",")[0].split(";")[0].split(":")[0].strip()
                key = head.lower()
                if head and key not in rec["english_seen"]:
                    rec["english_glosses"].append(head)
                    rec["english_seen"].add(key)
            md = t.get("TranslationMetadata") or {}
            pos = md.get("PartOfSpeechCore")
            if pos:
                rec["pos_counter"][pos] += 1
            src = dn(md)
            if src is not None:
                rec["sources"].add(SRC_NAMES.get(src, str(src)))

    # Finalize
    result = {}
    for translit, rec in index.items():
        spellings = sorted(rec["spellings_set"], key=lambda t: (len(t), t))
        if not spellings:
            continue
        sign_count = len(spellings[0])
        pos_total = rec["pos_counter"]
        primary_pos = pos_total.most_common(1)[0][0] if pos_total else None
        # Determinatives documented in this word's raw writings (they get
        # stripped from playable spellings, but the optional determinative-
        # bonus rule needs them back).
        dets = set()
        for writing in rec["raw_writings"]:
            for s in writing:
                if s in determinatives and s not in GRAMMAR_MARKERS:
                    dets.add(s)
        result[translit] = {
            "spellings": [list(t) for t in spellings],
            "english_glosses": rec["english_glosses"][:6],
            "primary_pos_core": primary_pos,
            "all_pos_cores": sorted(pos_total.keys()),
            "sources": sorted(rec["sources"]),
            "shortest_sign_count": sign_count,
            "determinatives": sorted(dets),
        }
    return result


# ---------------------------------------------------------------------------
# Write per-word JSON files
# ---------------------------------------------------------------------------


def write_word_files(word_index, phonetic_signs):
    # The words/ tree is fully generated: clear it first. (The collision
    # suffix logic below exists for DISTINCT transliterations that share a
    # safe filename — rerunning into a non-empty tree would misread every
    # existing file as a collision and write 9,466 suffixed duplicates.)
    import shutil
    if WORDS_DIR.exists():
        shutil.rmtree(WORDS_DIR)
    WORDS_DIR.mkdir(parents=True, exist_ok=True)

    # Make subdirs by shortest sign count
    def bucket(n: int) -> str:
        if n == 1:
            return "1_sign"
        if n <= 6:
            return f"{n}_sign"
        return "7_plus_sign"

    counts = Counter()
    collisions = Counter()
    _used_stems: set = set()
    written = 0
    for translit, info in word_index.items():
        n = info["shortest_sign_count"]
        bucket_name = bucket(n)
        bucket_dir = WORDS_DIR / bucket_name
        bucket_dir.mkdir(parents=True, exist_ok=True)
        counts[bucket_name] += 1

        base = safe_filename(translit)
        # Collision handling must not rely on path.exists(): transliterations
        # are CASE-SENSITIVE (t vs T are different phonemes) but the target
        # filesystem may be case-insensitive (macOS), where "in.json" and
        # "iN.json" are the same file and one would silently overwrite the
        # other. Track used names casefolded instead.
        stem = base
        while (bucket_name, stem.lower()) in _used_stems:
            collisions[base] += 1
            stem = f"{base}__{collisions[base]+1}"
        _used_stems.add((bucket_name, stem.lower()))
        path = bucket_dir / f"{stem}.json"

        # Build the per-word record with annotated spelling
        spellings_annotated = []
        for sp in info["spellings"]:
            annotated = []
            for sign in sp:
                ph = phonetic_signs.get(sign, {})
                annotated.append({
                    "sign": sign,
                    "mnemonic": ph.get("mnemonic", ""),
                    "class": ph.get("class", ""),
                    "description": ph.get("description", ""),
                })
            spellings_annotated.append({
                "signs": sp,
                "sign_count": len(sp),
                "annotated": annotated,
            })

        tier = TIER_NAMES.get(min(n, 7), "expert")
        points = POINT_VALUES.get(n, max(POINT_VALUES.values()))

        rec = {
            "transliteration": translit,
            "english_glosses": info["english_glosses"],
            "shortest_sign_count": n,
            "difficulty_tier": tier,
            "point_value": points,
            "primary_pos": info["primary_pos_core"],
            "all_pos": info["all_pos_cores"],
            "sources": info["sources"],
            "determinatives": info.get("determinatives", []),
            "spellings": spellings_annotated,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        written += 1

    return written, counts


# ---------------------------------------------------------------------------
# Build the deck file
# ---------------------------------------------------------------------------


def scaled_picks(target_total: int) -> dict[int, int]:
    """Scale the baseline tier sizes to sum to approximately target_total.

    v7 (current): tier 6 dropped entirely (its 12 slots redistributed
    proportionally across tiers 1-5). Tier-6 words are 6 signs each, the
    hardest to complete, and were a major contributor to game-length stalls.
    Removing them shortens games without reducing balance.

    v6 baseline (kept for historical reference):
        {1: 40, 2: 50, 3: 56, 4: 76, 5: 66, 6: 12}  sums to 300
    """
    base = {1: 42, 2: 52, 3: 58, 4: 79, 5: 69}   # v7: tier-6 redistributed, sums to 300
    base_total = sum(base.values())
    scale = target_total / base_total
    out = {n: max(1, round(c * scale)) for n, c in base.items()}
    # Adjust the largest tier to hit target exactly
    delta = target_total - sum(out.values())
    biggest = max(out, key=out.get)
    out[biggest] = max(1, out[biggest] + delta)
    return out


def build_deck(word_index, phonetic_signs, logograms,
               picks_per_tier_override: dict[int, int] | None = None,
               content_filter: str = "family",
               determinatives: dict | None = None):
    """
    content_filter:
      "family"          — exclude sexual-anatomy signs and explicit glosses
      "mature"          — include everything (for the After Dark expansion)
      "archaeological"  — include but tag with content_warning field
    """
    """
    Build a ready-to-prototype starter deck.

    Order of operations:
      1. Select word cards (260 cards across tiers).
      2. Count sign usage IN THE SELECTED WORDS ONLY (not whole dictionary).
      3. Build the sign deck guaranteeing every needed sign has >=1 copy,
         then padding by usage frequency within the word pool.
      4. Add logograms whose word is in the selected pool.

    This guarantees that every word in the deck can actually be spelled
    using sign cards from the same deck.
    """

    # ----- 1. SELECT WORD CARDS FIRST -----
    # v3: bias toward words whose shortest spelling uses only common signs.
    # v5: ALSO bias medium-tier word selection toward words that have a
    # documented logogram, so logogram cards can target higher-point words
    # (not just trivial 1-sign words).
    global_sign_freq = Counter()
    for info in word_index.values():
        for sp in info["spellings"]:
            for s in sp:
                global_sign_freq[s] += 1
    TOP_N = 50
    top_signs = set(s for s, _ in global_sign_freq.most_common(TOP_N))

    def shortest_spelling_uses_only_common_signs(info) -> bool:
        if not info["spellings"]:
            return False
        return all(s in top_signs for s in info["spellings"][0])

    # v5: pre-compute the set of words that have a documented logogram OR
    # whose target matches a biliteral/triliteral mnemonic
    log_target_words = set()
    with open(DICT_DIR.parent / "res" / "res_signinfo.js", encoding="utf-8") as f:
        signinfo_content = f.read()
    for m in re.finditer(
        r'^([A-Za-z]{1,3}\d+[a-z]?):\'(.*?)(?=^[A-Za-z]{1,3}\d+[a-z]?:\'|\Z)',
        signinfo_content, re.MULTILINE | re.DOTALL,
    ):
        body = m.group(2)
        for lm in re.finditer(r'\bLog\.\s+(?:or\s+det\.\s+)?<span class="trans">([^<]+)</span>', body):
            word = lm.group(1).strip()
            if word and len(word) <= 25:
                log_target_words.add(word)
    for cls in ("biliteral", "triliteral", "4plus"):
        for sign, info in phonetic_signs.items():
            if info.get("class") != cls:
                continue
            mn = info.get("mnemonic", "").strip()
            if mn:
                log_target_words.add(mn)

    def has_logogram_target(translit: str) -> bool:
        return translit in log_target_words

    # v6: apply content filter at the word-index level
    if content_filter == "family":
        filtered_word_index = {
            t: info for t, info in word_index.items()
            if is_family_safe(t, info.get("english_glosses", []), info["spellings"])
        }
    else:
        filtered_word_index = word_index

    word_cards = []
    by_tier = defaultdict(list)
    for translit, info in filtered_word_index.items():
        n = info["shortest_sign_count"]
        if 1 <= n <= 6:
            by_tier[n].append(translit)

    # v7 tier sizes: drop tier 6 entirely (its 12 slots redistributed across
    # 1-5). v6 used {1: 40, 2: 50, 3: 56, 4: 76, 5: 66, 6: 12}. Can be
    # overridden for deck-size sweeps or backwards-compat experiments.
    picks_per_tier = picks_per_tier_override or {1: 42, 2: 52, 3: 58, 4: 79, 5: 69}
    for n in sorted(picks_per_tier.keys()):
        # v5: for the medium tiers (3-5), reserve ~40% of the slots for
        # logogram-target words. This guarantees logograms can target
        # higher-value words (2-7 points), not just trivial 1-point words.
        logogram_bias = n in (3, 4, 5)
        # Sort each subset by attestation + brevity
        def sort_by_quality(translits):
            return sorted(translits,
                          key=lambda t: (-len(word_index[t]["sources"]),
                                          len(word_index[t]["english_glosses"][0])
                                          if word_index[t]["english_glosses"] else 999,
                                          t))
        common = [t for t in by_tier[n]
                  if shortest_spelling_uses_only_common_signs(word_index[t])]
        other = [t for t in by_tier[n]
                 if not shortest_spelling_uses_only_common_signs(word_index[t])]
        if logogram_bias:
            # Split each group by logogram status
            common_log = sort_by_quality([t for t in common if has_logogram_target(t)])
            common_nolog = sort_by_quality([t for t in common if not has_logogram_target(t)])
            other_log = sort_by_quality([t for t in other if has_logogram_target(t)])
            other_nolog = sort_by_quality([t for t in other if not has_logogram_target(t)])
            cands = common_log + common_nolog + other_log + other_nolog
        else:
            cands = sort_by_quality(common) + sort_by_quality(other)
        n_picked = 0
        for translit in cands:
            if n_picked >= picks_per_tier[n]:
                break
            info = filtered_word_index[translit]
            # For family decks, only emit spellings that don't use blocked signs
            valid_spellings = info["spellings"]
            if content_filter == "family":
                valid_spellings = [sp for sp in valid_spellings
                                   if not any(s in FAMILY_BLOCKED_SIGNS for s in sp)]
            # v8.8: strip 1-sign spellings. Logogram CARDS become the only
            # single-card completions, which protects their "lottery win"
            # identity. Simulator-validated as balance-neutral
            # (VARIANT_PLAYTEST_REPORT.md). Printed point values / tiers are
            # unchanged (deliberate: keeps tier targets and the historical
            # point curve intact). Words whose ONLY documented spelling is a
            # single sign are skipped entirely — they are logograms in all
            # but name and belong in the logogram deck instead.
            valid_spellings = [sp for sp in valid_spellings if len(sp) > 1]
            if not valid_spellings:
                continue
            # v8.11: honorific transposition marker — the word contains a
            # divine or royal sign in at least one playable spelling.
            honorific = any(is_honorific_sign(s)
                            for sp in valid_spellings for s in sp)
            card = {
                "card_id": f"word_{safe_filename(translit)}_{n}",
                "type": "word",
                "transliteration": translit,
                "english_glosses": info["english_glosses"][:3],
                "shortest_sign_count": n,
                "difficulty_tier": TIER_NAMES[n],
                "point_value": POINT_VALUES[n],
                "primary_pos": info["primary_pos_core"],
                "valid_spellings": valid_spellings,
                "sources": info["sources"],
            }
            if honorific:
                card["honorific_transposition"] = True
            # Raw candidate determinatives (filtered to the side deck later)
            card["_det_candidates"] = info.get("determinatives", [])
            if content_filter == "archaeological":
                # Tag (don't exclude) words with mature content
                if not is_family_safe(translit, info.get("english_glosses", []),
                                       info["spellings"]):
                    card["content_warning"] = "mature"
            word_cards.append(card)
            n_picked += 1

    # ----- 2. COUNT SIGN USAGE IN SELECTED WORDS ONLY -----
    sign_usage = Counter()
    needed_signs = set()
    for card in word_cards:
        for sp in card["valid_spellings"]:
            for s in sp:
                sign_usage[s] += 1
                needed_signs.add(s)

    # ----- 3. BUILD SIGN DECK WITH FULL COVERAGE -----
    # Strategy:
    #   - Every needed sign appears at least once.
    #   - All standard uniliterals (whether needed or not) get 4 copies
    #     so the deck plays smoothly and players have alphabet flexibility.
    #   - Needed biliterals get extra copies proportional to usage in the
    #     word pool: 4 copies if used in 10+ words, 3 copies for 5-9
    #     words, 2 copies for 3-4 words, 1 copy for 1-2 words.
    #   - Needed triliterals follow the same rule but slightly thinner
    #     (max 3 copies).
    #   - Needed 4plus signs get 1 copy each (they're inherently rare).
    sign_deck = []
    seen = set()

    def add(sign, kind, copies):
        if sign in seen:
            return
        seen.add(sign)
        info = phonetic_signs.get(sign, {})
        entry = {
            "card_id": f"sign_{sign}",
            "type": "phonetic",
            "phonetic_class": info.get("class", kind),
            "sign_code": sign,
            "mnemonic": info.get("mnemonic", ""),
            "description": info.get("description", ""),
            "usage_in_word_pool": sign_usage.get(sign, 0),
            "copies": copies,
        }
        if is_honorific_sign(sign):
            entry["honorific"] = True   # divine/royal marker (optional rule)
        sign_deck.append(entry)

    # Bucket signs by phonetic class
    by_class = defaultdict(list)
    for sign, info in phonetic_signs.items():
        by_class[info["class"]].append((sign, sign_usage.get(sign, 0)))
    for cls in by_class:
        by_class[cls].sort(key=lambda x: -x[1])

    # 3a. ALL uniliterals get 4 copies (alphabet flexibility)
    for sign, _ in by_class.get("uniliteral", []):
        add(sign, "uniliteral", 4)

    def copies_for_usage(usage, kind):
        """Number of copies given how many word cards use this sign."""
        if kind == "biliteral":
            if usage >= 10:
                return 4
            if usage >= 5:
                return 3
            if usage >= 3:
                return 2
            return 1
        if kind == "triliteral":
            if usage >= 8:
                return 3
            if usage >= 3:
                return 2
            return 1
        # 4plus
        return 1

    # 3b. Every needed biliteral (regardless of overall popularity)
    for sign in needed_signs:
        info = phonetic_signs.get(sign)
        if info and info["class"] == "biliteral":
            add(sign, "biliteral", copies_for_usage(sign_usage[sign], "biliteral"))

    # 3c. Pad with the next most-popular biliterals (not strictly needed
    # but make the deck feel richer). Cap total biliteral count at 80.
    biliteral_count = sum(1 for c in sign_deck if c["phonetic_class"] == "biliteral")
    for sign, _ in by_class.get("biliteral", []):
        if biliteral_count >= 80:
            break
        if sign in seen:
            continue
        add(sign, "biliteral", 1)
        biliteral_count += 1

    # 3d. Every needed triliteral
    for sign in needed_signs:
        info = phonetic_signs.get(sign)
        if info and info["class"] == "triliteral":
            add(sign, "triliteral", copies_for_usage(sign_usage[sign], "triliteral"))

    # 3e. Pad with top triliterals up to 50 total
    triliteral_count = sum(1 for c in sign_deck if c["phonetic_class"] == "triliteral")
    for sign, _ in by_class.get("triliteral", []):
        if triliteral_count >= 50:
            break
        if sign in seen:
            continue
        add(sign, "triliteral", 1)
        triliteral_count += 1

    # 3f. Every needed quadriliteral+
    for sign in needed_signs:
        info = phonetic_signs.get(sign)
        if info and info["class"] == "4plus":
            add(sign, "4plus", copies_for_usage(sign_usage[sign], "4plus"))

    # 3g. Pad up to 12 4plus total
    fourplus_count = sum(1 for c in sign_deck if c["phonetic_class"] == "4plus")
    for sign, _ in by_class.get("4plus", []):
        if fourplus_count >= 12:
            break
        if sign in seen:
            continue
        add(sign, "4plus", 1)
        fourplus_count += 1

    # ----- VERIFY COVERAGE -----
    sign_deck_codes = {c["sign_code"] for c in sign_deck}
    missing = needed_signs - sign_deck_codes
    if missing:
        # Should never happen given the logic above, but guard against silent
        # bugs. Add any leftover needed signs with 1 copy each.
        for sign in missing:
            info = phonetic_signs.get(sign, {})
            add(sign, info.get("class", "unknown"), 1)

    sign_deck_codes = {c["sign_code"] for c in sign_deck}
    final_missing = needed_signs - sign_deck_codes
    assert not final_missing, f"Word cards need signs not in sign deck: {final_missing}"

    # v6: family-mode hard-strip — never include blocked signs even if some
    # word's spelling sneaks one in (shouldn't happen given is_family_safe,
    # but belt-and-suspenders).
    if content_filter == "family":
        sign_deck = [c for c in sign_deck if c["sign_code"] not in FAMILY_BLOCKED_SIGNS]

    # v4: build the logogram deck AFTER the word deck so every logogram
    # targets a word the players can actually have in front of them.
    # Two sources for the (sign, target_word) candidate pool:
    #   A) Documented `Log.` tags in res_signinfo.js (historical).
    #   B) Biliteral / triliteral signs whose mnemonic IS a Middle Egyptian
    #      word — many of these are also historically attested as logograms
    #      in practice, just not explicitly tagged Log. in the reference.

    # ----- A) Documented Log. mappings -----
    sign_to_logograms = defaultdict(set)
    sign_to_description = {}
    with open(DICT_DIR.parent / "res" / "res_signinfo.js", encoding="utf-8") as f:
        content = f.read()
    for m in re.finditer(
        r'^([A-Za-z]{1,3}\d+[a-z]?):\'(.*?)(?=^[A-Za-z]{1,3}\d+[a-z]?:\'|\Z)',
        content, re.MULTILINE | re.DOTALL,
    ):
        sign = m.group(1)
        body = m.group(2)
        for lm in re.finditer(r'\bLog\.\s+(?:or\s+det\.\s+)?<span class="trans">([^<]+)</span>', body):
            word = lm.group(1).strip()
            if word and len(word) <= 25:
                sign_to_logograms[sign].add(word)
        # Capture description
        text_clean = re.sub(r"<[^>]+>", " ", body)
        m_desc = re.search(rf"\b{re.escape(sign)}\s*:\s*([^.<]+?)\.\s", text_clean)
        if m_desc:
            sign_to_description[sign] = m_desc.group(1).strip()

    # ----- B) Mnemonic-as-logogram expansion -----
    # Take every biliteral/triliteral/4plus phonetic sign whose primary
    # mnemonic IS a word in our pool, and treat the sign as a logogram for
    # that word too. Filter to words actually in the WORD DECK.
    deck_word_translits = {c["transliteration"] for c in word_cards}

    candidate_pairs = []  # list of (sign, word, source)
    # Pass A: documented logograms
    for sign, words in sign_to_logograms.items():
        for w in words:
            if w in deck_word_translits:
                candidate_pairs.append((sign, w, "documented"))
    # Pass B: phonetic-mnemonic-as-logogram
    for sign, info in phonetic_signs.items():
        if info.get("class") not in ("biliteral", "triliteral", "4plus"):
            continue
        mn = info.get("mnemonic", "").strip()
        if mn and mn in deck_word_translits:
            candidate_pairs.append((sign, mn, "phonetic"))

    # Dedupe by (sign, word) — Pass A wins over Pass B
    seen_pairs = set()
    deduped = []
    for sign, w, src in candidate_pairs:
        if (sign, w) in seen_pairs:
            continue
        seen_pairs.add((sign, w))
        deduped.append((sign, w, src))

    # Optional: prefer the documented ones; ensure broad target-word coverage
    # by spreading across distinct target words first.
    word_to_options = defaultdict(list)
    for sign, w, src in deduped:
        word_to_options[w].append((sign, src))

    # Build logogram cards: one logogram per target word (prefer documented
    # signs). Cap at ~150 cards so the logogram pool is meaningful but not
    # overwhelming.
    LOGOGRAM_CAP = 150
    logogram_cards = []
    seen_card_ids = set()
    for word in sorted(word_to_options.keys()):
        # Pick the best sign for this word, preferring documented + not
        # blocked. In family mode, skip blocked-sign logograms entirely.
        opts = sorted(word_to_options[word],
                      key=lambda so: (0 if so[1] == "documented" else 1, so[0]))
        if content_filter == "family":
            opts = [o for o in opts if o[0] not in FAMILY_BLOCKED_SIGNS]
            if not opts:
                continue
        sign, src = opts[0]
        card_id = f"log_{sign}_{safe_filename(word)}"
        if card_id in seen_card_ids:
            continue
        seen_card_ids.add(card_id)
        # Look up description: from logograms dict, signinfo desc, or phonetic db
        desc = (
            logograms.get(sign, {}).get("description")
            or sign_to_description.get(sign, "")
            or phonetic_signs.get(sign, {}).get("description", "")
        )
        # Look up word english
        wi = word_index.get(word) or {}
        word_english = wi.get("english_glosses", [])[:2]
        logogram_cards.append({
            "card_id": card_id,
            "type": "logogram",
            "sign_code": sign,
            "word_transliteration": word,
            "word_english": word_english,
            "description": desc,
            "logogram_source": src,    # "documented" or "phonetic"
            "copies": 1,
            "effect": "Instantly completes the matching word card.",
        })
        if len(logogram_cards) >= LOGOGRAM_CAP:
            break

    # ----- DETERMINATIVE SIDE DECK (optional advanced rule support) -----
    # Pick the most-used determinatives across THIS deck's words, then
    # annotate each word card with (up to 3) of its determinatives that
    # actually appear in the side deck — cards never reference a
    # classifier you can't claim.
    if determinatives is None:
        _, _, determinatives = load_sign_data()
    det_usage = Counter()
    for card in word_cards:
        for dsign in card.get("_det_candidates", []):
            det_usage[dsign] += 1
    side_det_signs = [d for d, _ in det_usage.most_common(DET_SIDE_DECK_UNIQUE)]
    side_det_set = set(side_det_signs)
    determinative_deck = []
    for rank, dsign in enumerate(side_det_signs):
        dinfo = determinatives.get(dsign) or determinatives.get(norm_sign(dsign)) or {}
        desc = (dinfo.get("description")
                or phonetic_signs.get(dsign, {}).get("description", ""))
        determinative_deck.append({
            "card_id": f"det_{dsign}",
            "type": "determinative",
            "sign_code": dsign,
            "description": desc,
            "words_in_deck_using": det_usage[dsign],
            "copies": 2 if rank < DET_SIDE_DECK_TOP_COPIES else 1,
        })
    n_words_with_dets = 0
    for card in word_cards:
        usable = [d for d in card.pop("_det_candidates", [])
                  if d in side_det_set]
        usable.sort(key=lambda d: -det_usage[d])
        if usable:
            card["appropriate_determinatives"] = usable[:3]
            n_words_with_dets += 1

    deck = {
        "name": "Middle Egyptian Hieroglyphic Card Game — Starter Set",
        "version": "1.5",
        "generated_from": "Entries2.json",
        "summary": {
            "sign_deck_unique_cards": len(sign_deck),
            "sign_deck_total_copies": sum(c["copies"] for c in sign_deck),
            "logogram_cards": len(logogram_cards),
            "word_cards": len(word_cards),
            "word_cards_by_tier": {
                tier: sum(1 for c in word_cards if c["difficulty_tier"] == tier)
                for tier in TIER_NAMES.values()
            },
            "distinct_signs_needed_by_words": len(needed_signs),
            "sign_coverage_complete": len(needed_signs - {c["sign_code"] for c in sign_deck}) == 0,
            "determinative_cards": len(determinative_deck),
            "determinative_total_copies": sum(c["copies"] for c in determinative_deck),
            "word_cards_with_determinatives": n_words_with_dets,
            "word_cards_honorific": sum(1 for c in word_cards
                                        if c.get("honorific_transposition")),
        },
        "configuration": {
            # v8.10 production ruleset — keep in sync with rules.md and
            # playtest_simulator.GameConfig defaults.
            "ruleset_version": "8.10",
            "starting_hand_size": 8,
            "hand_limit": 12,
            "points_to_win_by_player_count": {"2": 8, "3": 7, "4": 6},
            "endgame": "equal_turns_round",
            "spelling_match": "multiset",   # order does not matter
            "draw_choices": {
                "market_size": 5,
                "blind_draw": "draw 2, keep 1, discard 1 face-up",
                "discard_take_min_players": 3,
            },
            "word_draw": "draw 2 word cards, keep 1, bottom the other",  # v8.8
            "word_mulligan": "once per player per game, free action: "
                             "replace your active word (signs return to "
                             "hand, old word to bottom, draw 2 keep 1); "
                             "flip your player marker (a coin) when used",  # v8.9
            "one_sign_spellings_stripped": True,   # v8.8: logogram cards are
                                                   # the only 1-card completions
            "recycle": "instead of playing signs, discard any 2 signs "
                       "and draw 2",  # v8.10
            "steal": "complete opponent word in one continuous play only",
            "first_player_gift_signs": 0,
            "point_values_by_sign_count": POINT_VALUES,
        },
        "sign_deck": sign_deck,
        "logogram_deck": logogram_cards,
        "determinative_deck": determinative_deck,
        "word_deck": word_cards,
    }
    return deck


# ---------------------------------------------------------------------------
# Rules markdown
# ---------------------------------------------------------------------------


RULES_MD = """# Hieroglyph Quest — Middle Egyptian Hieroglyphic Card Game

A card game in which players collect hieroglyphic signs to spell out
ancient Egyptian words. The first player to the target score wins
(8 points at 2 players, 7 at 3, 6 at 4 — see "Win condition" below).

## Isis and the secret name of Ra: why names are the game

The Egyptians told a story about what it means to know a name. Ra, the
sun god, ruled everything under the sky he crossed each day, and the
deepest root of his power was his **true name** — spoken at the moment
of creation and hidden ever since, for in Egypt, to know a thing's
true name was to hold power over the thing itself. As Ra grew old, the
goddess Isis, already the greatest magician among the gods, set her
mind on the one power still beyond her. She gathered a drop of the
aging god's spittle where it fell to earth, worked it into clay, and
shaped a serpent out of Ra's own substance. It struck him on his daily
walk, and no god could cure a venom drawn from his own essence. Isis
could — for a price. Ra offered her treasure, dominion, every honor in
creation; she refused them all. Only when the poison had nearly put
out the sun did he draw her close and breathe his secret name into her
ear. She spoke it, the venom obeyed her, and Ra lived. But the name
now lived in Isis too, and with it a share of the oldest authority in
the world. Nothing was taken back; nothing could be. She left that
lakeside as "the great sorceress, mistress of the gods, who knows Ra
by his name."

The Egyptians did not treat this as only a story. A person carried two
names, one public and one guarded; a name carved in a tomb kept its
owner alive in eternity, and chiseling it away was a second, final
death. To assemble the signs of a name was to reach into the thing it
named.

That is the game in front of you. Every word card is a name waiting to
be learned. Gather the right signs, spell it out, and the word becomes
yours — knowledge scored as points. Like Isis, you don't win by being
the strongest at the table; you win by knowing the signs, waiting for
your moment, and speaking the name first.

## Components

The starter deck contains three card types:

- **Sign cards** — single Egyptian hieroglyphs with their phonetic value.
  - **Uniliterals** (1 consonant): `G17` (owl, *m*), `M17` (reed, *i*),
    `N35` (water ripple, *n*), `D21` (mouth, *r*), ...
  - **Biliterals** (2 consonants): `F35` (good-luck shape, *nfr*),
    `D2` (face, *Hr*), `Y5` (game board, *mn*), ...
  - **Triliterals** (3 consonants): `S34` (ankh, *anx*),
    `R8` (god-sign, *nTr*), `G14` (vulture, *mwt*), ...
  - **Quadriliterals+** (4+ consonants): rare, single-copy cards.

- **Logogram cards** — single signs that *are* an entire word.
  Playing one of these instantly completes the matching word card.

- **Word cards** — Middle Egyptian words you must spell with sign cards.
  Each shows the transliteration (the scholarly Romanization), the
  English meaning, the difficulty tier, the point value, and one or more
  valid sign-sequence spellings.

## Setup

1. Shuffle the **sign deck** and the **word deck** separately.
2. Each player draws **8 sign cards** into their hand, and grabs a
   **coin** (or any other object with two distinct faces) to use as
   their **player marker**. Place it face-up (heads) in front of you —
   it tracks your once-per-game **word mulligan** (v8.9, see below).
3. Each player draws **2 word cards**, keeps **one** as their face-up
   active word card, and returns the other to the **bottom** of the
   word deck (v8.8 — you always have this choice when drawing a word
   card).
4. Place the **remaining word deck** face-up in a "word reserve" pile so
   all players can see what's coming.
5. Deal **5 sign cards face-up** from the sign deck into a row beside the
   draw pile. This is the **face-up market** — the cards in it are
   available for any player to take during their draw step (v8).
6. The sign **discard pile** is kept face-up alongside the deck. The top
   card of the discard is always visible and available to take.

## Turn structure (v8)

On your turn, in this order:

1. **Draw — choose ONE source** (v8):
   - **Take 1 face-up card** from the market (any of the 5 visible
     signs/logograms), OR
   - **Take the top card** of the sign discard pile *(3+ players only —
     see "Two-player variant" below)*, OR
   - **Draw 2 from the deck face-down** and keep one; the other goes
     to the discard pile face-up.
   After a market take, immediately refill the market from the top of
   the deck so it always has 5 cards.

**Two-player variant:** in a 2-player game, the discard pile is still
face-up and reusable, but the top card cannot be taken on your turn —
only the market and the blind draw-2 are available draw sources. (With
only one opponent feeding the discard pile, the visible discards
become too reliably useful and break the balance of the game. At 3+
players the pile is more chaotic and the take is fair.)
2. **Play sign cards** onto your own active word card (toward completing
   it). You may also **steal** an opponent's active word, but only by
   playing every sign it needs in one continuous play (see "Stealing a
   word") — signs are never left sitting on an opponent's card.

   **Or recycle (v8.10):** instead of playing signs this turn, you may
   **discard any 2 signs** from your hand (face-up) and **draw 2** from
   the deck. Scribes recycle their scrap.

   **Word mulligan (free action, once per game — v8.9):** at any point
   during your turn, if your player marker is still face-up, you may
   replace your active word: take back into your hand any signs you had
   played on it, put the word card on the **bottom** of the word
   reserve, then draw a new active word as usual (draw 2, keep 1,
   bottom the other). **Flip your marker face-down** — your mulligan is
   spent for the game. Use it when your hand and your word simply
   refuse to cooperate; scribes abandoned bad drafts too.
3. **Complete?** When the signs played on a word card match the full
   set of signs of any one of its valid spellings (order does not
   matter — see "Valid spellings"), declare the word complete:
   - Take the word card and put it in your scored pile.
   - Return the sign cards used to the sign discard pile (face up).
   - Draw **2 word cards** from the reserve, keep one as your new
     active word, and return the other to the bottom of the reserve
     (v8.8).
4. **Discard** down to your hand limit of 12 cards. Discards go to the
   face-up sign discard pile, where the top card becomes available
   for the next player's draw.

## Valid spellings

Each word card lists every accepted phonetic sign-sequence. To complete
the word, you must play the **full set of signs** of any one valid
spelling. **Order does not matter**: completion is checked against the
set of signs, not their sequence. (Every balance playtest since v2 was
run under this rule; it is now the official one. It's also historically
honest — scribes arranged signs into aesthetic blocks, and sign order
was flexible in practice.) Once you complete a word, arrange the signs
in the printed order as you score it — good scribal form.

The dictionary often documents multiple spellings — you can use any of
them.

**Biliterals and triliterals count for what they represent.** A biliteral
sign covers two consonants; a triliteral covers three. So if your word
spells `nfr` and you have the `F35` (*nfr*) biliteral, playing one card
covers all three positions instead of three separate uniliterals. This is
how the Egyptians actually wrote — biliterals were the workhorse of
efficient writing.

## Stealing a word

You may steal an opponent's active word card during your turn by playing
all the signs needed to complete *their* word, in one continuous play.
Stealing rules:

- You must complete the entire word in a single continuous play, on
  your own turn. **Partial building on someone else's card is not
  allowed** — you may never leave signs on an opponent's word.
- The stealing player takes the word card and scores its points; the
  victim draws a fresh word card (draw 2, keep 1, as always).

## Logogram cards

Logograms are single signs that stand for whole words. They are powerful
and rare — and as of v8.8 they are the **only** way to complete a word
with a single card: word cards no longer list 1-sign phonetic
spellings (where the dictionary documents one, the card shows only the
longer spellings; the 1-sign writing lives on as the logogram card).

- A logogram card can only be used on a word card whose transliteration
  matches the logogram's documented word.
- Playing the logogram card instantly completes the word card, regardless
  of how many phonetic signs the word would normally require.
- After use, the logogram card goes to the discard pile.

Examples:
- `A6` (man under flowing water) logogram = the word *wab* "pure".
- `A12` (soldier with bow and quiver) logogram = the word *mSa* "army".
- `D2` (face) logogram = the word *Hr* "face".
- `N5` (sun disc) logogram = the word *ra* "sun".

## Scoring

Word points are based on the sign count of the word's shortest
**documented** spelling in the dictionary (the difficulty tier printed
on the card). Note that for trivial-tier words this is the 1-sign
writing that now lives on the matching logogram card rather than on
the word card itself (v8.8) — the tier and point value still honor it:

| Signs | Tier         | Points |
|-------|--------------|-------:|
| 1     | trivial      | 1      |
| 2     | easy         | 1      |
| 3     | medium-easy  | 2      |
| 4     | medium       | 4      |
| 5     | medium-hard  | 7      |

v7 note: tier-6 (six-sign) words are no longer included in the deck.
Simulator tuning showed they were the main cause of game-length stalls
(players assembling them rarely completed in time), so they were dropped
and their slots redistributed across tiers 1-5.

A successful steal earns the word's full point value (the victim loses
no points but loses the card and the in-progress signs).

## Win condition

The first player to reach the **target score** triggers the **endgame
round**; the player with the highest score at the end of that round
wins. The target scales by player count (v8.6):

| Players | Target points to trigger endgame |
|--------:|---------------------------------:|
| 2       | **8**                            |
| 3       | **7**                            |
| 4       | **6**                            |

**Endgame round (v8.7):** when a player first crosses the target,
finish out the round so every player has had the same number of
turns. (If the first player is seat 0, the remaining seats each take
one more turn; if it's seat 1, seat 0 has already had this round and
the round ends after the remaining seats.) When the round is complete,
whoever has the highest score wins.

**Tie-breakers** (in order): most completed words, then fewest signs
left in hand, then the earlier seat (closer to seat 0).

The 2-player target was raised from 7 to 8 because at 2p the leader can
otherwise run away with games (the simulator measured an 89%
balance score with a flat 7-point target vs. 76% with 8 points). The
4-player target was lowered from 7 to 6 to keep that count's longer
clock under 40 minutes without hurting balance. The equal-turns
endgame rule was added (v8.7) so no player is robbed of a turn — a
seat that's one play away from victory still gets to take their
turn instead of losing because seat 0 went first.

If the sign deck runs out during play, shuffle the discard pile into a
new deck and continue — the classic game always ends by reaching the
target score. (A deck-exhaustion clock exists in this game, but it
belongs to Scribes Together, the co-op mode, where racing the deck IS
the game.)

## Mix Mode (combining expansion decks — provisional)

When you own more than one themed expansion, you can shuffle their
word decks together (and their logogram piles together) for a bigger
pool. One base sign library serves any combination. Adjusted targets:

| Decks combined | Target points (2p / 3p / 4p) | Hand limit |
|---:|---|---:|
| 1 | 8 / 7 / 6 (the standard game) | 12 |
| 2 | 13 / 11 / 10 | 14 |
| 3 | 16 / 14 / 12 | 16 |

**Provisional:** these targets scale the standard ones by ×1.6 and
×2.0, a formula validated under an older ruleset. They have not yet
been re-validated under v8.8+ (faster completions, mulligan, recycle) —
treat them as starting points and adjust to taste until an updated
playtest lands.

## Optional advanced rules

- **Determinative bonus** (raise targets by 2 when using it): the deck
  includes a 24-card **determinative side pool** of silent classifier
  signs (`D54` walking legs for motion, `A2` man with hand to mouth for
  speech and eating, `A1` seated man, and so on). Lay it out face-up at
  setup. When you complete a word whose card lists appropriate
  determinatives, you may claim ONE matching determinative card from
  the pool for **+1 point**. Supplies are limited: once a classifier's
  copies are claimed, they're gone until the next game. This rule adds
  roughly 4-5 points per game, so **play to targets of 10 / 9 / 8**
  (at 2 / 3 / 4 players) instead of the standard 8 / 7 / 6 —
  simulator-validated to keep game length and comeback health intact.

- **Honorific transposition**: word cards bearing the **honorific
  marker** contain a divine or royal sign in their spelling (the
  god-sign `R8`, the sun disc `N5`, crowns, deity figures — the same
  signs are marked on their sign cards). Completing such a word earns
  +1 point IF you place the divine sign first when you arrange the
  finished word and point out why — exactly as Egyptian scribes did.
  Adds about 1 point per game; no target adjustment needed.

- **Phonetic complement bonus**: for any biliteral or triliteral you
  play, you may also play an "unnecessary" uniliteral that repeats one of
  its consonants. This is how Egyptian scribes actually wrote — it earns
  +1 point for "good handwriting".

- **Variant credit**: if a word has multiple documented spellings, you
  may complete using any one but earn +1 extra point if your spelling
  matches the canonical (shortest) form.

## Race Mode (official variant)

The "race, not theft" way to play. Nobody owns a word; everyone chases
the same open board. Use it when the table prefers racing to stealing.

**Setup changes:**

- Deal NO personal word cards, and leave the mulligan coins in your
  pocket — there are no personal words to hold or to mulligan.
- Instead, deal **5 word cards face-up** in a row in the center of the
  table: the **commission board**. All players may complete any word
  on it.

**Turn structure:** the draw step is exactly the same as the classic
game (take from the market, take the top of the discard at 3+ players,
or blind draw 2 keep 1). Then take **one** action:

- **Complete any word on the board** by playing the full set of signs
  of one of its valid spellings from your hand (order still doesn't
  matter). Score it, discard the signs used face-up, and immediately
  refill the board from the word deck.
- **Play a logogram** whose word is on the board: instant completion,
  as usual.
- **Dredge:** put one board word of your choice on the bottom of the
  word deck and refill the board from the top. Use it when the board
  has gone stale — or to bury a word you suspect an opponent is one
  card away from claiming. Dredging IS Race Mode's denial play; don't
  feel bad.
- **Recycle:** discard any 2 signs and draw 2, exactly as in the
  classic game.

End your turn by discarding down to the hand limit (12), as usual.

**No steals.** The steal rule does not exist in Race Mode — taking a
word out from under your opponent is the interaction.

**Scoring, win condition, and endgame** are unchanged (scaled targets
8/7/6, equal-turns final round).

Design notes: the board of 5 **with dredge** is the simulator-validated
configuration; without dredge, 2-player games stall badly once the easy
words are cleared (see `playtest_results/SHARED_POOL_PLAYTEST_REPORT.md`).
Expect 2-player Race Mode to run somewhat longer than the classic game;
3-4 players play at classic speed.

## Scribes Together (co-op / solo mode)

All players are one workshop of scribes racing the sands, not each
other. Works with any player count, **including 1** — this is also the
official solo mode.

**What changes from the classic game** (everything else is identical:
setup, markers, market, draw choices, recycle, word draw-2-keep-1,
mulligan):

- **One team score.** All completed words score into a single team
  total. The team wins the moment the total reaches the target (see
  the difficulty table below).
- **Steals become assists.** Completing a teammate's active word is
  encouraged — play the signs, score it for the team, and they draw a
  fresh word (draw 2, keep 1, as always). Same rule, friendlier name.
- **The loss clock:** the sign deck may only be dealt through
  **twice**. The first time it runs out, shuffle the discard pile into
  a new deck. The second time it runs out, every player takes one
  last turn with the cards in hand — then the game ends. If the team
  hasn't reached the target, the sands have won.
- **Table talk is unlimited.** Show your hands, plan together, argue
  about spellings. That's the game.

**Difficulty targets** (simulator-calibrated to roughly 90% / 60% /
30% team win rates; real coordinated teams should do a little better):

| Players | Apprentice | Scribe | Master Scribe |
|--------:|-----------:|-------:|--------------:|
| 1-2     | 9          | 15     | 19            |
| 3-4     | 13         | 19     | 25            |

Start at Apprentice for a first game, then climb. Beating Master
Scribe with the full table is meant to be rare — name the workshop
after whoever completes the winning word.

## Educational notes

- **Egyptian doesn't write vowels.** A word's transliteration shows only
  consonants, marked by either uppercase letters (`A` = aleph, `H` =
  emphatic h, `S` = "sh", etc.) or lowercase letters (the soft
  equivalents). When you read a word card you're seeing the consonant
  skeleton.

- **The same consonant sequence can mean different things.** That's why
  Egyptian writing also uses determinatives — silent end-of-word
  classifiers showing semantic category. In this game we strip
  determinatives to focus on the phonetic-matching mechanic, but the
  optional advanced rule above lets you bring them back.

- **One word, many spellings.** Egyptian scribes had choices: the same
  word could be written with just a logogram, or fully spelled out, or
  spelled out with phonetic complements. This game embraces that
  flexibility by listing multiple valid spellings per word card.

## Game design credits

Material drawn from the project's `Entries2.json` dictionary (45,492
entries, combining Faulkner, Vygus 2012/2018, Dickson, and Lexicon
sources) and `res_signinfo.js` sign reference (1,070 signs).

Sign classifications, mnemonics, and phonetic groupings derived from
Mark-Jan Nederhof's RES reference data and the standard Gardiner sign
list.
"""


def write_rules():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "rules.md", "w", encoding="utf-8") as f:
        f.write(RULES_MD)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--content-filter", choices=["family", "mature", "archaeological"],
        default="family",
        help="family (default): exclude sexual-anatomy signs + explicit "
             "glosses. mature: include everything (for After Dark expansion). "
             "archaeological: include but tag with content_warning.")
    parser.add_argument(
        "--deck-size", type=int, default=165,
        help="Total word cards in the deck (default 165, the 3-print-sheet "
             "sweet spot from playtest sweep)")
    args = parser.parse_args()

    print(f"Content filter: {args.content_filter}")
    print(f"Deck size: {args.deck_size}")
    print()
    print("Loading sign reference data...")
    phonetic_signs, logograms, determinatives = load_sign_data()
    det_set = set(determinatives.keys()) | {norm_sign(k) for k in determinatives}
    phonetic_set = set(phonetic_signs.keys())

    print(f"  phonetic signs : {len(phonetic_set):,}")
    print(f"  logograms      : {len(logograms):,}")
    print(f"  determinatives : {len(det_set):,}")

    print("\nLoading Entries2.json ...")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  {len(entries):,} entries")

    print("\nBuilding playable-word index ...")
    word_index = build_word_index(entries, phonetic_set, det_set)
    print(f"  {len(word_index):,} playable words")
    bucket_counts = Counter()
    for w in word_index.values():
        bucket_counts[w["shortest_sign_count"]] += 1
    for n in sorted(bucket_counts):
        print(f"    {n:2}-sign words: {bucket_counts[n]:5,}")

    print("\nWriting per-word JSON files ...")
    written, by_bucket = write_word_files(word_index, phonetic_signs)
    print(f"  wrote {written:,} word files")
    for b, n in sorted(by_bucket.items()):
        print(f"    {b}: {n:5,}")

    print("\nWriting rules.md ...")
    write_rules()

    print("\nBuilding deck.json ...")
    picks = scaled_picks(args.deck_size)
    deck = build_deck(word_index, phonetic_signs, logograms,
                       picks_per_tier_override=picks,
                       content_filter=args.content_filter)
    # Tag the deck file with provenance
    deck["content_filter"] = args.content_filter
    deck["target_deck_size"] = args.deck_size
    with open(OUT_DIR / "deck.json", "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    print(f"  sign deck    : {deck['summary']['sign_deck_unique_cards']} unique cards / "
          f"{deck['summary']['sign_deck_total_copies']} total copies")
    print(f"  logogram deck: {deck['summary']['logogram_cards']} cards")
    print(f"  word deck    : {deck['summary']['word_cards']} cards")
    for tier, n in deck['summary']['word_cards_by_tier'].items():
        print(f"    {tier:14}: {n} cards")

    print(f"\nGame material written to: {OUT_DIR}")


if __name__ == "__main__":
    main()
