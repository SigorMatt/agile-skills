# Implementation report — BUG-0004

## What was built

One guard in `build_plan`, one helper beside `_no_rule_reason`, two regression tests and two
sentences in `README.md`. `tidy/cli.py`, `tidy/apply.py` and `tidy/rules.py` are byte-for-byte
identical to `main`: ADR-0006's target-level handler is untouched, and so is every exit status the
CLI returns.

The guard wraps the two calls that interrogate an entry — `entry.is_dir()` and `entry.stat()` —
and nothing else, which is what ADR-0009 fixes. `os.scandir(folder)` stays outside it, so a folder
that cannot be listed still reaches `cli.py` and still exits 2. An `OSError` from either call
becomes that entry's `leave` action and the loop continues with the next entry.

What a user now sees, from the item's own reproduction steps run verbatim:

```
$ mkdir -p /tmp/dangling && echo x > /tmp/dangling/photo.jpg
$ ln -s /tmp/dangling/gone.pdf /tmp/dangling/broken.pdf
$ python3 -m tidy /tmp/dangling
tidy: preview only - nothing will be moved. Re-run with --apply to move.
leave  broken.pdf   [cannot be examined: No such file or directory]
move   photo.jpg -> recent/images/photo.jpg
$ echo $?
0
$ python3 -m tidy /tmp/dangling --apply
tidy: moving files. Nothing will be overwritten.
leave  broken.pdf   [cannot be examined: No such file or directory]
move   photo.jpg -> recent/images/photo.jpg
$ echo $?
0
$ find /tmp/dangling | sort
/tmp/dangling
/tmp/dangling/broken.pdf
/tmp/dangling/recent
/tmp/dangling/recent/images
/tmp/dangling/recent/images/photo.jpg
```

The banner is on stderr and the two action lines are on stdout, as before. `photo.jpg` is tidied,
`broken.pdf` is left exactly where it was, and neither run says the folder could not be read.

The reason string carries the operating system's own words — `error.strerror` — and names no
cause. The second member of the class behaves the same way through the same guard: a symlink
pointing at itself raises `ELOOP` from `is_dir()`, one call before any `stat()`, and now prints
`leave  loop.pdf   [cannot be examined: Too many levels of symbolic links]` with exit 0, where on
`main` it printed `tidy: /tmp/loopy cannot be read: Too many levels of symbolic links` and exited
2.

Branch `wi/BUG-0004`, three commits: `7ab0811` (the guard and both test classes), `1156654` (the
README), `38218c0` (the opening tracker entry). Branched from `main` at `73bb1f4`.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — either mode still reports every other file | The `OSError` no longer leaves `build_plan`; the entry gets a `leave` action and the loop continues, so every other entry is classified as usual | `tests.test_cli.UnexaminableEntryTests.test_a_dangling_symlink_does_not_cost_the_rest_of_the_folder` → ok. It asserts, for `[folder]` and `[folder, "--apply"]`, exactly one move line naming `photo.jpg` and exactly one leave line naming `broken.pdf`; then, on disk, that `recent/images/photo.jpg` is a file and `broken.pdf` is still a symlink in the top level. `tests.test_planner.UnexaminableEntryTests.test_the_other_files_are_still_planned` → ok, asserting `{"broken.pdf": "leave", "photo.jpg": "move"}`. By hand: the reproduction above, where stdout names both files |
| AC2 — nothing states or implies the folder could not be read | The message that made the false claim is `cli.py`'s target-level handler, which is never reached now; the replacement wording contains neither the phrase nor a traceback | The same CLI test asserts `cannot be read` is absent from **both** `result.stdout` and `result.stderr`, and that `Traceback` is absent from both, in both modes. By hand: `python3 -m tidy /tmp/dangling 2>&1 \| grep -c 'cannot be read'` → `0`, grep exit 1 |
| AC3 — the exit status is one `README.md` documents, and `README.md` says which case | A `leave` is a planned outcome, not a failed move, so `apply_plan` returns no `"failed"` outcome and `cli.py` returns 0 (ADR-0007). `README.md`'s exit-status paragraph now names this case | The same CLI test asserts `result.status == 0` in both modes. By hand: `python3 -m tidy /tmp/dangling; echo $?` → `0` and `--apply` → `0`. `README.md` reads "Exit status is 0 on success — including when there was nothing to do, and when some files were left where they are" |
| AC4 — a regression test builds the fixture, asserts AC1 and AC2, fails when the handling is removed, and skips where symlinks cannot be created | Three new tests across two files; the fixture is built in a helper that calls `self.skipTest` when `os.symlink` raises `OSError`, `NotImplementedError` or `AttributeError` — gated on the operation failing, not on a platform name | Reverted `tidy/planner.py` to `main` with the tests in place, cleared both `__pycache__` directories and ran with `PYTHONDONTWRITEBYTECODE=1`: `Ran 72 tests ... FAILED (failures=3, errors=2)`, and the failing set is exactly the three new tests — `test_a_dangling_symlink_does_not_cost_the_rest_of_the_folder` (both subtests and the on-disk assertion), `test_an_entry_that_cannot_be_stat_ed_is_left_with_the_os_reason`, `test_the_other_files_are_still_planned`. The 69 pre-existing tests were unaffected in both directions. Restored: `Ran 72 tests ... OK` |

