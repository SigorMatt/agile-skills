# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T18:54:29Z — intake v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** not dispatched by `next`. The human's answer to `EP-001/Q-001` widened the epic's
  scope to include settling up. `answer-questions` propagated that scope change into the epic and
  the vision, and then ran `intake`'s item-creation procedure for the one item the change implies,
  because `pipeline.yaml` permits an item to be created at `draft` only with `actor: intake`. Both
  executions are journalled: the decision to widen the scope is on EP-001, the creation of this
  item is here.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` — the question, its three options, and the human's
    answer verbatim
  - `tracker/items/EP-001/item.md` — the epic's goal, scope and out-of-scope list, as amended by
    the same batch
  - `tracker/items/WI-0003/item.md` — to place the dependency and avoid duplicating what that item
    already promises
  - `tracker/items/WI-0002/item.md` — for the shape and roughness of a sibling's criteria
  - `docs/product/vision.md` (v2)
  - `.claude/agile-skills/spec/work-item.md`, `.claude/agile-skills/pipeline.yaml`
- **Decisions:**
  - **One item, not two.** Recording a payment and netting it off the balances could be split, but
    recording a payment nobody can see the effect of is not observable on its own — the same
    reasoning `intake` used when it declined to make persistence its own item.
  - **Depends on WI-0003, not the reverse.** AC4 and AC5 are statements about WI-0003's output, so
    that item's criteria must be settled first. WI-0003 stays demonstrable over expenses alone.
  - **Criteria written at intake roughness.** AC1 to AC6 name the observable outcome and
    deliberately do not name a command, because the command surface was an open question when this
    item was created. `refine` makes them decidable, as it must for WI-0001 to WI-0003.
  - **Stated AC4 as a difference, not an absolute.** "The payer owes that much less" is checkable
    against a before-and-after pair of outputs without committing to how a balance is displayed,
    which is WI-0003's decision to make.
  - **Excluded a "settle everyone" reset explicitly.** It was option C of `EP-001/Q-001` and was
    not chosen; recording the rejected alternative in `## Out of scope` is what stops it being
    re-proposed later as an obvious missing feature.
  - **Excluded deleting or amending a payment**, by the same reasoning the epic uses to exclude
    correcting an expense. A payment and an expense are both recorded facts; admitting corrections
    for one and not the other would be arbitrary.
- **Questions raised:** none. Everything this item needed from the human was already asked and
  answered on `EP-001/Q-001`; the questions that remain open across the epic are about the command
  surface and the arithmetic, and they are already filed on WI-0001 and WI-0002.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --next-id work-item` -> `WI-0004`
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0004 ... --actor answer-questions`
    -> exit 0, but `validate-workspace` then failed with
    `history.transition.illegal: None -> draft by 'answer-questions' is not a transition in
    pipeline.yaml`. The item was removed and recreated with `--actor intake`; see the toolkit note
    on EP-001's journal entry.
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0004 --type work-item --title "Record a
    settlement payment and net it off the balances" --epic EP-001 --priority high --status draft
    --actor intake --reason "..."` -> exit 0
- **Gates:** `intake`'s contract gates, applied to this one item:
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0, one pre-existing warning
    about the null test command, which `plan` owns.
  - `epic-has-success-measures` (hard) -> **pass, and amended** — the epic gained a fourth measure
    in the same batch, covering a recorded payment no longer being reported as a debt and the
    all-settled outcome. It is checkable by a person with a terminal.
  - `items-are-separable` (advisory) -> **pass** — WI-0004 delivers something demonstrable on its
    own once WI-0003 exists: record a payment, ask again, see a smaller debt. Its dependency on
    WI-0003 is recorded in `depends-on`, so the orchestrator enforces the order.
  - `no-solution-in-the-problem` (advisory) -> **pass** — the body names no file format, data
    structure or library. "Recorded", "listed back" and "survives exiting and restarting" are
    outcomes, not implementations.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — story, AC1–AC6, out-of-scope, notes
  - `tracker/items/WI-0004/journal.md` — this entry
  - the item's creation row, written by the `new-item` script
- **Status:** `—` -> `draft` (creation)
- **Result:** The settlement capability the human asked for has an item to be refined, planned,
  built and verified against, behind WI-0003. Nothing about it has been designed.

## 2026-08-21T21:24:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` once WI-0003 reached `done`. A fresh
  refinement: the item's history has exactly one row, its creation, and it has never been past
  `draft`.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md` (one entry, `intake`'s); the
    `questions/` directory is **empty** — this item has never had a question of its own
  - `tracker/items/EP-001/questions/Q-001.md` — the human's answer that created this item, since
    it is the only thing they have said about payments
  - `ADR-0001` to `ADR-0010`, `docs/product/prd.md` (v2), `docs/product/vision.md` (v3),
    `docs/architecture/overview.md` (v3)
  - **`tracker/items/WI-0002/item.md` and `WI-0003/item.md` `## Notes`** — the accepted gaps their
    reviews handed to this item by name, and their `artifacts/review.md` for the reasoning
  - `tracker/items/WI-0003/item.md` criteria, for the settlement behaviour this item's criteria
    build on
