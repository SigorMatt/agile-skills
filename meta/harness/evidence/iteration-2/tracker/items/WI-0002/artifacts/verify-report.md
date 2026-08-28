# Verification report — WI-0002

Verified-commit: 93a958599cdfe10c81dfba337d62811e23db564c

## Verdict

**Pass.** All thirteen acceptance criteria are met, each demonstrated by a command run in this
execution against the branch head, over fixtures built by this skill rather than by the project's
test suite (`.verify-scratch/fix.py`, an `os.utime`-based builder written here and independent of
`tests/support.py`). One defect in behaviour delivered elsewhere was found and filed as
**BUG-0003** — `--help` still describes destinations as chosen by file type alone. No WI-0002
criterion covers the help text, so it is a bug rather than a send-back.

## Criteria

Ages below are set with `os.utime` relative to an instant captured before the run. `PREVIEW` is
`python3 -m tidy <folder>`, `APPLY` adds `--apply`. Full transcripts are the commands' actual
stdout, quoted.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — destination is exactly `<band>/<type>/<name>` | **pass** | fixture `.verify-scratch/ac1` with `holiday.jpg` at mtime now; `python3 -m tidy .verify-scratch/ac1` | `move   holiday.jpg -> recent/images/holiday.jpg` | The string matches the criterion character for character, three spaces included. Three components confirmed again over the four-file AC5 fixture, where every move line had exactly three. |
| AC2 — same type, two bands, two destinations | **pass** | `a.pdf` mtime now, `b.pdf` mtime 400 days; PREVIEW | `move   a.pdf -> recent/documents/a.pdf` / `move   b.pdf -> old/documents/b.pdf` | Both in one plan, one run. |
| AC3 — age is `st_mtime` and nothing else | **pass** | `mnow-a400.pdf` (mtime now, atime 400d) and `m400-anow.pdf` (mtime 400d, atime now); PREVIEW | `move   m400-anow.pdf -> old/documents/m400-anow.pdf` / `move   mnow-a400.pdf -> recent/documents/mnow-a400.pdf` | Timestamps printed from `os.stat` before the run to prove they were crossed. A tool reading `st_atime` would place them the other way round; the mutation below confirms it. |
| AC4 — two bands, boundary 365 days, boundary is `old` | **pass** | (a) three files at 365d, 365d−60s, 365d+60s; PREVIEW. (b) `band_for` called directly for the exact boundary, which a folder fixture cannot pin because the run reads its own clock | (a) `exactly-365.pdf -> old/…`, `over-by-a-minute.pdf -> old/…`, `under-by-a-minute.pdf -> recent/…`. (b) `DEFAULT_BANDS = (('recent', 31536000), ('old', None))`; `band_for(31535999.999)='recent'`, `band_for(31536000)='old'`, `band_for(31536060)='old'`, `band_for(-1e9)='recent'`, `band_for(1e12)='old'` | The bound is the literal 31 536 000. "No third band name appears anywhere in either mode's output over any folder" is universal and was not tested by exhaustion; it was decided by its grounds — the first component of every destination is `band_for`'s return, `band_for` returned only `recent` or `old` over a sweep of ages from 0 to 3 × 365 days, and `DEFAULT_BANDS` has exactly those two names. |
| AC5 — PREVIEW and APPLY agree; both components created | **pass** | four files spanning both bands and three type folders; PREVIEW, then APPLY on the unchanged folder | PREVIEW and APPLY printed the identical four move lines; `find` afterwards shows every file at exactly the path PREVIEW named | `ls` before the APPLY confirmed neither `old/` nor `recent/` existed (`No such file or directory` for both); `old/documents/song.mp3` and `old/documents/taxes.pdf` exist afterwards. |
| AC6 — an unrecognised file is not aged | **pass** | `notes.xyz` and `LICENSE`, both at 400 days; PREVIEW and APPLY | both modes: `leave  LICENSE   [no extension]` / `leave  notes.xyz   [no rule for '.xyz']` / `Nothing to do…`, exit 0 | No band string in either line. `find` after APPLY shows only the two original files — no `old/` was created. |
| AC7 — never-overwrite inside the band path | **pass** | `report.pdf` at 400 days beside a pre-existing `old/documents/report.pdf` of different contents; PREVIEW then APPLY | both modes: `move   report.pdf -> old/documents/report (2).pdf   [old/documents/report.pdf exists]` | The pre-existing file's sha256 is `b4b4a381…d052d2cb` and size 39 both before and after APPLY, and its contents still read `PRE-EXISTING CONTENTS, different length`; the incoming file is in `report (2).pdf`. |
| AC8 — hidden files skipped whatever their age | **pass** | `.hidden.jpg` at 400 days beside `visible.jpg` at 1 day; PREVIEW and APPLY | both modes printed one line only: `move   visible.jpg -> recent/images/visible.jpg` | `.hidden.jpg` is still at its original path after APPLY. |
| AC9 — pre-existing subfolders untouched, `old/` and `recent/` included | **pass** | pre-existing `documents/leftover.pdf`, `old/documents/already-filed.pdf`, `recent/images/already-filed.jpg`, plus a top-level `newthing.jpg`; recursive listing with per-file size and content hash before and after APPLY | output in both modes was one line, `move   newthing.jpg -> recent/images/newthing.jpg`; `documents` and `old` listings byte-identical before and after; `recent` differs only by `images/newthing.jpg`, this run's own destination | All three folders still at the same paths. No file inside any of them appears in either mode's output. |
| AC10 — a file that ages after sorting is never re-filed | **pass** | `recent/documents/notes.txt` aged to 400 days (mtime age printed as 400.0 days); PREVIEW and APPLY | both modes: `Nothing to do: no files to move in .verify-scratch/ac10.`, exit 0 | No output line names `notes.txt`; the recursive listing is identical after APPLY; no `old/` was created. |
| AC11 — a second APPLY is a no-op | **pass** | APPLY, capture listing, PREVIEW, APPLY again | APPLY #1 moved `holiday.jpg` and `taxes.pdf`; the PREVIEW between printed 0 lines beginning `move ` (only the `notes.xyz` leave line and `Nothing to do…`); APPLY #2 the same | Listing after the second APPLY equals the listing after the first, hashes included. |
| AC12 — band folder name taken by a regular file | **pass** | exactly the criterion's fixture: a regular file `old` and `taxes.pdf` at 400 days; PREVIEW and APPLY | both modes: `leave  old   [no extension]` / `leave  taxes.pdf   ['old' exists and is not a folder]` / `Nothing to do…`, exit **0** | The reason names `old`. Nothing moved. The blocking file's sha256 and size are unchanged. Exit 0 matches the control run (a folder holding only `notes.xyz`), which also exits 0. Extra boundary run: with `old/documents` a regular file, `taxes.pdf` gets `['old/documents' exists and is not a folder]` — the check walks both components. |
| AC13 — `README.md` states tree, bands, field and boundary | **pass** | read `README.md` and compared against AC1, AC3 and AC4 | §"Where each file goes": ``Every file that moves ends up at `<band>/<type>/<name>` ``; §"The band": "how long ago it was **last modified** — its `mtime` … when you last opened it does not count"; the band table gives `recent` = "less than **365 days** ago" and `old` = "**365 days** ago or longer"; "There are two bands and no others" | It is the same file the extension table lives in, as the criterion requires. |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on `93a9585` → exit 0, `Ran 63 tests in 0.056s` / `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, `checked 6 item(s), 7 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | every row of `## Criteria` names a command run in this execution over a fixture built here. No row cites `impl-report.md`. |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` |
| `tests-would-fail-without-the-change` (advisory) | **pass, with one weakness** | see `## Test sensitivity check` |

