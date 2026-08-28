# Verification report — BUG-0001

Verified-commit: d80c35a562faad3155b195234e3ff5b3061c834e

## Verdict

**Pass.** All three acceptance criteria are met, each decided by a command run in this execution
against `d80c35a` with the output quoted below. Every fixture was built here, with `mkdir`,
`chmod` and `ln -s` in a scratch tree, rather than through `tests/support.py` — so the criteria are
decided independently of the test helpers the item's own regression test uses.

One defect was found that BUG-0001 neither causes nor claims to fix, and is filed as **BUG-0004**
against WI-0002. It is not a send-back; the reasoning is in `## Defects found`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| **AC1** — either mode against a folder the process cannot read: a message naming it on stderr, nothing on stdout, no traceback, and a status the tool documents | **pass** | Four runs over two fixtures I built (`mkdir` + `chmod 000`, one with two files inside, one empty), each in preview and `--apply`: `python3 -m tidy /tmp/v-bug1/locked`, `... --apply`, `python3 -m tidy /tmp/v-bug1/locked-empty`, `... --apply` | All four identical in shape: `exit: 2`; `stdout: ''` (**0 bytes**); `stderr: 'tidy: /tmp/v-bug1/locked cannot be read: Permission denied\n'` (path substituted per fixture); `'Traceback' in stdout → False`, `in stderr → False` | Every one of the four observables checked programmatically, not by eye. The empty-folder fixture is there because "nothing to move" and "cannot be read" are different runs that could plausibly have been conflated; they are not. "A status the tool documents" resolves to 2 via AC2 |
| **AC2** — `README.md`'s exit-status paragraph states what this case exits with, so contract and behaviour agree | **pass** | Read `README.md:31-34`; then exercised **every case that paragraph names**: a folder with a file to move, an empty folder, a missing path, a plain file, and an unreadable folder | The paragraph: *"Exit status is 0 on success — including when there was nothing to do — 2 when the folder you named cannot be used, which covers all of: it does not exist, it is not a folder, or it cannot be read — and 1 when some file could not be moved while others were."* The runs: success → **0**; nothing to do → **0**; does not exist → **2**; not a folder → **2**; cannot be read → **2** | Contract and behaviour agree on every case the paragraph makes a claim about, not only on the new one. The one `exit`-shaped string in `--help` is argparse's own `show this help message and exit`, so `--help` makes no competing exit-status claim |
| **AC3** — a regression test in `tests/` creates an unreadable folder, asserts AC1's observables, fails when the handling is removed, and skips itself where `chmod 000` does not deny the read | **pass** | `grep -rn chmod tests/` located exactly one such test; read it in full; ran it alone (`python3 -m unittest -v tests.test_cli.BadTargetTests.test_an_unreadable_folder_exits_2_without_a_traceback`); then five mutations of `tidy/cli.py` and one of the test's own `chmod` | Baseline: `OK` — it **runs** here rather than skipping (`id -u` → 1000, so the mode bites). All five mutations break it, and the skip branch fires correctly when the read is made to succeed. Both tables below | The test asserts status 2, `stdout == ""`, the path in stderr, and no `Traceback` in either stream, for `[folder]` and `[folder, "--apply"]` — AC1's observables plus the status |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on `d80c35a`, after clearing every `__pycache__` → exit **0**, `Ran 64 tests in 0.057s`, `OK` with no skips |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit **0** |
| `workspace-valid` | **pass** | `validate-workspace` → `checked 8 item(s), 8 document(s)`, **0 errors, 0 warnings**, after BUG-0004 was filled in and the board regenerated |
| `every-criterion-independently-checked` | **pass** | Each of AC1-AC3 has a command in the table above that I ran here, with its actual output. `impl-report.md` is cited nowhere as evidence; it was read, and where its claims overlap mine they agree — see `## Notes on the implementation report` |
| `negative-cases-exercised` | **pass** | Eleven conditions triggered, not read about — see `## Negative and boundary cases exercised`. AC1 is entirely a negative case, and it was produced with `chmod`, `ln -s` and a relative path rather than asserted about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Five independent mutations of `tidy/cli.py`, each confirmed present in the file before the test ran, each breaking it — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Every row is a condition I created and ran, on `d80c35a`. "clean" means: no `Traceback` in either
stream.

