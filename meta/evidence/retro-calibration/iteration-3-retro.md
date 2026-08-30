---
engagement: EP-001
ending: E1
written: 2026-08-30T18:42:54Z
items-read: 6
journal-entries-read: 77
proposals: 12
---

# Retrospective — EP-001

Read after the ending, by `retro`, on a record its analyst did not write. Every sentence below
about this engagement carries a citation; an uncited sentence would be asking a reader to believe
me about a record they are holding.

## What was read

- **Items:** EP-001, WI-0001, WI-0002, WI-0003, WI-0004 and BUG-0001 — six items, all of them:
  `item.md`, `history.md` and `journal.md` for each, in full. No item was skipped. The epic names
  five children [src: EP-001] and the workspace holds exactly those five directories and no
  others, so the two lists agree.
- **History:** 70 rows across the six items — EP-001 10, WI-0001 14, WI-0002 9, WI-0003 14,
  BUG-0001 11, WI-0004 12. Every chain is unbroken and every last row matches its item's status
  [src: run: .claude/agile-skills/scripts/validate-workspace → exit 1, 13 unresolved-citation errors, none about history].
- **Journal entries:** 77, read in full and not by heading — EP-001 14, WI-0001 15, WI-0002 10,
  WI-0003 14, BUG-0001 11, WI-0004 13. Their `**Gates:**` bullets were also extracted
  mechanically and compared skill by skill, which is where the gate observations below come from.
- **Questions:** 20 — 15 to the human (12 decisions and three `kind: sign-off`) and five to the
  architect [src: EP-001/Q-004; EP-001/Q-005]. All 20 are `status: answered`; none is `open` and
  none is `deferred`. Their `created`/`answered-at` pairs were tabulated to read lateness.
- **Artifacts:** all 25 — every `plan.md`, `impl-report.md`, `verify-report.md`, `review.md` and
  `refinement-qa.md`, plus the epic's termination review [src: tracker/items/EP-001/artifacts/review.md].
  The five `review.md` files and the two longest `verify-report.md` were read in full; the rest
  were read by section against the journal entries that produced them.
- **Documents:** `docs/product/vision.md` at v11 [src: docs/product/vision.md],
  `docs/architecture/overview.md` at v9 [src: docs/architecture/overview.md], and ADR-0001 to
  ADR-0010, with both change logs matched row by row to the item and the execution that wrote
  them [src: ADR-0009; ADR-0010].
- **Contracts:** the installed `.claude/skills/*/references/contract.md` and
  `.claude/agile-skills/skills/*/skill.yaml` for `intake`, `refine`, `plan`, `implement`,
  `verify`, `review-close` and `answer-questions`, plus `spec/dor-dod.md`, `spec/question.md`,
  `spec/journal-and-history.md`, `spec/retro.md` and `spec/workspace-layout.md`
  [src: .claude/agile-skills/spec/dor-dod.md].
- **Requests:** none. `tracker/requests/` holds only `.gitkeep`, so the stakeholder opened nothing
  on their own initiative and the whole exchange is in the questions.
- **Not available, and what it cost:**
  - **The product source tree.** `mdtab/` and `tests/` were not banked with this copy
    [src: RECORD-NOTICE.md]. Nothing below is a judgement about the software: every claim in the
    record that names a source file was read as a claim, not re-checked against the code. The
    `workspace-valid` gate fails for this reason and no other — 13 `claim.citation.unresolved`
    errors, every one of them a `mdtab/*.py` or `tests/*.py` path.
  - **The commit history.** There is no repository in this copy, so nothing was drawn from commit
    times or messages, and the twenty-odd commit shas the record names could not be resolved.
    Timings below come from record timestamps only.
  - **`IDEA.md`, `SIMULATION-NOTICE.md` and `HARNESS-STATUS.md`**, all three cited by executions
    [src: tracker/items/WI-0001/journal.md]. The stakeholder's original one-line idea is quoted
    verbatim inside the record, so the loss is bounded; what cannot be checked is whether the
    quotations are faithful.
  - **The acting contracts.** Every entry names a skill version earlier than the one installed
    here — `intake` 0.2.1 against 0.3.0, `refine` 0.2.2 against 0.3.0, `plan` 0.3.1 against 0.4.1,
    `implement` 0.2.2 against 0.3.0, `verify` 0.1.4 against 0.2.0, `review-close` 0.5.0 against
    0.6.0, `answer-questions` 0.3.1 against 0.4.0 [src: .claude/agile-skills/VERSION]. So the
    reading this skill's procedure asks for third — comparing an entry's gates with the acting
    contract's — cannot be made for any execution in this engagement. What was compared instead:
    each skill's gate list against its own other executions, which is decidable from the record
    alone, and each against the **installed** contract, with the difference reported as unknown.

## Engagement retrospective

### Five send-backs, and not one of them was about the tool's behaviour

