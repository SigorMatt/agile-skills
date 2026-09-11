# Journal — WI-0005

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T02:15:12Z — answer-questions v0.6.3 — architect

- **Item:** WI-0005
- **Trigger:** created by `answer-questions` while consuming the stakeholder's answers on `EP-001`; this item did not exist before that answer
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` — the stakeholder's answer, option C: *"I mistype things in the spreadsheet most weeks, so being able to correct a spend I already recorded matters to me more than keeping a perfect history of my own typos — if I fix an entry, a past summary should just show the corrected figure."*
  - `tracker/items/EP-001/questions/Q-003.md` — the summary's content, which rules the individual spends out of the only report this tool has, and so leaves nothing that shows a spend to be referred to
  - `tracker/items/EP-001/questions/Q-002.md` — the overspend rule, which says nothing about correcting a spend upward
  - `tracker/items/EP-001/questions/Q-006.md` — the command's name, `envel`
  - `tracker/items/WI-0002/item.md` — the item that records a spend, which this one corrects
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 — the creation authority under which this item was filed
- **Decisions:**
  - **Filed as its own work item.** `answer-questions` step 3b, for the same reason as `WI-0004`: an answer that implies unscoped work becomes an item at `draft` with `arose-from`, not an amendment to an existing item's criteria.
  - **A correction replaces the entry rather than being recorded beside it.** This is the stakeholder's own sentence — *"a past summary should just show the corrected figure"* — read as AC3 and as the `## Out of scope` bullet ruling out a history of corrections. It is their decision, not ours; it is recorded here because it is the part of the answer most easily lost.
  - **Scoped to a spend, because that is the word they used.** Whether income and moves can also be corrected is written into `## Notes` as `refine`'s to ask rather than assumed either way.
  - **The hardest open point is named rather than solved:** nothing in the record gives a way to refer to one recorded spend, and `EP-001/Q-003` removed the one report that might have shown one. That is in `## Notes` for `refine` and for `plan`.
- **Questions raised:** none — the open points are recorded in `## Notes` for `refine`, which talks to the stakeholder directly
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0005 --type work-item --title "Correct a spend that was already recorded" --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from EP-001/Q-005` → exit 0, created at `draft`
- **Gates:**
  - `answer-is-propagated` → **pass** (this item **is** part of the propagation of `EP-001/Q-005`; it is named in that question's `## Consequences` and it exists)
  - `answered-from-the-record` → **pass** (the basis is the stakeholder's own `## Answer` on `EP-001/Q-005`, quoted above and in `## Notes`)
  - `escalation-is-justified` → **skipped** (nothing was escalated from this item)
  - `propagated-claims-carry-their-obligation` → **pass** (this execution wrote nothing under `docs/` from this item; the claims it wrote are acceptance criteria in `item.md`)
  - `engagement-state-is-left-to-the-ending` → **pass** (no `## Engagement state` section was written or amended here)
  - `cross-answer-consistency` → **pass** (the cross-answer check for `EP-001/Q-005` is written on that question and in `EP-001`'s journal, where the answer was consumed)
  - `workspace-valid` → **pass** (`validate-workspace` run at the end of the `EP-001` execution this item was created by)
  - `item-resumed-correctly` → **skipped** (this item was created, not resumed; its history has one row and no `resume-to`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply on this engagement deferred)
- **Artifacts:**
  - `tracker/items/WI-0005/item.md` (new) — story, five acceptance criteria, three exclusions, and four open points `refine` must ask about
  - `tracker/items/WI-0005/history.md`, `tracker/items/WI-0005/journal.md` (new, by `new-item`)
- **Status:** `—` → `draft`
- **Result:** `WI-0005` exists at `draft` because the stakeholder asked to be able to correct a spend at `EP-001/Q-005`, and said a past summary should show the corrected figure. It is not Ready; how a single spend is referred to at all is the open point that matters most and it is written down.

## 2026-09-11T07:16:15Z — refine v0.6.1 — product-analyst

- **Item:** WI-0005
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority `medium`, ahead of `WI-0006` at `low`)
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` — the draft, its five criteria, three exclusions and the four open points `answer-questions` left for this skill
  - `tracker/items/WI-0005/history.md` — one row; this is a fresh draft, **not** a send-back from `verifying` or `in-review`, so the whole story is open rather than one named defect
  - `tracker/items/WI-0005/journal.md` — `answer-questions`' filing entry, which names the identification gap as the point that matters most
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — the stakeholder's six epic-level answers, verbatim
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md`, `WI-0002/questions/Q-001.md` … `Q-005.md`, `WI-0003/questions/Q-001.md` … `Q-005.md`, `WI-0004/questions/Q-001.md` — every prior answer on the engagement, read for what is already settled and for what a new answer would have to coexist with
  - `tracker/items/WI-0006/item.md` — the sibling item that owns the other half of the identification gap
  - `envel/cli.py`, `envel/envelopes.py`, `envel/store.py` — what `envel spend` actually records today (envelope, cents, `on`, `at`, optional description; no identifier of any kind), so that the options put to the stakeholder describe the tool that exists
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Filed five blocking questions and suspended, rather than refining on.** The stakeholder is not in this session (`SIMULATION-NOTICE.md`), which is precondition 2's case exactly: file, suspend with `resume-to: draft`, stop. No acceptance criterion was rewritten this round, because every rewrite worth making depends on an answer — writing them now would be guessing and then presenting the guess as a requirement.
  - **Q-001 is first and the other four are shaped around it.** Nothing in this tool can display an individual spend, and that is a consequence of the stakeholder's own answer at `EP-001/Q-003` rather than an omission. Until they say how a spend is named, AC1–AC4 cannot be made decidable at all, which is why R4 fails on four of the five criteria for one reason.
  - **Split what the item's `## Notes` carried as one open point into four questions**, one decision each (`spec/question.md` §2): which fields are correctable (Q-002), whether a spend can be removed (Q-003), what happens below zero (Q-004), whether income is included (Q-005). The note listed removal and field-scope in a single sentence; folding them into one question is how a scope refusal gets logged as something else (F-027).
  - **Q-005 is a cross-answer question and is filed as one, not resolved here.** At `WI-0001/Q-003` the stakeholder refused a negative income *because* corrections were coming: *"I have asked for proper corrections … so there is no need for a back door."* At `EP-001/Q-005` they asked to correct *"a spend"*. If corrections reach only spends, the first answer is left without the thing it traded for. ADR-0008 §3 gives two moves and repairing the older sentence is not one of them, so both are quoted by ID and the stakeholder is asked which reading is theirs.
  - **`WI-0004/Q-001` is treated as settled and is not reopened.** *"I can fix a spend afterwards and I can't fix a move"* is the sentence `WI-0004` was designed around. Q-005 offers correcting moves as option C and marks it explicitly as contradicting that answer, so it is available but not recommended.
  - **No question was routed to `plan`.** The hard part of this item looks like a design question and is not: every way of naming a recorded spend shows up on the command line, so choosing one would be choosing what the stakeholder types.
  - **One delegation is named before it is spent, not after.** The command's spelling falls under `WI-0003/Q-004` — *"I'd rather everything in this tool be typed the same way"* — and cannot be decided until Q-001 is answered. `refinement-qa.md` records the `**Under delegation:** WI-0003/Q-004 — argument style` line that round 2 will carry, so R12's licence has a written scope before anything is taken under it (F-082).
  - **`depends-on: WI-0002` was left unrecorded this round.** It is true and now costless — `WI-0002` is `done` — but it belongs with the criteria rewrite in round 2, and R7 passes either way.
- **Questions raised:** `Q-001`, `Q-002`, `Q-003`, `Q-004`, `Q-005` — five, all `addressed-to: human`, all blocking, all open. One conversation in five artifacts: each `## Context` carries the *"round 1, question N of 5"* frame and Q-005 closes it (F-020). Recorded in `tracker/items/WI-0005/artifacts/refinement-qa.md`.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 before the questions were filed (7 items, 11 documents, 0 errors)
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 after filing, reporting `question.blocking.not-suspended` on this item — which is the condition this transition resolves
  - `.claude/agile-skills/scripts/lint-answers --item WI-0005` → exit 0, "checked 0 consumed human answer(s) and 0 delegation(s) spent"
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` judged against the pending move to `awaiting-answer`; the only error before it was `question.blocking.not-suspended`, which this move clears)
  - `definition-of-ready` → **fail** (walked criterion by criterion in `refinement-qa.md`: R1 pass, R2 pass, R3 pass, **R4 fail** — AC1–AC4 name no command and no way to say which spend, R5 pass, **R6 fail by construction** — five blocking questions now open, R7 pass, **R8 fail** — `refinement-qa.md` is `status: agenda`, **R9 unresolved** — the split depends on Q-002/Q-003/Q-005, **R10 fail** — no behaviour combination is stated because no behaviour is chosen, R11 pass, R12 pass vacuously with the one anticipated delegation named in advance. The item is not Ready and is not being passed as Ready)
  - `criteria-are-decidable` → **fail** (AC1 names no command; AC2, AC3 and AC4 cannot be observed until a spend can be referred to; only AC5 — a correction survives into a later invocation — is decidable as written)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0005`, exit 0; and the check it cannot make was made by hand — `WI-0001/Q-003` against `EP-001/Q-005` is put to the stakeholder as `Q-005` rather than reconciled here)
  - `qa-recorded-verbatim` → **skipped** (no answer has been received, so there is nothing verbatim to record; `refinement-qa.md` declares `status: agenda` for exactly this reason and R8 reads that field)
- **Artifacts:**
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-005.md` (new)
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (new, `status: agenda`)
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0005` is suspended on five blocking questions to the stakeholder. It is not Ready and no criterion was rewritten: the whole item turns on how a recorded spend is referred to, and nothing in the tool can show one today because `EP-001/Q-003` ruled the individual spends out of the only report there is. Round 2 rewrites AC1–AC5, decides whether R9 requires a split, and records the `WI-0003/Q-004` delegation it spends.

## 2026-09-11T07:31:31Z — answer-questions v0.6.3 — architect

- **Item:** WI-0005
- **Trigger:** status `awaiting-answer`; the stakeholder's five replies had arrived in the question files since the last turn, which is precondition 1's second branch — `addressed-to: human` with `## Answer` filled in. Consumed before `next` was run at all, because an answered question left open stops the orchestrator on every subsequent turn (F-011)
- **Inputs read:**
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-005.md` — the five questions in full: context, options, recommendation, and the stakeholder's reply verbatim
  - `tracker/items/WI-0005/item.md` — the draft: five criteria, three exclusions, and the four open points `answer-questions` left for `refine`
  - `tracker/items/WI-0005/history.md` — the suspending row, which carries `resume-to: draft`
  - `tracker/items/WI-0005/journal.md` — the filing entry and `refine`'s round-1 entry, for what each question was filed to settle
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (`status: agenda`) — round 1's Definition-of-Ready walk, the delegation named in advance, and what round 2 was told to do
  - `tracker/items/WI-0004/questions/Q-001.md` — the *"I can fix a spend afterwards and I can't fix a move"* answer, which two of this round's replies lean on
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md`, `WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-005.md`, `WI-0003/questions/Q-001.md`, `Q-003.md`, `Q-004.md`, `EP-001/questions/Q-001.md` … `Q-006.md` — the prior recorded human answers, for the cross-answer checks
  - `tracker/items/WI-0006/questions/Q-001.md`, `Q-003.md` — the sibling item's replies, which bear on this item's `Q-001` and are consumed on their own item, not here
  - `docs/product/vision.md` (v3) — the document this answer had to reach
  - `docs/architecture/adr/ADR-0001` … `ADR-0009` — read for a recorded decision these answers contradict; none does. `ADR-0002` (the store is a JSON entry log) and `ADR-0006` (a spend carries the date it happened) are the two the reference of `Q-001` will bear on, and that is `plan`'s to take, not this execution's
  - `.claude/agile-skills/spec/question.md` §3 and §4, `spec/doc-header.md` §4a, `spec/journal-and-history.md`, `spec/ids-and-statuses.md` §5
