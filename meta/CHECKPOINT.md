# CHECKPOINT

## Current unit: META-121 — F-066, a claims gate that cannot pass vacuously

**Session:** builder 3 (`meta/BUILDER-3-PROMPT.md`). Phase IV of `meta/plan.md`.
**Done and pushed:** META-119 (ADR-0008), META-120 (`lint-answers`, `scope.py`, fixtures).

The plan's Phase IV was reordered after META-120: the two script-scope fixes and the two spec
changes land first, and **all** skill contracts are re-derived in one pass (META-124) so each
skill takes one version bump rather than three.

**Intent.** `scripts/lint-claims --changed-since main` at an epic ending compares `main` with
`main`, prints "checked no documents" and exits 0. Iteration 4's reviewer: *"It passed here, but
it would have passed over anything."* `scripts/lib/scope.py` already knows the difference between
a window that is empty and one that could not have seen anything; apply it.

1. `lint-claims` refuses a degenerate window (`claim.scope.degenerate`) instead of passing over
   it, and always prints the scope it actually had — both rules, not only rule 2.
2. An explicit named scope stays available and becomes the ending's contract: `--all`.
3. Must-fail and must-pass cases in `./scripts/check`, built in a throwaway repository:
   the F-066 shape refused, a real-but-empty window still a pass, `--all` at the same commit
   still a real scope.

**Not in this unit:** the gate command in any `skill.yaml` (META-124), F-067's repair path
(META-122).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
