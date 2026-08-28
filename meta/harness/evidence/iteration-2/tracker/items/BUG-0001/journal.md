# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-27T16:32:20Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** Filed by `verify` while verifying WI-0001 at `verifying`; this is the item's creation entry, not a dispatch.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC14 is the nearest criterion and does not extend to an unreadable folder, which is what makes this a bug rather than a send-back
  - `tracker/items/WI-0001/artifacts/impl-report.md` `## What I did not do` — predicted this as "a candidate bug item"
  - `tidy/planner.py`, `tidy/cli.py` on `wi/WI-0001` at `6b1873161b148392d8ee5cb6ff5824a4ab404289` — located the uncaught `os.scandir` call
  - `README.md` — the documented exit-status contract this behaviour contradicts (RB3)
  - `.claude/agile-skills/spec/dor-dod.md` §2 — the bug Definition of Ready applied below
- **Decisions:**
  - **Bug, not a send-back.** SKILL.md step 7's test is whether an acceptance criterion of WI-0001 says the behaviour should be different. None does: AC14 names "a target path that does not exist, or one that is a regular file rather than a folder", and an unreadable directory is neither. WI-0001 therefore passes with this defect present, and sending it back would be verifying against a criterion nobody wrote.
  - **`found-in: WI-0001`**, which per `spec/ids-and-statuses.md` §5 satisfies provenance on a bug on its own: WI-0001 is the item that delivered `build_plan`.
  - **The exit status is deliberately not fixed by the criteria.** AC1 requires a documented status, not a specific number. Choosing between 2 and a new code is a design decision, and pinning it here would be `verify` doing `plan`'s job.
  - **Priority `medium`**, matching BUG-0002: a real user-facing crash, but neither blocks the epic's success measures and both are reachable only off the happy path.
  - Definition of Ready for a bug (`spec/dor-dod.md` §2): RB1 **pass** — five numbered steps, runnable as written, with the root caveat stated; RB2 **pass** — the traceback and `echo $?` are the verbatim output of the run in `## Commands`, not a paraphrase; RB3 **pass** — cites `README.md`'s exit-status paragraph, and says explicitly why WI-0001 AC14 does *not* cover it; RB4 **pass** — `found-in: WI-0001`; RB5 **pass** — AC3 is the regression test, with its root-skip condition stated.
