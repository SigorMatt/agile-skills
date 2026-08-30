# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T11:08:42Z — intake v0.3.0 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly. The workspace had a `tracker/` with `project.yaml` but zero items and zero documents; the stakeholder's idea was waiting in `IDEA.md`. No request under `tracker/requests/` dispatched this, so step 0 of the procedure does not apply.
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, in their own words
  - `SIMULATION-NOTICE.md` — establishes that the stakeholder answers asynchronously, in files, and is not in this session
  - `CONSUMER-PROMPT.md`
  - `tracker/project.yaml` (name `recall-4c`, trunk `main`, all three `commands.*` null)
  - `tracker/items/` — empty; highest allocated IDs were none, confirmed by `scripts/new-item --next-id`
  - `docs/product/vision.md` — did not exist
  - `.claude/agile-skills/spec/` — `work-item.md`, `ids-and-statuses.md`, `journal-and-history.md`, `question.md`, `doc-header.md`
- **Decisions:**
  - **The idea is shapeable, so an epic was created rather than refusing.** The procedure's impasse test is whether there is an observable outcome, a user and a constraint. All three are present in one sentence: a person studying something, cards that come back on a schedule, and state that survives a restart. It is thin, but it is not empty, and the thin parts are questions rather than guesses.
  - **The stakeholder's sentence is quoted verbatim and never paraphrased into a requirement.** It appears in `EP-001` `## Why now` and in `docs/product/vision.md`. Everything else in the epic is marked as derivation, so a later reader can tell the two apart. The simulation notice forbids recording that a real person said something, so the record says "the stakeholder stated" and attributes nothing further.
  - **Split into two items, not four.** The candidates were: add a card; store cards; select what is due; grade and reschedule; persist the schedule. Storage and persistence are not separately deliverable — a card that is added but not stored fails the stakeholder's own "progress persists" — so they collapse into the item that adds cards. Selecting what is due and rescheduling are likewise one deliverable: a session that shows due cards but never updates the schedule produces an identical day tomorrow, which is not an increment anybody could observe. That leaves `WI-0001` (add a card, it survives a restart) and `WI-0002` (review what is due, reschedule it). Rationale for stopping at two: each item costs a full plan/implement/verify/review pipeline, and the procedure's stated failure mode is splitting too finely.
  - **Ordering is derived, not guessed.** The stakeholder's own sentence orders it — "add cards, review due cards daily" — and a review session is untestable with no cards, so `WI-0002` carries `depends-on: WI-0001` and `WI-0001` is `critical`.
  - **The `## Out of scope` list is intake's inference and is labelled as such.** The stakeholder mentioned no exclusions. Eight were derived from what a reasonable reader would assume is included — decks and tags, multiple users, syncing, editing or deleting cards, importing other formats, media on cards, reminders, statistics. Recording them now is nearly free and prevents an argument at review. Because they are our inference rather than their words, `Q-004` lists all eight back to the stakeholder and invites them to contradict any of it.
  - **Four questions were filed rather than asked in conversation, because the stakeholder is not in this session** (`SIMULATION-NOTICE.md`). The procedure prefers asking now; the applicable route is its own "the human leaves mid-intake" case — finish what is unambiguous, file the rest as questions addressed to `human` on the epic, suspend the epic, stop. Three are blocking and one is the elicitation.
  - **Why these three blocking questions and no more.** `Q-001` (how the person interacts with the tool) is the one nothing on disk can answer — the repository has no code, no language and no framework to fit into — and it decides how every criterion in both items is written. `Q-002` (what the spacing rule does) is the product's core behaviour; "simple" bounds it but does not specify it. `Q-003` (what makes a card due on a given day) is what turns "review due cards daily" into something a person with a terminal could decide. Each is one decision in one file, per `spec/question.md`.
  - **What was deliberately not asked.** The grading scale is downstream of `Q-002` and would have to be re-asked once the rule is chosen. Whether there are multiple decks was put into `## Out of scope` instead of a question, because the stakeholder described one pile of cards and inventing a question to fill a batch is the failure mode the protocol warns about. Both are recorded so that "not asked" is distinguishable from "forgotten".
  - **`commands.*` in `project.yaml` were left null.** There is no test, lint or build command in this repository, and inventing one would make the first `tests-pass` gate report a pass for a command nobody can run. `plan` owns filling these in.
- **Questions raised:**
  - `EP-001/Q-001` (blocking, to human) — how the person interacts with the tool: command line, local web page, full-screen terminal app, or something else.
  - `EP-001/Q-002` (blocking, to human) — what "simple spaced repetition" does: a fixed Leitner ladder, SM-2, two intervals only, or intervals they name.
  - `EP-001/Q-003` (blocking, to human) — what makes a card due on a given day: calendar days in local time, elapsed hours, or a day that starts at a chosen hour.
  - `EP-001/Q-004` (non-blocking, to human, `kind: elicitation`) — what else matters to them that we have not asked about, with the eight inferred exclusions listed back to them to push against.
  - **Verbatim answers recorded:** none. The stakeholder is asynchronous and was not present in this session, so no answer was given to any of the four. All four `## Answer` sections are empty and all four questions are `open`. Nothing in this record claims otherwise.
