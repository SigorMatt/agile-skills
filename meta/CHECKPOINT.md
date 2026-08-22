# CHECKPOINT

## Current unit: META-091 — cluster 4: refine calibration (F-020, F-023)

- **F-020** — `refine` files several separate questions for one item in one round; the protocol
  batches per round-trip but presents per-file. Keep one artifact per decision (provenance needs
  it), add a grouped presentation per item per round.
- **F-023** — `refine` over-escalates technical trivia; a stakeholder's standing deferral on a
  category should be honoured for that category. Add a routing test before filing to the human.
- Also fold in **F-027** (a question must not bundle two decisions) — same section, same skill,
  and 1d gave it both evidence and counter-evidence.

Then: **META-092/093/094** (cluster 5), **META-101** (FINAL-REPORT-2 §4–§6).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024); `scripts/check` now
  enforces it.
- `meta/harness/evidence/**` is read-only; filed finding text is appended to, never rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture.
- Toolkit commits and harness commits stay separate.
