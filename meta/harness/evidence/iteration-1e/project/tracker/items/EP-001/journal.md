# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-26T23:25:47Z — intake v0.2.0 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the stakeholder's opening statement; the workspace had been initialised but held no items
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `SIMULATION-NOTICE.md` — establishes that the stakeholder is asynchronous and not in this session
  - `tracker/project.yaml` (name `expenses-1e`, trunk `main`, all three commands null)
  - `tracker/items/` — empty; no prior epic, item or vision existed
  - `.claude/agile-skills/spec/` — `work-item.md`, `ids-and-statuses.md`, `question.md`, `doc-header.md`, `journal-and-history.md`, `request.md`
- **Decisions:**
  - Split the idea into three work items rather than one or five. The test applied was whether
    each delivers something a person can observe on its own: WI-0001 lets you record people and
    expenses and see them survive a restart; WI-0002 answers the question the tool exists for;
    WI-0003 removes the typing. Persistence was folded into WI-0001 rather than made its own item
    because "record an expense" that does not survive the process is not observable value, and the
    two could not be ordered independently.
  - Made WI-0002 and WI-0003 depend on WI-0001. Neither has anywhere to read from or write to
    until people and expenses exist, so the dependency is real rather than a scheduling preference.
  - Did not restate the idea back to the stakeholder for correction before creating anything, as
    the procedure asks. There was nobody in session to correct it. The restatement is instead the
    epic's `## Goal`, and the three questions below carry the parts the restatement could not
    settle; if the framing is wrong, the answers are where that will surface.
  - Filed three questions rather than assuming, and stopped. The bank CSV layout (Q-001) has no
    standard and an invented one would pass verification and fail on the stakeholder's real file.
    "Who owes whom" (Q-002) has two readings — net positions and a settlement list — that produce
    different output, different code and different criteria. The delivery order (Q-003) was not
    stated, and a guessed priority is executed by the scheduler as if it were intent, invisibly.
  - Set priorities high/high/medium as a placeholder pending Q-003, and said so in Q-003 itself
    and in the epic body, so that nothing downstream mistakes the placeholder for a decision.
  - Recorded two unstated details as notes on WI-0001 rather than inventing them: how an expense
    divides between its sharers (an equal split is the plain reading of "shared by some or all",
    but was not said), and how amounts are represented and rounded. Both are refinement's to
    settle, and neither blocks intake.
  - Wrote an out-of-scope list on the epic and on every item, none of which the stakeholder asked
    for, derived from what a reader would otherwise assume: no payments, no network, no multi-user
    or sync, one group per store, no currency conversion, no GUI. The authority is intake's own
    procedure, which requires the section; the exclusions follow from "no external services" and
    from the tool being described as one person's command line.
  - Named no technology the stakeholder did not: Python, the standard library, local files and CSV
    are all their words. No storage format, module layout or command syntax appears anywhere in
    the epic or the items — those are `plan`'s.
- **Questions raised:** `Q-001` (blocking, to human — bank CSV layout), `Q-002` (blocking, to
  human — net positions or settlement list), `Q-003` (blocking, to human — delivery order). All
  three are open. No answers have been given, because the stakeholder is asynchronous and was not
  in this session; the only thing they have said is their opening statement, recorded verbatim
  below.

  The stakeholder's opening statement, verbatim, from `IDEA.md`:

  > A command-line tool to track shared expenses in my friend group: add people, add expenses
  > paid by someone and shared by some or all — and import expenses from my bank's CSV export
  > instead of me typing them in — and at any point show who owes whom. Data must survive
  > between runs. Python, no external services.

  Nothing else was said, and nothing else is recorded as having been said.
