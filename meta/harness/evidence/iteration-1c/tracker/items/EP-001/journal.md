# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T21:10:30Z — intake v0.1.1 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the stakeholder's stated idea; no epic existed for it
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, verbatim, treated as the stated idea
  - `SIMULATION-NOTICE.md` — establishes that the stakeholder is asynchronous and cannot be
    asked in session
  - `tracker/project.yaml` (before edit) — name `expenses-1c`, trunk `main`, all commands null
  - `tracker/items/` — empty; no prior epic, no prior items, so no overlap and no ID collision
  - `docs/product/vision.md` — did not exist
  - `.claude/agile-skills/spec/` — `work-item.md`, `ids-and-statuses.md`, `question.md`,
    `journal-and-history.md`, `doc-header.md`, `workspace-layout.md`, `dor-dod.md`
  - `.claude/agile-skills/scripts/pipeline.yaml`
- **Decisions:**
  - **Did not restate-and-confirm the idea with the stakeholder first**, as the procedure's step
    2 requires, because they are not in the session and there is no interactive channel
    (`SIMULATION-NOTICE.md`). Followed instead the procedure's "the human leaves mid-intake"
    path: shaped what the idea unambiguously supports, and filed everything else as questions.
    The restatement is nevertheless written down — it is `## Goal` and `## Why now` on this epic
    — so that the stakeholder can correct it when they answer.
  - **Split into four items rather than two or six.** The split is by what each delivers that a
    person can observe on its own: WI-0001 registers people and proves data survives a restart;
    WI-0002 records expenses; WI-0003 answers the question the stakeholder actually asked ("who
    owes whom"); WI-0004 removes the typing. Rejected merging WI-0001 into WI-0002 — "add
    people" is a capability the stakeholder named separately, and it is the cheapest place to
    establish persistence, which every later item depends on. Rejected splitting WI-0003 into
    "compute balances" and "print the report": neither half is observable without the other.
  - **Did not set `depends-on` between the items,** although WI-0002 genuinely cannot ship before
    WI-0001. The orchestrator treats `depends-on` as a runnability bar (`pipeline.yaml`,
    `orchestrator.runnable`), so recording it would prevent `refine` from even reading WI-0002
    until WI-0001 was closed and merged — serialising refinement behind full delivery for no
    gain. `priority` already produces the same order deterministically, and the build order is
    written into `## Scope` here and into each item's `## Notes`.
  - **Wrote `## Out of scope` on the epic from exclusions the stakeholder never stated** —
    settlement payments, editing and deleting, multiple currencies, multiple groups, any non-CLI
    interface, any statement format other than the named CSV export, and access control. Each is
    something a reader could reasonably have assumed was included. They are marked in the epic as
    intake's derivation, not the stakeholder's decision, so answering the questions can overturn
    any of them cheaply.
  - **Named no technology beyond the two the stakeholder named** (Python, no external services).
    In particular the storage format is absent from every item: JSON, SQLite and a flat file all
    satisfy "data must survive between runs", and choosing between them is `plan`'s job.
  - **Filed EP-001/Q-001 as `blocking: false`.** An epic at `open` can never carry a blocking
    question: `open` is terminal in `pipeline.yaml`, so `open → awaiting-answer` is not a
    transition and `scripts/transition` refuses it (verified with `--dry-run`), while
    `validate-workspace` reports `question.blocking.not-suspended` if the question is blocking.
    Non-blocking is also the truthful flag here — WI-0001 is first under every candidate
    ordering, so no work is stopped — and the orchestrator halts on any open human-addressed
    question regardless.
  - **Filed five questions in one batch rather than one at a time.** Each costs a full round trip
    to an asynchronous stakeholder, and all five were answerable now: none of them asks about
    work not yet reached, and none was invented to fill the batch.
- **Questions raised:**
  - `EP-001/Q-001` (non-blocking, to human) — delivery order of the four items, specifically
    whether the CSV import comes before or after the report
  - `WI-0002/Q-001` (blocking, to human) — are shares always equal, or can one person owe more
  - `WI-0003/Q-001` (blocking, to human) — pairwise debts, or a minimal settlement
  - `WI-0003/Q-002` (blocking, to human) — what happens to pennies that do not divide evenly
  - `WI-0004/Q-001` (blocking, to human) — what the bank's CSV export contains, and how a row
    becomes an expense with a payer and sharers

  All five are unanswered at the time of this entry. Nothing was asked in session and no
  stakeholder answer is recorded anywhere in this workspace, because there was none to record.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/workspace-init .` → exit 0, "workspace already present"
  - `python3 .claude/agile-skills/scripts/new-item --next-id epic` → `EP-001`
  - `python3 .claude/agile-skills/scripts/new-item --next-id work-item` → `WI-0001`
  - `python3 .claude/agile-skills/scripts/new-item --id …` ×5 → exit 0, EP-001 and WI-0001…0004
  - `python3 .claude/agile-skills/scripts/transition EP-001 --to awaiting-answer … --dry-run` →
    exit 1, "open → awaiting-answer by 'intake' is not a transition in pipeline.yaml"
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the fixes below
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --resume-to
    draft`, and the same for WI-0003 and WI-0004 → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `scripts/validate-workspace .` exits 0 with 0 errors.
    It first reported 9 errors: five `journal.execution.missing` (this entry and its four
    siblings did not exist yet) and four `question.blocking.not-suspended`. Three of the latter
    were fixed by suspending WI-0002, WI-0003 and WI-0004; the fourth, on this epic, by the
    `blocking: false` decision recorded above.
  - `epic-has-success-measures` (hard) → **pass** — SM1 names a sequence of commands and a
    hand-checkable result; SM2 is a restart test; SM3 names a file, a command and an observable
    outcome; SM4 is checkable by reading the install instructions and running offline. None of
    them restates the goal.
  - `items-are-separable` (advisory) → **pass** — build order and dependency for each: WI-0001
    first, depends on nothing; WI-0002 second, needs the people WI-0001 registers; WI-0003
    third, needs the expenses WI-0002 records; WI-0004 fourth, needs WI-0002's expense
    representation to write into, and is the one item whose position is genuinely free — which
    is why EP-001/Q-001 asks about it.
  - `no-solution-in-the-problem` (advisory) → **pass** — read every title and story back. Two
    removals: an earlier draft of WI-0001's title said "in a JSON store", and an earlier draft
    of WI-0004's story named `csv.DictReader`. Both are `plan`'s decisions and neither was the
    stakeholder's word. Python and "no external services" remain, in the epic and the vision
    only, because the stakeholder stated both.
- **Artifacts:**
  - `tracker/items/EP-001/` (new) — `item.md`, `journal.md`, `history.md`, `questions/Q-001.md`
  - `tracker/items/WI-0001/` (new) — item body written
  - `tracker/items/WI-0002/` (new) — item body written, `questions/Q-001.md`
  - `tracker/items/WI-0003/` (new) — item body written, `questions/Q-001.md`, `questions/Q-002.md`
  - `tracker/items/WI-0004/` (new) — item body written, `questions/Q-001.md`
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` (updated) — `project.description` filled in; `commands.*` left null,
    which is honest: the project has no source code yet, and `plan` owns filling them in
  - the generated board (regenerated by `scripts/board-gen`)
- **Status:** `—` → `open`
- **Result:** EP-001 created with four work items, one of which (WI-0001) is at `draft` and
  refinable now. The other three are suspended at `awaiting-answer` on questions only the
  stakeholder can answer. The loop stops here: five human-addressed questions are open.

## 2026-08-21T21:27:10Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** written alongside the `answer-questions` execution on WI-0002, because that
  answer changed the epic's scope rather than one item's detail.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` (answered by the stakeholder)
  - `tracker/items/EP-001/item.md`
  - `docs/product/vision.md` (v2)
- **Decisions:**
  - **Unequal shares are out of scope for the whole epic, not just for WI-0002.** The stakeholder
    answered WI-0002/Q-001 with "Equal is fine for now — most of the time we're just splitting a
    bill evenly. Don't need per-person amounts." Recorded on the epic because a reader of EP-001
    who never opens WI-0002 would otherwise assume a restaurant bill with one expensive dish is
    covered. Adding it later is a new item and a change to what an expense stores.
- **Questions raised:** none
- **Commands:** none — the epic did not transition.
- **Gates:**
  - `answer-is-propagated` → **pass**. `tracker/items/EP-001/item.md` `## Out of scope` contains
    the unequal-shares bullet; `docs/product/vision.md` v3 contains the matching product-level
    statement.
  - `answered-from-the-record` → **pass**. The stakeholder's answer in WI-0002/Q-001.
  - `escalation-is-justified` → **skipped**. Nothing escalated by this entry.
  - `workspace-valid` → **pass** (exit 0, checked after WI-0002's transition).
  - `item-resumed-correctly` → **skipped**. The epic did not move; `open` is terminal and it
    advances only through its children.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` — `## Out of scope` extended; `updated` bumped
- **Status:** `open` → `open` (no transition)
- **Result:** The epic now says out loud that an expense cannot be split unevenly.

## 2026-08-21T21:33:20Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** the epic's Q-001 was answered by the stakeholder between turns. The epic is at
  `open`, which is terminal and has no owner, so `next` would never have dispatched anything for
  it — but `next` step 2 stops the whole loop on any open human-addressed question, so an
  answered-but-open question here would have blocked every item in the project. Run before
  `next` for that reason.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` (with the stakeholder's `## Answer` filled in)
  - `tracker/items/EP-001/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` —
    the `priority` and `created` fields the selection key actually reads
  - `.claude/agile-skills/pipeline.yaml` — `orchestrator.selection_key`
  - `docs/product/vision.md` (v4)
- **Decisions:**
  - **Delivery order: WI-0001, WI-0002, WI-0003, WI-0004.** Route: recorded intent. The
    stakeholder opened with "whatever you think is best" and then chose, with a reason — "get me
    the report working first — that's the bit I actually asked for" — so this is their decision,
    not a delegation, and it is recorded as theirs.
  - **The answer was written into `priority`, not only into the epic's prose.** Rationale: the
    order the orchestrator would have executed was already correct, but only as a tie-break —
    WI-0003 and WI-0004 were both `high` with the same `created` second, and ID ordering decided
    it. Intent that lives in a tie-break is invisible and fragile. Lowering WI-0004 to `medium`
    puts the stakeholder's choice on the field `pipeline.yaml` says is read first.
  - **Nothing else was re-prioritised.** Rationale: the order of WI-0001 to WI-0003 follows from
    data dependencies that predate this question, so changing their priorities would be the
    architect restating a constraint as a preference.
  - **The epic was not transitioned.** `open` is terminal in `pipeline.yaml` and advances only
    through its children; the question was filed `blocking: false` for exactly that reason.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, board regenerated to reflect WI-0004's new priority
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 pre-existing warning (`project.commands.test-null`, owned by `plan`)
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `## Consequences` was reopened after
    writing: `tracker/items/EP-001/item.md` `## Scope` states the settled order and quotes the
    stakeholder; `tracker/items/WI-0004/item.md` reads `priority: medium` with the reason in
    `## Notes`; `docs/product/vision.md` is at v5 with the order recorded and the CSV sample left
    as the only outstanding question.
  - `answered-from-the-record` → **pass**. The stakeholder's own words in Q-001's `## Answer`.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0). Unlike the three work items, no
    interval of invalidity arose here: the question was non-blocking, so the epic was never at
    `awaiting-answer` and no transition was needed.
  - `item-resumed-correctly` → **skipped**. The epic did not move; `open` is terminal and there
    is no `resume-to` on its history.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/EP-001/item.md` — `## Scope` closing paragraph rewritten; `updated` bumped
  - `tracker/items/WI-0004/item.md` — `priority` `high` to `medium`; `## Notes` records why
  - `docs/product/vision.md` — v4 to v5
  - `tracker/board.md` — regenerated
- **Status:** `open` → `open` (no transition)
- **Result:** The delivery order is settled and is now executable rather than accidental. All
  five questions raised at intake are closed; the only fact the project is still missing is the
  bank CSV sample, which `refine` must obtain before WI-0004 can be called Ready.

## 2026-08-21T21:47:30Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** not dispatched against the epic. Written because WI-0004/Q-002's answer changed the
  shape of the epic rather than one item's detail, which `answer-questions` requires to be
  journalled here so that it is findable from the epic and not only from a child.
- **Inputs read:** `tracker/items/WI-0004/questions/Q-002.md` (the stakeholder's answer),
  `tracker/items/EP-001/item.md` (SM3, `## Scope`), `tracker/items/EP-001/questions/Q-001.md` (the
  delivery order), `docs/product/vision.md` (v8), `.claude/agile-skills/spec/dor-dod.md` (the epic
  Definition of Done).
- **Decisions:**
  - **The import is confirmed as non-negotiable scope.** Offered the chance to drop WI-0004 while
    the bank CSV sample is missing, the stakeholder refused: "the import stays part of this, it
    doesn't get dropped or pushed to a later epic... I'm not signing off on a version without it."
  - **The consequence was recorded at epic level, not left implicit.** Because the epic Definition
    of Done requires every child `done`, and WI-0004 cannot even reach Ready without the sample,
    **EP-001 is blocked on a fact only the stakeholder holds**. `## Scope` now says so. The
    alternative — leaving the note on the child — would let a reader of the epic believe it was
    three items from closing when it is three items and one missing file.
  - **The delivery order is unchanged.** "Build it last if that's easiest" is what
    `priority: medium` on WI-0004 already produces under the orchestrator's selection key.
  - **The epic was not transitioned.** `open` is terminal in `pipeline.yaml`; an epic advances only
    through its children. Nor was it set to `blocked`: three of its four children are unblocked and
    fully specified, and marking the epic blocked would stop work that can proceed.
- **Questions raised:** none.
- **Commands:** none beyond those recorded on WI-0004's journal entry for the same execution.
- **Gates:** all five are recorded on `tracker/items/WI-0004/journal.md` for this execution, which
  is the item it acted on. `answer-is-propagated` covers `tracker/items/EP-001/item.md` and
  `docs/product/vision.md` (v9) explicitly.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` — `## Scope` gains "The import is not optional and this epic
    cannot close without it"
  - `docs/product/vision.md` — v8 to v9
- **Status:** `open` → `open` (no transition)
- **Result:** EP-001 keeps all four children and all four success measures. Three of them can be
  delivered now; the fourth, SM3, waits on a bank CSV sample the stakeholder has twice said they do
  not have to hand — and the epic cannot close until it arrives.

## 2026-08-22T09:05:00Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** not dispatched. Written because answering `WI-0004/Q-006` changed the shape of this
  epic's work rather than one item's detail, and a scope decision recorded only on a child item is
  one nobody looking at the epic will find.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-006.md` — the question and the stakeholder's answer
  - `tracker/items/EP-001/item.md` — SM3 and the two paragraphs asserting this epic was blocked on
    the CSV sample
  - `docs/product/vision.md` (v10)
- **Decisions:**
  - **This epic is no longer blocked on the stakeholder, and its own notes had to stop saying it
    was.** For five askings EP-001 could not close because WI-0004 could not pass the Definition of
    Ready without a sample only the stakeholder had, and they had instructed us to wait rather than
    guess. Q-006 offered a route that needs no sample and guesses nothing — the tool holding no bank
    format and being told the file's shape at each import — and they chose it. The paragraph reading
    "the only thing that will move EP-001 is the sample itself" was true when written and is now
    false, so it was replaced rather than left.
  - **SM3 was rewritten.** It required "a CSV file in the stakeholder's bank's export format", which
    made a success measure depend on a document nobody has. It now requires a CSV imported by one
    documented command that names its own columns — checkable by anyone with a terminal, which is
    what the epic's own preamble demands of every success measure. The measure is not weakened: it
    still requires expenses to reach the report without being typed in by hand.
  - **What did not change.** The import is still not optional, still a child of this epic, and still
    last in the delivery order — the stakeholder's Q-002 answer and their EP-001/Q-001 ordering are
    both untouched. WI-0004 remains the only thing between this epic and closure.
  - **The sample, when it arrives, becomes a new item under this epic** — a named shortcut for the
    four options — and not a change to WI-0004. Recorded so that its arrival is understood as an
    addition rather than as reopening work already done.
- **Questions raised:** none
- **Commands:** none — this execution's commands are recorded on WI-0004, the item it acted on
- **Gates:** all five are recorded in full on `tracker/items/WI-0004/journal.md` for this same
  execution; this entry adds no gate of its own and transitions nothing. `answer-is-propagated`
  covers `tracker/items/EP-001/item.md`, which is named in `Q-006`'s `## Consequences` and was
  reopened after writing to confirm both changes are present.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` — SM3 rewritten; the "blocked on a fact only the stakeholder
    holds" and "the only thing that will move EP-001 is the sample itself" paragraphs replaced with
    the record of how that dependency ended
  - `docs/product/vision.md` — v10 → v11, which carries the same fact for the product record
- **Status:** unchanged — EP-001 stays `open`; this execution transitioned WI-0004 only
- **Result:** EP-001 stops waiting on the stakeholder. Its last child, WI-0004, is refinable again
  and returns to `draft`; nothing else stands between this epic and closure.

## 2026-08-22T12:20:00Z — review-close v0.1.1 — reviewer

- **Item:** EP-001
- **Trigger:** not dispatched on this item. Written because closing WI-0004 made every child of
  EP-001 `done`, which is the moment step 10 reserves for applying the epic's own Definition of
  Done — the only point in the pipeline where every sibling's state is already in hand.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the goal, SM1 to SM4, `## Scope` and its two paragraphs about
    the import
  - all four children's `item.md`, and WI-0004's `verify-report.md` and `review.md`
  - `docs/product/vision.md` v11 in full, `docs/architecture/overview.md` v5, `README.md`
  - `tracker/items/EP-001/questions/Q-001.md` (answered), and the six on WI-0004 (all answered)
- **Decisions:**
  - **The epic is left `open`, on DE4.** Eleven of the twelve points hold; `docs/product/vision.md`
    does not yet reflect what was actually built. Two passages in `## How it is used` describe the
    command surface as it stood before WI-0004: it lists the tool's commands as "`./expenses
    add-person Ana`, `./expenses list-people`, and so on", written when there were two and now
    six; and its output rule — confirmation on stdout with 0, refusal on stderr with 1 — has no
    place for the third case WI-0004 introduced, a partial import that writes `Skipped line …` to
    stderr and still exits 0. Neither sentence is false. Neither is what DE4 asks for.
  - **`review-close` may not fix it, so it asked.** `spec/doc-header.md` §5 assigns
    `product/vision.md` to `intake`, `refine` and `answer-questions`; this skill is not among them,
    and editing it anyway would be the reviewer quietly taking another persona's pen. `EP-001/Q-002`
    is filed, addressed to `architect`, **non-blocking**, naming both passages, quoting what each
    currently says, and offering three options including the option of deciding DE4 is already met.
    `next` step 3 dispatches `answer-questions` on any open architect question, so the loop
    continues without a human and the epic can close on the following pass.
  - **Closing today and noting the gap was available, and declined.** It is a legitimate reading —
    nothing in `docs/product/` is untrue, and the spec says explicitly that closing an epic over an
    unmet point is allowed provided it is said. What made it the wrong call here is the immediate
    history: WI-0004 was rejected one transition earlier for documentation that did not match what
    shipped, and it cost a full round trip. Certifying DE4 over the same class of gap minutes later
    would make the criterion mean nothing and would teach the record that documentation findings
    apply to work items and not to epics.
  - **DE3 was assessed and all four success measures are met** — recorded here rather than deferred
    to the closing pass, because this is the execution that had every child's state in hand:
    **SM1** — three people, three expenses paid by different people, one reproducible report: met,
    and checked by hand during WI-0003's verification and again here (`Ana is owed 15.00`,
    `Ben is square`, `Cass owes 15.00`, `Cass pays Ana 15.00` from two expenses of 30.00 and 15.00).
    **SM2** — the tool stopped and restarted between recording and reporting, with the report
    unchanged: met; every command is a separate process against one JSON file, which is what
    WI-0001 AC7 and WI-0002 AC3 check.
    **SM3** — a CSV imported by one documented command, its expenses appearing in the report without
    being typed: met, and the measure itself was rewritten when Q-006 was answered because its
    original wording ("in the stakeholder's bank's export format") depended on a document nobody
    had. WI-0004 AC1 and AC3 are the demonstration, and `README.md` is the documentation.
    **SM4** — stock CPython, no network, no third-party package named in the install instructions:
    met; `python3 -m compileall` and `unittest` are the only tools, `README.md`'s Requirements
    section says "A Python 3 interpreter, and nothing else", and the six modules import only `csv`,
    `datetime`, `hashlib`, `json`, `os`, `re`, `tempfile`, `argparse` and `sys`.
  - **DE6 was begun, not finished.** Every claim in `docs/` about behaviour WI-0004 delivered was
    re-read against the code during that item's two reviews, and ADR-0002, ADR-0005, ADR-0006 and
    ADR-0009 each check out. What has *not* been re-checked during this epic is the prose about
    WI-0001 to WI-0003's behaviour, which is exactly the class DE6 exists for — and the epic's own
    evidence that this matters is that three false sentences about the report and the command
    surface sat in `README.md` from WI-0002 and WI-0003 until a reviewer read the file this turn.
    The closing pass owes that read.
  - **DE1, DE2 and DE5 hold.** All four children `done`; all four with `outcome: delivered`, none
    dropped; every question across every child `answered`, and the one question now open is on the
    epic itself and non-blocking.
- **Questions raised:** `EP-001/Q-002` — non-blocking, to `architect`, for DE4.
- **Commands:** the commands for this assessment are recorded on `tracker/items/WI-0004/journal.md`
  for the same execution; this entry adds `python3 .claude/agile-skills/scripts/board-gen .` →
  rewrote the board, and `validate-workspace` → exit 0.
- **Gates:** the six gates for this execution are recorded in full on WI-0004's journal, which is
  the item this execution acted on and transitioned. The epic-level checklist is under Decisions:
  DE1 pass, DE2 pass, **DE3 pass on all four success measures**, **DE4 fail — `EP-001/Q-002` filed**,
  DE5 pass, DE6 partial and owed by the closing pass.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-002.md` (new)
  - `tracker/items/EP-001/item.md` unchanged; the epic stays `open` and no transition was made
  - the merge of `wi/WI-0004` into `main`, which is what made this assessment possible
- **Status:** unchanged — EP-001 stays `open`
- **Result:** Every child of EP-001 is delivered and merged: people, expenses, the who-owes-whom
  report, and the bank CSV import the stakeholder refused to sign off a version without. All four
  success measures are met. The epic is not closed, for one reason: `docs/product/vision.md` still
  describes a two-command tool, and putting that right belongs to `answer-questions`, which
  `EP-001/Q-002` now asks. The closing pass also owes DE6 a read of the prose about WI-0001 to
  WI-0003, which nobody has re-checked since those items closed.

## 2026-08-22T12:35:00Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** `EP-001/Q-002` open and addressed to `architect`, dispatched by `next` step 3. The
  epic is at `open`, not `awaiting-answer`, because the question is **non-blocking**: `review-close`
  filed it rather than suspending anything, so there is no suspending history row and **no
  `resume-to` to return to**. That is correct rather than a defect in the asker — a non-blocking
  question does not suspend an item (`spec/question.md` §3 rule 2) — and it is why this execution
  makes no transition.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-002.md` — the only open question in the workspace
  - `tracker/items/EP-001/questions/Q-001.md` — answered; re-read to confirm nothing in it bears on
    this
  - `tracker/items/EP-001/item.md` — the goal, SM1 to SM4 as they now stand, and `## Scope`
  - `tracker/items/EP-001/journal.md` — `review-close`'s entry of 2026-08-22T12:20:00Z, which
    records why the epic was left open and what the closing pass still owes
  - `tracker/items/WI-0004/item.md` — AC1, AC4, AC6, AC10 and the `## Notes` sections, which are
    where the delivered behaviour is actually recorded
  - `tracker/items/WI-0004/questions/Q-006.md` — the stakeholder's words, quoted into v12
  - `docs/product/vision.md` v11 — **read end to end**, not only the two passages named
  - `docs/architecture/overview.md` v5, `README.md`'s `### Importing from your bank` section
  - `docs/architecture/adr/` — ADR-0005 in particular, whose consequences note anticipated the
    skipped-row case by name; ADR-0001, ADR-0002, ADR-0004, ADR-0006, ADR-0009 and ADR-0011 checked
    for anything contradicted by the new wording. Nothing is
  - `spec/doc-header.md` §5 (who may write `vision.md`) and `spec/question.md` §3
- **Decisions:**
  - **Q-002 — answered by route 1, from existing documents.** Option A. Nothing here needed an
    architect's judgement: every fact written into v12 was read from `WI-0004/item.md`,
    `overview.md` v5, ADR-0005, or the stakeholder's own words in Q-006. The document had simply
    fallen behind decisions that were all properly recorded elsewhere. That is the cheapest kind of
    answer and the kind that cannot drift, because the sources stay authoritative.
  - **Option B declined.** A section describing the finished product end to end would duplicate
    `README.md`, which already does that job, and would be a second copy of the same claims to keep
    true — which is the failure mode this whole exercise is about.
  - **Option C declined, agreeing with `review-close`.** Declaring DE4 already met was a legitimate
    reading and the question said so. It costs one document and one version to close the gap
    properly, and certifying a criterion over a gap that cheap would have taught the record that
    documentation findings bind work items but not epics.
  - **The document was read end to end, and three more stale claims were found.** The question was
    scoped to `## How it is used`; reading only that would have been enough to answer it and would
    have left the rest wrong. What turned up: `## How we will know it works` still described SM3 as
    "a real bank CSV export populates it without hand typing", though SM3 itself was rewritten in
    `EP-001/item.md` when Q-006 was answered; the section headed "Open at the time of writing" still
    said "All but one are now settled", true until Q-006 and false since; and its counts were wrong
    in both directions — the files say five questions from `intake` and eleven from `refine`,
    sixteen in all, against the document's "five and four more". **WI-0004/Q-005 had no entry at
    all**, which matters because it is the asking whose failure is the reason Q-006 asked something
    else. All four are fixed in v12.
  - **Why that read was in scope rather than scope creep.** DE6 asks for exactly this — claims about
    delivered behaviour re-checked *during* the epic rather than at the moment they were written —
    and this document is the case it describes: eleven versions, each amending the paragraph its own
    decision touched, none re-reading the paragraphs no decision touched. `review-close` recorded
    that the closing pass owes DE6 a read; this is part of that debt paid on the document the
    question already had open.
  - **Nothing was escalated, and nothing needed to be.** None of the four conditions in
    `spec/question.md` §4 applies: no intent is missing, nothing is irreversible, no ADR is
    contradicted, and the record is the opposite of silent.
  - **No ADR written.** No decision was taken. Writing one would record as an architect's choice
    what is simply the delivered behaviour of a merged item.
  - **No item, plan or acceptance criterion was touched.** This answer moved one document. The code,
    the tests and the criteria are exactly as `review-close` merged them.
- **Questions raised:** none. `EP-001/Q-002` was the last open question in the workspace; all
  eighteen across five items are now `answered`.
- **Commands:**
  - `grep -h "^addressed-to:" tracker/items/*/questions/Q-*.md | sort | uniq -c` → 16 human, 2
    architect; and by origin, the sixteen human-addressed split five `intake` / eleven `refine` —
    which is where v12's corrected counts come from, rather than from the sentence they replaced
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before the edits; exit 1
    mid-execution on `board.stale` alone, the expected transient after a question changes state;
    exit 0 after `board-gen`
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `answer-is-propagated` → **pass**. The one file named in `## Consequences` was reopened after
    writing and every change confirmed present in `docs/product/vision.md`: frontmatter `version: 12`
    with `updated-for: EP-001`; the change-log row for v12; `## How it is used` naming all six
    subcommands and carrying the `import-csv` paragraph with the stakeholder's quote; the
    output-and-exit-code paragraph carrying both the already-imported refusal and the skipped-row
    sentence citing ADR-0005; `## How we will know it works` matching SM3's current wording and
    stating that all four measures are met; the section now headed "Questions put to the stakeholder,
    and where their answers landed", opening with "Nothing is open", carrying the corrected counts,
    and containing exactly one `WI-0004/Q-005` entry where before there were none.
  - `answered-from-the-record` → **pass**, and in its strongest form: every statement added to v12
    is traceable to `WI-0004/item.md` (AC1, AC4, AC6, AC10), `docs/architecture/overview.md` v5,
    ADR-0005's consequences, `EP-001/item.md`'s SM3, the question files' own frontmatter, or the
    stakeholder's verbatim answer to Q-006. The record was not silent anywhere, so no ADR was
    required and none was written.
  - `escalation-is-justified` → **pass, vacuously**. No question was re-addressed to the human.
    Checked against `spec/question.md` §4 explicitly rather than assumed: no missing intent, nothing
    irreversible, no ADR contradicted, no silence.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after. The single exit-1 in
    between was `board.stale` and nothing else, cleared by `board-gen`.
  - `item-resumed-correctly` → **not applicable, and recorded rather than skipped silently**. The
    question was non-blocking, so EP-001 was never suspended: its history has no row into
    `awaiting-answer` for this question and therefore no `resume-to`. There is no status to return
    the item to and this skill makes no transition of its own. The epic stays `open`, which is where
    `review-close` left it and where it belongs until the closing pass applies the epic Definition
    of Done.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-002.md` — `status: answered`, `answered-by: answer-questions`,
    `answered-at: 2026-08-22T12:35:00Z`; `## Answer` recording option A, the two passages fixed, the
    three further stale claims found, and why B and C were declined; `## Consequences` naming the
    one file changed and stating explicitly that no item, plan or criterion moved
  - `docs/product/vision.md` — v11 → **v12**, with a change-log row
  - the generated board, regenerated by its script
- **Status:** unchanged — EP-001 stays `open`; this skill transitions nothing and this question
  suspended nothing
- **Result:** DE4 is now satisfiable: `docs/product/vision.md` describes the tool as delivered —
  six commands, the per-import column mapping the stakeholder chose over waiting for a sample, and
  the skipped-row case that exits 0. Three stale claims the question did not ask about were found by
  reading the whole document and fixed with it, including a section still headed "Open at the time
  of writing" when nothing is open. No question remains open anywhere in the workspace, and EP-001
  is ready for `review-close` to apply the epic Definition of Done.

## 2026-08-22T12:55:00Z — review-close v0.1.1 — reviewer

- **Item:** EP-001
- **Trigger:** invoked directly on the epic, **not dispatched by `next`** — and that is itself a
  finding. `next` was run first and correctly reported *nothing runnable*: all four children are
  `done`, no question is open, and the only remaining item is EP-001 at status `open`, which
  `pipeline.yaml` gives `owner: null`. Yet `open → done` by `review-close` is a legal transition
  with every precondition satisfied. Epic closure is reachable **only** from inside the last child's
  `review-close` execution (step 10), so an epic that is legitimately not closable at that instant —
  exactly the case step 10 provides for with "or leave it open and record why" — can never be picked
  up afterwards. This execution finishes the step the WI-0004 close deferred, using the owning skill
  and the legal transition rather than improvising, and records the reachability gap.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` in full — the goal, SM1 to SM4, `## Scope` and `## Out of scope`
  - `tracker/items/EP-001/journal.md` — nine entries, including this skill's own entry of
    2026-08-22T12:20:00Z recording why the epic was left open and what the closing pass owed, and
    `answer-questions`' entry of 12:35 recording that it paid part of that debt
  - `tracker/items/EP-001/questions/Q-001.md` and `Q-002.md` — both `answered`
  - all four children's `item.md`, their `outcome` fields and their `review.md` verdicts
  - all eighteen question files across five items
  - `docs/product/vision.md` **v12, end to end**; `docs/architecture/overview.md` v5; all eleven ADRs
  - **the running tool**, for DE6
- **Decisions:**
  - **EP-001 closed, `outcome: delivered`.** All six epic Definition of Done points pass, each
    recorded with its own evidence in `artifacts/review.md`.
  - **DE4 passes now and did not before**, which is the whole reason this took two executions. At
    v11 `vision.md`'s `## How it is used` described a two-command tool and its output rule had no
    place for a partial import. v12 fixes both, and `answer-questions` found three further stale
    claims while it was there — a summary of SM3 that still named "a real bank CSV export", a
    section headed "Open at the time of writing" when nothing was open, and question counts wrong in
    both directions. Deferring the epic cost one loop iteration and bought four corrections.
  - **DE6 was done by running the claims, not re-reading them.** Eight behavioural claims from
    ADR-0001, ADR-0003, ADR-0004, ADR-0005, ADR-0010, ADR-0011, `vision.md` and `overview.md` were
    each checked against the tool: the penny-splitting rule, name identity and list order, the
    default data-file path, the greedy settlement and its n−1 bound, the three empty-answer
    sentences, one line per person and never per pair, the absence of any bank format, and the
    stored import record's exact shape. All eight are true. This is the read the earlier execution
    recorded as owed, and it was owed because this epic proved the risk: three false sentences about
    the report and the command surface survived in `README.md` from WI-0002 and WI-0003 until a
    reviewer read the file during WI-0004.
  - **DE3: all four success measures met, and SM3's rewrite is declared rather than buried.** SM3
    originally required "a CSV file in the stakeholder's bank's export format", which nobody but the
    stakeholder could check; it was rewritten when Q-006 was answered. A success measure that
    changed during the epic is exactly the kind of thing a closing review should surface, so
    `review.md` says what it used to require and why it no longer does.
  - **Two toolkit findings recorded in `review.md`**, neither about the product: the orchestrator
    cannot reach a closable epic, and `review-close` cannot file a bug item though its own
    escalation section instructs it to. The second bit twice during WI-0004 and left the
    `store.save` traceback with no owner.
  - **No child was reopened and no bug filed.** Nothing found in this review is a defect in
    delivered behaviour.
- **Questions raised:** none. All eighteen questions in the workspace are `answered`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `grep -H "^outcome:" tracker/items/WI-*/item.md` → `delivered` four times (DE2)
  - `grep -h "^addressed-to:"` and `grep -L "status: answered"` over all question files → eighteen
    files, none unanswered; sixteen to the stakeholder, two to the architect (DE5)
  - DE6, from an empty store each time: 10.00 shared three ways → `Ana is owed 6.66` (ADR-0001);
    `add-person "  Zoe "` → `Added Zoe`, `add-person zoe` → `Zoe is already registered`,
    `list-people` → `ana`, `Ben`, `Zoe` (ADR-0003); `list-people` / `list-expenses` / `report` on an
    empty store → three plain sentences, each exit 0 (ADR-0005); 40.00 by Ana and 20.00 by Ben
    shared four ways → `Cass pays Ana 15.00`, `Dan pays Ana 10.00`, `Dan pays Ben 5.00`, three
    payments for four non-zero balances (ADR-0010, and SM1);
    `grep -n DEFAULT_DATA_FILE expenses_tool/cli.py` → `os.path.join("~", ".expenses.json")`
    (ADR-0004)
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests … OK`, on `main` after
    the merge
  - `python3 .claude/agile-skills/scripts/transition EP-001 --to done --actor review-close
    --reason "..."` → applied
- **Gates:**
  - `definition-of-done` → **pass**. Applied as §4's epic checklist, criterion by criterion, with
    the table in `artifacts/review.md` as evidence: DE1 pass, DE2 pass, DE3 pass on all four
    measures, **DE4 pass — the point that held the epic open**, DE5 pass, DE6 pass on eight claims
    re-run against the code.
  - `verification-postdates-the-code` → **not applicable to an epic, and recorded rather than
    skipped silently**. An epic has no branch, no code and no verification report of its own; the
    criterion belongs to its children, and all four passed it at their own closes — WI-0004's twice,
    once at `909b394` and once at `89cce7e` after the README send-back moved the head.
  - `commits-reference-the-item` → **not applicable for the same reason**. EP-001 has no branch.
    `check-commit-refs` passed on each child's branch at its own close; WI-0004's reported
    `all 10 commit(s) on main..wi/WI-0004 name WI-0004`.
  - `tests-pass-on-the-merge-result` → **pass, on the trunk as it now stands**. There is no epic
    merge to trial, so the meaningful check is the state the project actually got:
    `python3 -m unittest discover -s tests -t . -q` on `main` after all four merges → exit 0, 145
    tests. Recorded this way rather than as "not applicable", because "all four children merged
    cleanly one at a time" is not the same claim as "the trunk is green now".
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after the transition.
  - `record-is-reconstructible` → **pass**, and this is the criterion the whole epic is a test of.
    From `tracker/`, `docs/` and `git log` alone a reader can answer all four questions for the
    epic: what was built and why (`item.md`'s goal, `vision.md` v12's twelve versions, four child
    items); which skill decided what (five `history.md` files, five `journal.md` files, eleven ADRs
    each naming its deciding skill and item); what questions arose and how they were resolved
    (eighteen files, all `answered`, sixteen of them the stakeholder's own words verbatim — including
    the five identical deferrals that are the most informative thing in this record); and what
    verification found (four verification reports, WI-0004's twice-written and each carrying its own
    verified commit).
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/review.md` (new) — what was examined, the six-row epic
    Definition of Done table, the four success measures with their evidence, the eight DE6 claims
    re-run, two toolkit findings, five accepted gaps and the verdict
  - `tracker/items/EP-001/item.md` — `status: done`, `outcome: delivered`
  - no merge commit and no branch; an epic has neither
- **Status:** `open` → `done` (`outcome: delivered`)
- **Result:** EP-001 is delivered and closed. The tool adds people, records expenses paid by one
  person and shared by several, imports expenses from a CSV export whose shape the user states at
  each import, and reports who owes whom as the payments that settle it — in Python, on one machine,
  with the data in one JSON file that survives between runs. Four items, four `delivered`, eighteen
  questions answered, four success measures met, 145 tests green on the trunk. The epic was held
  open for five turns by one fact only the stakeholder had, nothing was ever guessed, and what
  finally moved it was asking a different question rather than the same one a sixth time.
