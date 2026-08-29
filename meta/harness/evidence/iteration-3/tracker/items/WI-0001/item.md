---
id: WI-0001
type: work-item
title: Align table columns in a stdin-to-stdout markdown filter
status: done
priority: high
epic: EP-001
created: "2026-08-28T18:24:38Z"
updated: "2026-08-28T20:06:15Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone who edits markdown documents by hand, I want to pipe a document through a command and
get it back with every table's columns padded to a common width, so that I can read and edit the
table in a plain text editor without counting spaces.

## Acceptance criteria

- [x] AC1 — with a markdown document on stdin, the tool writes the whole document to stdout and
      exits 0, when run from a checkout on a machine that has Python 3 and nothing else
      installed for it (`EP-001/Q-001`, ADR-0001). The exact invocation is recorded by `plan` in
      `artifacts/plan.md`; every criterion below is checked against that invocation.
- [x] AC2 — for every table in the output, all rows of that table have the same *display width*,
      and each `|` separator sits at the same display column in every row of the table. Display
      width is the rule in ADR-0002 — combining marks, joiners and variation selectors count 0,
      East Asian wide and fullwidth characters count 2, everything else counts 1 — not the number
      of characters (`EP-001/Q-003`). Display columns are counted from the start of the line,
      which is well defined even for an indented table because AC15 requires every line of that
      table to carry the same prefix.
- [x] AC3 — AC2 holds for a table whose cells contain accented letters written both precomposed
      (`é`, U+00E9) and decomposed (`e` + U+0301), an emoji with a variation selector, and CJK
      text — not only for ASCII ones (`EP-001/Q-003`).
- [x] AC4 — every line of the input that is not part of a table appears in the output
      byte-for-byte unchanged, in the same order.
- [x] AC5 — a document containing no table is reproduced on stdout byte-for-byte.
- [x] AC6 — the tool is idempotent: running it on its own output produces identical bytes.
- [x] AC7 — a table is a run of consecutive lines containing `|` whose **second** line is a
      delimiter row: cells made only of `-`, optional `:` at either end, and spaces. Both are
      judged after the line prefix of AC15 has been stripped. A **run** is a maximal sequence
      of two or more consecutive lines, none of them inside a fenced code block (AC8), each
      containing at least one unescaped `|` (AC10); it ends at the first line that does not, or
      at the end of the document. A run whose second line is not a delimiter row is not a
      table. Checked by feeding a document that
      contains a reStructuredText grid table (`+---+---+`), a raw HTML `<table>`, and a run of
      pipe lines with no delimiter row, and observing that all three come back byte-for-byte
      under AC4 (`EP-001/Q-002`).
- [x] AC8 — lines inside a fenced code block are reproduced byte-for-byte, including lines that
      would otherwise satisfy AC7 (`EP-001/Q-002`). A code block opens at a line whose content,
      after its AC15 prefix is stripped, is three or more consecutive backticks or three or more
      consecutive tildes optionally followed by anything else, and closes at the next line whose
      prefix-stripped content is at least as many of the same character and nothing else. A fence
      that is never closed runs to the end of the document, as it does in every markdown
      renderer. The opening and closing fence lines are themselves reproduced byte-for-byte.
      Checked by feeding a document whose fenced block contains a ragged pipe table and whose
      final fence is missing, and diffing input against output.
- [x] AC9 — line terminators and the end of the document are preserved: a document whose lines
      end `\r\n` comes back with `\r\n`, and a document whose final line has no trailing
      newline comes back with none. Checked with `xxd` or `od -c` on the last bytes. A line's
      terminator is not part of the line for the purpose of any criterion here: it is removed
      before the line is examined and restored unchanged afterwards, so a `\r` never becomes
      part of a cell and never affects a width, a cell count or an outer-pipe test.
