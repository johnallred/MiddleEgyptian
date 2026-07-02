"""
Medium-effort cleanups on Entries2.json. Run in this order:

  Step 1  HTML separation
          Faulkner translations carry inline HTML (<b>, <span style>, <sup>,
          <canvas>, <i>, <br>). Split each into:
            translation       -> clean text (HTML stripped, whitespace
                                 normalized, entities decoded, <canvas> MdC
                                 content kept inline so plain text consumers
                                 still see the related-word data)
            translation_html  -> verbatim original HTML (only added when the
                                 original differed from the clean text)

  Step 2  Citation extraction
          Faulkner's translations are rich with source references like
          "Sin. B70; Urk. IV, 425, 8; Westc. 9, 16; Gr. §245; JEA 34, 12".
          We use an explicit whitelist of Egyptological abbreviations and
          capture the location string that follows each. Output goes into a
          new `Citations` array on the translation:
            Citations: [{abbreviation: "Sin.", source: "Sinuhe",
                         location: "B70", raw: "Sin. B70"}, ...]
          The original `translation` text is left intact so visual fidelity
          is preserved; citations are an ADDITIVE structured index.

  Step 3  "var. of X" cross-references
          Translations starting with "var. of <word>" link a variant entry to
          a head entry. Promote each to an entry-level `VariantOf` list, e.g.
            VariantOf: ["ixxw"]
          A few entries say "variant of X and Y"; both targets are recorded.

  Step 4  Duplicate entries merge
          (Transliteration, GardinerSigns) duplicates are merged when safe:
            - Same / null ManuelDeCodage across the group  -> merge
            - Different non-null ManuelDeCodage             -> tag with a
              DuplicateGroupId, leave separate
          Translations are concatenated and deduped on (translation,
          DictionaryName, page, indexOnPage).
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# Step 1: HTML separation
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*>")
_WS = re.compile(r"\s+")
_ENTITY_MAP = {
    "&quot;": '"', "&amp;": "&", "&lt;": "<", "&gt;": ">",
    "&nbsp;": " ", "&apos;": "'", "&#39;": "'", "&#34;": '"',
}


def clean_text_from_html(s: str) -> str:
    """
    Strip HTML but preserve the *content* of <canvas> (MdC strings of
    related words). Decode named entities. Collapse whitespace.
    """
    if not s:
        return s
    for entity, ch in _ENTITY_MAP.items():
        s = s.replace(entity, ch)
    # <br> -> space.
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.IGNORECASE)
    # Drop the wrapping tags but keep inner text for <canvas>, <b>, <i>,
    # <span>, <sup>. _TAG removes EVERY tag while leaving text inside intact.
    s = _TAG.sub("", s)
    return _WS.sub(" ", s).strip()


# ---------------------------------------------------------------------------
# Step 2: Citation extraction
# ---------------------------------------------------------------------------

# Map abbreviation -> human-readable source name. Longer multi-word
# abbreviations come first; the matcher tries them in length-descending order.
SOURCE_MAP = {
    # Multi-word abbreviations
    "Caminos, Lit. Frag.": "Caminos, Literary Fragments",
    "Lit. Frag.": "Literary Fragments",
    "P. Kah.": "Kahun Papyrus",
    "P. Ram.": "Ramesseum Papyri",
    "P. Ed.": "Edwin Smith Papyrus",
    "P. Eb.": "Ebers Papyrus",
    "P. Harris": "Papyrus Harris",
    "Sh. S.": "Shipwrecked Sailor",
    "M. u. K.": "Mutter und Kind",
    "T. Carn.": "Tablette Carnarvon",
    "Th. T.": "Theban Tomb",
    "D. el Geb.": "Deir el-Gebrawi",
    "D. el Bah.": "Deir el-Bahari",
    "Mar. Mast.": "Mariette, Mastabas",
    "Mar. Karn.": "Mariette, Karnak",
    "Mar. Abyd.": "Mariette, Abydos",
    "Dav. Ptah.": "Davies, Ptahhotep",
    "Hor. and Suty": "Horemheb and Suty Stela",
    "Rec. trav.": "Recueil de Travaux",
    "Bull. Inst.": "Bulletin de l'Institut",
    "Adm. p.": "Admonitions of Ipuwer",  # page reference variant
    "Gr. p.": "Gardiner's Egyptian Grammar",
    "Gr. §": "Gardiner's Egyptian Grammar",
    "Ram. p.": "Ramesseum Papyrus",

    # Single-token abbreviations
    "Urk.": "Urkunden",
    "Sin.": "Sinuhe",
    "Peas.": "Eloquent Peasant",
    "Pyr.": "Pyramid Texts",
    "BD": "Book of the Dead",
    "Westc.": "Westcar Papyrus",
    "Eb.": "Ebers Papyrus",
    "Gr.": "Gardiner's Egyptian Grammar",
    "Adm.": "Admonitions of Ipuwer",
    "RB": "Sethe, Reading Book",
    "TR": "Theban Recension",
    "BH": "Beni Hasan",
    "JEA": "Journal of Egyptian Archaeology",
    "ZÄS": "Zeitschrift für Ägyptische Sprache",
    "PSBA": "Proceedings of the Society of Biblical Archaeology",
    "Hatnub": "Hatnub Graffiti",
    "Leb.": "Dispute of a Man with his Ba",
    "Les.": "Sethe, Lesestücke",
    "GAS": "Gardiner, Admonitions Studies",
    "GNS": "Gardiner, Notes on Sinuhe",
    "AEO": "Ancient Egyptian Onomastica",
    "CT": "Coffin Texts",
    "Sm.": "Edwin Smith Papyrus",
    "Pr.": "Ptahhotep (Prisse)",
    "Mill.": "Millingen Papyrus",
    "Siut": "Siut Tomb",
    "BM": "British Museum",
    "Bersh.": "Bersheh",
    "Hamm.": "Hammamat",
    "Hymnen": "Egyptian Hymns",
    "Bull.": "Bulletin",
    "Louvre": "Louvre",
    "Piankhi": "Piankhi Stela",
    "Merikarē": "Instruction for King Merikare",
    "Merikare": "Instruction for King Merikare",
    "Sethe": "Sethe",
    "COA": "City of Akhenaten",
    "Cair.": "Cairo Museum",
    "Berl.": "Berlin Museum",
    "TT": "Theban Tomb",
}

# Sort abbreviations longest-first so multi-word matches win over their
# substrings ("Gr. p." before "Gr.").
_ABBREV_LIST = sorted(SOURCE_MAP.keys(), key=lambda s: -len(s))

# Build a single regex that captures: <abbrev> then a chunk of citation
# location text. Location is greedy across digits, Roman numerals, page/
# paragraph markers, commas, periods, slashes and hyphens — but stops at
# clear gloss boundaries (semicolon, English word start, opening paren of
# a transliteration, etc.).
_LOCATION = (
    r"(?:"
    r"[IVX]+,?\s*"                # Roman volume
    r"|p?l?\.?\s*\d+"             # page or plate or bare number
    r"|§§?\s*\d+(?:[.,]\d+)*"     # paragraph
    r"|\d+(?:[.,]\s*\d+)*"        # numbers with optional commas
    r"|[A-Z]\d+(?:[.,]\d+)*"      # version markers like B70 / R45
    r")"
)

_CITATION_RX = re.compile(
    r"(?P<abbrev>" + "|".join(re.escape(a) for a in _ABBREV_LIST) + r")"
    r"\s+(?P<loc>" + _LOCATION + r"(?:[.,]\s*" + _LOCATION + r"){0,4})"
    r"(?P<tail>[a-z]?)",          # trailing letter qualifier (Eb. 2, 12a)
    flags=re.UNICODE,
)


def extract_citations(text: str) -> list[dict]:
    citations = []
    if not text:
        return citations
    seen_spans = set()  # avoid overlapping matches
    for m in _CITATION_RX.finditer(text):
        span = m.span()
        if any(s <= span[0] < e for s, e in seen_spans):
            continue
        seen_spans.add(span)
        abbrev = m.group("abbrev")
        loc = m.group("loc").strip().rstrip(",;:")
        tail = m.group("tail")
        full_loc = loc + tail
        raw = text[span[0]: span[1]].strip()
        citations.append({
            "abbreviation": abbrev,
            "source": SOURCE_MAP.get(abbrev),
            "location": full_loc,
            "raw": raw,
        })
    return citations


# ---------------------------------------------------------------------------
# Step 3: "var. of X" cross-references
# ---------------------------------------------------------------------------

_VAR_OF = re.compile(
    r"^(?:var\.\s+of|variant\s+of)\s+([\wāēīōūɛ.ʿ-]+)"
    r"(?:\s+and\s+([\wāēīōūɛ.ʿ-]+))?",
    re.IGNORECASE,
)


def extract_variant_of(clean_text: str) -> list[str]:
    """Return list of variant headwords, or []."""
    m = _VAR_OF.match(clean_text or "")
    if not m:
        return []
    targets = [m.group(1)]
    if m.group(2):
        targets.append(m.group(2))
    return targets


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def dict_name(md):
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return v


def translation_signature(t):
    """Identity for dedup: (clean text, DictionaryName, Page, IndexOnPage)."""
    md = t.get("TranslationMetadata") or {}
    return (
        (t.get("translation") or "").strip(),
        dict_name(md),
        md.get("Page"),
        md.get("IndexOnPage"),
    )


def merge_entries(group):
    """
    Merge a group of entries sharing (Transliteration, GardinerSigns).
    Returns (merged_entry, was_safe). When MdC values disagree we mark the
    group and don't actually merge — caller leaves them separate.
    """
    mdc_values = {e.get("ManuelDeCodage") for e in group if e.get("ManuelDeCodage")}
    if len(mdc_values) > 1:
        # Tag both and skip merge.
        gid = group[0].get("_id", {}).get("$oid") or id(group[0])
        for e in group:
            e["DuplicateGroupId"] = gid
        return None, False

    primary = dict(group[0])
    merged_translations = []
    seen_sigs = set()
    for e in group:
        for t in e.get("Translations") or []:
            sig = translation_signature(t)
            if sig in seen_sigs:
                continue
            seen_sigs.add(sig)
            merged_translations.append(t)
    primary["Translations"] = merged_translations

    # Take first non-null Res across the group.
    for e in group:
        if e.get("Res"):
            primary["Res"] = e["Res"]
            break

    # Concatenate VariantOf lists (added in step 3).
    variants = []
    for e in group:
        for v in e.get("VariantOf") or []:
            if v not in variants:
                variants.append(v)
    if variants:
        primary["VariantOf"] = variants

    return primary, True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ===== Step 1 + 2 + 3 (per-entry passes) =====
    html_split = 0
    citations_total = 0
    citations_per_source = Counter()
    citation_abbrev_hits = Counter()
    variant_promoted = 0
    variant_examples = []

    for e in entries:
        for t in e.get("Translations") or []:
            raw = t.get("translation", "") or ""
            had_html = bool(re.search(r"<[^>]+>", raw))
            clean = clean_text_from_html(raw)

            # Step 1: store clean text in `translation`, keep html aside
            if had_html and clean != raw:
                t["translation_html"] = raw
                t["translation"] = clean
                html_split += 1

            # Step 2: citations
            cits = extract_citations(clean)
            if cits:
                t["Citations"] = cits
                citations_total += len(cits)
                for c in cits:
                    citation_abbrev_hits[c["abbreviation"]] += 1
                    if c["source"]:
                        citations_per_source[c["source"]] += 1

        # Step 3: variant cross-references (entry-level)
        targets = []
        for t in e.get("Translations") or []:
            clean = t.get("translation", "") or ""
            ts = extract_variant_of(clean)
            for x in ts:
                if x not in targets:
                    targets.append(x)
        if targets:
            e["VariantOf"] = targets
            variant_promoted += 1
            if len(variant_examples) < 5:
                variant_examples.append((e.get("Transliteration"), targets))

    print("\n=== Step 1: HTML separation ===")
    print(f"Translations with translation_html added: {html_split:,}")

    print("\n=== Step 2: citation extraction ===")
    print(f"Total citations extracted: {citations_total:,}")
    print("Top 15 source abbreviations:")
    for ab, n in citation_abbrev_hits.most_common(15):
        print(f"  {n:5}  {ab:18}  -> {SOURCE_MAP.get(ab,'?')}")

    print("\n=== Step 3: variant cross-references ===")
    print(f"Entries promoted with VariantOf: {variant_promoted:,}")
    for tr, targets in variant_examples:
        print(f"  {tr:18}  -> VariantOf={targets}")

    # ===== Step 4: duplicate merge =====
    print("\n=== Step 4: duplicate merge ===")
    by_key = defaultdict(list)
    for e in entries:
        by_key[(e.get("Transliteration"), e.get("GardinerSigns"))].append(e)

    merged_out = []
    merged_groups = 0
    flagged_groups = 0
    translations_deduped = 0

    # Track which entries are absorbed so we can skip them.
    absorbed = set()
    for key, group in by_key.items():
        if len(group) == 1:
            continue
        # Get original translation count
        before = sum(len(e.get("Translations") or []) for e in group)
        primary, ok = merge_entries(group)
        after = len(primary["Translations"]) if ok else before
        if ok:
            merged_groups += 1
            translations_deduped += before - after
            absorbed.update(id(e) for e in group)
            # Update the primary entry in place; mark group's other members
            # as removed.
            group[0].clear()
            group[0].update(primary)
            for e in group[1:]:
                e["__deleted__"] = True
        else:
            flagged_groups += 1

    # Filter out deleted markers
    final = [e for e in entries if not e.get("__deleted__")]

    print(f"Duplicate (Translit, Gardiner) keys: {sum(1 for g in by_key.values() if len(g)>1):,}")
    print(f"Groups merged (compatible)         : {merged_groups:,}")
    print(f"Groups flagged DuplicateGroupId    : {flagged_groups:,}")
    print(f"Duplicate translations removed     : {translations_deduped:,}")
    print(f"Entries after merge                : {len(final):,}  (was {len(entries):,})")

    # ===== Write =====
    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in final:
            # never serialize the temp delete marker
            e.pop("__deleted__", None)
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(final):,} entries")


if __name__ == "__main__":
    main()
