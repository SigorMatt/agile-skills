# Plan — WI-0002 Honour column alignment markers when aligning table cells

## Problem

`mdtab.py` today pads every content cell on the right, whatever its column's delimiter cell says
[src: mdtab.py]. WI-0002 makes the marker decide instead: a left marker keeps the padding on the
right, a right marker moves it all to the left, a centre marker splits it with the odd space going
right, and a column with no marker is unchanged [src: ADR-0005]. It applies to every content cell
of a marked column, the header row included, on the stakeholder's own words
[src: WI-0002/Q-001]. The constraints are inherited and none of them moves: a column's width is
still the display width of its widest content cell [src: ADR-0003], the delimiter row is still
composed from the colons the input had [src: ADR-0004], the one space either side of a cell's text
is untouched [src: WI-0001/Q-003], and no composed line may end in whitespace
[src: EP-001/Q-001]. This is one change in one function, plus the function that tells it which
column is aligned how.

## Approach

Alignment is a property of a **column**, read once from the delimiter row and then applied to
every content cell of that column — the same shape `column_widths` already has [src: mdtab.py].
So the change is two functions, not a rewrite:

1. A new `column_alignments(rows)` reads `rows[1]` — the delimiter row — and returns one value per
   column: `LEFT` when the cell begins with `:` and does not end with one, `RIGHT` when it ends
   with `:` and does not begin with one, `CENTRE` when it does both, and `None` when it does
   neither. `None` is kept distinct from `LEFT` even though the two compose identically today,
   because they are two different facts — one is a marker the author wrote, the other is its
   absence — and ADR-0005 decides them separately.
2. `compose_row` gains the alignment list and places the padding accordingly. It computes
   `pad = width - display_width(cell)` exactly as now, then splits it: `RIGHT` puts all of `pad`
   before the text, `CENTRE` puts `pad // 2` before and the rest after, and `LEFT` and `None` put
   all of it after. Integer division is what makes the odd space fall to the right
   [src: ADR-0005].
3. `emit_block` computes the alignments once per table, beside the widths, and passes them to
   `compose_row`. `compose_delimiter` is not touched: which colons a delimiter cell carries, and
   where they sit, was decided under WI-0001 and is out of scope here [src: WI-0002; ADR-0004].

The signature change is deliberate rather than reading the delimiter row inside `compose_row`:
composing one row is not where a table-wide fact belongs, and passing it in keeps `compose_row` a
pure function of its arguments, which is what makes it testable on its own.

Two things follow that are not obvious from the criteria.

**`markers.expected.md` changes.** That fixture exists already and WI-0001's AC4 test compares the
filter's output against it byte for byte [src: tests/test_mdtab.py]. Its content columns are
currently all left-padded; under this item three of its four columns move. The expected file must
be regenerated and the diff read, not accepted — it is the clearest single artifact showing what
this item does, and it is also the one place where a mistake would be rubber-stamped by a passing
test.

**Test names collide.** WI-0001's coverage test asserts exactly one test method contains `ac<n>_`
for each n [src: tests/test_mdtab.py; src: WI-0001 AC11], and this item's AC10 needs the same tags
[src: WI-0002 AC10]. ADR-0006 settles it: every criterion-covering test is named
`test_<item>_ac<n>_<slug>` and each item's coverage test searches for its own prefix. WI-0001's
eleven methods are renamed and its tag string changed, with no assertion touched.

## Steps

1. **`mdtab.py` — add the alignment constants and `column_alignments(rows)`.** Three module-level
   string constants `LEFT`, `RIGHT`, `CENTRE`, and a function taking the row list `table_or_none`
   returns and giving back one value per column, read from `rows[1]` by the leading and trailing
   colon of each delimiter cell, `None` when there is neither. Afterwards: calling it on the rows
   of `tests/fixtures/markers.md`'s first table returns `[LEFT, CENTRE, RIGHT, None]`.
2. **`mdtab.py` — change `compose_row(cells, widths, alignments, prefix)`.** Keep the existing
   `" " + cell + padding + " "` shape and the existing `pad = width - display_width(cell)`
   computation; split `pad` into a leading and a trailing run by the column's alignment, per
   ADR-0005: `RIGHT` → all leading, `CENTRE` → `pad // 2` leading and the remainder trailing,
   `LEFT` and `None` → all trailing. Afterwards: a centred column of width 3 holding `ab` composes
   as `| ab  |` and holding `Q` as `| Q |`.
3. **`mdtab.py` — pass the alignments through `emit_block`.** Compute them once, next to
   `widths = column_widths(rows)`, and hand them to each `compose_row` call. `compose_delimiter`'s
   call is unchanged. Afterwards: `python3 mdtab.py < tests/fixtures/markers.md` shows the Center
   column's `b` centred and the Right column's `c` against its right-hand space.
