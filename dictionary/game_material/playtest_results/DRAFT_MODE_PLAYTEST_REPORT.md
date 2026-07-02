# Draft Mode Playtest (Sushi Go structure)

Core deck (v8.10 build), 60 games per cell, seed 1000. 3 rounds of pick-and-pass (hands 10/9/8 at 2/3/4p), face-up word board visible during the draft, alternating completion phase, leftovers discarded between rounds. Highest score after 3 rounds wins. No draw step exists — draw luck is deleted by construction.

## Smart mirror by player count

| Variant | Players | Words/game | Avg winning score | Avg spread | Tie % | Logos/g | Sign use % | Est. minutes | Seat rates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| draft6 | 2 | 0.4 | 0.6 | 0.6 | 66.7 | 0.17 | 0.7 | 10.1 | 57% / 43% |
| draft6 | 3 | 0.5 | 0.7 | 0.7 | 63.3 | 0.23 | 0.6 | 10.1 | 32% / 27% / 42% |
| draft6 | 4 | 0.5 | 0.8 | 0.8 | 63.3 | 0.33 | 0.4 | 10.0 | 37% / 27% / 13% / 23% |
| draft6r | 2 | 0.4 | 0.6 | 0.6 | 68.3 | 0.17 | 0.8 | 10.1 | 55% / 45% |
| draft6r | 3 | 0.5 | 0.7 | 0.7 | 63.3 | 0.23 | 0.6 | 10.1 | 32% / 27% / 42% |
| draft6r | 4 | 0.5 | 0.9 | 0.9 | 60.0 | 0.35 | 0.4 | 10.0 | 37% / 25% / 13% / 25% |
| draft8 | 2 | 0.6 | 0.9 | 0.9 | 50.0 | 0.25 | 1.2 | 10.1 | 57% / 43% |
| draft8 | 3 | 0.6 | 0.9 | 0.9 | 55.0 | 0.37 | 0.6 | 10.1 | 37% / 23% / 40% |
| draft8 | 4 | 0.8 | 1.3 | 1.3 | 50.0 | 0.52 | 0.7 | 10.1 | 30% / 27% / 22% / 22% |
| draft_carry | 2 | 1.4 | 1.7 | 1.3 | 35.0 | 0.37 | 3.9 | 10.3 | 52% / 48% |
| draft_carry | 3 | 1.6 | 1.6 | 1.5 | 38.3 | 0.45 | 3.0 | 10.3 | 28% / 32% / 40% |
| draft_carry | 4 | 1.9 | 2.2 | 2.1 | 40.0 | 0.62 | 3.0 | 10.5 | 27% / 15% / 28% / 30% |
| draft_carry10 | 2 | 1.8 | 2.7 | 1.9 | 25.0 | 0.6 | 4.9 | 10.4 | 50% / 50% |
| draft_carry10 | 3 | 2.5 | 2.6 | 2.4 | 30.0 | 0.85 | 4.4 | 10.6 | 37% / 22% / 42% |
| draft_carry10 | 4 | 2.7 | 2.5 | 2.3 | 26.7 | 0.85 | 4.1 | 10.7 | 23% / 32% / 13% / 32% |

## Skill check (random vs smart drafter, 2p)

| Variant | Smart win % | Tie % |
|---|---:|---:|
| draft6 | 71.7 | 58.3 |
| draft6r | 71.7 | 58.3 |
| draft8 | 76.7 | 43.3 |
| draft_carry | 71.7 | 31.7 |
| draft_carry10 | 75.0 | 21.7 |

## Reading of the results: the structure doesn't fit

**The pure Sushi Go structure is broken here** — not mistuned, broken. draft6/draft6r/draft8 complete 0.4-0.8 words per GAME (all players, all 3 rounds combined) with 50-68% of games ending in ties, mostly 0-0. The reason is arithmetic, not tuning: Sushi Go works because EVERY drafted card scores; Hieroglyph Quest words demand an exact multiset of specific signs. A round exposes only hand_size × players cards (20 at 2p) out of a 374-card sign space, so the probability that the 2-5 specific signs a board word needs even PASS THROUGH the draft is a few percent. The classic game solves this by cycling hundreds of cards per game (draw-2-keep-1, market, recycle); a draft structurally cannot.

**Rescue attempts helped but nowhere near enough.** Keeping drafted signs across rounds (draft_carry) and enlarging the board and hands (draft_carry10) lifted completions to 1.8-2.7 words/game with 25-30% ties — better, but that's still one word per player per 30-minute game and a quarter of games decided by tiebreaker. Sign utilization peaked at 5%: players draft 30 cards to spend 1.5 of them. The fun would not survive contact with a table.

**Verdict: do not pursue as designed.** Drafting is only compatible with this game if scoring is redesigned so partial progress scores — e.g. score drafted signs that match ANY consonant of a claimed word, set-collection style, with full spelling as a bonus rather than the only payoff. That's a different game wearing the same deck, and it would abandon the documented-spellings mechanic that defines the project. The draw-luck problem drafting was meant to solve is also far smaller than it used to be: the market, draw-2-keep-1, word choice, recycle, and the mulligan are all draw-luck dampeners the classic game has gained since v8. Recommendation: shelve Draft Mode; if a faster/lighter mode is wanted, Race Mode (already shipped) is the better vehicle.

## Caveats

Standalone simulator (`playtest_draft.py`), separate from the classic engine. Agents draft for themselves only — no hate-drafting (taking a card because an opponent needs it), which is a real and probably significant human layer. Wall-clock estimates assume 12 s per simultaneous pick round and 10 s per completion turn.