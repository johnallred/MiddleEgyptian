"""
Round 2 of POS gap-filling on Entries2.json.

Round 1 (fill_pos_gaps.py) brought coverage from 91.3% to 97.4%.
Three residual issues remain:

  Q1. Glosses like "duty (of someone)" or "wealthy man" weren't caught
      because the previous gloss heuristic looked at the full first comma-
      bounded chunk. Stripping parenthesized tails first turns "duty (of
      someone)" into "duty" (a clean single noun).

  Q2. Two-word glosses of the form ADJECTIVE + NOUN (e.g. "wealthy man",
      "noble heir", "former state") are nouns — the noun is the head.

  Q3. Pronoun glosses like "I, me, my" / "you, your" / "he, him, his" are
      a recognizable cluster and should be tagged `pronoun`.

  Q4. PartOfSpeechCore lags PartOfSpeech (3,528 vs 1,553 null). When P1
      and P2 copied a compound label like "noun plural of ky" or
      "stative past tense" from a sibling, the recipient ended up with
      PartOfSpeech set but Core still null. Re-derive Core from the
      filled PartOfSpeech using the existing splitter vocabulary plus
      the EXTENDED_COMPOUND_RESCUE table from round 1.
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# Improved gloss extraction
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")
_PAREN_TAIL = re.compile(r"\s*\([^)]*\)\s*$")


def first_gloss_clean(text: str) -> str:
    """First comma-bounded gloss with any trailing parenthesized clarifier removed."""
    s = _TAG.sub("", text or "").strip()
    head = s.split(",")[0].split(";")[0].split(":")[0].strip()
    # Strip a trailing "(of X)" or "(?)" clarifier
    while True:
        new = _PAREN_TAIL.sub("", head)
        if new == head:
            break
        head = new
    return head.strip()


# ---------------------------------------------------------------------------
# Q1/Q2/Q3 gloss rules
# ---------------------------------------------------------------------------

_ENG_ADJECTIVES = {
    "great", "small", "big", "little", "long", "short", "tall", "broad",
    "wide", "narrow", "deep", "shallow", "high", "low", "good", "bad",
    "evil", "fine", "fair", "beautiful", "ugly", "red", "white", "black",
    "green", "blue", "yellow", "bright", "dark", "old", "young", "new",
    "ancient", "strong", "weak", "rich", "poor", "noble", "wealthy",
    "holy", "sacred", "pure", "clean", "dirty", "hot", "cold", "warm",
    "wet", "dry", "hard", "soft", "heavy", "light", "right", "true",
    "false", "real", "sweet", "bitter", "sour", "joyful", "joyous",
    "happy", "sad", "angry", "fearful", "afraid", "quiet", "silent",
    "loud", "exalted", "supreme", "first", "last", "many", "much",
    "few", "successful", "skilful", "skillful", "wise", "foolish",
    "splendid", "famous", "favourable", "favorable", "former",
    "perfect", "complete", "ready", "open", "shut", "closed",
    "alive", "dead", "free", "favoured", "favored", "blessed",
    "powerful", "weary", "tired", "fresh", "stale", "elder", "eldest",
    "junior", "senior", "yonder",
}

_ENG_VERBS = {
    "be", "do", "go", "say", "make", "come", "take", "give", "see", "hear",
    "die", "live", "rise", "fall", "run", "fly", "eat", "drink", "sit",
    "stand", "walk", "speak", "look", "find", "send", "bring", "carry",
    "cause", "let", "build", "open", "shut", "close", "lift", "raise",
    "spread", "shine", "weep", "smell", "praise", "fight", "kill", "beat",
    "stir", "knead", "rejoice", "embrace", "flee", "depart", "enter",
    "leave", "return", "appear", "become", "begin", "end", "seek", "guard",
    "follow", "lead", "command", "destroy", "create", "fashion", "shape",
    "save", "rescue", "throw", "place", "set", "put", "wash",
    "clean", "wear", "drive", "anoint", "fill", "empty", "pour",
    "neglect", "test", "prove", "answer", "ask", "tell", "name", "call",
    "release", "untie", "tie", "bind", "loose", "draw", "pull", "push",
    "hold", "grasp", "seize", "catch",
    "pound", "cut", "trim", "scratch", "carve", "engrave", "steal", "rob",
    "march", "travel", "sleep", "wake",
}

# Q3: pronoun gloss clusters
_PRONOUN_GLOSSES = {
    "i, me, my",
    "you, your",
    "you, your, yours",
    "he, him, his",
    "she, her, hers",
    "we, us, our",
    "they, them, their",
    "i",
    "me",
    "you",
    "he",
    "she",
    "we",
    "they",
    "this",
    "that",
    "these",
    "those",
}


def gloss_rule_round2(text: str) -> tuple[str | None, str | None]:
    """Round 2 gloss heuristics returning (PartOfSpeech, PartOfSpeechCore)."""
    raw_first = re.sub(r"\s+", " ", (text or "")).strip()
    head_low = (raw_first[:80]).lower()

    # Q3: pronoun cluster ("I, me, my" / "you, your" / "he, him, his")
    for pat in _PRONOUN_GLOSSES:
        if head_low.startswith(pat):
            return "pronoun", "pronoun"

    # Use the cleaned head for noun/adj/verb judgement
    head = first_gloss_clean(text)
    if not head:
        return None, None
    parts = head.split()
    head_low = head.lower()

    if len(parts) == 1:
        # Q1: paren-clarifier stripped, single word -> categorize
        word = parts[0].lower().strip(".")
        if word in _ENG_ADJECTIVES:
            return "adjective", "adjective"
        if word in _ENG_VERBS:
            return "verb", "verb"
        # Lowercase bare word -> noun
        if word and word[0].isalpha() and parts[0][0].islower():
            return "noun", "noun"

    elif len(parts) == 2:
        # Q2: ADJ + NOUN -> noun
        a, b = parts[0].lower().strip(",."), parts[1].lower().strip(",.")
        if a in _ENG_ADJECTIVES and b not in _ENG_VERBS:
            return "noun", "noun"
        # First word is verb -> verb (e.g. "make extensive")
        if a in _ENG_VERBS:
            return "verb", "verb"

    return None, None


# ---------------------------------------------------------------------------
# Q4: Re-derive Core from filled PartOfSpeech
# ---------------------------------------------------------------------------

# Reuse the vocabulary from split_pos.py (inlined for self-containment)
POS_TOKENS = {
    "noun", "verb", "adjective", "pronoun", "particle", "preposition",
    "adverb", "conjunction", "interjection", "interrogative", "infinitive",
    "imperative", "participle", "numeral", "exclamation", "article",
    "unknown",
}

MODIFIER_TOKENS = {
    "feminine", "masculine", "singular", "plural", "dual", "collective",
    "causative", "transitive", "intransitive", "passive", "stative",
    "reciprocal", "auxiliary", "enclitic", "non-enclitic", "proclitic",
    "suffix", "possessive", "demonstrative", "independent", "dependent",
    "conjunctive", "negative", "vocative", "admirative", "interrogative",
    "relative", "genitival", "definite", "indefinite",
    "cardinal", "ordinal", "past", "tense", "perfective", "imperfective",
    "subjunctive", "conditional", "temporal", "proper", "prefix",
    "compound", "verbal", "nominal", "intensifying", "intensifier",
}

DOMAIN_TOKENS = {
    "title", "architecture", "body", "flora", "food", "animal", "furniture",
    "divinity", "clothing", "location", "locality", "boat", "mineral",
    "bird", "fish", "astronomy", "medical", "medicinal", "mathematics",
    "mathematical", "musical", "epithet", "ceremonial", "magical",
    "military", "diplomatic", "ritual", "religious", "royal", "financial",
    "mythological", "festival", "morbid", "physical", "facial", "bodily",
    "urinary", "ornamental", "wet", "dry", "ancient", "archaic", "late",
    "foreign", "greco-roman", "aegean", "motion", "evil",
}

TOKEN_REWRITES = {
    "presposition": "preposition", "prepostion": "preposition",
    "auxillary": "auxiliary", "compund": "compound",
    "femimine": "feminine", "indepentdent": "independent",
    "dependant": "dependent", "causitive": "causative",
    "ausative": "causative", "djective": "adjective", "vnoun": "noun",
    "title": "title", "arch": "architecture", "bod": "body",
    "furn": "furniture", "foof": "food", "pl": "plural", "plura": "plural",
}

# From round 1: high-confidence compound rescues
COMPOUND_RESCUE = {
    "verb and noun": ("verb", [], []),
    "noun and verb": ("noun", [], []),
    "adjective and verb": ("adjective", [], []),
    "auxillary verb with past meaning": ("verb", ["auxiliary", "past"], []),
    "auxiliary verb with past meaning": ("verb", ["auxiliary", "past"], []),
    "pl": ("noun", ["plural"], []),
    "number": ("numeral", [], []),
    "definite article": ("article", ["definite"], []),
    "indefinite article": ("article", ["indefinite"], []),
    "demonstrative pronoun": ("pronoun", ["demonstrative"], []),
    "possessive pronoun": ("pronoun", ["possessive"], []),
    "suffix pronoun": ("pronoun", ["suffix"], []),
    "dependent pronoun": ("pronoun", ["dependent"], []),
    "independent pronoun": ("pronoun", ["independent"], []),
    "interrogative pronoun": ("pronoun", ["interrogative"], []),
    "stative past tense": ("verb", ["stative", "past"], []),
    "stative plural past tense": ("verb", ["stative", "plural", "past"], []),
    "causative intransitive": ("verb", ["causative", "intransitive"], []),
    "negation": ("particle", ["negative"], []),
    "late egyptian": ("noun", [], ["late"]),
    "negative": ("particle", ["negative"], []),
    "stative": ("verb", ["stative"], []),
    "adverb used after an imperative": ("adverb", [], []),
    "prepostion with suffixes": ("preposition", ["suffix"], []),
    "preposition with suffixes": ("preposition", ["suffix"], []),
    "stative perfective": ("verb", ["stative", "perfective"], []),
    "stative imperfective": ("verb", ["stative", "imperfective"], []),
}


def normalize_token(t: str) -> str:
    low = t.lower().strip(".,")
    return TOKEN_REWRITES.get(low, low)


def derive_core(label: str):
    """Return (core, modifiers, domains, used_rescue) or (None, [], [], False)."""
    if not label:
        return None, [], [], False
    norm = label.strip().lower()
    if norm in COMPOUND_RESCUE:
        core, mods, doms = COMPOUND_RESCUE[norm]
        return core, mods, doms, True
    tokens = [normalize_token(t) for t in norm.split()]
    core = None
    mods, doms, unrec = [], [], 0
    for tok in tokens:
        if tok in POS_TOKENS:
            if core is None:
                core = tok
        elif tok in MODIFIER_TOKENS:
            if tok not in mods:
                mods.append(tok)
        elif tok in DOMAIN_TOKENS:
            if tok not in doms:
                doms.append(tok)
        else:
            unrec += 1
    if unrec >= 2:
        return None, [], [], False
    return core, sorted(mods), sorted(doms), False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ----- Q1/Q2/Q3: gloss rules on the residual nulls -----
    q_filled = 0
    q_by_pos = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            pos, core = gloss_rule_round2(t.get("translation", "") or "")
            if pos:
                md["PartOfSpeech"] = pos
                if not md.get("PartOfSpeechCore"):
                    md["PartOfSpeechCore"] = core
                t["TranslationMetadata"] = md
                q_filled += 1
                q_by_pos[pos] += 1
    print(f"\nQ1-Q3 gloss rules: {q_filled:,}")
    for pos, n in q_by_pos.most_common():
        print(f"  -> {pos}: {n}")

    # ----- Q4: derive Core from filled PartOfSpeech where Core is still null -----
    q4_filled = 0
    q4_by_core = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            label = md.get("PartOfSpeech")
            if not label or md.get("PartOfSpeechCore"):
                continue
            core, mods, doms, _ = derive_core(label)
            if not core:
                continue
            md["PartOfSpeechCore"] = core
            if mods:
                existing = list(md.get("Modifiers") or [])
                for m in mods:
                    if m not in existing:
                        existing.append(m)
                md["Modifiers"] = sorted(existing)
            if doms:
                existing = list(md.get("Domains") or [])
                for d in doms:
                    if d not in existing:
                        existing.append(d)
                md["Domains"] = sorted(existing)
            t["TranslationMetadata"] = md
            q4_filled += 1
            q4_by_core[core] += 1
    print(f"\nQ4 core derived from filled POS: {q4_filled:,}")
    for c, n in q4_by_core.most_common():
        print(f"  -> {c}: {n}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
