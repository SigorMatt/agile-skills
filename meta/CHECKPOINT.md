# CHECKPOINT

## Current unit: META-120 — enforcement for ADR-0008

**Session:** builder 3 (`meta/BUILDER-3-PROMPT.md`). Phase IV of `meta/plan.md`.
**Derivation done:** `meta/adr/ADR-0008-cross-answer-consistency.md` (META-119, pushed).

**Intent.** Build the mechanical half of ADR-0008 §4 — obligations 1, 2 and 3 — and nothing
else. Contracts and version bumps are META-121.

1. `scripts/lib/scope.py` — one answer to "could this diff window contain anything?", shared
   with `lint-claims` in META-123. A window that cannot contain this execution's work is
   **degenerate** and its gate FAILS; a real window with nothing in it passes and says so.
2. `scripts/lint-answers` — at rest: `## Cross-answer check` present and shaped on every
   consumed human answer, and a declared conflict matched by a question citing both IDs. Over a
   diff: a claim sourced to a human answer whose text this execution changed needs either that
   question or a `**Cross-answer check:**` journal bullet naming the answer.
3. `spec/question.md` — the `## Cross-answer check` section, its shape, and why it is written by
   the consuming skill and not by the person.
4. Fixtures both ways, wired into `./scripts/check`: the iteration-3 shape (an answer consumed
   with no check; a conflict declared and never escalated; the human's own sentence rewritten
   without a question) must fail, and a clean engagement must pass.

**Not in this unit:** skill.yaml gates, version bumps, re-render.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
