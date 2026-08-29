# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-29T10:47:30Z — intake v0.2.1 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's opening statement in `IDEA.md`; no status made this runnable, `intake` is not scheduled
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement)
  - `tracker/project.yaml`
  - `tracker/items/` (empty — no prior epic or item to overlap with)
- **Decisions:**
  - This item exists because EP-001 was split into three; see EP-001's entry for how the split was chosen and why it is three and not one or five. This item carries deciding when a reviewed card comes back.
  - Acceptance criteria written without naming any interface technology, because the stakeholder named none and `EP-001/Q-001` is open on exactly that. Writing "runs `recall add`" here would have been design smuggled in as analysis.
  - Depends-on set to WI-0002, derived from logical necessity rather than from a stated preference: there is nothing to review before cards persist, and nothing to schedule before a review records a result. The stakeholder gave no ordering, so priority is uniform and the ordering lives in `depends-on` where it can be justified.
- **Questions raised:** none on this item; `EP-001/Q-001`–`Q-004` are open on the epic and gate this item's refinement
- **Commands:**
  - `scripts/new-item --id WI-0003 --type work-item --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, reported on EP-001's entry for the whole execution)
  - `epic-has-success-measures` → **pass** (EP-001 SM1–SM5; assessed on the epic, see its entry)
  - `items-are-separable` (advisory) → **pass** (build order WI-0001 → WI-0002 → WI-0003, recorded in `depends-on`)
  - `no-solution-in-the-problem` (advisory) → **pass** (title and story name no technology; see EP-001's entry for what was kept out)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/history.md` (new, creation row)
  - `tracker/items/WI-0003/journal.md` (this entry)
- **Status:** `—` → `draft`
- **Result:** Created at draft with provisional acceptance criteria. It cannot be refined until the four questions open on EP-001 are answered.

## 2026-08-29T12:23:25Z — refine v0.2.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — the only runnable item on the board, WI-0001 and WI-0002 being `done`
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (one row: created by `intake`; not a send-back, so this is a fresh refinement), `journal.md`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-004.md` — all four answered by the stakeholder; `Q-002` and `Q-003` are what fix this item's ladder
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` and `tracker/items/WI-0002/artifacts/refinement-qa.md` — for the standing deferral and for what each round decided rather than asked
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md`, `ADR-0006-review-state-on-a-card-and-store-version-2.md`
  - `README.md` and `recall.py` (`today`, `add_card`, `due_cards`, `record_result`) — to know what a verifier can already observe and what this item must add
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **One question filed, to the stakeholder: which rung a brand-new card starts on** (`Q-001`). It survives all four branches of the addressee test — it changes what the user experiences the first time they get a new card right; their reply to `EP-001/Q-002` is honestly readable both ways and `ADR-0001` fixed the intervals without fixing the starting point; the standing deferral covers file layout and wording, not the shape of the schedule, which is the one subject they have answered specifically and twice; and the answer differs depending on who the stakeholder is. Both `WI-0002`'s refinement and its `review-close` recorded the gap and routed it here rather than deciding it.
  - **The observation mechanism, which is what the item's `## Notes` said `refine` owed it: read and hand-edit the store file.** `[assumed]` under `WI-0001/Q-002`'s standing deferral, whose category is file layout and how a thing is checked. `README.md` already documents hand-editing `due` to move a card and `WI-0002` AC8 was verified this way, so the mechanism is established. Stated at the head of the criteria so AC2, AC3, AC5, AC7, AC8 and AC9 all mean one thing, and so none of them needs a month to check.
  - **AC4 now names `README.md`** rather than "the project's documentation", and requires the rung field to have a row in the card-field table — the same resolution `WI-0001` AC5 took for the same phrase, under the same deferral.
  - **AC9 is new, and it settles the defect `review-close` handed this item**: a `due` of `"tomorrow"` is accepted by `load`, sorts above every real date, and removes a card from every review for ever. Decided as an unreadable store — reported, exit 1, file left byte-identical — which is what `README.md` already promises and what `ADR-0004` already makes the rule. Not left alone, because this item makes hand-editing that field the documented way to move a card.
  - **AC7 and AC8 are new**: a card the session never reached keeps its rung and due date (nothing said what happened to unreached cards, and this is the first item for which they carry state worth keeping); and a store written before this item is read and upgraded in place, by the precedent `ADR-0006` set when WI-0002 added `due` and `result`.
  - **AC1 and AC5 restated in observable form** — a regression check on behaviour WI-0001 and WI-0002 already deliver, and a named second process plus the file on disk. No new decision in either.
  - **Three exclusions added to `## Out of scope`**: the session's output does not change, there is no command for seeing or setting a schedule, and no review history is kept. The first two are what a reader would most reasonably assume this item includes.
  - **Five design questions routed to `plan`** in `## Notes` rather than to anyone's inbox: the rung field's name and representation, whether `version` becomes 3, where the intervals live, whether the never-answered state is a stored value or an absence, and which error path AC9 reports through. Each would have the same answer whoever the stakeholder was.
  - **AC2 and AC3 deliberately do not depend on `Q-001`.** A wrong answer returns a card to the bottom *rung*, not to the never-answered state (`ADR-0001`), so the rung-to-rung moves and the reset are checkable either way. Only AC6 waits.
- **Questions raised:** `WI-0003/Q-001` — one, addressed to `human`, blocking, open; recorded in `artifacts/refinement-qa.md` as `[unresolved]`
- **Commands:**
  - `scripts/validate-workspace .` → exit 1 before the transition, reporting exactly the two errors this execution intends to create and resolve: `board.stale` and `question.blocking.not-suspended` on this item
  - `scripts/board-gen .` → exit 0, wrote `tracker/board.md`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/transition` ran it against the state this move produces, per F-014: the open blocking question is legal once the item is `awaiting-answer`)
  - `definition-of-ready` → **fail, recorded criterion by criterion** in `artifacts/refinement-qa.md`. R1 pass (frontmatter complete), R2 pass (role, capability, outcome), R3 pass (AC1–AC9 as labelled checkboxes), **R4 fail** (AC6 is a placeholder naming `Q-001` as what chooses between two candidate behaviours; every other criterion names a command and its verdict), R5 pass (six exclusions, three of them things a reader would assume were included), **R6 fail** (`Q-001` open and blocking — deliberately), R7 pass (`depends-on: WI-0002`, which is `done`), **R8 fail** (this round's Q&A is `status: agenda`; the conversation has not happened), R9 pass (one coherent change: a rung, the ladder that moves it, and the documentation and validation of the field carrying it), R10 pass (the item's R10 paragraph enumerates every combination). R4, R6 and R8 fail together and for one reason — the stakeholder has not replied
  - `criteria-are-decidable` → **fail on AC6, pass on the other eight**, each with the command named in the R4 row of the Q&A table
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` holds the question as filed and every decision tagged `[assumed]` with the deferral or precedent it rests on; the one thing asked is tagged `[unresolved]` rather than written up as though it had been answered)
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0003/item.md` (AC1–AC5 rewritten, AC6–AC9 added, three exclusions added, `## Notes` restructured)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `awaiting-answer`
- **Result:** Round 1 refined eight of the nine criteria to the point where a verifier with a terminal could settle each one, and filed the single decision that is not `refine`'s to take. The item is suspended on `Q-001` with `resume-to: draft`; `refine` returns for round 2 once the stakeholder has replied, and what round 2 has to do is AC6, the R8 flip to `recorded`, and nothing else.

