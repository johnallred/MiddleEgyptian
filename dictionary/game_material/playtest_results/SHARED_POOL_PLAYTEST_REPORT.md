# Shared Word Pool Playtest (race, not theft)

Core deck (v8.9 build), 150 games per cell, seed 1000, scaled points (2p=8, 3p=7, 4p=6), max 800 turns. `shared_word_pool` lever in GameConfig; classic = 0.

In shared mode there are no personal words, no steals, and no word mulligan; a face-up row of N word cards is open to everyone and refills after each completion.

## Balanced mirror by player count

| Variant | Players | First-scorer wins | Median turns | Victory % | Avg score | Logograms/g | Steals/g | Trash/g |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classic | 2 | 55.3% | 140 | 100.0 | 6.9 | 0.82 | 1.44 | 96.54 |
| classic | 3 | 44.0% | 108 | 100.0 | 4.6 | 0.94 | 2.49 | 75.19 |
| classic | 4 | 35.3% | 108 | 100.0 | 3.6 | 1.31 | 3.7 | 76.39 |
| shared4 | 2 | 69.1% | 800 | 48.7 | 4.5 | 0.94 | 0.0 | 547.89 |
| shared4 | 3 | 49.3% | 168 | 99.3 | 4.2 | 0.99 | 0.0 | 219.61 |
| shared4 | 4 | 36.7% | 216 | 96.7 | 3.1 | 0.91 | 0.0 | 236.55 |
| shared5 | 2 | 51.7% | 464 | 68.0 | 5.3 | 1.08 | 0.0 | 445.8 |
| shared5 | 3 | 48.0% | 138 | 100.0 | 4.3 | 1.09 | 0.0 | 179.44 |
| shared5 | 4 | 32.0% | 108 | 100.0 | 3.1 | 1.04 | 0.0 | 181.47 |
| shared6 | 2 | 56.0% | 266 | 82.7 | 5.9 | 1.13 | 0.0 | 354.98 |
| shared6 | 3 | 44.0% | 108 | 98.7 | 4.5 | 1.1 | 0.0 | 156.95 |
| shared6 | 4 | 42.0% | 108 | 99.3 | 3.0 | 1.09 | 0.0 | 141.33 |
| shared5_dredge | 2 | 57.3% | 188 | 100.0 | 6.3 | 2.01 | 0.0 | 203.55 |
| shared5_dredge | 3 | 54.0% | 114 | 100.0 | 4.4 | 1.83 | 0.0 | 126.67 |
| shared5_dredge | 4 | 35.3% | 108 | 100.0 | 3.2 | 1.77 | 0.0 | 121.3 |

## Skill check (random vs balanced, 2p)

Greedy and balanced collapse to the same policy in shared mode, so random-vs-balanced is the meaningful gap. Classic shows the same matchup for comparison.

| Variant | Balanced win % | First-scorer wins |
|---|---:|---:|
| classic | 86.0 | 70.0% |
| shared4 | 64.7 | 62.8% |
| shared5 | 74.0 | 65.3% |
| shared6 | 84.0 | 71.3% |
| shared5_dredge | 82.7 | 62.7% |

## Reading of the results

**1. The naked shared pool stalls at 2 players.** With no way to cycle the row, both players clear the easy words and then sit staring at 4-6 leftovers nobody can build: shared4's 2p median hit the 800-turn cap; shared5 ran 464 turns vs classic's 140. Smaller rows stall harder (fewer outs). 3p/4p churn the row naturally and play at classic speed.

**2. Dredge is mandatory.** Adding 'spend your action to bottom one row card and refill' (shared5_dredge) cuts the 2p median from 464 to 188 turns, doubles logogram fire rate (dredging surfaces targets), and restores the skill gap (balanced-vs-random 74% → 83%, near classic's 86%). Any table version of Race Mode must include it.

**3. Even with dredge, shared mode doesn't beat classic on any measured axis.** 2p games run ~35% longer (188 vs 140), 3p comeback health is worse (first-scorer-wins 54% vs 44%), and skill expression is a touch lower. Its genuine advantages are exactly the ones the simulator can't see: no steal social friction, no personal-word frustration, fully visible shared state. Note that classic v8.9 already fixed 'blind word assignment' (word draw-2-keep-1 + mulligan), so shared mode's original selling points have partly been absorbed.

**Recommendation:** ship as an optional 'Race Mode' variant (row of 5, dredge included, no steals/mulligan) rather than replacing the classic rules. It costs zero new components and gives steal-averse tables an official way to play; the tuned classic game remains the default. If human playtests show the steal mechanic consistently souring tables, revisit promotion of Race Mode with a 2p target-point retune.

## Caveats the numbers can't see

Agents race but do not model **denial** (grabbing a word specifically because an opponent is close to it), **table talk**, or the reading load of a 4-6 card open row for players still learning the signs. Human playtests should weight those; the simulator's job here is speed, balance, comeback health, and degenerate-loop detection only.