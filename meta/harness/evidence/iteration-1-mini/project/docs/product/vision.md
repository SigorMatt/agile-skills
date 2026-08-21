---
title: Product vision — shared expenses in a friend group
version: 3
status: current
updated: 2026-08-21T03:05:00Z
updated-by: answer-questions
updated-for: EP-001
---

# Product vision — shared expenses in a friend group

## Who it is for

A group of friends who regularly pay for things on each other's behalf — one person picks up a
dinner bill, another books the accommodation, a third buys the train tickets — and who want to
square up fairly afterwards. The person using the tool is one of the group, working at a
terminal on their own machine. They are comfortable typing a command; they are not running a
service and they do not want an account anywhere.

Today that group does this in their heads, in a chat thread, or in a spreadsheet one person
maintains. Each of those loses information, and the loss shows up as either an argument or a
quietly out-of-pocket friend.

## What it is for

Keeping an honest, durable record of who paid for what on whose behalf, and answering one
question well: **who owes whom, right now.** The record lives in a file on the user's own
machine and survives between runs, so it can be built up over weeks rather than reconstructed
from memory at the end of a trip.

Concretely, the product lets someone:

- record the people in the group,
- record that one person paid an amount that some or all of the group shared,
- ask, at any time, who owes whom.

The moment the product is built around is the end of a trip. The stakeholder described success
as: *"After a weekend away, one command tells us who pays whom and nobody argues about it."*
Both halves of that sentence are requirements. **One command** means the answer is a single
invocation over what has already been recorded, not a process. **Nobody argues** means the
answer has to be checkable by the people it is about — so the tool prints the payments that
settle the group *and*, next to them, each person's net position, which anyone can reconcile
against their own memory of what they paid.

## What it deliberately is not

- **Not a service.** No server, no account, no sync between machines, no network access at all.
  The store is one file on one machine, and the tool installs nothing from the internet.
- **Not a payments system.** It says who owes whom; it never moves money.
- **Not a general finance tool.** One unnamed currency, no exchange rates, no budgets, no
  categories, no reports beyond the balance between people.
- **Not a fair-shares calculator.** Every expense is divided **equally** among the people who
  shared it. There is no per-person amount, weight or percentage: *"Equal split is all I need —
  that's what I meant."* Someone who had the cheap main course and someone who had the steak owe
  the same.
- **Not a multi-group tool.** One ledger, one friend group, one file: *"One group — just me and
  my friends, no second group I need this for."*
- **Not a multi-user application.** There are no logins and no permissions: whoever can run the
  tool can see and change everything in the store.
- **Not a GUI or a web app.** A command-line interface is the whole of the interface.

## What has been settled since v1

The four questions v1 recorded as open have all been answered by the stakeholder, and the
answers are now part of the product above rather than a list of pending decisions:

- **Equal splits only** (EP-001/Q-001) — see "Not a fair-shares calculator".
- **Settling up is deferred, not refused** (EP-001/Q-002) — *"Leave settling up out of this
  first version, let's get expenses and balances working first."* Recording a repayment is out
  of scope for EP-001 and expected in a later epic, so WI-0003's balance model must stay open to
  netting a transfer in later.
- **One ledger, one group** (EP-001/Q-003) — see "Not a multi-group tool"; the storage
  consequences are in `docs/architecture/adr/ADR-0002-one-store-file-per-user.md`.
- **The report prints the payments, with net positions alongside** (WI-0003/Q-001) — *"I want
  the actual payments — who pays whom — not just a list of who's up and down. A quick per-person
  summary alongside it is fine too."*

Two further decisions were delegated to the architect rather than made by the stakeholder, and
are recorded as ADRs: the Python baseline and the ban on third-party dependencies
(`ADR-0001-python-baseline-and-no-dependencies.md`, from EP-001/Q-004 — *"Whatever you think is
best"*), and how a remainder is allocated when an amount does not divide evenly
(`ADR-0004-payer-absorbs-the-rounding-remainder.md`, from WI-0003/Q-002 — *"Not sure yet — go
ahead anyway, we'll decide later."*).

## What is deferred, with its shape already agreed

- **Importing expenses from a bank's CSV export.** The stakeholder asked for this while
  answering EP-001/Q-002 — *"I want to import expenses from my bank's CSV export instead of
  typing them in"* — and settled its shape in EP-001/Q-006: *"Yeah, D then A sounds right — get
  expenses and balances working first, come back to this later. I'll send you a sample of my
  bank's export when I get to it."*

  So it is **not** in EP-001, and it is **not** refused. It becomes its own epic once people,
  expenses and balances are working. When it does, it takes the shape of option A in
  EP-001/Q-006: the tool reads the file and, for each row the user picks, asks who shared it,
  recording an expense with the amount, date and description already filled in. The reason it
  cannot be a silent bulk import is a property of bank statements, not a design preference — a
  row carries a date, a description and an amount, and can never say **who shared the expense**,
  which is the one field this product turns on. Some typing therefore has to remain; A removes
  only the part the file can supply.

  It has one outstanding input: the header row and one data row of a real export from the
  stakeholder's bank, which they have said they will send. There is no standard bank CSV format —
  banks differ on column names, date format, and whether an amount is one signed column or a
  debit/credit pair — so that sample is what makes any of this buildable without another round
  trip. Nothing in EP-001 waits on it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-21T03:05:00Z | answer-questions | EP-001 | Recorded the stakeholder's answer to EP-001/Q-006: the bank-CSV import is deferred to a later epic and will take the shape of that question's option A, with a real export sample outstanding. Replaced "What is not yet settled" with "What is deferred, with its shape already agreed" — nothing about the product is unsettled any more |
| 2 | 2026-08-21T02:27:20Z | answer-questions | EP-001 | Recorded the stakeholder's answers to EP-001/Q-001..Q-005 and WI-0003/Q-001: equal splits only, one ledger, settling up deferred, the settlement-plus-net-positions report, and the one-command success measure. Replaced the open-questions list with what was settled, and raised the new bank-CSV-import request as unsettled |
| 1 | 2026-08-21T02:05:17Z | intake | EP-001 | First version, written from the stakeholder's stated idea |
