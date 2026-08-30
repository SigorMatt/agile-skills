---
title: The break-tag exemption is applied per cell at composition, not by rewriting a column's alignment
version: 1
status: current
updated: 2026-08-30T00:23:48Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0009 — The break-tag exemption is applied per cell at composition, not by rewriting a column's alignment

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

ADR-0008 fixed the rule: a content cell whose text contains a break tag is laid out left whatever
its column's marker says, it is still padded out to the column's width, and every other cell of
that column is still placed by the marker [src: ADR-0008]. The rule is settled. Where in the code
it is applied is not, and the choice decides whether the "per cell, not per column" half of it
survives contact with an implementation.

The filter computes a column's alignment once per table, from the delimiter row, in
`column_alignments` [src: mdtab.py:220], and `emit_block` passes that one list to `compose_row`
for every content row of the block [src: mdtab.py:287]. `compose_row` then decides, per cell, how
much of the leftover padding goes before the text [src: mdtab.py:244]. Three places could carry
the exemption and they are not equivalent: one of them cannot express a per-cell rule at all, and
it is the one a reader skimming `column_alignments` would reach for first.

This ADR does not decide the rule and does not reconcile anything the stakeholder said. It records
which of three implementation sites the plan tells the developer to use, and why the cheapest-looking
one is wrong.

## Options considered

- **A — Test the cell's text inside `compose_row`, as the first branch of the existing
  before-padding chain.** The alignment list is untouched, and `emit_block` is untouched. Cost:
  `compose_row` gains one predicate call per cell and one branch; the rule then lives in the same
  function as the three marker rules it is an exception to, which is where a reader looking for
  "where does this cell's text sit" already goes [src: mdtab.py:244]. Risk: low — the change is
  additive and cannot alter a cell containing no break tag, because the new branch is the only new
  path and its condition is false for such a cell.
- **B — Build a per-cell alignment matrix in `emit_block` and pass a row's own list to
  `compose_row`.** Cost: `emit_block` gains a nested loop over every cell of every row, and
  `compose_row`'s parameter changes meaning from "the column's alignments" to "this row's
  alignments" — a signature whose type is unchanged while its meaning is not, which is the kind of
  change a later reader mis-reads. Risk: moderate, and it buys nothing: the exemption depends only
  on the cell being composed, so no caller needs to know about it before composition begins.
- **C — Set a column's alignment to `None` when any of its cells contains a break tag.** Cost:
  one line in `column_alignments`. Risk: **it is wrong**, and it fails silently. It makes the
  exemption per column, so a single `<br>` in one row would un-align every other cell of that
  column — which contradicts ADR-0008 decision 6 and the stakeholder's own *"markers govern
  everything else"* [src: EP-001/Q-005]. It is named here because it is the smallest diff of the
  three and would pass a test suite that only ever put one exempt cell in a single-column table.
- **Chosen: A.** It is the only option that puts the exception in the same function as the rule it
  excepts, it cannot express the per-column mistake, and WI-0003 AC3 fails against C by
  construction — its expected table has an exempt cell and three marker-placed cells in the same
  two columns [src: WI-0003 AC3].

## Decision

1. **A module-level compiled pattern `_BREAK_TAG` and a predicate `has_break_tag(text)` are added
   to `mdtab.py`, beside `column_alignments`.** The pattern is `<br\s*/?>` compiled with
   `re.IGNORECASE`, which is ADR-0008 decision 1's shape and no more: `<`, `br` in any letter
   case, any whitespace, an optional `/`, `>` [src: ADR-0008].
2. **`compose_row` consults `has_break_tag` on each cell's text, as the first branch of its
   existing before-padding chain, ahead of the RIGHT and CENTRE branches** [src: mdtab.py:244].
   When it is true, `before` is 0 and the whole leftover padding follows the text, which is the
   LEFT and no-marker path the function already has.
3. **`column_alignments` is not changed, and `emit_block` is not changed** [src: mdtab.py:220;
   src: mdtab.py:287]. A column's alignment stays a property of the delimiter row, which is what
   makes AC7's colon-for-colon identity and ADR-0004 decision 1 keep holding without anyone
   defending them.
4. **The predicate is compiled once at module level, not per call.** `compose_row` runs once per
   cell of every table in the document, and re-compiling inside it would be the one place in this
   filter where a per-cell cost is paid for nothing. This is a preference, not a measurement: no
   performance requirement exists on this tool and none is being invented.
5. **The predicate is a substring search over the cell's text as split, not over the raw line.**
   `split_cells` has already discarded the outer pipes and stripped the surrounding whitespace
   [src: mdtab.py:143], so a break tag in a delimiter cell is unreachable — a delimiter cell that
   `table_or_none` accepted matches `^:?-+:?$` and can contain no `<` [src: mdtab.py:90;
   src: ADR-0007].

## Consequences

Easy: the diff is one pattern, one predicate, one branch and one docstring, in one file. Nothing
that recognises a table, measures a column or composes a delimiter row changes, so every criterion
of WI-0001 and WI-0002 that does not involve a break tag is untouched by construction rather than
by testing. A cell containing no break tag reaches exactly the branch it reaches today.

Hard: the predicate is textual and knows nothing about context. A cell whose text says `<br>`
inside a code span, or as prose about HTML, is exempt like any other — ADR-0008 decision 3 says
"nothing else exempts a cell" and this is its other half, "and nothing exempts a cell from being
exempt". That cost was stated to the stakeholder's options and is recorded in ADR-0008's
consequences; it is repeated here because this is the file a developer reads.

Reversibility: high, and cheaply so. Reversing decision 2 is deleting one branch; reversing
decision 1 is deleting two lines. Moving to option B later would be a refactor of two functions
with no change in behaviour, and the criteria would not move. What is not reversible from here is
option C, and only because it was never taken: adopting it would change the output of every table
that mixes an exempt cell with marker-placed cells, which is the behaviour ADR-0008 decision 6
fixes and only the stakeholder may reopen.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T00:23:48Z | plan | WI-0003 | First version: the break-tag exemption is applied per cell inside `compose_row`, the alignment list is left alone, and the per-column shortcut is named and refused |
