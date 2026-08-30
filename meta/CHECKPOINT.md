# CHECKPOINT

## Current unit: META-133 — ADR-0009, the retro skill's design

Builder session four (`meta/BUILDER-4-PROMPT.md`) is running: the first gated-track session.
Phase V is laid out in `meta/plan.md`. META-132 (the plan itself) is committed.

**Steps**
1. Write `meta/adr/ADR-0009-retrospective-reading.md`, in ADR-0006/0008's shape: context from
   the banked evidence, then the derivation.
2. It must settle, at minimum: what a retro reads (the workspace record only — no SIM-LOG, no
   harness); that it is read-only over the engagement it audits; when it is dispatched (after
   an ending, before archive, per `pipeline.yaml`); the two output audiences and why they are
   separated; the three-way classification (toolkit defect / this-project circumstance /
   observation) and the misclassification failure mode it exists to prevent; the citation rule;
   and — in ADR-0008 §5's shape — what a lint over a retro can and cannot see.
3. No code in this unit. Derivation only.

**Done when** the ADR is written, `./scripts/check` is still green (it does not read ADRs, but
the tree must be clean), the box is ticked with the commit, the journal entry is written, and
this file is advanced to META-134.

**Next unit:** META-134 — `scripts/lib/record.py`, the shared record model.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**
