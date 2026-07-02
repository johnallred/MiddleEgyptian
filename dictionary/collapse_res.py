"""
Collapse the Res / ResAuto / ResSource trio down to a single Res field.

After verifying the converter port at 99.9% fidelity, we trust ResAuto and
overwrite Res with it. The 11 entries where curated Res disagreed with the
converter are normalized to the converter's output (e.g. F37Aa is lowercased
to F37aa, matching the C# postprocessor's behavior).

Result: every entry has exactly one Res field, no parallel ResAuto, no
ResSource flag. Reversible by re-running generate_res.py if needed.
"""

import json
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    overwritten = 0
    auto_removed = 0
    source_removed = 0
    for e in entries:
        auto = e.get("ResAuto")
        if auto is not None:
            if e.get("Res") != auto:
                overwritten += 1
            e["Res"] = auto
            del e["ResAuto"]
            auto_removed += 1
        if "ResSource" in e:
            del e["ResSource"]
            source_removed += 1

    print(f"\nRes values overwritten by ResAuto (the 11 mismatches): {overwritten}")
    print(f"ResAuto fields removed:    {auto_removed:,}")
    print(f"ResSource fields removed:  {source_removed:,}")

    # Sanity: every entry should still have a populated Res
    res_populated = sum(1 for e in entries if e.get("Res"))
    print(f"\nRes populated after collapse: {res_populated:,} / {len(entries):,}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
