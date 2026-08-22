---
title: The ledger is one JSON document, at an XDG default location, selectable per run
version: 1
status: current
updated: 2026-08-22T02:06:34Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — The ledger is one JSON document, at an XDG default location, selectable per run

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 must persist people, expenses and repayments across process exits [src: WI-0001 AC10],
from a default location when none is given and from a location chosen per run when one is
[src: WI-0001 AC9]. The stakeholder settled the requirement — "being able to point it at a
different file would be handy — like a separate one for a trip. Otherwise just use a sensible
default" [src: WI-0001/Q-004] — and `refine` deliberately left the format and the path to this
skill [src: WI-0001].

Two constraints narrow the field. `ADR-0001` requires two record kinds stored together, never one
represented as the other [src: ADR-0001]. `WI-0001` AC5 requires that the stored form of an expense hold one
amount and a set of sharers and no per-person amount, so `verify` can read the file and check it.
That second constraint means the on-disk form is not a private implementation detail: it is
inspected by an acceptance criterion, so it has to be something a person can read.

Scale is small and known: one operator, one friend group, expenses entered by hand or imported
from one bank export at a time [src: docs/product/vision.md].

## Options considered

- **A — one JSON document per ledger.** Cost: the whole file is read and rewritten on every
  change, so the cost of a write grows with the ledger [src: WI-0001 AC10]. Risk: a crash mid-write could truncate
  the file, which is why the decision below specifies an atomic replace. Benefit: readable by a
  person and by `verify` without a tool, trivially diffable, and one file is exactly the unit the
  stakeholder wants to copy for a trip.
- **B — SQLite, one database file per ledger.** Cost: schema and migration machinery for a
  three-table model that fits in a page of JSON; `verify` needs a SQL client to check AC5. Risk:
  low technically, but it is machinery this item does not need. Benefit: real transactions and
  indexed lookups nobody here will use — the whole ledger fits in memory by construction.
- **C — one CSV file per record kind.** Cost: three files to keep consistent, and a sharer list
  inside a CSV cell needs its own escaping convention. Risk: the file the user copies for a trip
  is no longer one file. Benefit: none that A does not have.
- **D — JSON Lines, one record per line.** Cost: append-only writes are cheap. Risk: people,
  expenses and repayments interleave in one stream and the reader has to discriminate them,
  which is `ADR-0001`'s "never represent one as the other" made harder rather than easier.

On where the default lives:

- **E — `$XDG_DATA_HOME/expenses/ledger.json`, falling back to `~/.local/share/expenses/ledger.json`.**
  The platform convention for data a program keeps on the user's behalf, and the option that makes
  "every run uses the same default" independent of the working directory [src: WI-0001 AC9].
- **F — `~/.expenses.json`.** Simpler to say out loud; puts a dotfile in the home directory,
  which the XDG convention exists to stop.
- **G — `./expenses.json`, relative to the working directory.** Rejected: the ledger a person
  sees would depend on which directory they ran the command from, which turns AC9's "every run
  uses the same default" into a trap rather than a guarantee.

## Decision

**A, with E.**

The ledger is a single JSON object, written UTF-8 with a trailing newline, of this shape:

```json
{
  "version": 1,
  "people":     [ { "name": "Ana" } ],
  "expenses":   [ { "date": "2026-08-22", "payer": "Ana", "amount_minor": 6000,
                    "description": "dinner", "sharers": ["Ana", "Ben", "Cara"] } ],
  "repayments": [ { "date": "2026-08-22", "from": "Ben", "to": "Ana", "amount_minor": 2000 } ]
}
```

- `version` is the on-disk schema version, so a later change has somewhere to branch. It is `1`.
- The three arrays preserve insertion order, which is what AC2, AC8 and AC12 mean by "in the
  order they were recorded" [src: WI-0001 AC8]. No sort is applied on read or on write.
- `people` holds objects rather than bare strings so that a later field — an email, a nickname —
  does not change the type of the array.
- `expenses` and `repayments` are separate arrays. Nothing in an expense identifies a repayment
  and nothing in a repayment identifies an expense, which is `ADR-0001`'s decision expressed in
  the file.
- `amount_minor` is an integer; `ADR-0004` records why.
- Names in `payer`, `sharers`, `from` and `to` are stored in the display form the person first
  typed, and are the same strings that appear in `people`.

**Location, in precedence order:** the `--file PATH` option if given; otherwise the
`EXPENSES_LEDGER` environment variable if set and non-empty; otherwise
`$XDG_DATA_HOME/expenses/ledger.json`, with `$XDG_DATA_HOME` defaulting to `~/.local/share` when
unset or empty. A location that does not exist yet is created — parent directories included — on
the first write. A missing file reads as an empty ledger; it is not an error.

**Writes are atomic:** serialise to a temporary file in the same directory, then `os.replace` it
over the target [src: docs/architecture/overview.md]. A crash leaves either the old ledger or the
new one, never half of either — which is what AC10 requires of data that has already been
recorded [src: WI-0001 AC10].

## Consequences

- `verify` can satisfy AC5 by opening the file and reading it, with no tooling and no knowledge
  of the code.
- Every command rewrites the whole file. For a friend group's expenses that is microseconds, and
  the plan records it as a risk with the threshold at which it stops being true.
- Two ledgers are two paths, and they cannot interfere: nothing is shared between them, which is
  AC9's independence requirement satisfied by construction rather than by care.
- The environment variable makes the whole test suite able to run against a scratch path without
  touching the operator's real ledger, and without every test having to remember a flag.
- **Reversibility: moderate, and it decays.** Until there is data on disk, changing to SQLite is
  a rewrite of one module. Afterwards it is a migration, and `version` is the field that would
  carry it. The default *location* is cheaper to change than the *format*: a person can move one
  file. Changing the shape of the JSON after this ships is the expensive direction, which is why
  `version` exists from the first write rather than being added when it is first needed.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T02:06:34Z | plan | WI-0001 | First version |
