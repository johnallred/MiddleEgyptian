"""
Playtest every expansion deck in game_material/expansions/ at 2/3/4 player
counts with the balanced agent. Produces a consolidated balance report.

Under the v2 signs-in-base architecture (PROJECT_GUIDE §20), each themed
expansion's gameplay sign pool comes from base_sign_library.json, NOT from
the expansion's own embedded sign_deck. This is the production
configuration: one shared base library, themed expansions ship words +
logograms only. Each test deck is synthesized by combining the expansion's
word/logogram cards with the base library's sign cards before swapping
into deck.json.

Special case: after_dark.json uses base library PLUS its expansion-specific
family-blocked signs (D27, D52, etc.), reflecting its production design
(base library + small adult sign supplement shipped with the 18+ box).

Use --sign-source embedded to fall back to the v1 per-theme behavior
(each expansion uses its own embedded sign_deck) for historical comparison.

Usage:
  python3 playtest_all_expansions.py                      # default: base library
  python3 playtest_all_expansions.py --sign-source embedded   # v1 baseline
  python3 playtest_all_expansions.py --games 100
"""

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import playtest_simulator as ps

EXPANSIONS_DIR = ps.DICT_DIR / "game_material" / "expansions"
DECK_PATH = ps.DICT_DIR / "game_material" / "deck.json"
DECK_BACKUP = ps.DICT_DIR / "game_material" / "deck.json.swap_backup"
BASE_SIGN_LIBRARY = ps.DICT_DIR / "game_material" / "base_sign_library.json"
REPORT_PATH = ps.OUT_DIR / "EXPANSION_BALANCE_REPORT.md"
REPORT_PATH_V1 = ps.OUT_DIR / "EXPANSION_BALANCE_REPORT_V1_PER_THEME.md"

PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"


def measure(deck_name: str, n_players: int, n_games: int, seed: int,
            points_to_win: int = 7, draw_n: int = 2,
            logograms_as_wildcards: bool = False,
            market_size: int = 5,
            discard_take_enabled: bool = True,
            actions_per_turn: int = 1,
            equal_turns_ending: bool = True,
            first_player_gift_signs: int = 0,
            logogram_ratio: int = 15) -> dict:
    sign_pool, word_pool, logo_pool = ps.load_deck()
    cfg = ps.GameConfig(
        n_players=n_players,
        agent_names=[AGENT] * n_players,
        starting_hand=8, hand_limit=12,
        points_to_win=points_to_win, max_turns=800,
        draw_n=draw_n,
        logograms_as_wildcards=logograms_as_wildcards,
        market_size=market_size,
        discard_take_enabled=discard_take_enabled,
        actions_per_turn=actions_per_turn,
        equal_turns_ending=equal_turns_ending,
        first_player_gift_signs=first_player_gift_signs,
        logogram_ratio=logogram_ratio,
    )
    results = ps.run_batch(n_games, seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)

    # Dead-card rate within this deck
    deck = json.load(open(DECK_PATH))
    deck_translits = {c["transliteration"] for c in deck["word_deck"]}
    completed = set()
    for r in results:
        for w in r.completed_word_cards:
            completed.add(w)
    dead = len(deck_translits - completed)
    stats["dead_cards"] = dead
    stats["deck_word_count"] = len(deck_translits)
    stats["dead_rate"] = round(dead / len(deck_translits), 3) if deck_translits else 0
    stats["sign_card_copies"] = sum(c["copies"] for c in deck["sign_deck"])
    stats["logogram_count"] = len(deck["logogram_deck"])
    return stats


