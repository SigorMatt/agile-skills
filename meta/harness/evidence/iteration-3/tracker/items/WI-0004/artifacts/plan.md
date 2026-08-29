# Plan — WI-0004 Leave a cell containing a line break plain, whatever its column marker says

## Problem

mdtab pads every cell of a column the same way, from the column's marker in the delimiter row.
For a cell holding an HTML `br` tag that is wrong: the cell reads as two lines, and centring or
right-shifting it puts the first line somewhere the second one is not. The stakeholder asked for
such a cell to sit plain at the left, whatever the marker says, and settled the three questions
that turn that into criteria — every spelling of the tag counts, a tag written inside a code span
does not, only the cell with the break moves, and the header row is no exception
[src: WI-0004/Q-001; src: WI-0004/Q-002; src: WI-0004/Q-003]. The constraints are narrow: column
widths are still measured from the cell's text exactly as typed, the delimiter row's marker is
never rewritten [src: WI-0004 AC2], no existing test is expected to change [src: WI-0004 AC5], and
the epic's standing properties — idempotence, non-table lines byte-for-byte, silence, exit 0 —
must survive [src: WI-0004 AC4]. This is the last item in the engagement: *"Fix that and we are
done"* [src: EP-001/Q-005].

## Approach

One override, in one place, fed by one new module.

**The override.** `mdtab/table.py` goes on deriving one alignment per column from the delimiter
row, exactly as [src: ADR-0007] left it. `_render_row` — which already knows whether it is
rendering the delimiter row, and already strips each cell before handing it to `_render_cell` —
chooses `"left"` instead of `alignments[column]` when the stripped cell text contains a line
break. Because the choice is made per cell at the point of render, the other cells of the column
are untouched [src: WI-0004 AC3]; because the header row is rendered by `_render_row` like every
other non-delimiter row, it is included without a clause of its own [src: WI-0004 AC6]; and
because the delimiter row goes to `_render_delimiter` on the other side of the same branch, no
marker can be rewritten [src: WI-0004 AC2]. Nothing in `_column_widths`, `_render_cell` or
`column_alignments` changes, so a column's width and the guard spaces are as they were, and the
row's total display width is unchanged — which is why the fixture-wide invariants keep holding.

**The detection.** A new module, `mdtab/inline.py`, answers one question of one cell's text:
does it contain an HTML `br` tag that is not inside a code span. It is a new module rather than
three more lines of `mdtab/table.py` because it is the first *inline* markdown grammar this tool
reads, and `table.py` owns the grammar of where a cell **ends** — a rule the recognition path
depends on. Keeping them apart is what stops the recognition path acquiring a dependency on code
spans, which it must never have [src: ADR-0010].

The rules it implements, in full:

1. **The tag.** `<`, then `br` in either case, then either `>` immediately, or one of space, tab
   or `/` followed by any run of characters up to the next `>`. `<br>`, `<BR>`, `<br/>`,
   `<br />` and `<br class="k">` all match; `<brx>` does not [src: WI-0004 AC1].
2. **The code spans, found first and excluded from the search.** A run of *n* backticks opens a
   span, closed by the next run of exactly *n* backticks; everything from the opening run to the
   closing run inclusive is the span. A run with no matching closer is literal text, and the scan
   resumes after it looking for the next opener. A backslash before a backtick is an ordinary
   character — this project's only escaping rule is the one about `|` in `split_row`
   [src: WI-0001 AC10], and a second one is not needed by any criterion.
3. **One cell at a time.** The answer depends on the cell's text and on nothing else in the
   document, which is what keeps the layout idempotent: the text a cell is measured and rendered
   from is the same text on the second run [src: WI-0001 AC6].

Worked through the cases the criteria and `## Notes` name, this rule gives: `a<br>b`, `a<BR/>b`,
`c<br />d`, `e<br class="k">f` and a cell that is only `<br>` → left; `` `<br>` `` and
``` ``<br>`` ``` → the column's marker, unchanged [src: WI-0004 AC7]; and the three cases
[src: WI-0004] left deliberately unconstrained → `` a`<br>b `` left (the run never closes, so
there is no span), ``` ``<br>`` ``` and a span holding a shorter backtick run → marker, and
`` a`<br>`b<br>c `` left (the second tag is outside the span). Those three are decided in
[src: ADR-0010] §3, which is what `verify` judges them against.

**What this does not do.** It does not measure anything new — a cell's width is still the display
width of its text as typed. It does not touch recognition, run extent, fences, prefixes, escaped
pipes or terminators. It adds no output and no diagnostic.

## Steps

1. **Add `mdtab/inline.py`.** One public function, `contains_line_break(text: str) -> bool`,
   returning `True` when `text` holds a `br` tag outside a code span, per `## Approach` rules 1–3;
   plus whatever private helper finds the spans. Module docstring states the two rules and cites
   [src: ADR-0010]. Afterwards: `python3 -c "from mdtab.inline import contains_line_break"`
   succeeds, and the function answers the worked cases above.
