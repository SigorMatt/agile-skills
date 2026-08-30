---
id: WI-0002
type: work-item
title: Review the cards due today and reschedule them on the fixed ladder
status: done
priority: high
epic: EP-001
created: "2026-08-30T11:04:23Z"
updated: "2026-08-30T12:53:59Z"
depends-on:
  - WI-0001
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone studying a subject, I want a daily session that shows me only the cards that are due
and asks whether I got each one right, so that I spend my time on the material I am about to
forget rather than on the whole pile.

## Acceptance criteria

- [x] AC1 — Running the tool's `review` subcommand from a terminal, with no further arguments,
      starts a session that offers the due cards one at a time. For each card the tool prints that
      card's front side and waits; nothing it has printed contains that card's back side until the
      person presses Enter at that prompt, and the back side is printed once they do.
- [x] AC2 — A card is offered when its due date is today or earlier, in the machine's local
      calendar date, and is not offered otherwise; every such card is offered, with no cap on how
      many a session may contain, and a reader can check the set the session offered against the
      due dates in the stored file by hand.
- [x] AC3 — A card whose due date is in the past is offered on the same terms as a card due today:
      being overdue changes nothing about it. Its rung in the card file is the same after the
      session started as before, however many days were missed, and when it is answered its new
      rung and due date are AC5's or AC6's, counted from the day of the review and not from the
      date it was due.
- [x] AC4 — After the back side has been shown, the tool waits for the person to record the
      outcome and accepts exactly two answers, `y` for right and `n` for wrong — no third outcome
      and no difficulty scale. As soon as one is given, that card's new rung and due date are in
      the card file before the next card's front side is printed, which a reader can check by
      reading the file from another terminal part-way through a session.
- [x] AC5 — A card answered right moves up one rung of the fixed ladder 1, 3, 7, 30 days and its
      due date is set that many days after the day of the review: rung 0 — never answered, which
      is how WI-0001 writes a newly added card — becomes rung 1, due 1 day later; rung 1 becomes
      rung 2, due 3 days later; rung 2 becomes rung 3, due 7 days later; rung 3 becomes rung 4,
      due 30 days later; and a card already at rung 4 stays at rung 4 and is due 30 days later
      again (`ADR-0002`, `ADR-0007`).
- [x] AC6 — A card answered wrong is written back at rung 1 and due one day after the day of the
      review, whatever rung it was on before — including rung 0 and including rung 4.
- [x] AC7 — The updated rungs and due dates survive stopping and starting the tool: a session
      started again on the same day offers only the cards that are still due, and offers no card
      that was answered earlier that day.
- [x] AC8 — When nothing is due — including when the card file holds no cards, and when it does
      not exist at all — the session prints a message saying nothing is due, offers no card, exits
      zero, and writes nothing: the card file afterwards is byte-identical to what it was before
      the command ran, or still does not exist if it did not before.
- [x] AC9 — Quitting a session part-way keeps every answer already given: the cards answered
      before the quit have their new rung and due date in the stored file, and the cards not
      reached are unchanged and still due. This holds both for AC11's explicit stop and for the
      tool being killed at a prompt.
- [x] AC10 — Before the first card is shown, the session states how many cards it is about to
      offer, and that number equals the number of cards in the stored file whose due date is
      today or earlier, so a reader can check it by hand.
- [x] AC11 — The session offers an explicit way to stop at any card: typing `q` at either the
      reveal prompt or the outcome prompt ends the session at once, and so does the input stream
      ending (the person pressing Ctrl-D, or a piped input running out). Either way the tool exits
      zero, prints no error, and AC9 holds — the card that was on screen was not answered and is
      unchanged in the card file. What the person may type is named in what the session prints at
      each prompt.
- [x] AC12 — When more than one card is due, the session offers them in order of due date,
      earliest first, and cards sharing a due date in the order they appear in the card file. The
      order is a function of the stored file alone: a reader can predict the whole sequence by
      reading the file before starting the session, and two sessions started against the same
      stored file offer the same order.
