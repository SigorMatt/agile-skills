# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T01:32:30Z — intake v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly by the operator on the stakeholder's stated idea in `IDEA.md`; this item did not exist before this execution
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement)
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution — no existing item to overlap with)
- **Decisions:**
  - This item is the scheduling rule alone. Split from WI-0002 because it is where the stakeholder's phrase 'simple spaced repetition' has to be made concrete, and that decision is with them (EP-001/Q-003) while WI-0002's behaviour is not.
  - See EP-001's entry for this execution for how the work was split and why.
- **Questions raised:** none on this item; `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003` were filed on the epic and both blocking ones bear on this item's acceptance criteria
- **Commands:**
  - `scripts/new-item --id WI-0003 --type work-item --epic EP-001 --priority high --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, run after this entry and the epic's suspension completed the record)
  - `epic-has-success-measures` → **pass** (EP-001 carries four measures, each checkable by running the tool and reading what it stored; evidence in EP-001's entry)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation`, exit 0; `EP-001/Q-001`)
  - `items-are-separable` (advisory) → **pass** (build order and dependencies stated in EP-001's entry)
  - `no-solution-in-the-problem` (advisory) → **pass** (no technology named in this item's title, story or criteria; the storage medium and the interface are both left open)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/journal.md`, `tracker/items/WI-0003/history.md` (new)
- **Status:** `—` → `draft`
- **Result:** Created at draft with a story, rough acceptance criteria and derived exclusions. Not ready: the criteria state what must be true rather than what to run, because `EP-001/Q-002` is unanswered. `refine` owns it next.

## 2026-08-30T01:41:39Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** not dispatched; this item's artifacts were amended while `answer-questions` consumed the stakeholder's answer to `EP-001/Q-003`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — four criteria written to state the shape an answer must have rather than the rule
  - `tracker/items/EP-001/questions/Q-003.md` — *"Just right or wrong, no rating scale. If I get it right it comes back later each time — a day, then three, then a week, then a month or so. If I get it wrong it goes back to the start."*
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md` — checked against, for the cross-answer check on the epic
  - `docs/architecture/adr/ADR-0002-the-interval-ladder.md` (v1) — written by this execution
- **Decisions:**
  - **Rewrote AC1, AC2 and AC3 from shapes into the rule.** AC1 now names the ladder `1, 3, 7, 30`; AC2 says a missed card is due one day after the review whatever rung it was on, and never later the same day; AC3 gains a worked example — days 0, 1, 4, 11, 41, 71, 101 for a card answered correctly every time — so that "work it out by hand and the tool agrees" has something concrete to be checked against. The item's own `## Notes` had instructed exactly this rewrite once `EP-001/Q-003` was answered.
  - **Wrote the top-rung clause into AC1 and flagged it as a reading, not a decision of theirs.** The stakeholder named four intervals and stopped at *"a month or so"*. AC1 now says the gap holds at 30 days thereafter. The alternative — the ladder keeps growing past a month by a rule nobody stated — fits the sentence equally well. It was decided rather than escalated because it is one constant, entirely reversible, and `ADR-0002` records both readings with the choice attributed to this skill rather than to the stakeholder. `## Notes` instructs `refine`, which speaks to them directly, to confirm it on this item.
  - **Did not decide how a card's next-review date is read back.** AC4 requires the new date to be visible without a further command, and what "visible" means depends on what `recall review` and `recall list` print — a `plan` and `refine` concern, recorded in `## Notes`.
- **Questions raised:** none
- **Commands:** none
- **Gates:** recorded in full on `EP-001`'s journal, the item this execution was dispatched on; the amendments here are evidence for its `answer-is-propagated` gate, which passed.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — AC1, AC2 and AC3 rewritten, `## Notes` replaced
  - `tracker/items/WI-0003/journal.md` — this entry
- **Status:** `draft` → `draft` (unchanged)
- **Result:** This item now states the scheduling rule rather than the shape of one, with the single clause the stakeholder did not settle marked as ours and handed to `refine` to confirm.

## 2026-08-30T03:34:48Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** dispatched by `next` on status `draft`, the highest-ranked runnable item (priority `high`, created 2026-08-30T01:30:04Z, `depends-on: WI-0002` which is `done`)
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (one row — a fresh draft, not a send-back), `journal.md` (intake, and `answer-questions`' amendment of 01:41:39Z)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`; `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — every human answer recorded in this workspace
  - `docs/product/vision.md` v3; `docs/architecture/adr/ADR-0001`, `ADR-0002` v2; `docs/process/using-recall.md` v4
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — the delivered criteria this item's change can invalidate
  - `recall/deck.py`, `recall/cli.py`, `recall/store.py` — so that "visible" and "read the date back" are asked about the tool that exists
  - `tracker/project.yaml`, `.claude/agile-skills/spec/dor-dod.md`, `spec/question.md`, `spec/workspace-layout.md`
- **Decisions:**
  - **Filed two blocking questions to the stakeholder as one ask, and rewrote no criterion.** `Q-001` decides the text of AC1 and `Q-002` decides what AC4's word *visible* means, so rewriting either now would have to be undone. The criteria are left exactly as `answer-questions` wrote them, and `artifacts/refinement-qa.md` says `agenda` rather than `recorded`, which is what Definition of Ready R8 reads.
  - **`Q-001` — what happens above the longest gap — is the stakeholder's, not ours.** `ADR-0002` §"Options considered" already carries an answer (the ladder tops out at 30 days) attributed to `answer-questions` as a reading rather than to them, and both it and `docs/product/vision.md` §"What is still open" instruct this execution to confirm it. The cost of the reading falls entirely on them: a card known cold returning twelve times a year rather than once or twice is their evening. Three options put — stop at a month, double with no ceiling, grow to a ceiling they name — with our preference (A) last and marked as ours.
  - **`Q-002` — whether a sitting says when the card is next due — is product stake, not message wording.** `ADR-0001` reserves wording to `plan`, and this is not wording: it is whether the fact is shown at all, and it decides whether the only behaviour this item delivers is perceptible to the person using the tool. Today `recall list` prints `question | answer` and a sitting prints nothing after a grade, so with option A the ladder would be observable only by opening the deck file. Three options put, preference (B) last and marked as ours.
  - **Decided rather than asked, all recorded in `refinement-qa.md` §"Decided here rather than asked":** the four intervals and that a right answer measures from the day of the sitting (`EP-001/Q-003`, `ADR-0002` §4 — the case that bites is an overdue card under WI-0002 AC13, which is a criterion to write, not a question); that a wrong answer resets `rung` as well as the date (*"If I get it wrong it goes back to the start"*, `ADR-0002` §6's first clause, which the placeholder does not satisfy); and that the deck file is a legitimate observation medium for a criterion (`ADR-0004`, and WI-0002's criteria already write it directly).
  - **Routed to `plan`, not to the stakeholder:** what the tool does with a stored ladder position outside the ladder in a hand-edited deck — clamp, or refuse the deck as unreadable the way `store.py` already refuses an unrecognised `grade`. The answer would be the same whoever the stakeholder was. Recorded in `## Notes` as deliberately unconstrained, which is how Definition of Ready R10 is satisfied for it.
  - **Carried WI-0002's two closing notes into this item's `## Notes`** so they cannot be lost: `record_answer`'s docstring overclaims conformance to `ADR-0002` §6 and this item must add the rung reset; and `docs/process/using-recall.md` §"What this version does not do yet" is written on the premise that scheduling is unbuilt and is invalidated wholesale by this item.
- **Questions raised:** `WI-0003/Q-001`, `WI-0003/Q-002` — both `addressed-to: human`, both `blocking: true`, filed as one ask with the shared round frame in each `## Context` and the last one closing the round
- **Commands:**
  - `scripts/validate-workspace .` → exit 0 (before the questions were filed)
  - `scripts/lint-answers --item WI-0003` → exit 0 (0 consumed human answers on this item)
  - `scripts/validate-workspace .` → exit 1 mid-execution, `question.blocking.not-suspended` and `board.stale`, both expected and both cleared by this transition and the board regeneration that follows it
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0 at entry; the mid-execution failure is this suspension in progress and is cleared by the transition)
  - `definition-of-ready` → **fail**, per criterion: R1 pass (frontmatter complete, `type`/`epic`/`priority` set); R2 pass (role, capability, "so that" outcome); R3 pass (AC1–AC4, labelled, checkboxes); **R4 fail** — no criterion names an invocation, AC3 names no document, and AC4 turns on "visible", which nothing in the tool currently makes true; R5 pass (three exclusions, one a reader would assume included); **R6 fail** by this execution's own doing — `Q-001` and `Q-002` are open and blocking, which is the suspension; R7 pass (`depends-on: WI-0002`, `done`); **R8 fail** — `refinement-qa.md` says `agenda`; R9 pass (one coherent change: the arithmetic in `record_answer` plus the documentation AC3 asks for); **R10 fail** — right at the top rung is `Q-001`, and an overdue card's origin date and an out-of-range stored rung were not yet visible anywhere
  - `criteria-are-decidable` → **fail** (AC1 and AC2 describe arithmetic with no observation; AC3 names no document; AC4's observation is undecided and is `Q-002`. Not repaired this round, because two of the four turn on unanswered questions)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item WI-0003`, exit 0. Checked against: none — this execution consumed no human answer, and recorded no new criterion or condition from one. The five prior answers were read, and none was rewritten, paraphrased or reconciled here)
  - `qa-recorded-verbatim` → **skipped** — no answer has been received, so there is nothing verbatim to record. `refinement-qa.md` says `agenda` and states in its first paragraph that nothing below the round heading is anything the stakeholder said
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new), `tracker/items/WI-0003/questions/Q-002.md` (new)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0003/item.md` — `## Notes` extended with the round, the `plan`-routed design question, and the two inheritances from WI-0002
  - `tracker/board.md` (regenerated), and a commit of the above
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0003 is suspended on two blocking questions to the stakeholder — what happens above the longest gap, and whether a sitting tells you when you will next see the card. No criterion was rewritten, because both questions decide criterion text; the Definition of Ready gap analysis that set the agenda is in `refinement-qa.md`, which honestly says `agenda`.

## 2026-08-30T03:43:10Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer` with two open blocking questions addressed to the human,
  both of which now carry a `## Answer`. Dispatched by the turn's first-action rule
  (`answer-questions` runs before `next` when an escalated question has been answered).
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both, in full, with their answers
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (`status: agenda`)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` and
    `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — every prior human answer in the
    workspace, read for the cross-answer check
  - `docs/architecture/adr/ADR-0002` (v2), `ADR-0001` (v1), `ADR-0006` (v1)
  - `docs/product/vision.md` (v3), `docs/process/using-recall.md` (v4)
  - `tracker/project.yaml`, `tracker/board.md`
  - `recall/cli.py`, `recall/deck.py` — to check that what `ADR-0007` says the tool does today is
    true of the code rather than of the plan
- **Decisions:**
  - `Q-001` — **answered from the human's reply; route: escalation consumed.** They chose option A,
    the ladder that stops at a month. This confirms `ADR-0002` §5, which had recorded the same
    rule as its own reading with an explicit instruction to `refine` to put it to them. The
    propagation is therefore about *provenance and consequence*, not about the rule: §5 and the
    `Decided by` line now attribute it to them, and the consequence "a card known cold returns
    monthly for ever" is recorded as a cost they were shown — the question stated it as ten cards
    a day on a 300-card deck — and accepted, with what would make them revisit it.
  - `Q-001` — **no acceptance criterion amended, deliberately.** AC1 already ends *"and stays at
    30 days on every correct answer after that"*, which is exactly option A. Had they chosen B or
    C, AC1 would have had to be rewritten. Recording that the criterion needed no change is the
    honest result; editing something to demonstrate propagation would not be.
  - `Q-002` — **answered from the human's reply; route: escalation consumed, and the decision is
    new, so it is recorded as an ADR.** They chose option B: a sitting prints one line per card
    saying when that card is next due. Nothing in the record decided this — `ADR-0001` fixes the
    interface and `ADR-0002` fixes the arithmetic, and neither says whether the person is told —
    so `ADR-0007` is written and the question cites it.
  - `ADR-0007` fixes **that** the fact is shown and **which** fact it is, and leaves the wording of
    the line to `plan`. Rationale: `ADR-0001` §5 reserves message wording to `plan`, and an ADR
    that fixed a sentence would take a decision the stakeholder was not asked for.
  - `ADR-0007` states that `recall list` is unchanged. Rationale: option C was the one that would
    have changed it, and they did not choose it; delivered and signed-off WI-0001 behaviour must
    not drift on the back of an answer about something else.
  - **The criteria are not rewritten here; `refine`'s round 2 does that.** Rationale: the item is
    at `draft` and returns there, Definition of Ready R4 fails for all four criteria on grounds
    neither answer touches (no criterion names an invocation), R8 fails because
    `refinement-qa.md` still says `agenda`, and `refine` explicitly reserved a single-pass rewrite
    so that the item and the Q&A cannot disagree. What that pass must say is now fixed in
    `item.md`'s `## Notes`: AC1 stands, AC4's *visible* means the printed line, and all four need
    invocations. This is the one judgement in this execution a reviewer should check hardest — the
    alternative reading is that `answer-questions` should have amended AC4 itself.
  - **No work item filed under step 3b.** Printing the line is inside WI-0003 AC4 and inside its
    `## Out of scope`, which excludes any interface onto the schedule beyond what a review run
    shows. Neither answer implies work no item records.
  - One stale sentence corrected while bumping `ADR-0002`: its consequence bullet said "WI-0003
    AC1 must be amended", an obligation discharged when v1 was written. It now says so. This is a
    repair of our own paraphrase, not a rewrite of anything sourced to a human answer.
- **Cross-answer check:**
  - `Q-001`, checked against `EP-001/Q-003`, `EP-001/Q-001`, `WI-0002/Q-001`, `WI-0002/Q-002`.
    `EP-001/Q-003` — compatible; this answer completes the sentence that stopped at "a month or
    so" and changes no rung. `EP-001/Q-001` — compatible, and the one real tension: that answer
    named a sitting that drags as a failure, and option A is the shape that leaves a large deck a
    permanent daily floor. Not escalated, because the question stated that arithmetic in terms and
    they chose it anyway while naming what would change their mind — the author of both sentences
    reconciled them. `WI-0002/Q-001` — compatible; the no-cap answer already carries their own
    reconciliation of a big pile. `WI-0002/Q-002` — compatible; bottom of the ladder, not the top.
  - `Q-002`, checked against `EP-001/Q-001`, `EP-001/Q-002`, `WI-0002/Q-001`, `WI-0003/Q-001`.
    `EP-001/Q-001` — compatible and reconciled by them in the same sentence as the choice ("one
    line isn't going to slow me down"); the option list had already been bounded by their "nothing
    fancier than that". `EP-001/Q-002` — compatible; a printed line is how the interface they
    chose says things. `WI-0002/Q-001` — compatible; the per-card line cost was stated in the
    option and accepted. `WI-0003/Q-001` — compatible; same round, and a capped ladder makes the
    printed dates more predictable.
  - **No conflict declared, so no question filed.** No sentence in `docs/` sourced to a human
    answer was rewritten by this execution: the couple-of-minutes quotation in
    `docs/product/vision.md` "Who it is for" stands untouched with its citation.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 consumed human answers
    checked, 0 errors
  - `.claude/agile-skills/scripts/lint-claims docs/architecture/adr/ADR-0007-a-sitting-says-when-the-card-is-next-due.md`
    → exit 0, 0 errors (after fixing three citations it rejected on first run)
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1 before this transition, with only
    the two errors this transition and `board-gen` clear (`question.awaiting.none-open`,
    `board.stale`); re-run after transitioning
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in either `## Consequences` was opened and
    the change confirmed present: `ADR-0002` v3 (§5, `Decided by`, the `(i) is chosen` clause, the
    monthly-floor consequence, the stale AC1 bullet), `ADR-0007` (created, 102 lines),
    `docs/product/vision.md` v4 ("What it is for" ×2, "What is still open" restructured),
    `tracker/items/WI-0003/item.md` (`## Notes`, three paragraphs and both round-1 bullets),
    `tracker/items/WI-0003/artifacts/refinement-qa.md` (both `**Answer:**` placeholders, the
    opening paragraph, "What is still open after this round").
  - `answered-from-the-record` → **pass**. Both answers came from the human directly; neither was
    inferred. `Q-001` cites `ADR-0002` §5 as the reading it confirms; `Q-002`'s decision was not in
    the record at all, and is recorded as `ADR-0007` and cited from the question.
  - `escalation-is-justified` → **skipped**, no question was escalated by this execution. Both had
    already been escalated by `refine` and this execution consumed the replies.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0). Both answers
    carry a `## Cross-answer check` naming four prior human answers each, every ID resolving, and
    no conflict declared.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, re-run after this transition and
    `board-gen`).
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-30T03:34:48Z records
    `resume-to: draft`; this execution returns the item to `draft`, not to the status that would
    have seemed natural.
  - `a-deferral-is-not-an-answer` → **skipped**, neither reply deferred. Both name an option and
    give a reason; `Q-001` adds a condition for revisiting later, which is a future intention
    rather than a withheld answer.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at`, plus `## Cross-answer check` and `## Consequences`
  - `tracker/items/WI-0003/questions/Q-002.md` — the same
  - `docs/architecture/adr/ADR-0007-a-sitting-says-when-the-card-is-next-due.md` — **new**, v1
  - `docs/architecture/adr/ADR-0002-the-interval-ladder.md` — v2 → **v3**
  - `docs/product/vision.md` — v3 → **v4**
  - `tracker/items/WI-0003/item.md` — `## Notes` rewritten around both answers
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — both answers recorded verbatim; still
    `status: agenda`, which is `refine`'s to change
  - `tracker/board.md` — regenerated
  - commit on `main` (this workspace has no item branch checked out)
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of `refine`'s blocking questions on WI-0003 are answered and propagated: the
  interval ladder stops at a month by the stakeholder's decision rather than by our reading, and a
  sitting will print one line per card saying when it is next due — a new decision, recorded as
  `ADR-0007`. AC1 needed no amendment and AC4's rewrite belongs to `refine`'s round 2, which the
  item's notes now specify. The item returns to `draft`.

## 2026-08-30T03:48:40Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item
  (priority high, rank 2); BUG-0001 and WI-0004 rank 3.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — round 1's agenda, gap table and answers
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both answered and propagated
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`,
    `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — every prior human answer, re-read
    while writing the criteria
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — the criteria AC6 names
  - `docs/product/vision.md` (v4), `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v3),
    `ADR-0004` (v1), `ADR-0005` (v1), `ADR-0006` (v1), `ADR-0007` (v1)
  - `docs/process/using-recall.md` (v4) — AC5 is written against this file by name
  - `recall/cli.py`, `recall/deck.py`, `recall/store.py`, `tracker/project.yaml`
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Nothing was asked of the stakeholder in this round, and that is the substantive decision.**
    Every remaining gap was put through the routing test in order. `Q-001` and `Q-002` had just
    been answered, so re-asking would have told them their answer was not heard. The rest were
    either settled by a standing decision (`ADR-0002` §4 for the overdue case, `ADR-0002` §6 for
    the reset, `ADR-0007` for the printed line, `ADR-0004` §2 for the deck format) or
    implementation-only and routed to `plan`. Filing a question to be safe would have cost the
    stakeholder a round trip for nothing.
  - **Four criteria became six.** AC1 now walks the ladder five sittings deep rather than four,
    so the top rung *holding* is demonstrated rather than asserted — that clause is the one the
    stakeholder was asked about, and a criterion that stopped at 30 days would not check it.
    AC2 gained part (b): a wrong answer at the top rung, followed by a right answer, so that the
    reset of the **ladder position** is observable and not only the reset of the date. The
    placeholder in `recall/deck.py` passes a date-only check today, which is exactly why the
    criterion has to be able to fail.
  - **AC3 is new**: a gap counts from the day of the sitting even when the card is overdue. It
    was `[assumed]` in round 1's Q&A and nothing checked it. `WI-0002` AC13 makes overdue cards
    real, and the wrong reading — counting from the missed date — would put a card's next review
    in the past, which is the stakeholder's *"don't lose my progress"* failing quietly.
  - **AC5 replaces "written down … in enough detail" with five named facts, one named file, and
    the worked example.** "Enough detail" is the unmeasurable adjective R4 exists to catch. The
    file is `docs/process/using-recall.md`, whose current "What this version does not do yet"
    section this item falsifies, so AC5 also requires that section to stop saying scheduling is
    unbuilt — which is D7 and D12 pulled forward into a criterion rather than left to review.
  - **AC6 is written to the `spec/dor-dod.md` §6a shape**: it names `WI-0001` AC1–AC9 and
    `WI-0002` AC1–AC13 by ID, says the assessment is a read of their text with the suite as
    evidence rather than as definition, names the four most at risk, and says what to do when
    nothing executable exercises both — state the non-intersection, then cover or waive by ID.
  - **The criteria compress the calendar by resetting `due` and never by writing `rung`.** A
    hundred-day ladder is not walkable in a test otherwise. It is faithful because `ADR-0002` §4
    counts from the day of the sitting, and it has a second benefit worth the sentence: no
    criterion depends on how a ladder position is stored, so `plan` can choose the encoding
    without any criterion's verdict moving.
  - **AC4 fixes one string — the date as `YYYY-MM-DD` — and nothing else about the line.**
    Recorded as `refine`'s decision, marked `[assumed]` in the Q&A and called out in `## Notes`,
    because `ADR-0001` §5 reserves message wording to `plan` and this trims that freedom. The
    reason is R4: a criterion nobody can grep is not decidable. It is the form `ADR-0004` §2
    already uses.
  - **Two design questions routed to `plan`, both recorded in `## Notes` for R10**: what an
    out-of-range stored ladder position does, and how a ladder position is encoded in `rung`.
    The second was noticed while writing AC1 — `ADR-0004` §2 calls `rung` an index while
    `ADR-0002` §3 says a new card starts below the ladder, which differ by one in what `0` means
    and produce identical dates. Neither is the stakeholder's, because the answer would be the
    same whoever they were.
  - **`## Out of scope` grew from three entries to six**, on the authority of `ADR-0007` §3–§4
    and the epic's exclusion of statistics: `recall list` gains nothing (option C of `Q-002`,
    which they did not choose — the thing a reader of that question would most reasonably assume
    was included), no end-of-sitting summary, no history beyond the single `grade` field, and no
    setting for changing the ladder despite the stakeholder saying they might revisit it.
  - **No Definition of Ready override.** None was needed and none was recorded.
