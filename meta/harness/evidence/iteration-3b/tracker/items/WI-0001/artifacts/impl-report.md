# Implementation report — WI-0001

Branch `wi/WI-0001`, commits `ac16080..a3297d9` (six, every one naming the item).

## What was built

`mdtab.py` at the repository root — one executable Python 3 file, standard library only, reading
standard input and writing standard output, with no arguments [src: ADR-0001]. It is the whole
tool; there is no package, no build step and nothing to install.

Four layers, in the shape `artifacts/plan.md` designed:

1. **Edges.** `main()` reads `sys.stdin.buffer`, decodes with `errors="surrogateescape"`, encodes
   back the same way, and returns 0. `split_lines()` splits on `\r\n`, `\n` and `\r` only, keeping
   each terminator on its line, so `"".join(split_lines(t)) == t` for every `t` — the property the
   byte-for-byte passthrough promise rests on. `strip_terminator()` is its inverse for one line.
2. **Measurement.** `display_width()` — 2 for a character whose `east_asian_width` is `W` or `F`,
   0 for a combining mark, 1 otherwise [src: ADR-0003] decision 7.
3. **Recognition.** One left-to-right scan in `transform()` holding two pieces of state: the open
   fence and the candidate block. `fence_delta()` tracks ``` and `~~~` fences; `candidate_parts()`
   returns `(prefix, body)` for a line that could be a table row; a candidate block is a maximal
   run of candidates sharing a byte-identical prefix, and a line whose prefix differs both ends
   the current block and starts the next.
4. **Validation and composition.** `split_cells()` splits on unescaped pipes; `is_delimiter_cell()`,
   `table_or_none()`, `column_widths()`, `compose_row()`, `compose_delimiter()` and `emit_block()`
   do the rest. A block that is not a table is copied byte for byte, whole.

`tests/test_mdtab.py` — 14 `unittest` methods. `tests/fixtures/` — 24 files: an input per
criterion group and, where the output differs from the input, a hand-written expected document.

## Acceptance criteria evidence

Every row's command is `python3 -m unittest discover -s tests -t .`, which exits 0 and reports
`Ran 14 tests ... OK`. Each test's docstring is the criterion's own text.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `column_widths()` maxes `display_width()` over the header and body cells; `compose_row()` pads by the same measure | `AlignmentTest.test_ac1_every_table_line_has_the_same_display_width` — runs the filter on `fixtures/wide_chars.md` (ragged rows containing `中文字`, `Jose` + U+0301 and U+1F642), compares byte for byte against the hand-written `wide_chars.expected.md`, asserts the four output lines share one display width, and asserts the **input** lines did not — so the criterion cannot pass vacuously |
| AC2 | the same widths drive every row including the delimiter row | `AlignmentTest.test_ac2_every_column_starts_at_the_same_display_offset` — computes the display width of the text before each `|` on every output line of that table and asserts all four rows give the same list of offsets |
| AC3 | `compose_row()` writes `" " + cell + padding + " "`; cells are stripped in `split_cells()` | `AlignmentTest.test_ac3_cells_carry_one_space_either_side` — `fixtures/ragged.md` against `ragged.expected.md` byte for byte, an explicit assertion that the empty `Note` cell is a pipe and two spaces, and a sweep over **every** fixture's output asserting no composed line ends in a space or a tab |
| AC4 | `compose_delimiter()` fills `width + 2` with hyphens; `column_widths()` excludes the delimiter row | `AlignmentTest.test_ac4_delimiter_row_fills_its_column` — asserts `\|------------\|-----\|-------\|` in `ragged`'s output, where the input's middle delimiter cell was 11 hyphens and the column is 3 wide; and `fixtures/wide_delimiter.md` (delimiter 14 hyphens, content 1 column) against its expected file. **Read AC4 with the item's `## Out of scope` and ADR-0004**: a delimiter cell that carries colons keeps them and still fills the column, which the same test checks via `fixtures/markers.md` |
| AC5 | `emit_block()` re-emits the block's own `prefix` on every composed line; a differing prefix ends the block, and `>` is not whitespace so a blockquote never becomes a candidate | `AlignmentTest.test_ac5_indent_is_restored_byte_for_byte` — `fixtures/indented.md` against its expected file plus an assertion that every output line containing a pipe starts with the original three spaces; and `fixtures/indent_mismatch.md` and `fixtures/blockquote.md` compared byte for byte against their own inputs |
| AC6 | the surrogateescape edges and `split_lines()` | `PassthroughTest.test_ac6_no_table_is_byte_identical` — output compared byte for byte against input for `empty.md`, `prose_only.md`, `no_final_newline.md`, `crlf.md` and `not_utf8.markdown` (which contains `0xe9`, `0x80`, `0xfe` and `0xed 0xa0 0x80`) |
| AC7 | `fence_delta()`; a line inside or bounding a fence is copied and is never a candidate | `AlignmentTest.test_ac7_fenced_pipe_lines_are_left_alone` — `fixtures/fenced.md` holds a ``` block and a `~~~` block each full of pipe lines, plus one real table; the test asserts the output has the same line count and that **every** line not belonging to the real table is byte-identical to its input line, then asserts the real table was aligned |
| AC8 | `table_or_none()` returns `None` and `emit_block()` copies the whole block | `MalformedBlockTest.test_ac8_malformed_block_is_copied_whole` — `fixtures/malformed.md` (a block with no delimiter row, a block with a short body row among well-formed ones, a block whose delimiter row has the wrong cell count) byte-identical to its input, plus explicit assertions that the individually well-formed rows `\| 3 \| 4 \| 5 \|` and `\|  a  \|   b \|` are still exactly as written |
| AC9 | composition is a fixed point of recognition: composed rows re-split to the same cells and re-measure to the same widths, and ADR-0004 decision 2's minimum width keeps a marked delimiter row recognisable | `WholeFilterTest.test_ac9_running_the_filter_on_its_own_output_changes_nothing` — for all 16 input fixtures, the filter is run on its own output and the second output compared byte for byte against the first |
| AC10 | `main()` returns 0 unconditionally | `WholeFilterTest.test_ac10_exit_status_is_zero` — all 16 fixtures run as a subprocess, exit status asserted 0, then run again on their own output and asserted 0 again |
| AC11 | one named method per criterion | `SuiteCoverageTest.test_ac11_each_criterion_has_a_named_test` — discovers the suite and asserts that for each of AC1 to AC10 there is **exactly one** test method whose name carries that criterion's tag and whose docstring quotes the criterion. The suite command is `commands.test` in `tracker/project.yaml`, which exits 5 rather than 0 if no test runs |

**The tests were checked against mutants, not just run.** Self-check 1 asks whether each criterion
would fail if the behaviour were removed, so nine mutations were applied to `mdtab.py` one at a
time and the suite re-run against each:

| mutation | detected by |
|----------|-------------|
| `emit_block` never tidies, only copies | 6 tests |
| `column_widths` measures `len()` instead of display width | 2 tests |
| `compose_row` pads by `len()` instead of display width | 2 tests |
| `compose_delimiter` drops the alignment colons | 2 tests |
| fences ignored | 1 test |
| the delimiter row counts towards column width | 8 tests |
| the cell-count consistency check removed | 4 tests |
| the two-colon minimum width removed (ADR-0004 decision 2) | 1 test |
| composed lines normalise their terminator to `\n` | 1 test |

**Two of those mutants initially survived, and both were real gaps in the tests, now closed.**

- *Width measured in characters rather than display columns.* The first `wide_chars` fixture had
  every column's width set by its ASCII header, so the wide, emoji and combining cells never
  decided a width and `len()` and `display_width()` agreed everywhere. The fixture was rewritten
  so that in each of its three columns the two measures disagree and the non-ASCII cell is the
  widest — which is precisely what `plan.md`'s `## Risks` warned AC1 could otherwise fail to pin
  down. Both `wide_chars.md` and `wide_chars.expected.md` are hand-written, and the expected file
  matched the code's output on the first run.
