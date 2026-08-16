# Verification report — BUG-0001

Verified-commit: 4bf2cba5a4ccb7f2a97d10183cd60a66bf375001

Branch `wi/BUG-0001`, head `4bf2cba`; the last code commit under it is `06fc185`, and the two
commits after it touch only `tracker/`. Fixtures were built fresh under `/tmp/vbug1-ZITq/` — **not**
the `/tmp/bug1a`, `/tmp/bug1b`, `/tmp/bug1c`, `/tmp/bug1d` folders the item names and `implement`
reused, so that a fixture left in a helpful state by an earlier step could not flatter the result.
Criteria were read before the implementation report, with AC6 read in the form `Q-002` left it.

## Verdict

**Pass — all six criteria.** Each was decided by a command run here against a fixture built here.
No defect found, no bug filed, nothing sent back. The fix is eleven lines and the boundary it draws
— an entry that cannot be *resolved* is silent, a file that cannot be *read* still speaks, the
folder's own failure still exits 2 — holds under all four mutations tried.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | a fresh folder with `ok.txt` (3 lines) and the loop `q → p → q`; `python3 $L $F \| cat -A` | `3  ok.txt$` / `3  total$`, stderr **0 bytes**, exit 0 | the criterion's exact expected output. Before the fix this folder produced empty stdout, `linecount: <folder>: Too many levels of symbolic links` and exit 2 |
| AC2 | **pass** | `ok.txt` (3 lines) and `ln -s self self` | `3  ok.txt$` / `3  total$`, stderr 0 bytes, exit 0 | the single-link form of the same trigger |
| AC3 | **pass** | a `chmod 000` `vault/` holding `hidden.txt`, a symlink `into-vault` pointing into it, and `ok.txt` (2 lines) | `2  ok.txt$` / `2  total$`, stderr **empty**, exit 0 | the readable file is counted, the folder is not blamed, and nothing is said about `into-vault` — ADR-0006's choice of silence, which AC3 explicitly leaves to `plan`. Run as uid 1000 |
| AC4 | **pass** | a folder with `target.txt` (6), `link.txt` → it, `dirlink` → a real directory, `broken` → nothing | ` 6  link.txt$` / ` 6  target.txt$` / `12  total$`, stderr 0 bytes, exit 0 | WI-0001 AC7's three named cases behave exactly as they did: the link listed under its own name with its target's count, the directory link and the broken link ignored |
| AC5 | **pass** | `mkdir noread; chmod 000 noread; python3 $L .../noread`; plus a missing path and a regular file | stdout **0 bytes**, stderr exactly one line — `linecount: /tmp/vbug1-ZITq/ac5/noread: Permission denied` — exit **2**. Missing path → `No such file or directory`, exit 2; regular file → `Not a directory`, exit 2 | the folder's own failure still reaches `main`'s handler. This is the criterion the fix could most easily have broken, and mutation 4 below shows the test would catch it |
| AC6 | **pass** | `git show 6d1e437:linecount.py > linecount.py`, then `python3 -m unittest discover`; restored afterwards. Then the suite on the branch head | at `6d1e437`: **exit 1**, failing `test_ac1_symlink_loop_does_not_abort_the_listing`, `test_ac2_self_referential_symlink`, `test_ac3_symlink_into_an_untraversable_directory`. On the branch head: `Ran 50 tests in 1.438s`, `OK`, exit 0 | AC6 as scoped by `Q-002`: the tests for AC1, AC2 and AC3 each fail against the old code. I re-ran this myself rather than accepting `impl-report.md`'s copy of it. The AC5 test passes at `6d1e437`, as AC6 no longer requires otherwise and as AC5's own meaning demands |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | run here on the branch head: `Ran 50 tests in 1.438s`, `OK`, exit 0 |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` (hard) | **pass** | six rows above, each a command run here against a fixture built here, in a directory the earlier steps never touched |
| `negative-cases-exercised` (hard) | **pass** | six conditions triggered on a real filesystem — see below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | four mutations, all caught; table below |

## Negative and boundary cases exercised

1. **Symlink loop** (`q → p → q`) → ignored, the readable file still counted, exit 0.
2. **Self-referential symlink** (`self → self`) → same.
3. **Symlink into a `chmod 000` directory** → ignored silently, exit 0, folder not named.
4. **Symlink to a directory, and a broken symlink** → ignored, as WI-0001 AC7 always required.
5. **A `chmod 000` folder**, as uid 1000 → empty stdout, one stderr line, exit 2. Also a missing
   path and a regular-file path, both exit 2.
6. **A `chmod 000` *file* inside a readable folder** (ADR-0002's case, not this bug's) →
   `5  a.txt` / `5  total` on stdout, `linecount: secret.txt: Permission denied` on stderr, exit 0.
   This is the boundary ADR-0006 draws, and it still holds: an entry that cannot be **resolved** is
   silent, a file that cannot be **read** is reported.

## Test sensitivity check

Each mutation was applied to `linecount.py`, the suite run, and the file restored; `git status`
clean afterwards. **Four mutations, four caught.**

| mutation | caught by |
|----------|-----------|
| the code as it stood at `6d1e437` (AC6's own demonstration) | the AC1, AC2 and AC3 tests |
| the `try`/`except` removed from today's file | the same three |
| `except OSError` narrowed to `except FileNotFoundError` — the error `DirEntry.is_file` already swallows, so the catch becomes a no-op | the same three; a too-narrow catch is not silently accepted |
| the catch **widened** to wrap `os.scandir` itself, so the folder's own failure returns an empty listing | `test_ac5_an_unreadable_folder_still_exits_2`, plus WI-0001's `test_ac11_folder_that_cannot_be_read`, `test_ac11_path_that_does_not_exist` and `test_ac12_path_is_a_regular_file` |

The fourth is the one worth keeping. It is the way this fix could plausibly have been written
wrong — one `try` a few lines higher up — and it turns AC5's "unchanged" test, which passes on
both sides of the fix and therefore looks redundant, into the guard that catches it. `Q-002`
argued for keeping that test required; this is the measurement behind that argument.

## Diff review against the plan

`git diff main..wi/BUG-0001 --stat -- linecount.py tests/` → `linecount.py` +18/−3,
`tests/test_linecount.py` +64/−0. Every hunk traces to plan step 1 (the `try`/`except` and the
docstring naming ADR-0006) or step 2 (the appended `UnresolvableEntryTest`). The test file's diff
contains **0** deleted lines, so WI-0001's and WI-0002's tests are untouched and all 46 of them are
in the passing run. Nothing anticipates BUG-0002 or BUG-0003: `format_report`, `main`'s `not rows`
branch and the printing path are byte-identical to `main`.

## Defects found

None. No criterion of this item failed. Nothing was found in behaviour delivered by another item —
and specifically, BUG-0002's symptom is **unchanged** by this fix, which is correct: a folder whose
entries are now all silently ignored still prints `no files`, exactly as `impl-report.md` declares
under `## What I did not do`. That is BUG-0002's, and filing it again here would duplicate an open
item.

## Not verified, and why

- **Lint.** No lint command exists (ADR-0003); the eleven changed lines were read at review and by
  no tool.
- **Entries that are neither file, directory nor symlink** — a socket or device node. `is_file()`
  returns `False` for them without raising, so they take neither the old path nor the new one; no
  criterion mentions them and `impl-report.md` declares the gap.
- **Non-POSIX platforms.** Every fixture here uses symlinks and Unix permissions. Unchanged from
  WI-0001.
- **A symlink loop deeper than the kernel's `ELOOP` limit in an unusual filesystem.** Only ext4 was
  exercised; the error is the kernel's to raise and the code does not inspect it.
- **Whether silence is the right answer for AC3's case.** ADR-0006 decided it and AC1 forces it for
  the loop case; a user who wants such entries reported would need a new criterion, not a defect
  report. Named here because it is the one visible behaviour in this fix that a reasonable person
  might want different.