## 2026-08-29T12:29:01Z — answer-questions v0.3.1 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer` with `WI-0003/Q-001` open and its `## Answer` filled in by the stakeholder; run first this turn, before `next`, per the precondition that only this skill may consume a human's reply
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` (the only question on the item; the reply)
  - `tracker/items/WI-0003/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` (v1) — the ADR that owns the ladder
  - `docs/architecture/adr/ADR-0006-review-state-on-a-card-and-store-version-2.md` (v1) — for the declared day-after placeholder and the `result` field
  - `tracker/items/WI-0002/questions/Q-001.md` and `tracker/items/WI-0001/questions/Q-002.md` — the two precedents for how a stakeholder's own choice and a stakeholder's deferral are each recorded
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — the precedent for what this skill writes into a Q&A file and what it leaves to `refine`'s round 2
  - `.claude/agile-skills/spec/question.md`, `spec/journal-and-history.md`, `spec/doc-header.md`
- **Decisions:**
  - **`Q-001` is answered, route: the human replied to an escalation.** They named option B — *"B — tomorrow. When I said one day, then three, then a week, then a month, that's the order I meant to actually see, starting from a new card."* `answered-by: human`, not `answer-questions`: they picked a named option and gave the reason, so recording anything else would understate what they settled. This is not a deferral — contrast `WI-0001/Q-002`, where the same field says `answer-questions` because the stakeholder declined to choose.
  - **`ADR-0001` is amended to version 2 rather than superseded.** Version 1 fixed the four intervals and both moves and left the starting rung *unstated*; it did not decide it the other way. An amendment is therefore honest and a supersession would misdescribe the record. The never-answered state is written into `## Decision` as its own rule, with the two consequences that follow — the top rung is reached after four right answers rather than three, and on a new card's first review right and wrong are indistinguishable except in `result`.
  - **AC6 is amended, and the amendment is legal and named.** The item is at `draft` (criteria freeze at `ready`), and this skill is one of the two permitted to change a criterion. AC6 was written by `refine` as an explicit placeholder naming this question; the answer replaces it with a criterion someone with a terminal can settle — `recall add` into an empty store, `printf '\ny\n' | recall review`, the card due the day after today on the 1-day rung, then 3 days after a second right answer. It still describes what the stakeholder asked for, because it is the option they chose in their own words.
  - **The cost option B named is written into AC6 rather than left for verification to trip over.** On a brand-new card's first review a right answer and a wrong answer produce the same rung and the same due date; only `result` differs. A verifier meeting that without warning would reasonably read it as a defect, and the stakeholder accepted it when choosing.
  - **No bug filed and no work item filed.** The answer chooses between two behaviours AC6 already bounded, so nothing is widened (`spec/ids-and-statuses.md` §5 not engaged). Nothing delivered contradicts it either: `WI-0002` writes the day after the review for both answers as `ADR-0006`'s declared placeholder, which option B happens to make correct for a new card's first right answer — so WI-0003 still changes the right-answer path for cards already on a rung, exactly as its notes say.
  - **`refinement-qa.md` keeps `status: agenda`.** The reply is recorded verbatim there and its Definition of Ready table is marked out of date, but flipping the file to `recorded` and re-reading the DoR is `refine`'s round 2, not this skill's. R4 and R6 are settled by the answer; R8 reads this field and is honestly still failing until `refine` runs.
  - Round 1's reasoning in `refinement-qa.md` is kept rather than replaced — it is the record of *why* this was asked instead of decided, which is the part a later reader needs.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-29T12:26:01Z
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 first (changelog newest-first, and an unresolvable `[src: `Q-001`]` citation in the new AC6), both fixed, then exit 1 only on `board.stale` and `question.awaiting.none-open`, which this transition and `board-gen` clear
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in `## Consequences` opened and checked after writing: `ADR-0001` frontmatter reads `version: 2` / `updated-for: WI-0003` with the never-answered bullet in `## Decision`, the reply quoted in `## Context` and a version-2 change-log row; `item.md` AC6 no longer says "pending", its `## Notes` section is retitled to what was settled and quotes the reply, the R10 paragraph no longer says "pending `Q-001`", and the plan-routed bullet now bounds what `plan` still owns; `refinement-qa.md` carries the reply tagged `[human]` in place of `[unresolved]`. Four files, all changed.
  - `answered-from-the-record` → **pass** — the answer is the stakeholder's own words in `Q-001`'s `## Answer`, quoted verbatim in all three places it landed, and the decision it settles is recorded as an ADR amendment (`ADR-0001` v2) rather than left in the question file.
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human. `refine` had already escalated this one under `spec/question.md` §4 (intent no document records) and it has now been answered.
  - `workspace-valid` → **pass** — `validate-workspace` reports 0 errors after this transition and `board-gen`; the two errors outstanding before it were exactly the ones the move clears.
  - `item-resumed-correctly` → **pass** — the suspending row (2026-08-29T12:23:25Z, `draft` → `awaiting-answer`, actor `refine`) records `resume-to: draft`, and this row's target is `draft`. Not inferred from which skill asked.
  - `a-deferral-is-not-an-answer` → **not engaged** — the reply is not a deferral. The stakeholder named option B and gave their reasoning, so neither move in §3a applies; move 1 would have understated it and move 2 would have parked an item nobody is waiting on.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — `status: answered`, `answered-by: human`, `answered-at: 2026-08-29T12:26:01Z`, `## Consequences` written naming four files
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` — v1 → **v2**, `## Decision` and `## Context` amended, change-log row added
  - `tracker/items/WI-0003/item.md` — AC6 rewritten; `## Notes` retitled and rewritten around the answer; the plan-routed never-answered bullet bounded; the R10 paragraph de-pended; "Where the criteria came from" cites `ADR-0001` v2
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — the reply recorded verbatim under Round 1, the header narrowed to say what is and is not still outstanding, the DoR table marked out of date
  - commit on `main` (below)
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's answer to `Q-001` is consumed and propagated into the ADR that owns the ladder, the criterion it settles, and the item's Q&A record: a card that has never been answered sits below the bottom rung, so the intervals they enumerated are the ones experienced in order from a new card. WI-0003 returns to `draft` for `refine`'s round 2, which has AC6 settled, R4 and R6 with it, and only the Definition of Ready re-read and the flip of `refinement-qa.md` to `recorded` left to do.

## 2026-08-29T12:31:41Z — refine v0.2.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — the item returned here from `awaiting-answer` when `answer-questions` consumed the stakeholder's reply to `Q-001`. This is round 2, not a fresh refinement and not a send-back from a later stage: `history.md` shows `draft → awaiting-answer` (refine, `resume-to: draft`) then `awaiting-answer → draft` (answer-questions), so round 1's work stands and only what round 1 could not finish is in scope.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (as amended by `answer-questions`), `history.md`, `journal.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (round 1, and the reply recorded into it)
  - `tracker/items/WI-0003/questions/Q-001.md` — the stakeholder's answer and its `## Consequences`
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` (v2) and `ADR-0006-review-state-on-a-card-and-store-version-2.md` (v1)
  - `README.md` — the card-field table and the exit-code table, to confirm AC4 and AC9 name things that exist
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/journal-and-history.md`
- **Decisions:**
  - **Nothing was asked of the stakeholder this round.** Their one question is answered; re-reading the item against the Definition of Ready produced exactly one gap, and the addressee test in step 3 put it at "already answered" rather than "product stake".
  - **AC2 gains the overdue case: the new due date is measured from the day of the review, never from the card's old `due`.** This is the gap round 1 could not see — every criterion it wrote sets the card under test to `due` today, so "3 days after today" and "3 days after the card's old due date" were the same value in every single check and the item never had to choose. R10 demands the combination be *visible*; `## Out of scope` said an overdue card is simply due and said nothing about the interval that follows it. Decided rather than filed, on three agreeing grounds: `ADR-0001` already words both moves from the review ("becomes due **in** 3 days", "next due **one day after the review**"); `WI-0002` already ships it, because `ADR-0006`'s placeholder writes the day after the review whatever the card's previous `due` was, and that is merged and verified; and the alternative — a card ten days overdue coming back overdue or immediately due again — is the penalty for having been away that `## Out of scope` already refuses. Written as an observable check (a card on the 3-day rung with a `due` ten days in the past is, after a right answer, due 7 days after today), and echoed in the catching-up exclusion, which now says no credit as well as no penalty, and in the R10 paragraph.
  - **The criteria preamble now names AC4 as what makes the hand-edits executable.** Six criteria are checked by hand-editing a rung field whose name `plan` has not chosen; AC4 requires `README.md` to carry a row naming that field and its values, so a checker with no context can set every one of them up from the documentation. A clarification of round 1's mechanism, not a new decision.
  - **`refinement-qa.md` flips `agenda` → `recorded`,** and round 1's Definition of Ready table is kept rather than edited, marked as superseded by round 2's. The file is the record of an exchange; rewriting the earlier verdict would destroy the evidence that R4, R6 and R8 ever failed and why.
  - **No criterion was weakened and no override was recorded.** AC6 is the stakeholder's own choice in their own words, not a target reshaped around anything; nothing is built yet, so there is no code for a criterion to have been fitted to.
  - The five design questions stay routed to `plan` in the item's `## Notes`, and the two things `WI-0002` handed forward stay decided as round 1 decided them.
