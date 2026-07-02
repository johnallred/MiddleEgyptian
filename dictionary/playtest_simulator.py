"""
Hieroglyph Quest playtest simulator.

Simulates the card game defined in game_material/deck.json + rules.md using
AI agents, runs thousands of games deterministically, and emits a balance
report flagging broken openers, dominant strategies, dead cards, and
seat-order advantage.

Design borrowed from PlaytestAI (https://github.com/TabletopFoundry/playtestai):
  - Deterministic seeded PRNG so any finding is reproducible.
  - Three agent strategies (Random, Greedy, Balanced) for comparison.
  - Per-card analytics (completion rate, usage rate).
  - Single-number balance score (0-100) summarizing the report.

Usage:
  python3 playtest_simulator.py                  # run default batch
  python3 playtest_simulator.py --games 20000    # bigger run
  python3 playtest_simulator.py --players 3      # 3-player table
  python3 playtest_simulator.py --seed 42        # reproducible run
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DICT_DIR = Path(__file__).parent
DECK_PATH = DICT_DIR / "game_material" / "deck.json"
OUT_DIR = DICT_DIR / "game_material" / "playtest_results"


# =============================================================================
# Game state
# =============================================================================


@dataclass
class SignCard:
    code: str          # Gardiner code e.g. "G17"
    cls: str           # "uniliteral" / "biliteral" / "triliteral" / "4plus"
    mnemonic: str      # e.g. "m"

    def __repr__(self):
        return f"{self.code}({self.mnemonic})"


@dataclass
class WordCard:
    translit: str
    english: list[str]
    sign_count: int
    points: int
    valid_spellings: list[list[str]]   # each spelling is a list of sign codes
    pos: Optional[str]
    determinatives: list = field(default_factory=list)  # v8.11 optional rule
    honorific: bool = False                             # v8.11 optional rule

    def __repr__(self):
        return f"Word({self.translit}, {self.points}pt)"


@dataclass
class LogogramCard:
    sign_code: str
    target_word: str
    description: str

    def __repr__(self):
        return f"Logo({self.sign_code}={self.target_word})"


@dataclass
class Player:
    pid: int
    agent_name: str
    hand_signs: list[SignCard] = field(default_factory=list)
    hand_logos: list[LogogramCard] = field(default_factory=list)
    active_word: Optional[WordCard] = None
    score: int = 0
    words_completed: list[WordCard] = field(default_factory=list)
    words_stolen: list[WordCard] = field(default_factory=list)

    def total_score(self) -> int:
        return self.score


@dataclass
class GameRecord:
    """Per-game record for analytics."""
    winner_seat: int
    winner_agent: str
    turns: int
    end_reason: str          # "victory" | "deck_exhausted" | "turn_limit"
    final_scores: list[int]
    final_agent_names: list[str]
    seat_winners: list[bool]   # winner flag by seat
    completed_word_cards: list[str]   # transliterations
    stolen_word_cards: list[str]
    opening_hands: list[list[str]]    # sign codes per player at game start
    opening_words: list[str]          # word card transliteration per player
    logograms_played: int
    steals_executed: int
    trash_actions: int = 0
    logogram_exchanges: int = 0
    first_scorer_seat: int = -1   # seat that scored the FIRST word of the game
    first_scorer_won: bool = False
    mulligans_used: int = 0       # total word mulligans across all players
    bonus_points: int = 0         # v8.11 optional-rule bonus points awarded
    seed: int = 0


# =============================================================================
# Deck loading
# =============================================================================


def load_deck() -> tuple[list[SignCard], list[WordCard], list[LogogramCard]]:
    with open(DECK_PATH) as f:
        deck = json.load(f)

    sign_pool: list[SignCard] = []
    for c in deck["sign_deck"]:
        for _ in range(c["copies"]):
            sign_pool.append(SignCard(
                code=c["sign_code"], cls=c["phonetic_class"],
                mnemonic=c["mnemonic"],
            ))

    word_pool: list[WordCard] = [
        WordCard(
            translit=c["transliteration"],
            english=c["english_glosses"],
            sign_count=c["shortest_sign_count"],
            points=c["point_value"],
            valid_spellings=c["valid_spellings"],
            pos=c.get("primary_pos"),
            determinatives=c.get("appropriate_determinatives") or [],
            honorific=c.get("honorific_transposition", False),
        ) for c in deck["word_deck"]
    ]

    logogram_pool: list[LogogramCard] = [
        LogogramCard(
            sign_code=c["sign_code"],
            target_word=c["word_transliteration"],
            description=c.get("description", ""),
        ) for c in deck["logogram_deck"]
    ]

    return sign_pool, word_pool, logogram_pool


_DET_SUPPLY_CACHE: dict = {}


def load_determinative_supply() -> dict:
    """{sign_code: copies} for the deck's determinative side pool (v8.11
    optional rule). Cached per deck path."""
    key = str(DECK_PATH)
    if key not in _DET_SUPPLY_CACHE:
        with open(DECK_PATH) as f:
            deck = json.load(f)
        _DET_SUPPLY_CACHE[key] = {
            c["sign_code"]: c.get("copies", 1)
            for c in deck.get("determinative_deck", [])
        }
    return dict(_DET_SUPPLY_CACHE[key])


# =============================================================================
# Rules helpers
# =============================================================================


# NOTE: Completion is a multiset check: do you have the signs for any
# spelling in your hand? Order does not matter. Since the v8.7 rules sync
# this IS the printed rule in rules.md (it began as a simulation-only
# relaxation in v2 — with strict-order rules, even moderately complex
# words were near-impossible to complete in reasonable game length, and
# every published balance number was produced under multiset matching).


def shortest_completable_spelling(spellings: list[list[str]],
                                   available_signs: Counter) -> Optional[list[str]]:
    """
    Return the shortest spelling that the player has all signs for (multiset),
    or None if no spelling is fully in hand.
    """
    candidates = []
    for sp in spellings:
        need = Counter(sp)
        if all(available_signs[s] >= need[s] for s in need):
            candidates.append(sp)
    if not candidates:
        return None
    return min(candidates, key=len)


def shortest_completable_with_wildcards(
        spellings: list[list[str]],
        available_signs: Counter,
        n_wildcards: int) -> Optional[tuple[list[str], int]]:
    """
    v8.1 helper for logograms-as-wildcards. Return (spelling, wildcards_needed)
    for the shortest spelling completable with up to n_wildcards substitutions.
    Returns None if no spelling is completable even with wildcards.
    """
    best = None
    for sp in spellings:
        need = Counter(sp)
        shortfall = 0
        for code, count in need.items():
            have = available_signs[code]
            if have < count:
                shortfall += count - have
        if shortfall <= n_wildcards:
            if best is None or len(sp) < len(best[0]) or (
                    len(sp) == len(best[0]) and shortfall < best[1]):
                best = (sp, shortfall)
    return best


# =============================================================================
# AI agents
# =============================================================================


class Agent:
    name = "base"

    def __init__(self, rng: random.Random):
        self.rng = rng

    def decide_turn(self, me: Player, opponents: list[Player],
                    logogram_play_target: Optional[Player] = None,
                    cfg: Optional["GameConfig"] = None,
                    peek: Optional[list] = None) -> dict:
        """
        Return a decision dict. v2 actions:
          "complete_own" / "complete_steal" — needs signs_to_play
          "play_logogram"                    — needs logogram + target_player
          "trash_and_draw"                   — needs signs_to_trash (2 cards)
          "pass"                             — no action this turn
        Optional kwargs:
          cfg          — game config (so agents can read tuning knobs)
          peek         — top N cards visible from sign deck (forward-looking)
        """
        raise NotImplementedError


def find_signs_for_spelling(hand_signs: list[SignCard],
                             spelling: list[str]) -> Optional[list[SignCard]]:
    """Pick concrete sign cards from hand that satisfy a spelling (multiset)."""
    need = Counter(spelling)
    chosen = []
    chosen_ids = set()
    for code, count in need.items():
        matched = 0
        for s in hand_signs:
            if matched >= count:
                break
            if s.code == code and id(s) not in chosen_ids:
                chosen.append(s)
                chosen_ids.add(id(s))
                matched += 1
        if matched < count:
            return None
    return chosen


def smart_discard_order(me) -> list[SignCard]:
    """
    Return hand signs sorted so the first ones are the BEST to discard.
    Useless-for-current-word goes first; uniliterals are easier to redraw
    than rare 4plus signs, so within the same usefulness bucket, prefer to
    discard uniliterals.
    """
    if not me.active_word:
        return list(me.hand_signs)
    useful_codes = set()
    for sp in me.active_word.valid_spellings:
        useful_codes.update(sp)
    # Useless first (key 0), useful last (key 1).
    # Within useless: discard plain uniliterals first (easy to redraw).
    # Within useful: never reached in normal play, but if it must happen,
    #   discard duplicates of common signs first.
    return sorted(me.hand_signs,
                  key=lambda s: (
                      0 if s.code not in useful_codes else 1,
                      {"uniliteral": 0, "biliteral": 1,
                       "triliteral": 2, "4plus": 3}.get(s.cls, 9),
                  ))


def best_missing_multiset(word, hand_signs) -> Counter:
    """Multiset of signs missing for the EASIEST spelling of `word` given
    this hand (the v9 expert draw-targeting helper — classic agents only
    ever look at valid_spellings[0])."""
    hand = Counter(s.code for s in hand_signs)
    best = None
    for sp in word.valid_spellings:
        missing = Counter(sp) - hand
        n = sum(missing.values())
        if best is None or n < best[0]:
            best = (n, missing)
    return best[1] if best else Counter()


class RandomAgent(Agent):
    """Naive: try to complete; random logogram play; rarely trashes."""
    name = "random"

    def preferred_discard_order(self, me):
        return smart_discard_order(me)

    def decide_turn(self, me, opponents, logogram_play_target=None,
                    cfg=None, peek=None):
        if me.hand_logos and self.rng.random() < 0.5:
            log = self.rng.choice(me.hand_logos)
            for p in [me] + opponents:
                if p.active_word and p.active_word.translit == log.target_word:
                    return {"action": "play_logogram", "logogram": log, "target_player": p}

        if me.active_word:
            hand_codes = Counter(s.code for s in me.hand_signs)
            sp = shortest_completable_spelling(me.active_word.valid_spellings, hand_codes)
            if sp:
                chosen = find_signs_for_spelling(me.hand_signs, sp)
                if chosen:
                    return {"action": "complete_own", "signs_to_play": chosen}

        # Random agent occasionally trashes
        if cfg and cfg.allow_trash_and_draw and me.active_word and self.rng.random() < 0.3:
            useful = set(c for sp in me.active_word.valid_spellings for c in sp)
            useless = [s for s in me.hand_signs if s.code not in useful]
            if len(useless) >= 2:
                return {"action": "trash_and_draw", "signs_to_trash": useless[:2]}
        return {"action": "pass"}


class GreedyAgent(Agent):
    """
    v2 tuned: always complete own word if possible; steal ANY opponent word
    (loosened from v1's higher-value-only); use logograms greedily; trash
    useless cards to cycle the deck when nothing else is playable.
    """
    name = "greedy"

    def preferred_discard_order(self, me):
        return smart_discard_order(me)

    def decide_turn(self, me, opponents, logogram_play_target=None,
                    cfg: Optional["GameConfig"] = None, peek: list = None):
        # 1. Logogram on self
        for log in me.hand_logos:
            if me.active_word and me.active_word.translit == log.target_word:
                return {"action": "play_logogram", "logogram": log, "target_player": me}

        # 2. Complete own word
        if me.active_word:
            hand_codes = Counter(s.code for s in me.hand_signs)
            sp = shortest_completable_spelling(me.active_word.valid_spellings, hand_codes)
            if sp:
                chosen = find_signs_for_spelling(me.hand_signs, sp)
                if chosen:
                    return {"action": "complete_own", "signs_to_play": chosen}

        # 3. Logogram steal — TUNED v2: any matching opponent word
        for log in me.hand_logos:
            for op in opponents:
                if not op.active_word:
                    continue
                if op.active_word.translit != log.target_word:
                    continue
                # v2: removed the "must be worth more than mine" gate
                return {"action": "play_logogram", "logogram": log, "target_player": op}

        # 4. Steal opponent's word with signs in hand — TUNED v2: any value
        for op in opponents:
            if not op.active_word:
                continue
            # v2: removed the "only if higher value" gate
            hand_codes = Counter(s.code for s in me.hand_signs)
            sp = shortest_completable_spelling(op.active_word.valid_spellings, hand_codes)
            if sp:
                chosen = find_signs_for_spelling(me.hand_signs, sp)
                if chosen:
                    return {"action": "complete_steal", "signs_to_play": chosen,
                            "target_player": op}

        # 4b. v8.8 test lever: exchange a dead logogram (its target word is
        # nobody's active word) for 2 sign draws.
        if cfg and getattr(cfg, "dead_logogram_exchange", False) and me.hand_logos:
            active = {pl.active_word.translit
                      for pl in [me] + list(opponents) if pl.active_word}
            dead = [lg for lg in me.hand_logos if lg.target_word not in active]
            if dead:
                return {"action": "exchange_logogram", "logogram": dead[0]}

        # 5. NEW v2: Trash 2 useless cards to draw 2 fresh (cycle the deck)
        if cfg and cfg.allow_trash_and_draw and me.active_word:
            useful = set(c for sp in me.active_word.valid_spellings for c in sp)
            useless = [s for s in me.hand_signs if s.code not in useful]
            if len(useless) >= 2:
                return {"action": "trash_and_draw", "signs_to_trash": useless[:2]}

        return {"action": "pass"}


class BalancedAgent(GreedyAgent):
    """
    v3 tuned: Greedy + actively uses look-and-take.
    If a useful card is visible in the top-N peek, ACT on it (look-and-take,
    swap a useless hand card for it) rather than passing. This removes the
    v2 over-planning trap.
    """
    name = "balanced"

    def preferred_discard_order(self, me) -> list[SignCard]:
        return smart_discard_order(me)

    def decide_turn(self, me, opponents, logogram_play_target=None,
                    cfg=None, peek=None):
        # 1. Greedy chain first (complete own, logogram, steal)
        d = GreedyAgent.decide_turn(self, me, opponents, logogram_play_target,
                                     cfg=cfg, peek=peek)
        if d["action"] not in ("trash_and_draw", "pass"):
            return d

        # 1b. v8.1: logogram-as-wildcard completion. Try to complete the
        # active word by substituting up to N logograms (any unused logograms
        # in hand) for missing signs. Pick the fewest-wildcards solution.
        if (cfg and cfg.logograms_as_wildcards
                and me.active_word and me.hand_logos):
            # An unused logogram = one whose target is NOT the active word
            # (otherwise greedy already would have played it for instant win).
            available_wildcards = [
                lg for lg in me.hand_logos
                if lg.target_word != me.active_word.translit
            ]
            if available_wildcards:
                hand_codes = Counter(s.code for s in me.hand_signs)
                # v8.1: cap at 1 wildcard per completion to prevent
                # logogram-stacking dominance. Encourages "I have 4 of 5
                # signs and just need one more" recovery rather than
                # wholesale wildcard spelling of whole words.
                result = shortest_completable_with_wildcards(
                    me.active_word.valid_spellings,
                    hand_codes,
                    n_wildcards=1)
                if result is not None and result[1] > 0:
                    spelling, n_wild = result
                    # v8.2 (Option A): skip wildcard if it would not yield a
                    # net positive score (e.g. burning a wildcard on a 1-pt
                    # tier-1 word for 0 net points is strictly worse than
                    # waiting one more turn).
                    cost = n_wild * (cfg.wildcard_point_cost if cfg else 0)
                    if me.active_word.points - cost < 1:
                        result = None
                if result is not None and result[1] > 0:
                    spelling, n_wild = result
                    # Build the actual sign list: take what we have, mark
                    # the rest as wildcard slots.
                    needed = Counter(spelling)
                    chosen_signs = []
                    consumed_ids = set()
                    for code, count in needed.items():
                        matched = 0
                        target_avail = min(count, hand_codes[code])
                        for s in me.hand_signs:
                            if matched >= target_avail:
                                break
                            if s.code == code and id(s) not in consumed_ids:
                                chosen_signs.append(s)
                                consumed_ids.add(id(s))
                                matched += 1
                    chosen_wildcards = available_wildcards[:n_wild]
                    return {
                        "action": "complete_own",
                        "signs_to_play": chosen_signs,
                        "wildcards_to_play": chosen_wildcards,
                    }

        # 2. v3: look_and_take if a useful card is in the peek and we have
        # a useless card to discard
        if cfg and cfg.allow_look_and_take and peek and me.active_word:
            useful_codes = set(c for sp in me.active_word.valid_spellings for c in sp)
            useful_peeks = [pk for pk in peek
                            if (isinstance(pk, SignCard) and pk.code in useful_codes)
                            or isinstance(pk, LogogramCard)]
            if useful_peeks:
                useless_hand = [s for s in me.hand_signs if s.code not in useful_codes]
                if useless_hand:
                    return {
                        "action": "look_and_take",
                        "take_card": useful_peeks[0],
                        "discard_card": useless_hand[0],
                    }
        # 3. Fall through to greedy's trash_and_draw or pass
        return d


class ExpertAgent(GreedyAgent):
    """
    v9: the stronger third tier. Three upgrades over greedy/balanced:

    1. VALUE-MAXIMIZING COMPLETIONS: instead of always completing its own
       word first, it enumerates every completion available this turn
       (own word, every steal, every logogram play) and takes the highest
       point value; its own word gets a +0.5 tempo bonus (completing your
       own word also rotates you onto a fresh, hand-fitted word).
    2. BEST-SPELLING DRAW TARGETING (`smart_draw`): the engine scores
       draw options against the missing signs of the EASIEST spelling of
       its active word, not spelling[0].
    3. DENIAL-AWARE DISCARDS: at 3+ players the top of the discard pile
       is takeable, so among cards it doesn't need, it discards the ones
       the NEXT player's visible active word can't use first.
    """
    name = "expert"
    smart_draw = True

    def preferred_discard_order(self, me, next_word=None):
        base = smart_discard_order(me)
        if next_word is None or not next_word.valid_spellings:
            return base
        opp_useful = set()
        for sp in next_word.valid_spellings:
            opp_useful.update(sp)
        # Stable re-sort: keep my own usefulness ordering, but within it
        # discard cards USELESS to the next player first.
        return sorted(base, key=lambda s: s.code in opp_useful)

    def decide_turn(self, me, opponents, logogram_play_target=None,
                    cfg=None, peek=None):
        options = []   # (value, tiebreak, decision)
        hand_codes = Counter(s.code for s in me.hand_signs)
        # Logogram plays (own word gets the tempo bonus)
        for log in me.hand_logos:
            for pl in [me] + list(opponents):
                if pl.active_word and pl.active_word.translit == log.target_word:
                    bonus = 0.5 if pl is me else 0.0
                    options.append((pl.active_word.points + bonus, len(options),
                                    {"action": "play_logogram", "logogram": log,
                                     "target_player": pl}))
        # Sign completions: own word and steals, by value
        for pl in [me] + list(opponents):
            if not pl.active_word:
                continue
            sp = shortest_completable_spelling(pl.active_word.valid_spellings,
                                               hand_codes)
            if not sp:
                continue
            chosen = find_signs_for_spelling(me.hand_signs, sp)
            if not chosen:
                continue
            bonus = 0.5 if pl is me else 0.0
            act = "complete_own" if pl is me else "complete_steal"
            d = {"action": act, "signs_to_play": chosen}
            if pl is not me:
                d["target_player"] = pl
            options.append((pl.active_word.points + bonus, len(options), d))
        if options:
            options.sort(key=lambda o: (-o[0], o[1]))
            return options[0][2]
        # Fall through to greedy's tail (dead-logogram exchange lever,
        # trash-and-draw, pass) without re-running its completion logic.
        if cfg and getattr(cfg, "dead_logogram_exchange", False) and me.hand_logos:
            active = {pl.active_word.translit
                      for pl in [me] + list(opponents) if pl.active_word}
            dead = [lg for lg in me.hand_logos if lg.target_word not in active]
            if dead:
                return {"action": "exchange_logogram", "logogram": dead[0]}
        if cfg and cfg.allow_trash_and_draw and me.active_word:
            # Expert recycles what its EASIEST spelling can't use.
            needed = best_missing_multiset(me.active_word, me.hand_signs)
            useful = set(needed)
            for sp in me.active_word.valid_spellings:
                useful.update(sp)
            useless = [s for s in me.hand_signs if s.code not in useful]
            if len(useless) >= 2:
                return {"action": "trash_and_draw", "signs_to_trash": useless[:2]}
        return {"action": "pass"}


AGENTS = {"random": RandomAgent, "greedy": GreedyAgent,
          "balanced": BalancedAgent, "expert": ExpertAgent}


# =============================================================================
# Game engine
# =============================================================================


@dataclass
class GameConfig:
    n_players: int = 2
    starting_hand: int = 8
    hand_limit: int = 12
    points_to_win: int = 7         # v7: lowered from 10 to shorten games
    max_turns: int = 1000
    draw_n: int = 2                # v8: draw 2, keep 1 (the most useful);
                                    # discard the other to sign_discard.
                                    # Cuts ~15% more turn count vs draw_n=1.
    logograms_as_wildcards: bool = False  # v8.1 lever: an unused logogram in
                                    # hand can substitute for ONE missing sign
                                    # when completing a word. Addresses the
                                    # "I have 4 of 5 signs and can't find the
                                    # last one" stall.
    wildcard_point_cost: int = 1   # v8.2 (Option A): each wildcard used in a
                                    # completion deducts this many points from
                                    # the word's score. 0 = free (was v8.1).
    market_size: int = 5           # v8.3 adopted: face-up sign market
                                    # (Splendor style). 5 cards kept visible
                                    # alongside the sign deck. Each turn the
                                    # agent chooses: take a face-up card from
                                    # the market (or top of discard if
                                    # discard_take_enabled), OR draw_n blind
                                    # from the deck and keep the best. Market
                                    # refills from the deck after each take.
    discard_take_enabled: bool = True
                                    # v8.4 adopted: top of sign_discard is
                                    # face-up and may be taken instead of a
                                    # market card or blind draw. Gated by
                                    # `discard_take_min_players` below — at
                                    # 2-player the discard pile is dominated
                                    # by the one opponent's throwaways, which
                                    # made games too lopsided (balance 87+).
                                    # Default 3+ keeps the lever active where
                                    # it's interesting and safe.
    discard_take_min_players: int = 3
                                    # Discard-take only triggers when
                                    # n_players >= this value.
    actions_per_turn: int = 1      # v8.5 lever: number of productive
                                    # actions a player may take per turn
                                    # after the auto-draw. Default 1 (1
                                    # decision per turn). Set to 2 to test
                                    # "draw + 2 actions" pattern. The loop
                                    # breaks early when the agent passes.
    word_draw_n: int = 2           # v8.8 ADOPTED: when drawing a new word
                                    # card (setup and after completions), draw
                                    # N and keep the best fit for the current
                                    # hand; the rest go to the bottom of the
                                    # word deck. Balance-neutral but nearly
                                    # doubles steals and boosts logogram
                                    # completions ~60% (see
                                    # VARIANT_PLAYTEST_REPORT.md). Set to 1
                                    # for pre-v8.8 comparison runs.
    dead_logogram_exchange: int = 0
                                    # v8.8 tested and REJECTED: a dead
                                    # logogram exchanged for N sign draws.
                                    # Agents cashed in ~30 logograms/game and
                                    # logogram completions fell ~40% in both
                                    # the 1-draw and 2-draw forms. Kept as a
                                    # lever (0 = off) for future bounded
                                    # variants (e.g. once per player/game).
    # ----- 2p catch-up candidates (v8.9 test levers, all default OFF) -----
    score_rebound_draw: int = 0    # v8.9 tested, NOT adopted (no measurable
                                    # effect on first-scorer-wins): when a
                                    # player scores a word, each opponent
                                    # immediately draws N sign cards.
    steal_victim_draws: int = 0    # v8.9 tested, NOT adopted (no measurable
                                    # effect): when your word is stolen,
                                    # draw N signs.
    word_mulligan: int = 1         # v8.9 ADOPTED: once per player per game,
                                    # as a FREE action, replace your active
                                    # word (old word to the bottom of the
                                    # reserve, draw a fresh word with the
                                    # usual draw-2-keep-1). Tracked at the
                                    # table by flipping a two-sided player
                                    # marker (a coin). Agents use it when >=3
                                    # signs of their easiest spelling are
                                    # missing. Cut 2p first-scorer-wins from
                                    # 60.1% to 53.5% with skill expression
                                    # intact (CATCHUP_PLAYTEST_REPORT.md).
                                    # Set 0 for pre-v8.9 comparison runs.
    determinative_bonus: bool = False
                                    # v8.11 OPTIONAL RULE: on completing a
                                    # word, claim one matching determinative
                                    # card from the shared side pool for +1
                                    # point (supply-limited; the deck ships a
                                    # determinative_deck). Off by default —
                                    # it's an optional advanced rule.
    honorific_bonus: bool = False  # v8.11 OPTIONAL RULE: +1 when completing
                                    # a word flagged honorific_transposition
                                    # (models players who always notice).
    coop_mode: bool = False        # v9 CANDIDATE (co-op/solo): all players
                                    # are one team. Victory = TEAM total
                                    # reaches points_to_win before the sign
                                    # deck is exhausted (see passes below).
                                    # Completing a teammate's word is an
                                    # assist (same engine path as a steal;
                                    # the team scores either way). Works at
                                    # n_players=1 for solo play.
    coop_sign_deck_passes: int = 2 # co-op loss clock: the sign deck may be
                                    # dealt through this many times total
                                    # (2 = one reshuffle of the discard).
                                    # When it empties past that, the game
                                    # ends and the team wins only if the
                                    # target was already reached.
    shared_word_pool: int = 0      # v9 CANDIDATE ("race, not theft"): if >0,
                                    # players have NO personal active words.
                                    # Instead N word cards sit face-up in a
                                    # shared center row; on your turn you may
                                    # complete ANY of them from hand (or play
                                    # a logogram targeting one). The row
                                    # refills from the word deck after each
                                    # completion. Steals and the word
                                    # mulligan don't exist in this mode.
                                    # 0 = classic personal-word game.
    shared_dredge: bool = True     # In shared-pool mode, a player may spend
                                    # their action to "dredge" — bottom one
                                    # row word card and refill from the deck.
                                    # Default True: the PRINTED Race Mode
                                    # includes dredge (without it, 2p games
                                    # stall — see SHARED_POOL_PLAYTEST_
                                    # REPORT.md). No effect when
                                    # shared_word_pool == 0. Set False only
                                    # for the historical no-dredge runs.
    underdog_token: bool = False   # v8.9 tested, NOT adopted (runner-up:
                                    # 56.6% first-scorer-wins vs mulligan's
                                    # 53.5%): 2-player only, a token moves to
                                    # the OTHER player whenever anyone scores;
                                    # the holder's blind draw is 3-keep-1
                                    # instead of 2-keep-1 ("Eye of Horus").
    equal_turns_ending: bool = True
                                    # v8.7 adopted: when a player hits the
                                    # target score, finish the current round
                                    # so every player has had the same number
                                    # of turns. Winner = highest score at the
                                    # end of the round. Ties broken by:
                                    # most completed words, then fewest signs
                                    # remaining in hand, then earlier seat.
    # v3 mechanics:
    allow_unconditional_steal: bool = True    # Drop "only steal if higher value" gate
    allow_trash_and_draw: bool = True         # Trash 2 sign cards, draw 2.
                                               # v8.10: now a PRINTED rule
                                               # ("recycle") — it was the
                                               # game's de facto pacing engine
                                               # (fires nearly every
                                               # non-scoring turn) and the
                                               # rulebook finally says so.
    allow_look_and_take: bool = False         # v3: peek top N, take 1,
                                               # discard 1. v8.10: OFF — it
                                               # was never in the printed
                                               # rules, and the v8 market +
                                               # draw-2-keep-1 supersede it.
                                               # Set True only for historical
                                               # comparison runs.
    look_n: int = 3                           # How many cards to look at
    logograms_in_sign_pile: bool = True       # v3: shuffle logograms into sign deck
    logogram_ratio: int = 15                  # v4: 1 logogram per N signs
    logogram_refresh_every: int = 0           # 0 disables periodic refresh
    first_player_gift_signs: int = 0          # v8.7: zeroed out — the v8.6
                                                # points scaling already
                                                # equalizes seat advantage;
                                                # the gift was over-correcting
                                                # at 4p (balance 87.5 with
                                                # gift=4 vs 76.2 with gift=0).
    agent_names: list[str] = field(default_factory=lambda: ["greedy", "greedy"])


def deal_initial(rng, sign_pool, word_pool, logogram_pool, cfg) -> tuple[list[Player], list, list, list]:
    """
    v3: if `logograms_in_sign_pile`, the logogram cards are shuffled INTO
    the sign deck. They are drawn organically during play and routed to the
    player's logogram hand automatically. The separate `logo_deck` returned
    in that mode is empty (unused).
    """
    word_deck = list(word_pool)
    rng.shuffle(word_deck)

    sign_deck = list(sign_pool)
    if cfg.logograms_in_sign_pile and logogram_pool:
        # Mix logograms into sign pile at the configured ratio. Add roughly
        # len(sign_deck) // logogram_ratio logograms (so a 350-sign deck with
        # ratio 30 gets ~11 logograms shuffled in, from the 30 available).
        target_logograms = max(1, len(sign_deck) // cfg.logogram_ratio)
        log_pool = list(logogram_pool)
        rng.shuffle(log_pool)
        mixed = log_pool[:target_logograms]
        sign_deck.extend(mixed)
        logo_deck = []  # rest of logograms not used in this mode
    else:
        logo_deck = list(logogram_pool)
        rng.shuffle(logo_deck)
    rng.shuffle(sign_deck)

    players = []
    for i in range(cfg.n_players):
        agent_name = cfg.agent_names[i % len(cfg.agent_names)]
        p = Player(pid=i, agent_name=agent_name)
        # Draw starting hand — may include logograms naturally
        # v5: seat 0 gets +first_player_gift_signs extra signs as a first-move
        # compensation for the second-mover's information advantage
        target = cfg.starting_hand
        if i == 0 and cfg.first_player_gift_signs > 0:
            target += cfg.first_player_gift_signs
        drawn = 0
        while drawn < target and sign_deck:
            card = sign_deck.pop()
            if isinstance(card, LogogramCard):
                p.hand_logos.append(card)
            else:
                p.hand_signs.append(card)
                drawn += 1
        if word_deck and cfg.shared_word_pool == 0:
            p.active_word = draw_word_card(word_deck, p, cfg)
        # Pre-v3 fallback: give each player 1 logogram 30% chance
        if not cfg.logograms_in_sign_pile and logo_deck and rng.random() < 0.3:
            p.hand_logos.append(logo_deck.pop())
        players.append(p)

    return players, sign_deck, word_deck, logo_deck


def draw_word_card(word_deck: list, player: Player, cfg: GameConfig):
    """
    v8.8 test lever: draw cfg.word_draw_n word cards, keep the one whose
    easiest spelling has the fewest signs missing from the player's current
    hand (tiebreak: higher points). Rejected candidates go to the BOTTOM of
    the word deck. word_draw_n=1 reproduces classic pop() behavior.
    """
    if not word_deck:
        return None
    n = max(1, getattr(cfg, "word_draw_n", 1))
    if n == 1:
        return word_deck.pop()
    candidates = [word_deck.pop() for _ in range(min(n, len(word_deck)))]
    hand = Counter(s.code for s in player.hand_signs)
    def missing(w) -> int:
        best = None
        for sp in w.valid_spellings:
            need = Counter(sp)
            miss = sum(max(0, c - hand[code]) for code, c in need.items())
            if best is None or miss < best:
                best = miss
        return 99 if best is None else best
    candidates.sort(key=lambda w: (missing(w), -w.points))
    keep = candidates[0]
    for w in candidates[1:]:
        word_deck.insert(0, w)
    return keep


def shared_pool_decision(p: Player, word_market: list, cfg: GameConfig,
                         rng: random.Random, agent_name: str) -> dict:
    """
    v9 shared-word-pool mode: the agent policy replaces the classic
    decide_turn (personal words / steals don't exist here).
    Priority: logogram on a row word > complete the best row word >
    trash useless signs > pass. The random agent completes a random
    completable word most of the time and never trashes.
    """
    hand_codes = Counter(s.code for s in p.hand_signs)
    # 1. Logogram targeting a row word (highest points first)
    best_log = None
    for log in p.hand_logos:
        for w in word_market:
            if w.translit == log.target_word:
                if best_log is None or w.points > best_log[1].points:
                    best_log = (log, w)
    if best_log and (agent_name != "random" or rng.random() < 0.5):
        return {"action": "logogram_shared",
                "logogram": best_log[0], "word": best_log[1]}
    # 2. Complete a row word from hand
    completable = []
    for w in word_market:
        sp = shortest_completable_spelling(w.valid_spellings, hand_codes)
        if sp:
            completable.append((w, sp))
    if completable:
        if agent_name == "random":
            if rng.random() < 0.7:
                w, sp = rng.choice(completable)
                chosen = find_signs_for_spelling(p.hand_signs, sp)
                if chosen:
                    return {"action": "complete_shared", "word": w,
                            "signs_to_play": chosen}
        else:
            w, sp = max(completable, key=lambda x: (x[0].points, -len(x[1])))
            chosen = find_signs_for_spelling(p.hand_signs, sp)
            if chosen:
                return {"action": "complete_shared", "word": w,
                        "signs_to_play": chosen}
    # 2b. Dredge: if nothing in the row is close to completable, spend the
    # action cycling the row — bottom the word furthest from this hand.
    if (agent_name != "random" and cfg.shared_dredge and word_market):
        def missing_for(w):
            best = None
            for sp in w.valid_spellings:
                miss = sum((Counter(sp) - hand_codes).values())
                if best is None or miss < best:
                    best = miss
            return best if best is not None else 99
        misses = {id(w): missing_for(w) for w in word_market}
        if min(misses.values()) >= 3:
            worst = max(word_market, key=lambda w: misses[id(w)])
            return {"action": "dredge_shared", "word": worst}

    # 3. Trash signs useless for EVERY row word (competent agents only)
    if agent_name != "random" and cfg.allow_trash_and_draw and word_market:
        useful = set()
        for w in word_market:
            for sp in w.valid_spellings:
                useful.update(sp)
        useless = [s for s in p.hand_signs if s.code not in useful]
        if len(useless) >= 2:
            return {"action": "trash_and_draw", "signs_to_trash": useless[:2]}
    return {"action": "pass"}


def simulate_game(seed: int, sign_pool, word_pool, logogram_pool, cfg: GameConfig) -> GameRecord:
    rng = random.Random(seed)
    players, sign_deck, word_deck, logo_deck = deal_initial(
        rng, sign_pool, word_pool, logogram_pool, cfg)

    # Build agents
    agents = [AGENTS[p.agent_name](random.Random(rng.random())) for p in players]

    # Capture opening hands and words for analytics
    opening_hands = [[s.code for s in p.hand_signs] for p in players]
    opening_words = [p.active_word.translit if p.active_word else "" for p in players]

    sign_discard: list[SignCard] = []
    completed_words: list[str] = []
    stolen_words: list[str] = []
    logograms_played = 0
    steals_executed = 0
    trash_actions = 0
    logogram_exchanges = 0
    first_scorer_seat = -1        # v8.9 metric: seat of the game's first score
    mulligans_total = 0           # v8.9 lever metric
    token_holder = None           # v8.9 lever: underdog token (2p)
    end_reason = "turn_limit"
    winner = -1
    endgame_triggered = False     # v8.7: equal-turns endgame flag

    deck_passes_used = 1   # the initial deal is pass #1 (co-op loss clock)

    def maybe_recycle_deck():
        nonlocal sign_deck, deck_passes_used
        if not sign_deck and sign_discard:
            # Co-op: the deck may only be dealt through a limited number of
            # times; past that, no reshuffle — the sands have run out.
            if cfg.coop_mode and deck_passes_used >= cfg.coop_sign_deck_passes:
                return
            sign_deck = list(sign_discard)
            rng.shuffle(sign_deck)
            sign_discard.clear()
            deck_passes_used += 1

    # v8.3: face-up sign market. Populated once now from the deck.
    market: list = []
    def refill_market():
        while len(market) < cfg.market_size and (sign_deck or sign_discard):
            maybe_recycle_deck()
            if not sign_deck:
                break
            market.append(sign_deck.pop())
    if cfg.market_size > 0:
        refill_market()

    # v9 candidate: shared word pool ("race, not theft"). A face-up row of
    # N word cards anyone may complete; refills after each completion.
    word_market: list = []
    def refill_word_market():
        while (cfg.shared_word_pool > 0
               and len(word_market) < cfg.shared_word_pool and word_deck):
            word_market.append(word_deck.pop())
    refill_word_market()

    def row_needed(pl) -> Counter:
        """Missing-sign multiset for the row word this player is CLOSEST to
        completing (used to score draw usefulness in shared mode)."""
        hand = Counter(s.code for s in pl.hand_signs)
        best = None
        for w in word_market:
            for sp in w.valid_spellings:
                missing = Counter(sp) - hand
                miss_n = sum(missing.values())
                if best is None or miss_n < best[0]:
                    best = (miss_n, missing)
        return best[1] if best else Counter()

    def draw_signs(pl, n):
        """Draw n cards from the sign deck into pl's hand (logogram-aware)."""
        for _ in range(n):
            maybe_recycle_deck()
            if not sign_deck:
                break
            c = sign_deck.pop()
            if isinstance(c, LogogramCard):
                pl.hand_logos.append(c)
            else:
                pl.hand_signs.append(c)

    # v8.11 optional advanced rules (both default off)
    det_supply = (load_determinative_supply()
                  if cfg.determinative_bonus else None)
    bonus_points_total = 0

    def optional_bonuses(word) -> int:
        """+1 for claiming a matching determinative from the shared pool
        (supply-limited), +1 for an honorific word. Models players who
        always take the bonus — the upper bound."""
        nonlocal bonus_points_total
        pts = 0
        if det_supply is not None and word.determinatives:
            for dsign in word.determinatives:
                if det_supply.get(dsign, 0) > 0:
                    det_supply[dsign] -= 1
                    pts += 1
                    break
        if cfg.honorific_bonus and word.honorific:
            pts += 1
        bonus_points_total += pts
        return pts

    def on_score(scorer_idx, victim=None):
        """v8.9 catch-up hooks, fired every time a word is scored."""
        nonlocal first_scorer_seat, token_holder
        if first_scorer_seat < 0:
            first_scorer_seat = scorer_idx
        if cfg.underdog_token and cfg.n_players == 2:
            token_holder = 1 - scorer_idx
        if cfg.score_rebound_draw > 0:
            for j, pp in enumerate(players):
                if j != scorer_idx:
                    draw_signs(pp, cfg.score_rebound_draw)
        if victim is not None and cfg.steal_victim_draws > 0:
            draw_signs(victim, cfg.steal_victim_draws)

    turn = 0
    dry_turns = 0   # co-op: consecutive turns with the sign deck dead
    while turn < cfg.max_turns:
        for i, p in enumerate(players):
            turn += 1
            if turn > cfg.max_turns:
                break

            # Co-op loss clock: once the deck is dead (empty, no reshuffles
            # left), everyone gets ONE last dry turn to flush completions
            # from hand, then the game ends.
            if cfg.coop_mode:
                if (not sign_deck
                        and deck_passes_used >= cfg.coop_sign_deck_passes):
                    dry_turns += 1
                    if dry_turns > cfg.n_players:
                        end_reason = "deck_exhausted"
                        winner = max(range(len(players)),
                                     key=lambda j: players[j].score)
                        break
                else:
                    dry_turns = 0

            # 0. v2 fallback: periodic logogram refresh (off in v3 mode)
            if cfg.logogram_refresh_every > 0 and turn % cfg.logogram_refresh_every == 0:
                for pp in players:
                    if not pp.hand_logos and logo_deck:
                        pp.hand_logos.append(logo_deck.pop())

            # 1. Draw — v3 may pull a logogram from the mixed pile
            #    v7.1: optional draw_n>1 means look at N, keep the most useful,
            #    discard the rest to sign_discard.
            #    v8.3: optional face-up market. If a useful card is visible,
            #    the agent takes that single card instead of doing the blind
            #    draw_n pull. Market refills from the deck after the take.
            maybe_recycle_deck()
            took_face_up = False
            # v8.3 / v8.4: assemble the set of face-up cards the agent may
            # take from: the market (5 cards) plus, if enabled, the top of
            # the discard pile (1 card). Pick the most useful one.
            visible_options = []   # list of ("market", idx, card) or ("discard", None, card)
            if cfg.market_size > 0:
                for idx, card in enumerate(market):
                    visible_options.append(("market", idx, card))
            if (cfg.discard_take_enabled
                    and cfg.n_players >= cfg.discard_take_min_players
                    and sign_discard):
                visible_options.append(("discard", None, sign_discard[-1]))

            if visible_options:
                # Score each option by usefulness to this player.
                needed_now = Counter()
                if cfg.shared_word_pool > 0:
                    needed_now = row_needed(p)
                elif (getattr(agents[i], "smart_draw", False)
                      and p.active_word and p.active_word.valid_spellings):
                    # v9 expert: target the EASIEST spelling, not spelling[0]
                    needed_now = best_missing_multiset(p.active_word,
                                                       p.hand_signs)
                elif p.active_word and p.active_word.valid_spellings:
                    spelling = p.active_word.valid_spellings[0]
                    hand_have = Counter(s.code for s in p.hand_signs)
                    for code in spelling:
                        if hand_have[code] > 0:
                            hand_have[code] -= 1
                        else:
                            needed_now[code] += 1
                active_translit = (p.active_word.translit if p.active_word
                                   else None)
                row_translits = ({w.translit for w in word_market}
                                 if cfg.shared_word_pool > 0 else None)
                def visible_score(card):
                    if isinstance(card, LogogramCard):
                        if row_translits is not None:
                            return 100 if card.target_word in row_translits else 30
                        return 100 if card.target_word == active_translit else 30
                    if needed_now.get(card.code, 0) > 0:
                        return 50
                    return 0   # only take a face-up if it's genuinely useful
                best = max(visible_options, key=lambda o: visible_score(o[2]))
                source, idx, card = best
                if visible_score(card) > 0:
                    if source == "market":
                        market.pop(idx)
                        if isinstance(card, LogogramCard):
                            p.hand_logos.append(card)
                        else:
                            p.hand_signs.append(card)
                        refill_market()
                    else:  # discard
                        sign_discard.pop()
                        if isinstance(card, LogogramCard):
                            p.hand_logos.append(card)
                        else:
                            p.hand_signs.append(card)
                    took_face_up = True

            took_from_market = took_face_up   # back-compat name

            drawn_options = []
            if not took_from_market:
                eff_draw_n = max(1, cfg.draw_n)
                # v8.9 lever: underdog token holder blind-draws one extra
                # (draw 3, keep 1, at the default draw_n=2).
                if (cfg.underdog_token and cfg.n_players == 2
                        and token_holder == i):
                    eff_draw_n += 1
                for _ in range(eff_draw_n):
                    if not sign_deck:
                        break
                    drawn_options.append(sign_deck.pop())
            if drawn_options:
                if len(drawn_options) == 1:
                    keep = drawn_options[0]
                else:
                    # Score each option for usefulness to this player; keep best.
                    # Compute the multiset of signs still needed for active word.
                    needed_multiset = Counter()
                    if cfg.shared_word_pool > 0:
                        needed_multiset = row_needed(p)
                    elif (getattr(agents[i], "smart_draw", False)
                          and p.active_word and p.active_word.valid_spellings):
                        needed_multiset = best_missing_multiset(p.active_word,
                                                                p.hand_signs)
                    elif p.active_word and p.active_word.valid_spellings:
                        spelling = p.active_word.valid_spellings[0]
                        hand_have = Counter(s.code for s in p.hand_signs)
                        for code in spelling:
                            if hand_have[code] > 0:
                                hand_have[code] -= 1
                            else:
                                needed_multiset[code] += 1
                    active_translit = (p.active_word.translit if p.active_word
                                       else None)
                    row_tr = ({w.translit for w in word_market}
                              if cfg.shared_word_pool > 0 else None)
                    def score(card):
                        if isinstance(card, LogogramCard):
                            if row_tr is not None:
                                return 100 if card.target_word in row_tr else 30
                            if card.target_word == active_translit:
                                return 100
                            return 30
                        if needed_multiset.get(card.code, 0) > 0:
                            return 50
                        if card.cls == "uniliteral":
                            return 5
                        return 1
                    drawn_options.sort(key=score, reverse=True)
                    keep = drawn_options[0]
                    for discarded in drawn_options[1:]:
                        # rules.md: the rejected card of the blind draw-2 goes
                        # to the discard pile face-up — logograms included
                        # (they recirculate on reshuffle, and at 3p+ the top
                        # of the discard is takeable).
                        sign_discard.append(discarded)
                if isinstance(keep, LogogramCard):
                    p.hand_logos.append(keep)
                else:
                    p.hand_signs.append(keep)

            # 1c. v8.9 lever: word mulligan — replace a stuck active word as
            # a FREE action (limited uses per game). "Stuck" for the agent:
            # even the easiest spelling is missing 3+ signs from hand.
            if (cfg.word_mulligan > 0 and cfg.shared_word_pool == 0
                    and p.active_word
                    and p.active_word.valid_spellings and word_deck
                    and getattr(p, "_mulligans_used", 0) < cfg.word_mulligan):
                hand_now = Counter(s.code for s in p.hand_signs)
                best_missing = min(
                    sum(max(0, c - hand_now[code])
                        for code, c in Counter(sp).items())
                    for sp in p.active_word.valid_spellings)
                if best_missing >= 3:
                    word_deck.insert(0, p.active_word)
                    p.active_word = draw_word_card(word_deck, p, cfg)
                    p._mulligans_used = getattr(p, "_mulligans_used", 0) + 1
                    mulligans_total += 1

            # 2-3. Decision + resolve loop. v8.5: actions_per_turn lets the
            # player chain up to N actions per turn (e.g. complete own word,
            # then play a logogram on the next word). Break early on pass or
            # on victory.
            for _action_idx in range(max(1, cfg.actions_per_turn)):
                opponents = [pp for j, pp in enumerate(players) if j != i]
                maybe_recycle_deck()
                peek = list(sign_deck[-cfg.look_n:]) if cfg.look_n and sign_deck else []
                if cfg.shared_word_pool > 0:
                    decision = shared_pool_decision(
                        p, word_market, cfg, agents[i].rng, p.agent_name)
                else:
                    decision = agents[i].decide_turn(p, opponents, cfg=cfg, peek=peek)

                # 3. Resolve decision
                act = decision["action"]

                if act == "pass":
                    break

                if act == "play_logogram":
                    log = decision["logogram"]
                    target = decision["target_player"]
                    if target.active_word and target.active_word.translit == log.target_word:
                        if target is p:
                            p.score += target.active_word.points
                            p.words_completed.append(target.active_word)
                            completed_words.append(target.active_word.translit)
                        else:
                            p.score += target.active_word.points
                            p.words_stolen.append(target.active_word)
                            stolen_words.append(target.active_word.translit)
                            completed_words.append(target.active_word.translit)
                            steals_executed += 1
                        p.score += optional_bonuses(target.active_word)
                        on_score(i, victim=target if target is not p else None)
                        target.active_word = draw_word_card(word_deck, target, cfg)
                        p.hand_logos.remove(log)
                        # rules.md: "After use, the logogram card goes to the
                        # discard pile" — it re-enters circulation on reshuffle.
                        sign_discard.append(log)
                        logograms_played += 1

                elif act == "complete_shared":
                    # v9 shared pool: complete a center-row word from hand.
                    w = decision["word"]
                    if w in word_market:
                        signs = decision["signs_to_play"]
                        for s in signs:
                            p.hand_signs.remove(s)
                        sign_discard.extend(signs)
                        p.score += w.points + optional_bonuses(w)
                        p.words_completed.append(w)
                        completed_words.append(w.translit)
                        word_market.remove(w)
                        on_score(i)
                        refill_word_market()

                elif act == "logogram_shared":
                    # v9 shared pool: logogram instantly completes a row word.
                    log = decision["logogram"]
                    w = decision["word"]
                    if w in word_market and log in p.hand_logos:
                        p.hand_logos.remove(log)
                        sign_discard.append(log)   # per rules: used logograms
                                                   # go to the discard pile
                        p.score += w.points + optional_bonuses(w)
                        p.words_completed.append(w)
                        completed_words.append(w.translit)
                        logograms_played += 1
                        word_market.remove(w)
                        on_score(i)
                        refill_word_market()

                elif act == "dredge_shared":
                    # v9 shared pool addon: bottom a row word, refill from top.
                    w = decision["word"]
                    if w in word_market and word_deck:
                        word_market.remove(w)
                        word_deck.insert(0, w)
                        refill_word_market()

                elif act == "exchange_logogram":
                    # v8.8 test lever: swap a dead logogram for N sign draws.
                    # The logogram goes to the sign discard pile face-up
                    # (recycled with the rest of the discard when the deck
                    # runs out), exactly as a physical table would play it.
                    log = decision["logogram"]
                    if log in p.hand_logos:
                        p.hand_logos.remove(log)
                        sign_discard.append(log)
                        for _ in range(max(1, cfg.dead_logogram_exchange)):
                            maybe_recycle_deck()
                            if sign_deck:
                                nc = sign_deck.pop()
                                if isinstance(nc, LogogramCard):
                                    p.hand_logos.append(nc)
                                else:
                                    p.hand_signs.append(nc)
                        logogram_exchanges += 1

                elif act == "trash_and_draw":
                    signs_to_trash = decision["signs_to_trash"]
                    for s in signs_to_trash:
                        if s in p.hand_signs:
                            p.hand_signs.remove(s)
                            sign_discard.append(s)
                    for _ in range(len(signs_to_trash)):
                        maybe_recycle_deck()
                        if sign_deck:
                            nc = sign_deck.pop()
                            if isinstance(nc, LogogramCard):
                                p.hand_logos.append(nc)
                            else:
                                p.hand_signs.append(nc)
                    trash_actions += 1

                elif act == "look_and_take":
                    # v3: peek the top N of the deck, take the most useful one,
                    # discard one useless card from hand. The other N-1 cards
                    # are put back on top of the deck in unchanged order.
                    discard_card = decision["discard_card"]
                    if discard_card in p.hand_signs:
                        p.hand_signs.remove(discard_card)
                        sign_discard.append(discard_card)
                    # Peek the top N
                    maybe_recycle_deck()
                    n_peek = min(cfg.look_n, len(sign_deck))
                    if n_peek > 0:
                        peeked = sign_deck[-n_peek:]
                        take_card = decision["take_card"]
                        if take_card in peeked:
                            sign_deck.remove(take_card)
                            if isinstance(take_card, LogogramCard):
                                p.hand_logos.append(take_card)
                            else:
                                p.hand_signs.append(take_card)

                elif act in ("complete_own", "complete_steal"):
                    signs = decision["signs_to_play"]
                    wildcards = decision.get("wildcards_to_play", [])
                    target = decision.get("target_player", p)
                    # Remove cards from hand and discard them
                    for s in signs:
                        p.hand_signs.remove(s)
                    sign_discard.extend(signs)
                    # v8.1: consume any logograms used as wildcards.
                    # v8.2 (Option A): each wildcard costs cfg.wildcard_point_cost
                    # points; the deduction is applied below when scoring.
                    for lg in wildcards:
                        p.hand_logos.remove(lg)
                        sign_discard.append(lg)
                        logograms_played += 1
                    # Score and replace word; v8.2 (Option A) deducts wildcard cost
                    wildcard_penalty = len(wildcards) * cfg.wildcard_point_cost
                    gross = target.active_word.points
                    net = max(0, gross - wildcard_penalty)
                    if target is p:
                        p.score += net
                        p.words_completed.append(target.active_word)
                    else:
                        p.score += net
                        p.words_stolen.append(target.active_word)
                        stolen_words.append(target.active_word.translit)
                        steals_executed += 1
                    completed_words.append(target.active_word.translit)
                    p.score += optional_bonuses(target.active_word)
                    on_score(i, victim=target if target is not p else None)
                    target.active_word = draw_word_card(word_deck, target, cfg)

                # v8.5: stop chaining actions if the player already won.
                # v8.7: if equal_turns_ending, just mark endgame and keep
                # cycling the action loop (player can still finish their
                # remaining actions this turn).
                # Co-op: the TEAM total is what wins, instantly (no
                # equal-turns round needed — everyone wins together).
                win_score = (sum(pl.score for pl in players)
                             if cfg.coop_mode else p.score)
                if win_score >= cfg.points_to_win:
                    if cfg.equal_turns_ending and not cfg.coop_mode:
                        endgame_triggered = True
                    break

            # 4. Discard down to hand limit (Balanced agent uses smarter
            # ordering; Expert additionally denies the next player when the
            # discard top is takeable at 3+ players).
            agent_obj = agents[i]
            next_word = None
            if (cfg.discard_take_enabled
                    and cfg.n_players >= cfg.discard_take_min_players):
                next_word = players[(i + 1) % len(players)].active_word
            while len(p.hand_signs) > cfg.hand_limit:
                if hasattr(agent_obj, "preferred_discard_order"):
                    try:
                        order = agent_obj.preferred_discard_order(
                            p, next_word=next_word)
                    except TypeError:
                        order = agent_obj.preferred_discard_order(p)
                    discard = order[0]
                else:
                    discard = p.hand_signs[0]
                p.hand_signs.remove(discard)
                sign_discard.append(discard)

            # 5. Check win
            win_score = (sum(pl.score for pl in players)
                         if cfg.coop_mode else p.score)
            if win_score >= cfg.points_to_win:
                if cfg.equal_turns_ending and not cfg.coop_mode:
                    # Let the rest of this round play out; resolve after.
                    endgame_triggered = True
                else:
                    end_reason = "victory"
                    winner = i
                    break
            if cfg.shared_word_pool > 0:
                if not word_market and not word_deck:
                    end_reason = "deck_exhausted"
                    winner = max(range(len(players)), key=lambda j: players[j].score)
                    break
            elif not p.active_word:
                # Word deck empty AND player has no card
                if not word_deck:
                    end_reason = "deck_exhausted"
                    # Highest score wins
                    winner = max(range(len(players)), key=lambda j: players[j].score)
                    break

        # v8.7: resolve the endgame at round boundary (every player has
        # had a turn this iteration). Winner = highest score, ties broken
        # by completed-word count, then fewest hand signs, then seat order.
        if winner < 0 and endgame_triggered:
            end_reason = "victory"
            winner = max(
                range(len(players)),
                key=lambda j: (
                    players[j].score,
                    len(players[j].words_completed),
                    -len(players[j].hand_signs),
                    -j,   # earlier seat wins ties
                ),
            )

        if winner >= 0:
            break

    if winner < 0:
        # Turn limit reached. Highest score wins; ties broken RANDOMLY
        # (not by seat order) so seat-0 doesn't get a free win from ties.
        max_score = max(p.score for p in players)
        tied = [j for j, p in enumerate(players) if p.score == max_score]
        winner = rng.choice(tied)
        end_reason = "turn_limit"

    return GameRecord(
        winner_seat=winner,
        winner_agent=players[winner].agent_name,
        turns=turn,
        end_reason=end_reason,
        final_scores=[p.score for p in players],
        final_agent_names=[p.agent_name for p in players],
        seat_winners=[i == winner for i in range(len(players))],
        completed_word_cards=completed_words,
        stolen_word_cards=stolen_words,
        opening_hands=opening_hands,
        opening_words=opening_words,
        logograms_played=logograms_played,
        steals_executed=steals_executed,
        trash_actions=trash_actions,
        logogram_exchanges=logogram_exchanges,
        first_scorer_seat=first_scorer_seat,
        first_scorer_won=(first_scorer_seat == winner),
        mulligans_used=mulligans_total,
        bonus_points=bonus_points_total,
        seed=seed,
    )


# =============================================================================
# Batch + analytics
# =============================================================================


def run_batch(n_games: int, base_seed: int, sign_pool, word_pool,
              logogram_pool, cfg: GameConfig) -> list[GameRecord]:
    results = []
    for i in range(n_games):
        rec = simulate_game(base_seed + i, sign_pool, word_pool, logogram_pool, cfg)
        results.append(rec)
    return results


def analyze(results: list[GameRecord]) -> dict:
    n = len(results)
    if n == 0:
        return {}

    n_players = len(results[0].final_scores)

    # Win rate by seat
    seat_wins = Counter()
    for r in results:
        seat_wins[r.winner_seat] += 1

    # Win rate by agent
    agent_wins = Counter()
    agent_games = Counter()
    for r in results:
        for i, name in enumerate(r.final_agent_names):
            agent_games[name] += 1
            if r.seat_winners[i]:
                agent_wins[name] += 1

    # Game length
    turns = [r.turns for r in results]
    turns.sort()
    median_turns = turns[len(turns) // 2]

    # End reason
    end_reasons = Counter(r.end_reason for r in results)

    # Word completion frequency
    word_completions = Counter()
    for r in results:
        for w in r.completed_word_cards:
            word_completions[w] += 1

    # Stolen words
    stolen = Counter()
    for r in results:
        for w in r.stolen_word_cards:
            stolen[w] += 1

    # Logogram/steal action rates
    avg_logo = sum(r.logograms_played for r in results) / n
    avg_steal = sum(r.steals_executed for r in results) / n
    # v8.9 comeback-health metric: how often the seat that scored the game's
    # FIRST word went on to win. 1/n_players = perfect; 1.0 = pure runaway.
    scored_games = [r for r in results if r.first_scorer_seat >= 0]
    first_scorer_win_rate = (
        round(sum(r.first_scorer_won for r in scored_games) / len(scored_games), 3)
        if scored_games else None)
    avg_mulligans = sum(r.mulligans_used for r in results) / n
    avg_trash = sum(r.trash_actions for r in results) / n

    # Average score
    avg_score = sum(sum(r.final_scores) / len(r.final_scores) for r in results) / n

    # Broken openers — opening hands correlated with winning
    # For each seat-0 player, group by sorted opening-hand sign-class signature
    opening_class_wins = defaultdict(lambda: [0, 0])  # signature -> [games, wins]
    for r in results:
        for seat in range(n_players):
            sig = tuple(sorted(r.opening_hands[seat]))
            opening_class_wins[sig][0] += 1
            if r.seat_winners[seat]:
                opening_class_wins[sig][1] += 1
    # Show signatures observed in at least 3 games (lower threshold because
    # word/sign combos are highly variable across games)
    broken_openers = sorted(
        [(sig, games, wins, wins/games)
         for sig, (games, wins) in opening_class_wins.items()
         if games >= 3 and wins/games >= 0.7],
        key=lambda x: (-x[3], -x[1])
    )[:15]

    # First-card hand contents (sign classes) win rates
    class_in_open = defaultdict(lambda: [0, 0])
    for r in results:
        for seat in range(n_players):
            # Distinguish by which sign classes appeared at all
            classes = set()
            # We don't have classes in opening_hands (only codes). Reuse sign_pool lookup not available here.
            for s in r.opening_hands[seat]:
                classes.add(s)
            for cls in classes:
                class_in_open[cls][0] += 1
                if r.seat_winners[seat]:
                    class_in_open[cls][1] += 1

    # Opening WORD card win rates
    open_word_wins = defaultdict(lambda: [0, 0])
    for r in results:
        for seat in range(n_players):
            w = r.opening_words[seat]
            open_word_wins[w][0] += 1
            if r.seat_winners[seat]:
                open_word_wins[w][1] += 1
    open_word_ranked = sorted(
        [(w, games, wins, wins/games)
         for w, (games, wins) in open_word_wins.items() if games >= 10],
        key=lambda x: -x[3]
    )

    # Balance score: 0-100
    # Components:
    #   - Seat-fairness: how close to 1/n_players each seat's win rate is
    #   - Agent-fairness: how close agent win rates are (only meaningful for same-agent batches; ignored otherwise)
    #   - Game-length sanity: 50-150 turns is "good"
    #   - End-reason variety: too many turn_limits = stalemate-prone
    target_seat = 1.0 / n_players
    seat_dev = sum(abs(seat_wins[i]/n - target_seat) for i in range(n_players)) / n_players
    seat_score = max(0.0, 1.0 - seat_dev / target_seat)
    length_score = 1.0 if 30 <= median_turns <= 150 else max(0.0, 1.0 - abs(median_turns - 90) / 90)
    stalemate_rate = end_reasons["turn_limit"] / n
    stalemate_score = 1.0 - stalemate_rate
    balance_score = round(100 * (0.4 * seat_score + 0.3 * length_score + 0.3 * stalemate_score), 1)

    return {
        "n_games": n,
        "n_players": n_players,
        "median_turns": median_turns,
        "avg_score": round(avg_score, 1),
        "avg_logograms_per_game": round(avg_logo, 2),
        "avg_steals_per_game": round(avg_steal, 2),
        "first_scorer_win_rate": first_scorer_win_rate,
        "avg_mulligans_per_game": round(avg_mulligans, 2),
        "avg_trash_actions_per_game": round(avg_trash, 2),
        "end_reasons": dict(end_reasons),
        "seat_win_rates": {f"seat_{i}": round(seat_wins[i] / n, 3) for i in range(n_players)},
        "agent_win_rates": {a: round(agent_wins[a] / agent_games[a], 3)
                            for a in agent_games if agent_games[a]},
        "top_completed_words": word_completions.most_common(15),
        "top_stolen_words": stolen.most_common(10),
        "broken_openers": [{
            "opening_signs": list(sig)[:7],
            "games_observed": games,
            "win_rate": round(rate, 3),
        } for sig, games, wins, rate in broken_openers[:10]],
        "best_opening_word_cards": [{
            "word": w, "games": games, "win_rate": round(rate, 3)
        } for w, games, wins, rate in open_word_ranked[:10]],
        "worst_opening_word_cards": [{
            "word": w, "games": games, "win_rate": round(rate, 3)
        } for w, games, wins, rate in open_word_ranked[-10:]],
        "balance_score": balance_score,
    }


# =============================================================================
# Markdown report
# =============================================================================


def write_report(stats: dict, cfg: GameConfig, out_path: Path):
    md = [f"# Playtest Report — Hieroglyph Quest"]
    md.append("")
    md.append(f"**Configuration**: {cfg.n_players} players, "
              f"agents = {cfg.agent_names}, "
              f"{stats['n_games']:,} games simulated.")
    md.append("")
    md.append(f"## Balance score: **{stats['balance_score']}/100**")
    md.append("")
    md.append(f"Higher = more balanced. Composed of seat-fairness (40%), "
              f"game-length sanity (30%), and stalemate avoidance (30%).")
    md.append("")
    md.append("## Game-flow summary")
    md.append("")
    md.append(f"- Median game length : **{stats['median_turns']} turns**")
    md.append(f"- Average final score: {stats['avg_score']}")
    md.append(f"- Logograms played per game (avg): {stats['avg_logograms_per_game']}")
    md.append(f"- Steals per game (avg): {stats['avg_steals_per_game']}")
    md.append("- End reasons:")
    for r, n in stats["end_reasons"].items():
        md.append(f"  - {r}: {n} ({100*n/stats['n_games']:.1f}%)")
    md.append("")
    md.append("## Seat (first-player) advantage")
    md.append("")
    md.append("Win rate by seat order. Ideal: each seat ~= 1/N.")
    md.append("")
    md.append("| Seat | Win rate |")
    md.append("|---|---:|")
    for seat, rate in stats["seat_win_rates"].items():
        md.append(f"| {seat} | {rate*100:.1f}% |")
    md.append("")
    md.append("## Agent matchup")
    md.append("")
    md.append("Win rate by AI agent strategy.")
    md.append("")
    md.append("| Agent | Win rate |")
    md.append("|---|---:|")
    for agent, rate in stats["agent_win_rates"].items():
        md.append(f"| {agent} | {rate*100:.1f}% |")
    md.append("")
    md.append("## Most-completed word cards (top 15)")
    md.append("")
    md.append("Words that appear in lots of completed-card piles — frequent + valuable.")
    md.append("")
    md.append("| Word | Times completed |")
    md.append("|---|---:|")
    for w, n in stats["top_completed_words"]:
        md.append(f"| `{w}` | {n} |")
    md.append("")
    md.append("## Most-stolen word cards (top 10)")
    md.append("")
    md.append("Words that opponents steal often — these may be too valuable or too easy.")
    md.append("")
    md.append("| Word | Times stolen |")
    md.append("|---|---:|")
    for w, n in stats["top_stolen_words"]:
        md.append(f"| `{w}` | {n} |")
    md.append("")
    md.append("## Best opening word cards")
    md.append("")
    md.append("Word cards that, when drawn at game start, correlate with winning.")
    md.append("")
    md.append("| Opening word | Games | Win rate |")
    md.append("|---|---:|---:|")
    for r in stats["best_opening_word_cards"]:
        md.append(f"| `{r['word']}` | {r['games']} | {r['win_rate']*100:.1f}% |")
    md.append("")
    md.append("## Worst opening word cards")
    md.append("")
    md.append("Word cards that consistently give their drawer a poor game.")
    md.append("")
    md.append("| Opening word | Games | Win rate |")
    md.append("|---|---:|---:|")
    for r in stats["worst_opening_word_cards"]:
        md.append(f"| `{r['word']}` | {r['games']} | {r['win_rate']*100:.1f}% |")
    md.append("")
    md.append("## Broken openers (opening hand signatures)")
    md.append("")
    md.append("Specific opening hands that win disproportionately often.")
    md.append("Each is reproducible: run the same seed with the same config to replay.")
    md.append("")
    md.append("| Opening sign codes (first 7) | Games | Win rate |")
    md.append("|---|---:|---:|")
    for op in stats["broken_openers"]:
        signs_text = " ".join(op["opening_signs"])
        md.append(f"| `{signs_text}` | {op['games_observed']} | {op['win_rate']*100:.1f}% |")
    md.append("")
    md.append("## Recommendations")
    md.append("")
    recs = []
    if abs(stats["seat_win_rates"][f"seat_0"] - 1.0/stats["n_players"]) > 0.05:
        recs.append("- **Seat-0 advantage detected.** Consider letting later seats draw an extra opening card or sign card to compensate.")
    if stats["avg_logograms_per_game"] > 1.0:
        recs.append("- **Logograms are very common in play.** They may be too easy to acquire; consider reducing their count or making them harder to draw.")
    if stats["avg_steals_per_game"] < 0.1:
        recs.append("- **Steals are rare.** The steal mechanic may be too strict; consider letting players steal across multiple turns or relaxing the all-in-one-turn rule.")
    if stats["end_reasons"].get("turn_limit", 0) / stats["n_games"] > 0.15:
        recs.append("- **More than 15% of games stalemate.** Consider raising the hand limit so players can build toward longer words, or lowering points_to_win.")
    if not recs:
        recs.append("- Game looks reasonably balanced. Continue playtesting with human players to validate.")
    for r in recs:
        md.append(r)
    md.append("")

    out_path.write_text("\n".join(md))


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=5000, help="Number of games to simulate")
    parser.add_argument("--players", type=int, default=2, help="Number of players per game")
    parser.add_argument("--agents", type=str, default="balanced,balanced",
                        help="Comma-separated agent names (random, greedy, balanced)")
    parser.add_argument("--seed", type=int, default=12345, help="Base seed for reproducibility")
    parser.add_argument("--points-to-win", type=int, default=7)
    parser.add_argument("--max-turns", type=int, default=1000)
    parser.add_argument("--starting-hand", type=int, default=8)
    parser.add_argument("--hand-limit", type=int, default=12)
    parser.add_argument("--out", type=str, default="balance_report.md")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sign_pool, word_pool, logogram_pool = load_deck()
    print(f"Loaded deck: {len(sign_pool)} sign cards (copies expanded), "
          f"{len(word_pool)} word cards, {len(logogram_pool)} logograms")

    cfg = GameConfig(
        n_players=args.players,
        agent_names=args.agents.split(","),
        starting_hand=args.starting_hand,
        hand_limit=args.hand_limit,
        points_to_win=args.points_to_win,
        max_turns=args.max_turns,
    )
    print(f"Config: {cfg.n_players} players, agents={cfg.agent_names}, "
          f"target {cfg.points_to_win} pts, max {cfg.max_turns} turns")

    print(f"\nRunning {args.games:,} games (base seed {args.seed})...")
    results = run_batch(args.games, args.seed, sign_pool, word_pool, logogram_pool, cfg)
    print(f"Done. Analyzing...")
    stats = analyze(results)
    out_path = OUT_DIR / args.out
    write_report(stats, cfg, out_path)
    print(f"\nReport written to: {out_path}")
    print(f"\n=== Quick summary ===")
    print(f"Balance score : {stats['balance_score']}/100")
    print(f"Median turns  : {stats['median_turns']}")
    print(f"Seat 0 win %  : {stats['seat_win_rates'].get('seat_0', 0)*100:.1f}%")
    print(f"Agent rates   : {stats['agent_win_rates']}")
    print(f"Top word      : {stats['top_completed_words'][0] if stats['top_completed_words'] else '-'}")
    print(f"End reasons   : {stats['end_reasons']}")

    # Also dump raw results json for further offline analysis
    raw_path = OUT_DIR / "raw_results.json"
    with open(raw_path, "w") as f:
        json.dump({"stats": stats, "config": {
            "n_players": cfg.n_players,
            "agents": cfg.agent_names,
            "n_games": args.games,
            "seed": args.seed,
        }}, f, indent=2)
    print(f"Raw stats     : {raw_path}")


if __name__ == "__main__":
    main()
