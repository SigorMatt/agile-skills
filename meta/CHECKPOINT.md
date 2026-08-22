# CHECKPOINT

## Current unit: META-099 — iteration 1d is RUNNING

Started 2026-08-22T01:33:23Z. Driver log:
`/tmp/claude-1000/-home-msi-git-agile-skills/f8232ed6-406d-4a7f-81c0-f51ae1592eab/scratchpad/1d-driver.log`
Run directory: `harness/runs/iteration-1d-expenses/`. Project: `~/agile-skills-throwaway/expenses-1d`.

**While it runs, do not touch `methodology/`, `spec/`, `scripts/`, `adapters/`, `examples/`,
`fixtures/`, `README.md`, `USAGE.md`, `CONSUMER-PROMPT.md` or `PROMPT.md`.** An uncommitted change
under any of those appearing during a worker turn trips the harness's own W4 contamination rule
and stops the run. `meta/` and `harness/` are exempt by design (`harness/audit.py`,
`TOOLKIT_PATHS`).

If the run has stopped when you read this:
- resumable stop (`turn-timeout`, `api-rejected`, `turn-failed`) → rerun
  `harness/run_iteration.py --iteration iteration-1d-expenses` and it continues;
- terminal stop → move to META-100.

## Next units

- **META-100** — findings pass over 1d's trail: `harness/runs/iteration-1d-expenses/SIM-LOG.md`,
  `iteration-log.jsonl`, then the project's `tracker/board.md` and item trail. Anything new is
  filed as F-025+/H-008+. Bank the evidence under `meta/harness/evidence/iteration-1d/`.
- **META-097** — the queued toolkit work in
  `/tmp/claude-1000/-home-msi-git-agile-skills/f8232ed6-406d-4a7f-81c0-f51ae1592eab/scratchpad/post-1d-todo.md`:
  F-024(b) (a `scripts/check` step asserting every cited commit sha is an ancestor of HEAD) and
  the `status_claims` false-positive fix found by self-review.
- **META-091** — cluster 4: F-020, F-023.
- **META-092/093/094** — cluster 5: F-002, F-003, F-004, F-005, F-007, F-009.
- **META-101** — finish `meta/FINAL-REPORT-2.md` §4, §5, §6 (§1–§3 are already written).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work,
  then record the sha in a follow-up commit.
- It may NOT touch `meta/harness/evidence/**` and may not rewrite filed finding text.
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml`. Spec change ⇒ append to that spec
  file's `## Revisions` section. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
