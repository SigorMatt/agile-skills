# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T02:08:03Z — intake v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this item was
  created by that execution
- **Inputs read:** `IDEA.md`; `tracker/project.yaml`; `.claude/agile-skills/spec/work-item.md`;
  `.claude/agile-skills/spec/ids-and-statuses.md`. No prior artifact existed for this item.
- **Decisions:** see `tracker/items/EP-001/journal.md`, same timestamp, for how the work was
  split and why this is one of the parts. For this item specifically: it delivers a roster of people that is still there after the process exits, which is the persistence claim in the idea and is testable with nothing else built, and
  it is first, because WI-0002 cannot name a payer before people exist. Its acceptance criteria are deliberately left rough — they name what must be
  observable, not the command that would observe it — because the stakeholder has not yet
  answered the questions that decide them, and a polished criterion invented here would read as
  a decision nobody made. `refine` sharpens them.
- **Questions raised:** none on this item by this execution. The five open questions that bear on
  it are `EP-001/Q-001` … `EP-001/Q-005`.
- **Commands:** `python3 .claude/agile-skills/scripts/new-item --id WI-0001 …` → exit 0
- **Gates:** the four intake gates are evaluated once for the whole execution and recorded in
  full on `EP-001`: `workspace-valid` **pass**, `epic-has-success-measures` **pass**,
  `items-are-separable` **pass** (this item's order and dependency are named there),
  `no-solution-in-the-problem` **pass** (this item's title and story name no technology).
- **Artifacts:** `tracker/items/WI-0001/item.md` (new)
- **Status:** — → `draft`
- **Result:** Created at `draft` under EP-001, with the acceptance criteria intake could state
  honestly and no more.

## 2026-08-21T02:13:32Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, this item's owning status for `refine` per `pipeline.yaml`.
  Run directly rather than through `next`: `next` stops at orchestrator step 2 while the five
  questions on EP-001 are open and addressed to `human`, so it would never have dispatched
  this. Running `refine` anyway is deliberate — the stakeholder answers between turns, so every
  question that can honestly be asked now is worth asking in the same round trip as the epic's.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (the draft, AC1-AC4)
  - the item's history — one row, `- → draft` by `intake`. A fresh draft, not an item sent back
    from `verifying` or `in-review`, so this is a first refinement and the whole story is open
    rather than one specific defect
  - `tracker/items/WI-0001/journal.md` — `intake`'s entry. It records that **no** verbatim
    stakeholder answers exist, so there was nothing already answered to avoid re-asking
  - `docs/product/vision.md` (v1)
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — checked for overlap;
    neither claims the roster or the store
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — to avoid asking the stakeholder the
    same thing twice
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Did not rewrite a single acceptance criterion.** The procedure's step 5 says to rewrite
    them into decidable form, and I could have made AC3 decidable in one line by choosing what a
    duplicate does. That choice *is* the requirement, not a detail of its phrasing, and inventing
    it is precisely what the question protocol exists to prevent. The criteria stay as `intake`
    left them until Q-001 and Q-002 are answered.
  - **Filed two questions rather than four.** Where the store file lives is already
    `EP-001/Q-003`, and the command names are `plan`'s to choose, so neither was asked. Batching
    is the point: the stakeholder's attention is the scarce resource and each round trip costs a
    whole turn.
  - **Made Q-002's recommendation conditional on `EP-001/Q-003`.** Silent store creation is safe
    for a single fixed file and dangerous for a per-directory store, where running the tool in
    the wrong directory silently starts an empty ledger. Rather than ask a question whose answer
    depends on another open question, I stated the pairing and said I will record it as assumed
    if only Q-003 comes back.
  - **Recorded R4, R6, R9 and R10 honestly as failing.** No override was sought and none was
    recorded: `spec/dor-dod.md` §1 makes an override the stakeholder's act, and there was no
    stakeholder in the session to make it.
- **Questions raised:** `WI-0001/Q-001` (what identifies a person; what a repeat does),
  `WI-0001/Q-002` (first-run creation; damaged-store behaviour). Both blocking, both to `human`.
  Full record in `artifacts/refinement-qa.md`; both answers `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 1 warning
    (`commands.test` null, which `plan` owns)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to awaiting-answer …` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `scripts/validate-workspace` exit 0.
  - `definition-of-ready` (hard) → **fail**, per criterion: R1 pass, R2 pass, R3 pass,
    **R4 fail** (AC3 states no behaviour for a duplicate; AC1 and AC4 turn on Q-001/Q-002),
    R5 pass, **R6 fail** (two open blocking questions — expected for a suspended item), R7 pass,
    R8 pass (`artifacts/refinement-qa.md` written), R9 pass, **R10 fail** (duplicate name, first
    run and damaged store are three unspecified modes). Evidence for every criterion is in
    `artifacts/refinement-qa.md`. The item is **not** Ready and was not passed.
  - `criteria-are-decidable` (hard) → **fail** — AC2 can be settled today ("add people, exit, run
    the listing command in a new process, compare"). AC1 and AC4 can be settled once the commands
    exist but their verdicts depend on Q-001. AC3 cannot be settled at all: there is no
    observation that decides "the behaviour is stated and exercised".
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` holds both questions,
    both tagged `[unresolved]`, the questions deliberately not asked and why, and the
    per-criterion DoR table. Nothing is paraphrased into agreement; there is nothing to
    paraphrase, and the file says so explicitly.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` (new)
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0001/item.md` (unchanged in body; `updated` bumped by `transition`)
- **Status:** `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Not Ready, and correctly so. The stakeholder is not in this session, so `refine`'s
  precondition 2 applies: the two questions that stand between this item and the Definition of
  Ready are filed, the item is suspended, and it returns to `draft` for a second pass when they
  are answered.

## 2026-08-21T02:30:30Z — answer-questions v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`. Not dispatched by `next`: the orchestrator's step 2
  (`surface-human-questions`) stops the loop on any open question addressed to `human` and never
  reaches step 3, so `next` could not have dispatched this. The stakeholder had answered both
  questions in the files between sessions, and this skill's step 4 explicitly provides for
  `answered-by: human`, so this execution was started directly. See `**Decisions:**` below.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` (both with `## Answer` filled in by
    the stakeholder)
  - `tracker/items/WI-0001/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `tracker/items/EP-001/item.md`, and `EP-001/questions/Q-003.md` — required, because Q-002's
    recommendation was conditional on Q-003's answer
  - `docs/product/vision.md` (v1, read; v2 after this execution)
  - `docs/architecture/adr/` — empty at the time of reading; no ADR existed to contradict
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`, `spec/journal-and-history.md`
  - no `artifacts/plan.md` exists yet; the item has never been planned
- **Decisions:**
  - **Ran this skill on a human-answered question at all.** The contract's first precondition
    reads as though it only applies to questions addressed to `architect`. It is written for the
    case where the human has *not* answered; a human-addressed question whose `## Answer` the
    human has filled in is squarely this skill's job — its own step 4 provides for
    `answered-by: human` — and nothing else in the pipeline can propagate it. Recorded here
    because the precondition and step 4 disagree, and that is a defect worth fixing in the skill.
  - **Q-001 → option B (case-insensitive, repeat is an error).** Route: **recorded intent**. The
    stakeholder's second sentence decides the duplicate case outright. Their first sentence does
    not choose between A and B — it says the difference is unobservable in this group, which
    removes the only cost the question attached to B, so the standing recommendation holds rather
    than being overturned. Deciding *for* them was avoided: B is what was recommended to them and
    what they declined to contradict.
  - **Whitespace stripped before matching; first spelling wins.** Route: **decided**. Neither was
    asked. Without stripping, a trailing space silently defeats the duplicate check the
    stakeholder asked for — the same failure by another route. "First spelling wins" is forced by
    AC3's requirement that a rejected add leaves the roster exactly as it was. Both are
    reversible, and both are tagged `[assumed]` in `refinement-qa.md` rather than attributed to
    the stakeholder, per `SIMULATION-NOTICE.md`'s rule that the record must not claim more than
    it can support.
  - **Q-002 → option A (create silently; damaged store is fatal).** Route: **recorded intent**,
    with a cross-check. This question's recommendation was conditional: option C if
    `EP-001/Q-003` returned one-ledger-per-directory. It returned "One group", so the conditional
    does not fire and A is safe as well as asked for. Answering Q-002 without reading Q-003 would
    have produced the same letter for the wrong reason.
  - **A damaged store is fatal to writes, not only to reads.** Route: **decided**, from the
    stakeholder's "rather than quietly starting over with nothing". The failure being guarded
    against is a write that reads an unparseable file as empty and renames a fresh one over it;
    restricting the rule to reads would leave exactly that path open.
  - **Where the store lives — decided as ADR-0002.** Route: **decided, recorded as an ADR**. The
    record was silent (the item's own Notes said so) and three items depend on it. A fixed
    per-user path rather than the working directory, because the working directory is the option
    the stakeholder declined on `EP-001/Q-003`. `EXPENSES_STORE` added for test isolation, with
    the ADR stating explicitly that it is not a groups feature so it cannot be read as
    reinstating what was declined. Atomic writes added so an interrupted run cannot manufacture
    the damaged store AC6 must report.
  - **Did not declare the Definition of Ready met.** `refinement-qa.md` records R4, R6 and R10 as
    failed. This skill does not own the DoR, so it recorded what changed and left the re-test to
    the second `refine` pass that `resume-to: draft` produces.
- **Questions raised:** none on this item.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors,
    1 warning (`project.commands.test-null`, pre-existing; ADR-0001 tells `plan` what to set)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to draft --actor answer-questions`
    → see `**Status:**`
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in a `## Consequences` section was
    reopened and the change confirmed present: `item.md` AC3 now states the matching rule, the
    error, the non-zero exit and the unchanged roster (it previously said only that the behaviour
    "is stated"); AC4 now requires exit zero and a message; AC5 and AC6 are new and cover the
    first-run and damaged-store modes; `## Notes` no longer says the store's location is
    undecided. `refinement-qa.md` carries both answers verbatim under "Answers received".
    `docs/architecture/adr/ADR-0002-one-store-file-per-user.md` exists and is cited from AC5,
    AC6 and the Notes.
  - `answered-from-the-record` → **pass**. Q-001 cites the stakeholder's own answer plus the
    question's recommendation; Q-002 cites the stakeholder's answer plus `EP-001/Q-003`'s answer
    for the conditional; the parts the record was silent on are recorded as ADR-0002 and as
    `[assumed]` entries, not presented as answers.
  - `escalation-is-justified` → **skipped**, no escalation on this item: nothing here required
    intent the record lacks, nothing is irreversible, and no ADR existed to contradict.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft`; this
    execution transitioned to `draft`. Both blocking questions are answered, so the item is
    eligible to resume.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — answered; AC3/AC4 consequences recorded
  - `tracker/items/WI-0001/questions/Q-002.md` — answered; AC5/AC6/Notes/ADR-0002 consequences
  - `tracker/items/WI-0001/item.md` — AC3 and AC4 rewritten, AC5 and AC6 added, `## Notes`
    replaced with the storage decision
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — "Answers received" section appended
  - `docs/architecture/adr/ADR-0002-one-store-file-per-user.md` (new)
  - `docs/architecture/adr/ADR-0001-python-baseline-and-no-dependencies.md` (new, for EP-001;
    binds this item's implementation)
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both blocking questions answered from the stakeholder's own words, with the two
  gaps their words left — the matching details and the store's location — decided and recorded
  as assumptions and as ADR-0002 respectively. The item returns to `draft` for a second `refine`
  pass, which is what must re-test the three Definition of Ready criteria that failed.

*Correction to the entry above, appended immediately after it (`spec/journal-and-history.md` §1:
a wrong entry is corrected by a later entry, never by rewriting).* The `**Commands:**` bullet
lists `validate-workspace` as exit 0, which is what it returns now and what the gate report
printed after the move. It is not what `transition`'s pre-move gate run printed. That run
reported `workspace-valid` as **FAIL** with two errors — `board.stale`, and
`question.awaiting.none-open` on this item — because it evaluates the gates against the workspace
*before* the transition it is about to make: at that moment the item was still `awaiting-answer`
while its two questions had already been set to `answered`, which is precisely the state this
skill has to pass through, and the board had not yet been regenerated for a status that had not
yet changed. `transition` itself printed `gates reported above are NOT blocking this move`,
because `answer-questions` gates only its completion transition, and made the move; the
post-move validation in the same output is `0 errors, 1 warning`. Recorded because a hard gate
printing FAIL on the way to a legitimate move is a toolkit defect worth fixing — the check is
being run against the wrong side of the transition — and because a reader comparing this journal
to a terminal transcript would otherwise conclude the entry was falsified.

## 2026-08-21T02:40:30Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (selection key: priority `critical`, rank 1,
  beating WI-0002 and WI-0003 at `high`; no open blocking questions; no `depends-on`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md`,
    `artifacts/refinement-qa.md` — the history first, per precondition 3: this item reached
    `draft` from `awaiting-answer`, not from a send-back, so it is a resumed first refinement and
    not a defect fix
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both now `answered`, with the
    stakeholder's words
  - `.claude/agile-skills/spec/dor-dod.md` §1 (the ten criteria), `spec/journal-and-history.md`
  - `docs/architecture/adr/ADR-0001-python-baseline-and-no-dependencies.md`,
    `ADR-0002-one-store-file-per-user.md`
  - `tracker/items/EP-001/item.md` — for the success measure AC8 localises
- **Decisions:**
  - **Asked the stakeholder nothing, and did not file a question.** Precondition 2 says that when
    the human is absent, `refine` files a question listing **what it needs** and stops. It needed
    nothing: the two questions this item was suspended on were answered between sessions and
    propagated, and step 1 forbids re-asking what has already been answered. Filing a question
    with nothing in it would have cost a full round trip and returned no information. Everything
    this pass added is tagged `[assumed]` by `refine` in `refinement-qa.md` and is attributed to
    this skill, never to the stakeholder — which is what `SIMULATION-NOTICE.md` requires of the
    record.
  - **AC1 rewritten.** It named no observable output, so an implementation printing
    `1. Alice (added today)` and one printing `Alice` would both satisfy it and `verify` could
    not choose. Now: both commands appear in `--help`; a non-empty listing prints one bare name
    per line, in insertion order; exit zero.
  - **Listing order fixed as insertion order** (`[assumed]`). Without an order, two correct
    implementations print different things and AC2 becomes an unordered set comparison, which is
    a weaker check for the property AC2 exists to test. Insertion order needs no rule explained
    to the group and is trivially reversible.
  - **AC2 tightened to a *fresh* process.** The criterion exists to prove the data is on disk;
    a test that reuses the interpreter would pass while proving nothing about persistence.
  - **AC7 added** for the empty, whitespace-only and absent name. `[assumed]`. Left open, AC3's
    matching rule would end up comparing empty strings, and a nameless person is not something
    anyone would want.
  - **AC8 added** for tracebacks and stream discipline. Not a new requirement — it is EP-001's
    fourth success measure — but `verify` reads the item, not the epic, and this is the item that
    introduces the file I/O producing most of the failures. Localising it here is what makes it
    testable at all.
  - **Name character rules deliberately *not* decided.** Recorded under
    `## Deliberately unconstrained` with `plan` named as the owner. The decision turns on whether
    WI-0002 takes sharers as a comma-separated list or a repeated flag, which is `plan`'s to make
    and does not exist yet; constraining names now would couple this item to a design that has not
    been chosen. R10 requires such a gap to be **visible**, not resolved, and this satisfies it
    without inventing a constraint nobody asked for.
  - **No Definition of Ready override.** None was needed and none was recorded. Naming a criterion
    as overridden when it is not failing would be a false entry in the record.
- **Questions raised:** none. Two pre-existing questions (`Q-001`, `Q-002`) are answered; four new
  assumptions are recorded as `[assumed]` in
  `tracker/items/WI-0001/artifacts/refinement-qa.md`, none `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`; ADR-0001 §3 tells `plan` what to set)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to ready --actor refine` → see
    `**Status:**`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0)
  - `definition-of-ready` → **pass**, per criterion: R1 pass, R2 pass, R3 pass,
    **R4 fail → rewrote AC1 and AC2, added AC7 and AC8, now pass**, R5 pass,
    **R6 fail → both questions answered between sessions, now pass**, R7 pass, R8 pass, R9 pass,
    **R10 fail → added `## Deliberately unconstrained` naming four open points and their owners,
    now pass**. The full table with evidence is in `artifacts/refinement-qa.md`.
  - `criteria-are-decidable` → **pass**. Each of AC1–AC8 taken in turn and matched to the
    observation that settles it: AC1 `--help` plus a listing after two adds; AC2 the same listing
    from a new process; AC3 a second `add` of the same name in a different case and with padding,
    checking exit status, stderr and the unchanged listing; AC4 a listing against an empty store;
    AC5 a listing and an add against a path that does not exist; AC6 a store containing invalid
    JSON, checking that both a read and a write fail and that the file's bytes are unchanged
    afterwards; AC7 an add with `""`, with `"   "`, and with no argument; AC8 stderr, stdout and
    exit status across every failing case above. Searched the criteria for unmeasurable
    adjectives — "appropriate", "reasonable", "clean", "properly", "gracefully" — none occurs.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` carries the stakeholder's two
    answers verbatim under "Answers received", tagged `[human]`, and this pass's four additions
    tagged `[assumed]` with `refine` named as their author. No answer was paraphrased into
    something more confident than it was.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC1 and AC2 rewritten, AC7 and AC8 added,
    `## Deliberately unconstrained` added
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — "Second refinement pass" appended with
    the per-criterion DoR table
  - the board, regenerated
- **Status:** `draft` → `ready`
- **Result:** Ready, without an override and without asking the stakeholder anything they had not
  already answered. Eight criteria, each with a named observation that settles it, and four
  points left deliberately open with `plan` named as the owner of the one that matters — what
  characters a name may contain, which cannot be decided before the sharer syntax exists.

## 2026-08-21T02:45:00Z — plan v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` (only `critical` item; WI-0002 and WI-0003 are
  `high` and still `draft`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC8, `## Notes`, `## Deliberately unconstrained`),
    `history.md`, `journal.md`, `artifacts/refinement-qa.md` — the `[assumed]` entries in
    particular, since they are where the design's ground is soft
  - `tracker/items/WI-0002/item.md` and `WI-0003/item.md` — required, not optional: the gap
    `refine` handed to `plan` can only be answered by deciding WI-0002's sharer syntax
  - `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1), `ADR-0003` (v1), `ADR-0004` (v1),
    `ADR-0005` (v1) — all five read; ADR-0002 and ADR-0006 govern this item, the others bound
    what the overview may claim
  - `docs/product/vision.md` (v2), `tracker/items/EP-001/item.md`
  - `tracker/project.yaml`, `.claude/agile-skills/spec/doc-header.md`,
    `spec/journal-and-history.md`
  - **The code that already exists:** none. `ls` of the repository root shows `.claude`, `docs`,
    `tracker` and the four markdown files — no `expenses/`, no `tests/`, no Python at all. This
    is the first item planned in the project, so step 2 of the procedure ("read the code this
    change touches") had nothing to read, and precondition 3 fired: `docs/architecture/overview.md`
    did not exist and was created here.
  - `python3 -V` → 3.12.3, against the 3.9 floor `ADR-0001` sets. The floor bounds what may be
    *used*, not what it runs on; recorded because a reader will otherwise wonder whether 3.9 was
    chosen in ignorance of what is installed.
- **Decisions:**
  - **Answered the gap `refine` left, as `ADR-0006`.** Route: **decided**. WI-0001's
    `## Deliberately unconstrained` named `plan` as the owner of "what characters a name may
    contain" and gave the reason it could not be settled earlier. The answer runs through the CLI:
    sharers are a **repeated `--with` flag** and no argument value is ever split on a delimiter,
    so no character is reserved and a name may contain anything printable. Only control
    characters are rejected, and for a stated reason — a newline would break AC1's one-name-per-
    line listing, and a carriage return or escape sequence can overwrite what a terminal has
    already drawn.
  - **Fixed the whole CLI surface now, not just this item's two commands.** Route: **decided**,
    recorded in ADR-0006 rule 2. A command line designed one item at a time ends up with three
    spellings of the same idea, and `WI-0002`'s syntax had to be decided here anyway.
  - **`ExpensesError` as the single failure type, caught once in `cli.main()`.** Route:
    **decided**. AC8 forbids tracebacks and fixes stream discipline; making that a property of
    one `except` clause means there is one place to check and a new failure added later cannot
    forget the rule. The alternative — each call site handling its own errors — passes AC8 today
    and decays.
  - **The store is loaded and saved whole.** Route: **decided**. The data is a friend group's
    dinners; anything cleverer would complicate the atomic replace `ADR-0002` decision 7 requires
    without buying anything.
  - **`load()` before any write in `add-person`.** Route: **from the record** (`ADR-0002`
    decision 6). It is what makes AC6's "a damaged store must not be overwritten" true by
    sequencing rather than by a check somebody could remove.
  - **Did not create `money.py`, `expenses.py`, `balances.py` or `settle.py` as empty modules.**
    Route: **decided**. They are named in the overview because the shape matters now; creating
    them empty would read as decisions already taken, and no AC maps to them. Recorded under the
    plan's `## Out of scope for this item`, which is where the procedure's "delete any step no AC
    maps to" check landed.
  - **Four assumptions recorded rather than escalated**, all in the plan's `## Assumptions` with
    what reversal costs: the store's top-level shape, `people` as bare strings, exit status 2, and
    the exact wording of the confirmation and empty-group messages. Route: **assumed**, branch 2
    of `question.md` §1. Assumption 2 is flagged in `## Risks` as the only one that would cost a
    data migration, so a later reader can find the one soft spot without re-reading the plan.
  - **`commands.test` set to `python3 -m unittest discover -s tests -t .`** Route: **from the
    record** (`ADR-0001` §3, which instructed `plan` to write exactly this). `commands.lint` and
    `commands.build` stay `null`, each with an inline comment citing the ADR section that makes
    the absence deliberate, so a future reader does not "fix" them.
  - **Nothing was asked of the human.** No decision here is irreversible or turns on intent the
    record does not hold, so `question.md` §1's third branch did not apply.
- **Questions raised:** none.
- **Commands:**
  - `ls -a` in the repository root → no source tree exists yet
  - `python3 -V` → `Python 3.12.3`
  - `python3 -m unittest discover -s tests -t .` → **fails**, `ImportError: Start directory is
    not importable: 'tests'`. Reported honestly rather than smoothed over: the command is correct
    and is not yet green, because the directory it discovers does not exist. Plan step 1 creates
    `tests/__init__.py`, and the plan's `## Risks` says this in as many words so `implement` meets
    it before it meets a red gate.
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, **0 errors, 0
    warnings** — the pre-existing `project.commands.test-null` warning is cleared by this
    execution
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to planned --actor plan` → see
    `**Status:**`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 warnings)
  - `every-criterion-is-addressed` → **pass**. The `## Acceptance criteria mapping` table in
    `artifacts/plan.md` carries a row for each of AC1–AC8, and each `demonstrated by` cell names
    the specific observation rather than the word "tests": AC1 `--help` contents plus an exact
    two-line listing; AC2 three separate `subprocess.run` interpreters; AC3 three collision
    spellings with the roster asserted unchanged; AC4 an empty temporary directory; AC5 parent
    creation plus a fresh-process listing; AC6 both a read and a write against invalid JSON with
    the file's bytes compared before and after; AC7 three ways of giving no name; AC8 the absence
    of `"Traceback"` and the stream and exit-status assertions across every failing case.
  - `project-commands-resolved` → **pass**. `commands.test` is set; `commands.lint` and
    `commands.build` are `null` **by decision**, each citing `ADR-0001`, which is the honest form
    the gate description asks for rather than inventing a command that does nothing.
  - `decisions-recorded` → **pass**. One new ADR (`ADR-0006`), five existing ADRs cited by number
    in the plan's `## Decisions and ADRs` with the route each answer came from, and four
    assumptions recorded with their reversal cost.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new)
  - `docs/architecture/overview.md` (new, v1)
  - `docs/architecture/adr/ADR-0006-cli-surface-and-what-a-name-may-contain.md` (new, v1)
  - `tracker/project.yaml` — `commands.test` set; `lint` and `build` annotated
  - the board, regenerated
- **Status:** `ready` → `planned`
- **Result:** Eight steps, each naming its files and what is true afterwards, with every
  criterion mapped to a specific observation. The gap `refine` deliberately left open is closed
  by `ADR-0006`, which decides the sharer syntax first and gets a permissive name rule as the
  consequence. The one thing `implement` must do before anything else is create `tests/`, without
  which the newly-set test command errors rather than passing empty.

## 2026-08-21T02:50:00Z — implement v0.1.1 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next` (only `critical` item)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC8, `## Notes`, `## Deliberately unconstrained`),
    `artifacts/plan.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered`; per step 2 their
    answers were **not** acted on from the question files, they were read from `item.md` and
    `ADR-0002`, which is where `answer-questions` propagated them
  - `tracker/project.yaml` (`commands.test` now set), `docs/architecture/overview.md` (v1),
    `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1), `ADR-0006` (v1)
  - the branch: `git branch -a` showed only `main`, so no partial work existed to reconcile with
  - the source tree: empty. This is the first code in the project
- **Decisions:** (all inside the plan's latitude; none changed *what* is delivered)
  - **The temporary file for the atomic write is created with `mkstemp(dir=path.parent)`.** The
    plan required the store's own directory, and the reason is in its `## Risks`: `os.replace` is
    atomic only within one filesystem, so a temporary file in `/tmp` would silently degrade to a
    copy and reintroduce exactly the half-written file `ADR-0002` decision 7 exists to prevent.
    Every test in this item would still pass, which is why it is called out.
  - **`load()` validates the document's shape, not only that it is JSON.** A file containing
    `["Alice", "Bob"]` is refused. The plan said so; it is journalled because AC6's wording
    ("cannot be read or parsed") does not obviously reach it, and a reader should not have to
    infer that the check is deliberate.
  - **`main(argv=None, out=None, err=None)`.** Two extra parameters not in the plan, so the domain
    can be exercised in-process later without a subprocess. No behaviour depends on them, and the
    end-to-end tests deliberately do not use them: AC2 and AC8 are claims about the process
    boundary, and testing them in-process would assert nothing.
  - **`FAILURE = 2`, matching argparse's own usage-error status**, per the plan's assumption 3, so
    the tool does not have two meanings for "you got it wrong".
  - **Ran the whole suite after every step**, not once at the end, so a regression introduced in
    one step could not be attributed to another.
  - **Did not fix anything I noticed on the way.** Nothing outside the plan's file list was
    touched, with one exception I made and undid: I appended `__pycache__/` and `*.py[cod]` to
    `.gitignore`, which already ignored both. Reverted in `7d02a68` so this item's net diff
    contains no `.gitignore` change. Declared rather than quietly left, because the mistaken
    commit is in the history.
- **Questions raised:** none. Nothing in the plan was silent on a decision that was not mine to
  make: `ADR-0006` had already settled the one thing `refine` flagged (what a name may contain),
  which is exactly what stopped this execution needing a round trip.
- **Commands:**
  - `git branch -a` → `main` only; `git checkout -b wi/WI-0001` → branch created from `main`
  - `python3 -c "import expenses.store"` → exit 0, after step 3
  - a manual three-call smoke of `add-person Alice` / `people` / `add-person alice` → `0 0 2` with
    the duplicate message on stderr, after step 5
  - `python3 -m unittest discover -s tests -t .` → after step 6: exit 0, `Ran 5 tests … OK`;
    after step 7, on the branch head: **exit 0, `Ran 18 tests in 1.560s … OK`**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to in-progress --actor implement`
    → succeeded, and its post-move validation reported
    `journal.execution.missing: 'implement' appears as an actor in history.md but wrote no
    journal entry`. That error is unavoidable as the procedure is written and is not a defect in
    this execution: step 3 requires the move to `in-progress` **before** any code is written, so
    that an interruption leaves a truthful status, while step 9 requires the journal entry to be
    written at the end. Every `implement` run must therefore pass through a window in which the
    validator is red. Recorded as a toolkit finding; the fix would be for the validator to exempt
    `in-progress`, or for `transition` to accept a placeholder entry.
- **Gates:** run on the branch head `7d02a68`, after the last change.
  - `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .`, exit 0, 18 tests.
  - `lint-clean` → **skipped**, with the reason: `commands.lint` is `null` **by decision**, because
    there is no linter in the standard library (`ADR-0001` §4, which anticipates this exact skip).
    Not recorded as a pass.
  - `workspace-valid` → **pass**. `validate-workspace`, exit 0, 0 errors, 0 warnings.
  - `every-criterion-has-a-test` → **pass**. The table in `artifacts/impl-report.md` names, for
    each of AC1–AC8, the test that demonstrates it by its full node id. AC8's evidence is
    `assertFailedCleanly()`, applied to nine failing invocations across five tests.
  - `commits-reference-the-item` → **pass**. `git log --grep WI-0001 --oneline` returns every
    commit on the branch; each subject matches `<scope>: <summary> (refs WI-0001)`.
- **Artifacts:**
  - `expenses/__init__.py`, `__main__.py`, `errors.py`, `store.py`, `people.py`, `cli.py` (new)
  - `tests/__init__.py`, `tests/test_store.py`, `tests/test_cli.py` (new)
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
  - branch `wi/WI-0001`, commits `8e2ceaa..7d02a68` (`c8cdd73` the feature, `7d02a68` the
    `.gitignore` revert)
- **Status:** `in-progress` → `verifying`
- **Result:** All eight criteria implemented and tested, 18 tests green on the branch head, one
  gate honestly skipped rather than claimed. Handing to verification with one thing named for it
  in `## What I did not do`: I did not confirm by mutation that each test goes red when the
  behaviour is removed, and AC3 and AC6 are the two where that matters, because their assertions
  are about something *not* changing.

## 2026-08-21T03:02:03Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next` (highest-ranked runnable item: priority
  `critical`, no open blocking question, no `depends-on`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eight criteria, **read first and in full**, and the
    checks for each derived from the criterion before anything built was looked at
  - `tracker/items/WI-0001/artifacts/plan.md`, `artifacts/impl-report.md` (read *after* the
    criteria and after deriving the checks), `artifacts/refinement-qa.md` (for AC8's wording),
    `history.md`
  - `tracker/project.yaml` — `commands.test`, and `commands.lint: null`
  - the code on `wi/WI-0001` at `b74757f9f472d70d2731f485358df1cdd029620b`: all five modules of
    `expenses/` and both test files, read in full
  - `.claude/agile-skills/spec/dor-dod.md` §3 (D2, D3, D10), `spec/skill-contract.md` §1.3 (what
    `enforcement: advisory` permits), `spec/question.md`
- **Decisions:**
  - **Chose evidence that distinguishes the two readings, not evidence that agrees with the
    code.** AC1 and AC2 say "in the order they were added". A roster of `Alice, Bob` cannot show
    that, because it is also alphabetical order. The check used `Alice, Bob, Zoe, Carol`, where
    insertion order and alphabetical order differ. This turned out to be the single most
    productive decision of the execution — see the next one.
  - **Recorded `tests-would-fail-without-the-change` as FAIL for AC1/AC2, and still passed the
    item.** Replacing `listing()` with `sorted(...)` breaks no test in the suite, because every
    ordering assertion uses `Alice` then `Bob`. The *behaviour* is right — demonstrated
    independently, with names that distinguish the orders — so AC1 and AC2 pass on evidence. What
    is missing is the item's protection of them. Three routes were considered and two rejected:
    **send-back to `in-progress`** — rejected, because no acceptance criterion of this item
    requires test sensitivity, and sending an item back on a standard the item does not carry is
    the scheduler-style judgement this pipeline exists to keep out of the record;
    **file a bug item** — rejected, because bug DoR `RB3` requires naming the criterion, doc or
    ADR the behaviour contradicts, and there is none: no document in this project says tests must
    be sensitive, so the entry would have been a fabrication;
    **pass, and put it in front of the reviewer in writing** — taken, because
    `spec/skill-contract.md` §1.3 says `advisory` means "run it, record the result, and may
    proceed on failure with the reason journaled", and because `review-close` owns D2 ("every
    ticked criterion cites its evidence") and is the right place for the judgement. The fix is one
    line of test data and is named as such in the report.
  - **Passed AC8 despite argparse printing two lines where AC8 says "one-line".** Not decided on
    preference: `plan.md` step 5 explicitly chose argparse's native output for this exact
    invocation ("do not re-implement it"), and AC8 states its own purpose as EP-001's fourth
    success measure, whose contrast is message-versus-traceback. Recorded as its own section in
    the report, with the exact output quoted, so a reviewer can disagree with the evidence rather
    than with a verdict. **No question was filed**: the criterion is not ambiguous in a way the
    record leaves open — the record settles it — and filing one would have suspended the item to
    re-ask something `plan` already answered.
  - **Judged the bare `python3 -m expenses` invocation an undeclared behaviour, not a failure.**
    It prints 11 lines of help to stderr and exits 2, and appears in no plan step and no criterion.
    Procedure step 6 says record it, and step 7's test — *does an acceptance criterion of this
    item say the behaviour should be different?* — answers no: AC8 is scoped to "this item's
    commands", and a bare invocation runs neither of them. Recorded under `## Defects found` as an
    observation so the decision about it is visible rather than absent.
  - **Went beyond the criteria on AC6 deliberately.** AC6 says "cannot be read **or** parsed", and
    the item's own tests only cover the parse case. The read case was exercised four further ways
    — non-UTF-8 bytes, `chmod 000`, a directory in the store's place, and valid JSON that is not a
    store in three shapes — all on **both** the read and the write command, with a checksum before
    and after each. 14 invocations. AC6's most dangerous clause is about the write path, so
    checking only reads would have left the clause that matters untested by this skill.
  - **Never wrote to the machine's own store.** Every check set `EXPENSES_STORE` into
    `.harness/verify-WI-0001/` (git-ignored). The consequence is declared under `## Not verified,
    and why`: the two default-path fallback branches in `store.store_path()` were read but not
    executed.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 18 tests in 1.628s`, `OK`
  - `python3 -m expenses --help` → exit 0; lists `add-person` and `people`
  - `python3 -m expenses people` (no store) → exit 0, stdout `Nobody in the group yet.`
  - `python3 -m expenses add-person Alice` (missing parents) → exit 0, `Added Alice.`; store and
    two parent levels created
  - `add-person Bob`, `add-person Zoe`, `add-person Carol`, `add-person "   Dave   "` → exit 0 each
  - `python3 -m expenses people | od -c` → `A l i c e \n B o b \n Z o e \n C a r o l \n` — bare
    names, one per line, insertion order
  - `add-person` × 4 duplicate spellings (`alice`, `ALICE`, `"  Alice  "`, `aLiCe`) → exit 2 each,
    stderr `Alice is already in the group; nothing was added`, store `sha256sum` unchanged
  - `add-person ""` / `"     "` / `"<tab>"` / no argument → exit 2 each, roster unchanged
  - 7 damage kinds × `people` and `add-person Bob` = 14 invocations → exit 2 each, path named,
    `sha256sum` unchanged after every one
  - traceback sweep: 11 failing and 4 succeeding invocations checked for `Traceback` in both
    streams, stream discipline and exit status → no traceback anywhere
  - `python3 .harness/verify-WI-0001/sensitivity.py` → 8 mutations, 7 caught, 1 not; tree restored
  - `git diff -- expenses tests` → empty (mutations reverted); suite re-run → exit 0, 18 passed
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `tests-pass` → **pass**. Run by this skill on the branch head, not read from the report.
  - `lint-clean` → **skipped, not passed**. `commands.lint` is null by `ADR-0001` §4. What it
    leaves unchecked is written into `## Not verified, and why` rather than left implicit.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `every-criterion-independently-checked` → **pass**. Eight rows, each citing a command this
    skill ran and its actual output. No row's evidence is a test name from `impl-report.md`.
  - `negative-cases-exercised` → **pass**. Every error, empty-input and boundary clause across
    AC3–AC8 was triggered and its output recorded; roughly 40 invocations in total.
  - `tests-would-fail-without-the-change` → **FAIL** (advisory). 7 of 8 behaviours protected;
    AC1/AC2's ordering is not. Proceeding is permitted by `spec/skill-contract.md` §1.3 and the
    reason is the second Decision above.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new) — verdict, the eight criteria with
    commands and actual output, the gates, the negative cases, the sensitivity table, the two
    findings, and five declared gaps
  - `tracker/items/WI-0001/item.md` — AC1–AC8 all ticked, each against a row of that table;
    `updated` bumped
  - no bug item filed; no `docs/` change (this execution changed no behaviour and invalidated no
    document)
- **Status:** `verifying` → `in-review`
- **Result:** All eight acceptance criteria met, on evidence this skill gathered itself. Two things
  are handed to `review-close` rather than buried: the item's tests cannot distinguish insertion
  order from alphabetical order, so AC1/AC2 are correct but unprotected; and the bare-invocation
  behaviour belongs to no criterion and no plan step.

## 2026-08-21T03:08:15Z — review-close v0.1.2 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` (highest-ranked runnable item: priority
  `critical`; no open question anywhere in the workspace)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md` (8 rows), `journal.md` (**all seven entries, in
    full** — D5 certifies the record's completeness and cannot be done from a skim),
    `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`,
    `artifacts/refinement-qa.md`, `questions/Q-001.md`, `questions/Q-002.md`
  - **the diff `main...wi/WI-0001`, hunk by hunk** — 421 added lines across nine new files under
    `expenses/` and `tests/`, plus the tracker and `docs/` hunks. Not the reports about it
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0006`, and `docs/architecture/overview.md`,
    read **against the code** for D12 rather than recalled
  - the branch's git topology: `git log main..wi/WI-0001` and which commit touches which path
  - `.claude/agile-skills/spec/dor-dod.md` §3, `spec/journal-and-history.md`,
    `spec/skill-contract.md` §1.3