4. **`mdtab.py` — correct and extend the module docstring's list of rule documents.** It must name
   ADR-0005 as the document deciding where cell text sits. While rewriting that list, fix the
   filename it gives for ADR-0004: it says `ADR-0004-delimiter-row-keeps-alignment-markers.md` and
   the file is `ADR-0004-delimiter-row-preserves-alignment-markers.md`. Afterwards: every path in
   that docstring resolves to a file that exists. **This correction is called out rather than
   folded in:** it is a defect in a delivered artifact, it is being fixed only because step 4
   rewrites the very lines it lives on, and it changes no behaviour and no criterion. No bug item
   was filed for it, and a reviewer who thinks one was owed should say so.
5. **`tests/test_mdtab.py` — rename WI-0001's eleven criterion tests to the ADR-0006 convention**
   and change its coverage test's tag from `"ac%d_"` to `"wi0001_ac%d_"`. No assertion, fixture or
   docstring changes. Afterwards: `python3 -m unittest discover -s tests -t .` passes with the same
   number of tests as before this step.
6. **`tests/fixtures/` — add the inputs the new criteria need**, and their expected outputs, each
   compared byte for byte:
   - `aligned.md` — one table with a left, a right, a centre and an unmarked column, header and
     several body rows of differing widths, covering AC1 to AC4 in one document.
   - `aligned_empty.md` — a table in which each of the three marked columns has one empty cell,
     and a second table in which every content cell of a `:---`, a `---:` and a `:---:` column is
     empty, for AC5.
   - `aligned_wide.md` — the three marked columns carrying an East Asian wide character, an emoji
     and a letter with a combining accent, for AC6.
   Add every new input to `INPUT_FIXTURES`, which is what AC8's idempotence loop and the
   exit-status loop range over.
7. **`tests/fixtures/markers.expected.md` — regenerate and read the diff.** It is the existing
   fixture WI-0001's AC4 test compares against; three of its four columns move. Afterwards: the
   diff shows content cells moving and the delimiter row byte-identical.
8. **`tests/test_mdtab.py` — add one test per criterion, AC1 to AC9**, named
   `test_wi0002_ac<n>_<slug>` per ADR-0006, plus a coverage test
   `test_wi0002_ac10_each_criterion_has_a_named_test` searching for the `wi0002_ac%d_` tag over 1
   to 9. AC1 to AC4 assert the composed cell against the expected fixture and, for at least one
   cell of each kind, against the formula in the criterion so a reader can see the arithmetic.
   AC3 additionally asserts the two worked examples the criterion names. AC5 to AC8 use the
   fixtures from step 6. AC9's test asserts that `artifacts/verify-report.md` is `verify`'s to
   write, so this one is not a code test — see the mapping table.
9. **Write `artifacts/impl-report.md`** mapping each criterion to the test and the command output
   that demonstrates it, per `implement`'s contract.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — left marker | 1, 2, 3 | `test_wi0002_ac1_...` compares the filter's output on `aligned.md` with `aligned.expected.md` and checks the left-marked column's cells are text-then-padding |
| AC2 — right marker | 1, 2, 3 | `test_wi0002_ac2_...` on the same pair, checking the right-marked column's cells are padding-then-text and that every row's text ends at one offset |
| AC3 — centre marker and the odd remainder | 1, 2, 3 | `test_wi0002_ac3_...` on the same pair, plus the two literal examples the criterion states: width 3 with `ab` → `\| ab  \|`, with `Q` → `\| Q \|` |
| AC4 — no marker | 1, 2, 3 | `test_wi0002_ac4_...` checks the unmarked column of `aligned.expected.md` is byte-identical to what WI-0001's rule produces, and that `ragged.expected.md` is unchanged by this item |
| AC5 — empty cells and zero-width marked columns | 2, 6 | `test_wi0002_ac5_...` on `aligned_empty.md` / `.expected.md`, including the second run over the first run's output |
| AC6 — markers and display width together | 2, 6 | `test_wi0002_ac6_...` on `aligned_wide.md`, asserting equal display width per line and equal column spans per row using `mdtab.display_width` |
| AC7 — markers survive and mean the same | 3, 7 | `test_wi0002_ac7_...` reads the delimiter cells of every table in every input fixture and its output and asserts the leading/trailing colon pair is identical per column; `markers.expected.md`'s delimiter row is byte-identical after step 7 |
| AC8 — idempotence over marked tables | 6 | `test_wi0002_ac8_...` runs the filter twice over each new fixture and each existing one, asserting equality; the new fixtures are in `INPUT_FIXTURES` |
| AC9 — WI-0001's criteria re-read by ID | 5, 7 | not a code test: `verify` writes the verdicts into `artifacts/verify-report.md`. `implement` supplies the evidence it needs — the suite result after step 5's rename, and the `markers.expected.md` diff from step 7 — and states in `impl-report.md` that WI-0001 AC3's text now holds only for an unmarked column |
| AC10 — tests exist and exit status is 0 | 5, 8 | `test_wi0002_ac10_each_criterion_has_a_named_test` finds exactly one `wi0002_ac<n>_` method for n in 1 to 9; the exit-status assertion rides the existing loop over `INPUT_FIXTURES` |

