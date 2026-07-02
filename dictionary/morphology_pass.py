"""
Morphology + gloss pass to fill remaining null POS values in Entries2.json.

Reads and writes Entries2.json in place.

Design
------
The Vygus cross-fill and Faulkner HTML-abbreviation passes leave a long tail
of translations whose PartOfSpeech is still null. For those, we have only two
signals: the Egyptian transliteration itself and the English translation gloss.

Each rule must be conservative: we'd rather leave a translation null than
guess wrong. Every rule cross-checks transliteration morphology against the
gloss before firing, and the rule that fires is recorded so the output is
auditable.

Rules, applied in order; first match wins.

  R1  "to X" gloss                          -> verb
        Faulkner / Dickson convention for an infinitive entry.
        Example: "to enter, depart" -> verb.

  R2  ".n.f" / ".n .f" / ".tw" verb forms   -> verb
        Translit contains the sDm.n.f past or .tw passive marker. These
        morphemes are diagnostic.

  R3  "be ADJ" gloss                        -> verb
        Stative / pseudo-verbal; Egyptian state verbs are conventionally
        verbs in the dictionary tradition (e.g. "be tall").

  R4  Article-led nominal phrase            -> noun
        Gloss starts with "a/an/the/kind of/name of/type of/sort of/
        species of/variety of".

  R5  Feminine -t ending + nominal gloss    -> feminine noun
        Translit ends in 't' (not '.t', not double 'tt'), AND the gloss does
        not start with a verb-form English word. The 't' suffix is the
        Egyptian feminine marker.

  R6  Plural -w / -wt ending + plural gloss -> plural noun
        Translit ends in 'w' or 'wt' AND the gloss contains a plural-noun
        marker (plural English word like "ones", "men", "people", "those",
        or an English -s plural at the end).

  R7  Nisbe -y ending + adjective gloss     -> adjective
        Translit ends in 'y' (single trailing y, not 'iy'/'yy') AND the gloss
        is a short adjective form (English word in a known adjective list,
        or simply a single short non-verb gloss).

  R8  Multi-word adverb / preposition gloss -> preposition / adverb
        Translit contains a space AND gloss starts with one of a small set
        of preposition / adverb words ("upon", "before", "with", "of",
        "into", "from", "by", "for", "in").

Anything not matching is left null.
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
ENTRIES = HERE / "Entries2.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TAG = re.compile(r"<[^>]+>")
_SP = re.compile(r"\s+")


def strip_html(s: str) -> str:
    return _SP.sub(" ", _TAG.sub("", s or "")).strip()


def dict_name(md):
    v = md.get("DictionaryName")
    if isinstance(v, dict):
        return v.get("$numberInt") or v.get("$numberLong")
    return str(v) if v is not None else None


def first_gloss(text: str) -> str:
    """Cut off at first ';' or '.' followed by space (Faulkner's citation
    delimiter), and at first comma to get just the leading sense."""
    t = strip_html(text)
    # Drop trailing source citations like ", Sin. B70; Urk. IV, 1234."
    t = re.split(r",\s+[A-Z]{1,5}\.\s", t, maxsplit=1)[0]
    t = t.split(";")[0]
    return t.strip()


# Known English verbs that frequently appear as bare infinitive at the
# start of an Egyptian dictionary gloss. Used only to guard against false
# positives in the noun-tagging rules; not used to tag verbs directly.
COMMON_VERB_STARTS = {
    "be", "do", "go", "say", "make", "come", "take", "give", "see", "hear",
    "die", "live", "rise", "fall", "run", "fly", "eat", "drink", "sit",
    "stand", "walk", "speak", "look", "find", "send", "bring", "carry",
    "cause", "let", "build", "open", "shut", "close", "lift", "raise",
    "spread", "shine", "weep", "smell", "praise", "fight", "kill", "beat",
    "stir", "knead", "rejoice", "embrace", "flee", "depart", "enter",
    "leave", "return", "appear", "become", "begin", "end", "seek", "guard",
    "follow", "lead", "command", "destroy", "create", "fashion", "shape",
    "form", "save", "rescue", "throw", "place", "set", "put", "wash",
    "clean", "wear", "drive", "anoint", "dry", "fill", "empty", "pour",
    "neglect", "test", "prove", "answer", "ask", "tell", "name", "call",
    "release", "untie", "tie", "bind", "loose", "draw", "pull", "push",
    "hold", "grasp", "seize", "catch",
}

# Common English adjective forms that often appear as Egyptian glosses.
COMMON_ADJ = {
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
    "splendid", "famous",
}

PREPOSITION_STARTS = {
    "upon", "before", "behind", "after", "into", "from", "with", "by",
    "for", "in", "on", "to", "of", "above", "below", "under", "over",
    "without", "through", "among", "between", "according",
}

ARTICLE_PATTERNS = (
    "a ", "an ", "the ",
    "kind of ", "name of ", "type of ", "sort of ", "species of ",
    "variety of ", "title of ",
)


def gloss_starts_with_verb(gloss: str) -> bool:
    """Heuristic: does the gloss start with an English verb-form word?"""
    head = gloss.lower().split()
    if not head:
        return False
    first = head[0].strip(".,()")
    return first in COMMON_VERB_STARTS


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def classify(translit: str, gloss_raw: str) -> tuple[str, str] | tuple[None, None]:
    """
    Return (pos_label, rule_id) or (None, None) when no rule fires.
    """
    if not gloss_raw:
        return None, None

    gloss = first_gloss(gloss_raw)
    g_low = gloss.lower()

    # R1 ----------------------------------------------------------------------
    if re.match(r"^to\s+[a-z]", g_low):
        return "verb", "R1_to_verb"

    # R2 ----------------------------------------------------------------------
    # sDm.n.f past or .tw passive in the transliteration itself.
    if re.search(r"\.n\b", translit) and re.search(r"\.[fksjnT]", translit):
        return "verb", "R2_sDm_n_f"
    if ".tw" in translit:
        return "verb", "R2_tw_passive"

    # R3 ----------------------------------------------------------------------
    m = re.match(r"^be\s+([a-z]+)", g_low)
    if m:
        return "verb", "R3_be_X"

    # R4 ----------------------------------------------------------------------
    for prefix in ARTICLE_PATTERNS:
        if g_low.startswith(prefix):
            return "noun", "R4_article_noun"

    # R8 ----------------------------------------------------------------------
    if " " in translit:
        first_word = g_low.split()[0] if g_low.split() else ""
        if first_word in PREPOSITION_STARTS:
            return "preposition", "R8_prep_multiword"

    # R5/R6/R7 inspect the END of the transliteration as an Egyptian morpheme.
    # That assumption only holds for SINGLE-WORD entries: in "iry at" the
    # final 't' belongs to the second word "at", not to the headword.
    single_word_translit = " " not in translit.strip()

    # R5 ----------------------------------------------------------------------
    # Feminine -t ending. Single trailing 't' (not 'tt' doubled, not '.t').
    if single_word_translit and re.search(r"[^t.]t$", translit) and not gloss_starts_with_verb(gloss):
        # Cross-check: gloss should look nominal (not start with a verb word).
        if re.match(r"^[a-z][a-z -]*[a-z]\.?$", g_low) or any(
            g_low.startswith(p) for p in ARTICLE_PATTERNS
        ):
            return "feminine noun", "R5_t_fem_noun"

    # R6 ----------------------------------------------------------------------
    if single_word_translit and re.search(r"w[t]?$", translit) and not gloss_starts_with_verb(gloss):
        plural_markers = (" ones", " men", " people", " those", "soldiers",
                          "priests", "officials", "children", "enemies",
                          "wives", "subjects", "fields", "lands", "gods",
                          "places")
        # English -s plural at end of single-word gloss
        m_plural = re.match(r"^[a-z]+s$", g_low) and not g_low.endswith("ss")
        if m_plural or any(mk in g_low for mk in plural_markers):
            return "plural noun", "R6_w_plural_noun"

    # R7 ----------------------------------------------------------------------
    if single_word_translit and re.search(r"[^y]y$", translit):
        first_word = g_low.split()[0].strip(".,") if g_low.split() else ""
        if first_word in COMMON_ADJ:
            return "adjective", "R7_y_nisbe_adj"

    return None, None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Reading: {ENTRIES}")
    with open(ENTRIES, encoding="utf-8") as f:
        entries = [json.loads(l) for l in f if l.strip()]
    print(f"  loaded {len(entries):,} entries")

    rule_counts = Counter()
    by_source_rule = defaultdict(Counter)
    samples_per_rule = defaultdict(list)
    src_names = {"0": "Lexicon", "1": "Dickson", "2": "Vygus", "4": "Faulkner"}

    null_before = 0
    filled = 0
    for e in entries:
        translit = e.get("Transliteration", "")
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeech"):
                continue
            null_before += 1
            src = dict_name(md)
            pos, rule = classify(translit, t.get("translation", ""))
            if pos:
                md["PartOfSpeech"] = pos
                t["TranslationMetadata"] = md
                filled += 1
                rule_counts[rule] += 1
                by_source_rule[src_names.get(src, src)][rule] += 1
                if len(samples_per_rule[rule]) < 4:
                    samples_per_rule[rule].append(
                        (translit, first_gloss(t.get("translation", ""))[:80], pos)
                    )

    print(f"\nNull-POS translations before pass: {null_before:,}")
    print(f"Filled by morphology pass        : {filled:,}")
    print(f"Still null after pass            : {null_before - filled:,}")

    print("\n=== Fills by rule ===")
    for rule, n in rule_counts.most_common():
        print(f"  {n:5}  {rule}")

    print("\n=== Fills by source x rule ===")
    for src, counter in by_source_rule.items():
        print(f"  {src}:")
        for rule, n in counter.most_common():
            print(f"    {n:5}  {rule}")

    print("\n=== Samples per rule (max 4 each) ===")
    for rule, samples in samples_per_rule.items():
        print(f"  [{rule}]")
        for translit, gloss, pos in samples:
            print(f"    {translit:25}  -> {pos:18}  | {gloss}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
