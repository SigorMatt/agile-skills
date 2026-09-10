# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 83541cf — 41 steps; 108 codes; selftest 354; 62 citations; harness 110

**CLUSTERS 1–4 ARE COMPLETE.** Cluster 5 — planning/criteria and the stakeholder protocol —
opens now.

## Current unit

**META-160** — cluster 5, part 1: **F-089, F-090, F-088**.

- **F-089** — a criterion that **counts** artefacts is a criterion that will be amended after
  the fact. Criteria must **name** artifacts rather than count them, and a wanted count is
  **measured first**. (This session has twice been saved by measuring before scoping — the same
  discipline, now written into a contract.)
- **F-090** — work recorded in an artifact for a skill that is dispatched only by status or by
  an open question is **inert**. An accepted gap naming an owner must become **dispatchable** —
  an open question at acceptance time.
- **F-088** — a claim audit is passed by an example that **could not have falsified** the claim.
  An audit example must be able to falsify; the audit row records **why** it could. This is the
  same disease as F-076 (*a window empty by construction*) and F-052/F-066 (*a gate reporting a
  scope it did not have*) — read META-148's `scope.py` fourth state before designing it, and
  reuse rather than reinvent if it fits.

Note F-088 lands on the **audit row**, which META-146 defined in `spec/doc-header.md` §4a and
META-148b gave a labelled form (`Enumeration:` / `Set:` / `Enumerated by:` / `Members:` /
`Verdict:`). Extend that form; do not start a second one.

## Discipline reminders that have paid off this session
- Must-fail fixtures both ways; a `./scripts/check` step **proved non-vacuous in the strong
  form** (stub the deciding bodies) — and **run the stubs against your own new cases**: three
  units in a row have caught a vacuous case of their own that way.
- **Measure before scoping.** Twice this session an unscoped rule would have invalidated
  imported real-run evidence retroactively.
- `review-close`'s rendered SKILL.md is at **exactly 500/500 lines**; pay for additions by
  compressing skill-specific prose, never by moving a requirement out of the contract.
- A contract bump silently changes which journal entries META-154's **version-scoped** `Gates:`
  comparison reads. Expect it; the fixtures catch it.

- Done when: three fixed, fixtures where a rule changed, gate green, three statuses updated with
  resolving citations, journalled, committed AND pushed.
- Next: **META-161** (F-082), **META-162** (F-097 + F-104's deadlock), cluster 6
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

### Cluster 3 — enforcement mechanics — COMPLETE
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
- **META-157** F-094/F-096 (**181e69d** + **3ae7bcd**), 39 steps, 106 → **108** codes, selftest
  354. **F-077's mechanism did NOT generalise, and the reason is the finding's substance**:
  F-077's fix is a *bound* (a line number against the file's length), and the equivalent bound
  for `ITEM ACn` — does the item declare an ACn? — **was already the behaviour F-094 reports as
  fooled**. A bound cannot distinguish a moved target from a standing one; only the target's
  content can. So the *place* was extended, not a second mechanism added: a citation may carry
  the criterion's own words, and an **unanchored** citation is refused only while the item is at
  `draft`/`ready` — the statuses §2 still permits a rewrite at. **Scope measured first**: 84
  standing `ITEM ACn` citations exist across the repo and requiring an anchor everywhere would
  have invalidated all 84 retroactively, which §4a's own grandfathering paragraph forbids.
  **F-096**: a third checkbox state `- [~]`, written by `verify` alone. It follows `scope.py`'s
  exit-0-and-say-so shape, then departs from it in the harder direction — a `- [~]` **MUST** name
  a question on this item (an ERROR), which is the finding's demand that somebody put the
  criterion's wording to the stakeholder while the engagement can still act; the question need
  not be answered, because an open question already holds the engagement short of rest. Also
  unified two divergent criterion-line regexes into one, since adding a state to one would have
  left the other reading `[~]` as unticked. **A vacuous case of its own, caught by its own
  stub** — the second such catch in two units. **A bump-time hazard worth remembering**: the
  `verify` and `refine` bumps silently dropped nine fixture entries out of META-154's
  version-scoped `**Gates:**` comparison; the fixture caught it.