- **Questions raised:** none this round. Round 1's two — `Q-001` and `Q-002`, both blocking, both
  addressed to the stakeholder — are `answered`; the full exchange is in
  `artifacts/refinement-qa.md`, `status: recorded`. Nothing is left `[unresolved]`.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace` → exit 0, 6 items, 10 documents, 0 errors
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 consumed human answers
    checked, 0 errors
  - `python3 .claude/agile-skills/scripts/board-gen .` → board regenerated
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `definition-of-ready` → **pass**, criterion by criterion. R1 pass (frontmatter complete, auto).
    R2 pass (`## Story` has role, capability and a "so that"). R3 pass (six labelled checkboxes,
    auto). R4 **was fail, now pass** — every criterion names `recall add` or `recall review` and
    the deck file, or one named document (AC5), or named criteria to read (AC6); the last
    adjective-shaped phrase, AC5's "well enough to work a date out by hand", is discharged by the
    five facts and the worked example it enumerates. R5 pass (six exclusions). R6 pass (both
    questions answered, none open, auto). R7 pass (`depends-on: WI-0002`, done, auto). R8 **was
    fail, now pass** — `refinement-qa.md` says `status: recorded` and holds both rounds. R9 pass
    (one coherent change: the arithmetic in `record_answer`, one line in `cmd_review`, the
    documentation AC5 requires). R10 **was fail, now pass** — every combination is visible: right
    at the top rung (AC1's fifth sitting), wrong at the bottom (AC2a), wrong at the top with the
    reset (AC2b), right and wrong on an overdue card (AC3), the printed line on both answers at
    two gaps (AC4), and the two unconstrained design choices in `## Notes` with who left them so.
    The full table is in `refinement-qa.md`.
  - `criteria-are-decidable` → **pass**. AC1: `recall add`, then five cycles of "set `due` to
    today, `recall review` answering right"; read the five `due` values from the deck file —
    verdict is whether they are today +1, +3, +7, +30, +30. AC2: the same setup, answering wrong
    at the bottom rung and at the top and then right; verdict is whether `due` is today +1 each
    time and today +1 rather than +30 on the last. AC3: a deck file with `due` ten days past, one
    sitting each way; verdict is whether `due` is today +1 rather than nine days in the past.
    AC4: grep the runs' stdout for the `YYYY-MM-DD` strings for today +1 and today +30; verdict
    is whether each appears after that card's answer side and matches the `due` written. AC5:
    read `docs/process/using-recall.md`; verdict is whether all five named facts and the worked
    example are present and whether the "does not do yet" section still claims scheduling is
    unbuilt. AC6: read `WI-0001` AC1–AC9 and `WI-0002` AC1–AC13 against the shipped behaviour;
    verdict is whether each still reads true, with the suite cited as evidence and any
    non-intersection stated and then covered or waived by ID.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0). No new human
    answer was recorded this round, so there was none to check; the two this item carries were
    checked when consumed and both checks are in the question files. Round 2 re-read all five
    prior answers against the criteria it wrote and found no conflict, and recorded that in
    `refinement-qa.md` under `## Cross-answer check, round 2` rather than leaving it blank.
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` carries both rounds: round 1's two
    questions with the stakeholder's answers word for word, and round 2's decisions each tagged
    `[human]` or `[assumed]` with what it rests on. Nothing is paraphrased into agreement and
    nothing is left `[unresolved]`.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — acceptance criteria rewritten (4 → 6), `## Out of scope`
    extended (3 → 6), `## Notes` rewritten around round 2
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; round 2,
    the round-2 cross-answer check, and the per-criterion Definition of Ready verdict added
  - `tracker/board.md` — regenerated
  - commit on `main`
