---
id: WI-0005
type: work-item
title: Correct or remove a spend that has already been recorded
status: draft
priority: high
epic: EP-001
created: "2026-09-10T13:27:07Z"
updated: "2026-09-10T13:27:07Z"
depends-on:
  - WI-0002
arose-from: EP-001/Q-005
---

## Story

As someone budgeting into envelopes, I want to correct or remove a spend I have already
recorded, so that a mistake I make while typing does not leave an envelope balance permanently
wrong.

## Acceptance criteria

- [ ] AC1 — a command identifies an already-recorded spend well enough for a person at a
      terminal to pick out the one they mean, and exits 0
- [ ] AC2 — a command removes an identified spend, and afterwards the envelope's balance is what
      it would have been had that spend never been recorded
- [ ] AC3 — a command corrects an identified spend's amount, and afterwards the envelope's
      balance reflects the corrected amount
- [ ] AC4 — correcting or removing a spend that does not exist reports that, exits non-zero, and
      changes nothing
- [ ] AC5 — a correction or removal made in one invocation is still reflected by a later,
      separate invocation

## Out of scope

- An audit trail of corrections, an undo stack, or any record of what a spend said before it was
  amended. The stakeholder said they care about the correction "far more than about keeping a
  history of what I got wrong" (`EP-001/Q-005`), and the epic places that trail out of scope.
- Correcting a recorded income, or a move between envelopes. Only a spend is asked for; whether
  the other two need the same treatment is a question for `refine`, not an assumption to make
  here.
- How a correction appears in the monthly summary; that is WI-0003's to decide.

## Notes

- This item exists because of the stakeholder's answer to `EP-001/Q-005`: "I make mistakes weekly
  in the spreadsheet, so I need to correct or remove a spend I've already recorded." It was filed
  by `answer-questions` when that answer was consumed.
- That answer also replaced a line in the epic: `EP-001` previously placed editing and deleting a
  transaction out of scope altogether. That reading was the pipeline's, not the stakeholder's,
  and `EP-001/item.md` now records it as replaced.
- AC1 is the hard one and it is deliberately loose at `draft`: nothing in the record says how a
  person names the spend they mean — by an index in a listing, by a generated identifier, or by
  matching on envelope, amount and date. `refine` must pin that with the stakeholder before this
  item can be Ready.