- **Decisions:**
  - **All five answered by route 2 — the human's own reply — and none by a decision of ours.** Every one of the five is a question `refine` correctly refused to decide: what the stakeholder types, what can be put right, and what stays permanent. The basis recorded on each question is their reply verbatim, and no ADR was written because no architectural choice was taken here.
  - **The one conflict round 1 filed for was settled by the stakeholder, not reconciled by us.** `WI-0001/Q-003` refused a negative income *because* corrections were coming; `EP-001/Q-005` said *"a spend"*. `Q-005`'s reply supplies exactly what the earlier answer traded for, in their own words. Neither sentence was edited — ADR-0008 §3's outcome, reached the way it is supposed to be reached.
  - **No new item was filed, and that was checked rather than assumed.** The widening `Q-003` and `Q-005` produce — removal, and corrections reaching income — is this item's own scoping question being answered: `item.md`'s `## Notes` listed both as things `refine` must ask *on this item*. Step 3's "file a work-item" move is for work no item records, and this item records it. `Q-001`'s answer needs the listing command, and `WI-0006` already exists for it.
  - **The criteria were rewritten here, not left for `refine`.** Five criteria became ten: AC1 (the reference), AC3 (four correctable parts), AC7 (below zero refused with the shortfall), AC8 (removal), AC9 (income) are the five answers, and the old AC1–AC5 were renumbered around them. The reason is `answer-is-propagated`: an answer that reaches only the question file has not been given, and `item.md` is what `refine` re-reads. What was **not** done is the Definition-of-Ready work — the criteria record the decisions and are not yet decidable to R4's standard, `refinement-qa.md` stays `status: agenda`, and R9's split question is explicitly left open. This item is not Ready and nothing here claims it is.
  - **Two gaps these answers open were recorded for `refine` rather than filed as questions.** Whether an **income** can be removed (`Q-003` names a spend; `Q-005` extends only correcting), and whether the reference is per-envelope or global (`Q-001`'s example says one thing, `WI-0006/Q-003`'s reply points the other way). Both are real and both are the stakeholder's to settle — and this item returns to `draft`, where `refine` is the skill that asks. Filing them here would take the conversation out of the skill that owns it and would put a second round of questions on the board before the first had been digested.
  - **`depends-on: WI-0006` deliberately not recorded.** It is now true — the stakeholder said the listing has to exist — but writing it into the frontmatter freezes this item's refinement under `pipeline.yaml`'s `runnable` rule while `WI-0006` is itself mid-refinement. Recorded in `## Notes` with the reason, for `refine` to take with the criteria rewrite.
  - **The vision was updated and nothing in it was rewritten.** Two paragraphs added after the sentence sourced to `EP-001/Q-005`, which still says what it said. Rule 3 of `lint-answers` is the thing being respected: a later answer of theirs does not license editing an earlier sentence of theirs.
  - **One sentence was weakened to discharge its obligation honestly.** The added paragraph opened *"each part of that is the stakeholder's own answer"* — a quantifier over a family, which `lint-documents` flagged. Rather than manufacture an enumeration for a rhetorical *each*, the sentence was rewritten to say the same thing without quantifying: *"What follows was decided by the stakeholder, question by question."* `spec/doc-header.md` §4a's own instruction — weaken the sentence until it is a cited fact.
- **Cross-answer check:** five human answers consumed, each with its own `## Cross-answer check` section on the question file. `Q-001` against `EP-001/Q-003`, `EP-001/Q-004`, `WI-0002/Q-002`, `WI-0003/Q-004`, `EP-001/Q-005` — compatible throughout; the monthly summary keeps its four figures and the reference is read off a command asked for by name. `Q-002` against `WI-0004/Q-001`, `WI-0002/Q-001`, `WI-0002/Q-002`, `WI-0001/Q-002`, `EP-001/Q-005` — compatible; the stakeholder drew the spend/move boundary themselves. `Q-003` against `WI-0001/Q-001`, `WI-0001/Q-003`, `WI-0002/Q-005`, `EP-001/Q-005` — compatible; option C was refused by them as a back door through the zero rule. `Q-004` against `EP-001/Q-002`, `EP-001/Q-001`, `WI-0002/Q-005`, `EP-001/Q-005`, `WI-0005/Q-005` — compatible, with the two-step cost accepted in as many words. `Q-005` against `WI-0001/Q-003`, `EP-001/Q-005`, `WI-0004/Q-001`, `WI-0003/Q-003`, `WI-0005/Q-004` — compatible, and it is the reply that closes the pair round 1 escalated. **No verdict of `conflicts` was recorded, so no question was filed under ADR-0008 §3.**
- **Questions raised:** none — two open gaps were recorded in `item.md`'s `## Notes` and in `refinement-qa.md` for `refine` round 2, which is the skill that puts questions to the stakeholder on a `draft` item
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0005` → exit 0, "checked 5 consumed human answer(s) and 0 delegation(s) spent"
  - `.claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0005 --uncommitted` → exit 1 first, `document.enumeration.missing` on `docs/product/vision.md:40`; then exit 0 after the sentence was weakened, 0 quantified sentences newly written
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, 1 document compared region by region against HEAD
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 before this transition, reporting `question.awaiting.none-open` on this item, `board.stale`, and `doc.changelog.no-execution` for the version row this entry is the execution of — all three resolved by this transition, the board regeneration and this entry
- **Gates:**
  - `answer-is-propagated` → **pass** (each of the five `## Consequences` sections names files and the changes are in them: `item.md` AC1/AC2/AC3/AC4/AC7/AC8/AC9, the rewritten first `## Out of scope` bullet, the removed income exclusion and the two new exclusions, five new `## Notes` bullets and the round-2 list; `refinement-qa.md`'s three new sections; `docs/product/vision.md` v4's two new paragraphs)
  - `answered-from-the-record` → **pass** (route 2 for all five — the stakeholder's own reply, quoted verbatim on the question, in `refinement-qa.md` and in `item.md`'s `## Notes`; no answer was invented and no ADR was needed because no architectural decision was taken)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human by this execution; the two remaining gaps go to `refine`, which asks directly)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0005 --uncommitted`, exit 0 after the `each` sentence was weakened. The five sentences written into `docs/product/vision.md` are cited facts, sourced `[src: WI-0005/Q-001]` … `[src: WI-0005/Q-005]`, and each citation resolves to a question file that exists; the four correctable parts of a spend are written out by name rather than quantified over)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted`, exit 0. `docs/product/vision.md`'s `## Engagement state` was read and left untouched. Its second bullet was already false before this execution — overtaken when the `EP-001` answers were consumed, not by anything here — and `Q-001`'s `## Consequences` records that the ending owns it. There is no `plan.md` on this item, so no invalidation row was written)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0005`, exit 0, 5 consumed answers checked; the read the script cannot make is above under `**Cross-answer check:**`, and the one conflict this round could have produced was settled by the stakeholder rather than by us)
  - `workspace-valid` → **fail** (`validate-workspace .` judged against this transition: the three errors standing before it were `question.awaiting.none-open`, which this move clears, `board.stale`, cleared by regenerating the board, and `doc.changelog.no-execution` on the v4 row, which this entry is the execution of; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0005:awaiting-answer->draft+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-11T07:16:15Z records `resume-to: draft`, read from `history.md` rather than inferred; this move is `awaiting-answer` → `draft`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred; all five chose an option and gave a reason)
- **Artifacts:**
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-005.md` — each `status: answered`, `answered-by: human`, `answered-at` stamped, with a `## Cross-answer check` written on consumption above the one filed with the question, and a `## Consequences` naming the files changed
  - `tracker/items/WI-0005/item.md` — ten acceptance criteria where there were five; `## Out of scope` rewritten (income exclusion removed, moves exclusion sourced to the stakeholder's own words, listing command and the `envel add` refusal added); `## Notes` carrying what each answer settled, the `WI-0006` dependency and what is left for round 2
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — header paragraph updated, `## What happens next` rewritten, and `## Answers — round 1`, `## Cross-answer check — round 1, on the replies` and `## What round 1's answers left for round 2` added. `status: agenda` deliberately unchanged: `refine` sets it to `recorded` when round 2 records the exchange
  - `docs/product/vision.md` — v3 → v4, two paragraphs added to `## What it is for`, with a change-log row
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** All five of `WI-0005`'s blocking questions are answered by the stakeholder and propagated into `item.md`, `refinement-qa.md` and the product vision. The item returns to `draft` with ten criteria recording what was decided — a reference on every entry, four correctable parts, removal of a spend, a below-zero correction refused with the shortfall named, and corrections reaching income. It is **not** Ready: `refine` round 2 owes the decidability work, the R9 split call, and two questions these answers opened — whether an income can be removed, and whether the reference is per-envelope or global.

## 2026-09-11T07:43:41Z — refine v0.6.1 — product-analyst

- **Item:** WI-0005
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority `medium`, ahead of `WI-0006` at `low`). This is round 2: the item returned to `draft` earlier in this turn when `answer-questions` consumed the stakeholder's five round-1 replies
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` — the item as `answer-questions` left it: ten criteria recording the five decisions, five exclusions, and the round-2 agenda in `## Notes`
  - `tracker/items/WI-0005/history.md` — three rows. This is **not** a send-back from `verifying` or `in-review`; it is a second refinement round on an item that has never been built, so the whole story is open
  - `tracker/items/WI-0005/journal.md` — round 1's entry and the `answer-questions` entry that propagated the answers
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (`status: agenda`) — round 1's Definition-of-Ready walk, the delegation named in advance, and the three things it left for this round
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-005.md` — the five answers verbatim, including the halves of `Q-002` and `Q-005` that were promised to the criteria rather than asked about
  - `tracker/items/WI-0003/questions/Q-003.md`, `Q-004.md`, `Q-005.md` — income is dated when it is typed and `envel add` is not reopened; `envel summary 2026-08` and the consistency preference; a future month refused
  - `tracker/items/WI-0006/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the sibling's answers, which decide who owns the reference and make `Q-008` necessary
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — the delivered criteria this item's criteria have to agree with, read for the wording each citation anchors to
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md`, `tracker/items/EP-001/questions/Q-002.md`, `Q-005.md` — the prior answers the new criteria and the three new questions are checked against
  - `envel/cli.py`, `envel/envelopes.py`, `envel/store.py` — what an entry actually holds today. A spend carries `kind`, `envelope`, `cents`, `on`, `at` and an optional `description`; an **income** carries `kind`, `envelope`, `cents` and `at`, and no `on` at all. That fact is what turned `Q-006` from a tidiness question into a real one
  - `docs/product/vision.md` (v5), `docs/architecture/adr/ADR-0003`, `ADR-0006`, `ADR-0007`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/doc-header.md` §4a, `spec/journal-and-history.md`
