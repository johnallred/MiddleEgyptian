"""
Co-op / Solo Mode playtest (v9 structural candidate).

Design under test:

  All players are ONE TEAM (works at 1 player = solo). Classic v8.10
  mechanics are unchanged — market, draw-2-keep-1, recycle, word
  draw-2-keep-1, mulligan — except:

  * The team wins the moment the TEAM TOTAL reaches the target score.
  * "Steals" become ASSISTS: completing a teammate's word scores for
    the team exactly the same (the engine path is identical).
  * The loss clock: the sign deck may only be dealt through TWICE
    (one reshuffle of the discard). When it dies, everyone gets one
    last dry turn, then the game ends — if the target wasn't reached,
    the team loses.

Method: agents aren't target-aware, so one batch per player count with
an unreachable target measures the natural distribution of team score
at deck death; the win rate for ANY target T is then P(final >= T).
One run yields the whole difficulty curve, from which we recommend
printed difficulty tiers (~90% / ~60% / ~30% win rates).

Usage:
  python3 playtest_coop.py --players 1        # one player count
  python3 playtest_coop.py --players all      # everything + report
  python3 playtest_coop.py --report
"""

import argparse
import json
import statistics
from pathlib import Path

import playtest_simulator as ps

RUNS_DIR = ps.OUT_DIR / "coop_runs"
REPORT = ps.OUT_DIR / "COOP_MODE_PLAYTEST_REPORT.md"

PLAYER_COUNTS = [1, 2, 3, 4]
UNREACHABLE = 10 ** 9


def run_count(n_players, games, seed, agent="balanced"):
    sign_pool, word_pool, logo_pool = ps.load_deck()
    cfg = ps.GameConfig(
        n_players=n_players, agent_names=[agent] * n_players,
        starting_hand=8, hand_limit=12,
        points_to_win=UNREACHABLE, max_turns=5000,
        coop_mode=True, coop_sign_deck_passes=2)
    results = ps.run_batch(games, seed, sign_pool, word_pool, logo_pool, cfg)
    finals = [sum(r.final_scores) for r in results]
    words = [len(r.completed_word_cards) for r in results]
    return {
        "n_players": n_players, "agent": agent, "games": games,
        "final_scores": finals,
        "score_mean": round(statistics.mean(finals), 1),
        "score_median": statistics.median(finals),
        "score_min": min(finals), "score_max": max(finals),
        "words_mean": round(statistics.mean(words), 1),
        "turns_median": statistics.median(r.turns for r in results),
        "mulligans_mean": round(statistics.mean(r.mulligans_used
                                                for r in results), 2),
        "logos_mean": round(statistics.mean(r.logograms_played
                                            for r in results), 2),
    }


def pct_at_least(finals, t):
    return round(100 * sum(1 for s in finals if s >= t) / len(finals), 1)


def tier_target(finals, want_win_pct):
    """Largest target whose win rate is still >= want_win_pct."""
    best = 1
    for t in range(1, max(finals) + 1):
        if pct_at_least(finals, t) >= want_win_pct:
            best = t
    return best


def run_all(games, seed):
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    for n in PLAYER_COUNTS:
        out = run_count(n, games, seed)
        (RUNS_DIR / f"coop_{n}p.json").write_text(json.dumps(out, indent=1))
        print(f"  {n}p: score median={out['score_median']} "
              f"range=[{out['score_min']},{out['score_max']}] "
              f"words={out['words_mean']} turns={out['turns_median']}")
    # random-agent sanity at solo + 2p
    for n in (1, 2):
        out = run_count(n, games, seed, agent="random")
        (RUNS_DIR / f"coop_{n}p_random.json").write_text(
            json.dumps(out, indent=1))
        print(f"  {n}p random: score median={out['score_median']}")


