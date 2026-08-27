---
title: An operating-system error on the dataset becomes a refusal in store.py, not in the CLI
version: 1
status: current
updated: 2026-08-27T01:48:49Z
updated-by: plan
updated-for: BUG-0002
---

# ADR-0008 — An operating-system error on the dataset becomes a refusal in `store.py`, not in the CLI

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0002
- **Supersedes:** —

## Context

This tool has one way of failing on purpose: a layer below the command line raises
`ExpensesError`, and `cli.main` turns it into a line on stderr and exit status 2
[src: expenses/cli.py; docs/architecture/overview.md]. Every refusal anybody specified is a
refusal of the *user's input* — an amount that is not a number, a name nobody added, a position
that does not exist.

The environment refusing is a different thing, and nobody decided how it is handled. It was
settled twice, by accident and in opposite directions. `store.load` catches `OSError` and raises
`ExpensesError("cannot read ...")`; `store.save` catches nothing, so a store the user cannot write
to produces an eleven-line traceback and exit 1 [src: expenses/store.py; BUG-0002].
Neither branch was asked for by a plan or an ADR — the asymmetry is the finding recorded in
BUG-0002 [src: tracker/items/BUG-0002/journal.md].

So the question this ADR answers is not "should the traceback go away" — the bug's criteria
already say it must [src: BUG-0002 AC1]. It is **where in the layering an operating-system error
stops being an exception and becomes a refusal**, because that boundary is what the next writer
of a store function, and WI-0003's importer, will follow or break.

## Options considered

- **A — at the store boundary: every function in `expenses/store.py` that touches the file turns
  `OSError` into `ExpensesError` naming the dataset path.** `load` already does this; `save` is
  changed to match. Cost: each such function carries a wrapper, so a new one that forgets it
  reintroduces the bug — the same failure mode that produced this item. Risk: an `OSError` raised
  for a reason that is genuinely a programming mistake is presented to the user as a refusal,
  losing the traceback that would have identified it.
- **B — at the command line: `cli.main` catches `OSError` alongside `ExpensesError`.** One place,
  and it cannot be forgotten. Cost: `main` does not know which path was being touched, so the
  message cannot name the dataset — and naming the path is what makes the message useful and is
  required by the criteria [src: BUG-0002 AC1]. It also catches `OSError` from anywhere in the
  process, including from printing to a closed pipe and from any future code that has nothing to
  do with the dataset, which turns unrelated crashes into confident-looking refusals. Risk: it
  contradicts the rule that the layers below raise one type and the CLI translates it
  [src: docs/architecture/overview.md], by making the CLI the place that knows about `OSError`.
- **C — at each handler: `person_add`, `expense_add`, `person_delete` and `expense_delete` each
  wrap their `store.save` call.** Cost: four wrappers for one condition, in the layer that is
  supposed to do no error classification, and they will drift. Risk: `expense delete` and
  `person delete` are outside this item's criteria [src: BUG-0002 AC1; BUG-0002 AC2], so
  two of the four would be written with nothing checking them.
- **D — leave `save` alone and let the traceback stand**, on the grounds that an unwritable store
  is the operator's problem. Cost: none in code. Risk: it is the behaviour the stakeholder's own
  tool already contradicts on the read path, and a traceback reads as "this program is broken"
  rather than "I cannot write there" [src: tracker/items/BUG-0002/journal.md].

## Decision

**A.** The rule is: **a function in `expenses/store.py` that touches the dataset file catches
`OSError` and raises `ExpensesError` naming the path it was given** [src: expenses/store.py].
Nothing above `store.py` learns about `OSError`, and `cli.main` goes on catching exactly one type
[src: expenses/cli.py].

Three things follow, and they are what code can be checked against:

1. **The whole of `save` is inside the boundary**, including `target.parent.mkdir` — the
   directory creation fails on exactly the same class of error as the write, and BUG-0002's note
   asks for this to be decided rather than discovered [src: BUG-0002].
2. **The message mirrors the read path.** `load` says `cannot read <path>: <error>`; `save` says
   `cannot write <path>: <error>`, with the path as given to the function, not the temporary
   file's [src: expenses/store.py].
3. **Cleanup keeps precedence over translation.** `save` writes a temporary file and replaces the
   target with it, and it already removes that temporary file when anything goes wrong. The
   translation to `ExpensesError` wraps that cleanup rather than replacing it, so a failed write
   leaves neither a changed dataset nor a `.expenses-` file behind [src: BUG-0002 AC3].

`ExpensesError` is not a subclass of `OSError`, so a refusal raised inside the wrapped region —
`add_person`'s "already in the group", say — passes through untouched [src: expenses/money.py].

## Consequences

Easy: the two ways this tool can fail now look the same to the person at the terminal, and the
claim already written in the architecture overview — that every refusal writes to stderr, changes
nothing on disk and exits non-zero [src: docs/architecture/overview.md] — becomes true of the
write path as well as the read path. A future store function has a stated rule to follow instead
of a precedent to guess at, which matters most for WI-0003's importer, the next thing that will
write [src: WI-0003].

Hard: the rule is a convention over a module, not something a program enforces, so it is exactly
as strong as the next author's attention. Nothing checks that a new `store.py` function wraps its
file access; the only defence is that this ADR says so and that BUG-0002 leaves a test behind
[src: BUG-0002 AC4]. And an `OSError` that is really a bug — a mistake in this code rather than
the environment refusing — is now reported as a one-line refusal, and whoever debugs it has lost
the traceback.

Reversibility: **cheap.** Moving the boundary to option B is deleting the wrappers in one file
and adding one `except` clause in another; no stored data changes, no command's arguments change,
and the only externally visible difference is the wording of a message and which failures are
covered [src: ADR-0001]. Nothing here touches the record format, so no migration is implied in
either direction.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T01:48:49Z | plan | BUG-0002 | First version |
