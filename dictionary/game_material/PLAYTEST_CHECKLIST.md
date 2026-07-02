# Hieroglyph Quest — Human Playtest Checklist (v8.10)

The list of things to watch for at a real table that the simulator
cannot measure. The game is shippable on the data; this is the layer
only humans reveal. Print it, take notes during sessions, and bring
tunable problems back to the simulator as hypotheses.

Covers all three modes: **Classic** (competitive, v8.10), **Race Mode**
(shared board, no steals), and **Scribes Together** (co-op / solo).

## Session setup

For each session, record:

- **Date / location / group.**
- **Mode played** (Classic / Race / Scribes Together / Mix) and which
  expansion deck(s), with the base sign library solo or mixed.
- **Player count (1-4) and experience level** per player: *first-time*
  / *played once* / *experienced*.
- **Familiarity with hieroglyphs** (0-10). Still the dominant variable
  for turn time; note Egyptology enthusiasts separately.
- **Targets used** (scaled points for Classic/Race; difficulty tier
  for Scribes Together).
- **Wall-clock start and end per game** — the headline number the
  simulator can't generate.

## Headline questions

### 1. Wall-clock time per game

Simulator medians under v8.10 (at a calibrated 15 s/turn): Classic 2p
~144 turns ≈ 36 min, 3p ~117 ≈ 29 min, 4p ~116 ≈ 29 min. Race Mode 2p
runs ~35% longer than Classic. Scribes Together runs ~175-180 total
turns at any player count (the deck is the clock).

Real values by experience level:

- **First-time players:** 25-35 s/turn (sign recognition is the
  bottleneck). Expect 60-90 min.
- **Second-game-onward:** 12-18 s/turn. Expect 30-45 min.
- **Experienced:** 8-12 s/turn. Expect 20-30 min.

Goals: ~35-min Classic game at 3p second-game-onward; 2p should feel
like Sushi Go / Lost Cities, not Splendor / Wingspan; 4p under 50 min
even with first-timers. Flag any cell consistently over 75 min.

### 2. Turn-time distribution

- **Fast (<10 s):** routine draw + discard. Should be 70-80% of turns.
- **Medium (10-30 s):** playing signs, weighing a market take, choosing
  between 2 word cards. ~15-25%.
- **Slow (>30 s):** planning a steal, a logogram play, or a mulligan.
  Should be ≤5%.

Flag if slow turns exceed 15% (analysis paralysis). New in v8.8+:
watch whether the **word draw-2-keep-1 choice** creates slow turns for
first-timers reading two word cards at once.

## Mechanics to watch (Classic)

### Hieroglyph readability

Still the top human-only variable. Watch for sign pairs beginners
confuse (e.g. Q3 vs D21 — small rectangles), whether the mnemonic is
readable across the table, and whether the English gloss is
intelligible without the transliteration. If players need the gloss to
identify SIGNS as well as words, that's a card-layout fix, not a rules
fix.

### The word mulligan (v8.9 — WATCH CLOSELY)

The game's only once-per-game power, tracked by flipping a coin
marker.

- **Do players remember it exists?** If first-timers never use it,
  the rules card needs a MULLIGAN reminder line or a printed marker.
- **When do they spend it?** Simulator agents spend ~1.6-2.8 per game
  across the table (i.e. most players use theirs). Too early (turn 2)
  or never are both signals.
- **Does the coin flip feel satisfying or fiddly?** This decides
  whether a printed marker is worth adding to the box.

### The recycle action (v8.10)

Discard 2, draw 2, instead of playing signs. The simulator uses it on
most idle turns — it's the pacing engine.

- **Do players find it without prompting?** It's the "nothing good
  happened" turn; if they instead sit and pass, games will drag far
  past the simulator estimates.
- **Does it feel productive or like a wasted turn?** If the latter,
  consider renaming/reframing on the rules card, not changing rules.

### The face-up market and discard-take

- Is the 5-card row visible from every seat?
- Do players actually scan the market, or blind-draw by default?
- Refill timing clear (immediately after a take)?
- At 3p+: do players notice the discard is takeable? Do they
  **strategically discard** signs the next player can't use? (The
  simulator's expert agent shows this denial layer exists — see
  whether humans find it.)
- Does the 2-player no-discard-take restriction feel deliberate or
  arbitrary? One-sentence explanation on the rules card if needed.

### Steals

v8.8 roughly **doubled steal rates** (now ~1.5/game at 2p, ~2.5 at 3p,
~3.8 at 4p) — the social questions matter twice as much:

