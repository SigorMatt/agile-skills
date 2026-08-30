---
title: A review session offers every due card, states how many there are, and can be quit without loss
version: 1
status: current
updated: 2026-08-30T11:24:23Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0003 — A review session offers every due card, states how many there are, and can be quit without loss

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** answer-questions (architect), for EP-001, on the stakeholder's answer to
  `EP-001/Q-005`
- **Supersedes:** —

## Context

`ADR-0002` fixed the schedule — when each card falls due — and deliberately left one thing open:
which of the due cards a session actually shows [src: ADR-0002]. It could not settle that,
because two of the stakeholder's own statements pulled against each other.

They asked for no cap: *"And no cap on how many come up at once — whatever's due, all of it."*
[src: EP-001/Q-003] And they named a session length as a failure of the product: *"Two things
would make this a failure for me: losing my progress, or a review taking more than a couple
minutes to get through."* [src: EP-001/Q-004]

On a small deck both hold. They stop holding together once a backlog exists, and their own rule
that a missed day costs nothing makes a backlog likely [src: EP-001/Q-003]: after a week away,
a session that shows everything due runs well past a couple of minutes. `answer-questions`
escalated the conflict to its author as `EP-001/Q-005` rather than deciding which of their
sentences lost [src: EP-001/Q-005].

## Options considered

- **A — No cap; show every due card, and say nothing about length.** Cost: none in code. Risk:
  a hundred-card backlog is a single long sitting, and the person meets it with no warning — the
  failure mode they named themselves [src: EP-001/Q-004].
- **B — Cap the session** at some number of cards, oldest due first, and report how many remain.
  Cost: a number nobody has a basis for, plus the reporting. Risk: the tool shows fewer cards
  than are due, so "the session offers exactly what is due" stops being true, and the tool is
  choosing on the person's behalf which cards they do not get to see today.
- **C — No cap, but the size is stated up front and quitting is a supported exit.** Cost: a count
  before the first card, and a quit path that persists what has been answered so far. Risk:
  neither of their two sentences is honoured literally — a full review of a large backlog still
  takes as long as it takes.

The stakeholder was given all three, with no recommendation, and chose **C**:

> C. Don't cap it at some arbitrary number, but let me quit partway through without losing
> anything — whatever I already answered keeps its new schedule, and the rest is still due
> tomorrow. I'd rather see the honest number of cards waiting than have the tool quietly decide
> which ones I don't get to see today.

[src: EP-001/Q-005]

## Decision

**A session offers every card that is due, with no cap.** The set a session offers is exactly the
set whose due date is today or earlier under `ADR-0002`, however large that set is
[src: ADR-0002] [src: EP-001/Q-003] [src: EP-001/Q-005]. No card that is due is withheld, deferred
or hidden from the person by the tool.

**A session states how many cards are due before it shows the first one.** The number is the
count of the cards it is about to offer, so the person meets a backlog knowing its size rather
than discovering it card by card [src: EP-001/Q-005].

**Quitting part-way is a supported exit, not an interruption.** The session offers a way to stop
at any point, and stopping is an ordinary outcome rather than a crash or a kill: every card
already answered keeps the rung and the due date that answer gave it, and every card not reached
is unchanged and still due [src: EP-001/Q-005] [src: WI-0002].

**The session does not estimate how long it will take.** This is the architect's inference, not a
sentence the stakeholder wrote: option C as put to them offered "how many are due and roughly how
long that is", and their answer restated only the count — *"the honest number of cards
waiting"* [src: EP-001/Q-005]. Nothing in the record establishes how long this person takes per
card, `ADR-0002` stores nothing from which it could be derived [src: ADR-0002], and a duration
printed from a guessed per-card constant would be a number the tool made up. If they later want
one, it needs a timing to be recorded first, which is a change to what is stored.

**The couple-of-minutes statement is a design pressure, not an acceptance criterion.** After this
answer no criterion on any item bounds how long a session takes, and none should be written:
their answer accepts that a large backlog is a long sitting and asks for the size to be visible
instead. It remains the right thing to keep sessions short by other means — a small daily habit
keeps the backlog small — but the tool does not enforce it [src: EP-001/Q-004]
[src: EP-001/Q-005].

## Consequences

Easy: the schedule and the session agree exactly, so WI-0002's criterion that a reader can check
the offered set against the stored file by hand stays decidable — there is no cap to reason about
[src: WI-0002]. The count is derivable from the same pass that selects the due cards, so it costs
nothing extra to produce.

Hard: writing must happen per answered card rather than once at the end of the session, because a
quit at any point has to leave the answers already given on disk. That constrains how WI-0002 is
implemented — a session cannot hold its results in memory and write them on a clean exit — and it
is the mechanism behind the first of the two failure modes the stakeholder named, losing progress
[src: EP-001/Q-004] [src: WI-0002].

Also hard: nothing protects the person from a very large session except their own habit. The tool
will tell them 240 cards are due and then offer all 240.

Reversibility: **cheap.** Introducing a cap later changes which due cards one session shows, not
when any card falls due, so no stored data changes shape and no history is migrated — unlike the
scheduling state in `ADR-0002`, which is not cheap to change [src: ADR-0002]. A cap is a
superseding ADR and an amended criterion on WI-0002, and it would need the stakeholder's
authorisation because this decision is theirs, not ours [src: EP-001/Q-005].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:24:23Z | answer-questions | EP-001 | First version: records the stakeholder's answer to Q-005 — no cap, the count stated up front, quitting a supported exit — and the one derived decision, that the session does not estimate its own duration. |
