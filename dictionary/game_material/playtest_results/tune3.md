# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 1,000 games simulated.

## Balance score: **48.9/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **1000 turns**
- Average final score: 8.7
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.01
- End reasons:
  - turn_limit: 676 (67.6%)
  - victory: 324 (32.4%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 49.0% |
| seat_1 | 51.0% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `sHD` | 32 |
| `sip` | 30 |
| `mnH` | 30 |
| `snwt` | 29 |
| `snHA` | 28 |
| `sTy` | 28 |
| `rwi` | 28 |
| `sDfAy` | 28 |
| `rmT` | 28 |
| `tn` | 27 |
| `ispr` | 26 |
| `Hw` | 26 |
| `HArw` | 26 |
| `DArw` | 26 |
| `Tst` | 25 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `dnit` | 1 |
| `xtxt` | 1 |
| `sTs` | 1 |
| `xAstyw` | 1 |
| `iAAyt` | 1 |
| `sDfAy` | 1 |
| `ntsn` | 1 |
| `amat` | 1 |
| `nsyw` | 1 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `sfnA` | 10 | 90.0% |
| `nDyt` | 10 | 90.0% |
| `sTy` | 10 | 80.0% |
| `Xnwtyw` | 10 | 80.0% |
| `nDmmyt` | 10 | 80.0% |
| `dnyt` | 13 | 76.9% |
| `msADt` | 17 | 76.5% |
| `pr dwAt` | 12 | 75.0% |
| `rSwt` | 11 | 72.7% |
| `pnayt` | 10 | 70.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `rmT` | 11 | 27.3% |
| `pnq` | 11 | 27.3% |
| `sip` | 12 | 25.0% |
| `sTs` | 12 | 25.0% |
| `DArw` | 13 | 23.1% |
| `pHty` | 10 | 20.0% |
| `Tst` | 11 | 18.2% |
| `smAyt` | 12 | 16.7% |
| `snwt` | 14 | 14.3% |
| `dfdf` | 10 | 10.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
