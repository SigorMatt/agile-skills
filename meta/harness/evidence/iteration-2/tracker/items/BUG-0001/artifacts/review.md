# Review — BUG-0001

## What I examined

**The record, in full.** `item.md` including all three criteria and their tick state;
`history.md`, five rows, chained `— → ready → planned → in-progress → verifying → in-review` with
the last row matching `item.md`; `journal.md`, all five entries read end to end, one per execution
the history implies; `plan.md` including `## Out of scope for this item`; `impl-report.md`
including `## Deviations from the plan` and `## What I did not do`; `verify-report.md` including
`## Not verified, and why`; `questions/` — empty, no question was ever filed on this item.

**The diff, hunk by hunk**, at `git diff main..wi/BUG-0001` — not the reports about it. Three code
hunks and the tracker record; the mapping is in `## The diff` below.

**The code the claims point at**, opened rather than remembered — see `## D12` below:
`tidy/cli.py` in full (`main()` and `render()`), `tidy/apply.py` in full, `tidy/planner.py`'s
`build_plan`, `docs/architecture/overview.md`, `docs/architecture/adr/ADR-0002` `## Decision`, and
`ADR-0006` `## Decision` and `## Change log`.

**The merge result**, not just the branch: a detached worktree at `.harness/trial`, `main` merged
with `--no-ff` to `25fab17`, the project's own test and lint commands run **inside it**, and the
fix itself exercised there against a folder I made unreadable.

**Two things I checked rather than accepted.** `check-verify-freshness` reports that the branch
moved past the verified commit; I confirmed independently with
`git diff --name-only d80c35a..09733b1` that every file in that range is under `tracker/`, so no
code postdates the verification. And `shutil.Error.__mro__`, because ADR-0006 asserts that
`apply_plan` lets nothing raise out of it and that rests on every failure being an `OSError` —
`shutil.Error` subclasses `OSError`, so it holds.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC"` → **3**; `grep -c "^- \[ \] AC"` → **0** |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | Its `## Criteria` table gives each of AC1-AC3 a command run in that execution and its quoted output: four runs over two self-built mode-000 fixtures for AC1; the five documented cases (0/0/2/2/2) for AC2; the located test plus six mutations for AC3. No row cites `impl-report.md` |
| D3 | the declared gates passed on the **final** state of the code | **pass** | `implement` ran its seven gates after `068cecd`, the last code commit. `verify` re-ran test and lint itself on `d80c35a`. I ran both again on the merge result `25fab17`: 64 tests `OK`, `compileall` exit 0. Three independent runs, the last of them on what the trunk actually gets |
| D4 | no open blocking question | **pass** | `tracker/items/BUG-0001/questions/` contains only `.gitkeep`; none was ever filed. Workspace-wide, `grep -l "^status: open"` over every question file returns nothing |
| D5 | a journal entry per execution; `history.md` chains to the current status | **pass** | Five history rows imply five executions (`verify` creating it, `plan`, `implement` opening, `implement` closing, `verify` closing); `journal.md` has exactly five entries with matching timestamps and personas. No gap in the chain; the last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | **ADR-0006** carries all five: exit 2 over a new code (option A), the CLI boundary over the planner and over an `os.access` pre-check (C over D and E), `OSError` rather than `PermissionError`, the OS's own reason in the message, and `README.md` rewritten as one rule. Cited from `plan.md` `## Decisions and ADRs` and from both `implement` journal entries. The one decision left to the developer — the message's exact wording — is plan assumption 2 and is journalled as such |
| D7 | documents the change invalidated have been updated, with a version bump and a change-log row | **pass, with nothing to bump** | The change invalidated one document: `README.md`'s exit-status paragraph, updated in `068cecd`. `README.md` has no doc header, so no version or change-log row applies to it. Nothing under `docs/` was invalidated — established by the D12 audit below, not assumed — so no bump was due. ADR-0006 stays at version 1: every claim it makes about the code came true |
| D8 | every commit references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, *"all 4 commit(s) on main..wi/BUG-0001 name BUG-0001"* |
| D9 | merged into the trunk | **pass** | Merged after this review and after the close, in that order. Trial first at `25fab17`, discarded; `git rev-parse main` was `e96c5e2` before the trial and `e96c5e2` after it |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0: verified at `d80c35a`, branch now `09733b1`, *"only the record changed (10 file(s) under tracker/ or docs/)"*. Confirmed independently: `git diff --name-only d80c35a..09733b1` filtered of `tracker/` and `docs/` is **empty** |
| D11 | `review.md` exists and states what was examined | **pass** | This file; `## What I examined` is first and names artifacts, code files, commands and shas |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, read against the code | **pass** | Seven claims opened and decided from their citations — the table below |