- **META-158** the F-099 sweep (**f61ce10** + **715ef26**), 40 steps, new step 17b. Reads **every
  git-tracked file** — F-099's own direction proposed `meta/**.md` and that was **too narrow for
  the finding's own reason**: a phantom in `dist/` reaches a user, one in `fixtures/` teaches a
  wrong number, one in `harness/` sits in the instrument. Cost 0.4s. A phantom in read-only
  evidence is corrected by a **tombstone in the ledger**, which makes the standing citation
  resolve while the evidence stays byte-identical — F-071's precedent turned into the mechanism.
  One tracked path is a gitlink and cannot be read as text; it is **named on stdout every run**
  rather than passed over, and its 129 files were checked by hand. **Yield: 3276 citations, 128
  numbers, one phantom — H-001**, cited in banked evidence and in the journal, never filed: the
  H-numbering begins at H-002 and the defect was **fixed instead of filed** (META-081). F-071's
  mirror — there a number was named 66 seconds too early, here a fix outran its record.
  Tombstoned; neither citing file edited. **Calibration**: run over a detached worktree at
  `ff8be8a^`, the instant before F-071's tombstone, the sweep reports `PHANTOM F-071 ->
  meta/harness/evidence/iteration-3b/README.md:27` — the known instance at the exact line.
  A subtle one it found: **the report of a phantom must quote the phantom**, so with the H-001
  heading removed the sweep flags the tombstone's own body — a design without tombstones would
  leave the ledger unable to describe its own gaps. `f61ce10` is **red by construction** (the
  step's first run *is* the finding) and `715ef26` is green; the reverse order would have filed
  the tombstone before the instrument that found it, citing a sha that did not exist — F-024's
  trap.

### Cluster 4 — ending contracts — COMPLETE
- **META-159** F-085/F-086/F-061 (**bb76d7d** + **83541cf**), 41 steps, 108 codes unmoved.
  **F-085**: a gate row gains `applies_to` + `not_applicable`, reusing `pipeline.yaml`'s scoping
  key, syntax and meaning; `run-gate` **does not run** the gate on a type the row leaves out and
  `transition` composes the line from it. **No third verdict word** — a contract-declared
  non-subject is `skipped` reached *deliberately* rather than through a null placeholder; one
  fact, one word, and what changed is only who noticed it. The load-bearing case:
  `tests-pass-on-the-merge-result` resolves `{{commands.test}}`, which an epic **has**, so it
  **ran the suite and reported PASS at an ending that merged nothing** — iteration-4b's worker
  recorded it skipped, `run-gate` disagreed by running it, and they had to correct their own
  entry. Now unwritable. **F-086**: `dor-dod.md` §4a — DE1/2/3/5/6 and DE4's first half **before**
  the engagement's account of itself; DE4's restatement, DE7, DE8 after. It **is** ADR-0011's E4
  ordering, unified by one argument: a late DE6 finding invalidates an acceptance at E1–E3, and
  at E4 it files a bug, which is a child, which the `## Ending statement` must name — the same
  audit broken by a second route. **F-061**: one sentence, as specified. **No mechanism needed
  and none filed** — the mechanism worked (it reopened, built and asked again); the *label* lied,
  and a gate here would have to decide whether prose is true. **Deliberate non-scoping recorded**:
  `epic-sign-off` self-passes on a work item — the same shape from the other side — but scoping
  it would flip every work-item entry from `pass` to `skipped` across banked fixtures for
  something F-085 did not ask. **F-086 has no fixture, and the reason is stated rather than
  skipped**: `definition-of-done` is a `manual_check`, so its verdict is the caller's word by
  design (F-091), and nothing in a workspace distinguishes a checklist applied before an
  acceptance from one applied after. **F-085's section-3/4 half was already fixed** before the
  unit and is recorded, not re-claimed. Fourth unit running to catch a vacuous case of its own:
  inverting the scoping to fire everywhere failed 5 observations, including *"it skips everywhere
  and checks nothing"*.

