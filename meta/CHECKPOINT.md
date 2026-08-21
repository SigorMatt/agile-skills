# CHECKPOINT

## Current unit — META-078

Driver restart, verified by execution.

**Steps**
1. Start a run against the scratch project, kill the driver mid-turn (SIGKILL to the driver and
   its `claude` child), then rerun the same command.
2. It must resume the same iteration from `state.json` — same run directory, turn numbering
   continuing, no lost or duplicated log lines, the project trail intact.
3. Record what the interrupted turn left behind and how the rerun reconciled it; if the toolkit
   handles the half-finished turn badly, that is a finding, not a fix.

**Done when** — the kill/rerun is demonstrated with the log to show for it, `./scripts/check`
passes, tree clean.

**Next unit** — META-079, `harness/USAGE.md`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
