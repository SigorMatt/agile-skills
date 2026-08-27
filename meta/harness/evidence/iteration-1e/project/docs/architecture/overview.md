---
title: Architecture overview
version: 7
status: current
updated: 2026-08-27T01:54:48Z
updated-by: implement
updated-for: BUG-0002
---

# Architecture overview

## The shape of the system

One Python package, run as a command, reading and writing one JSON file on the machine it runs
on. There is no server, no daemon, no database and no network call — the stakeholder's own
constraint is python3 and its standard library with no external services
[src: IDEA.md; tracker/items/EP-001/item.md].

```
python3 -m expenses <noun> <verb> [options]
        │
        ├── expenses/__main__.py   entry point: hands argv to the CLI, returns its exit code
        ├── expenses/cli.py        argparse surface, one handler per command, all printing
        ├── expenses/money.py      parsing, formatting and splitting of amounts
        ├── expenses/settle.py     each person's position, and the payments that settle them
        └── expenses/store.py      locating, loading, validating and saving the dataset
                │
                └── one JSON file  people and expenses together (ADR-0001)
```

The layering is one-way: `cli.py` depends on `store.py`, `money.py` and `settle.py`, `store.py`
depends on `money.py`, `settle.py` depends on neither of them, and nothing below `cli.py` imports
`cli.py` or prints anything [src: expenses/settle.py; expenses/store.py]. That is
what lets the arithmetic and the storage be tested without running commands, and it is the one
structural rule this project has [src: tracker/items/WI-0001/artifacts/plan.md].

## The pieces, and why each exists

**`expenses/money.py`** — amounts are integers counting minor units, never floats
[src: ADR-0002], and an equal split gives any indivisible remainder to the first-named sharers
[src: ADR-0003]. Both decisions are here because "the shares sum to exactly the amount" is an
acceptance criterion rather than an aspiration [src: WI-0001 AC2; WI-0001 AC8].

**`expenses/store.py`** — the dataset is one JSON object holding people and expenses together,
found via `EXPENSES_STORE` or the XDG data directory, written by replacing a temporary file
[src: ADR-0001]. A missing file reads as an empty dataset, which is why the listings can answer
before anything has ever been recorded [src: WI-0001 AC9]. It is also where records are removed,
and where the one relation between the two kinds of record is enforced. WI-0004 added three
module-level functions here — `naming_expenses`, `delete_person` and `delete_expense`
[src: expenses/store.py]. The first reports every stored expense that names a given person, as
`paid_by`, in `shared_by`, or as a key of `shares_minor`; the other two do the removals. That is
what makes the invariant checkable: **every name in a stored expense is a name in
`data["people"]`**, enforced at the two points that can break it — `add_expense`, which refuses an
unknown name, and `delete_person`, which refuses while any expense still names the person and
says how many do [src: ADR-0007; WI-0004 AC3]. Nothing was added to `load`, so the invariant is a
property of what this tool writes rather than of every dataset it can read [src: ADR-0007]. An
expense carries no stored identifier and the record shape did not change for any of this:
`VERSION` is still 1 [src: ADR-0006; expenses/store.py]. Both of the functions that touch the file turn
an operating-system error into a refusal — `load` says `cannot read <path>: <error>`, `save` says
`cannot write <path>: <error>` — so nothing above this module ever sees an `OSError`
[src: ADR-0008; expenses/store.py]. The whole of `save` is inside that boundary, the
parent-directory creation included, and the temporary file it writes is removed before the error
is translated, so a write the operating system refuses changes neither the dataset nor the
directory it lives in [src: expenses/store.py; BUG-0002 AC3].

**`expenses/settle.py`** — the answer to "who owes whom". `positions()` gives each recorded
person their net in whole minor units — what they paid, minus the shares recorded against them —
and `settlement()` turns those into a list of payments by matching the largest debt against the
largest credit, breaking ties on the order people were recorded [src: ADR-0005]. It takes the
dataset dictionary and returns plain data: no file, no print, no import of `store.py` or `cli.py`
[src: expenses/settle.py]. That is what lets every figure in the settlement be tested without
touching a disk [src: tests/test_settle.py], and it is why the report cannot change what it
reports on [src: WI-0002 AC5].

