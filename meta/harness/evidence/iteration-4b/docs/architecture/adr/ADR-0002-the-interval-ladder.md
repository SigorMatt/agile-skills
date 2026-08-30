---
title: Right-or-wrong grading over a fixed interval ladder of 1, 3, 7 and 30 days
version: 3
status: current
updated: 2026-08-30T03:38:18Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0002 — Right-or-wrong grading over a fixed interval ladder of 1, 3, 7 and 30 days

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** the stakeholder, answering `EP-001/Q-003`, `WI-0002/Q-002` (for §3) and
  `WI-0003/Q-001` (for §5); recorded by answer-questions (architect)
- **Supersedes:** —

## Context

"Simple spaced repetition" was the stakeholder's phrase and it does not name a rule. Which rule
decides how many answers a person chooses between after each card, what WI-0003's criteria say,
and whether a reader can work out a next-review date by hand [src: WI-0003 AC3]. Intake filed it
as `EP-001/Q-003` and suspended the epic on it [src: EP-001/Q-003].

The stakeholder answered: *"Just right or wrong, no rating scale. If I get it right it comes back
later each time — a day, then three, then a week, then a month or so. If I get it wrong it goes
back to the start."* [src: EP-001/Q-003]

That is a doubling-ladder shape — the question's option A — with the rungs named explicitly, and
those rungs are not the ones option A offered. The stakeholder's rungs win.

## Options considered

The three the question put to them, and one clause the answer left open.

- **A — a ladder with two answers.** Cost: the least of the three; a person can predict every
  date in their head. Risk: coarse — a card nearly known and a card not known at all are treated
  the same. **Chosen**, with the stakeholder's own rungs.
- **B — Leitner boxes.** Cost: similar. Risk: the schedule belongs to the box rather than the
  card, which is a different mental model from the one the answer describes.
- **C — SM-2 with an ease factor and a 0-5 rating.** Cost: materially more — per-card ease is
  extra stored state and its own arithmetic. Risk: explicitly refused — *"no rating scale"*
  [src: EP-001/Q-003].
- **The clause the answer did not settle: what happens above the last rung.** The stakeholder
  named four intervals and stopped at *"a month or so"*.
  - **(i) The ladder tops out.** A card at 30 days that keeps being recalled stays at 30 days.
    Cost: none. Risk: the gap stops growing, so WI-0003 AC1 as intake wrote it — *strictly*
    longer each time — becomes false at the top and has to be amended.
  - **(ii) The ladder keeps growing** past a month, by some rule nobody stated.
    Cost: invents an interval the stakeholder did not name. Risk: a deck could put a card out of
    reach for a year on a rule they never chose.
  **(i) is chosen.** It began as this ADR's own reading of *"a month or so"* — what they
  enumerated, and "simple" was their word for the whole thing — and it was flagged for `refine`
  to confirm with them. It has been: `refine` put all three shapes to them as `WI-0003/Q-001`,
  with the cost of (i) spelled out, and they chose (i). *"Stops at a month — option A. The whole
  point was simple, and I don't want to be doing math to figure out when a card's coming back."*
  [src: WI-0003/Q-001]. It is no longer a reading.

## Decision

1. **Two answers, not a scale.** A reviewed card is graded either *right* or *wrong*.
2. **The ladder is `[1, 3, 7, 30]`, in days.** A card carries its position on it.
3. **A new card starts below the ladder** and is due on the day it was added, so a deck is
   reviewable as soon as it has a card in it. (This began as intake's assumption. It was put to
   the stakeholder as `WI-0002/Q-002` and they confirmed it: *"Today — A. If I've just added a
   card I want to try recalling it right away, not wait till tomorrow."* It is no longer an
   assumption, and `WI-0002` AC12 makes it checkable.)
4. **Right moves the card up one rung**, and its next review is that rung's number of days after
   the day it was reviewed.
5. **At the top rung, right keeps the card at 30 days.** The gap grows on every correct answer
   until 30 days and then holds. There is no fifth rung and no rule that grows the gap past a
   month. (This began as this ADR's reading of an answer that stopped at *"a month or so"*. It
   was put to the stakeholder as `WI-0003/Q-001`, against a doubling ladder and against a
   ceiling they would name, and they chose it: *"Stops at a month — option A."* It is no longer
   a reading, and WI-0003 AC1's closing clause — the gap "stays at 30 days on every correct
   answer after that" — is what they asked for.)
6. **Wrong sends the card back to the first rung**, so its next review is one day after the day
   it was reviewed — not later the same day.
7. **The next date is computed and stored at the moment the answer is recorded**, not at the
   start of the next session [src: WI-0003 AC4].

Worked by hand, a card answered right every time is due on day 0 (added), then +1, +4, +11, +41,
+71, +101 … A card answered wrong on any review is due the day after that review, whatever rung
it was on.

## Consequences

- WI-0003's criteria become concrete arithmetic a verifier can check with a calendar, which is
  exactly what AC3 asks for.
- WI-0003 AC1 had to be amended: "strictly longer each time" holds only up to the top rung. That
  amendment was made for version 1 of this ADR and AC1 now says so; `WI-0003/Q-001` confirmed the
  clause rather than changing it, so nothing further is owed here.
- WI-0002's grading is settled as a two-way choice, which was the open half of its notes.
- Stored state per card is small: a position on the ladder and a next-review date. No ease
  factor, so WI-0001's storage does not have to carry one.
- A card the person knows cold still returns monthly for ever. That is the cost of (i), and it
  was put to the stakeholder with its arithmetic — on a deck of 300 cards known cold, roughly ten
  cards a day for ever — before they chose it. They accepted it and said what would change their
  mind: *"If my deck gets huge later I might change my mind, but not now."* [src: WI-0003/Q-001].
  A deck that grows large is the signal to revisit this, and revisiting it is one constant.
- **Reversibility: high.** The rungs are a list; changing them, or extending the ladder, changes
  one constant and the dates of cards already scheduled. Moving to SM-2 later would be a bigger
  change — it needs per-card state the storage does not have — but nothing in this decision makes
  it harder than starting from nothing.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-30T03:38:18Z | answer-questions | WI-0003 | §5 is no longer this ADR's reading: the stakeholder chose the topping-out ladder in `WI-0003/Q-001` over a doubling one and over a named ceiling, and the consequence that a known card returns monthly for ever is now recorded as accepted rather than as a cost they may not want. The rule itself is unchanged |
| 2 | 2026-08-30T02:28:46Z | answer-questions | WI-0002 | §3 is no longer an assumption: the stakeholder confirmed in `WI-0002/Q-002` that a card added today is due today. The rule itself is unchanged |
| 1 | 2026-08-30T01:37:42Z | answer-questions | EP-001 | First version, recording the stakeholder's answer to `EP-001/Q-003` and the top-rung clause it left open |