def assemble_report(games, seed):
    runs = {}
    for f in RUNS_DIR.glob("coop_*.json"):
        runs[f.stem] = json.loads(f.read_text())
    md = ["# Co-op / Solo Mode Playtest", ""]
    md.append(f"Core deck (v8.10 build), classic mechanics, team scoring, "
              f"sign deck limited to 2 passes (one reshuffle), one dry "
              f"round of grace at deck death. {games} games per cell, seed "
              f"{seed}, balanced agents unless noted. Win rate for a "
              f"target T = share of games whose team total at deck death "
              f"reached T (exact, since agents are not target-aware).")
    md.append("")
    md.append("## Team score at deck death (the whole difficulty curve)")
    md.append("")
    md.append("| Players | Median score | Range | Words/game | "
              "Median turns | Mulligans/g | Logograms/g |")
    md.append("|---:|---:|---|---:|---:|---:|---:|")
    for n in PLAYER_COUNTS:
        r = runs.get(f"coop_{n}p")
        if not r:
            continue
        md.append(f"| {n} | {r['score_median']} | "
                  f"[{r['score_min']}, {r['score_max']}] | "
                  f"{r['words_mean']} | {r['turns_median']} | "
                  f"{r['mulligans_mean']} | {r['logos_mean']} |")
    md.append("")
    md.append("## Win rate by target")
    md.append("")
    header = "| Target | " + " | ".join(f"{n}p" for n in PLAYER_COUNTS
                                        if f"coop_{n}p" in runs) + " |"
    md.append(header)
    md.append("|" + "---:|" * (header.count("|") - 1))
    all_finals = [runs[f"coop_{n}p"]["final_scores"]
                  for n in PLAYER_COUNTS if f"coop_{n}p" in runs]
    max_t = max(max(f) for f in all_finals)
    targets = [t for t in range(5, max_t + 1, 5)]
    for t in targets:
        row = f"| {t} | " + " | ".join(
            f"{pct_at_least(f, t)}%" for f in all_finals) + " |"
        md.append(row)
    md.append("")
    md.append("## Recommended printed difficulty tiers")
    md.append("")
    md.append("Chosen as the largest target still winning at roughly "
              "90% (Apprentice), 60% (Scribe), and 30% (Master Scribe):")
    md.append("")
    md.append("| Players | Apprentice (~90%) | Scribe (~60%) | "
              "Master Scribe (~30%) |")
    md.append("|---:|---:|---:|---:|")
    for n in PLAYER_COUNTS:
        r = runs.get(f"coop_{n}p")
        if not r:
            continue
        f = r["final_scores"]
        md.append(f"| {n} | {tier_target(f, 90)} | {tier_target(f, 60)} | "
                  f"{tier_target(f, 30)} |")
    md.append("")
    md.append("## Random-agent sanity check")
    md.append("")
    for key in ("coop_1p_random", "coop_2p_random"):
        r = runs.get(key)
        if r:
            md.append(f"- {r['n_players']}p random agents: median team "
                      f"score {r['score_median']} "
                      f"(range [{r['score_min']}, {r['score_max']}]) — "
                      f"skill should and does matter.")
    md.append("")
    md.append("## Caveats")
    md.append("")
    md.append("Agents are not clock-aware: they recycle (discard 2 / draw "
              "2) on idle turns even when the deck is nearly dead, where a "
              "human team would hoard. Real teams should therefore score "
              "somewhat HIGHER than these curves late in the deck, making "
              "the printed tiers slightly easier than measured — the right "
              "direction to err for a co-op. Table talk and coordinated "
              "assists (trading completions) are also unmodeled upside. "
              "Engine levers: `GameConfig.coop_mode`, "
              "`GameConfig.coop_sign_deck_passes`.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", default=None,
                    help="1|2|3|4|all (all also writes the report)")
    ap.add_argument("--games", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.players == "all":
        run_all(args.games, args.seed)
        assemble_report(args.games, args.seed)
        return
    if args.players:
        n = int(args.players)
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        out = run_count(n, args.games, args.seed)
        (RUNS_DIR / f"coop_{n}p.json").write_text(json.dumps(out, indent=1))
        print(f"  {n}p: median={out['score_median']} "
              f"range=[{out['score_min']},{out['score_max']}] "
              f"turns={out['turns_median']}")
    if args.report:
        assemble_report(args.games, args.seed)


if __name__ == "__main__":
    main()
