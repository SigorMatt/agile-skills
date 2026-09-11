# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T10:58:28Z — review-close v0.14.1 — reviewer

- **Item:** BUG-0001
- **Trigger:** not dispatched — filed by this `review-close` execution on `EP-001`, whose Definition of Done walk failed at DE3. The execution's full record is the entry of the same timestamp on `tracker/items/EP-001/journal.md`; this entry exists because `review-close` is the actor on this item's creation row and an execution with no entry is indistinguishable from one that never happened
- **Inputs read:**
  - `tracker/items/EP-001/item.md` `## Success measures` — the sentence this bug contradicts
  - `tracker/items/EP-001/questions/Q-002.md` and `tracker/items/WI-0005/questions/Q-004.md` — the stakeholder's two statements of the rule, in their own words
  - `tracker/items/WI-0005/questions/Q-001.md` and `tracker/items/WI-0003/questions/Q-003.md` — the workflow that makes it reachable, and the reason income cannot be backdated
  - `tracker/items/WI-0002/item.md` AC5 and `tracker/items/WI-0005/item.md` AC9 — the guards that hold, and the scope each is written to
  - `tracker/items/WI-0003/item.md` AC3, AC7 and AC8, and `tracker/items/WI-0006/item.md` AC9 — what the two surfaces were required to do
  - `envel/summary.py` in full — `figures`, `bounded_balance`, `balance_before`, `balance_through`, `list_entries`
  - `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` in full — read to check whether a past month closing below zero was a decision already taken; it is not mentioned there
  - the tool itself, run against `/tmp/de3b/store.json`
- **Decisions:**
  - **Filed as a `bug` at `ready` rather than as a work item or a note.** `spec/dor-dod.md` §4a: a DE1–DE6 failure at the ask *"is not an ending. It is work."* The pipeline row that permits it is `from: null → ready`, actor `review-close`, for a `bug`, with `arose-from` naming the item under review and `found-in` naming the item whose delivered behaviour it contradicts.
  - **`found-in: WI-0003`, not `WI-0006`.** Both surfaces print the figure, but the month-bounded balance was introduced as `summary.figures`' `left` for `WI-0003`; `WI-0006`'s opening and closing lines are the same sum with the bound made an argument. The body names both so that nothing rests on the choice.
  - **Priority `high`.** It is the stakeholder's own rule, given twice and unqualified, and the epic cannot end while a success measure is false.
  - **The criteria pin the observable requirement without choosing the remedy.** AC1 and AC2 say no amount less than zero is printed, at each surface; AC3 covers the refusal branch if `plan` takes it, and says how it is decided if `plan` does not; AC4 is the regression pair with the baseline commit named; AC5 names the four test files that must keep passing unmodified. A criterion that picked a remedy would be `review-close` doing `plan`'s job in a place no ADR records.
  - **Definition of Ready for a bug, walked at filing time as `spec/dor-dod.md` §2 requires:** RB1 **pass** — seven numbered steps, every one an exact command, with the month-relativity stated in the preamble so a reader in a later month can still run them; RB2 **pass** — `## Actual behaviour` quotes three real outputs with their exit codes, including the contrasting `envel list` that is correct; RB3 **pass** — `## Expected behaviour` cites `EP-001`'s success measure, `EP-001/Q-002` and `WI-0005/Q-004`, and `docs/product/vision.md`; RB4 **pass** — `found-in: WI-0003`, and `arose-from: EP-001`; RB5 **pass** — AC4 is the regression test, with the commit it must fail at named.
  - **Step 7 is honestly labelled a store-file probe.** The second surface needs an envelope that existed in the month being summarised and the tool stamps `created` itself, so it cannot be reached through the command line inside one calendar month. Saying that is better than omitting the surface or implying a command produced it.
- **Cross-answer check:** none — this filing consumed no human answer. It quotes four recorded ones as evidence and changes none of them; the contradiction it records is between one of those answers and the code.
- **Questions raised:** none — the question this bug will need is `plan`'s to ask, and `## Notes` says so rather than filing it from here
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --next-id bug` → exit 0, `BUG-0001`
  - `python3 .claude/agile-skills/scripts/new-item --id BUG-0001 --type bug --title "…" --epic EP-001 --priority high --status ready --actor review-close --found-in WI-0003 --arose-from EP-001` → exit 0, `created BUG-0001 at status ready`
  - `python3 -m envel new groceries`, `add groceries 300.00`, `spend groceries 250.00 "august shop" --on 2026-08-14`, `list` → exit 0 each
  - `python3 -m envel entries groceries --month 2026-08` → exit 0, `groceries holds -250.00 at the end of 2026-08`
  - `python3 -m envel summary 2026-08` (after the step-7 probe) → exit 0, `groceries  in 0.00  spent 250.00  moved 0.00  left -250.00`
  - `python3 -m unittest discover -s tests -t .` → exit 0, 299 tests — the baseline AC4 and AC5 cite
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the two unrecognised citation markers in the body were rewritten to the `item` form, and after two `path:line` citations were corrected from lines they did not name to `envel/summary.py:68` and `envel/summary.py:173`
- **Gates:** the contract's gates belong to this execution as a whole and their evidence is recorded once, on `EP-001`'s entry of this timestamp. By name, as they stood there:
  - `definition-of-done` → **fail** (DE3, on `EP-001`; this item is the consequence of that failure, not a subject of the walk)
  - `engagement-state-is-restated` → **pass** (on `EP-001`; nothing restated, both sections enumerated)
  - `accepted-gaps-are-dispatchable` → **pass** (on `EP-001`; 0 accepted gaps — this finding was filed, not accepted)
  - `verification-postdates-the-code` → **skipped** (no branch and no verification on either item; this one has not been implemented)
  - `commits-reference-the-item` → **skipped** (no branch; this item's record commit goes on the trunk carrying its ID)
  - `tests-pass-on-the-merge-result` → **skipped** (nothing is being merged; the suite run above is the baseline AC4 cites and discharges no gate)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0 with this item's body in place)
  - `record-is-reconstructible` → **pass** (on `EP-001`; this item's own record is one creation row and this entry)
  - `claims-are-sourced` → **pass** (`lint-claims --context epic --changed-since main` exit 0 over every markdown file in the workspace, this body included)
  - `cross-answer-consistency` → **pass** (`lint-answers --context epic --changed-since main` exit 0)
  - `epic-sign-off` → **fail** (on `EP-001`; no sign-off could be filed over a state that fails DE3)
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` (new, body written in full)
  - `tracker/items/BUG-0001/history.md` — the creation row, written by `scripts/new-item`
  - `tracker/items/EP-001/artifacts/review.md` — where this finding is recorded as finding 1
- **Status:** `—` → `ready`
- **Result:** A bug filed at `ready` for the one Definition of Done failure `EP-001` produced: a past month's closing figure can show an envelope holding a negative amount, at two surfaces, against a rule the stakeholder stated twice without qualification. It carries the reproduction, both outputs verbatim, five criteria that pin the requirement without choosing the remedy, and a note saying why the remedy is `plan`'s and probably the stakeholder's.

## 2026-09-11T11:01:53Z — plan v0.6.3 — architect

- **Item:** BUG-0001
- **Trigger:** status `ready`, dispatched by `next` step 4 — the only runnable item on the board
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — five criteria, the reproduction, and the `## Notes` naming the two candidate remedies
  - `tracker/items/BUG-0001/history.md` — one row, the creation by `review-close`
  - no `artifacts/refinement-qa.md`: a bug enters at `ready` and is not refined, so there is none to read
  - `tracker/items/EP-001/artifacts/review.md` — the Definition of Done walk that filed this item, and finding 2 beside it
  - `tracker/items/EP-001/item.md` `## Success measures`
  - the answers this design turns on, at their own files: `WI-0002/Q-001` (a spend carries the day it happened), `WI-0003/Q-003` (income is not dated), `WI-0005/Q-006` (a correction does not date an income either), `WI-0005/Q-001` (when they reconcile), `WI-0005/Q-004` and `EP-001/Q-002` (no negative envelopes), `WI-0006/Q-004` (the lines have to add up)
  - `tracker/items/WI-0003/item.md` AC3, AC7, AC8 and `tracker/items/WI-0006/item.md` AC9 — the criteria an option would have to amend
  - `docs/architecture/overview.md` (v9) and `docs/product/vision.md` (v7)
  - the eleven ADRs' `## Decision` sections; `ADR-0006` and `ADR-0008` in full, as the two that govern what month a figure counts an entry in
  - `envel/summary.py` in full, and `envel/envelopes.py` — `balance`, `record_spend`, `move`, `envelopes_below_zero`, `correct`, `remove`
  - `tracker/project.yaml`
