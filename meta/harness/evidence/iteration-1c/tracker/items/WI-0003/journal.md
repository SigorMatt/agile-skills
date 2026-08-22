# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T21:10:30Z — intake v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was
  created by that execution
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/items/` — empty before this execution, so `WI-0003` is a fresh allocation
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/question.md`
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — filed by this execution
- **Decisions:** see EP-001's entry of the same timestamp for how the work was split. Specific to
  this item: AC1 and AC2 were written to survive either answer to Q-001, so that the item is not
  invalidated by whichever the stakeholder picks — AC2 asks only that the printed amounts match
  what a reader computes by hand from a stated worked example, which is true of a pairwise report
  and of a settlement report alike. AC3 (owed total equals due total) was added as a check that
  holds under both readings and catches the arithmetic errors this kind of code actually makes.
  Rejected splitting "compute balances" from "print the report": neither half is observable on
  its own, so they would not be two items.
- **Questions raised:**
  - `Q-001` (blocking, to human) — pairwise debts as they arose, or the smallest set of
    settling transfers. Unanswered. Blocking because it decides what the command prints, and
    AC1's wording cannot be sharpened past its current deliberate vagueness without it.
  - `Q-002` (blocking, to human) — where the leftover pennies go when an amount does not divide
    evenly. Unanswered. Blocking because AC2 asks a reader to reproduce the amounts by hand, and
    they cannot do that unless the rounding rule is written down; it also decides whether amounts
    are stored as whole pence, which is expensive to change after data exists.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0003 --type work-item …` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to awaiting-answer --actor intake
    --resume-to draft --reason "Q-001, Q-002 blocking: …"` → exit 0
- **Gates:** the four gates in intake's contract were applied to this execution as a whole and
  are recorded, with their evidence, in EP-001's entry: `workspace-valid` → pass,
  `epic-has-success-measures` → pass, `items-are-separable` → pass, `no-solution-in-the-problem`
  → pass. For this item specifically, `items-are-separable` places it third, needing the expenses
  WI-0002 records.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/questions/Q-001.md`, `questions/Q-002.md` (new)
  - `tracker/items/WI-0003/journal.md`, `history.md` (new)
- **Status:** `—` → `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Created at `draft` and immediately suspended on two questions. This is the item
  that delivers the outcome the stakeholder actually asked for, and it is the one intake could
  say least about without them.

## 2026-08-21T21:23:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer`; the stakeholder answered Q-001 and Q-002 in the question
  files between turns, so this execution was run before `next` (which would otherwise have
  surfaced them as open human-addressed questions and stopped the loop).
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` (both with the stakeholder's `## Answer` filled in)
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/questions/Q-001.md` — the equal-shares answer, because the split rule depends on it
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/` — empty; no prior decision this could contradict
  - `tracker/items/WI-0003/artifacts/` — empty; no `plan.md` exists yet, so nothing to propagate into
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Q-001 — the report is a minimal settlement.** Route: recorded intent. The stakeholder's own
    words name the transfers ("the actual payments — who pays whom to settle up") and decline the
    pairwise reading, which is option B, not the recommended C. No ADR: nothing was derived, so
    an ADR would record the architect deciding something the stakeholder decided.
  - **AC1 gained a bound on the number of payments.** Rationale: "the smallest set of payments"
    is not decidable by observation, and a full pairwise listing also settles the group, so
    without a bound the criterion could be passed by exactly the output the stakeholder rejected.
    The bound chosen — at most `n - 1` payments for `n` people with a non-zero balance — is a
    property any greedy settlement achieves, so it constrains the output without committing
    `plan` to a particular algorithm.
  - **Per-person balances are not required to be printed.** Rationale: the stakeholder asked for
    payments and said the debt listing was not wanted; adding a printing requirement they did not
    state would be `answer-questions` designing rather than propagating. Left to `refine` as a
    presentation choice, and recorded as such in `## Notes` so it is not silently lost.
  - **Q-002 — decided by the architect, as ADR-0001.** Route: decided. The stakeholder read the
    question and handed it back ("go ahead anyway"), which is an authorisation to decide, not an
    escalation trigger; none of `spec/question.md` §4's four conditions is met by a choice the
    human has been shown and declined. Chose option B (whole pence; remainder handed one penny
    each to the sharers first in case-insensitive name order) because it is the only option that
    makes AC3's balance exact by construction while staying reproducible by hand for AC2, and it
    does not charge the payer for the arithmetic as option A does.
  - **Toolkit note, recorded because it will recur.** `validate-workspace` reports
    `question.awaiting.none-open` for the interval between marking an item's last blocking
    question `answered` and running `transition`. That interval is unavoidable for this skill —
    `spec/question.md` §3 requires the answer and its consequences to be written *before* the
    item is resumed — so the `workspace-valid` hard gate cannot pass at the instant it is
    nominally checked. It was checked after the transition instead, where it passes. The
    `transition` script itself does not treat this as blocking, and said so.
  - **The whole-pence representation was decided here rather than left to `implement`.**
    Rationale: it is the part of the decision that is expensive to reverse once data is on disk,
    and `spec/question.md` §1 makes irreversibility the property that decides where a choice
    belongs. ADR-0001 states the asymmetry explicitly.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (before the transition) → exit 1,
    2 errors: `board.stale`, and `question.awaiting.none-open` on WI-0003. Both are artefacts of
    the moment, not defects in this work — see the toolkit note under **Decisions**.
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to draft --actor answer-questions --reason "Q-001 and Q-002 answered and propagated: report is a settlement (item.md AC1/AC3), rounding fixed by ADR-0001 (AC6)"` → exit 0; the transition regenerated the board
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after the transition, run by `transition`) → exit 0, 0 errors, 1 warning (`project.commands.test-null`, pre-existing, owned by `plan`)
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in a `## Consequences` section was reopened
    after writing: `tracker/items/WI-0003/item.md` contains the rewritten AC1 and AC3, the new
    AC6, the new out-of-scope bullet and the rewritten `## Notes`;
    `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md`
    exists with the decision in `## Decision`; `docs/product/vision.md` is at v2 with the
    settlement wording in "What it is for" and both questions moved out of the open list;
    `tracker/items/WI-0002/item.md` `## Notes` cites ADR-0001.
  - `answered-from-the-record` → **pass**. Q-001 cites the stakeholder's answer verbatim; Q-002
    states the record was silent on the stakeholder's preference, that they declined to supply
    one, and records the new decision as ADR-0001.
  - `escalation-is-justified` → **skipped**. No question was re-addressed to the human by this
    execution, so the gate has nothing to check. The reason for *not* escalating Q-002 is under
    **Decisions** above.
  - `workspace-valid` → **pass**, checked after the transition (`validate-workspace`, exit 0, 1
    pre-existing warning). Before the transition it failed with `question.awaiting.none-open`;
    that state is required by the protocol and clears the moment the item is resumed. See the
    toolkit note under **Decisions**.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:12:35Z, `draft` →
    `awaiting-answer`, actor `intake`) records `resume-to: draft`; this execution transitioned to
    `draft`.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/WI-0003/questions/Q-002.md` — answered, `answered-by: answer-questions`, consequences listed
  - `tracker/items/WI-0003/item.md` — AC1, AC2, AC3 amended; AC6 added; out-of-scope and notes rewritten
  - `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md` — created (v1)
  - `docs/product/vision.md` — v1 → v2
  - `tracker/items/WI-0002/item.md` — `## Notes` cites ADR-0001 (that item's own answer is a separate execution)
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both questions answered and propagated; the report is a settlement of payments and
  the money rule is fixed by ADR-0001. WI-0003 returns to `draft` for `refine`, which still has
  to pin the command name, the output wording and the worked example AC2 names.

