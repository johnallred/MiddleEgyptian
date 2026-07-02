# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['greedy', 'greedy'], 300 games simulated.

## Balance score: **68.5/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **248 turns**
- Average final score: 8.1
- Logograms played per game (avg): 0.31
- Steals per game (avg): 0.62
- End reasons:
  - victory: 296 (98.7%)
  - turn_limit: 4 (1.3%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 48.7% |
| seat_1 | 51.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| greedy | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `snSmSm` | 10 |
| `STyt` | 10 |
| `sHDn` | 10 |
| `DArw` | 10 |
| `btk` | 10 |
| `pnayt` | 10 |
| `sip` | 10 |
| `irt` | 10 |
| `ngw` | 9 |
| `sDfAy` | 9 |
| `aDAw` | 9 |
| `nht` | 9 |
| `mwnf` | 9 |
| `iknw` | 9 |
| `sTs` | 8 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `A` | 6 |
| `aq` | 6 |
| `dm` | 5 |
| `wi` | 5 |
| `t` | 5 |
| `irt` | 5 |
| `spdt` | 4 |
| `aHaw` | 4 |
| `is` | 4 |
| `Hsb` | 4 |

## Best opening word cards

Word cards that, when drawn at game start, correlate with winning.

| Opening word | Games | Win rate |
|---|---:|---:|

## Worst opening word cards

Word cards that consistently give their drawer a poor game.

| Opening word | Games | Win rate |
|---|---:|---:|

## Broken openers (opening hand signatures)

Specific opening hands that win disproportionately often.
Each is reproducible: run the same seed with the same config to replay.

| Opening sign codes (first 7) | Games | Win rate |
|---|---:|---:|

## Recommendations

- Game looks reasonably balanced. Continue playtesting with human players to validate.
