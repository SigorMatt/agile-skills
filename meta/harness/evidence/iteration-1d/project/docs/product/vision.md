---
title: Product vision — shared expenses in a friend group
version: 3
status: current
updated: 2026-08-22T01:55:49Z
updated-by: answer-questions
updated-for: WI-0001
---

# Product vision — shared expenses in a friend group

## Who it is for

One person in a group of friends who share costs — the one who ends up keeping track. They have
a terminal, they are comfortable running a command, and they are the only person who operates
the tool. The rest of the group are named in it but do not use it.

## What it is for

To answer one question reliably: **who owes whom, and how much.** It does that by holding the
group's people and the expenses they shared, so that the answer is arithmetic over a record
rather than a reconstruction from memory. Two things make it worth using rather than a
spreadsheet:

- the record persists between runs, so it accumulates rather than being rebuilt; and
- expenses that already exist in the person's bank CSV export can be brought in rather than
  retyped.

The answer stays true over time rather than only over one trip, because the tool also records
that someone paid someone back: the stakeholder settled this on `EP-001/Q-003` — "let us log that
someone paid, so the report doesn't go stale". Recording a repayment is deliberately plain: who
paid whom, how much, and the debt shrinks.

## What it deliberately is not

- **Not a service.** Nothing is hosted, nothing is signed up for, nothing leaves the machine.
  The tool answers the same way with no network available.
- **Not a bank client.** It never talks to a bank. Its input is a CSV file the person exported
  themselves.
- **Not multi-user and not multi-currency.** One operator, one currency. A run may be pointed at
  a different data file so a trip can keep its own books, but the tool never holds two groups at
  once and never compares them [src: WI-0001/Q-004; WI-0001 AC9].
- **Not a tool for uneven splits.** An expense is shared equally among the people who shared it;
  there is no way to say that one person owes more of a bill than another. The stakeholder chose
  this — "equal split's fine for now. If we hit a case that needs otherwise we'll deal with it
  then" — so an uneven bill is entered as two expenses [src: WI-0001/Q-001; WI-0001 AC5].
- **Not a UI.** It is a command-line tool; there is no web or graphical front end.
- **Not an accounting system.** It tracks what was shared, what that implies is owed, and what
  has since been paid back. It does not do anything else an accounting system does — no
  categories, no budgets, no reports beyond who owes whom.

## How we will know it works

The measures live on `EP-001`. In short: a person can start from nothing, enter their group and
their expenses, come back tomorrow and find them, import a bank export without hand-editing it,
and get a set of debts that adds up.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-22T01:55:49Z | answer-questions | WI-0001 | Equal splits recorded as a product boundary, and a per-run data file recorded as the limit of "one group's books" (`WI-0001/Q-001`, `WI-0001/Q-004`) |
| 2 | 2026-08-22T01:44:16Z | answer-questions | EP-001 | Repayments moved from open question to delivered scope (`EP-001/Q-003`, `ADR-0001`) |
| 1 | 2026-08-22T01:36:34Z | intake | EP-001 | First version, from the stakeholder's stated idea |
