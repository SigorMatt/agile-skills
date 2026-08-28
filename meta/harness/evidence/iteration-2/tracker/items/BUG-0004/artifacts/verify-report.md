# Verification report — BUG-0004

Verified-commit: ab644840c026e5f546128dd1700102539824000d

## Verdict

**Pass.** All four acceptance criteria are met, each demonstrated by a command run here rather
than by reading `impl-report.md`. The item goes to `in-review`.

Every criterion was decided from the criterion's own wording first, against the fixture the item
itself specifies in `## Steps to reproduce`, before the implementation report was opened. The
report's claims were then checked and each one held, including the revert experiment behind AC4,
which was re-run here rather than quoted.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — either mode still reports every other file in the folder | **pass** | `mkdir -p /tmp/v4 && echo x > /tmp/v4/photo.jpg && ln -s /tmp/v4/gone.pdf /tmp/v4/broken.pdf` then `python3 -m tidy /tmp/v4` and `python3 -m tidy /tmp/v4 --apply`, each with stdout and stderr captured to separate files | Both runs, stdout: `leave  broken.pdf   [cannot be examined: No such file or directory]` / `move   photo.jpg -> recent/images/photo.jpg`. Neither run aborted. After `--apply`, `find /tmp/v4 \| sort` → `/tmp/v4/broken.pdf`, `/tmp/v4/recent/images/photo.jpg` | The item's own reproduction steps, run verbatim. stdout names `photo.jpg` in both modes, which is what AC1 asks. Measured on disk as well as in the output: `photo.jpg` really moved, and `ls -l /tmp/v4/broken.pdf` shows the dangling symlink still in the top level, untouched |
| AC2 — no output states or implies the folder could not be read | **pass** | `grep -c 'cannot be read' <file>` and `grep -c 'Traceback' <file>` over all four captured streams (`/tmp/v4.out`, `/tmp/v4.err`, `/tmp/v4a.out`, `/tmp/v4a.err`) | `0` for all eight greps | Checked on both streams of both modes separately, which is what the criterion says ("stdout or stderr"). The only stderr content is the mode banner. The false sentence the bug reported came from `cli.py`'s target-level handler, which this fixture no longer reaches |
| AC3 — the exit status is one `README.md` documents, and `README.md` says which case | **pass** | `python3 -m tidy /tmp/v4; echo $?` → `0`; `python3 -m tidy /tmp/v4 --apply; echo $?` → `0`; then `grep -n -A5 'Exit status' README.md` | `exit=0` in both modes. `README.md:34` reads "Exit status is 0 on success — including when there was nothing to do, and when some files were left where they are" | The run left one file where it was and moved another, and the sentence names that case. Read the two halves against each other rather than checking only that the status is documented somewhere: the status is 0, and the document's `0` clause is the one this run belongs to |
| AC4 — a regression test builds the fixture, asserts AC1 and AC2, fails when the handling is removed, and skips where symlinks cannot be created | **pass** | Read `tests/test_cli.py` `UnexaminableEntryTests` and `tests/test_planner.py` `UnexaminableEntryTests` in the diff; then reverted the fix myself — `git checkout main -- tidy/planner.py`, `rm -rf tidy/__pycache__ tests/__pycache__`, `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t .` — and restored with `git checkout wi/BUG-0004 -- tidy/planner.py` | Reverted: `Ran 72 tests ... FAILED (failures=3, errors=2)`, and the five entries are exactly the three new tests — `test_a_dangling_symlink_does_not_cost_the_rest_of_the_folder` (both subtests plus its on-disk assertion) and the two planner tests. The other 69 were untouched. Restored: `grep -c _unexaminable_reason tidy/planner.py` → `2`, `git status --short` → empty, `Ran 72 tests ... OK` | The test builds `photo.jpg` alongside a dangling `broken.pdf` (AC4's fixture), asserts a move line naming `photo.jpg` in both modes (AC1) and the absence of `cannot be read` and `Traceback` from both streams (AC2). The skip is `os.symlink` inside a `try` calling `self.skipTest` on `OSError`, `NotImplementedError` or `AttributeError` — gated on the operation failing, not on a platform name, so it will skip rather than fail where symlinks cannot be made. The revert was confirmed to be in the file (`grep -c _unexaminable_reason` → `0`) before the run, and bytecode caches were cleared, so the failure is the code's and not a stale `.pyc` |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` at `ab64484` with caches cleared and `PYTHONDONTWRITEBYTECODE=1` → exit 0, `Ran 72 tests in 0.062s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0, no output |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 9 item(s), 11 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | Every row of the table above names a command run in this execution and quotes its real output. No row cites `impl-report.md`. AC4's revert experiment was re-run here rather than taken from the report |
| `negative-cases-exercised` | **pass** | Six conditions triggered, below — the loop, the all-unexaminable folder, the unexaminable entry with no rule, the two resolvable symlink shapes, and the three target-level failures ADR-0006 owns |
| `tests-would-fail-without-the-change` (advisory) | **pass** | The revert experiment in AC4's row: three tests fail against `main`'s `tidy/planner.py` with the new tests in place, and the 69 pre-existing ones are unaffected in both directions |

## Negative and boundary cases exercised

1. **A symlink loop** — the second member of the class, which raises `ELOOP` from `entry.is_dir()`
   one call before any `stat()`, so a guard written around `stat()` alone would have left it
   aborting while every criterion passed. `ln -s /tmp/b1/loop.pdf /tmp/b1/loop.pdf` beside an
   ordinary `photo.jpg`, then `python3 -m tidy /tmp/b1`:

   ```
   leave  loop.pdf   [cannot be examined: Too many levels of symbolic links]
   move   photo.jpg -> recent/images/photo.jpg
   ```
   exit `0`. No criterion names this case; `plan`'s `## Risks` asked for it to be checked in
   verification, and it is handled by the same guard.

2. **Every entry unexaminable.** `/tmp/b2` holding only `a.pdf` and `b.jpg`, both dangling. Both
   modes print a `leave` line for each and then `Nothing to do: no files to move in /tmp/b2.`,
   exit `0`, and `find` shows both links still in place after `--apply`. Nothing moved, nothing
   was lost, and no stream mentions the folder being unreadable.

3. **An unexaminable entry whose extension has no rule** — the case that must *not* reach the new
   guard, because WI-0002 AC6 says an unrecognised file is never aged. `/tmp/b3` holding a
   dangling `broken.xyz` and a dangling extensionless `noext`:
   `leave  broken.xyz   [no rule for '.xyz']` and `leave  noext   [no extension]`, exit `0`. The
   pre-existing reasons still win, so the guard has not been pulled up above the extension check.

4. **Symlinks whose targets exist**, in both shapes, since the guard now wraps `entry.is_dir()`.
   `/tmp/b6` with `dirlink -> realdir` and `filelink.jpg -> target.jpg`: the directory link is
   still skipped silently as a directory, and the file link is still moved and still aged by its
   target — `move   filelink.jpg -> recent/images/filelink.jpg`, exit `0`. Unchanged from before
   the item, which is what `plan`'s out-of-scope list requires.

5. **The destination-collision path** — the case `plan`'s "the guard can be written too widely"
   risk is about. `/tmp/b7` with `report.pdf` and a *file* named `recent/documents` in the way:
   `leave  report.pdf   ['recent/documents' exists and is not a folder]`, exit `0`. The collision
   reason is still reported as itself and has not been flattened into `cannot be examined`. The
   diff confirms why: the `try` closes after `band = band_for(...)`, and `_blocking_component` is
   below the `except`.

6. **ADR-0006's target-level boundary, which this item had to leave alone.** All three of its
   cases still behave exactly as BUG-0001 left them: a folder that does not exist →
   `tidy: /tmp/does-not-exist-zz is not a folder`, exit `2`; a target that is a file →
   `tidy: /tmp/afile.txt is not a folder`, exit `2`; a folder at mode `000` →
   `tidy: /tmp/b5 cannot be read: Permission denied`, exit `2`. The phrase AC2 forbids for *this*
   fixture is still present where it is true, which is the distinction the item was filed about.

## Test sensitivity check

Performed by reverting, not by reading. `git checkout main -- tidy/planner.py` with the new tests
and the README left in place; `grep -c _unexaminable_reason tidy/planner.py` → `0`, confirming the
revert was really in the file; both `__pycache__` directories deleted and the run made with
`PYTHONDONTWRITEBYTECODE=1`, because a stale cache has produced a false pass in this project
before. Result: `Ran 72 tests ... FAILED (failures=3, errors=2)` — the CLI test failing in both
subtests and again on its on-disk assertion, and both planner tests erroring on the uncaught
`FileNotFoundError`. Every one of the 69 pre-existing tests passed, so the new tests are specific
to the new behaviour and the guard breaks nothing that was already asserted.

Restored with `git checkout wi/BUG-0004 -- tidy/planner.py`: `git status --short` empty,
`grep -c _unexaminable_reason` → `2`, suite `Ran 72 tests ... OK`. The working tree is back at
`ab64484` exactly.

## Diff read against the plan

`git diff main..wi/BUG-0004` touches nine files, four of them outside `tracker/`: `tidy/planner.py`
(plan step 1 — the guard and `_unexaminable_reason`), `tests/test_cli.py` (step 2 — the end-to-end
class and the module docstring), `tests/test_planner.py` (step 3 — the reason-string class, its
two tests, the `errno` import and the docstring), and `README.md` (step 4 — the example line and
the two sentences). Nothing in the code is unaccounted for by a plan step, and no criterion is
carried by code no test touches.

Two implementation choices the plan explicitly delegated were checked against what it fixed rather
than against taste. The guard is **one** `try` around the loop body rather than two around the two
calls: `os.scandir(folder)` is outside it, the only calls inside that can raise `OSError` are
`entry.is_dir()` and `entry.stat()` — `folder_for` and `band_for` are dictionary lookups and
`Action` is a dataclass — and case 3 above demonstrates that the existing order still holds. The
`except` clause is `OSError` rather than `FileNotFoundError`, which case 1 shows to be necessary.

The README deviation the report declares is real and is as described: `git diff` shows the `1`
clause's words unchanged but its line breaks moved, because the paragraph was re-wrapped. That
matters to BUG-0005, which edits that clause; it is recorded in this item's `impl-report.md`
`## Deviations` and repeated here so a verifier of BUG-0005 sees it too.

## Defects found

**None.** No criterion of this item failed, and nothing was found that belongs to another item.

One observation that is deliberately *not* filed as a defect: in cases 2, 3 and 5 above the mode
banner does not appear on stderr, because `cli.py` prints it only when at least one action is a
move. That is WI-0001's decided behaviour, settled at WI-0001/Q-001 and commented in
`tidy/cli.py:72`, and it reproduces identically on a folder containing no symlinks at all
(`/tmp/b4`, a lone `notes.xyz`: `leave  notes.xyz   [no rule for '.xyz']` then
`Nothing to do: ...`, exit `0`). It is untouched by this item and contested by no criterion.

## Not verified, and why

- **An entry that fails with `EACCES`, `EIO` or `ENOTDIR` rather than `ENOENT` or `ELOOP`.** The
  guard is written for the whole `OSError` class, and two members of it are exercised above, but a
  per-entry permission failure needs an unreadable *parent*, which is ADR-0006's target-level case
  rather than this one, and could not be constructed as a per-entry failure without root. The
  handler is one `except OSError` and `error.strerror` is populated for every errno, so the
  untested members differ only in the words the operating system supplies — but that is an
  argument, not a measurement, and it is recorded here as such. `impl-report.md` `## What I did
  not do` item 5 declares the same gap.
- **A file deleted between `os.scandir` and `entry.stat()`** — the other real-world source of
  `ENOENT` on a listed entry. It needs a race this suite cannot schedule deterministically. Its
  output would be identical to case AC1's, since the reason string names no cause, which is why
  `_unexaminable_reason` was written not to guess at one.
- **Behaviour on a filesystem or platform where symlinks cannot be created.** The tests' skip path
  was read and its trigger conditions confirmed, but it was not executed, because symlinks work
  here. What is verified is that the skip is gated on `os.symlink` raising rather than on a
  platform name, so it cannot silently pass on a platform it never ran on.
- **Whether the epic's other open items are affected by the README re-wrap.** Out of scope for
  this item's criteria; flagged above for BUG-0005 rather than checked.
