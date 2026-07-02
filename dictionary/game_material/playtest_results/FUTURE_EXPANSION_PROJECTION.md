# Future-Expansion Projection: 431-Copy Unified Sign Deck

**Question:** the shrunk 431-copy unified sign deck was built from the 8 current expansion decks. Will it support future expansion decks built from the long tail of the dictionary, or will those need their own sign cards?

Two checks were run.

## 1. Analytical sign coverage across the unused dictionary pool

Of the **9,466** playable words in `Entries2.json`, **1,137** are already in one of the 8 current expansions, leaving **8,329** unused. That long tail is the pool future expansions will draw from.

**Words with sign demand the shrunk deck can't fulfill:** **583** (7.0% of unused).

These signs are required by some unused words but are **absent from the shrunk 431-copy deck entirely**. Any expansion built around them would need to ship its own copies of these specific signs, or skip the affected words:

| Sign code | Unused words blocked |
|---|---:|
| `D52` | 68 |
| `W17` | 29 |
| `N28` | 22 |
| `S33` | 20 |
| `I6` | 19 |
| `D45` | 18 |
| `M30` | 18 |
| `M29` | 18 |
| `U36` | 18 |
| `D60` | 15 |
| `F29` | 14 |
| `U24` | 14 |
| `N40` | 13 |
| `I1` | 13 |
| `M26` | 13 |
| `M20` | 12 |
| `D61` | 12 |
| `S19` | 12 |
| `U17` | 11 |
| `O22` | 10 |
| `S40` | 10 |
| `T18` | 10 |
| `O47` | 10 |
| `V26` | 9 |
| `U26` | 9 |

### Highest-demand signs across the unused word pool

This shows which signs would be drawn on most by future expansions. The `In shrunk deck` column shows how many copies the 431-copy deck holds; the `Words using` column shows how many unused words include this sign.

| Sign | In shrunk deck | Words using | Total uses |
|---|---:|---:|---:|
| `X1` | 4 | 2,694 | 3,095 |
| `M17` | 4 | 1,584 | 2,313 |
| `N35` | 4 | 1,688 | 1,904 |
| `D21` | 4 | 1,593 | 1,742 |
| `G1` | 4 | 1,365 | 1,556 |
| `G43` | 4 | 1,059 | 1,118 |
| `D36` | 4 | 930 | 1,042 |
| `S29` | 4 | 924 | 978 |
| `G17` | 4 | 876 | 938 |
| `D58` | 4 | 756 | 828 |
| `Z7` | 4 | 717 | 783 |
| `D46` | 4 | 627 | 675 |
| `V28` | 4 | 584 | 608 |
| `Q3` | 4 | 528 | 556 |
| `Y1` | 1 | 479 | 486 |
| `I9` | 4 | 458 | 485 |
| `O34` | 4 | 433 | 456 |
| `N37` | 4 | 412 | 449 |
| `O1` | 4 | 393 | 442 |
| `V31` | 4 | 385 | 417 |

## 2. Synthetic future-expansion playtests

Four hypothetical future expansion decks were built from the largest unused-domain pools in the dictionary, then played 50 games each at 2/3/4p **against the shrunk 431-copy unified sign deck** (no per-theme sign tuning).

| Synthetic theme | Domain pool | Words drawn | Logograms | Per-theme sign copies it would have used |
|---|---|---:|---:|---:|
| Builders of Egypt | architecture | 165 | 14 | 330 |
| Markets & Feasts | food | 165 | 16 | 329 |
| Houses & Hearths | furniture | 165 | 17 | 346 |
| Threads of Linen | clothing | 163 | 20 | 333 |

### Results at the shrunk 431-copy unified sign deck

Reference baselines from the original expansion playtest (per-theme tuned signs, hand=8): balance avg = ~62, victory ≥ 80%, dead-card rate ~14–17%.

| Theme | 2p balance | 3p balance | 4p balance | Avg balance | Avg victory | Avg dead | Avg turns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Builders of Egypt | 66.8 | 58.1 | 56.4 | 60.4 | 93% | 22% | 310 |
| Markets & Feasts | 67.0 | 58.1 | 59.0 | 61.4 | 89% | 23% | 320 |
| Houses & Hearths | 57.2 | 65.7 | 55.8 | 59.6 | 96% | 20% | 313 |
| Threads of Linen | 58.4 | 59.3 | 50.4 | 56.0 | 81% | 24% | 349 |

### Health flags

- **Builders of Egypt**: dead-card 22% above 20%
- **Markets & Feasts**: dead-card 23% above 20%
- **Threads of Linen**: dead-card 24% above 20%
