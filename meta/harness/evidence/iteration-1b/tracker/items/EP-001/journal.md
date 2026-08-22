# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T18:52:10Z — intake v0.1.1 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on a raw idea stated by the person who owns this project; no
  epic existed and `tracker/items/` was empty
- **Inputs read:**
  - the stated idea, verbatim: "A command-line tool to track shared expenses in my friend group:
    add people, add expenses paid by someone and shared by some or all, and at any point show who
    owes whom. Data must survive between runs. Python, no external services."
  - `tracker/project.yaml` (name `expenses-1b`, trunk `main`, all three commands null)
  - `tracker/items/` — empty; no EP- or WI- had been allocated, so EP-001 and WI-0001..WI-0003
  - `docs/product/vision.md` — did not exist
  - `.claude/agile-skills/spec/`: `work-item.md`, `ids-and-statuses.md`, `question.md`,
    `doc-header.md`, `dor-dod.md`, `journal-and-history.md`, `workspace-layout.md`
- **Decisions:**
  - **Restated the idea in writing rather than asking it back interactively.** The person who
    stated the idea is not present in this session and answers asynchronously in files, so the
    restatement was written into `docs/product/vision.md` for them to correct, and the questions
    that would have been a conversation were filed as question artifacts instead. This is the
    path `intake`'s own escalation section gives for a human who has left the session.
  - **Split into three work items along the three verbs in the idea** — add people, add expenses,
    show who owes whom. Each delivers something observable on its own: after WI-0001 you can see
    the group and it survives a restart; after WI-0002 you can see the expenses; after WI-0003 you
    get the answer the tool exists for. The order is forced by data dependency, recorded as
    `depends-on`, not by preference.
  - **Did not split persistence into its own item.** Storage delivers nothing a person can observe
    by itself, and an item nobody can demonstrate is a plan step, not a work item. It is folded
    into WI-0001, where "survives a restart" is an acceptance criterion.
  - **Did not split the read side out from the write side.** Recording something you cannot read
    back is not observable, so listing people belongs to WI-0001 and listing expenses to WI-0002.
  - **Excluded editing and deleting a recorded expense**, on my own authority, and said so in the
    epic's `## Out of scope`. The idea describes recording and reporting only; correction is a
    second problem with its own design question (does a correction rewrite history or append a
    reversal?) and admitting it here would roughly double the epic. If that exclusion is wrong it
    is cheap to file as a new item later.
  - **Excluded multi-currency, multi-machine use, accounts, attachments and any GUI** by
    derivation from "my friend group" and "Python, no external services". None was mentioned; all
    are things a reader could reasonably assume, which is what the out-of-scope list is for.
  - **Kept the success measures free of implementation.** An earlier draft included a measure that
    the persisted file be readable in a text editor; it was removed before this entry was written,
    because it decides the storage format — `plan`'s decision, and not an outcome the person
    asking for this stated.
  - **Recorded five things as questions rather than filling them in.** Each changes an artifact,
    and none can be derived from anything on disk. They are listed below.
  - **Filed `EP-001/Q-001` as non-blocking, against its substance, because the pipeline cannot
    express a suspended epic.** `pipeline.yaml` marks the epic status `open` as terminal, so
    `open -> awaiting-answer` is rejected by `scripts/transition` even though `awaiting-answer` is
    listed as applying to epics; `validate-workspace` meanwhile reports
    `question.blocking.not-suspended` for an open blocking question on an item that is not
    suspended. The two rules cannot both be satisfied for a question that belongs to the epic. I
    marked it non-blocking and said so in the question's own `## Context`, rather than silently
    dropping the question or leaving the workspace invalid. Nothing is lost in practice: all three
    work items are suspended in their own right, and the orchestrator stops on any open question
    addressed to the human regardless of the flag. This is a defect in the toolkit, not a
    judgement about the question.
