# CHECKPOINT

## Current unit: META-087 — F-013: an epic can be suspended

F-013: three rules that cannot all hold. `open` is `terminal: true`; the only transitions into
`awaiting-answer`/`blocked` are `from: any-non-terminal`; and the validator demands an item with
an open blocking question be suspended — epics included. A skill with a genuine epic-level
impasse has to either lie in the record (`blocking: false`) or leave the workspace invalid. Both
happened, in two separate runs.

Diagnosis: `terminal` is carrying two meanings — "no skill owns this status" and "this status
may not be suspended". `open` is the first and not the second. Separate them.

Steps:
1. `methodology/pipeline.yaml` — every status declares `suspendable`; the two escalation
   transitions read `from: any-suspendable`. `open` stays `terminal: true` (it genuinely has no
   owning skill) and becomes `suspendable: true`. Pipeline version → 0.2.0.
2. `scripts/lint-skills` — `suspendable` is required and must be a boolean; a status that is
   both terminal and suspendable is legal and a status neither owned nor suspendable is the
   real dead end.
3. `scripts/transition`, `scripts/validate-workspace` — `any-suspendable` replaces
   `any-non-terminal`.
4. `spec/ids-and-statuses.md` §4 — the table and a note saying which meaning is which.
5. Prove by execution: the exact command F-013 quotes as refused now succeeds; suspending a
   `done` epic is still refused. Must-fail fixture row for the still-illegal case.
6. Re-render; check green; FINDINGS; journal; commit; push.

Next unit: **META-088** — F-022 (epic sign-off gate).

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