- *Composed lines normalising their line ending.* No fixture had a **table** with CRLF endings or
  a table as the last line of a file with no terminator, so nothing observed the rule that a
  composed line takes the terminator of the line it replaces [src: ADR-0003] decision 6 and [src: WI-0001]
  `## Notes`. `fixtures/crlf_table.md` and `fixtures/table_no_final_newline.md` were added with
  their expected files, covered by a test named for the rule rather than for a criterion, since no
  criterion names this case.

## Deviations from the plan

1. **Tests were written alongside each step rather than all at step 9.** The `implement`
   procedure requires the test to come with the change in the same commit; the plan collected
   test-writing into step 9. Only the ordering changed — the plan's step 9 content, one method per
   criterion named for it with the criterion as its docstring, is exactly what was produced. Where
   a step's behaviour was not yet final (AC1 to AC5 and AC7 all need step 7's composition), that
   criterion's test was written at step 7 rather than earlier, so no failing test was ever
   committed.
2. **Plan step 5's temporary block-collection test was run but not committed.** The plan said to
   delete it before step 9 if it asserted on an internal shape no criterion needs, which it did.
   It was run as an ad-hoc check — `fixtures/malformed.md` yields exactly three blocks with the
   expected bodies — and never entered the suite.
3. **`tests/fixtures/not_utf8.md` is named `not_utf8.markdown`.** See `## Toolkit collision`
   below. Only the extension differs; the bytes are what AC6 asks for.