- **Status:** `draft` → `ready`
- **Result:** WI-0003 is Ready. Six criteria, each decidable by someone with a terminal and no
  context; the stakeholder's two answers are now checkable behaviour rather than prose; and the
  two things nobody has decided — an out-of-range stored ladder position, and how a ladder
  position is encoded — are named in `## Notes` for `plan` rather than left for `implement` to
  discover.

## 2026-08-30T03:55:25Z — plan v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` as the highest-ranked runnable item
  (priority high, rank 2); BUG-0001 and WI-0004 rank 3.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the six criteria, `## Out of scope`, and `## Notes`, which
    route two design questions here by name
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — both rounds, and every `[assumed]` entry
  - `tracker/items/WI-0003/history.md`, `journal.md`
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`
  - `docs/architecture/overview.md` (v2), `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v3),
    `ADR-0003` (v1, via `project.yaml`), `ADR-0004` (v1), `ADR-0005` (v1), `ADR-0006` (v1),
    `ADR-0007` (v1)
  - `docs/product/vision.md` (v4), `docs/process/using-recall.md` (v4)
  - `tracker/project.yaml`, `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`,
    `tracker/items/WI-0002/artifacts/plan.md`, `tracker/items/BUG-0001/item.md`
  - Source actually read: `recall/deck.py` (all), `recall/cli.py` (all), `recall/store.py`
    (`deck_path`, `load`, `save`, `_card_from`, `_card_to_entry`), `tests/support.py`,
    `tests/test_review.py`
