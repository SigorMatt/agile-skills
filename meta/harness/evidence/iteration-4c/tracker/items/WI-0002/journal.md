# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T11:07:51Z — intake v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was created by that execution, so the trigger is the creation itself rather than a status.
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement, verbatim)
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution)
  - `tracker/items/WI-0001/item.md` (written earlier in this same execution, to set the boundary between the two items)
- **Decisions:**
  - See `EP-001`'s entry of the same execution for how the work was split and why this is one of two items.
  - "Review due cards daily" and "simple spaced repetition" are kept in **one** item rather than split into "show due cards" and "reschedule them". Rationale: a session that shows due cards but never updates the schedule delivers nothing observable on its own — the next day would be identical — so the two are one deliverable, not two. Splitting them would have bought three extra pipeline round trips for no user-visible increment.
  - Priority `high` and `depends-on: WI-0001`: derived from the stakeholder's own ordering ("add cards, review due cards daily") and from the fact that a review session with no cards is untestable. This is derivation, not a guess about their preference.
  - AC3 and AC4 are stated as "a single stated rule" and "sooner than" rather than with numbers. Rationale: the rule itself is `EP-001/Q-002` and is the stakeholder's to choose; inventing "1, 3, 7, 14, 30" here would have made the criterion look decidable while recording a requirement nobody asked for.
  - The grading scale (how many buttons, what they are called) is deliberately **not** asked at intake. It is downstream of `EP-001/Q-002` — SM-2 implies four or six grades, a Leitner ladder implies two — so asking now would produce an answer that has to be re-asked. Recorded in `## Notes` for `refine`.
- **Questions raised:** none on this item; four were raised on `EP-001` (`Q-001`–`Q-004`), three of which this item's criteria depend on.
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --title "Review the cards due today and reschedule them by how well they went" --epic EP-001 --priority high --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` reported 0 errors after this execution's journals and the epic transition; see `EP-001`'s entry for the run)
  - `epic-has-success-measures` → **pass** (judged on `EP-001`; see that entry for the evidence — this gate is not an item-level check)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation` → exit 0; the elicitation is `EP-001/Q-004`)
  - `items-are-separable` (advisory) → **pass** — it is second in order, depends on `WI-0001`, and delivers something on its own: a person with cards can do a daily review and see the schedule change.
  - `no-solution-in-the-problem` (advisory) → **pass** — no algorithm is named in the story or criteria. The three algorithms appear in `EP-001/Q-002` as options offered to the stakeholder, which is where a choice they have not made belongs.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/history.md`, `tracker/items/WI-0002/journal.md` (new, by `scripts/new-item`)
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The second work item under EP-001: the daily review session and the spacing rule that reschedules each card. Its core behaviour is unspecified on purpose — `EP-001/Q-002` and `EP-001/Q-003` are exactly the decisions it needs and neither is ours to make.

## 2026-08-30T11:19:08Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** `answer-questions` consuming the stakeholder's answers to `EP-001/Q-001` to `EP-001/Q-004`; this item is named in the `## Consequences` of all four
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (answers)
  - `tracker/items/WI-0002/item.md` (the criteria as intake left them)
  - `tracker/items/EP-001/item.md` (success measures)
  - `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md` (written by this execution)
- **Decisions:**
  - Replaced AC3 and AC4 — "records how well it went … a single stated rule" and "a card answered as gone badly comes back sooner" — with AC4, AC5 and AC6, which name the two outcomes, the four intervals, the top-rung behaviour and the reset. Rationale: intake's wording was written to be replaced; the stakeholder has now stated the rule, and a criterion that says "a single stated rule" cannot be decided by anyone.
  - Split the due-date behaviour into AC2 (the date comparison), AC3 (a missed day is still due, unpenalised) and AC7 (a second session the same day). Rationale: the stakeholder made three separate statements in `EP-001/Q-003` and each is separately checkable; folding them into one criterion would let two of them pass untested.
  - Added AC9 — quitting part-way keeps the answers already given. Rationale: it was already an epic success measure, and the stakeholder named losing progress as one of two things that would make the tool a failure (`EP-001/Q-004`). It belongs on the item that can lose it.
  - Left AC2 as the literal "no cap" reading and said so in `## Notes`, rather than writing a session cap or a session length into a criterion. Rationale: `EP-001/Q-005` asks the stakeholder which of two of their own statements wins; writing either into a criterion now would settle it on their behalf, which is the move `spec/question.md` §2 refuses.
  - Renamed the item from "…reschedule them by how well they went" to "…reschedule them on the fixed ladder". Rationale: "how well they went" describes a difficulty scale the stakeholder explicitly refused.
  - Recorded the loss of per-review history in `## Out of scope` rather than leaving it implicit. Rationale: the ladder stores only a rung and a date, so a future adaptive algorithm has nothing to learn from; ADR-0002 states what that costs.
