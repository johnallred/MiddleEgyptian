"""
Remove the CompareWith field that was added by cleanup_1_through_9.py.

Audit revealed all 296 of those entries pointed at bibliographic references
(JEA, ZÄS, GNS, Caminos, Žába, etc.), not at word lemmas. Faulkner's "cf."
means "compare the discussion in <author/source>", not "compare with
word X" — unlike "q.v." which is a true lexical cross-reference.

Better to delete the field than leave a misleading one in place.
"""

import json
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


def main():
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    dropped = 0
    for e in entries:
        for t in e.get("Translations") or []:
            if "CompareWith" in t:
                del t["CompareWith"]
                dropped += 1
    print(f"Dropped CompareWith from {dropped} translations")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")


if __name__ == "__main__":
    main()
