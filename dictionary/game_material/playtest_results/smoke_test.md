# Playtest Report — Hieroglyph Quest

**Configuration**: 2 players, agents = ['balanced', 'balanced'], 100 games simulated.

## Balance score: **4.8/100**

Higher = more balanced. Composed of seat-fairness (40%), game-length sanity (30%), and stalemate avoidance (30%).

## Game-flow summary

- Median game length : **200 turns**
- Average final score: 0.1
- Logograms played per game (avg): 0.0
- Steals per game (avg): 0.0
- End reasons:
  - turn_limit: 100 (100.0%)

## Seat (first-player) advantage

Win rate by seat order. Ideal: each seat ~= 1/N.

| Seat | Win rate |
|---|---:|
| seat_0 | 94.0% |
| seat_1 | 6.0% |

## Agent matchup

Win rate by AI agent strategy.

| Agent | Win rate |
|---|---:|
| balanced | 50.0% |

## Most-completed word cards (top 15)

Words that appear in lots of completed-card piles — frequent + valuable.

| Word | Times completed |
|---|---:|
| `TAbt` | 1 |
| `Xsy` | 1 |
| `rwty` | 1 |
| `wsT` | 1 |
| `qni` | 1 |
| `mtn` | 1 |
| `sTy` | 1 |
| `Tst` | 1 |
| `hA` | 1 |
| `rDw` | 1 |
| `ink` | 1 |
| `ngw` | 1 |
| `snwt` | 1 |
| `Hnkyt` | 1 |

## Most-stolen word cards (top 10)

Words that opponents steal often — these may be too valuable or too easy.

| Word | Times stolen |
|---|---:|

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
- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.
- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.
