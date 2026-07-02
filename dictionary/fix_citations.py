"""
Replace the Citations field in Entries2.json with a better extraction.

Bugs in the first pass:
  - "Urk. IV, 425, 8" came out as `location: "IV"` because the Roman volume
    alternative consumed "IV," and could not bridge to the page+line.
  - Mid-sentence Roman letters like "V" in "Adm. 2, 4. Va" were captured
    as a continuation volume, producing junk like "Adm. 2, 4. Va".
  - Duplicate "Urk." citations appeared because the matcher fired on each
    "Urk. <vol>" prefix without capturing the trailing page+line.

Fix:
  - Volume is captured ONLY immediately after the abbreviation, in a
    separate named group, never as a continuation.
  - Location is a clean numeric/alpha pattern that allows comma- and
    period-separated chunks plus an optional trailing letter (Eb. 2, 12a)
    and ranges (Urk. IV, 53-62).
  - One citation match per `<abbrev> [vol] <location>` instance; the
    scanner then continues from the end of that match to find the next.
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


SOURCE_MAP = {
    # Multi-word abbreviations (matched first by being longer)
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
    "Adm. p.": "Admonitions of Ipuwer",
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

_ABBREVS = sorted(SOURCE_MAP.keys(), key=lambda s: -len(s))
_ABBREV_ALT = "|".join(re.escape(a) for a in _ABBREVS)

# Location: page-style or paragraph-style or alphanumeric, with optional
# comma/period continuations and optional trailing single lowercase letter
# (Eb. 2, 12a) or numeric range (Urk. IV, 53-62).
_LOCATION = (
    r"(?:"
    r"§§?\s*\d+(?:[.,]\s*\d+)*"                                   # §245, §§80.263
    r"|p\.\s*\d+(?:,\s*[A-Za-z]?\d+(?:[.,]\s*\d+)*)*"             # p. 449, C11
    r"|pl\.\s*\d+(?:[.,]\s*\d+)*"                                  # pl. 13, 29
    r"|[A-Z]?\d+(?:\s*-\s*\d+)?(?:\.\d+)*"                         # 119 or 53-62 or 14.16
    r"(?:\s*,\s*[A-Z]?\d+(?:\s*-\s*\d+)?(?:\.\d+)*)*"              # ,5  ,12 etc.
    r"[a-z]?"                                                       # 12a
    r")"
)

_CITATION_RX = re.compile(
    r"(?P<abbrev>" + _ABBREV_ALT + r")"
    r",?\s+"
    r"(?:(?P<volume>[IVX]+)[,;]?\s+)?"
    r"(?P<location>" + _LOCATION + r")",
    flags=re.UNICODE,
)


# Context guard: abbreviation must appear at start of string, or after a
# clause boundary (comma, semicolon, colon, paren, period+space).
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
    citations = []
    if not text:
        return citations
    pos = 0
    while pos < len(text):
        m = _CITATION_RX.search(text, pos)
        if not m:
            break
        # Skip false matches lacking proper clause boundary context.
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
        citations.append(cit)
        pos = m.end()
    return citations


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]

    before_total = 0
    after_total = 0
    abbrev_hits = Counter()
    sample_translations = []
    for e in entries:
        for t in e.get("Translations") or []:
            before = t.get("Citations") or []
            before_total += len(before)
            new = extract_citations(t.get("translation", ""))
            if new:
                t["Citations"] = new
                after_total += len(new)
                for c in new:
                    abbrev_hits[c["abbreviation"]] += 1
                if len(sample_translations) < 5 and any(c.get("volume") for c in new):
                    sample_translations.append(
                        (e["Transliteration"], t.get("translation","")[:80], new[:4])
                    )
            elif before:
                t.pop("Citations", None)

    print(f"\nBefore: {before_total:,} citations")
    print(f"After : {after_total:,} citations")
    print(f"\nTop 12 abbreviations:")
    for ab, n in abbrev_hits.most_common(12):
        print(f"  {n:5}  {ab:18}  -> {SOURCE_MAP.get(ab,'?')}")

    print("\nSamples with volume captured:")
    for tr, gloss, cits in sample_translations:
        print(f"  {tr:14} | {gloss}")
        for c in cits:
            print(f"     {c}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")


if __name__ == "__main__":
    main()