- **Questions raised:** none
- **Commands:**
  - `mkdir -p .harness/fperm && echo x > .harness/fperm/photo.jpg && chmod 000 .harness/fperm` → 0
  - `python3 -m tidy .harness/fperm` → **1**, `PermissionError: [Errno 13] Permission denied: '.harness/fperm'` traceback on stderr, stdout empty
  - `python3 -m tidy .harness/fperm --apply` → **1**, identical traceback
  - `scripts/new-item --id BUG-0001 --type bug --title "..." --epic EP-001 --priority medium --status ready --actor verify --found-in WI-0001 --reason "..."` → 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 37 tests … OK`, run on `6b18731`; recorded on WI-0001, where the suite lives)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace` → 0 errors, 0 warnings, after this entry and BUG-0002's were written)
  - `every-criterion-independently-checked` → **pass** (this bug's own three criteria are the fix's, not yet met; the criteria checked in this execution are WI-0001's, each with a command and its output in `WI-0001/artifacts/verify-report.md`)
  - `negative-cases-exercised` → **pass** (this item *is* a negative case that was exercised rather than read about — the traceback above is the run, not the report's account of it)
  - `tests-would-fail-without-the-change` (advisory) → **skipped** (no fix exists yet; AC3 is what will carry it)
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` — created and filled in
  - `tracker/items/BUG-0001/history.md` — creation row, actor `verify`
  - `tracker/items/BUG-0001/journal.md` — this entry
- **Status:** `—` → `ready`
- **Result:** A folder the process cannot read makes `tidy` die with an uncaught `PermissionError` traceback and exit 1, in both modes. No WI-0001 criterion covers it, so it is filed here at `ready` rather than sent back; WI-0001's own verification is unaffected.

## 2026-08-27T19:21:54Z — plan v0.3.1 — architect

- **Item:** BUG-0001
- **Trigger:** Status `ready`, dispatched by `next` as the highest-ranked runnable item — priority rank 3, and the earliest `created` (16:30:45Z) among BUG-0001, BUG-0002 and BUG-0003; WI-0003 is rank 4.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the summary, the five reproduction steps, the expected/actual sections, and AC1–AC3, which are this design's contract
  - `tracker/items/BUG-0001/history.md` — one row, `— → ready`, actor `verify`
  - `tracker/items/BUG-0001/journal.md` — `verify`'s creation entry, including why this is a bug rather than a WI-0001 send-back and why the exit status was deliberately left to `plan`
  - `tracker/items/BUG-0001/artifacts/refinement-qa.md` — **absent**; a bug filed with reproduction steps already satisfies the bug Definition of Ready and never passes through `refine` (`spec/dor-dod.md` §2)
  - `docs/architecture/overview.md` v3 — the three-layer shape and the module table
  - `docs/architecture/adr/`: **ADR-0001** (Python 3.9+, stdlib only, one terminal command), **ADR-0002** (planning is separated from applying — the constraint that decides where the fix goes), **ADR-0003** (`os.link`, and the fallback BUG-0002 is about), **ADR-0004** (the test and lint commands), **ADR-0005** (the band table, for what WI-0002 left in `planner.py`)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` already resolved by ADR-0004; nothing to fill in
  - `tidy/cli.py` — the `os.path.isdir` guard, the `return 2`, the unguarded `build_plan(folder)` call, and the message shape the new line must match
  - `tidy/planner.py` — `os.scandir(folder)`, the call that raises, and everything else `build_plan` does, which is what makes the breadth of the `except` clause decidable
  - `tidy/apply.py` — confirmed `apply_plan` lets nothing raise out of it, so the CLI needs one handler and not two
  - `README.md` — the exit-status paragraph the current behaviour contradicts
  - `tests/support.py` and `tests/cli_support.py` — the `FolderTestCase` cleanup order and the `run()` helper the regression test uses
  - `tests/test_cli.py` `BadTargetTests` — the existing missing-path/not-a-folder test, which is both the pattern for the new one and the test this change could most easily break
- **Decisions:**
  - **Exit 2, not a new status code** — *asked of no one; decided from the documents plus a recorded assumption.* `README.md` already assigns 2 to a target that cannot be used, BUG-0001 AC1 asks only for "a status the tool documents", and no document expresses an intent about exit codes beyond that contract. The alternative — a third code — is named and costed in ADR-0006 option B. Recorded as ADR-0006 and as `## Assumptions` 1 with its three-line reversal.
  - **Caught at the CLI boundary, in `tidy/cli.py`** — *from the documents.* ADR-0002 fixes the layering: the planner decides and writes nothing, the CLI turns results into text and exit codes. A planner that caught the error would have to invent a return value meaning "the run failed" while `cli.py` still chose the status, so the decision would not have moved. ADR-0006 options C and D.
  - **Not an `os.access` pre-check** — *from the documents and from the failure mode.* Time-of-check to time-of-use: the folder can stop being readable between the check and the scan, which puts the traceback back on exactly the path the check was added to remove. ADR-0006 option E.
  - **The `except` clause is `OSError`, not `PermissionError`** — *assumption 3, with its cost stated.* An unreadable folder is the reproduced case but not the only way listing fails, and narrowing the clause would leave the others as tracebacks while claiming the class was handled. It rests on `build_plan` doing filesystem reads and string composition and nothing else, which is checkable. ADR-0006 `## Decision` §1 records what reversing it costs: one word, and the other failure modes go back to tracebacks.
  - **`README.md`'s paragraph is rewritten as one rule rather than extended with a third case** — ADR-0006 `## Decision` §3, satisfying AC2.
  - **The regression test skips by attempting the read, not by testing `os.geteuid() == 0`.** The euid is a guess at why the permission might not bite; the read is the fact. It also covers a filesystem that ignores the mode, and `os.geteuid` does not exist on every platform an stdlib-only tool could run on [src: ADR-0001]. Recorded in step 4 rather than as an ADR: it is a test-construction choice with no consequence outside the test.
  - **`tidy/planner.py` and `tidy/apply.py` are not touched, and `cli.py`'s `--help` strings are not either.** The second is a prohibition with a step of its own: those strings are BUG-0003's subject, and two items editing the same text makes both unverifiable against their own criteria.
  - **No ADR for the message's wording** — it is a format string constrained by three observables (begins `tidy: `, names the folder, carries the OS reason). An ADR trail padded with non-decisions hides the real ones.
  - **`docs/architecture/overview.md` was deliberately not bumped.** The change adds an error path inside a responsibility the module table already states for `cli.py` ("argparse setup, rendering an action list as lines, exit codes"); the three-layer shape and both architectural commitments are untouched. A version bump with no substantive change devalues every other one.
  - **Nothing was escalated to the human.** The only choice with product stake — which exit status — is invisible to a user who reads the message, documented either way, and reversible in three lines.
- **Questions raised:** none
- **Commands:**
  - `mkdir -p /tmp/bug1repro/unreadable && echo x > /tmp/bug1repro/unreadable/photo.jpg && chmod 000 /tmp/bug1repro/unreadable` → 0
  - `python3 -m tidy /tmp/bug1repro/unreadable` → **1**, `PermissionError: [Errno 13] Permission denied` traceback through `tidy/cli.py:59` and `tidy/planner.py:41`, stdout empty — the defect reproduced on `main` after WI-0002 merged, not taken from the bug report
  - `python3 -m tidy /tmp/bug1repro/unreadable --apply` → **1**, identical traceback
  - `id -u` → `1000`, so the reproduction was not masked by running as root
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 first (three unsourced absolutes in the new ADR), then exit 0 after the citations were added
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 7 item(s), 8 document(s)`, 0 errors 0 warnings
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 63 tests … OK` (the baseline step 5's count is measured against)
  - `python3 -m compileall -q tidy tests` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 7 items and 8 documents)
  - `every-criterion-is-addressed` → **pass** (`plan.md` `## Acceptance criteria mapping`: AC1 → step 1, AC2 → step 3, AC3 → step 4, each with a named demonstration — the test and the by-hand command for AC1, the document comparison for AC2, the revert-and-rerun sensitivity check for AC3. Three of three; no step exists that no criterion maps to, step 2 being a prohibition and step 5 the gate run)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` names `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q tidy tests` under ADR-0004; both were run in this execution, exit 0 each — not assumed to work)
  - `decisions-recorded` → **pass** (five choices point at ADR-0006 — the status, the location, the breadth of the `except`, the message content, the README rewrite — and four more at `## Assumptions` 1–4, each with what reversing it costs. The two remaining choices, the test's skip condition and the absence of an ADR for the message wording, are recorded in the step and in the decisions table)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0, after three absolutes in ADR-0006 were given citations the linter had refused)
  - `plan-is-executable-without-you` (advisory) → **pass** (read back cold: step 1 names the file, the call to wrap, the clause, the three observables and the return value; step 3 names the sentence to replace and what it must say; step 4 names the class, the fixture, the cleanup ordering and why, the four assertions and the skip rule. The one thing left open is the message's exact wording, which `## Assumptions` 2 declares as the developer's within three constraints)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` — created: problem, approach, the fixed interface, five steps, the AC mapping, four assumptions, the decisions table, `## Scaffolding: none`, four risks, five exclusions
  - `docs/architecture/adr/ADR-0006-report-an-unusable-target-at-the-cli-boundary.md` — created at v1: two questions, five options across them, the decision with three fixed details, and reversibility for both halves
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** BUG-0001 is designed as one `try`/`except OSError` around `build_plan` in `tidy/cli.py`, returning 2 after one line on stderr, plus one rewritten sentence in `README.md` and one regression test that skips itself where `chmod 000` does not bite. ADR-0006 records why 2 rather than a new code and why the boundary rather than the planner. `tidy/planner.py` and `tidy/apply.py` are untouched, and `cli.py`'s `--help` strings are explicitly off limits because they belong to BUG-0003.

## 2026-08-27T19:24:09Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `planned` — `next` dispatched `implement` as the status owner; BUG-0001 was the
  highest-ranked runnable item (medium/rank 3, created 2026-08-27T16:30:45Z, earliest of the three
  medium bugs).
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — AC1 (message on stderr, empty stdout, no traceback, documented
    status), AC2 (`README.md` states it), AC3 (regression test that skips where `chmod 000` does not bite)
  - `tracker/items/BUG-0001/artifacts/plan.md` — five steps; step 2 is a prohibition, not an edit
  - `tracker/items/BUG-0001/history.md` — two rows, `verify` created it at `ready`, `plan` moved it to
    `planned`; no send-back, so this is a fresh start and not a resumption
  - `tracker/items/BUG-0001/questions/` — empty; no question has ever been filed on this item
  - `docs/architecture/adr/ADR-0006-report-an-unusable-target-at-the-cli-boundary-with-exit-status-2.md`
    — options A/C chosen, and the three details it fixes (`OSError` not `PermissionError`; the OS's own
    reason in the message; `README.md` rewritten as one rule)
  - `docs/architecture/adr/ADR-0002` as cited by the plan for the layering it must not breach
  - `tracker/project.yaml` — trunk `main`, branch prefix `wi/`, test and lint commands both non-null
  - `tidy/cli.py`, `tidy/planner.py`, `tests/test_cli.py` (`BadTargetTests`), `tests/cli_support.py`,
    `tests/support.py`, `README.md` — the four files the plan's steps name, plus the two test helpers
    step 4 builds on
- **Decisions:**
  - Reproduce the defect on this branch's head before changing anything, rather than trusting
    BUG-0001's `## Actual behaviour` block. The bug report was written against `wi/WI-0001` at commit
    `6b18731`; WI-0002 has merged since and moved the raising line from `planner.py:35` to
    `planner.py:41`, so the report's traceback is no longer literally accurate and only running it
    could establish that the defect itself survived the merge. It did.
  - No other decision has been taken yet: no source file has been edited.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → 0 (branch created from trunk at `e96c5e2`)
  - `id -u` → 0, printed `1000` — not root, so `chmod 000` will deny the read in this environment and
    AC3's skip path will not be the one exercised here
  - `mkdir -p /tmp/bug1-impl/unreadable && echo x > /tmp/bug1-impl/unreadable/photo.jpg && chmod 000 /tmp/bug1-impl/unreadable`
    → 0
  - `python3 -m tidy /tmp/bug1-impl/unreadable` → **1**, stdout empty, stderr a `PermissionError`
    traceback ending `[Errno 13] Permission denied: '/tmp/bug1-impl/unreadable'`. The defect is live on
    the branch head.
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no code has been changed, so a run now would report on the
    trunk rather than on this execution's work — the plan's step 5 runs it on the final state)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **skipped** (this entry and its history row are what the validator would check;
    it is run at the closing entry, on the finished workspace)
  - `every-criterion-has-a-test` → **skipped** (no test written yet)
  - `commits-reference-the-item` → **skipped** (no commit on the branch yet)
  - `claims-are-sourced` → **skipped** (nothing changed since `main` yet)
  - `no-unplanned-scope` (advisory) → **skipped** (empty diff)
- **Artifacts:**
  - branch `wi/BUG-0001`, created from `main` at `e96c5e2`; no commit on it yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation started. The plan was read, the ADR's three fixed details noted, and the
  defect reproduced on this branch's head — exit 1 with a traceback, which is what the four steps ahead
  have to replace with one stderr line and exit 2.

## 2026-08-27T19:27:47Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress` — the same `implement` execution that opened the branch at
  19:24:09Z, continuing without interruption.
- **Inputs read:**
  - the six inputs listed in this item's opening entry, unchanged since
  - `tidy/cli.py` `main()` — the `isdir` branch, for the message shape the plan says to follow
  - `tidy/planner.py` `build_plan()` — to confirm the plan's premise that it does filesystem reads
    and string composition only, which is what makes an `OSError` clause honest rather than broad
  - `tests/test_cli.py` `BadTargetTests` and its module docstring, `tests/cli_support.py` `run()`,
    `tests/support.py` `FolderTestCase.setUp`/`make_folder`/`write`
  - `README.md` lines 26-34 — the exit-status paragraph AC2 is about
- **Decisions:**
  - **The stderr line is `tidy: <folder> cannot be read: <os reason>`.** Plan assumption 2 leaves
    the wording to the developer provided it begins `tidy: `, names the folder and carries the OS's
    reason; this shape parallels the existing `tidy: %s is not a folder` line. `error.strerror or
    error` is the reason, because `strerror` is `None` for some `OSError`s and an empty reason after
    a colon would be worse than the repr.
  - **The regression test asserts `assertNotIn("Traceback", ...)` on both streams**, not only on
    stderr. AC1 says no traceback is printed; a traceback on stdout would also violate
    `stdout == ""`, so the stdout assertion is redundant with the one above it — kept anyway,
    because it states the criterion rather than a consequence of it.
  - **The module docstring of `tests/test_cli.py` was updated to name BUG-0001.** Not in the plan.
    Taken as part of step 4 rather than as unplanned scope: it is one line describing what the file
    covers, and step 4 changed that. Declared as deviation 1 in `impl-report.md`.
  - **Mutation testing was redone after two false negatives**, rather than reported as it first
    came out. See `## Commands` and the note in `impl-report.md`.
  - **Nothing was escalated.** The plan makes every decision this change needed; the only latitude
    it left — the message's wording — is plan assumption 2's, explicitly the developer's.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → 0
  - `python3 -m tidy /tmp/bug1-impl/unreadable` (before any edit) → **1**, `PermissionError`
    traceback on stderr, stdout empty — the defect, live on this branch's base
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 64 tests ... OK` (branch head, after
    `068cecd`)
  - `python3 -m compileall -q tidy tests` → 0
  - `python3 -m tidy /tmp/bug1-check/unreadable` → **2**, stdout 0 bytes, stderr
    `tidy: /tmp/bug1-check/unreadable cannot be read: Permission denied`, `grep -c Traceback` 0 on
    both streams. Same with `--apply` → **2**, identical output
  - four mutation runs of `tidy/cli.py` against
    `tests.test_cli.BadTargetTests.test_an_unreadable_folder_exits_2_without_a_traceback`, each
    applied and reverted: handling removed → errors(2); `return 2`→`return 0` → failures(2);
    folder name dropped from the message → failures(2); `OSError`→`FileNotFoundError` →
    errors(2). Full suite green after each revert
  - `find . -name __pycache__ -not -path './.git/*' -exec rm -rf {} +` → 0. Run because the first
    `return 2`→`return 0` attempt reported the test still passing: identical file lengths meant the
    stale `.pyc` was reused and the "restored" run was still executing the mutant. Subsequent
    mutation runs used `PYTHONDONTWRITEBYTECODE=1`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → 0, "all 2
    commit(s) on main..wi/BUG-0001 name BUG-0001"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0, 0 errors,
    0 warnings, "checked no documents changed since main"
  - `git commit` ×2 → 0 each: `5f2cd4f`, `068cecd`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 64 tests, on
    the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (AC1 and AC3:
    `tests/test_cli.py::BadTargetTests::test_an_unreadable_folder_exits_2_without_a_traceback`,
    sensitivity shown by four mutations; AC2 is a documentation criterion, evidenced by the
    `README.md` sentence quoted against the exit status and stderr line of an actual run)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, both commits)
  - `no-unplanned-scope` (advisory) → **pass** (`git diff main -- tidy/ tests/ README.md` is three
    hunks, each traceable to plan step 1, 3 or 4; the `--help` strings step 2 protects are
    unchanged)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0; no file under
    `docs/` changed)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/impl-report.md` (new)
  - branch `wi/BUG-0001`, commits `5f2cd4f` and `068cecd` (range `main..wi/BUG-0001`)
  - `tidy/cli.py`, `tests/test_cli.py`, `README.md` (modified, on the branch)
- **Status:** `in-progress` → `verifying`
- **Result:** An unreadable target folder now produces one stderr line naming it and the operating
  system's reason, nothing on stdout, no traceback, and exit 2 — in both modes, checked by hand and
  by a regression test that four separate mutations of the fix all break. `README.md` states the
  same rule. The `--help` strings BUG-0003 owns were deliberately left wrong, and the case of a
  single entry becoming unreadable mid-scan is handled only in the sense that it no longer crashes;
  both are named in `impl-report.md` `## What I did not do`.

## 2026-08-27T19:35:42Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying` — `next` dispatched `verify` as the status owner; BUG-0001 was
  again the highest-ranked runnable item on the selection key.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — AC1-AC3, read **before** `impl-report.md`, so that what
    would settle each criterion was derived from the criterion rather than from what was built
  - `tracker/items/BUG-0001/artifacts/plan.md` — the five steps, and `## Out of scope for this
    item`, which turned out to be where BUG-0004 was already named
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — read last, and checked rather than trusted
  - `tracker/items/BUG-0001/history.md` — two `implement` rows this turn, no send-back
  - no `refinement-qa.md` exists on this item; no criterion's wording was contested
  - `docs/architecture/adr/ADR-0006` — `## Decision` §1-3 and `## Consequences`
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - the code on `wi/BUG-0001` at **`d80c35a562faad3155b195234e3ff5b3061c834e`**: `tidy/cli.py`,
    `tidy/planner.py`, `tests/test_cli.py`, `README.md`
- **Decisions:**
  - **Every fixture was built here rather than through `tests/support.py`.** The item's own
    regression test uses that helper, so reusing it would have made my AC1 evidence share a
    failure mode with the thing it is checking. `mkdir`, `chmod`, `ln -s` and a scratch tree
    instead.
  - **AC1's fourth requirement — "a status the tool documents" — was resolved through AC2**, by
    exercising every case `README.md`'s paragraph makes a claim about (0/0/2/2/2), not only the new
    one. A contract half-checked is a contract not checked.
  - **The dangling-symlink defect is a bug against WI-0002, not a send-back on BUG-0001.** The
    procedure's test: does an acceptance criterion of *this* item say the behaviour should be
    different? AC1 governs a folder that cannot be read, and this folder can be. Provenance was
    established by running the fixture in three trees rather than by reading the diff —
    `2a4b928~1` exits 0 and previews both files, `main` gives a traceback and exit 1,
    `wi/BUG-0001` gives the false message and exit 2 — and `git log -S "entry.stat()"` returns
    exactly one commit, WI-0002's. Filed as **BUG-0004**.
  - **BUG-0001 is not sent back even though it made that defect quieter.** Before it, a traceback;
    after it, a calm false sentence. That is a real cost and it is written into BUG-0004's
    `## Notes` so a later reader does not read it as grounds to unpick this item — but no criterion
    of this item covers it, the plan scoped it out in advance, and reversing a correct fix to
    restore a traceback would be worse.
  - **The skip clause of AC3 was exercised by producing its condition, not by reasoning about it.**
    I cannot become root, so I made the read succeed by changing the test's own `chmod` and
    confirmed it reports `skipped` with its stated reason rather than failing. What that does not
    establish is recorded in `## Not verified, and why`.
  - **No criterion was judged ambiguous**, so nothing was escalated to the architect.
- **Questions raised:** none
- **Commands:**
  - `find . -name __pycache__ -exec rm -rf {} +` → 0, run first because identical-length mutations
    are masked by a stale `.pyc`; I hit that trap independently before reading that
    `impl-report.md` documents it
  - `python3 -m unittest discover -s tests -t . -q` → **0**, `Ran 64 tests`, `OK`, no skips
  - `python3 -m compileall -q tidy tests` → **0**
  - AC1: four runs over two self-built mode-000 fixtures (one with files, one empty), preview and
    `--apply` → all **exit 2**, stdout **0 bytes**, stderr `tidy: <path> cannot be read: Permission
    denied`, `Traceback` in neither stream
  - AC2: `sed -n '31,35p' README.md`, then the five cases the paragraph names → **0 / 0 / 2 / 2 /
    2**; `python3 -m tidy --help | grep -i exit` → argparse's own `show this help message and exit`
    and nothing else
  - AC3: `grep -rn chmod tests/` → exactly one test; `python3 -m unittest -v <that test>` → `OK`
    (it runs here, `id -u` → 1000); five mutations of `tidy/cli.py` → errors(2), failures(2),
    failures(2), failures(2), errors(2); one mutation of the test's own `chmod` → `OK (skipped=1)`
    with the stated reason. Full suite green after every `git checkout --` restore
  - boundary battery, eleven conditions → tabulated in `verify-report.md`; mode 400, mode 100, a
    symlink to an unreadable folder, a dangling symlink *as* the target, a relative path, and an
    unreadable **sub**folder (exit 0, no regression)
  - `git log --oneline -S "entry.stat()" -- tidy/planner.py` → 0, one commit `2a4b928` (WI-0002)
  - `git worktree add --detach .harness/wt-main main`, `... .harness/wt-pre2 2a4b928~1`, the
    fixture run in each, then `git worktree remove --force` ×2 → all 0; `.harness/` is gitignored
    and nothing was left behind
  - `new-item --id BUG-0004 --type bug --status ready --actor verify --found-in WI-0002` → 0
  - `journal-entry BUG-0004 --skill verify` → 0 (first attempt exit 1: the standalone tool requires
    a `**Status:**` bullet, which `transition` would have written itself)
  - `board-gen` → 0; `validate-workspace` → **0 errors, 0 warnings**, 8 items
- **Gates:**
  - `tests-pass` → **pass** (exit 0, 64 tests, on `d80c35a` with caches cleared)
  - `lint-clean` → **pass** (exit 0)
  - `workspace-valid` → **pass** (0 errors, 0 warnings, 8 items, after BUG-0004 was completed)
  - `every-criterion-independently-checked` → **pass** (AC1-AC3 each decided by a command run in
    this execution with its output quoted; `impl-report.md` is cited as evidence nowhere)
  - `negative-cases-exercised` → **pass** (eleven conditions produced and run; AC1 is itself
    entirely a negative case and was produced with `chmod` and `ln -s`)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (five mutations, each confirmed
    present in the file before its run, each breaking the test; three of them aimed at one
    observable each)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` (new), with `Verified-commit: d80c35a`
  - `tracker/items/BUG-0001/item.md` — AC1, AC2 and AC3 ticked, each against a command above
  - `tracker/items/BUG-0004/` — new bug at `ready`, `found-in: WI-0002`, body and journal entry
  - `tracker/board.md` (regenerated)
- **Status:** `verifying` → `in-review`
- **Result:** BUG-0001 passes. An unreadable target folder now gives one stderr line naming it and
  the operating system's reason, an empty stdout, no traceback and exit 2 — in both modes, across
  six shapes of unreadable — and `README.md` states the same rule for every case it covers. The
  regression test is sensitive to each of AC1's observables separately and skips honestly where the
  mode does not bite. One defect was found that this item does not own and does not fix: a single
  dangling symlink still aborts the whole scan, filed as BUG-0004 against WI-0002.

## 2026-08-27T19:40:52Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0001
- **Trigger:** status `in-review` — `next` dispatched `review-close` as the status owner; BUG-0001
  was the earliest-created of five medium-priority runnable items.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md`, `history.md` (five rows), `journal.md` (five entries, read
    end to end), `plan.md`, `impl-report.md`, `verify-report.md`, `questions/` (empty)
  - **the diff `main..wi/BUG-0001`**, hunk by hunk, not the reports about it
  - `docs/architecture/overview.md`; `docs/architecture/adr/ADR-0002` `## Decision`;
    `docs/architecture/adr/ADR-0006` `## Decision` and `## Change log`
  - the code the docs claims cite, opened for the D12 audit: `tidy/cli.py` in full,
    `tidy/apply.py` in full, `tidy/planner.py`'s `build_plan`
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `trunk-branch`
- **Decisions:**
  - **Accept.** All twelve Definition of Done criteria pass, each recorded with its own evidence in
    `review.md` `## Definition of Done`. Not one overall verdict.
  - **One finding, not sent back.** The comment above the new handler opens "Listing the target is
    the last thing that can make it unusable", which describes a narrower `try` than the one that
    is there: `entry.stat()` also runs inside `build_plan`, and when it fails the handler blames
    the target folder. That is BUG-0004's misconception in comment form. Sending the item back to
    reword a comment whose substance is already an item would cost two executions and buy nothing,
    and BUG-0004's fix has to rewrite it anyway. Recorded as gap 5 in `item.md`.
  - **Seven gaps accepted and written into `item.md` `## Gaps accepted at review`**, not left in
    the reports: AC3's skip branch never run as root; the `OSError` clause exercised for `EACCES`
    and `ENOENT` only; the TOCTOU race unexercised; BUG-0004; the comment's framing; `--help` still
    wrong (BUG-0003); and no distinct exit status for this case (ADR-0006 option B). A gap that
    lives only in a verification report stops being read the moment an item closes.
  - **D7 passes with nothing to bump.** The only document the change invalidated is `README.md`,
    which was updated and has no doc header, so no version or change-log row applies. Nothing under
    `docs/` was invalidated — decided by the D12 audit, not assumed — so no bump was due, and
    ADR-0006 stays at version 1 because every claim it makes about the code came true.
  - **D10 checked twice.** `check-verify-freshness` passed; I also ran
    `git diff --name-only d80c35a..09733b1` and confirmed that filtering out `tracker/` and `docs/`
    leaves it empty, rather than taking the script's summary on trust.
  - **`verify`'s classification of BUG-0004 upheld.** I re-read BUG-0001's AC1-AC3 against it: none
    governs a folder that *can* be read, so it is not this item's failure. `found-in: WI-0002` also
    holds — `git log -S "entry.stat()"` returns one commit and it is WI-0002's.
  - **The epic is not at rest**, so no sign-off question was filed. `engagement-state` says so; I
    did not decide it from the board.
- **Questions raised:** none
- **Commands:**
  - `check-verify-freshness BUG-0001 wi/BUG-0001` → **0**: verified at `d80c35a`, branch at
    `09733b1`, "only the record changed (10 file(s) under tracker/ or docs/)"
  - `git diff --name-only d80c35a..09733b1 | grep -v '^tracker/' | grep -v '^docs/'` → **empty**
  - `check-commit-refs BUG-0001 wi/BUG-0001` → **0**, "all 4 commit(s) on main..wi/BUG-0001 name
    BUG-0001"
  - `lint-claims --changed-since main` → **0**, "checked no documents changed since main"
  - `grep -c "^- \[x\] AC"` → **3**; `grep -c "^- \[ \] AC"` → **0**
  - `git rev-parse main` **before** the trial → `e96c5e263d5779e22d566f950aa79a980ae9e046`
  - `git worktree add --detach .harness/trial main` → 0; `git -C .harness/trial merge --no-ff
    wi/BUG-0001` → 0, merge head **`25fab17`**
  - **on the merge result**: `python3 -m unittest discover -s tests -t . -q` → **0**, `Ran 64
    tests`, `OK`; `python3 -m compileall -q tidy tests` → **0**; and the fix itself against a
    mode-000 folder → exit **2** with `tidy: <path> cannot be read: Permission denied`, in preview
    and in `--apply`
  - `git worktree remove --force .harness/trial` → 0; `git rev-parse main` **after** →
    `e96c5e26...`, **unchanged**; `git worktree list` shows only the main checkout
  - `python3 -c "import shutil; print(shutil.Error.__mro__)"` → `shutil.Error` subclasses
    `OSError`, which is what ADR-0006's claim about `apply_plan` rests on
  - `engagement-state EP-001` → **active**, "still in flight: BUG-0001, BUG-0002, BUG-0003,
    BUG-0004, WI-0003"
- **Gates:**
  - `definition-of-done` → **pass** (D1-D12 each with its own result and evidence in `review.md`
    `## Definition of Done`, including the seven-claim D12 audit table naming what was opened for
    each)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0, plus the
    independent `git diff --name-only` check)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 4 commits)
  - `tests-pass-on-the-merge-result` → **pass** (64 tests `OK` and `compileall` exit 0 run **inside**
    the detached trial worktree at `25fab17`, not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition)
  - `record-is-reconstructible` → **pass** (all four questions answered from the tracker, docs and
    `git log --grep BUG-0001` in `review.md` `## Record is reconstructible`)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0; no `docs/` file
    changed, so the automated half had nothing to inspect and D12's read is the whole of it)
  - `epic-sign-off` → **pass** (`check-epic-signoff BUG-0001` exit 0, run by this transition.
    Corrected after the fact: this bullet first said `skipped`, on the reasoning that
    `engagement-state EP-001` reports **active** with five children in flight so there is nothing
    to sign off. That reasoning is sound but the verdict was wrong — the gate is not conditional on
    the epic being at rest, it ran, and it passed. Recording `skipped` for a gate that executed
    would misdescribe this execution, so the bullet is corrected here rather than left to stand)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/review.md` (new)
  - `tracker/items/BUG-0001/item.md` — `## Gaps accepted at review` added, then `status: done` and
    `outcome: delivered`
  - the merge commit into `main` (recorded in `review.md` after it is made)
  - no bug filed by this execution; BUG-0004 was `verify`'s
- **Status:** `in-review` → `done`
- **Result:** Accepted and closed. An unreadable target folder now gives one stderr line naming it
  and the operating system's reason, an empty stdout, no traceback and exit 2 in both modes, and
  `README.md` states the same rule for every case it covers — confirmed on the merge result rather
  than only on the branch. One finding was accepted rather than sent back, and seven gaps were
  written onto the item so they outlive its reports. The engagement stays open: four children are
  still in flight.
