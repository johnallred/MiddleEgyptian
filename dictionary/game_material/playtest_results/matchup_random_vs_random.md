# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['random', 'random'], 300 games simulated.

## Balance score: **67.2/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **458 turns**
- Average final score: 7.6
- Logograms played per game (avg): 0.26
- Steals per game (avg): 0.09
- End reasons:
  - victory: 272 (90.7%)
  - turn_limit: 28 (9.3%)

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
| random | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `snSmSm` | 11 |
| `STyt` | 11 |
| `pnayt` | 11 |
| `irt` | 11 |
| `XsA` | 10 |
| `nht` | 10 |
| `sHDn` | 9 |
| `mwnf` | 9 |
| `rwi` | 9 |
| `inpw` | 9 |
| `wi` | 8 |
| `inr` | 8 |
| `sDfAy` | 8 |
| `iSdd` | 8 |
| `aXmw` | 8 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `inpw` | 3 |
| `bnw` | 2 |
| `biA` | 2 |
| `Tsm` | 2 |
| `wHAt` | 2 |
| `pr` | 1 |
| `wnwt` | 1 |
| `qrsw` | 1 |
| `snf` | 1 |
| `wDa` | 1 |

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

- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
