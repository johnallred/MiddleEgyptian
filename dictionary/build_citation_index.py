"""
Build CitationIndex.json from the `Citations` arrays inside Entries2.json.

This is the inverted concordance: given a source text and a location
(e.g. "Urkunden" "IV, 425, 8"), list every dictionary entry attested there.

Structure
---------
{
  "_meta": {
    "generated_from": "Entries2.json",
    "total_sources": N,
    "total_unique_locations": M,
    "total_entry_citations": K
  },
  "sources": {
    "Urkunden": {
      "IV, 425, 8": [
        {
          "transliteration": "qd",
          "gardiner": "A35 A24",
          "entry_id": "628573...",
          "gloss": "build, fashion men, construct..."
        }
      ],
      ...
    },
    "Sinuhe": {
      "B70": [...]
    }
  }
}

Notes
-----
- Location keys are flat: when a citation has a volume the key is
  "<volume>, <location>" (e.g. "IV, 425, 8"); otherwise just the location
  string. This means a single `index[source][location]` lookup works for
  every source.
- Citations whose source could not be resolved (no SOURCE_MAP entry) are
  filed under the raw abbreviation. They'll show up at the bottom of the
  output for triage.
- Within a location, entries are deduplicated by entry_id and sorted by
  transliteration for deterministic output.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "Entries2.json"
DST = HERE / "CitationIndex.json"

_WS = re.compile(r"\s+")


def entry_id(e: dict) -> str | None:
    """Best-effort durable identifier for the entry."""
    _id = e.get("_id")
    if isinstance(_id, dict):
        return _id.get("$oid") or _id.get("$numberLong")
    if isinstance(_id, str):
        return _id
    # Faulkner-style Mongo ObjectId components, if present
    if isinstance(_id, dict) and "Increment" in _id:
        return str(_id.get("Increment"))
    return None


def location_key(c: dict) -> str:
    """Combine volume (if any) with location into a single flat key."""
    loc = (c.get("location") or "").strip()
    vol = (c.get("volume") or "").strip()
    if vol and loc:
        return f"{vol}, {loc}"
    return vol or loc


def gloss_preview(text: str, n: int = 80) -> str:
    text = _WS.sub(" ", text or "").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def location_sort_key(loc: str):
    """Sort key: leading Roman volume, then leading integer, then string."""
    roman = re.match(r"^([IVX]+)\b", loc)
    rest = loc[roman.end():].lstrip(", ") if roman else loc
    roman_val = 0
    if roman:
        roman_val = sum(
            {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}[c]
            for c in roman.group(1)
        )
        # Crude subtractive correction so IV<V<VI; close enough for sort.
        for i, c in enumerate(roman.group(1)[:-1]):
            if {"I": 1, "V": 5, "X": 10}[c] < {"I": 1, "V": 5, "X": 10}[roman.group(1)[i + 1]]:
                roman_val -= 2 * {"I": 1, "V": 5, "X": 10}[c]
    m = re.match(r"^[A-Z]?(\d+)", rest)
    int_val = int(m.group(1)) if m else 10**9
    return (roman_val, int_val, loc)


def main():
    print(f"Reading: {SRC}")
    with open(SRC, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # source -> location_key -> {entry_id: entry_ref}
    index: dict[str, dict[str, dict[str, dict]]] = defaultdict(lambda: defaultdict(dict))
    total_citations = 0

    for e in entries:
        eid = entry_id(e)
        translit = e.get("Transliteration", "")
        gardiner = e.get("GardinerSigns", "")
        for t in e.get("Translations") or []:
            cits = t.get("Citations") or []
            if not cits:
                continue
            gloss = gloss_preview(t.get("translation", ""))
            for c in cits:
                total_citations += 1
                source = c.get("source") or c.get("abbreviation")  # fall back
                if not source:
                    continue
                loc = location_key(c)
                if not loc:
                    continue
                ref_key = eid or f"{translit}|{gardiner}"
                # First write wins per (source, location, entry); preserves
                # the gloss from whichever translation cited it first.
                if ref_key not in index[source][loc]:
                    index[source][loc][ref_key] = {
                        "transliteration": translit,
                        "gardiner": gardiner,
                        "entry_id": eid,
                        "gloss": gloss,
                    }

    # ---- Materialize to sorted, plain dicts/lists -------------------------
    sources_out: dict[str, dict[str, list[dict]]] = {}
    src_loc_count = Counter()
    src_ref_count = Counter()
    for source in sorted(index.keys()):
        locations = index[source]
        locs_sorted = sorted(locations.keys(), key=location_sort_key)
        loc_dict: dict[str, list[dict]] = {}
        for loc in locs_sorted:
            refs = list(locations[loc].values())
            refs.sort(key=lambda r: (r["transliteration"], r["gardiner"]))
            loc_dict[loc] = refs
            src_loc_count[source] += 1
            src_ref_count[source] += len(refs)
        sources_out[source] = loc_dict

    total_unique_refs = sum(src_ref_count.values())
    out = {
        "_meta": {
            "generated_from": SRC.name,
            "total_sources": len(sources_out),
            "total_unique_locations": sum(src_loc_count.values()),
            "total_citation_records_processed": total_citations,
            "total_entry_citation_edges": total_unique_refs,
        },
        "sources": sources_out,
    }

    print("\n=== Citation index summary ===")
    print(f"Sources                       : {out['_meta']['total_sources']}")
    print(f"Unique locations              : {out['_meta']['total_unique_locations']:,}")
    print(f"Citation records processed    : {total_citations:,}")
    print(f"Distinct (source, location, entry) edges: {total_unique_refs:,}")

    print("\nTop 12 sources by location count:")
    for src, n in src_loc_count.most_common(12):
        refs = src_ref_count[src]
        print(f"  {n:5} locs  {refs:5} entry refs  {src}")

    # Top most-cited single locations
    flat = []
    for src, locs in sources_out.items():
        for loc, refs in locs.items():
            flat.append((len(refs), src, loc))
    flat.sort(reverse=True)
    print("\nTop 10 most-cited single locations (entries attested in one place):")
    for n, src, loc in flat[:10]:
        print(f"  {n:4} entries  {src}: {loc}")

    print(f"\nWriting: {DST}")
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"  wrote {DST.name}")


if __name__ == "__main__":
    main()