## Deviations from the plan

None in substance. Three notes on how the steps were carried out:

1. **The guard is one `try` around the existing loop body, not two around the two calls.** The
   plan left the shape to me and fixed three properties instead; all three hold. `os.scandir` is
   outside; the only calls inside that can raise `OSError` are `entry.is_dir()` and
   `entry.stat()`, because `folder_for` and `band_for` are pure lookups and `Action` is a
   dataclass; and the existing order is preserved, so an unrecognised extension is still
   `[no rule for '.xyz']` and is still never aged. Writing it as two guards would have meant
   stat-ing entries the current code deliberately does not stat, which would have changed
   behaviour WI-0002 AC6 fixes.
2. **The planner step produced two tests rather than one.** Plan step 3 asks for the reason string
   to be pinned; splitting "the reason is right" from "the other files are still planned" makes a
   failure say which of the two broke. Both are inside step 3's scope.
3. **The README's exit-status paragraph was re-wrapped.** The `0` clause grew by seven words and
   the paragraph's line breaks were redone so the file keeps its ~96-column style. No word of the
   `2` clause or the `1` clause changed — the `1` clause is BUG-0005's subject and `git diff` shows
   its words untouched — but its line breaks moved, so whoever implements BUG-0005 should re-read
   the paragraph rather than apply a remembered diff.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests ... OK`, on the branch head after the last commit (69 before this item) |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 9 items, 11 documents, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1, AC2 and AC3 are each asserted by `test_a_dangling_symlink_does_not_cost_the_rest_of_the_folder`, and AC1 again by `test_the_other_files_are_still_planned`; AC4 is demonstrated by the revert experiment, whose exact output is in the table above. No criterion is carried by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 3 commit(s) on main..wi/BUG-0004 name BUG-0004". It reported a false failure at the opening transition — see `## What I did not do`, item 3 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/BUG-0004 -- tidy tests README.md` is four hunks in four files: the guard and its helper (steps 1, AC1-AC3), the CLI test class and the module docstring (step 2, AC4), the planner test class with its `errno` import and docstring (step 3, AC4), and the two README edits (step 4, AC3). Nothing else |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, "checked no documents changed since main" — correct, because this branch touches nothing under `docs/`; ADR-0009 and overview v7 were linted on `main` when `plan` wrote them |

## What I did not do

1. **`tidy/cli.py` was not touched, and ADR-0006's handler is unchanged.** It is still what
   answers a folder that cannot be listed, still exits 2, and BUG-0001's regression test
   `test_an_unreadable_folder_exits_2_without_a_traceback` still passes untouched. That the
   dangling-symlink message *came from* that handler was the symptom, not a defect in it.
2. **Symlink ageing was not changed.** A symlink whose target exists is still aged by that
   target's `mtime`, which WI-0002's review examined and accepted. ADR-0009 costs the alternative
   (`follow_symlinks=False`) and rejects it for this item; nothing here forecloses it.
3. **`check-commit-refs` reported a false failure at the `planned → in-progress` transition**, for
   the fourth recorded time. The branch had just been created and held zero commits, so
   `main..wi/BUG-0004` was empty; the script read the empty range as "already merged into `main`"
   and advised rewinding a merge that never happened. It does not block that move, so nothing was
   lost, and it exits 0 on this branch now. It is a defect in the methodology under
   `.claude/agile-skills/`, not in this project, and BUG-0003's `review.md` Finding 7 is the
   standing record of it.
4. **BUG-0005 and WI-0003 were left alone.** BUG-0005 touches the same README paragraph and was
   not started; `git diff --stat main..wi/BUG-0004` lists eight files, four of them the tracker's.
5. **No test covers an entry that fails with `EACCES` or `EIO`.** The guard is written for the
   class and the two members that can be built with one shell command — a dangling link and a
   symlink loop — are both exercised, the second by hand rather than by a test. Making a `stat`
   fail with a permission error requires an unreadable parent directory, which is the *target*
   being unreadable and therefore ADR-0006's case, not this one; I could not construct it as a
   per-entry failure without root.
