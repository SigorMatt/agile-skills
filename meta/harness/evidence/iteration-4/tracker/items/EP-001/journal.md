# Journal — EP-001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-29T10:48:03Z — intake v0.2.1 — product-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the stakeholder's opening statement in `IDEA.md`; `intake` is not dispatched by status
- **Inputs read:**
  - `IDEA.md` — "A flashcard tool: add cards, review due cards daily, simple spaced repetition. Progress persists."
  - `tracker/project.yaml` (name `recall`, trunk `main`, all three commands null)
  - `tracker/items/` — empty; no existing epic, no overlap, highest allocated IDs are none
  - `docs/product/vision.md` — absent before this execution
  - `SIMULATION-NOTICE.md` — establishes that the stakeholder answers asynchronously in files and cannot be asked in session
- **Decisions:**
  - Split the epic into three items rather than one or five. One item would have bundled storage, an interactive session and a scheduling algorithm behind a single acceptance gate, so a failure anywhere would block everything. Five would have split storage from listing, and review from grading, neither of which delivers anything a user can observe on its own. Three is the smallest set where each item is separately observable: WI-0001 a card that survives a restart, WI-0002 a finite daily session, WI-0003 intervals that stretch.
  - Ordered the items with `depends-on` (WI-0001 → WI-0002 → WI-0003) rather than with `priority`. The stakeholder stated no ordering, and the skill forbids guessing one; this chain is not a preference but a necessity — there is nothing to review before cards persist, and no result to schedule from before a review records one. Priority is therefore uniform `high` across all three, which claims nothing the stakeholder did not say.
  - Wrote every acceptance criterion without naming an interface, a language, a file format or a library. The stakeholder named none, and `no-solution-in-the-problem` would have failed otherwise. Specifically removed from consideration while drafting: naming a CLI, naming JSON or SQLite as the store, and naming SM-2 as the algorithm. Each became a question instead.
  - Wrote an out-of-scope list on the epic although the stakeholder named no exclusions, deriving it from what a reader would assume is included: sync and accounts, media on cards, import/export, statistics, per-card tuning, editing and deleting cards, and reminders. Editing and deleting is the one a reasonable person might dispute, so it is written as an exclusion the stakeholder can overturn by saying so, not as a silent omission.
  - Recorded the four things the opening statement did not say as blocking questions to the human rather than as assumptions. None of them is reversible cheaply: the interface determines the shape of every criterion, the scheduling scheme and the grade granularity determine each other and the stored state, and decks reach into storage, selection and every command. Guessing any of them would have produced criteria that look decidable and encode my preference rather than the stakeholder's intent.
  - Filed them as four files rather than one, per `spec/question.md` (one decision per question), but wrote them as one ask: each `## Context` opens with the same frame and says which of four it is, and `Q-004` says it is the last. The restatement of the idea lives in `Q-001` so the stakeholder can correct the framing before answering the rest.
  - Left `commands.test`, `commands.lint` and `commands.build` null in `project.yaml`. The project has no code and no test runner, so naming one would make the first `tests-pass` gate report a pass for a command nobody can run. `plan` sets them.
- **Questions raised:** `Q-001` (interface), `Q-002` (scheduling scheme), `Q-003` (grade granularity), `Q-004` (decks) — all blocking, all addressed to `human`, all open
- **Commands:**
  - `scripts/workspace-init .` → exit 0, workspace already present
  - `scripts/new-item --id EP-001 --type epic --status open --actor intake` → exit 0
  - `scripts/new-item --id WI-0001|WI-0002|WI-0003 --type work-item --status draft --actor intake` → exit 0 (three invocations)
  - `scripts/journal-entry WI-0001|WI-0002|WI-0003 --skill intake` → exit 0 (three invocations)
  - `scripts/board-gen .` → exit 0
  - `scripts/validate-workspace .` → exit 1 before this transition, with `question.blocking.not-suspended` on EP-001 and `journal.execution.missing` on EP-001; both are what this transition and this entry resolve
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, run by this transition against the state the move produces)
  - `epic-has-success-measures` → **pass** (SM1–SM5 in `item.md`; each names a thing to do and a thing to observe — add then restart, add then check the due list, review twice in a day, compare two next-due dates, open the stored file — none restates the goal)
  - `items-are-separable` (advisory) → **pass** (build order WI-0001 → WI-0002 → WI-0003, each delivering something observable alone; recorded in `depends-on`)
  - `no-solution-in-the-problem` (advisory) → **pass** (no title, story or criterion names a technology; CLI, JSON/SQLite and SM-2 were each considered and removed, and each became a question)
