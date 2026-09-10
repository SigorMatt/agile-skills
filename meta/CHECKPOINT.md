# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Execution model (binding, from the mission): every unit is executed by a **dedicated
sub-agent**. The orchestrator holds only the mission, `meta/plan.md`, this file, and each unit's
verdict. Per unit: checkpoint the intent → dispatch with scope, files to read, definition of
done, and the obligation to commit AND push → verify cheaply (git log for the sha,
`./scripts/check` or the unit's fixture) → advance this file.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at bf1caa9 — 43 steps; 108 codes; selftest 356; 64 citations; harness 110

## Current unit

**META-162** — cluster 5, part 3: **F-097**, and **F-104**'s deadlock with it. **ADR the
resolution** — the mission says so explicitly, because this one has to be designed against the
one-action rule rather than patched.

**F-097** — the loop stops on the **first** human question, so an asynchronous stakeholder is
asked one item at a time. A collect-askable-questions pass before the loop stops on the human.

**F-104** (filed this session by META-153b) — `next` step 3 halts on **any** open
human-addressed question, while `spec/question.md` §2 says an elicitation *"must not stop the
loop"*. Both cannot hold; today the first wins, so an unanswered elicitation makes **every**
ending unreachable, **E1 included**. And META-153b established a locus that is in **no ADR**:
**rest itself** (`scripts/lib/engagement.py`, *no question anywhere is open*) counts
elicitations — so **repairing step 3 alone moves the deadlock rather than removing it.** That
sentence is the design constraint; do not lose it.

These are one problem. F-097 asks the loop to gather more before it stops; F-104 says the
current stopping rule is contradictory *and* has a second site. Solve them together.

**The one-action rule is the hard constraint.** `next` dispatches one action. A
collect-askable-questions pass that walks the board looking for what else could be asked is,
naively, several actions — and the pipeline's determinism and auditability rest on the one-action
property. Derive a resolution that does not quietly break it, or derive an explicit, argued
amendment to it. Either is acceptable; an unacknowledged breach is not.

Interacts with ADR-0011's silence threshold: a *silent round* is one halt at *waiting on the
human* with no inbound change. If the loop gathers more questions before halting, the shape of a
round changes. **Reconcile the two or the threshold's meaning drifts.** ADR-0011 §1 is explicit
that the count is defined against **the halt**, not the question set, precisely so it survives
this — check that claim rather than assuming it.

Also relevant: **F-008** (asynchronous file-based interaction, deferred), **F-060** (the pipeline
cannot say what it is waiting for, deferred behind F-008), **F-013**, **F-020** (refine files
several separate questions for one item in one round), **F-021**, **F-028**.

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

- **The rendered body limit is on the RENDERED file, not `process.md`.** META-160 was told
  "473/500, there is room" by this checkpoint and found the rendered body was at **500/500**.
  Check the rendered artefact, not the source.
- **The rendered body limit is on the RENDERED file, not `process.md`** — `review-close` has hit
  exactly 500/500 three times and been compressed each time.
- Done when: the ADR exists, the mechanism (if any) lands with fixtures, the one-action rule is
  either preserved or explicitly amended, the ADR-0011 reconciliation is **checked** not assumed,
  F-097 and F-104 statuses updated with resolving citations, gate green, journalled, committed
  AND pushed.
- Next: cluster 6 (**META-163** — triage every remaining open finding), staging (**META-164** —
  provision-verify both regressions and tear down), the report (**META-165**).

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

### Cluster 5 — planning/criteria and stakeholder protocol — in progress
- **META-160** F-089/F-090/F-088 (**5e43182** + **4bdcbf1**), 42 steps, 108 codes (delta 0, **but
  not trivially** — bumping `verify` dropped five `journal.gates.*` codes out of META-154's
  version-scoped comparison, 108 → 103, so the fixture entries were bumped with the contract;
  this is the third time a bump has moved that comparison). **F-089** lands as DoR **R11** and is
  marked **`[skill]` with evidence, not opinion**: the narrowest regex catching its own three
  criteria flags **26 of 53** criteria in the must-pass toy project for **2 true positives** —
  and that measurement is written into `dor-dod.md` §1 beside the rule, not left in the ledger.
  A wanted count is measured first and carried as a `[src: run: … → …]` citation, a form that
  already existed. **F-089 is smaller than billed and says so**: its own evidence shows no
  criterion was ever reshaped around what was built, so R11 removes a round trip, not a
  correctness failure. **F-090**: acceptance time = the execution that accepts the gap, **before
  its closing transition**; on a `done` item the gate reports NOT APPLICABLE in those words.
  Dispatch sets were **derived from `pipeline.yaml`, not restated** — `intake`, `next` and `retro`
  are reachable by neither route, so a gap owned by one is inert wherever it is written.
  **F-088: the diagnosis transferred from `scope.py`'s fourth state, the mechanism did not** —
  `constrained()` re-reads a git window from a repo, a ref and a permitted set, and an audit row
  is prose with no window to re-read. What transferred is the **shape of the verdict**: a pass
  that could not have failed is marked, never spelled like an ordinary pass. The existing
  labelled form gained a fifth label `Falsifier:`; **reach under-claimed on purpose and stated in
  both specs** — nothing mechanical reads `review.md`'s `## What I examined` or
  `verify-report.md`, before this change or after it. **The vacuous case of its own**: two new
  findings had **no case at all** and would have shipped unexercised; both now fire, and one is
  F-090's *literal* historical shape. Fifth unit running to catch one.
- **META-161** F-082 (**cb344f4** + **bf1caa9**), 43 steps, 108 codes (delta 0; `crossed-answers`
  5 → **8**). A consumed delegation records one labelled line in ADR-0008's `Checked against:`
  shape — ID, category, what was assumed — read by the same `record.blocks()`, and read both as
  a block **and nested inside another block**, because `plan.md`'s natural home for it is under
  the assumption bullet it belongs to and the first draft passed silently over exactly those.
  The sign-off gains a **sixth rule** naming every answer spent under delegation; at **E4**, where
  there is nobody to address, the same list goes into the `## Ending statement`. Enforced at
  `review-close`'s **existing** `cross-answer-consistency` gate — nothing new dispatched.
  **The `[skill]` mark is justified by measurement, in the spec beside the rule**: `[assumed]` is
  not a usable proxy — the toy project records **eight** assumed answers, six confirmed by the
  human, one taken under *no* licence, and exactly **one** a real delegation quoted in prose with
  no ID; eight fires, one true positive. What the lint **cannot** see is stated ADR-0008-§5 style,
  the largest being **a delegation relied on and never written down at all**. **Half 1 was partly
  there and is recorded, not re-claimed** — `refine` step 3 already said to name the deferral;
  missing were the category, the ID, and anything that read the line. **The vacuous case of its
  own**: the fixture exercised only the sign-off branch — the E4 branch, the deliberately-silent
  branch and the citing-an-existing-request path had **no cases at all**. Sixth unit running.

