# CHECKPOINT

## Current unit — META-081

Findings F-011+ and `meta/harness/FINAL-REPORT.md`.

**Steps**
1. Append to `meta/findings/FINDINGS.md`: F-011 (answer-questions precondition), F-012 (an
   untrusted workspace's allow-list is discarded in headless runs), F-013 (a blocking question on
   an epic is unrepresentable), F-014 (transition gates the pre-move workspace), F-015 (implement
   must pass through a red validator), F-016 (epic-level record commits have no home branch),
   F-017 (the restamp deadlock in journal.md, and invented timestamps), F-018 (the write guard
   matches the command string). Update F-006 with the probe that settled it.
2. Fix the two harness defects the run exposed (H-001): worker turn prompt v2 reconciling
   amendments A and E, and a `turn-budget-exhausted` value in the `stop_reason` enum.
3. `meta/harness/FINAL-REPORT.md` — what was built, key decisions, defects found, what the
   harness does not test, and the exact command sequence for full iteration 1.
4. Final sweep: `./scripts/check`, `git diff --stat` proving `methodology/` and `spec/`
   untouched, tree clean, pushed.

**Done when** — the report is committed and the acceptance checklist in
`meta/harness/HARNESS-PROMPT.md` is answered box by box with evidence pointers.

**Next unit** — none. Stop and report.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