## 2026-08-21T21:38:20Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** not dispatched by `next` — `next` dispatched `refine` on WI-0001 this run. This
  entry records a question filed as part of that execution's batch, under the standing rule for
  this project that when the pipeline is about to stop on a human-addressed question, every
  question already known to be needed is filed in the same round trip. `item.md` is untouched.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md`, `questions/Q-001.md`, `Q-002.md`
  - `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md` (v1)
  - `docs/product/vision.md` (v5)
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **One question filed: Q-003, whether the report also prints each person's balance.** This is
    not a question refinement invented. When `answer-questions` propagated Q-001 it deliberately
    added no requirement the stakeholder had not stated, and recorded in this item's `## Notes`
    that whether to print balances is a presentation choice for `refine`. It is an R10 failure as
    it stands: the report's content beyond the transfers is neither required, nor excluded, nor
    recorded as deliberately unconstrained.
  - **The question spells out that a per-person balance is not the pairwise listing the
    stakeholder declined.** Rationale: they rejected "every individual debt listed out", and the
    obvious risk is that they read this question as re-asking Q-001 and reject it again for the
    wrong reason. One line per person is a different artifact from one line per pair, and the
    question says so with both shapes written out.
  - **AC2's checkability is the reason this is worth their attention at all.** AC2 asks a reader
    to reproduce the report's amounts by hand; the balances are the working that makes that
    feasible. That argument is in the question so the recommendation is not a matter of taste.
  - **Nothing else on this item was asked.** The command name and the exact output wording are
    the same "documented command" gap as WI-0001, asked once at WI-0001/Q-001. The worked example
    AC2 names is refinement's to construct from ADR-0001, not the stakeholder's to supply.
