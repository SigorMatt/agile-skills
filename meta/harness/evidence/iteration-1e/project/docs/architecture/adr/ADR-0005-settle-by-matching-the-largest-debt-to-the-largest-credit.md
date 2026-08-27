---
title: Settle by matching the largest debt to the largest credit
version: 1
status: current
updated: 2026-08-27T00:28:48Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0005 — Settle by matching the largest debt to the largest credit

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

The stakeholder asked for a list of payments that settles the group rather than a table of who is
up and who is down — *"The list of payments that settles it — that's what actually saves us the
arguing after a trip."* [src: EP-001/Q-002]. A group can almost always be settled by more than one
equally valid set of payments, so a rule has to choose one, and the same recorded data has to
produce the same list every time [src: WI-0002 AC4].

That answer also said who owns this decision: the settlement rule "is not the stakeholder's to
decide; it is refinement's, and then `plan`'s" [src: EP-001/Q-002]. Refinement took the half it
owns and fixed the properties the output must have — every amount positive, nobody both paying
and receiving, a person with a zero position absent, at most one fewer payment than there are
people with a non-zero position, and the whole list settling the group exactly
[src: tracker/items/WI-0002/artifacts/refinement-qa.md]. What is left, and what this ADR decides,
is which of the settlements satisfying those properties is printed, and in what order.

The arithmetic underneath is already settled and is exact. An expense divides equally between its
named sharers [src: WI-0001/Q-001], the computed shares are stored as whole minor units
[src: ADR-0002; ADR-0001], and an indivisible remainder goes to the first-named sharers
[src: ADR-0003]. So each person's **position** — what they paid minus the shares recorded against
them — is a whole number of minor units, and across a dataset the positions sum to exactly zero.
No rounding arises in this decision, and none may be introduced by it.

## Options considered

- **A — Match the largest debt against the largest credit, repeatedly.** Take the person who owes
  most and the person who is owed most, transfer the smaller of the two amounts, and repeat until
  no debt is left. Cost: a sort per step, on a list the size of the group. Risk: two people can owe
  exactly the same amount, so the rule is not by itself deterministic and needs a stated tie-break.
- **B — Match debtors against creditors in the order the people were recorded.** Walk the debtors
  in `person add` order and pay each one off against the creditors in the same order. Cost:
  identical, and no tie-break is needed because the order is total already. Risk: the first line
  of the output is whoever happens to have been typed in first, so a reader gets no sense of
  which debts matter; and the list reorders itself when a person is added, because the recorded
  order is what drives it.
- **C — Compute the settlement with the fewest possible payments.** Find subsets of people whose
  positions cancel exactly and settle each subset on its own. Cost: the subset search is
  exponential in the size of the group, so it needs a cutoff and a fallback, which is two rules
  where one would do. Risk: a rule nobody can explain in a sentence, for a gain that is at most a
  line or two of output in a friend group. The properties refinement fixed already cap the list at
  one fewer payment than there are people with a non-zero position, which is the guarantee that
  matters [src: tracker/items/WI-0002/item.md].
- **D — Print every pairwise debt as its own payment.** Excluded: it contradicts the properties
  refinement fixed — the same person would both pay and receive — and it is the arithmetic the
  stakeholder said they wanted to stop doing [src: EP-001/Q-002].

A and B produce the same number of payments in every case, because both settle at least one
person completely at each step, so the choice between them is about which list is nicer to read
and not about how short it is.

## Decision

The settlement is computed by repeatedly matching the **largest debt against the largest credit**:

1. Compute each recorded person's position: the sum of the amounts of the expenses they paid,
   minus the sum of the shares recorded against them, in whole minor units.
2. Split the people whose position is not zero into debtors (negative) and creditors (positive).
   A person whose position is zero takes no part.
3. While both a debtor and a creditor remain, take the debtor owing the most and the creditor
   owed the most, record a payment from the debtor to the creditor of the smaller of the two
   amounts, and reduce both by it. At least one of the two reaches zero and leaves the pool.
4. **The tie-break, in both pools, is the order the people were recorded** — the order
   `person list` prints [src: WI-0001 AC1]. So of two people owing the same amount, the one added
   first pays first.
5. The payments print in the order they were generated, largest debt first.

This is option A with its tie-break made explicit, and both halves are load-bearing: step 3 is
what makes the list short, step 4 is what makes it the same list every time [src: WI-0002 AC4].

Worked against the item's own criteria, so the decision can be checked rather than believed. For
`Ana +20.00, Ben −10.00, Cara −10.00` the debtors tie, the recorded order breaks it, and the
result is `Ben pays Ana 10.00` then `Cara pays Ana 10.00` [src: WI-0002 AC1]. For
`Ana +16.66, Ben −1.33, Cara −9.33, Dan −6.00, Eve 0` the result is `Cara pays Ana 9.33`, then
`Dan pays Ana 6.00`, then `Ben pays Ana 1.33` — three payments, `Eve` absent [src: WI-0002 AC3].

## Consequences

Easy: the list is short, the largest debts are at the top where a person looking to settle up
wants them, and every amount is a whole number of minor units because it is always the smaller of
two whole numbers. Nothing here rounds, so nothing here can lose a unit [src: ADR-0002].

Hard: the payments follow from each person's overall position and not from who shared what with
whom, so the list can tell one person to pay another they never shared an expense with. That is
inherent to settling a group in few payments rather than unwinding every pairwise debt; it is
recorded on the item as a deliberate exclusion rather than left to be discovered
[src: tracker/items/WI-0002/item.md].

Also hard, and accepted: adding an expense can reshuffle the whole list rather than adding a line
to it, because the matching starts from the positions afresh each time. That is a property of any
rule that settles a group rather than tracking pairwise IOUs.

The loop terminates on any input, including a dataset whose positions do not sum to zero, because
each step removes at least one person from a pool and the loop stops when either pool is empty.
Positions can only fail to sum to zero if the file was hand-edited, which the product's success
measures say nobody should need to do [src: tracker/items/EP-001/item.md].

**Reversibility: high.** The rule is one function in one module and no stored data depends on it:
the settlement is computed on every run and never written down [src: WI-0002 AC5]. Replacing it
with option B or C would change the printed order and possibly the pairings, but would leave every
recorded expense untouched and would not need a migration. The acceptance criteria do pin the
exact expected output for two datasets [src: WI-0002 AC1; WI-0002 AC3], so a future change of rule
has to come with a change to those criteria — which is the visible cost of pinning them, and it is
the right way round: the criteria are what make the rule checkable at all.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T00:28:48Z | plan | WI-0002 | First version |