- **Questions raised:** none on this item (`EP-001/Q-005` was filed on the epic; it constrains AC2 and is recorded in `## Notes`)
- **Commands:** none
- **Gates:**
  - `answer-is-propagated` → **pass** (this file is named in all four questions' `## Consequences`, and each named change is in it: AC1 the terminal command, AC4–AC6 the ladder, AC2/AC3/AC7 the due dates, AC9 the part-way quit)
  - `answered-from-the-record` → **pass** (`## Notes` quotes the two answers the criteria were written from; the inferred parts cite ADR-0002)
  - `escalation-is-justified` → **pass by reference** (the escalation is `EP-001/Q-005`, on the epic, stating condition 1 of `spec/question.md` §4 — intent no document records)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item EP-001`, exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported on the EP-001 entry for this execution)
  - `item-resumed-correctly` → **skipped** (this item was never suspended; it stays at `draft`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (title changed; six criteria became nine and every one rewritten; out-of-scope list extended; `## Notes` replaced)
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The item now states the ladder, the due-date comparison and the two outcomes as criteria a reader with a terminal can decide, with one criterion — how many cards a session shows — explicitly parked on `EP-001/Q-005` rather than guessed.

## 2026-08-30T11:27:41Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** no status change of its own — this entry records an acceptance-criteria amendment
  made while consuming `EP-001/Q-005`, whose answer is about what a review session shows
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` (the stakeholder's answer)
  - `tracker/items/WI-0002/item.md`, `history.md`
  - `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md` (v1),
    `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md` (v1, written by the same
    execution)
- **Decisions:**
  - **AC2 amended, and why it is not a target being reshaped.** It already said a card is offered
    when its due date is today or earlier; it now also says every such card is offered, with no cap
    on how many a session may contain. That is the stakeholder's own answer — *"Don't cap it at
    some arbitrary number"* — made explicit rather than left to the reader of `## Notes`. The item
    is at `draft`, so its criteria are not frozen, and the amendment widens what must be true
    rather than narrowing it.
  - **AC10 added** — the session states how many cards it is about to offer, before the first one,
    and the number is checkable against the stored file. From *"I'd rather see the honest number of
    cards waiting"*. Written as a count rather than a count-and-duration, per `ADR-0003`.
  - **AC11 added** — an explicit way to stop at any card, which exits without an error. AC9 already
    said what stopping must preserve; nothing said stopping was a supported action at all, and the
    stakeholder asked for one: *"let me quit partway through without losing anything"*. AC11 names
    AC9 as its preservation obligation rather than restating it, so the two cannot drift.
  - **`## Notes` rewritten.** The paragraph warning `refine` not to settle the session-size
    question alone is replaced by the answer that settled it, and by an instruction not to add a
    session-length criterion — because the stakeholder traded that bound for visibility, and
    adding one later would contradict the answer rather than sharpen it.
  - Did not touch the remaining `## Notes` items for `refine` (what the person types, and the order
    due cards are offered in). Ordering is now slightly more visible with a stated count, but
    nothing in the answer decides it and inventing a decision here is not this skill's job.
- **Cross-answer check:** EP-001/Q-005 checked against EP-001/Q-001, EP-001/Q-002, EP-001/Q-003 and
  EP-001/Q-004 — all compatible, no conflict declared; the full check is on the question file and
  on EP-001's journal entry of the same execution.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item EP-001` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 1 warning
    (`commands.test` null, `plan`'s to fill)
- **Gates:**
  - `answer-is-propagated` → **pass** — `tracker/items/WI-0002/item.md`, named in Q-005's
    `## Consequences`, carries the amended AC2 and the new AC10 and AC11
  - `answered-from-the-record` → **pass** — every amendment traces to a sentence of the
    stakeholder's answer, quoted above and in `ADR-0003`
  - `escalation-is-justified` → **skipped** — nothing escalated from this item
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0)
  - `item-resumed-correctly` → **skipped** — this item was never suspended; it stays at `draft`
  - `a-deferral-is-not-an-answer` → **skipped** — no deferral on this item
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — AC2 amended; AC10 and AC11 added; `## Notes` rewritten
- **Status:** `draft` → `draft` (unchanged)
- **Result:** WI-0002 now states what a review session offers, that it says how many, and that
  stopping part-way is supported — the three things the stakeholder's answer to `EP-001/Q-005`
  decided. The item stays at `draft` for `refine`.

## 2026-08-30T12:23:36Z — refine v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` — the highest-ranked runnable item once WI-0001 closed and its `depends-on` was satisfied. A fresh draft, not a send-back: `history.md` holds one row, the creation by `intake`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1 to AC11 and `## Notes` as `answer-questions` left them
  - `tracker/items/WI-0002/history.md` (1 row) and `journal.md` (3 entries, in full) — the stakeholder's verbatim answers from `intake` and from the two `answer-questions` executions, so that nothing already answered was asked again
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md`, `Q-004.md`, `Q-005.md` — the four answers this item's criteria are written from
  - `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`, `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`, `ADR-0006`, `ADR-0007`
  - `docs/architecture/overview.md` (v2) — the entry point, the card file's shape and the `review` subcommand's place in it
  - `tracker/items/WI-0001/item.md` and `artifacts/refinement-qa.md` — how the same deferral was applied to the sibling item, and what `rung: 0` means on a card this session will meet
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Nothing was put to the stakeholder, and that is this execution's main judgement.** Every failing Definition of Ready criterion was either already answered by them or fell inside the standing delegation *"As for how it's actually built — whatever you think is best"* (`EP-001/Q-004`). Each decision is a key, a sort key or a message — reversible in one line — and each is recorded `[assumed]` in `artifacts/refinement-qa.md` naming the deferral, never as something they said. The test applied to each was `refine`'s own: would the answer be the same whoever the stakeholder was.
  - **R4 repaired on the three criteria that named no action.** AC1 said the back is revealed *"after the person asks for it"*, AC4 said *"the person records right or wrong"*, and AC11 said there is *"an explicit way to stop"* — three criteria `verify` could not decide, because `verify` cannot ask anyone what to type. AC1 now names Enter, AC4 names `y` and `n`, AC11 names `q` and the input stream ending. Words, numbers and raw-terminal keys were the alternatives; the Q&A records why each was rejected, including that raw terminal input cannot be driven by a pipe, which would leave AC9 and AC11 untestable.
  - **AC12 added — the order due cards are offered in — and it was the closest call here.** Order is something the person sees daily, so it was tested against the product question rather than assumed into the deferral. It was settled from their own words in `EP-001/Q-005`: they asked for the honest count and for the tool not to *"quietly decide which ones I don't get to see today"*, and AC2 and AC10 turn that into a hand-check against the stored file. A hand-check has to be repeatable, so the order is a function of the file — oldest due date first, ties in file order. Shuffling is recorded in the Q&A as the option not taken, with its real argument (order effects) and the reason it loses (it makes the hand-check unrepeatable).
  - **AC13 added — unrecognised input re-asks for the same card**, and never counts as right, wrong or a quit. Nothing said what happens to a stray key, and the failure it prevents is recording an answer the person did not give.
  - **AC8 widened to one case, not three.** No due cards, no cards at all and no card file now behave identically: a message, exit zero, and nothing written. The missing-file case is what anyone meets first on a clean machine and nothing stated it. `review` deliberately does not create the card file the way `add` does — a command that writes a file merely by being run is a surprise on a machine someone is only trying out.
  - **AC5 and AC6 now spell out all five rungs**, including rung 0, which is how WI-0001 writes a newly added card and therefore the state of every card at its first review. `ADR-0002` says "moves up one rung" and `ADR-0007` defines rung 0 as never-answered; the criteria restate the walk rather than leaving the first review to be inferred. This is a restatement of recorded decisions, not a new one.
  - **AC14 added — an unparsable card file stops the session before the first card.** It is the refusal WI-0001's `add` already makes on the same file (`ADR-0007`), stated here so that the case is specified rather than discovered part-way through a session.
  - **AC3, AC4 and AC9 sharpened into observations.** AC3 says the new date is counted from the day of the review and not from the date the card was due — the only reading under which *"nothing lost, nothing punished"* (`EP-001/Q-003`) is true. AC4 requires each answer to be in the card file before the next card's front is printed, which is the only mechanism that satisfies AC9's kill-at-a-prompt case. AC9 now names both ways a session can end.
  - **Four entries added to `## Out of scope`:** undoing an answer, re-reviewing a card inside the same session, editing a card's sides during a review, and — already there — capping the session. The first three are things a reader could reasonably assume are included.
  - **No session-length or session-size bound was added**, though the stakeholder called a review over a couple of minutes a failure (`EP-001/Q-004`). They traded that bound for the honest count in `EP-001/Q-005`, and `## Notes` instructs `refine` not to add one. Adding it would contradict their answer rather than sharpen it.
  - **R9: not split.** Fourteen criteria describe one command holding one loop over one list, writing one file. Showing cards without recording answers delivers nothing usable; recording answers without showing cards is not a session.
  - **No Definition of Ready override.** No criterion was waived and the stakeholder was not asked to waive one.
- **Cross-answer check:** the four answers this item rests on — `EP-001/Q-002` (binary grading and the 1/3/7/30 ladder), `EP-001/Q-003` (due is today or earlier; a missed day is unpunished; a second session shows only what is still due), `EP-001/Q-004` (the build delegation, and losing progress as a failure), `EP-001/Q-005` (no cap, the honest count, the clean quit) — were each checked against every decision recorded above. **No conflict**, so compatibility is cited rather than a question filed: AC12's ordering sequences the due cards without withholding any, which is what `Q-005` asked about; AC4 and AC9 make `Q-004`'s failure mode observable; AC3's counting from the review day is the reading that makes `Q-003` true. Nothing of theirs was overtaken, and no document, criterion or vision statement was edited to accommodate a newer answer. `scripts/lint-answers --item WI-0002` → exit 0.
- **Questions raised:** none. Six decisions are recorded as `Q1` to `Q6` in `artifacts/refinement-qa.md` with their options and the reason each was ours rather than theirs; none was filed as a question artifact, because filing one would have put a category they already answered back to them. Nothing is left `[unresolved]`
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 10 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors 0 warnings)
  - `definition-of-ready` → **pass**, criterion by criterion: **R1 pass** (frontmatter complete, `type`, `epic`, `priority`, `depends-on` set); **R2 pass** (role, capability and a "so that" naming the outcome); **R3 pass** (AC1 to AC14, labelled, checkboxes); **R4 fail as found → pass** (AC1, AC4 and AC11 named no action anyone could perform; each now names the key, and AC3, AC8 and AC9 were sharpened into observations); **R5 pass** (nine entries in `## Out of scope`, four added here); **R6 pass** (no question is open on this item); **R7 pass** (`depends-on: WI-0001`, which is `done` and merged into `main`); **R8 fail as found → pass** (`artifacts/refinement-qa.md` did not exist; it now exists at `status: recorded`, with all six decisions, their options and their `[assumed]` tags); **R9 pass** (one subcommand, one loop, one file — the rationale is in the Q&A); **R10 fail as found → pass** (unrecognised input is AC13, an empty deck and a missing file are AC8, a rung-0 card is AC5 and AC6, two cards due the same day are AC12, an unparsable file is AC14, and the prompt wording, the rung display and the argument-count case are named in `## Notes` as deliberately unconstrained by `refine`)
  - `criteria-are-decidable` → **pass** — each of AC1 to AC14 was taken in turn and the settling observation stated: AC1 a piped Enter and what standard output does and does not contain; AC2, AC10 and AC12 a seeded card file compared by hand against what the session offers and in what order; AC3, AC5 and AC6 the rung and due lines before and after an answer, per rung; AC4 the card file read part-way through a session; AC7 two sessions on the same day; AC8 an empty deck and an absent file, with the file byte-identical or still absent; AC9 an answer, then a kill at the next prompt; AC11 `q` at each prompt and an input stream that ends; AC13 a stray key followed by a valid answer, with the same card asked again; AC14 a hand-mangled file. No criterion contains an unmeasurable adjective
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0; the substantive check is the `**Cross-answer check:**` bullet above and the `## Cross-answer check` section of the Q&A, which name all four prior answers by ID)
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` is at `status: recorded` and quotes `EP-001/Q-003`, `Q-004` and `Q-005` verbatim with their IDs. Every decision this execution took is tagged `[assumed]` and names the deferral it rests on; no `[human]` tag claims the stakeholder said something in this round, because they were not asked anything in it
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: recorded`) — the agenda as a DoR table, six decisions with their options and the reason each was ours, the cross-answer check, and what is left open and for whom
  - `tracker/items/WI-0002/item.md` — AC1, AC3, AC4, AC5, AC6, AC8, AC9 and AC11 rewritten; AC12, AC13 and AC14 added; four entries added to `## Out of scope`; a `### Refined 2026-08-30` section added to `## Notes` recording every decision, what was deliberately left unconstrained, and what was deliberately not added
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. The three criteria that named actions nobody could perform now name the keys, the five gaps R10 found are stated, and the item is decidable by someone with a terminal and no context — which matters here because the next three skills cannot ask anyone anything. No question went to the stakeholder: every gap was inside the delegation they gave or already answered by them, and the Q&A records which, one decision at a time.

