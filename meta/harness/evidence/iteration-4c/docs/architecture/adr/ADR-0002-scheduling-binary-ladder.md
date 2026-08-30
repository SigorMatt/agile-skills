---
title: Scheduling — binary grading on a fixed 1/3/7/30-day ladder, due by calendar date
version: 1
status: current
updated: 2026-08-30T11:13:36Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0002 — Scheduling: binary grading on a fixed 1/3/7/30-day ladder, due by calendar date

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** answer-questions (architect), for EP-001, on the stakeholder's answers to
  `EP-001/Q-002` and `EP-001/Q-003`
- **Supersedes:** —

## Context

"Simple spaced repetition" was the stakeholder's whole statement of the behaviour at the heart of
the product [src: EP-001]. It decides when each card comes back, it is what WI-0002's criteria
are written against, and the scheduling data it writes is what has to persist from the first day
[src: WI-0002]. `intake` escalated both halves of it — the rule itself as `EP-001/Q-002`, and what
makes a card due on a given day as `EP-001/Q-003` — rather than assume either.

The stakeholder answered the rule, in their own words: *"Just right or wrong — no difficulty
scale. Get it right and it comes back later each time: a day, then three days, then a week, then a
month. Get it wrong and it goes back to the start."* [src: EP-001/Q-002]

And the due-date question: *"A card's due if its date is today or earlier. If I miss a day it's
just still due — nothing lost, nothing punished. A second session the same day should only show me
whatever's still due, not everything again. And no cap on how many come up at once — whatever's
due, all of it."* [src: EP-001/Q-003]

Two things those two sentences do not settle, which the code cannot avoid settling: what happens
to a card that is already at a month, and when a brand-new card first becomes due. Both are
recorded as decisions below rather than left to the implementation to invent.

## Options considered

- **A — A fixed ladder of intervals, graded right/wrong.** A card sits on a rung; right moves it
  up one rung, wrong returns it to the first. Cost: one integer of state per card. Risk: it
  treats "just barely right" and "instant" identically — which is what the stakeholder asked
  for, having been offered the alternative [src: EP-001/Q-002].
- **B — SM-2, the Anki-style algorithm**: a per-card interval and ease, driven by a multi-point
  grade. Cost: floating-point state to persist and a grading scale to design. Risk: rejected by
  the stakeholder in the same sentence — *"no difficulty scale"* [src: EP-001/Q-002].
- **C — Two intervals only** (right → a week, wrong → tomorrow). Cost: the least of the three.
  Risk: it is not what was asked for; the stakeholder named four increasing intervals.

On what a card at the top of the ladder does, two further options were weighed: **stay at the top
rung, repeating the month interval**, or **keep growing** (doubling, or unbounded). On when a new
card is first due: **due on the day it is added**, or **due the day after**.

## Decision

**Grading is binary.** A reviewed card is marked right or wrong. There is no difficulty scale and
no third outcome [src: EP-001/Q-002].

**The ladder is fixed: 1, 3, 7, 30 days.** A card answered right moves up one rung and its next
due date is set that many days after the day it was reviewed. A card answered wrong returns to
the first rung, so it is due one day after the day it was reviewed [src: EP-001/Q-002]. The
option the stakeholder answered against stated that behaviour as *"it drops back to rung 1 and
you see it tomorrow"* [src: EP-001/Q-002].

**A card at the top rung stays there.** Answering a card right when it is already on the 30-day
rung schedules it 30 days out again; the ladder does not grow past a month. Basis: the
stakeholder's list of intervals ends at a month, and the option text they answered against
described the ladder as *"then stays at 30"* [src: EP-001/Q-002]. This is the architect's
inference from their answer, not a sentence they wrote.

**Due is a calendar-date comparison.** Each card carries a due date. It is due when that date is
today or earlier, in the machine's local calendar date [src: EP-001/Q-003]. Missed days
accumulate with no penalty and no expiry: a card due three days ago is simply still due
[src: EP-001/Q-003]. Nothing is discarded, rescheduled or escalated for having been missed.

**A new card is due on the day it is added.** Basis: WI-0001 already required that a newly added
card is recorded as due for review [src: WI-0001], and a due date of the day it was added is what
makes that true under the comparison above. This is the architect's inference, not a sentence the
stakeholder wrote.

**A second session on the same day re-offers nothing that was answered in the first.** This falls
out of the rules above rather than needing a rule of its own: every outcome of a review sets the
card's next due date at least one day ahead, so no card answered today is due today
[src: EP-001/Q-003].

**No cap on session size** — a session offers every due card [src: EP-001/Q-003]. The stakeholder
also stated that a review taking more than a couple of minutes to get through is a failure of the
product [src: EP-001/Q-004]. Those two statements are in tension once a backlog is large, they
are both theirs, and the tension is open with them as `EP-001/Q-005` [src: EP-001/Q-005]. This
ADR does not resolve it: what is decided here is the schedule, and a cap or a split session, if
one is ever introduced, changes which due cards a session shows, not when a card falls due.

## Consequences

Easy: a card's whole scheduling state is a rung and a date, both readable by eye in the stored
file, so WI-0002's criterion that a reader can check the due set by hand is satisfiable
[src: WI-0002]. Every next-due date is predictable from the two of them without running the tool.

Hard: the schedule cannot adapt to how hard a particular card is for this person, because nothing
distinguishing "barely right" from "instant" is recorded. Nothing is stored that would let a
later, adaptive algorithm reconstruct history: the outcome of a review is not retained beyond its
effect on the rung. A project that later wants SM-2 starts collecting the data it needs from the
day it switches, not before.

Reversibility: **the rule is cheap to reverse; the stored shape is not.** Changing the intervals,
or the top-rung behaviour, is a change to one function and a re-derivation of due dates. Moving to
a graded algorithm is not: it needs per-card state this decision does not store, so it is a data
migration on a file holding real study history, which is exactly the durability promise the epic
rests on [src: EP-001]. Recording the outcome of each review — even unused — would buy that
option back cheaply, and is deliberately not being done now because the stakeholder asked for the
simple thing.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:13:36Z | answer-questions | EP-001 | First version: records the stakeholder's answers to Q-002 and Q-003, and the two derived decisions (top-rung behaviour, when a new card is first due). |
