# Implementation report — WI-0001

## What was built

`python3 -m tidy <folder>` previews; `python3 -m tidy <folder> --apply` moves. Four modules, in
the layering ADR-0002 fixes:

| module | what it does |
|--------|--------------|
| `tidy/rules.py` | AC5's table as `DEFAULT_RULES`, and `folder_for(filename)` over a flattened index of it |
| `tidy/planner.py` | `Action` and `build_plan(folder)` — every destination, collision suffix included, decided here and nowhere else. Writes nothing. |
| `tidy/apply.py` | `apply_plan(folder, actions)` — executes an action list, decides nothing, and returns one message per action that did not complete |
| `tidy/cli.py` + `tidy/__main__.py` | argument parsing, rendering, exit codes |

`README.md` is the file a user reads the rule table in (AC5). 37 tests across four test modules
and two helper modules.

stdout carries one line per file and nothing else; the banner and every error go to stderr. That
is what makes "exactly one line per file that would be moved" (AC3) checkable by counting lines
matching `^move `.

## Acceptance criteria evidence

Every test named below is in `tests/`, and `python3 -m unittest discover -s tests -t . -q` exits 0
with 37 tests.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `argparse` help names the positional `folder`, `--apply`, and — in the epilog — that without it tidy "previews only … changes nothing on disk" | `test_cli.HelpAndModeTests.test_help_names_folder_apply_and_default` — asserts exit 0 and all four strings in stdout |
| AC2 | `main` returns before `apply_plan` unless `args.apply` | `test_cli.HelpAndModeTests.test_bare_invocation_moves_nothing` — (path, size, sha256) listing identical after a bare run, and neither `images/` nor `documents/` exists |
| AC3 | `render` emits `move   <name> -> <destination>`; `leave` lines start with a different word | `test_cli.PreviewOutputTests.test_preview_prints_one_move_line_per_moved_file` — 3 recognised + 1 unrecognised file, asserts exactly 3 `^move ` lines, the exact set of (name, destination) pairs, and exit 0 |
| AC4 | `build_plan` performs no writes; `os.makedirs` is only ever called from `apply_plan` | `test_cli.HelpAndModeTests.test_preview_leaves_tree_byte_identical` and `test_planner.ScanTests.test_building_a_plan_changes_nothing_on_disk` — recursive (path, size, sha256) sets compared before and after, plus asserting no destination folder was created |
| AC5 | `DEFAULT_RULES`; `folder_for` lowercases `os.path.splitext(...)[1]` | `test_rules.ExtensionTableTests.test_the_table_is_exactly_ac5s` (a second copy of AC5's table, asserted equal row by row), `test_every_extension_maps_to_its_folder` (one fixture file per extension — all 59 — asserting both `folder_for` and the planned destination), `test_extension_match_is_case_insensitive` (`PHOTO.JPG` → `images`), `test_readme_documents_every_rule` (reads `README.md` and asserts each extension appears in its folder's row) |
| AC6 | `folder_for` returning `None` produces `Action(kind="leave", reason=...)`; `cli.main` prints every action line unconditionally | `test_planner.ScanTests.test_unrecognised_file_yields_leave_action`, `test_cli.PreviewOutputTests.test_leave_line_is_not_a_move_line` (asserts the lines for `notes.xyz` and `README` are `leave` lines, are not move lines, and that both files are still at their original paths after `--apply`), and `test_leave_lines_are_printed_when_nothing_moves` (the folder holding only those two files — the fixture Q-001 settled) |
| AC7 | `apply_plan` creates each destination's parent with `os.makedirs(..., exist_ok=True)` then links and unlinks | `test_cli.ApplyTests.test_apply_lands_every_destination_and_loses_nothing` — the multiset of (basename, size) found recursively is identical before and after, every previewed destination exists, and no source path remains; plus `test_apply.ApplyTests.test_every_move_lands_and_the_source_is_gone` (asserts each destination holds the file's actual contents) and `test_destination_folders_are_created_as_needed` |
| AC8 | Apply is `build_plan` → render → `apply_plan` over the same list, so agreement is structural (ADR-0002) | `test_cli.ApplyTests.test_apply_matches_the_preview_it_printed` — parses (file, destination) pairs from both runs and asserts the sets are equal, and additionally that the two stdouts are identical strings |
| AC9 | Collisions are resolved in `build_plan` before anything moves; the move itself is `os.link`, which fails rather than overwrites (ADR-0003) | `test_apply.NeverOverwriteTests.test_existing_file_is_untouched_on_collision` (the pre-existing `documents/report.pdf` has the same sha256 and the same contents after the run; the incoming file is at `documents/report (2).pdf`) and `test_link_refuses_an_existing_destination` (a fabricated colliding action, as if the folder changed mid-run — reported, not executed, both files intact); plus `test_planner.CollisionTests` ×4 |
| AC10 | `render` appends `   [<renamed_from> exists]` when a suffix was applied, in both modes | `test_cli.CollisionReportingTests.test_collision_line_names_the_suffixed_name_in_both_modes` — asserts `documents/report (2).pdf` appears in the preview move line and in the apply move line |
| AC11 | `build_plan` skips `entry.is_dir()` and never recurses | `test_cli.ApplyTests.test_subfolder_and_contents_are_untouched` (the recursive listing under `holiday/` is identical after `--apply`, and neither `holiday`, `pic.jpg` nor `deep.png` appears in either mode's stdout) and `test_planner.ScanTests.test_subfolders_are_neither_listed_nor_entered` |
| AC12 | Follows from AC11: the folders the first run created are subfolders on the second | `test_cli.ApplyTests.test_second_apply_is_a_no_op` — the listing after the second `--apply` equals the listing after the first, and a following preview prints no `^move ` lines and exits 0 |
| AC13 | `build_plan` emits no action at all for a name starting with `.` | `test_planner.ScanTests.test_hidden_files_produce_no_action` and `test_cli.HiddenFileTests.test_hidden_files_appear_in_no_output` — `.bashrc` and `.hidden.jpg` appear in neither mode's stdout and are still at their original paths after `--apply` |
| AC14 | `main` returns 2 after writing to stderr when `os.path.isdir` is false | `test_cli.BadTargetTests.test_missing_path_and_non_directory_exit_2` — four subtests (missing path and a regular file, × both modes): exit 2, stdout exactly `""`, the offending path in stderr, and the folder's listing unchanged |
| AC15 | When the action list holds no `move`, the "Nothing to do" line is printed after the action lines (of which there are none in AC15's four cases) | `test_cli.NothingToDoTests.test_nothing_to_do_cases` — three fixtures (empty; only a subfolder; only hidden files) × both modes, asserting exit 0, no `^move ` lines, and **exactly one** stdout line stating there is nothing to do; plus `test_an_already_tidy_folder_has_nothing_to_do` for the fourth case AC15 names |

**The tests were checked for bite, not just for passing.** Five behaviours were removed one at a
time and the suite re-run, to confirm each criterion's tests fail when the behaviour is gone:

| behaviour removed | result |
|-------------------|--------|
| the hidden-file skip in `build_plan` (AC13) | FAILED (3 failures) |
| the subfolder skip in `build_plan` (AC11) | FAILED (4 failures, 4 errors) |
| collision resolution in `_free_destination` (AC9, AC10) | FAILED (3 failures, 1 error) |
| the `--apply` guard in `cli.main` (AC2, AC4) | FAILED (4 failures) |
| unconditional printing of action lines (AC6, per Q-001) | FAILED (2 failures) |

The suite was restored and is green after each.

## Deviations from the plan

1. **The `leave` reason for a file with no extension reads `no extension`**, not the plan's
   template `no rule for '<ext>'`, which would have rendered as `no rule for ''`. Message wording
   is explicitly the developer's [src: WI-0001], and AC6 constrains what a leave line must contain,
   not how it reads.
2. **The preview banner uses a hyphen, not an em dash** — `tidy: preview only - nothing will be
   moved. Re-run with --apply to move.` The plan gave its text as an example ("e.g."). A hyphen
   avoids depending on the terminal's encoding for a line printed on every run.
3. **`os.path.lexists` rather than `os.path.exists`** in `_is_taken` and in the destination-parent
   check. A broken symlink at a destination path counts as taken, so it is suffixed around rather
   than linked over. This tightens AC9 in the direction it points; `os.link` would have failed on
   it anyway, but as an apply-time failure rather than a planned rename.
4. **Two helper modules the plan's step 8 did not name** — `tests/support.py` (`FolderTestCase`,
   the fixture builders, and the (path, size, sha256) listing several criteria compare against) and
   `tests/cli_support.py` (running `main` in-process and parsing what it wrote). Neither holds a
   test. `unittest discover`'s default pattern is `test*.py`, so neither is collected as one.
5. **More tests than the mapping table names** — 37 rather than the 16 it lists. Every row of the
   table is present under the name it gives; the extras are `test_the_table_is_exactly_ac5s`,
   four `test_planner.CollisionTests`, `test_actions_are_in_name_order`,
   `test_an_existing_destination_folder_is_used_normally`,
   `test_one_failure_does_not_stop_the_remaining_actions`, `test_leave_actions_do_nothing`, and
   `test_an_already_tidy_folder_has_nothing_to_do`.
6. **No opening journal entry was written for this execution.** SKILL.md step 3 ties it to the move
   to `in-progress`, and the item was already there — `answer-questions` returned it at
   2026-08-27T16:16:56Z. There was no transition to carry an entry, and writing a free-standing one
   claiming a move would have been false. The reconciliation it would have recorded is in this
   report's first `## What I did not do` bullet and in the closing journal entry.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 37 tests … OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC15; none is demonstrated by reading the code; the mutation table shows the tests fail when the behaviour is removed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → `all 6 commit(s) on main..wi/WI-0001 name WI-0001` |
| `no-unplanned-scope` (advisory) | **pass** | the diff against `main` is 5 modules, 6 test files and `README.md`; every one is a numbered plan step (1–8). No age routing, no rule loading, no unrelated fix. |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → 0 errors; no document under `docs/` changed |

## What I did not do

- **Nothing exercises ADR-0003's hard-link fallback.** `_move_without_a_link` runs only when
  `os.link` raises a non-`FileExistsError` `OSError`, which needs a filesystem the test suite
  cannot create. The plan records this as a risk and asks that `verify` be told rather than
  discover it. Two consequences follow, and neither is covered by a criterion: on such a
  filesystem the never-overwrite guarantee is the weaker check-then-move, and — because plan step 4
  puts the "fallback was used" note in the same list the CLI reads as failures — a run in which
  every file moved successfully would exit **1**. That is the plan followed literally; if it is
  wrong it is a decision to revisit, not something this execution should have quietly changed.
- **An unreadable target folder is not handled.** `os.scandir` raises `PermissionError` out of
  `build_plan` and the user sees a traceback. AC14 covers a missing path and a regular file only,
  and no criterion covers this. It is a candidate bug item; it was left rather than guessed at,
  because inventing an exit code and a message here would be inventing a requirement.
- **Symlinks at the top level are unspecified and untested.** `entry.is_dir()` follows them, so a
  symlink to a directory is skipped like any subfolder, and a symlink to a file is classified by
  its own name and moved. `os.link` follows the symlink by default, so what lands at the
  destination is a hard link to the target rather than the link. No criterion mentions symlinks.
  Named here so it is a known gap rather than a surprise.
- **Nothing was done about the in-memory action list.** The plan accepts it as a risk for the
  folder sizes the vision describes.
- **No performance, packaging, or installation work.** `python3 -m tidy` is run from the repository
  root, as ADR-0001 intends; there is no `setup.py`, entry point or man page, and none was planned.
