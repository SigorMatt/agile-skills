# CHECKPOINT

## Current unit: META-139 — cluster 3, the small fixes

META-132..138 are committed. The retro skill exists end to end: ADR-0009, `spec/retro.md`,
`methodology/skills/retro/` 0.1.0, `next` 0.4.0's dispatch step, `scripts/lint-retro` and
`fixtures/retro/`. `./scripts/check` is green across **29 steps**. `scripts/lib/record.py` is the
shared record model and every lint reads it.

**Steps** — three fixes, and this unit yields first if the budget runs short.
1. **H-017**, harness: the driver stamps the turn number into the HARNESS-STATUS contract and
   rejects (records "no status written") a status file whose heading does not match the turn
   just run. Companion, toolkit side: `board-gen`'s "board already current" notice goes to
   stdout, not stderr. **Separate commits** — toolkit and harness never share one.
2. The stale `max-turns: 24` in `harness/iterations/iteration-4-recall.json`.
3. The inert `*.1` run directories: a terminal marker or a driver startup sweep if it is cheap;
   otherwise file the H-finding properly and defer it with the gate named.
4. File anything new; do not fix silently.

**Done when** `./scripts/check` and `harness/tests/test_harness.py` are green, H-017's status is
current in the ledger, the box is ticked, the journal entry is written, and this file is advanced
to META-140.

**Next unit:** META-140 — the ground-truth test. Write the honest workspace-visible subset into
the journal **before** running anything.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
