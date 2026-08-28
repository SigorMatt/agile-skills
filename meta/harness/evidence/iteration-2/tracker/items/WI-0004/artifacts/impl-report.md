# Implementation report — WI-0004

Branch `wi/WI-0004`, off `main` at `4d60b3b`. Three code commits, `baa4ebf..7aaa697`, plus the
tracker commit that carries this report and the closing journal entry — so the full range at the
point `verify` picks the item up is `main..wi/WI-0004`, and `git log --grep WI-0004` reconstructs
it. All eight plan steps executed; two deviations, recorded below.

## What was built

**`tidy/ruleset_file.py` gains the "which file" decision** — two functions beside `load`, which is
where it belongs because this module is already the only one that reads a rule file (ADR-0011).

- `default_path(environ)` → `<XDG_CONFIG_HOME>/tidy/rules.ini` when that key is set and non-empty,
  else `<HOME>/.config/tidy/rules.ini` when `HOME` is, else `None`. It reads the mapping it is
  handed and nothing else — no `pwd` lookup, no `expanduser` — so what a run will read is a
  function of its environment (ADR-0014 point 1). `CONFIG_SUBDIRECTORY` and `RULE_FILE_NAME` keep
  the path in one place.
- `resolve(argument, environ)` → `(Ruleset, path)` or `(None, None)`. The flag wins by being
  *given*: the test is `argument is not None`, so `--rules ""` is a path that cannot be opened
  rather than a fallback (ADR-0014 point 3). Presence at the default path is `os.path.lexists`, so
  a dangling symlink counts as present and `load` refuses it with the operating system's reason
  (point 4). `RuleFileError` propagates untouched.

**`tidy/cli.py` calls `resolve` and names the file.** The `if args.rules:` guard is gone; the call
sits inside the same `try`/`except RuleFileError` that already turns a bad rule file into one
stderr line and exit 2, and still above the `os.path.isdir` check, so a rule file is resolved
before the target folder is examined. When a file was loaded, from either source, the run writes
`tidy: using rules from <path>` to stderr — before the banner and therefore before any per-file
line. A run that loaded none writes nothing of the kind. The `--rules` help text and the parser
epilog name the default path in both its forms and say the flag overrides it.

**`tests/support.py` makes the suite hermetic.** `FolderTestCase.setUp` points `XDG_CONFIG_HOME`
at a second throwaway directory and removes `HOME`, restoring both on cleanup, and gains
`default_rules_path()` and `write_default_rules(text)`. No assertion anywhere changed.

**`README.md`** replaces "**There is no default location.**" with a "Where tidy looks when you do
not say" section covering the path, the override, the no-search rule, that nothing in the folder
being tidied is a rule source, the stderr line, and the malformed / unreadable / absent / empty
cases.

## Acceptance criteria evidence

