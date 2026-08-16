---
title: format_report grows optional parameters instead of changing its signature
version: 1
status: current
updated: 2026-08-17T00:05:00Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0005 — format_report grows optional parameters instead of changing its signature

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

`format_report(rows)` was written for WI-0001: it sums the rows it is given, prints the total
right-aligned in a column sized to the widest number printed, and labels it `total`. With no rows
it returns `no files`.

WI-0002 needs the same renderer to print something it cannot derive from its argument. With
`--top`, the rows shown are the first N, but the total is the sum of **every** file in the folder
and its label names how many that was: `1204  total (all 27 files)` (AC3, AC5, AC10). And with
`--top 0` on a folder that does have files, there are **no** rows and there is still a total row
(AC6) — while a folder with no files at all still prints `no files` whatever N is (AC9).

Two criteria constrain how this may be done. WI-0002 AC4: without `--top`, the output must be
byte-identical to WI-0001's and "the tests written for WI-0001 pass unmodified after this item".
Those tests include `format_report([]) == "no files\n"` and three calls of the one-argument form
with exact expected strings. WI-0001's criteria may not be edited to accommodate this item.

## Options considered

- **A — optional parameters: `format_report(rows, total=None, label="total")`.** When `total` is
  `None` it is the sum of the rows, which is WI-0001's behaviour exactly; `no files` is returned
  when there are no rows *and* no explicit total, so an explicit total still prints its row with
  no rows above it. Cost: the `None` sentinel carries two meanings at once — "derive the total"
  and "an empty call means no files". Risk: low, and it is the only option that leaves WI-0001's
  unit tests untouched by construction.
- **B — a second function for the `--top` path**, leaving `format_report` alone. Cost: the column
  arithmetic and the row formatting — the two places AC1 and AC10 make exact — would exist twice
  and could drift apart. Risk: high for a rule stated to the space character in two items'
  criteria.
- **C — change the signature to `format_report(rows, total, label)` and update WI-0001's tests.**
  Cost: it edits tests that another item's criterion (AC4) requires to pass unmodified. Risk:
  it makes AC4 unverifiable, which is not the implementer's or the architect's to trade away.

## Decision

**Option A.** `format_report(rows, total=None, label="total")`:

- no rows and `total is None` → `"no files\n"` (WI-0001 AC10, WI-0002 AC9);
- `total is None` → the sum of `rows`, and the label stays `total` (WI-0001 AC1/AC3, WI-0002 AC4);
- otherwise the caller's `total` and `label` are printed, with the column sized to the widest
  number actually printed — the total included — exactly as before (WI-0002 AC10).

`main` decides which call to make; the renderer holds no opinion about `--top`.

## Consequences

- WI-0001's four `FormatReportTest` cases and all of its end-to-end cases pass without being
  touched, which is what makes AC4 checkable rather than an assurance.
- The rendering rules — two spaces, right alignment, width over every number printed, the total
  last — exist in exactly one place, so a later change to the row format cannot make `--top`
  and plain output disagree.
- The `None` sentinel means "the folder had no files" is a judgement `main` makes, not one the
  renderer can make on its own. If a third caller ever forgets, it prints `no files` for a folder
  that had some — the one way this design can be misused. The docstring says so, and the AC6 and
  AC9 tests pin both branches.
- **Reversibility: cheap but not free.** Collapsing to option C later is a one-line signature
  change plus edits to WI-0001's tests; those edits are only permissible once AC4 has been
  delivered and closed, which it will have been. Moving to option B is a straight duplication and
  should not be done.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-17T00:05:00Z | plan | WI-0002 | First version |
