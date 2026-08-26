# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-110 — iteration 1e

**The regression gate.** 1d's config and probe, unchanged; fresh project `expenses-1e`;
max-turns 18. The probe file is **byte-identical** to `probes/iteration-1d-expenses.md`
(sha256 `9f51368f…`), so the toolkit is the only variable.

```
harness/provision.py --iteration iteration-1e-expenses --wipe
harness/run_iteration.py --iteration iteration-1e-expenses
```

Expected shape: the run reaches the impasse as 1d did — and this time **ends through the
termination gate**. `next` step 6 dispatches `review-close` on the epic at rest; the sign-off
fires naming every child; the sim answers "no, not as it stands"; the ending is recorded on the
epic; the driver stops on a terminal reason with zero contamination violations.

**While the run is in flight, do not touch the toolkit.** An uncommitted change under
`methodology/`, `spec/`, `scripts/`, `adapters/`, `examples/`, `fixtures/` or the top-level docs
trips the harness's own W4 rule and stops the run. `meta/` and `harness/` are exempt.

Watch for: a `turn-budget` stop before the ending is recorded. 1d reached `blocked` at turn 14 of
16; the ending needs ~3 turns after that. If 18 is not enough, say so plainly in the report
rather than quietly raising it — the budget came from the mission.

Done when: the run has stopped, the trail is copied to `meta/harness/evidence/iteration-1e/`
and committed, plan ticked, journalled.

## Next unit — META-111

Findings pass over 1e's trail: anything new filed as F-049+/H-###.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work, then
  record the sha in a follow-up commit. `scripts/check` step 9 enforces this.
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **Do not modify the toolkit while a harness run is in flight.** An uncommitted change under
  `methodology/`, `spec/`, `scripts/`, `adapters/`, `examples/`, `fixtures/` or the top-level docs
  trips the harness's own W4 rule and stops the run. `meta/` and `harness/` are exempt.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump in
  `skill.yaml`. Spec change ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
- Toolkit commits and harness commits stay separate.
