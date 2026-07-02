# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['random', 'random'], 300 games simulated.

## Balance score: **69.7/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **252 turns**
- Average final score: 6.6
- Logograms played per game (avg): 0.72
- Steals per game (avg): 0.35
- End reasons:
  - victory: 300 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 49.7% |
| seat_1 | 50.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 34 |
| `Hryt` | 32 |
| `hAi` | 31 |
| `wHAt` | 29 |
| `im` | 29 |
| `ink` | 28 |
| `iAs` | 28 |
| `dSrw` | 28 |
| `hnn` | 28 |
| `inr` | 28 |
| `inq` | 27 |
| `wnwt` | 27 |
| `qmA` | 27 |
| `Ahw` | 27 |
| `aq` | 27 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `pr` | 6 |
| `Stw` | 5 |
| `Hn` | 5 |
| `bnt` | 5 |
| `Xaq` | 4 |
| `im` | 4 |
| `aq` | 4 |
| `qrsw` | 4 |
| `wHAt` | 4 |
| `mn` | 4 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `iAs` | 12 | 66.7% |
| `dSrw` | 12 | 58.3% |
| `inr` | 11 | 54.5% |
| `hAw` | 10 | 50.0% |
| `Hryt` | 11 | 27.3% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `iAs` | 12 | 66.7% |
| `dSrw` | 12 | 58.3% |
| `inr` | 11 | 54.5% |
| `hAw` | 10 | 50.0% |
| `Hryt` | 11 | 27.3% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- Game looks reasonably balanced. Continue playtesting with human players to validate.
