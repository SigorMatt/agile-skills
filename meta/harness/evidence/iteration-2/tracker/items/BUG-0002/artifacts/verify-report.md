# Verification report — BUG-0002

Verified-commit: 6a5b1a7f0ed19923e82a1da76018a46ba36b2e0a

## Verdict

**Pass.** All four acceptance criteria are met, each demonstrated by a command run in this
execution rather than by reading `impl-report.md`. No defect was found in this item and none is
filed against another. One observation about `README.md`'s wording is recorded below and
deliberately not filed as a bug; the reasoning is stated so a reviewer can disagree with it.

Every check was derived from the criterion first. Where a criterion named a means of checking it —
AC3's `FileExistsError` path — that means was exercised directly rather than substituted.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — an APPLY run in which every move landed exits 0, whether the moves used `os.link` **or** ADR-0003's fallback | **pass** | *Primary route, no injection:* `python3 -m tidy .harness/v/primary --apply; echo $?` | `move   doc.pdf -> recent/documents/doc.pdf` / `move   photo.jpg -> recent/images/photo.jpg` / `EXIT: 0`, and `find` shows `recent/documents/doc.pdf` and `recent/images/photo.jpg` | The criterion says "whether ... or", so both routes were run, not just the one the bug is about |
| AC1 (fallback route) | **pass** | *The item's own reproduction, verbatim:* `python3 nolink.py <folder>` with `os.link` replaced by one raising `OSError(18, "Invalid cross-device link")` | `EXIT: 0` / both move lines on stdout / both files found at `recent/documents/doc.pdf` and `recent/images/photo.jpg` | The item records `EXIT: 1` here on `main`. Confirmed still 1 on `main` in this execution — see AC2's diff |
| AC2 — the fallback is still reported; the stderr line is unchanged and **only** the exit status changes | **pass** | The same fixture run twice — once against a `main` worktree, once against the branch — capturing stderr to two files, normalising only the fixture directory name, then `diff` | `DIFF EXIT: 0`. `main` printed `EXIT: 1`, the branch printed `EXIT: 0`, and the three stderr lines are byte-identical between them | This is the strongest available reading of "unchanged": not "contains the substring" but "identical to what the unfixed code produced". Only the exit status differs |
| AC3 — a run in which a move genuinely did not land still exits non-zero | **pass** | *(a) The `FileExistsError` path the criterion names, with nothing patched:* `build_plan`, then create the destination, then `apply_plan` — so `os.link` itself raises | `outcomes: [Outcome(kind='failed', message='recent/documents/report.pdf appeared while tidying; report.pdf was left where it is')]`; the destination still holds `'appeared mid-run'` and the source is still present | A real kernel `FileExistsError`, no injection of any kind |
| AC3 (end to end, nothing patched at all) | **pass** | `chmod 0500` on a pre-existing `recent/`, then `python3 -m tidy .harness/v/perm --apply; echo $?` | two `could not create the folder for ...: [Errno 13] Permission denied` lines, `EXIT: 1`, and `find` shows both files still at the top level | No `mock`, no injected `os.link` — a genuine filesystem failure driven through the real entry point |
| AC3 (mixed run: one failure, one fallback) | **pass** | `chmod 0500` on `recent/documents/`, then the injected-`os.link` reproduction | `EXIT: 1`; `doc.pdf could not be moved to recent/documents/doc.pdf: [Errno 13] Permission denied`, `photo.jpg was moved ... without a hard link`; `doc.pdf` still at the top level, `photo.jpg` at `recent/images/photo.jpg` | The case the fix could most easily have broken: a fallback in the same run does not mask a real failure |
| AC4 — a regression test in `tests/` patches `os.link` to raise a non-`FileExistsError` `OSError`, asserts AC1-AC3, and fails when the fix is reverted | **pass** | Read the tests; confirmed the injected error's type; then ran five mutations, each in a detached worktree at `6a5b1a7` with `__pycache__` cleared and `PYTHONDONTWRITEBYTECODE=1`, each confirmed present in the file before running | `python3 -c "isinstance(OSError(18, ...), FileExistsError)"` → `False`, `isinstance(..., OSError)` → `True`. Mutation results in `## Test sensitivity check` | Four tests across two classes: `tests.test_apply.HardLinkFallbackTests` (2) and `tests.test_cli.FallbackExitStatusTests` (2), all patching `tidy.apply.os.link` |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` run by this skill on `6a5b1a7` → exit 0, `Ran 68 tests in 0.062s` / `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 8 item(s), 9 document(s)` / `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | The `## Criteria` table's `command run` column is this skill's own commands. No row cites `impl-report.md`. AC1's primary-route check and AC3's unpatched end-to-end check are not in `impl-report.md` at all |
| `negative-cases-exercised` | **pass** | See `## Negative and boundary cases exercised` — six conditions triggered, not read about |
| `tests-would-fail-without-the-change` | **pass**, advisory | Five mutations, each turning a different test red; the restored tree is green again |

## Negative and boundary cases exercised

