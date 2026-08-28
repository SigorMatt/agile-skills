# Journal — BUG-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-27T19:33:17Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0004
- **Trigger:** created by `verify` while verifying BUG-0001 at `verifying`. `new-item` writes the
  creation row into `history.md` but no journal entry, so this entry is the one that row requires.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` AC1-AC3 and `artifacts/plan.md` `## Out of scope for this
    item` — to decide whether this belongs to BUG-0001 or elsewhere
  - `docs/architecture/adr/ADR-0006` `## Consequences` — which names the broad `except OSError` as
    the cost that produces the misleading message
  - `tidy/planner.py` `build_plan` and `tidy/cli.py` `main` on `wi/BUG-0001` at `d80c35a`
  - `README.md` — the `leave` line format cited in `## Expected behaviour`
  - `git log -S "entry.stat()" -- tidy/planner.py` → the single commit `2a4b928` (WI-0002)
- **Decisions:**
  - **Filed as a bug against WI-0002, not as a send-back on BUG-0001.** The test in the `verify`
    procedure is whether an acceptance criterion of the item under verification says the behaviour
    should be different. BUG-0001's AC1 governs "a folder the process cannot read"; this folder can
    be read. AC2 and AC3 are about `README.md` and the regression test. None of them is
    contradicted, so BUG-0001 is not sent back.
  - **`found-in: WI-0002`, established by running rather than by reading the diff.** The fixture
    was run against `2a4b928~1` (previews both files, exit 0), against `main` (traceback, exit 1)
    and against `wi/BUG-0001` (false message, exit 2), in three separate worktrees. WI-0002's
    `entry.stat()` is where the abort begins.
  - **One bug, not two.** The abort and the misleading wording have one root cause — an `OSError`
    from a single entry propagating out of `build_plan` — and splitting them would give two items
    that cannot be verified independently.
  - **AC1 deliberately does not say what should happen to the dangling symlink itself**, only that
    it must not cost the user the other files. Deciding the per-entry answer is `plan`'s, and
    pinning it here would be `verify` designing the fix.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline -S "entry.stat()" -- tidy/planner.py` → 0, one commit: `2a4b928` (WI-0002)
  - `git worktree add --detach .harness/wt-main main` and `... .harness/wt-pre2 2a4b928~1` → 0
  - the fixture run in each worktree → `2a4b928~1`: exit **0**, both files previewed; `main`:
    exit **1**, `FileNotFoundError` traceback out of `planner.py:55`; `wi/BUG-0001` at `d80c35a`:
    exit **2**, `tidy: <folder> cannot be read: No such file or directory`, stdout empty
  - `git worktree remove --force` ×2 → 0 (no worktree left behind)
  - the item's own `## Steps to reproduce`, run verbatim against `/tmp/dangling` → preview and
    `--apply` both exit **2** with that line; `grep -c photo.jpg` over the output → **0**; the
    folder's contents unchanged afterwards
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 64 tests, run
    on `d80c35a` during the BUG-0001 verification this item was filed from)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` exit 0, same run)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0 after this entry and the board
    regeneration; it reported `journal.execution.missing` for this item until this entry existed,
    which is the gate working)
  - `every-criterion-independently-checked` → **skipped** (this is a creation, not a verification
    of BUG-0004; its four criteria are unticked and are for a later `verify` execution to decide)
  - `negative-cases-exercised` → **pass** (the defect *is* a negative case, built here and
    triggered in three trees; see `## Commands`)
  - `tests-would-fail-without-the-change` (advisory) → **skipped** (no change has been made for
    this item; there is nothing yet to be sensitive to)
- **Artifacts:**
  - `tracker/items/BUG-0004/item.md` — summary, verbatim reproduction steps, expected and actual
    behaviour quoted from real runs in three trees, and AC1-AC4
  - `tracker/board.md` (regenerated)
- **Status:** `—` → `ready`
- **Result:** BUG-0004 filed at `ready` against WI-0002: one dangling symlink aborts the whole
  scan, so no file in the folder is tidied and the user is told the folder cannot be read when it
  can. Found from a boundary case built for BUG-0001's verification; BUG-0001 neither causes it nor
  claims to fix it, and is not sent back.

## 2026-08-27T20:48:26Z — plan v0.3.1 — architect

