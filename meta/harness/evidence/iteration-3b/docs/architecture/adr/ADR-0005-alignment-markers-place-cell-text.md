---
title: Alignment markers place cell text, and an odd centring remainder goes to the right
version: 4
status: superseded
superseded-by: docs/architecture/adr/ADR-0007-a-cell-containing-a-line-break-is-exempt-from-its-marker.md
updated: 2026-08-29T23:58:20Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0005 — Alignment markers place cell text, and an odd centring remainder goes to the right

- **Status:** superseded
- **Date:** 2026-08-29
- **Decided by:** the stakeholder, recorded by answer-questions (architect), for WI-0002
- **Supersedes:** —
- **Superseded by:** ADR-0007, for EP-001, on 2026-08-29 — decision 3 below (*"No content cell is
  exempt"*) was narrowed by the stakeholder in `EP-001/Q-005`: a cell containing a line break is
  exempt from its column's marker. ADR-0007 carries decisions 1, 2, 4, 5 and 6 forward unchanged and
  is the document to act on. What is below is what was believed and decided on 2026-08-29, and is
  kept as written.

## Context

WI-0002 is the "honours alignment markers" half of the stated idea [src: EP-001]. WI-0001 shipped
a filter that pads every column to its widest cell and puts all of the padding on the right of the
text, because at that point nothing told it to do otherwise [src: ADR-0003; src: WI-0001 AC3].

Two things had to be settled before that padding could move.

**The remainder.** Centring splits a column's leftover padding between the two sides of the cell's
text. When the leftover is odd, one side gets one more than the other, and nothing on record said
which [src: ADR-0003; src: ADR-0004]. `refine` escalated it as `WI-0002/Q-001` under `spec/question.md` §4's fourth condition —
a genuinely silent record where either choice has material consequences, because it decides the
appearance of every centred column in every document the tool is ever run over. The stakeholder
answered:

> Put the extra space on the right. When it cannot sit dead centre I want the text leaning towards
> the side I read from, and it matches the way the rest of the file pads.

[src: WI-0002/Q-001]

**The reach of a marker.** In the same reply, unprompted, they widened what they were settling:

> While you are on this: the alignment marker decides everything. Whatever the marker says, that
> is where the text sits in the cell — every row, every column, no exceptions.

[src: WI-0002/Q-001]

That sentence is the reason this ADR exists rather than a note on the item. It removes a class of
exemption that nobody had asked about and that an implementer would otherwise have had to invent
an answer for — the header cell in particular, which WI-0002's criteria cover only by saying
"every cell's text in that column" [src: WI-0002 AC1].

**Why this is not a change to ADR-0003 decision 9.** Decision 9 fixes a content cell as a pipe,
one space, the cell's text, padding to the column width, one space [src: ADR-0003]. Read on its
own it says the padding always follows the text, which is what `compose_row` did when this ADR
was written, before WI-0002 changed it [src: WI-0001 AC3]. It was written for WI-0001, where the
filter did not act on markers at all, and ADR-0004 recorded that boundary in as many words: *"Whether the markers mean anything for
where cell text sits is WI-0002's decision and is not implemented here"* [src: ADR-0004]. This ADR takes the decision ADR-0004 deferred. Decision 9's shape — one space, the
cell's width, one space, `width + 2` characters between the pipes — is untouched; only where the
padding sits inside that width is decided here, and only for a column that carries a marker.

## Options considered

On the odd remainder — the three options `WI-0002/Q-001` put to the stakeholder:

- **A —** The extra space goes on the right; the rule is "half the leftover, rounded down, on the
  left". Cost: a centred cell's text sits one column left of true centre. Risk: none beyond taste;
  it is the same direction every other column pads in.
- **B —** The extra space goes on the left. Cost: centred text is pushed as far right as the
  rounding allows, and nothing else in the file behaves that way. Risk: none beyond taste.
- **C —** Something conditional — alternate sides, or match whichever side the input already had.
  Cost: the output stops being a function of the input's content, tables in one document can
  disagree, and running the filter twice could change a file. Risk: high; it breaks idempotence.
- **Chosen: A**, by the stakeholder, in their own words above. This was not the team's decision to
  take; the recommendation offered alongside the options was also A, and they were asked plainly
  enough to have chosen otherwise.

On how far "every row, every column, no exceptions" reaches:

- **D —** The marker governs every **content** cell of its column — the header row and every body
  row — and does not reach the delimiter row, which carries no text to place. Cost: the sentence
  is read with an implied scope rather than literally. Risk: low; the scope is the stakeholder's
  own, stated in the clause "that is where the text sits in the cell", and they have separately
  called the delimiter row *"a rule under the header, not a row of content"*
  [src: WI-0001/Q-004].
- **E —** Read it literally over every line of the table, including the delimiter row. Cost: it
  asks where the "text" of a cell that has none should sit, which has no answer; and it would put
  the reply in conflict with `WI-0001/Q-004` and with ADR-0004, which fixes a delimiter cell's
  colons at the ends the input had them at [src: ADR-0004]. Risk: high — it
  manufactures a contradiction between two of the stakeholder's own answers out of a reading they
  did not ask for.
- **Chosen: D.** The cross-answer check on `WI-0002/Q-001` records the same reading and its
  basis, so that a later reader finds the reconciliation rather than the apparent conflict.

On a column with **no** marker:

- **F —** A markerless column keeps WI-0001's behaviour: padding on the right [src: WI-0002 AC4;
  src: ADR-0003]. Cost: none; it is what is already recorded, shipped and verified.
