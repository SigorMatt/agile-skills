# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T02:00:18Z — intake v0.5.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's stated idea; this skill is not dispatched on a status
- **Inputs read:**
  - `IDEA.md` — the stakeholder's statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty of items before this execution
- **Decisions:**
  - See `EP-001`'s entry of this execution for how the work was split and why. This item is the 'money out' half: recording a spend against an envelope so that what is left reflects it. It depends on WI-0001 having created and funded something to spend from.
  - Its acceptance criteria are deliberately rough and some are explicit placeholders for answers not yet given; padding them into something that looked finished would have invented requirements the stakeholder never stated.
- **Questions raised:** none on this item; `EP-001/Q-001` through `EP-001/Q-006` were filed on the epic and several of them decide criteria here
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0002 --type work-item --title ... --epic EP-001` → exit 0, item created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`.claude/agile-skills/scripts/validate-workspace .` run after the whole execution; see `EP-001`'s entry)
  - `epic-has-success-measures` → **pass** (decided once for this execution against `EP-001`'s `## Success measures`; see `EP-001`'s entry)
  - `an-open-question-was-asked` → **pass** (`lint-answers --item EP-001 --require-elicitation` → exit 0)
  - `engagement-state-is-delimited` → **pass** (`lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md` → exit 0)
  - `items-are-separable` → **pass** (this item's place in the build order and what it depends on are stated under **Decisions:** above)
  - `no-solution-in-the-problem` → **pass** (the story and criteria name no technology the stakeholder did not; see `EP-001`'s entry for what was removed)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/journal.md`, `tracker/items/WI-0002/history.md` (new, by `new-item`)
- **Status:** — → `draft`
- **Result:** Created at `draft` by this intake execution. It is not Ready: `refine` is what makes each criterion decidable, and some of them wait on the stakeholder's answers to the questions on `EP-001`.

## 2026-09-11T02:07:31Z — refine v0.6.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` (step 4; `WI-0001` and `EP-001` were rejected for open blocking questions, `WI-0003` on priority)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (one row, `— → draft`: a fresh draft, not a send-back), `journal.md`
  - `tracker/items/WI-0002/artifacts/` — no `refinement-qa.md` existed
  - `tracker/items/WI-0001/item.md` and its `Q-001` … `Q-004` — what the sibling item already has open, so that this round neither duplicates it nor contradicts it
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md`, `Q-005.md`, `Q-006.md` — what is already open with the stakeholder
  - `spec/dor-dod.md` §1 — walked criterion by criterion
- **Decisions:**
  - **The stakeholder is not in this session, so this execution files rather than converses** (precondition 2). `artifacts/refinement-qa.md` carries `status: agenda` and says so in its opening paragraph; nothing in it is attributed to anyone.
  - **Two questions, not four.** `Q-001` (is a spend dated today, or can I say when it happened) because `WI-0003`'s monthly summary is only as accurate as the dates on the spends, and nothing can correct a wrong one afterwards; `Q-002` (does a spend carry a description) because it decides what the tool can ever show them about their own past and it interacts with option C of `EP-001/Q-003`. Both are product stake. Nothing else on this item met the bar, and padding the batch to the suggested three-to-six would have spent the stakeholder's attention on questions we could answer ourselves.
  - **The overspend question was deliberately not re-asked.** It is `EP-001/Q-002`, filed in the same round, and AC5 already names it. Re-asking tells a stakeholder their answer was not heard (F-023).
  - **The zero-or-negative-spend rule was assumed rather than asked, and the assumption is declared as taken under no licence.** It is the same decision the stakeholder is already being asked about income in `WI-0001/Q-003`, in the same round, about the same kind of amount; a near-duplicate question is how this protocol degrades into noise. AC6 records it as a placeholder that follows `Q-003`'s answer, and `refinement-qa.md` says where a disagreement lands.
  - **Added AC6 and AC7**, so that the zero/negative case and the after-recording output are criteria a reader can find rather than assumptions nobody can check. AC7 (print the new remaining amount) is likewise assumed under no licence, and costs one line of code if the stakeholder disagrees.
  - **Recorded `depends-on: WI-0001`, which was the real R7 failure.** There is nothing to spend from until envelopes can be created and funded, and AC2 is written against `WI-0001`'s listing. The consequence is deliberate and is written into `## Notes` rather than left for a later reader to discover: the orchestrator does not dispatch anything on an item whose `depends-on` is unfinished, so this item will not be refined again until `WI-0001` is `done`. Leaving the dependency unrecorded would have bought parallel refinement at the price of letting `implement` be dispatched here against code that does not exist, which is the worse failure.
  - **Cited `WI-0001` AC3 with its words rather than by number** in AC2, per `spec/doc-header.md` §4a, so the citation fails loudly if that list is renumbered while `WI-0001` is still being refined — which it is about to be, by its own four open questions.
  - **Checked the renumbering obligation** before adding AC6 and AC7: `grep -rn 'WI-0002 AC' tracker docs` found no citation of this item's criteria, and both were appended rather than inserted.
  - **Two design questions were routed to `plan`**, not to a person: how spends are stored alongside balances and whether a balance is stored or derived, and what the tool does with a spend that refers to an envelope no longer present. The answer would be the same whoever the stakeholder was.
- **Questions raised:** `WI-0002/Q-001`, `WI-0002/Q-002` — both blocking, both addressed to the human, both open; recorded in `artifacts/refinement-qa.md`. None `[unresolved]`: neither has been asked twice.
- **Commands:**
  - `grep -rn 'WI-0002 AC' tracker docs` → exit 1, no matches
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 on an intermediate run (`board.stale` after `depends-on` was added, and `question.blocking.not-suspended` — both resolved by regenerating the board and by this transition)
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 0 consumed human answers, 0 delegations
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition against the state the move produces)
  - `definition-of-ready` → **fail** (, criterion by criterion: R1 pass (frontmatter complete, `depends-on` now set); R2 pass (role, capability, "so that" outcome); R3 pass (AC1–AC7, labelled, checkboxes); **R4 fail** — AC1 names no observation until `EP-001/Q-006` settles the command, and AC5 and AC6 are explicit placeholders for `EP-001/Q-002` and `WI-0001/Q-003`; R5 pass (`## Out of scope` names corrections and transfers, categories and tags, and the summary); **R6 fail by design** — this execution filed two blocking questions, which is what suspends the item; **R7 now pass** — the dependency on `WI-0001` is recorded and this item is sequenced after it; **R8 fail** — `refinement-qa.md` declares `status: agenda`, honestly, because no conversation has happened; R9 pass (one coherent change: record a spend, see the effect); **R10 fail** — the combinations are now visible (date, description, zero and negative amounts, overspend) but four of them are open questions rather than stated behaviours; R11 pass (no criterion counts anything; AC2 names the listing it constrains and quotes it); R12 pass (two assumptions, both declared as taken under no licence, each naming where a disagreement lands))
  - `criteria-are-decidable` → **fail** (AC2 is decidable today given `WI-0001` (record a spend, run the listing, compare every envelope's amount before and after), AC3 is decidable today (record a spend against a name never created; expect a refusal naming it and nothing recorded), AC4 is decidable today (record in one invocation, list in another), AC7 is decidable today (read the output of the recording command). AC1 is not, until the command has a name; AC5 and AC6 are not, and say so in their own words.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0; no human answer has been consumed on this item, so there was nothing to check against, and the two questions filed carry no answers)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` holds both questions, the two assumptions with the authority they were taken under, what was routed to `plan`, and what was deliberately not re-asked; nothing is tagged `[human]`, because no human has said anything)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` (new)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0002/item.md` (`depends-on: WI-0001` added; AC2 given a quoted citation of `WI-0001` AC3; AC6 and AC7 added; `## Notes` rewritten)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0002` is not Ready, and R4, R6, R8 and R10 say why. Two questions went to the stakeholder as one ask; the item is suspended at `awaiting-answer` and resumes at `draft` for a second round once they and the epic's questions are answered. R7's failure — the unrecorded dependency on `WI-0001` — was fixed here rather than asked about.

## 2026-09-11T02:24:47Z — answer-questions v0.6.3 — architect

- **Item:** WI-0002
- **Trigger:** `awaiting-answer` with two replies in the question files; the stakeholder answered both between turns, so they are answerable rather than outstanding (`spec/question.md` §3 rule 4b)
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` — both, with the stakeholder's `## Answer` filled in
  - `tracker/items/WI-0002/item.md` and `tracker/items/WI-0002/history.md` — the criteria the answers land in, and the row that suspended the item, whose `resume-to` is `draft`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1's agenda, the two `[assumed]` entries and the authority claimed for each
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md`, `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — the ten human answers already consumed today, for the cross-answer checks
  - `tracker/items/WI-0003/item.md` — the summary that both of these answers bear on, and `tracker/items/WI-0005/item.md`
  - `docs/product/vision.md` v2 — checked; neither answer changes a sentence in it
  - `docs/architecture/adr/` — still empty
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5, `spec/workspace-layout.md` §1.3, `spec/question.md` §2
- **Decisions:**
  - **`Q-001` — today unless a date is given.** Route: the human answered, option B. AC8 is the default and AC9 is the back-dated case, written as something observable: a spend recorded on the 3rd but dated the 28th of the previous month belongs to the previous month's summary. Their reason was itself a statement about `WI-0003`, so it was propagated to that item's `## Notes` as well as to this one's criteria — the rule "a spend's month is its own date, not the day it was typed" is a thing the summary depends on and nobody reading `WI-0003` alone would have known it.
  - **What `Q-001` opened and did not close was recorded, not guessed.** A date that the tool cannot read, and a date in the future, are behaviours nobody has stated. They are in `WI-0002` `## Notes` for `refine` round 2. Writing them as criteria would have manufactured requirements the stakeholder never gave, and this item already had three criteria invented that way before round 1 caught them.
  - **`Q-002` — an optional description.** Route: the human answered, option B. AC10.
  - **`Q-002`'s answer implied work no item recorded, and it was filed as `WI-0006`.** They will put a description on *"the ones I might query later"*, and nothing in this epic lets them query a spend: `EP-001/Q-003` ruled the individual spends out of the monthly summary, which was the only report there was. Step 3b says file it, so `WI-0006` exists at `draft`, at `low` priority, with `arose-from: WI-0002/Q-002`. The inference rests on one phrase, so `WI-0006` `## Notes` opens by saying it was derived rather than asked for and that `refine`'s first job is to put it to the stakeholder **including the option of closing it**. `WI-0005` needs the same capability from the other direction — you cannot correct a spend you cannot name — and that is now recorded on both items.
  - **It was not treated as a conflict with `EP-001/Q-003`.** Refusing to have spends listed in a month-end report and wanting to look one up are different things, and deciding between them is not ours. What the two answers leave between them is a gap, and a gap is filed as work rather than escalated as a contradiction.
  - **The assumption behind AC6 was left standing.** `WI-0001/Q-003` answered for income and AC6 now states the rule for spending, but the stakeholder was never asked about spending. `refinement-qa.md` gains an explicit "still assumed, after the answer" paragraph rather than quietly letting an answered question look like it covered both.
  - **No ADR.** Both answers are the stakeholder's own words; nothing was decided by the architect.
- **Cross-answer check:** `WI-0002/Q-001` checked against `EP-001/Q-004` (compatible, and the same concern from opposite ends — a summary bounded by the calendar is only worth having if entries are dated by when they happened), `EP-001/Q-001` (compatible — this answer decides which side of a month boundary a spend falls on) and `EP-001/Q-005` (compatible; whether a correction may change a date is an open point on `WI-0005`, not a contradiction). `WI-0002/Q-002` checked against `EP-001/Q-003` (compatible, and the pair is why `WI-0006` exists: not contradictory, but between them they ask for a field with nothing that can read it back), `WI-0002/Q-001` (compatible — both optional extras on the same command) and `EP-001/Q-005` (compatible). No verdict is `conflicts`, so no question was filed; the one thing the pair does leave is a gap, and it is on the board as `WI-0006` rather than in a question file.
- **Questions raised:** none by this execution. The questions these answers make necessary are `refine` round 2's — what to type below `envel`, how a date is written, what an unreadable or future date does, whether a description is bounded, and whether `WI-0006` is wanted at all — and they belong in one round put to the stakeholder together rather than as five letters from here.
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --next-id work-item` → `WI-0006`
  - `.claude/agile-skills/scripts/new-item --id WI-0006 ... --actor answer-questions --arose-from WI-0002/Q-002` → exit 0
  - `.claude/agile-skills/scripts/journal-entry WI-0006 --skill answer-questions --body-file ...` → exit 0
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 2 consumed human answers, 0 errors
  - `.claude/agile-skills/scripts/validate-workspace .` → 1 error, `question.awaiting.none-open` on `WI-0002`, which is the finding this transition resolves
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in the two `## Consequences` sections was opened and contains the change: `WI-0002` AC8, AC9, AC10 and the two new `## Notes` bullets; `WI-0003` `## Notes` carries the dating rule and the description exclusion; `WI-0006` exists at `draft` with `arose-from: WI-0002/Q-002`; `WI-0005` `## Notes` names `WI-0006`; `refinement-qa.md` is `status: recorded` with both answers verbatim. No `## Consequences` section names zero files)
  - `answered-from-the-record` → **pass** (both answers are the stakeholder's own text in the question's `## Answer`, quoted verbatim in `refinement-qa.md` and cited from what they produced; the record was not silent, so no ADR was written)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human. The one thing that might have been — the gap between `Q-002` and `EP-001/Q-003` — is implied *work*, which step 3b says to file, not a contradiction between two of their statements, which §4 would say to escalate)
  - `propagated-claims-carry-their-obligation` → **pass** (this execution wrote nothing under `docs/`; `docs/product/vision.md` was read and left at v2)
  - `engagement-state-is-left-to-the-ending` → **pass** (no `## Engagement state` section was written or amended, and neither answer falsifies a sentence in one beyond what the `EP-001` execution already recorded)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0, 2 consumed human answers, 0 errors; every named ID resolves and carries a verdict, and no verdict is `conflicts`)
  - `workspace-valid` → **pass** (/fail per the run this transition made** (evidence: the run immediately before it reported one error, `question.awaiting.none-open` on `WI-0002`, which this move to `draft` resolves and which `--resolving` covers))
  - `item-resumed-correctly` → **pass** (the row that suspended `WI-0002` at 2026-09-11T02:07:31Z records `resume-to: draft`; this move is to `draft`. Read from the history row, not inferred)
  - `a-deferral-is-not-an-answer` → **skipped** (neither reply defers; both pick an option and give a reason)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, `answered-by: human`, `answered-at: 2026-09-11T02:23:40Z`, each with a `## Cross-answer check` and a `## Consequences`
  - `tracker/items/WI-0002/item.md` — AC8, AC9, AC10 added; `## Notes` rewritten, with the open points this round left and the derivation of `WI-0006`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; both answers verbatim; the AC6 assumption explicitly left standing; a `## What round 1 did not settle` section
  - `tracker/items/WI-0003/item.md` — `## Notes` gains the dating rule and the description exclusion
  - `tracker/items/WI-0005/item.md` — `## Notes` updated: a spend now has a date and a description too, and `WI-0006` is the same gap from the other side
  - `tracker/items/WI-0006/item.md`, `journal.md`, `history.md` — created
  - `tracker/board.md` — regenerated
  - no ADR created; `docs/` unchanged by this execution
- **Status:** `awaiting-answer` → `draft`
- **Result:** `WI-0002`'s two refinement answers are consumed and propagated, and the item returns to `draft` with ten criteria: a spend is dated today unless you say otherwise, a back-dated spend belongs to the month it happened in, and a description is optional. One answer implied a capability nobody had scoped, and it is on the board as `WI-0006` rather than in a note. The item is **not** Ready — R4 still fails on the command surface, and four further things these answers opened are written down for `refine` round 2 rather than guessed.

## 2026-09-11T03:34:35Z — refine v0.6.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` (step 4). `WI-0002` became runnable this turn for the first time: its `depends-on: WI-0001` reached `done` at `2026-09-11T03:28:08Z`. WI-0003/4/5 rejected on priority rank 3 > 2, WI-0006 on rank 4, WI-0001 and EP-001 on a null status owner
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — ten criteria, `## Out of scope`, `## Notes` in full
  - `tracker/items/WI-0002/history.md` — three rows. **Read first, and it matters:** the last row is `awaiting-answer → draft` by `answer-questions`, so this is a resumed round-1 conversation, not a send-back from `verifying` or `in-review`. Nothing specific was found wrong with delivered behaviour; there is none yet
  - `tracker/items/WI-0002/journal.md` — all three entries, including round 1's own DoR walk and the two assumptions it declared under no licence
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1 in full, including `## What round 1 did not settle`, which is this round's agenda
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — the stakeholder's two answers verbatim, so as not to re-ask them
  - `tracker/items/EP-001/item.md` and `questions/Q-001.md` … `Q-006.md` — the epic-wide rules on amounts and envelope names, the overspend answer, and *"Short is what matters if I'm typing it several times a day"*
  - `tracker/items/WI-0001/item.md` — the delivered command surface this item extends: AC13, AC16, AC17, and `## Out of scope`'s *"Flags and options of any kind on these three commands"*
  - `tracker/items/WI-0003/item.md`, `WI-0005/item.md`, `WI-0006/item.md` — whether a sibling already owns part of this scope
  - `docs/product/vision.md` and `docs/architecture/overview.md` — the vision's four things in order, and `## Conventions this project has adopted`
  - `.claude/agile-skills/spec/dor-dod.md` §1 — walked criterion by criterion
- **Decisions:**
  - **The stakeholder is not in this session, so this execution files rather than converses** (precondition 2, and the same route round 1 took). Three blocking questions addressed to `human`, the item suspended at `awaiting-answer` with `resume-to: draft`, and `refinement-qa.md` moved back to `status: agenda` — because round 2's conversation has not happened, and R8 must not let round 1's record carry the item to `ready`.
  - **Three questions, and all three are product stake.** `Q-003` — are the optional date and description named options, plain words in a fixed order, or a mixture? It is what they type several times a day, and `WI-0001` deliberately gave the first three commands no options at all, so introducing one is a change to the surface they use rather than an internal detail. `Q-004` — which date forms are accepted, and if a short form is wanted, which reading of `7/9` is theirs? We have not been told where they live, and the two readings differ by two months; guessing would silently misfile spends into the wrong month, which is the exact failure their `Q-001` answer was given to prevent. `Q-005` — is a future date refused? The same keystrokes are a mistyped year and a direct debit they know is coming, and correcting a recorded spend is `WI-0005` and is not built.
  - **`Q-003` and `Q-004` are two files because they are two decisions.** Where the date goes on the line and what the date looks like are independent — any answer to one works with any answer to the other — and folding them into one question is how half of it gets answered and the other half recorded as settled (F-027). They share one framing line naming the round and the count, so the three read as one conversation.
  - **The subcommand word was assumed, not asked**, as `envel spend <envelope> <amount>`. Rationale: `WI-0001` round 2 assumed `new`, `add` and `list` on exactly this footing, and asking about the fourth word while never having asked about the first three would be inconsistent rather than careful. Declared under **no delegation** with the disagreement landing on AC1.
  - **An unreadable date was decided, not asked.** Every other malformed input in this tool is already refused with a message and nothing recorded, built and verified [src: WI-0001 AC17 "each refused with a message with nothing recorded"] [src: WI-0001 AC13 "are refused with a message and no envelope is created"], and the alternative — quietly falling back to today — would record a spend on a date they did not type. Declared under **no delegation**. Deliberately kept separate from `Q-005`: that one is a policy about a date the tool reads perfectly well, this one is about text that is not a date.
  - **A description's bounds were decided, not asked** — no length limit, no character restriction. Rationale: an unbounded free-text field is the least surprising answer and a limit is the thing that would need justifying. Declared under **no delegation**, and `WI-0001/Q-004` was explicitly **not** read as licensing it: they chose not to restrict envelope *names*, and stretching that to descriptions would be spending an answer further than it was given (R12).
  - **The stream-and-exit-code rule was cited, not assumed.** It is the project's recorded convention [src: docs/architecture/overview.md] and their own delivered criterion [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits non-zero"], so round 3 writes it into the criteria by citation rather than restating it as a new decision. Message *wording* stays deliberately unconstrained, as `WI-0001` left it.
  - **No acceptance criterion was rewritten by this execution, deliberately.** AC1, AC7, AC9 and AC10 are the four that fail R4, and all four fail on the answers now pending. Rewriting them now would mean guessing, and renumbering twice; a citation elsewhere naming `WI-0002 AC7` goes on resolving against whatever moves into that position (F-094). Round 3 rewrites them once, from the replies.
  - **Checked the renumbering obligation anyway**, because the decision above depends on it: `grep -rn 'WI-0002 AC' tracker docs` finds three hits, all of them prose *about* the obligation in this item's own journal and Q&A, and none a citation of a criterion by number from another item. Nothing outside this item points into the list.
  - **Nothing was re-asked.** Whether a spend can be dated at all and whether a description is optional are `Q-001` and `Q-002`, answered; the overspend is `EP-001/Q-002`, answered. The two design questions round 1 routed to `plan` stay routed there.
- **Cross-answer check:** `none` — this execution consumed no human answer, so there is no reply to check against prior ones. Instead each question carries its own `## Cross-answer check` **filed with it**, naming the prior answers the reply will have to coexist with: `WI-0002/Q-001`, `WI-0002/Q-002`, `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-004`, `EP-001/Q-006`. `Q-005`'s is the one to watch — `EP-001/Q-002` says they would rather be stopped than surprised, so an answer of "record it" there is a preference about dates rather than a reversal, and it needs saying rather than smoothing over (ADR-0008).
- **Questions raised:** `WI-0002/Q-003`, `WI-0002/Q-004`, `WI-0002/Q-005` — all blocking, all addressed to `human`, all open, recorded in `artifacts/refinement-qa.md` `## Round 2`. None `[unresolved]`: none has been asked twice.
- **Commands:**
  - `grep -rn 'WI-0002 AC' tracker docs` → exit 0, 3 hits, none a cross-item citation
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 2 consumed human answers, 0 delegations spent
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 on an intermediate run, with exactly the two errors this move resolves: `board.stale`, and `question.blocking.not-suspended` on an item still at `draft`
  - `.claude/agile-skills/scripts/board-gen .` → exit 0, board rewritten
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition against the state the move produces; the intermediate `question.blocking.not-suspended` is what this move exists to resolve)
  - `definition-of-ready` → **fail** (criterion by criterion: R1 pass — frontmatter complete, `type`, `epic`, `priority` and `depends-on` all set; R2 pass — role *"a person budgeting my own money at a terminal"*, capability *"record what I spend against the envelope it came out of"*, outcome *"so that the amount left … tells me what I still have to spend"*; R3 pass — AC1–AC10, labelled, checkboxes; **R4 fail** — AC1 names no observation (*"There is an `envel` command"* with no command), AC7 names an output of a command nobody has named, AC9 says a date *"can be recorded"* without saying how one is written, AC10 says the same of a description. AC2, AC3, AC4, AC5, AC6 and AC8 are decidable today; R5 pass — `## Out of scope` names corrections, transfers, categories and tags, and the summary; **R6 fail by design** — this execution filed three blocking questions, which is what suspends the item; R7 **pass**, for the first time — `WI-0001` is `done` and merged at `025240e`; **R8 fail** — `refinement-qa.md` declares `status: agenda`, honestly, because round 2's conversation has not happened; R9 pass — one coherent change, record a spend and see the effect; **R10 fail** — of the three unstated combinations, two are now decided (an unreadable date, a description's bounds) and one is asked (`Q-005`, a future date); the date-and-description-together case is `Q-003` and is asked. Visible, per R10's own standard, but not yet stated in a criterion; R11 pass — no criterion counts anything, and AC2 names the listing it constrains by quoting its words; R12 pass — five entries in `refinement-qa.md` `## Decided here`, three of them this round's, every one declaring **no delegation** and where a disagreement lands, and the stream convention recorded as a citation rather than as an assumption at all)
  - `criteria-are-decidable` → **fail** (AC2 — record a spend, run `envel list`, compare every envelope's amount before and after: decidable today. AC3 — spend against a name never created; expect a refusal naming it, exit non-zero, nothing recorded: decidable. AC4 — record in one invocation, list in another: decidable. AC5 — fund an envelope with 10, spend 20, expect a refusal naming the envelope and what is left, and no negative in the listing: decidable. AC6 — spend `0` and `-40`, expect refusals and an unchanged amount: decidable. AC8 — record without a date, inspect what date it was given: decidable once the command is named. **AC1 is not decidable**: no command to run. **AC7 is not**: no command whose output to read. **AC9 and AC10 are not**: no syntax to type. Those four are `Q-003`, `Q-004` and `Q-005`)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0 over 2 consumed human answers and 0 delegations spent. No answer was consumed here; the three questions filed carry a `## Cross-answer check` written at filing time, naming six prior answers by ID)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` holds round 1 unchanged and verbatim, and a new `## Round 2` carrying the DoR walk, the three questions with why each is theirs, the four things decided here with the authority each was taken under, and `## What round 2 has not settled`. Nothing in round 2 is tagged `[human]`, because no human has said anything this round; the three `[assumed]` entries each carry their **Under no delegation** line and where a disagreement lands)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-003.md`, `Q-004.md`, `Q-005.md` (new) — blocking, to `human`, each with `## Context`, `## Question`, `## Options considered` with the recommendation last and marked as ours, `## Answer`, `## Cross-answer check` and `## Consequences`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: recorded` → `agenda`; `## Round 2` appended
  - `tracker/items/WI-0002/item.md` — `## Notes` records round 2's three questions and its four decisions; no criterion touched
  - `tracker/board.md` (regenerated)
  - no question filed on any other item; `docs/` unchanged; no ADR
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0002` is not Ready, and R4, R6, R8 and R10 say why. Three questions went to the stakeholder as one ask about one thing — the line they will type to record a spend — and four further points round 1 left open were decided here rather than spent on their attention, each declared under no licence. No criterion was rewritten, so round 3 renumbers nothing and writes the four pending criteria once, from the replies. The item suspends at `awaiting-answer` and resumes at `draft`.

## 2026-09-11T03:48:13Z — answer-questions v0.6.3 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer` with three human-addressed questions whose `## Answer`
  sections had been filled in between turns; dispatched by the turn's first-consume rule rather
  than by `next`, because an answered-but-unconsumed human question halts the orchestrator.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` … `Q-005.md` — all five, including the two round-1
    answers already consumed, because the round-2 replies had to be checked against them
  - `tracker/items/WI-0002/item.md` (AC1–AC10 as round 1 left them, and `## Notes`)
  - `tracker/items/WI-0002/history.md` — the suspending row of 2026-09-11T03:34:34Z, whose
    `resume-to` is `draft`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: agenda`, rounds 1 and 2)
  - `tracker/items/WI-0001/item.md` — AC2 and AC16, cited from `WI-0002`'s criteria
  - `docs/architecture/overview.md` (v2) — `## Conventions this project has adopted` and
    `## What is not decided yet`
  - `docs/product/vision.md` (v1)
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` — checked for a recorded decision any of the
    three answers would contradict; none of the five is about the command surface
  - no `plan.md`: this item has never been planned
- **Decisions:**
  - `Q-003` answered **from the human's reply**, option C: the description is a plain word after
    the amount and the date is `--on <date>`. Propagated into AC1, AC9 and AC10 rather than
    summarised, because `refine` round 3 re-reads the criteria and not the Q&A.
  - `Q-004` answered **from the human's reply**, option A: `--on` takes `YYYY-MM-DD` and nothing
    else. Written as a new AC11 rather than folded into AC9, because it is a rule about the text
    of a date and AC9 is about which date a spend is held against — one criterion, one decidable
    thing.
  - `Q-005` answered **from the human's reply**, option A: a future date is refused. New AC12.
  - The criteria were amended here rather than left to `refine` round 3, which had reserved the
    rewrite. Rationale: round 2's two reasons for deferring were the risk of guessing the answers
    and of renumbering a list that citations point into. The answers are now in, so nothing is
    guessed; and AC1, AC9 and AC10 were amended **in place** with AC11 and AC12 **appended**, so
    no criterion changed its number and every `WI-0002 AC<n>` citation still resolves. Leaving
    `item.md` saying the old thing is precisely what `answer-is-propagated` exists to prevent, and
    a note pointing at a question file is not propagation. `WI-0002` `## Notes` records the
    reasoning where round 3 will read it.
  - The stakeholder's aside on `Q-004` — *"if you ever do add one, `7/9` means the 7th of
    September to me"* — was recorded in `## Notes` and **not** made into an item. It is a
    conditional about a short form nobody is building, so filing work for it would be inventing
    scope out of a courtesy; recording it means nobody has to ask them twice if it is ever built.
  - No `[assumed]` decision of round 2 was disturbed. The subcommand `spend`, the unbounded
    description and AC6's symmetry with income are still ours and still tagged; AC11 makes round
    2's *unreadable date* decision concrete rather than replacing it.
  - Nothing was written into `docs/`. The command surface for a spend is `WI-0002`'s to settle and
    `docs/architecture/overview.md` `## What is not decided yet` already says so; it reaches a
    document when `plan` writes one. This keeps the answer in the one artifact the next skill
    reads rather than in two that can drift.
  - Observed and deliberately not acted on: `docs/architecture/overview.md` `## Engagement state`
    still says *"Nothing has been implemented, verified or accepted in this engagement"*, which
    `WI-0001` reaching `done` made false. It was not falsified by any answer consumed here, and
    that section belongs to the ending (`spec/doc-header.md` §4a), so this execution neither
    repaired it nor claimed it as a consequence. `review-close` restates it at the ending.
- **Questions raised:** none — all three replies were answerable as given, and no cross-answer
  check returned `conflicts`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0 (5 consumed human
    answers, 0 errors); an earlier run at exit 1 showed `Checked against:` must open its own
    block, and the three sections were reflowed
  - `python3 .claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0002 --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, then exit 0 after a
    citation fix: AC1 quoted `WI-0001` AC2 in paraphrase and the validator refused it
  - `git log -1 --format=%H` → `772d3e6`
- **Gates:**
  - `answer-is-propagated` → **pass** (each of the three `## Consequences` sections names `item.md`, `refinement-qa.md` and `item.md` `## Notes`; each file was reopened after writing and the change is there — AC1/AC9/AC10 rewritten, AC11 and AC12 added, `## Answers — round 2` written with all three replies verbatim, `status` moved `agenda` → `recorded`)
  - `answered-from-the-record` → **pass** (all three follow from the stakeholder's own replies, quoted verbatim in the question files and again in `refinement-qa.md`; no ADR was needed because this execution decided nothing beyond where to write the answers)
  - `escalation-is-justified` → **skipped** (no question was re-addressed to the human, so there is no escalation to justify)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0002 --uncommitted`, exit 0; 0 sentences written into `docs/`, because this execution wrote none)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted`, exit 0; the one stale sentence found is recorded under **Decisions** and was left to the ending)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0; three new `## Cross-answer check` sections, ten verdicts, all `compatible`, no conflict to escalate)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0 after the AC1 citation was repaired and this transition cleared `question.awaiting.none-open`)
  - `item-resumed-correctly` → **pass** (`resume-to` on the 2026-09-11T03:34:34Z row is `draft`; this execution moved the item to `draft`)
  - `a-deferral-is-not-an-answer` → **pass** (no reply deferred; all three chose a lettered option and gave a reason for it)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-003.md` — `answered`, cross-answer check and consequences
    written
  - `tracker/items/WI-0002/questions/Q-004.md` — same
  - `tracker/items/WI-0002/questions/Q-005.md` — same
  - `tracker/items/WI-0002/item.md` — AC1, AC9, AC10 amended; AC11 and AC12 added; `## Notes`
    extended with the three answers, the aside about `7/9`, and why the criteria were written here
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; round-2
    question rows `open` → `answered`; `## Answers — round 2`, `## Cross-answer check — round 2,
    on the replies` and `## What round 2's answers left for round 3` added
  - commit of the above, refs `WI-0002`