## 2026-08-30T12:28:29Z — plan v0.4.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` — the highest-ranked runnable item at priority rank 2, WI-0003 ranking below it
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1 to AC14, the contract this plan is written against
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — all six decisions, every one tagged `[assumed]`, and the reason each was ours; nothing is `[unresolved]`, so this design stands on no soft ground `refine` left behind
  - `tracker/items/WI-0002/history.md` and `journal.md` — a first plan, not a re-plan: the item reached `ready` from `draft` with no rejection behind it
  - `docs/architecture/overview.md` (v2) — and in particular its sentence deferring the ladder's home to this item
  - `docs/architecture/adr/` — `ADR-0001` (single-user command line), `ADR-0002` (binary grading, the 1/3/7/30 ladder, the top rung, the due comparison), `ADR-0003` (no cap, the stated count, the clean quit), `ADR-0004` (the file is the tool's to rewrite), `ADR-0006` (Python 3, standard library only, the gate commands), `ADR-0007` (the file's format and `rung` 0 to 4), `ADR-0008` (where the file lives and how it is written)
  - the code this change touches, read in full rather than inferred: `recall/cli.py` (`main()`, `_parser()`, `add()`, `_side_error()`), `recall/store.py` (`Card`, `card_file_path()`, `load()`, `save()`, `_parse()`, `_render()`), `recall/__main__.py`, `tests/test_add.py` and `tests/test_store.py` for how the existing tests drive the tool
  - `tracker/items/WI-0001/artifacts/review.md` — its finding 2, that `main()` calls `add()` unconditionally, which this item is the first to break
  - `tracker/project.yaml`, `.claude/agile-skills/spec/work-item.md`, `.claude/agile-skills/spec/dor-dod.md`