- **Commands:**
  - `scripts/workspace-init .` → exit 0, "workspace already present; nothing to do"
  - `scripts/new-item --next-id epic` → `EP-001`; `--next-id work-item` → `WI-0001`
  - `scripts/new-item --id EP-001 --type epic --status open --actor intake` → exit 0
  - `scripts/new-item --id WI-0001|WI-0002|WI-0003 --type work-item --status draft --actor intake` → exit 0 each
  - `scripts/journal-entry WI-0001|WI-0002|WI-0003 --skill intake` → exit 0 each
  - `scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `scripts/validate-workspace .` → exit 1 before this transition, with exactly the two errors this
    transition clears (`question.blocking.not-suspended` on EP-001, `journal.execution.missing` on
    EP-001)
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, run by this transition after the
    move; the two errors above were the pending move and this entry)
  - `epic-has-success-measures` → **pass** — the epic's four measures are each checkable by a
    person at a terminal: build a group and print a report from an empty store using documented
    commands only; run the report again in a fresh process and compare the figures; get an expense
    into the report from a CSV file rather than typed arguments; do all of it offline with python3
    and the standard library. None restates the goal.
  - `items-are-separable` (advisory) → **pass** — buildable order is WI-0001, then WI-0002 and
    WI-0003 in either order; WI-0002 and WI-0003 each declare `depends-on: WI-0001` and neither
    depends on the other.
  - `no-solution-in-the-problem` (advisory) → **pass** — every technology named in the epic and
    the items (Python, standard library, local files, CSV) is the stakeholder's own word. Nothing
    was removed, because nothing was added.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` (new)
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (new, all open, all to human)
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` (`project.description` filled in; `commands.*` deliberately left null
    for `plan`)
  - `tracker/board.md` (regenerated)
- **Status:** `open` → `awaiting-answer`
- **Result:** EP-001 is open with three work items at draft and a vision document. Intake stopped
  short of a complete framing on purpose: three blocking questions to the stakeholder are open on
  the epic, and the epic is suspended until they are answered. Nothing can be refined against a
  guess at the CSV layout or at what "who owes whom" should print.

## 2026-08-26T23:33:24Z — answer-questions v0.2.0 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with three blocking questions to the human, all three of which the stakeholder had replied to in the question files since the last turn. Dispatched directly at the start of the turn, ahead of `next`, because `next` step 3 stops on any open human-addressed question.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three replies
  - `tracker/items/EP-001/item.md`, `history.md` (the suspending row carries `resume-to: open`), `journal.md` (intake's reasoning and the stakeholder's verbatim opening statement)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/` — empty, so no answer here could contradict a recorded decision
  - `tracker/project.yaml`; `tracker/board.md`
  - `IDEA.md`, `SIMULATION-NOTICE.md`
  - `.claude/agile-skills/spec/question.md`, `ids-and-statuses.md`, `journal-and-history.md`, `dor-dod.md`; `.claude/agile-skills/pipeline.yaml`
- **Decisions:**
  - **Q-002 — answered from the stakeholder's reply.** They chose option B outright: *"The list of payments that settles it — that's what actually saves us the arguing after a trip."* Propagated into WI-0002's AC1–AC4, its out-of-scope list, the epic's `## Scope`, and the vision. Route: recorded intent, quoted.
  - **Q-003 — half answered by the stakeholder, half delegated and decided here.** The ordering was handed to us (*"Whatever you think is best on the order"*), so `answer-questions` decided it: WI-0001, then WI-0002, then WI-0003, on the basis that WI-0002 is the item that makes the tool answer the question `IDEA.md` says it exists for, and that WI-0003 cannot start until the CSV sample arrives in any case. The other half was theirs and was not a delegation: *"I don't want to drop either one, the import's part of what I asked for too"* — so WI-0003 went from `medium` to `high`, which is what §6 calls an item the epic's outcome requires. Checked that the priority change does not silently reorder anything: the selection key breaks a priority tie on `created`, and WI-0002 is two seconds older.
  - **Q-001 — a deferral, and the reason this entry is long.** The stakeholder replied *"I'll send you a sample later."* That is not the layout, which is what was asked. Per `spec/question.md` §2 there are two moves. Move 1 (decide under the deferral) is available here and was taken: the reply *does* settle the choice Q-001 put — it takes option A and refuses B (invent a layout) and C (drop the item) — and Q-001's own recommendation named the response to exactly this reply, "park WI-0003 and deliver the rest". So Q-001 is `answered` with the decision recorded and the deferral quoted as its basis, and the thing that was *not* settled is carried by WI-0003, which is now at `blocked` with its exit condition written down. Nothing in any artifact claims the layout is known.
  - **Why Q-001 is not marked `deferred`, which is a toolkit defect and not a preference.** Move 2 would set `status: deferred` and require *the item carrying the question* to be at `blocked`; `validate-workspace` enforces exactly that (`question.deferred.not-blocked`, which it applies to every item type). But Q-001 is filed on an **epic**, and `pipeline.yaml` gives `awaiting-answer → blocked` for `answer-questions` `applies_to: [work-item, bug]` — an epic may reach `blocked` only as the E3 impasse ending, through `review-close`. So marking an epic-level question `deferred` produces a workspace that cannot be made valid by any legal move. Move 1 was available and is honest here, so this execution was not forced; but had the deferral been undecidable, this skill would have had no legal action at all. The deferral machinery assumes the deferred question lives on the item it parks. Worth fixing upstream — either let `answer-questions` park an epic, or scope `question.deferred.not-blocked` so an epic-level deferral parks the child items that depend on it.
  - Filed no new work item. None of the three answers widened scope: Q-002 chose between two shapes of WI-0002's existing output, Q-003 ordered and re-prioritised existing items, and Q-001 added nothing. AC4 on WI-0002 is part of what option B stated it entailed, not new work.
  - Escalated nothing back to the human. Every one of the four conditions in `spec/question.md` §4 was checked: the record is not silent (they replied to all three), no ADR exists to contradict, nothing here is irreversible, and the only intent-dependent question left — the CSV layout — has already been asked and answered with "later". Re-asking it would deadlock the loop on a question they have already responded to.
  - Recorded no ADR. Nothing decided here is an architecture decision: the settlement-list choice is the stakeholder's, the ordering is scheduling, and the CSV layout is precisely what was *not* decided. `plan` will owe ADRs on WI-0002's storage and tie-break rule; they are not this skill's to pre-empt.
