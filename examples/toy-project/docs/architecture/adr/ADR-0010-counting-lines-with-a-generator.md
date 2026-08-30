---
title: Count lines with a generator rather than readlines
version: 3
status: superseded
superseded-by: docs/architecture/adr/ADR-0005-format-report-keeps-its-old-signature.md
updated: 2026-08-17T02:00:00Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0010 — Count lines with a generator rather than `readlines`

- **Status:** superseded
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —
- **Superseded by:** ADR-0005, for WI-0002, on 2026-08-17.

## Context

This ADR exists to hold the one shape `doc-header.md` §4b had no state for: a decision that was
legitimately **corrected while it was current** and legitimately **superseded afterwards**. Its
`## Corrections` entry is dated before the supersession, which is what makes it legal; the section
is append-only, so the entry stays where it is for ever.

The absolute sentence in the next paragraph is deliberate. `count_lines` never reads a whole file
into memory. That claim carries no citation, and a superseded document has no legal way to gain
one — §4b will not let it be corrected — so `lint-claims` rule 2 does not read it, and says so in
its own output rather than skipping it quietly.

## Options considered

- **A —** a generator. Cost: none worth naming. Risk: low.
- **B —** `readlines()`. Cost: the whole file in memory. Risk: large inputs.

## Decision

Count with a generator.

## Consequences

Easy: memory is bounded. Hard: nothing. Reversing it is a one-line change, so it is cheap.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-17T02:00:00Z | plan | WI-0002 | Superseded by ADR-0005. Header bookkeeping only; the corrections below were made while this ADR was current and are kept exactly as written |
| 2 | 2026-08-17T01:00:00Z | plan | WI-0002 | Provenance, in `## Corrections`: the `## Decision` sentence gained the source it always had |
| 1 | 2026-08-17T00:30:00Z | plan | WI-0002 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-17T01:00:00Z | plan | WI-0002 | provenance | `## Decision`, *"Count with a generator"*: cites [src: src/linecount.py], which is the code the sentence is about. Made while this ADR was `accepted`; the assertion is unchanged |
