# Implementation report — WI-0003

## What was built

One branch in one function, and the tests that pin it down.

`mdtab.py` gains a module-level compiled pattern `_BREAK_TAG` (`<br\s*/?>`, `re.IGNORECASE`) and
a predicate `has_break_tag(text)`, sited between `column_alignments` and `compose_row`
decisions 1 and 4 of [src: ADR-0009]. `compose_row` consults the predicate on each cell's text as the
**first** test of its existing before-padding chain, ahead of RIGHT and CENTRE; when it is true,
`before` is 0, which is the LEFT and no-marker path the function already had
decision 2 of [src: ADR-0009]. Nothing else in the function moves: the one space either side, the
`pad` arithmetic and the `width + 2` cell length are as they were.

`column_alignments` and `emit_block` are untouched, so a column's alignment stays a property of
the delimiter row alone and the exemption cannot become per-column decision 3 of [src: ADR-0009].
A cell containing no break tag reaches exactly the branch it reached before.

Two docstrings were brought up to date: `compose_row`'s names the exception and cites ADR-0008
and ADR-0009 beside the existing ADR-0005 citation, noting ADR-0005 is superseded by ADR-0007;
the module docstring's rule-document list gains ADR-0007, ADR-0008 and ADR-0009 and marks
ADR-0005 superseded.

Under `tests/fixtures/`, nine inputs and seven expected outputs. Each expected file is
byte-identical to the table quoted in its criterion — AC1, AC2, AC3, AC5 and AC6 quote theirs in
`item.md`, AC4's and AC8's are quoted in `plan.md` step 5 — checked by extracting the fenced
blocks from those two documents and comparing the bytes, not by eye. `break_fenced.md` and
`break_malformed.md` have no expected file: their criterion is identity with the input.

In `tests/test_mdtab.py`, eleven criterion tests named `test_wi0003_ac<n>_<slug>`
decision 1 of [src: ADR-0006], in five classes of their own, plus one untagged predicate test.
WI-0003's nine inputs join `INPUT_FIXTURES`, which is what makes WI-0001 AC3, AC9 and AC10 and
WI-0002 AC8 range over tables carrying a break tag.

## Acceptance criteria evidence

Commands below were run from the repository root on the branch head (`1100203`). "byte-compared"
means `assertEqual` on the two files' bytes, not on decoded text.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `has_break_tag` matches all six spellings; each is composed with `before = 0` despite the centre marker, while the header `form` is centred | `test_wi0003_ac1_every_spelling_of_a_break_tag_exempts` — `break_forms.md` byte-compared with `break_forms.expected.md`, plus a per-cell check that each of the six sits at offset 1 within `W = 8`. `python3 -m unittest tests.test_mdtab.BreakTagExemptionTest.test_wi0003_ac1_every_spelling_of_a_break_tag_exempts` → `OK` |
| AC2 | the pattern requires `<`, `br`, optional space, optional `/`, `>`, so none of the five texts matches and each is centred by the existing CENTRE branch | `test_wi0003_ac2_nothing_else_exempts_a_cell` — `break_not.md` byte-compared with `break_not.expected.md`, plus a computed centring check (`pad // 2` before, remainder after) for each of the five |
| AC3 | the predicate is consulted per cell, so an exempt header cell is laid out left under a right marker while its column's other cells keep the marker | `test_wi0003_ac3_markers_header_row_and_per_cell` — `break_markers.md` byte-compared with `break_markers.expected.md`; `\| own<br>er \|`, `\|     alice \|`, `\|        bo \|`, `\|         c \|`, `\|   ok   \|`, `\|  done  \|`, `\| x<br>y \|` each asserted present; plus the narrow-header table below |
| AC4 | the exemption selects the same `before = 0` the no-marker path already used, so an unmarked column's output is unchanged either way | `test_wi0003_ac4_no_marker_is_unaffected_either_way` — `break_no_marker.md` byte-compared with `break_no_marker.expected.md`; `\| a<br>b \|` and `\| plain  \|` have the identical shape |
| AC5 | `pad` is still `width - display_width(cell)` for an exempt cell and the leftover follows the text, so the cell fills `W + 2` like any other | `test_wi0003_ac5_an_exempt_cell_is_padded_to_the_column_width` — `break_padded.md` byte-compared with `break_padded.expected.md`; all five output lines have one distinct `display_width`; every `\|` is at the same display offset on every row; the input asserted ragged so the check is not vacuous |
| AC6 | `column_alignments` is untouched, so a column all of whose content cells are exempt still emits its marker in the delimiter row | `test_wi0003_ac6_a_wholly_exempt_column` — `break_all_exempt.md` byte-compared with `break_all_exempt.expected.md`; column 0's output delimiter cell asserted to end with `:` and not begin with one; the second column's three cells asserted right-placed |
| AC7 | an empty cell's text contains no break tag so the predicate is false for it; `compose_delimiter` never sees the predicate at all | `test_wi0003_ac7_empty_cells_and_the_delimiter_row` — `aligned_empty.md` byte-compared with its expected file; then for each of `break_forms`, `break_not`, `break_markers`, `break_padded`, `break_all_exempt`, every output delimiter cell checked for leading-colon identity, trailing-colon identity, `^:?-+:?$`, no space, and length `W + 2`, with `W` recomputed from the *input*'s content rows rather than by calling `mdtab.column_widths` |
| AC8 | the predicate is applied to a cell of a block `table_or_none` already accepted, so it is unreachable from a fenced or malformed block | `test_wi0003_ac8_indented_fenced_and_malformed` — `break_indented.md` byte-compared with `break_indented.expected.md` and every pipe line asserted to start `   \|`; `break_fenced.md` and `break_malformed.md` each asserted byte-identical to their own input, exit status 0 |
| AC9 | an exempt cell's output text is its input text with the same surrounding shape, so a second pass measures the same widths | `test_wi0003_ac9_idempotence` — each of the nine inputs filtered once, byte-compared with its expected file where there is one, then re-filtered and asserted byte-identical, exit status 0 |
| AC10 | WI-0003's nine inputs are in `INPUT_FIXTURES`, so WI-0001 AC3, AC9, AC10 and WI-0002 AC8 loop over them; three further prior criteria get inline covering cases | `test_wi0003_ac10_prior_criteria_meet_a_break_tag` — see the map below. The twenty-one per-ID **verdicts** are `verify`'s to write into `verify-report.md`; this test supplies only the covering half |
| AC11 | eleven methods named `test_wi0003_ac<n>_<slug>`, one per criterion, each quoting its criterion in its docstring | `test_wi0003_ac11_each_criterion_has_a_named_test` — exactly one discovered method matches `wi0003_ac<n>_` for each n in 1..11 and its docstring contains `AC<n> `; then each of the nine inputs run twice with exit status 0. Whole suite: `python3 -m unittest discover -s tests -t .` → `Ran 37 tests ... OK`, exit 0 |

