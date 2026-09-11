---
title: Hold every amount as a whole number of cents
version: 1
status: current
updated: 2026-09-11T02:34:57Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0001 — Hold every amount as a whole number of cents

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder fixed what an amount looks like on the way in and on the way out, and was
explicit about why: *"One currency, cents exactly, two decimal places both ways — `12.5` meaning
12.50 is fine. I do not want anything rounded off; the figures have to add up"*
[src: WI-0001/Q-002]. In the same breath they handed the inside of it over — *"How you keep it
under the hood is yours to decide"* — so this decision is taken under that licence and nothing
wider.

`WI-0001` turns the requirement into an observation: adding `0.01` a hundred times in a hundred
separate runs must show `1.00` [src: WI-0001 AC9 "the listing shows `1.00` for that envelope"].
That single criterion is what rules out the obvious representation.

## Options considered

- **A — `float`.** Cost: none to write. Risk: fails the exactness criterion outright
  [src: WI-0001 AC9 "No amount is rounded or truncated"] — a hundred additions of 0.01
  in IEEE-754 binary do not total 1.0 — and every later total in the epic inherits the drift.
- **B — `decimal.Decimal`.** Cost: a context to configure and a type that has to be carried in
  and out of JSON as a string. Risk: exact, so AC9 holds; the risk is that its exactness is
  configurable and a later contributor changes the context.
- **C — a whole number of cents in a Python `int`.** Cost: every boundary needs a conversion —
  one parse function in and one format function out. Risk: a raw integer is easy to print by
  accident, which shows the user `4000` where they expect `40.00`; the mitigation is that only
  one function formats an amount.

## Decision

Every amount is a Python `int` counting cents, everywhere inside the tool and everywhere in the
stored file. Option C.

Two functions in `envel/money.py` are the only places the two forms meet
[src: tracker/items/WI-0001/artifacts/plan.md]: one parses the text the
user typed into cents, one renders cents back into text. No other module converts between them,
and no amount is ever held as a `float` or written to the store as a decimal string.

## Consequences

Easy: exact arithmetic with no configuration, JSON that round-trips without a custom encoder, and
one place to change if the rules about how an amount is written ever move.

Hard: a raw `int` is not self-describing, so a module that prints an amount without going through
the formatter shows the wrong thing and nothing crashes. The tests for the format functions are
what catch that.

**Reversibility: easy while no data exists, and a migration once it does.** Changing to
`Decimal` would mean rewriting the two functions and converting every amount in every stored
file. Nothing published depends on it, so the cost is one file plus a data migration — which is
exactly why the choice is made now, before the stakeholder has a file.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version |
