# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-105a

**Enforcement over the workspace at rest.** `scripts/validate-workspace` and
`scripts/transition`, holding the model META-103/104 wrote down.

Steps:
1. `transition_is_legal` honours `applies_to`, so an epic can no longer be blocked by whichever
   skill happens to hold it.
2. `transition` refuses a move whose matching row is `gated: true`, not only the move to the
   actor's own `next_status` (ADR-0006 §1c).
3. `item.arose-from.missing` / `item.arose-from.unresolved` — provenance for every item whose
   creation row names an actor other than `intake` (F-029, F-042).
4. `question.deferred.*` — `deferred` is a legal status; a deferred blocking question leaves its
   item at `blocked` (F-028).
5. `epic.closed-with-active-children` and `epic.outcome.overclaims` replace
   `epic.closed-with-open-children`: children must be terminal, and an epic that closes with an
   undelivered child may not call itself `delivered` (DE1 as re-derived).
6. Every new code gets a case in `fixtures/broken-workspace` + `EXPECTED-CODES.txt`.

Done when: `./scripts/check` green with the new codes in the must-fail fixture, re-rendered,
committed and pushed, plan ticked, journalled.

## Next unit — META-105b

`scripts/engagement-state` and `check-epic-signoff` as the termination gate.

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
