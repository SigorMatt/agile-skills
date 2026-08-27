---
id: EP-001
type: epic
title: Track and settle shared expenses in a friend group from the command line
status: blocked
priority: high
created: "2026-08-26T23:21:56Z"
updated: "2026-08-27T02:40:24Z"
---

## Goal

Someone in a friend group can sit at a terminal, record who paid for what and who shared it,
and at any moment ask the tool who owes whom — instead of keeping the arithmetic in their head
or typing every line by hand. Expenses can also arrive from their bank's CSV export rather than
being typed in one at a time. Whatever has been recorded is still there the next time the tool
is run.

## Why now

The stakeholder's statement is that they type shared expenses in themselves today and want the
bank's CSV export to do that for them, and that they want to be able to ask "who owes whom" at
any point rather than working it out. What they use today to reach that answer is not recorded,
and this intake did not establish it — see the journal on this epic.

## Success measures

- Starting from an empty data store, a person at a terminal can add the group's members, record
  an expense paid by one member and shared by a named subset of members, and print a who-owes-whom
  report, using only documented commands and without hand-editing any data file.
- Running the report command a second time, in a new process, prints the same figures as the
  first — so the data demonstrably survived between runs.
- At least one expense enters the store from a bank CSV export file rather than from typed
  command arguments, and appears in the report.
- Every command in the measures above completes on a machine with no network access, using
  python3 and its standard library only.

## Scope

- Adding and listing the people in the group.
- Recording an expense: an amount, the person who paid it, and the people who shared it — some
  or all of the group.
- Keeping people and expenses on local disk so they survive between runs.
- Importing expenses from the stakeholder's bank CSV export.
- Reporting who owes whom, on demand, as a list of payments that settles the group (EP-001/Q-002).
- Deleting a person or an expense recorded by mistake (WI-0004). Added to this epic on
  2026-08-26 after the stakeholder answered `WI-0001/Q-003`; scheduled after WI-0002 at their
  request, and `medium` because the goal and the success measures above are coherent without it.
- A command-line program in Python, standard library only, no external services.

Two of the three facts this epic was suspended on are now settled by the stakeholder, and one
is not:

- **Settled (Q-002).** "Who owes whom" means a list of specific payments that settles the group,
  not each person's net position — *"The list of payments that settles it."* WI-0002 is written
  against that.
- **Settled (Q-003).** The delivery order was delegated to us and decided: WI-0001, then WI-0002,
  then WI-0003. The stakeholder also refused to drop any of the three — *"the import's part of
  what I asked for too"* — so WI-0003 is `high` priority, not optional. WI-0004, added later, sits
  after WI-0002 by the stakeholder's own constraint on it.
- **Outstanding (Q-001).** The layout of the bank's CSV export is still not known: the
  stakeholder replied *"I'll send you a sample later."* WI-0003 is therefore parked at `blocked`
  until a sample or the column layout arrives. Nothing was invented in its place. The rest of the
  epic proceeds; this epic cannot end as fully delivered until that item moves.

## Where the engagement stands

On 2026-08-27 the stakeholder was asked, in `EP-001/Q-004`, whether they accept this engagement
as it stands: five of six children delivered, and the bank CSV import (WI-0003) not delivered for
want of a sample of their bank's export. **They did not accept it.** Their words:

> No, not as it stands — the bank import was part of what I asked for and it isn't there.
> Everything else looks right. I'll send the file and then we can finish it.

What that means for this epic:

- It selects **ending E3, the impasse** (`ids-and-statuses.md` §3.5): every child is terminal,
  one was not delivered, and the stakeholder did not accept. The epic ends at `blocked`, not at
  `done`. That is a legitimate ending and the honest one — it is what "no" was given somewhere to
  go for. `review-close` records it; nothing further is scheduled until then.
- The refusal is confined to WI-0003. *"Everything else looks right"* accepts WI-0001, WI-0002,
  WI-0004, BUG-0001 and BUG-0002 as delivered, and the reply names no defect, no missing
  criterion and no new scope. Nothing was reopened and no new item was filed.
- **What would end the impasse:** the sample of the bank's CSV export the stakeholder says they
  will send — or its header row and two or three example rows. That unparks WI-0003
  (`WI-0003/item.md` §Notes lists exactly what is needed), and a delivered WI-0003 would bring
  the engagement back to rest with every child delivered, at which point a fresh sign-off is due
  and the ending can be E1 instead.

The ending was recorded by `review-close` on 2026-08-27, against the epic Definition of Done
criterion by criterion — `artifacts/review.md` carries the seven results with their evidence, the
claims in `docs/` re-checked against the running code, and two findings: a wrong example command
in `Q-004` (corrected in place, in that file, without rewriting what the stakeholder read) and a
sentence in `docs/product/vision.md` that presented the unbuilt CSV import as a current
capability (fixed in v5). The epic carries **no `outcome`**: `blocked` is an impasse, not a
closure, and recording `delivered-partial` here would claim an acceptance that was refused.

## Out of scope

- Moving money. The tool reports what is owed; it does not pay, transfer or settle anything.
- Any network call, hosted service, account or login — excluded by the stakeholder's own words.
- Sharing one dataset across several people's machines, or any form of sync or merge.
- More than one group in one data store, unless the stakeholder later asks for it.
- Converting between currencies.
- **Editing** a person or an expense in place. Offered to the stakeholder alongside deletion in
  `WI-0001/Q-003` and not chosen — *"being able to delete a mistake matters more to me than
  editing one"* — so a correction is a deletion and a re-record. Nothing is scheduled for it.
- A graphical or web interface.
