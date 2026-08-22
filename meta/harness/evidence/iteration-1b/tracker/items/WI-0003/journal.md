# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T18:52:10Z — intake v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly; created by this execution of `intake` as a child of EP-001
- **Inputs read:**
  - the stated idea, verbatim (quoted in full in EP-001's entry for this execution)
  - `tracker/items/` — empty, so this item took the next free `WI-` number
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/dor-dod.md`
- **Decisions:** see EP-001's entry for this execution for how the work was split and why this
  item is one of the parts. `depends-on: WI-0002` is recorded because this item is a pure function of the recorded expenses and has nothing to compute without them.
- **Questions raised:** `Q-001` (blocking, to human) — netted pairwise debts, or the minimised set of transfers? The two print different things, so AC1 and AC4 cannot be settled without it. It has not been answered.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0003 ... --status draft` -> exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to awaiting-answer --resume-to draft ...` -> exit 0
- **Gates:** the four gates of `intake` are execution-wide and are recorded once, with their
  evidence, in EP-001's entry for this execution: `workspace-valid` **pass**,
  `epic-has-success-measures` **pass**, `items-are-separable` **pass** (this item's place in the
  order and its `depends-on` are stated there), `no-solution-in-the-problem` **pass**.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/journal.md`, `tracker/items/WI-0003/history.md` (new)
  - `tracker/items/WI-0003/questions/Q-001.md` (new, open)
- **Status:** `—` -> `draft` -> `awaiting-answer` (resume-to `draft`)
- **Result:** WI-0003 exists but is suspended behind one blocking question addressed to the human. It also waits on WI-0002 through `depends-on`.

## 2026-08-21T19:00:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer`, with `Q-001` open, addressed to `human`, and a `## Answer`
  written into it by the human since the previous turn. Last of four executions in this batch.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` — the question, its three options and the human's
    answer
  - `tracker/items/WI-0003/item.md`, `history.md` (the suspending row records `resume-to: draft`),
    `journal.md` (intake's entry)
  - `tracker/items/WI-0004/item.md` — AC4 and AC5 there are statements about this item's output
  - `tracker/items/EP-001/item.md` and its answered `Q-001`
  - `docs/product/vision.md` (v2, as read), `docs/product/prd.md` (did not exist)
  - `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1), `ADR-0003` (v1) — all written earlier
    in this batch; ADR-0003 is what makes AC4 exact rather than approximate
  - `.claude/agile-skills/spec/question.md` §4, `doc-header.md` §§2–4, `work-item.md` §2
- **Decisions:**
  - **Recorded the human as the decider on `ADR-0004`.** The choice is between two intentions, not
    two techniques, and the question said in as many words that there was no basis in the record to
    choose. Naming them means a later reader knows that superseding it needs their authorisation
    rather than an architect's opinion.
  - **Refused to write "the fewest possible payments" into an acceptance criterion.** Finding the
    provably smallest set means finding subsets of net positions that cancel exactly — the partition
    problem, NP-hard. A criterion asserting minimality would either be unverifiable or would be
    quietly reinterpreted by whoever implemented it, which is the failure mode where a criterion
    stops meaning anything. AC5 asserts what greedy settlement actually guarantees — at most one
    fewer payments than there are people with a non-zero position — and the ADR states plainly that
    this is what "fewest" was traded for. It is the common-case minimum and it is exactly the thing
    the human was complaining about.
  - **Added AC6 for determinism.** No criterion about printed output is decidable if the output can
    legitimately differ between runs, and a greedy settlement has ties to break whenever two people
    hold the same net position. Breaking them by name makes the whole output a function of the
    recorded data. This is a criterion nobody asked for; it is here because without it AC1, AC4 and
    AC5 cannot be checked by someone with a terminal and no context.
  - **Wrote the strangers-paying-strangers consequence into the item, not only the ADR.** `verify`
    reads `item.md`; a plausible-looking defect ("Carol owes Dave, but they never shared anything")
    would otherwise be filed as a bug against behaviour the human explicitly chose.
  - **Left AC2 and AC3 as two criteria rather than merging them.** They are different situations —
    nothing recorded, and recorded things that happen to balance — that must produce the same
    output, and a single criterion would let an implementation satisfy one and fail the other.
  - **Wrote `docs/product/prd.md` now, as the last execution in the batch.** Each of the five
    answers alone changes one item; together they change what the product is, and the epic and four
    items are the wrong altitude to read that from. It was deferred until now, as EP-001's journal
    entry recorded, because a PRD written between the answers would have described a product half
    of whose behaviour was undecided.
  - **Replaced vision.md's open-questions section rather than deleting it.** The document said the
    section would be removed once the questions were answered. Removing it outright would lose the
    fact that these five things were asked at all and who settled each one, so it became a summary
    of what was asked and what was decided, with the traces.
