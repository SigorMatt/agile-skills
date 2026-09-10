# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T13:17:35Z — intake v0.5.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's idea in `IDEA.md`; no status made this runnable, because the item did not exist yet
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement, verbatim)
  - `tracker/project.yaml`
  - `tracker/items/` (empty — no prior items to overlap with)
- **Decisions:**
  - This item carries income in, spending out, balances. See EP-001's entry of the same execution for how the work was split and why.
- **Questions raised:** none on this item; five were filed on EP-001 (`Q-001`…`Q-005`), of which the ones this item's criteria depend on are named in its `## Notes`
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, run to exit 0 after this execution's writes; see EP-001's entry for the run)
  - `epic-has-success-measures` → **pass** (judged on EP-001, not here; see its entry)
  - `an-open-question-was-asked` → **pass** (judged on EP-001, not here; see its entry)
  - `engagement-state-is-delimited` → **pass** (judged on `docs/product/vision.md`; see EP-001's entry)
  - `items-are-separable` → **pass** (this item is deliverable and observable on its own; its dependency, if any, is in its `depends-on`)
  - `no-solution-in-the-problem` → **pass** (the story names no technology the stakeholder did not; the provisional command name is flagged in `## Notes` rather than asserted)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (created and filled in)
  - `tracker/items/WI-0002/history.md`, `tracker/items/WI-0002/journal.md` (created)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` from the stakeholder's idea, carrying income in, spending out, balances. Its acceptance criteria are deliberately rough; `refine` is what makes them decidable.

## 2026-09-10T14:42:01Z — refine v0.6.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` — the highest-ranked runnable item
  (priority `high`, created 13:14:49, `depends-on: WI-0001` which is `done`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (one row: created by `intake`, never sent back),
    `journal.md` (intake's entry: the criteria are "deliberately rough")
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md`, `Q-004.md`, `Q-005.md` — the
    stakeholder's answers this item's criteria already rest on, read verbatim so that none is
    re-asked
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — the command name and envelope identity
  - `tracker/items/WI-0001/item.md` `## Acceptance criteria` — the house form a criterion takes
    here, and AC2 and AC4, which `WI-0002/Q-001` may change
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — checked for a standing delegation; there
    is none in this engagement
  - `tracker/items/WI-0003/item.md`, `WI-0004/item.md`, `WI-0005/item.md` — sibling scope, to keep
    `## Out of scope` true
  - `docs/product/vision.md` (v2), `docs/architecture/overview.md` (v2), `IDEA.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1 (R1–R12), `spec/question.md`
- **Decisions:**
  - **Kept AC1–AC7's numbering and their cited meanings, and appended AC8–AC12.** Five artifacts
    outside this item cite these numbers — `EP-001/Q-002` (AC1), `EP-001/Q-003` (AC6),
    `EP-001/Q-004` (AC7), `WI-0001/Q-002` (AC4), `WI-0004/item.md` (AC6). Renumbering would leave
    each citation resolving silently against whatever moved into that position, which is F-094's
    shape. Every existing criterion was sharpened in place instead.
  - **Named the sub-commands `income` and `spend` rather than asking.** The stakeholder's own
    words in `IDEA.md` are "put income into them, record spending against an envelope". Recorded
    `[assumed]` under **no** licence — there is no standing delegation in this engagement, and
    `WI-0001/Q-001`'s "not going to spend a round renaming things" is about the tool's own name —
    with where a disagreement lands. The three questions quote the words back, so they can be
    objected to before code exists.
  - **Pinned the date format as `--date YYYY-MM-DD`.** `EP-001`'s journal records that the format
    was left for `refine` to pin. Taken rather than asked because `10/9` is ambiguous between two
    readings a UK person could both mean, and a criterion on an ambiguous format is not decidable
    (R4).
  - **Extended AC4 to both recording commands, and to never creating an envelope implicitly.**
    Their recorded preference is to be told rather than to end up with two envelopes
    (`WI-0001/Q-002`); a typo silently creating `gorceries` is that failure exactly. `[assumed]`,
    with the reasoning in the Q&A.
  - **Added AC8 — a spend of exactly the balance succeeds and leaves zero.** Zero is not negative,
    and `EP-001/Q-003` refuses a balance going below zero. Written as a criterion so the boundary
    is visible rather than left to an implementer's reading.
  - **Added AC9 (zero and negative amounts refused) and AC10 and AC11 (a non-amount, and a missing
    argument).** AC9 is `[assumed]` under no licence: a negative income is a spend written
    backwards, which would give two ways to record one movement and make WI-0005's correction
    ambiguous.
  - **Added AC12, a criterion whose subject is other criteria, written to be read rather than
    run** (`spec/dor-dod.md` §6a): it names WI-0001's eleven criteria individually, says the
    assessment is a read of their text with the tests as evidence rather than as definition, and
    names the likely non-intersection — WI-0001 AC2 and AC4, if `WI-0002/Q-001` puts balances on
    `envel list`'s lines.
  - **Recorded a future date as deliberately unconstrained, in `## Notes`, by `refine`** (R10's
    third route). `EP-001/Q-004` is about days already past; refusing a future date would be a rule
    nobody asked for.
  - **Recorded that AC7's "defaults to today" half is not observable through any command this item
    delivers** — nothing here shows a transaction's date — and that `WI-0002/Q-003`'s answer
    decides whether it becomes observable. Written into `## Notes` so `verify` meets a stated gap
    rather than discovering one.
  - **Routed three decisions to `plan` instead of to the stakeholder**: the store shape and the
    migration of a `version: 1` store, the wording of every message, and which refusal wins when
    several apply. The answer to each is the same whoever the stakeholder is (`refine` step 3,
    F-023).
  - **Filed three questions and no more.** Each changes what the tool is for them and none is
    answered anywhere in the record: where a balance is seen (which un-does part of a closed
    item), what may be typed as an amount (whose second half is the "number is the truth" rule
    applied to precision), and what a successful recording prints (the only way a wrong amount or
    a wrong date is catchable at the moment it is made).
  - **Judged this one item, not two (R9).** Income in, spending out and a balance are one store
    shape, one lookup rule and one arithmetic; a balance is not observable without the recording
    commands.
- **Questions raised:** three, all blocking, all addressed to the human, filed as one ask —
  `WI-0002/Q-001` (where a balance is seen), `WI-0002/Q-002` (what an amount may look like),
  `WI-0002/Q-003` (what a successful recording prints). The agenda and the reason for each is in
  `artifacts/refinement-qa.md`, which is `status: agenda` because the conversation has not
  happened.
- **Commands:**
  - `grep -rn "WI-0002" tracker docs | grep -E "AC[0-9]"` → the five external citations of this
    item's criteria numbers, which is why AC1–AC7 were not renumbered
  - `grep -nE "^- \[ \] AC[0-9]+" tracker/items/WI-0002/item.md` → 12 criteria after the rewrite
  - `grep -n "Under delegation" tracker/items/WI-0001/artifacts/refinement-qa.md` → no delegation
    line in this engagement; the two hits are the sentences saying none could be written
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 before this move
    (`board.stale`, `question.blocking.not-suspended`), then `board-gen` → exit 0, and this
    transition is what clears the second
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` reported two errors before this move: `board.stale`, cleared by `board-gen` (exit 0), and `question.blocking.not-suspended` on this item, which is the condition this very transition exists to resolve — three blocking questions are open and the item is moving to `awaiting-answer` because of them)
  - `definition-of-ready` → **fail** (, criterion by criterion, which is why this item is not moving to `ready`: R1 **pass** — `id`, `type`, `epic`, `priority`, `created`, `updated` all present and set. R2 **pass** — the story names the role ("someone budgeting into envelopes"), the capability (record money in and out) and the outcome ("so that I can see what is left … without working it out myself"). R3 **pass** — twelve criteria, each `AC<n>` and a checkbox. R4 **fail** — nine of the twelve are decidable at a terminal as written; AC1, AC3 and AC10 each name an open question rather than a value (what a success prints, where a balance is read, what else counts as an amount). Sharpened as far as the record allows and no further. R5 **pass** — five entries, two of them new and both things a reader would assume were included: listing the individual transactions, and any notion of a second currency. R6 **fail** — three blocking questions are open, by construction. This is the criterion that makes the suspension correct rather than a failure. R7 **pass** — `depends-on: WI-0001`, which is `done`. R8 **fail** — `artifacts/refinement-qa.md` exists and declares `status: agenda`, because the questions have been filed and not answered. Writing `recorded` on it would be the lie the field exists to prevent. R9 **pass** — judged one coherent change; the reasoning is in `## Notes` and above. R10 **pass** — two commands, one option, and every pair is covered by a criterion, named as `plan`'s, or recorded as deliberately unconstrained; the paragraph is in `## Notes`. R11 **pass** — no criterion counts anything. AC12 names WI-0001's eleven criteria individually rather than saying "all of WI-0001's criteria" or "the suite is unchanged". R12 **pass** — six `[assumed]` decisions, and no `**Under delegation:**` line is written for any of them, because this engagement contains no standing delegation. Each says so and names where a disagreement lands, which is R12's other form.)
  - `criteria-are-decidable` → **fail** (nine of twelve carry the command and the verdict: AC2, AC4, AC6, AC7, AC8, AC9, AC11 are exit status and stderr on a named command line; AC5 is the third invocation showing 340; AC12 is a read of eleven named criteria with a stated procedure for a non-intersection. AC1 and AC3 depend on `WI-0002/Q-001` and `Q-003` for what is printed and where a balance is read; AC10 depends on `Q-002` for what else counts as an amount. Each of the three says which question it is waiting on, in its own text)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0, "checked 0 consumed human answer(s) and 0 delegation(s)". No stakeholder answer was consumed by this execution: the four `EP-001` answers and the two `WI-0001` answers this item rests on were consumed by `answer-questions` when they arrived, and were read here rather than re-recorded. The three questions filed today were checked against them before filing and contradict none: `Q-001` is about where a balance is shown, on which the record is silent; `Q-002` about what may be typed, on which it is silent; `Q-003` about what is printed on success, on which it is silent. `Q-002`'s recommendation is built on `EP-001/Q-003`'s reasoning rather than against it)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` carries all three questions with `[unresolved]` and the filing time, because no answer exists to record; nothing is paraphrased into agreement and no answer is attributed to the stakeholder. Six `[assumed]` decisions are recorded with their authority, each stating that nothing licensed it and where a disagreement lands)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — criteria rewritten (AC1–AC7 sharpened in place, AC8–AC12
    added), `## Out of scope` extended by two entries, `## Notes` rewritten
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (new)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** Round 1 of refinement is done and the item is not Ready. Nine of its twelve criteria
  are now decidable at a terminal; the other three name the question they are waiting on. Three
  blocking questions are open with the stakeholder — one of them un-does part of WI-0001 and is
  theirs to ask for — and six decisions were taken without them, each recorded as an assumption
  under no licence, with where a disagreement lands.

## 2026-09-10T15:03:57Z — answer-questions v0.6.2 — architect

- **Item:** WI-0002
- **Trigger:** `awaiting-answer` with three `addressed-to: human` questions whose `## Answer`
  sections had been filled in since the last execution; dispatched ahead of `next`, because an
  answered-but-unconsumed human question stops the orchestrator's loop at `next` step 5.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the three replies, with
    the options each question put and the recommendation each made.
  - `tracker/items/WI-0002/item.md` — nineteen criteria after this execution, twelve before.
  - `tracker/items/WI-0002/history.md` — the suspending row carries `resume-to: draft`.
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: agenda`; its round-1 entries and
    its six `[assumed]` decisions.
  - `tracker/items/WI-0001/item.md` — all eleven criteria, read one at a time against the answer
    to Q-001, which is how the count of affected criteria was established.
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` and `tracker/items/WI-0001/questions/`
    `Q-001.md`, `Q-002.md` — the seven prior human answers, for the cross-answer checks.
  - `docs/product/vision.md` v2; `docs/architecture/overview.md`; `docs/process/`
    `ways-of-working.md` v2.
  - `docs/architecture/adr/` — ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005. None of the five
    is contradicted by any of the three answers; ADR-0003 (one JSON store) and ADR-0004 (envelope
    identity) are the two the answers touch, and both are extended rather than overturned.
  - `.claude/agile-skills/spec/question.md` §§2–4, `spec/work-item.md` §2, `spec/doc-header.md`
    §§3, 4, 4a, `spec/dor-dod.md`.
- **Decisions:**
  - **Q-001 — route: the human already answered it.** Option A: `envel list` shows the balances,
    no second command and no flag. Propagated as `WI-0002` AC15 and AC16, with AC3, AC4, AC5, AC6,
    AC8 and AC9 rewritten to name `envel list` as the place a balance is read rather than "the
    balance the tool then shows".
  - **Q-001 — the affected criteria on `WI-0001` are six, not two.** The question told the
    stakeholder that "two of its acceptance criteria" were about a `list` line's content and named
    AC2 and AC4. Reading all eleven against the answer gives a different set. **Six** say a line's
    content is an envelope's name and nothing else — AC2 ("a line whose only content is
    `groceries`"), AC3 ("a line `a` and a line `b`"), AC5 and AC11 ("the line `groceries` once and
    only once"), AC7 ("only content is `Groceries`") and AC8 ("only content is `eating out`").
    **AC4 is not one of them**: its subject is the *order* of the lines and their byte-stability
    across two runs, and a second column changes neither. The other four that survive are AC1
    (`envel new`, not `list`) and AC6, AC9, AC10 (all about `envel list` on a store with no
    envelopes, where there is no envelope line to carry a balance). The stakeholder authorised the
    change without qualification — "Change the criteria on the earlier item, that's fine by me —
    I'm asking for it" — so the correction widens what their answer touches and does not need to
    go back to them; it is recorded here, in `WI-0001`'s `## Notes` and in `WI-0002` AC12.
  - **Q-001 — `WI-0001` was not re-opened and its criteria were not rewritten.** `work-item.md`
    §2 permits this skill to amend a criterion when it propagates an answer, and rewriting the six
    was the obvious move. It was refused: `WI-0001` is `done`, its boxes are ticked, and a tick
    means "settled by the observation the criterion names". Rewriting the text under a tick would
    convert eleven observations that were genuinely made at that item's verification into a claim
    about words nobody ever checked. Instead each of the six carries a `**[superseded: …]**`
    marker, the criteria's own words stand, and the new requirement is stated where it will
    actually be built and checked — as criteria on `WI-0002`. The alternative is recorded because
    it is defensible and a later reader should see it was weighed.
  - **Q-001 — a waiver must not drop what the criterion was protecting, so AC19 was added.**
    `WI-0002` AC12 waives the six by name. Two of them carry facts the stakeholder decided in
    `WI-0001/Q-002` and never withdrew: an envelope comes back with the capitalisation it was
    created with (`WI-0001` AC7) and a name may contain a space (AC8). Waiving the wording would
    have silently revoked those. AC19 re-checks the substance of the six against the new line
    shape, case by case, on a store that starts empty.
  - **Q-002 — route: the human already answered it, and one consequence of it was decided here.**
    Option C: a single leading `£` is accepted and ignored; more than two decimal places is
    refused rather than rounded; one currency, pounds and pence. Propagated as `WI-0002` AC17 and
    AC18, with AC10 pointing at them instead of deferring.
  - **Q-002 — `ADR-0006`, decided under route 3.3.** Their answer settles the **input** and leaves
    the **output** open, and the criteria cannot be written without it: "the balance is 340" is
    not decidable at a terminal while `340`, `340.0` and `340.00` are three answers to the same
    question. Decided: every amount and balance the tool prints carries exactly two decimal
    places. Not escalated, and the four conditions of `question.md` §4 were walked rather than
    waved at. **Intent no document records** — no: they have said the tool deals in pounds and
    pence and that it is not changing, and digit count is a consequence of that sentence.
    **Irreversible** — no: it is one formatting function and the criteria that name its output,
    and nothing is persisted in the printed form. **Contradicts an ADR or product doc** — no:
    ADR-0001 to ADR-0005 say nothing about rendering, and the vision's "One currency" is what it
    follows from. **Genuinely silent with material consequences** — silent, yes; material, no, in
    the sense §4 means: the cost of the wrong choice is two characters on a line. It binds
    WI-0003, WI-0004 and WI-0005 as well, which is why it is an ADR and not a line in one plan.
  - **Q-003 — route: the human already answered it.** Option C: one line saying what was recorded
    — envelope, amount, date filed under, and what is left. Propagated as `WI-0002` AC13 and AC14,
    with AC1 pointing at AC13 instead of deferring.
  - **Q-003 closed a gap `refine` had recorded as open.** That refinement wrote into `WI-0002`'s
    `## Notes` that AC7's "defaults to today" half was not observable through any command this
    item delivers, and that Q-003's answer might make it so. It did: the recording line carries
    the date, and AC14 is the criterion that checks it against `date +%F`. The note is replaced by
    the record that the gap is closed. Nothing was widened to achieve it — it falls out of an
    answer given for a different reason.
  - **Two things stopped being `plan`'s and it is said where `plan` will look.** The item's
    `## Notes` routed "the exact wording of every message this item adds" to `plan`. Which four
    facts a successful recording puts on the screen is now AC13's, and how many decimal places a
    printed figure carries is now `ADR-0006`'s. The sentence they sit in is still `plan`'s.
  - **`artifacts/refinement-qa.md` was left at `status: agenda` with its three `[unresolved]`
    markers.** That file says in its own words that `answer-questions` propagates into `item.md`
    and that a second round of `refine` records the answers here verbatim and sets `status:
    recorded`. The item resumes at `draft`, so `refine` is the next skill to run on it. Editing
    another skill's artifact ahead of it would have made the record say the conversation had been
    recorded when it had not.
  - **No new item was filed.** `question.md` step 3b applies when an answer implies work no item
    records. All three answers land inside `WI-0002`'s existing scope — where a balance is read,
    what an amount may look like, what a recording prints — and none of them asks for a behaviour
    that no item covers. Q-001 changes a *closed* item's requirement rather than adding work: the
    behaviour it asks for is `envel list`'s and `WI-0002` is the item that touches `envel list`.
- **Questions raised:** none. No cross-answer check returned `conflicts`, so no question was owed;
  nothing was re-addressed to the human.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0 (3 consumed human answers,
    0 delegations, 0 errors)
  - `.claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation
    --item WI-0002 --uncommitted` → exit 1 with 5 errors on first run, exit 1 with 2 after
    weakening incidental prose, exit 0 after the enumeration was written
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending
    --uncommitted` → exit 0 (2 documents in window, compared region by region against HEAD)
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1 before this transition, on the two
    change-log rows this entry is what makes true, the stale board, and `question.awaiting.none-open`
  - `grep -c '^- \[ \] AC' tracker/items/WI-0002/item.md` → 19
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in the three `## Consequences` sections was opened after writing and the change is there: `WI-0002/item.md` carries AC13–AC19 and the rewrites of AC1, AC3, AC4, AC5, AC6, AC8, AC9, AC10 and AC12; `WI-0001/item.md` carries six superseded markers and the new `## Notes` section; `docs/product/vision.md` is at v3 with both sentences changed; `ADR-0006` exists. No `## Consequences` section names zero files.)
  - `answered-from-the-record` → **pass** (each of the three answers is the stakeholder's own reply, quoted verbatim in `## Answer` and in the item's `## Notes`; the one decision the record did not settle — the printed form of a figure — is recorded as `ADR-0006` and cited from Q-002 and Q-003.)
  - `escalation-is-justified` → **skipped** (nothing was escalated: no question was re-addressed to the human, and no cross-answer check found a conflict. The one decision taken here rather than asked, `ADR-0006` rule 3, has the four conditions of `question.md` §4 walked against it under **Decisions** above.)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents` exit 0. Rule 3 of `ADR-0006` is the one quantified claim this execution wanted to keep, and its enumeration is nested under the ADR's entry in `WI-0002/Q-002`'s `## Consequences`: three print sites, a verdict for each, and a falsifier naming the refusal message as the site where a raw `340` could really have appeared, because no criterion inspects a refusal's digits.)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents` exit 0. No `## Engagement state` section was written or amended. `docs/product/vision.md`'s section is stale — it says five intake questions are open and that nothing has been designed or built — and it was already stale before this execution: none of these three answers falsified a sentence in it. It is the ending's and it is left alone.)
  - `cross-answer-consistency` → **pass** (`lint-answers` exit 0. Each of the three answers was checked against all nine recorded human answers in the workspace — the seven prior ones and, for each, the other two of this round. Every verdict is `compatible`. Two pairs needed a real look rather than an assertion: `WI-0001/Q-002`'s "don't restrict the characters", whose subject is an envelope name and not an amount, and the same answer's capitalisation and spaces guarantees, which live on two of the six criteria Q-001 supersedes and are carried forward by AC19 rather than dropped.)
  - `workspace-valid` → **fail** (before this transition: 4 errors, every one of them a state this move resolves — two `doc.changelog.no-execution` rows naming an execution this entry is, `board.stale`, and `question.awaiting.none-open` on an item whose three questions are now answered. The transition's own run is the verdict.; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel --resolving 'WI-0002:awaiting-answer->draft+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-10T14:42:01Z records `resume-to: draft`; this move is `awaiting-answer → draft`. It was read from that row and not inferred from which skill asked.)
  - `a-deferral-is-not-an-answer` → **skipped** (none of the three replies defers. Each names an option letter and gives the reason for it; none says "later" or withholds anything.)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — each `status: answered`,
    `answered-by: human`, `answered-at` stamped, with a `## Cross-answer check` over nine prior
    answers and a `## Consequences` naming the files changed. Q-002's carries the enumeration for
    `ADR-0006` rule 3.
  - `tracker/items/WI-0002/item.md` — AC13, AC14, AC15, AC16, AC17, AC18, AC19 added; AC1, AC3,
    AC4, AC5, AC6, AC8, AC9, AC10 and AC12 amended; three entries added to `## Out of scope`;
    `## Notes` rewritten where it recorded the three questions as open, and its R10 combinations
    paragraph extended to cover the dimensions the answers added.
  - `tracker/items/WI-0001/item.md` — six criteria marked `superseded`, a `## Notes` section added.
    No criterion's own text was changed and no box was un-ticked; the item stays `done`.
  - `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` — created at v1.
  - `docs/product/vision.md` — v2 → v3, with a change-log row.
  - Commit: the workspace files this execution wrote, referencing WI-0002 and WI-0001.
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's three answers to WI-0002's first refinement round are consumed and
  propagated. `envel list` gains the balances and `WI-0001`'s six criteria that said a listing line
  carries a name and nothing else are superseded rather than rewritten, with their substance
  re-checked by a new criterion; an amount is pounds and pence with a leading `£` ignored and
  over-precision refused, and `ADR-0006` settles the printed form the criteria needed; a successful
  recording prints what it recorded, which incidentally makes AC7's "defaults to today" checkable
  in this item for the first time. The item returns to `draft` for `refine` round 2, which owes the
  conversation's verbatim record and the Definition of Ready.

## 2026-09-10T15:08:12Z — refine v0.6.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** `draft`, dispatched by `next` step 4 as the runnable item with the best selection
  key (priority rank 2 against BUG-0001's 3). Round 2 of refinement: round 1 suspended the item on
  three blocking questions, and `answer-questions` returned it here with all three answered and
  propagated.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — nineteen criteria as `answer-questions` left them.
  - `tracker/items/WI-0002/history.md` — three rows. The item reached `draft` by **resumption**
    from `awaiting-answer`, not by a send-back from `verifying` or `in-review`, so this is a
    continued refinement rather than a defect repair; precondition 3 was read before anything else.
  - `tracker/items/WI-0002/journal.md` — the round-1 refinement entry and the `answer-questions`
    entry that precedes this one.
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` at `status: agenda`, and its six `[assumed]`
    entries.
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the three answers verbatim,
    with their cross-answer checks and consequences.
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md`, `tracker/items/WI-0001/questions/`
    `Q-001.md`, `Q-002.md` — the six other recorded human answers, re-read for the standing-delegation
    check rather than taken from round 1's finding.
  - `tracker/items/WI-0001/item.md` — the eleven criteria and their new `superseded` markers.
  - `tracker/items/BUG-0001/item.md` and `docs/architecture/adr/ADR-0005-text-crossing-the-process-boundary.md`
    — read because AC17 puts a non-ASCII character into an argument.
  - `docs/product/vision.md` v3, `docs/architecture/adr/ADR-0003`, `ADR-0004`, `ADR-0006`.
  - `tracker/items/WI-0003/item.md`, `WI-0004/item.md`, `WI-0005/item.md` — checked for scope this
    item might already own; none overlaps, and each states the boundary in its own `## Out of scope`.
- **Decisions:**
  - **Nothing was asked this round, and that is the decision rather than the absence of one.**
    Step 3's routing test was applied to everything still open on the item. What is open is how a
    transaction is stored, the wording of each message, which refusal wins when two apply, and the
    `£`/`BUG-0001` interaction — every one an answer that would be the same whoever the
    stakeholder was, and therefore `plan`'s. Filing a question to fill a round would have spent a
    stakeholder round trip on nothing.
  - **AC1 and AC2 were rewritten to be decidable standing alone.** Both said a command "records"
    an amount, which named no observation: a reader with a terminal could see the exit status and
    the streams and had no way to check the recording. Each now says what `envel list` writes
    afterwards, from a stated starting balance. This is R4, and it was the last thing on the item
    that would have reached `verify` as a judgement call.
  - **AC4's case-insensitive lookup was rewritten from "finds that envelope and is not refused".**
    "Is not refused" is the absence of an observation. It now states the store's starting balance,
    exit 0, empty stderr, and that the balance shown for `groceries` goes down — which is what
    distinguishes finding the envelope from silently doing nothing.
  - **AC7 gained the store precondition it was missing.** It required `envel spend groceries 10
    --date 2026-08-31` to exit 0 without saying what `groceries` held, and AC6 refuses a spend
    larger than the balance — so on a store where `groceries` held 5, AC6 and AC7 contradicted each
    other and both were decidable. The criterion now fixes the starting balance at 30, which covers
    its three invocations.
  - **AC16 is new and is recorded as an assumption taken under no licence** (`A7` in the Q&A). The
    stakeholder's answer to Q-001 says `envel list` shows the balances and says nothing about an
    envelope that has never held money — the state every envelope is in when it is created. `0.00`
    was chosen over an empty column and over omitting the envelope because it is the only reading
    under which `envel list` still answers "what are my envelopes called", which is what the
    command did before this item.
  - **`envel new` is left silent, recorded as `A8`.** Q-003's option A described the quiet tool as
    "the way `envel new` does today" and they chose C — for the two commands that question was
    about. Extending their answer to a third command would be widening it. Their answer protects
    nothing here either: `WI-0001` AC1 constrains only that command's stderr and exit status, and
    that criterion is the pipeline's rather than theirs.
  - **AC17's `£` meets BUG-0001, and it is a note rather than a criterion or a dependency.** `£` is
    non-ASCII and `BUG-0001` is open against the tool raising `UnicodeEncodeError` out of the argv
    path under a non-UTF-8 locale (`ADR-0005` measures the encodings). AC17 says nothing about the
    locale and the ordinary one is UTF-8, so it is checkable as written and this item does **not**
    gain a `depends-on` — sequencing it behind a medium-priority bug would be a scheduling decision
    taken inside a criterion. What `plan` may not do is parse the amount past whatever boundary
    `BUG-0001` establishes, and the item's `## Notes` says so where `plan` will read it.
  - **The criteria were not renumbered, and the four external citations were re-read against what
    they now point at.** `grep` over the workspace finds `WI-0002 AC1` (EP-001's journal, "no
    pool"), `AC4` (WI-0001's journal, envelope identity), `AC6` (WI-0004's `## Notes` and journal,
    the overspend counterpart) and `AC7` (EP-001's journal, the optional date). All seven criteria
    added since round 1 were **appended** as AC13–AC19, so every one of those four still resolves
    against the criterion it was written for; each was opened and read rather than assumed.
  - **No cross-answer conflict was found.** Each of the three answers already carries a
    `## Cross-answer check` against all nine recorded human answers, written by `answer-questions`
    when it consumed them; this round re-read the two pairs those checks called out as needing a
    real look — `WI-0001/Q-002`'s "don't restrict the characters" against Q-002's restriction on
    amounts, and the same answer's capitalisation and spaces guarantees against the six criteria
    Q-001 supersedes — and agrees with both verdicts. No criterion written here contradicts a prior
    answer, so no question was owed under ADR-0008.
  - **The standing-delegation check was re-run rather than inherited.** All nine human answers were
    re-read for a category answer. There is none; the nearest, `WI-0001/Q-001`, is about the tool's
    own name. Every `[assumed]` entry therefore takes R12's other form — nothing licensed it, and
    the entry names where a disagreement lands.
- **Questions raised:** none. Round 1's three (`Q-001`, `Q-002`, `Q-003`) are `answered`, recorded
  verbatim in `artifacts/refinement-qa.md`, and nothing is left `[unresolved]` in that file.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace` → exit 0 (7 items, 9 documents, 0 errors)
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0 (3 consumed human answers,
    0 delegations)
  - `grep -c '^- \[ \] AC' tracker/items/WI-0002/item.md` → 19
  - `grep -rn "WI-0002 AC" --include=*.md tracker/ docs/` → 4 external citations, in
    `tracker/items/EP-001/journal.md` (AC1, AC6, AC7), `tracker/items/WI-0004/item.md` and
    `journal.md` (AC6), `tracker/items/WI-0001/journal.md` (AC4)
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors and 0 warnings.)
  - `definition-of-ready` → **pass** (, criterion by criterion:)
  - `criteria-are-decidable` → **pass** (. The observation for each: **AC1** run `envel income groceries 400` on a store where `groceries` holds 0, then `envel list` — exit 0, empty stderr, one stdout line, and a line containing `groceries` and `400.00`. **AC2** the same shape from 400, expecting `340.00`. **AC3** three invocations, then a line containing `groceries` and `340.00`. **AC4** two refusals with `rent` on stderr and no `rent` line, plus `envel spend Groceries 10` exiting 0 and moving the balance. **AC5** a fourth invocation of `envel list` after AC3's, expecting the same line. **AC6** `envel spend groceries 500` on 340 — non-zero, `groceries` on stderr, balance still `340.00`. **AC7** three invocations on a store holding 30, one exiting 0 and two non-zero with stderr and no change. **AC8** `envel spend groceries 340` on 340 — exit 0, empty stderr, `0.00`. **AC9** four invocations, each non-zero with stderr, and an unchanged `envel list` line. **AC10** two invocations, same shape. **AC11** two invocations, same shape. **AC12** a read of eleven named criteria's text with a verdict each, six of them `waived — superseded by WI-0002/Q-001`; the procedure is `spec/dor-dod.md`'s and the criterion asks for it by name. **AC13** one invocation, exit 0, empty stderr, exactly one stdout line containing four named substrings. **AC14** one invocation beside `date +%F`, comparing the printed date. **AC15** `envel list` on a two-envelope store — exit 0, empty stderr, exactly two lines in a stated order with stated substrings, and byte-identical stdout on a second run. **AC16** `envel new petrol` then `envel list` — a line containing `petrol` and `0.00`. **AC17** five invocations, one with `£12.50` and four plain, each exiting 0 with empty stderr, and a listing line containing `12.50`. **AC18** two invocations, each non-zero with stderr, and a listing line still containing `340.00`. **AC19** four sequences on stores that start empty, each with a stated line count and stated substrings.)
  - `cross-answer-consistency` → **pass** (`lint-answers` exit 0, 3 consumed human answers and 0 delegations. No conflict was found; the two pairs that needed a real look are named under **Decisions**, and neither is a contradiction between two of the stakeholder's statements.)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` at `status: recorded` holds all three questions and all three answers quoted verbatim as `[human]`, each in a block quote and none paraphrased — including the sentence in Q-001 that authorises changing a closed item's criteria, which is the one a tidier record would have softened. Eight `[assumed]` entries, each stating that nothing licensed it and where a disagreement lands, and no `**Under delegation:**` line, because there is no standing delegation to name.)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — rewritten from `agenda` to `recorded`:
    round 1's three questions with the answers verbatim, a "Round 2 — nothing asked" section saying
    why, the standing-delegation re-check, `A1`–`A6` carried forward and `A7` and `A8` added, the
    `plan` routing including the `£`/`BUG-0001` constraint, and the DoR position.
  - `tracker/items/WI-0002/item.md` — AC1, AC2, AC4 and AC7 rewritten for decidability; the stray
    blank line between AC12 and AC13 removed and two over-long lines reflowed; the R11 note
    rewritten; a new `## Notes` paragraph on AC17's `£` and `BUG-0001`.
  - No document under `docs/` was written. `refine` does not edit architecture documents, and
    nothing this round needed one.
  - Commit: the workspace files this execution wrote.
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Nineteen criteria, every one naming a command and a verdict; the
  three questions round 1 filed are answered and recorded verbatim; eight assumptions are on the
  record, each with the criterion a disagreement would land on. Nothing was asked this round
  because nothing left open is the stakeholder's. `plan` inherits four decisions — the store shape
  and the `version: 1` migration, the wording of each message, which refusal wins when two apply,
  and the constraint that AC17's `£` shares an argument-decoding path with `BUG-0001`.

## 2026-09-10T15:16:38Z — plan v0.6.2 — architect

- **Item:** WI-0002
- **Trigger:** `ready`, dispatched by `next` step 4 as the runnable item with the best selection
  key (priority rank 2 against BUG-0001's 3). `refine` passed it to `ready` in the execution
  immediately above this one.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the nineteen criteria, which are this plan's contract, and
    the three `## Notes` sections routing work here.
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` at `status: recorded` — the three
    stakeholder answers verbatim and the eight `[assumed]` entries, which are the design's soft
    ground. `A7` (a new envelope shows `0.00`) and `A8` (`envel new` stays silent) are the two this
    plan has to honour without a criterion forcing it, and both are in `## Out of scope for this
    item` or in a step.
  - `tracker/items/WI-0002/history.md` and `journal.md` — three executions; this is a first plan,
    not a re-plan after a rejection.
  - `tracker/items/WI-0001/item.md` and `artifacts/plan.md` — the eleven criteria with their six
    `superseded` markers, and WI-0001's own assumption P1 on message wording, which this plan
    follows rather than reinventing.
  - `tracker/items/BUG-0001/item.md` and `artifacts/plan.md` — read in full, because it changes
    `envel/cli.py` and `envel/store.py` on a parallel branch. Its steps 1–4 are what `## Risks`
    row 1 is about.
  - `tracker/items/WI-0003/item.md` and `WI-0005/item.md` — read to decide whether the store keeps
    the movements. They are the two items that need them, and they are the whole argument of
    `ADR-0007` option A's risk.
  - `docs/architecture/overview.md` v2, `docs/product/vision.md` v3,
    `docs/process/ways-of-working.md` v2 — all three opened and read for the invalidation set, not
    recalled.
  - `docs/architecture/adr/` — `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`,
    `ADR-0006`, each read in full and each given a line under `## Binding ADRs`.
  - The code: `envel/cli.py` (all 83 lines), `envel/store.py` (all 92), `envel/envelopes.py` (all
    63), `bin/envel`, `tests/test_cli.py` (all 125) and `tests/test_envelopes.py`. Reading the
    tests rather than only the source is what produced step 8, which is the step that matters most.
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both set and both were run.
- **Decisions:**
  - **The store keeps the movements rather than a running balance — decided, `ADR-0007`.** This is
    the decision of the item and it is taken in the item that does not need it. WI-0002 alone is
    satisfied by one number per envelope; WI-0003 summarises a month's movements and WI-0005
    corrects one of them, and neither can be built on a balance. `ADR-0003` fixed the window: the
    format "is cheap to reverse while `version` is 1 and no real data exists", and adding movements
    once the stakeholder has months of spending in the file means a migration with no history to
    reconstruct. Option C, a cache beside the movements, was refused because two representations of
    one fact can disagree and the first time they do the person's money is wrong silently.
  - **An amount is a positive integer number of pence — decided, `ADR-0007`.** `ADR-0006` fixed
    what a printed figure looks like and left the stored one open. A JSON float is the standard way
    to lose a penny, and the stakeholder's stated reason for this whole area is that the number
    should be the truth (`EP-001/Q-003`); AC6 compares a spend against a balance, so a drifted
    balance is a wrong refusal. `decimal.Decimal` was considered and is more machinery than a
    product whose every amount is a whole number of pence by the stakeholder's own rule.
  - **Format version 2, with a version 1 document upgraded in memory — decided, `ADR-0007`.**
    `ADR-0003` put the `version` field there for exactly this and said so; this is that later item
    using it for that purpose. A store from a newer build raises `StoreError` rather than being
    read on the guess that the fields this build knows are still the fields that are there.
    `ADR-0003` is **not** superseded: its decision was one JSON document at an overridable path,
    replaced atomically, and all of that stands.
  - **`--date` is extracted by hand rather than by `argparse` — assumed, P2.** `argparse` is in the
    standard library and `ADR-0001` permits it, and it collides with two criteria that are already
    signed off: WI-0001 AC9 and AC10 compare `envel list`'s stdout byte-for-byte against a
    reference, and `WI-0002` AC9 requires `-5` to reach the amount parser rather than being read as
    an option. Reversal is one function and its two callers.
  - **`envel/movements.py` is a new module beside `envel/envelopes.py`, not an addition to it.**
    The overview's reason for the one-way dependency is that "the domain rules are the part later
    items keep adding to", and this is the first of those additions. It imports `envel.envelopes`
    for `identity` and does not import `envel.store`, so the direction the overview asserts is
    unchanged — only its enumeration of modules is, which is a row of the invalidation set.
  - **`envelopes.listing` keeps its signature and `envel/envelopes.py` does not change.** The
    obvious move was to have `listing` return entries so a caller could read a balance off them.
    That would have changed `envel/envelopes.py`, `ADR-0004`'s module, and broken
    `tests/test_envelopes.py`'s two listing cases, for no gain: the balance is looked up by
    identity in `envel/cli.py` instead. The narrower change is the one that leaves WI-0001's unit
    tests untouched.
  - **The order in which a recording command refuses — decided, `## Approach`.** Arity and options,
    then the amount, then the date, then the envelope, then the balance. The reason for this order
    rather than another is that the first three look only at what was typed, so a malformed command
    never reads the store, and the person is told about the thing on their own screen. `envel spend
    nosuch -5` therefore refuses on the amount; the item said any one refusal satisfies AC4, AC9
    and AC10, and this fixes which.
  - **Every message this item adds is written out in the plan — assumed, P1.** Not left as "the
    wording is `plan`'s", which would push the decision into `implement` where no reviewer argues
    with it. AC13's line is spelled out and checked against the criterion's four substrings by
    hand: `spend 12.50 from groceries on 2026-08-31 — 387.50 left` contains `groceries`, `12.50`,
    `2026-08-31` and `387.50`.
  - **`parse_date` validates the shape with a regular expression before calling
    `date.fromisoformat`.** This looks redundant and is not: on Python 3.11 and later
    `date.fromisoformat` also accepts `20260831` and a full timestamp, and AC7 says the date is
    given as `YYYY-MM-DD`. Without the regex the criterion would pass while the tool accepted a
    form nobody specified.
  - **Step 8 edits eight of WI-0001's test cases, and the plan says which and why.** Reading
    `tests/test_cli.py` rather than only the criteria produced this: eight cases assert `envel
    list`'s exact stdout as a literal — `"groceries\n"`, `"a\nb\n"`, `"Zebra\napple\n"` — and every
    one fails the moment a balance column exists. Six belong to criteria `WI-0002` AC12 waives.
    The seventh, `test_ac4`, belongs to a criterion that is **not** waived: AC4's subject is
    ordering and byte-stability, both of which survive, and only its literal moves. That
    distinction is written into the step because a reader who saw "six waived" would edit six.
  - **Nothing was asked of the human.** No decision here is irreversible in `question.md` §4's
    sense — the store shape is the nearest and `ADR-0003` establishes that it is cheap to reverse
    while no real data exists, which is now — and no decision depends on intent the record does not
    hold. The three answers that would have been needed were given in `WI-0002/Q-001`, `Q-002` and
    `Q-003` and are cited from the steps that rest on them.
  - **No bug was filed.** Reading `envel/cli.py` and `envel/store.py` for this plan turned up no
    delivered behaviour that is wrong; the one defect in this area is `BUG-0001`, already filed and
    already planned, and this plan does not widen to absorb it.
- **Cross-answer check:** `Checked against: EP-001/Q-002; EP-001/Q-003; EP-001/Q-004;
  WI-0001/Q-002; WI-0002/Q-001; WI-0002/Q-002; WI-0002/Q-003` — the seven recorded human answers
  this plan rests on. No answer was recorded here; each was relied on and each is cited from the
  step or the ADR clause that rests on it.
  - `EP-001/Q-002` — compatible: no pool and no split, which is why `record` names an envelope on
    every movement and there is no unassigned bucket in the version 2 document.
  - `EP-001/Q-003` — compatible, and it is the answer `ADR-0007` decision F rests on: "the number
    is the truth" is why an amount is integer pence rather than a float.
  - `EP-001/Q-004` — compatible: the optional date defaulting to today is step 1's `parse_date` and
    `today`, and it is stored per movement, which is what `ADR-0007` decision 5 makes possible.
  - `WI-0001/Q-002` — compatible: identity and the display form are `ADR-0004`'s and unchanged.
    This plan deliberately leaves `envel/envelopes.py` alone so that nothing about it moves.
  - `WI-0002/Q-001` — compatible: step 6 is that answer, and step 8 is its cost, paid where the
    stakeholder said to pay it.
  - `WI-0002/Q-002` — compatible: step 1's `parse_amount` is rule 2 of `ADR-0006`, and `ADR-0007`
    decides the stored form their answer left open.
  - `WI-0002/Q-003` — compatible: step 5's line is that answer, with the four facts they named.
  No two of these disagree, so nothing was put back to them and no ADR here reconciles two of their
  statements — which is the move `plan` step 5a forbids and the one this design came closest to,
  since `WI-0002/Q-002` (refuse over-precision) and `WI-0002/Q-001` (put a balance on every line)
  both bear on how a figure is written. They agree; `ADR-0006` had already read them together.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 24 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1 with 2 `claim.unsourced`
    errors on the first run, exit 1 with 1 after the first repair, exit 0 after the second
  - `.claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item
    WI-0002` → exit 0 (10 invalidation rows, 0 deliverable documents, 7 binding ADRs)
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0 (10 consumed human answers,
    0 delegations)
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1 before this transition, on the one
    `doc.changelog.no-execution` row this entry is what makes true; exit 0, 7 items and 10
    documents, 0 errors and 0 warnings, immediately after it
- **Gates:**
  - `workspace-valid` → **fail**, and the move is forced. The run's own output:
    `validate-workspace --resolving 'WI-0002:ready->planned+journal'` exited 1 with
    `docs/architecture/adr/ADR-0007-...:149: ERROR [doc.changelog.no-execution] the row says plan
    changed this at 2026-09-10T15:11:11Z for WI-0002, and WI-0002's journal has no execution of
    plan at all`. That is the whole of the workspace's state: one error, and it is this one.

    The four conditions of `docs/process/ways-of-working.md` are walked here rather than asserted,
    and **the third is not met**, which is said plainly rather than papered over.

    1. **Outside the rule the gate implements — yes.** `spec/journal-and-history.md` §0 is what
       `doc.changelog.no-execution` mechanises, and the fabrication it exists to catch is a
       version row naming a run that never happened. This row names a run that is happening: the
       entry that makes it true is this one, appended by step 5 of the command being refused.
       `--resolving` is told the pending move is `ready->planned+journal` and still reads the
       journal as it stands before the append.
    2. **The change that would clear it is unavailable — enumerated, skill by skill, through the
       nine in `pipeline.yaml`.** The change is "append a `plan` execution entry to
       `tracker/items/WI-0002/journal.md`". `intake` creates epics and items and does not journal
       another skill's execution. `refine` journals as `refine`, on `draft`; WI-0002 is at `ready`
       and a `refine` entry would not satisfy a row naming `plan`. `plan` is the acting skill and
       is the one that may — through `scripts/journal-entry` or through this transition, and both
       are the same append. `implement`, `verify` and `review-close` each journal as themselves
       and none is dispatchable on a `ready` item. `answer-questions` runs on `awaiting-answer` and
       WI-0002 is not there, and a row naming `plan` would not be satisfied by its entry either.
       `next` writes no journal entry at all, by its own contract. `retro` runs on an ended epic.
       So exactly one skill may make the change, it is this one, and the only route it has is the
       command that is being refused for the state the command would remove.
    3. **A question recording the diagnosis — NOT MET, deliberately.** The convention was written
       for a finding that stays false after the move and needs an owner. This one clears the
       instant the command finishes: `validate-workspace` reports 0 errors immediately afterwards,
       which is recorded under **Commands**. Filing a question from the architect to the architect
       about a state that no longer exists would be theatre, and `question.md` §4 licenses none of
       its four conditions for it. The convention should distinguish the two kinds; it cannot be
       amended from here, because `spec/doc-header.md` §5 makes `docs/process/ways-of-working.md`
       `review-close`'s and `answer-questions`' to update and `plan`'s only to create.
    4. **The verdict and the run's output are here — yes**, above, and the history reason names
       the forced gate. It names no question, because condition 3 is not met and there is none.

    **This is the third occurrence of the identical refusal in this engagement.** It forced
    `WI-0001`'s `ready → planned` and `BUG-0001`'s, and it will force every future `plan` execution
    that writes an ADR, which is most of them. The fix looks small and is not this project's to
    make: `--resolving` already downgrades other findings for the pending move and does not credit
    the journal entry that arrives with it.
  - `every-criterion-is-addressed` → **pass** (the `## Acceptance criteria mapping` table has
    nineteen rows, AC1 to AC19, contiguous, each naming the plan steps that satisfy it and a
    specific demonstration — a named test case or a by-hand run — rather than "tests". AC12, whose
    subject is other criteria, maps to the eleven-row read in `impl-report.md` and says explicitly
    that `verify` makes the assessment and `implement` supplies the evidence.)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` carries
    `test: python3 -m unittest discover -s tests -t .` and
    `lint: python3 -m compileall -q envel tests`. Both were run from the repository root by this
    execution: 24 tests OK, and compileall exit 0. Neither was invented and neither exits zero
    without checking anything.)
  - `decisions-recorded` → **pass** (the `## Decisions and ADRs` table lists twelve choices. Three
    point at `ADR-0007`, written by this execution; four point at standing ADRs this change is
    constrained by rather than deciding again; one is the refusal order, decided in `## Approach`
    because it needs no ADR and no alternative is worth a document; four point at assumptions P1 to
    P4, each stating what reversal costs — a string, a function and its two callers, a field and a
    write path, and the order of two calls.)
  - `plan-is-executable-without-you` → **pass** (advisory. The plan was re-read as if by someone
    who had not seen the item, looking for a step at which they would have to decide something the
    plan does not decide. Three places would have been that step and each was written out rather
    than left: the exact regular expressions in step 1, the exact message strings and the order of
    the five refusals in step 5, and the eight test cases named one by one in step 8 with the
    instruction not to weaken an equality into a containment. What a reader still has to supply is
    the code, which is theirs.)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents` exit 0. Ten rows, written from
    opening `docs/product/vision.md`, `docs/architecture/overview.md`, `docs/process/`
    `ways-of-working.md` and all six standing ADRs rather than from recall. Six rows are on the
    overview and are the real work of step 11; one is `vision.md`'s `## Engagement state`,
    disposed `owned-by-ending` because nobody in this pipeline may write one; and three record
    documents read and **not** falsified — `ADR-0003`, whose shape illustration is scoped "at this
    version"; `ADR-0006`, whose rule 3 this item is the first to make true and whose enumeration
    named step 5's refusal messages as a print site; and `ways-of-working.md`, which is about the
    pipeline and not the tool. `## Deliverable documents` is `none` and the reason is stated: no
    criterion of this item is about a document.)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0, 10 consumed human
    answers and 0 delegations. The seven this plan rests on are listed above with a verdict each;
    no claim in `docs/` sourced to one of their answers was rewritten by this execution.)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0. It caught three real
    unsourced absolutes in `ADR-0007` on the way — "nothing is written", "cannot be built on it",
    and an option heading — and each was repaired by adding the citation or by removing an
    absolute that was rhetoric rather than a claim, not by arguing with the gate.)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` — created: the problem, the approach, eleven steps,
    a nineteen-row criteria mapping, four assumptions, a twelve-row decision table, a ten-row
    invalidation set, `none` for deliverable documents, seven binding ADRs, `none` for scaffolding,
    five risks, and five things out of scope.
  - `docs/architecture/adr/ADR-0007-the-store-keeps-movements-in-integer-pence.md` — created at v1.
  - No other document was written. `docs/architecture/overview.md` is in the invalidation set and
    is step 11's, not this execution's: it describes the shape the system has, and the system does
    not have it yet.
  - Commit: the workspace files this execution wrote.
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. The design's one real decision is that the store keeps the
  movements rather than a running balance, taken in an item that does not need them because the two
  items that do would otherwise owe a migration of the stakeholder's real data with no history to
  reconstruct — and `ADR-0003` says the window for taking it closes as soon as that data exists.
  An amount is a positive integer number of pence, which is what makes "the number is the truth"
  arithmetic rather than a slogan. Eleven steps, nineteen criteria mapped, and one step — step 8 —
  that edits eight test cases WI-0001 wrote, which is the cost of `WI-0002/Q-001` and is where a
  reviewer should look first.

  One gate was forced: `workspace-valid`, on the third occurrence in this engagement of the same
  circularity — `plan` writing an ADR and transitioning in one execution cannot leave
  `validate-workspace` green beforehand, because `doc.changelog.no-execution` reads the item's
  journal for an execution that step 5 of the very command being run is what appends. The four
  conditions of `docs/process/ways-of-working.md` are walked under **Gates:** and the third is
  stated as not met, with why. Nothing else in the workspace was in error before the move and
  nothing is after it.

## 2026-09-10T15:19:19Z — implement v0.6.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next` as the highest-ranked runnable item (priority rank 2; BUG-0001 rank 3; WI-0003/4/5 depend on this item)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — nineteen acceptance criteria, the out-of-scope list, and the three notes routing the message wording, the store shape and the refusal order to `plan`
  - `tracker/items/WI-0002/artifacts/plan.md` — the eleven steps, the AC mapping, assumptions P1–P4, the ten-row invalidation set, `none` for deliverable documents and `none` for scaffolding, seven binding ADRs, five risks
  - `tracker/items/WI-0002/history.md` — five rows; the last is `ready → planned` by `plan`. No send-back, so this is a fresh execution rather than a defect fix
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three `answered` and propagated before `refine` round 2; read for orientation only, the criteria are authoritative
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both non-null; branch prefix `wi/`, trunk `main`
  - `envel/cli.py`, `envel/store.py`, `envel/envelopes.py`, `tests/test_cli.py` — the code the plan changes, read before touching it
  - `docs/architecture/overview.md` — the one document in the invalidation set with real repair work in it
- **Decisions:**
  - Branch from `main` at `ce87246` rather than from `wi/WI-0001`: WI-0001 is merged and `main` carries it (`bab1509`). `wi/WI-0002` therefore contains BUG-0001's fix not at all, which is the sequencing `plan`'s first risk describes and accepts
  - Nothing else is decided yet. The plan's steps are executed in order and the choices made inside their latitude are recorded in the closing entry
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0 (branch created; `git branch --show-current` prints `wi/WI-0002`)
- **Gates:**
  - `tests-pass` → **pending** (no code has changed yet; decided at the closing transition on the branch head; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (no test has been written yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range is empty at this moment, which is exactly the case the word `pending` exists for; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (advisory; the diff is empty; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (nothing under `docs/` has been touched; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/WI-0002`, created from `main` at `ce87246`; no commit yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started on `wi/WI-0002`. The plan was read in full and reconciles with the code on disk; the closing entry reports the work.

## 2026-09-10T15:32:22Z — implement v0.6.0 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, resumed within the same execution that opened the branch
- **Inputs read:**
  - `tracker/items/WI-0002/artifacts/plan.md` — all eleven steps, the AC mapping, P1–P4, the ten-row invalidation set, `none` for deliverable documents and for scaffolding, seven binding ADRs, five risks
  - `tracker/items/WI-0002/item.md` — the nineteen criteria, read again at the end against the report
  - `envel/cli.py`, `envel/store.py`, `envel/envelopes.py`, `tests/test_cli.py` as WI-0001 left them
  - `docs/architecture/overview.md` (repaired), and `docs/architecture/adr/ADR-0003`, `ADR-0006`, `docs/process/ways-of-working.md` (reopened and found still true)
  - `docs/architecture/adr/ADR-0005` — to decide what this item's new output owes the non-UTF-8 locale, and what is `BUG-0001`'s
  - `.claude/agile-skills/spec/doc-header.md` §5 and §4b — who may write which document, walked skill by skill for the forced gate's second condition
  - `docs/process/ways-of-working.md`, `## When a pipeline gate refuses something no actor is permitted to fix` — the four conditions, and its own clause about dispatching an owner instead of forcing
- **Decisions:**
  - **Suspended rather than forced, and that is this entry's consequential decision.** `claims-are-sourced` reports three `claim.unsourced` errors and **none** of the three sentences was written, changed or falsified by this branch; they are in scope because `--plan-documents WI-0002` widens the window to every claim in every document the plan named, including the three it disposed `verified-still-true`. One of the three — `docs/product/vision.md:85`, an engagement-state sentence — has no possible actor before the ending and is exactly what `WI-0001/Q-003` and the ways-of-working convention already own. The other two do have an actor: `spec/doc-header.md` §5 makes `docs/process/ways-of-working.md` `answer-questions`' to update and §4b makes an ADR's `## Corrections` its append-only repair path, and `answer-questions` is dispatchable now. The convention's own words are *"If a skill the pipeline can dispatch could have made the repair, the answer is to dispatch it rather than to override the gate"*, so forcing over those two would have been a misuse of it. `Q-004` is filed blocking, the item suspends at `awaiting-answer` with `resume-to: in-progress`, and the next `implement` execution expects to force over the `vision.md` finding alone — where condition 2 is genuinely met
  - `InvalidAmount` gained an optional `reason`, so `envel/cli.py` can print plan step 5's two different refusals without a second copy of the amount grammar living in the CLI. How, not what
  - `_check_shape` tolerates a missing `transactions` key only on a **version 1** document. Plan step 3 says "check the key only when it is present"; read literally that lets a damaged version 2 document through the shape check and into a `KeyError` in `balances`. Narrowing it keeps assumption P4 and closes that
  - AC3 and AC5 are one test, because AC5 is defined as a fourth invocation over AC3's store; named `test_ac3_and_ac5_...` so a reader searching for either finds it
  - `StoreFormatTests` written, which the plan does not name: step 3's "afterwards" is a by-hand check, and three cases assert the same thing every run
  - The success line keeps plan step 5's wording, `—` included. Under the locale `BUG-0001` reproduces it cannot be encoded — the same out-hop `ADR-0005` already records as broken for `envel list` — and `ADR-0005` decision B fixes both at one boundary, which is `BUG-0001`'s step. Recorded in the report rather than deviated from: P1 makes the sentence the plan's
  - `docs/product/vision.md` not opened for repair at any point. Its row is `owned-by-ending`
  - One invalidation row added rather than an undeclared write: step 9's imports moved `tests/test_cli.py`'s helper, so the overview's `[src: tests/test_cli.py:29]` had gone stale and `plan` did not have it
- **Cross-answer check:** none. No sentence in `docs/` carrying `[src: <ITEM>/Q-nnn]` for a stakeholder-answered question was edited by this execution. `lint-answers --changed-since main` checked 10 consumed human answers and 0 delegations and reported 0 errors
- **Questions raised:** `Q-004` (blocking, addressed to the architect)
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 69 tests`, `OK` (run last on the branch head)
  - `python3 -m compileall -q envel tests` → 0
  - `python3 -c "from envel import movements; print(movements.parse_amount('£12.50'))"` → 0, prints `1250` (plan step 1's own check)
  - six deliberate mutations, each reverted: list without the balance → 23 failures; `spend` without the balance check → 1; `parse_amount` accepting any precision → 3; the recording line without the date → 2; `format_amount` at one decimal place → 23; no version 1 upgrade → 2
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → 1, 3 errors
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1, `doc.changelog.no-execution` on `docs/architecture/overview.md:81`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests`, `OK`, on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **fail** (`doc.changelog.no-execution` on `docs/architecture/overview.md:81`: the row names `implement` and `WI-0002` at `2026-09-10T15:28:26Z` and the journal entry that makes it true is the one this very command appends. Fourth occurrence in this engagement — `WI-0001`, `BUG-0001` and `WI-0002`'s `ready → planned` were the others. It does not block this move, which is not this skill's completion transition, and it clears the instant the command finishes)
  - `every-criterion-has-a-test` → **pass** (all nineteen criteria mapped to a named test function in `artifacts/impl-report.md`; six mutations each broke the suite, so the cases can fail)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → `all 3 commit(s) on main..wi/WI-0002 name WI-0002`; a fourth commit carries the report and the repairs)
  - `no-unplanned-scope` → **pass** (advisory; `git diff --stat main..HEAD` is five files, every one named by the plan, and the five deviations a reader would not predict are written out in the report)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0, `checked 10 consumed human answer(s) and 0 delegation(s)`, window non-degenerate: 1 path differs from `main` under `docs`)
  - `claims-are-sourced` → **fail** (`lint-claims --changed-since main --plan-documents WI-0002` → 3 errors: `ADR-0006:39`, `ways-of-working.md:96`, `vision.md:85`. Scope printed: `5 document(s) in 5 path(s) — 1 path(s) differ from main (ce87246) under docs, plus 5 document(s) named by WI-0002's plan`, so the window was not empty. Not forced — `Q-004` filed and the item suspended, because two of the three have a dispatchable owner)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, `1 document(s) written under docs/ on this branch; 5 named by the plan`)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md`
  - `tracker/items/WI-0002/artifacts/plan.md` — the `disposition` column only, eleven entries closed, and one row appended
  - `tracker/items/WI-0002/questions/Q-004.md`
  - `envel/movements.py` (new), `envel/store.py`, `envel/cli.py`, `tests/test_movements.py` (new), `tests/test_cli.py`
  - `docs/architecture/overview.md` → version 3
  - branch `wi/WI-0002`, commits `d4a460f..9d7b96b` (four, `main` at `ce87246`)
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** WI-0002 is built, green at 69 tests, and every criterion is mapped to a named test in the implementation report; all eleven invalidation entries are disposed and `docs/architecture/overview.md` is repaired to version 3. The item does **not** go to `verifying`: `claims-are-sourced` fails on three sentences this branch never wrote, and two of the three belong to `answer-questions`, so `Q-004` is filed blocking and the item suspends at `in-progress`.

## 2026-09-10T15:37:10Z — answer-questions v0.6.2 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`, dispatched by `next` at step 3 — `Q-004` is open and addressed to the architect, and is the only answerable question in the workspace
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-004.md` — the only open question on this item; `Q-001`, `Q-002` and `Q-003` are `answered` and were re-read for the cross-answer check
  - `tracker/items/WI-0002/history.md` — the suspending row carries `resume-to: in-progress`
  - `tracker/items/WI-0002/artifacts/plan.md` — the invalidation set, to re-dispose the two rows this execution wrote to
  - `tracker/items/WI-0002/artifacts/impl-report.md` — for the print-site enumeration `implement` had already made, re-run rather than copied
  - `.claude/agile-skills/spec/doc-header.md` §4a (the three claim kinds and the citation forms), §4b (correcting a standing ADR), §5 (which skill writes what)
  - `.claude/agile-skills/spec/dor-dod.md` D12, for whether an engagement-state sentence is inside the audit obligation
  - `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` v1, `docs/process/ways-of-working.md` v2, `docs/product/vision.md` v3 (`## Engagement state` **not** read for repair — its section was left closed)
  - `docs/architecture/adr/ADR-0001` … `ADR-0007`, checked for a decision this answer would contradict; none does
  - `envel/cli.py` and `envel/movements.py`, to enumerate the print sites the ADR-0006 citation asserts
- **Decisions:**
  - **`Q-004`, both halves, answered from the record — route 1, no ADR needed.** `spec/doc-header.md` §4a attaches the citation obligation to the **paragraph**, not to the clause a gate quotes, and both flagged paragraphs contain an absolute and a backticked code token. The asker's reasoning — that an option label and a conditional are not claims about named code — is right about each sentence's emphasis and wrong about the rule's unit. So both owed a citation and both now carry one
  - **`implement`'s recommendation to leave `ADR-0006` alone was refused, and the refusal is the substantive decision here.** The recommendation rested on `## Options considered` being a record of what was weighed rather than a statement about the product. That is a sound argument about **supersession** — §4 protects what was decided and nothing here changes it — but §4b exists for exactly this gap and was written from a run where a reviewer read three true-but-unsourced claims in a standing ADR, could not add citations, and left a permanent lint error behind (F-067). A `provenance` correction adds a citation with the assertion unchanged, and no reader would have to change any code to satisfy the new text, which §4b names as the boundary
  - **The `ways-of-working` sentence was changed twice, and the second change was the gate's suggestion.** Adding the citations left `no` in *"If no dispatchable item opens that code"*, and `propagated-claims-carry-their-obligation` then asked for the enumeration a quantified claim owes over *dispatchable items that open that code*. That family is not enumerable — the clause is a condition evaluated per gap, so any enumeration would be true of one instance and assert nothing. Took the gate's own alternative and weakened the clause to *"Absent a dispatchable item that opens that code"*, which says the same thing as a cited fact. Recorded in `Q-004`'s `## Consequences` so a reader does not have to reconstruct why one paragraph moved twice
  - **`docs/product/vision.md` was not opened for repair.** Its `## Engagement state` is the third `claim.unsourced` error and it is the ending's: `spec/doc-header.md` §4a gives every such section to `review-close` after the sign-off, and `spec/dor-dod.md` D12 puts them outside the audit obligation. This is the move F-093 exists to prevent — the sentence is plainly wrong, this execution was the only one looking, and it was left alone. The row was already `owned-by-ending` in WI-0002's invalidation set
  - **The `--plan-documents` window is a real finding and was recorded rather than acted on.** `claims-are-sourced` charged WI-0002 for prose it correctly disposed as untouched, because the flag widens the window to every claim in every document the plan named — so an item whose invalidation set is honest about what it reopened is audited harder than one whose set is thin. `scripts/lint-claims` is toolkit machinery and no skill here may edit it; written into `Q-004`'s answer for the retrospective
  - **No acceptance criterion was amended and no ADR was superseded.** Nothing in this answer is about what WI-0002 must do
- **Cross-answer check:** none — `Q-004` was raised by `implement` and answered by the architect from `spec/doc-header.md`; no answer of the stakeholder's was consumed. All nine of their recorded answers were considered for relevance and none is about citations, linting or the pipeline's own conventions, and no sentence carrying `[src: <ITEM>/Q-nnn]` for a stakeholder-answered question was edited — `ADR-0006`'s new citations are `envel/movements.py:68` and `WI-0002/Q-004`, and `ways-of-working.md`'s are two `spec/` paths. `lint-answers --item WI-0002` → exit 0, `checked 3 consumed human answer(s) and 0 delegation(s)`
- **Questions raised:** none — nothing was re-addressed to the human, and no answer widened the scope, so no item was filed
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0002 --uncommitted` → 1 then 0 (the first run demanded an enumeration for `ways-of-working.md`; the second, after the clause was weakened, reports `1 quantified sentence(s) newly written … 0 unanswered`)
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → 0
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → 1, and its error count fell from 3 to 1
  - `grep -n "print(" envel/cli.py` → 21; `grep -rn "print(" envel/ --include=*.py | grep -v "^envel/cli.py" | wc -l` → 0; `grep -rn "format_amount(" envel/` → five call sites at three print sites — the enumeration written into `Q-004`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1 (`doc.changelog.no-execution` on both edited documents, cleared by the journal entry this command appends)
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in `Q-004`'s `## Consequences` was opened and carries the change: `ADR-0006` line 43 shows the new `[src: envel/movements.py:68; WI-0002/Q-004]` and a `## Corrections` section exists; `ways-of-working.md` shows *"Absent a dispatchable item…"* with both citations; `plan.md`'s two rows read `to-update — re-disposed by answer-questions for WI-0002/Q-004`. `vision.md` and `item.md` are named as deliberately unchanged, with the reason)
  - `answered-from-the-record` → **pass** (route 1: `spec/doc-header.md` §4a for the obligation and its unit, §4b for the repair instrument, §5 for who may make it, `spec/dor-dod.md` D12 for why the third error is out of scope. No ADR was needed and none was written)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human; none of `spec/question.md` §4's four conditions applies — the record was not silent, nothing here is irreversible, no ADR is contradicted, and no intent of the stakeholder's is involved)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0002 --uncommitted` → exit 0, `0 unanswered`. The one quantified sentence written is `ADR-0006`'s option B, whose enumeration in `Q-004` carries the set, the command with its output, three members, a verdict for each, and a falsifier — a print that interpolates a figure without `format_amount` — checked at the boundary the absolute has, which is the amount refusal that echoes the text typed rather than a figure computed)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, `2 document(s) in the window, compared region by region against HEAD`; no `## Engagement state` region was written, and `vision.md` was not in the window at all)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0)
  - `workspace-valid` → **fail** (`validate-workspace` after this transition; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel --resolving 'WI-0002:awaiting-answer->in-progress+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-10T15:32:22Z records `resume-to: in-progress`, and this move is `awaiting-answer → in-progress`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred: `Q-004` was answered by the architect from the record, not by a person saying "later")
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-004.md` — answered, with `## Answer`, `## Cross-answer check`, `## Consequences` carrying the ADR-0006 enumeration, and a `## Verification` block quoting the gate's new output
  - `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` — version 1 → 2; option B cited; `## Corrections` created with one `provenance` entry
  - `docs/process/ways-of-working.md` — version 2 → 3; the *"What it is not"* paragraph cited and its opening clause weakened
  - `tracker/items/WI-0002/artifacts/plan.md` — two invalidation rows re-disposed `verified-still-true` → `to-update`
- **Status:** `awaiting-answer` → `in-progress`
- **Result:** `Q-004` is answered from `spec/doc-header.md` alone. Both sentences it asked about now carry resolving citations — `ADR-0006` through an append-only `provenance` correction, `ways-of-working.md` through an ordinary update by a skill §5 names as its updater — and `claims-are-sourced` falls from three errors to one. The remaining error is `vision.md`'s engagement-state sentence, which nobody may repair before the ending; WI-0002 resumes at `in-progress` with that single finding in front of it.

## 2026-09-10T15:39:41Z — implement v0.6.0 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, resumed by `next` after `answer-questions` returned the item to its recorded `resume-to`
- **Inputs read:**
  - `tracker/items/WI-0002/history.md` — the last row is `awaiting-answer → in-progress` by `answer-questions`, not a send-back from `verifying` or `in-review`, so this is a resumption rather than a defect fix
  - `tracker/items/WI-0002/questions/Q-004.md` — now `answered`; read for what it propagated, not for the answer itself
  - `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` **v2** and `docs/process/ways-of-working.md` **v3** — the artifacts the answer landed in, re-read on disk
  - `tracker/items/WI-0002/artifacts/plan.md` — the invalidation set, whose two re-disposed rows are what the answer changed here
  - `tracker/items/WI-0002/artifacts/impl-report.md` — this execution's own report from before the suspension
  - `.claude/agile-skills/spec/dor-dod.md` D12 and `docs/process/ways-of-working.md` `## When a pipeline gate refuses something no actor is permitted to fix` — the four conditions, walked below
  - the branch: `git log --oneline main..HEAD` → seven commits, three of code and tests, four of record
- **Decisions:**
  - **Nothing was rebuilt.** The reconciliation found all eleven plan steps already done on `wi/WI-0002` at `dea5528`: `envel/movements.py` and `tests/test_movements.py` exist, `envel/store.py` is at format version 2, `envel/cli.py` carries `income`, `spend` and `_take_date`, the eight WI-0001 literals are moved, and `docs/architecture/overview.md` is at version 3. Redoing any of it differently is the defect this step exists to prevent, so the work of this execution was gates, the report and the transition
  - **Fixed a defect `answer-questions` left in `plan.md`, and it was mine to fix.** It re-disposed two invalidation rows by writing its reasoning **into the disposition cell**, so the cell read `to-update — **re-disposed by …** …` and `document-writes-are-declared` refused it with `document.disposition.unknown` on both rows: *"a disposition outside the enum is a sentence, and the consumers of this set branch on the word"*. The disposition column is the one part of `plan.md` this skill writes (`SKILL.md` step 4a), so the prose was moved into the `why` cell — where it is kept in full, because it is the record of why a `verified-still-true` row became `to-update` — and the disposition cell left holding `to-update` alone. Not journalled as someone else's failure to escalate: it is a formatting slip in a column this skill owns, and the gate caught it before anything downstream read the word
  - **`claims-are-sourced` forced, on one finding rather than three.** The four conditions are in the `**Gates:**` bullet below. The reason this execution is entitled to force where the last one was not is that the two findings with a dispatchable owner have been dispatched and repaired: condition 2 now holds for everything the gate reports
  - **The report's own commit count is one behind the branch head, and deliberately.** `impl-report.md` records `all 6 commit(s)`; the head is at seven because the seventh commit is the one carrying that report. A report cannot state the count of a range that includes itself, so the current figure is here instead: `check-commit-refs WI-0002 wi/WI-0002` → `all 7 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0
- **Cross-answer check:** none. This execution wrote no sentence into `docs/` at all — the only documents on this branch's diff are `docs/architecture/overview.md` (repaired by the earlier half of this same execution) and `ADR-0006` and `ways-of-working.md` (written by `answer-questions`). No claim carrying `[src: <ITEM>/Q-nnn]` for a stakeholder-answered question was edited by anyone on this branch, which `lint-answers --changed-since main` confirms over a window of 3 paths
- **Questions raised:** none — `Q-004` was raised by this skill's previous execution and is answered
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 69 tests`, `OK`
  - `python3 -m compileall -q envel tests` → 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 7 commit(s)`
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → 1 then 0 (`document.disposition.unknown` on two rows, then clean after the prose moved)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → 1, one error
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests`, `OK`, run on the branch head at `0fae075`)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` → `checked 7 item(s), 10 document(s)`, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (all nineteen criteria mapped to a named test function in `artifacts/impl-report.md`, plus the eleven-row read AC12 asks for; six mutations each broke the suite, so none of the cases passes against an absent implementation)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → `all 7 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0)
  - `no-unplanned-scope` → **pass** (advisory; `git diff --stat main..HEAD` under `envel/` and `tests/` is the same five files as before the suspension, every one named by the plan. Nothing was added this pass)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0, `claim window: 3 path(s) differ from main (ce87246) under docs`, `checked 10 consumed human answer(s) and 0 delegation(s)`)
  - `claims-are-sourced` → **fail, FORCED.** `lint-claims --changed-since main --plan-documents WI-0002` → exit 1. Scope: *"5 document(s) in 5 path(s) in scope — 3 path(s) differ from main (ce87246) under docs, plus 5 document(s) named by WI-0002's plan"*, so the window is not one that could contain nothing. Its whole output is one error: *"docs/product/vision.md:85: ERROR [claim.unsourced] an absolute claim ('no') about 'EP-001/Q-001' with no citation"*. The four conditions of `docs/process/ways-of-working.md`, `## When a pipeline gate refuses something no actor is permitted to fix`, in order. **(1) The finding is outside the rule the gate implements.** `spec/dor-dod.md` D12 says of the obligation `lint-claims` rule 2 mechanises: *"**Engagement-state sentences are out of scope**: no item audit is charged with one"*. `docs/product/vision.md:85` is inside that document's `## Engagement state` section, which begins at line 83 and runs to line 91. **(2) The change that would clear it is unavailable, skill by skill through the nine of `pipeline.yaml`.** `next` writes no document but the board and the halt log. `verify` writes no document ever, and `retro` none either (`spec/doc-header.md` §5). `intake` creates `vision.md` but is dispatched only on an open request under `tracker/requests/`, and there is none. `refine` and `answer-questions` are §5's updaters of `vision.md`, and §4a forbids each of them this particular sentence — an engagement-state section belongs to the ending — which `answer-questions` demonstrated rather than asserted this very round: dispatched on `Q-004`, holding the licence to write `docs/product/`, it left the sentence untouched and said so in `Q-004`'s `## Consequences`. `plan` creates `architecture/overview.md` and `process/ways-of-working.md`, not `product/`. `implement` — this skill — is forbidden by §5's rule that it never writes an engagement-state sentence, at any disposition. `review-close` **owns** it, restating every such section at the ending under `spec/dor-dod.md` DE4, and the condition under which it may is one that does not hold: `engagement-state EP-001` → `active`, five children still in flight, so there is no ending to restate at. **(3) A question records the diagnosis, the options and the decision.** `WI-0001/Q-003`, answered, is the original diagnosis and is what `ways-of-working.md`'s section was written from; `WI-0002/Q-004`, answered this round, records this occurrence, states that this sentence *"survives this execution deliberately"*, and gives the reason. **(4)** This bullet carries the verdict as `fail` with the run's own output, and the history reason names both questions. What the convention also says, and what makes this force different from the one this item's previous execution refused to make: *"If a skill the pipeline can dispatch could have made the repair, the answer is to dispatch it rather than to override the gate."* Two of the three findings had such a skill, it was dispatched, and it repaired them — which is why the error count is 1 and not 3
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, `3 document(s) written under docs/ on this branch; 5 named by the plan`. It refused once first, with `document.disposition.unknown` on the two rows `answer-questions` re-disposed; the prose moved to the `why` cell and the enum word stayed in the disposition cell)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` — `## Documents` rows for `ADR-0006` and `ways-of-working.md` now record their new versions and who wrote them; the gate table updated; `## What I did not do` records that `answer-questions` refused this report's recommendation about `ADR-0006` and why
  - `tracker/items/WI-0002/artifacts/plan.md` — the two disposition cells repaired to the enum word, their reasoning kept in `why`
  - branch `wi/WI-0002` at `0fae075`, seven commits, `main` at `ce87246`
- **Status:** `in-progress` → `verifying`
- **Result:** WI-0002 goes to `verifying`. Nineteen criteria, each with a named test; 69 tests green; every invalidation entry disposed and every document on this branch declared. One hard gate is forced — `claims-are-sourced`, on the single engagement-state sentence in `docs/product/vision.md` that no skill may repair before the ending — and the two findings that did have an owner were dispatched to it and repaired rather than overridden.

## 2026-09-10T15:58:36Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying` — `implement` reported the branch complete and green; dispatched by `next` as the highest-ranked runnable item (priority high beat BUG-0001's medium)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the nineteen acceptance criteria, read **before** the implementation report
  - `tracker/items/WI-0002/artifacts/plan.md` — the eleven steps, the seven binding ADRs, the eleven-row invalidation set
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria, and checked rather than quoted
  - `tracker/items/WI-0002/history.md`, and `questions/Q-001`…`Q-004`
  - `tracker/items/WI-0001/item.md` — AC12's subject: the eleven criteria and the six `superseded` markers
  - all seven of `docs/architecture/adr/ADR-0001`…`ADR-0007`, in full, for the conformance verdicts
  - every document in the invalidation set: `docs/architecture/overview.md`, `docs/product/vision.md`, `docs/architecture/adr/ADR-0003`, `ADR-0006`, `docs/process/ways-of-working.md`
  - `tracker/project.yaml` — the two gate commands
  - the code at `wi/WI-0002` head `ae397c22ae785bbcca7982142f7b0bd49dba2843`: `envel/cli.py`, `envel/movements.py`, `envel/store.py`, `envel/envelopes.py`, `bin/envel`, `tests/test_cli.py`
  - `.claude/agile-skills/spec/doc-header.md` §5 and §4b, `spec/dor-dod.md` D7/D12/D13, `spec/question.md`
- **Decisions:**
  - **All nineteen criteria pass, each on a command run here.** Derived what would settle each criterion from the criterion before looking at what was built. Nothing is evidenced by `impl-report.md`.
  - **AC12 is a read, not a run.** Named all eleven of `WI-0001`'s criteria by ID and gave each its own verdict from its sentence. Five hold as written; six are waived by name, and each of the six was checked to carry the `superseded` marker on `WI-0001/item.md` rather than assumed. Stated non-intersection both ways: it does **not** exist for the five, because plan step 8 rewrote the `WI-0001` cases so they assert the old criterion and the new column in one assertion, and mutation M16 failed one of them; it is **intrinsic** for the six, since no case can assert both the old *name-only* line and the new shape — AC15 and AC19 carry the substance instead, and both were run.
  - **`WI-0001` AC4 was checked on a set built to break it.** AC12 flags it as most likely to break. Two names would not distinguish a byte-wise sort from a casefold one, so five were used — created `rent, Zebra, apple, Apple2, eating out`, printed `Apple2, Zebra, apple, eating out, rent`, equal to an independently computed `sorted(names)`, where a casefold sort would have ordered them differently.
  - **ADR-0006 rule 3 is quantified, so it owed members rather than a citation.** Enumerated the set by `grep -n "print(" envel/*.py` → 21 sites, 3 carrying money, 5 printed figures; verdict per member; falsifier stated two ways and both tried; and checked **at the boundary** — `0.05`, `0.00`, `7.00` — rather than at the happy path.
  - **`ADR-0004`'s rule 3 is stretched by this change, and it is recorded rather than smoothed over.** *"Nothing downstream folds a name a second time"*, yet `movements.balances` computes `identity` on stored names. Verdict `conforms`: rule 3 guards against folding the person's *input* twice, and `ADR-0007` §2 — this item's own architect, citing `ADR-0004` — states that matching a movement by identity *"is `ADR-0004`'s rule and not a second one"*. The tension is in the conformance row.
  - **Four falsified `[src: path:line]` citations, and the classification is the substantive call.** Not a send-back and not a bug item. Not a **bug item**: no behaviour delivered by another item is broken, and `BUG-0001` already owns the non-UTF-8 paths. Not a **send-back**, even though this item's own change caused it: `spec/doc-header.md` §5 does not permit `implement` to repair any of the three documents — an ADR's document half takes only an append-only `## Corrections` entry, and `ways-of-working.md`'s updaters are `review-close` and `answer-questions` — so `in-progress` would hand `implement` a repair it is forbidden to make. SKILL.md's *"send-back if this item's own change made it false"* and §5 point at different owners here; §5 decides who **can** act, so the routing follows it. Filed `Q-005` to the architect, which is the route `Q-004` took on this same item for the same class of finding.
  - **The criteria are ticked even though the item is suspended.** D1/D2 are met and the evidence is in `verify-report.md`; what is unmet is D7 and D12. Ticking on demonstrated evidence and suspending on the document defect are two separate statements, and collapsing them would lose one.
  - **The `ways-of-working.md` invalidation row's `verified-still-true` claim is false**, and this is exactly what the reopening obligation exists to catch: the row says the document *"mentions neither the tool's behaviour, its store or its commands"*, and the section it names cites `envel/store.py` twice by line. It survived a re-disposition for `Q-004` because that re-disposition was about a different sentence.
  - **No document was written by this execution.** Four sentences were found wrong and none was edited.
- **Questions raised:** WI-0002/Q-005
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests`, `OK` (run twice: at the start, and after the mutation work with `git status --short` clean)
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 7 item(s), 10 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0002` → exit 1 then, after naming `envel/movements.py:50` in the `ADR-0005` row, exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 1 then, after writing the two ADR paths in full rather than abbreviated, exit 0; `11 invalidation entr(y/ies) against 11 row(s)`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → exit 1, 1 error, `docs/product/vision.md:85` — the engagement-state sentence, the ending's
  - `git rev-parse HEAD` → `ae397c22ae785bbcca7982142f7b0bd49dba2843`; `git diff --stat main..HEAD`; `git diff main..HEAD -- envel/store.py envel/cli.py bin/`; `git show main:envel/store.py`; `git show main:envel/cli.py`; `git log --oneline -8 wi/WI-0002`
  - ~90 `bin/envel` invocations against scratch stores under `ENVEL_FILE`, one scenario per criterion — every command and its actual output is in `artifacts/verify-report.md`'s `## Criteria`
  - a by-hand audit of all 25 `[src: <path>:<line>]` citations in `docs/`, each resolved against the branch head with a short Python walk of `docs/**/*.md` — this is what found the four
  - `env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C envel list` against a store holding `café` → exit 1, `UnicodeEncodeError` at `envel/cli.py, line 100, in _list`
  - `LC_ALL=C … envel income groceries £12.50` → exit 1, one clean stderr line, no traceback
  - 17 mutations, each `python3 -m unittest discover -s tests -t .` then `git checkout -- envel/` → 1 to 26 failing tests each; table in `verify-report.md`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 69 tests`, `OK`, on the branch head with a clean tree; re-run after the mutation work)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, `checked 7 item(s), 10 document(s)`, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (nineteen rows in `verify-report.md`'s `## Criteria`, each with the command run here and its quoted output; `impl-report.md` is cited as evidence nowhere)
  - `negative-cases-exercised` → **pass** (every refusal triggered rather than read about: unknown envelope, overspend, two malformed dates, zero and negative on both commands, non-numeric and empty, missing arguments on both, over-precision on both, duplicate and whitespace-only names, empty store; boundaries at the exact balance, a zero balance, sub-pound and whole-pound figures at all three print sites, a version 1 store, a store from a newer build)
  - `a-criterion-about-criteria-is-read` → **pass** (AC12: eleven criteria named by ID with a per-criterion verdict read from each sentence, the six waivers named individually and checked against `WI-0001`'s `superseded` markers, non-intersection stated in the gate's own words for both groups)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0002` exit 0; seven rows, each quoting a clause of that ADR's `## Decision` with the file and line, plus ADR-0006 rule 3's member enumeration and falsifier)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0002` exit 0; eleven rows, the one `verified-still-true` entry reopened against the branch head, and the finding that the `ways-of-working.md` row's claim is false)
  - `tests-would-fail-without-the-change` → **pass** (advisory; 17 mutations, every criterion covered by at least one that failed a test naming it, 1 to 26 failures each; no test survived the removal of the behaviour it claims to test)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — written, at `Verified-commit: ae397c22ae785bbcca7982142f7b0bd49dba2843`
  - `tracker/items/WI-0002/item.md` — all nineteen criteria ticked `- [x]`
  - `tracker/items/WI-0002/questions/Q-005.md` — filed, blocking, to the architect
  - no bug item filed; no file under `docs/` written
- **Status:** `verifying` → `awaiting-answer`
- **Result:** WI-0002's behaviour is verified: all nineteen criteria pass on evidence gathered here, all seven binding ADRs conform, and seventeen mutations show the suite can fail. The item is suspended rather than passed because four `[src: path:line]` citations in `ADR-0005`, `ADR-0007` and `ways-of-working.md` were falsified by this item's own edits and still resolve mechanically, so D7's closing question is answered wrongly and one `verified-still-true` claim is false. `verify` may not repair a document and `implement` is not an updater of any of the three, so it is `Q-005` to the architect with `resume-to: verifying`.
