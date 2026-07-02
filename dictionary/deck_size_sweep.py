"""
Sweep deck size at multiple player counts to find the optimal deck.

For each (deck_size, n_players) cell we:
  1. Regenerate the deck with scaled tier sizes.
  2. Convert deck.json into in-memory pools the simulator needs.
  3. Run N games with the balanced agent (most representative).
  4. Record balance score, victory rate, median turns, steals/game,
     logograms/game, dead-card rate.

Result: a heat-map-style markdown report comparing all cells.

Usage:
  python3 deck_size_sweep.py             # default: 100 games per cell
  python3 deck_size_sweep.py --games 200 # bigger sweep
"""

import argparse
import json
from pathlib import Path

import build_game_material as bgm
import playtest_simulator as ps


DECK_SIZES = [150, 175, 200, 225, 250, 275, 300]
PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"

OUT_DIR = ps.OUT_DIR


def regenerate_deck_at_size(size: int):
    """Regenerate deck.json with tier sizes scaled to `size` total words."""
    phonetic_signs, logograms, determinatives = bgm.load_sign_data()
    print(f"  Loading entries... ", end="", flush=True)
    with open(bgm.ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"loaded {len(entries):,}.", flush=True)
    print(f"  Building word index... ", end="", flush=True)
    det_set = set(determinatives.keys()) | {bgm.norm_sign(k) for k in determinatives}
    word_index = bgm.build_word_index(entries, set(phonetic_signs.keys()), det_set)
    print(f"{len(word_index):,} words.", flush=True)

    picks = bgm.scaled_picks(size)
    deck = bgm.build_deck(word_index, phonetic_signs, logograms,
                           picks_per_tier_override=picks)
    deck["version"] = f"sweep-{size}"
    deck_path = bgm.OUT_DIR / "deck.json"
    with open(deck_path, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    return deck


def measure_cell(size: int, n_players: int, n_games: int, base_seed: int) -> dict:
    """Run n_games games at given size+players, return aggregate metrics."""
    sign_pool, word_pool, logo_pool = ps.load_deck()
    cfg = ps.GameConfig(
        n_players=n_players,
        agent_names=[AGENT] * n_players,
        starting_hand=8, hand_limit=12,
        points_to_win=10, max_turns=800,
    )
    results = ps.run_batch(n_games, base_seed, sign_pool, word_pool, logo_pool, cfg)
    stats = ps.analyze(results)
    # Add dead-card rate
    word_translits = {c["transliteration"] for c in
                      json.load(open(ps.DECK_PATH))["word_deck"]}
    completed = set()
    for r in results:
        for w in r.completed_word_cards:
            completed.add(w)
    dead = len(word_translits) - len(completed & word_translits)
    stats["dead_cards"] = dead
    stats["deck_word_count"] = len(word_translits)
    stats["dead_rate"] = round(dead / len(word_translits), 3) if word_translits else 0
    return stats


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, default=100)
    p.add_argument("--seed", type=int, default=1000)
    args = p.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = {}  # (size, players) -> stats

    for size in DECK_SIZES:
        print(f"\n=== Regenerating deck at size {size} ===")
        deck = regenerate_deck_at_size(size)
        actual_words = len(deck["word_deck"])
        actual_signs = sum(c["copies"] for c in deck["sign_deck"])
        actual_logos = len(deck["logogram_deck"])
        print(f"  deck: {actual_words} words / {actual_signs} sign copies / {actual_logos} logograms")
        for nplayers in PLAYER_COUNTS:
            print(f"  {nplayers}p: ", end="", flush=True)
            stats = measure_cell(size, nplayers, args.games, args.seed)
            stats["actual_words"] = actual_words
            stats["actual_signs"] = actual_signs
            stats["actual_logograms"] = actual_logos
            results[(size, nplayers)] = stats
            print(f"balance={stats['balance_score']} "
                  f"victories={stats['end_reasons'].get('victory',0)}/{args.games} "
                  f"dead={stats['dead_rate']*100:.0f}% "
                  f"logos/game={stats['avg_logograms_per_game']}", flush=True)

    # ----- Write comparison report -----
    md = ["# Deck-Size Sweep Report", ""]
    md.append(f"Each cell = {args.games} games with `balanced` agent. "
              f"Seed {args.seed}. Target 10 points, max 800 turns.")
    md.append("")

    for metric, fmt, label in [
        ("balance_score", "{:.1f}", "Balance score (0-100, higher is better)"),
        ("end_reasons", "victory_pct", "Victory rate %"),
        ("median_turns", "{}", "Median game length (turns)"),
        ("avg_steals_per_game", "{:.2f}", "Steals per game"),
        ("avg_logograms_per_game", "{:.2f}", "Logograms played per game"),
        ("dead_rate", "{:.0%}", "Dead-card rate (% of deck never completed)"),
    ]:
        md.append(f"## {label}")
        md.append("")
        md.append("| Deck size | 2p | 3p | 4p |")
        md.append("|---:|---:|---:|---:|")
        for size in DECK_SIZES:
            row = [f"{size}"]
            for nplayers in PLAYER_COUNTS:
                s = results[(size, nplayers)]
                if fmt == "victory_pct":
                    v = s["end_reasons"].get("victory", 0)
                    cell = f"{100*v/args.games:.0f}%"
                else:
                    cell = fmt.format(s[metric])
                row.append(cell)
            md.append("| " + " | ".join(row) + " |")
        md.append("")

    # Recommendations
    md.append("## Recommendations")
    md.append("")
    # Find the deck size with best balance score averaged across player counts
    by_size = {}
    for size in DECK_SIZES:
        scores = [results[(size, np)]["balance_score"] for np in PLAYER_COUNTS]
        dead_rates = [results[(size, np)]["dead_rate"] for np in PLAYER_COUNTS]
        victory_rates = [results[(size, np)]["end_reasons"].get("victory", 0) / args.games
                         for np in PLAYER_COUNTS]
        by_size[size] = {
            "avg_balance": sum(scores) / len(scores),
            "avg_dead": sum(dead_rates) / len(dead_rates),
            "avg_victory": sum(victory_rates) / len(victory_rates),
        }

    best_balance = max(by_size, key=lambda s: by_size[s]["avg_balance"])
    best_victory = max(by_size, key=lambda s: by_size[s]["avg_victory"])
    least_dead = min(by_size, key=lambda s: by_size[s]["avg_dead"])

    md.append(f"- **Best average balance score**: deck size **{best_balance}** "
              f"({by_size[best_balance]['avg_balance']:.1f})")
    md.append(f"- **Highest average victory rate**: deck size **{best_victory}** "
              f"({by_size[best_victory]['avg_victory']*100:.0f}%)")
    md.append(f"- **Lowest dead-card rate**: deck size **{least_dead}** "
              f"({by_size[least_dead]['avg_dead']*100:.0f}%)")
    md.append("")

    md.append("### Averages by deck size")
    md.append("")
    md.append("| Deck size | Avg balance | Avg victory % | Avg dead-card % |")
    md.append("|---:|---:|---:|---:|")
    for size in DECK_SIZES:
        d = by_size[size]
        md.append(f"| {size} | {d['avg_balance']:.1f} | "
                  f"{d['avg_victory']*100:.0f}% | {d['avg_dead']*100:.0f}% |")
    md.append("")

    md.append("Smaller decks have fewer dead cards (each card sees the table more often) "
              "but offer less replay variety. Larger decks have more variety but more "
              "of the cards never get completed in any given game.")
    md.append("")

    out_path = OUT_DIR / "DECK_SIZE_SWEEP_REPORT.md"
    out_path.write_text("\n".join(md))
    print(f"\nReport: {out_path}")


if __name__ == "__main__":
    main()
