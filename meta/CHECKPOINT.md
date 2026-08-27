# CHECKPOINT

## META-118 is complete. There is no next unit.

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

Done, in commits `e81582d` and `2cd1a65`:

- `strip_heredoc_bodies()` in `harness/audit.py`, wired into `_paths_in`.
- Two tests, both confirmed to fail with the fix reverted — the synthetic shape and
  `test_iteration_2_tidy_turn_6_is_clean`, which audits the **real** transcript with `exists`
  pinned to "every path is real" so it asserts the structural rule rather than the existence
  filter it replaces. **55 tests**, was 53. `./scripts/check` green.
- **H-009** filed in `meta/findings/FINDINGS.md`, fixed, with the residual hole stated rather
  than buried: a read of an outside path performed *inside* a heredoc body (`bash <<'EOF'`, or
  a python program in one) is no longer visible to the transcript scrape.

## What the owner does next

**`iteration-2-tidy` is stopped at turn 6** with `stop-reason: contamination`, and that stop is
a verdict rather than an interruption. The violation it stopped on is not one, and the rule that
produced it is fixed — so the run is resumable on its merits, but restarting it is the owner's
call and was deliberately not done here. The project is
`/home/msi/agile-skills-throwaway/tidy`; `next-role` is `worker`.

Findings: **50 fixed, 15 open**, 1 rejected, 1 deferred.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- **A harness run is in flight.** `meta/` and `harness/` are exempt from the W4 rule; everything
  else trips it — so touch nothing outside them.
- Toolkit commits and harness commits stay separate.
