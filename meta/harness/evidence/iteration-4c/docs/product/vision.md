---
title: Product vision — a flashcard tool
version: 7
status: current
updated: 2026-08-30T13:31:49Z
updated-by: answer-questions
updated-for: EP-001
---

# Product vision — a flashcard tool

## Who it is for

One person studying something they want to keep in their head — a language, an exam syllabus,
terminology, anything that rewards repetition. They are willing to sit down once a day and be
asked questions. They are not willing to shuffle a box of index cards, and they are not looking
for a study platform, a course, or a social product.

The stakeholder described the product in a single sentence, quoted here as they wrote it:

> A flashcard tool: add cards, review due cards daily, simple spaced repetition. Progress
> persists.

[src: EP-001]

Asked how they would actually use it, they described themselves: *"it's just me, once a day at a
terminal, running through vocab."* [src: EP-001/Q-001]

## What it is for

Three things the person does, and one promise the tool makes.

- **Write a card down.** They capture a question and its answer at the moment they meet it, so
  the thing they want to remember leaves their head and enters the tool. A card is a front and a
  back, one line of text each. The tool never refuses a card for looking like one they already
  have — a word with two meanings is two cards with the same front — but it says so, because the
  same thing typed twice looks identical to it: *"add it and warn me."*
  [src: WI-0001] [src: EP-001/Q-004] [src: WI-0001/Q-001]
- **Do today's review.** Once a day they are shown the cards that are due *now* — not the whole
  pile — one at a time, and say whether they got each one right. Every due card is offered and
  none is withheld; the session says how many there are before the first one; and they can stop
  part-way without losing what they have answered. [src: WI-0002] [src: EP-001/Q-005]
  [src: docs/architecture/adr/ADR-0003-session-composition-no-cap-stated-count-clean-quit.md]
- **Throw a card away.** A card they no longer want can be deleted, named by its front side, and
  stops coming up. The tool shows them the card and what it had learned about it — how far up the
  ladder it had reached, when it was next due — and removes it only when they say yes. Deleting is
  permanent, which is their choice: they preferred one keystroke every time to a trash they could
  fish things out of. [src: WI-0003] [src: WI-0003/Q-001] [src: WI-0003/Q-002]
  [src: docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md]
- **And it is all still there tomorrow.** Cards, and where each one has reached in the schedule,
  survive quitting the tool and rebooting the machine. "Progress persists" is the stakeholder's
  own phrase and it is the promise everything else rests on. [src: EP-001] [src: EP-001/Q-004]

## The spacing rule

The rule is what makes the daily review worth doing: a card answered wrong comes back tomorrow, a
card answered right comes back later each time, so the person's time goes to the material they are
about to forget. The stakeholder chose it themselves, in these words:

> Just right or wrong — no difficulty scale. Get it right and it comes back later each time: a
> day, then three days, then a week, then a month. Get it wrong and it goes back to the start.

[src: EP-001/Q-002]

A card is due when its date is today or earlier, so a missed day costs nothing — the cards simply
stay due. [src: EP-001/Q-003] The full model, including the two things the stakeholder did not
state and the architect decided, is
`docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`. [src: docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md]

## How it is used

A command-line tool, run in a terminal on the person's own machine, with the cards and their
schedule in a file on that machine. The stakeholder chose the command line over a browser page
and a full-screen terminal application. [src: EP-001/Q-001]
[src: docs/architecture/adr/ADR-0001-command-line-delivery-surface.md]

That file is readable text, and the person can open it and see their cards and where each one has
reached in the schedule, with the tool not running. They asked for that themselves — *"I want to
be able to open it and see my cards are still there"* — and it is the one promise here that binds
every later version, because their real study history accumulates in whatever the first one
writes. [src: WI-0001/Q-002]
[src: docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md]

How it is built underneath — language, file format, packaging — the stakeholder left to us:
*"whatever you think is best."* [src: EP-001/Q-004] The one part of that they since narrowed is
the format, which may be anything a person can read. [src: WI-0001/Q-002]

## What would make it a failure

The stakeholder named two things, and they are worth more than any feature list:

> Two things would make this a failure for me: losing my progress, or a review taking more than a
> couple minutes to get through.

[src: EP-001/Q-004]

The first is the promise above. The second was in tension with something else they asked for — a
session showing every due card with no cap [src: EP-001/Q-003] — because on a backlog the two
cannot both hold. That was put back to them as `EP-001/Q-005` rather than settled for them, and
they settled it themselves:

> Don't cap it at some arbitrary number, but let me quit partway through without losing anything —
> whatever I already answered keeps its new schedule, and the rest is still due tomorrow. I'd
> rather see the honest number of cards waiting than have the tool quietly decide which ones I
> don't get to see today.

[src: EP-001/Q-005]

So the couple of minutes is a pressure on the design and not a promise the tool makes: after a
week away the session will be long, and it will say so up front instead of hiding cards. What the
tool owes them is the honest count, a supported way to stop, and nothing lost when they do.
[src: EP-001/Q-005]
[src: docs/architecture/adr/ADR-0003-session-composition-no-cap-stated-count-clean-quit.md]

## What it deliberately is not

These are recorded so a later reader can tell a deliberate exclusion from an oversight. Most of
them are intake's inference from what the stakeholder said rather than their words, and
`EP-001/Q-004` invited them to contradict any of it — which they did, on deleting a card.
[src: EP-001/Q-004]

- Not a multi-user product. One person, one collection of cards, one machine.
- Not a deck manager: no decks, tags or categories.
- Not a sync service: nothing moves between machines or devices.
- Not a card editor: a card can be added and deleted, but not amended. Deleting is the
  stakeholder's own request; editing is the part they said can wait. [src: EP-001/Q-004]
