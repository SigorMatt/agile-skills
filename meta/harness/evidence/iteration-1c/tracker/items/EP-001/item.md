---
id: EP-001
type: epic
title: Track shared expenses in a friend group from the command line
status: done
priority: critical
outcome: delivered
created: "2026-08-21T21:07:03Z"
updated: "2026-08-22T00:05:58Z"
---

## Goal

Someone who pays for things on behalf of a group of friends can, from a terminal, keep a
running record of who paid for what and who shared in it, and at any moment ask the tool who
owes whom and how much. The record survives between runs, so the answer on Tuesday accounts for
everything entered on Monday. Expenses can be brought in from a bank's CSV export rather than
retyped by hand.

## Why now

Today the group settles up from memory, a chat thread, and a bank statement nobody wants to
read twice. The cost is not arithmetic — it is that the arithmetic is never done, so debts are
either forgotten or settled by guesswork. A statement export already exists and already
contains most of the facts; the missing piece is somewhere to put them and something that will
do the netting.

## Success measures

Each of these is a thing a person with a terminal can check, from an empty data store.

- SM1 — Starting from no data, a sequence of documented commands that adds three people and
  records three expenses paid by different people produces a "who owes whom" report whose
  amounts a reader can reproduce by hand from the same three expenses.
- SM2 — The tool is stopped and started again between recording an expense and asking for the
  report, and the report is unchanged by the restart.
- SM3 — A CSV file is imported by one documented command — the command naming which of its columns
  hold the date, the amount and the description, and in what date format (WI-0004/Q-006) — and the
  expenses it created appear in the report without any of them having been typed in by hand. This
  used to name "the stakeholder's bank's export format"; it no longer does, because the tool no
  longer needs to know any bank's format, which is what made the measure checkable at all.
- SM4 — Every command runs with a stock CPython interpreter and no network access, and the
  tool's install instructions name no third-party package.

## Scope

- A single command-line program, in Python: one executable file named `expenses` at the
  repository root, invoked `./expenses <subcommand>` and using only the standard library
  (ADR-0002). Its data is one file in the user's home directory, `~/.expenses.json` by default,
  which any single run can redirect with `--data-file PATH` (ADR-0004) — the mechanism that lets
  SM1 and SM2 be checked from an empty store without writing to the stakeholder's own ledger.
  Every command follows one output convention: confirmation on stdout with exit 0, refusals on
  stderr with exit 1, and "nothing to show" treated as a normal answer rather than an error
  (ADR-0005).
- People: adding them and listing them.
- Expenses: recording who paid, how much, what for, when it happened, and which of the people
  shared in it. Every expense carries a date; a hand-entered one defaults to today and an
  imported one takes the date from its bank row (WI-0002/Q-002).
- A report of who owes whom, computed from all recorded expenses.
- Importing expenses from the stakeholder's bank's CSV export.

The delivery order is people (WI-0001), then expenses (WI-0002), then the report (WI-0003), then
the CSV import (WI-0004). The first three are forced — expenses need people, the report needs
expenses — and the stakeholder chose the position of the import in EP-001/Q-001: "get me the
report working first — that's the bit I actually asked for. Import can come after." The item
priorities are set to produce exactly this order under the orchestrator's selection key, so the
order is executed rather than merely described.

**The import is not optional and this epic cannot close without it.** Asked in WI-0004/Q-002
whether to drop it while the bank CSV sample is missing, the stakeholder said: *"And no — the
import stays part of this, it doesn't get dropped or pushed to a later epic. Build it last if
that's easiest, but I'm not signing off on a version without it."* So WI-0004 stays a child of
EP-001, it is not closed with an outcome of `dropped`, and SM3 stays a success measure. WI-0001 to
WI-0003 have been delivered in full; WI-0004 is the only thing between this epic and closure.

**This epic was blocked on a fact only the stakeholder held, and no longer is.** For five askings
WI-0004 could not pass the Definition of Ready because nobody but the stakeholder knew what their
bank's CSV export contained, and they had instructed us to wait rather than guess (WI-0004/Q-004:
*"I'd rather you wait for my actual file than guess at the format."*). WI-0004/Q-006 broke that
without breaking the instruction: it offered a route in which the tool holds no bank format at all
and is told the file's shape at import time, and the stakeholder chose it —

> "Let's do C — build it against the columns I name now, and I'll still send the sample when I get
> to it so you can add the shortcut for my bank later. Typing four options each time is fine."

So the sample is no longer a precondition for anything. It is still coming, and when it arrives it
buys a named shortcut for the four options — **a new item under this epic, not a change to
WI-0004** — and this epic does not wait for it.

## Out of scope

Derived by intake from what a reader could reasonably assume is included. None of these were
excluded by the stakeholder; if any is wanted, it is a new item.

- Unequal shares of a single expense. Everyone who shares in an expense shares it equally; the
  stakeholder settled this in WI-0002/Q-001. Supporting a restaurant bill where one person had
  the expensive thing, or a holiday flat where two people take the double room, would be a new
  item and a change to what an expense stores.
- Recording settlement payments ("Ana paid Ben back £20") and having the report account for
  them. The report describes the debt, it does not close it.
- Editing or deleting a person or an expense once recorded.
- More than one currency, or any exchange-rate handling.
- More than one group, or any notion of separate ledgers in one data store.
- Any graphical, web or mobile interface, any hosted service, any synchronisation between
  machines.
- Reading the bank's statement in any format other than the CSV export named in WI-0004/Q-001 (no PDF,
  no OFX, no direct bank connection).
- Authentication, encryption, or multi-user access control on the data file.
