# Implementation report — WI-0002

Branch `wi/WI-0002`, seven commits, `main..wi/WI-0002`. All six hard gates pass on the branch
head; the advisory one is reported below with the one thing it flags.

## What was built

Age routing, as the plan's nine steps describe it, in two source files and nothing else.

- **`tidy/rules.py`** gains `DEFAULT_BANDS` — an ordered `(band, max_age_seconds)` table,
  `(("recent", 365 * 24 * 3600), ("old", None))` — and `band_for(age_seconds)`, which returns the
  first band whose bound is `None` or strictly greater than the age. The final `None` bound is what
  makes the table total, and the strict comparison is what puts a file exactly on the boundary into
  `old` [src: ADR-0005].
- **`tidy/planner.py`** reads the clock **once** per `build_plan` call, ages each recognised file by
  `now - entry.stat().st_mtime`, and composes the destination as `os.path.join(band, type_folder,
  name)`. The not-a-folder check that WI-0001/Q-002 introduced for the type folder now walks every
  component of the destination in turn, via a new `_blocking_component`, and the `leave` line's
  reason names the component that is actually blocked.
- **`tidy/apply.py` and `tidy/cli.py` are byte-for-byte unchanged**, which the plan predicted and
  which `git diff main..wi/WI-0002 --stat` confirms. `apply_plan` already created the destination's
  parent with `os.makedirs(..., exist_ok=True)`, and `render` already printed whatever destination
  string the action carried.
- **`README.md`** documents the tree shape, both bands, the field age is measured from, and the
  boundary. **`docs/architecture/overview.md`** goes to v3, correcting the two statements the code
  falsified.

The order in which the type folder and the band are decided matters and is deliberate: a file with
no matching extension is returned as `leave` **before** any age is looked at, so no band is ever
chosen or created on an unrecognised file's account (AC6).

## Acceptance criteria evidence