The gate results match `impl-report.md`'s, which is a check of that report rather than a
substitute for one: the report claimed `Ran 63 tests … OK` and this execution reproduced it on
the branch head.

## Negative and boundary cases exercised

Each was triggered, not read about.

1. **The 365-day boundary itself** (AC4) — a file exactly 365 days old lands in `old`; one minute
   under lands in `recent`; one minute over lands in `old`. Also `band_for(31535999.999)` →
   `recent` and `band_for(31536000)` → `old`, which is the boundary the folder fixture cannot pin.
2. **A file with an unrecognised extension, and a file with none at all** (AC6) — `notes.xyz` and
   `LICENSE`, both aged 400 days: `leave` in both modes, no band folder created.
3. **A destination that is already taken** (AC7) — a pre-existing `old/documents/report.pdf` of
   different size and contents; verified unchanged by sha256 after APPLY.
4. **A band folder's name taken by a regular file** (AC12) — and, beyond the criterion, the *type*
   component taken by a regular file inside a band (`old/documents` as a file), which produces
   `['old/documents' exists and is not a folder]`.
5. **A folder with nothing to move** — the AC12 control: only `notes.xyz`, prints
   `Nothing to do…`, exit 0.
6. **An empty folder** — `Nothing to do: no files to move in .verify-scratch/empty.`, exit 0.
7. **A folder that does not exist** — `tidy: .verify-scratch/nope is not a folder`, exit 2, which
   is `README.md`'s documented contract.