- **Decisions:**
  - **Where the ladder rule lives — `recall/schedule.py`, pure functions given the date by their caller. [documented, then decided]** The overview named this item as the one that would decide it, so the decision was owed here rather than invented. Three options were weighed with their costs — in the review loop, on `store.Card`, or a third module — and the deciding argument is testability of the rule itself: a function handed its date settles all ten rung transitions of AC5 and AC6 without a clock, a card file or a subprocess, where the other two options make every such question a session test. Recorded as `ADR-0009`, with the evidence that would show it was one seam too many.
  - **`due_positions()` returns positions in the card list, not cards. [documented]** Forced by WI-0001's AC6: two cards may legitimately share a front side, so a session that matched by value could write back the wrong one. This is the one interface choice in the plan that is not obvious from the criteria, and it is in `## Approach` where it can be argued with.
  - **Every answer is written before the next card is printed, by rewriting the whole file. [documented]** AC4 and AC9 decide this between them — a session that saved at the end would lose everything to the kill AC9 names — so no ADR was written for it; the mechanism is `ADR-0008`'s existing temporary-file-and-rename write, unchanged.
  - **`main()` now dispatches on the parsed subcommand. [documented]** WI-0001's review recorded this as a trap for exactly this item: left alone, `python3 -m recall review` would silently run `add`. Step 4 names the line and step 4's observable result requires WI-0001's criteria to still hold afterwards.
  - **Five reversible assumptions, all recorded rather than buried. [assumed]** Line-based input so `y` is `y` and Enter; whitespace stripped and case ignored; `today` taken once at the start of the session; prompt wording left to `implement` within what the criteria require it to contain; and no re-read of the card file mid-session. Each names what reversing it costs — a body, a line, a call site, a string, a reload — and each rests on the standing delegation `EP-001/Q-004`.
  - **Nothing was put to the stakeholder. [not asked]** No decision here is irreversible: the expensive commitment in this product is the card file's format, and this item adds no field to it. Every rule it applies was decided with them already, and `refine` settled what they type. Asking again would spend their attention on a category they have twice delegated.
  - **The overview was updated because the shape changed**, not as a courtesy: two modules became three, and `review` moved from a named future subcommand to a planned one. v2 → v3 with a change-log row.
  - **No ADR was written for the choices with no alternative worth naming** — the exit codes, the streams, the save mechanism — which are either WI-0001's conventions or forced by a criterion. An ADR trail padded with non-decisions hides the real ones.
  - **`tracker/project.yaml` needed nothing.** `commands.test` and `commands.lint` were filled in by WI-0001's plan and both were run again by this execution before being relied on.
- **Cross-answer check:** this execution recorded no new human answer and relied on four already consumed — `EP-001/Q-002` (binary grading and the ladder), `EP-001/Q-003` (the due comparison and the unpunished missed day), `EP-001/Q-004` (the build delegation), `EP-001/Q-005` (no cap, the honest count, the clean quit). Each was checked against every design decision above and against the two documents this execution edited: `ADR-0009` decides where a rule lives and changes no rule, so it touches none of them; the overview's new text describes the same three behaviours those answers fixed. **No conflict, and nothing of theirs was overtaken** — so neither move in `ADR-0008` §3 was needed beyond citing compatibility, and no sentence citing an answer of theirs was edited. `scripts/lint-answers --uncommitted` → exit 0 over 9 consumed answers with 2 documents in the window.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests in 1.157s`, `OK` — the command recorded in `project.yaml`, run before being relied on
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 2 documents in 2 uncommitted paths (it failed twice first: an absolute claim about `recall/schedule.py` with no citation, then a citation to `plan.md` before `plan.md` existed — both repaired in place)
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 9 consumed human answers, 2 paths in the claim window
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 11 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors 0 warnings, 11 documents — one more than before, `ADR-0009`)
  - `every-criterion-is-addressed` → **pass** — `plan.md`'s `## Acceptance criteria mapping` has one row for each of AC1 to AC14, each naming the plan steps that satisfy it and a specific named test with what it asserts, never "tests". The three that carry the most design are AC4 (the file read part-way through a session, which is what proves the write did not wait for the end), AC9 (a `SIGKILL` at a prompt) and AC12 (the same session run twice against a restored file, comparing the sequence of fronts)
  - `project-commands-resolved` → **pass** — `commands.test` and `commands.lint` are non-null and both were run by this execution against the current tree, exit 0 each; `commands.build` stays null, honestly, because there is nothing to build [src: ADR-0006]
  - `decisions-recorded` → **pass** — the one decision that outlives this item is `ADR-0009`, with three options and their costs, the decision, the consequences and its reversibility; the five reversible ones are in `## Assumptions` with what each reversal costs; and `## Decisions and ADRs` maps every decision to where it is recorded and which branch of the preference order it came from
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` → exit 0; the substantive check is the bullet above, naming all four prior answers by ID)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` → exit 0 over *"2 document(s) in 2 uncommitted path(s) under docs"* — `ADR-0009` and the overview, which are the two this execution wrote)
  - `plan-is-executable-without-you` → **pass, advisory, and it found something.** The plan was read back as a stranger would read it, step by step, asking at each one whether it demands a decision the plan does not make. Step 3 said `_ask()` "re-asks the same prompt" after an unrecognised key, while AC13's demonstration asserts the card's front appears **twice** before the back is shown — a developer could satisfy the sentence with a bare re-prompt and fail the test. `## Approach` and steps 3 and 5 now say that a re-ask reprints the whole prompt including the card's text, and that the card's front and back are what the caller passes as the prompt. No other step required a decision it does not make. This gate is advisory and was not in this skill's `At a glance` hard-gate list; `run-gate` named it, and the fix above is what it bought
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — eight steps, a fourteen-row criteria mapping, five assumptions, five risks and the out-of-scope list
  - `docs/architecture/adr/ADR-0009-the-ladder-rule-lives-in-its-own-module.md` (new, v1) — the overview's deferred decision, made
  - `docs/architecture/overview.md` v2 → v3 — `## The pieces` now describes three modules and two seams; `review` is a planned subcommand rather than a named one
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. One new module holds the ladder as pure functions, the command layer gains the session and finally dispatches on its subcommand, and every answer reaches the card file before the next card is printed — which is what makes AC9's kill survivable. Every one of AC1 to AC14 has a step and a named demonstration; nothing went to the stakeholder, because nothing here is irreversible and the rules were all decided with them already.

