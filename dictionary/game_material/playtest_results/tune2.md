# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 1,000 games simulated.

## Balance score: **39.9/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **1000 turns**
- Average final score: 0.0
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.0
- End reasons:
  - turn_limit: 1000 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 49.9% |
| seat_1 | 50.1% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `smn` | 1 |
| `nHH` | 1 |
| `Hpt` | 1 |
| `saH` | 1 |
| `ink` | 1 |
| `rmT` | 1 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `pnayt` | 10 | 80.0% |
| `sSm` | 10 | 80.0% |
| `HwAAt` | 10 | 80.0% |
| `HAyw` | 10 | 80.0% |
| `nSp` | 12 | 75.0% |
| `tn` | 10 | 70.0% |
| `dmDyt` | 10 | 70.0% |
| `Drit` | 10 | 70.0% |
| `hmhmt` | 10 | 70.0% |
| `dAwt` | 10 | 70.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `DArw` | 13 | 38.5% |
| `pnq` | 11 | 36.4% |
| `wgyt` | 12 | 33.3% |
| `TAbt` | 10 | 30.0% |
| `sTy` | 10 | 30.0% |
| `wrS` | 10 | 30.0% |
| `ntTn` | 10 | 30.0% |
| `snwt` | 14 | 21.4% |
| `ndbwt` | 10 | 20.0% |
| `srft` | 12 | 8.3% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