## Assumptions

- **`None` and `LEFT` compose identically, and the code keeps them apart anyway.** Reversing this
  means deleting one branch of a three-way split in `compose_row`; one file, no fixture changes,
  no interface anyone outside the module sees. It is kept because ADR-0005 decides the markerless
  case separately from the left-marked one, and a reader of the code should be able to see that.
- **The alignment list is computed in `emit_block` and passed down, rather than derived inside
  `compose_row`.** Reversing it is a signature change in one file with three call sites, all in
  `mdtab.py` and its tests.
- **`aligned.md` carries all four column kinds in one table rather than four tables.** Reversing
  it is a fixture edit. It is done this way because AC6 and AC5 both require several marked
  columns in one table, so the multi-column case has to exist regardless, and one fixture that
  exercises the interaction is worth more than four that do not.
- **AC9's verdicts are `verify`'s to record, not `implement`'s to assert in a test.** The
  criterion asks for a read of eleven criteria's text, which no assertion can perform. If this is
  wrong the cost is one more test and no design change.

## Decisions and ADRs

- **ADR-0005** — where a marker puts cell text, and that the odd centring remainder goes right.
  Recorded by `answer-questions` from the stakeholder's answer; this plan implements it and
  decides nothing about it. Route: answered from the documents.
- **ADR-0006** — test method names carry the item ID as well as the criterion number. **New, and
  written for this item.** Route: this was a real decision with three options worth naming, and it
  had to be taken before any test was written, because the alternative — discovering it while
  implementing — means either a delivered criterion starts failing or somebody invents a
  convention under time pressure.
- **ADR-0003 and ADR-0004** — unchanged and unchallenged. Column width, the delimiter row's
  composition and the minimum width of a doubly-colonned column are all read from them; nothing in
  this item revisits any of it.
- **No ADR for the internal shape of the change.** `column_alignments` beside `column_widths`, and
  a wider `compose_row`, is the one arrangement that mirrors what is already there; the
  alternatives are recorded under `## Assumptions` where they belong, because each is one file to
  reverse.

## Scaffolding

None. Every file this plan creates is a test fixture or a test, and both are `implement`'s to
write; `tracker/project.yaml` already carries a `test` and a `lint` command that run in this
project.

## Risks

- **Step 7 is where a wrong rule gets frozen.** `markers.expected.md` is regenerated from the
  filter's own output, so if step 2 places the padding on the wrong side the fixture records the
  mistake and the test then passes. The mitigation is in the step: the diff is read against AC3's
  two worked examples, which are literal text in the criterion and were written before any code.
- **WI-0001's AC3 text becomes conditionally true**, and the temptation at review will be to edit
  it. AC9 exists to make the reconciliation a recorded read rather than a document repair; ADR-0005
  is the citation it rests on. If somebody edits WI-0001 AC3, the record of what was verified
  under WI-0001 is destroyed and the ADR-0008 rule is broken.
- **Renaming eleven delivered tests (step 5) is the largest edit in this item and covers no new
  behaviour.** If it goes wrong the failure is loud — the suite stops passing or the coverage test
  stops finding a criterion — but it does put WI-0002 in WI-0001's test file, which `git log
  --grep WI-0001` will not show. ADR-0006 records why.
- **A right-aligned or centred final column is the case that could reintroduce trailing
  whitespace.** It cannot, because the padding is placed before the closing space and pipe
  [src: ADR-0005], and WI-0001's AC3 test already asserts no composed line ends in whitespace over
  every fixture — but the new fixtures must be added to `INPUT_FIXTURES` (step 6) for that
  assertion to reach them. Forgetting that is a silent loss of coverage.
- **Nothing here was measured on a large document**, exactly as WI-0001 recorded. The change adds
  one list of small strings per table and no extra pass over the input.

## Out of scope for this item

- Changing which alignment a column has, and where a marker's colons sit inside its delimiter
  cell. ADR-0004 owns the second and this item does not reopen it.
- Any change to recognition, indentation, fences, passthrough or column width. `table_or_none`,
  `candidate_parts`, `fence_delta` and `column_widths` are read but not modified — except that
  `column_widths` is read closely, because its existing minimum-width rule for a doubly-colonned
  column is what makes AC5's all-empty centred column work.
- Rendering, or any assertion about how a markdown renderer displays the result.
- The escaped-pipe question `docs/product/vision.md` routes to `plan`. It is not raised by any
  criterion of this item and no step touches `split_cells`, so deciding it here would be
  designing past the item.
