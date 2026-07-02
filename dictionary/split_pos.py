"""
Split composite PartOfSpeech labels in Entries2.json into structured
PartOfSpeechCore + Modifiers + Domains, preserving the raw label.

For each translation's PartOfSpeech (a space-separated string like
"dual noun clothing body" or "causative verb"), this pass:

  1. Normalizes known typos/abbreviations (presposition -> preposition,
     auxillary -> auxiliary, arch -> architecture, pl -> plural,
     Title -> title, ...).
  2. Tokenizes on whitespace.
  3. Classifies each token into one of three buckets:
       - POS_TOKENS       (noun, verb, adjective, ...)
       - MODIFIER_TOKENS  (causative, transitive, dual, feminine, ...)
       - DOMAIN_TOKENS    (architecture, divinity, flora, ...)
  4. Emits:
       PartOfSpeech       <- unchanged (raw composite string)
       PartOfSpeechCore   <- first POS token found, or null
       Modifiers          <- sorted unique modifier tokens (omitted if empty)
       Domains            <- sorted unique domain tokens   (omitted if empty)

When a label has >=2 unrecognized tokens it is treated as prose (e.g.
"variant of Tni", "used in connection with effects of a cure") — we leave
the raw PartOfSpeech alone and omit the structured fields. The reason: those
labels are data-entry errors from the original parsers and need
case-by-case attention, not auto-structuring.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# Vocabulary tables
# ---------------------------------------------------------------------------

# Typo / abbreviation rewrites applied per-token before classification.
TOKEN_REWRITES = {
    "presposition": "preposition",
    "prepostion": "preposition",
    "auxillary": "auxiliary",
    "compund": "compound",
    "femimine": "feminine",
    "indepentdent": "independent",
    "dependant": "dependent",
    "causitive": "causative",
    "ausative": "causative",
    "djective": "adjective",
    "vnoun": "noun",
    "Title": "title",
    "arch": "architecture",
    "bod": "body",
    "furn": "furniture",
    "foof": "food",
    "pl": "plural",
    "plura": "plural",
}

POS_TOKENS = {
    "noun", "verb", "adjective", "pronoun", "particle", "preposition",
    "adverb", "conjunction", "interjection", "interrogative", "infinitive",
    "imperative", "participle", "numeral", "exclamation", "article",
}

MODIFIER_TOKENS = {
    # Number / gender
    "feminine", "masculine", "singular", "plural", "dual", "collective",
    # Verbal voice / valence
    "causative", "transitive", "intransitive", "passive", "stative",
    "reciprocal", "auxiliary",
    # Pronoun / particle subtype
    "enclitic", "non-enclitic", "proclitic", "suffix", "possessive",
    "demonstrative", "independent", "dependent", "conjunctive", "negative",
    "vocative", "admirative", "interrogative", "relative", "genitival",
    # Determiners
    "definite", "indefinite",
    # Numeral subtype
    "cardinal", "ordinal",
    # Temporal / mood
    "past", "tense", "perfective", "imperfective", "subjunctive",
    "conditional", "temporal",
    # Other grammatical features
    "proper", "prefix", "compound", "verbal", "nominal", "intensifying",
    "intensifier",
}

DOMAIN_TOKENS = {
    # Concrete-noun semantic categories used by Vygus
    "title", "architecture", "body", "flora", "food", "animal", "furniture",
    "divinity", "clothing", "location", "locality", "boat", "mineral",
    "bird", "fish", "astronomy", "medical", "medicinal", "mathematics",
    "mathematical", "musical", "epithet", "ceremonial", "magical",
    "military", "diplomatic", "ritual", "religious", "royal", "financial",
    "mythological", "festival", "scribe's", "ship's", "builder's",
    "morbid", "physical", "facial", "bodily", "urinary", "ornamental",
    "wet", "dry", "ancient", "archaic", "late",
    # Stylistic / register
    "derogatory", "euphemistic", "euphemistically", "figurative",
    "figuratively", "jocular", "obscenity",
    # Provenance / period
    "egyptian", "foreign", "greco-roman", "aegean",
    # Movement / abstract notion
    "motion", "evil", "festival", "rite",
}


def normalize_token(tok: str) -> str:
    """Apply lowercase + typo/abbreviation rewrites."""
    low = tok.lower().strip(".,")
    if low in TOKEN_REWRITES:
        return TOKEN_REWRITES[low]
    # Also catch the typo on the original-case form (e.g. "Title")
    if tok in TOKEN_REWRITES:
        return TOKEN_REWRITES[tok]
    return low


# ---------------------------------------------------------------------------
# Splitter
# ---------------------------------------------------------------------------


def split_pos(label: str | None) -> dict:
    """
    Return {"core": ..., "modifiers": [...], "domains": [...], "raw_kept": bool}.

    raw_kept == True means we did NOT emit structured fields (label is prose).
    """
    if not label:
        return {"core": None, "modifiers": [], "domains": [], "raw_kept": False}

    tokens = label.split()
    cleaned = [normalize_token(t) for t in tokens]
    unrecognized = []
    core: str | None = None
    modifiers: list[str] = []
    domains: list[str] = []

    for tok in cleaned:
        if tok in POS_TOKENS:
            # First POS wins as the core; further POS tokens are unusual
            if core is None:
                core = tok
            else:
                # rare e.g. "verb noun" -> record both as alternatives
                unrecognized.append(tok)
        elif tok in MODIFIER_TOKENS:
            if tok not in modifiers:
                modifiers.append(tok)
        elif tok in DOMAIN_TOKENS:
            if tok not in domains:
                domains.append(tok)
        else:
            unrecognized.append(tok)

    # If >=2 unrecognized tokens (likely prose like "variant of Tni" or
    # "used in connection with X"), refuse to structure the label.
    if len(unrecognized) >= 2:
        return {"core": None, "modifiers": [], "domains": [], "raw_kept": True}

    return {
        "core": core,
        "modifiers": sorted(modifiers),
        "domains": sorted(domains),
        "raw_kept": False,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]

    structured = 0
    prose_skipped = 0
    unique_labels_seen: dict[str, dict] = {}
    core_counter: Counter = Counter()
    modifier_counter: Counter = Counter()
    domain_counter: Counter = Counter()
    skipped_examples: list[str] = []
    no_core_examples: list[tuple[str, dict]] = []

    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            raw = md.get("PartOfSpeech")
            if not raw:
                continue
            if raw not in unique_labels_seen:
                unique_labels_seen[raw] = split_pos(raw)
            split = unique_labels_seen[raw]
            if split["raw_kept"]:
                prose_skipped += 1
                if len(skipped_examples) < 8 and raw not in skipped_examples:
                    skipped_examples.append(raw)
                continue
            if split["core"]:
                md["PartOfSpeechCore"] = split["core"]
                core_counter[split["core"]] += 1
            elif (split["modifiers"] or split["domains"]):
                # Modifier/domain-only label with no core POS -- unusual
                if len(no_core_examples) < 5:
                    no_core_examples.append((raw, split))
            if split["modifiers"]:
                md["Modifiers"] = split["modifiers"]
                for m in split["modifiers"]:
                    modifier_counter[m] += 1
            if split["domains"]:
                md["Domains"] = split["domains"]
                for d in split["domains"]:
                    domain_counter[d] += 1
            structured += 1
            t["TranslationMetadata"] = md

    print(f"\n=== POS-split summary ===")
    print(f"Translations with structured POS    : {structured:,}")
    print(f"Translations left as prose (raw)     : {prose_skipped:,}")
    print(f"Distinct POS labels processed       : {len(unique_labels_seen):,}")

    print(f"\nTop 12 PartOfSpeechCore values:")
    for c, n in core_counter.most_common(12):
        print(f"  {n:6}  {c}")
    print(f"\nTop 12 Modifiers:")
    for m, n in modifier_counter.most_common(12):
        print(f"  {n:6}  {m}")
    print(f"\nTop 12 Domains:")
    for d, n in domain_counter.most_common(12):
        print(f"  {n:6}  {d}")

    print(f"\nProse-style POS labels skipped (kept raw, examples):")
    for label in skipped_examples:
        print(f"  - {label!r}")

    if no_core_examples:
        print(f"\nLabels that produced modifiers/domains but no core POS (rare):")
        for raw, split in no_core_examples:
            print(f"  - raw={raw!r}  mods={split['modifiers']}  doms={split['domains']}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