**`expenses/cli.py`** — `argparse` subcommands under two nouns, `person` and `expense`, plus a
third top-level command `settle` which takes no arguments [src: expenses/cli.py]. Each noun has
three actions: `add`, `list` and `delete` [src: expenses/cli.py]. An expense is named to
`expense delete` by its 1-based position in the listing, which is why `expense list` prints that
position as its leading column [src: ADR-0006; WI-0004 AC2]. The positions are not identities —
after a deletion the remaining expenses renumber — so nothing outside a single listing can hold
onto one [src: ADR-0006]. Every success writes to stdout and exits 0; every refusal writes to
stderr, changes nothing on disk and exits non-zero [src: tracker/items/WI-0001/artifacts/refinement-qa.md]. Refusals are raised as a
single exception type from the layers below and turned into a message and an exit code in exactly
one place, so that "nothing was written" is a property of the design rather than of each handler.

**`expenses/__main__.py`** — exists so the tool can be run with `python3 -m expenses`, which
needs no installation step [src: tracker/items/WI-0001/artifacts/plan.md]. That is what makes the
standard-library-only constraint [src: tracker/items/EP-001/item.md] hold at the point of use as
well as in the source; `commands.build` is `null` for the same reason [src: ADR-0004].

## What this shape does not do

It does not support two people using one dataset, or two processes writing at once; the product
is explicitly one person on one machine [src: docs/product/vision.md]. It does not convert
between currencies, and it stores no currency at all [src: ADR-0002]. It does not move money: `settle` prints the payments and
records nothing, so the group hands the money over elsewhere [src: WI-0002 AC5].

## What is coming

WI-0003 adds an importer that turns rows of a bank CSV export into the same expense records;
it is parked until the stakeholder supplies a sample of their bank's format
[src: tracker/items/EP-001/questions/Q-001.md]. It will have to honour the invariant recorded
above under `expenses/store.py`, which is enforced where this tool writes and nowhere else
[src: ADR-0007].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 7 | 2026-08-27T01:54:48Z | implement | BUG-0002 | `store.save` turns an `OSError` into a refusal now, so ADR-0008's rule moves out of "What is coming" into the `expenses/store.py` piece, where it describes both functions that touch the file rather than an intention. Only WI-0003 is still coming |
| 6 | 2026-08-27T01:48:49Z | plan | BUG-0002 | Records the boundary BUG-0002 will move `store.save` behind, as ADR-0008: an operating-system error on the dataset becomes an `ExpensesError` inside `expenses/store.py`, not in the CLI. Written under "What is coming", together with the fact that the refusal claim in the `expenses/cli.py` piece does not yet hold on the write path |
| 5 | 2026-08-27T01:32:29Z | implement | WI-0004 | `person delete` and `expense delete` exist, so deletion moves out of "What is coming" into the body: the `expenses/store.py` piece names the **three** functions the item added — `naming_expenses`, `delete_person` and `delete_expense`, not the two version 4 claimed — and states ADR-0007's invariant as a property of the delivered code, and the `expenses/cli.py` piece records the third action under each noun and `expense list`'s position column. Only WI-0003 is still coming |
| 4 | 2026-08-27T01:11:28Z | plan | WI-0004 | Records the shape WI-0004 will add: `expense list` gains a position column and an expense becomes addressable by it (ADR-0006), and the people-and-expenses relation becomes a named invariant enforced in `store.py` (ADR-0007). Written under "What is coming" rather than in the body, because neither function exists yet |
| 3 | 2026-08-27T00:35:17Z | implement | WI-0002 | `expenses/settle.py` and the `settle` command exist, so they move from "What is coming" into the diagram, the layering rule and a piece of their own. "What this shape does not do" now says what `settle` does instead of what WI-0002 will do |
| 2 | 2026-08-27T00:28:48Z | plan | WI-0002 | Records the shape WI-0002 will add: a new pure-arithmetic module `expenses/settle.py` at the bottom of the one-way layering, a third top-level command in `cli.py`, and the settlement rule as ADR-0005. Written under "What is coming" rather than in the body, because the module does not exist yet |
| 1 | 2026-08-26T23:52:03Z | plan | WI-0001 | First version: the package layout, the one-way layering, and the four decisions recorded as ADR-0001 to ADR-0004 |
