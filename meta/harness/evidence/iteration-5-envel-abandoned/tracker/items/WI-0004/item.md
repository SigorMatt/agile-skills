---
id: WI-0004
type: work-item
title: Move money from one envelope to another
status: draft
priority: high
epic: EP-001
created: "2026-09-10T13:27:04Z"
updated: "2026-09-10T13:27:04Z"
depends-on:
  - WI-0002
arose-from: EP-001/Q-005
---

## Story

As someone budgeting into envelopes, I want to move money from one envelope to another, so that
I can cover a shortfall in one pot from another pot without leaving the tool or falsifying what
I actually spent.

## Acceptance criteria

- [ ] AC1 — a command moves a stated amount from one named envelope to another named envelope
      and exits 0
- [ ] AC2 — after a move, the source envelope's balance is lower by the amount and the
      destination envelope's balance is higher by the amount, and nothing else changes
- [ ] AC3 — a move naming an envelope that does not exist reports the unknown name, exits
      non-zero, and moves nothing
- [ ] AC4 — a move larger than the source envelope's balance is refused, exits non-zero, and
      moves nothing, on the same principle as WI-0002's refusal of an overspend
- [ ] AC5 — a move recorded in one invocation is still reflected in the balances shown by a
      later, separate invocation

## Out of scope

- Automatically covering an overspend. WI-0002 refuses a spend that exceeds its envelope; this
  item gives the person the means to fix that themselves, and does not do it for them. The
  stakeholder was explicit that they do not want the tool working out splits (`EP-001/Q-002`).
- Moving money into or out of anything that is not an envelope; there is no pool
  (`EP-001/Q-002`).
- How a move appears in the monthly summary; that is WI-0003's to decide.

## Notes

- This item exists because of the stakeholder's answer to `EP-001/Q-005`: "I need to be able to
  move money from one envelope to another — that's how I cover an overspend." It was filed by
  `answer-questions` when that answer was consumed, because no existing item recorded the work
  and widening one to swallow it would have hidden the scope change from the board.
- It is the counterpart to WI-0002 AC6. Refusing an overspend is only workable because this
  command exists, so whoever plans the two should look at them together.
- The command word, the argument order and the amount format are not fixed here; `refine` pins
  them, consistently with WI-0002.
