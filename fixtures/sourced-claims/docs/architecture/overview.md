---
title: Architecture overview
version: 1
status: current
updated-by: plan
updated-for: WI-0001
updated: 2026-08-16T09:00:00Z
---

# Architecture overview

The tool reads no environment variable other than `EXPENSES_STORE`
[src: docs/architecture/adr/ADR-0001-one-environment-variable.md].

`format_report` only renders the rows it is handed; the decision about how many rows there are
belongs to its caller [src: ADR-0001].

Recursion was deferred by the author, so adding it later is a change of scope rather than a
natural extension. No citation is required for that sentence: it hedges, and hedged prose is not
what goes wrong.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T09:00:00Z | plan | WI-0001 | First version |
