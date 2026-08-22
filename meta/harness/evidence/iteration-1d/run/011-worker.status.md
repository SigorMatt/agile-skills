# Harness status — turn 11

No stakeholder answers were pending: all eleven questions on disk were already `answered` and
propagated, so `answer-questions` had nothing to consume and the turn went straight into the
loop. WI-0002 — "show who owes whom" — went from `ready` to `in-review` in three skill
executions, which is the turn budget.

- **`plan`** designed the debt report and wrote `tracker/items/WI-0002/artifacts/plan.md`: five
  steps, all eleven criteria mapped to a step and a named demonstration. Two ADRs came out of it.
  `ADR-0008` puts the computation in a new pure module rather than in the CLI handler, so AC3's
  arithmetic identity can be asserted without going through `argparse` and captured stdout.
  `ADR-0009` settles the one place the record disagreed with itself: where an uneven split's
  remainder goes when the payer is not among the sharers. `ADR-0004` said both "the payer is owed
  `t`" and "the sum of what is owed is `t - remainder`"; WI-0002's R10 table took the first half
  and AC3's "these net positions sum to zero" only holds under the second. It was answerable from
  the documents — arithmetic, not intent — so it was decided rather than escalated, and the ADR
  exists so a reader who trips over the R10 row finds the resolution.
- **`implement`** built it on `wi/WI-0002`: `expenses/debts.py` (one signed integer per unordered
  pair, so netting is addition), a `debts` subcommand in `cli.py` that only prints, and two test
  files. The suite went 83 → 115 tests. The overview went to v5. One thing worth noting: the
  first version of the AC5 ordering test would have passed against a sort on the display names —
  the people it used happened to sort the same way both ways — and it was found by mutation and
  rewritten.
- **`verify`** passed all eleven criteria against `c73f039`, using commands it ran itself over
  thirteen scratch ledgers plus a purpose-written AC3 checker that recomputes the arithmetic from
  the JSON ledger without importing the module under test. Eight negative cases were triggered
  rather than read about, and seven mutations confirm every criterion has a test that bites. No
  defect found, no bug filed.

Nothing refused to pass. Nothing is blocked, nothing is awaiting an answer.

**Where the next turn picks up.** WI-0002 is at `in-review`, so `next` will dispatch
`review-close`, which merges `wi/WI-0002` into `main` and closes the item. **The working tree is
left on branch `wi/WI-0002`, not `main`** — that is deliberate, since `check-commit-refs` reads
`main..wi/WI-0002` and merging before closing would empty that range (the gate says so itself).
After WI-0002 closes, BUG-0001 (`ready`, medium) becomes the top runnable item and WI-0003
(`draft`) unblocks.

Two things a reader should know, neither of which is a defect in this item:

- `expenses/cli.py`'s module docstring still says the module is "the only one that exits", which
  is false — `main` returns an `int` and `__main__.py` raises the `SystemExit`. `review-close`
  corrected exactly that sentence in the architecture overview for WI-0001 and left the docstring.
  `implement` declined to fix it here (no criterion traces to it) and declared it; `verify`
  classified it as an observation rather than a bug, since there is nothing to reproduce. It is
  still there.
- A methodology hazard hit during verification, worth recording for whoever repeats it: a mutation
  whose replacement line was the same length as the original, reverted within the same second,
  left `__pycache__` serving the mutated bytecode. The suite reported 22 failures against a
  working tree `git status` called clean. Removing `expenses/__pycache__` and `tests/__pycache__`
  restored `Ran 115 tests … OK`. Clear the caches between mutations rather than trusting
  timestamp invalidation.

Two toolkit frictions, both minor:

- `lint-claims` treats a repeated `src:` prefix inside a single citation marker as part of the
  citation text. Writing two sources in one marker works only if the second omits the prefix and
  is separated by a semicolon alone; repeating the prefix on the second source fails to resolve.
  `spec/doc-header.md` says several sources are "separated by a semicolon inside one marker"
  without showing an example, and the error message names the malformed citation rather than the
  repeated prefix. It cost two edits to work out, in an ADR and in the plan.
- `validate-workspace` lints this file too, even though it is git-ignored and belongs to the
  harness rather than to the project. Describing the citation-syntax problem above in its own
  notation made the validator red, so it had to be written around. Worth knowing before anyone
  tries to quote a malformed citation in a status report.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["plan", "implement", "verify"],
  "open_human_questions": [],
  "items_touched": ["WI-0002"],
  "last_action": "verify passed all eleven criteria on WI-0002 against c73f039 and moved it to in-review; the record is committed on branch wi/WI-0002",
  "notes": "No answers were pending, so answer-questions did not run. WI-0002 is at in-review and the tree is left on wi/WI-0002 on purpose — check-commit-refs reads main..wi/WI-0002 and merging before closing empties it. Next turn: review-close merges and closes, then BUG-0001 is top of the queue and WI-0003 unblocks. Planning surfaced a genuine contradiction inside the record (ADR-0004's two halves versus WI-0002's R10 row versus AC3's sum-to-zero claim) and resolved it as ADR-0009 rather than guessing. Toolkit: lint-claims rejects a repeated 'src:' prefix on the second source inside one citation marker, and its error message points at the citation rather than at the prefix; separately, validate-workspace lints this git-ignored status file, so a status report cannot quote a malformed citation to describe the problem."
}
```
