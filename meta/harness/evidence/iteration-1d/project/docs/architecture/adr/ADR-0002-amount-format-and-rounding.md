---
title: Amounts are plain two-decimal numbers, and the payer absorbs the rounding remainder
version: 1
status: current
updated: 2026-08-22T01:55:49Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0002 — Amounts are plain two-decimal numbers, and the payer absorbs the rounding remainder

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** —

## Context

`refine` could not make WI-0001 Ready because AC3 said "an amount" and nothing more
[src: WI-0001/Q-002]. Two facts were missing, and both have to be settled before anyone can write
a test: what an amount may look like when it is typed, and what happens to the leftover minor
unit when a shared amount does not divide evenly among its sharers.

The stakeholder answered `Q-002` in two halves:

> "Format — whatever's easiest to type, I don't need symbols or commas. Who eats the odd cent —
> not sure yet, go ahead anyway, we'll decide later."

The first half is a decision: it selects the question's option A — a plain decimal, no currency
symbol, no thousands separator. The second half is an explicit delegation. The stakeholder did
not decline to have a rule; they declined to pick one and told the architect to proceed. That is
the case `answer-questions` exists for, so this ADR picks it rather than re-escalating: effort is
not an escalation condition, and none of the four conditions in `spec/question.md` §4 applies —
intent was stated (proceed), the choice is reversible (see Consequences), and it contradicts
nothing recorded.

Two other recorded decisions bear on this one. `Q-001` settled that a shared expense is split
**equally** among its sharers [src: WI-0001/Q-001], which is what makes a remainder possible at
all. `ADR-0001` settled that a repayment is its own record with a single payer and a single payee
[src: ADR-0001], so a repayment never divides and this rule does not reach it.

## Options considered

On what an amount may look like when typed:

- **A — a plain decimal number, at most two decimal places, no symbol, no thousands separator.**
  `12.5` and `12.50` both mean twelve-fifty. Cost: a bank export carrying a symbol or a comma has
  to be normalised by the importer rather than accepted here. Risk: low; one rule, and every
  rejection case is decidable.
- **B — also accept a leading currency symbol and thousands separators, and normalise them.**
  Cost: a longer list of accepted forms in the one place a person types an amount. Risk: the
  importer and the hand-entry command drift into accepting different sets of strings, and the
  difference is invisible until a real file is imported.

On the leftover minor unit when an equal split does not divide evenly:

- **C — the payer absorbs it.** €10 shared by three: two sharers owe €3.33, the payer carries
  €3.34. Cost: the payer is out at most a few cents per expense. Risk: low, and it is what people
  do informally anyway.
- **D — spread the extra units over the sharers in a fixed order** (alphabetical, say). Cost: the
  report has to explain why one person owes a cent more. Risk: the amount someone owes depends on
  their name, which reads as a bug the first time it is seen.
- **E — refuse an amount that does not divide evenly.** Cost: none to build. Risk: the tool
  refuses to record a real €10 pizza split three ways, which defeats the purpose. Listed to be
  rejected.

## Decision

**A and C.**

**A.** An amount is a plain decimal number with at most two decimal places, no currency symbol
and no thousands separator. `12`, `12.5` and `12.50` are accepted and all mean twelve euros
fifty. `€12.50`, `1,234.56`, `12.505`, `0`, a negative number and any non-numeric string are
refused with a message on stderr and a non-zero exit code. This is the stakeholder's choice, not
the architect's.

**C.** When an equal split leaves a remainder, the **payer** absorbs it. Stated so that code can
be checked against it: each non-payer sharer owes the total divided by the number of sharers,
rounded **down** to the minor unit; the payer's own share is the total minus the sum of the other
sharers' shares. The consequence is a property WI-0002's report can be tested against — the sum
of every sharer's share equals the recorded total exactly, for every expense, with no minor unit
invented or lost.

Which command applies the rule is not fixed here. WI-0001 records the total and the set of
sharers; the per-person share is arithmetic performed where the debts are computed, which is
WI-0002 [src: WI-0002 AC2]. This ADR fixes the rule, not its location.

## Consequences

- WI-0001's AC3 can now state exactly which strings are accepted and which are refused, which is
  what `refine` needs for Definition of Ready criterion R4 [src: WI-0001 AC3].
- WI-0002's report has a checkable balance property rather than a rounding convention nobody
  wrote down. Its `## Notes` records this rule as settled input [src: WI-0002].
- WI-0003 inherits an obligation: a bank export that writes amounts with a symbol, a comma or a
  trailing minus must be normalised into form A by the importer, because this ADR does not widen
  what the hand-entry command accepts [src: WI-0003 AC1].
- **Reversibility: high.** The store holds the expense total and its sharers; it does not hold
  per-person shares, so changing the remainder rule later changes a computation and rewrites no
  data. The amount *format* is a little stickier — widening it (A → B) is safe, narrowing it
  after data exists is not — but widening is the direction anyone would want. The stakeholder
  said "we'll decide later", and later remains cheap; that is the fact this section exists to
  record.
- The stakeholder has not seen this rule. If the odd cent matters to them, `Q-002`'s deferral is
  the place a later question should cite.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T01:55:49Z | answer-questions | WI-0001 | First version |
