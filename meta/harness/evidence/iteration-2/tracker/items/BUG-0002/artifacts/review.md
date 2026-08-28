# Review — BUG-0002

Reviewed at `in-review`, on `wi/BUG-0002` at `d0a7ebd`, against `main` at `a0fe21e`.

Two executions. The first, at `52d588e`, found the code sound and the Definition of Done failing
on D12 — two sentences in `docs/` that this branch makes false — and suspended the item to
`awaiting-answer` with Q-001 and Q-002 to the architect. `answer-questions` edited both documents
and returned the item here. This file is the whole review, first pass and second; the parts that
are unchanged are unchanged because they were checked again and still hold.

## What I examined

**The record.**

- `history.md` — seven rows, chaining without a gap: `— → ready` (verify), `ready → planned`
  (plan), `planned → in-progress` and `in-progress → verifying` (implement), `verifying →
  in-review` (verify), `in-review → awaiting-answer` (review-close, `resume-to: in-review`),
  `awaiting-answer → in-review` (answer-questions). The last row matches `item.md`.
- `journal.md` — seven entries, one per row, read in full. No execution is missing an entry and
  no entry claims a move the history does not carry.
- `questions/Q-001.md`, `Q-002.md` — both `status: answered`, `answered-by: answer-questions`,
  `answered-at: 2026-08-27T20:11:11Z`. Both `## Consequences` name files; I opened each and
  confirmed the change is there rather than reading the answer (below, D12).
- `item.md` — AC1–AC4 all ticked, each cited in `verify-report.md`; `## Notes` carries
  `### Gaps accepted at review`, the five gaps this review accepted.

**The change.** `git diff main..wi/BUG-0002`, hunk by hunk — four code files, two documents, and
the tracker:

- `tidy/apply.py` — the `Outcome` frozen dataclass and the docstring naming both `kind` values
  (plan step 1); `failures` → `outcomes` and the three `Outcome("failed", …)` wrappings (step 2);
  `_move_without_a_link`'s three tagged returns (step 3).
- `tidy/cli.py` — the print loop over `outcome.message` and
  `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`, with the ADR-0007
  comment (step 4).
- `tests/test_apply.py` — two existing assertions upgraded to `.kind` / `.message` (step 5), and
  `HardLinkFallbackTests` with two tests (step 6).
- `tests/test_cli.py` — `FallbackExitStatusTests` with two tests, and the module docstring
  (step 7).
- `docs/architecture/overview.md` v4 → v5 and
  `docs/architecture/adr/ADR-0007-tagged-outcomes-from-apply-plan.md` v1 → v2 — the two
  propagations, added by `answer-questions` after the first pass.

Every code hunk maps to a plan step; no hunk serves neither a criterion nor a step. The four
message strings were checked against their `main` versions in the diff: each moved inside an
`Outcome(...)` call and re-wrapped, with no character of the text changed, which is what AC2 rests
on. The two document hunks are exactly what Q-001 and Q-002 recorded as their consequences, and
nothing else in either file changed.

**The claims, from their citations (D12).** Each opened rather than remembered, and the two the
first pass rejected re-checked against the code rather than against the answer that claims to have
fixed them:

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| never-overwrite is kernel-enforced via `os.link` on the primary path | `overview.md` ¶2 | `tidy/apply.py` — `os.link` then `except FileExistsError` | true |
| the fallback is `lexists` then `shutil.move`, holding the promise by check-then-act with a race window | `overview.md` ¶3 | `tidy/apply.py` `_move_without_a_link` | true |
| "No test reached that path until BUG-0002 … It is reached now — `tests/test_apply.py` and `tests/test_cli.py` each enter it by patching `tidy.apply.os.link`" | `overview.md` ¶3, **v5** | `git grep -n "os.link" main -- tests/` → no output, so no test on the trunk reaches it; `tests/test_apply.py:120,144` and `tests/test_cli.py:413,447` on the branch; `python3 -m unittest …FallbackExitStatusTests …HardLinkFallbackTests -v` on the merge result → 4 `ok`, none skipped | **true** — finding 1 resolved |
| `apply_plan` returns an `Outcome` per action not completed by the primary path; only `"failed"` exits non-zero; both wordings unchanged | `overview.md` ¶4 | `tidy/apply.py`, `tidy/cli.py`, the message diff | true |
| "BUG-0002 **carried** that change into the code, together with the first regression tests" | `overview.md` ¶4, **v5** | the same; the tense fix `answer-questions` made beyond what Q-001 asked | true |
| `apply_plan` already creates the destination's parent with `os.makedirs` | `overview.md` §"Modules" prose | `tidy/apply.py` | true |
| `kind` is one of exactly two strings | ADR-0007 `## Decision` | `tidy/apply.py` — `"failed"` ×4, `"fell-back"` ×1, no other | true |
| "The only caller in the package is `cli.py`; `tests/test_apply.py` imports `apply_plan` as well and reads the type" | ADR-0007 `## Consequences`, **v2** | `grep -rn "from tidy.apply import\|from .apply import" --include=*.py .` → `tidy/cli.py:12`, `tests/test_apply.py:16`; the four `.kind` / `.message` assertions in that module | **true** — finding 2 resolved |
| "There is one caller in the package — `cli.py` … and `tests/test_apply.py` calls it directly as well" | ADR-0007 `## Consequences`, **v2** | the same. This second occurrence was **not** in Q-002's quotation; `answer-questions` found and corrected it | **true** |
| ADR-0006's parenthetical describing the old `list[str]` return | ADR-0006 | ADR-0007 `## Consequences`, `spec/doc-header.md` §4 | historical by design, left as written |
| "Exit status is 0 on success … and 1 when some file could not be moved while others were" | `README.md` | the all-fail run, reproduced in the first pass | incomplete — finding 3, filed as BUG-0005 |