- [x] AC10 — an escaped pipe `\|` inside a cell is not a cell separator. A table row
      `| a \| b | c |` comes back with two cells, the first containing `a \| b`. A `|` is
      escaped exactly when the number of consecutive `\` characters immediately preceding it is
      odd, so `| a \\| b |` is two cells and `| a \| b |` is one.
- [x] AC11 — cell content is unchanged apart from the spaces around it: for every cell, the
      output cell with leading and trailing spaces stripped is byte-for-byte equal to the input
      cell with leading and trailing spaces stripped.
- [x] AC12 — a laid-out cell is rendered as `|`, one space, the cell content, padding spaces,
      one space, then the next `|`; so every column is `2 + max(display width of its cells)`
      columns wide, and an empty cell renders as two spaces between pipes. Two clauses qualify
      that arithmetic, and both are forced by AC6 rather than chosen (`WI-0001/Q-005`):
      the maximum is taken over the header row and the body rows only, never over the delimiter
      row's own cell, because a column measured over a delimiter cell that was itself widened to
      the column would grow on every run; and a column is never narrower than its delimiter cell
      can be written. The delimiter row's *field* in a column — the characters between that
      column's pipes, less whichever of the two surrounding spaces the row's outer-pipe style
      drops (AC14) — must hold at least one `-`, plus one character for a leading `:` and one
      for a trailing `:` where the input's delimiter cell had them. Where `2 + max` would leave
      a smaller field than that, the column is widened until it does not.
      The only column that is ever widened this way is one whose header and body cells are all
      empty: with marker `:---:` such a column is 3 wide rather than 2, and with `---` or `:---`
      it is 2. The delimiter row's cells are filled with `-` across the whole field, keeping any
      `:` at the ends they had. The outer `|` at the start and end of a row is
      present in the output exactly when it was present in the input, per AC14; a row without
      outer pipes therefore begins with its first cell's content and ends with its last cell's,
      each still separated from the interior `|` by one space.
- [x] AC13 — a run of lines that would otherwise be a table under AC7, but whose rows do not
      all contain the same number of cells, is **not** laid out: every line of that run is
      reproduced byte-for-byte, as under AC4. Cells are counted by splitting a row on its
      unescaped `|` (AC10) and discarding the empty field a leading pipe produces and the one a
      trailing pipe produces; the header row, the delimiter row and every body row must agree.
      Checked by feeding a table whose body contains a row with one cell too many and a row with
      one too few, and diffing the input against the output (`WI-0001/Q-001`, ADR-0003 rule 3).
- [x] AC14 — a pipe table whose rows are written without a leading `|`, without a trailing `|`,
      or without either is recognised and laid out, and the output carries exactly the outer
      pipes the input had: none are added to a table that had none, none are removed from a
      table that had them, and no `|` is added to or removed from any line of the document. A
      run whose rows do not all agree about both the leading and the trailing pipe is **not**
      laid out and is reproduced byte-for-byte, as under AC4 (`WI-0001/Q-002`, ADR-0003 rule 4).
- [x] AC15 — a table every line of which begins with the same prefix is laid out inside that
      prefix. A line's prefix is its maximal leading run of space, tab and `>` characters,
      compared byte-for-byte between lines; the prefix is reproduced unchanged at the start of
      every output line of the table, the table is laid out as though the prefix were not there,
      and AC2 holds. A run whose lines' prefixes are not byte-identical is **not** laid out and
      is reproduced byte-for-byte, as under AC4. A run's extent is fixed by AC7 *before* its
      prefixes are compared, so a change of prefix part-way through disqualifies the whole run
      rather than splitting it into two shorter ones. Checked with a table inside a blockquote (`> `
      on every line), a table indented two spaces under a list item, and a blockquote table one
      of whose rows carries extra spaces after its `>` (`WI-0001/Q-003`, ADR-0003 rule 2).

## Out of scope

- Honouring the alignment markers `:---`, `:---:` and `---:` — that is WI-0002. This item pads
  every cell the same way regardless of what the delimiter row says, and must not lose the
  markers from the delimiter row (AC12).
- Reading or writing files by name; stdin and stdout only.
- Any change to cell text: no trimming beyond the padding needed to align, no rewrapping (AC11).
- Splitting a table whose rendered width exceeds any particular number of columns. A wide table
  comes back wide; the tool has no maximum line length.
- Any diagnostic output. The tool writes the document on stdout and nothing on stderr, even when
  it meets something it does not recognise as a table (EP-001 out of scope: not a linter).

## Notes

The three questions this item's criteria depended on have been answered by the stakeholder and
propagated here: the runtime and invocation (`EP-001/Q-001`, ADR-0001) into AC1, which syntaxes
count as a table (`EP-001/Q-002`) into AC7 and AC8, and how cell width is measured
(`EP-001/Q-003`, ADR-0002) into AC2 and AC3.

### Settled by the stakeholder, round 1

`WI-0001/Q-001`, `Q-002` and `Q-003` have been answered and propagated into the criteria above.
The three answers are one policy, recorded as ADR-0003: the tool lays out a run of lines only
when every row agrees about its cell count (AC13), its outer-pipe style (AC14) and its leading
prefix (AC15) — and it copies anything else through byte-for-byte. Inside a table it changes
spaces and nothing else; it never adds or removes a `|`, in the stakeholder's words *"I only
want the spacing changed, never the punctuation"* (`WI-0001/Q-002`).

One case nobody asked about was settled by ADR-0003 on the strength of those answers rather
than by a fourth question: a run whose rows disagree about their outer-pipe style. It is left
byte-for-byte, because laying it out per-row would keep the punctuation promise of `Q-002` while
breaking AC2's promise that the pipes line up. The stakeholder disposed of the analogous case
themselves — *"same as any other table you don't understand"* (`WI-0001/Q-003`) — which is what
makes it derivable rather than a guess.

### Assumed, and open to being overturned

AC9 to AC12 were not asked about. They follow from what the stakeholder has already said, and
each is recorded as `[assumed]` in `artifacts/refinement-qa.md` with the basis it rests on. They
are cheap to change if the stakeholder disagrees when they read them.

Refinement round 2 added five more mechanical clarifications, none of which was put to the
stakeholder: what a *run* is (AC7), when a code fence opens and closes and what an unclosed one
does (AC8), that a line's terminator is not part of the line (AC9), what "escaped" means for a
`|` (AC10), and that a prefix change disqualifies a run rather than splitting it (AC15). Each is
`[assumed]` in `artifacts/refinement-qa.md`. They rest on the stakeholder's standing deferral —
*"The rest of how it's built is your call, not mine"* (`EP-001/Q-001`) — and each would have the
same answer whoever the stakeholder was, which is what kept them off a fourth question round.

### Routed to `plan`, not to the stakeholder

- What the entry point is called and how it is invoked. ADR-0001 delegates it explicitly, and
  AC1 defers to whatever `plan` records.
- Whether the tool streams the document or reads it whole. Nothing observable in these criteria
  distinguishes the two, so it is a design decision.
- What the test framework is. `ADR-0001` leaves it to `plan`, and `tracker/project.yaml` keeps
  `commands.test` null until then.

### Gaps review accepted

Recorded here by `review-close` because a gap that lives only in a report is forgotten once the
item closes.

- **AC12's degenerate-column gap is closed — see `### AC12 amended, round 3` below.** It is
  recorded here as a gap only because `review-close` accepted it as one in the first review
  cycle; the criterion has since been amended and the exception no longer exists.