### The covering map AC10 asks for

Which prior criterion meets a break tag, and where. `verify` writes the verdicts; this is what it
has to read them against.

| prior criterion | where it now meets a break tag |
|-----------------|-------------------------------|
| WI-0001 AC1 (equal display width) | `test_wi0003_ac5_...` asserts one distinct width over `break_padded`'s output; `test_wi0003_ac10_...` asserts it again on a wide-character table whose right-marked column holds an exempt cell |
| WI-0001 AC2 (equal column offsets) | same two tests — offsets compared row against row on `break_padded`'s output and on the wide-character table |
| WI-0001 AC3 (one space either side, no trailing whitespace) | `test_wi0001_ac3_...` loops over `INPUT_FIXTURES`, which now contains all nine WI-0003 inputs |
| WI-0001 AC4 (delimiter fills `W + 2`) | `test_wi0003_ac7_...`, over five break-tag tables |
| WI-0001 AC5 (indent restored byte for byte) | `test_wi0003_ac8_...`, over `break_indented.md` |
| WI-0001 AC6 (no table → byte-identical) | `test_wi0003_ac10_...`, inline: prose containing `<br>` and `<br/>` and no table, asserted byte-identical |
| WI-0001 AC7 (fenced pipe lines left alone) | `test_wi0003_ac8_...`, over `break_fenced.md` |
| WI-0001 AC8 (malformed block copied whole) | `test_wi0003_ac8_...`, over `break_malformed.md` |
| WI-0001 AC9 (idempotence) | `test_wi0001_ac9_...` over the extended `INPUT_FIXTURES`, and `test_wi0003_ac9_...` |
| WI-0001 AC10 (exit status 0) | `test_wi0001_ac10_...` over the extended `INPUT_FIXTURES`, and `test_wi0003_ac11_...` |
| WI-0001 AC11 (each criterion has a named test) | **structural, and does not intersect content.** It is a claim about the suite's method names, and `test_wi0003_ac10_...` asserts all eleven `wi0001_ac<n>_` tags still resolve after this item's additions |
| WI-0002 AC1 (left marker pads right) | `test_wi0003_ac3_...` — `break_markers`' left-marked column, in a table carrying two break tags, is unchanged |
| WI-0002 AC2 (right marker pads left) | `test_wi0003_ac3_...` — the right-marked column holds an exempt header and three marker-placed body cells; and `test_wi0003_ac6_...` |
| WI-0002 AC3 (centre marker, odd space right) | `test_wi0003_ac2_...` (five centred cells in a table of break-tag lookalikes) and `test_wi0003_ac5_...` (`ok` with an odd remainder of 19 in a table whose widest cell is exempt) |
| WI-0002 AC4 (no marker unchanged) | `test_wi0003_ac4_...` |
| WI-0002 AC5 (empty and zero-width marked cells) | `test_wi0003_ac7_...` re-runs `aligned_empty`; `test_wi0003_ac10_...` adds an inline centre-marked table with an empty cell **and** an exempt cell, byte-compared |
| WI-0002 AC6 (markers and display width together) | `test_wi0003_ac10_...`, inline: a right-marked column of CJK cells one of which is exempt, checked for equal widths and offsets and for both placements |
| WI-0002 AC7 (markers survive and mean the same) | `test_wi0003_ac7_...`'s colon-for-colon identity over five outputs, and `test_wi0003_ac6_...` on a wholly exempt column |
| WI-0002 AC8 (idempotence over marked tables) | `test_wi0002_ac8_...` loops `WI0002_INPUTS + INPUT_FIXTURES`, which now includes the nine |
| WI-0002 AC9 (WI-0001's criteria meet marked columns) | **structural**, like WI-0001 AC11; `test_wi0003_ac10_...` asserts every `wi0001_ac<n>_` tag still resolves |
| WI-0002 AC10 (each criterion has a named test) | **structural**; `test_wi0003_ac10_...` asserts every `wi0002_ac<n>_` tag still resolves, and ADR-0006's per-item tag is why adding `wi0003_ac1_` did not break it |

Three criteria are marked structural above. They are claims about the suite rather than about the
filter's output, so "intersecting a break tag" has no meaning for them; what could break them is a
later item's test names, and that is what is asserted instead. `verify` may take that as the
covering case or waive those three by ID — the criterion allows either, and the report must say
which.

## Deviations from the plan

1. **AC3's test carries one assertion the plan did not list.** Every exempt cell in AC3's own
   quoted table is its column's widest — `own<br>er` is 9 in a column of width 9, `x<br>y` is 6 in
   a column of width 6 — so `W - w` is zero for both and that table is *equally* the output of a
   filter with no exemption at all. Deleting the `compose_row` branch and re-running the suite
   confirmed it: AC1, AC6 and AC9 failed and AC3 passed. AC3's stated claim is that the exemption
   reaches a header cell under a right marker, so the test now also runs a second, inline table in
   which the exempt header is *narrower* than its column
   (`| id | h<br>x |` over `| 1 | abcdefgh |`), where the exemption is observable. With that
   assertion, deleting the branch fails AC1, AC3, AC6 and AC9. No criterion text was changed and
   no expected file was changed; the byte comparison the criterion specifies is still there and
   still first.
2. **Nothing else.** Steps 1 to 7 were executed as written, in order, and the interfaces are the
   two the plan specified with the signatures it specified.

Not a deviation, but worth stating: AC5's and AC8's exempt cells are also their columns' widest,
so those two criteria are likewise insensitive to the exemption on their own. They are left as
written — they are the stakeholder-facing statements of padding and of indent/passthrough, and
AC1, AC3 and AC6 are what discriminate. `verify` should not read a green AC5 as evidence that the
exemption exists.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → `Ran 37 tests in 7.883s / OK`, exit 0, on `1100203` |
| `lint-clean` | pass | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → exit 0 |
| `workspace-valid` | pass | `validate-workspace .` → `checked 4 item(s), 11 document(s) / 0 errors, 0 warnings`, exit 0 |
| `every-criterion-has-a-test` | pass | the table above names a test method for each of AC1 to AC11; `test_wi0003_ac11_...` enforces one-per-criterion mechanically |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0003 wi/WI-0003` → `all 2 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → `claim window: 0 path(s) differ from main (fbf9fce) under docs; checked 12 consumed human answer(s); 0 errors`, exit 0. This execution edited no file under `docs/` |
| `claims-are-sourced` | pass | `lint-claims --changed-since main` → `0 document(s) in 0 path(s) differ ...; citations: every markdown file in the workspace; 0 errors`, exit 0 |
| `no-unplanned-scope` (advisory) | pass | `git diff main..HEAD --stat`: `mdtab.py` (steps 1 to 4), `tests/test_mdtab.py` (step 6 and the `INPUT_FIXTURES` extension AC10 requires), sixteen new files under `tests/fixtures/` (step 5). Every hunk traces to a plan step or to AC3 and AC10; the one addition beyond the plan's list is deviation 1 above |

## What I did not do

- **I did not touch `docs/`.** D12's question — are the claims about the behaviour I changed still
  true? — was asked and answered no-change-needed. `docs/architecture/overview.md` v4 already
  describes the exemption and names ADR-0007, ADR-0008 and ADR-0009 in its rule-document list;
  `docs/product/vision.md` v7 already carries the stakeholder's round-2 absolute verbatim with the
  paragraph recording that its author narrowed it [src: EP-001/Q-005]. There is no sentence in
  `docs/` that this execution made false, and therefore no sentence of theirs to repair or to ask
  about.
- **I did not settle WI-0001's escaped-pipe question**, and nothing here needed it. An exempt cell
  containing `\|` is measured and re-emitted exactly as any other cell is: `split_cells` keeps the
  backslash in the cell text and `display_width` counts it, unchanged by this item. The item and
  the plan both leave it deliberately unconstrained.
- **I did not write the twenty-one per-ID verdicts AC10 requires.** They belong in
  `artifacts/verify-report.md` and are `verify`'s to reach by reading each criterion's own text.
  What is here is the covering map above and the executable cases behind it.
- **I did not add a fixture for the wide-character or empty-cell covering cases.** They are built
  inline in `test_wi0003_ac10_...` as byte literals, so that the fixture directory contains exactly
  the nine inputs plan step 5 lists and nothing a reader has to reconcile against it.