- **Questions raised:**
  - `EP-001/Q-001` (blocking, to human) — is recording a settlement ("Alice paid Bob 20") in
    scope, or is the tool expenses-only? Decides whether this epic has a fourth work item.
  - `WI-0001/Q-001` (blocking, to human) — one-shot subcommands or an interactive session?
    Decides the shape of every acceptance criterion in the epic, so its answer must reach WI-0002
    and WI-0003 as well as WI-0001. Filed on WI-0001 rather than on the epic because that is the
    first item it bites, and because an epic cannot be suspended (see the decision below).
  - `WI-0002/Q-001` (blocking, to human) — equal splits only, or explicit unequal shares?
  - `WI-0002/Q-002` (blocking, to human) — how are leftover pennies assigned when a split does not
    divide evenly?
  - `WI-0003/Q-001` (blocking, to human) — netted pairwise debts, or the minimised set of
    transfers?
  - **Answers received: none.** Nothing in this entry is recorded as a human answer, because no
    human answered anything in this session. Every statement here that is not quoted from the
    stated idea is my derivation, and is labelled as such.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/workspace-init .` -> exit 0 ("workspace already present")
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 2 warnings (null test
    command; empty project description) before any item existed
  - `python3 .claude/agile-skills/scripts/new-item --next-id epic` -> `EP-001`
  - `python3 .claude/agile-skills/scripts/new-item --id EP-001 ...` -> exit 0, and likewise for
    WI-0001, WI-0002 and WI-0003
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 1, 8 errors on the first
    pass: four missing journal entries (this one and its three item counterparts), three items
    with an open blocking question not yet suspended, and `project.unparsable` because the
    description had been written as a multi-line YAML scalar. All three causes were fixed; the
    final run is recorded under **Gates**.
  - `python3 .claude/agile-skills/scripts/transition EP-001 --to awaiting-answer ...` -> exit 1,
    "open -> awaiting-answer by 'intake' is not a transition in pipeline.yaml"
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to awaiting-answer --resume-to draft ...`
    -> exit 1: the move itself was applied, but the script re-validates afterwards and WI-0002 and
    WI-0003 were still unsuspended at that moment. Same for WI-0002 (exit 1, WI-0003 still
    outstanding). WI-0003 -> exit 0, at which point the workspace was clean.
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0 ("board already current")
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning (null test
    command), final state
- **Gates:**
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0 after the fixes above.
  - `epic-has-success-measures` (hard) -> **pass** — three measures, each checkable by a person
    with a terminal: (1) add three people and two expenses, restart the tool, and the balances
    still account for both with nothing re-entered; (2) the who-owes-whom output names a debtor, a
    creditor and an amount for every non-zero net position, and those amounts settle every
    recorded expense; (3) it imports and runs with no third-party package installed and opens no
    socket. None of the three restates the goal.
  - `items-are-separable` (advisory) -> **pass** — WI-0001 depends on nothing and delivers a
    persisted group list; WI-0002 depends on WI-0001, because an expense names people who must
    already exist, and delivers persisted expenses; WI-0003 depends on WI-0002, because it is a
    function of the expense list, and delivers the answer the tool exists for. Both dependencies
    are recorded in `depends-on`, so the orchestrator enforces the order rather than trusting it.
  - `no-solution-in-the-problem` (advisory) -> **pass, with one removal** — the epic and all three
    stories were read back looking for technology the person did not name. "Python" and "no
    external services" are their own words and stay. One success measure asserting that the
    storage file be human-readable text was removed, because it chose a storage format. Nothing
    else names a data structure, a library or a file format: WI-0001 says "listing the group", not
    "prints a JSON array".