- **Artifacts:**
  - `tracker/items/EP-001/item.md` (new)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (new, open, to `human`)
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` (new)
  - `docs/product/vision.md` (new, v1)
  - `tracker/project.yaml` (description filled in)
  - `tracker/board.md` (regenerated)
- **Status:** `open` → `awaiting-answer`
- **Result:** The idea is now an epic with five checkable success measures and three separable draft items. Four questions the opening sentence could not answer are open with the stakeholder, and the epic is suspended until they come back; nothing can be refined before then, because all four change acceptance criteria.

## 2026-08-29T10:54:21Z — answer-questions v0.3.1 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer`, invoked directly after the stakeholder filled in `## Answer` on all four open questions; `next` would have stopped on them
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — all four answered by the stakeholder, all blocking, all addressed to `human`
  - `tracker/items/EP-001/item.md`, `history.md` (the suspending row carries `resume-to: open`), `journal.md` (intake's entry, for what each question was meant to settle)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — the criteria the answers had to reach
  - `docs/product/vision.md` (v1) — its "What is not yet decided" section named all four questions
  - `docs/architecture/adr/` — empty before this execution; no recorded decision could be contradicted
  - `tracker/project.yaml`; `tracker/items/*/artifacts/` — empty, so there is no `plan.md` or `refinement-qa.md` yet
- **Decisions:**
  - `Q-001` (interface) — answered by the human: a command-line tool. Route: the stakeholder replied to an escalation, so it is recorded as theirs, not derived. Propagated as an interface statement in `vision.md` and as command-shaped phrasing in WI-0001 AC1–AC4 and WI-0002 AC1/AC3, because a criterion that does not say what is operated is not decidable by someone with a terminal.
  - `Q-002` (scheduling scheme) — answered by the human: a fixed ladder, "one day, then three, then a week, then a month", wrong goes back to the start. Their enumeration names **four** rungs where the question's option A offered five (1/3/7/14/30). I took their words literally — the ladder is 1, 3, 7, 30 — rather than padding it with a rung they did not say. Rationale: adding 14 would put a choice in the record as the stakeholder's that they never made, and the rung values are a single constant, so being wrong here is cheap to correct; escalating again would spend a round trip on the cheapest decision in the epic. Recorded as `ADR-0001` with that reasoning and its reversibility, because WI-0003 AC4 needs a document to point at.
  - `Q-002`, second part — "goes back to the start" collided with epic SM4, which said a card answered incorrectly is next due "no later than the day of the review". That cannot hold alongside WI-0002 AC4 (nothing reviewed today is presented again today). Resolved in favour of the bottom rung, one day, so a card missed today returns tomorrow; SM4 amended to say so. This is the only reading under which the epic and both items agree, and it is what "back to the start" means once the start is known.
  - `Q-003` (grade granularity) — answered by the human: right or wrong, no four-point scale. Propagated into WI-0002 AC2 and AC6, into WI-0002's out-of-scope list, and into `ADR-0001`, which records that reversing it is part of the cost of ever adopting SM-2.
  - `Q-004` (decks) — answered by the human: one flat pool. Propagated as a confirmed exclusion on the epic and WI-0001, and as new criteria — WI-0001 AC6 and WI-0002 AC7 — because "no decks" is only checkable if something states that the commands take no deck argument.
  - Amended acceptance criteria on all three child items while they are at `draft`, and one epic success measure. Recorded here explicitly because criteria are frozen after `ready`: WI-0001 AC1–AC4 reworded and AC6 added; WI-0002 AC1, AC2, AC3, AC6 reworded and AC7 added; WI-0003 AC2, AC3, AC4 given the concrete ladder; EP-001 SM4 corrected. Every one of those edits states what the stakeholder asked for in their answer; none was made to accommodate code, of which there is none.
  - Did not file any new work item. All four answers chose the smallest option offered, so none of them widened the scope: nothing is implied that WI-0001..WI-0003 do not already cover.
  - Did not escalate anything. Left deliberately for `refine` rather than asked again now: the exact spelling of the commands, what the reviewer types to reveal an answer and to record right or wrong, and the exact wording AC3 and AC6 check for. Those are refinement questions on items nobody has begun refining, and asking them from here would be asking about work not yet reached.
- **Questions raised:** none
- **Commands:**
  - `scripts/lint-claims docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` → exit 1 (4 unsourced absolutes), then exit 0 after citations added
  - `scripts/lint-claims docs/product/vision.md` → exit 0
  - `scripts/validate-workspace .` → exit 1 before this transition, with `board.stale` and `question.awaiting.none-open` on EP-001; both are what this transition and the board regeneration resolve
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in a `## Consequences` section was opened and checked: `docs/product/vision.md` v2 states the CLI, the flat pool and the 1/3/7/30 ladder; `ADR-0001` exists; `EP-001/item.md` carries the amended SM4, the scope line and two new exclusions; `WI-0001` carries reworded AC1–AC4, new AC6 and the settled decks line; `WI-0002` carries reworded AC1/AC2/AC3/AC6 and new AC7; `WI-0003` carries the concrete ladder in AC2–AC4. No `## Consequences` section is empty and none names an intention rather than a file.
  - `answered-from-the-record` → **pass** — all four answers are the stakeholder's own words, quoted in the artifacts they reached. The one thing they did not settle, the number of rungs, is recorded as a decision in `ADR-0001` with its options rather than presented as theirs.
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human, so no condition from `spec/question.md` §4 had to be stated.
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, run by this transition against the state the move produces)
  - `item-resumed-correctly` → **pass** — the suspending row (`open → awaiting-answer`, actor `intake`) records `resume-to: open`, and this execution returns EP-001 to `open`.
  - `a-deferral-is-not-an-answer` → **not applicable** — none of the four replies defers. Each names a choice from the options offered, in the stakeholder's own words, and each is propagated into artifacts that now contain the decision.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — `status: answered`, `answered-by: human`, `answered-at` stamped, `## Consequences` filled with the files each answer reached
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` (new) — the 1/3/7/30 ladder, the binary result, the wrong-answer reset, and reversibility
  - `docs/product/vision.md` (v1 → v2) — CLI, flat pool, and "How the schedule behaves" in place of "What is not yet decided"
  - `tracker/items/EP-001/item.md` — SM4 amended; scope and out-of-scope extended
  - `tracker/items/WI-0001/item.md` — AC1–AC4 reworded, AC6 added, decks settled, notes rewritten
  - `tracker/items/WI-0002/item.md` — AC1, AC2, AC3, AC6 reworded, AC7 added, notes rewritten
  - `tracker/items/WI-0003/item.md` — AC2, AC3, AC4 given the concrete ladder, notes rewritten
- **Status:** `awaiting-answer` → `open`
- **Result:** All four questions the epic was suspended on are answered by the stakeholder and propagated into the vision, a new ADR, the epic and all three child items; EP-001 returns to `open`. The four unknowns intake could not decide are now decided, so `refine` can start on WI-0001 — what it still owes is the exact command wording, not the shape of the product.

## 2026-08-29T13:14:31Z — review-close v0.5.0 — reviewer

- **Item:** EP-001
- **Trigger:** the epic at `open`, dispatched by `next` step 6 after `engagement-state EP-001`
  reported `at-rest`. Not a review of code: this execution is the "ending an engagement" path, so
  steps 1–9 of the procedure do not apply and step 10 does.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — `## Goal`, `## Why now`, the five success measures, and the
    scope and exclusions
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-004.md` — all four `answered`, the
    stakeholder's own words on the interface, the ladder, the binary result and the flat pool
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — every child, its
    title, its status and its outcome
  - `docs/product/vision.md` (v2) — for the stakeholder's own vocabulary, which the sign-off's
    `## Context` has to be written in rather than the tracker's
  - `tracker/items/WI-0003/artifacts/review.md` — the accepted gap that the sign-off names
  - `.claude/agile-skills/spec/question.md` §2, `kind: sign-off` — the five extra rules
  - the merged code on `main`, run end to end
- **Decisions:**
  - **File the sign-off and suspend the epic; do not close it.** `engagement-state` says
    `at-rest` and no sign-off has ever been filed on EP-001 (its four questions are `intake`'s,
    all answered long before rest). Rest, not closure, is the trigger, and closing here without
    asking is precisely the failure the rule exists for.
  - **`## Question` names all three children by ID** — WI-0001, WI-0002, WI-0003 — each marked
    delivered with one line of what it delivers. All three are `done` / `delivered`; **no bug
    item exists anywhere in the engagement**, which the question states explicitly rather than
    leaving as an absence the stakeholder has to notice.
  - **The three options are real, and B is not padding.** Three exclusions in the record are
    things a person might actually want next and were decided on the stakeholder's behalf rather
    than by them: editing or deleting a card, a command to see or set a schedule, and any form of
    statistics. B names them so that "accept with follow-ups" is a choice they can act on rather
    than a blank.
  - **The one accepted gap is disclosed in the sign-off.** WI-0003's review accepted that a
    hand-edited store containing `1.0` where `1` is expected is read rather than refused. It
    changes no schedule and drops no card, but the stakeholder is told, because a gap they learn
    about after accepting is a gap they did not accept.
  - **The success measures were demonstrated rather than asserted.** SM1–SM5 were run end to end
    against the merged trunk before the question was written, and the transcript is in the
    question, so the stakeholder is answering about the tool rather than about the tickets.
  - **No ending was recorded and no epic Definition of Done was applied.** Both wait on the
    reply; taking an ending now would be deciding the one thing that is theirs to decide.
- **Questions raised:** EP-001/Q-005 (`kind: sign-off`, `addressed-to: human`, `blocking: true`)
- **Commands:**
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → exit 0, "EP-001 **at-rest** —
    every child has stopped, no question is open, no request is open; rest reached at
    2026-08-29T13:12:14Z"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 9 documents,
    0 errors 0 warnings
  - `python3 -m unittest discover -s tests -t .` on `main` after the merge → exit 0, `Ran 87
    tests`, `OK`
  - the SM walkthrough on the merged trunk: `recall add "die Katze" "the cat"` → `Added card 1.`;
    `recall add "Grüße" "greetings"` → `Added card 2.`; `recall review` with `\ny\n\nn\n` →
    both cards shown, `Reviewed 2, right 1.`; a second `recall review` the same day →
    `Nothing is due today.` (SM3); the store file holds card 1 `right`/`interval 1`/due
    2026-08-30 and card 2 `wrong`/`interval 1`/due 2026-08-30 (SM1, SM5); card 1 brought forward
    by hand and answered right again → `interval 3`, due 2026-09-01, strictly later than after
    one right answer, while the wrong card stays at the shortest rung (SM4); a new card being due
    the day it is added is SM2, visible in the first review
  - `git log --oneline -3` on `main` → the merge `d73a284`, and `git rev-parse main` →
    `d73a284712c36bc47e6326a12bc2e44863469187`