- **Decisions:**
  - **Rejected the item.** All eight criteria are met and correctly ticked, and the verification
    is strong — but two defects in the change would land on WI-0002, and this is the only stage
    that checks for those. Detail in `artifacts/review.md` `## Findings`; the two are summarised
    in the next two bullets. Rejection is the designed outcome here, not a failure of the item.
  - **Finding 1 — `people.match_key()` is dead and AC3's rule is written out twice — send-back.**
    Found by reading the diff, not by any report: `plan.md` step 4 says `add()` raises *"if
    `match_key` collides"*, and the delivered `add()` inlines `stripped.lower()` and
    `existing.lower()` instead. `grep -rn 'match_key' expenses tests` returns one hit — the
    definition. So the function both `plan.md` and `impl-report.md` present as *"AC3's comparison
    key"* is unreferenced and untested. Behaviour is identical today, which is why no criterion
    catches it. The reason it is a send-back rather than an accepted gap is specific: WI-0002 must
    decide whether a sharer's name is a roster person — the same question AC3 answers — and will
    find `match_key` sitting there for exactly that purpose; and `ADR-0006` line 92 records
    `str.lower()` as a known-imperfect choice, so the one place someone will edit is the one place
    that is not wired in. Also: `impl-report.md` declares three deviations from the plan and this
    is not among them, so the record currently says the plan was followed here.
  - **Finding 2 — AC1/AC2's ordering is unprotected — send-back.** `verify` raised it as an
    advisory gate failure and correctly left the decision here. Deciding it: send back.
    `spec/skill-contract.md` §1.3 permits proceeding on an advisory failure, so this is a
    judgement, and the reasoning is that `test_listing_prints_one_bare_name_per_line_in_insertion_order`
    **asserts insertion order in its name and does not test it** — `Alice`/`Bob` is also
    alphabetical order, so `listing()` can be replaced with `sorted(...)` and the suite stays
    green. A test whose name claims a property it cannot detect is worse than no test, because a
    ticked criterion is never re-examined; and `item.md` `## Notes` says this item is the
    foundation WI-0002 and WI-0003 both build on. The fix is one line of test data. AC1 and AC2
    stay ticked: the behaviour is right and `verify` proved it.
  - **Finding 3 — repaired the branch topology rather than overriding a hard gate or blocking.**
    `check-commit-refs` failed (exit 1): two commits on `main..wi/WI-0001` name EP-001, not
    WI-0001. They are epic-level record commits from `answer-questions` acting on the epic, which
    landed here only because HEAD happened to be on this branch. Three routes were considered.
    **Amend their messages to name WI-0001** — refused, it would put a false statement in the
    history. **Merge first, close after** — refused, it is the deadlock `SKILL.md` step 8 warns
    about, and `commits-reference-the-item` inspects a range that is empty after a merge. **Set
    the item `blocked`** — refused: `blocked` is terminal and needs a human, and this is a
    misplaced commit, not an impasse. So the topology was corrected: the two commits were moved
    off the item branch and onto `main`, where epic-level record commits belong. That is the only
    route that makes the gate pass on its merits. Nothing was published; both pre-repair refs are
    tagged (`pre-review-close-WI-0001` = `9ef63781`, `pre-review-close-main` = `8e2ceaa4`); every
    conflict was in the generated board and was resolved with `scripts/board-gen`. Old → new
    hashes are recorded in `review.md`, along with the consequence that
    `verify-report.md`'s `Verified-commit` now names an unreachable commit — which the re-verification
    this rejection triggers will replace.
  - **Recorded Finding 3 as a defect in the methodology.** `answer-questions` acting on an epic is
    told to commit and told nothing about which branch to be on, so every future epic-level answer
    will land on whatever item branch is checked out and fail that item's
    `commits-reference-the-item`. No skill in this project can fix it from the inside; it is in
    `review.md` and in `HARNESS-STATUS.md` for the toolkit's owner.
  - **Correction: the `verify` entry's heading was restamped, and this bullet is the record of
    it.** Old value `2026-08-21T03:20:00Z`, new value `2026-08-21T03:02:03Z`, which is the stamp
    `scripts/transition` put on the history row that same execution wrote. The old value was
    wrong — it was written from a guess rather than read from the clock, it sat 18 minutes in the
    future of the real time (`03:02:32Z`), and it claimed the execution finished after the
    transition it describes.

    The restamp was not the first choice. This entry was written and appended with its own
    truthful heading, `03:08:15Z`, read from `date -u`, and the intent was to leave the wrong
    heading in place and correct it in prose — journals are append-only, and
    `spec/journal-and-history.md`'s one sanctioned restamp exception is written for **history**
    rows. `validate-workspace` then failed:

    ```
    tracker/items/WI-0001/journal.md:602: ERROR [journal.order] entry timestamp
    2026-08-21T03:08:15Z is earlier than the previous entry (2026-08-21T03:20:00Z)
    ```

    That is the exception's own situation, arriving in the other file: an earlier entry carries a
    wrong clock, the correct next entry is legitimately earlier than it, and **no appended entry
    can ever repair the pair** — every future entry on this item would fail the same check until
    one of them lied. The alternative was to stamp this entry `03:20:00Z` or later, which would
    have propagated the fabrication forward and made the item's whole timeline wrong rather than
    one heading. So the spec's rule was applied to the file it was not written for, with the same
    discipline it demands: one heading changed, to a value not earlier than what precedes it,
    nothing else in the entry touched, and the old value, the new value and the reason recorded
    here.

    The same drift is in the `implement` entry — headed `02:50:00Z` against a `02:48:40Z` history
    row — and it is left alone, because it breaks no ordering and appending is enough. **Skills in
    this run are writing plausible timestamps instead of reading the clock**, and the validator
    only catches it once the drift runs backwards. That is a finding about the toolkit: nothing
    stops a skill inventing a heading, and `spec/journal-and-history.md`'s restamp exception
    should cover `journal.md` explicitly, since the failure it describes plainly occurs there.
  - **Accepted five gaps and wrote every one into `item.md` `## Notes`**, not into `review.md`
    alone: the bare-invocation help output, the total absence of static analysis, the
    inspection-only atomic-write check, the two never-executed default store-path branches, and
    concurrent writes losing a person. An accepted gap recorded only in a review report stops
    being true the moment the item closes. Note the connection worth having: Finding 1 is a dead
    function, which is exactly what the linter this project decided not to have would have caught
    in a second.
  - **Did not trial-merge and did not merge.** `SKILL.md` step 8 follows acceptance, and this is a
    rejection. `wi/WI-0001` is intact with all four of its commits; `main` is unchanged apart from
    the two EP-001 commits that belong to it.
