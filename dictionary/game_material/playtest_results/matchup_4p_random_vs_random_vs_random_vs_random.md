# Playtest Report — Hieroglyph Quest

**Configuration**: 4 players, agents = ['random', 'random', 'random', 'random'], 300 games simulated.

## Balance score: **68.7/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **200 turns**
- Average final score: 3.4
- Logograms played per game (avg): 1.09
- Steals per game (avg): 0.8
- End reasons:
  - victory: 300 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 25.3% |
| seat_1 | 23.3% |
| seat_2 | 26.3% |
| seat_3 | 25.0% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 25.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 45 |
| `hAi` | 41 |
| `inr` | 38 |
| `iAs` | 37 |
| `dm` | 36 |
| `biA` | 36 |
| `Xsy` | 36 |
| `aq` | 36 |
| `wHAt` | 35 |
| `ST` | 34 |
| `dSrw` | 34 |
| `wnwt` | 34 |
| `Ais` | 34 |
| `twA` | 34 |
| `sTy` | 34 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `mn` | 13 |
| `Hsb` | 11 |
| `pr` | 10 |
| `t` | 10 |
| `wr` | 9 |
| `wnwt` | 9 |
| `DbA` | 9 |
| `sSp` | 8 |
| `wHAt` | 8 |
| `Xkr` | 7 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `mn` | 14 | 50.0% |
| `aq` | 14 | 42.9% |
| `sHDn` | 10 | 40.0% |
| `rwt` | 10 | 40.0% |
| `Ad` | 13 | 38.5% |
| `hAi` | 11 | 36.4% |
| `dm` | 14 | 35.7% |
| `im` | 14 | 35.7% |
| `wSm` | 12 | 33.3% |
| `wHAt` | 15 | 33.3% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `apr` | 10 | 10.0% |
| `nX` | 11 | 9.1% |
| `sTy` | 11 | 9.1% |
| `rwi` | 12 | 8.3% |
| `ink` | 13 | 7.7% |
| `dSrw` | 17 | 5.9% |
| `Hryt` | 18 | 0.0% |
| `twA` | 12 | 0.0% |
| `srf` | 11 | 0.0% |
| `nHH` | 11 | 0.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Logograms are very common in play.** They may be too easy to acquire; consider reducing their count or making them harder to draw.
