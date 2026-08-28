# Verification report — WI-0001

Verified-commit: 6b1873161b148392d8ee5cb6ff5824a4ab404289

## Verdict

**Pass.** All fifteen acceptance criteria are met, each demonstrated by a command run in this
execution against the branch head, with the output quoted below. The item moves `verifying` →
`in-review`.

Two defects were found that **no criterion of this item covers**, so neither is a send-back:
BUG-0001 (an unreadable target folder dies with a Python traceback) and BUG-0002 (a wholly
successful apply exits 1 on a filesystem that refuses hard links). Both were filed at `ready`
with `found-in: WI-0001`. Both were predicted in `impl-report.md` `## What I did not do`; this
execution confirmed them by running them rather than by reading about them.

Everything below was run from the repository root on branch `wi/WI-0001`, working in
`.harness/` (git-ignored). Fixture folders are referred to by the paths used in the commands.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 -m tidy --help; echo $?` | `usage: tidy [-h] [--apply] folder` … `folder      the folder to tidy; only the files directly inside it are considered` … `--apply     actually move the files; without this flag tidy only previews and moves nothing` … `Without --apply, tidy previews only: it prints every move it would make and changes nothing on disk.` → exit `0` | `folder` is the first positional; `--apply` is the flag; preview-by-default is stated twice, in the flag help and in the epilog |
| AC2 | **pass** | `python3 -m tidy .harness/f1` over `photo.jpg report.pdf script.py notes.xyz README`, then `diff` of a recursive `(path, size, sha256)` listing before and after | `IDENTICAL`; exit `0`; `ls -a .harness/f1` shows only the five original files — no `images/`, `documents/` or `code/` | The same run as AC4. APPLY happened only when `--apply` was added: the tree changed only on that later run |
| AC3 | **pass** | same run; `grep -c '^move ' .harness/f1.out` | stdout was exactly `leave  README   [no extension]` / `leave  notes.xyz   [no rule for '.xyz']` / `move   photo.jpg -> images/photo.jpg` / `move   report.pdf -> documents/report.pdf` / `move   script.py -> code/script.py`; move-line count `3`; exit `0` | 3 recognised files → exactly 3 `move` lines, each naming the file and its destination path. The two files that would not move produce no move line |
| AC4 | **pass** | `python3 .harness/snap.py .harness/f1` before and after the bare run, then `diff` | `IDENTICAL` — same paths, same sizes, same sha256 | No destination subfolder was created; `ls -a` confirms |
| AC5 | **pass** | 59 files, one per extension in AC5's table typed by hand from `item.md` (deliberately **not** imported from `tidy/rules.py`), plus `PHOTO.JPG`; `python3 -m tidy .harness/f5` and every move line compared against the table | `expected rows: 59  got move lines: 60` / `MISMATCHES: none` / `PHOTO.JPG -> images/PHOTO.JPG` (the 60th is the case-insensitivity file) | Case-insensitive on the final extension. The README check parsed `README.md`'s table row by row against the same hand-typed copy: `README rows found: ['archives', 'audio', 'code', 'documents', 'images', 'spreadsheets', 'video']` / `DISCREPANCIES: none` — that is AC5's "stated in a file in the repository a user can read" |
| AC6 | **pass** | `python3 -m tidy .harness/f1` and `python3 -m tidy .harness/f1 --apply`; then the tree | both modes printed `leave  README   [no extension]` and `leave  notes.xyz   [no rule for '.xyz']`; after apply the tree holds `FILE README` and `FILE notes.xyz` at the top level with their original sha256 | The line starts with `leave` where a move line starts with `move`, so the two are distinguishable by the first field. Also checked with the folder holding **only** those two files (below) |
| AC7 | **pass** | `python3 -m tidy .harness/f1 --apply`; multiset of `(basename, size)` recursively before and after | `before: {('README',13),('notes.xyz',10),('photo.jpg',11),('report.pdf',10),('script.py',9)}` = `after` → `EQUAL: True`; sha256 per basename also equal; `code/`, `documents/` and `images/` created and each holding its file | On a second fixture with a collision, every previewed destination existed afterwards and every source path was gone: `DISCREPANCIES: none — every previewed destination exists and every source is gone` |
| AC8 | **pass** | preview and apply over two byte-identical fixtures, move lines compared: `diff .harness/f8.preview .harness/f8.apply`; **and** preview's printed pairs checked against what apply actually put on disk | `AC8: SETS IDENTICAL`; on the disk check, `previewed pairs: [['photo.jpg','images/photo.jpg'],['report.pdf','documents/report (2).pdf'],['sheet.csv','spreadsheets/sheet.csv'],['song.mp3','audio/song.mp3']]` → `DISCREPANCIES: none` | Checked against **disk state**, not only against the two printed outputs — see `## Defects found` note 3 for why that distinction matters |
| AC9 | **pass** | `documents/report.pdf` containing `eeeee` pre-existing, a different `report.pdf` containing `bb` at the top level; `python3 -m tidy .harness/f8b --apply` | `FILE documents/report.pdf size=6 sha=5057ae10c213` (unchanged, `cat` → `eeeee`); `FILE documents/report (2).pdf size=3` (`cat` → `bb`) | Also with `report.pdf` **and** `report (2).pdf` already present: the incoming file became `report (3).pdf` and both existing files kept their contents and sizes |
| AC10 | **pass** | the same fixture, both modes | preview: `move   report.pdf -> documents/report (2).pdf   [documents/report.pdf exists]`; apply: `move   report.pdf -> documents/report (2).pdf` | Both modes name the suffixed name, so the rename is visible before it happens |
| AC11 | **pass** | fixture with `holiday/pic.jpg`, `holiday/trip.pdf`, `holiday/nested/deep.png` and a top-level `photo.jpg`; both modes, then `diff` of a recursive listing of `holiday/` | preview and apply each printed exactly `move   photo.jpg -> images/photo.jpg`; `holiday/ IDENTICAL`; `holiday` is still a directory at the top level | No file inside the subfolder appears in either mode's output; the subfolder was neither entered nor moved |
| AC12 | **pass** | `python3 -m tidy .harness/f12 --apply` twice, listings compared, then a preview | `AC12: tree IDENTICAL after 2nd apply`; the second apply's stdout was `leave  notes.xyz   [no rule for '.xyz']` then `Nothing to do: no files to move in .harness/f12.`; the following preview printed `0` move lines and exited `0` | Both applies exited 0 |
| AC13 | **pass** | fixture with `.bashrc`, `.hidden.jpg`, `photo.jpg`; both modes; then `grep -c 'hidden\|bashrc'` over the combined output | only `move   photo.jpg -> images/photo.jpg` in each mode; grep count `0`; after apply both dotfiles are still at the top level with their original sha256 | Not even a `leave` line, as AC13 requires |
| AC14 | **pass** | `python3 -m tidy .harness/does-not-exist-xyz` and `python3 -m tidy .harness/regular.txt`, each also with `--apply` | all four: exit `2`, `stdout bytes: 0`, stderr `tidy: <path> is not a folder` naming the offending path; `regular.txt` still contains `iam a file` | Nothing on disk changed |
| AC15 | **pass** | four fixtures — empty, only a subfolder, only hidden files, already-tidy — × both modes, counting stdout lines and move lines | all eight runs: `exit=0 stdout-lines=1 move-lines=0`, the one line being `Nothing to do: no files to move in <folder>.` | The amendment clause was checked separately: over a folder holding only `notes.xyz` and `README`, both modes printed the two `leave` lines **and then** the nothing-to-do line, with 0 move lines and exit 0 — AC6 governs and is not overridden |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on `6b18731` → `Ran 37 tests in 0.037s` / `OK`, exit `0` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit `0` |
| `workspace-valid` | **pass** | `scripts/validate-workspace .` → `checked 6 item(s), 6 document(s)`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | every row of `## Criteria` names a command this execution ran and quotes its output. No row cites `impl-report.md`. AC5's expected table was typed from `item.md` rather than imported from `tidy/rules.py`, so the check cannot pass by agreeing with itself |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — every error, empty-input and boundary case named by a criterion was triggered |
| `tests-would-fail-without-the-change` (advisory) | **pass** | 13 mutations, one or more per criterion, each restored with `git checkout` — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Triggered, not read about:

1. **Missing target path**, both modes → exit 2, empty stdout, path named on stderr (AC14).
2. **Target is a regular file**, both modes → exit 2, empty stdout, path named on stderr (AC14).
3. **Empty folder**, both modes → one line, exit 0 (AC15).
4. **Folder holding only a subfolder**, both modes → one line, exit 0 (AC15).
5. **Folder holding only hidden files**, both modes → one line, exit 0 (AC15).
6. **Already-tidy folder**, both modes → one line, exit 0 (AC15).
7. **Folder holding only files AC6 leaves alone** (`notes.xyz`, `README`), both modes → two `leave`
   lines, then the nothing-to-do line, 0 move lines, exit 0. This is the fixture WI-0001/Q-001
   settled, and it is the one AC6 and AC15 were once read as disagreeing over.
8. **File with no extension at all** (`README`) → `leave  README   [no extension]`, still at its
   original path after apply (AC6).
9. **Single collision** → suffixed to `report (2).pdf`, the pre-existing file byte-identical (AC9).
10. **Double collision** — `report.pdf` *and* `report (2).pdf` already present → the incoming file
    became `report (3).pdf`; both existing files unchanged. Beyond any criterion; it confirms the
    suffix counts up rather than stopping at 2.
11. **An AC5 destination name taken by a regular file** (a file literally called `images`) → both
    modes printed `leave  photo.jpg   ['images' exists and is not a folder]` and
    `leave  images   [no extension]`, then the nothing-to-do line; exit 0; nothing moved. This is
    the case `refine` routed to `plan` and `answer-questions` decided for WI-0001/Q-002 — the
    behaviour on disk matches `plan.md` `## Assumptions` 6.
