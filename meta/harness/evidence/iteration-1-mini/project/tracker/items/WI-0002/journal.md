# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T02:08:03Z — intake v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this item was
  created by that execution
- **Inputs read:** `IDEA.md`; `tracker/project.yaml`; `.claude/agile-skills/spec/work-item.md`;
  `.claude/agile-skills/spec/ids-and-statuses.md`. No prior artifact existed for this item.
- **Decisions:** see `tracker/items/EP-001/journal.md`, same timestamp, for how the work was
  split and why this is one of the parts. For this item specifically: it delivers a recorded expense and a way to see what was recorded, with no arithmetic in it, and
  it is second, because it needs WI-0001's roster and store, and WI-0003 has nothing to compute over until it exists. Its acceptance criteria are deliberately left rough — they name what must be
  observable, not the command that would observe it — because the stakeholder has not yet
  answered the questions that decide them, and a polished criterion invented here would read as
  a decision nobody made. `refine` sharpens them.
- **Questions raised:** none on this item by this execution. The five open questions that bear on
  it are `EP-001/Q-001` … `EP-001/Q-005`.
- **Commands:** `python3 .claude/agile-skills/scripts/new-item --id WI-0002 …` → exit 0
- **Gates:** the four intake gates are evaluated once for the whole execution and recorded in
  full on `EP-001`: `workspace-valid` **pass**, `epic-has-success-measures` **pass**,
  `items-are-separable` **pass** (this item's order and dependency are named there),
  `no-solution-in-the-problem` **pass** (this item's title and story name no technology).
- **Artifacts:** `tracker/items/WI-0002/item.md` (new)
- **Status:** — → `draft`
- **Result:** Created at `draft` under EP-001, with the acceptance criteria intake could state
  honestly and no more.

## 2026-08-21T02:15:09Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, this item's owning status for `refine` per `pipeline.yaml`.
  Run directly rather than through `next`: `next` stops at orchestrator step 2 while the
  human-addressed questions on EP-001 are open, so it would never have dispatched this. Asking
  now is deliberate — the stakeholder answers between turns, and every question that can
  honestly be asked in this round trip saves a whole turn.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (the draft, AC1-AC5)
  - the item's history — one row, `- → draft` by `intake`; a fresh draft, not a send-back
  - `tracker/items/WI-0002/journal.md` — `intake`'s entry, which records that no verbatim
    stakeholder answers exist
  - `docs/product/vision.md` (v1)
  - `tracker/items/WI-0001/item.md` — WI-0001 owns the roster and the store, so this item's
    "person who paid" is a reference into it rather than a second concept
  - `tracker/items/WI-0003/item.md` — WI-0003 owns all arithmetic; this item must not compute
    balances, and its criteria do not
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Left AC1 and AC2 exactly as `intake` wrote them, despite both failing R4.** They fail
    because of `WI-0002/Q-002` (is the payer one of the sharers) and `EP-001/Q-001` (are shares
    always equal). Either could be made decidable by picking an answer, and picking would be a
    silent half-sized error in every balance the tool ever prints — the two readings of "Alice
    paid 30, shared by Bob and Carol" give 15 each and 10 each, and the difference is invisible
    in the output. This is the clearest case in the whole item for asking rather than assuming.
  - **Asked about the payer's share as its own question rather than folding it into
    `EP-001/Q-001`.** They look related — both are "how is this expense divided" — but Q-001 is a
    scope decision about the data model (equal or uneven), while this is a reading of the word
    "shared" that applies whatever the answer to Q-001 is. Folding them would have let one answer
    silently settle both.
  - **Asked about the amount format (Q-003) even though it looks like a design detail.** It is
    not: AC5 already promises to reject an amount that is "not a positive number", and that
    promise is undecidable until someone says whether `12.345` is a number this tool accepts.
    The related engineering point — that money must not be held as binary floating point, or the
    totals will not add up — is mine to decide, and is recorded in the question as such rather
    than asked.
  - **Did not ask what "everyone" looks like on the command line, or what the expense command is
    called.** Both are `plan`'s. AC2 requires only that a shorthand exists.
  - **Named an R10 gap I will close myself rather than ask about**: an expense that names an
    unknown person *and* carries an invalid amount hits AC3 and AC5 at once. Which error is
    reported first is a matter of implementation order, not of intent, so it is recorded in
    `artifacts/refinement-qa.md` as mine to specify at the next pass.
- **Questions raised:** `WI-0002/Q-001` (what an expense carries besides the arithmetic),
  `WI-0002/Q-002` (is the payer one of the sharers), `WI-0002/Q-003` (what a valid amount looks
  like). All blocking, all to `human`. Full record in `artifacts/refinement-qa.md`; all three
  `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 1 warning
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer …` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `scripts/validate-workspace` exit 0.
  - `definition-of-ready` (hard) → **fail**, per criterion: R1 pass, R2 pass, R3 pass,
    **R4 fail** (AC1/AC2 turn on Q-002 and `EP-001/Q-001`; AC4 on Q-001; AC5 on Q-003), R5 pass,
    **R6 fail** (three open blocking questions), R7 pass, R8 pass, R9 pass (considered splitting
    the listing into its own item and rejected it — a recording command you cannot see the output
    of delivers nothing observable), **R10 fail** (payer in or out; "everyone" versus a name
    list; more than two decimals; unknown person and bad amount together). Evidence per criterion
    in `artifacts/refinement-qa.md`. Not Ready, and not passed.
  - `criteria-are-decidable` (hard) → **fail** — AC3 is decidable today ("record an expense
    naming a person who was never added; expect a non-zero exit, a message naming them, and no
    new expense in the listing"). AC1, AC2, AC4 and AC5 are not, for the reasons under R4.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` holds all three
    questions tagged `[unresolved]`, the three questions deliberately not asked with the reason,
    and the per-criterion DoR table. Nothing paraphrased into agreement.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (new)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0002/item.md` (body unchanged; `updated` bumped by `transition`)
- **Status:** `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Not Ready. Three questions filed and the item suspended per `refine` precondition
  2. The one that matters most is Q-002: until it is answered, every balance this tool could
  print is ambiguous, and no amount of careful implementation would fix that.

## 2026-08-21T02:34:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`. Not dispatched by `next`: orchestrator step 2
  (`surface-human-questions`) stops the loop on any open human-addressed question and never
  reaches step 3. The stakeholder had answered all three questions in the files between sessions,
  and this skill's step 4 provides for `answered-by: human`, so it was started directly. The same
  precondition/step-4 disagreement is recorded on WI-0001's journal.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (all with `## Answer`
    filled in by the stakeholder)
  - `tracker/items/WI-0002/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `tracker/items/EP-001/item.md` and `EP-001/questions/Q-001.md` — the equal-split answer this
    item's AC1 had been deferring to
  - `tracker/items/WI-0001/item.md` (after this turn's amendments) — for the name-matching rule
    AC3 now shares
  - `tracker/items/WI-0003/questions/Q-002.md` — to confirm the rounding question is *not* what
    Q-003 answers
  - `docs/product/vision.md` (v2), `docs/architecture/adr/ADR-0001-…` (v1),
    `ADR-0002-…` (v1) — both written earlier in this turn; neither is contradicted here
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`, `spec/journal-and-history.md`
  - no `artifacts/plan.md` exists yet
- **Decisions:**
  - **Q-001 → a hybrid of options B and C.** Route: **recorded intent**. The stakeholder asked
    for B's back-dating and C's optional description in one sentence. Recording a single letter
    would have meant discarding half of what they said; the two properties do not conflict, so
    both are recorded. Rationale for not "picking the closest option": the options list is a tool
    for asking, not a menu the answer has to fit.
  - **Date format fixed as `YYYY-MM-DD`.** Route: **decided**. The record is silent and an AC
    saying "a date" is not decidable by someone with a terminal, which is the R4 failure this
    item already carries. Chosen because it is unambiguous between day-first and month-first
    conventions, sorts as text, and `date.fromisoformat` parses it on the ADR-0001 baseline.
    Reversible; tagged `[assumed]` in `refinement-qa.md`, not attributed to the stakeholder.
  - **Q-002 → option A, with the everyone case as the default and option C's guard.** Route:
    **decided, recorded as ADR-0003**. The stakeholder's answer is conditional — "*if* … it's
    shared by all of us" — and settles only the everyone case. Making "no sharers given" mean
    everyone-including-the-payer satisfies that case with fewer keystrokes than option B would
    have, while an explicit list keeps meaning exactly what it says, so "I paid for you two and
    walked" stays expressible. Option B was rejected because a command that silently means three
    people when it names two is the worse failure for a tool whose output is read aloud to the
    people it charges, and because it removes a capability rather than adding a keystroke.
  - **AC8's stderr note.** Route: **decided**. It is the mitigation that makes choosing A over B
    defensible: it converts A's silent error into a visible one, without making a legitimate
    "I did not share" into an error.
  - **Did not escalate Q-002, but flagged it loudly.** None of `spec/question.md` §4's four
    conditions holds for the case the stakeholder answered, and the residual case is reversible
    *today*. It stops being reversible the moment expenses are stored, because the record cannot
    distinguish "did not share" from "forgot to type my own name" — so the caveat is in
    `item.md` `## Notes` and in ADR-0003's Consequences, where `plan` and `implement` will read
    it, rather than only in the question file, which they do not read.
  - **Q-003 → option A.** Route: **recorded intent**, unambiguous. Folded into the existing AC5
    rather than added as a new criterion, so that "what is a valid amount" is defined in exactly
    one place and cannot drift.
  - **Amounts held as integer minor units, not floats.** Route: **decided**, forced by the
    combination of Q-003's "never silently change my number" and EP-001's success measure that
    the balances net to zero to the last minor unit. `12.10` has no exact binary float, so the
    two requirements are not simultaneously satisfiable in floating point. Recorded in the item's
    Notes rather than as an ADR because it is an implementation consequence of a decision already
    recorded, not a decision with live alternatives.
  - **AC3 now cites WI-0001 AC3's matching rule.** Route: **from the record** (WI-0001/Q-001's
    answer). Two commands resolving "alice" differently would be a defect nobody would find until
    a balance came out wrong.
- **Questions raised:** none on this item. The residual on Q-002 is recorded as `[unresolved]` in
  `refinement-qa.md` and as an open caveat in `item.md`, not as a new blocking question, because
  a decision exists and is safe until expenses are stored.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`, pre-existing; ADR-0001 §3 tells `plan` what to set)
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to draft --actor answer-questions`
    → see `**Status:**`. As on WI-0001, `transition`'s pre-move gate run reports
    `workspace-valid` FAIL because it evaluates gates against the pre-transition workspace — the
    item still `awaiting-answer` with its questions already `answered`, and a board not yet
    regenerated. `transition` states the gates are not blocking this move, makes it, and the
    post-move validation is clean. Recorded as a toolkit defect on WI-0001's journal.
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section reopened
    and checked: `item.md` AC1 states the equal split; AC2 states the no-sharers-means-everyone
    default, the exactly-those-named rule and the frozen sharer set; AC3 cites WI-0001's matching
    rule; AC4 shows date and description; AC5 states the two-decimal rule and "never rounded";
    AC6, AC7, AC8 are present; `## Notes` carries the confirm-before-implementation caveat and
    the integer-minor-units requirement. `ADR-0003-sharers-are-exactly-who-you-name.md` exists
    and is cited from AC2, AC8 and the Notes. `refinement-qa.md` carries all three answers
    verbatim.
  - `answered-from-the-record` → **pass**. Q-001 and Q-003 cite the stakeholder's own words;
    Q-002 cites their words for the case they covered and ADR-0003 for the case they did not,
    with the silence stated explicitly rather than papered over.
  - `escalation-is-justified` → **skipped**, no question was re-addressed to the human from this
    item. The nearest candidate, Q-002's residual, is recorded above with the reason it did not
    meet any of §4's conditions.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the move).
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft`; this
    execution transitioned to `draft`. All three blocking questions are answered.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — answered, each with
    file-level consequences
  - `tracker/items/WI-0002/item.md` — AC1–AC5 amended, AC6–AC8 added, `## Notes` replaced
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — "Answers received" section appended
  - `docs/architecture/adr/ADR-0003-sharers-are-exactly-who-you-name.md` (new)
- **Status:** `awaiting-answer` → `draft`
- **Result:** All three blocking questions answered, eight acceptance criteria now state
  behaviour a stranger with a terminal could check, and the one thing the stakeholder's words did
  not settle — an explicit sharer list that omits the payer — is decided in ADR-0003, guarded by
  AC8, and flagged for confirmation while it is still cheap to change. Back to `draft` for the
  second `refine` pass.

## 2026-08-21T03:46:54Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` (WI-0001 is now `done`; WI-0002 and WI-0003
  tie on priority-rank 2 and on `created`, so the ID tie-break selected this one)
