---
id: WI-0003
type: work-item
title: Show a monthly summary of envelope activity
status: draft
priority: high
epic: EP-001
created: "2026-09-10T13:14:52Z"
updated: "2026-09-10T13:27:40Z"
depends-on:
  - WI-0002
---

## Story

As someone budgeting into envelopes, I want a summary of a month's activity, so that I can look
back at where the money went without reading every transaction I recorded.

## Acceptance criteria

- [ ] AC1 — a command prints a summary for a month and exits 0
- [ ] AC2 — the summary has one row per envelope, showing what went in, what went out, and what
      remains. The stakeholder asked for exactly these three per envelope (`EP-001/Q-005`)
- [ ] AC3 — a month in which nothing was recorded produces a summary that says so and exits 0,
      rather than printing nothing or failing
- [ ] AC4 — a transaction belongs to the month of its own date — the one given when it was
      recorded, or today's when none was given (`EP-001/Q-004`) — and transactions belonging to
      other months do not appear in the requested month's in and out totals
- [ ] AC5 — the "what remains" figure for an envelope is its balance, which carries across the
      turn of the month untouched: running the summary for a month does not sweep, zero or move
      anything (`EP-001/Q-005`)

## Out of scope

- Comparing two months, trends, or any chart.
- Exporting the summary to a file or another format.
- Rolling a leftover balance forward into the next month.

## Notes

- The answer AC4 was waiting on has landed: a transaction carries the date it happened, given
  explicitly when catching up and defaulting to today otherwise (`EP-001/Q-004`). AC4 above now
  says so.
- The stakeholder named what the summary should show, unprompted: "the monthly summary should
  show me what each envelope took in and what went out of it" (`EP-001/Q-005`). Anything beyond
  that — ordering, totals across envelopes, the format of the month argument — is `refine`'s to
  establish.
- WI-0004 (moving money between envelopes) and WI-0005 (correcting or removing a spend) both
  produce movements this summary will have to account for. This item does not depend on them,
  but whoever refines it should decide how a transfer and a correction appear in a month's in
  and out figures.