- **Gates:**
  - `definition-of-done` → **skipped, deliberately** — the epic Definition of Done
    (`spec/dor-dod.md` §4) is applied when the *ending* is recorded, and this execution records
    no ending. Applying it now would be judging an acceptance nobody has given.
  - `verification-postdates-the-code` → **not applicable** — an epic has no branch and no
    verification of its own; its children each passed this gate at their own close
  - `commits-reference-the-item` → **not applicable** — an epic is not a branch-scoped unit of
    work; this execution's commit is made on `main`, which is where an epic-level commit belongs
  - `tests-pass-on-the-merge-result` → **pass, incidentally** — 87 tests green on `main` after
    WI-0003's merge, run above; there is no merge of the epic's own to test
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings, run again by
    the transition against the state the move produces)
  - `record-is-reconstructible` → **pass** — from the tracker, `docs/` and `git log` alone: what
    was asked for (`IDEA.md`, the epic's `## Why now`, `vision.md` v2), what was decided and by
    whom (four answered stakeholder questions on the epic, one on WI-0001's terms, one each on
    WI-0002 and WI-0003; seven ADRs), what was built (three items, each with plan, implementation
    report, verification report and review), and what went wrong on the way (WI-0003's rejection
    on AC9, with both reproductions and the fix)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0 at WI-0003's
    close; this execution changes no document under `docs/`)
  - `epic-sign-off` → **FAIL, and correctly so — non-blocking on this move.**
    `check-epic-signoff EP-001` exited 1: "EP-001 has no usable sign-off — `Q-005.md` is
    still 'open' — the engagement waits on the stakeholder, which is the point of the gate."
    `transition` reported it as not blocking, because `review-close` gates only its
    completion move (to `done`) and this is `awaiting-answer`. That is the gate working:
    it refuses an *ending* while the sign-off is unanswered, and this execution records no
    ending. No sign-off had ever been filed on EP-001; `Q-005` is it, and the epic is
    suspended on it rather than closed over it.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-005.md` — the sign-off question: the goal in the
    stakeholder's own words, a transcript of the delivered tool, all three children named by ID
    with how each ended, the one accepted gap disclosed, and three real options
  - `tracker/items/EP-001/item.md` — suspended to `awaiting-answer` with `resume-to: open`
  - the commit of these files, made on `main`
- **Status:** `open` → `awaiting-answer`
- **Result:** EP-001 is at rest with every child delivered, and the stakeholder has been asked
  whether they accept it. The epic is suspended at `awaiting-answer` with `resume-to: open` and
  the loop stops here — this is the one gate in the pipeline that belongs to a person, and no
  ending may be recorded until they reply. Their answer selects it: accept → `done` /
  `delivered`; accept with follow-ups → `done` / `delivered` with new items filed; do not accept
  → `blocked`, the impasse, with what would resolve it; withdraw → `done` / `dropped`.

## 2026-08-29T13:22:02Z — answer-questions v0.3.1 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with `EP-001/Q-005` open, `addressed-to: human`, and
  `## Answer` filled in since the last turn — the case SKILL.md precondition 1 names as
  answerable. Run ahead of `next`, because an answered question left open stops the orchestrator.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` — the sign-off question and the stakeholder's reply
  - `tracker/items/EP-001/questions/Q-001.md`..`Q-004.md` — the four earlier answers, to check
    this one contradicts none of them
  - `tracker/items/EP-001/item.md`, `history.md` (the `resume-to: open` on the suspending row),
    `journal.md`
  - `docs/product/vision.md` (v2), `docs/architecture/overview.md` (v3)
  - `docs/architecture/adr/ADR-0001` (the ladder), `ADR-0002` (store location and format),
    `ADR-0004` (store schema, write protocol, next card number), `ADR-0007` (scheduling state)
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — each item's
    `## Out of scope`, all three of which name editing and deleting
  - `tracker/items/WI-0001/artifacts/refinement-qa.md`, `plan.md`
  - `.claude/agile-skills/spec/question.md`, `ids-and-statuses.md` §3.4/§3.5/§4/§5,
    `work-item.md`, `doc-header.md` §4/§5, `request.md`
- **Decisions:**
  - Read the reply as **an answer, not a deferral**. *"Yes — B. This is what I asked for, close it
    out."* settles the sign-off; the follow-up they name is additional work, not a condition on
    the acceptance. Route: the human answered an escalation (SKILL.md step 3, route 4 returning).
  - Filed the named follow-up as `WI-0004`, a `work-item` at `draft` under `EP-001` with
    `arose-from: EP-001/Q-005`. Rationale: SKILL.md step 3b requires it — an answer implied work
    no item recorded — and `EP-001`'s own `## Out of scope` had reserved exactly this case
    ("if the stakeholder wants it now they can say so and it becomes a new item"). Filing it as a
    request under `tracker/requests/` was not open to me: a request's only legal author is the
    human (`spec/request.md` §2).
  - Moved **deleting** a card into `EP-001`'s `## Scope` and left **editing** out, because the
    stakeholder split those two themselves: *"editing can wait"*. Recorded their refusals of a
    schedule-view command and of statistics as exclusions in their own words, so a later reader
    can tell a decision from an omission.
  - Recorded the disclosed `1.0` store gap as an explicit non-exclusion-by-choice rather than
    filing a bug for it. Rationale: it was put in front of them by name at sign-off and waved off
    — *"doesn't bother me"* — so filing a bug would overrule the person the bug is for.
  - **Returned the epic to `open` rather than closing it**, and said so in `Q-005`'s
    `## Consequences` rather than only here. Rationale: they asked for closure *and* for new work
    under the same epic, and mechanically those pull apart — ending E1 requires every child `done`
    and delivered (`spec/ids-and-statuses.md` §3.5), and `WI-0004` is now a child at `draft`.
    `open` is also the `resume-to` recorded on the suspending row, so this is the move the
    protocol prescribes either way. Their acceptance is preserved verbatim in `Q-005` for
    `review-close` to read when the engagement next comes to rest. Closing the epic first and
    filing `WI-0004` afterwards would have reached the same board via a `done → open` reopen
    (§3.4), and would have recorded an ending that was already known to be untrue when it was
    written.
  - Wrote **no ADR**. Rationale: nothing here was mine to decide. The scope decision is the
    stakeholder's, recorded verbatim, and it now lives in the two documents that carry scope; a
    third copy in an ADR is a place for it to drift.
  - Left `ADR-0004` unedited although the answer falsifies a premise it cites — option F weighed
    card-number reuse as low risk *"because nothing in the epic deletes a card"*. Rationale:
    `spec/doc-header.md` §5 says an ADR is updated "superseded only" and §4 says it preserves what
    was believed at the time; and there is no decision to supersede it with yet, since choosing
    between F and G is `plan`'s job on `WI-0004`. I had written the correction into `ADR-0004` as
    a v2 note and reverted it on reading §5. The overtaken premise is instead flagged in
    `WI-0004`'s `## Notes`, where `plan` will read it. Recorded as a gap in the toolkit rather
    than resolved by me: the record has no way to mark a still-current ADR's premise as overtaken
    short of superseding the decision.
