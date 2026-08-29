---
title: A cell's width is its display width in terminal columns, not its character count
version: 1
status: current
updated: 2026-08-28T18:30:21Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0002 — A cell's width is its display width in terminal columns, not its character count

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** the stakeholder, answering `EP-001/Q-003`; the measurement rule below decided
  by answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

"Pads columns" needs a definition of how wide a cell's text is, and for text that is not plain
ASCII there is more than one honest answer: a CJK character is one code point and draws two
columns, an accented letter may be one code point or two depending on how the file was saved,
and an emoji may be several code points that draw as one glyph. `intake` escalated the choice
rather than guessing it [src: EP-001/Q-003].

The stakeholder answered: *"It has to line up on the screen. My tables have accented names and
the odd emoji in them, and if the columns go ragged the moment one appears then the tool hasn't
done its job. Measure what the character actually takes up in my editor, not how many of them
there are."* [src: EP-001/Q-003]

That settles the *property* — alignment is judged on screen — but not the rule that computes it,
and the rule has to be written down because it is threaded through every layout decision and
every test in the tool. Deciding the rule is the architect's job; the stakeholder delegated the
build [src: EP-001/Q-001].

The rule also has to be buildable under [src: ADR-0001], which permits only the Python standard
library. It is: `unicodedata` exposes both the East Asian Width property and the general
category, which is everything the rule below needs
[src: run: python3 -c "print(__import__('unicodedata').east_asian_width('表'))" → W].

## Options considered

- **A — Count Unicode code points.** Cost: negligible — it is `len(s)`. Risk: contradicts the
  stakeholder's answer. A table containing CJK text or emoji draws visibly ragged in an editor
  because a two-column glyph was counted as one.
- **B — Measure display width from the East Asian Width property, with combining marks, joiners
  and variation selectors counted as zero.** Cost: a width function and its tests, and a small
  table-driven rule that has to be understood by anyone touching layout. Risk: it is never
  exact [src: EP-001/Q-003]. Terminals and editor fonts disagree about ambiguous-width
  characters and about emoji sequences, so a residue of misalignment survives in any
  implementation.
- **C — Declare non-ASCII table content out of scope.** Cost: nothing. Risk: contradicts the
  stakeholder's answer, which named accented names and emoji as content they actually have.

## Decision

Every width in the tool — column widths, padding counts, alignment offsets — is a **display
width in terminal columns**, computed by summing a per-character width over the cell's text:

1. width **0** if the character's general category is `Mn`, `Me` or `Cf` — combining marks,
   enclosing marks, and format characters including the zero-width joiner `U+200D` and the
   variation selectors;
2. otherwise width **2** if its East Asian Width property is `W` (wide) or `F` (fullwidth);
3. otherwise width **1**, including the `A` (ambiguous) class.

Rule 1 is stated by general category rather than by `unicodedata.combining()`, because the
variation selector `U+FE0F` — which is what makes many emoji render wide — has a combining class
of zero and would otherwise be counted as a visible column
[src: run: python3 -c "print(__import__('unicodedata').category('\ufe0f'))" → Mn].

The tool does **not** normalise cell text. It has no need to: under rules 1–3 a precomposed
`é` and a decomposed `e` + `U+0301` both measure 1, so the measurement is already
normalisation-independent, and rewriting the author's bytes would breach the epic's
"changes spacing, not content" scope [src: EP-001].

Ambiguous-width characters count as one column. This is the right default for a stakeholder
working in a Western locale, and it is the behaviour of every terminal not explicitly configured
for East Asian ambiguous-wide rendering.

## Consequences

What becomes easy: a table containing accented names, CJK text or common emoji lays out with its
pipes in a straight vertical line in a fixed-width font, which is the outcome the epic's success
measures describe [src: EP-001]. Because the width function is one function, every layout
decision inherits the rule for free, and a future change to the rule is a change in one place.

What becomes hard: character count and display width part company, so nothing in the tool may
use `len()` on cell text to mean a width, and tests must contain non-ASCII cases or they will
not detect a regression to code-point counting. Acceptance criteria phrased in characters have to
be phrased in display columns instead — which is why AC2 of WI-0001 was reworded when this was
recorded [src: WI-0001 AC2].

What this does not promise: exactness for every glyph. Emoji formed from joined sequences, and
ambiguous-width characters in a terminal configured to draw them wide, will still be measured
differently from how some fonts draw them. This is a known limitation of any display-width rule,
it was stated to the stakeholder when the question was asked [src: EP-001/Q-003], and it should
be recorded in the tool's own documentation rather than discovered as a bug.

**Reversibility: low.** The rule is consumed by every layout decision and asserted by the tests
that check alignment, so replacing it means revisiting all of them. Widening it — adding a data
table for specific emoji sequences, or making the ambiguous class configurable — is an additive
change and is cheap. Narrowing it back to code-point counting would contradict an explicit
stakeholder answer and needs their authorisation.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T18:30:21Z | answer-questions | EP-001 | First version, recording the stakeholder's answer to Q-003 and the measurement rule derived from it |