- **Inputs read:**
  - `item.md` — the eight criteria as `answer-questions` left them, `## Out of scope`, `## Notes`
  - the item's transition record — three rows: created, suspended on Q-001..Q-003, resumed to
    `draft`. Read first, per the procedure: this is **not** a fresh draft and it is **not** a
    send-back from a later stage; it is a first refinement that was interrupted by the
    stakeholder's absence and has since been answered
  - `journal.md` — the `intake` and first-`refine` entries, and `answer-questions`'
  - `artifacts/refinement-qa.md` — both the original three questions and the propagated answers,
    so nothing already settled was re-opened
  - `questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all `answered`, `answered-by: human`
  - `docs/architecture/adr/ADR-0003-sharers-are-exactly-who-you-name.md` decisions 1–5
  - `docs/architecture/adr/ADR-0006-cli-surface-and-what-a-name-may-contain.md` decisions 2–6
  - `docs/architecture/adr/ADR-0002-one-store-file-per-user.md` decision 6
  - `tracker/items/WI-0001/item.md` — AC1, AC3, AC4, AC8, and its `## Deliberately unconstrained`
    section as the precedent for this item's
  - `tracker/items/WI-0001/artifacts/review.md` — F6, the handover this item inherits
  - `tracker/items/WI-0003/item.md` — checked for scope overlap; the balances belong there and
    nothing in this pass moved toward them
  - `.claude/agile-skills/spec/dor-dod.md` §1, `.claude/agile-skills/spec/question.md`