`review-close` rejected an item four times and `verify` once. WI-0001 went back on two false
sentences — one in an ADR about a test, one in the architecture overview about a function
[src: tracker/items/WI-0001/journal.md]. WI-0003 went back on D7 and D12, with the review saying
in terms that the code "maps hunk-for-hunk to the plan, contradicts no ADR and merges clean and
green" [src: tracker/items/WI-0003/history.md]. BUG-0001 went back once from `verify` because the
sentence written to replace a false absolute was itself false [src: tracker/items/BUG-0001/history.md],
and once from `review-close` because a test expressed its documents as Python literals against
ADR-0005 [src: tracker/items/BUG-0001/artifacts/review.md]. WI-0004 went back on D7 and D12 over
four sentences in the product vision [src: tracker/items/WI-0004/artifacts/review.md]. In four of the
five every acceptance criterion had passed and the merge result was green before the rejection;
in the fifth the criterion that failed was one about the text of a document
[src: BUG-0001 AC1].

**Where it shows in the record:** the five `in-review → in-progress` and `verifying → in-progress`
rows across the four items' `history.md`, and the verdict paragraph of each `review.md`.

### The engagement's only bug was a sentence, and it survived every automated gate and two hand audits

`"no column's width depends on its marker"` was written for WI-0002, repeated into the
architecture overview and into a test's docstring, and cited `WI-0002 AC6`, which says
*alignment* [src: BUG-0001]. It passed `lint-claims` throughout, because the citation resolves;
it passed WI-0002's own D12 audit, which recorded the claim as holding [src: tracker/items/WI-0002/artifacts/review.md];
and it passed a unit test named for it, whose cells were wide enough that the rule it denied never
applied [src: tracker/items/BUG-0001/artifacts/plan.md]. It was caught at the epic's termination
review, by DE6, by one command run against an empty column [src: tracker/items/EP-001/journal.md].
The first replacement sentence was false in the same shape — it stated an increment per colon
that neither an interior column nor a bare table's first column obeys — and `lint-claims --all`
passed over it too [src: tracker/items/BUG-0001/artifacts/verify-report.md].

**Where it shows in the record:** BUG-0001's filing entry, its first verification's AC1 failure,
and the audit row in WI-0002's review that reads **holds**.

### The one automated documentation gate examined nothing on the executions where the documents were most at risk

`claims-are-sourced` is contracted as `lint-claims --changed-since {{trunk}}`
[src: .claude/skills/implement/references/contract.md]. On WI-0003 it reported *"checked no
documents changed since main"* and exited 0 at the review that then rejected the item on D7 and
D12, and the `implement` execution that cleared the send-back records that it had passed
vacuously on the executions before it too — because `plan` had committed ADR-0008 and the
overview edits to the trunk before the branch was cut [src: tracker/items/WI-0003/journal.md]. At the epic's two termination reviews it
checked zero documents again [src: tracker/items/EP-001/artifacts/review.md]. Each execution
recorded the pass as vacuous rather than claiming it; none of them was misled by it.

**Where it shows in the record:** WI-0003's second `implement` entry, which states the mechanism,
and finding 1 of `tracker/items/EP-001/artifacts/review.md`.

### Two full implement–verify–review cycles were spent on documents, with no line of code changed in either

WI-0003's send-back was cleared by editing two documents; its own entry records `mdtab/` untouched
and the suite unchanged at 71 tests [src: tracker/items/WI-0003/journal.md]. WI-0004's was cleared
by editing one document; its entry records the diff since verification as "one document and the
tracker" [src: tracker/items/WI-0004/journal.md]. Both re-entered `verifying` and `in-review` and
were verified again from scratch. On WI-0004 the plan had learned the lesson and carried a step 7
naming `docs/architecture/overview.md` [src: tracker/items/WI-0004/artifacts/plan.md]; the
document that failed was the one that step did not name.

**Where it shows in the record:** rows 9–12 of `tracker/items/WI-0004/history.md` and rows 11–14
of `tracker/items/WI-0003/history.md`.

### A criterion that counts artefacts needed reconciling four times, and the record kept the count

Three criteria quantified over artefacts the item would move, and they produced four
reconciliations. WI-0001 AC12 fixed a column at "exactly `2 + max`" and could not be satisfied for
a degenerate column [src: WI-0001 AC12]. WI-0002 AC14 required WI-0001's suite to run "unchanged"
while excepting the clause two of its tests encode [src: WI-0002 AC14]. WI-0003 AC9 said "exactly
one" pre-existing test changes, then two did [src: WI-0003/Q-002] — and after that amendment its
prose accounted for four changed tests while its arithmetic still said 63
[src: tracker/items/WI-0003/artifacts/verify-report.md]. The first three were repaired by
`answer-questions` amending the criterion's checking clause [src: WI-0001/Q-005; WI-0002/Q-003];
the fourth was recorded and passed as decidable on either reading. The verifier kept the tally:
"the fourth criterion in EP-001 to count artefacts and need reconciling"
[src: tracker/items/WI-0003/journal.md].

**Where it shows in the record:** three architect-addressed questions filed from `verify` or
`implement`, each amending a criterion's checking clause and none amending its substance.

### An obligation recorded in four artifacts waited three executions for a skill to volunteer the question that would discharge it

`plan` recorded AC12's conflict under `## Assumptions`, the first verification confirmed it, and
the first review accepted it as a gap and wrote that the wording is what should change and that
the amendment belongs to `answer-questions` [src: tracker/items/WI-0001/artifacts/review.md]. Two
further executions ran without it. The second verification filed it, and said why: *"answer-questions
runs only when a question is open, and no skill had filed one"* — adding that had it passed the
item on in silence the obligation would have died at close, with WI-0002 refined against the
arithmetic [src: tracker/items/WI-0001/journal.md].

