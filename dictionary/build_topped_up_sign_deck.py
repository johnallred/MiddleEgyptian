"""
Build a "topped-up" version of the shrunk unified sign deck so it can
support future expansions across (effectively) the entire family-safe
dictionary, not just the 8 current expansions.

Two adjustments are layered onto the shrunk 431-copy deck:

  1. ADD MISSING SIGNS. For every sign that is required by at least
     --min-blocking-threshold family-safe unused words AND is missing
     from the shrunk deck, add it. Signs that block ≥10 words get 2
     copies; others get 1 copy. Raising --min-blocking-threshold shrinks
     the resulting deck by dropping rare-blocking signs (signs that only
     block 1-2 niche words).

  2. TOP UP UNDER-SUPPLIED HIGH-DEMAND SIGNS. For any sign currently in
     the deck whose unused-pool demand suggests it's chronically short
     (specifically: present with < 4 copies AND used by >= 200 unused
     family-safe words), bump it to a minimum of 4 copies.

The result is saved to `proposed_base_sign_deck_topped_up.json` with a
comparison summary printed to stdout.

Threshold reference (run with --print-threshold-table to regenerate):
    threshold 1  → 530 copies, 100% family-safe coverage
    threshold 5  → 494 copies, 98.97% coverage
    threshold 10 → 479 copies, 97.79% coverage  ← v2 default
    threshold 15 → 453 copies, 95.94% coverage
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import build_expansion_deck as bed
import build_game_material as bgm
import playtest_simulator as ps

SHRUNK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck_shrunk.json"
TOPPED_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck_topped_up.json"
EXPANSIONS_DIR = ps.DICT_DIR / "game_material" / "expansions"

# Defaults (overridable via CLI)
DEFAULT_MIN_BLOCKING_THRESHOLD = 10  # only add signs that block ≥ this many unused family-safe words
ADD_EXTRA_COPY_IF_BLOCKS_AT_LEAST = 10
TOP_UP_TO_FOUR_THRESHOLD = 200   # >= 200 family-safe unused words using this sign
TOP_UP_MIN_COPIES = 4


def collect_used_translits() -> set[str]:
    used = set()
    for path in EXPANSIONS_DIR.glob("*.json"):
        deck = json.load(open(path))
        for c in deck["word_deck"]:
            used.add(c["transliteration"])
    return used


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--min-blocking-threshold", type=int,
                   default=DEFAULT_MIN_BLOCKING_THRESHOLD,
                   help="Only add missing signs that block at least this many "
                        "family-safe unused words. Higher = smaller deck, less "
                        "coverage. Default 10 (yields ~480 copies).")
    args = p.parse_args()
    threshold = args.min_blocking_threshold
    print(f"Min-blocking threshold: {threshold} "
          f"(only add signs that unblock ≥{threshold} family-safe unused words)\n")

    print("Loading dictionary, signs, and the shrunk unified deck...")
    phonetic_signs, logograms, determinatives = bgm.load_sign_data()
    det_set = set(determinatives.keys()) | {bgm.norm_sign(k) for k in determinatives}
    phonetic_set = set(phonetic_signs.keys())
    with open(bgm.ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    word_index = bgm.build_word_index(entries, phonetic_set, det_set)

    shrunk = json.load(open(SHRUNK_PATH))
    supply = {c["sign_code"]: c["copies"] for c in shrunk["sign_deck"]}
    print(f"  shrunk deck: {len(supply)} codes, {sum(supply.values())} copies")

    used_words = collect_used_translits()

    # Compute family-safe unused word pool and its sign demand
    family_unused = {}
    for translit, info in word_index.items():
        if translit in used_words:
            continue
        if not info["spellings"]:
            continue
        if not bgm.is_family_safe(translit, info.get("english_glosses", []),
                                   info["spellings"]):
            continue
        family_unused[translit] = info
    print(f"  family-safe unused words: {len(family_unused):,}")

    # Sign demand across that pool. Each word uses the family-safe spelling
    # the build script would actually pick (first spelling that doesn't use
    # any FAMILY_BLOCKED_SIGNS); if no such spelling exists the word is
    # effectively excluded from family decks regardless of demand.
    sign_uses_total = Counter()
    sign_words_using = defaultdict(int)
    sign_words_blocked = defaultdict(int)
    skipped_no_family_spelling = 0
    for translit, info in family_unused.items():
        family_spellings = [sp for sp in info["spellings"]
                            if not any(s in bgm.FAMILY_BLOCKED_SIGNS for s in sp)]
        if not family_spellings:
            skipped_no_family_spelling += 1
            continue
        sp = family_spellings[0]
        seen_this_word = set()
        for s in sp:
            sign_uses_total[s] += 1
            if s not in seen_this_word:
                sign_words_using[s] += 1
                if s not in supply:
                    sign_words_blocked[s] += 1
                seen_this_word.add(s)
    print(f"  ({skipped_no_family_spelling} words had no family-safe spelling — excluded)")

    # ----- ADJUSTMENT 1: ADD MISSING SIGNS -----
    new_supply = dict(supply)
    missing_signs = [s for s in sign_words_blocked if s not in supply]
    added = []
    skipped_rare = 0
    for sign in missing_signs:
        blocks = sign_words_blocked[sign]
        if blocks < threshold:
            skipped_rare += 1
            continue
        copies = 2 if blocks >= ADD_EXTRA_COPY_IF_BLOCKS_AT_LEAST else 1
        new_supply[sign] = copies
        added.append((sign, copies, blocks))

    # ----- ADJUSTMENT 2: TOP UP UNDER-SUPPLIED HIGH-DEMAND SIGNS -----
    topped_up = []
    for sign, copies in list(new_supply.items()):
        if sign in missing_signs:
            continue   # just added
        n_words = sign_words_using.get(sign, 0)
        if copies < TOP_UP_MIN_COPIES and n_words >= TOP_UP_TO_FOUR_THRESHOLD:
            topped_up.append((sign, copies, TOP_UP_MIN_COPIES, n_words))
            new_supply[sign] = TOP_UP_MIN_COPIES

    print(f"\nADJUSTMENT 1: added {len(added)} missing signs "
          f"({sum(c for _, c, _ in added)} new card copies), "
          f"skipped {skipped_rare} rare-blocking signs (each blocking < {threshold} words)")
    if added:
        print(f"  Top 10 by words they unblock:")
        for sign, copies, blocks in sorted(added, key=lambda x: -x[2])[:10]:
            print(f"    {sign:<8} {copies} copies, unblocks {blocks} words")

    print(f"\nADJUSTMENT 2: topped up {len(topped_up)} under-supplied "
          f"high-demand signs to {TOP_UP_MIN_COPIES} copies")
    if topped_up:
        print(f"  All affected signs:")
        for sign, old, new, n_words in sorted(topped_up, key=lambda x: -x[3]):
            print(f"    {sign:<8} {old} → {new} copies ({n_words:,} unused words use it)")

    # Reconstruct sign card list (preserve metadata for known signs)
    by_code = {c["sign_code"]: c for c in shrunk["sign_deck"]}
    new_cards = []
    for code in sorted(new_supply.keys()):
        if code in by_code:
            card = dict(by_code[code])
            card["copies"] = new_supply[code]
        else:
            info = phonetic_signs.get(code, {})
            card = {
                "card_id": f"sign_{code}",
                "type": "phonetic",
                "phonetic_class": info.get("class", "uniliteral"),
                "sign_code": code,
                "mnemonic": info.get("mnemonic", ""),
                "description": info.get("description", ""),
                "copies": new_supply[code],
            }
        new_cards.append(card)

    total = sum(c["copies"] for c in new_cards)
    out = {
        "name": "Hieroglyph Quest: Proposed Base Sign Library (TOPPED UP)",
        "version": "1.0",
        "expansion_type": "base_sign_library_proposal_topped_up",
        "sign_deck": new_cards,
        "logogram_deck": [],
        "word_deck": [],
        "unique_sign_count": len(new_cards),
        "total_sign_copies": total,
        "shrinkage_strategy": "shrunk_then_topped_up_for_future_coverage",
        "build_notes": {
            "started_from": "proposed_base_sign_deck_shrunk.json (238 codes / 431 copies)",
            "missing_signs_added": len(added),
            "new_cards_for_missing": sum(c for _, c, _ in added),
            "under_supplied_signs_topped_up": len(topped_up),
            "top_up_threshold_words": TOP_UP_TO_FOUR_THRESHOLD,
            "top_up_min_copies": TOP_UP_MIN_COPIES,
        },
    }
    TOPPED_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2))

    # Verify: how many family-safe unused words are STILL blocked?
    still_blocked = 0
    for translit, info in family_unused.items():
        sp = info["spellings"][0]
        if any(s not in new_supply for s in sp):
            still_blocked += 1

    print(f"\n=== RESULTS ===")
    print(f"Shrunk deck:    {len(supply):>4} codes, {sum(supply.values()):>4} copies")
    print(f"Topped-up deck: {len(new_supply):>4} codes, {total:>4} copies "
          f"(+{len(new_supply)-len(supply)} codes, +{total - sum(supply.values())} copies)")
    print(f"Family-safe unused words now reachable: "
          f"{len(family_unused) - still_blocked:,} of {len(family_unused):,} "
          f"({(1 - still_blocked/len(family_unused))*100:.2f}%)")
    print(f"Still blocked (require a sign not in any reference data): {still_blocked}")
    print(f"\nWritten: {TOPPED_PATH}")


if __name__ == "__main__":
    main()