| # | condition | result |
|---|-----------|--------|
| 1 | folder at mode 000 with two files inside, preview | exit 2, stdout 0 bytes, `tidy: <path> cannot be read: Permission denied`, clean |
| 2 | the same, `--apply` | identical to 1 |
| 3 | **empty** folder at mode 000, preview and `--apply` | exit 2, stdout 0 bytes, same message, clean |
| 4 | folder **readable but not executable** (mode 400), preview and `--apply` | exit 2, same message, clean — the mode-400 case reaches the same handler rather than a different failure |
| 5 | folder **executable but not readable** (mode 100) | exit 2, same message, clean |
| 6 | **symlink pointing at** an unreadable folder | exit 2, message names the **link** path as given on the command line, clean |
| 7 | **dangling symlink as the target itself** | exit 2, `tidy: <path> is not a folder` — falls to the pre-existing `isdir` branch, which is correct and unchanged |
| 8 | **relative** path to an unreadable folder, run from another cwd | exit 2, `tidy: rel cannot be read: Permission denied` — the message repeats the path as given, it does not absolutise it |
| 9 | readable folder containing an **unreadable subfolder** | exit **0**, `move photo.jpg -> recent/images/photo.jpg` — subfolders are skipped without being stat'd, so no regression here |
| 10 | readable folder containing a **dangling symlink** | exit 2, `tidy: <folder> cannot be read: No such file or directory` — **the defect filed as BUG-0004** |
| 11 | the full documented contract: success / nothing-to-do / missing / not-a-folder / unreadable | 0 / 0 / 2 / 2 / 2 — matches `README.md` exactly |

Case 9 is the one I most expected to have regressed and it has not. Cases 4, 5 and 6 matter
because ADR-0006 chose `except OSError` over `except PermissionError` specifically so that the
whole class would be handled; they are that claim, tested.

## Test sensitivity check

Each mutation was applied to `tidy/cli.py`, **confirmed present in the file**, the test run alone,
and the file restored with `git checkout --`. All runs used `PYTHONDONTWRITEBYTECODE=1` with the
caches cleared first, because identical-length mutations are otherwise masked by a stale `.pyc`.
The full 64-test suite was green after every restore.

| mutation of `tidy/cli.py` | test result |
|---------------------------|-------------|
| M1 — the whole `try`/`except` removed, back to a bare `actions = build_plan(folder)` | **errors (2)** — `PermissionError` escapes through the test helper, once per subTest |
| M2 — the handler returns **1** (the old, wrong status) instead of 2 | **failures (2)** |
| M3 — the message goes to **stdout** instead of stderr | **failures (2)** |
| M4 — the message **omits the folder path**, keeping the OS reason | **failures (2)** |
| M5 — `except OSError` narrowed to `except FileNotFoundError`, so `PermissionError` escapes again | **errors (2)** |

M2, M3 and M4 are each aimed at exactly one of AC1's observables, so the test is sensitive to
them individually rather than only to the handler's wholesale removal.

**The skip clause, exercised.** I cannot become root, so I produced the condition AC3 actually
names — a read that succeeds despite the `chmod` — by changing the test's own
`os.chmod(unreadable, 0)` to `os.chmod(unreadable, 0o700)` and running it:

```
test_an_unreadable_folder_exits_2_without_a_traceback ... skipped 'the read succeeded at mode
000: running as root, or on a filesystem that does not enforce the mode'
OK (skipped=1)
```

It skips with a stated reason rather than failing, which is what AC3 requires. The test decides
this by attempting the read, not by testing the euid, so the same branch is what root would take.

## Defects found

**BUG-0004 — one dangling symlink stops the whole folder being tidied.** Filed at `ready`,
`found-in: WI-0002`, priority medium.

A readable folder containing a dangling symlink is refused entirely: `build_plan` calls
`entry.stat()` on every entry to compute its age band, `stat` on a symlink with no target raises
`FileNotFoundError`, and the whole scan aborts. The ordinary files in the folder are never
mentioned. On `d80c35a` the user is told `tidy: <folder> cannot be read: No such file or
directory` and gets exit 2 — a calm sentence that is false, because the folder was read fine.

**Why this is a bug against WI-0002 and not a send-back on BUG-0001.** The procedure's test is
whether an acceptance criterion of *this* item says the behaviour should be different. BUG-0001's
AC1 governs "a folder the process cannot read"; this folder can be read. AC2 and AC3 concern
`README.md` and the regression test. None is contradicted.

**Why WI-0002 and not WI-0001**, established by running rather than by reading:

| tree | result on the same fixture |
|------|---------------------------|
| `2a4b928~1` — the commit before WI-0002 added `entry.stat()` | exit **0**, both files previewed: `move broken.pdf -> documents/broken.pdf`, `move photo.jpg -> images/photo.jpg` |
| `main` (`e96c5e2`) | exit **1**, uncaught `FileNotFoundError` out of `planner.py:55` |
| `wi/BUG-0001` (`d80c35a`) | exit **2**, the false "cannot be read" message |

