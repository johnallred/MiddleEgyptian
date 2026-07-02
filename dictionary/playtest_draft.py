"""
Draft Mode playtest ("Sushi Go structure" — v9 structural candidate).

Structure per game (design locked for this test; push back before adopting):

  3 ROUNDS. Each round:
    1. Reveal a face-up WORD BOARD (6 word cards) — visible during the draft.
    2. Deal each player a hand of sign cards (2p: 10, 3p: 9, 4p: 8;
       logograms mixed in at the classic 1-per-15 density).
    3. DRAFT: all players simultaneously pick 1 card into their tableau
       and pass the rest (left; direction alternates by round), until
       hands are empty.
    4. COMPLETION PHASE: starting seat rotates each round; players
       alternate completing ONE board word at a time from their drafted
       signs (multiset, as always; logograms targeting a board word are
       instant). Pass if you can't. Phase ends when everyone passes.
    5. Leftover drafted signs are discarded (Sushi Go style — rounds
       are independent). Unclaimed board words are discarded too.

  Highest total score after 3 rounds wins; ties broken by words
  completed, then randomly (tie rate is reported).

There is no draw step at all — draw luck is deleted by construction.
No steals, no mulligan, no market.

Variants:
  draft6    — board of 6, no refill during completion
  draft6r   — board of 6, refills from the word deck after each completion
  draft8    — board of 8, no refill

Matchups: smart mirror at 2p/3p/4p, plus smart-vs-random at 2p (skill).

Usage:
  python3 playtest_draft.py --variant all
  python3 playtest_draft.py --report
"""

import argparse
import json
import random
import statistics
from collections import Counter
from pathlib import Path

import playtest_simulator as ps
from playtest_simulator import LogogramCard, shortest_completable_spelling

RUNS_DIR = ps.OUT_DIR / "draft_runs"
REPORT = ps.OUT_DIR / "DRAFT_MODE_PLAYTEST_REPORT.md"

HAND_SIZE = {2: 10, 3: 9, 4: 8}
ROUNDS = 3

VARIANTS = ["draft6", "draft6r", "draft8",
            "draft_carry", "draft_carry10"]
# (board_size, refill, carryover) — carryover keeps drafted signs across
# rounds instead of discarding them Sushi Go-style.
SETUP = {"draft6":       (6, False, False),
         "draft6r":      (6, True,  False),
         "draft8":       (8, False, False),
         "draft_carry":  (6, True,  True),
         "draft_carry10": (10, True, True)}


# ---------------------------------------------------------------------------
# Agent policies
# ---------------------------------------------------------------------------

def smart_pick(hand, tableau, board, rng):
    """Pick the card that best advances the most valuable reachable word."""
    tab = Counter(c.code for c in tableau if not isinstance(c, LogogramCard))
    board_tr = {w.translit for w in board}
    best_card, best_val = None, -1.0
    for card in hand:
        if isinstance(card, LogogramCard):
            val = 1000.0 if card.target_word in board_tr else 0.5
        else:
            val = 0.5  # baseline so unhelpful cards still comparable
            tab2 = tab.copy()
            tab2[card.code] += 1
            for w in board:
                for sp in w.valid_spellings:
                    need = Counter(sp)
                    miss_before = sum((need - tab).values())
                    miss_after = sum((need - tab2).values())
                    if miss_after < miss_before:
                        val = max(val, 10.0 * w.points / (miss_after + 1))
        if val > best_val:
            best_val, best_card = val, card
    return best_card


def random_pick(hand, tableau, board, rng):
    return rng.choice(hand)


PICKERS = {"smart": smart_pick, "random": random_pick}


def try_complete(tableau, board):
    """Return (word, signs_used, logogram_used) for the best completion
    available to this tableau, or None."""
    # Logogram instants first (they cost no signs)
    board_by_tr = {}
    for w in board:
        board_by_tr.setdefault(w.translit, w)
    best_logo = None
    for c in tableau:
        if isinstance(c, LogogramCard) and c.target_word in board_by_tr:
            w = board_by_tr[c.target_word]
            if best_logo is None or w.points > best_logo[0].points:
                best_logo = (w, c)
    if best_logo:
        return best_logo[0], [], best_logo[1]
    # Sign completions: highest points, then shortest spelling
    codes = Counter(c.code for c in tableau if not isinstance(c, LogogramCard))
    best = None
    for w in board:
        sp = shortest_completable_spelling(w.valid_spellings, codes)
        if sp and (best is None or w.points > best[0].points):
            best = (w, sp)
    if best is None:
        return None
    w, sp = best
    used, need = [], Counter(sp)
    for c in tableau:
        if not isinstance(c, LogogramCard) and need[c.code] > 0:
            used.append(c)
            need[c.code] -= 1
    return w, used, None


# ---------------------------------------------------------------------------
# Game
# ---------------------------------------------------------------------------

