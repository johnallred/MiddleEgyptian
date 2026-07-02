# Playtest Report — Hieroglyph Quest

**Configuration**: 3 players, agents = ['balanced', 'balanced', 'balanced'], 300 games simulated.

## Balance score: **99.5/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **117 turns**
- Average final score: 4.8
- Logograms played per game (avg): 1.21
- Steals per game (avg): 2.46
- End reasons:
  - victory: 300 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 32.7% |
| seat_1 | 34.0% |
| seat_2 | 33.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 33.3% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `hAw` | 41 |
| `qmA` | 37 |
| `biA` | 37 |
| `tn` | 37 |
| `wHAt` | 36 |
| `diwt` | 36 |
| `twA` | 35 |
| `hAi` | 35 |
| `bAq` | 35 |
| `pr` | 34 |
| `im` | 34 |
| `iAs` | 33 |
| `dm` | 33 |
| `Ais` | 33 |
| `rwi` | 32 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `im` | 21 |
| `Hw` | 20 |
| `Ais` | 19 |
| `tn` | 19 |
| `iAs` | 17 |
| `wHAt` | 17 |
| `gAw` | 16 |
| `pr` | 16 |
| `hAi` | 16 |
| `biA` | 16 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|
| `Ais` | 10 | 40.0% |
| `hAw` | 15 | 33.3% |
| `inr` | 13 | 30.8% |
| `biA` | 13 | 30.8% |
| `mAT` | 10 | 30.0% |
| `dm` | 10 | 30.0% |
| `mn` | 10 | 30.0% |
| `inq` | 10 | 30.0% |
| `qAb` | 11 | 27.3% |
| `Hsb` | 11 | 27.3% |

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|
| `Hsb` | 11 | 27.3% |
| `bAq` | 11 | 27.3% |
| `Hryt` | 16 | 25.0% |
| `ink` | 10 | 20.0% |
| `Ad` | 10 | 20.0% |
| `rpw` | 11 | 18.2% |
| `iAs` | 13 | 15.4% |
| `dSrw` | 15 | 13.3% |
| `wnwt` | 11 | 9.1% |
| `irr` | 13 | 7.7% |

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- **Logograms are very common in play.** They may be too easy to acquire; consider reducing their count or making them harder to draw.