- **Questions raised:** none. No question in this batch was re-addressed to the human, and every one
  of the five is now `answered` with a non-empty `## Consequences`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to draft --actor answer-questions
    --reason "..."` -> recorded under Gates
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
- **Gates:**
  - `answer-is-propagated` (hard) -> **pass** — every path in `Q-001`'s `## Consequences` was
    reopened after writing. `ADR-0004` exists at v1 with three options and a reversibility
    statement. `WI-0003/item.md` AC1 now describes a set of settling payments and names the
    shared-nothing consequence, AC5 and AC6 exist, and `## Notes` points `verify` at the ADR.
    `docs/product/prd.md` exists at v1 and its "What it derives" section is this decision.
    `docs/product/vision.md` is at v3 with the open-questions section replaced.
  - `answered-from-the-record` (hard) -> **pass** — the choice is the human's own words, quoted in
    the question file and in `ADR-0004`. The two elaborations on top of it — what "fewest" can
    honestly promise, and determinism — are derivations, are labelled as such in the ADR, and are
    recorded there rather than asserted in the answer alone.
  - `escalation-is-justified` (hard) -> **not applicable, nothing escalated** — no question in this
    batch was re-addressed to the human.
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0 over 5 items and 6
    documents, one pre-existing warning about the null test command, which `plan` owns.
  - `item-resumed-correctly` (hard) -> **pass** — the suspending row of 2026-08-21T18:46:03Z
    records `resume-to: draft`; this execution transitioned the item to `draft`. Read from the row.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — answered; `answered-by: human`
  - `docs/architecture/adr/ADR-0004-minimum-transfers.md` — new, v1
  - `tracker/items/WI-0003/item.md` — AC1 and AC3 amended, AC5 and AC6 added, `## Notes` rewritten
  - `docs/product/prd.md` — new, v1
  - `docs/product/vision.md` — v3
- **Status:** `awaiting-answer` -> `draft`
- **Result:** All five questions `intake` filed are answered and propagated. Four ADRs and a PRD
  record what was decided; WI-0001 to WI-0004 are at `draft` with no open question, and `refine` can
  take them on. Nothing has been designed and no code exists.

## 2026-08-21T20:40:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` once WI-0002 reached `done`. A fresh
  refinement, not a send-back: the history's last row is `awaiting-answer → draft` by
  `answer-questions`, and this item has never been past `draft`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md` (two entries), `questions/Q-001.md`
    with the human's answer and its consequences
  - `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0009`
  - `docs/product/prd.md` (v2), `docs/product/vision.md` (v3),
    `docs/architecture/overview.md` (v2)
  - `tracker/items/WI-0002/item.md` and `artifacts/review.md` — for the criteria style that
    worked and for the gap its review handed to WI-0004
  - `tracker/items/WI-0004/item.md` — to confirm this item stops where that one starts
- **Decisions:**
  - **Pinned the transfer line as `<debtor> pays <creditor> <amount>`** and the settled message as
    `Everybody is settled up.` Rejected an arrow form and a table: the sentence is what somebody
    reads aloud at the end of a meal, which is the moment this command exists for.
  - **One settled message for three different situations** — nothing recorded, people but no
    expenses, and expenses that balance. A user cannot act differently on the three, and
    distinguishing them would invite a criterion about which is which. AC1, AC2 and AC3 are
    therefore the same assertion from three starting states.
  - **Ties broken by identity key, not by raw spelling.** `ADR-0004` property 3 says ties go "by
    the person's name" without saying which form. Comparing spellings would make the printed order
    depend on who typed a capital letter — the exact failure `ADR-0005` rules out for identity, so
    reusing the identity key is the consistent reading rather than a new rule.
  - **Pinned the greedy procedure in the criteria, and recorded that as a cost.** This is the
    largest decision here. `ADR-0004` promises three *properties* — exact settlement, at most
    `n - 1` transfers, determinism — not a particular output. But a criterion cannot name an
    expected output without fixing which valid settlement is produced, and the alternative —
    property-only criteria — would force `verify` to write its own settlement checker and would
    let two disagreeing implementations both pass. So the criteria pin the procedure `ADR-0004`
    itself names when justifying its bound. The price is written into the Q&A in as many words:
    if `plan` finds a better settlement algorithm, it must come back to these criteria, not just
    change the code.
  - **Turned each of ADR-0004's three promises into a checkable instance** rather than leaving
    them as prose: AC7 does the arithmetic for AC5's record by hand, AC8 counts transfers against
    non-zero positions for three different records, and AC9 requires byte-identical output across
    two runs in one process and a third in another.
  - **Added AC10 — the command never modifies the record.** Nothing in the record says so; it
    follows from `ADR-0003` point 6 and it is the kind of property that is free to assert now and
    awkward to notice later, when a caching change quietly makes a read command a writer.
  - **Added AC12 — a person at zero is not named at all.** AC6's example produces exactly that
    situation for Bob, and without the criterion an implementation that printed `Bob pays Bob
    0.00` would pass everything else.
  - **Excluded the pairwise breakdown loudly.** It is what "who owes whom" means in most other
    tools, so it is the thing a reader will assume is here; the human chose against it knowingly,
    and `ADR-0004` records what to do if that turns out to bite — a flag, as a new item.
  - **Checked every worked example by hand before writing it**, because the criteria now assert
    exact output: AC4 (30 split three ways → two transfers of 10.00, Bob first on the tie), AC5
    (10 split three ways → 3.33 twice against a net of 6.66), AC6 (two expenses leaving Bob at
    zero and Carol paying Alice 15.00, two people who never shared anything), AC3 (two expenses
    that cancel). An example that did not add up would have been worse than no example.
  - **Filed nothing to the human.** Their one question here is answered; what remained was format
    and tie-breaking, which they have twice declined to be asked about. All four such choices are
    `[assumed]` in the Q&A and repeated in `## Notes` as unconfirmed.