`git log -S "entry.stat()" -- tidy/planner.py` returns exactly one commit, `2a4b928`, which is
WI-0002's. The two comparison trees were detached worktrees under the gitignored `.harness/`, both
removed afterwards.

**BUG-0001 changed this defect's symptom without causing it, and arguably made it harder to
notice** — a traceback advertises itself and a wrong sentence does not. That is an argument for
fixing BUG-0004, not for reversing BUG-0001, and BUG-0004 says so explicitly so that a later
reader does not treat it as grounds to unpick this item. The gap was *declared* in advance:
BUG-0001's `plan.md` `## Out of scope` names "a file that disappears or becomes unreadable partway
through a scan", ADR-0006 `## Consequences` names the misleading-message cost of the broad
`except OSError`, and `impl-report.md` `## What I did not do` repeats it. A declared gap that then
turns out to be reachable with two shell commands is worth an item.

## The diff, read against the plan

`git diff main..wi/BUG-0001 -- ':!tracker/'` is three hunks and I can account for all of them:

| hunk | accounted for by |
|------|------------------|
| `tidy/cli.py` — the `try`/`except OSError` and its comment | plan step 1, and ADR-0006's decision including both details the comment restates |
| `README.md` — the exit-status paragraph | plan step 3, and ADR-0006 §3 (rewritten as one rule, not appended to) |
| `tests/test_cli.py` — the new test | plan step 4 |
| `tests/test_cli.py` — the module docstring gaining `and BUG-0001 AC1 and AC3` | **not in the plan**; declared as deviation 1 in `impl-report.md`. One line, describing the contents of the file step 4 edits. Not a finding: leaving it would have made the file state something false about itself as a direct result of this change |

Nothing in the code is unaccounted for by a criterion or a plan step, and the tracker hunks are
this execution's own record. Plan step 2 was a prohibition rather than an edit and was honoured.

## Notes on the implementation report

Read after the criteria, and checked rather than trusted. Every claim in it that I re-ran held:
the 64-test count, both gate commands, the by-hand AC1 run, and four of my five mutations overlap
its four and agree. Its `## What I did not do` is accurate, including the entry it declares that
became BUG-0004.

Two things worth recording, neither a defect:

1. Its `## Gates` row for `workspace-valid` cites the run made by `transition`, not one the
   developer made separately. That is the same command and the same result, and it is labelled as
   such rather than presented as an independent check.
2. It documents, at some length, two false negatives during its own mutation testing — a stale
   `.pyc` and a mis-anchored `str.replace`. I hit the first of these independently before reading
   that section (the suite failed 4 tests after a restore that had in fact succeeded), which is
   why every mutation here was confirmed present in the file before its test ran. A report that
   records how its own evidence misled it is more useful than one that does not, and this is the
   opposite of the WI-0002 case where a report's mutation claim did not survive checking.

## Not verified, and why

- **AC3 under an actual root user, or on a filesystem that ignores the mode.** I cannot become
  root here (`id -u` → 1000) and have no such filesystem. What I verified instead is the branch's
  *trigger*: the test decides by attempting the read, and when I made that read succeed it skipped
  with its stated reason. The inference from "the read succeeded" to "as root it will skip" rests
  on root being able to read a mode-000 directory, which I did not demonstrate.
- **The `except OSError` clause against failure modes other than permission and `ENOENT`.** A
  vanished mount, an `EIO` from failing hardware, a name that stops being a directory between the
  `isdir` check and the scan — ADR-0006 §1 names all of these as reasons for the broad clause. I
  exercised `EACCES` (cases 1-6, 8) and `ENOENT` (case 10) and could not manufacture the rest here.
  They share the code path, so the risk is low, but it is inference and not evidence.
- **The time-of-check-to-time-of-use race** ADR-0006 option E was rejected to avoid: a folder that
  becomes unreadable between `os.path.isdir` and `os.scandir`. Producing it reliably needs a second
  process racing the first, which I judged out of proportion to the risk — the handler's coverage
  of it follows from the same `except` clause the eleven cases above exercise.
- **BUG-0004's own acceptance criteria.** They are unticked and were not evaluated; filing an item
  is not verifying it. That is a later `verify` execution's work.
- **Anything about BUG-0002 or BUG-0003.** Both are open against behaviour this item does not
  touch. In particular the `--help` text is still wrong about age routing, and this item correctly
  left it alone — `git diff main..wi/BUG-0001 -- tidy/cli.py` shows no change to the `description`
  or `epilog` strings, which is plan step 2 honoured.