- **Questions raised:** none. No question is open anywhere in this engagement.
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0004 --type work-item --title "Delete a card
    that was added by mistake" --epic EP-001 --priority medium --status draft --actor
    answer-questions --arose-from EP-001/Q-005 --reason "..."` → exit 0
  - `.claude/agile-skills/scripts/journal-entry WI-0004 --skill answer-questions --body-file ...`
    → exit 0, appended the entry at `2026-08-29T13:21:07Z`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 three times while the
    work was in flight (stale board; `EP-001` still suspended; `WI-0004`'s entry not yet written;
    one unresolvable citation form, `[src: ADR-0004 option F, v2 note]`, which I corrected to
    `[src: ADR-0004]`), then run again after this transition — see `**Gates:**`
  - `git checkout -- docs/architecture/adr/ADR-0004-...md` → exit 0, reverting the v2 note above
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `Q-005`'s `## Consequences` opened and
    checked: `tracker/items/WI-0004/item.md` exists and carries the follow-up, the epic
    (`EP-001`) and `arose-from: EP-001/Q-005`; `tracker/items/EP-001/item.md` `## Scope` line 54
    names removing a card and `## Out of scope` carries the split editing/deleting bullet plus the
    two new exclusions; `docs/product/vision.md` is v3 with the new section and a change-log row.
    The fourth entry names `ADR-0004` as deliberately unchanged and says where the fact went
    instead, which is a consequence a reader can check rather than an intention.
  - `answered-from-the-record` → **pass**. The answer is the human's own, quoted verbatim in
    `## Answer`; the scope split it produces is cited to it from `EP-001/item.md`,
    `docs/product/vision.md` and `WI-0004/item.md`. It contradicts no ADR: `ADR-0001`, `ADR-0002`
    and `ADR-0007` are untouched by deletion, and `ADR-0004`'s decision stands with only a premise
    overtaken, recorded in `WI-0004`'s notes.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human; no question is
    open on any item in this engagement.
  - `workspace-valid` → **pass** (`python3 .claude/agile-skills/scripts/validate-workspace .`,
    exit 0 after this transition and `board-gen`; recorded in the commit that follows).
  - `item-resumed-correctly` → **pass**. The suspending row
    (`2026-08-29T13:14:31Z`, `open → awaiting-answer`, actor `review-close`) records
    `resume-to: open`, and this execution's row targets `open`.
  - `a-deferral-is-not-an-answer` → **pass**, vacuously and deliberately checked: the reply defers
    nothing. *"Yes — B. This is what I asked for, close it out"* decides the sign-off, and the
    follow-up they name is scoped work rather than a condition withheld. `status: answered`, not
    `deferred`; no item was parked.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-005.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-08-29T13:20:04Z`, `## Consequences` written
  - `tracker/items/EP-001/item.md` — `## Scope` and `## Out of scope` amended as above
  - `docs/product/vision.md` — v2 → v3, new section, change-log row
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md` — new item at `draft`
  - `docs/architecture/adr/ADR-0004-...md` — edited, then reverted; unchanged in the end
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `open`
- **Result:** The stakeholder accepted EP-001 and asked for one more thing. Their acceptance is on
  the record in their words, the three things they declined are recorded as decisions rather than
  omissions, and `WI-0004` — delete a card added by mistake — exists at `draft`. The epic returns
  to `open`; it cannot end while a child is unfinished, and `review-close` will read this
  acceptance when the engagement comes back to rest.

## 2026-08-29T14:03:23Z — review-close v0.5.0 — reviewer

- **Item:** EP-001
- **Trigger:** status `open`, dispatched by `next` step 6 — no item was runnable (all four children at `done`, whose owner in `pipeline.yaml` is null) and `scripts/engagement-state EP-001` reported `at-rest`
- **Inputs read:**
  - `tracker/items/EP-001/item.md` (goal, the five success measures, scope and out-of-scope as amended by Q-005)
  - `tracker/items/EP-001/history.md` (five rows, chaining, last row `to: open` matching `item.md`)
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` (all five `answered`; Q-005 read in full, including its answer and its `## Consequences`)
  - `tracker/items/WI-0004/item.md` — the child delivered since the last rest: its ten ticked criteria, its `## Out of scope`, and the six accepted gaps recorded in `## Notes` at its close
  - `tracker/board.md`, and the frontmatter of `WI-0001`, `WI-0002`, `WI-0003` (status, priority, outcome)
  - `tracker/project.yaml` (trunk `main`, test command), `.claude/agile-skills/pipeline.yaml`
  - `.claude/agile-skills/spec/dor-dod.md` §4, `.claude/agile-skills/spec/question.md` §2
  - `git log --oneline` on `main`, and `README.md`/`recall.py` by running them (see Commands) rather than by reading about them
  - **No diff was read and no branch was examined:** this execution is the engagement-ending path of step 10, not the item-review path. There is no code and no branch belonging to EP-001.
- **Decisions:**
  - **Asked rather than closed.** `check-epic-signoff EP-001` refused the existing sign-off: `Q-005` was filed at 13:13:43Z, before this rest was reached at 13:58:30Z. That is correct and not a technicality — `Q-005` accepted a three-item tool and asked for a fourth; what is now on the table is the four-item tool. `spec/question.md` §2 says exactly one sign-off is due per rest, so a second one is due. Filed `Q-006`.
  - **Did not re-litigate the previous acceptance.** `Q-005`'s answer is on the record in the stakeholder's words and `Q-006`'s `## Context` opens by saying so, so that the second ask reads as a consequence of their own request rather than as the pipeline having lost their answer. Rationale: the failure mode a repeated sign-off invites is the stakeholder concluding they were not listened to.
  - **Grounded the question in a run of the merged code, not in the reports.** Every claim in `Q-006`'s `## Context` is a transcript produced just now on `main` — the add/delete/re-add/review loop, the second-review-same-day line, the 1 → 3 → 7 ladder with the wrong answer collapsing it, and `recall delete 9` exiting 1. Rationale: a sign-off is the one artifact the stakeholder judges the product from, and a product description assembled from item reports is a description of the tracker.
  - **Disclosed two of `WI-0004`'s six accepted gaps by name, and not the other four.** `ADR-0004`'s now-stale sentence and the weak `AC5` test are the two a stakeholder could plausibly care about; the remaining four (a two-survivor `AC3` run, unexercised argument shapes, unverified concurrency, an over-attributed mutation in the impl report) are internal evidence-quality gaps with no user-visible surface. Rationale: naming all six would bury the two that matter. All six remain recorded in `WI-0004`'s `## Notes`, which is where they survive.
  - **Warned about option B rather than presenting it neutrally.** Choosing B is what produced this second sign-off, and the stakeholder has no way to know that from the option text alone. Rationale: an options list that hides the cost of an option is not a real choice.
  - **Applied no Definition of Done criterion as passed.** DE1–DE7 are the criteria for *recording an ending*, and no ending has been selected — the answer selects it. Recording them as passed now would be claiming an outcome the stakeholder has not chosen. They are deferred to the execution that reads the reply.
- **Questions raised:** `Q-006` (blocking, `kind: sign-off`, to human)
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 11 documents, 0 errors (before filing)
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → exit 0, `at-rest`, rest reached 2026-08-29T13:58:30Z
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 1, `Q-005` filed before rest (before filing `Q-006`)
  - `python3 .claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 1, `Q-006` is still `open` — the engagement waits on the stakeholder (after filing)
  - `python3 -m unittest discover -s tests -t .` → exit 0, 101 tests, OK, on `main` at `48fba04`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors, 0 warnings
  - `./recall add|list|delete|review` against a throwaway `RECALL_FILE` → the transcript quoted in `Q-006`; `recall delete 9` → exit 1
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `epic-sign-off` → **fail** (`check-epic-signoff EP-001`, exit 1 — first because `Q-005` predates this rest, then because `Q-006` is open awaiting the stakeholder). This is the gate working: it is what sent this execution down the asking path rather than the closing one.
  - `definition-of-done` → **skipped** — `spec/dor-dod.md` §3 is the work-item and bug checklist and EP-001 is an epic; the epic checklist is §4 (DE1–DE7), which gates *recording an ending*, and this execution records none. DE7 is the criterion currently unsatisfied and `Q-006` is the act of satisfying it.
  - `verification-postdates-the-code` → **skipped** — no branch and no verification report exist for an epic; `check-verify-freshness` has no arguments to take.
  - `commits-reference-the-item` → **skipped** — EP-001 has no branch. Its record commits carry `refs EP-001` and are made on the trunk (`spec/workspace-layout.md` §5).
  - `tests-pass-on-the-merge-result` → **pass**, on the merge result the trunk already is: `python3 -m unittest discover -s tests -t .` exit 0, 101 tests, on `main` at `48fba04` with every child's branch merged. There is nothing to trial-merge, so no worktree was created and `main` was never at risk of being advanced (F-055).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 before filing). Filing `Q-006` deliberately makes `question.blocking.not-suspended` fire until this transition lands; re-run after the transition and recorded below.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log` alone: *what was built and why* — EP-001's goal and five success measures, four children each with a story and ticked criteria, `docs/product/vision.md` v3; *which skill decided what* — every history row names its actor and every journal entry names its skill and version; *what questions arose and how they resolved* — ten questions, every one `answered` with `## Consequences` naming files; *what verification found* — four `verify-report.md`s, including the two findings on `WI-0004` and the defect `WI-0003` was sent back for and re-verified.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0). No document changed relative to the trunk, which is the honest reading: this execution wrote a question, not a claim about code.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-006.md` (new) — the sign-off, naming all four children
  - `tracker/items/EP-001/item.md`, `history.md`, `journal.md` (updated by this transition)
  - `tracker/board.md` (regenerated)
  - No `review.md`: this execution reviewed no change. It will be written by the execution that records the ending.