### D12 — the claims, and what I opened to decide each

Decided by reading the cited code, not the sentence and not a neighbouring document.

| claim | where | opened | verdict |
|-------|-------|--------|---------|
| "**Every destination is decided in `planner.py` and nowhere else**" `[src: ADR-0002; src: tidy/planner.py]` | `overview.md` | `tidy/cli.py` in full — the file this item changed | **true.** `main()` computes no destination; it reads `action.destination`. `render()` only formats. The new handler adds a message and a return code |
| `tidy/cli.py` — may write to disk: **no** | `overview.md` module table | `grep -n "open(\|os.makedirs\|os.link\|shutil\|write(" tidy/cli.py` | **true.** All six writes are `sys.stderr.write` or `sys.stdout.write`, including the line this item added. No file write of any kind |
| `tidy/cli.py` — "`argparse` setup, rendering an action list as lines, exit codes" | `overview.md` module table and diagram | `tidy/cli.py` | **true**, and this item strengthens it: the new exit path is squarely that responsibility |
| "`build_plan(folder) -> list[Action]` (reads; writes nothing)" and "It performs no writes of any kind" | `overview.md`; `ADR-0002` §1 | `tidy/planner.py`; `git diff --name-only main..wi/BUG-0001` | **true**, and untouched — the diff names only `README.md`, `tests/test_cli.py` and `tidy/cli.py` |
| "Preview is `build_plan` followed by rendering. Apply is `build_plan`, rendering, then `apply_plan` over the same list produced by the same call" | `ADR-0002` §3 | `tidy/cli.py` `main()` | **true.** One `build_plan` call, now inside a `try`; the same `actions` list is rendered and then handed to `apply_plan`. The wrapper introduces no second call |
| "`apply_plan` already lets nothing raise out of it, returning a message per action that did not complete" `[src: tidy/apply.py]` | `ADR-0006` `## Decision` | `tidy/apply.py` in full, plus `shutil.Error.__mro__` | **true.** Every filesystem call in the loop and in `_move_without_a_link` is inside `except OSError`; `os.path.join`/`dirname` are string operations and `os.path.lexists` returns `False` rather than raising. It rests on `OSError` covering everything raised there, which is why I checked `shutil.Error` — it subclasses `OSError` |
| "a run using the fallback exits 1 even when every file moved" `[src: BUG-0002]` | `overview.md` | `tidy/apply.py` `_move_without_a_link`; `tidy/cli.py`'s final `return 1 if failures else 0` | **still true**, and still BUG-0002's open subject. On success the fallback returns its note into the same `failures` list. This item did not touch either line |

`lint-claims --changed-since main` → exit 0, *"checked no documents changed since main"* — this
item changed no file under `docs/`, so the automated half of D12 had nothing to inspect and the
whole of it is the read above.

## The diff

`git diff main..wi/BUG-0001 -- ':!tracker/'` is three files. Every hunk traces to a criterion or a
plan step:

| hunk | serves | judgement |
|------|--------|-----------|
| `tidy/cli.py` — `try` / `except OSError` around the `build_plan` call, plus a four-line comment | AC1; plan step 1; ADR-0006 options A and C and details §1-2 | The `try` wraps exactly one call, so it cannot swallow a failure from rendering or from `apply_plan`. `error.strerror or error` handles the `OSError`s whose `strerror` is `None` rather than printing an empty reason after a colon. Contradicts no ADR: ADR-0002 puts presentation in `cli.py`, and this is presentation |
| `README.md` — the exit-status paragraph | AC2; plan step 3; ADR-0006 §3 | Rewritten as one rule rather than extended with a third case, which is what ADR-0006 specified. I exercised all five cases it now claims and got 0/0/2/2/2 |
| `tests/test_cli.py` — the new test in `BadTargetTests` | AC3; plan step 4 | Sits in the class that already owns the other two unusable-target cases and reuses their `run()` helper. `addCleanup` is registered before the mode is dropped, so the restoring `chmod` runs before `TemporaryDirectory.cleanup` — the ordering the plan called out, and it is correct |
| `tests/test_cli.py` — the module docstring gains "and BUG-0001 AC1 and AC3" | **not in the plan** | Declared as deviation 1 in `impl-report.md` rather than left for me to find. One line describing the contents of the file step 4 edits; leaving it would have made the file false about itself. Accepted |

Plan step 2 was a prohibition — do not touch the `--help` strings, which BUG-0003 owns — and it
was honoured: no change to `description` or `epilog`.

## Findings

**One, non-blocking.** The comment above the new handler opens "Listing the target is the last
thing that can make it unusable". That is not quite right. `entry.stat()` runs inside
`build_plan` too, and when *it* fails the handler reports that the **target folder** cannot be
read — which is false, and is the defect `verify` filed as BUG-0004. The code is correct for what
it was written for; the sentence describes a narrower `try` than the one that is there.

I did not send the item back for it. The substantive half is already an item, the fix for
BUG-0004 must rewrite this comment regardless, and a round trip to reword a comment whose
misconception is already tracked would cost two executions to buy nothing. It is gap 5 in
`item.md` `## Gaps accepted at review`, where BUG-0004's implementer will meet it.

**Nothing else.** No hunk is unaccounted for, no ADR is contradicted, no error path swallows an
error it should not — the `try` covers one call and the OS's own reason reaches the user, which is
what makes the broad clause auditable at the terminal rather than only in the ADR.

## Accepted gaps

Seven, all written into `item.md` `## Gaps accepted at review` so that they survive the close:
AC3's skip branch never actually run under root; the `OSError` clause exercised for `EACCES` and
`ENOENT` only; the TOCTOU race unexercised; the unstattable-entry defect (**BUG-0004**); the
handler comment's framing (fixed as part of BUG-0004); `--help` still wrong about age routing
(**BUG-0003**); and no distinct exit status for the unreadable case (ADR-0006 option B, additive
later).

Two of the seven already have items. The other five are recorded on the item itself, which is the
only place a reader of a closed bug will look.

## Record is reconstructible

Answered from `tracker/`, `docs/` and `git log --grep BUG-0001` alone:

- **What was built and why** — `plan.md` `## Problem` and `## Approach`, and `impl-report.md`
  `## What was built`. One `try`/`except` at the CLI boundary and one sentence in `README.md`,
  because a traceback is not a message and exit 1 contradicted the documented contract.
- **Which decisions, by which skill** — `plan` decided the five in ADR-0006 and recorded the two
  rejected options with what each would cost; `implement` decided the message's wording under
  plan assumption 2 and journalled it; `verify` decided the send-back-versus-bug classification
  and journalled the reasoning; this review decided the seven gaps.
- **What questions arose and how they were resolved** — none were filed on this item, which the
  empty `questions/` directory and the absence of any `awaiting-answer` row both state.
- **What verification found** — `verify-report.md`: three passes with quoted output, eleven
  boundary conditions, six mutations, and one defect that became BUG-0004.

## Verdict

**Accept.** All twelve Definition of Done criteria pass, each with its own evidence. The change
is small, sits where ADR-0002 says presentation belongs, is exactly what ADR-0006 specified, and
does what BUG-0001 asked for — checked at the terminal on the merge result, not only on the
branch. Merged into `main` after the close, as merge commit **`fe10f31`**; the item is `done` with
`outcome: delivered`. 64 tests pass on the trunk after the real merge, matching the trial.
