"""
Cleanup pass G-K on Entries2.json.

G. RelatedWords extraction.
   Faulkner translations embed inline related-word references as
   <canvas class="res">MdC</canvas> tags, sometimes followed by an italic
   transliteration and a quoted gloss. Walk translation_html, extract every
   canvas block plus its immediate surroundings, and emit a structured
   RelatedWords array on the translation.

H. Sub-gloss split.
   Faulkner translations of the form "(1) gloss1, citations: (2) gloss2,
   citations: (3) gloss3" are split into separate Translation records,
   each carrying a SenseNumber. Each split chunk gets its POS and
   Citations re-extracted so they belong to the right sense.

I. q.v. cross-references.
   Where a translation says "<word> 'gloss', q.v." the target word is a
   structured cross-reference. Extract into a translation-level SeeAlso
   list. (cf., loc. cit., op. cit. are recorded as raw markers but the
   target isn't always extractable; left as a note rather than promoted.)

J. Corpus file mapping.
   For citations whose source corresponds to a file in
   EgyptianTranslation/texts/nederhof-texts/, add a corpus_file pointer.
   Sinuhe with B-location -> SinuheTrB.txt, Peasant B1 -> PeasantTrB1.txt,
   etc. About a dozen abbreviation+version-letter mappings cover the
   common cases.

K. HTML residue.
   No-op: the prior pass already decoded entities from the clean
   translation field. Verified empty during audit.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
ENTRIES = HERE / "Entries2.json"


# ---------------------------------------------------------------------------
# G. RelatedWords extraction
# ---------------------------------------------------------------------------

# canvas tag content (MdC), then optional italic transliteration, then
# optional smart-quoted gloss
_CANVAS_RX = re.compile(
    r"<canvas[^>]*>([^<]+)</canvas>"             # group 1: MdC
    r"(?:\s*<[^>]+>)*\s*"                         # any tags between
    r"(?:<i[^>]*>([^<]+)</i[^>]*>)?"             # group 2: transliteration (optional)
    r"(?:[\s,;:]*<[^>]+>)*\s*"
    r"(?:[‘'\"]([^’'\"]{1,80})[’'\"])?",          # group 3: gloss (optional, smart or straight quotes)
    re.IGNORECASE,
)

# Strip any nested HTML tags from group captures
_INNER_TAG = re.compile(r"<[^>]+>")


def extract_related_words(translation_html: str) -> list[dict]:
    if not translation_html or "<canvas" not in translation_html:
        return []
    related = []
    for m in _CANVAS_RX.finditer(translation_html):
        mdc = _INNER_TAG.sub("", m.group(1) or "").strip()
        translit = _INNER_TAG.sub("", m.group(2) or "").strip() if m.group(2) else ""
        gloss = (m.group(3) or "").strip()
        if not mdc:
            continue
        entry = {"mdc": mdc}
        if translit:
            entry["transliteration"] = translit
        if gloss:
            entry["gloss"] = gloss
        related.append(entry)
    return related


# ---------------------------------------------------------------------------
# H. Sub-gloss split
# ---------------------------------------------------------------------------

# A translation is a multi-sense entry when it starts with "(1) " and
# contains at least "(2) " somewhere later, with a sense separator before it.
# Senses are separated by ":" / ";" / "." then space then "(N)".
_SUBGLOSS_HEAD = re.compile(r"^\(\d+\)\s+")
_SUBGLOSS_SPLIT = re.compile(r"\s*[:;.]\s*(?=\(\d+\)\s+[a-zA-Z])")
_SENSE_LABEL = re.compile(r"^\((\d+)\)\s+")

# Compact Faulkner POS extractor for the split chunks; matches the rules
# from parse_faulkner.py.
_FAULKNER_POS_PATTERNS = [
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?intrans\.", re.I), "intransitive verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?trans\.", re.I), "transitive verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?caus\.", re.I), "causative verb"),
    (re.compile(r"^vb\.\s+(?:\([^)]+\)\s+)?recipr\.", re.I), "reciprocal verb"),
    (re.compile(r"^vb\.", re.I), "verb"),
    (re.compile(r"^n\.\s+div\.", re.I), "noun divinity"),
    (re.compile(r"^n\.\s+pr\.", re.I), "proper noun"),
    (re.compile(r"^n\.\s+coll\.", re.I), "collective noun"),
    (re.compile(r"^n\.\s+loc\.", re.I), "noun location"),
    (re.compile(r"^n\.", re.I), "noun"),
    (re.compile(r"^adj\.", re.I), "adjective"),
    (re.compile(r"^adv\.", re.I), "adverb"),
    (re.compile(r"^prep\.", re.I), "preposition"),
    (re.compile(r"^conj\.", re.I), "conjunction"),
    (re.compile(r"^encl\.\s+part\.", re.I), "enclitic particle"),
    (re.compile(r"^non[- ]encl\.\s+part\.", re.I), "non-enclitic particle"),
    (re.compile(r"^part\.", re.I), "particle"),
    (re.compile(r"^pron\.", re.I), "pronoun"),
    (re.compile(r"^suff\.\s+pron\.", re.I), "suffix pronoun"),
    (re.compile(r"^dep\.\s+pron\.", re.I), "dependent pronoun"),
    (re.compile(r"^indep\.\s+pron\.", re.I), "independent pronoun"),
    (re.compile(r"^demonstr\.\s+pron\.", re.I), "demonstrative pronoun"),
    (re.compile(r"^interrog\.", re.I), "interrogative"),
    (re.compile(r"^imper\.", re.I), "imperative"),
    (re.compile(r"^inf\.", re.I), "infinitive"),
    (re.compile(r"^excl\.", re.I), "exclamation"),
    (re.compile(r"^num\.", re.I), "numeral"),
]


def extract_pos_from_chunk(text: str) -> str | None:
    for rx, label in _FAULKNER_POS_PATTERNS:
        if rx.match(text):
            return label
    return None


# Reuse the citation regex from the earlier pass (full table).
SOURCE_MAP = {
    "Caminos, Lit. Frag.": "Caminos, Literary Fragments",
    "Lit. Frag.": "Literary Fragments",
    "P. Kah.": "Kahun Papyrus", "P. Ram.": "Ramesseum Papyri",
    "P. Ed.": "Edwin Smith Papyrus", "P. Eb.": "Ebers Papyrus",
    "P. Harris": "Papyrus Harris", "Sh. S.": "Shipwrecked Sailor",
    "M. u. K.": "Mutter und Kind", "T. Carn.": "Tablette Carnarvon",
    "Th. T.": "Theban Tomb", "D. el Geb.": "Deir el-Gebrawi",
    "D. el Bah.": "Deir el-Bahari", "Mar. Mast.": "Mariette, Mastabas",
    "Mar. Karn.": "Mariette, Karnak", "Mar. Abyd.": "Mariette, Abydos",
    "Dav. Ptah.": "Davies, Ptahhotep", "Hor. and Suty": "Horemheb and Suty Stela",
    "Rec. trav.": "Recueil de Travaux", "Bull. Inst.": "Bulletin de l'Institut",
    "Adm. p.": "Admonitions of Ipuwer", "Gr. p.": "Gardiner's Egyptian Grammar",
    "Gr. §": "Gardiner's Egyptian Grammar", "Ram. p.": "Ramesseum Papyrus",
    "Urk.": "Urkunden", "Sin.": "Sinuhe", "Peas.": "Eloquent Peasant",
    "Pyr.": "Pyramid Texts", "BD": "Book of the Dead", "Westc.": "Westcar Papyrus",
    "Eb.": "Ebers Papyrus", "Gr.": "Gardiner's Egyptian Grammar",
    "Adm.": "Admonitions of Ipuwer", "RB": "Sethe, Reading Book",
    "TR": "Theban Recension", "BH": "Beni Hasan",
    "JEA": "Journal of Egyptian Archaeology",
    "ZÄS": "Zeitschrift für Ägyptische Sprache",
    "PSBA": "Proceedings of the Society of Biblical Archaeology",
    "Hatnub": "Hatnub Graffiti", "Leb.": "Dispute of a Man with his Ba",
    "Les.": "Sethe, Lesestücke", "GAS": "Gardiner, Admonitions Studies",
    "GNS": "Gardiner, Notes on Sinuhe", "AEO": "Ancient Egyptian Onomastica",
    "CT": "Coffin Texts", "Sm.": "Edwin Smith Papyrus",
    "Pr.": "Ptahhotep (Prisse)", "Mill.": "Millingen Papyrus",
    "Siut": "Siut Tomb", "BM": "British Museum",
    "Bersh.": "Bersheh", "Hamm.": "Hammamat",
    "Hymnen": "Egyptian Hymns", "Bull.": "Bulletin",
    "Louvre": "Louvre", "Piankhi": "Piankhi Stela",
    "Merikarē": "Instruction for King Merikare",
    "Merikare": "Instruction for King Merikare",
    "Sethe": "Sethe", "COA": "City of Akhenaten",
    "Cair.": "Cairo Museum", "Berl.": "Berlin Museum", "TT": "Theban Tomb",
}

_ABBREVS = sorted(SOURCE_MAP.keys(), key=lambda s: -len(s))
_ABBREV_ALT = "|".join(re.escape(a) for a in _ABBREVS)
_LOCATION_PAT = (
    r"(?:"
    r"§§?\s*\d+(?:[.,]\s*\d+)*"
    r"|p\.\s*\d+(?:,\s*[A-Za-z]?\d+(?:[.,]\s*\d+)*)*"
    r"|pl\.\s*\d+(?:[.,]\s*\d+)*"
    r"|[A-Z]?\d+(?:\s*-\s*\d+)?(?:\.\d+)*"
    r"(?:\s*,\s*[A-Z]?\d+(?:\s*-\s*\d+)?(?:\.\d+)*)*"
    r"[a-z]?"
    r")"
)
_CITATION_RX = re.compile(
    r"(?P<abbrev>" + _ABBREV_ALT + r"),?\s+"
    r"(?:(?P<volume>[IVX]+)[,;]?\s+)?"
    r"(?P<location>" + _LOCATION_PAT + r")",
    flags=re.UNICODE,
)


def _has_clean_context(text: str, pos: int) -> bool:
    if pos == 0:
        return True
    prev = text[pos - 1]
    if prev in ",;:([{ \n\t":
        return True
    if pos >= 2 and text[pos - 2:pos] in (". ", "! ", "? "):
        return True
    return False


def extract_citations(text: str) -> list[dict]:
    out = []
    if not text:
        return out
    pos = 0
    while pos < len(text):
        m = _CITATION_RX.search(text, pos)
        if not m:
            break
        if not _has_clean_context(text, m.start()):
            pos = m.end()
            continue
        abbrev = m.group("abbrev")
        volume = m.group("volume")
        location = m.group("location").strip(",;:.")
        raw = text[m.start():m.end()].strip(",; ")
        cit = {
            "abbreviation": abbrev,
            "source": SOURCE_MAP.get(abbrev),
            "location": location,
            "raw": raw,
        }
        if volume:
            cit["volume"] = volume
        out.append(cit)
        pos = m.end()
    return out


def split_subglosses(translation: dict) -> list[dict]:
    """
    If the translation text starts with "(1) ... (2) ...", split into a list
    of new translation dicts (each inheriting metadata). Otherwise return
    [translation] unchanged.
    """
    text = (translation.get("translation") or "").strip()
    if not _SUBGLOSS_HEAD.match(text):
        return [translation]
    # Quick guard: must contain at least (2)
    if "(2)" not in text:
        return [translation]

    chunks = _SUBGLOSS_SPLIT.split(text)
    if len(chunks) < 2:
        return [translation]

    base_md = translation.get("TranslationMetadata") or {}
    parent_pos = base_md.get("PartOfSpeech")
    parent_html = translation.get("translation_html")

    new_translations = []
    for chunk in chunks:
        m = _SENSE_LABEL.match(chunk)
        if not m:
            continue
        sense_no = int(m.group(1))
        body = chunk[m.end():].strip()
        if not body:
            continue
        # Derive POS for this sense (Faulkner abbreviations at start)
        chunk_pos = extract_pos_from_chunk(body)
        new_md = dict(base_md)
        if chunk_pos:
            new_md["PartOfSpeech"] = chunk_pos
        else:
            new_md["PartOfSpeech"] = parent_pos
        new_md["SenseNumber"] = sense_no
        new_t = {
            "translation": body,
            "TranslationMetadata": new_md,
        }
        if parent_html:
            new_t["translation_html"] = parent_html
        cits = extract_citations(body)
        if cits:
            new_t["Citations"] = cits
        new_translations.append(new_t)

    # If splitting produced nothing usable, fall back to original
    return new_translations or [translation]


# ---------------------------------------------------------------------------
# I. q.v. cross-references
# ---------------------------------------------------------------------------

# Find the target word immediately before ", q.v."
# Patterns:
#   "<word> 'gloss', q.v."         e.g. "in wDa-rwt 'judge', q.v."
#   "earlier <word>, q.v."         e.g. "Earlier ina, q.v."
#   "var. of <word>, q.v."         e.g. "var. of foo, q.v."

_QV_TARGETS = [
    re.compile(r"\b([\w][\w.-]*)\s+[‘'\"][^’'\"]+[’'\"][,\s]+q\.v\."),
    re.compile(r"\bearlier\s+([\w][\w.-]*)[,\s]+q\.v\.", re.I),
    re.compile(r"\bvar\.\s+of\s+([\w][\w.-]*)[,\s]+q\.v\.", re.I),
    re.compile(r"\bnext\s+below[,\s]+q\.v\."),  # no extractable target
]


def extract_qv_targets(text: str) -> list[str]:
    targets = []
    for rx in _QV_TARGETS[:-1]:
        for m in rx.finditer(text or ""):
            tgt = m.group(1)
            # Filter false matches: must look like a Middle Egyptian
            # transliteration token (not a common English word).
            if tgt.lower() in {"the", "a", "an", "of", "and", "is", "in",
                               "see", "also", "as", "with", "or", "but",
                               "from", "for", "by", "than", "than", "for",
                               "below", "above", "next"}:
                continue
            if tgt not in targets:
                targets.append(tgt)
    return targets


# ---------------------------------------------------------------------------
# J. Corpus file mapping
# ---------------------------------------------------------------------------

# Build the abbreviation+version-letter -> filename mapping by inspecting
# the actual corpus folder.
NEDERHOF_DIR = HERE.parent.parent.parent / "EgyptianTranslation/texts/nederhof-texts"

# Patterns mapping (abbreviation, optional location-prefix) -> filename stem.
def build_corpus_map() -> dict:
    """Map (source_abbrev, version_prefix) -> filename."""
    if not NEDERHOF_DIR.exists():
        return {}
    files = {f.name for f in NEDERHOF_DIR.iterdir() if f.suffix == ".txt"}
    m = {}

    def reg(key, fname):
        if fname in files:
            m[key] = fname

    # Sinuhe witnesses
    for ver in ("B", "R", "G", "L", "BA", "AOS"):
        reg(("Sin.", ver), f"SinuheTr{ver}.txt")
    # Peasant witnesses
    for ver in ("B1", "B2", "R"):
        reg(("Peas.", ver), f"PeasantTr{ver}.txt")
    # Ptahhotep witnesses (Prisse and DE)
    reg(("Pr.", None), "PtahhotepTrP.txt")
    # Common single-version sources
    reg(("Sh. S.", None), "ShipwreckedTr.txt")
    reg(("Westc.", None), "WestcarTr.txt")
    reg(("Leb.", None), "DisputeTr.txt")
    reg(("Eb.", None), "EbersTr.txt")
    reg(("Hatnub", None), "HatnubGr24Tr.txt")
    reg(("Hamm.", "110"), "Hammamat110Tr.txt")
    reg(("Hamm.", "113"), "Hammamat113Tr.txt")
    reg(("Hamm.", "191"), "Hammamat191Tr.txt")
    reg(("Hamm.", "192"), "Hammamat192Tr.txt")
    return m


def lookup_corpus_file(citation: dict, corpus_map: dict) -> str | None:
    abbrev = citation.get("abbreviation")
    loc = citation.get("location", "") or ""
    if not abbrev:
        return None
    # Versioned lookup: leading capital letter of location is the witness
    m = re.match(r"^([A-Z][A-Za-z]?\d*)", loc)
    if m:
        ver = m.group(1)
        # Try with exact prefix first
        key = (abbrev, ver)
        if key in corpus_map:
            return corpus_map[key]
        # Strip trailing digits and try again ("B1" -> "B")
        ver_strip = re.sub(r"\d+$", "", ver)
        if ver_strip and (abbrev, ver_strip) in corpus_map:
            return corpus_map[(abbrev, ver_strip)]
    # Versionless fallback
    if (abbrev, None) in corpus_map:
        return corpus_map[(abbrev, None)]
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    corpus_map = build_corpus_map()
    print(f"Corpus map keys: {len(corpus_map)}")

    # G: RelatedWords
    g_added = 0
    g_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            html = t.get("translation_html","") or ""
            if "<canvas" not in html:
                continue
            rel = extract_related_words(html)
            if rel:
                t["RelatedWords"] = rel
                g_added += sum(1 for _ in rel)
                if len(g_examples) < 4 and any(r.get("transliteration") for r in rel):
                    g_examples.append((e["Transliteration"], rel[:3]))
    print(f"\nG. RelatedWords entries added: {g_added:,}")
    for tr, rel in g_examples:
        print(f"   {tr}: {rel}")

    # H: split sub-glosses
    h_splits = 0
    h_new_translations = 0
    for e in entries:
        new_ts = []
        for t in e.get("Translations") or []:
            result = split_subglosses(t)
            if len(result) > 1:
                h_splits += 1
                h_new_translations += len(result) - 1
            new_ts.extend(result)
        e["Translations"] = new_ts
    print(f"\nH. Translations split into senses: {h_splits} multi-sense translations -> +{h_new_translations} new translation records")

    # I: q.v. cross-references
    i_qv = 0
    i_examples = []
    for e in entries:
        for t in e.get("Translations") or []:
            text = t.get("translation","") or ""
            if "q.v." not in text:
                continue
            targets = extract_qv_targets(text)
            if targets:
                t["SeeAlso"] = targets
                i_qv += 1
                if len(i_examples) < 4:
                    i_examples.append((e["Transliteration"], targets))
    print(f"\nI. SeeAlso fields populated from q.v.: {i_qv}")
    for tr, tgts in i_examples:
        print(f"   {tr}: SeeAlso={tgts}")

    # J: corpus_file on citations
    j_added = 0
    j_by_file = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            for c in t.get("Citations") or []:
                fname = lookup_corpus_file(c, corpus_map)
                if fname:
                    c["corpus_file"] = fname
                    j_added += 1
                    j_by_file[fname] += 1
    print(f"\nJ. corpus_file added to citations: {j_added:,}")
    print(f"   distinct files referenced: {len(j_by_file)}")
    for f, n in j_by_file.most_common(10):
        print(f"     {n:5}  {f}")

    # K: no-op
    print("\nK. HTML residue: no-op (clean already).")

    # Write back
    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        total = 0
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
            total += 1
    print(f"  wrote {total:,} entries")


if __name__ == "__main__":
    main()
