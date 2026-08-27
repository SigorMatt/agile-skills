---
title: Referential consistency between people and expenses is enforced where data is written
version: 1
status: current
updated: 2026-08-27T01:09:41Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0007 — Referential consistency between people and expenses is enforced where data is written

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** —

## Context

A person in this dataset is not a record; they are a name, listed in `data["people"]` and
repeated inside every expense that names them as payer or sharer [src: expenses/store.py]. Until
WI-0004 nothing could remove a name, so the question of what an expense naming an absent person
means never arose in practice — but the reading side already has an answer, and it is a silent
one. `settle.positions()` builds its result from `data["people"]` and skips any name in an
expense that is not in that list [src: expenses/settle.py]. An expense naming somebody who is not
in the group therefore contributes its payer's credit or its sharers' debts only in part, and
`settle` prints a smaller, wrong answer without saying anything. WI-0002's review recorded this
[src: tracker/items/WI-0002/artifacts/review.md].

WI-0004 adds `person delete`, which is the first way to create that state. The stakeholder was
asked what should happen and chose to be refused, in their words: *"Go with A — refuse and tell me
what's in the way. I'd rather do a couple extra commands than have expenses vanish or numbers
quietly go wrong because I mistyped a name."* [src: WI-0004/Q-001]. That settles the product
behaviour. What it does not settle, and what this ADR decides, is **where in the system the rule
lives** — because the same guarantee can be bought at the writing end, at the reading end, or at
both, and those are different systems.

## Options considered

- **A — enforce it where data is written, and nowhere else.** `store.delete_person` refuses when
  the name appears in any stored expense; `store.add_expense` already refuses a payer or sharer
  who is not in the group [src: expenses/store.py]. Together those are the only two ways the
  relation can be broken, so the invariant holds for every dataset this tool produces, and the
  reading side may go on assuming it. Cost: the invariant is a property of two functions rather
  than a thing anyone can see stated in one place, which is what this ADR is for. Risk: a
  hand-edited JSON file still violates it and `settle` still says nothing.
- **B — check it where data is read.** `store.load` validates the relation and refuses a dataset
  whose expenses name unknown people. Cost: every command pays for the check on every run, and a
  person whose file is already inconsistent — from a hand edit, or from a future importer — is
  locked out of the tool entirely, including out of the listings that would show them what is
  wrong. Risk: this converts a wrong answer into a dead tool, which is worse for the one case it
  catches that A does not.
- **C — make `settle.positions()` refuse rather than skip**, leaving writes alone. Cost: it
  would surface the inconsistency at the moment it matters, but it does not prevent it, so
  `person delete` would still have to decide what to do — which is the question the stakeholder
  already answered. Risk: it contradicts the stakeholder's choice by allowing the deletion.
- **D — both A and B.** Cost: the check in two places, and two messages for one condition. Risk:
  they drift.

## Decision

**A.** The invariant is: **every name appearing in a stored expense — as `paid_by`, in
`shared_by`, or as a key of `shares_minor` — is a name in `data["people"]`.** It is enforced
in `expenses/store.py`, at the two points that can break it: `add_expense`, which already
refuses unknown names [src: expenses/store.py], and `delete_person`, which WI-0004 adds and which
refuses when the name is still in use [src: WI-0004 AC3]. Nothing is added to `store.load`, and
`settle.positions()` is not changed — it may keep assuming what it already assumes
[src: expenses/settle.py].

The refusal names what stands in the way, rather than merely refusing, because that is the whole
of what the stakeholder bought with the extra commands [src: WI-0004 AC3].

## Consequences

Easy: `settle` stays a pure function over a consistent dataset and needs no defensive code; the
cost of the guarantee is paid once, at the moment somebody tries to break it, rather than on every
read. `store.py` remains the only module that knows what a valid dataset is, which is the
layering the project already has [src: docs/architecture/overview.md].

Hard: the invariant is not checked on data this tool did not write. A hand-edited file, or one
produced by a future importer that bypasses `add_expense`, can still violate it, and `settle`
will still under-report silently. WI-0003, the bank CSV importer, is the concrete case to watch:
if it appends expenses by any path other than `add_expense`, this ADR's guarantee does not
extend to it [src: WI-0003].

Reversibility: **cheap.** Adding option B later is a validation function called from
`store.load`, one file and no data change. Removing the `delete_person` refusal would be
reversing the stakeholder's own decision, so it is cheap in code and expensive in authority — it
would need them to say so, not an architect. Nothing here changes the stored format, so no
migration is implied in either direction [src: ADR-0001].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T01:09:41Z | plan | WI-0004 | First version |
