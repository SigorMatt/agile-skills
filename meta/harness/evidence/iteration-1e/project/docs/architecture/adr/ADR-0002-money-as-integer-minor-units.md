---
title: Represent money as integer minor units
version: 1
status: current
updated: 2026-08-26T23:52:03Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0002 — Represent money as integer minor units

- **Status:** accepted
- **Date:** 2026-08-26
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

An amount is a decimal with at most two decimal places and must be strictly greater than zero;
`12`, `12.5` and `12.50` all mean the same thing, and `1.005` is a refusal
[src: tracker/items/WI-0001/artifacts/refinement-qa.md]. AC2 requires an expense's shares to sum
to exactly the amount paid [src: WI-0001 AC2], and AC8 requires that to hold for an amount that
does not divide evenly between its sharers [src: WI-0001 AC8]. WI-0002's settlement list is
computed from these figures and cannot balance if they do not [src: WI-0002].

"Exactly" is the whole of this decision. The representation has to make it a property of the type
rather than something the code is careful about.

## Options considered

- **A — `int`, counting the smallest unit (what most currencies call cents).** Cost: parsing and
  formatting have to be written, roughly twenty lines. Risk: an amount larger than 2^63 minor
  units, which is not a friend group.
- **B — `decimal.Decimal`.** Cost: nothing to write; it ships with Python
  [src: run: python3 -c 'import decimal' → exit 0]. Risk: it is
  exact for the arithmetic here, but it carries a context, a precision and rounding modes, so
  "exactly" becomes a property of how it is configured rather than of the value. It also
  round-trips through JSON as a string or a float, and the float path silently reintroduces the
  problem this ADR exists to remove.
- **C — `float`.** Cost: none. Risk: `0.1 + 0.2 != 0.3`. Excluded.

## Decision

Money is an `int` counting minor units. `12`, `12.5` and `12.50` all parse to `1250`; `1.005`,
`abc`, `0` and `-4` are refusals [src: WI-0001 AC6].

Parsing accepts digits and an optional `.` followed by one or two digits, and nothing else — it
is a whole-string match rather than a call to `float()` or `Decimal()`, so that `1e3`, `inf`,
`nan` and `1_000` are refusals without any special case
[src: tracker/items/WI-0001/artifacts/plan.md; WI-0001 AC6]. Formatting for display is
`f"{minor // 100}.{minor % 100:02d}"`, so a printed amount always shows two decimal places.

The stored field is named `amount_minor`, and every stored share is `..._minor`, so that a reader
of the JSON file cannot mistake the unit [src: ADR-0001].

No currency symbol or code is stored or printed. EP-001 excludes currency conversion, and naming
a currency the stakeholder never mentioned would be inventing a fact about their data
[src: tracker/items/EP-001/item.md].

## Consequences

Easy: exact sums, an exact remainder rule [src: ADR-0003], and comparisons that behave. JSON
round-trips integers without loss, so the store is exact too.

Hard: any future currency with a different number of minor units, and any future need for
fractional-unit precision. Both would need this ADR superseded.

**Reversibility: medium.** The representation is confined to one module and the store's field
names, but changing it means both a code change and a conversion of every stored amount — the
data on disk is in minor units. It is reversible with a migration, not by editing one function.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-26T23:52:03Z | plan | WI-0001 | First version |
