---
id: WI-0002
type: work-item
title: Review the cards that are due and record each answer
status: done
priority: high
epic: EP-001
created: "2026-08-29T10:45:15Z"
updated: "2026-08-29T12:16:14Z"
depends-on:
  - WI-0001
blocks:
  - WI-0003
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone reviewing daily, I want to be shown only the cards that are due, one at a time, and to
record whether I got each one right, so that a day's review is finite and my answers are
remembered rather than re-entered tomorrow.

## Acceptance criteria

Every criterion below is checked against a store of the checker's own, by running
`RECALL_FILE=<tmp>/cards.json` in front of each command [src: WI-0001 AC5]. The setup all of
them share is two cards added with `recall add`, which are due on the day they are added
[src: ADR-0001; EP-001] and are therefore the session's due cards.

A key is given followed by Enter: the session reads standard input a line at a time, so what a
person types and what AC9's `printf` writes are the same input. That follows from AC9 rather
than being a separate decision — a reader that demanded a terminal could not be driven from a
pipe at all.

- [x] AC1 — After `recall add "die Katze" "the cat"` and `recall add "der Hund" "the dog"`,
      running `recall review` presents those two cards one at a time, showing a card's question
      side first and its answer side only after an Enter has been read for it. Checked with
      `printf '\ny\n\nn\n' | recall review`: in the output, `die Katze` appears before `the cat`,
      `the cat` appears before `der Hund`, and neither answer side appears before the Enter that
      precedes it in the input.
- [x] AC2 — For each card presented, once the answer side is showing, the reviewer records the
      result with **`y`** for right or **`n`** for wrong — two responses, no third option and no
      finer grade. The result is still recorded after the process ends: after
      `printf '\ny\n\nn\n' | recall review`, the store file holds a recorded result for both
      cards, and the record for the card answered `y` **differs** from the record for the card
      answered `n`. `README.md` names the field that carries the result and what its two values
      mean.
- [x] AC3 — `recall review` when no card is due prints a single plain line saying nothing is
      due, presents no card, and exits 0. Checked in both of its readings: against a store with
      no cards in it at all, and again immediately after a session in which every due card was
      reviewed.
- [x] AC4 — A card reviewed in one run is not presented again by a second review run started on
      the same day: immediately after the AC2 session, a fresh `recall review` prints the AC3
      nothing-due line and presents neither card.
- [x] AC5 — **`q`** — at either moment, with the question side showing or the answer side
      showing — ends the review immediately: no further card is presented, every result already
      recorded is kept, and the cards not yet reached are still due. Checked over three due
      cards, twice. With `printf '\ny\nq\n' | recall review` — card 1 revealed and answered
      right, then `q` at card 2's question side — the output shows no third card, and a
      following `recall review` presents cards 2 and 3 and not card 1. With
      `printf '\ny\n\nq\n' | recall review` from the same starting state — `q` at card 2's
      answer side — the same holds: card 2 is still due, because `q` recorded no result for it.
- [x] AC6 — A review session's **last line on stdout** is a single line stating how many cards
      were reviewed and how many were answered right, and it is printed whether the session ran
      out of due cards or was ended with `q`. Checked on the AC2 session — the line contains `2`
      and `1` — and on the first AC5 session, where it contains `1` and `1`.
- [x] AC7 — A review session covers every card that is due, from the one flat pool: with three
      cards due, one uninterrupted session presents all three; and `recall review` takes no deck,
      tag or filter argument to narrow it — `recall review --deck german` exits non-zero, presents
      no card and records nothing, checked by a following `recall review` still presenting all
      three.
- [x] AC8 — Due cards are presented oldest-due-first, ties broken by ascending card number, and
      two review runs over the same stored state present them in that same order. Checked by
      adding three cards and then setting their stored due dates by hand — in the store file,
      through the field `README.md` documents — to two days ago for card 3 and to yesterday for
      cards 1 and 2, then driving a session from a pipe: card 3 is presented first, then card 1,
      then card 2. With that same stored state restored from a copy, a second run presents them
      in the same order.
- [x] AC9 — The whole session is drivable from a pipe: the keys AC1, AC2 and AC5 describe are
      read from standard input rather than requiring a terminal, so a session over two due cards
      is driven by `printf '\ny\n\nn\n' | recall review` — reveal, right, reveal, wrong — which
      exits 0, and AC1–AC6 are each checked by one command and its output with nobody at the
      keyboard. If the input ends before the session does, the session ends there exactly as `q`
      does: `printf '\ny\n' | recall review` over two due cards records card 1's result, leaves
      card 2 due, prints the AC6 line, and exits 0.