- **Questions raised:** none new. One (`Q-001`) was raised by `intake` and is answered; the
  exchange is at `artifacts/refinement-qa.md`, with five further answers recorded `[assumed]` and
  none left `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to ready --actor refine` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion:
    - **R1** frontmatter complete [auto] → **pass**: validator clean; `depends-on: WI-0002`, now
      `done`.
    - **R2** story names role, capability, outcome [skill] → **pass**: "As a member of the group
      settling up … so that we can square up without anyone re-deriving the arithmetic and
      disagreeing about it."
    - **R3** labelled checkbox criteria [auto] → **pass**: AC1–AC12.
    - **R4** every criterion decidable by observation [skill] → **fail on entry** — the six
      criteria named properties (`prints a set of payments`, `at most one fewer than…`) with no
      command, no line format and no expected output, and AC6's "the order follows their names"
      did not say which form of the name. Rewrote all six against the pinned format and procedure
      and added six more → **pass**.
    - **R5** out-of-scope names something a reader would assume included [skill] → **fail on
      entry** (three entries, all things nobody would expect here) → **pass**: five entries led by
      the pairwise breakdown.
    - **R6** every open question non-blocking [auto] → **pass**: `Q-001` is `answered`.
    - **R7** independently deliverable [auto] → **pass**: `depends-on: WI-0002`, `done` and
      merged.
    - **R8** Q&A recorded verbatim [auto] → **fail on entry** (no such file) → **pass**:
      `artifacts/refinement-qa.md`, with the human's answer quoted exactly.
    - **R9** one coherent change [skill] → **pass**: derive net positions, produce transfers,
      print them. No half of it is separately useful.
    - **R10** every combination stated, excluded, or unconstrained [skill] → **fail on entry** —
      nothing said what happens with people but no expenses, with a person at zero, or with an
      argument → **pass**: AC1 to AC12 cover every case the subcommand introduces, and `## Notes`
      names three things left open with `refine` recorded as who left them.
  - `criteria-are-decidable` (hard) → **pass**. Nine of the twelve are settled by running one
    command and comparing stdout against a string given in the criterion. AC7 is settled by
    arithmetic the criterion performs in full. AC8 is settled by counting lines against a number
    the criterion states for each of three records. AC10 is settled by comparing the record file's
    bytes before and after.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` reproduces the filed
    question with the reason it was asked and the human's answer word for word, including that the
    question offered no recommendation. The five answers decided here are tagged `[assumed]` and
    stated to be unconfirmed, and Q5 records what pinning the procedure costs rather than
    presenting it as free.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0003/item.md` — criteria rewritten and extended from six to twelve; the
    output format, the net-position definition and the settlement procedure stated at the head of
    the list; `## Out of scope` widened from three entries to five; `## Notes` restructured
