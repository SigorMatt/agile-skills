# CHECKPOINT

## Current unit: META-113 — F-050, part 1: `applies_to` completeness becomes a gate

Phase III is builder micro-session 2.6 (`meta/BUILDER-2.6-PROMPT.md`): the three findings
FINAL-REPORT-2.5 §9 named as conditions on the iteration-2 go, and nothing else. Scope is
closed — anything new is filed and left open.

**Intent of this unit.** F-050 is F-013's shape in this repo's own work: a validator rule that
names a status was written for every item type while the transition that satisfies it was scoped
to two of them, so an epic-level deferral produced a workspace no legal move could repair. The
instance is one line; the class is what the mission asks for. So this unit builds the mechanism
first:

- `methodology/pipeline.yaml` gains a `rule_obligations:` block. Each entry names a validator
  rule that requires an item to be at one of a fixed set of statuses, the item types it applies
  to, and the transition that must be legal for those types if the rule is to be satisfiable.
- `scripts/validate-workspace` **reads** the obligation's `applies_to` rather than deciding for
  itself which item types a status rule constrains, and reports `pipeline.obligation.missing`
  when an obligation it depends on is absent.
- `scripts/lint-skills` checks each obligation against the transition table in both directions:
  a transition the obligation names and no row provides (`obligation.unsatisfiable`), and a
  scope the rule claims and the transitions do not permit (`obligation.applies_to.mismatch`) —
  which is F-050 exactly, and, in the other direction, F-013.
- Two injected faults in `scripts/check`'s pipeline-invariant step, one per code.

META-114 then fixes the instance: the epic branch of the deferral, in the spec and in
`answer-questions`, with the by-execution must-fail case.

## The units of this session

- **META-113** — F-050 part 1: the obligation registry and its gate (this unit).
- **META-114** — F-050 part 2: the instance — spec, `answer-questions`, by-execution fixtures.
- **META-115** — F-049: the `**Status:**` bullet, all occurrences, plus the class check if cheap.
- **META-116** — F-055: name `git worktree add --detach` in `review-close`, with the must-fail case.
- **META-117** — findings statuses with citations that resolve, `./scripts/check` green,
  `meta/FINAL-REPORT-2.5.md` §11.

Then **stop**. Do not run iteration 2 — the owner launches it.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work, then
  record the sha in a follow-up commit.
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
- **From F-050:** when you add a rule, enumerate the item types it applies to, and check it
  against the transitions that are legal for each. This session's job is to stop that being a
  thing a person has to remember.
