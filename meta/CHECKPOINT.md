# CHECKPOINT

## Current unit: META-098 — the regression gate, part 1: everything is rendered and installable

Clusters 1, 2, 3 and 6 are done. Before iteration 1d runs against this toolkit, prove that what
*ships* works — the harness installs the adapter's `dist/` into a throwaway project, so a script
that exists in `scripts/` and not in `dist/` would surface as a mid-run failure with no
explanation.

Steps:
1. `./scripts/check` green (10 steps).
2. Provision a scratch throwaway project through the real installer and confirm: every new
   script is present and runs from the installed location (`journal-entry`, `lint-claims`,
   `check-epic-signoff`), `spec/request.md` shipped, `tracker/requests/` created, the pipeline
   carries `suspendable`, and the validator is green on the fresh workspace.
3. Fix anything that does not ship; commit; push.

Next unit: **META-099** — configure and run iteration 1d.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` and may not rewrite filed finding text.
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml`. Spec change ⇒ append to that spec
  file's `## Revisions` section. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