- **Decisions:**
  - **`rung`'s meaning — decided, `ADR-0008` §2.** `ADR-0004` §2 calls it "the index into
    `ADR-0002`'s ladder" while `ADR-0002` §3 says a new card starts *below* the ladder; the two
    sentences do not pick out the same integer, and this item is the first to read the field
    back. Chose "the index of the gap the next correct answer applies", because it is the value
    `add` already writes and it satisfies `ADR-0004` §2 word for word. Route: **decided** — the
    item routed it here explicitly, and every observable date is identical under either reading,
    so it is not the stakeholder's.
  - **The arithmetic — decided, `ADR-0008` §3–§5**, transcribed from `ADR-0002` §4–§6: right
    applies `LADDER[rung]` then advances with a `min`; wrong resets to `FIRST_RUNG` and applies
    `LADDER[FIRST_RUNG]`; both count from the day of the sitting. Route: **documented** — the
    rule is the stakeholder's and this only fixes its form in code.
  - **An out-of-range stored `rung` is `DeckUnreadable` — decided, `ADR-0008` §6.** Not clamped:
    `ADR-0004` §5 refuses to repair a deck it cannot read, and `ADR-0006` §3 already treats a
    malformed later-added field exactly this way. Clamping would silently reschedule somebody's
    cards; leaving it undefined would produce an `IndexError` and a traceback, which is the shape
    `BUG-0001` was filed about. Route: **documented**, from two standing ADRs.
  - **The deck format version does not move — `ADR-0008` §7.** No key is added and none changes
    type; this tightens an existing field's legal values, and no deck ever written carries a
    `rung` other than `0` because nothing until now changed it.
  - **The printed line's wording — assumed, `## Assumptions` 1–3.** `ADR-0007` §2 leaves it here
    and AC4 fixes only the date's form. Chose `  next review: <YYYY-MM-DD> (in <n> days)`,
    indented to match the answer side. The parenthesised gap is not required by any criterion; it
    is there because the stakeholder chose the ladder with *"I don't want to be doing math to
    figure out when a card's coming back"*, and the date alone makes them subtract. Recorded as an
    assumption rather than an ADR because reversing it is editing one module constant. Route:
    **assumed**, reversible.
  - **The line is printed after `store.save`, not before — assumed.** A person is told only what
    is already on disk. One statement to move.
  - **Where the range check lives — assumed, `## Assumptions` 4.** The rejection itself is
    `ADR-0008` §6 and not an assumption; putting it in `store.py` rather than `deck.py` is, and it
    is what lets `record_answer` stay a total function over valid cards.
  - **No new module and no change to the three-layer split.** The overview has said since v1 that
    the scheduling rule belongs in `deck.py`; this plan puts it there and nothing else moves.
  - **`docs/architecture/overview.md` taken to v3 by this execution**, worded as what the design
    commits to rather than as what is built, because the code does not exist yet. Step 8 now asks
    `implement` to check it against what was actually built and to correct it only if the design
    moved — a version bump with no substantive change devalues every other one.
  - **Nothing was asked of the stakeholder.** No decision above is irreversible or turns on intent
    no document records, and both of this item's questions were answered before planning began.
  - **`BUG-0001` was not absorbed.** It touches the same call path — a filesystem error surfacing
    as a traceback — and fixing it here would make both changes unverifiable against their
    criteria. It is named under `## Risks` and under `## Out of scope for this item`.
