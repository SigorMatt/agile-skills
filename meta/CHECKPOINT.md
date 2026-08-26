# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-108

**The correctness batch.** Three findings, one unit, because each is small and none of them
touches the others.

1. **F-031** — DoR R8 is an `[auto]` check that only tests that `refinement-qa.md` exists. It
   must read a **field**: the artifact declares `status: agenda | recorded`, and R8 is satisfied
   only by `recorded`. A mechanical gate that checks the wrong thing is worse than a manual one,
   because it is trusted. Migrating `examples/toy-project`'s artifacts is part of the unit.
2. **F-034** — `plan` created empty `__init__.py` files so its own gate commands could run at
   all, and flagged it under `## Risks` because `plan` is specified as producing no code.
   Resolve the contract conflict explicitly by ADR, whichever way it goes.
3. **F-038** — a transition can leave the tracker committed-invalid. Documented behaviour,
   undocumented window: state it in `spec/skill-contract.md` §2.3.

Done when: `./scripts/check` green, rendered output current, committed and pushed, plan ticked,
journalled.

## Next unit — META-109

Ledger statuses current with real commit citations, and the gate green end to end.

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
