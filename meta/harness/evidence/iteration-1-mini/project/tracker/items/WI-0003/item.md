---
id: WI-0003
type: work-item
title: Show who owes whom
status: ready
priority: high
epic: EP-001
created: "2026-08-21T02:03:44Z"
depends-on:
  - WI-0002
relates-to:
  - WI-0001
updated: "2026-08-21T03:55:28Z"
---

## Story

As a member of the friend group, I want to ask at any point who owes whom, so that we can settle
up without anybody recomputing the arithmetic by hand or arguing about it.

## Acceptance criteria

- [ ] AC1 — **one** command, run over the expenses already recorded, prints the payments that
      settle the group: for each, who pays, whom they pay, and how much. No second command and no
      arithmetic by hand. (WI-0003/Q-001, EP-001/Q-005.)
- [ ] AC2 — for a worked example the stakeholder can check by hand — Alice pays 30 for a dinner
      shared by Alice, Bob and Carol — the payments the output lists are exactly *Bob pays Alice
      10.00* and *Carol pays Alice 10.00*: two payments, no third, and no other pair of people.
      *"Nothing else"* is scoped to the payments deliberately, because AC5 requires a net-position
      summary alongside them and the two criteria would otherwise contradict each other; the
      original wording predates AC5 and was corrected by `refine` rather than left for `verify` to
      discover.
- [ ] AC3 — the amounts printed net to zero: what is owed and what is owing are equal to the last
      minor unit
- [ ] AC4 — running the command with no expenses recorded succeeds, exits zero, and says that
      nobody owes anybody. The same is true when expenses exist but every net position is zero.
- [ ] AC5 — the same output shows, alongside the payments, each person's net position — how much
      they are up or down overall — so that a reader can reconcile the payments against what they
      remember paying. (WI-0003/Q-001, EP-001/Q-005.) Two details are fixed so this is decidable:
      **every person currently in the group appears**, including anyone who has neither paid nor
      shared anything, shown at `0.00` rather than omitted — a reader who believes they paid for
      something and finds themselves at zero has learnt exactly what AC5 exists to tell them; and
      **the direction is stated in words**, not by the sign of a number alone, so that "owed" and
      "owes" cannot be read the wrong way round. For AC2's worked example the summary shows Alice
      owed 20.00, Bob owing 10.00 and Carol owing 10.00. Both details are assumed by `refine` from
      AC5's own stated purpose, not stated by the stakeholder.
- [ ] AC6 — when an amount does not divide evenly among its sharers, **the payer absorbs the
      remainder**: 10.00 shared by three charges the two others 3.33 each and leaves 3.34 with the
      person who paid. Every figure is printed to exactly two decimal places, and no fraction of a
      minor unit is ever printed. (WI-0003/Q-002, ADR-0004.)
- [ ] AC7 — the number of payments printed is at most one fewer than the number of people with a
      non-zero net position, and running the command twice over an unchanged store prints
      identical output. (ADR-0005.)
- [ ] AC8 — no failure in this item's command prints a Python traceback. Every failure prints a
      message on **stderr** naming what was wrong and exits non-zero; the command never writes to
      the store at all, so its bytes are unchanged after every invocation, successful or not —
      checked by comparing the file before and after. A store that exists but cannot be read or
      parsed is fatal, naming the path, per `ADR-0002` decision 6. This is WI-0001 AC8 and WI-0002
      AC10 restated for this item's command, because each of those scopes itself to its own
      commands by design and EP-001's fourth success measure is about the whole tool.
- [ ] AC9 — when the store holds an expense naming a payer or a sharer who is **not** in the
      group, the command fails, naming the offending expense and the unknown person, exits
      non-zero and prints no report. It does not silently include that person, and it does not
      silently drop the expense. This state is unreachable through the tool — WI-0002 AC3 refuses
      to record such an expense — so it is only reachable by hand-editing the store, which is
      exactly the class `ADR-0002` decision 6 makes fatal rather than best-effort. Reporting a
      settlement that names somebody who is not in the group would produce payments nobody can
      act on. Assumed by `refine`; it is the referential half of the structural check WI-0002 AC10
      adds to `store.load()`, and neither of the two earlier items owns it.

## Out of scope

- Recording a repayment between two people so that a debt is cleared. Deferred to a later epic by
  the stakeholder's answer to EP-001/Q-002 — *"Leave settling up out of this first version"* — not
  refused. See the Notes: this item must leave a seam for it.
- Any history of past settlements or per-period reports.
- Exporting the result to a file or another format.
- Claiming, anywhere in the output, the help text or the criteria, that the payments are the
  *smallest possible* set. The tool does not compute that; see ADR-0005 decision 3.

## Notes

Both of this item's questions have been answered by the stakeholder:

