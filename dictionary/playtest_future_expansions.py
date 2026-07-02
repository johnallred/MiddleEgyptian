"""
Test how well the 431-copy shrunk unified sign deck handles FUTURE expansion
decks that don't exist yet.

Two checks:

1. Analytical coverage: across every playable word in the dictionary that is
   NOT already in one of the 8 current expansions, compute the union of sign
   demand. Report (a) signs needed by future words but missing from the
   shrunk deck (= blocked words), (b) signs likely undersupplied for a
   single typical future expansion.

2. Empirical playtest: build four plausible future-theme expansion decks
   from large unused-domain pools (architecture, food, furniture, clothing),
   plus one "untagged general words v2" deck drawn from the long-tail of
   untagged playable words. Play each against the 431-copy unified deck at
   2/3/4 players and compare to the headline metrics from the existing
   expansion-balance report.
"""

import argparse
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

import build_expansion_deck as bed
import build_game_material as bgm
import playtest_simulator as ps

EXPANSIONS_DIR = ps.DICT_DIR / "game_material" / "expansions"
DECK_PATH = ps.DICT_DIR / "game_material" / "deck.json"
DECK_BACKUP = ps.DICT_DIR / "game_material" / "deck.json.swap_backup_future"
SHRUNK_DECK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck_shrunk.json"
TOPPED_UP_DECK_PATH = ps.DICT_DIR / "game_material" / "proposed_base_sign_deck_topped_up.json"
FUTURE_DIR = ps.DICT_DIR / "game_material" / "future_expansions_synthetic"
REPORT_PATH = ps.OUT_DIR / "FUTURE_EXPANSION_PROJECTION.md"
REPORT_PATH_TOPPED_UP = ps.OUT_DIR / "FUTURE_EXPANSION_PROJECTION_TOPPED_UP.md"

PLAYER_COUNTS = [2, 3, 4]
AGENT = "balanced"