- **Item:** BUG-0004
- **Trigger:** Status `ready`, dispatched by `next` as the best-ranked runnable item (priority `medium`, rank 3, ahead of BUG-0005 and WI-0003 on priority; BUG-0003 closed earlier in this turn).
- **Inputs read:**
  - `tracker/items/BUG-0004/item.md` — the four criteria, the reproduction steps, and the three symptom forms recorded against `2a4b928~1`, `main` and `wi/BUG-0001`
  - `tracker/items/BUG-0004/journal.md` — `verify`'s creation entry: why this is a bug against WI-0002 rather than a send-back of BUG-0001, and that the per-entry answer was deliberately left to `plan`
  - `tracker/items/BUG-0004/history.md` — the single creation row; no send-back, so this is a first plan
  - `tracker/items/BUG-0004/questions/` — empty
  - ADR-0006 in full — the target-level boundary, and in particular its rejected option D and its details 1 and 2, which this decision has to stay clear of and reuses one level down
  - ADR-0002 (destinations decided in `planner.py` alone), ADR-0007 (the exit status turns on a `"failed"` outcome), ADR-0005 (the band table), ADR-0003 (the move route), ADR-0004 (the commands), ADR-0001 (stdlib only), ADR-0008 (the help text, untouched here)
  - `docs/architecture/overview.md` v6 — the three-layer shape, the module table, and `## What is deliberately not here`
  - `docs/product/vision.md` — the preview promise, which is what makes silently skipping an entry unacceptable
  - `tidy/planner.py` in full — `build_plan`'s loop, `_blocking_component`, `_no_rule_reason`, `_free_destination`, `_is_taken`; `tidy/cli.py` `main` lines 57-93; `tidy/apply.py` `apply_plan`; `tidy/rules.py`
  - `tests/test_cli.py` — `BadTargetTests` (the skip-by-attempted-operation shape and BUG-0001's assertions) and the class layout; `tests/test_planner.py` `ScanTests`; `tests/support.py` `FolderTestCase`; `tests/cli_support.py` `run()`, which is in-process
  - `README.md` — `## What it does` and the exit-status paragraph, which AC3 turns on
  - `tracker/project.yaml` — trunk `main`, the test and lint commands
- **Decisions:**
  - **An `OSError` from one entry becomes a `leave` action inside `build_plan`, and the scan continues** — ADR-0009, the only decision this item forces. **[documented]**, against ADR-0002 and the `leave` mechanism the planner already has for "this entry cannot be placed". Options B (skip silently), C (age symlinks by the link, `follow_symlinks=False`) and D (keep aborting, improve the message) are costed in the ADR; B breaks the preview promise, C changes behaviour WI-0002's review accepted and does not fix the class, D leaves AC1 exactly as it is.
  - **The guard covers `entry.is_dir()` and `entry.stat()`, and `os.scandir` stays outside it** — **[documented, by measurement]**. A symlink loop raises `ELOOP` from `is_dir()`, one call before the item's own fixture reaches `stat()`, and reaches the user identically today; a guard around `stat()` alone would leave it aborting while every criterion passed. Leaving `os.scandir` outside is what keeps ADR-0006's target-level boundary and BUG-0001's regression test intact.
  - **The clause is `except OSError`, not `except FileNotFoundError`** — **[documented]**, the same reasoning ADR-0006 detail 1 gives at the target level: `ENOENT`, `ELOOP`, `EACCES` and `EIO` are one event from the entry's point of view, and narrowing to the reproduced errno would claim the class was handled while most of it still aborted.
  - **The reason carries the operating system's own words and names no cause** — **[documented]**, ADR-0006 detail 2 one level down. `ENOENT` on an entry `scandir` just listed is usually a broken symlink and sometimes a file deleted mid-scan; the planner cannot tell which, so it says what failed rather than why it thinks it failed.
  - **The exit status stays 0, and `README.md` is amended to say which case that is** — **[documented]**, from ADR-0007 (only a `"failed"` outcome from `apply_plan` makes the process exit non-zero) and from `README.md` already treating a `leave` as ordinary output. A status of its own would be a new documented number, which is the human's decision and not a plan step.
  - **Option C was rejected for its semantics, not for an apply-time failure** — **[measured, and worth recording because the obvious argument is wrong]**. I expected `os.link` to follow the symlink and fail on a dangling target; it does not, and the move would have succeeded. The reason C is rejected is that it changes how every symlink is aged and still leaves the `is_dir()` and `EACCES` cases aborting. Written into ADR-0009 so that a later reader reconstructing the decision from the symptom does not rebuild it on a false premise.
  - **The wording, the test placement and symlink ageing are assumptions, not ADRs** — each reversible in one file, recorded under `plan.md` `## Assumptions` with what reversal costs.
  - **`README.md`'s `1` clause is left alone** — **[documented]**. It is BUG-0005's subject; rewriting it here would make two items unverifiable against their own criteria. Step 4 touches the `0` clause only.
  - **No question filed.** Every decision was answerable from ADR-0002, ADR-0006, ADR-0007, the vision and the code, or is reversible at the cost of one string in one file. Neither branch of `question.md` §1 that reaches the human was taken.
- **Questions raised:** none
- **Commands:**
  - `python3 -m tidy /tmp/bug4` and `python3 -m tidy /tmp/bug4 --apply` over the item's fixture → exit **2** both times, `tidy: /tmp/bug4 cannot be read: No such file or directory`, stdout empty, `photo.jpg` unmentioned and unmoved — the defect, reproduced on `main` after BUG-0003 merged
  - a `scandir` probe over that fixture → `broken.pdf`: `is_dir()` returns `False`, `stat()` raises `FileNotFoundError` errno 2; `photo.jpg`: both succeed — the exact call that aborts
  - `os.link("/tmp/bug4/broken.pdf", "/tmp/bug4dest/broken.pdf")` → **no error**: on this platform the dangling link is hard-linked rather than followed. This is what falsified the obvious argument against option C
  - `os.lstat("/tmp/bug4/broken.pdf").st_mtime` → a real timestamp, so option C would have produced an age
  - the same probe over a **symlink loop** (`ln -s loop.pdf loop.pdf`) → `is_dir()` **raises** `OSError` "Too many levels of symbolic links" before `stat()` is reached; `python3 -m tidy /tmp/bug4loop` → exit **2**, `tidy: /tmp/bug4loop cannot be read: Too many levels of symbolic links` — the second member of the class, and the reason the guard covers `is_dir()`
  - `grep -n "^class\|^    def test" tests/test_cli.py tests/test_planner.py` → the class layout the new tests join
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 69 tests ... OK`
  - `python3 -m compileall -q tidy tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 2 documents (ADR-0009 and the overview)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 9 items, 11 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings)
  - `every-criterion-is-addressed` → **pass** — `plan.md` `## Acceptance criteria mapping`, four rows for four criteria: AC1 → step 1, demonstrated by the end-to-end test in both modes plus the item's own reproduction run and pasted output; AC2 → step 1, demonstrated by assertions that `cannot be read` and `Traceback` are absent from **both** streams, which the chosen reason string is what makes possible; AC3 → steps 1 and 4, demonstrated by `status == 0` in both modes read against the amended exit-status paragraph; AC4 → steps 2, 3 and 5, demonstrated by the two new tests and by step 5's recorded failure against a reverted `planner.py`
  - `project-commands-resolved` → **pass** — `tracker/project.yaml` names `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q tidy tests`; both were run in this execution and both exited 0 with 69 tests. Unchanged by this item; ADR-0004 is the record of why they are these
  - `decisions-recorded` → **pass** — one ADR (ADR-0009) for the one decision with real alternatives, four assumptions each stating what reversal costs, and `plan.md` `## Decisions and ADRs` mapping every choice to one or the other. No second ADR was minted: the reason wording and the test placement have no alternative worth a document
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0, 2 documents; the ADR's two measured claims carry `[src: run: ...]` citations recording the command and its outcome)
  - `plan-is-executable-without-you` (advisory) → **pass** — re-read as a stranger: step 1 names the two calls by line number and states what the guard may not cover, the helper is given as code, step 2 names the assertions and the skip shape with an existing test to copy, step 4 quotes both README edits and says which clause not to touch, and step 5 names the two hazards that have produced a false pass in this project before. The step needing most care is 1, and `## Risks` says how a reviewer should check it
- **Artifacts:**
  - `tracker/items/BUG-0004/artifacts/plan.md` — created
  - `docs/architecture/adr/ADR-0009-one-entry-that-cannot-be-examined-is-a-leave.md` — created, v1
  - `docs/architecture/overview.md` — v6 → v7, one paragraph recording the two error boundaries, with the change-log row
  - `tracker/project.yaml` — unchanged; already resolved
- **Status:** `ready` → `planned`
- **Result:** BUG-0004 is planned. `build_plan` gains one guard around `entry.is_dir()` and `entry.stat()`; an `OSError` from either becomes `leave  <name>   [cannot be examined: <the OS's reason>]` and the rest of the folder is planned as usual. ADR-0009 records why the entry-level boundary belongs to the planner while the target-level one stays at the CLI, which is the part a future item inherits. Two facts were measured rather than assumed: a symlink loop aborts the scan from `is_dir()` before `stat()` is reached, and `os.link` does not follow a dangling symlink — the second one falsified the obvious argument against the alternative design.

## 2026-08-27T20:49:01Z — implement v0.2.2 — developer

- **Item:** BUG-0004
- **Trigger:** Status `planned`, dispatched by `next` as the best-ranked runnable item (priority `medium`, rank 3, ahead of BUG-0005 and WI-0003 on priority). This is the opening entry: the branch exists, no code has been written yet.
- **Inputs read:**
  - `tracker/items/BUG-0004/item.md` — the four criteria, the reproduction steps, and the three recorded symptom forms
  - `tracker/items/BUG-0004/artifacts/plan.md` — six steps, the guard's exact scope, the reason string, the two README edits quoted, and the AC mapping
  - `tracker/items/BUG-0004/history.md` — two rows, `— → ready` (verify) and `ready → planned` (plan); no send-back, so this is a fresh start rather than a resume
  - `tracker/items/BUG-0004/questions/` — empty; nothing to reconcile
  - ADR-0009 — the decision this item carries into the code, including the three properties of the guard that are not mine to re-decide; ADR-0006 — the target-level boundary the guard must leave alone
  - `tracker/project.yaml` — branch prefix `wi/`, trunk `main`, `commands.test` and `commands.lint` both set
  - `tidy/planner.py`, `tidy/cli.py`, `tests/test_cli.py`, `tests/test_planner.py`, `README.md` — the loop to guard, the handler that must keep working, the two test homes, and the two paragraphs step 4 amends
- **Decisions:**
  - **Fresh branch, not a resume.** `git branch -a` showed no `wi/BUG-0004`, and the history's last row is `plan`'s rather than a send-back. Branched from `main` at `73bb1f4`, the commit carrying this item's plan, ADR-0009 and overview v7.
- **Questions raised:** none so far
- **Commands:**
  - `git branch -a` → exit 0; `wi/BUG-0004` absent, five earlier item branches present
  - `git checkout -b wi/BUG-0004 main` → exit 0, head `73bb1f4`
- **Gates:**
  - `tests-pass` → **not yet run** (no change has been made; the gates run on the branch head after the last commit)
  - `lint-clean` → **not yet run** (same)
  - `workspace-valid` → **not yet run** as a completion gate; the transition accompanying this entry runs it
  - `every-criterion-has-a-test` → **not yet run** (no test written yet)
  - `commits-reference-the-item` → **not yet run** (no commits on the branch yet)
  - `no-unplanned-scope` (advisory) → **not yet run** (no diff yet)
  - `claims-are-sourced` → **not yet run** as a completion gate
