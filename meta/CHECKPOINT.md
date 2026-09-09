# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model for this session (binding, from the mission): every unit is executed by a
**dedicated sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this
file, and each unit's verdict. Per unit: checkpoint the intent → dispatch the sub-agent with
scope, files to read, definition of done, and the obligation to commit AND push → verify
cheaply (git log for the sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## Current unit

**META-145** — `meta/adr/ADR-0010-document-as-deliverable.md`.

- Steps: enumerate document kinds × lifecycle events; derive the authority-and-obligation
  table and the claim taxonomy; re-check F-076, F-087, F-093, F-095, F-053-class, F-092,
  F-057, F-058 against the derived model as fixtures; state costs and rejected alternatives.
- Done when: the ADR exists in the ADR-0006 shape (Context → numbered derivation sections →
  historical cases → costs → alternatives rejected), every named finding has a row in the
  historical-cases section, `./scripts/check` still green (docs only), committed AND pushed.
- Derivation only. No spec edits, no code, no findings-status edits — those are META-146..149.
- Next unit: **META-146** (spec/doc-header.md + spec/dor-dod.md carry the derivation).

## Done this session

- **META-144** — Phase VI laid out in `meta/plan.md` (commit 2c4b0b7).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