2. **Override the column's alignment per cell in `mdtab/table.py`.** In `_render_row`, in the
   non-delimiter branch, pass `"left"` to `_render_cell` in place of `alignments[column]` when
   `contains_line_break` is true of the same stripped text that is passed as the cell's content.
   Import from `mdtab.inline` at module scope — `inline` imports nothing from `table`, so there is
   no cycle to break at a call site as there is with `scan`. Update `_render_row`'s and
   `_render_cell`'s docstrings to say where the alignment now comes from, citing
   [src: ADR-0010]. Afterwards: the four transcripts in AC1, AC6 and AC7 produce the outputs those
   criteria require, checked by hand at a terminal before any test is written.
3. **Unit-test the detection rule in `tests/test_units.py`.** A new class, `LineBreakTest`,
   importing `contains_line_break`: one test that every spelling in AC1 counts and that case, a
   slash, internal spaces and attributes make no difference; one that `<brx>` and `</br>` do not
   count (the assumptions below); one that a tag inside a single-backtick span does not count
   [src: WI-0004 AC7]; and one test per unconstrained case of [src: ADR-0010] §3 — the unbalanced
   backtick, the multi-backtick span with a shorter run inside it, and the cell holding a tag both
   inside and outside a span — each asserting the outcome that table gives. Afterwards: the class
   fails against the code as it stands before step 1 and passes after step 2.
4. **Unit-test the override through `lay_out` in `tests/test_units.py`.** A new class,
   `LineBreakPlacementTest`, driving `lay_out` on hand-written runs and asserting on the returned
   lines: (a) a `:---:` column and a `---:` column each return the break cell flush against its
   opening guard space with the padding after it [src: WI-0004 AC1]; (b) a three-row centred
   column whose middle row has the break returns rows 1 and 3 centred exactly as they are today
   and only the middle one flush left, with the column's width and the delimiter row's text
   unchanged [src: WI-0004 AC3; src: WI-0004 AC2]; (c) a header cell with a break comes back flush
   left while its column's other cells stay centred [src: WI-0004 AC6]; (d) a cell whose text is
   `` `<br>` `` in a `---:` column comes back right-aligned, byte for byte as it is today
   [src: WI-0004 AC7]. Afterwards: four tests, each failing before step 2 for the reason it names.
5. **Add two fixture pairs under `tests/fixtures/`, and register them.** `line-break-cells.in.md`
   / `.out.md`: one document holding a table with a centred and a right-aligned column, a header
   cell with a break, body cells spelling the tag four ways, a row with no break in the same
   columns, and a prose line before and after the table. `line-break-code-span.in.md` / `.out.md`:
   a table whose cells write about the tag inside backticks — including a multi-backtick span —
   under a `---:` marker, so the whole table obeys its markers. Both expected outputs written by
   hand, not captured from the code [src: tests/test_fixtures.py]. Add both names to the
   `ALIGNED` dict in `tests/test_fixtures.py` with the line range of each table, which is how a
   fixture joins the document-level invariants. Afterwards: `FixtureRoundTripTest`,
   `AlignmentTest`, `ContentPreservationTest` and the idempotence test all run over the two new
   documents and pass [src: WI-0004 AC4].
6. **Run the gates and record the evidence.** `python3 -m unittest discover -s tests -t .` exits 0
   with no failures and no errors; `python3 -W error -m compileall -q mdtab tests` exits 0;
   `git diff --stat` against the trunk shows no change to any of the twenty tests AC5 names, and
   `grep -rniE '<br' tests/` now exits 0 rather than 1 because the new tests and fixtures contain
   the tag — which is expected and is the point [src: WI-0004 AC5]. Run each AC transcript and
   paste the actual output into `impl-report.md`, including running the tool twice on each
   document and diffing, and checking stderr is empty and the exit code 0 [src: WI-0004 AC4].