## 2026-08-30T12:31:28Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC14, the out-of-scope list, and the two `refine` notes)
  - `tracker/items/WI-0002/artifacts/plan.md` (eight steps and the AC mapping table)
  - `tracker/items/WI-0002/history.md` (three rows; no send-back, so this is a fresh start)
  - `tracker/items/WI-0002/questions/` — the directory does not exist; no question was ever filed
    on this item
  - `tracker/project.yaml` (`commands.test`, `commands.lint`, `conventions.branch-prefix`,
    `conventions.commit-subject`)
  - `docs/architecture/adr/ADR-0009-the-ladder-rule-lives-in-its-own-module.md`
  - `recall/store.py` and `recall/cli.py` — the two modules WI-0001 built, read to see what
    `Card`, `load`, `save`, `card_file_path` and `main()` actually offer
  - `tests/test_add.py` — the subprocess harness this item's session tests will follow
- **Decisions:**
  - Started fresh rather than reconciling: `git branch` showed `main` and `wi/WI-0001` only, the
    item was at `planned` (no branch by definition), and the history's last row is `plan`'s. There
    is no partial work to preserve.
  - Branched `wi/WI-0002` from `main` at `45f8d03`, which is the commit `plan` wrote — so the plan
    and the ADR it rests on are on the branch's first parent.
- **Cross-answer check:** none — this entry edits no document, so no claim sourced to a
  stakeholder answer has been touched yet. The closing entry answers this properly.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no code has been written; the closing entry runs it
    on the branch head)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **pass** (`validate-workspace`, run by this transition; 0 errors)
  - `every-criterion-has-a-test` → **skipped** (no test exists yet)
  - `commits-reference-the-item` → **skipped** (the branch has no commit of its own yet)
  - `no-unplanned-scope` (advisory) → **skipped** (no diff yet)
  - `cross-answer-consistency` → **skipped** (no document changed yet)
  - `claims-are-sourced` → **skipped** (no document changed yet)
- **Artifacts:**
  - branch `wi/WI-0002`, created from `main` at `45f8d03`; no commit on it yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started on `wi/WI-0002`. Nothing is built yet; the
  entry exists so that an interruption from here leaves a truthful status.

## 2026-08-30T12:39:58Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, this execution's own opening transition
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1 to AC14, `## Out of scope`, and both `refine` notes
  - `tracker/items/WI-0002/artifacts/plan.md` — the eight steps, the AC mapping table, the five
    assumptions and the four risks
  - `tracker/items/WI-0002/history.md` — three rows, no send-back
  - `tracker/project.yaml` — the test and lint commands and the two conventions
  - `docs/architecture/adr/ADR-0009-the-ladder-rule-lives-in-its-own-module.md`
  - `docs/architecture/overview.md` — read in full for the D12 check reported below
  - `.claude/agile-skills/spec/doc-header.md` §4b, §4a and §5, and
    `.claude/agile-skills/spec/dor-dod.md` D7 and D12 — read to settle whether this skill could
    repair the overview itself
  - `recall/store.py`, `recall/cli.py`, `tests/test_add.py` — the two modules and the subprocess
    harness WI-0001 left
- **Decisions:**
  - **`_ask()` derives its refusal wording from `accepted` instead of taking it as an argument.**
    `_named(("", "q"))` is `Enter, q`. Rationale: the plan fixed the signature at two arguments and
    still required the refusal to say what the prompt takes; deriving it means a prompt cannot name
    a key it does not accept, which is a class of bug rather than a wording choice.
  - **The outcome prompt prints the back only, never the front again.** Rationale: the plan says
    so, and it is also what makes AC13's evidence readable — "the front appears exactly twice
    before the back" is a real check only if the outcome prompt does not reprint the front.
  - **The card file is read back in `tests/test_review.py` by a parser written in the test module,
    not by `recall.store`.** Rationale: a test that decodes the file with the code under test
    cannot detect a change to the format; WI-0001's tests read bytes for the same reason.
  - **Two mutations were run against the finished code, and reverted.** Rationale: self-check 1
    asks whether each test would fail if the behaviour were removed, and the honest way to answer
    is to remove it. Moving `store.save()` to the end of the session broke four tests; unsorting
    `due_positions()` broke four more. Both are listed under `**Commands:**`.
  - **`docs/architecture/overview.md` was left untouched, and the staleness handed to
    `review-close`.** Three of its sentences — `review` "is planned", "WI-0002 is the item that
    puts it in", and an opening line dating the document to before WI-0001 was built — are false
    against this branch. `spec/doc-header.md` §5 says `implement` does not write to `docs/`, and
    this skill's contract lists no document among its outputs, so repairing them here would be the
    circular edit that rule prevents. Recorded in `impl-report.md` under `## What I did not do` as
    a D7 and D12 handover rather than left for someone to notice.
  - **Not escalated as a question.** The overview is stale, not wrong about a decision: no
    behaviour is in doubt, nothing this item builds depends on the answer, and D7 and D12 already
    own it at the close. Filing a blocking question would have stopped the pipeline for a version
    bump the Definition of Done demands anyway.
