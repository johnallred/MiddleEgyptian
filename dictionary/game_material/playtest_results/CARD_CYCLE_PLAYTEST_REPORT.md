# Card-Cycle Actions Playtest (rules-fidelity check)

Core deck (v8.9 build), classic mode, 300 games per cell, seed 1000, scaled points (2p=8, 3p=7, 4p=6), max 800 turns.

The engine has always granted agents two actions the printed rules never mention: `trash_and_draw` (discard 2 useless signs, draw 2) and `look_and_take` (peek top 3, take 1, discard 1). `printed` below is the game exactly as rules.md reads.

## Balanced mirror by player count

| Variant | Players | Victory % | Median turns | First-scorer wins | Steals/g | Logograms/g | Trash/g | Mulligans/g |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 2 | 100.0 | 132 | 54.7% | 1.46 | 0.91 | 94.12 | 1.64 |
| baseline | 3 | 100.0 | 105 | 38.3% | 2.4 | 1.05 | 73.35 | 2.26 |
| baseline | 4 | 100.0 | 108 | 33.0% | 3.52 | 1.39 | 74.19 | 2.79 |
| no_trash | 2 | 100.0 | 180 | 56.7% | 0.9 | 0.9 | 0.0 | 1.71 |
| no_trash | 3 | 100.0 | 132 | 42.0% | 1.83 | 1.03 | 0.0 | 2.3 |
| no_trash | 4 | 100.0 | 124 | 32.0% | 2.43 | 1.17 | 0.0 | 2.83 |
| no_look | 2 | 99.7 | 140 | 60.3% | 1.49 | 1.05 | 137.76 | 1.64 |
| no_look | 3 | 100.0 | 120 | 40.3% | 2.59 | 1.3 | 112.6 | 2.3 |
| no_look | 4 | 100.0 | 112 | 30.7% | 3.82 | 1.58 | 112.54 | 2.88 |
| printed | 2 | 99.7 | 294 | 58.0% | 1.29 | 1.09 | 0.0 | 1.75 |
| printed | 3 | 100.0 | 219 | 41.7% | 2.15 | 1.23 | 0.0 | 2.4 |
| printed | 4 | 100.0 | 216 | 33.7% | 3.01 | 1.59 | 0.0 | 2.97 |

## Skill check (greedy vs balanced, 2p)

| Variant | Balanced win % | Greedy win % |
|---|---:|---:|
| baseline | 60.3 | 39.7 |
| no_trash | 92.7 | 7.3 |
| no_look | 48.0 | 52.0 |
| printed | 48.0 | 52.0 |

Levers: `GameConfig.allow_trash_and_draw`, `GameConfig.allow_look_and_take`.