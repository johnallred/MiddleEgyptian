# Expert Agent Report (v9 simulator tier)

Classic v8.10 rules, core deck, 500 games per matchup, seed 1000, scaled points.

Expert = value-maximizing completions + easiest-spelling draw targeting + denial-aware discards (3p+). Balanced is the production baseline agent.

| Matchup | Expert win % | Fair share | Median turns | Steals/g | Logos/g | First-scorer wins | Victory % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2p_expert_vs_balanced | 50.4 | 50% | 142 | 1.57 | 1.04 | 53.2% | 99.8 |
| 2p_expert_mirror | 50.0 | 50% | 142 | 1.56 | 1.04 | 53.2% | 99.8 |
| 3p_expert_vs_balanced | 36.4 | 33% | 123 | 2.65 | 1.24 | 42.6% | 100.0 |
| 4p_expert_vs_balanced | 23.4 | 25% | 116 | 3.87 | 1.5 | 36.8% | 100.0 |

Expert mirror seat rates: {'seat_0': 0.5, 'seat_1': 0.5} (seat fairness sanity), balance 99.9.

Reading guide: expert win % above fair share = the skill ceiling the ruleset supports beyond the baseline agent. Watch the mirror matchup for degeneracy signals (collapsed game length, exploding steal rate) — an exploit found by a stronger agent shows up there first.

## Reading of the results

**The expert's edge is small: ~+3 pp at 3p, nothing at 2p or 4p.** At 2p two of its three upgrades can't bind (denial discards need a takeable discard pile; easiest-spelling targeting rarely differs because valid_spellings are already sorted shortest-first), and value-maximizing completion choice only matters in the rare turns where multiple completions are simultaneously available.

**This is a finding about the RULESET, not just the agent: skill saturates at basic competence.** The huge skill step is random → competent (~83% win). Beyond that, deliberate sharper play buys almost nothing — outcomes between competent players are healthily luck-tempered, which is the right profile for a family/educational game (Sushi Go has the same shape) and softens the v8.10 concern about greedy and balanced collapsing into one tier: the gradient up there was always shallow.

**No exploit found.** The mirror matchup shows no degeneracy: game length (142 vs 144 turns), steal rate (1.56 vs 1.61), and seat fairness all match the balanced baseline. A deliberately ruthless policy playing the same rules produces the same game — good robustness evidence before printing.

**Where real headroom would be:** card counting (tracking what's left in the deck across recycles) and multi-turn planning — true search. That's a research project with diminishing returns for a tabletop game; not recommended unless a specific exploit hypothesis needs testing. The expert ships in AGENTS as the third tier regardless — it's never worse, and 3p playtests should prefer it.