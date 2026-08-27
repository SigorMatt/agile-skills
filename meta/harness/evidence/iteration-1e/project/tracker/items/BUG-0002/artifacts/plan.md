# Plan — BUG-0002 A write the operating system refuses escapes as a traceback, not a message

## Problem

`expenses/store.py` has two functions that touch the dataset file, and they disagree about what
an operating-system error is. `load` catches `OSError` and raises `ExpensesError("cannot read
...")`, which `cli.main` prints on stderr before exiting 2; `save` catches nothing, so a store the
user cannot write to — a read-only directory, a full disk, a path owned by somebody else — ends
the process with an eleven-line traceback and exit 1. Reproduced on the current trunk before
planning: `mkdir -p /tmp/bug2ro; chmod 500 /tmp/bug2ro; EXPENSES_STORE=/tmp/bug2ro/expenses.json
python3 -m expenses person add Ana` → exit 1, ending `PermissionError: [Errno 13] Permission
denied: '/tmp/bug2ro/.expenses-43qi2spl.tmp'`. What changes is the presentation only: the write is
a temporary file replaced over the target, so the previous dataset is already safe, and the fix
must keep it that way. The constraints are the project's own — python3 and the standard library,
no new module, and the layering rule that only `cli.py` prints and everything below it raises one
exception type.

## Approach

Make `save` obey the same boundary `load` already obeys, and write the boundary down so the next
person who adds a store function does not have to guess it. ADR-0008 records the decision and the
alternatives; in code it is one wrapper.

`save`'s body — the parent-directory creation, the temporary file, the write, and the
`os.replace` — moves inside a region that catches `OSError` and raises
`ExpensesError("cannot write %s: %s" % (path, err))`, with `path` as the caller gave it rather
than the temporary file's name. The existing cleanup, which removes the temporary file when
anything goes wrong, stays *inside* that region and keeps running first, so a refused write leaves
neither a changed dataset nor a `.expenses-` file behind. Nothing above `store.py` changes:
`cli.main` already catches `ExpensesError`, prints it to stderr and returns 2, and in all four
handlers that write, the `print` of the success line comes *after* the `store.save` call
[src: expenses/cli.py], which is why a refusal leaves stdout empty without anybody adding code
for it.

The regression goes in `tests/test_cli.py`, at the level the criteria are written at: a real
subprocess, so that "exits 2" and "no `Traceback`" are observed the way a person at a terminal
would see them. `tests/test_cli.py` already runs commands out of process in three places and has
`subprocess`, `sys` and `REPO_ROOT` for it [src: tests/test_cli.py].

Two hazards belong here rather than in a step, because getting either wrong makes the test lie:

- **The suite must not fail for a user who can write anyway.** `chmod 500` does not stop root, and
  a suite that fails for a legitimate reason gets ignored [src: BUG-0002 AC4]. The test probes the
  directory it just made read-only by trying to create a file in it, and skips itself if that
  succeeds — a probe, not a `geteuid` check, because the question is whether this process can
  write there, not who it is.
- **The read-only directory must be made writable again before the temporary directory is
  cleaned up**, or teardown fails and takes unrelated tests with it. `unittest` runs cleanups in
  reverse order of registration, so the `chmod 0o700` cleanup is registered *after* the
  `TemporaryDirectory` cleanup in order to run *before* it.

## Steps

1. **`expenses/store.py` — put `save`'s file access inside the refusal boundary.** Wrap the body
   of `save`, from `target.parent.mkdir` to the end, so that an `OSError` escaping any of it
   becomes `ExpensesError("cannot write %s: %s" % (path, err))`. Keep the existing
   `except BaseException:` cleanup where it is, nested inside, so it still unlinks the temporary
   file and re-raises before the translation happens. Afterwards: `save` raises `ExpensesError`
   and never `OSError`, the message names the path the caller passed, and no other function in the
   module changes.

2. **`expenses/store.py` — say in the module docstring what the boundary is.** The docstring
   already states that a refusal is an `ExpensesError`; add that this includes the operating
   system refusing the file, and cite ADR-0008. Afterwards: a reader of the module meets the rule
   before the code that implements it.

