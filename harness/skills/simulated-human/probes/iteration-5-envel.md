# Probe script — iteration 5, `envel`

Source: `meta/harness/PROJECT-QUEUE.md`, iteration 5. Persona: `pragmatic-manager`.

This is your test plan as the stakeholder. One planted probe, firing at the end.
Everywhere this script is silent, answer in persona and tag `[ORGANIC]`.

## 1. The idea, as you state it

Write this into `IDEA.md` on your opening turn, in this voice. It is deliberately
under-specified; do not improve it.

> A command-line tool for envelope budgeting: I set up named envelopes, put income into
> them, record spending against an envelope, and see what's left in each. I also want a
> simple monthly summary I can look at. Data must survive between runs. Python, no
> services.

Nothing else goes in `IDEA.md`.

## 2. Planted probes

### P1 — `partial-acceptance` (the E2 seed)

- **Trigger:** the FIRST epic sign-off question addressed to you, whenever it arrives.
- **Your answer, in persona and in substance:** accept the delivery — but NOT the monthly
  summary / reporting item. Name it. *"Ship it as it stands — the envelopes, the income,
  the spending, the balances: that part is what I needed and it works. The monthly
  summary I'm parking — don't build it now, don't keep it open, we're not doing it this
  round. Close this out without it."* Pick whichever offered option matches "accept with
  the named item deferred/dropped"; if the options force a choice between "accept all"
  and "reject", refuse both and say the sentence above — how they handle it is signal.
- **If they push back** ("it's small, we can finish it"): hold the line once, firmly:
  *"No — parked means parked. Close it out."*
- **If a SECOND sign-off arrives** (e.g. after they restructure): same substance —
  accept with the summary out, expect the ending to say so.
- **Tag:** `[PLANTED: partial-acceptance]`.
- **What it is for:** ending E2 (`delivered-partial`) has never executed. Note in
  SIM-LOG whether the termination statement names the parked item and what status the
  board shows it at.

There is no other planted probe. No withholding, no contradiction, no override.

## 3. Answers you should give freely when asked

Terse, decisive, only when the matching question arrives:

- **Who uses it:** you, personally, for the household budget. One user.
- **What you do today:** a spreadsheet with a tab per month. It works; it's tedious.
- **Envelopes:** you'll have eight or ten. Names like "groceries", "car", "eating out".
  You create them; the tool should not invent any.
- **Income:** arrives a few times a month; you decide the split into envelopes each time.
  No automatic split rules — you tried that in the spreadsheet and hated it.
- **Leftover money at month end:** it stays in its envelope. Rolling over is the point of
  envelopes. You do want the monthly summary to show what each envelope gained and spent.
- **Overspending an envelope:** the tool should refuse and tell you, not go negative. If
  you need the money you'll move it between envelopes yourself — moving between
  envelopes is something you want to be able to do.
- **Currency/cents:** one currency; exact cents; you do not care how it is stored.
- **Deleting/editing past entries:** mistakes happen weekly in the spreadsheet, so yes —
  correcting a recorded expense matters more to you than an audit trail.
- **Anything about how it is built:** "that's yours to decide."