- **Decisions:**
  - **This item cannot be designed without the stakeholder, and the reason is a rule rather than a preference.** `plan`'s preference order was applied in order and the first two branches are genuinely closed here:
    1. *Answer it from the documents.* No document decides it. `ADR-0006` settles that a spend carries `on` and income does not, and is silent about what a month-bounded balance may do; `ADR-0008` settles that every figure is a filtered sum and explicitly says *"nothing here checks the identity"*; no ADR mentions a lower bound on a month's closing figure. The three guards in `envel/envelopes.py` all read `balance()`, the unbounded sum, so the code records no decision about the bounded one either.
    2. *Make a reversible assumption.* Each candidate remedy contradicts something the stakeholder has already said, which is exactly what an assumption may not do. Refusing the backdated spend takes away the late reconciliation they described at `WI-0005/Q-001` and forces the *"Saturday shop landing in the wrong month"* they asked us to prevent at `WI-0002/Q-001`. Changing what is printed breaks the adding-up they asked for at `WI-0006/Q-004` and needs two delivered criteria amended. Dating income reverses `WI-0003/Q-003` and `WI-0005/Q-006`. Nothing here is reversible in the sense the preference order means — one file, no data migration, no published interface change.
    3. *Ask the human.* Which is this.
  - **More precisely, it is step 5a's case: two of their own answers have met and one has to give.** *"No negative envelopes anywhere in this tool"* [src: WI-0005/Q-004] and *"income … cannot be dated"* [src: WI-0003/Q-003] cannot both hold once a spend may be dated into a month whose income is already recorded elsewhere. `plan` may not record which of two stakeholder answers wins — *"Nobody asked the person who gave them"* is the failure that rule exists to prevent — so the question quotes both by ID and stops.
  - **One question, four options, and no plan written yet.** Writing `plan.md` now would mean designing against a remedy nobody has chosen; every section of it would be rewritten by the answer. The item suspends at `awaiting-answer` with `resume-to: ready`, so the plan is written by the execution that resumes, against a decided remedy.
  - **Option D is offered although they have refused it twice.** Dating income is the root of the behaviour rather than a handling of it, and an option list that hides the root to avoid re-asking a settled question is steering. It is marked as the root, and marked as something we do not think they have changed their mind about.
  - **The recommendation is C and is written as ours, after the options.** `spec/question.md` §2: options first, the recommendation last and marked as the team's preference. C is the only option that keeps both things they have asked for — no minus number, and freedom to type last month's spends late — and its whole cost falls on us. The recommendation also says plainly which option we would avoid and why, so the ranking is visible rather than implied by omission.
  - **Finding 2 from `EP-001`'s review was not filed as a second question.** A spend dated into a month before its envelope existed appears in no `spent` column; whether that matters depends on the answer to this question, and asking two entangled questions in one round is how a half-answer gets recorded as a whole one. It stays recorded in `BUG-0001`'s `## Out of scope` and in `EP-001`'s `artifacts/review.md`.
