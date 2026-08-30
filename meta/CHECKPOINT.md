# CHECKPOINT

## Current unit: META-140 and META-141 — the two tests, in flight

META-132..139 are committed. `./scripts/check` is green across **29 steps**;
`harness/tests/test_harness.py` is 74 tests, OK.

**META-140's ground-truth subset is written and committed** (journal, 2026-08-30, "the
ground-truth subset, written before anything ran"). It must not be revised after seeing results:
five workspace-visible findings — F-061, F-062, F-063 (bar lowered, with the reason recorded),
F-064, F-065 — out of ten filed across iterations 2 and 3, plus three positive-record targets.
The five excluded are all harness findings whose evidence is a run transcript, a driver log or
the sim's own skill file.

**In flight** — three context-free subagents, each confined to its own scratch directory under
`.../scratchpad`:
- `gt/iteration-2` and `gt/iteration-3` — the rendered `retro` skill run against a banked
  engagement (META-140).
- `live` — `next`, then whatever it dispatches, then `next` again, over recall-4c's workspace
  (META-141).

Each scratch copy carries a `RECORD-NOTICE.md`: the product source and the commit history were
never banked, so `workspace-valid` fails on `claim.citation.unresolved` for that reason and no
other, and the installed contracts are newer than the versions the record names.

**If this session is resumed with the agents gone:** re-run them. The setup is reproducible —
copy `meta/harness/evidence/<iteration>/{tracker,docs}` into scratch, run
`python3 adapters/claude-code/install.py <scratch>`, write the notice, and dispatch a
context-free subagent with the workspace path and nothing else.

**Done when** both tests are read and journaled — the rediscovery fraction and the noise count
stated and judged honestly, and the live dispatch shown end to end with `engagement-state`
reporting `closed`.

**Next unit:** META-142 — the findings pass over both tests.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
