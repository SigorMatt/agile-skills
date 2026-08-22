# CHECKPOINT

## Current unit: META-083 — F-019: the record cannot diverge from the status undetectably

F-019 (`meta/findings/FINDINGS.md`): a `cd` made a relative script path fail mid-chain, the
rest of the chained command ran anyway, and a journal entry plus a tracker commit claimed a
transition that never happened. Three mechanical fixes, per the finding's Direction:

Steps:
1. `scripts/lib/workspace.py` — `find_workspace_root()` / `resolve_root()`: walk up from CWD to
   the directory holding `tracker/project.yaml`. Every script defaults its root to it and says
   on stderr when it resolved somewhere other than CWD.
2. `spec/skill-contract.md` — the transition is a checkpoint: never chained, its exit code gates
   everything after it; scripts are invoked by a path that does not depend on CWD. Rendered into
   every SKILL.md by `adapters/claude-code/render.py`.
3. `scripts/validate-workspace` — `journal.status.unmatched`: every transition a journal entry
   claims under `**Status:**` must have a matching row in `history.md`.
4. Must-fail fixture: a journal entry claiming a transition `history.md` does not carry; code
   added to `fixtures/broken-workspace/EXPECTED-CODES.txt`.
5. Re-render, `./scripts/check` green, FINDINGS.md F-019 → fixed, journal, commit, push.

Done when: check green with the new code in the fixture, and running any script from a
subdirectory of a workspace acts on the workspace, demonstrated.

Next unit: **META-084** — F-017 (mechanical journal-entry provenance).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- This session MAY modify `methodology/`, `spec/`, `scripts/`, `adapters/`, `harness/`.
  It may NOT touch `meta/harness/evidence/**` (read-only history) and may not rewrite filed
  finding text (append corrections instead).
- Every change traces to an F-### or H-###. Anything unfiled gets filed first.
- Behavioural skill change ⇒ version bump in `skill.yaml` (patch for a fix, minor for a contract
  change). Spec change ⇒ append to that spec file's `## Revisions` section. Re-render after any
  of it.
- Every enforcement fix ships a must-fail fixture proving the old failure is now blocked.
- Toolkit commits and harness commits stay separate (two ledgers, two prefixes).