- [x] AC13 — Input the session does not recognise at either prompt — anything other than what
      that prompt accepts — leaves the card unanswered and unchanged in the card file: the tool
      says what it accepts and asks again for the same card. It never counts an unrecognised
      answer as right, as wrong, or as a quit.
- [x] AC14 — A card file the tool cannot parse stops the session before any card is shown: it
      prints a message naming the file and the line it stopped at, exits non-zero, offers no card,
      and leaves the file byte-identical. This is the refusal WI-0001's `add` already makes on the
      same file (`ADR-0007`).

## Out of scope

- Adding cards; that is WI-0001. Deleting cards; that is WI-0003.
- Reminding or notifying the person that a review is due. They start the session themselves.
- Any statistics, streaks or history display beyond what the session itself needs to show.
- Choosing between several scheduling algorithms. One rule, applied to every card, per
  `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`.
- Retaining a per-review history of outcomes. The rung and the due date are the whole of a card's
  scheduling state; ADR-0002 states what that costs.
- Undoing an answer once it is given. AC4 writes each outcome to the card file as soon as it is
  given, which is what makes AC9 true; a card answered wrong by a slip of the finger is reviewed
  again tomorrow, and nothing in the record asks for more than that.
- Re-reviewing, in the same session, a card already answered in it. Every outcome sets the next
  due date at least a day ahead (`ADR-0002`), so a card answered in this session is no longer due
  and the session does not come back to it.
- Editing a card's front or back during a review. That is editing, which the stakeholder deferred
  (`EP-001/Q-004`), and no item is filed for it.

## Notes

The criteria above were rewritten from the stakeholder's answers to `EP-001/Q-002` and
`EP-001/Q-003`, which were the two things this item could not state at intake. In their words, on
the rule: *"Just right or wrong — no difficulty scale. Get it right and it comes back later each
time: a day, then three days, then a week, then a month. Get it wrong and it goes back to the
start."* And on what makes a card due: *"A card's due if its date is today or earlier. If I miss a
day it's just still due — nothing lost, nothing punished. A second session the same day should
only show me whatever's still due, not everything again."* The whole model, including the two
things they did not state — what a card at the top of the ladder does, and when a new card is
first due — is recorded with its basis in
`docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`.

AC9 comes from the epic's success measure about killing the tool part-way through a session, and
from the stakeholder naming the loss of progress as one of two things that would make the tool a
failure for them (`EP-001/Q-004`).

**The session-size question is settled, by the stakeholder.** AC2, AC10 and AC11 are written
from their answer to `EP-001/Q-005`, which reconciled two of their own statements — every due card
with no cap (`EP-001/Q-003`) against a review over a couple of minutes being a failure
(`EP-001/Q-004`). They chose no cap plus visibility: *"Don't cap it at some arbitrary number, but
let me quit partway through without losing anything ... I'd rather see the honest number of cards
waiting than have the tool quietly decide which ones I don't get to see today."* AC2 keeps the
literal no-cap reading, AC10 is the honest number, AC11 is the clean quit. The decision, including
the one part the architect inferred — that the session does **not** estimate how long it will take,
because their answer restated only the count and nothing in the record says how fast they read —
is `docs/architecture/adr/ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`.

No criterion on this item bounds how long a session takes, and that is deliberate: their answer
accepts a long sitting after a backlog in exchange for seeing its size. `refine` should not add
one.

### Refined 2026-08-30

`refine` took the two things `answer-questions` left for it — what the person types, and the order
the due cards come in — plus the gaps the Definition of Ready found, and settled all of them
**without putting anything further to the stakeholder**. Every one of them falls inside the
standing delegation they gave in their own words, *"As for how it's actually built — whatever you
think is best"* (`EP-001/Q-004`); re-asking a category they have already answered would tell them
their answer was not heard. Each decision is reversible — a key, a sort key, a message — and each
is recorded with its basis in `artifacts/refinement-qa.md`, marked `[assumed]` rather than as
something they said.

