# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-103

**The spec re-derived from ADR-0006.** Prose only; `pipeline.yaml` and the scripts follow in
META-104/105, so `./scripts/check` may report the spec and the pipeline disagreeing at the end of
this unit only if a lint rule reads the prose — it does not, so the gate must stay green.

Files, and what changes in each:
1. `spec/ids-and-statuses.md` — §3.2 the four endings and the epic's final states; §4 the
   transition table gains `applies_to` and the epic ending rows; new §6 **creation authority**
   with the provenance rule. `## Revisions` row.
2. `spec/work-item.md` — `arose-from` (required for items created by `refine`,
   `answer-questions`, `verify`, `review-close`); `outcome: delivered-partial` for epics.
3. `spec/dor-dod.md` — DE1 generalised to "every child at a terminal status, the undelivered
   named"; DE7 generalised from completion to **termination**.
4. `spec/question.md` — `kind: sign-off` is the termination question (trigger = rest, content =
   every child named); `status: deferred` (F-028) with the rule that a deferred blocking question
   sends its item to `blocked`.

Done when: the four files carry the rules and a `## Revisions` row each, `./scripts/check` green,
committed and pushed, plan ticked, journalled.

## Next unit — META-104

`pipeline.yaml` 0.4.0 and the `lint-skills` rules that hold it to the spec.

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