- **Questions raised:** none. Nothing here contradicts an ADR, so `question.md` §4's escalation
  conditions do not apply.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0
    (before the repair, and again after: verified at `b74757f9`, branch at `2b3efc4c`, only
    `tracker/` and `docs/` differ)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → **exit 1**
    before the repair (2 of 6 commits named EP-001); → exit 0 after (`all 4 commit(s) … name
    WI-0001`)
  - `git tag pre-review-close-WI-0001 wi/WI-0001` / `git tag pre-review-close-main main`
  - `git rebase --onto fb7e3ac b74757f wi/WI-0001` → 1 board conflict, resolved by `board-gen`
  - `git cherry-pick ed25f27 b74757f` on `main` → 2 board conflicts, resolved by `board-gen`
  - `git rebase main` on `wi/WI-0001` → 3 board conflicts, resolved by `board-gen`
  - `git diff --name-only --diff-filter=U` at each stop → `tracker/board.md` and nothing else,
    every time
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 18 tests in 1.525s`, `OK`, on the
    rebased branch
  - `grep -rn 'match_key' expenses tests` → one hit, the definition (evidence for Finding 1)
  - `grep -c '^- \[x\] AC' tracker/items/WI-0001/item.md` → 8 (evidence for D1)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `cat .gitignore` → the five correct lines; the duplicate-rules revert replayed correctly
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-21T03:08:15Z`, this entry's heading
- **Gates:**
  - `definition-of-done` → **fail, deliberately**, and recorded criterion by criterion in
    `review.md` `## Definition of Done`. D1–D8 and D10–D12 pass with per-criterion evidence; **D9
    (merged into the trunk) is not met by decision**, because the item is rejected. A single
    overall verdict would not have satisfied this gate and none was written.
  - `verification-postdates-the-code` → **pass**. `check-verify-freshness` exit 0, run twice —
    before the repair and again after it, since the repair changed every hash on the branch.
  - `commits-reference-the-item` → **pass, after the repair described in Finding 3**. Exit 1
    before, exit 0 after. No override was used and none was reached for.
  - `tests-pass-on-the-merge-result` → **skipped, not passed**. There is no merge result: the item
    is rejected, so `SKILL.md` step 8 was never entered. The suite was run on the rebased branch
    head (exit 0, 18 tests) and that is recorded under D3, but it is not this gate and is not
    claimed as it.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `record-is-reconstructible` → **pass**. Answered from the tracker, `docs/` and `git log`
    alone: *what was built and why* — `item.md` `## Story` and `plan.md` `## Problem`, with
    `IDEA.md` and `vision.md` behind them; *which skill decided what* — `history.md`'s `actor`
    column across 8 rows and the 7 journal entries, with `plan.md` `## Decisions and ADRs`
    labelling each decision's route; *what questions arose and how they were resolved* — `Q-001`
    and `Q-002`, both `answered-by: human`, both with `## Consequences` naming the files that
    changed, and AC3–AC6 visibly carrying those answers; *what verification found* — eight
    criteria with commands and real output, one advisory gate failure with its mutation table, and
    five declared gaps. The one thing a reader could **not** previously reconstruct was why
    `match_key` exists and nothing calls it; Finding 1 records it.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, the twelve DoD
    criteria with evidence, five findings, the accepted gaps, and what `implement` must do next
  - `tracker/items/WI-0001/item.md` — new `## Accepted gaps` section carrying all five; criteria
    untouched and still ticked
  - git: `main` `8e2ceaa4` → `d457169` (the two EP-001 commits, cherry-picked to where they
    belong); `wi/WI-0001` `9ef63781` → `2b3efc4c` (same four commits, rebased); tags
    `pre-review-close-main` and `pre-review-close-WI-0001` left in place as the undo
  - **no merge commit** — the item was not accepted
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected with two specific, cheap defects: a dead `match_key()` with AC3's rule
  duplicated inline, and ordering tests that cannot tell insertion order from alphabetical order.
  All eight acceptance criteria are met and stay ticked; no criterion was edited. A hard gate
  failure caused by two EP-001 commits sitting on this branch was repaired rather than overridden,
  and reported upward as a methodology defect that will recur.

