# Implementation report — WI-0003

Branch `wi/WI-0003`, from `main` at `0a56b7a`. The code and documents are in five commits,
`58c4607` through `5f85705`; the commits after those carry this report and the item's own record,
so `git log --grep WI-0003 wi/WI-0003` is longer than five and the count grows by one more when
this execution's journal entry is committed.

## What was built

The tool's two sorting tables are now a value a run is handed rather than constants it reads.

- **`tidy/rules.py`** keeps `DEFAULT_RULES` and `DEFAULT_BANDS` byte-for-byte as they were, and
  gains a frozen `Ruleset` holding `by_extension` and `bands` with `folder_for` and `band_for` as
  its methods, `BUILT_IN` built from the two constants, and `merge(base, types, bands)` — the
  layering, which is a dict update on the inverted extension index (ADR-0011). The two
  module-level lookup functions are gone.
- **`tidy/ruleset_file.py`** is new: `load(path)` reads one INI file with `configparser`
  (`interpolation=None`, `optionxform = str`), validates it in the order `plan` fixed, and returns
  `merge(BUILT_IN, ...)`; anything wrong raises `RuleFileError` carrying one line that names the
  file and the problem (ADR-0010).
- **`tidy/planner.py`**'s `build_plan(folder, ruleset=None)` resolves `None` to `BUILT_IN` in its
  body and calls the two lookups on it. Nothing else in the function moved — the collision
  handling, the `leave` reasons, the per-entry `OSError` boundary and the single clock read are
  untouched.
- **`tidy/cli.py`** gains `--rules PATH` and reads it **before** the target folder is examined: a
  rule file that cannot be used gets one stderr line, nothing on stdout, and exit 2, in both
  modes, with nothing moved (ADR-0006).
- **`README.md`** gains a "Your own rules" section, and its exit-status paragraph now covers a
  rule file. **`docs/architecture/overview.md`** is at v9.

## Acceptance criteria evidence

