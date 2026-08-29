---
id: EP-001
type: epic
title: A flashcard tool with daily spaced-repetition review and persistent progress
status: done
priority: high
created: "2026-08-29T10:44:45Z"
updated: "2026-08-29T14:20:24Z"
outcome: delivered
---

## Goal

Someone who is trying to memorise things — vocabulary, definitions, facts — can write each one
down as a card, and then, once a day, be shown only the cards that are due rather than the whole
pile. What they got right stops coming back so often; what they got wrong comes back sooner. The
tool remembers all of this between sessions, so the effort they put in yesterday still counts
today.

## Why now

Stated by the stakeholder as the opening idea for this project: *"A flashcard tool: add cards,
review due cards daily, simple spaced repetition. Progress persists."* Without scheduling, a
learner reviews everything every day, which stops being possible somewhere around a hundred
cards, so they either stop reviewing or review the wrong things. Without persistence, every
session starts from zero and no interval can ever stretch — the whole point of spaced repetition
is that it accumulates. The cost of not building it is that the cards exist but the schedule
does not, which is the same as not having a flashcard tool.

## Success measures

Each of these is checkable by a person with a terminal and no context, on a fresh installation.

- SM1 — a card added in one run of the tool is present in the next run of the tool, without any
  export or import step.
- SM2 — a newly added card appears in the due list on the day it was added.
- SM3 — a card answered correctly during a review is not offered again in a second review run on
  the same day.
- SM4 — a card answered correctly twice in a row has a strictly later next-due date than the
  same card after one correct answer, and a card answered incorrectly is next due at the shortest
  interval in the ladder — the day after the review — rather than at the interval it had
  reached.
- SM5 — the stored progress is a file (or files) on disk whose contents a person can open and
  read to confirm SM1–SM4 without running the tool.

## Scope

- Everything below is operated as a command-line tool run in a terminal, and every card lives in
  one flat pool (`Q-001`, `Q-004`).
- Capturing a card: its question side, its answer side, and the scheduling state that belongs to
  it.
- Persisting cards and their scheduling state across runs of the tool.
- Selecting the cards that are due and presenting them one at a time for review.
- Recording the result of each review and computing when that card is next due.
- Removing a card the user added by mistake. Added after the fact: the stakeholder accepted the
  engagement and named this as the one follow-up they wanted (`Q-005`), which is exactly the
  case `## Out of scope` had reserved. It is `WI-0004`, and it is delivered.

**This scope is now final.** Shown the whole tool at the second sign-off, the stakeholder accepted
it as complete and asked for nothing further: *"Add, review, the schedule, and now delete — that's
the whole thing I asked for, and the transcript shows it working. I don't have anything else I
want built right now, so close it out."* (`Q-006`). Nothing may be added to this epic; anything
wanted later is a new request.

## Out of scope

Written even though the stakeholder named no exclusions, because a reader would otherwise assume
these are included:

- Any form of sync, sharing, accounts, or multi-user support. This is one person's cards on one
  machine.
- Media on cards: images, audio, LaTeX, formatting. Card sides are plain text.
- Importing from or exporting to other flashcard tools (Anki, Mnemosyne, CSV).
- Statistics, streaks, retention graphs, or any reporting beyond what the review session itself
  shows. Declined again by the stakeholder when they were offered it by name: *"I don't need a
  schedule-view command or any stats, I never asked for those"* (`Q-005`), and left out a third
  time when it was put to them once more at the final sign-off (`Q-006`).
- A command to see or change a card's schedule. Hand-editing the store remains the way to move a
  card. Declined by the stakeholder in the same answer (`Q-005`), and again at the final sign-off
  (`Q-006`).
- Refusing a hand-edited store that carries the JSON number `1.0` where `1` is expected. The tool
  reads it rather than refusing it; no card is dropped and no schedule differs. Disclosed at
  sign-off and explicitly waved off — *"that `1.0` thing in the store file doesn't bother me"*
  (`Q-005`). No item covers it, deliberately.
- Tuning the scheduling algorithm per card or per user, and any second algorithm to switch
  between. The one scheme is the 1/3/7/30-day ladder recorded in `ADR-0001`.
- Organising cards into decks, tags or categories, and reviewing one grouping separately from
  another. Confirmed by the stakeholder's answer to `Q-004`.
- Any interface other than the command line: no web page, no server, no graphical interface.
  Confirmed by the stakeholder's answer to `Q-001`.
- Editing a card after it is added. The stakeholder was asked directly at sign-off and said
  *"editing can wait"* (`Q-005`), so it stays out; offered it once more at the final sign-off they
  again took nothing (`Q-006`). **Deleting** a card no longer does: they asked for it in the same
  answer, it went in scope as `WI-0004`, and it is built.
- Reminders, notifications, or anything that runs when the user did not start it.
