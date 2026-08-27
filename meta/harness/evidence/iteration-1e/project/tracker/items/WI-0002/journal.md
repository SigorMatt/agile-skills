# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-26T23:24:58Z — intake v0.2.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's opening statement (`IDEA.md`); no prior workspace state existed
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/project.yaml`
  - `tracker/items/EP-001/item.md` (written by this same execution)
- **Decisions:**
  - See EP-001's entry for this execution for how the work was split and why.
  - Left AC1 deliberately imprecise and filed EP-001/Q-002 instead of choosing between net positions and a settlement list. Writing a precise criterion here would have been a design decision disguised as analysis.
- **Questions raised:** none on this item; `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003` are filed on the epic and affect this item
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace` reported 0 errors at the end of this execution)
  - `epic-has-success-measures` → **pass** (assessed on EP-001; see its entry)
  - `items-are-separable` (advisory) → **pass** (see EP-001's entry for the order and dependencies of all three items)
  - `no-solution-in-the-problem` (advisory) → **pass** (see EP-001's entry)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
- **Status:** `—` → `draft`
- **Result:** Created at draft. Its central acceptance criterion cannot be made decidable until EP-001/Q-002 establishes whether "who owes whom" means net positions or a settlement list.

## 2026-08-26T23:31:59Z — answer-questions v0.2.0 — architect

- **Item:** WI-0002
- **Trigger:** no status of its own — this item's acceptance criteria were amended as a consequence of EP-001/Q-002 and EP-001/Q-003, both answered by the stakeholder. `answer-questions` was run on EP-001; this entry records what it changed here.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-002.md` (the stakeholder's reply on what "who owes whom" should print)
  - `tracker/items/EP-001/questions/Q-003.md` (the stakeholder's reply on delivery order)
  - `tracker/items/WI-0002/item.md` (the criteria as intake left them)
  - `tracker/items/EP-001/item.md`, `tracker/items/EP-001/journal.md` (intake's framing and what it deliberately left open)
  - `docs/product/vision.md` (v1, before this execution bumped it)
  - `docs/architecture/adr/` — empty; no recorded decision could be contradicted by this answer
- **Decisions:**
  - Amended AC1 from "prints … who owes whom and how much" to "prints a list of payments …
    naming who pays, who they pay, and how much". Rationale: the stakeholder chose option B of
    Q-002 explicitly, and the old wording is the ambiguity the question existed to remove. The
    amendment is legal and recorded rather than quiet: the item is at `draft`, criteria are frozen
    only after `ready`, and `answer-questions` is one of two skills permitted to change one.
  - Amended AC2 and AC3 to speak about the payment list rather than about unspecified "figures",
    so that all four criteria describe one artifact. AC3 now states the settlement property —
    payments made minus payments received equals each person's overall position — which is what
    "the figures balance" has to mean once the output is a payment list.
  - Added AC4: the same recorded data must print the same payments in the same order. Rationale:
    this is not an invention, it is part of what was chosen. Option B's stated consequence was
    that a settlement list "needs a rule for choosing between equally valid settlements … that
    rule becomes an acceptance criterion", and the stakeholder chose option B.
  - Did **not** decide what the tie-break rule is. AC4 fixes that a stable rule must exist; which
    settlement to prefer and in what order to print it is refinement's to settle and `plan`'s to
    record. Deciding it here would pre-empt two skills to no benefit.
  - Recorded net-position-per-person under `## Out of scope` rather than leaving it unmentioned.
    It was offered as option C and not chosen, so a later reader would otherwise have no way to
    tell an omission from a decision.
  - Recorded the delivery order in `## Notes` so it is visible on the item, not only on the epic.
- **Questions raised:** none
- **Commands:**
  - `scripts/journal-entry WI-0002 --skill answer-questions --body-file /tmp/j-wi0002.md` → this entry
- **Gates:**
  - `answer-is-propagated` → **pass** — Q-002's `## Consequences` names this file for AC1–AC4, `## Notes` and `## Out of scope`; all are present above. Q-003's names this file for the delivery-order note; present.
  - `answered-from-the-record` → **pass** — every change here follows from the stakeholder's own words in Q-002 and Q-003, quoted in the item's notes. Nothing was decided that the record did not support, so no ADR was needed.
  - `escalation-is-justified` → **skipped** — nothing on this item was escalated.
  - `workspace-valid` → **pass** — `scripts/validate-workspace` run by the EP-001 transition in this same execution, after every edit including these.
  - `item-resumed-correctly` → **skipped** — this item did not change status, so there is no resume-to to honour. It stays at `draft` for `refine`.
  - `a-deferral-is-not-an-answer` → **skipped** — neither Q-002 nor Q-003 was a deferral; both were answered outright. The deferral in this round was Q-001, which does not touch this item.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — AC1, AC2, AC3 amended; AC4 added; `## Out of scope` and `## Notes` rewritten
- **Status:** `draft` → `draft` (unchanged)
- **Result:** WI-0002 now states what it must print — a settlement list, stably ordered — instead of deferring to a question. It stays at `draft` and is `refine`'s next.

## 2026-08-27T00:27:02Z — refine v0.2.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item — priority `high` (rank 2), created 2026-08-26T23:22:38Z, its only dependency WI-0001 now `done`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the criteria as `answer-questions` left them on 2026-08-26T23:31:59Z
  - `tracker/items/WI-0002/history.md` — one row, `— → draft` from `intake`. This is a **fresh** draft, not an item sent back from a later stage, so the whole story is open rather than one named defect
  - `tracker/items/WI-0002/journal.md` — `intake`'s entry (why AC1 was left imprecise) and `answer-questions`' entry (what EP-001/Q-002 and Q-003 changed here, and what they deliberately did not decide)
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md` — the stakeholder's answers on what "who owes whom" prints, and on delivery order
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the equal-split answer this item's arithmetic rests on, and the two boundaries it must not cross
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — the precedent for which calls refinement takes without asking (A1–A12 there), followed here
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0004/item.md`, `tracker/items/WI-0003/item.md` — sibling scope: what is already delivered, and what belongs to deletion and to the importer
  - `docs/product/vision.md` v3 — checked for contradiction; none. It already states the answer is a payment list and not a table of positions, which is what AC1 says
  - `docs/architecture/adr/ADR-0002-money-as-integer-minor-units.md`, `ADR-0003-remainder-goes-to-the-first-named-sharers.md` — why no rounding arises in this item
  - `expenses/money.py`, `expenses/store.py`, `expenses/cli.py`, `README.md` — the delivered command surface and stored shape, so the new criteria name commands that exist and a line form consistent with the ones already printed
- **Decisions:**
  - **Asked the stakeholder nothing, deliberately.** The one product-stake question on this item — what "who owes whom" means — was answered in EP-001/Q-002, and that answer states in terms that the settlement *rule* "is not the stakeholder's to decide; it is refinement's, and then `plan`'s". Every remaining gap was a naming, wording or arithmetic call. Eight candidate questions were considered and each is recorded in `refinement-qa.md` with the reason it was not asked, so that "nothing was asked" is auditable rather than asserted.
  - **AC1 rewritten** from "a documented command prints … a list of payments" to a named command over a named three-person dataset with an exact expected pair of lines. What changed about its meaning: it is no longer decidable only by someone who knows what the command is called. What did not change: it is still a payment list, not a balance report.
  - **AC2 rewritten** from "prints that no payments are needed" to the exact string `no payments needed` over three stores. Its meaning widened on purpose: the original covered only "people but no expenses", and two further ways to have nothing to settle — an empty store, and expenses that leave everybody square — were unstated (R10). All three now print the same thing.
  - **AC3 rewritten** from a property with no dataset into that property checked on a five-person dataset with an exact expected output. The property is unchanged; what is new is that it can now be decided. The dataset was chosen to carry three of R10's gaps at once: an expense whose payer did not share in it, an amount that does not divide by three, and a person (`Eve`) whose position is zero and who must therefore appear nowhere. Its figures were computed by building the store with the delivered tool and summing the recorded shares, not by hand: Ana +16.66, Ben −1.33, Cara −9.33, Dan −6.00, Eve 0, summing to exactly zero.
  - **AC4 rewritten** from "the same payments in the same order" to a `cmp` of two runs in separate processes. Same meaning, now observable.
  - **AC5 added** — the command changes nothing on disk and creates no data file where none exists. Reason: R10 had no statement of whether asking the question writes anything, and the command name chosen in B1 (`settle`) could be read as *doing* the settling. Rather than argue the name is clear, the behaviour is made a criterion.
  - **AC6 added** — the README documents the command. The original AC1 said "a documented command" and named none; naming the command satisfies half of that, and this criterion keeps the other half rather than dropping it.
  - **B1–B7 settled without asking**, each recorded `[assumed — refine, not asked]` in `refinement-qa.md`: the command `python3 -m expenses settle` with no flags; a person's position as amounts paid minus shares recorded; the five properties the printed list must satisfy; the exact `no payments needed` string; the `Ben pays Ana 10.00` line form; that the command writes nothing; and that group size and speed are left unconstrained. The authority is EP-001/Q-002's own delegation plus the precedent set on WI-0001, where the command surface, exit codes, amount rules and empty-listing strings were settled the same way.
  - **Did not decide which settlement algorithm, or the print order.** AC3's dataset has a single creditor, so its expected output is forced by the properties rather than by an algorithm; with several creditors a choice remains, and it is recorded in `## Notes` as `plan`'s, constrained only to be deterministic. Deciding it here would pre-empt `plan` to no benefit, and EP-001/Q-002 named `plan` as its owner.
  - **Recorded the pairwise-debt consequence in `## Out of scope`** rather than leaving it to be discovered: computing from positions means the list may tell someone to pay a person they never shared an expense with. It is the one consequence of B3 a reader might not expect, and a reader must be able to tell it from an oversight.
  - **Did not split the item (R9).** A settlement list without its arithmetic is nothing and the arithmetic without the printing is unobservable; there is no ordering of two halves that delivers anything.
- **Questions raised:** none — no question was filed on this item, to the human or to anyone. `artifacts/refinement-qa.md` records the eight candidates considered and why each was not asked. Nothing is `[unresolved]`.
- **Commands:**
  - `EXPENSES_STORE=/tmp/ac3.json python3 -m expenses person add {Ana,Ben,Cara,Dan,Eve}` and three `expense add` runs → exit 0 each; used to compute AC3's expected figures from the delivered tool rather than by hand
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace` reported 0 errors and 0 warnings over 7 items and 6 documents, run after the item and the Q&A were written
  - `definition-of-ready` → **pass**, criterion by criterion, re-assessed on the item as this execution leaves it. R1 pass (frontmatter complete; `type`, `epic`, `priority` set; `depends-on` names WI-0001). R2 pass (role, capability and "so that" all present; unchanged). R3 pass (AC1–AC6, each labelled and a checkbox). R4 **fail on entry → pass**: every criterion said "a documented command" and named none, AC2 did not say what it prints, AC3 had no dataset, AC4 did not say how sameness is observed; all six criteria now name commands, data and an observation, and none contains an unmeasurable adjective. R5 pass (seven entries, including net positions and the pairwise-debt reading). R6 pass (no question exists on this item). R7 pass (WI-0001 is `done`). R8 **fail on entry → pass**: `artifacts/refinement-qa.md` did not exist and now exists at `status: recorded`. R9 pass (one coherent read-only command). R10 **fail on entry → pass**: no people, people without expenses and everybody-square are AC2; a zero-position person among non-zero ones is `Eve` in AC3; a payer who did not share is AC3's second expense; an uneven split is AC3's third; whether the command writes is AC5; and two things are recorded as deliberately unconstrained with who left them so — group size and speed (refinement) and the matching and print order (`plan`)
  - `criteria-are-decidable` → **pass** — AC1: run the four commands then `settle`, sort stdout, expect exactly `Ben pays Ana 10.00` and `Cara pays Ana 10.00` and exit 0. AC2: three stores, `settle` in each, expect stdout exactly `no payments needed` and exit 0. AC3: build the five-person store, run `settle`, sort stdout, expect exactly the three lines named; the four stated properties are then arithmetic on those lines. AC4: `settle > a; settle > b; cmp a b` → no output, exit 0. AC5: `md5sum` the data file either side of a run and compare; then `EXPENSES_STORE=<nonexistent> settle` and `test ! -e` that path. AC6: read `README.md` for the command name, an output example and the no-payments case. Every verdict follows from an exit code, a byte comparison or a string a reader can see
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` at `status: recorded` carries the three stakeholder answers this item rests on quoted verbatim and tagged `[human]`, B1–B7 tagged `[assumed — refine, not asked]` with the reason each was not the stakeholder's, and the eight candidate questions with the verdict on each. Nothing is paraphrased into agreement; no answer is attributed to the stakeholder that they did not give
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: recorded`)
  - `tracker/items/WI-0002/item.md` — AC1–AC4 rewritten, AC5 and AC6 added, `## Out of scope` grown from four entries to seven, `## Notes` restructured into what the stakeholder settled, what refinement settled, what is left to `plan`, and what is deliberately unconstrained
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. It names one command, `python3 -m expenses settle`, and six criteria a person with a terminal can decide by exit code, sorted output or byte comparison. Nothing was asked of the stakeholder, because the only product-stake question here was already answered and that answer delegated the settlement rule to refinement and `plan`; the eight candidates considered are recorded with the reason each was not asked. What `plan` inherits is one real decision — which settlement to prefer when there is more than one creditor, and in what order to print it — and the requirement that it be deterministic.

## 2026-08-27T00:31:51Z — plan v0.3.0 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` as the highest-ranked runnable item — priority `high` (rank 2), created 2026-08-26T23:22:38Z, `depends-on: WI-0001` satisfied
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC6, the contract this design satisfies
  - `tracker/items/WI-0002/history.md` — two rows, `— → draft` then `draft → ready`. This is a first plan, not a re-plan after a rejection, so there is no review or verification record to read first
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — B1–B7, all tagged `[assumed — refine, not asked]`; these are the design's soft ground and every one of them is honoured rather than re-decided. Nothing in the file is `[unresolved]`
  - `tracker/items/WI-0002/journal.md` — `intake`, `answer-questions` and `refine`, for what each deliberately left open
  - `tracker/items/EP-001/questions/Q-002.md` — the stakeholder's choice of a payment list, and its explicit statement that the settlement rule is `plan`'s
  - `tracker/items/WI-0001/questions/Q-001.md` — the equal-split answer the arithmetic rests on
  - `docs/architecture/overview.md` v1 — the one-way layering rule this design has to fit
  - `docs/architecture/adr/` — all four: **ADR-0001** (one JSON file; shares stored with each expense), **ADR-0002** (money as integer minor units), **ADR-0003** (the remainder rule, and why positions are exact), **ADR-0004** (unittest, and why `commands.lint` is null)
  - `tracker/project.yaml` — `commands.test` already set to a real command; `lint` and `build` null with ADR-0004 as the record
  - `expenses/money.py`, `expenses/store.py`, `expenses/cli.py` — the code this change touches and depends on: the stored expense shape (`amount_minor`, `paid_by`, `shared_by`, `shares_minor`), `format_amount`, and the `(command, action)` handler dispatch
  - `tests/test_cli.py` — the existing subprocess helper AC4's test can follow, and the case style AC1–AC5's tests should match
- **Decisions:**
  - **Which settlement to print, and in what order — ADR-0005.** Preference-order branch: **decided by the architect**, not asked. The documents do not answer it, and `EP-001/Q-002` puts it here in terms. Match the largest debt against the largest credit repeatedly, break ties in both pools by the order people were recorded, print in the order generated. Four options were weighed: largest-first (chosen), recorded-order-first, a minimum-transaction subset search, and every pairwise debt. The last contradicts the properties refinement fixed; the third is exponential for a gain the properties already cap; the second needs no tie-break but puts whoever was typed in first at the top. Checked against the item rather than asserted: AC1's `Ben`/`Cara` tie resolves to `Ben` first, and AC3's dataset yields `Cara 9.33`, `Dan 6.00`, `Ben 1.33` with `Eve` absent — which is what those criteria say.
  - **No rounding anywhere in this item.** Preference-order branch: **answered from the documents** — ADR-0002 makes money integer minor units and ADR-0003 makes each expense's stored shares sum exactly to its amount, so every position is a whole number and the positions sum to exactly zero. Every payment is the smaller of two whole numbers. No ADR: there is no alternative worth naming, since a float here would contradict a decision already taken.
  - **The command's name, its lack of flags, and its two output forms.** Preference-order branch: **answered from the documents** — refinement fixed `settle`, `no payments needed` and `Ben pays Ana 10.00` as B1, B4 and B5 and recorded them as its own calls. `plan` may propose a change with a recorded reason; there is no reason to, so they stand unchanged.
  - **A new module, `expenses/settle.py`, rather than code in `store.py` or in a handler.** Preference-order branch: **assumed, reversibly**, recorded under `## Assumptions` with the cost of reversal — the two functions move file with no signature, data or command change. Rationale: `store.py` is about the dataset's storage and validity, and a handler in `cli.py` would put arithmetic in the one layer that prints, which is what the project's layering rule exists to prevent.
  - **`positions()` is keyed on `data["people"]` in recorded order.** Preference-order branch: **assumed, reversibly**. It is what makes a person who has shared nothing reportable as zero — AC3's `Eve` — and what gives ADR-0005 its tie-break order.
  - **A dataset whose positions do not sum to zero is settled as far as it can be.** Preference-order branch: **assumed, reversibly**. The loop terminates on any input because each step empties at least one party. Only a hand-edited file can reach that state, which EP-001's measures say nobody should need. Raising instead would be behaviour nobody asked for.
  - **Named the `(args.command, args.action)` dispatch trap in the plan** rather than leaving it to be discovered: `settle` has no sub-action, so its subparser must `set_defaults(action=None)` and its handler register under `("settle", None)`, or the command raises `AttributeError`.
  - **Did not decide the implementations.** Signatures, the module boundary and the printed forms are fixed; how `positions()` walks the expenses and how the pools are kept sorted are the developer's.
  - **Recorded a risk WI-0004 inherits** rather than widening this plan: deleting a person without touching their expenses would silently drop them from this report. No delivered command can produce that state today, so it is not a defect and no bug was filed; it is named so WI-0004's plan starts from it.
  - **Did not update `tracker/project.yaml`.** `commands.test` is already a real command and was run in this execution; `lint` and `build` stay null on ADR-0004's record.
- **Questions raised:** none. Nothing in this design is irreversible, and nothing turns on intent no document records — the one decision that could have gone to the human was explicitly assigned to `plan` by the stakeholder's own answer to EP-001/Q-002.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 2 documents checked, 0 errors, 0 warnings
  - `python3 -m unittest discover -s tests -t .` → exit 0, 50 tests, OK — the declared test command, run in this project rather than assumed to work
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace` reported 0 errors and 0 warnings over 7 items and 7 documents, after the ADR, the plan and the overview were written. It failed once in between, on the change-log row order in `overview.md`, and was fixed before the transition
  - `every-criterion-is-addressed` → **pass** — the mapping table in `plan.md` has one row per AC, each naming the step that satisfies it and a specific demonstration rather than the word "tests". AC1 → steps 2, 3, sorted stdout against two named lines. AC2 → steps 2, 3, three stores each asserting stdout is exactly `no payments needed`. AC3 → steps 1, 2, 3, the exact three payments plus the four properties asserted separately. AC4 → step 2, two `subprocess.run` invocations compared as bytes. AC5 → step 3, an `md5` either side of a run and a non-existent path that stays non-existent. AC6 → step 6, reading `README.md` for the command, an example and the empty case. No AC is unmapped and no step is unmapped to an AC
  - `project-commands-resolved` → **pass** — `commands.test` is `python3 -m unittest discover -s tests -t .`, run in this execution and exiting 0 over 50 tests. `commands.lint` and `commands.build` are null, and ADR-0004 records why: the project may install nothing, the standard library ships no linter, and there is nothing to build. This item does not change that
  - `decisions-recorded` → **pass** — the `## Decisions and ADRs` table lists all five choices this plan makes with where each came from. One is **ADR-0005**; two are answered from ADR-0002, ADR-0003 and the refinement Q&A with citations; three are entries under `## Assumptions`, each stating what reversal would cost. Nothing is left as a choice without a record
  - `plan-is-executable-without-you` (advisory) → **pass** — read back as a stranger, each of the seven steps names its files and what is true afterwards, and the two function signatures are fixed in `## Approach`. The one place a stranger would have stalled — dispatching a subcommand with no sub-action — is decided in the approach rather than left as a discovery
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exited 0 over the 2 changed documents, `ADR-0005` and `overview.md`
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — problem, approach, seven steps, the AC mapping, three assumptions, the decision table, scaffolding `none`, four risks, five exclusions
  - `docs/architecture/adr/ADR-0005-settle-by-matching-the-largest-debt-to-the-largest-credit.md` (new, v1)
  - `docs/architecture/overview.md` — v1 → **v2**, with a change-log row: the module `expenses/settle.py` and the third top-level command are described under "What is coming" rather than in the body, because the module does not exist yet; step 7 of the plan moves it once it does
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. Seven steps over three files — a new `expenses/settle.py` holding `positions()` and `settlement()` as pure functions, a `settle` subcommand in `cli.py` that does all the printing, tests for each criterion, the README section, and the overview move. The one real decision is ADR-0005: match the largest debt to the largest credit, tie-broken by the order people were recorded, which is what makes AC1's and AC3's pinned outputs reproducible. Nothing was asked of the human, and no scaffolding was written.

## 2026-08-27T00:32:31Z — implement v0.2.1 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`. No branch existed, so this is a fresh start rather than a resumed one — `history.md`'s last row is `ready → planned` by `plan`, not a send-back from `verifying` or `in-review`, so there is no verification or review record to work from
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC6, the contract; and `## Notes`, which names what `plan` was left to decide
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, the two fixed signatures, the AC mapping, the three assumptions and the four risks
  - `tracker/items/WI-0002/history.md` — three rows, ending `ready → planned`; a fresh start
  - `tracker/items/WI-0002/questions/` — empty. No question has ever been filed on this item, so nothing has been answered since the last journal entry and there is nothing to re-read
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — B1–B5, the strings and forms this implementation must print exactly
  - `docs/architecture/adr/ADR-0005-settle-by-matching-the-largest-debt-to-the-largest-credit.md` — the settlement rule and its tie-break; `ADR-0002` and `ADR-0003` for why no rounding arises; `ADR-0001` for the stored expense shape
  - `docs/architecture/overview.md` v2 — the one-way layering the new module must obey
  - `tracker/project.yaml` — `branch-prefix: wi/`, `commit-subject: "<scope>: <summary> (refs <ITEM-ID>)"`, `commands.test: python3 -m unittest discover -s tests -t .` (present, not null), `commands.lint: null` with ADR-0004 as the record
  - `expenses/cli.py`, `expenses/store.py`, `expenses/money.py`, `tests/test_cli.py` — the code being extended and the test style to match
- **Decisions:** none yet. Nothing has been written; this entry exists to open the execution in the record before any code is, so that an interruption leaves a truthful status
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0, branched from `main` at `55536ec`
- **Gates:**
  - `tests-pass` → **not yet run** — the completion gates run on the branch head after the last change
  - `lint-clean` → **not yet run**
  - `workspace-valid` → **not yet run**
  - `every-criterion-has-a-test` → **not yet run**
  - `commits-reference-the-item` → **not yet run**
  - `no-unplanned-scope` (advisory) → **not yet run**
  - `claims-are-sourced` → **not yet run**
- **Artifacts:**
  - branch `wi/WI-0002`, at `55536ec`, no commits of its own yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation started. The branch exists and the item's status says so; no code has been written yet.

## 2026-08-27T00:37:31Z — implement v0.2.1 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, continuing this same execution — the opening entry above created the branch and moved the item before any code was written
- **Inputs read:**
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, worked in order
  - `tracker/items/WI-0002/item.md` — AC1–AC6, unchanged by this execution
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — B4 and B5, the exact `no payments needed` string and the `Ben pays Ana 10.00` line form
  - `docs/architecture/adr/ADR-0005-...md` — the settlement rule and the tie-break implemented in `settlement()`
  - `expenses/cli.py` — the `(command, action)` dispatch and `format_amount`'s use in the listings
  - `expenses/store.py` — the stored expense shape (`amount_minor`, `paid_by`, `shares_minor`), and that `load()` returns an empty dataset for a missing file without creating one, which is what AC5's second half rests on
  - `tests/test_cli.py` — the `CommandTestCase` fixture and the existing `subprocess.run` pattern AC4's test follows
- **Decisions:** all inside the plan's latitude; none of them changes what is delivered.
  - **Tie-break implemented as `max(pool, key=lambda e: (e[1], -recorded[e[0]]))`** — largest amount first, and among equal amounts the smaller recorded index. This is ADR-0005's rule stated as one expression rather than as a sort plus a scan, so there is one place to read it.
  - **Pools rebuilt by filtering rather than by removing entries.** After each transfer the two pools are re-derived with a comprehension that drops anything at zero. Chosen over `list.remove` because `remove` matches on equality and the entries are mutable lists; filtering cannot pick the wrong one.
  - **`positions()` guards membership with `if name in net`** before adding or subtracting. Today no dataset can name someone absent from `data["people"]` — `add_expense` refuses an unknown name — so the guard is unreachable through the CLI. It is there because the plan's fourth risk says WI-0004's deletion could create exactly that state, and the alternative is a `KeyError` in a report.
  - **`tests/test_settle.py` builds its datasets from two small helpers**, `expense()` and `dataset()`, shaped exactly as `store.add_expense` writes a record. The alternative was to build stores by running commands, which would have made the pure-function tests depend on a disk for no gain.
  - **AC3's five-person dataset is defined once in `tests/test_settle.py` and once in `tests/test_cli.py`**, rather than shared. The CLI one is built by running the real commands, which is what makes it end-to-end; sharing a literal would have removed the only thing that test adds.
  - **Escalated nothing.** No decision in this item met the marks — nothing here changes an interface another item depends on, contradicts an ADR, or decides user-visible behaviour no criterion covers. The two places a guess would have been tempting were both already decided: the settlement rule by ADR-0005, and the printed strings by refinement's B4 and B5.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → run after each of steps 1, 2, 3/5/6 and 7. Exit 0 at every step except the run between step 5 and step 6, which failed with 3 errors — AC6's README tests, which is the point of them. Final: **exit 0, `Ran 86 tests`, `OK`** (50 before this item)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 4 commit(s) on main..wi/WI-0002 name WI-0002`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 1 document, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `git diff main...wi/WI-0002 --stat` → 6 files changed, 437 insertions(+), 25 deletions(-)
  - Each criterion also run by hand on the branch head against fresh temporary stores; the outputs are quoted in `impl-report.md`
- **Gates:** all seven, on the branch head `b873060`, after the last change.
  - `tests-pass` → **pass** — `python3 -m unittest discover -s tests -t .`, `Ran 86 tests`, `OK`, exit 0
  - `lint-clean` → **skipped** — `commands.lint` is `null` in `tracker/project.yaml` and ADR-0004 records why: the project installs nothing and the standard library ships no linter. Nothing was run, so this is not a pass
  - `workspace-valid` → **pass** — `validate-workspace`, 7 items and 7 documents, 0 errors, 0 warnings
  - `every-criterion-has-a-test` → **pass** — AC1 → `WI0002AC1SettleListsThePayments` (1 test) and `SettlementTest::test_ac1_*` (2); AC2 → `WI0002AC2NothingToSettle` (3); AC3 → `WI0002AC3TheListSettlesTheGroupExactly` (6) and `SettlementTest`'s six matching function-level tests; AC4 → `WI0002AC4TheSameDataPrintsTheSameBytes` (1, two subprocesses compared as bytes); AC5 → `WI0002AC5SettleChangesNothing` (2, an md5 comparison and a non-existent path); AC6 → `WI0002AC6TheReadmeDocumentsTheCommand` (3). No criterion is demonstrated by reading the code. AC6's three were observed **failing** on the run between steps 5 and 6 and passing after step 6, which is direct evidence they test the behaviour rather than coexist with it
  - `commits-reference-the-item` → **pass** — `check-commit-refs WI-0002 wi/WI-0002` exit 0 over all 4 commits. Worth recording: the same gate run at `planned → in-progress`, when the branch had no commits, reported that `wi/WI-0002` was "already merged into main" and advised rewinding a merge that had never happened. The range was empty because nothing was committed yet, not because everything was merged
  - `no-unplanned-scope` (advisory) → **pass** — every hunk traces to a step. `expenses/settle.py` steps 1–2, `expenses/cli.py` step 3, the two test files steps 4–5, `README.md` step 6, `docs/architecture/overview.md` step 7. All 25 deletions are sentences saying who-owes-whom was not built yet, in the two places that said so
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0. Also worth recording: the run made after step 6, when `README.md` had been edited but not committed, reported "checked no documents changed since main" and exited 0. The gate's scope appears to be `docs/` only; the summary line claims a breadth it does not have
- **Artifacts:**
  - branch `wi/WI-0002`, commits `1e6853b..b873060` — four, off `main` at `55536ec`
  - `expenses/settle.py` (new, 60 lines), `expenses/cli.py` (a subparser, a handler, a dispatch entry), `tests/test_settle.py` (new, 20 tests), `tests/test_cli.py` (13 new tests plus 3 over the README), `README.md` (a `### settle` section and a corrected opening paragraph), `docs/architecture/overview.md` (v2 → v3)
  - `tracker/items/WI-0002/artifacts/impl-report.md` (new)
- **Status:** `in-progress` → `verifying`
- **Result:** The `settle` command is built and every criterion has a test. Four commits, six files, 50 tests to 86. The one decision that mattered was already made — ADR-0005 — and the implementation is it stated once, in one expression. Three deviations are declared in the report, all in how rather than what; nothing was escalated, no defect was found in delivered behaviour, and the two open bugs against WI-0001 were left alone.

## 2026-08-27T00:47:33Z — verify v0.1.3 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying` — `next` dispatched this skill as the status owner, WI-0002 being the highest-ranked runnable candidate (priority-rank 2, ahead of BUG-0002 at 3 and BUG-0001 at 4)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the six acceptance criteria, read **before** the implementation report so that the checks were derived from what was asked rather than from what was built
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps and the AC mapping, for the diff review
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria and after every check had been run, so that it was checked rather than followed
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - `docs/architecture/adr/ADR-0004-unittest-for-tests-and-no-lint-command.md` — why `commands.lint` is null
  - the code on `wi/WI-0002` at `6b2fb40989f413f09f0214bd76c74dab8a4e062a`: `expenses/settle.py`, the `settle` parts of `expenses/cli.py`, `README.md`, `docs/architecture/overview.md`, `tests/test_settle.py`, `tests/test_cli.py`, and `git diff main..wi/WI-0002`
- **Decisions:**
  - **No send-back and no bug item.** Every criterion passed on evidence gathered here, so neither escalation applies. The classification test in the procedure was never reached because there was no failure to classify.
  - **AC3's properties were checked against positions this skill recomputed from the raw stored JSON**, not against `expenses/settle.py`'s own `positions()`. Calling the function under test to check the function under test would have made five of AC3's clauses unfalsifiable: a wrong `positions()` would have produced a self-consistent wrong answer that every property still held over.
  - **`positions()` silently dropping a name present in an expense but absent from `data["people"]` is not a defect of this item.** No delivered command can reach that dataset (`add_expense` refuses unknown names, nothing deletes a person), no criterion of WI-0002 covers it, and it is already declared in both `plan.md` `## Risks` and `impl-report.md` `## What I did not do` as WI-0004's to solve. It is recorded in `verify-report.md` `## Defects found` as a looked-at-and-cleared item rather than left silent.
  - **AC1 cannot distinguish ADR-0005's tie-break, and that is the criterion's shape rather than a fault.** Mutation M1 reversed the tie-break and `WI0002AC1SettleListsThePayments` still passed, because AC1 compares *sorted* stdout. The behaviour is correct and the tie-break is pinned by two function-level tests that M1 did fail. Recorded as a qualification on the advisory gate, not as a verdict of `ambiguous`: the criterion is decidable, it simply decides less than the ADR fixes.
  - **M5 was strengthened to M5b rather than accepted.** Appending an empty string failed only one of AC5's two tests; the md5 test's sensitivity was unproven until the mutation actually changed a byte. Recording M5 alone would have overstated what the sensitivity check established.
  - **The verified commit is the branch head `6b2fb40`, not the `b873060` the implementation reported against.** `git diff --name-only b873060..HEAD` returns only `tracker/` paths, so the code is identical and the two sets of runs are comparable — checked rather than assumed, because D10 turns on it.
- **Questions raised:** none — no criterion was ambiguous and the record settled every reading that arose
- **Commands:**
  - `git rev-parse HEAD` → `6b2fb40989f413f09f0214bd76c74dab8a4e062a`; `git status --porcelain` → empty
  - `python3 -m unittest discover -s tests -t .` → `Ran 86 tests in 0.781s`, `OK`, exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 7 item(s), 7 document(s)`, `0 errors, 0 warnings`, exit 0
  - AC1: `person add Ana|Ben|Cara`, `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara`, `python3 -m expenses settle` → exit 0, `cat -A` shows `Ben pays Ana 10.00$` and `Cara pays Ana 10.00$`, `wc -l` → 2
  - AC2, three separate stores: untouched / two people no expense / `expense add --amount 10 --paid-by Ana --shared-by Ana` — `python3 -m expenses settle` in each → exit 0 and `no payments needed$` in all three
  - AC3: five `person add` then three `expense add` in the criterion's order, `python3 -m expenses settle` → exit 0, three lines, emitted `Cara pays Ana 9.33` / `Dan pays Ana 6.00` / `Ben pays Ana 1.33`
  - AC3 properties: a python script written here recomputing positions from `ac3.json` → `{Ana: 1666, Ben: -133, Cara: -933, Dan: -600, Eve: 0}`, sum 0; all five clauses `True`; the three amounts sum to 1666 = Ana's credit
  - AC4: `settle > run1`, `settle > run2` in two processes, `cmp run1 run2` → no output, exit 0
  - AC5: `md5sum` before/after a `settle` run → `ad65189c9362a13c953dee6d87db2a49` both times; `EXPENSES_STORE=$T/nested/does/not/exist.json python3 -m expenses settle` → exit 0, `no payments needed`, path still absent, `$T/nested` never created
  - AC6: `grep -n settle README.md` and `sed -n '85,120p' README.md` → `### settle` names the command at line 94, shows the two-line example, and states the `no payments needed` case
  - Sensitivity M1 (tie-break flipped) → `FAILED (failures=2)`; M2 (`no payments needed` → `nothing to do`) → `FAILED (failures=4)`; M3 (`net[name] -= 0`) → `FAILED (failures=11, errors=6)`; M4 (pid-parity reversal) → `FAILED (failures=1)` three times running; M5 (append `""`) → `FAILED (failures=1)`; M5b (append `"\n"`) → `FAILED (failures=2)`; M6 (README section deleted) → `FAILED (failures=3)`. Each reverted with `git checkout`; `git status --porcelain` empty and `Ran 86 tests ... OK` afterwards
  - `git diff main..wi/WI-0002 --stat` and `git diff main..wi/WI-0002 -- expenses/ README.md docs/` → every hunk traceable to a plan step
  - `git diff --name-only b873060..HEAD` → only `tracker/` paths
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → `all 6 commit(s) on main..wi/WI-0002 name WI-0002`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` on `6b2fb40` → `Ran 86 tests`, `OK`, exit 0; re-run after the last mutation was reverted → `OK`)
  - `lint-clean` → **skipped** (`commands.lint` is null in `tracker/project.yaml`; ADR-0004 records why. Nothing was checked, so it is not a pass; `verify-report.md` `## Not verified, and why` says what that leaves unchecked)
  - `workspace-valid` → **pass** (`validate-workspace .` → 0 errors, 0 warnings, exit 0)
  - `every-criterion-independently-checked` → **pass** (six rows in `verify-report.md` `## Criteria`, each a command run here with its actual output; AC3's properties recomputed from the raw JSON rather than from the code under test)
  - `negative-cases-exercised` → **pass** (AC2's three empty/zero stores and AC5's missing path each constructed and run; the equal-debt tie and the zero-position person exercised too — six conditions in `## Negative and boundary cases exercised`)
  - `tests-would-fail-without-the-change` (advisory) → **pass, qualified** (six mutations, each reverted; every criterion has at least one test that failed when its behaviour was disabled. The qualification: AC1's end-to-end test survives M1 because AC1 compares sorted output, so the tie-break is pinned only by `test_settle`'s two order tests)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` (new) — `Verified-commit: 6b2fb40989f413f09f0214bd76c74dab8a4e062a`, the six verdicts, the gates, the negative cases, the sensitivity table, and what was not verified
  - `tracker/items/WI-0002/item.md` — AC1 to AC6 ticked, each on a command run by this skill
  - no bug items filed
  - commit: `tracker: the verification report and the ticked criteria (refs WI-0002)`
- **Status:** `verifying` → `in-review`
- **Result:** All six acceptance criteria pass on evidence gathered here against `6b2fb40`, with the suite green at 86 tests and every criterion's behaviour shown to break at least one test when disabled. No defect was found and nothing was sent back. Four things are declared unverified — lint (no linter in this project), the hand-edited unsettled dataset, scale, and the multi-creditor tie-break, which no criterion of this item reaches.

## 2026-08-27T00:51:47Z — review-close v0.4.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review` — `next` dispatched this skill as the status owner, WI-0002 being the highest-ranked runnable candidate (priority-rank 2, ahead of BUG-0002 at 3 and BUG-0001 at 4)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (six rows, chaining without a gap, last row matching the status), `journal.md` **in full** (seven entries: `intake`, `answer-questions`, `refine`, `plan`, `implement` ×2, `verify`)
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - the diff `main..wi/WI-0002` — hunk by hunk, code, tests and docs separately, not the reports about it
  - `docs/architecture/adr/ADR-0005-settle-by-matching-the-largest-debt-to-the-largest-credit.md` in full, read against `expenses/settle.py`
  - `docs/architecture/overview.md` v3 and `README.md`, and the code each of their absolute claims cites — the D12 read
  - `tracker/project.yaml`; `.claude/agile-skills/spec/dor-dod.md` §3
  - WI-0002 has no questions of its own; the decisions it inherited are `EP-001/Q-002` and `WI-0001/Q-001`, both `answered`
- **Decisions:**
  - **Accept and close as `delivered`.** All twelve Definition of Done criteria pass with their own evidence; the per-criterion table is in `artifacts/review.md` and is this gate's evidence.
  - **Two findings, neither a send-back.** (i) `tests/test_settle.py`'s datasets hard-code the shares `store.py` computes (`334/333/333`), so they could drift from ADR-0003's rule while still passing — not worth a follow-up item, because `tests/test_cli.py` builds the same dataset with the real commands and would fail first, and because I confirmed the literals match the stored JSON today. (ii) AC1's end-to-end test cannot see ADR-0005's tie-break, since AC1 compares sorted stdout — `verify` found this by mutation and declared it; it is correct as written, so it is carried into the item's `## Notes` rather than sent back.
  - **Five declared gaps accepted, and all five written into `item.md` `## Notes`.** Lint checked nothing (null `commands.lint`, ADR-0004); the unsettled-dataset docstring claim is untested; `positions()` silently drops a name absent from `data["people"]`, which WI-0004 must solve when it adds deletion; scale is unexercised, consistent with `## Deliberately unconstrained`; and no acceptance criterion reaches ADR-0005's creditor-side tie-break. An accepted gap living only in a report stops being true without anyone noticing, so none of them was left there.
  - **No ADR is contradicted.** `max(pool, key=(amount, -recorded_index))` in `settle.py` is ADR-0005 step 4 exactly, and the ADR's two worked examples are the output the delivered command actually produces. Nothing to escalate to the architect.
  - **Closed before merging, deliberately.** `check-commit-refs` inspects the commits not yet on the trunk, so merging first would empty that range and make the gate refuse the very close it gates. Trial-merge → discard → close → merge, in that order.
  - **D12 was decided by opening each citation, not by reading the sentence.** Eight claims, including one *pre-existing* claim the new command could have falsified — "every refusal writes to stderr and exits non-zero" — which holds because `settle` returns through `main()`'s common `except ExpensesError` rather than a new path. That is the case D12 exists for: nobody was obliged to re-check a WI-0001 sentence while delivering WI-0002.
- **Questions raised:** none — nothing was ambiguous enough to need the architect, and this skill may not ask the human
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0, *"verified at 6b2fb409; wi/WI-0002 has moved to 04e662c2 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 7 commit(s) on main..wi/WI-0002 name WI-0002`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 1 document(s)`, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0, *"WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."*
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 7 documents, 0 errors, 0 warnings
  - `git checkout -b trial-merge-WI-0002 main`, `git merge --no-ff wi/WI-0002` → exit 0, clean; `python3 -m unittest discover -s tests -t .` **on the merge result** → `Ran 86 tests in 0.763s`, `OK`, exit 0; then `git checkout wi/WI-0002` and `git branch -D trial-merge-WI-0002` → `Deleted branch trial-merge-WI-0002 (was 34cdf54)`
  - `git diff main..wi/WI-0002 --stat`, and the diff read separately over `expenses/ README.md docs/` and over `tests/`
  - the D12 reads: the import block of every file in `expenses/`; `grep -rn "print(" expenses/` excluding `cli.py` → no output; `build_parser()` lines 46–56; `main()` lines 136–150
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each with its own result and evidence in `artifacts/review.md` `## Definition of Done`; no single verdict was written in place of the table)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the move from `6b2fb40` to `04e662c` is `tracker/`-only, which the script checked rather than I)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 7 commits)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 86 tests`, `OK`, exit 0, run on the trial merge into `main` — not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone: *what was built and why* — one read-only `settle` command answering EP-001's original question, `item.md` `## Story` and `plan.md` `## Problem`; *which skill decided what* — `refine` fixed the command name, the position definition, the output strings and the printed-list properties under EP-001/Q-002's explicit delegation (`refinement-qa.md` B1–B7), `plan` chose the settlement rule (ADR-0005) and where the code lives (`plan.md` `## Assumptions`), `implement` declared three deviations all in *how*; *what questions arose and how they were resolved* — none on this item, and the two it inherited, EP-001/Q-002 and WI-0001/Q-001, are `answered` with `## Consequences` naming real files; *what verification found* — six criteria passing on commands `verify` ran, six mutations proving the tests can fail, and four declared gaps
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0. Its scope is narrower than its summary line suggests — see `## Result` — so the eight-claim D12 table in `review.md` is what actually carries this)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` exit 0: WI-0002 is a work item. EP-001's own ending is not this execution's to record. `engagement-state EP-001` reported `active` before this run, with BUG-0001, BUG-0002, WI-0002 and WI-0004 in flight, so the engagement is not at rest and closing WI-0002 does not put it there)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new) — what was examined, the D12 claim table, the diff mapping, D1–D12, the findings, the accepted gaps, the verdict
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`, and a new `## Notes` subsection carrying the five accepted gaps and the AC1 tie-break fact
  - the merge of `wi/WI-0002` into `main`, made after this transition
  - commit: `tracker: the review, the closed item, and the merge (refs WI-0002)`
  - no bug filed, no question filed, no epic touched
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is delivered: `python3 -m expenses settle` prints the payments that settle the group, and EP-001's original question is now answerable by the tool. All twelve Definition of Done criteria pass with individual evidence, the trial merge into `main` was clean with 86 tests green, and five accepted gaps were moved out of the reports and onto the item so they survive the close. One toolkit note for whoever maintains the scripts: `lint-claims --changed-since main` reported `checked 1 document(s)` where four files carrying claims changed on this branch, so its summary line reads as broader coverage than it has.
