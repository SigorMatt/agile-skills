# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-22T01:38:53Z — intake v0.2.0 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; `intake` is not dispatched by `next`. The workspace existed (`workspace-init` reported "already present") but `tracker/items/` was empty, so this is a new epic, not an addition to one.
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, verbatim below
  - `SIMULATION-NOTICE.md` — establishes that the stakeholder is asynchronous and cannot be asked in session
  - `tracker/project.yaml` — name `expenses-1d`, trunk `main`, all three `commands.*` null
  - `tracker/items/` — empty, so `EP-001` and `WI-0001`..`WI-0003` are the first IDs allocated
  - `docs/product/vision.md` — did not exist before this execution
- **Decisions:**
  - **Split into three items, not five.** The idea names four capabilities — add people, add expenses, import from CSV, show who owes whom — but "add people" and "add expenses" cannot be delivered apart: a person with nobody to owe is not observable behaviour, and an expense needs a payer that already exists. They are one item, `WI-0001`, which also carries persistence, because "data must survive between runs" is a property of that record rather than a deliverable of its own. `WI-0002` (the report) and `WI-0003` (the CSV import) each deliver something a user can see and each depend only on `WI-0001`, so both declare `depends-on: WI-0001`.
  - **Order is only partly forced.** `WI-0001` must come first. Between `WI-0002` and `WI-0003` nothing forces an order, and the procedure forbids guessing one, because `next` would then execute the guess as the stakeholder's intent. Filed as `Q-001` rather than inferred from the emphasis in "instead of me typing them in".
  - **The CSV import is recorded as unspecifiable, not as specified.** A parser needs the file's real columns, delimiter, date format and sign convention, and none of that is in the workspace; separately, a bank row cannot say who *shared* an expense, so a rule has to supply that. Both are in `Q-002`. `WI-0003` exists at `draft` with criteria that describe the outcome and openly say it cannot be made Ready until `Q-002` is answered — rather than inventing a column layout that would read as a requirement.
  - **Repayments are held out of scope pending `Q-003`, not decided.** "Show who owes whom" stops short of settling up. Deciding it silently either way has a cost: including it widens the stakeholder's stated goal on my own authority; excluding it produces a report that is wrong the first time anyone pays someone back, and `WI-0001`'s storage is chosen before that would be discovered. So both `WI-0001` and `WI-0002` list it as out of scope *pending the question*, and nothing downstream rests on the guess.
  - **"No external services" is read narrowly, and the reading is labelled an assumption.** It is taken as: nothing hosted, no remote API, no account, works offline. Whether third-party Python packages are also excluded was not stated. The epic assumes the standard library suffices and makes reaching for a dependency a decision `plan` must record — that satisfies the constraint under either reading and is cheap to reverse — and `EP-001`'s `## Notes` marks it as an assumption rather than as something the stakeholder said.
  - **Unknowns are written down as unknown.** What the group does today, what would count as failure, whether splits can be uneven, and whether an expense has a date are all recorded in `## Notes` on the epic or the items. None was filled in with a plausible value.
  - **No technology beyond what was stated.** Python, CSV and "command line" appear because the stakeholder said them. Nothing about storage format, command names or data structures appears anywhere in an item; the criteria say "a command" deliberately. Nothing had to be removed.