## 2026-08-21T03:11:39Z — implement v0.1.1 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, dispatched by `next`. The history's last row is a send-back
  from `in-review`, so per step 1 `artifacts/review.md` was read **first**: this execution's job is
  the two defects it names, not the item.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/review.md` — Findings 1–5 and `## What happens next`
  - `tracker/items/WI-0001/item.md` (criteria unchanged and still ticked; the new
    `## Accepted gaps` section), `history.md`, `artifacts/plan.md` step 4, `artifacts/impl-report.md`
  - `questions/Q-001.md`, `Q-002.md` — both still `answered`; nothing moved since the last entry,
    so step 2 required no re-reading of artifacts
  - `expenses/people.py`, `tests/test_cli.py`, and `docs/architecture/adr/ADR-0006` line 92
  - `tracker/project.yaml`
- **Decisions:**
  - **Wired `match_key` in rather than deleting it.** The review offered both. `plan.md` step 4
    names `match_key` as AC3's comparison key and specifies `add()` raising *"if `match_key`
    collides"*, so wiring it in is the plan as written; deleting it would leave WI-0002 — which
    must decide whether a sharer is a roster person, the same question — to re-derive the rule,
    which is the same duplication arriving one item later. `add()` now compares
    `match_key(existing) == match_key(stripped)`, so the rule exists once.
  - **Extended `match_key`'s docstring to say it is the single place the rule lives.** `ADR-0006`
    line 92 records `str.lower()` as knowingly not full Unicode case-folding, so this function is
    where someone will eventually go; the docstring tells them that changing it changes
    everything, which is only true now that `add()` routes through it.
  - **Chose `Alice, Zoe, Carol` for the ordering tests.** Not arbitrary: alphabetical order would
    give `Alice, Carol, Zoe`, so the assertion now fails under `sorted()`, which was the whole of
    Finding 2. Applied to both tests the review named, not just the one whose name mentions order.
  - **Added one test rather than none.** `test_matching_goes_through_one_key_function` asserts on
    `people.match_key` **directly** and then through the CLI. The direct assertion is deliberate:
    without it, `match_key` is referenced only by `add()`, and a future inline-it-again change
    would go unnoticed exactly as it did the first time.
  - **Confirmed both fixes by mutation before claiming them.** The first pass declared under
    `## What I did not do` that it had not done this, and the review found the consequence. Both
    mutations now go red; the transcript is in `impl-report.md`.
  - **Changed nothing else.** Findings 3–5 were not this skill's: 3 was repaired by
    `review-close`, 4 is a journal correction, 5 is an accepted gap now in `item.md`. The
    bare-invocation behaviour was deliberately left alone — it is an accepted gap, and changing it
    here is the "fixing things you noticed on the way" this skill is told not to do.
  - **No acceptance criterion was touched**, and none is edited by this pass.