- **Questions raised:** none this round. Round 1 filed `Q-001` (blocking, to the human); it is `answered` and nothing is `[unresolved]` in `artifacts/refinement-qa.md`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - `grep -n "field" README.md` → the card-field table at lines 117–123 and the exit-code table at 138–142, confirming AC4 has a table to add a row to and AC9's exit 1 is the code README already assigns to an unreadable store
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 4 items and 8 documents, 0 errors 0 warnings; re-run by `transition` against the state this move produces)
  - `definition-of-ready` → **pass**, criterion by criterion. R1 pass (frontmatter complete, `[auto]`). R2 pass (role, capability and outcome, unchanged from round 1). R3 pass (AC1–AC9 labelled checkboxes, `[auto]`). **R4 fail → pass**: the only failing criterion was AC6, a placeholder naming `Q-001`; the stakeholder's answer settled it and it now states its own check, and round 2 added AC2's overdue sentence. R5 pass (six exclusions, three of them things a reader would assume were included). **R6 fail → pass**: `Q-001` is `answered`, no question on this item is open (`[auto]`). R7 pass (`depends-on: WI-0002`, which is `done`, `[auto]`). **R8 fail → pass**: `refinement-qa.md` is `status: recorded` and holds both rounds with every answer tagged (`[auto]`). R9 pass (one coherent change — the schedule alone). R10 pass (the item's R10 paragraph enumerates every combination; the overdue card moved this round from "excluded" to "excluded *and* checked"). All ten pass; no override.
  - `criteria-are-decidable` → **pass**, one by one. AC1: `recall add "die Katze" "the cat"` in a scratch store, then read `due` — today's date, and `recall review` presents it. AC2: hand-edit a card onto each rung with `due` today, `printf '\ny\n' | recall review`, read back — 3, 7, 30, 30 days after today with the rung field moved; plus one card with a `due` ten days past, which must give 7 days after today. AC3: same setup, `printf '\nn\n'`, due tomorrow on the bottom rung; then reset `due` and answer right for 3 days. AC4: read `README.md` — the four intervals in order, both moves, and a card-field row for the rung field. AC5: a second `recall list` process and the file on disk. AC6: `recall add` into an empty store then `printf '\ny\n' | recall review` — due tomorrow on the bottom rung; a second right answer gives 3 days. AC7: two due cards, `printf '\ny\nq\n'` and `printf '\ny\n\n'` — the second card's rung and `due` unchanged. AC8: a hand-written store with `due` and `result` but no rung field — `recall list` and `recall review` succeed, the cards read as never answered, the next write carries the rung field. AC9: a store with `due: "tomorrow"` and one with an unlisted rung value — `recall list`, `recall review` and `recall add "a" "b"` each exit 1 with a message on stderr naming the file, and `cmp` shows the file byte-identical. Every one names a command and the verdict that follows.
  - `qa-recorded-verbatim` → **pass** — `refinement-qa.md` is `status: recorded` and holds round 1's question as it was asked, the stakeholder's reply quoted word for word and tagged `[human]`, and every `[assumed]` decision in both rounds with the standing deferral or the precedent it rests on named. Nothing is `[unresolved]`; nothing hesitant was tidied into agreement — round 2 says in terms that round 1 could not see the overdue gap, rather than presenting it as a considered omission.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — AC2 extended with the overdue case; the criteria preamble now names AC4 as what makes the hand-edits executable; the catching-up exclusion says no credit as well as no penalty; the R10 paragraph records the overdue combination as checked rather than only excluded
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; a Round 2 section; a round-2 Definition of Ready table with all ten passing; round 1's table kept and marked superseded
  - commit on `main` (below)
- **Status:** `draft` → `ready`
- **Result:** WI-0003 is Ready. The stakeholder's answer settled AC6, and re-reading the item against the Definition of Ready found one gap the answer had made visible — what an overdue card's next interval is measured from — which `ADR-0001`'s own wording and `WI-0002`'s shipped placeholder both already answered, so it was decided rather than filed. All ten Definition of Ready criteria pass with no override, and the item goes to `plan` with five design questions routed to it and nothing owed to anyone.

## 2026-08-29T12:37:35Z — plan v0.3.1 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` — the only runnable item; `refine` passed it on all ten Definition of Ready criteria with no override
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC9, `## Out of scope`, and the five design questions its `## Notes` routes here), `history.md`, `journal.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — both rounds, and in particular every `[assumed]` entry: the hand-edit mechanism, `README.md` as the documentation AC4 names, AC9's decision, and round 2's overdue-card decision. Nothing is `[unresolved]`
  - `tracker/items/WI-0003/questions/Q-001.md` — the stakeholder's answer and where it landed
  - `docs/architecture/overview.md` (v2), and every ADR: `ADR-0001` (v2 as read, the ladder and the never-answered state), `ADR-0002` (store location and format), `ADR-0003` (stdlib-only commands), `ADR-0004` (schema, write protocol, refuse-not-overwrite), `ADR-0005` (command surface and exit codes), `ADR-0006` (per-card review state, version 2, the placeholder)
  - `tracker/project.yaml` — trunk `main`, and the two declared commands
  - The code: `recall.py` in full (342 lines — `load`, `save`, `add_card`, `due_cards`, `record_result`, `cmd_add`, `cmd_list`, `cmd_review`, `_await_key`, `main`), `tests/support.py`, `tests/test_docs.py`, and the parts of `tests/test_store.py` and `tests/test_review.py` this change invalidates
  - `README.md` — the card-field table, the version paragraph and the exit-code table
- **Decisions:**
  - **A card's rung is stored as the interval in days — `interval`, one of 1/3/7/30, `null` for never answered — not as a rung index.** Route: decided, and recorded as `ADR-0007`; the item routed the representation here. The reason is the reader: `due` is then the review date plus `interval`, so the two scheduling fields check each other by eye, which is most of what AC4 asks a reader to be able to do, and a person hand-editing types the number of days they want rather than consulting a table. Hand-editing is now the documented and only way to move a card, which raises the weight of that. The cost is real and is recorded: changing an existing rung's *value* strands cards holding the old one, because AC9 makes an interval outside the ladder an unreadable store, so retuning becomes a migration. An index would have survived it.
  - **`ADR-0001`'s reversibility note is amended to v3, because this decision made a sentence in it false.** It said "existing cards keep working because a rung index remains a rung index" — a prediction about a representation nobody had chosen. Amended rather than superseded: the ladder itself is untouched, and only the consequence claim changed. This is D12's failure mode caught before it propagated, rather than after — the alternative was to pick the index for the sake of a sentence written before the choice existed.
  - **Store version 3, read 1, 2 and 3.** Route: documented — `ADR-0004` and `ADR-0006` both state that one version means one card shape, and adding `interval` changes the shape. `save` stamps 3; a version-2 card has no `interval` and reads as never answered, which is the same in-place upgrade version 2 used, so there is still no migration to run.
  - **`load` gains two content checks and a normalisation pass.** `due` must be exactly `YYYY-MM-DD` and `interval` must be a ladder value or `null`; both failures are unreadable stores on the existing path. Route: forced by AC9, and the shape of the refusal is documented — `ADR-0004` already makes refuse-not-overwrite the rule. The normalisation (`setdefault` for `interval` and `result`, and deliberately *not* for `due`, whose absence already means "due") is what makes AC8's upgrade fall out of the next write.
  - **`strptime(value, "%Y-%m-%d")` rather than `date.fromisoformat`**, recorded as a reversible assumption. On Python 3.11+ `fromisoformat` accepts `"20260829"` and datetimes; AC9 is about a field a person hand-edits, so the exact shape `README.md` documents is the right strictness. Reversing it is one expression and a test.
  - **The ladder is one constant in `recall.py`, and `next_interval(current, right)` is a pure function.** Route: decided. A store-side table would deliver per-user tuning, which the item excludes. Pure so the ladder's arithmetic can be tested in-process, without a store or a session, in the suite that already does that.
  - **The next due date is the review day plus the new interval, never the card's old `due`.** Route: documented — `ADR-0001` words both moves from the review and round 2 of refinement made it AC2's last sentence. Called out in `## Risks` because it is the one case a plausible implementation gets wrong while passing every other check in the item.
  - **The session is not touched at all.** No output change, no new command, no flag — the item excludes all three, and `record_result` keeping its signature is what confines the change to the scheduling arithmetic.
  - **Nothing was asked of the human.** Every decision came from a document or is a recorded reversible assumption; none is irreversible, and none depends on intent no document records. The stakeholder's one question on this item was answered before planning began.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 55 tests, OK
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 3 documents checked, 0 errors (after fixing one unsourced absolute about `record_result` in ADR-0007's first draft)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0; re-run by `transition` against the state this move produces)
  - `every-criterion-is-addressed` → **pass** — `plan.md`'s `## Acceptance criteria mapping` has a row for each of AC1–AC9, each naming the numbered steps that satisfy it and the specific demonstration, not "tests": AC1→step 5; AC2→1, 2, 6 with a case per rung plus the overdue card; AC3→2, 6; AC4→7, 8; AC5→4, 6; AC6→2, 5, 6; AC7→6; AC8→1, 4; AC9→3. No AC is unmapped and no step exists that no AC maps to.
  - `project-commands-resolved` → **pass** — `tracker/project.yaml` already names both, and both were run in this project during this execution: `python3 -m unittest discover -s tests -t .` exit 0 with 55 tests, and `python3 -m compileall -q -x '[.]claude' .` exit 0. Neither is a command that exits zero without checking anything; `ADR-0003` records why they are the stdlib ones.
  - `decisions-recorded` → **pass** — `plan.md`'s `## Decisions and ADRs` table lists eight choices; five point at `ADR-0007` §Decision, one at the `ADR-0001` v3 amendment, one at the overview's v3 update, and one at `ADR-0006` as the document it follows. The four choices that are neither — the strptime strictness, normalisation on read, the README table row, and where the arithmetic lives — are under `## Assumptions`, each with what reversing it costs.
  - `plan-is-executable-without-you` (advisory) → **pass** — thirteen numbered steps, each naming the file, the change and what is true afterwards; the four interfaces are given as signatures and contracts, with no bodies. The one ordering constraint a reader could get wrong (step 3 before step 6) is stated in `## Risks` rather than left implicit.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0 over `ADR-0007`, `ADR-0001` and `docs/architecture/overview.md`)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0007-scheduling-state-as-an-interval-in-days.md` (new, v1)
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` — v2 → **v3**, the reversibility note corrected and a change-log row added
  - `docs/architecture/overview.md` — v2 → **v3**: `review` now decides when a card comes back and the placeholder sentence is gone, `ADR-0007` in the constraints table, and a new section on the store refusing rather than repairing what it cannot read
  - `tracker/project.yaml` — unchanged; both commands were already resolved and were re-run rather than assumed
  - no scaffolding: `plan.md`'s `## Scaffolding` says `none`, and this execution created no file outside `tracker/` and `docs/`
  - commit on `main` (below)