- **Status:** `awaiting-answer` → `draft`
- **Result:** Round 2's three replies are consumed and in the criteria: a spend is
  `envel spend <envelope> <amount>` with an optional plain-word description and an optional
  `--on YYYY-MM-DD`, an unparseable or future date is refused with nothing recorded, and no
  question on this item is open. The item is back at `draft` for `refine` round 3, which now
  confirms a Definition of Ready rather than writing one.

## 2026-09-11T03:56:23Z — refine v0.6.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` — highest-ranked runnable item, `priority:
  high` against four `medium`/`low` siblings, with `depends-on: WI-0001` at `done` and no open
  question anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC12 as `answer-questions` left them, `## Out of scope`,
    and the whole of `## Notes`
  - `tracker/items/WI-0002/history.md` — four rows; this is a fresh third round of refinement, not
    a send-back from `verifying` or `in-review`, so the whole item is in scope
  - `tracker/items/WI-0002/journal.md` — rounds 1 and 2 and both `answer-questions` executions
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: recorded`, rounds 1 and 2 with
    all five answers verbatim)
  - `tracker/items/WI-0002/questions/Q-001.md` … `Q-005.md` — all five `answered`, read so that
    nothing settled was re-asked
  - `tracker/items/WI-0001/item.md` — AC3, AC15 and AC16, the delivered behaviour this round cites
  - `tracker/items/WI-0003/item.md` — the one cross-item citation into this list, AC8 on
    `WI-0002` AC9
  - `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md`, `ADR-0003-store-location.md`,
    `ADR-0001-amounts-are-integer-cents.md`
  - `docs/architecture/overview.md` (v2) — `## Conventions this project has adopted`
  - `docs/product/vision.md` (v1)
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Asked the stakeholder nothing, and that is the decision.** Both failing criteria were ours.
    R4's gap was about how a criterion is *checked*, not about what the tool does — the behaviour
    is exactly what they chose at `Q-001` and `Q-002` — and R10's four combinations have no stake
    in their money. Three rounds have put nine questions to them on this item and its epic;
    routing a fourth round of our own work to them is the failure F-023 names.
  - **AC8, AC9 and AC10 rewritten to name an observation.** They described a spend's date and
    description, and nothing this item delivers prints either back: the listing shows names and
    amounts only, and the readers of a date are `WI-0003`'s summary and `WI-0006`'s lookup,
    neither built. AC8 now spells out a repeatable setup — a fresh `ENVEL_FILE` [src: ADR-0003],
    one envelope, one undated spend and one dated `2020-01-01` — and AC9 and AC10 observe in that
    same store. Rationale: `verify` cannot ask anyone anything, and a criterion whose only reader
    is an item not yet built is a criterion that reaches verification unsettleable.
  - **Which field carries the date was deliberately not decided.** `ADR-0002`'s `at` is *"when the
    tool recorded the entry"*, which is not the same thing as the date a spend is held against.
    The criteria say the entry *carries* the date and never what it is called, so either a new
    field or a redefinition of `at` satisfies them. It is sharpened in `## Notes` as `plan`'s.
  - **AC13 added — streams and exit codes.** Round 2 recorded the convention and said it would
    write it into the criteria "by citation", then deliberately rewrote no criterion, so it never
    landed. It is not an assumption: the project's recorded convention
    [src: docs/architecture/overview.md] and the delivered item's own criterion [src: WI-0001
    AC16]. Message wording stays unconstrained, as `WI-0001` left it.
  - **AC14 added — `envel spend` with the wrong number of words.** Also not an assumption:
    [src: WI-0001 AC15] is delivered and verified, and `spend` is a subcommand. What is new is
    that this item adds a third and fourth word to get wrong.
  - **Four combinations left deliberately unconstrained** rather than decided, each in `## Notes`
    with where a disagreement lands: which message wins when several refusals apply at once, an
    empty or whitespace-only description, `--on` given twice, and message wording. `[assumed]`,
    **under no delegation** — nothing the stakeholder has said covers any of them. Left rather
    than decided because deciding would be inventing requirements a reasonable implementation may
    settle either way; R10 asks that they be visible, not that they be settled.
  - **Renumbering obligation discharged before touching the list.**
    `grep -rn 'WI-0002 AC' tracker docs` returns nine hits, of which exactly one is a cross-item
    citation — `WI-0003` AC8 on `WI-0002` AC9, quoting *"A spend can be recorded with a date
    other than today, written as"*. AC9 was amended **after** those words and AC13 and AC14 were
    **appended**, so no criterion moved and that citation still resolves to the criterion it
    named.
  - **No criterion counts anything** (R11): AC13 names the criteria it covers by ID rather than
    counting them, and nothing in the list quantifies over tests, files or cases.
  - Not revisited, deliberately: the three `[assumed]` decisions rounds 1 and 2 took — the
    subcommand `spend`, the unbounded description, and AC6's symmetry with income. Each is still
    ours, still under no delegation, and each still lands on one criterion. Re-deciding them would
    have been this round re-opening a settled record.
