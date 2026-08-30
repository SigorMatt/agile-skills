---
id: WI-0001
type: work-item
title: Align markdown table columns, passing all other content through unchanged
status: done
priority: high
epic: EP-001
created: "2026-08-29T21:12:23Z"
updated: "2026-08-29T22:14:55Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone who edits markdown documents by hand, I want to pipe a document through one command
and get it back with every table's columns padded to a uniform width, so that my source tables
stay readable after I edit them without my having to re-space them myself.

## Acceptance criteria

*In every criterion below, "running the filter" means running the single Python 3 script
ADR-0001 specifies, with no arguments, the named input on standard input and output captured
from standard output. "Display width" means the function ADR-0003 decision 7 defines: 2 for a
character whose `unicodedata.east_asian_width` is `W` or `F`, 0 for a combining mark, 1
otherwise. "A table" means what ADR-0003 decisions 2 and 3 recognise as one.*

- [x] AC1 — Given input containing a table whose rows differ in width, and whose cells include
      an East Asian wide character, an emoji and a letter carrying a combining accent, every
      line of that table in the output has the same display width.
- [x] AC2 — In that output table, every column occupies the same span of display columns on
      every row of the table, including the delimiter row.
- [x] AC3 — Every content cell in the output — header row and body rows — is written as `|`,
      one space, the cell's text with leading and trailing whitespace removed, spaces padding it
      to the column's width, then one space. A cell whose text is empty is written as `|`
      followed by two spaces. No line the filter composes ends in a space or a tab.
- [x] AC4 — The delimiter row in the output is, for each column, `|` followed by (that column's
      width + 2) hyphens and no spaces, closed by a final `|`. Given a table whose input
      delimiter row is longer than any of its content cells, the output delimiter row is
      narrowed accordingly: the delimiter row does not contribute to a column's width.
- [x] AC5 — Given a table every line of which begins with the same non-empty run of spaces, the
      output tidies that table and every one of its output lines begins with that same run,
      byte for byte. Given a block whose lines' leading whitespace differs between lines, and
      given a block whose lines each begin with `> `, the output is byte-identical to the input
      for those lines.
- [x] AC6 — Given input containing no table, the output is byte-identical to the input. This
      holds for empty input, for input whose last line has no terminating newline, for input
      with CRLF line endings, and for input containing bytes that are not valid UTF-8.
