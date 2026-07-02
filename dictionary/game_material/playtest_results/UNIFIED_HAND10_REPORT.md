# Unified Signs + Starting Hand 10 — Re-Playtest Report

**Tested config:** unified sign deck (547 copies), `starting_hand=10`, `hand_limit=12`.

All cells: 50 games with `balanced` agent, seed 1000, target 10 points, max 800 turns.

**Hypothesis:** unified-sign deck (547 copies) dilutes each draw vs. per-theme decks (305–357 copies). Bumping starting hand from 8 → 10 gives each player two extra signs at game start, hopefully recovering the speed lost to centralization while keeping the 57% card-print savings.

## Game length (median turns) — three-way comparison

| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 | Δ vs per-theme h=8 |
|---|---:|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 287 | 437 | 432 | -6 | +144 |
| Hieroglyph Quest: Body & Healing | 244 | 395 | 437 | +41 | +193 |
| Hieroglyph Quest: Core Set: Daily Life | 238 | 439 | 450 | +11 | +212 |
| Hieroglyph Quest: Gods & Temples | 254 | 428 | 445 | +16 | +191 |
| Hieroglyph Quest: Kings & Court | 266 | 413 | 425 | +12 | +159 |
| Hieroglyph Quest: Pantheon Expanded | 276 | 435 | 420 | -15 | +144 |
| Hieroglyph Quest: The Land of Egypt | 274 | 451 | 384 | -67 | +110 |
| Hieroglyph Quest: Wild Egypt | 240 | 408 | 386 | -22 | +146 |

## Balance score — three-way comparison

| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 | Δ vs per-theme h=8 |
|---|---:|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 63.3 | 58.6 | 60.7 | +2.1 | -2.6 |
| Hieroglyph Quest: Body & Healing | 65.3 | 63.0 | 61.4 | -1.6 | -3.9 |
| Hieroglyph Quest: Core Set: Daily Life | 62.9 | 62.1 | 59.8 | -2.3 | -3.1 |
| Hieroglyph Quest: Gods & Temples | 62.5 | 60.3 | 61.0 | +0.7 | -1.5 |
| Hieroglyph Quest: Kings & Court | 59.7 | 58.7 | 54.3 | -4.4 | -5.4 |
| Hieroglyph Quest: Pantheon Expanded | 62.9 | 63.0 | 62.0 | -1.0 | -0.9 |
| Hieroglyph Quest: The Land of Egypt | 65.2 | 59.4 | 62.2 | +2.7 | -3.0 |
| Hieroglyph Quest: Wild Egypt | 61.9 | 60.4 | 62.9 | +2.5 | +1.0 |

## Dead-card rate — three-way comparison

| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 14% | 14% | 16% | +1.8 pp |
| Hieroglyph Quest: Body & Healing | 13% | 14% | 14% | -0.6 pp |
| Hieroglyph Quest: Core Set: Daily Life | 15% | 16% | 16% | -0.6 pp |
| Hieroglyph Quest: Gods & Temples | 13% | 14% | 14% | +0.3 pp |
| Hieroglyph Quest: Kings & Court | 17% | 17% | 17% | -0.1 pp |
| Hieroglyph Quest: Pantheon Expanded | 14% | 15% | 17% | +1.8 pp |
| Hieroglyph Quest: The Land of Egypt | 15% | 15% | 16% | +0.8 pp |
| Hieroglyph Quest: Wild Egypt | 14% | 16% | 16% | +0.0 pp |

## Unified-signs + hand=10: results by player count

### Balance score

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 64.4 | 63.1 | 54.6 | 60.7 |
| Hieroglyph Quest: Body & Healing | 65.2 | 62.5 | 56.4 | 61.4 |
| Hieroglyph Quest: Core Set: Daily Life | 63.6 | 63.9 | 51.8 | 59.8 |
| Hieroglyph Quest: Gods & Temples | 64.0 | 62.9 | 56.2 | 61.0 |
| Hieroglyph Quest: Kings & Court | 55.4 | 53.3 | 54.2 | 54.3 |
| Hieroglyph Quest: Pantheon Expanded | 66.0 | 63.3 | 56.6 | 62.0 |
| Hieroglyph Quest: The Land of Egypt | 67.8 | 62.7 | 56.0 | 62.2 |
| Hieroglyph Quest: Wild Egypt | 67.8 | 60.3 | 60.6 | 62.9 |

### Median turns

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 309 | 476 | 510 | 432 |
| Hieroglyph Quest: Body & Healing | 283 | 418 | 609 | 437 |
| Hieroglyph Quest: Core Set: Daily Life | 329 | 456 | 565 | 450 |
| Hieroglyph Quest: Gods & Temples | 299 | 427 | 608 | 445 |
| Hieroglyph Quest: Kings & Court | 307 | 370 | 598 | 425 |
| Hieroglyph Quest: Pantheon Expanded | 303 | 399 | 558 | 420 |
| Hieroglyph Quest: The Land of Egypt | 289 | 367 | 497 | 384 |
| Hieroglyph Quest: Wild Egypt | 272 | 408 | 477 | 386 |

### Victory rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 92% | 86% | 78% | 85% |
| Hieroglyph Quest: Body & Healing | 100% | 98% | 76% | 91% |
| Hieroglyph Quest: Core Set: Daily Life | 100% | 94% | 66% | 87% |
| Hieroglyph Quest: Gods & Temples | 96% | 94% | 78% | 89% |
| Hieroglyph Quest: Kings & Court | 94% | 94% | 74% | 87% |
| Hieroglyph Quest: Pantheon Expanded | 92% | 92% | 82% | 89% |
| Hieroglyph Quest: The Land of Egypt | 98% | 90% | 88% | 92% |
| Hieroglyph Quest: Wild Egypt | 98% | 98% | 98% | 98% |

### Dead-card rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 21% | 14% | 13% | 16% |
| Hieroglyph Quest: Body & Healing | 20% | 12% | 9% | 14% |
| Hieroglyph Quest: Core Set: Daily Life | 20% | 13% | 14% | 16% |
| Hieroglyph Quest: Gods & Temples | 18% | 13% | 11% | 14% |
| Hieroglyph Quest: Kings & Court | 21% | 15% | 16% | 17% |
| Hieroglyph Quest: Pantheon Expanded | 23% | 16% | 11% | 17% |
| Hieroglyph Quest: The Land of Egypt | 21% | 16% | 10% | 16% |
| Hieroglyph Quest: Wild Egypt | 23% | 14% | 12% | 16% |

## Health flags

- **Hieroglyph Quest: Kings & Court**: balance 54 below 55
