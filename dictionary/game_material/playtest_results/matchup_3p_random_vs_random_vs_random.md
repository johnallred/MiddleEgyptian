# Playtest Report — Hieroglyph Quest

**Configuration**: 3 players, agents = ['random', 'random', 'random'], 300 games simulated.

## Balance score: **64.0/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **201 turns**
- Average final score: 4.6
- Logograms played per game (avg): 0.84
- Steals per game (avg): 0.53
- End reasons:
  - victory: 299 (99.7%)
  - turn_limit: 1 (0.3%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 40.7% |
| seat_1 | 28.3% |
| seat_2 | 31.0% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 33.3% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 41 |
| `biA` | 37 |
| `Xsy` | 37 |
| `im` | 36 |
| `wHAt` | 36 |
| `qmA` | 34 |
| `hAi` | 34 |
| `wnwt` | 33 |
| `tn` | 32 |
| `inr` | 32 |
| `ink` | 31 |
| `Hryt` | 31 |
| `hnn` | 31 |
| `Hw` | 30 |
| `Ais` | 30 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `wnwt` | 8 |
| `pr` | 7 |
| `Hsb` | 7 |
| `wHAt` | 7 |
| `rHw` | 6 |
| `Hn` | 6 |
| `mhr` | 6 |
| `t` | 6 |
| `sSp` | 5 |
| `aq` | 5 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `qAb` | 11 | 54.5% |
| `dm` | 10 | 50.0% |
| `mAT` | 10 | 40.0% |
| `Ad` | 10 | 40.0% |
| `inr` | 13 | 38.5% |
| `iAs` | 13 | 38.5% |
| `Hryt` | 16 | 31.2% |
| `ink` | 10 | 30.0% |
| `Ais` | 10 | 30.0% |
| `inq` | 10 | 30.0% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `inq` | 10 | 30.0% |
| `rpw` | 11 | 27.3% |
| `wnwt` | 11 | 27.3% |
| `bAq` | 11 | 27.3% |
| `irr` | 13 | 23.1% |
| `hAw` | 15 | 20.0% |
| `dSrw` | 15 | 20.0% |
| `biA` | 13 | 15.4% |
| `Hsb` | 11 | 0.0% |
| `mn` | 10 | 0.0% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Seat-0 advantage detected.** Consider letting later seats draw an extra opening card or sign card to compensate.
