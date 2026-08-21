---
title: Settle by repeatedly matching the largest debtor with the largest creditor
version: 1
status: current
updated: 2026-08-21T02:35:30Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0005 — Settle by repeatedly matching the largest debtor with the largest creditor

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** answer-questions (architect), for WI-0003
- **Supersedes:** —

## Context

`WI-0003/Q-001` asked what the report should print. The stakeholder answered: *"I want the actual
payments — who pays whom — not just a list of who's up and down. A quick per-person summary
alongside it is fine too if that's easy, but the payments are what matters."* That is the
question's option **D** — a settlement, with net positions shown alongside — and `EP-001/Q-005`
independently reinforces both halves: *"one command tells us who pays whom and nobody argues
about it."*

What the stakeholder chose is the *shape* of the output. It does not say how the payments are
computed, and the phrase used in the question — "the **smallest** set of payments that settles the
group" — cannot be delivered literally. Minimising the number of transfers that clears a set of
balances is equivalent to a partition problem and is NP-hard; a tool that promised it would either
be wrong or would hang on a large group. An acceptance criterion must be decidable by someone with
a terminal, so `WI-0003` cannot say "smallest" and must say what it actually does.

There is a second constraint from `EP-001/Q-002`: settling up — recording that Bob actually paid
Alice — is deferred to a later epic, and the recommendation accepted there promised that WI-0003
would be built knowing it is coming. Whatever is decided here must leave a seam for it.

## Options considered

- **A — Greedy largest-first matching.** Compute every person's net position, then repeatedly take
  the largest debtor and the largest creditor and transfer the smaller of the two magnitudes,
  until every balance is zero.
  Cost: trivial to implement and to explain; sorting plus a loop.
  Risk: produces at most `k − 1` payments for `k` people with a non-zero net, which is not always
  the theoretical minimum. In a friend group — under ten people — the difference is at most a
  payment or two, and often none.
- **B — Exact minimisation by subset search.** Find genuinely minimal transfer sets.
  Cost: exponential; needs a cutoff and a fallback, so the tool has two code paths and the output
  depends on which one ran.
  Risk: unjustifiable for the problem size, and it makes the output non-obvious to predict, which
  works against *"nobody argues about it"*.
- **C — Pairwise debts, unnetted** (the original question's option C).
  Cost: none.
  Risk: rejected by the stakeholder — *"not just a list of who's up and down"* is a rejection of
  option B of that question, and unnetted pairwise debts are worse still, telling two friends to
  pay each other on the same evening.

## Decision

1. **Balances first.** Every expense is turned into per-person integer deltas by `ADR-0004`'s
   splitting rule, and summed into one net position per person. This intermediate step is
   deliberately a named, separately testable stage: it is the seam a future repayment (`EP-001/
   Q-002`) plugs into, as one more transfer applied to the same nets, without the settlement code
   changing at all.
2. **Then settle, greedily.** While any balance is non-zero: take the person with the most
   negative net (the largest debtor) and the person with the most positive net (the largest
   creditor), record a payment from the first to the second of `min(|debt|, credit|)`, and apply
   it to both. Ties are broken by name, ascending, so the output is deterministic and two runs
   over the same store print the same thing.
3. **At most `k − 1` payments** are produced, where `k` is the number of people with a non-zero
   net. Each iteration zeroes at least one person's balance. This is the claim `WI-0003` may make
   and a test may assert — **not** "the smallest possible set", which is not computed and must not
   be claimed anywhere in the item, the help text or the output.
4. **Both parts are printed by one command**, per `EP-001`'s "settling up after a trip takes one
   command": the payments, and each person's net position alongside them.
5. **Nobody owes anybody** is a first-class case: when every net is zero — including when there
   are no expenses at all — the command exits zero and says so.

## Consequences

- Easy: the output is short, actionable, and deterministic, so two people running the tool cannot
  get different answers and argue about that instead.
- Easy: adding repayments later. Decision 1 makes it an addition to the balance stage, not a
  change to the settlement stage.
- Easy: verifying. Two independent properties can be asserted over generated data — the payments
  applied to the nets zero them all out, and the payment count is at most `k − 1`.
- Hard: a group could occasionally settle in one fewer transfer than the tool suggests. This is
  accepted, and decision 3 exists so that the item never claims otherwise. Overclaiming here would
  be a defect a verifier could not falsify without solving an NP-hard problem.
- Hard: a payment does not correspond to any single expense — Carol may be told to pay Alice for a
  taxi Bob paid for. That is inherent to settling rather than a property of this algorithm, and it
  is exactly why decision 4 keeps the net positions on screen: they are what a sceptic reconciles
  against their own memory.
- **Reversibility: high.** The settlement stage consumes net positions and produces payments;
  replacing it changes one function and this ADR. Nothing about it is persisted.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:35:30Z | answer-questions | WI-0003 | First version; makes WI-0003/Q-001's chosen output shape decidable, and replaces the unachievable "smallest set of payments" wording |