- **Status:** `open` → `awaiting-answer`
- **Result:** EP-001 reached rest a second time, because the stakeholder's previous acceptance came with a request for more work and `WI-0004` delivered it. The sign-off they gave at the first rest cannot stand for the second, so `Q-006` was filed naming all four children, grounded in a run of the merged tool, and the epic is suspended awaiting their reply. Nothing is wrong and nothing is blocked; the pipeline is at the one gate that belongs to a person.

## 2026-08-29T14:07:31Z — answer-questions v0.3.1 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with `EP-001/Q-006` open, `addressed-to: human`,
  `kind: sign-off`, and `## Answer` filled in since the last turn — SKILL.md precondition 1's
  second case. Run ahead of `next`, because an answered question left open stops the orchestrator
  for ever (F-011).
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-006.md` — the second sign-off question and the reply
  - `tracker/items/EP-001/questions/Q-005.md` — the first sign-off, to check this answer against
    it; and `Q-001`..`Q-004`, the four framing answers it must not contradict
  - `tracker/items/EP-001/item.md`, `history.md` (the `resume-to: open` on the row of
    2026-08-29T14:03:23Z), `journal.md`
  - `docs/product/vision.md` (v3), `docs/architecture/overview.md` (v4)
  - `docs/architecture/adr/` — all nine: `ADR-0001` (ladder), `ADR-0002` (store location and
    format), `ADR-0003`, `ADR-0004` (store schema and write protocol, and the sentence the delete
    command overtook), `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008` (card numbers may be reused
    after a deletion), `ADR-0009`
  - `.claude/agile-skills/spec/question.md` §3/§4, `ids-and-statuses.md` §3.5, `doc-header.md`
    §3/§5, `work-item.md`
- **Decisions:**
  - Read the reply as **an answer, not a deferral**. *"A — accept as complete… I don't have
    anything else I want built right now, so close it out."* names an option, gives a reason and
    closes off follow-up work; nothing about it is contingent. Route: the human answered an
    escalation (SKILL.md step 3, route 4 returning). Contrast `Q-005`, which was option B and
    carried a named follow-up with it.
  - **Filed no new work item.** Option A names nothing further, so SKILL.md step 3b does not
    apply. The three candidates put to them by name — editing a card, a schedule-view command,
    statistics — were declined for the second time and are recorded as refusals rather than
    omissions, in both documents that carry scope.
  - **Did not close the epic.** `answer-questions` has no transition of its own and closure runs
    the Definition of Done, which is `review-close`'s (`spec/ids-and-statuses.md` §3.5). The epic
    goes to `open`, which is also the `resume-to` on the suspending row, and `review-close` will
    end it at E1 with this acceptance in hand.
  - **Wrote no ADR.** Nothing here was mine to decide: the decision is the stakeholder's and it
    is scope, not architecture. It now lives in `EP-001/item.md` and `vision.md`; a third copy in
    an ADR would be a place for it to drift. Same reasoning as the `Q-005` propagation.
  - **Left `ADR-0004` unedited**, although `Q-006`'s context discloses that the delete command
    overtook one of its sentences. Three reasons, all of them checkable: `spec/doc-header.md` §5
    makes an ADR superseded-only and §4 makes it a record of what was believed at the time; the
    fact that supersedes it is already decided and recorded, in `ADR-0008`, which is cited from
    `overview.md`; and the stakeholder was offered the tidying by name in option B and took
    nothing, so filing an item for it would manufacture work they declined. The overtaken premise
    remains flagged in `WI-0004`'s `## Notes`, where it has been since that item closed. This is
    the same gap in the toolkit noted at the `Q-005` propagation: the record still has no way to
    mark a still-current ADR's premise as overtaken short of superseding the decision.
  - Recorded the acceptance as **final scope** rather than merely as a sign-off: `EP-001`'s
    `## Scope` now says nothing may be added to this epic and that anything wanted later is a new
    request. Rationale: the engagement has now come to rest twice and reopened once, and a reader
    arriving at the epic should be able to tell from the epic itself that the second ending is
    the intended one.
- **Questions raised:** none. No question is open anywhere in this engagement.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before the work began;
    run again after this transition — see `**Gates:**`
  - `.claude/agile-skills/scripts/transition EP-001 --to open --actor answer-questions
    --reason "..." --journal-body-file ...` → see `**Status:**`
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `Q-006`'s `## Consequences` opened and
    re-read after editing: `docs/product/vision.md` is v4 with the new `## Where this stands`
    section, the delete bullet reading "Built and delivered as `WI-0004`" instead of "not built
    yet", the *"Not a card editor"* exclusion with its *"yet"* removed, and a change-log row;
    `tracker/items/EP-001/item.md` carries the "This scope is now final" paragraph at `## Scope`
    and three `## Out of scope` bullets that now cite `Q-006` as a second refusal. The two
    "deliberately unchanged" entries name what was not touched and why, which a reader can check
    against the files.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own, quoted verbatim
    in `## Answer` and again in both artifacts. It is checked against `Q-001`..`Q-005` and
    contradicts none of them; it repeats the `Q-005` refusals rather than reversing them.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human; this
    execution consumed an escalation rather than raising one.
  - `a-deferral-is-not-an-answer` → **pass** (no deferral). The reply names an option, gives a
    reason for it and states there is no further work — it settles the question outright, so
    SKILL.md step 3a does not apply and `status: answered` does not overstate it.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-29T14:03:23Z, actor
    `review-close`) records `resume-to: open`; this execution moves `awaiting-answer → open`,
    read from that row rather than inferred from the asking skill.
  - `workspace-valid` → see the run recorded after this entry; `validate-workspace` was exit 0
    immediately before the edits and is re-run immediately after the transition.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-006.md` — `status: answered`, `answered-at`,
    `answered-by: human`, and a `## Consequences` section naming every file changed and every
    file deliberately not changed
  - `docs/product/vision.md` — v3 → **v4**; new `## Where this stands`; delete recorded as
    delivered; editing/schedule-view/statistics recorded as declined a second time; change-log row
  - `tracker/items/EP-001/item.md` — `## Scope` final-scope paragraph and `WI-0004` marked
    delivered; three `## Out of scope` bullets now cite `Q-006`
  - `tracker/items/EP-001/journal.md`, `history.md` — this entry and its row
  - a commit of the above on the trunk
- **Status:** `awaiting-answer` → `open`
- **Result:** The stakeholder accepted the engagement as complete and asked for nothing further,
  so `EP-001` returns to `open` with its acceptance on the record and its scope closed. No work
  item was implied and none was filed. The epic is now at rest with all four children `done`,
  which is the state `review-close` ends at E1.

## 2026-08-29T14:12:28Z — review-close v0.5.0 — reviewer

- **Item:** EP-001
- **Trigger:** dispatched by `next` step 6 — no item is runnable and
  `scripts/engagement-state EP-001` reports `at-rest`. SKILL.md precondition 4: an epic at `open`
  at rest, so there is no branch and no diff, and the run goes straight to step 10. The sign-off
  (`Q-006`) was filed after rest and has been answered, so this execution is the *record the
  ending* half of step 10 rather than the *ask* half.
