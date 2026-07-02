# Shrunk Unified Sign Deck — Re-Playtest Report

**Tested config:** shrunk unified sign deck (238 codes, 431 copies, target 400), `starting_hand=8`, `hand_limit=12`.

All cells: 50 games with `balanced` agent, seed 1000, target 10 points, max 800 turns.

**Shrinkage strategy:** for each sign code, set copies = mean across themes that contain it (rounded, min 1), then if total exceeds target (400), scale all sign counts down uniformly.

Compared to: per-theme baseline (305–357 copies, per-theme tuned) and original unified (547 copies, union-of-max).

## Game length (median turns) — four-way comparison

| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 | Δ vs Per-theme |
|---|---:|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 287 | 437 | 345 | -93 | +57 |
| Hieroglyph Quest: Body & Healing | 244 | 395 | 301 | -94 | +58 |
| Hieroglyph Quest: Core Set: Daily Life | 238 | 439 | 334 | -105 | +96 |
| Hieroglyph Quest: Gods & Temples | 254 | 428 | 349 | -79 | +95 |
| Hieroglyph Quest: Kings & Court | 266 | 413 | 357 | -56 | +92 |
| Hieroglyph Quest: Pantheon Expanded | 276 | 435 | 396 | -39 | +120 |
| Hieroglyph Quest: The Land of Egypt | 274 | 451 | 368 | -83 | +94 |
| Hieroglyph Quest: Wild Egypt | 240 | 408 | 303 | -105 | +63 |

## Balance score — four-way comparison

| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 | Δ vs Per-theme |
|---|---:|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 63.3 | 58.6 | 64.6 | +6.1 | +1.3 |
| Hieroglyph Quest: Body & Healing | 65.3 | 63.0 | 62.8 | -0.1 | -2.5 |
| Hieroglyph Quest: Core Set: Daily Life | 62.9 | 62.1 | 60.8 | -1.3 | -2.0 |
| Hieroglyph Quest: Gods & Temples | 62.5 | 60.3 | 62.2 | +1.9 | -0.3 |
| Hieroglyph Quest: Kings & Court | 59.7 | 58.7 | 61.4 | +2.7 | +1.7 |
| Hieroglyph Quest: Pantheon Expanded | 62.9 | 63.0 | 62.2 | -0.8 | -0.7 |
| Hieroglyph Quest: The Land of Egypt | 65.2 | 59.4 | 62.4 | +3.0 | -2.7 |
| Hieroglyph Quest: Wild Egypt | 61.9 | 60.4 | 61.7 | +1.3 | -0.2 |

## Dead-card rate — four-way comparison

| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 14% | 14% | 15% | +0.4 pp |
| Hieroglyph Quest: Body & Healing | 13% | 14% | 14% | +0.0 pp |
| Hieroglyph Quest: Core Set: Daily Life | 15% | 16% | 15% | -1.2 pp |
| Hieroglyph Quest: Gods & Temples | 13% | 14% | 14% | +0.3 pp |
| Hieroglyph Quest: Kings & Court | 17% | 17% | 15% | -2.8 pp |
| Hieroglyph Quest: Pantheon Expanded | 14% | 15% | 16% | +0.9 pp |
| Hieroglyph Quest: The Land of Egypt | 15% | 15% | 14% | -0.9 pp |
| Hieroglyph Quest: Wild Egypt | 14% | 16% | 14% | -2.4 pp |

## Shrunk-deck results, by player count

### Balance score

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 67.8 | 66.1 | 60.0 | 64.6 |
| Hieroglyph Quest: Body & Healing | 60.8 | 66.7 | 61.0 | 62.8 |
| Hieroglyph Quest: Core Set: Daily Life | 60.8 | 60.9 | 60.8 | 60.8 |
| Hieroglyph Quest: Gods & Temples | 65.4 | 63.9 | 57.4 | 62.2 |
| Hieroglyph Quest: Kings & Court | 68.4 | 62.9 | 52.8 | 61.4 |
| Hieroglyph Quest: Pantheon Expanded | 65.0 | 60.7 | 60.8 | 62.2 |
| Hieroglyph Quest: The Land of Egypt | 66.0 | 60.5 | 60.8 | 62.4 |
| Hieroglyph Quest: Wild Egypt | 59.8 | 66.7 | 58.6 | 61.7 |

### Median turns

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 249 | 336 | 449 | 345 |
| Hieroglyph Quest: Body & Healing | 213 | 313 | 378 | 301 |
| Hieroglyph Quest: Core Set: Daily Life | 232 | 355 | 415 | 334 |
| Hieroglyph Quest: Gods & Temples | 248 | 328 | 471 | 349 |
| Hieroglyph Quest: Kings & Court | 244 | 358 | 470 | 357 |
| Hieroglyph Quest: Pantheon Expanded | 281 | 392 | 514 | 396 |
| Hieroglyph Quest: The Land of Egypt | 251 | 360 | 493 | 368 |
| Hieroglyph Quest: Wild Egypt | 225 | 283 | 401 | 303 |

### Victory rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 98% | 96% | 88% | 94% |
| Hieroglyph Quest: Body & Healing | 96% | 96% | 86% | 93% |
| Hieroglyph Quest: Core Set: Daily Life | 96% | 100% | 96% | 97% |
| Hieroglyph Quest: Gods & Temples | 90% | 94% | 82% | 89% |
| Hieroglyph Quest: Kings & Court | 100% | 94% | 88% | 94% |
| Hieroglyph Quest: Pantheon Expanded | 94% | 94% | 88% | 92% |
| Hieroglyph Quest: The Land of Egypt | 92% | 88% | 88% | 89% |
| Hieroglyph Quest: Wild Egypt | 98% | 98% | 94% | 97% |

### Dead-card rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 21% | 13% | 10% | 15% |
| Hieroglyph Quest: Body & Healing | 20% | 13% | 10% | 14% |
| Hieroglyph Quest: Core Set: Daily Life | 20% | 14% | 12% | 15% |
| Hieroglyph Quest: Gods & Temples | 19% | 13% | 10% | 14% |
| Hieroglyph Quest: Kings & Court | 16% | 17% | 10% | 15% |
| Hieroglyph Quest: Pantheon Expanded | 21% | 14% | 12% | 16% |
| Hieroglyph Quest: The Land of Egypt | 19% | 13% | 10% | 14% |
| Hieroglyph Quest: Wild Egypt | 18% | 13% | 12% | 14% |

## Health flags

All decks pass health checks under the shrunk unified-signs deck (431 copies).
