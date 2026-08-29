# Implementation report — WI-0001

## What was built

`mdtab`, a Python 3 package with no third-party dependency and no install step, run as
`python3 -m mdtab` from the checkout root. It reads a markdown document on stdin, rewrites the
spacing inside the tables it recognises so the columns line up on screen, and writes every other
byte back exactly as it arrived. Nothing is ever written to stderr.

Six modules, exactly as `plan.md` and `docs/architecture/overview.md` name them:

| module | what it holds |
|--------|---------------|
| `mdtab/textio.py` | `decode`, `encode`, `split_lines`, `join_lines` — the only place an encoding or a line ending is mentioned |
| `mdtab/width.py` | `display_width` — ADR-0002's three rules, and the only place a width is computed |
| `mdtab/scan.py` | `line_prefix`, `strip_prefix`, `in_fence`, `find_runs` — finding candidates, never judging them |
| `mdtab/table.py` | `split_row`, `row_cells`, `is_delimiter_row`, `lay_out` — where a cell boundary is, the four recognition rules, and the layout |
| `mdtab/filter.py` | `format_document(text) -> str`, the pure seam every test drives |
| `mdtab/__main__.py` | decode, call, encode, flush, return 0 |

The whole of ADR-0003's "copy the bytes through" behaviour is one branch: `lay_out` returns
`None` and `format_document` leaves the run's lines where they were.

