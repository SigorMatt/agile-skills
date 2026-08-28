# Plan — BUG-0004 One dangling symlink stops the whole folder being tidied

## Problem

One entry the filesystem will not describe costs the user the entire folder. `build_plan` asks
each entry two questions — `entry.is_dir()` and `entry.stat()` — and both raise `OSError` for an
entry whose target is gone or whose link points at itself [src: tidy/planner.py:47;
src: tidy/planner.py:55]. Nothing in the loop catches it, so the exception leaves `build_plan`
and lands in `cli.py`'s `except OSError`, where ADR-0006's handler — written for a folder that
cannot be listed — reports the *target folder* as unreadable and exits 2 [src: tidy/cli.py:67;
src: ADR-0006]. The user gets one confident false sentence, an empty stdout, and none of their
ordinary files tidied [src: run: python3 -m tidy /tmp/bug4 → exit 2, "tidy: /tmp/bug4 cannot be
read: No such file or directory", stdout empty]. The change is for that user: the entry that
cannot be examined should cost them that entry and nothing else. It is constrained on three
sides — ADR-0002 keeps every per-entry decision in `planner.py` [src: ADR-0002], ADR-0006's
target-level boundary must keep working exactly as BUG-0001 left it [src: ADR-0006;
src: BUG-0001], and the exit status must stay one `README.md` documents [src: BUG-0004 AC3].

## Approach

`build_plan` gains one guard around the two calls that interrogate an entry. An `OSError` from
either becomes a `leave` action for that entry, and the loop continues:

```
leave  broken.pdf   [cannot be examined: No such file or directory]
move   photo.jpg -> recent/images/photo.jpg
```

That is ADR-0009, and it is the only decision this item forces. The alternatives are costed
there: skipping the entry silently (breaks the preview's promise), ageing symlinks by the link
instead of its target (changes behaviour WI-0002's review accepted, and does not fix the class),
and keeping the abort while improving the message (leaves AC1 exactly as it is).

Three properties of the guard are fixed by the ADR and are not the developer's to re-decide.
It wraps `entry.is_dir()` and `entry.stat()` and nothing else — the collision helpers call
`os.path.lexists` and `os.path.isdir`, which return rather than raise [src: tidy/planner.py:85;
src: tidy/planner.py:114]. `os.scandir(folder)` stays **outside** it, because listing the target
is ADR-0006's case and BUG-0001's regression test asserts that behaviour [src: ADR-0006;
src: tests/test_cli.py]. And the clause is `except OSError`, not `except FileNotFoundError`: the
symlink loop reaches the user identically today and raises `ELOOP` from `is_dir()`, one call
earlier than the item's own fixture [src: run: python3 -m tidy /tmp/bug4loop → exit 2, "tidy:
/tmp/bug4loop cannot be read: Too many levels of symbolic links"].

The reason string is `"cannot be examined: %s" % (error.strerror or error)`. Three things about
it are deliberate. It carries the operating system's own words, which is ADR-0006 detail 2
applied one level down [src: ADR-0006]. It names no cause — `ENOENT` on an entry `scandir` just
listed is usually a broken symlink and sometimes a file deleted mid-scan, and the planner cannot
tell which. And it does not contain the phrase `cannot be read`, which is the string BUG-0004 AC2
forbids anywhere in either stream [src: BUG-0004 AC2].

The exit status does not move. A `leave` is a planned outcome rather than a failed move, and only
a `"failed"` outcome from `apply_plan` makes the process exit non-zero [src: ADR-0007;
src: tidy/cli.py:93], so the fixture exits **0** in both modes. `README.md` is amended to say so:
its exit-status paragraph currently reads "0 on success — including when there was nothing to do"
[src: README.md], which does not tell a reader which case a run that *left* files belongs to.

Layering is untouched. No module gains an import, `apply.py` is not opened, and `planner.py`
still writes nothing [src: ADR-0002; src: docs/architecture/overview.md].

## Steps

1. **`tidy/planner.py` — guard the two calls that interrogate an entry.** Inside `build_plan`'s
   `for entry in listing:` body, arrange that an `OSError` raised by `entry.is_dir()` (line 47)
   or `entry.stat()` (line 55) appends
   `Action(kind="leave", name=name, reason=_unexaminable_reason(error))` and continues with the
   next entry. Add the module-level helper beside `_no_rule_reason`:

   ```python
   def _unexaminable_reason(error):
       """What to say about an entry the filesystem would not describe (ADR-0009)."""
       return "cannot be examined: %s" % (error.strerror or error)
   ```

   Whether that is one `try`/`except` around the interrogation or two is yours, subject to three
   things the ADR fixes: `os.scandir(folder)` stays outside any guard you add; no call that can
   raise an `OSError` about something *other than this entry* may sit inside one; and the
   existing order is preserved, so an unrecognised extension is still reported as
   `[no rule for '.xyz']` and is never aged [src: tidy/planner.py:50]. Afterwards,
   `python3 -m tidy <folder>` over a folder holding `photo.jpg` and a dangling `broken.pdf`
   prints a `leave` line for `broken.pdf`, a `move` line for `photo.jpg`, and exits 0.

2. **`tests/test_cli.py` — the end-to-end regression test.** Add a class
   `UnexaminableEntryTests(FolderTestCase)` with one test that builds the item's fixture — an
   ordinary `photo.jpg` and a symlink `broken.pdf` pointing at a path that does not exist — and,
   for both `[folder]` and `[folder, "--apply"]`, asserts: the status is `0`; a move line names
   `photo.jpg`; the string `cannot be read` appears in neither `result.stdout` nor
   `result.stderr`; and `Traceback` appears in neither. Use `subTest(argv=argv)` as
   `BadTargetTests` does [src: tests/test_cli.py].

   Skipping where symlinks cannot be made: create the link inside a `try`, and on `OSError`,
   `NotImplementedError` or `AttributeError` call `self.skipTest(...)` with a reason naming
   symlink creation — the same shape `test_an_unreadable_folder_exits_2_without_a_traceback`
   uses for a mode that does not bite [src: tests/test_cli.py]. Do not gate on the platform name;
   gate on the operation failing.

   In `--apply` mode assert as well that `photo.jpg` really landed under its band and that
   `broken.pdf` is still in the top level of the folder, so "the rest of the folder was tidied"
   is measured on disk rather than in the output.

3. **`tests/test_planner.py` — the reason string is the planner's contract.** Add one test to
   `ScanTests` (or a class beside it) building the same fixture and asserting that `build_plan`
   returns, for the dangling entry, an action with `kind == "leave"`, `name == "broken.pdf"` and a
   `reason` that starts with `cannot be examined:` and contains the operating system's reason for
   that errno — take it from `os.strerror(errno.ENOENT)` rather than writing the English out, so
   the test does not depend on the locale or on the platform's wording. Same skip shape as step 2.

4. **`README.md` — say which case this run is.** Two edits, and no others in this file:

   - In `## What it does`, add one line to the example block and one sentence under it. The line:

     ```
     leave  broken.pdf   [cannot be examined: No such file or directory]
     ```

     The sentence, after the existing "A `move` line names the file ..." paragraph: "An entry
     tidy cannot examine — a broken symbolic link, most often — gets a `leave` line carrying the
     reason the operating system gave, and does not stop the rest of the folder being tidied."

   - In the exit-status paragraph, extend the first clause only, so it reads: "Exit status is 0 on
     success — including when there was nothing to do, and when some files were left where they
     are". Leave the `2` clause and the `1` clause exactly as they are: the `1` clause is
     BUG-0005's subject and rewriting it here would make two items unverifiable against their own
     criteria [src: BUG-0005].

5. **Show the tests fail without the guard.** Revert step 1 only — `git checkout <trunk> --
   tidy/planner.py` — leaving the new tests and the README in place, and confirm that both new
   tests fail while the other 69 pass; then restore. Record both outputs in `impl-report.md`. Two
   hazards, both of which have produced a false pass in this project before: run with
   `PYTHONDONTWRITEBYTECODE=1` and delete `tidy/__pycache__` and `tests/__pycache__` first, and
   read `tidy/planner.py` back to confirm the revert is actually in the file before running.

6. **Run the gates and report.** From the repository root:
   `python3 -m unittest discover -s tests -t . -q`, `python3 -m compileall -q tidy tests`,
   `.claude/agile-skills/scripts/lint-claims --changed-since main`, and
   `.claude/agile-skills/scripts/validate-workspace .`. Run the item's own
   `## Steps to reproduce` verbatim and paste both runs — preview and `--apply`, with their exit
   statuses — into `impl-report.md`, since the item's evidence is what a user sees.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — either mode still reports every other file in the folder | 1 | The step-2 test, both modes: a move line names `photo.jpg`, and in `--apply` the file is on disk under its band while `broken.pdf` is still where it was. Plus the item's `## Steps to reproduce` run verbatim in step 6 and pasted into `impl-report.md`, where stdout now names both files |
| AC2 — no output states or implies the folder could not be read | 1 | The step-2 test asserts `cannot be read` is absent from `result.stdout` **and** `result.stderr` in both modes, and that `Traceback` is absent from both. The reason string chosen in `## Approach` does not contain the phrase, which is why the assertion can hold at all |
| AC3 — the exit status is one `README.md` documents, and `README.md` says which case it belongs to | 1, 4 | The step-2 test asserts `result.status == 0` in both modes; step 4 makes `README.md`'s exit-status paragraph name this case — "0 on success ... and when some files were left where they are" — so the status and the document agree. Checkable by `python3 -m tidy /tmp/dangling; echo $?` → `0` read against `README.md`'s exit-status paragraph |
| AC4 — a regression test builds the fixture, asserts AC1 and AC2, fails when the handling is removed, and skips where symlinks cannot be created | 2, 3, 5 | The step-2 test is the one AC4 names; the step-3 test pins the reason string that AC2 depends on. Step 5 records both failing against the reverted `planner.py` — the pre-fix code aborts, so `run()` returns status 2 with `cannot be read` on stderr and no `photo.jpg` line, failing AC1's and AC2's assertions together. The skip is by attempted operation, not by platform name |

## Assumptions

- **The reason wording is `cannot be examined: <the OS's reason>`.** Any wording works for the
  criteria provided it avoids the forbidden phrase and names the OS's reason; this one is chosen
  to sit beside the existing `no rule for '.xyz'` and `'old/documents' exists and is not a folder`
  [src: tidy/planner.py:65; src: tidy/planner.py:94]. Reversing is one string in one helper and
  one assertion in `tests/test_planner.py`, with no other consequence.
- **A run with an unexaminable entry exits 0 rather than gaining a status of its own.** It
  follows from ADR-0007 — the exit status turns on a `"failed"` outcome from `apply_plan`, and a
  `leave` produces none [src: ADR-0007] — and from `README.md` already treating a `leave` as an
  ordinary part of a successful run [src: README.md]. Reversing means a new documented status,
  which is a decision for the human and not a plan step.
- **Symlinks keep being aged by their target's `mtime`.** Unchanged by this item; the guard only
  decides what happens when that read fails. WI-0002's review examined this and accepted it
  [src: WI-0002]. Reversing is one keyword argument in `planner.py`, but it is a behaviour change
  no criterion asks for and it needs its own item.
- **The regression tests live in `tests/test_cli.py` and `tests/test_planner.py`.** AC4 asks for
  a test in `tests/`; the end-to-end assertions belong where `run()` is already used and the
  reason string belongs where `build_plan` is called directly [src: tests/test_cli.py;
  src: tests/test_planner.py]. Reversing is moving a test function.

## Decisions and ADRs

| decision | where |
|----------|-------|
| An `OSError` from one entry becomes a `leave` action inside `build_plan`; the run continues | ADR-0009 (new), `## Decision` |
| Silently skipping the entry, ageing symlinks by the link, and keeping the abort with a better message — all rejected, with costs | ADR-0009 `## Options considered`, B, C and D |
| The guard covers `is_dir()` and `stat()` only; `os.scandir` stays outside; the clause is `OSError`; the reason carries the OS's words | ADR-0009 `## Decision`, details 1-4 |
| The exit status stays 0, and `README.md` says which case that is | ADR-0009 `## Decision`, last paragraph; step 4 above |
| Reason wording, test placement, symlink ageing left alone | `## Assumptions` above |

`docs/architecture/overview.md` goes to version 7 in this execution: one paragraph recording that
the system now has two error boundaries at different levels — the target folder's, which ends the
run at the CLI, and one entry's, which is data the planner returns. That is a rule about the shape
of the system rather than a detail of this fix, which is why it is in the overview and not only in
the ADR.

`tracker/project.yaml` already names a real test and lint command, both re-run in step 6; this
execution does not change it [src: tracker/project.yaml; src: ADR-0004].

## Scaffolding

none.

## Risks

- **BUG-0005 edits the same paragraph.** It is open against `README.md`'s exit-status sentence for
  the case where *every* move fails [src: BUG-0005]. Step 4 deliberately touches only the `0`
  clause and leaves the `1` clause alone; if the two items are implemented close together, the
  second one to land must re-read the paragraph rather than reapply a remembered diff.
- **The guard can be written too widely.** A `try` that wraps the collision helpers as well would
  turn a genuine defect in destination selection into a `leave` line — the same cost ADR-0006
  names at the target level, one level down and harder to spot because the run still looks
  successful. Step 1 names the two calls it may cover; a reviewer should check the diff against
  that sentence rather than against the behaviour, because the behaviour is identical either way
  until something else breaks.
- **A test that passes for the wrong reason.** If the fixture's symlink is created with a name
  whose extension has no rule — `broken.xyz` rather than `broken.pdf` — the entry never reaches
  `entry.stat()` at all [src: tidy/planner.py:50], the run passes on today's code, and the test
  guards nothing. Step 5 is what catches that: the pre-fix code must fail these tests. The item's
  own fixture uses `.pdf`, which is why.
- **The symlink loop case is fixed by the same guard but is not in any criterion.** It is
  reproduced in ADR-0009 `## Context` and it raises from `is_dir()` rather than `stat()`, so a
  guard written around `stat()` alone would leave it aborting while every criterion passed. Worth
  a boundary case in verification even though no AC names it.
- **`run()` is in-process** [src: tests/cli_support.py], so an exception the CLI does not catch
  propagates out of `run()` and errors the test rather than appearing as a traceback in
  `result.stderr`. AC2's "no traceback" assertion is therefore a check on the *handled* path; the
  unhandled one shows up as a test error instead, which is louder rather than quieter.

## Out of scope for this item

- Changing how symlinks are aged, in either direction. WI-0002's review accepted ageing them by
  their target and no criterion here disturbs it [src: WI-0002].
- BUG-0005's exit-status sentence, and any other edit to `README.md` beyond the two in step 4
  [src: BUG-0005].
- ADR-0006's target-level boundary and BUG-0001's message. This item must leave both exactly as
  they are, and step 1 says how [src: ADR-0006; src: BUG-0001].
- WI-0003 (user-supplied rules), which changes where the tables come from and touches none of
  this [src: WI-0003].
- Recursing into subfolders, undo, or anything else on the epic's out-of-scope list [src: EP-001].