- **Questions raised:** `Q-003` (blocking, to `human`). No `artifacts/refinement-qa.md`: no
  exchange has taken place, and this item has not been refined.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to awaiting-answer --actor refine --resume-to draft --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after all four suspensions) → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 once every item carrying a new
    blocking question had been suspended).
  - `definition-of-ready` → **not evaluated in full**. This execution did not attempt to make
    WI-0003 Ready. The criterion it did assess is **R10 fail** — what the report prints besides
    the transfers is stated nowhere. Q-003 exists to clear it.
  - `criteria-are-decidable` → **not evaluated**. No criterion was rewritten by this execution.
    Note for the execution that does refine this item: AC1 to AC6 were already sharpened by
    `answer-questions` on 2026-08-21T21:23:00Z and are in better shape than a fresh draft; what
    they still lack is the command name, which WI-0001/Q-001 covers.
  - `qa-recorded-verbatim` → **skipped**. There is no exchange to record.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-003.md` (new)
  - `tracker/items/WI-0003/item.md` — **unchanged**, deliberately
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** One blocking question filed on whether the report prints per-person balances
  alongside the transfers. The item is suspended and returns to `draft` when it is answered.

## 2026-08-21T21:46:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer`; the stakeholder filled in Q-003's `## Answer` between
  turns, so this execution was run ahead of `next`.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-003.md` (answered by the stakeholder), `Q-001.md` and
    `Q-002.md` (both answered earlier — the settlement reading, and the rounding rule)
  - `tracker/items/WI-0003/item.md` (AC1–AC6, `## Out of scope`), `history.md`
    (`resume-to: draft`), `journal.md`
  - `docs/architecture/adr/ADR-0001` (v1, money in pence and the split rule), `ADR-0002`,
    `ADR-0003`, `ADR-0005` (all v1, written earlier this turn)
  - `docs/product/vision.md` (v7, "Not multi-currency"), `tracker/items/EP-001/item.md` (SM1)
  - `tracker/items/WI-0003/artifacts/plan.md` — **does not exist**; nothing planned yet
- **Decisions:**
  - **Q-003 answered by the stakeholder, option B, verbatim**: "show each person's balance too,
    not just the payments — makes it easier to check." Route: recorded intent, `answered-by:
    human`. No ADR: the decision is theirs.
  - **Balances first, payments second.** Their stated reason is the hand-check, and the payments
    are derived from the balances, so that is the order a reader works in. AC7 fixes the order
    rather than leaving it to `implement`, because AC2 asks a reader to reproduce the report and
    an unordered report cannot be reproduced.
  - **Everyone registered gets a balance line, including the square.** Omitting people who owe
    nothing would make a registered person invisible, and nothing else in this epic can show a
    person's standing.
  - **The amount format was answered from an existing document, not decided.** Two decimal places
    and no currency symbol follows from `docs/product/vision.md` ("the tool does not name it") and
    ADR-0001 (minor units internally, formatted at the boundary). It is written into AC7 only
    because `verify` needs a concrete string to compare.
  - **Nothing pairwise was added.** The stakeholder declined the per-pair listing in Q-001 and the
    question was careful to distinguish it; the item's `## Out of scope` is unchanged and the notes
    say explicitly that a balance line is per person, never per pair.
  - **Criteria changed:** **AC7 added**, AC4 amended to say an empty report prints no balance lines
    and to name ADR-0005's stream and exit code. Journalled because this skill is one of only two
    that may change a criterion; both changes add requirements the answer created.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to draft --actor answer-questions --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, both files reopened after writing.
    `tracker/items/WI-0003/item.md` carries AC7 with the three line forms, the ordering and the
    zero-sum property, an amended AC4, and `## Notes` recording the answer.
    `docs/product/vision.md` is at v8, "What it is for" describing balances plus payments, with a
    change-log row.
  - `answered-from-the-record` → **pass**. The stakeholder's own sentence for the decision;
    `docs/product/vision.md` and ADR-0001 for the amount format; WI-0003/Q-001 for what stays
    excluded.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:31:44Z, `refine`)
    records `resume-to: draft`; this execution transitioned WI-0003 to `draft`.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-003.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/WI-0003/item.md` — AC7 added, AC4 amended, `## Notes` extended
  - `docs/product/vision.md` — v7 to v8
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** The report will print each person's balance and then the payments that settle them.
  WI-0003's last open question is closed and the item is back at `draft` for `refine`, which still
  has to pin the command name, the exact wording and the worked example AC2 names.

## 2026-08-21T22:31:30Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — WI-0001 and WI-0002 are closed, making this
  the highest-ranked runnable item (rank 2; WI-0004 is rank 3)
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC7 as `answer-questions` left them, `## Out of scope`,
    `## Notes`), `history.md` (a fresh draft returned by `answer-questions`, not a send-back),
    `journal.md` (all four prior entries)
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all answered
  - `docs/architecture/adr/ADR-0001` (the split rule and its worked example), `ADR-0002`,
    `ADR-0003`, `ADR-0005`, `ADR-0009` (what a stored expense holds); `docs/architecture/overview.md`
    (v2); `docs/product/vision.md` (v9)
  - `tracker/items/WI-0001/item.md` and `WI-0002/item.md` — for the criterion style, the exact
    command surface now delivered, and what an expense actually stores
  - The delivered code: `expenses_tool/expenses.py` and `cli.py`, to check that the report this
    item specifies can be computed from the records that exist rather than from imagined ones
