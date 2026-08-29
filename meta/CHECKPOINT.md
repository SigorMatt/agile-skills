# CHECKPOINT

## Current unit: META-122 — F-067, the legal repair for a standing ADR

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..121 done and pushed.

**Intent.** `lint-claims --all` finds three `claim.unsourced` in iteration 4's `ADR-0002`. The
reviewer verified all three true against the code. Adding the citation is an edit; ADRs are
superseded-only; superseding one to add provenance is disproportionate — so *"no legal move
clears it"*, and the ledger carries a permanent known-unfixable lint error class.

The repair, per ADR-0008's neighbour reasoning and the consumer run's own ADR-0009:

1. `spec/doc-header.md` §4b — a standing ADR may be repaired **without supersession** in exactly
   two ways, `provenance` and `erratum`, each recorded as an entry in a new append-only
   `## Corrections` section. Anything that changes what the code must do is a new decision and
   §4's supersession rule applies with full force. §5's table cell changes to match.
2. `scripts/validate-workspace` — the shape: every correction entry carries a resolving citation
   and names its kind; an erratum quotes the removed text; a corrected ADR is still `accepted`;
   the change log has a row per correction.
3. `fixtures/adr-correction/` — iteration 4's instance reduced: the ADR **before** (three true,
   unsourced absolutes) and the same ADR repaired through the new path, asserted by execution in
   `./scripts/check` — the defect is found, the repair clears it, and a malformed repair does not.

**Not in this unit:** the skill contracts that name the path (META-124).

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- `./scripts/check` green before every commit; every enforcement change ships a must-fail case.
