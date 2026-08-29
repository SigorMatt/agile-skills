# Plan — WI-0002 Honour the alignment markers in a table's delimiter row

## Problem

`mdtab` lays out every table it recognises with each cell's content flush left in its field and
the padding after it. WI-0002 makes the padding follow the `:` markers the author wrote in the
delimiter row: content flush right for `---:`, centred for `:---:`, unchanged for `:---` and
`---`. Nothing else about a table may change — not its width, not its punctuation, not its
markers — and everything mdtab does not recognise must still come back byte-for-byte. The two
places where this is not merely a swap are the ends of a row that has no outer pipe there: the
stakeholder decided both, in favour of honouring the marker anyway (`WI-0002/Q-002`), and
accepted that mdtab will then emit a bare table it does not recognise until WI-0003 fixes that.

## Approach

One new per-column value, computed where the widths already are, and one changed renderer.

- **Alignment is read once per table**, from the delimiter row, by a new public function
  `column_alignments(rows) -> list[str]` in `mdtab/table.py`, returning `"left"`, `"right"` or
  `"centre"` for each column. It is called from `lay_out` beside `_column_widths`, from the same
  parsed `rows`, so the delimiter row is read for its markers in exactly one place. Public rather
  than private because `tests/test_units.py` drives the other rules that way — `row_cells`,
  `is_delimiter_row`, `has_trailing_pipe` — and marker reading is the same kind of rule.
- **The field is unchanged and so are the widths.** `_render_cell` already computes
  `padding = width - 2 - display_width(text)`; that quantity is the spare space and the change is
  only where it goes: after the text (left), before it (right), or `padding // 2` before and
  `padding - padding // 2` after (centre, the extra column on the right per `WI-0002/Q-001`).
  `_column_widths` is not touched at all, which is what keeps AC6 true and leaves the two
  idempotence rules the overview names where they are.
- **The guard spaces stay outside.** `_render_cell` keeps adding them exactly as it does now,
  including dropping the one against a missing outer pipe. Because the field keeps its width, a
  right-aligned first column in a bare table puts its padding at the start of the line (AC10) and
  a right-aligned last column in a table with no trailing pipe ends the line at its content
  (AC11). Both fall out of the arithmetic; neither is a special case in the code.
- **The delimiter row is untouched by this change.** `_render_delimiter` already fills the field
  with `-` and keeps the `:` at the ends the input had, so AC9 is a regression check rather than
  new behaviour.

Recorded as ADR-0007, with the options the stakeholder was shown and the recognition property
this costs.

## Steps

1. **`mdtab/table.py` — read the markers.** Add `column_alignments(rows: list) -> list[str]`,
   returning one of `"left"`, `"right"`, `"centre"` per column, derived from `rows[1][column]`
   stripped of spaces: a leading `:` alone → `"left"`, a trailing `:` alone → `"right"`, both →
   `"centre"`, neither → `"left"`. Afterwards,
   calling it on the parsed rows of a table whose delimiter row is `| :--- | ---: | :---: | --- |`
   returns `["left", "right", "centre", "left"]`.
