---
title: When the payer is not a sharer, an uneven split's remainder is owed by nobody
version: 1
status: current
updated: 2026-08-22T03:03:14Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0009 — When the payer is not a sharer, an uneven split's remainder is owed by nobody

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** — (refines `ADR-0002` and `ADR-0004`; supersedes neither)

## Context

An expense may be paid by someone who is not among its sharers: `add-expense --payer Ana
--shared-by Ben --shared-by Cara` is accepted, and `_resolve_sharers` does not add the payer to
the list [src: expenses/cli.py; WI-0001 AC3]. When such an expense also has a total that does not
divide evenly among its sharers, one minor unit or more is left over, and the record disagrees
with itself about where it goes.

- `ADR-0004` states the arithmetic: "When the payer is not among the sharers, the payer is owed
  `t` and each sharer owes `share`, with the `remainder` staying with the payer as an amount
  nobody owes them — the sum of what is owed is then `t - remainder`" [src: ADR-0004]. The two
  halves of that sentence do not agree: if each of `n` sharers owes `share`, the payer is owed
  `n × share`, which is `t - remainder`, not `t`.
- WI-0002's R10 table takes the first half — "the payer is owed the whole total, since they have
  no share of it" [src: WI-0002].
- WI-0002's AC3 asserts that every person's net position sums, across all people, to zero, and
  computes a person's net position from "the sum of P's shares of the expenses P shared in"
  minus "the sum of the totals of the expenses P paid" [src: WI-0002 AC3].

Those three cannot all hold. If a non-sharing payer is owed the whole total, then the sharers'
shares sum to `t` and at least one of them is paying a rounded-up share, which is option D that
`ADR-0002` rejected [src: ADR-0002]. If instead they owe `share` each, AC3's net positions only
sum to zero when the payer's "share" of that expense is counted as the leftover `remainder` —
which is what "the payer absorbs the remainder" has meant since `ADR-0002`.

This is not a question for the stakeholder: it is arithmetic, the intent behind it was already
recorded, and the sums involved are a fraction of a cent per person per expense. `ADR-0002`'s
delegation ("go ahead anyway, we'll decide later") covers this case explicitly
[src: WI-0001/Q-002].

## Options considered

- **A — the remainder stays with the payer even when they are not a sharer.** Each sharer owes
  `share = t // n`; the payer is owed `n × share`; the leftover `t - n × share` is money the
  payer spent that nobody owes them back. Cost: a non-sharing payer is out at most `n - 1` minor
  units on an expense they did not benefit from, which is harder to justify in words than the
  same rule applied to a payer who did share. Benefit: one rule for every expense, no dependence
  on whether the payer is in the sharer list, and AC3's "these net positions sum to zero" becomes
  true when "P's share" of a paid-but-not-shared expense is read as the leftover.
- **B — the sharers absorb the remainder, so the payer is owed exactly `t`.** The extra minor
  units go to sharers in some fixed order. Cost: this is `ADR-0002`'s rejected option D
  reintroduced through a side door, for one case only, so the amount someone owes starts
  depending on their name [src: ADR-0002]. Risk: two remainder rules in one report, selected by
  whether the payer happens to appear in the sharer list — the kind of rule nobody can predict
  from the output.
- **C — refuse to record an expense whose payer does not share and whose total does not divide
  evenly.** Cost: none to build. Risk: WI-0001 already accepts these expenses and data may exist;
  refusing at report time means a recorded ledger has no report at all. Listed to be rejected.

## Decision

**A.** For every expense, without exception, each sharer other than the payer owes
`total // len(sharers)` minor units, and nothing else is owed to anybody for that expense
[src: ADR-0002; ADR-0004]. Whether the payer is among the sharers changes which people appear in
that set; it changes no arithmetic.

Consequently, **AC3's phrase "the sum of P's shares of the expenses P shared in" is read as "the
sum of P's shares under `ADR-0002`'s rule", where a payer's own share is `total` minus the sum of
every other sharer's share — whether or not the payer is listed as a sharer** [src: WI-0002 AC3].
Under that reading AC3's closing assertion, that the net positions sum to zero, holds for every
ledger. Under the other reading it fails on exactly the expenses this ADR is about, so the
reading is forced by the criterion rather than chosen against it.

WI-0002's R10 row saying "the payer is owed the whole total" is right whenever the total divides
evenly and off by the remainder when it does not [src: WI-0002]. It is a coverage note under
`## Notes`, not an acceptance criterion, so nothing in it is being changed here; this ADR is
where a reader who trips over it finds out which document governs.

## Consequences

- `verify` has a stated answer for the case it would otherwise have to invent: a ledger of Ana,
  Ben and Cara with `--payer Ana --amount 10.00 --shared-by Ben --shared-by Cara` reports
  `Ben owes Ana 5.00` and `Cara owes Ana 5.00`; the same ledger with `--amount 10.01` reports
  `5.00` from each, and the odd cent is Ana's [src: WI-0002 AC3].
- The rule that `debts()` implements has no branch on payer membership, which is one fewer place
  for the two cases to drift apart.
- WI-0003's importer can create expenses whose payer is not a sharer, and inherits this rule
  without a decision of its own [src: WI-0003].
- **Reversibility: high.** Nothing is stored; per-person shares are computed at report time from
  a total and a sharer list [src: WI-0001 AC5]. Changing to option B later changes one function
  and rewrites no data. What it would also change is every printed line for an affected expense,
  which is why the rule is written down rather than left in a plan step.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T03:03:14Z | plan | WI-0002 | First version |