8. **A file dated in the future** — mtime 30 days ahead: `recent`, as `plan`'s assumption 6 says.
   No criterion constrains it; it is recorded because it was run.
9. **Three files of identical age either side of nothing** — all at 365 days + 1 second, all three
   land in `old`, which is the observable of ADR-0005's read-the-clock-once rule.
10. **A symlink** — `link.pdf` pointing at a future-dated file is aged by its target and moved.
    Declared behaviour (`impl-report.md` §3 of "What I did not do"); no criterion covers it and
    none is added here.

## Test sensitivity check

Every mutation below was applied to the working tree, the suite run, and the tree restored with
`git checkout --`; `git status --porcelain` showed only the untracked scratch directory after each,
and the suite was green again before the next.

| mutation | criteria it should break | tests that failed |
|----------|--------------------------|-------------------|
| `entry.stat().st_mtime` → `st_atime` | AC3 | 4, including `test_planner.BandRoutingTests.test_age_is_the_modification_time_not_the_access_time` |
| `band_for` always returns the first band | AC1, AC2, AC4 | 15, including `test_rules.BandTableTests.test_the_boundary_itself_is_old` and `test_one_minute_either_side_of_the_boundary` |
| destination drops the band component | AC1, AC2, AC5, AC7 | 25, including `test_cli.AgeBandTests.test_apply_lands_every_file_where_preview_said` and `test_a_collision_inside_the_band_path_never_overwrites` |
| `band_for`'s `<` → `<=` (boundary becomes `recent`) | AC4 | 1: `test_rules.BandTableTests.test_the_boundary_itself_is_old` |
| unrecognised files routed to a `misc` folder and aged | AC6 | 14, including `test_planner.BandRoutingTests.test_an_unrecognised_file_is_left_and_never_aged` and `test_cli.AgeBandTests.test_an_old_unrecognised_file_is_left_and_makes_no_band_folder` |
| `_blocking_component` checks the full path only, not each component | AC12 | 4, including `test_planner.DestinationNameTakenTests.test_band_name_taken_by_a_file_yields_leave_naming_the_band` |
| the `name.startswith(".")` skip removed | AC8 | 6, including `test_cli.AgeBandTests.test_an_old_hidden_file_is_still_skipped_entirely` |
| the planner recurses into every subfolder | AC9, AC10, AC11 | 15, including `test_pre_existing_band_and_type_folders_are_left_alone`, `test_a_file_that_ages_after_sorting_is_never_refiled` and `test_a_second_apply_over_banded_folders_is_a_no_op` |
| `README.md`'s `old` row loses the number | AC13 | 1: `test_rules.ExtensionTableTests.test_readme_documents_the_bands` |
| `README.md` loses the `` `<band>/<type>/<name>` `` shape | AC13 | 1: the same test |

