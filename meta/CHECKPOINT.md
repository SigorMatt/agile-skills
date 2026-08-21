# CHECKPOINT

## Phase H is complete. There is no next unit.

The two-session iteration harness is built and proven:
[`meta/harness/FINAL-REPORT.md`](harness/FINAL-REPORT.md) — what was built, the decisions, the
acceptance boxes with their evidence, what it does **not** test, and §6, the exact command
sequence for full iteration 1.

If you are a fresh session picking this up, the next piece of work is **running iteration 1**,
not building anything:

```bash
./scripts/check
harness/provision.py --iteration iteration-1-expenses
harness/run_iteration.py --iteration iteration-1-expenses --fresh
```

Then review with the owner per `harness/USAGE.md` §5 and §8, and append findings from F-019
onward. `meta/findings/FINDINGS.md` now carries F-001 … F-018; F-006 is closed as rejected.

Do not fix the toolkit inside a harness run. The harness must work against the toolkit as it is.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
