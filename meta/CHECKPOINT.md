# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at d788007 — 38 steps; 106 codes; selftest 332; 57 citations; harness 110

## Current unit

**META-157** — cluster 3's two citation-integrity fixes: **F-094** and **F-096**.

- **F-094** — a criterion cited by number keeps resolving after the number has come to mean
  something else. Acceptance criteria are cited as `ITEM ACn`; renumber the list and every
  standing citation silently now points at a different criterion. It is **F-077's family** (a
  `path:line` citation resolves for ever, whatever is at the line) — read F-077's resolution
  first and follow it if it fits, rather than inventing a second mechanism for one problem.
- **F-096** — a criterion the environment cannot execute is ticked on a substitution, and the
  tick carries no mark of it. The substituted verification must leave a mark. Compare with
  `scope.py`'s *out-of-scope-by-construction*, landed this session in META-148: a pass that is
  not the same as an ordinary pass **exits 0 and says so in its own words**. That precedent is
  probably the right shape here too.

Both are `spec/work-item.md` / `scripts/lib/claims.py` / `validate-workspace` territory.

- Done when: both fixed with fixtures both ways, a `./scripts/check` step proved non-vacuous in
  the strong form, gate green, both statuses updated with resolving citations (second commit if
  a sha must be cited), journalled, committed AND pushed.
- Next units: **META-158** (the F-099 sweep — expect phantoms; tombstone or correct each,
  honestly), then cluster 4 (**META-159**), cluster 5 (**META-160/161/162**), cluster 6
  (**META-163**), staging (**META-164**), the report (**META-165**).

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
- **META-156** F-081/F-083/F-084 (**8804bd7** + **d788007**), 38 steps, 102 → **106** codes,
  selftest 332. **F-081**: `item.md` gains `merge-commit`, written by a new `scripts/record-merge`
  and nothing else — a second entry was rejected (§2 is one entry per execution, and the format
  would force the tool to invent `Inputs read`/`Decisions`/`Gates` to record an anti-fabrication
  fact) and an amendment convention was rejected (a second in-place exception to append-only,
  which §0 forbids by name). **F-035 is not reintroduced structurally, not carefully**:
  `vcs.merge_problems` answers four questions once, `record-merge` refuses on it and
  `validate-workspace` re-asks it every run, so a typed field is held to exactly what a written
  one is. **F-083: the ORDER, not the gate** — F-014's downgrade exists for a state the move
  *forces*, and this is not that; a legal order already existed (`transition --outcome` writes
  both fields in one act) and the procedure simply never named it, so downgrading the code would
  have legalised the one order that leaves a committable-invalid workspace behind. **F-084**: the
  execution match is scoped to rows whose item is **not yet `done`** — measured first, because
  without that boundary the rule reports 10 rows in the must-pass `examples/toy-project`, which
  is imported real-run evidence. What is **not** decidable is stated in a `[auto]`/`[skill]`
  table: the version *number* being right, `what changed` describing the change, and whether the
  named skill made *this* edit. **A stub caught a vacuous case of the agent's own** — its first
  F-083 case passed with both guards disabled, because the move it used was refused by a gate
  instead. **Filed F-108**: the new change-log rules' first run over the toy project reports six
  rows whose named skill was not executing then, two versions out of order with their own
  timestamps, nine sharing one hand-typed timestamp, and four typed by hand by builder units into
  a tree whose README says *"Nothing here was written by hand."* Exactly one was repaired — a
  builder correcting its own splice — and the other seven stand, which is why the rule is scoped
  rather than retroactive.