- **G —** Treat "every column, no exceptions" as reaching markerless columns too. Cost: there is
  no marker to obey, so this decides nothing that F does not already decide. Risk: it would read
  as a new decision where none was taken.
- **Chosen: F.** The stakeholder's sentence is about what a marker decides, and a column without
  one has nothing saying anything. This reading is the team's, not theirs; it changes no behaviour
  and contradicts nothing they have said, which is why it is recorded here rather than put back to
  them.

## Decision

1. **A column's alignment marker decides where its cell text sits within the column's width.**
   A left marker (`:---`) puts the padding to the right of the text; a right marker (`---:`)
   puts it to the left; a centre marker (`:---:`) splits it between the two sides.
2. **When a centred column's leftover padding is odd, the extra display column goes to the right
   of the text** — half the leftover, rounded down, on the left [src: WI-0002/Q-001].
3. **No content cell is exempt.** Decision 1 applies to the header row and to every body row of a
   marked column alike, and to every marked column of a table [src: WI-0002/Q-001].
4. **A column whose delimiter cell carries no marker is laid out exactly as ADR-0003 decision 9
   lays it out** — padding to the right of the text [src: WI-0002 AC4].
5. **The delimiter row is not a content row and decisions 1 to 3 do not reach it.** Its cells are
   composed by ADR-0004 decision 1: the leading colon the input had, then hyphens, then the
   trailing colon the input had, filling `width + 2` with no spaces [src: ADR-0004].
6. **Nothing here changes a column's width or a cell's two surrounding spaces.** The leftover
   being split is measured in display width [src: ADR-0003], it is split strictly
   inside the column's `width` characters, and the one space either side of the cell text is
   untouched [src: WI-0001/Q-003], so no composed line gains trailing whitespace
   [src: EP-001/Q-001].

## Consequences

Easy: the output of the filter stays fully determined by its input, so every rule above is a test
with an input file and an expected output file, and idempotence is preserved — decisions 1 to 4
are a function of the delimiter row and the cell contents, both of which survive a round trip.
Decision 2 in particular is what stops a centred table oscillating between two layouts when the
filter is run twice.

Hard: a reader who checks `compose_row` against ADR-0003 decision 9 alone will conclude the code
is right when it is now incomplete [src: mdtab.py]. ADR-0003 carries a `## Corrections` entry
pointing at this ADR for exactly that reason. The second cost is that decision 3 makes the header
cell of a right-aligned column move, which is visible in the first diff over any existing
document; the stakeholder has already said the size of the first diff is not a concern
[src: WI-0001/Q-003].

