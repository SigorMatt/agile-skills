---
id: EP-001
type: epic
title: Track shared expenses in a friend group from the command line
status: done
priority: high
outcome: delivered
created: "2026-08-21T18:38:55Z"
updated: "2026-08-21T20:36:04Z"
---

## Goal

A person in a friend group can, from a terminal, record who is in the group, record expenses
that one of them paid and several of them shared, and at any later moment ask the tool who owes
whom and by how much. The answer must be correct across separate invocations of the tool: the
data outlives the process that recorded it.

## Why now

Today the group tracks this in memory, in a chat thread, or in an ad-hoc spreadsheet. All three
lose entries and none of them answers "who owes whom" without someone doing the arithmetic by
hand, which is where the disagreements come from. The cost of not solving it is small per
occurrence and constant: every shared meal or trip needs the same manual reconciliation, and the
result is only as trustworthy as whoever did the sums.

## Success measures

- Starting from an empty state, a person can add three people and record two expenses, exit the
  tool, start it again, and see balances that account for both expenses — with no re-entry of
  data.
- Asking the tool who owes whom prints, for every person with a non-zero net position, a debtor,
  a creditor and an amount, such that the printed amounts settle every recorded expense.
- After recording a payment from one person to another, asking who owes whom no longer reports
  the debt that payment covered; when the recorded payments cover every debt, the tool says
  everybody is settled up.
- The tool runs on a stock CPython 3 installation with no third-party packages installed and no
  network access: `python3 -c "import <the tool>"` succeeds in an environment where `pip list`
  shows only the standard distribution, and no invocation opens a socket.

## Scope

- Recording the members of the group.
- Recording an expense: an amount, who paid it, and which subset of the group shared it.
- Deriving and displaying who owes whom from the recorded expenses.
- Recording that one person has paid another, and netting that payment off the balances, so that
  the reported debts are what is still outstanding rather than a running total since the group
  started (the human's answer to `Q-001`).
- Persisting all of the above to local storage between invocations.
- A Python implementation using only the standard library.

## Out of scope

- Any external service: no server, no cloud sync, no database daemon, no network calls of any
  kind. This is the human's stated constraint and it is absolute.
- More than one currency. Amounts are assumed to be in a single unstated currency.
- Sharing state between machines or between users; the data file is local and single-writer.
- Authentication, user accounts, or any notion of permission over who may record what.
- Receipts, attachments, photographs, or free-text expense history beyond a description.
- A graphical, web or mobile interface.
- Editing or deleting a previously recorded expense. A correction, if it is needed at all, is
  a new epic — see EP-001's journal for why this was excluded rather than assumed.
- Reminders, notifications, or anything that contacts a person outside the terminal.
