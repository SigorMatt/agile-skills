---
id: EP-001
type: epic
title: A flashcard tool with daily spaced-repetition review
status: done
outcome: delivered
priority: high
created: "2026-08-30T11:03:50Z"
updated: "2026-08-30T13:39:15Z"
---

## Goal

Someone studying a subject can write down the things they want to remember as flashcards, and
then, once a day, be shown only the cards that are due for them right now — not the whole pile.
Cards they find hard come back soon; cards they know come back later. Everything they have
entered, and everything the tool has learned about how well they know each card, is still there
the next day, and the day after that.

## Why now

The stakeholder stated the idea as a whole: "A flashcard tool: add cards, review due cards
daily, simple spaced repetition. Progress persists." Nothing exists yet — this repository is
empty of product code — so the cost of not doing it is that there is no tool at all. The reason
to settle the shape now rather than later is that "progress persists" is a durability promise:
whatever storage format the first version writes, real study data starts accumulating in it
immediately, and changing it afterwards means either migrating a user's history or losing it.

## Success measures

Rewritten from the stakeholder's answers to `EP-001/Q-001` to `EP-001/Q-005`; the vague ones
intake wrote before those answers are gone.

- A person can add a card from a terminal, restart the machine, run a review the next day, and
  that card is offered — with no re-entry of anything.
- On a day when some cards are due and others are not, a review session offers exactly the cards
  whose due date is today or earlier, and a reader can check that set against the stored file by
  hand.
- A card answered wrong in a session is due again the next day; a card answered right is due 1, 3,
  7 or 30 days later according to its rung; and both new due dates are visible in the stored file.
- A session started a second time on the same day offers only what is still due, and offers no
  card that was already answered that day.
- A review session offers every card that is due and withholds none of them, and it says how many
  they are before it shows the first one, so a person facing a backlog is told its size rather
  than discovering it card by card.
- Stopping a session part-way is a supported way to end it, and killing the tool part-way does not
  lose the answers already given in it either: in both cases the cards already answered keep their
  new schedule and the rest are unchanged and still due.
- A person can delete a card they no longer want, and it stops being offered.
- The whole of the data — cards and their scheduling state — lives in a file on the person's own
  machine and survives a reboot of it.

## Scope

- Entering new flashcards, each a front and a back of one line of text, and having them stored
  durably in a file on the local machine.
- Deleting a card that is no longer wanted.
- Selecting, each day, the cards whose due date is today or earlier.
- Recording right or wrong for each answered card and moving it along the fixed ladder of 1, 3, 7
  and 30 days, per `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`.
- Persisting cards and their scheduling state across restarts of the tool and of the machine.
- A command-line interface, per `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`.

## Out of scope

- Multiple decks, tagging, or any grouping of cards beyond one collection. The stakeholder
  described one pile of cards; grouping is a separate body of work if they want it.
- More than one user, accounts, or syncing between machines or devices.
- Editing a card after it has been added. The stakeholder's own words: *"I want to be able to
  delete a card; editing can wait"* (`EP-001/Q-004`) — so deletion is now in scope as WI-0003 and
  editing is not.
- Importing or exporting other flashcard formats (Anki, CSV, Quizlet).
- Rich card content: images, audio, formatting, cloze deletions. Cards are one line of text a
  side, which the stakeholder confirmed (`EP-001/Q-004`).
- Reminders, notifications, or anything that makes the daily review happen on its own.
- Statistics, streaks, graphs, or any reporting beyond what a review session itself shows.
- Choosing the spaced-repetition algorithm from a menu at runtime. One stated rule, applied to
  every card.
- A graphical or browser interface. The stakeholder chose the command line knowing the
  alternatives (`EP-001/Q-001`).

## Notes

Two of the stakeholder's statements were in tension and they settled it themselves in
`EP-001/Q-005`: a session shows every due card with no cap (`EP-001/Q-003`) against a review over
a couple of minutes being a failure (`EP-001/Q-004`). Their choice was no cap plus visibility —
*"I'd rather see the honest number of cards waiting than have the tool quietly decide which ones I
don't get to see today"* — with quitting part-way a supported exit. Recorded in
`docs/architecture/adr/ADR-0003-session-composition-no-cap-stated-count-clean-quit.md` and carried
into WI-0002's AC2, AC10 and AC11.

No success measure above constrains how long a session takes, and after that answer none should:
they accepted a long sitting after a backlog in exchange for seeing its size. Keeping sessions
short is a habit the tool supports rather than a property it enforces.

The stakeholder delegated the technology: *"As for how it's actually built — whatever you think is
best"* (`EP-001/Q-004`). `plan` chooses the language, the file format and the packaging, and
records that choice as its own ADR.

The stakeholder accepted the engagement at its ending. Asked in `EP-001/Q-006` — the sign-off
question, which named all three children and the four endings available — they chose **A, accept
as complete**: *"A — accept as complete. This is what I asked for and it works. Nothing else comes
to mind right now; if I want more later I'll open something new."* That selects the outcome
`delivered` rather than `delivered-partial`, an impasse or a withdrawal, and it names no follow-up
work, so no item was filed from it. `review-close` records the ending; this note records what the
answer was and what it chose.

One caveat travelled with that acceptance and is written here so the measure it qualifies is not
later read as fully demonstrated. The last success measure above — the data lives in a file on the
person's own machine and survives a reboot of it — is met as to the file, which every item's
verification exercised, and **untested as to the reboot itself**: nothing has been run against a
real restart of a machine, only against stopping and starting the tool. The sign-off said so
plainly before asking, so the acceptance is of a tool with that gap in its evidence rather than in
spite of an undisclosed one.
