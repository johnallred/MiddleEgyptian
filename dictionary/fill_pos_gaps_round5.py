"""
Round 5 of POS gap-filling on Entries2.json (final round).

Round 4 brought coverage to 99.73% (165 still null). The residual falls
into four small clusters:

  T1. Single-word capitalized proper nouns / titles:
      "Nubia", "Asia", "Unas", "Servant", "Pilot" -> proper noun (or
      noun title for occupation-like words).

  T2. Pure parenthesized glosses where the meaningful content is inside
      the parens: "(in)", "(appointed)", "(unknown plant)", "(part of a
      feminine title)" -> strip the parens and re-classify the inner.

  T3. Vocative / interjection markers: "O !", "O" -> interjection.

  T4. Verbal-marker glosses: "'past tense' marker", "'future tense'
      marker", "imperfective marker" -> particle (modal/aspect marker).
"""

import json
import re
from collections import Counter
from pathlib import Path

ENTRIES = Path(__file__).parent / "Entries2.json"


_TAG = re.compile(r"<[^>]+>")
_OUTER_PAREN = re.compile(r"^\s*\(([^)]+)\)\s*$")


def strip_tags(text):
    return _TAG.sub("", text or "").strip()


# Common capitalized words that are titles (occupations)
_TITLE_WORDS = {
    "servant", "pilot", "scribe", "soldier", "priest", "priestess",
    "judge", "officer", "official", "general", "captain",
    "physician", "doctor", "potter", "baker", "brewer", "fisherman",
    "fowler", "farmer", "herdsman", "shepherd", "smith", "carpenter",
    "mason", "messenger", "envoy", "ambassador", "magistrate",
    "governor", "mayor", "treasurer", "steward", "overseer",
    "supervisor", "manager", "guardian", "warden", "keeper",
    "watchman", "guard", "warrior", "hunter", "musician", "singer",
    "dancer", "actor", "performer", "labourer", "laborer", "worker",
    "craftsman", "artisan", "noble", "lord", "lady", "master",
    "mistress", "king", "queen", "prince", "princess", "pharaoh",
}


def gloss_rule_round5(text: str) -> tuple[str | None, str | None]:
    raw = re.sub(r"\s+", " ", strip_tags(text)).strip()
    if not raw:
        return None, None

    # T3: vocative interjection
    if raw in ("O !", "O", "O!", "ah", "ha", "lo", "behold"):
        return "interjection", "interjection"
    if raw.startswith(("O,", "O ", "Oh,", "Oh ")) and len(raw) <= 4:
        return "interjection", "interjection"

    # T4: tense/aspect marker glosses
    if re.search(r"\b(past|future|present|perfective|imperfective)\s+tense\b", raw, re.I) \
       and "marker" in raw.lower():
        return "particle", "particle"
    if "marker" in raw.lower() and any(
        w in raw.lower() for w in ("modal", "aspect", "tense", "negative", "interrogative")
    ):
        return "particle", "particle"

    # T2: pure parenthesized gloss — recurse on inner content
    head = raw.split(",")[0].split(";")[0].strip()
    m = _OUTER_PAREN.match(head)
    if m:
        inner = m.group(1).strip()
        if inner:
            # Recurse with the inner text
            pos, core = gloss_rule_round5(inner)
            if pos:
                return pos, core
            # Specific cases for parenthesized inner content
            inner_low = inner.lower()
            if inner_low.startswith(("in ", "at ", "on ", "to ", "from ", "by ")) or inner_low == "in":
                return "preposition", "preposition"
            if inner_low in ("appointed", "approved", "completed", "ready"):
                return "adjective", "adjective"
            if inner_low.startswith("unknown") or inner_low.startswith("part of"):
                return "noun", "noun"
            # Otherwise default to noun (parenthesized glosses are usually
            # descriptive noun phrases in Egyptian dictionaries).
            return "noun", "noun"

    # T1: single-word capitalized
    if " " not in head and head and head[0].isupper() and not head.isupper():
        lower = head.lower().strip(".,*!")
        if lower in _TITLE_WORDS:
            return "noun title", "noun"
        # Otherwise treat as proper noun
        return "proper noun", "noun"

    return None, None


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    rfilled = 0
    rby_pos = Counter()
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            pos, core = gloss_rule_round5(t.get("translation", "") or "")
            if pos:
                md["PartOfSpeech"] = pos
                if not md.get("PartOfSpeechCore"):
                    md["PartOfSpeechCore"] = core
                t["TranslationMetadata"] = md
                rfilled += 1
                rby_pos[pos] += 1
    print(f"\nT1-T4 gloss rules: {rfilled:,}")
    for pos, n in rby_pos.most_common():
        print(f"  -> {pos}: {n}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
