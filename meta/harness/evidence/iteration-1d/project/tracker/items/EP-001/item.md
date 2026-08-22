---
id: EP-001
type: epic
title: Track shared expenses in a friend group from the command line
status: open
priority: high
created: "2026-08-22T01:34:49Z"
updated: "2026-08-22T01:47:30Z"
---

## Goal

A person in a friend group can keep track, from their own terminal, of who paid for what and
who shared in it, and can ask at any moment who owes whom how much. Records they entered
yesterday are still there today. Where expenses already exist in a bank's CSV export, they can
be brought in rather than retyped. Nothing leaves the machine and nothing is signed up for.

## Why now

The stakeholder's group has no record of shared spending that they can query: today the
alternative to this tool is typing expenses in by hand, or not recording them at all. The
stakeholder said explicitly that they do not want to type expenses in, and that their bank
already exports the transactions as CSV — so the data exists and is not in a form that answers
"who owes whom". What the group does today instead, and what the cost of getting it wrong has
been, were not stated and are recorded as unknown; `refine` may pick them up.

## Success measures

- Starting from an empty state, a person can add the members of their group, record several
  expenses each paid by one member and shared by some or all, quit the tool, start it again,
  and see the same expenses listed.
- Asking the tool who owes whom produces a list of debts in which every named amount is
  arithmetically consistent with the recorded expenses, and the amounts owed and the amounts
  owing sum to the same total.
- A bank CSV export can be turned into recorded expenses by running one command against the
  file, without the person opening a text editor to reshape the file first.
- No step in any of the above requires a network connection, a hosted service, or an account:
  the tool runs and gives the same answers with networking unavailable.
- After recording that one member repaid another, the who-owes-whom answer shrinks by that
  amount rather than continuing to report the debt as outstanding.

## Scope

- A command-line tool, written in Python, run locally.
- Adding and listing the people in the group.
- Recording an expense: who paid, how much, what for, and which of the people shared it.
- Persisting people and expenses to local storage that survives process exit.
- Reporting who owes whom, from all recorded expenses.
- Reading a bank CSV export and turning its rows into recorded expenses.
- Recording that one member repaid another, and netting those repayments into the who-owes-whom
  report.

## Out of scope

- Any server, hosted service, account, or synchronisation between machines.
- A graphical or web interface.
- Multi-currency handling and exchange rates: one currency throughout.
- Connecting to a bank directly, or any API; the input is a CSV file the person already has.
- Authentication, permissions, or more than one group's books in one place.

## Notes

Recorded as **assumptions**, not as things the stakeholder said, so that a later reader can see
which is which:

- "No external services" is read as: nothing hosted, no remote API, no account. It is taken to
  imply the tool must work offline. Whether third-party Python packages are also excluded was
  not stated; the epic assumes the standard library is sufficient and treats reaching for a
  dependency as a decision `plan` must record, because that reading satisfies the stated
  constraint under either interpretation and is cheap to reverse.
- One currency throughout is an assumption; the stakeholder named no currency.

Recorded as **unknown**, because the stakeholder was not asked and has not said:

- What the group does today instead of this tool.
- What would make this a failure even if it worked.
- Whether expenses can be split unevenly, or only equally among those who shared them —
  `refine` must settle this on WI-0001 before it is Ready.

### Decisions the stakeholder made on the intake questions (2026-08-22)

- **`Q-001` — build order.** WI-0001, then WI-0002 ("that's the point of the tool"), then WI-0003
  last. Neither WI-0002 nor WI-0003 is optional: the stakeholder said explicitly that they are
  not shipping a version without the import. WI-0003's `priority` was lowered to `medium` to
  encode "built last" in the orchestrator's selection key, and `depends-on: WI-0002` was added;
  neither change means the import matters less.
- **`Q-002` — the bank CSV's shape and the import rule.** Deferred by the stakeholder ("I'll send
  you a sample later"). Both facts are still missing. WI-0003 stays at `draft` and is not
  refinable until a sample arrives; `refine` must file a fresh question citing `Q-002` rather
  than guess a CSV shape.
- **`Q-003` — repayments.** In scope for this epic ("let us log that someone paid, so the report
  doesn't go stale... whatever's simplest to build"). Implemented as two criteria on WI-0001
  (record and persist a repayment) and two on WI-0002 (net them into the report) rather than as a
  fourth work item — see `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md`,
  which also records that only `intake` may create a work item, so `answer-questions` could not
  have opened a fourth one even had it preferred to.

Open questions filed at intake: `Q-001`, `Q-002`, `Q-003` — all three now answered.