- **Artifacts:**
  - branch `wi/BUG-0004`, created from `main` at `73bb1f4`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of BUG-0004 has started on `wi/BUG-0004`. The plan is one guard in `build_plan` around `entry.is_dir()` and `entry.stat()`, a reason helper beside `_no_rule_reason`, two regression tests and two sentences in `README.md`; nothing has been changed yet.

## 2026-08-27T20:52:40Z — implement v0.2.2 — developer

- **Item:** BUG-0004
- **Trigger:** Status `in-progress` on `wi/BUG-0004`, continuing this execution. This is the closing entry: the plan's six steps are done and the gates were run on the branch head.
- **Inputs read:**
  - `tracker/items/BUG-0004/artifacts/plan.md` — worked step by step; `## Approach` fixes the guard's scope, the reason string and the two README edits, and they were used as written
  - `tracker/items/BUG-0004/item.md` — the four criteria, unchanged by this execution
  - ADR-0009 — the three properties of the guard that are not mine to re-decide; ADR-0006 — the handler this change must leave alone; ADR-0007 — why the exit status does not move
  - `tidy/planner.py` `build_plan` — the loop, and the order that keeps an unrecognised file from ever being aged; `tidy/cli.py` — read, not edited
  - `tests/test_cli.py` `BadTargetTests` — the skip-by-attempted-operation shape copied for symlink creation; `tests/test_planner.py` `ScanTests`; `tests/cli_support.py` `run()`, which is in-process; `tests/support.py` `FolderTestCase`
  - `README.md` `## What it does` and the exit-status paragraph — the two places step 4 amends
  - `tests/test_planner.py::test_an_unrecognised_file_is_left_and_never_aged` — the test that decided the guard's shape: it pins that a file with no rule is never aged, so the guard could not be written as "stat every entry first"
- **Decisions:**
  - **The guard is one `try` around the existing loop body rather than two around the two calls.** The plan fixed three properties and left the shape to me. Two separate guards would have required reading `entry.stat()` before the `folder_for` check — stat-ing entries the current code deliberately never stats — which `test_an_unrecognised_file_is_left_and_never_aged` exists to prevent (WI-0002 AC6). Inside the single `try`, the only calls that can raise `OSError` are the two the ADR names: `folder_for` and `band_for` are pure lookups and `Action` is a frozen dataclass.
  - **The comment inside the `except` names both ADRs.** The next reader's question is "why is this caught here and not where the other one is caught", and the answer is a two-line comment rather than an archaeology exercise.
  - **The planner step produced two tests instead of one** — one pinning the reason string, one pinning that the other entries are still planned — so a failure says which of the two broke. Inside step 3's scope.
  - **The planner test asks the operating system for the wording**, `os.strerror(errno.ENOENT)`, rather than spelling out one platform's English. The reason string's *shape* is the contract; the sentence inside it belongs to the OS.
  - **The README's exit-status paragraph was re-wrapped**, because the `0` clause grew by seven words. No word of the `2` or `1` clauses changed — the `1` clause is BUG-0005's subject — but their line breaks moved, which `impl-report.md` `## Deviations` records for whoever implements BUG-0005.
  - **Nothing was escalated.** No decision arose that the plan and ADR-0009 do not make, and the one judgement inside the latitude — the guard's shape — is measured against an existing test rather than chosen by taste.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0004 main` → exit 0, head `73bb1f4`
  - `python3 -m tidy /tmp/dangling` and `... --apply` over the item's own reproduction fixture → exit **0** both times, `leave  broken.pdf   [cannot be examined: No such file or directory]` and `move   photo.jpg -> recent/images/photo.jpg`; `find /tmp/dangling` afterwards → `photo.jpg` under `recent/images/`, `broken.pdf` still in the top level
  - `python3 -m tidy /tmp/dangling 2>&1 | grep -c 'cannot be read'` → `0`, grep exit 1 — AC2 by hand
  - `python3 -m tidy /tmp/loopy` over a self-pointing symlink → exit **0**, `leave  loop.pdf   [cannot be examined: Too many levels of symbolic links]` — the `is_dir()` member of the class, which on `main` aborted the run with exit 2
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests ... OK` (69 before this item)
  - `python3 -m compileall -q tidy tests` → exit 0
  - `python3 -m unittest tests.test_cli.UnexaminableEntryTests -v` and `tests.test_planner.UnexaminableEntryTests -v` → exit 0, 1 and 2 tests, all `ok`
  - `git checkout main -- tidy/planner.py`, both `__pycache__` directories removed, `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t .` → exit 1, `Ran 72 tests ... FAILED (failures=3, errors=2)`; the failing set is exactly the three new tests and no other
  - `git checkout wi/BUG-0004 -- tidy/planner.py` then the suite again → exit 0, `Ran 72 tests ... OK`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 3 commit(s) on main..wi/BUG-0004 name BUG-0004"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 9 items, 11 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, "checked no documents changed since main"
  - `git diff main..wi/BUG-0004 --stat` → exit 0, eight files: `README.md`, `tests/test_cli.py`, `tests/test_planner.py`, `tidy/planner.py`, and four the tracker wrote
- **Gates:**
  - `tests-pass` → **pass** (`Ran 72 tests ... OK`, exit 0, run on the branch head after the last code commit)
  - `lint-clean` → **pass** (`compileall -q tidy tests` exit 0)
  - `workspace-valid` → **pass** (exit 0, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** — AC1, AC2 and AC3 are each asserted inside `test_a_dangling_symlink_does_not_cost_the_rest_of_the_folder`, in both modes, and AC1 again by `test_the_other_files_are_still_planned`; AC4 is demonstrated by the revert experiment with its exact output. The mapping is the table in `impl-report.md`
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 3 commits). It reported the same **false failure** at the opening transition as on BUG-0003 — an empty `main..wi/BUG-0004` read as "already merged into main" — for the fourth recorded time; recorded in `impl-report.md` `## What I did not do` item 3
  - `no-unplanned-scope` (advisory) → **pass** — four hunks in four files, each traceable: the guard and `_unexaminable_reason` (step 1), the CLI test class and its docstring line (step 2), the planner test class with its `errno` import (step 3), and the two README edits (step 4)
  - `claims-are-sourced` → **pass** (exit 0). "No documents changed since main" is correct: this branch touches nothing under `docs/`; ADR-0009 and overview v7 were linted on `main` when `plan` wrote them
- **Artifacts:**
  - `tracker/items/BUG-0004/artifacts/impl-report.md` — created: the reproduction run verbatim in both modes, the four-row evidence table, three deviations, the gate table and five declared omissions
  - branch `wi/BUG-0004`, commits `7ab0811` (the guard and both test classes), `1156654` (the README), `38218c0` (the opening tracker entry), plus this entry's commit
  - `tidy/planner.py` — the `try`/`except OSError` in `build_plan` and the `_unexaminable_reason` helper
  - `tests/test_cli.py` — `UnexaminableEntryTests` and the module docstring; `tests/test_planner.py` — `UnexaminableEntryTests`, `import errno`, the module docstring
  - `README.md` — one example line, one sentence, and seven words in the exit-status paragraph
- **Status:** `in-progress` → `verifying`
- **Result:** A dangling symlink now costs the user that entry and nothing else: `leave  broken.pdf   [cannot be examined: No such file or directory]` on stdout, every other file planned and moved as usual, exit 0 in both modes, and no sentence anywhere claiming the folder could not be read. The same guard catches the `is_dir()` member of the class — a symlink loop — which aborted the run on `main`. ADR-0006's target-level handler is untouched and BUG-0001's regression test still passes; the three new tests are proven to fail against the reverted planner and the other 69 are unaffected in both directions.

## 2026-08-27T20:58:11Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0004
- **Trigger:** `verifying` — `next` dispatched `verify` as the status owner; highest-ranked runnable item (priority rank 3, ahead of BUG-0005 and WI-0003 at rank 4).
- **Inputs read:**
  - `tracker/items/BUG-0004/item.md` — the four acceptance criteria, read before anything else and before the implementation report, so each check was derived from the criterion rather than from what was built
  - `tracker/items/BUG-0004/artifacts/plan.md` — the delegated choices, the out-of-scope list, and the three risks it asked verification to exercise
  - `tracker/items/BUG-0004/artifacts/impl-report.md` — the claims, checked rather than trusted
  - `tracker/items/BUG-0004/history.md`
  - `tracker/project.yaml` — the test and lint commands
  - the code at `wi/BUG-0004` head `ab644840c026e5f546128dd1700102539824000d`, and `git diff main..wi/BUG-0004`
  - `README.md` lines 19-38, for AC3