**Commands this execution ran**, on the second trial merge result `88fb911` unless stated:

- `git worktree add --detach .harness/trial2 main`; `git -C .harness/trial2 merge --no-ff wi/BUG-0002` → clean, `88fb911`
- `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 68 tests in 0.062s`, `OK`
- `python3 -m compileall -q tidy tests` → exit 0
- `validate-workspace .` → 9 items, 9 documents, 0 errors 0 warnings; `lint-claims --changed-since a0fe21e` → 2 documents, 0 errors — both run **inside** the merge result, so the documents were judged as the trunk will hold them
- `git worktree remove --force .harness/trial2`; `git rev-parse main` → `a0fe21e`, identical to the sha recorded before the trial
- `check-verify-freshness BUG-0002 wi/BUG-0002` → exit 0: verified at `6a5b1a7`, branch at `d0a7ebd`, 15 files between them all under `tracker/` or `docs/`
- `check-commit-refs BUG-0002 wi/BUG-0002` → exit 0, all 5 commits
- `git grep -n "os.link" main -- tests/` → no output — the evidence behind the first D12 row above
- `grep -rn "from tidy.apply import\|from .apply import" --include=*.py .` → two hits
- `engagement-state EP-001` → `active`; still in flight: BUG-0002, BUG-0003, BUG-0004, BUG-0005, WI-0003

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `item.md` AC1–AC4 all `[x]`; `validate-workspace` clean |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | `## Criteria` has seven rows over four criteria, each with a command and its output; two of them (AC1 primary route, AC3 unpatched end-to-end) appear nowhere in `impl-report.md`, so verification was independent rather than a re-reading of the implementation |
| D3 | the item's gates passed on the final state of the code | **pass** | the suite, the lint, `validate-workspace` and `lint-claims` re-run by this execution inside the merge result `88fb911` — not on the branch head, and not on the first pass's `71eb7d4`, which predates the document edits |
| D4 | no open blocking question remains | **pass** | Q-001 and Q-002 both `answered`, with `answered-at`, `answered-by`, and `## Consequences` naming files that carry their changes. No other question exists on this item |
| D5 | a journal entry per execution; history chains | **pass** | seven rows, seven entries, matched one by one |
| D6 | every design-changing decision is in an ADR, cited from plan or journal | **pass** | ADR-0007 is the only design decision; cited in `plan.md` `## Decisions and ADRs`, in the `plan` and `implement` journal entries, and in comments in both `apply.py` and `cli.py`. Its v2 edit changed no decision — the change-log row says so and the diff confirms it |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `overview.md` v5 and ADR-0007 v2, each with a row naming what changed and why, `updated-by: answer-questions`, `updated-for: BUG-0002`. This was **partial** on the first pass: v4 bumped the document without updating the sentence the change invalidated |
| D8 | every commit on the branch references the item | **pass** | `check-commit-refs` → exit 0, all 5 commits name BUG-0002 |
| D9 | merged into the trunk | **pass** | merged into `main` immediately after this close, in the order SKILL.md step 8 mandates — the close must precede the merge, because `commits-reference-the-item` inspects `main..wi/BUG-0002` and merging empties that range. The merge commit is named in `## Verdict` |
| D10 | verification ran after the last code change | **pass** | `check-verify-freshness` → exit 0: verified at `6a5b1a7`, branch at `d0a7ebd`, and all 15 files between them are under `tracker/` or `docs/`. No code file changed after verification |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` precedes the verdict and names the commands, the hunks and the claims |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | the audit table above, eleven claims, each decided by opening what it cites. The two that failed the first pass were re-checked against the code and the tests — `git grep` on `main`, the four patch sites on the branch, the four tests run green on the merge result, and the two-hit import grep — not against the answers that claim to have fixed them. `lint-claims` passes inside the merge result, which it also did when both claims were false |

## Findings

1. **`docs/architecture/overview.md` ¶3 became false on merge** — "That path is unreachable from
   the test suite … a run using the fallback exits 1 even when every file moved", against four
   tests that reach it and a run that exits 0. Raised as Q-001, answered from
   `spec/doc-header.md` §1–§3, propagated into `overview.md` v5. **Resolved**, re-checked here
   against the code.
2. **ADR-0007's `## Consequences` stated something false about the code** — "`apply_plan` is
   imported only by `cli.py`", against `tests/test_apply.py:16`, which imported it on `main`
   already. Raised as Q-002, answered from `spec/doc-header.md` §3 and §4 — the prohibition on
   editing an ADR is on changing its *decision* — propagated into ADR-0007 v2, in both places the
   claim appeared rather than only the one that was quoted. **Resolved**, re-checked here.