- **Decisions:**
  - **Pinned `add-payment <amount> --from <name> --to <name>`.** The positional amount mirrors
    `add-expense`; `--from`/`--to` rather than `--paid-by`/`--paid-to` because a payment has a
    direction. Rejected three bare positionals — that is the shape that gets typed wrong, and this
    is money.
  - **Past tense in the listing.** `payments` prints `1. Bob paid Alice 10.00` where
    `who-owes-whom` prints `Bob pays Alice 10.00`. One records what happened; the other proposes
    what to do; a reader seeing both should be able to tell which is which without thinking.
  - **Computed all five settlement examples against the delivered code before writing them down.**
    AC5, AC6, AC7, AC8 and AC15 each assert what `who-owes-whom` prints *after* a payment, and an
    example that did not add up would be a criterion the tool could never satisfy. Doing this
    caught a real error: my first draft of AC8 had `Carol pays Bob` before `Alice pays Bob`, and
    the tie-break — equal debts, `alice` before `carol` — puts Alice first. Corrected before the
    item was written out.
  - **Accepted overpayment (AC8) rather than asking.** This is the closest call in the refinement.
    The human's one sentence about payments — "otherwise the numbers just keep racking up forever
    and stop meaning anything" — carries the principle: record what actually happened. A tool that
    refused an overpayment would decline to record a real event, and the group could not express
    it. Recorded in the Q&A with a pointer for the human if they would rather have a warning.
  - **Refused a self-payment (AC10).** It moves no net position, so accepting it would put a fact
    in the record that no arithmetic can ever see. Compared by identity key, like everything else
    about people.
  - **Dealt with all three inherited gaps, and deliberately made only one of them a criterion.**
    "A refusal creates no record file" is observable, so it is AC13's last clause. The other two —
    `net_positions`' unasserted ordering contract, and a purity test whose fixture holds one
    expense — are **not** observable through any command, so a criterion about them could not be
    decidable and would fail R4. They are written into `## Notes` as instructions to `plan`
    instead. Writing an undecidable criterion to look thorough is precisely the failure the
    Definition of Ready exists to prevent, and the Q&A says so in as many words.
  - **Excluded refusing an overpayment and correcting a mistaken payment**, naming them as the two
    things a reader would most reasonably assume are here. The second has an answer that costs
    nothing: record the opposite payment, which AC8 and AC15 show is possible.
  - **Filed nothing to the human.** Their scope decision is on file; everything else was syntax,
    wording, or already settled by an ADR written for a sibling.
