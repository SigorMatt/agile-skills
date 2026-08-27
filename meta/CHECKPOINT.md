# CHECKPOINT

## Current unit: META-118 — H-009, a W3 false positive on a heredoc body

Iteration 2 (`iteration-2-tidy`) is **in flight and stopped** at turn 6 on a contamination
violation that is not one. Scope is one finding; the run is **not** to be resumed here — the
owner does that.

**What happened.** Turn 6's worker wrote a bug report into
`tracker/items/BUG-0002/item.md` with `python3 - <<'PYEOF'`, and the document it wrote contains
the sentence *"Anything scripting the tool — `tidy ~/Downloads --apply && notify-send done` —
silently treats a completely successful run as a failure there."* `HOME_PATH_RE` scraped
`~/Downloads` out of the command string; `/home/msi/Downloads` exists on this machine, so
`plausible()`'s existence filter passed it, and W3 fired on prose.

This is the same class as the false positive the existence filter was written for (a question's
`## Context` quoting the stakeholder's own folders) — one step further in: the path is real, so
existence cannot separate the document from the command.

**The fix.** `harness/audit.py` strips heredoc bodies from a Bash command string before scraping
paths out of it. The command line itself — `cd`, redirect targets — is still scraped; only the
document between the introducer and its delimiter is treated as content. W1 and W2 are
unchanged: they read the whole blob, and writing a forbidden token into a document is still
evidence.

- Regression test named after this run, reading the **real** transcript at
  `harness/runs/iteration-2-tidy/turns/006-worker.stream.jsonl`.
- The residual hole gets said plainly rather than papered over: a read of an outside path
  performed *inside* a heredoc body (`bash <<'EOF'`, or a python program in one) is no longer
  visible to the transcript scrape.
- File **H-009** in `meta/findings/FINDINGS.md`, evidence: that transcript and this stop.
- Run `harness/tests/test_harness.py`. Commit, push, **stop**.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **A harness run is in flight.** `meta/` and `harness/` are exempt from the W4 rule; everything
  else trips it — so touch nothing outside them.
- Toolkit commits and harness commits stay separate.
