# CHECKPOINT

## Builder session six is RUNNING. Mission: `meta/BUILDER-6-PROMPT.md`; plan: `meta/plan.md` Phase VII.

**Done so far.** META-167 (`cd00504`) one mask for every citation surface · META-168 (`656b6c5`)
severity follows knowledge + check step 6a · META-169 (`c8f69b3`) ADR-0013, a toolkit source is
quoted and attributed · META-170 (`b6ff22f`) the grammar placed in seven skills + check step 15d ·
META-171 (`55d7f03`) ADR-0014, the bounded self-repair allowance. **47 steps, 110 fixture codes,
419 selftest cases, 191 harness tests.**

**Current unit: META-171b — the preserved original error must name the defect (harness commit).**

META-171 implemented ADR-0014's promise that an exhausted allowance stops with *the original
error* preserved, then found the promise only nominally kept: `scan_project` keeps
`(...).split("\n")[-1:]` of the validator's output (`harness/run_iteration.py:354`), so the
preserved detail is the summary line — `validate-workspace: 1 error, 0 warnings` — which names no
defect. Iteration 5's whole value was that the *first* error was the finding; a terminal stop that
cannot say which line failed loses exactly that.

Steps: widen what the driver keeps of the validator's output to enough lines to name the failing
findings, in whatever shape leaves the existing stop details intact and truthful; test that an
exhausted allowance's detail names the *original* failing line, not the summary; ADR-0014's
Consequences and H-022's status updated to say the deferral was taken rather than left.

Done when: harness tests green, `./scripts/check` green, committed AND pushed.

**Next unit: META-172** — the open-findings sweep and triage, including the three defects this
session's units found on the way (the unreachable `run:` outcome message, the render that wipes
`dist/` before it validates, and the pruned-directory tuple that had already drifted).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5r is staged in META-173 and is NOT run here; its
  probe is NOT read.
