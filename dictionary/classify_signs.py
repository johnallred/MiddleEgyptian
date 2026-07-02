"""
Classify every Gardiner sign used in Entries2.json by its phonetic /
functional role, using res_signinfo.js as the reference.

Output (written to ./sign_classification/):

  signs_phonetic.json
      Four sections: uniliteral, biliteral, triliteral, "4plus".
      Each sign is placed in the section corresponding to the consonant
      count of its primary (first) Mnemonic. Multi-mnemonic signs are
      filed by their primary; alternates are recorded for traceability.

  signs_determinative.json
  signs_logogram.json
  signs_phonetic_determinative.json
  signs_use_as_variant.json
  signs_other_phonetic.json    # signs with a Phon. usage but no Mnemonics
      One file per non-phonetic-class functional category, for signs
      that don't carry a Mnemonics field. Each sign can appear in more
      than one of these files when its entry documents multiple roles.

  signs_unclassified.json
      Signs used in Entries2.json that have no entry in res_signinfo.js
      OR have an entry with no recognizable classification at all.

Console: per-category overview with sign-count and total occurrences.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DICT_DIR = Path(__file__).parent
ENTRIES = DICT_DIR / "Entries2.json"
SIGNINFO = DICT_DIR.parent / "res" / "res_signinfo.js"
OUT_DIR = DICT_DIR / "sign_classification"


# ---------------------------------------------------------------------------
# Parse res_signinfo.js
# ---------------------------------------------------------------------------

# Entry header pattern: NAME:'...content...'
_ENTRY_RX = re.compile(r"^([A-Za-z]{1,3}\d+[a-z]?):'", re.MULTILINE)

# Strip HTML tags but keep inner text
_TAG = re.compile(r"<[^>]+>")


def parse_signinfo() -> dict[str, dict]:
    """Return {sign_code: {description, mnemonics, classifications}}."""
    with open(SIGNINFO, encoding="utf-8") as f:
        content = f.read()
    # Locate each entry by its start position
    positions = [(m.group(1), m.end()) for m in _ENTRY_RX.finditer(content)]
    positions.append((None, len(content)))

    signs = {}
    for i, (sign, start) in enumerate(positions[:-1]):
        # Find the body up to the next entry's quote
        end = positions[i + 1][1] if positions[i + 1][1] else len(content)
        # We need the body from `start` until the closing `',` of THIS entry.
        # Simple heuristic: read until the next entry's header (a line like
        # XX:'). That gives a slight overrun but the regex below tolerates it.
        body = content[start:end]
        # Trim at the final `',` before the next entry's header
        close = body.rfind("'")
        if close > 0:
            body = body[:close]

        text = _TAG.sub(" ", body)
        text = re.sub(r"\s+", " ", text).strip()

        # Description: text after the FIRST occurrence of "<sign>: ", up to the
        # first period. Use re.search because the HTML strip prepends a copy of
        # the sign code from the leading <canvas> tag.
        desc_match = re.search(rf"\b{re.escape(sign)}\s*:\s*([^.<]+?)\.\s", text)
        description = desc_match.group(1).strip() if desc_match else ""

        # Mnemonics — comma-separated transliteration values
        mnem_match = re.search(r"Mnemonics:\s*([^.<]+?)\s*\.", text)
        mnemonics_raw = mnem_match.group(1).strip() if mnem_match else ""
        mnemonics_list = [m.strip() for m in mnemonics_raw.split(",") if m.strip()] if mnemonics_raw else []

        # Detect functional classifications by scanning the entry body for
        # the leading tag of each <li>.
        classifications = set()
        if re.search(r"\bDet\.\s", text):
            classifications.add("determinative")
        if re.search(r"\bLog\.\s", text):
            classifications.add("logogram")
        if re.search(r"\bPhon\.\s+det\.", text):
            classifications.add("phonetic_determinative")
        if re.search(r"\bPhon\.\s+(?!det\.)", text):
            classifications.add("phonetic")
        if re.search(r"\bUse\s+as\b", text):
            classifications.add("use_as_variant")

        signs[sign] = {
            "description": description,
            "mnemonics": mnemonics_list,
            "classifications": sorted(classifications),
        }
    return signs


# ---------------------------------------------------------------------------
# Phonetic classification from mnemonic
# ---------------------------------------------------------------------------


def classify_mnemonic(mnemonic: str) -> str:
    """uniliteral / biliteral / triliteral / 4plus / numeric"""
    m = mnemonic.strip().rstrip(".,")
    if not m:
        return None
    if m.isdigit():
        return "numeric"
    n = len(m)
    if n == 1:
        return "uniliteral"
    if n == 2:
        return "biliteral"
    if n == 3:
        return "triliteral"
    return "4plus"


# ---------------------------------------------------------------------------
# Count sign occurrences in Entries2.json
# ---------------------------------------------------------------------------


def count_signs(entries) -> Counter:
    counter = Counter()
    for e in entries:
        gs = e.get("GardinerSigns") or ""
        for tok in gs.split():
            if tok:
                counter[tok] += 1
    return counter


_NORMALIZE_PREFIX = re.compile(r"^(Aa|AA)(\d+)([A-Za-z]?)$")
_NORMALIZE_SINGLE = re.compile(r"^([A-Z])(\d+)([A-Za-z])$")


def normalize_sign_to_signinfo(sign: str) -> str:
    """
    The dictionary writes signs like "AA1", "Z3A", "Y1V" (uppercase variant
    suffix). res_signinfo.js uses the standard convention: "Aa1" (lowercase
    second letter for the Aa prefix) and "Z3a" (lowercase trailing variant
    suffix). Convert dictionary form -> signinfo form for lookup.
    """
    m = _NORMALIZE_PREFIX.match(sign)
    if m:
        return "Aa" + m.group(2) + m.group(3).lower()
    m = _NORMALIZE_SINGLE.match(sign)
    if m:
        return m.group(1) + m.group(2) + m.group(3).lower()
    return sign


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("Parsing res_signinfo.js ...")
    sign_db = parse_signinfo()
    print(f"  {len(sign_db):,} signs in reference")

    print("Loading Entries2.json ...")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  {len(entries):,} entries")

    sign_counts = count_signs(entries)
    print(f"  {len(sign_counts):,} distinct sign codes used in entries")
    print(f"  {sum(sign_counts.values()):,} total sign occurrences")

    # Buckets
    phonetic: dict[str, dict] = {k: {} for k in ("uniliteral", "biliteral", "triliteral", "4plus")}
    non_phonetic: dict[str, dict] = {k: {} for k in
                                     ("determinative", "logogram",
                                      "phonetic", "phonetic_determinative",
                                      "use_as_variant")}
    unclassified: dict[str, dict] = {}
    numeric_signs: dict[str, dict] = {}

    for sign, count in sign_counts.items():
        info = sign_db.get(sign)
        # Try normalized form (dictionary "AA1"/"Z3A" -> signinfo "Aa1"/"Z3a")
        normalized = sign
        if info is None:
            normalized = normalize_sign_to_signinfo(sign)
            if normalized != sign:
                info = sign_db.get(normalized)
        if info is None:
            unclassified[sign] = {"count": count, "reason": "not in res_signinfo"}
            continue

        mnemonics = info["mnemonics"]
        classifications = info["classifications"]
        description = info["description"]

        placed = False

        # Phonetic by primary mnemonic
        if mnemonics:
            primary = mnemonics[0]
            phon_class = classify_mnemonic(primary)
            if phon_class == "numeric":
                numeric_signs[sign] = {
                    "count": count, "mnemonics": mnemonics,
                    "description": description,
                }
                placed = True
            elif phon_class:
                rec = {
                    "count": count,
                    "primary_mnemonic": primary,
                    "description": description,
                }
                if len(mnemonics) > 1:
                    rec["alt_mnemonics"] = mnemonics[1:]
                phonetic[phon_class][sign] = rec
                placed = True

        # Non-phonetic functional roles: only file the sign here if it
        # didn't already get a phonetic placement, OR if we want full
        # coverage. Per the spec, signs with a mnemonic go in the
        # phonetic file; only un-mnemoniced signs land in functional files.
        if not placed:
            for cls in classifications:
                rec = {
                    "count": count,
                    "description": description,
                }
                if cls in non_phonetic:
                    non_phonetic[cls][sign] = rec
                    placed = True

        if not placed:
            unclassified[sign] = {
                "count": count,
                "description": description,
                "reason": "no mnemonic and no recognized classification",
            }

    # ---- Write files ----
    OUT_DIR.mkdir(exist_ok=True)

    # Sort each bucket by descending occurrence
    def sort_dict(d):
        return dict(sorted(d.items(), key=lambda kv: (-kv[1]["count"], kv[0])))

    with open(OUT_DIR / "signs_by_phonetic_class.json", "w", encoding="utf-8") as f:
        json.dump({k: sort_dict(v) for k, v in phonetic.items()}, f,
                  ensure_ascii=False, indent=2)

    if numeric_signs:
        with open(OUT_DIR / "signs_numeric.json", "w", encoding="utf-8") as f:
            json.dump(sort_dict(numeric_signs), f, ensure_ascii=False, indent=2)

    # Rename the non-phonetic "phonetic" bucket on disk to avoid colliding
    # with the by-phonetic-class file above.
    DISK_NAMES = {
        "phonetic": "signs_phonetic_marker.json",
    }
    for cls, d in non_phonetic.items():
        if not d:
            continue
        fname = DISK_NAMES.get(cls, f"signs_{cls}.json")
        with open(OUT_DIR / fname, "w", encoding="utf-8") as f:
            json.dump(sort_dict(d), f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "signs_unclassified.json", "w", encoding="utf-8") as f:
        json.dump(sort_dict(unclassified), f, ensure_ascii=False, indent=2)

    # ---- Overview ----
    print("\n=== Sign classification overview ===")
    print("Phonetic classes (by mnemonic length):")
    for cls in ("uniliteral", "biliteral", "triliteral", "4plus"):
        d = phonetic[cls]
        n_signs = len(d)
        n_occ = sum(v["count"] for v in d.values())
        print(f"  {cls:18}: {n_signs:5,} signs / {n_occ:9,} occurrences in Entries2.json")
    if numeric_signs:
        n_signs = len(numeric_signs)
        n_occ = sum(v["count"] for v in numeric_signs.values())
        print(f"  {'numeric':18}: {n_signs:5,} signs / {n_occ:9,} occurrences")

    print("Non-phonetic functional classes (signs without Mnemonics):")
    for cls in ("determinative", "logogram", "phonetic",
                "phonetic_determinative", "use_as_variant"):
        d = non_phonetic[cls]
        if not d:
            continue
        n_signs = len(d)
        n_occ = sum(v["count"] for v in d.values())
        print(f"  {cls:25}: {n_signs:5,} signs / {n_occ:9,} occurrences")

    n_signs = len(unclassified)
    n_occ = sum(v["count"] for v in unclassified.values())
    print(f"\n  {'unclassified':25}: {n_signs:5,} signs / {n_occ:9,} occurrences")

    print(f"\nOutputs written to: {OUT_DIR}")
    for f in sorted(OUT_DIR.glob("*.json")):
        size = f.stat().st_size
        print(f"  {f.name:36}  {size:>9,} bytes")


if __name__ == "__main__":
    main()
