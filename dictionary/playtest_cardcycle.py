"""
Rules-fidelity playtest: the two UNDOCUMENTED card-cycle actions.

The engine's agents have always been allowed two actions that the
printed rules.md never grants:

  trash_and_draw  (v2) — discard 2 useless signs, draw 2 fresh
  look_and_take   (v3) — peek top 3 of the deck, take 1, discard 1

Both default ON, so every published balance number assumes players can
cycle dead cards in ways the rulebook doesn't allow. This driver
measures what the PRINTED game actually plays like, to decide whether
to (a) turn the engine actions off and re-baseline, or (b) print a
trash rule.

Variants (classic v8.9 mode, core deck):
  baseline — both on (all published numbers)
  no_trash — trash_and_draw off, look_and_take on
  no_look  — trash_and_draw on, look_and_take off
  printed  — both off: the game as the rulebook actually reads

Matchups per variant: balanced mirror at 2p/3p/4p (scaled points),
plus greedy-vs-balanced at 2p as the skill check.

Usage:
  python3 playtest_cardcycle.py --variant printed
  python3 playtest_cardcycle.py --variant all
  python3 playtest_cardcycle.py --report
"""

import argparse
import json
from pathlib import Path

import playtest_simulator as ps

RUNS_DIR = ps.OUT_DIR / "cardcycle_runs"
REPORT = ps.OUT_DIR / "CARD_CYCLE_PLAYTEST_REPORT.md"

SCALED_POINTS = {2: 8, 3: 7, 4: 6}
VARIANTS = ["baseline", "no_trash", "no_look", "printed"]
FLAGS = {
    "baseline": {"allow_trash_and_draw": True,  "allow_look_and_take": True},
    "no_trash": {"allow_trash_and_draw": False, "allow_look_and_take": True},
    "no_look":  {"allow_trash_and_draw": True,  "allow_look_and_take": False},
    "printed":  {"allow_trash_and_draw": False, "allow_look_and_take": False},
}


def run_matchup(agents, n_players, flags, games, seed, pools):
    sign_pool, word_pool, logo_pool = pools
    cfg = ps.GameConfig(
        n_players=n_players, agent_names=agents,
        starting_hand=8, hand_limit=12,
        points_to_win=SCALED_POINTS[n_players], max_turns=800, **flags)
    results = ps.run_batch(games, seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)
    return {
        "first_scorer_win_pct": (round(100 * stats["first_scorer_win_rate"], 1)
                                 if stats["first_scorer_win_rate"] is not None
                                 else None),
        "agent_win_rates": stats["agent_win_rates"],
        "balance": stats["balance_score"],
        "victory_pct": round(100 * stats["end_reasons"].get("victory", 0) / games, 1),
        "end_reasons": stats["end_reasons"],
        "median_turns": stats["median_turns"],
        "avg_score": stats["avg_score"],
        "steals_per_game": stats["avg_steals_per_game"],
        "logograms_per_game": stats["avg_logograms_per_game"],
        "trash_per_game": stats["avg_trash_actions_per_game"],
        "mulligans_per_game": stats["avg_mulligans_per_game"],
    }


def run_variant(variant, games, seed):
    pools = ps.load_deck()
    flags = FLAGS[variant]
    out = {"variant": variant, "games": games, "seed": seed,
           "mirror": {}, "skill": None}
    for np_ in (2, 3, 4):
        out["mirror"][str(np_)] = run_matchup(
            ["balanced"] * np_, np_, flags, games, seed, pools)
        m = out["mirror"][str(np_)]
        print(f"  {variant} {np_}p: victory={m['victory_pct']}% "
              f"turns={m['median_turns']} fsw={m['first_scorer_win_pct']}% "
              f"trash={m['trash_per_game']}")
    out["skill"] = run_matchup(["greedy", "balanced"], 2, flags, games,
                               seed, pools)
    print(f"  {variant} skill: balanced="
          f"{out['skill']['agent_win_rates'].get('balanced')}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{variant}.json").write_text(json.dumps(out, indent=1))
    return out


def assemble_report(games, seed):
    runs = {v: json.loads((RUNS_DIR / f"{v}.json").read_text())
            for v in VARIANTS if (RUNS_DIR / f"{v}.json").exists()}
    md = ["# Card-Cycle Actions Playtest (rules-fidelity check)", ""]
    md.append(f"Core deck (v8.9 build), classic mode, {games} games per "
              f"cell, seed {seed}, scaled points (2p=8, 3p=7, 4p=6), max "
              f"800 turns.")
    md.append("")
    md.append("The engine has always granted agents two actions the printed "
              "rules never mention: `trash_and_draw` (discard 2 useless "
              "signs, draw 2) and `look_and_take` (peek top 3, take 1, "
              "discard 1). `printed` below is the game exactly as rules.md "
              "reads.")
    md.append("")
    md.append("## Balanced mirror by player count")
    md.append("")
    md.append("| Variant | Players | Victory % | Median turns | "
              "First-scorer wins | Steals/g | Logograms/g | Trash/g | "
              "Mulligans/g |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        for np_ in ("2", "3", "4"):
            m = runs[v]["mirror"][np_]
            md.append(f"| {v} | {np_} | {m['victory_pct']} | "
                      f"{m['median_turns']} | {m['first_scorer_win_pct']}% | "
                      f"{m['steals_per_game']} | {m['logograms_per_game']} | "
                      f"{m['trash_per_game']} | {m['mulligans_per_game']} |")
    md.append("")
    md.append("## Skill check (greedy vs balanced, 2p)")
    md.append("")
    md.append("| Variant | Balanced win % | Greedy win % |")
    md.append("|---|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        s = runs[v]["skill"]
        md.append(f"| {v} | {100*s['agent_win_rates'].get('balanced',0):.1f} | "
                  f"{100*s['agent_win_rates'].get('greedy',0):.1f} |")
    md.append("")
    md.append("Levers: `GameConfig.allow_trash_and_draw`, "
              "`GameConfig.allow_look_and_take`.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default=None)
    ap.add_argument("--games", type=int, default=300)
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