- **Decisions:**
  - **No question was filed.** The gaps were the command name, the two sections and their order,
    the exact line forms, the payment ordering and the empty-report message — all conventions the
    stakeholder delegated on WI-0001/Q-004 and that ADR-0002 and ADR-0005 bind this item to. The
    three substantive product questions on this item were all answered by the stakeholder already.
  - **The report shape was defined once, above the criteria**, and AC2 and AC6 quote complete
    expected output including the blank line. Two criteria asking a reader to reproduce figures by
    hand are only decidable against a fixed layout.
  - **The worked example is written into AC2 with its arithmetic.** It was previously "a stated
    worked example", which meant `verify` would have had to invent one — and an invented example
    cannot be reproduced by a reader who was not there.
  - **A second worked example was written into AC6**, the indivisible case: `10.00` three ways is
    `3.34`, `3.33`, `3.33`, so the report reads `Ana is owed 6.66` and two payments of `3.33`. This
    is where ADR-0001 becomes observable rather than theoretical, and it is checked arithmetically:
    `666 = 1000 - 334`, and `333 + 333 = 666`.
  - **Payments are sorted by payer then payee for output.** This was the one place where making the
    criteria decidable risked constraining `plan`'s algorithm. Sorting the *printed* lines does not:
    any algorithm that produces a settlement can sort its output, and both worked examples have a
    unique settlement anyway.
  - **`Nobody owes anybody` covers both empty cases**, including "expenses exist but everyone is
    square", which no criterion previously mentioned — a report that printed balances and then
    stopped would read as truncated.
  - **Two criteria were added that no earlier version had**: AC8, that registering someone after
    the fact does not change a recorded expense's shares (the report-side counterpart of WI-0002's
    snapshot, and the place a lazy implementation would recompute from the current people list),
    and AC9, that the report never writes the ledger and is repeatable. Neither was stated
    anywhere, and both are behaviour a reader would assume.
  - **`## Out of scope` gained two entries**: no explanation of a payment (netting means a payment
    corresponds to no single expense, so an explanation would be misleading exactly when it is most
    wanted — this is option C from Q-003, which the record already rejects), and no options on
    `report` beyond `--data-file`.
  - **Three behaviours left unconstrained and named (R10):** which minimal settlement is printed
    when several exist, `argparse`'s usage wording, and behaviour with a very large group. The
    first is the interesting one — it is left to `plan` deliberately, because pinning it here would
    choose an algorithm from the analyst's chair.
- **Questions raised:** none this execution. The three answered questions are recorded verbatim in
  `artifacts/refinement-qa.md` with seven `[assumed]` decisions and three `[unresolved]` entries.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to ready --actor refine --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, before and after).
  - `definition-of-ready` → **pass**, criterion by criterion:
    **R1 pass** — frontmatter complete; `priority: high`, `epic: EP-001`.
    **R2 pass** — the story names the role, the capability and the "so that".
    **R3 pass** — AC1 to AC9, each a labelled checkbox.
    **R4 pass** — was failing: AC1, AC2 and AC4 said "a documented command" and AC2 referred to a
    worked example that did not exist. Every criterion now names `./expenses report` and quotes its
    exact expected output, including two complete reports.
    **R5 pass** — `## Out of scope` names six things, two added here.
    **R6 pass** — no open question; Q-001, Q-002 and Q-003 are all answered.
    **R7 pass** — no `depends-on`. The report needs expenses, and WI-0002 is `done`, so the
    dependency is satisfied in fact as well as in the epic's stated order.
    **R8 pass** — was failing: no `artifacts/refinement-qa.md` existed. It now records all three
    stakeholder answers verbatim, including the one where they rejected the recommendation and the
    one where they declined to choose, plus seven assumptions and three unresolved entries.
    **R9 pass** — computing balances and printing a settlement is one coherent change reading
    records WI-0002 already writes.
    **R10 pass** — the combinations are visible: no expenses (AC4), expenses that settle to zero
    (AC4), an even split (AC2), an indivisible split (AC6), a person who shared in nothing (AC7,
    AC8), records written in earlier invocations (AC5), and repeated runs (AC9). Three are named as
    deliberately unconstrained in `## Notes`, and one is recorded there as unable to arise.
  - `criteria-are-decidable` → **pass**. AC1: run `report`, count the payment lines, check each
    against the balances. AC2: build the worked example with three `add-person` and two
    `add-expense` calls, run `report`, compare the whole output to the four quoted lines. AC3: sum
    the payment amounts in each direction and apply them to the printed balances. AC4: run against
    an empty file, compare to `Nobody owes anybody`; then build a settled ledger and compare again.
    AC5: build the example across three invocations, run `report` in a fourth. AC6: one `10.00`
    expense, compare the whole output to the five quoted lines. AC7: check the line forms, the
    order and that the amounts sum to zero. AC8: build the example, `add-person Dan`, compare to
    AC2's output plus `Dan is square`. AC9: `cmp` the data file before and after, and compare two
    consecutive runs.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` carries all three questions with
    the options each offered and the stakeholder's answers copied unaltered — including "Not sure
    yet — go ahead anyway", which is recorded as the declination it was rather than as agreement
    with the recommendation. What refinement decided is separated from what they said, with the
    delegation each assumption rests on named.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0003/item.md` — AC1 to AC7 rewritten, AC8 and AC9 added, the report shape and
    the worked example defined above the criteria, `## Out of scope` extended, `## Notes` extended
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0003 is Ready. Nine criteria, two of which quote a complete expected report; the
  arithmetic a reader must be able to redo is written down in both the even and the indivisible
  case; and which settlement to print when several are minimal is left to `plan`, named, rather
  than decided from the analyst's chair.

