# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Standing instructions (survive session restarts)

- **The unit cycle ends with `git push`, not `git commit`.** The human instructed on
  2026-08-16: add `git@github.com:SigorMatt/agile-skills.git` as `origin`, push everything, and
  push after every commit from then on. `origin` is configured and `main` tracks it. Journaled
  under META-035.

## Current unit: META-040 — `adapters/README.md`, the adapter contract

**Why:** acceptance B4 requires the contract to be complete enough that a Codex CLI adapter
could be written **without touching `methodology/`**. Writing it before the renderer keeps the
renderer honest — it becomes an implementation of a stated contract rather than the contract
being back-filled from whatever the renderer happened to do.

**Steps**
1. Write `adapters/README.md` covering:
   - the capabilities any adapter must map (C1 skill discovery/triggering, C2 asking the human,
     C3 gate execution, C4 install/uninstall, C5 optional isolated subagent execution), each
     with what the methodology needs and what a runtime may substitute;
   - exactly what a renderer consumes (`skill.yaml` + `process.md` + `spec/` + `pipeline.yaml`)
     and the rule that needing anything else is a methodology defect;
   - placeholder resolution (`spec/skill-contract.md` §1.4) and where `pipeline.yaml` and the
     scripts must be installed so `validate-workspace` can find them;
   - the honesty rule: an adapter documents per gate whether enforcement is hard or convention;
   - a conformance checklist a new adapter can be graded against.
2. Commit `adapters: the adapter contract (refs META-040)` and **push**.

**Done criteria**
- `adapters/README.md` exists and its conformance checklist is specific enough to grade against.
- `./scripts/check` still green; tree clean; plan ticked; journal appended; pushed.

**Next unit:** META-041 — `adapters/claude-code/render.py`.