- [x] AC10 — A line that is not one of the keys expected at that moment is ignored: the same
      prompt is repeated, no result is recorded, and the session does not end. Checked over one
      due card with `printf 'x\n\nz\ny\n' | recall review` — `x` where an Enter or `q` was
      expected and `z` where `y`, `n` or `q` was expected are both ignored, the card is revealed
      by the Enter and recorded right by the `y`, and the AC6 line contains `1` reviewed and `1`
      right.

## Out of scope

- Computing *when* a reviewed card is next due — that is WI-0003. This item only needs "not
  again today", which AC4 states.
- Reviewing cards that are not due, and any way to force or shuffle a session.
- Undoing or re-grading an answer after it has been recorded.
- Any response other than right or wrong; the four-way grade was declined by the stakeholder in
  `EP-001/Q-003`.
- Any timing or measurement of how long the reviewer took.
- A cap on how many cards a session offers, and any way to break a long session into parts. The
  session is finite because only due cards are in it; assumed by `refine`, not stated by the
  stakeholder.
- Any command other than reviewing. Adding and listing are WI-0001.
- Anything that requires standard input to be a terminal: no raw single-keypress mode, no screen
  clearing, no cursor control, no colour. Added by `refine` in round 2, because a reader could
  reasonably assume a review session takes over the terminal. It is a consequence of AC9 rather
  than a taste: a session that cannot be driven from a pipe cannot be verified by anyone who is
  not sitting at the keyboard.
- Any command or output that shows a card's recorded results back to the reviewer — a history, a
  per-card record, a statistics line. AC2's persistence is observed by reading the store file,
  which WI-0001 AC5 exists to make possible; the epic already excludes reporting beyond what the
  review session itself shows.

## Notes

`EP-001/Q-001` and `Q-003` are answered and their answers are in the criteria above: the review
is run from a terminal, and the reviewer records right or wrong — *"Just right or wrong. I don't
want to sit there grading myself on a four-point scale for every card."* AC7 carries `Q-004`'s
flat pool. `answer-questions` amended AC1, AC2, AC3 and AC6 and added AC7 while the item was at
`draft`.

`refine` round 1 (see `artifacts/refinement-qa.md`) settled the command name, the session order
(AC8), the pipe-drivable requirement (AC9), the empty-session wording (AC3) and the
end-of-session report, all as recorded assumptions, and filed one question the stakeholder must
answer. It is now resolved:

- `Q-001` — the review key map. The stakeholder chose option A — *"Enter to see the answer, y for
  right, n for wrong, q to stop. That's the one I can just use without being told the keys."*
  AC1, AC2, AC5 and AC6 now name those keys, and AC9 carries a concrete piped invocation so a
  verifier can drive a whole session from one command.

Open design questions left for `plan` rather than for the stakeholder: whether a result is
written to the store after each card or once at the end (AC5 requires that an interrupted session
keeps what it recorded, which constrains but does not decide it), and how the session detects
that standard input is a pipe rather than a terminal for AC9. Round 2 adds three more, each of
the same kind — the answer would be the same whoever the stakeholder was:

- which fields carry a card's recorded result and its next-due date, and what the store's
  `version` becomes when they are added [src: ADR-0004];
- what a card's next-due date is set to by this item, given that it must not be due again today
  (AC4) and that WI-0003 replaces the value with the ladder's;
- how the end of standard input is distinguished from a `q`, since AC9 requires both to end the
  session the same way.

`refine` round 2 asked the stakeholder nothing. Everything still open was either covered by their
standing deferral — *"Whatever you think is best, you know this better than I do."*
(`WI-0001/Q-002`), which applies to the category of naming, output wording, file layout and
checking mechanics rather than only to the question that produced it — or was a design question
already routed to `plan`. Round 2 changed five things, all `[assumed]` in
`artifacts/refinement-qa.md`:

- **AC1 now names the setup that makes a card due.** It could not be checked before: nothing in
  this item said which cards a session presents, and a verifier with no context had no way to
  produce a due card. A newly added card is due the day it is added — already settled in
  `ADR-0001` and `EP-001` SM2, so this is a citation, not a new decision.
- **AC2 now names where the recorded result is observed** — the store file — and requires the
  record of a card answered `y` to differ from that of a card answered `n`, with `README.md`
  naming the field. "Still recorded" had no stated observation, and AC4 only shows that a card
  was reviewed, not which answer was given.
- **AC8 now names how a mixed set of due dates is produced**: by hand, in the store file, which
  is what WI-0001 AC5 makes possible and what `verify` already did for WI-0001 AC6. Without it
  the ordering was unobservable in this item, because every card in a fresh pile is equally due.