## 2026-08-21T22:34:30Z — plan v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC9, the report shape and the worked example defined above
    them, `## Out of scope`, `## Notes` including the three behaviours left unconstrained),
    `history.md`, `journal.md`, `artifacts/refinement-qa.md` (seven `[assumed]`, three
    `[unresolved]` — the first of which is this plan's main decision), `questions/Q-001.md`,
    `Q-002.md`, `Q-003.md`
  - `docs/architecture/adr/ADR-0001` (clause 2's split and its worked example, clause 3's balances),
    `ADR-0002`, `ADR-0003`, `ADR-0005`, `ADR-0007`, `ADR-0008`, `ADR-0009`;
    `docs/architecture/overview.md` (v2); `docs/product/vision.md` (v9)
  - **The code:** `expenses_tool/expenses.py` (what a stored expense holds and how `list_expenses`
    reads it), `expenses_tool/money.py` (`format_amount`), `expenses_tool/store.py` (`normalise`,
    `load`), `expenses_tool/cli.py` (the parent-parser pattern and `render_expense`), and
    `tests/test_cli_expenses.py` for the shape of a criterion test
- **Decisions:**
  - **ADR-0010 written: the settlement is greedy, largest debtor to largest creditor, tie-broken by
    name, and its output is sorted for printing.** Route: decided — `refine` explicitly left this
    to `plan` and named it as unconstrained, which is as clear a hand-off as the protocol produces.
    A provably minimal settlement is NP-hard and worth nothing to a friend group; the criteria ask
    for `n-1`, which greedy achieves by construction because every payment zeroes somebody.
  - **The print order is fixed in the ADR, not just the algorithm.** Sorting the emitted payments by
    payer then payee is what makes the report deterministic for identical data, and therefore what
    makes any criterion over it reproducible. Without it, AC2 would be checking an artefact of the
    loop.
  - **`settle.py` computes and `cli.py` renders**, per ADR-0008 clause 3. The three line forms
    (`is owed`, `owes`, `is square`) and the payment form live in `cli.py` with every other
    user-visible string.
  - **Two code paths produce the same sentence.** `Nobody owes anybody` is printed alone when no
    expense exists, and after the balances when expenses exist but everyone is square. AC4 asks for
    both, and conflating them would print a bare sentence for a group with a full ledger.
  - **This item adds no stored state and does not touch `store.py`.** The report is a pure function
    of what WI-0002 already writes, which is also why AC9 is cheap to satisfy: `cmd_report` never
    calls `store.save`.
  - **AC8 needs no work, and is worth testing anyway.** The sharers come from the stored record
    (ADR-0009 clause 3), so registering someone later cannot change a past expense. The risk
    section says why the criterion earns its place regardless: the natural shortcut in a report is
    to recompute "everyone" from `data["people"]`, and this is the test that would catch it.
  - **A payer who is not a sharer is covered by a unit test, not by a criterion.** Every example in
    the item has the payer sharing; the case is easy to get wrong (credited in full, debited
    nothing) and the plan puts it in step 7 rather than leaving it to chance.
  - **Four assumptions recorded** (route: assumed, all reversible): a zero-balance person never
    appears in a payment, the blank line is a single `print()`, `balances` keys off
    `data["people"]`, and the two empty cases are separate paths.
  - **`docs/architecture/overview.md` bumped to v3** for the new module, the new command, and a
    short section stating that the report stores nothing — the property AC9 checks and the one a
    later item could break without noticing.
- **Questions raised:** none. The one decision that could have needed the stakeholder — what the
  report *is* — they made themselves in Q-001, and the one `refine` could not settle was handed to
  `plan` by name rather than escalated.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to planned --actor plan --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `every-criterion-is-addressed` → **pass**. One row per criterion, AC1 to AC9, each naming the
    steps that satisfy it and a specific test — `AC1::test_payments_settle_and_are_bounded`,
    `AC2::test_worked_example`, `AC3::test_totals_match_and_balances_clear`, `AC4::test_no_expenses`
    and `AC4::test_everyone_square`, `AC5::test_reads_earlier_invocations`,
    `AC6::test_indivisible_split`, `AC7::test_balance_lines_and_order`,
    `AC8::test_late_person_changes_nothing`, `AC9::test_report_does_not_write_and_repeats` — plus
    two property tests in `test_settle.py` for the bound and for the clearing. No row says "tests".
  - `project-commands-resolved` → **pass**. Both commands are set and have been run repeatedly in
    this project; `commands.build` stays `null` per ADR-0007 clause 5.
  - `decisions-recorded` → **pass**. ADR-0010 created with context, four options and their costs and
    risks, a five-clause decision, and consequences including reversibility. Everything else is
    cited to an existing ADR in `## Decisions and ADRs`.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new) — ten steps, nine mapped criteria, four
    assumptions, five named risks
  - `docs/architecture/adr/ADR-0010-greedy-settlement-largest-creditor-first.md` (new)
  - `docs/architecture/overview.md` — v2 to v3
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0003 has a plan that settles the one thing refinement deliberately left open — which
  settlement to print — and records it as ADR-0010 with its tie-break and print order, so the report
  is deterministic and every quoted expected output in the criteria is reproducible.

