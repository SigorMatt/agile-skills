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

An earlier draft of this page carried `[src: WI-0001 ## Acceptance criteria]`, which is not one of
the seven forms, and the correction is recorded here rather than by rewriting the draft. A marker
inside backticks is a quotation, not a citation — without that rule this paragraph could not exist
and the record could not describe its own defect (F-037) [src: ADR-0001].

Nothing in this workspace may cite the toolkit by pointing at a path inside it, so the rule this
page is written under is quoted and attributed instead. The gate cannot open that document — it is
installed outside the record and it upgrades underneath this page — so what it is checking is that
the citation carries enough for a reader to check it (ADR-0013)
[src: toolkit: doc-header.md §4a "An unresolvable citation is worse than none"].

A marker must sit on one line to be read at all, and two toolkit sources fit inside one of them —
which is where this form parts company with `run:`, whose command swallows every remaining
semicolon
[src: toolkit: doc-header.md §4a "the quoted text lives inside the marker"; toolkit: pipeline.yaml orchestrator.steps "no question anywhere in the engagement is open"].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T09:00:00Z | plan | WI-0001 | First version |
