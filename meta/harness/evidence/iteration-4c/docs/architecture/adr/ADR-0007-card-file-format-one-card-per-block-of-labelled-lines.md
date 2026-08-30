---
title: The card file format — one card per block of labelled lines
version: 1
status: current
updated: 2026-08-30T11:55:01Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0007 — The card file format: one card per block of labelled lines

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder chose a card file they can open and read, which the tool owns and rewrites:
*"B. I want to be able to open it and see my cards are still there, but I'm not asking to
hand-edit it — that's a different thing."* [src: WI-0001/Q-002] `ADR-0004` turned that into a
standing commitment — no part of a card or its schedule may be stored in a form that has to be
decoded to be seen — and left the exact format to `plan` under the standing delegation
[src: ADR-0004] [src: EP-001/Q-004].

The format has to carry four things per card: the two sides, and the two pieces of scheduling
state `ADR-0002` defines — where the card sits on the 1/3/7/30-day ladder, and the calendar date
it is next due [src: ADR-0002]. WI-0001's criteria then require two properties of it. AC2 asks
that a side read back out of the file is *byte-identical* to the argument that was given
[src: WI-0001 AC2]. AC3 asks that three added cards appear as three separate records, none
overwriting another, each with its own sides and its own scheduling state [src: WI-0001 AC3].

Byte-identical is the demanding one, because it rules out any format whose values need
unescaping to be read.

## Options considered

- **A — A JSON array, pretty-printed.** One object per card. Cost: none to write; the standard
  library parses and emits it. Risk: JSON escapes. A card whose front contains a quotation mark
  or a backslash appears in the file as `\"` or `\\`, so what the reader sees is not what they
  typed, and AC2's byte-identical reading fails on exactly the cards a language learner is most
  likely to enter [src: WI-0001 AC2]. An escaped field is also close to the thing `ADR-0004`
  forbids — a field that has to be decoded to be seen [src: ADR-0004].
- **B — Tab-separated values**, one card per line: front, back, rung, due. Cost: the smallest
  parser of the three, and the most compact file. Risk: a tab in either side breaks the record,
  so the format would have to refuse tabs as well as newlines, and a file of tab-aligned columns
  is markedly harder to read by eye than labelled lines when the two sides differ in length —
  which is the whole point of the promise being kept.
- **C — One card per block of labelled `field: value` lines**, blocks separated by a blank line.
  Cost: a hand-written parser of about a dozen lines, and a file roughly four times the height of
  option B's. Risk: a side containing a newline cannot be represented, so `add` has to refuse
  one; and the field labels are repeated on every card, which is wasted space at any scale but
  this one.

## Decision

**The card file is UTF-8 text with `\n` line endings, holding one card per block of four
labelled lines, in this fixed order:**

```
front: bonjour
back: hello
rung: 0
due: 2026-08-30
```

Blocks are separated by one blank line. The file begins with a short header of lines starting
`#`, saying what the file is and that the tool rewrites it; those lines are ignored on reading.

**A value is everything after the first `: ` on its line, to the end of the line, taken
verbatim.** No escaping, no quoting, no trimming — which is what makes AC2's byte-identical
reading true for any one-line side, including one with quotation marks, backslashes, tabs or
leading and trailing spaces [src: WI-0001 AC2].

**`rung` is an integer 0 to 4.** 0 means the card has never been answered. 1 to 4 are the rungs
of the ladder `ADR-0002` fixed, with intervals of 1, 3, 7 and 30 days [src: ADR-0002]. A card
added by `add` is written at `rung: 0` — it has not been answered, and `ADR-0002`'s first rung is
the one a card answered wrong returns to, which is a day away, so a never-answered card is not on
it [src: ADR-0002]. This ADR defines the field; it does not change the ladder or the grading rule,
which stay as `ADR-0002` decided them, and how a review session moves a card between rungs is
WI-0002's [src: WI-0002].

**`due` is a calendar date written `YYYY-MM-DD`**, in the machine's local calendar, which is the
comparison `ADR-0002` fixed [src: ADR-0002].

**A side may not contain a line break.** `add` refuses a front or back containing one, the same
way it refuses an empty side [src: WI-0001 AC7], because a record spanning lines is a record no
reader and no parser can see the boundaries of. Every acceptance criterion on this item describes
sides that are one line of text, so nothing that was asked for is refused by this
[src: WI-0001 AC1].

**Records keep the order they were added**, with a new card appended after the last one. Nothing
requires an order, and appending is the one that lets a person watch their own file grow.

## Consequences

Easy: `cat` shows a person their cards, their sides exactly as typed, and where each one has
reached — which is the promise they chose [src: WI-0001/Q-002]. Every one of WI-0001's file-reading
criteria becomes a `cat` and a look [src: WI-0001 AC2] [src: WI-0001 AC3] [src: WI-0001 AC5].
WI-0003's requirement to show the rung and the due date of a card before deleting it reads two
labelled lines rather than decoding anything [src: WI-0003].

Hard: the format is ours, so the parser is ours, and every field added later — an outcome
history, a deck name — is a change to it. A side with a line break in it cannot be stored, and if
that is ever wanted the format has to gain a quoting rule and this ADR has to be superseded.

Reversibility: **the parser is cheap to replace; the file is not.** Changing the format later
means converting a file holding real study history, and losing that history is one of the two
things the stakeholder named as making the product a failure [src: EP-001/Q-004]. That is why the
format is chosen against AC2's byte-identical reading now rather than after the first format has
accumulated cards.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:55:01Z | plan | WI-0001 | First version: one card per block of labelled lines, values verbatim to end of line, `rung` 0-4 against ADR-0002's ladder, `due` as a local calendar date, and line breaks refused in a side. |