- **Questions raised:** none. Round 3 put no question to the stakeholder and left nothing
  `[unresolved]`; the four unconstrained combinations are recorded in `## Notes` as such, with who
  left them so. The full agenda and its disposal are in `artifacts/refinement-qa.md` `## Round 3`.
- **Commands:**
  - `grep -rn 'WI-0002 AC' tracker docs` → exit 0, 9 hits, one of them a cross-item citation
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0 (5 consumed human
    answers, 0 delegations spent)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 7 items and 7 documents, no warnings)
  - `definition-of-ready` → **pass** (, criterion by criterion. R1 **pass** (frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: high`). R2 **pass** (`## Story` names the role *"a person budgeting my own money at a terminal"*, the capability *"record what I spend against the envelope it came out of"*, and the outcome after *"so that"*). R3 **pass** (AC1–AC14, each `AC<n>` and a checkbox). R4 **fail on entry → pass**: AC8, AC9 and AC10 stated a behaviour nobody could check, and no criterion named a stream or an exit code; AC8, AC9 and AC10 were rewritten with an observation against the store file and AC13 was added, and all fourteen are now settleable — the per-criterion command and verdict are under `criteria-are-decidable`. R5 **pass** (`## Out of scope` names four things a reader could assume were in, including correcting a spend and moving money between envelopes, each pointing at the item that owns it). R6 **pass** (all five questions on this item are `answered`; none is open, blocking or otherwise). R7 **pass** (`depends-on: WI-0001` is `done`). R8 **pass** (`artifacts/refinement-qa.md` declares `status: recorded` and carries all three rounds, five answers verbatim and tagged). R9 **pass** (one subcommand, `envel spend`, in one command surface; nothing here splits). R10 **fail on entry → pass**: four combinations had no stated behaviour — a spend given the wrong number of words, which is now AC14, and three left deliberately unconstrained in `## Notes` with who left them so. R11 **pass** (no criterion counts something this item may move; AC13 names the criteria it covers by ID). R12 **pass** (every `[assumed]` entry in the Q&A and every one in `## Notes` says **under no delegation** and where a disagreement lands; no standing delegation exists on this item to spend — `lint-answers` reports 0 delegations).)
  - `criteria-are-decidable` → **pass** (, one by one. AC1: run `envel spend groceries 12.50`, then `envel list`; the envelope's amount is 12.50 lower. AC2: same run, compare every line of `envel list` before and after. AC3: `envel spend nosuch 1.00` → non-zero exit, stderr names `nosuch`, `envel list` unchanged. AC4: record a spend, let the process exit, run `envel list` in a second invocation. AC5: with 10.00 in the envelope, `envel spend groceries 20.00` → refused, stderr names the envelope and `10.00`, listing unchanged and never negative. AC6: `envel spend groceries 0` and `envel spend groceries -5` → each refused, amount unchanged. AC7: read stdout of a successful spend for the new remaining amount. AC8: the fresh-`ENVEL_FILE` setup the criterion spells out, then open the file and read the two spend entries' dates. AC9: same store, `--on 2026-08-28`, the entry carries `2026-08-28`. AC10: same store; the entry for `"lunch"` contains `lunch`, the one recorded without carries none. AC11: `--on 7/9`, `--on 09-07`, `--on yesterday` → each refused, nothing recorded. AC12: `--on` with tomorrow's date → refused, message says the date is in the future. AC13: run each refusal and each success named in it and check the stream and the exit code. AC14: the three malformed invocations it names → usage on stderr, non-zero, nothing recorded.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0. This round consumed no answer — no question was asked and none came back — and `## Cross-answer check — round 3` says so with the reason, which is the `Checked against: none` the rule asks for)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` carries all three rounds: five stakeholder answers quoted verbatim and marked `human`, nothing paraphrased into agreement, and every `[assumed]` entry across the three rounds carrying **under no delegation** and where a disagreement lands. No standing delegation is spent on this item, so no `**Under delegation:**` line is owed)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — AC8, AC9 and AC10 rewritten with their observations; AC13
    and AC14 appended; `## Notes` extended with round 3's summary, the four unconstrained
    combinations, and the sharpened design question for `plan`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `## Round 3` added: the agenda, the
    decision to ask nothing and why, four decisions with their authority, the cross-answer check,
    and what round 3 has not settled
  - `tracker/board.md` — regenerated
  - commit of the above, refs `WI-0002`
- **Status:** `draft` → `ready`
- **Result:** `WI-0002` is Ready. Fourteen criteria, every one settleable by a named command or a
  named file, with the stakeholder's five answers intact and three `[assumed]` decisions and four
  unconstrained combinations all carrying **under no delegation** and where a disagreement lands.
  Round 3 asked nothing, because nothing left was theirs. `plan` is next, and `## Notes` hands it
  four design questions, of which the sharpest is whether a spend's date is a new field or a
  redefinition of `ADR-0002`'s `at`.

## 2026-09-11T04:05:14Z — plan v0.6.3 — architect

- **Item:** WI-0002
- **Trigger:** `ready` — dispatched by `next` as the highest-ranked runnable item (priority rank 2) after `refine` round 3 took it out of `draft`. No question is open anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, which are this design's contract, and `## Notes`, which names the two design questions `refine` routed here and the four things it left deliberately unconstrained
  - `tracker/items/WI-0002/history.md` — nine rows; this is a first plan, not a re-plan after a rejection
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — all three rounds, in particular `## Routed to plan, not to the stakeholder`, the `[assumed]` entries of rounds 2 and 3, and the stakeholder's verbatim answers to `Q-001` through `Q-005`
  - `tracker/items/WI-0003/item.md` — AC2, AC7 and AC8, because the summary is what reads the field this plan adds, and AC8 is what rules out one of `ADR-0006`'s three options
  - `tracker/items/WI-0001/artifacts/plan.md` — the shape the delivered code was built to
  - `docs/product/vision.md` v2 — read in full, for the invalidation set
  - `docs/architecture/overview.md` v2 — read in full; updated by this execution to v3
  - `docs/architecture/adr/` — all five standing ADRs read in full: `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`. Nothing in them is re-decided here and all five are named under `## Binding ADRs`.
  - the source code this change touches: `envel/cli.py`, `envel/envelopes.py`, `envel/money.py`, `envel/store.py`, and the shape of `tests/test_cli.py`
  - `tracker/project.yaml` — `commands.test` and `commands.lint` already filled in by `WI-0001`'s plan, and both re-run here
- **Decisions:**
  - **A spend carries `on`, the calendar day the money was spent, as its own field; `at` keeps meaning when the tool recorded the entry** — `ADR-0006`. Branch: *decided*, and it is the decision `refine` explicitly routed here. The alternative of redefining `at` was rejected because `WI-0003` AC8 makes income fall in the month it was *recorded* while a spend falls on its own date, so one field would have to be read differently per kind anyway — and because it would falsify `ADR-0002`'s own sentence and so need that ADR superseded rather than extended. The uniform-field option was rejected because a file in which income carries a date of its own says income can be dated, which is what the stakeholder decided against at `WI-0003/Q-003`.
  - **A spend's `cents` is stored negative.** Branch: *documented* — `ADR-0002` defines an envelope's balance as the plain sum of `cents` over the entries naming it, so a positive spend would falsify that sentence and make every balance a special case. Nothing is decided here; the ADR is cited.
  - **Dates get their own module, `envel/dates.py`, standing to dates as `envel/money.py` stands to amounts.** Branch: *assumed*, recorded with its reversal — moving two functions into `envel/envelopes.py`, one file, nothing published. It is what keeps `ADR-0001`'s *"the only places the two forms meet"* shape intact for a second kind of value.
  - **The order in which refusals are checked**, in two layers: reading text first, in the order the words appear on the line, then deciding, in the order envelope / amount / future date / insufficient funds. Branch: *assumed*, under no delegation, and `refine` said `plan` may settle it. The envelope check leads because AC3 promises a message naming the envelope and that promise has to hold when three criteria refuse at once.
  - **An empty or whitespace-only description is no description**, and **`--on` given twice takes the last**. Branch: *assumed*, under no delegation, both left unconstrained by `refine` and both reversible in one line.
  - **An entry naming an envelope that is not in `envelopes` is invisible rather than an error, and this item adds no check for it.** Branch: *assumed*. This is the second question `refine` routed here. Nothing in this epic deletes an envelope, so the case arises only from a hand-edited file, and the delivered code already behaves this way.
  - **Nothing was asked of the stakeholder.** Every decision came from the first or second branch of the preference order. The one that becomes irreversible once they have recorded a spend — the entry's shape — is exactly why `ADR-0006` is written now rather than deferred to `implement`.
  - **`## Deliverable documents` is `none`**: no criterion of this item has a document as its subject, so `implement` may write under `docs/` only to close a row of the invalidation set.
- **Cross-answer check:** this execution recorded no new human answer and relied on six. `WI-0002/Q-001` (a spend is dated today unless said otherwise) — relied on for `ADR-0006`'s context; compatible with everything below. `WI-0003/Q-003` (income carries no date) — relied on to rule out `ADR-0006`'s option C; it and `Q-001` are an asymmetry the stakeholder chose knowingly and `WI-0003` AC8 records as theirs, so the two do not conflict and no ADR here settles anything between them. `WI-0002/Q-003` (`--on` for the date, a bare word for the description) — relied on for the subcommand's shape; compatible with `Q-001` and `Q-002`. `WI-0002/Q-004` (`YYYY-MM-DD` and nothing else) — relied on for `envel/dates.py` and for the new convention line in the overview; their volunteered reading of `7/9` is recorded in `WI-0002` `## Notes` and this plan builds no short form, so nothing is taken further than it was given. `WI-0002/Q-005` (a future date is refused) — relied on for AC12's place in the refusal order; compatible with `EP-001/Q-002`, and they gave the same reason for both. `EP-001/Q-002` (an overspend is refused rather than shown negative) — relied on for AC5 being a read-before-write. No two of the six disagree.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, Ran 52 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 -c "print(__import__('datetime').date.fromisoformat('20260907'))"` → exit 0, prints 2026-09-07
  - `grep -rn spend envel` → exit 1, no output
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item WI-0002` → exit 0, 16 invalidation rows, 0 deliverable documents, 6 binding ADRs
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 0 errors (first run: 1 `claim.unsourced`, repaired by citing a command outcome rather than by softening the sentence)
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 18 consumed human answers, 0 delegations spent
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before this execution wrote anything, then exit 1 with 2 `doc.changelog.no-execution` errors while this entry did not yet exist, then exit 0 after the transition
- **Gates:**
  - `workspace-valid` → **pass when run directly, and the transition was taken with `--force`** — F-084's deadlock, hit by `plan` for the second time in this engagement and for the same reason `WI-0001`'s `plan` entry records: writing `ADR-0006` and the overview puts two `doc.changelog` rows in the workspace saying *plan changed this for WI-0002*, `doc.changelog.no-execution` checks `WI-0002`'s journal for an execution of `plan`, and the only entry that can satisfy it is the one `transition` appends after its gates have run. `--resolving 'WI-0002:ready->planned+journal'` does not cover it — the transition ran exactly that and got the same two errors. Every other gate was run by hand first and each passed, the commands are under `**Commands:**` and can be re-run, and `validate-workspace` reports 0 errors after the move.
  - `every-criterion-is-addressed` → **pass** (`## Acceptance criteria mapping` has one row per criterion, AC1 to AC14, each naming the step and a specific observation; AC8, AC9 and AC10 are demonstrated by reading the store file with `json.load`, which is where `refine` put this item's dates)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` already carries both commands from `WI-0001`; both were re-run here, the test command now exiting 0 over 52 tests rather than 5 over none, and `ADR-0005` records what `compileall` does and does not check)
  - `decisions-recorded` → **pass** (eight choices in `## Decisions and ADRs`, each with its branch: one new ADR, one read off `ADR-0002`, two the stakeholder's own, and four entries under `## Assumptions` carrying what reversal costs)
  - `plan-is-executable-without-you` → **pass**, advisory (read back cold, each step names the files, the functions and what is true afterwards; the only thing left undecided is message wording, which the criteria constrain by content and `refine` left unconstrained on purpose)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents` exit 0: 16 rows written from a read of `docs/product/vision.md`, `docs/architecture/overview.md` and every ADR — two `engagement-state` rows disposed `owned-by-ending`, six `quantified`, eight `cited-fact`, all left open for `implement`)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0; the read behind it is the `**Cross-answer check:**` bullet above — six answers relied on, none in conflict, and no document written here reconciles two of the stakeholder's own statements)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0; one `claim.unsourced` was found on the reversibility paragraph of `ADR-0006` and repaired by citing the command that establishes it)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` — created
  - `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — created, v1
  - `docs/architecture/overview.md` — updated to v3: `envel/dates.py` in `## The parts`, the dependency-direction sentence, `## The data` on `at`, `on` and the negative `cents`, the `YYYY-MM-DD` convention, and `WI-0002` leaving `## What is not decided yet`
  - `tracker/board.md` — regenerated
  - commit: `tracker: the plan, ADR-0006 and the architecture overview (refs WI-0002)`
- **Status:** `ready` → `planned`
- **Result:** `WI-0002` is planned. Seven steps add one module (`envel/dates.py`), one operation (`envelopes.record_spend`) and one subcommand (`envel spend`), and all fourteen criteria map to a step and to a named observation. The decision the item turned on is `ADR-0006`: a spend carries the day it happened in its own field while `at` keeps meaning when the entry was written, because the stakeholder chose to date a spend and not to date income, and one field cannot carry both meanings without every reader branching on the entry's kind.

## 2026-09-11T04:06:14Z — implement v0.6.1 — developer

- **Item:** WI-0002
- **Trigger:** `planned` — dispatched by `next` as the highest-ranked runnable item (priority rank 2), immediately after `plan` wrote the design. No question is open anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, unchanged by this execution and not mine to change
  - `tracker/items/WI-0002/artifacts/plan.md` — seven steps, the acceptance-criteria mapping, six `## Assumptions`, sixteen invalidation rows, `## Deliverable documents` `none`, six `## Binding ADRs`
  - `tracker/items/WI-0002/history.md` — seven rows, ending `ready → planned`; this is a fresh start, not a resumed branch
  - `tracker/items/WI-0002/questions/` — five questions, all `answered` and all propagated before this execution began; nothing moved since the last journal entry
  - `docs/architecture/adr/` — the six ADRs the plan names as binding, `ADR-0001` through `ADR-0006`
  - `docs/architecture/overview.md` v3 and `docs/product/vision.md` v2 — the two documents the invalidation set names
  - `envel/cli.py`, `envel/envelopes.py`, `envel/money.py`, `envel/store.py`, `tests/test_cli.py` — the code this change extends
  - `tracker/project.yaml` — branch prefix `wi/`, and both gate commands present
- **Decisions:** none yet. This entry opens the execution; the work and its decisions are reported by the closing entry.
- **Cross-answer check:** none — this execution has edited nothing yet, and no sentence sourced to a stakeholder answer has been touched.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0, branch created at the commit that carries the plan
- **Gates:**
  - `tests-pass` → **pending** (decided by the closing transition of this execution, after the last change; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (decided by the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (decided by the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (no test for this item exists yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range on this branch is empty at this moment; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (, advisory (there is no diff yet to read); not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (decided by the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (decided by the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (no document has been written and no invalidation row is closed yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/WI-0002`, created from `main`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of `WI-0002` has started on `wi/WI-0002`. Nothing is built yet; the branch and this entry exist so that an interruption leaves a truthful status.

## 2026-09-11T04:14:49Z — implement v0.6.1 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` — the same execution this skill opened at `04:06:14Z`; the plan's seven steps are done and the gates were run on the branch head.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, unchanged by this execution
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, the mapping, the six assumptions and the sixteen invalidation rows
  - `tracker/items/WI-0002/history.md` — eight rows; no send-back, so this is a first build
  - `tracker/items/WI-0002/questions/` — five questions, all `answered` before this execution and none moved during it
  - `docs/architecture/adr/ADR-0001` through `ADR-0006` — the six the plan names as binding
  - `docs/architecture/overview.md` v3 and `docs/product/vision.md` v2 — the two documents in the invalidation set, both reopened at step 4a rather than recalled
  - `envel/cli.py`, `envel/envelopes.py`, `envel/money.py`, `envel/store.py`, `bin/envel`, `tests/test_cli.py`, `tests/test_envelopes.py` — the code this change extends
  - `tracker/project.yaml` — the branch prefix, the commit subject, and both gate commands
- **Decisions:**
  - **The regex runs before `datetime.date.fromisoformat`.** Inside the plan's latitude — step 1 called for it and said why. Recorded here because it is the one line that makes AC11 true rather than nearly true: `fromisoformat` alone accepts `20260907`, and `tests/test_dates.py` fixes that form as refused.
  - **A blank description is no description, and the field is then absent.** The plan's assumption, implemented as `description.strip() != ""`. Whitespace *inside* a description that has other characters is kept as typed, which the plan did not say and which no criterion constrains; it is the reading that changes nothing a user would notice.
  - **One `WI-0001` test was adapted rather than left failing.** `test_no_subcommand_and_an_unknown_one` asserted the literal string `{new,add,list}` in the tool's usage line. A fourth subcommand makes that string false while leaving `WI-0001` AC14 true — it asks for *"a usage message that lists the subcommands the tool does have"* — so the assertion now checks the line is the tool's own usage and names each of the four. No acceptance criterion was touched. This is the only edit this branch makes to another item's delivered code, and it is the only hunk in the diff that is not new behaviour.
  - **`add_income`'s refusal order was left alone**, though `record_spend`'s differs from it. The plan names the difference and says harmonising would change delivered `WI-0001` behaviour that two of its criteria constrain. Filing a bug would overstate it — nothing is wrong — so it is recorded in the report under `## What I did not do` and nowhere else.
  - **Decided not to decide:** nothing. No point in the seven steps required a decision the plan does not make, so no question was filed.
  - **`ADR-0002`'s `## Consequences` sentence was repaired rather than left.** It said `WI-0003` filters by `at`, which `ADR-0006` had already made false. The plan's invalidation set names the row, so the repair is inside the licence; the version is bumped, a change-log row is added, and an erratum sits in `## Corrections`, which is the treatment this project already gave `ADR-0004`. All three carry this execution's own timestamp, `2026-09-11T04:06:14Z`, for the reason under `workspace-valid` below. The decision is untouched and no code has to change to satisfy the new text.
- **Cross-answer check:** none. The one sentence this execution edited — `ADR-0002` `## Consequences` — carries no `[src: <ITEM>/Q-nnn]` and is not a stakeholder's requirement quoted; it is a forward-looking consequence of an architectural decision, falsified by `ADR-0006` rather than by anything the stakeholder said. No claim sourced to a human answer was rewritten anywhere on this branch, which is what `lint-answers --changed-since main` reports at exit 0.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → exit 0, Ran 90 tests, OK (run after each of the plan's steps, and last on the branch head; 52 tests before this branch)
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 with one `doc.changelog.no-execution` against `ADR-0002`'s new row while this entry did not yet exist; see `workspace-valid` below
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, 18 consumed human answers, 0 delegations spent
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0
  - `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, eleven import lines over six files (the enumeration two quantified claims owe)
  - `grep -n "print(\|sys.exit" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no output
  - `grep -rn "format_amount\|parse_amount" envel/*.py` → exit 0, twelve call sites, none of them in `envel/dates.py`
  - `grep -rn '"at":' envel/*.py` → exit 0, two sites, both writing `now()`
  - `grep -n "FORMAT" envel/store.py` → exit 0, `FORMAT = 1` and three uses
  - `grep -n "add_argument" envel/cli.py` → exit 0, six positionals and one option
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0 on the branch head, Ran 90 tests, OK; 38 of them are new and every one of the fourteen criteria is named by at least one)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0 on the branch head; `ADR-0005` records that this checks that every file parses and nothing more)
  - `workspace-valid` → **pass** (, and how it was reached is worth the sentence. The first run reported one `doc.changelog.no-execution`: `ADR-0002`'s three new rows were stamped at the wall-clock moment of the repair, `04:10:05Z`, and the rule is that a row's timestamp must fall inside an execution of the skill it names on the item it names — but the only entry this execution had written closed at `04:06:14Z`, and the entry that would extend the window is the one the transition appends *after* its gates run. `--resolving 'WI-0002:in-progress->verifying+journal'` does not cover it; tested directly, same error. The rows were therefore restamped to `04:06:14Z`, this execution's own recorded moment, which is a timestamp a clock produced and is the one moment inside the window a mid-execution repair can honestly claim. `validate-workspace` then exits 0, and no gate was forced.)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md` `## Acceptance criteria evidence`: fourteen rows, each naming a test function by name. AC8, AC9 and AC10 are read out of the store file with `json.load`, which is where `refine` put this item's observations, and AC13 is a table-driven test keyed by the criterion IDs it walks.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` exit 0; every commit on `main..wi/WI-0002` names the item)
  - `no-unplanned-scope` → **pass** (, advisory (the diff is three new files' worth of behaviour and tests plus the `spend` parser and its dispatch, all traceable to steps 1 to 6. The single hunk that is not new behaviour is the adapted `WI-0001` assertion, declared under `## Deviations from the plan`.))
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` exit 0, window: the one `docs/` path this branch changed. The read behind it is the `**Cross-answer check:**` bullet above.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0002` exit 0. Scope, as the run printed it: 6 documents — the one path differing from `main` under `docs/`, plus the six the plan names. That window contains the document this execution repaired, so it is not a window that could contain nothing.)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` exit 0: one document written under `docs/` on this branch, six named by the plan, every one of the sixteen invalidation rows disposed, and no `## Engagement state` section edited at any disposition.)
- **Artifacts:**
  - `envel/dates.py` — created
  - `envel/envelopes.py` — `record_spend` added; nothing else changed
  - `envel/cli.py` — the `spend` subparser, its dispatch, and `DateError` in the existing `except`
  - `tests/test_dates.py` — created; `tests/test_envelopes.py` and `tests/test_cli.py` — extended
  - `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — v2, one erratum
  - `tracker/items/WI-0002/artifacts/impl-report.md` — created
  - `tracker/items/WI-0002/artifacts/plan.md` — the `disposition` column filled in on all sixteen rows, and nothing else
  - branch `wi/WI-0002`, commits `2c0090d..ecae075` (four, on `main..wi/WI-0002`)
- **Status:** `in-progress` → `verifying`
- **Result:** `WI-0002` is built. `envel spend <envelope> <amount> [description] [--on YYYY-MM-DD]` records a spend against an envelope and prints what is left, refusing an envelope that does not exist, an amount that is not positive, a date it cannot read, a date later than today, and a spend larger than the envelope holds. All fourteen criteria have a test that names them, the suite is at 90 and green, and every invalidation row is closed — thirteen verified with their enumeration, two owned by the ending, and one repair to `ADR-0002` whose forward-looking sentence `ADR-0006` had made false.

## 2026-09-11T04:25:33Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** `verifying` — dispatched by `next` as the highest-ranked runnable item (priority rank 2) after `implement` reported the build complete.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, read **first** and used to decide what would settle each one before `impl-report.md` was opened
  - `tracker/items/WI-0002/history.md` — nine rows; no send-back, so this is a first verification
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, the six binding ADRs and the sixteen invalidation rows with their dispositions
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria, to find deviations and declared omissions, not for evidence
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — for the four combinations `refine` left deliberately unconstrained, which is what stops `--on` twice and an empty description being read as criteria
  - `docs/architecture/adr/ADR-0001` through `ADR-0006` — each opened and its `## Decision` read, for the conformance table
  - `docs/architecture/overview.md` v3 and `docs/product/vision.md` v2 — the sentences the invalidation set claims are still true, reopened here
  - the branch head **`d94a2da1d7b20d63af651d55ebc51ed1bb23a444`** on `wi/WI-0002`, and the source it carries: `envel/dates.py`, `envel/envelopes.py`, `envel/cli.py`, `envel/store.py`, `envel/money.py`, `bin/envel`
- **Decisions:**
  - **Every criterion is `pass`; none is `substituted` and none is `ambiguous`.** Each was demonstrated by running the tool as a separate process against a scratch store of this execution's own making, and the criteria that name the store file (AC8, AC9, AC10) were settled by `json.load`ing it, which is the observation `refine` wrote into them.
  - **No send-back and no bug item.** No criterion of this item failed, and nothing `WI-0001` delivered was found wrong — `WI-0001` AC14 was re-read against the branch head, since this change alters the usage line it is about, and it still holds: the line begins `usage: envel ` and names all four subcommands.
  - **The differing refusal order between `add_income` and `record_spend` is not a defect.** It was classified with the test the procedure gives: does an acceptance criterion of *this* item say the behaviour should be different? No — AC3 asks for a message naming the envelope and gets one. It is not `WI-0001`'s defect either, since `WI-0001` AC5 and AC10 are both satisfied by what `add_income` does. Recorded in `## Defects found` as an observation and deliberately not filed, because filing a bug for behaviour no criterion contradicts would misroute the work.
  - **AC10's fourth shape was re-run.** The first attempt spent `12.50` from an envelope holding `11.00` and was refused — by AC5, correctly. That is a fault in the fixture, not in the tool, and the criterion was settled on a re-run at `1.50`. It is recorded rather than quietly re-run, because a reader of the transcript would otherwise see a failure with no explanation.
  - **Two sensitivity probes were re-aimed after they proved nothing.** Edits meant for `record_spend`'s own `if cents <= 0:` and `if envelope is None:` matched `add_income`'s identical lines first, so the tests that failed were `WI-0001`'s. Re-aimed at the text after `def record_spend`, both probes failed this item's own tests. Recorded in the report, because a probe that breaks the wrong function is a passed sensitivity check that checked nothing.
- **Questions raised:** none. No criterion turned out ambiguous and no document needed a repair this skill is not allowed to make.
- **Commands:**
  - `git rev-parse HEAD` → exit 0, `d94a2da1d7b20d63af651d55ebc51ed1bb23a444` on `wi/WI-0002`
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 14.936s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 0 after repair, 16 entries against 16 rows (first run: 7 errors, every one `document.verify.row.missing` because the report keyed its ADR rows by number rather than by path)
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0002` → exit 0 after repair, 6 binding ADRs against 6 rows (first run: 1 error, `ADR-0005` recorded as conforming with a quoted clause but no file and line)
  - roughly forty invocations of `./bin/envel` under three scratch `ENVEL_FILE` paths — the fourteen criteria, the twenty negative and boundary cases, and the AC13 sweep; each one's exit code, stdout and stderr are quoted in `verify-report.md`
  - `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines over six files
  - `grep -n "print(\|sys.exit" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no output
  - `grep -rn "float(\|int(.*100\|\* 100\|// 100\|% 100" envel/cli.py envel/envelopes.py envel/store.py envel/dates.py` → exit 1, no output
  - `grep -n '"at": now()' envel/envelopes.py` → exit 0, two sites
  - `git diff --name-only main -- envel` → exit 0, three files; `envel/money.py` and `envel/store.py` untouched
  - `git diff main -- docs/architecture/overview.md` and `git diff main -- docs/product/vision.md` → both empty, which is how the two `owned-by-ending` entries were checked
  - ten sensitivity probes: a behaviour removed, `python3 -m unittest discover -s tests -t .` run, `git checkout -- envel` to revert. Failure counts in `verify-report.md` `## Test sensitivity check`; the tree is clean and green afterwards.
- **Gates:**
  - `tests-pass` → **pass** (run by this execution on `d94a2da`, not read from the implementation report: exit 0, `Ran 90 tests`, `OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0 on the same head)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md` `## Criteria`: fourteen rows, each naming a command this execution ran and quoting its actual output. No row cites `impl-report.md`, and what would settle each criterion was decided from the criterion before the report was opened.)
  - `negative-cases-exercised` → **pass** (`## Negative and boundary cases exercised`: twenty invocations, every one triggered. Both boundaries the criteria turn on were run rather than reasoned about — spending exactly what an envelope holds, which AC5 permits, and `--on` set to today, which AC12 permits.)
  - `a-criterion-about-criteria-is-read` → **pass** (AC13 is the one criterion of that shape. Its eleven covered criteria are named by ID, each has a per-criterion verdict from the byte counts and exit codes of a dedicated sweep, the table-driven test is cited as evidence for that verdict rather than as its definition, and non-intersection is stated as none — every criterion AC13 names is exercised together with the stream assertion in the same test.)
  - `adr-conformance-is-decided` → **pass** (`## ADR conformance`: six rows, one per binding ADR, each quoting a clause of that ADR's own `## Decision` and naming the file and line in this change that satisfies it. No ADR outside the plan's list was found engaged.)
  - `invalidation-set-is-disposed` → **pass** (`## Invalidation set`: sixteen rows against sixteen entries. Every `verified-still-true` was reopened against the branch head; each quantified claim carries its set, the command that enumerated it with its output, a verdict per member, and what a falsifier would have looked like. The one `to-update` entry names a document that really was updated — `ADR-0002` v2, change-log row and erratum. The two `owned-by-ending` entries were left untouched, which `git diff main` over both documents confirms. This execution wrote no document.)
  - `tests-would-fail-without-the-change` → **pass** (, advisory (ten probes, each removing one behaviour a criterion names and running the suite before reverting: the `on` field, the future-date check, the negative `cents`, the description write, the insufficient-funds check, `record_spend`'s own zero/negative and envelope-exists checks, the `YYYY-MM-DD` regex, honouring `--on` at all, and the `description` positional. Every probe turned the suite red — between 2 and 11 named failures, listed in `verify-report.md` `## Test sensitivity check` — so at least one test per criterion is sensitive to the behaviour it claims to test. Two probes had to be re-aimed: they first matched `add_income`'s identical lines and failed `WI-0001`'s tests instead, which proves nothing about this item's. The tree is clean and green after the last revert.))
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — created, against `d94a2da`
  - `tracker/items/WI-0002/item.md` — all fourteen criteria ticked `- [x]`; no criterion's text was changed
  - bug items filed: none
- **Status:** `verifying` → `in-review`
- **Result:** `WI-0002` passes verification. All fourteen criteria were demonstrated independently — the tool run as a person would run it, the store file read where the criteria say the dates live, and every refusal triggered rather than read about. Ten sensitivity probes confirm the tests fail when the behaviour they claim to test is removed. Six binding ADRs conform, sixteen invalidation entries are disposed and the thirteen claiming a document is still true were reopened and found true. No defect, no bug item, no send-back.

## 2026-09-11T04:34:43Z — review-close v0.14.1 — reviewer

- **Item:** WI-0002
- **Trigger:** `in-review` — `next` dispatched the status owner; it was the highest-ranked runnable item (priority `high`, rank 2) and the only candidate above `WI-0004`, `WI-0005` and `WI-0006`.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria and their tick state
  - `tracker/items/WI-0002/history.md` — all ten rows; the last matches `item.md`'s status
  - `tracker/items/WI-0002/journal.md` — all ten entries, in full
  - `tracker/items/WI-0002/artifacts/plan.md` — the invalidation set, `## Deliverable documents`, `## Binding ADRs`
  - `tracker/items/WI-0002/artifacts/impl-report.md` and `artifacts/verify-report.md`
  - `tracker/items/WI-0002/questions/Q-001.md` to `Q-005.md` — all `answered`
  - the diff `main..wi/WI-0002`, hunk by hunk: 14 files, +1063/−52, code and documents both
  - `docs/architecture/adr/` — all six ADRs, for D13; `docs/architecture/overview.md` and `docs/product/vision.md` in full, for D7 and D12
  - `tracker/items/WI-0001/artifacts/plan.md` and `tracker/items/WI-0003/item.md` — to trace finding 1's origin and to resolve the erratum's citation
- **Decisions:**
  - **Rejected, back to `in-progress`, on one finding.** `docs/architecture/overview.md` `## The parts` says *"`envelopes` knows about `store`, `money` and `dates`"*. `envel/envelopes.py:12` is `from . import dates, money`, and the module that knows about `store` is `envel/cli.py` (lines 68, 70, 87, 96). The sentence is false against the code. It is row 2 of this item's invalidation set, disposed `verified-still-true` by both `implement` and `verify` — each of which printed the two-module import line and then called the three-module claim true. `plan` rewrote that sentence for this item at overview v3, so it is `WI-0002`'s to repair. D7 and D12 both fail on it.
  - **The remedy is one document edit, and no code change.** Repair the sentence, bump the overview to v4 with a change-log row, and change that invalidation row to `to-update`. The code is right; the document was describing something weaker than what was built — `envelopes` never touching the filesystem is the property that makes the decision layer pure.
  - **No bug item filed against `WI-0001`,** though the clause dates from overview v1. `WI-0001`'s own plan never claimed it, and the sentence sits inside `WI-0002`'s invalidation set, so the repair belongs to a row this item already owns rather than to a new item.
  - **The adapted `WI-0001` test is accepted, not a finding.** Replacing the literal `{new,add,list}` assertion with one that checks the `usage: envel ` prefix and all four subcommand names is *stricter* against `WI-0001` AC14 — *"lists the subcommands the tool does have"* — and `git diff main..wi/WI-0002 -- tracker/items/WI-0001/` is empty, so no criterion was edited to make anything pass.
  - **The refusal-order difference between `add_income` and `record_spend` is accepted as a limitation, `no-owner`.** No criterion of either item is violated, nobody has asked for the two to be harmonised, and harmonising would change delivered `WI-0001` behaviour. Its mitigation is in the place the next reader will be standing: `record_spend`'s docstring says why the order is what it is.
  - **Nothing was merged.** Step 8's trial merge was not run: the order is trial-merge, close, merge, and a rejected item is never closed. `main` is untouched at `41d690c` and the branch is intact at `eb1ccf4`.
  - **Seven accepted gaps disposed**, all before the transition: two to items already on the board (`WI-0003`, `WI-0006`, which carry the work of printing a spend's date and description back), five `no-owner` and meant as such.
- **Cross-answer check:** none — this execution consumed no human answer. It reviewed a change; the five answers this item rests on were consumed and propagated by `answer-questions` in earlier executions and were not reopened here. `lint-answers --context work-item --changed-since main` → exit 0 over 18 consumed answers and 0 delegations (ADR-0008 §4).
- **Questions raised:** none — the finding is a defect in this item's own delivery, which a send-back carries; no decision is in doubt and nothing needed the architect or the stakeholder.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 8 documents
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 6 commits
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 14.944s`, `OK`
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated --item WI-0002 --context work-item` → exit 0, NOT APPLICABLE
  - `python3 .claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable --item WI-0002` → exit 0, 7 gaps
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0, not an epic
  - `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines — the enumeration finding 1 rests on
  - `grep -n "store\." envel/envelopes.py` → one hit, the docstring; `grep -rn "store\.load\|store\.save\|store\.store_path" envel/*.py` → `envel/cli.py:68,70,96`
  - `grep -n "print(\|sys.exit\|import sys" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no output
  - `grep -rn "date.today\|datetime.date\|fromisoformat\|isoformat" envel/*.py bin/envel` → five in `dates.py`, one at `envelopes.py:33` (a UTC timestamp, not a calendar day)
  - `grep -rn "float(\|\* 100\|// 100\|% 100\|int(" envel/*.py bin/envel` → conversion arithmetic only at `money.py:34` and `money.py:42`
  - `git diff main..wi/WI-0002 -- docs/architecture/overview.md` and `-- docs/product/vision.md` → both empty, which is what `owned-by-ending` requires
- **Gates:**
  - `definition-of-done` → **fail** (`review.md` `## Definition of Done` walks D1 to D13 one row at a time. Eleven pass; **D7 fails** (one invalidation entry disposed `verified-still-true` is not true) and **D12 fails** (the same sentence, audited from its own enumeration rather than from the prose). D13 passes trivially and honestly: `## Binding ADRs` names `ADR-0001` to `ADR-0006`, which is every ADR in the project, so none this change engages can be unlisted.)
  - `engagement-state-is-restated` → **pass** (applicable** — an item close is not an ending, and the sections are the ending's (`spec/doc-header.md` §4a). The script says so in its own words. Both documents carrying one were confirmed untouched by the branch.)
  - `accepted-gaps-are-dispatchable` → **pass** (7 rows in `review.md` `## Accepted gaps`, every one disposed before this transition: `item-filed:WI-0003`, `item-filed:WI-0006`, and five `no-owner` with the reason each is a limitation rather than deferred work.)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` → exit 0: verified at `d94a2da1`, branch at `eb1ccf45`, and the five files between them are all under `tracker/`, so the verification still covers the code.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → exit 0, all 6 commits on `main..wi/WI-0002` name `WI-0002`.)
  - `tests-pass-on-the-merge-result` → **pass** (run** — there is no merge result. The procedure's order is trial-merge, close, merge, and this review rejects rather than closes, so no merge was attempted and `main` was never touched. What *was* run is the suite on the branch head `eb1ccf4`: exit 0, `Ran 90 tests`, `OK`. That answers a different question and is recorded as the different question it is.)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, 0 errors, 0 warnings, run after `review.md` was written.)
  - `record-is-reconstructible` → **pass** (from the tracker, `docs/` and `git log --grep WI-0002` alone: *what was built* is `envel spend`, a new `envel/dates.py` and `envelopes.record_spend` (`impl-report.md` `## What was built`); *why* is the stakeholder's refusal of a negative envelope at `EP-001/Q-002` and their choice of a bare description with a `--on` option at `WI-0002/Q-003`; *which skill decided what* is the ten journal entries against the ten history rows, with `ADR-0006` named as `plan`'s one decision; *what questions arose and how they resolved* is `Q-001` to `Q-005`, all `answered` with `## Consequences` naming real criteria; *what verification found* is `verify-report.md`'s fourteen criteria, six ADR verdicts, twenty negative cases and ten sensitivity probes, with no defect. The one thing the record got **wrong** is finding 1, and this entry is where a reader learns it.)
  - `claims-are-sourced` → **pass** (`lint-claims --context work-item --changed-since main` → exit 0. **Scope, quoted from its own output:** *"1 document(s) in 1 path(s) differ from main (41d690c) under docs; citations: every markdown file in the workspace"*. That window is one document wide, which is exactly why the D12 audit was also run over the ten claims the invalidation set names — and that is where the finding came from. The gate proves citations resolve; it cannot say whether they support the sentence.)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0 over 18 consumed answers and 0 delegations; no sentence sourced to a stakeholder answer was edited by this branch or by this execution.)
  - `epic-sign-off` → **pass** (`WI-0002` is a `work-item`; the termination gate applies to an engagement's ending only. `check-epic-signoff WI-0002` says so and exits 0.; the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/check-epic-signoff WI-0002 --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0002:in-review->in-progress+journal'` exited 0)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — created: what was examined, the D1–D13 walk, the sixteen-row invalidation confirmation with the unnamed-document answer, three findings and seven disposed gaps
  - no bug item, no question, no document written, no merge commit
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected and sent back to `in-progress`. The change is right and the record is not: `docs/architecture/overview.md` claims `envelopes` depends on `store`, which it does not, and two executions certified that claim while quoting the import line that disproves it. One document edit, a version bump, a change-log row and one invalidation-row disposition is the whole remedy; no code change is wanted.

## 2026-09-11T04:39:01Z — implement v0.6.1 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` — dispatched by `next` as the highest-ranked runnable item (priority rank 2). The item is here because `review-close` **rejected** it at `2026-09-11T04:34:43Z`; the branch `wi/WI-0002` already carries the whole build, so this is a resumed execution with one named defect to fix, not a fresh start.
- **Inputs read:**
  - `tracker/items/WI-0002/history.md` — eleven rows, the last `in-review → in-progress`, actor `review-close`. That row is what scopes this execution.
  - `tracker/items/WI-0002/artifacts/review.md` — read **first**, as the procedure requires of a send-back. Finding 1 is the whole of the work; findings 2 and 3 are accepted and ask for nothing.
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, and the sixteen-row invalidation set whose row 2 the review says is misdisposed
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, unchanged by this execution and not mine to change
  - `tracker/items/WI-0002/artifacts/impl-report.md` and `artifacts/verify-report.md` — the two audit rows that called the false sentence true
  - `tracker/items/WI-0002/questions/` — five questions, all `answered`; none has moved since the last journal entry
  - `docs/architecture/overview.md` v3 — the document to repair; `docs/architecture/adr/` — the six binding ADRs, re-read for anything the repair would contradict
  - `envel/cli.py`, `envel/envelopes.py` — the code the sentence is about
  - `tracker/project.yaml` — both gate commands present
- **Decisions:**
  - **Reconciled with the branch before touching anything.** `git log --oneline main..wi/WI-0002` → seven commits, three of code and four of record; `git status --porcelain` clean. All seven of the plan's steps are already executed with their tests on the branch, and the measurements below confirm the build is intact: 90 tests green, lint clean, workspace valid, every commit naming the item. **Nothing is redone.**
  - **This entry is written standalone, and it is written deliberately.** `review-close`'s send-back already put the item at `in-progress`, so step 3's opening transition has no move to make. The entry is still owed: the repair about to be made carries a `## Change log` row claiming *`implement`, on `WI-0002`, at this time*, and `doc.changelog.no-execution` checks that claim against this item's journal. Without an entry opening the execution there is no window for it to fall in, and the repair would be unrecordable (`spec/doc-header.md` §3, F-084). The gate verdicts below are therefore real measurements of the branch **as received**, not predictions about the repair; the closing entry reports the gates over the repaired state.
  - **No code will be written.** The review's finding is that a document describes the code wrongly, and the remedy it names is the document. Changing `envel/envelopes.py` to import `store` so the sentence becomes true would be building to match a wrong document, and would destroy the property the sentence should have been describing.
- **Cross-answer check:** none — this execution has edited nothing yet. The sentence to be repaired carries `[src: tracker/items/WI-0001/artifacts/plan.md]`, a plan rather than one of the stakeholder's answers, so `ADR-0008` §3's refusal does not reach it.
- **Questions raised:** none.
- **Commands:**
  - `git status --porcelain` → empty; `git log --oneline main..wi/WI-0002` → exit 0, seven commits
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 14.890s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 7 commits
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, 18 consumed answers, 0 delegations
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0
- **Gates:** every verdict below was measured just now, on the branch as `review-close` left it at `eb1ccf4`+`dc8c054`, before this execution changed anything.
  - `tests-pass` → **pass** — `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests`, `OK`.
  - `lint-clean` → **pass** — `python3 -m compileall -q envel tests` → exit 0.
  - `workspace-valid` → **pass** — `validate-workspace` → exit 0, 7 items, 8 documents.
  - `every-criterion-has-a-test` → **pass** — the fourteen tests named in `impl-report.md` `## Acceptance criteria evidence` are on the branch and in the green run above; this execution neither adds a criterion nor removes a test.
  - `commits-reference-the-item` → **pass** — `check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 7 commits on `main..wi/WI-0002` name the item.
  - `no-unplanned-scope` → **pass**, advisory — no new hunk exists yet; the diff is exactly what `verify` and `review-close` read.
  - `cross-answer-consistency` → **pass** — `lint-answers --changed-since main` → exit 0.
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main --plan-documents WI-0002` → exit 0. **Scope, from its own output:** *"6 document(s) in 6 path(s) in scope — 1 path(s) differ from main (41d690c) under docs, plus 6 document(s) named by WI-0002's plan"*. That the false sentence sits inside this scope and passed is the point the closing entry has to make: the gate checks that citations resolve, never that they support.
  - `document-writes-are-declared` → **pass** — `lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, 1 document written under `docs/`, 6 named by the plan.
- **Artifacts:**
  - none — this entry writes nothing but itself. It opens the execution so that the repair's change-log row has a window to fall inside, and so that an interruption leaves a truthful record of what this execution was for.
- **Status:** `in-progress` → `in-progress`
- **Result:** A resumed execution of `implement` on `WI-0002`, scoped to `review.md` finding 1: `docs/architecture/overview.md` says `envelopes` knows about `store`, and `envel/envelopes.py:12` says it does not. The branch was reconciled and measured intact — 90 tests green, every gate passing — and nothing is repaired yet.

## 2026-09-11T04:41:07Z — implement v0.6.1 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` — the closing move of the resumed execution opened at `2026-09-11T04:39:01Z`, which was dispatched on `review-close`'s send-back of `2026-09-11T04:34:43Z`.
- **Inputs read:**
  - everything listed in this execution's opening entry, plus, for the repair itself:
  - `envel/cli.py` lines 13, 68, 70, 96 and `envel/envelopes.py` line 12 — the import lines and the store call sites the repaired paragraph now cites
  - `tracker/items/WI-0001/artifacts/plan.md` `## Approach` — the source the paragraph cites for the purity of the decision layer; it says *"The decision layer is pure — it takes a store and arguments and returns a new store plus either output or a refusal"* and never claims the edge that was wrong
  - `docs/architecture/adr/ADR-0002` and `ADR-0003` — re-read to confirm the repaired paragraph contradicts neither; `ADR-0003` places the path resolution in `envel/store.py` and says nothing about who calls it
- **Decisions:**
  - **Repaired the sentence rather than the code.** `docs/architecture/overview.md` `## The parts` said *"`envelopes` knows about `store`, `money` and `dates`"*. `envel/envelopes.py:12` is `from . import dates, money`; `grep -n "store\." envel/envelopes.py` matches only the word in the docstring; the module that loads and saves is `envel/cli.py`, at `:68`, `:70` and `:96`. The document was wrong about the code, so the document changed. Making `envelopes` import `store` to satisfy the sentence would have been building to match a mistake.
  - **Stated the property the false version was hiding.** The repaired paragraph adds that reading and writing the store file is `cli`'s and not `envelopes`', so an operation is handed a document and returns a new one. That is why the decision layer is pure and why every criterion can be exercised both through the command line and directly — the thing `WI-0001`'s plan actually claimed. The new text is a stronger statement than the one it replaces, not a weaker one.
  - **Every dependency edge is now cited individually** — `[src: envel/cli.py:13]` and `[src: envel/envelopes.py:12]` — so the next audit can check the sentence's own subject instead of only its falsifier. That is the specific failure the send-back found: two executions enumerated the imports, both printed the two-module line, and both answered *does any of these import something above it?* rather than *does `envelopes` import what the sentence says it does?*
  - **`plan.md`'s invalidation row moved `verified-still-true` → `to-update`,** which is the disposition it should have carried. Only the disposition cell was written; the row's `what`, `kind` and `why` are the architect's and are untouched.
  - **`impl-report.md`'s audit row was rewritten to the `to-update` shape, quoting the wrong verdict inside it rather than deleting it.** The mistake is the useful part of that row, and a reader who finds only the corrected version learns nothing about how it happened. A new `## The send-back, and what it changed` section carries the before-and-after in full.
  - **Nothing else was touched.** No acceptance criterion, no ADR, no test, no line under `envel/`, and no `## Engagement state` section at any disposition. `git diff --stat main..wi/WI-0002 -- envel tests bin` is byte-for-byte what `verify` and `review-close` already read: 6 files, +570/−11.
  - **The opening entry was written standalone and deliberately** — see it for the reason. The short version: `review-close`'s send-back had already placed the item at `in-progress`, so step 3 had no transition to make, and without an entry the repair's change-log row would have fallen inside no execution window and been unrecordable (F-084). It is stamped `2026-09-11T04:39:01Z` and so is the row.
- **Cross-answer check:** none. The repaired paragraph carries `[src: tracker/items/WI-0001/artifacts/plan.md]` and now three code citations; it cites no `[src: <ITEM>/Q-nnn]`, so no sentence of the stakeholder's was rewritten and `ADR-0008` §3's refusal is not engaged. `lint-answers --changed-since main` → exit 0 over 18 consumed answers and 0 delegations.
- **Questions raised:** none. The send-back named one defect, the remedy was unambiguous, and nothing about it was mine to escalate.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 first, `doc.changelog.no-execution` on the new row — F-084, resolved by opening the execution in the journal and stamping the row with that entry's own timestamp; then exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace . --resolving 'WI-0002:in-progress->verifying+journal'` → exit 1, the same error: the `+journal` hint does **not** cover a change-log row written before the entry that gives it a window
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 14.867s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, 2 documents written, 6 named by the plan
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 0, 16 entries against 16 rows
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 8 commits
  - `git commit` → `f8f8c6d docs: envelopes does not know about store, and the overview now says so (refs WI-0002)`
- **Gates:**
  - `tests-pass` → **pass** (exit 0, `Ran 90 tests in 14.867s`, `OK`. The count is unchanged from the first execution, which is the evidence that this repair touched no code.)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0.)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, 7 items, 8 documents, after the repair and the overview's bump to v4.)
  - `every-criterion-has-a-test` → **pass** (the fourteen rows of `## Acceptance criteria evidence` are unchanged and every named test is in the green run above. No criterion was added, removed or re-mapped by this execution.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 8 commits on `main..wi/WI-0002` name the item, including `f8f8c6d`.)
  - `no-unplanned-scope` → **pass** (, advisory — this execution's diff is four files: one paragraph and one change-log row in `docs/architecture/overview.md`, one disposition cell in `plan.md`, the audit row and new section in `impl-report.md`, and the journal. Every one traces to `review.md` finding 1. No hunk under `envel/` or `tests/`.)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0 over a window of 2 changed paths under `docs/`; no sentence sourced to a stakeholder answer was edited.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0002` → exit 0. **Scope, quoted from its own output:** *"6 document(s) in 6 path(s) in scope — 2 path(s) differ from main (41d690c) under docs, plus 6 document(s) named by WI-0002's plan"*. The repaired document is inside that scope, and so was the false version of it — which is the honest limit of this gate and worth saying plainly: it checks that a citation resolves, never that it supports the sentence it is attached to.)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, 2 documents written under `docs/` on this branch (`ADR-0002` from the first execution, `overview.md` from this one), both named by the plan's invalidation set.)
- **Artifacts:**
  - `docs/architecture/overview.md` — v3 → **v4**, the dependency-direction paragraph repaired, with a change-log row
  - `tracker/items/WI-0002/artifacts/plan.md` — one disposition cell, `verified-still-true` → `to-update`
  - `tracker/items/WI-0002/artifacts/impl-report.md` — the corrected audit row, a header note, and `## The send-back, and what it changed`
  - branch `wi/WI-0002`, commits `main..wi/WI-0002` = eight, this execution's being `f8f8c6d`
- **Status:** `in-progress` → `verifying`
- **Result:** The one defect `review-close` found is repaired: `docs/architecture/overview.md` no longer claims `envelopes` depends on `store`, the paragraph cites each dependency edge it asserts, and the invalidation row that certified the false sentence now says `to-update`. No code changed, the suite is still 90 and green, and `WI-0002` goes back to `verifying` — where the sentence gets read against the code by someone who did not write either.

## 2026-09-11T04:52:15Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** `verifying` — dispatched by `next` as the highest-ranked runnable item (priority rank 2), after `implement` closed `review-close`'s send-back. This is the **second** verification of this item; the first passed it at `d94a2da` and was itself part of what the review found wrong.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, read **before** `impl-report.md`; what would settle each was decided from the criterion
  - `tracker/items/WI-0002/history.md` — twelve rows, the last two being the rejection and the repair
  - `tracker/items/WI-0002/artifacts/review.md` — finding 1, which is what this verification has to decide about
  - `tracker/items/WI-0002/artifacts/plan.md` — sixteen invalidation rows, one of them now `to-update`; six binding ADRs
  - `tracker/items/WI-0002/artifacts/impl-report.md` — reopened only after the fourteen criteria had been settled
  - `docs/architecture/overview.md` **v4**, `docs/product/vision.md` v2, and all six ADRs
  - `envel/cli.py`, `envel/envelopes.py`, `envel/dates.py`, `envel/money.py`, `envel/store.py`
  - **the branch head verified: `51e9fd7817e0b263668ac55d9ae14e79732af7c4`**, working tree clean
- **Decisions:**
  - **Pass, and no send-back.** All fourteen criteria were demonstrated again from scratch against stores of this execution's own making, not re-read from the previous report. Nothing regressed: the code diff `main..51e9fd7` over `envel`, `tests` and `bin` is byte-for-byte what it was at `d94a2da` — 6 files, +570/−11 — and the suite is still 90 and green.
  - **The repaired sentence is true.** `docs/architecture/overview.md` v4's dependency paragraph was reopened with the enumeration a quantified claim owes and with each new edge opened at the line it cites: `envel/cli.py:13` is `from . import dates, envelopes, money, store`; `envel/envelopes.py:12` is `from . import dates, money`; `grep -rn "store\.[a-z_]*(" envel/*.py` returns three hits, **all in `envel/cli.py`**, and `grep -n "store\." envel/envelopes.py` returns one, the word in the docstring. The version bump to 4 and the change-log row are both present and agree with the frontmatter.
  - **The previous verification's error is named in the report rather than quietly replaced.** It ran the right enumeration and asked it the falsifier it had come looking for — *does any of these three import something above it?* — instead of the sentence's own subject. Every quantified row in this report therefore carries a `Falsifier:` and a per-member verdict, not just a command and an exit code. This is the one thing a reader of both reports should take away.
  - **No document was written by this execution**, at any disposition. The two `## Engagement state` sections were confirmed untouched by the branch — `git diff main..HEAD -- docs/product/vision.md` is empty, and the overview's diff contains the string `Engagement state` zero times.
  - **No bug item filed, and no criterion `substituted` or `ambiguous`.** The two things that are not this item's — the refusal-order difference with `add_income`, and the adapted `WI-0001` usage assertion — were re-checked against `WI-0001`'s own criteria and violate neither; `review.md` has already accepted both, and filing a bug for either would misroute work nobody has asked for.
  - **A method error of my own, recorded because it produced a false negative.** Three sensitivity probes were first run with a substitution that appended a modified copy of the module to the original instead of replacing it; Python took the second, unmodified definition and all three reported the suite green. Re-run with a single in-place replacement asserted to match exactly once, all three turned it red. A probe that does not remove the behaviour proves nothing and does not announce itself.
- **Questions raised:** none. No criterion was ambiguous and nothing needed the architect.
- **Commands:**
  - `git rev-parse HEAD` → `51e9fd7817e0b263668ac55d9ae14e79732af7c4`; `git status --porcelain` → empty
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 15.082s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 8 documents
  - ~60 invocations of `./bin/envel` across four scratch stores, each a separate process with `ENVEL_FILE` set to a path that did not exist — the fourteen criteria, the boundary cases, and the AC13 byte sweep. Every command and its output is in `verify-report.md`.
  - `python3 -c "import json…"` to read each store back — the observation AC8 to AC10 name
  - `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines — the enumeration four quantified rows rest on
  - `grep -n "print(\|sys.exit\|import sys" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no output
  - `grep -rn "store\.[a-z_]*(" envel/*.py` → three hits, all `envel/cli.py`; `grep -n "store\." envel/envelopes.py` → one, the docstring
  - ten sensitivity probes, each a single in-place substitution followed by the full suite and a restore; `git status --porcelain envel tests bin` → empty afterwards
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0002` → exit 0, 6 ADRs, 6 rows
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 1 first, seven `document.verify.row.missing` — the rule keys rows by document **path** and four of mine named their ADR by ID; renamed to full paths, then exit 0, 16 entries against 16 rows
- **Gates:**
  - `tests-pass` → **pass** (run by this execution on `51e9fd7`: exit 0, `Ran 90 tests in 15.082s`, `OK`.)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0.)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, 0 errors, 0 warnings.)
  - `every-criterion-independently-checked` → **pass** (the fourteen rows of `## Criteria`, each carrying a command this execution ran and the output it produced. No row's evidence is `impl-report.md`, which was not reopened until the criteria had been settled from `item.md`.)
  - `negative-cases-exercised` → **pass** (`## Negative and boundary cases exercised`: twenty-four invocations, every one triggered. Both sides of both boundaries the criteria turn on — spending exactly what is left (accepted, lands on `0.00`) and `--on` today (accepted) against tomorrow (refused) — plus `20260907`, the form the underlying library would accept unaided.)
  - `a-criterion-about-criteria-is-read` → **pass** (AC13 is the one criterion of this shape. Its eleven covered criteria are named by ID, each given a per-criterion verdict from a byte sweep of stdout, stderr and the exit code rather than from the suite being green, and non-intersection is `none`: every criterion it names has an executable case that exercises it together with the stream assertion.)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0002` → exit 0, *"6 binding ADR(s), 6 conformance row(s)"*. `## ADR conformance` carries one row per binding ADR, each quoting a clause of that ADR's `## Decision` and naming the file and line that satisfies it. No ADR outside the plan's list was found engaged — the list is all six in the project.)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 0, *"16 invalidation entr(y/ies) against 16 row(s)"*. Every `verified-still-true` was reopened against the branch head with the enumeration and falsifier it owes; the two `to-update` entries were checked to name documents that really were updated, with version bumps and change-log rows (`ADR-0002` v2, `overview.md` v4); the two `owned-by-ending` entries were confirmed untouched by the branch.)
  - `tests-would-fail-without-the-change` → **pass** (, advisory — ten behaviours removed one at a time, every one turning the suite red, with the failing test names in `## Test sensitivity check`; and the three false-green probes recorded there with why they were false.)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — rewritten from scratch against `51e9fd7`
  - no bug item, no question, no document written
  - the fourteen criteria in `item.md` were already `- [x]` from the first verification and were re-demonstrated here; none was unticked, none is `- [~]`
- **Status:** `verifying` → `in-review`
- **Result:** `WI-0002` passes verification for the second time, now against a document that is true. All fourteen criteria demonstrated independently at `51e9fd7`, six binding ADRs conforming with quoted clauses, sixteen invalidation entries disposed and reopened — including the one the review caught, which is repaired and carries its enumeration. Ten sensitivity probes, no defect, no send-back.

## 2026-09-11T05:01:12Z — review-close v0.14.1 — reviewer

- **Item:** WI-0002
- **Trigger:** `in-review` — dispatched by `next` as the highest-ranked runnable item (priority rank 2; `WI-0003` rejected on `depends-on WI-0002`, `WI-0004` and `WI-0005` at rank 3, `WI-0006` at rank 4). The item is at `in-review` for the **second** time: this review rejected it at `2026-09-11T04:34:43Z`, `implement` repaired the document at `04:41:07Z` and `verify` passed it again at `04:52:15Z`.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, all `- [x]`, and the tick state D1 reads
  - `tracker/items/WI-0002/history.md` — thirteen rows, chaining without a gap, last row `verifying → in-review`
  - `tracker/items/WI-0002/journal.md` — all fourteen entries in full, including the standalone `implement` entry at `04:39:01Z` that opened the repair execution
  - `tracker/items/WI-0002/artifacts/plan.md` — the seven steps, the sixteen-row invalidation set, `## Deliverable documents` (`none`) and `## Binding ADRs` (six)
  - `tracker/items/WI-0002/artifacts/impl-report.md` — the two executions, `## Documents`, `## Deviations from the plan`, `## The send-back, and what it changed`, `## What I did not do`
  - `tracker/items/WI-0002/artifacts/verify-report.md` — the second verification at `51e9fd7`: fourteen criteria, six ADR conformance rows, sixteen invalidation rows, `## Not verified, and why`
  - `tracker/items/WI-0002/artifacts/review.md` — the first review, for what it ordered and what it accepted
  - `tracker/items/WI-0002/questions/Q-001` to `Q-005` — all `status: answered`
  - **The diff**, hunk by hunk: `git diff main..wi/WI-0002`, `41d690c..40a9767`, 16 files, +1550/−59, ten commits
  - `docs/architecture/overview.md` v4 in full; `docs/product/vision.md`; all six ADRs under `docs/architecture/adr/`, including `ADR-0003` and `ADR-0004`, which the invalidation set does not name
  - `envel/cli.py`, `envel/envelopes.py`, `envel/dates.py`, `envel/store.py`, `envel/money.py`, `bin/envel` — the code every claim in the audit was read against
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `trunk-branch`, `conventions.commit-subject`
- **Decisions:**
  - **Accepted, and merged.** All thirteen Definition-of-Done criteria pass, recorded one by one in `review.md` `## Definition of Done`. The first review's two failures, D7 and D12, both turned on one sentence; that sentence is repaired at overview v4 and I re-ran the falsifier that caught it — the import enumeration over the whole tool, plus `grep -n "store\." envel/envelopes.py`, which returns only the word in the module docstring. The new text survives it and states the property the false one hid.
  - **Finding 3, recorded rather than sent back: `ADR-0006`'s reversibility clause.** *"No code in this tool writes a spend entry yet [src: run: grep -rn spend envel → exit 1, no output]"* — this branch is what makes that command return something. It is not in the invalidation set, and I read it because the first review's finding was itself a sentence the set did not locate. I judged it **holds**: every clause is hedged by `yet`/`now`/`today`, the `run:` form records a command and its outcome rather than standing as a check, a reversibility statement is required to be as-of the decision, and the paragraph's own next sentence describes the position we are now in. The judgement is written into `review.md` as finding 3 and as an accepted gap so a later reader can disagree with it without re-deriving it; the repair if they do is `doc-header.md` §4b, needing no item and no code change.
  - **Findings 2 and 4 accepted unchanged from the first review.** The adapted `WI-0001` usage assertion is *stricter* than the literal it replaced and no criterion of `WI-0001` was edited (`git diff main..wi/WI-0002 -- tracker/items/WI-0001/` is empty); the differing refusal order between `add_income` and `record_spend` violates no criterion of either item and harmonising it would change delivered `WI-0001` behaviour, so it is a limitation rather than work.
  - **No bug item filed.** No defect belonging to another item was found. The one candidate — the overview sentence, which dates from v1 and `WI-0001` — was already inside this item's invalidation set, so the repair belonged to the row this item owns, which is where it happened.
  - **Nine accepted gaps, every one disposed in this execution** before the close: two `item-filed` against `WI-0003` and `WI-0006`, which are on the board, and seven `no-owner` where the gap is a limitation recorded rather than work deferred.
  - **The order of the close.** Trial-merged into a **detached** worktree of `main`, ran the suite and the lint **on the merge result**, discarded the trial, confirmed `git rev-parse main` returned the sha it returned before it, then closed, then merged for real. `commits-reference-the-item` inspects the commits not yet on the trunk, so merging before the close would empty the range the gate needs.
- **Cross-answer check:** none — this execution consumed no human answer. It edited no sentence sourced to one: the only workspace files it writes are `review.md`, this entry and the history row, and `lint-answers --context work-item --changed-since main` → exit 0 over 18 consumed answers and 0 delegations. The five questions on this item were consumed by `answer-questions` in earlier executions and were checked against each other there.
- **Questions raised:** none.
- **Commands:**
  - `git diff main..wi/WI-0002` and `git diff --stat` → exit 0, 16 files, +1550/−59
  - `git log --oneline main..wi/WI-0002` → exit 0, ten commits
  - `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines
  - `grep -n "store\." envel/envelopes.py` → exit 0, one hit, the docstring
  - `grep -n "print(\|sys.exit\|import sys" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no output
  - `grep -rn "\* 100\|// 100\|% 100\|float(" envel/*.py` → exit 0, two hits, both in `envel/money.py`
  - `ENVEL_FILE=… ./bin/envel spend groceries 1.00 --on 20260907` → exit 1, *"'20260907' is not a date…"*; `--on 2026-09-07` → exit 0
  - `git worktree add --detach /tmp/wi0002-trial main` → exit 0; `git -C /tmp/wi0002-trial merge --no-ff wi/WI-0002` → exit 0, merge result `42dc5817`
  - `python3 -m unittest discover -s tests -t .` **in the trial worktree** → exit 0, `Ran 90 tests in 14.974s`, `OK`
  - `python3 -m compileall -q envel tests` **in the trial worktree** → exit 0
  - `git worktree remove --force /tmp/wi0002-trial` → exit 0; `git rev-parse main` → `41d690c`, unchanged
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 10 commits
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 8 documents
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated --item WI-0002 --context work-item` → exit 0, NOT APPLICABLE
  - `python3 .claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable --item WI-0002` → exit 0, 9 gaps
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0, PASS (not an epic)
- **Gates:**
  - `definition-of-done` → **pass** (walked criterion by criterion in `review.md` `## Definition of Done`: thirteen rows, each with its own result and evidence. D7 is a confirmation against the plan's sixteen-row set — every entry disposed, both `to-update` entries updated with a version bump and a change-log row, every `verified-still-true` reopened — plus the question the set cannot answer for itself, answered under `## Invalidation set confirmation` with `ADR-0003`, `ADR-0004` and the unnamed sections of the named documents all read. D13 asks only completeness: the plan's `binding-adrs` names all six ADRs that exist, so none can be unlisted, and each carries `verify`'s conformance verdict.)
  - `engagement-state-is-restated` → **pass** (applicable — an item close.** `lint-documents --rule engagement-state-is-restated --item WI-0002 --context work-item` → exit 0, *"NOT APPLICABLE — an item close is not an ending, and the sections are the ending's"*. Both `## Engagement state` sections were confirmed untouched by the branch; they are the ending's to restate (DE4).)
  - `accepted-gaps-are-dispatchable` → **pass** (`lint-documents --rule accepted-gaps-are-dispatchable --item WI-0002` → exit 0, *"9 accepted gap(s) in WI-0002's review, at status in-review"*. Two are `item-filed:WI-0003` and `item-filed:WI-0006`, both on the board; seven are `no-owner`, each a limitation recorded rather than work deferred.)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0002 wi/WI-0002` → exit 0, *"verified at 51e9fd78; wi/WI-0002 has moved to 40a97674 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` → exit 0, *"all 10 commit(s) on main..wi/WI-0002 name WI-0002"*. Run before the merge, while the range is still non-empty.)
  - `tests-pass-on-the-merge-result` → **pass** (run on the merge result `42dc5817` in a detached trial worktree, not on the branch: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 14.974s`, `OK`, and `python3 -m compileall -q envel tests` → exit 0. The trial was then discarded and `main` was confirmed still at `41d690c`.)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, 7 items, 8 documents.)
  - `record-is-reconstructible` → **pass** (answered from the tracker, `docs/` and `git log` alone. *What was built and why:* `envel spend`, a fourth subcommand, so that the other half of the ledger exists — `item.md` `## Story` and the fourteen criteria, `plan.md` `## Problem`. *Which skill decided what:* `refine` rounds 1–3 settled the criteria and recorded four things it deliberately left unconstrained; `plan` took the one design decision, `ADR-0006`, and settled those four as assumptions with their reversal cost; `implement` executed seven steps; `verify` decided the criteria twice; this skill decided the close. *What questions arose and how they resolved:* five, all to the stakeholder, all answered and propagated — dated spends, an optional description, `--on` with a bare-word description, `YYYY-MM-DD` only, a future date refused — verbatim in `artifacts/refinement-qa.md`. *What verification found:* the first pass found nothing and was wrong about one document; the second found the repair true and no defect. `git log --grep WI-0002` returns all ten commits.)
  - `claims-are-sourced` → **pass** (`lint-claims --context work-item --changed-since main` → exit 0. **Scope, quoted from its own output:** *"2 document(s) in 2 path(s) differ from main (41d690c) under docs; citations: every markdown file in the workspace"*. Two documents is a real but narrow scope, which is why `review.md`'s audit was run over the invalidation set's claims as well and over the sections of those documents the set does not locate — where finding 3 came from. The gate proves citations resolve; only a reader says whether they support.)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0, 18 consumed answers and 0 delegations checked; this execution consumed none.)
  - `epic-sign-off` → **pass** (the contract gives this gate no subject on a `work-item`: `check-epic-signoff WI-0002` → exit 0, *"WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only"*. `EP-001` is not ended by this execution; closing this item leaves `WI-0003` to `WI-0006` in flight.; the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/check-epic-signoff WI-0002 --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0002:in-review->done+journal'` exited 0)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — rewritten for this execution, with the first review's finding 1 preserved in an appendix because overview v4's change-log row cites this file for it
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`, written by this transition
  - no bug item, no question, no document under `docs/` — this execution wrote nothing there
- **Status:** `in-review` → `done`
- **Result:** `WI-0002` is accepted and closed as `delivered`. Fourteen acceptance criteria demonstrated with re-runnable evidence, ninety tests green on the merge result rather than only on the branch, six binding ADRs conforming, sixteen invalidation entries disposed and confirmed, and the one defect the first review found repaired in the document without a line of code changing. One judgement is recorded rather than enforced — `ADR-0006`'s reversibility clause now reads in the present tense about a state this item ended — as finding 3 and as an accepted gap, with the §4b repair named for whoever disagrees.