**Where it shows in the record:** `WI-0001/Q-005`, filed 19:47:17Z against a gap recorded at
19:21:09Z, and the four artifacts that had already named it.

### Two journal entries recorded a gate verdict that the program had contradicted, and both were found by the executions that wrote them

At 08:24:12Z the epic's entry recorded `epic-sign-off` → **pass** where `check-epic-signoff`
printed FAIL; a correction entry twenty-nine seconds later restates it and says why:
*"the gate bullet is the one place a reader checks whether a check actually ran"*
[src: tracker/items/EP-001/journal.md]. At 08:37:26Z the closing entry recorded
`tests-pass-on-the-merge-result` → **skipped** where `run-gate` printed PASS, corrected the same
way. The second correction names the cause: `transition` prints a gate report and appends a
journal body, and nothing checks that the two agree. A third case is quieter: WI-0002's opening
`implement` entry lists six gates where every other `implement` execution in the engagement lists
seven, `no-unplanned-scope` being absent [src: tracker/items/WI-0002/journal.md].

**Where it shows in the record:** the two `review-close` correction entries on EP-001, and the
gate lists of the sixteen other `implement` entries.

### Two rules recorded in an ADR were broken by code that had already passed verification, and a reviewer's reading is what caught both

ADR-0005 says a test may not build a document from a Python literal. WI-0001 shipped one, with a
module docstring asserting the opposite, and the first review rejected the item for it
[src: tracker/items/WI-0001/artifacts/review.md]. BUG-0001 shipped two, after three gates and a
verification pass, and the first review rejected the item for it again, noting the same ADR and
the same precedent [src: tracker/items/BUG-0001/artifacts/review.md]. No acceptance criterion and
no Definition-of-Done criterion asks whether a change conforms to the decisions already recorded:
D6 asks that new decisions be written down, D12 asks whether claims in `docs/` are still true
[src: .claude/agile-skills/spec/dor-dod.md].

**Where it shows in the record:** finding 1 of both first reviews, and the `## Decision` of
ADR-0005.

### The stakeholder was asked to accept the engagement three times, and the pipeline's own work caused two of the three asks

`Q-004` was answered "Yes — A" at 22:29:11Z [src: EP-001/Q-004]. The next termination review,
nine minutes after that, failed DE6 on a false absolute and filed BUG-0001; the engagement left
rest, and `check-epic-signoff` then refused `Q-004` in terms — *"filed before the engagement reached rest… the stakeholder was
asked about something other than what they are being asked to accept"* [src: tracker/items/EP-001/journal.md].
`Q-005` was refused by the stakeholder with one behaviour named, which became WI-0004
[src: EP-001/Q-005]. `Q-006` was accepted [src: EP-001/Q-006]. The order is what produced the
second round: the sign-off is filed at step 10 and the epic's Definition of Done is applied only
after the reply, so a DE1–DE6 failure found afterwards invalidates an acceptance already given.

**Where it shows in the record:** three `review-close` entries on EP-001 — 22:25:23Z filing the
sign-off, 22:38:11Z failing DE6 and filing BUG-0001, 23:26:16Z filing the second sign-off after
the gate refused the first.

### Two documents were corrected by skills that do not own them, because the item that owned them was already closed

`docs/product/vision.md` v10 was written by `review-close`, which records why: the sentence
*"they have not yet been asked"* was made false by that execution filing the sign-off, and
*"the only route that would normally carry the fix is a send-back to `implement` on the item that
owns the document, and that item is the one this execution just closed"* [src: tracker/items/EP-001/journal.md].
v11 was written by `answer-questions`, which corrected a second sentence beyond its answer's own
scope, false since WI-0004's code landed and missed by v9's sweep [src: docs/product/vision.md].
WI-0004's review had seen the first one coming and written it into the item's Notes for the
execution that would end the engagement [src: tracker/items/WI-0004/artifacts/review.md].

**Where it shows in the record:** change-log rows 10 and 11 of `docs/product/vision.md`, each
naming a skill that is not the document's usual author.

### Renumbering an item's criteria while it was still at draft silently invalidated a citation in another item

WI-0002's round-2 refinement rewrote AC1–AC7 as AC1–AC14 [src: tracker/items/WI-0002/journal.md].
WI-0003 had been filed seven minutes earlier citing "WI-0002 AC7" for the behaviour that is now
AC10, and `refine` found and corrected two such citations in round 1
[src: tracker/items/WI-0003/journal.md]. The same hazard was recorded once before, when three
criteria were renumbered on WI-0001 and the entry noted that "a reader of an earlier journal entry
will otherwise find the numbers have moved under them" [src: tracker/items/EP-001/journal.md].
`validate-workspace` resolves `ITEM ACn` by checking the item declares that number
[src: .claude/agile-skills/scripts/lib/claims.py], so a citation that has come to mean something
else still resolves.

**Where it shows in the record:** `### Corrected in refinement round 1` on WI-0003, and the
renumbering decision in `answer-questions`' entry of 18:34:47Z.