- **Questions raised:** none. Both findings were specific enough to act on; neither needed a
  decision that was not mine.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 19 tests in 3.354s`, `OK`
  - mutation run 1 — `listing()` returns `sorted(...)` → **red**:
    `test_listing_prints_one_bare_name_per_line_in_insertion_order`,
    `test_the_roster_survives_into_a_fresh_process`
  - mutation run 2 — `if existing == stripped` instead of comparing `match_key`s → **red**:
    `test_a_duplicate_is_refused_however_it_is_spelled`,
    `test_matching_goes_through_one_key_function`
  - tree restored, suite re-run → exit 0, 19 tests, `OK`
  - `git commit` → `fix: route the duplicate check through match_key and make the ordering tests
    assert order (refs WI-0001)`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0,
    `all 6 commit(s) on main..wi/WI-0001 name WI-0001`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:** run on the branch head, after the last change.
  - `tests-pass` → **pass** (exit 0, 19 tests).
  - `lint-clean` → **skipped, not passed**. `commands.lint` is null by `ADR-0001` §4. Worth saying
    plainly rather than as boilerplate: Finding 1 was a dead function, which is the first thing a
    linter reports, and this project has none. `review-close` recorded that in `item.md`
    `## Accepted gaps`.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `every-criterion-has-a-test` → **pass**. The first pass's AC→test mapping is unchanged and
    still complete; AC1 and AC2 now have data that can actually fail, which is what the review
    said was missing.
  - `commits-reference-the-item` → **pass** (exit 0, 6 of 6).
- **Artifacts:**
  - `expenses/people.py` — `add()` compares through `match_key`; `match_key`'s docstring records
    that it is the single home of the rule
  - `tests/test_cli.py` — both ordering tests re-datad to `Alice, Zoe, Carol`;
    `test_matching_goes_through_one_key_function` added
  - `tracker/items/WI-0001/artifacts/impl-report.md` — a `## Second pass` section; the first
    pass's text left as written, with the one now-false statement marked superseded in place
  - commit `fix: route the duplicate check through match_key …` on `wi/WI-0001`
- **Status:** `in-progress` → `verifying`
- **Result:** Both review findings fixed and both confirmed by mutation rather than asserted. 19
  tests green. AC1–AC8 unchanged and untouched; whether their ticks still stand against this
  commit is `verify`'s call, not this skill's.

## 2026-08-21T03:19:49Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next` (selection key: priority-rank 1, the only
  critical item; WI-0002 and WI-0003 rank 2)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eight acceptance criteria, read **first and in full**,
    before any implementation artifact, so that what settles each criterion was derived from the
    criterion
  - this item's transition history — the reject/fix loop this pass follows
  - `tracker/items/WI-0001/artifacts/plan.md` — steps 3–7 and the AC mapping, to read the diff
    against
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read **after** the criteria and after the
    evidence was gathered; used to find claims to check, not as evidence for any of them
  - `tracker/items/WI-0001/artifacts/review.md` (Findings 1 and 2) — what the fix was supposed to do
  - `docs/architecture/adr/ADR-0002-one-store-file-per-user.md` (decisions 1, 2, 6, 7) and
    `ADR-0006` (rules 3–5)
  - `tracker/project.yaml` — the gate commands
  - the code at branch head `f994258bafd98f8e886a6b8f827c305a53739fc4` on `wi/WI-0001`
- **Decisions:**
  - **Re-derived all eight criteria from scratch rather than re-checking only the two the review
    touched.** The commit under verification is not the one the first pass verified, and a
    criterion ticked against an older commit is a claim about that commit. This costs a second
    full sweep and is the only thing that makes `Verified-commit: f994258` mean anything.
  - **AC8's "one-line" clause: judged `pass`, on the record, not on taste.** Four failure paths
    are argparse's and print `usage:` plus the error — two lines. `plan.md` step 5 chose
    argparse's native output for exactly those invocations ("do not re-implement it"), and AC8's
    stated purpose — no traceback, named failure on stderr, non-zero exit — holds for all four.
    Recorded as a judgement in `verify-report.md` `## A note on AC8's "one-line"` so that anyone
    who disagrees can find it, with the one-line fix named as an option rather than made.
  - **No question filed.** AC8's clause was the only candidate for `ambiguous`, and the record
    settled it. Filing a question the plan already answers would have cost a round trip for
    nothing.
  - **No send-back and no bug item.** No criterion of this item failed. WI-0001 is EP-001's first
    item, so there is no other delivered behaviour a defect could belong to.
  - **Closed two declared gaps instead of re-declaring them.** The previous pass could not run the
    two default store-path branches without writing to the machine's real store; setting
    `XDG_DATA_HOME` and `HOME` into the git-ignored `.harness/` directory runs both safely, and
    both match `ADR-0002` decisions 1–2. Same for `store.load()`'s undecodable-bytes branch,
    which was live but untested code. The `item.md` `## Accepted gaps` bullet claiming the
    default-path branches "have never been executed" is now false; it belongs to `review-close`,
    so it is flagged in `verify-report.md` `## Gaps closed by this pass` rather than edited here.
  - **Two plan deviations recorded, neither raised as a defect:** `people.add()` returns the
    stored spelling where `plan.md` step 4 declares `-> None` (the alternative would put a name
    rule in two places, which is what Finding 1 was about); and `plan.md`'s AC mapping still
    cites `"Alice\nBob\n"` where the tests now use `Alice/Zoe/Carol`. The code is right and the
    plan's demonstration column is stale — noted so nobody later "fixes" the tests back.