- **Decisions:**
  - **All four criteria pass; the item goes to `in-review` and no defect is filed.** Every verdict rests on a command run in this execution; no row of the report cites `impl-report.md` as its evidence.
  - **AC4's revert experiment was re-run here rather than quoted.** The report's claim is the kind that is cheap to assert and expensive to check, so it was checked: `git checkout main -- tidy/planner.py`, caches cleared, `PYTHONDONTWRITEBYTECODE=1`, and `grep -c _unexaminable_reason` → `0` to confirm the revert was really in the file before running. Exactly the three new tests failed and the 69 pre-existing ones did not; restored and re-verified clean.
  - **The mode banner disappearing when nothing moves is not a defect and was not filed as one.** It showed up in three boundary cases. It is WI-0001's decided behaviour, settled at WI-0001/Q-001 and commented at `tidy/cli.py:72`, and it reproduces identically on a folder with no symlinks at all — so it is neither this item's failure (no criterion mentions it) nor another item's defect (its item decided it deliberately). Recorded as an observation in `verify-report.md` `## Defects found` instead.
  - **The symlink-loop case was exercised although no criterion names it**, because `plan`'s `## Risks` identified it as the case a guard around `stat()` alone would miss while every AC still passed. It is handled: `leave  loop.pdf   [cannot be examined: Too many levels of symbolic links]`, exit 0.
  - **No criterion was judged ambiguous.** AC3 was the only one needing a judgement — it asks that the status be documented *and* that the document say which case — so both halves were read against each other rather than the status alone being looked up.
  - **The two implementation choices `plan` delegated were checked against the properties it fixed, not against taste.** One `try` rather than two: `os.scandir` is outside it, and the only calls inside that can raise `OSError` are `entry.is_dir()` and `entry.stat()`. `except OSError` rather than `except FileNotFoundError`: boundary case 1 shows it is load-bearing.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `ab644840c026e5f546128dd1700102539824000d`, exit 0
  - `git status --short` → empty, exit 0
  - `rm -rf tidy/__pycache__ tests/__pycache__` then `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests in 0.062s`, `OK`
  - `python3 -m compileall -q tidy tests` → exit 0, no output
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 9 items, 11 documents, 0 errors 0 warnings
  - `mkdir -p /tmp/v4 && echo x > /tmp/v4/photo.jpg && ln -s /tmp/v4/gone.pdf /tmp/v4/broken.pdf` → exit 0 (the item's own fixture)
  - `python3 -m tidy /tmp/v4` (streams captured separately) → exit 0, stdout the `leave` and `move` lines, stderr the preview banner
  - `python3 -m tidy /tmp/v4 --apply` → exit 0, same two lines; `find /tmp/v4 | sort` → `photo.jpg` under `recent/images/`, `broken.pdf` still top-level; `ls -l /tmp/v4/broken.pdf` → still a symlink
  - `grep -c 'cannot be read'` and `grep -c 'Traceback'` over all four captured streams → `0` eight times (grep exit 1, no match)
  - `grep -n -A5 'Exit status' README.md` → exit 0, line 34 names the case
  - `git checkout main -- tidy/planner.py` → exit 0; `grep -c _unexaminable_reason tidy/planner.py` → `0`; `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t .` → exit 1, `Ran 72 tests ... FAILED (failures=3, errors=2)`
  - `git checkout wi/BUG-0004 -- tidy/planner.py` → exit 0; `grep -c _unexaminable_reason` → `2`; `git status --short` → empty; suite → exit 0, `Ran 72 tests ... OK`
  - `python3 -m tidy /tmp/b1` (symlink loop beside `photo.jpg`) → exit 0, `leave  loop.pdf   [cannot be examined: Too many levels of symbolic links]`
  - `python3 -m tidy /tmp/b2` and `--apply` (every entry dangling) → exit 0 both, two `leave` lines then `Nothing to do: ...`, both links still on disk
  - `python3 -m tidy /tmp/b3` (dangling `broken.xyz`, dangling extensionless `noext`) → exit 0, `[no rule for '.xyz']` and `[no extension]` — the guard has not been pulled above the extension check
  - `python3 -m tidy /tmp/b6` (`dirlink -> realdir`, `filelink.jpg -> target.jpg`, targets present) → exit 0, directory link still skipped, file link still moved and still aged by its target
  - `python3 -m tidy /tmp/b7` (a file named `recent/documents` blocking the destination) → exit 0, `leave  report.pdf   ['recent/documents' exists and is not a folder]` — the collision reason is not flattened into `cannot be examined`
  - `python3 -m tidy /tmp/b4` (a lone `notes.xyz`, no symlinks) → exit 0 — the control that shows the missing banner is pre-existing
  - `python3 -m tidy /tmp/does-not-exist-zz` → exit 2; `python3 -m tidy /tmp/afile.txt` → exit 2; `python3 -m tidy /tmp/b5` at mode 000 → exit 2, `cannot be read: Permission denied` — ADR-0006's boundary intact
  - `git diff main..wi/BUG-0004 -- tidy tests README.md`, `git diff --stat main..wi/BUG-0004`, `git diff --name-only main..wi/BUG-0004 | grep -v '^tracker/'` → exit 0; four non-tracker files, four hunks, all accounted for by plan steps 1-4
  - `rm -rf` of every `/tmp` fixture built here → exit 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` at `ab64484`, caches cleared, exit 0, `Ran 72 tests ... OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 0 errors 0 warnings)
  - `every-criterion-independently-checked` → **pass** (each of AC1-AC4 has a command run in this execution and its quoted output in `verify-report.md` `## Criteria`; none cites the implementation report)
  - `negative-cases-exercised` → **pass** (six conditions triggered, not read about: the symlink loop, the all-unexaminable folder, the unexaminable entry with no rule, both resolvable symlink shapes, the destination collision, and all three of ADR-0006's target-level failures)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (the revert experiment above: three tests fail against `main`'s planner, 69 unaffected, restored clean)
- **Artifacts:**
  - `tracker/items/BUG-0004/artifacts/verify-report.md` — created, with `Verified-commit: ab644840c026e5f546128dd1700102539824000d`
  - `tracker/items/BUG-0004/item.md` — AC1, AC2, AC3 and AC4 ticked, each against a command in this execution
  - no bug items filed
  - commit of this execution's tracker files, per `conventions.commit-subject`
- **Status:** `verifying` → `in-review`
- **Result:** BUG-0004 passes all four of its acceptance criteria on `ab64484`, verified against the item's own reproduction fixture rather than against the implementation report, with the revert experiment re-run here and the same guard shown to handle the symlink loop no criterion names. ADR-0006's target-level boundary, WI-0002's never-age-an-unrecognised-file rule and the destination-collision reason all still behave as their own items left them, so the fix is contained to the case it was filed for.

## 2026-08-27T21:05:14Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0004
- **Trigger:** `in-review` — `next` dispatched `review-close` as the status owner; highest-ranked runnable item (priority rank 3, ahead of BUG-0005 and WI-0003 at rank 4).
- **Inputs read:**
  - `tracker/items/BUG-0004/item.md` — the four criteria, all ticked, and the outcome to be recorded
  - `tracker/items/BUG-0004/artifacts/verify-report.md` — the evidence behind each tick and the four declared gaps
  - `tracker/items/BUG-0004/artifacts/impl-report.md` — the three deviations and the five declared omissions
  - `tracker/items/BUG-0004/artifacts/plan.md` — the six steps, the AC mapping, the three risks and the out-of-scope list
  - `tracker/items/BUG-0004/journal.md` — all five entries, in full, read rather than skimmed, because this execution certifies the record is complete
  - `tracker/items/BUG-0004/history.md` — five rows, chaining `— → ready → planned → in-progress → verifying → in-review`
  - `tracker/items/BUG-0004/questions/` — empty when this review opened
  - `git diff main..wi/BUG-0004`, the range `73bb1f4..5b5b92c9`, read hunk by hunk
  - `docs/architecture/adr/ADR-0009` and `ADR-0006` in full; `ADR-0002` and `ADR-0007` where the change relies on them; `ADR-0008`'s one code citation
  - `docs/architecture/overview.md` v7 — the two-error-boundaries paragraph, the module table, the destination commitment
  - `tidy/planner.py` and `tidy/cli.py` at the branch head, opened at each line a document cites
  - `tracker/items/BUG-0002/questions/Q-002.md` — the precedent for correcting a factual clause inside a current ADR
  - `.claude/agile-skills/spec/doc-header.md` §4a and §5, and `spec/dor-dod.md` §3