2. **`mdtab/table.py` — place the content.** Give `_render_cell` an `alignment` parameter and
   distribute its existing `padding` accordingly: all after for `"left"` (today's behaviour), all
   before for `"right"`, `padding // 2` before and the rest after for `"centre"`. Afterwards,
   `_render_cell("ab", 5, "centre", False, False)` is `" ab  "`.
3. **`mdtab/table.py` — thread it through.** Give `_render_row` an `alignments` parameter and
   pass each column's value to `_render_cell`; the delimiter branch ignores it. In `lay_out`,
   compute `alignments = column_alignments(rows)` beside `widths = _column_widths(...)` and pass
   it to both `_render_row` calls. Afterwards, `python3 -m mdtab` on a table with `---:` in one
   column right-aligns that column and leaves the others as they are today.
4. **`tests/fixtures/` — the documents.** Add these pairs, `.in.md` and `.out.md`, the expected
   half written by hand rather than by running the code:
   - `align-markers` — one table with leading and trailing pipes and four columns, one per marker
     (`:---`, `---:`, `:---:`, `---`), cells of differing width in each (AC1, AC2, AC3, AC9).
   - `align-centre-odd` — a centred column whose field is three columns wide holding `ab`, so the
     spare space is odd; expected `| ab  |` (AC4).
   - `align-unicode` — a right-aligned column holding `表`, `é` (U+00E9), `e`+U+0301 and an ASCII
     word (AC5).
   - `align-empty-cell` — a `:---:` column whose header and body cells are all empty, beside a
     normal column (AC8).
   - `align-bare-first-column` — no leading or trailing pipes, first column `---:`; the expected
     output carries leading spaces on the header and body rows and none on the delimiter row
     (AC10).
   - `align-no-trailing-pipe` — leading pipes but no trailing ones, last column `---:`; the
     expected output's lines end at the content (AC11).
   - `align-blockquote` — the `align-markers` table with `> ` on every line (AC12).
   - `align-unrecognised` — one document holding four runs that all carry `:` markers and none of
     which is recognised: rows disagreeing about cell count, rows disagreeing about outer-pipe
     style, lines disagreeing about prefix, and a table inside a fence. `.out.md` is byte-for-byte
     identical to `.in.md` (AC13).
5. **`tests/test_fixtures.py` — register them.** Add the eight names to `ALIGNED` with their line
   ranges, except `align-unrecognised`, which goes in `UNTOUCHED`. Afterwards every existing
   document-level test — equal row widths, pipes at one column, idempotence, content preserved,
   no pipe gained or lost — runs over the new fixtures without another line being written, which
   is most of AC14's evidence. Two places in that suite do have to move, which this plan
   did not foresee: `tests/fixtures/basic-ascii.out.md` and one assertion in
   `test_ac12_every_cell_has_exactly_one_space_against_each_pipe` both encode the
   padding-position clause AC14 excepts, because `basic-ascii`'s `id` column is marked
   `---:`. Nothing else in that suite changes. Recorded after the fact, through
   `WI-0002/Q-003`, which amended AC14's checking clause to say so.
6. **`tests/test_units.py` — the rules.** Add a `ColumnAlignmentTest` covering `column_alignments`
   on all four markers, on markers written with surrounding spaces (`|  :---  | ---:  |`), and on
   a run whose delimiter cell has no `-` (`| : | --- |`), which `is_delimiter_row` already rejects
   so `lay_out` returns `None` (AC1). Add a `PaddingPlacementTest` driving `lay_out` directly for:
   the odd centred remainder (AC4), a right-aligned column's cells all ending at one display
   column (AC3), the guard space after every interior `|` in a right-aligned and a centred table
   (AC7), and a right-aligned bare first column producing leading spaces whose output `lay_out`
   then declines to recognise — asserted as the current, deliberate consequence with WI-0003
   named in the test's docstring (AC10).
7. **Widths do not move (AC6).** Add one test that lays out the same four-column table four times,
   once per marker in the same column, and asserts the display column of every `|` is identical
   across the four outputs.
8. **Run the gates.** `python3 -m unittest discover -s tests -t .` and
   `python3 -W error -m compileall -q mdtab tests`, both from the repository root, both exit 0.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the marker is read from the delimiter cell | 1 | `ColumnAlignmentTest` (step 6) on all four markers, on spaced markers, and on a delimiter cell with no dash in it; fixture `align-markers` |
| AC2 — left column | 2, 3 | fixture `align-markers` (its `:---` and `---` columns); existing pipe-column test over the new fixtures |
| AC3 — right column | 2, 3 | fixture `align-markers`; `PaddingPlacementTest`'s "cells end at one column" assertion (step 6) |
| AC4 — centre column, extra space on the right | 2 | fixture `align-centre-odd` (`\| ab  \|`); `PaddingPlacementTest` odd-remainder assertion (step 6) |
| AC5 — display columns, not characters | 2 | fixture `align-unicode`, whose expected output is hand-written so a wrong width cannot agree with itself |
| AC6 — width does not depend on alignment | 3, 7 | step 7's four-way comparison; `_column_widths` is unchanged, which the diff shows |
| AC7 — guard spaces do not move | 2 | `PaddingPlacementTest`'s "every interior `\|` is followed by a space" assertion (step 6), over a right-aligned and a centred table |
| AC8 — empty cell in a right or centre column | 2 | fixture `align-empty-cell` (`\|   \|` over `\|:-:\|`) |
| AC9 — delimiter row keeps its markers and its width | 3 | fixture `align-markers`; the existing `test_ac14_no_line_gains_or_loses_a_pipe` and the layout-shape tests over the new fixtures |
| AC10 — first column of a bare table | 2, 3 | fixture `align-bare-first-column`, plus the idempotence test (step 5) proving the output is a fixed point in bytes, plus `PaddingPlacementTest`'s recognition assertion (step 6) |
| AC11 — last column with no trailing pipe | 2, 3 | fixture `align-no-trailing-pipe`, plus the existing equal-row-width test over it |
| AC12 — alignment inside a prefix | 3 | fixture `align-blockquote`; `line_prefix` and the prefix rule are untouched |
| AC13 — an unrecognised run is still copied through | 4 | fixture `align-unrecognised` in `UNTOUCHED`, which the existing byte-for-byte test covers |
| AC14 — WI-0001's criteria still hold, less AC12's padding-position clause | 5, 8 | the whole existing suite, which passes apart from the two places encoding the superseded clause (`basic-ascii.out.md` and one assertion in `test_ac12_every_cell_has_exactly_one_space_against_each_pipe`) — see step 5 and `WI-0002/Q-003` — plus every existing document-level test running over the new fixtures. `implement` delivered ten fixture pairs rather than the eight named in step 4; that difference is its declared deviations 2 and 3 in `impl-report.md`, left as a deviation rather than written back into this plan |

## Assumptions

- **The three alignments are represented as the strings `"left"`, `"right"` and `"centre"`.**
  Reversing it — to an enum, or to the `(lead, trail)` pair of booleans the markers literally
  are — is one file, no interface anyone outside `mdtab/table.py` and `tests/test_units.py` sees,
  and no change to any output byte.
- **`column_alignments` is public.** If a later item wants it private, renaming it touches
  `mdtab/table.py` and the unit test that drives it, and nothing else.
- **`align-unrecognised` covers all four rejection routes in one document.** If a future reader
  wants one fixture per rule, splitting it is a fixture-only change with no code impact.

## Decisions and ADRs

| decision | where |
|----------|-------|
| Padding moves inside the field; guard spaces and column widths do not move; the marker is honoured at the ends of a bare row, at the cost of output mdtab will not recognise | ADR-0007 (new) |
| A centred cell's odd spare column goes on the right | the stakeholder, `WI-0002/Q-001`, recorded in AC4 and cited by ADR-0007 |
| The first column of a bare table is aligned anyway | the stakeholder, `WI-0002/Q-002`, recorded in AC10 and cited by ADR-0007 |
| Alignment is computed once per column from the delimiter row rather than re-derived per cell | ADR-0007 §Decision 1 |
| Representation of an alignment value; visibility of `column_alignments`; one fixture for all four rejection routes | `## Assumptions`, above |

## Scaffolding

None. Every file this plan creates is a test fixture or a test, written by `implement`.

## Risks

- **A hand-written expected output can be wrong in the same direction as the code.** The
  `align-unicode` and `align-centre-odd` fixtures are the ones where this bites, because a wrong
  display width or a wrong rounding would agree with itself. Mitigation: their expected halves
  are written by counting columns before the code is changed, and `PaddingPlacementTest` asserts
  the arithmetic independently of any fixture.
- **`align-bare-first-column` encodes behaviour that WI-0003 will change.** Its expected output is
  correct under this item and will stay correct — WI-0003 changes what mdtab *recognises*, not
  what it emits — but the assertion in step 6 that `lay_out` returns `None` for that output is
  exactly the thing WI-0003 makes false. It is written with WI-0003 named in its docstring so the
  next implementer finds it rather than being surprised by it.
- **The existing suite is most of AC14's evidence, and it only helps if the new fixtures are
  registered.** A fixture added to `tests/fixtures/` but missing from `ALIGNED` or `UNTOUCHED`
  would still be round-tripped by `FixtureRoundTripTest` but skipped by every criterion-level
  test. Step 5 is therefore not optional bookkeeping. The same risk has a second face this
  plan missed: the existing suite also *contradicts* AC14 in the two places that encode
  the clause AC14 excepts, so "unchanged" was never available. See step 5.

## Out of scope for this item

- Changing which runs mdtab recognises. WI-0003 owns the recognition fault AC10 creates, and
  `lay_out`'s four rules must come out of this item unchanged.
- Any change to `mdtab/width.py`, `mdtab/scan.py`, `mdtab/textio.py`, `mdtab/filter.py` or
  `mdtab/__main__.py`. If the change appears to need one, that is a signal the design is wrong,
  not a licence.
- Diagnostics of any kind.