- **Status:** `ready` → `planned`
- **Result:** WI-0003 is planned. One new card field — `interval`, in days — one new constant, one rewritten `record_result`, a tightening of `load` that closes the defect WI-0002 handed forward, and the documentation and tests that go with them. `ADR-0007` records the representation and what it costs; `ADR-0001` was amended because this decision made one of its consequence claims false, and the overview no longer describes a placeholder that step 6 removes.

## 2026-08-29T12:39:32Z — implement v0.2.2 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next` — the only runnable item on the board; WI-0001 and WI-0002 are `done` and EP-001's `open` has no owner
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC9, `## Out of scope`, and the `## Notes` sections recording what `refine` routed to `plan` and the two things WI-0002 handed forward
  - `tracker/items/WI-0003/artifacts/plan.md` — the thirteen steps, the four interface contracts, `## Acceptance criteria mapping`, `## Assumptions` and `## Risks`
  - `tracker/items/WI-0003/history.md` — five rows, ending `ready` → `planned`; no send-back, so this is a fresh execution rather than a resumption
  - `tracker/items/WI-0003/journal.md` — the `refine` and `plan` entries, in particular `plan`'s decisions about `interval` and store version 3
  - `tracker/items/WI-0003/questions/Q-001.md` — `status: answered`, and its consequences already propagated into `item.md` AC6 and `ADR-0001` v2, which are what I build from rather than the question file
  - `tracker/project.yaml` — trunk `main`, branch prefix `wi/`, commit subject convention, and both declared commands
  - `recall.py` in full — `load`, `save`, `add_card`, `due_cards`, `record_result` and the three commands, so I know which lines the plan's steps 1–6 touch
  - `README.md` — the card-field table, the version paragraph, the sample JSON and the "cannot be read as a card store" sentence, which steps 7 and 8 edit
  - `tests/support.py`, `tests/test_docs.py`, `tests/test_session_parts.py` and the two assertions in `tests/test_store.py` that step 11 names
  - `docs/architecture/adr/ADR-0007-*.md` and `ADR-0001` v3, as the constraints the plan executes but does not restate
- **Decisions:**
  - Work the plan's steps in their given order, and in particular step 3 before step 6, which `## Risks` calls out: `next_interval` may assume `load` has already refused an interval outside the ladder, and implementing it the other way round would turn a validation gap into what looks like a scheduling bug.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → exit 0, branch created from the trunk at 47ac197
- **Gates:**
  - `tests-pass` → **not yet run** — no code has changed; it runs on the branch head at step 7
  - `lint-clean` → **not yet run** — same
  - `workspace-valid` → **not yet run** as a completion gate; `transition` runs it against the state this move produces
  - `every-criterion-has-a-test` → **not yet run** — no test written yet
  - `commits-reference-the-item` → **not yet run** — the branch has no commits yet
  - `claims-are-sourced` → **not yet run** — no document changed yet
- **Artifacts:**
  - branch `wi/WI-0003`, created from `main` at 47ac197, no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0003 has started on `wi/WI-0003`. Nothing is built yet; this entry records what was read and that the branch exists, so an interruption from here leaves a truthful status.

## 2026-08-29T12:46:37Z — implement v0.2.2 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, opened by this skill's own step-3 move; the plan's thirteen steps are executed and the gates pass on the branch head
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC9 and `## Out of scope`; not edited, and no criterion changed
  - `tracker/items/WI-0003/artifacts/plan.md` — the thirteen steps, the four interface contracts, `## Assumptions` and `## Risks`
  - `tracker/items/WI-0003/history.md`, `journal.md` — the `plan` entry's decisions about `interval` and version 3
  - `tracker/items/WI-0003/questions/Q-001.md` — `answered`; its consequences were already in `item.md` AC6 and `ADR-0001`, which is what I built from
  - `recall.py`, `README.md`, `tests/support.py`, `tests/test_store.py`, `tests/test_docs.py`, `tests/test_session_parts.py`
  - `docs/architecture/adr/ADR-0007-scheduling-state-as-an-interval-in-days.md`, `ADR-0001` v3, `ADR-0004`, `ADR-0006`
  - `tracker/project.yaml` — both declared commands, the branch prefix and the commit subject convention
