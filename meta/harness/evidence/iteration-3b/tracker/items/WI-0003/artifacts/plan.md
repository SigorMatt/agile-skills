# Plan — WI-0003 Leave a cell containing a line break at the left of its column

## Problem

The filter places every content cell of a marked column by that column's alignment marker
[src: ADR-0007]. The stakeholder asked for one exception: a cell they have put a line break inside
should sit at the left of its column whatever the marker says, because the marker was meant for
ordinary one-line text [src: EP-001/Q-004; src: EP-001/Q-005]. They then said which cells those
are — any cell whose text contains an HTML break tag in any spelling, and *not* a cell merely
ending in a backslash — and that such a cell is still padded out to the column's width so the
table's closing pipes keep lining up [src: WI-0003/Q-001; src: WI-0003/Q-002]. Both are recorded as
ADR-0008.

What changes is one branch in one function. The constraints are that the exemption is **per cell**
— one exempt cell must not move any other cell of its column [src: ADR-0008] — that nothing about
recognition, column width, the delimiter row or the two spaces either side of a cell's text moves
[src: ADR-0007; src: ADR-0004], and that every criterion WI-0001 and WI-0002 already deliver keeps
holding except the three whose *"every content cell of that column"* this narrows
[src: WI-0003 AC10].

## Approach

`compose_row` is already the one place that decides how much of a cell's leftover padding goes
before its text [src: mdtab.py:244]. The exemption is one more branch there, tested first, ahead of
the RIGHT and CENTRE branches, and it selects the `before = 0` behaviour the function already has
for LEFT and for no marker. The alignment list stays a property of the delimiter row and neither
`column_alignments` nor `emit_block` changes [src: mdtab.py:220; src: mdtab.py:287].

That siting is the design decision this item forces, and ADR-0009 records it with the two
alternatives — a per-cell alignment matrix built in `emit_block`, and the smaller, wrong shortcut
of nulling a whole column's alignment when any of its cells carries a tag [src: ADR-0009].

The interfaces this adds, and no more:

```python
_BREAK_TAG = re.compile(r"<br\s*/?>", re.IGNORECASE)

def has_break_tag(text):
    """True when *text* contains an HTML line-break tag in any spelling."""
```

`has_break_tag` takes a cell's text as `split_cells` produced it — outer pipes gone, surrounding
whitespace stripped [src: mdtab.py:143] — and returns a bool. It is not given a line, a row or a
column. The implementation of the predicate body and of the branch is the developer's.

## Steps