## 2026-08-21T22:38:00Z — implement v0.1.1 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next`; no branch existed, so a fresh implementation.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC9, the report shape and both worked examples quoted
    above the criteria, `## Notes`), `history.md`, `artifacts/plan.md` (ten steps and the mapping
    table), `artifacts/refinement-qa.md`; the three answered questions
  - `docs/architecture/adr/ADR-0001` (clauses 2 and 3), `ADR-0003`, `ADR-0005`, `ADR-0008`,
    `ADR-0009`, `ADR-0010`; `docs/architecture/overview.md` (v3)
  - **The code:** `expenses_tool/store.py` (`normalise`, `load`), `expenses_tool/money.py`
    (`format_amount`), `expenses_tool/expenses.py` (the stored record), `expenses_tool/cli.py`
    (the parent parser, `_refuse`, `render_expense`), `tests/test_cli_expenses.py` (test shape)
- **Decisions:** all inside the plan's latitude.
  - **`settle.settle` returns payments in emission order and `cli.py` sorts them.** ADR-0010 clause
    4 puts the print order in the caller, and keeping the module's return unsorted makes it obvious
    in the tests that the sort is a presentation step rather than part of the algorithm.
  - **`NOBODY_OWES` is one constant used by both branches.** AC4 requires the same sentence in two
    different situations; a constant makes that a fact rather than an intention.
  - **`balances` seeds every registered person at zero before applying expenses**, so AC7's "a
    person who shared in nothing appears as `is square`" falls out rather than being special-cased,
    and so does AC8.
  - **The tie-break in `settle` sorts by amount descending, then by `store.normalise`.** Without the
    name tie-break, two people owing the same amount would settle in dictionary order, which is
    stable in CPython but not something a criterion should rest on.
  - **Three property tests were written rather than more examples**: shares always sum to the
    amount, payments always clear the balances, and the payment count never exceeds `n-1` — the
    last over every zero-sum split of six units among four people. The bound in AC1 is a claim about
    all data, and examples cannot establish it.
  - **`test_cli_report.py` parses the printed report** to check AC1 and AC3, rather than calling
    `settle` directly. The criteria are about what the report prints, and a test that bypassed the
    rendering would not notice a balance line that disagreed with the payments beneath it.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 87 tests`, `OK` (run after each
    module and again on the branch head)
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003 --root . --trunk main` → all commits name WI-0003
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `transition WI-0003 --to in-progress …` and `--to verifying …` → exit 0
  - Smoke checks before the tests existed: `./expenses report` against an empty file →
    `Nobody owes anybody`; the worked example → the four AC2 lines; the `10.00` example → the five
    AC6 lines
- **Gates:** run on the branch head, after the last change.
  - `tests-pass` → **pass**. 87 tests, exit 0.
  - `lint-clean` → **pass**. `compileall`, exit 0; a syntax check rather than a style linter
    (ADR-0007 clause 4).
  - `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
  - `every-criterion-has-a-test` → **pass**. One class per criterion in `tests/test_cli_report.py`
    (`AC1` to `AC9`), with AC1, AC3, AC7 and AC9 additionally asserting properties of the printed
    output rather than fixed strings, because those criteria are about relationships rather than
    text.
  - `commits-reference-the-item` → **pass**, as above.
- **Artifacts:**
  - `expenses_tool/settle.py` (new); `expenses_tool/cli.py` — three functions, one constant and one
    subparser added
  - `tests/test_settle.py`, `tests/test_cli_report.py` (new)
  - `README.md` — "Who owes whom" section
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0003/item.md` — `branch: wi/WI-0003` recorded
  - branch `wi/WI-0003`, head `a830980`
  - `tracker/board.md` — regenerated
- **Status:** `in-progress` → `verifying`
- **Result:** `./expenses report` prints the balances and the payments that clear them, reproducing
  both of the criteria's quoted reports exactly. 87 tests pass on the branch head, three of them
  property tests over generated data, and two deviations from the plan are declared.

## 2026-08-21T22:41:30Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next`
- **Verified commit:** `e8a82310b21ca9b46afc6571f287b35c8f71a64f`, the head of `wi/WI-0003`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the nine criteria **first and in full**, with the two quoted
    reports and what would settle each criterion written down before `impl-report.md` was opened;
    `history.md`; `artifacts/plan.md`; `artifacts/impl-report.md` (afterwards);
    `artifacts/refinement-qa.md`; the three answered questions
  - `docs/architecture/adr/ADR-0001`, `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0009`, `ADR-0010`;
    `docs/architecture/overview.md` (v3)
  - The code and the diff: `expenses_tool/settle.py`, the three additions to `cli.py`, both new test
    modules, `README.md`, `git diff --stat main..HEAD`, and the `item.md` diff
