# CHECKPOINT

## Current unit: META-119 — ADR-0008, cross-answer consistency

**Session:** builder 3 (`meta/BUILDER-3-PROMPT.md`), the proven-kernel push. Phase IV of
`meta/plan.md`.

**Intent.** Derive, before any code, the obligation that gives the stakeholder a seat in
conflicts between their own recorded answers (F-062) — the queue's sharpest lesson, where a
planted contradiction was detected twice, named "false", and repaired unilaterally while the
sim held a one-line reconciliation in reserve nobody asked for.

`meta/adr/ADR-0008-cross-answer-consistency.md` must settle:

1. What counts as a **recorded human answer** (the question record, `refinement-qa.md` `[human]`
   entries, a sign-off condition, a stakeholder request).
2. When a new answer, criterion, or sign-off condition **touches** a prior one — the test must be
   mechanical enough to lint and honest about its blind spots.
3. The two legal moves: cite compatibility, or file a question quoting both answers by ID and
   asking which wins.
4. The **refused move**: repairing a stakeholder-sourced falsehood in `docs/` without a question
   to its author. Say which half is a hard gate and which is a contract rule.
5. What the lint can and cannot see — stated in the ADR, not implied.

**Not in this unit:** any script, any skill version bump. Derivation only.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