3. **`tests/test_cli.py` — add one test class for this bug, with the read-only fixture.** A
   `unittest.TestCase` (not `CommandTestCase`, whose store is writable by construction) that:
   creates a `TemporaryDirectory`; makes a `ro/` subdirectory inside it with the store path
   `ro/expenses.json`; runs `person add Ana` **while it is still writable**, so there is a
   recorded dataset to protect; `chmod 0o500` on `ro/`; registers the `chmod 0o700` cleanup after
   the temporary directory's; and skips the test if creating a probe file inside `ro/` still
   succeeds. Give it a helper that runs one command in a subprocess — modelled on
   `AC4ARerunInANewProcessPrintsTheSameBytes.run_in_a_new_process` [src: tests/test_cli.py] but
   returning `(returncode, stdout, stderr)` and asserting nothing itself.

4. **`tests/test_cli.py` — the AC1 test.** `person add Ben` against the unwritable store exits 2,
   `stdout` is empty, `stderr` is a single line that contains the store path and does not contain
   `Traceback`. Afterwards: removing step 1's wrapper makes this test fail on the exit code.

5. **`tests/test_cli.py` — the AC2 test.** The same three assertions for
   `expense add --amount 10 --paid-by Ana --shared-by Ana`, against the same unwritable store.
   Afterwards: both writing commands named in the criteria are covered, not just the first.

6. **`tests/test_cli.py` — the AC3 test.** Read the dataset's bytes before the refused command;
   run the refused command; `chmod 0o700` back; assert the bytes are identical and that no entry
   in the directory begins with `.expenses-`. Afterwards: the claim that a refused write changes
   nothing on disk is checked rather than asserted.

7. **Run the suite** — `python3 -m unittest discover -s tests -t .` from the repository root —
   and record the count. Afterwards: it exits 0, with the three new tests and the 120 that already
   pass [src: run: python3 -m unittest discover -s tests -t . → exit 0, 120 tests, OK].

8. **Re-run BUG-0002's own reproduction by hand** — the four numbered steps in `## Steps to
   reproduce`, including the restore — and paste the new output into `impl-report.md`. Afterwards:
   the report shows the reproduction failing to reproduce, in the same form the bug quoted it.

9. **`docs/architecture/overview.md` — move the paragraph this plan put under "What is coming"
   into the `expenses/store.py` piece, and bump to version 7.** The sentence describing the
   boundary becomes a description of code that exists, cited to `expenses/store.py` and ADR-0008,
   and "What is coming" goes back to naming WI-0003 alone. Afterwards: no paragraph in the
   overview describes this bug's fix in the future tense. (This project's precedent is that
   `implement` makes this move once the code exists — versions 3 and 5 were both written by
   `implement` for exactly this reason [src: docs/architecture/overview.md].)

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — unwritable store, `person add Ana`: exit 2, empty stdout, one stderr line with the path and no `Traceback` | 1, 4 | the new AC1 test in `tests/test_cli.py`, and the hand-run reproduction in step 8 pasted into `impl-report.md` |
| AC2 — the same for `expense add` | 1, 5 | the new AC2 test in `tests/test_cli.py` |
| AC3 — the previous dataset is byte-identical afterwards and no `.expenses-` file is left | 1, 6 | the new AC3 test, comparing the file's bytes either side of the refusal and listing the directory |
| AC4 — a regression test covers AC1 by making a temporary directory read-only, fails if the handling is removed, and skips when the process can write regardless | 3, 4 | the fixture's write-probe skip, and the deliberate check in step 4 that reverting step 1 turns the test red — to be recorded in `impl-report.md` as a command and its output |
| AC5 — `python3 -m unittest discover -s tests -t .` exits 0 | 7 | the command's own exit code and summary line, pasted into `impl-report.md` |

## Assumptions

- **The message reads `cannot write <path>: <error>`, mirroring `load`'s `cannot read <path>:
  <error>`.** The criteria fix only that it is one line naming the path with no traceback
  [src: BUG-0002 AC1], so the exact wording is this plan's choice. Reversing it is editing one
  string literal in `expenses/store.py` and whatever asserts on it; no stored data, no argument
  and no exit code depends on it. The tail carries Python's own error text, which for a
  `PermissionError` names the temporary file the operating system actually refused — accepted
  deliberately, because it is the true cause and because `load` already prints the same kind of
  detail.
- **The regression tests run the tool in a subprocess rather than through `main()` in process.**
  With the handling removed, an in-process test would see an `OSError` propagate — which fails the
  test, so it would satisfy AC4 — but it would never observe a `Traceback` on stderr or an exit
  status, which is what AC1 is written about. Reversing this is rewriting three short test methods
  against the existing `run_command` helper.
- **`person delete` and `expense delete` are fixed by the same wrapper and are not tested here.**
  They call the same `save` [src: expenses/cli.py], so step 1 covers them; no criterion names
  them, and adding tests for them would be work with nothing checking it.

## Decisions and ADRs

| decision | where it came from | record |
|----------|--------------------|--------|
| An `OSError` on the dataset becomes an `ExpensesError` inside `store.py`, not in `cli.main` and not in each handler | asked of the documents, then decided — the layering rule in `docs/architecture/overview.md` rules out the CLI knowing about `OSError`, but nothing said where the boundary was | **ADR-0008** |
| The parent-directory creation is inside the boundary too | decided; BUG-0002's `## Notes` asks for it explicitly rather than leaving it to be discovered | **ADR-0008** §1 |
| The temporary-file cleanup keeps precedence over the translation | decided; it is what AC3 turns on | **ADR-0008** §3 |
| The exact message wording | assumed, reversible | `## Assumptions`, first entry |
| Subprocess rather than in-process regression tests | assumed, reversible | `## Assumptions`, second entry |
| `delete` commands are covered but not tested | assumed, reversible | `## Assumptions`, third entry |
| No new test framework, no lint command | documented | ADR-0004, and `tracker/project.yaml` already carries the test command |