- **Inputs read:**
  - `tracker/items/EP-001/item.md`, `history.md`, `journal.md` in full
  - `tracker/items/EP-001/questions/Q-001.md`..`Q-006.md` — all six, including `Q-006`'s reply
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` —
    status and `outcome` on each
  - `docs/product/vision.md` (v4), `docs/architecture/overview.md` (v4)
  - `docs/architecture/adr/` — `ADR-0001`..`ADR-0009`; `ADR-0002` and `ADR-0004` read closely
  - `recall.py` (491 lines, in full), `recall`, `README.md` (221 lines), `tests/`
  - `.claude/agile-skills/spec/dor-dod.md` §4, `question.md` §2, `doc-header.md` §5,
    `ids-and-statuses.md` §3.5
  - no diff range: there is no branch for an epic and nothing to merge (SKILL.md step 8 does not
    apply to the engagement-ending path)
- **Decisions:**
  - **Did not certify the record from the reports.** Re-ran the five success measures myself
    against the merged trunk in a scratch store (`RECALL_FILE=/tmp/recallcheck/cards.json`)
    rather than reading `verify-report.md` and agreeing with it — SM1..SM5 all hold; the figures
    are in `## Commands` and the DE table.
  - **DE6 fails, and that is the finding.** Applying DE6 the one way that can fail — open the
    cited source, not the sentence — `docs/architecture/overview.md` line 80 says `recall.py` is
    *"roughly 280 lines"*, cited `[src: recall.py]`, and `wc -l recall.py` is **491**. The
    citation refutes the sentence it is cited for. It is not a stray number: it is the stated
    basis for a live decision (the store stays in one module), in the present tense, in a
    document marked `status: current`. It went stale because `plan` revised this document at v3
    and v4 for `WI-0003` and `WI-0004` — each adding a command and about a hundred lines — and
    neither revision re-checked a paragraph its own item had not touched. That is exactly the
    propagation DE6 was written against.
  - **Filed `Q-007` to the architect and suspended the epic rather than closing over it.**
    `spec/doc-header.md` §5 lists `architecture/overview.md` as updated by `plan` and
    `answer-questions`; `review-close` is not one of them, and the same table is what stops a
    reviewer editing the document it is about to certify. So the correction is not mine to make
    and closing with it recorded as an "accepted gap" would be recording `definition-of-done` as
    passed while knowing which criterion did not — the countersigning failure this skill's
    procedure names. `Q-007` is addressed to `architect`, so it does not stop the loop: `next`
    step 4 dispatches `answer-questions`, which may make the edit, and the epic then returns to
    `open` and is dispatched here again to close.
  - **Two related things checked and deliberately not escalated**, so that `Q-007` carries one
    decision. (1) `ADR-0004` line 65 — *"nothing in the epic deletes a card"* — is overtaken by
    `WI-0004`, but it is already handled correctly: `ADR-0008` quotes that sentence and
    supersedes the premise, which is what §5's superseded-only rule prescribes; it is in
    `WI-0004`'s `## Notes` and was disclosed to the stakeholder by name in `Q-006`, who closed
    without asking for it. (2) `scripts/lint-claims --all` reports three rule-2 errors in
    `ADR-0002` (lines 72, 97, 102: absolutes with no citation in the paragraph). Every
    *citation* in the workspace resolves, the contracted gate form exits 0, and `ADR-0002` is
    superseded-only. Both are recorded as accepted gaps in `Q-007`'s context so they survive
    this execution rather than living in a journal nobody re-reads.
  - **Recorded no ending yet, and wrote no `review.md` yet.** Both belong to the execution that
    actually closes the epic; writing a verdict now would date a Definition of Done table that
    has a failing criterion in it.
  - **Filed no bug item.** Nothing in delivered *behaviour* is wrong: the finding is a sentence
    in a design document, and a bug item would give it a plan, criteria and a verification it
    does not need.
- **Questions raised:** `EP-001/Q-007` — to `architect`, blocking. It does not stop the loop.
- **Commands:**
  - `.claude/agile-skills/scripts/engagement-state EP-001` → exit 0, `at-rest`, "every child has
    stopped, no question is open, no request is open; rest reached at 2026-08-29T13:58:30Z"
  - `.claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 0, "Q-006.md carries the
    stakeholder's reply, names all 4 child item(s), and was filed after the engagement reached
    rest"
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0 (the contracted
    form); `.claude/agile-skills/scripts/lint-claims --all` → exit 1, 3 errors, all in
    `ADR-0002`, all rule 2
  - `python3 -m unittest discover -s tests -t .` → exit 0, **101 tests, OK**, on the merged trunk
  - `wc -l recall.py` → **491**
  - `recall add`/`list`/`delete`/`review` against a scratch `RECALL_FILE`, and a five-round
    ladder walk → `interval` 1 → 3 → 7 → 30 → 30, then a wrong answer → 1, `due` moving
    2026-08-30, 09-01, 09-05, 09-28, 09-28, 08-30
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before this transition;
    re-run by the transition itself
- **Gates:**
  - `definition-of-done` → **fail** (DE6). Criterion by criterion, `spec/dor-dod.md` §4:
    **DE1 pass** — all four children terminal (`WI-0001`..`WI-0004`, every one `done`), and all
    four named in `Q-006`'s table; none undelivered.
    **DE2 pass** — every child carries `outcome: delivered`; nothing dropped, so no `## Notes`
    reason is owed.
    **DE3 pass** — all five success measures re-run by me on the merged trunk, not taken from
    the reports: SM1 three cards added and read back in later runs; SM2 a card added today is
    due today (`due: 2026-08-29` on add, and it appears in `review`); SM3 a second `review` the
    same day prints "Nothing is due today."; SM4 the ladder walk above — strictly later after
    two rights (3 days) than one (1 day), capped at 30, and a wrong answer back to 1 day counted
    from the day of review; SM5 the store is one readable JSON file, printed in `## Commands`.
    **DE4 pass** — `docs/product/vision.md` v4 describes the tool as built, including `delete`
    as delivered and the three declined candidates; checked against the four commands `main`
    actually dispatches (`recall.py:482-491`).
    **DE5 pass** — no question anywhere in the engagement was open when this execution began;
    `Q-007` is the one this execution filed.
    **DE6 FAIL** — `docs/architecture/overview.md:80` claims `recall.py` is "roughly 280 lines"
    citing `recall.py`, which is 491. Claims I checked from their citations and found sound:
    the ladder is 1/3/7/30 (`recall.py:34` `LADDER`); a new card is due the day it is added
    (`recall.py:212-222` + `cmd_add` passing `today()`); a card at 30 days stays at 30
    (`recall.py:266-267`); a wrong answer returns to the bottom rung and is due the next day
    (`next_interval` + `record_result`, `recall.py:264-282`); the wait is counted from the day of
    review, never from the old `due` (`recall.py:281-282`); "not a card editor" and "nothing else
    acts on an existing card" (`main` dispatches only `add`/`list`/`review`/`delete`,
    `recall.py:482-491`); `delete` leaves every other card untouched and does not renumber
    (`delete_card`, `recall.py:234-238`); the next number is one above the largest stored, so a
    freed number is reusable (`add_card`, `recall.py:220`); `RECALL_FILE` when set and non-empty
    else `~/.recall.json` (`store_path`, `recall.py:69-74`); the store is refused rather than
    repaired, by every command, on a bad `due` or `interval` (`load`, `recall.py:104-171`, called
    from all four commands); the session reads whole lines and never a terminal, and end-of-input
    ends it exactly as `q` does (`read_line` and `_await_key`, `recall.py:285-295`, `459-473`).
    Every citation in the workspace resolves.
    **DE7 pass** — `check-epic-signoff` exit 0, above.
  - `epic-sign-off` → **pass**. `check-epic-signoff EP-001` exit 0; `Q-006` names all four
    children and postdates rest.
  - `claims-are-sourced` → **pass** as contracted (`lint-claims --changed-since main`, exit 0).
    Recorded with the `--all` result beside it, because the passing form checks nothing when the
    trunk is the working tree, and the finding above is the substance the gate is for.
  - `tests-pass-on-the-merge-result` → **pass**. 101 tests, exit 0, on the merged trunk. There is
    no branch to trial-merge for an epic, so SKILL.md step 8's worktree procedure does not apply
    and `git rev-parse main` was never at risk of moving; the trunk is untouched by this
    execution apart from its own record commit.
  - `verification-postdates-the-code` → **skipped**. No branch and no `verify-report.md` on an
    epic; each child ran this gate at its own close.
  - `commits-reference-the-item` → **skipped**. Same reason: an epic has no branch, and the gate
    inspects commits not yet on the trunk.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep EP-001`
    alone: what was built and why is in `## Goal` and `vision.md`; which skill decided what is in
    six history chains and nine ADRs; what was asked and how it resolved is `Q-001`..`Q-006` with
    `## Consequences` naming real files in each; what verification found is four
    `verify-report.md`s, including the two defects `WI-0003` verification caught in `load` and
    the six gaps `WI-0004` closed with. The one thing a reader could not have reconstructed —
    why `overview.md`'s line count disagrees with the file — is what `Q-007` now records.
  - `workspace-valid` → run by this transition; exit 0 immediately before it.
