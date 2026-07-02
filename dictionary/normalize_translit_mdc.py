"""
Normalize transliteration and MdC for internal consistency.

The audit found that most apparent variation is deliberate Egyptological
convention (variant slashes "bAgi / wrd", restored brackets "[i]rp",
uncertainty marks "?", proper-noun capitals, MdC compound joiner "&",
Gardiner variant suffixes like "Y1V" / "N35A").

Genuine inconsistencies to normalize:

  N1. Morpheme separator
      15 entries use the Egyptological middle dot U+00B7 (e.g. "pAy·i",
      "Sma·s") while 587 use a period (e.g. "sDm.n.f"). The corpus
      dominantly uses period; rewrite the 15 middle dots to periods.

  N2. Yodh notation
      1 entry contains "j" for yodh ("wab qnjt"); the entire rest of the
      corpus uses "i". Normalize the one outlier.

  N3. Dot-run normalization
      ~10 placeholder entries like "xy ....... xy" use runs of literal
      dots of varying length to represent elided material. Collapse any
      run of 4+ dots to "..." for visual consistency without losing the
      placeholder semantics.

MdC and GardinerSigns are left unchanged: their conventions differ from
each other intentionally (MdC writes "Aa15", Gardiner writes "AA15"), and
their cross-source variation reflects different graphemic representations
of the same word — also intentional.
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"

_MIDDLE_DOT = "·"            # ·
_DOT_RUN = re.compile(r"\.{4,}")  # runs of 4 or more literal dots


def normalize_translit(t: str) -> tuple[str, list[str]]:
    """Return (normalized, applied_rule_ids)."""
    if not t:
        return t, []
    applied = []
    new = t

    # N1: middle dot -> period
    if _MIDDLE_DOT in new:
        new = new.replace(_MIDDLE_DOT, ".")
        applied.append("N1")

    # N2: j -> i for yodh. Only the literal "j" character in transliteration
    # contexts where it represents yodh. Be conservative: only the one known
    # outlier. We DON'T do a blanket j->i replace because j is sometimes used
    # in compound English notation tokens we may not have seen.
    if "j" in new:
        # The audit identified exactly one match: "wab qnjt"
        new_candidate = new.replace("j", "i")
        if new == "wab qnjt":
            new = new_candidate
            applied.append("N2")

    # N3: long dot runs -> "..."
    new_after_runs, count = _DOT_RUN.subn("...", new)
    if count:
        new = new_after_runs
        applied.append("N3")

    return new, applied


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    rule_counter = Counter()
    examples = {"N1": [], "N2": [], "N3": []}

    for e in entries:
        old = e.get("Transliteration")
        new, applied = normalize_translit(old)
        if not applied:
            continue
        e["Transliteration"] = new
        for r in applied:
            rule_counter[r] += 1
            if len(examples[r]) < 4:
                examples[r].append((old, new))

    print("\n=== Normalization report ===")
    print(f"N1 middle-dot -> period : {rule_counter['N1']} entries")
    for old, new in examples["N1"][:3]:
        print(f"   {old!r:25}  ->  {new!r}")
    print(f"\nN2 j -> i (yodh)        : {rule_counter['N2']} entries")
    for old, new in examples["N2"]:
        print(f"   {old!r:25}  ->  {new!r}")
    print(f"\nN3 dot-run -> '...'     : {rule_counter['N3']} entries")
    for old, new in examples["N3"][:3]:
        print(f"   {old!r:45}  ->  {new!r}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