- **Status:** `draft` → `ready`
- **Result:** WI-0003 meets the Definition of Ready on all ten criteria, with no override. The
  three properties `ADR-0004` promises are each a checkable instance, four worked examples are
  computed by hand in the criteria themselves, and the one thing `plan` should read first is Q5 in
  the Q&A: the criteria fix which valid settlement is printed, so a different algorithm is a
  criteria change and not just a code change.

## 2026-08-21T20:48:00Z — plan v0.1.1 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next`. Not a re-plan: this item has never been past
  `ready` and its history carries no send-back.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC12, the pinned output format and procedure),
    `history.md`, and `artifacts/refinement-qa.md` — **Q5 first**, as the dispatch note said, since
    it records that the criteria fix which settlement is printed and what that costs
  - `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0009`, `ADR-0010`
  - `docs/architecture/overview.md` (v2), `docs/product/prd.md` (v2)
  - **the code**: `expenses/group.py` (`shares_of`, `expenses`, `identity_key`, `find_person`),
    `expenses/cli.py` (the dispatch table and the two listing handlers),
    `expenses/money.py`, `tests/support.py` (`ExpenseTestCase`)
  - `tracker/items/WI-0002/artifacts/review.md` — for the gaps it handed forward, none of which
    lands on this item; the one that does is WI-0004's
- **Decisions:**
  - **Two functions, not one (route: decided, structure).** `net_positions` is arithmetic over the
    recorded expenses; `settle` is a scheduling loop over the result. Separating them means AC7 —
    paying the transfers zeroes everybody — can be asserted as a property linking the two halves
    rather than as a hand-checked case, and it keeps the tie-break rule in one place.
  - **`net_positions` reuses `shares_of` rather than recomputing the split.** That keeps
    `ADR-0003`'s rounding rule in exactly one place in the codebase, which is the property that
    makes the human's "we'll decide later" still true: change the rule, and both the listing and
    the settlement change together.
  - **`net_positions` returns everybody, including people at zero (route: reversible
    assumption).** Filtering inside would hide the zero case from every test that does not reach
    for internals, and AC12 is precisely about the zero case. Reversal is one `filter` moved
    between two functions in the same file.
  - **`settle` recomputes the extremes each iteration rather than sorting once (route: reversible
    assumption).** With a friend group's handful of people the cost is irrelevant, and recomputing
    is the shape in which "ties by identity key" is visibly applied at *every* step rather than
    once at the start.
  - **The settlement lives in `group.py` (route: documented).** `overview.md` has said so since
    v1; `group.py` reaches ~230 lines, which is still one screen of concepts.
  - **No new ADR, deliberately.** The one consequential decision — pinning which valid settlement
    is printed — was made by `refine` in the criteria, with its cost recorded in
    `refinement-qa.md` Q5. An ADR restating it would put the same decision in two documents with
    no way to tell which governs. Instead the **overview's decisions table gains a row** pointing
    at WI-0003's criteria, and spelling out the consequence: changing the settlement algorithm is
    a criteria change, not just a code change. That is where a future `plan` execution asking "may
    I improve this?" will actually look.
  - **Named the runtime invariant nobody checks.** The net positions sum to zero for any record
    the tool wrote; for a hand-edited one they might not, and `settle` would then emit a transfer
    set that settles nobody, silently. `ADR-0007`'s shape check cannot catch it — the file would
    be structurally valid. No criterion covers it, so `## Risks` says explicitly that `implement`
    should **not** add a guard on its own initiative and that wanting one is a question for the
    architect. Left unfixed rather than quietly widened.
  - **Wrote a risk about a test that would pass by accident.** Python's sort is stable, so an
    implementation that never compares names still prints `Bob` before `Carol` when they were
    added in that order — AC4 would pass with no tie-break at all. The plan tells `implement` to
    add a test that adds `Carol` first and still expects `Bob pays Alice` first. This is the same
    class of near-miss `refine` caught in its own AC7 example on WI-0002, and it is cheaper to
    name here than to find in verification.
  - **Named the limit of AC10.** Comparing the record file's bytes before and after catches a
    rewrite only if the serialisation differs; a byte-identical rewrite would pass. Nothing can
    catch that from outside, so the mitigation is structural — step 3 says the handler never calls
    `save`, and that is eleven lines a reviewer can read.
  - **Did not design past the item.** No payments, no pairwise view, no caching of positions, no
    guard for hand-edited records. Every step maps to at least one criterion.
  - **Asked the human nothing.** Their one question here is answered and recorded as `ADR-0004`;
    everything this execution decided is one file to reverse.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0003 --to planned --actor plan` → exit 0
  - no test run: this execution wrote no code.
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table in `plan.md` has one row
    per criterion, AC1 to AC12, each naming the step and the specific assertion, down to the
    expected string. AC7 and AC8 are mapped as properties over **three** records rather than one,
    because a single-creditor case exercises neither the multi-creditor branch nor a split
    payment.
  - `project-commands-resolved` (hard) → **pass** — unchanged from `ADR-0008`; both commands were
    executed against real failures when they were chosen, and `implement` runs them on the branch.
    `commands.build` stays null; there is still nothing to build.
  - `decisions-recorded` (hard) → **pass** — six decisions cited to existing records (`ADR-0003`,
    `ADR-0004`, `ADR-0005`, `ADR-0006`, and WI-0003's own criteria for the settlement), one
    document change (`overview.md` v3, which is where the "no new ADR" choice is itself recorded),
    and three entries under `## Assumptions`, each with its reversal cost.
  - `plan-is-executable-without-you` (advisory) → **pass, with one soft spot.** Every step names
    its files and the interface it must expose. Read cold, the place a developer still has to
    think is the loop in step 2: it says what is chosen and what is emitted, but not how to hold
    the positions while they change. That is deliberate — sequencing it would be writing the
    function — and the two risks that bite there are named.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new) — 6 steps, a 12-row mapping table, 3
    assumptions with reversal costs, 4 risks, and what is out of scope
  - `docs/architecture/overview.md` — v2 → v3: `group.py` now owns net positions and the
    settlement, and the decisions table records where the normative procedure lives and why it is
    not an ADR
  - no new ADR, for the reason recorded above
