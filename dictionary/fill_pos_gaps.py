"""
Target the remaining true POS gaps in Entries2.json.

After all previous passes, 5,297 translations still have null PartOfSpeech
and 203 more have PartOfSpeech but no PartOfSpeechCore (prose labels).

Strategy:

  P1. Sibling fill (any source).
      The original Vygus cross-fill only copied POS FROM Vygus translations.
      But many null-POS translations have a non-Vygus sibling with a
      perfectly good POS (Dickson, Lexicon, or Faulkner). Audit shows 328
      such cases. Copy the most common sibling POS to the null one.

  P2. Translit-only cross-entry consensus.
      3,595 null-POS translations have the same Transliteration appearing
      in another entry that DOES have a POS. When all attestations of a
      transliteration unanimously share a single core POS, copy it. Skip
      ambiguous cases where the cross-entry POS values disagree.

  P3. Targeted gloss rules for the residue.

      (a) "(unknown)" gloss -> POS = "unknown" (definitive marker that
          the meaning, and likely the POS, is irrecoverable).
      (b) "(a X)" / "(an X)" / "kind of X" / "name of X" / "type of X"
          gloss start -> noun. (Some were caught in earlier pass with
          strict article-only rules; this also handles the parenthesized
          variants.)
      (c) "who X" / "what X" / "which X" / "those who X" / "he who X"
          gloss start -> noun. Egyptian participial forms used
          substantively are treated as nouns by Egyptological convention.
      (d) Gloss first letter uppercase (proper noun) -> proper noun.
      (e) Single English adjective-form gloss -> adjective (using an
          expanded adjective list).
      (f) Single English noun-form gloss (lowercase first letter, not
          starting with verb word, no spaces) -> noun.

  P4. Prose-label core POS rescue. Extend the COMPOUND_RESCUE table to
      cover the 203 prose-style labels that have no structured core:
      "stative past tense" -> verb, "negation" -> particle,
      "auxillary verb with past meaning" -> verb, etc.

Each pass only fills NULL fields; existing POS values are never overwritten.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def dn(md: dict):
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return v


def first_gloss(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text or "").strip()
    return s.split(",")[0].split(";")[0].split(":")[0].strip()


def normalize_pos(pos: str) -> str:
    return pos.strip().lower() if pos else ""


# ---------------------------------------------------------------------------
# P1 + P2: cross-fill helpers
# ---------------------------------------------------------------------------


def best_pos(counter: Counter) -> str | None:
    """Most common POS string, tie-broken alphabetically for determinism."""
    if not counter:
        return None
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def collect_sibling_pos(translations: list) -> Counter:
    """Count POS values across siblings."""
    c = Counter()
    for t in translations:
        md = t.get("TranslationMetadata") or {}
        pos = md.get("PartOfSpeech")
        if pos:
            c[pos] += 1
    return c


# ---------------------------------------------------------------------------
# P3: gloss rules
# ---------------------------------------------------------------------------

_PAREN_NOUN_HEADS = (
    "a ", "an ", "the ",
    "kind of ", "name of ", "type of ", "sort of ", "species of ",
    "variety of ", "title of ",
)

# Egyptian participial-noun glosses
_PARTICIPIAL_NOUN_HEADS = (
    "who ", "what ", "which ", "those who", "he who", "she who",
    "one who", "ones who", "those whom", "they who",
    "the one ", "the ones ",
)


def gloss_rule(translit: str, gloss_text: str) -> tuple[str | None, str | None]:
    """Return (PartOfSpeech, PartOfSpeechCore) for the gloss, or (None, None)."""
    g = first_gloss(gloss_text)
    if not g:
        return None, None

    g_low = g.lower()
    g_low_stripped = g_low.strip().strip("()")  # strip a surrounding paren

    # (a) (unknown)
    if g.strip().lower() in {"(unknown)", "unknown"}:
        return "unknown", "unknown"

    # (b) Article-led noun (including parenthesized: "(a X)", "(an X)")
    for head in _PAREN_NOUN_HEADS:
        if g_low.startswith(head):
            return "noun", "noun"
        if g_low_stripped.startswith(head):
            return "noun", "noun"

    # (c) Participial / relative noun
    for head in _PARTICIPIAL_NOUN_HEADS:
        if g_low.startswith(head):
            return "noun", "noun"

    # (d) Capitalized first letter (proper noun)
    # Only if the gloss is a single concrete-looking phrase (not all-caps).
    if g and g[0].isupper() and not g.isupper() and " " in g[:30]:
        # E.g. "Sothis", "Eye of Horus", "Lord of the Two Lands"
        return "proper noun", "noun"

    return None, None


# Curated adjective lookup for single-word adjective glosses.
_ENG_ADJECTIVES = {
    "great", "small", "big", "little", "long", "short", "tall", "broad",
    "wide", "narrow", "deep", "shallow", "high", "low", "good", "bad",
    "evil", "fine", "fair", "beautiful", "ugly", "red", "white", "black",
    "green", "blue", "yellow", "bright", "dark", "old", "young", "new",
    "ancient", "strong", "weak", "rich", "poor", "noble", "wealthy",
    "holy", "sacred", "pure", "clean", "dirty", "hot", "cold", "warm",
    "wet", "dry", "hard", "soft", "heavy", "light", "right", "true",
    "false", "real", "sweet", "bitter", "sour", "joyful", "joyous",
    "happy", "sad", "angry", "fearful", "afraid", "quiet", "silent",
    "loud", "exalted", "supreme", "first", "last", "many", "much",
    "few", "successful", "skilful", "skillful", "wise", "foolish",
    "splendid", "famous", "favourable", "favorable", "former",
    "perfect", "complete", "ready", "open", "shut", "closed",
    "alive", "dead", "free", "favoured", "favored", "blessed",
    "powerful", "weary", "tired", "fresh", "stale",
}

# Curated English verb forms — bare gloss = verb. These are the most common
# Egyptian-dictionary verb glosses written as bare English infinitives.
_ENG_BARE_VERBS = {
    "be", "do", "go", "say", "make", "come", "take", "give", "see", "hear",
    "die", "live", "rise", "fall", "run", "fly", "eat", "drink", "sit",
    "stand", "walk", "speak", "look", "find", "send", "bring", "carry",
    "cause", "let", "build", "open", "shut", "close", "lift", "raise",
    "spread", "shine", "weep", "smell", "praise", "fight", "kill", "beat",
    "stir", "knead", "rejoice", "embrace", "flee", "depart", "enter",
    "leave", "return", "appear", "become", "begin", "end", "seek", "guard",
    "follow", "lead", "command", "destroy", "create", "fashion", "shape",
    "form", "save", "rescue", "throw", "place", "set", "put", "wash",
    "clean", "wear", "drive", "anoint", "fill", "empty", "pour",
    "neglect", "test", "prove", "answer", "ask", "tell", "name", "call",
    "release", "untie", "tie", "bind", "loose", "draw", "pull", "push",
    "hold", "grasp", "seize", "catch",
    "pound", "cut", "trim", "scratch", "carve", "engrave", "steal", "rob",
    "march", "travel", "fall", "sleep", "wake",
}


def gloss_single_word_rule(translit: str, gloss_text: str) -> tuple[str | None, str | None]:
    g = first_gloss(gloss_text)
    if not g:
        return None, None
    g_low = g.lower().strip(".")
    if " " in g or "-" in g:
        return None, None
    if not g_low.isalpha():
        return None, None
    if g_low in _ENG_ADJECTIVES:
        return "adjective", "adjective"
    if g_low in _ENG_BARE_VERBS:
        return "verb", "verb"
    # Default: lowercase single English word that isn't a verb -> noun.
    # (Egyptian dictionary convention.)
    if g[0].islower():
        return "noun", "noun"
    return None, None


# ---------------------------------------------------------------------------
# P4: extended prose-label rescue
# ---------------------------------------------------------------------------

EXTENDED_COMPOUND_RESCUE = {
    "stative past tense":           ("verb",   ["stative", "past"],   [], None),
    "stative plural past tense":    ("verb",   ["stative", "plural", "past"], [], None),
    "causative intransitive":       ("verb",   ["causative", "intransitive"], [], None),
    "auxillary verb with past meaning": ("verb", ["auxiliary", "past"], [], None),
    "auxiliary verb with past meaning": ("verb", ["auxiliary", "past"], [], None),
    "negation":                     ("particle", ["negative"], [], None),
    "late egyptian":                ("noun",   [], ["late egyptian"], None),
    "negative":                     ("particle", ["negative"], [], None),
    "compound":                     ("noun",   [], [], "Compound expression"),
    "stative":                      ("verb",   ["stative"], [], None),
    "noun plural of ky":            ("noun",   ["plural"], [], "Plural of ky"),
    "adverb used after an imperative": ("adverb", [], [], None),
    "written":                      ("noun",   [], [], "Written/spelled variant"),
    "variant of next below":        ("noun",   [], [], "Variant of following entry"),
    "spelling":                     ("noun",   [], [], "Spelling variant"),
    "adjective and verb":           ("adjective", [], [], "Polysemous adjective/verb"),
    "prepostion with suffixes":     ("preposition", ["suffix"], [], None),
    "preposition with suffixes":    ("preposition", ["suffix"], [], None),
    "1/320th HqAt":                 ("numeral", [], [], "Volume unit, 1/320 of a HqAt"),
    "1st suffixes":                 ("pronoun", ["suffix"], [], "1st person suffix pronoun"),
    "1st person":                   ("pronoun", [], [], "1st person pronoun"),
    "3rd person":                   ("pronoun", [], [], "3rd person pronoun"),
    "stative perfective":           ("verb",   ["stative", "perfective"], [], None),
    "stative imperfective":         ("verb",   ["stative", "imperfective"], [], None),
}


def extended_rescue(label: str):
    if not label:
        return None
    return EXTENDED_COMPOUND_RESCUE.get(label.strip().lower())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ----- Build translit -> POS counter for P2 -----
    translit_pos: dict[str, Counter] = defaultdict(Counter)
    translit_core: dict[str, Counter] = defaultdict(Counter)
    for e in entries:
        translit = e.get("Transliteration", "")
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            pos = md.get("PartOfSpeech")
            core = md.get("PartOfSpeechCore")
            if pos:
                translit_pos[translit][pos] += 1
            if core:
                translit_core[translit][core] += 1

    # ----- P1: sibling fill (any source) -----
    p1_filled = 0
    for e in entries:
        ts = e.get("Translations") or []
        sib_pos = collect_sibling_pos(ts)
        if not sib_pos:
            continue
        chosen = best_pos(sib_pos)
        if not chosen:
            continue
        for t in ts:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            md["PartOfSpeech"] = chosen
            t["TranslationMetadata"] = md
            p1_filled += 1

    print(f"\nP1 sibling fill (any source): {p1_filled:,}")

    # ----- P2: translit-only cross-entry consensus -----
    # Only apply when the transliteration has a SINGLE dominant POS across
    # all other entries (no disagreement on core POS).
    p2_filled = 0
    p2_skipped_ambiguous = 0
    for e in entries:
        translit = e.get("Transliteration", "")
        if not translit:
            continue
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            available = translit_pos.get(translit, Counter())
            if not available:
                continue
            cores = translit_core.get(translit, Counter())
            # Only fill when core POS is unanimous across attestations.
            if len(cores) != 1:
                p2_skipped_ambiguous += 1
                continue
            chosen = best_pos(available)
            md["PartOfSpeech"] = chosen
            t["TranslationMetadata"] = md
            p2_filled += 1

    print(f"P2 translit cross-fill (unanimous): {p2_filled:,}")
    print(f"   skipped (ambiguous translit) : {p2_skipped_ambiguous:,}")

    # ----- P3: gloss rules -----
    p3_filled = 0
    p3_by_rule = Counter()
    for e in entries:
        translit = e.get("Transliteration", "")
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            text = t.get("translation", "") or ""
            pos, core = gloss_rule(translit, text)
            if pos is None:
                pos, core = gloss_single_word_rule(translit, text)
            if pos:
                md["PartOfSpeech"] = pos
                if not md.get("PartOfSpeechCore"):
                    md["PartOfSpeechCore"] = core
                t["TranslationMetadata"] = md
                p3_filled += 1
                p3_by_rule[pos] += 1

    print(f"P3 gloss rules: {p3_filled:,}")
    for pos, n in p3_by_rule.most_common():
        print(f"   -> {pos}: {n}")

    # ----- P4: extended prose-label core POS rescue -----
    p4_filled = 0
    p4_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            label = md.get("PartOfSpeech")
            if not label or md.get("PartOfSpeechCore"):
                continue
            rescue = extended_rescue(label)
            if not rescue:
                continue
            core, mods, doms, note = rescue
            md["PartOfSpeechCore"] = core
            if mods:
                existing = list(md.get("Modifiers") or [])
                for m in mods:
                    if m not in existing:
                        existing.append(m)
                md["Modifiers"] = sorted(existing)
            if doms:
                existing = list(md.get("Domains") or [])
                for d in doms:
                    if d not in existing:
                        existing.append(d)
                md["Domains"] = sorted(existing)
            if note and not md.get("Notes"):
                md["Notes"] = note
            t["TranslationMetadata"] = md
            p4_filled += 1
            if len(p4_examples) < 4:
                p4_examples.append((label, core))

    print(f"\nP4 prose-label core rescue: {p4_filled:,}")
    for raw, core in p4_examples:
        print(f"   {raw!r} -> core={core!r}")

    # ----- Write -----
    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