- **Artifacts:**
  - `tracker/items/EP-001/` (new: item.md, journal.md, history.md, questions/Q-001.md)
  - `tracker/items/WI-0001/` (new, with questions/Q-001.md)
  - `tracker/items/WI-0002/` (new, with questions/Q-001.md and questions/Q-002.md)
  - `tracker/items/WI-0003/` (new, with questions/Q-001.md)
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` (updated: `project.description` filled in; `commands.*` deliberately
    left null, because this project has no test, lint or build command yet and inventing one would
    make a gate report a pass for something nobody can run — `plan` sets them)
  - `tracker/board.md` (regenerated by its script)
- **Status:** `open` -> `open` (unchanged; the epic cannot be suspended — see Decisions)
- **Result:** The epic and three work items exist and the workspace validates. Five blocking
  questions are open and addressed to the human; all three work items are suspended behind them at
  `awaiting-answer`, and the epic stays at `open` because this pipeline has no way to suspend an
  epic. Nothing was designed and no code was written. When the
  answers arrive, `answer-questions` propagates them into these artifacts and `refine` takes the
  items on from `draft`.

## 2026-08-21T18:53:00Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** `EP-001/Q-001` was open, addressed to `human`, and the human had written a `##
  Answer` into it since the previous turn. The epic itself is at `open`, not `awaiting-answer`,
  because this pipeline cannot suspend an epic (see `intake`'s entry above); the question was
  still this skill's to close, and nothing else in the pipeline can close it.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` — including the human's answer
  - `tracker/items/EP-001/item.md`, `history.md`, `journal.md` (intake's entry)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` and their histories,
    to see which of them the scope change touches
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/` — does not exist; no recorded decision could be contradicted
  - `tracker/project.yaml`
  - `.claude/agile-skills/spec/question.md`, `doc-header.md`, `work-item.md`,
    `journal-and-history.md`; `.claude/agile-skills/pipeline.yaml`
  - no `refinement-qa.md` exists yet — nothing has been refined
- **Decisions:**
  - **Read the answer as option B, not option C, and said so in the question file.** The human
    wrote "being able to mark that someone's paid up matters"; a payment is what is marked, and
    the reason they gave — the numbers racking up forever — is not cured by a reset action, which
    only defers the same problem to the next partial payment. Recording the reading explicitly
    matters because B and C differ in what gets built, and a later reader must be able to see that
    the alternative was rejected on the words rather than never noticed.
  - **Created WI-0004 rather than folding settlement into WI-0003.** The answer adds a fourth kind
    of fact to store, which is a separable deliverable: WI-0003 remains demonstrable over expenses
    alone, and WI-0004 adds a record type the same calculation nets off. Folding it into WI-0003
    would have made that item undemonstrable until both halves worked, which is the failure
    `items-are-separable` exists to prevent.
  - **Made WI-0004 depend on WI-0003, not the reverse.** The dependency is real: WI-0004's AC4 and
    AC5 are statements about WI-0003's output, so WI-0003's criteria must be settled first.
  - **Created the item under `intake`'s name, after the pipeline refused to let this skill do it.**
    `answer-questions`' contract has no output for "a new work item" and its escalation section
    sanctions only a bug item, but an answer that grows the epic's scope has nowhere else to land:
    leaving it in the epic's `## Scope` with no item would mean the capability the human asked for
    was recorded and never built, which is exactly the "answered but not propagated" failure the
    `answer-is-propagated` gate exists to catch. The first attempt created WI-0004 with
    `--actor answer-questions`; `validate-workspace` then failed with
    `history.transition.illegal: None -> draft by 'answer-questions'`, because `pipeline.yaml`
    admits exactly one creation transition into `draft` and reserves it to `intake`. The item was
    deleted and recreated with `--actor intake`, and `intake`'s own procedure and gates were run
    for it and journalled on WI-0004. That attribution is accurate rather than convenient: turning
    a human's stated want into a tracked item under an epic *is* `intake`'s contract, and it is the
    contract that was actually in force — which is what `actor` exists to record. What
    `answer-questions` did here is the scope decision, recorded in this entry. The alternative,
    forcing an illegal row through with `--force`, would have left the workspace claiming a
    transition the pipeline does not have.
  - **Left the epic's `## Out of scope` alone.** Corrections to a recorded expense stay excluded;
    a settlement is a new fact, not an edit to an old one, so nothing there is contradicted. The
    same exclusion is restated on WI-0004 for payments.
  - **Deferred `docs/product/prd.md`.** Three of the five questions in this batch were still
    unanswered when this execution ran, and a product document written between them would have
    described a product half of whose behaviour was undecided. It is created by the last execution
    in the batch instead.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning (null test
    command), before this execution changed anything
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0 ("board already current")
  - `python3 .claude/agile-skills/scripts/new-item --next-id work-item` -> `WI-0004`
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0004 --type work-item ... --status draft
    --actor answer-questions` -> exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 1, 2 errors:
    `history.transition.illegal` on the row just written (`None -> draft by 'answer-questions'`),
    and `board.stale`
  - `rm -rf tracker/items/WI-0004` and
    `python3 .claude/agile-skills/scripts/new-item --id WI-0004 ... --actor intake --reason "..."`
    -> exit 0; the item body was restored from the copy taken before the delete
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning, after
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
- **Gates:**
  - `answer-is-propagated` (hard) -> **pass** — every file named in `Q-001`'s `## Consequences` was
    reopened after writing: `WI-0004/item.md` exists with the story, six ACs and the dependency;
    `EP-001/item.md` carries the new scope bullet and the fourth success measure;
    `WI-0003/item.md`'s settlement bullet now names WI-0004 instead of an open question;
    `docs/product/vision.md` is at v2 with the settlement paragraph and one fewer open question.
  - `answered-from-the-record` (hard) -> **pass** — the answer is the human's own words, quoted in
    the question file. The only derivation on top of it is B-not-C, which is argued from the
    wording in the question file itself, not asserted.
  - `escalation-is-justified` (hard) -> **not applicable, nothing escalated** — no question was
    re-addressed to the human by this execution.
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0, one pre-existing warning
    about the null test command, which `plan` owns.
  - `item-resumed-correctly` (hard) -> **skipped, no suspension to resume** — EP-001 was never
    suspended: its history has one row, `— -> open`, with `resume-to` empty, because the pipeline
    has no legal transition out of `open` for an epic. There is no target to compare against.
    WI-0001 to WI-0003 are resumed by their own executions in this batch.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md` — answered; `answered-by: human`,
    `answered-at: 2026-08-21T18:51:11Z`; `## Answer` records the B-not-C reading, `## Consequences`
    names four paths
  - `tracker/items/WI-0004/` — new item at `draft`, created under `intake`'s name and journalled
    there with `intake`'s gates
  - `tracker/items/EP-001/item.md` — one scope bullet and one success measure added
  - `tracker/items/WI-0003/item.md` — settlement out-of-scope bullet rewritten
  - `docs/product/vision.md` — v2
- **Status:** `open` -> `open` (unchanged; an epic has no suspended state to return from)
- **Result:** Settling up is in the epic. WI-0004 exists at `draft` behind WI-0003, the epic's
  scope and success measures say so, and the vision document no longer lists this as open. Three
  human answers on the work items remain to be propagated by the executions that follow.

### Toolkit note

Two things in the toolkit made this execution harder than it should have been, and both are worth
fixing rather than working around again.

1. **A human answer that widens an epic's scope has no sanctioned way to become a work item.**
   `answer-questions`' contract has no "new work item" output, and `pipeline.yaml` admits exactly
   one creation transition into `draft`, reserved to `intake`. So the skill whose entire job is
   propagating answers cannot propagate the most consequential kind of answer without borrowing
   another skill's name — which is what happened here. Either `answer-questions` should be a
   permitted actor on `null -> draft`, or the pipeline should have a way to hand a scope change
   back to `intake` as a dispatchable action.
2. **`new-item` writes a history row without checking it against `pipeline.yaml`.** It accepted
   `--actor answer-questions` happily and produced an item that only `validate-workspace` would
   later reject. The check the `transition` script performs on every other row is simply absent at
   creation, so the failure surfaces one step late and the only repair is to delete the item
   directory and start again — which means hand-restoring the body that was already written.

## 2026-08-21T19:11:21Z — answer-questions v0.1.1 — architect

- **Item:** EP-001
- **Trigger:** not dispatched on this epic. Written because two of the three answers consumed on
  WI-0001 govern every item under EP-001, and a decision that shapes four items should be findable
  from the epic rather than only from the child that happened to raise it.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-002.md`, `Q-003.md`, `Q-004.md` — the human's answers
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md`
  - `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` (v1), `ADR-0002-share-model.md` (v1)
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v1)
- **Decisions:**
  - **The epic now has a fixed command vocabulary (`ADR-0006`).** Seven subcommands and no others:
    `add-person`/`people`, `add-expense`/`expenses`, `who-owes-whom`, `add-payment`/`payments`. A
    fact is recorded with `add-<noun>`; facts of a kind are listed with the bare plural noun. This
    changes where the names are decided, not what the tool does: `ADR-0001` had left each name to
    the item that introduces it, which is right for one command and wrong for seven, since the
    choice made on WI-0001 dictates the other six. Each command's *arguments* remain `refine`'s to
    pin on its own item.
  - **The epic now has an identity rule for people (`ADR-0005`).** A name may contain spaces; `,`
    and `=` are refused inside one because they are reserved for writing sharers and their amounts;
    two names denote the same person when equal after whitespace normalisation and case folding.
    This is epic-level because every fact the tool holds points at a person: WI-0002 resolves a
    payer and sharers, WI-0004 resolves both parties to a payment, and WI-0003 prints nothing but
    names and amounts. The human's reason for it is the one worth carrying forward — "I don't want
    two half-right versions of the same person messing up the totals."
  - **Scope is unchanged.** Neither decision adds or removes an item, and no item's `## Out of
    scope` moved. WI-0004 remains the last child.
- **Questions raised:** none.
- **Commands:** none on this epic; the commands this execution ran are recorded on WI-0001.
- **Gates:** the five gates of this execution are recorded once, on `WI-0001/journal.md`, against
  the item it was dispatched on. Listing them again here would imply a second execution.
- **Artifacts:**
  - `docs/architecture/adr/ADR-0005-person-identity-and-names.md` — new (v1)
  - `docs/architecture/adr/ADR-0006-subcommand-names.md` — new (v1)
  - `docs/product/prd.md` — v1 → v2, both decisions written into the product-level description
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — criteria and notes
    brought into line with both ADRs
- **Status:** `open` → `open` (unchanged; an epic is not transitioned by this)
- **Result:** Two epic-wide decisions recorded — what every command in this epic is called, and
  when two names are the same person. Both were answers the human gave or delegated on WI-0001; the
  children were updated so that none of them re-decides either.

## 2026-08-21T19:50:00Z — review-close v0.1.0 — reviewer

- **Item:** EP-001
- **Trigger:** not dispatched on this epic. Written because WI-0001 closed, and step 10 of
  `review-close` requires the epic to be examined whenever a child reaches `done` — including when
  the answer is that it stays open.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the success measures
  - `tracker/items/WI-0001/item.md` (now `done`, `outcome: delivered`) and its `artifacts/review.md`
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — all three at `draft`
- **Decisions:**
  - **EP-001 stays `open`.** DE1 of the epic Definition of Done — every child item is `done` —
    fails: three of the four children have not been refined yet. The epic's Definition of Done was
    therefore not applied and no success measure was assessed; doing either now would produce a
    verdict about a product that is a quarter built.
  - **What the epic has actually delivered so far**, for a reader who arrives at the epic rather
    than the item: the group's membership. `add-person` and `people`, one JSON file that survives
    between runs, and the identity rule that makes every later item's arithmetic safe — two names
    that differ only in case or spacing are one person, so the totals cannot be split between two
    half-right versions of somebody. That was the human's own stated worry when they answered
    `WI-0001/Q-002`.
  - **What the epic gained that is not visible in WI-0001's criteria**: an architecture
    (`docs/architecture/overview.md` v1), a storage decision that lets WI-0002 and WI-0004 add
    their kinds of fact without a migration (`ADR-0007` point 2, demonstrated by probe during
    verification), a command vocabulary for all seven subcommands (`ADR-0006`), and a test and
    lint story (`ADR-0008`). The next three items inherit all of it.
  - **One thing handed forward with a name on it**: `storage.save` tracebacks when the target
    cannot be written. WI-0002 and WI-0004 inherit that function unchanged, so WI-0002's `plan`
    execution is where the write-failure behaviour should be decided. Recorded on WI-0001's
    `## Notes` and in its review; repeated here so it is findable from the epic.