- **Cross-answer check:** this execution recorded no new human answer and relied on none. It read seven recorded answers as evidence and changed no sentence citing any of them — `lint-answers --uncommitted` exit 0 over 0 uncommitted paths under `docs`, which is the honest reading for an execution that edited no document. The conflict it found between `WI-0005/Q-004` and `WI-0003/Q-003` is **not** resolved here: it is quoted by ID in `Q-001`'s `## Context` and put to the person who gave both, which is ADR-0008 §3's only permitted move.
- **Questions raised:** `Q-001` (blocking, to human) — *"When a past month's closing figure for an envelope would be negative … what should the tool do?"* Four options with their costs: leave it and amend the success measure; refuse the backdated spend; keep recording and say the shortfall in words; or let income be dated. No answer yet.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 0 errors
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 0 errors
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the suspension; before it, the expected `question.blocking.not-suspended` on this item
  - `grep -n "def \|holds\|less than\|short" envel/envelopes.py` → exit 0, the three guards located, every one of them reading `balance()`
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0 once the item was suspended; the one error before that was `question.blocking.not-suspended`, which this transition is the cure for)
  - `every-criterion-is-addressed` → **skipped** (no `plan.md` exists, so `BUG-0001`'s AC1–AC5 have no mapping table yet. They cannot have one: AC3 is written to branch on which remedy is chosen, and AC1 and AC2 are satisfied by different code depending on that choice. The execution that resumes at `ready` owes the table)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` carries `test: python3 -m unittest discover -s tests -t .` and `lint: python3 -m compileall -q envel tests`; the test command was run this turn → exit 0, 299 tests. Neither is null and neither was changed)
  - `decisions-recorded` → **skipped** (this execution records one decision — that the remedy is the stakeholder's — and it is recorded where the protocol puts it, in `Q-001`, not in an ADR. The ADR is owed by the execution that resumes: it will record which remedy was chosen and why, with the answer as its context)
  - `plan-is-executable-without-you` → **skipped** (advisory, and there is no plan to read. Nothing was written that a developer could execute or misread)
  - `documents-at-risk-are-enumerated` → **fail** (the invalidation set is a section of `plan.md` and there is none. It is not writable yet either: which documents this change falsifies depends entirely on the remedy — option A rewrites a success measure and no document under `docs/`, option C rewrites `vision.md` and two delivered criteria, option D reaches `ADR-0006` and `ADR-0008`; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item BUG-0001 --root /home/msi/agile-skills-throwaway/envel-2` exited 1)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0; 33 consumed answers and 2 delegations checked. No document was edited, so rule 3 had nothing to look at and says so)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0. Scope, quoted: *"absolute claims: 0 document(s) in 0 uncommitted path(s) under docs; citations: every markdown file in the workspace"* — the absolute-claim half saw nothing because this execution wrote no document, and the citation half read `Q-001` along with every other markdown file in the workspace)
- **Artifacts:**
  - `tracker/items/BUG-0001/questions/Q-001.md` (new) — blocking, addressed to `human`
  - `tracker/board.md` (regenerated)
  - no `plan.md`, no ADR, no `docs/` edit and no change to `tracker/project.yaml`: all four wait on the answer
- **Status:** `ready` → `awaiting-answer`
- **Result:** `BUG-0001` cannot be designed without the stakeholder. Three of their recorded answers meet here and one of them has to give, which is not a decision `plan` may record. `Q-001` puts the four remedies to them with the cost of each, recommends one and marks the recommendation as ours, and the item is suspended at `awaiting-answer` with `resume-to: ready`.

## 2026-09-11T11:10:49Z — answer-questions v0.6.3 — architect

- **Item:** BUG-0001
- **Trigger:** `awaiting-answer` with `resume-to: ready`, suspended by `plan` on `Q-001`; the
  stakeholder filled in `## Answer` between turns, which is what makes the question answerable.
- **Inputs read:**
  - `tracker/items/BUG-0001/questions/Q-001.md` — the escalation, its four options and the reply
  - `tracker/items/BUG-0001/item.md` — the criteria the answer had to reach
  - `tracker/items/BUG-0001/history.md` — carries `resume-to: ready` on the suspending row
  - `tracker/items/BUG-0001/journal.md`
  - `docs/architecture/adr/` — all eleven ADRs listed; `ADR-0008` (a month is a string and every
    figure is a filtered sum) and `ADR-0009` (reporting lives in its own module) are the two the
    remedy touches, and neither records a decision this answer contradicts, so no ADR is superseded
  - `docs/product/vision.md` v7 — `## What it is for`, the paragraphs sourced to `EP-001/Q-002`
    and `WI-0005/Q-004`, and `## Engagement state`
  - `docs/architecture/overview.md` — `## Engagement state`
  - `tracker/items/EP-001/item.md` — `## Success measures`, which carries the rule this bug is
    filed against
  - `tracker/items/WI-0003/item.md` — AC3, AC8, AC11; `tracker/items/WI-0006/item.md` — AC9, AC10
  - `tracker/items/WI-0005/questions/Q-004.md`, `WI-0003/questions/Q-005.md` and the other prior
    human answers named in the cross-answer check
  - `tests/test_entries.py` — the two assertions at lines 173 and 310 that AC5 freezes
- **Decisions:**
  - `Q-001` — **answered by the human**, option C: keep recording the backdated spend and say a
    short month's shortfall in words instead of printing a minus. Route: the human replied to an
    escalation and this execution consumed the reply. Propagated to `BUG-0001/item.md` and
    `docs/product/vision.md`.
  - **AC1 amended**, and it is an amendment of an acceptance criterion, so it is called out here.
    It required no amount less than zero *"on any of its lines — opening, entry or closing"*. That
    reached the entry line showing the spend itself, which contradicts this item's own AC5: AC5
    freezes `tests/test_entries.py` as it stands at `127664a`, and two assertions there require an
    entry line to print `-30.00` and `-20.00`. One of the two had to give. It is AC1, because the
    entry line `2  2026-08-14  spend  groceries  -250.00  august shop` was printed verbatim in
    `Q-001`'s `## Context`, option C proposed changing only the closing line and the summary
    column, and the stakeholder chose C with that line in front of them. The amendment narrows AC1
    to the two balance lines and does not change what the stakeholder asked for.
  - **AC3 amended**: it branched on whether the design refuses the input. The answer settles that
    it does not, so the refusing branch is removed rather than left for a later reader to choose.
  - **AC6 added**, appended so nothing is renumbered: the worded line must still carry the figure
    that makes it reconcile. This is the condition the stakeholder attached to their own answer,
    and without it a clamp-to-zero fix would satisfy AC1 and AC2 while failing what they asked for.
  - **No ADR written.** The answer records the stakeholder's intent rather than an architectural
    choice, and the choice it forecloses — where the shortfall is computed — is still `plan`'s to
    make on an item that is now returning to `ready`.
  - **No work item filed, and the reason is recorded rather than assumed.** Option C was put to the
    stakeholder carrying a warning that `WI-0003` AC3 and `WI-0006` AC9 would need amending by a
    follow-up item. Their reply removed the need for one: a figure in words still carries the
    figure, and *"a figure I can read is what the adding-up rule was about"*. Both criteria stand
    unamended, both items stay `done`, and the obligation is carried by `BUG-0001` AC6 instead.
  - **No `## Engagement state` sentence written or amended.** The two sections describe the
    engagement as it stood at `intake` and were already out of date before this question was
    asked; this answer falsifies nothing new in either. `BUG-0001` has no `plan.md`, so there is no
    invalidation set to carry a row.
- **Cross-answer check:**
  - `EP-001/Q-002` — compatible: the overspend refusal is untouched; C stops a minus at a second
    moment rather than weakening the rule.
  - `WI-0005/Q-004` — compatible, and it is the sentence the bug was filed against; option A would
    have qualified it and the stakeholder refused A in those terms.
  - `WI-0003/Q-001` — compatible, and it was the pair at risk: *"I won't use a report whose rows
    don't add up"* against *"no negative envelopes"*. The stakeholder reconciled their own two
    sentences rather than leaving it to us, so `WI-0003` AC3 is neither amended nor reinterpreted.
  - `WI-0006/Q-004` — compatible, same reconciliation, same sentence of theirs; `WI-0006` AC9
    stands.
  - `WI-0002/Q-001` — compatible: option B would have broken the dated spend and they refused B.
  - `WI-0003/Q-003` — compatible: option D would have reversed it and they refused D.
  - `WI-0005/Q-006` — compatible: the second of the two refusals they counted.
  - No verdict of `conflicts`, so no question was filed under that rule. The one genuine tension
    was this question's whole subject and the stakeholder settled it in their own words.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-09-11T11:07:09Z`, the stamp used on the answer and the
    document
  - `python3 .claude/agile-skills/scripts/lint-answers --item BUG-0001` → exit 0, 1 consumed human
    answer checked
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item BUG-0001 --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
  - `grep -n "AC9 —" tracker/items/WI-0006/item.md`, `grep -rn -- "-[0-9]*\.00" tests/test_entries.py` → the AC5 conflict that forced the AC1 amendment
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in `Q-001`'s `## Consequences` opened and the change confirmed present: `tracker/items/BUG-0001/item.md` carries the rewritten `## Expected behaviour`, the amended AC1 and AC3, the appended AC6 and the rewritten `## Notes`; `docs/product/vision.md` carries the new paragraph in `## What it is for`, at version 8 with its change-log row. The section names files and is not empty.)
  - `answered-from-the-record` → **pass** (the answer is the human's own reply, quoted in `## Answer`; every derived decision cites either that reply or a prior answer by ID, and the AC1 amendment cites the two test assertions it resolves against)
  - `escalation-is-justified` → **skipped** (no question was re-addressed to the human; the one escalation on this item was `plan`'s and it has been answered)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item BUG-0001 --uncommitted` → exit 0. Every claim written into `docs/product/vision.md` is a cited fact, not a quantified one: the paragraph makes no *every*/*all*/*no*/*only* claim over a family, and each sentence carries a citation that resolves — `[src: WI-0002/Q-001]`, `[src: WI-0003/Q-003]`, `[src: WI-0005/Q-006]` and `[src: BUG-0001/Q-001]`, all question files in this workspace. The two command names it uses, `envel entries` and `envel summary`, are the ones `Q-001` itself names.)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0; neither `## Engagement state` section was opened for editing, and the new paragraph sits in `## What it is for`)
  - `cross-answer-consistency` → **pass** (`lint-answers --item BUG-0001` → exit 0; the `## Cross-answer check` names seven prior answers with a verdict each)
  - `workspace-valid` → **fail** (`validate-workspace .` → exit 0; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'BUG-0001:awaiting-answer->ready+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-11T11:01:53Z records `resume-to: ready`; this execution moves `awaiting-answer` → `ready`)
  - `a-deferral-is-not-an-answer` → **skipped** (the reply is a decision, not a deferral: it names one of the four options, refuses the other three by letter and gives a reason for each)
- **Artifacts:**
  - `tracker/items/BUG-0001/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-09-11T11:07:09Z`, with `## Cross-answer check` and `## Consequences` written
  - `tracker/items/BUG-0001/item.md` — `## Expected behaviour` rewritten to carry the decided
    remedy and to put the entry lines out of scope; AC1 amended; AC2 extended to say what the
    `left` column prints; AC3 amended; AC6 appended; `## Notes` rewritten to record the three
    refused options and that neither `WI-0003` AC3 nor `WI-0006` AC9 is amended
  - `docs/product/vision.md` — v7 → v8, one paragraph added under `## What it is for`, change-log
    row added
  - commit of the workspace files this execution wrote
- **Status:** `awaiting-answer` → `ready`
- **Result:** The stakeholder chose option C. A backdated spend is still recorded, and a month that
  closes short says so in words rather than printing a minus, on the closing line of
  `envel entries` and in the `left` column of an `envel summary` row. `BUG-0001` returns to `ready`
  with the remedy settled and the design of it still open for `plan`.

## 2026-09-11T11:19:09Z — plan v0.6.3 — architect

- **Item:** BUG-0001
- **Trigger:** `ready`, dispatched by `next` as the only runnable item — the six work items are
  `done` and `EP-001` at `open` has no owner.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — AC1–AC6 as amended by `answer-questions` this turn
  - `tracker/items/BUG-0001/history.md`, `journal.md`, `questions/Q-001.md`
  - no `artifacts/refinement-qa.md` exists: this bug was filed at `ready` by `review-close` at
    `EP-001`'s DE3 walk and never passed through `refine`
  - `docs/architecture/overview.md` v9 — all six sections
  - `docs/product/vision.md` v8 — `## What it is for`, `## What it deliberately is not`,
    `## Engagement state`
  - `docs/architecture/adr/` — all eleven: `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`,
    `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008`, `ADR-0009`, `ADR-0010`, `ADR-0011`. Five bind
    this change and are listed under `## Binding ADRs`; the other six were read and do not, which
    is said there too rather than left as silence
  - `tracker/project.yaml` — trunk `main`, both commands already filled in
  - `envel/summary.py` in full, `envel/money.py` in full, `tests/test_summary.py` and
    `tests/test_entries.py` at the assertions `BUG-0001` AC5 freezes
  - `tracker/items/WI-0003/item.md` AC2, AC3, AC11; `tracker/items/WI-0006/item.md` AC9, AC10
- **Decisions:**
  - **Where the wording goes — `ADR-0012`, option C.** Route: decided, with an ADR. Two helpers in
    `envel/summary.py`, `balance_line()` and `left_column()`, called from the three places that
    print a bounded balance. Rejected A (render it in `envel/money.py`, so the rule holds
    tool-wide) because it would reword transaction figures and break two assertions `BUG-0001` AC5
    freezes. Rejected B (clamp the balance to `0.00`) because it fails AC6, which is the
    stakeholder's own condition that the line still add up.
  - **No sum changes.** Route: from the documents — `ADR-0008` makes `WI-0003` AC3's reconciliation
    a property of the arithmetic, so a clamp would put code between the two numbers. `figures()`,
    `bounded_balance()`, `balance_before()` and `balance_through()` keep returning signed cents.
  - **Transaction figures keep their signs** — a spend's own line, the side a move left, and the
    summary's `moved` column. Route: from the record. The entry line carrying `-250.00` was printed
    verbatim in `Q-001`'s context and the option the stakeholder chose left it alone; `moved -20.00`
    is delivered behaviour for an envelope that only gave money away, and `tests/test_summary.py`
    asserts the signed figure at line 149. `ADR-0012` names the distinction — a figure answering
    *how much does this hold* is worded, a figure answering *how much moved and which way* is
    signed — because nothing in the project had had to state it before.
  - **The summary's short row reads `short 250.00`.** Route: assumption, recorded under
    `## Assumptions` with its reversal cost (one branch of `left_column()` and two assertions).
    The stakeholder was shown *"the summary's last column showing the same thing"* without the
    exact wording, so this is ours and is **not** under delegation — no answer of theirs licenses a
    category here.
  - **The opening line words the negative case as `was … short at the start of`.** Route:
    assumption, by symmetry with the closing line they did approve. Same reversal cost, also not
    under delegation.
  - **New tests are appended to the two existing modules** rather than put in a new file, because
    AC5's evidence is `git diff 127664a -- tests/` showing additions only in those files. Route:
    assumption, recorded.
  - **`tracker/project.yaml` needed no change**: `test` and `lint` were already real commands and
    both were run this execution.
  - **`docs/architecture/overview.md` `## What is not decided yet` repaired here, to v10.** That
    section is `plan`'s and its sentence naming `WI-0005` as the last design taken is false the
    moment `ADR-0012` exists. It is carried as a row of the invalidation set with disposition
    `to-update` so the set still names every path this execution touched under `docs/`.
- **Cross-answer check:** this execution relied on one human answer, `BUG-0001/Q-001`, which
  `answer-questions` consumed earlier this turn and checked against seven prior answers there. It
  is relied on here, not recorded anew, so no second check is owed and none was performed —
  `lint-answers --uncommitted` → exit 0 over the whole workspace confirms nothing this execution
  wrote reinterprets an answer. No ADR written here reconciles two of the stakeholder's own
  statements: the one genuine tension, between *"I won't use a report whose rows don't add up"* and
  *"no negative envelopes"*, was settled by them at `Q-001` and `ADR-0012` quotes that settlement
  rather than making it.
- **Questions raised:** none. Everything this design forced was answerable from `Q-001`, from the
  standing ADRs, or by a reversible assumption; nothing here is irreversible and nothing depends on
  intent no document records.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 299 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 -m envel new/add/move/spend/summary/entries` against `ENVEL_FILE=/tmp/planprobe/store.json`
    → reproduced both surfaces and confirmed `moved -20.00` is ordinary current-month output
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item BUG-0001` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0 (three
    `claim.unsourced` errors on the first run of `ADR-0012`, all three repaired in place)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after this entry is written
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0. Before this entry existed it
    reported two `doc.changelog.no-execution` errors, one per document this execution versioned:
    the change-log row names a timestamp inside an execution whose journal entry the transition has
    not yet written. The gate runs before the entry, so the two are unavoidably reported and are
    cured by the same command that reports them.)
  - `every-criterion-is-addressed` → **pass** (`## Acceptance criteria mapping` has a row for each
    of AC1–AC6, each naming the step that satisfies it and a specific demonstration — a literal
    expected line, a named `git diff`, or the figure a clamp would print instead. AC3 maps to *no*
    step, deliberately: its demonstration is that the write path is absent from the diff.)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` carries
    `test: python3 -m unittest discover -s tests -t .` and
    `lint: python3 -m compileall -q envel tests`; both were run this execution, exit 0 and exit 0.
    Neither is null and neither was changed.)
  - `decisions-recorded` → **pass** (`## Decisions and ADRs` lists four decisions, all four in
    `ADR-0012`; `## Assumptions` lists three, each with what reversing it costs and each stating
    that it is not under delegation)
  - `plan-is-executable-without-you` → **pass** (advisory. Each of the eight steps names the file
    and the lines it touches and what is true afterwards; steps 1 and 3 give the branch conditions
    and the literal output strings, so no step requires a decision the plan does not make. Step 8
    hands the invalidation set to `implement`, which is that skill's own contract rather than an
    instruction beyond it.)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule
    documents-at-risk-are-enumerated --item BUG-0001` → exit 0: 12 invalidation rows, 0 deliverable
    documents, 10 binding ADR mentions. The set was assembled by opening `docs/product/vision.md`,
    `docs/architecture/overview.md` and the eleven ADRs, not from recollection. Two rows are
    `engagement-state` and disposed `owned-by-ending`; one is `to-update` and discharged by this
    execution; the other nine are open for `implement`. `## Deliverable documents` is `none` and
    says why — no criterion of this bug has a document as its subject.)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` → exit 0; 34 consumed human
    answers and 2 delegations checked across the workspace)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` → exit 0)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` — created: problem, approach, eight steps, the AC
    mapping, three assumptions, the decisions, a twelve-row invalidation set, deliverable documents,
    binding ADRs, scaffolding `none`, four risks and six out-of-scope items
  - `docs/architecture/adr/ADR-0012-a-shortfall-is-said-in-words.md` — created at v1
  - `docs/architecture/overview.md` — v9 → v10, `## What is not decided yet` repaired, change-log
    row added
  - commit of the workspace files this execution wrote
- **Status:** `ready` → `planned`
- **Result:** The shortfall is rendered, not computed: two helpers in `envel/summary.py` word a
  negative balance — `groceries was 250.00 short at the end of 2026-08` and a summary column
  reading `short 250.00` — while every sum, every stored figure and every transaction sign stays
  exactly as it is. `BUG-0001` is `planned` and the change is four small edits and two test classes.

## 2026-09-11T11:20:27Z — implement v0.6.1 — developer

- **Item:** BUG-0001
- **Trigger:** `planned`, dispatched by `next`; `artifacts/plan.md` exists and carries its
  invalidation set, its deliverable documents and its binding ADRs.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — AC1–AC6 as amended when `Q-001` was consumed
  - `tracker/items/BUG-0001/artifacts/plan.md` — eight steps, the AC mapping, three assumptions,
    twelve invalidation rows, `none` deliverable documents, five binding ADRs
  - `tracker/items/BUG-0001/history.md` and `journal.md` — no send-back; this is a first run
  - `tracker/items/BUG-0001/questions/Q-001.md` — `answered`, consumed by `answer-questions` at
    2026-09-11T11:10:49Z and already propagated into `item.md` and `docs/product/vision.md` v8
  - `tracker/project.yaml` — `test` and `lint` both set and non-null
  - `envel/summary.py`, `envel/money.py`, `tests/test_summary.py`, `tests/test_entries.py`
  - `docs/architecture/adr/ADR-0012-a-shortfall-is-said-in-words.md`
- **Decisions:** none yet. The branch `wi/BUG-0001` was created from `main` at `51a0a62`, which is
  the commit carrying the plan and `ADR-0012`; no code has been written.
- **Cross-answer check:** none — this execution has edited nothing yet, in `docs/` or anywhere.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → exit 0
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (no test is written yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range on this branch is empty; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (advisory; there is no diff yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/BUG-0001`, created from `main` at `51a0a62`; no commit on it yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation has started. The branch exists and the plan has been read; nothing is
  built.

## 2026-09-11T11:26:57Z — implement v0.6.1 — developer

- **Item:** BUG-0001
- **Trigger:** `in-progress`, continuing this execution's own opening transition at 11:20:27Z.
- **Inputs read:**
  - `tracker/items/BUG-0001/artifacts/plan.md` — the eight steps, worked in order
  - `tracker/items/BUG-0001/item.md` — AC1–AC6
  - `docs/architecture/adr/ADR-0012-a-shortfall-is-said-in-words.md` — the five numbered decisions
  - `docs/architecture/adr/` — `ADR-0001`, `ADR-0008`, `ADR-0009`, `ADR-0011` reopened at the
    sentences the invalidation set names
  - `docs/architecture/overview.md` v10 and `docs/product/vision.md` v8 — the five rows of the set
  - `envel/summary.py`, `envel/money.py` — the code changed and the code it calls
  - `tests/test_summary.py`, `tests/test_entries.py` — the builders, `fields()` and
    `entry_lines()`, and the assertions `BUG-0001` AC5 freezes
- **Decisions:**
  - **`row()` now formats its first three columns with three explicit `money.format_amount`
    calls.** Inside the plan's latitude: the existing line produced all four with a starred
    generator over `figures()`, which cannot be mixed with a fifth argument of a different shape.
    Same three strings, same function, different spelling — recorded as a deviation.
  - **The no-negative assertion is word-wise rather than line-wise.** The plan asked for *"no line
    matches `-\d`"*, which fails on the date: `2026-08` contains `-0`. Asserting that no
    whitespace-delimited word begins with a minus and a digit is the same claim about amounts
    without being a claim about hyphens. One `import re` added.
  - **The new tests are written against `summarise()` and `list_entries()`, not against the two
    helpers.** The plan's fourth risk names why: a test against the helpers would fail at
    `127664a` with an `AttributeError`, which is a weak demonstration of AC4. Against the entry
    points they fail on behaviour — 6 of 11 failing with the change stashed.
  - **Two tests were written for behaviour that must *not* change** —
    `test_the_entry_line_still_carries_its_sign` and `test_the_moved_column_keeps_its_sign`. They
    map to no acceptance criterion and are not scope: they are the executable form of `ADR-0012`
    §Decision 4, which is the boundary this fix could most easily overrun.
  - **Nothing was escalated.** No decision arose that the plan and `ADR-0012` did not already
    make.
- **Cross-answer check:** none. This execution edited no sentence in `docs/` at all — the branch's
  diff under `docs/` is empty — so no claim sourced to a stakeholder answer was touched, and the
  question of whether an edit was an ordinary repair does not arise. `lint-answers --changed-since
  main` → exit 0.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 310 tests, OK (run after the last
    change, on the branch head)
  - `python3 -m compileall -q envel tests` → exit 0
  - `git stash push envel/summary.py`; `python3 -m unittest tests.test_entries.AMonthThatClosedShort tests.test_summary.AMonthThatClosedShort`
    → **FAILED (failures=6)** of 11; `git stash pop`; same command → **OK**. This is AC4's evidence
  - `git diff 127664a --stat -- tests/` → 2 files changed, 124 insertions(+), 0 deletions;
    `git diff 127664a -- tests/ | grep -c "^-[^-]"` → `0`. This is AC5's evidence
  - the bug's steps 1–7 at the command line against `ENVEL_FILE=/tmp/bug1/store.json` → step 4
    exit 0, `envel list` → `groceries  50.00`, `envel entries groceries --month 2026-08` →
    `groceries was 250.00 short at the end of 2026-08`, `envel summary 2026-08` →
    `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`
  - `grep -rn "format_amount" envel/ --include=*.py` → 35 hits;
    `grep -rn "parse_amount\|:.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → 6 hits;
    `grep -n "print\|sys\.exit\|import sys" envel/summary.py` → 4 hits, all prose. These are the
    three enumerations the quantified rows of the invalidation set owe
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents BUG-0001` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item BUG-0001 --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 310 tests, OK, run on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md` `## Acceptance criteria evidence` names a test function for AC1, AC2, AC4 and AC6 and an exact command with its output for AC3 and AC5. AC3 is the one with no test of its own and it is not demonstrated by reading code: its evidence is `git diff main...wi/BUG-0001 --name-only` showing the write path absent, plus step 4's exit code and streams. AC4's evidence is the stash-and-rerun, which is what makes the other tests' failure against `127664a` a fact rather than a claim.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs BUG-0001 wi/BUG-0001` → exit 0; all 2 commits on `main..wi/BUG-0001` name the item)
  - `no-unplanned-scope` → **pass** (advisory. `git diff main...wi/BUG-0001 --name-only` → `envel/summary.py`, `tests/test_entries.py`, `tests/test_summary.py` and two files under `tracker/`. Every hunk traces to a plan step: two functions added (steps 1 and 3), four call sites changed (steps 2 and 4), two test classes (steps 5 and 6). The two must-not-change tests trace to `ADR-0012` §Decision 4 rather than to an AC, which is stated in the report.)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0. The window printed *0 paths differ from main under docs*, which here is the true state and not a blind window: this execution deliberately wrote no document, and `document-writes-are-declared` checked the same emptiness from the other direction.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents BUG-0001` → exit 0. Scope printed: *6 documents in 6 paths — 0 paths differ from main under docs, plus 6 documents named by BUG-0001's plan*; citations checked over every markdown file in the workspace. The window is non-empty because the plan named its six documents, which is exactly the case `--plan-documents` exists for.)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item BUG-0001 --changed-since main` → exit 0; 0 documents written under `docs/` on this branch, 6 named by the plan. All twelve invalidation rows carry a disposition: nine `verified-still-true` with their audits in `impl-report.md` `## Documents`, two `owned-by-ending` and untouched, one `to-update` discharged by `plan` on `main`. No row was added, because nothing outside the set appears in the branch's `docs/` diff.)
- **Artifacts:**
  - `envel/summary.py` — `left_column()` and `balance_line()` added; `row()` and `list_entries()`
    call them
  - `tests/test_entries.py` — `AMonthThatClosedShort`, six tests, appended
  - `tests/test_summary.py` — `AMonthThatClosedShort`, five tests, appended
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — created
  - `tracker/items/BUG-0001/artifacts/plan.md` — the `disposition` column only, twelve rows closed
  - branch `wi/BUG-0001`, commits `de57e3e..HEAD`, range `main..wi/BUG-0001` (2 commits)
- **Status:** `in-progress` → `verifying`
- **Result:** A month that closed short now says so — `groceries was 250.00 short at the end of
  2026-08` and a summary column reading `short 250.00` — while every sum, every stored figure and
  every transaction sign is exactly as it was. 310 tests green; the two new classes fail 6 of 11
  against the code at `127664a` and pass against this branch.

## 2026-09-11T11:42:17Z — verify v0.5.1 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable candidate on the board — `EP-001` has a null owner at `open` and `engagement-state` reported it `active`, and `WI-0001`..`WI-0006` are all `done`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the six criteria, read first and before the implementation report
  - `tracker/items/BUG-0001/history.md` — the six rows, including `plan`'s forced `workspace-valid`
  - `tracker/items/BUG-0001/artifacts/plan.md` — the eight steps, the AC mapping, the three assumptions, the nine binding ADRs its section names and the twelve-row invalidation set
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — read **after** the criteria and after the evidence was gathered; cited nowhere as evidence
  - `tracker/items/BUG-0001/questions/Q-001.md` — the stakeholder's answer, for what wording they actually approved
  - the code at branch `wi/BUG-0001` head, commit `df2cf4d4e0c48693a996935e68119618cff801a2`, and `envel/summary.py` at `127664a` for comparison
  - `docs/architecture/adr/` — all nine ADRs the plan's section names, in full, for their `## Decision` clauses
  - `docs/product/vision.md`, `docs/architecture/overview.md` and the four ADRs of the invalidation set — the sentences behind the nine `verified-still-true` dispositions
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0005/item.md`, `WI-0006/item.md` — the five criteria AC5 and AC6 take as their subject
  - `tracker/project.yaml` — the two gate commands
- **Decisions:**
  - **Pass, all six criteria, none ambiguous and none substituted.** Every verdict rests on a command run against the branch head, and the item goes to `in-review`.
  - **The one observation found is a finding, not a defect and not a bug item.** `WI-0002` AC5 says *"The listing never shows a negative amount for any envelope"*, and `envel entries` — a listing — shows `-250.00` on an entry line, as a summary row shows `moved -100.00`. Classified as a finding on three grounds, recorded in `verify-report.md` `## Defects found`: it is not this change's doing (entry-line signs predate the branch and are asserted by tests that do too), `WI-0002` AC5's subject is `envel list` and `envel entries` did not exist when it was written, and the stakeholder was shown the entry line verbatim at `Q-001` and chose the option that left it alone. The send-back/bug test both answer no: no criterion of `BUG-0001` says the behaviour should differ, and no other item's delivered criteria are broken. **No question was filed**, because re-asking would reopen a decision `Q-001` settled. What the ending should weigh is narrower and is written down for it: `EP-001`'s success measure *"No envelope ever shows a negative amount"* does not carry `ADR-0012`'s worded-balance/signed-transaction distinction, and whoever closes the epic should say so rather than let the measure read as unqualified.
  - **The non-intersection of AC5's covered criteria is waived by name** — `WI-0002` AC5 and `WI-0005` AC9 — rather than covered by a new test. Stated in those words in the report: nothing executable exercises either criterion together with the new worded-shortfall behaviour. The waiver is structural, not a judgement that the happy path looked convincing: the two criteria's figure is `envelopes.balance` and the new behaviour's is `summary.bounded_balance`, different functions in different modules, and the module holding the refusals is absent from the branch's diff — so no combining test could fail for a reason connected to this change. I exercised the intersection myself at the command line in `/tmp/vfy6` instead, so the gap is examined rather than unnoticed.
  - **I wrote no test and repaired no document.** Step 3a offers adding a covering case; I declined it here because a verifier who writes the covering test and then reports the criterion covered by it has weakened the only thing this stage sells. Nothing under `docs/` was edited by this execution.
  - **The `abs(moved)` mutation was re-run after its first result was discarded.** The first run came back green, which would have been a finding about an insensitive test; with the edit confirmed on disk by `grep` the guard test fails. The first run is recorded void in the report — I cannot show the edit was in place when those tests ran — and every mutation was grep-confirmed before its run thereafter.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 310 tests`, `OK` (run twice: at the start, and after every mutation was reverted)
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `8 item(s), 14 document(s)`, `0 errors, 0 warnings` (final run; an earlier run caught one `claim.citation.outside-the-record` on my own `.claude/…/dor-dod.md` citation, rewritten to the `[src: toolkit: …]` form)
  - the bug's steps 1–4 in `/tmp/vfy1`, then `python3 -m envel entries groceries --month 2026-08` → exit 0, `groceries held 0.00 at the start of 2026-08` / `2  2026-08-14  spend  groceries  -250.00  august shop` / `groceries was 250.00 short at the end of 2026-08`
  - step 4 with the streams split, `>s4.out 2>s4.err` → exit 0, stdout `spent 250.00 from groceries, which now holds 50.00`, stderr 0 bytes; `python3 -m envel list` → exit 0, `groceries  50.00`
  - `python3 -m envel summary 2026-08` before the step-7 probe → exit 0, `no envelopes existed in 2026-08`; after it → exit 0, `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`
  - the two balance lines piped through a `re.match(r'^-\d', word)` filter → `negative-looking words: []` for each
  - `summary.figures` / `balance_before` / `balance_through` read off `/tmp/vfy1` and `/tmp/vfy5` → `left=-25000` and `left=-10001`, and the `ADR-0008` identity `left − (in − spent + moved) == balance_before` true in both months
  - `/tmp/vfy4`: `python3 -m envel move source target 100.00 --on 2026-08-05`, `python3 -m envel spend target 100.00 … --on 2026-08-20` → the exact-zero boundary, `target holds 0.00 at the end of 2026-08` and `left 0.00`, not `short 0.00`
  - `/tmp/vfy5`: a `100.01` backdated spend → `g was 100.01 short at the end of 2026-08`, `g was 100.01 short at the start of 2026-09`, `short 100.01`; `python3 -m envel entries g --month 2026-07` → exit 0, unchanged wording
  - `/tmp/vfy6`: `python3 -m envel spend groceries 999.00 "too much"` → exit 1; `python3 -m envel fix 1 --amount 10.00` → exit 1; `python3 -m envel remove 1` → exit 1; `python3 -m envel list` → `groceries  50.00` after each
  - `git show 127664a:envel/summary.py > envel/summary.py`; `python3 -m unittest -v tests.test_entries.AMonthThatClosedShort tests.test_summary.AMonthThatClosedShort` → `FAILED (failures=6)` of 11, the AC1 and AC2 tests among them; file restored → `OK`
  - three further mutations, each grep-confirmed on disk first: `max(0, left)` in `figures()` → `test_the_arithmetic_was_not_clamped` FAILS; `max(0, sum(…))` in `bounded_balance()` → 3 of 6 FAIL; `abs(moved)` in `row()` → `test_the_moved_column_keeps_its_sign` FAILS; `abs(entry["cents"])` in `entry_line()` → 6 FAIL in `tests.test_entries`
  - `git status --porcelain` after every revert → empty
  - `git diff 127664a --stat -- tests/` → `2 files changed, 124 insertions(+)`; `… | grep -c "^-[^-]"` → `0`; `git diff 127664a --name-only -- tests/` → only `test_entries.py` and `test_summary.py`
  - `git diff 127664a --stat -- envel/` → `envel/summary.py | 62` and nothing else; `git diff main...wi/BUG-0001 --name-only -- docs/` → empty
  - `grep -rn "parse_amount\|:\.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → `money.py:20`, `money.py:42` and four `parse_amount` calls in `cli.py`; `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → no hit
  - `git show 51a0a62 -- docs/architecture/overview.md` → the v10 change-log row and the `## What is not decided yet` rewrite only; no `## Engagement state` line in the diff
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item BUG-0001` → exit 1 at first (`9 binding ADR(s), 5 conformance row(s)`), then exit 0 after four `not-engaged` rows were added
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item BUG-0001` → exit 1 at first (four rows labelled by ADR ID rather than by path), then exit 0, `12 entr(y/ies) against 12 row(s)`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 310 tests`, `OK`, against commit `df2cf4d` and again after the last mutation was reverted)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `8 item(s), 14 document(s)`, `0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (six rows in `## Criteria`, each naming the command this execution ran and quoting its real output; `impl-report.md` is cited as evidence nowhere)
  - `negative-cases-exercised` → **pass** (nine conditions triggered and quoted in `## Negative and boundary cases exercised`, including the `cents < 0` branch boundary from both sides: exactly `0.00` at a past month end takes the unworded path, one cent below it is worded)
  - `a-criterion-about-criteria-is-read` → **pass** (AC5 and AC6 read as such: five covered criteria named by ID — `WI-0002` AC5, `WI-0005` AC9, `WI-0002` AC6 with `WI-0005` AC10, `WI-0003` AC3, `WI-0006` AC9 — each with a verdict read from its text, non-intersection stated in those words, covering case waived by name with a structural reason)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item BUG-0001` exit 0; nine rows, five `conforms` each quoting a clause of the ADR's `## Decision` with the file and line that satisfies it, four `not-engaged` with the reason)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item BUG-0001` exit 0; twelve rows, the nine `verified-still-true` reopened against the branch head with enumerations and falsifiers for the four quantified ones, the two `owned-by-ending` untouched, the one `to-update` confirmed discharged by `plan` at `version: 10` with its change-log row)
  - `tests-would-fail-without-the-change` → **pass** (advisory; four mutations in `## Test sensitivity check`, each grep-confirmed on disk before its run, each failing the tests that claim the behaviour. No test passes against code with its own behaviour removed)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — created, 238 lines
  - `tracker/items/BUG-0001/item.md` — AC1–AC6 ticked `- [x]`, six of six, none `- [~]`
  - no bug item filed; no question filed; no file under `docs/` and no file under `envel/` or `tests/` written by this execution
  - commit: `tracker: the verification report and the six ticked criteria (refs BUG-0001)`
- **Status:** `verifying` → `in-review`
- **Result:** `BUG-0001` passes verification against commit `df2cf4d`. The worded shortfall is delivered at both surfaces, the arithmetic behind it is unclamped and still reconciles — checked by introducing the clamp and watching the criterion's own test fail — and the three older refusals that guard the current balance were triggered rather than read about, in a store whose past month had closed short. One finding is recorded for the epic's ending: `EP-001`'s success measure is worded without the distinction `ADR-0012` draws, and a minus still appears on an entry line and in the `moved` column by the stakeholder's own decision.

## 2026-09-11T11:54:26Z — review-close v0.14.1 — reviewer

- **Item:** BUG-0001
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable candidate — `EP-001` has a null owner at `open` and `engagement-state` reported it `active` with `BUG-0001` still in flight.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md`, `history.md` (7 rows), `journal.md` (509 lines, 7 entries, read in full), `plan.md`, `impl-report.md`, `verify-report.md`, `questions/Q-001.md`
  - the diff `main...wi/BUG-0001` — `main` at `51a0a62`, head at `d710459` — hunk by hunk, including both appended test classes
  - `docs/architecture/adr/` — the nine ADRs the plan's section names, plus `ADR-0004`, `ADR-0005` and `ADR-0006` which it does not, for D13
  - `docs/product/vision.md` and `docs/architecture/overview.md` — the sentences behind the invalidation set's dispositions, re-audited rather than accepted
  - **every `envel/*.py:<line>` citation in `docs/`, all 35, resolved against the branch head** — the sweep `WI-0005/Q-009` performed for `envel/cli.py`, repeated for the module this item changed
  - `tracker/items/WI-0005/questions/Q-009.md` in full — the settled policy for a stale `path:line` citation, which governs this review's one finding
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0005/item.md`, `WI-0006/item.md` — the criteria `verify` read under AC5 and AC6
  - `tracker/project.yaml`; `tests/*.py` directly, to settle where the new test class was appended
- **Decisions:**
  - **Accepted and closed as `delivered`.** Every code hunk maps to a plan step and every plan step to a criterion; the one declared deviation — three explicit `money.format_amount` calls in `row()` instead of the starred generator — is a *how*, not a *what*, and the whole-row assertions hold it. No unrequested scope, no duplicated rule, no swallowed error.
  - **F1, the one finding that matters, accepted as a gap and made dispatchable rather than sent back.** `ADR-0012` `## Consequences` cites `[src: envel/summary.py:173]` for *"the same filtered sum bounded by a month"*. At `main` line 173 is `def bounded_balance(...)`; on the branch head it is `if "description" in entry:`, inside `entry_line()` — the function rendering the **signed transaction figure**, which is the one figure `ADR-0012` Decision 4 exists to distinguish from a balance. So the citation resolves and does not support, and `validate-workspace` and `lint-claims` both pass because the line exists. Not a send-back: the **assertion is true** (both surfaces are that sum and neither was touched — `verify` measured the identity), no criterion of this item is about it, and the remedy is not a decision anyone needs to take because `WI-0005/Q-009` settled the policy for this exact shape under `spec/doc-header.md` §4b. `review-close` may not make the edit — its `docs/` licence covers a correction inside this item's invalidation set and `ADR-0012` is not in it — so it is filed as `Q-002` to `answer-questions`, non-blocking, and disposed `question-filed:BUG-0001/Q-002`. Sending the item back would re-open a branch and re-run `implement` and `verify` to move one number in a document.
  - **D7's closing question is answered yes, and the set could not have named it.** A set lists documents a change could make false; a document the item's own `plan` writes *from* that change is not one. That is `Q-009`'s diagnosis verbatim, and its prediction — *"Every later item whose plan cites a line its own implementation then moves will land in the same place"* — has now come true on the next item. I did **not** add a row to the set: `Q-009` measured that doing so after `verify` has run fails `lint-documents --rule invalidation-set-is-disposed`, because the set is checked against a verification report a closing item cannot rewrite.
  - **F2 accepted with nothing owed, and the reason is the path, not the size.** `tests/test_summary.py` now defines `AMonthThatClosedShort` at line 349, below the `__main__` guard at 345, so `PYTHONPATH=. python3 tests/test_summary.py` reports `OK` over **27** of the module's **32** tests — the five hidden ones including AC2's own and AC6's clamp test. Disposed `no-owner` because direct execution of a test module is not a supported path here and fails at `ModuleNotFoundError` for every module, the guard being vestigial in all three that have one, while the single declared `commands.test` sees all 32. Recorded in `review.md` for whoever ever makes that path work. It was avoidable: inserting the class above the guard would not have breached AC5.
  - **No bug item filed.** Neither finding is behaviour delivered by another item, and neither is a failure of this item's criteria. `verify`'s observation about `WI-0002` AC5's wording I re-read and agree with its classification: the stakeholder settled the entry line at `Q-001` with it printed in front of them, so re-asking would reopen a decision.
  - **One thing carried forward to the ending rather than resolved here:** `EP-001`'s success measure *"No envelope ever shows a negative amount"* is unqualified while `ADR-0012` draws a distinction it does not — a balance is worded, a transaction figure keeps its sign — and `moved -100.00` and a spend's `-250.00` are still printed. Nothing is wrong; the measure's wording is what the ending must state in those terms.
  - **Merge order followed as written:** trial-merge into a `--detach` worktree, suite on the merge result, worktree discarded, trunk confirmed unmoved, item closed while the branch is still unmerged, then the real merge and `record-merge`.
- **Cross-answer check:** none — this execution consumed no human answer. `Q-001` was consumed by `answer-questions` at `11:10:49Z` and is already propagated; `Q-002`, filed here, is addressed to the architect and is unanswered. `lint-answers --context bug --changed-since main` exits 0 over 34 consumed human answers and 2 delegations spent, none of them this execution's.
- **Questions raised:** BUG-0001/Q-002 (non-blocking, addressed to architect)
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` on branch head `d710459` → exit 0, `Ran 310 tests`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0, *"verified at df2cf4d4; wi/BUG-0001 has moved to d710459e but only the record changed (5 file(s) under tracker/ or docs/)"*
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 4 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `git worktree add --detach /tmp/trial-bug1 main` → detached at `51a0a62`; `git -C /tmp/trial-bug1 merge --no-ff wi/BUG-0001` → clean, `10 files changed, 760 insertions(+), 27 deletions(-)`, trial sha `50ff2a7`
  - inside the trial worktree: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 310 tests`, `OK`; `python3 -m compileall -q envel tests` → exit 0
  - `git worktree remove --force /tmp/trial-bug1`, then `git rev-parse main` → `51a0a62bc29ae7b5fd1fe5c765334d737edb0c13`, byte-identical to the sha taken before the trial
  - `grep -rno "envel/[a-z_]*\.py:[0-9]*" docs/` piped through `sed -n "<n>p"` on each cited file → 35 citations resolved one at a time; exactly one stale, `ADR-0012:137`
  - `git show 51a0a62:envel/summary.py | sed -n 173p` → `def bounded_balance(store, name, within):`; `sed -n 173p envel/summary.py` → `    if "description" in entry:`; `sed -n 196p envel/summary.py` → `def bounded_balance(store, name, within):`; `sed -n 68p envel/summary.py` → `    left = sum(...)`, unmoved and still supporting
  - `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → no hit; `grep -rn "parse_amount\|:\.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → nothing outside `money.py`
  - `python3 -m envel entries g --month 2026-08` on a `100.01` shortfall → `g was 100.01 short at the end of 2026-08` — D12's falsifier for the two-decimal claim, chosen over the round magnitude `verify` used
  - `grep -n '__main__' tests/*.py` → guards at `test_dates.py:115`, `test_corrections.py:413` (of 414) and `test_summary.py:345` (of 401); `PYTHONPATH=. python3 tests/test_summary.py` → `Ran 27 tests`, `OK`; `python3 -m unittest tests.test_summary` → `Ran 32 tests`, `OK`
  - `python3 .claude/agile-skills/scripts/lint-claims --context bug --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context bug --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/check-epic-signoff BUG-0001` → exit 0, *"BUG-0001 is a 'bug', not an epic"*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated --item BUG-0001 --context bug` → exit 0, *"NOT APPLICABLE"*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable --item BUG-0001` → exit 1 three times (owner outside the closed vocabulary, then disposition cells carrying trailing prose), then exit 0 at `4 accepted gap(s)`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`
- **Gates:**
  - `definition-of-done` → **pass** (D1–D13 walked one at a time with a result and evidence each, in `review.md` `## Definition of Done`. D7 and D12 pass *with a finding* — the same finding, filed as `Q-002`. No single overall verdict stands in for the table)
  - `engagement-state-is-restated` → **pass** (not applicable — an item close is not an ending, and the sections are the ending's. The rule's own output says `NOT APPLICABLE`; no `## Engagement state` section was read for repair or written, and they belong to `EP-001`'s ending; the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated --item BUG-0001 --context bug --root /home/msi/agile-skills-throwaway/envel-2` exited 0)
  - `accepted-gaps-are-dispatchable` → **pass** (four rows, every one disposed: `question-filed:BUG-0001/Q-002` for F1, and `no-owner` for F2 and for `verify`'s two carried gaps, each row stating why nothing is owed)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness BUG-0001 wi/BUG-0001` exit 0; the comparison was run, not inferred from how the last commit looked — `df2cf4d` verified, `d710459` now, record-only in between)
  - `commits-reference-the-item` → **pass** (`check-commit-refs BUG-0001 wi/BUG-0001` exit 0, all 4 commits on `main..wi/BUG-0001`; run before the merge, while that range is still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (the suite run *inside* the trial worktree at merge sha `50ff2a7`, not on the branch: `Ran 310 tests`, `OK`, exit 0, with `compileall` exit 0 beside it)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `8 item(s), 14 document(s)`, `0 errors, 0 warnings`)
  - `record-is-reconstructible` → **pass** (answered from the record alone. *What and why:* `item.md` and `ADR-0012`, back to the stakeholder's words at `Q-001`. *Which skill decided what:* seven journal entries against seven history rows, each naming its skill and version. *What questions arose and how they resolved:* `Q-001` answered by the human and propagated into `item.md` and `vision.md` v8; `Q-002` filed here and open. *What verification found:* `verify-report.md` — six criteria with commands and output, nine ADR verdicts, twelve invalidation rows, four mutations. The one thing a reader cannot get is the stakeholder's view of two wordings nobody showed them, and that is written down three times as a gap rather than left silent)
  - `claims-are-sourced` → **pass** (`lint-claims --context bug --changed-since main` exit 0. The **scope**, quoted from its own output: *"checked absolute claims: 0 document(s) in 0 path(s) differ from main (51a0a62) under docs; citations: every markdown file in the workspace"*. The claim window is **empty** because this branch wrote no document — correct for this change, and exactly F-066's shape — so the D12 read was done by hand over the set's documents and the 35-citation sweep. The finding is the sweep's, not the gate's, and the gate is recorded as passing over nothing)
  - `cross-answer-consistency` → **pass** (`lint-answers --context bug --changed-since main` exit 0, `34 consumed human answer(s) and 2 delegation(s)`; this execution consumed none, as the cross-answer check records)
  - `epic-sign-off` → **pass** (by subject: `BUG-0001` is a `bug`, not an epic, and the termination gate applies to an engagement's ending only. `check-epic-signoff BUG-0001` says so itself and exits 0; the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/check-epic-signoff BUG-0001 --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'BUG-0001:in-review->done+journal'` exited 0)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/review.md` — created
  - `tracker/items/BUG-0001/questions/Q-002.md` — created, non-blocking, addressed to architect
  - `tracker/items/BUG-0001/item.md` — `outcome: delivered` written by this transition, not edited ahead of it
  - `tracker/board.md` — regenerated
  - no bug item filed; no file under `docs/`, `envel/` or `tests/` written by this execution
  - commit: `tracker: the review, the closed item, and the merge (refs BUG-0001)`; the merge sha is recorded separately by `scripts/record-merge`, not here, because it does not exist yet
- **Status:** `in-review` → `done`
- **Result:** `BUG-0001` is accepted and closes as `delivered`. The worded shortfall is delivered at both surfaces with the arithmetic untouched, six criteria each carry a command, the trial merge is green on the merge result and the trunk did not move. Two gaps accepted, both disposed; the one that matters is a citation in this item's own ADR that now points at the line rendering the very figure that ADR distinguishes a balance from — the second occurrence in two consecutive items of a defect whose policy `WI-0005/Q-009` settled and whose recurrence it predicted in writing, now filed as `Q-002` with a count for the retrospective.

## 2026-09-11T11:58:23Z — answer-questions v0.6.3 — architect

- **Item:** BUG-0001
- **Trigger:** `next` step 3 — `Q-002` was `status: open` and `addressed-to: architect`, which is answerable by definition, so it outranked building the candidate set. The item itself is `done`; this is the gap `review-close` made dispatchable at the close, falling due on the next pass exactly as `accepted-gaps-are-dispatchable` intends.
- **Inputs read:**
  - `tracker/items/BUG-0001/questions/Q-002.md` — the only open question on the item; `Q-001` is `answered`, `answered-by: human`, and already propagated
  - `tracker/items/BUG-0001/item.md`, `history.md` (8 rows, last `in-review → done`), `artifacts/plan.md` (the invalidation set and `## Binding ADRs`), `artifacts/review.md` (F1 and its disposition), `artifacts/verify-report.md` (the identity measurement this answer relies on)
  - **`tracker/items/WI-0005/questions/Q-009.md` in full** — the decided policy for a stale `path:line` citation, its refusal of B and D, what it deliberately left alone, and its prediction that this would recur
  - `docs/architecture/adr/ADR-0012-a-shortfall-is-said-in-words.md` **v1** — the document repaired; `## Decision` read in full to confirm no clause moved
  - `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` **v2** — the shape to mirror: its `## Corrections` table, its v2 change-log row and its header stamps, all written by this skill for `WI-0005/Q-009`
  - `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` **v2** — the fourth occurrence `Q-009` found and repaired under the same policy
  - `.claude/agile-skills/spec/doc-header.md` §4b — the two legal repairs to an accepted ADR and the line between a correction and a supersession
  - `envel/summary.py` at `main` — lines 68, 173 and 196, and `git show 51a0a62:envel/summary.py` line 173 for what the citation meant when written
  - `docs/product/vision.md` **v8** and `docs/architecture/overview.md` **v10** — checked for any sentence this repair touches; neither is affected, and neither was edited
- **Decisions:**
  - **`Q-002` answered: option A on both halves, from the record rather than by deciding.** Route 1 — an existing document. `WI-0005/Q-009` settled the policy for this exact shape and grounded it in `spec/doc-header.md` §4b, so this execution applies a decision rather than taking one. I checked §4b's two conditions against this instance myself rather than inheriting them: the **assertion is unchanged** (both surfaces are that bounded sum and neither was touched — `verify` measured `left − (in − spent + moved) == balance_before` at both bounds on a month that closed short, so this is measured and not inferred), and the **new citation resolves and supports** (`sed -n 196p envel/summary.py` → `def bounded_balance(store, name, within):`). §4b's non-negotiable line is not crossed — no reader has to change code to satisfy the new text — so `ADR-0012` is corrected to v2 and not superseded.
  - **The second half: the two stale tracker citations are left alone**, on `Q-009`'s reasoning that *"an implementation report is a statement about a moment, not a standing claim"*. `tracker/items/WI-0005/item.md:272` and `tracker/items/WI-0006/artifacts/impl-report.md:344` both belong to `done` items, and the claims they support are still true of the tool. Option B was refused for the reason `Q-009` refused it: the cost is not the edits but the precedent that every code change owes a sweep of every closed item's artifacts.
  - **Option C was deliberately not taken, and this answer says so explicitly.** Replacing `path:line` with a symbol citation is the real fix and it is a workspace-wide decision about the record's grammar; settling it from the second instance would be settling it from an anecdote. `Q-009` sent it to the retrospective and that is still the right venue. What I added is the **count**: three reviews in one engagement, and `Q-009`'s written prediction — *"Every later item whose plan cites a line its own implementation then moves will land in the same place"* — has now come true on the very next item. That is in `Q-002` `## Answer` so `retro` finds the two instances and the prediction together rather than one worry.
  - **This instance is sharper than `Q-009`'s and the answer records why.** Line 173 did not merely drift: it came to rest on `if "description" in entry:`, inside `entry_line()`, which renders the signed transaction figure that `## Decision` 4 of this very ADR exists to distinguish from a balance. The citation landed on the one line that contradicts the sentence it was supporting, and no mechanical check can see that — `validate-workspace` and `lint-claims` both exit 0 because the line exists.
  - **I re-ran the whole sweep on `main` after the merge before answering**, as `Q-009`'s execution did and for the same reason: that pass found a fourth occurrence nobody had filed. All 35 `envel/*.py:<line>` citations in `docs/` resolved one at a time; exactly one stale, every other resolving to a line that supports its sentence. Only `envel/summary.py` citations could have newly gone stale, that being the only module in the change's diff. **No fifth occurrence this time.**
  - **No invalidation-set row added, and the reason is measured, not asserted.** Step 6a would normally require one for a document this execution changed. `Q-009` probed exactly that and found it fails `lint-documents --rule invalidation-set-is-disposed`: the set is checked against `verify-report.md`'s disposition table, which a closing item cannot rewrite. Step 6a is for edits made mid-flight on a live branch; this one is on `main` after the merge, with `BUG-0001` at `done`. The fact is already recorded where a reader finds it — `review.md`'s answer to *did this change falsify a document the set does not name* names `ADR-0012` and explains the structural reason the set could not.
  - **No acceptance criterion amended, no scope widened, no bug filed, no item created.** All six criteria are settled and ticked and nothing here reopens one; the tool's output is unchanged by this repair, so there is no delivered behaviour to file a defect against.
  - **No escalation.** None of `spec/question.md` §4's four conditions applies: the record is not silent (it is the opposite — the policy is written down), nothing is irreversible, and nothing contradicts an ADR. Option C *would* need the human, and it is referred to `retro` rather than asked, because nobody is blocked by it.
  - **I estimated a timestamp and the validator caught it.** The first write of this repair stamped `2026-09-11T12:02:17Z`, ahead of the clock, and `validate-workspace` refused it with `doc.changelog.timestamp.future`. I read the clock and rewrote all six occurrences across two files. Recording it because the rule it enforces — a timestamp is read, never estimated — is one this execution broke and the gate is why it did not reach the record.
- **Cross-answer check:** `none — this execution consumed no human answer.` `Q-002` is addressed to the architect and was answered from the record. `Q-001`, the one human answer on this item, was consumed by `answer-questions` at `11:10:49Z` and is untouched here: this repair does not edit `ADR-0012` `## Decision`, which is where the stakeholder's `Q-001` choice is recorded, so no sentence sourced to an answer of theirs is altered. `lint-answers --item BUG-0001` exits 0 over `1 consumed human answer(s) and 0 delegation(s)`.
- **Questions raised:** none
- **Commands:**
  - `grep -rno "envel/[a-z_]*\.py:[0-9]*" docs/` piped through `sed -n "<n>p"` on each cited file → 35 citations resolved one at a time against `main`; exactly one stale, `ADR-0012:137`
  - `git show 51a0a62:envel/summary.py | sed -n 173p` → `def bounded_balance(store, name, within):` — what the citation meant when `plan` wrote it
  - `sed -n 173p envel/summary.py` → `    if "description" in entry:`; `sed -n 196p envel/summary.py` → `def bounded_balance(store, name, within):`; `sed -n 68p envel/summary.py` → `    left = sum(entry["cents"] for entry in mine if entry_month(entry) <= month)`
  - `grep -n "summary.py:196\|summary.py:173" docs/architecture/adr/ADR-0012-*.md` → line 137 now cites `:196`; `:173` survives only inside the `## Change log` and `## Corrections` rows that record the move
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-09-11T11:57:12Z`, the stamp actually used
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item BUG-0001 --uncommitted` → exit 0, `window: 1 uncommitted path(s) under docs`
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, `1 document(s) in the window, compared region by region against HEAD`
  - `python3 .claude/agile-skills/scripts/lint-answers --item BUG-0001` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → `wrote tracker/board.md`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 first, on `doc.changelog.timestamp.future` at `ADR-0012:171` and a stale board; exit 0 after the clock reading and the board regeneration, `8 item(s), 14 document(s)`, `0 errors, 0 warnings`
- **Gates:**
  - `answer-is-propagated` → **pass** (each file named in `## Consequences` opened afterwards and the change confirmed present: `ADR-0012:137` now carries `[src: envel/summary.py:196]`, the header reads `version: 2` / `updated-by: answer-questions` / `updated-for: BUG-0001`, the v2 change-log row and the `provenance` `## Corrections` row both exist, and `Q-002` carries `status: answered` with both stamps. The section names two files and both were changed)
  - `answered-from-the-record` → **pass** (route 1, an existing document: `WI-0005/Q-009`'s decided policy and `spec/doc-header.md` §4b, with §4b's two conditions checked against this instance rather than inherited — the unchanged assertion measured by `verify`, the replacement citation resolved by `sed`. The record was not silent, so no new ADR was written)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human. None of `spec/question.md` §4's four conditions applies; option C, which would need them, is referred to `retro` because nobody is blocked by it, and that is stated in the answer rather than left implicit)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item BUG-0001 --uncommitted` exit 0. The one claim written is a **cited fact** — an absolute about named code — so what it owes is a citation that resolves, and here also one that supports, since supporting-but-resolving is the defect being repaired. `## Consequences` carries that evidence per claim. No quantified sentence was written, which the gate confirms at `0 quantified sentence(s)`)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` exit 0, the one document in the window compared region by region against `HEAD`. `ADR-0012` has no `## Engagement state` section, nothing in this answer is a sentence about the engagement, and no such sentence anywhere was edited, moved into or moved out of one)
  - `cross-answer-consistency` → **pass** (`lint-answers --item BUG-0001` exit 0, `1 consumed human answer(s) and 0 delegation(s)`. The `## Cross-answer check` is written and its honest content is `none` with the reason: this answer consumed no human answer and alters no sentence sourced to one)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `0 errors, 0 warnings` — after it correctly refused an estimated timestamp and a stale board, both of which are recorded above rather than quietly fixed)
  - `item-resumed-correctly` → **skipped** (there is nothing to compare. `Q-002` is `blocking: false`, so it suspended nothing: no history row carries a `resume-to` for it, and `BUG-0001` was `done` before this execution began and is `done` after it. This execution makes no transition, which is this skill's declared behaviour — *on success: no status transition of its own*)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred. `Q-002` was answered outright from the record; neither of step 3a's two moves was needed, and no question on this item carries `status: deferred`)
- **Artifacts:**
  - `docs/architecture/adr/ADR-0012-a-shortfall-is-said-in-words.md` — **v1 → v2**: `## Consequences`' citation repaired `:173 → :196`; header stamps updated; one `## Change log` row; one `## Corrections` row of kind `provenance` in a new append-only section. No `## Decision` clause changed, so every conformance verdict `verify` recorded against this ADR stays true of it
  - `tracker/items/BUG-0001/questions/Q-002.md` — `## Answer`, `## Cross-answer check` and `## Consequences` written; `status: open → answered`; `answered-by: answer-questions`; `answered-at: 2026-09-11T11:57:12Z`
  - `tracker/board.md` — regenerated; the open-questions section is now empty
  - no ADR created, no item created, no bug filed, no acceptance criterion amended, no other document under `docs/` touched
  - commit: `tracker: Q-002 answered, and the ADR-0012 citation it repaired (refs BUG-0001)`
- **Status:** `done` → `done`
- **Result:** `Q-002` is answered and the repair is propagated: `ADR-0012` is at v2 with its `## Consequences` citation pointing at `bounded_balance` again, recorded in an append-only `## Corrections` row that says what moved and why. The policy was `WI-0005/Q-009`'s and this execution applied it rather than re-deciding it; the two stale citations in closed items' artifacts stay as dated records, also on `Q-009`'s reasoning. The real fix — retiring `path:line` for claims about statements that move — is referred to `retro` with a count of three and a prediction that came true, not re-asked here. `BUG-0001` has no open question left and `EP-001` has none anywhere.