- **Questions raised:** none — and none has ever been raised on this item. The full exchange, such
  as it is, is at `artifacts/refinement-qa.md`: one answer quoted from the epic's question, five
  decided here (four `[assumed]`, one answered from `ADR-0003`), and a table of the three
  inherited gaps.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - a script computing net positions and the settlement for all five of AC5 to AC8 and AC15
    against `group.net_positions` and the settlement rule → every example confirmed, and AC8's
    order corrected
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to ready --actor refine` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion:
    - **R1** frontmatter complete [auto] → **pass**: `depends-on: WI-0003`, now `done`.
    - **R2** story names role, capability, outcome [skill] → **pass**: "As a member of the group
      who has just handed money to someone I owed … so that the tool stops reporting a debt that
      has already been paid."
    - **R3** labelled checkbox criteria [auto] → **pass**: AC1–AC15.
    - **R4** every criterion decidable by observation [skill] → **fail on entry** — all six named
      outcomes with no command, and AC4 and AC5 were written against "whatever WI-0003's criteria
      settle on", which was nothing at the time. Rewrote them against the pinned syntax and the
      delivered settlement, with every expected output computed first → **pass**.
    - **R5** out-of-scope names something a reader would assume included [skill] → **fail on
      entry** (four entries, all obvious) → **pass**: six, led by refusing an overpayment and
      correcting a mistaken payment.
    - **R6** every open question non-blocking [auto] → **pass**: none exists.
    - **R7** independently deliverable [auto] → **pass**: `depends-on: WI-0003`, `done`.
    - **R8** Q&A recorded verbatim [auto] → **fail on entry** (no such file) → **pass**:
      `artifacts/refinement-qa.md`, opening with the human's answer that created the item.
    - **R9** one coherent change [skill] → **pass**: record a payment, list payments, let the
      existing settlement net them off. The write side and its effect on `who-owes-whom` are
      unobservable without each other.
    - **R10** every combination stated, excluded, or unconstrained [skill] → **fail on entry** —
      nothing said what a self-payment, an overpayment, a payment with no expense behind it, or an
      empty listing does → **pass**: AC1 to AC15 state all of them, and `## Notes` names the two
      things left open with `refine` recorded as who left them.
  - `criteria-are-decidable` (hard) → **pass**. Thirteen of the fifteen are settled by running one
    or two commands and comparing captured output against a string in the criterion. AC13 is
    settled by re-running two listing commands and checking for the absence of a file. AC14 is
    settled by two commands whose expected output is stated.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` quotes the human's
    only statement about payments exactly, and marks the five answers decided here as `[assumed]`
    or as answered from `ADR-0003`. It also records, for Q4, that the decision was close to being
    a question and why it was not asked — which is the part a later reader would otherwise have to
    guess at.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0004/item.md` — criteria rewritten and extended from six to fifteen; the
    syntax and the meaning of a payment stated at the head of the list; `## Out of scope` widened
    from four entries to six; `## Notes` restructured, with a section for the three inherited gaps
- **Status:** `draft` → `ready`
- **Result:** WI-0004 meets the Definition of Ready on all ten criteria, with no override. It is
  the epic's last item, and it carries three gaps inherited from two earlier reviews: one is now
  an acceptance criterion and two are instructions to `plan` that `review-close` can check were
  followed.

## 2026-08-21T21:32:00Z — plan v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `ready`, dispatched by `next`. The epic's last item; not a re-plan.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` (AC1–AC15, the pinned syntax, and the three inherited gaps in
    `## Notes`), `artifacts/refinement-qa.md`, `history.md`
  - `tracker/items/EP-001/questions/Q-001.md` — the human's answer that created this item
  - `ADR-0001` to `ADR-0010`, `docs/architecture/overview.md` (v3), `docs/product/prd.md` (v2)
  - **the code**: `expenses/group.py` (`net_positions`, `settle`, `find_person`, `add_expense`),
    `expenses/cli.py` (`_options`, `_add_expense`, `_expenses`, `_who_owes_whom`),
    `expenses/storage.py` (`_is_expense`, `load`), `expenses/money.py`, `tests/support.py`,
    `tests/test_who_owes_whom.py` — the last because steps 5 and 6 extend it
  - `tracker/items/WI-0002/artifacts/review.md` and `WI-0003/artifacts/review.md` — the two
    reviews that handed instructions here