- **Decisions:**
  - **Step 11's list of existing assertions to move was one short, and the third was updated the same way rather than deleted.** `tests/test_store.py::test_a_new_card_is_due_today_with_no_recorded_result` asserts a card's key list exactly, so `interval` moved it too. `plan.md`'s `## Risks` says a third failing test is a signal to re-read the criterion; re-read, it is AC1 and AC6, and it now states both. Not a question: nothing about what the test checks changed, only the version number and the field list this item is defined to move.
  - **`README.md`'s `## Not yet built` section was rewritten, though no step named it.** It claimed the ladder "is not here yet", which step 6 makes false and step 7's new section contradicts. Shipping the two together would have been a documentation defect inside the item's own scope, so it was corrected rather than filed. It now names what is deliberately absent, which is the item's `## Out of scope` list.
  - **The three `RecordResultTest` cases were rewritten rather than left passing.** They passed unchanged — a never-answered card's first right answer does give tomorrow — but their names and docstrings described the placeholder step 6 removes. A test that passes while describing behaviour that no longer exists is worse than one that fails, so they now put the card on the 3-day rung, and a new case covers the never-answered pair explicitly.
  - **The AC9 tests were tightened after first being written.** As first written they asserted only exit 1 and the file being named, and passed against `main`'s `recall.py` — where a version-3 store is refused for its *version*, not for its `due`. They now assert the message names the card, the field and the value. Recorded because the first version was a gate that would have passed without checking the thing it was for.
  - **Nothing was escalated.** No decision arose that the plan does not make: every deviation above is inside its latitude — how, not what — and none changes an interface, contradicts an ADR, or alters behaviour a user would notice that no criterion covers.
  - **Nothing neighbouring was fixed.** `due_cards`' empty-string sort for a missing `due`, and `cmd_review` saving the whole document per card, were both read while working and both left as WI-0002 delivered them.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → exit 0, **82 tests, OK** (55 before this item; run after each of the plan's steps and last on the branch head)
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 2 commit(s) on main..wi/WI-0003 name WI-0003" (run before the report commit; three commits now)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings
  - `git show main:recall.py > recall.py` then `python3 -m unittest tests.test_schedule` → **16 of 18 fail**; `recall.py` restored and the suite re-run → OK. This is the every-criterion-has-a-test gate checked in the direction that matters
  - By hand on 2026-08-29, against `RECALL_FILE=/tmp/wi3/demo/cards.json`: `recall add "die Katze" "the cat"` → `Added card 1.` with `"due": "2026-08-29"`, `"interval": null`; `printf '\ny\n' | recall review` → `1 2026-08-30`; `due` reset to today and reviewed right again → `3 2026-09-01`
  - By hand, against a store whose card has `"due": "tomorrow"`: `recall list`, `recall review` and `recall add a b` each → exit 1 with `recall: /tmp/wi3/demo/bad.json is not a readable card store: card 1 has a 'due' of 'tomorrow', which is not a YYYY-MM-DD date`, and `cmp` → byte-identical
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 82 tests OK, on branch head `5f8aae2` — after the last code change and before the report-only commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '[.]claude' .`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings; re-run by `transition` against the state this move produces)
  - `every-criterion-has-a-test` → **pass**, each named in `impl-report.md`'s evidence table. AC1 `NewCardTest.test_a_new_card_is_due_the_day_it_is_added_and_is_presented`; AC2 `RightAnswerTest` ×3 (subTests 1→3, 3→7, 7→30; the top rung; the overdue card) plus `NextIntervalTest`; AC3 `WrongAnswerTest` ×2 (subTests from all four rungs); AC4 `test_docs.py::test_the_readme_names_the_ladder_and_the_field_that_carries_it`, which asserts the four waits appear **in order**; AC5 `PersistenceTest`, across four separate processes; AC6 `NeverAnsweredCardTest` ×3, one asserting the sequence is exactly [1, 3, 7, 30]; AC7 `UnreachedCardTest` ×2; AC8 `OlderStoreTest` ×3; AC9 `UnreadableSchedulingValueTest` ×3 × three commands, each asserting the message names the card, the field and the value, and the file's bytes unchanged. No AC rests on reading the code. Checked in the removal direction: with `main`'s `recall.py` in place, 16 of the 18 tests in `test_schedule.py` fail — the two that do not are AC1's regression over WI-0001 and AC8's read-without-error, both of which held before this item and whose siblings do fail
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0003 wi/WI-0003`, exit 0)
  - `no-unplanned-scope` (advisory) → **pass** — `git diff main..wi/WI-0003` read hunk by hunk against the plan: `recall.py`'s six hunks are steps 1–6, `README.md`'s are steps 7–8 plus the `## Not yet built` correction recorded above, and the test changes are steps 9–12 plus the `RecordResultTest` rewrite recorded above. No hunk is untraceable to a step or an AC
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0; it reports no documents changed, because `plan` wrote `ADR-0007` and amended `ADR-0001` before implementation began and both are already on `main`)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - `recall.py` — `LADDER`, `STORE_VERSION` 3, `READABLE_VERSIONS` (1, 2, 3), `_is_date`, `next_interval`, `load`'s two checks and normalisation pass, `add_card`, `record_result`
  - `README.md` — the "When a card comes back" section, the `interval` row, version 3 in the sample and the version paragraph, the unreadable-store sentence, and `## Not yet built`
  - `tests/test_schedule.py` (new, 18 tests), `tests/test_session_parts.py` (+`NextIntervalTest`, `RecordResultTest` rewritten), `tests/test_docs.py` (+1), `tests/test_store.py` (three assertions moved to version 3)
  - branch `wi/WI-0003`, commits `ddc6280..3785da2` — `main..wi/WI-0003` is `ddc6280`, `5f8aae2`, `3785da2`
- **Status:** `in-progress` → `verifying`
- **Result:** WI-0003 is implemented on `wi/WI-0003` and goes to `verify`. A card now climbs 1 → 3 → 7 → 30 days on right answers and drops back to one day on a wrong one, measured from the day of the review; a card never answered starts below the ladder, so its first right answer brings it back tomorrow. `load` refuses a `due` that is not a date and an `interval` that is not on the ladder, which closes the defect WI-0002 handed forward. Four deviations from the plan are recorded in `impl-report.md`, all of them how rather than what.

