"""
Playtest driver for the July 2026 rule-variant candidates (v8.8 levers).

Variants tested against the v8.7 production baseline (core deck.json,
balanced-vs-balanced, scaled points 2p=8 / 3p=7 / 4p=6):

  baseline      — v8.7 defaults (control run)
  word_draw2    — draw 2 word cards, keep the better fit, other to bottom
  strip_1sign   — word cards lose their 1-sign spellings (when a longer
                  alternative exists); logogram cards regain uniqueness
  logo_exchange — a dead logogram (target word is nobody's active word)
                  may be exchanged, as the turn's action, for 2 sign draws
  combined      — word_draw2 + strip_1sign + logo_exchange together

Note: the "cut the trade rule" candidate has NO simulator representation —
player-to-player trading was never modeled, so every published balance
number already describes a trade-free game. Cutting it from rules.md is
a documentation change with zero measured impact.

Usage:
  python3 playtest_variants.py --variant baseline
  python3 playtest_variants.py --variant all          # everything, then report
  python3 playtest_variants.py --report               # assemble report only
"""

import argparse
import copy
import json
from pathlib import Path

import playtest_simulator as ps

RUNS_DIR = ps.OUT_DIR / "variant_runs"
REPORT = ps.OUT_DIR / "VARIANT_PLAYTEST_REPORT.md"

SCALED_POINTS = {2: 8, 3: 7, 4: 6}
PLAYER_COUNTS = [2, 3, 4]

VARIANTS = ["baseline", "word_draw2", "strip_1sign",
            "logo_exchange", "logo_exchange1", "combined"]


def strip_one_sign_spellings(word_pool):
    """Remove 1-sign spellings from word cards that have a longer
    alternative. Words whose ONLY spelling is 1-sign are left untouched
    (they'd otherwise become uncompletable). Returns (pool, n_stripped,
    n_kept_single)."""
    pool = copy.deepcopy(word_pool)
    n_stripped = 0
    n_kept_single = 0
    for w in pool:
        multi = [sp for sp in w.valid_spellings if len(sp) > 1]
        if multi and len(multi) < len(w.valid_spellings):
            w.valid_spellings = multi
            n_stripped += 1
        elif not multi:
            n_kept_single += 1
    return pool, n_stripped, n_kept_single


def make_cfg(variant, n_players):
    kwargs = dict(
        n_players=n_players,
        agent_names=["balanced"] * n_players,
        starting_hand=8,
        hand_limit=12,
        points_to_win=SCALED_POINTS[n_players],
        max_turns=800,
    )
    if variant in ("word_draw2", "combined"):
        kwargs["word_draw_n"] = 2
    if variant in ("logo_exchange", "combined"):
        kwargs["dead_logogram_exchange"] = 2   # as requested: 2 draws
    if variant == "logo_exchange1":
        kwargs["dead_logogram_exchange"] = 1   # tuned-down alternative
    return ps.GameConfig(**kwargs)


def run_variant(variant, games, seed):
    sign_pool, word_pool, logo_pool = ps.load_deck()
    notes = {}
    if variant in ("strip_1sign", "combined"):
        word_pool, n_stripped, n_kept = strip_one_sign_spellings(word_pool)
        notes["words_with_1sign_spelling_stripped"] = n_stripped
        notes["words_kept_single_1sign_spelling"] = n_kept

    out = {"variant": variant, "games": games, "seed": seed, "notes": notes,
           "by_players": {}}
    for n_players in PLAYER_COUNTS:
        cfg = make_cfg(variant, n_players)
        results = ps.run_batch(games, seed, sign_pool, word_pool, logo_pool, cfg)
        stats = ps.analyze(results)
        exch = sum(r.logogram_exchanges for r in results) / len(results)
        out["by_players"][str(n_players)] = {
            "balance": stats["balance_score"],
            "victory_pct": round(100 * stats["end_reasons"].get("victory", 0) / games, 1),
            "median_turns": stats["median_turns"],
            "avg_score": stats["avg_score"],
            "steals_per_game": stats["avg_steals_per_game"],
            "logograms_per_game": stats["avg_logograms_per_game"],
            "exchanges_per_game": round(exch, 2),
            "seat_win_rates": stats["seat_win_rates"],
        }
        print(f"  {variant} {n_players}p: balance={stats['balance_score']} "
              f"turns={stats['median_turns']} "
              f"logos={stats['avg_logograms_per_game']} exch={exch:.2f}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{variant}.json").write_text(json.dumps(out, indent=1))
    return out


