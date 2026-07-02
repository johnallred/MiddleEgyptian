"""
One-off corrector for the multi-word `feminine noun` / `plural noun` mistakes
introduced by the first morphology pass.

The original morphology_pass.py inspected the last character of the entry's
transliteration to decide whether the morpheme was the Egyptian feminine -t or
plural -w. For multi-word entries (e.g. "iry at" = "hall-keeper") that
character belongs to the SECOND word ("at"), not the headword, so the entry
was labeled `feminine noun` even though the head noun "iry" is masculine.

This script:
  1. Loads Entries2.json.
  2. Finds translations whose POS is `feminine noun` or `plural noun` AND
     whose entry has a multi-word transliteration.
  3. Resets each such POS to null.
  4. Re-runs the corrected classifier from morphology_pass.py (which now
     restricts R5/R6/R7 to single-word transliterations); multi-word entries
     can still match R1/R3/R4/R8, falling through to noun/verb/preposition.
  5. Writes Entries2.json back in place.

`adjective` could also have been mis-assigned on multi-word translits, but
Vygus and Faulkner both use "adjective" as a valid POS too, so we don't
revert those without being able to tell ours apart.
"""

import json
from collections import Counter
from pathlib import Path

import morphology_pass as mp  # reuse classify(), first_gloss()

ENTRIES = Path(__file__).parent / "Entries2.json"
TARGET_LABELS = {"feminine noun", "plural noun"}


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]

    reverted = Counter()
    relabel = Counter()
    relabel_rule = Counter()
    still_null = 0
    samples = []

    for e in entries:
        translit = e.get("Transliteration", "")
        if " " not in translit.strip():
            continue
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            pos = md.get("PartOfSpeech")
            if pos in TARGET_LABELS:
                reverted[pos] += 1
                md["PartOfSpeech"] = None
                # Re-classify with the corrected rules.
                new_pos, rule = mp.classify(translit, t.get("translation", ""))
                if new_pos:
                    md["PartOfSpeech"] = new_pos
                    relabel[new_pos] += 1
                    relabel_rule[rule] += 1
                    if len(samples) < 8:
                        samples.append(
                            (translit,
                             mp.first_gloss(t.get("translation", ""))[:80],
                             pos, new_pos)
                        )
                else:
                    still_null += 1
                t["TranslationMetadata"] = md

    print("\nReverted (mis-labeled multi-word entries):")
    for label, n in reverted.most_common():
        print(f"  {n:5}  {label}")
    print(f"\nRe-labeled by corrected rules:")
    for label, n in relabel.most_common():
        print(f"  {n:5}  -> {label}")
    print(f"  ({still_null} could not be re-classified and were left null)")

    print("\nWhich corrected rule fired:")
    for rule, n in relabel_rule.most_common():
        print(f"  {n:5}  {rule}")

    print("\nSample relabelings:")
    for translit, gloss, old, new in samples:
        print(f"  {translit:25}  {old} -> {new}  | {gloss}")

    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"\nWrote {len(entries):,} entries back to {ENTRIES.name}")


if __name__ == "__main__":
    main()