- **Decisions:**
  - **`ADR-0011`, the stored shape of a payment (route: decided; `ADR-0007` point 2 left the key
    open and `refine` named this execution).** Three fields — amount in minor units, `from`, `to`,
    both stored spellings. The option worth recording is the one rejected: modelling a payment as
    an expense paid by one person and shared solely by the other. The arithmetic genuinely comes
    out the same and `net_positions` would have needed no change at all — but `expenses` would
    then list fictitious expenses the group never had, which is a lie about what was spent, and
    `prd.md` lists the two kinds of fact separately precisely because they are different to the
    person reading the output.
  - **The second half of `ADR-0011` is where payments are read, and it is the more consequential
    half.** They fold in inside `group.net_positions` and nowhere else. The alternative — adjusting
    in `settle` or in the handler — would leave `net_positions` returning a number that is not
    anybody's actual position, and the next caller to arrive would have to remember to correct it.
    That is the shape of rule that drifts. Written into `overview.md` v4 as a standing rule:
    every balance-shaped question goes through `net_positions`.
  - **`who-owes-whom` is not changed at all.** AC5 to AC8 and AC15 are satisfied by a function
    verified over 407 records in WI-0003, given different inputs. Stating that explicitly in the
    plan's out-of-scope list is what stops `implement` "helpfully" touching the settlement.
  - **Reused `cli._options` unchanged (route: reversible assumption).** WI-0002 wrote it taking the
    known-flag set as an argument, so `("--from", "--to")` needs nothing new — including the two
    messages AC12 pins for a repeated or unknown option, which are the same strings.
  - **Refusal ordering: unknown person before self-payment (route: reversible assumption).**
    `--from Dave --to Dave` reports that Dave is not in the group. Both refusals are true;
    membership is the more useful thing to hear first and is the check that already exists.
  - **Turned both non-criterion instructions into numbered steps (5 and 6) rather than a note.**
    `refine` was right that neither is observable through a command, so neither could be a
    criterion — but a plan step is binding in a way a note is not, and the mapping table lists
    them explicitly as *(not a criterion)* rows so nobody mistakes them for one. Step 5 asserts
    `net_positions`' ordering contract; step 6 rebuilds WI-0003's purity assertion on a record
    where reordering is actually detectable.
  - **Wrote risks for both, because both are easy to write so they still cannot fail.** Step 5's
    test must use people whose added order differs from their alphabetical order *and* from their
    position magnitudes; step 6's record needs at least two expenses and two payments with
    different amounts. A one-element list in a new place would repeat exactly the mistake being
    fixed.
  - **Named the AC13 trap.** "A refused `add-payment` leaves no file behind" needs a record with
    no file, which means no people — so the refusal exercised has to be one that does not require
    a person to exist. A test that adds people first has already created the file and proves
    nothing.
  - **Did not design past the item.** No link from a payment to the debt it discharges, no
    duplicate detection, no shared listing helper, nothing for a fifth kind of fact. Every step
    maps to a criterion or to one of the two declared instructions.
  - **Asked the human nothing.** Their scope decision is on file and is quoted in `ADR-0011`; the
    two decisions this execution made are a data shape (migratable) and a call-site (one function
    to move).
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to planned --actor plan` → exit 0
  - no test run: this execution wrote no code.
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table has one row per
    criterion, AC1 to AC15, each naming the step and the exact expected output, plus two clearly
    labelled *(not a criterion)* rows for steps 5 and 6 so that the instructions from earlier
    reviews are visible in the same table rather than buried in prose.
  - `project-commands-resolved` (hard) → **pass** — unchanged from `ADR-0008`; both commands have
    been exercised against real failures and by three items since.
  - `decisions-recorded` (hard) → **pass** — one new ADR (`ADR-0011`, both halves), one document
    change (`overview.md` v4, including the standing `net_positions` rule), six ADRs cited rather
    than re-decided, and three entries under `## Assumptions` with their reversal costs.
  - `plan-is-executable-without-you` (advisory) → **pass.** Every step names its files and the
    interface it must expose, and the two steps that are not criteria say what would make them
    vacuous. The place a developer still has to think is the sign of the two lines in
    `net_positions` — and `## Risks` says what failing that looks like: getting the sign wrong
    fails five criteria loudly, while folding payments in twice fails AC6 but not AC5, which is
    why the criteria include a part payment.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` (new) — 8 steps, a 17-row mapping table, 3
    assumptions with reversal costs, 5 risks, and what is out of scope
  - `docs/architecture/adr/ADR-0011-stored-shape-of-a-payment.md` (new, v1)
  - `docs/architecture/overview.md` — v3 → v4: payments in `group.py`, the standing rule that
    balances go through `net_positions`, and "what is not here yet" replaced by the complete
    record, since nothing in EP-001 remains after this item
- **Status:** `ready` → `planned`
- **Result:** WI-0004 has a plan that adds one key, one loop and two handlers, and changes nothing
  about the settlement. The two instructions earlier reviews left for this step are numbered steps
  with their own risks, so `review-close` can check they were done rather than hope.

## 2026-08-21T21:42:00Z — implement v0.1.0 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next`. Fresh start: `git branch --list 'wi/*'`
  showed the three earlier branches only, and the last history row was `ready → planned`.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` (AC1–AC15, the pinned syntax, the three inherited gaps in
    `## Notes`), `artifacts/plan.md`, `artifacts/refinement-qa.md`, `history.md`
  - the `questions/` directory — **empty**; this item has never had a question
  - `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0009`, `ADR-0010`, `ADR-0011`,
    `docs/architecture/overview.md` (v4)
  - the existing source: `group.py` (`net_positions`, `settle`, `find_person`, `identity_key`,
    `add_expense`), `cli.py` (`_options`, `_add_expense`, `_who_owes_whom`), `storage.py`
    (`_is_expense`), `tests/support.py`, and `tests/test_who_owes_whom.py`, which steps 5 and 6
    modify
