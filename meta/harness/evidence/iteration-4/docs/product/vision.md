---
title: Recall — product vision
version: 4
status: current
updated: 2026-08-29T14:06:18Z
updated-by: answer-questions
updated-for: EP-001
---

# Recall — product vision

## Who this is for

One person, learning something by heart on their own machine: vocabulary for a language they are
studying, definitions for an exam, facts they keep forgetting. They already know what they want
to memorise. What they do not have is a way to be told, each day, which of it to look at.

They are not a team, not a classroom, and not a customer of a service. Nothing in this product
assumes a second person exists.

## What it is for

Recall turns a pile of things-to-remember into a daily, finite review. The user writes each thing
down as a card with a question side and an answer side. Once a day they review, and the tool
shows them only the cards that are due — not the whole pile. It records what they got right and
what they got wrong, and it uses that to decide when each card comes back: right answers push a
card further out, wrong answers bring it back soon.

Recall is a **command-line tool**, run in a terminal. The stakeholder settled that in answer to
`EP-001/Q-001` — *"Command-line tool. I'll be sitting at a terminal doing this once a day,
that's all it needs to be."* [src: EP-001/Q-001] There is no web page, no server and no
graphical interface; a review session is text in a terminal. That choice is what lets every
acceptance criterion in this epic be decided by running a command and reading its output.

All cards live in **one flat pool**. There are no decks, tags or categories, and a review covers
everything that is due [src: EP-001/Q-004].

Everything the user has done accumulates. Progress is stored on disk and survives closing the
tool, which is the only reason the intervals can grow at all. A flashcard tool without
persistence is a list; the persistence is the product.

## What it deliberately is not

- **Not a sync service.** No accounts, no server, no sharing, no second device.
- **Not a rich editor.** Card sides are plain text. No images, audio, formatting or LaTeX.
- **Not an import target.** It does not read Anki, Mnemosyne or CSV decks.
- **Not a dashboard.** No streaks, retention curves or statistics beyond what a review session
  itself reports.
- **Not configurable scheduling.** There is one scheduling scheme, the same for every card and
  every user, and it is not tunable [src: ADR-0001].
- **Not a deck manager.** One flat pool of cards; no decks, tags or categories
  [src: EP-001/Q-004].
- **Not a reminder.** Nothing runs unless the user starts it.
- **Not a card editor.** A card's text cannot be changed after it is added. The stakeholder was
  asked twice and left it out both times: *"editing can wait"* [src: EP-001/Q-005], and then, at
  the final sign-off, *"I don't have anything else I want built right now"* [src: EP-001/Q-006].
  Removing a card is different, and is built — see below.

## What the user can do to a card once it exists

Cards accumulate, and so do mistakes. The stakeholder settled the shape of this at sign-off,
having been offered three candidates by name and having taken one [src: EP-001/Q-005]:

- **Delete a card** they added by mistake — *"the one thing from your list I actually want next"*.
  Built and delivered as `WI-0004`: `recall delete <n>` removes one card at once and prints what
  it removed [src: WI-0004].
- **Change a card's text** — deliberately not yet. *"Editing can wait."*
- **See or change a card's schedule from a command** — declined. Opening the store file and
  editing `due` or `interval` by hand stays the way to move a card [src: EP-001/Q-005; ADR-0007].

Nothing else acts on an existing card, and nothing else is planned to. Offered all three
candidates again at the final sign-off, the stakeholder took none of them and accepted the tool as
it stands [src: EP-001/Q-006].

## How the schedule behaves

The stakeholder chose a fixed interval ladder over an adaptive algorithm, and a binary result
over a finer grade [src: EP-001/Q-002; EP-001/Q-003]. In their words: *"A card I get right comes
back later each time — one day, then three, then a week, then a month. Get it wrong and it goes
back to the start."*

- The intervals are **1 day, 3 days, 7 days, 30 days** [src: ADR-0001].
- A new card is due the day it is added.
- Right moves a card up one rung; a card already at 30 days stays at 30 days.
- Wrong sends a card back to the bottom rung, so it comes round again the next day — not the
  same day.
- At review the user records only **right or wrong**. There is no four-point grade and no ease
  factor per card [src: ADR-0001].

`ADR-0001` is the authoritative statement of this, including the one thing the stakeholder's
answer left open — whether the ladder has a 14-day rung — and how it was decided.

## Where this stands

Recall as described above is **finished and accepted**. The stakeholder was shown the whole tool
run end to end — adding, listing, deleting, a review session, the ladder moving a card 1 → 3 → 7
days and a wrong answer sending it back to 1 — and accepted it as complete: *"Add, review, the
schedule, and now delete — that's the whole thing I asked for, and the transcript shows it
working. I don't have anything else I want built right now, so close it out."* [src: EP-001/Q-006]

That closes `EP-001`. Everything in *"What it deliberately is not"* stays out, and anything the
stakeholder wants later — editing, decks, statistics, a different schedule — begins as a new
request rather than as a continuation of this one.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-08-29T14:06:18Z | answer-questions | EP-001 | The stakeholder's answer to Q-006: the engagement is accepted as complete and EP-001 closes. `recall delete` recorded as built rather than coming; editing, a schedule-view command and statistics declined a second time; new section 'Where this stands' |
| 3 | 2026-08-29T13:20:30Z | answer-questions | EP-001 | The stakeholder's answer to Q-005: deleting a card is in scope (WI-0004), editing a card and a schedule-view command are not. New section 'What the user can do to a card once it exists' |
| 2 | 2026-08-29T10:52:22Z | answer-questions | EP-001 | The stakeholder's answers to Q-001..Q-004: command-line interface, one flat pool of cards, a 1/3/7/30-day ladder and a right-or-wrong result. Replaced "What is not yet decided" with "How the schedule behaves" |
| 1 | 2026-08-29T10:45:17Z | intake | EP-001 | First version, from the stakeholder's opening statement |
