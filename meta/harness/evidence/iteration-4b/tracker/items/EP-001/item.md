---
id: EP-001
type: epic
title: A flashcard tool that schedules its own reviews
status: done
priority: high
created: "2026-08-30T01:29:17Z"
updated: "2026-08-30T06:07:34Z"
outcome: delivered
---

## Goal

Someone learning a body of material keeps their own deck of question-and-answer cards in this
tool, sits down with it once a day, and is shown exactly the cards they are close to forgetting
— not the whole deck. How well they recalled each card decides when they next see it: the ones
they know come back less often, the ones they fumble come back sooner. Shutting the tool down
and returning tomorrow, or next week, loses none of that; the deck and every card's schedule are
still there.

## Why now

Reviewing a whole deck every day does not scale past a few dozen cards, and reviewing at random
means the cards you nearly know get the same attention as the ones you know cold. Spaced
repetition is the well-established answer, but it is only useful if something remembers the
schedule for you — which means the tool has to hold state across sessions, not just show cards.
The stakeholder did not state a deadline or an external trigger, and none is recorded here; the
cost of not building it is simply that the learning stays manual.

## Success measures

- Adding a card, exiting the tool, and starting it again shows that card still present. A person
  can check this in one terminal with two runs and no other setup.
- A review session presents only cards whose next-review date is today or earlier. A card that
  has just been reviewed and scheduled forward is absent from a second review run on the same
  day.
- Across a sequence of reviews of one card, the gap to its next review follows the ladder
  `1, 3, 7, 30` days: a correct answer moves the card up one rung and holds it at 30 days once
  there, a wrong answer sends it back to one day. Checkable by reading the card's stored
  next-review dates after each graded answer and comparing them with a calendar. The rule is
  `ADR-0002`, from the stakeholder's answer to `EP-001/Q-003`.
- Someone with this repository, a terminal, and no other context can follow the project's own
  documentation to add a card and to run a day's review, without reading the source. The
  interface is a command-line one — `recall add`, `recall list`, `recall review` — per
  `ADR-0001`, from the stakeholder's answer to `EP-001/Q-002`.
- A day's review sitting does not drag on. The stakeholder named this as one of the two things
  that would make the tool a failure: *"a review session that drags on more than a couple
  minutes"* (`EP-001/Q-001`). What makes it decidable — the deck size it is measured at, and
  whether the tool caps how many cards one sitting presents — was left for WI-0002's refinement
  to pin down with the stakeholder, and it did: they refused a cap and reconciled the two
  sentences themselves — *"No limit — A. Show me everything that's due. If it's a big pile after
  a week away I'll just stop partway, that's fine by me."* (`WI-0002/Q-001`). So this measure has
  no threshold and nothing measures it: a sitting presents every due card, and the couple of
  minutes is a design target the stakeholder chose not to make a rule. They were told that
  plainly at sign-off — *"Your 'couple of minutes' sitting is not a criterion anywhere"* — and
  accepted the engagement on that basis (`EP-001/Q-004`).
- Progress is not lost. The other failure the stakeholder named: *"don't lose my progress —
  that's the one thing that would make this a failure"* (`EP-001/Q-001`). Concretely: the deck
  and every card's schedule live in a file on the person's own machine that survives the process
  ending and survives a reboot. That file's location is fixed —
  `~/.local/share/recall/deck.json`, derived from the home directory and from nothing else, with
  no flag, no environment variable and no configuration file for pointing `recall` elsewhere
  (`ADR-0004`). The stakeholder confirmed at `EP-001/Q-005` that this is what they asked for:
  *"a fixed file under my home directory is exactly what I asked for."*

## Scope

- Creating cards that have a question side and an answer side, held by the tool itself.
- A review session over the cards that are due, in which the person records how well they
  recalled each card.
- A scheduling rule that turns those recorded answers into each card's next review date.
- Storage that survives the process exiting and a reboot: a file on the machine the tool runs
  on, per the stakeholder — *"Storage should just be a file on my machine that survives a
  reboot"* (`EP-001/Q-001`). Which file, and in what format, is `plan`'s.
- Removing a card from the deck, which the stakeholder asked for in answer to `EP-001/Q-001`.
  Carried by WI-0004.

## Out of scope

These were exclusions intake derived, not exclusions the stakeholder stated, and `EP-001/Q-001`
was the place to contradict them. The stakeholder has now answered it. Deleting a card is no
longer excluded — it is WI-0004 — and everything below survived the answer: they confirmed one
person, one machine, a terminal, once a day, learning vocabulary.

- More than one person using the tool: accounts, login, per-user decks, sharing. Assumed to be
  one person on one machine.
- Syncing between devices, or any network or hosted service.
- Importing or exporting other flashcard formats — Anki packages, other tools' CSV.
- Anything on a card other than text: images, audio, rich formatting.
- Statistics, streaks, dashboards or gamification beyond what a single review session needs to
  show.
- More than one deck, or choosing between decks.
- **Editing** a card once it has been added. Deleting one is now in scope (WI-0004); the
  stakeholder drew the line themselves — *"I want to be able to delete a card I don't need
  anymore; editing can wait"* (`EP-001/Q-001`).
