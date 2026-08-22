# CHECKPOINT

## Current unit: META-095 — harness H-002 and H-003: resume means resume, fresh means fresh

H-002: a turn killed by `--turn-timeout` records `stop-reason: turn-failed`, and a plain rerun
says "pass --fresh to archive it and start a new one" — while `harness/USAGE.md` §9 promises
"resume with the same command". The documented recovery did not exist; the only offered exit
archives four turns of good work. Recovery required hand-editing `state.json`.

H-003: `--fresh` archives the run logs and not the project workspace, so iteration 1 silently
resumed the mini run's epic. Acceptable outcome, wrong expectation.

Steps:
1. `harness/run_iteration.py` — stop reasons are classified `resumable` (a killed turn, a
   limit/auth rejection) or `terminal` (epic-done, blocked-no-recourse, turn-budget,
   contamination, validator-failed, stalled). A resumable stop clears on a plain rerun and the
   run continues, exactly as USAGE §9 already promises. A terminal stop says what `--fresh`
   actually does.
2. `harness/provision.py --wipe` — delete and re-create the project workspace, with an explicit
   confirmation and a refusal outside the throwaway root.
3. `harness/USAGE.md` §3 and §9 — one flag, one meaning, and the two of them stated together.
4. `harness/tests/test_harness.py` — the classification, both directions.
5. Check green; FINDINGS; journal; commit; push. **Harness commit prefix.**

Next unit: **META-096** — H-004, H-005, H-006, H-007 (one unit; all four are the turn loop).

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