Every row names a test function. `run(...)` is `tests/cli_support.py`'s in-process CLI runner;
`self.preview()` / `self.apply()` pass **no** `--rules`, which is what makes these criteria about
the default location. The transcripts quoted are from the live runs in `## Gates` below.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — a file at `D` sorts the folder, both modes, same as `--rules` on the same file | `resolve` reads `D` when the flag is absent; `cli.py` passes the resulting `Ruleset` to `build_plan` unchanged | `tests/test_cli.py::DefaultLocationSortsTheFolderTests` — `test_preview_stdout_matches_the_same_file_passed_with_rules` (stdout is `SAMPLE_LINES` with `budget.csv` → `recent/data/`, **and** equal to the `--rules` run's), `test_apply_lands_every_file_where_the_preview_said`, `test_apply_from_the_default_location_gives_the_same_tree_as_the_flag`, `test_renamed_bands_from_the_default_location` (`F4`: `taxes.pdf` → `archive/documents/`, the rest under `current/`), `test_renamed_bands_apply_matches_the_flag` |
| AC2 — nothing readable at `D` is a no-rules run | `resolve` returns `(None, None)` when `default_path` is `None` or `lexists` is false | `tests/test_cli.py::NothingAtTheDefaultLocationTests` — `test_preview_prints_exactly_the_built_in_lines`, `test_apply_lands_every_file_where_the_built_in_rules_say`, `test_a_config_directory_that_exists_but_has_no_tidy_folder`, `test_no_config_directory_at_all_is_a_no_rules_run` (`mock.patch.dict(os.environ, {}, clear=True)` — neither variable — exit 0). The suite half: `python3 -m unittest discover -s tests -t . -q` → exit 0, 203 tests, **no existing assertion edited** (see `## Deviations`) |
| AC3 — `--rules PATH` beats `D` | `resolve` short-circuits on `argument is not None` | `tests/test_cli.py::TheFlagBeatsTheDefaultLocationTests::test_the_flags_answer_is_the_one_printed` — `F1` at `D` plus `--rules F3` prints `move   budget.csv -> recent/tables/budget.csv`, the other five lines are AC1's, exit 0, and the stderr line names `F3`'s path and **not** `D` |
| AC4 — the run names the file it used, on stderr, and says nothing when it used none | the `if rule_file is not None:` write in `cli.py`, placed before the banner | `tests/test_cli.py::NamingTheRuleFileTests` — `test_both_modes_name_a_default_location_file`, `test_both_modes_name_a_file_given_with_rules`, `test_a_no_rules_run_says_nothing_in_either_mode`, `test_the_line_carries_the_path_as_given`, and `test_the_line_comes_before_the_first_per_file_line`, which uses `run_interleaved` because the ordering claim spans two streams. `assert_names_the_rule_file` asserts the path is **absent from stdout** in every case |
| AC5 — a malformed file at `D` is refused as a named one is | `RuleFileError` propagates out of `resolve` into `cli.py`'s existing handler | `tests/test_cli.py::MalformedAtTheDefaultLocationTests::test_every_malformed_class_is_rejected_in_both_modes` — the shared `MALFORMED_RULE_FILES` table (11 exhibits across WI-0003 AC8's classes), each at `D`, both modes: exit 2, stdout empty, exactly one stderr line naming `D`, `sample_listing()` unchanged. Plus `test_the_message_is_the_one_the_flag_would_have_given`, which compares the two messages with the paths blanked |
| AC6 — present and unreadable is exit 2, not a no-rules run | `lexists` treats it as present, `load` raises | `tests/test_cli.py::UnreadableAtTheDefaultLocationTests` — `test_a_mode_000_file_stops_the_run`, `test_a_dangling_symlink_stops_the_run` (both: exit 2, stdout empty, one stderr line naming `D`, nothing moved, both modes), `test_the_operating_systems_reason_is_in_the_message` (`Permission denied`), `test_it_is_not_treated_as_a_no_rules_run` |
| AC7 — an empty file at `D` is a rule file that was used | `load("")` returns the built-in tables merged with nothing; `resolve` still reports the path | `tests/test_cli.py::EmptyFileAtTheDefaultLocationTests` — `test_preview_is_the_no_rules_output_but_the_file_is_named` (stdout equals AC2's, stderr names `D`, exit 0), `test_apply_gives_the_no_rules_tree_and_names_the_file` |
| AC8 — a default rule file changes nothing else the tool promises | nothing below `cli.py` can tell where the `Ruleset` came from (ADR-0011) | `tests/test_cli.py::DefaultRulesChangeNothingElseTests` — `test_a_hidden_file_appears_in_neither_stream_and_is_not_moved`, `test_a_pre_existing_subfolder_is_neither_entered_nor_moved_nor_listed`, `test_a_file_matching_neither_the_rules_nor_the_table_is_still_left`, `test_a_collision_at_a_rule_files_destination_is_never_overwritten` (the `budget (2).csv` line in both modes, and the pre-existing file's sha256 unchanged after APPLY) |
| AC9 — `README.md` states all of it | the rewritten `## Your own rules` → `### Where tidy looks when you do not say` | `grep -c "There is no default location" README.md` → `0`. The section states `D` in both forms, that `--rules` overrides it, the stderr line and its absence on a no-rules run, exit 2 for malformed and unreadable, and that an empty file is read and changes nothing — readable against AC1–AC7 |
| AC10 — `--help` no longer says there is no default location | the rewritten `--rules` help and epilog | `tests/test_cli.py::HelpNamesTheDefaultLocationTests` — `test_help_names_the_rule_file_and_says_the_flag_overrides_it` (`rules.ini`, `XDG_CONFIG_HOME`, `--rules` all present) and `test_help_no_longer_says_there_is_no_default_location`. Live: `python3 -m tidy --help | grep -c "no default location"` → `0` |

**Every criterion's test was mutation-checked** — each new behaviour was removed in turn and the
suite re-run, so no criterion is satisfied by a test that would pass against the old code:

| behaviour removed | tests that failed |
|-------------------|-------------------|
| the default location (back to `if args.rules:`) | 25 |
| the `tidy: using rules from` line | 7 |
| `lexists` → `exists` (dangling symlink becomes absent) | 2 |
| `argument is not None` → truthiness (`--rules ""` falls back) | 1 |
| the `HOME` fallback in `default_path` | 2 |

## Deviations from the plan

- **`tests/cli_support.py` gained `run_interleaved()`.** Plan step 7 says the end-to-end tests use
  "the existing `run()` helper", and `run()` keeps stdout and stderr apart. AC4 asks that the
  naming line come **before the first per-file line**, and those are on different streams, so the
  claim is not checkable against two separate buffers. `run_interleaved` redirects both into one
  `StringIO` and returns `(status, text)`. It is additive: `run()` is unchanged and every other
  test still uses it. This is a *how*, not a *what* — without it AC4's ordering clause would have
  been asserted only against stderr's internal order, which is weaker than the criterion.
- **AC5 reuses `MALFORMED_RULE_FILES` from `tests/test_cli.py`, not from
  `tests/test_ruleset_file.py`.** Plan step 7 says the six classes "reuse whatever
  `tests/test_ruleset_file.py` already builds for WI-0003 AC8"; in fact that module builds each
  malformed file inline per test, and the reusable table lives in `tests/test_cli.py`. The intent
  — do not restate the classes — is met, against the table that actually exists. It carries eleven
  exhibits rather than six, because two of AC8's classes have more than one shape.
- **Nothing else.** Steps 1–6 and 8 were executed as written, including step 5's placement of the
  environment isolation in the shared `FolderTestCase`.

## Gates

Run on the branch head `7aaa697`, after the last commit.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 203 tests ... OK` (was 174 on `main`; 29 new) |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 11 item(s), 16 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above: every one of AC1–AC10 names at least one test function, and AC9's non-test half is an exact command with its output. Mutation-checked, five behaviours, table above |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → `all 3 commit(s) on main..wi/WI-0004 name WI-0004`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | seven source files changed. `tidy/ruleset_file.py` → steps 1–2; `tidy/cli.py` → steps 3–4; `tests/support.py` → step 5; `tests/test_ruleset_file.py` → step 6; `tests/test_cli.py` → step 7; `tests/cli_support.py` → step 7, as deviated above; `README.md` → step 8. No hunk traces to anything else |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → `0 errors, 0 warnings` |

**The suite's hermeticity was checked, not assumed** — this is the risk plan step 5 exists for,
and it is the one thing a reader cannot verify by looking at the diff:

- with a rule file at the caller's `XDG_CONFIG_HOME`: `Ran 203 tests ... OK`;
- with one at the caller's `HOME` and `XDG_CONFIG_HOME` unset: `Ran 203 tests ... OK`;
- with step 5's isolation removed and a rule file at the caller's `XDG_CONFIG_HOME`:
  `FAILED (failures=11, errors=32)`.

**Live end-to-end**, outside the suite, over a six-file sample folder:

```
$ XDG_CONFIG_HOME=<cfg> python3 -m tidy <S>          # F1 at D, AC1 and AC4
tidy: using rules from <cfg>/tidy/rules.ini
tidy: preview only - nothing will be moved. Re-run with --apply to move.
move   budget.csv -> recent/data/budget.csv
...                                                   exit 0

$ env -u XDG_CONFIG_HOME -u HOME python3 -m tidy <S>  # AC2, no config directory at all
tidy: preview only - nothing will be moved. Re-run with --apply to move.
move   budget.csv -> recent/spreadsheets/budget.csv
...                                                   exit 0

$ XDG_CONFIG_HOME=<cfg> python3 -m tidy <S> --apply   # AC5, 'csv = data' at D
tidy: <cfg>/tidy/rules.ini cannot be used: 'csv' in [types] is not an extension: it must begin with a '.'
                                                      exit 2

$ XDG_CONFIG_HOME=<cfg> python3 -m tidy <S>           # AC6, mode 000 at D
tidy: <cfg>/tidy/rules.ini cannot be used: Permission denied
                                                      exit 2

$ XDG_CONFIG_HOME=<cfg> python3 -m tidy <S>           # AC7, zero-byte file at D
tidy: using rules from <cfg>/tidy/rules.ini
tidy: preview only - nothing will be moved. Re-run with --apply to move.
move   budget.csv -> recent/spreadsheets/budget.csv
...                                                   exit 0
```

## What I did not do

- **`--rules ""` is now exit 2, and `README.md` does not mention it.** ADR-0014 point 3 made the
  flag win by being *given*, so the empty string names a path that cannot be opened. Live:
  `tidy:  cannot be used: No such file or directory`, exit 2. This is a user-visible change to
  behaviour nobody asked to change — `plan` recorded it as a risk and `review-close` had recorded
  the old behaviour as a gap on WI-0003. The item puts `--rules ''` **out of scope** as a
  documented way of turning `D` off, and `plan` required only that it not be *silently* different
  from `README.md`; `README.md` has never said anything about an empty `--rules`, so nothing there
  contradicts it. I did not document it, and I did not widen the item to cover it. **Two things a
  reviewer should look at:** whether the silence is the right call, and that the message has a
  double space where the empty path would be (`tidy:  cannot be used:`), which is cosmetic, which
  no criterion covers, and which I have not touched because it would be unplanned scope.
- **`XDG_CONFIG_HOME` is not checked for being absolute.** Plan assumption A1, unchanged: a
  relative value is used as given, which the XDG convention says should be ignored. Reversing it is
  one condition in `default_path` and one test.
- **A rule file whose *parent directory* cannot be searched reads as absent, not as present.**
  Plan assumption A3, unchanged: `lexists` returns `False`, so such a run is a no-rules run rather
  than exit 2. It is the one place where "present but unusable" is reported as "absent". No
  criterion names the case and no test asserts it.
- **`docs/architecture/overview.md` still says WI-0004 "is planned and not yet built"** (line 123),
  which this branch makes false. `plan` already wrote the rest of the overview forward-looking and
  bumped it to v10, so everything *else* it says about `default_path`, `resolve` and the default
  location is accurate; it is the one status sentence that is now stale. Updating it is not one of
  the plan's eight steps and no acceptance criterion names it, so I have not made the edit rather
  than widening the item on my own authority — **this is a handover to `review-close`'s D7 and
  D12**, which own document truth, and it needs a version bump and a change-log row when it is
  made.
- **No bug items were filed.** Nothing in another item's delivered behaviour looked wrong while
  working this one.
