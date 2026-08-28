# Plan — BUG-0001 A folder tidy cannot read crashes with a Python traceback instead of a message

## Problem

Pointing `tidy` at a folder the process is not permitted to read makes it die with an uncaught
`PermissionError` traceback and exit 1, in both PREVIEW and APPLY mode [src: BUG-0001]. The user
sees a stack trace naming `os.scandir` and three files of ours; what they asked for was to tidy a
folder, and what they need to be told is that this one cannot be read. The exit status is wrong as
well as ugly: `README.md` assigns 1 to "some file could not be moved while others were", and here
nothing was even planned [src: README.md; src: BUG-0001].

`tidy/cli.py` checks `os.path.isdir(folder)` and returns 2 when that fails, then calls
`build_plan(folder)`, whose first act is `os.scandir(folder)` — the call that raises
[src: tidy/cli.py; src: tidy/planner.py]. Still live on `main` after WI-0002 merged
[src: run: python3 -m tidy /tmp/bug1repro/unreadable → exit 1, PermissionError traceback].

The constraints are the project's existing ones: Python 3.9+, standard library only, one terminal
command [src: ADR-0001]; the planner decides and the CLI presents [src: ADR-0002]; and the fix must
leave every one of WI-0001's and WI-0002's criteria passing, because this is a bug fix and not a
change of behaviour.

## Approach

One `try`/`except` at the CLI boundary, and one sentence in `README.md`. The decision — exit 2
rather than a new code, caught in `tidy/cli.py` rather than in `tidy/planner.py`, with an `OSError`
clause rather than a `PermissionError` one — is **ADR-0006**, together with the three details it
fixes and what reversing each would cost.

Why the boundary and not the planner: `build_plan` decides destinations and writes nothing, and
`cli.py` is where results become text and exit codes [src: ADR-0002]. A planner that caught the
error would have to invent a return value meaning "the run failed", and `cli.py` would still have
to choose the status — so the decision would not have moved, only the mess. Why not a pre-check
with `os.access`: the folder can stop being readable between the check and the scan, which puts
the traceback back on the very path the check was added to remove (ADR-0006 option E).

`tidy/planner.py` and `tidy/apply.py` are not touched. `apply_plan` is already the module that
lets nothing raise out of it [src: tidy/apply.py], and `build_plan` keeps raising — which is what
makes the CLI's one handler sufficient.

### The interface this plan fixes

A contract, not an implementation. How it is written is the developer's call.

```python
# tidy/cli.py — main() gains one guarded call; its signature does not change
def main(argv=None) -> int      # 2 when the target folder cannot be listed,
                                # after one line on stderr and nothing on stdout
```

`build_plan` and `apply_plan` are unchanged, in signature and in behaviour.

## Steps

1. **`tidy/cli.py` — guard the `build_plan` call.** Wrap `actions = build_plan(folder)` in
   `try`/`except OSError`. In the handler: write exactly one line to stderr naming the folder and
   the operating system's own reason for the failure, write nothing to stdout, and `return 2`.
   Follow the file's existing message shape — the `isdir` branch writes
   `"tidy: %s is not a folder\n"` — so the new line begins `tidy: ` too and carries the folder
   path and the reason. Afterwards: `python3 -m tidy <unreadable-folder>` prints one line on
   stderr, nothing on stdout, no `Traceback`, and exits 2; the same holds with `--apply`
   [src: BUG-0001 AC1].

2. **`tidy/cli.py` — extend the epilog only if step 1's wording needs it.** The `argparse` epilog
   describes preview, the rules table and the invariants; it says nothing about exit statuses
   today [src: tidy/cli.py], so nothing is required here. **Do not** rewrite the description or
   the epilog for any other reason: they are wrong about age routing and that is BUG-0003's
   subject, not this item's. Afterwards: `git diff` shows no change to the `--help` strings that
   BUG-0003 will edit.

3. **`README.md` — restate the exit-status contract as one rule.** In the "What it does" section,
   replace the sentence "Exit status is 0 on success — including when there was nothing to do —
   2 when the folder you named does not exist or is not a folder, and 1 when some file could not
   be moved while others were" so that 2 covers the whole class: the folder does not exist, is not
   a folder, **or cannot be read**. Keep 0 and 1 as they are. Afterwards: a reader comparing
   `README.md` against step 1's behaviour finds them stating the same rule
   [src: BUG-0001 AC2; src: ADR-0006].