- **Questions raised:** none
- **Commands:**
  - `scripts/journal-entry WI-0002 --skill answer-questions --body-file …` → exit 0
  - `scripts/transition WI-0003 --to blocked --actor answer-questions --resume-to draft --journal-body-file …` → exit 1 on the first attempt (journal body missing the `**Status:**` bullet, which the tool requires even though it writes the bullet itself); exit 1 again on the second attempt with the move applied and `workspace-valid` reporting two errors introduced by this execution's own edits and one that only this transition clears
  - `scripts/validate-workspace .` → exit 1 before this transition, with the remaining error being `question.awaiting.none-open` on EP-001 — the pending move
  - `scripts/transition EP-001 --to open --actor answer-questions --journal-body-file …` → this entry
- **Gates:**
  - `answer-is-propagated` → **pass** — each of the three `## Consequences` sections names files, and each file was opened and confirmed to contain the change. Q-001 → `WI-0003/item.md` (notes rewritten, priority `high`), `WI-0003/history.md` (`draft` → `blocked`, `resume-to: draft`), `EP-001/item.md` (the three-unknowns paragraph replaced), `docs/product/vision.md` v2. Q-002 → `WI-0002/item.md` (AC1–AC3 amended, AC4 added, out-of-scope and notes rewritten), `EP-001/item.md` (`## Scope` reporting line), vision v2. Q-003 → `WI-0003/item.md` (priority, notes), `WI-0002/item.md` (order note), `EP-001/item.md`, vision v2.
  - `answered-from-the-record` → **pass** — Q-002 and Q-003's substance are the stakeholder's own words, quoted verbatim in the answers and in the items. The two things decided rather than quoted are the delivery order, which they explicitly delegated, and the park of WI-0003, whose basis is their deferral plus their refusal to drop the item. The record was not silent on any of them, so no ADR was required.
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human. The four conditions were checked against each question and none applies; see Decisions.
  - `workspace-valid` → **pass** — run by this transition. The three errors seen mid-execution were `doc.changelog.version` and `doc.changelog.order` on the vision, both from this execution writing the new change-log row oldest-first and both fixed by reordering, and `question.awaiting.none-open` on EP-001, which is this move.
  - `item-resumed-correctly` → **pass** — the suspending row of 2026-08-26T23:25:47Z records `resume-to: open`, and this transition targets `open`. Read from the history row, not inferred from which skill asked.
  - `a-deferral-is-not-an-answer` → **pass** — Q-001 was the only deferral. Move taken: move 1, decide under it. Quoted: *"I'll send you a sample later."* What it settled: option A over B and C — no layout is to be invented and WI-0003 is not to be dropped. What it did not settle: the layout itself, which is why WI-0003 is at `blocked` with its exit condition named rather than being refined against a guess. Q-002 and Q-003 were answered outright and are not deferrals.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three `open` → `answered`, with `answered-at`, `answered-by: human`, and non-empty `## Answer` and `## Consequences`
  - `tracker/items/EP-001/item.md` — the paragraph naming three unknown facts replaced with what is settled and what is not; `## Scope` now says the report is a settlement list
  - `tracker/items/WI-0002/item.md` — AC1–AC3 amended, AC4 added, out-of-scope and notes rewritten
  - `tracker/items/WI-0003/item.md` — `priority` `medium` → `high`, notes rewritten with the park and its exit condition
  - `tracker/items/WI-0003/history.md`, `journal.md` — `draft` → `blocked`
  - `tracker/items/WI-0002/journal.md` — entry recording the criteria amendment
  - `docs/product/vision.md` — v1 → v2, with a change-log row
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `open`
- **Result:** All three of the stakeholder's replies are consumed and propagated. Two questions are settled outright — the tool prints a settlement list, and the order is WI-0001, WI-0002, WI-0003 with none of them dropped. The third was a deferral: no bank CSV layout exists yet, so WI-0003 is parked at `blocked` naming the one thing that would restart it, and nothing was invented in its place. EP-001 is back at `open` and WI-0001 is the next runnable item.

