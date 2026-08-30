# CHECKPOINT

## Current unit: META-136 — `spec/retro.md`, the retro report and the proposal format

META-132..135 are committed: Phase V is planned, ADR-0009 is the design, `scripts/lib/record.py`
is the shared record model and every lint now reads it (F-074 filed and fixed along the way).
**Read `meta/adr/ADR-0009-retrospective-reading.md` before this unit** — §4 (two audiences),
§5 (the classification and its two required fields), §6 (citations reuse `doc-header.md` §4a's
seven forms) and §7 (non-vacuity) are what this spec writes down.

**Steps**
1. Write `spec/retro.md`: the schema of `tracker/items/<EP>/artifacts/retro.md` — required
   sections in order, the observation format, the PROPOSED proposal format with its required
   fields, the classification's closed set, the citation rule, and the `## What was read` scope
   declaration.
2. Add it to `spec/README.md`'s index and to `SPEC_TO_SHIP` in the renderer.
3. Add `process-analyst` to `spec/skill-contract.md`'s persona enum (ADR-0009 §9) and to
   `scripts/lint-skills`' persona list, with the revision row.
4. No skill and no lint in this unit.

**Done when** `./scripts/check` is green, the box is ticked, the journal entry is written, and
this file is advanced to META-137.

**Next unit:** META-137 — `methodology/skills/retro/`, the pipeline dispatch, the re-render.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
