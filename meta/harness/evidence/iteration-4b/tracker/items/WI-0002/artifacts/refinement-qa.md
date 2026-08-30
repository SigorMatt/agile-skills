---
status: recorded
---

# Refinement Q&A — WI-0002

## Why this file said `agenda`, and why it now says `recorded`

The stakeholder on this project answers asynchronously, in files, and is not present in the
session that runs a skill (`SIMULATION-NOTICE.md`). This refinement needed two things from them
that nobody else may decide, so it filed `WI-0002/Q-001` and `WI-0002/Q-002`, suspended the item
at `awaiting-answer` with `resume-to: draft`, and stopped. While that was true this file said
`agenda`: the questions were written down and the conversation had not happened.

Both answers have since arrived and `answer-questions` consumed them on
2026-08-30T02:28:46Z. They are written in verbatim under the two entries below, tagged
`[human]`, and this field is now `recorded`, which is what Definition of Ready R8 reads
(`spec/workspace-layout.md` §1.3). Nothing else in this file was rewritten: the reasoning below
is what `refine` recorded at the time, and it stands as written whether or not the answers agreed
with it.

Everything already tagged `[human]` below is the stakeholder's own words, quoted from the
questions `intake` filed on the epic and they answered — `EP-001/Q-001`, `EP-001/Q-002`,
`EP-001/Q-003`. Everything tagged `[assumed]` is this skill's own decision, and says whose
authority it rests on.

---

## Round 1 — the two questions put to the stakeholder

### Q&A 1 — Does a review sitting cap how many cards it presents? (`WI-0002/Q-001`, DoR R4, R10)

**Status: answered.** Filed as `WI-0002/Q-001`, blocking; answered by the stakeholder and
consumed by `answer-questions` on 2026-08-30T02:28:46Z.

The stakeholder volunteered one of the two failure conditions for this whole tool and it lands
on this item:

> [human] `EP-001/Q-001` — "don't lose my progress — that's the one thing that would make this a
> failure, along with a review session that drags on more than a couple minutes."

That sentence is not a criterion and this skill will not make it one by inventing a number.
Nothing has fixed whether a sitting bounds how many cards it presents at all, and the whole
point of a spaced-repetition tool is that the daily load is not under the person's control — a
week away and the due pile is whatever it is. Intake left this here explicitly, `ADR-0002`
carries it, and `docs/product/vision.md` "What is still open" names it. It is theirs.

**Answer** `[human]`, from `WI-0002/Q-001`, verbatim:

> No limit — A. Show me everything that's due. If it's a big pile after a week away I'll just
> stop partway, that's fine by me.

They read the trade-off in the question — that option A leaves the couple-of-minutes sentence as
a constraint we design towards rather than a criterion — and chose it anyway, supplying their own
reconciliation of the two statements in the same breath. So the sitting is uncapped, that became
**AC11**, and the couple-of-minutes constraint is recorded in `item.md` `## Notes` as an
unbounded design concern, exactly as this entry said it would be if the answer was not a cap.

### Q&A 2 — Is a card added today due in today's sitting? (`WI-0002/Q-002`, DoR R4, R10)

**Status: answered.** Filed as `WI-0002/Q-002`, blocking; answered by the stakeholder and
consumed by `answer-questions` on 2026-08-30T02:28:46Z.

Intake assumed yes so that a new deck is reviewable the day it is built. `ADR-0002` §3 carries
the assumption forward and still labels it an assumption, and says in terms that it is
*"WI-0002's to confirm at refinement"*. The delivered `recall add` already writes `due` = the day
the card was added (`recall/deck.py`, `new_card`), so the storage has taken the assumption's side
— which is a reason to confirm it now rather than later, not a reason to stop asking.

**Answer** `[human]`, from `WI-0002/Q-002`, verbatim:

> Today — A. If I've just added a card I want to try recalling it right away, not wait till
> tomorrow.

Intake's assumption is confirmed by the person who was assumed about. `ADR-0002` §3 no longer
carries it as an open assumption, and it became **AC12**. Nothing delivered has to change:
`recall add` already writes `due` = the day the card was added.

