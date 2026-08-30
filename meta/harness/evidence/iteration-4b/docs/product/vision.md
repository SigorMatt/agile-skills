---
title: Product vision
version: 6
status: current
updated: 2026-08-30T06:01:20Z
updated-by: answer-questions
updated-for: EP-001
---

# Product vision

## Who it is for

One person, learning something on their own, on their own machine. They already know what they
want to memorise; what they do not have is anything that remembers *when* they should see each
piece again. Today that means either reviewing everything every day, which stops being possible
past a few dozen cards, or reviewing whatever catches their eye, which spends the same effort on
what they know cold as on what they are about to lose.

That this is one person rather than a class, a team or a shared service began as an assumption
intake made. The stakeholder has since confirmed it in their own words: *"It's just me, learning
vocabulary, at a terminal, once a day — nothing fancier than that."* [src: EP-001/Q-001]

They also named the two ways this tool would fail them: *"don't lose my progress — that's the one
thing that would make this a failure, along with a review session that drags on more than a
couple minutes."* [src: EP-001/Q-001] Everything below is in service of those two sentences.

## What it is for

Holding a deck of question-and-answer cards, and deciding for its owner which of them to show
today. Three things have to be true for that to be worth anything:

- the deck outlives the session — cards added last week are there this week, kept in a file on
  the person's own machine that survives a reboot [src: EP-001/Q-001]. That file is at one fixed
  place, `~/.local/share/recall/deck.json`, and there is no flag, environment variable or
  configuration file for pointing the tool at a different one; asked directly at the engagement's
  ending whether that was what they wanted, they said it was — *"a fixed file under my home
  directory is exactly what I asked for"* [src: EP-001/Q-005; ADR-0004];
- a sitting shows the due cards and nothing else — **all** of them, with no cap on how many it
  presents [src: WI-0002/Q-001]. A couple of minutes remains what they want a sitting to feel
  like, and the tool does not enforce it: asked directly whether a sitting should stop after N
  cards, they chose not to cap it and reconciled the two themselves — *"If it's a big pile after
  a week away I'll just stop partway, that's fine by me."* [src: WI-0002/Q-001] Which is why an
  abandoned sitting must keep the answers already given;
- how the person did on a card changes when they see it next, in a direction they can predict:
  right pushes it further out, wrong brings it back — and the sitting says so, printing when each
  card is next due as they answer it, because a schedule nobody is told about is one they cannot
  tell from a broken one [src: WI-0003/Q-002; ADR-0007].

It is operated from a terminal: one command with subcommands, chosen by the stakeholder over a
browser page and a full-screen terminal application [src: EP-001/Q-002; ADR-0001]. A card is
graded right or wrong — no rating scale — and the gap to its next review walks the ladder 1, 3,
7, 30 days, resetting to one day when the person misses it [src: EP-001/Q-003; ADR-0002]. The
ladder stops at a month: a card known cold comes back monthly for ever rather than drifting out
of sight [src: WI-0003/Q-001; ADR-0002].

## What it deliberately is not

- Not a shared or multi-user system. No accounts, no login, no sharing a deck with anyone.
- Not synced. It does not reach the network, and a second machine is a second deck.
- Not compatible with other flashcard tools. Nothing is imported from or exported to them.
- Not a media tool. Cards are text.
- Not a statistics product. No streaks, no dashboards, no gamification beyond what one review
  sitting needs to show.
- Not a deck manager. One deck, and no **editing** a card once it is added. Deleting one is a
  different matter and the stakeholder asked for it: *"I want to be able to delete a card I don't
  need anymore; editing can wait."* [src: EP-001/Q-001] That work is `WI-0004`.

Each of those exclusions was derived at intake from what a reasonable reader would otherwise
assume was included, and each was recorded so it could be argued with rather than discovered
late. The stakeholder argued with exactly one of them, which is what the list was for.

## What is still open

Nothing. Every question this document ever listed as open has been put to the stakeholder and
answered, and on 2026-08-30 they accepted the engagement as complete: *"A — accept as complete.
This is what I asked for."* [src: EP-001/Q-004]. They were shown, before answering, the list of
things this version does not do — no editing a card, exact-match deletion only, no memory of past
sittings, fixed rungs, and no rule anywhere bounding a sitting's length — and named no follow-up
work. Anything further is a fresh engagement, not a loose end on this one.

