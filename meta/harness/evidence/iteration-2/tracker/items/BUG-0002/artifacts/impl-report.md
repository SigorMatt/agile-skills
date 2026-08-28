# Implementation report — BUG-0002

## What was built

ADR-0007, in four files and 178 added lines.

| file | change |
|------|--------|
| `tidy/apply.py` | a frozen `Outcome(kind, message)` dataclass; `apply_plan` returns `list[Outcome]` in action order instead of `list[str]`; `_move_without_a_link` tags its three returns |
| `tidy/cli.py` | prints `outcome.message`, and exits non-zero only when some outcome is `"failed"` |
| `tests/test_apply.py` | `HardLinkFallbackTests` — two tests reaching ADR-0003's fallback by patching `os.link`; two existing assertions upgraded to read `.kind` and `.message` |
| `tests/test_cli.py` | `FallbackExitStatusTests` — the exit status and the stderr wording, end to end through `main()` |

Every message string is byte-identical to what was there before. The diff shows each one moved
inside an `Outcome(...)` call and re-wrapped, with no character of the text changed —
`git diff main..wi/BUG-0002 -- tidy/apply.py` is the check, and it is what AC2 rests on.

The one behavioural line is `tidy/cli.py`'s last:

```
return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0
```

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — an APPLY run in which every move landed exits 0, by either route | `_move_without_a_link` tags its success `"fell-back"`; `cli.main` exits non-zero only on `"failed"` | `tests.test_cli.FallbackExitStatusTests.test_a_run_that_falls_back_for_every_file_exits_0` — asserts `status == 0` and that both files are at the destinations the move lines named. Plus the item's own reproduction re-run verbatim against the branch: `python3 nolink.py <folder>` → `EXIT: 0`, with `recent/documents/doc.pdf` and `recent/images/photo.jpg` both present (it printed `EXIT: 1` on `main` at `f363721`) |
| AC2 — the fallback is still reported, unchanged | no message string was edited | The same CLI test asserts the full line is present in stderr, character for character: `tidy: <name> was moved to <destination> without a hard link, because this filesystem refused one ([Errno 18] Invalid cross-device link)`. `tests.test_apply.HardLinkFallbackTests.test_a_fallback_move_lands_and_is_not_a_failure` asserts the same content at the unit level. Mutation: rewording `hard link` to `hardlink` in `tidy/apply.py` fails both (2 failures, 1 error) |
| AC3 — a run in which a move genuinely did not land still exits non-zero | the three failure returns keep the `"failed"` tag, so the exit rule still sees them | `tests.test_cli.FallbackExitStatusTests.test_a_genuine_failure_alongside_a_fallback_still_exits_1` — a `0o500` destination folder makes `doc.pdf`'s `shutil.move` fail with `EACCES` while `photo.jpg` falls back cleanly: `status == 1`, `doc.pdf` still at the top level, `photo.jpg` at `recent/images/photo.jpg`, and the failure line printed before the fallback line. At the unit level: `test_a_fallback_that_cannot_land_is_a_failure`, plus `NeverOverwriteTests.test_link_refuses_an_existing_destination` and `test_one_failure_does_not_stop_the_remaining_actions`, all three now asserting `kind == "failed"` |
| AC4 — a regression test that patches `os.link` to raise a non-`FileExistsError` `OSError`, asserts AC1-AC3, and fails when the fix is reverted | both new classes patch `tidy.apply.os.link` with `OSError(18, "Invalid cross-device link")` | Three mutations, each run in a detached worktree with `__pycache__` cleared and `PYTHONDONTWRITEBYTECODE=1`, and each confirmed present in the file before running — see `## Gates` |

## Deviations from the plan

- **Plan step 6 named two tests in `HardLinkFallbackTests`; a third was written and then removed.**
  It asserted that an all-clean run still returns `[]` and that two equal `Outcome`s compare equal.
  The first half duplicates `ApplyTests.test_every_move_lands_and_the_source_is_gone`, which the
  plan explicitly says must stay unchanged as that evidence; the second tests
  `dataclasses`. Neither traces to an acceptance criterion, so it was deleted rather than shipped.
- **Plan step 8 said "revert steps 1-4 in a scratch copy — or stash them".** Neither: a detached
  `git worktree` under `.harness/` was used, so the branch's working tree was never in a reverted
  state and there was no stash to lose. Three mutations were run rather than one whole-file revert,
  because the whole-file revert conflates the type change with the behaviour change — see below.
