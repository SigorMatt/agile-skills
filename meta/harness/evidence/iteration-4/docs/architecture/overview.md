---
title: Architecture overview
version: 5
status: current
updated: 2026-08-29T14:13:13Z
updated-by: answer-questions
updated-for: EP-001
---

# Architecture overview

## What this system is

Recall is a single-user command-line tool, run in a terminal by the person whose cards they are
[src: EP-001/Q-001]. It has no server, no network use, no accounts and no second device
[src: docs/product/vision.md]. Everything it knows lives in one JSON file on that person's disk
[src: ADR-0002].

This document describes the shape as of WI-0004, which adds `recall delete` — the follow-up the
stakeholder asked for when they accepted the engagement, and the tool's first destructive command
[src: WI-0004; src: EP-001/Q-005].

## The shape

```
recall            # executable entry point: sets the import path, calls main(), exits with it
recall.py         # the module: argument handling, the commands, and the store
tests/            # unittest cases, driving the command as a subprocess
~/.recall.json    # the store: one JSON document, overridable by RECALL_FILE
```

Three responsibilities, in one module:

1. **The command line.** The first argument names a command; the rest are positional and are
   never options [src: ADR-0005]. The command decides an exit code: 0 for success, 2 when the
   command line is wrong on its own terms — decidable without opening the store — and 1 when the
   command line was fine and the command could not be carried out. A store that cannot be read or
   written is one instance of that; a card number naming no card is the other
   [src: ADR-0005; src: ADR-0009].
2. **The commands.** `add` appends a card; `list` prints the pile in card-number order
   [src: WI-0001 AC1; WI-0001 AC6]. `review` walks the due cards one at a time, records a
   result for each, and decides when each comes back by moving it along the interval ladder
   [src: WI-0002 AC1; WI-0002 AC2; WI-0003 AC2]. `delete` removes one card by its number,
   immediately and with no confirmation prompt, printing what it removed — which is what the
   stakeholder chose over being asked [src: WI-0004 AC2; src: WI-0004/Q-001]. The placeholder
   next-due date that version 2 of this document described is gone; ADR-0007 replaced it
   [src: ADR-0006; ADR-0007].
3. **The store.** Resolve the path, read the document, write it back by rename. The path is
   `RECALL_FILE` when that is set and non-empty, and `~/.recall.json` otherwise
   [src: ADR-0002]. The schema and the write protocol are ADR-0004's, the per-card review
   state is ADR-0006's, and the scheduling state and the version-3 shape are ADR-0007's
   [src: ADR-0004; ADR-0006; ADR-0007].

The store is the only state. There is no cache, no index and no second copy of a card, so a
question about what the tool believes is answered by reading one file [src: ADR-0004].

## The session reads a stream, never a terminal

`review` is the tool's only interactive command, and it is deliberately not *terminal*
interactive: it reads standard input a line at a time, so a key is followed by Enter, and a
whole session can be driven from a pipe [src: WI-0002 AC9]. There is no raw keypress mode, no
screen clearing and no cursor control [src: WI-0002].

That is a constraint on every future interactive feature in this tool, not a detail of this one.
It exists because the only party that checks a criterion here has no hands: `verify` runs
commands and reads output, and a session that demanded a terminal could not be checked at all.
The end of standard input therefore ends a session exactly as `q` does, keeping what was already
recorded [src: WI-0002 AC9].

## Why it is arranged this way

The user is one person on one machine, so the file *is* the database and the process lifetime is
one command [src: docs/product/vision.md]. Dependencies are the standard library only, for
running and for testing, because the environment that runs the pipeline refuses to install
anything into its interpreter [src: ADR-0003].

**The store stays inside `recall.py`.** Version 1 of this document said the obvious next move
would be to split it out once a third command needed it, and named WI-0002 as where the question
gets asked again. It has been asked, at WI-0002 and again now with all four commands built, and
the answer is still no [src: EP-001/Q-007; src: WI-0002].

At the end of the epic the module is **491 lines**, of which roughly 260 are code and the rest
are docstrings, comments and blank lines — a ratio that is deliberate, because most of what is
written down here is *why* a check exists rather than what it does
[src: run: wc -l recall.py → 491; src: recall.py]. It holds 20 functions and one exception class,
and the store layer is separated within the file by the function contracts WI-0001 fixed:
`load` and `save` are the only functions that touch the disk at all, `store_path` decides where
they touch it, and `add_card`, `delete_card`, `due_cards`, `next_interval` and `record_result`
work on a document already in memory and never reach past it [src: recall.py; src: WI-0001]. Every `cmd_*` function is written against that
seam, which is what makes each of them short. A second file would add an import graph and a
second place to keep in step, for no reader's benefit [src: WI-0002].

