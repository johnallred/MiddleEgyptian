"""
Cleanup pass A-F on Entries2.json.

A. Rescue prose POS labels by inferring core POS from a lone modifier or
   domain token (e.g. "causative" -> verb modifier, "demonstrative" -> pronoun
   modifier, "feminine" -> noun modifier, "locality" -> noun domain).

B. Canonicalize translations within an entry that differ from a sibling
   only in case. Adopt the most-lowercase variant's text so duplicates
   look identical without losing per-source attribution.

C. Collapse runs of internal whitespace in translation text to a single
   space. Skip translation_html (HTML may have meaningful whitespace).

D. Loosen citation extraction for two patterns the earlier pass missed:
     - "BD <numbers>" packed against an MdC sequence (e.g. "T26BD 289, 3")
     - "Gr. pp. 554-5" (double-p pages, not just single-p)

E. The rwt entry says "var. D21-..., in wDa-rwt 'judge', q.v." — promote
   wDa-rwt into VariantOf.

F. The 7 entries with no Transliteration get TransliterationUnknown: true
   so consumers can tell absence-by-design apart from missing data.
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# A. Prose-POS rescue
# ---------------------------------------------------------------------------

# When the original POS label is JUST a modifier or domain token (single
# normalized token, no core POS), infer what the core POS most likely is.
MODIFIER_TO_CORE = {
    # Verbal modifiers -> the word is almost certainly a verb
    "causative":     "verb",
    "transitive":    "verb",
    "intransitive":  "verb",
    "reciprocal":    "verb",
    "stative":       "verb",
    "passive":       "verb",
    "auxiliary":     "verb",
    # Nominal modifiers -> the word is almost certainly a noun
    "feminine":      "noun",
    "masculine":     "noun",
    "plural":        "noun",
    "dual":          "noun",
    "collective":    "noun",
    "proper":        "noun",
    "singular":      "noun",
    # Pronoun modifiers
    "demonstrative": "pronoun",
    "possessive":    "pronoun",
    "dependent":     "pronoun",
    "independent":   "pronoun",
    "suffix":        "pronoun",
    # Particle modifiers
    "enclitic":      "particle",
    "non-enclitic":  "particle",
    "negative":      "particle",
    "conjunctive":   "particle",
    "vocative":      "particle",
    "interrogative": "particle",
    "admirative":    "particle",
    # Article modifiers
    "definite":      "article",
    "indefinite":    "article",
}

# Domain-only -> default to noun (every domain in our vocabulary is a noun
# semantic category by convention).
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

# Multi-token rescue table: known compound prose labels we can map
COMPOUND_RESCUE = {
    "verb and noun":  ("verb",   [],            [],            "Polysemous: verb/noun"),
    "noun and verb":  ("noun",   [],            [],            "Polysemous: verb/noun"),
    "adjective and verb": ("adjective", [],     [],            "Polysemous: adjective/verb"),
    "auxillary verb with past meaning": ("verb", ["auxiliary","past"], [], None),
    "auxiliary verb with past meaning": ("verb", ["auxiliary","past"], [], None),
    "pl":             ("noun",   ["plural"],    [],            None),
    "number":         ("numeral",[],            [],            None),
    "pyramid of Unas":("noun",   [],            ["location"],  "Refers to Pyramid of Unas"),
    "definite article":("article",["definite"], [],            None),
    "indefinite article":("article",["indefinite"],[],         None),
    "demonstrative pronoun":("pronoun",["demonstrative"],[],   None),
    "possessive pronoun":("pronoun",["possessive"],[],         None),
    "suffix pronoun": ("pronoun",["suffix"],    [],            None),
    "dependent pronoun":("pronoun",["dependent"],[],           None),
    "independent pronoun":("pronoun",["independent"],[],       None),
    "interrogative pronoun":("pronoun",["interrogative"],[],   None),
}


def rescue_prose_pos(label: str) -> tuple[str|None, list[str], list[str], str|None]:
    """
    Return (core, modifiers, domains, note) for a prose-style POS label,
    or (None, [], [], None) if we can't rescue it.
    """
    if not label:
        return None, [], [], None
    norm = label.strip().lower()
    if norm in COMPOUND_RESCUE:
        return COMPOUND_RESCUE[norm]
    tokens = norm.split()
    if len(tokens) == 1:
        tok = tokens[0]
        if tok in MODIFIER_TO_CORE:
            return MODIFIER_TO_CORE[tok], [tok], [], None
        if tok in DOMAIN_TOKENS:
            return "noun", [], [tok], None
    return None, [], [], None


# ---------------------------------------------------------------------------
# B. Case-only sibling canonicalization
# ---------------------------------------------------------------------------

def canonicalize_case_duplicates(translations):
    """
    Within a list of translations, when two translations have the same
    .lower() but different actual text, rewrite the more-capitalized one to
    match the less-capitalized one. Returns number of rewrites.
    """
    # group by lowercase form
    groups: dict[str, list[int]] = {}
    for i, t in enumerate(translations):
        text = (t.get("translation") or "").strip()
        if not text:
            continue
        groups.setdefault(text.lower(), []).append(i)

    rewrites = 0
    for key, idxs in groups.items():
        if len(idxs) < 2:
            continue
        # Choose canonical = the version with the fewest uppercase letters
        canonical = min(
            (translations[i].get("translation","") for i in idxs),
            key=lambda s: sum(1 for c in s if c.isupper())
        )
        for i in idxs:
            cur = translations[i].get("translation","")
            if cur != canonical:
                translations[i]["translation"] = canonical
                rewrites += 1
    return rewrites


# ---------------------------------------------------------------------------
# C. Double-space collapse
# ---------------------------------------------------------------------------

_MULTI_SPACE = re.compile(r"[ \t]{2,}")


def collapse_double_spaces(text: str) -> str:
    if not text:
        return text
    return _MULTI_SPACE.sub(" ", text)


# ---------------------------------------------------------------------------
# D. Catch BD-after-MdC and pp. page citations
# ---------------------------------------------------------------------------

# Find "BD <numbers>" not already followed by a context-guard match. The
# special case is BD packed against MdC like "T26BD 289, 3": the B belongs
# to T26B, then D 289, 3 is "BD 289, 3" Book of the Dead.
_BD_AFTER_MDC = re.compile(
    r"(?<![A-Z])BD\s+(?P<location>\d+(?:[.,]\s*\d+)*[a-z]?(?:\s*,\s*\d+(?:[.,]\s*\d+)*[a-z]?)*)"
)

# "Gr. pp. 554-5" / "Gr. pp. 554, 5"
_GR_PP = re.compile(
    r"Gr\.\s+pp\.\s+(?P<location>\d+(?:\s*-\s*\d+)?(?:[.,]\s*\d+)*)"
)


def find_extra_citations(text: str) -> list[dict]:
    cits = []
    # BD that was missed because it abuts an MdC token
    for m in re.finditer(r"(?<![A-Z])BD\s+(\d+(?:[.,]\s*\d+)*[a-z]?(?:\s*,\s*\d+(?:[.,]\s*\d+)*[a-z]?)*)", text):
        # Only emit if the BD wasn't separated from a token by whitespace; in
        # that case the original citation pass would have got it.
        # Use the start-of-match's preceding context.
        start = m.start()
        if start > 0 and not text[start - 1].isspace():
            cits.append({
                "abbreviation": "BD",
                "source": "Book of the Dead",
                "location": m.group(1).strip(",;:"),
                "raw": m.group(0),
            })
    for m in _GR_PP.finditer(text):
        cits.append({
            "abbreviation": "Gr. pp.",
            "source": "Gardiner's Egyptian Grammar",
            "location": m.group("location").strip(",;:"),
            "raw": m.group(0),
        })
    return cits


# ---------------------------------------------------------------------------
# E. rwt VariantOf promotion
# ---------------------------------------------------------------------------

_VAR_IN_FORM = re.compile(
    r"^var\.\s+[A-Z][\w\-*:&]+(?:\s*,\s*[A-Z][\w\-*:&]+)*"
    r"\s*,\s*in\s+([\w\-.]+)",
    re.IGNORECASE,
)


def extract_var_in_target(text: str) -> str|None:
    """Match 'var. <MdC>, in <translit> ...' and return the translit."""
    m = _VAR_IN_FORM.match((text or "").strip())
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ===== A =====
    rescued = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            raw = md.get("PartOfSpeech")
            if not raw or md.get("PartOfSpeechCore"):
                continue
            core, mods, doms, note = rescue_prose_pos(raw)
            if core is None and not mods and not doms:
                continue
            if core:
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
            if note:
                md["Notes"] = note
            rescued[raw] += 1
            t["TranslationMetadata"] = md
    print(f"\nA. Prose-POS rescue: {sum(rescued.values()):,} translations rescued, "
          f"{len(rescued)} distinct raw labels.")
    print("   Top rescued labels:")
    for raw, n in rescued.most_common(8):
        print(f"     {n:5}  {raw!r}")

    # ===== B =====
    b_rewrites = 0
    for e in entries:
        b_rewrites += canonicalize_case_duplicates(e.get("Translations") or [])
    print(f"\nB. Case-only canonical rewrites: {b_rewrites:,}")

    # ===== C =====
    c_fixes = 0
    for e in entries:
        for t in e.get("Translations") or []:
            text = t.get("translation","") or ""
            if "  " not in text and "\t" not in text:
                continue
            new = collapse_double_spaces(text)
            if new != text:
                t["translation"] = new
                c_fixes += 1
    print(f"\nC. Double-space collapses: {c_fixes:,}")

    # ===== D =====
    d_added = 0
    d_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            text = t.get("translation","") or ""
            extras = find_extra_citations(text)
            if not extras:
                continue
            cur = t.get("Citations") or []
            existing_raw = {c.get("raw") for c in cur}
            for x in extras:
                if x["raw"] not in existing_raw:
                    cur.append(x)
                    d_added += 1
                    if len(d_examples) < 5:
                        d_examples.append((e["Transliteration"], x))
            t["Citations"] = cur
    print(f"\nD. Extra citations rescued: {d_added}")
    for tr, c in d_examples:
        print(f"     {tr}: {c}")

    # ===== E =====
    e_promoted = 0
    for e in entries:
        if e.get("VariantOf"):
            continue
        for t in e.get("Translations") or []:
            text = t.get("translation","") or ""
            target = extract_var_in_target(text)
            if target:
                e["VariantOf"] = [target]
                e_promoted += 1
                print(f"\nE. Promoted variant: {e['Transliteration']!r} -> VariantOf=[{target!r}]")
                break

    if e_promoted == 0:
        print("\nE. No 'var. <MdC>, in <translit>' patterns found to promote.")

    # ===== F =====
    f_flagged = 0
    for e in entries:
        if not e.get("Transliteration") and "TransliterationUnknown" not in e:
            e["TransliterationUnknown"] = True
            f_flagged += 1
    print(f"\nF. Entries flagged TransliterationUnknown: {f_flagged}")

    # ===== Write =====
    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
