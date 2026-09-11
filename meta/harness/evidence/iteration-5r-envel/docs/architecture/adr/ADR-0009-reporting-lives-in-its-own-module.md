---
title: Reporting lives in its own module, beside the operations rather than among them
version: 2
status: current
updated: 2026-09-11T08:22:40Z
updated-by: implement
updated-for: WI-0006
---

# ADR-0009 — Reporting lives in its own module, beside the operations rather than among them

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

`envel/envelopes.py` holds the tool's five operations — create, add income, list, record a spend,
move money [src: docs/architecture/overview.md] — and each of them is the same kind of thing: a
decision about a store, taking a document and returning a new one or a refusal
[src: envel/envelopes.py:1].

`WI-0003` adds something that is not that kind of thing. A summary changes nothing, returns no new
document, and is the first thing in the tool that needs month arithmetic [src: ADR-0008] and a
per-envelope fold over the entry log. It is also not the last: `WI-0006` [src: WI-0006] asks for
the spends recorded against an envelope, which is another read that answers a question about
stored entries rather than changing them.

Somewhere has to hold it, and the tool's stated shape is one module per concern
[src: docs/architecture/overview.md].

## Options considered

- **A — a sixth operation in `envel/envelopes.py`.** Cost: nothing new to learn; it is what every
  previous item did. Risk: the module's own docstring says an operation *"returns either Ok,
  carrying the new document and the lines to show, or Refusal"* [src: envel/envelopes.py:1], and a
  report returns lines and no new document, so the file would hold two kinds of thing under one
  description. The month arithmetic — roughly sixty lines nothing else in the file needs — would
  sit among the five functions that every command depends on.
- **B — a new module `envel/summary.py`**, importing `envelopes` for name matching, and `money`
  and `dates` for formatting and month parsing. Cost: one more row in the overview's module table
  and one more level in the dependency graph. Risk: if `WI-0006` turns out to want the same place,
  the module is named for one report rather than for reporting; that is `WI-0006`'s plan's call and
  renaming a module nothing outside the package imports costs one line.
- **C — put it in `envel/cli.py`.** Cost: none at first. Risk: `cli` is *"the only module that
  writes to a stream or decides an exit code"* [src: envel/cli.py:1], and putting the computation
  there makes the one module that cannot be tested without a subprocess also the one that holds the
  arithmetic AC3 is about.

## Decision

Option **B**. `envel/summary.py` holds this project's reports: the month rule of `ADR-0008`, and
for each report the figures or lines it prints and the order it prints them in. At the time of
writing that was the monthly summary alone; `WI-0006`'s listing of a month's entries was put here
too, for the reason this ADR gives [src: envel/summary.py]. Each returns `envelopes.Ok` or
`envelopes.Refusal`, the same two types every operation returns [src: envel/envelopes.py], so
`cli` dispatches them exactly as it dispatches the operations [src: envel/cli.py] and gains no new
branch shape.

The dependency direction stays one way and gains one edge: `cli` → `summary` → (`envelopes`,
`money`, `dates`). `summary` imports `envelopes`; `envelopes` does not import `summary`, and
nothing below `summary` learns about it.

`summary` prints nothing and calls no `sys.exit`, like everything else below `cli`
[src: docs/architecture/overview.md].

## Consequences

**Easy: `envelopes.py` keeps one description that is true of everything in it**
[src: envel/envelopes.py:1], and the summary's
arithmetic is testable as a function of (document, month) with no subprocess and no store on disk —
which is what `WI-0003` AC3's reconciliation needs, because it is an assertion about numbers rather
than about output.

**Hard: there are now two places a reader might look for "what the tool does"**, and the answer is
that `envelopes` changes things and `summary` reports on them. That distinction has to be written
in the overview's module table or it is folklore; this ADR is why the row exists.

**Reversibility: easy.** Moving the functions into `envel/envelopes.py` is one file's worth of cut
and paste plus one import line in `envel/cli.py`. No stored data, no published interface, and no
acceptance criterion of any item names the module [src: WI-0003].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-09-11T08:22:40Z | implement | WI-0006 | One erratum, recorded below: `## Decision` enumerated what `envel/summary.py` holds, and the enumeration stopped being complete when `WI-0006` put a second report there. The decision — reporting lives in its own module and returns the two types `cli` already dispatches — is unchanged and is exactly what this item followed; no code has to change to satisfy the new text. The `## Consequences` sentence about *two places a reader might look* is untouched and still true: this change added a report, not a third module. |
| 1 | 2026-09-11T06:20:16Z | plan | WI-0003 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T08:22:40Z | implement | WI-0006 | erratum | `## Decision`, first paragraph, said *"`envel/summary.py` holds the summary: the month rule of `ADR-0008`, the four figures, the row ordering and the lines"*. That enumeration is no longer what the module holds: `WI-0006` added a second report to it [src: WI-0006 AC1 "The command is `envel entries`"], [src: envel/summary.py], which is what this ADR's own reasoning called for. Replaced with a clause saying the module holds this project's reports, naming what that was when the ADR was written and what was added. The two line-number citations in the same paragraph were widened to their files, because the lines they named have moved. |
