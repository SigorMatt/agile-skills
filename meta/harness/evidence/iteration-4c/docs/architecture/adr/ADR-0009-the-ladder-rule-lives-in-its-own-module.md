---
title: The ladder rule lives in its own module, between the command layer and the store
version: 1
status: current
updated: 2026-08-30T12:26:00Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0009 — The ladder rule lives in its own module, between the command layer and the store

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0001 built two modules with one seam: `recall/cli.py`, which talks to the person, and
`recall/store.py`, which owns the card file [src: docs/architecture/overview.md]. The overview
written at the time left one thing explicitly undecided and named the item that would decide it:
*"The rule that moves a card along the ladder belongs to neither: it is the scheduling rule
`ADR-0002` fixed, and WI-0002 is the item that puts it in"* [src: docs/architecture/overview.md].
This is that item, so this ADR is the promised decision.

What has to find a home is small and very well specified. `ADR-0002` fixes it: grading is binary,
the ladder is 1, 3, 7 and 30 days, a card answered right moves up one rung, a card answered wrong
returns to the first rung, a card at the top rung stays there, and a card is due when its date is
today or earlier [src: ADR-0002]. `ADR-0007` fixes how it is written down: `rung` is an integer 0
to 4, where 0 means the card has never been answered [src: ADR-0007]. WI-0002's AC5 and AC6 walk
all five rungs, and AC12 fixes the order due cards are offered in — earliest due date first, ties
in card-file order [src: WI-0002 AC5] [src: WI-0002 AC6] [src: WI-0002 AC12].

So the question is not what the rule is. It is where the rule goes, and the answer binds WI-0003
and anything after it, because a rule in the wrong place is re-implemented rather than reused.

## Options considered

- **A — In `recall/cli.py`, inside the review loop.** Cost: nothing to build; the code is a
  handful of lines and it is used in exactly one place today. Risk: the one thing in this product
  that is a *rule* rather than a mechanism becomes indistinguishable from prompt handling, and it
  can only be exercised through a subprocess with a pipe. Every question of the form "what does
  rung 3 do when answered wrong" is then answered by a session test, which is the slowest and
  least direct way to ask it.
- **B — On `store.Card`, as methods.** Cost: also nothing to build, and the data and the rule sit
  together, which reads well. Risk: `store.py`'s stated job is the file — *"Nothing above it knows
  the format"* [src: docs/architecture/overview.md] — and the ladder is not about the file. It
  would also make `store.py` the module that has to know what day it is, which is the one piece of
  ambient state in this tool, and it would put an `ADR-0002` change inside the module whose
  contents are the expensive thing to change [src: ADR-0007].
- **C — A third module, `recall/schedule.py`, holding pure functions over `Card` and a date.**
  Cost: one more file, and a seam that has exactly one caller today; the indirection is real and
  is not free to read. Risk: little, provided it stays pure — a module that grows an opinion about
  input or about the file would be worse than either of the others.

## Decision

**The ladder rule lives in `recall/schedule.py`, as pure functions taking cards and a date and
returning cards and dates** — option C. What this requires of the module WI-0002 is about to
build [src: WI-0002], and what its plan specifies [src: tracker/items/WI-0002/artifacts/plan.md]:
it imports `recall.store` for the `Card` record and nothing else; it opens no file, reads no
environment variable, prints nothing, and does not call `datetime.date.today()` itself. The day
is passed in by the caller.

The last clause is the load-bearing one. A rule that is handed its date is decidable at any rung
and any date without a clock, a card file or a subprocess, which is what makes WI-0002's AC5 and
AC6 — ten transitions across five rungs — checkable directly rather than through ten sessions.
The session, not the rule, is the thing that knows it is today.

**The command layer keeps the conversation and the store keeps the file.** The seam WI-0001
established is unchanged; this adds a third piece beside it rather than moving anything
[src: docs/architecture/overview.md].

**What belongs here:** whether a card is due on a given date, which due cards a session offers and
in what order [src: WI-0002 AC12], and what a card's rung and due date become after a right or a
wrong answer [src: ADR-0002]. **What does not:** anything about prompts, keys, streams or exit
codes, which are the command layer's [src: WI-0002 AC1]; and anything about the file's format,
which is the store's [src: ADR-0007].

## Consequences

Easy: WI-0003 deletes a card without touching this module, and a future change to the ladder —
the one thing in this product a person might plausibly want to tune — is a change to one file with
no I/O in it. The rule can be read in full in one screen, next to the ADR that fixes it.

Hard: three modules for a tool this small is one more than the work strictly needs today, and the
indirection has to be paid for on every read. If WI-0003 and WI-0004 pass through it without ever
using it, that is evidence this was one seam too many.

Reversibility: **cheap, in either direction.** The module has no state, no file and no interface
outside the package; folding it back into `cli.py` or onto `Card` is moving three functions and
their tests, with no data migration and nothing published to anyone. That is why this was decided
here under the stakeholder's standing delegation — *"As for how it's actually built — whatever you
think is best"* [src: EP-001/Q-004] — rather than put to them.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T12:26:00Z | plan | WI-0002 | First version: the ladder rule gets its own module of pure functions, taking the date from its caller; the overview's deferred decision, made. |