- **Decisions:**
  - **Asked three questions and no more.** The stakeholder is not in this session, so every
    question costs a full turn; the discipline applied was `spec/question.md` §4 — escalate only
    for intent no document records, irreversibility, contradiction of an ADR, or a genuinely
    silent record where any choice has material consequences. Q-004 qualifies on the first two,
    Q-005 and Q-006 on the fourth. Seven further gaps found in this pass did **not** qualify and
    were decided here instead, each marked in the criterion as assumed by `refine`.
  - **Q-004 is the one that had to be asked.** `## Notes` has carried it as "confirm rather than
    assume" since the first answers were propagated, addressed to *"anyone planning or
    implementing this item who has the stakeholder's attention"* — but `implement` and `plan` may
    not ask, and `refine` is the only skill on this item that may. A note asking someone who
    cannot ask is a gap that would never have closed itself. Filed with the irreversibility
    stated: once expenses are stored, the data cannot distinguish "did not share" from "forgot to
    type my own name".
  - **Q-005 is a real R4 failure, not tidiness.** AC4 gives no listing order, and the
    stakeholder's own "catching up days later" makes entry order and date order routinely differ,
    so the criterion is genuinely undecidable. AC9's empty-listing default is folded into the same
    question rather than filed as a fourth.
  - **Seven things decided rather than asked**, listed with their derivations in
    `refinement-qa.md`: the two-decimal display form and the roster spelling in AC4; what counts
    as a number in AC5; control characters in a description in AC6 (from `ADR-0006` decision 5's
    own reasoning); the empty listing in AC9; the fault-reporting order in AC10 — which the first
    pass had already committed `refine` to specifying itself; and AC11's duplicate-sharer rule,
    which is not an assumption at all but a consequence of WI-0001 AC3 and therefore something
    `spec/question.md` §4 forbids escalating.
  - **AC10 turns WI-0001's F6 handover into a criterion of this item.** WI-0001's review recorded
    that `store.load()` validates roster entries but not expense records, and named WI-0002 as the
    owner because only this item knows what an expense record is. A handover that lives in a
    closed item's accepted-gaps list is one re-read away from being lost; a criterion is not.
  - **AC10 also restates the no-traceback rule for this item's commands.** WI-0001 AC8 scoped
    itself to WI-0001's two commands by design, so EP-001's fourth success measure has no cover
    over `add-expense` and `expenses` unless this item claims it. Added with the reason stated in
    the criterion.
  - **`## Deliberately unconstrained` added**, following WI-0001's precedent, naming five gaps and
    who left each open — the command spellings (`plan`/`ADR-0006`), size limits, currency,
    duplicate expenses, and what happens to an expense naming a person later removed. It also
    lists the combinations that **are** specified, so that R10's check is auditable rather than
    asserted.
  - **R10 recorded as failing anyway**, on one combination: the everyone shorthand given together
    with an explicit name list. R10 only requires a combination to be *visible*, and it is — but
    the item states no behaviour for a command a user can type, and calling that a pass would be
    the quiet kind of pass this gate exists to prevent. Named as `plan`'s to settle with the flag
    spellings rather than made into a fourth question, because it is a consequence of a CLI shape
    that does not exist yet.
  - **Nothing already answered was re-opened.** Equal shares, the everyone default, the two-decimal
    rule, the optional description and the settable date are the stakeholder's and were left
    alone. The procedure names re-refining as one of the two ways this skill goes wrong.
  - **No override sought or recorded.** The stakeholder is not present to give one, and writing an
    override on their behalf is what `spec/dor-dod.md` §1 exists to make impossible to do quietly.
