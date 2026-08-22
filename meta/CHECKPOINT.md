# CHECKPOINT

## Current unit: META-097 — fix what 1d found in this session's own work

Priority order within the unit, worst first:
1. **F-037** — a `[src: ...]` inside an inline code span or a fenced block is a quotation, not a
   citation. Both `lint-claims` and `validate-workspace.check_claim_citations`. Must-fail fixture
   both ways.
2. **F-033** — `lint-claims` must never exit 0 having examined nothing; explicit file arguments are
   linted, not silently treated as a workspace root.
3. **F-044** — `transition` escapes `|` in the reason cell; the validator names an unescaped pipe
   as the likely cause of a mis-shaped row.
4. **F-039** — validate the journal body before the history row is written.
5. **F-025** — `--resolving` carries whether the transition will write the entry, so
   `journal.execution.missing` is downgraded only then.
6. **F-040** — strip a repeated `src:` prefix; say which part failed.
7. **F-041** — skip git-ignored paths.
8. **F-024(b)** — `scripts/check` asserts every commit sha cited in FINDINGS.md is an ancestor of
   HEAD, with an exemption list.
9. **F-032** — a filed question must carry `## Answer` and `## Consequences` from the start.

Then: **META-091** (cluster 4), **META-092/093/094** (cluster 5), **META-101** (FINAL-REPORT-2).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- **Never record a commit sha by amending the commit being cited** (F-024).
- `meta/harness/evidence/**` is read-only; filed finding text is appended to, never rewritten.
- Every change traces to an F-### or H-###. Behavioural skill change ⇒ version bump. Spec change
  ⇒ a `## Revisions` row. Re-render after any of it.
- Every enforcement fix ships a must-fail fixture.
- Toolkit commits and harness commits stay separate.
