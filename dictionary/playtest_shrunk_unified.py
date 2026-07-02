"""
Playtest a SHRUNK unified sign deck.

Premise: the 547-copy union-of-max unified deck is conservative — for any
single expansion in play, many signs are oversupplied. A smaller unified
deck that targets the AVERAGE per-game demand per sign (not the worst-case
demand) should restore much of the per-theme game speed while keeping the
signs-in-base architecture.

Shrinkage strategy (mean-of-containing-themes):
  For each sign code that appears in at least one expansion's sign deck,
    copies = round(mean of copy-count across themes that contain that sign)
    clamp min 1
  Then if total still exceeds target, scale all counts down uniformly.

The target is configurable (`--target-copies`, default 400). The script
writes the shrunken deck to `proposed_base_sign_deck_shrunk.json` and runs
50-game playtests at 2/3/4p for each themed expansion.
"""

import argparse
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import playtest_simulator as ps

EXPANSIONS_DIR = ps.DICT_DIR / "game_material" / "expansions"
DECK_PATH = ps.DICT_DIR / "game_material" / "deck.json"
DECK_BACKUP = ps.DICT_DIR / "game_material" / "deck.json.swap_backup4"
SHRUNK_DECK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck_shrunk.json"
REPORT_PATH = ps.OUT_DIR / "UNIFIED_SHRUNK_REPORT.md"
PRIOR_PER_THEME = ps.OUT_DIR / "EXPANSION_BALANCE_REPORT.md"
PRIOR_UNIFIED = ps.OUT_DIR / "UNIFIED_SIGN_DECK_REPORT.md"

PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"


def build_shrunk_sign_deck(expansion_paths: list[Path], target_copies: int) -> tuple[list[dict], dict]:
    """
    Compute per-sign:
       - sum of copies across themes that include it
       - count of themes that include it
       - max copies across any single theme (for floor — we never go below 1)
    Then assign copies = max(1, round(sum / count)) → "mean per containing theme".
    Then if total > target, scale down uniformly with floor 1.
    """
    sums = defaultdict(int)
    counts = defaultdict(int)
    max_per_sign = defaultdict(int)
    canonical = {}
    for path in expansion_paths:
        deck = json.load(open(path))
        for card in deck["sign_deck"]:
            code = card["sign_code"]
            sums[code] += card["copies"]
            counts[code] += 1
            if card["copies"] > max_per_sign[code]:
                max_per_sign[code] = card["copies"]
            if code not in canonical:
                canonical[code] = {k: v for k, v in card.items() if k != "copies"}

    # Mean-of-containing
    chosen = {code: max(1, round(sums[code] / counts[code])) for code in sums}
    raw_total = sum(chosen.values())
    print(f"  mean-of-containing: {len(chosen)} unique codes, {raw_total} copies "
          f"(target ~{target_copies})")

    # Scale down if over target
    if raw_total > target_copies:
        factor = target_copies / raw_total
        chosen = {code: max(1, round(n * factor)) for code, n in chosen.items()}
        scaled_total = sum(chosen.values())
        print(f"  scaled down by {factor:.3f} → {scaled_total} total copies")

    # Build the deck card list
    unified = []
    for code in sorted(chosen.keys()):
        c = dict(canonical[code])
        c["copies"] = chosen[code]
        unified.append(c)
    debug = {
        "raw_total": raw_total,
        "max_per_sign": dict(max_per_sign),
        "chosen": chosen,
    }
    return unified, debug


def synthesize_test_deck(expansion_path: Path, unified_signs: list[dict]) -> dict:
    exp = json.load(open(expansion_path))
    out = dict(exp)
    out["sign_deck"] = unified_signs
    out["name"] = f"{exp.get('name', expansion_path.stem)} [UNIFIED-SHRUNK]"
    return out


