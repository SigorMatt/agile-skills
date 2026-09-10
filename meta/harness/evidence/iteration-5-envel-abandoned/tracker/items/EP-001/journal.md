# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T13:18:13Z — intake v0.5.1 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the stakeholder's idea in `IDEA.md`; there was no tracker content to be dispatched on
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, quoted verbatim in `EP-001/Q-001`
  - `SIMULATION-NOTICE.md` — the stakeholder is asynchronous and cannot be asked in session
  - `tracker/project.yaml` — project name `envel`, trunk `main`, all three commands null
  - `tracker/items/` — empty; no existing epic, item or vision to overlap with or contradict
  - `docs/` — no `vision.md` existed, so no `## Engagement state` section was in flight
- **Decisions:**
  - **The split is three items, along the line of what a person can watch happen.** WI-0001 gives
    envelopes that exist and are still there next run; WI-0002 gives money moving in and out and a
    balance that reflects it; WI-0003 gives the month's summary. Each is demonstrable at a terminal
    on its own, and each depends only on the one before it.
  - **Income and spending were deliberately not split apart.** They are the same mechanism —
    recording an amount against a named envelope — and neither alone produces a balance worth
    looking at. Two items there would have bought three extra pipeline round trips and delivered
    nothing observable in between.
  - **Persistence was not made its own item.** The stakeholder stated it as a property of the whole
    tool ("data must survive between runs"), so it is a criterion on WI-0001 (AC3) and WI-0002
    (AC5) rather than a deliverable somebody could forget to connect to anything.
  - **Priority was read off the stakeholder's own ordering and the dependency chain**, not guessed.
    Their sentence names envelopes, then income and spending, then the summary, and each of those
    genuinely needs the one before it. WI-0001 is `critical` because nothing else can start without
    it; WI-0002 and WI-0003 are `high` and are ordered by their `depends-on`.
  - **"No services" was read at its widest** — no server, daemon, hosted account, sync or network
    access — and written into the epic's `## Out of scope` and the vision. That is an inference from
    two words, so it is put back to the stakeholder as option A of `Q-001` rather than left silent.
  - **The command name `envel` is provisional.** It comes from `project.name` in
    `tracker/project.yaml`, which the harness provisioned; the stakeholder never said it. It is used
    in WI-0001's criteria so they are concrete, and flagged in that item's `## Notes` as unconfirmed,
    for `refine` to put to them. Recording it as decided would have invented a requirement.
  - **Storage format, amount representation and exact command words were left out of every item.**
    They are design, they are `plan`'s, and naming them here would have been the `no-solution-in-the-problem`
    failure.
  - **The stakeholder could not be asked in session** (`SIMULATION-NOTICE.md`), so intake's
    conversation was filed instead: the restatement that step 2 owes them is `Q-001`, and the batch
    of step 3 is `Q-002`…`Q-004`. All five carry the same framing so they read as one conversation.
- **Questions raised:** `Q-001` (blocking — is the restatement of their idea faithful), `Q-002`
  (blocking — income straight into envelopes, or a pool that is then allocated), `Q-003` (blocking —
  what happens when a spend exceeds the envelope), `Q-004` (blocking — does a transaction take a
  date, or is it stamped when recorded), `Q-005` (non-blocking, `kind: elicitation` — what else
  matters to them that nobody asked). All five are open and addressed to the human; none has been
  answered, and none was answered by us.
