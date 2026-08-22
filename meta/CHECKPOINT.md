# CHECKPOINT

## Current unit: META-094 — F-009: README positioning against BMAD-METHOD

Ship-blocker for the open-source release. Per the finding's filed direction: a positioning
section that is honest about the incumbent, states our thesis as delegate-and-verify rather than
collaborate-and-facilitate, points users who want facilitation at them, and respects the
trademark constraint ("derived from" is the only permitted relationship claim; we make no such
claim, having derived nothing).

Then **META-093** (F-007 export), then **META-101** (FINAL-REPORT-2 §4–§6).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024); `scripts/check`
  enforces it.
- `meta/harness/evidence/**` is read-only; filed finding text is appended to, never rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture.
- Toolkit commits and harness commits stay separate.