- **Nothing else.** Steps 1-5, 7 and 9 were executed as written.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 68 tests ... OK` (64 before this item; the four new ones ran rather than skipped, confirmed with `-v`) |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1-AC4; none rests on reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0002 wi/BUG-0002` → exit 0, `all 1 commit(s) on main..wi/BUG-0002 name BUG-0002` |
| `no-unplanned-scope` | **pass**, advisory | `git diff main..wi/BUG-0002 --stat` is four files: `tidy/apply.py` and `tidy/cli.py` (plan steps 1-4), `tests/test_apply.py` (steps 5-6), `tests/test_cli.py` (step 7). No hunk outside those |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0. It reports "checked no documents changed since main", because this branch touches no file under `docs/` — the ADR and the overview were written and committed by `plan` on `main` at `a0fe21e` |

### The mutations behind AC4

Each was applied to a detached worktree at `cb4a882`, verified present by reading the file back,
with `__pycache__` removed and `PYTHONDONTWRITEBYTECODE=1` set — a same-length edit has served a
stale `.pyc` in this project before and produced a false pass.

| mutation | result |
|----------|--------|
| `tidy/apply.py` and `tidy/cli.py` restored to their `main` versions — the fix removed entirely | 1 failure, 2 errors. `test_a_run_that_falls_back_for_every_file_exits_0` fails `1 != 0`; both `HardLinkFallbackTests` error on `'str' object has no attribute 'kind'` |
| the exit rule alone reverted to `return 1 if outcomes else 0`, keeping the `Outcome` type | 1 failure: `test_a_run_that_falls_back_for_every_file_exits_0`, `1 != 0`. This is the sharp one — it isolates the behaviour from the type change |
| the exit rule weakened to `any(outcome.kind == "never" ...)`, so nothing is ever a failure | 1 failure: `test_a_genuine_failure_alongside_a_fallback_still_exits_1`, `0 != 1`. AC3 is guarded in the other direction |
| the fallback message reworded `hard link` → `hardlink` | 2 failures, 1 error across both new classes. AC2 is guarded |

`test_a_genuine_failure_alongside_a_fallback_still_exits_1` **passes against the unfixed code**, and
that is correct: it asserts exit 1, which the old code also produced. It is a guard against
over-fixing — against a change that silences real failures along with the fallback note — not a
demonstration that the bug was present. Mutation 3 is what proves it is sensitive to anything.

## What I did not do

- **No test runs on a filesystem that actually refuses hard links.** All four patch `os.link` to
  raise errno 18. That is the error such filesystems raise, so what is proven is the branch's
  behaviour rather than the platform's; exFAT, FAT32 and SMB remain untested by observation. The
  plan records this as a risk and it is unchanged by anything here.
- **`test_a_genuine_failure_alongside_a_fallback_still_exits_1` skips under root** or on a
  filesystem that does not enforce mode `0o500`, exactly as
  `BadTargetTests.test_an_unreadable_folder_exits_2_without_a_traceback` already does. On such a
  platform AC3's end-to-end leg does not run and only the three unit-level `kind == "failed"`
  assertions carry it. It did **not** skip in this execution — `-v` shows it as `ok`.
- **`README.md` is untouched.** Its exit-status paragraph already stated the contract this item
  implements, which the plan records as an assumption. Nothing in the README documents the fallback
  note on stderr, and adding that would be new behaviour to document rather than this fix.
- **The TOCTOU window in `_move_without_a_link` is untouched**, between `os.path.lexists` and
  `shutil.move`. ADR-0003 accepted it knowingly and BUG-0002 does not reopen it.
- **BUG-0003 and BUG-0004 were not touched**, though both live in these two files. Both are open at
  `ready`.
- **One toolkit observation, not a defect in this item.** At plan step 3, `transition ... --to
  in-progress` ran `check-commit-refs BUG-0002 wi/BUG-0002` against a branch with zero commits and
  reported `wi/BUG-0002 is already merged into main, so main..wi/BUG-0002 is empty`. An empty range
  on a branch that has never been committed to is not a merge; the diagnosis is wrong for the
  freshly-branched case. It did not block the move — `implement` only gates its completion
  transition — and the gate passes correctly now that a commit exists.