7. **Put the two documents into the present tense.** `docs/architecture/overview.md` v8 says four
   times that this design is *"Planned for WI-0004, not yet in the code"* — in the modules table,
   in two one-place-per-rule bullets, and in the "What is deliberately absent" paragraph. Once the
   code exists those sentences are false, so `implement` removes each of them and bumps the
   document to v9 with a change-log row. [src: ADR-0010] needs no edit: it describes a decision,
   not a state of the code.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — any spelling of the tag outside a code span puts the cell left | 1, 2 | `LineBreakTest` (step 3) on the five spellings; `LineBreakPlacementTest` case (a) on `:---:` and `---:` (step 4); the two AC1 transcripts re-run and pasted into `impl-report.md` (step 6) |
| AC2 — the delimiter row's marker is unchanged | 2 | `LineBreakPlacementTest` case (b) asserts the returned delimiter line equals today's (step 4); `LayoutShapeTest.test_ac12_the_delimiter_row_keeps_its_colons_and_fills_the_column`, unmodified |
| AC3 — only the cell with the break moves | 2 | `LineBreakPlacementTest` case (b): a three-row centred column, rows 1 and 3 byte-identical to today's output, row 2 flush left, column width unchanged (step 4) |
| AC4 — idempotence, non-table lines, silence, exit 0 | 5, 6 | the two new fixtures joining `FixtureRoundTripTest.test_ac6_running_the_tool_on_its_own_output_changes_nothing` and `test_ac4_lines_outside_a_table_are_untouched_in_the_fixtures_that_have_one`; plus the double-run diff and the stderr/exit-code check pasted into `impl-report.md` (step 6) |
| AC5 — the suite passes and no existing test changes | 6 | `python3 -m unittest discover -s tests -t .` exit 0; `git diff` against the trunk showing `tests/test_units.py` and `tests/test_fixtures.py` gaining only the new classes and the two `ALIGNED` entries, and none of the twenty named tests altered — quoted in `impl-report.md` |
| AC6 — a header cell with a break sits left too | 2 | `LineBreakPlacementTest` case (c) (step 4); the AC6 transcript re-run and pasted (step 6); the `line-break-cells` fixture's header row (step 5) |
| AC7 — a tag inside a code span is not a break | 1, 2 | `LineBreakTest`'s code-span tests (step 3); `LineBreakPlacementTest` case (d) (step 4); the `line-break-code-span` fixture (step 5); the AC7 transcript, which must come back byte-for-byte identical, pasted (step 6) |

## Assumptions

Each is one regex or one loop in `mdtab/inline.py`, a file with a single caller, so reversing any
of them is a change in one file with no effect on stored data or on any published interface.

1. **`</br>` is not a line break.** [src: WI-0004 AC1] names case, a trailing slash, internal
   spaces and attributes as the variations that must not matter; a *leading* slash makes an HTML
   closing tag, which is not what an author types to break a line. Reversal: one alternation in
   the tag pattern.
2. **A `br` tag ends at the first `>` after it**, so an attribute whose value contains a literal
   `>` — `<br title="a>b">` — is not modelled. It is not a document anyone in this project has
   written, and understanding it means parsing attribute quoting. Reversal: the same pattern, at
   the cost of that parsing.
3. **A backslash does not escape a backtick when spans are found**, per `## Approach` rule 2.
   Reversal: one condition in the span scan.
4. **The question is asked of the cell's text after its surrounding spaces are stripped** — the
   same text `_render_cell` places and `_column_widths` measures. Stripping cannot create or
   destroy a tag or a backtick, so this is a statement about which string is passed, not about the
   answer. Reversal: the argument at one call site.

Assumptions 1 and 2 are cases [src: WI-0004] does not mention. They are recorded rather than
asked, because a different stakeholder would not answer them differently: both are about what an
HTML `br` tag is, not about what the tool is for, which is the routing rule `refine` applied to
the same kind of question at round 2 [src: tracker/items/WI-0004/artifacts/refinement-qa.md].

## Decisions and ADRs