### No question in the engagement carries a Cross-answer check, and no execution recorded the gate that produces one

`spec/question.md` §2 defines `## Cross-answer check` as the section that stops a contradiction
being settled privately, and the installed contracts of `answer-questions`, `refine`, `plan`,
`implement` and `review-close` all carry a hard `cross-answer-consistency` gate run through
`scripts/lint-answers` [src: .claude/skills/answer-questions/references/contract.md]. None of the
twenty question files has that section, and none of the 77 journal entries lists that gate
[src: EP-001/Q-006; WI-0004/Q-001]. Every acting version predates the installed one
[src: .claude/agile-skills/VERSION], so whether the contract in force required either cannot be
decided from this copy; what can be said is that fifteen human answers were consumed and the
record contains no check of any of them against the others.

**Where it shows in the record:** the `**Gates:**` bullets of all seventeen `answer-questions`
entries, and the section list of every file under `tracker/items/*/questions/`.

## Positive record

### Not one gate was forced and not one Definition of Ready was overridden, across 77 executions

`scripts/transition --force` writes `[gates forced]` into the reason it records
[src: .claude/agile-skills/scripts/transition], and no reason in any of the 70 history rows
contains it [src: tracker/items/EP-001/history.md]. Both `refinement-qa.md` files that carry an
`## Override` section declare `None` [src: tracker/items/WI-0004/artifacts/refinement-qa.md], and
two history rows state "no override" in terms [src: tracker/items/WI-0001/history.md]. Where a
gate failed it was recorded as failed and acted on — WI-0003's `implement` entry records
`tests-pass` → **fail** and suspends the item rather than moving it forward
[src: tracker/items/WI-0003/journal.md].

### A program refused an acceptance a reading would have accepted

`check-epic-signoff` failed `Q-004` because it was filed before the rest it would have covered,
and quoted the reason: *"the stakeholder was asked about something other than what they are being
asked to accept"* [src: tracker/items/EP-001/journal.md]. Nothing in the tracker looked wrong at
that moment — every child was `done` and the stakeholder had said yes — and the gate is the only
thing in the engagement that would have stopped an ending covering a child the stakeholder had
never seen [src: EP-001/Q-005]. It is the clearest case in this record of a rule catching
something rather than confirming something.

### The non-blocking question did exactly what it exists for, twice

`WI-0001/Q-005` and `WI-0002/Q-003` were both filed by `verify` against a criterion that could not
be satisfied as written, both `blocking: false` [src: WI-0001/Q-005; WI-0002/Q-003]. Neither
suspended its item; `next` dispatched `answer-questions` ahead of `review-close`, so the criterion
was amended before the review that would have closed the item over it, and the amendment was to
the checking clause and not to what the tool must do [src: tracker/items/WI-0002/journal.md].
Both entries record `item-resumed-correctly` → **skipped** with the reason — there was no
suspension to resume from — rather than recording a pass over a comparison with nothing to
compare [src: tracker/items/WI-0001/journal.md].

### Every re-verification re-decided every criterion instead of inheriting the previous verdict

WI-0003's second verification states that between the two verified commits the code changed by two
bytes, that a cheap re-run citing the first report was available, and that it was rejected —
*"the first report is a claim, and the whole standing of this skill is that it does not confirm
claims"* — and it regenerated its differential corpus with a different seed so the two runs are
independent measurements [src: tracker/items/WI-0003/journal.md]. WI-0004's second verification
re-decided all seven criteria on a head whose code diff was empty, and reported the empty diff as
corroboration rather than as the evidence [src: tracker/items/WI-0004/artifacts/verify-report.md].
Verification also caught its own instrument: a mutation applied by `sed` matched nothing and
reported a clean suite, which would have been recorded as sensitivity where nothing had changed;
the harness now asserts its target is present before mutating [src: tracker/items/WI-0001/journal.md].

### Two toolkit defects were reported rather than patched from inside a work item, and both are addressed in the toolkit installed here

`implement` found that `validate-workspace` aborted with a `UnicodeDecodeError` on a `.md` fixture
holding an undecodable byte — a hard gate of every skill taken down by one project file — and
filed `WI-0001/Q-004` rather than editing the pipeline's own machinery, on the ground that such an
edit "would be audited by nobody, covered by no criterion, and discarded by the next toolkit
install" [src: WI-0001/Q-004]. The installed reader now decodes with `errors="replace"` and
reports a finding instead of a traceback [src: .claude/agile-skills/scripts/lib/textio.py]. The
vacuous claims window that executions on four items recorded rather than filed — *"a defect in
the contract rather than in this engagement… no item in this project can fix a skill contract"*
[src: tracker/items/EP-001/artifacts/review.md] — is likewise modelled in the installed toolkit
as a third state that fails rather than passes, and the current `review-close` exit criteria name
it [src: .claude/agile-skills/scripts/lib/scope.py]. Whether this record is what caused either
fix cannot be read from this copy; that both are fixed in the version installed over it can.

### The record corrected itself by appending, twice, including against its own interest