4. **`tests/test_cli.py` — the regression test.** Add one test to the existing `BadTargetTests`
   class, which already covers the missing-path and not-a-folder cases through the same `run()`
   helper [src: tests/test_cli.py; src: tests/cli_support.py]. It must:
   - make a folder inside the test's temporary folder, put a file in it, and `os.chmod(path, 0)`;
   - register the restoring `os.chmod(path, 0o700)` with `self.addCleanup` **before** it removes
     the permission, so the temporary directory can still be cleaned up when the assertions fail —
     `addCleanup` runs last-registered-first, and `FolderTestCase.setUp` registers the directory's
     own cleanup first [src: tests/support.py];
   - assert, for both `[folder]` and `[folder, "--apply"]`: `result.status == 2`,
     `result.stdout == ""`, the folder's path appears in `result.stderr`, and `"Traceback"` appears
     in neither stream;
   - **skip itself when the permission cannot be made to bite** — as root, or on a filesystem that
     ignores the mode. Decide that by attempting the read after the `chmod` and skipping when it
     succeeds, rather than by testing `os.geteuid() == 0`: the euid test is a guess about why, and
     the read is the fact. `os.geteuid` also does not exist on every platform this stdlib-only tool
     could run on [src: ADR-0001].

   Afterwards: the test fails on `main` before step 1 (with the `PermissionError` escaping through
   `run()`) and passes after it [src: BUG-0001 AC3].

5. **Run the gates and check the neighbours.** `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q tidy tests` [src: ADR-0004]. Afterwards: 64 tests pass — the 63 on
   `main` plus step 4's — and in particular `BadTargetTests.test_missing_path_and_non_directory_exit_2`
   still passes, which is the criterion this change could most easily break
   [src: tests/test_cli.py].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — either mode against an unreadable folder writes a message naming it to stderr, nothing to stdout, no traceback, and exits with a documented status | 1 | `tests/test_cli.py`: the new test in `BadTargetTests` asserts `status == 2`, `stdout == ""`, the path in `stderr`, and no `"Traceback"` in either stream, for `[folder]` and `[folder, "--apply"]`. By hand: `mkdir -p /tmp/unreadable && echo x > /tmp/unreadable/photo.jpg && chmod 000 /tmp/unreadable && python3 -m tidy /tmp/unreadable; echo $?` prints one `tidy: …` line and `2` |
| AC2 — `README.md`'s exit-status paragraph states what this case exits with | 3 | Reading `README.md`'s "What it does" section against step 1: both say 2 for a folder that cannot be read. The documented rule and the behaviour are compared in the same sentence, so a reviewer can check it without running anything |
| AC3 — a regression test creates an unreadable folder, asserts AC1's three observables, and fails when the handling is removed; it skips itself where `chmod 000` does not deny the read | 4 | `tests/test_cli.py`, the new test in `BadTargetTests`. Sensitivity is shown by reverting step 1 and re-running: the `PermissionError` escapes `run()` and the test errors. The skip is decided by attempting the read after the `chmod`, so it triggers as root and on a mode-ignoring filesystem alike |

Every criterion has a step and a demonstration; no step exists that no criterion maps to — step 2
is a prohibition rather than an edit, and step 5 is the gate run every item performs.

## Assumptions

1. **Exit 2 is the right status**, rather than a new code. Not the stakeholder's to decide: no
   document expresses an intent about exit codes beyond `README.md`'s own contract, and BUG-0001
   AC1 asks for a documented status rather than a specific one [src: BUG-0001 AC1]. Recorded as
   the decision in ADR-0006 rather than as an open question. **To reverse:** one returned constant
   in `tidy/cli.py`, one sentence in `README.md`, one assertion in step 4's test. Cheap.
2. **The message's wording is the developer's**, provided it begins `tidy: `, names the folder, and
   carries the operating system's reason. Nothing downstream parses stderr — the tests assert that
   the path appears in it, not the whole line [src: tests/test_cli.py]. **To reverse:** one format
   string. Cheap.
3. **An `OSError` out of `build_plan` is a filesystem condition, not a defect in our code**, which
   is what makes the broad `except` clause honest. It rests on `build_plan` performing filesystem
   reads and string composition and nothing else [src: tidy/planner.py]. **To reverse:** narrow the
   clause to `PermissionError`, and accept that the other failure modes go back to tracebacks. One
   word. Cheap; ADR-0006 states what it would cost.