- **Questions raised:** none.
- **Commands:** none on this epic; the commands this execution ran are recorded on WI-0001.
- **Gates:** the six gates of this execution are recorded once, on `WI-0001/journal.md`, against
  the item it was dispatched on. The epic Definition of Done was **not** applied, because DE1
  fails and applying the rest would be theatre.
- **Artifacts:** none on the epic. `tracker/items/WI-0001/` carries everything this execution
  wrote.
- **Status:** `open` → `open` (unchanged)
- **Result:** The first of four children is delivered and merged. EP-001 remains open with
  WI-0002, WI-0003 and WI-0004 at `draft`; none of them can be refined until its predecessor is
  `done`, so WI-0002 is next.

## 2026-08-21T20:34:00Z — review-close v0.1.0 — reviewer

- **Item:** EP-001
- **Trigger:** not dispatched on this epic. Written because WI-0002 closed, and step 10 of
  `review-close` requires the epic to be examined whenever a child reaches `done` — including
  when the answer is that it stays open.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the success measures
  - `tracker/items/WI-0002/item.md` (now `done`, `outcome: delivered`) and its `artifacts/review.md`
  - `tracker/items/WI-0003/item.md`, `WI-0004/item.md` — both still `draft`
- **Decisions:**
  - **EP-001 stays `open`.** DE1 — every child item is `done` — fails: WI-0003 and WI-0004 have
    not been refined. The epic Definition of Done was not applied and no success measure was
    assessed.
  - **What the epic has delivered now**: the group's membership and its spending. Two people can
    be added and listed; an expense can be recorded with a payer and sharers, split equally by
    default or with a stated share for any subset, and listed back with each sharer's share
    worked out to the penny. The half that is missing is the half the human actually asked the
    question about — who owes whom, and marking that somebody has paid up.
  - **What the epic gained beyond WI-0002's criteria**: the stored shape of an expense
    (`ADR-0009`) with the property that adding a kind of fact needs no migration, and the rule
    that a failed write is a stated message rather than a traceback (`ADR-0010`) — the gap
    WI-0001's review handed forward, now closed for every subcommand including WI-0001's own.
  - **One thing handed forward with an owner**: nothing pins that a refusal by a *recording*
    command leaves the record file uncreated. WI-0001 pins it for `add-person`; WI-0002 does not
    for `add-expense`, and two of `verify`'s mutations survived because of it. WI-0004's
    refinement adds the third recording command and should pin it there.
