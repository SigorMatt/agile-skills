---
title: An indivisible remainder goes to the first-named sharers
version: 1
status: current
updated: 2026-08-26T23:52:03Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — An indivisible remainder goes to the first-named sharers

- **Status:** accepted
- **Date:** 2026-08-26
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder settled that an expense divides equally between the people named as its sharers —
*"Equal split, keep it simple"* [src: WI-0001/Q-001]. An equal split does not always come out
even: 10.00 between three people is 333 minor units each with one left over
[src: ADR-0002]. The shares must still sum to exactly the amount [src: WI-0001 AC2], so that
minor unit has to go somewhere.

`refine` routed this here rather than to the stakeholder, on the grounds that nobody would have a
preference between equally fair answers, and placed exactly one constraint on it: the rule must
be deterministic, so that the same recorded data always produces the same shares
[src: tracker/items/WI-0001/item.md]. AC8 is that constraint made checkable — the same commands
run twice against a fresh store must print byte-identical output [src: WI-0001 AC8] — and
WI-0002's own AC4 depends on it too [src: WI-0002 AC4].

## Options considered

- **A — The first `r` sharers in the order they were named each take one extra minor unit.**
  Cost: two lines. Risk: the order is the one the person typed, so it must be stored with the
  expense or the shares cannot be recomputed. This plan stores the computed shares anyway
  [src: ADR-0001].
- **B — The payer absorbs the whole remainder.** Cost: two lines. Risk: it is not a rounding rule
  but a policy — it says the person who paid should be out of pocket by up to a unit per expense,
  systematically, in every expense they pay for. That is a judgement the stakeholder was never
  asked for.
- **C — The sharers sorted alphabetically take the extra units.** Cost: a sort. Risk: `Ana` pays
  the extra unit on every uneven expense in the dataset, for ever, because her name sorts first.
  A rule that is deterministic and also systematically biased is worse than one that is merely
  deterministic.
- **D — Round each share to the nearest unit and let the total drift.** Excluded: it contradicts
  AC2 [src: WI-0001 AC2].

## Decision

A share is `amount_minor // n` for each of the `n` sharers, and the remaining
`amount_minor % n` minor units are given one each to the **first `r` sharers, in the order they
were named on the command line**.

So `--amount 10 --shared-by Ana,Ben,Cara` records `Ana: 334, Ben: 333, Cara: 333`, summing to
1000 [src: WI-0001 AC8].

The sharer order is stored with the expense, and the computed shares are stored alongside it
[src: ADR-0001], so the record says what each person owes rather than leaving it to be
recomputed by every reader — WI-0002 and WI-0003 both read these figures.

## Consequences

Easy: the sum is exact by construction, and it is explainable to a person in one sentence — the
people named first round up.

Hard: nothing yet. The bias is per-expense and follows the order the person typed rather than any
property of the people, so it does not accumulate against anyone in particular unless they always
type the same name first.

The shares are stored, which means an expense's shares and its amount could in principle
disagree if the file were hand-edited. That is a consequence of storing them, and it is accepted:
`store.py` recomputes nothing on read, so a hand-edited file is believed. EP-001's measures say a
person should never need to hand-edit the file [src: tracker/items/EP-001/item.md].

**Reversibility: high.** The rule is one function and it is not part of any acceptance criterion —
AC8 deliberately does not name which sharer takes the extra unit [src: WI-0001 AC8]. Changing it
would leave existing stored shares as they are, since they are already computed; only new
expenses would differ.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-26T23:52:03Z | plan | WI-0001 | First version |