3. **`README.md` does not say what an all-fail run exits with.** Its exit-status enumeration gives
   1 only for "some file could not be moved while others were", and a run where *no* file moved
   also exits 1 — reproduced in the first pass. Prose BUG-0002 did not change and no criterion
   covers, so it belongs to another item: **filed as BUG-0005** at `ready`, `found-in: WI-0001`.
   `verify` examined the same sentence and recorded the opposite judgement; both views are in
   BUG-0005 `## Notes`.
4. **No finding against the code or the tests, on either pass.** The diff does what the plan says,
   the layering ADR-0002 sets is untouched, no message string moved, and the one behavioural line
   is the exit rule. The two things I would otherwise have raised are declared and bounded: the
   `0o500` test skips under root (guarded, and it did not skip in implementation, verification or
   either review pass), and the module-level `NO_HARD_LINKS` `OSError` instance is shared across
   tests — `apply.py` only `%s`-formats it, so nothing observable depends on the reused
   `__traceback__`.
5. **A toolkit defect, recorded for the owner rather than against this item.**
   `check-commit-refs` told `implement` at step 3 that `wi/BUG-0002` "is already merged into
   `main`" when the branch had just been created with zero commits, and advised rewinding a merge
   that did not exist. An empty `main..branch` range is not evidence of a merge when the branch
   head equals the trunk head. It blocked nothing and the gate has been correct on every run
   since; it is in `impl-report.md` `## What I did not do` and in this turn's harness status.

## Accepted gaps

Each is recorded in `item.md` `## Notes` under `### Gaps accepted at review`, so it survives the
item closing.

- **No test runs on a filesystem that genuinely refuses hard links.** All four patch `os.link` to
  raise errno 18. Accepted: the branch's behaviour given that error is what the item asks for, no
  such volume is available here, and the item's own reproduction steps take the same approach and
  name the same limitation. `overview.md` v5 now says this in the document too.
- **The `0o500` end-to-end leg of AC3 skips under root or on a filesystem ignoring the mode.**
  Accepted: it did not skip in any execution, three unit-level `kind == "failed"` assertions carry
  AC3 independently, and the guard matches what `BadTargetTests` already does.
- **The `os.unlink` duplicate path is untested** — link succeeded, unlink failed. Accepted: it was
  equally untested before this item, no criterion covers it, and it is tagged `"failed"` so it
  exits non-zero. Recorded because it is the one `Outcome("failed", …)` in `apply.py` that no test
  constructs.
- **A genuine mid-run `FileExistsError` was not driven through `main()`.** Accepted: `build_plan`
  reserves colliding names, so it cannot be produced through the CLI; it was exercised one layer
  down with a real kernel error, and the CLI's `"failed"` → exit 1 mapping separately.
- **`README.md` untouched by the change.** Accepted as a plan assumption, and now separately
  tracked: what is incomplete in it is BUG-0005, not this item.

## Verdict

**Accept.** All twelve Definition of Done criteria pass, each with its own evidence. The change is
four files and one behavioural line, it sits where ADR-0002 says execution and presentation
belong, it implements ADR-0007 exactly, and it does what BUG-0002 asked: a run that used
ADR-0003's fallback for every file exits 0 with its stderr byte-identical to what the unfixed code
printed, while a genuine failure — including one in the same run as a fallback — still exits 1. It
brings with it the first tests in this project that reach the fallback branch at all.

The item was suspended once rather than sent back, because the two defects were in documents
neither `review-close` nor `implement` may edit; both are now fixed at their source and re-checked
here against the code rather than against the answers.

Merged into `main` after the close, as merge commit **`2c85fa3`**; the item is `done` with
`outcome: delivered`. 68 tests pass on the trunk after the real merge, matching the trial, and
`validate-workspace` reports 9 items, 9 documents, 0 errors and 0 warnings there.