- **Decisions:**
  - **Suspended rather than closed, on the record and not on the code.** The change itself would be accepted: four hunks, each traceable to a plan step and a criterion, no unrequested scope, and a verification that triggered six boundary conditions and re-ran the revert experiment rather than quoting it. D1, D2, D3, D5, D6, D8, D10 and D11 pass. D7 and D12 fail, and both failures are in `docs/`.
  - **Finding 1 — ADR-0006's `## Consequences` is now partly false, and it is escalated, not fixed.** Its "a genuine defect inside `build_plan` that surfaced as an `OSError` would now be reported as an unusable target" stops being true for the region this item guards: such an error now becomes a `leave` line and the run exits 0. The decision ADR-0006 records is untouched — all three of its target-level cases still exit 2 — so this is a stale consequence paragraph, which is the shape BUG-0002/Q-002 established a remedy for. `review-close` may not edit an ADR (`spec/doc-header.md` §5 makes that class "superseded only"), so it is **Q-001** to the architect.
  - **Finding 2 — ADR-0009's line citations stop pointing at what they name, and that is a decision rather than a repair.** Its six `tidy/planner.py:NN` citations were exact against `main` and drift by 1 to 19 lines once the nine-line guard lands: `:47` becomes `try:`, `:55` becomes `continue`, `:114` lands in a different function from the call it cites. The claims stay true and `lint-claims` passes, because §4a's table makes a path citation resolve when the *file* exists — so no gate catches it, and what breaks is D12 §9a's own procedure, which says to open what a sentence cites and decide from what is there. Filed as **Q-002** with the general question attached, because an ADR whose subject is a change to a file cites that file, and the change invalidates its own line numbers.
  - **Two questions, not one.** The two documents are wrong in different ways and the remedies differ — one is a factual correction with a version bump, the other is a choice about how ADRs cite code at all — so folding them together would get one of them half-answered (`spec/question.md` §2, one decision per question).
  - **Not merged, deliberately.** Both remedies edit documents on `main`, so the trunk will move before this review resumes; a trial merge run now would be a trial of a state that will not exist. The trial merge, the trunk-did-not-move check and the merge-result test all belong to the execution that resumes at `in-review`.
  - **No send-back and no bug item.** A send-back would put the item with `implement`, which may not write to `docs/` — the status owner could not perform the fix. A bug item would be a second-class route to the same edit that `answer-questions` makes directly, and would let the item close with a known-false sentence in a current ADR.
  - **Five gaps accepted, and copied out of the reports into `item.md` `## Notes`.** An accepted gap that lives only in a verification report stops being read the moment the item closes. The `EACCES`/`EIO` gap, the deleted-mid-scan race, the unexecuted skip path, the README re-wrap that BUG-0005 must re-read, and the pre-existing banner suppression are now all in the item itself.
  - **The banner suppression is not a defect and was not filed as one.** `verify` reached the same conclusion independently; I checked it the same way, against `tidy/cli.py:72` and WI-0001/Q-001, and it reproduces on a folder containing no symlinks at all.
- **Questions raised:** Q-001, Q-002 (both `addressed-to: architect`, both blocking)
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0004 wi/BUG-0004` → exit 0: "verified at `ab644840`; `wi/BUG-0004` has moved to `5b5b92c9` but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 5 commit(s) on main..wi/BUG-0004 name BUG-0004"
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests in 0.064s`, `OK` (D3, on the branch head as it stands now)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, "checked no documents changed since main", 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before the questions were filed; exit 1 after, reporting `question.blocking.not-suspended` and a stale board — which is the state this transition resolves
  - `git diff main..wi/BUG-0004 -- tidy tests README.md`, `git diff --stat`, `git diff --name-only … | grep -v '^tracker/'` → exit 0; four non-tracker files, four hunks
  - `grep -rn "planner.py:[0-9]\|cli.py:[0-9]\|apply.py:[0-9]\|rules.py:[0-9]" docs/` → exit 0, six citations in ADR-0009 and one in ADR-0008 — the D12 audit's worklist
  - `grep -n "" tidy/planner.py | sed -n '40,75p'`, `sed -n '84,100p'`, `sed -n '120,126p'` → the post-merge contents of every line ADR-0009 cites
  - `git show main:tidy/planner.py | sed -n '47p;55p;85p;114p'` → `if entry.is_dir():`, `band = band_for(now - entry.stat()…)`, `if os.path.lexists(path) and not os.path.isdir(path):`, `return destination in reserved or os.path.lexists(…)` — proving the citations were exact when written and that the guard is what moved them
  - `sed -n '67p;93p' tidy/cli.py` → `except OSError as error:` and `return 1 if any(outcome.kind == "failed" …) else 0` — ADR-0009's two `cli.py` citations still exact
  - `sed -n '60,80p' docs/architecture/overview.md`, `sed -n '85,92p;105,115p' docs/architecture/adr/ADR-0006-…md` → the two paragraphs Findings 1 and 2 turn on
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → the `created` stamps on Q-001 and Q-002
  - **not run, and why:** `git worktree add --detach`, the merge-result test run, and `git rev-parse main` before and after — the trial merge is deferred with the merge itself, because answering the two questions will move `main`
- **Gates:**
  - `definition-of-done` → **fail** — walked criterion by criterion in `review.md` `## Definition of Done`, twelve rows with twelve results. D1, D2, D3, D5, D6, D8, D10, D11 pass; D4 fails (Q-001 and Q-002 now open); D7 fails (ADR-0006 not updated, Finding 1); D9 not yet (not merged, deliberately); D12 fails (eleven claims audited from their citations, nine hold, Findings 1 and 2)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the only movement since `ab644840` is five files under `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 5 commits; no false failure this time, since the branch is not empty)
  - `tests-pass-on-the-merge-result` → **skipped** — there is no merge result to test. The branch is deliberately unmerged and `main` will move when the questions are answered; this gate belongs to the execution that resumes and merges
  - `workspace-valid` → **pass** (exit 0 as the transition ran it; the two errors between filing the questions and this move are exactly what the move resolves)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone. *What was built and why:* one guard in `build_plan` so a dangling symlink costs its own entry and nothing else — `item.md`, ADR-0009, `README.md`. *Which skill decided what:* `verify` filed it and fixed `found-in` by running three trees; `plan` decided ADR-0009 and its four details; `implement` chose the single `try` against an existing test; `verify` passed all four criteria. *What questions arose:* none until this review; Q-001 and Q-002 now, both recorded with options and a recommendation. *What verification found:* four passes, six boundary conditions, four declared gaps — `verify-report.md`
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0). Worth recording that this gate passing is compatible with Finding 2: it checks that a citation resolves to a file, not that the cited line supports the sentence
  - `epic-sign-off` → **skipped** — this execution reviews a bug, not an epic; `engagement-state EP-001` reported `active` with BUG-0004, BUG-0005 and WI-0003 still in flight when `next` dispatched this run, so the engagement is not at rest and DE7's trigger has not fired
- **Artifacts:**
  - `tracker/items/BUG-0004/artifacts/review.md` — created: what was examined including the eleven-claim D12 audit table, the twelve-row Definition of Done, two findings, five accepted gaps, and a verdict that says why the item is suspended rather than merged
  - `tracker/items/BUG-0004/questions/Q-001.md` — ADR-0006's stale consequence paragraph, four options, recommendation A
  - `tracker/items/BUG-0004/questions/Q-002.md` — ADR-0009's drifting line citations, four options, recommendation B (and D if the class is worth a standing rule)
  - `tracker/items/BUG-0004/item.md` — `## Notes` gains the five accepted gaps
  - no merge, no bug items filed
  - commit of this execution's tracker files, per `conventions.commit-subject`
