---
title: Record a review on the card as a next-due date and a last result, at store version 2
version: 1
status: current
updated: 2026-08-29T11:44:28Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0006 — Record a review on the card as a next-due date and a last result, at store version 2

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0002 is the first item that writes anything to a card after it has been added. Three of its
criteria force per-card stored state, and they force different parts of it:

- a review's result must survive the process, and the stored record of a card answered `y` must
  differ from that of a card answered `n` [src: WI-0002 AC2];
- a card reviewed today must not be presented again by a second run today [src: WI-0002 AC4];
- due cards are presented oldest-due-first, checked by setting due dates by hand in the store
  file [src: WI-0002 AC8].

What is already fixed:

- The store is one JSON object with a `version` integer and a `cards` array, written whole by
  rename, created by the first add [src: ADR-0004].
- The scheduling state per card is "which rung it is on, and the date it is next due", and
  due-ness is decided by date, not by clock time [src: ADR-0001].
- A newly added card is due the day it is added [src: ADR-0001].
- Computing *when* a reviewed card is next due is WI-0003's, not this item's; this item needs
  only "not again today" [src: WI-0002; src: WI-0003 AC2].
- A person opens this file and reads it, which is the point of the store rather than a side
  effect [src: WI-0001 AC5].

**Its relationship to ADR-0004, stated rather than left to be noticed.** ADR-0004 says
"`version` is an integer, `1` for the shape this item delivers. WI-0003 adds per-card scheduling
fields to each card object and bumps it" [src: ADR-0004]. This ADR has WI-0002 add the fields
and bump the version instead. That is not a contradiction of ADR-0004's decision and is not
recorded as a supersession: ADR-0004 decided that the `version` field is the seam through which
per-card scheduling state arrives, and this uses that seam exactly as designed. What ADR-0004
got wrong was a prediction about *which item* would reach the seam first, made before WI-0002
was refined to require persisted results of its own. A contradiction would be a different
schema, a different write protocol, or scheduling state carried somewhere other than the card —
and none of those is proposed here. Recorded this explicitly because a later reader finding
version 2 arriving from WI-0002 would otherwise have to reconstruct whether the seam had been
respected or bypassed.

## Options considered

On what a review stores:

- **A — a next-due date and the last result, both on the card.** `due` as a date, `result` as
  right or wrong. Cost: two fields where AC4 alone would need one. Risk: low — AC2 requires the
  result to be distinguishable in the file, and a due date alone cannot distinguish a right
  answer from a wrong one while both mean "not today".
- **B — a next-due date only.** Cost: under this item's placeholder rule both answers produce
  the same date, so right and wrong become indistinguishable in the store and AC2 fails
  [src: WI-0002 AC2]. WI-0003 would then have to reconstruct the result from the interval,
  which is exactly backwards — the interval is derived *from* the result. Risk: high.
- **C — a review log per card, an array of dated results.** Cost: an unbounded structure in a
  file a person reads by eye, for a tool whose epic excludes statistics and history
  [src: EP-001]. Risk: medium — it invites a feature nobody asked for, and the epic says the
  review session's own output is the only reporting.

On the version:

- **D — bump `version` to 2, and accept 1 and 2 on read.** Cost: a version check to write and a
  rule for what an older document means. Risk: low.
- **E — leave `version` at 1 and add the fields silently.** Cost: two documents both claiming
  version 1 with different shapes, which is the failure the field exists to prevent
  [src: ADR-0004]. Risk: high.

On what next-due value a *review* writes, given that WI-0003 owns the ladder:

- **F — the day after the review, for both answers.** Cost: it is knowingly wrong for a right
  answer until WI-0003 lands, and it is the same value the ladder gives a wrong answer
  [src: ADR-0001]. Risk: low, and it is the only value that satisfies AC4 without deciding
  anything WI-0003 owns.
- **G — the full ladder now.** Cost: it implements WI-0003 inside WI-0002, against that item's
  `## Out of scope`, and delivers behaviour no criterion of this item can check. Risk: high.

## Decision

Options A, D and F.

