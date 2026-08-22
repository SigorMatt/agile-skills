# CHECKPOINT

## Current unit: META-088 — F-022: an epic cannot close without stakeholder acceptance

F-022: both 1b and 1c closed EP-001 with no sign-off ever addressed to the human. The DE gates
check the record, and the record only holds what the stakeholder said when last consulted. Every
real agile process has a product-owner acceptance moment; this one had none.

Steps:
1. `spec/question.md` — optional frontmatter `kind`: `decision` (default) | `sign-off`, and the
   shape a sign-off must have (goal restated, delivered vs deferred, the explicit ask).
2. `spec/dor-dod.md` — epic Definition of Done gains **DE7**: an answered sign-off question,
   filed after the last child closed.
3. `scripts/check-epic-signoff` — the mechanical half: on an epic, require a `kind: sign-off`
   question addressed to `human`, answered, with a non-empty `## Answer`, `created` no earlier
   than the last child's move to `done`. On anything that is not an epic, pass and say why.
4. `review-close` — hard gate `epic-sign-off`; step 10 files the sign-off, suspends the epic to
   `awaiting-answer` (possible since META-087) and stops; the next pass closes it. Minor bump.
5. `scripts/validate-workspace` — `question.kind` and `question.signoff.addressed`.
6. Fixtures both ways; prove by execution that a `done` move is refused before sign-off and
   allowed after.
7. Re-render; check green; FINDINGS; journal; commit; push.

Next unit: **META-089** — F-021 (a stakeholder-initiated request, routed by `next`).

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
