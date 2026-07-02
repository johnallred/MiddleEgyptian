# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['greedy', 'balanced'], 300 games simulated.

## Balance score: **63.0/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **212 turns**
- Average final score: 8.1
- Logograms played per game (avg): 0.29
- Steals per game (avg): 0.58
- End reasons:
  - victory: 297 (99.0%)
  - turn_limit: 3 (1.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 41.7% |
| seat_1 | 58.3% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| greedy | 41.7% |
| balanced | 58.3% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `STyt` | 11 |
| `sHDn` | 11 |
| `irt` | 11 |
| `snSmSm` | 10 |
| `mwnf` | 10 |
| `sip` | 10 |
| `iSdd` | 10 |
| `nht` | 9 |
| `pnayt` | 9 |
| `aXmw` | 9 |
| `ngw` | 8 |
| `hAw` | 8 |
| `wi` | 8 |
| `XsA` | 8 |
| `wnwn` | 8 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `A` | 6 |
| `irt` | 6 |
| `aHaw` | 5 |
| `aq` | 5 |
| `spdt` | 4 |
| `wi` | 4 |
| `rHw` | 3 |
| `Hsb` | 3 |
| `t` | 3 |
| `Apd` | 3 |

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

- **Seat-0 advantage detected.** Consider letting later seats draw an extra opening card or sign card to compensate.
