# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['random', 'random'], 2,000 games simulated.

## Balance score: **48.7/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **1000 turns**
- Average final score: 8.8
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.0
- End reasons:
  - turn_limit: 1362 (68.1%)
  - victory: 638 (31.9%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 48.9% |
| seat_1 | 51.1% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `sHwy` | 55 |
| `Sna` | 51 |
| `nX` | 51 |
| `inbA` | 50 |
| `saHa` | 49 |
| `Xsy` | 49 |
| `sTs` | 48 |
| `anDw` | 48 |
| `rpyt` | 48 |
| `msdmt` | 47 |
| `sTy` | 46 |
| `iyt` | 46 |
| `HmAt` | 46 |
| `ink` | 45 |
| `rmT` | 45 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `nsywt` | 13 | 92.3% |
| `nhnhA` | 19 | 89.5% |
| `nmHyt` | 17 | 88.2% |
| `sfnA` | 21 | 85.7% |
| `hrwyt` | 13 | 84.6% |
| `Snyt` | 13 | 84.6% |
| `nDmmyt` | 13 | 84.6% |
| `dgAyt` | 17 | 82.4% |
| `snSmSm` | 11 | 81.8% |
| `xAxA` | 11 | 81.8% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `imy r ab wHmt Swt nSmt` | 21 | 23.8% |
| `nht` | 13 | 23.1% |
| `rwty` | 13 | 23.1% |
| `Htmt` | 13 | 23.1% |
| `inr` | 14 | 21.4% |
| `Ahw` | 15 | 20.0% |
| `tpiw` | 10 | 20.0% |
| `qsnt` | 16 | 18.8% |
| `xAstyw` | 12 | 16.7% |
| `Hawt` | 13 | 7.7% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