## 2026-08-29T12:53:30Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next` — the only runnable item; `implement` reported all six of its hard gates passing on the branch head
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC9 and `## Out of scope`, read **first** and used to derive what would settle each criterion before anything else was opened
  - `tracker/items/WI-0003/artifacts/plan.md` — the thirteen steps, the interface contracts, and in particular `## Assumptions`' choice of `strptime` over `date.fromisoformat`, which turns out to be where AC9 fails
  - `tracker/items/WI-0003/artifacts/impl-report.md` — read after the criteria; its claims were checked, and it is cited as evidence nowhere in `verify-report.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — consulted on AC9's wording, which is not contested
  - `tracker/items/WI-0003/history.md`, `journal.md`, `questions/Q-001.md` (`answered`)
  - the code at branch head **eb4cc23c96de0247a70520432aaed4b23b182cac** on `wi/WI-0003` — `recall.py`, `README.md` (via `git show HEAD:README.md`), and `git diff main..HEAD`
  - `tracker/project.yaml` — both gate commands
- **Decisions:**
  - **Both defects are send-backs, not bug items.** Step 7's test is whether an acceptance criterion of *this* item says the behaviour should be different. AC9 says a rung value `README.md` does not list must exit 1 (D1: `interval: true` exits 0 and is taken as the 1-day rung), and that no command silently drops a card (D2: `due: "2026-8-9"` is accepted and the card is never due again). Both are AC9. Filing them as bugs would let the item close with its own criterion unmet.
  - **D2 in particular is not WI-0002's bug to carry.** The same *shape* of defect was handed forward by WI-0002's review, and this item's AC9 is the criterion written to close it. The behaviour is unmet here, so it belongs to this item and `found-in: WI-0002` would misattribute it.
  - **AC4 passes despite a real coverage gap.** Removing the `interval` row from `README.md`'s card-field table leaves all 82 tests green, because the only test asserts the name appears somewhere and the prose section mentions it too. AC4 is about the documentation, and the row is present and was read, so the verdict is `pass`; the gap is recorded under `## Test sensitivity check` for the same pass that fixes AC9. Marking AC4 `fail` for a missing test would be judging the tests rather than the criterion.
  - **AC1–AC8 are ticked, though the item is going back.** Each was demonstrated here. The report states the ticks are against `eb4cc23` and that the AC9 fix touches `load`, so the next verification must re-run all nine rather than trusting them.
  - **Nothing was repaired.** The two defects have obvious one-line fixes — `load` already guards the identical `bool`/`int` trap on `number` a few lines above D1's check — and both were left alone. A verifier who fixes the code has nobody checking the repair.
  - **Nothing was escalated.** No criterion was ambiguous: AC9's general clause and its list of accepted values in `README.md` settle both cases without needing the architect.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `eb4cc23c96de0247a70520432aaed4b23b182cac` on `wi/WI-0003`
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 82 tests in 5.507s / OK`
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings
  - AC1: `recall add "die Katze" "the cat"` → `Added card 1.`, store `"due": "2026-08-29"`, `"interval": null`; `printf '\nq\n' | recall review` printed the card. exit 0
  - AC2: four hand-written stores, one per rung, each `printf '\ny\n' | recall review` → `3 2026-09-01`, `7 2026-09-05`, `30 2026-09-28`, `30 2026-09-28`; plus a card on the 3-day rung with `due: "2026-08-19"` → `7 2026-09-05`, measured from today
  - AC3: `printf '\nn\n' | recall review` from each of the four rungs → `1 2026-08-30 wrong` every time; then `due` reset and answered right → `3 2026-09-01`
  - AC4: `git show HEAD:README.md` — the "When a card comes back" section and the `interval` row read in full; a due date predicted from that text alone (interval 30, five days overdue, answered right → 30 and 2026-09-28) then confirmed against the tool
  - AC5: four processes over one store → file on disk held `interval: 7`; `recall list` exit 0; a later review climbed to `30 2026-09-28`
  - AC6: `recall add` then four reviews with `due` reset between → `None`, then 1, 3, 7, 30; a wrong answer on a fresh card → `1 2026-08-30 wrong`
  - AC7: `printf '\ny\nq\n' | recall review` and `printf '\ny\n\n' | recall review`, and additionally `printf '\ny\n'` — card 2's dict equal to its pre-run value in all three
  - AC8: a version-2 store with no `interval` → `recall list` exit 0 and the file untouched; `recall review` exit 0; the file afterwards version 3 with `interval` on both cards, the reviewed one at `1`
  - AC9: nine invocations (`list`, `review`, `add a b` × `due: "tomorrow"`, `interval: 5`) → exit 1, empty stdout, message naming file and card, `cmp` byte-identical each time. Then four unlisted values: `interval: "3"` refused, `due: "2026-13-45"` refused, **`interval: true` accepted (exit 0, promoted to rung 3)**, **`due: "2026-8-9"` accepted (exit 0, `Nothing is due today.` on a card twenty days overdue)**
  - `python3 -c "print(True in (1,3,7,30,None))"` → `True`; `python3 -c "print('2026-8-9' <= '2026-08-29')"` → `False` — the two causes, confirmed directly
  - Mutation runs, each disabling one behaviour and restoring it: placeholder `record_result` → 19 failures + 1 error; `next_interval` always bottom rung → 17 failures; `add_card` without the field → 2 failures + 1 error; `due` check removed → 6 failures; `interval` check removed → 3 failures; normalisation removed → 2 failures; README ladder section removed → 1 failure; **README `interval` row removed → OK, nothing failed**. Suite green and `git status` clean after every restore
  - `git diff main..HEAD` read hunk by hunk against `plan.md` and `impl-report.md`'s four declared deviations
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 82 tests OK, run here on `eb4cc23`)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '[.]claude' .`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings; re-run by `transition`)
  - `every-criterion-independently-checked` → **pass** — `verify-report.md`'s criteria table gives, for each of AC1–AC9, the command this skill ran and the output it produced. Each check was derived from the criterion before `impl-report.md` was read, and the stores were set up from `README.md`'s field names alone, which is the setup AC4 is supposed to make possible. No row cites the implementation report
  - `negative-cases-exercised` → **pass** — AC9's two named cases triggered across all three commands with `cmp` before and after; four further unlisted values triggered, two of which are D1 and D2; plus the in-ladder boundaries: top rung right, bottom rung wrong, never-answered wrong, and cards 5 and 10 days overdue
  - `tests-would-fail-without-the-change` (advisory) → **pass, with one gap recorded** — seven of eight disabled behaviours were caught by the suite; removing `README.md`'s `interval` table row was not, which is the AC4 coverage gap in `verify-report.md`
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` (new) — `Verified-commit: eb4cc23c96de0247a70520432aaed4b23b182cac`
  - `tracker/items/WI-0003/item.md` — AC1 to AC8 ticked; AC9 left unticked
  - no bug item filed — both defects are this item's own AC9
  - commit on `wi/WI-0003` (below)
- **Status:** `verifying` → `in-progress`
- **Result:** WI-0003 goes back to `in-progress` on AC9. Its two named cases work, but `interval: true` is accepted as the 1-day rung (`True == 1` in Python, so the membership test lets it through) and `due: "2026-8-9"` is accepted while sorting above every real date, so the card is listed, never presented, and never reported — which is `WI-0002`'s handed-forward defect in a second spelling, and the one AC9 exists to close. AC1 to AC8 pass on evidence gathered here. A coverage gap on AC4's card-field row is recorded for the same pass.

## 2026-08-29T12:57:13Z — implement v0.2.2 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, dispatched by `next` — the item was sent back by `verify` at 12:53:30Z with AC9 failing; the last history row is that send-back, so `verify-report.md` was read before anything else
- **Inputs read:**
  - `tracker/items/WI-0003/history.md` — the last row is `verifying` → `in-progress`, so this is a resumption against a defect, not a fresh execution
  - `tracker/items/WI-0003/artifacts/verify-report.md` — read **first**, in particular `## Defects found` (D1 and D2 with their reproductions) and the AC4 coverage gap under `## Test sensitivity check`
  - `tracker/items/WI-0003/item.md` — AC9's wording, and the eight ticked criteria I must not disturb; not edited
  - `tracker/items/WI-0003/artifacts/plan.md` — `## Assumptions`, where the `strptime` strictness is declared reversible at the cost of "one expression in `load` and a test"
  - `tracker/items/WI-0003/artifacts/impl-report.md` (pass 1), `journal.md`
  - `docs/architecture/adr/ADR-0007-scheduling-state-as-an-interval-in-days.md` — it requires `due` to be "exactly `YYYY-MM-DD`" and `interval` a ladder value or null, and names no parsing function, so the fix brings the code to the ADR rather than away from it
  - the branch: `git log main..HEAD` — five commits from pass 1 and `verify`; `recall.py` and `README.md` at `eb4cc23`
- **Decisions:**
  - **Both defects were fixed in `load` and nowhere else.** D1 gets an `isinstance(..., bool)` test before the membership test, which is the idiom `load` already uses for `number` — the verifier named it, and following it keeps one pattern in the file rather than two. D2 makes `_is_date` require the round trip, so the only accepted `due` is the canonical zero-padded form.
  - **Reversing the plan's `strptime` assumption was not escalated.** `plan.md` records it under `## Assumptions` as reversible, states the cost as one expression and a test, and says nothing is stored differently. Verification falsified it against AC9. Changing a pre-declared reversible assumption on the evidence that falsified it is inside the plan's latitude — how, not what — and it changes no interface, contradicts no ADR, and alters no behaviour a criterion does not cover.
  - **`due_cards`' string comparison was left alone.** It is the reason an unpadded date is dangerous, but it is behaviour `WI-0002` delivered and no criterion of this item asks for it to change. AC9 asks for the value to be refused, which is what `load` now does. Changing it here would be the neighbouring fix this skill is told not to make.
  - **`README.md` and `ADR-0007` were not touched.** Both already promise what the code now does — `README.md` says a `due` that is not `YYYY-MM-DD` and an `interval` outside the four values make the file unreadable, and that "Nothing is silently dropped or repaired". Those sentences were false at `eb4cc23` and are true at `5d9c323`. The verifier asked specifically that the last one not be softened to match the old behaviour, and it was not.
  - **The AC4 coverage gap was closed in the same pass.** `verify` recorded it as a gap rather than a criterion failure and said it was worth tightening while the item was back here. `test_docs.py` now asserts the card-field row as a row — exactly one line beginning with the field name in a table cell, naming all five values — rather than the field name appearing anywhere in the file.
  - **No acceptance criterion was edited, and the eight ticks were left in place.** `verify-report.md` states they are against `eb4cc23` and that the next verification must re-run all nine; that is the verifier's call to make, not mine.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline main..HEAD` → five commits from pass 1 and `verify`; branch reconciled before any change
  - `python3 -m unittest discover -s tests -t .` → exit 0, **Ran 87 tests, OK** (82 after pass 1)
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 6 commit(s) on main..wi/WI-0003 name WI-0003"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 9 documents, 0 errors 0 warnings
  - `git show eb4cc23:recall.py > recall.py`, then `python3 -m unittest tests.test_schedule` → `test_a_rung_of_json_true_stops_the_tool` and `test_an_unpadded_due_stops_the_tool_rather_than_dropping_the_card` **both fail**; `recall.py` restored and the suite re-run → OK
  - `README.md`'s `| \`interval\` |` row renamed, then `python3 -m unittest tests.test_docs` → `test_the_readme_card_field_table_has_a_row_for_the_rung_field` **fails**, and no other test does; `README.md` restored
  - The verifier's own reproductions re-run by hand. D1: `recall list`, `recall review`, `recall add a b` against a card with `"interval": true` → each exit **1**, `recall: /tmp/v3/D1fix/cards.json is not a readable card store: card 1 has an 'interval' of True, and the ladder is 1, 3, 7, 30 or null`, `cmp` byte-identical. D2: the same three against `"due": "2026-8-9"` → each exit **1**, `... card 1 has a 'due' of '2026-8-9', which is not a YYYY-MM-DD date`, `cmp` byte-identical
  - Regression by hand: `recall add "die Katze" "the cat"` → `Added card 1.`; `printf '\ny\n' | recall review` → `Reviewed 1, right 1.`; the card reads `1 2026-08-30`, which is AC6's first rung
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 87 tests OK, on branch head `5d9c323` after the last code change)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '[.]claude' .`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings; re-run by `transition`)
  - `every-criterion-has-a-test` → **pass** — AC1–AC8's evidence is pass 1's and their code is byte-identical; nothing outside `load` changed. AC9 gains four tests: `test_a_rung_of_json_true_stops_the_tool`, `test_a_rung_of_json_false_stops_the_tool`, `test_an_unpadded_due_stops_the_tool_rather_than_dropping_the_card` and `test_every_padded_date_the_readme_documents_is_still_accepted` (the fix must not start refusing well-formed dates: `2026-01-02`, `2026-12-31`, `2026-02-28`, today). AC4 gains the card-field-row assertion. Each was confirmed to fail with its behaviour removed, as the commands above record
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, all 6 commits)
  - `no-unplanned-scope` (advisory) → **pass** — pass 2's diff is three hunks in `recall.py` (`_is_date`'s round trip, the `bool` guard, and the comment on each) and two test files. Every hunk traces to D1, D2 or the AC4 gap named in the send-back. `due_cards`, `next_interval`, `record_result`, `add_card`, every command, `README.md` and `ADR-0007` are untouched
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0)
- **Artifacts:**
  - `recall.py` — `_is_date` requires the round trip; the `interval` check rejects `bool` before testing membership
  - `tests/test_schedule.py` — four new tests in `UnreadableSchedulingValueTest`
  - `tests/test_docs.py` — `test_the_readme_card_field_table_has_a_row_for_the_rung_field`
  - `tracker/items/WI-0003/artifacts/impl-report.md` — a `## Second pass — the send-back on AC9` section, and a header naming both passes and their commits
  - branch `wi/WI-0003`, head `5d9c32329fefeaa6ed51fd75d6cd47d1e4ca5a09`; `main..wi/WI-0003` is six commits
  - no ADR written or amended, no bug item filed, no acceptance criterion edited