1. **Add the pattern and the predicate to `mdtab.py`**, immediately after `column_alignments` and
   before `compose_row`, so that a reader meets it between "what the column says" and "where the
   text goes". `_BREAK_TAG` is `re.compile(r"<br\s*/?>", re.IGNORECASE)`; `has_break_tag(text)`
   returns whether the pattern is found anywhere in `text`. Its docstring cites ADR-0008 decision 1
   for the shape and ADR-0009 decision 1 for why it is compiled at module level.
   *Afterwards:* `has_break_tag` is true for `a<br>b`, `a<br/>b`, `a<br />b`, `a<BR>b`, `a<Br />b`
   and `a<br >b`, and false for `freeze\`, `C:\dir\`, `<b>bold</b>`, `<break>`, `brr` and `""`.

2. **Add the exemption branch to `compose_row`** in `mdtab.py`, as the **first** test of the
   existing chain that computes `before`, ahead of `alignment == RIGHT`. When
   `has_break_tag(cell)`, `before` is 0. Nothing else in the function changes: the one space either
   side, the `pad` arithmetic and the `width + 2` cell length are untouched.
   *Afterwards:* a cell containing a break tag is written as one space, the text, `W - w` spaces,
   one space, in a column with any marker or none; a cell containing none reaches exactly the
   branch it reached before.

3. **Update `compose_row`'s docstring** in `mdtab.py` to name the exception and cite ADR-0008 and
   ADR-0009 beside the existing ADR-0005 citation — and note that ADR-0005 is superseded by
   ADR-0007, which is the current statement of the marker rules the exception excepts.
   *Afterwards:* a reader of the function reaches the ADR that decided the rule in one hop.

4. **Update the module docstring's rule-document list** in `mdtab.py` to add ADR-0007 (the current
   marker decision, superseding ADR-0005), ADR-0008 (which cells are exempt and how they are
   padded) and ADR-0009 (where the exemption is applied).
   *Afterwards:* the list at the top of the file names every ADR the module implements.

5. **Add the fixture pairs** under `tests/fixtures/`, each an untidied input and its byte-exact
   expected output, the expected outputs being the ones quoted in the criteria:
   - `break_forms.md` / `break_forms.expected.md` — the six spellings, centre-marked (AC1)
   - `break_not.md` / `break_not.expected.md` — the five non-exempting texts, centre-marked (AC2)
   - `break_markers.md` / `break_markers.expected.md` — left / right / centre, a tag in the
     right-marked column's **header** and in one centre-marked body cell (AC3)
   - `break_no_marker.md` / `break_no_marker.expected.md` — a colon-free delimiter row, one cell
     with a tag and one without (AC4). Expected:
     ```
     | note   | n  |
     |--------|----|
     | a<br>b | 1  |
     | plain  | 22 |
     ```
   - `break_padded.md` / `break_padded.expected.md` — the Task/Notes table whose widest cell is the
     exempt one (AC5)
   - `break_all_exempt.md` / `break_all_exempt.expected.md` — two right-marked columns, the first
     entirely exempt (AC6)
   - `break_indented.md` / `break_indented.expected.md` — indented by three spaces (AC8). Expected:
     ```
        | step |  detail  |
        |:----:|:--------:|
        | one  | do<br>it |
        | two  |    ok    |
     ```
   - `break_fenced.md` — a fenced code block whose lines look like table rows containing `<br>`;
     no expected file, because the assertion is identity with the input (AC8)
   - `break_malformed.md` — a block whose body row has a different number of cells from its header
     and contains `<br>`; identity with the input (AC8)
   *Afterwards:* each expected file is byte-identical to the table quoted in its criterion, and the
   two identity fixtures have no expected file by design.

6. **Add one test method per criterion** to `tests/test_mdtab.py`, named
   `test_wi0003_ac<n>_<slug>` under ADR-0006's convention, in a class of their own beside
   WI-0002's:
   - AC1 `test_wi0003_ac1_every_spelling_of_a_break_tag_exempts` — run the filter on
     `break_forms.md`, compare with the expected file byte for byte.
   - AC2 `test_wi0003_ac2_nothing_else_exempts_a_cell` — same over `break_not.md`; this fixture's
     expected output is also what the filter produces **today**, which is the point.
   - AC3 `test_wi0003_ac3_markers_header_row_and_per_cell` — same over `break_markers.md`, and
     additionally assert on that output that the right-marked column's three non-exempt cells are
     right-placed and the centre-marked column's two non-exempt cells are centred, so the test
     fails against ADR-0009's refused option C rather than merely against no change at all.
   - AC4 `test_wi0003_ac4_no_marker_is_unaffected_either_way` — same over `break_no_marker.md`.
   - AC5 `test_wi0003_ac5_an_exempt_cell_is_padded_to_the_column_width` — same over
     `break_padded.md`, and additionally assert every line of that output has the same display
     width, using `mdtab.display_width` [src: mdtab.py:65].
   - AC6 `test_wi0003_ac6_a_wholly_exempt_column` — same over `break_all_exempt.md`.
   - AC7 `test_wi0003_ac7_empty_cells_and_the_delimiter_row` — assert the existing
     `aligned_empty.md` pair still holds, and assert over the outputs of AC1, AC2, AC3, AC5 and
     AC6 that each delimiter cell begins with `:` exactly when its input's did, ends with `:`
     exactly when its input's did, is hyphens between, and is `W + 2` characters long.
   - AC8 `test_wi0003_ac8_indented_fenced_and_malformed` — the indented pair by comparison, and
     `break_fenced.md` and `break_malformed.md` by identity with their own bytes.
   - AC9 `test_wi0003_ac9_idempotence` — feed each expected output of AC1 to AC8 back through the
     filter and assert the result is byte-identical.
   - AC10 `test_wi0003_ac10_prior_criteria_meet_a_break_tag` — the covering cases for the prior
     criteria that no existing test crosses with a break tag. The *verdicts* on WI-0001 AC1–AC11
     and WI-0002 AC1–AC10 are `verify`'s to write into `artifacts/verify-report.md`; this test
     supplies the executable half AC10 asks for, so that where a criterion has no covering case
     `verify` can add one or waive it by ID rather than discovering there is nothing to read.
   - AC11 `test_wi0003_ac11_each_criterion_has_a_named_test` — search the module for the tag
     `wi0003_ac<n>_` for `n` in 1..11 and require exactly one match each, mirroring
     `test_wi0002_ac10_each_criterion_has_a_named_test` [src: ADR-0006].
   *Afterwards:* `python3 -m unittest discover -s tests -t .` exits 0 with every WI-0001, WI-0002
   and WI-0003 test passing.

7. **Run the declared gates on the branch head**: `python3 -m unittest discover -s tests -t .` and
   `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .`, both from `tracker/project.yaml`, plus
   `.claude/agile-skills/scripts/lint-claims --uncommitted` for the docstring citations added in
   steps 3 and 4.
   *Afterwards:* all three exit 0 on the final state of the code, not on an earlier one.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 1, 2, 5 | `test_wi0003_ac1_every_spelling_of_a_break_tag_exempts` — `break_forms.md` output byte-compared with `break_forms.expected.md`, which is AC1's quoted table |
| AC2 | 1, 5 | `test_wi0003_ac2_nothing_else_exempts_a_cell` — `break_not.md` output byte-compared with `break_not.expected.md`, which is AC2's quoted table and is also today's output |
| AC3 | 2, 5 | `test_wi0003_ac3_markers_header_row_and_per_cell` — byte comparison against AC3's quoted table, plus per-cell assertions on the three right-placed and two centred neighbours |
| AC4 | 2, 5 | `test_wi0003_ac4_no_marker_is_unaffected_either_way` — byte comparison against the table quoted in step 5 |
| AC5 | 2, 5 | `test_wi0003_ac5_an_exempt_cell_is_padded_to_the_column_width` — byte comparison against AC5's quoted table, plus equal `display_width` across every output line |
| AC6 | 2, 5 | `test_wi0003_ac6_a_wholly_exempt_column` — byte comparison against AC6's quoted table |
| AC7 | 2 (unchanged behaviour), 6 | `test_wi0003_ac7_empty_cells_and_the_delimiter_row` — the `aligned_empty` pair, plus the colon-for-colon and `W + 2` assertions over five outputs |
| AC8 | 2, 5 | `test_wi0003_ac8_indented_fenced_and_malformed` — indented pair by comparison; `break_fenced.md` and `break_malformed.md` by identity |
| AC9 | 2, 6 | `test_wi0003_ac9_idempotence` — each AC1–AC8 expected output fed back through the filter, byte-identical |
| AC10 | 6 | `test_wi0003_ac10_prior_criteria_meet_a_break_tag` supplies the covering cases; the 21 per-ID verdicts and the three required statements are written by `verify` into `artifacts/verify-report.md` |
| AC11 | 6 | `test_wi0003_ac11_each_criterion_has_a_named_test` — exactly one method matching `wi0003_ac<n>_` for n in 1..11; the suite exits 0 under `commands.test` |

## Assumptions

- **The six spellings in AC1 and the five non-exempting texts in AC2 are an adequate sample of
  ADR-0008 decision 1's shape.** The rule is a pattern, not a list, and a test can only ever
  exercise finitely many strings. Reversing this costs one row per fixture and one line per
  expected file: the fixtures are plain text and nothing else depends on their contents. It is
  cheap because no interface and no other criterion refers to them.
- **`re.IGNORECASE` over the ASCII letters `b` and `r` is what "any letter case" means**
  [src: ADR-0008]. The Turkish dotless-i class of Unicode case surprises does not arise for these
  two letters. Reversing this is replacing the flag with an explicit character class in one line.
- **No performance requirement exists on this filter**, so compiling the pattern once is a
  preference recorded in ADR-0009 decision 4 rather than a measured need. Nothing in the record
  states a throughput or latency target [src: EP-001; src: WI-0003]. Reversing it is one line, and
  would change no output.

## Decisions and ADRs

| decision | where it came from | recorded in |
|----------|--------------------|-------------|
| Which cells are exempt, and that an exempt cell is still padded | the stakeholder, `WI-0003/Q-001` and `Q-002` | ADR-0008 (written by `answer-questions` before this execution) |
| The exemption is applied per cell inside `compose_row`; the alignment list and `emit_block` are untouched; the per-column shortcut is refused | decided here, from the documents — ADR-0008 decision 6 and `EP-001/Q-005` rule out per-column | **ADR-0009**, new |
| Test method naming, and the per-item coverage tag `wi0003_ac<n>_` | documented — ADR-0006 decisions 1 and 2 | ADR-0006, cited not re-decided |
| The delimiter row keeps its colons and is never exempt | documented — ADR-0004 decision 1, ADR-0007 decision 6 | cited, not re-decided |
| Column width, display width, the two surrounding spaces | documented — ADR-0003 decisions 7 and 9, ADR-0008 decision 5 | cited, not re-decided |
| The three assumptions above | assumed, reversibly | `## Assumptions`, this file |

