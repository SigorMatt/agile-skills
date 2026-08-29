---
title: Alignment is placed inside the cell's field, and mdtab may emit a bare table it will not recognise
version: 2
status: current
updated: 2026-08-28T22:54:00Z
updated-by: implement
updated-for: BUG-0001
---

# ADR-0007 — Alignment is placed inside the cell's field, and mdtab may emit a bare table it will not recognise

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for WI-0002, on the stakeholder's answers to
  [src: WI-0002/Q-001] and [src: WI-0002/Q-002]
- **Supersedes:** —

## Context

[src: ADR-0003] fixed which runs mdtab lays out and promised that inside one it "changes spaces
and nothing else". [src: WI-0001 AC12] then fixed the shape of a laid-out cell: a `|`, one guard
space, the content, the padding, one guard space, the next `|` — with the guard space against a
missing outer pipe dropped [src: WI-0001 AC14]. WI-0002 makes the padding follow the delimiter
row's markers, which means deciding *where inside that shape* the padding may move, and what to
do at the two places where a row has no pipe to align against.

The stakeholder answered both of the questions that were theirs. On how a centred cell divides an
odd spare column: *"put the spare space on the right so the text leans left"* [src: WI-0002/Q-001].
On the first column of a table written without a leading `|`, where right-alignment puts padding
at the start of the line: *"Honour the marker there too… a space at the front of the line is a
price I'll pay. Don't add the bars, and don't leave the table alone either"* [src: WI-0002/Q-002].
They also stated the general rule the item now rests on: *"Whatever the marker says, that's where
the text sits in the cell — every row, every column, no exceptions"* [src: WI-0002/Q-001].

That answer has a cost they were shown and accepted, and then refused to leave in place: a bare
table whose first column is right- or centre-aligned comes back with leading spaces on some lines
and none on its delimiter row, so the prefix rule [src: ADR-0003] no longer sees one run with one
prefix, and mdtab will not recognise its own output. *"That's a fault in the tool and I'd want it
sorted rather than worked around"* [src: WI-0002/Q-002] — which is [src: WI-0003], not this item.

## Options considered

- **A — Redistribute the padding inside the field, leave the guard spaces and the column widths
  alone, and accept the unrecognisable output.** The field is what [src: WI-0001 AC12] already
  leaves between the guard spaces; alignment changes the order of content and padding within it
  and nothing else. Cost: mdtab emits a bare right- or centre-aligned table it will not recognise
  on a later run, until [src: WI-0003] lands. Risk: low, and bounded — the property that fails is
  recognition, not correctness: the bytes are stable, so `format_document` is still idempotent
  [src: WI-0001 AC6].
- **B — Move the guard space instead of the padding**, so a right-aligned cell reads
  `|`, padding, content, space, space, `|`. Cost: none in code. Risk: it changes the column
  arithmetic that [src: WI-0001 AC12] fixes and that idempotence depends on, and the pipes of a
  right-aligned column would no longer land where a left-aligned one's do — breaking
  [src: WI-0001 AC2] for a table with mixed markers.
- **C — Widen a centred column by one when the remainder is odd**, so both sides always match.
  Cost: a column's width would depend on its alignment marker, which contradicts the
  one-place-per-rule statement about column width in `docs/architecture/overview.md` and
  interacts with the minimum-width rule [src: WI-0001/Q-005]. Risk: the stakeholder was offered
  this as option C of [src: WI-0002/Q-001] and did not take it.
- **D — Except the first column of a bare table from alignment**, which is what this plan's
  author recommended and the stakeholder rejected in terms [src: WI-0002/Q-002]. Cost: one
  exception to remember. Risk: it contradicts an explicit answer, so it is not available.

## Decision

**A.** Concretely, and checkably against `mdtab/table.py`:

1. A column's alignment is derived once per table from the delimiter row's cell for that column,
   stripped of spaces: a leading `:` alone is left, a trailing `:` alone is right, both are
   centre, neither is left [src: WI-0002 AC1]. It is computed beside the column widths, from the
   same parsed rows, and passed to the renderer — no second reading of the delimiter row
   anywhere [src: tracker/items/WI-0002/artifacts/plan.md].
2. A cell's **field** is `width - 2` display columns: what remains after the two guard spaces of
   [src: WI-0001 AC12]. Alignment places `text` within the field and distributes the remaining
   `padding = field - display_width(text)` columns around it — all after for left, all before for
   right, `floor(padding / 2)` before and `ceil(padding / 2)` after for centre
   [src: WI-0002 AC4].
3. The guard spaces are outside the field and do not move. Where the row's outer-pipe style drops
   one [src: WI-0001 AC14], only that space is missing; the field keeps its width, so the padding
   of a right-aligned first column in a bare table lands at the start of the line
   [src: WI-0002 AC10] and that of a right-aligned last column removes the trailing spaces the
   row would otherwise have carried [src: WI-0002 AC11].
4. `_column_widths` is not touched. A column's width does not depend on the *alignment* a
   marker declares [src: WI-0002 AC6] — which is what this decision needs, and all it needs, for
   the two rules idempotence forces to stay exactly where `docs/architecture/overview.md` says
   they are [src: WI-0001/Q-005]. The marker's colons are a different matter: they already
   reached the width before WI-0002, through the minimum width a delimiter cell must have, so a
   column too narrow to hold its own marker is wider with `:-:` than with `---`
   [src: WI-0001 AC12]. WI-0002 changes neither rule; it changes where the content sits inside
   the field those rules size [src: BUG-0001].
5. The delimiter row keeps being rendered by `_render_delimiter`, which fills the field with `-`
   and keeps the `:` it had [src: WI-0001 AC12]. Alignment never rewrites a marker
   [src: WI-0002 AC9].

## Consequences

What becomes easy: the layout has one new input — a list of alignments, one per column, computed
where the widths are — and every other rule stays where it was. A reader checking that mdtab
"changes spaces and nothing else" [src: ADR-0003] still finds one renderer and one width
function.

What becomes hard: mdtab's output is no longer always an input mdtab recognises. That is a real
loss of a property the tool had, it is invisible to a user because the tool emits no diagnostics
[src: EP-001], and it is why [src: WI-0003] exists. Until it lands, the affected documents are
exactly those with a bare table (no leading `|`) whose first column's marker is `---:` or
`:---:`, plus the same case inside a blockquote or indent prefix [src: WI-0002 AC12]. Every other
table is unaffected, and no document is corrupted: the second run reproduces the bytes
[src: WI-0001 AC6].

**Reversibility: high for the mechanism, low for the bytes.** The mechanism is one argument
threaded from `_column_widths`' neighbour into `_render_cell`, and reverting it is a small
edit in one file. What is not free is the output: documents already reformatted under this
decision would be reformatted again by the reversal, so anyone reversing it should expect a
one-off diff across every right- or centre-aligned table. Point 3 in particular is the one the
stakeholder decided rather than the architect, so reversing it needs them
[src: WI-0002/Q-002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T22:54:00Z | implement | BUG-0001 | Corrected a false clause inside `## Decision` item 4, in place and under the four conditions of [src: ADR-0009]. The removed sentence read, in full: *"A column's width does not depend on its marker [src: WI-0002 AC6], so the two rules idempotence forces stay exactly where `docs/architecture/overview.md` says they are [src: WI-0001/Q-005]."* It is false — a column too narrow to hold its own marker is wider with `:-:` than with `---`, which one command shows [src: BUG-0001] — and the criterion it cites says *alignment*, which is true and is what item 4 actually rests on. **The decision is unchanged:** `_column_widths` is still not touched, and no code conforming to version 1 needs to change. `status` stays `accepted` [src: ADR-0009] |
| 1 | 2026-08-28T20:30:00Z | plan | WI-0002 | First version, recording where alignment padding goes and the recognition property it costs |
