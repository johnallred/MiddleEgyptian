# Unified Sign Deck — Re-Playtest Report

**Tested architecture:** signs centralized in base, expansions ship words + logograms only.

All cells: 50 games with `balanced` agent, seed 1000, target 10 points, max 800 turns.

**Unified sign deck:** 238 unique Gardiner codes, **547 total card copies**.

Built by taking the union of every sign code seen across any of the 8 expansion sign decks, with each sign's copy count set to the maximum copy count that sign had in any single expansion. This guarantees the unified deck can support every expansion at the per-theme tuned sign-demand it was designed for.

## Balance: per-theme signs vs. unified signs

| Deck | Per-theme avg | Unified avg | Δ |
|---|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 63.3 | 58.6 | -4.7 |
| Hieroglyph Quest: Body & Healing | 65.3 | 63.0 | -2.3 |
| Hieroglyph Quest: Core Set: Daily Life | 62.9 | 62.1 | -0.8 |
| Hieroglyph Quest: Gods & Temples | 62.5 | 60.3 | -2.2 |
| Hieroglyph Quest: Kings & Court | 59.7 | 58.7 | -1.0 |
| Hieroglyph Quest: Pantheon Expanded | 62.9 | 63.0 | +0.1 |
| Hieroglyph Quest: The Land of Egypt | 65.2 | 59.4 | -5.7 |
| Hieroglyph Quest: Wild Egypt | 61.9 | 60.4 | -1.5 |

## Dead-card rate: per-theme signs vs. unified signs

| Deck | Per-theme avg | Unified avg | Δ |
|---|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 14% | 14% | +0.1 pp |
| Hieroglyph Quest: Body & Healing | 13% | 15% | +1.2 pp |
| Hieroglyph Quest: Core Set: Daily Life | 15% | 16% | +1.2 pp |
| Hieroglyph Quest: Gods & Temples | 13% | 14% | +0.2 pp |
| Hieroglyph Quest: Kings & Court | 17% | 18% | +0.9 pp |
| Hieroglyph Quest: Pantheon Expanded | 14% | 15% | +0.9 pp |
| Hieroglyph Quest: The Land of Egypt | 15% | 15% | +0.3 pp |
| Hieroglyph Quest: Wild Egypt | 14% | 16% | +2.7 pp |

## Unified-signs results, by player count

### Balance score

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 59.6 | 57.1 | 59.0 | 58.6 |
| Hieroglyph Quest: Body & Healing | 65.6 | 60.9 | 62.4 | 63.0 |
| Hieroglyph Quest: Core Set: Daily Life | 66.2 | 61.3 | 58.8 | 62.1 |
| Hieroglyph Quest: Gods & Temples | 67.2 | 58.5 | 55.2 | 60.3 |
| Hieroglyph Quest: Kings & Court | 57.6 | 61.9 | 56.6 | 58.7 |
| Hieroglyph Quest: Pantheon Expanded | 68.8 | 64.3 | 55.8 | 63.0 |
| Hieroglyph Quest: The Land of Egypt | 65.4 | 58.1 | 54.8 | 59.4 |
| Hieroglyph Quest: Wild Egypt | 60.8 | 60.7 | 59.8 | 60.4 |

### Victory rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 92% | 82% | 82% | 85% |
| Hieroglyph Quest: Body & Healing | 96% | 98% | 80% | 91% |
| Hieroglyph Quest: Core Set: Daily Life | 98% | 96% | 84% | 93% |
| Hieroglyph Quest: Gods & Temples | 96% | 92% | 80% | 89% |
| Hieroglyph Quest: Kings & Court | 96% | 96% | 74% | 89% |
| Hieroglyph Quest: Pantheon Expanded | 96% | 90% | 74% | 87% |
| Hieroglyph Quest: The Land of Egypt | 90% | 94% | 76% | 87% |
| Hieroglyph Quest: Wild Egypt | 96% | 94% | 90% | 93% |

### Dead-card rate

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 22% | 12% | 9% | 14% |
| Hieroglyph Quest: Body & Healing | 21% | 14% | 8% | 15% |
| Hieroglyph Quest: Core Set: Daily Life | 22% | 15% | 12% | 16% |
| Hieroglyph Quest: Gods & Temples | 20% | 12% | 9% | 14% |
| Hieroglyph Quest: Kings & Court | 19% | 18% | 15% | 18% |
| Hieroglyph Quest: Pantheon Expanded | 21% | 14% | 10% | 15% |
| Hieroglyph Quest: The Land of Egypt | 21% | 13% | 11% | 15% |
| Hieroglyph Quest: Wild Egypt | 23% | 15% | 11% | 16% |

### Median game length (turns)

| Deck | 2p | 3p | 4p | Avg |
|---|---:|---:|---:|---:|
| Hieroglyph Quest: Beasts of the Nile | 321 | 460 | 531 | 437 |
| Hieroglyph Quest: Body & Healing | 269 | 363 | 554 | 395 |
| Hieroglyph Quest: Core Set: Daily Life | 353 | 416 | 548 | 439 |
| Hieroglyph Quest: Gods & Temples | 288 | 421 | 576 | 428 |
| Hieroglyph Quest: Kings & Court | 314 | 393 | 532 | 413 |
| Hieroglyph Quest: Pantheon Expanded | 288 | 447 | 569 | 435 |
| Hieroglyph Quest: The Land of Egypt | 333 | 429 | 591 | 451 |
| Hieroglyph Quest: Wild Egypt | 288 | 408 | 528 | 408 |

## Health flags (unified signs)

All decks pass health checks under the unified-signs architecture (balance ≥ 55, victory ≥ 80%, dead-card rate ≤ 20%).
