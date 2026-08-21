# CHECKPOINT

## Current unit — META-073

**Phase H, the two-session iteration harness.** Mission prompt:
`meta/harness/HARNESS-PROMPT.md` (read it below its divider). Design: `meta/harness/DESIGN.md`.
Queue: `meta/harness/PROJECT-QUEUE.md`. Plan units: `meta/plan.md` Phase H.

**Steps**
1. `harness/provision.py` — create the throwaway project directory (default root
   `~/agile-skills-throwaway`, `--root`/`HARNESS_THROWAWAY_ROOT` override), `git init` with a
   repo-local identity, initial commit, run `adapters/claude-code/install.py`, run
   `workspace-init`, merge the USAGE §4 allow-list into `.claude/settings.json`, write
   `SIMULATION-NOTICE.md` and the project `.gitignore`, commit.
2. Idempotent on re-run; refuses to touch a non-empty directory that is not one of ours
   (marker file `.harness/provision.json`).
3. Verify by execution: provision a real project, run `validate-workspace` in it, re-run
   provision to prove idempotence, and prove the refusal on a non-empty stranger directory.

**Done when** — the script is committed with its execution evidence quoted in the journal,
`./scripts/check` passes, tree clean.

**Next unit** — META-074, `harness/skills/simulated-human/`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
