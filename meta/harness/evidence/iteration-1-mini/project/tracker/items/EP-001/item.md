---
id: EP-001
type: epic
title: Track shared expenses in a friend group from the command line
status: open
priority: high
created: "2026-08-21T02:03:44Z"
updated: "2026-08-21T03:05:00Z"
---

## Goal

A member of a friend group can, from a terminal, keep track of money the group spends on each
other's behalf: record who is in the group, record that one person paid for something that
several people shared, and ask at any moment who owes whom. The record persists on the machine
between runs, so the group can build it up over weeks of dinners and trips rather than
reconstructing it from memory at the end.

## Why now

Today the group does this in their heads, in a chat thread, or in a spreadsheet somebody has to
maintain. All three lose information: the chat thread has no totals, the spreadsheet is one
person's job and breaks when they are not there, and memory produces arguments. The cost of not
solving it is small each time and cumulative — the group either over-pays a generous member or
stops splitting things at all.

## Success measures

- Running the tool, adding three people and two expenses, exiting, and running it again in a
  fresh process shows the same people and the same expenses.
- For a worked example the stakeholder can check by hand — say, Alice pays 30 for a dinner
  shared by Alice, Bob and Carol — the "who owes whom" output states that Bob owes Alice 10 and
  Carol owes Alice 10, and no other debt.
- Across any set of recorded expenses, the amounts in the "who owes whom" output net to zero:
  the total owed equals the total owing, to the last minor unit.
- Every command the tool offers, run with no arguments or with bad arguments, exits non-zero
  and prints a message naming what was wrong, rather than a Python traceback.
- The tool runs on a machine with a Python interpreter and no network access, and installs
  nothing from the internet.
- **Settling up after a trip takes one command.** With the people and the expenses already
  recorded, a single invocation prints the payments that clear the group — who pays whom, and
  how much — with no second command and no arithmetic done by hand. (From the stakeholder's
  answer to EP-001/Q-005: *"After a weekend away, one command tells us who pays whom and nobody
  argues about it."*)
- **The settlement can be checked without trusting it.** The same output carries each person's
  net position alongside the payments, so anyone at the table can reconcile the figure against
  what they remember paying, rather than having to take the payment list on faith. This is the
  observable form of "nobody argues about it"; see WI-0003/Q-001.

## Scope

- A persistent store of the group's people and expenses, held in **one** file on the local
  machine — one ledger for one friend group, at a fixed per-user path, created on first use.
  See ADR-0002. (EP-001/Q-003.)
- Adding a person; listing people.
- Recording an expense: an amount, who paid it, and which people shared it (some or all).
  **Shares are always equal** among the people who shared the expense; the money is divided by
  the number of sharers, and nothing carries a per-person amount, weight or percentage.
  (EP-001/Q-001.)
- Listing the expenses that have been recorded.
- Reporting who owes whom, derived from the recorded expenses: the set of payments that settles
  the group, with each person's net position shown alongside. (WI-0003/Q-001.)
- A command-line interface in Python, usable with no external services. Python 3.9+, standard
  library only, at runtime and in tests. See ADR-0001. (EP-001/Q-004.)

## Out of scope

- Any server, account, sync between machines, or shared/hosted storage. The store is one file
  on one machine.
- Multiple currencies, exchange rates, or currency conversion. One unnamed currency throughout.
- **Recording a repayment between two people ("Bob paid Alice 10") so that it clears a debt.**
  Out of scope *for this epic*, deferred to a later one: the stakeholder's answer to
  EP-001/Q-002 was *"Leave settling up out of this first version, let's get expenses and
  balances working first."* This is provisional-by-deferral, not a permanent no. WI-0003 must
  keep the balance calculation shaped so that a repayment can later be netted in as a transfer.
- Uneven or weighted splits — a per-person amount, a share count, or a percentage within one
  expense. Permanently out of scope for this epic: the stakeholder's answer to EP-001/Q-001 was
  *"Equal split is all I need — that's what I meant."*
- Keeping several friend groups apart. One ledger, one group (EP-001/Q-003, ADR-0002).
- Editing or deleting a person or an expense once recorded, and any undo. Still nobody's
  decision; no question has been asked about it, and nothing in the epic depends on it.
- A graphical or web interface, and any notification, reminder or email.
- Authentication or per-user permissions: whoever can run the tool can see and change
  everything in the store.
- Importing from a spreadsheet or a chat export.
- **Importing expenses from a bank's CSV export.** Out of scope *for this epic*, deferred to a
  later one, and the later one's shape is already decided. The stakeholder asked for it while
  answering EP-001/Q-002 — *"I want to import expenses from my bank's CSV export instead of
  typing them in"* — and then chose between four shapes in EP-001/Q-006: *"Yeah, D then A sounds
  right — get expenses and balances working first, come back to this later. I'll send you a
  sample of my bank's export when I get to it."* This is provisional-by-deferral, not a
  permanent no.

  Two facts belong here so that the future epic does not re-derive them. First, the shape when it
  comes is **option A** of EP-001/Q-006: the tool reads the CSV and, for each row the user picks,
  asks who shared it, recording an expense whose amount, date and description are already filled
  in. It is not a silent bulk import — a statement row carries a date, a description and an
  amount but cannot say **who shared the expense**, which is the field this whole product turns
  on, so some typing necessarily remains and A is the shape that removes only the tedious part.
  Second, it needs one input this project does not yet have: the header row and one data row of a
  real export from the stakeholder's bank, which they have undertaken to send. There is no such
  thing as a standard bank CSV format, so without that sample any implementation would start with
  another round trip.

  Nothing in EP-001 depends on this, and nothing in EP-001 should be built to accommodate it.
  Note in passing that option A records expenses with a **date** and a **description**, which
  EP-001 already carries on an expense (WI-0002/Q-001), so the store does not need reshaping for
  it.