Both gate misrecordings were repaired by a new entry naming the old value, the right one and the
reason, with no edit to the entry being corrected [src: tracker/items/EP-001/journal.md]. The
second correction goes further than the fix and names the general cause for whoever reads next.
The same discipline appears in the documents: `docs/product/vision.md` keeps the 2026-08-28
acceptance below the correction that supersedes it, "because it accurately records what they were
shown then" [src: docs/product/vision.md].

### A criterion practice was improved inside the engagement, citing the failures that motivated it

After three criteria had been amended for counting artefacts, WI-0004's AC5 names twenty tests
individually instead of counting them, and the item's history row says so
[src: tracker/items/WI-0004/history.md]. `refine` measured the claim before writing it —
`grep -rniE '<br' tests/` exits 1, so no existing test could be disturbed — rather than asserting
it [src: tracker/items/WI-0004/journal.md]. WI-0003's refinement had already established the
practice of measuring every transcript in a criterion against a prototype before writing it
[src: tracker/items/WI-0003/artifacts/refinement-qa.md].

### Ten things are on the record as deliberately not work, each with the stakeholder's own words

Five caveats declined at `Q-004`, three gaps declined at `Q-005` and two declined at `Q-006` are
written into the epic's item and into the vision, not left in three items' Notes, with the reason
given each time: a decline that lives only in a question file reads later as a gap nobody looked
at [src: EP-001; docs/product/vision.md]. Each sign-off also offered "accept with follow-ups" as a
real option and recorded that it was refused in terms [src: EP-001/Q-006]. That is what makes the
absence of follow-up items in this engagement a decision rather than an omission.

## Proposed toolkit findings

Twelve, for triage upstream. Ten are classified `toolkit-defect`, which is a high proportion and
is stated as such: this engagement's own executions identified most of them as toolkit
observations while running, and none of them could be filed from inside a consumer project. Two
of the three that most resemble a defect — the vacuous claims window, and a validator that
crashes rather than reports — are **not** proposed here, because the toolkit installed in this
workspace already addresses them; they are in `## Positive record` instead.

### P-1 — PROPOSED — one contract serves two subjects, and at an engagement's ending half of it is undefined

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (review-close), `.claude/skills/review-close/references/contract.md`, `spec/dor-dod.md`
- **Symptom:** `review-close` closes work items and also ends engagements, and its gate list is
  written for the first. Three of its hard gates resolve `{{item.branch}}` or a merge, which an
  epic does not have, and its `definition-of-done` gate says to walk `spec/dor-dod.md` section 3 —
  the work-item checklist — when an ending must be judged by section 4. Every epic-level execution
  in this engagement recorded the same three gates as skipped for the same reason
  [src: tracker/items/EP-001/journal.md], and the termination review recorded walking section 4
  "the contract's wording notwithstanding… as a contract defect rather than followed literally".
  The same contract lists `artifacts/review.md` as an always-output, while the ask-and-stop path
  has no verdict to write, which left the epic's `review.md` asserting "not ended" for eleven
  hours after the finding that caused it had been fixed
  [src: tracker/items/EP-001/artifacts/review.md]. The installed 0.6.0 contract still says
  section 3 and still resolves `{{item.branch}}` [src: .claude/skills/review-close/references/contract.md].
- **Counterfactual:** every engagement reaches an ending, and every ending is judged by a skill
  whose gates were specified for a branch. Nothing about a project's subject matter is load-bearing:
  an epic has no branch in any project.
- **Recurrence:** five epic-level executions in this engagement, each skipping the same three
  gates; once for the section-3/section-4 mismatch; once for the always-output.
- **Direction:** give the ending its own gate list and its own outputs, or make each gate's row
  state its subject so that "skipped, an epic has no branch" is the contract's answer rather than
  the worker's. A gate that is skipped by every execution of a whole class is not a gate.
- **Status:** proposed — not filed. Triage upstream.

### P-2 — PROPOSED — the acceptance is asked for before the epic's Definition of Done is applied, so a late finding invalidates an acceptance already given

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (review-close step 10), `spec/dor-dod.md` §4, `spec/question.md` §2
- **Symptom:** the termination review files the sign-off and stops; DE1–DE6 are applied when the
  reply arrives, because DE7 cannot be satisfied before it [src: tracker/items/EP-001/journal.md].
  Here the stakeholder accepted at 22:29:11Z and the DE6 claim audit — run nine minutes later, in
  the next execution — found a false absolute and filed a bug, which made the engagement leave
  rest and made the sentence *"no bug was filed and left unfixed"* in the question they had just
  answered false [src: EP-001/Q-004]. `check-epic-signoff` then correctly refused that acceptance
  and a second sign-off was due [src: EP-001/Q-005]. The engagement paid one full extra round for
  the ordering, and said so.
- **Counterfactual:** any engagement whose termination review finds anything at DE1–DE6 reaches
  this, because the audit that could find it runs after the question that would be invalidated by
  it. The subject matter of the finding is irrelevant; only its timing matters.
- **Recurrence:** once, and it produced a fourth child item, a second sign-off and a third.
- **Direction:** apply the criteria that do not depend on the reply — DE1 through DE6 — before
  the question is filed, and file the sign-off only against a state that has passed them. DE7
  stays where it is; it is the one that genuinely cannot precede the answer.
- **Status:** proposed — not filed. Triage upstream.

