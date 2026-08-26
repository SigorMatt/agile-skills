# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-106

**The skill contracts re-derived from ADR-0006.** Prose and contracts; version bumps; re-render.

1. `next` — orchestrator step 6: an engagement at rest is dispatched to `review-close`, read
   from `scripts/engagement-state` rather than judged. 0.2.0 → 0.3.0.
2. `review-close` — it ends engagements: `dispatch.item_types` gains `epic`; step 10 rewritten
   around rest and the four endings; it may file a bug at `ready` with provenance (F-029.2).
   0.3.1 → 0.4.0.
3. `answer-questions` — the deferral (F-028): decide under it, or record `deferred` and move the
   item to `blocked`. It may create a work item at `draft` when an answer widens scope
   (F-029.1). 0.1.4 → 0.2.0.
4. `refine` — DoR R9's split is a creation, and it now has the authority and the provenance rule.
5. `verify` — provenance on a filed bug.

Done when: `./scripts/check` green, rendered output current, committed and pushed, plan ticked,
journalled.

## Next unit — META-107

Fixtures both ways for every historical contradiction, plus a must-pass ended engagement.

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
