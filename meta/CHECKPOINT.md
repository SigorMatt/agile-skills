# CHECKPOINT

## Current unit: META-099 — iteration 1d: configure, then run

The regression gate. 1c's setup, fresh project `expenses-1d`, with the probe extended so the
stakeholder also refuses every alternative to the sample — including the one 1c escaped through
(a design that needs no sample).

Steps:
1. `harness/skills/simulated-human/probes/iteration-1d-expenses.md` — 1c's probe with P2 extended:
   no name-the-columns version, no interactive mapping, no format guessing, no "wait for the
   sample" workaround. Everything else identical.
2. `harness/iterations/iteration-1d-expenses.json` — project `expenses-1d`.
3. Amend H-007's fix: the sim also gets a closing turn before `blocked-no-recourse` is accepted.
   1d is expected to end there, and an impasse is an ending the stakeholder should see. Filed as
   an addendum to H-007.
4. `provision.py --iteration iteration-1d-expenses`, then run it.
5. Findings pass (META-100), then FINAL-REPORT-2 (META-101).

Done when: the run has stopped and its trail is banked under `meta/harness/evidence/`.

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