- Not undoable: no trash, no archive, nothing a deleted card can be recovered from. This was
  intake's exclusion until it was put to the stakeholder, and it is now theirs — they chose to be
  asked before each deletion instead. [src: WI-0003/Q-002]
- Not an importer: no Anki, CSV or Quizlet formats.
- Not a hand-editable file. The card file can be read but is the tool's to write, and the tool
  may rewrite or reformat it whenever it saves. The stakeholder drew that line themselves: *"I'm
  not asking to hand-edit it — that's a different thing."* [src: WI-0001/Q-002]
- Not a card browser: no command lists the cards or searches them. The stakeholder declined one
  when they were offered it: *"I don't need a numbered list for this."* [src: WI-0003/Q-001]
- Not a media product: card sides are one line of text.
- Not a reminder system: the person starts their review themselves.
- Not an analytics product: no streaks, graphs or study statistics.
- Not a graphical product: no browser page and no full-screen terminal interface.
  [src: EP-001/Q-001]

## How we will know it is working

The epic's success measures are the checkable form of this vision. They live in
`tracker/items/EP-001/item.md` rather than being restated here, so that the two cannot drift
apart. [src: EP-001]

## Open with the stakeholder

Nothing on the epic is open with them. Five questions were put to them there and all five are
answered, and this version is written from those answers: how they interact with the tool (`EP-001/Q-001`), what
the spacing rule does (`EP-001/Q-002`), what makes a card due on a given day (`EP-001/Q-003`), what
else mattered to them that nobody had asked (`EP-001/Q-004`), and which of two of their own
statements about session size wins (`EP-001/Q-005`).
[src: EP-001/Q-001] [src: EP-001/Q-002] [src: EP-001/Q-003] [src: EP-001/Q-004]
[src: EP-001/Q-005]

`refine` has since put two further questions to them on WI-0001, and both are answered: what
happens when the same front side is added twice (`WI-0001/Q-001`), and whether the card file has
to be legible (`WI-0001/Q-002`). This version is written from those two answers as well.
[src: WI-0001/Q-001] [src: WI-0001/Q-002]

`refine` has also put two questions to them on WI-0003, and both are answered and taken into this
version: how a card is named for deletion (`WI-0003/Q-001`) and what protects them from deleting
the wrong one (`WI-0003/Q-002`). [src: WI-0003/Q-001] [src: WI-0003/Q-002]

Nothing is still to be put to them. The three things this section listed as open — what the
person types to reveal a card's back, what they type to answer right or wrong, and in what order
due cards are offered — were settled by `refine` on WI-0002 and are now built and verified; so was
what the commands are called. None of them was re-asked, because they had already delegated the
category — *"whatever you think is best"* — and each is recorded as an assumption of ours rather
than as something they said. [src: WI-0002] [src: WI-0003] [src: EP-001/Q-004]
[src: tracker/items/WI-0002/artifacts/refinement-qa.md]

Since then one further question has been put to them and answered: `EP-001/Q-006`, the sign-off,
asked at the engagement's rest whether they accept what was built. They accepted it as complete —
*"This is what I asked for and it works. Nothing else comes to mind right now; if I want more later
I'll open something new."* — and named no follow-up work, so nothing in this document has been
reopened and no new item exists. Anything they want next begins as a new request rather than as
more of this engagement, which is their own description of what they will do.
[src: EP-001/Q-006]

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 7 | 2026-08-30T13:31:49Z | answer-questions | EP-001 | The stakeholder's answer to the sign-off `EP-001/Q-006` taken into the record: they accept the engagement as complete and name no follow-up work, so `## Open with the stakeholder` records the sign-off round and its answer. Nothing else changed — no statement of theirs was overtaken by this answer, so no sentence sourced to an earlier one was rewritten. |
| 6 | 2026-08-30T12:51:14Z | review-close | WI-0002 | D7 at WI-0002's close. `## Open with the stakeholder` still listed three things as "still to be put to them" — what the person types at each prompt and the order due cards come in — which `refine` had settled on WI-0002 under their standing delegation without asking them. Rewritten to say that nothing is open with them and that those three are ours, recorded as assumptions. No statement of theirs was changed. |
| 5 | 2026-08-30T11:43:03Z | answer-questions | WI-0003 | Written from the stakeholder's answers to `WI-0003/Q-001` and `WI-0003/Q-002`: a card is deleted by typing its front side, the tool shows it and asks first, and deletion is permanent by their choice rather than our inference. The no-browser exclusion is now sourced to them, and the absence of undo is recorded as theirs. |
| 4 | 2026-08-30T11:38:16Z | answer-questions | WI-0001 | Written from the stakeholder's answers to `WI-0001/Q-001` and `WI-0001/Q-002`: a duplicate front side is added with a warning rather than refused, and the card file is readable text that the tool owns and that they are not asking to hand-edit. Two exclusions added for what that second answer rules out. |
| 3 | 2026-08-30T11:24:23Z | answer-questions | EP-001 | Written from the stakeholder's answer to Q-005: a session offers every due card and withholds none, states how many before the first one, and can be stopped part-way without loss. The couple-of-minutes sentence is recorded as a design pressure rather than a promise, in their words. Nothing is now open with them. |
| 2 | 2026-08-30T11:15:14Z | answer-questions | EP-001 | Written from the stakeholder's answers to Q-001 to Q-004: the command-line surface, the spacing rule in their words, what a card is, deletion added as something they asked for, the two failure modes they named, and Q-005 recorded as the open conflict between two of their statements. |
| 1 | 2026-08-30T11:07:09Z | intake | EP-001 | First version: who the tool is for, the two things it does, the persistence promise, and the eight exclusions intake inferred. |
