"""
Build themed expansion decks (Option C: modular boosters).

Each themed deck is self-contained (165 word cards + its own sign + logogram
support cards) AND designed to mix with other decks for Festival Mode.

Usage:
  python3 build_expansion_deck.py --all                  # generate all 7 themed decks
  python3 build_expansion_deck.py --theme gods           # generate just one
  python3 build_expansion_deck.py --theme custom --domains divinity,epithet --name "My Deck"

Outputs go to game_material/expansions/<safe_name>.json.

Each output is a fully-self-contained deck.json with the same schema as the
core deck. Per the PROJECT_GUIDE Mix Mode rules, players combine multiple
deck.json files (shuffle word decks, shuffle sign decks, shuffle logogram
decks) to play with bigger pools.

Themes ship with v1 are below; add new ones by editing THEMES.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import build_game_material as bgm

EXPANSIONS_DIR = bgm.OUT_DIR / "expansions"


# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------
#
# Each theme is a tuple of:
#   (slug, display_name, [domain_set | gloss_keyword_predicate],
#    optional exclusion of previously-used words)
#
# A theme accepts a word if it has ANY of the listed domains, OR if its
# English glosses match the optional keyword predicate. The "core" theme is
# the special general-vocab pool: words with NO Domain tag (the long tail).
# "Pantheon Expanded" and "Wild Egypt" are second-pulls from the same domain
# pools as their primary decks, using `exclude_already_used`.

THEMES = [
    {
        "slug": "core_daily_life",
        "name": "Core Set: Daily Life",
        "description": "General Middle Egyptian vocabulary. The entry-point deck.",
        # Strategy: use Faulkner-/Vygus-/Dickson-attested words with NO specific Domain.
        "domain_set": None,    # special: no domain filter
        "gloss_keywords": None,
        "fallback_general": True,
    },
    {
        "slug": "gods_and_temples",
        "name": "Gods & Temples",
        "description": "Divinities, priests, temples, and ritual.",
        "domain_set": {"divinity", "epithet", "ritual", "religious", "ceremonial"},
        "gloss_keywords": [
            "god", "goddess", "divine", "temple", "shrine",
            "priest", "ritual", "offering", "sacred",
        ],
        "fallback_general": False,
    },
    {
        "slug": "beasts_of_the_nile",
        "name": "Beasts of the Nile",
        "description": "Animals, birds, and fish of Egypt.",
        "domain_set": {"animal", "bird", "fish"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "body_and_healing",
        "name": "Body & Healing",
        "description": "Anatomy, medicine, and healing arts.",
        "domain_set": {"body", "medical", "medicinal", "bodily"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "kings_and_court",
        "name": "Kings & Court",
        "description": "Royalty, officials, titles, and court life.",
        "domain_set": {"title", "royal"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "the_land_of_egypt",
        "name": "The Land of Egypt",
        "description": "Geography, sailing, sky, and place names.",
        "domain_set": {"location", "locality", "boat", "astronomy"},
        "gloss_keywords": None,
        "fallback_general": False,
    },
    {
        "slug": "pantheon_expanded",
        "name": "Pantheon Expanded",
        "description": "More gods, epithets, and religious vocabulary.",
        "domain_set": {"divinity", "epithet", "ritual", "religious", "ceremonial",
                        "mythological", "festival"},
        "gloss_keywords": [
            "deity", "goddess", "spirit", "soul", "afterlife", "tomb", "amulet",
        ],
        "fallback_general": False,
        "exclude_from": "gods_and_temples",
    },
    {
        "slug": "wild_egypt",
        "name": "Wild Egypt",
        "description": "More flora, fauna, and the natural world.",
        "domain_set": {"animal", "bird", "fish", "flora", "mineral"},
        "gloss_keywords": None,
        "fallback_general": False,
        "exclude_from": "beasts_of_the_nile",
    },
    # ----- v2 expansions (validated against base_sign_library.json) -----
    {
        "slug": "builders_of_egypt",
        "name": "Builders of Egypt",
        "description": "Architecture, monuments, structures, and the craft of building.",
        "domain_set": {"architecture"},
        "gloss_keywords": ["temple", "pyramid", "tomb", "wall", "column",
                            "pillar", "doorway", "gate"],
        "fallback_general": False,
    },
    {
        "slug": "markets_and_feasts",
        "name": "Markets & Feasts",
        "description": "Food, drink, agriculture, and the table.",
        "domain_set": {"food"},
        "gloss_keywords": ["bread", "beer", "wine", "loaf", "harvest", "grain"],
        "fallback_general": False,
    },
    {
        "slug": "houses_and_hearths",
        "name": "Houses & Hearths",
        "description": "Furniture, household goods, and daily implements.",
        "domain_set": {"furniture"},
        "gloss_keywords": ["chair", "table", "bed", "chest", "vessel", "jar"],
        "fallback_general": False,
    },
    {
        "slug": "threads_of_linen",
        "name": "Threads of Linen",
        "description": "Clothing, textiles, jewelry, and adornment.",
        "domain_set": {"clothing"},
        "gloss_keywords": ["linen", "robe", "kilt", "garment", "amulet",
                            "ornament", "crown"],
        "fallback_general": False,
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def build_translit_to_domains(entries) -> dict[str, set[str]]:
    m = defaultdict(set)
    for e in entries:
        t = (e.get("Transliteration") or "").strip()
        if not t:
            continue
        for tr in e.get("Translations") or []:
            md = tr.get("TranslationMetadata") or {}
            for d in md.get("Domains") or []:
                m[t].add(d)
    return m


def filter_word_index(word_index: dict, theme: dict,
                      translit_to_domains: dict[str, set[str]],
                      excluded_words: set[str]) -> dict:
    """
    Return a sub-dict of word_index containing only words that match the
    theme's domain set or gloss keywords, and aren't in excluded_words.
    """
    out = {}
    domain_set = theme.get("domain_set")
    gloss_kw = theme.get("gloss_keywords") or []
    gloss_pat = (re.compile(r"\b(" + "|".join(re.escape(k) for k in gloss_kw) + r")\b",
                             re.IGNORECASE) if gloss_kw else None)

    for translit, info in word_index.items():
        if translit in excluded_words:
            continue
        # Core / fallback general: take words with NO Domain tag
        if theme.get("fallback_general"):
            if not translit_to_domains.get(translit):
                out[translit] = info
            continue
        # Theme: match on domain OR gloss keyword
        word_domains = translit_to_domains.get(translit, set())
        if domain_set and word_domains & domain_set:
            out[translit] = info
            continue
        if gloss_pat:
            for g in info.get("english_glosses", []):
                if gloss_pat.search(g or ""):
                    out[translit] = info
                    break
    return out


def write_expansion(theme: dict, deck: dict) -> Path:
    EXPANSIONS_DIR.mkdir(parents=True, exist_ok=True)
    slug = theme["slug"]
    path = EXPANSIONS_DIR / f"{slug}.json"
    deck["name"] = f"Hieroglyph Quest: {theme['name']}"
    deck["theme_slug"] = slug
    deck["theme_description"] = theme["description"]
    deck["expansion_type"] = "modular_booster"
    deck["mix_mode_compatible"] = True
    path.write_text(json.dumps(deck, ensure_ascii=False, indent=2))
    return path


def auto_relax_picks(filtered_index: dict, base_picks: dict[int, int],
                     content_filter: str = "family") -> tuple[dict[int, int], list[str]]:
    """
    Adjust per-tier pick counts when the filtered (themed) word pool has
    insufficient words in some tiers. Shortfall from sparse tiers is
    redistributed to neighboring tiers that have surplus availability,
    preferring the closest tier so theme difficulty drift is minimized.

    Returns: (adjusted_picks, notes_about_relaxation)

    For family decks, a tier's available word count is computed using only
    words that have at least one family-safe spelling, since the build
    script will drop the rest before populating tiers.
    """
    # Tiers are driven by what's in base_picks; v7 drops tier 6 entirely.
    tiers = sorted(base_picks.keys())
    avail = {n: 0 for n in tiers}
    for translit, info in filtered_index.items():
        n = info.get("shortest_sign_count", 0)
        if n not in avail:
            continue
        if content_filter == "family":
            spellings = info.get("spellings", [])
            if not any(not any(s in bgm.FAMILY_BLOCKED_SIGNS for s in sp)
                       for sp in spellings):
                continue
        avail[n] += 1

    adjusted = dict(base_picks)
    notes = []
    # First pass: cap each tier at availability, accumulate shortfall
    for n in tiers:
        if adjusted[n] > avail[n]:
            shortfall = adjusted[n] - avail[n]
            notes.append(
                f"tier {n} ({bgm.TIER_NAMES.get(n, '?')}): target {adjusted[n]} "
                f"→ capped at {avail[n]} (shortfall {shortfall})"
            )
            adjusted[n] = avail[n]
            # Push shortfall to nearest tier with surplus, preferring +1, -1, +2, ...
            for dist in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
                target_tier = n + dist
                if target_tier not in avail:
                    continue
                surplus = avail[target_tier] - adjusted[target_tier]
                if surplus <= 0:
                    continue
                take = min(shortfall, surplus)
                adjusted[target_tier] += take
                shortfall -= take
                notes.append(
                    f"  ↳ +{take} pushed to tier {target_tier} "
                    f"({bgm.TIER_NAMES.get(target_tier, '?')})"
                )
                if shortfall == 0:
                    break
            if shortfall > 0:
                notes.append(
                    f"  ↳ {shortfall} cards UNFILLED (filtered pool too small overall)"
                )
    return adjusted, notes


def build_one(theme: dict, deck_size: int, content_filter: str,
              shared_state: dict) -> tuple[Path, int, int]:
    """
    Build one themed deck.
    `shared_state` carries cross-theme info like:
      - 'word_index' (built once)
      - 'translit_to_domains'
      - 'used_words_by_theme' (slug -> set of translits used)
      - 'phonetic_signs', 'logograms'
    """
    word_index = shared_state["word_index"]
    translit_to_domains = shared_state["translit_to_domains"]
    phonetic_signs = shared_state["phonetic_signs"]
    logograms = shared_state["logograms"]
    used = shared_state["used_words_by_theme"]

    excluded = set()
    if theme.get("exclude_from"):
        excluded = used.get(theme["exclude_from"], set())

    filtered = filter_word_index(word_index, theme, translit_to_domains, excluded)
    if not filtered:
        print(f"  WARNING: theme '{theme['slug']}' matched 0 words.")
        return None, 0, 0

    # Auto-relax tier targets if the filtered pool is sparse in any tier.
    # This keeps decks playable for themes drawn from less-common vocabulary.
    base_picks = bgm.scaled_picks(deck_size)
    picks, relax_notes = auto_relax_picks(filtered, base_picks, content_filter)
    if relax_notes:
        print(f"  auto-relax for '{theme['slug']}':")
        for note in relax_notes:
            print(f"    {note}")

    deck = bgm.build_deck(filtered, phonetic_signs, logograms,
                          picks_per_tier_override=picks,
                          content_filter=content_filter)
    deck["content_filter"] = content_filter
    deck["target_deck_size"] = deck_size
    deck["picks_per_tier"] = picks
    if relax_notes:
        deck["tier_auto_relaxed"] = True
        deck["tier_relax_notes"] = relax_notes

    # Record words used (for downstream exclusion in 'expanded' decks)
    used_translits = {c["transliteration"] for c in deck["word_deck"]}
    used[theme["slug"]] = used_translits

    path = write_expansion(theme, deck)
    return path, len(deck["word_deck"]), len(deck["logogram_deck"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true", help="Generate all themed decks")
    p.add_argument("--theme", type=str, help="Single theme slug to generate")
    p.add_argument("--deck-size", type=int, default=165)
    p.add_argument("--content-filter", choices=["family", "mature", "archaeological"],
                   default="family")
    p.add_argument("--name", type=str, help="Custom theme name (with --theme custom)")
    p.add_argument("--domains", type=str, help="Comma-separated domains "
                   "(with --theme custom)")
    args = p.parse_args()

    if not args.all and not args.theme:
        print("ERROR: pass --all or --theme <slug>")
        sys.exit(1)

    # Load shared data once
    print("Loading data...")
    phonetic_signs, logograms, determinatives = bgm.load_sign_data()
    det_set = set(determinatives.keys()) | {bgm.norm_sign(k) for k in determinatives}
    phonetic_set = set(phonetic_signs.keys())
    with open(bgm.ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    word_index = bgm.build_word_index(entries, phonetic_set, det_set)
    translit_to_domains = build_translit_to_domains(entries)
    print(f"  {len(word_index):,} playable words")
    print(f"  {len(translit_to_domains):,} words with Domain tags\n")

    shared = {
        "word_index": word_index,
        "translit_to_domains": translit_to_domains,
        "phonetic_signs": phonetic_signs,
        "logograms": logograms,
        "used_words_by_theme": {},
    }

    if args.all:
        for theme in THEMES:
            print(f"Building '{theme['name']}'...")
            path, nw, nl = build_one(theme, args.deck_size, args.content_filter, shared)
            if path:
                print(f"  → {path.name}: {nw} word cards, {nl} logogram cards\n")
    elif args.theme == "custom":
        if not args.name or not args.domains:
            print("ERROR: --theme custom requires --name and --domains")
            sys.exit(1)
        theme = {
            "slug": re.sub(r"[^a-z0-9]+", "_", args.name.lower()).strip("_"),
            "name": args.name,
            "description": "Custom deck",
            "domain_set": set(args.domains.split(",")),
            "gloss_keywords": None,
            "fallback_general": False,
        }
        path, nw, nl = build_one(theme, args.deck_size, args.content_filter, shared)
        if path:
            print(f"  → {path.name}: {nw} word cards, {nl} logogram cards")
    else:
        for theme in THEMES:
            if theme["slug"] == args.theme:
                path, nw, nl = build_one(theme, args.deck_size, args.content_filter, shared)
                if path:
                    print(f"  → {path.name}: {nw} word cards, {nl} logogram cards")
                break
        else:
            print(f"ERROR: no theme '{args.theme}'. Choices: "
                  f"{[t['slug'] for t in THEMES]}, custom")
            sys.exit(1)


if __name__ == "__main__":
    main()
