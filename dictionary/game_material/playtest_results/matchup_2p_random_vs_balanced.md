# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['random', 'balanced'], 300 games simulated.

## Balance score: **47.9/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **178 turns**
- Average final score: 6.3
- Logograms played per game (avg): 0.8
- Steals per game (avg): 0.95
- End reasons:
  - victory: 299 (99.7%)
  - turn_limit: 1 (0.3%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 21.7% |
| seat_1 | 78.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 21.7% |
| balanced | 78.3% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 32 |
| `qmA` | 31 |
| `Hryt` | 30 |
| `hnn` | 30 |
| `twA` | 30 |
| `biA` | 30 |
| `bAq` | 30 |
| `wHAt` | 29 |
| `inr` | 29 |
| `Ad` | 29 |
| `hAi` | 29 |
| `ST` | 27 |
| `im` | 27 |
| `Hw` | 26 |
| `dm` | 26 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `mn` | 10 |
| `pr` | 10 |
| `Stw` | 9 |
| `hAw` | 8 |
| `qmA` | 8 |
| `biA` | 8 |
| `wr` | 7 |
| `DbA` | 7 |
| `im` | 7 |
| `HDD` | 7 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `Hryt` | 11 | 72.7% |
| `inr` | 11 | 54.5% |
| `dSrw` | 12 | 50.0% |
| `iAs` | 12 | 50.0% |
| `hAw` | 10 | 40.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `Hryt` | 11 | 72.7% |
| `inr` | 11 | 54.5% |
| `dSrw` | 12 | 50.0% |
| `iAs` | 12 | 50.0% |
| `hAw` | 10 | 40.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Seat-0 advantage detected.** Consider letting later seats draw an extra opening card or sign card to compensate.
