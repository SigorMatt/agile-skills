# CHECKPOINT

## Session: builder 2.5 (`meta/BUILDER-2.5-PROMPT.md`). Phase II is running.

Read `meta/BUILDER-2.5-PROMPT.md`, then `meta/plan.md` § Phase II, then this file.

## Current unit — META-112 — the final report

`meta/FINAL-REPORT-2.5.md` §§1–5 are drafted (commit `4a9e15f`-ish, see git log for META-110).
Finish it:

- **§6 What 1e proved**, and what it did not. The headline is the epic's three history rows. Say
  plainly what was *not* exercised (`status: deferred`, the DoR override).
- **§7 What 1e found** — F-049…F-060 and H-008, with F-050 named as this session's own defect.
- **§8 ROADMAP §2, an honest read** — three conditions, each judged against 1e.
- **§9 Go / no-go for iteration 2.** `iteration-2-tidy` runs only on a go. Say which, and why.

Done when: the report is complete and committed, plan ticked, journalled, checkpoint closed.

## Next unit — none. Phase II ends here.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** `origin` is
  `git@github.com:SigorMatt/agile-skills.git`; `main` tracks it.
- **Never record a commit sha by amending the commit being cited** (F-024). Commit the work, then
  record the sha in a follow-up commit. `scripts/check` step 9 enforces this.
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **Do not modify the toolkit while a harness run is in flight.** An uncommitted change under
  `methodology/`, `spec/`, `scripts/`, `adapters/`, `examples/`, `fixtures/` or the top-level docs
  trips the harness's own W4 rule and stops the run. `meta/` and `harness/` are exempt.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump in
  `skill.yaml`. Spec change ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture, and — where a rule could be satisfied
  vacuously — a fixture proving it can be passed.
- Toolkit commits and harness commits stay separate.
