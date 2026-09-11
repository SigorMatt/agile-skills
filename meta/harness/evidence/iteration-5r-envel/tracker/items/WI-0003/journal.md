# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T02:00:18Z — intake v0.5.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's stated idea; this skill is not dispatched on a status
- **Inputs read:**
  - `IDEA.md` — the stakeholder's statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty of items before this execution
- **Decisions:**
  - See `EP-001`'s entry of this execution for how the work was split and why. This item is the look-back: a summary of a month. It depends on both of the others, because a month with no income and no spending in it has nothing to summarise.
  - Its acceptance criteria are deliberately rough and some are explicit placeholders for answers not yet given; padding them into something that looked finished would have invented requirements the stakeholder never stated.
- **Questions raised:** none on this item; `EP-001/Q-001` through `EP-001/Q-006` were filed on the epic and several of them decide criteria here
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0003 --type work-item --title ... --epic EP-001` → exit 0, item created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`.claude/agile-skills/scripts/validate-workspace .` run after the whole execution; see `EP-001`'s entry)
  - `epic-has-success-measures` → **pass** (decided once for this execution against `EP-001`'s `## Success measures`; see `EP-001`'s entry)
  - `an-open-question-was-asked` → **pass** (`lint-answers --item EP-001 --require-elicitation` → exit 0)
  - `engagement-state-is-delimited` → **pass** (`lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md` → exit 0)
  - `items-are-separable` → **pass** (this item's place in the build order and what it depends on are stated under **Decisions:** above)
  - `no-solution-in-the-problem` → **pass** (the story and criteria name no technology the stakeholder did not; see `EP-001`'s entry for what was removed)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/journal.md`, `tracker/items/WI-0003/history.md` (new, by `new-item`)
- **Status:** — → `draft`
- **Result:** Created at `draft` by this intake execution. It is not Ready: `refine` is what makes each criterion decidable, and some of them wait on the stakeholder's answers to the questions on `EP-001`.

## 2026-09-11T03:40:05Z — refine v0.6.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` (step 4, which sits above the halt — the three open human questions on `WI-0002` do not stop another item being refined). WI-0002 rejected (three open blocking questions), WI-0004 and WI-0005 rejected on `created` at equal priority rank 3, WI-0006 on rank 4, WI-0001 and EP-001 on a null status owner
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — six criteria, `## Out of scope`, `## Notes` in full
  - `tracker/items/WI-0003/history.md` — **read first, and it decides the job**: one row, `— → draft` by `intake`. A fresh draft, not a send-back, so the whole story is open rather than one specific defect
  - `tracker/items/WI-0003/journal.md` — both entries, including what `answer-questions` propagated here from `EP-001/Q-003` and `EP-001/Q-004`
  - `tracker/items/WI-0003/artifacts/` — empty; no `refinement-qa.md` existed
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — all six answers verbatim, so as not to re-ask any of them
  - `tracker/items/WI-0002/item.md`, its `Q-001.md` and `Q-002.md` (answered) and `Q-003`, `Q-004`, `Q-005` (open) — what is already in front of the stakeholder this round
  - `tracker/items/WI-0001/item.md` — the delivered conventions this item inherits: AC3's ordering, AC13, AC16, AC17
  - `tracker/items/WI-0004/item.md`, `WI-0005/item.md`, `WI-0006/item.md` — whether a sibling already owns part of this scope
  - `docs/product/vision.md` — *"An envelope's balance carries over … the rule they said they would least want us to get wrong"*, and the four things in order
  - `.claude/agile-skills/spec/dor-dod.md` §1 — walked criterion by criterion
- **Decisions:**
  - **The stakeholder is not in this session, so this execution files rather than converses** (precondition 2). Three blocking questions addressed to `human`, the item suspended at `awaiting-answer` with `resume-to: draft`, and `refinement-qa.md` written with `status: agenda` — because no conversation has happened and R8 must not let an agenda carry the item to `ready`. Nothing in that file is tagged `[human]`.
  - **Recorded `depends-on: WI-0002`, which is the real R7 failure and the most consequential thing this round did.** There is no such thing as *"the money spent from it during that month"* until spending exists, and AC3's reconciliation cannot be demonstrated at all against a tool that only takes money in. `WI-0002` already depends on `WI-0001`, which is `done`, so naming `WI-0002` alone is enough. The consequence is deliberate and is written into `## Notes` rather than left to be discovered: the orchestrator dispatches nothing on an item whose `depends-on` is unfinished, so this item will not move again — not even to consume the three answers — until `WI-0002` is `done`. Leaving it unrecorded would have bought a little parallelism at the price of letting `plan` and `implement` be dispatched here against a tool that cannot record a spend, which is the worse failure and the same trade `WI-0002` round 1 made.
  - **Three questions, and each is product stake.** `Q-001` — do transfers count as money in and money out? `EP-001/Q-003` chose what the report shows *before* moving money existed as a thing the tool would do; they asked for that minutes later at `EP-001/Q-005` and called it something they would need *"the moment an envelope runs short"*. The answer changes what every number in the report means. `Q-002` — which envelopes get a row? *"One row per envelope"* does not say whether it ranges over the envelopes that exist now or the ones that existed then, and the difference is whether a past month's summary is a fixed document; they read a month *"a couple of days after it has ended"* against payslips and statements, which do not change afterwards. `Q-003` — can income be dated?
  - **`Q-003` was found by reading their answers against what is built, and it is the one nobody would have asked.** `envel add` is shipped and stamps income with the moment the command was typed, so this summary's first column is keyed to when they sat at the terminal. Their own justification for dating spends — *"a Saturday shop landing in the wrong month would make the monthly summary wrong"* [src: WI-0002/Q-001] — applies to a payslip word for word and by a larger amount, and at `EP-001/Q-004` they said calendar months matter precisely because *"calendar months are what my payslips and statements use."* It is asked rather than decided because the two honest answers cost very different things: one reopens a finished command, one accepts a limitation. Neither is ours. Where the work lands if they say yes is `answer-questions`' to route, not this round's.
  - **How a month is named was deliberately NOT asked**, though the item's own `## Notes` listed it as `refine`'s to ask. It is already open with the stakeholder in another form: `WI-0002/Q-003` asks whether an optional date is a named option or a plain word, and `WI-0002/Q-004` asks which date forms are accepted. A month is a date with the day taken off, so those two answers settle this, and asking again in the same round would put a near-duplicate in front of them — which is how a question protocol degrades into noise (F-023). Recorded with the condition under which it becomes a real question: if they pick a day-first short form, where `9/2026` and `2026/9` are both plausible, round 2 files it.
  - **Three things were decided rather than asked, each declared under no delegation** with where a disagreement lands: the subcommand is `summary`, on the same footing as `new`, `add`, `list` and `spend`; a month the tool cannot read is refused with a message and nothing printed, on the convention `WI-0001` AC13 and AC17 already deliver; a month in the future is summarised like any other and is simply empty, because there is nothing there to protect and AC4 already covers the empty case.
  - **Row ordering and the stream-and-exit-code rule were cited, not assumed.** Both are delivered conventions with the stakeholder's own criteria behind them [src: WI-0001 AC3 "the lines ordered alphabetically by name ignoring capitalisation"] [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits non-zero"], so round 2 writes them in by citation rather than restating them as new decisions. Message and column-heading *wording* stays deliberately unconstrained, as `WI-0001` left it.
  - **Three design questions were routed to `plan`**, not to a person, because the answer would be the same whoever the stakeholder was: how a month's figures are computed from the entry log, how the end-of-month balance is derived for a month that is not the current one, and what to do with an entry naming an envelope no longer present — which is the same question `WI-0002` routed to `plan` and should get the same answer.
  - **No acceptance criterion was rewritten, deliberately.** Five of the six are downstream of something pending: AC1 and AC5 on the command surface open at `WI-0002/Q-003` and `Q-004`, AC2 on `Q-001` and `Q-002`, AC3 on `Q-001` (if a transfer counts as money in, the reconciliation equation changes), AC4 on the command name. Only AC6 is unaffected, and rewriting one criterion alone is not worth renumbering for. Round 2 writes them once, from the answers.
  - **Checked the renumbering obligation** before deciding that: `grep -rn 'WI-0003 AC' tracker docs` → exit 1, no matches, so nothing outside this item cites its criteria by number. That is a reason to renumber carefully once rather than a licence to do it twice (F-094).
  - **Nothing was re-asked.** What the summary shows is `EP-001/Q-003`; the period is `EP-001/Q-004`; carry-over is `EP-001/Q-001`; whether descriptions appear is ruled out by `EP-001/Q-003`; what a correction does to a past summary is `EP-001/Q-005` and is a constraint on `WI-0005`, recorded in `## Notes` for `plan`.
- **Cross-answer check:** `none` — this execution consumed no human answer, so there is no reply to check against prior ones. Each question instead carries its own `## Cross-answer check` written at filing time, naming the prior answers the reply must coexist with: `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`, `WI-0001/Q-002`, `WI-0002/Q-001`. `Q-003`'s is the one to watch — `WI-0002/Q-001` is an answer about **spending** and is deliberately not read as covering income, because stretching it would answer `Q-003` on their behalf; a "no" there is a decision about income, not a reversal, and must be recorded as one (ADR-0008).
- **Questions raised:** `WI-0003/Q-001`, `WI-0003/Q-002`, `WI-0003/Q-003` — all blocking, all addressed to `human`, all open, recorded in `artifacts/refinement-qa.md`. None `[unresolved]`: none has been asked twice.
- **Commands:**
  - `grep -rn 'WI-0003 AC' tracker docs` → exit 1, no matches
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 0 consumed human answers, 0 delegations spent
  - `.claude/agile-skills/scripts/board-gen .` → exit 0, board rewritten
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 on an intermediate run, with exactly the one error this move resolves: `question.blocking.not-suspended` on an item still at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition against the state the move produces; the intermediate `question.blocking.not-suspended` is what this move exists to resolve)
  - `definition-of-ready` → **fail** (criterion by criterion: R1 pass — frontmatter complete, `type`, `epic` and `priority` set, and `depends-on` now too; R2 pass — role *"a person budgeting my own money at a terminal"*, capability *"a simple summary of a month"*, outcome *"so that I can look back at what came in and what went out"*; R3 pass — AC1–AC6, labelled, checkboxes; **R4 fail** — AC1 names no command and no way to name a month, AC5 says a month can be named without saying how, AC2 says *"one row per envelope"* without saying which envelopes and gives its three figures no treatment of a transfer, AC4 names neither stream nor exit code. AC3 is decidable as written, because it carries a worked example — 50.00 carried in, 0.00 added, 20.00 spent, 30.00 left — and AC6 is decidable; R5 pass — `## Out of scope` names non-month periods, the total line and the individual spends, charts, and comparison between months; **R6 fail by design** — this execution filed three blocking questions, which is what suspends the item; **R7 fail, and fixed here** — the dependency on `WI-0002` was real and unrecorded, and is now in `depends-on` with the item sequenced after it; **R8 fail** — `refinement-qa.md` declares `status: agenda`, honestly, because no conversation has happened; R9 pass — one coherent change, print one month's figures; **R10 fail** — of four unstated combinations, two are asked (`Q-001` a transfer, `Q-002` an envelope with no activity) and two are decided here (an unreadable month, a future month). Visible by R10's own standard, not yet stated in a criterion; R11 pass — no criterion counts anything, and AC3 states a worked example rather than a count; R12 pass — three `[assumed]` entries in `refinement-qa.md`, every one declaring **no delegation** and where a disagreement lands, and the two delivered conventions recorded as citations rather than as assumptions at all)
  - `criteria-are-decidable` → **fail** (AC3 — fund an envelope with 50.00 in a prior month, spend 20.00 in this one, read the row and check it says in 0.00, spent 20.00, left 30.00: decidable today, from its own worked example. AC6 — read the output and check for a total line and for any individual spend: decidable. **AC1 is not decidable**: no command to run. **AC5 is not**: no way to name a month. **AC2 is not**: *"one row per envelope"* does not say which envelopes, and the three figures have no stated treatment of a transfer. **AC4 is not**: no command whose output to read, and neither stream nor exit code named. Those four are `Q-001`, `Q-002`, `Q-003` and the command surface pending at `WI-0002/Q-003` and `Q-004`)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` → exit 0 over 0 consumed human answers and 0 delegations spent — nothing has been consumed on this item, so there was nothing to check against. The three questions filed carry a `## Cross-answer check` written at filing time, naming seven prior answers by ID)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` holds the DoR walk, the three questions with why each is theirs, what was deliberately not asked and why, the four things decided here with the authority each was taken under, what was routed to `plan`, and `## What round 1 has not settled`. Nothing is tagged `[human]`, because no human has said anything on this item; the three `[assumed]` entries each carry their **Under no delegation** line)
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (new) — blocking, to `human`, each with `## Context`, `## Question`, `## Options considered` with the recommendation last and marked as ours, `## Answer`, `## Cross-answer check` and `## Consequences`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0003/item.md` — `depends-on: WI-0002` added; `## Notes` rewritten. No criterion touched
  - `tracker/board.md` (regenerated)
  - no question filed on any other item; `docs/` unchanged; no ADR; no item created
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0003` is not Ready, and R4, R6, R7, R8 and R10 say why. R7 was fixed here — the dependency on `WI-0002` was real, unrecorded, and is the reason this item cannot be built yet. Three questions went to the stakeholder as one ask about what the three numbers in a row mean, and one of them, `Q-003`, is a gap nobody had noticed: a spend can be dated and income cannot, so the summary's first column is keyed to when they typed rather than when they were paid. Four further points were decided here rather than spent on their attention, each under no licence, and how a month is named was left unasked because it is already in front of them in another form. No criterion was rewritten; round 2 writes them once.

## 2026-09-11T03:52:07Z — answer-questions v0.6.3 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer` with three human-addressed questions whose `## Answer`
  sections had been filled in between turns; consumed before `next` was run, because an
  answered-but-unconsumed human question halts the orchestrator.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three, with the
    prospective cross-answer lists `refine` filed alongside them
  - `tracker/items/WI-0003/item.md` (AC1–AC6 as `intake` and round 1 left them, and `## Notes`)
  - `tracker/items/WI-0003/history.md` — the suspending row of 2026-09-11T03:40:05Z, whose
    `resume-to` is `draft`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (`status: agenda`, round 1)
  - `tracker/items/WI-0002/item.md` — AC9, cited from the new AC8, and `Q-003`/`Q-004`'s answers,
    which are what round 1 said AC1 and AC5 were waiting on
  - `tracker/items/WI-0001/item.md` — AC3 and AC16, the delivered conventions round 1 cited
  - `docs/architecture/overview.md` (v2) and `docs/product/vision.md` (v1)
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` — checked for a recorded decision any of the
    three answers would contradict. `ADR-0002` is the closest: the store is an append-only entry
    log and a balance is the sum of an envelope's entries, which is what makes AC7's carried-over
    balance for a past month computable at all. Nothing is contradicted.
  - no `plan.md`: this item has never been planned
- **Decisions:**
  - `Q-001` answered **from the human's reply**, option C: a move is excluded from *spent* and
    shown as a fourth figure. Propagated into AC2 (four figures), AC3 (the reconciliation, with a
    worked example whose numbers add up) and AC6. AC6 had to change or it would have contradicted
    AC2 in the same list — it said *"the three columns of AC2 and nothing else"*.
  - `Q-002` answered **from the human's reply**, option C: every envelope that existed by the end
    of the month, zeros for untouched ones. Written as a new AC7. AC4 was rewritten as a
    consequence: with zero rows for untouched envelopes, *"a month in which nothing was recorded"*
    is no longer the empty case, and the honest empty case is a month that ended before any
    envelope existed.
  - `Q-003` answered **from the human's reply**, option B: income stays dated when it is typed.
    Written as a new AC8, which states the rule and names the asymmetry with a spend as their
    decision. **No item was filed under step 3b**: A and C would each have implied new work on the
    delivered `envel add`, and B declines both, so filing work would have put something on the
    board they had just refused. Step 3b is for an answer that widens scope; this one narrows it.
  - The limitation B carries — income entered late lands in the month it was typed, with no way to
    correct it, since `WI-0005` is scoped to spends — is recorded in AC8 and in `## Notes` as
    chosen rather than overlooked, with their own sentence about what they would do if it bites.
    Rationale: without that, the first person to find a payslip in the wrong month reads working
    behaviour as a defect and files a bug against a decision the stakeholder made.
  - Decided, not asked: `Q-001`'s option C said *"moved in or out"* without saying whether that is
    one figure or two. One net figure, `[assumed]` under no delegation. Two would be a fifth
    column on a report they have twice asked to stay small, and net is what lets AC3's row
    reconcile in a single expression. Recorded in AC2 and in `## Notes`; a disagreement costs one
    column.
  - The criteria were amended here rather than left to `refine` round 2, which had reserved the
    rewrite. Round 1's reason for deferring was renumbering, and it does not arise: AC2, AC3, AC4
    and AC6 were amended **in place** and AC7 and AC8 **appended**, so no criterion moved. The
    reason not to wait is specific to this item — `depends-on: WI-0002` means the orchestrator
    dispatches nothing here until `WI-0002` is `done`, which is several items away, so an answer
    left in a question file would have sat unpropagated for all of it while `item.md` went on
    telling every reader the summary has three columns.
  - **Not** written, deliberately: AC1 and AC5's command surface. Round 1 left them waiting on
    `WI-0002/Q-003` and `WI-0002/Q-004`, which are now answered, and `## Notes` says so — but
    deriving what is typed to get a summary, and how a month is named, from answers given about a
    different item is refinement's judgement taken in the open, not a propagation of anything
    asked here. Round 2 writes them or files its own question.
  - Nothing was written into `docs/`. What a month's summary shows is `WI-0003`'s to decide and
    `docs/architecture/overview.md` `## What is not decided yet` already says so; it reaches a
    document when `plan` writes one.
  - Observed and deliberately not acted on, for the second execution running: the same
    `## Engagement state` sentence in `docs/architecture/overview.md` — *"Nothing has been
    implemented, verified or accepted in this engagement"* — is false since `WI-0001` closed. No
    answer consumed here falsified it, the section belongs to the ending (`spec/doc-header.md`
    §4a), and this execution neither repaired it nor claimed it as a consequence.
- **Cross-answer check:** eleven verdicts across the three answers, all `compatible`, no conflict,
  so no question was filed under ADR-0008 §3.
  - `Q-001` checked against `EP-001/Q-003` (**compatible** — the answer adds a column to a report
    they asked to be small, and they reconciled that themselves after the question named it:
    *"A column of zeros costs me nothing; a number I can't account for costs me an evening."*
    What `EP-001/Q-003` ruled out — a total line, individual spends — is untouched in AC6),
    `EP-001/Q-005` (**compatible** — moving money is routine, which is why the column is ordinary),
    `EP-001/Q-002` (**compatible** — a refused overspend is what produces the moves), `EP-001/Q-001`
    (**compatible** — the last column stays a carried-over balance).
  - `Q-002` checked against `EP-001/Q-003` (**compatible** — *"one row per envelope"* is what the
    answer reads, not what it departs from), `EP-001/Q-001` (**compatible**, and the reason C beats
    B — an untouched envelope is the rollover case), `EP-001/Q-004` (**compatible**, and quoted back
    by them as the deciding reason).
  - `Q-003` checked against `WI-0002/Q-001` (**compatible** — that answer is about spending and is
    deliberately not read as covering income; the question said in advance that B here would be a
    decision about income rather than a reversal, and it is), `EP-001/Q-004` (**compatible**, and
    where the cost sits — payslips are income, and they accepted option B's stated cost),
    `EP-001/Q-005` (**compatible** — `WI-0005` is scoped to spends, which is what makes the
    limitation unrepairable and therefore worth a criterion), `WI-0001/Q-002` (**compatible** —
    amount formatting is untouched).
- **Questions raised:** none — all three replies were answerable as given, and no cross-answer
  check returned `conflicts`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0 (3 consumed human
    answers, 0 errors)
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0003 --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 on `board.stale` and
    `question.awaiting.none-open` only, both of which this transition and `board-gen` clear
- **Gates:**
  - `answer-is-propagated` → **pass** (each of the three `## Consequences` sections names `item.md`, `item.md` `## Notes` and `refinement-qa.md`; each file was reopened after writing and the change is there — AC2/AC3/AC4/AC6 rewritten, AC7 and AC8 added, `## Answers — round 1` written with all three replies verbatim, `status` moved `agenda` → `recorded`)
  - `answered-from-the-record` → **pass** (all three follow from the stakeholder's own replies, quoted verbatim in the question files and again in `refinement-qa.md`; the one thing decided rather than read — the net moved figure — is tagged `[assumed]` under no delegation in AC2 and `## Notes`, and needed no ADR because it is one column on one item rather than a project-wide decision)
  - `escalation-is-justified` → **skipped** (no question was re-addressed to the human, so there is no escalation to justify)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0003 --uncommitted`, exit 0; 0 sentences written into `docs/`, because this execution wrote none)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted`, exit 0; the stale sentence found is recorded under **Decisions** and left to the ending)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0; three new `## Cross-answer check` sections, eleven verdicts, all `compatible`, no conflict to escalate)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0 once this transition cleared `question.awaiting.none-open`)
  - `item-resumed-correctly` → **pass** (`resume-to` on the 2026-09-11T03:40:05Z row is `draft`; this execution moved the item to `draft`)
  - `a-deferral-is-not-an-answer` → **pass** (no reply deferred; all three chose a lettered option and gave a reason for it. `Q-003`'s B is a refusal of work, not a deferral of a decision — they decided, and said what would make them revisit it)
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — `answered`, cross-answer check and consequences
    written
  - `tracker/items/WI-0003/questions/Q-002.md` — same
  - `tracker/items/WI-0003/questions/Q-003.md` — same, and it records that no item was filed and
    why
  - `tracker/items/WI-0003/item.md` — AC2, AC3, AC4, AC6 amended; AC7 and AC8 added; `## Notes`
    extended with the three answers, the accepted limitation on income dating, the net-figure
    assumption, why the criteria were written here, and what round 2 still owes
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; round-1
    question rows `open` → `answered`; `## Answers — round 1`, `## Cross-answer check — round 1,
    on the replies` and `## What round 1's answers left for round 2` added
  - commit of the above, refs `WI-0003`
- **Status:** `awaiting-answer` → `draft`
- **Result:** Round 1's three replies are consumed and in the criteria: a move gets a fourth
  column and is kept out of *spent*, every envelope that existed by the end of the month gets a
  row, and income stays dated when it is typed with the limitation recorded as their choice. No
  question on this item is open and no new item was filed. The item is back at `draft`; `refine`
  round 2 still owes AC1 and AC5's command surface, and cannot run until `WI-0002` is `done`.

## 2026-09-11T05:07:41Z — refine v0.6.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** `draft` — dispatched by `next` as the highest-ranked runnable item. `WI-0002` closed as `delivered` at `2026-09-11T05:01:12Z`, which cleared this item's `depends-on` and made it runnable for the first time since round 1 suspended it. Among the four runnable drafts, `WI-0003`, `WI-0004` and `WI-0005` tie at priority rank 3 and this one has the earliest `created` (01:57:16Z); `WI-0006` is rank 4.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — eight criteria and the whole of `## Notes`, including round 1's four assumptions and its list of what round 2 has to do
  - `tracker/items/WI-0003/history.md` — three rows. **Read first, as the procedure requires:** this item reached `draft` from `answer-questions` propagating round 1's replies, not from a send-back, so round 2 is a continuation of round 1's agenda rather than a repair of a named defect
  - `tracker/items/WI-0003/journal.md` — round 1's entry and `answer-questions`' propagation entry
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — round 1 in full: the agenda, what it deliberately did not ask and why, its four assumptions with their authority, and `## What round 1's answers left for round 2`
  - `tracker/items/WI-0003/questions/Q-001` to `Q-003` — all `answered`, with their `## Cross-answer check` and `## Consequences` sections
  - `tracker/items/WI-0002/questions/Q-003.md` and `Q-004.md` — the two answers round 1 said would settle this item's command surface, read in full including the stakeholder's stated reasons
  - `tracker/items/WI-0002/questions/Q-005.md` — the future-date refusal, for `Q-005`'s cross-answer check
  - `tracker/items/EP-001/questions/Q-003.md`, `Q-004.md`, `Q-006.md` — what the summary shows, the period, and the command name
  - `tracker/items/WI-0002/item.md` — AC11 and AC13 as delivered, which is what round 1's unreadable-month assumption now stands on
  - `.claude/agile-skills/spec/dor-dod.md` §1 and `spec/question.md` §2
- **Decisions:**
  - **Two blocking questions filed to the human, no criterion rewritten.** `Q-004` on how a month is named on the command line; `Q-005` on a month that has not happened yet. They are one ask, framed as *round 2, question n of 2*, and the last one says so.
  - **`Q-004` is filed rather than decided, and the reason is structural.** Round 1 declined to ask this on the grounds that `WI-0002/Q-003` and `WI-0002/Q-004` would settle it, and set a condition for round 2 to file anyway. `Q-004`'s answer settles **half**: a month is `2026-08` and no digit is in doubt. `Q-003`'s does not settle the other half, because the reason the stakeholder gave — *"The description is the bit I'll actually type, so make that the cheap one, and put the longer spelling on the date since I'll hardly ever give one"* — was ranking **two** optional things competing for one bare-word slot on `envel spend`. `envel summary` has one optional thing, so the contest is absent and what remains of their rule is a bare frequency question about their own habits. The record points both ways: they look at a month *"a couple of days after it has ended"* [src: EP-001/Q-004], which makes naming a month the common case; their own rule sends the rare thing behind an option. Applying either would be answering for them, and `WI-0002/Q-003` is direct evidence they have a non-obvious preference here — they chose option C, neither of the two obvious answers.
  - **`Q-005` exists because one of round 1's own assumptions was falsified by the stakeholder's reply to `Q-002`, and it is withdrawn rather than corrected.** Round 1 assumed *"a month in the future is summarised like any other, and is simply empty"*, on the premise that a future month holds no entries and so lands in AC4's empty case. AC7 now says a row goes to every envelope that existed by the end of the month summarised — and every envelope that exists today existed by the end of any future month. So `envel summary 2027-03` prints every envelope, zeros in the three activity columns and today's balance under what is left: a page indistinguishable from a real report for a month that has not happened. Re-deciding it from `WI-0002/Q-005` — where they refused a future date on a spend — would be stretching an answer about **writing to their file** to cover **reading a report**, which is the exact move round 1 refused to make with `WI-0002/Q-001` on income. The assumption is withdrawn, the withdrawal is recorded in `## Notes` and in the Q&A, and the case goes to them.
  - **No acceptance criterion was rewritten, deliberately.** AC1 and AC5 are downstream of `Q-004` and AC4 is downstream of `Q-005`. Writing them now means guessing two answers and renumbering the list again in round 3 while citations point into it. Round 3 has three things to write and no more.
  - **The renumbering obligation was discharged rather than assumed.** `grep -rn 'WI-0003 AC' tracker docs` → exit 0, four citations, every one naming **AC8** and every one anchored to its opening words, in `ADR-0002` `## Corrections`, `ADR-0006`, and `WI-0002`'s review and verification reports. Each was re-read against the criterion it now points at; AC8 still opens with *"A month's money-in figure is the income"*, so all four resolve to the sentence their author meant. Round 1's note that this grep found nothing is true of round 1 and is now out of date — `WI-0002`'s ADR work cited AC8 in between — and the Q&A says so rather than leaving the stale claim standing.
  - **Round 1's other three assumptions re-read and left standing**, each still `[assumed]` under **no** delegation with where a disagreement lands: the subcommand `summary`; an unreadable month refused with a message and nothing printed, which now rests on delivered behaviour rather than planned behaviour [src: WI-0002 AC11 "accepts the full `YYYY-MM-DD` form and nothing else"]; and *"moved in or out"* as one net figure. Nothing new was assumed this round.
  - **Nothing was routed to `plan` that was not already there.** Round 1's three design questions stand in `## Notes` unchanged; this round found no fourth.
- **Questions raised:** two, both blocking and both addressed to `human` — `WI-0003/Q-004` (how a month is named on the command line) and `WI-0003/Q-005` (a month that has not happened yet). Full text in the question files; the round's record is `artifacts/refinement-qa.md` `## Round 2`. None left `[unresolved]`.
- **Commands:**
  - `grep -rn 'WI-0003 AC' tracker docs` → exit 0, four citations, all naming AC8, all anchored
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 3 consumed human answers, 0 delegations
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition; before it, the two expected errors this round's own act creates — `board.stale` and `question.blocking.not-suspended` on an item still at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0. Filing two blocking questions against an item still at `draft` raises `question.blocking.not-suspended` by construction; the suspension this transition makes is what clears it, which is why the gate is read after the move rather than before it.)
  - `definition-of-ready` → **fail** (, criterion by criterion.** R1 pass (frontmatter complete, `type`/`epic`/`priority` set). R2 pass (`## Story` names role, capability and outcome). R3 pass (eight labelled checkboxes). **R4 fail** — AC1 and AC5 name no command surface; `Q-004`. R5 pass (`## Out of scope` names four things, including the total line and the individual spends a reader could reasonably assume were included). **R6 fail by this round's own act** — two blocking questions now open, which is what suspends the item. R7 pass (`depends-on: WI-0002`, now `done`). R8 pass (this Q&A, `status: recorded`, round 1 in full and round 2 appended). R9 pass (one coherent change: one subcommand that reads the store and prints a table). **R10 fail** — the future-month combination had a stated behaviour and AC7 falsified it, so it is now neither stated nor honestly unconstrained; `Q-005`. R11 pass — no criterion counts a project artefact; AC2's *"four figures"* counts columns of the tool's own output, which R11 is not about. R12 pass — three `[assumed]` entries survive, each saying in terms that it was taken under **no** delegation and where a disagreement lands, and no standing licence is relied on anywhere in this item.)
  - `criteria-are-decidable` → **fail** (on two of eight, and it is the same fail as R4.** AC2, AC3, AC4, AC6, AC7 and AC8 each name what would be observed — the figures in a row, the arithmetic across them, which envelopes appear, what a quiet month prints. AC1 and AC5 do not: *"There is an `envel` command that prints a summary for a calendar month"* names no command to run, and until `Q-004` is answered nobody can write the invocation a verifier would type. Recorded as failing rather than papered over with a plausible command line.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` → exit 0, 3 consumed human answers and 0 delegations. This execution consumed **no** answer — round 2 asks, it does not propagate — so `Checked against: none`, with that reason. Both new questions carry their `## Cross-answer check` filed **with** the question, naming the prior answers each reply will have to coexist with, and `Q-005`'s records the watch: `WI-0002/Q-005` is about recording a spend and is deliberately not read as covering a report.)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` carries round 1 in full and round 2 appended: the DoR walk as a table, the R10 failure with round 1's own words quoted before they are withdrawn, both questions with why each is the stakeholder's, the detailed reason `WI-0002/Q-003` does not reach `Q-004`, the four round-1 assumptions re-read with three left standing and one withdrawn, and what round 2 has not settled. No answer was received this round, so nothing is tagged `[human]` by it; the three `[assumed]` entries that survive each carry their **under no delegation** line and where a disagreement lands.)
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-004.md` — new, blocking, to `human`
  - `tracker/items/WI-0003/questions/Q-005.md` — new, blocking, to `human`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `## Round 2` appended
  - `tracker/items/WI-0003/item.md` — `## Notes` only; **no criterion changed, and no criterion changed its number**
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0003` round 2 asked the stakeholder two questions and rewrote nothing. One is the item's own recorded remaining R4 failure — how a month is named on the `envel summary` line, which the two `WI-0002` date answers turned out to settle only half of. The other is new and arises from the collision of two of their own answers: round 1 assumed a future month would print nothing, and their reply to `Q-002` made that false, so the tool would now print a plausible-looking report for a month that has not happened. The assumption is withdrawn rather than quietly re-decided. Round 3 writes AC1, AC5 and AC4 from the replies and walks the Definition of Ready with R4, R6 and R10 closed.

## 2026-09-11T05:19:53Z — answer-questions v0.6.3 — architect

- **Item:** WI-0003
- **Trigger:** `awaiting-answer` since `refine` round 2 suspended the item, with `resume-to: draft`
  on that history row. The stakeholder's replies had arrived in both question files' `## Answer`
  sections, so the two open human-addressed questions were answerable in the precondition's sense
  and this skill is the only one that may consume them.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` … `Q-005.md` — all five, the three already
    `answered` for what round 1 settled, and `Q-004`/`Q-005` for the replies being consumed
  - `tracker/items/WI-0003/item.md` — the nine criteria, `## Out of scope` and the whole of
    `## Notes`, including round 2's withdrawal of the future-month assumption
  - `tracker/items/WI-0003/history.md` — the suspending row and its `resume-to: draft`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — both rounds' agendas, round 1's answers,
    and `## Decided here, and by what authority — round 2`
  - `tracker/items/WI-0003/artifacts/` — no `plan.md` exists; the item has never been planned, so
    there is no invalidation set for this execution to write into
  - `docs/architecture/adr/` — all six ADRs, checked for anything either answer would contradict:
    `ADR-0001` (integer cents), `ADR-0002` (JSON entry log), `ADR-0003` (store location),
    `ADR-0004` (invocation package and shim), `ADR-0005` (stdlib-only checks), `ADR-0006` (a spend
    carries the date it happened). None states or implies how a month is named on the command
    line, and none states what a future month does. No contradiction, so no escalation under
    `spec/question.md` §4's third condition.
  - `docs/product/vision.md` v2 — read in full, for the same reason and for whether either answer
    had to be propagated into it
  - `tracker/items/WI-0002/item.md` — AC11 for the delivered date form, cited in the new AC5
  - `tracker/items/WI-0001/item.md` — AC16 for the delivered refusal convention, cited in the new
    AC9
- **Decisions:**
  - **Q-004 — answered by the human, route: escalation returned.** Option A: the month is a plain
    word, `envel summary 2026-08`, and `--month` is not accepted. Propagated into AC1 (the command
    surface, the plain word, the rejection of `--month`, their reason quoted) and AC5 (both
    invocations shown, a month fixed at `YYYY-MM` citing `WI-0002` AC11). This is the criterion
    pair round 1 and round 2 both left standing, and it is settled by the stakeholder directly
    rather than derived — which is precisely what round 1 declined to do on their behalf.
  - **Q-005 — answered by the human, route: escalation returned.** Option A: a month later than
    the current one is refused with a message. Propagated into a new AC9 (the refusal, the *later
    than the current month* boundary rather than *later than today*, stream and exit code cited to
    `WI-0001` AC16), into AC4 (its empty case is reached only for a month the command accepts) and
    into `## Out of scope` (the forward projection they declined in the same reply).
  - **The criteria were written here rather than left to `refine` round 3.** Round 2's stated
    reason for deferring them was that writing them would have meant guessing two answers; the
    answers are now in and they are answers about exactly these criteria, so the reason no longer
    holds. AC1, AC4 and AC5 were amended **in place** and AC9 **appended**, so no criterion
    changed its number — the cost round 2 was avoiding did not arise. This is the same call round
    1's consumption made, for the same reason, and it is recorded in `## Notes` rather than left
    for a reader to reconstruct.
  - **One thing deliberately *not* written**: round 1's remaining `[assumed]` decision that *a
    month the tool cannot read is refused, with a message, and nothing is printed* still has no
    criterion. No question asked it, it is `refine`'s own assumption under no delegation, and
    putting an assumption into a criterion is refinement's judgement taken in the open rather than
    a propagation. It is named in the round-3 hand-over so it cannot be lost.
  - **No item filed.** The only work either answer could have implied is the forward projection
    behind `Q-005`'s option B, and the reply refuses it in as many words. Filing it would put work
    on the board the stakeholder had just declined — the same reasoning round 1 applied to
    `Q-003`.
  - **No document under `docs/` was changed.** Both answers settle one command's surface and one
    command's refusal, which is item-level detail; no sentence in `vision.md` or in any ADR
    asserts either. Nothing was written into a `## Engagement state` section and neither answer
    falsified a sentence in one.
- **Questions raised:** none — no cross-answer verdict came out `conflicts`, and neither reply
  left anything that the record could not settle.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0 (5 consumed human answers,
    0 delegations, 0 errors, 0 warnings)
  - `.claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation
    --item WI-0003 --uncommitted` → exit 0 (0 uncommitted paths under `docs`, 0 quantified
    sentences, 0 unanswered)
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending
    --uncommitted` → exit 0 (0 documents in the window)
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1 before the transition, on exactly
    the two errors this execution's own move clears: `board.stale` and
    `question.awaiting.none-open` on `WI-0003`. Re-run after the transition and `board-gen`.
- **Gates:**
  - `answer-is-propagated` → **pass** (each `## Consequences` section names files, and every file was re-opened after writing: `item.md` AC1 names `envel summary` and rejects `--month`; AC5 shows both invocations and fixes `YYYY-MM`; AC9 exists and states the refusal and its boundary; AC4 carries the new sentence deferring to AC9; `## Out of scope` carries the projection bullet; `refinement-qa.md` carries `## Answers — round 2` with both replies verbatim. Neither Consequences section names zero files.)
  - `answered-from-the-record` → **pass** (neither answer was produced by this skill — both are the stakeholder's own replies to escalations, quoted verbatim in `## Answer` and again in `refinement-qa.md` `## Answers — round 2`; the two supporting citations this execution wrote into criteria both resolve, `WI-0002` AC11 and `WI-0001` AC16, checked by grep against those items)
  - `escalation-is-justified` → **pass** (no question was re-addressed to the human by this execution; both questions it handled were already escalations filed by `refine` round 2, and both are now returned)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0003 --uncommitted` exit 0; no sentence was written into `docs/` at all, so there is no cited fact and no quantified claim to discharge)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` exit 0; no `## Engagement state` section was written or amended, and neither answer falsified a sentence in one — both are about a command's behaviour, not about the engagement)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` exit 0; eight verdicts across the two replies, all `compatible`, no conflict, so no question was filed under ADR-0008 §3 — `Q-004` against `WI-0002/Q-003`, `WI-0002/Q-004`, `EP-001/Q-004`, `EP-001/Q-006`, and `Q-005` against `WI-0002/Q-005`, `WI-0003/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`; no claim in `docs/` sourced to a human answer was rewritten, none being touched)
  - `workspace-valid` → **pass** (`validate-workspace` re-run after this transition and `board-gen`; the two errors it reported beforehand, `board.stale` and `question.awaiting.none-open`, are exactly the ones this move clears)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-11T05:07:41Z records `resume-to: draft`; this execution moves the item to `draft` and to nothing else, both blocking questions on it now being `answered`)
  - `a-deferral-is-not-an-answer` → **pass** (no reply deferred — both choose an option by letter and give a reason, and `Q-005`'s reply also refuses a named piece of work outright, which is a decision rather than a postponement and is recorded as `## Out of scope` rather than as something to revisit)
- **Cross-answer check:**
  - `Q-004` — checked against `WI-0002/Q-003` (compatible: their stated rule is *the thing you
    type often gets the short form*, and this reply supplies the missing fact that the month is
    typed often; `envel spend`'s `--on` is untouched), `WI-0002/Q-004` (compatible: a month is
    `YYYY-MM-DD` with the day taken off), `EP-001/Q-004` (compatible: bare `envel summary` still
    means the current month), `EP-001/Q-006` (compatible: the command is still `envel`).
  - `Q-005` — checked against `WI-0002/Q-005` (compatible, and deliberately not read as having
    already answered it: that was about writing a future-dated spend to the file, this is about
    reading a report, and the stakeholder gave a different reason for each), `WI-0003/Q-002`
    (compatible: AC7 is untouched and simply never applies to a refused month), `EP-001/Q-003`
    (compatible: option C would have added a line to the page, option A adds nothing, so AC6
    stands), `EP-001/Q-004` (compatible: the boundary is *later than the current month*, so the
    current month is still summarisable).
  - No verdict was `conflicts`, so no question was filed and no document was edited in place of
    asking.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-004.md` — `status: answered`, `answered-by: human`,
    `answered-at` stamped, `## Cross-answer check` written with four verdicts, `## Consequences`
    naming the three files
  - `tracker/items/WI-0003/questions/Q-005.md` — the same, with four verdicts and five
    consequence rows
  - `tracker/items/WI-0003/item.md` — AC1 rewritten, AC4 amended, AC5 rewritten, AC9 appended,
    `## Out of scope` gained the forward-projection bullet, `## Notes` gained round 2's answers,
    the closure of the withdrawn assumption and the round-3 hand-over
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `## Answers — round 2`,
    `## Cross-answer check — round 2, on the replies` and `## What round 2's answers left for
    round 3` added; the `status: recorded` paragraph and `## What round 2 has not settled`
    updated
  - no ADR created, no document under `docs/` touched, no new item filed
  - commit: `tracker: the answered questions and every artifact you propagated into (refs
    WI-0003)`
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of round 2's escalations came back answered and are propagated: the month is a
  plain word on the command line, and a month later than the current one is refused rather than
  printed. AC1 and AC5 finally have a command surface, AC9 states the refusal, and nothing on
  `WI-0003` is waiting on the stakeholder — the item returns to `draft` for `refine` round 3,
  whose remaining job is the Definition of Ready itself rather than any more writing.

## 2026-09-11T05:26:39Z — refine v0.6.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** `draft`, dispatched by `next` as the highest-ranked runnable item on the selection
  key — priority-rank, then `created`, then ID. This is `refine` round 3. `history.md` shows the
  item reached `draft` from `awaiting-answer` by `answer-questions` consuming round 2's two
  stakeholder answers, not by a send-back from `verifying` or `in-review`, so this is a
  continuation of refinement rather than a repair of something specific.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — nine criteria, `## Story`, `## Out of scope`, the whole of
    `## Notes`
  - `tracker/items/WI-0003/history.md` — all four rows, to establish which kind of `draft` this is
  - `tracker/items/WI-0003/journal.md` — the earlier rounds' entries and their renumbering checks
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — rounds 1 and 2, both answer sections,
    both cross-answer checks, and `## Decided here, and by what authority` for each round
  - `tracker/items/WI-0003/questions/Q-001.md` … `Q-005.md` — all five, all answered, re-read
    while writing criteria
  - `.claude/agile-skills/spec/dor-dod.md` §1 — the twelve Definition-of-Ready criteria
  - `tracker/items/WI-0001/item.md` — AC3, AC6, AC8, AC11, AC15, AC16 and AC17, the delivered
    conventions four of this round's criteria cite
  - `tracker/items/WI-0002/item.md` — AC11, AC13 and AC14, for the date form, the stream rule as
    a sibling item wrote it, and the usage treatment
  - `tracker/items/WI-0004/item.md` — status and `depends-on`, to establish that adding it as a
    dependency creates no cycle
  - `docs/architecture/overview.md` — the recorded stdout/stderr convention AC13 cites
  - `docs/product/vision.md` v2 — read; nothing in it constrains this round's criteria
- **Decisions:**
  - **R7 — `depends-on: WI-0004` recorded. This is the round's real finding.** Round 1's argument
    for depending on `WI-0002` — *"there is no such thing as the money spent from it during that
    month until spending exists"* — now applies word for word to moving money, because the
    stakeholder's answer at `Q-001` put a fourth **moved** column in the report after round 1 had
    already recorded the dependency. AC3's worked example is a required observation and needs a
    non-zero moved figure, which no tool without `envel move` can produce. The consequence is
    written into `## Notes`: nothing is dispatched on this item until `WI-0004` is `done`.
    `WI-0004` depends only on `WI-0001`, which is `done`, so there is no cycle. This reorders the
    board and is a mechanical consequence of a criterion rather than a judgement about priority.
  - **R4 — AC1 amended.** *"`envel summary --month 2026-08` is not accepted"* said nothing a
    reader could observe. It now says the line is refused as a wrong command line, per AC14. The
    stakeholder's choice and their quoted reason are untouched.
  - **R4 — AC4 amended.** *"produces a summary that says so"* named no stream and no exit code. It
    now prints to stdout and exits 0, cited to the delivered empty-listing behaviour at `WI-0001`
    AC6. The reasoning is recorded: an empty month is a successful answer to a readable question,
    not a refusal, and the project already treats an empty listing that way.
  - **R10 — AC10 appended, row ordering.** Not an assumption: the delivered convention
    [src: WI-0001 AC3]. The criterion also records that there is no tie to break, because names
    match case-insensitively [src: WI-0001 AC11].
  - **R10 — AC11 appended, how a figure is written.** Not an assumption: two decimal places
    [src: WI-0001 AC8] and no currency symbol [src: WI-0001 AC17]. Written down because AC3's
    worked example is already in that form and a reader should not have to infer the rule.
  - **R10 — AC12 appended, an unreadable month. This is the one genuine decision of the round.**
    `[assumed]`, under **no delegation**. It is round 1's own assumption — *"a month the tool
    cannot read is refused, with a message, and nothing printed"* — finally reaching a criterion,
    made decidable by naming the rejected forms (`2026-8`, `08-2026`, `august`, `2026-13`,
    `2026-08-01`) and the accepted month range `01`–`12`, which nobody had ever written down. A
    disagreement lands on AC12 alone and costs one parser rule. `answer-questions` declined to
    write this twice, on the grounds that putting an assumption into a criterion is refinement's
    judgement taken in the open; this round takes it.
  - **R10 — AC13 appended, streams and exit codes.** Not an assumption: the recorded convention
    [src: docs/architecture/overview.md] and the delivered rule [src: WI-0001 AC16]. Written case
    by case against the criteria that name them, in the shape `WI-0002` AC13 already uses.
  - **R10 — AC14 appended, a wrong command line.** Not an assumption: the delivered treatment
    [src: WI-0001 AC15] [src: WI-0002 AC14]. It is what makes AC1's refusal observable and it is
    where the extra-word case lives.
  - **Nothing was asked of the stakeholder, and the test was applied failure by failure.** R4's
    two gaps are the wording of criteria about behaviour they have already chosen; R7 is a
    scheduling fact derived from their own answer; four of R10's five combinations are delivered
    conventions and the fifth is round 1's assumption. Asking would have been asking them to
    confirm what they have already said, which is `refine` step 3's second test.
  - **Three things left deliberately unconstrained**, each `[assumed]` under no delegation and
    each recorded in `## Notes` with where a disagreement lands: which message wins when more than
    one refusal applies at once (`envel summary 2027-13` is both unreadable and in the future);
    the wording of every message; and whether the four figures carry a header line.
  - **Numbering held.** AC1 and AC4 amended in place, AC10–AC14 appended, so no criterion changed
    its number.
- **Questions raised:** none. Round 3 filed no question — nothing on the Definition-of-Ready
  agenda was the stakeholder's. Five questions exist on this item from rounds 1 and 2 and all five
  are `answered`; none is `[unresolved]`. The full record of this round is
  `artifacts/refinement-qa.md` `## Round 3`.
- **Commands:**
  - `grep -rn 'WI-0003 AC' tracker docs` → exit 0, seven citations from outside this item's own prose: four naming AC8 (`ADR-0002` `## Corrections`, `ADR-0006` line 38, `WI-0002`'s review and verify reports) and three naming AC2 (`WI-0004`'s `Q-001`, its `refinement-qa.md`, its `item.md`). Every one is anchored to its criterion's opening words, and neither AC2 nor AC8 was touched this round, so all seven still resolve.
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0 (5 consumed human answers, 0 delegations, 0 errors, 0 warnings)
  - `python3 .claude/agile-skills/scripts/board-gen .` → wrote `tracker/board.md`
  - `.claude/agile-skills/scripts/validate-workspace` → exit 0 after the board was regenerated
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` exit 0; the one error it reported mid-round was `board.stale`, cleared by `board-gen`)
  - `definition-of-ready` → **pass** (, criterion by criterion: R1 pass (frontmatter complete, `type`/`epic`/`priority` set); R2 pass (`## Story` names role, capability and outcome); R3 pass (fourteen criteria, each labelled and a checkbox); R4 **fail → fixed** (AC1 and AC4 were not decidable; both amended, and the twelve others re-read one by one — each names a command to run and an output to inspect, and none carries an unmeasurable adjective); R5 pass (`## Out of scope` names six things, including the forward projection the stakeholder ruled out at `Q-005`); R6 pass (no open question on this item); R7 **fail → fixed** (`depends-on` gained `WI-0004`, the dependency recorded and the item sequenced after it); R8 pass (`artifacts/refinement-qa.md`, `status: recorded`, both rounds' answers verbatim and round 3 appended); R9 pass (one command producing one report; nothing here is two items); R10 **fail → fixed** (five unstated combinations, now AC10–AC14; three further combinations recorded in `## Notes` as deliberately unconstrained with who left them so); R11 pass (no criterion counts anything this item may move — AC3's figures are the tool's own output, not project artefacts); R12 pass (every `[assumed]` entry says plainly that nothing licensed it and names the criterion a disagreement lands on; no standing delegation exists on this project, the stakeholder having answered every question by choosing an option))
  - `criteria-are-decidable` → **pass** (each of the fourteen taken in turn with the command that settles it: AC1 `envel summary 2026-08` against `envel summary --month 2026-08`; AC2 and AC3 the four figures and the arithmetic of the worked example; AC4 an empty month on stdout with exit 0; AC5 bare `envel summary` against a named month; AC6 the absence of a total line and of individual spends; AC7 the rows for untouched and later-created envelopes; AC8 income entered late; AC9 `envel summary 2027-03`; AC10 the order of the rows; AC11 the form of every figure; AC12 each named unreadable month; AC13 the stream and exit code case by case; AC14 each wrong command line)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` exit 0. `Checked against: none — this execution consumed no human answer`: round 3 asked nothing and recorded no reply, and every answer this item holds was consumed by `answer-questions` earlier, each carrying its own verdicts. The five were re-read while writing the criteria and none of AC10–AC14 touches a sentence the stakeholder wrote — they are conventions and one prior assumption of ours.)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` declares `status: recorded` and carries every question and every reply verbatim across three rounds, each answer tagged `human` or `[assumed]`; round 3's own section records that it asked nothing and why, with each decision's authority named — citation or assumption under no delegation)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — `depends-on` gained `WI-0004`; AC1 and AC4 amended in place;
    AC10, AC11, AC12, AC13 and AC14 appended; `## Notes` gained round 3's record, what it added and
    on whose authority, the numbering check, and three things left deliberately unconstrained; the
    trailing `[assumed]` list updated to name the criterion each lands on
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `## Round 3` added: the Definition-of-
    Ready walk as a table, the R7 finding in full, `## Decided here, and by what authority — round
    3`, what was left unconstrained, the cross-answer check, and what round 3 leaves
  - `tracker/board.md` — regenerated; `WI-0003` now shows `blocked by WI-0004 (draft)`
  - commit: `tracker: the refined item and its Q&A record (refs WI-0003)`
- **Status:** `draft` → `ready`
- **Result:** `WI-0003` is Ready, with no override and no question to the stakeholder. Two
  criteria were made decidable, five were appended to cover combinations nothing had stated, and
  the round's real finding is R7: the stakeholder's own answer at `Q-001` put a **moved** column in
  this report, which makes `WI-0004` a dependency that round 1 could not have seen. The item is
  Ready but not runnable until `WI-0004` is `done`, which is that criterion working rather than
  failing.

## 2026-09-11T06:26:47Z — plan v0.6.3 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` as the status owner. It became runnable this
  turn: `depends-on: WI-0002, WI-0004` and `WI-0004` closed at `06:15:17Z`, which is what the
  dependency was recorded for. Highest-ranked runnable candidate (priority `medium`, created
  `2026-09-11T01:57:16Z`), ahead of `WI-0005` on `created` and `WI-0006` on priority.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the fourteen criteria, the out-of-scope list, and the four
    things `## Notes` routes to `plan`
  - `tracker/items/WI-0003/history.md` — three `refine` rounds and two `answer-questions`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — every `[assumed]` entry (the subcommand
    name, AC12's unreadable-month rule, the net moved figure), `## Routed to plan, not to the
    stakeholder`, and `## Left deliberately unconstrained by round 3`
  - `docs/architecture/overview.md` (v5, now v6) and `docs/product/vision.md` (v2), opened rather
    than recalled, to seed the invalidation set
  - every ADR: `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0007`
  - `tracker/items/WI-0002/artifacts/plan.md` — for the answer it gave to the absent-envelope
    question, so that this item gives the same one
  - the code: `envel/cli.py`, `envel/envelopes.py`, `envel/dates.py`, `envel/money.py`,
    `envel/store.py`, and `tests/test_cli.py` and `tests/test_envelopes.py` for the shapes the new
    tests follow
  - `tracker/project.yaml`
- **Decisions:**
  - **`ADR-0008` — a month is the `on`-else-`at` prefix of an entry, held as a `YYYY-MM` string,
    and every figure is a filtered sum.** *Asked of the documents, then decided.* Four options, and
    the one rejected loudest is branching on `kind`: it would make `ADR-0006`'s own sentence
    *"with no branch on what a date means"* false the day it was written, and a kind added later
    would fall through whichever branch the `else` is. The string form is the part that buys the
    most: both stored date fields are zero-padded fixed-width ISO, so lexicographic order **is**
    chronological order and *earlier*, *in* and *later* are `<`, `==`, `>` with no calendar
    arithmetic anywhere in the change. And the filtered sums are what make AC3's reconciliation a
    property of the arithmetic — the three month-M columns partition month M's entries, `left` is
    the sum over months ≤ M, so `left − (in − spent + moved)` is the sum over months < M, the
    carried-in balance, by definition. No plan step computes a carried-in figure and none checks
    the identity, because there is nothing that could drift.
  - **`ADR-0009` — the report lives in `envel/summary.py`.** *Decided*, with a real alternative:
    a sixth operation in `envelopes.py`. The module's own docstring says an operation returns
    *"the new document and the lines to show"*, and a report returns lines and no new document, so
    the file would hold two kinds of thing under one description. Reversal is cut-and-paste plus
    one import line, and it is priced in the ADR.
  - **Month parsing goes in `envel/dates.py`.** *Answered from the documents* — that module is
    already *"the only place text and calendar days meet"*, so this is a decision read rather than
    taken. `parse_month`'s regex carries the `01`–`12` range itself, because there is no
    `date.fromisoformat` equivalent for a month to check the calendar afterwards the way
    `parse_date` does. `2026-13` is AC12's own example and the regex is what refuses it.
  - **All four things `refine` routed here are answered, none of them re-asked.**
    - *How a month's figures are computed:* filtered sums over the entry log on every run
      (`ADR-0008`).
    - *How an end-of-month balance is derived for a month that is not the current one:* the sum of
      `cents` over the envelope's entries whose month is ≤ that month — the same sum `balance`
      already is, bounded (`ADR-0008`).
    - *What the summary does with an entry naming an envelope no longer present:* it contributes to
      no row, and this item adds no check. This is deliberately, word for word, the answer
      `WI-0002`'s plan gave — *"an entry naming an absent envelope is invisible, and this item adds
      no check"* — quoted in `## Assumptions` so the two cannot drift. It cannot arise today: no
      command removes an envelope.
    - *The order of the refusals:* argparse (AC14), then an unreadable month (AC12), then a future
      month (AC9). **Read off the existing structure rather than chosen** — a malformed value is
      raised where it is parsed in `cli`, which is exactly what `WI-0002` and `WI-0004` already do,
      so `envel summary 2027-13` reports the unreadable month. `refine` recorded that every
      criterion involved is satisfied by any of the messages.
  - **AC14 needs no new code, and that was checked rather than assumed.** An argparse probe over
    the intended subparser confirmed that `--month 2026-08` and a trailing `extra` each leave
    something unrecognised, which the delivered `parse_known_args` path routes to the
    **subcommand's** own parser; and `python3 bin/envel list --month 2026-08` on a shipped
    subcommand already prints `usage: envel list [-h]` and exits 2. Writing a plan step that says
    "handle the wrong shape" without knowing this would have been the deferral this skill is
    warned about.
  - **The row is a labelled sentence with no header line.** *Assumed, reversibly*, under **no
    delegation**. `refine` round 3 left the header question open in as many words. Two reasons:
    every success line this tool prints is prose that says what it is, and AC6 says the content is
    *"the four columns of AC2 and nothing else"*, which a header would have to argue past and an
    in-row label would not. Reversal is one format string.
  - **`-h` stays on the subparser.** *Assumed, reversibly.* Every delivered subcommand has it, and
    AC14's subject is an option carrying the month.
  - **Nothing is precomputed.** *Answered from the documents* — `ADR-0002` makes a balance derived
    rather than stored, and precomputing a month would be a second source of truth and a `format`
    change. Recorded under `## Assumptions` only so the routed question has a visible answer.
  - **The overview went to v6**: the `envel/summary.py` row, the dependency sentence and its new
    edge, `WI-0003` leaving `## What is not decided yet`, and — the one that matters — the
    conventions line. It said *"A date typed at the command line is written `YYYY-MM-DD` and
    nothing else"*, and this item is the first to type a **month** at the command line. That
    sentence was about to become false; it now reads *"`YYYY-MM-DD`, and a month `YYYY-MM`, and
    nothing else"* and is an invalidation row for `implement` to check against the built parser.
  - **`tracker/project.yaml` needed no change.** Both commands are real and both were run here.
- **Cross-answer check:** `none in the sense that matters` — this execution consumed no human
  answer and recorded none. It did find one sentence where a repair could have looked like
  choosing between two of theirs, and that is written down rather than acted on:
  `docs/product/vision.md` calls the balance *"the summary's third column"*, citing
  `EP-001/Q-001`; `WI-0003/Q-001` later added the **moved** column ahead of it, so the balance is
  the fourth. The two answers coexist — `EP-001/Q-001` is about the balance **carrying over**
  rather than about its position, and nothing they said about carry-over is overtaken — and only
  the ordinal moved. It is an invalidation row with that reasoning attached, so `implement` repairs
  an ordinal rather than reconciling two answers. `scripts/lint-answers --uncommitted` → exit 0
  over 21 consumed answers and 0 delegations spent.
- **Questions raised:** none. Nothing this item forced is irreversible or depends on intent no
  document records: the two ADRs are answerable from `ADR-0002` and `ADR-0006`, the four routed
  questions are design with one right answer each, and the three assumptions each name the
  criterion a disagreement lands on and cost one line to reverse.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated
    --item WI-0003` → exit 0, *27 invalidation row(s), 0 deliverable document(s), 9 binding ADR(s)*
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1 twice on this
    execution's own new prose, then exit 0: seven absolutes in the two new ADRs needed a citation,
    and one `run:` citation recorded a command with no readable outcome
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 with exactly three
    `doc.changelog.no-execution` errors, one per document this execution versioned; exit 0 once
    this entry exists. See the `workspace-valid` gate line
  - `python3 .claude/agile-skills/scripts/validate-workspace . --resolving
    'WI-0003:ready->planned+journal'` → exit 1, the same three errors: the flag does not cover
    this rule
  - `python3 bin/envel list --month 2026-08` → exit 2, `usage: envel list [-h]` and
    `unrecognized arguments: --month 2026-08`; `python3 bin/envel list extra` → exit 2, the same
    shape — the delivered behaviour AC14 relies on
  - `python3 -` , an argparse probe building the intended `summary` subparser and calling
    `parse_known_args` on `summary`, `summary 2026-08`, `summary --month 2026-08` and
    `summary 2026-08 extra` → month `None`, then `2026-08` three times; unrecognised empty, empty,
    `--month`, `extra`
  - `find docs -name "*.md"` → 9 documents before this execution, 11 after
- **Gates:**
  - `workspace-valid` → **pass when run directly; the transition was taken with `--force`.** Read
    this in full, because the record must not overstate it.
    - Run on its own against the state this entry describes, `validate-workspace` reports **0
      errors, 0 warnings**.
    - It could not report that from *inside* the transition, and the deadlock is F-084's — the
      **fifth** time this engagement has hit it. This execution versioned three documents
      (`overview.md` to v6, and the two new ADRs at v1), and each change-log row says *plan changed
      this at `2026-09-11T06:20:16Z` for `WI-0003`*. `doc.changelog.no-execution` asks whether an
      execution of `plan` on `WI-0003` was running then, and the windows come from the journal —
      `WI-0003`'s journal has **no** `plan` entry at all until this transition writes one, so all
      three rows sit outside every window that exists and inside the one this entry creates.
    - `--resolving 'WI-0003:ready->planned+journal'` was tried and does not cover it: it exits 1
      with the same three errors. `resolved_by_move` downgrades `journal.execution.missing` for
      precisely this ordering, citing F-025 in its own comment, and `doc.changelog.no-execution` is
      the same problem one rule along.
    - The rows are honest and were not restamped. `spec/journal-and-history.md` §0 requires a
      change-log row's `when` to be read from a clock at the moment it is written, and
      `06:20:16Z` is when these were written. Backdating them to buy a green gate would record a
      time that is not true, which is the failure §0 exists to prevent.
    - So the move was made with `--force`, which skips the gate run and records `[gates forced]` in
      the history reason for ever. **Every other gate below was run by hand before that, and each
      passed**; the commands and their exit codes are under `**Commands:**` and can be re-run.
      `validate-workspace` was re-run immediately after the transition and reports 0 errors.
  - `every-criterion-is-addressed` → **pass** — `plan.md` `## Acceptance criteria mapping` carries
    fourteen rows, AC1 to AC14, matching the fourteen criteria in `item.md`
    (`grep -c '^- \[ \] AC'` → 14). Each names the step or steps that satisfy it and a **specific**
    demonstration rather than "tests": AC3's row names AC3's own worked example in cents and an
    identity asserted over a three-month document, AC7's names a byte-identical comparison of a
    past month's output before and after a new envelope is created, and AC11's names the regex
    every printed amount must match.
  - `project-commands-resolved` → **pass** — `tracker/project.yaml` already names
    `python3 -m unittest discover -s tests -t .` and `python3 -m compileall -q envel tests`, and
    both were run by this execution on the current tree: exit 0 with 119 tests, and exit 0. Neither
    exits zero without checking anything. No change was needed and none was made.
  - `decisions-recorded` → **pass** — `plan.md` `## Decisions and ADRs` lists nine choices, each
    pointing either at an ADR (`ADR-0008`, `ADR-0009`), at a document that already settles it, or
    at an entry under `## Assumptions` that states what reversing it costs. The three genuine
    assumptions — the row's wording, `-h`, and the absent-envelope rule — each say plainly that
    nothing licensed them and where a disagreement lands.
  - `plan-is-executable-without-you` → **pass**, advisory — ten numbered steps, each naming the
    files it touches and what is true afterwards. The two places a developer would otherwise have
    to decide are closed: the order of the refusals (`## Approach`, read off the existing
    structure) and the shape of a row (`## Approach` interface decision 3, with the AC6 reasoning).
    Step 3's afterwards gives the four integers `figures` must return for AC3's own example, so the
    sign of the spent column cannot be guessed.
  - `documents-at-risk-are-enumerated` → **pass** — `lint-documents --rule
    documents-at-risk-are-enumerated --item WI-0003` → exit 0, *27 invalidation row(s), 0
    deliverable document(s), 9 binding ADR(s)*. The set was written from a read of `docs/`, not
    from memory: all nine pre-existing documents plus the two this execution wrote were opened, and
    the rows that would not have survived recollection are the ones worth naming — the overview's
    conventions line, which this item is the first to falsify by typing a month at the command
    line; `ADR-0006`'s and `ADR-0007`'s `WI-0003` sentences, which are predictions about this item
    that this change turns into descriptions; and the vision's *"the summary's third column"*,
    which is now the fourth.
  - `cross-answer-consistency` → **pass** — `lint-answers --uncommitted` → exit 0, *21 consumed
    human answer(s) and 0 delegation(s) spent*. The `**Cross-answer check:**` bullet above is the
    read behind it, including why the vision's ordinal is a repair rather than a contradiction.
  - `claims-are-sourced` → **pass** — `lint-claims --uncommitted` → exit 0 over *3 document(s) in 3
    uncommitted path(s) under docs*, with citations checked across every markdown file in the
    workspace. It failed twice first, on this execution's own new prose, and both failures were
    real: seven absolute claims in the two new ADRs carried no citation, and one `run:` citation
    recorded a command whose outcome the grammar could not read. Both were fixed rather than
    reworded around.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new) — ten steps, fourteen mapped criteria, five
    assumptions, twenty-seven invalidation rows, no deliverable documents, nine binding ADRs
  - `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md`
    (new, v1)
  - `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` (new, v1)
  - `docs/architecture/overview.md` (v5 → v6)
  - `tracker/project.yaml` — unchanged; both commands were already real and both were re-run
  - no scaffolding: no file was created outside `tracker/` and `docs/`
- **Status:** `ready` → `planned`
- **Result:** `WI-0003` is designed and ready to build. One subcommand, one new module and three
  new functions in `envel/dates.py`; `ADR-0008` decides that a month is the `on`-else-`at` prefix
  of an entry and that every figure is a filtered sum, which makes AC3's reconciliation a property
  of the arithmetic rather than something a step arranges; `ADR-0009` puts the report in its own
  module. All four questions `refine` routed here are answered, none re-asked, and the
  absent-envelope one gives `WI-0002`'s answer word for word. Nothing was put to the stakeholder.

## 2026-09-11T06:30:02Z — implement v0.6.1 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next` as the highest-ranked runnable item — rank 3
  and `created` 2026-09-11T01:57:16Z, ahead of `WI-0005` at the same rank and a later `created`,
  with both `depends-on` (`WI-0002`, `WI-0004`) `done`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — fourteen acceptance criteria, `## Out of scope`, and the
    three rounds of refinement notes, including the three assumptions still under no delegation
  - `tracker/items/WI-0003/artifacts/plan.md` — ten steps, the criteria mapping, five assumptions,
    twenty-seven invalidation rows, `## Deliverable documents` `none`, nine binding ADRs
  - `tracker/items/WI-0003/history.md` — seven rows, ending `ready → planned` by `plan`; no
    send-back from `verifying` or `in-review`, so this is a first execution rather than a defect fix
  - `tracker/items/WI-0003/questions/Q-001.md` … `Q-005.md` — all five `answered` and already
    propagated into `item.md` by `answer-questions`; read as the record, not acted on directly
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`,
    `conventions.commit-subject`
  - `docs/architecture/adr/ADR-0008-*.md` and `ADR-0009-*.md` — this item's own two decisions
  - `envel/dates.py`, `envel/cli.py`, `envel/money.py`, `envel/envelopes.py`, `envel/store.py`,
    `tests/test_dates.py`, `tests/test_envelopes.py`, `tests/test_cli.py` — the shapes steps 1 to 9
    extend
- **Decisions:**
  - none yet. This entry opens the execution; the decisions taken inside the plan's latitude are
    reported by the closing entry at `in-progress → verifying`.
- **Cross-answer check:** none — this execution has written nothing yet, and no sentence under
  `docs/` carrying `[src: <ITEM>/Q-nnn>]` has been touched.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → exit 0, branch created at `main`
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition, on the branch head; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (decided at the closing transition, on the branch head; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (no test has been written yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (`main..wi/WI-0003` is empty at this moment, so the check has nothing to inspect; F-080 is the reason this is `pending` and not a `fail`; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (the diff is empty; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (nothing changed since `main`; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (nothing changed since `main`; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (nothing under `docs/` written yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/WI-0003`, created from `main`; no commit yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of `WI-0003` has started. The branch exists, the plan's ten steps and
  the two ADRs it rests on have been read, and the item is `in-progress` so that an interruption
  leaves a truthful status.

## 2026-09-11T06:47:20Z — implement v0.6.1 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, opened by this same execution's step-3 transition at
  2026-09-11T06:30:02Z; no send-back, no partial branch to reconcile.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the fourteen acceptance criteria and `## Out of scope`
  - `tracker/items/WI-0003/artifacts/plan.md` — ten steps, the criteria mapping, five assumptions,
    twenty-seven invalidation rows, `## Deliverable documents` `none`, nine binding ADRs
  - `tracker/items/WI-0003/history.md` and `questions/Q-001.md`…`Q-005.md` — all five `answered`
    and already propagated by `answer-questions`
  - `docs/architecture/adr/ADR-0008-*.md`, `ADR-0009-*.md` — this item's two decisions, read
    clause by clause; `ADR-0001`…`ADR-0007` — the seven it inherits
  - `docs/architecture/overview.md` (v6) and `docs/product/vision.md` (v2) — the two documents the
    invalidation set names
  - `envel/dates.py`, `envel/cli.py`, `envel/money.py`, `envel/envelopes.py`, `envel/store.py`,
    `envel/__main__.py`, `tests/test_dates.py`, `tests/test_envelopes.py`, `tests/test_cli.py`
  - `tracker/project.yaml` — the test and lint commands and the branch and commit conventions
- **Decisions:**
  - **`MONTH_LENGTH = 7` as a module constant in `envel/dates.py`.** Step 1 asked that the seven
    be *"written once"*; `this_month` needs it as well as `month_of`, so the literal is in a
    constant rather than in two places. The plan's own reason is what asked for it.
  - **`envel/dates.py`'s module docstring was reworded.** It said *"These three functions are the
    only conversions…"* and this change makes six, so the sentence was false in the commit that
    made it so. It is source rather than `docs/`, so no invalidation row covers it; declared as
    deviation 3 in the implementation report because it is a hunk tracing to no step.
  - **The plan's month-boundary race was left open, and this is the decision not to close it.**
    `cli` defaults to `dates.this_month()` and `summarise` compares against `dates.this_month()`;
    a run at exactly midnight on the first could refuse the month it had just defaulted to. The
    plan said to close it *"only if `implement` finds it free"*. It is not free: closing it means
    passing the current month into `summarise`, and both the plan and `ADR-0009` state the
    signature `summarise(store, month)`. Changing an interface an ADR names is not mine.
  - **Two `tests/test_cli.py` tests seed the store file rather than using `envel new`.** No command
    creates an envelope into the past, and AC7 gives a row only to envelopes that existed by the
    end of the month — so a test about last month's figures needs one that was there. Both first
    drafts used `envel new` and failed against AC7 working as specified; the tests were fixed and
    the code was not.
  - **Decided *not* to make, and not escalated either, because `ADR-0008` had already made it:**
    what a summary does with an entry naming an envelope that is not present. Point 5 of the ADR
    settles it — the summary iterates envelopes, so such an entry is in no row — and
    `tests.test_summary.Figures.test_an_entry_naming_an_envelope_that_is_not_there_is_in_no_row`
    asserts it. No question was needed.
  - **The plan's steps were paired rather than run in file order**, so that each code step was
    committed with the test that demonstrates it. Three pairs, three commits, plus the document
    repair.
- **Cross-answer check:** one sentence under `docs/` sourced to a stakeholder answer was edited:
  `docs/product/vision.md` `## What it is for`, *"It is why the summary's third column is a balance
  rather than a monthly remainder"*, which sits on `[src: EP-001/Q-001]`. It is an **ordinary
  repair**, not a decision that was theirs, and the test is `ADR-0008` §3's third row: has the
  stakeholder since said something incompatible? No. `EP-001/Q-001` says money left in an envelope
  at the end of a month stays in that envelope — a claim about **carrying over**, which this item
  delivers and which the sentence still makes. `WI-0003/Q-001` added a *moved* column ahead of the
  balance, which changed the column's **position** and nothing about what it is. The two answers
  coexist, so only the ordinal was repaired — to "the last column, the fourth of four" — with the
  history of the ordinal written into the sentence so that a later reader does not take the edit
  for a choice between two things the stakeholder said. `plan` reached the same reading before any
  code was written (`plan.md` `## Decisions and ADRs`, last paragraph) and recorded it as an
  invalidation row rather than a question.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → exit 0, **176 tests** (119 before this item),
    run after every step and last on the branch head
  - `python3 -m compileall -q envel tests` → exit 0
  - step 1 afterwards: `python3 -c "from envel import dates; …"` → `2026-08 2026-09`, and seven
    forms including `2026-13`, `2026-00` and `2026-08-01` each raising `DateError`
  - step 3 afterwards: `figures` over AC3's worked example → `(0, 2000, 3000, 6000)`
  - step 6 afterwards, against a scratch `ENVEL_FILE`: `bin/envel summary` → exit 0, two rows;
    `bin/envel summary 2026-08` → exit 0, `no envelopes existed in 2026-08`;
    `bin/envel summary --month 2026-08` → exit 2, `usage: envel summary [-h] [YYYY-MM]`;
    `bin/envel summary 2026-08 extra` → exit 2; `bin/envel summary 2027-03` → exit 1, a message on
    stderr; `bin/envel summary august` → exit 1; `bin/envel` → exit 2,
    `usage: envel [-h] {new,add,list,spend,move,summary} ...`;
    `python3 -m envel summary 2026-09` → exit 0, the same two rows (ADR-0004, both entry points)
  - the sensitivity check: fourteen mutants, one per criterion, each patch checked to match
    exactly once in its file before it was applied and the file restored afterwards → exit 0,
    **14 of 14 make their named test fail**. The uniqueness check is deliberate: `WI-0004`'s
    verification recorded three false negatives from a replace-first harness that patched an
    identical guard in the wrong function.
  - the claims audit, nine enumerations: `ls envel/*.py`; `sed -n '13p' envel/cli.py`;
    `grep -n "print(\|sys\.exit"` over the five modules below `cli` → exit 1;
    `grep -n import envel/envelopes.py` → no `summary`;
    `grep -n "ENVEL_FILE\|XDG\|store_path\|pathlib" envel/summary.py` → exit 1;
    `grep -rn "int(whole)\|% 100\|// 100\|\* 100\|float(" envel/*.py` → 2 lines, both `money.py`;
    `grep -rn "socket\|urllib\|http\|requests\|ssl" envel/ bin/envel` → exit 1;
    `grep -rn "curses\|colorama" envel/` → exit 1; and the entry-kind enumeration over a store
    built by the delivered commands → kinds `income`, `move`, `spend`, spend entries missing
    `on`: none
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, all 4
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents
    WI-0003` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared
    --item WI-0003 --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, one error, F-084 (see
    the gate line); `validate-workspace --root . --resolving 'WI-0003:in-progress->verifying
    +journal'` → exit 1, the same error, so the flag does not cover this rule
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 176 tests, run
    on the branch head after the last change. 119 of them are the delivered suite and 57 are this
    item's: 27 in `tests/test_summary.py`, 9 in `tests/test_dates.py` `Month`, 21 in
    `tests/test_cli.py` `Summary`.)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0, and it covers the two
    new files: `envel/__pycache__/summary.cpython-312.pyc` and
    `tests/__pycache__/test_summary.cpython-312.pyc` exist after it runs.)
  - `workspace-valid` → **fail** at the moment the gate was run, 0 errors immediately
    after this entry exists, and the move was taken with `--force`. Read this in full,
    because the record must not overstate it in either direction. The deadlock is F-084's,
    for the sixth time in this engagement.
    `validate-workspace .` exits 1 with exactly one error: `docs/product/vision.md:82`,
    `doc.changelog.no-execution` — the change-log row says `implement` changed the file at
    06:38:45Z for `WI-0003`, and this execution's journal window closes at its **opening** entry,
    06:30:02Z, because the closing entry is the one this transition is appending. The window
    becomes (06:30:02Z, this entry's stamp] the moment the entry exists, and 06:38:45Z is inside
    it — so the error is an artefact of the gate running before the entry it needs. `--resolving
    'WI-0003:in-progress->verifying+journal'` was passed explicitly and does not cover this rule.
    The row was **not** backdated to 06:30:02Z to buy a green gate: `spec/journal-and-history.md`
    §0 requires the `when` to be a clock reading, and 06:38:45Z is when the edit happened. Every
    other gate was run and is green, and `validate-workspace` is re-run immediately after this
    transition — its output is in the `**Result:**` below.
  - `every-criterion-has-a-test` → **pass** (all fourteen criteria have a row in
    `impl-report.md` `## Acceptance criteria evidence` naming a test function or a command with
    its output; none is demonstrated by reading code. Checked for sensitivity rather than
    existence: fourteen mutants, one per criterion, all fourteen make their named test fail.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0003 wi/WI-0003` → exit 0, all
    4 commits on `main..wi/WI-0003` name `WI-0003`.)
  - `no-unplanned-scope` → **pass** (advisory. `git diff main...HEAD --stat` → 8 files. Six are
    code and tests, every hunk tracing to a plan step; `docs/product/vision.md` is the one
    `to-update` row; `plan.md` is the disposition column, which is the only part of the plan this
    skill may write. The one hunk tracing to no criterion and no step is the `envel/dates.py`
    docstring reword, declared as deviation 3.)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0, *21
    consumed human answer(s) and 0 delegation(s) spent*, over a window of 1 changed path under
    `docs/` — the one document this execution wrote, so the window contained the sentence at risk.
    The `**Cross-answer check:**` bullet above is the read behind it.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0003` →
    exit 0. The **scope** it printed: *11 document(s) in 11 path(s) in scope — 1 path(s) differ
    from main (34e811c) under docs, plus 11 document(s) named by WI-0003's plan; citations: every
    markdown file in the workspace.* Not a window that could contain nothing: the changed path is
    `docs/product/vision.md`, the document actually repaired.)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule
    document-writes-are-declared --item WI-0003 --changed-since main` → exit 0, *1 document(s)
    written under docs/ on this branch; 11 named by the plan*. All twenty-seven invalidation
    entries carry a disposition: 24 `verified-still-true`, 2 `owned-by-ending`, 1 `to-update`.)
- **Artifacts:**
  - `envel/summary.py` (new), `tests/test_summary.py` (new)
  - `envel/dates.py`, `envel/cli.py`, `tests/test_dates.py`, `tests/test_cli.py` (changed)
  - `docs/product/vision.md` → **v3**, the one `to-update` row, with a change-log row
  - `tracker/items/WI-0003/artifacts/plan.md` — the disposition column, 27 rows
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - branch `wi/WI-0003`, commits `main..wi/WI-0003` = `29ccc3d`, `45c24f6`, `192db54`, `425b1c9`
  - no bug item filed, no question filed, no engagement-state section touched
- **Status:** `in-progress` → `verifying`
- **Result:** `envel summary` is built and every one of the fourteen criteria has a test that fails
  when the behaviour is removed. The four figures reconcile as a property of the arithmetic rather
  than by arrangement — nothing in `envel/summary.py` computes a carried-in figure and nothing
  there checks the identity; the test computes it independently over three envelopes across four
  months. 176 tests green on the branch head. Twenty-seven invalidation entries disposed, one of
  them a real repair: the vision said the balance was the summary's **third** column, written
  before `WI-0003/Q-001` put the moved figure ahead of it. `validate-workspace` was the only gate
  forced, for F-084, and it reports **0 errors** immediately after this entry exists — the error it
  raised was the absence of this entry.

## 2026-09-11T07:01:05Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next` as the highest-ranked runnable item.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the fourteen acceptance criteria, read **before** the
    implementation report, so that what would settle each one was derived from the criterion
  - `tracker/items/WI-0003/artifacts/plan.md` — the nine binding ADRs and the twenty-seven-row
    invalidation set, which are the subjects of two of this skill's gates
  - `tracker/items/WI-0003/artifacts/impl-report.md` — read as a claim to check, cited as evidence
    for nothing
  - `tracker/items/WI-0003/history.md`; `artifacts/refinement-qa.md` was not needed — no
    criterion's wording turned out to be contested
  - `docs/architecture/adr/ADR-0001` … `ADR-0009`, each opened at its `## Decision`
  - `docs/architecture/overview.md` and `docs/product/vision.md` — the two documents the
    invalidation set names, reopened sentence by sentence
  - the code at branch head **`6eb35e318f640e0c35d550c03ac07cc06c87e7f3`** on `wi/WI-0003`
  - `tracker/project.yaml` — the test and lint commands
- **Decisions:**
  - **All fourteen criteria pass, so there is no classification call to make** — nothing was sent
    back and no bug item was filed. The two things that could have looked like defects were
    classified and are recorded in `verify-report.md` `## Defects found`: the month-boundary race
    is the plan's own named risk with no criterion reaching it, and income's month being the typed
    one is AC8 working as specified on a limitation the stakeholder accepted at `WI-0003/Q-003`.
    Neither is this item's criteria failing, and neither is another item's delivered behaviour
    being wrong, so neither route applies.
  - **No criterion was judged ambiguous.** The one place two criteria could have contradicted each
    other is AC13's *"non-zero"* against AC14's exit code of 2; both sentences were quoted and read
    against the same run rather than against each other's summary, and they agree.
  - **The four figures were recomputed independently rather than checked against the tool's own
    arithmetic.** A script that reads the store's JSON and rebuilds *in*, *spent*, *moved* and
    *left* from the criteria's words — importing nothing from `envel.summary` — was compared
    against the printed rows for every envelope in every month of two stores, and it asserts AC3's
    identity itself. That is the difference between checking the code against itself and checking
    it against the criterion.
  - **The sensitivity mutations were designed here, not taken from the implementation report**, and
    deliberately boundary-flavoured — `<=` to `<`, `>` to `>=`, `nargs="?"` to `nargs="*"`, the
    folded sort key to the raw one, the two date fields swapped — so that the check is a second
    look rather than a re-run of the developer's.
  - **Two harness faults were classified as the harness's and not the item's**, which is the
    judgement call this execution came closest to getting wrong. Both are in
    `verify-report.md` `## Test sensitivity check` and in `**Commands:**` below.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `6eb35e318f640e0c35d550c03ac07cc06c87e7f3`
  - `python3 -m unittest discover -s tests -t .` → exit 0, **176 tests**;
    `python3 -m compileall -q envel tests` → exit 0
  - the criteria, each against a scratch `ENVEL_FILE`: `bin/envel summary`, `summary 2026-08`,
    `summary 2026-07`, `summary 2026-09`, `summary 2026-06`, `summary 2026-04`, `summary 2020-01`
    → exit 0 with the rows quoted in the report; `summary 2026-10`, `summary 2027-03` → exit 1,
    stderr, empty stdout; `summary 2026-8`, `08-2026`, `august`, `2026-13`, `2026-00`,
    `2026-08-01` → exit 1, empty stdout; `summary 2027-13` → the month-form message, so no row was
    computed; `summary --month 2026-08`, `summary 2026-08 extra`, `summary a b c` → exit 2,
    `usage: envel summary [-h] [YYYY-MM]`; `bin/envel` → exit 2,
    `usage: envel [-h] {new,add,list,spend,move,summary} ...`
  - the independent recomputation: `python3 -` over `/tmp/vfy/a.json` and `/tmp/vfy/c.json`,
    rebuilding the four figures from the criteria and asserting `left == carried_in + in − spent +
    moved` → exit 0, four months across two stores, **every one MATCH**, 12 (envelope, month)
    assertions
  - AC11 over output: 60 amount tokens across five stores matched against `^-?\d+\.\d\d$` and
    scanned for `£ $ € ,` → `violations: none`
  - AC13: ten invocations, one per criterion it names, all three streams read off each →
    `all ten as the convention requires: True`
  - AC10: `bin/envel summary | cut -d' ' -f1` against `bin/envel list | cut -d' ' -f1` → `diff`
    empty, `apples`/`Fun`/`zebra`
  - AC7: `bin/envel summary 2026-08` before and after `bin/envel new car` → `diff` empty
  - the invalidation enumerations: `ls envel/*.py`; `sed -n '13p' envel/cli.py`;
    `grep -n 'print(\|sys\.exit'` over the five modules below `cli` → exit 1, and the same grep
    over `cli.py` → 3, so it could have found a counterexample; `grep -n import envel/envelopes.py`
    → no `summary`; `grep -n 'ENVEL_FILE\|XDG\|store_path\|pathlib\|open(' envel/summary.py` →
    exit 1; `grep -rn 'int(whole)\|% 100\|// 100\|\* 100\|float(' envel/*.py` → 2, both `money.py`;
    `grep -rn 'socket\|urllib\|http\|requests\|ssl\|curses\|colorama' envel/ bin/envel` → exit 1;
    `md5sum` of a store before and after three summary runs → unchanged; a spend recorded with no
    `--on` → `on='2026-09-11'`, the boundary `ADR-0006` names; `od -c | grep -c '033'` → 0
  - `git diff main...HEAD --stat` → 13 files; `git diff main...HEAD -- docs/` → three hunks, all in
    `vision.md`, none in either `## Engagement state`
  - the sensitivity harness, **twice**: first run → 13 of 14 sensitive, AC11 reported insensitive;
    the same mutation run alone → the test fails with
    `AssertionError: 'in 1200.00' not found in 'groceries  in 120000  spent 0  moved 0  left 120000'`.
    Cause found by measurement: the AC10 and AC11 mutants are **both 4864 bytes** against a 4880-byte
    original and were written in the same second, so CPython reused AC10's cached bytecode.
    Re-run with `__pycache__` purged between mutations and `PYTHONDONTWRITEBYTECODE=1` → **14 of 14
    sensitive**
  - after that harness, `python3 -m unittest discover` → **17 failures, 2 errors** with a clean
    `git diff` — the same cache fault again, because `nargs="?"` → `nargs="*"` is a same-length
    replacement. `find . -name __pycache__ -type d -prune -exec rm -rf {} +` then
    `python3 -m unittest discover -s tests -t .` → exit 0, 176 tests, with no source change
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item
    WI-0003` → exit 1 once on a bare `conforms` for `ADR-0004`, then exit 0, *9 binding ADR(s), 9
    conformance row(s)*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item
    WI-0003` → exit 1 once with 22 errors while the rows named documents in shorthand, then exit 0,
    *27 invalidation entr(y/ies) against 27 row(s)*
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 176 tests, run by this execution against `6eb35e3` and again after the bytecode cache was purged.)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0.)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings. This is also the re-run that settles the gate `implement` forced: the F-084 error it reported was the absence of its own closing journal entry, and with that entry present the workspace validates. Checked before this transition, not inferred from it.)
  - `every-criterion-independently-checked` → **pass** (fourteen rows in `verify-report.md` `## Criteria`, each carrying a command this execution ran and its actual output. The implementation report is cited as evidence nowhere. AC3, the criterion most at risk of being checked against the code rather than against the criterion, was settled by an independent recomputation that imports nothing from `envel.summary`.)
  - `negative-cases-exercised` → **pass** (fifteen conditions triggered and their output read, not inferred: both sides of AC9's boundary on the day it was run, six malformed months including both ends of the `01`–`12` range, a valid date offered as a month, a month that is both unreadable and in the future, three wrong command lines, the empty case and the case AC4 says is **not** the empty case, and a store path that does not exist.)
  - `a-criterion-about-criteria-is-read` → **pass** (AC13 named ten criteria by ID and each got a per-criterion verdict read from its own sentence, in `verify-report.md` `## A criterion about criteria`. The one possible collision — AC14's exit 2 against AC13's *"non-zero"* — is resolved by quoting both. Non-intersection was checked and is **absent**: the evidence is one invocation per criterion with all three streams read off it, so every one of the ten is exercised together with AC13's claim rather than by the suite being green.)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0003` → exit 0, *9 binding ADR(s), 9 conformance row(s)*. Every row quotes a clause of that ADR's `## Decision` and names a file and line; the first run exited 1 on `ADR-0004`, which had the observation but no line, and that was a fair catch. No ADR outside the list was found engaged, and `find docs/architecture/adr -name '*.md'` → 9, so the list is complete by exhaustion.)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0003` → exit 0, *27 invalidation entr(y/ies) against 27 row(s)*. All 24 entries disposed `verified-still-true` were **reopened** and read against the branch head, with the enumeration and a falsifier for each quantified one; the `to-update` entry names a document that really was updated, to v3 with a change-log row; the two `owned-by-ending` entries were left alone and confirmed untouched by inspecting the diff's hunks.)
  - `tests-would-fail-without-the-change` → **pass** (advisory. Fourteen boundary mutations of this execution's own design, one per criterion, all fourteen making their named test fail — after the harness's own bytecode-cache fault was found and fixed.)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` (new)
  - `tracker/items/WI-0003/item.md` — **all fourteen** criteria ticked `- [x]`, each on a command
    this execution ran
  - no bug item filed, no question filed, **no file under `docs/` written** — `git diff` over
    `docs/` shows only `implement`'s own `vision.md` repair, which this execution read and did not
    touch
- **Status:** `verifying` → `in-review`
- **Result:** `WI-0003` passes verification on `6eb35e3`. Fourteen criteria, fourteen verdicts,
  every one from a command run here; nine binding ADRs conforming with a clause quoted and a line
  named for each; twenty-seven invalidation entries disposed and the twenty-four still-true ones
  reopened. The reconciliation at the centre of the item was checked by rebuilding the four figures
  from the criteria's own words and matching them against the tool's output for every envelope in
  every month of two stores. No defect was found. The two faults this execution did hit were its
  own harness's — a false negative from a bytecode-cache collision, and a workspace left looking
  broken by the same cause — and both are written up, because the second is the shape that would
  make a verifier send a sound item back.

## 2026-09-11T07:08:03Z — review-close v0.14.1 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next` as the highest-ranked runnable item.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (10 rows), `journal.md` **in full** (10 entries),
    `plan.md`, `impl-report.md`, `verify-report.md`, and all five `questions/Q-*.md` with their
    `## Consequences`
  - the diff `main..wi/WI-0003`, hunk by hunk — 13 files, 1333 insertions, 43 deletions, mapped
    in `review.md` `## What I examined`
  - `docs/architecture/adr/ADR-0001` … `ADR-0009`, `docs/architecture/overview.md`,
    `docs/product/vision.md` — the eleven documents, which is also the whole of `docs/`
  - `item.md` of `WI-0001` and `WI-0002`, opened for the two criteria D12's audit cites into
    (`WI-0002` AC11, `WI-0001` AC14)
- **Decisions:**
  - **Accept and close as `delivered`.** No criterion failed, nothing in the diff serves neither a
    criterion nor a plan step, and the record reconstructs without me.
  - **Three findings, none a send-back.** (1) The `envel/dates.py` docstring reword is the one hunk
    mapping to neither a criterion nor a step; examined and accepted because the old sentence —
    *"These three functions"* — was made false by the same commit, and it is source rather than
    `docs/`. (2) `verify`'s own mutation harness produced a false negative and then left the
    workspace showing 17 failures with a clean `git diff`; I checked the diagnosis rather than
    taking it, and the two mutants really are both 4864 bytes against a 4880-byte original, which
    is exactly what CPython's mtime-and-size bytecode check cannot distinguish inside one second.
    (3) One verification store is not one the tool could produce; declared, examined, accepted as
    gap G4.
  - **Seven gaps accepted, every one disposed `no-owner`, and I made that call deliberately rather
    than by default.** The one I weighed hardest is G1, the month-boundary race: it is real, and
    closing it means changing a signature `ADR-0009` states, for a fault that costs one refused
    invocation that succeeds on retry. Filing an item would put an ADR'd interface change on the
    board out of proportion to the fault; `no-owner` is the honest record, and the plan, the
    implementation report and the verification report all carry it. G6 is the other one worth
    naming: its owner *looks* like the human, and it is `no-owner` because they have already
    answered it — filing a question would re-ask something they declined in as many words.
  - **D13 is complete by exhaustion.** `find docs/architecture/adr -name '*.md'` → 9, and the plan
    names 9, so no ADR in this project can be engaged and unlisted.
  - **D7's open question has a mechanical answer here**, which is unusual and worth the sentence:
    the invalidation set names all **eleven** documents under `docs/`, so there is no document it
    does not name. F-087's question could not have caught anything on this item because the plan
    left it nowhere to hide.
  - **Merge, in the order the procedure requires**: trial first in a `--detach`ed worktree, close
    while the commit range is still non-empty, then the real merge and `record-merge`.
- **Cross-answer check:** this execution consumed **no** new human answer — no question was
  answered here and no sign-off was filed, the engagement being `active`. One prior pair was
  re-read, because `implement` edited a sentence sourced to one of them: `docs/product/vision.md`'s
  *"the summary's … column is a balance rather than a monthly remainder"* carries
  `[src: EP-001/Q-001]`, and the ordinal in it was made wrong by `WI-0003/Q-001`. I read both
  answers rather than accepting `implement`'s reading. `EP-001/Q-001` says money left in an
  envelope at the end of a month stays in that envelope — a claim about **carrying over**, which
  this item delivers and which the sentence still makes. `WI-0003/Q-001` added a *moved* column
  ahead of the balance — a claim about **which columns exist**. The two do not touch, so this was
  an ordinary repair of an ordinal and not a decision that was the stakeholder's, and `ADR-0008`
  §3's third row does not apply. Verdict: consistent.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → exit 0,
    *verified at 6eb35e31; wi/WI-0003 has moved to 61aea9be but only the record changed (5 file(s)
    under tracker/ or docs/)*
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, *all 6
    commit(s) on main..wi/WI-0003 name WI-0003*
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main`
    → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main`
    → exit 0, *21 consumed human answer(s) and 0 delegation(s) spent*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated
    --item WI-0003 --context work-item` → exit 0, *NOT APPLICABLE — an item close is not an ending*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable
    --item WI-0003` → exit 1 twice on the owner and disposition columns, then exit 0, *7 accepted
    gap(s)* over a **seven**-row table — the count read against the table rather than off the exit
    code, because `WI-0004`'s close found this rule silently dropping rows whose text began with
    the word "Nothing"
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed
    --item WI-0003` → exit 0, *27 entries against 27 rows*
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0003` → exit 0, not an epic
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → `active`, *still in flight:
    WI-0003, WI-0005, WI-0006*
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - the trial merge: `git rev-parse main` → `34e811c` before; `git worktree add --detach
    /tmp/wi0003-trial main`; `git -C /tmp/wi0003-trial merge --no-ff wi/WI-0003` → clean, merge
    result `c6854f6`; `python3 -m unittest discover -s tests -t .` **inside the trial** → exit 0,
    176 tests; `python3 -m compileall -q envel tests` in the trial → exit 0; `git worktree remove
    --force /tmp/wi0003-trial`; `git rev-parse main` → `34e811c`, **unmoved**
  - the record's mechanics: 10 journal entries against 10 history rows, matched pairwise by skill
    and timestamp; every `## Consequences` path on all five questions resolved on disk
  - the D12 audit, six claims opened from their citations: `item.md` AC2 in full (twice — for the
    four-figure count and order, and for the *"one net number, positive when more arrived"*
    sentence `ADR-0007` attributes to it); `WI-0002` AC11; `WI-0003` AC5; `ADR-0007` line 78;
    `envel/cli.py:13`; `envel/summary.py:54`. Boundary observations: `bin/envel summary 2026-09`
    → `groceries  in 0.00  spent 0.00  moved 0.00  left 60.00`, a balance where a monthly remainder
    would print `0.00`; `bin/envel summary 2026-08-01` → exit 1, a valid **date** refused as a
    month; `giver … moved -30.00` beside `taker … moved 30.00`, the same pair from both ends
  - the finding-2 check: `len()` of the two mutant sources → **4864** and **4864** against an
    original of **4880**
  - `find docs -name '*.md'` → 11; the paths named by the plan's invalidation set → the same 11;
    `find docs/architecture/adr -name '*.md'` → 9 against 9 binding ADRs
- **Gates:**
  - `definition-of-done` → **pass** (`review.md` `## Definition of Done` walks D1 to D13 with its own result and its own evidence for each. D3 examines the one forced transition rather than noting it: `implement`'s F-084 forcing is settled by `validate-workspace` exiting 0 and by the row's timestamp, 06:38:45Z, now sitting inside the window 06:30:02Z…06:47:20Z. D7 is a confirmation against the plan's 27-row set plus the question the set cannot answer, answered by enumerating `docs/` and finding the set exhaustive over it. D13 is complete by exhaustion at nine ADRs against nine.)
  - `engagement-state-is-restated` → **pass** (recorded as *not applicable* rather than passed: an item close is not an ending, and the sections are the ending's. `lint-documents --rule engagement-state-is-restated --item WI-0003 --context work-item` says so in as many words and exits 0. The two `owned-by-ending` invalidation entries were confirmed untouched by inspecting the diff's three hunks, none of which is in a `## Engagement state` section — worth doing here because `vision.md` **was** edited two sections away.)
  - `accepted-gaps-are-dispatchable` → **pass** (`lint-documents --rule accepted-gaps-are-dispatchable --item WI-0003` → exit 0, *7 accepted gap(s)* over a seven-row table, counted against the table. The first two runs exited 1 — the owner column took prose where it wants a skill, an item, `human` or `none`, and the disposition column took prose where it wants one of three tokens — so the reasoning moved to a fourth column and the tokens are now bare.)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0003 wi/WI-0003` → exit 0: verified at `6eb35e31`, the branch has since moved to `61aea9be` but only under `tracker/`, so the verification still covers the code. Run, not judged by eye.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0003 wi/WI-0003` → exit 0, all 6 commits on `main..wi/WI-0003` name `WI-0003`. Run before the merge, while the range is still non-empty.)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` run **inside** the detached trial worktree after `git merge --no-ff wi/WI-0003`, not on the branch: exit 0, 176 tests. `compileall` in the same worktree → exit 0. `git rev-parse main` returned `34e811c` both before and after, so the trial moved nothing.)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, run immediately before this transition and again after the gaps table was rewritten.)
  - `record-is-reconstructible` → **pass** (answered from the tracker, `docs/` and `git log` alone. *What was built and why* — one subcommand printing a month's four figures per envelope, because the stakeholder asked for a monthly summary in their opening statement and chose its columns at `EP-001/Q-003` and `WI-0003/Q-001`. *Which skill decided what* — `refine` took three rounds and three assumptions under no delegation, routing four design questions to `plan`; `plan` recorded `ADR-0008` and `ADR-0009` and settled the refusal order; `implement` took six declared deviations and one document repair; `verify` ticked nothing it had not run. *What questions arose and how they resolved* — five, all to the stakeholder across two rounds, every one answered with their words quoted in `refinement-qa.md` and propagated into named criteria. *What verification found* — fourteen passes, nine ADRs conforming, 27 entries disposed, no defect, and two faults in its own harness. None of that came from this conversation.)
  - `claims-are-sourced` → **pass** ((`lint-claims --context work-item --changed-since main` → exit)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0, *21 consumed human answer(s) and 0 delegation(s) spent*. The `**Cross-answer check:**` bullet above is the read; this execution consumed no answer of its own and re-read the one pair an edited sentence sits on.)
  - `epic-sign-off` → **pass** (not applicable in substance: `check-epic-signoff WI-0003` → exit 0, *WI-0003 is a 'work-item', not an epic*. `engagement-state EP-001` reports `active` with three items still in flight, so no ending is due and none was taken.)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` (new)
  - `tracker/items/WI-0003/item.md` — `outcome: delivered`, written by this transition
  - no bug item filed; no question filed; no file under `docs/` written by this execution
  - the merge commit is not named here because it does not exist yet: `scripts/record-merge` puts
    it in `item.md` once the real merge has happened
- **Status:** `in-review` → `done`
- **Result:** `WI-0003` is accepted and closed as `delivered`. Fourteen criteria settled with
  evidence, thirteen Definition-of-Done criteria each with their own result, no unrequested scope
  in the diff, nine binding ADRs complete by exhaustion, twenty-seven invalidation entries
  confirmed and D7's open question answered by enumeration — the set names all eleven documents in
  the project. Six absolute claims audited from their citations with a falsifier each and, where
  the rule has a boundary, at the boundary. Seven gaps accepted and every one disposed where the
  orchestrator can see it. 176 tests green on the merge result with `main` unmoved. `EP-001` stays
  `open`; closing this item makes `WI-0005` the next thing the board dispatches.
