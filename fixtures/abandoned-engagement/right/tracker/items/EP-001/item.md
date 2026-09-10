---
id: EP-001
type: epic
title: Settle a shared trip without arguing
status: done
priority: high
outcome: dropped
created: 2026-09-06T09:00:00Z
updated: 2026-09-08T10:00:00Z
---

## Goal

Settle a shared trip without arguing: enter expenses, see who owes whom, and import the bank export instead of retyping it.

## Why now

The stakeholder asked for it, and then stopped replying.

## Success measures

- A trip's expenses can be entered and listed.
- A bank export can be imported without retyping.
- Settling up produces the right amounts to the penny.

## Scope

- The children listed on the board.

## Out of scope

- Everything else.

## Notes

The goal was to settle a shared trip without arguing: put the expenses in, see
who owes whom, and read the bank export rather than typing it all in again.

**The engagement was abandoned.** The pipeline came to you three times with the same open
questions and nothing you could have changed changed between them. The first of those halts was
`2026-09-07T08:00:00Z`; the last was `2026-09-08T09:40:00Z`. Three silent rounds against a
threshold of three (`termination.silence.threshold_rounds`), recorded in
`tracker/waiting/EP-001.md`. This statement is a document rather than a question because there
is nobody to address it to.

Every child of this epic, by ID and by class (`spec/ids-and-statuses.md` §3.5a):

| Child | Class | What that means here |
|-------|-------|----------------------|
| `WI-0001` | **delivered** | adding and listing expenses shipped and was reviewed; the abandonment did not touch it |
| `WI-0002` | **dropped earlier** | the summary line was dropped on 2026-09-07, on your own answer, before the silence began |
| `BUG-0001` | **blocked earlier** | the three-way split loses a penny. It hit its own impasse — the rounding rule — and is not an orphan |
| `WI-0003` | **orphaned, in flight** | the import parser exists on `wi/WI-0003` and stops there |
| `WI-0004` | **orphaned, in flight** | suspended on `WI-0004/Q-001`, which was never answered |
| `WI-0005` | **orphaned, never started** | only the intent was recorded; nothing was built |

Success measures, each addressed (DE3):

- *A trip's expenses can be entered and listed* — **met**, by `WI-0001`.
- *A bank export can be imported without retyping* — **not met**. `WI-0003` and `WI-0004` carry
  the work and both stop here; `WI-0004/Q-001` is the question that would have unblocked it.
- *Settling up produces the right amounts to the penny* — **not met**. `BUG-0001` is the reason
  and it is recorded against this epic rather than implied by the absence of a claim.

Whether you are actually gone is the one thing no program and no reader here can decide. What
this record asserts is only what it can see: that you were asked, that nothing came back, and
how many times.
