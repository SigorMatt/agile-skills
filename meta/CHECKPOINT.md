# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-102

**ADR-0006 — the termination model.** The derivation the mission asks for, written once, before
any code moves. F-013, F-029, F-045 and F-046 are one design debt: the status graph and the
authority rules were derived from the happy path.

Steps:
1. Enumerate every legal **ending** of an engagement, and every legal mid-flight event that
   changes the item set.
2. State the **termination gate**: no engagement ends, in any ending, without a blocking
   human-addressed question saying what was delivered, what was not, and why.
3. Derive the **creation-authority table** — who may create an item, in which status, with what
   provenance.
4. Name each historical contradiction (F-013, F-029 ×2, F-045, F-046) and say what the derived
   model does with it, so META-107 can turn each into a fixture.

Done when: `meta/adr/ADR-0006-termination-model.md` exists, `./scripts/check` is still green
(it does not read ADRs, so this is a no-op guard), committed and pushed, plan ticked, journalled.

## Next unit — META-103

The spec files re-derived from ADR-0006.

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
