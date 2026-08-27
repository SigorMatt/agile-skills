---
id: WI-0003
type: work-item
title: Import expenses from a bank CSV export
status: blocked
priority: high
epic: EP-001
depends-on:
  - WI-0001
created: "2026-08-26T23:22:40Z"
updated: "2026-08-26T23:32:30Z"
---

## Story

As someone who shares costs with friends, I want to import expenses from my bank's CSV export,
so that I do not have to type each one in by hand.

## Acceptance criteria

- [ ] AC1 — a documented command reads a CSV file exported by the stakeholder's bank and records
      the expenses in it, so that they appear in WI-0001's expense listing
- [ ] AC2 — a row the command cannot turn into an expense is reported to the user, identifying
      the row, and no partial expense is recorded for it

## Out of scope

- Connecting to a bank, downloading a statement, or any network access.
- Any export format other than the CSV the stakeholder's bank produces.
- Categorising or matching transactions against anything.

## Notes

- **This item is parked, and one thing unparks it.** EP-001/Q-001 asked the stakeholder what
  their bank's CSV export looks like. Their reply was *"I'll send you a sample later."* That
  refuses inventing a layout and refuses dropping the item, but it does not supply the layout,
  so neither acceptance criterion here can yet be made decidable and the item cannot be refined
  or planned. It is at `blocked` with `resume-to: draft`.
- **What would unblock it:** a sample of the bank's CSV export — amounts or names changed if
  preferred — or failing that its header row and two or three example rows, saying which column
  holds the amount, the date and the description. Nothing else is needed to restart this item.
- The stakeholder refused to drop it: *"I don't want to drop either one, the import's part of
  what I asked for too"* (EP-001/Q-003). That is why it is parked rather than closed as
  `dropped`, and why its priority is `high` — the epic is not coherent without it. The
  consequence is that EP-001 cannot end as fully delivered while this item sits here; when the
  engagement reaches rest, the termination question will name it as not delivered and put the
  choice back to the stakeholder.
- Delivery order, from EP-001/Q-003: WI-0001, then WI-0002, then this item. The stakeholder
  delegated the order and `answer-questions` chose it. The `high` priority does not disturb that
  order — the orchestrator breaks a priority tie on `created` ascending, and WI-0002 is older.
- A CSV row does not say who shared the expense, only who was charged. How the importer learns
  the sharers is still open, still a consequence of the layout, and still refinement's to settle
  once the sample exists. This answer did not touch it.
- **Refused to let it go, a second time.** At sign-off on 2026-08-27 the stakeholder was asked
  whether they accept the engagement without this item and answered no — *"the bank import was
  part of what I asked for and it isn't there… I'll send the file and then we can finish it"*
  (`EP-001/Q-004`). That is why this item stays parked at `blocked` with `resume-to: draft`
  rather than being closed as `dropped`, and it is why EP-001 ends at the impasse (E3) instead of
  as delivered. Nothing about what would unblock it has changed.
- Depends on WI-0001: an import has nowhere to put an expense until expenses can be recorded.