- **Decisions:**
  - **The reference belongs to `WI-0006`, and `depends-on: WI-0002, WI-0006` is now recorded.** Round 1's draft had this item creating the reference and `WI-0006` printing it, which made the two items circular — each unable to be delivered before the other. The stakeholder settled it themselves at `Q-001`: *"That does mean the listing command has to exist, and I am saying yes to that separately."* Had they meant the reference first and the listing later, option D at that question was exactly that, and they did not choose it. So AC1 **consumes** a reference rather than defining one, and the reference is in `## Out of scope`.
  - **`WI-0006` is therefore built before this item, and *"keep it small and keep it last"* is still honoured.** That instruction is about size and priority — `WI-0006` stays `low`, stays small, and is the last thing designed — and the dependency is about build order, which their `Q-001` answer decided. The two sentences are not in conflict and this round did not put them back to the stakeholder as though they were; the reasoning is written into both items' `## Notes` so that whoever schedules the work has both.
  - **R9 resolved: not split.** Round 1 left it `unresolved` pending these answers. With the reference gone to `WI-0006`, what remains is `envel fix` and `envel remove` over one piece of machinery — find an entry by its reference, change or drop it, re-check the one balance invariant `WI-0002` AC5 already keeps. Splitting them would put that invariant in two items and leave the second unverifiable without the first.
  - **The command surface was decided, not asked about.** `envel fix <ref>` with `--amount`, `--on`, `--description` and `--envelope`, and `envel remove <ref>`. Taken under the standing delegation at `WI-0003/Q-004` and recorded as `[assumed]` with the line R12 requires — **Under delegation:** `WI-0003/Q-004` — argument style and the naming of commands and options. The licence is spent the way the existing tool is typed: the argument a command always takes is a plain word, the ones it takes rarely are named options.
  - **The removal command is `remove`, not the `unspend` that appeared in `Q-003`'s option B.** They endorsed that option's behaviour, not its spelling, and `unspend` would need renaming the moment `Q-007` lets an income be removed. The word is put in front of them in `Q-007`'s context rather than buried in the Q&A, so a disagreement costs one amendment and is easy to raise.
  - **AC4 — a description is removed by correcting it to an empty one — is `[assumed]` under no licence, and says so.** The basis is `Q-002`'s own cross-answer check, which promised the stakeholder this would be written into the criteria rather than asked about. That is a promise being kept, not a delegation being spent, and R12's other half is the honest form for it: the entry names where a disagreement lands.
  - **Fifteen criteria rewritten to be decidable**, each naming a line to type and an outcome to observe, with `## How each criterion is decided` in `refinement-qa.md` giving the command and the verdict for every one. Two are new behaviours nobody had written down: AC6 (`envel fix <ref>` with no option is a usage error) and AC13 (`envel fix` or `envel remove` aimed at a **move** is refused) — the second is the stakeholder's own exclusion made observable instead of left as prose in `## Out of scope`.
  - **Citations to the delivered items are anchored to the criteria's own words**, per `spec/doc-header.md` §4a, because three of them point into `WI-0001` and `WI-0002`, whose lists are long and have been renumbered before (F-094).
  - **Income has no criterion, and that is deliberate.** `Q-005` put income in scope and `Q-006`/`Q-007` are what it would take to write it. Rather than write criteria to one reading of *"in the same way as a spend"*, `## Out of scope` says income is out **this round** and `## Notes` names the two open questions that own it — R10 satisfied by naming the unconstrained case and who left it so.
  - **Three questions filed and the item suspended**, because the stakeholder is not in this session (`SIMULATION-NOTICE.md`) — precondition 2's case: file, suspend with `resume-to: draft`, stop.
- **Questions raised:** `Q-006`, `Q-007`, `Q-008` — three, all `addressed-to: human`, all blocking, all open. One conversation in three artifacts, each `## Context` carrying the *"round 2, question N of 3"* frame and `Q-008` closing it (F-020). Recorded in `artifacts/refinement-qa.md`. `Q-006` is a cross-answer question: `WI-0005/Q-005` (*"in the same way as a spend"*) against `WI-0003/Q-003` (income gets no date, *"I'm not paying for rework on a command that already works for a case I don't have"*), both quoted verbatim and by ID, with `Recommendation` marked as ours and placed last
- **Commands:**
  - `grep -n 'def \|kind' envel/envelopes.py`, `grep -n 'add_parser\|add_argument' envel/cli.py`, `sed -n '1,80p' envel/store.py` → read the entry shapes; an income entry has no `on` field, which is the fact `Q-006` rests on
  - `.claude/agile-skills/scripts/lint-answers --item WI-0005` → exit 0, "checked 5 consumed human answer(s) and 1 delegation(s) spent"
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1 before this transition, reporting `question.blocking.not-suspended` on this item — the condition this move resolves
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` judged against the pending move to `awaiting-answer`; the only error before it was `question.blocking.not-suspended`, which this move clears, and every `[src: ...]` citation written this round resolves)
  - `definition-of-ready` → **fail** (walked criterion by criterion in `refinement-qa.md`: R1 pass, R2 pass, R3 pass, **R4 fail** — the fifteen written criteria are each decidable and the sixteenth, for income, cannot be written until `Q-006` and `Q-007` are answered, R5 pass, **R6 fail by construction** — three blocking questions now open, R7 pass — `depends-on` recorded this round, **R8 fail** — `refinement-qa.md` is `status: agenda`, **R9 resolved, not split** — one piece of machinery under two subcommands, R10 pass — the combinations are AC6, AC5+AC9, AC3+AC8, AC13, AC1+AC12, and the income case is named as unconstrained with who left it so, R11 pass — nothing counted, **R12 pass** — one delegation spent with its ID and category, one assumption under no licence saying so. The item is **not** Ready and is not being passed as Ready)
  - `criteria-are-decidable` → **pass** (for the criteria written** (`refinement-qa.md`'s `## How each criterion is decided` gives, for each of AC1–AC15, the line to type and the verdict that follows, all observed in a store of its own under `ENVEL_FILE`. The gate is recorded as passing on what exists; what is missing is a criterion, and R4 carries that))
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0005`, exit 0, 5 consumed answers and 1 delegation; the read it cannot make is that one conflict was found — `Q-005` against `WI-0003/Q-003` — and filed as `Q-006` quoting both, rather than reconciled here, and that `Q-007` and `Q-008` are silences rather than conflicts)
  - `qa-recorded-verbatim` → **pass** (`refinement-qa.md` carries round 1's five replies verbatim and round 2's three questions with what was decided instead of asking; the two `[assumed]` entries carry their basis — one `**Under delegation:**` line with ID and category, one statement that no licence covered it and where a disagreement lands. No answer was paraphrased, and no reply has been received this round to record)
- **Artifacts:**
  - `tracker/items/WI-0005/item.md` — `depends-on` added; `## Acceptance criteria` rewritten from ten to fifteen, decidable, with the command surface declared `[assumed]` above them; `## Out of scope` grown to five entries including the reference and income-this-round; `## Notes` rewritten with the dependency, the sequencing, the two income gaps, the reference question and the R9 judgement
  - `tracker/items/WI-0005/questions/Q-006.md`, `Q-007.md`, `Q-008.md` (new)
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — `# Round 2` added: the Definition-of-Ready walk, what was decided and by what authority, the three questions, the round-2 cross-answer check, the per-criterion decidability table, and what is left for round 3. `status: agenda` unchanged
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0005` is suspended on three blocking questions. Round 2 turned the stakeholder's five decisions into fifteen decidable criteria, resolved R9 against a split, recorded `depends-on: WI-0006` after finding that round 1 had left the two items circular over who owns the reference, and spent one delegation with its scope written down. What it could not do is write a single criterion for correcting an **income**: *"in the same way as a spend"* collides with their own refusal to give income a date, and that is `Q-006`, quoting both of their sentences and asking which wins.

## 2026-09-11T07:51:44Z — answer-questions v0.6.3 — architect

- **Item:** WI-0005
- **Trigger:** status `awaiting-answer`, with three human-addressed questions carrying replies; consumed ahead of `next` because an answered-but-unconsumed question stops the orchestrator (`spec/question.md` §3)
- **Inputs read:**
  - `tracker/items/WI-0005/questions/Q-006.md`, `Q-007.md`, `Q-008.md` (the three replies)
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-005.md` (round 1, for the cross-answer check)
  - `tracker/items/WI-0005/item.md` and `history.md` (the suspending row carries `resume-to: draft`)
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (rounds 1 and 2)
  - `docs/product/vision.md` (v5)
  - `docs/architecture/adr/` — nine ADRs listed; `ADR-0006` (a spend carries the date it happened) and `ADR-0008` (a month is a string and every figure is a filtered sum) read, because `Q-006` turns on whether an income has a date and which month it counts in. Neither is contradicted: the stakeholder's answer leaves income undated, which is what the code already does.
  - `envel/envelopes.py` `add_income` (lines 78–103) and `envel/cli.py` — to establish that an income entry records `kind`, `envelope`, `cents` and `at`, and carries no date and no description
