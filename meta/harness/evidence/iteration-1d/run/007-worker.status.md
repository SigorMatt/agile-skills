# Harness status — turn 7

No question was waiting, so this turn ran the pipeline straight through and delivered the first
work item end to end. Three skills, one item, `main` now has a working tool on it.

- **`implement` on WI-0001 → `verifying`.** All eight plan steps, nine commits on `wi/WI-0001`.
  `expenses/model.py` (validators + four dataclasses), `expenses/store.py` (path resolution, load,
  atomic save), `expenses/cli.py` (six subcommands behind one `main`), `expenses/__main__.py`, and
  83 tests across six files. `impl-report.md` maps every criterion to a named test method and
  declares five deviations from the plan. All seven gates green on the branch head.
- **`verify` on WI-0001 → `in-review`.** Every criterion checked by commands run here rather than
  by reading the implementation report — 41 refusals triggered, the ledger's md5 compared before
  and after each, AC10 driven through real `subprocess` invocations. Then twelve source mutations,
  one per criterion; every one turned the suite red, so nothing is covered only in appearance.
  All twelve criteria ticked. **BUG-0001 filed.**
- **`review-close` on WI-0001 → `done` (`delivered`), merged into `main`.** D1–D12 each recorded
  with its own evidence. Trial-merged into a throwaway branch first, ran the suite on the merge
  result (83 pass), discarded it, closed the item while the branch was still unmerged, then
  merged. `EP-001` stays `open` — three children to go, so no sign-off question is due.

## What was found

- **BUG-0001 (ready, `found-in: WI-0001`, medium).** `add-person`, `add-expense` and `repay` all
  print their success line *before* `main` attempts the save. With the ledger's directory
  unwritable, a run prints `Added Cara.` on stdout, the failure on stderr, and exits 1. Filed as
  its own item rather than as a send-back: WI-0001 defines a refusal as a stderr message, a
  non-zero exit and unchanged data, and all three hold, so no criterion of WI-0001 is violated.
  `cli.py`'s own module docstring states the intended order the other way round, so it is a slip
  against the stated design, not a choice.
- **D12 caught a false claim in the docs.** `overview.md` said `cli.py` is "the only one that
  exits"; `cli.main` returns an int and `__main__.py` is the only statement in the package that
  ends the process. Found by opening the four modules, which is the one way that check can fail.
  Corrected in v3 rather than sent back — one clause, no code wrong. This is exactly the failure
  mode D12 was written for.
- **Five gaps accepted and written into `WI-0001`'s `## Notes`**, not left in the reports: the
  on-disk `version` is written and never read; concurrent writers can lose an update; `--file ""`
  falls through to the default rather than being refused; `lint` is a `compileall` syntax check
  and nothing more; the literal `~/.local/share` default was never written to during verification.
  Each row names who should pick it up.

## Things worth knowing about the toolkit

- **`check-commit-refs` fails loudly and helpfully on an `in-progress` transition.** The opening
  `implement` move runs the completion gates for information, and on a branch with no commits yet
  the gate reports "already merged into main, so main..wi/WI-0001 is empty". It is not blocking —
  the transition says so explicitly — but the message reads as an error on a perfectly healthy
  branch, and a worker could waste time on it. The same message is the right one later.
- **`journal-entry` requires a `**Status:**` bullet even for an entry that records no transition.**
  BUG-0001's creation entry was refused until it carried `- **Status:** \`—\` → \`ready\``. Fine
  once known; the `--template` output does not flag that it is mandatory in the no-move case.
- **`new-item` writes a `history.md` row but no journal entry**, so a freshly created item fails
  `validate-workspace` with `journal.execution.missing` until the creating skill journals it. That
  is the right design, but the script's own success message ("fill in the body headings before
  transitioning it") does not mention the journal entry, and the validator error arrives later.
- **`check-verify-freshness` is better than D10 requires.** It distinguishes record-only commits
  under `tracker/` and `docs/` from code changes, so a review that corrects a document does not
  invalidate its own verification. Both of this turn's post-verification commits relied on that.
- `lint-claims` still ignores explicit file arguments, as turn 6 recorded. Only `--changed-since`
  checks anything. This turn always used that form.

Workspace validates with 0 errors and 0 warnings. `main` is at the merge commit, 83 tests pass on
it, and the tool runs: `python3 -m expenses --help`.

Next turn's `next` will dispatch `refine` on WI-0002 — it is `high`, and its `depends-on WI-0001`
is now satisfied, so it outranks BUG-0001 at `medium`.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["implement", "verify", "review-close"],
  "open_human_questions": [],
  "items_touched": ["WI-0001", "BUG-0001"],
  "last_action": "review-close closed WI-0001 as delivered and merged wi/WI-0001 into main; the board shows 1 done, 1 ready bug, 2 draft, EP-001 open",
  "notes": "Three skills, one item, delivered end to end with no question filed and nothing blocked. verify filed BUG-0001 (success line printed on stdout when the ledger write fails) and review-close's D12 audit corrected a false sentence in docs/architecture/overview.md. Toolkit notes: check-commit-refs emits an alarming 'already merged into main' message on the opening in-progress transition of a commit-less branch (non-blocking, but misleading); journal-entry requires a **Status:** bullet even for an entry that records no transition; new-item leaves the item failing validate-workspace until the creating skill journals the creation, which its success message does not mention. check-verify-freshness correctly treats tracker/ and docs/-only commits as not invalidating a verification, which both post-verification commits this turn depended on."
}
```