- **Artifacts:**
  - `tracker/items/EP-001/questions/Q-007.md` — created, to `architect`, blocking, with the two
    checked-and-not-escalated findings recorded in its context
  - `tracker/items/EP-001/journal.md`, `history.md` — this entry and its row
  - no `review.md` yet, no merge commit, no bug item — all three belong to the execution that
    records the ending
  - a commit of the above on the trunk
- **Status:** `open` → `awaiting-answer`
- **Result:** Everything the stakeholder was promised is built and works — I re-ran all five
  success measures myself and the 101-test suite passes on the trunk — and six of the seven epic
  Definition of Done criteria pass. DE6 does not: `docs/architecture/overview.md` states
  `recall.py` is "roughly 280 lines" as the basis for a live design decision, and it is 491.
  Correcting it belongs to the architect, so `EP-001` is suspended on `Q-007` and will close on
  the next pass rather than closing over a criterion I know to have failed.

## 2026-08-29T14:14:45Z — answer-questions v0.3.1 — architect

- **Item:** EP-001
- **Trigger:** status `awaiting-answer` with `EP-001/Q-007` open and `addressed-to: architect` —
  SKILL.md precondition 1's first case. Dispatched by `next` step 4; it is the only open question
  in the workspace.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-007.md` — the finding, its four options and its two
    checked-and-not-escalated notes
  - `tracker/items/EP-001/item.md`, `history.md` (the `resume-to: open` on the row of
    2026-08-29T14:12:28Z), and the `review-close` journal entry that filed it
  - `docs/architecture/overview.md` (v4) — the whole document, and `## Why it is arranged this
    way` line by line
  - `recall.py` in full, and measured: 491 lines, ~90 blank, ~24 comment lines, ~120 docstring
    lines, ~257 code; 20 functions and one exception class
  - `docs/architecture/adr/ADR-0002` (lines 60-110, the three lint-claims sites), `ADR-0004`
    (line 65), `ADR-0008` (line 22, which quotes and supersedes it)
  - `.claude/agile-skills/spec/doc-header.md` §3/§4/§5, `question.md` §3/§4, `dor-dod.md` §4
- **Decisions:**
  - **Answered A, and decided it myself** — SKILL.md step 3 route 3. No escalation condition in
    `spec/question.md` §4 applies: the record is not silent, the correction is trivially
    reversible, it contradicts no ADR, and it commits the project to nothing. Forwarding a line
    count to the stakeholder — who has just closed the engagement — would be the "architect who
    forwards every question" the procedure warns about.
  - **Re-affirmed the decision rather than rubber-stamping the number.** Option A asks whether
    keeping the store in one module still holds at 491 lines, which is a judgement, so I checked
    the two things it rests on. (1) Composition: ~260 of the 491 lines are code and ~230 are
    docstrings, comments and blanks — several comments recording defects verification found, in
    `_is_date` and the `isinstance(..., bool)` guard in `load`. Judged as code the module is near
    the size the stale sentence claimed, which is why the drift was invisible: what grew was
    mostly the explanation. (2) The seam: `load` and `save` are still the only functions that
    touch the disk, `store_path` decides where, and `add_card`, `delete_card`, `due_cards`,
    `next_interval` and `record_result` all work on an in-memory document. `delete_card`, added
    last by `WI-0004`, was written to that contract without altering it. Both hold, so B — record
    the premise as changed — would have been false.
  - **Fixed the deeper fault, not only the number.** The paragraph led with a line count, which
    invited three successive `plan` executions to read size as the criterion; it never was. The
    rewrite states the re-ask trigger — *something other than a command needs the store* — as the
    trigger rather than as a trailing sentence, and says explicitly that the figure is not the
    reason. Correcting 280 to 491 alone would have left the next reader measuring the wrong
    thing, and the number would go stale again.
  - **Wrote no ADR.** This is not a new decision: `overview.md` already carried it and it is
    unchanged. An ADR would be a second copy of a live decision and a place for it to drift —
    which is, precisely, the failure being repaired.
  - **Left `ADR-0002`'s three rule-2 errors alone**, and recorded why in `Q-007`'s
    `## Consequences` rather than only here. The claims are true — checked against `store_path`
    (`recall.py:69-74`) — so what is missing is provenance, not accuracy; and
    `spec/doc-header.md` §5 makes an ADR superseded-only, so adding a citation to a live one is
    an edit I may not make. **Recorded as a toolkit gap:** there is no legal move in this
    methodology that adds a missing citation to a still-current ADR, so a `claim.unsourced` error
    introduced in an ADR can never be cleared by any skill. It is invisible to the contracted
    gate (`lint-claims --changed-since <trunk>` checks only what a branch changed) and only
    surfaces under `--all`.
  - **Filed no work item and no bug.** Nothing widened scope, so step 3b does not apply, and no
    delivered behaviour is wrong — `recall.py` is untouched by this execution.
- **Questions raised:** none.
- **Commands:**
  - `wc -l recall.py` → 491; a tokenizer pass over `recall.py` → ~90 blank, 24 comment lines,
    ~120 docstring lines, ~257 code; `grep -c '^def \|^class '` → 21 (20 functions, 1 class)
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 1, 4 errors after my first edit — my
    own new paragraph had introduced one (`overview.md:77`, an unsourced "all four commands") —
    then exit 1 with 3 after citing it, all three the pre-existing `ADR-0002` sites. The gate
    caught my own regression within a minute of writing it, which is the argument for running
    `--all` rather than the contracted form when the trunk is the working tree.
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → run by this transition
- **Gates:**
  - `answer-is-propagated` → **pass**. Both files named in `Q-007`'s `## Consequences` re-opened
    after editing: `docs/architecture/overview.md` is v5 with the rewritten paragraph — "roughly
    280 lines" is gone, 491 is present and cited `[src: run: wc -l recall.py → 491]`, the seam is
    named function by function, the trigger is restated and the figure disclaimed as not being it
    — plus the `[src: EP-001/Q-007; src: WI-0002]` citation on the first paragraph and a
    change-log row. The three "deliberately unchanged" entries name what was not touched and why.
  - `answered-from-the-record` → **pass**. The correction follows from the cited source itself:
    `recall.py` is 491 lines and the sentence citing it said 280. The re-affirmation follows from
    `recall.py`'s function boundaries, read rather than remembered, and from `WI-0001`'s function
    contracts which fixed them.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human; none of
    `spec/question.md` §4's four conditions applies, and the reasoning is in `## Decisions`.
  - `a-deferral-is-not-an-answer` → **pass** (no deferral). `Q-007` was addressed to the
    architect, answered by the architect, and settles the question outright.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-29T14:12:28Z, actor
    `review-close`) records `resume-to: open`; this execution moves `awaiting-answer → open`.
  - `workspace-valid` → run by this transition; `lint-claims --all` additionally re-run and down
    to the three pre-existing `ADR-0002` errors, none introduced here.