Every row names test functions. `T` is `python3 -m unittest discover -s tests -t . -q`, which
reports `Ran 157 tests ... OK`, exit 0.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — no rules, nothing changes | `build_plan`'s parameter defaults to `None`; `--rules` is optional | `tests.test_cli.NoRulesSuppliedTests` — `test_preview_prints_exactly_the_built_in_lines` asserts PREVIEW's stdout equals `SAMPLE_LINES`, the item's "where it goes today" column verbatim; `test_preview_moves_nothing` compares `listing()` before and after; `test_apply_lands_every_file_where_the_preview_said` asserts the resulting tree; `test_a_rules_flag_naming_nothing_is_a_no_rules_run` covers the empty-file case. Plus `tests.test_planner.RulesetParameterTests.test_no_ruleset_is_the_built_in_one`. **No existing test was edited to accommodate this item**: `tests/test_rules.py`'s call sites moved onto `BUILT_IN` and not one assertion changed (`git diff main..wi/WI-0003 -- tests/test_rules.py`) |
| AC2 — a named extension is redirected, and only it | `merge` is a dict update per entry | `tests.test_cli.TypeEntryTests.test_a_named_extension_is_redirected_and_only_it` — `F1` over `S`, asserting stdout equals `SAMPLE_LINES` with only line 0 replaced by `move   budget.csv -> recent/data/budget.csv`. Value level: `tests.test_rules.MergeTests.test_a_named_extension_is_redirected` and `.test_an_extension_the_rules_do_not_name_keeps_its_folder` |
| AC3 — an extension the built-in table lacks | `merge` adds keys the base has not got | `tests.test_cli.TypeEntryTests.test_an_extension_the_built_in_table_lacks_is_added` — `F2` over `S`, asserting the `leave` line becomes `move   notes.xyz -> recent/notes/notes.xyz` and the other four lines are unchanged. Also `tests.test_planner.RulesetParameterTests.test_an_added_extension_turns_a_leave_into_a_move` and `tests.test_rules.MergeTests.test_an_extension_the_built_in_table_lacks_is_added` |
| AC4 — two rule files, two previews, one differing line | no state carries between calls | `tests.test_cli.TypeEntryTests.test_two_rule_files_over_one_unmoved_folder_differ_in_one_line` — `F1` then `F3`, no APPLY between; asserts the two outputs are the same length and that the zipped differences are exactly one pair, `recent/data/budget.csv` against `recent/tables/budget.csv` |
| AC5 — bands renamed, boundary moved | `[bands]` replaces the pair outright | `tests.test_cli.BandEntryTests.test_bands_are_renamed_and_the_boundary_moves` asserts all four destinations under `F4`; `.test_the_boundary_belongs_to_the_older_band` adds three files at 90 days, 90 days − 1 min and 90 days + 1 min and asserts `archive`, `current`, `archive`. The **exactly**-on-the-boundary case is pinned where a clock cannot blur it: `tests.test_ruleset_file.WellFormedTests.test_a_user_boundary_keeps_the_half_open_comparison` asserts `band_for(90 * DAY) == "archive"` |
| AC6 — either section alone | `merge` keeps what is not given | `tests.test_cli.EitherSectionAloneTests.test_type_entries_alone_keep_the_built_in_bands` (`F1` → `taxes.pdf` at `old/documents/taxes.pdf`) and `.test_band_entries_alone_keep_the_built_in_type_table` (`F4` → `budget.csv` at `current/spreadsheets/budget.csv`). Also `tests.test_ruleset_file.WellFormedTests.test_types_alone_keeps_the_built_in_bands`, `.test_bands_alone_keeps_the_built_in_type_table` |
| AC7 — exactly two bands | `[bands]` has three fixed keys, so a third band is unrepresentable | `tests.test_cli.BandEntryTests.test_a_third_band_is_rejected_in_both_modes` and `.test_a_single_band_is_rejected_in_both_modes` — each asserts, in both modes, non-zero exit, empty stdout, exactly one stderr line, and `listing()` unchanged. `.test_no_third_band_name_appears_in_either_mode` asserts the set of top-level components under `F4` is exactly `{current, archive}`. Message level: `tests.test_ruleset_file.MalformedTests.test_a_band_count_other_than_two` (asserts the message names `middling` and "two bands") and `.test_a_band_count_of_one` |
| AC8 — six malformed classes, both modes | validated in `ruleset_file.load`, before the folder is touched | `tests.test_cli.MalformedRuleFileTests.test_every_malformed_class_is_rejected_in_both_modes` — 11 exhibits covering all six classes, each run in **both** modes, asserting exit non-zero, `stdout == ""`, exactly one stderr line naming the rule file, and `listing(S)` byte-for-byte unchanged. `.test_the_exit_status_is_2` pins the status. Per-class messages: `tests.test_ruleset_file.MalformedTests`, 17 tests, each asserting the message is one line, names the file, and names the offending key or value — including `test_a_multi_line_parser_error_is_collapsed_to_one_line` |
| AC9 — never-overwrite on a user destination | the collision logic is in `build_plan` and is not rule-dependent | `tests.test_cli.NeverOverwriteUnderRulesTests.test_both_modes_print_the_suffixed_destination` (`F5`, pre-existing `recent/papers/report.pdf`, asserts `recent/papers/report (2).pdf` in **both** modes) and `.test_the_file_that_was_already_there_is_untouched` (sha256 identical afterwards, and the incoming file's contents are at the suffixed path) |
| AC10 — hidden files, subfolders, no catch-all | none of the three is reachable from a rule file | `tests.test_cli.RulesChangeNothingElseTests` — `test_a_hidden_file_is_in_neither_mode_s_output_and_is_not_moved`; `test_a_pre_existing_subfolder_is_neither_entered_nor_moved_nor_listed`; `test_a_file_matching_neither_table_still_gets_a_leave_line`; `test_removing_an_extension_from_a_rule_file_leaves_its_files_again`. Also `tests.test_planner.RulesetParameterTests.test_a_ruleset_does_not_disturb_the_invariants` |
| AC11 — preview and apply agree, collision included | `build_plan` is still the only place a destination is chosen (ADR-0002) | `tests.test_cli.PreviewAndApplyAgreeUnderRulesTests` — one test per rule file (`F1`, `F2`, `F4`, `F5`, `F6`); each captures PREVIEW's (name, destination) pairs, applies over the unchanged `S`, and asserts every promised destination exists and no source name remains. `test_f6_a_destination_named_after_a_band` additionally asserts `taxes.pdf` at `old/old/taxes.pdf` and `report.pdf` at `recent/old/report.pdf` |
| AC12 — `README.md` says all of it | the "Your own rules" section | `tests.test_rules.ReadmeDocumentsTheRuleFileTests`, 7 tests read against AC2, AC5, AC7, AC8 and AC11: where a rule file comes from and that there is no default location; the worked example's six lines, which are ADR-0010's and produce AC2's and AC5's results; layering and that a mapping cannot be removed; exactly two bands whatever they are called; one stderr line, nothing on stdout, exit 2; `old/old/report.pdf`; and that the exit-status paragraph now names `--rules` |

## Deviations from the plan

Five, all of them "how" rather than "what". None changes what is delivered.

1. **`[DEFAULT]` is rejected as an unknown section.** The plan's step 4 says "a section other than
   `[types]` or `[bands]`", and `configparser` does not report `DEFAULT` in `sections()` — its
   keys leak into every section instead. `_reject_unknown_sections` checks `parser.defaults()`
   first, so `[DEFAULT]` is rejected by name rather than silently changing both tables. Pinned by
   `tests.test_ruleset_file.MalformedTests.test_a_default_section`.
2. **A comment is a whole line.** `configparser`'s default is that a `#` part-way through a line
   is part of the value, and neither ADR-0010 nor the plan overrode it, so
   `.csv = data  # note` yields a folder literally called `data  # note`. Taken as the default
   ADR-0010's "INI via `configparser`" chose; documented in `README.md` ("put your note on the
   line above") and pinned by
   `tests.test_ruleset_file.WellFormedTests.test_a_comment_part_way_through_a_line_is_part_of_the_value`.
   Reversing is one keyword argument, `inline_comment_prefixes`, and it would cost a folder name
   containing a `#`.
3. **ADR-0008's grep needs its word-boundary form.** `cli.py` imports `.ruleset_file`, and
   `ruleset` begins with the five letters `rules`, so the plan's literal check — "no line naming
   `rules`" — now gives a false hit. What ADR-0008 decided is that `cli.py` imports no rule
   *table*, and that holds: `grep -nE "^(from|import).*\brules\b" tidy/cli.py` exits 1 with no
   output, and `cli.py`'s six import lines are `argparse`, `os`, `sys`, `.apply`, `.planner`,
   `.ruleset_file`. Recorded in `docs/architecture/overview.md` v9 so a later reader is not left
   to work it out. No ADR was changed; `implement` may not.
4. **`_has_separator` checks `os.altsep` too**, not only `/` and `os.sep`. One extra element in a
   list, and it is the same rejection on a platform where `\` separates paths.
5. **AC5's exactly-on-the-boundary case is asserted at the value level**, in
   `test_ruleset_file`, rather than through the CLI. A file whose mtime is set to exactly 90 days
   ago is fractionally *older* than 90 days by the time `build_plan` reads the clock, so no
   clock-driven test can assert the exact case; the CLI test does the three files AC5 names and
   the value-level test does the exact one. Both are cited in the AC5 row above.

## Gates

Run after the last code or document commit, `5f85705`, and re-run on `5a5639c` once
this report was written. Both runs are identical: the commits between them touch only
`tracker/`.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 157 tests in 0.159s / OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 10 item(s), 13 document(s) / 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above: every one of AC1–AC12 names test functions, none is demonstrated by reading code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → `all 7 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0. The count rises as this report and the journal entry are committed; every commit on the branch names the item |
| `no-unplanned-scope` (advisory) | **pass** | 10 files changed under `tidy/`, `tests/`, `README.md` and `docs/`; every hunk traces to one of plan steps 1–11. Nothing else was fixed on the way, and no acceptance criterion was edited — `item.md`'s only diff is the `status`, `updated` and `branch` fields the transition script writes |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → `checked 1 document(s) / 0 errors, 0 warnings` |

## What I did not do

- **Nothing in the plan was left undone.** All eleven steps are on the branch.
- **No default rule-file location**, and no way to remove a built-in mapping, change the band
  count, or write a destination more than one folder deep. All are on the item's out-of-scope
  list, and `README.md` says so plainly rather than leaving a user to discover it.
- **I did not fix anything I noticed on the way**, and I noticed nothing new: BUG-0005 and
  BUG-0006 are already filed and were left alone.
- **`float("inf")` is accepted as `boundary-days`.** It is a positive number, so it passes the
  check AC8 asks for, and it means "everything is in the newer band". Not specified either way,
  cheap to reject later, and the preview shows the result. Named here rather than left for
  `verify` to find.
- **A rule file that is well-formed but meaningless is accepted**, as `plan` predicted:
  `.csv = .csv` files spreadsheets under a folder called `.csv`. Odd, not wrong, and visible in
  the preview.