- **Status:** `in-review` → `awaiting-answer`
- **Result:** BUG-0004's code passes review and its record does not. The change is four hunks, each traceable to a plan step, verified against six boundary conditions; but the merge makes one paragraph of ADR-0006 untrue and moves every line ADR-0009 cites, and `review-close` may edit neither. The item is suspended at `awaiting-answer` with `resume-to: in-review`, carrying Q-001 and Q-002 to the architect, and is deliberately left unmerged because both remedies will move `main` before this review resumes.

## 2026-08-27T21:09:01Z — answer-questions v0.3.1 — architect

- **Item:** BUG-0004
- **Trigger:** `awaiting-answer` — `next` step 4 dispatched `answer-questions` on the item owning the oldest open architect-addressed question (Q-001, created 21:01:43Z). No request and no human-addressed question was open, so the candidate set was never built.
- **Inputs read:**
  - `tracker/items/BUG-0004/questions/Q-001.md` and `Q-002.md` — both `addressed-to: architect`, both blocking, both filed by `review-close` in this round
  - `tracker/items/BUG-0004/history.md` — the suspending row carries `resume-to: in-review`, read from the row rather than inferred from which skill asked
  - `tracker/items/BUG-0004/item.md`, `artifacts/review.md`, `artifacts/plan.md`, `artifacts/verify-report.md` — what the review examined and what it found
  - `docs/architecture/adr/ADR-0006` v1 in full and `ADR-0009` v1 in full — the two documents the questions are about
  - `docs/architecture/adr/ADR-0007` v2 and `tracker/items/BUG-0002/questions/Q-002.md` — the precedent for correcting a factual clause inside a `status: current` ADR, and the reasoning it recorded
  - `docs/architecture/overview.md` v7, `ADR-0002`, `ADR-0008` — checked for the same class of stale citation; `ADR-0008`'s `[src: tidy/cli.py:52]` is still exact
  - `.claude/agile-skills/spec/doc-header.md` §3, §4, §4a and its citation table, and §5's "which skill writes what"; `spec/question.md` §4; `spec/dor-dod.md` D12
  - `tidy/planner.py` and `tidy/cli.py` at the branch head, opened at the lines under discussion
  - `git log --oneline --all -- docs/architecture/adr/ADR-0007-…md` and `git branch --contains d0a7ebd` — to establish where this project puts a document correction
- **Decisions:**
  - **Q-001 → answered, option A, from the record.** ADR-0006's `## Consequences` cost paragraph is corrected in place and the ADR goes to v2 with a change-log row. The route is *from an existing document*: BUG-0002/Q-002 asked this exact question about ADR-0007 and answered it, on grounds that transfer word for word — `spec/doc-header.md` §4's "never edited to change its decision" governs the **decision**, while §3 requires every content change to bump the version and add a row, so the class is editable on matters of fact and the row is what keeps it honest. ADR-0007 stands at `version: 2, updated-by: answer-questions` as the precedent in force.
  - **The correction states the two halves rather than deleting the cost.** An `OSError` from `os.scandir` or outside the guard still reaches `cli.py` and is reported as an unusable target; one raised while interrogating an entry becomes that entry's `leave` line and never arrives. The new text says explicitly that a defect in the guarded region surfaces **more quietly** than before — that is the fact a future `plan` judging "may I widen this guard?" needs, and the version this review found had it inverted.
  - **Q-002 → answered, option B, from the record plus one decision of mine.** ADR-0009's six `tidy/planner.py:NN` citations become file-level. What made it answerable from the record is `spec/doc-header.md` §4a's own citation table: `path` and `path:line` are one form with one test — the file exists — so the line number was never what made the citation valid, and dropping it forfeits nothing a gate measures. Every one of those sentences already names its subject in backticks, which is a search term that survives edits above it.
  - **Option A on Q-002 rejected on the question's own evidence** — repointing buys accuracy until the next edit, and WI-0003 is already scoped to change where the rule tables come from, which moves these lines again. **C rejected** because §4's "preserve what was believed at the time" protects the decision and the reasoning, not the accuracy of a pointer, and leaving it means D12's own procedure lands on `continue`.
  - **D not taken, on a rule rather than a preference.** `spec/doc-header.md` §5 makes `process/ways-of-working.md` a document `plan` *creates* and this skill may only update; it does not exist here yet, so minting the standing convention would exceed what `answer-questions` may write. The class-level reasoning is instead a new `## Consequences` bullet in ADR-0009 — "an ADR about a change to a file cites that file, and the change is what moves its own line numbers" — where the next `plan` will read it, and can lift it into `ways-of-working.md` if it wants it binding.
  - **The edit was kept to what was asked.** Only the six planner citations changed. ADR-0009's two `tidy/cli.py` citations and ADR-0008's one were re-checked line by line and are exact, because no item in play touches `cli.py`; rewriting correct citations no question named would have widened the answer past the ask.
  - **No escalation, on either question.** Checked against all four of `spec/question.md` §4's conditions and none holds: no intent is required that the record does not carry, both edits are reversible in one commit, neither contradicts an ADR — ADR-0006's decision is untouched and ADR-0009's is restated unchanged — and the record is the opposite of silent, since this project has answered the first question once already.
  - **No scope widening, so no new item.** Neither answer implies work no item records (`spec/question.md` step 3b). The citation-drift class is a property of the methodology under `.claude/agile-skills/`, which is out of this project's scope; it is recorded in the ADR and reported to the toolkit's owner rather than filed against EP-001.
  - **One correction to the record, made where corrections belong rather than by rewriting the artifact.** `review.md` `## Verdict` predicted that answering these questions would move `main` and that a trial merge now would therefore be a trial of the wrong state. That is wrong: this project's precedent puts a document correction on the item's branch — BUG-0002's ADR-0007 v2 is `d0a7ebd`, made on `wi/BUG-0002` — so both edits are commits on `wi/BUG-0004` and `main` is untouched at `73bb1f4`. Recorded in Q-001's `## Answer` and here; `review.md` is left as written, because it is what the reviewer believed at the time and the resumed review will read this entry.