4. **Two fixtures beyond the plan's list**: `crlf_table` and `table_no_final_newline`, added for
   the surviving mutant described above. The plan's list was written before the mutation check
   existed and its `## Risks` section asks for exactly this kind of hardening.
5. **`docs/architecture/overview.md` bumped to v2.** Its layout table said `tests/` holds "test
   modules, one per group of acceptance criteria"; the code as built has one module, which the
   plan's own step 9 authorised. This is D12's ordinary repair — the sentence describes the code
   and the code is now written. No sentence citing a stakeholder answer was touched.

## Toolkit collision — the non-UTF-8 fixture and the pipeline's own markdown walkers

AC6 requires an input "containing bytes that are not valid UTF-8", and the natural place for it is
a fixture file with a `.md` extension. Both `.claude/agile-skills/scripts/validate-workspace`
(`check_claim_citations`, line ~1391) and `.claude/agile-skills/scripts/lint-claims`
(`all_markdown`, line ~190) walk **every** non-ignored `*.md` file in the repository and open it
with `encoding="utf-8"` and no error handler. `validate-workspace` catches only `OSError` around
that read. With the fixture named `not_utf8.md`, both gates died with an uncaught
`UnicodeDecodeError` traceback rather than reporting a finding:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 26: invalid continuation byte
```

This is a defect in the toolkit, not in this item or in any item's delivered behaviour, so no bug
item was filed — there is no item it would belong to. The workaround is the rename to
`not_utf8.markdown`, which those walkers skip. It was taken as an ordinary in-plan choice: it is a
fixture's filename, it changes no behaviour, no criterion names a filename, and reversing it is one
`git mv` once the scripts read with `errors="replace"` or catch `UnicodeDecodeError` alongside
`OSError`. It is recorded in `overview.md`'s layout table and in `fixture()`'s docstring so the
next person to reach for `.md` finds out why before the gate crashes on them.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → 0, `Ran 14 tests ... OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test method for each of AC1–AC11; `test_ac11_each_criterion_has_a_named_test` re-checks the mapping mechanically |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → 0, "all 6 commit(s) on main..wi/WI-0001 name WI-0001" |
| `no-unplanned-scope` (advisory) | **pass** | 31 files in `main..HEAD`: `mdtab.py` and `tests/` are plan steps 1–9, the 24 fixtures are step 8, `overview.md` is the D12 repair above, and the rest is this item's own tracker record. No hunk is unrelated |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → 0, 7 consumed human answers checked |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → 0 |

All eight were run on the branch head, after the last commit.

## What I did not do

- **Nothing in the plan was left undone.** All ten steps were executed.
- **No alignment marker is acted on.** `compose_delimiter()` preserves colons and nothing reads
  them; where cell text sits is WI-0002 [src: ADR-0004] decision 3.
- **No bug item was filed** for the toolkit collision above, because a `bug` item in this tracker
  is filed against behaviour another *item* delivered, and no item owns the pipeline's scripts.
  It is reported here and in the turn's harness status instead.
- **A surrogate-escaped byte inside a table cell counts as one display column**, so alignment may
  be off inside a table in a document that is not valid UTF-8. `plan.md`'s `## Risks` names this,
  no criterion covers it, and the passthrough promise is unaffected. Left alone deliberately.
- **A pipe table inside an *indented* code block is still tidied.** ADR-0003 decision 2 accepts
  this and the item's `## Out of scope` records it, so it is not a defect. Not addressed.
- **`main()` ignores any command-line argument** rather than rejecting it, as `plan.md`'s
  `## Assumptions` decided. No test covers argument handling; no criterion mentions arguments.