Twenty-three fixture pairs under `tests/fixtures/`, all written as bytes and all with their
expected output written by hand rather than produced by running the code — including
`unicode-mixed`, which is the plan's first named risk. 55 tests across `tests/test_fixtures.py`
(documents, and the criteria stated over whole documents) and `tests/test_units.py` (the rule each
module owns, and each of ADR-0003's four rejection rules on its own).

### What this round changed

`review-close` rejected the first delivery on D12 with four findings and returned the item to
`in-progress`. All four are closed. No fixture's expected output changed, which is what
`review.md` said should be true of a correct fix, and the tool's behaviour is byte-for-byte what
it was: the whole of this round is tests, one refactor with no observable effect, and type
annotations.

| finding | what changed | shown by |
|---------|--------------|----------|
| 1 — a test built a document from a Python literal, against ADR-0005, undeclared | the AC9 undecodable-bytes document is now the `invalid-utf8` fixture pair; discovery keys on the `.in.` infix so the pair's `.bin` extension is invisible to every other test | the pair exists and `test_ac9_undecodable_bytes_survive_the_round_trip` reads it; the module docstring is true again. Storing it needed a decision — see deviation 6 |
| 2 — the AC11 test was insensitive to the behaviour it names | fixture `tab-in-cell`, whose middle cell's content is `\tb\t` | replacing `_TRIM = " "` with `_TRIM = None` (the `strip(" ")` → `strip()` mutation review named) fails `test_ac11_cell_content_survives_apart_from_the_spaces_around_it` and the `tab-in-cell` round trip. Before this round the same mutation left all 54 tests green |
| 3 — the escaping rule was expressed twice, and the outer-pipe test bypassed the cell splitter | `has_trailing_pipe` decides from `split_row`'s last field; `_escaped_at` is deleted | behaviour-preserving over all 19531 strings up to six characters from `{ \| \\ a space tab }`, 0 disagreements with the deleted version. Breaking `split_row`'s escape handling now fails `test_a_trailing_pipe_that_is_escaped_is_not_a_trailing_pipe`; against the rejected code (`256260f`) the same mutation left that test passing |
| 4 — six signatures were weaker than `plan.md` fixed them | `split_lines`, `join_lines`, `split_row`, `in_fence`, `find_runs` and `lay_out` carry their documented parameterised types | `git diff 256260f..HEAD -- mdtab/` — annotations only, no statement changed |

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `mdtab/__main__.py` reads `sys.stdin.buffer`, writes `sys.stdout.buffer`, returns 0, and never touches stderr | `ProcessTest.test_ac1_python3_m_mdtab_writes_the_document_and_exits_zero` and `ProcessTest.test_ac1_a_document_it_does_not_recognise_still_leaves_stderr_empty`, both spawning `python3 -m mdtab` with `cwd` at the checkout root. Also by hand: `python3 -m mdtab < tests/fixtures/basic-ascii.in.md` → exit 0, stderr 0 bytes, document on stdout |
| AC2 | `_column_widths` measures with `display_width`; `_render_row` pads every field to its column's width | `AlignmentTest.test_ac2_ac3_every_row_of_a_laid_out_table_has_the_same_display_width` and `test_ac2_ac3_each_pipe_sits_at_the_same_display_column_in_every_row`, over all eleven fixtures that contain a laid-out table; the test's `pipe_columns` counts display columns from the line start and skips escaped pipes |
| AC3 | the same code path — nothing in it special-cases ASCII | the two AC2 tests above include `unicode-mixed`, whose cells hold precomposed `José`, decomposed `José`, `表計算`, `⚠️ warn` and `😀`; `DisplayWidthTest` pins each of ADR-0002's rules separately |
| AC4 | `format_document` replaces only the line ranges `lay_out` accepted | `FixtureRoundTripTest.test_ac4_ac5_documents_with_nothing_to_lay_out_come_back_byte_for_byte` (ten fixtures) and `test_ac4_lines_outside_a_table_are_untouched_in_the_fixtures_that_have_one` (the eleven that do contain one) |
| AC5 | same | fixture `no-table`, asserted byte-identical by the test above |
| AC6 | `_column_widths` excludes the delimiter row's own cell and never lets a column be narrower than its delimiter cell can be written | `FixtureRoundTripTest.test_ac6_running_the_tool_on_its_own_output_changes_nothing`, over all 23 fixtures. Also by hand: `python3 -m mdtab < unicode-mixed.in.md \| python3 -m mdtab \| cmp - unicode-mixed.out.md` → identical |
| AC7 | `find_runs` groups two or more non-fenced lines each holding an unescaped `\|`; `lay_out` refuses a run whose second line is not a delimiter row | fixtures `rst-grid`, `html-table`, `pipes-no-delimiter` byte-identical; `RunTest` (four cases) and `DelimiterRowTest` (nine rows); `RejectionTest.test_rule_1_a_run_whose_second_line_is_not_a_delimiter_row` |
| AC8 | `in_fence` flags fence lines and everything between; `find_runs` takes the mask rather than re-deriving it | fixtures `fenced-table` (a ragged table inside a fence) and `fence-unclosed` byte-identical; `FenceTest` covers backtick vs tilde, a longer fence not closed by a shorter one, an unclosed fence running to the end, and a fence inside a blockquote |
| AC9 | `split_lines` returns `(content, terminator)` pairs and `join_lines` reattaches each line's own terminator | `TerminatorTest.test_ac9_crlf_stays_crlf_and_never_reaches_a_cell`, `test_ac9_a_document_with_no_final_newline_gets_none_added`, `test_ac9_undecodable_bytes_survive_the_round_trip` (which reads fixture `invalid-utf8`, asserts its input really does raise `UnicodeDecodeError` under strict UTF-8, and compares bytes); `LineSplittingTest.test_the_round_trip_is_exact_for_bytes_that_are_not_utf_8`. Also by hand: `python3 -m mdtab < crlf.in.md \| od -c \| tail -1` → `\|  \r  \n`, and the same on `no-final-newline.in.md` → ends `\|` with no `\n` |
| AC10 | `split_row` counts the consecutive backslashes before each `\|` and treats it as a separator only when that count is even | fixture `escaped-pipe`; `CellSplittingTest.test_an_escaped_pipe_is_not_a_separator` and `test_an_escaped_backslash_leaves_the_pipe_after_it_a_separator` (`\| a \\\| b \|` → one cell, `\| a \\\\\| b \|` → two) |
| AC11 | `_render_cell` writes back the cell stripped of spaces and pads with spaces only | `ContentPreservationTest.test_ac11_cell_content_survives_apart_from_the_spaces_around_it`, over all 23 fixtures, excluding the delimiter row for the reason under `## Deviations from the plan`. Fixture `tab-in-cell` is what makes it sensitive: its middle cell's content is `\tb\t`, so the mutation `strip(" ")` → `strip()` eats the tabs, narrows the column from 5 to 3 and fails both this test and the round trip |
| AC12 | `_render_cell` is one space, content, padding, one space; `_render_delimiter` fills the column and keeps the colons it found | `LayoutShapeTest`, four tests: each column is `2 + max` over the header and body cells, one space against each pipe, an empty cell renders as spaces (fixture `empty-cells`), and the delimiter row keeps `:` at the ends it had and matches the header's field widths |
| AC13 | `lay_out` compares every row's cell count, delimiter row included, and returns `None` on disagreement | fixture `ragged-rows` byte-identical; `RejectionTest.test_rule_3_a_run_whose_rows_disagree_about_their_cell_count`, both too many and too few |
| AC14 | `_outer_style` requires every row to agree about the leading and the trailing pipe; `_render_row` re-adds exactly the ones the input had | fixtures `bare-pipes` (laid out, still bare), `outer-pipes` (laid out, still fenced by pipes), `mixed-pipes` (byte-identical); `ContentPreservationTest.test_ac14_no_line_gains_or_loses_a_pipe` compares the raw `\|` count of every line of every fixture; `test_ac14_a_bare_table_stays_bare_and_an_outer_pipe_table_keeps_its_pipes`; `RejectionTest.test_rule_4_...` |
| AC15 | `lay_out` compares `line_prefix` byte-for-byte across the whole run before anything else, strips it, and re-attaches it to every output line | fixtures `blockquote-table` and `list-indent-table` (laid out inside `> ` and `  `, both carried through the AC2 assertion), `ragged-prefix` and `tab-prefix` (byte-identical); `PrefixTest`; `RejectionTest.test_rule_2_a_run_whose_prefixes_are_not_byte_identical` |

## Deviations from the plan

1. **AC11 does not govern the delimiter row; AC12 does.** Read literally the two disagree: AC11
   says a cell's content survives, AC12 says the delimiter row's cells are "filled with `-` to the
   same width". AC12 is the specific rule, plan step 6 instructs "render the delimiter cells", and
   AC2 could not hold otherwise — a delimiter row left at its original width would put its pipes
   where no other row's are. The AC11 test therefore skips the delimiter row and
   `LayoutShapeTest.test_ac12_the_delimiter_row_keeps_its_colons_and_fills_the_column` checks it
   instead. This is a reading of two criteria, not a change to either; it is called out here
   because `verify` reading AC11 absolutely would find every laid-out table in breach.
2. **The delimiter minimum-width rule is applied to the delimiter *field*, not to the column.**
   The plan states the minimum as `1 + leading_colon + trailing_colon` characters against the
   column width. For a table written without outer pipes the first and last columns lose one of
   their two spaces, so the field the delimiter cell has to fill is one or two narrower than the
   column; `_column_widths` therefore adds those omitted spaces back before comparing. For every
   table with outer pipes this is arithmetically identical to what the plan wrote.
3. **One fixture beyond the plan's list: `tab-prefix`.** A blockquote table one row of which is
   indented with a tab where the others have a space. It was added because a mutation check showed
   the plan's `ragged-prefix` fixture is rejected by the outer-pipe rule rather than by the prefix
   rule, so with the prefix rule deleted every test still passed. `tab-prefix` and the matching
   unit test isolate rule 2; deleting the prefix check now fails four tests.
4. **`find_runs` imports `has_unescaped_pipe` inside the function body.** `mdtab.table` imports
   `line_prefix` from `mdtab.scan`, so a module-level import back would be a cycle. The rule about
   where a cell boundary is stays in `mdtab.table`, which is what the overview requires; only the
   import site moved. A comment at the call site says so.
5. **Cell content is trimmed of spaces (U+0020) and of nothing else**, rather than of all
   whitespace. AC11 says "leading and trailing spaces", and `str.strip()` would fail it literally
   for a cell containing a tab. The plan does not state which; this is the reading that keeps AC11
   true as written.

6. **The `invalid-utf8` fixture pair carries `.bin`, not `.md`.** Declared here because the route
   matters even though `plan.md` step 10 now states the rule. Fixing finding 1 as `review.md`
   specified produces a `.md` file holding a `0xFF` byte, and `validate-workspace` walks every
   non-ignored `.md` file in the project, opens it as UTF-8, and catches only `OSError` — so that
   file aborted the validator with a `UnicodeDecodeError` traceback rather than producing a
   finding. Since `workspace-valid` is a hard gate of every skill, the pipeline could not run at
   all with the pair present. That is not a decision `implement` may take, so it was filed as
   `Q-004`, answered by `answer-questions` as ADR-0006, and propagated into `plan.md` steps 10 and
   11 before this round resumed. The intermediate commits are on the branch: `cc0eea6` made the
   pair `.md`, `a2059b7` backed it out so `answer-questions` could run, and `459123c` recreated it
   as `.bin`.

   The underlying `validate-workspace` behaviour is a defect in the pipeline's own machinery, not
   in mdtab. It is reported in this item's journal and in ADR-0006's `## Consequences`, and it was
   deliberately not patched: a local edit to `.claude/agile-skills/scripts/` would be invisible to
   a reviewer of mdtab, covered by no criterion, and discarded by the next toolkit install.

7. **One test beyond the plan's list: `test_every_fixture_is_a_complete_pair_with_one_extension`.**
   It is the cost of deviation 6. Keying discovery on the `.in.` infix means a half-renamed pair —
   `invalid-utf8.in.bin` beside `invalid-utf8.out.md` — would simply never be read, and every test
   here would keep passing against a document nobody compared. The test asserts both halves exist
   at the discovered extension and that no file in `tests/fixtures/` is outside a discovered pair;
   renaming one half turns 55 green into 2 failures and 2 errors.

Steps 1 to 12 of the plan were all executed, in order, and no step was changed in substance.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 55 tests ... OK`, on branch head `459123c` |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function, or a command with its output, for all fifteen |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 13 commit(s) on main..wi/WI-0001 name WI-0001" |
| `no-unplanned-scope` (advisory) | **pass** | every file in `git diff --stat main..HEAD` maps to a numbered plan step: 1 → `textio.py`, 2 → `width.py`, 3/5/6 → `table.py`, 4 → `scan.py`, 7 → `filter.py`, 8 → `__main__.py`, 9 → `.gitattributes`, 10 → `tests/fixtures/`, 11 → `test_fixtures.py`, 12 → `test_units.py`. Every hunk in `git diff 256260f..HEAD` maps to a numbered finding in `review.md`: 1 → `tests/fixtures/invalid-utf8.*.bin` and `test_fixtures.py`, 2 → `tests/fixtures/tab-in-cell.*`, 3 and 4 → `table.py`, 4 → `scan.py` and `textio.py`. Nothing else in the tool was touched |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, `checked 2 document(s) changed since main` — ADR-0005 (v2) and ADR-0006, both written by `answer-questions` this round. Its first draft of ADR-0006 failed with four `claim.unsourced` errors, which were sourced before the commit |

Beyond the gates, each of the eleven behaviours the tests exist to protect was deleted in turn and
the suite re-run; every deletion failed at least one test. The one that did not — removing the
prefix-equality rule — is deviation 3 above, and was fixed rather than reported.

This round re-ran three mutations against the branch head and recorded what each proves:
`_TRIM = " "` → `_TRIM = None` (finding 2's regression) → 2 failures; `split_row` ignoring the
backslash count (finding 3's drift) → 6 failures including the escaped-trailing-pipe unit test,
which the rejected code at `256260f` survived; and half-renaming the `invalid-utf8` pair
(deviation 7's risk) → 2 failures and 2 errors.

## What I did not do

- **No `bin/mdtab`, no way to name a file, no flags.** `plan.md`'s assumptions record
  `python3 -m mdtab` from the checkout root as the single supported invocation, and no criterion
  asks for more.
- **Alignment markers are preserved but not honoured.** `:---:` survives the delimiter row and
  changes nothing about how a cell is padded. That is WI-0002 and this item's `## Out of scope`.
- **The CPython 3.8 floor is asserted, not tested.** Only 3.12.3 is installed here. Nothing in the
  code uses syntax or a builtin newer than 3.8 — `str.removeprefix` in particular is not used
  anywhere — but no interpreter proved it, and `plan.md` already flags this as review's only
  check.
- **No `README` or user-facing documentation.** No criterion asks for one, and ADR-0002's
  limitation about joined emoji sequences is recorded in the ADR rather than in a document a user
  would read. Worth an item if the tool is ever published.
- **AC12's wording is still not amended.** `item.md`'s `## Notes` and `review.md` both record that
  AC12's "exactly `2 + max`" clause cannot hold for a column whose cells are all empty and whose
  marker is `:---:`; the tool renders 3, which `plan.md` decided before implementation and which
  `verify` and `review-close` both accepted. `review.md` says explicitly that `implement` must not
  touch AC12 or the code for it, so I did not. It needs its own question and it is worth settling
  before WI-0002 builds on AC12's arithmetic.
- **The `validate-workspace` defect behind deviation 6 was reported, not fixed.** See deviation 6
  for why.
- **Nothing was fixed that this item did not ask for.** No defect in another item's behaviour was
  found; WI-0001 is the first item to deliver any.