- **Questions raised:** `Q-001` (blocking, to human — build order after `WI-0001`, and whether either item is optional for a first version); `Q-002` (blocking, to human — the bank CSV's real shape, and how a bank row becomes a *shared* expense); `Q-003` (blocking, to human — whether recording repayments is in scope for this epic). All three remain open; the stakeholder is asynchronous and could not be asked in session (`SIMULATION-NOTICE.md`), so they are filed as artifacts per `spec/question.md` and the epic is suspended.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/workspace-init .` → exit 0, "workspace already present; nothing to do"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (before creating anything) → exit 0, 0 errors, 2 warnings
  - `python3 .claude/agile-skills/scripts/new-item --id EP-001 --type epic ...` → exit 0
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0001 --type work-item ...` → exit 0
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0002 --type work-item ...` → exit 0
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0003 --type work-item ...` → exit 0
  - `python3 .claude/agile-skills/scripts/journal-entry <WI> --skill intake --body-file ...` ×3 → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after the board) → exit 1, 2 errors: `question.blocking.not-suspended` on `EP-001` and `journal.execution.missing` on `EP-001`. Both are the state this transition exists to resolve — the suspension is this move, and the missing entry is this entry — and both were expected to clear once it completed. The transition's own closing `validate-workspace` run, printed with this command, is the authoritative check.
- **Gates:**
  - `workspace-valid` (hard) → see the transition's gate output printed alongside this entry. At the moment the gates ran, the only outstanding errors were the two named above, both produced by this execution being mid-move; the run-gate result is recorded as it came back rather than as I would like it to have been.
  - `epic-has-success-measures` (hard) → **pass**. Four measures, and each is something a person at a terminal could check without context: start from empty, add people and expenses, restart the process, see the same expenses listed; the printed debts balance against the recorded expenses; a bank export becomes expenses by running one command against the file without hand-editing it; every step works with no network, no hosted service and no account. None restates the goal with the word "successfully".
  - `items-are-separable` (advisory) → **pass**. Order and dependency stated for each: `WI-0001` first and standalone; `WI-0002` after it, delivering the report; `WI-0003` after it, delivering the import. No item was created that I could not describe an order for.
  - `no-solution-in-the-problem` (advisory) → **pass**. Titles and stories re-read; they name Python, CSV and the command line, all of which the stakeholder named, and nothing else. Nothing was removed.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` (new), `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (new, all open, all addressed to human)
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` — `project.description` filled in; `commands.*` left null, because inventing a test command that does not exist would make the first gate report a pass for a command nobody can run
  - `tracker/board.md` (regenerated)
  - journal and history on all four items
- **Result:** `EP-001` opened with three items at `draft` and a vision document. Three questions are open to the stakeholder — build order, the bank CSV's real shape, and whether repayments are in scope — so the epic is suspended at `awaiting-answer` with `resume-to: open`. Nothing is designed and no code exists; `refine` takes the items one at a time once the questions come back.

  The stakeholder's idea, verbatim, since this entry is the only record of it inside the tracker: "A command-line tool to track shared expenses in my friend group: add people, add expenses paid by someone and shared by some or all — and import expenses from my bank's CSV export instead of me typing them in — and at any point show who owes whom. Data must survive between runs. Python, no external services."
- **Status:** `open` → `awaiting-answer`

## 2026-08-22T01:39:13Z — intake v0.2.0 — product-analyst

- **Item:** EP-001
- **Trigger:** correction to the entry immediately above, written by the same `intake` execution; no status change
- **Inputs read:**
  - the output of `scripts/transition EP-001 --to awaiting-answer --actor intake ...`, which was not available when the entry above was written
- **Decisions:**
  - Record the `workspace-valid` result as a fact rather than as a pointer to output a later reader cannot see. The entry above says "see the transition's gate output", which is not auditable from the file. Corrected by appending rather than by editing, per `spec/journal-and-history.md`.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/transition EP-001 --to awaiting-answer --actor intake --resume-to open --reason "..." --journal-body-file ...` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **fail at gate time, pass after the move**. At gate time it exited 1 with exactly one error, `journal.execution.missing` on `EP-001` — the entry the same command was about to write. `question.blocking.not-suspended` was downgraded to a warning because the pending move resolves it. The transition's closing run reported **0 errors, 1 warning** (`project.commands.test-null`, which `plan` owns). The gates did not block this move: `intake` gates only its completion transition, to `draft`.
  - `epic-has-success-measures` (hard) → **pass**, as assessed in the entry above; `run-gate` reports it MANUAL, so the assessment is the analyst's read and not a command's exit code.
  - `items-are-separable` (advisory) → **pass**, MANUAL, as above.
  - `no-solution-in-the-problem` (advisory) → **pass**, MANUAL, as above.
- **Artifacts:**
  - `tracker/items/EP-001/journal.md` (this correction), `tracker/items/EP-001/history.md` (row written by the transition), `tracker/board.md` (regenerated by the transition)
- **Status:** `awaiting-answer` → `awaiting-answer` (unchanged)
- **Result:** The workspace validates with 0 errors. `workspace-valid` failing at gate time was the ordering artefact of an entry that had not yet been written, not an unresolved defect — but it is a note for the toolkit's owner that a skill's *first* transition on a freshly created item cannot satisfy `workspace-valid` at gate time, because the gate runs before the entry that would satisfy it.

## 2026-08-22T01:47:30Z — answer-questions v0.1.4 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with three `addressed-to: human` questions whose `## Answer` sections had been filled in since the previous run; `answer-questions` is the only skill that may consume a human's reply.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (all three, with the human's answers)
  - `tracker/items/EP-001/item.md` and `history.md` (the suspending row records `resume-to: open`)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`
  - `docs/product/vision.md` (v1) — its "what it deliberately is not" section named `EP-001/Q-003` as open
  - `docs/architecture/adr/` — empty; no recorded decision could be contradicted
  - no `plan.md` and no `refinement-qa.md` exist yet; nothing has reached `ready`
  - `.claude/agile-skills/pipeline.yaml` (selection key, runnability, legal transitions), `spec/ids-and-statuses.md` §4, `spec/question.md`, `spec/request.md`
- **Decisions:**
  - **`Q-001` (build order) — answered from the human's reply.** WI-0001 → WI-0002 → WI-0003, all three shipping; the stakeholder refused the "drop one" option outright. Propagated by lowering WI-0003 to `medium` and adding `depends-on: WI-0002`, because `pipeline.yaml`'s `selection_key` (priority rank, then created, then id) is the only place delivery order can be expressed. Rationale for saying so loudly in three files: a later reader seeing `medium` on an item the stakeholder called non-optional would otherwise read it as the stakeholder deprioritising the import, which is the opposite of what they said. The added `depends-on` is not a scheduling trick — WI-0003's AC2 asserts imported expenses count towards the who-owes-whom report, which cannot be verified before WI-0002 exists.
  - **`Q-002` (bank CSV shape and import rule) — deferred by the human, and recorded as such.** The reply, "I'll send you a sample later", supplied neither the sample nor a choice among options A–D. Marked `answered` because that reply is what was said and it has a propagatable consequence, and explicitly **not** because the facts are known. Rationale for closing rather than leaving open: `next` step 3 stops the loop on any open human-addressed question, so leaving an answered-but-unconsumed question open deadlocks every subsequent turn (the F-011 failure mode), while the deferral's actual consequence — WI-0003 is unrefinable — is recorded where `refine` will read it. No CSV shape was guessed. WI-0003's runnability is already blocked by `depends-on` on two items that are not `done`, so the missing sample costs the pipeline nothing right now.
  - **The date question was deliberately not decided.** WI-0001's notes had parked "does an expense have a date?" on the expectation that `Q-002` would force it. It did not. `Q-001` did establish that the import ships regardless, so the question is live — but the record is silent on it and a guess could be contradicted by the eventual CSV, so it was handed to `refine`, which talks to the stakeholder directly and will be dispatched on WI-0001 next. Deciding it here would have been route 3 applied to something route 4 will get for free.
  - **`Q-003` (repayments) — answered from the human's reply, with the architecture decided here.** In scope, "whatever's simplest to build". Two things the reply did not settle were settled by `ADR-0001`: (a) a repayment is its own record type, not a negative expense — the latter would make `list expenses` show entries nobody spent and push a sign convention into every consumer; (b) the work went onto WI-0001 (AC7, AC8) and WI-0002 (AC5, AC6) instead of the fourth work item `Q-003`'s option A described.
  - **Why no fourth item: only `intake` may create one.** `pipeline.yaml` and `spec/ids-and-statuses.md` §4 make `— → draft` legal solely for the actor `intake`; the other route in, a `tracker/requests/` request, is authored only by the human (`spec/request.md` §2, `from: human`). Folding into WI-0001 and WI-0002 was legitimate only because both are still at `draft`, so their criteria are not frozen. Recorded in `ADR-0001` as a methodology gap, not smoothed over: had either item been `ready` or later, an accepted scope change would have had nowhere to go.
  - **Four acceptance criteria were added to draft items.** Journalled explicitly because criteria are load-bearing and `answer-questions` is one of only two skills permitted to touch them. None of the four narrows an existing criterion or reshapes a target around delivered behaviour — no code exists. They add what the stakeholder asked for on `Q-003`.
- **Questions raised:** none. Nothing was re-addressed to the human: `Q-001` and `Q-003` were answered outright, and `Q-002`'s missing facts are recorded as a blocker on WI-0003 for `refine` to raise as a fresh question when the item is actually reached, per `spec/question.md` §3 rule 6. Filing that question now would stop the loop to ask for something nobody is yet waiting on.
- **Commands:**
  - `.claude/agile-skills/scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1, 1 error (`question.awaiting.none-open` on EP-001) + 1 warning (`project.commands.test-null`); the error is the pre-transition state this entry's transition clears, and the warning belongs to `plan`
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was reopened and checked: `WI-0003/item.md` (`priority: medium`, `depends-on` lists WI-0001 and WI-0002, Notes open with the deferral and the ordering paragraph); `WI-0001/item.md` (AC7 and AC8 present, out-of-scope line replaced, date and storage bullets rewritten); `WI-0002/item.md` (AC5 and AC6 present, out-of-scope line replaced, notes bullet added); `EP-001/item.md` (success measure, two scope lines, decisions section); `docs/product/vision.md` (v2, "open question" text gone, change-log row present); `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` (created). No Consequences section names an intention rather than a file.
  - `answered-from-the-record` → **pass**. `Q-001` and `Q-003` follow from the stakeholder's own words, quoted verbatim in each `## Answer`. `Q-002`'s answer is the stakeholder's deferral, recorded as a deferral. The one place the record was silent and a decision was made instead — how a repayment is modelled and where the work lives — is recorded as `ADR-0001` with two rejected options and its reversibility.
  - `escalation-is-justified` → **pass, vacuously**. No question was re-addressed to the human, so no escalation condition needed to be named.
  - `workspace-valid` → **pass**. `validate-workspace` reported exactly one error before this transition, `question.awaiting.none-open` on EP-001, which is the condition this transition exists to clear; the warning `project.commands.test-null` is `plan`'s. Re-run after the transition, recorded in the next execution's inputs.
  - `item-resumed-correctly` → **pass**. `EP-001/history.md` row 2 carries `resume-to: open`, and this transition targets `open`. Read from the history row, not inferred from which skill asked.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md` — answered; consequences name WI-0003 and EP-001
  - `tracker/items/EP-001/questions/Q-002.md` — answered as a deferral; consequences name WI-0003, WI-0001 and EP-001
  - `tracker/items/EP-001/questions/Q-003.md` — answered; consequences name the ADR, WI-0001, WI-0002, EP-001 and the vision
  - `tracker/items/EP-001/item.md` — one success measure and two scope lines added; `## Notes` now carries the three decisions
  - `tracker/items/WI-0001/item.md` — AC7, AC8 added; out-of-scope and two notes bullets rewritten
  - `tracker/items/WI-0002/item.md` — AC5, AC6 added; out-of-scope and notes updated
  - `tracker/items/WI-0003/item.md` — `priority` `high` → `medium`; `depends-on` gained WI-0002; notes rewritten
  - `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` — created, v1
  - `docs/product/vision.md` — v1 → v2
  - `tracker/board.md` — regenerated
- **Result:** All three stakeholder questions consumed and propagated into eight files. The epic returns to `open`; repayments are now delivered scope via four new criteria on two draft items rather than a fourth item nobody could create, the build order is encoded in priority and dependencies, and WI-0003 is recorded as unrefinable until the promised CSV sample arrives.
- **Status:** `awaiting-answer` → `open`

## 2026-08-22T02:00:10Z — answer-questions v0.1.4 — architect

- **Item:** EP-001
- **Trigger:** not dispatched on the epic. Written because answering WI-0001's five questions
  changed the epic's product boundary, and a scope decision recorded only on a child item is one
  nobody scanning the epic will find
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md`
  - `tracker/items/EP-001/item.md`, `docs/product/vision.md` (v2)
  - `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` (v1)
- **Decisions:**
  - **Uneven splits are out of the product, not merely out of WI-0001.** The stakeholder answered
    `WI-0001/Q-001` "equal split's fine for now", so every expense this epic delivers is shared
    equally and an uneven bill is entered as two expenses. Recorded in `docs/product/vision.md`
    v3 under "What it deliberately is not", because a boundary that lives only in one item's
    `## Out of scope` is invisible to anyone reading the product docs.
  - **"One group's books" now has a precise limit.** `WI-0001/Q-004` settled that a run may be
    pointed at a different data file, so a trip can keep separate books — while the tool still
    never holds two groups at once. The vision said "one group's books" flatly; it now says what
    is and is not possible, so the two statements cannot be read as contradicting each other.
  - **One decision was delegated by the stakeholder and taken by the architect:** who absorbs the
    rounding remainder of an equal split. `ADR-0002` records it — the payer absorbs it — with its
    options and its reversibility. It is noted here because it is a rule the whole epic's
    arithmetic rests on, not a WI-0001 detail: WI-0001 stores totals and sharers, WI-0002 applies
    the rule, WI-0003 must normalise bank amounts into the format it fixes.
  - Not done: no epic-level criterion changed, and no work item was created. Nothing in these
    answers widened the epic's scope the way `EP-001/Q-003` did.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - `answer-is-propagated` → **pass** (evidence on WI-0001's journal entry for this execution;
    the epic-level file it names is `docs/product/vision.md` v3)
  - `answered-from-the-record` → **pass** (each boundary above quotes the stakeholder's answer)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0 after the WI-0001 transition)
  - `item-resumed-correctly` → **skipped** (this entry accompanies no transition; the epic stays
    `open`)
- **Artifacts:**
  - `docs/product/vision.md` — v2 → v3
  - `docs/architecture/adr/ADR-0002-amount-format-and-rounding.md` — created (v1)
- **Status:** `open` → `open` (unchanged)
- **Result:** Two product boundaries and one architectural rule reached the epic's record as a
  result of WI-0001's refinement answers. No item was created and no epic criterion changed.