Nothing was asked of the human by this execution, and nothing needed to be: the two decisions that
depended on their intent were asked and answered in refinement, and every remaining choice follows
from a document or is a reversible assumption. No ADR written here reconciles two of their
statements — the one contradiction in this area was put to them as `EP-001/Q-005` and settled by
them [src: ADR-0007].

## Scaffolding

None. This execution created no file outside `tracker/` and `docs/`. `tests/` already exists with
`__init__.py` and `test_mdtab.py`, and `commands.test` already runs against it.

## Risks

- **The per-column shortcut is smaller than the per-cell branch and would pass a weak test.** If a
  developer sets a column's alignment to `None` when any cell carries a tag, AC1, AC2, AC5 and AC6
  would all still pass — each has at most one marked column whose behaviour is dominated by its
  exempt cells. AC3 is the criterion that catches it, which is why step 6 requires its neighbour
  assertions explicitly rather than trusting the byte comparison alone [src: ADR-0009].
- **A pattern that is too loose exempts cells the stakeholder wanted placed.** `<br` without the
  closing `>`, or a pattern anchored only on `br`, would exempt `<break>` and `brr`. AC2 exists to
  fail in that case, and its fixture is the one whose expected output equals today's output, so a
  regression there is visible as a change in behaviour that was supposed to be unchanged.
