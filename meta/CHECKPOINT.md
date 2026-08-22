# CHECKPOINT

## Current unit: META-092 — cluster 5a: the workspace a consumer actually gets

- **F-002 + F-047** — every directory the schema requires gets a `.gitkeep` from the tool that
  creates it: `workspace-init` **and** `new-item`. 1d found the sharper form: an item's empty
  `questions/` is deleted by the trial merge `review-close` performs, so the item fails
  `questions.missing` while being closed.
- **F-003** — the consumer workspace needs a `.gitignore` (`__pycache__` from the validator).
- **F-005** — the uninitialised state is not a hard failure; distinct exit code and a next step.
- **F-004 + F-012** — USAGE §2 (skills load at session start) and §4 (the trust requirement).

Then **META-093** (F-007 export), **META-094** (F-009 README), **META-101** (FINAL-REPORT-2).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024); `scripts/check`
  enforces it.
- `meta/harness/evidence/**` is read-only; filed finding text is appended to, never rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture.
- Toolkit commits and harness commits stay separate.
