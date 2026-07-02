# Hieroglyph Quest — Master Balance Report

Player counts tested: [2, 3, 4]. 300 games per matchup, seed 1000, target v8.6 scaled points (2p=8, 3p=7, 4p=6), max 800 turns. Ruleset v8.10 (multiset spelling match, market 5, sign draw-2-keep-1, WORD draw-2-keep-1, 1-sign spellings stripped from word cards, word mulligan once per player per game, recycle (discard 2 draw 2) printed, look-and-take removed, discard-take at 3p+, equal-turns endgame, no first-player gift).

## Matchup summary (by player count)

| Players | Matchup | Balance | Victories | Median turns | Avg score | Steals/game | Logograms/game | First-scorer wins | Mulligans/game |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | balanced vs balanced | 98.9 | 300/300 (100%) | 142 | 6.5 | 1.49 | 1.05 | 52% | 1.66 |
| 2 | greedy vs balanced | 98.9 | 300/300 (100%) | 142 | 6.5 | 1.49 | 1.05 | 52% | 1.66 |
| 2 | greedy vs greedy | 98.9 | 300/300 (100%) | 142 | 6.5 | 1.49 | 1.05 | 52% | 1.66 |
| 2 | random vs balanced | 47.9 | 299/300 (100%) | 178 | 6.3 | 0.95 | 0.8 | 64% | 1.64 |
| 2 | random vs random | 69.7 | 300/300 (100%) | 252 | 6.6 | 0.35 | 0.72 | 60% | 1.67 |
| 3 | balanced vs balanced vs balanced | 99.5 | 300/300 (100%) | 117 | 4.8 | 2.46 | 1.21 | 36% | 2.27 |
| 3 | greedy vs greedy vs greedy | 99.5 | 300/300 (100%) | 117 | 4.8 | 2.46 | 1.21 | 36% | 2.27 |
| 3 | random vs random vs random | 64.0 | 299/300 (100%) | 201 | 4.6 | 0.53 | 0.84 | 39% | 2.26 |
| 4 | balanced vs balanced vs balanced vs balanced | 95.7 | 300/300 (100%) | 112 | 3.6 | 3.8 | 1.51 | 31% | 2.83 |
| 4 | greedy vs greedy vs greedy vs greedy | 95.7 | 300/300 (100%) | 112 | 3.6 | 3.8 | 1.51 | 31% | 2.83 |
| 4 | random vs random vs random vs random | 68.7 | 300/300 (100%) | 200 | 3.4 | 0.8 | 1.09 | 32% | 2.81 |

## Seat advantage by matchup (target = 1/N per seat)

| Players | Matchup | Seat rates | Max deviation |
|---:|---|---|---:|
| 2 | balanced vs balanced | 51.3% / 48.7% | +1.3% |
| 2 | greedy vs balanced | 51.3% / 48.7% | +1.3% |
| 2 | greedy vs greedy | 51.3% / 48.7% | +1.3% |
| 2 | random vs balanced | 21.7% / 78.3% | +28.3% |
| 2 | random vs random | 49.7% / 50.3% | +0.3% |
| 3 | balanced vs balanced vs balanced | 32.7% / 34.0% / 33.3% | +0.7% |
| 3 | greedy vs greedy vs greedy | 32.7% / 34.0% / 33.3% | +0.7% |
| 3 | random vs random vs random | 40.7% / 28.3% / 31.0% | +7.4% |
| 4 | balanced vs balanced vs balanced vs balanced | 24.3% / 25.7% / 29.7% / 20.3% | +4.7% |
| 4 | greedy vs greedy vs greedy vs greedy | 24.3% / 25.7% / 29.7% / 20.3% | +4.7% |
| 4 | random vs random vs random vs random | 25.3% / 23.3% / 26.3% / 25.0% | +1.7% |

### Agent skill ordering

Where the same agent appears in mixed matchups, its win rate:

| Agent | Players | Matchup | Win rate |
|---|---:|---|---:|
| random | 2 | random vs random | 50.0% |
| random | 3 | random vs random vs random | 33.3% |
| random | 4 | random vs random vs random vs random | 25.0% |
| random | 2 | random vs balanced | 21.7% |
| greedy | 2 | greedy vs balanced | 51.3% |
| greedy | 2 | greedy vs greedy | 50.0% |
| greedy | 3 | greedy vs greedy vs greedy | 33.3% |
| greedy | 4 | greedy vs greedy vs greedy vs greedy | 25.0% |
| balanced | 2 | random vs balanced | 78.3% |
| balanced | 2 | balanced vs balanced | 50.0% |
| balanced | 2 | greedy vs balanced | 48.7% |
| balanced | 3 | balanced vs balanced vs balanced | 33.3% |
| balanced | 4 | balanced vs balanced vs balanced vs balanced | 25.0% |

## Top 20 most-completed word cards (across all matchups)

| Word | Total completions |
|---|---:|
| `hAw` | 437 |
| `wHAt` | 397 |
| `hAi` | 387 |
| `biA` | 350 |
| `qmA` | 347 |
| `im` | 337 |
| `twA` | 311 |
| `Xsy` | 240 |
| `iAs` | 219 |
| `dm` | 210 |
| `Ais` | 208 |
| `inr` | 207 |
| `Hryt` | 192 |
| `tn` | 192 |
| `bAq` | 184 |
| `wnwt` | 178 |
| `hnn` | 173 |
| `aq` | 144 |
| `ST` | 142 |
| `Hw` | 138 |

## Dead cards: word cards never completed in 3,300 games

**134 of 165 word cards** (81.2%) never got completed.

These cards never made it to a score pile. They may be too hard (too many required signs, or signs not stocked in the sign deck), wrongly tier-graded, or simply unlucky.

First 30 (sample):

```
ATwt
Afry
Apd
Aqs
DArw
DbA
HDD
Haawt
Hawt
Hn
Hni
Hnkw
Hnkyt
Hsb
Htm
HwAAt
Hwn
SAd
SAmw
SbSb
Sf
SmSmt
Stw
Tnfyt
TpHt
Tsm
Xaq
Xkr
aHaw
afnt
```

## Broken openers across all matchups

Opening hands that won >=70% of the time in at least 3 games. Listed per matchup so you can reproduce by seeding.

## Recommendations

**Average balance score across matchups: 85.2/100**.

- **Seat advantage detected** (up to 28.3% from the per-seat target). Consider seat-position compensation.

## Reproducibility

Every result here is reproducible. Base seed: `1000`. Each individual game uses `seed = base_seed + game_index`. To replay a specific game, run:

```bash
python3 playtest_simulator.py --games 1 --seed 1000 --agents balanced,balanced --out single_game.md
```