- **An exempt cell that also contains an escaped pipe is not constrained by this item**, on
  purpose: how `\|` is measured and re-emitted is WI-0001's open design question and is still
  unsettled [src: WI-0001; src: docs/product/vision.md]. Today `split_cells` keeps the backslash in
  the cell text [src: mdtab.py:143] and `display_width` counts it [src: mdtab.py:65], so whatever
  is decided there will apply to an exempt cell exactly as it applies to any other — the exemption
  moves where a cell's text sits, never what its text is. If that question is settled while this
  item is in flight, nothing in this plan needs to change; if a developer finds themselves needing
  to decide it in order to finish, that is a question for `answer-questions`, not a decision to
  take inside step 2.
- **`verify` cannot complete AC10 from the suite alone.** AC10 asks for 21 per-ID verdicts reached
  by reading each prior criterion's *text*; step 6 gives it the executable half only. If the
  verify report records "the suite is green" in place of those verdicts, AC10 is not met — this is
  the failure F-065 records and the criterion is written to prevent it.

## Out of scope for this item

- **Settling WI-0001's escaped-pipe question.** It is another item's open design question; deciding
  it here would hide the decision inside a plan for something else.
- **Any other line-break convention.** A trailing backslash was put to the stakeholder and declined
  [src: WI-0003/Q-001]; widening the pattern later is a new decision, not a defect in this one.
- **Rendering, wrapping or splitting an exempt cell.** The filter emits the cell text exactly as it
  arrived [src: WI-0003].
- **Changing recognition, column width, the delimiter row, or the two spaces either side of a
  cell's text.** Steps 1 to 4 touch none of `candidate_parts`, `split_cells`, `table_or_none`,
  `column_widths`, `column_alignments`, `compose_delimiter` or `emit_block`
  [src: mdtab.py:124; src: mdtab.py:143; src: mdtab.py:168; src: mdtab.py:190; src: mdtab.py:220;
  src: mdtab.py:270; src: mdtab.py:287].
- **Refactoring `compose_row` into option B's per-row alignment lists.** ADR-0009 records it as a
  behaviour-preserving refactor available later; doing it now would be designing past the item.