| decision | where it is recorded | how it was reached |
|----------|----------------------|--------------------|
| A cell containing a line break is rendered as if its column were left-aligned; the override is per cell, at render time | [src: ADR-0010] §1 | the stakeholder's answers, which fix the *what*; the placement is derived from them and from [src: ADR-0007] |
| The detection lives in a new module, `mdtab/inline.py`, rather than in `mdtab/table.py` | [src: ADR-0010] §2, option B | decided here, against the documented alternative: `table.py` owns a rule the recognition path uses, and the code-span rule must not become reachable from it |
| What a line break is: the tag pattern, and the code-span rule that excludes one | [src: ADR-0010] §2 | the stakeholder settled which cells count [src: WI-0004/Q-001]; the grammar is derived, deliberately smaller than markdown's |
| The three unconstrained cases — unbalanced backtick, multi-backtick span, a tag both inside and outside | [src: ADR-0010] §3 | routed to `plan` by `refine` [src: WI-0004]; decided as consequences of the span rule rather than as an exception list |
| `</br>`, an attribute containing `>`, and backslash before a backtick | `## Assumptions` 1–3 above | reversible, one file, no criterion turns on them |
| `docs/architecture/overview.md` records the design now, in the future tense, and `implement` puts it in the present tense at step 7 | overview v8 change-log row | the pattern `review-close` recorded on WI-0003 — `plan` has no step for the documents a change invalidates — so the step is written into this plan rather than left to be noticed |

Nothing here supersedes or corrects an existing ADR. [src: ADR-0007] item 1 says the *column's*
alignment is derived once per table from the delimiter row and read nowhere else; that stays true,
and [src: ADR-0010] adds only that a cell may decline the value its column offers. No condition of
[src: ADR-0009] is engaged, because no statement in [src: ADR-0007] becomes false.

## Scaffolding

None. Every file this plan names is either an existing file or a test, fixture or module that an
acceptance criterion depends on, and `python3 -m unittest discover -s tests -t .` already runs
against the project as it stands.

## Risks

1. **The code-span rule is the only genuinely new machinery, and it is the one thing here that can
   be wrong in a way an author would call a bug.** A span mis-found either shifts an ordinary cell
   left or leaves a broken cell where it was, and nothing warns anyone, because the tool says
   nothing about anything [src: EP-001]. Mitigated by step 3, which tests the three edge cases and
   the plain case directly rather than only through a rendered table — the failures are then
   localised to the rule instead of showing up as a padding difference.
2. **A document that mentions `<br>` in a table cell without backticks now shifts left.** This is
   the criterion working as asked [src: WI-0004 AC1], not a defect, but it is a visible change to
   documents nobody edited. The stakeholder chose it with the alternative in front of them
   [src: WI-0004/Q-001]. If it turns out to be unwanted, the reversal is [src: ADR-0010]'s
   part 1 — one condition at one call site.
3. **`grep -rniE '<br' tests/` stops exiting 1 as soon as step 5 lands.** AC5 quotes that command
   as evidence that no existing expectation is about a document this rule reaches, and it is only
   evidence *before* the change. Step 6 records it as such; `verify` should read it as a statement
   about the trunk, not about the branch, and should check AC5 with a diff against the trunk
   instead.
4. **Registering the new fixtures in `ALIGNED` edits `tests/test_fixtures.py`,** a file AC5 wants
   left alone. The edit adds two dict entries and no assertion; none of the twelve tests named in
   AC5 from that file changes. If `verify` reads AC5 as "the file is untouched" rather than "the
   named tests are unmodified", it will report a defect that is not one — so step 6 quotes the
   diff of that file in full, which is small enough to read.
5. **A wide or combining character in the same cell as a break.** Width is display width and this
   item moves padding rather than measuring it [src: ADR-0002], so nothing should change; the
   `align-unicode` and `unicode-mixed` fixtures are unaffected because neither contains a tag. Not
   tested further, deliberately: a test crossing the two would assert the absence of an
   interaction that no line of this change creates.

## Out of scope for this item

- Rendering, wrapping or splitting a multi-line cell across output lines. mdtab changes spacing,
  not content [src: WI-0004].
- Any wider markdown inline grammar. `mdtab/inline.py` learns a `br` tag and a code span because
  [src: WI-0004 AC1] and [src: WI-0004 AC7] turn on them, and learns nothing else — no emphasis,
  no links, no HTML beyond the one tag, and none of CommonMark's further rules about a code span's
  content [src: ADR-0010].
- Measuring a multi-line cell as its longest rendered line. The column's width is still the
  display width of the text as typed, settled during refinement
  [src: tracker/items/WI-0004/artifacts/refinement-qa.md].
- The five caveats and the three gaps the stakeholder declined as work
  [src: EP-001/Q-004; src: EP-001/Q-005]. No item is to be filed for any of them.