- **Cross-answer check:** none. This execution edited no file under `docs/`, so no claim carrying
  `[src: <ITEM>/Q-nnn>]` was touched, and `lint-answers --changed-since main` exited 0 over a
  window it correctly reports as empty. The one sentence in this area sourced to the stakeholder —
  `overview.md`'s card-file location, from `WI-0001 AC5` — is unaffected by this item, which adds
  no field and changes no path.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 37 tests after step 2 (schedule)
  - `git commit` (schedule module and its tests) → exit 0, `0aba73d`
  - `python3 -m recall review` by hand against a seeded deck, three times → the nothing-due case,
    a two-card session answered `y` then a stray key then `n`, and the resulting card file read
    back; all as the criteria describe
  - `python3 -m unittest discover -s tests -t . -q` → exit 1 first run, 1 failure
    (`test_nothing_due_says_so_and_writes_nothing`: the missing-file sub-test ran after a sub-test
    that had created the file). Fixed in the test, not in the tool
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 60 tests, `OK`
  - mutation 1 — `store.save()` moved out of the loop to a single call at the end →
    `test_each_answer_is_written_before_the_next_card`,
    `test_quitting_keeps_the_answers_already_given`,
    `test_a_kill_at_a_prompt_keeps_the_answers_already_given` and
    `test_a_second_session_the_same_day_offers_only_what_is_still_due` all failed; reverted
  - mutation 2 — `due_positions()` returning its list unsorted →
    `test_due_cards_are_offered_oldest_first`, `test_the_order_is_the_same_twice`,
    `test_the_oldest_due_date_comes_first` and
    `test_ties_keep_file_order_among_earlier_and_later_dates` all failed; reverted
  - `python3 -m compileall -q recall tests` → exit 0
  - `git commit` (the session and its tests) → exit 0, `e595079`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `git diff main..HEAD` → read hunk by hunk for the scope gate
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q`, exit 0, 60 tests
    `OK`, run on the branch head `e595079` after the last change; WI-0001's 26 among them)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0, same head)
  - `workspace-valid` → **pass** (`validate-workspace`, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (AC1 to AC14 each name a test function in
    `impl-report.md`'s evidence table; every one asserts on the tool's output or on the bytes of
    the card file, none on the shape of the code. Two mutations confirm eight of them bite)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002`, exit 0,
    "all 2 commit(s) on main..wi/WI-0002 name WI-0002")
  - `no-unplanned-scope` (advisory) → **pass** (`git diff main..HEAD` is 686 added lines in four
    files: `recall/schedule.py` is steps 1 and 2, the `cli.py` hunks are steps 3, 4 and 5, and the
    two test files are steps 6 and 7. No hunk touches `add()`, `store.py`, or anything outside the
    plan)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main`, exit 0, and the
    `**Cross-answer check:**` bullet above states the reading rather than resting on the window)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0. The window is
    empty — this branch changed no document — so `lint-claims --all` was run as well and also
    exited 0, and `overview.md` was read by hand; what that read found is under `**Decisions:**`)
- **Artifacts:**
  - `recall/schedule.py` (new), `recall/cli.py` (updated)
  - `tests/test_schedule.py` (new, 11 tests), `tests/test_review.py` (new, 23 tests)
  - `tracker/items/WI-0002/artifacts/impl-report.md` (new)
  - branch `wi/WI-0002`, commits `0aba73d..e595079` — two, both naming WI-0002
- **Status:** `in-progress` → `verifying`
- **Result:** `review` is built: every due card oldest first, the back hidden until Enter, `y` and
  `n` the only outcomes, each answer on disk before the next card is printed, and `q` or the end of
  the input stream stopping cleanly at either prompt. All eight hard and advisory gates pass on the
  branch head. One thing is handed on rather than done: `docs/architecture/overview.md` still says
  `review` is planned, and `implement` may not repair a document — that is a D7 and D12 obligation
  on `review-close`, recorded in `impl-report.md`.

## 2026-08-30T12:48:17Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1 to AC14, read **before** the implementation report, and
    what would settle each one derived from the criterion's own sentence
  - `tracker/items/WI-0002/history.md` — five rows; `implement` made both of the last two
  - `tracker/items/WI-0002/artifacts/plan.md` — the eight steps, the AC mapping and the five
    assumptions, read for step 6's diff-against-the-plan
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria, as the claim to be
    checked rather than the evidence
  - `tracker/items/WI-0001/item.md` — its eight criteria, read against the new `main()` dispatch
  - `tracker/project.yaml` — the test and lint commands
  - the code at branch head `c706d837b0a8a6555b201858efabc68c3ac720b6`: `recall/schedule.py`,
    `recall/cli.py`, and `git diff main..HEAD` in full
- **Decisions:**
  - **AC13 was re-run at rung 2 after the first attempt proved undecidable.** The obvious seed is a
    new card, but at rung 0 a right answer and a wrong answer both give rung 1 due today+1 — so the
    criterion's "never counted as right, as wrong, or as a quit" cannot be told apart on that seed.
    Re-seeded at rung 2, where right gives 3/+7 and wrong gives 1/+1, and ran it both ways. The
    first run is reported as what it was.
  - **`Y ` accepted as `y` is not a defect.** AC13 covers input the prompt does *not* accept, and
    `Y ` normalises into one it does. It is `plan.md`'s assumption 2, recorded before the code
    existed. No send-back, no bug.
  - **The `[1/4]` counter and the closing `Done.` line are not unrequested scope.** No criterion
    requires them and none forbids them; wording is `implement`'s under `plan.md` assumption 4, and
    AC10's required count is its own separate line printed before the first card.
  - **`overview.md`'s staleness is not a defect of this item, and not mine to fix.** `review` "is
    planned" is false against this branch, but no criterion of WI-0002 mentions the overview, and
    `spec/doc-header.md` §5 names `verify` alongside `implement` as skills that do not write to
    `docs/`. `implement` declared it; this report carries it forward to `review-close` as a D7 and
    D12 obligation. Neither a send-back (it fails no criterion) nor a bug (no delivered behaviour
    is wrong).
  - **The criterion-about-criteria gate is vacuous here, and the read was done anyway.** None of
    AC1 to AC14 has a criterion as its subject. Because `main()`'s dispatch changed under WI-0001,
    its eight criteria were read one by one against the new behaviour and six of them re-executed
    by hand. The non-intersection is stated in the report in those words — nothing executable runs
    `add` and `review` together — and a covering case was **added by hand** rather than waived:
    three cards written by `add`, then offered by `review` in the same deck.
  - **One mutant survived and is reported as equivalent, not as a gap.** `card.rung + 1 if
    card.rung < 3 else 4` agrees with `min(card.rung + 1, 4)` on every rung 0 to 4, so it changes
    no behaviour. Two mutations that genuinely change the cap were then run, and both failed tests.
    Recorded rather than quietly dropped.
- **Questions raised:** none — no criterion turned out ambiguous once AC13's seed was corrected
- **Commands:**
  - `git rev-parse HEAD` → `c706d837b0a8a6555b201858efabc68c3ac720b6`; `git status --short` → no
    source modification
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 60 tests in 2.702s`, `OK`
  - `python3 -m compileall -q recall tests` → exit 0
  - AC1 — `printf 'q\n' | RECALL_CARD_FILE=… python3 -m recall review` → exit 0, and
    `… | grep -c BACKWORD` → `0`; then `printf '\nq\n' | …` → the back printed
  - AC2, AC10, AC12 — a six-card deck answered through → `4 cards due.`, `[1/4] CARD-overdue3`,
    `[2/4] CARD-overdue1`, `[3/4] CARD-today-a`, `[4/4] CARD-today-b`; `grep -n 'front:\|due:'` on
    the seed for the hand count; the file restored byte-for-byte and re-run → `SAME ORDER TWICE`
  - AC3, AC4, AC9 — a `subprocess.Popen` session driven from a short Python driver: file read from
    outside the running process before the answer (`digest unchanged: True`, `rungs: ['2','1','1']`),
    after the answer (`alive: True  rungs: ['3','1','1']`), then `Popen.kill()` → `returncode: -9`
    with the answer still on disk
  - AC5 — five cards, one per rung, all answered `y` → rungs 1,2,3,4,4 at +1,+3,+7,+30,+30
  - AC6 — the same deck answered `n` → five records at `rung: 1  due: 2026-08-31`
  - AC7 — three sessions the same day → `3 cards due.` / `2 cards due.` / `Nothing is due.`
  - AC8 — three seeds (due later, header-only, absent) → exit 0, `Nothing is due.`, `sha256sum`
    identical before and after, and no file created in the third
  - AC11 — four runs (`q\n`, `\nq\n`, empty, `\n`) → exit 0, stderr empty, bytes unchanged, each time
  - AC13 — `x`, `zz`, Enter, `1`, `maybe`, `y` on a rung-2 card → both prompts reprinted in full
    with `Not one of the answers. This prompt takes: …`, card ends `rung: 3  due: 2026-09-06`
  - AC14 — `bakc:` for `back:` → exit 1, `line 5: expected a line starting 'back: ', found 'bakc:
    hello'` on stderr, empty stdout, bytes unchanged; and `rung: 9` → `line 5: 'rung: 9' is outside
    0 to 4`, exit 1
  - WI-0001 — `add` re-run for its AC1, AC3 to AC8 → `Added: bonjour`, the duplicate warning, the
    empty-side refusal at exit 1 with the file unchanged; `python3 -m unittest … -p 'test_add.py'`
    → 16 tests `OK`, `-p 'test_store.py'` → 10 tests `OK`; `git diff main..HEAD -- tests/test_add.py
    tests/test_store.py recall/store.py` → empty
  - two cards sharing a front, answered right and wrong → written back independently (rung 2/+3 and
    rung 1/+1)
  - `python3 -m recall review extra` → exit 2, `unrecognized arguments: extra`
  - fifteen mutations applied and reverted by a script this skill wrote, the suite run against each;
    `git status --short recall/` → `clean` afterwards, suite green
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q`, exit 0, 60 tests
    `OK`, run here on `c706d83`)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (fourteen rows in `verify-report.md`, each a
    command run here against a hand-seeded card file with its actual output quoted; none cites
    `impl-report.md`)
  - `negative-cases-exercised` → **pass** (fourteen conditions triggered, listed in the report:
    nothing due, an empty deck, no file, two unparsable shapes, unrecognised input at both prompts,
    end of input at both prompts, `q` at both prompts, both ends of the ladder, the due boundary, a
    `SIGKILL`, duplicate fronts, and a bad command line)
  - `a-criterion-about-criteria-is-read` → **pass** (vacuous — no criterion of WI-0002 has criteria
    as its subject — and performed anyway for WI-0001's eight, with the non-intersection stated in
    those words and a covering case added rather than waived)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (fifteen mutations; every criterion
    has at least one test that fails when its behaviour is removed. The single survivor is shown to
    be an equivalent mutant and is reported as such)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` (new), carrying
    `Verified-commit: c706d837b0a8a6555b201858efabc68c3ac720b6`
  - `tracker/items/WI-0002/item.md` — AC1 to AC14 all ticked, each against a command in that report
  - no bug item filed