The two decisions that shaped everything below them are recorded as `ADR-0001` (a command-line
interface) and `ADR-0002` (the interval ladder). The last item this section carried —

- **How a card is named when deleting it** (`WI-0004`) — was settled at that item's refinement:
  a card is named by typing its question side exactly, `recall delete --question "<text>"`, and a
  name matching two cards refuses and removes nothing. *"B — let me just type the question,
  that's the most natural way for me to say which card I mean."* [src: WI-0004/Q-001]. It was
  still listed here when WI-0004 shipped; that was this document lagging the record, not an open
  question.

Three others were settled earlier. The first two were open at version 2 and were closed by `WI-0002`'s
refinement; the third was closed by `WI-0003`'s:

- **How long a sitting may take.** Answered by not bounding it. A sitting presents every due
  card; the couple of minutes is a design target rather than a rule the tool applies, and that is
  their choice, not ours [src: WI-0002/Q-001].
- **Whether a newly added card is due the day it was added.** It is. Intake's assumption was put
  to them and confirmed [src: WI-0002/Q-002; ADR-0002], whose §3 now records it as settled.
- **What happens above the top rung of the ladder.** It stops there. They named four intervals
  and stopped at *"a month or so"*; `ADR-0002` read that as the ladder topping out and said so as
  a reading, and `WI-0003`'s refinement put all three shapes to them — stop, keep doubling, or
  grow to a ceiling they name. They chose to stop, having been shown what it costs a large deck:
  *"Stops at a month — option A. The whole point was simple, and I don't want to be doing math to
  figure out when a card's coming back."* [src: WI-0003/Q-001]. `ADR-0002` §5 now records it as
  theirs rather than as ours.

`WI-0003`'s refinement also settled a thing that had never been listed here as open, because
nobody had noticed it was: **whether a sitting tells you when you will next see a card.** It
does, one line per card as you answer it — the alternative being a schedule that runs invisibly
[src: WI-0003/Q-002; ADR-0007].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 6 | 2026-08-30T06:01:20Z | answer-questions | EP-001 | The stakeholder's answer to `EP-001/Q-005` propagated: the deck bullet under "What it is for" now says the file's location is fixed and unchangeable, and cites their confirmation of it. `Q-004`'s sign-off description had told them the opposite — that `RECALL_DECK` could relocate the deck — and no document ever said so; this records the true thing in the place a reader of the vision would look |
| 5 | 2026-08-30T05:51:35Z | answer-questions | EP-001 | The stakeholder's sign-off answer to `EP-001/Q-004` propagated: they accepted the engagement as complete with no follow-up work, so "What is still open" holds nothing. The one entry it still carried — how a card is named when deleting it — was recorded as having been settled at `WI-0004/Q-001`, which this document had lagged |
| 4 | 2026-08-30T03:38:18Z | answer-questions | WI-0003 | The stakeholder's answers to `WI-0003/Q-001` and `WI-0003/Q-002` propagated: the ladder stops at a month by their decision rather than by our reading, and a sitting prints each card's next-review date as it is answered. The top-rung entry moved out of "What is still open", which now holds one item |
| 3 | 2026-08-30T02:28:46Z | answer-questions | WI-0002 | The stakeholder's answers to `WI-0002/Q-001` and `WI-0002/Q-002` propagated: a sitting presents every due card with no cap, with their own reconciliation of that against the couple-of-minutes sentence recorded beside it, and a card added today is due today. Two entries moved out of "What is still open" |
| 2 | 2026-08-30T01:39:00Z | answer-questions | EP-001 | The stakeholder's answers to `Q-001`, `Q-002` and `Q-003` propagated: a command-line interface, right-or-wrong grading over a 1/3/7/30-day ladder, storage as a file that survives a reboot, and deleting a card moved from excluded to `WI-0004` |
| 1 | 2026-08-30T01:31:05Z | intake | EP-001 | First version, from the stakeholder's stated idea |