- **Questions raised:** none
- **Commands:** every one run by this skill against the branch head. Exit statuses as observed.
  - `git rev-parse HEAD` → `f994258bafd98f8e886a6b8f827c305a53739fc4`, exit 0
  - `git status --short` → empty (clean tree) before and after the mutation sweep
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 19 tests`, `OK`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - **AC1** `python3 -m expenses --help` → exit 0, both subcommands listed; `add-person Zoe`,
    `add-person alice`, `add-person Carol` → exit 0 each; `python3 -m expenses people | cat -A` →
    `Zoe$ alice$ Carol$`, exit 0
  - **AC2** `python3 -m expenses people` in a fourth process → same three names, same order,
    exit 0; `cat store.json` → `"people": ["Zoe","alice","Carol"]`
  - **AC3** `add-person Zoe`, `add-person ALICE`, `add-person "  Alice  "` → exit 2 each, each
    naming the stored spelling; `people` and `sha256sum` after → unchanged
  - **AC4** `people` against an empty store and against a missing store → `Nobody in the group
    yet.`, exit 0; re-run with `2>/dev/null` → still printed, so it is on stdout
  - **AC5** `people` then `add-person Bob` against `.harness/vs3/deep/nested/store.json` with no
    ancestor directories → exit 0, 0; `ls -d` after the read → `No such file or directory`;
    `find` after the write → all three directories and the file; fresh `people` → `Bob`
  - **AC6** four damage modes × two commands, each with `sha256sum` before and after: non-JSON,
    `[1,2,3]`, `people` not a list, and `chmod 000` → exit 2 in all eight, every hash identical,
    `ls -a` showing no leftover `.store-*.tmp`; `id -u` → 1000, so the permission denial is real
  - **AC6 (extra)** a store of `\xff\xfe\x00\x01not utf8` → `it is not valid UTF-8 text (…)`,
    exit 2 from both commands, bytes unchanged — previously untested code
  - **AC7** `add-person ""`, `add-person "   "`, `add-person $'\t '`, `add-person` with no
    argument → exit 2 each; store hash identical before and after all four
  - **AC8** a sweep capturing stdout, stderr and exit status separately for 8 failing and 2
    succeeding invocations → every failure exit 2 with empty stdout, non-empty stderr and no
    `Traceback` in either stream; every success exit 0 with non-empty stdout and empty stderr
  - **default paths** `env -u EXPENSES_STORE XDG_DATA_HOME=…` → store at
    `<scratch>/expenses/store.json`; `env -u EXPENSES_STORE -u XDG_DATA_HOME HOME=…` → store at
    `<scratch>/.local/share/expenses/store.json`; `EXPENSES_STORE=""` → falls through to the
    default. All exit 0
  - **sensitivity sweep** nine mutations, each applied to a backed-up working copy, the named test
    run, the source restored: AC1 `listing → sorted` → FAILED(1); AC2 `save` no-op → FAILED(1);
    AC3 `match_key` stops lowercasing → FAILED(3) and FAILED(1) on the key-function test; AC4
    empty-group message removed → FAILED(1); AC5 `mkdir(parents=True)` removed → ERRORS(1); AC6
    JSON-parse error → `return empty()` → FAILED(2); AC7 empty-name rejection removed →
    FAILED(3); AC8 the single `except ExpensesError` removed → FAILED(4). All exit 1. Tree
    restored, `git status --short` empty, full suite re-run → exit 0, `OK`
  - `git show --stat 9eb3cc1` and `git show 9eb3cc1 -- expenses/ tests/` → the two review findings
    and nothing else
  - `date -u` → the timestamps in this entry, read from the clock rather than estimated
- **Gates:** all six, by name.
  - `tests-pass` → **pass** (exit 0, 19 tests, run by this skill on the branch head).
  - `lint-clean` → **skipped, not passed**. `commands.lint` is null by `ADR-0001` §4. What that
    leaves unchecked is in `verify-report.md` `## Not verified, and why`.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `every-criterion-independently-checked` → **pass**. Each of the eight rows in
    `verify-report.md` `## Criteria` names a command this skill ran and quotes its real output;
    no row cites `impl-report.md`.
  - `negative-cases-exercised` → **pass**. Seventeen error, empty-input and boundary conditions
    triggered, enumerated in `verify-report.md`.
  - `tests-would-fail-without-the-change` (advisory) → **pass**, for all eight criteria. **This is
    the gate that failed in the first pass, for AC1 and AC2.** With the old `Alice/Bob` data the
    AC1 mutation would have left the test green; with `Alice/Zoe/Carol` it turns it red. The
    review finding is closed by evidence, not by assertion.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — rewritten for this commit, carrying
    `Verified-commit: f994258bafd98f8e886a6b8f827c305a53739fc4`
  - `tracker/items/WI-0001/item.md` — AC1–AC8 remain ticked; every tick now rests on a command in
    this entry rather than on the first pass's
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** All eight criteria pass on `f994258`, with evidence gathered by this skill. Both
  review findings confirmed fixed by mutation. Three previously-unverified behaviours — the two
  default store-path branches and the undecodable-bytes branch — now executed. One item-level
  `## Accepted gaps` bullet is stale as a result and is flagged for `review-close`.

## 2026-08-21T03:25:45Z — review-close v0.1.2 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` (priority-rank 1, the only critical item)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — all eight criteria, `## Accepted gaps`,
    `## Deliberately unconstrained`
  - this item's transition record — eleven rows, read for gaps and for the last row against
    `item.md`'s status
  - `tracker/items/WI-0001/journal.md` — **all ten entries, in full**, not skimmed; certifying the
    record is complete is half of what this skill signs off
  - `tracker/items/WI-0001/artifacts/plan.md` (steps 1–8, the AC mapping, the four assumptions),
    `impl-report.md` (both passes, including `## What I did not do`), `verify-report.md` (second
    verification, including `## Not verified, and why`)
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered`, `## Consequences`
    checked against the files they name
  - `docs/architecture/adr/ADR-0001` §4–5, `ADR-0002` decisions 1, 2, 6, 7, `ADR-0006` rules 3–5
  - `docs/architecture/overview.md` v1 — read **against the code**, per D12, not recalled
  - **the diff**, `git diff main...wi/WI-0001` — 9 files, 440 lines added, nothing deleted, read
    hunk by hunk with every hunk mapped to a criterion or plan step (table in `review.md`)
- **Decisions:**
  - **Rejected the item.** Three findings force it; the mapped-hunk read found no unrequested
    scope, and the first review's two findings are confirmed fixed, so this is a new class of
    defect rather than a repeat.
  - **F1 — a Python traceback reaches the user — is a send-back, not a bug item and not an
    accepted gap.** `store.load()` checks that `people` is a *list* but never what is in it, so
    `{"version":1,"people":[123],"expenses":[]}` passes the shape check and
    `people.normalise()` then raises `AttributeError`, which `cli.main`'s `except ExpensesError`
    does not catch. Exit 1, traceback on stderr. AC8 forbids this without qualification, and the
    skill's own test for routing — *does a criterion of this item say the behaviour should be
    different?* — answers yes, so it is this item's to fix. It also misses both halves of
    `ADR-0002` decision 6: the write path exits 1 with no path named, and the **read** path exits
    **0** and prints `123` as a member of the group.
  - **Did not file a question about the ADR conflict, deliberately.** The escalation clause is for
    a change that departs from an ADR and might be right, leaving the architect to weigh
    superseding. Here `ADR-0002` decision 6 is plainly correct and the code plainly falls short of
    it; there is nothing to weigh, and a question would spend a round trip to be told what the ADR
    already says. Recorded as a finding instead, with the reasoning, so the call is visible.
  - **F2 — an error blaming the typed name for a stored one — is also a send-back**, and it was
    **introduced by this skill's own previous Finding 1**. Routing `add()` through `match_key()`
    was right, and it brought `normalise()`'s *validation* along with the *comparison*, so every
    stored name is re-validated on every add. A store holding a control-character name makes
    `add-person Carol` fail with `a name cannot contain control characters (found '\x07')`.
    Recording that the earlier instruction created this is the point of having a review record.
    Not accepted as a gap because `match_key`'s docstring designates it the shared key for
    WI-0002's sharer matching — one line now, three call sites later.
  - **F3 — `overview.md` states something false — is part of the same send-back.** Its `cli`
    bullet claims the no-traceback property is *"a property of one function rather than a
    discipline applied everywhere"*. F1 is the counter-example: the property depends on every
    module below `cli` raising only `ExpensesError`, which is the discipline, and `store.load()`
    breaks it. The same sentence is echoed in `errors.py` and `plan.md`, which is the spreading
    D12 exists to catch, so all three need re-reading when F1 is fixed.
  - **F4 — `cli.main`'s unused `out`/`err` parameters — accepted, and written into `item.md`.**
    Inert and cheap, and stream injection is reasonable for a CLI entry point. Recorded rather
    than actioned because it is the *second* instance in this item of flexibility no gate catches,
    after the dead `match_key()`, on a project with no linter. An accepted gap left only in a
    review report is forgotten the moment the item closes.
  - **Unticked AC8 in `item.md`.** Nothing in the spec says who may clear a tick. Leaving it
    ticked while rejecting *for an AC8 failure* would put a false statement in the item, and a
    tick is the one thing this skill relies on to close. This is not "editing a criterion to make
    something pass" — the wording is untouched and the edit makes the item fail where it claimed
    to pass. Flagged as a methodology gap in `review.md`.
  - **Struck the stale `## Accepted gaps` bullet** claiming the two default store-path branches had
    never been executed. The second verification ran both and flagged the bullet rather than
    editing a section belonging to this skill, which was the right call. A closed gap left on the
    record is as misleading as an unrecorded one.
  - **Ran no trial merge and attempted no merge.** Steps 8–10 are for an accepted change; a
    rejected one must not be measured against the trunk. The branch is left intact.
  - **Did not close the epic.** EP-001 has three children and none is `done`.
- **Questions raised:** none
- **Commands:**
  - `git diff main...wi/WI-0001 --stat -- expenses/ tests/` → 9 files, 440 insertions, 0 deletions
  - `git diff main...wi/WI-0001` → read in full, hunk by hunk
  - `git log --oneline main..wi/WI-0001` → 8 commits
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0,
    `all 8 commit(s) on main..wi/WI-0001 name WI-0001`
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0,
    `verified at f994258b; wi/WI-0001 has moved to 847d0f9c but only the record changed (5 file(s)
    under tracker/ or docs/), so the verification still covers the code`
  - `python3 -m unittest discover -s tests -t .` → exit 0, 19 tests, `OK`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `grep -rn "main(" expenses/ tests/` → only `__main__.py:5: sys.exit(main())`; nothing passes
    `out` or `err` (F4)
  - **F1 probe**, a script run by this skill: a store of `{"version":1,"people":[123],...}` →
    `people` exit 0 printing `123`; `add-person Carol` exit **1** with
    `AttributeError: 'int' object has no attribute 'strip'` and a traceback on stderr. Repeated
    for `[{"name":"Alice"}]` and `[["Alice"]]` → same. `[None]` → exit 2, no traceback
  - **F2 probe**: a store holding a name containing `\x07` → `people` exit 0 listing it;
    `add-person Carol` exit 2, `a name cannot contain control characters (found '\x07')`, store
    bytes unchanged. The same input against the pre-fix `add()` from `0310dc7` → accepted, roster
    updated — confirming the previous fix introduced it
  - `date -u` → the timestamp on this entry, read from the clock
- **Gates:** all six, by name.
  - `definition-of-done` → **fail**. D1–D12 recorded individually in `review.md`
    `## Definition of Done`: nine pass, **three fail** — D1 (AC8 unticked), D7 and D12
    (`overview.md` contradicted by the code) — and D9 not reached, the item being rejected.
  - `verification-postdates-the-code` (D10) → **pass**, by running `check-verify-freshness`
    rather than judging it by how the last commit looked.
  - `commits-reference-the-item` → **pass** (exit 0, 8 of 8). No branch-topology repair was needed
    this time; the epic-level commits that caused it last turn now sit on `main`.
  - `tests-pass-on-the-merge-result` → the transition script reported **PASS**, and that report is
    weaker than its name. What `run-gate` actually executed is
    `python3 -m unittest discover -s tests -t .` in the working tree — the branch head, not a
    merge result. **This skill ran no trial merge**, because a rejected change must not be
    measured against the trunk. So: the tests pass on the branch (19, exit 0); whether they pass
    after merging is untested and this gate did not test it. Recorded honestly rather than
    accepted at face value, and reported as a toolkit finding — the gate's name promises
    something its command cannot deliver, and on an *accepted* item it would read as a trial
    merge that never happened.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `record-is-reconstructible` → **pass**. Eleven history rows chaining without a gap to
    `in-review`; ten journal entries, one per execution the history implies, in ascending time
    order; both questions `answered` with `## Consequences` naming files that exist; every commit
    naming the item. Using only the tracker, `docs/` and `git log`, what was built, who decided
    what, which questions arose and how they were answered, and what verification found are all
    answerable.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` — rewritten: what was examined, the hunk-to-
    criterion map, four findings, the D1–D12 table, the amended accepted gaps, and a
    `## For the next verification` handover
  - `tracker/items/WI-0001/item.md` — AC8 unticked; the stale default-store-path gap struck; F4
    added to `## Accepted gaps`
  - no merge commit, no epic closure, no bug items
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected. `implement` owns F1 (the AC8 traceback), F2 (the misattributed
  control-character error) and F3 (`overview.md`'s false claim, with `errors.py` and `plan.md` to
  re-read alongside it); F4 is recorded, not actioned. The findings are not a repeat — the first
  review's two are confirmed fixed — but F2 was created by the first review's own instruction,
  and the record says so.