- **Status:** `verifying` → `in-review`
- **Result:** All fourteen criteria pass on evidence gathered here, independently of the
  implementation report. `review` offers exactly the due cards oldest first, hides the back until
  Enter, takes only `y` and `n`, has each answer on disk before the next card, and stops cleanly on
  `q`, on end of input and even on `SIGKILL`. WI-0001's behaviour is intact under the new dispatch.
  One obligation is carried forward rather than closed: `docs/architecture/overview.md` still says
  `review` is planned, which is D7 and D12 work at the close.

## 2026-08-30T12:53:59Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (six rows), and `journal.md` **in full** — all
    eight entries: `intake`, `answer-questions` ×2, `refine`, `plan`, `implement` ×2, `verify`
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — opened to decide the `vision.md` claim
  - `tracker/items/WI-0001/item.md` — its status and outcome, to decide the `overview.md` claim
  - the diff `git diff main..wi/WI-0002`, hunk by hunk — 686 added lines in four files
  - `docs/architecture/adr/` — ADR-0002, ADR-0003, ADR-0006, ADR-0007, ADR-0008, ADR-0009
  - `docs/architecture/overview.md` and `docs/product/vision.md` in full, for the claims audit
  - `recall/schedule.py` and `recall/cli.py`, opened as the things the claims cite