Test names are given as `module.Class.test`; every one of them is in the 63 that
`python3 -m unittest discover -s tests -t . -q` runs.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — destination is `<band>/<type>/<name>` | `build_plan` joins band, type folder and name | `test_planner.BandRoutingTests.test_a_destination_is_band_then_type_then_name` asserts the destination splits into exactly `["recent", "images", "holiday.jpg"]`; `test_cli.AgeBandTests.test_the_move_line_shows_the_band` asserts the stdout line is exactly `move   holiday.jpg -> recent/images/holiday.jpg` |
| AC2 — same type, two bands, two destinations | the band is computed per file, the type folder is not | `test_planner.BandRoutingTests.test_same_type_different_bands_different_destinations`: `a.pdf` (now) → `recent/documents/a.pdf`, `b.pdf` (400 days) → `old/documents/b.pdf` in one plan |
| AC3 — age is `st_mtime` and nothing else | `now - entry.stat().st_mtime` | `test_planner.BandRoutingTests.test_age_is_the_modification_time_not_the_access_time`, with mtime and atime crossed on two files. **Mutation-checked:** changing the planner to read `st_atime` makes this test fail (see `## Gates`) |
| AC4 — two bands, boundary 365 days, boundary is `old` | `DEFAULT_BANDS` and `band_for`'s strict `<` | `test_rules.BandTableTests`: `test_there_are_exactly_two_bands_named_recent_and_old`, `test_the_boundary_is_365_days_and_the_last_band_is_unbounded` (asserts the literal `31_536_000`), `test_the_boundary_itself_is_old`, `test_one_minute_either_side_of_the_boundary`, `test_every_age_gets_a_band`. Through a folder: `test_planner.BandRoutingTests.test_the_boundary_lands_where_band_for_says` |
| AC5 — PREVIEW and APPLY agree, both components created | one `build_plan`, two callers | `test_cli.AgeBandTests.test_apply_lands_every_file_where_preview_said`: PREVIEW's `(name, destination)` set equals APPLY's, every promised path is a file afterwards, and `old/documents/` is a folder afterwards having not existed before. Also `test_apply.ApplyTests.test_destination_folders_are_created_as_needed`, which now asserts both components |
| AC6 — an unrecognised file is not aged | the `leave` return precedes the age lookup | `test_planner.BandRoutingTests.test_an_unrecognised_file_is_left_and_never_aged` (reason is exactly `no rule for '.xyz'`, no band in it); `test_cli.AgeBandTests.test_an_old_unrecognised_file_is_left_and_makes_no_band_folder` — in both modes, and neither `recent/` nor `old/` exists afterwards |
| AC7 — never-overwrite inside the band path | `_free_destination` operates on the joined path | `test_planner.BandRoutingTests.test_a_collision_inside_the_band_path_is_suffixed` (destination `old/documents/report (2).pdf`); `test_cli.AgeBandTests.test_a_collision_inside_the_band_path_never_overwrites` — the pre-existing `old/documents/report.pdf` has the same sha256 after APPLY and the same contents |
| AC8 — hidden files skipped whatever their age | the `.`-prefix check precedes everything | `test_cli.AgeBandTests.test_an_old_hidden_file_is_still_skipped_entirely`: `.hidden.jpg` at 400 days appears in neither mode's stdout and `self.listing()` is unchanged |
| AC9 — existing subfolders untouched, `old/` and `recent/` included | `entry.is_dir()` still short-circuits | `test_cli.AgeBandTests.test_pre_existing_band_and_type_folders_are_left_alone`: pre-existing `documents/`, `old/` and `recent/` each holding a file; each folder's `self.listing()` is identical before and after APPLY once this run's own destination is excluded, and no file inside any of them appears in either mode's output |
| AC10 — a file that ages after sorting is never re-filed | follows from AC9 | `test_cli.AgeBandTests.test_a_file_that_ages_after_sorting_is_never_refiled`: `recent/documents/notes.txt` aged to 400 days; no output line names it in either mode and `self.listing()` is unchanged |
| AC11 — a second APPLY is a no-op | follows from AC9 | `test_cli.AgeBandTests.test_a_second_apply_over_banded_folders_is_a_no_op`: `self.listing()` after the second APPLY equals the one after the first, and the PREVIEW between them has no move lines |
| AC12 — band folder name taken by a regular file | `_blocking_component` walks both components | `test_planner.DestinationNameTakenTests.test_band_name_taken_by_a_file_yields_leave_naming_the_band` (reason is exactly `'old' exists and is not a folder`) and `test_a_blocked_band_does_not_block_the_other_one`; `test_cli.AgeBandTests.test_a_band_name_taken_by_a_regular_file_leaves_the_files_alone` — both modes, exit status 0, nothing moved, the blocking file's sha256 unchanged |
| AC13 — `README.md` states tree, bands, field and boundary | README section "Where each file goes" | `test_rules.ExtensionTableTests.test_readme_documents_the_bands`, which parses `README.md` and checks it against `DEFAULT_BANDS`: the literal `` `<band>/<type>/<name>` ``, the phrase `last modified`, a table row per band name naming `365`, and the boundary written as `**365 days**`. **Mutation-checked:** rewording the `old` row to drop the number, or the field to "last opened", each fails it |

**AC4's "no third band name appears anywhere in either mode's output over any folder"** is a
universal claim and is not tested by exhaustion. What is tested is the reason it holds: the first
component of a destination is always `band_for`'s return value, `band_for` returns only a name from
`DEFAULT_BANDS`, and `DEFAULT_BANDS` is asserted to be exactly `["recent", "old"]`
(`test_there_are_exactly_two_bands_named_recent_and_old`, `test_every_age_gets_a_band`). `verify`
should treat that as the claim to check rather than the criterion's wording.

## Deviations from the plan

1. **AC13's test lives in `tests/test_rules.py`, not `tests/test_cli.py`.** Plan step 7 put it in
   the CLI module. `test_rules.py` already holds the README-parsing helper, `REPOSITORY_ROOT`, and
   the equivalent test for the extension table; putting AC13's test in `test_cli.py` would have
   duplicated all three in a module that imports nothing from `tidy`. What the plan asked for — the
   README parsed rather than restated, so documentation and table cannot drift — is unchanged.