- **Status:** `ready` → `planned`
- **Result:** WI-0003 has a plan whose every step maps to a criterion and which adds no module and
  no stored data. The three things most likely to go wrong are named: a tie-break that passes by
  accident on a stable sort, AC7 and AC8 tested on too few records, and a hand-edited record whose
  positions do not sum to zero — which this item deliberately does not guard against.

## 2026-08-21T20:58:00Z — implement v0.1.0 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next`. Fresh start: `git branch --list 'wi/*'`
  showed `wi/WI-0001` and `wi/WI-0002` only, and the last history row was `ready → planned`.
  Nothing to reconcile with.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC12, the pinned line format, net-position definition and
    settlement procedure), `artifacts/plan.md`, `artifacts/refinement-qa.md` — Q5 first, as both
    the plan and the dispatch note said — and `history.md`
  - `questions/Q-001.md`, answered long before `plan` ran; nothing moved since the last journal
    entry
  - `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0009`, `docs/architecture/overview.md`
    (v3)
  - the existing source: `expenses/group.py` (`shares_of`, `expenses`, `identity_key`),
    `expenses/cli.py`, `expenses/money.py`, `tests/support.py`
- **Decisions:**
  - **`net_positions` reuses `shares_of` rather than re-deriving the split**, as the plan says.
    Worth restating because it is the property that keeps the human's deferred rounding decision
    cheap: there is one implementation of `ADR-0003` point 3 in this codebase, and both the
    listing and the settlement read it.
  - **Wrote the creditor selection as `min` over the negated amount** instead of `max` with a
    negated-name key. My first draft used `max` and a tuple of negated character codes to make the
    identity key sort ascending under a descending comparison; it worked and was unreadable.
    `min(owing, key=lambda p: (-owing[p], identity_key(p)))` says the same thing.
  - **Added a loop-termination guard the plan did not name, and checked it against the line the
    plan drew.** `plan.md` § *Risks* forbids adding a guard that *reports or refuses* a
    hand-edited record whose positions do not sum to zero. What I added is different: the loop
    stops when the extreme debtor is not in debt or the extreme creditor is not owed. Without it
    `while owing` spins forever on that input; with it the command returns a short, wrong
    settlement, which is the behaviour the plan's risk describes. It emits no message and changes
    no valid output. Declared in the implementation report as the place I came closest to the
    line, so `verify` can judge it rather than discover it.
  - **`net_positions` tolerates an expense naming somebody not in `people`** — `position.get(...)`
    rather than a bare index. Only reachable by hand-editing, and the alternative is a `KeyError`
    traceback, which `ADR-0001` point 3 rules out.
  - **Wrote two tie-break tests rather than one.** `plan.md` § *Risks* pointed out that Python's
    stable sort would make AC4 pass with no tie-break at all when Bob was added first, so one test
    adds `Carol` **before** Bob and still expects Bob first. The second uses `alice`, `bob` and
    `CAROL`, so only a *case-folded* key produces the pinned order — that one is what catches an
    implementation comparing raw spellings.
  - **Found a real hole in my own tests, by mutation, and closed it.** Making `settle` pay the
    debtor's whole debt to one creditor — a genuine defect that overpays a creditor — passed the
    entire suite, because every record I had written had a single creditor, so
    `min(-debt, credit)` and `-debt` were always the same number. This is precisely what
    `plan.md` § *Risks* warned about, and I wrote the tests without covering it anyway. Added
    `test_one_debtor_owing_two_creditors_splits_the_payment` and two more records to the property
    tests; the mutation now fails. Recorded in the report as a hole that existed rather than as
    thirteen mutations caught.
  - **Left the second surviving mutation alone, with an explanation.** Keeping zero-position
    people in `settle`'s working set changes no output — the extremes are unaffected by zeros and
    the guard fires when only zeros remain — so it is behaviour-preserving, not a gap. The filter
    stays for clarity.
  - **Escalated nothing and filed no bug.** Every decision above is one function to reverse, none
    contradicts an ADR, and the one place the plan drew a line I stayed on the near side of it and
    said so.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0003` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 96 tests ... OK` (final run, on
    the branch head). Intermediate: 15 tests after step 4, 95 after the subprocess test, 96 after
    the multi-creditor fix
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - the four worked examples computed against `group.settle` in a throwaway interpreter **before**
    any test was written, including the tie case with `Carol` added first
  - `python3 /tmp/mut3.py` — thirteen mutation runs, each reverted, then two re-runs after the fix
