# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model for this session (binding, from the mission): every unit is executed by a
**dedicated sub-agent**. The orchestrator session holds only the mission, `meta/plan.md`, this
file, and each unit's verdict. Per unit: checkpoint the intent → dispatch the sub-agent with
scope, files to read, definition of done, and the obligation to commit AND push → verify
cheaply (git log for the sha, `./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## Current unit

**META-146** — `spec/doc-header.md` and `spec/dor-dod.md` carry ADR-0010's derivation.

The six spec-level to-dos ADR-0010 left, verbatim from its own reckoning:

1. `doc-header.md` §5's final paragraph — "`implement` and `verify` do not write to `docs/`" —
   is replaced by ADR-0010 §3.4's rule. §5's created-by/updated-by table stays.
2. `doc-header.md` §4a gains the second obligation (a **quantified** claim needs member
   enumeration recorded in the audit row) and the K8 delimiter convention.
3. `dor-dod.md` D7 becomes a confirmation against `plan`'s invalidation set — scope becomes
   "touched **or** named by the plan".
4. `dor-dod.md` D12 and DE6: the audit row gains the enumeration columns, and both are scoped
   to exclude K8 (engagement-state) sentences.
5. `dor-dod.md` DE4 gains the ending's restatement of every delimited K8 section.
6. `dor-dod.md` §3 gains one D-criterion: `binding-adrs` completeness, owned by `review-close`.

- Done when: all six land, each spec file's **Revisions** table gains a row citing ADR-0010 and
  the findings, `./scripts/check` green, journalled, committed AND pushed.
- Not this unit: skill contracts and `pipeline.yaml` (META-147); scripts and fixtures
  (META-148); findings statuses (META-149).
- Next unit: **META-147** (skill contracts + re-render).

## Done this session

- **META-144** — Phase VI laid out in `meta/plan.md` (2c4b0b7, 0deafc0).
- **META-145** — `meta/adr/ADR-0010-document-as-deliverable.md`, 699 lines (**3701069**).
  Decisions that bind every later unit: `doc-header.md` §5 **does not hold** and the claims gate
  **stays on `implement`** (F-076); record-vs-deliverable is a property of **sentences**, not
  files; **K8**, the engagement-state statement, is a third claim kind **owned by the ending**
  (F-093); the **invalidation set** is a `plan` output consumed by `implement`, `verify`,
  `review-close`, `check-verify-freshness` and the claims window (F-087); a **quantified** claim
  is discharged only by member enumeration recorded in the audit row (F-095); **`verify`**
  decides ADR conformance per ID, `review-close` checks only that `binding-adrs` is complete
  (F-092). Residual gap named and not solved: a false sentence found **after** the engagement is
  closed has no owner.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