def synthesize_test_deck(exp_deck: dict, base_signs: list[dict],
                          drop_tiers: set[int] = None) -> dict:
    """
    Build the test deck a player will actually experience: this expansion's
    words + logograms, plus the canonical base sign library. For after_dark,
    also keep its expansion-specific signs (D27, D52, F45, ...) that are
    intentionally absent from the family-safe base library.

    If drop_tiers is given, filter out word cards in those difficulty tiers
    (e.g. drop_tiers={6} removes hardest-tier words). Logogram cards whose
    target word is in a dropped tier are also removed.
    """
    drop_tiers = drop_tiers or set()
    out = dict(exp_deck)
    if drop_tiers:
        kept_translits = set()
        out["word_deck"] = []
        for c in exp_deck["word_deck"]:
            if c.get("shortest_sign_count") in drop_tiers:
                continue
            out["word_deck"].append(c)
            kept_translits.add(c["transliteration"])
        # Logograms only useful if their target word is still in the deck
        out["logogram_deck"] = [
            l for l in exp_deck.get("logogram_deck", [])
            if l.get("word_transliteration") in kept_translits
        ]
        out["dropped_tiers"] = sorted(drop_tiers)
    is_after_dark = (exp_deck.get("theme_slug") == "after_dark"
                     or "After Dark" in exp_deck.get("name", ""))
    base_codes = {c["sign_code"] for c in base_signs}
    if is_after_dark:
        supplement = [c for c in exp_deck.get("sign_deck", [])
                      if c["sign_code"] not in base_codes]
        out["sign_deck"] = list(base_signs) + supplement
        out["sign_source"] = "base_library + after_dark_mature_supplement"
        out["sign_source_supplement_count"] = sum(c["copies"] for c in supplement)
    else:
        out["sign_deck"] = list(base_signs)
        out["sign_source"] = "base_library"
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, default=50)
    p.add_argument("--seed", type=int, default=1000)
    p.add_argument("--sign-source", choices=["base_library", "embedded"],
                   default="base_library",
                   help="Use the canonical base sign library (v2 production "
                        "default) or each expansion's embedded sign_deck (v1 "
                        "per-theme tuned, for historical comparison).")
    p.add_argument("--points-to-win", type=int, default=7,
                   help="Score threshold to win. Used only when "
                        "--flat-points is set. By default points are "
                        "scaled per player count (2p=8, 3p=7, 4p=6).")
    p.add_argument("--flat-points", action="store_true",
                   help="Use a flat --points-to-win for all player counts "
                        "instead of the v8.6 scaled targets (8/7/6).")
    p.add_argument("--draw-n", type=int, default=2,
                   help="Cards drawn per turn. If >1, agent keeps best, "
                        "discards rest. v8 default: 2 (draw-2-keep-1).")
    p.add_argument("--logograms-as-wildcards", action="store_true",
                   help="Allow an unused logogram in hand to substitute "
                        "for ONE missing sign when completing a word.")
    p.add_argument("--market-size", type=int, default=5,
                   help="Face-up sign market of N cards alongside the deck. "
                        "v8 default: 5. Set to 0 to disable.")
    p.add_argument("--no-discard-take", action="store_true",
                   help="Disable the discard-take draw source. By default "
                        "v8 enables it at 3+ players (auto-gated off at 2p "
                        "where it's too dominant).")
    p.add_argument("--actions-per-turn", type=int, default=1,
                   help="Max productive actions per turn. Default 1 "
                        "(draw + 1 action). Set 2 to test multi-action "
                        "turns; agent breaks early on pass.")
    p.add_argument("--instant-win", action="store_true",
                   help="Disable equal-turns ending. v8.7 default is to "
                        "finish the round after a player hits target; this "
                        "flag falls back to the v8.6 instant-win behavior.")
    p.add_argument("--gift", type=int, default=0,
                   help="Number of bonus signs seat 0 gets at game start. "
                        "v8.7 default: 0 (the points scaling obsoletes the "
                        "gift). Set 2 or 4 to test historical behavior.")
    p.add_argument("--logogram-ratio", type=int, default=15,
                   help="One logogram is shuffled into the sign pile per "
                        "this many sign cards. v4 default: 15 (denser = "
                        "more logograms drawn per game). Higher = sparser.")
    p.add_argument("--drop-tier", type=int, action="append", default=None,
                   help="Difficulty tier(s) to drop from each expansion's "
                        "word deck. Default: none (decks are now v7-built "
                        "without tier-6 to begin with; this flag is for "
                        "additional ad-hoc filtering).")
    p.add_argument("--report-suffix", type=str, default="",
                   help="Optional suffix appended to the report filename to "
                        "preserve previous runs.")
    args = p.parse_args()
    drop_tiers = set(args.drop_tier or [])
    if args.sign_source == "base_library":
        report_path = REPORT_PATH
    else:
        report_path = REPORT_PATH_V1
    if args.report_suffix:
        report_path = report_path.with_name(
            report_path.stem + args.report_suffix + report_path.suffix)

    # Discover expansion decks
    expansion_files = sorted(EXPANSIONS_DIR.glob("*.json"))
    if not expansion_files:
        print(f"No expansion decks in {EXPANSIONS_DIR}")
        sys.exit(1)
    print(f"Found {len(expansion_files)} expansion decks")
    print(f"Sign source: {args.sign_source}")

    # Load the base sign library if we'll be using it
    base_signs = None
    if args.sign_source == "base_library":
        if not BASE_SIGN_LIBRARY.exists():
            print(f"ERROR: {BASE_SIGN_LIBRARY} not found")
            sys.exit(1)
        base_signs = json.load(open(BASE_SIGN_LIBRARY))["sign_deck"]
        print(f"Base sign library: "
              f"{len(base_signs)} unique codes, "
              f"{sum(c['copies'] for c in base_signs)} total copies\n")

    # Backup current deck.json
    if DECK_PATH.exists():
        shutil.copy(DECK_PATH, DECK_BACKUP)
        print(f"Backed up {DECK_PATH.name} → {DECK_BACKUP.name}")

    results = {}  # (deck_slug, n_players) -> stats
    deck_metadata = {}

    try:
        for exp_path in expansion_files:
            with open(exp_path) as f:
                exp_deck = json.load(f)
            slug = exp_deck.get("theme_slug", exp_path.stem)
            name = exp_deck.get("name", slug)
            deck_metadata[slug] = {
                "name": name,
                "description": exp_deck.get("theme_description", ""),
                "word_count": len(exp_deck["word_deck"]),
                "logogram_count": len(exp_deck["logogram_deck"]),
                "sign_copies": sum(c["copies"] for c in exp_deck["sign_deck"]),
            }
            # Build the test deck players will actually experience
            if args.sign_source == "base_library":
                test_deck = synthesize_test_deck(exp_deck, base_signs, drop_tiers)
                DECK_PATH.write_text(json.dumps(test_deck, ensure_ascii=False, indent=2))
            elif drop_tiers:
                # Per-theme signs, but still need to filter word tiers
                exp_filtered = dict(exp_deck)
                kept_translits = set()
                exp_filtered["word_deck"] = []
                for c in exp_deck["word_deck"]:
                    if c.get("shortest_sign_count") in drop_tiers:
                        continue
                    exp_filtered["word_deck"].append(c)
                    kept_translits.add(c["transliteration"])
                exp_filtered["logogram_deck"] = [
                    l for l in exp_deck.get("logogram_deck", [])
                    if l.get("word_transliteration") in kept_translits
                ]
                DECK_PATH.write_text(json.dumps(exp_filtered, ensure_ascii=False, indent=2))
            else:
                shutil.copy(exp_path, DECK_PATH)
            print(f"\n=== {name} ({slug}) ===")
            for nplayers in PLAYER_COUNTS:
                # v8.6 default: per-player-count point target scaling.
                if args.flat_points:
                    pts = args.points_to_win
                else:
                    pts = {2: 8, 3: 7, 4: 6}.get(nplayers, args.points_to_win)
                print(f"  {nplayers}p (pts={pts}): ", end="", flush=True)
                stats = measure(slug, nplayers, args.games, args.seed,
                                 points_to_win=pts,
                                 draw_n=args.draw_n,
                                 logograms_as_wildcards=args.logograms_as_wildcards,
                                 market_size=args.market_size,
                                 discard_take_enabled=not args.no_discard_take,
                                 actions_per_turn=args.actions_per_turn,
                                 equal_turns_ending=not args.instant_win,
                                 first_player_gift_signs=args.gift,
                                 logogram_ratio=args.logogram_ratio)
                results[(slug, nplayers)] = stats
                v = stats['end_reasons'].get('victory', 0)
                print(f"balance={stats['balance_score']:>4} "
                      f"victories={v:>3}/{args.games} "
                      f"median_turns={stats['median_turns']:>4} "
                      f"dead={stats['dead_rate']*100:>2.0f}% "
                      f"logos/g={stats['avg_logograms_per_game']:.2f} "
                      f"steals/g={stats['avg_steals_per_game']:.2f}", flush=True)
    finally:
        if DECK_BACKUP.exists():
            shutil.copy(DECK_BACKUP, DECK_PATH)
            try:
                DECK_BACKUP.unlink()
            except (PermissionError, OSError):
                # Some filesystems (mounted user dirs) disallow unlink;
                # leave the backup file in place.
                pass
            print(f"\nRestored {DECK_PATH.name} from backup")

    # ----- Build report -----
    sign_source_label = ("v2 production: signs from base_sign_library.json "
                          f"({sum(c['copies'] for c in base_signs)} copies)"
                          if args.sign_source == "base_library"
                          else "v1 historical: each expansion uses its embedded sign_deck")
    tiers_label = (f", DROPPED tiers: {sorted(drop_tiers)}"
                   if drop_tiers else "")
    points_label = (f"{args.points_to_win} (flat)" if args.flat_points
                    else "v8.6 scaled (2p=8, 3p=7, 4p=6)")
    md = ["# Expansion Decks — Balance Report", ""]
    md.append(f"**Sign source:** {sign_source_label}")
    md.append(f"**Points to win:** {points_label}{tiers_label}")
    md.append("")
    md.append(f"All cells: {args.games} games with `{AGENT}` agent, seed {args.seed}, "
              f"max 800 turns.")
    md.append("")

    # Deck inventory
    md.append("## Deck inventory")
    md.append("")
    md.append("| Deck | Words | Logograms | Sign copies |")
    md.append("|---|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        md.append(f"| {meta['name']} | {meta['word_count']} | "
                  f"{meta['logogram_count']} | {meta['sign_copies']} |")
    md.append("")

    # Per-metric tables
    metric_specs = [
        ("balance_score", "{:.1f}", "Balance score (0–100, higher is better)"),
        ("victory_pct", "{:.0f}%", "Victory rate %"),
        ("median_turns", "{}", "Median game length (turns)"),
        ("avg_score", "{:.1f}", "Average final score"),
        ("avg_steals_per_game", "{:.2f}", "Steals per game"),
        ("avg_logograms_per_game", "{:.2f}", "Logograms played per game"),
        ("dead_rate", "{:.0%}", "Dead-card rate"),
    ]
    for key, fmt, label in metric_specs:
        md.append(f"## {label}")
        md.append("")
        md.append("| Deck | 2p | 3p | 4p | Avg |")
        md.append("|---|---:|---:|---:|---:|")
        for slug, meta in deck_metadata.items():
            cells = []
            cell_vals = []
            for nplayers in PLAYER_COUNTS:
                s = results[(slug, nplayers)]
                if key == "victory_pct":
                    v = s["end_reasons"].get("victory", 0) / args.games
                    cell_vals.append(v)
                    cells.append(fmt.format(v * 100))
                elif key == "dead_rate":
                    cell_vals.append(s[key])
                    cells.append(fmt.format(s[key]))
                else:
                    cell_vals.append(s[key])
                    cells.append(fmt.format(s[key]))
            avg = sum(cell_vals) / len(cell_vals)
            if key == "victory_pct":
                avg_str = f"{avg*100:.0f}%"
            elif key == "dead_rate":
                avg_str = f"{avg*100:.0f}%"
            else:
                avg_str = fmt.format(avg)
            md.append(f"| {meta['name']} | " + " | ".join(cells) + f" | {avg_str} |")
        md.append("")

    # Rankings
    md.append("## Rankings")
    md.append("")

    def avg_metric(slug, key):
        if key == "victory_pct":
            return sum(results[(slug, np)]["end_reasons"].get("victory", 0)
                       for np in PLAYER_COUNTS) / (args.games * len(PLAYER_COUNTS))
        if key == "dead_rate":
            return sum(results[(slug, np)]["dead_rate"]
                       for np in PLAYER_COUNTS) / len(PLAYER_COUNTS)
        return sum(results[(slug, np)][key]
                   for np in PLAYER_COUNTS) / len(PLAYER_COUNTS)

    rank_by_balance = sorted(deck_metadata.keys(),
                              key=lambda s: -avg_metric(s, "balance_score"))
    rank_by_victory = sorted(deck_metadata.keys(),
                              key=lambda s: -avg_metric(s, "victory_pct"))
    rank_by_dead = sorted(deck_metadata.keys(),
                           key=lambda s: avg_metric(s, "dead_rate"))

    md.append("### Best balance (avg across 2/3/4p)")
    md.append("")
    md.append("| Rank | Deck | Avg balance |")
    md.append("|---:|---|---:|")
    for i, slug in enumerate(rank_by_balance, 1):
        md.append(f"| {i} | {deck_metadata[slug]['name']} | "
                  f"{avg_metric(slug, 'balance_score'):.1f} |")
    md.append("")

    md.append("### Best victory rate")
    md.append("")
    md.append("| Rank | Deck | Avg victory % |")
    md.append("|---:|---|---:|")
    for i, slug in enumerate(rank_by_victory, 1):
        md.append(f"| {i} | {deck_metadata[slug]['name']} | "
                  f"{avg_metric(slug, 'victory_pct')*100:.0f}% |")
    md.append("")

    md.append("### Lowest dead-card rate")
    md.append("")
    md.append("| Rank | Deck | Avg dead-card % |")
    md.append("|---:|---|---:|")
    for i, slug in enumerate(rank_by_dead, 1):
        md.append(f"| {i} | {deck_metadata[slug]['name']} | "
                  f"{avg_metric(slug, 'dead_rate')*100:.0f}% |")
    md.append("")

    # Health flags
    md.append("## Health flags")
    md.append("")
    flagged = []
    for slug, meta in deck_metadata.items():
        b = avg_metric(slug, "balance_score")
        v = avg_metric(slug, "victory_pct")
        d = avg_metric(slug, "dead_rate")
        notes = []
        if b < 55:
            notes.append(f"balance {b:.0f} (below healthy 55+ threshold)")
        if v < 0.80:
            notes.append(f"victory rate {v*100:.0f}% (below healthy 80%+)")
        if d > 0.20:
            notes.append(f"dead-card rate {d*100:.0f}% (above healthy 20% ceiling)")
        if notes:
            flagged.append((meta["name"], notes))
    if flagged:
        for name, notes in flagged:
            md.append(f"- **{name}**: " + "; ".join(notes))
    else:
        md.append("All decks pass health checks (balance ≥ 55, victory ≥ 80%, "
                  "dead-card rate ≤ 20%).")
    md.append("")

    report_path.write_text("\n".join(md))
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    main()