### P-3 — PROPOSED — the pipeline asks which documents a change touched, and never asks which documents it falsified, until the last gate

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (plan, implement, verify), `spec/dor-dod.md` D7
- **Symptom:** D7 is a `review-close` criterion, so the question "what does this change make
  false?" is first asked after `implement` and `verify` have both passed. The automated gate that
  looks at documents is scoped to what the execution *changed*, not to what it *falsified*, so a
  document the branch never touches is invisible to it [src: tracker/items/WI-0003/journal.md].
  Two items were sent back on D7 and D12 and cleared by editing documents only, each costing a
  full `implement → verify → review-close` cycle with no code change
  [src: tracker/items/WI-0004/journal.md]. The second is the sharper case: WI-0004's plan had
  learned from WI-0003 and carried a step for updating the architecture overview, which
  `implement` executed faithfully; the document that failed was the product vision, which no step
  named [src: tracker/items/WI-0004/artifacts/plan.md]. The installed `plan` skill's own step 8
  still names `docs/architecture/overview.md` and no other document
  [src: .claude/skills/plan/SKILL.md].
- **Counterfactual:** any engagement whose change makes a sentence in a delivered document false
  reaches this, and the later items of any engagement are the ones most likely to. What the
  document says is not load-bearing; that nothing before the last gate is asked about it is.
- **Recurrence:** twice as a send-back (WI-0003, WI-0004); a third time as a finding recorded
  rather than sent back [src: tracker/items/WI-0002/artifacts/review.md].
- **Direction:** make the set of documents a change invalidates an output of `plan` — enumerated
  as a step, from the documents the plan itself cites — and have `implement`'s self-check answer
  D7 before it hands over, so that the last gate confirms the answer instead of discovering it.
- **Status:** proposed — not filed. Triage upstream.

### P-4 — PROPOSED — a claim audit is passed by an example that could not have falsified the claim

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** `spec/dor-dod.md` D12 and DE6, methodology (review-close)
- **Symptom:** D12 says a claim is checked "by reading it against the code", and leaves the choice
  of what to run to the reader. WI-0002's audit recorded *"no column's width depends on its
  marker"* as **holds**, having laid the same table out under all four markers — a table whose
  cells were wide enough that the rule the sentence denies never applied
  [src: tracker/items/WI-0002/artifacts/review.md]. The unit test named for the claim had the same
  blind spot [src: tracker/items/BUG-0001/artifacts/plan.md]. The sentence was false, and the
  example that shows it is one empty column [src: BUG-0001]. The replacement sentence then passed
  the item's own two reproduce commands and was still false, and what caught it was a verifier
  choosing the boundary instead of the happy path: *"the item's own two reproduce commands both
  agree with the new sentence… the one-colon markers are the case the sentence generalises over
  and gets wrong"* [src: tracker/items/BUG-0001/artifacts/verify-report.md].
- **Counterfactual:** any engagement whose documents state an absolute about a rule with a
  boundary reaches this: the auditor picks the example, and the natural example is the one the
  sentence was written from. Nothing about this project's subject is needed to state it.
- **Recurrence:** twice — the original claim at WI-0002's close, and its replacement at BUG-0001's
  first verification. Both were eventually caught by an example chosen to be able to fail.
- **Direction:** an audit row records the example **and why that example could have falsified the
  claim**; an absolute about a rule with a threshold is checked at the threshold. The audit table
  already has a "what I opened" column; what it lacks is the obligation that what was opened be
  capable of a `false`.
- **Status:** proposed — not filed. Triage upstream.

### P-5 — PROPOSED — a criterion that counts artefacts is a criterion that will be amended after the fact

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (refine), `spec/dor-dod.md` R4
- **Symptom:** four criteria in this engagement quantified over things the implementation would
  change — "exactly `2 + max`" [src: WI-0001 AC12], "the suite runs unchanged" [src: WI-0002 AC14],
  "exactly one of its 65 tests changes" [src: WI-0003/Q-002] — and each had to be amended by
  `answer-questions` after the code existed [src: WI-0001/Q-005; WI-0002/Q-003]. Every amendment
  was to a checking clause rather than to a requirement, and each execution checked that
  distinction explicitly, so no criterion was reshaped around what was built; the cost was three
  architect round trips and one criterion that still miscounts while remaining decidable
  [src: tracker/items/WI-0003/artifacts/verify-report.md]. `refine`'s Definition of Ready asks
  that a criterion be decidable; it does not ask whether the quantity it names is one the item
  will move [src: .claude/agile-skills/spec/dor-dod.md].
- **Counterfactual:** any engagement whose item modifies a suite an earlier item shipped reaches
  this, because "unchanged" and "exactly n" are the natural way to write a regression guard and
  both are false the moment the item touches the thing they count.
- **Recurrence:** four reconciliations across three criteria — WI-0001 AC12, WI-0002 AC14, and
  WI-0003 AC9 twice; the record's own running count reached four.
- **Direction:** a criterion names the artefacts it constrains rather than counting them, and
  where a count is genuinely wanted it is measured before the criterion is written. This
  engagement adopted exactly that on its last item and recorded the measurement that justified it
  [src: tracker/items/WI-0004/journal.md]; the practice is not in the toolkit.
- **Status:** proposed — not filed. Triage upstream.

