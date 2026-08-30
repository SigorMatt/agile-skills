# CHECKPOINT

## Current unit: META-142 — the findings pass, then META-143 — the final report

META-132..141 are committed. `./scripts/check` is green across **30 steps**;
`harness/tests/test_harness.py` is 74 tests; `scripts/lib/selftest.py` is 252 cases.

**Both tests are done and read.**
- **META-140, the ground-truth reading:** scored against the subset written and committed
  *before* the runs — **1 full hit, 2 partial, 2 misses** of five workspace-visible findings;
  strictly 1/5, with partials at half credit 2/5. The marquee case (F-062) was **missed** and the
  journal says so. Precision is the strong half: 28 proposals, nine verified in depth against the
  current kernel, **zero unfounded**. Reports banked verbatim in
  `meta/evidence/retro-calibration/`.
- **META-141, the live test:** `next` dispatched `retro` at step 7 on the `ended` verdict, the
  report filed, `next` then reported `closed` and stopped. Only two files were written, verified
  by mtime.

**Filed since:** F-075 (a quoted citation read as a real one — found by the live test, fixed),
F-076 (a claims window empty by construction — verified, **deferred** to the
document-as-deliverable derivation), F-077 (`path:line` unbounded — fixed), F-078 (the retro's
own calibration defect — fixed in `retro` 0.2.0), and an addendum to F-061 recording that the
retro answered the question that entry was holding open.

**In flight:** one context-free subagent re-running `retro` **0.2.0** over `gt2/iteration-3`.
It is a check that 0.2.0's new instruction is followable, **not** an independent measurement —
the change was made after reading the miss, and everything written about it must say so.

**What remains**
1. Finish META-142: a positive record for the retro's first runs, and statuses current.
2. META-143: `meta/FINAL-REPORT-4.md`, and the ROADMAP §3 stamp for the retro track.

**Next unit:** META-143.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