- **The CPython 3.8 floor `plan.md` sets is asserted, not tested.** Only CPython 3.12.3 is
  installed here, so no run can prove it. `review-close` read for it instead — no
  `str.removeprefix`, no match statement, no 3.9+ builtin in `mdtab/`, and
  `from __future__ import annotations` wherever an annotation appears — but an inspection is not a
  check, and it stays one until a second interpreter exists.
- **How a terminal or editor font actually draws the output is not verifiable from here.** AC2 and
  AC3 are met against ADR-0002's rule, which is what they name; ADR-0002's own recorded limitation
  for joined emoji sequences and for ambiguous-width characters in a terminal configured to draw
  them wide is unchanged and is documentation, not a defect.

Added by the second review, on the second verification's declared gaps:

- **The shipped fixtures' expected outputs were not independently re-derived.** The suite asserts
  the code reproduces them; the second verification's own evidence came from documents written
  during verification instead. Both checks would miss a fixture whose hand-written expected
  output is wrong in a way none of the fifteen criteria detects. Review read the fixture pairs
  hunk by hunk in the first cycle and no fixture's expected output has changed since, which
  bounds the risk rather than removing it.
- **No README or user-facing documentation.** No criterion asks for one and the epic does not
  scope it; ADR-0002's limitation about joined emoji sequences lives in the ADR rather than
  anywhere a user would read. Worth an item if the tool is ever published — not filed as one,
  because nobody has asked to publish it.
- **`validate-workspace` aborts with a `UnicodeDecodeError` traceback on any `.md` file it cannot
  decode.** A defect in the pipeline's machinery, not in mdtab, and one that stops every skill
  because `workspace-valid` is a hard gate of all of them. Reported in ADR-0006's
  `## Consequences` and in this item's journal, deliberately not patched from inside a work item.
- **Concurrency, large inputs and pathological documents are unexercised.** No criterion mentions
  them; the largest document run through the tool in either verification was 27 lines.
- **`impl-report.md`'s `## Deviations from the plan` 3 miscounts.** It says "One fixture beyond
  the plan's list: `tab-prefix`"; three fixtures are not named in `plan.md`'s mapping table —
  `empty-cells`, `tab-in-cell` and `tab-prefix`. `tab-in-cell` is declared elsewhere in the same
  report, so the undeclared one is `empty-cells`, which is what plan step 10 requires anyway: a
  test may not build a document from a Python literal, so AC12's empty-cell assertion has nowhere
  but a fixture to put its document. Accepted rather than sent back — nothing in `docs/` is
  false, no ADR is contradicted and no behaviour is in question. The true count is recorded here
  because a reader of a closed item reads `## Notes`, not the report.

### Settled by the architect, round 2

