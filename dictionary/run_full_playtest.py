"""
Runs the full playtest suite: 5 agent matchups x N games each, then writes
a consolidated balance report to game_material/playtest_results/.

Usage:
  python3 run_full_playtest.py                  # default 2000 games per matchup
  python3 run_full_playtest.py --games 5000     # bigger
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import playtest_simulator as ps

OUT_DIR = ps.OUT_DIR


MATCHUPS_2P = [
    ("random", "random"),
    ("greedy", "greedy"),
    ("balanced", "balanced"),
    ("random", "balanced"),
    ("greedy", "balanced"),
]
# For 3+ players, just same-agent matchups to keep total runs manageable.
MATCHUPS_NP = [
    ("random",),
    ("greedy",),
    ("balanced",),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=1000)
    parser.add_argument("--max-turns", type=int, default=1500)
    parser.add_argument("--points-to-win", type=int, default=None,
                        help="Flat points target for ALL player counts. "
                             "Default: v8.6 per-player-count scaling "
                             "(2p=8, 3p=7, 4p=6).")
    parser.add_argument("--player-counts", type=str, default="2",
                        help="Comma-separated player counts to test")
    args = parser.parse_args()

    player_counts = [int(p) for p in args.player_counts.split(",")]

    # v8.6: points-to-win scales with player count unless overridden.
    SCALED_POINTS = {2: 8, 3: 7, 4: 6}

    def target_points(n_players: int) -> int:
        if args.points_to_win is not None:
            return args.points_to_win
        return SCALED_POINTS.get(n_players, 7)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sign_pool, word_pool, logo_pool = ps.load_deck()

    all_stats = {}  # key: (n_players, matchup_name) -> stats
    for n_players in player_counts:
        matchups = MATCHUPS_2P if n_players == 2 else MATCHUPS_NP
        for agents in matchups:
            # Replicate the agent for n_players seats
            agent_list = list(agents) if len(agents) == n_players else \
                         [agents[0]] * n_players if len(agents) == 1 else \
                         (list(agents) + [agents[-1]] * (n_players - len(agents)))[:n_players]
            name = "_vs_".join(agent_list)
            cfg = ps.GameConfig(
                n_players=n_players,
                agent_names=agent_list,
                starting_hand=8,
                hand_limit=12,
                points_to_win=target_points(n_players),
                max_turns=args.max_turns,
            )
            print(f"\nRunning {n_players}p {name} ({args.games} games)...")
            results = ps.run_batch(args.games, args.seed, sign_pool, word_pool, logo_pool, cfg)
            stats = ps.analyze(results)
            per_matchup_path = OUT_DIR / f"matchup_{n_players}p_{name}.md"
            ps.write_report(stats, cfg, per_matchup_path)
            all_stats[(n_players, name)] = stats
            print(f"  balance={stats['balance_score']}  "
                  f"victories={stats['end_reasons'].get('victory',0)}/{args.games}  "
                  f"agent_rates={stats['agent_win_rates']}")

    # Consolidated cross-matchup report
    md = ["# Hieroglyph Quest — Master Balance Report", ""]
    target_desc = (f"{args.points_to_win} points (flat)" if args.points_to_win is not None
                   else "v8.6 scaled points (" +
                        ", ".join(f"{n}p={target_points(n)}" for n in player_counts) + ")")
    md.append(f"Player counts tested: {player_counts}. {args.games:,} games per matchup, "
              f"seed {args.seed}, target {target_desc}, "
              f"max {args.max_turns} turns. Ruleset v8.10 "
              f"(multiset spelling match, market 5, sign draw-2-keep-1, "
              f"WORD draw-2-keep-1, 1-sign spellings stripped from word cards, "
              f"word mulligan once per player per game, recycle (discard 2 draw 2) printed, look-and-take removed, "
              f"discard-take at 3p+, equal-turns endgame, no first-player gift).")
    md.append("")
    md.append("## Matchup summary (by player count)")
    md.append("")
    md.append("| Players | Matchup | Balance | Victories | Median turns | Avg score | Steals/game | Logograms/game | First-scorer wins | Mulligans/game |")
    md.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for (n_players, name), s in sorted(all_stats.items()):
        victories = s['end_reasons'].get('victory', 0)
        fsw = s.get('first_scorer_win_rate')
        fsw_str = f"{100*fsw:.0f}%" if fsw is not None else "—"
        md.append(f"| {n_players} | {name.replace('_vs_', ' vs ')} | {s['balance_score']} | "
                  f"{victories}/{args.games} ({100*victories/args.games:.0f}%) | "
                  f"{s['median_turns']} | {s['avg_score']} | {s['avg_steals_per_game']} | "
                  f"{s['avg_logograms_per_game']} | {fsw_str} | "
                  f"{s.get('avg_mulligans_per_game', 0)} |")
    md.append("")

    # Cross-matchup findings
    md.append("## Seat advantage by matchup (target = 1/N per seat)")
    md.append("")
    md.append("| Players | Matchup | Seat rates | Max deviation |")
    md.append("|---:|---|---|---:|")
    for (n_players, name), s in sorted(all_stats.items()):
        target = 1.0 / n_players
        rates = [s['seat_win_rates'][f'seat_{i}'] for i in range(n_players)]
        rate_str = " / ".join(f"{r*100:.1f}%" for r in rates)
        max_dev = max(abs(r - target) for r in rates)
        md.append(f"| {n_players} | {name.replace('_vs_', ' vs ')} | "
                  f"{rate_str} | {max_dev*100:+.1f}% |")
    md.append("")

    # Agent skill ordering
    md.append("### Agent skill ordering")
    md.append("")
    md.append("Where the same agent appears in mixed matchups, its win rate:")
    md.append("")
    agent_summary = {}
    for (n_players, name), s in all_stats.items():
        for agent, rate in s['agent_win_rates'].items():
            agent_summary.setdefault(agent, []).append((n_players, name, rate))
    md.append("| Agent | Players | Matchup | Win rate |")
    md.append("|---|---:|---|---:|")
    for agent in ("random", "greedy", "balanced"):
        for n_players, matchup, rate in sorted(agent_summary.get(agent, []),
                                                 key=lambda x: -x[2]):
            md.append(f"| {agent} | {n_players} | {matchup.replace('_vs_', ' vs ')} | "
                      f"{rate*100:.1f}% |")
    md.append("")

    # Most-completed word cards (aggregated across matchups)
    word_total = Counter()
    for key, s in all_stats.items():
        for w, n in s['top_completed_words']:
            word_total[w] += n
    md.append("## Top 20 most-completed word cards (across all matchups)")
    md.append("")
    md.append("| Word | Total completions |")
    md.append("|---|---:|")
    for w, n in word_total.most_common(20):
        md.append(f"| `{w}` | {n} |")
    md.append("")

    # Words never completed — dead cards in the starter deck
    word_pool_translits = {c['transliteration']
                            for c in json.load(open(ps.DECK_PATH))['word_deck']}
    completed_translits = set(word_total.keys())
    never_completed = word_pool_translits - completed_translits
    md.append(f"## Dead cards: word cards never completed in {len(all_stats) * args.games:,} games")
    md.append("")
    md.append(f"**{len(never_completed)} of {len(word_pool_translits)} word cards** "
              f"({100*len(never_completed)/len(word_pool_translits):.1f}%) never got completed.")
    md.append("")
    md.append("These cards never made it to a score pile. They may be too hard "
              "(too many required signs, or signs not stocked in the sign deck), "
              "wrongly tier-graded, or simply unlucky.")
    md.append("")
    if never_completed:
        md.append("First 30 (sample):")
        md.append("")
        md.append("```")
        for w in sorted(never_completed)[:30]:
            md.append(w)
        md.append("```")
    md.append("")

    # Broken openers across matchups
    md.append("## Broken openers across all matchups")
    md.append("")
    md.append("Opening hands that won >=70% of the time in at least 3 games. "
              "Listed per matchup so you can reproduce by seeding.")
    md.append("")
    for key, s in all_stats.items():
        n_players, name = key
        ops = s['broken_openers']
        if not ops:
            continue
        md.append(f"### {n_players}p {name.replace('_vs_', ' vs ')}")
        md.append("")
        md.append("| Opening signs (first 7) | Games | Win rate |")
        md.append("|---|---:|---:|")
        for op in ops[:8]:
            signs_text = " ".join(op["opening_signs"])
            md.append(f"| `{signs_text}` | {op['games_observed']} | {op['win_rate']*100:.1f}% |")
        md.append("")

    # Consolidated recommendations
    md.append("## Recommendations")
    md.append("")
    bal_avg = sum(s['balance_score'] for s in all_stats.values()) / len(all_stats)
    md.append(f"**Average balance score across matchups: {bal_avg:.1f}/100**.")
    md.append("")
    recs = []

    # Stalemate rate
    avg_stalemate = sum(s['end_reasons'].get('turn_limit', 0)
                        for s in all_stats.values()) / (args.games * len(all_stats))
    if avg_stalemate > 0.4:
        recs.append(f"- **{avg_stalemate*100:.0f}% of games hit turn limit** without "
                    f"a victor reaching {args.points_to_win} points. The game is "
                    f"completion-starved. Try one or more of: bigger starting hand "
                    f"(currently 8), bigger hand limit (currently 12), lower "
                    f"points_to_win, more copies of common biliterals in the sign "
                    f"deck, or a 'discard hand and redraw' option for stuck players.")

    # Logogram usage
    avg_logo = sum(s['avg_logograms_per_game'] for s in all_stats.values()) / len(all_stats)
    if avg_logo < 0.1:
        recs.append("- **Logograms basically never get played** (<0.1/game). The 30% "
                    "deal-rate at game start means most games have no logogram in play, "
                    "and even when one exists the player rarely draws the matching "
                    "word card. Consider drawing one logogram per N turns, or letting "
                    "players draw a logogram in lieu of a sign card sometimes.")

    # Steal rate
    avg_steal = sum(s['avg_steals_per_game'] for s in all_stats.values()) / len(all_stats)
    if avg_steal < 0.1:
        recs.append("- **Steals are vanishingly rare** (<0.1/game). The mechanic "
                    "requires having all opponent's word signs in hand simultaneously, "
                    "which is much harder than completing one's own. Consider "
                    "allowing partial-completion build-up that opponents can finish, "
                    "or making steal_value > own_value irrelevant (always allow).")

    # Seat fairness (now per player-count: target = 1/n_players)
    seat_devs = []
    for (n_players, name), s in all_stats.items():
        target = 1.0 / n_players
        rates = [s['seat_win_rates'][f'seat_{i}'] for i in range(n_players)]
        seat_devs.append(max(abs(r - target) for r in rates))
    max_seat_dev = max(seat_devs) if seat_devs else 0
    if max_seat_dev > 0.05:
        recs.append(f"- **Seat advantage detected** (up to {max_seat_dev*100:.1f}% from "
                    f"the per-seat target). Consider seat-position compensation.")

    # Agent skill ordering
    if 'balanced' in agent_summary and 'random' in agent_summary:
        bal_rate = max((r for _, _, r in agent_summary['balanced']))
        rand_rate = max((r for _, _, r in agent_summary['random']))
        if bal_rate < rand_rate + 0.05:
            recs.append("- **Strategic agents barely beat random**. The game has too "
                        "little decision space — outcomes are mostly luck of the draw. "
                        "Consider mechanics that reward planning: trading cards, "
                        "look-at-deck powers, or strategic discard rules.")

    if not recs:
        recs.append("- Game looks reasonably balanced. Continue with human playtests.")

    for r in recs:
        md.append(r)
    md.append("")

    md.append("## Reproducibility")
    md.append("")
    md.append(f"Every result here is reproducible. Base seed: `{args.seed}`. "
              f"Each individual game uses `seed = base_seed + game_index`. "
              f"To replay a specific game, run:")
    md.append("")
    md.append("```bash")
    md.append(f"python3 playtest_simulator.py --games 1 --seed {args.seed} "
              f"--agents balanced,balanced --out single_game.md")
    md.append("```")

    out_path = OUT_DIR / "MASTER_BALANCE_REPORT.md"
    out_path.write_text("\n".join(md))
    print(f"\nMaster report: {out_path}")


if __name__ == "__main__":
    main()