---

## Round 1 — the gaps that were closed without asking, and how

Each of these is a Definition of Ready gap this refinement found. None went to the stakeholder,
and the reason each did not is recorded here so a reader can disagree with it.

### 1. What does a person type to run a sitting? (R4) — already answered

**Answer** `[human]`, from `EP-001/Q-002`, verbatim:

> A command-line tool — I'm doing this at a terminal once a day, so option A works fine.

Recorded as `ADR-0001`, which fixes the surface far enough to write criteria: one executable
`recall`, `review` as a subcommand, and — §4 — `review` interactive on standard input,
*"so it can be driven by a here-document in a test"*. Every criterion on this item is now written
as a `recall review` invocation with its input and its output named. Re-asking would be asking a
question they have already answered.

### 2. How many answers does a person choose between? (R4) — already answered

**Answer** `[human]`, from `EP-001/Q-003`, verbatim:

> Just right or wrong, no rating scale. If I get it right it comes back later each time — a day,
> then three, then a week, then a month or so. If I get it wrong it goes back to the start.

Settled as `ADR-0002` §1 and already carried into this item's AC by `answer-questions`. AC3 now
says the run accepts exactly two responses and names the consequence of anything else.

### 3. Does "due" mean *due today*, or *due today or earlier*? (R4) `[assumed]`

Nobody said. A card whose date has passed must still come back — the alternative is that missing
a day silently drops a card out of the schedule for ever, which is the stakeholder's own stated
failure condition (*"don't lose my progress"*, `EP-001/Q-001`) applied to the schedule rather
than to the file. There is no version of this tool in which the other reading is what they meant.

**Decided here:** due means the card's stored next-review date is **today or earlier**. Recorded
in `item.md` `## Notes` and in the preamble to the criteria, and named in `Q-001`'s context so
the stakeholder can object to it while they are answering the question it bears on.

### 4. What happens to answers already given when a sitting ends early? (R10) `[assumed]`

A person closes the terminal, or standard input runs out, half-way through. Two behaviours are
possible: the answers already given stick, or the sitting is discarded as incomplete.

**Decided here:** they stick, and AC9 requires it. This is not a guess — it is their own
category answer applied directly: *"don't lose my progress — that's the one thing that would
make this a failure"* (`EP-001/Q-001`). An answer given is progress; discarding it is the failure
they named. Filing a question whose option B contradicts a sentence they have already written
would be asking them to repeat themselves.

### 5. In what order are due cards presented? (R10) — routed to `plan`

Oldest-due first, insertion order, or shuffled. The answer would be the same whoever the
stakeholder was, nothing in the record bears on it, and no criterion needs it: AC1 is written
over "each due card", not over a sequence. `refine`'s step 3 routes a decision of that shape to
`plan`, not to a person. Recorded in `item.md` `## Notes` as deliberately unconstrained, with
this skill named as who left it so, which is what R10 asks for.

### 6. The exact words of the prompts, the two grade responses, and the exit code of an early
end (R4, R10) — routed to `plan`

`ADR-0001` reserves *"the exact wording of any message"* to `plan`. The criteria are therefore
written against what must be observable — a question side before an answer side, exactly two
recognised responses, no traceback — and never against a sentence. Where a criterion needs to
name the two responses, it names them by reference to the documentation the tool ships, which is
the same device WI-0001 AC7(a) used.

### 7. What a sitting does when the deck file exists but cannot be read (R10) — a criterion, and
a boundary against `BUG-0001`

WI-0001 AC8 fixed this for `add` and `list`; `review` is a third subcommand and inherits nothing
automatically, so AC7 states it here. The boundary matters: AC7 covers a deck whose **content**
is not a deck. A filesystem error that is not a content problem — a permission denial, a
directory where the file should be — is `BUG-0001`, which is open against the existing
subcommands. `item.md` `## Notes` says so, so that `verify` does not read one as evidence about
the other.

---

## Round 2 — the Definition of Ready walk, after the answers came back

