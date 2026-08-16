# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Current unit: META-010 — `spec/README.md` + `spec/ids-and-statuses.md`

**Why:** every other artifact in the build refers to IDs and statuses. Fixing them first stops
`pipeline.yaml`, the skills and the validators from each inventing their own vocabulary.

**Steps**
1. `spec/README.md` — index of the spec files, the normative-language convention (MUST/SHOULD),
   and the rule that `spec/` is the single source of truth that skills and adapters cite.
2. `spec/ids-and-statuses.md` — ID formats and allocation rule; the tracked-item types; the
   status set per type with the owning skill and terminal flag; the legal transition table with
   the actor skill for each; priority values and their rank.
3. Write `meta/adr/ADR-0003-tracker-layout-and-id-allocation.md` for the two decisions that are
   not forced by the seed: epics/work-items/bugs share one uniform `tracker/items/<ID>/`
   directory shape, and IDs are derived from the filesystem rather than a counter file.
4. Commit `spec: IDs, item types and the status graph (refs META-010)`.

**Done criteria**
- Both spec files exist; no runtime name (the word for any specific agent CLI) appears in them.
- Every status listed has either an owning skill or is marked terminal.
- Every transition names the actor skill.
- ADR-0003 committed; plan ticked; journal appended; tree clean.

**Next unit:** META-011 — `spec/work-item.md`.
