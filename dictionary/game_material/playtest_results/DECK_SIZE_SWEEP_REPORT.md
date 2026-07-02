# Deck-Size Sweep Report

Each cell = 50 games with `balanced` agent. Seed 1000. Target 10 points, max 800 turns.

## Balance score (0-100, higher is better)

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 67.8 | 62.5 | 59.2 |
| 175 | 67.9 | 68.3 | 63.6 |
| 200 | 64.0 | 66.1 | 60.8 |
| 225 | 63.6 | 63.1 | 65.8 |
| 250 | 62.4 | 61.5 | 64.6 |
| 275 | 64.6 | 54.1 | 58.6 |
| 300 | 57.4 | 66.1 | 57.8 |

## Victory rate %

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 98% | 100% | 96% |
| 175 | 96% | 98% | 100% |
| 200 | 96% | 96% | 96% |
| 225 | 100% | 100% | 94% |
| 250 | 96% | 100% | 98% |
| 275 | 98% | 88% | 86% |
| 300 | 90% | 96% | 94% |

## Median game length (turns)

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 192 | 208 | 354 |
| 175 | 178 | 223 | 311 |
| 200 | 181 | 258 | 326 |
| 225 | 215 | 260 | 321 |
| 250 | 185 | 272 | 334 |
| 275 | 214 | 297 | 428 |
| 300 | 223 | 323 | 348 |

## Steals per game

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 0.84 | 2.02 | 3.02 |
| 175 | 0.86 | 1.60 | 2.52 |
| 200 | 0.62 | 1.88 | 2.74 |
| 225 | 1.06 | 1.92 | 2.46 |
| 250 | 0.78 | 1.60 | 2.68 |
| 275 | 0.54 | 1.48 | 2.36 |
| 300 | 0.56 | 1.60 | 2.40 |

## Logograms played per game

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 0.54 | 0.84 | 1.32 |
| 175 | 0.54 | 0.80 | 1.10 |
| 200 | 0.46 | 0.70 | 0.96 |
| 225 | 0.60 | 0.82 | 0.96 |
| 250 | 0.54 | 0.70 | 0.80 |
| 275 | 0.26 | 0.36 | 0.60 |
| 300 | 0.24 | 0.42 | 0.76 |

## Dead-card rate (% of deck never completed)

| Deck size | 2p | 3p | 4p |
|---:|---:|---:|---:|
| 150 | 20% | 11% | 7% |
| 175 | 23% | 18% | 12% |
| 200 | 32% | 20% | 16% |
| 225 | 28% | 21% | 17% |
| 250 | 35% | 26% | 21% |
| 275 | 38% | 30% | 25% |
| 300 | 46% | 34% | 28% |

## Recommendations

- **Best average balance score**: deck size **175** (66.6)
- **Highest average victory rate**: deck size **150** (98%)
- **Lowest dead-card rate**: deck size **150** (12%)

### Averages by deck size

| Deck size | Avg balance | Avg victory % | Avg dead-card % |
|---:|---:|---:|---:|
| 150 | 63.2 | 98% | 12% |
| 175 | 66.6 | 98% | 18% |
| 200 | 63.6 | 96% | 23% |
| 225 | 64.2 | 98% | 22% |
| 250 | 62.8 | 98% | 27% |
| 275 | 59.1 | 91% | 31% |
| 300 | 60.4 | 93% | 36% |

Smaller decks have fewer dead cards (each card sees the table more often) but offer less replay variety. Larger decks have more variety but more of the cards never get completed in any given game.