### P-6 — PROPOSED — work recorded in an artifact for a skill that is dispatched only by status or by an open question is inert

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (next, review-close), `pipeline.yaml`
- **Symptom:** a review can accept a gap and record that the remedy belongs to
  `answer-questions`; nothing then causes `answer-questions` to run. AC12's amendment was recorded
  by `plan` under `## Assumptions`, confirmed by the first verification, and written into the
  first review as an accepted gap naming the skill that owns it
  [src: tracker/items/WI-0001/artifacts/review.md]; two executions passed over it, and it was
  discharged only because the second verification chose to file a non-blocking question about it
  and said what would have happened otherwise — the obligation would have died at close
  [src: tracker/items/WI-0001/journal.md]. The orchestrator dispatches on status and on open
  questions; an accepted gap is neither [src: .claude/agile-skills/pipeline.yaml].
- **Counterfactual:** any engagement in which a review accepts a gap whose remedy belongs to a
  skill it does not dispatch. The only reason it did not become a lost obligation here is that a
  worker volunteered a question nobody required.
- **Recurrence:** once as a near miss over three executions; twice more the discovering skill
  filed the question immediately, which is the same mechanism working by choice rather than by
  rule [src: WI-0002/Q-003; WI-0003/Q-002].
- **Direction:** an accepted gap that names an owner is a dispatchable thing — either it is
  recorded as an open question at the moment it is accepted, or the board carries it and the
  orchestrator can see it. A to-do that only a reader can act on is not part of the pipeline.
- **Status:** proposed — not filed. Triage upstream.

### P-7 — PROPOSED — nothing reconciles a journal entry's gate verdicts with the gate runner's output

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** `.claude/agile-skills/scripts/transition`, `.claude/agile-skills/scripts/journal-entry`
- **Symptom:** `transition` runs the acting skill's gates, prints a report, and appends the body
  the caller wrote — and the body's `**Gates:**` bullet is composed before the run. Two entries in
  this engagement recorded a verdict the program had contradicted: `epic-sign-off` → **pass**
  where `check-epic-signoff` printed FAIL, and `tests-pass-on-the-merge-result` → **skipped**
  where `run-gate` printed PASS. Both were caught by the executions that wrote them and corrected
  by a later entry, the second naming the cause exactly: *"`transition` prints a gate report and
  appends a journal body, and nothing checks that the two agree"*
  [src: tracker/items/EP-001/journal.md]. Completeness is unchecked in the same way: one
  `implement` entry lists six gates where the other sixteen list seven
  [src: tracker/items/WI-0002/journal.md]. `journal-entry` requires the bullet to exist and reads
  nothing in it [src: .claude/agile-skills/scripts/journal-entry].
- **Counterfactual:** every execution of every skill in every engagement writes this bullet, and
  nothing anywhere compares it to what ran. The two mistakes here were caught by unusually careful
  workers; the format's own premise is that it should not depend on that.
- **Recurrence:** three times in 77 entries — two contradicted verdicts and one omitted gate.
- **Direction:** the tool that runs the gates writes their verdicts into the entry it appends, the
  way the transition tool already owns the `**Status:**` bullet; the worker supplies the evidence
  sentence, not the pass or fail. Short of that, the tool can refuse a bullet that names a gate
  the contract does not list, or omits one it does.
- **Status:** proposed — not filed. Triage upstream.

### P-8 — PROPOSED — no criterion asks whether a change conforms to the decisions already recorded

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** `spec/dor-dod.md` §3, methodology (implement, verify)
- **Symptom:** the Definition of Done asks that new decisions be written into an ADR (D6) and that
  claims in `docs/` still be true (D12). Nothing asks whether the code and tests obey the ADRs
  that already exist. ADR-0005's rule that a test may not build a document from a Python literal
  was broken twice — once in WI-0001, with a module docstring asserting the opposite
  [src: tracker/items/WI-0001/artifacts/review.md], and once in BUG-0001, after a verification that had passed all
  six of its criteria [src: tracker/items/BUG-0001/artifacts/review.md]. Both were caught only by a
  reviewer reading the diff against the ADR; both cost a send-back. `review-close`'s contract names
  `docs/architecture/adr/` as an input whose purpose is that "the change must not silently
  contradict a recorded decision", and no criterion turns that purpose into a check
  [src: .claude/skills/review-close/references/contract.md].
- **Counterfactual:** any engagement that records an ADR constraining how code or tests are
  written reaches this, and the constraint is invisible to every gate until someone reads for it.
  The content of the rule does not matter; that no stage owns conformance does.
- **Recurrence:** twice, on the same ADR, four items apart.
- **Direction:** make ADR conformance a criterion of its own, applied where the ADRs that bind the
  change are named — most cheaply by having `plan` list the ADRs its steps are constrained by and
  `verify` or `review-close` decide each one, the way D12's claims are decided.
- **Status:** proposed — not filed. Triage upstream.

