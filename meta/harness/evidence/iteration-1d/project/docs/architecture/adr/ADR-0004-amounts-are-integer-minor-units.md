---
title: Amounts are integer minor units everywhere, and floats never touch money
version: 1
status: current
updated: 2026-08-22T02:06:34Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — Amounts are integer minor units everywhere, and floats never touch money

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`ADR-0002` fixed what an amount looks like when typed — digits, at most two decimal places, no
symbol, no separator — and fixed that an equal split's remainder goes to the payer, computed as
"each non-payer sharer owes the total divided by the number of sharers, rounded down to the minor
unit; the payer's own share is the total minus the sum of the others" [src: ADR-0002]. It did not
say what a program holds while doing that.

The choice matters more here than it usually does, because the property WI-0002 must satisfy is
exact: the shares of one expense sum to its recorded total, with no minor unit invented or lost
[src: WI-0002 AC2]. A representation that cannot express that exactly makes the acceptance
criterion unprovable rather than merely hard.

`WI-0001` AC6 also demands that `12.5` and `12.50` produce the same stored amount, which is a
statement about normalisation on the way in.

## Options considered

- **A — integer minor units (cents) in memory and on disk.** `12.50` is `1250`. Cost: parsing and
  formatting are explicit, at exactly two places — the two functions named in the decision below
  [src: ADR-0002]. Risk: an integer overflow is not reachable in
  Python. Benefit: division with `divmod` gives the floor and the remainder in one operation,
  which is precisely `ADR-0002`'s rule; equality and summation are exact by construction.
- **B — `decimal.Decimal`, serialised as a string.** Cost: every arithmetic site must be careful
  about context and rounding mode, and the JSON carries `"12.50"` which invites a reader to
  compare it as a string. Risk: `Decimal("12.5") != Decimal("12.50")` is false for `==` but the
  two serialise differently, so AC6's "mean the same amount" becomes a normalisation rule anyway
  — the same work as A, plus a type.
- **C — `float`.** Cost: none up front. Risk: `0.1 + 0.2 != 0.3`, so WI-0002 AC2's balance
  property fails on ordinary inputs and the failure is intermittent and hard to explain. Listed
  to be rejected, and named here so that nobody re-proposes it as "simpler".

## Decision

**A.** Money is an `int` count of minor units, everywhere: in the parsed arguments, in the model
objects, in the JSON (`amount_minor`), and in every computation WI-0002 performs — which is what
makes its balance property exactly checkable [src: WI-0002 AC2]. `float` is never used for an
amount, and `decimal` is not imported for one.

Two functions own the boundary, and they are the only places a money string exists:

- `parse_amount(text) -> int` — accepts exactly `^[0-9]+(\.[0-9]{1,2})?$` with a value greater
  than zero, and returns minor units. The grammar and the eleven refused strings are the
  criterion's, not this ADR's [src: WI-0001 AC6]. It normalises by padding the fractional part to two digits
  before converting, so `12`, `12.5` and `12.50` all return `1250`. Anything else raises the
  validation error that becomes AC6's refusal.
- `format_amount(minor) -> str` — the inverse, always two decimal places, no symbol.

`ADR-0002`'s remainder rule, restated in these terms for WI-0002 to implement [src: ADR-0002]: for
a total of `t` minor units over `n` sharers, `share, remainder = divmod(t, n)`; every non-payer
sharer owes `share`, and the payer's own share is `share + remainder`. When the payer is not among the
sharers, the payer is owed `t` and each sharer owes `share`, with the `remainder` staying with the
payer as an amount nobody owes them — the sum of what is owed is then `t - remainder`, and the
payer has absorbed it exactly as the rule says.

## Consequences

- WI-0002's balance property is provable by integer arithmetic rather than argued about, and its
  test can assert equality rather than a tolerance.
- The JSON holds `6000` rather than `60.00`, which is less readable to a person opening the file
  than the alternative. That is the real cost of this decision, and the field name `amount_minor`
  is chosen so that the number is not misread as sixty thousand euros.
- WI-0003 inherits `parse_amount`: whatever normalisation a bank row needs, it ends at the same
  function, so the import cannot accept an amount the hand-entry command would refuse
  [src: WI-0003].
- **Reversibility: low once data exists, trivial before.** The integers are on disk under
  `amount_minor`, so changing representation later is a file migration keyed on `ADR-0003`'s
  `version` field. Before `implement` runs, it is two functions. There is no reason to expect to
  reverse it: A is the standard answer to this problem, and C is the only alternative anyone is
  tempted by.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T02:06:34Z | plan | WI-0001 | First version |
