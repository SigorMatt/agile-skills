---
title: A cell that contains a line break ignores its column's marker, and mdtab learns what a code span is
version: 1
status: current
updated: 2026-08-29T07:41:58Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0010 — A cell that contains a line break ignores its column's marker, and mdtab learns what a code span is

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** the stakeholder, answering [src: WI-0004/Q-001], [src: WI-0004/Q-002] and
  [src: WI-0004/Q-003] — which cells the rule reaches, that it reaches one cell rather than its
  column, and that a header cell is not excepted; the mechanics below derived from those answers
  by plan (architect), for WI-0004
- **Supersedes:** —

## Context

[src: ADR-0007] settled where a cell's padding goes: a column's alignment is read once per table
from the delimiter row, and the renderer distributes the spare space around the content —
all after it, all before it, or split. Every cell of a column has been treated identically ever
since, which is what [src: WI-0002] asked for: *"Whatever the marker says, that's where the text
sits in the cell — every row, every column, no exceptions"* [src: WI-0002/Q-001].

[src: WI-0004] is the one exception the stakeholder now wants, and it is the last thing standing
between this engagement and its ending [src: EP-001/Q-005]. A cell holding an HTML `br` tag is
read as two lines by anyone looking at the document, and centring or right-shifting it puts the
first line somewhere the second is not. They asked for such a cell to *"just sit top-left, plain,
whatever the column marker says"* [src: EP-001/Q-005], and then settled the three questions that
turned that sentence into criteria:

- **Which spellings count** — all of them, *"capitals, a slash, spaces, an attribute, doesn't
  matter"* — **except a tag written inside a code span**, which is *"someone showing the tag, not
  using it"* [src: WI-0004/Q-001]. That exception is the whole of the new machinery: mdtab looks
  for a code span nowhere today.
- **One cell, not the column.** *"Putting a break in one row must not go and shift rows I never
  touched"* [src: WI-0004/Q-002].
- **The header is a cell like any other.** *"I do not want a rule I have to remember an exception
  to"* [src: WI-0004/Q-003].

Two constraints from this project's own record bound the design. A column's width is still
measured from the cell's text exactly as typed, because the tool exists to line the `|` characters
up in a fixed-width font [src: tracker/items/WI-0004/artifacts/refinement-qa.md]; so this decision
moves padding and never measures it. And the alignment marker in the delimiter row is content, not
spacing, so it is never rewritten [src: WI-0004 AC2].

This does not contradict [src: ADR-0007] and does not correct it under [src: ADR-0009]. ADR-0007
item 1 says the *column's* alignment is derived once per table from the delimiter row, with no
second reading of that row anywhere; that stays exactly true. What changes is that a cell may
decline the value its column offers, on evidence from its own text — a question ADR-0007 never
asked, because until now no cell had any say.

## Options considered

- **A — Decide it per cell at render time, from the cell's own text, in a new module that owns
  what mdtab knows about the inside of a cell.** `mdtab/table.py` keeps deriving one alignment per
  column and gains one line where a row is rendered: a non-delimiter cell whose text contains a
  line break is rendered as `left` whatever its column says. The detection — the `br` tag and the
  code span it may hide in — lives in `mdtab/inline.py`, a module that exists because this is the
  first inline markdown grammar the tool understands. Cost: a new module, and a second place a
  reader must look to predict a cell's padding. Risk: low. Nothing measures anything new, the
  delimiter row cannot reach the branch, and the decision depends only on text the layout never
  alters, so idempotence is untouched [src: WI-0001 AC6].
- **B — The same override, with the detection inside `mdtab/table.py`.** Cost: none in code; the
  file already owns the other rule about the inside of a cell, where a boundary is
  [src: WI-0001 AC10]. Risk: it merges two different kinds of knowledge in one module —
  *where a cell ends*, which is table grammar and is used to decide whether a run is a table at
  all, and *what a cell's text says*, which is markdown's inline grammar and is used only when
  laying one out. `docs/architecture/overview.md` names each rule's single home, and a module that
  holds both makes the code-span rule reachable from the recognition path, where it has no
  business being.
- **C — Compute a per-cell alignment matrix beside the per-column one, in `column_alignments`'
  neighbourhood, and pass it to the renderer.** Cost: an extra structure the width of the table,
  built for a case most tables do not have. Risk: it puts the override on the same footing as the
  marker, which invites a later change to let a *column* be derived from its cells — the reading
  [src: WI-0004/Q-002] explicitly rejected.
- **D — Give the multi-line cell its own layout: split it and lay the row out over several
  lines.** Cost: large, and it changes content rather than spacing. Risk: excluded by
  [src: WI-0004] `## Out of scope` and by [src: EP-001] — mdtab changes spacing, not content.

## Decision

**A**, in three parts.

### 1. A cell that contains a line break is rendered as if its column were left-aligned

