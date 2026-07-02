# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 1,000 games simulated.

## Balance score: **39.2/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **200 turns**
- Average final score: 0.0
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.0
- End reasons:
  - turn_limit: 1000 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 51.0% |
| seat_1 | 49.0% |

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
| `nDt` | 13 | 84.6% |
| `pAqyt` | 11 | 81.8% |
| `HwAAt` | 10 | 80.0% |
| `XsA` | 11 | 72.7% |
| `rmT` | 11 | 72.7% |
| `sfnA` | 10 | 70.0% |
| `pnayt` | 10 | 70.0% |
| `nDyt` | 10 | 70.0% |
| `dfdf` | 10 | 70.0% |
| `pHty` | 10 | 70.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `rSwt` | 11 | 36.4% |
| `dni` | 12 | 33.3% |
| `dnyt` | 13 | 30.8% |
| `TAbt` | 10 | 30.0% |
| `Hpt` | 11 | 27.3% |
| `mxAt` | 11 | 27.3% |
| `dmDyt` | 10 | 20.0% |
| `wrS` | 10 | 20.0% |
| `wgyt` | 12 | 16.7% |
| `sTs` | 12 | 16.7% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
