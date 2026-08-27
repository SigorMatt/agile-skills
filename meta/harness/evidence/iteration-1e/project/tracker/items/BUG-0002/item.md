---
id: BUG-0002
type: bug
title: A write the operating system refuses escapes as a traceback, not a message
status: done
priority: medium
epic: EP-001
created: "2026-08-27T00:16:35Z"
updated: "2026-08-27T02:10:02Z"
found-in: WI-0001
arose-from: WI-0001
branch: wi/BUG-0002
outcome: delivered
---

## Summary

`expenses/store.py` turns an operating-system error into a refusal when it *reads* the dataset,
but not when it *writes* it. `load()` catches `OSError` and raises `ExpensesError`; `save()`
catches nothing. So a store the user cannot write to — a read-only directory, a full disk, a path
owned by someone else — produces an eleven-line Python traceback and exit status 1, instead of
the one-line message on stderr and exit 2 that every other failure of this tool produces.

Found while reviewing WI-0001, by probing the error paths the diff leaves open. No acceptance
criterion of WI-0001 covers it: AC5 and AC6 are about inputs the *user* got wrong, and this is
the environment refusing, which nobody specified. That is why WI-0001 was closed rather than sent
back, and why this is filed as its own item.

Nothing is corrupted when it happens: the write is a temporary file replaced over the target, so
a failure to create the temporary file leaves the previous dataset exactly as it was. The defect
is the presentation, not the data.

## Steps to reproduce

1. Make a directory the current user cannot write to, and point the store at a file inside it:

       mkdir -p /tmp/rc-ro
       chmod 500 /tmp/rc-ro

2. Try to record something:

       EXPENSES_STORE=/tmp/rc-ro/expenses.json python3 -m expenses person add Ana

3. Restore the directory afterwards: `chmod 700 /tmp/rc-ro`.

4. For contrast, the *read* path on the same class of error, which behaves correctly:

       mkdir -p /tmp/rc-dir/expenses.json
       EXPENSES_STORE=/tmp/rc-dir/expenses.json python3 -m expenses person list

## Expected behaviour

Step 2 writes one line to stderr naming the path and what went wrong, writes nothing to stdout,
and exits 2 — the same shape as every other failure. `docs/architecture/overview.md` states that
every refusal writes to stderr, changes nothing on disk and exits non-zero, and that refusals are
turned into a message and an exit code in exactly one place; `expenses/store.py`'s own docstring
says a refusal is an `ExpensesError`. Step 4 already does exactly this.

## Actual behaviour

