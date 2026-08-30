# CHECKPOINT

## Phase V is complete. There is no next unit in this session.

Builder session four (`meta/BUILDER-4-PROMPT.md`) is done: META-132 through META-143, committed
and pushed. `./scripts/check` is green across **30 steps**; `harness/tests/test_harness.py` is 74
tests; `scripts/lib/selftest.py` is 252 cases; `fixtures/broken-workspace` is **82 codes,
unchanged**, which is the record-model migration's proof.

**What was built.** `retro` 0.2.1 — the ninth skill, derived first in
`meta/adr/ADR-0009-retrospective-reading.md`, specified in `spec/retro.md`, gated by
`scripts/lint-retro` against `fixtures/retro/`, and dispatched by `next` 0.4.0 on
`engagement-state`'s new `ended` / `closed` distinction. Plus `scripts/lib/record.py`, the shared
record model every lint now reads, and cluster 3's three fixes.

**What the tests said.** Ground truth: **1 full hit, 2 partial, 2 misses** of five
workspace-visible findings, the marquee case among the misses. Precision: 28 proposals, nine
verified in depth, **zero unfounded**. Live dispatch: `next` → `retro` → `closed`, two files
written, verified by mtime. `meta/FINAL-REPORT-4.md` §4 and §5 carry both, with the re-run's
better number disclaimed wherever it appears.

## What the owner does next

`meta/ROADMAP.md`'s 2026-08-30 §3 stamp names three things, in order:

1. **Run the retro inside a live harness iteration** — the one thing no banked record tests,
   because a live workspace has the product source and the commit history that a banked copy
   does not.
2. **Triage the thirty-seven proposals** in `meta/evidence/retro-calibration/`. They are the
   first output of the feedback engine and nobody has read them as a backlog. Its README names
   the four worth reading first.
3. **A held-out engagement**, if a real recall number is wanted. This session cannot supply one:
   the procedure was changed after reading the miss.

**F-076 is the finding to carry forward.** It joins the *document-as-deliverable* class (F-057,
F-058) and turns it into a question with two answers that cannot both be right — either
`spec/doc-header.md` §5 holds and `implement`'s claims gate does not belong on it, or §5 does not
hold and the gate is right to be there. That is an ADR-0006-shaped derivation, not a patch.

Findings, of 95 filed: F-079 and H-019 are the newest. Still open or deferred: **F-076** (new,
deferred with its gate named), F-061 (open observation, now with the mechanism the retro found),
the *half-written record* class (F-036, F-043, F-051, F-053) and *document-as-deliverable*
(F-057, F-058), F-008 and F-030 behind their named gates.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
