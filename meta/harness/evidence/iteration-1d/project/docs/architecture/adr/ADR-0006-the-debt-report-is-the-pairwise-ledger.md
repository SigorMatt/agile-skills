---
title: The debt report is the pairwise ledger, not a minimised settlement
version: 1
status: current
updated: 2026-08-22T02:48:51Z
updated-by: answer-questions
updated-for: WI-0002
---

# ADR-0006 — The debt report is the pairwise ledger, not a minimised settlement

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** the stakeholder, answering `WI-0002/Q-001`; recorded by answer-questions
  (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0002 is the item that answers "who owes whom". `refine` could not make it Ready because AC1
said the command prints "a set of debts" without saying **which** set, and five of the item's six
criteria — AC1, AC2, AC4, AC5 and AC6 — mean different things depending on the answer
[src: WI-0002/Q-001]. `intake` had already recorded the gap rather than guessing it
[src: WI-0002].

Two readings are both correct and print different lines from the same data:

- the **pairwise** ledger, where everything one person owes another is summed across all
  expenses and repayments between those two people, and a line is printed per non-zero pair;
- the **minimised** settlement, where each person's net position is computed first and the fewest
  transfers that bring everyone to zero are printed.

`refine` recommended the minimised settlement, on the grounds that the epic's goal is settling up
and fewer transfers is less money changing hands. It did not act on that recommendation, because
the choice depends on intent no document records — condition 1 of `spec/question.md` §4 — and put
it to the stakeholder with a worked three-person example.

## Options considered

- **A — the pairwise ledger.** Cost: can ask for more payments than are strictly necessary, and
  can print a circle (Ana owes Ben, Ben owes Cara, Cara owes Ana) which reads oddly when one
  transfer would have settled the group. Benefit: every printed line traces back to expenses the
  two named people actually shared, so any line can be justified against the expense list.
- **B — the minimised settlement.** Cost: a printed line need not correspond to any expense the
  two named people shared — in the worked example, Cara's 16.00 to Ana silently carries the 6.00
  she owes Ben for a taxi, and nothing in the output says so. Benefit: fewest transfers, never a
  circle.
- **C — one un-netted line per expense.** Rejected in the question as filed: that is the expense
  list from WI-0001 with per-row arithmetic, not an answer to "who owes whom", and it grows
  without bound.

## Decision

**A — the pairwise ledger.** The stakeholder chose it and gave the reason:

> "A — I want the pairwise breakdown. If the number ever gets questioned I want it to trace
> straight back to what those two people actually shared, not to some clever routing through
> somebody else's taxi. Fewer transfers doesn't matter as much as nobody being able to argue
> about a line." [src: WI-0002/Q-001]

Concretely, the report is computed as follows.

1. For each expense, the payer is owed, by each other sharer, that sharer's share — the total
   divided by the number of sharers, rounded down to the minor unit, with the payer absorbing the
   remainder [src: ADR-0002; ADR-0004]. A sharer who is also the payer owes nothing.
2. For each ordered pair of people, the amounts one owes the other are summed, in integer minor
   units [src: ADR-0004], across every expense.
3. Each repayment from A to B reduces what A owes B by its amount [src: ADR-0001].
4. The two directions of a pair are netted against each other, so at most one line is printed per
   pair, in the direction of the non-zero remainder. A pair whose net is zero produces no line
   [src: WI-0002].
5. Lines are ordered by debtor name, then creditor name, under WI-0001 AC1's matching rule —
   trimmed, ignoring case [src: WI-0002].

Steps 2 and 3 are what makes this the *pairwise* report: no amount is ever moved between pairs.
A person's net position across the whole group is therefore the sum of their pairwise lines, but
it is never used to reduce the number of lines printed.

## Consequences

- **A circle may be printed, and that is correct output, not a defect.** A ⟶ B ⟶ C ⟶ A can appear
  and no skill may "fix" it. `verify` should treat a circular case as expected behaviour.
- **A repayment between two people who share no expense prints a debt the other way round.** That
  case was recorded as unsettled in WI-0002's R10 table pending this answer; under A it is now
  settled — if Ana repays Ben 5.00 and they share nothing, the report prints `Ben owes Ana 5.00`.
  This follows from step 3 applied to a pair whose expense total is zero, and is consistent with
  AC5 as written.
- **AC2's balance property is per pair and in total.** The printed amounts account for every
  recorded minor unit exactly: summing a person's printed lines, signed by direction, gives their
  net position [src: WI-0002]. Integer minor units make this an equality,
  not a tolerance [src: ADR-0004].
- **The output can be longer than the minimised form**, up to one line per pair of people. For a
  friend group this is small, and the stakeholder has accepted the trade explicitly.
- **Reversibility.** Adding a minimised view later is additive — the same pairwise data, summed
  per person and re-routed — and would be a new command or flag, not a change to this one. No
  stored data depends on this decision; it is a reporting rule only. Reversing it *silently*,
  however, would change every printed line, so it is recorded here rather than left in a plan.
- WI-0002 returns to `draft`; the next `refine` execution owns the Definition of Ready verdict
  and may sharpen AC2, AC4, AC5 and AC6 against this decision.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T02:48:51Z | answer-questions | WI-0002 | Created, recording the stakeholder's answer to `WI-0002/Q-001`. |
