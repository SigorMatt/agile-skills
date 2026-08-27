# Implementation report — BUG-0002

## What was built

One wrapper and three tests.

`expenses/store.py`'s `save` now has its whole body inside a `try`, from `target.parent.mkdir`
to the `os.replace`, and an `except OSError as err` that raises
`ExpensesError("cannot write %s: %s" % (path, err))`. That is the boundary ADR-0008 fixes, and
the one `load` has always used; `cli.main` already turns an `ExpensesError` into a line on stderr
and exit 2, so nothing above `store.py` changed. The existing `except BaseException` cleanup that
unlinks the temporary file stays nested *inside* the new wrapper, so it still runs before the
translation and a refused write leaves no `.expenses-` file behind. The module docstring now
states the rule, citing ADR-0008.

`tests/test_cli.py` gained `BUG0002AnUnwritableStoreIsRefusedNotATraceback` — a fixture that
records one person while the directory is still writable, drops it to mode 500, and runs the tool
in a real subprocess so the exit status and any traceback are observed the way a person at a
terminal would see them. It skips itself when the process can write to a mode-500 directory
anyway.

`docs/architecture/overview.md` went from version 6 to **7**: the paragraph `plan` wrote under
"What is coming" describes code that now exists, so it moved into the `expenses/store.py` piece
and says what both file-touching functions do.

Branch `wi/BUG-0002`, from `main` at `37e57f0`. Two commits: `db45f4f` (the fix and the tests) and
the documentation commit that follows this report.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — unwritable store, `person add Ana`: exit 2, nothing on stdout, one stderr line with the path and no `Traceback` | `save` translates the `PermissionError` raised by `NamedTemporaryFile`; `person_add` prints its success line only after `store.save` returns, so stdout stays empty without new code | `tests.test_cli.BUG0002AnUnwritableStoreIsRefusedNotATraceback.test_ac1_person_add_is_refused_with_one_line_naming_the_path`, which asserts all four. And by hand, the bug's own reproduction: `mkdir -p /tmp/rc-ro; chmod 500 /tmp/rc-ro; EXPENSES_STORE=/tmp/rc-ro/expenses.json python3 -m expenses person add Ana` → `cannot write /tmp/rc-ro/expenses.json: [Errno 13] Permission denied: '/tmp/rc-ro/.expenses-ls2wcmxl.tmp'`, `exit=2`; and the same command with stderr discarded, piped to `wc -c` → `0` bytes on stdout |
| AC2 — the same for `expense add` | the same wrapper; `expense_add` also prints after `store.save` | `...test_ac2_expense_add_is_refused_with_one_line_naming_the_path`, running `expense add --amount 10 --paid-by Zoe --shared-by Zoe` against the same unwritable store |
| AC3 — the previous dataset is byte-identical afterwards, no `.expenses-` file left | the temporary file is never renamed over the target when the write fails, and the nested cleanup removes it before the `OSError` is translated | `...test_ac3_the_dataset_and_the_directory_are_left_as_they_were`, comparing `store.read_bytes()` either side of the refusal and listing the directory for names beginning `.expenses-`. And by hand: `ls -a /tmp/rc-ro` after the refusal above → `.` and `..` only |
| AC4 — a regression test covers AC1 by making a temporary directory read-only, fails if the handling is removed, and skips when the process can write regardless | the fixture chmods its own directory to 500 and probes it by trying to create a file, skipping if that succeeds | the deliberate check: `cp expenses/store.py /tmp/store.fixed.py; git show main:expenses/store.py > expenses/store.py; python3 -m unittest tests.test_cli.BUG0002AnUnwritableStoreIsRefusedNotATraceback` → `Ran 3 tests`, `FAILED (failures=3)`, each `AssertionError: 1 != 2 : expected a refusal; stderr was b'Traceback (most recent call last): ...PermissionError: [Errno 13] Permission denied'`; then `cp /tmp/store.fixed.py expenses/store.py` and the suite green again |
| AC5 — `python3 -m unittest discover -s tests -t .` exits 0 | — | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 123 tests in 1.475s`, `OK` — 120 before this item, plus these three |

## Deviations from the plan

- **Plan step 3 says the fixture runs `person add Ana` while the directory is still writable.
  It records `Zoe` instead.** With `Ana` already in the group, AC1's literal command
  `person add Ana` would have been refused by `add_person` with "Ana is already in the group" —
  a refusal that never reaches `save` and never names the path, so the test would have passed for
  the wrong reason under AC1's own wording. Recording a different name keeps AC1's command exactly
  as the criterion writes it and still leaves a dataset for AC3 to protect.
- **Plan step 6 says to `chmod 0o700` back before asserting.** The AC3 test does not: listing the
  directory and reading the file both work at mode 500 (`r-x`), and the restore is already
  registered as a cleanup. Doing it twice would work but would hide which permission the assertion
  actually needs.
- Nothing else. The nine steps were executed in order; steps 1, 2, 7, 8 and 9 as written.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 123 tests`, `OK`, run on the branch head |
| `lint-clean` | **skipped** | `commands.lint` is null in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. The gate checked nothing and is not reported as a pass |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1, AC2 and AC3 each name a test function above; AC4 names the command that removed the handling and the three failures it produced; AC5 is the suite command and its own output. No criterion rests on reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0002 wi/BUG-0002` → exit 0 |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | the diff against `main` is four files: `expenses/store.py` (step 1 and step 2), `tests/test_cli.py` (steps 3 to 6, plus one line of the module docstring naming the new class), `docs/architecture/overview.md` (step 9), and this item's own tracker files. No hunk is outside a plan step |

## What I did not do

- **No test for `person delete` or `expense delete` against an unwritable store.** They call the
  same `save` and are fixed by the same wrapper, but no criterion names them; the plan records
  this under `## Assumptions` and it is unchanged.
- **No unit test in `tests/test_store.py` calling `save` on an unwritable path.** The plan puts it
  under `## Out of scope for this item`.
- **`README.md` is untouched.** Its "When something is wrong" section already says a command that
  cannot do what you asked writes to standard error and exits 2 — a sentence that was not true of
  an unwritable store before this change and is true now. Nothing in it had to change, and no
  criterion asks for a new example.
- **Nothing was done about `expense delete 01`**, the non-blocking finding recorded in WI-0004's
  review. It is not this item's, and fixing it here would have put an unverified change in this
  diff.
