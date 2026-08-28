---
id: BUG-0001
type: bug
title: A folder tidy cannot read crashes with a Python traceback instead of a message
status: done
priority: medium
epic: EP-001
created: "2026-08-27T16:30:45Z"
updated: "2026-08-27T19:40:52Z"
found-in: WI-0001
branch: wi/BUG-0001
outcome: delivered
---

## Summary

Pointing `tidy` at a folder the user is not permitted to read makes it die with an uncaught
`PermissionError` traceback and exit **1**. Found on branch `wi/WI-0001` at commit
`6b1873161b148392d8ee5cb6ff5824a4ab404289` while verifying WI-0001, in both PREVIEW and APPLY
mode. `os.scandir` raises out of `build_plan` (`tidy/planner.py:35`) and nothing catches it;
`tidy/cli.py` validates only `os.path.isdir` (AC14) before calling it.

No WI-0001 acceptance criterion covers this case — AC14 names a missing path and a regular file
only — so this is not a failure of WI-0001, which is why it is filed here rather than sent back.
WI-0001's `impl-report.md` `## What I did not do` predicted it as "a candidate bug item"; this
item is that candidate, confirmed by running it.

## Steps to reproduce

1. Check out `wi/WI-0001` (or `main` once WI-0001 is merged) and work from the repository root.
2. Create an unreadable folder with a file in it:

   ```
   mkdir -p /tmp/unreadable && echo x > /tmp/unreadable/photo.jpg && chmod 000 /tmp/unreadable
   ```

3. Run the preview: `python3 -m tidy /tmp/unreadable`
4. Run the apply too: `python3 -m tidy /tmp/unreadable --apply`
5. Clean up: `chmod 755 /tmp/unreadable`

Steps 3 and 4 behave identically. Run as a non-root user; root bypasses the permission check.

## Expected behaviour

A message naming the folder on stderr, nothing on stdout, and a documented exit status —
consistent with how the tool already handles the other two unusable targets.

`README.md` states the exit-status contract: "Exit status is 0 on success — including when there
was nothing to do — 2 when the folder you named does not exist or is not a folder, and 1 when
some file could not be moved while others were." An unreadable folder is neither of the cases
`README.md` assigns to 1, so the current exit 1 contradicts the documented contract, and a
traceback is not "a message" under any reading of it. `WI-0001` AC14 is the shape the answer
should take — stderr names the path, stdout is empty, the exit status is deliberate — but AC14's
own wording does not extend to this case, which is why WI-0001 passes verification with the
defect present.

Which exit status it should use is for `plan` to decide: 2 treats it as another unusable target,
and a distinct code says something different happened. Both are defensible and neither is
constrained by an existing criterion, so AC1 below fixes the observable behaviour and leaves the
number to the design.

## Actual behaviour

```
$ python3 -m tidy .harness/fperm
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/msi/agile-skills-throwaway/tidy/tidy/__main__.py", line 3, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File "/home/msi/agile-skills-throwaway/tidy/tidy/cli.py", line 59, in main
    actions = build_plan(folder)
              ^^^^^^^^^^^^^^^^^^
  File "/home/msi/agile-skills-throwaway/tidy/tidy/planner.py", line 35, in build_plan
    with os.scandir(folder) as entries:
         ^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: '.harness/fperm'
$ echo $?
1
```

`python3 -m tidy .harness/fperm --apply` produces the same traceback and the same exit 1.

## Acceptance criteria

- [x] AC1 — Running either mode against a folder the process cannot read writes a message naming
      that folder to stderr, writes **nothing** to stdout, prints no Python traceback, and exits
      with a status the tool documents. Checkable by the steps above: stdout is empty, stderr
      contains the folder's path, and `Traceback` appears nowhere in either stream.
- [x] AC2 — `README.md`'s exit-status paragraph states what this case exits with, so the
      documented contract and the behaviour agree.
- [x] AC3 — A regression test in `tests/` creates an unreadable folder, asserts AC1's three
      observables, and fails when the handling is removed. It skips itself when run as root,
      where `chmod 000` does not deny the read.

## Gaps accepted at review

Recorded here rather than left in the reports, because once an item is `done` nobody reads its
verification report again. Seven gaps, none of them blocking; `review.md` has the reasoning.

1. **AC3's skip branch has never actually run.** This environment is uid 1000 on a filesystem that
   enforces the mode, so the test always takes the assert path. `verify` produced the *condition*
   instead — it made the read succeed and watched the test report `skipped` with its stated reason
   — but nobody has run it as root. The inference from "the read succeeded" to "root will skip"
   rests on root being able to read a mode-000 directory, which was not demonstrated.
2. **The `except OSError` clause is exercised for `EACCES` and `ENOENT` only.** ADR-0006 §1 chose
   the broad clause to cover a vanished mount, an `EIO`, and a name that stops being a directory
   mid-run. Those share the code path with the two that were tested, so the risk is low — but it
   is inference, not evidence.
3. **The time-of-check-to-time-of-use race is unexercised.** ADR-0006 rejected option E (an
   `os.access` pre-check) specifically to avoid it. Producing it needs a second process racing the
   first; `verify` judged that out of proportion and said so.
4. **A single unstattable entry still aborts the whole scan**, and the message blames the folder.
   Reachable with two shell commands; filed as **BUG-0004** against WI-0002. BUG-0001's plan scoped
   it out in advance and ADR-0006 `## Consequences` named it as the cost of the broad clause. This
   item made the symptom *quieter* — a traceback became a calm false sentence — which is an
   argument for fixing BUG-0004, not for reversing this item.
5. **The comment above the new handler frames it too narrowly.** It opens "Listing the target is
   the last thing that can make it unusable", but `entry.stat()` inside `build_plan` can fail too,
   and when it does this handler blames the target folder. The code is right and the sentence is
   not quite. Not worth a round trip on its own: it is the same misconception as gap 4, and
   whoever fixes **BUG-0004** has to rewrite this comment anyway.
6. **`--help` is still wrong about age routing.** Deliberately untouched — plan step 2 forbids it
   and **BUG-0003** owns it. `git diff main..wi/BUG-0001 -- tidy/cli.py` shows no change to the
   `description` or `epilog` strings.
7. **The unreadable case has no exit status of its own.** ADR-0006 option B, rejected there; a
   script cannot tell "no such folder" from "cannot read it" by status alone, only from stderr.
   Additive later if anyone asks.


## Notes

Filed by `verify` while verifying WI-0001; `found-in: WI-0001` names the item that delivered
`build_plan`. WI-0001 itself passes every one of its own criteria — see
`tracker/items/WI-0001/artifacts/verify-report.md`.

A second unspecified failure mode was found in the same execution and is filed separately as
BUG-0002; they are unrelated faults in different modules and each needs its own reproduction.
