# CHECKPOINT

## Current unit: META-090 — cluster 3: F-011, F-014, F-015, F-016

Four independent pipeline/spec correctness defects, all found organically by the worker in
iteration 1.

Steps:
1. **F-011** — `answer-questions` precondition 1 tells the only skill that can consume a human's
   answer that it has nothing to do. Rewrite it: answerable means addressed to `architect`, **or**
   addressed to `human` with `## Answer` filled in. Drop the harness worker-prompt workaround
   that exists only to talk the worker past that sentence.
2. **F-014** — `transition` runs `workspace-valid` against the pre-move workspace, so every
   `answer-questions` resume prints a FAIL for correct work. Evaluate the gate against the state
   the move produces.
3. **F-015** — `implement` step 3 moves to `in-progress` before any journal entry exists, so
   `journal.execution.missing` is guaranteed mid-run. META-084b's one-command journal+transition
   is the mechanism; adopt it at step 3.
4. **F-016** — an epic-level record commit lands on whatever branch is checked out and fails the
   commit-reference gate for an unrelated item. State the rule and enforce it.
5. Fixtures/demonstrations per fix; re-render; check green; FINDINGS; journal; commit; push.

Next unit: **META-095** — harness H-002/H-003 (cluster 6 is pulled ahead of clusters 4 and 5,
because iteration 1d depends on it; see meta/plan.md).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` and may not rewrite filed finding text.
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml`. Spec change ⇒ append to that spec
  file's `## Revisions` section. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