- **Questions raised:** three, all blocking and addressed to `human` — `Q-004` (the `ADR-0003`
  confirmation; intent and irreversibility), `Q-005` (the expense listing's order, with AC9's
  empty-listing default folded in), `Q-006` (dates in the future). Full text and options in
  `artifacts/refinement-qa.md` `## Second refine pass`. Three earlier questions, `Q-001`–`Q-003`,
  remain `answered` and were not touched.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --actor refine
    --resume-to draft --reason "…"` → exit 0; it regenerates the board and re-validates
- **Gates:**
  - `workspace-valid` → **fail at gate time, pass after the transition**, and the sequence is
    worth recording rather than rounding to either end. It passed at the start of this execution
    (exit 0, 0 errors, 0 warnings). When the transition script re-ran it, immediately after the
    three question files were written and before the status moved, it reported two errors —
    `board.stale`, and `question.blocking.not-suspended` on this item, *"an open blocking question
    exists but the item is 'draft'"*. Both describe the half-second in which the questions existed
    and the suspension had not yet happened; neither is a defect in the workspace. The script said
    so itself — *"gates reported above are NOT blocking this move; refine only gates its
    completion transition (to 'ready'), and this is 'awaiting-answer'"* — and its own closing
    `validate-workspace` reported 0 errors, 0 warnings. Recorded this way because a gate line
    reading "pass" would hide a real transient that a reader of the tool's output would see.
  - `definition-of-ready` → **fail**, recorded criterion by criterion, not as a verdict. R1 pass,
    R2 pass, R3 pass, **R4 fail** (AC4 alone, on the listing order — down from four failing
    criteria in the first pass), R5 pass, **R6 fail** (Q-004..Q-006 open and blocking, the
    expected state of a suspended item), R7 pass (WI-0001 is `done`), R8 pass, R9 pass,
    **R10 fail** (one combination named but unsettled). The full table with evidence is in
    `artifacts/refinement-qa.md`. This is why the item goes to `awaiting-answer` and not to
    `ready`.
  - `criteria-are-decidable` → **fail, on one criterion**. Ten of eleven name a command to run and
    the verdict that follows; AC4 does not, because the listing order is undecided. Recorded as a
    failure rather than rounded up: the gate asks whether *each* AC is decidable, and one is not.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` carries both passes. The three
    new questions are `[unresolved]` because no answer has been received; the seven decisions this
    pass made itself are tagged `[assumed]` with their derivations, and the two resolved from the
    record are labelled as such rather than as assumptions. The first pass's `[unresolved]` markers
    are left as written, since the file records an exchange rather than being a form to correct.
- **Artifacts:**
  - `questions/Q-004.md`, `questions/Q-005.md`, `questions/Q-006.md` (new, blocking, to `human`)
  - `item.md` — AC4, AC5 and AC6 tightened; AC9, AC10 and AC11 added; `## Notes` rewritten around
    the three open questions; `## Deliberately unconstrained` added
  - `artifacts/refinement-qa.md` — `## Second refine pass` appended, with the per-criterion DoR
    table
  - the board, regenerated by the transition script
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** Not Ready, and suspended on the stakeholder rather than on a guess. Seven of the
  gaps this pass found were closed here and are marked as `refine`'s work rather than the
  stakeholder's; three were not `refine`'s to close and are now blocking questions. The item is in
  materially better shape than the first pass left it — eleven criteria instead of eight, one R4
  failure instead of four — and the single thing that has blocked it since the first answers
  landed, the `ADR-0003` confirmation, has finally been asked by the only skill permitted to ask
  it.