def measure(n_players: int, n_games: int, seed: int) -> dict:
    sign_pool, word_pool, logo_pool = ps.load_deck()
    cfg = ps.GameConfig(
        n_players=n_players,
        agent_names=[AGENT] * n_players,
        starting_hand=8, hand_limit=12,
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
    p.add_argument("--target-copies", type=int, default=400)
    args = p.parse_args()

    expansion_files = sorted(EXPANSIONS_DIR.glob("*.json"))
    if not expansion_files:
        print(f"No expansion decks in {EXPANSIONS_DIR}")
        sys.exit(1)
    print(f"Found {len(expansion_files)} expansion decks\n")

    # Build the shrunk deck
    print(f"Building shrunk unified sign deck (target={args.target_copies}):")
    shrunk_signs, debug = build_shrunk_sign_deck(expansion_files, args.target_copies)
    total = sum(c["copies"] for c in shrunk_signs)
    shrunk_meta = {
        "name": "Hieroglyph Quest: Proposed Base Sign Library (SHRUNK)",
        "version": "1.0",
        "expansion_type": "base_sign_library_proposal_shrunk",
        "sign_deck": shrunk_signs,
        "logogram_deck": [],
        "word_deck": [],
        "unique_sign_count": len(shrunk_signs),
        "total_sign_copies": total,
        "target_copies": args.target_copies,
        "shrinkage_strategy": "mean_of_containing_themes_then_uniform_scale",
    }
    SHRUNK_DECK_PATH.write_text(json.dumps(shrunk_meta, ensure_ascii=False, indent=2))
    print(f"  written to {SHRUNK_DECK_PATH.name}")
    print(f"  {len(shrunk_signs)} unique codes, {total} total copies\n")

    # Backup deck.json
    if DECK_PATH.exists():
        shutil.copy(DECK_PATH, DECK_BACKUP)

    results = {}
    deck_metadata = {}
    try:
        for exp_path in expansion_files:
            with open(exp_path) as f:
                exp_deck = json.load(f)
            slug = exp_deck.get("theme_slug", exp_path.stem)
            name = exp_deck.get("name", slug)
            deck_metadata[slug] = {"name": name}
            test_deck = synthesize_test_deck(exp_path, shrunk_signs)
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

    # Pull prior data
    pt_turns = parse_prior_metric(PRIOR_PER_THEME, "Median game length (turns)")
    pt_bal = parse_prior_metric(PRIOR_PER_THEME, "Balance score (0–100, higher is better)")
    pt_dead = parse_prior_metric(PRIOR_PER_THEME, "Dead-card rate")
    u8_turns = parse_prior_metric(PRIOR_UNIFIED, "Median game length (turns)")
    u8_bal = parse_prior_metric(PRIOR_UNIFIED, "Balance score")
    u8_dead = parse_prior_metric(PRIOR_UNIFIED, "Dead-card rate")

    md = [f"# Shrunk Unified Sign Deck — Re-Playtest Report", ""]
    md.append(f"**Tested config:** shrunk unified sign deck "
              f"({len(shrunk_signs)} codes, {total} copies, target {args.target_copies}), "
              f"`starting_hand=8`, `hand_limit=12`.")
    md.append("")
    md.append(f"All cells: {args.games} games with `{AGENT}` agent, seed {args.seed}, "
              f"target 10 points, max 800 turns.")
    md.append("")
    md.append("**Shrinkage strategy:** for each sign code, set copies = mean across "
              "themes that contain it (rounded, min 1), then if total exceeds target "
              f"({args.target_copies}), scale all sign counts down uniformly.")
    md.append("")
    md.append(f"Compared to: per-theme baseline (305–357 copies, per-theme tuned) "
              f"and original unified (547 copies, union-of-max).")
    md.append("")

    def fmt(v, suffix=""): return "—" if v is None else f"{v:.0f}{suffix}"
    def fmtf(v, suffix=""): return "—" if v is None else f"{v:.1f}{suffix}"
    def fmtd(v): return "—" if v is None else f"{v:+.0f}"
    def fmtdf(v): return "—" if v is None else f"{v:+.1f}"

    # Game length
    md.append("## Game length (median turns) — four-way comparison")
    md.append("")
    md.append("| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 | Δ vs Per-theme |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["median_turns"] for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = pt_turns.get(meta["name"])
        u8 = u8_turns.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_u8 = (new_avg - u8_avg) if u8_avg is not None else None
        d_pt = (new_avg - pt_avg) if pt_avg is not None else None
        md.append(f"| {meta['name']} | {fmt(pt_avg)} | {fmt(u8_avg)} | "
                  f"{new_avg:.0f} | {fmtd(d_u8)} | {fmtd(d_pt)} |")
    md.append("")

    # Balance
    md.append("## Balance score — four-way comparison")
    md.append("")
    md.append("| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 | Δ vs Per-theme |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = pt_bal.get(meta["name"])
        u8 = u8_bal.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_u8 = (new_avg - u8_avg) if u8_avg is not None else None
        d_pt = (new_avg - pt_avg) if pt_avg is not None else None
        md.append(f"| {meta['name']} | {fmtf(pt_avg)} | {fmtf(u8_avg)} | "
                  f"{new_avg:.1f} | {fmtdf(d_u8)} | {fmtdf(d_pt)} |")
    md.append("")

    # Dead-card
    md.append("## Dead-card rate — four-way comparison")
    md.append("")
    md.append("| Deck | Per-theme | Unified 547 | Shrunk | Δ vs Unified 547 |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        pt = pt_dead.get(meta["name"])
        u8 = u8_dead.get(meta["name"])
        pt_avg = (sum(pt) / len(pt)) if pt else None
        u8_avg = (sum(u8) / len(u8)) if u8 else None
        d_u8 = (new_avg - u8_avg) if u8_avg is not None else None
        md.append(f"| {meta['name']} | {fmt(pt_avg, '%')} | {fmt(u8_avg, '%')} | "
                  f"{new_avg:.0f}% | {fmtdf(d_u8)} pp |")
    md.append("")

    # Per-player-count breakdown
    md.append("## Shrunk-deck results, by player count")
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
        md.append(f"All decks pass health checks under the shrunk unified-signs deck "
                  f"({total} copies).")
    md.append("")

    REPORT_PATH.write_text("\n".join(md))
    print(f"\nReport: {REPORT_PATH}")


if __name__ == "__main__":
    main()
