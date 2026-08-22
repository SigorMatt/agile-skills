# CHECKPOINT

## Current unit: META-082 — Phase I plan + checkpoint

Builder session two. Mission: `meta/BUILDER-2-PROMPT.md`. Backlog: `meta/findings/FINDINGS.md`.

Steps:
1. Append Phase I (META-082 … META-101) to `meta/plan.md`.
2. Overwrite this checkpoint with the unit cycle for Phase I.
3. Commit; push.

Done when: `meta/plan.md` carries the Phase I unit list and this file names META-083 next.

Next unit: **META-083** — F-019 (root-resolving scripts, no chained transitions,
journal-status ↔ history cross-check).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` (read-only history) and may not rewrite filed
  finding text (append corrections instead).
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml` (patch for a fix, minor for a contract
  change). Spec change ⇒ bump the spec's version header. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