- **The first steal of the session:** "oh cool" or "that's bullshit"?
  If the latter, consider the Race Mode pitch ("if your table hates
  this, play the board mode") rather than softening Classic.
- Do players ever steal at all? If steal rate is far below ~1/game
  across sessions, humans are avoiding it out of social discomfort.
- Does getting stolen from feel recoverable? (The victim redraws with
  choice, and comeback health is good on the data: first-scorer wins
  only 53% at 2p.) Watch whether it FEELS that way.

### Logograms

Fire rate is now ~1-1.5/game (up from ~0.3 pre-v8.8). Watch for the
"yes!" moment on a matching draw, and for frustration when one sits
dead in hand. (A dead-logogram exchange rule was simulated and
rejected — it gutted the "yes!" moments. If tables still hate dead
logograms, the bounded once-per-game exchange is the thing to test
next, not the unrestricted version.)

### Optional advanced rules (if the table opts in)

- **Determinative bonus:** did the table remember to raise targets to
  10/9/8? Does claiming a classifier card feel thematic ("this word
  needs the walking legs!") or like bookkeeping? Does the supply-
  limited pool create a race for popular classifiers (D54, A2)?
- **Honorific transposition:** do players spot the marker and enjoy
  announcing the god, or does it go unused? It's the most educational
  +1 in the game — if nobody engages, the marker needs to be louder
  on the card.

### Endgame round (equal turns)

- Does the table notice/announce the endgame trigger?
- Does anyone win it dramatically in the final round? If never, it's
  a polite formality (that's fine — it exists for perceived fairness).

## Race Mode sessions

- **Board reading load:** 5 open word cards is a lot of hieroglyphs
  for beginners. Do players scan the whole board or fixate on one
  word?
- **Dredge usage:** do players use it at all? As tempo (stale board)
  or as denial (burying an opponent's word)? The first deliberate
  denial dredge is Race Mode's "first steal" moment — record the
  reaction.
- **Does no-steals actually reduce friction** for steal-averse groups,
  or does the race produce the same feelings by other means?
- **2p length:** simulator says ~35% longer than Classic 2p. Does it
  feel slow, or does open information make it feel faster than it is?

## Scribes Together sessions

- **Tier choice:** does the table pick Apprentice first as
  instructed? Does beating it feel earned or automatic? (Tiers err
  forgiving by design; if Apprentice is a rout, recommend starting at
  Scribe in the rules card.)
- **Clock awareness:** do teams hoard cards and stop recycling when
  the deck runs low? (Agents don't — humans who do should beat the
  printed curves. If teams beat Master Scribe regularly, tiers need a
  bump.)
- **Table talk:** is unlimited coordination fun, or does an
  experienced player quarterback everyone else's turns? (Classic
  co-op failure mode — if it appears, test a "no naming specific
  cards" house rule.)
- **Solo:** is a ~180-turn solo session engaging or grindy? Where does
  it stop being fun — track the turn number.
- **Assists:** do teammates actually complete each other's words, or
  play solitaire side by side?

## Mix Mode (combining expansions)

- Does the bigger pool feel exciting or overwhelming?
- **RETUNE FLAG:** the printed Mix Mode targets predate v8.8-v8.10
  (faster completions, mulligan, recycle). Before trusting them,
  re-run the Mix Mode sims. Treat printed Mix targets as provisional
  at the table.
- Do players have a favorite single-expansion experience they retreat
  to? (Positive signal — themes differentiating.)

## After Dark specific

- **Player consent first.** Not a "surprise the table" expansion.
- Pacing of the 55-card pool: does complete-and-rotate hold up?
- The supplemental mature signs (D27, D52, F45, F51 + copies) must be
  visually distinct enough not to get mixed into the base library
  when packing up.

## Dead-card frustration

Short games mean many word cards never appear in a session. Watch
whether players complain about "words I never got to see," and whether
they want to keep playing after game end to see more (the second is a
positive signal). If rotation complaints recur, test shuffling 30
fresh words in between games of a session.

## When to bring it back to the simulator

Parametrically tunable issues (game length, per-count balance,
mechanic fire rates, difficulty tiers, Mix targets) go back into the
sims — every lever from this design cycle is preserved in
`GameConfig`: catch-up options, dead-logogram exchange, shared pool +
dredge, co-op clock, and agent strength tiers. Issues that are NOT
simulator-tunable: card layout/readability, rules-card clarity, social
feel (steal language, quarterbacking), component quality. Those are
design and product concerns; human input is the only driver.

## Sample notes template (per game)

```
DATE:    YYYY-MM-DD      MODE: classic / race / co-op / mix
PLAYERS: 1 2 3 4 (circle)   DECK: ______________ (mix with: ________)
EXPERIENCE: [new][new][new][seasoned]     FAMILIARITY: ___/10
TARGET/TIER: ______      START: ____:____  END: ____:____  DUR: ___min

POINTS (or TEAM total):  P0 ___  P1 ___  P2 ___  P3 ___
WINNER: P__ / team won / team lost

TURN-TIME:  fast(<10s) ~__%   medium(10-30s) ~__%   slow(>30s) ~__%

NOTABLE MOMENTS:
  [ ] First steal (or denial dredge) — reaction: __________________
  [ ] First logogram fire            — reaction: __________________
  [ ] Mulligan used? by whom, what turn: _________________________
  [ ] Did anyone forget the mulligan existed?  yes / no
  [ ] Recycle discovered without prompting?    yes / no
  [ ] Endgame round dramatic?                  yes / no / n.a.
  [ ] Sign-recognition confusion — which pairs: __________________
  [ ] Co-op: quarterbacking observed?          yes / no / n.a.

WOULD THEY PLAY AGAIN?  yes / no / unsure    WHICH MODE NEXT? ________
GAME LENGTH FELT:  too short / just right / too long
```

## Closing

The simulator took the game from a flagged 60-balance, ~92-minute
v2.1 baseline to a ~35-minute v8.10 production state with validated
comeback health (first-scorer wins 53% at 2p), three playtested modes,
and calibrated co-op difficulty tiers. Roughly 80% of the design space
is closed. The remaining 20% lives in human-only signals: legibility,
social feel, whether the mulligan coin delights or annoys, and whether
the game scratches the Sushi Go itch it's aiming for. Bring back what
you learn — the numbers are documented, and every mechanism has a
lever waiting in the simulator.
