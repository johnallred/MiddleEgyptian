"""
Round 3 of POS gap-filling on Entries2.json.

Round 2 brought coverage from 97.4% -> 98.2% (5,297 -> 1,103 null POS).
Inspecting the residual shows four clusters:

  R1. Faulkner pronoun shorthand: "suff. 1 sg." / "suff. 2 pl." / etc.
      Adds suffix pronoun POS.

  R2. Expanded adjective+noun vocabulary for two-word noun phrases like
      "due time", "upper part", "wealthy man", "hereditary noble".
      Extends the adjective list to cover the Faulkner repertoire.

  R3. Participial/relative noun heads beyond what round 2 had:
      "being X", "one X", "way of X", "manner of X", "form of X",
      "part of X" -> noun.

  R4. Preposition phrases. Glosses like "except me", "apart from",
      "according to", "by means of", "in front of", "in the midst of"
      are prepositions. Add a small head-pattern table.

  R5. Single-word capitalized ethnonyms / proper nouns: "Bedouin",
      "Egyptian", "Syrian", "Nubian" -> proper noun.

  R6. Then re-derive Core from any filled PartOfSpeech (catches anything
      P1/P2 from round 1 left behind).
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


_TAG = re.compile(r"<[^>]+>")
_PAREN_TAIL = re.compile(r"\s*\([^)]*\)\s*$")


def first_gloss_clean(text: str) -> str:
    s = _TAG.sub("", text or "").strip()
    head = s.split(",")[0].split(";")[0].split(":")[0].strip()
    while True:
        new = _PAREN_TAIL.sub("", head)
        if new == head:
            break
        head = new
    return head.strip()


# Faulkner abbreviation patterns at gloss start
_FAULKNER_SUFFIX_PRONOUN = re.compile(
    r"^suff\.\s+\d\s+(?:sg|pl)\.?",
    re.I,
)
_FAULKNER_DEP_PRONOUN = re.compile(
    r"^dep\.\s+pron\.\s+\d\s+(?:sg|pl)\.?",
    re.I,
)
_FAULKNER_INDEP_PRONOUN = re.compile(
    r"^indep\.\s+pron\.\s+\d\s+(?:sg|pl)\.?",
    re.I,
)


# ---------------------------------------------------------------------------
# Expanded vocabularies
# ---------------------------------------------------------------------------

_ADJECTIVES = {
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
    # added in round 3
    "due", "upper", "lower", "inner", "outer", "middle", "front",
    "back", "central", "main", "chief", "principal", "hereditary",
    "official", "royal", "divine", "human", "female", "male",
    "private", "public", "personal", "common", "ordinary", "special",
    "general", "specific", "particular", "ceremonial", "ritual",
    "sacred", "secular", "minor", "major", "near", "far", "next",
    "previous", "early", "late", "raw", "cooked", "ripe", "rotten",
    "smooth", "rough", "thick", "thin", "round", "flat", "straight",
    "curved", "northern", "southern", "eastern", "western",
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

# Preposition / locative phrase heads
_PREP_HEADS = (
    "except ", "apart from", "according to", "by means of",
    "in front of", "in the midst of", "in the middle of",
    "in the presence of", "on behalf of", "for the sake of",
    "in place of", "on top of", "underneath", "underneath of",
    "above", "below", "next to", "alongside", "across from",
    "out of", "within", "without", "beyond", "outside of",
    "inside of", "near", "around", "throughout", "from among",
    "instead of", "in addition to", "by reason of", "for lack of",
    "as well as", "rather than",
)

# Participial / relative noun heads (extends round 1)
_PARTICIPIAL_HEADS = (
    "who ", "what ", "which ", "those who", "he who", "she who",
    "one who", "ones who", "those whom", "they who",
    "the one ", "the ones ",
    "being ", "one ", "way of ", "manner of ", "form of ", "part of ",
    "side of ", "kind of ", "type of ", "act of ", "state of ",
)

# Ethnonyms / common proper nouns that appear as single capitalized words
_ETHNONYMS = {
    "Bedouin", "Egyptian", "Syrian", "Nubian", "Asiatic", "Libyan",
    "Hittite", "Mesopotamian", "Babylonian", "Theban", "Memphite",
    "Heliopolitan", "Nubian", "Cushite", "Punt", "Puntite",
    "Phoenician", "Cretan", "Aegean", "Persian", "Mycenaean",
    "Israelite", "Hebrew", "Canaanite",
}


# ---------------------------------------------------------------------------
# Gloss rule
# ---------------------------------------------------------------------------


def gloss_rule_round3(text: str) -> tuple[str | None, str | None]:
    raw = re.sub(r"\s+", " ", (text or "")).strip()
    raw_low = raw.lower()

    # R1: Faulkner pronoun shorthand
    if _FAULKNER_SUFFIX_PRONOUN.match(raw):
        return "suffix pronoun", "pronoun"
    if _FAULKNER_DEP_PRONOUN.match(raw):
        return "dependent pronoun", "pronoun"
    if _FAULKNER_INDEP_PRONOUN.match(raw):
        return "independent pronoun", "pronoun"

    # R3: participial/relative noun heads
    for head in _PARTICIPIAL_HEADS:
        if raw_low.startswith(head):
            return "noun", "noun"

    # R4: preposition phrase heads (matched against lowercased first ~30 chars)
    for head in _PREP_HEADS:
        if raw_low.startswith(head):
            return "preposition", "preposition"

    # Clean head for adjective+noun
    head = first_gloss_clean(text)
    if not head:
        return None, None

    # R5: single-word ethnonym
    if " " not in head and head in _ETHNONYMS:
        return "proper noun", "noun"

    parts = head.split()
    if len(parts) == 2:
        a = parts[0].lower().strip(",.")
        b = parts[1].lower().strip(",.")
        if a in _ADJECTIVES and b not in _ENG_VERBS:
            return "noun", "noun"

    return None, None


# ---------------------------------------------------------------------------
# Core derivation (reuse round 2 logic)
# ---------------------------------------------------------------------------

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


def normalize_token(t):
    return TOKEN_REWRITES.get(t.lower().strip(".,"), t.lower().strip(".,"))


def derive_core(label):
    if not label:
        return None, [], []
    tokens = [normalize_token(t) for t in label.strip().lower().split()]
    core = None; mods = []; doms = []; unrec = 0
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
        return None, [], []
    return core, sorted(mods), sorted(doms)


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # R1-R5: gloss rules
    rfilled = 0
    rby_pos = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            pos, core = gloss_rule_round3(t.get("translation", "") or "")
            if pos:
                md["PartOfSpeech"] = pos
                if not md.get("PartOfSpeechCore"):
                    md["PartOfSpeechCore"] = core
                t["TranslationMetadata"] = md
                rfilled += 1
                rby_pos[pos] += 1
    print(f"\nR1-R5 gloss rules: {rfilled:,}")
    for pos, n in rby_pos.most_common():
        print(f"  -> {pos}: {n}")

    # R6: derive Core from any still-null Core
    r6_filled = 0
    r6_by_core = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            label = md.get("PartOfSpeech")
            if not label or md.get("PartOfSpeechCore"):
                continue
            core, mods, doms = derive_core(label)
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
            r6_filled += 1
            r6_by_core[core] += 1
    print(f"\nR6 core derived: {r6_filled:,}")
    for c, n in r6_by_core.most_common():
        print(f"  -> {c}: {n}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