The trigger for re-asking is not a line count and never was — the number above only records what
the module grew to, and reading it as the reason would be reading this decision backwards. It is
worth re-asking when something **other than a command** needs the store: a migration, a second
front end, or anything that must key on a card across time, which `ADR-0008` already says cannot
key on the card number [src: ADR-0008].

## Decisions that constrain future work

| ADR | what it fixes |
|-----|---------------|
| ADR-0001 | the interval ladder: 1, 3, 7, 30 days, driven by a binary right/wrong result |
| ADR-0002 | the store's location — `~/.recall.json`, overridable by `RECALL_FILE` — and that it is JSON |
| ADR-0003 | the test and lint commands: stdlib `unittest`, and `compileall` as the syntax gate |
| ADR-0004 | the store's schema, its write protocol, and what happens when it cannot be used |
| ADR-0005 | the entry point, positional-only arguments, exit codes, streams and the listing format |
| ADR-0006 | what a review stores on a card — a next-due date and a last result — store version 2, and saving after each card |
| ADR-0007 | the scheduling state — `interval` in days, `null` for a card never answered — store version 3, the strict validation of `due` and `interval`, and the ladder as one constant |
| ADR-0008 | that a card number is derived from the largest one stored and may be reused after a deletion, and that deleting changes neither the schema nor the store version |
| ADR-0009 | exit code 1 as "the command could not be carried out", of which an unusable store is one case and a number naming no card the other |

## The store refuses what it cannot read, rather than repairing it

`load` checks every field it reads on the way in, and a document that fails any check is reported
and left byte-for-byte alone rather than repaired or overwritten
[src: recall.py; ADR-0004; WI-0003 AC9]. WI-0003 extended that from the *shape* of a card to the
*content* of its two scheduling fields: a `due` that is not a `YYYY-MM-DD` date, and an `interval`
outside the ladder, are both unreadable stores [src: ADR-0007].

The extension has a cost worth stating where it will be found: a store an older `recall` read
happily can be one this `recall` refuses [src: ADR-0007]. It was taken deliberately, because from
WI-0003 onwards hand-editing those two fields is the documented way to move a card, so a typo in
one of them is the likeliest mistake a user makes [src: WI-0003; README.md].

## A card number is a handle, not an identity

`delete` removes a card object from the store and leaves every other card exactly as it was, so
surviving cards keep the numbers they had [src: WI-0004 AC3; src: ADR-0008]. The next number is
still one more than the largest stored, so deleting the highest-numbered card frees its number
for the next card added [src: ADR-0004; src: ADR-0008].

That is accepted rather than overlooked, and it leaves one constraint behind for whatever comes
next: anything that refers to a card *across time* — a review history, a statistics command, an
export — must not key on the card number, because one number can name two cards over the life of
a store [src: ADR-0008]. Nothing in the tool does today; there is no history and no second copy
of a card [src: ADR-0004].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 5 | 2026-08-29T14:13:13Z | answer-questions | EP-001 | EP-001/Q-007: the store-stays-in-one-module decision was resting on "roughly 280 lines", true at v2 and never re-checked when v3 and v4 each added a command. Corrected to the module as it actually is, with the seam that carries the decision named function by function, and the re-ask trigger stated as what it always was rather than as a size |
| 4 | 2026-08-29T13:34:39Z | plan | WI-0004 | `delete`, the tool's first destructive command; exit code 1 widened to "the command could not be carried out"; ADR-0008 and ADR-0009 added to the constraints table; and a section on a card number being a handle rather than an identity |
| 3 | 2026-08-29T12:33:35Z | plan | WI-0003 | The schedule: `review` now decides when a card comes back and the placeholder is gone, ADR-0007 added to the constraints table, and a section on the store refusing rather than repairing what it cannot read |
| 2 | 2026-08-29T11:44:28Z | plan | WI-0002 | The `review` command and the per-card review state; the rule that the session reads a stream and never requires a terminal; ADR-0006 added to the constraints table; and the store-module question v1 deferred to this item, answered — it stays in `recall.py` |
| 1 | 2026-08-29T11:16:00Z | plan | WI-0001 | First version, written while planning WI-0001: the entry point, the two commands, the single-file store, and the ADRs that constrain them |
