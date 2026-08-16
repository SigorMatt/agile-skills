# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Current unit: META-001 — build scaffolding

**Steps**
1. `git init`; branch `main`. (done)
2. Create `meta/plan.md`, `meta/CHECKPOINT.md`, `meta/journal.md`, `meta/BLOCKERS.md`, `meta/adr/`.
3. Add `.gitignore` (`__pycache__/`, `.venv/`, `*.pyc`, `.DS_Store`).
4. Commit `meta: scaffold builder paper trail (refs META-001)`.

**Done criteria**
- `git log --oneline` shows exactly one commit referencing META-001.
- Working tree clean.
- `meta/plan.md` lists all planned units; META-001 ticked.

**Next unit:** META-002 — fetch current Claude Code skills docs and write
`meta/adr/ADR-0001-claude-code-skill-format.md`.