## Scaffolding

none. Every file this plan touches already exists, and `commands.test` runs today
[src: run: python3 -m unittest discover -s tests -t . → exit 0, 120 tests, OK].

## Risks

- **The fixture cannot make a directory unwritable for the process running the suite.** Then AC4's
  skip fires and the regression silently stops guarding anything on that machine. That is the
  behaviour the criterion asks for, and the mitigation is that the skip is visible in the runner's
  output rather than a passing test; it is worth naming here because a green suite on such a
  machine proves less than it looks like it does.
- **`chmod 0o500` is not the only way a write fails, and it is the only one tested.** A full disk
  and a read-only mount reach the same `except`, but nothing here demonstrates that. The wrapper
  catches `OSError` rather than `PermissionError` precisely so they are covered; the evidence for
  the others is the exception hierarchy, not a test.
- **A refusal raised inside the wrapped region could be swallowed.** It is not, because
  `ExpensesError` derives from `Exception` and not from `OSError` [src: expenses/money.py] — but
  if a future change makes it an `OSError` subclass, `save` would start reporting other people's
  refusals as `cannot write`. Named here because it is invisible at the call site.
- **Cleanup order in the test.** If the `chmod 0o700` restore is registered before the temporary
  directory's cleanup rather than after, teardown fails and the failure looks like an unrelated
  error in another test. It is the one thing in step 3 that is easy to get backwards.

## Out of scope for this item

- **A unit test in `tests/test_store.py` calling `save` on an unwritable path directly.** AC4 asks
  for a regression at the level of AC1, which is the command, and the CLI test exercises the same
  code. Adding a second one would be untested-against-criteria work.
- **`load`'s behaviour and its message.** It already does what this item asks of `save`
  [src: expenses/store.py], and it is what the fix is being made to match.
- **Any other `OSError` in the process** — printing to a closed pipe, an unreadable
  `XDG_DATA_HOME`, a failure inside `argparse`. ADR-0008 puts the boundary at functions in
  `store.py` that touch the dataset file, and nothing else in this item extends it.
- **Locking, or two processes writing at once.** The product is one person on one machine
  [src: docs/product/vision.md], and the atomic replace this plan preserves is the whole of the
  concurrency story.
