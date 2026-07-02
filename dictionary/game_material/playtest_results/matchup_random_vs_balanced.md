# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['random', 'balanced'], 300 games simulated.

## Balance score: **45.9/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **280 turns**
- Average final score: 7.2
- Logograms played per game (avg): 0.24
- Steals per game (avg): 0.4
- End reasons:
  - victory: 280 (93.3%)
  - turn_limit: 20 (6.7%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 22.3% |
| seat_1 | 77.7% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| random | 22.3% |
| balanced | 77.7% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `XsA` | 11 |
| `STyt` | 10 |
| `sHDn` | 10 |
| `snSmSm` | 9 |
| `srft` | 9 |
| `nbibi` | 9 |
| `inpw` | 9 |
| `wi` | 8 |
| `aDAw` | 8 |
| `nht` | 8 |
| `mwnf` | 8 |
| `sDty` | 8 |
| `innk` | 8 |
| `iSdd` | 8 |
| `rwi` | 8 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|
| `thm` | 4 |
| `kAp` | 4 |
| `DbA` | 4 |
| `Hnk` | 3 |
| `spdt` | 3 |
| `t` | 3 |
| `inpw` | 3 |
| `hAw` | 2 |
| `Hsb` | 2 |
| `bnw` | 2 |

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
