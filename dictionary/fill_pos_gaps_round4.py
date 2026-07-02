"""
Round 4 of POS gap-filling on Entries2.json.

Round 3 brought coverage to 98.3% (1,046 still null).

Looking at the residue, almost all are multi-word compound expressions:
verb phrases ("get in front of", "make inspection of", "act properly"),
preposition phrases ("down to", "as far as", "at his times"), particle
phrases ("there is not", "old negative particle"), and concrete noun
compounds ("river mouth", "ten-day week", "disaffected man").

  S1. Verb-phrase glosses: expanded verb-form English-word vocabulary.
      "get/make/act/show/feel/look/hear/think/say/do/give X" -> verb.

  S2. Existential / negative particle glosses: "there is/are/was/were
      [not]" -> particle.

  S3. Preposition + the/his/her/its glosses: "to the X", "at his X",
      "by his X", "in his X" -> preposition.

  S4. "old <particle/article/etc>" / "early <particle>" / etc. classifier
      glosses describe their POS literally.

  S5. Default fallback: if all else fails AND the gloss begins with a
      lowercase letter (not a verb-form word), tag as `noun`. The
      Egyptian-dictionary convention is that bare lowercase glosses for
      concrete-meaning entries are nouns.

After this pass we expect well over 99% coverage. The remaining null
entries will be the genuinely ambiguous or anomalous cases.
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


_VERB_STARTS = {
    # round 1-3 vocabulary
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
    "hold", "grasp", "seize", "catch", "pound", "cut", "trim", "scratch",
    "carve", "engrave", "steal", "rob", "march", "travel", "sleep", "wake",
    # round 4 additions
    "get", "act", "show", "feel", "think", "know", "learn", "teach",
    "remember", "forget", "wonder", "doubt", "fear", "love", "hate",
    "want", "wish", "hope", "expect", "intend", "plan", "decide",
    "choose", "select", "prefer", "agree", "refuse", "accept", "deny",
    "admit", "promise", "swear", "lie", "shout", "whisper", "sing",
    "dance", "play", "work", "serve", "rule", "govern", "judge",
    "punish", "reward", "honour", "honor", "worship", "adore",
    "address", "greet", "approach", "withdraw", "advance", "retreat",
    "halt", "rest", "wait", "watch", "guard", "protect", "defend",
    "attack", "strike", "wound", "heal", "cure", "feed", "nourish",
    "raise", "bear", "carry", "deliver", "exit", "go", "enter",
    "spend", "waste", "save", "store", "collect", "gather", "harvest",
    "plant", "sow", "till", "plough", "plow", "reap", "thresh",
    "mill", "grind", "bake", "cook", "roast", "boil", "fry",
    "preserve", "ferment", "brew", "press",
}

_PARTICLE_GLOSS_HEADS = (
    "there is", "there are", "there was", "there were",
    "old negative", "old enclitic", "old particle",
    "particle of", "particle marking", "particle introducing",
    "not", "no ",
)

_PREP_HEADS_EXPANDED = (
    "to the", "in the", "from the", "at the", "by the", "on the",
    "into the", "with the", "of the", "for the",
    "to his", "at his", "by his", "in his", "from his", "with his",
    "to her", "at her", "by her", "in her", "from her", "with her",
    "to my", "to your", "to its",
    "down to", "up to", "out from", "as far as", "as much as",
    "as little as", "as the price of", "in exchange for",
    "by way of", "in the manner of", "in the form of",
    "according to", "due to", "owing to", "thanks to",
    "in front of", "behind",
)


def gloss_rule_round4(text: str) -> tuple[str | None, str | None]:
    raw = re.sub(r"\s+", " ", (text or "")).strip()
    if not raw:
        return None, None
    raw_low = raw.lower()
    parts = raw_low.split()
    if not parts:
        return None, None

    # S1: verb-phrase start
    first = parts[0].strip(".,")
    if first in _VERB_STARTS:
        return "verb", "verb"

    # S2: existential / particle phrases
    for head in _PARTICLE_GLOSS_HEADS:
        if raw_low.startswith(head):
            return "particle", "particle"

    # S3: preposition phrases
    for head in _PREP_HEADS_EXPANDED:
        if raw_low.startswith(head + " ") or raw_low == head:
            return "preposition", "preposition"

    # S4: "old/early <X>" classifier glosses
    if parts[0] in ("old", "early", "late") and len(parts) >= 2:
        second = parts[1].strip(".,")
        if second in {"negative", "enclitic", "particle", "form", "version"}:
            return "particle", "particle"

    # S5: lowercase fallback -> noun
    head = first_gloss_clean(text)
    if head and head[0].isalpha() and head[0].islower():
        # Don't apply to gloss starting with a verb word (handled above) or
        # an article (those should have been caught earlier).
        if first not in _VERB_STARTS:
            return "noun", "noun"

    return None, None


# Core derivation reused
POS_TOKENS = {
    "noun", "verb", "adjective", "pronoun", "particle", "preposition",
    "adverb", "conjunction", "interjection", "interrogative", "infinitive",
    "imperative", "participle", "numeral", "exclamation", "article",
    "unknown",
}


def derive_core(label):
    if not label:
        return None
    for tok in label.strip().lower().split():
        if tok in POS_TOKENS:
            return tok
    return None


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
            pos, core = gloss_rule_round4(t.get("translation", "") or "")
            if pos:
                md["PartOfSpeech"] = pos
                if not md.get("PartOfSpeechCore"):
                    md["PartOfSpeechCore"] = core
                t["TranslationMetadata"] = md
                rfilled += 1
                rby_pos[pos] += 1
    print(f"\nS1-S5 gloss rules: {rfilled:,}")
    for pos, n in rby_pos.most_common():
        print(f"  -> {pos}: {n}")

    # Final Core derivation
    core_filled = 0
    for e in entries:
        for t in e.get("Translations") or []:
            md = t.get("TranslationMetadata") or {}
            if md.get("PartOfSpeechCore") or not md.get("PartOfSpeech"):
                continue
            core = derive_core(md["PartOfSpeech"])
            if core:
                md["PartOfSpeechCore"] = core
                core_filled += 1
    print(f"\nFinal Core derivation: {core_filled}")

    print(f"\nWriting: {ENTRIES}")
    with open(ENTRIES, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")
    print(f"  wrote {len(entries):,} entries")


if __name__ == "__main__":
    main()
