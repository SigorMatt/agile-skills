# Implementation report — WI-0002

Branch `wi/WI-0002`, off `main` at `571cac2`. Two commits: `3647766` (the behaviour and its
unit tests) and `34c0c73` (the ten fixture pairs and their registration).

## What was built

Three changes in `mdtab/table.py`, exactly the three the plan's steps 1–3 describe, and nothing
else in `mdtab/`:

1. `column_alignments(rows) -> list` reads one of `"left"`, `"right"` or `"centre"` per column
   from `rows[1]`, the delimiter row, with the spaces around each marker stripped. A leading `:`
   alone is left, a trailing `:` alone is right, both are centre, neither is left.
2. `_render_cell` gained an `alignment` parameter and distributes its existing
   `padding = width - 2 - display_width(text)` accordingly: all after the text for left (what
   WI-0001 did for every cell), all before it for right, and `padding // 2` before with the rest
   after for centre, so an odd spare column falls on the right.
3. `_render_row` threads a per-column `alignments` list through to `_render_cell`, and `lay_out`
   computes it once — `alignments = column_alignments(rows)` — beside `widths`, from the same
   parsed rows. The delimiter branch ignores it.

`_column_widths`, `_render_delimiter`, `_spaces_omitted` and all four recognition rules are
untouched, which is what makes AC6, AC9 and AC13 regression checks rather than new behaviour. No
file outside `mdtab/table.py` and `tests/` changed. `docs/architecture/overview.md` v3 and
ADR-0007, both written by `plan`, already describe what was built; neither needed an edit.

Ten fixture pairs were added under `tests/fixtures/`, every expected half written by counting
display columns by hand before the code was run.

## Acceptance criteria evidence

