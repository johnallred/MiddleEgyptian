"""
Re-run the unified-sign-deck playtest with starting_hand bumped 8 → 10.

Premise: under the unified-sign architecture, the sign draw deck is larger
(547 copies) than per-theme decks (305–357 copies), so each individual draw
has a lower probability of producing a sign a player actually needs. Median
game length grew ~60%. Bumping starting hand size should compensate by
giving each player more in-play sign material from the outset, hopefully
recovering the per-theme speed without giving up the architecture savings.

This script reuses the same unified sign deck written to
`proposed_base_sign_deck.json` by playtest_unified_signs.py.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

import playtest_simulator as ps

EXPANSIONS_DIR = ps.DICT_DIR / "game_material" / "expansions"
DECK_PATH = ps.DICT_DIR / "game_material" / "deck.json"
DECK_BACKUP = ps.DICT_DIR / "game_material" / "deck.json.swap_backup3"
PROPOSED_DECK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck.json"
REPORT_PATH = ps.OUT_DIR / "UNIFIED_HAND10_REPORT.md"
PRIOR_PER_THEME_REPORT = ps.OUT_DIR / "EXPANSION_BALANCE_REPORT.md"
PRIOR_UNIFIED_REPORT = ps.OUT_DIR / "UNIFIED_SIGN_DECK_REPORT.md"

PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"
NEW_STARTING_HAND = 10
NEW_HAND_LIMIT = 12  # unchanged, so starting_hand=10 has a 2-card buffer


def synthesize_test_deck(expansion_path: Path, unified_signs: list[dict]) -> dict:
    exp = json.load(open(expansion_path))
    out = dict(exp)
    out["sign_deck"] = unified_signs
    out["name"] = f"{exp.get('name', expansion_path.stem)} [UNIFIED+HAND10]"
    return out


def measure(n_players: int, n_games: int, seed: int) -> dict:
    sign_pool, word_pool, logo_pool = ps.load_deck()
    cfg = ps.GameConfig(
        n_players=n_players,
        agent_names=[AGENT] * n_players,
        starting_hand=NEW_STARTING_HAND,
        hand_limit=NEW_HAND_LIMIT,
        points_to_win=10, max_turns=800,
    )
    results = ps.run_batch(n_games, seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)
    deck = json.load(open(DECK_PATH))
    deck_translits = {c["transliteration"] for c in deck["word_deck"]}
    completed = set()
    for r in results:
        for w in r.completed_word_cards:
            completed.add(w)
    stats["dead_rate"] = round(
        (len(deck_translits) - len(completed)) / len(deck_translits), 3
    ) if deck_translits else 0
    return stats


def parse_prior_metric(report_path: Path, metric_header: str) -> dict:
    """
    Pull a per-deck row from a prior report. Returns {name: [v2p, v3p, v4p]}.
    """
    out = {}
    if not report_path.exists():
        return out
    current = None
    for line in report_path.read_text().splitlines():
        if line.startswith("## ") or line.startswith("### "):
            current = line.lstrip("# ").strip()
        elif line.startswith("| Hieroglyph Quest:") and current == metric_header:
            parts = [p.strip() for p in line.strip("|").split("|")]
            name = parts[0]
            try:
                vals = [float(x.rstrip("%")) for x in parts[1:4]]
                out[name] = vals
            except ValueError:
                continue
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, default=50)
    p.add_argument("--seed", type=int, default=1000)
    args = p.parse_args()

    if not PROPOSED_DECK_PATH.exists():
        print(f"ERROR: {PROPOSED_DECK_PATH} not found. "
              f"Run playtest_unified_signs.py first.")
        sys.exit(1)
    proposed = json.load(open(PROPOSED_DECK_PATH))
    unified_signs = proposed["sign_deck"]
    print(f"Unified sign deck: {proposed['unique_sign_count']} unique codes, "
          f"{proposed['total_sign_copies']} total copies")
    print(f"Config: starting_hand={NEW_STARTING_HAND}, hand_limit={NEW_HAND_LIMIT}\n")

    expansion_files = sorted(EXPANSIONS_DIR.glob("*.json"))
    if DECK_PATH.exists():
        shutil.copy(DECK_PATH, DECK_BACKUP)
        print("Backed up deck.json\n")

    results = {}
    deck_metadata = {}
    try:
        for exp_path in expansion_files:
            with open(exp_path) as f:
                exp_deck = json.load(f)
            slug = exp_deck.get("theme_slug", exp_path.stem)
            name = exp_deck.get("name", slug)
            deck_metadata[slug] = {"name": name}
            test_deck = synthesize_test_deck(exp_path, unified_signs)
            DECK_PATH.write_text(json.dumps(test_deck, ensure_ascii=False, indent=2))
            print(f"=== {name} ===")
            for nplayers in PLAYER_COUNTS:
                print(f"  {nplayers}p: ", end="", flush=True)
                stats = measure(nplayers, args.games, args.seed)
                results[(slug, nplayers)] = stats
                v = stats['end_reasons'].get('victory', 0)
                print(f"balance={stats['balance_score']:>4} "
                      f"victories={v:>3}/{args.games} "
                      f"median_turns={stats['median_turns']:>4} "
                      f"dead={stats['dead_rate']*100:>2.0f}% "
                      f"logos/g={stats['avg_logograms_per_game']:.2f} "
                      f"steals/g={stats['avg_steals_per_game']:.2f}", flush=True)
            print()
    finally:
        if DECK_BACKUP.exists():
            shutil.copy(DECK_BACKUP, DECK_PATH)
            try:
                DECK_BACKUP.unlink()
            except (PermissionError, OSError):
                pass
            print("Restored deck.json from backup")

    # Pull prior data for side-by-side
    per_theme_turns = parse_prior_metric(PRIOR_PER_THEME_REPORT, "Median game length (turns)")
    per_theme_bal = parse_prior_metric(PRIOR_PER_THEME_REPORT, "Balance score (0–100, higher is better)")
    per_theme_dead = parse_prior_metric(PRIOR_PER_THEME_REPORT, "Dead-card rate")
    unified_h8_turns = parse_prior_metric(PRIOR_UNIFIED_REPORT, "Median game length (turns)")
    unified_h8_bal = parse_prior_metric(PRIOR_UNIFIED_REPORT, "Balance score")
    unified_h8_dead = parse_prior_metric(PRIOR_UNIFIED_REPORT, "Dead-card rate")

    # Build report
    md = ["# Unified Signs + Starting Hand 10 — Re-Playtest Report", ""]
    md.append(f"**Tested config:** unified sign deck ({proposed['total_sign_copies']} copies), "
              f"`starting_hand={NEW_STARTING_HAND}`, `hand_limit={NEW_HAND_LIMIT}`.")
    md.append("")
    md.append(f"All cells: {args.games} games with `{AGENT}` agent, seed {args.seed}, "
              f"target 10 points, max 800 turns.")
    md.append("")
    md.append("**Hypothesis:** unified-sign deck (547 copies) dilutes each draw vs. "
              "per-theme decks (305–357 copies). Bumping starting hand from 8 → 10 gives "
              "each player two extra signs at game start, hopefully recovering the speed "
              "lost to centralization while keeping the 57% card-print savings.")
    md.append("")

    # Build report
    md = ["# Unified Signs + Starting Hand 10 — Re-Playtest Report", ""]
    md.append(f"**Tested config:** unified sign deck ({proposed['total_sign_copies']} copies), "
              f"`starting_hand={NEW_STARTING_HAND}`, `hand_limit={NEW_HAND_LIMIT}`.")
    md.append("")
    md.append(f"All cells: {args.games} games with `{AGENT}` agent, seed {args.seed}, "
              f"target 10 points, max 800 turns.")
    md.append("")
    md.append("**Hypothesis:** unified-sign deck (547 copies) dilutes each draw vs. "
              "per-theme decks (305–357 copies). Bumping starting hand from 8 → 10 gives "
              "each player two extra signs at game start, hopefully recovering the speed "
              "lost to centralization while keeping the 57% card-print savings.")
    md.append("")

    def fmt(v, suffix=""):
        return "—" if v is None else f"{v:.0f}{suffix}"

    def fmtf(v, suffix=""):
        return "—" if v is None else f"{v:.1f}{suffix}"

    def fmt_delta(v):
        return "—" if v is None else f"{v:+.0f}"

    def fmt_delta_pp(v):
        return "—" if v is None else f"{v:+.1f}"

    # Game length
    md.append("## Game length (median turns) — three-way comparison")
    md.append("")
    md.append("| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 | Δ vs per-theme h=8 |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["median_turns"] for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = per_theme_turns.get(meta["name"])
        u8 = unified_h8_turns.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_h8 = (new_avg - u8_avg) if u8_avg is not None else None
        d_pt = (new_avg - pt_avg) if pt_avg is not None else None
        md.append(f"| {meta['name']} | {fmt(pt_avg)} | {fmt(u8_avg)} | "
                  f"{new_avg:.0f} | {fmt_delta(d_h8)} | {fmt_delta(d_pt)} |")
    md.append("")

    # Balance
    md.append("## Balance score — three-way comparison")
    md.append("")
    md.append("| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 | Δ vs per-theme h=8 |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = per_theme_bal.get(meta["name"])
        u8 = unified_h8_bal.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_h8 = (new_avg - u8_avg) if u8_avg is not None else None
        d_pt = (new_avg - pt_avg) if pt_avg is not None else None
        md.append(f"| {meta['name']} | {fmtf(pt_avg)} | {fmtf(u8_avg)} | "
                  f"{new_avg:.1f} | {fmt_delta_pp(d_h8)} | {fmt_delta_pp(d_pt)} |")
    md.append("")

    # Dead-card rate
    md.append("## Dead-card rate — three-way comparison")
    md.append("")
    md.append("| Deck | Per-theme h=8 | Unified h=8 | Unified h=10 | Δ vs unified h=8 |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = per_theme_dead.get(meta["name"])
        u8 = unified_h8_dead.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_h8 = (new_avg - u8_avg) if u8_avg is not None else None
        md.append(f"| {meta['name']} | {fmt(pt_avg, '%')} | {fmt(u8_avg, '%')} | "
                  f"{new_avg:.0f}% | {fmt_delta_pp(d_h8)} pp |")
    md.append("")

    # Per-player-count breakdown
    md.append("## Unified-signs + hand=10: results by player count")
    md.append("")
    md.append("### Balance score")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        c = [results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        md.append(f"| {meta['name']} | {c[0]:.1f} | {c[1]:.1f} | {c[2]:.1f} | "
                  f"{sum(c)/len(c):.1f} |")
    md.append("")

    md.append("### Median turns")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        c = [results[(slug, np)]["median_turns"] for np in PLAYER_COUNTS]
        md.append(f"| {meta['name']} | {c[0]} | {c[1]} | {c[2]} | "
                  f"{sum(c)/len(c):.0f} |")
    md.append("")

    md.append("### Victory rate")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        c = [results[(slug, np)]["end_reasons"].get("victory", 0) / args.games * 100
             for np in PLAYER_COUNTS]
        md.append(f"| {meta['name']} | {c[0]:.0f}% | {c[1]:.0f}% | {c[2]:.0f}% | "
                  f"{sum(c)/len(c):.0f}% |")
    md.append("")

    md.append("### Dead-card rate")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        c = [results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        md.append(f"| {meta['name']} | {c[0]:.0f}% | {c[1]:.0f}% | {c[2]:.0f}% | "
                  f"{sum(c)/len(c):.0f}% |")
    md.append("")

    # Health flags
    md.append("## Health flags")
    md.append("")
    flagged = []
    for slug, meta in deck_metadata.items():
        b = sum(results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS) / len(PLAYER_COUNTS)
        v = sum(results[(slug, np)]["end_reasons"].get("victory", 0)
                for np in PLAYER_COUNTS) / (args.games * len(PLAYER_COUNTS))
        d = sum(results[(slug, np)]["dead_rate"] for np in PLAYER_COUNTS) / len(PLAYER_COUNTS)
        notes = []
        if b < 55:
            notes.append(f"balance {b:.0f} below 55")
        if v < 0.80:
            notes.append(f"victory {v*100:.0f}% below 80%")
        if d > 0.20:
            notes.append(f"dead-card {d*100:.0f}% above 20%")
        if notes:
            flagged.append((meta["name"], notes))
    if flagged:
        for name, notes in flagged:
            md.append(f"- **{name}**: " + "; ".join(notes))
    else:
        md.append("All decks pass health checks under unified signs + hand=10.")
    md.append("")

    REPORT_PATH.write_text("\n".join(md))
    print(f"\nReport: {REPORT_PATH}")


if __name__ == "__main__":
    main()