- **Gates:** all six, on the branch head after the last code change.
  - `tests-pass` (hard) → **pass** — 96 tests, exit 0.
  - `lint-clean` (hard) → **pass** — `compileall`, exit 0, with the standing `ADR-0008` caveat.
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `every-criterion-has-a-test` (hard) → **pass** — a test function per criterion, and thirteen
    mutations as the evidence they bite. The honest part of this gate is that it did **not** pass
    on the first attempt: one mutation survived because AC7 and AC8 were tested on too narrow a
    set of records, and the gate is claimed only after that was fixed.
  - `commits-reference-the-item` (hard) → **pass** — exit 0.
  - `no-unplanned-scope` (advisory) → **pass, with three declared deviations** — every hunk traces
    to a plan step and a criterion. Nothing anticipates WI-0004: `net_positions` reads expenses
    only.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - branch `wi/WI-0003`, commits `main..wi/WI-0003` — the code and tests, plus the commit carrying
    this entry and the report
  - `expenses/group.py` (`net_positions`, `settle`), `expenses/cli.py` (`_who_owes_whom`, one more
    entry in `COMMANDS`)
  - `tests/test_who_owes_whom.py` (new, 16 tests), `tests/test_persistence.py` (extended)
  - `tracker/items/WI-0003/item.md` — `branch: wi/WI-0003` set
- **Status:** `in-progress` → `verifying`
- **Result:** `who-owes-whom` prints the settling transfers, with 96 tests over twelve criteria and
  thirteen mutations behind them. The thing `verify` should press hardest is the multi-creditor
  branch: it is the one a mutation escaped through, and the test that now covers it was written
  after the fact.

