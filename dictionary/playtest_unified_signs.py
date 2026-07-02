"""
Playtest each themed expansion's word + logogram cards against a SINGLE
unified sign deck (the "signs-in-base" architecture proposal).

The unified sign deck is built by taking the union of every sign code that
appears across any expansion's sign_deck, and setting each sign's copy count
to the MAXIMUM seen for that sign in any single expansion. That guarantees
the unified deck can support the highest single-deck demand for every sign.
If the result is materially below the 400-copy target, we scale up by a
constant factor to reach ~400. If it's materially above, we leave it (the
data is telling us the real number is higher).

For each themed expansion we then build a synthetic deck:
    word_deck      = expansion's word_deck (165)
    logogram_deck  = expansion's logogram_deck (theme-tuned)
    sign_deck      = unified sign deck (same for all themes)

…and run a 50-game balanced-agent batch at 2, 3, and 4 players.

Output:
  game_material/playtest_results/UNIFIED_SIGN_DECK_REPORT.md
  game_material/proposed_base_sign_deck.json   (the deck itself, for reference)
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
DECK_BACKUP = ps.DICT_DIR / "game_material" / "deck.json.swap_backup2"
REPORT_PATH = ps.OUT_DIR / "UNIFIED_SIGN_DECK_REPORT.md"
PROPOSED_DECK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck.json"
PRIOR_REPORT = ps.OUT_DIR / "EXPANSION_BALANCE_REPORT.md"

PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"


def build_unified_sign_deck(expansion_paths: list[Path], target_copies: int) -> list[dict]:
    """
    Union of all sign codes across expansions; each sign's copy count is the
    max seen across any expansion. Then optionally scale to hit ~target_copies.
    """
    max_copies = defaultdict(int)
    canonical_card = {}  # sign_code -> a representative dict from one of the decks
    for path in expansion_paths:
        deck = json.load(open(path))
        for card in deck["sign_deck"]:
            code = card["sign_code"]
            if card["copies"] > max_copies[code]:
                max_copies[code] = card["copies"]
            if code not in canonical_card:
                canonical_card[code] = {k: v for k, v in card.items() if k != "copies"}
    raw_total = sum(max_copies.values())
    print(f"  union-of-max sign deck: {len(max_copies)} unique codes, "
          f"{raw_total} total copies (target: ~{target_copies})")

    # Only scale UP if substantially below target; never scale below the
    # union-of-max requirement (that would break the single-expansion guarantee).
    if raw_total < target_copies * 0.92:
        factor = target_copies / raw_total
        for code in max_copies:
            max_copies[code] = max(1, round(max_copies[code] * factor))
        scaled_total = sum(max_copies.values())
        print(f"  scaled up by {factor:.3f} → {scaled_total} total copies")

    unified = []
    for code in sorted(max_copies.keys()):
        card = dict(canonical_card[code])
        card["copies"] = max_copies[code]
        unified.append(card)
    return unified


def write_unified_deck(unified_signs: list[dict]) -> dict:
    deck = {
        "name": "Hieroglyph Quest: Proposed Base Sign Library",
        "version": "1.0",
        "expansion_type": "base_sign_library_proposal",
        "sign_deck": unified_signs,
        "logogram_deck": [],
        "word_deck": [],
        "unique_sign_count": len(unified_signs),
        "total_sign_copies": sum(c["copies"] for c in unified_signs),
    }
    PROPOSED_DECK_PATH.write_text(json.dumps(deck, ensure_ascii=False, indent=2))
    return deck


def synthesize_test_deck(expansion_path: Path, unified_signs: list[dict]) -> dict:
    """Combine an expansion's word + logo cards with the unified sign deck."""
    exp = json.load(open(expansion_path))
    test_deck = dict(exp)
    test_deck["sign_deck"] = unified_signs
    test_deck["name"] = f"{exp.get('name', expansion_path.stem)} [UNIFIED-SIGNS TEST]"
    test_deck["unified_sign_test"] = True
    return test_deck


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
    dead = len(deck_translits - completed)
    stats["dead_rate"] = round(dead / len(deck_translits), 3) if deck_translits else 0
    return stats


