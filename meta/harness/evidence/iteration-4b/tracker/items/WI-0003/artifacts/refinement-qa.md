---
status: recorded
---

# Refinement Q&A — WI-0003

**This file is now a record.** It holds two rounds. Round 1 asked the stakeholder two blocking
questions on 2026-08-30T03:32:14Z; both were answered on 2026-08-30T03:38:18Z and propagated by
`answer-questions`. Round 2, on 2026-08-30T03:46:57Z, rewrote the acceptance criteria in one pass
and **asked nothing new** — everything left was either already theirs and answered, settled by a
standing decision, or a design choice routed to `plan`. Every answer below is tagged `[human]`,
`[assumed]` or `[unresolved]`, verbatim where it is theirs.

The Definition of Ready gap table below is the one round 1 wrote, kept as it was written. Round
2's verdict on each criterion is the table at the end of this file, not this one.

## What was read before asking

- `tracker/items/WI-0003/item.md` — the draft, its four criteria and its `## Notes`, which
  instruct this execution to settle two things with the stakeholder.
- `tracker/items/WI-0003/history.md` — one row. This is a **fresh** draft, not an item sent back
  from a later stage, so the whole story is open rather than one defect.
- `tracker/items/WI-0003/journal.md` — intake's entry, and `answer-questions`' amendment of
  2026-08-30T01:41:39Z which rewrote AC1–AC3 from shapes into the rule and flagged the top-rung
  clause as its own reading.
- `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — every human answer in this
  workspace, plus `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`.
- `docs/product/vision.md` v3, `docs/architecture/adr/ADR-0001`, `ADR-0002` v2,
  `docs/process/using-recall.md` v4.
- `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — the delivered criteria this
  item's change can invalidate.
- `recall/deck.py`, `recall/cli.py`, `recall/store.py` — what exists, so that "visible" and "read
  back" are asked about the tool that is actually there.

## The Definition of Ready gaps that set this agenda

Recorded before the questions were written, per the procedure. `R` numbers are
`spec/dor-dod.md` §1.

| # | Verdict now | Why |
|---|-------------|-----|
| R1 | pass | frontmatter complete; `type`, `epic`, `priority` all set (`validate-workspace`, exit 0) |
| R2 | pass | role ("someone reviewing daily"), capability, and a "so that" outcome |
| R3 | pass | four criteria, labelled `AC1`–`AC4`, all checkboxes |
| R4 | **fail** | no criterion names an invocation. AC1 and AC2 describe arithmetic with no way to observe it; AC3 says "written down … in enough detail" without naming the document or the check; AC4 turns on the word "visible", which nothing in the tool currently makes true — `recall list` prints `question \| answer` and a sitting prints nothing after a grade |
| R5 | pass | three exclusions, one of which (no new interface onto the schedule) a reader would otherwise assume was included |
| R6 | **fail by this execution's own doing** | `Q-001` and `Q-002` are open and blocking. That is the suspension, not a defect |
| R7 | pass | `depends-on: WI-0002`, which is `done` |
| R8 | **fail** | this file, and it says `agenda` |
| R9 | pass | one coherent change: the scheduling arithmetic in `recall/deck.py`'s `record_answer`, plus the documentation AC3 requires. Not two items |
| R10 | **fail** | the combinations this item introduces are not all visible: right at the top rung (that is `Q-001`), wrong at each rung, a right answer on a card that is **overdue** (WI-0002 AC13) and whether its next date counts from today or from the date it missed, and a stored ladder position outside the ladder in a hand-edited deck |

## Round 1 — asked

Both questions were filed as one ask, on 2026-08-30T03:32:14Z, and both are blocking. The item is
suspended at `awaiting-answer` with `resume-to: draft`.

### Q1 — `questions/Q-001.md`: what happens above the longest gap?

> Once a card has reached the longest gap — a month — and you keep getting it right, should it
> keep coming back every month for ever, or should the gap carry on growing?

Options put: **A** stop at a month; **B** keep doubling with no ceiling; **C** keep growing to a
ceiling they name. Our preference, stated last and marked as ours, was A.

Why the stakeholder and not us: `ADR-0002` already contains an answer — the ladder tops out —
and records it as `answer-questions`' reading rather than as the stakeholder's decision, with an
instruction to this execution to confirm it. `docs/product/vision.md` §"What is still open"
carries the same instruction. The cost of the reading falls entirely on them: a card known cold
returning every month for ever is their evening.

**Answer:** given 2026-08-30T03:38:18Z, verbatim — **A**:

> Stops at a month — option A. The whole point was simple, and I don't want to be doing math to
> figure out when a card's coming back. If my deck gets huge later I might change my mind, but
> not now.