Nothing was asked of the stakeholder in this round. Both round-1 questions were answered and
consumed, and the walk through `spec/dor-dod.md` §1 found nothing further that is theirs: what
remains is either decidable now, or `plan`'s. Filing a question to say "we have no questions"
would spend their attention on nothing.

Three things were decided here, all `[assumed]`, all under authority already on the record.

### 8. An overdue card was a reading with no criterion behind it (R4, R10) `[assumed]`

Round 1 decided that "due" means the card's stored date is **today or earlier** (entry 3 above),
wrote it into the preamble to the criteria and into `## Notes`, and showed it to the stakeholder
in `WI-0002/Q-001`'s `## Context`. What it did not do is leave a criterion that exercises it:
AC4 tested a card dated *today* against one dated seven days *ahead*, and no criterion anywhere
put a card in the past. A reading stated only in prose is a reading `verify` cannot check and
`implement` can miss without failing anything.

**Decided here:** **AC13** added — one card dated seven days before today is presented, and the
run exits 0. No new decision; the round-1 decision made observable. Authority: the same sentence
it always rested on, *"don't lose my progress"* (`EP-001/Q-001`), applied to the schedule.

### 9. "Says so plainly" is an adjective with no threshold (R4) `[assumed]`

AC5 said the run *"says so plainly"* when nothing is due, and AC6 said it *"says there is nothing
to review"*. Both then named a real observation, so neither was empty — but "plainly" is exactly
the word `refine`'s own procedure flags as the place a disagreement will later happen, and "a
line saying nothing is due" asks a verifier to judge whether a given sentence means that.

**Decided here:** both criteria now name the message **by reference to the documentation the tool
ships**, which is the device WI-0001 AC7(a) already used for the deck path, and which
`ADR-0001` requires because it reserves message wording to `plan`. A verifier reads the
documentation and greps stdout; there is nothing left to judge. The consequence for `plan` is
that the message must be documented, and that is recorded in `## Notes`.

**And a second decision inside it, stated separately because it constrains `plan`:** AC6 now
requires the *same* message as AC5. `ADR-0004` §6 makes an absent deck an empty deck rather than
a fault, so "the deck is missing" and "everything is scheduled for later" are the same situation
to the person at the terminal. Two different messages would invent a distinction the record
denies. Authority: `ADR-0004` §6. If `plan` disagrees it should say so in an ADR rather than in
code.

### 10. The numbers in the criteria are witnesses, not requirements (R4) `[assumed]`

AC11 says twenty-five cards; AC1 says three; AC4 says seven days. The stakeholder gave none of
these. They are sizes chosen so that the observation means something — twenty-five sits
comfortably above any batch size an implementation might pick by accident, which is what makes
"presents all of them" evidence that nothing caps the sitting.

**Decided here:** recorded in `## Notes` as `refine`'s, so that nobody later reads twenty-five as
a limit the stakeholder asked for, and so that `verify` knows it may use a different number if it
has a reason to. The requirement is the absence of a cap.

---

## What is still open after this round

**Nothing with the stakeholder.** Both filed questions are answered and consumed, and round 2
found nothing further to ask.

Refinement wrote the ten original criteria so that they held whichever way the stakeholder
answered, and named in `## Notes` exactly what each answer would add. That held: the two answers
added **AC11** and **AC12** and amended nothing. AC1–AC10 are as `refine` wrote them.

What remains open is not for the stakeholder. `item.md` `## Notes` routes four design decisions
to `plan` — the order due cards are presented in, the wording of the prompts and the two grade
responses, the exit code of a sitting that ends early, and the placeholder forward step that
makes AC8 true before WI-0003 exists. Round 2 adds a fifth: the nothing-due message AC5 and AC6
now name must be documented, because a criterion that points at documentation fails if the
documentation is not written.

AC11 adds nothing to that list, but it does raise the stakes on the placeholder forward step: a
sitting may now present an arbitrarily large number of cards, so whatever `plan` chooses has to
hold for a pile, not just for three.
