---
id: EP-001
type: epic
title: Envelope budgeting from the command line
status: done
priority: high
created: "2026-09-11T01:56:43Z"
updated: "2026-09-11T19:22:35Z"
outcome: delivered
---

## Goal

A person who budgets their own money should be able to sit at a terminal, set up named
envelopes, put income into them, record what they spend against a particular envelope, and see
at a glance how much is left in each one — plus look at a summary for a month. What they put in
is still there the next time they run the tool, on the same machine, with nothing running in the
background between invocations.

## Why now

The stakeholder is doing this some other way today and asked for a tool for it; they stated the
want as a whole workflow ("set up envelopes … put income in … record spending … see what's
left … a simple monthly summary"), which is a sign the pieces are only useful together. Nothing
exists in this repository yet, so the cost of not doing it is that the workflow stays wherever
it is now. What "today" is, is a spreadsheet with a tab per month: the stakeholder said it works
and is tedious, which is the cost this epic is against [src: EP-001/Q-001].

## Success measures

- In one shell session, a person can create a named envelope, add income to it, record a spend
  against it, and read the amount remaining in it, using only commands this tool provides.
- The tool is quit between every one of those steps and the figures are unchanged: values
  written by one invocation are read back by a later, separate invocation on the same machine.
- Asking the tool for a month's summary prints per-envelope figures that reconcile arithmetically
  for that month: for each envelope, money added minus money spent in the month equals the change
  in that envelope's remaining amount across the month.
- Running any of the above requires no server, daemon, database process or network access: the
  whole sequence completes with no other process started by the user or the tool.
- Recording a spend against an envelope that does not exist is refused with a message that names
  the envelope, rather than silently creating one or failing with a stack trace.
- Recording a spend larger than the amount left in its envelope is refused: the spend is not
  recorded, the envelope's amount is unchanged, and the message says how much is left. No
  envelope ever shows a negative amount [src: EP-001/Q-002].
- Money left in an envelope when a calendar month ends is still in that envelope on the first
  day of the next month: a summary of the new month starts from the amount carried over rather
  than from zero [src: EP-001/Q-001].
- A person can move an amount from one envelope to another, and can correct a spend they already
  recorded so that a summary of the month it fell in shows the corrected figure
  [src: EP-001/Q-005].

## Scope

- Creating named envelopes and listing them with the amount remaining in each.
- Putting income into a named envelope.
- Recording a spend against a named envelope, so the remaining amount reflects it.
- A summary for a month.
- Moving an amount from one envelope to another (`WI-0004`).
- Correcting a spend that was already recorded (`WI-0005`).
- Storing the data on the local machine so it survives between runs.
- Python, and no services.

## Out of scope

- Anything multi-user: sharing, accounts, permissions, or two people using one set of envelopes.
- Any server, daemon, hosted service, sync, or network access of any kind — the stakeholder said
  "no services" and this is that exclusion written down.
- Importing from a bank, a CSV, or another budgeting product, and exporting to one.
- Forecasting, projections, goals, or advice about how money should be allocated.
- Automatic or recurring transactions, scheduling, and reminders.
- More than one currency, and any currency conversion.
- A graphical, web or full-screen terminal interface.
- Reporting periods other than the month-level summary asked for.
- Encryption, password protection, or any other protection of the stored data beyond ordinary
  file permissions.

## Notes

- Who this is for, and what they use today, was answered at `EP-001/Q-001`: the stakeholder
  themselves and nobody else, for the household budget, and today a spreadsheet with a tab per
  month. Their reply also stated the rule they were most concerned we would get wrong — money
  left in an envelope at the end of a month stays in that envelope — which is now a success
  measure above.
- The command the tool is invoked as is `envel` [src: EP-001/Q-006]. The exact wording of its
  output is not decided here; that is for `refine` and `plan`.
- `EP-001/Q-005` widened the scope: the stakeholder asked for both moving money between
  envelopes and correcting a spend they had already recorded. Those are `WI-0004` and `WI-0005`,
  filed by `answer-questions` rather than folded into the existing items.
- **Two rules the stakeholder settled on `WI-0001` hold across every item in this epic**, and are
  recorded here so that `WI-0003`, `WI-0004` and `WI-0005` inherit them rather than re-asking:
  - **Amounts.** At most two decimal places on the way in, exactly two on the way out, and
    nothing rounded — *"the figures have to add up"* [src: WI-0001/Q-002]. One currency. How the
    amounts are held internally they left to us in so many words.
  - **Envelope names.** Matched without regard to capitalisation, shown back the way they were
    first typed, and not restricted in what characters they may contain beyond the empty name
    and a leading or trailing space [src: WI-0001/Q-004].
- **`EP-001/Q-009` is the stakeholder's reply to the sign-off, and it opened nothing.** They kept
  the tool as it stands — *"Ship it as it stands"* — and answered in their own words rather than
  picking one of the four options. Two things in it bind later work. First, the monthly summary is
  parked: *"don't build on it, don't keep it open as work, we're not doing it this round … I asked
  for it at the start and I've changed my mind."* What they parked is further work on it, not the
  command: `envel summary` was delivered under `WI-0003` and stays delivered, in scope, and shipped.
  Second, the one change the sign-off offered them — the `left` column of a short month reading
  `short 250.00`, which was the pipeline's wording and not theirs — they declined to spend a round
  on, and it is parked with the summary. So no follow-up item is filed under this epic from this
  answer, and the wording stands as built with its authorship recorded in
  `docs/product/vision.md` rather than attributed to them [src: EP-001/Q-009].