## 2026-08-21T21:06:00Z — verify v0.1.0 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the twelve criteria, **read first**, before the
    implementation report
  - `history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/refinement-qa.md`
    (Q5, which records that the criteria pin the procedure)
  - `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `docs/architecture/overview.md`
    (v3)
  - the branch `wi/WI-0003` at commit **f6b37ed89b5a6274f41213b19a959ddc6f98e88a**, and the source
    of `group.net_positions`, `group.settle` and `cli._who_owes_whom`
- **Decisions:**
  - **Checked the three properties beyond the criteria's own examples.** The criteria name four
    worked examples; a settlement algorithm can satisfy four examples and be wrong. So AC7, AC8,
    AC9 and AC12 were also checked over seven hand-built records covering shapes no criterion
    reaches — one debtor with two creditors, two debtors with two creditors, five people across
    three expenses, a payer who shares nothing — and then over **400 randomly generated records**
    with a fixed seed, mixing stated and unstated shares. Zero violations. That is the kind of
    evidence the criteria cannot supply and the reason not to stop at them.
  - **Probed the tie-break three ways**, because it is the only thing distinguishing two valid
    outputs in AC4 and the easiest thing in this item to satisfy by accident: `Carol` added before
    `Bob` (proves it is not insertion order), mixed case (proves the key is folded), and two
    creditors owed the same (proves the rule applies on the creditor side, which no criterion
    example exercises).
  - **Reported three surviving mutations rather than the ten caught.** One is
    behaviour-preserving; two are real gaps in the tests — `net_positions`' documented ordering is
    unasserted, and AC10's fixture holds a single expense, so a rewrite that merely reorders would
    pass it. I confirmed the second mechanically: the same mutation applied to a two-expense
    record does change the file's bytes.
  - **Neither gap is a send-back.** The classification test is whether a criterion of this item
    says the behaviour should be different. AC10 says the record must not be modified, and it is
    not — I read the eleven-line handler and it calls no `save`. What is weak is the *test*, and
    sending the item back to strengthen a test that already passes against correct code would be
    verification rewriting the target rather than checking it. Both are recorded as findings for
    `review-close`, and finding 2 is the one WI-0004 should care about, since it extends
    `net_positions`.
  - **Recorded the hand-edited-record behaviour with its actual output.** `plan.md` predicted "a
    short, wrong settlement"; what actually happens is `Everybody is settled up.` while somebody
    is a pound down. Deliberately unguarded, `implement` correctly did not guard it, and no
    criterion covers it — but the record should carry what it really does, not the milder
    prediction.
  - **Noted that this loop fails by hanging.** Rounding transfers to 10p made the suite never
    finish rather than produce a wrong answer. That is a caught mutation, and it is worth knowing
    the failure mode for anyone who changes the loop later.
  - **Filed no bug and no question.** No criterion was ambiguous; the exact strings `refine`
    pinned made every verdict a comparison.
- **Questions raised:** none.
- **Commands:**
  - `git rev-parse HEAD` → `f6b37ed89b5a6274f41213b19a959ddc6f98e88a`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 96 tests ... OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - ~25 `python3 -m expenses …` invocations covering AC1 to AC12, quoted in `verify-report.md`
  - a seven-record property script (AC7, AC8, AC12, and the zero-sum invariant), printing the
    transfers for each
  - a 400-record randomised property script, fixed seed `20260821`, checking AC7, AC8, AC9 and
    AC12 plus that no transfer is ever zero or negative → `violations: 0`
  - three tie-break probes and four boundary probes, including a corrupt record and a hand-edited
    non-zero-sum one
  - thirteen mutation runs, each reverted, plus one targeted re-run to confirm why the purity
    mutation survived
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here on the branch head, 96 tests, exit 0.
  - `lint-clean` (hard) → **pass** — exit 0, with the standing `ADR-0008` caveat, restated under
    *Not verified*.
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `every-criterion-independently-checked` (hard) → **pass** — twelve rows of commands and
    captured output, none citing the implementation report, plus 407 records' worth of property
    evidence for the four criteria that are properties rather than single observations.
  - `negative-cases-exercised` (hard) → **pass** — AC11 triggered; four boundary probes; the
    hand-edited record that no criterion covers exercised deliberately to see what it does.
  - `tests-would-fail-without-the-change` (advisory) → **pass, with three survivors** — ten of
    thirteen caught; one behaviour-preserving and two real coverage gaps, each analysed rather
    than excused.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` (new), carrying
    `Verified-commit: f6b37ed89b5a6274f41213b19a959ddc6f98e88a`
  - `tracker/items/WI-0003/item.md` — AC1 to AC12 ticked, each after its row in the report existed
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0003 does what its twelve criteria say, checked by command and by property over
  407 records. Three findings for `review-close`: a hand-edited record can make the tool announce
  everybody is settled when somebody is not, and two places where the tests are weaker than the
  code — the ordering contract of `net_positions`, and AC10's single-expense fixture.

