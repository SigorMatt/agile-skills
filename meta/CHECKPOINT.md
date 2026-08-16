# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Current phase: META-021..028 — the eight skills

One skill per unit, one commit per skill. Each unit writes
`methodology/skills/<name>/skill.yaml` + `process.md`, then journals and commits. No linter
exists yet (META-031), so each unit ends by parsing the new `skill.yaml` with
`python3 scripts/lib/miniyaml.py`-based check and re-running `scripts/lib/selftest.py`, whose
cross-check now covers every YAML file in the repo.

Order and current position: **META-021 `intake`** → 022 `refine` → 023 `plan` → 024 `implement`
→ 025 `verify` → 026 `review-close` → 027 `answer-questions` → 028 `next`.

**What every skill unit must satisfy**
1. `skill.yaml` conforms to `spec/skill-contract.md` §1 — all required fields, no unknown keys,
   `dispatch.on_status` consistent with `methodology/pipeline.yaml` `statuses[].owner`.
2. `process.md` has the five required sections in order (`spec/skill-contract.md` §2.1), its
   first step re-reads item state from disk, its last step is the transition *after* journaling,
   and `## Self-check` names ≥ 2 specific failure modes for that role.
3. No runtime, vendor, tool, or product name appears anywhere in either file.
4. `python3 scripts/lib/selftest.py` exits 0 (it cross-checks the new YAML against PyYAML).
5. Journal appended, plan ticked, tree clean.

**Next unit after META-028:** META-031 — `scripts/lint-skills`, which turns rules 1–3 above
from a habit into a gate.