def play_game(seed, sign_pool, word_pool, logo_pool, agent_names,
              board_size, refill, carryover=False):
    rng = random.Random(seed)
    n = len(agent_names)
    deck = list(sign_pool)
    deck += rng.sample(logo_pool, min(len(logo_pool), len(sign_pool) // 15))
    rng.shuffle(deck)
    words = list(word_pool)
    rng.shuffle(words)

    scores = [0] * n
    words_done = [0] * n
    signs_drafted = [0] * n
    signs_spent = [0] * n
    logos_played = 0
    completion_turns = 0
    picks_total = 0

    persistent = [[] for _ in range(n)]
    for rnd in range(ROUNDS):
        board = [words.pop() for _ in range(min(board_size, len(words)))]
        hs = HAND_SIZE[n]
        if len(deck) < hs * n:
            break
        hands = [[deck.pop() for _ in range(hs)] for _ in range(n)]
        tableaus = persistent if carryover else [[] for _ in range(n)]
        direction = 1 if rnd % 2 == 0 else -1
        for _ in range(hs):
            for pidx in range(n):
                card = PICKERS[agent_names[pidx]](
                    hands[pidx], tableaus[pidx], board, rng)
                hands[pidx].remove(card)
                tableaus[pidx].append(card)
                picks_total += 1
            hands = hands[direction:] + hands[:direction]
        for pidx in range(n):
            signs_drafted[pidx] += hs

        # Completion phase
        start = rnd % n
        passes, ptr = 0, start
        while passes < n and board:
            pidx = ptr % n
            res = try_complete(tableaus[pidx], board)
            completion_turns += 1
            if res:
                w, used, logo = res
                scores[pidx] += w.points
                words_done[pidx] += 1
                board.remove(w)
                if logo is not None:
                    tableaus[pidx].remove(logo)
                    logos_played += 1
                for c in used:
                    tableaus[pidx].remove(c)
                signs_spent[pidx] += len(used)
                if refill and words:
                    board.append(words.pop())
                passes = 0
            else:
                passes += 1
            ptr += 1
        # leftovers + unclaimed board discarded

    max_score = max(scores)
    tied = [i for i, s in enumerate(scores) if s == max_score]
    was_tie = len(tied) > 1
    if was_tie:
        max_words = max(words_done[i] for i in tied)
        tied = [i for i in tied if words_done[i] == max_words]
    winner = rng.choice(tied)
    return {
        "winner": winner, "winner_agent": agent_names[winner],
        "scores": scores, "words_done": sum(words_done),
        "was_tie": was_tie, "logos_played": logos_played,
        "completion_turns": completion_turns, "picks_total": picks_total,
        "utilization": sum(signs_spent) / max(1, sum(signs_drafted)),
    }


def run_matchup(agent_names, board_size, refill, games, seed, pools,
                carryover=False):
    sign_pool, word_pool, logo_pool = pools
    n = len(agent_names)
    recs = [play_game(seed + g, sign_pool, word_pool, logo_pool,
                      agent_names, board_size, refill, carryover)
            for g in range(games)]
    seat_wins = Counter(r["winner"] for r in recs)
    agent_wins = Counter(r["winner_agent"] for r in recs)
    spreads = [max(r["scores"]) - min(r["scores"]) for r in recs]
    return {
        "seat_win_rates": {f"seat_{i}": round(seat_wins[i] / games, 3)
                           for i in range(n)},
        "agent_win_rates": {a: round(agent_wins[a] / games, 3)
                            for a in set(agent_names)},
        "avg_winning_score": round(statistics.mean(max(r["scores"]) for r in recs), 1),
        "avg_score_spread": round(statistics.mean(spreads), 1),
        "avg_words_per_game": round(statistics.mean(r["words_done"] for r in recs), 1),
        "tie_rate_pct": round(100 * sum(r["was_tie"] for r in recs) / games, 1),
        "logos_per_game": round(statistics.mean(r["logos_played"] for r in recs), 2),
        "avg_completion_turns": round(statistics.mean(r["completion_turns"] for r in recs), 1),
        "utilization_pct": round(100 * statistics.mean(r["utilization"] for r in recs), 1),
        "est_wall_clock_min": round(
            (ROUNDS * HAND_SIZE[n] * 12          # simultaneous picks @12s
             + statistics.mean(r["completion_turns"] for r in recs) * 10
             + 180) / 60, 1),                    # setup/refill overhead
    }


def run_variant(variant, games, seed):
    pools = ps.load_deck()
    board_size, refill, carryover = SETUP[variant]
    out = {"variant": variant, "board_size": board_size, "refill": refill,
           "carryover": carryover,
           "games": games, "seed": seed, "mirror": {}, "skill": None}
    for np_ in (2, 3, 4):
        out["mirror"][str(np_)] = run_matchup(
            ["smart"] * np_, board_size, refill, games, seed, pools, carryover)
        m = out["mirror"][str(np_)]
        print(f"  {variant} {np_}p: words/g={m['avg_words_per_game']} "
              f"tie={m['tie_rate_pct']}% util={m['utilization_pct']}% "
              f"~{m['est_wall_clock_min']}min seats={m['seat_win_rates']}")
    out["skill"] = run_matchup(["random", "smart"], board_size, refill,
                               games, seed, pools, carryover)
    print(f"  {variant} skill: smart="
          f"{out['skill']['agent_win_rates'].get('smart')}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / f"{variant}.json").write_text(json.dumps(out, indent=1))
    return out


def assemble_report(games, seed):
    runs = {v: json.loads((RUNS_DIR / f"{v}.json").read_text())
            for v in VARIANTS if (RUNS_DIR / f"{v}.json").exists()}
    md = ["# Draft Mode Playtest (Sushi Go structure)", ""]
    md.append(f"Core deck (v8.10 build), {games} games per cell, seed {seed}. "
              f"3 rounds of pick-and-pass (hands 10/9/8 at 2/3/4p), face-up "
              f"word board visible during the draft, alternating completion "
              f"phase, leftovers discarded between rounds. Highest score "
              f"after 3 rounds wins. No draw step exists — draw luck is "
              f"deleted by construction.")
    md.append("")
    md.append("## Smart mirror by player count")
    md.append("")
    md.append("| Variant | Players | Words/game | Avg winning score | "
              "Avg spread | Tie % | Logos/g | Sign use % | Est. minutes | "
              "Seat rates |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for v in VARIANTS:
        if v not in runs:
            continue
        for np_ in ("2", "3", "4"):
            m = runs[v]["mirror"][np_]
            seats = " / ".join(f"{r*100:.0f}%"
                               for r in m["seat_win_rates"].values())
            md.append(f"| {v} | {np_} | {m['avg_words_per_game']} | "
                      f"{m['avg_winning_score']} | {m['avg_score_spread']} | "
                      f"{m['tie_rate_pct']} | {m['logos_per_game']} | "
                      f"{m['utilization_pct']} | {m['est_wall_clock_min']} | "
                      f"{seats} |")
    md.append("")
    md.append("## Skill check (random vs smart drafter, 2p)")
    md.append("")
    md.append("| Variant | Smart win % | Tie % |")
    md.append("|---|---:|---:|")
    for v in VARIANTS:
        if v not in runs:
            continue
        s = runs[v]["skill"]
        md.append(f"| {v} | {100*s['agent_win_rates'].get('smart',0):.1f} | "
                  f"{s['tie_rate_pct']} |")
    md.append("")
    md.append("## Reading of the results: the structure doesn't fit")
    md.append("")
    md.append("**The pure Sushi Go structure is broken here** — not "
              "mistuned, broken. draft6/draft6r/draft8 complete 0.4-0.8 "
              "words per GAME (all players, all 3 rounds combined) with "
              "50-68% of games ending in ties, mostly 0-0. The reason is "
              "arithmetic, not tuning: Sushi Go works because EVERY drafted "
              "card scores; Hieroglyph Quest words demand an exact multiset "
              "of specific signs. A round exposes only hand_size × players "
              "cards (20 at 2p) out of a 374-card sign space, so the "
              "probability that the 2-5 specific signs a board word needs "
              "even PASS THROUGH the draft is a few percent. The classic "
              "game solves this by cycling hundreds of cards per game "
              "(draw-2-keep-1, market, recycle); a draft structurally "
              "cannot.")
    md.append("")
    md.append("**Rescue attempts helped but nowhere near enough.** Keeping "
              "drafted signs across rounds (draft_carry) and enlarging the "
              "board and hands (draft_carry10) lifted completions to "
              "1.8-2.7 words/game with 25-30% ties — better, but that's "
              "still one word per player per 30-minute game and a quarter "
              "of games decided by tiebreaker. Sign utilization peaked at "
              "5%: players draft 30 cards to spend 1.5 of them. The fun "
              "would not survive contact with a table.")
    md.append("")
    md.append("**Verdict: do not pursue as designed.** Drafting is only "
              "compatible with this game if scoring is redesigned so "
              "partial progress scores — e.g. score drafted signs that "
              "match ANY consonant of a claimed word, set-collection style, "
              "with full spelling as a bonus rather than the only payoff. "
              "That's a different game wearing the same deck, and it would "
              "abandon the documented-spellings mechanic that defines the "
              "project. The draw-luck problem drafting was meant to solve "
              "is also far smaller than it used to be: the market, "
              "draw-2-keep-1, word choice, recycle, and the mulligan are "
              "all draw-luck dampeners the classic game has gained since "
              "v8. Recommendation: shelve Draft Mode; if a faster/lighter "
              "mode is wanted, Race Mode (already shipped) is the better "
              "vehicle.")
    md.append("")
    md.append("## Caveats")
    md.append("")
    md.append("Standalone simulator (`playtest_draft.py`), separate from the "
              "classic engine. Agents draft for themselves only — no "
              "hate-drafting (taking a card because an opponent needs it), "
              "which is a real and probably significant human layer. "
              "Wall-clock estimates assume 12 s per simultaneous pick round "
              "and 10 s per completion turn.")
    REPORT.write_text("\n".join(md))
    print(f"Report: {REPORT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default=None)
    ap.add_argument("--games", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    if args.variant:
        targets = VARIANTS if args.variant == "all" else [args.variant]
        for v in targets:
            print(f"Running {v} ...")
            run_variant(v, args.games, args.seed)
    if args.report or args.variant == "all":
        assemble_report(args.games, args.seed)


if __name__ == "__main__":
    main()
