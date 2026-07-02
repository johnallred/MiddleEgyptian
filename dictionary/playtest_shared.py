"""
Shared word pool playtest ("race, not theft" — v9 structural candidate).

Instead of personal active words, N word cards sit face-up in a shared
center row; on your turn you may complete ANY of them from hand. The row
refills after each completion. Steals and the word mulligan don't exist
in this mode — interaction comes from racing (and, for humans, denial).

Variants:
  classic   — v8.9 production baseline (personal words, steals, mulligan)
  shared4 / shared5 / shared6 — center row of 4 / 5 / 6 word cards

Matchups per variant:
  balanced mirror at 2p / 3p / 4p (scaled points 8/7/6)
  random vs balanced at 2p — skill check. NOTE: greedy and balanced
  collapse to the same policy in shared mode (no look_and_take, no
  steal decisions), so random-vs-balanced is the meaningful skill gap.

Simulator caveat to keep in mind when reading results: agents RACE but
do not model DENIAL (completing a word cheaply just because an opponent
is about to take it). Human play should show more interaction than
these numbers do, not less.

Usage:
  python3 playtest_shared.py --variant classic
  python3 playtest_shared.py --variant all
  python3 playtest_shared.py --report
"""

import argparse
import json
from pathlib import Path

import playtest_simulator as ps

RUNS_DIR = ps.OUT_DIR / "shared_pool_runs"
REPORT = ps.OUT_DIR / "SHARED_POOL_PLAYTEST_REPORT.md"

SCALED_POINTS = {2: 8, 3: 7, 4: 6}
VARIANTS = ["classic", "shared4", "shared5", "shared6",
            "shared5_dredge"]
POOL = {"classic": 0, "shared4": 4, "shared5": 5, "shared6": 6,
        "shared5_dredge": 5}
DREDGE = {"shared5_dredge"}


def run_matchup(agents, n_players, pool_size, games, seed, pools, dredge=False):
    sign_pool, word_pool, logo_pool = pools
    cfg = ps.GameConfig(
        n_players=n_players, agent_names=agents,
        starting_hand=8, hand_limit=12,
        points_to_win=SCALED_POINTS[n_players], max_turns=800,
        shared_word_pool=pool_size, shared_dredge=dredge)
    results = ps.run_batch(games, seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)
    return {
        "agents": agents,
        "first_scorer_win_pct": (round(100 * stats["first_scorer_win_rate"], 1)
                                 if stats["first_scorer_win_rate"] is not None
                                 else None),
        "agent_win_rates": stats["agent_win_rates"],
        "balance": stats["balance_score"],
        "victory_pct": round(100 * stats["end_reasons"].get("victory", 0) / games, 1),
        "median_turns": stats["median_turns"],
        "avg_score": stats["avg_score"],
        "logograms_per_game": stats["avg_logograms_per_game"],
        "steals_per_game": stats["avg_steals_per_game"],
        "trash_per_game": stats["avg_trash_actions_per_game"],
    }


def run_variant(variant, games, seed):
    pools = ps.load_deck()
    n = POOL[variant]
    out = {"variant": variant, "pool_size": n, "games": games, "seed": seed,
           "mirror": {}, "skill": None}
    dredge = variant in DREDGE
    for np_ in (2, 3, 4):
        out["mirror"][str(np_)] = run_matchup(
            ["balanced"] * np_, np_, n, games, seed, pools, dredge=dredge)
        m = out["mirror"][str(np_)]
        print(f"  {variant} {np_}p: fsw={m['first_scorer_win_pct']}% "
              f"turns={m['median_turns']} logos={m['logograms_per_game']} "
              f"steals={m['steals_per_game']}")
    out["skill"] = run_matchup(["random", "balanced"], 2, n, games, seed,
                               pools, dredge=dredge)
    print(f"  {variant} skill: balanced="
          f"{out['skill']['agent_win_rates'].get('balanced')}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{variant}.json").write_text(json.dumps(out, indent=1))
    return out