12. **Unreadable target folder** → uncaught `PermissionError` traceback, exit 1. **Defect** — see
    BUG-0001.
13. **A filesystem that refuses hard links**, simulated by making `os.link` raise
    `OSError(18, "Invalid cross-device link")` → both files moved correctly, both reported on
    stderr as fallbacks, exit **1**. **Defect** — see BUG-0002. This is the branch `plan.md`
    `## Risks` records as unreachable from the test suite.
14. **Symlinks at the top level** — a symlink to a file outside the folder, and a symlink to a
    sibling directory. The file symlink was classified by its own name and moved as a symlink; the
    directory symlink was skipped like any subfolder; the outside target was untouched. See
    `## Defects found` note 2.
15. **`PHOTO.JPG`** — uppercase extension → `images/PHOTO.JPG` (AC5).

## Test sensitivity check

Thirteen behaviours were removed one at a time from the branch head, the suite re-run, and the
file restored with `git checkout --`. Every criterion has at least one test that bites.

| behaviour removed | suite result |
|-------------------|--------------|
| the whole `--help` epilog **and** the `--apply` help text (AC1) | FAILED — `test_cli.HelpAndModeTests.test_help_names_folder_apply_and_default` |
| the `--apply` guard in `cli.main`, so it always applies (AC2, AC4) | FAILED (4 failures) |
| printing `leave` lines — iterate `moves` instead of `actions` (AC3, AC6) | FAILED (4 failures) |
| `.png` moved from `images` to `documents` in `DEFAULT_RULES` (AC5) | FAILED (1 failure) |
| `.lower()` in `extension_of`, so matching becomes case-sensitive (AC5) | FAILED (1 failure) |
| `os.makedirs` in `apply_plan` (AC7) | FAILED (5 failures) |
| applying only the first action, `apply_plan(folder, actions[:1])` (AC8) | FAILED — `test_apply_lands_every_destination_and_loses_nothing`, `test_second_apply_is_a_no_op` |
| collision suffixing in `_free_destination` (AC9, AC10) | FAILED (3 failures, 1 error) |
| the subfolder skip in `build_plan` (AC11, AC12) | FAILED (4 failures, 4 errors) incl. `test_subfolders_are_neither_listed_nor_entered`, `test_subfolder_and_contents_are_untouched`, `test_nothing_to_do_cases`, `test_an_already_tidy_folder_has_nothing_to_do` |
| the hidden-file skip in `build_plan` (AC13) | FAILED (3 failures) |
| `return 2` → `return 0` for a bad target (AC14) | FAILED (4 failures) |
| the nothing-to-do line (AC15) | FAILED (6 failures) |

`git status` was clean after the run and the suite green again: `Ran 37 tests … OK`.

## Defects found

**BUG-0001 — a folder tidy cannot read crashes with a Python traceback instead of a message.**
Filed at `ready`, `found-in: WI-0001`, priority medium. `os.scandir` raises `PermissionError` out
of `build_plan` and nothing catches it; both modes print a traceback and exit 1. AC14 covers a
missing path and a regular file only, so no criterion of this item says the behaviour should be
different — which is why it is a bug and not a send-back.

