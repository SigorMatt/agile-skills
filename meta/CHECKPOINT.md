# CHECKPOINT

## Current unit: META-134 — `scripts/lib/record.py`, the shared record model

Phase V is laid out in `meta/plan.md`. META-132 and META-133 are committed (ADR-0009 is the
retro skill's design; read it before this unit — §6 and §7 name what `lint-retro` will need).

**Steps**
1. Write `scripts/lib/record.py`: one parser for the workspace's record *structures*, so that
   rules about a record's shape stop being reimplemented per script (F-069, F-073's class,
   FINAL-REPORT-3 §6.3). At minimum it must model, with line spans:
   - **blocks** inside a section: a bullet **with its continuation lines**, a labelled
     declaration (`Label: ...`) **with its continuation lines**, a paragraph, a table, a fenced
     block — the two shapes F-073 got wrong, in one place;
   - the ledger/report **entry** shape (a `##`/`###` heading with labelled bullets under it),
     which `lint-retro` will read.
2. Cases in `scripts/lib/selftest.py`, taken from F-069 and F-073's own fixtures: a bullet that
   wraps, a bullet followed by unindented closing prose, a declaration that wraps over four
   lines, a declaration ended by a bullet, a fenced block that must not be read as prose.
3. No caller changes in this unit — the migration is META-135, so that "behaviour-identical"
   has a commit boundary it can be proved across.

**Done when** `python3 scripts/lib/selftest.py` passes with the new cases, `./scripts/check` is
green (28 steps, unchanged codes), the box is ticked, the journal entry is written, and this
file is advanced to META-135.

**Next unit:** META-135 — migrate `lint-answers`, `lint-claims` and `validate-workspace` onto
the model; the 82 broken-workspace codes unchanged is the proof.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