### P-9 — PROPOSED — a document sentence falsified by the pipeline's own closing act has no item left to carry the fix

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (review-close, answer-questions), `spec/dor-dod.md` D7 and DE4
- **Symptom:** the product vision said the stakeholder had not yet been asked to accept the
  engagement. That was true when `implement` wrote it at 08:05Z and false at 08:22Z, when the
  same closing turn filed the sign-off. The item that owns the document was closed by that turn,
  so `review-close` wrote the document itself and recorded that "there was no send-back available
  that would not have been a fiction" [src: tracker/items/EP-001/journal.md]. `answer-questions`
  wrote the next version and corrected a second sentence beyond its own answer's scope
  [src: docs/product/vision.md]. The review that closed the item had predicted this precise
  sentence going stale and written it into the item's Notes
  [src: tracker/items/WI-0004/artifacts/review.md] — the record saw it coming and had nowhere to
  put it.
- **Counterfactual:** any engagement whose delivered documents describe the engagement's own state
  reaches this, because the last acts of the pipeline are the ones that change that state and the
  items that own the documents are closed by then.
- **Recurrence:** twice in one turn, on the same document, by two different skills.
- **Direction:** either a document section that states the engagement's state is owned by the
  ending rather than by an item — written once, at the ending, by the skill that knows it — or the
  authority to correct it there is stated in the contract rather than reasoned out per execution.
  Both corrections here were declared and defensible; neither was authorised by anything.
- **Status:** proposed — not filed. Triage upstream.

### P-10 — PROPOSED — a criterion cited by number keeps resolving after the number has come to mean something else

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, low
- **Component:** `.claude/agile-skills/scripts/lib/claims.py`, `spec/doc-header.md` §4a
- **Symptom:** criteria may be renumbered while an item is at `draft`, and they were, twice
  [src: tracker/items/EP-001/journal.md]. WI-0003 was filed citing "WI-0002 AC7" and WI-0002's
  round-2 rewrite made AC7 mean something else seven minutes later; `refine` found and corrected
  two such citations by reading [src: tracker/items/WI-0003/journal.md]. The citation resolver
  checks only that the item declares a criterion with that number
  [src: .claude/agile-skills/scripts/lib/claims.py], so both the stale citations resolved cleanly
  the whole time, and `validate-workspace` was green throughout.
- **Counterfactual:** any engagement whose second item cites a first item's criterion by number,
  which is the citation form the spec offers for exactly that purpose. Renumbering at `draft` is
  legal and cheap, and every renumbering silently rewrites every outstanding citation.
- **Recurrence:** twice — once producing two stale citations in another item, once flagged in the
  entry that did the renumbering as a hazard for later readers.
- **Direction:** either a criterion carries an identity that renumbering does not move, or the
  skill that renumbers is required to rewrite the citations that name it — the same obligation
  `answer-questions` already accepts for a `## Consequences` list. A resolver that cannot tell a
  stale citation from a live one should say so where the rule is stated.
- **Status:** proposed — not filed. Triage upstream.

### P-11 — PROPOSED — the engagement's scope grew twice from the stakeholder's own answers, which is why it took three acceptances

- **Classification:** project-circumstance
- **Severity:** none to the toolkit; to this engagement, two of the five children and two of the
  three sign-offs
- **Component:** this project — the stakeholder's answers at `WI-0002/Q-002` and `EP-001/Q-005`
- **Symptom:** WI-0003 exists because the stakeholder accepted a cost and then refused its
  consequence — *"that's a fault in the tool and I'd want it sorted rather than worked around"*
  [src: WI-0002/Q-002]. WI-0004 exists because they declined the second sign-off with one
  behaviour named [src: EP-001/Q-005]. Both were handled the way the spec provides for: a new item
  at `draft` with `arose-from`, rather than widening a closed item
  [src: tracker/items/WI-0004/journal.md]. Two of the five children, and one of the three
  sign-offs, come from this.
- **Direction:** none for the toolkit. Recorded because a reader of the timeline will otherwise
  read three sign-offs as a process fault, and two of the three are a stakeholder deciding
  something new after seeing the tool work — which is the loop working.
- **Status:** proposed — not filed. Triage upstream.

### P-12 — PROPOSED — the record contains no cross-answer check, and this copy cannot decide whether the acting contracts required one

- **Classification:** observation
- **Severity:** correctness of the record, low
- **Component:** methodology (answer-questions), `spec/question.md` §2
- **Symptom:** fifteen human answers were consumed across twenty question files, and no question
  file carries the `## Cross-answer check` section that `spec/question.md` §2 defines, nor does
  any of the 77 journal entries record the `cross-answer-consistency` gate that the installed
  contracts of five skills make hard [src: .claude/skills/answer-questions/references/contract.md].
  Whether that is an omission or a version difference cannot be settled here: every entry names a
  skill version earlier than the one installed — `answer-questions` 0.3.1 against 0.4.0
  [src: .claude/agile-skills/VERSION] — and the contracts those versions carried were not banked
  with the record [src: RECORD-NOTICE.md]. What is decidable is that the stakeholder's fifteen
  answers were never checked against each other anywhere in the record, and that two of them did
  in fact narrow an earlier one [src: WI-0003/Q-001; WI-0002/Q-001].
- **Direction:** none proposed. If the gate post-dates the run, this is only a note about what an
  older record cannot show; if it does not, it is a gate omitted by every execution of the
  five skills whose contracts carry it, and the difference is worth a triager's minute.
- **Status:** proposed — not filed. Triage upstream.