- **Decisions:**
  - **AC1 and AC3 were checked on data the criteria do not mention** — a four-person ledger with
    three expenses, one of them indivisible — rather than only on the worked example. Both are
    claims about arbitrary data, and the worked example has a unique one-payment settlement that
    would hide almost any error.
  - **AC7 was checked with a group whose alphabetical and registration orders differ** (`Cass`,
    `ana`, `Ben`, `Dan`). An implementation sorting by insertion order or by ASCII would pass a
    tidier example and fail this one.
  - **AC9's test was found to be insensitive, and the behaviour was checked another way.** Adding
    `store.save(path, data)` to `cmd_report` broke no test — because the file is rewritten with
    identical content, and AC9 asks only that `cmp` show it unchanged. I checked `stat`'s inode,
    mtime and size before and after (identical; the inode changes on a real write, since ADR-0006
    replaces the file), and read `cmd_report` for `store.save` (absent). AC9 therefore passes on its
    own terms **and** on a stricter test.
  - **That insensitivity was recorded, not fixed.** Amending a criterion is not this skill's job,
    and the delivered behaviour is right. It is flagged in the report and in `## Not verified` so
    `review-close` sees it, rather than being quietly absorbed into a green tick.
  - **Nothing was classified as a bug.** Nothing failed, and nothing was found in behaviour
    delivered by WI-0001 or WI-0002.
  - **Six gaps declared**, including one new: a hand-edited ledger naming a sharer who is not in
    `people` would be reported rather than refused. ADR-0009 clause 5 says it cannot arise through
    the tool; it can arise through a text editor, and the record should say that was considered.
- **Questions raised:** none.
- **Commands:** (all run by this skill, on the verified commit)
  - `git rev-parse HEAD`; `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 87 tests`,
    `OK`; `python3 -m compileall -q …` → exit 0; `validate-workspace` → exit 0
  - AC4 (empty): `./expenses report` → `Nobody owes anybody`, `exit=0`
  - AC2/AC5: the example built in separate `bash -c` processes; `report | cat -A` →
    `Ana is owed 15.00$`, `Ben is square$`, `Cass owes 15.00$`, `$`, `Cass pays Ana 15.00$`
  - AC9: `cmp` → unchanged; `diff` of two runs → identical; `stat` → `inode=6987881 mtime=1787351689
    size=495` before and after, versus `inode=6987886` after a deliberate `add-person`;
    `grep -n "store.save" expenses_tool/cli.py` → lines 56 and 132 only (`add-person`, `add-expense`)
  - AC8: `add-person Dan` then `report` → the AC2 report with `Dan is square` inserted
  - AC6: the `10.00` example → the five quoted lines
  - AC7: `Cass`, `ana`, `Ben`, `Dan` → `ana is owed 20.00`, `Ben owes 10.00`, `Cass owes 10.00`,
    `Dan is square`
  - AC4 (settled): Ana pays `10.00` for her own lunch → `Ana is square`, `Ben is square`, blank,
    `Nobody owes anybody`
  - AC1/AC3: the four-person ledger → `balances sum: 0`, `paid total == received total: True`,
    `after payments, all zero: True`, `payments=3 nonzero=4 bound_ok=True`
  - Sensitivity: four edits, each followed by the test command and `git checkout -- expenses_tool`
    → `FAILED (failures=32)`, `FAILED (failures=6)`, `FAILED (failures=1)`, and **`OK`** for the
    fourth, which is the finding above
  - `transition WI-0003 --to in-review --actor verify …` → exit 0
- **Gates:**
  - `tests-pass` → **pass**. 87 tests, exit 0, on the verified commit.
  - `lint-clean` → **pass**, with the standing qualification (`compileall` is a syntax check).
  - `workspace-valid` → **pass**. Exit 0.
  - `every-criterion-independently-checked` → **pass**. Nine rows, each with a command and quoted
    output; the ticks were applied only afterwards.
  - `negative-cases-exercised` → **pass**. Both empty cases, the indivisible split inside a larger
    ledger, a non-sharing person, a late-registered person, and repeated runs.
  - **Test sensitivity** (step 5) → **pass with one finding**: three of four edits failed the suite;
    the fourth did not, and that gap is reported rather than hidden.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` (new), carrying `Verified-commit:`
  - `tracker/items/WI-0003/item.md` — all nine criteria ticked
  - bug items filed: none
  - `tracker/board.md` — regenerated
- **Status:** `verifying` → `in-review`
- **Result:** The report does what WI-0003's criteria say, checked command by command against
  `e8a8231`, including both quoted reports reproduced exactly and the arithmetic re-derived by hand
  on a ledger the criteria do not mention. One weakness in AC9's construction is reported for
  `review-close`: the criterion cannot detect a write that changes nothing, so the behaviour was
  established by inode and mtime instead.

## 2026-08-21T22:44:30Z — review-close v0.1.1 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (nine rows), `journal.md` **in full** (eight
    entries), the three answered questions
  - `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md` — the last read
    closely, because its `## Test sensitivity check` contains a finding rather than a formality —
    and `artifacts/refinement-qa.md`
  - `docs/architecture/overview.md` (v3) re-read against the code for D12; ADR-0001, ADR-0003,
    ADR-0005, ADR-0008, ADR-0009, ADR-0010; `README.md`
  - **The diff:** `git diff main..HEAD` hunk by hunk over `settle.py`, the `cli.py` additions, both
    test modules and the README, plus the `item.md` diff to confirm no criterion was touched by
    `implement`
