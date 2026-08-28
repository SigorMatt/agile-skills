# Implementation report — BUG-0001

## What was built

One `try`/`except` at the CLI boundary, one sentence in `README.md`, one regression test.

`tidy/cli.py` `main()` wraps its `build_plan(folder)` call in `try`/`except OSError`. The handler
writes one line to stderr — `tidy: <folder> cannot be read: <the OS's reason>` — writes nothing to
stdout, and returns 2. That is ADR-0006's decision unchanged: option A (exit 2, the status the
`isdir` check already returns for a target that cannot be used) and option C (caught at the
boundary, not in the planner and not by an `os.access` pre-check), with the three details ADR-0006
fixes — the clause is `OSError` and not `PermissionError`; the message carries the operating
system's own reason; `README.md`'s paragraph is rewritten as one rule rather than extended with a
third case.

`tidy/planner.py` and `tidy/apply.py` are untouched, as the plan requires: `build_plan` keeps
raising, which is what makes the CLI's one handler sufficient, and `apply_plan` already lets
nothing raise out of it.

Commits on `main..wi/BUG-0001`:

- `5f2cd4f` — `tidy/cli.py` and `tests/test_cli.py` (plan steps 1 and 4)
- `068cecd` — `README.md` (plan step 3)

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| **AC1** — either mode against an unreadable folder writes a message naming it to stderr, nothing to stdout, no traceback, and exits with a documented status | `tidy/cli.py`: `except OSError` writes one stderr line naming `folder` and returns 2 before anything reaches stdout | Test `tests/test_cli.py::BadTargetTests::test_an_unreadable_folder_exits_2_without_a_traceback`, which asserts all four observables for `[folder]` and for `[folder, "--apply"]`. Also by hand on the branch head: `mkdir -p /tmp/bug1-check/unreadable && echo x > /tmp/bug1-check/unreadable/photo.jpg && chmod 000 /tmp/bug1-check/unreadable && python3 -m tidy /tmp/bug1-check/unreadable` → exit **2**, stdout **0 bytes**, stderr `tidy: /tmp/bug1-check/unreadable cannot be read: Permission denied`, `grep -c Traceback` **0** in both streams. Identical with `--apply`. Before the fix, the same command on this branch's base gave exit **1** and a `PermissionError` traceback |
| **AC2** — `README.md`'s exit-status paragraph states what this case exits with | `README.md` "What it does": *"2 when the folder you named cannot be used, which covers all of: it does not exist, it is not a folder, or it cannot be read"*, plus a sentence stating that such a folder gets one stderr line and nothing on stdout | Read `README.md:31-34` against the run quoted for AC1: the document says 2 and one line on stderr; the run gives 2 and one line on stderr. `git diff main -- README.md` is that one hunk |
| **AC3** — a regression test creates an unreadable folder, asserts AC1's observables, fails when the handling is removed, and skips itself where `chmod 000` does not deny the read | `tests/test_cli.py::BadTargetTests::test_an_unreadable_folder_exits_2_without_a_traceback` | Sensitivity shown by running it against four mutations of `tidy/cli.py`, each applied and reverted with `PYTHONDONTWRITEBYTECODE=1` — see `## Gates` below. All four fail it. The skip is decided by `os.listdir(unreadable)` inside a `try`: if the read succeeds the test calls `self.skipTest`, so it triggers as root and on a mode-ignoring filesystem alike, without consulting `os.geteuid` |

## Deviations from the plan

1. **The module docstring of `tests/test_cli.py` was updated** — `"WI-0001 AC1-AC15, and WI-0002
   AC1 and AC5-AC12."` became `"WI-0001 AC1-AC15, WI-0002 AC1 and AC5-AC12, and BUG-0001 AC1 and
   AC3."`. The plan's step 4 does not mention it. It is one line, it describes the contents of the
   file step 4 edits, and leaving it would have made the file state something false about itself
   as a direct result of this change. Declared here rather than left for review to notice.