- The report prints the **payments** — who pays whom — with each person's net position alongside
  (WI-0003/Q-001, option D). Their words: *"I want the actual payments — who pays whom — not just
  a list of who's up and down."*
- The remainder rule was deferred to the architect — *"Not sure yet — go ahead anyway, we'll
  decide later"* — and decided as **the payer absorbs it**
  (`docs/architecture/adr/ADR-0004-payer-absorbs-the-rounding-remainder.md`). That ADR is
  deliberately cheap to reverse: the rule is applied at report time and never persisted, so
  changing it later is one function and a re-run, with no migration. If the stakeholder decides
  they want it spread among the sharers instead, that is still genuinely available.

**How the payments are computed** is `docs/architecture/adr/ADR-0005-settlement-by-greedy-largest-
first-matching.md`: net positions first, then repeatedly match the largest debtor with the largest
creditor, ties broken by name. Note what AC7 does *and does not* claim. The original question
asked about "the smallest set of payments"; minimising transfers is NP-hard, so the tool does not
do it and the item must not say it does. What is claimed — at most `k − 1` payments for `k` people
with a non-zero net, and identical output on a re-run — is decidable by someone with a terminal,
which "smallest" is not.

**Leave a seam for settling up.** EP-001/Q-002's accepted option promised this item would be built
knowing repayments are coming. Concretely: computing net positions must be a separate, separately
testable stage from turning those nets into payments, so that a repayment can later be applied as
one more transfer against the nets without the settlement code changing. Computing payments
straight from expense rows would satisfy every criterion here and quietly break that promise.

Money is integer minor units throughout (ADR-0004 decision 1) — never a binary float — which is
what makes AC3 true by construction rather than by luck.

**`depends-on: WI-0002` is now recorded in the frontmatter**, where the first pass had only
`relates-to`. The reason is not tidiness: this item reads expense records, and what an expense
record *is* has not been designed yet — WI-0002's `plan` decides it. Left as a `relates-to`, the
orchestrator would happily dispatch `plan` on this item the moment it turned `ready`, and that
plan would be written against a data shape that does not exist. With the dependency recorded,
`pipeline.yaml`'s runnable rule holds this item back until WI-0002 is `done`, which is the
sequencing the first pass argued for informally via the priority tie-break. Ready and runnable are
different things, and this item is meant to be the first and not yet the second. WI-0001 is
already `done`, so it needs no dependency of its own.

Python 3.9+, standard library only, per ADR-0001.

## Deliberately unconstrained

Recorded per the Definition of Ready **R10**, so that these are open questions someone can find
rather than gaps nobody knows exist. Each names who left it open, following WI-0001's practice.

- **The exact wording and layout of the report.** AC1, AC2, AC5 and AC6 pin the payments, the
  pairs, the figures, who appears and that direction is stated in words — which is what can be got
  wrong. Whether the summary comes above or below the payments, what the headings say, and whether
  anything is aligned into columns are `plan`'s. Left open by `refine` at the first pass and still
  open deliberately.
- **The command's name.** `ADR-0006` decision 2 already spells it `settle` for the whole tool.
  AC1 constrains only that there is exactly **one** command and what it prints, so it stays true
  whatever the ADR settles on.
- **How large the group or the expense list may get.** Nothing sets a limit and no criterion
  depends on one. `ADR-0005`'s greedy matching is not sensitive to size at any scale a friend
  group reaches. Left open by `refine`, on the same reasoning WI-0001 and WI-0002 used.
- **Whether the report can be filtered** — by date range, by person, by description. Nobody has
  asked for it and no criterion mentions it; `## Out of scope` already excludes per-period
  reports, which is the nearest thing. Named here so that the absence is visible rather than
  assumed.

**Combinations that are specified rather than left open**, listed so R10's check is auditable:

- *An uneven division* — AC6, via `ADR-0004`.
- *A person in the group who has neither paid nor shared anything* — AC5: they appear at `0.00`.
  This is the combination the first pass named as `refine`'s to settle once the output form was
  fixed. The form is now fixed, so it is settled here.
- *Expenses exist but every net position is zero* — AC4, second sentence.
- *No expenses at all* — AC4, first sentence.
- *Exactly one person with a non-zero net* — arithmetically impossible, because the nets sum to
  zero. AC7's `k − 1` bound therefore never has to describe it.
- *Two people who each owe the other* — netted before any payment is computed, per `ADR-0005`'s
  net-positions-first stage; the result is a single payment or none.
- *A tie between two debtors or two creditors of equal size* — `ADR-0005` breaks it by name, which
  is also what makes AC7's "identical output on a re-run" achievable.
- *A damaged or unreadable store* — AC8, via `ADR-0002` decision 6.
- *A hand-edited store naming somebody outside the group* — AC9.