def assemble_report(games, seed):
    runs = {v: json.loads((RUNS_DIR / f"{v}.json").read_text())
            for v in VARIANTS if (RUNS_DIR / f"{v}.json").exists()}
    md = ["# Shared Word Pool Playtest (race, not theft)", ""]
    md.append(f"Core deck (v8.9 build), {games} games per cell, seed {seed}, "
              f"scaled points (2p=8, 3p=7, 4p=6), max 800 turns. "
              f"`shared_word_pool` lever in GameConfig; classic = 0.")
    md.append("")
    md.append("In shared mode there are no personal words, no steals, and no "
              "word mulligan; a face-up row of N word cards is open to "
              "everyone and refills after each completion.")
    md.append("")
    md.append("## Balanced mirror by player count")
    md.append("")
    md.append("| Variant | Players | First-scorer wins | Median turns | "
              "Victory % | Avg score | Logograms/g | Steals/g | Trash/g |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        for np_ in ("2", "3", "4"):
            m = runs[v]["mirror"][np_]
            md.append(f"| {v} | {np_} | {m['first_scorer_win_pct']}% | "
                      f"{m['median_turns']} | {m['victory_pct']} | "
                      f"{m['avg_score']} | {m['logograms_per_game']} | "
                      f"{m['steals_per_game']} | {m['trash_per_game']} |")
    md.append("")
    md.append("## Skill check (random vs balanced, 2p)")
    md.append("")
    md.append("Greedy and balanced collapse to the same policy in shared "
              "mode, so random-vs-balanced is the meaningful gap. Classic "
              "shows the same matchup for comparison.")
    md.append("")
    md.append("| Variant | Balanced win % | First-scorer wins |")
    md.append("|---|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        s = runs[v]["skill"]
        md.append(f"| {v} | {100*s['agent_win_rates'].get('balanced',0):.1f} | "
                  f"{s['first_scorer_win_pct']}% |")
    md.append("")
    md.append("## Reading of the results")
    md.append("")
    md.append("**1. The naked shared pool stalls at 2 players.** With no way "
              "to cycle the row, both players clear the easy words and then "
              "sit staring at 4-6 leftovers nobody can build: shared4's 2p "
              "median hit the 800-turn cap; shared5 ran 464 turns vs "
              "classic's 140. Smaller rows stall harder (fewer outs). 3p/4p "
              "churn the row naturally and play at classic speed.")
    md.append("")
    md.append("**2. Dredge is mandatory.** Adding 'spend your action to "
              "bottom one row card and refill' (shared5_dredge) cuts the 2p "
              "median from 464 to 188 turns, doubles logogram fire rate "
              "(dredging surfaces targets), and restores the skill gap "
              "(balanced-vs-random 74% → 83%, near classic's 86%). Any "
              "table version of Race Mode must include it.")
    md.append("")
    md.append("**3. Even with dredge, shared mode doesn't beat classic on "
              "any measured axis.** 2p games run ~35% longer (188 vs 140), "
              "3p comeback health is worse (first-scorer-wins 54% vs 44%), "
              "and skill expression is a touch lower. Its genuine advantages "
              "are exactly the ones the simulator can't see: no steal "
              "social friction, no personal-word frustration, fully visible "
              "shared state. Note that classic v8.9 already fixed 'blind "
              "word assignment' (word draw-2-keep-1 + mulligan), so shared "
              "mode's original selling points have partly been absorbed.")
    md.append("")
    md.append("**Recommendation:** ship as an optional 'Race Mode' variant "
              "(row of 5, dredge included, no steals/mulligan) rather than "
              "replacing the classic rules. It costs zero new components and "
              "gives steal-averse tables an official way to play; the tuned "
              "classic game remains the default. If human playtests show "
              "the steal mechanic consistently souring tables, revisit "
              "promotion of Race Mode with a 2p target-point retune.")
    md.append("")
    md.append("## Caveats the numbers can't see")
    md.append("")
    md.append("Agents race but do not model **denial** (grabbing a word "
              "specifically because an opponent is close to it), **table "
              "talk**, or the reading load of a 4-6 card open row for "
              "players still learning the signs. Human playtests should "
              "weight those; the simulator's job here is speed, balance, "
              "comeback health, and degenerate-loop detection only.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default=None)
    ap.add_argument("--games", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.variant:
        targets = VARIANTS if args.variant == "all" else [args.variant]
        for v in targets:
            print(f"Running {v} ...")
            run_variant(v, args.games, args.seed)
    if args.report or args.variant == "all":
        assemble_report(args.games, args.seed)


if __name__ == "__main__":
    main()