- **Status:** `in-progress` → `verifying`
- **Result:** Both defects the send-back named are closed and go back to `verify`. A JSON `true` in `interval` is refused rather than read as the 1-day rung, and an unpadded `due` is refused rather than sorting the card out of every review — which is the `WI-0002` defect AC9 exists to close, in the spelling that got past pass 1. The AC4 coverage gap `verify` recorded is closed in the same pass. 87 tests pass on the branch head; `verify-report.md` says the next verification must re-run all nine criteria rather than trusting pass 1's eight ticks, and that is what should happen.

## 2026-08-29T13:07:29Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying` — the second verification, dispatched by `next`. `implement`
  returned the item here at `f841f09` after fixing the two AC9 defects the first verification
  found.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the nine acceptance criteria, read before anything else
  - `tracker/items/WI-0003/history.md` — the send-back and the return, and why
  - `tracker/items/WI-0003/artifacts/plan.md` — the thirteen steps and the two reversible
    assumptions, for the diff read
  - `tracker/items/WI-0003/artifacts/impl-report.md` — both passes, including `## Second pass`
  - `tracker/items/WI-0003/artifacts/verify-report.md` — the first verification's own report,
    for what it declared unverified
  - `tracker/project.yaml` — the test and lint commands
  - `README.md` — read as a checker with no context would, to derive the AC2/AC3/AC5/AC6/AC7/AC9
    setups from it rather than from the code
  - the branch head `wi/WI-0003` at `f841f096374450ebb8c4fbb2688382c860322651`, and
    `git diff main..HEAD` on `recall.py` and `README.md`
- **Decisions:**
  - **Re-ran all nine criteria, not the one that had failed.** The first verification ticked
    AC1–AC8 against `eb4cc23` and said the AC9 fix touches `load`, which every command goes
    through. Its ticks were therefore treated as unverified and each was re-established from a
    command run here. Nothing in this report cites `impl-report.md` as evidence.
  - **Derived the setups from `README.md` rather than from `recall.py`.** AC4's whole purpose is
    that a checker with no context can put a card on a rung from the documentation; using the
    code instead would have made AC4 unfalsifiable while appearing to pass.
  - **Probed AC9 well past its named values, and answered the question the first pass left
    open.** 30 malformed stores, attacking wrong type, wrong shape, wrong position in the file,
    and equal-but-not-identical to a ladder value. Both earlier defects stay closed and nothing
    new was found — except the class below.
  - **`interval: 1.0` and `3.0` (JSON floats) are accepted, and this is recorded as a pass, not
    a defect.** They reach `next_interval` and behave as the 1-day and 3-day rungs; the file is
    rewritten with the integer. AC9 refuses "a value `README.md` does not list", and in JSON
    `1.0` and `1` denote the same number, which the README lists. The contrast with the earlier
    D1 is the reasoning: JSON `true` is a boolean, not a number of days, and was silently
    reinterpreted as a rung nobody wrote; `1.0` *is* the rung that was written, the card is not
    dropped, and the schedule is identical. The argument is in `verify-report.md` in full so it
    can be disagreed with rather than merely relied on.
  - **Two things looked at and deliberately not filed as bugs:** `due_cards` still compares `due`
    as a string (correct for every value `load` now admits — checked at `"0999-01-01"` and
    `"9999-12-31"`), and `cmd_review` still saves the whole document per card (unchanged from
    WI-0002, untouched by any criterion here). Neither is a defect in delivered behaviour, so
    neither is a bug item and neither is a send-back.
  - **No criterion was judged ambiguous.** Every one of the nine had a command that settled it.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 87 tests`, `OK`
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 9 documents,
    0 errors 0 warnings
  - `git rev-parse HEAD` → `f841f096374450ebb8c4fbb2688382c860322651`; `git status --short` →
    empty, before and after the mutation runs
  - AC1: `recall add "die Katze" "the cat"` → `Added card 1.`, exit 0; `cat cards.json` →
    `"due": "2026-08-29"`, `"interval": null`; `printf '\ny\n' | recall review` → exit 0, card
    presented, `Reviewed 1, right 1.`
  - AC2: four hand-edited stores (rungs 1, 3, 7, 30) each `printf '\ny\n' | recall review` →
    `3/2026-09-01`, `7/2026-09-05`, `30/2026-09-28`, `30/2026-09-28`; a fifth on rung 3 with
    `due` at `2026-08-19` → `7/2026-09-05`
  - AC3: five stores (`null`, 1, 3, 7, 30) each `printf '\nn\n' | recall review` → all
    `interval 1`, `due 2026-08-30`, `result wrong`; then `due` reset to today and
    `printf '\ny\n' | recall review` → `interval 3`, `due 2026-09-01`
  - AC4: `grep -n` on `README.md` → line 95 the ladder, 97 and 99 the two bullets, 146 the
    `interval` row under `### What each card records` at 137
  - AC5: four processes against one store → `interval 7 due 2026-09-05` on disk; `recall list`
    exit 0; `recall review` → `Nothing is due today.`; after a hand-edit, `interval 30 due
    2026-09-28`
  - AC6: `recall add` then five reviews with `due` reset between → 1, 3, 7, 30, 30; a fresh card
    answered `n` → `interval 1`, `due 2026-08-30`, `result wrong`
  - AC7: `printf '\ny\nq\n' | recall review` and `printf '\ny\n\n' | recall review`, two cards
    each → card 1 `30/2026-09-28/right`, card 2 `7/2026-08-29/None`, both times
  - AC8: a `"version": 2` store with no `interval` → `recall list` exit 0 and
    `grep -c interval` → 0; after `printf '\ny\n' | recall review`, `"version": 3` with
    `interval 1` on the reviewed card and `interval null` on the card that was never due
  - AC9: 30 malformed stores × `recall list`, `recall review`, `recall add a b`, each with
    `cmp -s` against a pre-run copy. Every refusal → exit 1, empty stdout, stderr naming the
    file, the card, the field and the value, file byte-identical. Includes `due: "tomorrow"`,
    `interval: 5`, `due: "2026-8-9"`, `interval: true`, `interval: false`, five wrong types for
    `due`, ten malformed `due` strings, six non-ladder `interval` values, and a fault on the
    second card rather than the first
  - Test sensitivity: nine mutations of `recall.py` and `README.md`, each followed by the full
    suite and then restored — see the gate bullet and `verify-report.md` for the table
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 87 tests OK,
    run on the branch head after the last change)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '[.]claude' .`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 0 errors 0 warnings)
  - `every-criterion-independently-checked` → **pass** (each of the nine has a command run in
    this execution and its actual output in `verify-report.md`; AC1–AC8's earlier ticks were
    re-earned rather than carried over)
  - `negative-cases-exercised` → **pass** (30 deliberately malformed stores for AC9 across three
    commands each; plus AC7's two abandoned sessions, AC8's pre-version store, AC2's top rung and
    overdue card, AC3 from every rung including the never-answered one)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (nine mutations, one per
    criterion, each making a named test fail: AC1 `NewCardTest`, AC2 `RightAnswerTest`, AC3
    `WrongAnswerTest`, AC4 both the table-row and the ladder tests in `test_docs`, AC5
    `PersistenceTest`, AC6 `NeverAnsweredCardTest`, AC7 `test_review`'s `ac5` test, AC8
    `OlderStoreTest` and `test_store`, AC9 both `UnreadableSchedulingValueTest` cases. All backed
    out; suite returned to 87 passing and the tree to clean)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` — rewritten as this pass's report, with
    the first verification condensed into an appendix pointing at commit `9cda720` for its full
    text
  - `tracker/items/WI-0003/item.md` — AC9 ticked; all nine now ticked, each on evidence gathered
    here
  - the commit of these workspace files