At render time, for a non-delimiter cell, the alignment used is `left` when the cell's text —
stripped of the spaces around it, which is the same text whose width is measured — contains a
line break, and the column's own alignment otherwise [src: WI-0004 AC1]. The override is per cell,
so the cells above and below it are untouched [src: WI-0004 AC3], and it applies to the header row
because the header row is rendered by the same function as every other non-delimiter row
[src: WI-0004 AC6]. The delimiter row is rendered by its own function and cannot reach this branch,
so a marker is never rewritten [src: WI-0004 AC2] — and in any case a delimiter cell holding
anything but dashes, colons and spaces stops the run being a table at all.

Nothing else moves: the column's width, the guard spaces, and where the padding sits inside the
field are all as [src: ADR-0007] left them. A left-aligned cell already puts all of its padding
after the content, so this decision reuses that placement rather than defining a new one.

### 2. A line break is an HTML `br` tag that is not inside a code span

`mdtab/inline.py` answers one question — does this text contain a line break — under these rules:

1. A `br` tag is `<`, then `br` in either case, then either `>` immediately, or one of space, tab
   or `/` and then any run of characters up to the next `>`. So `<br>`, `<BR>`, `<br/>`,
   `<br />` and `<br class="k">` are all line breaks and `<brx>` is not [src: WI-0004 AC1].
2. Code spans are found first and their contents, delimiters included, are excluded from the
   search. A run of *n* backticks opens a span, which is closed by the next run of exactly *n*
   backticks; the run between them is the span. A run with no matching closer is literal text and
   the scan continues after it, looking for the next opener. Backticks are counted as written: a
   backslash before one is an ordinary character, because the only escaping rule this project has
   is the one about `|` in `split_row` [src: WI-0001 AC10] and a second one is not needed to
   satisfy any criterion.
3. The question is asked of one cell's text at a time, and the answer depends on nothing else in
   the document.

### 3. The three cases WI-0004 left unconstrained, decided

`refine` recorded that [src: WI-0004/Q-001] settles what a code span *contains* but not what one
*is* at its edges, and left three cases to this decision [src: WI-0004] `## Notes`. Rule 2 decides
all three, and each is decided the way a markdown renderer would:

| case | outcome | why |
|------|---------|-----|
| `` a`<br>b `` — an unbalanced backtick | the cell sits **left** | the run never closes, so there is no span and the tag is in plain text — which is also what a renderer shows the author: a literal backtick and a broken line |
| ``` ``<br>`` ``` — a multi-backtick span, and a span holding a literal backtick | the cell **obeys its marker** | a run of two closes a run of two, and a shorter run inside it closes nothing, so the tag is inside the span and the author is showing it |
| `` a`<br>`b<br>c `` — a tag inside a span and another outside | the cell sits **left** | the second tag is in plain text, and [src: WI-0004 AC1] asks only whether the cell contains a tag outside a span |

## Consequences

**What becomes easy.** The stakeholder's rule holds without exceptions to remember: any cell that
reads as two lines sits plain at the left, header or body, under any marker
[src: WI-0004 AC1; src: WI-0004 AC6], and a cell that only *mentions* the tag is left alone
[src: WI-0004 AC7]. A reader predicting a cell's padding has two things to check — the column's
marker, and whether the cell's own text contains a break — and each has one home named in
`docs/architecture/overview.md` [src: docs/architecture/overview.md].

**What becomes hard.** mdtab now knows a little markdown inline grammar, and *"no markdown
parser"* is a sentence in the overview that has to become more careful rather than staying
absolute. The code-span rule is the first thing in this tool that could be wrong in a way an
author would call a bug rather than a limitation: a span mis-found makes an ordinary cell shift
left, or leaves a broken one where it was. It is also a rule markdown itself states more elaborately
than rule 2 does — CommonMark strips one leading and trailing space from a span's content, and lets
a backslash escape a backtick — and this project deliberately implements the smaller rule, because
none of the elaboration changes whether a `br` tag is inside a span or outside one.

A visible change for authors, which the stakeholder chose with the alternatives in front of them:
a cell that writes about `<br>` without backticks stops obeying its column's marker
[src: WI-0004/Q-001]. Nothing warns them, because the tool says nothing about anything
[src: EP-001].

**Reversibility: high, for both parts.** Part 1 is one condition at one call site in
`mdtab/table.py`; deleting it restores WI-0002's behaviour exactly, because the column's alignment
is still computed and still passed. Part 2 is a whole module with no other caller, and its rules
are tightened or loosened in one file — adopting CommonMark's fuller code-span rule later, for
instance, needs no change anywhere else. What is not free is the bytes: documents laid out under
this decision would be re-laid-out by a reversal, a one-off diff across every table holding a `br`
tag [src: ADR-0007]. Part 3's table is the cheapest thing here to revisit — each row is a
consequence of rule 2 rather than a separate switch, so a different answer means a different span
rule, not an exception list.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T07:41:58Z | plan | WI-0004 | First version, recording the per-cell override, the code-span rule the tool needed to learn, and the three edge cases WI-0004 left to it |