- **Decisions:**
  - **Accepted.** Every hunk maps to a plan step and a criterion; the table is in
    `artifacts/review.md`.
  - **`verify`'s AC9 finding was re-checked, not taken on trust, and then classified.** The
    criterion says `cmp` must show the file unchanged; a write of identical bytes satisfies it, so
    neither the criterion nor its test can detect a report that writes. That is a defect in the
    **criterion**. It is not a send-back — the delivered behaviour is correct, and asking a
    developer to fix nothing is worse than useless — and it is not mine to amend, since only
    `refine` and `answer-questions` may change a criterion. It is written into the item's `## Notes`
    with what a future execution should do about it, which is the only form in which it survives
    closure.
  - **The two same-sentence exits in `cmd_report` were reviewed as correct and noted anyway**, so
    that a later reader does not collapse them into one branch and print balances for an empty
    ledger.
  - **Seven gaps copied into the item**, including the AC9 insensitivity and one about how the
    product will actually be used: the report describes the ledger and does not know that anyone has
    settled up. That is EP-001's scope, and it is the thing most likely to surprise a real user, so
    it belongs on the item rather than only in the README.
  - **D12 was a read, not a recollection.** The overview's new "What the report does" section
    claims the report stores nothing; I checked `cmd_report` and grepped for `store.save`. The
    README's worked example was run as written and produced exactly the output it shows.
  - **Trial-merge, discard, close, then merge**, in that order, for the reason the skill gives.
  - **The epic stays `open`.** WI-0004 remains at `draft` and cannot pass the Definition of Ready
    until the stakeholder supplies the CSV sample, which `tracker/items/EP-001/item.md` `## Scope`
    already records. Three of the four children are now `done`.
- **Questions raised:** none. The AC9 finding is a criterion weakness with correct behaviour behind
  it, not a contradiction with an ADR, so there was nothing to put to the architect.
- **Commands:**
  - `check-verify-freshness WI-0003 wi/WI-0003` → *"verified at e8a82310; … only the record
    changed (5 file(s) under tracker/ or docs/)"*
  - `git branch -f trial-wi3 main; git checkout trial-wi3; git merge --no-edit wi/WI-0003` → clean;
    on the merge result `unittest discover` → exit 0, `Ran 87 tests`, `OK`, and `compileall` → exit
    0; then `git checkout wi/WI-0003; git branch -D trial-wi3`
  - `check-commit-refs WI-0003 wi/WI-0003` → *all 3 commit(s) … name WI-0003*
  - `grep -n "store.save" expenses_tool/cli.py` → lines 56 and 132 only, both in the two `add-`
    commands
  - `validate-workspace` → exit 0; `transition WI-0003 --to done --actor review-close --outcome
    delivered …` → exit 0; then `git checkout main; git merge --no-ff wi/WI-0003`
- **Gates:**
  - `definition-of-done` → **pass**, criterion by criterion, with the table in `artifacts/review.md`:
    D1 nine ticks; D2 nine evidence rows; D3 gates on `a830980`, `e8a8231` and the merge result; D4
    three answered questions; D5 eight entries against eight actors; D6 ADR-0010 cited from the
    plan, the overview and `settle.py`'s docstring; D7 overview v2→v3 and the README extended; D8
    `check-commit-refs` clean; D9 merged after closing; D10 `check-verify-freshness` clean; D11 this
    review's `## What I examined`; D12 the overview's report claim and the README's worked example
    both checked against the code.
  - `verification-postdates-the-code` → **pass**, quoted above.
  - `commits-reference-the-item` → **pass**, run while the branch was unmerged.
  - `tests-pass-on-the-merge-result` → **pass**. 87 tests and `compileall` on the throwaway merge.
  - `workspace-valid` → **pass**. Exit 0.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0003`:
    what was asked (the three stakeholder answers, including the one where they rejected the
    recommendation), who decided what (eight journal entries; ADR-0001 and ADR-0010), what was built
    (`plan.md`, `impl-report.md`), what verification found (`verify-report.md`, with quoted output,
    four sensitivity checks and the AC9 finding), and what remains unchecked (seven accepted gaps on
    the item).
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` (new)
  - `tracker/items/WI-0003/item.md` — `status: done`, `outcome: delivered`, `## Notes` gains
    "Accepted gaps at close" including the AC9 insensitivity
  - merge commit on `main`: see `git log --grep WI-0003 --merges`
  - epic: **not** closed; EP-001 stays `open` with WI-0004 at `draft`
  - `tracker/board.md` — regenerated
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** WI-0003 is delivered and merged: the tool now answers the question the stakeholder
  opened with — who owes whom — with the balances beside it so the arithmetic can be checked. Three
  findings, one of them a real weakness in a criterion, now recorded on the item. EP-001 remains
  open on WI-0004, which is waiting on the bank CSV sample.