- **Cross-answer check:** This execution recorded no new human answer and relied on four already
  consumed: `EP-001/Q-003` (the ladder and the two-way grade), `WI-0003/Q-001` (the ladder stops
  at a month), `WI-0003/Q-002` (the sitting says the next date), and `EP-001/Q-001` ("nothing
  fancier than that"). All four were checked when consumed — by `answer-questions` on
  2026-08-30T03:38:18Z for the two on this item — and re-read here against every decision this
  plan makes. Verdict: compatible in each case. `ADR-0008` decides an internal representation
  none of them speaks to; the printed line's wording is bounded by *"nothing fancier"* and adds
  one line and no accumulation; the ladder is transcribed, not reinterpreted. No ADR this
  execution wrote reconciles two of their statements, and no sentence in `docs/` sourced to one of
  their answers was rewritten (`lint-answers --uncommitted`, exit 0).
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 32 tests, OK (the declared test
    command, run against the current tree to confirm it works and to establish the baseline AC6
    is read against)
  - `.claude/agile-skills/scripts/lint-claims docs/architecture/adr/ADR-0008-what-rung-means-and-what-an-out-of-range-one-does.md`
    → exit 1 then, after adding one citation, exit 0
  - `.claude/agile-skills/scripts/lint-claims tracker/items/WI-0003/artifacts/plan.md` → exit 1
    then, after adding one citation, exit 0
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 7 consumed human answers
  - `.claude/agile-skills/scripts/validate-workspace` → exit 0, 6 items, 11 documents
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `every-criterion-is-addressed` → **pass**. The `## Acceptance criteria mapping` table in
    `plan.md` has one row per criterion, AC1 to AC6, each naming the steps that satisfy it and the
    specific observation that demonstrates it — not "tests". Three rows name the observation that
    would fail against the code as it stands today, which is the point of them: AC2(b) fails
    against a `record_answer` that moves the date and leaves the rung, AC3 fails against one that
    counts from the missed date, and AC4 fails against a printed constant.
  - `project-commands-resolved` → **pass**, unchanged. `commands.test` is
    `python3 -m unittest discover -s tests -t . -q` and `commands.lint` is
    `python3 -m compileall -q recall tests`; the test command was run by this execution and exited
    0 over 32 tests. `commands.build` is `null` and `ADR-0005` records why there is no build step.
  - `decisions-recorded` → **pass**. Eight choices, all listed in `plan.md`'s
    `## Decisions and ADRs` table with their route: three decided in `ADR-0008`, two already the
    stakeholder's in `ADR-0002` and `ADR-0007`, one already resolved in `ADR-0003`, and five
    recorded as reversible assumptions with what reversing each costs.
  - `plan-is-executable-without-you` → **pass (advisory)**. Nine numbered steps, each naming the
    files it touches and what is true afterwards. The two places a developer would otherwise have
    to decide something are removed: the encoding of `rung` (`ADR-0008` §2) and the wording of the
    printed line (`## Assumptions` 1). The one thing deliberately left open — whether the days
    remaining are computed by a helper in `deck.py` or a subtraction at the call site — carries the
    constraint that decides it: the ladder's numbers must not reach `cli.py`.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0). See the
    cross-answer bullet above.
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0). Two documents under
    `docs/` were touched and both are clean; two files were rejected on their first run for an
    unsourced absolute and both were repaired by adding the citation rather than by weakening the
    sentence.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` — new
  - `docs/architecture/adr/ADR-0008-what-rung-means-and-what-an-out-of-range-one-does.md` — new,
    v1
  - `docs/architecture/overview.md` — v2 → **v3**
  - `tracker/project.yaml` — unchanged; already resolved
  - `tracker/board.md` — regenerated
  - commit on `main`
- **Status:** `ready` → `planned`
- **Result:** WI-0003 is planned. Nine steps in three source files and two documents, with every
  criterion mapped to an observation that can actually fail. The two questions the item routed
  here are decided in `ADR-0008` — what `rung` counts, and that a value outside the ladder makes
  the deck unreadable rather than being clamped — and the only thing left to taste, the wording of
  the line the person reads, is fixed as an assumption so `implement` does not have to invent it.

## 2026-08-30T03:58:05Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next` as the highest-ranked runnable item (priority `high`, rank 2; `WI-0004` and `BUG-0001` are both rank 3).
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the six acceptance criteria, `## Out of scope`, and the `## Notes` recording what the stakeholder decided and what was routed to `plan`
  - `tracker/items/WI-0003/artifacts/plan.md` — nine steps, the criteria mapping, five assumptions
  - `tracker/items/WI-0003/history.md` — five rows, no send-back; this is a fresh execution, not a resumption
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both `answered`, both already propagated into `ADR-0002` v3 and `ADR-0007` before `refine` rewrote the criteria; nothing in them is unconsumed
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both set; `commands.build` is `null` with `ADR-0005` recording why
  - `docs/architecture/adr/ADR-0002` (the ladder), `ADR-0007` (the printed line), `ADR-0008` (what `rung` counts, and the out-of-range rule)
  - `docs/architecture/overview.md` v3, `docs/process/using-recall.md` v4
  - `recall/deck.py`, `recall/store.py`, `recall/cli.py`, `tests/support.py`, `tests/test_review.py`
- **Decisions:**
  - Start fresh rather than reconcile: `git branch` showed `wi/WI-0001` and `wi/WI-0002` and no `wi/WI-0003`, and the item is at `planned`, so no partial work exists to reconcile with.
  - Take the plan's five assumptions as given rather than re-deciding them. The wording of the printed line in particular is `plan`'s choice under `ADR-0007` §2, and `implement` choosing a different sentence would be re-litigating the plan.
