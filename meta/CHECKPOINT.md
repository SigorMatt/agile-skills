# CHECKPOINT

## Current unit: META-089 — F-021: the stakeholder can speak without being spoken to

F-021: the human can only speak when spoken to. Run 1b's sim held a new requirement across two
turns and logged that no question gave it a vehicle; the run then ended `epic-done` with the
requirement never voiced. Real stakeholders volunteer things constantly.

Steps:
1. `spec/request.md` — a new artifact: `tracker/requests/R-###.md`, a question in reverse. The
   stakeholder writes it at any time; a skill responds and records what changed.
2. `scripts/workspace-init` — creates `tracker/requests/`.
3. `scripts/validate-workspace` — the request schema, and the rule that an open request has a
   response or is still open with nothing else claiming to have handled it.
4. `methodology/pipeline.yaml` — orchestrator step 2a: an open request outranks building the
   candidate set; `next` dispatches `intake` on it. Pipeline minor bump.
5. `methodology/skills/next/process.md` and `intake/process.md` — the routing and the handling.
6. `spec/workspace-layout.md`, `spec/README.md` — the directory and the index.
7. Fixture both ways; re-render; check green; FINDINGS; journal; commit; push.

Next unit: **META-090** — cluster 3 (F-011, F-014, F-015, F-016).

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