- **Artifacts:**
  - `docs/architecture/overview.md` — v4 → **v5**; the `## Why it is arranged this way` store
    paragraph rewritten; two citations added; change-log row
  - `tracker/items/EP-001/questions/Q-007.md` — `status: answered`, `answered-by:
    answer-questions`, with the answer, the two checks behind it, and why each of B, C and D was
    rejected
  - `tracker/items/EP-001/journal.md`, `history.md` — this entry and its row
  - a commit of the above on the trunk
- **Status:** `awaiting-answer` → `open`
- **Result:** The DE6 finding was real and is fixed at the root: `overview.md` v5 states the
  module's actual size, names the seam that carries the decision so a reader can re-check it, and
  says plainly that the re-ask trigger is a need, not a line count — which is what stopped three
  `plan` executions noticing. `EP-001` returns to `open` for `review-close` to re-apply the
  Definition of Done and record ending E1.

## 2026-08-29T14:20:24Z — review-close v0.5.0 — reviewer

- **Item:** EP-001
- **Trigger:** epic at `open` and `scripts/engagement-state EP-001` reporting `at-rest`; dispatched by `next` at orchestrator step 6, no item being runnable
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the goal, SM1–SM5, the now-final scope, the exclusions
  - `tracker/items/EP-001/history.md` (9 rows) and `journal.md` (8 entries) — read in full; the chain has no gap and the last row `→ open` matches `item.md`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-007.md` — all `answered`; `Q-006` is the sign-off this ending rests on, `Q-007` the DE6 finding from the previous execution
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — statuses and outcomes; and the five questions across them, all `answered`
  - `docs/product/vision.md` v4, `docs/architecture/overview.md` v5, `docs/architecture/adr/ADR-0002`, `ADR-0007`, `ADR-0008`, `ADR-0009`, `README.md`
  - `recall.py` — read for the claim audit, not for a diff: there is no branch and no diff range at an epic ending; the code was reviewed under each child item
- **Decisions:**
  - **Ending E1 — delivered.** Every child is terminal at `done` with `outcome: delivered`, and the stakeholder accepted unconditionally at `Q-006` (option A, *"close it out"*). The table in `spec/dor-dod.md` §4 maps accept + all delivered to `open → done`, `outcome: delivered`. No child is undelivered, so nothing here overclaims.
  - **Re-ran SM1–SM5 myself rather than reading the previous ending's evidence.** DE3 asks whether the success measures are met, and the prior run's transcript is a claim like any other. All five met: SM4's ladder walk gave `interval` 1 → 3 → 7 → 30 → 30 with a wrong answer returning to 1 and `due` to the day after the review.
  - **Audited DE6 from the citations, not the prose.** Eight claims opened at their sources. The claim that failed at the previous ending (`overview.md`'s *"roughly 280 lines"*) is now *"491 lines… roughly 260 code"* and `wc -l` returns 491; an AST split gives 260 code against 90 blank, 24 comment, 118 docstring. I also checked the seam the surrounding decision rests on rather than the sentence describing it — `load` and `save` are the only functions in the module containing `open(`, `tempfile`, `.write(` or `os.replace`. The fix is real, not editorial.
  - **Two hard gates recorded as skipped, not forced.** `check-commit-refs` and `check-verify-freshness` are branch-and-verification gates; an epic has neither, which `SKILL.md` precondition 4 states outright. Both scripts exit 1 with messages that say exactly this. Forcing them would have recorded `[gates forced]` on a clean ending and made a structural non-applicability look like an override.
  - **Accepted three gaps rather than closing over them silently**, each written into `review.md` `## Accepted gaps`: `ADR-0002`'s three unsourced-but-true absolutes, which `spec/doc-header.md` §5 makes unfixable by any skill; the contracted claims gate being structurally blind at an epic ending; and the `1.0`-in-the-store behaviour the stakeholder waved off at `Q-005`, which survives in the epic's `## Out of scope`.
- **Questions raised:** none — `Q-006` already carries the stakeholder's reply and `Q-007` resolved the only Definition of Done failure, so there was nothing left to ask
- **Commands:**
  - `scripts/engagement-state EP-001` → 0, `at-rest`, rest reached 2026-08-29T13:58:30Z
  - `scripts/check-epic-signoff EP-001` → 0, PASS — `Q-006` carries the reply, names all 4 children, filed after rest
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 101 tests… OK`
  - `recall add` / `list` / `review` / `delete` against `RECALL_FILE=/tmp/smcheck/store.json` → SM1–SM5 transcripts in `review.md`
  - `wc -l recall.py` → 491
  - `scripts/lint-claims --changed-since main` → 0, `checked no documents changed since main`
  - `scripts/lint-claims --all` → 1, 3 `claim.unsourced` errors, all in `ADR-0002`
  - `scripts/check-commit-refs EP-001 main` → 1, `main..main is empty`
  - `scripts/check-verify-freshness EP-001 main` → 1, `EP-001 has no verify-report.md`
  - `scripts/validate-workspace .` → 0, 5 items / 11 documents, 0 errors 0 warnings
- **Gates:**
  - `definition-of-done` → **pass** (epic §4 walked criterion by criterion; the DE1–DE7 table with per-criterion evidence is in `review.md` `## Definition of Done`. DE3 rests on SM1–SM5 re-run here, DE6 on eight claims opened at their citations)
  - `epic-sign-off` → **pass** (`check-epic-signoff EP-001` exit 0; `Q-006` names all four children and postdates rest)
  - `tests-pass-on-the-merge-result` → **pass** (no merge to make at an epic ending; `{{commands.test}}` run against the trunk, which is the merge result of all four children: 101 tests, OK)
  - `workspace-valid` → **pass** (`validate-workspace` 0 errors, 0 warnings)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 — and recorded as an accepted gap that the contracted form inspects nothing on this path, since there is no branch; `--all` was run in addition and its 3 findings are the `ADR-0002` gap)
  - `record-is-reconstructible` → **pass** (what was built and why: the epic's goal, `vision.md` v4 and nine ADRs. Which skill decided what: 9 history rows and 8 journal entries on the epic, each naming its actor. What questions arose and how they resolved: 12 questions, all `answered`, each with `## Consequences` naming files that exist. What verification found: each child's `verify-report.md`, reachable with `git log --grep` — 8 commits for EP-001, 14/19/18/15 for WI-0001..WI-0004)
  - `verification-postdates-the-code` → **skipped** (an epic has no `verify-report.md` of its own; `check-verify-freshness EP-001 main` says so and exits 1. Each child's verification freshness was gated at that child's own close)
  - `commits-reference-the-item` → **skipped** (an epic has no branch; `check-commit-refs EP-001 main` reports `main..main` is empty and exits 1. Each child's commits were gated at that child's own close)
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/review.md` — created: what was examined, the DE1–DE7 table, two findings, three accepted gaps, the E1 verdict
  - `tracker/items/EP-001/item.md` — `status: done`, `outcome: delivered`
  - `tracker/items/EP-001/history.md`, `journal.md` — this row and this entry
  - `tracker/board.md` — regenerated by the transition
  - commit: `tracker: the epic's review and the ending of the engagement (refs EP-001)`
- **Status:** `open` → `done`
- **Result:** EP-001 is closed at ending **E1 — delivered**. The engagement asked for a flashcard tool that adds cards, reviews what is due each day, schedules with simple spaced repetition, and keeps progress across runs; all four children delivered it, all five success measures were re-run at this ending and met, and the stakeholder accepted it as complete. Recall does what was asked: `recall add` writes a card, `recall list` prints the pile, `recall review` walks the due cards recording right or wrong, `recall delete` takes one back out, and the 1/3/7/30-day ladder in one JSON file on disk is what makes yesterday's effort still count today.
