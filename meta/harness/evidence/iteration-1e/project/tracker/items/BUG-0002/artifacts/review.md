# Review — BUG-0002

## What I examined

- `tracker/items/BUG-0002/item.md` — the summary, the four reproduction steps, AC1–AC5 and their
  tick state, and the four notes the filing review left, including the `mkdir` question the plan
  was told to settle.
- `tracker/items/BUG-0002/history.md` — five rows, read as a chain: `— → ready → planned →
  in-progress → verifying → in-review`. Every `from` equals the previous `to`, the first is `—`,
  and the last row's `to` matched `item.md` when this review began.
- `tracker/items/BUG-0002/journal.md` — **read in full**, all five entries (`review-close` filing
  it at 00:17:21Z, `plan` at 01:51:54Z, `implement` twice at 01:52:45Z and 01:56:45Z, `verify` at
  02:00:08Z). Five entries, five history rows, one-to-one by timestamp and actor.
- `tracker/items/BUG-0002/questions/` — `.gitkeep` only. Nothing was ever asked on this item, by
  any skill, so there is nothing to be open.
- `tracker/items/BUG-0002/artifacts/plan.md` (the nine steps, the five-row mapping table, the
  three assumptions, the decision table, the four risks, the four things out of scope),
  `impl-report.md` (including `## Deviations from the plan` and `## What I did not do`) and
  `verify-report.md` (including `## Defects found` and `## Not verified, and why`).
- **The diff, hunk by hunk, not the reports about it**: `git diff main..wi/BUG-0002` read in full
  for `expenses/`, `tests/` and `docs/` — three files, and every hunk mapped to a plan step in F4
  below.
- `expenses/store.py` in its entirety on the branch head, `expenses/cli.py`'s `main` and its
  imports, `tests/test_cli.py`'s `CommandTestCase` and all eleven `setUp` methods,
  `docs/architecture/overview.md` v7, `docs/architecture/adr/ADR-0008-…md`, `ADR-0001-…md`,
  `docs/product/vision.md`, `README.md`'s `## When something is wrong`, `tracker/project.yaml`.
- `tracker/items/WI-0004/artifacts/review.md` — for finding F4 of that review, which fixes how a
  trial merge is done in this project.
- A **detached** trial merge (`git worktree add --detach /tmp/trial-bug2 main`) with the suite run
  on the merge result, and the bug's own reproduction re-run by hand against that code.

### The D12 claim audit — what I opened for each claim

Each row is a claim in `docs/` about behaviour this item touched. The verdict comes from opening
the thing the claim cites and reading it — not from the sentence, not from a neighbouring
document, and not from `impl-report.md` or `verify-report.md`.

