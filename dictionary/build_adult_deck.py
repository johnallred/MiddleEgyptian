"""
Build the "Hieroglyph Quest: After Dark" expansion deck.

This deck contains the words that the family-mode filter excludes:
  - Words whose only spellings use the sexual-anatomy signs
    (D27/D27a, D52/D52a/D53/D53a, F45/F45a, F51).
  - Words whose English glosses contain explicit anatomical/sexual terms
    (phallus, penis, vulva, vagina, copulate, etc.).

The deck is intentionally smaller (≈ one print sheet of 55 cards) since the
total pool of mature-content words in the playable index is limited.
"""

import argparse
import json
from pathlib import Path

import build_game_material as bgm
import playtest_simulator as ps


OUT_PATH = bgm.OUT_DIR / "expansions" / "after_dark.json"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--deck-size", type=int, default=55,
                   help="Total mature word cards (default 55, one print sheet)")
    args = p.parse_args()

    print("Loading sign reference data...")
    phonetic_signs, logograms, determinatives = bgm.load_sign_data()
    det_set = set(determinatives.keys()) | {bgm.norm_sign(k) for k in determinatives}
    phonetic_set = set(phonetic_signs.keys())

    print("Loading Entries2.json ...")
    with open(bgm.ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    word_index = bgm.build_word_index(entries, phonetic_set, det_set)
    print(f"  {len(word_index):,} playable words")

    # Keep ONLY words that family mode would exclude.
    mature_index = {
        t: info for t, info in word_index.items()
        if not bgm.is_family_safe(t, info.get("english_glosses", []),
                                   info["spellings"])
    }
    print(f"  {len(mature_index):,} mature-content words available")

    # Build the deck using the mature-only index, with picks scaled small.
    # Use the same tier proportions as the family deck.
    picks = bgm.scaled_picks(args.deck_size)
    deck = bgm.build_deck(mature_index, phonetic_signs, logograms,
                           picks_per_tier_override=picks,
                           content_filter="mature")
    deck["name"] = "Hieroglyph Quest: After Dark — Adult Expansion"
    deck["version"] = "1.0"
    deck["content_filter"] = "mature"
    deck["target_deck_size"] = args.deck_size
    deck["warning"] = (
        "This expansion contains adult content (sexual anatomy hieroglyphs "
        "and explicit English glosses) drawn from Middle Egyptian dictionary "
        "sources. Intended for ages 18+. Not for sale alongside family decks."
    )

    OUT_PATH.write_text(json.dumps(deck, ensure_ascii=False, indent=2))
    print(f"\nWrote: {OUT_PATH}")
    print(f"  word cards : {len(deck['word_deck'])}")
    print(f"  logograms  : {len(deck['logogram_deck'])}")
    print(f"  sign cards : {sum(c['copies'] for c in deck['sign_deck'])} copies")
    print(f"  signs include the blocked set: "
          f"{sorted(set(c['sign_code'] for c in deck['sign_deck']) & bgm.FAMILY_BLOCKED_SIGNS)}")

    # Sample contents
    print("\nSample word cards:")
    for c in deck["word_deck"][:8]:
        print(f"  {c['transliteration']:14} {' '.join(c['valid_spellings'][0]):25} "
              f"→ {c['english_glosses'][:1]}")


if __name__ == "__main__":
    main()