- **Decisions:**
  - **Accepted the change and closed it, `outcome: delivered`.** Fourteen criteria, each ticked
    against a command `verify` ran, each traceable to a hunk. No ADR is contradicted: `ADR-0009`'s
    purity holds literally, `ADR-0007`'s format is untouched, `ADR-0002`'s ladder appears once as
    `INTERVALS` rather than being restated in `cli.py`.
  - **Repaired `overview.md` (v4) and `vision.md` (v6) here rather than sending the item back or
    filing a question.** Four sentences in them had been made false by what was built. `implement`
    and `verify` both found this and both correctly declined to fix it — `spec/doc-header.md` §5
    names those two skills, and only those two, as ones that do not write to `docs/`. D7 is checked
    at this gate, so this is where the repair belongs. Sending the item back would have asked
    `implement` to do the one thing its contract forbids.
  - **One maintainability finding accepted, not sent back.** What each prompt accepts is stated
    twice in `cli.py` — as literal prompt text and derived by `_named(accepted)` — and a new key
    would update only the second. Accepted because two tests pin both strings, so the drift fails
    the suite. Written into `item.md`'s `## Notes`, not left in this journal.
  - **Four accepted gaps written into `item.md` `## Notes`.** Concurrent writers, WI-0001's literal
    restart, no measurement at backlog scale, and the duplicated prompt hint. A gap recorded only
    in a report nobody reopens is not on the record.
  - **No bug item filed and nothing returned to `verifying`.** `check-verify-freshness` reports the
    branch moved after verification but only under `tracker/` and `docs/`; the last commit touching
    `recall/` or `tests/` is `e595079`, which precedes the verified commit `c706d83`.
  - **The claims audit was done from the citations, not from the prose.** Twelve claims, each
    decided by opening the file it cites. Four false, one true-but-incomplete, seven true. No
    standing ADR needed a §4b correction — every ADR sentence read here was true and already
    sourced, and `lint-claims --all` is clean over the whole document set.
- **Cross-answer check:** none consumed. This execution consumed no new human answer — no question
  was answered into it and none is open anywhere in the engagement. It did **edit** two sentences
  in `docs/` that sit near the stakeholder's words, and both were checked against the answers they
  cite before being touched: `vision.md`'s *"Still to be put to them"* paragraph cites
  `EP-001/Q-004`, and the repair **keeps** that citation and their quoted delegation verbatim —
  what changed is our own claim about what was still open, not anything they said.
  `overview.md`'s repaired sentences cite `recall/cli.py`, `WI-0001` and `ADR-0009`, none of which
  is a stakeholder answer. No answer of theirs was overtaken by a later one, so ADR-0008's question
  route was not triggered. `lint-answers --context work-item --changed-since main` → exit 0 over a
  window of 2 documents.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0, *"verified
    at c706d837; wi/WI-0002 has moved to 229a49f8 but only the record changed (7 file(s) under
    tracker/ or docs/)"*
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, *"all 5
    commit(s) on main..wi/WI-0002 name WI-0002"*
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0, *"WI-0002 is a 'work-item',
    not an epic — the termination gate applies to an engagement's ending only. PASS."*
  - `.claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → exit 0,
    scope *"2 document(s) in 2 path(s) differ from main (45f8d03) under docs"*
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 0, scope *"every document under
    …/docs"*
  - `.claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → exit 0,
    *"claim window: 2 path(s) differ"*, 9 consumed human answers checked
  - `git diff main..wi/WI-0002` → read hunk by hunk; `git diff e595079..229a49f8 --stat` → only
    `tracker/` and `docs/`
  - `git rev-parse main` → `45f8d039…` **before** the trial
  - `git worktree add --detach /tmp/wi2-trial main` → exit 0, detached at `45f8d03`
  - `git -C /tmp/wi2-trial merge --no-ff wi/WI-0002` → exit 0, trial head `9027dc4e`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → exit 0,
    `Ran 60 tests in 2.877s`, `OK`
  - `python3 -m compileall -q recall tests` inside the trial worktree → exit 0
  - `git worktree remove --force /tmp/wi2-trial` → exit 0
  - `git rev-parse main` → `45f8d039…` **after** the trial — unmoved
  - `python3 -m recall review` driven against a deck with two cards sharing a front side → each
    written back independently (`first-back` rung 2 due +3, `second-back` rung 1 due +1)
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
- **Gates:**
  - `definition-of-done` → **pass** (D1 to D12 walked one at a time in `review.md`'s table, each
    with its own result and evidence; D7 passes *because this execution performed it*, and D9 is
    satisfied by the merge made after this entry)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness`, exit 0, quoted above)
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, 5 commits; run **before**
    the merge, because `main..branch` is empty once merged)
  - `tests-pass-on-the-merge-result` → **pass** (60 tests `OK` and `compileall` clean inside the
    detached trial worktree at `9027dc4`, not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace`, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone:
    *what was built and why* — `item.md`'s story and criteria, `plan.md`'s approach, five commits
    whose subjects name the work; *which skill decided what* — six history rows and eight journal
    entries, with `ADR-0009` carrying the one architectural decision and `refinement-qa.md` the six
    `[assumed]` ones; *what questions arose and how they were resolved* — none on this item, and
    the five on `EP-001` plus their propagation into these criteria are in the two
    `answer-questions` entries here; *what verification found* — `verify-report.md`'s fourteen
    rows, fourteen negative cases, fifteen mutations and one equivalent mutant explained
  - `claims-are-sourced` → **pass**, and the scope is the point: `lint-claims --context work-item
    --changed-since main` examined *"2 document(s) in 2 path(s) differ from main (45f8d03) under
    docs"*. That window is non-empty **only because this execution edited those two documents**;
    before the repair the same command read *"0 document(s) in 0 path(s)"* and exited 0 having
    looked at nothing. The audit that actually found the four false sentences is the twelve-row
    table in `review.md`, done by hand from the citations, plus `lint-claims --all` → exit 0
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main`,
    exit 0, 9 consumed answers checked; the reading is in `**Cross-answer check:**` above)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` → exit 0: WI-0002 is a
    work item, not an epic. `engagement-state EP-001` → *"active — still in flight: WI-0002,
    WI-0003"*, so the engagement is not at rest and no sign-off is due at this close)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new) — what was examined, the twelve-claim audit,
    D1 to D12, the hunk-by-hunk mapping, four accepted gaps, the verdict
  - `tracker/items/WI-0002/item.md` — `## Notes` gains the four accepted gaps; status and outcome
  - `docs/architecture/overview.md` **v4** and `docs/product/vision.md` **v6**, each with a
    change-log row (commit `229a49f8`)
  - the merge of `wi/WI-0002` into `main`, made after this entry
  - no bug item filed, no question filed
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is delivered. `review` offers exactly the due cards oldest first, hides each
  back until Enter, takes only `y` or `n`, writes every answer to the card file before the next
  card, and stops cleanly on `q`, on end of input and on `SIGKILL`. The trial merge ran 60 tests
  green on the merge result and left `main` where it found it. The one thing this review had to
  *do* rather than check was D7: two documents carried sentences that the delivered work had made
  false, and both are repaired with a version bump and a change-log row.