| claim | cited | what I opened | verdict |
|-------|-------|---------------|---------|
| `overview.md` v7: "Both of the functions that touch the file turn an operating-system error into a refusal" | ADR-0008; `expenses/store.py` | `grep -n "^def " expenses/store.py` → eleven functions; of them only `load` (line 37) and `save` (line 61) touch the file — `store_path` reads environment variables and `Path.home()` and opens nothing. `load` has `except OSError as err` at :43, `save` at :87 | **true** |
| `overview.md` v7: "`load` says `cannot read <path>: <error>`, `save` says `cannot write <path>: <error>`" | ADR-0008; `expenses/store.py` | `store.py:44` → `"cannot read %s: %s" % (path, err)`; `store.py:88` → `"cannot write %s: %s" % (path, err)`. Both format the `path` argument, not the temporary file | **true** |
| `overview.md` v7: "nothing above this module ever sees an `OSError`" | ADR-0008; `expenses/store.py` | both `except OSError` clauses above, plus `expenses/cli.py:186-191` — `main` catches `ExpensesError` and nothing else, so an escaping `OSError` would be a traceback and is what BUG-0002 was. Re-run by hand on the merge result: exit 2, `Traceback count: 0` | **true** |
| `overview.md` v7: "the temporary file it writes is removed before the error is translated" | `expenses/store.py`; BUG-0002 AC3 | `store.py:79-86` — the `except BaseException` that unlinks `handle.name` is **nested inside** the new outer `try`, and re-raises; the outer `except OSError` at :87 is therefore reached after the unlink. Checked by hand: `ls -a` on the refused directory → `.`, `..`, `expenses.json` only | **true** |
| `overview.md` v7: "a write the operating system refuses changes neither the dataset nor the directory it lives in" | `expenses/store.py`; BUG-0002 AC3 | `os.replace` is the last statement and is never reached on a refusal; `md5sum` either side of a refusal on the merge result → `c21ac18dc401812361a7da5baec700af` both times, 66 bytes | **true, with one edge — see F3** |
| `overview.md` v7: "The whole of `save` is inside that boundary, the parent-directory creation included" | `expenses/store.py` | `store.py:67-88` — `target.parent.mkdir` (:69) is the first statement inside the `try` (:68). One statement, `target = pathlib.Path(path)` (:67), is outside it | **true of the substance — see F2** |
| `overview.md` (`expenses/cli.py` piece, written for WI-0001): "every refusal writes to stderr, changes nothing on disk and exits non-zero" | `WI-0001/artifacts/refinement-qa.md` | `cli.py:186-191` (`print(str(refusal), file=err)` at :189, `return REFUSED` at :190, `REFUSED = 2` at :15) and, for the write path this item changed, the hand-run refusal above: stderr 1 line, stdout 0 bytes, exit 2, dataset unchanged. **This is the claim BUG-0002 contradicted**, and it is the one that has become true | **true — now** |
| `overview.md` (same piece): "Refusals are raised as a single exception type from the layers below and turned into a message and an exit code in exactly one place" | `expenses/cli.py` | `grep -n "except" expenses/cli.py` → two hits: `:188`, the only place a refusal becomes a message and an exit code, and `:82`, a `ValueError` inside `parse_date` that is immediately re-raised as an `ExpensesError` rather than printed. `store.py` raises `ExpensesError` and nothing else | **true** |
| ADR-0008 Decision §1: "The whole of `save` is inside the boundary, including `target.parent.mkdir`" | `expenses/store.py`; BUG-0002 | `store.py:69`, inside the `try`. Triggered by hand at plan time and again by `verify` against a mode-500 parent → `cannot write …/sub/expenses.json: [Errno 13] Permission denied: '…/sub'`, exit 2 | **true** |
| ADR-0008 Decision §3: "Cleanup keeps precedence over translation" | BUG-0002 AC3 | the nesting at `store.py:79-88`, as above | **true** |
| ADR-0008: "`ExpensesError` is not a subclass of `OSError`, so a refusal raised inside the wrapped region … passes through untouched" | `expenses/money.py` | `expenses/money.py:12` → `class ExpensesError(Exception)`. And by construction: `person add Ana` on a dataset already holding Ana → `Ana is already in the group`, not `cannot write …` | **true** |
| ADR-0001 (unchanged, but this item rewrote the code it describes): "Its parent directory is created on the first write. A write is done by writing a sibling temporary file and `os.replace`-ing it over the target" | `WI-0001 AC9` and the store code | `store.py:69-78` — `mkdir(parents=True, exist_ok=True)`, `NamedTemporaryFile(dir=str(target.parent), prefix=".expenses-")`, `os.replace`. The refactor moved these lines into a `try`; it changed none of them | **still true** |
| `README.md` `## When something is wrong`: "A command that cannot do what you asked writes a message to standard error and leaves your data exactly as it was … The exit status of a refusal is 2" | WI-0001 AC5/AC6; WI-0001 plan | `README.md:155-166`, then the hand-run refusal on the merge result. Untouched by this item and made **more** true by it, which is why `impl-report.md` is right that nothing had to change | **true** |
| `docs/product/vision.md` | — | `grep -i "error\|refus\|stderr\|traceback\|exit"` → one hit, in an unrelated sentence about what the stakeholder refused to drop. Nothing in it speaks to this behaviour | **not touched** |