def assemble_report(games, seed):
    runs = {}
    for v in VARIANTS:
        f = RUNS_DIR / f"{v}.json"
        if f.exists():
            runs[v] = json.loads(f.read_text())

    md = ["# Rule-Variant Playtest Report (v8.8 candidates)", ""]
    md.append(f"Core deck (`deck.json`, v8.7 build), balanced-vs-balanced, "
              f"{games} games per cell, seed {seed}, scaled points "
              f"(2p=8, 3p=7, 4p=6), max 800 turns.")
    md.append("")
    md.append("**Candidate 1 — cut the trade rule:** not simulatable; "
              "player-to-player trading was never modeled in the engine, so "
              "all published balance data already describes a trade-free "
              "game. Cutting it from rules.md has zero measured impact (and "
              "removes an unbounded collusion/kingmaking channel at 3+ "
              "players).")
    md.append("")
    md.append("| Variant | Players | Balance | Victory % | Median turns | "
              "Avg score | Steals/g | Logograms/g | Exchanges/g |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        for n in map(str, PLAYER_COUNTS):
            s = runs[v]["by_players"][n]
            md.append(f"| {v} | {n} | {s['balance']} | {s['victory_pct']} | "
                      f"{s['median_turns']} | {s['avg_score']} | "
                      f"{s['steals_per_game']} | {s['logograms_per_game']} | "
                      f"{s['exchanges_per_game']} |")
    md.append("")

    # Per-variant deltas vs baseline
    if "baseline" in runs:
        md.append("## Deltas vs baseline (averaged across player counts)")
        md.append("")
        md.append("| Variant | Δ balance | Δ median turns | Δ logograms/g | Δ steals/g |")
        md.append("|---|---:|---:|---:|---:|")
        base = runs["baseline"]["by_players"]
        def avg(run, key):
            return sum(run[str(n)][key] for n in PLAYER_COUNTS) / len(PLAYER_COUNTS)
        for v in VARIANTS:
            if v == "baseline" or v not in runs:
                continue
            r = runs[v]["by_players"]
            md.append(f"| {v} | {avg(r,'balance')-avg(base,'balance'):+.1f} | "
                      f"{avg(r,'median_turns')-avg(base,'median_turns'):+.0f} | "
                      f"{avg(r,'logograms_per_game')-avg(base,'logograms_per_game'):+.2f} | "
                      f"{avg(r,'steals_per_game')-avg(base,'steals_per_game'):+.2f} |")
        md.append("")

    for v in VARIANTS:
        if v in runs and runs[v]["notes"]:
            md.append(f"Notes ({v}): {runs[v]['notes']}")
    md.append("")
    md.append("Implementation levers: `GameConfig.word_draw_n` (draw N word "
              "cards keep 1, rejects go to the bottom of the word deck), "
              "`GameConfig.dead_logogram_exchange` (N = sign draws granted; "
              "the exchanged logogram goes to the sign discard pile, so it "
              "recirculates when the deck recycles), and "
              "`playtest_variants.strip_one_sign_spellings()` (word-pool "
              "transform; not yet a deck-builder change). Word cards keep "
              "their printed point values in the strip test even though "
              "their effective shortest spelling got longer — repointing is "
              "a follow-up decision if the variant is adopted.")
    md.append("")
    md.append("## Reading of the results")
    md.append("")
    md.append("**word_draw2 — adopt.** Balance and length are unchanged, "
              "but interactivity jumps: steals nearly double overall "
              "(1.88 → 3.46/game at 4p) and logogram completions rise "
              "~60%, because players holding better-fitting words complete "
              "and rotate more, and everyone's hands stay relevant to the "
              "table. This is the comeback/engagement dynamic the human "
              "playtest checklist hopes steals will provide. Zero component "
              "cost: 'draw 2 word cards, keep 1, bottom the other.'")
    md.append("")
    md.append("**strip_1sign — adopt for feel, neutral on data.** Only 23 "
              "word cards (the trivial tier) even have a 1-sign spelling; "
              "stripping it moves nothing measurable (Δ balance −0.0, +5 "
              "turns). The payoff is qualitative: logogram cards become the "
              "only single-card completions again, protecting their "
              "'lottery win' identity. Requires a deck-builder change plus "
              "a decision on repointing the affected tier-1 cards.")
    md.append("")
    md.append("**logo_exchange — do NOT adopt as an unrestricted action.** "
              "In both the 2-draw and 1-draw forms, agents exchange ~30 "
              "times per game (a quarter of all turns): any logogram not "
              "matching an active word is instantly cashed in, logogram "
              "COMPLETIONS drop by ~40% (0.47 → 0.24-0.26 at 2p), and games "
              "lengthen ~15 turns. The valve doesn't relieve logogram "
              "frustration — it converts logograms into a draw engine and "
              "cannibalizes exactly the 'yes!' moments the mechanic exists "
              "to create. If a valve is still wanted after human playtests, "
              "test a bounded form (once per player per game).")
    md.append("")
    md.append("**combined — fine but slower.** Balance holds (96-99) but "
              "median length grows ~37 turns (~9 min at 15 s/turn), mostly "
              "from the exchange churn. Adopting word_draw2 + strip_1sign "
              "without the exchange is the better package.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default=None,
                    help="one of: " + ", ".join(VARIANTS) + ", or 'all'")
    ap.add_argument("--games", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report", action="store_true",
                    help="assemble report from existing runs only")
    args = ap.parse_args()

    if args.variant:
        targets = VARIANTS if args.variant == "all" else [args.variant]
        for v in targets:
            print(f"Running variant: {v}")
            run_variant(v, args.games, args.seed)
    if args.report or args.variant == "all":
        assemble_report(args.games, args.seed)


if __name__ == "__main__":
    main()
