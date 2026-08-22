# CHECKPOINT

## Phase I is complete. There is no next unit.

Builder session two worked the findings ledger and ran iteration 1d as its regression gate.
Everything is on `main` and pushed. Read [`meta/FINAL-REPORT-2.md`](FINAL-REPORT-2.md) first.

Where things stand:

- **38 findings fixed**, each citing a commit that `./scripts/check` verifies is in this
  repository's history. **14 open**, 1 rejected, 1 deferred.
- `./scripts/check`: **13 steps, all passing** — 195 selftest cases, 63 must-fail fixture codes,
  30 write-guard cases, 47 harness tests.
- **Iteration 1d** ran to `blocked-no-recourse` in 16 turns and $71.75 with zero contamination
  violations. `blocked` executed for the first time in five runs; the trail is banked at
  `meta/harness/evidence/iteration-1d/` and is read-only.
- **ROADMAP §2 is not met**: two of three conditions hold, and "a full consumer run with zero
  version bumps" does not. The Codex adapter and the content packs stay gated. FINAL-REPORT-2 §6
  is the argument.

## What the owner does next

1. Review 1d's trail: `meta/harness/evidence/iteration-1d/README.md`, then `run/SIM-LOG.md`
   (`[PLANTED:` is coverage, `[ORGANIC]` is signal), then the item trail.
2. Then iteration 2 (`tidy`), already configured, against the fixed toolkit.

## If you are a builder session picking this up

The highest-value open findings, in order, are in FINAL-REPORT-2 §6 "Recommended next":
**F-045** (the sign-off gate does not fire on an impasse) and **F-029** (three skills need to
create items and only two may) — both are F-013's structural shape again — then **F-028**
(a deferred answer has no representation, which undermines the F-011 fix).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work, then
  record the sha in a follow-up commit. `scripts/check` step 11 enforces this.
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