Fourteen rows; every claim about this behaviour is true against the code it cites. Two carry a
precision note rather than a defect — F2 and F3 below.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox ticked | **pass** | `grep -c "^- \[x\] AC" tracker/items/BUG-0002/item.md` → 5; `grep -c "^- \[ \] AC"` → 0 |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | its Criteria table gives, for each of AC1–AC5, a command `verify` ran and its actual output: for AC1 four clauses measured separately (`wc -c < out`, `wc -l < err`, `grep -c -F <path>`, `grep -c Traceback`) against two fixtures, one of them the bug's literal reproduction; for AC3 `md5sum` and `wc -c` bracketing two refusals plus a directory listing; for AC4 three separate checks including a revert-and-rerun and a forced-skip injection; for AC5 the suite's own summary line. No row cites `impl-report.md`, which that skill records as having opened last |
| D3 | All declared gates passed on the **final** state of the code | **pass** | the last commit touching `expenses/`, `tests/`, `docs/` or `README.md` is `f23bfda`; `git diff --stat f23bfda..a332c73 -- expenses/ tests/ README.md docs/` is **empty**, so `d8b4c4e` and `a332c73` are record-only. `implement` ran the suite on `f23bfda` (123 tests), `verify` re-ran it on `d8b4c4e` (123 tests), and this review ran it on the trial-merge result (123 tests, `OK`). `lint-clean` is recorded as **skipped** citing ADR-0004 by every skill at every stage, never as a pass |
| D4 | No open blocking question on the item | **pass** | `tracker/items/BUG-0002/questions/` holds `.gitkeep` and nothing else; no question was filed on this item by any skill. `validate-workspace` reports 0 open questions workspace-wide |
| D5 | A journal entry per execution; `history.md` chains without a gap | **pass** | five rows, `— → ready → planned → in-progress → verifying → in-review`, each `from` matching the previous `to` and the last matching `item.md`. Five journal entries, matching the rows one-to-one by timestamp and actor; no extra entries and none missing |
| D6 | Every design decision is in an ADR cited from the plan or journal | **pass** | **ADR-0008** (`status: current`, version 1), cited by name from `plan.md`'s `## Decisions and ADRs` for three decisions — the boundary itself, the `mkdir` clause (§1) and cleanup-before-translation (§3) — and from `plan`'s journal entry with route `[documented → decided]`. Its four options (store boundary / CLI / per-handler / leave it) are real alternatives with costs, not a rationalisation of one. The three remaining choices are `[assumed, reversible]` in `## Assumptions` with what reversal costs, and the seventh points at ADR-0004. No ADR was amended or superseded, which is right: this item decided something nothing had decided before |
| D7 | Documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` is `version: 7`, `updated-by: implement`, `updated-for: BUG-0002`, with change-log row 7. The v6 paragraph under `## What is coming` — written by `plan` in the future tense — is **gone**, and its content is now in the `expenses/store.py` piece describing code that exists; `## What is coming` holds WI-0003 alone, as the row claims. `README.md` and `docs/product/vision.md` needed no change, checked in the audit above rather than assumed |
| D8 | Every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0002 wi/BUG-0002` → exit 0, `all 4 commit(s) on main..wi/BUG-0002 name BUG-0002` |
| D9 | Merged into the trunk | **pass** | trial-merged first into a **detached** worktree (`git worktree add --detach /tmp/trial-bug2 main`), which left `git rev-parse --short main` at `37e57f0` before and after; merge clean, 9 files changed, 432 insertions; `python3 -m unittest discover -s tests -t .` on the merge result → `Ran 123 tests in 1.521s`, `OK`, exit 0. The trial worktree was then removed, the item closed while the branch was still unmerged, and only then was `wi/BUG-0002` merged into `main` for real |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0002 wi/BUG-0002` → exit 0: `verified at d8b4c4e8; wi/BUG-0002 has moved to a332c738 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code`. Compared by the script, and independently by the empty `git diff --stat` in D3 |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is first and names the artifacts, the diff ranges, the fourteen claims audited and what was opened for each |
| D12 | Claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **pass** | the fourteen-row audit above, every verdict reached by opening the citation. `lint-claims --changed-since main` → exit 0, `checked 1 document(s)`, `0 errors, 0 warnings` — the half a program can check; the audit is the half it cannot. Two rows carry precision notes (F2, F3); neither is a false statement about behaviour |