**BUG-0002 — a fully successful apply exits 1 on a filesystem that refuses hard links.** Filed at
`ready`, `found-in: WI-0001`, priority medium. `apply_plan` returns ADR-0003's fallback note in
the same list it uses for genuine failures, and `cli.main` ends `return 1 if failures else 0`.
ADR-0003 assigns a non-zero exit to `FileExistsError` only and describes the fallback as still
satisfying AC9; `README.md` says exit 1 means "some file could not be moved while others were".
No criterion of this item constrains the exit status of a successful APPLY.

Three further observations, none of them a defect and none blocking:

1. **`impl-report.md`'s symlink claim is wrong in one detail.** It states that for a symlink
   "`os.link` follows the symlink by default, so what lands at the destination is a hard link to
   the target rather than the link". On Linux it does not: `ls -l` after the run shows
   `images/link.png -> ../outside/target.png`, still a symlink. The user-visible consequence is
   different from the one recorded — a *relative* symlink is silently broken by being moved a level
   deeper, rather than being replaced by a hard link. No criterion mentions symlinks, and `mv` has
   the same effect on a relative symlink, so this is recorded rather than filed. It is worth
   correcting in the record because WI-0003 may make symlinks reachable in new ways.
2. **AC8's named test is weaker than AC8.** `test_cli.ApplyTests.test_apply_matches_the_preview_it_printed`
   compares the *printed* output of a preview run with the *printed* output of an apply run. Both
   are produced by the same `render` loop before `apply_plan` is called, so an apply that silently
   moved nothing would still pass it — as the AC8 mutation above demonstrates: it broke
   `test_apply_lands_every_destination_and_loses_nothing` (AC7's test) and left AC8's own test
   green. The criterion is genuinely met — this verification checked preview's pairs against disk
   state directly — but the suite's coverage of AC8 rests on AC7's test rather than on the one
   `plan.md`'s mapping table names for it.
3. **`python3 -m tidy` only runs from the repository root.** There is no install step, no entry
   point and no `PYTHONPATH` handling, so `cd`-ing into the folder being tidied and running the
   tool gives `No module named tidy`. This is exactly what ADR-0001 chose and no criterion
   requires otherwise; it is noted because "a command typed in a terminal" reads as more portable
   than it is, and packaging is a candidate future item rather than a defect in this one.

## Not verified, and why

- **ADR-0003's fallback on a real filesystem that refuses hard links.** It was exercised by
  patching `os.link` to raise `OSError(18)`, which reaches the real branch in `apply_plan` and the
  real return in `cli.main` — that is how BUG-0002 was found. What was *not* exercised is the
  behaviour on an actual exFAT, FAT32, SMB or NFS mount, because this environment cannot create
  one. In particular, `shutil.move`'s own behaviour there (permissions, metadata, partial copies on
  a full volume) is unverified, and AC9's never-overwrite guarantee on such a filesystem rests on
  the check-then-move of the fallback rather than on the kernel.
- **Concurrent modification of the folder between planning and applying.** `apply_plan`'s
  `FileExistsError` branch is what handles it, and `plan.md` `## Risks` accepts the mental-model
  gap. Provoking a genuine race needs a second process interleaved with the run, which was not
  attempted; `test_apply.NeverOverwriteTests.test_link_refuses_an_existing_destination` covers the
  branch with a fabricated action, but that is the suite's evidence, not this execution's.
- **Scale.** No fixture exceeded 60 files. `plan.md` `## Risks` accepts the in-memory action list
  for the folder sizes the vision describes, and no criterion mentions scale, so nothing was run
  against a folder large enough to test it.
- **Non-Linux platforms.** Everything here was run on Linux with Python 3.13 on ext4. macOS and
  Windows behaviour — case-insensitive filesystems in particular, where `PHOTO.JPG` and `photo.jpg`
  would collide in a way AC9's suffix rule has never been tested against — is unverified. No
  criterion names a platform.
- **The stakeholder's own judgement of the output wording.** AC3, AC6 and AC10 constrain what each
  line must *contain*; `plan` chose how each reads. The lines satisfy the criteria, and whether a
  user finds `leave  notes.xyz   [no rule for '.xyz']` clear is not something `verify` can settle.
  `review-close` and the epic sign-off are where that belongs.
