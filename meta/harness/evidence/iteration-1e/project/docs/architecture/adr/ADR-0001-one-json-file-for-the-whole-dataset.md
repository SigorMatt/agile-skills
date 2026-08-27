---
title: Keep the whole dataset in one JSON file, found by EXPENSES_STORE or the XDG data directory
version: 1
status: current
updated: 2026-08-26T23:52:03Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0001 — Keep the whole dataset in one JSON file, found by EXPENSES_STORE or the XDG data directory

- **Status:** accepted
- **Date:** 2026-08-26
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 requires that people and expenses survive the process exiting [src: WI-0001 AC4], and
`refine` deliberately left both the store's location and its format undecided, recording them as
open design questions for this skill [src: tracker/items/WI-0001/item.md]. EP-001 constrains the
whole epic to python3 and its standard library, with no network and no external services, and its
success measures require that a person never has to hand-edit a data file to use the tool
[src: tracker/items/EP-001/item.md].

Two further constraints come from the criteria rather than from the prose. AC8 has to be checked
by running a sequence of commands "against a fresh empty store" twice [src: WI-0001 AC8], and AC4
compares two runs byte for byte [src: WI-0001 AC4] — so whoever verifies this item needs to be
able to point the tool at an empty store without deleting the developer's own data. And WI-0003
will later append imported expenses to the same dataset [src: WI-0003].

## Options considered

- **A — One JSON file holding people and expenses together.** Cost: the whole file is rewritten
  on every change, so the largest dataset that works is the largest one that fits in memory.
  Risk: none at this scale — a friend group's expenses are thousands of records at the outside.
- **B — `sqlite3` from the standard library.** Cost: a schema, migrations once WI-0004 adds
  deletion, and a binary file a person cannot read or repair. Risk: heavier than the problem, and
  it makes the "never hand-edit" measure harder to honour rather than easier, because a person
  who does need to look cannot.
- **C — Two CSV files, one for people and one for expenses.** Cost: an expense's sharers are a
  list, so CSV needs a nested encoding inside a cell; the description is free text and will
  contain commas. Risk: a hand-rolled escaping scheme, which is exactly the kind of thing that
  breaks on the first real description.
- **D — A file in the current working directory.** Cost: none to build. Risk: the tool answers
  differently depending on where it is run from, which is a surprise a person discovers by losing
  data.

## Decision

The dataset is a single JSON object in one file, written with `json.dump` and read with
`json.load`, with this shape:

```json
{
  "version": 1,
  "people": ["Ana", "Ben"],
  "expenses": [
    {
      "amount_minor": 3000,
      "paid_by": "Ana",
      "shared_by": ["Ana", "Ben", "Cara"],
      "shares_minor": {"Ana": 1000, "Ben": 1000, "Cara": 1000},
      "date": "2026-08-26",
      "description": ""
    }
  ]
}
```

The file is located, in order:

1. the value of the `EXPENSES_STORE` environment variable, if it is set and non-empty;
2. otherwise `$XDG_DATA_HOME/expenses/expenses.json`, if `XDG_DATA_HOME` is set and non-empty;
3. otherwise `~/.local/share/expenses/expenses.json`.

A missing file means an empty dataset — no people and no expenses — and is not an error
[src: WI-0001 AC9]. Its parent directory is created on the first write. A write is done by
writing a sibling temporary file and `os.replace`-ing it over the target, so an interrupted write
cannot leave a half-written dataset behind.

`version` is written and read back; a file whose `version` is not 1 is a refusal rather than
something to guess at.

## Consequences

Easy: reading the whole dataset for a listing or a report; adding WI-0003's imported expenses;
WI-0004's deletions, which become a filter and a rewrite. A person can open the file and see
their own data, which is what makes "you should never have to hand-edit it" a promise rather than
a restriction.

Hard: concurrent use from two processes, which nothing in EP-001 asks for and which the vision
explicitly excludes [src: docs/product/vision.md]. Datasets far larger than memory, likewise out
of scope.

`EXPENSES_STORE` exists so that the acceptance criteria can be checked at all: each of AC4, AC8
and AC9 is stated against a fresh or empty store [src: WI-0001 AC4; WI-0001 AC8; WI-0001 AC9],
and without an override, verifying them would mean deleting whatever is in the default location.
It is a documented part of the tool, not a test hook — step 7 of the plan puts it in the README
[src: tracker/items/WI-0001/artifacts/plan.md].

**Reversibility: high.** The store's location is resolved in one function and its format is read
and written in one module [src: tracker/items/WI-0001/artifacts/plan.md]. Changing either means
changing that module and a one-off conversion of an existing file; no acceptance criterion names
a path or a format, which `refine` arranged deliberately.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-26T23:52:03Z | plan | WI-0001 | First version |
