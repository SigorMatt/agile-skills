# Evidence — a failing hard gate blocks a transition

Acceptance box **B3**: "Each declared quality gate is enforced by an executable mechanism
(script/hook) — demonstrated by a deliberate failing case that blocks the transition."

Reproduce with `meta/evidence/gate-failure-demo.sh [scratch-dir]`. It builds a throwaway
project, installs the rendered skills into it, and runs five checks. Nothing outside the
scratch directory is written.

## What is being demonstrated

| # | Claim | Mechanism |
|---|-------|-----------|
| 1 | A legal transition whose gates pass is allowed. | `scripts/transition` |
| 2 | A transition that is not in `pipeline.yaml` is refused, gates or no gates. | `scripts/transition` |
| 3 | **A failing hard gate refuses the transition, and the item's status is unchanged afterwards.** | `scripts/transition` + `scripts/run-gate` |
| 4 | The edit that would route around the transition script is denied by the guard hook — through the file tool *and* through a shell redirect — while an ordinary source edit is allowed. | `hooks/guard-workspace-writes.py` |
| 5 | Fixing the cause lets the identical command through. The gate is a real check, not a refusal. | `scripts/transition` |

Note on scope for check 4: the hook program is fed the exact JSON payload the runtime sends a
`PreToolUse` hook, and its decision is read from the JSON it prints. That is the whole of the
hook's contribution — the runtime's part is to call it and honour `permissionDecision`, which is
documented behaviour recorded in `meta/adr/ADR-0001-claude-code-skill-format.md`. What is
demonstrated here is that the decision is correct; what is taken from the documentation is that
a `deny` decision blocks the call.

## Transcript

```text
=== install the rendered skills into a fresh project ===
install: 11 action(s)
install: next, initialise the workspace with
           python3 .claude/agile-skills/scripts/workspace-init .

=== 1. a legal transition with passing gates is allowed (draft -> ready) ===
PASS   workspace-valid  (hard)
MANUAL definition-of-ready  (hard)
MANUAL criteria-are-decidable  (hard)
MANUAL qa-recorded-verbatim  (hard)
transition: WI-0001 draft → ready (by refine)

=== 2. an illegal transition is refused (ready -> done) ===
transition: ready → done by 'refine' is not a transition in pipeline.yaml
exit=1
transition: WI-0001 ready → planned (by plan)

=== 3. THE BLOCK: a failing hard gate refuses the transition (planned -> in-progress) ===
transition: refused — a hard gate for 'implement' failed. Fix it, or rerun with --force to record an explicit override in the history reason.
FAIL   tests-pass  (hard)
SKIP   lint-clean  (hard)
PASS   workspace-valid  (hard)
MANUAL every-criterion-has-a-test  (hard)
PASS   commits-reference-the-item  (hard)
MANUAL no-unplanned-scope  (advisory)
status is still: status: planned

=== 4. the hook denies the edit that would route around the gate ===
DENY: Blocked: tracker/items/*/history.md is append-only and is written by .claude/agile-skills/scripts/transition, which checks the transition against pipeline.yaml and runs the acting skill's hard gates first. Run:
DENY: Blocked: tracker/items/*/history.md is append-only and is written by .claude/agile-skills/scripts/transition, which checks the transition against pipeline.yaml and runs the acting skill's hard gates first. Run:
an ordinary source edit: ALLOW (no output)

=== 5. fixing the gate lets the same transition through ===
PASS   tests-pass  (hard)
SKIP   lint-clean  (hard)
PASS   workspace-valid  (hard)
MANUAL every-criterion-has-a-test  (hard)
PASS   commits-reference-the-item  (hard)
MANUAL no-unplanned-scope  (advisory)
transition: WI-0001 planned → in-progress (by implement)
status is now: status: in-progress

=== history, showing only the transitions that were allowed to happen ===
| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-16T21:05:21Z | — | draft | intake | — | created for the demo |
| 2026-08-16T21:05:21Z | draft | ready | refine | — | DoR passed |
| 2026-08-16T21:05:21Z | ready | planned | plan | — | plan.md written |
| 2026-08-16T21:05:22Z | planned | in-progress | implement | — | starting work |

scratch: <a throwaway directory>
```

## Reading the result

The interesting line is in check 3:

```text
transition: refused — a hard gate for 'implement' failed. …
FAIL   tests-pass  (hard)
status is still: status: planned
```

and then in check 5, after the test command is fixed, the same command with the same arguments
produces `transition: WI-0001 planned → in-progress`. The item's `history.md` at the end
contains only the transitions that were allowed to happen — there is no row for the refused
attempt, because nothing was written.

Also visible, and deliberate:

- `SKIP   lint-clean  (hard)` — the project has no lint command, so the gate is reported as
  **skipped**, not as passed. A hard gate that checked nothing must never look like a hard gate
  that passed.
- `MANUAL every-criterion-has-a-test  (hard)` — a `manual_check` cannot be discharged by a
  script. It is reported as MANUAL and the worker must record the evidence in the journal. The
  adapter README's enforcement table lists exactly which gates are in this position rather than
  claiming enforcement that does not exist.