Step 2:

    $ EXPENSES_STORE=/tmp/rc-ro/expenses.json python3 -m expenses person add Ana
    Traceback (most recent call last):
      File "<frozen runpy>", line 198, in _run_module_as_main
      ...
      File "/home/msi/agile-skills-throwaway/expenses-1e/expenses/store.py", line 61, in save
        handle = tempfile.NamedTemporaryFile(
      ...
    PermissionError: [Errno 13] Permission denied: '/tmp/rc-ro/.expenses-94v6and6.tmp'
    $ echo $?
    1

Step 4, the read path, for contrast:

    $ EXPENSES_STORE=/tmp/rc-dir/expenses.json python3 -m expenses person list
    cannot read /tmp/rc-dir/expenses.json: [Errno 21] Is a directory: '/tmp/rc-dir/expenses.json'
    $ echo $?
    2

## Acceptance criteria

- [x] AC1 — with the store pointed at a file inside a directory the user cannot write to,
      `python3 -m expenses person add Ana` exits 2, writes nothing to stdout, and writes to
      stderr a single line that contains the path and no `Traceback`.
- [x] AC2 — the same holds for `expense add` against the same unwritable store.
- [x] AC3 — the dataset that was there before the attempt is byte-identical afterwards, and no
      leftover temporary file beginning `.expenses-` remains in the directory.
- [x] AC4 — a regression test covers AC1 by making a temporary directory read-only, and it fails
      if the handling is removed. It is skipped when the test process can write regardless of the
      permission bits, so that the suite does not fail for a user running it as root.
- [x] AC5 — `python3 -m unittest discover -s tests -t .` exits 0.

## Notes

- **Priority is medium, not high.** No data is lost or corrupted — the atomic-replace write means
  the previous dataset survives untouched — and the tool still fails rather than pretending to
  succeed. What is wrong is that it fails in a shape the rest of the tool never uses, which is
  exactly the kind of thing a person reads as "the program is broken" rather than "I cannot write
  there".
- **The likely fix is small**, but it is the implementer's to choose: wrapping `save()`'s body so
  that `OSError` becomes an `ExpensesError` naming the path would mirror what `load()` already
  does. Whether the same treatment belongs on `mkdir` is part of the same decision.
- **Why not a send-back to WI-0001.** None of AC1 to AC9 covers an environment error, so there
  was nothing in that item for this to fail against, and sending it back would have asked
  `implement` to add behaviour with no criterion behind it. Recorded in WI-0001's review under
  `## Findings`.
- **Where the contrast comes from.** `load()` gained its `OSError` branch during implementation;
  `save()` did not, and neither the plan nor any ADR asked for either. The asymmetry is the
  finding.

### Added at close by `review-close`

These are the gaps this review accepted rather than sent back. They are here, and not only in
`artifacts/review.md`, because a report stops being read once an item is `done`.

- **`verify`'s docstring finding does not hold, and was not acted on.** `verify` recorded that
  this diff made `tests/test_cli.py`'s module docstring — "each test starts from a store that
  does not exist yet" — inaccurate, because the new fixture records `Zoe` before removing the
  write permission. Opened rather than accepted: seven pre-existing classes (`setUp` at lines
  166, 185, 214, 352, 468, 499 and 555) already record people and expenses through
  `CommandTestCase.succeed`, which calls `main()` in process and writes the file. So the strict
  reading has been inaccurate since WI-0001, and the reading that makes it true of those seven —
  each test's *fixture* starts from a store that does not exist — is true of the new class too.
  Not introduced by this item; not a bug against another one. See `review.md` F1.
- **`lint-clean` checked nothing**, here as everywhere in this project: `commands.lint` is null
  by ADR-0004. No statement is made about style or unused imports in the new code.
- **Only the permission case was ever triggered.** A full disk, a read-only mount and a name too
  long for the file system reach the same `except OSError` by the exception hierarchy; none was
  produced, because nothing in this environment creates them for less than they prove.
- **AC4's skip path was demonstrated by injection**, by making the fixture's directory writable —
  not by running the suite as a user for whom mode 500 is not binding.
- **`os.replace` failing after a successful write has no test.** The cleanup it would run is the
  one AC3 exercises through the `NamedTemporaryFile` failure, but that ordering was never
  produced.
- **`person delete` and `expense delete` against an unwritable store are untested.** They call
  the same `save` and are fixed by the same wrapper; the plan records this as assumption 3.
- **`docs/architecture/overview.md` v7 says "the whole of `save` is inside that boundary".**
  One statement, `target = pathlib.Path(path)` at `expenses/store.py:67`, is above the `try`.
  It performs no file-system access and cannot raise `OSError`, so no claim about behaviour is
  false; `save`'s own docstring puts it exactly ("everything the file system can refuse").
  Not worth a round trip; recorded so nobody re-derives it. See `review.md` F2.
- **One refusal edge the "changes nothing on disk" sentence does not cover.**
  `target.parent.mkdir(parents=True, exist_ok=True)` is inside the boundary, as ADR-0008 §1
  requires — but it creates directories. If the `mkdir` succeeds and the write that follows is
  refused, directories that did not exist before are left behind. Not reproducible with
  permission bits (a directory you may create subdirectories in is one you may create files in),
  so it needs a full disk or a quota. The dataset itself is safe in every case, because
  `os.replace` is the last statement and is never reached. See `review.md` F3.