Propagated by `answer-questions` into `ADR-0002` v3 (§5 and its "Decided by" line are now the
stakeholder's decision rather than the ADR's reading; the monthly-floor consequence is recorded
as accepted, with what would make them revisit it), `docs/product/vision.md` v4, and
`item.md`'s `## Notes`. **AC1 needs no amendment**: its closing clause already says the gap stays
at 30 days on every correct answer after that.

### Q2 — `questions/Q-002.md`: does a sitting tell you when you will next see the card?

> When you answer a card in a sitting, should the tool tell you when you will next see that
> card?

Options put: **A** say nothing; **B** one line after each answer; **C** silent sitting, and
`recall list` gains the date. Our preference, stated last and marked as ours, was B.

Why the stakeholder and not `plan`: this is not the wording of a message, which `ADR-0001`
reserves to `plan`. It is whether a fact is shown at all, and it decides whether the only
feature this item delivers is perceptible to the person using the tool. AC4 as intake wrote it
says the new date must be "visible", and the item's `## Notes` hand the meaning of that word to
this execution.

**Answer:** given 2026-08-30T03:38:18Z, verbatim — **B**:

> Option B — show the next date after each answer. I want to actually see it's working, and one
> line isn't going to slow me down.

Propagated by `answer-questions` into `ADR-0007` (new: a sitting names each card's next-review
date as the answer is recorded, one line, `recall list` unchanged, wording left to `plan`),
`docs/product/vision.md` v4, and `item.md`'s `## Notes`. **AC4 is what changes**: *visible* means
the printed line, and `refine` writes that into the criterion together with the invocation R4
still wants.

## Decided here rather than asked, with the basis

Recorded in round 1, before the answers arrived. All four still stand and all four are now in
the criteria or in `item.md`'s `## Notes`; round 2 changed none of them and added the two below
this list.

- `[assumed]` **The stakeholder's four intervals are 1, 3, 7 and 30 days, and a right answer
  measures the gap from the day of the sitting, not from the day the card was due.** Not asked
  again: `EP-001/Q-003` gave the rungs and `ADR-0002` §4 fixes the origin. Where this bites is a
  card reviewed late — WI-0002 AC13 presents an overdue card, and its next date must be counted
  from today. That is a criterion to write, not a question to ask.
- `[assumed]` **A wrong answer resets the ladder position as well as the date.** `ADR-0002` §6
  has two clauses and the placeholder in `recall/deck.py` satisfies only the second: it moves the
  card to tomorrow and leaves `rung` untouched. WI-0002's review recorded this in that item's
  `## Notes` as work WI-0003 inherits. Their own words are *"If I get it wrong it goes back to
  the start"*, which is the reset; no ambiguity to put to them.
- `[assumed]` **The deck file is a legitimate place to observe a criterion from.** `ADR-0004`
  fixes the format, `docs/process/using-recall.md` tells the person it is ordinary JSON they may
  read, and WI-0002's criteria already set up decks by writing it directly. So AC1–AC3 can be
  made decidable without waiting on Q2 — Q2 decides what the *person* sees, not what a verifier
  may inspect.
- **Routed to `plan`, not to the stakeholder:** what the tool does with a stored ladder position
  outside the ladder in a hand-edited deck — clamp it, or refuse the deck as unreadable the way
  `store.py` already refuses an unrecognised `grade` (`ADR-0006` §3). The answer would be the
  same whoever the stakeholder was. It is recorded in `item.md` `## Notes` for R10.

## Round 2 — asked nothing, decided the rest

2026-08-30T03:46:57Z. The two blocking questions were answered and propagated, so the only thing
left between this item and Ready was the criteria themselves. Each gap was put through the
skill's own routing test — product stake, already answered, standing deferral, or
implementation-only — and **none of them reached the stakeholder**. Filing a question to confirm
what they had just told us would have been the failure a real run recorded as *"technical calls
being routed to me as questions"*.

- `[human]` **The ladder stops at a month.** Verbatim in Q1 above. Written into AC1 as the fifth
  sitting: after four right answers the gap is 30 days, and the fifth right answer is 30 days
  again. Demonstrating the hold rather than asserting it is why AC1 runs five sittings and not
  four.
- `[human]` **A sitting says when the card is next due, one line per card.** Verbatim in Q2
  above. Written into AC4, and the old AC4's word *visible* is retired.