- **Decisions:**
  - **Wrote the payment fold as four lines in `net_positions` and changed nothing else about the
    arithmetic.** That was `ADR-0011` point 2 and the plan's central claim: `settle`,
    `who-owes-whom` and `shares_of` are untouched, and the five settlement criteria pass because
    the inputs changed. Worth recording that the claim held exactly — the diff for those three
    functions is empty.
  - **`RefusalLeavesNoFileTest` had to be a plain `TestCase`, not an `ExpenseTestCase`.** The
    criterion needs a record with no file at all, and `ExpenseTestCase.setUp` adds four people,
    which creates one. `plan.md` § *Risks* named this exact trap — "a test that first adds people
    has already created the file and proves nothing" — so the class repeats the temporary-directory
    setup by hand and its docstring says why. Recorded as a deviation because it duplicates
    scaffolding that otherwise exists once.
  - **Chose refusals for that test that do not need a person to exist**: a malformed amount, an
    unknown person against an empty group, and a missing `--to`. Each refuses before anything is
    written.
  - **Made AC13's assertion include `who-owes-whom`,** not only the three listings. It is the
    output a user would actually notice going wrong after a refusal, and it costs one line.
  - **Updated `group.__all__` with four names, not two.** It was written in WI-0002 and WI-0003
    did not add `net_positions` or `settle`, so it was already stale. Adding only this item's two
    would have left it wrong in a new way. Declared, because it touches a line no criterion
    covers.
  - **Built the two review instructions to fail for the right reason.** Step 5's test uses people
    added as `Zoe`, `alice`, `Mo`, `Bea` — an order matching neither the alphabet nor the sizes of
    their positions — because `plan.md` warned that a naive fixture would pass whatever the code
    did. Step 6's fixture holds two expenses **and** two payments with different amounts, where
    WI-0003's held one expense; a second one-element list would have repeated the original mistake
    in a new place. I checked both by mutation rather than by eye.
  - **Confirmed all three inherited gaps are actually closed**, by re-running the mutations that
    escaped on the earlier items: saving before validating, sorting `net_positions`, and
    reordering the record during `who-owes-whom`. All three are now caught, each by the test
    written for it. That is the part of this item a reader should be able to check, and it is in
    the report as a three-row table.
  - **Escalated nothing and filed no bug.** No decision here changes an interface, contradicts an
    ADR, or introduces user-visible behaviour no criterion covers.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0004` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests ... OK` (final run on
    the branch head). Intermediate: 16 tests after step 4, 18 in the modified module after steps 5
    and 6, 115 after step 4's subprocess addition
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - the AC1, AC3, AC5 and AC14 command lines by hand against a temporary `EXPENSES_FILE`, and
    `cat` of the resulting record to check it against `ADR-0011` point 1 field by field
  - `python3 /tmp/mut4.py` — fifteen mutation runs, each reverted; `git status -- expenses tests`
    clean afterwards