- **Questions raised:** none — neither question was re-addressed to the human
- **Commands:**
  - `git log --oneline --all -- docs/architecture/adr/ADR-0007-tagged-outcomes-from-apply-plan.md` → exit 0, `d0a7ebd tracker: the answered questions, overview v5 and ADR-0007 v2 (refs BUG-0002)`; `git branch --contains d0a7ebd` → `main`, `wi/BUG-0002`, `wi/BUG-0003`, `wi/BUG-0004` — the precedent for where a document correction is committed
  - `grep -n "A cost worth naming" -A 5 docs/architecture/adr/ADR-0006-…md` and `sed -n '1,10p'` → the paragraph and the v1 frontmatter to be edited
  - `sed -n '82,92p' docs/architecture/adr/ADR-0009-…md`, `grep -n "src: tidy/planner.py"` → the six citations, before and after
  - `git show main:tidy/planner.py | sed -n '47p;55p;85p;114p'` (in the review that filed these) → the citations were exact against `main`; re-read here as the basis for option B rather than taken from the question
  - `sed -n '67p;93p' tidy/cli.py`, `sed -n '52p' tidy/cli.py` → the three `cli.py` citations left alone, each still naming what its sentence says
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, "checked 2 document(s) changed since main", 0 errors 0 warnings — run after both edits, so the new citations resolve
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `OK` (no code was touched; run to confirm that)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 between the answers and this transition, reporting `question.awaiting.none-open` and a stale board — which is precisely the state this move resolves; exit 0 as the transition runs it
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → the `updated` and `answered-at` stamps
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in a `## Consequences` section was opened afterwards and contains the change. Q-001 → `ADR-0006`: the cost paragraph is the two-halves text (read back at lines 109-119), frontmatter is `version: 2, updated-by: answer-questions, updated-for: BUG-0004, updated: 2026-08-27T21:06:34Z`, change-log row 2 present. Q-002 → `ADR-0009`: `grep -c "tidy/planner.py:[0-9]"` → **0** remaining line citations, the new `## Consequences` bullet is at line 125, frontmatter is `version: 2, updated-by: answer-questions`, change-log row 2 present. Neither `## Consequences` names a file that was not edited, and neither names an intention
  - `answered-from-the-record` → **pass** — Q-001 follows from BUG-0002/Q-002 and `spec/doc-header.md` §3/§4, both cited in the answer; Q-002 follows from `spec/doc-header.md` §4a's citation table, cited, plus one architectural choice recorded in ADR-0009's `## Consequences` rather than left in the question file. Neither answer required a new ADR: no decision with real alternatives was taken about the *system*, only about how one existing ADR cites the code it describes
  - `escalation-is-justified` → **not applicable** — nothing was escalated. Recorded rather than omitted: both questions were checked against all four conditions in `spec/question.md` §4 and none applies, and "answering would take a while" is not among them
  - `workspace-valid` → **pass** (exit 0 as the transition ran it, with the pending move declared; the two errors it reported beforehand are the ones this move clears)
  - `item-resumed-correctly` → **pass** — `resume-to: in-review`, read from the `in-review → awaiting-answer` row that `review-close` wrote at 21:05:14Z, and the new row's target is `in-review`. Not inferred from which skill asked: the same suspension shape from `verify` would have meant `verifying`, and inferring would have silently discarded a completed verification
  - `a-deferral-is-not-an-answer` → **not applicable** — neither reply defers. Both questions were answered outright by this skill, with a decision and a consequence in a file; neither `status: deferred` was set and no item was parked at `blocked`
- **Artifacts:**
  - `tracker/items/BUG-0004/questions/Q-001.md` — `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-27T21:07:06Z`; `## Answer` records option A with its basis and the correction about where the commits land; `## Consequences` names ADR-0006 and this item's record
  - `tracker/items/BUG-0004/questions/Q-002.md` — same stamps; `## Answer` records option B, why A and C were rejected, why D is not this skill's to take, and the scope of the edit; `## Consequences` names ADR-0009 and this item's record
  - `docs/architecture/adr/ADR-0006-report-an-unusable-target-at-the-cli-boundary.md` — v1 → **v2**: the `## Consequences` cost paragraph restated as the two halves it has become since ADR-0009, with citations; change-log row 2
  - `docs/architecture/adr/ADR-0009-one-entry-that-cannot-be-examined-is-a-leave.md` — v1 → **v2**: six `tidy/planner.py:NN` citations replaced with file-level ones across `## Context`, `## Options considered` and `## Decision`, one duplicated pair collapsed and its paragraph re-wrapped, one new `## Consequences` bullet recording why this record cites files and symbols; change-log row 2
  - no ADR created, no bug filed, no work item filed, no acceptance criterion amended
- **Status:** `awaiting-answer` → `in-review`
- **Result:** Both of `review-close`'s questions are answered from the record, and both answers have landed in the documents they are about: ADR-0006 v2 no longer says a defect inside `build_plan` would be reported as an unusable target, because since ADR-0009 half of that class becomes a quiet `leave` line instead; ADR-0009 v2 cites `tidy/planner.py` by file and by symbol, because the nine-line guard it decides is what moved every line it used to cite. BUG-0004 returns to `in-review` with its two D12 findings closed, unmerged, and `main` untouched at `73bb1f4`.

## 2026-08-27T21:18:29Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0004
- **Trigger:** `in-review` — `next` dispatched `review-close` as the status owner. Highest-ranked runnable item at priority rank 3 (medium); BUG-0005 and WI-0003 both rejected at rank 4. Round 2 of this review: `answer-questions` returned the item here at 21:09:01Z with Q-001 and Q-002 answered.
- **Inputs read:**
  - `tracker/items/BUG-0004/item.md` — the four ticked criteria and the five gaps round 1 recorded in `## Notes`
  - `tracker/items/BUG-0004/history.md` — 7 rows, chaining `— → ready → planned → in-progress → verifying → in-review → awaiting-answer → in-review`, last row matching the item's status
  - `tracker/items/BUG-0004/journal.md` — all 7 entries in full, including `review-close`'s own round-1 entry and `answer-questions`' at 21:09:01Z, read rather than skimmed because this execution certifies the record is complete
  - `tracker/items/BUG-0004/artifacts/plan.md` (the six steps, the AC mapping, the three properties ADR-0009 fixed), `impl-report.md` (three deviations, five declared omissions), `verify-report.md` (the per-AC evidence and four declared gaps), `review.md` (round 1, in full)
  - `tracker/items/BUG-0004/questions/Q-001.md` and `Q-002.md` — both `status: answered`, `answered-by: answer-questions`, and each file named in their `## Consequences` sections opened afterwards
  - `git diff main..wi/BUG-0004`, the range `73bb1f4..d8582121`, re-read hunk by hunk — fifteen files, four outside `tracker/`
  - `docs/architecture/adr/ADR-0006` v2 and `ADR-0009` v2 in full, including frontmatter and both change-log tables; `ADR-0008` at the citation on line 48; `ADR-0002` and `ADR-0007` where the change relies on them
  - `docs/architecture/overview.md` v7 — the two-error-boundaries paragraph at lines 64-73, the module table, and the "every destination is decided in `planner.py`" commitment
  - `tidy/planner.py` and `tidy/cli.py` at the branch head, opened at every line the audited documents cite
  - `tracker/items/BUG-0005/item.md` — as the shape reference for a documentation-defect bug, before filing BUG-0006
  - `.claude/agile-skills/spec/dor-dod.md` §3 (D1-D12), `spec/doc-header.md` §4a and §5, `spec/work-item.md` §3, `spec/ids-and-statuses.md` §5
- **Decisions:**
  - **Accepted and merged.** All twelve Definition of Done criteria pass on the final state, walked one by one with their own evidence in `review.md` `## Definition of Done` `### Round 2`. Round 1's D4, D7, D9 and D12 failures are all closed.
  - **Finding 1 closed against the code, not against the correction.** ADR-0006 v2's rewritten cost paragraph was checked by opening `tidy/cli.py`'s `except OSError` handler and `build_plan`'s guard and by running the fixture, not by reading the new prose. Its three assertions — an error from outside the guard still exits 2, one from inside becomes a `leave` and the run exits 0, and a defect in the guarded region therefore surfaces *more* quietly — are each true. The version bump and change-log row are present.
  - **Finding 2 closed and measured.** `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` finds three `path:line` citations left in the whole of `docs/`, none into `planner.py`; the six ADR-0009 cited are gone. ADR-0009 v2's own historical claim — that all six were exact against `main` — was re-checked with `git show main:tidy/planner.py` rather than taken from the answer.
  - **Finding 3 — ADR-0008 line 48 cites `tidy/cli.py:52`, which is a blank line — filed as BUG-0006 at `ready` rather than fixed or held against this item.** The claim is true and the statement it names is at line 54. It belongs to BUG-0003: `git show b76b27c:tidy/cli.py | sed -n '52p'` prints the cited statement, and BUG-0003's own `46e5fd0` two commits later is what moved it. `tidy/cli.py` is not in this item's diff and no BUG-0004 criterion covers it, so it is neither a send-back nor a bar to closing; `spec/ids-and-statuses.md` §5 gives this skill the authority to file the item it observed the need for. Precedent: BUG-0005, filed the same way from BUG-0002's review, in a commit on that item's branch.
  - **Round 1's own D12 audit was wrong on one row, and the correction is recorded rather than overwritten.** It marked the ADR-0008 citation "**true** — unaffected, this item does not touch `cli.py`". "Unaffected by this change" and "supports its sentence" are different questions, and D12 §9a asks the second. `answer-questions` reached the same conclusion the same way; both checks ran `sed -n '52p'`, which prints a blank line and reads as agreement when the expected content is not held up beside it. `review.md` round 2 says so in `## What I examined`.
  - **`review.md` carries both rounds; round 1's text is unchanged.** A review records what its reviewer believed at the time, so round 1's `## Verdict` — including its prediction that `main` would move, which did not hold — stands, with a `### Round 2` subsection under each heading saying where and why the two disagree. A preamble at the top says so, so a reader who stops early is not misled.
  - **Two more gaps accepted, and copied into `item.md` `## Notes` rather than left in this review.** The three surviving `path:line` citations are unguarded by any gate, and round 1's verdict contains a prediction that did not hold. Both are now in the item, where they survive it closing.
  - **One stale citation in the tracker was fixed in place rather than filed.** Round 1's own note cited `tidy/cli.py:72` for the banner suppression; line 72 is blank and the guard is `if moves:` two lines below. It is in `item.md`, which this skill owns and writes, not in `docs/` — so it was corrected to name the symbol, and the correction is recorded in `## Notes` as one more instance of the class BUG-0006 carries rather than silently repaired.
  - **The engagement was not ended, and that was the script's verdict, not mine.** `engagement-state EP-001` reports `active` after this close, with BUG-0005, WI-0003 and now BUG-0006 still in flight. No sign-off question is due.
