# CHECKPOINT

## Current unit: META-100 — the findings pass over iteration 1d

1d stopped at `blocked-no-recourse`, turn 16, and its evidence is banked at
`meta/harness/evidence/iteration-1d/`. The toolkit is unfrozen.

Steps:
1. File F-025 … F-048 in `meta/findings/FINDINGS.md` from the notes in
   `/tmp/claude-1000/-home-msi-git-agile-skills/f8232ed6-406d-4a7f-81c0-f51ae1592eab/scratchpad/post-1d-todo.md`.
   Nothing is fixed silently: a defect this session caused gets filed like any other.
2. Addenda to F-002 (1d found its sharper form in `new-item`) and F-022 (the impasse gap).
3. Commit; push.

Next: **META-097** — fix the severe ones 1d found in this session's own work (F-033, F-037,
F-039, F-044, F-024b), then clusters 4 and 5, then **META-101** (FINAL-REPORT-2 §4–§6).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024).
- `meta/harness/evidence/**` is read-only; filed finding text is appended to, never rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture.
- Toolkit commits and harness commits stay separate.