- **Commands:**
  - `scripts/new-item --next-id epic` → exit 0, `EP-001`
  - `scripts/new-item --id EP-001 --type epic --status open --actor intake` → exit 0
  - `scripts/new-item --id WI-0001|WI-0002|WI-0003 --type work-item --status draft --actor intake` → exit 0 (three runs)
  - `scripts/validate-workspace .` → exit 1, 6 errors (journals and the vision's change-log row not yet written)
  - `scripts/lint-answers --item EP-001 --require-elicitation` → exit 0, 0 errors
  - `scripts/lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md` → exit 0, 1 section
  - `scripts/journal-entry WI-0001|WI-0002|WI-0003 --skill intake` → exit 0 (three runs)
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **fail** (`scripts/validate-workspace .`, run again by this transition over the state the move produces; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel --resolving 'EP-001:open->awaiting-answer+journal'` exited 1)
  - `epic-has-success-measures` → **pass** (five measures in `## Success measures`, each one an observation: a balance equal to income minus spending, the same balances after a restart, an in/out/remaining row per envelope, a non-zero exit on an unknown envelope name, and running with an interpreter and no network — none is the goal restated)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation`, exit 0; `Q-005` is the `kind: elicitation` question and is open with the stakeholder)
  - `engagement-state-is-delimited` → **pass** (`scripts/lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md`, exit 0; the one `## Engagement state` section in `docs/product/vision.md` holds the three sentences about what has been asked, what is open and what is built, and the shape check cannot see looseness in the body — that read was done by hand and moved nothing)
  - `items-are-separable` → **pass** (order is WI-0001, then WI-0002, then WI-0003, recorded as `depends-on`; each delivers something watchable at a terminal without the later ones)
  - `no-solution-in-the-problem` → **pass** (no story names a technology the stakeholder did not; Python and local persistence are theirs. The provisional command name `envel` is the one thing used that they did not say, and it is flagged as unconfirmed in WI-0001's `## Notes` rather than asserted)
- **Artifacts:**
  - `tracker/items/EP-001/item.md` — goal, why now, five success measures, scope, out of scope
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — created at `draft`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — the intake conversation, filed
  - `docs/product/vision.md` — v1, with its `## Engagement state` section
  - `tracker/project.yaml` — `project.description` filled in; `commands.*` left null, since the project has none and inventing one would make a gate report a pass for a command nobody can run
  - `tracker/board.md` — regenerated
- **Status:** `open` → `awaiting-answer`
- **Result:** The idea is now an epic with three drafted work items and a written vision. Four blocking questions and one elicitation are open with the stakeholder, so the epic is suspended at `awaiting-answer` with `resume-to: open`. Nothing has been designed or built, and no answer has been guessed.

## 2026-09-10T13:18:40Z — intake v0.5.1 — product-analyst

- **Item:** EP-001
- **Trigger:** correction to the entry immediately above, per `spec/journal-and-history.md` §0 — a wrong entry is corrected by a later entry, never rewritten. No status change; this is the same intake execution.
- **Inputs read:**
  - `tracker/items/EP-001/journal.md` (the entry of 2026-09-10T13:18:13Z)
  - the output of `scripts/transition EP-001 --to awaiting-answer`, whose final line reported the workspace clean
- **Decisions:**
  - The entry above records `workspace-valid` → **fail**, and that verdict is true of the moment the gate ran. It is **not** true of the workspace intake handed over, and left alone it would tell a reader that intake finished on a workspace that does not validate. This entry is the correction; the entry above stands unedited.
  - The single error at that moment was `doc.changelog.no-execution` on `docs/product/vision.md:69` — the change-log row names intake acting on EP-001, and it is checked against EP-001's journal. That journal entry is written **by** the transition, and the transition runs its gates **before** writing it, so the gate could not have seen the thing that satisfies it. The order is the toolkit's, not this execution's: intake must write a vision, its change-log row must name the epic, and the epic's first entry cannot exist until the first move is made. Recorded here as a toolkit finding for `retro`.
- **Questions raised:** none
- **Commands:**
  - `scripts/validate-workspace .` (run by the transition after the move) → exit 0, 0 errors, 1 warning (`project.commands.test-null`, expected: `plan` sets the commands)
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` over the handed-over state, exit 0; this supersedes the `fail` in the entry above, which was measured mid-move)
  - `epic-has-success-measures` → **pass** (unchanged; evidence in the entry above)
  - `an-open-question-was-asked` → **pass** (unchanged; `scripts/lint-answers --item EP-001 --require-elicitation`, exit 0)
  - `engagement-state-is-delimited` → **pass** (unchanged; `scripts/lint-documents`, exit 0)
  - `items-are-separable` → **pass** (unchanged)
  - `no-solution-in-the-problem` → **pass** (unchanged)
- **Artifacts:**
  - `tracker/items/EP-001/journal.md` (this entry appended; nothing edited)
- **Status:** `awaiting-answer` → `awaiting-answer`
- **Result:** The workspace intake handed over validates: 0 errors, 1 expected warning. The `fail` recorded above was the mid-move state and is corrected here rather than rewritten.

## 2026-09-10T13:30:22Z — answer-questions v0.6.2 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with five questions carrying replies from the human; dispatched by the turn's first-consume rule ahead of `next`
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` (all five, with the human's replies)
  - `tracker/items/EP-001/item.md`, `history.md` (the `resume-to` on the suspending row), `journal.md`
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md`, `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/` — empty; no recorded decision could be contradicted
  - `tracker/waiting/EP-001.md`, `tracker/project.yaml`
  - `.claude/agile-skills/spec/question.md`, `spec/journal-and-history.md`, `spec/doc-header.md` §4a
- **Decisions:**
  - All five answers were consumed by route 1 of step 3 — the human answered them directly, so there was nothing to decide and nothing to escalate. What this execution decided was where each answer lands, and the answer is recorded in each question's `## Consequences` file by file.
  - `Q-002` (A, envelopes only) landed as a rewrite of WI-0002 AC1 rather than as a note, because "there is no pool" is a testable property of the recording command and a note is not a criterion.
  - `Q-003` (B, refuse the overspend) added WI-0002 AC6 and WI-0004 AC4. The recommendation in that question was C, record-and-warn; the stakeholder chose B, and nothing in the record was written on C's strength. AC6 states the four observable parts — reports, exits non-zero, records nothing, balance unchanged — because "refuse it" alone is not decidable at a terminal.
  - `Q-004` (B, optional date defaulting to today) added WI-0002 AC7 and rewrote WI-0003 AC4 to say a transaction belongs to the month of its **own** date. The date *format* was deliberately left unpinned: they did not state one, and `refine` pins it with them alongside the command words.
  - `Q-005` widened the scope, so two items were filed at `draft` under this epic with `arose-from: EP-001/Q-005` — WI-0004 (move money between envelopes) and WI-0005 (correct or remove a recorded spend). Filing rather than widening WI-0002: swallowing new work into an existing item hides the change from the board (`spec/ids-and-statuses.md` §5, F-029).
  - `Q-005` also overturned an epic bullet that placed editing and deleting a transaction out of scope. That bullet was **replaced, and the replacement says so** — whose reading it was, and which answer replaced it — rather than being silently deleted. It was the pipeline's inference, not a sentence of the stakeholder's, so amending it is an ordinary repair and not the move `spec/question.md`'s cross-answer rule forbids.
  - Their third point in `Q-005` — a leftover balance stays in its envelope — was recorded as WI-0003 AC5 and as a "Not a sweeper" bullet in the vision, because "nothing happens at the turn of the month" is a claim the summary command can be tested against and is otherwise invisible.
  - Did **not** file a question about the apparent tension between `Q-001` ("yes, that restatement is right") and `Q-005` (asking for corrections the epic had placed out of scope). The restatement they endorsed does not claim to be exhaustive and does not mention editing; `Q-005` is the question that exists to collect what it omitted. The conflict is between their answer and our document, not between two of their statements, so there is nothing to put back to them. The reasoning is written out in `Q-001`'s and `Q-005`'s cross-answer checks rather than left implicit.
- **Cross-answer check:**
  - `Q-001` — checked against `Q-002`, `Q-003`, `Q-004`, `Q-005`; all four **compatible**. `Q-002`/`Q-003`/`Q-004` each narrow a point the restatement left open; `Q-005` adds to a paraphrase that never claimed to be exhaustive, and the line it overturns is ours.
  - `Q-002` — checked against `Q-001`, `Q-003`, `Q-005`; all **compatible**. A transfer between two named envelopes creates no pool and asks the tool to compute no split, which is the thing they said they did not want.
  - `Q-003` — checked against `Q-001`, `Q-002`, `Q-005`; all **compatible**, and `Q-003` with `Q-005` are mutually reinforcing: the refusal names moving money as the remedy and `Q-005` asks for that command.
  - `Q-004` — checked against `Q-001`, `Q-005`; both **compatible**. A monthly summary of in and out needs every movement to carry a date, which is what `Q-004` supplies.
  - `Q-005` — checked against `Q-001`, `Q-002`, `Q-003`; all **compatible**, with `Q-001`'s reasoning stated in full in that file.
  - No verdict of `conflicts` was recorded, so no conflict question was filed. `scripts/lint-answers --item EP-001` → exit 0 over five consumed answers.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --id WI-0004 ...` → exit 0
  - `scripts/new-item --id WI-0005 ...` → exit 0
  - `scripts/journal-entry WI-0004 --skill answer-questions --body-file ...` → exit 0
  - `scripts/journal-entry WI-0005 --skill answer-questions --body-file ...` → exit 0
  - `scripts/lint-documents --rule propagated-claims-carry-their-obligation --item EP-001 --uncommitted` → exit 0
  - `scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0
  - `scripts/lint-answers --item EP-001` → exit 0
  - `scripts/validate-workspace .` → exit 1 first (change-log rows out of order, two new items without journal entries, and the two errors this transition itself clears), then re-run
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in the five `## Consequences` sections was opened and the change is in it: `EP-001/item.md` (scope, out-of-scope, four new success measures), `WI-0002/item.md` (AC1 rewritten, AC6 and AC7 added, out-of-scope and notes rewritten), `WI-0003/item.md` (AC2 and AC4 rewritten, AC5 added, notes rewritten), `WI-0004/item.md` and `WI-0005/item.md` (created), `docs/product/vision.md` (v2). No `## Consequences` section names zero files.)
  - `answered-from-the-record` → **pass** (every one of the five was answered by the human directly; each `## Answer` carries their words and each `## Consequences` cites them. No ADR was needed, because this execution decided nothing the record did not already settle.)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human. The one candidate is argued against under `**Decisions:**`.)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item EP-001 --uncommitted` → exit 0, reporting 0 quantified sentences newly written into `docs/`. The new vision prose was written without quantifier words deliberately, and its absolutes about the stakeholder's own decisions carry `[src: EP-001/Q-00n]` citations that resolve.)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0. `docs/product/vision.md`'s `## Engagement state` section is byte-identical to HEAD, though this execution made two of its sentences false; that is recorded in `Q-001`'s `## Consequences` and left to `review-close`.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001` → exit 0 over five consumed human answers and zero delegations.)
  - `workspace-valid` → **fail** (`validate-workspace .` clean but for the pre-existing `project.commands.test-null` warning, which is `plan`'s to clear.; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel --resolving 'EP-001:awaiting-answer->open+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row (`2026-09-10T13:18:13Z`, `open → awaiting-answer`, actor `intake`) records `resume-to: open`, and this transition targets `open`.)
  - `a-deferral-is-not-an-answer` → **skipped** (none of the five replies defers. Each names a chosen option or supplies the requested content, and each is recorded `answered` with consequences that contain a decision.)
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — each `answered`, `answered-by: human`, `answered-at` stamped, with `## Cross-answer check` and a file-naming `## Consequences`
  - `tracker/items/EP-001/item.md` — `## Scope`, `## Out of scope` and `## Success measures` amended
  - `tracker/items/WI-0002/item.md` — AC1 rewritten, AC6 and AC7 added, `## Out of scope` and `## Notes` rewritten
  - `tracker/items/WI-0003/item.md` — AC2 and AC4 rewritten, AC5 added, `## Notes` rewritten
  - `tracker/items/WI-0004/item.md`, `tracker/items/WI-0005/item.md` — created at `draft`
  - `docs/product/vision.md` — v1 → v2, with change-log row
- **Status:** `awaiting-answer` → `open`
- **Result:** All five of the stakeholder's intake answers are consumed and propagated; the epic returns to `open`. Their answer to the elicitation widened the product by two commands, which are now WI-0004 and WI-0005 at `draft`, and it replaced an out-of-scope line the pipeline had inferred. Nothing on this epic is open.