- [x] AC7 — Given input containing prose, headings, a fenced code block opened with ``` and one
      opened with `~~~` — each containing lines that would otherwise be recognised as a table —
      and a real table outside both fences, every output line that is not part of that real
      table is byte-identical to the corresponding input line.
- [x] AC8 — Given a block of pipe lines that is not a well-formed table — its second line is not
      a delimiter row, or one of its rows has a different cell count from its header — every
      line of that block is byte-identical to the input, including the rows of it that were
      well formed.
- [x] AC9 — Running the filter on its own output produces output byte-identical to that output,
      for each of the inputs named in AC1 and AC5 to AC8.
- [x] AC10 — The filter exits with status 0 for every input named in AC1 to AC9.
- [x] AC11 — An automated test exists for each of AC1 to AC10, each naming the criterion it
      covers, and the whole suite passes with the command recorded in `tracker/project.yaml`.

## Out of scope

- Positioning cell text according to the delimiter row's alignment markers; that is WI-0002.
  This item may leave marker characters in place unchanged, and AC4's hyphen rule describes a
  delimiter cell that carries no marker.
- Tables inside a blockquote. The stakeholder declined them explicitly: *"Quoted ones I have
  never written and do not expect to, so do not spend anything on them"* [src: WI-0001/Q-002].
- Tables written without outer pipes, and grid or rst tables. ADR-0003 decisions 2 and 5 copy
  them; nothing reports that they were skipped.
- Distinguishing a table inside an *indented* code block from a table indented under a list.
  ADR-0003 decision 2 accepts that such a table will be tidied; only **fenced** blocks are
  protected.
- Any maximum column width, wrapping, or truncation. Columns grow to fit
  [src: EP-001/Q-001].
- Any input source other than standard input, any output other than standard output, and any
  argument, flag or configuration file.
- Reformatting non-table content, and reporting anything about a document to the user.

## Notes

**Where the rules live.** `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` is the
authoritative statement of what counts as a table and what one looks like coming back; it
supersedes ADR-0002 and every criterion above is checkable against it. The criteria were written
from two rounds of stakeholder answers — `EP-001/Q-001` to `Q-003` at intake, and `WI-0001/Q-001`
to `Q-004` at refinement — whose verbatim text is in `artifacts/refinement-qa.md`.

**Constraints the criteria assume, and where each comes from:**

- A single Python 3 script, standard library only, run as a stdin filter [src: ADR-0001].
- Conservatism is the first property: anything the filter cannot recognise is copied, and a
  block containing one bad row is copied whole rather than partly tidied [src: ADR-0003].
- A line the filter *copies* keeps whatever trailing whitespace and line ending it arrived with;
  only lines the filter *composes* are constrained by AC3. Those two are not in conflict —
  ADR-0003 decision 6 says why.
- Column widths have no maximum and nothing is wrapped or truncated [src: EP-001/Q-001].

**Settled by `refine` without asking, from what the stakeholder already said** — recorded as
assumptions in `artifacts/refinement-qa.md` rather than as things they decided:

- A copied line keeps its own line ending; a composed line takes the ending of the line it
  replaces. Both follow from *"exactly as it went in, byte for byte"* [src: EP-001/Q-001], and
  AC6 is how it is observed.
- Empty input produces empty output and exit status 0; the filter never exits non-zero for a
  document it declined to touch (AC10).
- Input containing bytes that are not valid UTF-8 must still round-trip byte for byte (AC6).
  That is the same promise as any other passthrough, applied to a case they did not name.

**Open design questions for `plan`, deliberately not sent to the stakeholder.** Each would have
the same answer whoever the stakeholder was, so `refine` routed them here rather than spending a
round trip (`refine` step 3):

- How an escaped pipe (`\|`) inside a cell is treated. GitHub-flavoured markdown, which the
  stakeholder named [src: EP-001/Q-003], makes it content rather than a cell boundary.
- How the script reads and re-emits bytes that are not valid UTF-8, which AC6 requires it to
  round-trip. Reading as text with `errors="surrogateescape"` is one way; the choice is `plan`'s.
- Where the script lives and what invokes it. AC11 requires `tracker/project.yaml`'s
  `commands.test` to be set — it is currently null, and `validate-workspace` warns about it —
  and every criterion above is run through the script `plan` places.
- A tab inside a cell's text counts as one column under ADR-0003 decision 7. Recorded so that it
  is a known consequence rather than a rediscovered gap.

**Gaps accepted at review, on closing this item.** Each was declared in
`artifacts/verify-report.md` `## Not verified, and why` or `artifacts/impl-report.md`
`## What I did not do`, judged acceptable by `review-close`, and written here because nobody reads
a closed item's reports again:

- **Column alignment inside a document that is not valid UTF-8 may be wrong.** A byte carried
  through by `surrogateescape` counts as one display column, which is a guess. Only the *columns*
  are affected; the byte-for-byte passthrough promise was verified and holds (AC6). No criterion
  covers it and none was added. Recorded in `artifacts/plan.md` `## Risks` as well.
- **Display width is an approximation of a terminal, not a measurement of one.** The stakeholder
  accepted this in advance — *"If a rare emoji is off by one in some terminal I will live with
  it"* [src: WI-0001/Q-001] — and nothing in this project can check a real terminal.
- **A pipe table inside an *indented* code block is tidied.** Already in `## Out of scope` above;
  repeated here because it is the one accepted behaviour most likely to be filed as a bug later.
- **Nothing was measured about performance on a large document.** No criterion mentions it.
- **The vision's second product property — cell text placed according to the alignment markers —
  is not delivered by this item and is not meant to be.** WI-0002 delivers it, and
  `docs/product/vision.md` `## What is not yet decided` already names it as outstanding. Recorded
  so that a reader who meets that sentence while reading this item is not misled.

**A defect in the pipeline's own tooling, found while building this item and worked around, not
fixed.** `.claude/agile-skills/scripts/validate-workspace` and `.claude/agile-skills/scripts/lint-claims`
walk every `*.md` file in the repository and decode it with `encoding="utf-8"` and no error
handler; `validate-workspace` catches only `OSError`. Any markdown file that is not valid UTF-8 —
which AC6 requires this project to contain — makes both exit with an uncaught `UnicodeDecodeError`
traceback instead of a finding. The workaround is that the fixture is named
`tests/fixtures/not_utf8.markdown` rather than `.md`, which those walkers skip. No `bug` item was
filed: a bug in this tracker is filed against behaviour an *item* delivered, and no item owns the
toolkit. Anyone renaming that fixture to `.md` will break two gates.

**DoR R10 — combinations of behaviours:** the tool has no options, flags or modes. It reads
standard input, writes standard output and takes no arguments, so there is no combination of
behaviours to specify. Recorded here because R10 asks for it to be visible rather than absent.
