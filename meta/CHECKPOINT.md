# CHECKPOINT

## Current unit — META-079

`harness/USAGE.md` — how the owner runs an iteration end to end.

**Steps**
1. Write it: prerequisites and quota, provision, run, the run directory's contents, how to read
   a run (board → SIM-LOG planted-vs-organic → iteration log → item trail), how to adjust the
   human between iterations, the contamination rules, what to do after an iteration, and the
   failure modes with what each stop reason means.
2. Then follow it literally for the mini run in META-080, and fix whatever it got wrong.

**Done when** — the document is committed, `./scripts/check` passes, tree clean.

**Next unit** — META-080, the mini end-to-end iteration on queue entry 1.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