- **Questions raised:** none.
- **Commands:** none on this epic; the commands this execution ran are recorded on WI-0002.
- **Gates:** the six gates of this execution are recorded once, on `WI-0002/journal.md`. The epic
  Definition of Done was **not** applied, because DE1 fails and applying the rest would be
  theatre.
- **Artifacts:** none on the epic.
- **Status:** `open` → `open` (unchanged)
- **Result:** Two of four children delivered and merged. EP-001 remains open; WI-0003 is next,
  and its dependency is now satisfied.

## 2026-08-21T21:16:00Z — review-close v0.1.0 — reviewer

- **Item:** EP-001
- **Trigger:** not dispatched on this epic. Written because WI-0003 closed and step 10 requires the
  epic to be examined whenever a child reaches `done`.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the success measures
  - `tracker/items/WI-0003/item.md` (now `done`) and its `artifacts/review.md`
  - `tracker/items/WI-0004/item.md` — still `draft`, and now unblocked
- **Decisions:**
  - **EP-001 stays `open`.** DE1 fails: WI-0004 has not been refined. The epic Definition of Done
    was not applied and no success measure was assessed.
  - **Three of four children are delivered, and the epic's central promise now works.** The group
    can be recorded, expenses can be entered and split, and `who-owes-whom` prints the payments
    that settle everybody — the thing the human asked for in their own words. What is missing is
    the second half of their answer to `EP-001/Q-001`: marking that somebody has paid up, so the
    numbers stop racking up forever. That is WI-0004 and it is the last child.
  - **Two gaps are travelling to WI-0004 with owners' names on them**, both from this review:
    `net_positions`' unasserted ordering contract, and a test fixture too small to catch a
    reordering rewrite. WI-0004 extends that function and adds a third record-writing command, so
    both land naturally in its refinement and plan rather than in somebody's memory. A third,
    from WI-0002's review — "a refusal creates no record file" is unpinned for recording commands
    — is also WI-0004's.