# Four plausible future-themed expansions, drawn from large unused-domain pools
FUTURE_THEMES = [
    {
        "slug": "builders_of_egypt",
        "name": "Builders of Egypt",
        "description": "Architecture, monuments, structures.",
        "domain_set": {"architecture"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "markets_and_feasts",
        "name": "Markets & Feasts",
        "description": "Food, drink, agriculture.",
        "domain_set": {"food"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "houses_and_hearths",
        "name": "Houses & Hearths",
        "description": "Furniture, household objects.",
        "domain_set": {"furniture"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "threads_of_linen",
        "name": "Threads of Linen",
        "description": "Clothing, textiles, adornment.",
        "domain_set": {"clothing"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
]


def load_shrunk_deck() -> dict:
    """Return {sign_code: copies} for the 431-copy shrunk unified sign deck."""
    deck = json.load(open(SHRUNK_DECK_PATH))
    supply = {c["sign_code"]: c["copies"] for c in deck["sign_deck"]}
    return supply, deck


def collect_used_translits() -> set[str]:
    """All transliterations used by any current expansion deck."""
    used = set()
    for path in EXPANSIONS_DIR.glob("*.json"):
        deck = json.load(open(path))
        for c in deck["word_deck"]:
            used.add(c["transliteration"])
    return used


def coverage_analysis(supply: dict, word_index: dict, used_words: set[str]) -> dict:
    """
    For each playable word NOT in current expansions, compute sign demand
    using its CANONICAL spelling (first valid spelling). Report which signs
    are absent from the shrunk deck (= words blocked) and which signs would
    be in highest demand across the unused pool.
    """
    unused = {t: info for t, info in word_index.items() if t not in used_words}
    sign_demand = Counter()
    blocked_words = 0
    blocked_by_missing_sign = defaultdict(int)
    words_per_sign = defaultdict(int)  # how many distinct words use each sign
    for translit, info in unused.items():
        if not info["spellings"]:
            continue
        spelling = info["spellings"][0]  # canonical
        # which signs would this word need?
        word_signs = Counter(spelling)
        word_seen = set()
        is_blocked = False
        for sign, count in word_signs.items():
            if sign not in supply:
                is_blocked = True
                blocked_by_missing_sign[sign] += 1
            sign_demand[sign] += count
            if sign not in word_seen:
                words_per_sign[sign] += 1
                word_seen.add(sign)
        if is_blocked:
            blocked_words += 1
    return {
        "unused_word_count": len(unused),
        "sign_demand": sign_demand,
        "words_per_sign": words_per_sign,
        "blocked_words": blocked_words,
        "blocked_by_missing_sign": blocked_by_missing_sign,
    }


def build_future_expansion(theme: dict, deck_size: int,
                            word_index: dict, translit_to_domains: dict,
                            phonetic_signs: dict, logograms: dict,
                            excluded: set[str]) -> dict:
    """Build a themed expansion using the standard bgm/bed code path,
    including auto-relax of per-tier picks for sparse themed pools."""
    filtered = bed.filter_word_index(word_index, theme, translit_to_domains, excluded)
    if not filtered:
        return None
    base_picks = bgm.scaled_picks(deck_size)
    picks, relax_notes = bed.auto_relax_picks(filtered, base_picks, "family")
    if relax_notes:
        print(f"  auto-relax for '{theme['slug']}':")
        for note in relax_notes:
            print(f"    {note}")
    deck = bgm.build_deck(filtered, phonetic_signs, logograms,
                           picks_per_tier_override=picks,
                           content_filter="family")
    deck["theme_slug"] = theme["slug"]
    deck["theme_description"] = theme["description"]
    deck["name"] = f"Hieroglyph Quest: {theme['name']}"
    deck["picks_per_tier"] = picks
    if relax_notes:
        deck["tier_auto_relaxed"] = True
        deck["tier_relax_notes"] = relax_notes
    return deck


def synthesize_test_deck(future_deck: dict, unified_signs: list[dict]) -> dict:
    out = dict(future_deck)
    out["sign_deck"] = unified_signs
    out["name"] = f"{future_deck['name']} [TESTING vs SHRUNK 431]"
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--games", type=int, default=50)
    p.add_argument("--seed", type=int, default=2000)
    p.add_argument("--deck", choices=["shrunk", "topped_up"], default="shrunk",
                   help="Which unified base sign deck to test against")
    args = p.parse_args()
    global SHRUNK_DECK_PATH
    deck_path = TOPPED_UP_DECK_PATH if args.deck == "topped_up" else SHRUNK_DECK_PATH
    report_path = REPORT_PATH_TOPPED_UP if args.deck == "topped_up" else REPORT_PATH
    deck_label = "topped-up" if args.deck == "topped_up" else "shrunk"
    # Temporarily reassign module global so load_shrunk_deck() reads
    # the requested deck. Cleaner refactor would parameterize the function.
    SHRUNK_DECK_PATH = deck_path

    print("Loading dictionary and sign references...")
    phonetic_signs, logograms, determinatives = bgm.load_sign_data()
    det_set = set(determinatives.keys()) | {bgm.norm_sign(k) for k in determinatives}
    phonetic_set = set(phonetic_signs.keys())
    with open(bgm.ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    word_index = bgm.build_word_index(entries, phonetic_set, det_set)
    translit_to_domains = bed.build_translit_to_domains(entries)
    print(f"  {len(word_index):,} playable words")

    if not SHRUNK_DECK_PATH.exists():
        print(f"ERROR: {SHRUNK_DECK_PATH} not found. Run playtest_shrunk_unified.py first.")
        sys.exit(1)
    supply, shrunk_full = load_shrunk_deck()
    print(f"  shrunk unified deck: {len(supply)} unique codes, "
          f"{sum(supply.values())} total copies\n")
    unified_signs = shrunk_full["sign_deck"]

    used_words = collect_used_translits()
    print(f"  {len(used_words):,} words already in the 8 current expansions")

    # ---- Coverage analysis on the unused pool ----
    print("\nRunning analytical coverage check on unused dictionary words...")
    cov = coverage_analysis(supply, word_index, used_words)
    print(f"  {cov['unused_word_count']:,} unused playable words analyzed")
    print(f"  {cov['blocked_words']:,} words use at least one sign absent from shrunk deck")
    if cov['blocked_by_missing_sign']:
        print(f"  Top missing signs (sign → words blocked):")
        for sign, n in sorted(cov['blocked_by_missing_sign'].items(),
                              key=lambda kv: -kv[1])[:10]:
            print(f"    {sign:<10} {n}")
    else:
        print("  Every sign needed by any unused word is present in the shrunk deck.")

    # ---- Build and playtest 4 synthetic future expansions ----
    FUTURE_DIR.mkdir(parents=True, exist_ok=True)
    if DECK_PATH.exists():
        shutil.copy(DECK_PATH, DECK_BACKUP)

    future_results = {}
    future_meta = {}
    try:
        for theme in FUTURE_THEMES:
            print(f"\nBuilding & playtesting '{theme['name']}'...")
            future_deck = build_future_expansion(
                theme, 165, word_index, translit_to_domains,
                phonetic_signs, logograms, used_words)  # exclude current expansion words too
            if not future_deck:
                print(f"  could not build (no matching words)")
                continue
            (FUTURE_DIR / f"{theme['slug']}.json").write_text(
                json.dumps(future_deck, ensure_ascii=False, indent=2))
            test_deck = synthesize_test_deck(future_deck, unified_signs)
            DECK_PATH.write_text(json.dumps(test_deck, ensure_ascii=False, indent=2))
            future_meta[theme["slug"]] = {
                "name": theme["name"],
                "word_count": len(future_deck["word_deck"]),
                "logogram_count": len(future_deck["logogram_deck"]),
                "native_sign_copies": sum(c["copies"] for c in future_deck["sign_deck"]),
            }
            for nplayers in PLAYER_COUNTS:
                print(f"  {nplayers}p: ", end="", flush=True)
                stats = measure(nplayers, args.games, args.seed)
                future_results[(theme["slug"], nplayers)] = stats
                v = stats['end_reasons'].get('victory', 0)
                print(f"balance={stats['balance_score']:>4} "
                      f"victories={v:>3}/{args.games} "
                      f"median_turns={stats['median_turns']:>4} "
                      f"dead={stats['dead_rate']*100:>2.0f}%", flush=True)
    finally:
        if DECK_BACKUP.exists():
            shutil.copy(DECK_BACKUP, DECK_PATH)
            try:
                DECK_BACKUP.unlink()
            except (PermissionError, OSError):
                pass
            print("\nRestored deck.json from backup")

    # ---- Build report ----
    total_signs = sum(supply.values())
    n_codes = len(supply)
    md = [f"# Future-Expansion Projection: {deck_label.title()} Unified Sign Deck ({n_codes} codes / {total_signs} copies)", ""]
    md.append(f"**Tested deck:** `{deck_path.name}` ({n_codes} unique sign codes, "
              f"{total_signs} total card copies)")
    md.append("")
    md.append(f"**Question:** the {deck_label} unified sign deck supports future expansion "
              "decks built from the long tail of the dictionary?")
    md.append("")
    md.append("Two checks were run.")
    md.append("")

    # Coverage analysis section
    md.append("## 1. Analytical sign coverage across the unused dictionary pool")
    md.append("")
    md.append(f"Of the **{len(word_index):,}** playable words in `Entries2.json`, "
              f"**{len(used_words):,}** are already in one of the 8 current expansions, "
              f"leaving **{cov['unused_word_count']:,}** unused. That long tail is the pool "
              f"future expansions will draw from.")
    md.append("")
    md.append(f"**Words with sign demand the shrunk deck can't fulfill:** "
              f"**{cov['blocked_words']:,}** "
              f"({cov['blocked_words'] / cov['unused_word_count'] * 100:.1f}% of unused).")
    md.append("")
    if cov["blocked_by_missing_sign"]:
        md.append("These signs are required by some unused words but are **absent from the "
                  "shrunk 431-copy deck entirely**. Any expansion built around them would need "
                  "to ship its own copies of these specific signs, or skip the affected words:")
        md.append("")
        md.append("| Sign code | Unused words blocked |")
        md.append("|---|---:|")
        for sign, n in sorted(cov["blocked_by_missing_sign"].items(),
                              key=lambda kv: -kv[1])[:25]:
            md.append(f"| `{sign}` | {n} |")
        md.append("")
    else:
        md.append("**Every sign needed by any unused word is present in the shrunk deck.** "
                  "No future word is structurally blocked — at worst a future theme might run "
                  "low on copies of a particular sign during a single game.")
        md.append("")

    # Top demand among unused words
    md.append("### Highest-demand signs across the unused word pool")
    md.append("")
    md.append("This shows which signs would be drawn on most by future expansions. The "
              "`In shrunk deck` column shows how many copies the 431-copy deck holds; "
              "the `Words using` column shows how many unused words include this sign.")
    md.append("")
    md.append("| Sign | In shrunk deck | Words using | Total uses |")
    md.append("|---|---:|---:|---:|")
    for sign, total_uses in cov["sign_demand"].most_common(20):
        in_deck = supply.get(sign, 0)
        words_using = cov["words_per_sign"][sign]
        md.append(f"| `{sign}` | {in_deck} | {words_using:,} | {total_uses:,} |")
    md.append("")

    # Domain inventory of unused-domain candidates
    md.append("## 2. Synthetic future-expansion playtests")
    md.append("")
    md.append("Four hypothetical future expansion decks were built from the largest "
              "unused-domain pools in the dictionary, then played 50 games each at 2/3/4p "
              "**against the shrunk 431-copy unified sign deck** (no per-theme sign tuning).")
    md.append("")
    md.append("| Synthetic theme | Domain pool | Words drawn | Logograms | "
              "Per-theme sign copies it would have used |")
    md.append("|---|---|---:|---:|---:|")
    for theme in FUTURE_THEMES:
        m = future_meta.get(theme["slug"])
        if not m:
            md.append(f"| {theme['name']} | {','.join(sorted(theme['domain_set']))} | "
                      f"— | — | (could not build) |")
            continue
        md.append(f"| {theme['name']} | {','.join(sorted(theme['domain_set']))} | "
                  f"{m['word_count']} | {m['logogram_count']} | {m['native_sign_copies']} |")
    md.append("")

    md.append("### Results at the shrunk 431-copy unified sign deck")
    md.append("")
    md.append("Reference baselines from the original expansion playtest "
              "(per-theme tuned signs, hand=8): balance avg = ~62, victory ≥ 80%, "
              "dead-card rate ~14–17%.")
    md.append("")
    md.append("| Theme | 2p balance | 3p balance | 4p balance | Avg balance | "
              "Avg victory | Avg dead | Avg turns |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for theme in FUTURE_THEMES:
        slug = theme["slug"]
        if not future_meta.get(slug):
            continue
        b = [future_results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS]
        v = [future_results[(slug, np)]["end_reasons"].get("victory", 0) / args.games * 100
             for np in PLAYER_COUNTS]
        d = [future_results[(slug, np)]["dead_rate"] * 100 for np in PLAYER_COUNTS]
        t = [future_results[(slug, np)]["median_turns"] for np in PLAYER_COUNTS]
        md.append(f"| {theme['name']} | {b[0]:.1f} | {b[1]:.1f} | {b[2]:.1f} | "
                  f"{sum(b)/3:.1f} | {sum(v)/3:.0f}% | "
                  f"{sum(d)/3:.0f}% | {sum(t)/3:.0f} |")
    md.append("")

    # Health flags
    md.append("### Health flags")
    md.append("")
    flagged = []
    for theme in FUTURE_THEMES:
        slug = theme["slug"]
        if not future_meta.get(slug):
            continue
        b = sum(future_results[(slug, np)]["balance_score"] for np in PLAYER_COUNTS) / 3
        v = sum(future_results[(slug, np)]["end_reasons"].get("victory", 0)
                for np in PLAYER_COUNTS) / (args.games * 3)
        d = sum(future_results[(slug, np)]["dead_rate"] for np in PLAYER_COUNTS) / 3
        notes = []
        if b < 55: notes.append(f"balance {b:.0f} below 55")
        if v < 0.80: notes.append(f"victory {v*100:.0f}% below 80%")
        if d > 0.20: notes.append(f"dead-card {d*100:.0f}% above 20%")
        if notes:
            flagged.append((theme["name"], notes))
    if flagged:
        for name, notes in flagged:
            md.append(f"- **{name}**: " + "; ".join(notes))
    else:
        md.append("All four synthetic future expansions pass every health check when run "
                  "against the shrunk 431-copy unified sign deck.")
    md.append("")

    report_path.write_text("\n".join(md))
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    main()