The test command for every row below is
`python3 -m unittest discover -s tests -t .`, from the repository root, exit 0, 65 tests, all
passing on branch head `34c0c73`.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — the marker is read from the delimiter cell | `column_alignments` in `mdtab/table.py` | `tests.test_units.ColumnAlignmentTest`: `test_each_of_the_four_markers_names_its_alignment` (`\| :--- \| ---: \| :---: \| --- \|` → `["left", "right", "centre", "left"]`), `test_spaces_around_a_marker_do_not_change_it` (`\|  :---  \| ---:  \|` → `["left", "right"]`), `test_the_body_rows_have_no_say_in_it`, `test_a_delimiter_cell_with_no_dash_is_not_a_delimiter_row_at_all`; fixture `align-markers` |
| AC2 — left column, content first | `_render_cell`'s `else` branch | fixture `align-markers` (its `:---` and `---` columns: `\| a     \|` and `\| dddd  \|`); `tests.test_fixtures.LayoutShapeTest.test_ac12_every_cell_has_exactly_one_space_against_each_pipe`, which asserts no second leading space in the two left columns of `basic-ascii` |
| AC3 — right column, content last | `_render_cell`'s `"right"` branch | `tests.test_units.PaddingPlacementTest.test_ac3_every_cell_of_a_right_column_ends_at_the_same_display_column`, which measures the display column of each cell's last non-space character; fixture `align-markers` (`\|    bb \|`, `\|  ffff \|`) |
| AC4 — centre, odd column on the right | `_render_cell`'s `"centre"` branch | `tests.test_units.PaddingPlacementTest.test_ac4_a_centred_cell_leans_left_when_the_spare_column_is_odd`: AC4's own document gives `\| ab  \|`, and two further documents with three and two spare columns give `\|  ab   \|` and `\|  ab  \|`, which a left-padding renderer would not; fixture `align-centre-odd` |
| AC5 — display columns, not characters | `_render_cell` measures with `display_width` | fixture `align-unicode`, hand-written: `\|   表 \|`, `\|    é \|` (U+00E9), `\|    é \|` (`e` + U+0301) and `\| word \|` all end at the same display column; `PaddingPlacementTest.test_ac3_...` includes `表` |
| AC6 — width does not depend on alignment | `_column_widths` is unchanged (the diff shows no hunk in it) | `tests.test_units.WidthIndependenceTest.test_the_pipes_land_in_the_same_places_under_all_four_markers`: the same four-column table laid out four times, once per marker in one column, with every `\|`'s display column identical across the four |
| AC7 — the guard spaces do not move | the guard spaces are added outside the field, unchanged from WI-0001 | `tests.test_units.PaddingPlacementTest.test_ac7_an_interior_pipe_keeps_a_space_on_each_side_under_every_marker`, over `\|---:\|---:\|`, `\|:---:\|:---:\|` and `\|:---\|---:\|`; and `python3 -m mdtab < tests/fixtures/align-markers.in.md \| sed -n '1p;3,4p' \| grep -n '\|[^ ]'` → no match, exit 1 |
| AC8 — an empty cell in a right or centre column | falls out of `padding == field` in every branch | fixture `align-empty-cell`: `\| a \|   \| c \|` over `\|---\|:-:\|---\|`; `tests.test_fixtures.LayoutShapeTest.test_ac12_an_empty_cell_renders_as_spaces_between_the_pipes` over `empty-cells` |
| AC9 — the delimiter row keeps its markers and its width | `_render_delimiter` is unchanged | fixture `align-markers`: input `\| :--- \| ---: \| :---: \| --- \|` → `\|:------\|------:\|:------:\|-------\|`; `tests.test_fixtures.LayoutShapeTest.test_ac12_the_delimiter_row_keeps_its_colons_and_fills_the_column` and `ContentPreservationTest.test_ac14_no_line_gains_or_loses_a_pipe` now run over the new fixtures too |
| AC10 — first column of a bare table | the field keeps its width when a guard space is dropped | `tests.test_units.PaddingPlacementTest.test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`: `a \| b` / `---:\|---` / `xxxx \| y` → `   a \| b` / `----:\|--` / `xxxx \| y`, both first-column cells ending at display column 3, and `lay_out` of that output returning `None`; fixture `align-bare-first-column`, whose idempotence is asserted by `FixtureRoundTripTest.test_ac6_running_the_tool_on_its_own_output_changes_nothing` |
| AC11 — last column with no trailing pipe | same arithmetic at the other end | `tests.test_units.PaddingPlacementTest.test_ac11_a_right_aligned_last_column_ends_the_line_at_its_content`; fixtures `align-no-trailing-pipe` and `align-leading-pipe-only`; `python3 -m mdtab < tests/fixtures/align-no-trailing-pipe.in.md \| awk '{print length($0)}'` → `11`, `11`, `11` |
| AC12 — alignment inside a prefix | `lay_out` strips the prefix before parsing and re-adds it, unchanged | fixtures `align-blockquote` (`> ` on every line) and `align-list-indent` (two spaces under a list item), both in `ALIGNED`, so every document-level test runs over them |
| AC13 — an unrecognised run is still copied through | the four recognition rules are unchanged | fixture `align-unrecognised` in `UNTOUCHED` — four runs carrying `:` markers (ragged cell counts, mixed outer pipes, ragged prefixes, a table inside a fence), whose `.out.md` is byte-identical to its `.in.md`, asserted by `FixtureRoundTripTest.test_ac4_ac5_documents_with_nothing_to_lay_out_come_back_byte_for_byte` |
| AC14 — WI-0001's criteria still hold, less AC12's padding-position clause | no rule of WI-0001 was changed except that one | all 65 tests pass, including the whole of WI-0001's suite; the eight new `ALIGNED` fixtures are carried by `AlignmentTest` (equal row widths, pipes at one display column), `ContentPreservationTest` and `FixtureRoundTripTest` (idempotence) without a line written for them. The two places that encoded the superseded clause are listed under **Deviations** below |

Mutation check, run twice while writing the tests and not committed: replacing `_render_cell`'s
three branches with the single left-padding line WI-0001 had fails six named tests —
`test_every_fixture_produces_its_expected_output`, `test_ac1_python3_m_mdtab_writes_the_document_and_exits_zero`,
`test_ac3_...`, `test_ac4_...`, `test_ac10_...` and `test_ac11_...`. No new criterion is
demonstrated only by a test that would still pass without the change.

## Deviations from the plan

