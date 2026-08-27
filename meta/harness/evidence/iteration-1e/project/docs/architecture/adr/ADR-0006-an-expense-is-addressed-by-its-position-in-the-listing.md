---
title: An expense is addressed by its position in the listing, and the listing prints it
version: 1
status: current
updated: 2026-08-27T01:09:04Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0006 — An expense is addressed by its position in the listing, and the listing prints it

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** —

## Context

WI-0004 adds `expense delete`, and it is the first command in this tool that has to *refer* to a
single stored expense. Nothing in the dataset supports that today. A stored expense is
`{amount_minor, paid_by, shared_by, shares_minor, date, description}` and carries no identifier
[src: expenses/store.py], and `expense list` prints a line per expense with no handle on it
[src: expenses/cli.py]. So a way to name one expense has to be invented; there is no option that
changes nothing.

The constraints in play. The dataset is one JSON file rewritten whole on every change
[src: ADR-0001], so a scheme that changes the record shape changes every existing dataset.
Expenses are stored and listed in the order they were recorded [src: WI-0001 AC3]. Nothing in
this tool is scripted or automated — it is one person at a terminal on one machine
[src: docs/product/vision.md]. And refinement had already reached this decision under WI-0001
A1's precedent and recorded it as an assumption, with its rejected alternatives, for an architect
to confirm or overturn [src: tracker/items/WI-0004/artifacts/refinement-qa.md].

## Options considered

- **A — the position in `expense list`, printed as a leading number column.** `expense list`
  gains a first field, `1`, `2`, …, and `expense delete 2` deletes the second line of the
  listing. Cost: the numbers are not stable — deleting expense 2 makes the old 3 the new 2 — and
  the change to `expense list` output breaks one WI-0001 test that reads the amount as
  `line.split()[1]` [src: tests/test_cli.py] and makes the README's sample output wrong
  [src: README.md]. Risk: a person who lists, walks away, and deletes from a remembered number
  deletes the wrong thing.
- **B — an opaque identifier stored on each expense** (a counter, or a UUID), printed by
  `expense list` and given to `expense delete`. Cost: it changes the stored record shape, so
  every existing dataset needs the field added on read or a migration on write, and `store.load`
  currently refuses anything whose `version` is not 1 [src: expenses/store.py] — so this is a
  version bump and a compatibility path. It also puts a token with no meaning in front of a
  person reading their own expenses. Risk: the identifier outlives nothing that needs it; no
  criterion, and nothing the stakeholder asked for, requires a handle that survives a session.
- **C — match on attributes**, e.g. `expense delete --date 2026-08-01 --amount 30`. Cost: no
  listing change and no stored change, but it needs its own rule for the common case of two
  identical amounts on one day — which is more behaviour to specify, implement and test than the
  instability it avoids. Risk: an ambiguity rule that silently picks one of two matching expenses
  is a deletion of something the person did not name, which is exactly what the stakeholder ruled
  out when they chose Q-001 option A [src: WI-0004/Q-001].

## Decision

**A.** An expense is addressed by its 1-based position in the recorded order, which is the order
`expense list` prints [src: WI-0001 AC3]. `expense list` prints that position as its first
whitespace-separated field [src: WI-0004 AC2]. `expense delete <NUMBER>` deletes the expense at
that position and nothing else. The numbers are positions, not identities: after any deletion the
remaining expenses renumber, and the number means "the Nth line of the listing you are looking
at" and nothing more. The stored record shape does not change, and `VERSION` stays 1
[src: expenses/store.py].

## Consequences

Easy: no data migration, no compatibility path, no change to any dataset written by the delivered
tool. The handle is the thing the person is already looking at, so `expense list` followed by
`expense delete` needs nothing explained between them. `store.expenses(data)` already returns
the list in recorded order [src: expenses/store.py], so the position is an index and no lookup
structure is needed [src: expenses/store.py].

Hard: nothing may be scripted against these numbers, and a listing held in a person's head across
a deletion is stale. This item states that cost in the item's `## Out of scope` rather than
mitigating it [src: WI-0004]. Two pieces of delivered work must be updated with this change
rather than left to fail: the WI-0001 test that reads `line.split()[1]` [src: tests/test_cli.py]
and the README's `expense list` sample [src: README.md]. Neither is a breach of a WI-0001
acceptance criterion — AC3 requires each entry to show its amount, payer, sharers, date and
description in recorded order, all of which a leading number leaves intact [src: WI-0001 AC3].

Reversibility: **easy in one direction, expensive in the other.** Adding a stored identifier
later (option B) is a data-format change and a `VERSION` bump — expensive, but no worse then than
now, because this decision leaves the stored record untouched [src: expenses/store.py]. Removing the number column later
is a one-line change to `expense_list` in `expenses/cli.py` plus its tests and the README. What
would be irreversible is option B's opposite: having published an identifier and then taken it
away. This decision publishes nothing that outlives a listing, so it forecloses nothing.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T01:09:04Z | plan | WI-0004 | First version |