- **Cross-answer check:** `none` — this entry edits no document.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → 0
- **Gates:**
  - `tests-pass` → **not yet run** — no code has changed; this gate belongs to the closing entry
  - `lint-clean` → **not yet run** — same
  - `workspace-valid` → **not yet run** as a completion gate; the transition runs it on the state this move produces
  - `every-criterion-has-a-test` → **not yet run** — no test has been written yet
  - `commits-reference-the-item` → **not yet run** — the branch has no commits of its own yet
  - `no-unplanned-scope` (advisory) → **not yet run** — there is no diff yet
  - `cross-answer-consistency` → **not yet run** — no document has been touched
  - `claims-are-sourced` → **not yet run** — same
- **Artifacts:**
  - branch `wi/WI-0003`, created from `main` at `a798a5e`, no commits of its own yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0003 has started on `wi/WI-0003`. The plan's nine steps are unchanged and nothing in them has been executed; the closing entry reports the work.

## 2026-08-30T04:06:16Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, this skill's own opening move; `plan.md`'s nine steps were unexecuted when the branch was cut.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `artifacts/plan.md`, `history.md`, `questions/Q-001.md`, `questions/Q-002.md`
  - `tracker/project.yaml` — both declared commands
  - `docs/architecture/adr/ADR-0002` (the ladder), `ADR-0004` (the deck file), `ADR-0006` (the grade), `ADR-0007` (the printed line), `ADR-0008` (what `rung` counts)
  - `docs/architecture/overview.md` v3, `docs/process/using-recall.md` v4
  - `recall/deck.py`, `recall/store.py`, `recall/cli.py`, `tests/support.py`, `tests/test_review.py`, `tests/test_storage.py`
- **Decisions:**
  - **`deck.days_until(due, today)` rather than a subtraction in `cli.py`.** Step 4's interface note left this open under one constraint — the ladder's numbers must not reach `cli.py`. A helper keeps `cli.py` free of date arithmetic as well, which is the same boundary the overview draws.
  - **The store-level range check got its own tests** (`LadderStorageTests`), though no acceptance criterion covers it. It is plan step 3 and `ADR-0008` §6, and it is the branch that lets `record_answer` index `LADDER` without re-checking; shipping it unexercised would leave the thing keeping a total function total untested.
  - **`docs/architecture/overview.md` was taken to v4, against step 8's "leave it alone if the design matches".** The design does match; what changed is tense. Version 3 was written at plan time and said "WI-0003's plan puts it there" and "once WI-0003 lands", citing the plan. On a merged trunk those describe pending work that is built. Two clauses now read as description and cite the code, and the change-log row says no design decision moved. Recorded as deviation 1 in `impl-report.md`.
  - **`recall/deck.py`'s module docstring was rewritten** for the same reason, one file lower down: it said the overview puts the arithmetic here "when WI-0003 arrives".
  - **The plan's five assumptions were taken as given, not re-decided.** In particular the printed line's wording is `plan`'s under `ADR-0007` §2; choosing a different sentence here would be re-litigating the plan.
  - **Decided not to decide:** nothing in the nine steps needed a decision this skill is not entitled to make, so no question was filed. Both of the item's questions were the stakeholder's, answered before this execution and already propagated into `ADR-0002` v3 and `ADR-0007`.
- **Cross-answer check:** `none`. Two documents were edited and neither carries a claim cited to one of the stakeholder's answers: `grep "Q-00" docs/process/using-recall.md` returns nothing, and the one such citation in `docs/architecture/overview.md` — `[src: WI-0002/Q-001]`, on the no-cap-on-a-sitting sentence — is in property 2, which this execution did not touch. `lint-answers --changed-since main` agrees, exit 0 over 7 consumed answers.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → 0
  - `python3 -m unittest discover -s tests -t . -q` → 0, **43 tests** (32 before this item)
  - `python3 -m compileall -q recall tests` → 0
  - `.claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → 0, all 6 commits name WI-0003
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → 0
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0
  - Two deliberate mutations, run and reverted, to show the suite can fail: reverting `record_answer` to the placeholder fails 10 cases; counting the gap from `card.due` instead of `today` fails exactly AC3's two.
  - A hand walk-through of AC1 to AC4 against `bin/recall` in a temporary `HOME`, printed in `impl-report.md`.
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 43 tests, on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0: 6 items, 11 documents, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass**. AC1 `test_a_correct_answer_walks_the_ladder_and_then_holds`; AC2 `test_a_wrong_answer_is_due_tomorrow_from_a_fresh_card` and `test_a_wrong_answer_resets_the_ladder_and_not_only_the_date`; AC3 `test_an_overdue_card_is_scheduled_from_the_day_of_the_sitting`; AC4 `test_the_sitting_prints_the_new_date_at_two_gaps_and_on_both_answers`, `test_the_date_comes_after_that_cards_answer_and_before_the_next_question` and `test_an_abandoned_sitting_prints_no_date`; AC5 `test_the_documentation_states_the_rule_and_the_worked_example`; AC6 the green suite plus four criteria read individually by ID, none waived. Every one of them fails against something: the mutation runs above name which.
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 6 commits)
  - `no-unplanned-scope` (advisory) → **pass**. Three source files, two test files, two documents. Every hunk traces to a plan step or to a recorded deviation; `BUG-0001` was left alone deliberately.
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` exit 0). See the cross-answer bullet.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0, 2 documents examined, no unsourced absolute)
- **Artifacts:**
  - `recall/deck.py` — `LADDER`, the real `record_answer`, `days_until`, rewritten module docstring
  - `recall/store.py` — the `rung` range check in `_card_from`
  - `recall/cli.py` — `NEXT_REVIEW_LINE`, `_next_review_line`, and the print after `store.save`
  - `tests/support.py` — `set_due`, which moves a card's `due` and nothing else
  - `tests/test_review.py` — `SchedulingTests`, `LadderStorageTests`, and three unit tests replacing the one that asserted the placeholder
  - `docs/process/using-recall.md` — v4 → **v5**
  - `docs/architecture/overview.md` — v3 → **v4**
  - `tracker/items/WI-0003/artifacts/impl-report.md` — new
  - branch `wi/WI-0003`, commits `88525dc..` (6 commits, `main` at `a798a5e`)
- **Status:** `in-progress` → `verifying`
- **Result:** The ladder is real. A right answer walks a card 1, 3, 7, 30 days and then holds at thirty; a wrong one sends it back to the start, rung as well as date; both count from the day of the sitting; and the sitting says the resulting date out loud after every answer. All eight gates pass on the branch head, and the two mutation runs show the suite would have caught both of the failures the plan's risk list named — the placeholder surviving a date-only check, and a gap counted from the day the card was due.