Twelve of twelve pass.

## Findings

**F1 — `verify`'s one non-blocking finding does not survive being checked, and it is worth saying
why.** `verify` recorded that `tests/test_cli.py`'s module docstring — "each test starts from a
store that does not exist yet" — was *made* inaccurate by this diff, because
`BUG0002AnUnwritableStoreIsRefusedNotATraceback.setUp` records `Zoe` before taking the write
permission away. It handed the decision to this review, correctly. Checking it rather than
accepting it: `grep -n "def setUp" -A 14 tests/test_cli.py` shows **seven** pre-existing classes
whose own `setUp` already records people and expenses through `self.succeed(...)` — at lines 166,
185, 214, 352, 468, 499 and 555 — and `CommandTestCase.run_command` calls `main()` in process,
which calls `store.save`, which writes the file. So under the strict reading ("the test method
begins with no file on disk") the sentence has been inaccurate since WI-0001 and WI-0002, for
roughly twenty tests, and this diff added three more; under the reading that makes it true of
those seven ("each test's fixture begins from a store that does not exist yet — no test inherits
another's data") it is true of the new class as well, whose `setUp` also starts from nothing.
Either way it is **not a defect this change introduced**, so it is not a send-back — and it is
not a bug against another item either, since the sentence is a matter of reading rather than a
statement about delivered behaviour. Recorded in `item.md`'s `## Notes` so the next reader meets
the resolution rather than re-deriving it. **This is the one finding I was handed on trust, and
it is the one that turned out to be wrong when opened** — which is exactly the reason D12 says to
read the source rather than the sentence.

**F2 — "The whole of `save` is inside that boundary" overstates by one statement.** Non-blocking;
recorded, not to be acted on here. `expenses/store.py:67` is `target = pathlib.Path(path)`, which
sits above the `try` opened at :68. `pathlib.Path()` performs no file-system access and can raise only
`TypeError` on a non-path argument, so **no `OSError` can arise there** and no behavioural claim
in `docs/` is false. The module's own docstring for `save` puts it exactly — "Everything the file
system can refuse is inside the try" — and ADR-0008 §1 is scoped to `target.parent.mkdir`, which
is inside. The overview's sentence is the loose one of the three. Not worth a round trip for one
word; recorded so nobody re-derives it.

**F3 — one refusal edge the "changes nothing on disk" sentence does not cover.** Non-blocking.
`target.parent.mkdir(parents=True, exist_ok=True)` is inside the boundary, which is what
BUG-0002's notes asked for — but it *creates* directories. If the `mkdir` succeeds and the write
that follows is then refused, the refusal leaves behind directories that did not exist before,
and the overview's "changes neither the dataset nor the directory it lives in" is, strictly, not
true of that case. It is not reproducible with permission bits — a directory you may create
subdirectories in is a directory you may create files in — so it needs a full disk, a quota or a
read-only remount between two adjacent statements, and no criterion covers it. The dataset itself
is safe in every case, because `os.replace` is the last statement and is never reached. Recorded
in `item.md`'s `## Notes`; not filed as a bug, because nothing observable in this environment
distinguishes it from the passing case.

**F4 — every hunk maps to a plan step; no unrequested scope, and no ADR contradicted.** Read hunk
by hunk. `expenses/store.py`: the module-docstring paragraph → step 2; the `save` docstring and
the re-indentation of its body inside the new `try`/`except OSError` → step 1. The diff moves the
`mkdir`, the `NamedTemporaryFile` and the inner `except BaseException` cleanup **without changing
what any of them does** — the only additions are the outer `try`, the outer `except`, and a
comment saying why the cleanup is nested. `tests/test_cli.py`: the module-docstring sentence
naming the new class, and `BUG0002AnUnwritableStoreIsRefusedNotATraceback` with its fixture,
process helper and three tests → steps 3–6. `docs/architecture/overview.md` → step 9. Nothing
else is in the diff outside `tracker/`. Against ADR-0008's three checkable clauses: §1 satisfied
(`mkdir` inside), §2 satisfied (`cannot write %s: %s` with the caller's path), §3 satisfied
(cleanup nested and re-raising). ADR-0001's atomic-write description is untouched. No ADR is
contradicted, so nothing needed superseding and nothing was.

**F5 — the code is one I would be comfortable maintaining, and here is what I checked rather than
felt.** The outer `except` catches `OSError`, not `PermissionError`, so a full disk and a
read-only mount reach it by the exception hierarchy rather than by anyone remembering to add a
clause. `handle` cannot be unbound where it is used: the inner `try` opens *after* the assignment,
so a `NamedTemporaryFile` that raises goes straight to the outer handler. A non-`OSError` failure
in `json.dump` — a value the encoder refuses, say — still runs the cleanup and still propagates as
itself, so a real programming error keeps its traceback, which is the cost ADR-0008 names and
bounds. The one comment added explains why the cleanup is nested, which is the thing a future
reader would otherwise flatten. The test is a real subprocess, so "exit 2" and "no `Traceback`"
are observed the way a person at a terminal sees them, and it fails loudly rather than silently
when the handling is removed — `verify` demonstrated both directions and restored the tree with
`md5sum -c` each time. The cleanup-registration order in the fixture, the thing the plan warned
was easy to get backwards, is right and carries a comment saying why.

## Accepted gaps

Seven, all written into `item.md`'s `## Notes` — which is the point of accepting them rather than
leaving them in a report nobody opens after an item is `done`:

1. `lint-clean` checked nothing on this project (ADR-0004, project-wide, every item).
2. Only the permission case was triggered. A full disk, a read-only mount and a name too long for
   the file system reach the same `except OSError` by the exception hierarchy; none was produced,
   because there is no way to create them here that would cost less than it proves.
3. The AC4 skip path was demonstrated by injection — making the directory writable — not by
   running the suite as a user for whom mode 500 is not binding.
4. `os.replace` failing *after* a successful write has no test. The cleanup it would run is the
   one AC3 exercises through the `NamedTemporaryFile` failure, but that specific ordering was
   never produced.
5. `person delete` and `expense delete` against an unwritable store are fixed by the same wrapper
   and are tested by nobody. The plan records this as assumption 3.
6. F2's one-word overstatement in `overview.md` v7.
7. F3's `mkdir`-then-refuse edge.

None justified a send-back: each is a limit on what was checked, or a consequence of a decision
already recorded, and none is a statement in the record that is untrue.

## Verdict

**Accepted — merged and closed, `outcome: delivered`.** Twelve of twelve Definition of Done
criteria pass. The change is one wrapper and three subprocess tests: `store.save` now turns an
`OSError` into the same kind of refusal `store.load` has always raised, with the temporary-file
cleanup still running first, so a store the operating system will not let this tool write
produces one line on stderr, nothing on stdout and exit 2, and leaves the previous dataset
byte-identical — re-run by hand on the merge result rather than taken from a report. The diff maps
hunk-for-hunk onto the plan's nine steps with two declared deviations, both improvements and both
explained; no ADR is contradicted; the trial merge was detached, clean, and green at 123 tests.
The one finding handed up by `verify` was opened and did not hold, which is recorded in F1 rather
than quietly dropped.
