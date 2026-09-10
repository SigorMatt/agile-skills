# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at e5a9bb8 — 37 steps; 102 codes; selftest 320; 56 citations; harness 110

## Current unit

**META-156** — cluster 3's three record-shape fixes: **F-081, F-083, F-084**.

- **F-081** — the close-before-merge order leaves the merge unrecordable in the entry that
  reports it. `review-close` closes the item, *then* merges; the merge sha is created **after**
  the closing entry is written, so the entry that reports the merge cannot name it. Give the sha
  a sanctioned home. (Related and already filed: **F-035**, `check-commit-refs` reports a merge
  that never happened.)
- **F-083** — `review-close`'s recorded step order fails its own `workspace-valid` gate. Make
  the legal order legal.
- **F-084** — a document's version row is a self-reported field with nothing behind it; match
  the rows against the executions that claim them.

Each ships its must-fail fixture. F-083 in particular is F-014's family — *the gate runs against
the pre-move workspace* — so check whether the fix belongs in the order or in when the gate runs,
and say which and why.

- Done when: three fixes, fixtures both ways, a `./scripts/check` step proved non-vacuous,
  gate green, the three statuses updated with resolving citations (a second commit if a sha
  must be cited), journalled, committed AND pushed.
- Next units: **META-157** (F-094, F-096), **META-158** (the F-099 sweep), then cluster 4
  (**META-159**), cluster 5 (**META-160/161/162**), cluster 6 (**META-163**),
  staging (**META-164**), the report (**META-165**).

## Done this session — one line per unit; the shas are the record

Full detail lives in the ADRs, `meta/journal.md` and `meta/findings/FINDINGS.md`.

- **META-144** Phase VI planned (2c4b0b7, 0deafc0).

### Cluster 1 — document-as-deliverable — COMPLETE
- **META-145** ADR-0010, 699 lines (**3701069**). §5 does not hold; the claims gate stays on
  `implement` (F-076). Record-vs-deliverable is a property of **sentences**, not files. **K8**
  engagement-state statements are **owned by the ending** (F-093). The **invalidation set** is a
  `plan` output (F-087). Quantified claims need member enumeration in the audit row (F-095).
  `verify` decides ADR conformance; `review-close` checks the list is complete (F-092).
- **META-146** specs carry it (**c1fbde8**); D13 new, marked `[skill]` honestly.
- **META-147** four contracts + dist (**5e6434d**); **META-147b** `intake` + `answer-questions`
  (**9adff0e**) — `intake` gets **no** `lint-claims` gate, F-076's shape in a new place.
- **META-148** the window (**5ae1539**): `scope.py`'s fourth state
  *out-of-scope-by-construction* passes **with a mark**; `constrained()` takes the permission
  knowledge from the caller, because **no diff distinguishes "nobody wrote a document" from
  "nobody was allowed to"**. 5 of 8 cases failed against the old scripts.
- **META-148b** all eight `[auto]` obligations become commands (**a843114**); each decides
  **less** than the `manual_check` it replaced and says so. **Obligation 10 is not claimed.**
  Non-vacuity proved twice, the second time with every rule body stubbed.
- **META-148c ABSORBED** — its cases already ran as by-execution steps.
- **META-149** the ledger (**f474027**), append-only proved (358/0), citations 43 → 49. Fixed
  F-076/087/092/093/095/057/058; **F-053 NOT fixed**. **META-148 and META-148b had filed
  contradictory reports; META-148 was right**, proved by execution. Filed **F-100..F-103**.

### Cluster 2 — E4 — COMPLETE
- **META-150** ADR-0011, 627 lines (**94606f5**). The threshold is a **silent round**, default
  3, in `pipeline.yaml`. Wall-clock rejected (wrong in **both** directions); turns rejected
  (ADR-0005). The count is **derived** from an append-only log; the halt is recorded **before**
  state is read; **the reader never writes**. E3 vs E4 in one test: **did the stakeholder's own
  words arrive?**
- **META-151** the model on paper (**877ee85**). **ADR-0006 repaired by a header pointer, not a
  `## Corrections` entry**, argued four ways — stretching §4b in the file its own ledger watches
  would be this repo failing F-067.
- **META-151b** the programs (**4d1b7ce**): `record-halt` is a **separate script**, so "the
  reader never writes" is structural. **The registry grew rather than taking a false triple** —
  pinning the actor is what makes it bite. Threshold single-source proved by execution.
- **META-152** the fixture, both ways (**e9f8d79**); digests **computed**, non-vacuity in the
  strong form; **three defects reported, not bent around**.
- **META-153** the harness (**b845342**), 74 → 105 tests. The driver **asks**; a test forbids the
  threshold's mechanics from its source. `abandoned` checked **first**. Undeclared abandonment is
  **not** a stop; the declared one takes **no closing sim turn**.
- **META-153b** cluster 2's ledger (**bc21bce**), 335/0, citations 49 → 54. Filed
  **F-104..F-107, H-020**; **corrected the orchestrator's summary in three places by reading the
  code**. F-060 not settled, deliberately. **No live run has produced an E4.**
- **META-153c** H-020's unsound half fixed (**4a59a9a** + **a98dbd0**), 110 tests. The driver
  reads **current state** (`done` + `outcome: dropped`), not an append-only derivation. Old
  predicate restored → five failures. A false negative removed: E4 **by withdrawal** now
  recognised. **No toolkit change needed or made.**

### Cluster 3 — enforcement mechanics — in progress
- **META-154** the `**Gates:**` bullet (**1ebba5a** + **e5a9bb8**), 37 steps, 97 → **102** codes,
  selftest 320. `transition` now **composes the whole bullet from the contract** — one line per
  gate, in contract order, verdict from the run, evidence from the caller — so F-091's
  completeness symptom is **unwritable**. A contradicted verdict is **replaced and named on
  stdout**, never silently overwritten. Two things stay the caller's because nothing decided
  them: a `manual_check`'s verdict, and the whole bullet under `--force`. The fourth verdict is
  **`pending`** — *no verdict is owed*, legal in exactly one **derived, not named** situation: a
  move into a status the acting skill's own `dispatch.on_status` contains. Two alternatives were
  tested against the transition table and rejected. **F-080's open question answered: yes, the
  gate belongs in the entry** — an entry naming a gate as not-owed-here is *stronger* evidence
  than silence, because it shows nobody was surprised. The comparison is **version-scoped**: an
  entry records an execution under the contract of its own time. It also found `implement`'s
  procedure was **factually false** (the gates *had* run; what was true is that nothing was
  owed — which is why `pending` means *not owed*, not *not run*) and a verbatim duplicated
  bullet in the same file.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.** Iteration 5 is a HELD-OUT calibration engagement: this
  session does not run it and does not read its probe beyond provision-verification.
