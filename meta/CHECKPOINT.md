# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) · META-168 (`656b6c5`) · META-169 (`c8f69b3`) ·
META-170 (`b6ff22f`) · META-171 (`55d7f03`) · META-171b (`68e65fb`) · META-172 (`73223e2`).
**47 steps, 110 fixture codes, 419 selftest cases, 195 harness tests, 139 findings entries.**

**Current unit: META-173 — stage the envel re-run. It is NOT run here.**

Steps:
1. `harness/iterations/iteration-5r-envel.json` — a copy of `iteration-5-envel.json` with
   id `iteration-5r-envel` and project `envel-2`. **Nothing else changed**, the probe field
   included.
2. Provision-verify it in a throwaway path and tear it down, leaving nothing behind.
3. **The held-out rules from builder five apply verbatim: do not run it, and do not read the
   probe — existence checks only (`isfile` + `getsize`, never the contents).**

Done when: the config is committed AND pushed, the throwaway path is gone, and the unit's report
carries the evidence for both attestations.

**Next unit: META-174** — `meta/FINAL-REPORT-6.md` and the session close.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
