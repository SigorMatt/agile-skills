# Harness status — turn 7

No question was open when this turn started, so nothing needed consuming and the loop ran
straight through. Three skill executions, all on WI-0001, which went from `planned` to `done` and
is now merged into `main`. The turn ended on the budget, not on a stopping point.

- **`implement` on WI-0001.** Branch `wi/WI-0001` off `main` at `f5285a5`, moved to `in-progress`
  before any code was written. All seven plan steps worked in order, one commit each: the package
  skeleton, `money.py` (integer minor units, the remainder rule), `store.py` (one JSON dataset,
  located by `EXPENSES_STORE`/XDG, written by atomic replace), `cli.py` (the four commands and a
  single failure path), and `README.md`. 50 tests, written with the module each covers rather
  than in one pass at step 6 — that and three others are declared as deviations in
  `impl-report.md`, all in *how* rather than *what*. Six gates pass on the branch head;
  `lint-clean` is `skipped` because the project has no lint command and ADR-0004 says why.
- **`verify` on WI-0001.** Every criterion checked by commands run in verification, derived from
  the criterion before reading the implementation report — nine verdicts, all pass. Nineteen
  refusals triggered rather than read about, byte comparisons done with `cmp` and `md5sum` for the
  four criteria that turn on identical output, and the data file's own hash checked across AC5's
  refusals so that "nothing changed" means the file and not just the listing. Nine mutations, one
  per criterion, each making that criterion's test fail; the tree was restored and the suite
  re-run green. **BUG-0001** filed at `ready`.
- **`review-close` on WI-0001.** D1–D12 walked one at a time with evidence for each. The D12 audit
  was done from the citations — eight claims in `docs/`, each checked by opening the code it is
  about, not by re-reading the sentence. Trial merge onto a throwaway copy of `main` was a clean
  fast-forward with the suite green on the merge result; the trial was discarded, the item closed
  `done`/`delivered`, and only then was the branch merged for real (`3ca3868`). **BUG-0002**
  filed at `ready`.

Two defects were found and neither was held against WI-0001, because no criterion of that item
covers either:

- **BUG-0001** (`low`) — two absolute claims in `docs/product/vision.md` carry their source in
  prose but not in the citation marker `spec/doc-header.md` §4a requires, so `lint-claims --all`
  exits 1 while the trunk-scoped run every contracted gate uses exits 0. `implement` found it and
  had no authority to file it; `verify` did.
- **BUG-0002** (`medium`) — `store.save` lets an `OSError` escape as a traceback where
  `store.load` turns the same class of error into a one-line refusal, so an unwritable store exits
  1 with a stack trace instead of 2 with a message. Found by `review-close` running the error
  paths the diff leaves open. No data is at risk: the atomic-replace write leaves the previous
  dataset untouched.

Nothing is blocked that was not blocked before: WI-0003 is still parked on the bank CSV sample the
stakeholder said they would send. `engagement-state EP-001` reports **active** — BUG-0001,
BUG-0002, WI-0002 and WI-0004 are still in flight — so no sign-off is due and none was filed. No
question is open, to anyone. The workspace validates with 0 errors and 0 warnings, and the trunk's
test suite passes. Next turn's `/next` should dispatch `refine` on WI-0002, which is now unblocked.

## Notes on the toolkit

Six things got in the way, none fatal. The two from last turn that were about `refine` and the
clock are gone: the clock now agrees with the harness at 2026-08-27, and `refine` was not run.

1. **`transition` says "nothing was written" when something was.** A journal body missing the
   `**Status:**` bullet is rejected with `transition: nothing was written`, but `branch:
   wi/WI-0001` had already been written into `item.md` by then. The message is wrong about its own
   behaviour, which is the one thing a checkpoint tool cannot afford. Validate the body before
   touching any file.
2. **The `**Status:**` bullet is required in a body whose `**Status:**` bullet the tool overwrites.**
   `SKILL.md` says the transition "writes the `**Status:**` bullet itself from the move it actually
   made", which reads as licence to omit it; the tool then refuses the body for omitting it. Either
   accept a body without one, or say plainly that a placeholder is mandatory.
3. **`check-commit-refs` mis-diagnoses an empty range on a fresh branch.** At `planned ->
   in-progress` the branch has no commits yet, and the gate reports "wi/WI-0001 is already merged
   into main ... Rewind the merge, close, then merge" — advice for the opposite situation. The
   range is empty because nothing has been committed, not because everything has been merged.
4. **`new-item` still leaves the workspace invalid** (`journal.execution.missing`) until the caller
   writes the entry by hand with `journal-entry`. Hit twice this turn, once per bug filed. This was
   reported in turn 6 and still stands: `new-item` should take `--journal-body-file` the way
   `transition` does.
5. **The citation linter reads its own quoted output as citations.** Filing BUG-0001 meant quoting
   `lint-claims`' error text, whose hint line contains the literal marker syntax; the validator then
   tried to resolve it against the workspace and failed the item — five errors on a freshly created
   item, including one in the history row's `reason`, which is append-only and cannot be edited. The
   item was seconds old and uncommitted, so it was deleted and re-filed with the hint lines elided
   and the elision declared. A reproduction of a claims-linter failure is a thing this toolkit
   should be able to record; today it cannot quote one.
6. **`lint-claims --changed-since main` reported "checked no documents changed since main"** while
   on a branch that had added `README.md` and several tracker artifacts relative to `main`. Rule 1
   did fire on `README.md` while the file was uncommitted, so the gate is not inert — but the
   summary line claims a scope it did not have, and a reader would take the exit-0 as broader
   coverage than it was. Worth checking whether the rule-2 scoping is `docs/`-only by design and
   whether committed branch changes are meant to count as "changed".

Smaller: `new-item` accepts a title over the 80-character limit and only `validate-workspace`
catches it afterwards, which means editing a file the tool just wrote.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["implement", "verify", "review-close"],
  "open_human_questions": [],
  "items_touched": ["WI-0001", "BUG-0001", "BUG-0002"],
  "last_action": "review-close closed WI-0001 as done/delivered and merged wi/WI-0001 into main as 3ca3868",
  "notes": "Three executions, the budget, not a stopping point. WI-0001 is delivered and merged: a python3 -m expenses CLI with 50 tests, all nine acceptance criteria verified by commands run in verification and every criterion's test shown to fail when its behaviour is removed. Two bugs filed rather than held against criteria that do not cover them: BUG-0001 (low, two unsourced absolutes in docs/product/vision.md) and BUG-0002 (medium, store.save lets an OSError escape as a traceback where store.load refuses cleanly). EP-001 is active, not at rest, so no sign-off is due. WI-0003 stays parked on the bank CSV sample. Workspace validates 0 errors 0 warnings and the trunk's suite passes. Toolkit findings above; the two most worth fixing are transition reporting 'nothing was written' after a partial write, and the citation linter making it impossible to quote its own output inside a tracker artifact."
}
```