## 2026-08-21T21:16:00Z — review-close v0.1.0 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next`.
- **Inputs read:**
  - the diff `main..wi/WI-0003` for `expenses/`, hunk by hunk, and the new test module
  - `item.md`, `history.md` (eight rows), `journal.md` **in full** (six entries), `plan.md`,
    `impl-report.md`, `verify-report.md`, `refinement-qa.md`, `questions/Q-001.md`
  - `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `overview.md` (v3), `prd.md` (v2)
  - `tracker/items/WI-0002/artifacts/review.md`, to check that the gaps it handed forward are
    still owned by WI-0004 and were not silently absorbed here
- **Decisions:**
  - **Re-derived `ADR-0004`'s `n - 1` argument against the actual loop** rather than accepting the
    empirical evidence alone. `amount = min(-debt, credit)` guarantees one of the two positions
    reaches zero, and both are deleted when they do, so each iteration removes at least one person
    from the working set. That is D12 done as a read of the code against the document, which is
    what the criterion asks for.
  - **Finding 1, a clarification rather than a defect.** `ADR-0004` says ties go "by the person's
    name"; the code compares identity keys. `refine` recorded that choice in `refinement-qa.md`
    Q4 with its reasoning. The ADR is less specific than the code, not in conflict with it, and
    recording that stops a future reader concluding they have found a bug.
  - **Finding 2, accepted with its real output.** A hand-edited record whose positions do not sum
    to zero makes the tool print `Everybody is settled up.` while somebody is out of pocket. The
    plan predicted something milder; the record should carry what actually happens. Accepted
    because no criterion covers it, the tool cannot produce such a record, and the plan explicitly
    forbade guarding it here — which `implement` respected.
  - **Finding 3 — the one I came closest to rejecting.** Two test gaps: `net_positions`' ordering
    contract is unasserted, and AC10's fixture holds one expense so a reordering rewrite is
    invisible to it. A test that cannot fail is a maintenance liability, which is a legitimate
    review concern. Against rejecting: both assertions are correct as far as they go, the code is
    right, the weakness is in a fixture rather than in the item's contract, and a rejection costs
    a full round trip to strengthen coverage of behaviour no criterion requires. Accepted, and
    both are named for **WI-0004** — which extends `net_positions` and adds a third
    record-writing command, so both gaps land in its refinement rather than being remembered.
  - **Finding 4, recorded because the failure mode is unusual.** Rounding the transfer amount
    makes the settlement loop hang rather than return a wrong answer. Worth one line for whoever
    changes that expression next.
  - **Judged the loop-termination guard the right call.** `plan.md` forbade a guard that *reports
    or refuses* a non-zero-sum record; what `implement` added neither reports nor refuses — it
    stops the loop. Declared in the implementation report at exactly the right level of detail,
    which is what made it reviewable rather than something I had to find.
  - **Trial-merged into a `--detach`ed worktree** and confirmed `main` was still at `ea5b447`
    afterwards. WI-0001's review moved the trunk by trial-merging a worktree checked out on the
    branch itself; that correction is in WI-0001's journal and this is the second execution to
    follow it.
  - **Left EP-001 open.** WI-0004 is still at `draft`, so DE1 fails; the epic Definition of Done
    was not applied. Recorded on the epic's journal.
  - **Filed no bug and no question.** Nothing contradicts an ADR; every finding is behaviour no
    criterion covers or a fixture weakness, and none belongs to another item.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → exit 0
  - `git diff --name-only f6b37ed..wi/WI-0003 -- expenses tests` → empty
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, three
    commits, run **before** the merge
  - `git worktree add --detach /tmp/trial3 main` → `git merge --no-edit wi/WI-0003` → clean
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0, 96 tests;
    `python3 -m compileall -q expenses tests` → exit 0
  - `git worktree remove --force /tmp/trial3`; `git log --oneline -1 main` → `ea5b447`, unmoved
  - re-ran AC4, AC5 and AC6 by hand → the same three outputs the report records
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the close
  - `git checkout main && git merge --no-ff wi/WI-0003` → after the close
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1 to D12 each with its own result and evidence in
    `artifacts/review.md`. D6 is the interesting one: the answer is a deliberate *absence* of an
    ADR, with the reasoning recorded in the plan and a pointer added to the overview's decisions
    table. D12 involved re-deriving the `n - 1` argument against the loop.
  - `verification-postdates-the-code` (hard) → **pass** — script exit 0 plus an independent diff
    over `expenses/` and `tests/`, which is empty.
  - `commits-reference-the-item` (hard) → **pass** — exit 0, before the merge.
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 96 tests, exit 0, on the merged tree.
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings.
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and
    `git log --grep WI-0003` a reader can answer all five questions in
    `spec/journal-and-history.md` §3. This item's record is unusually good on one of them: "what
    verification found" includes a 400-record randomised property check and thirteen mutations
    with three survivors analysed, none of which a reader would have to take on trust.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` (new)
  - `tracker/items/WI-0003/item.md` — `outcome: delivered`; `## Notes` extended with five accepted
    gaps, two of them owned by WI-0004
  - `tracker/items/EP-001/journal.md` — an entry recording that the epic stays open and why
  - the merge commit of `wi/WI-0003` into `main`
- **Status:** `in-review` → `done`
- **Result:** WI-0003 is delivered and merged: `who-owes-whom` prints the settling transfers, with
  every property `ADR-0004` promises checked over 407 records. Four findings, none blocking; the
  two test-coverage gaps are handed to WI-0004, which touches the same code.