`WI-0001/Q-004` asked how the AC9 undecodable-bytes document should be stored, because
`ADR-0005` requires it to be a `.md` fixture and `validate-workspace` cannot read a `.md` file
that does not decode as UTF-8. Decided as `ADR-0006`, not escalated: none of the four conditions
in `spec/question.md` §4 applies — the stakeholder deferred how it is built (*"The rest of how
it's built is your call, not mine"*, `EP-001/Q-001`), the change is two filenames and one
expression, and it reverses nothing `ADR-0005` decided.

A fixture whose bytes are deliberately not valid UTF-8 carries `.in.bin` / `.out.bin`; every
other fixture keeps `.in.md` / `.out.md`; `tests/test_fixtures.py` discovers pairs by the `.in.`
infix. No acceptance criterion changed — AC9 says nothing about how a fixture is named, and the
behaviour it asks for is unaffected.

`Q-004` did not touch AC12; that criterion got the question of its own it needed, and the next
section records the answer.

### AC12 amended, round 3

`WI-0001/Q-005` was filed by the second verification and answered by `answer-questions` from the
record. It asked one thing: how AC12's width clause should be worded so that it and AC12's own
delimiter clause are jointly satisfiable, without changing behaviour that `plan.md`, both
verifications and `review-close` had already accepted.

**AC12 has been amended and no behaviour changed.** Its "exactly `2 + max(display width of its
cells)`" now carries the two qualifications AC6 forces and that the tool has implemented since
the first delivery: the maximum is taken over the header and body rows only, never over the
delimiter row's own cell; and a column is never narrower than its delimiter cell can be written.
The one column affected is one whose header and body cells are all empty — with `:---:` it is 3
wide rather than 2.

Neither qualification is a change to what the stakeholder asked for. Both were already required
by AC6, which is a criterion of this item; the amended text makes AC12 consistent with AC6
rather than reshaping it around the code. AC12's basis is `[assumed]` in `refinement-qa.md` —
"not asked" — resting on the stakeholder's standing deferral, *"The rest of how it's built is
your call, not mine"* (`EP-001/Q-001`); and the alternative wording, which would have dropped a
`:` from a column too narrow to hold both, was rejected because it loses punctuation the
stakeholder asked to keep — *"I only want the spacing changed, never the punctuation"*
(`WI-0001/Q-002`) — and because WI-0002 is about to start honouring exactly those markers.

The verification of this item stands: `verify-report.md`'s AC12 row and its
`### AC12's one exception` section are the evidence for the amended clause, and the behaviour
they record is unchanged.

### Combinations (Definition of Ready R10)

This item introduces no flags, options or modes, so there are no option combinations to specify.
The behaviour combinations that exist are between the document's own constructs, and each is
either decided or named:

- A table adjacent to, or immediately after, a fenced code block — decided by AC8 and AC4.
- Two tables separated by a blank line, and a table at the very first or very last line of the
  document — decided by AC7, which needs only a run of pipe lines and a delimiter row.
- A table inside a blockquote or a list item — decided by AC15: laid out inside a prefix every
  line of it shares, left alone otherwise.
- A malformed table inside a fenced code block — decided by AC8 rather than AC13, because the
  fence wins; the run is reproduced byte-for-byte either way.
- An indented table that is also written without outer pipes, or that is also malformed — the
  three recognition rules are independent conditions on the same run (ADR-0003), so the run is
  laid out only if it passes all of them and is reproduced byte-for-byte if it fails any.
- A table inside a fenced code block that is itself inside a blockquote, and a fence whose
  opening line is indented — decided by AC8, which strips the AC15 prefix before deciding
  whether a line is a fence, so a quoted or indented fence protects its contents exactly as an
  unindented one does.
- An unclosed code fence at the end of a document — decided by AC8: it runs to the end of the
  document, so nothing after it is laid out.
- A one-column table written without outer pipes (`name` over `---`) — decided by AC7: such a
  line contains no `|`, so it is not part of a run and is not a table. It is not a GFM table
  either, so a renderer agrees.
- A run that begins unindented and continues indented, or the reverse — decided by AC15: the
  run's extent comes from AC7 first, so the whole run is disqualified and reproduced
  byte-for-byte rather than split into a laid-out part and an untouched part.
- A tab character inside a cell — deliberately unconstrained by `refine`. Under ADR-0002 a tab
  counts as one display column, which is what the criteria will judge; whether that matches any
  particular editor's tab stops is out of this tool's control, and nobody has asked for it.
- A tab inside the AC15 prefix — decided by AC15, which compares prefixes byte-for-byte: a
  tab-indented line and a space-indented line do not share a prefix, so a run mixing them is
  reproduced byte-for-byte.