- **Questions raised:** none — round 1's Q-001 and Q-002 were answered before this execution and nothing new required the architect or the human
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0004 wi/BUG-0004` → exit 0: "verified at `ab644840`; `wi/BUG-0004` has moved to `d8582121` but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code" — run, not assumed; the branch moved twice since verification
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 7 commit(s) on main..wi/BUG-0004 name BUG-0004"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, "checked 2 document(s) changed since main", 0 errors 0 warnings
  - `git rev-parse main` before the trial → `73bb1f459d541f90c49576c2ca34f5a20456bc38`
  - `git worktree add --detach /tmp/trial-bug4 main` → exit 0, "HEAD is now at 73bb1f4"; `git -C /tmp/trial-bug4 merge --no-ff wi/BUG-0004` → exit 0; `git -C /tmp/trial-bug4 rev-parse HEAD` → `54251e84c08e080c54bdc17ac9a800d0dd3d0f7d`
  - in `/tmp/trial-bug4`: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests in 0.065s`, `OK`; `python3 -m compileall -q tidy tests` → exit 0
  - `git worktree remove --force /tmp/trial-bug4` → exit 0; `git rev-parse main` after → `73bb1f45…`, identical to before, so the trial published nothing and moved no ref
  - `python3 -m tidy /tmp/rv4` and `python3 -m tidy /tmp/rv4 --apply` on the branch head → exit 0 both times, each printing `leave  broken.pdf   [cannot be examined: No such file or directory]` and `move   photo.jpg -> recent/images/photo.jpg`; `find /tmp/rv4` → `recent/images/photo.jpg` present, `broken.pdf` still a link in place
  - `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` → exit 0, three hits: `ADR-0008:48`, `ADR-0009:23`, `ADR-0009:106`
  - `grep -n "" tidy/cli.py | sed -n '52,54p'` → `52:` blank, `53:def main(argv=None):`, `54:    args = build_parser().parse_args(argv)` — Finding 3
  - `git show b76b27c:tidy/cli.py | sed -n '52p'` → `    args = build_parser().parse_args(argv)`; `git show 46e5fd0:tidy/cli.py | sed -n '52p'` → blank — Finding 3's provenance, established by running
  - `grep -n "" tidy/cli.py | sed -n '70,76p'` → the banner guard is `if moves:` at 73, not at the cited 72
  - `git show main:tidy/planner.py | sed -n '47p;55p;85p;114p'` (re-run from round 1) → the four statements ADR-0009 v1 cited, confirming v2's historical claim
  - `sed -n '55,80p' tidy/cli.py`, `sed -n '64,78p' docs/architecture/overview.md`, `sed -n '100,112p' docs/architecture/adr/ADR-0009-…md` → the paragraphs the D12 rows turn on
  - `python3 .claude/agile-skills/scripts/new-item --next-id bug` → `BUG-0006`; `new-item --id BUG-0006 --type bug --status ready --actor review-close --arose-from BUG-0004 --found-in BUG-0003 …` → exit 0, "created BUG-0006 at status ready"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 as the transition ran it
  - `git merge --no-ff wi/BUG-0004` on `main`, after this transition — recorded under Artifacts
- **Gates:**
  - `definition-of-done` → **pass** — walked criterion by criterion in `review.md` `## Definition of Done` `### Round 2`, twelve rows with twelve results and twelve pieces of evidence. D1 through D12 all pass; D3 and D9 are evidenced on the merge result `54251e84`, not on the branch
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the movement since `ab644840` is ten files, all under `tracker/` or `docs/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 7 commits on `main..wi/BUG-0004`; run before the merge, while that range was still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** — `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests`, `OK`, run *inside* the detached trial worktree at `54251e84`, not on the branch; `compileall` exit 0 there too
  - `workspace-valid` → **pass** (exit 0 as the transition ran it)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone. *What was built and why:* one guard in `build_plan` so an entry the filesystem will not describe costs its own entry and nothing else — `item.md`, ADR-0009 v2, `README.md`. *Which skill decided what:* `verify` filed it and established `found-in` by running three trees; `plan` decided ADR-0009 and the three properties it fixed; `implement` wrote one `try` and three tests, proven to fail against the reverted planner; `verify` passed all four criteria on `ab644840`; `review-close` suspended it on two document findings; `answer-questions` corrected ADR-0006 and ADR-0009; `review-close` closed it. *What questions arose:* Q-001 and Q-002, both to the architect, both answered from the record with their consequences in the two ADRs. *What verification found:* four passes, six boundary conditions triggered, four declared gaps — `verify-report.md`
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0). Recorded again, because it is the gate Finding 3 slips past: it checks that a citation *resolves to a file*, not that the cited *line* supports the sentence
  - `epic-sign-off` → **skipped** — this execution closes a bug, not an epic. `engagement-state EP-001` was still run, after the close: **`active`**, "still in flight: BUG-0005, WI-0003" plus the newly filed BUG-0006, so the engagement is not at rest and no sign-off is due
- **Artifacts:**
  - `tracker/items/BUG-0004/artifacts/review.md` — round-2 sections added under all five headings, plus a preamble; round 1's text unchanged. Nine claims re-audited from their citations, twelve Definition of Done rows, three findings, seven accepted gaps
  - `tracker/items/BUG-0004/item.md` — `outcome: delivered`; `## Notes` gains two round-2 gaps and one corrected citation
  - `tracker/items/BUG-0006/` — **filed at `ready`**: ADR-0008 cites `tidy/cli.py:52`, a blank line. Four criteria, reproduction steps that run, `found-in: BUG-0003`, `arose-from: BUG-0004`, and a `## Notes` recording why a bug's regression-test criterion is absent (`spec/work-item.md` §3)
  - the merge of `wi/BUG-0004` into `main` — `cea3b907`, a `--no-ff` merge commit made after this transition, with `main` moving `73bb1f45` → `cea3b907`. The suite was re-run on the merged trunk: exit 0, `Ran 72 tests`, `OK`. (The sha was filled into this bullet after the merge, which is the only thing in this entry not true at the moment the entry was stamped; nothing else in it was changed.)
  - commit of this execution's tracker files, per `conventions.commit-subject`
- **Status:** `in-review` → `done`
- **Result:** BUG-0004 is delivered. A folder containing a dangling symlink is now tidied: the entry that cannot be examined gets a `leave` line in the operating system's own words, every other file moves as it would have, and the run exits 0 — where before this item the same folder produced a `FileNotFoundError` traceback, or after BUG-0001 the calm false sentence "cannot be read" and an empty stdout. Both of round 1's document findings are closed against corrected ADRs that were checked by opening the code rather than by reading the corrections; a third, in ADR-0008 and belonging to BUG-0003, is filed as BUG-0006 rather than carried. The trial merge was detached, the suite green on the merge result, `main` confirmed unmoved before the real merge, and the item closed while the branch was still unmerged.