Every criterion has at least one test that fails when its behaviour is removed. Two findings about
the tests, neither of which changes a verdict:

- **AC13's "age is the last-modified time" clause is only weakly covered.** The test asserts
  `assertIn("last modified", readme)` over the whole file, and `README.md` contains that phrase
  three times. Rewording the sentence a user actually reads —
  `**last modified**` → `**last opened**` on line 43 — leaves the suite **green** (`Ran 63 tests …
  OK`, exit 0); only replacing all three occurrences fails it. `impl-report.md` claims this exact
  mutation fails the test ("rewording … the field to 'last opened'"); it does not. The criterion
  itself passes — the README does state the field — so this is a note on the regression net, not a
  defect in the delivered behaviour, and it is left as an observation rather than filed.
- **The first, shallower attempt at the subfolder mutation** (entering one level only) did not fail
  AC10's or AC11's tests, because both fixtures put the file two levels down. The fully recursive
  mutation, recorded above, fails all three. Recorded so that nobody re-derives it.

## Defects found

**BUG-0003 — `--help` still says destinations are chosen by file type alone.** `python3 -m tidy
--help` prints "Sort the files sitting directly in a folder into subfolders chosen by file type."
and "The extension-to-folder table is in README.md." Both were true before this item and are false
or incomplete after it: age chooses the top-level folder and there are now two rule tables.

Classified as a bug rather than a send-back by the SKILL's test: no WI-0002 acceptance criterion
says the help text should be different. AC13 fixes what `README.md` must say and nothing else, and
WI-0001 AC1 — the only criterion about `--help` — requires it to name the folder argument, the
apply flag, and the preview default, all of which it still does. `found-in: WI-0002` names the item
whose delivered behaviour the text contradicts: the string is WI-0001's, but it describes WI-0002's
routing, and it is wrong only on this branch.

`impl-report.md` declared this gap under `## What I did not do` and recommended exactly this
disposition. Verifying it did not consist of reading that declaration: the help output was run and
compared against WI-0001 AC1's wording and against the tool's actual behaviour.

No other defect was found. In particular, `git diff main..wi/WI-0002 --stat` confirms
`tidy/apply.py` and `tidy/cli.py` are untouched, and every hunk in `tidy/`, `README.md` and
`docs/architecture/overview.md` traces to a plan step (1–3, 8, 9). BUG-0001 and BUG-0002 remain
open against other behaviour and were not re-tested here.

## Not verified, and why

1. **AC4's universal clause — "no third band name appears anywhere in either mode's output over
   any folder"** — is not decidable by exhaustion and was not exhausted. It was decided by its
   grounds instead (see the AC4 row). A band name could in principle reach stdout by a route other
   than a destination's first component; no such route exists in `cli.py`'s `render`, which was
   read, but this is an argument rather than a measurement.
2. **The exact 365-day boundary at folder level.** `build_plan` reads its own clock, so a fixture
   cannot make a file exactly 31 536 000 seconds old at the instant the run measures it. The
   folder-level case is therefore boundary-plus-epsilon, and the exact point was settled by calling
   `band_for(31536000)` directly. Both are recorded in the AC4 row.
3. **Filesystems other than the one this repository sits on.** Timestamps were set with `os.utime`
   and read back to confirm they took; a filesystem with coarse or absent mtime resolution was not
   tried. BUG-0002 is the open item about a filesystem that behaves differently.
4. **Clock skew, backups and copied files.** `plan`'s risks name these; no criterion constrains
   them and nothing here exercised them.
5. **Symlink and permission behaviour beyond the single case in `## Negative and boundary cases`.**
   No criterion covers symlinks; unreadable folders are BUG-0001's subject and were not re-run.
6. **Whether `docs/architecture/overview.md` v3 is complete and correct.** It was read as part of
   the diff review and its two corrected statements match the code, but a document's completeness
   is `review-close`'s D7 check, not a criterion of this item.
