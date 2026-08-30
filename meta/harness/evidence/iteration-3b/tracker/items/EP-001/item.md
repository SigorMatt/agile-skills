---
id: EP-001
type: epic
title: Pretty-align markdown tables from a stdin filter
status: done
priority: high
created: "2026-08-29T21:12:20Z"
updated: "2026-08-30T01:10:42Z"
outcome: delivered
---

## Goal

Someone editing markdown by hand can pipe a document through a single command and get the same
document back with every one of its tables laid out neatly: each column padded to a uniform
width, the alignment markers in the delimiter row respected, and every line that is not part of
a table returned exactly as it arrived. The point is that hand-edited tables stop looking ragged
in the source, without the author having to re-space them by hand and without anything else in
the file being disturbed.

## Why now

Markdown tables are readable in the rendered output whatever their source spacing, so nothing
forces an author to keep the raw text tidy — and raw text is where the author actually lives.
Adding one column, or one row with a longer cell, ruins the alignment of a table that was
previously readable, and re-padding it by hand is tedious and error-prone. The cost of not
solving it is that source tables degrade with every edit, which makes diffs noisier and makes
people avoid touching tables at all. There is no existing tool in this project, and the project
is empty, so this is the first thing it will do.

## Success measures

- Piping a markdown file that contains a ragged table through the filter produces a table in
  which, for every row of that table, the rendered line has the same character width, and each
  column occupies the same character range on every row.
- Piping a markdown file that contains no table produces output byte-identical to the input.
- Diffing the filter's input against its output, for a file containing both prose and tables,
  shows changed lines only inside tables.
- Running the filter twice over the same input produces output identical to running it once.
- A table whose delimiter row carries alignment markers comes back with each column's cell text
  positioned according to that column's marker — with one exception the stakeholder added at the
  sign-off: a cell whose content contains a line break sits at the left of its column whatever the
  marker says [src: EP-001/Q-005; src: ADR-0007]. What exactly counts as a line break, and whether
  such a cell is still padded to its column's width, are `WI-0003`'s questions for them and are not
  settled here [src: WI-0003].
- A file whose only pipe-delimited rows sit inside a fenced code block comes back byte-identical
  to the input.
- A file containing a malformed table — a missing delimiter row, or a row with a different number
  of cells from its header — comes back byte-identical to the input.
- No line the filter writes ends in a space or a tab.

## Scope

- A command that reads markdown from standard input and writes markdown to standard output.
- Recognising tables in the input, and leaving everything else alone. Recognition follows
  ADR-0002: GitHub-flavoured pipe tables with a leading and trailing pipe on every line, outside
  a fenced code block, with a consistent cell count on every row.
- Tracking fenced code blocks while reading, so that table-looking lines inside one are copied.
- Passing a malformed table through unchanged, as a whole block, rather than repairing it.
- Padding each column of a recognised table to a uniform width.
- Honouring the alignment markers in a table's delimiter row.
- Exempting a cell that contains a line break from its column's marker, and leaving it at the left
  of the column. Added to this epic's scope by the stakeholder's answers to `EP-001/Q-004` and
  `EP-001/Q-005`, and carried by `WI-0003` [src: ADR-0007].
- Enough automated tests that each of the success measures above can be checked by running a
  command.

## Out of scope

- Reading or writing files by path, editing in place, or any argument other than what is needed
  to run the filter. The stakeholder asked for a stdin filter.
- Rendering markdown to HTML, or any other output format.
- Reformatting anything other than tables — no wrapping of prose, no heading normalisation, no
  list re-indentation.
- Repairing malformed tables into valid ones. A malformed table is copied, not fixed.
- Any table syntax other than pipe tables — grid tables and rst tables in particular, which the
  stakeholder asked us not to look for.
- Reporting, warning or exiting non-zero when a table is skipped. The tool is silent about what
  it declined to touch.
- Any interactive mode, editor plugin, or configuration file.