4. **The unreadable-folder case is not worth its own exit code**, so nothing distinguishes it from
   "does not exist" except the stderr line. **To reverse:** assumption 1's reversal, plus a third
   sentence in `README.md`. Cheap, and additive rather than breaking.

## Decisions and ADRs

| decision | where it is recorded | route |
|----------|---------------------|-------|
| Exit 2 rather than a new status code | **ADR-0006** (new) `## Decision` | decided here; BUG-0001 left the number to `plan` [src: BUG-0001 AC1] |
| Caught at the CLI boundary, not in the planner and not by an `os.access` pre-check | ADR-0006 `## Options considered` C, D, E | decided here, under ADR-0002's layering [src: ADR-0002] |
| The `except` clause is `OSError`, not `PermissionError` | ADR-0006 `## Decision` §1 | decided here, with the cost stated |
| The message carries the OS's own reason | ADR-0006 `## Decision` §2 | decided here |
| `README.md`'s paragraph is rewritten as one rule, not extended with a third case | ADR-0006 `## Decision` §3 | decided here [src: BUG-0001 AC2] |
| `tidy/planner.py` and `tidy/apply.py` are unchanged | this plan `## Approach` | documented — `build_plan` keeps raising and `apply_plan` already raises nothing [src: tidy/apply.py] |
| The regression test skips by attempting the read, not by testing the euid | this plan step 4 | documented — the read is the fact the skip is about; the euid is a guess at the cause |
| The four assumptions above | `## Assumptions` 1–4 | assumed, each with its reversal cost |
| No ADR for the message's wording | — | it is a format string constrained by three observables; an ADR for it would be padding |

Nothing was asked of the stakeholder, and nothing needed to be. The only question with any product
stake — which exit status — is invisible to a user who reads the message, is documented either way,
and is reversible in three lines; ADR-0006 records the alternative so a later reader can see it was
a choice rather than an oversight.

## Scaffolding

`none`. This plan creates no file outside `tracker/` and `docs/`. `tracker/project.yaml` already
carries commands that run in this project [src: ADR-0004], `tests/` is an existing package, and
step 4 adds a test to a class that already exists.

## Risks

- **The permission does not bite.** As root, or on a filesystem mounted without permission
  enforcement, `chmod 000` does not stop the read, and step 4's test would assert against a folder
  that lists fine. Handled inside the test: it attempts the read after the `chmod` and skips when it
  succeeds. The residual risk is that the case then goes unexercised in that environment, which is
  visible as a skip rather than as a pass.
- **The cleanup can strand a temporary directory.** A folder at mode 000 cannot be removed by
  `TemporaryDirectory.cleanup`. Step 4 registers the restoring `chmod` so it runs before that
  cleanup; getting the `addCleanup` order wrong shows up as an error in teardown rather than
  silently, which is why the ordering is written into the step.
- **A broad `except OSError` could mask a defect inside `build_plan`.** Named in ADR-0006
  `## Consequences` and mitigated by the message carrying the OS's own reason, so a nonsensical
  reason is visible. The alternative — narrowing to `PermissionError` — leaves the other listing
  failures as tracebacks, which is the same defect with a smaller blast radius.
- **The fix is in the one file WI-0002 deliberately did not touch.** `cli.py`'s `--help` strings are
  wrong about age routing [src: BUG-0003], and a developer editing this file will be tempted to fix
  them. Step 2 exists to say: do not. Two items editing the same strings makes both unverifiable
  against their own criteria.

## Out of scope for this item

- **BUG-0002** — a fully successful APPLY exiting 1 on a filesystem that refuses hard links. A
  different module, a different failure, its own criteria [src: BUG-0002].
- **BUG-0003** — the `--help` text still describing sorting by type alone [src: BUG-0003]. Same
  file, unrelated defect; step 2 forbids touching it here.
- **A file that disappears or becomes unreadable partway through a scan.** Step 1's handler will
  catch it, because `entry.stat()` is inside `build_plan`, and the message will name the folder and
  the OS's reason — which is honest but not tailored. No criterion of this item covers it and none
  is added; if per-entry resilience is wanted, that is a new item.
- **Distinguishing the failure modes by exit status.** ADR-0006 option B, rejected there, additive
  later.
- **Any change to what `tidy` does with a folder it *can* read.** This item adds an error path and
  nothing else; WI-0001's and WI-0002's criteria must all still pass, which step 5 checks.
