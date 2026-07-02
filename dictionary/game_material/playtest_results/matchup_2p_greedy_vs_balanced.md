# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['greedy', 'balanced'], 300 games simulated.

## Balance score: **98.9/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **142 turns**
- Average final score: 6.5
- Logograms played per game (avg): 1.05
- Steals per game (avg): 1.49
- End reasons:
  - victory: 300 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 51.3% |
| seat_1 | 48.7% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| greedy | 51.3% |
| balanced | 48.7% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 35 |
| `wHAt` | 34 |
| `Hryt` | 33 |
| `qmA` | 33 |
| `hAi` | 32 |
| `im` | 31 |
| `twA` | 31 |
| `biA` | 29 |
| `irr` | 28 |
| `wnwt` | 28 |
| `hnn` | 28 |
| `bAq` | 28 |
| `ST` | 27 |
| `Xsy` | 27 |
| `aq` | 27 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `hAw` | 13 |
| `im` | 13 |
| `qmA` | 12 |
| `tn` | 12 |
| `sTy` | 11 |
| `Hw` | 11 |
| `biA` | 11 |
| `hAi` | 11 |
| `mAT` | 10 |
| `bAq` | 10 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `hAw` | 10 | 70.0% |
| `Hryt` | 11 | 54.5% |
| `iAs` | 12 | 41.7% |
| `inr` | 11 | 27.3% |
| `dSrw` | 12 | 25.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `hAw` | 10 | 70.0% |
| `Hryt` | 11 | 54.5% |
| `iAs` | 12 | 41.7% |
| `inr` | 11 | 27.3% |
| `dSrw` | 12 | 25.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Logograms are very common in play.** They may be too easy to acquire; consider reducing their count or making them harder to draw.
