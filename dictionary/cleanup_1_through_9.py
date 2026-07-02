"""
Cleanup pass 1-9 on Entries2.json.

  1. cf. cross-references -> translation-level CompareWith list.
  2. (?) uncertainty -> translation-level Uncertain: true flag.
  3. det. <sign> references -> translation-level Determinatives: [<sign>...].
  4. VariantOf self-cycles -> stripped (entry pointed at itself).
  5. Morphology rescue on split-sense translations with null POS (the 51
     records left null by H).
  6. Citation location parsing -> per-citation location_parts structured form
     (witness/paragraph/page/numbers).
  7. GardinerSigns vs ManuelDeCodage token-count integrity check ->
     GardinerMdCMismatch flag on entries that disagree on count.
  8. AttestationCount derived field per entry (distinct (source, location)
     pairs across all translations).
  9. Same-source near-duplicate translations within an entry -> keep
     longest variant, drop the rest.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


# ---------------------------------------------------------------------------
# 1. cf. extraction
# ---------------------------------------------------------------------------

# "cf. <word>" where <word> is a transliteration-shaped token.
# Skip false matches where the word after cf. is an English stopword.
_CF_RX = re.compile(r"\bcf\.\s+([\w][\w.\-]*)", re.UNICODE)
_CF_STOPWORDS = {
    "the", "a", "an", "of", "and", "is", "in", "see", "also", "as",
    "with", "or", "but", "from", "for", "by", "than", "next", "above",
    "below", "earlier", "later", "under", "this", "that", "these",
    "those",
}


def extract_cf_targets(text: str) -> list[str]:
    if not text or "cf." not in text:
        return []
    seen = []
    for m in _CF_RX.finditer(text):
        tgt = m.group(1).rstrip(".,")
        if tgt.lower() in _CF_STOPWORDS:
            continue
        if tgt and tgt not in seen:
            seen.append(tgt)
    return seen


# ---------------------------------------------------------------------------
# 2. (?) uncertainty
# ---------------------------------------------------------------------------

# We add an Uncertain flag but DO NOT strip the marker — '(?)' carries
# placement information (which part is questioned).
def has_uncertainty_marker(text: str) -> bool:
    return "(?)" in (text or "")


# ---------------------------------------------------------------------------
# 3. det. <sign> extraction
# ---------------------------------------------------------------------------

# Patterns to capture:
#   "det. F51"           single determinative
#   "(det. Y1)"          parenthesized
#   "dets. F51-Z2"       plural form with multiple
#   "det. F51-Z2"        compound
#   "(dets. Y1 Z2)"      parenthesized plural
_DET_RX = re.compile(
    r"\bdets?\.\s+([A-Z][A-Za-z]?\d+[A-Za-z]?(?:[-\s][A-Z][A-Za-z]?\d+[A-Za-z]?)*)"
)
_SIGN_TOKEN = re.compile(r"[A-Z][A-Za-z]?\d+[A-Za-z]?")


def extract_determinatives(text: str) -> list[str]:
    if not text or "det." not in text:
        return []
    result = []
    for m in _DET_RX.finditer(text):
        for sign in _SIGN_TOKEN.findall(m.group(1)):
            if sign not in result:
                result.append(sign)
    return result


# ---------------------------------------------------------------------------
# 5. Morphology rescue (R1, R3, R4 from morphology_pass.py)
# ---------------------------------------------------------------------------

_FIRST_GLOSS_CUT = re.compile(r",\s+[A-Z]{1,5}\.\s")


def first_gloss(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text or "").strip()
    t = _FIRST_GLOSS_CUT.split(t, maxsplit=1)[0]
    return t.split(";")[0].strip()


_ARTICLE_PREFIXES = ("a ", "an ", "the ", "kind of ", "name of ",
                     "type of ", "sort of ", "species of ", "variety of ",
                     "title of ")


def morphology_pos(translit: str, gloss_text: str) -> str | None:
    g = first_gloss(gloss_text)
    if not g:
        return None
    gl = g.lower()
    if re.match(r"^to\s+[a-z]", gl):
        return "verb"
    if re.match(r"^be\s+[a-z]", gl):
        return "verb"
    for prefix in _ARTICLE_PREFIXES:
        if gl.startswith(prefix):
            return "noun"
    return None


# ---------------------------------------------------------------------------
# 6. Citation location parsing
# ---------------------------------------------------------------------------


def parse_location(volume: str | None, location: str) -> dict | None:
    """
    Parse the location string into structured components.

    Returns a dict with whichever of these keys apply:
      volume (Roman numeral if present)
      witness (single uppercase letter prefix)
      paragraph (number after §)
      page_prefix ("p." or "pl.")
      numbers (list of ints, in order)
    """
    if not location:
        return None
    out = {}
    if volume:
        out["volume"] = volume
    s = location.strip()

    # Paragraph form: §245, §§80.263.264
    if s.startswith("§"):
        nums = [int(n) for n in re.findall(r"\d+", s)]
        if nums:
            out["paragraph"] = nums[0]
            if len(nums) > 1:
                out["paragraph_extras"] = nums[1:]
        return out or None

    # Page/plate prefix: "p. 449, C11" or "pl. 13, 29"
    m = re.match(r"^(p|pl)\.\s*(.*)$", s)
    if m:
        out["page_prefix"] = m.group(1) + "."
        rest = m.group(2)
        nums = [int(n) for n in re.findall(r"\d+", rest)]
        if nums:
            out["numbers"] = nums
        # Trailing alpha-number like "C11"
        m2 = re.search(r"\b([A-Z])(\d+)\b", rest)
        if m2:
            out["witness"] = m2.group(1)
        return out or None

    # Witness prefix: "B70", "R45", "B114.205"
    m = re.match(r"^([A-Z])(\d+(?:[.,]\s*\d+)*)([a-z]?)\b", s)
    if m:
        out["witness"] = m.group(1)
        nums = [int(n) for n in re.findall(r"\d+", m.group(2))]
        if nums:
            out["numbers"] = nums
        if m.group(3):
            out["letter_suffix"] = m.group(3)
        return out

    # Plain numeric: "425, 8" or "1546, 10" or "53-62"
    range_m = re.match(r"^(\d+)\s*-\s*(\d+)$", s)
    if range_m:
        out["numbers"] = [int(range_m.group(1)), int(range_m.group(2))]
        out["is_range"] = True
        return out
    nums = [int(n) for n in re.findall(r"\d+", s)]
    if nums:
        out["numbers"] = nums
        return out
    return None


# ---------------------------------------------------------------------------
# 7. GardinerSigns vs MdC token-count integrity
# ---------------------------------------------------------------------------

_MDC_TOKEN = re.compile(r"(?:Aa|AA|[A-Z])\d+[A-Za-z]?", re.IGNORECASE)


def gs_mdc_mismatch(gs: str, mdc: str) -> bool:
    if not gs or not mdc:
        return False
    gs_tokens = [t for t in gs.split() if t]
    # Normalize MdC tokens: lowercase the second letter of 'Aa' becomes uppercase
    # so we count tokens by their underlying sign.
    mdc_tokens = _MDC_TOKEN.findall(mdc)
    return len(gs_tokens) != len(mdc_tokens)


# ---------------------------------------------------------------------------
# 8. AttestationCount
# ---------------------------------------------------------------------------


def dn(md: dict) -> str | int | None:
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return v


def attestation_count(entry: dict) -> int:
    """Distinct (source-name, location) pairs across all citations."""
    pairs = set()
    for t in entry.get("Translations") or []:
        for c in t.get("Citations") or []:
            src = c.get("source") or c.get("abbreviation")
            loc = c.get("location") or ""
            vol = c.get("volume") or ""
            pairs.add((src, f"{vol}|{loc}"))
    return len(pairs)


# ---------------------------------------------------------------------------
# 9. Same-source near-duplicate dedup
# ---------------------------------------------------------------------------


def dedup_same_source(translations: list[dict]) -> int:
    """
    Drop near-duplicate translations from the same source: when two
    translations share the same source AND the first 30 chars of their
    lowercased text match, keep the longer (more informative) variant.
    Returns count of translations removed.
    """
    if len(translations) < 2:
        return 0
    by_key: dict[tuple, list[int]] = defaultdict(list)
    for i, t in enumerate(translations):
        md = t.get("TranslationMetadata") or {}
        src = dn(md)
        text = (t.get("translation") or "").strip().lower()
        if not text:
            continue
        key = (src, text[:30])
        by_key[key].append(i)
    to_drop = set()
    for key, idxs in by_key.items():
        if len(idxs) < 2:
            continue
        # Keep longest; drop shorter siblings.
        sorted_idxs = sorted(
            idxs,
            key=lambda i: -len(translations[i].get("translation") or "")
        )
        keep = sorted_idxs[0]
        for drop_idx in sorted_idxs[1:]:
            to_drop.add(drop_idx)
    if not to_drop:
        return 0
    # Mutate in place: keep order
    kept = [t for i, t in enumerate(translations) if i not in to_drop]
    translations.clear()
    translations.extend(kept)
    return len(to_drop)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    # ----- 4. VariantOf self-cycles (do early so #8 sees clean variants) -----
    s4 = 0
    for e in entries:
        v = e.get("VariantOf") or []
        translit = e.get("Transliteration")
        if not v or not translit:
            continue
        cleaned = [x for x in v if x != translit]
        if len(cleaned) != len(v):
            s4 += 1
            if cleaned:
                e["VariantOf"] = cleaned
            else:
                del e["VariantOf"]
    print(f"\n4. VariantOf self-cycles stripped: {s4}")

    # ----- 1. cf. -----
    s1 = 0
    s1_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            tgts = extract_cf_targets(t.get("translation") or "")
            if tgts:
                t["CompareWith"] = tgts
                s1 += 1
                if len(s1_examples) < 4:
                    s1_examples.append((e.get("Transliteration"), tgts))
    print(f"\n1. CompareWith fields added: {s1}")
    for tr, tgts in s1_examples:
        print(f"   {tr!r}: CompareWith={tgts}")

    # ----- 2. (?) uncertainty -----
    s2 = 0
    for e in entries:
        for t in e.get("Translations") or []:
            if has_uncertainty_marker(t.get("translation") or ""):
                t["Uncertain"] = True
                s2 += 1
    print(f"\n2. Uncertain flags added: {s2}")

    # ----- 3. det. -----
    s3 = 0
    s3_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            dets = extract_determinatives(t.get("translation") or "")
            if dets:
                t["Determinatives"] = dets
                s3 += 1
                if len(s3_examples) < 4:
                    s3_examples.append((e.get("Transliteration"), dets))
    print(f"\n3. Determinatives extracted: {s3}")
    for tr, dets in s3_examples:
        print(f"   {tr!r}: Determinatives={dets}")

    # ----- 5. Morphology rescue on split senses -----
    s5 = 0
    for e in entries:
        translit = e.get("Transliteration") or ""
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if not md.get("SenseNumber"):
                continue
            if md.get("PartOfSpeech"):
                continue
            pos = morphology_pos(translit, t.get("translation") or "")
            if pos:
                md["PartOfSpeech"] = pos
                md["PartOfSpeechCore"] = pos
                t["TranslationMetadata"] = md
                s5 += 1
    print(f"\n5. Morphology-rescued split senses: {s5}")

    # ----- 6. Citation location parsing -----
    s6 = 0
    for e in entries:
        for t in e.get("Translations") or []:
            for c in t.get("Citations") or []:
                parts = parse_location(c.get("volume"), c.get("location") or "")
                if parts:
                    c["location_parts"] = parts
                    s6 += 1
    print(f"\n6. Citations with location_parts: {s6:,}")

    # ----- 7. GS/MdC mismatch flag -----
    s7 = 0
    for e in entries:
        if gs_mdc_mismatch(e.get("GardinerSigns") or "",
                           e.get("ManuelDeCodage") or ""):
            e["GardinerMdCMismatch"] = True
            s7 += 1
    print(f"\n7. Entries flagged GardinerMdCMismatch: {s7:,}")

    # ----- 8. AttestationCount -----
    s8 = 0
    for e in entries:
        n = attestation_count(e)
        if n > 0:
            e["AttestationCount"] = n
            s8 += 1
    print(f"\n8. Entries with AttestationCount: {s8:,}")

    # ----- 9. Same-source dedup -----
    s9 = 0
    for e in entries:
        s9 += dedup_same_source(e.get("Translations") or [])
    print(f"\n9. Same-source near-duplicate translations dropped: {s9}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