- **Gates:** all six, on the branch head after the last code change.
  - `tests-pass` (hard) → **pass** — 115 tests, exit 0.
  - `lint-clean` (hard) → **pass** — `compileall`, exit 0, with the standing `ADR-0008` caveat.
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `every-criterion-has-a-test` (hard) → **pass** — a test per criterion, and fifteen mutations
    as the evidence they bite. All fifteen were caught on the first pass, which was not true on
    either of the previous two items; the difference is that the plan named the two traps in
    advance and I wrote the fixtures against them.
  - `commits-reference-the-item` (hard) → **pass** — exit 0.
  - `no-unplanned-scope` (advisory) → **pass, with three declared deviations** — every hunk traces
    to a plan step and a criterion, and the three functions the plan put out of scope have an
    empty diff.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` (new)
  - branch `wi/WI-0004`, commits `main..wi/WI-0004`
  - `expenses/storage.py` (`payments` key, `_is_payment`), `expenses/group.py` (`payments`,
    `add_payment`, the fold in `net_positions`, `__all__`), `expenses/cli.py` (`_add_payment`,
    `_payments`, the last two `COMMANDS` entries)
  - `tests/test_payments.py` (new, 16 tests); `tests/test_who_owes_whom.py` and
    `tests/test_persistence.py` (extended)
  - `tracker/items/WI-0004/item.md` — `branch: wi/WI-0004` set
- **Status:** `in-progress` → `verifying`
- **Result:** The epic's last piece of code: payments are recorded, listed, and netted off by the
  settlement that was already there. 115 tests, fifteen mutations all caught, and the three gaps
  two earlier reviews handed forward are closed with a mutation apiece to prove it.

## 2026-08-21T21:50:00Z — verify v0.1.0 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next`. The epic's last item.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the fifteen criteria, **read first**
  - `history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/refinement-qa.md`
  - `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0010`, `ADR-0011`,
    `docs/architecture/overview.md` (v4)
  - **`tracker/items/WI-0002/item.md` and `WI-0003/item.md` `## Notes`** — the three gaps their
    reviews handed here, since checking those is half of what this verification is for
  - the branch `wi/WI-0004` at commit **f3be13cb4d0515a9a66587a9017cba120042205c**, and the source
    of `group.add_payment`, `group.net_positions`, `cli._add_payment`, `cli._payments` and
    `storage._is_payment`
- **Decisions:**
  - **Checked AC5 by running `who-owes-whom` before *and* after the payment.** A criterion that
    says "a payment reduces what its payer owes" is only meaningful against the prior state, and
    checking only the after-state would pass against a tool that had never had the debt.
  - **Verified the three inherited gaps the only way they can be verified** — by re-running the
    exact mutations that survived on WI-0002 and WI-0003 against this branch. All three now fail a
    test, each the one written for it. I added a fourth in the same family (`net_positions`
    dropping people at zero) and it is caught by four tests, so both halves of that contract are
    asserted, not just the ordering half.
  - **Found one real gap by mutation: the `payments` shape check is unasserted.** Deleting it
    entirely passes all 115 tests. `ADR-0011` point 5 and `plan.md` step 1 both require it. I
    confirmed the code is correct by feeding the tool four malformed records by hand — a non-list,
    a string amount, a missing field, and a bad nesting — each refused with the right message and
    the file left untouched.
  - **Classified that as a finding, not a send-back.** The classification test is whether a
    criterion of this item says the behaviour should be different: none does — no criterion here
    mentions a corrupt record. It is also not a bug against another item, since the behaviour is
    WI-0004's own. What it *is* worth saying plainly, and the report says it: this is the same
    species as the two gaps this item was created to close, and the pattern that produces them is
    **a plan step with no criterion behind it**. WI-0002 had a test for the equivalent on
    expenses; this item has no counterpart, and nothing in the process would have caught that.
  - **Probed backward compatibility with a WI-0003-era record** — no `payments` key at all — and
    confirmed `payments`, `who-owes-whom` and `add-payment` all work on it. That is `ADR-0007`
    point 2 holding for the fourth and last key.
  - **Probed `ADR-0010` on `add-payment` properly.** My first attempt used a record with no
    people, so the command refused on membership before ever trying to write, and proved nothing.
    Redone with people added first: `Cannot save to <path>: Permission denied.`, no traceback.
    Recording the false start because the first version of that probe looked like evidence and
    was not.
  - **Filed no bug and no question.** No criterion was ambiguous.