- **AC9 now settles what happens when piped input runs out** — the session ends exactly as `q`
  does. AC9 asks a verifier to drive a session from a `printf`, so an input that ends early is
  the normal case, not an edge one.
- **AC10 is new**: a line that is not one of the keys expected at that moment is ignored and the
  prompt repeats. Round 1 recorded this as unconstrained *because the key map was not yet
  settled*; `Q-001` settled it, so the reason is gone. Ignoring rather than counting a stray key
  as a wrong answer is the reading that cannot destroy a result the reviewer meant to give.

R10 — behaviour combinations introduced by this item: `review` with cards due (AC1, AC2, AC7,
AC8), with none due (AC3), with none left after a full session (AC3, AC4), stopped early at the
question side and at the answer side (AC5), run twice in a day (AC4), driven from a pipe (AC9),
with the piped input ending mid-session (AC9), with a key outside the map at either moment
(AC10), and with a deck-like argument (AC7); the end-of-session line after a full session and
after a `q` (AC6). Deliberately unconstrained, by `refine`: the exact wording of the prompts
around each card, of the nothing-due line (AC3) and of the end-of-session line (AC6), each of
which is required to exist and to carry the right numbers but not to be a particular sentence;
and whether the session prints anything between cards. Excluded rather than left open: anything
requiring a terminal, and any way to see a card's results other than the store file — both now
in `## Out of scope`. Depends on WI-0001, which is `done`, because there is nothing to review
until cards persist.

**The seam with WI-0003, recorded because this item has to pick something and WI-0003 replaces
it.** This item stores a result per card and makes a reviewed card not due again today; it does
not compute the ladder. So whatever it writes for "next due" is a placeholder that WI-0003's
AC2 and AC3 overwrite, and the store's `version` is where that shows up [src: ADR-0004]. One
thing neither item currently settles, and which WI-0003's refinement must: which rung a *newly
added* card is on when it is answered right for the first time. `ADR-0001` says a new card is
due the day it is added and that a right answer moves a card up one rung, but not what rung a
card starts on, so "due in 3 days" and "due in 1 day" are both readings of a first correct
answer. It is WI-0003's criterion to fix, not this item's.

Note for whoever refines this: AC4 ("not presented again by a second review run started on the
same day") and `ADR-0001`'s wrong-answer rule agree deliberately — a wrong answer sends a card
back to the bottom rung, which is one day, so it returns tomorrow rather than later today.

## What review accepted rather than fixed

`review-close` accepted this item and merged it. Six things were accepted rather than sent back,
and they are here rather than only in `artifacts/review.md` because a report stops being read the
moment an item closes. The full reasoning for each is in that file.

1. **A `due` that is a string but not a date silently removes a card from every review.** A card
   with `"due": "tomorrow"` is accepted by `load`, sorts above every real date in `due_cards`, and
   is never due again — while `recall list` still shows it, so it does not look lost. Reachable
   through a path the criteria endorse: AC8 requires hand-editing `due` in the store file. Not a
   criterion failure of this item and not fileable as a bug — `ADR-0006` states the `YYYY-MM-DD`
   format without requiring `load` to enforce it, so RB3 has nothing to cite. **WI-0003's
   refinement owns this**, because that item writes the same field.
2. **`cmd_review`'s `input_stream` parameter is unreachable.** It widens the signature the plan
   fixed and nothing ever passes it a value. Declared by `implement` as deviation 4 and accepted:
   one keyword argument with a default, no behaviour, plausibly useful to WI-0003. If WI-0003 does
   not use it, delete it — it is a one-line removal.
3. **`docs/architecture/overview.md`'s "roughly 280 lines" is imprecise, not wrong.** The
   delivered `recall.py` is 342 lines by `wc -l` and 274 non-blank; the document does not say which
   it means. The decision that sentence supports — keeping the store inside `recall.py` — holds
   under either reading. WI-0003 adds the ladder to the same module and will meet the sentence
   again with a larger file.
4. **Nothing was verified at a real terminal**, in implementation or in verification. That is this
   item's own design — AC9 requires pipe-drivability and `## Out of scope` excludes anything
   needing a terminal — but nobody has confirmed the tool is usable with a person at the keyboard.
5. **A card answered right comes back tomorrow**, exactly as a wrong one does. `ADR-0006`'s
   declared placeholder until WI-0003 lands, and the thing most likely to be read as a defect by
   anyone meeting the tool in between.
6. **`due` is a bare local date**, so a session crossing local midnight sees the date it started
   with, and the write protocol was not re-tested under interruption — inherited unchanged from
   WI-0001, where the same gap was accepted.
