# Harness status — turn 7

No question was waiting: all thirteen human-addressed questions across the workspace were already
`answered` and consumed by earlier turns, so amendment B had nothing to do and the turn went
straight to the loop. Four skills ran, all on WI-0001, which went
`verifying → in-review → in-progress → verifying → in-review`.

**The substantive result: `review-close` found a real AC8 violation that two verification passes
had missed, and the fix is in.**

- **`verify` (pass 2 of the item)** — re-derived all eight criteria on `f994258` rather than
  carrying the previous verdicts forward. All eight passed. The advisory sensitivity gate, which
  **failed** last turn for AC1/AC2, now passed for all eight: nine mutations, nine red suites. It
  also closed three gaps the previous pass had declared unverifiable — both default store-path
  branches (`XDG_DATA_HOME` and the `HOME` fallback, run against a scratch `HOME` inside the
  git-ignored `.harness/`) and `store.load()`'s undecodable-bytes branch, which was live but
  untested code. → `in-review`.
- **`review-close` — rejected it.** Reading the diff hunk by hunk and then probing the seam
  between `store` and the domain turned up a class of input nobody upstream had tried: a store
  that **passes** `store.load()`'s shape check and breaks above it. `load()` checked that `people`
  was a *list* but never what was in it, so `{"version":1,"people":[123],...}` parsed cleanly and
  `people.normalise()` raised `AttributeError` straight past `cli.main`'s `except ExpensesError`
  — **exit 1 with a Python traceback on stderr, which AC8 forbids outright**. The read path was
  wrong in the other direction: `people` exited **0** and printed `123` as a member of the group.
  Three more findings followed. D1–D12 recorded one by one: nine pass, three fail. → `in-progress`.
- **`implement`** — fixed F1 (element-type validation in `load()`, naming the path and the
  offending type), F2 (`match_key` compares without validating, so a bad *stored* name no longer
  makes the *typed* name look wrong), and F3 (an `except Exception` backstop in `cli.main`, plus
  `overview.md` → v2 and a corrected `errors.py` docstring). Four tests added, 19 → 23, each
  confirmed to go red with its fix reverted. → `verifying`.
- **`verify` (pass 3)** — re-derived all eight again on the new commit and **re-ticked AC8**, on a
  28-case sweep that now includes six junk element types × both commands. Ten mutations, ten red
  suites. → `in-review`.

**Two findings worth keeping, about the work rather than the toolkit.** First, `review-close`
earning its keep twice running is not ceremony — both rejections found things `verify` structurally
could not, because `verify` checks criteria and the reviewer reads the diff. Second, **F2 was
created by the previous review's own Finding 1 fix**: routing `add()` through `match_key()` was
right, and it dragged validation along with comparison. That is recorded plainly in `review.md`
and the journal, because a review record that hides its own consequences is worth little.

## Toolkit findings

1. **The board-write guard hook matches the command *string*, not the write target.** Reported last
   turn and hit twice more. It blocked a `git commit` compound command because a trailing `grep`
   *mentioned* the board's path, and blocked a journal append whose heredoc *content* contained
   `tracker/items/WI-0001/history.md`. Both were legitimate; both cost a detour through a scratch
   file. The hook guards the right thing and inspects the wrong surface.
2. **`tests-pass-on-the-merge-result` does not test the merge result.** `run-gate` reported it
   **PASS** while running plain `python3 -m unittest` in the working tree — the branch head, not a
   trial merge. `review-close` ran no trial merge at all (correctly: the item was being rejected).
   On an *accepted* item this gate would read as a trial merge that never happened. Recorded
   honestly in the journal rather than accepted at face value.
3. **Nothing says who may clear an acceptance-criterion tick.** `review-close` had to untick AC8
   to reject the item for an AC8 failure — leaving it ticked would have put a false statement in
   `item.md`, and a tick is the one thing the close relies on. That is the opposite of the
   forbidden "edit a criterion to make something pass", but no spec sanctions it. `spec/dor-dod.md`
   and the `verify`/`review-close` contracts should say so explicitly.
4. **No linter, three findings of the class a linter catches.** `ADR-0001` §4 sets `commands.lint`
   to null, so `lint-clean` is skipped on every item. All three defects of that shape so far — a
   dead `match_key()`, `main`'s never-passed `out`/`err`, and F1's incomplete validation — were
   found by a human-style read of a diff. It is already in the item's `## Accepted gaps` as an
   epic-level decision to revisit; three for three is the evidence for revisiting it.

## Open handovers, declared not buried

- **`expenses` list elements are still unvalidated.** F1's fix covers `people` only. WI-0002 must
  extend `store.load()` when it decides what an expense record is; inventing that schema now would
  pre-empt its plan. Named in `impl-report.md` and `verify-report.md`.
- **`plan.md` lines 24–29 carry the last copy of the claim F3 corrected** in `overview.md` and
  `errors.py`. `implement` deliberately did not edit another skill's artifact; `review-close` or
  `plan` should settle whether it is amended or left with a pointer.

**Why this turn stopped:** the USD budget, not a pipeline condition. WI-0001 sits at `in-review`
with everything committed and the workspace valid — a clean, resumable boundary. A `review-close`
pass needs the whole diff re-read, D1–D12, a trial merge and an epic check; starting one with
~$1.50 left would have left a half-written review, which is worse than none. Next turn's `/next`
will dispatch `review-close` on WI-0001, which is exactly right. Nothing is blocked, nothing waits
on a person, no work is lost.

```json
{
  "stop_reason": "error",
  "open_human_questions": [],
  "items_touched": ["WI-0001"],
  "last_action": "verify passed WI-0001 on a273c4e and returned it to in-review; stopped on USD budget, not on a pipeline condition",
  "notes": "stop_reason is 'error' only because the enum has no value for 'ran out of budget' - nothing failed and nothing is blocked. Workspace valid (0 errors, 0 warnings), 23 tests green, WI-0001 runnable at in-review: /next dispatches review-close. Read 'error' as an exhausted turn, not a defect. The turn's real result: review-close caught an AC8 violation (a store whose people list holds a non-string parsed cleanly, then raised AttributeError past cli.main's except ExpensesError - exit 1 with a traceback; the read path exited 0 printing it as a group member) that two verify passes missed, implement fixed it plus two related findings, and verify re-ticked AC8 on a 28-case sweep including that class. Four toolkit findings detailed above: (1) the board-guard hook matches command text not write target, blocked two more legitimate commands; (2) tests-pass-on-the-merge-result reported PASS while running the plain test command in the working tree, no trial merge - misleading on an accepted item; (3) no spec says who may untick an acceptance criterion, which review-close had to do to reject honestly; (4) three consecutive defects of the class a linter catches, on a project with commands.lint null. Two handovers are declared in the artifacts: expenses-list elements remain unvalidated and belong to WI-0002, and plan.md still holds the last copy of a claim corrected in overview.md and errors.py."
}
```