- **Questions raised:** none.
- **Commands:** none on this epic; they are recorded on WI-0003.
- **Gates:** the six gates of this execution are recorded once, on `WI-0003/journal.md`. The epic
  Definition of Done was **not** applied, because DE1 fails.
- **Artifacts:** none on the epic.
- **Status:** `open` → `open` (unchanged)
- **Result:** Three of four children delivered and merged. EP-001 remains open with WI-0004 at
  `draft`, now unblocked, carrying three inherited gaps that its refinement should pin.

## 2026-08-21T22:00:00Z — review-close v0.1.0 — reviewer

- **Item:** EP-001
- **Trigger:** WI-0004, the epic's last child, reached `done`. `review-close` step 10 applies the
  epic Definition of Done at exactly this moment because it is the only point where every
  sibling's state is already in hand.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the goal, the four success measures, the scope and the
    out-of-scope list
  - all four children's `item.md`, `artifacts/review.md` and `## Notes`
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v2),
    `docs/architecture/overview.md` (v4), and all eleven ADRs
- **Decisions:**
  - **EP-001 is closed, `outcome: delivered`.** DE1 to DE4 pass; the per-criterion table is in
    `WI-0004/artifacts/review.md`.
  - **All four success measures were run, not read.** The transcripts are in that review; in
    summary: three people and two expenses survived eight separate processes with nothing
    re-entered; the printed transfers took every net position to exactly zero; a payment removed
    the debt it covered and left the other untouched, and two payments produced "Everybody is
    settled up."; and every subcommand ran to completion with `socket.socket` replaced by a class
    that raises, on stock CPython 3.12.3 with no third-party import anywhere in the package.
  - **What the epic delivered, against what was asked for.** The idea was: "add people, add
    expenses paid by someone and shared by some or all, and at any point show who owes whom. Data
    must survive between runs. Python, no external services." All of it exists, as seven
    subcommands over one JSON file. The human then widened it once, in `Q-001`, to include marking
    that somebody has paid up — "otherwise the numbers just keep racking up forever and stop
    meaning anything" — and that is WI-0004. Nothing they asked for is missing.
  - **What they chose, and what was chosen for them.** They answered five questions: settlement is
    in scope (`EP-001/Q-001`), splits must handle equal and unequal (`WI-0002/Q-001`), the tool
    prints the fewest payments rather than pairwise debts (`WI-0003/Q-001`), names may contain
    spaces (`WI-0001/Q-004`), and a duplicate name is refused rather than creating a second person
    (`WI-0001/Q-002`). They delegated two — the command surface and the subcommand names — and
    deferred one, the rounding rule, saying "we'll decide later". `ADR-0003` was built so that
    later stays cheap: no derived share is stored anywhere, so changing the rule changes one
    function and no recorded data. That promise is still true at close, and `WI-0003`'s
    verification checked it against a real file rather than a document.
  - **The one thing the record contradicts itself about.** `EP-001`'s own `## Out of scope`
    excludes "free-text expense history beyond a description", which reads as though an expense
    may carry a description. None does: `prd.md` (v2) says an expense is an amount, a payer and
    sharers and "Nothing else", and WI-0002's refinement excluded a description citing it. The PRD
    governs and the product is coherent, but a reader starting here would expect a field that does
    not exist — and it is probably the first thing the group will ask for.
  - **The finding that outlives the epic, and it is about the pipeline, not the product.** Four
    reviews recorded gaps; **three of them arrived by the same route: a plan step or an ADR clause
    with no acceptance criterion behind it.** "A refusal creates no record file" (`ADR-0001`'s
    spirit, WI-0002's plan), `net_positions`' ordering contract (WI-0003's plan), and the
    `payments` shape check (`ADR-0011` point 5, WI-0004's plan step 1) were each required by a
    document, correctly implemented, and asserted by nothing — each discovered only because
    somebody ran a mutation. The criteria-driven gates cannot see them, because they check
    criteria. Two of the three were closed, by being handed forward to the next item by name;
    the third is open and recorded on `WI-0004`. Whoever runs this methodology next should know
    that handing a gap forward *by name to a specific item* worked, and that nothing automatic
    would have.
- **Questions raised:** none. All eight questions filed across this epic are `answered`, five of
  them by the human and three decided by the architect on delegated or deferred authority.
- **Commands:** the epic's four success measures and the six gates are recorded on
  `WI-0004/journal.md`; this entry adds none of its own.
- **Gates:** DE1 to DE4, with evidence, in `WI-0004/artifacts/review.md` § *Epic Definition of
  Done*. The six item-level gates of this execution are recorded once, on `WI-0004/journal.md`.
- **Artifacts:**
  - `tracker/items/EP-001/item.md` — `status: done`, `outcome: delivered`
  - `tracker/items/WI-0004/artifacts/review.md` — carries the epic's DE table and the four
    measures as run
- **Status:** `open` → `done`
- **Result:** EP-001 is delivered: seven subcommands, one JSON file, four kinds of fact, no
  network and no third-party package. Four work items, eight questions, eleven ADRs, 115 tests,
  and a record in which every decision names the skill that made it and every criterion names the
  command that checked it.