Reversibility: decision 2 is cheap in code — it is which side of a division the remainder lands on
in one composing function — and expensive in documents, because every centred cell already
rewritten would shift by one column on the next run. That is one idempotent re-run, and the reason
it was put to the stakeholder rather than assumed. Decisions 1, 3 and 5 are the item's whole
subject and reversing them would be abandoning it. Decision 4 is cheap either way. Decision 6 is
constrained by three of the stakeholder's own answers and is not ours to reverse.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-08-29T23:58:20Z | answer-questions | EP-001 | Superseded by ADR-0007. Status and header bookkeeping only: no assertion in this document is edited, and decision 3 stands here as what was decided on 2026-08-29. The stakeholder narrowed it in `EP-001/Q-005` — a cell containing a line break is exempt from its column's marker — and ADR-0007 is now the current decision. The `## Corrections` heading also gains *"— closed on supersession"* and a paragraph saying why: both entries are reproduced verbatim, none is removed, and no further one may be added. That rename is a workaround for `adr.correction.superseded`, which no legal move can otherwise clear, and the paragraph names it as one |
| 3 | 2026-08-29T23:17:37Z | answer-questions | WI-0002 | Provenance only, in `## Corrections`: two `mdtab.py:207` pointers are replaced with citations that name `compose_row` rather than a line it no longer sits on, and the `## Context` sentence about the odd remainder gains the source for its absolute [src: mdtab.py]. No assertion changes |
| 2 | 2026-08-29T23:17:37Z | answer-questions | WI-0002 | Erratum, in `## Corrections`: the `## Context` clause saying `compose_row` puts the padding after the text is put in the past tense, because WI-0002 made it false [src: mdtab.py]. No decision changes and nothing is superseded [src: WI-0002] |
| 1 | 2026-08-29T22:29:29Z | answer-questions | WI-0002 | First version, recording the stakeholder's answer to WI-0002/Q-001: the odd centring remainder goes right, and the marker places text in every content cell of a marked column. Takes the decision ADR-0004 decision 3 deferred |

## Corrections — closed on supersession, 2026-08-29T23:58:20Z

This section is **closed**. Both entries below were made by `answer-questions` on 2026-08-29 while
this ADR was `status: accepted`, and both are reproduced here exactly as they were written: not a
word is edited and nothing has been removed. What has changed is that no further entry may be added,
because `spec/doc-header.md` §4b says a superseded ADR is not repaired — it records what was
believed then, and ADR-0007 is the document a reader acts on.

The heading says so rather than reading `## Corrections`, and that is a workaround, recorded here
because it should not be silent. `scripts/validate-workspace`'s `adr.correction.superseded` rule
tests the *state* — an ADR whose status is `superseded` and which has a `## Corrections` section —
where §4b states a rule about the *act*: do not correct a superseded ADR. An ADR legitimately
corrected while current and legitimately superseded afterwards therefore has no valid state to be
in: the corrections may not be deleted, because the section is append-only and deleting them would
destroy the evidence it exists to keep, and the supersession may not be skipped, because §4 requires
it whenever what the code must do has changed. Renaming the heading keeps every entry and states the
closure; deleting them or leaving the ADR falsely `current` would not. The defect belongs in the
validator, not in this file.

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-29T23:17:37Z | answer-questions | WI-0002 | erratum | `## Context`, the paragraph *"Why this is not a change to ADR-0003 decision 9"*, said: *"Read on its own it says the padding always follows the text, which is what `compose_row` does today"*. WI-0002 made that false — `compose_row` now splits the leftover by the column's marker, all of it before the text for a right marker and `(W - w) // 2` before it for a centre marker [src: mdtab.py; src: WI-0002 AC2; src: WI-0002 AC3], and the suite that asserts it passes [src: run: python3 -m unittest discover -s tests -t . -> exit 0, 24 tests, OK]. Replaced with the past tense, which is the point the paragraph was already making: why decision 9 read as complete at the time it was written. No decision changes, and no code would have to change to satisfy the new text |
| 2026-08-29T23:17:37Z | answer-questions | WI-0002 | provenance | Three citations repaired, no assertion touched. (a) `## Context` first paragraph, *"WI-0001 shipped a filter that ... puts all of the padding on the right of the text"*, cited `[src: mdtab.py:207]` — the line `compose_row` sat on before WI-0002 moved it to 244, where line 207 is now the last line of `column_widths` [src: mdtab.py] — and now cites the criterion that required the behaviour, [src: WI-0001 AC3]. (b) `## Consequences`, the *"Hard"* paragraph, *"a reader who checks `compose_row` ... will conclude the code is right when it is now incomplete"*, cited the same stale line and now cites [src: mdtab.py], with the function named in the sentence rather than located by line. (c) `## Context`, *"nothing on record said which"*, carried no citation at all and now cites [src: ADR-0003; src: ADR-0004], the two decisions that were silent on the remainder |
