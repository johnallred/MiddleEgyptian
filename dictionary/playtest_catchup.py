"""
2-player catch-up mechanic playtest (v8.9 candidates).

The composite balance score never measured leader-runaway. The metric that
does: **first-scorer-wins** — how often the seat that scores the game's
FIRST word goes on to win. A perfectly comeback-friendly game would sit
near 50% at 2p; a pure-runaway game near 100%.

Candidates (all table-trackable, no score arithmetic):

  baseline      — v8.8 production, no catch-up
  rebound1      — "scoring rebound": when your opponent scores a word, you
                  immediately draw 1 sign card (event-triggered)
  salve2        — "steal salve": when your word is stolen, draw 2 signs
  mulligan1     — "word mulligan": once per game, replace your active word
                  as a free action (draw-2-keep-1, old word to bottom)
  token         — "Eye of Horus": token moves to the OTHER player whenever
                  anyone scores; holder blind-draws 3-keep-1
  reb_mull      — rebound1 + mulligan1 (the predicted winning package)

Each candidate runs two 2p matchups:
  balanced vs balanced  — comeback metric (first-scorer-wins)
  greedy  vs balanced   — skill check (balanced's win rate must not
                          collapse toward 50%: catch-up must aid the
                          trailing player, not erase skill)

Usage:
  python3 playtest_catchup.py                     # all candidates + report
  python3 playtest_catchup.py --variant rebound1  # one candidate
"""

import argparse
import json
from pathlib import Path

import playtest_simulator as ps

RUNS_DIR = ps.OUT_DIR / "catchup_runs"
REPORT = ps.OUT_DIR / "CATCHUP_PLAYTEST_REPORT.md"

VARIANTS = ["baseline", "rebound1", "salve2", "mulligan1", "token", "reb_mull"]

LEVERS = {
    "baseline":  {},
    "rebound1":  {"score_rebound_draw": 1},
    "salve2":    {"steal_victim_draws": 2},
    "mulligan1": {"word_mulligan": 1},
    "token":     {"underdog_token": True},
    "reb_mull":  {"score_rebound_draw": 1, "word_mulligan": 1},
}


def run_matchup(agents, levers, games, seed, pools):
    sign_pool, word_pool, logo_pool = pools
    cfg = ps.GameConfig(
        n_players=2, agent_names=agents,
        starting_hand=8, hand_limit=12,
        points_to_win=8, max_turns=800,
        **levers)
    results = ps.run_batch(games, seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)
    scored = [r for r in results if r.first_scorer_seat >= 0]
    fsw = 100 * sum(r.first_scorer_won for r in scored) / max(1, len(scored))
    return {
        "agents": agents,
        "first_scorer_win_pct": round(fsw, 1),
        "agent_win_rates": stats["agent_win_rates"],
        "seat_win_rates": stats["seat_win_rates"],
        "balance": stats["balance_score"],
        "median_turns": stats["median_turns"],
        "steals_per_game": stats["avg_steals_per_game"],
        "logograms_per_game": stats["avg_logograms_per_game"],
        "mulligans_per_game": round(
            sum(r.mulligans_used for r in results) / len(results), 2),
    }


def run_variant(variant, games, seed):
    pools = ps.load_deck()
    out = {"variant": variant, "games": games, "seed": seed,
           "mirror": run_matchup(["balanced", "balanced"], LEVERS[variant],
                                 games, seed, pools),
           "skill": run_matchup(["greedy", "balanced"], LEVERS[variant],
                                games, seed, pools)}
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{variant}.json").write_text(json.dumps(out, indent=1))
    m, s = out["mirror"], out["skill"]
    print(f"  {variant}: first-scorer-wins={m['first_scorer_win_pct']}% "
          f"turns={m['median_turns']} "
          f"balanced-vs-greedy={s['agent_win_rates'].get('balanced')} "
          f"mulligans={m['mulligans_per_game']}")
    return out


def assemble_report(games, seed):
    runs = {v: json.loads((RUNS_DIR / f"{v}.json").read_text())
            for v in VARIANTS if (RUNS_DIR / f"{v}.json").exists()}
    md = ["# 2-Player Catch-Up Mechanic Playtest (v8.9 candidates)", ""]
    md.append(f"Core deck (v8.8 build), 2 players, target 8 points, "
              f"{games} games per matchup, seed {seed}, max 800 turns.")
    md.append("")
    md.append("**Metric.** `first-scorer-wins %` = how often the seat that "
              "scores the game's first word goes on to win. 50% = perfect "
              "comeback health; 100% = pure runaway. The composite balance "
              "score never measured this.")
    md.append("")
    md.append("All candidates are table-trackable by design: they trigger "
              "on events (a word was just scored / stolen) or use a physical "
              "token, never on score arithmetic like 'behind by 3+'.")
    md.append("")
    md.append("## Comeback health (balanced mirror)")
    md.append("")
    md.append("| Candidate | First-scorer wins | Median turns | Steals/g | "
              "Logograms/g | Mulligans/g |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        m = runs[v]["mirror"]
        md.append(f"| {v} | {m['first_scorer_win_pct']}% | "
                  f"{m['median_turns']} | {m['steals_per_game']} | "
                  f"{m['logograms_per_game']} | {m['mulligans_per_game']} |")
    md.append("")
    md.append("## Skill check (greedy vs balanced)")
    md.append("")
    md.append("Balanced should keep beating greedy by a similar margin — "
              "catch-up should rescue the *trailing* player, not the "
              "*weaker* one.")
    md.append("")
    md.append("| Candidate | Balanced win % | Greedy win % | "
              "First-scorer wins |")
    md.append("|---|---:|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        s = runs[v]["skill"]
        md.append(f"| {v} | {100*s['agent_win_rates'].get('balanced',0):.1f} | "
                  f"{100*s['agent_win_rates'].get('greedy',0):.1f} | "
                  f"{s['first_scorer_win_pct']}% |")
    md.append("")
    md.append("Levers: `score_rebound_draw`, `steal_victim_draws`, "
              "`word_mulligan`, `underdog_token` in "
              "`playtest_simulator.GameConfig` (all default off). "
              "First-scorer tracking is now a permanent GameRecord field.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="all")
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    targets = VARIANTS if args.variant == "all" else [args.variant]
    if not args.report:
        for v in targets:
            print(f"Running {v} ...")
            run_variant(v, args.games, args.seed)
    if args.variant == "all" or args.report:
        assemble_report(args.games, args.seed)


if __name__ == "__main__":
    main()
