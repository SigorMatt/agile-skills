---
id: EP-001
type: epic
title: Envelope budgeting from the command line
status: open
priority: critical
created: "2026-09-10T13:14:43Z"
updated: "2026-09-10T13:30:22Z"
---

## Goal

Someone who budgets by dividing their money into named pots wants to do that at a terminal
instead of on paper or in a spreadsheet. They should be able to set up envelopes by name, put
income into them, record what they spend against a particular envelope, and see at a glance what
is left in each one. They should also be able to ask for a summary of a month's activity. What
they record must still be there the next time they run the tool, on the same machine, with
nothing else running.

## Why now

The stakeholder is doing this today outside any tool of their own — the idea as stated is a
description of a routine they already have and want mechanised. The cost of not solving it is
that every envelope balance is recomputed by hand from a list of spends, which is slow, easy to
get wrong, and gives no way to look back at a month once it has passed.

## Success measures

- In one terminal session a person can create an envelope, put money into it, record a spend
  against it, and see a remaining balance that equals what they put in minus what they spent.
- The balances printed after the process exits and is started again are the same as the ones
  printed before it exited, with no manual step in between.
- A person can ask for a summary of a named month and get, for each envelope, what went in, what
  went out, and what remains.
- Recording a spend against a name that is not an envelope does not silently succeed: the tool
  says so and exits non-zero.
- Recording a spend larger than what is left in its envelope does not silently succeed either:
  the tool says so, exits non-zero, and records nothing, so no envelope balance ever goes
  negative (`EP-001/Q-003`).
- A person can move money from one envelope to another, and can correct or remove a spend they
  already recorded, so that the balances can be made to match reality without leaving the tool
  (`EP-001/Q-005`).
- A transaction recorded a few days late lands in the month it happened in, not the month it was
  typed in (`EP-001/Q-004`).
- The tool runs from a checkout of this repository with a Python interpreter and nothing else —
  no server to start, no account to create, no network access.

## Scope

- Named envelopes: creating them, listing them, and their balances.
- Recording money into an envelope and money spent out of an envelope. Income goes straight into
  a named envelope; the tool holds no unallocated pool and computes no split (`EP-001/Q-002`).
- Refusing a spend that exceeds its envelope's balance, rather than letting the envelope go
  negative (`EP-001/Q-003`).
- A date on each transaction, defaulting to today and overridable when catching up
  (`EP-001/Q-004`).
- Moving money from one envelope to another (`EP-001/Q-005`, WI-0004).
- Correcting or removing a spend that has already been recorded (`EP-001/Q-005`, WI-0005).
- A summary covering a month, showing for each envelope what went in and what went out
  (`EP-001/Q-005`).
- Storing all of the above on the local filesystem so it survives between runs.
- A command-line interface, in Python.

## Out of scope

- Any client-server component, hosted service, background daemon or network access. The
  stakeholder said "no services"; this epic read that as covering all of them, and they have
  since confirmed the reading in as many words — "no network for anything" (`EP-001/Q-001`). It
  is therefore a decision rather than an inference.
- Importing from a bank, a CSV export, or any other external source of transactions.
- Multiple users, accounts, or profiles sharing one data store. "Data must survive between runs"
  was read as one machine and one person, and the stakeholder confirmed it: "it's my machine and
  my data, just me using it" (`EP-001/Q-001`). Syncing, sharing and a second copy of the data are
  out with it.
- Multiple currencies, or any conversion between them.
- Keeping a trail of corrections: an audit log of what was recorded before a spend was amended
  or removed, or an undo stack. The stakeholder asked for the correction itself and said they
  care about it "far more than about keeping a history of what I got wrong" (`EP-001/Q-005`).
  This bullet previously placed editing and deleting a transaction out of scope altogether; that
  reading was ours, and their answer to `EP-001/Q-005` replaced it.
- Budget planning ahead of time: recurring allocations, targets, forecasts, or rollover rules
  between months. What is left in an envelope at the end of a month stays there and is not swept
  anywhere, so there is nothing to roll over (`EP-001/Q-005`).
- A graphical or web interface, and packaging for distribution (PyPI, a system package).