- **Questions raised:** none.
- **Commands:**
  - `git rev-parse HEAD` → `f3be13cb4d0515a9a66587a9017cba120042205c`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests ... OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - ~45 `python3 -m expenses …` invocations covering AC1 to AC15, quoted in `verify-report.md`
  - the AC13 sweep: twelve refusals in sequence against a populated record, comparing all four
    listings **and the file's md5** before and after; then three refusals against a record with no
    file, checking none was created
  - seven boundary probes, including four hand-written malformed records and an unwritable
    directory
  - thirteen mutation runs, each reverted — the three inherited ones, a fourth in that family, and
    nine of my own
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here on the branch head, 115 tests, exit 0.
  - `lint-clean` (hard) → **pass** — exit 0, with the standing `ADR-0008` caveat, restated under
    *Not verified*.
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `every-criterion-independently-checked` (hard) → **pass** — fifteen rows of commands and
    captured output, none citing the implementation report.
  - `negative-cases-exercised` (hard) → **pass** — every refusal criterion triggered; twelve
    refusals swept in sequence; the "no file left behind" clause checked on a record that had
    none; seven further probes.
  - `tests-would-fail-without-the-change` (advisory) → **pass, with one survivor** — twelve of
    thirteen caught, and the three that matter most are the previously-surviving ones, now caught.
    The survivor is reported as a finding rather than smoothed over.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` (new), carrying
    `Verified-commit: f3be13cb4d0515a9a66587a9017cba120042205c`
  - `tracker/items/WI-0004/item.md` — AC1 to AC15 ticked, each after its row in the report existed
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0004 does what its fifteen criteria say, and the three gaps it inherited are
  closed with a mutation apiece proving it. One new finding for `review-close`: the `payments`
  shape check is required by an ADR and a plan step, is correctly implemented, and is asserted by
  nothing — the same shape of gap the last two reviews recorded, arriving again by the same route.

## 2026-08-21T22:00:00Z — review-close v0.1.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next`. The epic's last child, so this execution
  also decides EP-001.
- **Inputs read:**
  - the diff `main..wi/WI-0004` for `expenses/`, hunk by hunk, and the test modules it touches
  - `item.md`, `history.md` (six rows), `journal.md` **in full** (five entries), `plan.md`,
    `impl-report.md`, `verify-report.md`, `refinement-qa.md`
  - `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0010`, `ADR-0011`, `overview.md` (v4),
    `prd.md` (v2), `vision.md` (v3)
  - **`tracker/items/EP-001/item.md`** — the four success measures
  - `WI-0002/item.md` and `WI-0003/item.md` `## Notes` — the three gaps handed to this item
