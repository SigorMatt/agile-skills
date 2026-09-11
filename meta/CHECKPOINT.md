# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) · META-168 (`656b6c5`) · META-169 (`c8f69b3`) ·
META-170 (`b6ff22f`) · META-171 (`55d7f03`) · META-171b (`68e65fb`).
**47 steps, 110 fixture codes, 419 selftest cases, 195 harness tests.**

**Current unit: META-172 — the small batch and the triage sweep.**

Steps:
1. File the three defects this session's units found on the way, each with the status it actually
   has: the `run:` *records a command with no outcome* message was unreachable and a malformed
   `run:` citation would have been softened by META-168's change (found and fixed in META-168); a
   failed adapter render wipes `dist/` before it validates (found in META-170, **not** fixed); the
   pruned-directory tuple was written out by hand in two places and had already drifted (found and
   fixed in META-169).
2. Sweep the open-findings set. Anything TRIVIALLY adjacent to clusters 1-3 may be taken — say so
   per finding. Everything else gets a dated triage line. No status stale. F-098 is the one whose
   price this session changed: ADR-0013's `toolkit:` prefix is the mechanism its Direction asked
   for, and its cost is still the 97-citation sweep.
3. Confirm cluster 4's first bullet is already discharged — the H-022 correction was appended by
   the owner's staging pass at `9d31ce1` — and say so rather than appending a second one.

Done when: `./scripts/check` green (steps 17b and 17c are the ones this unit can break),
committed AND pushed.

**Next unit: META-173** — stage `iteration-5r-envel`, provision-verify, tear down. **NOT run; the
probe is NOT read.**

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
