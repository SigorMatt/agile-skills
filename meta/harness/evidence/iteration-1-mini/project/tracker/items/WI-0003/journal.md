# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T02:08:03Z — intake v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this item was
  created by that execution
- **Inputs read:** `IDEA.md`; `tracker/project.yaml`; `.claude/agile-skills/spec/work-item.md`;
  `.claude/agile-skills/spec/ids-and-statuses.md`. No prior artifact existed for this item.
- **Decisions:** see `tracker/items/EP-001/journal.md`, same timestamp, for how the work was
  split and why this is one of the parts. For this item specifically: it delivers the answer to the question the stakeholder actually asked — who owes whom — and it is the only item where netting and rounding live, and
  it is third, because it computes over the expenses WI-0002 records. Its acceptance criteria are deliberately left rough — they name what must be
  observable, not the command that would observe it — because the stakeholder has not yet
  answered the questions that decide them, and a polished criterion invented here would read as
  a decision nobody made. `refine` sharpens them.
- **Questions raised:** none on this item by this execution. The five open questions that bear on
  it are `EP-001/Q-001` … `EP-001/Q-005`.
- **Commands:** `python3 .claude/agile-skills/scripts/new-item --id WI-0003 …` → exit 0
- **Gates:** the four intake gates are evaluated once for the whole execution and recorded in
  full on `EP-001`: `workspace-valid` **pass**, `epic-has-success-measures` **pass**,
  `items-are-separable` **pass** (this item's order and dependency are named there),
  `no-solution-in-the-problem` **pass** (this item's title and story name no technology).
- **Artifacts:** `tracker/items/WI-0003/item.md` (new)
- **Status:** — → `draft`
- **Result:** Created at `draft` under EP-001, with the acceptance criteria intake could state
  honestly and no more.

## 2026-08-21T02:15:09Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, this item's owning status for `refine` per `pipeline.yaml`.
  Run directly rather than through `next`: `next` stops at orchestrator step 2 while the
  human-addressed questions on EP-001 are open, so it would never have dispatched this. Asking
  now is deliberate — the stakeholder answers between turns, and every question that can
  honestly be asked in this round trip saves a whole turn.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (the draft, AC1-AC4)
  - the item's history — one row, `- → draft` by `intake`; a fresh draft, not a send-back
  - `tracker/items/WI-0003/journal.md` — `intake`'s entry; no verbatim stakeholder answers exist
  - `docs/product/vision.md` (v1) — its "answering one question well: who owes whom" is the
    sentence this item is measured against
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — this item computes over
    what they store and must add no new stored concept
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Worked the four-person example out by hand before filing Q-001, and put all three outputs
    in the question.** "Who owes whom" reads three ways — pairwise, net per person, settlement —
    and an abstract question about "the output format" would have got an abstract answer. Showing
    the stakeholder the three actual outputs side by side is what makes this answerable in one
    round trip instead of two.
  - **Found that AC2 does not disambiguate, and said so rather than relying on it.** The
    Alice/Bob/Carol example `intake` wrote prints identically under all three readings, so it
    looked like a criterion that pinned the output and is not. Recorded in the question, because
    a later reader would otherwise reasonably conclude the format was already decided.
  - **Ruled out one of Q-002's options myself rather than presenting it neutrally.** Keeping
    exact fractions internally and rounding only at print time is a real approach, and it is
    incompatible with this item's own AC3 (the printed amounts must net to zero to the last minor
    unit). It is listed so the option is on the record with the reason it fails, rather than
    omitted and re-proposed later.
  - **Did not ask how balances are computed.** That is arithmetic, `plan` owns it, and AC3
    constrains it. Nor did I ask about the wording of the output: AC2 pins the numbers and the
    pairs, which is the part that can be wrong.
  - **Named an R10 gap I will close myself**: a person in the group who has neither paid for nor
    shared anything — do they appear with a zero or not at all? That follows from whichever
    output form Q-001 picks, so it is recorded in `artifacts/refinement-qa.md` as mine to specify
    at the next pass rather than asked now.
- **Questions raised:** `WI-0003/Q-001` (what the report prints), `WI-0003/Q-002` (who absorbs
  the rounding remainder). Both blocking, both to `human`. Full record in
  `artifacts/refinement-qa.md`; both `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 1 warning
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to awaiting-answer …` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `scripts/validate-workspace` exit 0.
  - `definition-of-ready` (hard) → **fail**, per criterion: R1 pass, R2 pass, R3 pass,
    **R4 fail** (AC1 does not say what form the statement takes — Q-001; AC3 needs a rounding
    rule — Q-002), R5 pass, **R6 fail** (two open blocking questions), R7 pass, R8 pass, R9 pass,
    **R10 fail** (uneven division; a person with no expenses at all). Evidence per criterion in
    `artifacts/refinement-qa.md`. Not Ready, and not passed.
  - `criteria-are-decidable` (hard) → **fail** — AC2 and AC4 are decidable today ("record the
    stated dinner and read three numbers"; "run the report on an empty store and expect exit 0
    and a statement that nobody owes anybody"). AC1 and AC3 are not, for the reasons under R4.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` holds both questions
    tagged `[unresolved]`, the three questions deliberately not asked with reasons, and the
    per-criterion DoR table. Nothing paraphrased into agreement.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` (new)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0003/item.md` (body unchanged; `updated` bumped by `transition`)
- **Status:** `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Not Ready. Two questions filed and the item suspended per `refine` precondition 2.
  Q-001 decides what this item's output actually is, and nothing sensible can be designed or
  built here until it comes back.

## 2026-08-21T02:36:40Z — answer-questions v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer`. Not dispatched by `next`: orchestrator step 2
  (`surface-human-questions`) stops the loop on any open human-addressed question and never
  reaches step 3. The stakeholder had answered both questions in the files between sessions, and
  this skill's step 4 provides for `answered-by: human`. Same precondition/step-4 disagreement
  recorded on WI-0001's journal.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` (both answered by the stakeholder)
  - `tracker/items/WI-0003/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `tracker/items/EP-001/questions/Q-002.md` and `Q-005.md` — the deferral of settling up, and
    the stakeholder's definition of success; both bear directly on this item's output
  - `tracker/items/WI-0002/questions/Q-003.md` — the never-silently-round rule that constrains
    the arithmetic here
  - `tracker/items/EP-001/item.md`, `docs/product/vision.md` (v2)
  - `docs/architecture/adr/ADR-0001-…`, `ADR-0002-…`, `ADR-0003-…` (all v1, written earlier this
    turn); none is contradicted by what is decided here
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`, `spec/journal-and-history.md`
  - no `artifacts/plan.md` exists yet
- **Decisions:**
  - **Q-001 → option D (payments, with net positions alongside).** Route: **recorded intent**.
    Both halves are in the stakeholder's sentence.
  - **The net-position summary is required (AC5), not optional.** Route: **recorded intent**, from
    a different question. The stakeholder hedged it here — "fine too if that's easy" — but
    `EP-001/Q-005` gave *"nobody argues about it"* as their definition of success, and the net
    line is the only part of the output somebody at the table can check against their own memory.
    Making it optional would leave that success measure unobservable. Reading two answers together
    rather than each in isolation is the point of triaging every open question at once.
  - **The item does not claim minimality.** Route: **decided**. The question offered "the smallest
    set of payments"; minimising transfers is NP-hard, so a criterion using that word is not
    decidable by someone with a terminal and could not be falsified by a verifier without solving
    the same problem. AC7 claims the `k − 1` bound and determinism instead, and `## Out of scope`
    forbids the claim appearing in the output or the help text. This is a correction to the
    question's wording, not to the stakeholder's answer, and it is recorded as such.
  - **Greedy largest-first matching, ties broken by name — ADR-0005.** Route: **decided, recorded
    as an ADR**. The stakeholder chose the output's shape and the record is silent on how it is
    produced. Exact minimisation was rejected on cost and on predictability; unnetted pairwise
    debts were rejected by the stakeholder. The name tie-break is there so two runs cannot print
    different things and give the group something new to argue about.
  - **Net positions are a separate stage from settlement — ADR-0005 decision 1.** Route: **from
    the record**. `EP-001/Q-002`'s accepted option promised this item would be built knowing
    repayments are coming. Computing payments straight from expense rows would pass every
    criterion here and quietly break that promise, so the constraint is written into the item's
    Notes and the ADR where an implementer will meet it.
  - **Q-002 → option A (the payer absorbs the remainder) — ADR-0004.** Route: **decided, recorded
    as an ADR**, on an explicit delegation. Leaving it open was not available: AC3 requires the
    figures to net to zero to the last minor unit, and `10.00` split three ways forces the
    question. Option C is excluded by AC3 itself. A over B on the question's own reasoning.
  - **Deciding on "we'll decide later" rather than escalating.** Route note. `spec/question.md` §4
    condition 2 (irreversibility) is the one that could have applied, and it does not: the
    remainder rule is applied at report time and never persisted, so switching to B later is one
    function, one ADR and one criterion, with no migration. ADR-0004's Consequences say this
    explicitly, so the stakeholder's "later" is genuinely still available. Had the rule been baked
    into stored data, escalation would have been the honest answer, because "later" would already
    have passed.
  - **Money is integer minor units, never a binary float — ADR-0004 decision 1.** Route:
    **decided**, forced by `WI-0002/Q-003` (never silently change the user's number) plus AC3
    (net to zero exactly). `12.10` has no exact binary float, so the two are not simultaneously
    satisfiable in floating point. This is why AC3 becomes a property of the arithmetic rather
    than something checked case by case.
  - **AC4 extended to the all-nets-zero case.** Route: **decided**. It previously covered only "no
    expenses recorded"; a store full of expenses that happen to net out is the same output and was
    unspecified.
- **Questions raised:** none on this item.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`, pre-existing; ADR-0001 §3 tells `plan` what to set)
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to draft --actor answer-questions`
    → see `**Status:**`. Same pre-move gate artefact as WI-0001 and WI-0002: `workspace-valid` is
    reported FAIL against the pre-transition workspace, `transition` states the gates are not
    blocking this move, and the post-move validation is clean. Recorded as a toolkit defect on
    WI-0001's journal.
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section reopened
    and checked: `item.md` AC1 requires one command printing the payments; AC4 covers the
    all-zero case; AC5 requires the net-position summary; AC6 states the remainder rule with the
    worked example and the two-decimal rule; AC7 states the `k − 1` bound and determinism;
    `## Out of scope` forbids claiming minimality and records repayments as deferred; `## Notes`
    is replaced. `ADR-0004-payer-absorbs-the-rounding-remainder.md` and
    `ADR-0005-settlement-by-greedy-largest-first-matching.md` exist and are cited from AC6, AC7
    and the Notes. `WI-0002/item.md` `## Notes` carries the integer-minor-units requirement.
    `docs/product/vision.md` is at v2 with both ADRs named. `EP-001/item.md` carries the amended
    scope bullet and the two new success measures. `refinement-qa.md` carries both answers.
  - `answered-from-the-record` → **pass**. Q-001 cites the stakeholder's words plus
    `EP-001/Q-005` for the summary being required, and states plainly that the algorithm was
    silent in the record and is now ADR-0005. Q-002 states that the stakeholder declined to
    choose and records ADR-0004 as the architect's decision, not theirs.
  - `escalation-is-justified` → **skipped**, no question was re-addressed to the human from this
    item. Q-002 was the candidate; the reason it did not meet §4 condition 2 is recorded under
    `**Decisions:**` above, with the fact that stands behind it (nothing is persisted).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the move).
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft`; this
    execution transitioned to `draft`. Both blocking questions are answered.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — answered, with file-level
    consequences
  - `tracker/items/WI-0003/item.md` — AC1 and AC4 amended, AC5–AC7 added, `## Out of scope` and
    `## Notes` rewritten
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — "Answers received" appended
  - `docs/architecture/adr/ADR-0004-payer-absorbs-the-rounding-remainder.md` (new)
  - `docs/architecture/adr/ADR-0005-settlement-by-greedy-largest-first-matching.md` (new)
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both questions answered — one from the stakeholder's choice, one from their explicit
  delegation — and the two things their answers did not settle, the settlement algorithm and the
  remainder rule, decided as ADR-0005 and ADR-0004. The item now states what the tool actually
  guarantees rather than the unachievable "smallest set of payments" the question had offered.
  Back to `draft` for the second `refine` pass.

## 2026-08-21T03:52:55Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`. Run in the same turn as WI-0002's refinement, deliberately: the
  stakeholder is asynchronous, every question costs a full turn of the pipeline, and the harness
  instruction to file every question for them across every reachable item before stopping is worth
  more than the strict one-action-per-`next` cadence here. The orchestrator would otherwise have
  stopped on WI-0002's new questions and left this item unrefined for a turn, for nothing.
- **Inputs read:**
  - `item.md` — the seven criteria as `answer-questions` left them, `## Out of scope`, `## Notes`
  - the item's transition record — three rows: created, suspended on Q-001 and Q-002, resumed to
    `draft`. Read first: this is an interrupted first refinement that has since been answered, not
    a fresh draft and not a send-back from a later stage
  - `journal.md` — the `intake`, first-`refine` and `answer-questions` entries
  - `artifacts/refinement-qa.md` — both the original questions and the propagated answers
  - `questions/Q-001.md`, `Q-002.md` — both `answered`, `answered-by: human`
  - `docs/architecture/adr/ADR-0004-payer-absorbs-the-rounding-remainder.md` decisions 1–2
  - `docs/architecture/adr/ADR-0005-settlement-by-greedy-largest-first-matching.md` decisions 1–3
  - `docs/architecture/adr/ADR-0002-one-store-file-per-user.md` decision 6
  - `docs/architecture/adr/ADR-0006-cli-surface-and-what-a-name-may-contain.md` decision 2
  - `tracker/items/WI-0001/item.md` AC8 and `tracker/items/WI-0002/item.md` AC3, AC10 — to find
    what those items' criteria do and do not cover, which is how AC8 and AC9 were scoped
  - `.claude/agile-skills/spec/dor-dod.md` §1, `.claude/agile-skills/spec/question.md` §4,
    `.claude/agile-skills/spec/work-item.md` frontmatter rules, `.claude/agile-skills/pipeline.yaml`
- **Decisions:**
  - **Asked the stakeholder nothing, and that is the finding.** Every gap found here was derivable
    from an answer they have already given, a consequence of the output form they chose in Q-001,
    or a mistake `refine` itself made. `spec/question.md` §4 forbids escalating because answering
    is effortful, and none of the six things settled below meets any of its four grounds. Refining
    WI-0002 minutes earlier produced three questions that genuinely belong to the stakeholder; the
    contrast is what makes "no questions" a result rather than a shortcut.
  - **Found and fixed a contradiction between AC2 and AC5.** AC2 required the output to state the
    two payments *"and nothing else"*; AC5, added in the same propagation, requires a net-position
    summary alongside them. An implementation could satisfy one or the other, and `verify` would
    have had to pick. Scoped *"nothing else"* to the payments — exactly two, no third, no other
    pair — which is plainly what the phrase was for, and said so in AC2's own text so the
    correction is visible rather than silent. This is the kind of defect that only surfaces when
    someone reads all the criteria against each other, which is this pass's job.
  - **Settled the gap the first pass explicitly left to itself.** That pass wrote that whether an
    inactive group member appears in the output was *"mine to specify once Q-001 fixes the output
    form, since it follows from the form rather than from intent"*. The form is fixed, so it is
    specified: everyone in the group appears, including at `0.00`. The reasoning is the
    stakeholder's own justification for the summary — *"so that a reader can reconcile the
    payments against what they remember paying"* — which is worthless to a reader who has been
    omitted.
  - **Required the direction of a net position to be stated in words.** Without it `Alice 20.00`
    is unreadable and AC5 is not decidable. It constrains meaning, not phrasing; the first pass
    deliberately left the wording open and this pass keeps it open.
  - **AC8 added: the no-traceback discipline, restated for this item's command.** WI-0001 AC8 and
    WI-0002 AC10 each scope themselves to their own commands by design, so EP-001's fourth success
    measure covers the settlement command only if this item claims it. Also states that this
    command never writes, so the store's bytes are unchanged after every invocation — a stronger
    and cheaper check than the other two items could make.
  - **AC9 added: an expense naming somebody outside the group is fatal.** This is the *referential*
    half of the check WI-0002 AC10 adds to `store.load()`; WI-0002 validates the shape of an
    expense record, not whether the names in it still resolve, and neither earlier item owns this.
    Chose fatal over silently including or dropping: a settlement naming somebody who is not in
    the group produces payments nobody can act on. Reversible.
  - **`depends-on: WI-0002` recorded in the frontmatter.** The first pass had only `relates-to` and
    argued the sequencing fell out of the priority tie-break. That was true about ordering and
    silent about runnability: with only a `relates-to`, the orchestrator would dispatch `plan` on
    this item as soon as it turned `ready`, and that plan would be designed against an
    expense-record shape WI-0002's plan has not decided. The dependency makes `pipeline.yaml`'s
    runnable rule enforce mechanically what the first pass could only hope for. This item is now
    Ready **and deliberately not runnable**, which are different things.
  - **`## Deliberately unconstrained` added**, per R10 and following WI-0001's practice: four gaps
    with who left each open — the report's wording and layout, the command's name, size limits,
    filtering — and nine combinations listed as specified, including two named as arithmetically
    impossible or handled upstream rather than left silent.
  - **Nothing already answered was re-opened.** The settlement-plus-summary form, the
    payer-absorbs-the-remainder rule, the deferral of settling up and the refusal to claim
    minimality are the stakeholder's or come from ADRs they delegated to.
  - **No override sought or recorded**, and none was needed: all ten Definition of Ready criteria
    are met on evidence.
- **Questions raised:** none. `Q-001` and `Q-002` remain `answered` and were not touched. The
  reasoning for asking nothing is in `artifacts/refinement-qa.md` `## Second refine pass`, and the
  six things settled instead are each tagged `[assumed]` there with their derivation.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 once, reporting
    `board.stale` after `depends-on` changed the board's "blocked by" column; `board-gen` → wrote
    the board; re-run → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to ready --actor refine
    --reason "…"` → exit 0
- **Gates:**
  - `workspace-valid` → **pass**, after one honest failure. Adding `depends-on: WI-0002` changed
    what the board must show, so `validate-workspace` reported `board.stale` until `board-gen` was
    run. Recorded rather than smoothed over: the failure was real, it was caused by this
    execution, and the fix was the one the validator's own hint named.
  - `definition-of-ready` → **pass**, recorded criterion by criterion. R1 pass, R2 pass, R3 pass,
    **R4 pass** (the first pass's two failures closed by the stakeholder's answers and `ADR-0004`;
    the two that would have replaced them closed by this pass), R5 pass, **R6 pass** (no question
    on this item is open and this pass filed none), **R7 pass** and now mechanically rather than by
    argument, R8 pass, R9 pass, **R10 pass**. The table with per-criterion evidence is in
    `artifacts/refinement-qa.md`.
  - `criteria-are-decidable` → **pass**. All nine are tabulated in `refinement-qa.md`
    `## Every acceptance criterion, and how it is decided`, each naming the store to build, the
    command to run and the verdict that follows. AC5's row is the one worth checking: it adds a
    fourth person who is named in nothing, because that is the case the criterion was widened to
    cover and a three-person example would not exercise it.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` carries both passes. No answer
    was received in this one, so nothing is tagged `[human]` here; the six decisions this pass made
    are tagged `[assumed]` with their derivations, and the `depends-on` change is recorded as a
    dependency rather than dressed up as an assumption. The first pass's `[unresolved]` markers are
    left as written — the file records an exchange rather than being a form to correct.
- **Artifacts:**
  - `item.md` — `depends-on: WI-0002` added; AC2 corrected and AC5 widened; AC8 and AC9 added;
    `## Notes` extended with the dependency's reasoning; `## Deliberately unconstrained` added
  - `artifacts/refinement-qa.md` — `## Second refine pass` appended, with the decidability table
    and the per-criterion DoR table
  - the board, regenerated
- **Status:** `draft` → `ready`
- **Result:** Ready, on all ten Definition of Ready criteria, with no questions filed and no
  override. Nine criteria, every one decidable by a named command; a contradiction between AC2 and
  AC5 found and fixed before it reached `verify`; and the dependency on WI-0002 recorded in
  frontmatter so the orchestrator will hold this item back until there is an expense record to
  design against. It is Ready and deliberately not yet runnable.
