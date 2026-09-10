---
title: Envelope budgeting at the command line
version: 3
status: current
updated: 2026-09-10T14:59:10Z
updated-by: answer-questions
updated-for: WI-0002
---

# Envelope budgeting at the command line

## Who this is for

One person, budgeting their own money on their own machine. They already divide their income
into named pots — groceries, rent, petrol — and decide what they can spend by looking at the pot
rather than at their bank balance. Today they do that on paper or in a spreadsheet, and every
balance is arithmetic they do themselves.

They are comfortable at a terminal. They are not asking for an app, and they are not asking to
be told how to budget: the method is theirs and already works. What they want is the arithmetic
and the remembering taken off their hands.

## What it is for

Six things. The first four are the shape of what they described; items 4 and 5 came out of
asking them what else mattered, and they carry as much weight as the rest [src: EP-001/Q-005].

1. Naming the envelopes they budget into.
2. Putting income into them — straight into a named envelope, decided at the moment the money
   arrives. The tool does not hold a pool of unassigned money and does not work out a split for
   them; they tried that in a spreadsheet and disliked it [src: EP-001/Q-002].
3. Recording what they spend, against the envelope it came out of. A spend larger than what is
   in that envelope is refused rather than recorded: they want an envelope's number to remain
   the truth, and a negative balance is a number that has stopped being one [src: EP-001/Q-003].
4. Moving money from one envelope to another. This is how they cover a shortfall themselves, and
   it is what makes the refusal in 3 workable rather than obstructive [src: EP-001/Q-005].
5. Correcting or removing a spend they have already recorded. They make that mistake weekly in
   the spreadsheet today, and they care much more about the number being right afterwards than
   about keeping a trail of having got it wrong [src: EP-001/Q-005].
6. Telling them what is left in each envelope, and summarising a month: for each envelope, what
   it took in and what went out of it [src: EP-001/Q-005]. What is left is shown by the same
   listing that names the envelopes, rather than by a command of its own: "the number is the whole
   reason I open the tool; I'm not going to type a second command to see it"
   [src: WI-0002/Q-001].

A transaction carries the date it happened. Typing nothing gets today, which is the ordinary
case; catching up after a few days away means giving the real date, so that a month's summary is
about the month it names [src: EP-001/Q-004].

Everything they record is kept on their own machine and is still there the next time they run
the tool. That is a requirement they stated, not an implementation preference, and it is the
line between a tool and a calculator.

## What it deliberately is not

- **Not a service.** There is nothing to host, nothing to sign into, and no reason for it to
  reach the network. The stakeholder said "no services", and this vision reads that at its
  widest: no server, no daemon, no account, no sync. They have since confirmed that widest
  reading in their own words — "no network for anything" — so it is a decision of theirs and not
  an inference of ours [src: EP-001/Q-001].
- **Not a ledger of your bank.** It knows what the person tells it. It does not import
  statements, reconcile against a bank, or try to discover transactions they did not record.
- **Not multi-user.** One person, one set of envelopes, one data store. No sharing, no
  permissions, no second device. Confirmed by the stakeholder: "it's my machine and my data, just
  me using it" [src: EP-001/Q-001].
- **Not a planner.** It records what happened and reports it. Forecasts, targets, recurring
  allocations and rollover rules between months are somebody else's product.
- **Not a sweeper.** What is left in an envelope at the end of a month stays in that envelope. It
  is untouched by the turn of the month, and the monthly summary reports a month's movement
  against a balance that simply carries on [src: EP-001/Q-005].
- **Not a general finance tool.** One currency — pounds and pence, which they have said is not
  changing — and an amount they type is the amount that is stored: a figure with more than two
  decimal places is refused rather than quietly rounded to the nearest penny
  [src: WI-0002/Q-002]. No investments, no debts, no tax.

## How we will know it works

The person can create an envelope, put money in it, spend against it, and see a balance that is
the one they would have worked out on paper — and can close the terminal, come back, and find
the same numbers. If they have to check the tool's arithmetic, it has failed, and if they have
to re-enter anything after a restart, it has failed.

## Engagement state

- The stakeholder stated this idea and has not been asked to accept anything yet; no ending has
  been proposed to them.
- Five questions from intake are open with them (`EP-001/Q-001` … `EP-001/Q-005`): four
  blocking ones about scope, and one non-blocking elicitation asking what else matters to them.
- Nothing has been designed or built. The epic has three work items, all at `draft`, and none
  has passed refinement.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-10T14:59:10Z | answer-questions | WI-0002 | The stakeholder's three WI-0002 answers propagated: what is left in each envelope is shown by the same listing that names them rather than by a second command, and the currency is pounds and pence with an over-precise amount refused rather than rounded |
| 2 | 2026-09-10T13:26:31Z | answer-questions | EP-001 | The stakeholder's five intake answers propagated: income goes straight into an envelope, an overspend is refused, a transaction carries the date it happened, moving money between envelopes and correcting a recorded spend are part of the product, and a leftover balance is not swept at the turn of the month |
| 1 | 2026-09-10T13:16:05Z | intake | EP-001 | First version: who envelope budgeting at the command line is for, the four things it does, and what it deliberately is not |
