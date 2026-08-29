---
title: Schedule with a fixed interval ladder of 1, 3, 7 and 30 days
version: 3
status: current
updated: 2026-08-29T12:33:35Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0001 — Schedule with a fixed interval ladder of 1, 3, 7 and 30 days

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

The stakeholder's opening statement said "simple spaced repetition" and nothing more, so
`intake` filed two questions rather than guess: which scheme "simple" means
[src: EP-001/Q-002], and what the reviewer records at each card [src: EP-001/Q-003]. Both are
now answered by the stakeholder.

To `Q-002` they replied: *"A card I get right comes back later each time — one day, then three,
then a week, then a month. Get it wrong and it goes back to the start."* To `Q-003`: *"Just
right or wrong. I don't want to sit there grading myself on a four-point scale for every card."*
[src: EP-001/Q-002; EP-001/Q-003]

That settles the family — a fixed ladder driven by a binary result, option A in both questions —
but it leaves one thing for the architect to determine. The ladder `Q-002` offered as option A
had five rungs, 1 / 3 / 7 / 14 / 30 days; the stakeholder's own enumeration names four, 1 / 3 /
7 / 30, omitting 14. Somebody has to decide which of those two sequences the tool implements,
and `WI-0003` AC4 requires the sequence to be written down somewhere a reader can work a due
date out from [src: WI-0003 AC4].

**Version 2 — where a brand-new card stands, added 2026-08-29.** Version 1 fixed the four
intervals and the two moves, and left one thing unstated that nobody noticed until `WI-0003` was
refined: which rung a card sits on *before it has ever been answered*. That decides what the
first right answer on a new card produces, which is the most frequent single event in the tool's
life. `WI-0003/Q-001` put it to the stakeholder rather than guessing, because their sentence is
honestly readable both ways — as the four places a card can rest, or as the sequence of waits
they actually experience. They replied: *"B — tomorrow. When I said one day, then three, then a
week, then a month, that's the order I meant to actually see, starting from a new card."*
[src: WI-0003/Q-001] The Decision records that as the never-answered state; nothing in
version 1 is reversed by it.

A second thing needed settling with it. The epic's success measure SM4 said a card answered
incorrectly is next due "no later than the day of the review", while `WI-0002` AC4 says a card
reviewed in one run is not presented again by a second review run on the same day
[src: WI-0002 AC4]. Under a same-day due date those two cannot both hold.

## Options considered

- **A — the stakeholder's four rungs: 1, 3, 7, 30.** Cost: a card that has been right three
  times jumps from a week to a month in one step, which is the largest ratio in the ladder.
  Risk: low, and it is what the stakeholder actually wrote.
- **B — the recommended five rungs: 1, 3, 7, 14, 30.** Cost: adds a rung the stakeholder did not
  name to the sequence they did name. Risk: the record would then say the stakeholder chose a
  ladder they never stated, which is the kind of small unearned addition this pipeline exists to
  prevent.
- **C — treat the enumeration as illustrative and ask again.** Cost: a whole round trip to the
  stakeholder for a constant that is one line of code to change. Risk: none, but it spends the
  scarcest thing in the loop on the cheapest decision in the epic.

## Decision

The ladder is **1, 3, 7, 30 days**, exactly the four rungs the stakeholder enumerated (option A).

- A newly added card is due the day it is added.
- A card that has **never been answered sits below the bottom rung**, not on it. The first
  correct answer therefore puts it on the 1-day rung and it is next due **the day after that
  review**; successive correct answers then give 1 day, 3 days, 7 days, 30 days — exactly the
  sequence the stakeholder enumerated, experienced in that order from a new card
  [src: WI-0003/Q-001]. A card reaches the top rung after four correct answers, not three.
  The accepted cost: on a brand-new card's first review a right answer and a wrong answer both
  bring it back the next day and both leave it on the bottom rung, so only the recorded `result`
  distinguishes them until the review after that [src: ADR-0006].
- A card answered **correctly** moves up one rung: a card at 1 day becomes due in 3 days, at 3
  days becomes due in 7, at 7 becomes due in 30. A card already at the top rung stays at 30 days.
- A card answered **incorrectly** returns to the bottom rung, so it is next due **one day after
  the review** — "back to the start" being the start of this ladder, not a same-day repeat.
- The result recorded per card is binary, right or wrong. No ease factor, no grade, and no
  per-card variation.
- Due-ness is decided by date, not by clock time [src: WI-0003].

The wrong-answer rule resolves the SM4 / `WI-0002` AC4 conflict in favour of the next day, which
is the only reading under which both hold; SM4 has been amended to say so
[src: WI-0002 AC4; EP-001].

## Consequences

What becomes easy: a reader with the stored state for a card and this document can work out its
next due date by hand, which is what `WI-0003` AC4 asks for. Verification of `WI-0003` needs
no clock arithmetic beyond adding one of four integers to a date [src: WI-0003 AC4]. The stored scheduling state
per card is small — which rung it is on, and the date it is next due.

What becomes hard: the schedule cannot respond to how hard a particular card is for this user.
A card they always get instantly and a card they barely scrape through advance identically, and
there is nothing in the stored state that would let a later algorithm tell them apart
retrospectively.

**Reversibility: medium, within this scheme; medium, out of it.** *(Amended at version 3; the
first sentence below used to say "high", on the strength of a claim about stored cards that is no
longer true.)* Adding a rung is still a change to one constant plus the documentation this ADR
anchors. Changing or removing an existing rung's value is not: `WI-0003` stores a card's rung as
the interval in days rather than as an index, and `load` refuses an interval the ladder does not
contain, so cards holding the old value make the store unreadable and have to be rewritten
[src: ADR-0007; src: WI-0003 AC9]. Version 1 of this ADR asserted the opposite — "existing cards
keep working because a rung index remains a rung index" — which was a prediction about a
representation nobody had chosen yet, and `ADR-0007` chose the other one for the reader's sake. Replacing the ladder with SM-2 or another
ease-factor scheme is the medium case: it needs an ease factor per card that no existing card
carries, a finer grade than right/wrong at review time (reversing `Q-003` [src: EP-001/Q-003] as
well as this ADR),
and a migration for cards already stored. That direction would supersede this ADR rather than
edit it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-29T12:33:35Z | plan | WI-0003 | Reversibility corrected from high to medium within the scheme: ADR-0007 stores a card's rung as the interval in days, not an index, so changing an existing rung's value now needs stored cards rewritten. The decision itself is unchanged |
| 2 | 2026-08-29T12:26:01Z | answer-questions | WI-0003 | The never-answered state: a card that has never been answered sits below the bottom rung, so a new card's first right answer schedules it one day out, from the stakeholder's answer to WI-0003/Q-001. Nothing in version 1 reversed |
| 1 | 2026-08-29T10:51:45Z | answer-questions | EP-001 | First version: the ladder from the stakeholder's answers to Q-002 and Q-003, and the wrong-answer reset that resolves SM4 against WI-0002 AC4 |
