# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) one mask for every citation surface · META-168 (`656b6c5`)
severity follows knowledge + check step 6a (the proof-case over a copy of the banked evidence) ·
META-169 (`c8f69b3`) ADR-0013, a toolkit source is quoted and attributed, not pointed at ·
META-170 (`b6ff22f`) the grammar placed in the seven skills whose contracts oblige a citation,
plus check step 15d. **47 steps, 110 fixture codes, 419 selftest cases.**

**Current unit: META-171 — H-022: is a fixable record defect terminal? (harness commit)**

The decision to implement: **a fixable record defect is not a verdict on the engagement.** On a
non-zero `validate-workspace` after a worker turn, the driver grants a **bounded self-repair
allowance** — up to N *consecutive* repair turns (config `repair-turns`, default 2) whose only job
is making the workspace validate. Green again resets the counter and the engagement resumes where
it was; exhaustion is terminal `validator-failed` with the **original** error preserved in the stop
detail. Reasoning in ADR-0014; harness tests for both the recovery and the exhaustion path; H-022's
status updated with the decision.

Done when: `harness/tests/test_harness.py` green (110 before this unit), `./scripts/check` green,
committed AND pushed.

**Next unit: META-172** — the open-findings sweep and triage.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