2. **The plan predicted "64 tests pass — the 63 on `main` plus step 4's".** That is exactly what
   happened; recorded because the number was a checkable prediction and it held.
3. Nothing else. Steps 1, 3 and 4 were executed as written; step 2 is a prohibition and was
   honoured (see `## What I did not do`); step 5 is the gate run, below.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 64 tests ... OK`, run on the branch head after `068cecd` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0 errors, 0 warnings (run by `transition` at the closing move) |
| `every-criterion-has-a-test` | **pass** | AC1 and AC3: `test_an_unreadable_folder_exits_2_without_a_traceback`, plus the by-hand run quoted above. AC2 is a documentation criterion with no test — its evidence is the exact `README.md` sentence quoted against the exact run output, which is a reproducible comparison rather than "see the code" |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, *"all 2 commit(s) on main..wi/BUG-0001 name BUG-0001"* |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main -- tidy/ tests/ README.md` is three hunks: `tidy/cli.py` (step 1), `README.md` (step 3), `tests/test_cli.py` (step 4 plus deviation 1). No other file under `tidy/` or `tests/` changed |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, *"checked no documents changed since main"* — this item changed no file under `docs/` |

### The four mutations behind AC3

Each was applied to `tidy/cli.py`, the test run alone, then the file restored. All runs used
`PYTHONDONTWRITEBYTECODE=1`; the full suite was green again after each restore.

| mutation | result |
|----------|--------|
| The whole `try`/`except` removed, back to a bare `actions = build_plan(folder)` | **errors (2)** — the `PermissionError` escapes through the test helper's `run()`, once per subTest |
| `except OSError` branch returns 0 instead of 2 | **failures (2)** |
| The message drops the folder name, keeping the OS reason | **failures (2)** |
| `except OSError` narrowed to `except FileNotFoundError`, so `PermissionError` escapes again | **errors (2)** |

**One thing a later reader should know about how these were run.** The first attempt at the
`return 2 → return 0` mutation reported the test still passing, twice, and both readings were
artefacts rather than findings. The first was stale bytecode: the mutation and the restore produce
files of identical length, and the `__pycache__` entry was reused, so a run after the restore was
still executing the mutant — clearing the caches and setting `PYTHONDONTWRITEBYTECODE=1` fixed it.
The second was a mis-anchored edit: `str.replace(..., 1)` on the string `return 2` hits the
`isdir` branch, which is the *first* `return 2` in the file, not the one in the new handler. The
table above is from runs where the mutation was confirmed present in the file before the test ran.
A mutation that appears not to bite is worth distrusting before it is worth believing.

## What I did not do

- **I did not touch the `--help` strings.** `tidy/cli.py`'s `description` and `epilog` still say
  files are sorted "by file type" and point at "the extension-to-folder table" as though there
  were one. Both are wrong after WI-0002 and both are BUG-0003's subject. Plan step 2 forbids
  editing them here, and `git diff main -- tidy/cli.py` shows no change to either string.
- **I did not touch `tidy/planner.py` or `tidy/apply.py`.**
- **I did not handle a file that disappears or becomes unreadable partway through a scan.** The
  new handler will catch it, because `entry.stat()` is inside `build_plan`, and the user will get
  a message naming the *folder* and the OS's reason — honest, but it names the wrong thing: the
  folder was readable and one entry inside it was not. The plan puts this out of scope explicitly
  and adds no criterion for it. If per-entry resilience is wanted, it is a new item.
- **I did not give the unreadable case its own exit status.** ADR-0006 option B, rejected there;
  a script cannot distinguish "no such folder" from "cannot read it" by status alone, only by the
  stderr line.
- **I did not exercise AC3's skip path.** This environment runs as uid 1000 on a filesystem that
  enforces the mode (`id -u` → 1000; `os.listdir` at mode 000 raises), so the skip branch was
  never taken here. Its *trigger* was checked — the test's decision is the result of an actual
  read, not an euid test — but the branch itself is unexecuted in this run, and it would show up
  as a skip rather than as a pass wherever it does fire.
