"""
Cross-fill Part-of-Speech from Vygus into other dictionaries' entries.

Reads:  Entries.json   (MongoDB-style JSONL dump of dictionary entries)
Writes: Entries2.json  (same shape, with PartOfSpeech filled where possible)

Strategy
--------
Each entry has Transliteration, GardinerSigns, and a Translations list whose
items carry TranslationMetadata.{PartOfSpeech, DictionaryName}.

DictionaryName values observed:
    0 = Lexicon, 1 = Dickson, 2 = Vygus, 4 = Faulkner.

We only borrow POS from Vygus (the only source with high POS coverage today),
and only fill translations whose PartOfSpeech is null/empty. The original
Vygus translations are left untouched.

Two passes per entry:
  1. Within-entry fill: if any sibling translation in the same entry is Vygus
     and carries a POS, use it for the entry's other null-POS translations.
  2. Cross-entry fill: for translations still null, look up the entry's
     (Transliteration, GardinerSigns) in a global index of Vygus POS values
     and copy the most common one.

Ambiguity handling: when multiple Vygus POS strings exist for the same key,
we copy the most common; ties are broken by lexicographic order so output is
deterministic. Each fill is logged so the operation is auditable.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "Entries.json"
DST = HERE / "Entries2.json"

VYGUS = "2"  # DictionaryName for Vygus


def dict_name(md):
    """Normalize DictionaryName which appears as int or {'$numberInt': '2'}."""
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return str(v) if v is not None else None


def get_pos(md):
    pos = md.get("PartOfSpeech")
    return pos if pos else None  # treat "" and None alike


def read_entries(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def build_vygus_index(entries):
    """(Transliteration, GardinerSigns) -> Counter of Vygus POS strings."""
    idx = defaultdict(Counter)
    for e in entries:
        key = (e.get("Transliteration"), e.get("GardinerSigns"))
        for t in e.get("Translations", []) or []:
            md = t.get("TranslationMetadata") or {}
            if dict_name(md) == VYGUS:
                pos = get_pos(md)
                if pos:
                    idx[key][pos] += 1
    return idx


def best_pos(counter):
    """Most common POS, ties broken alphabetically for determinism."""
    if not counter:
        return None
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def crossfill(entry, vygus_index, stats):
    """
    Mutates entry in place. Returns nothing.
    stats is a dict accumulator updated as we fill.
    """
    translations = entry.get("Translations", []) or []
    if not translations:
        return

    # Pass 1: within-entry Vygus POS, if any.
    within_pos_counter = Counter()
    for t in translations:
        md = t.get("TranslationMetadata") or {}
        if dict_name(md) == VYGUS:
            pos = get_pos(md)
            if pos:
                within_pos_counter[pos] += 1
    within_pos = best_pos(within_pos_counter)

    # Pass 2: cross-entry Vygus POS lookup.
    key = (entry.get("Transliteration"), entry.get("GardinerSigns"))
    cross_pos = best_pos(vygus_index.get(key, Counter()))

    for t in translations:
        md = t.get("TranslationMetadata") or {}
        if get_pos(md) is not None:
            continue  # leave existing POS alone
        src = dict_name(md)
        chosen = within_pos or cross_pos
        if not chosen:
            stats["unfilled"][src] += 1
            continue
        md["PartOfSpeech"] = chosen
        # ensure the key is written back even if metadata was reconstructed
        t["TranslationMetadata"] = md
        if within_pos:
            stats["filled_within"][src] += 1
        else:
            stats["filled_cross"][src] += 1


def main():
    print(f"Reading: {SRC}")
    entries = list(read_entries(SRC))
    print(f"Loaded {len(entries):,} entries")

    print("Building Vygus POS index...")
    vygus_index = build_vygus_index(entries)
    print(f"  index size: {len(vygus_index):,} unique (translit, gardiner) keys")

    stats = {
        "filled_within": Counter(),
        "filled_cross": Counter(),
        "unfilled": Counter(),
    }
    for e in entries:
        crossfill(e, vygus_index, stats)

    print(f"Writing: {DST}")
    with open(DST, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")

    print("\n=== Cross-fill report ===")
    src_names = {"0": "Lexicon", "1": "Dickson", "2": "Vygus", "4": "Faulkner"}

    def fmt(counter):
        items = sorted(counter.items(), key=lambda kv: kv[0] or "")
        return ", ".join(f"{src_names.get(k, k)}={v:,}" for k, v in items) or "(none)"

    total_within = sum(stats["filled_within"].values())
    total_cross = sum(stats["filled_cross"].values())
    total_unfilled = sum(stats["unfilled"].values())
    print(f"Filled from sibling Vygus translation : {total_within:,}")
    print(f"   by recipient source: {fmt(stats['filled_within'])}")
    print(f"Filled from cross-entry Vygus lookup  : {total_cross:,}")
    print(f"   by recipient source: {fmt(stats['filled_cross'])}")
    print(f"Still null after cross-fill           : {total_unfilled:,}")
    print(f"   by source: {fmt(stats['unfilled'])}")


if __name__ == "__main__":
    main()