2. **The plan did not mention the existing tests, and eleven of them had to change.** The suite
   asserted destinations of the form `documents/report.pdf`; the stakeholder's chosen layout makes
   those `recent/documents/report.pdf` [src: WI-0002/Q-001]. Each edit adds the band and keeps what
   the test tested — the collision fixtures move to `recent/documents/`, `DestinationNameTakenTests`
   blocks `recent/images` instead of `images`, and `test_destination_folders_are_created_as_needed`
   now asserts both components rather than one. **No assertion was weakened or deleted**, and the
   diff for each is one or two lines. This is called out because "the change made the old tests
   fail, so the old tests changed" is exactly the shape a defect hides in, and it should be read
   rather than taken on trust.
3. **One extra test beyond the plan's list: `test_the_whole_run_is_measured_against_one_instant`.**
   ADR-0005 §3 fixes the once-per-run clock and no criterion covers it; three files of equal age all
   landing in `old` is the cheapest observable that would fail if the clock moved into the loop.
4. **`tests/support.py`'s helper is `age(path, days, accessed_days_ago=None)`** — days rather than
   seconds, because every folder-level case in this item is expressed in days and the sub-day
   boundary cases are on `band_for` directly, which takes seconds and needs no folder.

Nothing in the plan's `## Approach`, its interfaces, or its decisions was departed from.

## Gates

Run on `0a1f0a8`, the last commit that touches code, tests or docs, and re-run on the branch
head (`25255b2`) after this report was committed. Identical results both times.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 63 tests ... OK` (37 before this item) |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, `checked 6 item(s), 7 document(s)`, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above; each of AC1–AC13 names at least one test function, and AC4's universal clause is discharged as stated |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 8 commit(s) on main..wi/WI-0002 name WI-0002` on the re-run at the branch head |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, 1 document checked |
| `no-unplanned-scope` (advisory) | **pass, with one thing to look at** | Every hunk in `tidy/` traces to plan steps 1–3, and `apply.py` and `cli.py` are untouched. The README and overview hunks are steps 8 and 9. The test hunks are steps 4–7 plus deviations 2 and 3 above. The one hunk that is judgement rather than a step: `README.md` gained two bullets under "What it will not do" — that a filed file is never re-filed, and that a folder tidied by the older version keeps its top-level type folders. Neither is required by AC13. They are AC10 and the accepted mixed tree, which a user meets whether or not they are written down |

**Mutation checks**, run to answer the self-check's first question rather than as a gate. Reverting
the planner to `st_atime`: 4 tests fail, including AC3's. Replacing `band_for`'s body with a
constant `"recent"`: 14 tests fail across all three test modules. Both mutations were reverted and
the suite re-run green; `git status` was clean at each step.

## What I did not do

1. **`tidy/cli.py`'s `--help` text still describes sorting by type only** — its `argparse`
   description says "chosen by file type", and its epilog says "The extension-to-folder table is in
   README.md". Both are now incomplete: a user reading `--help` is not told that age chooses a
   folder at all. This is a real, user-visible gap and it is **left open deliberately**, not
   overlooked. The plan's `## Out of scope` says any change to `cli.py` is a signal worth a question
   rather than a workaround, and no acceptance criterion covers the help text — AC13 fixes what
   `README.md` must say and nothing else. Filing a blocking question to suspend the item over a
   help string looked disproportionate against declaring it here, where `verify` and `review-close`
   both see it. **Recommendation:** a bug item against WI-0002's delivered behaviour, or a one-line
   amendment during review; it is two strings and no logic.
2. **No migration of a folder the previous version tidied.** Out of scope by the item's own list;
   `README.md` now tells the user it will not happen and why. AC9 fixes the behaviour.
3. **Symlinks are aged by their target's `mtime`,** because `entry.stat()` follows them, as
   `entry.is_dir()` already did. The plan named this as a risk and chose consistency with the
   existing behaviour; no criterion covers symlinks and none is added.
4. **Nothing was done about clock skew or copied files.** A file restored from a backup is aged by
   its original date. Inherent in the stakeholder's own framing, named in the plan's risks, and not
   a defect to fix here.
5. **`BUG-0001` and `BUG-0002` were not touched**, though this item's work is in the same two
   modules. They are separate items with their own criteria.
