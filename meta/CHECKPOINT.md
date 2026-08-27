# CHECKPOINT

## Current unit: META-114 — F-050, part 2: what a deferral does to an epic

META-113 built the mechanism: `rule_obligations` in `pipeline.yaml`, read by
`validate-workspace` and checked against the transition table by `lint-skills`, with two
injected faults and a step that refuses a pipeline which dropped an obligation. That closed the
class and scoped `question.deferred.not-blocked` to the item types the deferral row permits.

**Intent of this unit.** The instance. The validator now says nothing about an epic-level
deferral, and saying nothing is not an answer — `answer-questions` still has to know what to do
when the stakeholder replies "not yet" to a question on an epic. 1e's evidence names it: a
deferred acknowledgment is the E3 impasse, and only `review-close` ends an engagement. So:

- `spec/question.md` §2: on an epic, a deferred blocking question returns the epic to `open`;
  the engagement is ended through the stakeholder by `review-close` once it comes to rest. It is
  not parked at `blocked` by the answerer, because `blocked` on an epic *is* the ending.
- `methodology/skills/answer-questions/process.md` step 3a gains that branch; `skill.yaml`'s
  `a-deferral-is-not-an-answer` gate and exit criteria follow. Version 0.2.0 → 0.3.0 (MINOR: a
  new step).
- Two cases in `scripts/check`'s by-execution step: the move 1e's architect would have made on
  the other branch is **refused** (`transition EP-001 --to blocked --actor answer-questions`),
  and an epic carrying a deferred blocking question at `open` **validates clean**.

## The units of this session

- [x] **META-113** — F-050 part 1: the obligation registry and its gate.
- **META-114** — F-050 part 2: the instance (this unit).
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
  ⇒ a `## Revisions` row **appended in order**. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