## 2026-08-30T04:12:05Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next` as the highest-ranked runnable item (priority `high`, rank 2).
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the six criteria, read **before** the implementation report, so that what would settle each one was derived from the criterion rather than from what was built
  - `tracker/items/WI-0003/history.md` — no send-back; this is a first verification
  - `tracker/items/WI-0003/artifacts/plan.md` — for the diff read and the declared assumptions
  - `tracker/items/WI-0003/artifacts/impl-report.md` — read as a claim to check, never cited as evidence
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/item.md` — the twenty-two criteria AC6 covers, read as text
  - `docs/process/using-recall.md` v5 — AC5 is decided by reading it
  - `tracker/project.yaml` — the two declared commands
  - the branch head, `c2c547ac34e7e956ff84c2dd459fc82400050ee0` on `wi/WI-0003`, working tree clean
- **Decisions:**
  - **No criterion was judged ambiguous.** All six state a procedure and a result. AC5's one soft edge — the document writes the third gap as *"a week"* rather than *"7 days"* — was resolved as a pass rather than a question: the criterion asks that a reader can work a date out by hand, "a week" is not ambiguous, and the worked example states the arithmetic explicitly (4 → 11). Recorded in the report so a reviewer can disagree with it visibly.
  - **No send-back and no bug item.** Nothing failed. `BUG-0001` was checked against this item's change and is untouched by it: the new `DeckUnreadable` from an out-of-range `rung` travels `ADR-0004` §5's existing route and produced a message and exit 3 rather than a traceback, which boundary case 5 demonstrates. Filing anything here would have been filing the bug that is already open.
  - **AC6 was answered by reading twenty-two sentences, not by reading the suite.** Each of `WI-0001` AC1–AC9 and `WI-0002` AC1–AC13 has its own verdict in the report, with a command for each. The suite is quoted as evidence for those verdicts. Non-intersection was looked for and none was found — every one of the twenty-two is exercised by something that also runs the new behaviour, because `WI-0001`'s all go through the changed `store.load` and `WI-0002`'s all through the changed `cmd_review`. Nothing waived.
  - **The verification was run in a temporary `HOME` with real here-documents**, because the criteria are written as literal `recall …` invocations driven by a here-document (`ADR-0001` §4). Reading the tests would have answered a different question.
  - **Independence is procedural here, not organisational**, and the report says so: the same agent implemented and verified, under different personas, in one session. Every check was re-derived from the criterion and re-run as a command; no criterion's evidence is `impl-report.md`.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → 0, `c2c547ac34e7e956ff84c2dd459fc82400050ee0`; `git status --short` → clean
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 43 tests … OK`
  - `python3 -m compileall -q recall tests` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, 6 items, 11 documents
  - AC1: `recall add …` then five cycles of "rewrite only `due` to today, `recall review` on a here-document answering `y`" → stored gaps today +1, +3, +7, +30, +30
  - AC2: (a) fresh card answered `n` → today + 1; (b) four right answers → today + 30, then wrong → today + 1, then right → today + **1**
  - AC3: a hand-written deck with `due` ten days past, answered `y` and answered `n` → presented both times, stored `due` = today + 1 both times
  - AC4: the dates printed in AC1's four sittings (`2026-08-31`, `2026-09-02`, `2026-09-06`, `2026-09-29`) each equal the string then in `due`; AC2(b)'s wrong answer printed today + 1; a two-card sitting printed `q-one`, `a-one`, the date, `q-two`, `a-two`, the date
  - AC5: read `docs/process/using-recall.md` v5 for the five facts, the worked example, and the absence of the two stale sentences
  - AC6: `recall list`/`add`/`review` runs for all twenty-two covered criteria — twenty-five due cards presented 25/25, a graded card not re-presented the same day, `recall list` identical before and after a sitting, an absent deck creating nothing, a blank side refused with the deck byte-identical, and the rest as quoted in the report
  - six boundary conditions triggered: abandoned at the reveal, abandoned at the grade prompt, an unrecognised response, nothing due, a stored `rung` of `-1`, `4` and `9` against two subcommands, and a truncated deck
  - six mutations applied and reverted for sensitivity (M1 the placeholder, M2 counting from `card.due`, M3 the cap removed, M4 the printed line deleted, M5 the range check removed, M6 the document reverted to `main`'s), each followed by `python3 -m unittest discover -s tests -t . -q`; suite confirmed green again afterwards
  - `git diff main..HEAD` read in full for unaccounted hunks
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 43 tests, on `c2c547a` with a clean tree)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0: 6 items, 11 documents, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass**. Six rows, six commands run by this skill, each with its actual output quoted. No row's evidence is the implementation report.
  - `negative-cases-exercised` → **pass**. Six boundary conditions *triggered*, not read about: the two abandonment points (which must print no date), the unrecognised response, the nothing-due path, three out-of-range `rung` values against two subcommands each, and a truncated deck. All quoted in the report.
  - `a-criterion-about-criteria-is-read` → **pass**. AC6 covers twenty-two criteria; all twenty-two are named by ID and carry a verdict read from their own sentence, with the suite as evidence rather than as definition. Non-intersection: none found, stated in those words. Nothing waived.
  - `tests-would-fail-without-the-change` (advisory) → **pass**. Every criterion has at least one test that fails when its behaviour is removed; the mutation table names which. M2 is the one that matters most — AC3's two tests are the only ones that catch a gap counted from the due date, and they survive M1, so without AC3 that reading would have shipped.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` — new, with `Verified-commit: c2c547ac34e7e956ff84c2dd459fc82400050ee0`
  - `tracker/items/WI-0003/item.md` — AC1 to AC6 ticked, all six on evidence gathered here
  - no bug item filed
  - commit on `wi/WI-0003`
- **Status:** `verifying` → `in-review`
- **Result:** WI-0003 passes on all six criteria, each demonstrated by a command run here against `bin/recall` rather than by reading a test. The ladder walks 1, 3, 7, 30 and holds; a wrong answer resets the position and not only the date; overdue cards are scheduled from the day of the sitting; the sitting names the date it stored. The twenty-two criteria `WI-0001` and `WI-0002` delivered were re-read one by one and all still hold, with nothing waived. Six mutations confirm the suite would notice each behaviour going missing.

## 2026-08-30T04:20:06Z — review-close v0.6.0 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next` as the highest-ranked runnable item (priority `high`, rank 2).
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the six criteria, all six ticked; `## Out of scope`; the whole of `## Notes`
  - `tracker/items/WI-0003/history.md` — eight rows, chaining without a gap, last row matching the status
  - `tracker/items/WI-0003/journal.md` — read in full, all nine entries
  - `tracker/items/WI-0003/artifacts/plan.md`, `impl-report.md`, `verify-report.md` — in full, including `## Deviations from the plan`, `## What I did not do` and `## Not verified, and why`
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both `answered`, both with `## Consequences` naming files I opened
  - the diff `main..wi/WI-0003` — 8 commits, 13 files, read hunk by hunk
  - `docs/architecture/adr/ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0007`, `ADR-0008`; `docs/architecture/overview.md` v4; `docs/process/using-recall.md` v5