1. **Two places in WI-0001's shipped suite had to move, and the plan said the suite would run
   unchanged.** The plan's step 5 and its AC14 row both assert "the whole existing suite,
   unchanged". That is false, and it is false for exactly one reason: `basic-ascii`'s delimiter
   row is `|---|:---|---:|`, so its `id` column is right-aligned under AC3.
   - `tests/fixtures/basic-ascii.out.md`: `| 1  |` → `|  1 |`, `| 2  |` → `|  2 |`.
   - `tests/test_fixtures.py`, `test_ac12_every_cell_has_exactly_one_space_against_each_pipe`:
     its `assertFalse(cell[1:-1].startswith(" "))` is literally "the padding is to the right of
     the content". It was **narrowed, not deleted** — the guard-space half is still asserted for
     every column (AC7), and the no-second-space half is still asserted for the two columns AC2
     still governs.

   Both are the single clause WI-0002 AC14 excepts by name and AC2–AC4 supersede. WI-0001's
   `item.md` was not edited, as AC14 requires, and no acceptance criterion of either item was
   changed. This is the one judgement in this execution a reviewer should check.
2. **`align-no-trailing-pipe` became two fixtures.** The plan describes it as "leading pipes but
   no trailing ones", but AC11's own worked document — `a | bbbb` / `---|---:` / `xxxx | y` — has
   neither outer pipe. Rather than choose, both exist: `align-no-trailing-pipe` is AC11's
   document verbatim, and `align-leading-pipe-only` is the plan's description. Ten fixture pairs
   were therefore added, not the nine the plan lists.
3. **`align-list-indent` was added, which the plan does not list.** AC12 asks for two documents —
   a blockquote and "one indented two spaces under a list item" — and the plan's step 4 named only
   the blockquote. The list-indent fixture is the second half of AC12's own check.
4. **`PaddingPlacementTest` gained a fifth test, for AC11.** The plan assigns AC11 to fixtures
   only; asserting it on `lay_out` directly costs three lines and does not depend on a
   hand-written expected output being right.
5. **AC4's unit test asserts three documents, not one.** AC4's own document has a single spare
   column, where a centred cell and a left-padded one are identical, so on its own it fixes the
   tie-break but does not demonstrate centring at all. Two documents with three and two spare
   columns were added beside it. This came out of the mutation check.

Nothing else deviates. The plan's `## Assumptions` were all taken as written: the alignments are
the strings `"left"`, `"right"` and `"centre"`; `column_alignments` is public; and
`align-unrecognised` covers all four rejection routes in one document.

## Gates

Run on branch head `34c0c73`, after the last commit.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, "Ran 65 tests ... OK" |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → "checked 4 item(s), 9 document(s) ... 0 errors, 0 warnings" |
| `every-criterion-has-a-test` | **pass** | the table above names a test function or an exact command for all fourteen; none is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 2 commit(s) on main..wi/WI-0002 name WI-0002" |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main --stat`: `mdtab/table.py`, `tests/test_units.py`, `tests/test_fixtures.py`, twenty new fixture files, `tests/fixtures/basic-ascii.out.md`, and the tracker files this execution wrote. Every hunk traces to a plan step or to a criterion; the deviations above account for the four that trace to a criterion rather than to a step |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, "checked no documents changed since main" (no file under `docs/` changed) |

## What I did not do

- **No document under `docs/` was touched.** `plan` had already written ADR-0007 and taken
  `docs/architecture/overview.md` to v3, and both describe what was built — including the
  one-place-per-rule entry for where a cell's content sits and the section naming the recognition
  property this costs. Nothing in them turned out to be wrong, so nothing needed a revision. That
  is why `claims-are-sourced` reports zero documents checked rather than a clean pass over a
  changed one.
- **The recognition fault AC10 creates was not worked around**, in either of its forms — the bare
  table, and the same case inside a prefix that WI-0002's `## Notes` records for WI-0003's
  refinement. `lay_out`'s four rules come out of this item byte-identical. The unit test for AC10
  asserts, deliberately, that `lay_out` returns `None` for mdtab's own output, and names WI-0003
  in its docstring as the item that will make that assertion false.
- **No diagnostic output of any kind** was added; mdtab still says nothing.
- **The `.pyc` files under `mdtab/__pycache__/`** are untracked build output and were left alone;
  they were already untracked before this item.