| condition | command | result |
|-----------|---------|--------|
| every move fails, none succeeds | `recent/` at `0o500`, `python3 -m tidy ... --apply` | `EXIT: 1`, both files untouched at the top level |
| one failure and one fallback in the same run | `recent/documents/` at `0o500`, plus injected `os.link` | `EXIT: 1`, the failure line printed **before** the fallback line — action order preserved |
| destination appears between planning and applying | `build_plan`, create the destination, `apply_plan` — real `FileExistsError` | one outcome, `kind='failed'`; the pre-existing file is byte-unchanged and the source is still there |
| nothing to move | `python3 -m tidy <empty folder> --apply` | `Nothing to do: no files to move in ...`, `EXIT: 0` |
| the folder cannot be read | `chmod 0`, then `--apply` | `tidy: ... cannot be read: Permission denied`, `EXIT: 2` — BUG-0001's behaviour is unaffected |
| the folder does not exist | `python3 -m tidy <missing> --apply` | `tidy: ... is not a folder`, `EXIT: 2` |
| preview under the fallback condition | injected `os.link`, no `--apply` | `EXIT: 0`, the file still at the top level — `apply_plan` is not reached, so the new code cannot affect preview |

## Test sensitivity check

Five mutations, each applied to a detached `git worktree` at `6a5b1a7`, each verified present by
reading the file back, with `__pycache__` removed and `PYTHONDONTWRITEBYTECODE=1` set.

| mutation | full-suite result | which tests went red |
|----------|-------------------|----------------------|
| A — `tidy/apply.py` and `tidy/cli.py` restored to `main`; the fix removed entirely | `FAILED (failures=1, errors=4)` | `test_a_run_that_falls_back_for_every_file_exits_0` (`1 != 0`); both `HardLinkFallbackTests`; both upgraded `NeverOverwriteTests` assertions |
| B — exit rule alone reverted to `return 1 if outcomes else 0` | `FAILED (failures=1)` | `test_a_run_that_falls_back_for_every_file_exits_0` — isolates the behaviour from the type change |
| C — `main` returns `0` unconditionally after applying | `FAILED (failures=1)` | `test_a_genuine_failure_alongside_a_fallback_still_exits_1` (`0 != 1`) — AC3 is guarded against over-fixing |
| D — the fallback's success tagged `"failed"` instead of `"fell-back"` | `FAILED (failures=2)` | `test_a_fallback_move_lands_and_is_not_a_failure` and `test_a_run_that_falls_back_for_every_file_exits_0` |
| E — the fallback message reworded to `"%s was moved to %s (no hard link available: %s)"` | `FAILED (failures=2, errors=1)` | both `FallbackExitStatusTests` and one `HardLinkFallbackTests` — AC2's wording is guarded |
| *(control)* the tree restored, unmutated | `Ran 68 tests` / `OK` | — |

`test_a_genuine_failure_alongside_a_fallback_still_exits_1` **passes** under mutation A, and
`impl-report.md` says so itself. That is correct behaviour for it: it asserts exit 1, which the
unfixed code also produced. Mutation C is what establishes it is sensitive to anything, and it is.

## Defects found

**None.** No acceptance criterion of BUG-0002 failed, and no behaviour delivered by another item
was found broken. No bug item is filed by this execution.

Two things were looked at and judged not to be defects:

1. **`README.md`'s exit-1 clause is phrased for the partial case.** It reads "1 when some file
   could not be moved while others were", and the run where `recent/` is unwritable exits 1 with
   *no* file moved. The sentence is loose rather than false — "some file could not be moved" is
   true in that run — and the behaviour is unchanged by this item and covered by no BUG-0002
   criterion. Recorded here rather than filed, so that `review-close`'s document audit can take a
   different view with the evidence in front of it.
2. **`NO_HARD_LINKS` is one module-level `OSError` instance reused as `side_effect` across tests.**
   `mock` raises the same object each time, so its `__traceback__` is reassigned per raise.
   `apply.py` uses the error only for `%s` formatting, and `str(e)` is stable, so nothing observable
   depends on it. A test-hygiene observation, not a defect.

## Not verified, and why

- **No filesystem that genuinely refuses hard links was used.** Every fallback check replaces
  `os.link` with one raising `OSError(18)`. What is proven is the branch's behaviour given that
  error, not that exFAT, FAT32, SMB, NFS or FUSE raise exactly it. The item's own reproduction
  steps take the same approach and name the same limitation; nothing in this execution improves on
  it, and no such volume was available.
- **The `os.unlink` failure path is untested** — where `os.link` succeeded and the original could
  not be removed, leaving a duplicate. It is tagged `"failed"` in the code, so it exits non-zero,
  but producing it needs a link to succeed and an unlink to fail on the same file, which was not
  contrived here. It was equally untested before this item and no criterion covers it.
- **`test_a_genuine_failure_alongside_a_fallback_still_exits_1` was not observed skipping.** It ran
  (`ok` under `-v`) on this machine. Its `skipTest` guard fires under root or on a filesystem
  ignoring mode `0o500`; that path was not exercised, so what happens on such a platform is
  inferred from reading the guard rather than observed.
- **A genuine mid-run `FileExistsError` was not driven through `main()`.** `build_plan` reserves
  colliding names, so the destination cannot pre-exist at plan time, and `main` gives no point to
  intervene between planning and applying. It was exercised one layer down, through `apply_plan`
  with a real kernel error, and the CLI's mapping from a `"failed"` outcome to exit 1 was exercised
  separately end to end. Together those settle AC3; neither alone would.
