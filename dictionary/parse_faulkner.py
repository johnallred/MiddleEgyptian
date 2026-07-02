"""
Merge Faulkner entries into Entries2.json with POS parsed from translation HTML.

Reads:
    Entries2.json                       (current cross-filled dump)
    ../faulkner/page17.json ... page419.json  (Faulkner-per-page scrapes)

Writes back:
    Entries2.json                       (in-place update)

What it does
------------
Faulkner translations leave PartOfSpeech null but the abbreviations sit in the
HTML translation text itself (e.g. "vb. intrans. be slack", "n. div. Osiris",
"encl. part.", "(1) adj. broad").

For each Faulkner entry we:
  1. Strip HTML tags and normalize whitespace.
  2. Skip leading sense markers like "(1)" / "(2)".
  3. Match a long list of POS abbreviations against the leading text, longest
     pattern first.
  4. Map them to the same vocabulary Vygus uses ("verb", "noun",
     "intransitive verb", "noun divinity", "enclitic particle", ...) so the
     merged file stays internally consistent.
  5. Merge the Faulkner translation into Entries2.json: if a Mongo entry with
     the same (Transliteration, GardinerSigns) exists, append; otherwise add a
     new entry preserving Faulkner's ManuelDeCodage / Res / Id.

After Faulkner is merged we re-apply the Vygus cross-fill so any Faulkner
translation whose HTML had no recognizable abbreviation but whose key matches
a Vygus entry still picks up a POS.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
ENTRIES = HERE / "Entries2.json"
FAULKNER_DIR = HERE.parent / "faulkner"

VYGUS = "2"
FAULKNER = "4"


# ---------------------------------------------------------------------------
# HTML stripping
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")
_SP = re.compile(r"\s+")


def strip_html(s: str) -> str:
    s = _TAG.sub("", s or "")
    # decode the handful of named entities Faulkner's scrape produced
    s = (
        s.replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&nbsp;", " ")
    )
    return _SP.sub(" ", s).strip()


# ---------------------------------------------------------------------------
# POS pattern table.  Longest / most-specific patterns first; first match wins.
# Each pattern is anchored at start-of-string (after leading sense markers
# such as "(1)" or "(a)" are stripped off).
# ---------------------------------------------------------------------------

_SENSE = re.compile(r"^\s*\(\s*[\dA-Za-z]+\s*\)\s*")


def _drop_sense_marker(s: str) -> str:
    # strip any number of leading "(1) " / "(a) " markers
    while True:
        new = _SENSE.sub("", s)
        if new == s:
            return s
        s = new


# Patterns are matched against the leading text after sense markers are
# stripped.  The first capture is unused — we just want to know which one fired.
POS_PATTERNS = [
    # --- compound verb forms ---
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?intrans\.", re.I), "intransitive verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?trans\.", re.I), "transitive verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?caus\.", re.I), "causative verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?recipr\.", re.I), "reciprocal verb"),
    (re.compile(r"^vb\.\s+\d+\s*[-]\s*lit\.", re.I), "verb"),         # vb. 3-lit. -> verb
    (re.compile(r"^vb\.\s+\d+\s*[-]\s*ae\.\s*gem\.", re.I), "verb"),  # vb. 2ae. gem.
    (re.compile(r"^vb\.\s+anom\.", re.I), "verb"),

    # --- compound noun forms (match Vygus's "noun X" convention) ---
    (re.compile(r"^n\.\s+div\.", re.I), "noun divinity"),
    (re.compile(r"^n\.\s+pr\.", re.I), "proper noun"),
    (re.compile(r"^n\.\s+propr\.", re.I), "proper noun"),
    (re.compile(r"^n\.\s+coll\.", re.I), "collective noun"),
    (re.compile(r"^n\.\s+loc\.", re.I), "noun location"),

    # --- pronouns ---
    (re.compile(r"^dep\.\s+pron\.", re.I), "dependent pronoun"),
    (re.compile(r"^indep\.\s+pron\.", re.I), "independent pronoun"),
    (re.compile(r"^poss\.\s+pron\.", re.I), "possessive pronoun"),
    (re.compile(r"^suff\.\s+pron\.", re.I), "suffix pronoun"),
    (re.compile(r"^demonstr\.\s+pron\.", re.I), "demonstrative pronoun"),
    (re.compile(r"^interrog\.\s+pron\.", re.I), "interrogative pronoun"),
    (re.compile(r"^pron\.", re.I), "pronoun"),
    (re.compile(r"^prn\.", re.I), "pronoun"),

    # --- particles ---
    (re.compile(r"^encl\.\s+part\.", re.I), "enclitic particle"),
    (re.compile(r"^non[- ]encl\.\s+part\.", re.I), "non-enclitic particle"),
    (re.compile(r"^proclitic\s+part\.", re.I), "proclitic particle"),
    (re.compile(r"^neg\.\s+part\.", re.I), "negative particle"),
    (re.compile(r"^interrog\.\s+part\.", re.I), "interrogative particle"),
    (re.compile(r"^part\.", re.I), "particle"),

    # --- simple categories ---
    (re.compile(r"^vb\.", re.I), "verb"),
    (re.compile(r"^verb\b", re.I), "verb"),
    (re.compile(r"^n\.", re.I), "noun"),
    (re.compile(r"^adj\.[- ]vb\.", re.I), "adjectival verb"),
    (re.compile(r"^adj\.", re.I), "adjective"),
    (re.compile(r"^adv\.", re.I), "adverb"),
    (re.compile(r"^prep\.", re.I), "preposition"),
    (re.compile(r"^conj\.", re.I), "conjunction"),
    (re.compile(r"^interj\.", re.I), "interjection"),
    (re.compile(r"^excl\.", re.I), "exclamation"),
    (re.compile(r"^interrog\.", re.I), "interrogative"),
    (re.compile(r"^imper(?:\.|ative\b)", re.I), "imperative"),
    (re.compile(r"^inf(?:\.|initive\b)", re.I), "infinitive"),
    (re.compile(r"^num(?:\.|eral\b)", re.I), "numeral"),
    (re.compile(r"^card(?:\.|inal\b)", re.I), "cardinal numeral"),
    (re.compile(r"^ord(?:\.|inal\b)", re.I), "ordinal numeral"),
]


def extract_pos(translation_html: str):
    """Return a POS string or None."""
    text = strip_html(translation_html)
    if not text:
        return None
    # Skip "var. of X" cross-references — these aren't primary entries.
    if re.match(r"^var\.\s+of\b", text, re.I):
        return None
    text = _drop_sense_marker(text)
    for rx, label in POS_PATTERNS:
        if rx.match(text):
            return label
    return None


# ---------------------------------------------------------------------------
# Cross-fill helpers (mirrors crossfill_vygus.py so the logic is in one place)
# ---------------------------------------------------------------------------


def dict_name(md):
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return str(v) if v is not None else None


def get_pos(md):
    pos = md.get("PartOfSpeech")
    return pos if pos else None


def build_vygus_index(entries):
    idx = defaultdict(Counter)
    for e in entries:
        key = (e.get("Transliteration"), e.get("GardinerSigns"))
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if dict_name(md) == VYGUS:
                pos = get_pos(md)
                if pos:
                    idx[key][pos] += 1
    return idx


def best_pos(counter):
    if not counter:
        return None
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def crossfill_from_vygus(entries):
    """Re-apply Vygus sibling + cross-entry fill. Returns count filled."""
    vygus_index = build_vygus_index(entries)
    filled = 0
    for e in entries:
        translations = e.get("Translations") or []
        if not translations:
            continue
        within = Counter()
        for t in translations:
            md = t.get("TranslationMetadata") or {}
            if dict_name(md) == VYGUS and get_pos(md):
                within[get_pos(md)] += 1
        within_pos = best_pos(within)
        key = (e.get("Transliteration"), e.get("GardinerSigns"))
        cross_pos = best_pos(vygus_index.get(key, Counter()))
        for t in translations:
            md = t.get("TranslationMetadata") or {}
            if get_pos(md) is not None:
                continue
            chosen = within_pos or cross_pos
            if chosen:
                md["PartOfSpeech"] = chosen
                t["TranslationMetadata"] = md
                filled += 1
    return filled


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl(path, entries):
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")


def load_faulkner_pages():
    rows = []
    for fn in sorted(FAULKNER_DIR.iterdir()):
        if not fn.name.endswith(".json"):
            continue
        with open(fn, "r", encoding="utf-8") as f:
            rows.extend(json.load(f))
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    entries = load_jsonl(ENTRIES)
    print(f"  loaded {len(entries):,} entries")

    print(f"Reading Faulkner pages from: {FAULKNER_DIR}")
    faulkner_entries = load_faulkner_pages()
    print(f"  loaded {len(faulkner_entries):,} Faulkner entries")

    # Index existing entries by (translit, gardiner) so we can merge in O(1).
    by_key = defaultdict(list)
    for e in entries:
        by_key[(e.get("Transliteration"), e.get("GardinerSigns"))].append(e)

    pos_label_counter = Counter()
    pos_extracted = 0
    pos_unrecognized = 0
    merged = 0
    appended_to_existing = 0

    for fe in faulkner_entries:
        translation_dict = fe.get("Translations") or {}
        # The per-page format stores Translations as a SINGLE dict; the
        # Mongo dump uses a LIST.  Normalize to a list before merging.
        if isinstance(translation_dict, list):
            translation_list = translation_dict
        else:
            translation_list = [translation_dict] if translation_dict else []

        # Parse POS from the HTML for each translation we're about to inject.
        for t in translation_list:
            md = t.get("TranslationMetadata") or {}
            if get_pos(md) is None:
                pos = extract_pos(t.get("translation", ""))
                if pos:
                    md["PartOfSpeech"] = pos
                    t["TranslationMetadata"] = md
                    pos_extracted += 1
                    pos_label_counter[pos] += 1
                else:
                    pos_unrecognized += 1

        key = (fe.get("Transliteration"), fe.get("GardinerSigns"))
        existing = by_key.get(key)
        if existing:
            # Append our translation(s) to the FIRST matching entry's list.
            host = existing[0]
            host_translations = host.get("Translations") or []
            host_translations.extend(translation_list)
            host["Translations"] = host_translations
            appended_to_existing += 1
        else:
            # Add as a brand-new entry. Normalize Translations to a list.
            new_entry = dict(fe)
            new_entry["Translations"] = translation_list
            entries.append(new_entry)
            by_key[key].append(new_entry)
            merged += 1

    print("\n=== Faulkner parse + merge ===")
    print(f"POS extracted from HTML : {pos_extracted:,}")
    print(f"POS not found in HTML   : {pos_unrecognized:,}")
    print(f"Appended to existing key: {appended_to_existing:,}")
    print(f"Added as new entry      : {merged:,}")
    print(f"Top POS labels assigned :")
    for label, n in pos_label_counter.most_common(15):
        print(f"  {n:5}  {label}")

    # Final cross-fill pass: any Faulkner translation still null but whose
    # (translit, gardiner) matches a Vygus entry inherits the Vygus POS.
    cross_filled = crossfill_from_vygus(entries)
    print(f"\nAdditional Vygus cross-fills after merge: {cross_filled:,}")

    print(f"\nWriting: {ENTRIES}")
    write_jsonl(ENTRIES, entries)
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