def load_prior_results() -> dict:
    """Parse the EXPANSION_BALANCE_REPORT.md tables to enable side-by-side."""
    if not PRIOR_REPORT.exists():
        return {}
    text = PRIOR_REPORT.read_text()
    # Light-weight: just pull the balance + dead-card columns. We could parse
    # everything but the comparison is fine with these two metrics.
    prior = {}
    current_metric = None
    for line in text.splitlines():
        if line.startswith("## "):
            current_metric = line[3:].strip()
        elif line.startswith("| Hieroglyph Quest:"):
            parts = [p.strip() for p in line.strip("|").split("|")]
            name = parts[0]
            try:
                vals = [float(x.rstrip("%")) for x in parts[1:4]]
            except ValueError:
                continue
            prior.setdefault(name, {})[current_metric] = vals
    return prior


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

    # Backup current deck.json
    if DECK_PATH.exists():
        shutil.copy(DECK_PATH, DECK_BACKUP)
        print(f"Backed up deck.json")

    # Build unified sign deck
    print("Building unified sign deck (union-of-max across all expansions):")
    unified_signs = build_unified_sign_deck(expansion_files, args.target_copies)
    proposed_deck = write_unified_deck(unified_signs)
    print(f"  written to {PROPOSED_DECK_PATH.name}")
    print(f"  {proposed_deck['unique_sign_count']} unique codes, "
          f"{proposed_deck['total_sign_copies']} total copies\n")

    results = {}
    deck_metadata = {}
    try:
        for exp_path in expansion_files:
            with open(exp_path) as f:
                exp_deck = json.load(f)
            slug = exp_deck.get("theme_slug", exp_path.stem)
            name = exp_deck.get("name", slug)
            deck_metadata[slug] = {"name": name}
            # Synthesize and write the test deck
            test_deck = synthesize_test_deck(exp_path, unified_signs)
            DECK_PATH.write_text(json.dumps(test_deck, ensure_ascii=False, indent=2))
            print(f"=== {name} (unified signs) ===")
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
            print(f"Restored deck.json from backup")

    # Build report
    prior = load_prior_results()
    md = ["# Unified Sign Deck — Re-Playtest Report", ""]
    md.append(f"**Tested architecture:** signs centralized in base, expansions ship words + logograms only.")
    md.append("")
    md.append(f"All cells: {args.games} games with `{AGENT}` agent, seed {args.seed}, "
              f"target 10 points, max 800 turns.")
    md.append("")
    md.append(f"**Unified sign deck:** {proposed_deck['unique_sign_count']} unique Gardiner codes, "
              f"**{proposed_deck['total_sign_copies']} total card copies**.")
    md.append("")
    md.append("Built by taking the union of every sign code seen across any of the 8 expansion "
              "sign decks, with each sign's copy count set to the maximum copy count that sign "
              "had in any single expansion. This guarantees the unified deck can support every "
              "expansion at the per-theme tuned sign-demand it was designed for.")
    md.append("")

    # Side-by-side comparison vs. prior (per-theme) sign decks
    md.append("## Balance: per-theme signs vs. unified signs")
    md.append("")
    md.append("| Deck | Per-theme avg | Unified avg | Δ |")
    md.append("|---|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        prior_vals = prior.get(meta["name"], {}).get("Balance score (0–100, higher is better)", None)
        if prior_vals:
            old_avg = sum(prior_vals) / len(prior_vals)
            delta = new_avg - old_avg
            md.append(f"| {meta['name']} | {old_avg:.1f} | {new_avg:.1f} | "
                      f"{delta:+.1f} |")
        else:
            md.append(f"| {meta['name']} | — | {new_avg:.1f} | — |")
    md.append("")

    md.append("## Dead-card rate: per-theme signs vs. unified signs")
    md.append("")
    md.append("| Deck | Per-theme avg | Unified avg | Δ |")
    md.append("|---|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        new_vals = [results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        new_avg = sum(new_vals) / len(new_vals)
        prior_vals = prior.get(meta["name"], {}).get("Dead-card rate", None)
        if prior_vals:
            old_avg = sum(prior_vals) / len(prior_vals)
            delta = new_avg - old_avg
            md.append(f"| {meta['name']} | {old_avg:.0f}% | {new_avg:.0f}% | "
                      f"{delta:+.1f} pp |")
        else:
            md.append(f"| {meta['name']} | — | {new_avg:.0f}% | — |")
    md.append("")

    # Full per-cell tables on the new (unified) configuration
    md.append("## Unified-signs results, by player count")
    md.append("")
    md.append("### Balance score")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        cells = [results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        avg = sum(cells) / len(cells)
        md.append(f"| {meta['name']} | "
                  + " | ".join(f"{c:.1f}" for c in cells)
                  + f" | {avg:.1f} |")
    md.append("")

    md.append("### Victory rate")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        cells = [results[(slug, np)]["end_reasons"].get("victory", 0) / args.games * 100
                  for np in PLAYER_COUNTS]
        avg = sum(cells) / len(cells)
        md.append(f"| {meta['name']} | "
                  + " | ".join(f"{c:.0f}%" for c in cells)
                  + f" | {avg:.0f}% |")
    md.append("")

    md.append("### Dead-card rate")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        cells = [results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        avg = sum(cells) / len(cells)
        md.append(f"| {meta['name']} | "
                  + " | ".join(f"{c:.0f}%" for c in cells)
                  + f" | {avg:.0f}% |")
    md.append("")

    md.append("### Median game length (turns)")
    md.append("")
    md.append("| Deck | 2p | 3p | 4p | Avg |")
    md.append("|---|---:|---:|---:|---:|")
    for slug, meta in deck_metadata.items():
        cells = [results[(slug, np)]["median_turns"] for np in PLAYER_COUNTS]
        avg = sum(cells) / len(cells)
        md.append(f"| {meta['name']} | "
                  + " | ".join(str(c) for c in cells)
                  + f" | {avg:.0f} |")
    md.append("")

    # Health flags
    md.append("## Health flags (unified signs)")
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
        md.append("All decks pass health checks under the unified-signs architecture "
                  "(balance ≥ 55, victory ≥ 80%, dead-card rate ≤ 20%).")
    md.append("")

    REPORT_PATH.write_text("\n".join(md))
    print(f"\nReport: {REPORT_PATH}")
    print(f"Proposed base sign deck: {PROPOSED_DECK_PATH}")


if __name__ == "__main__":
    main()
