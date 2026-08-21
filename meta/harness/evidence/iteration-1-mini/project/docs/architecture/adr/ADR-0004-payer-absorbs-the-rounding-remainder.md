---
title: The payer absorbs the rounding remainder; money is integer minor units
version: 1
status: current
updated: 2026-08-21T02:35:00Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0004 — The payer absorbs the rounding remainder; money is integer minor units

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** answer-questions (architect), for WI-0003
- **Supersedes:** —

## Context

`WI-0003/Q-002` asked who absorbs the remainder when an amount does not divide evenly among its
sharers, and whether the tool should ever print a fraction of a penny. The stakeholder answered:
*"Not sure yet — go ahead anyway, we'll decide later."*

That is a delegation with a deadline attached to it, and both halves are taken seriously: the
decision is made here so nothing is blocked, and it is recorded in a form that can be changed
cheaply when they do decide. It cannot simply be left open — `WI-0003` AC3 requires that the
printed amounts net to zero **to the last minor unit**, and `EP-001` carries the same as a
success measure. A remainder rule is what makes that criterion satisfiable at all: `10.00` shared
by three people cannot be divided into three equal printable amounts, so somebody's figure must
differ by a penny, and the only question is whose.

Related and already decided: `WI-0002/Q-003` established that input amounts allow at most two
decimal places and are **never silently rounded** (*"I'd rather know than have it change my
number without telling me"*). A tool that refuses to round the user's input and then prints
figures that do not add up would be inconsistent in exactly the way that erodes trust in it,
which is what `EP-001/Q-005` — *"nobody argues about it"* — is about.

## Options considered

- **A — The payer absorbs the remainder; every figure prints to two decimal places.**
  Cost: the person who was already out of pocket carries up to one minor unit per expense.
  Risk: low, and roughly self-cancelling over many expenses because the payer changes. Explains
  in one sentence at a table.
- **B — The remainder is spread among the sharers in name order, first sharers taking the extra
  minor unit.**
  Cost: a rule that is harder to say out loud, and Alice is a penny worse off forever.
  Risk: fairer than A when one person always pays, which is a group the stakeholder has not
  described. Costs a stable ordering the whole calculation then depends on.
- **C — Keep exact fractions internally and round only when printing.**
  Cost: none up front.
  Risk: two printed figures can then fail to sum to a third, which is precisely what `WI-0003`
  AC3 forbids. Recorded so the option is on the record; not viable.

## Decision

1. **All money is held and computed as an integer number of minor units** (pence). Conversion
   from and to the two-decimal text form happens only at the boundaries — parsing input and
   formatting output. No binary float ever holds an amount: `12.10` is not representable as one,
   and AC3's exactness must not depend on luck. This binds `WI-0002` and `WI-0001`'s store as
   well as `WI-0003`.
2. **Splitting rule.** For an expense of `A` minor units shared by `n` people, every sharer
   **other than the payer** is charged `A // n` (integer floor division). The payer is credited
   with exactly the total charged to the others, so the payer carries whatever `A` minus that
   total comes to.
   - Payer among the sharers: `A = 1000`, `n = 3` → the two others owe `333` each, the payer's own
     share is `1000 − 666 = 334`.
   - Payer not among the sharers: `A = 1000`, `n = 3` → the three sharers owe `333` each and the
     payer, out of pocket `1000`, is owed `999`, absorbing the odd penny.

   One sentence covers both: **the payer absorbs the remainder**, which is option A.
3. **Every person's net position is the sum of integers**, so the balances net to zero by
   construction — for a single expense, `+charged_total` against `−(A // n)` per other sharer —
   and therefore across any number of expenses. `WI-0003` AC3 becomes a property of the
   arithmetic rather than something to be checked case by case.
4. **Output is always exactly two decimal places**, formatted from the integer. No figure is ever
   printed with a fraction of a minor unit, and no figure is ever rounded at print time, because
   there is nothing left to round.

## Consequences

- Easy: AC3 ("net to zero, to the last minor unit") holds by construction, and a test can assert
  it over randomly generated expenses rather than over hand-picked ones.
- Easy: explaining the rule to the group — "whoever paid carries the odd penny".
- Easy: switching to option B later. It is one function — the one that turns an expense into
  per-person deltas — plus this ADR and `WI-0003` AC6. Balances are recomputed from the stored
  expenses on every run, so nothing stored has to change and no migration is needed.
- Hard: nothing, materially. A group where the same person always pays will see that person carry
  a few pence over a trip; that is the case for option B, and it is why this stays cheap to
  reverse.
- **Reversibility: high**, and it stays high, because the remainder rule is applied at report time
  and never persisted. This is the reason it was safe to decide rather than escalate on
  *"we'll decide later"*: deciding later remains genuinely available.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:35:00Z | answer-questions | WI-0003 | First version, deciding WI-0003/Q-002 after the stakeholder deferred the choice |