## 2026-08-26T23:46:01Z — answer-questions v0.2.0 — architect

- **Item:** EP-001
- **Trigger:** status `open`; not dispatched — written alongside the `answer-questions` execution on WI-0001, because that execution changed the epic's scope and a scope change recorded only on a child is invisible from the epic
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (the stakeholder's replies)
  - `tracker/items/EP-001/item.md`
  - `docs/product/vision.md` (v2)
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 (creation authority) and §6 (priority)
- **Decisions:**
  - The epic gains a fourth work item, WI-0004 — "Delete a person or an expense recorded by mistake". Rationale: the stakeholder's answer to `WI-0001/Q-003` asked for deletion, no existing item records it, and §5 makes `answer-questions` the skill that may file work an answer implies. Widening WI-0001 to swallow it was refused because that hides the change from the board.
  - WI-0004 is `medium`, not `high`. Rationale: §6 reserves `high` for what the epic's stated outcome requires; EP-001's goal and its four success measures are coherent without deletion, and the stakeholder's own framing was *"if I have to pick"*.
  - WI-0004 carries `depends-on: WI-0002` rather than only `WI-0001`. Rationale: their constraint was *"doesn't need to hold up the who-owes-whom feature"*, and `depends-on` is the mechanical form of that sentence. It is not a technical dependency.
  - Editing a record in place is recorded in the epic's `## Out of scope` as offered and declined, not merely absent. Rationale: a reader who finds a delete command and no edit command should be able to tell a decision from an oversight.
  - The epic's delivery order is unchanged: WI-0001, WI-0002, WI-0003, with WI-0004 after WI-0002. Rationale: nothing in these three answers touches the order the stakeholder delegated in EP-001/Q-003.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --id WI-0004 --type work-item --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from WI-0001/Q-003` → exit 0, item created
- **Gates:** this entry accompanies no transition of the epic; the gates for the execution are journaled on WI-0001, where the item moved. For the epic specifically:
  - `answer-is-propagated` → **pass** (`tracker/items/EP-001/item.md` `## Scope` and `## Out of scope` both contain the change; `docs/product/vision.md` is at v3 with a change-log row)
  - `answered-from-the-record` → **pass** (every clause traces to a verbatim stakeholder reply in `WI-0001/Q-001`…`Q-003`; the priority and the dependency trace to `spec/ids-and-statuses.md` §6 and to their own words respectively)
  - `escalation-is-justified` → **skipped** (nothing was escalated from this execution)
  - `workspace-valid` → **pass** (reported on WI-0001's entry, one workspace, one run)
  - `item-resumed-correctly` → **skipped** (the epic was not suspended and did not move)
  - `a-deferral-is-not-an-answer` → **skipped** (all three replies decided their questions; none deferred)
- **Artifacts:**
  - `tracker/items/WI-0004/` (new) — item, history and journal
  - `tracker/items/EP-001/item.md` — `## Scope` gains WI-0004; `## Out of scope` gains editing in place; the Q-003 paragraph notes where WI-0004 sits in the order
  - `docs/product/vision.md` v2 → v3
- **Status:** `open` → `open` (unchanged)
- **Result:** The stakeholder's answers on WI-0001 widened the engagement by one item. EP-001 now has four children, and the vision says what the product does about splitting, dates, descriptions and mistakes.

## 2026-08-27T02:31:08Z — review-close v0.4.0 — reviewer

- **Item:** EP-001
- **Trigger:** dispatched by `next` step 6 — no item was runnable, and `scripts/engagement-state EP-001` reported the engagement at rest.
- **Inputs read:**
  - `scripts/engagement-state EP-001` → `at-rest`, `every child has stopped, no question is open, no request is open`, `not delivered: WI-0003`, rest reached at 2026-08-27T02:28:28Z
  - `tracker/items/EP-001/item.md` in full — the goal, the why-now, the four success measures, the scope with its three settled-and-outstanding notes, and the out-of-scope list
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three answered, none of them a sign-off
  - every child's `item.md` for its title, status, priority and outcome: WI-0001, WI-0002, WI-0003, WI-0004, BUG-0001, BUG-0002
  - `tracker/items/WI-0003/history.md` — the row recording why it is parked, and on whose reply
  - `README.md` — the delivered command surface, so the statement to the stakeholder is in terms of what they can type rather than in ticket numbers
  - no diff was read and no branch was merged: this dispatch is the engagement-ending path, and an epic has neither
- **Decisions:**
  - **The engagement is at rest, and the stakeholder has not been asked.** `check-epic-signoff EP-001` → exit 1, `EP-001 has no sign-off question`, listing all six children. So the ending cannot be recorded yet, whichever ending it turns out to be.
  - **A `kind: sign-off` question was filed rather than an ending chosen.** Five of six children delivered and WI-0003 did not; that shape could be argued into E2 or into E3, and choosing between them without asking is exactly the substitution this gate exists to prevent. The choice is the stakeholder's and the four options are put to them as four.
  - **The statement is written twice over, deliberately.** `## Context` says what happened feature by feature in the words of the original request — add people, add expenses, show who owes whom, import from the bank's CSV, data survives, no external services — and `## Question` names all six items by ID with a line each. The first is what a person can answer; the second is what the gate can check.
  - **WI-0003 is reported as not delivered, in the stakeholder's own terms and with the reason attributed to them.** They were asked for the export's layout and replied that they would send a sample later; nothing was invented in its place. The question says so and offers the two lines of a file that would unpark it.
  - **The two bugs are named as children, both marked delivered, and both attributed to our own testing rather than to them.** A bug nobody fixed would have appeared here too; naming every child is what makes that automatic instead of remembered.
  - **Recommendation B — accept with WI-0003 kept open as named follow-up — was given rather than withheld.** They refused to drop the import when asked, and the record should not let them accept as complete without seeing that their own earlier answer points elsewhere. A recommendation is not a decision: all four options stand.
- **Questions raised:** EP-001/Q-004 (kind: sign-off, addressed-to: human, blocking: true)
- **Commands:**
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → exit 0, `at-rest`
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 1 before filing, `no sign-off question`; exit 1 after filing, now reading `Q-004.md is still 'open' — the engagement waits on the stakeholder, which is the point of the gate`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 0, 0 errors, 0 warnings, with the new question in the tree
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 while the question was open and the epic was not yet suspended (`question.blocking.not-suspended`), which this transition resolves
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, `wrote tracker/board.md`
- **Gates:**
  - `definition-of-done` → **not applicable to this move** — the epic Definition of Done (`spec/dor-dod.md` §4) is applied when an ending is recorded, and no ending is being recorded here. DE7, the one criterion this move is about, is what the sign-off question satisfies
  - `verification-postdates-the-code` → **skipped** — an epic has no branch and no verification report; there is no code in this dispatch to be stale
  - `commits-reference-the-item` → **skipped** — an epic is not a branch-scoped unit of work, so there is no `main..branch` range to inspect
  - `tests-pass-on-the-merge-result` → **skipped** — nothing is being merged. The suite was last run green on the trunk at 123 tests when BUG-0001 merged, minutes before this execution
  - `workspace-valid` → **pass** — exit 0 at this transition, which is the move that clears the `question.blocking.not-suspended` error the open question created
  - `record-is-reconstructible` → **pass** — from `tracker/` alone: what the engagement set out to do is EP-001's goal and success measures; what each child did is its own closed record; what is not delivered and on whose reply is WI-0003's history row and EP-001/Q-001; and what the stakeholder was told at the end is Q-004, in full, without needing this journal
  - `claims-are-sourced` → **pass** — `lint-claims --all` exit 0 over the whole tree including the new question
  - `epic-sign-off` → **fails by design, and that is this execution's purpose** — exit 1, because the sign-off is open and unanswered. It will pass when the stakeholder replies, and not before; an ending recorded now would be an ending nobody was asked about
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-004.md` — created, the sign-off question
  - `tracker/board.md` — regenerated
  - no `review.md`: no item was reviewed, no branch merged, no bug filed
- **Status:** `open` → `awaiting-answer`
- **Result:** EP-001 has reached rest with five of its six children delivered and the bank CSV import parked on a sample the stakeholder said they would send. The engagement is not ended, because ending it is theirs to decide: Q-004 puts all six items to them by name, says plainly which one they did not get and why, and offers accept, accept-with-follow-up, refuse, or withdraw. The epic waits at `awaiting-answer` with `resume-to: open`, and the pipeline stops here.

## 2026-08-27T02:35:13Z — answer-questions v0.2.0 — architect

- **Item:** EP-001
- **Trigger:** the epic sat at `awaiting-answer` with `resume-to: open`, suspended by `review-close` on 2026-08-27T02:31:08Z pending the termination question; the stakeholder had since written a reply into `EP-001/Q-004`'s `## Answer`, which makes that question answerable under this skill's precondition 1 (`addressed-to: human` **with `## Answer` filled in`).
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-004.md` — the sign-off question and the stakeholder's reply
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the three intake questions, all already `answered`; Q-001 is the one the refusal turns on
  - `tracker/items/EP-001/item.md`, `history.md` — the goal in the stakeholder's terms, and the row carrying `resume-to: open`
  - `tracker/items/WI-0003/item.md`, `history.md` — the parked import: what would unblock it, and the stakeholder's earlier refusal to drop it
  - `tracker/board.md` — the state at the moment of the reply: 5 done, 1 blocked, 1 open question
  - `.claude/agile-skills/spec/question.md` §2 (`kind: sign-off`, `status: deferred`), §3, §4 — the protocol the reply has to be classified against
  - `.claude/agile-skills/spec/ids-and-statuses.md` §3.5 (the four endings and rest), §4 (legal transitions), §5 (creation authority)
  - `docs/architecture/adr/` — all nine ADRs listed; none is contradicted by the reply, and none needed writing, because the reply is a stakeholder's judgement about what was delivered rather than a technical decision
- **Decisions:**
  - **Q-004 is `answered`, not `deferred`** — route: the human replied to an escalation. The question asked whether the engagement is accepted as it stands; the reply refuses it outright and names what is missing. That settles the question that was asked. The trailing sentence *"I'll send the file and then we can finish it"* defers a **different** question — EP-001/Q-001, the CSV layout — and defers it no further than it was already deferred, so it changes nothing and creates no second deferral to record. Marking Q-004 `deferred` would have claimed the acceptance question went unanswered when it did not.
  - **The reply selects ending E3, the impasse** (`ids-and-statuses.md` §3.5): every child is terminal, WI-0003 was not delivered, and the stakeholder did not accept. Recorded in `EP-001/item.md`, not executed here — §3.5 reserves every ending to `review-close`, and the epic's `open → blocked` row names `review-close` as the only legal actor. This skill's job was to make that ending reachable, which means returning the epic to `open` with no question open.
  - **No new item was filed.** §5 would allow one had the answer widened scope. It did not: *"everything else looks right"* accepts the five delivered children, and the one thing named as missing is WI-0003, which already exists, is already `high`, and already records what would unblock it. Inventing a second item for the same want would double-count it on the board.
  - **No acceptance criterion was amended and no ADR written.** Nothing in the reply changes what any item must do.
  - **WI-0003 stays at `blocked`.** The reply is the second explicit refusal to drop it (the first was EP-001/Q-003). Closing it as `dropped` to let the epic end as delivered would contradict the stakeholder twice over.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition, as expected: `board.stale` and `question.awaiting.none-open` — the second is the mechanical consequence of answering the only open question while the item is still suspended, and both clear on the move and the board regeneration
  - `.claude/agile-skills/scripts/transition EP-001 --to open --actor answer-questions ...` → this move
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 after the move and `board-gen`
- **Gates:**
  - `answer-is-propagated` → **pass** — each file named in Q-004's `## Consequences` was opened after writing and the change is present: `EP-001/item.md` now carries a `## Where the engagement stands` section quoting the refusal and naming E3 (lines 66–88); `WI-0003/item.md` `## Notes` now carries the second refusal to drop it, citing `EP-001/Q-004`; the history row and this journal entry are this execution's own output. The Consequences section names files, not intentions.
  - `answered-from-the-record` → **pass** — the answer is the stakeholder's own reply, quoted verbatim in Q-004, in `EP-001/item.md` and in `WI-0003/item.md`. Its classification cites `question.md` §2 (deferral vs answer) and `ids-and-statuses.md` §3.5 (which ending a refusal selects); the record was not silent, so no ADR was required.
  - `escalation-is-justified` → **skipped** — nothing was escalated. No question was re-addressed to the human; the one question handled was already theirs and they answered it.
  - `a-deferral-is-not-an-answer` → **pass** — the reply was examined for a deferral and the deferral in it was found to belong to a different question. Move taken: **decide under it / mark answered** (SKILL.md step 3a.1), on the basis that the acceptance question was answered outright. Quoted in Q-004 and what it settled is stated there: the engagement is refused, the missing thing is WI-0003, the five other children are accepted. The still-outstanding CSV sample remains recorded as EP-001/Q-001's business and as WI-0003's `blocked` status, which is where a deferral's consequence is supposed to live.
  - `item-resumed-correctly` → **pass** — `history.md` row 4 records `resume-to: open` on the suspension by `review-close`; this row targets `open`. They match. Note that this is the one place where the resume-to and the ending diverge on purpose: the epic returns to `open` and `review-close` moves it to `blocked`, because ending an engagement is not this skill's move.
  - `workspace-valid` → **pass** — `validate-workspace .` exits 0 after this transition and `board-gen`.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-004.md` — `status: open` → `answered`, `answered-by: human`, `answered-at: 2026-08-27T02:33:50Z`; `## Answer` keeps the stakeholder's words verbatim and gains an `[answer-questions]` reading naming option C, ending E3 and why this is not a deferral; `## Consequences` filled in with three files
  - `tracker/items/EP-001/item.md` — new `## Where the engagement stands` section: the refusal quoted, the ending it selects, what is and is not affected by it, and what would end the impasse
  - `tracker/items/WI-0003/item.md` — `## Notes` gains the sign-off refusal as the second recorded reason the item is parked rather than dropped
  - `tracker/items/EP-001/history.md`, `tracker/items/EP-001/journal.md` — this execution
  - commit: `tracker: the answered questions and every artifact you propagated into (refs EP-001)`
- **Status:** `awaiting-answer` → `open`
- **Result:** The stakeholder refused the sign-off: the bank CSV import was part of what they asked for and it is not there, everything else is accepted, and they say they will send the file. Q-004 is answered and propagated into the epic and into WI-0003; EP-001 is back at its recorded `resume-to: open` with no question open, which puts the engagement at rest again so that `review-close` can record ending E3, the impasse, at `blocked`.

## 2026-08-27T02:40:24Z — review-close v0.4.0 — reviewer

- **Item:** EP-001
- **Trigger:** `next` step 6 — nothing was runnable (five children `done`, one `blocked`, all owner-less statuses) and `scripts/engagement-state EP-001` reported `at-rest`. Unlike the previous execution, the sign-off it filed now carries the stakeholder's reply, so this is the second of `review-close`'s two moves at rest: record the ending rather than ask.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-004.md` — the termination question and the stakeholder's answer, in full
  - `tracker/items/EP-001/item.md`, `history.md` (5 rows, chaining without a gap), `journal.md` end to end
  - every child's `item.md` frontmatter and last `history.md` row — WI-0001, WI-0002, WI-0003, WI-0004, BUG-0001, BUG-0002 — read from the items themselves rather than from the board
  - `docs/product/vision.md` v4, `docs/architecture/overview.md` v3, `README.md`, and the nine ADRs' claim lines, for DE4 and DE6
  - `expenses/cli.py`, `expenses/store.py`, `expenses/settle.py`, `expenses/money.py` — import blocks and command surface, to decide the DE6 claims from the code
  - `.claude/agile-skills/spec/dor-dod.md` §4 (DE1–DE7), `spec/ids-and-statuses.md` §3.5 (the four endings), `spec/question.md` §2–§3
  - **no diff, no branch, no merge:** an epic has none. Steps 1–9 of the procedure are about reviewing a change; precondition 4 sends an at-rest epic straight to step 10.
- **Decisions:**
  - **Ending E3, the impasse.** The stakeholder answered the sign-off with a refusal — *"No, not as it stands — the bank import was part of what I asked for and it isn't there."* Every child is terminal, WI-0003 did not deliver, and they did not accept: that is E3 exactly (`ids-and-statuses.md` §3.5). `open → blocked`, `resume-to: open`.
  - **No `outcome` on the epic.** E3 is the one ending that does not close the item, so there is nothing to record an outcome for; `delivered-partial` would assert an acceptance that was refused, and `blocked` is not `done`. The undelivered child is named instead — in Q-004, in the epic's body, in this row's reason, and in `review.md`.
  - **DE3 passes with one success measure explicitly not met.** Measure 3 — at least one expense entering the store from a bank CSV export — cannot be met, because no importer exists. DE3 requires the measures to be *addressed*; saying so is what is mandatory, and it is said in four places. I ran the other three measures rather than reading the reports that claim them.
  - **Finding 1: the example command in Q-004 is wrong, and the stakeholder read it.** `--shared-by Ana --shared-by Ben` is `argparse` last-wins, so it records the expense as shared by Ben alone and produces silently wrong arithmetic; the correct form is `--shared-by Ana,Ben`. Disposition: a dated `[review-close]` correction appended to that question's `## Consequences`, with the original text left exactly as they saw it (`question.md` §3 rule 6). **No bug item filed**, deliberately: the tool is not defective — `README.md` documents the comma form and all 123 tests use it — and filing a child at `ready` would take the engagement out of rest and invalidate the sign-off given minutes earlier, forcing the stakeholder to be asked again over a defect that changed nothing they decided. That reasoning is in `review.md` so a later reader can disagree with it.
  - **Finding 2: `vision.md` presented the unbuilt CSV import as a current capability**, in *What it is for*. Fixed under DE4 rather than recorded as a gap: it is a document overstating what is true, the same class of defect as BUG-0001, and DE4 is the criterion that owns it.
  - **The two accepted gaps** — WI-0003 undelivered, and how an importer would learn who shared an imported expense — are recorded on `WI-0003/item.md` where they survive this ending, not only in this review.
- **Questions raised:** none. Q-004, filed by the previous execution of this skill, is answered and consumed.
- **Commands:**
  - `.claude/agile-skills/scripts/engagement-state EP-001` → exit 0, `at-rest`, `not delivered: WI-0003`, rest reached `2026-08-27T02:28:28Z`
  - `.claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 0, PASS
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 0, 0 errors 0 warnings (run again after editing `vision.md` and `Q-004`)
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 123 tests … OK`
  - the product itself, from a scratch store: `person add` ×3, `expense add` ×2, `person list`, `expense list`, `settle` ×3 (one under `env -i`), two refusals with `md5sum` either side, and three commands against a non-existent store
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `definition-of-done` → **pass** — the epic Definition of Done applied criterion by criterion, DE1–DE7, each with its own result and evidence, in `artifacts/review.md`. DE4 passed only after a correction this execution made to `vision.md`; DE3 passes with success measure 3 recorded as not met. No single verdict was written in place of the table.
  - `epic-sign-off` → **pass** — `check-epic-signoff EP-001` exit 0: the reply is in the file, all 6 children are named, and the question was filed after rest was reached. This is the gate that would have refused this move had the stakeholder not been asked, and `open → blocked` is gated precisely so that an impasse cannot skip it (`ids-and-statuses.md` §4, note 1).
  - `claims-are-sourced` → **pass** — `lint-claims --all` exits 0 over the whole tree, after this execution added citations in `vision.md` v5 and in the Q-004 correction. Run over the whole tree rather than `--changed-since main`, because an epic has no branch and DE6 asks about the workspace, not about a diff.
  - `workspace-valid` → **pass** — `validate-workspace .` exits 0, both before this move and as the transition's own pre-check.
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone. *What was built and why:* the epic's `## Goal` and `docs/product/vision.md`. *Which skill decided what:* every child's `history.md` names an actor per row and every row has a journal entry. *What questions arose and how they resolved:* eight question files, all `answered`, each with `## Consequences` naming real files. *What verification found:* a `verify-report.md` per delivered child, and BUG-0001 and BUG-0002 exist because verification found them. *Why the engagement ends here:* `Q-004` and this review.
  - `verification-postdates-the-code` → **skipped** — no code and no branch. `check-verify-freshness` compares a verification against a branch head; an epic has neither. Each child ran this gate at its own close.
  - `commits-reference-the-item` → **skipped** — same reason: `main..<branch>` is undefined for an epic. The epic's record commits reference `EP-001` by the project's commit-subject convention, which is what makes `git log --grep EP-001` return this engagement's story.
  - `tests-pass-on-the-merge-result` → **skipped as a gate, run as evidence.** There is no merge. The suite was run anyway, on `main` as it stands, as evidence for DE3 and DE6: `Ran 123 tests … OK`, exit 0.
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/review.md` — created: what I examined, the DE6 claim table (8 claims decided from the code), DE1–DE7 with evidence, three findings, two accepted gaps, and the E3 verdict
  - `docs/product/vision.md` — v4 → v5, `updated-by: review-close`, `updated-for: EP-001`, change-log row added: *What it is for* corrected so it no longer presents the CSV import as a working capability, and a new *Where this ended* section recording the impasse in the stakeholder's words
  - `tracker/items/EP-001/questions/Q-004.md` — `## Consequences` gains a dated `[review-close]` correction of the wrong `--shared-by` example; the question's original text is untouched
  - `tracker/items/EP-001/item.md` — `## Where the engagement stands` gains a pointer to the review, the two findings, and why the epic carries no outcome
  - `tracker/items/EP-001/history.md`, `journal.md` — this execution
  - commit on `main`: `tracker: the review, the ended engagement and the impasse (refs EP-001)`
- **Status:** `open` → `blocked`
- **Result:** The engagement is over, at an impasse. The stakeholder was asked whether they accepted six children with five delivered, and refused: the bank CSV import was part of what they asked for and it is not there. All seven epic Definition of Done criteria are recorded with evidence — success measure 3 explicitly not met, `docs/product/vision.md` corrected to stop implying the import works, and the wrong example command in the sign-off question corrected in place. EP-001 is `blocked` with no outcome, because nothing was accepted. A person restarts it by sending the sample of their bank's export, which unparks WI-0003 and nothing else.
