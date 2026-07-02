# Optional Advanced Rules — Materials & Scoring Impact (v8.11)

Two of the four printed optional rules were unplayable for lack of
components (the same class of gap as the old trading-card shield):
the **determinative bonus** required a side deck that didn't exist and
per-word determinative listings that no card carried, and **honorific
transposition** required knowing which words contain divine/royal
elements with nothing marking them.

## Materials now generated (all 14 decks)

- **Determinative side pool:** 24 unique determinative cards per deck
  (top classifiers by usage among that deck's words; the 8 most-used
  get 2 copies, 32 total). Core deck top classifiers: D54 (walking
  legs / motion), Aa2, A2 (man with hand to mouth / speech, eating),
  A1 (seated man), A24, G37, N33, Z9.
- **Word card annotations:** `appropriate_determinatives` (up to 3,
  restricted to classifiers actually in the side pool so cards never
  reference something unclaimable). Coverage: 103-138 of 165 word
  cards per deck (core: 130).
- **Honorific markers:** `honorific_transposition: true` on word cards
  containing a divine/royal sign (R8, N5/N6, G7, C-category deities,
  A40-46, M23, L2, S1-7 crowns) in a playable spelling, and
  `honorific: true` on the matching sign cards. Core deck: 15
  honorific words; Gods & Temples: 41 (as it should be).
- **Per-word reference files** (`words/*.json`) now carry the full
  `determinatives` list derived from raw dictionary writings.

## Scoring impact (balanced mirror, 300 games/cell, seed 1000)

| Variant | Players | Median turns | Bonus pts/game | First-scorer wins |
|---|---:|---:|---:|---:|
| baseline | 2 / 3 / 4 | 146 / 117 / 112 | 0 | 50 / 40 / 34% |
| determinative bonus | 2 / 3 / 4 | 102 / 78 / 72 | 4.3-5.0 | 56 / 42 / 42% |
| honorific bonus | 2 / 3 / 4 | 136 / 108 / 104 | 0.9-1.2 | 51 / 42 / 33% |
| both | 2 / 3 / 4 | 98 / 72 / 68 | 4.8-5.6 | 57 / 45 / 40% |
| det bonus, targets +2 | 2 / 3 / 4 | 128 / 105 / 104 | — | 52 / 47 / 37% |
| both, targets +2 | 2 / 3 / 4 | 122 / 96 / 96 | — | 52 / 49 / 40% |

## Rulings adopted into rules.md

1. **Determinative bonus mechanics made concrete:** the side pool is
   laid out face-up at setup; completing a word whose card lists an
   appropriate determinative lets you claim ONE matching card for +1;
   supply-limited (claimed copies are gone until next game).
2. **Play to targets of 10 / 9 / 8** when using the determinative
   bonus (with or without honorific). Uncompensated, the rule cuts
   game length ~30-36% and worsens comeback health; +2 targets restore
   both to near baseline.
3. **Honorific bonus needs no target adjustment** (~1 point/game,
   negligible pacing effect).

Engine levers: `GameConfig.determinative_bonus`,
`GameConfig.honorific_bonus` (both default off — these are optional
rules), det pool via `load_determinative_supply()`; the sim models
players who always claim the bonus (upper bound).

## Incidental bug fixed during this work

`write_word_files` collision handling relied on `path.exists()`, which
breaks on case-insensitive filesystems (macOS): transliterations
differing only by case (`in` vs `iN` — different phonemes) silently
overwrote each other, losing 23 word files per build. Collision
tracking is now casefolded and filesystem-independent; the words/ tree
is cleared before regeneration (the old behavior also created 9,466
suffixed duplicates on any rerun into a non-empty tree). 9,466 records
now produce exactly 9,466 files.
