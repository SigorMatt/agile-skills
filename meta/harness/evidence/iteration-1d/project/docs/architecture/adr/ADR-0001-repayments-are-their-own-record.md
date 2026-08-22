---
title: Repayments are their own kind of record, added to WI-0001 and WI-0002
version: 1
status: current
updated: 2026-08-22T01:44:16Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — Repayments are their own kind of record, added to WI-0001 and WI-0002

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

`intake` filed `EP-001/Q-003` because the record was silent on what happens after the tool says
Ben owes €40 and Ben actually pays. The epic, the vision and all three work items had been
written with repayments held out of scope *pending that answer*, so nothing downstream depended
on a guess.

The stakeholder answered: *"Hadn't thought about it, but yes — let us log that someone paid, so
the report doesn't go stale. Doesn't need to be fancy, whatever's simplest to build."* That is
recorded intent, not an inference, and it settles the scope question. It leaves two things it
does not settle, and this ADR settles them:

1. **How a repayment is modelled.** A repayment is not an expense — nobody shared it, and it has
   a payee rather than a set of sharers.
2. **Where the work goes.** `Q-003`'s option A described "a fourth work item". Two constraints
   bear on that. First, `pipeline.yaml` and `spec/ids-and-statuses.md` §4 make `— → draft` legal
   only for the actor `intake`, so `answer-questions` cannot create a work item at all; the only
   sanctioned routes to a new item are `intake` (from a `tracker/requests/` request the
   stakeholder authors, which a skill may not author on their behalf per `spec/request.md` §2) or
   `verify` filing a bug. Second, WI-0001 and WI-0002 are both still at `draft`, so their
   acceptance criteria are not yet frozen and may legitimately be amended.

## Options considered

- **A — a repayment is a negative expense**, paid by the payee and shared by the payer alone.
  Cost: no new record type, no new storage shape. Risk: the expense list becomes untruthful —
  `list expenses` would show entries nobody spent — and every consumer of the expense list has to
  learn a sign convention. It also makes "what did we actually spend on the trip?" unanswerable,
  which is a question this data is otherwise well shaped for.
- **B — a repayment is its own record type**, stored alongside expenses, with a from, a to and an
  amount; the balance report nets expenses and repayments together. Cost: a second record kind in
  the store and a second listing command. Risk: slightly more storage surface to design in
  WI-0001, before there is any code.
- **C — defer the whole thing to a fourth work item**, created later by some other route. Cost: no
  work now. Risk: no route exists that this skill may take (see Context), so "later" means "when
  something else happens to create it" — which is how an accepted scope change silently fails to
  happen. It would also mean WI-0001 designs its storage without knowing a second record type is
  coming, which is exactly the retrofit `Q-003` was filed to avoid.

## Decision

**B.** A repayment is a first-class record with a payer, a payee and an amount, stored in the
same place as expenses and never represented as an expense. It is recorded and persisted by
WI-0001 (new AC7 and AC8) and consumed by WI-0002 (new AC5 and AC6), rather than by a fourth work
item.

Concretely, and checkable against code: the store holds two collections, not one; `list expenses`
never shows a repayment; the who-owes-whom computation is a fold over expenses *and* repayments;
and a repayment from A to B reduces A's debt to B by exactly its amount.

## Consequences

- WI-0001's storage design must accommodate two record kinds from the outset. That is the point:
  it is cheap now and expensive after there is data on disk.
- WI-0002's report is a net position over two inputs. AC2's balance property (total owed equals
  total owing) must hold with repayments present, which is why it was restated in AC5 rather than
  left implied.
- The epic gains scope without gaining an item. A reader scanning the board will not see
  "repayments" as a row; they will find it in EP-001's scope, in this ADR, and in the four new
  criteria. That is a real cost of the decision and is recorded here deliberately.
- **Reversibility: high, for now.** Both items are at `draft` and no code exists. Removing
  repayments means deleting four criteria and superseding this ADR. Once WI-0001 is implemented
  and a store format is on disk, reversing becomes a data migration and the decision should be
  treated as fixed.
- **A gap in the methodology, recorded because it shaped this decision:** an architect answering a
  scope question may widen an epic but cannot open the work item that widening implies, and the
  stakeholder-authored `tracker/requests/` channel is not one a skill may write into. Folding into
  draft items worked here only because both items happened to still be at `draft`. Had they been
  `ready` or later, this answer would have had nowhere to go.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T01:44:16Z | answer-questions | EP-001 | First version |
