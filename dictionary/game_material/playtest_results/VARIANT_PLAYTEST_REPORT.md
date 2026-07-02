# Rule-Variant Playtest Report (v8.8 candidates)

Core deck (`deck.json`, v8.7 build), balanced-vs-balanced, 500 games per cell, seed 1000, scaled points (2p=8, 3p=7, 4p=6), max 800 turns.

**Candidate 1 — cut the trade rule:** not simulatable; player-to-player trading was never modeled in the engine, so all published balance data already describes a trade-free game. Cutting it from rules.md has zero measured impact (and removes an unbounded collusion/kingmaking channel at 3+ players).

| Variant | Players | Balance | Victory % | Median turns | Avg score | Steals/g | Logograms/g | Exchanges/g |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 2 | 98.2 | 99.8 | 106 | 6.8 | 0.75 | 0.47 | 0.0 |
| baseline | 3 | 98.7 | 100.0 | 84 | 4.3 | 1.27 | 0.48 | 0.0 |
| baseline | 4 | 95.4 | 100.0 | 88 | 3.2 | 1.88 | 0.64 | 0.0 |
| word_draw2 | 2 | 96.7 | 99.8 | 110 | 6.6 | 1.38 | 0.67 | 0.0 |
| word_draw2 | 3 | 97.2 | 100.0 | 90 | 4.7 | 2.46 | 0.77 | 0.0 |
| word_draw2 | 4 | 97.1 | 100.0 | 92 | 3.5 | 3.46 | 1.03 | 0.0 |
| strip_1sign | 2 | 98.2 | 99.8 | 112 | 6.7 | 0.62 | 0.5 | 0.0 |
| strip_1sign | 3 | 97.0 | 100.0 | 84 | 4.2 | 1.06 | 0.53 | 0.0 |
| strip_1sign | 4 | 97.1 | 100.0 | 96 | 3.2 | 1.58 | 0.71 | 0.0 |
| logo_exchange | 2 | 98.7 | 99.8 | 124 | 6.7 | 0.63 | 0.24 | 29.84 |
| logo_exchange | 3 | 99.5 | 100.0 | 90 | 4.3 | 1.01 | 0.33 | 26.79 |
| logo_exchange | 4 | 96.6 | 100.0 | 108 | 3.2 | 1.58 | 0.49 | 32.09 |
| logo_exchange1 | 2 | 98.3 | 99.8 | 122 | 6.6 | 0.63 | 0.26 | 28.08 |
| logo_exchange1 | 3 | 99.3 | 100.0 | 96 | 4.2 | 1.03 | 0.32 | 31.98 |
| logo_exchange1 | 4 | 97.8 | 100.0 | 104 | 3.2 | 1.6 | 0.44 | 37.62 |
| combined | 2 | 98.9 | 100.0 | 140 | 6.7 | 0.86 | 0.4 | 33.61 |
| combined | 3 | 96.1 | 100.0 | 126 | 4.6 | 1.34 | 0.53 | 33.71 |
| combined | 4 | 97.4 | 100.0 | 124 | 3.4 | 2.23 | 0.74 | 35.12 |

## Deltas vs baseline (averaged across player counts)

| Variant | Δ balance | Δ median turns | Δ logograms/g | Δ steals/g |
|---|---:|---:|---:|---:|
| word_draw2 | -0.4 | +5 | +0.29 | +1.13 |
| strip_1sign | -0.0 | +5 | +0.05 | -0.21 |
| logo_exchange | +0.8 | +15 | -0.18 | -0.23 |
| logo_exchange1 | +1.0 | +15 | -0.19 | -0.21 |
| combined | +0.0 | +37 | +0.03 | +0.18 |

Notes (strip_1sign): {'words_with_1sign_spelling_stripped': 23, 'words_kept_single_1sign_spelling': 0}
Notes (combined): {'words_with_1sign_spelling_stripped': 23, 'words_kept_single_1sign_spelling': 0}

Implementation levers: `GameConfig.word_draw_n` (draw N word cards keep 1, rejects go to the bottom of the word deck), `GameConfig.dead_logogram_exchange` (N = sign draws granted; the exchanged logogram goes to the sign discard pile, so it recirculates when the deck recycles), and `playtest_variants.strip_one_sign_spellings()` (word-pool transform; not yet a deck-builder change). Word cards keep their printed point values in the strip test even though their effective shortest spelling got longer — repointing is a follow-up decision if the variant is adopted.

## Reading of the results

**word_draw2 — adopt.** Balance and length are unchanged, but interactivity jumps: steals nearly double overall (1.88 → 3.46/game at 4p) and logogram completions rise ~60%, because players holding better-fitting words complete and rotate more, and everyone's hands stay relevant to the table. This is the comeback/engagement dynamic the human playtest checklist hopes steals will provide. Zero component cost: 'draw 2 word cards, keep 1, bottom the other.'

**strip_1sign — adopt for feel, neutral on data.** Only 23 word cards (the trivial tier) even have a 1-sign spelling; stripping it moves nothing measurable (Δ balance −0.0, +5 turns). The payoff is qualitative: logogram cards become the only single-card completions again, protecting their 'lottery win' identity. Requires a deck-builder change plus a decision on repointing the affected tier-1 cards.

**logo_exchange — do NOT adopt as an unrestricted action.** In both the 2-draw and 1-draw forms, agents exchange ~30 times per game (a quarter of all turns): any logogram not matching an active word is instantly cashed in, logogram COMPLETIONS drop by ~40% (0.47 → 0.24-0.26 at 2p), and games lengthen ~15 turns. The valve doesn't relieve logogram frustration — it converts logograms into a draw engine and cannibalizes exactly the 'yes!' moments the mechanic exists to create. If a valve is still wanted after human playtests, test a bounded form (once per player per game).

**combined — fine but slower.** Balance holds (96-99) but median length grows ~37 turns (~9 min at 15 s/turn), mostly from the exchange churn. Adopting word_draw2 + strip_1sign without the exchange is the better package.