## 2026-08-21T03:31:24Z — implement v0.1.1 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, dispatched by `next`. The last history row is a send-back
  from `in-review`, so `artifacts/review.md` was read **first** and defines the scope of this
  execution — F1, F2 and F3, not the whole item.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/review.md` — the four findings, their reproductions, the
    D1–D12 table, and `## For the next verification`
  - `tracker/items/WI-0001/item.md` — AC8 now unticked by the review; `## Accepted gaps` carrying
    F4
  - this item's transition record and `journal.md` — to reconcile with what is already on the
    branch rather than redo it
  - `tracker/items/WI-0001/artifacts/plan.md` steps 3–5 and its AC8 mapping;
    `artifacts/verify-report.md` `## Not verified, and why`
  - `docs/architecture/adr/ADR-0002` decision 6, `ADR-0001` §4, `ADR-0006` rules 4–5
  - `docs/architecture/overview.md` v1 — the `cli` and `store` bullets and the module diagram
  - `expenses/store.py`, `people.py`, `cli.py`, `errors.py`, `tests/test_cli.py`,
    `tests/test_store.py`, and `.claude/agile-skills/spec/doc-header.md` §2 for the version header
- **Reconciliation:** the branch `wi/WI-0001` already existed with ten commits and a clean tree,
  and the item was already at `in-progress` — `review-close` transitioned it on rejecting. Nothing
  was recreated. The first review's two fixes were checked as still present before anything new
  was written: `match_key` is still the single home of the comparison rule, and the ordering tests
  still use `Alice/Zoe/Carol`.
- **Decisions:**
  - **F1's check belongs in `store.load()`, not in `cli` or `people`.** `overview.md` says
    everything above the store sees a plain dictionary; that promise has to hold at the *element*
    level or a caller ends up re-checking what the store handed it. One check fixes both commands
    and every future caller.
  - **F2 fixed by splitting validation from comparison, not by adding a second key function.** A
    separate key for the stored side would recreate the first review's Finding 1 exactly — the
    rule written twice and drifting. `match_key` is now `name.strip().lower()`: one function, used
    on both sides, comparing without validating. Validation stays in `normalise`, on the input
    side, once.
  - **F3 was resolved in the code as well as the document, and that is the substantive half.**
    Correcting `overview.md` alone would have made the sentence true only until the next
    unanticipated exception. `cli.main` now has an `except Exception` backstop, so AC8 is a
    property of that function rather than of every module below it remembering to raise
    `ExpensesError`.
  - **The backstop was mine to add, and I checked that rather than assumed it.** The test for
    whether a user-visible decision belongs to this skill is whether an acceptance criterion
    covers it. AC8 covers it unconditionally and in this item, so no question was filed. It does
    deviate from `plan.md` step 5's literal "catching `ExpensesError` once", and that is declared
    in the implementation report rather than folded in quietly.
  - **The backstop reports rather than swallows**: exception type and message on the line, so the
    failure stays diagnosable without a traceback; `BaseException` deliberately not caught, so
    `KeyboardInterrupt` and `SystemExit` are unaffected.
  - **Removed "nothing was written" from the backstop's message before committing it.** An
    unexpected failure can land *after* `store.save()`, so the reassurance would have been false
    on exactly the path where it mattered — and shipping a claim the code cannot verify is the
    defect the review had just written up in `overview.md`.
  - **Did not edit `plan.md`**, which carries the third and last copy of F3's false claim. It is
    `plan`'s artifact and it recorded what was believed when it was written; rewriting another
    skill's record to match a later discovery would destroy the evidence of how the mistake
    propagated. Flagged in `## What I did not do, third pass` for `review-close` or `plan` to
    settle.
  - **Did not extend the element check to `expenses`.** The same latent crash exists there, but
    this item's commands never read that list and WI-0002 has not yet decided what an expense
    record is; inventing a schema here would pre-empt that item's plan. Handed over explicitly
    rather than left to be rediscovered.
  - **Did not touch F4.** The review accepted it and wrote it into `item.md`; acting on an
    accepted gap would put a change in this diff no finding asked for. The new backstop test does
    happen to drive `main`'s `out`/`err` parameters, which is a side effect, not a fix.
  - **Did not repair or reject a stored name today's rules would refuse.** Rejecting it on read is
    a stricter contract than `ADR-0002` decision 6 asks for; repairing it would edit a user's file
    unasked. The tool cannot create one, so it is reachable only by hand-editing.
- **Questions raised:** none. Every decision above is either covered by an existing criterion or
  is a *how* within the plan's latitude; none changes an interface another item depends on or
  contradicts an ADR.
- **Commands:**
  - `git rev-parse --abbrev-ref HEAD` → `wi/WI-0001`; `git status --short` → clean before starting
  - `python3 -m unittest discover -s tests -t .` → exit 0 after each change; final: `Ran 23 tests`,
    `OK` (was 19)
  - **sensitivity, each fix reverted in a backed-up copy and restored after:**
    F1 element check removed → `test_a_roster_entry_that_is_not_a_string_is_fatal`
    `FAILED (failures=1)` and `test_a_roster_entry_that_is_not_a_name_is_fatal_to_both_commands`
    `FAILED (failures=6)`; `match_key` back to `normalise(name).lower()` →
    `test_a_stored_name_todays_rules_would_reject_does_not_blame_the_new_name` `FAILED (failures=1)`;
    catch-all removed → `test_an_unexpected_exception_is_reported_not_dumped` `FAILED (failures=1)`.
    All exit 1. Tree restored, `git status --short` on `expenses/ tests/` showing only the intended
    modifications, full suite re-run → exit 0
  - **the review's three reproductions re-run end to end:** `[123]`, `[{"name":"Alice"}]`,
    `[["Alice"]]`, `[None]` → **both** commands exit 2, no traceback, path and offending type on
    stderr, bytes unchanged; a store holding `Al\x07ice` → `add-person Carol` exit 0, `people`
    listing all three. Regression sweep of the ordinary paths — empty group, two adds, a
    case-differing duplicate, an empty name, a non-JSON store — all unchanged
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → **exit 1 twice** on the
    `overview.md` change log (`doc.changelog.version`, `doc.changelog.order`: rows must be newest
    first and the top row must match the frontmatter), then exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0,
    `all 10 commit(s) on main..wi/WI-0001 name WI-0001`
  - `git commit` → `fcf3cf4 fix: reject a roster entry that is not a name, stop match_key
    validating, and back cli.main with a catch-all (refs WI-0001)`
  - `date -u` → the timestamp on this entry, read from the clock
- **Gates:** run on the branch head `fcf3cf4`, after the last change.
  - `tests-pass` → **pass** (exit 0, 23 tests).
  - `lint-clean` → **skipped, not passed**. `commands.lint` is null by `ADR-0001` §4. Third
    execution running in the dark: the `# noqa: BLE001` on the new catch-all names a rule nothing
    in this project enforces, and it is there for the human reader only.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings), after the two change-log failures
    above were fixed rather than worked around.
  - `every-criterion-has-a-test` → **pass**. AC1–AC7 unchanged. AC8's coverage is materially
    stronger: previously nine failing invocations, all reached through argument parsing or
    `load()`'s own rejection; now also six junk element types × both commands through a store that
    *passes* `load()`, plus an arbitrary unexpected exception.
  - `commits-reference-the-item` → **pass** (exit 0, 10 of 10).
- **Artifacts:**
  - `expenses/store.py` — `load()` rejects a `people` entry that is not a `str`, naming the path
    and the type
  - `expenses/people.py` — `match_key` compares without validating; docstring records why the
    split exists
  - `expenses/cli.py` — the `except Exception` backstop behind the `ExpensesError` handler
  - `expenses/errors.py` — docstring corrected; it carried the same false claim as `overview.md`
  - `tests/test_cli.py`, `tests/test_store.py` — four tests, each confirmed sensitive
  - `docs/architecture/overview.md` — **v2**, with a change-log row: the `cli` bullet now names
    both handlers and which is load-bearing, the `store` bullet states the element-level promise,
    the diagram says what damage detection covers
  - `tracker/items/WI-0001/artifacts/impl-report.md` — `## Third pass` section; the second pass's
    AC8 row marked superseded in place rather than rewritten
  - commit `fcf3cf4` on `wi/WI-0001`
- **Status:** `in-progress` → `verifying`
- **Result:** F1, F2 and F3 fixed, each confirmed by reverting it and watching a test go red, and
  each re-checked end to end against the review's own reproduction. F4 left as the accepted gap it
  was recorded as. 23 tests green. Two handovers are declared rather than buried: `expenses` list
  elements are still unvalidated and belong to WI-0002, and `plan.md` still carries the last copy
  of the claim F3 corrected. AC8 was unticked by the review; whether it may be ticked again is
  `verify`'s call, and `review.md` `## For the next verification` names the input that has to be
  in the sweep.

## 2026-08-21T03:34:31Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next` (priority-rank 1, the only critical item)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eight criteria, read first and in full, with AC8
    unticked by `review-close`
  - `tracker/items/WI-0001/artifacts/review.md` — the four findings, their reproductions, and
    `## For the next verification`, which names the input class the previous sweep never reached
  - `tracker/items/WI-0001/artifacts/impl-report.md` `## Third pass` — read **after** the criteria
    and after the evidence was gathered; used to find claims to check, never as evidence
  - `tracker/items/WI-0001/artifacts/plan.md` steps 3–5 and its AC8 mapping; this item's
    transition record
  - `docs/architecture/adr/ADR-0002` decision 6, `ADR-0001` §4
  - the code at branch head `a273c4ee483b6d8bedab0aedd3e671ffc6f17d9c` (code as of `fcf3cf4`)
- **Decisions:**
  - **Re-derived all eight criteria against the new commit**, not just the three the review
    touched. A criterion ticked against an older commit is a claim about that commit, and this is
    the third distinct commit this item has been verified on.
  - **Re-ticked AC8.** It was cleared by `review-close` for a real failure, so restoring the tick
    needed evidence on the input that disproved it, not merely on the old sweep. The new sweep
    runs 28 cases including six junk element types × both commands through a store that *passes*
    `store.load()`, plus a forced `ZeroDivisionError` to exercise the backstop. All clean.
  - **Took the review's handover as a specification for this pass.**
    `review.md` `## For the next verification` named three things — feed a store that passes
    `load()` and breaks above it, re-run the AC8 sweep with that class, and check the read path as
    well as the write path against `ADR-0002` decision 6. All three were done, and the read path
    is the half that had been silently wrong (exit 0, printing `123` as a member of the group).
  - **No question filed and no defect found.** AC8's "one-line" clause was settled by `plan.md`
    step 5 in an earlier pass and nothing has changed it; the argparse paths still print
    `usage:` plus the error and still pass on that reading.
  - **Did not treat the declared `expenses`-list gap as a defect.** `impl-report.md` declares that
    F1's element check covers `people` only and hands the rest to WI-0002. No command in this item
    reads that list, so it is not verifiable here; recorded in `## Not verified, and why` so
    WI-0002 inherits it as a known task. The container type *is* checked — a store with
    `"expenses": 5` is rejected from both commands, which this pass confirmed.
  - **Did not act on `plan.md` still carrying the claim F3 corrected.** `impl-report.md` declares
    it deliberately and leaves it to `review-close` or `plan`. It is a record-accuracy question,
    this skill has no standing to edit either artifact, and it is flagged so it is not read as an
    oversight.
