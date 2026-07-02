# Hieroglyph Quest — Project Guide

A self-contained briefing for an AI assistant (or any new contributor)
asked to help expand this Middle Egyptian hieroglyphic card game. Read
this once and you'll know everything about the data, schemas, design
choices, and how to generate new decks.

---

## 1. What this project is

**Hieroglyph Quest** is a card game in which players collect Egyptian
hieroglyphic sign cards to spell out Middle Egyptian words. Each word
card shows a transliteration like `nfr` "good" along with the English
meaning; players must lay down the right **set** of phonetic signs
(or play a logogram shortcut) to complete it — completion is a
multiset match, order does not matter (made official in the v8.7
documentation sync, §23). Points are awarded by difficulty (1 sign =
1 point, 4 signs = 4 points, etc.). Stealing is allowed only by
completing an opponent's word in one continuous play.

The game is built on top of a cleaned, structured Middle Egyptian
dictionary called `Entries2.json` (45,492 entries pulled from four
academic sources: Faulkner's *Concise Dictionary of Middle Egyptian*,
Mark Vygus's 2012 and 2018 dictionaries, Paul Dickson's dictionary, and
the OpenGlyph Lexicon). A separate file `res_signinfo.js` (from
Mark-Jan Nederhof's RES project) provides the sign-by-sign reference
including phonetic mnemonics, logogram values, and determinative usage.

**Materials already produced** (under `game_material/`):

- `rules.md` — printable rules page (one tabletop session's worth).
- `deck.json` — the family-mode Core starter set (v8.10 build: 168
  unique sign cards / 349 copies, 47 logogram cards, 165 word cards).
- `words/` — 9,466 per-word JSON files organized by shortest
  phonetic-spelling length (`1_sign/` through `7_plus_sign/`). Each
  file describes one playable word with all valid spellings,
  point-value, POS, English glosses, and a sign-by-sign annotation.
- `PROJECT_GUIDE.md` — this file.

The game-design choice that ties everything together is that the game's
spelling mechanic mirrors real Egyptian writing: **biliterals and
triliterals cover multiple consonants at once**, **logograms shortcut
entire words**, and **multiple spellings per word are valid** — exactly
how ancient scribes worked.

---

## 2. Quick context: Middle Egyptian writing in two pages

If you (the AI) don't have strong Egyptology background, this section
will get you to working level. Skip if you're already fluent.

### 2.1 Consonant-only writing

Middle Egyptian is written without vowels. A word's transliteration
shows only the consonants. So `nfr` "good, beautiful" is read with
whatever vowels conventional pronunciation supplies (usually rendered
"nefer"), but the writing system only encodes the three consonants
n + f + r.

### 2.2 The transliteration alphabet

Twenty-four consonant letters, **case-sensitive**:

| Letter | Sound | Letter | Sound |
|---|---|---|---|
| A | aleph (glottal stop, ꜣ) | s | s |
| a | ayin (pharyngeal, ꜥ) | S | sh (š) |
| b | b | q | emphatic k (q) |
| p | p | k | k |
| f | f | g | g |
| m | m | t | t |
| n | n | T | "ty" (ṯ) |
| r | r | d | d |
| h | h | D | "dy" (ḏ) |
| H | emphatic h (ḥ) | i / j | reed-i (j̱) |
| x | "kh" (ḫ) | w / W | w (W is variant) |
| X | softer kh (ẖ) | y | "y" doubled-i |

Uppercase letters represent **distinct phonemes**, not variants of the
lowercase ones. `s` and `S` are completely different sounds; same for
`h`/`H`/`x`/`X`, `t`/`T`, `d`/`D`.

### 2.3 The sign categories

Every hieroglyph belongs to one of Gardiner's 26 semantic categories
(A through Z plus Aa for "miscellaneous"):

```
A: Man and his Activities          O: Buildings, parts of buildings
B: Woman and her Activities         P: Ships and parts of ships
C: Anthropomorphic Deities          Q: Domestic and funerary furniture
D: Parts of the Human Body          R: Temple furniture, sacred emblems
E: Mammals                          S: Crowns, dress, staves, etc.
F: Parts of Mammals                 T: Warfare, hunting, butchery
G: Birds                            U: Agriculture, crafts, professions
H: Parts of Birds                   V: Rope, basketry, baskets, bags
I: Reptiles, amphibians, etc.       W: Vessels of stone, earthenware
J: (unused historically)            X: Loaves, cakes
K: Fish, parts of fish              Y: Writings, games, music
L: Invertebrates, lesser animals    Z: Strokes, geometric figures
M: Trees, plants                    Aa: Unclassified
N: Sky, earth, water
```

A **sign code** is the category letter plus a number: `A1` (seated
man), `G17` (owl), `N5` (sun disc), `Aa1` (sieve/placenta). Variants
get a trailing lowercase letter (`F37a`, `Y1v`) — except this project's
dictionary historically uppercased them (`F37A`, `Y1V`) and the cleanup
pipeline normalizes case at lookup time.

### 2.4 The four roles a sign can play

The same sign can take any of several roles depending on context:

1. **Phonetic** — represents one, two, or three consonants
   (uniliteral, biliteral, triliteral). Example: `G17` (owl) is the
   uniliteral *m*. `Y5` (game board) is the biliteral *mn*. `Aa11`
   (placenta) is the triliteral *Hr* — wait that's biliteral too,
   choose another. `N5` (sun disc) is the uniliteral *r* used
   logographically for *ra* "sun"...
2. **Logogram** — IS an entire word. `N5` alone = *ra* "sun"; `A1` =
   *s* "man"; `D2` = *Hr* "face".
3. **Determinative** — silent semantic classifier at the end of a
   word. Tells the reader what kind of thing the word is (man,
   action, abstract idea, etc.) without contributing sound.
4. **Phonetic determinative** — hybrid: both adds sound and indicates
   category.

The phonetic role is what the game is built around. Determinatives are
stripped during deck generation (but referenced in the optional rules).

### 2.5 Multiple spellings are normal

Egyptian scribes routinely had several ways to write the same word:
just the logogram, the logogram plus determinative, fully phonetic, or
phonetic with a logogram thrown in as a clarifier. The dictionary
documents these alternative writings as separate entries. In our game,
a single word card can list 2–10 valid spellings — players pick
whichever path their hand supports.

### 2.6 "Mnemonic" terminology

In `res_signinfo.js`, the **mnemonic** field is the conventional
transliteration of a sign's primary phonetic value, used as a
memory aid. The mnemonic of `G17` is `m`; of `Y5` is `mn`; of `R8` is
`nTr`. The mnemonic's letter count tells you the phonetic class:

- 1 letter = uniliteral
- 2 letters = biliteral
- 3 letters = triliteral
- 4+ letters = quadriliteral or longer

A small number of signs have a numeric mnemonic (`100`, `1000`) —
those are pure numerals.

---

## 3. Project layout

```
MiddleEgyptian/                                       <- project root
└── MiddleEgyptian/MiddleEgyptian/                    <- web prototype root
    ├── dictionary/
    │   ├── Entries.json                              <- ORIGINAL, do NOT modify
    │   ├── Entries2.json                             <- cleaned working copy
    │   ├── Keywords.json / Keywords.bson              <- keyword index for Entries.json
    │   ├── CitationIndex.json                         <- inverted citation index
    │   ├── sign_classification/                       <- output of classify_signs.py
    │   │   ├── signs_by_phonetic_class.json
    │   │   ├── signs_logogram.json
    │   │   ├── signs_determinative.json
    │   │   ├── signs_use_as_variant.json
    │   │   ├── signs_phonetic_marker.json
    │   │   ├── signs_phonetic_determinative.json
    │   │   ├── signs_numeric.json
    │   │   └── signs_unclassified.json
    │   ├── game_material/                             <- the game
    │   │   ├── PROJECT_GUIDE.md                       <- you are here
    │   │   ├── rules.md
    │   │   ├── deck.json
    │   │   └── words/
    │   │       ├── 1_sign/  (779 files)
    │   │       ├── 2_sign/  (1,376 files)
    │   │       ├── 3_sign/  (2,239 files)
    │   │       ├── 4_sign/  (2,266 files)
    │   │       ├── 5_sign/  (1,423 files)
    │   │       ├── 6_sign/  (756 files)
    │   │       └── 7_plus_sign/  (627 files)
    │   └── *.py                                       <- cleanup + generation scripts
    ├── faulkner/                                      <- 403 per-page Faulkner JSON scrapes
    ├── fonts/                                         <- hieroglyph TTFs
    │   └── unknown_glyphs.txt                         <- signs with no Unicode glyph
    ├── index/                                         <- web-app sign-list assets
    └── res/                                           <- the RES rendering library
        └── res_signinfo.js                            <- THE sign reference; 1,070 signs
```

The path that matters for game-building work: everything in `dictionary/`.

---

## 4. The Entries2.json dictionary

The single source of truth for the game's content. JSONL: one entry
per line.

### 4.1 Entry schema

```json
{
  "_id": {"$oid": "628573728383418c993add6d"},
  "Transliteration": "rmT",
  "GardinerSigns": "A1 A1 A1",
  "ManuelDeCodage": "A1-A1-A1",
  "Res": "A1-A1-A1",
  "AttestationCount": 5,
  "VariantOf": ["other_word"],                  // optional
  "GardinerMdCMismatch": true,                  // optional flag
  "TransliterationUnknown": true,               // optional flag
  "Translations": [
    {
      "translation": "man, men, mankind, Egyptians",
      "TranslationMetadata": {
        "PartOfSpeech": "collective noun",
        "PartOfSpeechCore": "noun",
        "Modifiers": ["collective"],            // optional
        "Domains": ["body"],                    // optional
        "SenseNumber": 1,                       // optional (only on H-split)
        "DictionaryName": 2,                    // 0=Lexicon 1=Dickson 2=Vygus 4=Faulkner
        "Page": 163,                            // Faulkner only
        "IndexOnPage": 8,                       // Faulkner only
        "Notes": "..."                          // optional
      },
      "translation_html": "<b>...</b>",         // optional (Faulkner)
      "Citations": [                            // optional
        {
          "abbreviation": "Sin.",
          "source": "Sinuhe",
          "location": "B70",
          "raw": "Sin. B70",
          "volume": "IV",                       // optional
          "corpus_file": "SinuheTrB.txt",       // optional
          "location_parts": {"witness": "B", "numbers": [70]}
        }
      ],
      "RelatedWords": [                         // optional (Faulkner canvas blocks)
        {"mdc": "D60-X1:N35a", "transliteration": "wabwt", "gloss": "..."}
      ],
      "SeeAlso": ["other_word"],                // optional (q.v. links)
      "Determinatives": ["F51"],                // optional (det. <sign> annotations)
      "Uncertain": true                         // optional (translation contains "(?)")
    },
    ...
  ]
}
```

Key facts:

- 45,492 entries
- 60,630 translations across them (an entry can have multiple
  translations from different source dictionaries)
- POS coverage: 99.84% (`PartOfSpeech` field is populated)
- 13,817 citations across 48 source texts
- 9,466 distinct transliterations have at least one phonetic-only
  writing (those are the playable-word set)

### 4.2 GardinerSigns vs ManuelDeCodage vs Res

Three views of the same hieroglyph sequence:

- `GardinerSigns` — space-separated sign codes: `Q3 X1 N1`.
- `ManuelDeCodage` — JSesh-style notation with structural operators:
  `Q3-X1:N1` (`-` = horizontal sequence, `*` = grouped pair,
  `:` = vertical stack).
- `Res` — RES (Revised Encoding Scheme) for the project's
  JavaScript renderer. Mostly identical to MdC but with sign-name
  normalizations and explicit `[sep=...]` spacing hints.

**For game logic, use `GardinerSigns`.** It's the canonical
space-separated list. The other two are for rendering.

### 4.3 Case-of-letter conventions

Gardiner sign codes are uppercase by convention: `A1`, `G17`. **The
"Aa" prefix** (for unclassified signs in Gardiner's table) is written
as `Aa1` in res_signinfo.js but historically as `AA1` in this
project's GardinerSigns/ManuelDeCodage. Same for variant suffixes:
`Y1v` (signinfo) vs `Y1V` (dictionary).

When matching dictionary signs against signinfo, **normalize**:
- `AA<num>[suffix]` → `Aa<num>[suffix.lower()]`
- `<letter><num><suffix>` → `<letter><num><suffix.lower()>`

This is done in `classify_signs.py:normalize_sign_to_signinfo()` and
in `build_game_material.py:norm_sign()`. Reuse those helpers.

### 4.4 DictionaryName codes

- 0 = Lexicon (OpenGlyph, parsed via Morris Franken dataset)
- 1 = Dickson (Paul Dickson, 2006)
- 2 = Vygus (Mark Vygus, 2012 and 2018)
- 4 = Faulkner (*Concise Dictionary of Middle Egyptian*, 1962)

(3 was reserved but never used.)

When building a deck, **"sources" count is a good attestation signal**:
words documented in all 4 dictionaries are more reliable choices than
words only in Vygus, which contains some idiosyncratic spellings.

---

## 5. Sign classification (`sign_classification/`)

Generated by `classify_signs.py`. Two indexes you'll use most:

### 5.1 signs_by_phonetic_class.json

```json
{
  "uniliteral": {
    "X1": {
      "count": 16254,
      "primary_mnemonic": "t",
      "description": "flat loaf"
    },
    ...
  },
  "biliteral": { ... },
  "triliteral": { ... },
  "4plus": { ... }
}
```

Counts are occurrences in `Entries2.json`'s `GardinerSigns`. Use these
to choose how many copies of each sign to include in a sign deck.

### 5.2 signs_logogram.json

```json
{
  "A1": {"count": 2089, "description": "seated man"},
  "D40": {"count": 2027, "description": "forearm with stick"},
  ...
}
```

A sign appears here if its `res_signinfo.js` entry has a `Log.` tag.
The same sign can appear in both `signs_logogram.json` and
`signs_by_phonetic_class.json` (the role depends on context — `A1` is
the logogram for `s` "man" AND the determinative for masculine names).

### 5.3 signs_determinative.json / signs_use_as_variant.json / signs_phonetic_marker.json / signs_phonetic_determinative.json / signs_numeric.json

Same structure. Filter signs by functional role.

### 5.4 signs_unclassified.json

Signs used in `Entries2.json` that aren't in `res_signinfo.js` — mostly
Vygus's extended numerical codes like `A100`, `A282`, `Z2D`. These have
no standard Gardiner mapping and no Unicode glyph; the project's
website falls back to bitmap PNGs for them. **Avoid these signs in
game decks unless you also produce bitmap art.**

---

## 6. The playable word files (`words/`)

One JSON file per playable word, grouped by shortest-phonetic-spelling
length. A "playable word" is a distinct transliteration that has at
least one writing whose signs, after removing determinatives and
plural/dual/ideogram markers (Z1/Z2/Z3/Z4 and variants), are entirely
phonetic (uniliteral / biliteral / triliteral / quadriliteral).

### 6.1 File schema

```json
{
  "transliteration": "pr",
  "english_glosses": ["go forth", "house", ...],
  "shortest_sign_count": 2,
  "difficulty_tier": "easy",
  "point_value": 1,
  "primary_pos": "verb",
  "all_pos": ["verb", "noun"],
  "sources": ["Dickson", "Faulkner", "Lexicon", "Vygus"],
  "spellings": [
    {
      "signs": ["Q3", "D21"],
      "sign_count": 2,
      "annotated": [
        {"sign": "Q3", "mnemonic": "p", "class": "uniliteral", "description": "stool"},
        {"sign": "D21", "mnemonic": "r", "class": "uniliteral", "description": "mouth"}
      ]
    },
    {
      "signs": ["Q3", "D21", "O1"],
      ...
    }
  ]
}
```

### 6.2 Filename convention

`<safe_translit>.json` where `safe_translit` is the transliteration
with `/` replaced by `-or-`, spaces replaced by `_`, and a few unsafe
filename chars stripped. Collisions get a numbered suffix:
`pr.json`, `pr__2.json`, `pr__3.json` (rare).

### 6.3 Bucket folders

| Folder | Words | Notes |
|---|---:|---|
| `1_sign/` | 779 | Trivial; single-sign words. Often the logogram-alone case. |
| `2_sign/` | 1,376 | Easy starter words. |
| `3_sign/` | 2,239 | Common short words. |
| `4_sign/` | 2,266 | Solid mid-tier. |
| `5_sign/` | 1,423 | Challenging. |
| `6_sign/` | 756 | Hard. |
| `7_plus_sign/` | 627 | Expert / impractical for play. |

### 6.4 Point values

```python
POINT_VALUES = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7, 6: 10, 7: 15, 8: 20, 9: 25, 10: 30}
```

Tier names map to:

```python
TIER_NAMES = {1: "trivial", 2: "easy", 3: "medium-easy", 4: "medium",
              5: "medium-hard", 6: "hard", 7: "expert"}
```

---

## 7. The starter deck (`deck.json`)

A single self-contained JSON with three "deck" sub-arrays.

### 7.1 Schema

```json
{
  "name": "Middle Egyptian Hieroglyphic Card Game — Starter Set",
  "version": "1.0",
  "generated_from": "Entries2.json",
  "summary": { ... counts ... },
  "configuration": {
    "ruleset_version": "8.10",
    "starting_hand_size": 8,
    "hand_limit": 12,
    "points_to_win_by_player_count": {"2": 8, "3": 7, "4": 6},
    "endgame": "equal_turns_round",
    "spelling_match": "multiset",
    "draw_choices": {
      "market_size": 5,
      "blind_draw": "draw 2, keep 1, discard 1 face-up",
      "discard_take_min_players": 3
    },
    "word_draw": "draw 2 word cards, keep 1, bottom the other",
    "word_mulligan": "once per player per game ... flip your player marker",
    "recycle": "instead of playing signs, discard any 2 signs and draw 2",
    "one_sign_spellings_stripped": true,
    "steal": "complete opponent word in one continuous play only",
    "first_player_gift_signs": 0,
    "point_values_by_sign_count": {"1": 1, "2": 1, ...}
  },
  "sign_deck": [
    {
      "card_id": "sign_X1",
      "type": "phonetic",
      "phonetic_class": "uniliteral",
      "sign_code": "X1",
      "mnemonic": "t",
      "description": "flat loaf",
      "usage_in_word_pool": 8452,
      "copies": 4
    },
    ...
  ],
  "logogram_deck": [
    {
      "card_id": "log_A1_rHw",
      "type": "logogram",
      "sign_code": "A1",
      "word_transliteration": "rHw",
      "word_english": ["comrades"],
      "description": "seated man",
      "copies": 1,
      "effect": "Instantly completes the matching word card."
    },
    ...
  ],
  "word_deck": [
    {
      "card_id": "word_Hpt_2",
      "type": "word",
      "transliteration": "Hpt",
      "english_glosses": ["oar", "embrace", "take in ones hand"],
      "shortest_sign_count": 2,
      "difficulty_tier": "easy",
      "point_value": 1,
      "primary_pos": "noun",
      "valid_spellings": [
        ["P8", "X1"],
        ["V28", "Q3", "X1"],
        ...
      ],
      "sources": ["Dickson", "Faulkner", "Lexicon", "Vygus"]
    },
    ...
  ]
}
```

### 7.2 Sign deck composition (v8.10 core build)

Current build: **168 unique sign cards, 349 total copies**
(26 uniliterals, 79 biliterals, 50 triliterals, 13 quadriliterals+).
Uniliterals get multiple copies; multi-consonant signs mostly 1 copy.
Note that for production the embedded sign deck is advisory — the
printed product uses `base_sign_library.json` (§20).

The "top by usage" ordering uses `usage_in_word_pool` which counts how
many distinct playable words use the sign. Including more copies of
high-usage signs and fewer of niche ones is the simplest balance
heuristic.

### 7.3 Logogram deck (47 cards)

Logogram-word pairs whose target words are present in the word deck
(the v4 lesson — logograms are picked AFTER the words). Each card is
single-purpose: it only completes the one word listed.

### 7.4 Word deck (165 cards)

Tier breakdown (v7 scaled picks, no tier 6):

| Tier | Sign count | Cards |
|---|---:|---:|
| trivial | 1 | 23 |
| easy | 2 | 29 |
| medium-easy | 3 | 32 |
| medium | 4 | 43 |
| medium-hard | 5 | 38 |
| hard | 6 | 0 (dropped in v7) |
| expert | 7+ | 0 (deliberately excluded) |

Selection criterion: within each tier, words are sorted by
**attestation strength** (number of source dictionaries containing the
word, more = better) then by gloss brevity (a one-word English meaning
is more game-friendly than a paragraph). The starter deck favors
words documented in all 4 source dictionaries.

---

## 8. The rules (`rules.md`)

The user-facing rule book. Covers components, setup, the v8 turn
structure (draw from market/discard/blind-draw-2 → play → score →
discard), stealing, logogram use, scoring table, win condition
(scaled points + equal-turns endgame), and four optional advanced
rules: **determinative bonus**, **honorific transposition** (placing
divine/royal elements first when arranging a completed word),
**phonetic complement bonus**, **variant credit**. Educational notes
explain the writing system for non-Egyptologists.

Two rules were codified in the v8.7 documentation sync (§23):
**multiset spelling match** (completion checks the set of signs, not
their order — the rule every simulator run since v2 actually used) and
**steal-in-one-continuous-play** (partial building on an opponent's
card is explicitly forbidden, matching the engine). The undefined
"trading card shield" mention was removed.

The rules text is embedded in `build_game_material.py` as `RULES_MD`
and written out by `write_rules()`. **If you hand-edit
`game_material/rules.md`, sync the same text back into `RULES_MD`** or
the next builder run will clobber your edits. (As of the v8.7 sync the
two are identical.)

When you ship a new deck, refresh the rules page only if the new deck
changes a mechanic. The base rules are deliberately deck-agnostic.

---

## 9. Designing expansion decks

This is the most likely thing a future user will ask you to do. Here's
the playbook.

### 9.1 Choose a theme

Examples of themed decks that the data can support:

- **Religion deck** — words tagged with `domain = "divinity"` or
  containing god-name elements: `nTr` "god", `Hr` "Horus", `imn`
  "Amun", `wsir` "Osiris", `Hwt-nTr` "temple", etc.
- **Warfare deck** — `mSa` "army", `nxt` "victory", `aHa` "battle",
  `xrw` "enemy", `pDt` "bow", etc. POS verb + military domain.
- **Body parts deck** — entries with `Domain = "body"` (2,311 in
  Entries2.json). `tp` "head", `Hr` "face", `Hat` "neck", `ib` "heart".
- **Kinship & society deck** — `s` "man", `Hmt` "woman", `sA` "son",
  `mwt` "mother", `it` "father", `nb` "lord", `Hm` "servant".
- **Verbs of motion deck** — POS verb + Domain "motion" or det. D54
  (legs walking).
- **Animal deck** — `Domain = "animal"` / "bird" / "fish".
- **Food & drink deck** — `Domain = "food"`.
- **Common-life deck** (no specialized vocab) — top 300 most-
  attested words across all 4 sources, capped at 4 signs.
- **Difficulty-tiered packs** — "Beginner" (only 2-3 sign words),
  "Master" (only 5-6 sign words).

### 9.2 Build a word selector

The standard pattern is a small Python script that:

1. Loads `Entries2.json`.
2. Loads the `words/` per-word files (or rebuilds the playable-word
   index directly).
3. Applies a theme filter using POS, Modifiers, Domains, English
   gloss keywords, Determinatives, or sign-presence rules.
4. Sorts the filtered list by attestation strength + brevity.
5. Picks N per difficulty tier.
6. Adjusts the sign deck so every sign needed for those words is
   present in at least one copy (cross-check `valid_spellings`).
7. Adds relevant logograms (any logogram whose word is in the new
   word selection).
8. Writes a new `deck_<theme>.json`.

A starter template:

```python
import json
from collections import Counter, defaultdict
from pathlib import Path

DICT = Path("dictionary")
WORDS = DICT / "game_material" / "words"

# 1. Load every per-word file
def load_words():
    words = {}
    for f in WORDS.rglob("*.json"):
        with open(f) as fh:
            w = json.load(fh)
        words[w["transliteration"]] = w
    return words

words = load_words()
print(f"Available playable words: {len(words):,}")

# 2. Theme filter — pick words with Domain "body"
themed = [w for w in words.values()
          if w.get("primary_pos") == "noun"
          and any("body" in (g or "").lower() for g in w.get("english_glosses", []))]
# Or use POS / Domain from the original Entries2.json for more precision.

# 3. Sort by attestation + brevity
themed.sort(key=lambda w: (-len(w["sources"]),
                            len(w["english_glosses"][0]) if w["english_glosses"] else 999,
                            w["transliteration"]))

# 4. Pick balanced tiers
tier_caps = {2: 30, 3: 30, 4: 40, 5: 30, 6: 20}
picks = []
counts = Counter()
for w in themed:
    n = w["shortest_sign_count"]
    if n not in tier_caps:
        continue
    if counts[n] < tier_caps[n]:
        picks.append(w)
        counts[n] += 1

# 5. Collect signs needed
needed_signs = Counter()
for w in picks:
    for sp in w["spellings"]:
        for s in sp["signs"]:
            needed_signs[s] += 1

# 6. Now assemble the sign deck: include every needed sign with copies
#    proportional to its usage in this theme.
```

### 9.3 Themed deck recipes

#### Religion deck

```python
RELIGION_KEYWORDS = {"god", "goddess", "divine", "temple", "shrine",
                     "altar", "offering", "prayer", "festival",
                     "priest", "ritual", "soul", "ka", "ba", "akh"}
themed = [w for w in words.values()
          if any(any(k in g.lower() for k in RELIGION_KEYWORDS)
                 for g in w["english_glosses"])]
```

Then verify: words involving divine names are also natural picks
(`imn`, `wsir`, `ra`, `Hr`, `DHwty`, `pth`, `ist`, `nbt-Hwt`).

#### Body parts deck

For high accuracy, query `Entries2.json` directly for
`Domains` containing "body":

```python
entries = [json.loads(l) for l in open("dictionary/Entries2.json")]
body_translits = {
    e["Transliteration"]
    for e in entries
    for t in e.get("Translations") or []
    if "body" in ((t.get("TranslationMetadata") or {}).get("Domains") or [])
}
themed = [words[t] for t in body_translits if t in words]
```

This is more accurate than English-keyword filtering because the
Domain tags are curated.

#### Verbs of motion deck

```python
themed = [w for w in words.values()
          if w.get("primary_pos") == "verb"
          and ("motion" in any_domain(w) or
               "D54" in any_determinative(w))]
```

You'll need to look up the entries' `Determinatives` field for
the second condition.

#### Beginner deck

Just constrain to short, well-attested words:

```python
themed = [w for w in words.values()
          if w["shortest_sign_count"] <= 3
          and len(w["sources"]) >= 3
          and w.get("primary_pos") in {"noun", "verb", "adjective"}]
```

### 9.4 Sign-deck right-sizing

After picking words, **inspect what signs the chosen words actually
need**. Use `Counter` to count sign usage across all `valid_spellings`,
then build the sign deck so:

- Every uniliteral that appears at least once has at least 2 copies
  (3-4 for the top 10 most-used).
- Every biliteral / triliteral that appears has 1 copy.
- Add 1-2 "wild" extras of the most common signs for play balance.

A themed deck of 100 word cards typically needs 60-90 sign cards.

### 9.5 Logogram deck for a theme

For each picked word, check if there's a documented logogram for it
(in `signs_logogram.json` × `res_signinfo.js`'s Log. tags). If yes,
include the logogram as an instant-completion card. Keep these rare
(<10% of word count is a safe rule).

### 9.6 Reuse the build_game_material.py infrastructure

The existing script has helpful pieces:

- `safe_filename(translit)` — sanitizes a transliteration for use as
  a filename.
- `norm_sign(s)` — normalizes case for signinfo lookup.
- `build_word_index(...)` — rebuilds the playable-word set from
  Entries2.json.
- `build_deck(...)` — the deck assembler; can be parameterized for
  themes.

You can either copy-paste relevant functions or refactor them into a
shared `game_utils.py` module if you find yourself reaching for them
repeatedly.

---

## 10. Scripts reference

All scripts live in `dictionary/`. In rough order of build dependency:

| Script | Purpose |
|---|---|
| `crossfill_vygus.py` | Original POS cross-fill from Vygus to other sources |
| `parse_faulkner.py` | Merge Faulkner per-page JSONs + extract POS from HTML |
| `morphology_pass.py` | Initial gloss/morphology POS rules |
| `fix_multiword_morph.py` | Revert bad multi-word feminine/plural taggings |
| `cleanup_low_effort.py` | POS truncation fixes, DictionaryName format, whitespace |
| `medium_effort_cleanup.py` | HTML separation, citation extraction, VariantOf, dedup |
| `fix_citations.py` | Fix Urk. IV / Adm. citation regex bugs |
| `build_citation_index.py` | Build CitationIndex.json (inverted citation index) |
| `split_pos.py` | Split composite POS into Core/Modifiers/Domains |
| `generate_res.py` | Port C# MdC→RES converter and fill Res field |
| `collapse_res.py` | Drop ResAuto/ResSource after Res ratification |
| `cleanup_a_through_f.py` | Prose POS rescue, case-only sibling fix, etc. |
| `cleanup_g_through_k.py` | RelatedWords extraction, sub-gloss split, q.v., corpus_file |
| `normalize_translit_mdc.py` | Middle-dot, j→i, dot-run normalization |
| `cleanup_1_through_9.py` | Determinatives, Uncertain flag, location_parts, AttestationCount |
| `drop_comparewith.py` | Drop the bibliographic-cf. field |
| `unify_id_schema.py` | Convert Faulkner Id → MongoDB ObjectId form |
| `fill_pos_gaps.py` + `_round2/3/4/5.py` | Five iterative POS-gap-filling rounds |
| `classify_signs.py` | Build sign_classification/ outputs |
| `build_game_material.py` | Generate per-word files + rules + deck |

**Most important for future deck work**: `classify_signs.py` (to
regenerate sign classifications if `Entries2.json` changes) and
`build_game_material.py` (the deck builder you can copy from).

---

## 11. Common tasks / recipes

### Regenerate everything after Entries2.json changes

```bash
cd dictionary
python3 classify_signs.py            # refresh sign_classification/
python3 build_game_material.py       # refresh game_material/words/ and deck.json
```

### Inspect a specific word

```bash
# Find files for transliteration "nfr" (good)
find game_material/words -name "nfr*.json"
cat game_material/words/3_sign/nfr.json
```

### Find all words containing a specific sign

```python
import json
from pathlib import Path
for f in Path("game_material/words").rglob("*.json"):
    with open(f) as fh:
        w = json.load(fh)
    for sp in w["spellings"]:
        if "Y5" in sp["signs"]:    # words using the mn biliteral
            print(w["transliteration"], "→", w["english_glosses"][0])
            break
```

### Make a "first 100 words" beginner pack

```python
import json
from pathlib import Path
beginners = []
for f in sorted(Path("game_material/words/2_sign").glob("*.json")):
    with open(f) as fh:
        w = json.load(fh)
    if len(w["sources"]) == 4 and w.get("primary_pos") in {"noun", "verb"}:
        beginners.append(w)
        if len(beginners) >= 100:
            break
# Write a deck file using the same schema as deck.json
```

### Generate a printable card sheet

The deck.json fields map cleanly onto a card template. A simple
Python + ReportLab script can render each card as a PDF:

- Card face: hieroglyph image (need a font that has the sign), the
  transliteration, the English meaning, the difficulty tier, the
  point value. For word cards, optionally list 1-2 valid spellings.
- Card back: a consistent design (e.g., a hieroglyph border pattern).

The font assets are in `MiddleEgyptian/fonts/`:
`NewGardiner.ttf`, `ExtendedGardiner.ttf`, `HieroglyphicAux.ttf`.

For browser-based prototyping, the project's `res_render.js` library
renders RES strings to canvas — that's the most authentic rendering
path.

### Find words a player could complete with their current hand

(For an AI assistant in a digital game, given a hand of sign cards:)

```python
def can_complete(hand, valid_spellings):
    hand_remaining = list(hand)
    for spelling in valid_spellings:
        h = list(hand)
        ok = True
        for sign in spelling:
            if sign in h:
                h.remove(sign)
            else:
                ok = False
                break
        if ok:
            return spelling
    return None
```

---

## 12. Glossary

| Term | Meaning |
|---|---|
| Aleph (A) | Glottal stop, transliterated capital A. The "alif" sound. |
| Ayin (a) | Pharyngeal voiced consonant, transliterated lowercase a. |
| Biliteral | A sign representing two consonants (e.g. `Y5` *mn*). |
| Determinative | Silent semantic classifier at the end of a word. |
| Gardiner sign list | Standard classification of hieroglyphs by category (A-Z + Aa). |
| GardinerSigns field | Dictionary's space-separated sign-code field. |
| Logogram | A sign that IS an entire word (e.g. `N5` = *ra* "sun"). |
| MdC (Manuel de Codage) | Compact notation with operators `-`, `:`, `*`. |
| Mnemonic | Conventional transliteration of a sign's phonetic value. |
| Phonetic complement | A redundant uniliteral confirming a biliteral's reading. |
| Phonetic determinative | A sign that's both phonetic and a classifier. |
| RES | Revised Encoding Scheme; the project's chosen rendering format. |
| Sportive writing | Playful/unusual sign substitutions (rare). |
| Transliteration | Romanized consonant-only form of an Egyptian word. |
| Triliteral | A sign representing three consonants (e.g. `R8` *nTr*). |
| Uniliteral | A sign representing one consonant (e.g. `G17` *m*). |
| Yodh (i) | Reed-i consonant, transliterated lowercase i (sometimes j). |

---

## 13. Notes & quirks to be aware of

- **The original `Entries.json` must not be modified.** All cleanup
  work goes to `Entries2.json`. If anything looks wrong in
  `Entries2.json`, suspect a regression in one of the cleanup scripts.

- **`Keywords.json` is stale.** It was built against the original
  `Entries.json` and references entry IDs that may no longer exist in
  `Entries2.json` (834 entries were converted from `Id` to `_id`
  format). Treat `Keywords.json` as legacy.

- **The 11 F37Aa / Aa21A edge cases.** During the Res-field
  generation, 11 entries had their curated Res field disagree with the
  ported converter's output (the curator's normalization dropped the
  variant suffix; the converter lowercases it). The collapse step
  trusted the converter, so the on-disk Res values reflect the
  converter, not the curator. This is documented and intentional.

- **POS coverage is 99.84% (95 nulls remaining).** The residual nulls
  are entries where the gloss itself says `(unknown)` or
  `{used in connection with ...} (unknown)` — meaning the dictionary
  author marked the word's meaning as irrecoverable. Leaving POS null
  on these is honest.

- **The `j` vs `i` outlier.** One entry (`wab qnit`, originally
  `wab qnjt`) had a `j` instead of `i`; this was normalized. Any
  future ingest of Vygus or Faulkner data should re-check.

- **`AA` vs `Aa` is a cross-field divergence.** `ManuelDeCodage` uses
  lowercase `Aa15`, while `GardinerSigns` and the dictionary use
  uppercase `AA15`. The classify_signs.py / build_game_material.py
  normalize at lookup time. Don't try to "fix" it in the source
  fields — both forms are intentional.

- **`Z1` is overloaded.** It's used as:
  - The numeral "1".
  - The "ideogram marker" placed after a logogram to confirm the
    logographic reading.
  - A dual marker in some contexts (rare).
  In game logic it's stripped along with plural markers, but a serious
  expansion might handle each role separately.

- **Faulkner entry pages are 17 through 419.** If you're cross-
  referencing back to the printed book, those are the valid page
  numbers; anything else indicates a parser bug.

---

---

## 14. Content filtering (family / mature / archaeological)

Some Middle Egyptian signs and words depict sexual anatomy that's
inappropriate for a family card game. The deck builder supports three
content modes via `--content-filter`:

| Mode | Behavior | Use case |
|---|---|---|
| `family` (default) | Excludes words whose ONLY spellings use sexual-anatomy signs, and words whose English glosses match an explicit-terms pattern. Strips blocked signs from the sign deck and logograms. | Default starter deck; family game nights; schools; retail. |
| `mature` | Includes everything. Used for the After Dark expansion. | Adult party game expansion. |
| `archaeological` | Includes everything but adds `content_warning: "mature"` to affected cards. | Academic/research use; print-on-demand where the consumer chooses what to print. |

### Blocked signs (family mode)

The seven sign codes that visually depict sexual anatomy:

```python
FAMILY_BLOCKED_SIGNS = {
    "D27", "D27a",  # breast (small/large)
    "D52", "D52a",  # phallus
    "D53", "D53a",  # liquid issuing from phallus
    "F45", "F45a",  # uterus
    "F51", "F51a",  # piece of flesh / vulva
}
```

Two other signs (`N41` "well with ripple of water", `G11` "image of
falcon") have "uterus" or "breast" mentioned somewhere in their
res_signinfo.js description but are VISUALLY innocuous and are NOT
blocked. The filter operates on visual depiction, not academic
classification.

### Blocked gloss terms (family mode)

Regex of explicit English stems that mark a word as mature:

```
phallus | penis | testic* | scrotum | ejaculat* |
vulva | vagina | uterus | pubic | pudenda |
copulat* | intercourse | fornicat* | masturbat* |
breast (whole word) | nipple | teat
```

### Homophone handling caveat

Some innocuous-meaning words like `it` "father" / "barley" are
ALSO Egyptian homophones for explicit terms in the dictionary
sources. Because the family filter checks ALL recorded glosses, these
words get excluded from family decks even though their primary meaning
is innocent. They appear in the After Dark deck instead, where their
explicit meaning is the point.

This is acceptable collateral: better to over-filter for safety than
risk a child looking up "it" and finding "penis" as a secondary
meaning. If you want a word back in the family deck specifically,
manually add it to a `FAMILY_OVERRIDE_ALLOW` set.

### Two physical products

| Product | Card count | Source |
|---|---:|---|
| **Hieroglyph Quest: Core Set** | 165 word + ~50 logogram + ~350 sign = 565 cards | `build_game_material.py` (default) |
| **Hieroglyph Quest: After Dark** | 55 word + ~7 logogram + ~284 sign = 346 cards | `build_adult_deck.py` |

After Dark is intentionally smaller — there are only 97 mature-content
words in the playable pool, so 55 cards (one print sheet) is a
natural product size.

---

## 15. Playtesting findings (v1 through v6)

Six rounds of simulator-driven tuning took the game from broken to
playable. The journey is worth knowing because it surfaces several
design lessons that apply to future expansions.

### Headline progression

| Version | Balance score | Victory rate | Median turns | Logograms/game | Steals/game |
|---|---:|---:|---:|---:|---:|
| v1 (baseline) | 42 | 17% | 800 (max) | 0.00 | 0.01 |
| v2 (5 mechanics) | 59 | 90% | 379 | 0.00 | 0.22 |
| v3 (peek + logos in pile) | 62 | 95% | 239 | 0.0+ | 0.16 |
| v4 (logo selection rewrite) | 61 | 93% | 281 | 0.17 | 0.44 |
| v5 (first-player gift) | 63 | 96% | 279 | 0.31 | 0.62 |
| v6 (tier rebalance) | 65 | 94% | 279 | 0.34 | 0.65 |

### Key design lessons from the data

**1. Egyptian writing is inherently completion-starved.**
With 9,000+ playable words and specific sign requirements for each,
even moderate-complexity words (3–4 signs) are hard to complete from
random draws. The original rules (strict spelling order, no trash,
small hand) produced 17% victory rate. Loosening to **multiset
matching, trash-and-draw, larger starting hand (8), and lower point
target (10)** brought victory rate above 90%.

**2. Peek-and-wait is a strategy trap.**
Letting players see the top of the deck (peek) and pass to wait for
useful cards seemed strategically rich but actually punished thoughtful
players: greedy beat balanced 84% in v2. Replacing passive `peek` with
active `look_and_take` (peek, take one, discard one) fixed this —
balanced started beating greedy 60%.

**3. Logograms are useless if their target words aren't in the deck.**
v1–v3 picked logograms based on sign popularity. Only 9 of 30
logograms targeted words actually present in the word deck. Result:
logograms fired <0.05 times per game. v4 fixed this by picking
logograms AFTER the word deck, ensuring every logogram has a reachable
target. Plus the mnemonic-as-logogram expansion (treating biliterals
whose phonetic value IS a word as logograms for that word) doubled
the available pool.

**4. First-player advantage is real and small.**
With random tie-breaking, seat 0 still won ~58% in 2-player
balanced-vs-balanced. Reason: more turns to claim mid-deck logograms.
Fix: deal seat 0 +2 sign cards at start. Brings seat balance to
±2%.

**5. Hard-tier (6-sign) words are cosmetic.**
At 30 cards, hard-tier words clogged the deck but rarely completed
(needed too many specific signs). v6 cut hard tier from 30 → 12 cards
and reallocated the slots across medium tiers. Top completions
shifted to 2–3-sign words like `qmAw` "throwstick" (103×).

**6. Smaller decks have higher engagement.**
The deck-size sweep (150/175/200/225/250/275/300 word cards at 2/3/4
players) showed a clear cliff: dead-card rate jumps from 1% at 165 to
46% at 300 for the 2-player case. The winning size:

| Deck size | Avg balance | Avg dead-card rate |
|---:|---:|---:|
| 150 | 63 | 12% |
| **165 (optimal)** | **67** | **1%** |
| 175 | 67 | 18% |
| 300 (original) | 60 | 36% |

**165 word cards is the production deck size**. It also happens to
fit exactly 3 print sheets at the 55-cards-per-sheet print standard,
which makes the print job clean.

### Multi-player findings

The game scales beautifully from 2 → 4 players:

- Logograms per game scale linearly with player count (more active
  word cards on the table → more logogram-target overlap).
- Steals per game scale linearly too (more opponents to steal from).
- Seat-position balance is within ±3% at every player count.
- Random×4 only finishes 36% of games (random players cannot
  coordinate enough to reach 10 points). Real human players play
  more like the balanced agent — this is just a lower-bound check.

---

## 16. Simulator usage reference

### Setup

```bash
cd dictionary
python3 build_game_material.py            # regenerate decks + word files
python3 playtest_simulator.py --help      # single-matchup tools
python3 run_full_playtest.py --help       # multi-matchup runner
python3 deck_size_sweep.py --help         # deck-size optimizer
```

### Common runs

**Quick check after editing the deck:**
```bash
python3 playtest_simulator.py --games 200 --agents balanced,balanced --out check.md
```

**Full balance audit for a release candidate:**
```bash
python3 run_full_playtest.py --games 500 --player-counts 2,3,4 --max-turns 800
```
(Since the v8.7 sync, `run_full_playtest.py` defaults to the v8.6
scaled points targets — 2p=8, 3p=7, 4p=6. Pass `--points-to-win N`
only to force a flat target for historical comparisons.)

**Try a different deck size:**
```bash
python3 build_game_material.py --deck-size 200
python3 run_full_playtest.py --games 200 --player-counts 2,3,4
```

**Generate an After Dark deck:**
```bash
python3 build_adult_deck.py --deck-size 55
```

### Agents

| Agent | Behavior |
|---|---|
| `random` | Tries to complete own word; occasional logogram play; rarely trashes |
| `greedy` | Always complete own word if possible; steal any opponent word if possible; cycle aggressively |
| `balanced` | Greedy + uses `look_and_take` actively; smart discards prefer to keep useful signs |

### Engine knobs (`GameConfig`)

| Knob | Default | Notes |
|---|---:|---|
| `starting_hand` | 8 | Cards each player starts with |
| `hand_limit` | 12 | Forces discard at end of turn |
| `points_to_win` | 7 | Victory threshold (drivers scale: 2p=8, 3p=7, 4p=6) |
| `max_turns` | 1000 | Safety cap; games above this score-wins |
| `draw_n` | 2 | v8: blind draw pulls 2, keep 1, discard 1 face-up |
| `word_draw_n` | 2 | v8.8: word draws pull 2, keep 1, bottom the other |
| `word_mulligan` | 1 | v8.9: free active-word replacements per player per game |
| `dead_logogram_exchange` | 0 | v8.8 lever, tested and rejected; 0 = off |
| `score_rebound_draw` | 0 | v8.9 catch-up lever, tested and rejected |
| `steal_victim_draws` | 0 | v8.9 catch-up lever, tested and rejected |
| `underdog_token` | False | v8.9 catch-up lever, runner-up; 2p only |
| `market_size` | 5 | v8: face-up sign market beside the deck |
| `discard_take_enabled` | True | v8: top of discard takeable... |
| `discard_take_min_players` | 3 | ...but only at 3+ players |
| `equal_turns_ending` | True | v8.7: finish the round after target crossed |
| `allow_trash_and_draw` | True | v8.10: the printed "recycle" rule (discard 2, draw 2) |
| `allow_look_and_take` | False | v8.10: removed — never printed; superseded by market |
| `look_n` | 3 | Peek size for the (now off) look_and_take |
| `logogram_ratio` | 15 | One logogram per N sign cards in mixed pile |
| `first_player_gift_signs` | 0 | v8.7: zeroed — scaled points does the job |

### Reproducibility

All simulations are deterministic. Given the same seed and config,
the same results emerge every time. The base seed for the published
balance reports is `1000`. Each game uses `seed + game_index`.

---

## 17. Recommended product strategy

Based on data + market reality:

### Core Set: 165 cards (the optimum)

- Sells at $25–35 print-on-demand or $15–20 at scale
- Family-friendly content filter
- Self-contained game; no other product needed to play
- Print job: ~11 sheets at 55 cards/sheet (clean fit)

### Modular booster expansions: 165 cards each

The recommended product family is **modular boosters** (Option C from
the categories discussion): each themed deck is self-contained AND
designed to mix with other decks for variety. A player who owns 1 deck
plays alone; a player who owns 3 mixes them for "Festival Mode" with a
larger word pool.

Suggested release roadmap:

| # | Theme | Source words available | Deck size |
|---|---|---:|---:|
| 1 | Core Set (Daily Life) | 4,500 untagged + most-attested | 165 |
| 2 | Gods & Temples | 442 divinity | 165 |
| 3 | Beasts of the Nile | 556 animal + 239 bird + 81 fish | 165 |
| 4 | Body & Healing | 782 body + 19 medical | 165 |
| 5 | Kings & Court | 1,082 title | 165 |
| 6 | The Land of Egypt | 418 location + 306 boat + 151 astronomy | 165 |
| 7 | Hieroglyph Quest: After Dark | 97 mature-content | 55 (one sheet) |

Total available material: **9,445 playable words**, enough for ≈ 57
themed decks of 165 cards. After 7 decks you'd still have 92% of the
pool in reserve.

### Mix Mode rules addendum

**SUPERSEDED (historical):** Mix Mode now lives in rules.md as a
provisional section with per-player-count targets (13/11/10 at 2
decks, 16/14/12 at 3). The block below is the original v1-era
proposal, kept for history:

```
MIX MODE (multiple decks combined)
  2 decks combined: target 15 points, hand limit 14
  3+ decks combined: target 20 points, hand limit 16, max turns 1200
  Shuffle all word decks together; shuffle all sign decks together;
  shuffle all logogram piles together.
```

The simulator validated that 2-deck combinations (330 cards) still
score balance 60–66.

---

## 18. Updated scripts reference (additions since v1.0)

| Script | Purpose |
|---|---|
| `playtest_simulator.py` | Core game engine, agent strategies, single-matchup analysis |
| `run_full_playtest.py` | Multi-matchup runner, supports `--player-counts 2,3,4` |
| `deck_size_sweep.py` | Parameter sweep across deck sizes for any player count |
| `build_adult_deck.py` | Generate the After Dark expansion deck (mature content) |
| `build_game_material.py` | Main deck/rules/per-word builder, now with `--content-filter` and `--deck-size` flags |
| `build_expansion_deck.py` | Themed expansion builder (`--theme`, `--all`), auto-relax tier targets |
| `build_topped_up_sign_deck.py` | Regenerates the canonical base sign library (§20) |
| `playtest_variants.py` | v8.8 candidate tests (word draw-2, strip 1-sign, logogram exchange) |
| `playtest_catchup.py` | 2p catch-up candidates + first-scorer-wins metric (v8.9) |
| `playtest_cardcycle.py` | Rules-fidelity test of trash/look-and-take (v8.10) |
| `playtest_shared.py` | Race Mode (shared word pool + dredge) validation |
| `playtest_draft.py` | Standalone draft-mode sim (tested, shelved) |
| `playtest_coop.py` | Scribes Together difficulty-curve calibration |
| `playtest_expert.py` | Expert-agent evaluation / ruleset robustness check (§29) |

Build artifacts in `game_material/playtest_results/`:

| File | Contents |
|---|---|
| `MASTER_BALANCE_REPORT.md` | Latest cross-matchup analysis |
| `matchup_<NP>p_<agents>.md` | Detailed per-matchup report (one per cell) |
| `DECK_SIZE_SWEEP_REPORT.md` | Deck-size optimizer results |
| `raw_results.json` | Machine-readable stats |

---

---

## 19. Creating expansion decks (modular boosters)

The product family is built on Option C from the prior design
discussion: **each themed deck is self-contained AND mixable**. A
player who owns one deck plays alone; a player who owns several
shuffles them together for "Festival Mode" with a larger word pool.

### Shipping expansion decks

**v2 (current):** Twelve family-safe themed decks plus one adult expansion
live in `game_material/expansions/`. All share the canonical
`base_sign_library.json` for their sign deck (see §20).

**v1 (original 8 themes):**

| Slug | Name | Source domains |
|---|---|---|
| `core_daily_life` | Core Set: Daily Life | (untagged general vocab) |
| `gods_and_temples` | Gods & Temples | divinity, epithet, ritual, religious, ceremonial |
| `beasts_of_the_nile` | Beasts of the Nile | animal, bird, fish |
| `body_and_healing` | Body & Healing | body, medical, medicinal, bodily |
| `kings_and_court` | Kings & Court | title, royal |
| `the_land_of_egypt` | The Land of Egypt | location, locality, boat, astronomy |
| `pantheon_expanded` | Pantheon Expanded | divinity etc. (second pull) |
| `wild_egypt` | Wild Egypt | animal/bird/fish/flora/mineral (second pull) |

**v2 expansions (added after signs-in-base validation):**

| Slug | Name | Source domains |
|---|---|---|
| `builders_of_egypt` | Builders of Egypt | architecture |
| `markets_and_feasts` | Markets & Feasts | food |
| `houses_and_hearths` | Houses & Hearths | furniture |
| `threads_of_linen` | Threads of Linen | clothing |

**Mature expansion (18+):**

| Slug | Name | Source |
|---|---|---|
| `after_dark` | After Dark | the 97 mature-content words excluded by the family filter |

Each themed deck JSON is a complete `deck.json` (165 word cards + ~10–36
logograms + a sign deck), generated by the same builder that produces
the core deck. The schema is identical, so simulator, playtest scripts,
and printing tools work on any deck without modification. **In the v2
signs-in-base architecture, the embedded `sign_deck` in each expansion
file is advisory (it shows which signs that theme draws on); production
prints a single copy of `base_sign_library.json` instead of one sign
deck per box.** See §20.

### Generating an expansion deck

Two routes:

**Pre-defined theme** (from `THEMES` table in `build_expansion_deck.py`):

```bash
python3 build_expansion_deck.py --theme gods_and_temples
python3 build_expansion_deck.py --all          # regenerate all 8 at once
```

**Custom theme** (one-shot, no edits to the script):

```bash
python3 build_expansion_deck.py \
    --theme custom \
    --name "Magic & Amulets" \
    --domains magical,divinity,ritual
```

Custom themes use only the `--domains` filter (comma-separated set of
domain tags from `Entries2.json`'s `Domains` field). For more
elaborate filters (gloss keywords, exclusions, sign-presence), add a
new entry to the `THEMES` list in `build_expansion_deck.py`.

### Adding a new theme

Open `build_expansion_deck.py` and append to `THEMES`:

```python
{
    "slug": "magic_and_amulets",        # filename + ID
    "name": "Magic & Amulets",          # display title
    "description": "Spells, protection, and ritual objects.",
    "domain_set": {"magical", "ritual"},
    "gloss_keywords": [
        "amulet", "spell", "protection", "magic",
    ],
    "fallback_general": False,          # True only for the Core deck
    "exclude_from": None,               # or a slug to avoid duplicates
}
```

Then run `python3 build_expansion_deck.py --theme magic_and_amulets`.

**Best practices for theme design:**

1. **Domain set first, gloss keywords as backup.** Domain tags are
   curated; English keywords risk false positives. Use gloss keywords
   only to broaden a too-narrow domain match.

2. **Use `exclude_from` for "expanded" decks.** If you've already
   shipped a "Gods & Temples" deck and want a second religion deck,
   set `exclude_from: "gods_and_temples"` so the same gods don't
   reappear.

3. **Check the word pool first.** Before designing a theme, query:
   ```python
   from collections import defaultdict
   import json
   entries = [json.loads(l) for l in open("Entries2.json")]
   counts = defaultdict(int)
   for e in entries:
       for t in e.get("Translations") or []:
           for d in (t.get("TranslationMetadata") or {}).get("Domains") or []:
               counts[d] += 1
   for d, n in sorted(counts.items(), key=lambda x: -x[1]):
       print(f"{d}: {n}")
   ```
   You need ≥250 unique words for a 165-card deck after filtering and
   tier-balancing. Smaller pools can still work, but the deck-size
   sweep showed quality degrades when picks-per-tier scale below 80%.

4. **Verify with the simulator before printing.** Run
   `playtest_simulator.py` against the generated deck:
   ```bash
   cp game_material/expansions/magic_and_amulets.json game_material/deck.json
   python3 playtest_simulator.py --games 200 --agents balanced,balanced \
       --out magic_check.md
   ```
   Compare the balance score, victory rate, and logogram fire-rate
   against the published core-set numbers. Themed decks should land
   in the 60–70 balance range. If your deck scores below 50,
   investigate: the theme may be too narrow (not enough word
   variety) or too sign-clustered (always needs the same biliterals).

### Mix Mode rules

**Note:** the authoritative (provisional) Mix Mode text now lives in
rules.md; its targets scale the v8.6 per-player-count standards and
await post-v8.8 re-validation (see PLAYTEST_CHECKLIST.md). The block
below is the v8.6-era derivation:

```
MIX MODE
  Shuffle all word decks together into one word draw pile.
  Shuffle all sign decks together (with their multiple copies) into
    one sign draw pile.
  Shuffle all logogram decks together into the same sign draw pile
    (or as a separate "wild" draw pile, your choice).
  
  Adjust win conditions for larger combined decks:
    Player-count-scaled targets (v8.6); per-deck values for 1-deck play:
      2 players: 8 points  (hand limit 12)
      3 players: 7 points  (hand limit 12)
      4 players: 6 points  (hand limit 12)

    Mix Mode adds combined-deck multipliers on top of the per-player base:
      1 deck    × scale  (use the table above)
      2 decks   × 1.6    (e.g. 2p = 13, 3p = 11, 4p = 10), hand limit 14
      3 decks   × 2.0    (e.g. 2p = 16, 3p = 14, 4p = 12), hand limit 16
      4+ decks  × 0.5 per deck added (linear scaling), hand limit 16
```

The simulator validated 2-deck combinations remain in the balance 60–66
range. 3+ decks drift toward "looser" balance (still playable, just
less competitively tight).

### Sign-deck overlap when mixing

Each deck ships with its OWN sign-card pool biased to its theme. When
players combine decks, they accumulate duplicate copies of common
signs (X1 "t", M17 "i", N35 "n", etc.). This is intentional and
beneficial:

- More copies = faster draws of common letters
- Theme-specific signs (R8 god-sign in Gods deck, E1 cattle in Beasts
  deck) become available alongside their target words
- No need to remove duplicates — the larger draw pile is the point

Expected sign-card count when combining N decks of 165 words each:
roughly 300–360 × N total copies, ~170 unique signs (low new-unique
gain as N grows because the top 24 uniliterals appear in every deck).

### Inventory of available domains and pool sizes

From the v6 cleanup (current `Entries2.json` state):

| Domain | Playable words available | Suitable for ~N decks of 165 |
|---|---:|---:|
| title | 1,082 | 6 |
| body | 782 | 4 |
| flora | 732 | 4 |
| architecture | 673 | 4 |
| animal | 556 | 3 |
| food | 553 | 3 |
| furniture | 511 | 3 |
| divinity | 442 | 2 |
| clothing | 430 | 2 |
| location | 418 | 2 |
| boat | 306 | 1 |
| bird | 239 | 1 |
| mineral | 228 | 1 |
| astronomy | 151 | + mini-deck (~half size) |
| fish | 81 | combine with bird/animal |
| medical | 19 | combine with body |

Words with no Domain tag: **4,500** (general vocabulary, fills core
decks and untagged supplements). Total playable pool: 9,445 words.

**Estimated maximum themed-deck capacity** (with some word overlap
across themes): **36 decks** × 165 cards. Without overlap: **57
decks**. Either way you'll never run out of source material.

### Build artifacts on disk

```
game_material/
├── base_sign_library.json             # ★ CANONICAL sign deck (311 codes / 530 copies)
├── deck.json                          # Family-mode Core (default standalone build)
├── expansions/
│   ├── core_daily_life.json           # Same content as deck.json, in expansions/
│   ├── gods_and_temples.json
│   ├── beasts_of_the_nile.json
│   ├── body_and_healing.json
│   ├── kings_and_court.json
│   ├── the_land_of_egypt.json
│   ├── pantheon_expanded.json
│   ├── wild_egypt.json
│   ├── builders_of_egypt.json         # v2 theme (architecture)
│   ├── markets_and_feasts.json        # v2 theme (food)
│   ├── houses_and_hearths.json        # v2 theme (furniture)
│   ├── threads_of_linen.json          # v2 theme (clothing)
│   └── after_dark.json                # 18+ mature expansion (55 cards)
├── proposed_base_sign_deck.json       # 547-copy union-of-max (historical)
├── proposed_base_sign_deck_shrunk.json # 431-copy mean-of-containing (historical)
├── proposed_base_sign_deck_topped_up.json # 530-copy topped (promoted to base_sign_library)
├── words/                             # per-word JSON reference (9,466 files)
├── rules.md                           # core rules
├── PROJECT_GUIDE.md                   # this file
└── playtest_results/                  # simulator output (gitignored OK)
```

To validate an expansion before printing, swap it into `deck.json`
temporarily and run the playtest suite. The simulator is the cheapest
safety net you have — every found problem saves you from a print run
or a bad playtester reaction.

---

## 20. Signs-in-base architecture (v2)

The game launched with v1 architecture: each themed expansion was a
fully self-contained `deck.json` carrying its own ~330-copy sign deck.
Across the 10-product line that meant ~3,360 sign cards printed, ~65%
of which were duplicates of the same high-frequency phonetic carriers
(A1, N5, X1, etc.).

A multi-round simulator sweep validated a cleaner architecture:
**one shared sign library, themed expansions carry words + logograms
only.** That cuts the line's card count from 5,142 to roughly 2,290
(~56% reduction) without sacrificing balance, victory rate, or
dead-card health.

### The canonical sign library

**File:** `game_material/base_sign_library.json`
**Size:** **260 unique Gardiner codes, 479 total card copies (v2.1)**

**How it was built (in four rounds of analysis):**

1. **Union-of-max baseline (547 copies).** For every sign code that
   appeared in any of the 8 v1 expansion sign decks, take the maximum
   copy count seen across any single deck. Guarantees the unified deck
   supports every v1 theme at its tuned demand. (See
   `proposed_base_sign_deck.json`.)

2. **Shrink by mean-of-containing (431 copies).** For each sign code,
   set copies to the rounded mean of its copy count across the themes
   that contain it. Scale down uniformly if total exceeds 400. Faster
   game cycle, ~3-point balance drop on average vs. per-theme. (See
   `proposed_base_sign_deck_shrunk.json`.)

3. **Top up for future coverage (530 copies / v2.0).** Layer two
   additions onto the shrunk deck:
   - For every sign required by family-safe words *not* in the v1
     expansions, add 1 copy (or 2 if it blocks ≥10 unused words).
   - For under-supplied high-demand signs (present at <4 copies,
     used by ≥200 unused words), bump to 4 copies. This fixed Y1
     (1→4) and W11 (3→4).

4. **Dial back to ~480 copies (v2.1, current).** Skip rare-blocking
   additions: only add a sign if it unblocks ≥10 unused family-safe
   words. This drops 51 codes that each only blocked 1–9 future words,
   trading 2.5 pp of coverage (99.99% → 97.5%) for a 9% smaller deck
   (530 → 479 copies). Y1/W11 top-ups retained. Generator:
   `build_topped_up_sign_deck.py --min-blocking-threshold 10`. The
   v2.0 file remains at `proposed_base_sign_deck_topped_up.json` for
   reference, and is promoted to `base_sign_library.json` by:
   ```bash
   cp proposed_base_sign_deck_topped_up.json base_sign_library.json
   ```

**Coverage:** **97.5% of family-safe words** in the dictionary can be
spelled from the v2.1 library. The ~2.5% of unreachable words each
require a sign that is in the dictionary's sign reference but doesn't
appear in any current expansion — they can still be included in
future themes by shipping a small supplementary sign pack with that
expansion box. Words requiring D27 (breast) or D52 (penis) are
intentionally absent from the family deck and routed to After Dark.

**Generator script:** `build_topped_up_sign_deck.py` — regenerates the
topped-up deck from the shrunk deck and the current dictionary.

### Auto-relax tier targets

Themes drawn from sparse vocabulary domains (e.g. clothing) sometimes
can't fill the standard per-tier word picks. `build_expansion_deck.py`
now includes `auto_relax_picks()`, which:

1. Counts per-tier word availability in the filtered themed pool
   (family-safe spellings only when filter is "family").
2. Caps each tier at availability; sums shortfall.
3. Pushes shortfall to the **nearest** tier with surplus, preferring
   `+1` (one step harder), then `-1`, then `+2` etc. — minimizing
   theme difficulty drift.
4. Annotates the deck with `tier_auto_relaxed: true` and
   `tier_relax_notes: [...]` for traceability.

The relax mechanism fired on Threads of Linen during the v2 build
(tier-5 short by 2, pushed to tier 6), keeping the deck at the full
165-card target.

### Playtest results validating the architecture

Side-by-side balance scores across the 8 v1 themes (all 50-game,
balanced-agent, 2p/3p/4p averaged):

| Architecture | Avg balance | Avg dead-card | Median turns | Health flags |
|---|---:|---:|---:|---:|
| Per-theme tuned (v1) | 62.4 | 14.4% | ~262 | 0 |
| Unified 547-copy | 60.1 | 14.7% | ~426 | 0 |
| Shrunk 431-copy | 62.3 | 14.6% | ~346 | 0 |
| Topped-up 530-copy (v2.0) | 62.0 | 14.6% | ~370 | 0 |
| **Topped-up 479-copy (v2.1, canonical)** | **60.3** | **14.6%** | **~360** | **0** |

The v2.1 canonical deck performs within ~2 balance points of per-theme
tuning. Games run ~100 turns longer than per-theme (about 20–25 minutes
of real-world play) — the cost of centralization, paid once.

Future themes built from the long tail of the dictionary stay within
balance health (≥55) and within dead-card health (≤20% average) on
all four v2 expansions playtested.

### Print-line math comparison

| Architecture | Per box | Total across 13 products | Reduction |
|---|---:|---:|---:|
| Per-theme self-contained (v1) | ~530 cards | 5,142 | baseline |
| Shrunk unified (431-copy base) | 190 + 431 | 2,194 | −57% |
| Topped-up v2.0 (530-copy base) | 190 + 530 | ~2,290 | −55% |
| **Topped-up v2.1 (479-copy base, canonical)** | **190 + 479** | **~2,240** | **−56%** |

The v2.1 base costs **48 more cards than the shrunk version**
and **~2,900 fewer cards than per-theme**. You keep most of the print
savings, support 97.5% of the family-safe dictionary out of the box,
and never need to ship a per-expansion sign deck again. The remaining
2.5% of words requiring uncommon signs are handled by per-expansion
sign supplements (typically 5–15 extra cards in any future booster
that goes deep into a niche).

### Production guidance

1. **One physical sign library per player.** Print `base_sign_library.json`
   as the foundation product (or include it with the starter box).
2. **Each expansion box ships words + logograms only** (~190 cards).
   The embedded `sign_deck` in expansion JSON files is reference data
   for the design pipeline — production strips it.
3. **Mix Mode** (combining multiple themed decks) now just means
   shuffling word + logogram decks together. The same sign library
   serves any combination.
4. **After Dark** ships its own small slate of family-blocked signs
   (D27/D52/F45/etc.), included with that 18+ box. Production should
   not combine those signs into the canonical library.

### When future expansions exceed the library

If a future theme pulls heavily from the ~6% of words requiring signs
not yet in the library, regenerate the topped-up deck:

```bash
python3 build_topped_up_sign_deck.py
cp game_material/proposed_base_sign_deck_topped_up.json \
   game_material/base_sign_library.json
```

The script reads every family-safe word in the dictionary and adds any
missing signs needed by any of them. As the dictionary grows or new
themes drift the demand profile, the library can grow incrementally
without breaking existing expansions.

---

## 21. v7 ruleset: shorter games

After adopting the signs-in-base architecture (§20), the production
playtest revealed games ran ~90 minutes at the 15-second-per-turn
estimate. Two changes were tested and adopted as defaults in v7:

### Change 1: drop tier-6 (six-sign) words from the deck

Tier-6 words were 6 signs each, the hardest to assemble, and were the
main source of game-length stalls. Players would sit on partially-built
tier-6 cards while the game crawled forward. The slots they occupied
(~7 in a 165-card deck) were redistributed proportionally across tiers
1-5. The new baseline tier sizes are `{1: 42, 2: 52, 3: 58, 4: 79, 5: 69}`
(sums to 300 before scaling) instead of the old
`{1: 40, 2: 50, 3: 56, 4: 76, 5: 66, 6: 12}`.

### Change 2: lower `points_to_win` from 10 to 7

Average word point value is ~2.4, so a 10-point target requires
~4 completions per player. Cutting to 7 means ~3 completions — a 30%
reduction that translates directly into shorter games. The simulator's
default and the `playtest_simulator.py --points-to-win` default were
both updated.

### Combined impact (35-game balanced-agent playtest across all 12 family expansions)

| Metric | v2.1 / 10-pt / tier-6 | v7 / 7-pt / no tier-6 | Change |
|---|---:|---:|---:|
| Median game length (avg) | ~368 turns | ~211 turns | **−43%** |
| Estimated wall-clock at 15s/turn | ~92 min | ~53 min | **−39 min** |
| Avg balance score | 60.3 | 67.5 | +7.2 |
| Avg victory rate | 92% | 97% | +5 pp |
| After Dark balance | 54.6 (flagged) | 61.9 (OK) | +7.3 |

### Side effect: dead-card rate metric needs recalibration

Dead-card rates rose from ~26% to ~42% because shorter games mean
fewer of the deck's 165 cards see play. The old 20% ceiling was tuned
for ~90-minute games. With ~50-minute games, the appropriate ceiling
is probably ~40-50% — or better, recalibrate to "fraction of cards
seen across 3 consecutive games" (the variety players experience in a
typical session). The play experience itself isn't worse; the metric
just needs to track what matters.

### Re-running builds

All 12 family expansion JSONs and `after_dark.json` were regenerated
with the v7 tier distribution. To regenerate any expansion after
adjusting code:

```bash
python3 build_expansion_deck.py --all      # regenerate all 12 family
python3 build_adult_deck.py                # regenerate after_dark
```

Custom themes ship the same way; the tier-6 drop is now built into
`scaled_picks()` in `build_game_material.py`.

### Mix Mode targets (updated for v7 — since superseded by the
provisional table in rules.md, pending post-v8.8 re-validation)

| Decks combined | Target points | Hand limit |
|---:|---:|---:|
| 1 | 7 | 12 |
| 2 | 11 | 14 |
| 3 | 14 | 16 |
| 4+ | 4 per deck | 16 |

These scale roughly linearly with combined word pool size, preserving
the per-deck "complete 3 things to win" feel regardless of how many
boxes are on the table.

---

## 22. v8 ruleset: draw choice, face-up market, face-up discard

After §21 (the v7 point-and-tier changes that took game length from ~92
to ~53 minutes), three further mechanical changes were tested. Two
were adopted; one was tested and reverted.

### Change 1 (adopted): draw 2 keep 1

`GameConfig.draw_n` defaults to 2. The engine pulls 2 cards from the
top of the sign deck, the agent scores each for usefulness against the
active word (logogram for active word = 100, needed sign = 50,
uniliteral = 5, other = 1), keeps the highest-scoring, and discards
the rest to the sign discard pile face-up.

Simulator result: ~15% game-length reduction, ~6-point balance bump
across the 12 family expansions, no health flags introduced.

### Change 2 (adopted): face-up sign market of 5

`GameConfig.market_size` defaults to 5. At game start, 5 sign cards are
dealt face-up from the deck alongside the draw pile. Each turn the
agent can take ONE specific market card (in lieu of the blind draw-2)
when a card visible in the market is useful for their active word. The
market refills from the top of the deck immediately after a take.

Simulator sweep at sizes 0/3/5/7 showed all variants land within ~1
balance point and ~10 turns of each other — the difference is mostly
human-feel (a visible decision each turn replaces blind-draw frustration).
Size 5 was chosen as the slight optimum for measurable speed (169 vs.
180 turns at no-market) and as a clean table-space fit (one tidy row
alongside the deck).

### Change 3 (adopted with a 2-player gate): face-up discard, top card takeable

The sign discard pile is kept face-up. Its top card is always visible
and available as a third draw source. Each turn the agent's draw step
weighs: top of discard, any of the 5 market cards, or blind draw-2 from
the deck — and picks the most useful (or falls back to blind if nothing
visible is useful).

**2-player gate:** at 2p the discard pile is dominated by the one
opponent's throwaways, which are reliably useful for the receiving
player. The full-discard-take playtest produced 87-99 balance scores
at 2p — clearly broken (one player runs away with the lead). At 3p+
the pile is more chaotic and the take is fair.

The simulator enforces this with `discard_take_min_players=3` (the
default). Below that threshold the engine ignores the discard-take
option even when `discard_take_enabled=True`. Rules text in
`rules.md` documents the restriction as the 2-player variant.

| Player count | Available draw sources |
|---|---|
| 2 | market, blind draw-2 |
| 3+ | market, top of discard, blind draw-2 |

`GameConfig.discard_take_enabled` defaults to True; the gate above
prevents the 2p problem automatically. To disable entirely (e.g. for
historical comparison runs), pass `--no-discard-take`.

### Change tested but rejected: logograms as wildcards

Letting an unused logogram in hand substitute for one missing sign
during a word completion was tested in two variants:

| Variant | Avg balance | Avg game length | Logograms/game |
|---|---:|---:|---:|
| Off (v8 baseline) | 73.7 | ~180 turns | 0.47 |
| Free wildcards (cap 1/completion) | 92.4 | ~93 turns | 3.77 |
| Option A (−1 pt per wildcard) | 84.7 | ~136 turns | 2.13 |

Wildcards dominated the game economy even with cost. The AI agents'
"use it whenever it helps" behavior caused runaway 2p games (balance
87-99 across all decks), and 4× the logogram play rate broke the
deliberate scarcity of those cards. Reverted; `logograms_as_wildcards`
defaults to False.

### Change 4 (adopted): scale points-to-win by player count

Flat `points_to_win = 7` left 2-player games unbalanced (89% balance —
the better player wins ~95% of the time). The fix is per-player-count
scaling: **2p = 8, 3p = 7, 4p = 6**. Longer 2p clock gives the trailing
player a chance to catch up; lower 4p clock keeps the highest-player-count
game under 40 minutes.

| Players | Points to win | Median turns | Estimated wall-clock | Balance |
|---:|---:|---:|---:|---:|
| 2 | 8 | 163 | ~41 min | **75.6** |
| 3 | 7 | 116 | ~29 min | 86.3 |
| 4 | 6 | 138 | ~35 min | 83.0 |
| **avg** | — | **139** | **~35 min** | **81.6** |

The 2p balance improvement (89.3 → 75.6) is the single largest
parameter-tuning win in v8 — squarely in the healthy 60-80 band where
the per-theme baseline lived. 4p got a free balance bump (79.0 → 83.0)
and a 13-turn speedup. 3p is unchanged by definition.

Implementation: in `playtest_all_expansions.py`, the test driver picks
the appropriate target per player count. The simulator's
`GameConfig.points_to_win` itself remains a single field — at table
play the rules sheet tells players the right number; the driver
applies it.

### Change 5 (adopted): equal-turns endgame round

When a player crosses the target score, finish out the current round
so every player has had the same number of turns. Highest score at end
of round wins. Tie-breakers: most completed words → fewest signs in
hand → earlier seat.

The simulator measured an essentially identical balance score with
equal-turns on vs. off (81.1 vs. 81.6 average across player counts)
because the AI scores are uniformly distributed, so seat-0 advantage
doesn't appear strongly in the metric. But the rule still ships
because the perception of fairness at the table dominates the
measured fairness: tabletop players consistently complain about being
"robbed of their last turn" when an opponent triggers an instant win.
The equal-turns ending eliminates that complaint at near-zero
mechanical cost (+1.3 turns of average game length).

`GameConfig.equal_turns_ending` defaults to True. Pass
`--instant-win` to the playtest script to test against the v8.6
behavior.

### Change 6 (adopted): drop the first-player gift

The first-mover compensation (`first_player_gift_signs`) was carried
forward from v5 when seat-0 advantage was a real concern. The v8.6
points scaling does the same job better, and the gift sweep at v8
settings revealed it was actually making the 4p case *worse*:

| `first_player_gift_signs` | Avg balance | 4p balance |
|---:|---:|---:|
| 0 | 80.6 | 76.2 |
| 2 (old default) | 81.6 | 83.0 |
| 4 | 83.3 | 87.5 |

The gift amplifies whatever leader-runaway dynamic the higher player
counts already have. Removing it (`first_player_gift_signs = 0`) gives
the cleanest 4p balance and the simplest setup ("every player draws 8
signs to start").

### Combined v8 turn structure

The new turn (per `rules.md`):

```
Draw — choose ONE source:
  • Take 1 face-up card from the market (5 visible), OR
  • Take the top card of the sign discard pile, OR
  • Draw 2 face-down from the deck, keep 1, discard 1 face-up

Play sign cards (own word, or steal opponent's)
Complete any word that matches
Discard down to hand limit 12
```

### v8 combined impact

Going from v7 baseline (10-pt, includes tier-6) through to v8 (7-pt,
no tier-6, draw-2, market-5, discard-take):

| Metric | v2.1 (per-theme) | v7 | v8 production |
|---|---:|---:|---:|
| Median game length (avg) | ~368 turns | ~211 | ~170 |
| Estimated wall-clock at 15s/turn | ~92 min | ~53 min | **~42 min** |
| Avg balance score | 60.3 | 67.5 | 73-74 |
| Avg victory rate | 92% | 97% | 99% |
| Health flags | several | none | none |

The game now sits in standard card-game playtime territory while
preserving every aspect of the modular signs-in-base architecture.

---

## 23. v8.7 documentation & tooling sync (July 2026)

A consistency pass that brought every shipped artifact in line with
the rules the simulator had actually been validating. No mechanics
were re-tuned; the changes close documentation/implementation gaps.

### Rules text (`rules.md`)

1. **Multiset spelling match is now official.** The printed rules had
   said signs must be laid "in the order shown," but the engine has
   checked completion as a sign multiset since v2 — every published
   balance number assumed it. The rules now say order does not matter,
   with an educational note (scribes arranged signs into aesthetic
   blocks; order was flexible in practice).
2. **Steals are one continuous play.** Turn-structure step 2 used to
   permit playing signs "onto an opponent's word card (toward a
   steal)" while the steal section forbade partial building. Resolved
   in favor of the engine's behavior: a steal must complete the whole
   word in one continuous play; signs are never left on an opponent's
   card.
3. **The undefined "trading card shield" was removed.**
4. The honorific-transposition optional rule was reworded (order is
   now free, so the +1 rewards declaring the divine element and
   placing it first when arranging the finished word).

### Deck files

- `deck.json` was restored to the family-mode Core build (a Wild
  Egypt playtest swap had been left in place; the `*.swap_backup*`
  files in `game_material/` are the leftovers and are safe to delete).
- Every deck's embedded `configuration` block is now **self-describing
  v8.7**: `ruleset_version`, hand 8/12, `points_to_win_by_player_count`
  {2:8, 3:7, 4:6}, `spelling_match: "multiset"`, draw choices
  (market 5, draw-2-keep-1, discard-take at 3p+), one-play steal,
  equal-turns endgame, no first-player gift. Written by
  `build_game_material.py:build_deck()`; all 12 family expansions +
  After Dark were regenerated with it.
- `RULES_MD` inside `build_game_material.py` was synced to the fixed
  `rules.md`, so regenerating material no longer clobbers the current
  rules.

### Playtest tooling

- `run_full_playtest.py` now defaults to the v8.6 scaled points
  targets per player count instead of a flat `--points-to-win`.
- `MASTER_BALANCE_REPORT.md` was regenerated against the restored core
  deck: 500 games × 11 matchups × 2/3/4 players, seed 1000, max 800
  turns, full v8.7 ruleset. Headline (same-agent matchups): balance
  94–99, victory rate ≈100%, median turns 84–132 for competent agents
  (the pre-sync report, run at flat 10 points under pre-v8 mechanics,
  showed 61–69 balance and 210–477 median turns). Higher balance
  scores largely reflect the shorter v8 games maxing out the
  game-length component of the composite score.

---

## 24. v8.8 ruleset: word draw choice, logogram-only instant completions

Two mechanics were candidate-tested (500 games/cell, balanced agents,
2p/3p/4p, seed 1000 — full data in
`playtest_results/VARIANT_PLAYTEST_REPORT.md`) and adopted; two other
candidates were resolved without a rules change.

### Adopted 1: draw 2 word cards, keep 1

Whenever a player draws a word card (setup, after completing, after
being stolen from), they draw **2**, keep one, and return the other to
the **bottom** of the word deck. Simulator: balance and game length
unchanged, but **steals nearly double** (1.88 → 3.46/game at 4p) and
**logogram completions rise ~60%**, because players hold words their
hands can actually progress and the table rotates faster. This is the
single cheapest interactivity win found since the market.

Engine: `GameConfig.word_draw_n` (default now 2; set 1 for pre-v8.8
comparison runs). Selection heuristic: keep the word whose easiest
spelling has the fewest signs missing from the current hand.

### Adopted 2: strip 1-sign spellings from word cards

Word cards no longer list 1-sign phonetic spellings; **logogram cards
are the only single-card completions**, protecting their "lottery win"
identity. Only ~23 cards per deck (the trivial tier) were affected;
simulator confirmed the change is balance-neutral (Δ −0.0, +5 turns).
Words whose ONLY documented spelling is a single sign are now skipped
by the word-card picker entirely (they're logograms in all but name).
Printed point values and tier assignments are deliberately unchanged.

Builder: implemented in `build_game_material.py:build_deck()`; all 13
family decks + After Dark regenerated. Deck configs carry
`"one_sign_spellings_stripped": true`.

### Tested and rejected: dead-logogram exchange

"Trade a logogram whose word is nobody's active word for 2 sign
draws" was tested in 2-draw and 1-draw forms. Both degenerate: agents
exchanged ~30 logograms/game (a quarter of all turns), logogram
completions **fell ~40%**, games ran ~15 turns longer. The valve
cannibalizes the "yes!" moments it exists to protect. The lever
remains in the engine (`GameConfig.dead_logogram_exchange`, default 0)
for future bounded variants (e.g. once per player per game) if human
playtests still show logogram frustration.

### Resolved without simulation: the trade rule

The open-ended "trade with another player by mutual agreement" rule
was cut from rules.md. It had never been modeled in the simulator (all
published numbers already describe a trade-free game) and it was an
unbounded collusion/kingmaking channel at 3+ players.

### v8.8 master audit

`MASTER_BALANCE_REPORT.md` regenerated (300 games × 11 matchups ×
2/3/4p, seed 1000): same-agent competent matchups at balance 97-99,
victory ≈100%, median turns in the same band as v8.7. No health flags.

---

## 25. v8.9 ruleset: the word mulligan (2-player catch-up)

### The problem, correctly measured

The old worry ("2p leader wins 85%+") predated v8.8 and was based on
the composite balance score, which never actually measured
leader-runaway. v8.9 added the right metric — **first-scorer-wins %**:
how often the seat that scores the game's FIRST word goes on to win
(50% = perfect comeback health at 2p; 1/N ideal at N players). It's
now a permanent `GameRecord` / `analyze()` field and a column in the
master report.

True v8.8 baseline at 2p: **60.1%** — a real but modest runaway, much
of the historical problem having already been fixed by the v8.8 word
draw choice.

### Design constraint: table-trackability

Catch-up triggers like "when trailing by 3+ points" die at a real
table — nobody re-sums scored piles every turn, and a player who must
*claim* a handicap feels like they're begging. Candidates were
restricted to event-triggered rules ("a word was just scored") or
physical-token state, never score arithmetic.

### Candidates tested (1,000 games/matchup, 2p, seed 1000)

| Candidate | First-scorer wins | Median turns | Skill check* |
|---|---:|---:|---:|
| baseline (v8.8) | 60.1% | 120 | 58.0% |
| scoring rebound (opp. scores → draw 1) | 59.5% | 120 | 59.4% |
| steal salve (stolen from → draw 2) | 60.0% | 118 | 58.1% |
| **word mulligan (once/game)** | **53.5%** | 128 | 59.7% |
| Eye of Horus token | 56.6% | 108 | 59.0% |
| rebound + mulligan | 57.4% | 126 | 57.6% |

*Skill check = balanced agent's win rate vs greedy; catch-up must not
compress it toward 50%.

Full data: `playtest_results/CATCHUP_PLAYTEST_REPORT.md`; driver:
`playtest_catchup.py`.

### Adopted: word mulligan

**Rule:** once per player per game, as a free action on your turn,
replace your active word — signs you'd played on it return to hand,
the old word goes to the bottom of the reserve, draw a new word with
the usual draw-2-keep-1. **Tracking:** each player uses a coin (or any
two-faced object) as their player marker, placed heads-up at setup and
flipped when the mulligan is spent.

Why it won: 2p runaway is mostly the *stuck-word state*, not leader
speed — so fixing the stuck word beats feeding the trailer cards. The
rule is symmetric (both players get it, so it isn't charity), needs
zero knowledge of who's behind, and improved skill expression
slightly. Draw-based compensation (rebound, salve) measurably did
nothing: one extra sign card isn't enough fuel.

Engine: `GameConfig.word_mulligan = 1` (default; agents mulligan when
their easiest spelling is missing 3+ signs). Rejected levers remain
available at 0: `score_rebound_draw`, `steal_victim_draws`,
`underdog_token`.

### v8.9 master audit

All 14 decks regenerated at `ruleset_version: 8.9`;
`MASTER_BALANCE_REPORT.md` regenerated (300 games × 11 matchups ×
2/3/4p). First-scorer-wins: **55% at 2p** (ideal 50), **38% at 3p**
(ideal 33), **33% at 4p** (ideal 25) — comeback health is good at
every player count. Mulligans/game: 1.6 (2p) to 2.8 (4p), i.e. most
players spend theirs, confirming it reads as a tool rather than a
concession. Balance 98-99 for competent mirrors, victory ≈100%, median
turns 105-140.

---

## 26. Race Mode (official variant, shipped in rules.md)

The "race, not theft" structural variant, playtested and shipped as an
optional mode rather than a replacement for the classic game.

**Rules (see rules.md "Race Mode"):** no personal word cards and no
mulligan; 5 word cards sit face-up in a central "commission board"
that anyone may complete from hand. Turn action: complete any board
word, play a logogram targeting a board word, or **dredge** (bottom
one board card of your choice and refill — the row-refresh valve and
the denial play). No steals. Draw step, scoring, scaled targets, and
equal-turns endgame unchanged.

**Why dredge is mandatory:** without it, 2p games stall once the easy
words clear (shared4 hit the 800-turn cap at median; shared5 ran 464
turns vs classic's 140). With dredge: 188 turns at 2p, logogram fire
rate doubles, skill expression near classic (balanced-vs-random 83% vs
86%).

**Why it's a variant, not the default:** even with dredge it beats
classic on no measured axis (2p ~35% longer, 3p first-scorer-wins 54%
vs 44%). Its advantages are unmeasurable but real: no steal social
friction, no personal-word frustration, fully open information.

Engine: `GameConfig.shared_word_pool` (row size, 0 = classic) and
`GameConfig.shared_dredge` (default True — the printed Race Mode
includes dredge; set False only for historical no-dredge comparison
runs); agent policy in
`playtest_simulator.shared_pool_decision()`; driver
`playtest_shared.py`; data in
`playtest_results/SHARED_POOL_PLAYTEST_REPORT.md`.

---

## 27. v8.10: the recycle rule (rules/engine fidelity closed)

The last of the rules/engine gaps found in the v8.7 sync family. The
engine's agents had always been granted two actions the printed rules
never mentioned: `trash_and_draw` (v2: discard 2 useless signs, draw
2) and `look_and_take` (v3: peek top 3, take 1, discard 1). Every
published balance number assumed them.

**Measured** (`playtest_results/CARD_CYCLE_PLAYTEST_REPORT.md`, driver
`playtest_cardcycle.py`): trash was not a side mechanic but the game's
de facto pacing engine, firing on nearly every non-scoring turn
(94-138×/game); the exact printed game ran 2.2× longer (294 vs 132
median turns at 2p). Look-and-take contributed nothing to pacing; it
was the balanced agent's entire measured skill edge over greedy, and
for humans it's superseded by the v8 market + draw-2-keep-1.

**Adopted (v8.10):**

1. **Recycle is now a printed rule** — "instead of playing signs this
   turn, you may discard any 2 signs and draw 2." Added to the classic
   turn structure and to Race Mode's action list.
2. **Look-and-take removed from engine defaults**
   (`allow_look_and_take = False`). The simulator now plays exactly
   the printed game.

**v8.10 master audit** (300 games × 11 matchups, seed 1000): 2p median
144 turns (vs 132 with the hidden actions — the cost of dropping
look-and-take is 12 turns), first-scorer-wins 53% at 2p / 39% at 3p /
38% at 4p, victory 100% everywhere, balance 95-99 on competent
mirrors.

**Known artifact:** with look-and-take gone, the greedy and balanced
agents are now behaviorally identical (smart discard ordering is
shared), so mixed greedy-vs-balanced matchups report identical rows.
The simulator currently has only two real skill tiers: random and
competent. Building a genuinely stronger agent (search-based, or
denial-aware in Race Mode) is the natural next simulator investment.

---

## 28. Scribes Together (co-op / solo mode, shipped in rules.md)

The second official variant, and the project's solo mode. Tested in
`playtest_coop.py` (300 games/cell); data in
`playtest_results/COOP_MODE_PLAYTEST_REPORT.md`.

**Rules:** classic v8.10 mechanics unchanged; one team score; steals
reframed as assists (identical engine path); the sign deck may only be
dealt through twice (one reshuffle), then one final dry round and the
game ends — win only if the team total reached the target. Unlimited
table talk. Works at n_players=1.

**Calibration:** team score at deck death has median 17 (solo), 15
(2p), 21 (3-4p); games run ~175-180 total turns at every player count
because the deck is the clock. Printed difficulty tiers
(≈90/60/30% win): 9/15/19 points at 1-2 players, 13/19/25 at 3-4.
Random agents score 12-14 vs balanced 15-21, so play quality matters.
Agents aren't clock-aware (they recycle even when the deck is nearly
dead), so human teams should slightly beat these curves — the printed
tiers err forgiving, the right direction for a co-op.

**Engine:** `GameConfig.coop_mode` and
`GameConfig.coop_sign_deck_passes` (default 2). Win-rate-for-any-target
comes free from one unreachable-target batch per player count, since
agents aren't target-aware.

Sim-vs-table note: the drafting structural candidate was also tested
(`playtest_draft.py`, `DRAFT_MODE_PLAYTEST_REPORT.md`) and **shelved**:
exact-multiset word targets are incompatible with pick-and-pass
drafting (0.4-0.8 completions per game, 50-68% ties; carryover and
bigger boards only reached ~2 words/game). Sushi Go works because
every card scores; this game's cards mostly don't.

---

## 29. The expert agent, and what it says about the skill ceiling

The "natural next simulator investment" from §27 was built:
`ExpertAgent` (`AGENTS["expert"]`), with value-maximizing completion
choice (own word vs steals vs logograms by points), easiest-spelling
draw targeting (the `smart_draw` engine hook — classic agents only
ever target `valid_spellings[0]`), and denial-aware discards against
the next player's visible word when the discard top is takeable (3p+).
Driver: `playtest_expert.py`; data:
`playtest_results/AGENT_EXPERT_REPORT.md`.

**Result: expert beats balanced by only ~+3 pp at 3p and nothing at
2p/4p, and its mirror matchup shows zero degeneracy** (same game
length, steal rate, and seat fairness as the balanced baseline).

Two conclusions worth keeping:

1. **The ruleset is robust** — a deliberately ruthless policy found no
   exploit. Good evidence before a print run.
2. **Skill saturates at basic competence.** The big step is random →
   competent (~83% win at 2p); above that, outcomes are healthily
   luck-tempered. That's the Sushi Go profile the game aims for, and
   it means the v8.10 greedy/balanced collapse cost the simulator
   little: the gradient up there was always shallow. Real additional
   headroom would need card counting across recycles and multi-turn
   search — a research project with diminishing returns for a
   tabletop game.

The human playtest checklist was refreshed in the same pass
(PLAYTEST_CHECKLIST.md): v8.10 numbers, mulligan/recycle/word-draw
watch items, Race Mode and Scribes Together session sections, a Mix
Mode retune flag, and an updated notes template.

---

## 30. v8.11: the optional advanced rules got their components

An audit found two of the four printed optional rules unplayable for
lack of materials. Both gaps are now closed across all 14 decks
(details + scoring data:
`playtest_results/OPTIONAL_RULES_PLAYTEST_REPORT.md`).

**Determinative bonus:** every deck now ships a `determinative_deck`
(24 unique classifier cards, top 8 doubled, 32 copies), and word cards
carry `appropriate_determinatives` (up to 3, restricted to the side
pool; 103-138 of 165 words covered per deck). Mechanics were made
concrete in rules.md: face-up pool, claim one matching card per
completion for +1, supply-limited. **Play to 10/9/8 targets with this
rule** — uncompensated it shortens games ~a third (the sim measured
4.3-5.6 bonus points/game); +2 targets restore baseline pacing and
comeback health.

**Honorific transposition:** word cards containing a divine/royal sign
carry `honorific_transposition: true` and the signs themselves carry
`honorific: true` (R8, N5/N6, G7, C-category, A40-46, M23, L2, S1-7;
see `HONORIFIC_SIGNS` in the builder). ~1 point/game; no target
change.

**Data plumbing:** `build_word_index()` now derives each word's
documented determinatives from its raw writings (they were previously
stripped and discarded); per-word files in `words/` carry the full
list. Engine: `WordCard.determinatives` / `.honorific`,
`GameConfig.determinative_bonus` / `.honorific_bonus` (default off).

**Incidental bug fixed:** `write_word_files` lost 23 case-colliding
word files per build on case-insensitive filesystems (macOS) and
created suffixed duplicates when rerun into a non-empty tree.
Collision tracking is now casefolded and the tree is cleared before
regeneration; 9,466 records = 9,466 files, verified.

---

**End of project guide v13 (v8.11: complete optional-rule components,
three modes, three-tier agent roster).** With this file plus `Entries2.json`,
`res_signinfo.js`, and the `game_material/` outputs, an AI can:

- Generate themed expansion decks at any size with `--content-filter
  family|mature|archaeological` and `--deck-size N`, including
  auto-relaxed tier targets for sparse-vocabulary themes.
- Run playtests against the canonical base sign library or against
  any historical proposal for architectural comparison.
- Move from a research playtest to a production design without
  re-deriving the signs-in-base reasoning each time.

Six rounds of simulator-driven tuning produced the v6 ruleset; three
additional rounds (shrunk, hand-10, shrunk-with-tier-relax) produced
the v2 architecture. Any future change to the rules or the sign
library should be re-validated by re-running the relevant playtest
report — the data has now caught design problems nine times in a row
that human intuition would have missed.

Welcome aboard.
