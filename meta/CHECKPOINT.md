# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-111 — the findings pass over 1e

Read the banked trail at `meta/harness/evidence/iteration-1e/` and file what it found. Nothing is
fixed silently; anything new is **F-049+** or **H-009+**.

Sources, in the order USAGE §5 gives them:
1. `project/tracker/board.md` — where the work got to.
2. `run/SIM-LOG.md` — `[PLANTED:` is coverage, `[ORGANIC]` is signal. The stakeholder's
   "As a stakeholder I noticed" lines are the highest-yield part.
3. `run/iteration-log.jsonl` — durations, costs, the driver's observed status per turn.
4. `run/*-worker.status.md` — the worker's own account of what it hit.
5. The item trail — `history.md`, `journal.md`, `questions/`.

Already filed from this run and **not** to be re-filed: **H-008** (the driver's impasse test).
Already known and stated: `status: deferred` had no organic occurrence — the fork fired instead.

Done when: new findings appended with evidence citations, FINDINGS statuses current,
committed and pushed, plan ticked, journalled.

## Next unit — META-112

`meta/FINAL-REPORT-2.5.md` — finish §6 onward: what 1e proved, the honest ROADMAP §2 read, and an
explicit go/no-go for iteration 2 (`iteration-2-tidy` runs only on a go).

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