- **Decisions:**
  - **Ran the epic's four success measures rather than reasoning about them.** DE3 asks whether
    each is addressed; the only honest way to answer at the end of an epic is to be the user. All
    four are met, and the fourth — no third-party packages, no network — was checked by replacing
    `socket.socket` with a class that raises and running all seven subcommands. Every one exited
    `0`, so none opened a socket. Reading the imports would have been the easier half of that.
  - **Checked that the three inherited gaps were closed, which only this position in the pipeline
    can check.** `verify` did it by mutation and I confirmed the tests exist and are named for the
    gaps they close. This is the one thing a reviewer standing at the end of an epic can do that
    no upstream stage can: see whether a promise made two items ago was kept.
  - **Finding 1, accepted, and generalised.** The `payments` shape check is required by an ADR and
    a plan step, correctly implemented, and asserted by nothing. `verify` named the pattern and it
    is right: **a plan step or ADR clause with no acceptance criterion behind it is checked by
    nothing in this pipeline.** Three of the four gaps recorded across these four reviews arrived
    by that route. That is a methodology observation, not a code defect, so it goes in the epic's
    journal as well as the item's notes — it is the most useful thing this epic learned about
    itself.
  - **Finding 2 — the epic's own scope wording contradicts the PRD.** `EP-001` excludes
    "free-text expense history beyond a description", which reads as though a description is in
    scope; `prd.md` (v2) says an expense is an amount, a payer and sharers and "Nothing else", and
    WI-0002 excluded a description citing exactly that. Not treated as an unmet success measure —
    none of the four mentions it, and all four are met — but recorded in three places, because a
    reader starting at the epic would expect a field that does not exist, and because it is
    probably the first thing the group will ask for.
  - **Did not file a bug or a question for either finding.** Neither contradicts an ADR; Finding 1
    is behaviour no criterion covers and Finding 2 is a documentation inconsistency in an artifact
    the human owns. Both are recorded where a reader will meet them.
  - **Closed EP-001.** DE1 to DE4 all pass, with Finding 2 recorded against DE4. Closing an epic
    with a measure unmet is allowed if stated; none is unmet, and saying so required running them.
  - **Trial-merged into a `--detach`ed worktree** and confirmed `main` was still at `fbc6085`
    afterwards — the third execution to follow the correction WI-0001's review had to make.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → exit 0
  - `git diff --name-only f3be13c..wi/WI-0004 -- expenses tests` → empty
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, three
    commits, **before** the merge
  - `git worktree add --detach /tmp/trial4 main` → `git merge --no-edit wi/WI-0004` → clean; on
    the result: 115 tests exit 0, `compileall` exit 0; `git worktree remove --force`;
    `git log --oneline -1 main` → `fbc6085`, unmoved
  - the epic's four success measures, run end to end: eight processes for the first two, four more
    for the third, and a socket-sabotage run of all seven subcommands for the fourth
  - re-ran AC5's before-and-after and AC8's overpayment by hand → same output as the report
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the close
  - `git checkout main && git merge --no-ff wi/WI-0004` → after the close
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1 to D12 each with its own result and evidence in
    `artifacts/review.md`, plus the epic's DE1 to DE4 in the same document.
  - `verification-postdates-the-code` (hard) → **pass** — script exit 0 plus the independent diff,
    which is empty.
  - `commits-reference-the-item` (hard) → **pass** — exit 0, before the merge.
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 115 tests, exit 0, on the merged tree.
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings.
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and
    `git log --grep WI-0004` a reader can answer all five questions in
    `spec/journal-and-history.md` §3. This item is the unusual one for question 1, "what was asked
    for": it has no question of its own, and its `refinement-qa.md` opens by saying so and quoting
    the epic's answer that created it, rather than leaving an empty file to be puzzled over.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` (new) — D1–D12, the epic's DE1–DE4 and its four
    measures run, three findings, six accepted gaps
  - `tracker/items/WI-0004/item.md` — `outcome: delivered`; `## Notes` extended with five accepted
    gaps
  - `tracker/items/EP-001/item.md` — closed, `outcome: delivered`
  - `tracker/items/EP-001/journal.md` — the epic's closing entry
  - the merge commit of `wi/WI-0004` into `main`
- **Status:** `in-review` → `done`
- **Result:** WI-0004 is delivered and merged, and EP-001 is closed with all four success measures
  demonstrated. Three findings, none blocking; the one that outlives the epic is about the
  pipeline rather than the product — a plan step with no criterion behind it is checked by
  nothing, and that produced three of the four gaps this epic recorded.
