# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 300 games simulated.

## Balance score: **68.7/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **199 turns**
- Average final score: 7.8
- Logograms played per game (avg): 0.25
- Steals per game (avg): 0.6
- End reasons:
  - victory: 287 (95.7%)
  - turn_limit: 13 (4.3%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 50.0% |
| seat_1 | 50.0% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `STyt` | 11 |
| `irt` | 10 |
| `srf` | 9 |
| `sip` | 9 |
| `rwi` | 9 |
| `aXmw` | 9 |
| `dwAyt` | 9 |
| `mwnf` | 9 |
| `ngw` | 8 |
| `sbnw` | 8 |
| `snSmSm` | 8 |
| `fttw` | 8 |
| `wi` | 8 |
| `aDAw` | 8 |
| `sHDn` | 8 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `A` | 7 |
| `aq` | 5 |
| `biA` | 5 |
| `wi` | 5 |
| `DAi` | 4 |
| `rmi` | 4 |
| `iAs` | 4 |
| `kAp` | 4 |
| `DbA` | 4 |
| `thm` | 4 |

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
