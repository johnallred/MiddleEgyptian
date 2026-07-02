# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 500 games simulated.

## Balance score: **49.8/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **1000 turns**
- Average final score: 9.0
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.01
- End reasons:
  - turn_limit: 320 (64.0%)
  - victory: 180 (36.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 48.8% |
| seat_1 | 51.2% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `sHwy` | 18 |
| `sTy` | 17 |
| `qni` | 16 |
| `msdmt` | 16 |
| `gwAt` | 16 |
| `pSn` | 15 |
| `tbn` | 15 |
| `sawA` | 15 |
| `HmAt` | 15 |
| `ispr` | 15 |
| `snf` | 15 |
| `Aryt` | 14 |
| `rkrk` | 14 |
| `wpwty` | 14 |
| `Sna` | 14 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `ngyt` | 2 |
| `Afry` | 1 |
| `ihhy` | 1 |
| `nfryt` | 1 |
| `itnw` | 1 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `HmAt` | 11 | 54.5% |
| `Aryt` | 11 | 45.5% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `HmAt` | 11 | 54.5% |
| `Aryt` | 11 | 45.5% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
