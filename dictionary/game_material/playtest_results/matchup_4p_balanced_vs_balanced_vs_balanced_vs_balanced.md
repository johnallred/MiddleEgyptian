# Playtest Report — Hieroglyph Quest

**Configuration**: 4 players, agents = ['balanced', 'balanced', 'balanced', 'balanced'], 300 games simulated.

## Balance score: **95.7/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **112 turns**
- Average final score: 3.6
- Logograms played per game (avg): 1.51
- Steals per game (avg): 3.8
- End reasons:
  - victory: 300 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 24.3% |
| seat_1 | 25.7% |
| seat_2 | 29.7% |
| seat_3 | 20.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 25.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 49 |
| `wHAt` | 47 |
| `iAs` | 44 |
| `biA` | 43 |
| `Xsy` | 43 |
| `tn` | 43 |
| `hAi` | 43 |
| `im` | 42 |
| `twA` | 42 |
| `sbA` | 41 |
| `Hw` | 41 |
| `dm` | 41 |
| `qmA` | 41 |
| `inr` | 40 |
| `Ais` | 39 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `wHAt` | 35 |
| `im` | 31 |
| `hAw` | 30 |
| `Hw` | 27 |
| `tn` | 27 |
| `Ahw` | 26 |
| `iAs` | 24 |
| `biA` | 24 |
| `sTy` | 24 |
| `sbA` | 24 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `dm` | 14 | 50.0% |
| `aHaw` | 11 | 45.5% |
| `Ahw` | 10 | 40.0% |
| `Hsb` | 13 | 38.5% |
| `nX` | 11 | 36.4% |
| `sTy` | 11 | 36.4% |
| `wSm` | 12 | 33.3% |
| `wnwt` | 16 | 31.2% |
| `mAT` | 13 | 30.8% |
| `sHDn` | 10 | 30.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `im` | 14 | 14.3% |
| `iAs` | 16 | 12.5% |
| `mtwt` | 10 | 10.0% |
| `rwt` | 10 | 10.0% |
| `nHH` | 11 | 9.1% |
| `gAw` | 12 | 8.3% |
| `DbA` | 13 | 7.7% |
| `ST` | 16 | 6.2% |
| `dwAyt` | 10 | 0.0% |
| `hAi` | 11 | 0.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Logograms are very common in play.** They may be too easy to acquire; consider reducing their count or making them harder to draw.