- **Commands:**
  - `scripts/new-item --next-id epic` → exit 0, `EP-001`
  - `scripts/new-item --next-id work-item` → exit 0, `WI-0001`
  - `scripts/new-item --id EP-001 --type epic --status open --actor intake` → exit 0
  - `scripts/new-item --id WI-0001 --type work-item --epic EP-001 --priority critical --status draft --actor intake` → exit 0
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 --priority high --status draft --actor intake` → exit 0
  - `scripts/lint-answers --item EP-001 --require-elicitation` → exit 0, "0 errors, 0 warnings", one open question on file
  - `scripts/lint-claims --all` → exit 0, "0 errors, 0 warnings"
  - `scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `scripts/validate-workspace .` → exit 1 before journalling (4 × `journal.execution.missing` and `question.blocking.not-suspended`, both expected mid-execution), re-run to exit 0 after this transition
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .`, exit 0 after this transition; the errors seen mid-execution were the missing journal entries this transition writes and the suspension this transition performs)
  - `epic-has-success-measures` → **pass** — the five measures in `EP-001` `## Success measures` are each checkable by a person: add a card and restart, then see it offered; compare the session's card set against the stored schedule; compare two cards' next-due dates after opposite gradings; run a second session the same day; kill the tool mid-session and check nothing answered was lost. None of them is the goal restated with "successfully" in it. The third measure deliberately says "in the direction the stakeholder confirms is wanted" rather than naming a direction, because `Q-002` is unanswered.
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation` → exit 0; the elicitation is `EP-001/Q-004`, `blocking: false`, `addressed-to: human`, filed at the start of the engagement where an answer is cheapest to act on)
  - `items-are-separable` (advisory) → **pass** — `WI-0001` is buildable first and depends on nothing; `WI-0002` depends on it and is buildable second. Each delivers something a person could observe on its own.
  - `no-solution-in-the-problem` (advisory) → **pass** — the epic, both stories and all eleven criteria name no language, framework, library, command, file format or algorithm. The three scheduling algorithms and the three interaction styles appear only inside `Q-002` and `Q-001` as options put to the stakeholder, which is where an undecided choice belongs. One thing was removed in drafting: `WI-0001` AC5 originally required the store to be "a file (or files) a person can locate and read", which named a technology the stakeholder did not; it now requires only that the stored data be inspectable without running the tool, and `WI-0001` `## Notes` records that even that much is intake's addition.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` (new)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (new)
  - `tracker/items/WI-0001/item.md` (new) and `tracker/items/WI-0002/item.md` (new), with their `journal.md` and `history.md`
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` (`project.description` filled in; `commands.*` left null)
  - `tracker/board.md` (regenerated)
- **Status:** `open` → `awaiting-answer`
- **Result:** EP-001 exists with a goal, five checkable success measures and an explicit out-of-scope list, and two work items sit at `draft`. Four questions are open with the stakeholder — three blocking, one elicitation — so the epic is suspended at `awaiting-answer` with `resume-to: open`. Nothing was designed and no technology was chosen.

## 2026-08-30T11:09:28Z — intake v0.3.0 — product-analyst

- **Item:** EP-001
- **Trigger:** correction, same `intake` execution as the entry above. Not a new dispatch.
- **Inputs read:**
  - `tracker/items/WI-0001/journal.md`, `tracker/items/WI-0002/journal.md` (the entries this execution had just written)
  - `.claude/agile-skills/spec/journal-and-history.md` §2.2
- **Decisions:**
  - **Two journal `**Status:**` bullets were repaired in place rather than corrected by appending.** Both said ``` `draft` → `draft` (unchanged; the `— → draft` row was written by `scripts/new-item`) ```. `validate-workspace` parsed the trailing parenthetical as part of the transition and reported `journal.status.unmatched` — "entry claims — → draft → scripts/new-item but history.md has no such row" — on both items. The claim in the bullet was never wrong; its formatting was. An appended correction entry cannot clear this finding, because the malformed text stays on disk and the check keeps firing, so the workspace would have stayed invalid for ever. The parenthetical was reduced to `(unchanged)`; nothing else in either entry was touched, and the fact that `scripts/new-item` wrote the `— → draft` row is already in each item's `history.md` under `actor`.
  - This is recorded here rather than silently, because editing an append-only file is exactly the thing the record must not hide.
- **Questions raised:** none
- **Commands:**
  - `scripts/validate-workspace .` → exit 1, 2 × `journal.status.unmatched`
  - `scripts/validate-workspace .` (after the repair) → exit 0, "0 errors, 1 warning" (the warning is `commands.test` being null, which `plan` owns)
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0)
  - `epic-has-success-measures` → **skipped** — judged in the entry above; this correction did not touch the epic body.
  - `an-open-question-was-asked` → **skipped** — judged in the entry above; this correction filed no question and removed none.
  - `items-are-separable` (advisory) → **skipped** — this correction did not change the item set.
  - `no-solution-in-the-problem` (advisory) → **skipped** — this correction did not change any title, story or criterion.
- **Artifacts:**
  - `tracker/items/WI-0001/journal.md` (one line repaired)
  - `tracker/items/WI-0002/journal.md` (one line repaired)
- **Status:** `awaiting-answer` → `awaiting-answer` (unchanged)
- **Result:** The workspace validates. A note for whoever maintains the toolkit: `validate-workspace` reads the whole `**Status:**` line as the transition, so a parenthetical after the arrow becomes a bogus actor. The spec's own example bullet is bare, so this is a strictness worth knowing rather than a defect, but the error message points at a transition nobody claimed.

## 2026-08-30T11:20:13Z — answer-questions v0.4.0 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` — four questions addressed to the human on this epic had `## Answer` filled in; dispatched by the orchestrator's rule that only `answer-questions` may consume a human reply
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (all four with the stakeholder's replies)
  - `tracker/items/EP-001/item.md`, `history.md` (the suspending row carries `resume-to: open`), `journal.md`
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/` — empty; no prior decision existed to contradict
  - `tracker/project.yaml`; `.claude/agile-skills/spec/question.md`, `doc-header.md`, `journal-and-history.md`; `.claude/agile-skills/scripts/pipeline.yaml` (creation authority for a scope-widening item)
  - no `refinement-qa.md` and no `plan.md` exist yet — nothing has been refined or planned
- **Decisions:**
  - **Q-001 → answered from the human's reply.** The surface is a command-line tool: *"Command-line is fine — it's just me, once a day at a terminal, running through vocab."* Recorded as `ADR-0001-command-line-delivery-surface.md` rather than only in the question, because the surface is what every criterion on WI-0001 and WI-0002 is written against and `plan` reads ADRs, not the Q&A.
  - **Q-002 → answered from the human's reply, with two derived decisions.** Binary grading on the ladder 1, 3, 7, 30 days, wrong returning to the start. The stakeholder did not say what a card already at a month does, and did not say when a brand-new card first becomes due; code cannot avoid settling both. Decided: a card at the top rung stays there (the option text they answered against said *"then stays at 30"*), and a new card is due on the day it was added (WI-0001 AC4 already required a new card to be due, and under Q-003's rule "due" is a date). Both are recorded in `ADR-0002-scheduling-binary-ladder.md` marked as the architect's inference rather than as their words — the distinction the record has to keep.
  - **Q-003 → answered from the human's reply.** Due is a calendar-date comparison in the machine's local date; missed days accumulate unpenalised; a second session the same day re-offers nothing already answered. The last of those needed no rule of its own: every outcome of a review sets the next due date at least a day ahead, so it falls out of the ladder.
  - **Q-004 (elicitation, non-blocking) → answered, and it moved three things.** A card is a front and a back of one line each; the data lives in a file on their machine that survives a reboot; they want to delete a card and editing can wait; losing progress or a review over a couple of minutes would make the tool a failure; and how it is built is delegated to us. Deletion contradicted the epic's out-of-scope list — which was intake's inference, and Q-004 exists to invite exactly that contradiction — so it was filed as **WI-0003** at `draft` with `arose-from: EP-001/Q-004`, not folded into WI-0001.
  - **Escalated `EP-001/Q-005` rather than reconciling two of their sentences.** *"No cap on how many come up at once — whatever's due, all of it"* (Q-003) and *"a review taking more than a couple minutes to get through"* would be a failure (Q-004) cannot both hold on a backlog, which their own "a missed day is just still due" makes likely. Condition 1 of `spec/question.md` §4 applies: the answer depends on intent no document records. Both sentences are quoted by ID in the question, the options are their two positions plus a middle one, and the recommendation is `none — this is yours to settle`, because choosing between two of the stakeholder's own statements is the move ADR-0008 §3 refuses.
  - **Did not batch further questions.** The next open things — what the commands are called, the order due cards are offered in, how a card is identified for deletion — belong to `refine` on items it has not yet reached, and inventing them to fill a round is the failure mode the batching rule warns about.
  - **Epic stays at `awaiting-answer`.** Its recorded `resume-to` is `open`, but `Q-005` is blocking and open, so returning it would assert that the engagement can proceed past a question that is not answered.
- **Cross-answer check:**
  - `EP-001/Q-001` — checked against Q-002, Q-003, Q-004: **compatible** with all three; the surface is orthogonal to the schedule, and Q-004's "a file on my machine" and "whatever you think is best" reinforce it. The paragraph in `docs/product/vision.md` sourced to Q-001 was rewritten in this execution, and the rewrite is an ordinary repair: v1 said the four questions were unanswered, which their reply made false as a statement about the record — no claim of theirs was overtaken or contradicted, and the new text quotes their sentence in full.
  - `EP-001/Q-002` — checked against Q-001, Q-003, Q-004: **compatible** with all three. The vision paragraph sourced to Q-002 was rewritten in this execution, and this too is an ordinary repair rather than an overtaken claim: v1 said *"Which rule, exactly, has not been decided yet — it is open with the stakeholder as `EP-001/Q-002`"*, which is a statement about the state of the record and stopped being true when they answered. Their own sentence now stands quoted in `## The spacing rule` rather than paraphrased.
  - `EP-001/Q-003` — checked against Q-001, Q-002, Q-004: compatible with the first two; **conflicts** with Q-004 on session size, escalated as `EP-001/Q-005` quoting both by ID.
  - `EP-001/Q-004` — checked against Q-001, Q-002, Q-003: compatible with the first two; **conflicts** with Q-003, the same conflict, recorded in both directions. Its contradictions of the epic's out-of-scope list are not cross-answer conflicts — that list is ours, not theirs — and were routed into WI-0003 and the epic's scope.
- **Questions raised:** `EP-001/Q-005` (blocking, to human) — which of their two statements wins when more cards are due than fit in a couple of minutes
- **Commands:**
  - `scripts/new-item --id WI-0003 … --actor answer-questions --arose-from EP-001/Q-004` → exit 0
  - `scripts/lint-answers --item EP-001` → exit 0, 4 consumed human answers checked
  - `scripts/lint-answers --item EP-001 --uncommitted` → exit 0 after this entry; it had reported `answer.claim-rewritten-unasked` twice against `docs/product/vision.md` until the `**Cross-answer check:**` bullets above were written
  - `scripts/lint-claims --uncommitted` → exit 0 (one `claim.unsourced` in ADR-0001 fixed by citing ADR-0002, WI-0001 and WI-0002)
  - `scripts/validate-workspace .` → exit 0, 0 errors, 1 warning (`commands.test` is null — `plan`'s to fill)
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in the four `## Consequences` sections was opened and carries the change: `ADR-0001` and `ADR-0002` exist; `docs/product/vision.md` is at v2 with the spacing rule, the surface, what a card is, deletion and both failure modes; `tracker/items/EP-001/item.md` has the rewritten success measures, scope and out-of-scope; `WI-0001/item.md` has AC1–AC5 rewritten; `WI-0002/item.md` has nine criteria written from the ladder and the due-date rule; `WI-0003/` exists; `Q-005.md` exists.
  - `answered-from-the-record` → **pass** — three answers are the stakeholder's own sentences, quoted; the two things they did not say are recorded as decisions in ADR-0002 with their basis and marked as inference.
  - `escalation-is-justified` → **pass** — `Q-005`, condition 1 of `spec/question.md` §4 (intent no document records), stated in its `## Context`. It is not an effort escalation: the work of answering it is trivial and the authority to answer it is what is missing.
  - `cross-answer-consistency` → **pass** — `scripts/lint-answers --item EP-001`, exit 0; and with `--uncommitted`, exit 0.
  - `workspace-valid` → **pass** — `scripts/validate-workspace .`, exit 0.
  - `item-resumed-correctly` → **skipped, deliberately** — the epic is not being resumed. Its `resume-to` is `open` (the intake row of 2026-08-30T11:08:42Z), and a new blocking question, `Q-005`, is open, so step 7 keeps it at `awaiting-answer`.
  - `a-deferral-is-not-an-answer` → **skipped** — none of the four replies deferred. Q-004's *"whatever you think is best"* is the nearest, and it is an authorisation to decide rather than a "not yet": it settles who chooses, so it is recorded as an answer, with the delegation written into ADR-0001 for `plan` to act on.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — `status: answered`, `answered-by: human`, `answered-at` stamped, `## Cross-answer check` and `## Consequences` written
  - `tracker/items/EP-001/questions/Q-005.md` (new) — the conflict between Q-003 and Q-004, addressed to the human, blocking
  - `tracker/items/EP-001/item.md` — success measures rewritten from the answers; scope gains deletion and the command line; out-of-scope narrowed to editing and extended with a graphical interface; `## Notes` added for the open tension and the delegated technology choice
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — criteria rewritten (journalled on those items)
  - `tracker/items/WI-0003/` (new) — "Delete a card", `draft`, `arose-from: EP-001/Q-004`
  - `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md` (new)
  - `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md` (new)
  - `docs/product/vision.md` — v1 → v2, change-log row added
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `awaiting-answer` (unchanged)
- **Result:** All four stakeholder answers are consumed and propagated into two ADRs, the vision at v2, the epic, both existing work items and one new one. The epic stays suspended: `EP-001/Q-005` puts the one thing this execution refused to decide — which of two of their own statements about session size wins — back to the stakeholder.

## 2026-08-30T11:20:59Z — answer-questions v0.4.0 — architect

- **Item:** EP-001
- **Trigger:** a gate failure inside the same `answer-questions` execution as the entry above — `scripts/lint-answers --item EP-001 --uncommitted` reported `answer.claim-rewritten-unasked` three times after that entry was written
- **Inputs read:**
  - `.claude/agile-skills/scripts/lint-answers` (rule 3: `journal_checks`, `JOURNAL_BULLET_RE`)
  - `docs/product/vision.md` (v1 as committed, against v2 as written) — the two rewritten paragraphs at lines 38 and 67
  - `tracker/items/EP-001/journal.md` (the entry above)
- **Decisions:**
  - Appended this entry rather than editing the one above. Rationale: `journal.md` is append-only and the entry above is not wrong — it says exactly what was checked and why the two vision rewrites are ordinary repairs. What it does is put the answer IDs on sub-bullets under `**Cross-answer check:**`, and `lint-answers` matches only the text on the bullet line itself, so nothing it named was visible to the gate. The single line below carries the same content in the shape the gate can read.
  - Recorded the mismatch as a toolkit defect rather than working around it silently. `spec/question.md` §2 and this skill's own procedure both show the cross-answer check as a heading followed by one sub-bullet per answer, and `journal_checks` reads `^\s*[-*]\s*\*\*Cross-answer check:\*\*(?P<rest>.*)$` — one line, nothing beneath it. A compliant entry therefore fails rule 3 unless the IDs are also repeated inline.
- **Cross-answer check:** EP-001/Q-001 — compatible with EP-001/Q-002, EP-001/Q-003 and EP-001/Q-004; EP-001/Q-002 — compatible with EP-001/Q-001, EP-001/Q-003 and EP-001/Q-004; EP-001/Q-003 — conflicts with EP-001/Q-004 on session size, escalated as EP-001/Q-005; EP-001/Q-004 — the same conflict with EP-001/Q-003, recorded in both directions. The two paragraphs of `docs/product/vision.md` rewritten under citations to EP-001/Q-001 and EP-001/Q-002 are ordinary repairs and not overtaken claims: both said the questions were still open with the stakeholder, which their replies made false as statements about the record, and neither paraphrased anything they said. Their sentences are now quoted verbatim instead. Full per-answer reasoning is in the entry above.
- **Questions raised:** none
- **Commands:**
  - `scripts/lint-answers --item EP-001 --uncommitted` → exit 1, 3 × `answer.claim-rewritten-unasked` (before this entry)
  - `scripts/lint-answers --item EP-001 --uncommitted` → exit 0 (after it)
- **Gates:**
  - `answer-is-propagated` → **pass** (unchanged from the entry above; no artifact changed here)
  - `answered-from-the-record` → **pass** (unchanged)
  - `escalation-is-justified` → **pass** (unchanged: `EP-001/Q-005`, condition 1)
  - `cross-answer-consistency` → **pass** — this entry is what makes it pass; exit 0 above
  - `workspace-valid` → **pass** (`scripts/validate-workspace .`, exit 0)
  - `item-resumed-correctly` → **skipped** (the epic is not resumed; `Q-005` is open and blocking)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred)
- **Artifacts:**
  - `tracker/items/EP-001/journal.md` (this entry; no other file changed)
- **Status:** `awaiting-answer` → `awaiting-answer` (unchanged)
- **Result:** The cross-answer check for all four consumed answers is now readable by `lint-answers`, which passes. The gate and the journal format it checks disagree about where the answer IDs live, and that is written up here rather than papered over.

## 2026-08-30T11:27:17Z — answer-questions v0.4.0 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer`, dispatched by the harness after the stakeholder wrote an
  answer into `EP-001/Q-005`; consuming an answered human question is this skill's precondition 1
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` (the answer being consumed)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (the prior human
    answers, for the cross-answer check)
  - `tracker/items/EP-001/item.md`, `history.md` (the `resume-to` on the row that suspended it:
    `open`)
  - `tracker/items/WI-0002/item.md`, `history.md` — the item whose criteria the answer changes
  - `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`,
    `ADR-0002-scheduling-binary-ladder.md` (v1 — it names this question as the thing it does not
    resolve)
  - `docs/product/vision.md` (v2)
  - `.claude/agile-skills/spec/question.md`, `spec/journal-and-history.md`, `spec/doc-header.md`
- **Decisions:**
  - The answer is the stakeholder's own, so route (2) — recorded intent — settles it, and the whole
    of the work was propagation. Their words: no cap, the honest count up front, quitting part-way
    without loss. `ADR-0003` records it so that WI-0002 and `plan` have one place to cite, rather
    than three items quoting a question file.
  - **The session does not estimate how long it will take.** This is my inference and is labelled
    as such in `ADR-0003`: option C as put to them offered "how many are due and roughly how long
    that is", and their answer restated only the count — *"the honest number of cards waiting"*.
    Nothing in the record says how fast this person reads a card, and `ADR-0002` stores nothing
    from which a duration could be derived, so a printed estimate would be a number the tool
    invented. Reversible: it needs timing data to be stored before it could be built anyway.
  - **No criterion bounds session length, on any item.** Their answer trades the couple-of-minutes
    bound for visibility, so writing a length criterion now would contradict the answer that just
    arrived. Recorded in WI-0002's `## Notes` as an instruction to `refine`, because `refine` is
    the next skill to touch that item and the tempting move is to add one.
  - Amended WI-0002's acceptance criteria rather than filing a new item. Step 3b's rule is about
    an answer implying work no item records; this answer is about what a review session shows, and
    a review session is exactly WI-0002 — the question itself was filed saying it would change
    that item's criteria. The item is at `draft`, so the criteria are not yet frozen.
  - Kept AC2's literal no-cap wording and added AC10 and AC11 beside it, rather than folding
    everything into one criterion. Three separate things are decidable separately: what is
    offered, that the count is stated, and that stopping is supported.
- **Cross-answer check:** EP-001/Q-005 checked against EP-001/Q-001, EP-001/Q-002, EP-001/Q-003
  and EP-001/Q-004 — all four compatible, no conflict declared, nothing escalated. Q-005 is
  itself the resolution of the Q-003/Q-004 conflict that a previous execution escalated, so
  reading it as a fresh conflict with Q-004 would put a question back to them that they have just
  answered. Detail:
  - `EP-001/Q-003` — compatible and affirmed: "no cap" then, "don't cap it" now.
  - `EP-001/Q-004` — compatible as a reconciliation: the couple-of-minutes sentence stands as a
    design pressure and is no longer treated as a constraint on any criterion, which is written
    into `ADR-0003` and the vision rather than left implicit.
  - `EP-001/Q-002` — compatible: it decides when a card falls due, not which due cards a session
    shows. No interval changed.
  - `EP-001/Q-001` — compatible: a stated count and a quit key are things a command-line session
    does.
- **Questions raised:** none — the record answered this one, and no new conflict was found
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition, with
    exactly the two errors the transition clears (`board.stale`, `question.awaiting.none-open`)
  - `python3 .claude/agile-skills/scripts/lint-answers --item EP-001` → exit 0, 5 consumed human
    answers checked
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 2 uncommitted docs
    paths in the claim window
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → run after the transition
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition and
    the board regeneration
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in Q-005's `## Consequences` was opened
    and carries the change: `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`
    exists at v1; `WI-0002/item.md` has AC2 amended and AC10 and AC11 present; `EP-001/item.md`
    has the two new success measures and the rewritten `## Notes`; `docs/product/vision.md` is at
    v3 with the reconciliation quoted and nothing recorded as open.
  - `answered-from-the-record` → **pass** — the answer is the stakeholder's own text in
    `EP-001/Q-005`, quoted verbatim in `ADR-0003` and in the vision; the one part not in their
    words (no duration estimate) is recorded as the architect's inference with its basis.
  - `escalation-is-justified` → **skipped** — nothing was escalated this execution. The
    escalation that produced Q-005 was justified by `spec/question.md` §4 condition 1 and is
    recorded in that question's `## Context`.
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001`, exit 0; and
    `--uncommitted`, exit 0, which is the rule-3 half over the documents this execution rewrote)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after this transition and
    `board-gen`; the one remaining warning is `commands.test` still null, which is `plan`'s)
  - `item-resumed-correctly` → **pass** — the row that suspended EP-001 (2026-08-30T11:08:42Z,
    `open` → `awaiting-answer`, actor `intake`) records `resume-to: open`, and this execution
    returns it to `open`.
  - `a-deferral-is-not-an-answer` → **skipped** — the reply decides the question outright; there
    is no deferral on this item.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-005.md` — `status: answered`, `answered-by: human`,
    `answered-at` set; `## Cross-answer check` and `## Consequences` written
  - `docs/architecture/adr/ADR-0003-session-composition-no-cap-stated-count-clean-quit.md` (new,
    v1)
  - `docs/product/vision.md` (v2 → v3)
  - `tracker/items/EP-001/item.md` — success measures and `## Notes`
  - `tracker/items/WI-0002/item.md` — AC2 amended, AC10 and AC11 added, `## Notes` rewritten
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `open`
- **Result:** The stakeholder's answer to Q-005 is consumed and propagated: a review session
  offers every due card, says how many before the first one, and can be stopped part-way without
  loss, with no criterion bounding session length. EP-001 returns to `open` with nothing open
  against it.

## 2026-08-30T11:50:33Z — answer-questions v0.4.0 — architect

- **Item:** EP-001
- **Trigger:** Written by the second of two `answer-questions` executions on 2026-08-30, which
  consumed four stakeholder answers across WI-0001 and WI-0003. It is on the epic because two of
  those answers changed what the engagement will and will not deliver, and a scope decision that
  lives only on a child item is invisible to anyone reading the epic.
- **Inputs read:** `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md`;
  `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md`; `docs/product/vision.md` v3.
- **Decisions:** none taken here. This entry records, at epic level, four decisions taken on the
  child items and their consequence for the shape of the engagement:
  - **Two things left the scope, by the stakeholder's own decision rather than our inference.**
    A command to list or search the cards: offered to them as the way to name a card for deletion,
    and declined — *"I don't need a numbered list for this"* (`WI-0003/Q-001`). And an undo, trash
    or archive: offered as the protection against a wrong deletion, and declined in favour of a
    confirmation prompt (`WI-0003/Q-002`). Both are now exclusions in `docs/product/vision.md` with
    their words on them. Neither is deferred work waiting to be scheduled, and no work item was
    filed for either — which is the point of recording it here, because "declined" and "not yet
    scoped" look identical on a board.
  - **One promise was added that binds every later version.** The card file is human-readable text
    and stays that way (`WI-0001/Q-002`,
    `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md`). It is the
    only commitment in the engagement that is expensive to reverse, because the stakeholder's real
    study history accumulates in it, and losing that history is one of the two failures they named
    (`EP-001/Q-004`).
  - **One product behaviour was fixed across two items.** Two cards may share a front side
    (`WI-0001/Q-001`), which is why deleting by front side can be ambiguous and why WI-0003 carries
    a criterion for choosing among matches
    (`docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md`).
    The two items cannot be read independently on this point.
- **Cross-answer check:** performed per answer on the four child question files and summarised in
  each child item's journal. No answer conflicted with any prior recorded answer, so no question
  was put back to the stakeholder under ADR-0008's obligation. The one pairing worth naming at epic
  level is `EP-001/Q-005` against `WI-0003/Q-002`: there they refused a cap because they did not
  want the tool between them and their cards, here they asked for a prompt that is exactly that.
  Not a contradiction — one is about withholding cards they want to see, the other about destroying
  a card they may not have meant to name — and nothing was reconciled by us.
- **Questions raised:** none.
- **Commands:** none — the gate commands for these decisions were run on the child items and are
  recorded in their journals.
- **Gates:** none apply to this entry; it records no transition and takes no decision. The gates
  for the two executions it summarises are recorded in full on `tracker/items/WI-0001/journal.md`
  and `tracker/items/WI-0003/journal.md`.
- **Artifacts:** `docs/product/vision.md` — version 3 → 5 across the two executions, with a
  change-log row for each; `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md`
  and `ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md`, both created. The child
  items' own artifacts are listed in their journals.
- **Status:** `open` → `open` — no transition. The epic is untouched; only its children moved.
- **Result:** The engagement lost two candidate capabilities by the stakeholder's decision — a card
  listing and an undo — and gained one durable commitment, that the card file stays readable. Both
  are in the vision; this entry is so that a reader of the epic finds them without opening a child
  item.

## 2026-08-30T13:29:13Z — review-close v0.6.0 — reviewer

- **Item:** EP-001
- **Trigger:** `next` step 6 — every work item is `done` and no status in the workspace has a runnable owner, so step 5 produced no candidate. `scripts/engagement-state EP-001` reported `at-rest`, which dispatches this skill on the epic. Precondition 4 of the procedure, not precondition 1: there is no code to review and no branch to merge, so this execution went straight to step 10.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` in full — `## Goal`, `## Why now`, the eight `## Success measures` rewritten from the stakeholder's own answers, `## Scope`, `## Out of scope` and `## Notes`.
  - `tracker/items/EP-001/questions/Q-001.md` to `Q-005.md` — all five answered by the human; `Q-004` is the `kind: elicitation` question `intake` filed, which is what DE8 asks for.
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — the three children, their statuses, their outcomes and their acceptance criteria, so that each could be named as delivered or not delivered with a reason rather than by assertion.
  - `tracker/items/WI-0003/artifacts/review.md` and `verify-report.md`, written minutes earlier by this same skill and by `verify` — the accepted gaps that had to reach the stakeholder.
  - `docs/product/vision.md` v6 and `docs/architecture/overview.md` v5 — for the stakeholder's own vocabulary, which `## Context` is required to use instead of the tracker's.
  - No diff range: an ending is not an execution and there is no branch. `main` is at `307822a`, which is where WI-0003's merge left it.
- **Decisions:**
  - **The engagement is at rest and the stakeholder is being asked, not told.** `engagement-state` is the authority, not my read of the board: *"EP-001 at-rest — every child has stopped, no question is open, no request is open; rest reached at 2026-08-30T13:26:28Z"*. Rest was reached by WI-0003's close, which is the transition timestamped in that line.
  - **`EP-001/Q-006` filed, `kind: sign-off`, `blocking: true`, addressed to `human`.** All three children are named by ID and each is marked delivered with one line of why. There is no bug item in this engagement and no undelivered child, so the naming rule is satisfied by a complete list rather than by an absence.
  - **`## Context` is written in their words, and it carries the five things they could not otherwise know.** Deletion is permanent with no back door; the tool assumes it is the only writer of the card file; no reboot has actually been tested; a card cannot be edited; and there is no way to list or search the deck. The last two are their own earlier decisions (`EP-001/Q-004`, `WI-0003/Q-001`) and are restated so that accepting is an informed act rather than a formality. Every one of these is an accepted gap that lives in a work item's `## Notes`, which is not a place a stakeholder reads.
  - **Four options, and the recommendation last and marked as ours.** Accept as complete; accept with named follow-ups; do not accept, with what is missing; withdraw. The recommendation — A, or B — sits after every option inside `## Options considered` and nowhere else, and says in as many words that C is a real option we would rather have than a yes we talked them into (F-063).
  - **DE8 needed nothing from this execution.** `EP-001/Q-004` is a `kind: elicitation` question filed by `intake` at the beginning of the engagement and answered by the human — which is where an elicitation is worth something. `check-epic-signoff` confirms it; no second one was filed, because the rule asks for at least one and one asked at the ending would have been the weaker artefact.
  - **No ending is recorded by this execution and no Definition of Done for the epic is applied yet.** DE1 to DE8 are the gate on the move *out* of `open`, and that move is the stakeholder's to select. Recording an ending now would be the F-045 failure with the question filed as decoration.
  - **The epic goes to `awaiting-answer` with `resume-to: open`, and the run stops.** That is the one gate in the pipeline that belongs to a person.
- **Questions raised:** `EP-001/Q-006` — the sign-off, blocking, addressed to the human.
- **Cross-answer check:** none consumed — this execution consumed no human answer. It *filed* a question and answered nothing; the sign-off's own reply is not in the file yet, and the cross-answer check on it is owed by whichever execution consumes it (`spec/question.md` §2). The nine human answers already consumed in this workspace were nonetheless re-checked mechanically here: `lint-answers --context epic` reports `0 errors, 0 warnings` over all nine. The one pair worth a human read at an ending — *"I don't need a numbered list for this"* (`WI-0003/Q-001`) against `WI-0003` AC6's numbered several-match prompt — was read again while writing `## Context`, and `## Context` states the scope of their sentence rather than quietly relying on it: the numbers exist only inside that one prompt, and the sign-off tells them plainly that there is no way to list or search the deck.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → 0 (`EP-001 at-rest`; `every child has stopped, no question is open, no request is open`; `rest reached at 2026-08-30T13:26:28Z`)
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → 1, **run twice and expected to fail both times**. Before the question existed: `FAIL — EP-001 has no usable sign-off:`. After filing it: `FAIL — … tracker/items/EP-001/questions/Q-006.md is still 'open' — the engagement waits on the stakeholder, which is the point of the gate`. The gate is doing exactly its job; it will pass when the reply is in the file
  - `python3 .claude/agile-skills/scripts/lint-claims --context epic` → 0 (`checked absolute claims: every document under …/docs; citations: every markdown file in the workspace`, `0 errors, 0 warnings`)
  - `python3 .claude/agile-skills/scripts/lint-answers --context epic` → 0 (`checked 9 consumed human answer(s) in the workspace`)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1 before the suspension, reporting `question.blocking.not-suspended` on EP-001 and a stale board — both of which this execution's own transition resolves — and 0 after
  - `python3 .claude/agile-skills/scripts/board-gen .` → 0
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 90 tests` / `OK`) and `python3 -m compileall -q recall tests` → 0, both on the merged trunk at `307822a`, so the engagement comes to rest with the tool green
- **Gates:**
  - `definition-of-done` → **not applied by this execution, deliberately** — the epic Definition of Done (`spec/dor-dod.md` §4, DE1 to DE8) gates the move **out** of `open` to one of the four endings, and this execution does not take an ending. It is owed in full by the execution that records the stakeholder's reply. What can be said now: DE1's children are all terminal and all named in `Q-006`; DE2's outcomes are all recorded (`delivered` on each of the three); DE5 has no open question left besides the sign-off itself; DE8 is satisfied by `EP-001/Q-004`; **DE7 is the one being satisfied by this execution** — the asking, not the answer
  - `verification-postdates-the-code` → **not applicable** — an epic has no branch and no verification report of its own. Each child carried its own D10 at its own close
  - `commits-reference-the-item` → **not applicable** — an epic has no branch. The record commit this execution produces is on the trunk, which is where `spec/workspace-layout.md` §5 puts an epic-level commit
  - `tests-pass-on-the-merge-result` → **pass, on the trunk itself** (`Ran 90 tests` / `OK` and `compileall` exit 0 at `307822a`, the merge that closed WI-0003). There is no merge of this execution's own to test
  - `workspace-valid` → **pass** (0 errors after the transition; the two errors before it were `question.blocking.not-suspended` on EP-001 and a stale board, both of which the suspension and `board-gen` clear)
  - `record-is-reconstructible` → **pass** at the engagement level, from `tracker/`, `docs/` and `git log` alone. *What was built and why*: `docs/product/vision.md` v6 and the epic's `## Goal`, with nine ADRs behind them. *Which skill decided what*: every one of the three children carries a full journal, and each ADR names its deciding skill and the answer it rests on. *What questions arose and how they were resolved*: nine questions to the human across the engagement, all answered, each with `## Consequences` naming files. *What verification found*: three verification reports, thirty-eight criteria, each with the command that settled it
  - `claims-are-sourced` → **pass**, and the **scope is the point**. Quoted from the gate: *"checked absolute claims: every document under /home/msi/agile-skills-throwaway/recall-4c/docs; citations: every markdown file in the workspace"* — `--context epic` selects the whole document set, because an ending has no diff and a window over one would have examined nothing. `0 errors, 0 warnings` over all eleven documents. This is a green over something, which is what F-066 was about
  - `cross-answer-consistency` → **pass** (`lint-answers --context epic`, `0 errors, 0 warnings` over all 9 consumed human answers)
  - `epic-sign-off` → **fails, and must**. `check-epic-signoff EP-001` exits 1 with *"tracker/items/EP-001/questions/Q-006.md is still 'open' — the engagement waits on the stakeholder, which is the point of the gate"*. This execution is not attempting an ending; it is filing the question the gate exists to require. The gate will pass when the reply is in the file, and not before
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-006.md` — created: the `kind: sign-off` question, blocking, addressed to the human, naming all three children by ID, with four options and the recommendation last
  - `tracker/items/EP-001/item.md` and `history.md` and `journal.md` — the suspension to `awaiting-answer` with `resume-to: open`
  - `tracker/board.md` — regenerated
  - no `review.md` — this execution reviewed no change; `review.md` is an artefact of closing an item, and the epic's ending is not written until the reply arrives
  - no bug item, and no document changed: the claims audit over every document under `docs/` found nothing to repair
  - the commit of this record, on the trunk, where an epic-level commit belongs
- **Status:** `open` → `awaiting-answer`
- **Result:** The engagement is at rest with all three children delivered, ninety tests green on the trunk, and every claim in `docs/` audited over the whole document set rather than over a diff that could not have contained anything. `EP-001/Q-006` asks the stakeholder whether they accept it — with each child named, with four real options, with the recommendation marked as ours and placed after them, and with the five things they had no way to know: that deleting is permanent, that the tool assumes it is the only writer, that no reboot was ever tested, that a card cannot be edited, and that nothing lists the deck. The epic is suspended at `awaiting-answer`, `resume-to: open`. Nothing further can legitimately happen in this engagement until they reply, and the ending they select — accept, accept with follow-ups, refuse, or withdraw — is all four still open.

## 2026-08-30T13:33:32Z — answer-questions v0.4.0 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer`, dispatched by the harness ahead of `next` because the stakeholder had written into `## Answer` on the open human-addressed question. `next` stops on any open human-addressed question, so consuming the answer is what makes the loop runnable again.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-006.md` — the sign-off, with the stakeholder's reply in `## Answer`
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md`, `Q-005.md` — every prior human answer, read for the cross-answer check
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` and `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — the remaining four human answers in the workspace, same purpose
  - `tracker/items/EP-001/item.md` — the goal, the eight success measures and the notes
  - `tracker/items/EP-001/history.md` — for the `resume-to` on the row that suspended the epic (`open`, written by `review-close`)
  - `docs/product/vision.md` (v6)
  - `docs/architecture/adr/` — the nine ADRs, checked for anything the acceptance would contradict; it contradicts none, being an acknowledgment rather than a decision about the build
  - `.claude/agile-skills/spec/question.md` §2 (`kind: sign-off`, `## Cross-answer check`), §3, §4
- **Decisions:**
  - Answered `Q-006` by **propagating the human's reply**, route 4-returning: the question was already escalated and they answered it. Their choice is option **A, accept as complete**, which selects the ending `delivered`. No part of it was decided here.
  - Did **not** file any work item under the scope-widening route. Option B existed and they did not take it: *"Nothing else comes to mind right now; if I want more later I'll open something new."* Filing an item for editing, a card list or a reboot test would have been us naming follow-up work they declined to name, and the record would then show a backlog they never asked for.
  - Did **not** close the epic. `answer-questions` has no transition of its own and may not move an epic to `done`; the acceptance is the input to that move. The epic returns to `open` and `review-close` records the ending after running the Definition of Done for an ending. Written into the question's `## Consequences` explicitly so a reader does not read the acceptance as the closure.
  - Carried the untested-reboot caveat into `item.md` rather than leaving it only in the sign-off. The last success measure speaks of surviving a reboot; the evidence covers the file and not the reboot, the sign-off disclosed that before asking, and the acceptance is therefore of a tool with a known gap in its evidence. Without this note the measure would later read as demonstrated.
  - Recorded the cross-answer check against **all seven** prior human answers rather than a judged subset. A sign-off accepts the whole engagement, so every statement they made is a candidate for contradicting it; with nine answers in the workspace the exhaustive list is cheap, and a judged subset here would be a judgement about which of their own words might have been overridden.
- **Cross-answer check:** `EP-001/Q-006` (the only human answer consumed by this execution), checked against `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`, `WI-0001/Q-001`, `WI-0001/Q-002`, `WI-0003/Q-001`, `WI-0003/Q-002` — **compatible** with all seven; no verdict is `conflicts` and no question was filed back to them. The two that needed more than a line: `EP-001/Q-004`, which named losing progress and a review over a couple of minutes as failures and said editing can wait — the session-length half was reconciled by them in `EP-001/Q-005`, the editing half is why no edit command exists and was named in the sign-off before they answered, and the progress half carries the reboot caveat they accepted with their eyes open; and `WI-0003/Q-001`, where they declined a card list, which the sign-off restated as a consequence and their reply neither reopens nor asks for. `EP-001/Q-001` and `EP-001/Q-002` are not in the list because the sign-off quoted both back as delivered behaviour and the acceptance affirms them; naming them would have added rows without adding a check.
- **Questions raised:** none. No escalation was due: the question was already the human's and they answered it, and no cross-answer verdict was `conflicts`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item EP-001` → exit 0, "checked 6 consumed human answer(s) on EP-001, 0 errors, 0 warnings" (5 before this execution)
  - `python3 .claude/agile-skills/scripts/lint-claims --context epic` → exit 0, 0 errors, 0 warnings, over every document under `docs/` and every citation in the workspace
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition, with exactly the two errors the transition resolves: `board.stale` and `question.awaiting.none-open` (the epic is `awaiting-answer` and its only blocking question is now answered)
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 1 at the start of this execution: "Q-006.md is still 'open' — the engagement waits on the stakeholder". Re-run after this execution by `review-close`, which owns that gate.
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `Q-006`'s `## Consequences` was opened after writing and contains the change: `tracker/items/EP-001/item.md` carries the acceptance paragraph quoting their reply and the reboot-caveat paragraph, plus `updated: 2026-08-30T13:31:49Z`; `docs/product/vision.md` is at v7 with the sign-off round recorded under `## Open with the stakeholder` and a change-log row; `Q-006.md` itself carries `status: answered`, `answered-by: human`, `answered-at`, and the cross-answer check. Three files named, three checked, none an intention.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own reply, quoted verbatim in the question and in `item.md`. Nothing was inferred and no new ADR was needed, because an acceptance decides nothing about how the tool is built — every ADR was read and none is contradicted.
  - `escalation-is-justified` → **skipped**, no escalation. Nothing was re-addressed to the human: the one question here was already theirs and is now answered, and no cross-answer conflict was found that would require putting two of their statements back to them.
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001`, exit 0; it now counts six consumed human answers on the epic, the sixth being this one, and every ID named in the new check resolves to a human answer in this workspace).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition; before it, the only two errors were `board.stale` and `question.awaiting.none-open`, both of which the transition resolves by regenerating the board and moving the epic off `awaiting-answer`).
  - `item-resumed-correctly` → **pass**. The suspending row is `2026-08-30T13:29:13Z | open | awaiting-answer | review-close | open | ...`; its `resume-to` is `open` and this execution's row targets `open`. Not inferred from which skill asked — read from the row.
  - `a-deferral-is-not-an-answer` → **pass**, vacuously and worth stating. The reply defers nothing: it selects option A by name, gives a reason, and explicitly declines the follow-up work option B offered. So neither of step 3a's two moves applies, `status` is `answered` rather than `deferred`, and the epic goes to `open` — which is where its `resume-to` sends it, and coincidentally also where an epic-level deferral would have sent it, so the distinction is recorded here rather than left to the destination to imply.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-006.md` — `status: open` → `answered`, `answered-at: 2026-08-30T13:31:49Z`, `answered-by: human`; `## Cross-answer check` written against seven prior answers; `## Consequences` naming three files and stating that this execution does not end the engagement
  - `tracker/items/EP-001/item.md` — two paragraphs appended to `## Notes`: the acceptance with their words and the ending it selects, and the reboot caveat against the success measure it qualifies; `updated` restamped
  - `docs/product/vision.md` — v6 → v7, `updated-by: answer-questions`, `updated-for: EP-001`: the sign-off round and its answer added to `## Open with the stakeholder`, with a change-log row. No sentence sourced to an earlier answer of theirs was rewritten, because nothing they said was overtaken.
  - `tracker/items/EP-001/journal.md`, `tracker/items/EP-001/history.md` — this entry and its row
- **Status:** `awaiting-answer` → `open`
- **Result:** The stakeholder accepted the engagement as complete in `EP-001/Q-006`, naming no follow-up work. The acceptance is propagated into the epic's notes and the vision, checked against all seven of their prior answers with no conflict, and the epic returns to `open` — its recorded `resume-to` — where `review-close` can now record the ending it selects, `delivered`.

## 2026-08-30T13:39:15Z — review-close v0.6.0 — reviewer

- **Item:** EP-001
- **Trigger:** the epic at status `open`, dispatched by `next` at step 6 — `scripts/engagement-state EP-001` reported `at-rest`, which is the ending path of this skill (SKILL.md step 10) and not the item review of steps 1–9.
- **Inputs read:**
  - `tracker/items/EP-001/item.md`, `history.md` (5 rows), `journal.md` (in full)
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — all six, including `Q-004` (`kind: elicitation`) and `Q-006` (`kind: sign-off`, carrying the stakeholder's reply)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — status, outcome, criteria
  - `tracker/items/WI-000{1,2,3}/artifacts/verify-report.md` — each verdict and each `## Not verified, and why`
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`; `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`
  - `docs/product/vision.md` (v7); `docs/architecture/overview.md` (v5 at the start of this execution); all nine ADRs, `ADR-0001` to `ADR-0009`
  - the code in full: `recall/store.py`, `recall/schedule.py`, `recall/cli.py`, `recall/__main__.py`, and `tests/test_add.py`, `test_review.py`, `test_delete.py`, `test_store.py`, `test_schedule.py`
  - **no diff.** An ending has no branch and no diff of its own: the three children's diffs were each reviewed hunk by hunk at their own close, and what is judged here is the engagement.
- **Decisions:**
  - **Ended the engagement as E1 — delivered.** The stakeholder accepted in `EP-001/Q-006` (*"A — accept as complete"*) and every child is `done` with `outcome: delivered`, which is the row in SKILL.md step 10's table for accept-and-every-child-delivered. Not E2: `delivered-partial` would claim something did not deliver, and nothing failed to. Recorded `outcome: delivered`.
  - **One documentation defect found and repaired, not sent back.** `docs/architecture/overview.md` §How it is checked claimed that *every* test which runs the tool sets `RECALL_CARD_FILE` into a temporary directory and clears `XDG_DATA_HOME`. Two tests in `tests/test_add.py` run the tool with `RECALL_CARD_FILE` unset — one of them *setting* `XDG_DATA_HOME` — because the default path is what they check and it cannot be checked through the override. The sentence is false; the property it was reaching for (no test touches a real deck) is true, since both redirect into the same per-test temporary directory. Repaired in place at v6 rather than filed as a bug: no code and no test is wrong, so there is nothing for an item to do, and a bug item would leave a permanent open defect for a sentence.
  - **Did not treat the untested reboot as a send-back.** Success measure 8 names a reboot of the machine and nothing rebooted one. It is recorded as an accepted gap in three places that outlive this review, and — the part that decides it — the stakeholder was told before they answered. Sending the engagement back to manufacture a reboot after they have accepted would be re-deciding their acceptance for them.
  - **Did not file the repair as a superseding change to any ADR.** No reader would have to change code to satisfy the new text, so it is a repair and not a new decision (SKILL.md 9b's line). It also touched no ADR — `overview.md` is an ordinary document with a version and a change log.
  - **Ran the tool rather than compiling DE3 from the verification reports.** Ten commands in ten processes against a scratch deck. The reports are evidence; an ending that reads only reports cannot tell a measure that is met from a measure that three items each assumed another had covered.
- **Cross-answer check:** none consumed by this execution — the stakeholder's reply to `EP-001/Q-006` was consumed by `answer-questions` at 2026-08-30T13:33:32Z, which wrote the check against all seven of their prior answers and found no conflict. This execution re-read that check rather than repeating it, and `scripts/lint-answers --context epic` re-verified all ten consumed human answers in the workspace, exit 0. Recording a second check over the same answer would be a second opinion about their words, which is not this skill's to give.
- **Questions raised:** none. `EP-001/Q-006` was filed by the previous execution of this skill and is answered; nothing in this ending needed asking, and DE8 was already satisfied by `EP-001/Q-004` at intake.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, "Ran 90 tests ... OK", on `main` at `46db753`
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → `at-rest`; "every child has stopped, no question is open, no request is open; rest reached at 2026-08-30T13:26:28Z"
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 0, "carries the stakeholder's reply, names all 3 child item(s), and was filed after the engagement reached rest at 2026-08-30T13:26:28Z; DE8 satisfied by tracker/items/EP-001/questions/Q-004.md"
  - `python3 .claude/agile-skills/scripts/lint-claims --context epic --changed-since main` → exit 0, twice: before the repair and after it
  - `python3 .claude/agile-skills/scripts/lint-answers --context epic --changed-since main` → exit 0, "checked 10 consumed human answer(s) in the workspace"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - ten runs of the tool against `/tmp/epicend/cards.txt`: `add "bonjour" "hello"`, `add "chat" "cat"`, `review` (Enter/y/Enter/n → "2 cards due." … "Done. 2 cards reviewed."), `review` ("Nothing is due."), `add "au revoir" "goodbye"`, `review` (`q` → "Stopped. 0 cards answered"), `delete "au revoir"` (`y` → "Deleted: au revoir"), `review` ("Nothing is due."), `delete "nope"` (→ exit 1, "No card has the front 'nope'"), and two `cat`s of the card file between them
  - `python3 -m unittest tests.test_add.AddTests.test_default_path_is_the_documented_one tests.test_add.AddTests.test_default_path_without_a_data_directory_is_under_home -v` → exit 0, the two tests behind the DE6 finding
- **Gates:**
  - `definition-of-done` → **pass**. All eight epic criteria (`spec/dor-dod.md` §4) recorded individually with evidence in `artifacts/review.md`'s table, and DE3 walked measure by measure below it — seven met and demonstrated here, the eighth met as to the file and untested as to the reboot, which is stated rather than glossed.
  - `verification-postdates-the-code` → **skipped**: an epic has no branch and no `verify-report.md`. `scripts/check-verify-freshness` takes an item and a branch and there is neither. The freshness of each child's verification was checked at that child's own close; nothing has changed on `main` since except tracker and docs commits.
  - `commits-reference-the-item` → **skipped**: same reason. The gate inspects commits on `{{item.branch}}` not yet on the trunk; an epic has no branch, and the epic's own record commits go on the trunk by `spec/workspace-layout.md` §5.
  - `tests-pass-on-the-merge-result` → **pass, over the trunk rather than a merge result**, and the scope is stated because there is no merge to make: `python3 -m unittest discover -s tests -t . -q` on `main` at `46db753` → exit 0, 90 tests. That is what the project actually has at the ending.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 before this transition and again after it).
  - `record-is-reconstructible` → **pass**, answered from the tracker, `docs/` and `git log` alone: **what was built and why** — three subcommands, from the epic's goal and the stakeholder's five answers, in `EP-001/item.md` and `vision.md`; **which skill decided what** — nine ADRs, each naming its author and item, plus every `**Decisions:**` bullet across four journals; **what questions arose and how they were resolved** — ten question files, each with `## Answer` and `## Consequences` naming the files it changed; **what verification found** — three `verify-report.md` files with 38 criteria and their commands, including WI-0003's nine deliberate mutations. `git log --grep EP-001` returns this engagement's whole story.
  - `claims-are-sourced` → **pass**, and the scope is quoted from the gate's own output because a scope unread is a gate unreported: "an ending has no diff of its own, so the scope is the whole document set rather than anything --changed-since could name; absolute claims: every document under /home/msi/agile-skills-throwaway/recall-4c/docs; citations: every markdown file in the workspace" — 0 errors, 0 warnings. The mechanical half proves citations resolve; the reader's half is in `review.md` §DE6, and it is the half that found the false sentence in `overview.md`, which exited 0 both before and after the repair.
  - `cross-answer-consistency` → **pass** (`lint-answers --context epic --changed-since main`, exit 0, all ten consumed human answers in the workspace; rule 3, which checks an execution's own edits against a diff, does not run at an ending and the tool says so itself).
  - `epic-sign-off` → **pass** (`check-epic-signoff EP-001`, exit 0: the reply is in the file, all three children are named, it was filed after rest, and DE8 is satisfied by `Q-004`).
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/review.md` (new) — what was examined, the eight-criterion Definition of Done table, DE3 measure by measure with the commands, the DE6 claims audit claim by claim, one finding, three accepted gaps, and the verdict
  - `docs/architecture/overview.md` — v5 → v6, `updated-for: EP-001`: the false universal claim about test isolation replaced by what the tests actually do, with `tests/test_add.py` cited for the first time; change-log row records the old sentence verbatim and why it was false
  - `tracker/items/EP-001/item.md` — `outcome: delivered`
  - `tracker/items/EP-001/journal.md`, `tracker/items/EP-001/history.md` — this entry and its row
  - no merge commit, no bug item, no new question: an ending produces none of the three
- **Status:** `open` → `done`
- **Result:** The engagement is ended as **E1, delivered**. All eight epic Definition of Done criteria pass, the stakeholder accepted at rest in `EP-001/Q-006`, and the three work items closed `delivered` between them deliver `add`, `review` and `delete` against 38 verified acceptance criteria and 90 passing tests. The claims audit over the whole document set found one false sentence in `docs/architecture/overview.md` and repaired it at v6. Three gaps are accepted and recorded, the first of them — that no machine was rebooted — having been put to the stakeholder before they accepted.