- **Decisions:**
  - **Accept and close, `outcome: delivered`.** Every Definition of Done criterion passes with its own evidence; the merge result is green; the record reconstructs from the tracker, `docs/` and `git log --grep WI-0003` alone.
  - **F1 — the stale clause in `ADR-0008` `## Consequences` — is a recorded finding, not a send-back.** *"No deck file in any test carries a `rung` other than `0`"* was true when `plan` wrote it and this item's own §6 tests falsified it. It is not D12's: D12 is scoped to claims about the **behaviour** this item touched, and this is a statement about the test corpus supporting §7, which remains sound because those decks exist to be refused. Recorded in `review.md` F1 and in `item.md` `## Notes`.
  - **I attempted the `spec/doc-header.md` §4b erratum for F1 and reverted it**, rather than forcing a hard gate. Written properly — `## Corrections` row, change-log row, version bump — it made `cross-answer-consistency` fail with `answer.claim-rewritten-unasked`: `lint-answers` treats `## Consequences` as one paragraph block, that block also carries `[src: WI-0003/Q-001]`, and editing any bullet in it reads as rewriting a stakeholder-sourced claim. The escape its own hint names cannot be taken by the execution making the edit, because `transition` runs gates before it writes the journal. Forcing a hard gate over a low-severity stale clause is not a trade a review should make.
  - **Deliberately, this entry's cross-answer bullet names `WI-0003/Q-001`, which unblocks that repair for the next execution.** `journal_checks()` scans every journal in the workspace, so whoever next opens `ADR-0008` finds the gate already satisfied and can apply the erratum in one command. That is recorded in `item.md` `## Notes` so it is findable.
  - **F2 — fifteen decayed line-anchored citations across `ADR-0006`, `ADR-0007` and `ADR-0008` — is an accepted gap, not a defect of this change.** `spec/doc-header.md` §4a resolves a workspace-path citation when the file exists, so nothing fails; what is lost is the one-hop checkability the line numbers carried. Repairing them item by item is make-work; the durable fix is a convention that does not anchor to lines. Recorded in `review.md`, `item.md` `## Notes` and `HARNESS-STATUS.md`.
  - **`implement`'s deviation 1 — taking `overview.md` to v4 against plan step 8's "leave it alone" — was the right call and is accepted.** The design did not move; two clauses were commissive and would have read on a merged trunk as pending work that is built. The change-log row says in terms that no design decision moved, which is what stops the version bump from devaluing the others.
  - **No bug item filed.** `BUG-0001` is open, untouched and not made worse: the new `DeckUnreadable` from an out-of-range `rung` reports through `ADR-0004` §5's existing route, confirmed by verification's boundary case 5. F1 and F2 are record findings on this item and on the toolkit's citation convention, not defects in another item's delivered behaviour.
  - **The engagement is not over and no sign-off was filed.** `engagement-state EP-001` reports `active`, with `BUG-0001`, `WI-0003` and `WI-0004` in flight. Asking for sign-off now would ask about work nobody has stopped doing.
- **Cross-answer check:** this execution consumed no new human answer — it answered no question and recorded no reply. It did read one claim sourced to a stakeholder answer: `ADR-0008` `## Consequences`' bullet *"Changing the ladder — which the stakeholder said they might want if their deck grows [src: WI-0003/Q-001] — is editing `LADDER` and nothing else."* Checked against `WI-0003/Q-001` itself (*"If my deck gets huge later I might change my mind, but not now."*) and against `EP-001/Q-003`, which named the rungs: **compatible**, and untouched by this item — `LADDER` is one constant in one file, which is exactly what that sentence promises them, and nothing shipped here narrows it. The sentence is left byte-identical; the attempted §4b erratum on a neighbouring bullet in the same block was reverted for that reason, and naming `WI-0003/Q-001` here is what lets the next execution make it. `lint-answers --context work-item --changed-since main` → exit 0 over a non-degenerate window (*"2 path(s) differ from main (a798a5e) under docs"*), 7 consumed human answers checked.
- **Questions raised:** none
- **Commands:**
  - `check-verify-freshness WI-0003 wi/WI-0003` → 0, *"verified at c2c547ac; wi/WI-0003 has moved to d5fa9aa0 but only the record changed (5 file(s) under tracker/ or docs/)"*
  - `check-commit-refs WI-0003 wi/WI-0003` → 0, *"all 8 commit(s) on main..wi/WI-0003 name WI-0003"*
  - `git worktree add --detach <trial> main`; `git -C <trial> merge --no-ff wi/WI-0003` → clean, 13 files, 915 insertions; trial head `196df9aadd57306cbc0a8fb0a9fcb854eaceb895`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial** → 0, `Ran 43 tests … OK`; `python3 -m compileall -q recall tests` inside the trial → 0
  - `git worktree remove --force <trial>`; `git rev-parse main` → `a798a5e5…` before and after, unmoved
  - `lint-claims --context work-item --changed-since main` → 0, *"2 document(s) in 2 path(s) differ from main (a798a5e) under docs"*
  - `lint-answers --context work-item --changed-since main` → 0 (after the erratum was reverted; it had reported 1 error while the edit was in place)
  - `engagement-state EP-001` → *"EP-001 active — still in flight: BUG-0001, WI-0003, WI-0004"*
  - `validate-workspace .` → 0, 6 items, 11 documents
  - `grep -rnE "timedelta\(days=[0-9]+\)|\b(1, 3, 7|3, 7, 30)\b" recall/*.py` → one hit, `recall/deck.py:24`, for the "four numbers exist once" claim
- **Gates:**
  - `definition-of-done` → **pass**. Twelve criteria, each with its own result and evidence, in `review.md` `## Definition of Done`. D9 records the trial merge and the ordering the procedure requires; D12 records the twelve-claim audit table.
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; cross-checked by hand — `git diff --stat c2c547a..d5fa9aa` touches only `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 8 commits, run **before** the merge so the range is non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 43 tests … OK`, exit 0, run inside the detached trial worktree at `196df9a`, not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0: 6 items, 11 documents, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass**. Answered from the tracker, `docs/` and `git log --grep WI-0003` alone: *what was built* — the ladder, the reset, the overdue rule and the printed date, from `impl-report.md` and eight commit messages; *which skill decided what* — `refine` the criteria and AC4's date format, `plan` the encoding of `rung` and the line's wording, `implement` the `days_until` helper, the stakeholder the ladder itself; *what questions arose* — `Q-001` and `Q-002`, both theirs, both answered, both with `## Consequences` naming `ADR-0002` v3 and `ADR-0007`; *what verification found* — six passes on six commands, six boundary cases, six mutations, no defect.
  - `claims-are-sourced` → **pass**. `lint-claims --context work-item --changed-since main` exit 0, and the **scope it reports is not degenerate**: *"checked absolute claims: 2 document(s) in 2 path(s) differ from main (a798a5e) under docs; citations: every markdown file in the workspace"*. The read behind it is `review.md`'s twelve-claim table, each verdict taken from the cited thing.
  - `cross-answer-consistency` → **pass**. `lint-answers --context work-item --changed-since main` exit 0, window *"2 path(s) differ from main (a798a5e) under docs"*, 7 consumed answers checked. See the cross-answer bullet — including the one error it reported while the reverted erratum was in place, which is finding F1.
  - `epic-sign-off` → **not applicable this execution, and not skipped silently**: this is a work-item close, not an ending. `engagement-state EP-001` → `active`, three children in flight, so there is nothing to sign off and no sign-off question is owed.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` — new
  - `tracker/items/WI-0003/item.md` — `status: done`, `outcome: delivered`, and `## Notes` gains F1, F2 and the carried-forward `overview.md` line
  - `docs/architecture/adr/ADR-0008-…md` — **unchanged**; the attempted §4b erratum was reverted and is recorded as F1 instead
  - no bug item filed
  - the merge of `wi/WI-0003` into `main`, performed immediately after this close; its sha is recorded in the commit that follows
- **Status:** `in-review` → `done`
- **Result:** WI-0003 is delivered. The scheduling the epic is named for is real and visible: a right answer walks a card 1, 3, 7, 30 days and then holds, a wrong one sends it back to the start — position as well as date — both counted from the day of the sitting, and the sitting says the resulting date out loud after every answer. Twelve Definition of Done criteria pass on their own evidence, the merge result is green over 43 tests, and two low-severity record findings are written into the item's `## Notes` rather than closed over.
