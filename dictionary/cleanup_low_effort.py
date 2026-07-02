"""
Low-effort, high-value cleanups on Entries2.json.

Performed in one pass, in place:

  C1  POS truncation fix
        "clo" was a truncation of "clothing" introduced by the original
        Vygus parser. Replace every "clo" token inside a PartOfSpeech
        value (1,406 occurrences across ~22 distinct composite labels:
        "noun clo", "dual noun clo", "causative verb clo", etc.).

  C2  POS hyphenation normalization
        Unify "non enclitic particle" (41 entries) and
        "non-enclitic particle" (33) on the hyphenated form.

  C3  DictionaryName format unification
        The Mongo dump uses BSON extended JSON ({"$numberInt": "2"}),
        the Faulkner per-page files use bare ints (4). Normalize all to
        bare ints — valid relaxed extended JSON, every consumer accepts
        both, the file shrinks.

  C4  Transliteration whitespace
        Trim leading/trailing whitespace and collapse runs of internal
        spaces on the Transliteration field (25 affected).

  C5  Stray leading dash in one translation
        One translation literally starts with "- nurse"; drop the dash.

The script reports counts and samples before writing so the impact is
auditable.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"

# C1: token-level replacement so we catch every composite POS label.
POS_TOKEN_FIXES = {
    "clo": "clothing",
}

# C2: full-string replacements for POS variants that need merging.
POS_STRING_REWRITES = {
    "non enclitic particle": "non-enclitic particle",
}

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def fix_pos(pos: str | None) -> str | None:
    if not pos:
        return pos
    if pos in POS_STRING_REWRITES:
        return POS_STRING_REWRITES[pos]
    tokens = pos.split(" ")
    fixed = [POS_TOKEN_FIXES.get(tok, tok) for tok in tokens]
    return " ".join(fixed)


def normalize_dict_name(v):
    """Convert {"$numberInt": "2"} -> 2.  Leave plain int unchanged."""
    if isinstance(v, dict):
        for key in ("$numberInt", "$numberLong"):
            if key in v:
                try:
                    return int(v[key])
                except (TypeError, ValueError):
                    return v[key]
    return v


def normalize_translit(s: str) -> str:
    if not s:
        return s
    return _WS.sub(" ", s.strip())


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    c1_changes = Counter()         # old POS -> count
    c1_to_new = {}                 # old -> new mapping seen
    c2_changes = 0
    c3_changes = 0
    c4_changes = 0
    c4_samples = []
    c5_changes = 0
    c5_samples = []

    for e in entries:
        # C4: transliteration whitespace
        translit_before = e.get("Transliteration", "")
        translit_after = normalize_translit(translit_before)
        if translit_before != translit_after:
            c4_changes += 1
            if len(c4_samples) < 5:
                c4_samples.append((repr(translit_before), repr(translit_after)))
            e["Transliteration"] = translit_after

        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}

            # C1 + C2: POS rewrites
            pos = md.get("PartOfSpeech")
            new_pos = fix_pos(pos)
            if new_pos != pos:
                if pos in POS_STRING_REWRITES:
                    c2_changes += 1
                else:
                    c1_changes[pos] += 1
                    c1_to_new[pos] = new_pos
                md["PartOfSpeech"] = new_pos

            # C3: DictionaryName format
            dn = md.get("DictionaryName")
            new_dn = normalize_dict_name(dn)
            if new_dn != dn:
                c3_changes += 1
                md["DictionaryName"] = new_dn

            t["TranslationMetadata"] = md

            # C5: stray leading dash in a translation
            text = t.get("translation", "") or ""
            stripped = _WS.sub(" ", _TAG.sub("", text)).strip()
            if re.match(r"^-\s+[A-Za-z]", stripped):
                # Only act when the dash is leading, followed by whitespace
                # and a word: e.g. "- nurse". Don't touch en/em-dashes,
                # which are meaningful compound markers in Faulkner.
                new_text = re.sub(r"^\s*-\s+", "", text, count=1)
                if new_text != text:
                    c5_changes += 1
                    if len(c5_samples) < 5:
                        c5_samples.append((text[:60], new_text[:60]))
                    t["translation"] = new_text

    # ----- Report ------------------------------------------------------------
    print("\n=== Cleanup report ===")

    print(f"\nC1 POS token rewrites ({sum(c1_changes.values()):,} translations):")
    for old, n in c1_changes.most_common():
        print(f"  {n:5}  {old!r:40} -> {c1_to_new[old]!r}")

    print(f"\nC2 POS hyphenation normalization: {c2_changes:,} translations")

    print(f"\nC3 DictionaryName format normalization: {c3_changes:,} fields")

    print(f"\nC4 Transliteration whitespace fixes: {c4_changes}")
    for before, after in c4_samples:
        print(f"  {before:30} -> {after}")

    print(f"\nC5 Stray leading dash in translation: {c5_changes}")
    for before, after in c5_samples:
        print(f"  before: {before!r}")
        print(f"  after : {after!r}")

    # ----- Write -------------------------------------------------------------
    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
