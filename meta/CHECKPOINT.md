# CHECKPOINT

## Current unit — META-080

The mini end-to-end iteration, on PROJECT-QUEUE entry 1 (`expenses`).

**Steps**
1. Follow `harness/USAGE.md` literally, at the default throwaway root
   (`~/agile-skills-throwaway`), correcting the document wherever it is wrong.
2. `harness/provision.py --iteration iteration-1-expenses`, then
   `harness/run_iteration.py --iteration iteration-1-expenses --max-turns 16` with the default
   models (worker opus, sim sonnet).
3. Target: intake + refinement completed through the async protocol, one work item at `done`,
   at least one planted probe consumed — or a stop condition correctly reported.
4. Copy the whole run plus a copy of the project trail into
   `meta/harness/evidence/iteration-1-mini/` and commit it.

**Done when** — the evidence is committed with an honest account of how far the run got,
`./scripts/check` passes, tree clean.

**Next unit** — META-081, findings F-011+ and `meta/harness/FINAL-REPORT.md`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