- **Status:** `verifying` → `in-review`
- **Result:** WI-0003 passes verification at `f841f09`. All nine criteria were re-run
  independently and all nine hold; the two defects the first pass found are closed and neither
  reappeared under a much wider probe. No defect was found, so nothing was sent back and no bug
  item was filed. One accepted-value class — JSON floats equal to a ladder rung — is recorded
  with the reasoning for calling it a pass, so a reviewer can take a different view visibly.

## 2026-08-29T13:12:14Z — review-close v0.5.0 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review` — dispatched by `next` after the second verification passed all
  nine criteria at `f841f09`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the nine criteria and their tick state
  - `tracker/items/WI-0003/history.md` — ten rows, checked for a gap and against the item's status
  - `tracker/items/WI-0003/journal.md` — all ten entries, read in full
  - `tracker/items/WI-0003/artifacts/plan.md`, including `## Assumptions` and `## Risks`
  - `tracker/items/WI-0003/artifacts/impl-report.md`, both passes and both `## What I did not do`
  - `tracker/items/WI-0003/artifacts/verify-report.md`, including `## Not verified, and why`
  - `tracker/items/WI-0003/questions/Q-001.md` — the answer and the four files its
    `## Consequences` names, each opened
  - `git diff main..wi/WI-0003` — the diff itself, hunk by hunk, across `recall.py`, `README.md`
    and four test files
  - `docs/architecture/adr/ADR-0001-fixed-interval-ladder.md` (v3),
    `docs/architecture/adr/ADR-0007-scheduling-state-as-an-interval-in-days.md` (v1),
    `docs/architecture/overview.md` (v3), and `recall.py` itself, for the D12 audit
  - `tracker/project.yaml` — the trunk, the branch prefix and the commands
- **Decisions:**
  - **Accept.** All twelve Definition of Done criteria pass with their own evidence; the table is
    in `review.md` and is the evidence for the `definition-of-done` gate.
  - **Every hunk maps to a plan step, a criterion or a declared deviation.** The mapping table is
    in `review.md` `## What I examined`. Nothing unrequested, nothing contradicting an ADR.
  - **D12 was decided from the citations, not from the prose.** Nine absolute claims across
    `ADR-0007`, `ADR-0001` and `overview.md` were each checked by opening the code they cite. Two
    are worth naming: `ADR-0007`'s "a `due` must be exactly `YYYY-MM-DD`" and "an `interval` must
    be one of the ladder's values or `null`" were **false at `eb4cc23`** and are true now — the
    pass-2 fixes made the documents true rather than needing the documents changed, which is why
    no doc edit was required and why that had to be checked rather than assumed.
  - **Pass 2's reversal of a `plan.md` assumption needed no ADR.** `plan.md` recorded the
    `strptime` strictness under `## Assumptions` as reversible at the cost of "one expression in
    `load` and a test", and that is exactly what it cost. A declared reversible assumption
    falsified by verification is the mechanism working, not a design change.
  - **Five gaps accepted rather than sent back**, and all five copied into `item.md` `## Notes`
    so they survive the close: the JSON-float acceptance (`interval: 1.0` read as the 1-day
    rung), no observation across a real change of date, timezones unprobed, AC9's probe being a
    search rather than a proof, and no large or concurrent stores. The float case is the one that
    could be argued the other way; the verification's reasoning and my agreement with it are both
    on the record so that a later reader can disagree and file against it.
  - **Two things looked at and not filed as bugs**, agreeing with both reports: `due_cards`
    compares `due` as a string (correct for every value `load` now admits — the edges were
    checked at `"0999-01-01"` and `"9999-12-31"`), and `cmd_review` saves the whole document per
    card (unchanged from WI-0002, no criterion here touches it). Neither is a defect in delivered
    behaviour, so neither is a bug item.
  - **The send-back and the re-verification were the right calls.** The first verification's two
    defects were this item's own AC9, so a send-back rather than bug items; the second re-ran all
    nine criteria rather than only the failed one, which is what a fix inside `load` demands.
  - **Merge order: trial, close, then merge.** The trial merge ran in a **detached** worktree so
    it could not fast-forward the real `main`; `main` was confirmed unmoved afterwards. The item
    was closed while the branch was still unmerged, because `check-commit-refs` reads
    `main..wi/WI-0003` and merging first empties that range.
  - **The engagement was not ended here.** `engagement-state EP-001` reports `active — still in
    flight: WI-0003` at the time of this review, because WI-0003 is not yet `done`. Ending EP-001
    is a separate dispatch, and this execution is not it.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → exit 0,
    "verified at f841f096; wi/WI-0003 has moved to e9332d69 but only the record changed (5
    file(s) under tracker/ or docs/), so the verification still covers the code"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 9
    commit(s) on main..wi/WI-0003 name WI-0003"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors 0
    warnings (no documents changed on this branch — the three were written by `plan` and are
    already on `main`)
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0003` → exit 0, "WI-0003 is a
    'work-item', not an epic"
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → exit 0, "EP-001 active — still
    in flight: WI-0003"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 9 documents, 0
    errors 0 warnings
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 87 tests`, `OK`
  - `python3 -m compileall -q -x '[.]claude' .` → exit 0
  - `git rev-parse main` → `47ac197ded714b61f8587bf45c06f52e5f5baba3` (before the trial)
  - `git worktree add --detach /tmp/v3b/trial main` → detached at `47ac197`
  - `git -C /tmp/v3b/trial merge --no-ff wi/WI-0003` → clean, trial head
    `512528863c5b92df5cf34991e4ab25be957b79ee`
  - `python3 -m unittest discover -s tests -t .` inside the trial worktree → exit 0, `Ran 87
    tests`, `OK` — the merge result, not the branch
  - `git worktree remove --force /tmp/v3b/trial`; `git rev-parse main` →
    `47ac197ded714b61f8587bf45c06f52e5f5baba3`, unchanged
  - `git diff main..wi/WI-0003` → read hunk by hunk; `git worktree list` → only the main checkout
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each with its own result and evidence, in `review.md`
    `## Definition of Done`; no single overall verdict was substituted)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness`, exit 0 — run, not
    inferred from how small the last commits looked; the five commits after `f841f09` are all
    under `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, 9 commits)
  - `tests-pass-on-the-merge-result` → **pass** (87 tests OK inside the detached trial worktree,
    on the merge commit — not on the branch head)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and
    `git log --grep WI-0003` alone: **what and why** from `plan.md` and `ADR-0007`; **who decided
    what** from ten journal entries against ten history rows, each naming its skill and persona;
    **what was asked and answered** from `Q-001`, whose `## Consequences` names four files that
    all carry the change; **what verification found** from both verify reports, including the
    rejection, its two reproductions, and the appendix pointing at `9cda720` for the first
    report's full text
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0003` exit 0: WI-0003 is a
    work-item, and the termination gate applies to an engagement's ending only)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` — what was examined, the D1–D12 table, the
    findings, the five accepted gaps, the verdict
  - `tracker/items/WI-0003/item.md` — closed `done` / `delivered`, and `## Notes` gains "What was
    not checked", carrying the five accepted gaps forward past the close
  - the merge of `wi/WI-0003` into `main`, made after this transition
  - the commit of these workspace files
- **Status:** `in-review` → `done`
- **Result:** WI-0003 is accepted and closed as delivered. The interval ladder is in `main`: a
  right answer moves a card 1 → 3 → 7 → 30 days and a wrong one returns it to the bottom rung,
  measured from the day of the review; a never-answered card sits below the ladder, as the
  stakeholder chose in `Q-001`; the schedule persists at store version 3 and older stores upgrade
  in place; and an unreadable scheduling value stops the tool instead of silently dropping the
  card. Five gaps were accepted and written into the item. EP-001's last work item is done, so the
  engagement can now reach rest — ending it is a separate dispatch.