- **Decisions:**
  - `Q-006` answered **by the human**, option B: a correction reaches an income's amount and the envelope it went into. Route: the human's own reply to an escalation this execution did not make (round 2's `refine` filed it). Propagated as AC16, which also refuses `--on` and `--description` on an income reference. Rationale for writing the refusal into the criterion rather than leaving it unsaid: their sentence bounds what `envel fix` may change, and a bound nobody can observe is not a criterion.
  - `Q-007` answered **by the human**, option B: `envel remove` reaches an income, same command, no flag. Propagated as AC17, and as AC18 for the below-zero case — which is not a fresh decision but the application `Q-007`'s own text promised the stakeholder would be made rather than asked about again, of their `Q-004` answer.
  - `Q-008` answered **by the human**, option A: one number counted once across everything recorded. Propagated into AC1. The half of it that lands on `WI-0006` is recorded in `## Notes` and in the vision rather than written into `WI-0006`'s criteria: this execution is dispatched on `WI-0005`, and editing a sibling item's criteria would put a decision on the board under no execution's name.
  - **No new item filed**, on any of the three. `Q-006`'s option D offered the dated-income question as its own item and the stakeholder refused it in terms — *"I am not leaving a dated-income item sitting on the board either"* — so `spec/ids-and-statuses.md` §5 is not engaged; `Q-007` and `Q-008` settle scope questions `WI-0005` and `WI-0006` already record.
  - **Four stale AC cross-references repaired** in `item.md`'s round-1 `## Notes` — they pointed at AC3, AC8, AC7 and AC9 from the five-criterion draft, and round 2's renumbering had left each naming a criterion about something else. Ordinary repair: no sentence of the stakeholder's was changed, only our own pointers into our own list.
  - **No ADR written.** Each answer decides what the stakeholder types or what the tool refuses, and lands in criteria; none of the three chooses a technical approach, and an ADR recording a decision the human made would misattribute it.
- **Cross-answer check:**
  - `Q-006` — checked against `WI-0003/Q-003`; `WI-0005/Q-005`; `WI-0005/Q-002`; `WI-0005/Q-004`; `WI-0001/Q-003`. **No conflict.** The pair round 2 filed the question *for* — *"in the same way as a spend"* against the refusal to date income — was settled by the stakeholder in favour of the older sentence, in their own words. Neither sentence was edited anywhere under `docs/`.
  - `Q-007` — checked against `WI-0005/Q-003`; `WI-0001/Q-001`; `WI-0005/Q-005`; `WI-0005/Q-004`; `WI-0001/Q-003`. **No conflict.** `WI-0001/Q-001`'s *"nothing should ever be able to wipe money out of an envelope by accident"* was narrowed by its own author; it was recorded as their statement and **not** repaired in any document.
  - `Q-008` — checked against `WI-0005/Q-001`; `WI-0006/Q-003`; `WI-0001/Q-004`; `WI-0003/Q-004`; `WI-0006/Q-002`. **No conflict.** `Q-001`'s reply is not overtaken: the stakeholder says the per-envelope `7` in it was our example, so the vision paragraph sourced to `[src: WI-0005/Q-001]` was left as it stands and a new paragraph carries what `Q-008` decided.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0005` → exit 0, 8 consumed answers and 1 delegation checked
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0005 --uncommitted` → exit 0, 0 quantified sentences newly written
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, 1 document compared region by region against HEAD
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before this transition (`doc.changelog.no-execution` on the row this entry is the execution for, plus the two errors the transition and `board-gen` clear); re-run after
- **Gates:**
  - `answer-is-propagated` → **pass** (each of the three `## Consequences` sections names files; each was reopened after writing — `item.md` carries AC1's new sentences, AC15's extended case list, AC16, AC17, AC18, the rewritten `## Out of scope` income bullets and the round-2 `## Notes`; `refinement-qa.md` carries `## Answers — round 2` and the round-2 cross-answer section; `docs/product/vision.md` carries both new paragraphs at v6)
  - `answered-from-the-record` → **pass** (all three answers come from the human's own replies, quoted verbatim in the question files and in `refinement-qa.md`; the one fact not from them — that an income entry has no date and no description field — is cited to `envel/envelopes.py:92`)
  - `escalation-is-justified` → **skipped** (no question was re-addressed to the human by this execution; nothing to justify)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0005 --uncommitted` → exit 0. The sentences written into the vision are cited facts, each sourced to a question file that resolves; none ranges over a family, so no enumeration is owed. The gate's own output says a universal phrased without a quantifier word is caught by nothing here, and the read behind that: the two new paragraphs describe what one command does to one kind of entry, and say nothing about a set of commands, envelopes or entries)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, the vision's `## Engagement state` byte-identical to HEAD. No answer this execution consumed falsified a sentence in it: the three are about what the product does, not about the state of the engagement)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0005` → exit 0, 8 consumed human answers. Three conflict verdicts declared: none. The read behind that is the `**Cross-answer check:**` bullet above)
  - `workspace-valid` → **fail** (`validate-workspace .` re-run after this transition; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0005:awaiting-answer->draft+journal'` exited 1)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-11T07:43:41Z records `resume-to: draft`, read from `history.md` rather than inferred from which skill asked; this transition targets `draft`)
  - `a-deferral-is-not-an-answer` → **skipped** (none of the three replies defers. Each names an option letter and gives its reason, and `Q-006` explicitly closes the one route that would have deferred anything — option D, a dated-income item left on the board)
- **Artifacts:**
  - `tracker/items/WI-0005/questions/Q-006.md`, `Q-007.md`, `Q-008.md` — each `status: answered`, `answered-by: human`, with `## Cross-answer check` and `## Consequences` filled in
  - `tracker/items/WI-0005/item.md` — AC1 extended; AC16, AC17, AC18 added; AC15's case list extended; `## Out of scope` income bullet replaced by two; `## Notes` given the round-2 answers and the `WI-0006` hand-off; four stale AC cross-references repaired
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — preamble rewritten, `## Answers — round 2`, `## Cross-answer check — round 2, on the replies`, and `## What round 2 leaves for round 3` rewritten against what is now answered
  - `docs/product/vision.md` (v5 → v6) — two paragraphs added under `## What it is for`, with a change-log row
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's three round-2 answers are consumed and propagated. `WI-0005` now has eighteen criteria covering income as well as spends, and a reference that is one number across the whole store; the item returns to `draft` for `refine`'s third round, which walks the Definition of Ready against the new criteria and extends the decidability table to AC16–AC18.

## 2026-09-11T09:25:13Z — refine v0.6.1 — product-analyst

- **Item:** WI-0005
- **Trigger:** status `draft`, dispatched by `next` — the only runnable item on the board
- **Inputs read:**
  - `tracker/items/WI-0005/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (rounds 1 and 2, both answer sets)
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-008.md` (all `answered`)
  - `tracker/items/WI-0006/item.md` — the sibling that now owns the reference, `done` and merged
  - `docs/product/vision.md` (v7), `docs/architecture/overview.md`
  - `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md`, `ADR-0007`
  - `envel/envelopes.py`, `envel/summary.py` — for the shape of an income entry, a move's two
    halves, and the line `envel entries` prints
  - `.claude/agile-skills/spec/dor-dod.md`, `spec/journal-and-history.md`, `pipeline.yaml`
- **Decisions:**
  - **Asked the stakeholder nothing.** Every gap round 3 found was a reading of a convention the
    delivered tool already prints in the messages they read, not a choice about what the software
    promises. `refine` step 3's first test was applied to each and none reached it;
    `artifacts/refinement-qa.md` §*Why round 3 put nothing to the stakeholder* names each gap and
    why. Rationale: a third round of questions manufactured to look thorough costs a stakeholder
    round trip and buys nothing, and the protocol's cost is their attention.
  - **Appended AC19 and AC20 rather than inserting them.** AC19: a refused `envel fix` applies
    none of itself. AC20: the `envel entries` listing shows the change. Both are the R10
    combinations round 3 found with no criterion — an income reference given one accepted and one
    refused option, and any correction read back on the listing the reference came from. Both are
    `[assumed]` under **no** delegation and each says on its own line where a disagreement lands.
    Rationale for appending: `ADR-0010` cites this item's AC1 twice by number and AC15 lists nine
    criteria by number, so a renumbering would have left all of them resolving against whatever
    moved into the slot (F-094).
  - **Widened AC18 to the third route below zero.** It named removing an income and correcting one
    downwards; `envel fix <income-ref> --envelope <name>` takes the income's whole amount out of
    the envelope it went into and is the one income correction that goes below zero with no figure
    reduced. Rationale: `WI-0005/Q-004` is *"No negative envelopes anywhere in this tool, and that
    includes here"* — narrowing it to two of three routes would have been the decision, not
    widening it to all three.
  - **Repaired two stale source citations.** AC16 and a `## Out of scope` bullet cited
    `envel/envelopes.py:92` for the shape of an income entry; `WI-0006` added the reference
    counter and shifted `add_income` down eleven lines, so line 92 is now a docstring. Both now
    cite `:107`, and AC16 says the entry carries its reference as well. Rationale: the sentence was
    false because the *code* moved, which is the ordinary repair — deliberately distinct from
    repairing a sentence the stakeholder has since contradicted, which ADR-0008 §3 forbids.
  - **Recorded which figure the below-zero rule is about, with the measurement.** `envel entries
    <envelope>` can already print a negative opening figure — observed, `-42.30` — because a spend
    carries its own date and an income does not. AC9 and AC18 are about what `envel list` shows.
    Rationale: written so `implement` does not invent a second check over a bounded sum; not filed
    as a defect, because `refine` does not evaluate delivered behaviour and the figure falls out of
    two decisions the stakeholder has already taken and been told the cost of.
  - **Discharged round 2's two `WI-0006` obligations in the notes.** They read as outstanding work
    on a sibling; `WI-0006`'s own round 3 wrote AC3 and AC4 and the item is `done`. The notes now
    say so and cite both. Rationale: a note that describes the workspace as it was a turn ago is a
    note that will mislead `plan`.
  - **R9 re-read and still not split.** The income criteria that arrived since round 2 reach the
    same machinery with a narrower set of fields; splitting `fix` from `remove` would put the one
    balance invariant in two items.
  - **Three combinations left deliberately unconstrained**, each named in the R10 table with who
    left it so: a correction that changes nothing, `--envelope` naming the envelope the entry is
    already in, and `--on` setting a date before the envelope existed.
- **Questions raised:** none. All eight questions this item ever filed — `Q-001` to `Q-008` — are
  `status: answered`, `answered-by: human`, and nothing is left `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0005` → exit 0, 8 consumed human
    answers and 1 delegation checked, 0 errors
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 -m envel new|add|spend|move|entries|list` against a throwaway `ENVEL_FILE` → exit 0
    each; used to read the delivered line format and to measure the `-42.30` opening figure
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 7 items and 12 documents, 0 errors, 0 warnings)
  - `definition-of-ready` → **pass** (, criterion by criterion: R1 pass (frontmatter complete, `depends-on` names WI-0002 and WI-0006); R2 pass (role, capability and outcome, unchanged); R3 pass (AC1–AC20, each a checkbox); **R4 pass — this is the one round 2 recorded as failing**, and what failed was a missing criterion rather than a written one: income had none because Q-006 and Q-007 were open, and AC16–AC18 are now written and decidable; R5 pass (eight exclusions, three of them things a reader would assume included); **R6 pass** — no question on this item is open, the criterion that failed by construction in both earlier rounds; **R7 pass on the stronger reading** — `WI-0006` is now `done`, so nothing in `depends-on` is unfinished rather than merely sequenced; **R8 pass** — `refinement-qa.md` now declares `status: recorded` and the exchange under it is finished; R9 pass, not split, re-read against the income criteria; R10 pass (the full combination table in `refinement-qa.md`, with AC19 and AC20 closing the two gaps and three combinations named as deliberately unconstrained); R11 pass (nothing is counted; the one number written down was measured first and carries `[src: run: …]`); R12 pass (one delegation, `WI-0003/Q-004`, named with its category at the head of the criteria; three assumptions under no licence, each saying so where it is made))
  - `criteria-are-decidable` → **pass** (round 2's table covers AC1–AC15 and round 3's covers AC16–AC20, each naming the invocation to run and the verdict that follows, every one observable in a throwaway store via `ENVEL_FILE` and read back with `envel list`, `envel summary` and `envel entries`)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0005`, exit 0; and the read it cannot make is written out in `## Cross-answer check — round 3`: no new answer was recorded, no answer of theirs was edited, and the only pair that ever collided on this item was settled by them at Q-006)
  - `qa-recorded-verbatim` → **pass** (all eight questions and all eight answers are in `refinement-qa.md` in full, tagged `[human]`; the four `[assumed]` decisions are tagged and each names its licence or says it has none; nothing is paraphrased and nothing is `[unresolved]`)
- **Artifacts:**
  - `tracker/items/WI-0005/item.md` (updated — AC15, AC16, AC18 amended; AC19 and AC20 appended;
    three exclusions added; `## Notes` brought up to date with `WI-0006` being `done`)
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` (updated — `status: agenda` → `recorded`,
    and round 3 appended in full)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `ready`
- **Result:** WI-0005 is Ready. Three rounds, eight questions, eight answers, and a third round
  that asked nothing: the Definition of Ready passes on all twelve criteria, with R4, R6, R7 and R8
  — the four that failed in earlier rounds — each clearing because the thing that was missing
  arrived rather than because anything was waived.

## 2026-09-11T09:34:38Z — plan v0.6.3 — architect

- **Item:** WI-0005
- **Trigger:** status `ready`, dispatched by `next` — the only runnable item on the board
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` (AC1–AC20), `history.md`, `journal.md`
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — all three rounds, and in particular the
    four `[assumed]` decisions that are this design's soft ground: the command surface under
    `WI-0003/Q-004`, and AC4's empty description, AC19's all-or-nothing refusal and AC20's listing,
    each taken under no licence
  - `tracker/items/WI-0006/item.md` and `artifacts/plan.md` — the sibling that created the
    reference, and its invalidation set, which this one is shaped after
  - `docs/architecture/overview.md` (v8), `docs/product/vision.md` (v7)
  - `docs/architecture/adr/` — all ten: `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`,
    `ADR-0006`, `ADR-0007`, `ADR-0008`, `ADR-0009`, `ADR-0010`
  - `envel/cli.py`, `envel/envelopes.py`, `envel/store.py`, `envel/dates.py`, `envel/summary.py`
    in full; `envel/money.py`'s two functions; `tests/test_cli.py` and `tests/test_entries.py` for
    the shape the test suite already uses
  - `tracker/project.yaml`, `.claude/agile-skills/spec/doc-header.md` §4 and §4b
- **Decisions:**
  - **`ADR-0011`: a correction edits the entry in place and a removal deletes it.** This is the
    decision the item turns on, and it is an ADR rather than an assumption because it falsifies a
    standing sentence of `ADR-0002` — *"`entries` is append-only within a run"* — and because its
    effects are irreversible even though the code is not. Rationale: the two append-only
    alternatives each break a criterion the stakeholder wrote. Appending a compensating entry puts
    two figures in a past summary, which `EP-001/Q-005` refuses in terms and AC8 forbids; flagging
    the old entry and appending a new one puts a branch on a field into `balance`, `figures`,
    `bounded_balance` and `entries_in`, four readers that today share one rule, and stores the
    history they said they did not want. Editing in place keeps every reader unchanged, which is
    why AC7, AC8, AC14 and AC20 need no code at all.
  - **No `format` bump and no change to `envel/store.py`.** From the documents: nothing here adds,
    removes or renames a key, so a document written before this item and one written after are both
    `format: 2`. Rationale: `ADR-0010` raised it to 2 for a shape change and a reader will ask
    whether this is another one; saying plainly that it is not is what stops someone bumping it
    defensively.
  - **The operations go in `envel/envelopes.py`.** From the documents — `ADR-0009` puts the
    operations there and the reports in `envel/summary.py`, and both new functions change a store
    and return a new one.
  - **The order of the refusals within each operation is fixed by the plan**: identity, then
    applicability, then each option's own validity, then the balance invariant. Rationale: nothing
    can be said about an entry that was not found; `--on` on an income is a refusal about the
    entry rather than about the value typed; and the invariant's message quotes a balance, which
    means nothing until the envelope is known. Same reasoning `record_spend` and `move` already
    carry.
  - **Four reversible assumptions, each with its reversal cost, and each under no delegation**: a
    non-numeric reference matches no entry and takes AC1's path rather than a new error type; the
    `fix` success line names the source envelope too when `--envelope` moved the entry; *no option
    given* is caught in `envel/cli.py` before the store is loaded, because `argparse` cannot say
    *at least one of these four* and AC6 asks for the subcommand's own usage; and the new test
    module is `tests/test_corrections.py`. The standing licence at `WI-0003/Q-004` is about
    argument style and the naming of commands and options, and none of these four is that, so
    none of them claims it.
  - **`docs/architecture/overview.md` taken to v9.** The change alters the shape of the system:
    `envelopes.py` owns seven operations rather than five, the entry list stops being append-only,
    and `## What is not decided yet` becomes empty because this is the epic's last design.
    Rationale: an overview that still calls the log append-only would be read by `implement` as a
    constraint on the very thing it is building.
  - **Nothing was put to the stakeholder.** All eight questions this item ever needed were asked
    and answered during refinement. No decision here is irreversible in a way the documents do not
    cover, and none depends on intent no document records — which is the whole of step 4's third
    branch.
  - **No defect was filed.** Nothing in the delivered code was found wrong while planning. The one
    thing worth a reader's attention — `envel entries <envelope>` can print a negative opening
    figure — was recorded by `refine` in the item's `## Notes` with the measurement, and it falls
    out of two decisions the stakeholder has already taken, so it is not a defect to file.
- **Cross-answer check:** This execution recorded no new human answer and relied on the ones
  already consumed. Checked against `WI-0005/Q-001` through `Q-008`, `WI-0003/Q-003`,
  `WI-0003/Q-004`, `WI-0001/Q-001`, `WI-0001/Q-003`, `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-005`:
  **no conflict**. `ADR-0011` quotes `EP-001/Q-005` as the reason the append-only options lose and
  reconciles nothing — the one pair of their sentences that ever collided on this item
  (`WI-0005/Q-005` against `WI-0003/Q-003`) was settled by them at `Q-006` in round 2, and nothing
  written here depends on the reading they rejected. `lint-answers --uncommitted` exits 0 over the
  two documents this execution touched.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before this transition on
    `doc.changelog.no-execution` for the `ADR-0011` row and the overview's v9 row, which this entry
    is the execution of; nothing else
  - `python3 .claude/agile-skills/scripts/validate-workspace . --resolving 'WI-0005:ready->planned+journal'`
    → exit 1, the same two findings and no others
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 33 consumed human
    answers and 2 delegations checked, 0 errors
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 231 tests`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 -m envel new|add|spend|move|entries|list` against a throwaway `ENVEL_FILE` → exit 0
    each, to read the delivered output forms the new commands have to match
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **fail**, and this transition was taken with `--force` because the gate
    cannot be satisfied from here. `validate-workspace --resolving 'WI-0005:ready->planned+journal'`
    exits 1 on two findings and nothing else: `doc.changelog.no-execution` on `ADR-0011`'s row and
    on `docs/architecture/overview.md`'s v9 row, each saying *"WI-0005's journal has no execution
    of plan at all"*. It has none because the entry you are reading is the one that records it, and
    only the transition writes it — so a version row a skill writes **during** its own execution can
    never be inside a window until after the move the gate guards. `--resolving`'s `+journal` suffix
    already downgrades this exact shape for `journal.execution.missing` and does not cover
    `doc.changelog.no-execution`, which is the same fact about the same pending entry. This is the
    identical finding `plan` recorded on `WI-0006`; it has now cost two executions. Every other
    gate ran and passed, and `validate-workspace` exits 0 immediately after this move
  - `every-criterion-is-addressed` → **pass** — the `## Acceptance criteria mapping` table in
    `plan.md` has one row for each of AC1 to AC20, each naming the step or steps that satisfy it
    and the specific case that demonstrates it. Four of them — AC7, AC8, AC14, AC20 — name no step
    on purpose and say so: they fall out of `ADR-0011` leaving every reader unchanged, and their
    row carries the observation that proves it rather than a step that builds it
  - `project-commands-resolved` → **pass** — `tracker/project.yaml` already names both, they were
    both run this execution, and `ADR-0005` records what each does and does not check:
    `python3 -m unittest discover -s tests -t .` → exit 0, 231 tests; `python3 -m compileall -q
    envel tests` → exit 0. `commands.build` stays `null`, which is honest for a package with no
    build step
  - `decisions-recorded` → **pass** — `## Decisions and ADRs` in `plan.md` is a table of every
    choice this plan makes, each pointing either to an ADR, to the document it was read from, or to
    an entry under `## Assumptions` stating what reversing it costs. One ADR was written
    (`ADR-0011`); four assumptions were recorded, each with its reversal cost and each saying it
    was taken under no delegation
  - `plan-is-executable-without-you` → **pass** (advisory) — read back cold, the twelve steps name
    the file each touches, the order of the refusals, which module parses which value, and what is
    true afterwards. The one place a developer must still choose is the exact wording of a message,
    which is inside the stakeholder's standing licence at `WI-0003/Q-004`
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule
    documents-at-risk-are-enumerated --item WI-0005`, exit 0) — 29 rows, written from a read of
    `docs/` rather than from memory: twelve rows across all ten standing ADRs, twelve on
    `docs/architecture/overview.md`, five on `docs/product/vision.md`, two of which are the
    `engagement-state` rows — `owned-by-ending`, and nobody here touches them. `lint-documents`
    also reads eleven binding ADRs and no deliverable document. The central
    row is `ADR-0002`'s append-only sentence, which `ADR-0011` falsifies and `implement` must repair
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0; and the read it
    cannot make is under `**Cross-answer check:**` above — no answer of theirs was edited and no
    ADR written here reconciles two of their sentences)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0 over both documents this
    execution wrote; one absolute claim in `ADR-0011`'s reversibility paragraph was reported
    unsourced on the first run and was given its citations rather than reworded)
- **Artifacts:**
  - `tracker/items/WI-0005/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` (new, v1)
  - `docs/architecture/overview.md` (v8 → v9)
  - `tracker/board.md` (regenerated)
- **Status:** `ready` → `planned`
- **Result:** `WI-0005` is planned. One ADR carries the item — a correction edits the entry where it
  sits and a removal deletes it — and the reason it is worth an ADR is that it falsifies
  `ADR-0002`'s append-only sentence and leaves every reader in the tool untouched, which is what
  makes four of the twenty criteria fall out of the design instead of being built. Twelve steps,
  twenty mapped criteria, four reversible assumptions, and a 29-row invalidation set for
  `implement` to close.

## 2026-09-11T09:35:55Z — implement v0.6.1 — developer

- **Item:** WI-0005
- **Trigger:** status `planned`, dispatched by `next` — the only runnable item on the board
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` (AC1–AC20), `history.md`, `journal.md`
  - `tracker/items/WI-0005/artifacts/plan.md` — twelve steps, the AC mapping, four assumptions,
    the 29-row invalidation set, `## Deliverable documents` (`none`) and eleven binding ADRs
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — the four `[assumed]` decisions and where
    a disagreement about each one lands
  - `tracker/items/WI-0005/questions/Q-001.md` … `Q-008.md` — all `answered`, none since the last
    entry, so nothing to re-read under step 2
  - `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md`, and the ten
    standing ADRs the plan names as binding
  - `docs/architecture/overview.md` (v9), `docs/product/vision.md` (v7)
  - `envel/cli.py`, `envel/envelopes.py`, `envel/store.py`, `envel/summary.py`, `envel/dates.py`,
    `envel/money.py`; `tests/test_cli.py` and `tests/test_entries.py`
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both set and both run
- **Decisions:**
  - **A fresh start, not a resume.** `git branch` shows no `wi/WI-0005` and the history's last row
    is `ready → planned` by `plan`, not a send-back from `verifying` or `in-review`. There is no
    partial work to reconcile with and no defect report to read first.
  - **Branched from `main` at `73a5c7a`**, which carries this item's own plan, `ADR-0011` and the
    overview at v9.
- **Cross-answer check:** none — this entry edits no document.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0005 main` → exit 0
  - `git rev-parse --abbrev-ref HEAD` → `wi/WI-0005`
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range is empty at this moment, so there is nothing for it to inspect yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (advisory; decided at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:** branch `wi/WI-0005`, created from `main` at `73a5c7a`. No commit yet.
- **Status:** `planned` → `in-progress`
- **Result:** Implementation has started. The branch exists and the item is `in-progress`, so an
  interruption from here leaves a truthful status. The closing entry reports the work.

## 2026-09-11T10:00:14Z — implement v0.6.1 — developer

- **Item:** WI-0005
- **Trigger:** status `in-progress`, this skill's own opening transition at 09:35:55Z
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` (AC1–AC20), `artifacts/plan.md` (twelve steps, the AC mapping,
    four assumptions, the 29-row invalidation set, eleven binding ADRs), `history.md`
  - `tracker/items/WI-0005/artifacts/refinement-qa.md` — the four `[assumed]` decisions
  - `docs/architecture/adr/ADR-0011`, and the ten standing ADRs the plan names as binding; each of
    the 29 invalidation rows was reopened in the document it names
  - `docs/architecture/overview.md` (v9), `docs/product/vision.md` (v7)
  - `envel/cli.py`, `envel/envelopes.py`, `envel/store.py`, `envel/summary.py`, `envel/dates.py`,
    `envel/money.py`; `tests/test_cli.py`, `tests/test_entries.py`
- **Decisions:**
  - **Every plan step was executed as written, in order.** No step turned out impossible or
    differently shaped, so nothing about *what* is delivered was adapted.
  - **The refusal order is the plan's, and it shows in the code.** `correct` refuses in six steps —
    no such entry, a move, an income given a date or a description, an envelope that does not
    exist, an amount at or below zero, a date in the future — and only then takes a copy. That is
    what makes AC19 a property of the control flow rather than a check: there is no point at which
    a document has been changed and a refusal is still possible.
  - **The sign of a corrected amount is read off the entry, not off its kind.** A spend stores a
    negative `cents` and income a positive one, so `correct` writes `-cents if the entry's cents is
    negative else cents`. Rationale: `ADR-0002` makes a balance the plain sum with no branch on
    `kind`, and writing the typed number as-is would turn a spend into an income-shaped entry and
    silently double an envelope. The plan named this as a risk and a mutation confirmed the test
    catches it — 11 failures.
  - **`remove` reads `entry.get("on")` rather than importing `summary.entry_date`.** The plan named
    the temptation: `envel/summary.py` already has the function, and taking it would reverse the
    dependency direction `docs/architecture/overview.md` states. AC11 wants only the date the entry
    itself carries, and an income has none, which is AC17.
  - **`envel fix <ref>` with no option is caught before `store.load`.** The store file is not even
    opened, which is why the test can assert its bytes are identical rather than its contents.
  - **Two test cases seed the store file directly rather than through the commands.** AC8 and AC14's
    month-crossing half cannot be observed otherwise: `envel new` stamps `created` with now, and
    `WI-0003` AC4 gives a row only to an envelope that existed by the end of the month. The same
    device `tests/test_cli.py::Entries` already uses, for the same reason. Recorded as a deviation
    in `impl-report.md` because it is a deviation in the evidence, not in the behaviour.
  - **`ADR-0002` repaired as an erratum, not superseded.** Its `entries` bullet said the list is
    *"append-only within a run"*, which this change makes false. The decision — one JSON document
    holding envelopes and a dated entry log — is untouched, no code has to change to satisfy the
    new text, and the two clauses that did not change were re-read against the code and kept. That
    is `spec/doc-header.md` §4b's erratum, and it is the route `ADR-0002` has been repaired by
    twice before.
  - **Nothing was escalated, because nothing needed to be.** Every choice above is inside the
    plan's latitude or is the plan's own. No decision would have been expensive to reverse and none
    is behaviour a user would notice that no criterion covers.
  - **Nothing unrelated was fixed.** `git diff --stat main..HEAD` touches two source files, two test
    files, one ADR and this item's tracker files, and nothing else.
- **Cross-answer check:** **none edited.** The two paragraphs of `docs/product/vision.md` that
  describe correcting are sourced to `WI-0005/Q-002` through `Q-007` — the stakeholder's own
  answers, with a return address on them — and they are now **true** rather than overtaken: what
  was built is what those answers say. They were reopened, read against the delivered behaviour,
  and left exactly as they are, disposed `verified-still-true` in `impl-report.md`. The one
  document this execution did write, `ADR-0002`, carries no `[src: <ITEM>/Q-nnn]` on the clause
  that was changed; it was false because the **code** changed, which is the ordinary repair.
  `lint-answers --changed-since main` exits 0.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0005 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 299 tests`, `OK` (231 on `main`;
    this item adds 68)
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0005 wi/WI-0005` → exit 0,
    `all 3 commit(s) on main..wi/WI-0005 name WI-0005`
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0005`
    → exit 0, window `12 document(s) in 12 path(s) in scope — 1 path(s) differ from main under
    docs, plus 12 document(s) named by WI-0005's plan`
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item
    WI-0005 --changed-since main` → exit 0, `1 document(s) written under docs/ on this branch; 12
    named by the plan`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before this transition on
    `doc.changelog.no-execution` for `ADR-0002`'s v4 row, and nothing else; re-run after
  - six mutations applied and reverted (an empty description stored rather than the key deleted;
    the invariant checked against the live store; `next-ref` lowered on a removal; the sign of a
    corrected amount dropped; a move made correctable; `--on` allowed on an income) → 3, 7, 1, 11,
    5 and 7 failing tests respectively, and `OK` again after each revert
  - enumeration commands for the quantified claims, with their output in `impl-report.md`:
    `grep -n '\["ref"\]\|"ref":\|next-ref\|take_ref' envel/*.py` → 21 lines;
    `grep -n '"move"' envel/*.py` → 11 lines;
    `grep -n '^from \. import\|^import ' envel/*.py` → 15 lines;
    `grep -n 'print(\|sys.exit' envel/envelopes.py envel/summary.py envel/store.py envel/money.py
    envel/dates.py` → no matches
- **Gates:**
  - `tests-pass` → **pass** — `python3 -m unittest discover -s tests -t .` on the branch head after
    the last commit: exit 0, `Ran 299 tests`, `OK`
  - `lint-clean` → **pass** — `python3 -m compileall -q envel tests`, exit 0. `ADR-0005` records
    what this does and does not check, and it is not read as more than compilation
  - `workspace-valid` → **fail**, and this transition was taken with `--force` because the gate
    cannot be satisfied from here. `validate-workspace --resolving
    'WI-0005:in-progress->verifying+journal'` exits 1 on one finding and nothing else:
    `doc.changelog.no-execution` on `ADR-0002`'s v4 row, saying *"no execution of implement on
    WI-0005 was running then (its entries close at 2026-09-11T09:35:55Z)"*. The row is stamped
    09:56:03Z, which is **inside** this execution — after its opening entry and before the closing
    one — but the window the validator derives ends at the last entry **written**, and the closing
    entry is the one this transition is appending. This is the same toolkit finding `plan` recorded
    on this item and on `WI-0006`, in its second shape: there it was a row written before the only
    entry existed, here it is a row written between a skill's two entries. `--resolving`'s
    `+journal` suffix downgrades exactly this shape for `journal.execution.missing` and does not
    cover `doc.changelog.no-execution`. Every other gate ran and passed, and `validate-workspace`
    exits 0 immediately after this move. Recorded as a fail rather than argued into a pass
  - `every-criterion-has-a-test` → **pass** — `impl-report.md`'s `## Acceptance criteria evidence`
    names a test function for each of AC1 to AC20, and none is demonstrated by reading code. Six
    mutations were applied and reverted to check the tests would fail if the behaviour were
    removed; all six were caught, at 3, 7, 1, 11, 5 and 7 failures
  - `commits-reference-the-item` → **pass** — `check-commit-refs WI-0005 wi/WI-0005`, exit 0, all
    three commits on `main..wi/WI-0005`
  - `no-unplanned-scope` → **pass** (advisory) — `git diff --stat main..HEAD` is
    `envel/cli.py`, `envel/envelopes.py`, `tests/test_cli.py`, `tests/test_corrections.py`,
    `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` and this item's tracker files.
    Steps 1–5 are `envelopes.py`, 6–8 are `cli.py`, 9–10 are the tests, 11 is the ADR
  - `cross-answer-consistency` → **pass** — `lint-answers --changed-since main`, exit 0, over a
    window the run printed as `1 path(s) differ from main under docs`. The read it cannot make is
    under `**Cross-answer check:**` above
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main --plan-documents WI-0005`,
    exit 0. The **scope** the run printed: `12 document(s) in 12 path(s) in scope — 1 path(s)
    differ from main (73a5c7a) under docs, plus 12 document(s) named by WI-0005's plan`. The window
    is not empty and it contains `ADR-0002`, the one document this execution wrote
  - `document-writes-are-declared` → **pass** — `lint-documents --rule document-writes-are-declared
    --item WI-0005 --changed-since main`, exit 0, reporting `1 document(s) written under docs/ on
    this branch; 12 named by the plan`. All 27 previously open rows of the invalidation set now
    carry a disposition: one `to-update` (`ADR-0002`), 26 `verified-still-true`, and the two
    `engagement-state` rows stay `owned-by-ending` and were not touched
- **Artifacts:**
  - `tracker/items/WI-0005/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0005/artifacts/plan.md` (dispositions written into the invalidation set;
    nothing else in it changed)
  - `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` (v3 → v4, one erratum)
  - branch `wi/WI-0005`, commits `a88691f`, `2a3499d` and the tracker commit above, over
    `main..wi/WI-0005`
- **Status:** `in-progress` → `verifying`
- **Result:** `envel fix` and `envel remove` are built and every one of the twenty criteria has a
  test. The design held: `envel/summary.py`, `envel/store.py`, `envel/money.py` and `envel/dates.py`
  are byte-identical to `main`, which is what AC7, AC8, AC14 and AC20 rested on. One document was
  false afterwards — `ADR-0002`'s append-only clause — and it was repaired as an erratum; the other
  26 open rows were reopened and found still true, with the enumeration each quantified claim owes
  recorded in `impl-report.md`.

## 2026-09-11T10:28:31Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0005
- **Trigger:** status `verifying` — `next` dispatched this skill as the owner of that status; WI-0005 was the only runnable candidate on the board.
- **Inputs read:**
  - `tracker/items/WI-0005/item.md` — the twenty acceptance criteria, read **first** and used as the only standard.
  - `tracker/items/WI-0005/artifacts/plan.md` — the twelve steps, the binding-ADR list, the 29-row invalidation set, the four assumptions.
  - `tracker/items/WI-0005/artifacts/impl-report.md` — read **after** the criteria and after this execution's own evidence was gathered; cited nowhere as evidence for a criterion.
  - `docs/architecture/adr/ADR-0001` … `ADR-0011` — all eleven binding ADRs, in full, for the conformance verdicts.
  - `docs/architecture/overview.md` and `docs/product/vision.md` — the sentences named by the invalidation set's 26 `verified-still-true` rows.
  - `tracker/project.yaml` — the test and lint commands.
  - The code at branch head `1695487b4a9962308019729f446b21ae2f216e11` on `wi/WI-0005`, and `main` in a temporary worktree for one comparison.
- **Decisions:**
  - **Pass, all twenty criteria.** Each verdict rests on a command this execution ran against the branch head with the output quoted; roughly 110 invocations of the tool against scratch stores addressed by `ENVEL_FILE`.
  - **No send-back and no bug item.** No criterion of this item failed, so there is nothing to send back. The one candidate for a bug — `envel entries --month 2026-01` listing a spend whose date was corrected to a month before its envelope existed, while `envel summary 2026-01` prints `no envelopes existed in 2026-01` — was **not** filed. It is reachable on `main` with no correction at all: a worktree at `main` running `envel spend groceries 5.00 --on 2026-01-05` produces the same pair of outputs. It is `WI-0003` AC7 meeting `WI-0006`'s listing, and neither criterion is false, so filing a bug would be legislating rather than reporting.
  - **AC15 and AC19 were treated as criteria whose subject is other criteria.** Both name their covered criteria by ID; each named criterion got its own invocation and its own verdict, rather than a green suite standing in for the reading. AC15: nineteen obligations, nineteen separate runs with both streams measured in bytes. AC19: eleven combinations, each pairing an accepted option with a refused one.
  - **AC19's non-intersection stated and waived by name.** Nothing executable exercises AC19 together with the refusals of AC1, AC6, AC9, AC10, AC13 or AC18 — the suite's four AC19 cases cover AC16, AC5 and AC3 only. Waived for those six, because AC19 is one mechanism rather than nine: `correct` deep-copies after all six early refusals and the seventh reads the candidate, while `cli` saves only what an `Ok` carries. All six were verified here by hand.
  - **No criterion judged `ambiguous` and none `substituted`.** Every criterion names an observation this environment can make. AC8's month-crossing case needed a store whose envelopes existed in an earlier month, which was seeded by editing the store file's `created` stamps — the *setup* was seeded, the observation AC8 names was made by the tool.
  - **One finding recorded rather than escalated.** This item's change moved `envel/cli.py`'s `if result.changed:` from line 165 to 217, leaving three citations pointing at 165: `plan.md:44`, `plan.md:210` and `ADR-0011:101`. All three were correct when written and all three still *resolve*, so nothing mechanical notices; the claim each supports is still true. Not a send-back (no criterion is about a line number), not a bug (no delivered behaviour failed), and not mine to edit. Recorded in `## Defects found` for `review-close`, with the structural point: `ADR-0011` was written by this item's own `plan` and is therefore in no invalidation set.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 299 tests in 40.040s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`, 7 items and 13 documents
  - `scripts/lint-documents --rule adr-conformance-is-decided --item WI-0005` → exit 0, `11 binding ADR(s), 11 conformance row(s)`
  - `scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0005` → exit 0, `29 invalidation entr(y/ies) against 29 row(s)`
  - ~110 invocations of `envel` under `ENVEL_FILE`, each recorded with its exit code and output in `verify-report.md`: `fix` and `remove` across all twenty criteria, fifteen refusal paths, eleven AC19 combinations, nine extra boundaries, and the readers `list`, `summary` and `entries` run as separate processes after each.
  - 14 source mutations, each applied, run against the full suite and reverted from a pristine copy → every one `FAILED`; the suite is `OK` again afterwards and `git status` is clean.
  - `git worktree add /tmp/.../mainwt main`, three `envel` commands there, `git worktree remove --force` → exit 0, used to establish that the summary/listing divergence predates this branch.
  - `git diff --stat main..HEAD`, `git diff main..HEAD -- envel/`, `git show main:envel/cli.py` → the diff read against the plan; only `envel/cli.py`, `envel/envelopes.py`, the two test modules and `ADR-0002` are touched, and every hunk traces to a plan step.
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, `Ran 299 tests`, `OK`, run by this execution on the branch head)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (the `## Criteria` table gives, for each of AC1–AC20, a command this execution ran and its actual quoted output; the implementation report is cited for no criterion)
  - `negative-cases-exercised` → **pass** (every refusal *triggered*: 15 refusal paths, 11 AC19 combinations, 9 further boundaries — the below-zero rule checked one cent either side on both AC9 and AC18, the future-date rule at today and tomorrow, `remove` with file descriptor 0 closed)
  - `a-criterion-about-criteria-is-read` → **pass** (AC15 and AC19 each name their covered criteria by ID with a per-criterion verdict read from the text; AC19's non-intersection is stated in those words and waived by name for six combinations with the reason)
  - `adr-conformance-is-decided` → **pass** (`scripts/lint-documents --rule adr-conformance-is-decided --item WI-0005` → exit 0; eleven verdicts, all `conforms`, each quoting a clause of that ADR's `## Decision` and naming the file and line that satisfies it)
  - `invalidation-set-is-disposed` → **pass** (`scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0005` → exit 0; all 29 rows disposed, the 26 `verified-still-true` ones reopened and read against the branch head with enumerations and falsifiers, the one `to-update` row confirmed at `ADR-0002` v4 with a change-log row, the two `owned-by-ending` rows untouched — both documents are absent from the branch's diff)
  - `tests-would-fail-without-the-change` → **pass** (, advisory (14 mutations, each reverted: `find_entry` falling back to the first entry → 6 failures; the future-date refusal → 3; the unknown-envelope refusal → 1 failure and 2 errors; the invariant in `correct` → 7; the invariant in `remove` → 5; the zero/negative refusal → 5; the move refusal → 5; `correct` mutating the caller's store → 5; an empty description stored → 3; the date on every removal line → 2; the no-option check → 1; the sign of a corrected amount → 11; `next-ref` lowered on a removal → 1; `--on` accepted on income → 6))
- **Artifacts:**
  - `tracker/items/WI-0005/artifacts/verify-report.md` — created.
  - `tracker/items/WI-0005/item.md` — all twenty criteria ticked `- [x]`, each against a command in the report.
  - No bug item filed. No file under `docs/` written or touched by this execution.
- **Status:** `verifying` → `in-review`
- **Result:** WI-0005 passes verification against the branch head at `1695487`. All twenty acceptance criteria were independently demonstrated, all eleven binding ADRs conform with a quoted clause each, and all 29 invalidation entries are disposed with the 26 still-true claims reopened and read. Fourteen mutations confirm the tests bite. One finding — three `envel/cli.py:165` citations that this item's own change pushed off their line — is recorded for `review-close` rather than escalated, because no criterion and no delivered behaviour is wrong.

## 2026-09-11T10:38:33Z — review-close v0.14.1 — reviewer

- **Item:** WI-0005
- **Trigger:** status `in-review` — `next` dispatched this skill as the owner of that status; WI-0005 was the only runnable candidate on the board, and `engagement-state EP-001` reported `active`.
- **Inputs read:**
  - `tracker/items/WI-0005/item.md`, `history.md` and `journal.md` in full — ten history rows, ten journal entries, twenty ticked criteria.
  - `artifacts/plan.md` — the twelve steps, the 29-row invalidation set, the eleven binding ADRs, the four reversible assumptions.
  - `artifacts/impl-report.md` and `artifacts/verify-report.md` — the declared deviations and the declared gaps.
  - All eight questions on the item, and their `## Consequences`.
  - **The diff itself**, `main..wi/WI-0005` over `envel/`, `tests/` and `docs/` — nine hunks, read hunk by hunk and mapped to plan steps.
  - All eleven ADRs in full, `docs/architecture/overview.md`, `docs/product/vision.md`.
  - `tracker/waiting/EP-001.md` deliberately **not** read: it is the epic's, and this is an item close.
- **Decisions:**
  - **Accept and close as `delivered`.** All thirteen Definition of Done criteria pass, recorded one by one with their own evidence in `review.md`. Every hunk of the diff serves a plan step; nothing in it serves neither a criterion nor a step.
  - **D7's own question answers `yes`, and the document is `ADR-0011`.** The workspace holds thirteen documents under `docs/`; the invalidation set names twelve. The thirteenth is `ADR-0011`, written by **this item's own `plan`** from the design this change implements — a set lists documents a change could make false, and a document the plan writes from that same change is not a candidate for its own list. Reading it against the branch head: every clause of its `## Decision` is true, but `## Decision` 5's citation `[src: envel/cli.py:165]` now points at `elif arguments.command == "spend":`, because this change moved `if result.changed:` to line 217. `plan.md:44` and `plan.md:210` drifted the same way.
  - **That finding is dispatched, not banked.** It is not a criterion failure, so not a send-back; not a defect in delivered behaviour, so not a bug; and a document repair is `answer-questions`', so `WI-0005/Q-009` was filed — non-blocking, addressed to the architect, **before** this close — and disposed `question-filed:WI-0005/Q-009` in `## Accepted gaps`. Filed rather than written into `## Notes`, because the orchestrator dispatches on open questions and item status and on nothing else.
  - **Two findings recorded with no work deferred.** (1) `envel fix` is the first command in this tool that can succeed while changing nothing: a correction to the value already held exits 0 and rewrites the file with byte-identical content, which narrows how `overview.md`'s beat 3 reads without making it false — no reader of the store can tell, and `refine` listed the case among the three deliberately unconstrained. (2) `correct` infers *income* from the absence of `on` and then says so in its message; sound today under `ADR-0006`, and a note for whoever adds a third kind that carries no date.
  - **No finding against the change itself.** `correct`'s six positional parameters are at the edge of comfortable but are the shape `record_spend` and `move` already have; a second convention for one function would be worse. No duplicated rule, no swallowed error, no misleading name.
  - **The other ten declared gaps are `no-owner`**, each with its reason in the gap cell. The one worth naming is `--on` setting a date before the envelope existed: it is **not new** — `verify` reached the identical pair of outputs on `main` in a worktree — so it is `WI-0003` AC7 meeting `WI-0006`'s listing, and neither criterion is false.
  - **This close does not end the engagement.** `Q-009` is open, so `engagement-state EP-001` cannot report `at-rest`; the ending belongs to the execution dispatched after it is answered. The decision was the script's, not a read of the board.
- **Cross-answer check:** `none` — this execution consumed no human answer. The eight human answers on this item were consumed by `answer-questions` during refinement and were checked then; `Q-009` is addressed to the architect and is unanswered. `lint-answers --context work-item --changed-since main` → exit 0 over 33 consumed human answers and 2 delegations spent in the workspace.
- **Questions raised:** WI-0005/Q-009
- **Commands:**
  - `git diff main..HEAD -- envel/ tests/ docs/`, `git diff --stat main..HEAD`, `git show main:envel/cli.py` → the diff read hunk by hunk and the citation drift established
  - `check-commit-refs WI-0005 wi/WI-0005` → exit 0, *"all 5 commit(s) on main..wi/WI-0005 name WI-0005"*
  - `check-verify-freshness WI-0005 wi/WI-0005` → exit 0, *"verified at 1695487b; wi/WI-0005 has moved to 62f02d98 but only the record changed (5 file(s) under tracker/ or docs/)"*
  - `git worktree add --detach /tmp/…/trial main` → exit 0; `git -C … merge --no-ff wi/WI-0005` → merge commit `4bb7630a7497ccab4b3c62a7228882c48eaaa433`; `python3 -m unittest discover -s tests -t .` **inside the trial** → exit 0, `Ran 299 tests in 40.261s`, `OK`; `git worktree remove --force` → exit 0; `git rev-parse main` → `73a5c7a601f80c76edcf3cc0de0b11596ac83bc8`, the same sha as before the trial
  - `lint-documents --rule adr-conformance-is-decided --item WI-0005` → exit 0, `11 binding ADR(s), 11 conformance row(s)`
  - `lint-documents --rule invalidation-set-is-disposed --item WI-0005` → exit 0, `29 invalidation entr(y/ies) against 29 row(s)`
  - `lint-documents --rule accepted-gaps-are-dispatchable --item WI-0005` → exit 0, `11 accepted gap(s)`
  - `lint-documents --rule engagement-state-is-restated --item WI-0005 --context work-item` → exit 0, `NOT APPLICABLE`
  - `lint-claims --context work-item --changed-since main` → exit 0; `lint-answers --context work-item --changed-since main` → exit 0; `check-epic-signoff WI-0005` → exit 0
  - `validate-workspace .` → exit 0, `0 errors, 0 warnings`; `board-gen .` → wrote the board
  - D12's own reads: `grep -n 'ref"\]\|"ref":\|next-ref\|take_ref' envel/*.py` → 21 lines; `grep -n '"move"' envel/*.py` → 11 lines; and the boundary runs — the highest entry removed then a new one recorded, `envel fix 4 --amount 5` and a fresh envelope's `0.00`, a refused fix and a no-op fix compared by mtime and md5
- **Gates:**
  - `definition-of-done` → **pass** (D1–D13 walked one at a time in `review.md`'s table, each with its own result and evidence; D7 confirmed against the plan's enumerated set and D13 answered by the list naming all eleven ADRs in the index)
  - `engagement-state-is-restated` → **pass** (applicable — an item close.** `lint-documents` says so in those words: *"an item close is not an ending, and the sections are the ending's"*. Both sections were separately confirmed untouched — neither `overview.md` nor `vision.md` appears in this branch's diff)
  - `accepted-gaps-are-dispatchable` → **pass** (`lint-documents --rule accepted-gaps-are-dispatchable --item WI-0005` → exit 0; eleven gaps, ten `no-owner` with their reasons, one `question-filed:WI-0005/Q-009` filed before this close)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` → exit 0; the verified commit is the last one touching `envel/` or `tests/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → exit 0, all 5 commits on `main..wi/WI-0005`)
  - `tests-pass-on-the-merge-result` → **pass** (run inside the detached trial worktree on the merge commit `4bb7630a`, not on the branch: exit 0, `Ran 299 tests`, `OK`)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, 7 items and 13 documents)
  - `record-is-reconstructible` → **pass** (. From the tracker, `docs/` and `git log` alone: *what was built* — two subcommands, `envel fix <ref>` and `envel remove <ref>`, over `find_entry`, `envelopes_below_zero`, `correct` and `remove`; *why* — `EP-001/Q-005`, where the stakeholder chose correction over a history of their own typos; *which skill decided what* — `refine` took the scope across three rounds, `plan` took the one design decision as `ADR-0011`, `implement` built it and repaired `ADR-0002` as an erratum, `verify` demonstrated all twenty criteria, this review accepted; *what questions arose and how they resolved* — eight to the stakeholder across two refinement rounds, all answered and quoted verbatim in `refinement-qa.md` and in the criteria they produced, plus `Q-009` open to the architect; *what verification found* — no defect, with ~110 recorded invocations and fourteen mutations that all bit)
  - `claims-are-sourced` → **pass** (over a scope that could have found something: `lint-claims --context work-item --changed-since main` → exit 0, reporting its own scope as *"1 document(s) in 1 path(s) differ from main (73a5c7a) under docs; citations: every markdown file in the workspace"* — non-empty, and containing `ADR-0002`, the one document this branch wrote)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0 over 33 consumed human answers and 2 delegations; this execution consumed none of its own)
  - `epic-sign-off` → **pass** (by subject** — `check-epic-signoff WI-0005` reports *"WI-0005 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only"*, exit 0; the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/check-epic-signoff WI-0005 --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0005:in-review->done+journal'` exited 0)
- **Artifacts:**
  - `tracker/items/WI-0005/artifacts/review.md` — created.
  - `tracker/items/WI-0005/questions/Q-009.md` — filed, non-blocking, addressed to the architect.
  - `tracker/board.md` — regenerated.
  - No bug item filed. No file under `docs/` written by this execution. The merge commit is not named here because it does not exist yet; `scripts/record-merge` puts it in `item.md` once it does.
- **Status:** `in-review` → `done`
- **Result:** WI-0005 is accepted and closed as `delivered` — the last of `EP-001`'s six items. Twenty of twenty criteria settled with evidence, all thirteen Definition of Done criteria passed, the merge result tested green at 299 tests, and the trunk confirmed unmoved by the trial. The close does not end the engagement: `Q-009` is open, so `EP-001` cannot reach rest until the architect answers it.

## 2026-09-11T10:43:19Z — answer-questions v0.6.3 — architect

- **Item:** WI-0005
- **Trigger:** `WI-0005/Q-009` was `status: open` and `addressed-to: architect`, which makes it answerable under `next` step 3. The item itself is `done` and was never suspended — `Q-009` is `blocking: false` — so this execution makes no transition.
- **Inputs read:**
  - `tracker/items/WI-0005/questions/Q-009.md` — the only open question on the item; the other eight are `answered`, `answered-by: human`.
  - `tracker/items/WI-0005/artifacts/plan.md`, `review.md` and `verify-report.md` — where the defect was first recorded and where the three occurrences were named.
  - `.claude/agile-skills/spec/doc-header.md` §4b, *the repair kinds table* — the section that decides this question.
  - `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` v1 and `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` v1, both in full.
  - `envel/cli.py` and `envel/envelopes.py` at the branch head, and `git show 73a5c7a:envel/cli.py` and `git show 73a5c7a:envel/envelopes.py` for what each citation pointed at before this item.
  - All twenty-five `envel/*.py:<line>` citations in `docs/`, resolved one at a time against the merged code.
- **Decisions:**
  - **Q-009, option A, answered from an existing document — route 1, the best kind.** `spec/doc-header.md` §4b names exactly two legal repairs to an ADR at `status: accepted`, and `provenance` is this case almost word for word: add a citation to an existing sentence, the assertion unchanged, only the source new, and the new citation resolving. Both conditions hold — `ADR-0011` `## Decision` 5 still says exactly what it said, and `envel/cli.py:217` is `if result.changed:`, the statement the sentence is about. §4b's non-negotiable line settles that this is a correction and not a rewrite: no reader has to change any code to satisfy the new text, so `ADR-0011` is not superseded and the bump is 1 → 2.
  - **B and D refused, with their own reasons.** B — repair with no version bump — is refused because §4b requires a matching change-log row and a version bump for every correction, and a document whose text changed with nothing in its change log saying so is the habit those rules exist to prevent. D — leave them — is refused because a citation that resolves to the wrong line is this workspace's own *"appearance of evidence"* failure with better camouflage, and nothing mechanical would surface it again.
  - **A fourth occurrence found and repaired under the same policy.** Resolving all twenty-five code citations in `docs/` turned up `ADR-0010` `## Decision` 4, whose `[src: envel/cli.py:140]` for *"the file is saved only when a command changes something"* now points at an `argparse` comment. It is **not** this item's doing — on `main` before `WI-0005`, line 140 was a closing parenthesis inside a dispatch branch, so `WI-0006` had already moved it. Repaired anyway, to `:217`, with its own `provenance` row and bump: this question settles the policy for exactly this shape, and that sentence is a standing clause of a `## Decision` rather than a dated statement. Repairing one instance while leaving an identical one found in the same pass would be the narrower reading of the question and the worse answer to it.
  - **Three occurrences deliberately left alone, each for the same reason.** `ADR-0010` `## Context`'s `[src: envel/envelopes.py:92]` — the line is byte-identical to what it was on `main`, so nothing moved it here, and the sentence is a dated statement about the store as it was when `WI-0006` was designed. `tracker/items/WI-0003/artifacts/impl-report.md:26` and `tracker/items/WI-0006/artifacts/plan.md:280`, which also cite `envel/cli.py:140` — both belong to closed items and both are records of what an execution read at a moment. Repairing a dated statement is rewriting history, not fixing a citation.
  - **Option C's second half was not answered, and is left for `retro`.** Whether `path:line` is the right citation form for a claim about a statement that keeps moving is a real design question about the record, and this is its third cost in this engagement. It is not filed as a question: nobody is blocked, all six items are `done`, and there is no item to hang it on. It is written into `Q-009`'s `## Answer` so that the retrospective — which reads the engagement's own trail — finds it.
  - **Step 6a was deliberately not executed, and the reason was measured rather than assumed.** The skill says a document changed on an item's branch belongs in that item's invalidation set. A probe row for `ADR-0011` was added to `plan.md`'s set and `lint-documents --rule invalidation-set-is-disposed --item WI-0005` was run: it failed — *"ADR-0011 … is in WI-0005's invalidation set and has no row in verify-report.md's `## Invalidation set`"*. The probe was reverted and the gate is green again at 29/29. The gate checks the plan's set against the **verification report's** table, and that report is `verify`'s, a skill that has already run and cannot run again on a `done` item. So after a close, step 6a cannot be executed: it turns a cosmetic defect into a failing gate. Nothing is lost — `review.md` already names `ADR-0011` under *"Did this change falsify a document the set does not name?"* and points at this question.
  - **No scope was widened and no acceptance criterion was touched.** Step 3b does not apply: the answer implies no work no item records. All twenty of `WI-0005`'s criteria are exactly as `verify` ticked them.
- **Cross-answer check:** `none` — this execution consumed no human answer. `Q-009` is `addressed-to: architect` and was answered by this skill from `spec/doc-header.md` §4b, so §4a's obligation, which attaches to questions moving to `answered` with `answered-by: human`, does not arise. Checked against: none — the eight human answers on this item were consumed during refinement and checked then, and nothing in this answer touches a sentence sourced to any of them. `lint-answers --context work-item --changed-since main` → exit 0 over 33 consumed human answers and 2 delegations spent.
- **Questions raised:** none
- **Commands:**
  - `grep -rnoE '\[src: envel/[a-z_]+\.py:[0-9]+\]' docs/` → 25 citations, each resolved with `sed -n <n>p` against the merged code
  - `git show 73a5c7a:envel/cli.py`, `git show 73a5c7a:envel/envelopes.py` → what `:165`, `:140` and `:92` pointed at before this item
  - `sed -n 217p envel/cli.py` → `    if result.changed:` — the statement both repaired citations now name
  - `lint-documents --rule invalidation-set-is-disposed --item WI-0005` → exit 0 at 29/29 before the probe, exit 1 with the probe row in place, exit 0 again after reverting it
  - `lint-documents --rule adr-conformance-is-decided --item WI-0005` → exit 0
  - `lint-answers --context work-item --changed-since main` → exit 0
  - `validate-workspace .` → exit 0, `0 errors, 0 warnings`; `board-gen .` → wrote the board
  - `git diff --quiet main -- docs/architecture/overview.md docs/product/vision.md` → both unchanged, which is how the engagement-state gate was checked rather than asserted
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `## Consequences` was reopened and the change is there: `ADR-0011:101` and `ADR-0010:79` both read `[src: envel/cli.py:217]`; both headers read `version: 2`, `updated-by: answer-questions`, `updated-for: WI-0005`; each has one new `## Change log` row and one `## Corrections` row of kind `provenance`, with `## Corrections` last; `plan.md` carries `envel/cli.py:217` twice and `envel/cli.py:165` nowhere. No `envel/cli.py:165` survives in any standing document except inside the two correction rows that quote it, which is what those rows are for.
  - `answered-from-the-record` → **pass**. Route 1: the answer is `spec/doc-header.md` §4b's repair-kinds table, quoted in `## Answer` with the toolkit citation form, plus the §4b line that decides correction from rewrite. Nothing here was decided by preference.
  - `escalation-is-justified` → **skipped** — nothing was escalated. None of `spec/question.md` §4's four conditions applies: the record is not silent (§4b answers it), nothing is irreversible (a citation repair, and §4b says explicitly that an unchanged assertion is not a supersession), no ADR is contradicted, and there is no intent question for the stakeholder.
  - `propagated-claims-carry-their-obligation` → **pass**. Two claims were written into `docs/`, both **cited facts** rather than quantified claims — each is an absolute about one named statement in one named file, not a claim over a family — so what each owes is a citation that resolves, and each is recorded that way under its file's entry in `## Consequences`. `sed -n 217p envel/cli.py` is the check, and it both resolves and supports.
  - `engagement-state-is-left-to-the-ending` → **pass**. No `## Engagement state` section was written, edited, or had a sentence moved into or out of it, and this answer falsified none: `git diff --quiet main --` reports `docs/architecture/overview.md` and `docs/product/vision.md` both unchanged, and those two documents hold every such section in the workspace.
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0; this execution consumed no human answer, recorded above with the reason).
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, `0 errors, 0 warnings`, 7 items and 13 documents).
  - `item-resumed-correctly` → **skipped** — there is no suspension to resume from. `Q-009` is `blocking: false` and was filed by `review-close` at the close; `WI-0005` was never moved to `awaiting-answer` for it and carries no `resume-to` for it. The item stays `done`, which is where the close left it, and this execution makes no transition.
  - `a-deferral-is-not-an-answer` → **pass** (vacuously — nothing was deferred). `Q-009` is `answered` with a decision and four files changed behind it, not a "later".
- **Artifacts:**
  - `tracker/items/WI-0005/questions/Q-009.md` — answered; `status: answered`, `answered-at: 2026-09-11T10:40:54Z`, `answered-by: answer-questions`; `## Answer` and `## Consequences` written.
  - `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` — v1 → **v2**, citation repaired, change-log row, `## Corrections` section created with one `provenance` entry.
  - `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` — v1 → **v2**, citation repaired, change-log row, `## Corrections` section created with one `provenance` entry.
  - `tracker/items/WI-0005/artifacts/plan.md` — two citations repaired; no decision changed.
  - `tracker/board.md` — regenerated.
  - No ADR created, no item filed, no bug filed, no criterion amended.
- **Status:** `done` → `done` (unchanged — `Q-009` is non-blocking, the item was never suspended for it, and this skill makes no transition of its own)
- **Result:** `WI-0005/Q-009` is answered from `spec/doc-header.md` §4b — option A, repair in place with a `provenance` correction — and propagated into four files. A fourth occurrence of the same defect, in `ADR-0010` and predating this item, was repaired under the same policy; three dated statements carrying the same stale numbers were deliberately left. With no open question anywhere, `EP-001` can now reach rest.