**Schema, version 2.** A card object carries `number`, `question`, `answer`, `due` and
`result`:

```json
{
  "version": 2,
  "cards": [
    { "number": 1, "question": "die Katze", "answer": "the cat", "due": "2026-08-29", "result": null },
    { "number": 2, "question": "der Hund", "answer": "the dog", "due": "2026-08-30", "result": "right" }
  ]
}
```

- `due` is a date as `YYYY-MM-DD`, in the machine's local date. A card is **due** when its `due`
  is today or earlier; due-ness is decided by date and never by clock time [src: ADR-0001].
- `result` is `"right"`, `"wrong"`, or `null` for a card that has never been reviewed. These are
  the two values AC2 requires the store to distinguish, and `README.md` names the field and both
  values [src: WI-0002 AC2].
- `recall add` sets `due` to today and `result` to `null`, which is ADR-0001's "a newly added
  card is due the day it is added", made durable rather than inferred [src: ADR-0001].
- Nothing else is added. In particular no rung, no review count and no history: the rung is
  WI-0003's [src: WI-0003 AC2] and history is excluded by the epic [src: EP-001].

**Versions on read and on write.** `save` always writes `version: 2`. `load` accepts a document
whose `version` is 1 or 2 and refuses any other value with the same message and exit code as any
other unreadable store [src: ADR-0004]. In a version-1 document a card has no `due` and no
`result`; both are then treated as their new-card values — the card is due, and it has no
recorded result — so a store written by WI-0001 keeps working and is upgraded in place by the
next write. Refusing a *higher* version is the same principle ADR-0004 states for a file that
does not parse: a store this tool does not understand is not overwritten, because overwriting is
indistinguishable from losing the user's cards [src: ADR-0004].

**What a review writes.** Recording a result sets `result` to `"right"` or `"wrong"` and `due`
to **the day after the review**, for both answers. This is a placeholder that WI-0003 replaces
with the ladder, and it is named as one here so that nobody later reads it as the schedule
[src: WI-0003 AC2; WI-0003 AC3]. It satisfies AC4 — the card is not due again today — and it
happens to be exactly what ADR-0001 already specifies for a wrong answer, so WI-0003 changes the
right-answer path and leaves the wrong-answer path alone [src: ADR-0001].

**When it is written.** After each card, not once at the end: the whole document is saved as
soon as a result is recorded. WI-0002 AC5 and AC9 both require that a session ended early keeps
what it already recorded, and per-card saving satisfies them for an interruption that is *not*
graceful as well — a kill, a closed terminal — which neither criterion tests but a user would
meet first. The cost is one whole-document rewrite per card, which is the cost ADR-0004 already
accepted for one person's vocabulary [src: ADR-0004].

## Consequences

What becomes easy: a person reading the file sees, per card, when it is next due and how it went
last time, which is what SM5 asks of the stored progress [src: EP-001]. WI-0003 has the two
inputs its ladder needs — a result and a date — and has to add only the rung. Verification of
this item's ordering criterion is a hand edit of `due` in the file [src: WI-0002 AC8].

What becomes hard: `due` is a local date with no timezone, so a store carried across timezones
can make a card due a day early or late. That is invisible to a single-user tool on one machine
[src: EP-001] and would become wrong the moment sync existed, which the epic excludes. And
because a review rewrites the whole document, a session over a large pile does one full rewrite
per card rather than one per session.

**Reversibility: high on the field names and the placeholder, medium on the version scheme.**
Renaming `due` or `result` is a change to the reader, the writer, `README.md` and any test that
names them [src: WI-0002 AC2]; no stored card would survive it without a migration, which is
what makes it medium
rather than total once cards exist. The placeholder next-due rule is one expression that WI-0003
is expected to replace, and replacing it is that item's whole job. Accepting versions 1 and 2 on
read is one condition; the day a version 3 exists, this rule is the thing that tells the user
their file is newer than their tool rather than silently rewriting it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:44:28Z | plan | WI-0002 | First version: the `due` and `result` fields, store version 2 and the read rule for version 1, the day-after placeholder for the next-due date, and saving after each card |
