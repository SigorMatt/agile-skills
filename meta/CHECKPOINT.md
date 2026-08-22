# CHECKPOINT

## Current unit: META-096 — harness H-004, H-005, H-006, H-007: the turn loop

Four findings, one unit, because all four are the driver's turn loop and its worker prompt.

Steps:
1. **H-004** — before dispatching a worker turn, the driver checks its own observed state; if
   unanswered human-addressed questions exist, it dispatches a sim `answer` turn instead. One
   full round trip was wasted per occurrence.
2. **H-005** — a killed turn records `cost_usd: null` with `cost-unknown: true` rather than
   `0.00`, and a `HARNESS-STATUS.md` whose mtime predates the turn's start is recorded as "no
   status written" instead of being silently attributed to the killed turn.
3. **H-006** — the worker prompt bounds a turn to N skill executions (config
   `worker-skills-per-turn`, substituted into the prompt), so turns are comparable and
   `--turn-timeout` stops punishing progress.
4. **H-007** — the sim gets one closing turn before any `epic-done` stop is accepted, logged as
   job `closing`. Partly self-healing now that F-022 opens a sign-off question at closure, but
   belt and braces.
5. Tests for each; check green; FINDINGS; journal; commit; push. **Harness prefix.**

Next unit: **META-098** — re-render and the full regression gate, then **META-099** (iteration 1d).

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
