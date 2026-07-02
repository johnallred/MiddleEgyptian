# Co-op / Solo Mode Playtest

Core deck (v8.10 build), classic mechanics, team scoring, sign deck limited to 2 passes (one reshuffle), one dry round of grace at deck death. 300 games per cell, seed 1000, balanced agents unless noted. Win rate for a target T = share of games whose team total at deck death reached T (exact, since agents are not target-aware).

## Team score at deck death (the whole difficulty curve)

| Players | Median score | Range | Words/game | Median turns | Mulligans/g | Logograms/g |
|---:|---:|---|---:|---:|---:|---:|
| 1 | 17.0 | [3, 33] | 7.8 | 180.0 | 0.98 | 1.08 |
| 2 | 15.0 | [4, 40] | 8.5 | 176.0 | 1.77 | 1.47 |
| 3 | 21.0 | [5, 49] | 11.9 | 177.0 | 2.56 | 2.1 |
| 4 | 21.0 | [4, 41] | 12.5 | 173.0 | 3.32 | 2.37 |

## Win rate by target

| Target | 1p | 2p | 3p | 4p |
|---:|---:|---:|---:|---:|
| 5 | 99.7% | 99.3% | 100.0% | 99.7% |
| 10 | 88.7% | 86.3% | 95.7% | 97.0% |
| 15 | 64.0% | 56.7% | 83.3% | 83.3% |
| 20 | 29.7% | 26.3% | 59.0% | 58.7% |
| 25 | 10.3% | 9.3% | 34.3% | 31.3% |
| 30 | 3.0% | 1.7% | 14.0% | 11.7% |
| 35 | 0.0% | 0.7% | 5.0% | 3.7% |
| 40 | 0.0% | 0.3% | 1.7% | 0.3% |
| 45 | 0.0% | 0.0% | 0.7% | 0.0% |

## Recommended printed difficulty tiers

Chosen as the largest target still winning at roughly 90% (Apprentice), 60% (Scribe), and 30% (Master Scribe):

| Players | Apprentice (~90%) | Scribe (~60%) | Master Scribe (~30%) |
|---:|---:|---:|---:|
| 1 | 9 | 15 | 19 |
| 2 | 9 | 14 | 19 |
| 3 | 13 | 19 | 25 |
| 4 | 13 | 19 | 25 |

## Random-agent sanity check

- 1p random agents: median team score 14.0 (range [4, 28]) — skill should and does matter.
- 2p random agents: median team score 12.0 (range [1, 34]) — skill should and does matter.

## Caveats

Agents are not clock-aware: they recycle (discard 2 / draw 2) on idle turns even when the deck is nearly dead, where a human team would hoard. Real teams should therefore score somewhat HIGHER than these curves late in the deck, making the printed tiers slightly easier than measured — the right direction to err for a co-op. Table talk and coordinated assists (trading completions) are also unmodeled upside. Engine levers: `GameConfig.coop_mode`, `GameConfig.coop_sign_deck_passes`.