- **Questions raised:** none
- **Commands:** run by this skill against the branch head.
  - `git rev-parse HEAD` → `a273c4ee483b6d8bedab0aedd3e671ffc6f17d9c`
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 23 tests`, `OK` (before and after
    the mutation sweep)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - **AC1** `--help` → both subcommands; `add-person Zoe/alice/Carol` then `people | cat -A` →
    `Zoe$ alice$ Carol$`, exit 0
  - **AC2** `people` in a further process → same three names, same order, exit 0
  - **AC3** `add-person ALICE` and `add-person "  Alice  "` → exit 2 each,
    `alice is already in the group; nothing was added`; roster unchanged
  - **AC4** `people` against an empty store and against no store → `Nobody in the group yet.`,
    exit 0
  - **AC5** read against a missing store at a three-deep path → exit 0 and `ls -d` →
    `No such file or directory`; `add-person Bob` → exit 0, file and both parents created; fresh
    read → `Bob`
  - **AC6** four damage modes × both commands with `sha256sum` before and after — non-JSON,
    `[1,2,3]`, **`people` holding `123`**, undecodable bytes → all eight exit 2, no traceback,
    each naming the path and the fault, every hash identical
  - **AC7** `add-person ""`, `"   "`, and with no argument → exit 2 each
  - **AC8** a 28-case sweep, streams and exit captured separately: 23 failures → all non-zero,
    stdout empty, stderr non-empty, `Traceback` in neither stream; 5 successes → all exit 0,
    stdout non-empty, stderr empty. Backstop driver: `store.load` patched to raise
    `ZeroDivisionError` → `CODE 2`, `OUT ''`, `ERR 'an internal error in expenses
    (ZeroDivisionError: nobody planned this). This is a bug in the tool, not something you did
    wrong.'`
  - **the review's own reproductions**, re-run: F1's four junk types → both commands exit 2 with
    the named message and unchanged bytes; F2's control-character store → `add-person Carol`
    exit 0 and `people` listing all three
  - **sensitivity sweep** ten mutations, each reverted after: AC1 sorted listing; AC2 `save`
    no-op; AC3 `match_key` stops lowercasing; AC4 empty-group message removed; AC5 `mkdir`
    removed; AC6 parse error returns `empty()`; AC7 empty-name check removed; **F1 element check
    removed**; **F2 `match_key` validates again**; **F3 backstop removed**. All ten → exit 1. Tree
    restored, `git status --short` on `expenses/ tests/` empty, suite green
  - `date -u` → the timestamps here, read from the clock
- **Gates:** all six.
  - `tests-pass` → **pass** (exit 0, 23 tests).
  - `lint-clean` → **skipped, not passed** (`commands.lint` null, `ADR-0001` §4). Third
    consecutive pass in the dark, and the third finding of that class — `main`'s unused
    `out`/`err` — was again found by a person reading a diff, not by a tool.
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings).
  - `every-criterion-independently-checked` → **pass**. Eight rows, each naming a command this
    skill ran and quoting real output; none cites `impl-report.md`.
  - `negative-cases-exercised` → **pass**. 23 failing invocations across argument parsing, name
    rules, four store-damage modes, six junk element types and a forced internal exception.
  - `tests-would-fail-without-the-change` (advisory) → **pass**, ten of ten.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — rewritten for this commit, carrying
    `Verified-commit: a273c4ee483b6d8bedab0aedd3e671ffc6f17d9c`
  - `tracker/items/WI-0001/item.md` — **AC8 re-ticked**; AC1–AC7 remain ticked, each now resting
    on a command in this entry
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** All eight criteria pass on `a273c4e`. The review's three actionable findings are
  confirmed fixed by re-running its own reproductions, and each fix provably goes red when
  reverted. AC8's tick is earned again on the input that removed it. Two declared gaps are carried
  forward rather than closed: `expenses` list elements are unvalidated and belong to WI-0002, and
  `plan.md` still holds the last copy of the claim F3 corrected.

## 2026-08-21T03:39:41Z — review-close v0.1.2 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` (highest-ranked runnable item, priority
  `critical`; WI-0002 and WI-0003 rank below it at `high`, EP-001's `open` has no owner)
- **Inputs read:**
  - `item.md` — the eight criteria and all three prose sections
  - the item's transition record — thirteen rows, chain and timestamps checked
  - `journal.md` — all thirteen entries, end to end
  - `artifacts/plan.md` — steps 1–8, the AC mapping, the four assumptions
  - `artifacts/impl-report.md` — all three passes
  - `artifacts/verify-report.md` — the third verification, including `## Not verified, and why`
    in full
  - `questions/Q-001.md`, `questions/Q-002.md`
  - `docs/architecture/overview.md` (v2), `docs/architecture/adr/ADR-0001…`, `ADR-0002…`,
    `ADR-0006…` — read against the code, not remembered
  - `.claude/agile-skills/pipeline.yaml`, `.claude/agile-skills/spec/dor-dod.md`,
    `.claude/agile-skills/spec/journal-and-history.md`, `tracker/project.yaml`
  - the diff, `git diff main...wi/WI-0001`, hunk by hunk — 17 files, 10 of them code, docs or
    tests
- **Decisions:**
  - **Accept, after two rejections by this same skill.** What settled it was not that the reports
    say the fixes landed: the previous review's F1 was a *class* of input — a store that passes
    `store.load()` and breaks above it — and the fix moved the check into `store`, so it covers
    every caller at once. I went looking for more of that class myself (seven hand-written stores,
    both commands) and found no second instance, which is the evidence that mattered.
  - **F5, a hand-edited name today's rules would reject is listed verbatim — accepted, recorded.**
    A store holding `""` makes `people` print a blank line and one holding a newline prints across
    two, which is what `ADR-0006` decision 5 bans control characters to prevent. Accepted rather
    than sent back because the tool cannot create such a store, and both alternatives are worse
    than `ADR-0002` decision 6 asks for: rejecting on read makes a hand-edited store unusable, and
    repairing edits a user's file unasked. Written into `item.md`.
  - **F6, the `expenses` list's elements are unvalidated — recorded as a handover, not filed as a
    bug.** The reasoning is the bug Definition of Ready: RB3 wants an expected behaviour citing
    something it contradicts, and nothing yet says what an expense record is, so the bug would
    have to invent the schema WI-0002's plan owns. Recorded in `item.md` as an explicit obligation
    on WI-0002 instead.
  - **F7, AC8's "one-line message" against argparse's two-line failures — accepted, with the
    reading stated.** The reading applied: the message naming what was wrong is one line, and
    argparse's usage line precedes it as a hint. AC8's own sentence gives its purpose and all of
    it holds. The criterion was **not** edited — that is forbidden — and the tension is written
    into `item.md` so a stakeholder can ask for strictly one line if that is what they meant.
  - **F8, the catch-all backstop is a design decision in `overview.md` v2 rather than an ADR —
    D6 passes with a recorded caveat.** Sending back would produce nothing, because `implement`
    cannot write an ADR; filing a question would spend a round trip on a decision that blocks
    nobody. Recorded so a later `plan` can promote it.
  - **`plan.md`'s false paragraph: appended a `## Correction`, did not edit the paragraph.**
    `implement` handed this decision here by name. Rewriting it would destroy the evidence that
    the plan's central design idea was wrong — the most useful thing in this record for whoever
    plans WI-0002 — and a pointer in `item.md` alone sits one file away from the reader being
    misled, which is exactly the re-quote-rather-than-re-check failure D12 exists to catch. So:
    original text untouched, correction appended beneath, per the rule
    `spec/journal-and-history.md` gives for a wrong entry. **`plan.md` is not one of this skill's
    declared outputs**, so this is a deliberate step outside that list and is flagged here and in
    `review.md` rather than done quietly.
  - **Two carried gaps struck as closed rather than re-carried.** The default store-path branches
    (closed by the second verification) and the write path's `OSError` wrapper (closed by me, with
    a read-only parent directory). An accepted gap that has since been closed misleads as much as
    an unrecorded one.
  - **EP-001 stays open.** WI-0002 and WI-0003 are at `draft`, so DE1 fails on its face and the
    epic Definition of Done was not applied. Recorded rather than skipped silently, with two notes
    carried to whoever closes it: the no-linter decision is epic-level, and DE6 should re-read the
    fourth success measure against `cli.py` rather than against this report.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0,
    *"verified at a273c4ee; wi/WI-0001 has moved to 4b04b42a but only the record changed"*
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0,
    `all 12 commit(s) on main..wi/WI-0001 name WI-0001` — run before the merge, while the range
    is still non-empty
  - `git diff main...wi/WI-0001` → read hunk by hunk
  - `python3 -m unittest discover -s tests -t .` on the branch head → exit 0, `Ran 23 tests`, `OK`
  - `git worktree add --detach .harness/trial main` + `git merge --no-edit wi/WI-0001` → clean;
    `python3 -m unittest discover -s tests -t .` **on the merge result** → exit 0, `Ran 23 tests`,
    `OK`; `git worktree remove --force .harness/trial` → trial discarded
  - 20 CLI invocations against hand-written stores under `.harness/`, with `sha256sum` before and
    after each — the table is in `review.md` `## Behaviour I ran`
  - `chmod 500` on a store's parent directory, then `add-person Bob` → `cannot write …: Permission
    denied`, exit 2, no traceback
  - `git merge --no-ff wi/WI-0001` into `main` → after the close, not before
- **Gates:**
  - `definition-of-done` → **pass**. D1–D12 applied one by one, each with its own result and
    evidence, in `review.md` `## Definition of Done`. Eleven pass outright; D6 passes with the F8
    caveat recorded in `item.md`. None fails. A single verdict would not have satisfied this gate
    and the table is the evidence.
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness`, exit 0). Run, not
    assumed. The last code commit is `fcf3cf4`; `a273c4e` and `4b04b42` touch `tracker/` only.
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, 12 commits).
  - `tests-pass-on-the-merge-result` → **pass**. `Ran 23 tests … OK` on the trial merge of
    `wi/WI-0001` into a detached worktree at `main`, which is what the project actually gets.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors, 0 warnings).
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0001`
    alone: *what was built* — two commands and the store beneath them, `plan.md` steps 1–7;
    *why* — the story, and `ADR-0002`/`ADR-0006` for the two decisions that were not the
    stakeholder's; *which skill decided what* — thirteen transition rows and thirteen matching
    journal entries, `actor` on every row; *what questions arose* — `Q-001` and `Q-002`, both
    answered by the human, both with `## Consequences` naming criteria that carry the answers;
    *what verification found* — three verification reports' worth, and the two rejections that
    came between them, each with its findings and its fix. The one thing a reader would previously
    have got wrong is `plan.md`'s AC8 paragraph, and that is now corrected in place.
  - `lint-clean` is **not** a gate of this skill; the project has no linter (`ADR-0001` §4) and
    that is recorded as an accepted gap on the item rather than as a pass anywhere.
- **Artifacts:**
  - `artifacts/review.md` (rewritten for this, the third review)
  - `item.md` (`## Accepted gaps` extended with F5–F8 and the `plan.md` correction; two closed
    gaps struck; `status`, `outcome` and `updated` set by `transition`)
  - `artifacts/plan.md` (`## Correction` appended; nothing above it changed)
  - the merge commit of `wi/WI-0001` into `main`
  - EP-001 unchanged, deliberately — it stays `open`
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** Accepted at the third review. All eight acceptance criteria hold under commands I
  ran myself, twelve Definition of Done criteria are recorded one by one with eleven clean passes
  and one recorded caveat, the trial merge is green, and four declared gaps are decided and
  written into the item rather than left in a report. WI-0001 is merged and closed; EP-001 stays
  open with two siblings still at `draft`.
