# CHECKPOINT

## Current unit: META-124 — the contracts, once

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..123 done and pushed.

**Intent.** Every skill contract re-derived from ADR-0008 and the three spec changes, in one
pass, so each skill takes **one** version bump rather than three.

Two script changes come first, because the gate commands depend on them:

- `--context <item-type>` on `lint-claims` and `lint-answers`. An **ending** is not an execution
  and has no diff of its own, so at `--context epic` the scope is the whole document set — which
  is F-066's fix stated where the mission puts it, *explicit per context*.
- `--uncommitted` on both, for a skill that works on the trunk and commits once at the end
  (`plan`). Its honest window is the working tree, not a diff against the branch it is standing
  on — and a diff against the branch it is standing on is exactly the degenerate window F-066 is
  about.

Then the contracts: `intake` (the elicitation question), `refine` (prior human answers in the
contradiction check; presentation order; how a "still holds" criterion is written), `plan`,
`implement` (the refused move), `verify` (how a "still holds" criterion is assessed),
`review-close` (the ending's scopes, DE8, the §4b repair path), `answer-questions` (writes the
cross-answer check). Version bumps, `lint-skills`, re-render.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
