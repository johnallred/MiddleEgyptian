# 2-Player Catch-Up Mechanic Playtest (v8.9 candidates)

Core deck (v8.8 build), 2 players, target 8 points, 1000 games per matchup, seed 1000, max 800 turns.

**Metric.** `first-scorer-wins %` = how often the seat that scores the game's first word goes on to win. 50% = perfect comeback health; 100% = pure runaway. The composite balance score never measured this.

All candidates are table-trackable by design: they trigger on events (a word was just scored / stolen) or use a physical token, never on score arithmetic like 'behind by 3+'.

## Comeback health (balanced mirror)

| Candidate | First-scorer wins | Median turns | Steals/g | Logograms/g | Mulligans/g |
|---|---:|---:|---:|---:|---:|
| baseline | 60.1% | 120 | 1.07 | 0.76 | 0.0 |
| rebound1 | 59.5% | 120 | 1.06 | 0.77 | 0.0 |
| salve2 | 60.0% | 118 | 1.07 | 0.78 | 0.0 |
| mulligan1 | 53.5% | 128 | 1.43 | 0.99 | 1.63 |
| token | 56.6% | 108 | 1.09 | 0.8 | 0.0 |
| reb_mull | 57.4% | 126 | 1.42 | 0.99 | 1.63 |

## Skill check (greedy vs balanced)

Balanced should keep beating greedy by a similar margin — catch-up should rescue the *trailing* player, not the *weaker* one.

| Candidate | Balanced win % | Greedy win % | First-scorer wins |
|---|---:|---:|---:|
| baseline | 58.0 | 42.0 | 56.8% |
| rebound1 | 59.4 | 40.6 | 54.8% |
| salve2 | 58.1 | 41.9 | 57.1% |
| mulligan1 | 59.7 | 40.3 | 55.7% |
| token | 59.0 | 41.0 | 56.2% |
| reb_mull | 57.6 | 42.4 | 55.0% |

Levers: `score_rebound_draw`, `steal_victim_draws`, `word_mulligan`, `underdog_token` in `playtest_simulator.GameConfig` (all default off). First-scorer tracking is now a permanent GameRecord field.