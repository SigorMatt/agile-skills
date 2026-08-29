# CHECKPOINT

## Current unit: META-123 — F-065, F-063, F-064 in the spec, with what enforces them

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..122 done and pushed.

**Intent.** The three spec changes the contracts (META-124) then carry, each with the mechanical
half it can honestly have:

1. **F-065** — `spec/dor-dod.md`: a criterion *about other criteria* ("every AC of WI-0001..0003
   still holds") is assessed against those criteria's **text**. The test suite is evidence for
   the answer, never its definition. Where the domains do not intersect in anything executable,
   the non-intersection is stated and a covering case is added or waived by name. Contract-level;
   no program can read whether two sentences still agree.
2. **F-063** — `spec/question.md`: options first, recommendation last and marked as the team's
   preference; no recommendation in `## Context` or `## Question`. Lintable, and linted
   (`validate-workspace`).
3. **F-064** — `spec/question.md`: `kind: elicitation`, the one open question per engagement that
   is not about the team's agenda. Presence-checkable, and checked at the ending
   (`check-epic-signoff`, DoD **DE8**) — with `review-close` always able to file one, so the
   rule can never deadlock an engagement that forgot it.

Must-fail cases for 2 and 3 in `fixtures/broken-workspace` and `fixtures/ended-engagement`;
must-pass in `examples/toy-project` and the clean engagements.

**Not in this unit:** the skill contracts themselves (META-124).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