- **The subcommand is `review`, with no arguments**, alongside WI-0001's `add`, as
  `docs/architecture/overview.md` already anticipates. That is AC1.
- **Enter reveals the back side; `y` is right and `n` is wrong; `q` stops the session.** One key
  per action, no word to type and no Enter-after-the-letter promised beyond what a terminal
  line does. That is AC1, AC4 and AC11.
- **End of input stops the session exactly as `q` does**, so a session driven by a pipe ends
  cleanly rather than looking like a crash. That is AC11, and it is also what lets AC9 be tested
  without a terminal.
- **Unrecognised input re-asks for the same card** rather than guessing. That is AC13.
- **Due cards are offered oldest due date first, ties in card-file order.** That is AC12, and it
  is chosen against the stakeholder's own request to be able to check a session against the file
  by hand (`EP-001/Q-005`): a shuffled order would make AC2's and AC10's hand-check impossible to
  perform twice with the same answer. It is the one decision here that was a real choice rather
  than a convention, and the alternative — shuffling, to stop the person learning the sequence
  rather than the cards — is recorded in the Q&A as the option not taken.
- **Nothing due, no cards at all, and no card file are one case**, not three. That is AC8, and it
  makes the first ever `review` on a clean machine decidable, which nothing stated before.
- **An unparsable card file stops the session before the first card.** That is AC14, and it is
  WI-0001's existing refusal on the same file rather than new behaviour (`ADR-0007`).

**Deliberately left unconstrained, by `refine`, under the same deferral:** the exact wording of
every prompt and message, whether the session shows a card's rung or due date alongside its
sides, and what `review` does when given arguments it does not take — which gets a usage message
and a non-zero exit, as every command-line tool does and as WI-0001 left it. None of these would
tell anyone whether this item delivered what was asked for.

**Not added, deliberately:** any bound on how long a session takes or how many cards it holds.
`## Notes` above already says why, and the stakeholder traded that bound for the honest count in
AC10 (`EP-001/Q-005`). Adding one now would contradict their answer rather than sharpen it.

### Accepted at review, 2026-08-30

`review-close` accepted these four gaps rather than sending the item back, and records them here
because a gap that lives only in a report nobody reopens has stopped being on the record. The
reasoning for each is in `artifacts/review.md` `## Accepted gaps`.

- **A session does not notice a concurrent writer.** The session holds the card list in memory and
  rewrites the whole file after each answer (`plan.md` assumption 5), so anything another process
  writes to the card file mid-session is overwritten at the next save. No criterion covers it and
  `ADR-0001` makes the tool single-user; it is the same shape as the gap WI-0001 accepted.
- **WI-0001's AC2, the literal machine restart, is still not executed.** It was an accepted gap at
  that item's close and remains one. What stands in for it here is AC7: a *new process*, the same
  day, reads what an earlier process wrote.
- **Nothing was measured at backlog scale.** One whole-file rewrite and two `fsync` calls per
  answer (`ADR-0008`) means a 200-card session rewrites the file 200 times. No criterion bounds a
  session's length, deliberately — the stakeholder traded that bound for the honest count
  (`EP-001/Q-005`) — and the cost was observed at three-card scale only.
- **What a prompt accepts is stated twice in `recall/cli.py`**: as literal text inside the prompt,
  and derived from the `accepted` tuple by `_named()`. Adding a key would update only the second.
  Accepted because the drift is caught — `test_each_prompt_names_what_it_takes` and
  `test_an_unrecognised_key_re_asks_the_same_card` pin both strings.

Definition of Ready: **all ten criteria pass**, criterion by criterion, with the evidence in this
item's journal entry for the `refine` execution that moved it to `ready`. R4 and R10 were the two
that failed when this execution started — AC1, AC4 and AC11 named actions no one could perform,
and nothing said what an unrecognised key, an empty deck, a missing file, a rung-0 card or two
cards due on the same day did. Nothing here is a Definition of Ready override: no criterion was
waived and the stakeholder was not asked to waive one.
