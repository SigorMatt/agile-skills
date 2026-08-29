# CHECKPOINT

## Current unit: META-125 — budgets bound work, not verdicts

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..124 done and pushed; cluster 5's
findings pass and the regressions remain.

**Intent.** One rework in `harness/run_iteration.py`, five findings, and it is a **harness**
commit — separate from the toolkit commits above it.

- **H-014** — a workspace at a terminal ending stops `epic-done` (or `blocked-no-recourse`)
  regardless of the counter. Iteration 4 reached its ending, spent the budget's last slot on the
  closing sim turn, and stamped a finished engagement "turn-budget: not finished".
- **H-014** — the H-007 closing turn is budget-exempt. It exists for the engagement's benefit,
  not the budget's.
- **H-010** — a turn-budget stop is **resumable** unless the engagement is at an ending: a plain
  rerun with a larger `--max-turns` continues in place. Five occurrences, two of them landing
  between the sign-off being filed and the stakeholder answering it, and one visible to the
  person: *"I was asked to sign off twice for the same engagement, six hours apart."*
- **H-011** — the first job of a fresh run is derived from the workspace, exactly as mid-run
  scheduling is: unanswered human questions → sim answers; no `IDEA.md` → sim opens; otherwise
  the worker.
- **H-012** — the driver creates its run directory and opens its own console log **before its
  first line of output**. Wrappers stop being load-bearing.

Six-plus regression tests in `harness/tests/test_harness.py`, and `harness/USAGE.md` §9's stop
table rewritten to match. H-013 (the sim describing the disk) is META-126.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