- `[assumed]` **AC4's date appears as `YYYY-MM-DD`.** This is `refine`'s decision, not theirs and
  not `plan`'s, and it is the only place round 2 constrained something `ADR-0001` §5 would
  otherwise reserve to `plan`. The reason is decidability: R4 fails on a criterion nobody can
  grep, and *"the tool prints the date somehow"* is not observable. It is the form `ADR-0004` §2
  already uses in the deck file. Everything else about the line is `plan`'s — *"next in 7 days
  (2026-09-06)"* satisfies AC4. Recorded in `item.md` `## Notes` so `plan` cannot miss it.
- `[assumed]` **The criteria compress the calendar by resetting `due`, never by writing `rung`.**
  A hundred-day ladder cannot be walked in a test otherwise. It is faithful because `ADR-0002` §4
  counts a gap from the day of the sitting, so a card reviewed on its due date and one reviewed
  after a wait are the same case — which is also what AC3 checks directly. The side benefit is
  that no criterion depends on how a ladder position is stored, which keeps `plan`'s hands free.
- **Routed to `plan`, second one:** **how a ladder position is encoded in `rung`.** `ADR-0004` §2
  calls it an index into the ladder and `recall add` writes `0`; `ADR-0002` §3 says a new card
  starts *below* the ladder while §4 says a right answer moves it up one and then uses that
  rung's number. The two readings differ by one in what `0` means and produce identical dates.
  Noticed while writing AC1; not the stakeholder's, because the observable behaviour is the same
  either way. Recorded in `item.md` `## Notes` for R10.
- **Not re-asked, and worth saying so:** whether a wrong answer resets the ladder position (their
  *"it goes back to the start"* settles it, and AC2(b) now checks it); whether an overdue card's
  gap counts from today (`ADR-0002` §4, and AC3 now checks it); whether a sitting may be long
  (`WI-0002/Q-001`, already theirs); whether `recall list` changes (`Q-002` option C, which they
  did not choose, now in `## Out of scope`).

## Cross-answer check, round 2

`refine` recorded no new answer from the stakeholder in this round, so there is no new answer to
check against their prior ones. The two answers this item does carry were consumed and checked by
`answer-questions` on 2026-08-30T03:38:18Z; both checks are in `questions/Q-001.md` and
`questions/Q-002.md` and both concluded compatible, against `EP-001/Q-001`, `Q-002`, `Q-003`,
`WI-0002/Q-001` and `WI-0002/Q-002`. Round 2 re-read all five while writing the criteria and
found nothing the criteria contradict:

- The criteria cap no sitting and bound no number of cards, so `WI-0002/Q-001` stands.
- AC1 starts from `recall add` and reviews on the same day, which is `WI-0002/Q-002`.
- AC4 adds one line per card and nothing that accumulates, which is `EP-001/Q-001`'s *"nothing
  fancier than that"* and the epic's exclusion of statistics.
- Nothing in `docs/` sourced to one of their answers was rewritten by this execution.

## Definition of Ready — round 2 verdict

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` exit 0; `type`, `epic`, `priority` set |
| R2 | pass | `## Story` names the role ("someone reviewing daily"), the capability, and the outcome |
| R3 | pass | six criteria, `AC1`–`AC6`, each a checkbox |
| R4 | **pass, was fail** | every criterion names `recall add` or `recall review` and the deck file, or a named document (`AC5`), or named criteria to read (`AC6`). No unmeasurable adjective survives; the one adjective-shaped phrase left, AC5's "well enough to work a date out by hand", is discharged by the five facts and the worked example it enumerates |
| R5 | pass | `## Out of scope` names six, including `recall list` gaining nothing — the thing a reader of `Q-002` would most reasonably assume was included |
| R6 | pass | both questions on this item are `answered`; none open |
| R7 | pass | `depends-on: WI-0002`, which is `done` |
| R8 | **pass, was fail** | this file, `status: recorded`, both rounds |
| R9 | pass | one coherent change: the arithmetic in `recall/deck.py`'s `record_answer`, one line of output in `cmd_review`, and the documentation AC5 requires |
| R10 | **pass, was fail** | right at the top rung → AC1's fifth sitting; wrong at the bottom rung → AC2(a); wrong at the top rung, and the reset it implies → AC2(b); right on an overdue card → AC3; wrong on an overdue card → AC3's last sentence; the printed line on both answers and at two gaps → AC4; a stored ladder position outside the ladder → `## Notes`, routed to `plan`; the `rung` encoding → `## Notes`, routed to `plan`. `recall list` and the end-of-sitting summary → `## Out of scope` |

## What is still open after this item is Ready

Nothing with the stakeholder. Two design questions are deliberately unconstrained and named in
`item.md`'s `## Notes` for `plan`: what an out-of-range stored ladder position does, and how a
ladder position is encoded. Neither can change the verdict on any criterion above.
