# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T01:32:29Z — intake v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly by the operator on the stakeholder's stated idea in `IDEA.md`; this item did not exist before this execution
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement)
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution — no existing item to overlap with)
- **Decisions:**
  - This item is the daily sitting: only the due cards, and an answer captured for each. Split from WI-0003 because presenting due cards and choosing how far to push them are separately observable — this one can be built and checked with a trivial forward step, before the real rule exists.
  - See EP-001's entry for this execution for how the work was split and why.
- **Questions raised:** none on this item; `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003` were filed on the epic and both blocking ones bear on this item's acceptance criteria
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 --priority high --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, run after this entry and the epic's suspension completed the record)
  - `epic-has-success-measures` → **pass** (EP-001 carries four measures, each checkable by running the tool and reading what it stored; evidence in EP-001's entry)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation`, exit 0; `EP-001/Q-001`)
  - `items-are-separable` (advisory) → **pass** (build order and dependencies stated in EP-001's entry)
  - `no-solution-in-the-problem` (advisory) → **pass** (no technology named in this item's title, story or criteria; the storage medium and the interface are both left open)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/journal.md`, `tracker/items/WI-0002/history.md` (new)
- **Status:** `—` → `draft`
- **Result:** Created at draft with a story, rough acceptance criteria and derived exclusions. Not ready: the criteria state what must be true rather than what to run, because `EP-001/Q-002` is unanswered. `refine` owns it next.

## 2026-08-30T01:41:39Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** not dispatched; this item's artifacts were amended while `answer-questions` consumed the stakeholder's answers to `EP-001/Q-001`, `Q-002` and `Q-003`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — five criteria, and notes naming two things intake had left for `refine`
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's three answers
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md` (v1), `docs/architecture/adr/ADR-0002-the-interval-ladder.md` (v1) — both written by this execution
- **Decisions:**
  - **Amended AC2 to say the run records right or wrong, "a two-way choice and not a scale".** It previously said "how well the person recalled it", which was written that way only because the grading scale was unknown. Basis: *"Just right or wrong, no rating scale"* (`EP-001/Q-003`, `ADR-0002`). This closes one of the two things intake left open on this item.
  - **Did not turn the stakeholder's "a review session that drags on more than a couple minutes" into an acceptance criterion.** It is not decidable as stated: nobody has fixed the deck size it is measured at, and nobody has said whether a sitting should cap how many cards it presents. Turning it into a criterion would have required inventing a number, and inventing a number the stakeholder never gave and then verifying against it is the failure the question protocol exists to prevent. It is recorded in `## Notes` as `refine`'s to put to them, with that instruction written down.
  - **Left "a new card is due the day it was added" as an assumption rather than promoting it.** `ADR-0002` §3 carries it forward and still labels it intake's assumption. `refine` confirms it with the stakeholder; this skill has no basis to convert an assumption into a decision.
- **Questions raised:** none
- **Commands:** none
- **Gates:** recorded in full on `EP-001`'s journal, the item this execution was dispatched on; the amendments here are evidence for its `answer-is-propagated` gate, which passed.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — AC2 amended, `## Notes` replaced
  - `tracker/items/WI-0002/journal.md` — this entry
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The grading question on this item is settled at two answers; the sitting-length constraint the stakeholder volunteered is recorded as an open question for `refine` rather than guessed into a criterion.

## 2026-08-30T02:25:39Z — refine v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority rank 2; WI-0004 and BUG-0001 rank 3, WI-0003 blocked on this item's dependency)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (one row — created by intake, never sent back, so this is a fresh refinement and not a repair), `journal.md` (intake's entry, and `answer-questions`' amendment of AC2)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's three recorded answers, verbatim
  - `docs/product/vision.md` v2 — "What is still open" names both of this item's gaps
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md`, `ADR-0002-the-interval-ladder.md`, `ADR-0004-the-deck-file.md`
  - `tracker/items/WI-0001/item.md` (delivered criteria, AC8 in particular) and `artifacts/refinement-qa.md` (the standing-deferral precedent)
  - `recall/cli.py`, `recall/deck.py`, `recall/store.py` — what `add` already stores and what `review` will inherit
  - `.claude/agile-skills/spec/dor-dod.md`, `spec/question.md`
- **Decisions:**
  - **Rewrote all five criteria as ten, every one against a `recall review` invocation with its input and its observable output named** (`ADR-0001` §4 makes the sitting drivable by a here-document). The five that existed said what must be true; none named a command, which is R4's failure and the reason intake left them that way.
    - AC1 (was AC1) now fixes presentation *order* observably — question side before answer side, one card's output entirely before the next's, no question side twice — instead of the unobservable "one at a time".
    - **AC2 is new** and is what makes "shows the question side before the answer side" real rather than cosmetic: with standard input closed, the answer side must not be printed at all. Order in a transcript is cheap to fake; a reveal that requires an input read is not.
    - AC3 (was AC2) keeps the two-way grade `answer-questions` put there and adds the decidable half: exactly two recognised responses, and an unrecognised one re-asks the same card rather than advancing.
    - AC4 (was AC3) names how the not-due card is set up — a deck file written directly in `ADR-0004` §2's format — because otherwise nobody can construct the state the criterion is about.
    - AC5 (was AC4) unchanged in meaning, given its setup and its exit code.
    - **AC6, AC7, AC10 are new**: the absent deck (`ADR-0004` §6, and a sitting must create nothing), the unreadable deck (WI-0001 AC8's rule extended to a third subcommand, which inherits nothing automatically), and the promise that a sitting does not disturb card text.
    - AC8 (was AC5) unchanged in meaning; **AC9 is new** and covers the interrupted sitting.
  - **Decided two things rather than asking, both from one sentence of the stakeholder's** — *"don't lose my progress"* (`EP-001/Q-001`) — and both marked `[assumed]` in `artifacts/refinement-qa.md`: that "due" means today **or earlier**, and that an interrupted sitting keeps the answers already given (AC9). In each case the alternative directly contradicts a sentence they have already written, so filing a question would be asking them to repeat themselves. The first is named in `Q-001`'s context so they can still object to it.
  - **Routed four decisions to `plan` rather than to the stakeholder**, because the answer would be the same whoever they were: the order due cards are presented in, the wording of the prompts, the two grade responses (AC3 names them by reference to the tool's documentation, the device WI-0001 AC7(a) used), the exit code of a sitting that ends early, and the placeholder forward step that makes AC8 true before WI-0003 exists. All are in `## Notes` as R10 requires, naming `refine` as who left them unconstrained.
  - **Refused to turn *"a review session that drags on more than a couple minutes"* into a criterion.** It is not decidable without a number nobody has given, and inventing one and then verifying against it is the failure the question protocol exists to prevent. Filed as `Q-001` instead. This repeats and does not overturn `answer-questions`' judgement of 2026-08-30T01:41:39Z on this item.
  - **Added four exclusions** to `## Out of scope`: reviewing one named card on demand, correcting an answer from an earlier sitting, any end-of-sitting tally beyond AC5, and filesystem errors that are not content problems. The last draws the boundary against `BUG-0001` explicitly, so `verify` cannot read a passing AC7 as evidence about the bug.
  - **Wrote `artifacts/refinement-qa.md` with `status: agenda`, not `recorded`.** The conversation has not happened; R8 reads that field and must fail while it says `agenda` (`spec/workspace-layout.md` §1.3).
- **Questions raised:** two, both `addressed-to: human`, both blocking, filed as one ask for this item in this round (`spec/question.md` §2, F-020) — `WI-0002/Q-001` (does a sitting cap how many cards it presents, and at what number) and `WI-0002/Q-002` (is a card added today due in today's sitting). Nothing is left `[unresolved]`: every other gap was closed by an answer they had already given, by a decision recorded as `[assumed]` against a sentence of theirs, or by a routing to `plan`.
- **Commands:**
  - `scripts/lint-answers --item WI-0002` → exit 0 (0 consumed human answers on this item; the check is vacuous here and says so)
  - `scripts/validate-workspace .` → exit 1 before the transition, reporting exactly the two conditions this move creates and settles: `question.blocking.not-suspended` on this item and `board.stale`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, judged against the state this move produces, per F-014; the pre-move exit 1 was `question.blocking.not-suspended` — the open blocking questions this entry files — and `board.stale`, both resolved by the transition)
  - `definition-of-ready` → **fail**, criterion by criterion, which is why this item goes to `awaiting-answer` and not to `ready`:
    - R1 **pass** [auto] — `id`, `type`, `epic`, `priority`, `created` all present and set.
    - R2 **pass** — the story names a role ("someone with a deck already built up"), a capability (a sitting showing only due cards and asking how each went), and an outcome ("so that I spend my time on what I am about to forget").
    - R3 **pass** [auto] — ten criteria, `AC1`–`AC10`, each a checkbox.
    - R4 **fail on entry → pass as rewritten** — all five criteria as found named no invocation. Each of the ten now names what to run, what to feed its standard input, and what to look for on stdout, stderr or the filesystem. No criterion contains an unmeasurable adjective; the one adjective in the item — "a couple of minutes" — is deliberately *not* a criterion and is `Q-001`.
    - R5 **pass** — six exclusions, including reviewing a named card on demand and any end-of-sitting tally, both of which a reader could reasonably assume were included.
    - R6 **fail** [auto] — two open blocking questions, `Q-001` and `Q-002`. This is the criterion that stops the item, and it is failing on purpose.
    - R7 **pass** [auto] — `depends-on: WI-0001`, which is `done`.
    - R8 **fail** [auto] — `artifacts/refinement-qa.md` exists and declares `status: agenda`. An agenda for a conversation that has not happened does not satisfy R8, which is exactly what the field is for.
    - R9 **pass** — one coherent change: one new subcommand over storage that already exists. The scheduling arithmetic is WI-0003 and is excluded in terms.
    - R10 **fail on entry → pass** — the behaviours this item introduces are now each covered: due/not-due (AC4), nothing due (AC5), absent deck (AC6), unreadable deck (AC7), unrecognised grade response (AC3), interrupted sitting (AC9), second run the same day (AC8), and effect on the rest of the deck (AC10). Four are recorded in `## Notes` as deliberately unconstrained with `refine` named as who left them so. The two combinations still undecided — a cap, and a card added today — are visible in `## Notes` as the open questions they are, which is R10's requirement; it is R6 and R8 that stop the item, not R10.
  - `criteria-are-decidable` → **pass** for all ten. AC1: three due cards, here-document, read stdout for order and for repeats. AC2: `recall review < /dev/null`, assert the answer side is absent from stdout. AC3: unrecognised response then a recognised one, assert the same card is re-asked and the next card's question side has not appeared. AC4: deck file written with dates today and today+7, assert the second question side is absent, exit 0. AC5: all dates in the future, assert the "nothing due" line, no question side, exit 0. AC6: no deck file and no parent directory, assert both still absent afterwards and exit 0. AC7: six kinds of damaged deck as WI-0001's verification used, assert stderr names the path, exit non-zero, and the file hashes identically either side. AC8: two subprocesses, assert the finished card's question side is absent from the second. AC9: input for one card then EOF, assert no `Traceback (most recent call last)` on stderr and that the second run presents card two and not card one. AC10: `recall list` before and after, compare.
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item WI-0002`, exit 0). This execution consumed no human answer — it filed two and quoted three already-consumed ones from `EP-001` without re-deriving anything from them — so there is no `## Cross-answer check` to write yet; the section is written by whoever consumes `Q-001` and `Q-002` (`spec/question.md` §2). The two answers this refinement quoted are checked against each other in `EP-001/Q-001`–`Q-003` already, and nothing written today contradicts either: `ADR-0002`'s ladder and `ADR-0001`'s command line are both assumed by the criteria rather than argued with.
  - `qa-recorded-verbatim` → **pass with its state declared**. `artifacts/refinement-qa.md` carries every question this round asked, each stakeholder quotation verbatim from the question that recorded it, every `[assumed]` decision with the sentence it rests on, and the two filed questions as `[pending]`. It declares `status: agenda` because the exchange has not happened; nothing in it is paraphrased into agreement, and no answer is attributed to the stakeholder that they did not write.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — criteria rewritten from five to ten, four exclusions added, `## Notes` replaced
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` (new, both `addressed-to: human`, both blocking)
  - `tracker/board.md` (regenerated by this transition)
  - a commit of the above, subject `tracker: the refined criteria and two questions for the stakeholder (refs WI-0002)`
- **Status:** `draft` → `awaiting-answer`
- **Result:** Ten decidable criteria replace five that named no command, and every gap this item had is now either closed against something the stakeholder already said, routed to `plan`, or in front of them as one of two questions. The item is suspended at `awaiting-answer` with `resume-to: draft`; R6 and R8 are the criteria failing, both by design, and both are cleared by the same two answers.

## 2026-08-30T02:32:20Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer` with both blocking questions replied to by the
  stakeholder; consumed before `next` was run, per the resume path in `spec/question.md` §3
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` (both `open`, both with `## Answer`
    filled in by the human)
  - `tracker/items/WI-0002/item.md`, `history.md` (the suspending row carries `resume-to: draft`)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: agenda`)
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the three prior recorded
    human answers, read for the cross-answer check
  - `docs/architecture/adr/ADR-0002-the-interval-ladder.md` (v1), `ADR-0001` (v1), `ADR-0004` (v1)
  - `docs/product/vision.md` (v2)
  - `.claude/agile-skills/spec/question.md`, `spec/journal-and-history.md`, `spec/doc-header.md`
- **Decisions:**
  - **Q-001 answered by the human, not by me** (route 4 was already taken by `refine`; this
    execution is the consumption). No cap on a sitting. Propagated as **AC11** rather than as a
    note alone: *"Show me everything that's due"* is observable behaviour, and a criterion is the
    only thing that stops a later execution quietly adding a cap. Rationale for not inventing a
    length criterion as well: they were shown the trade-off and declined it, so a
    couple-of-minutes criterion would be ours, not theirs.
  - **Q-002 answered by the human.** A card added today is due today. Propagated as **AC12** and
    used to retire the assumption in `ADR-0002` §3, which had named this refinement as the thing
    that would confirm it. The rule in §3 is unchanged — only its standing. No bug filed and no
    delivered behaviour touched: `recall add` already writes `due` = the day added, so the
    confirmation costs nothing.
  - **The apparent contradiction with `EP-001/Q-001` was not escalated, and the reason is in the
    record rather than in my judgement.** *"A review session that drags on more than a couple
    minutes"* would make the tool a failure; refusing a cap means nothing bounds a sitting. That
    is the F-062 shape. It is not that failure because `Q-001`'s own `## Context` and option A put
    the trade-off to them explicitly — including that the sentence would stay a design constraint
    and not become a criterion — and they chose it anyway and reconciled the two themselves:
    *"If it's a big pile after a week away I'll just stop partway, that's fine by me."* The
    question that would have been filed has already been asked and answered by its author.
  - **Their earlier sentence was not rewritten to agree.** `docs/product/vision.md` "Who it is
    for" still carries the couple-of-minutes quote whole, with its `[src: EP-001/Q-001]`. The
    bullet under "What it is for" that asserted a sitting *is* over in a couple of minutes was
    amended, because as a claim about the product it is now false — and it was amended by adding
    both statements and attributing the reconciliation to them, not by deleting the older one.
    This is the ordinary-repair half of `lint-answers` rule 3, and it is declared here.
  - **No scope widening.** Neither answer implies work no item records, so no new item was filed.
  - **WI-0001 left alone.** Q-002 confirms what it delivered; amending a closed item's frozen
    criteria to restate a confirmation would add nothing.
- **Cross-answer check:**
  - `WI-0002/Q-001` checked against `EP-001/Q-001` — **compatible**, reconciled by the stakeholder
    inside the answer itself (see Decisions); `EP-001/Q-002` — **compatible**, a terminal makes
    stopping partway trivial; `EP-001/Q-003` — **compatible and supporting**, a lengthening ladder
    is what keeps an uncapped sitting short on ordinary days; `WI-0002/Q-002` — **compatible**,
    both trade sitting length for seeing everything due.
  - `WI-0002/Q-002` checked against `EP-001/Q-003` — **compatible**, it fixed how a card moves and
    said nothing about where it starts; `EP-001/Q-001` — **compatible**, the cost lands on sitting
    length, which they had just declined to bound; `WI-0002/Q-001` — **compatible**.
  - No verdict was `conflicts`, so no question was filed under ADR-0008 §3.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 1 first (`answer.conflict.unescalated`
    on Q-002), then exit 0 after the fix below
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 2 uncommitted paths under `docs`
    in the claim window, 5 consumed human answers checked
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 (`claim.citation.unresolved` on
    `vision.md`), then exit 1 with only the two errors this transition clears
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was
    reopened and the change confirmed present: `item.md` (AC11 at line 77, AC12 at line 82,
    `## Notes` rewritten), `refinement-qa.md` (`status: recorded`, both answers verbatim under
    their entries), `ADR-0002` (§3 rewritten, v2, change-log row), `vision.md` (v3, both bullets).
  - `answered-from-the-record` → **pass**. Both answers are the human's own words, quoted
    verbatim; neither was decided by me. `ADR-0002` §3 is cited for what Q-002 confirms.
  - `escalation-is-justified` → **skipped**, nothing was escalated. Recorded because the
    non-escalation of the `EP-001/Q-001` tension is the judgement call of this execution, and it
    is argued above rather than passed over.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0; and
    `lint-answers --uncommitted`, exit 0, which is the rule-3 check over the `docs/` edits).
  - `workspace-valid` → **pass** (`validate-workspace .`; the two remaining errors were
    `board.stale` and `question.awaiting.none-open`, both of which this transition and the
    following `board-gen` clear, and neither of which can be cleared before it).
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft`; this
    execution moves the item to `draft`, not to `ready` — every blocking question is now resolved,
    but the Definition of Ready is `refine`'s to re-check, not mine.
  - `a-deferral-is-not-an-answer` → **not applicable**. Neither reply deferred: each names an
    option letter and gives a reason. Both are `answered`, neither `deferred`, and the item
    resumes rather than parking at `blocked`.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — `answered`, `answered-by: human`,
    `answered-at: 2026-08-30T02:28:46Z`; `## Cross-answer check` and `## Consequences` written
  - `tracker/items/WI-0002/questions/Q-002.md` — same stamps; `## Cross-answer check` and
    `## Consequences` written
  - `tracker/items/WI-0002/item.md` — AC11 and AC12 added; `## Notes` rewritten
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `agenda` → `recorded`; both answers
    recorded verbatim as `[human]`; "What is still open after this round" rewritten
  - `docs/architecture/adr/ADR-0002-the-interval-ladder.md` — v1 → v2
  - `docs/product/vision.md` — v2 → v3
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both blocking questions on WI-0002 are answered in the stakeholder's own words and
  propagated into six files; a sitting is uncapped (AC11) and a card added today is due today
  (AC12), which also retires the last assumption in `ADR-0002`. The item returns to `draft` for
  `refine` to re-check the Definition of Ready, which is now unblocked on R8.

## 2026-08-30T02:35:52Z — refine v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority
  rank 2; BUG-0001 and WI-0004 rank 3; WI-0003 not runnable, `depends-on` this item)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: recorded` since
    `answer-questions` consumed the answers)
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, the stakeholder's
    words verbatim
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the three prior recorded
    human answers
  - `docs/product/vision.md` (v3), `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v2),
    `ADR-0004` (v1)
  - `tracker/items/WI-0001/item.md` — AC7 and AC8, the criteria AC6/AC7 here are written against
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **This is a resumed refinement, not a fresh one.** `history.md` row 2 shows the item left
    `draft` for two questions and row 3 shows it returned when they were answered. So round 1's
    conversation stands and was not re-opened; this execution is the Definition of Ready walk it
    could not finish. Nothing already agreed was re-asked.
  - **Nothing was asked of the stakeholder.** The walk found no remaining gap with product stake:
    what is left is either decidable from the record or is `plan`'s under `ADR-0001`. Filing a
    question to report having none would spend the scarcest thing in the loop on nothing.
  - **AC13 added — an overdue card is still presented.** Round 1 decided that "due" means today
    *or earlier*, wrote it into the criteria preamble and `## Notes`, and showed it to the
    stakeholder in `Q-001`'s context — but left no criterion that exercises it. AC4 tests today
    against seven days ahead; nothing put a card in the past. A reading that lives only in prose
    is one `verify` cannot check and `implement` can miss without failing anything, and this
    particular reading is the schedule's half of *"don't lose my progress"*. This adds no
    decision; it makes an existing one observable. Recorded `[assumed]` with its authority, and
    AC13 says in terms that the stakeholder not contesting it is not the same as their choosing
    it.
  - **AC5 and AC6 rewritten for decidability.** AC5 said the run *"says so plainly"* — an
    adjective with no threshold, which is the exact tell this skill's own procedure names — and
    both criteria asked a verifier to judge whether some sentence meant "nothing is due". Both
    now name the message **by reference to the documentation the tool ships**, the device
    WI-0001 AC7(a) used for the deck path and the only one available while `ADR-0001` reserves
    wording to `plan`. The verdict is now a read of the docs and a grep of stdout.
  - **AC6 now requires the same message as AC5**, on `ADR-0004` §6: an absent deck *is* an empty
    deck rather than a fault, so "the file is missing" and "everything is scheduled for later"
    are one situation to the person at the terminal, and two messages would invent a distinction
    the record denies. This constrains `plan`, so it is stated as a decision with its basis
    rather than buried in a criterion.
  - **The numbers in the criteria are recorded as witnesses, not requirements.** AC11's
    twenty-five, AC1's three, AC4's seven days are all `refine`'s. The stakeholder gave no
    threshold, and the requirement AC11 encodes is the *absence* of a cap. Written into
    `## Notes` so nobody later reads twenty-five as something they asked for.
  - **`plan` inherits a fifth open design question**, added to `## Notes`: the nothing-due message
    must be documented, because a criterion pointing at documentation fails if the documentation
    is not written.
- **Cross-answer check:** no new answer was recorded by this execution — round 2 asked nothing —
  so there is no new statement of the stakeholder's to check against their prior ones. The two
  answers this item does carry were checked when `answer-questions` consumed them, and those
  sections stand (`Q-001` against `EP-001/Q-001`, `Q-002`, `Q-003` and `WI-0002/Q-002`; `Q-002`
  against `EP-001/Q-001`, `EP-001/Q-003` and `WI-0002/Q-001`; every verdict `compatible`). The
  three decisions above were checked against those answers before being written and none touches
  a sentence of theirs: AC13 makes a `refine` reading checkable, AC5/AC6 name a message they
  never specified, and the witness sizes are explicitly marked as not theirs.
- **Questions raised:** none. Round 1's two are answered and closed; `artifacts/refinement-qa.md`
  holds both rounds, with round 2's three decisions tagged `[assumed]` and nothing `[unresolved]`.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 6 items and 8 documents).
  - `definition-of-ready` → **pass**, criterion by criterion against `spec/dor-dod.md` §1:
    - R1 **pass** [auto] — frontmatter complete; `type: work-item`, `epic: EP-001`,
      `priority: high` all set; `validate-workspace` exit 0.
    - R2 **pass** — the story names the role (*"someone with a deck already built up"*), the
      capability (a single daily sitting showing only due cards and asking how each went) and the
      outcome (*"so that I spend my time on what I am about to forget"*).
    - R3 **pass** [auto] — thirteen criteria, each labelled `AC<n>` as a checkbox.
    - R4 **fail on entry, pass on exit.** AC5 carried *"plainly"*, an unmeasurable adjective, and
      AC5/AC6 both asked a verifier to judge the meaning of a message: both rewritten to name the
      message by reference to the tool's documentation. AC1–AC4 and AC7–AC12 each already named a
      command, its input and the observation; re-read and unchanged. Evidence for every criterion
      is the `criteria-are-decidable` gate below.
    - R5 **pass** — six exclusions, of which at least three are things a reader would reasonably
      assume included: a "study everything" mode, undoing an answer, and any end-of-sitting tally.
    - R6 **pass** [auto] — no open question on this item; both are `answered`.
    - R7 **pass** [auto] — `depends-on: WI-0001`, which is `done`.
    - R8 **pass** [auto] — `artifacts/refinement-qa.md` declares `status: recorded` and holds both
      rounds with every answer tagged `[human]` or `[assumed]`.
    - R9 **pass** — one coherent change: present the due cards, capture an answer, persist it. The
      scheduling arithmetic is WI-0003 and is excluded explicitly, and the item was not split.
    - R10 **fail on entry, pass on exit.** `recall review` takes no flags, so the combinations are
      deck state × input state. Enumerated: due/overdue/future/empty/absent/unreadable deck ×
      full input / EOF immediately / EOF part-way / unrecognised response. Covered by AC1–AC4,
      AC5, AC6, AC7, AC9, AC11, AC12; **overdue was the hole** and is now AC13. Three
      combinations remain deliberately unconstrained and are named in `## Notes` with `refine` as
      who left them so: the presentation order of due cards, the exit code of a sitting that ends
      early, and the placeholder forward step. EOF while re-prompting after an unrecognised
      response falls under the early-end exit code and is covered by that entry.
  - `criteria-are-decidable` → **pass**. Each criterion with what settles it: AC1 three due cards
    via here-document, read stdout ordering and exit code; AC2 `recall review < /dev/null`, grep
    stdout for the answer side; AC3 an unrecognised token then a recognised one, read which card
    is re-asked; AC4 deck with today + today+7, grep for the second question side; AC5 all-future
    deck, grep stdout for the documented nothing-due message and check exit 0; AC6 no deck and no
    parent directory, same message, then `test -e` on both paths; AC7 truncate the deck, read
    stderr for the path, check exit non-zero and `sha256sum` before and after; AC8 two processes,
    grep the second's stdout; AC9 input for one card then EOF, grep stderr for a traceback and the
    second run's stdout; AC10 `recall list` before and after, diff; AC11 twenty-five due cards,
    count distinct question sides on stdout; AC12 `recall add` then `recall review`, grep stdout;
    AC13 deck with today−7, grep stdout and check exit 0.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0; two consumed
    human answers checked). See the `**Cross-answer check:**` bullet for why this execution added
    no new check of its own.
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` holds round 1's two questions with the
    stakeholder's answers quoted whole and tagged `[human]`, the seven round-1 gaps closed
    without asking, and round 2's three decisions tagged `[assumed]` with the authority each
    rests on. Nothing is paraphrased into agreement and nothing is `[unresolved]`.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — AC5 and AC6 rewritten, AC13 added, `## Notes` extended with
    the round-2 assumptions and the fifth design question for `plan`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — "Round 2" section added (entries 8, 9,
    10), "What is still open after this round" updated
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Thirteen criteria, each with a command and an observation behind
  it; the two stakeholder answers are in and recorded; the one substantive hole the walk found —
  no criterion exercised an overdue card, the schedule's half of *"don't lose my progress"* — is
  closed as AC13. Five design questions are routed to `plan`, named as such.

## 2026-08-30T02:42:05Z — plan v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` as the highest-ranked runnable item (priority
  rank 2; BUG-0001 and WI-0004 rank 3; WI-0003 not runnable, `depends-on` this item)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — thirteen criteria, the exclusions, and the five design
    questions `## Notes` routes here
  - `tracker/items/WI-0002/history.md`, `journal.md`, `artifacts/refinement-qa.md` — in
    particular the `[assumed]` entries, which are this design's soft ground
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — the stakeholder's two answers
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`
  - `docs/architecture/overview.md` (v1), `ADR-0001` (v1), `ADR-0002` (v2), `ADR-0003` (v1),
    `ADR-0004` (v1), `ADR-0005` (v1), `docs/product/vision.md` (v3),
    `docs/process/using-recall.md` (v2)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` already set by WI-0001's plan
  - **Code:** `recall/cli.py`, `recall/store.py`, `recall/deck.py`, `bin/recall`,
    `recall/__main__.py`, `tests/support.py`, `tests/test_list.py`
  - `tracker/items/WI-0001/artifacts/plan.md` and `verify-report.md` — the latter for where the
    project's documentation lives, since three criteria here are decided by reading it
  - `tracker/items/BUG-0001/item.md` — to fix the boundary rather than widen this plan
- **Decisions:**
  - **`ADR-0006` written: a sitting records the last answer as an optional `grade` key.** The item
    asks that an answer be *"stored against the card"* and `ADR-0004` owns the file, so this is a
    storage decision, not a plan step. Route 1 could not settle it — `ADR-0002` says only what
    *scheduling* needs — so it went to route 3 as an architect's decision with three options
    weighed. Chosen: absent until reviewed, two legal values, malformed is `DeckUnreadable`,
    written only when set, and `DECK_FORMAT_VERSION` does not move because the change is additive
    in both directions and spending the version on it would leave nothing to mark a real
    migration. An append-only review log was rejected partly because it is the substrate for the
    statistics the epic excludes.
  - **Four decisions answered from documents (route 1), recorded rather than skipped.** The
    conversation's shape — question, wait, answer, grade — is `ADR-0001` §4 verbatim. Two
    responses and not a scale is `ADR-0002` §1. Exit 0 for a sitting that ends part-way follows
    from `ADR-0001` §5: `0` is success and non-zero is *"a refused or failed operation"*, and
    stopping part-way is neither. Catching `DeckUnreadable` at one site rather than starting a
    fresh sitting is `ADR-0004` §5.
  - **The re-prompt after an unrecognised response must not reprint the question side.** AC1
    requires each question side to appear exactly once and AC3 requires the same card to be asked
    again; the only shape satisfying both is a re-issued grade prompt carrying no card text. This
    is written into `## Approach` as a contract because the natural phrasing of such a prompt
    ("did you get *der Bahnhof* right?") breaks AC1 silently.
  - **The deck is saved after every graded card, not once at the end.** Forced by AC9 — a single
    save at the end loses every answer in an abandoned sitting, which is the stakeholder's stated
    failure condition and, since `Q-001`, their stated normal use of the tool. No ADR: there is no
    alternative that satisfies AC9.
  - **Five assumptions recorded with what reversing each costs** (route 2): deck order for the due
    cards, exit 0 on an early end, the placeholder forward step, no closing line at the end of a
    completed sitting, and reading `date.today()` with no injectable clock. The placeholder was
    chosen so that half of it is already `ADR-0002`'s real rule for a *wrong* answer and it leaves
    `rung` untouched, so WI-0003 has no stored state to undo. The no-closing-line assumption is
    flagged in the plan as the one most likely to be wrong in a person's hands, and as something
    to reverse by asking rather than by a later plan deciding a tally is fine.
  - **Step 6 makes the documentation a required deliverable, not dressing.** AC3, AC5 and AC6 name
    the two grade responses and the nothing-due message *by reference to the tool's own
    documentation*, so `docs/process/using-recall.md` is where those three criteria are decided. A
    criterion that points at documentation fails if the documentation is not written.
  - **`BUG-0001` is not absorbed.** `review` reaches the deck through the same `store.load`, so it
    inherits the same weakness; the plan says so under `## Risks` and repeats the item's warning
    that a passing AC7 is not evidence about the bug.
  - **Nothing was asked of the stakeholder.** No decision here is irreversible and none turns on
    intent no document records; the two that did were asked at refinement and are answered.
- **Cross-answer check:** this execution relied on two recorded human answers — `WI-0002/Q-001`
  (no cap; *"I'll just stop partway"*) and `WI-0002/Q-002` (a card added today is due today) — and
  recorded no new one. Checked against `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003` and each
  other: every verdict **compatible**, the same verdicts `answer-questions` recorded when it
  consumed them, re-read here rather than assumed. The one pair that could have needed
  reconciling — the couple-of-minutes sentence in `EP-001/Q-001` against the no-cap answer — was
  reconciled by the stakeholder inside `Q-001` itself, so this plan quotes their reconciliation
  and neither chooses between the two nor edits either. `docs/architecture/overview.md` property 2
  was rewritten, and that edit is the ordinary kind: the sentence said the question was *"still
  open with the stakeholder"*, which is a claim about our own record and is now simply false. No
  sentence of theirs was touched. `lint-answers --uncommitted` exit 0 is the mechanical half.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1 (`claim.unsourced` on
    ADR-0006's Supersedes line), then exit 0 after the citation was added; exit 0 again after the
    overview edit, 2 documents checked
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 5 consumed human answers
    checked in the claim window of 2 uncommitted `docs/` paths
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 (`adr.section.missing` and
    `doc.changelog.missing` on ADR-0006), then exit 0 after the change log was added
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 6 items and 9 documents).
  - `every-criterion-is-addressed` → **pass**. `plan.md`'s `## Acceptance criteria mapping` has
    one row per criterion, AC1 through AC13, each naming the step that satisfies it and a
    specific demonstration — an input, an assertion and an exit code — rather than "tests". Two
    rows name step 2 or 3 alongside step 4 where the criterion turns on a value-layer or storage
    behaviour as well as the command.
  - `project-commands-resolved` → **pass**, unchanged. `commands.test` is
    `python3 -m unittest discover -s tests -t . -q` and `commands.lint` is
    `python3 -m compileall -q recall tests`, both set by WI-0001's plan against measurements in
    `ADR-0003`, both already run in this project by that item's implementation and verification.
    `commands.build` is `null` and honestly so — `ADR-0005` gives the tool no build step. This
    execution changed nothing in `tracker/project.yaml`, and adding a test framework is not a
    decision this item forces.
  - `decisions-recorded` → **pass**. One ADR created (`ADR-0006`) for the one decision with
    alternatives worth naming; four decisions answered from existing ADRs and listed under
    `## Decisions and ADRs` with the section each follows from, so a reader can see they were
    decided rather than passed over; five assumptions under `## Assumptions`, each with what
    reversing it costs. No ADR was superseded and no ADR reconciles two of the stakeholder's own
    statements — see the cross-answer bullet.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0, which is the
    rule-3 check over both `docs/` edits; `lint-answers --item WI-0002` exit 0 at refinement and
    nothing on this item's questions changed since).
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0 over
    `ADR-0006` and `docs/architecture/overview.md`). One real finding on the way: ADR-0006's
    `Supersedes` line made an absolute claim about `ADR-0004` with nothing behind it, and the
    citation was added rather than the sentence softened.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0006-what-a-sitting-records-against-a-card.md` (new, v1)
  - `docs/architecture/overview.md` — v1 → v2
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. Six steps, no new module, and the three-layer split unchanged;
  thirteen criteria each mapped to a step and a specific demonstration. One ADR was needed —
  what a sitting stores against a card — and everything else came from `ADR-0001`, `ADR-0002` and
  `ADR-0004` or is a recorded assumption with its reversal cost. The two things most likely to go
  wrong are written down as contracts rather than left to taste: a re-prompt that reprints the
  question would break AC1, and an unflushed prompt would make the tool appear to hang for its
  user while passing every criterion.

## 2026-08-30T02:42:34Z — plan v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** not dispatched; a correction to the `plan` entry immediately above, appended rather
  than edited (`spec/journal-and-history.md` — both files are append-only and a wrong entry is
  corrected by a later one)
- **Inputs read:**
  - `.claude/skills/plan/references/contract.md` — the gate table, line 47
  - `tracker/items/WI-0002/artifacts/plan.md` — re-read for the check below
- **Decisions:**
  - **What was wrong:** the entry above records six gates and omits the seventh,
    `plan-is-executable-without-you`. It is advisory rather than hard, which is why the transition
    still passed, but `spec/journal-and-history.md` §2.2 requires *every* gate in the contract to
    appear under `**Gates:**`, advisory included and skipped ones included — a silently omitted
    gate is the failure the format exists to prevent. The omission came from following SKILL.md's
    journaling section, which says "all five", rather than the contract's table, which lists
    seven. That mismatch is worth reporting as a toolkit defect and is noted in
    `HARNESS-STATUS.md`.
  - **Nothing in the plan changed.** This entry adds the missing gate result and touches no
    artifact.
- **Cross-answer check:** none — this execution recorded and relied on no human answer; it
  reports a gate result on work already journalled above, whose own cross-answer check stands.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - `plan-is-executable-without-you` (advisory) → **pass**. Read as a stranger, each of the six
    steps names the files it touches and what is true afterwards, and step 4 defers only to
    `## Approach` in the same document, which states the sitting as a numbered contract. One
    latitude is left deliberately and is bounded: the exact sentences of the reveal prompt, the
    grade prompt and the nothing-due message are the developer's, because `ADR-0001` reserves
    message wording and no criterion turns on a particular sentence. What the criteria *do* turn
    on is fixed here — the two recognised responses are `y` and `n`, AC5 and AC6 share one
    message, and step 6 requires both to be documented. The one place a stranger could still go
    wrong is covered by an explicit prohibition rather than left to inference: the grade prompt
    and its re-issue must not carry the card's question text, or AC1 fails.
  - The other six gates are recorded in the entry above and are not restated here.
- **Artifacts:** none
- **Status:** `planned` → `planned` (unchanged)
- **Result:** The `plan` entry above is complete as corrected: seven gates, not six. The plan,
  the ADR and the item are unchanged.

## 2026-08-30T02:44:51Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next` as the highest-ranked runnable item (priority rank 2, created 2026-08-30T01:30:02Z); BUG-0001 and WI-0004 are runnable but rank 3, WI-0003 is blocked on `depends-on: WI-0002`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — all thirteen acceptance criteria, `## Out of scope`, and `## Notes`
  - `tracker/items/WI-0002/artifacts/plan.md` — six steps, the sitting contract, the AC mapping table, five assumptions
  - `tracker/items/WI-0002/history.md` — five rows; the last is `ready` → `planned`, so this is a fresh start and not a send-back
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`; their consequences are already in `item.md` as AC11 and AC12
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`, `conventions.commit-subject`
  - `docs/architecture/adr/ADR-0006-what-a-sitting-records-against-a-card.md` — the optional `grade` key this item stores
  - `recall/deck.py`, `recall/store.py`, `recall/cli.py`, `tests/support.py`, `tests/test_add.py`, `tests/test_storage.py` — the code WI-0001 left, which every step extends rather than replaces
  - `docs/process/using-recall.md` v2 — the documentation AC3, AC5 and AC6 are decided by reading
- **Decisions:**
  - none yet — this entry opens the execution. Every choice inside the plan's latitude is recorded in the closing entry.
- **Cross-answer check:** none — this execution has edited no document yet.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no code has been written on this branch)
  - `lint-clean` → **skipped** (not yet run: no code has been written on this branch)
  - `workspace-valid` → **skipped** (not yet run: the completion gates run on the branch head, after the last change)
  - `every-criterion-has-a-test` → **skipped** (not yet run: `tests/test_review.py` is plan step 5 and does not exist)
  - `commits-reference-the-item` → **skipped** (not yet run: the branch has no commits of its own)
  - `no-unplanned-scope` → **skipped** (advisory; not yet run: there is no diff)
  - `cross-answer-consistency` → **skipped** (not yet run: nothing has changed since `main`)
  - `claims-are-sourced` → **skipped** (not yet run: nothing has changed since `main`)
- **Artifacts:**
  - branch `wi/WI-0002`, created from `main` at d2ca976
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started on `wi/WI-0002`. Nothing is built yet; the closing entry reports the work and the gates.

## 2026-08-30T02:53:11Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** resuming this execution's own `in-progress`, opened at 2026-08-30T02:44:51Z; the plan's six steps are complete
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the thirteen criteria this execution built against
  - `tracker/items/WI-0002/artifacts/plan.md` — six steps, the sitting contract, the AC mapping table, five assumptions
  - `docs/architecture/adr/ADR-0006-what-a-sitting-records-against-a-card.md` — §1–5, implemented in `store.py` and `deck.py`
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md`, `ADR-0002-the-interval-ladder.md`, `ADR-0004-the-deck-file.md` — the constraints the plan assumes and does not restate
  - `recall/cli.py`, `recall/deck.py`, `recall/store.py`, `tests/support.py`, `tests/test_add.py`, `tests/test_storage.py` — WI-0001's code, extended rather than replaced
  - `docs/process/using-recall.md` v2 — the file AC3, AC5 and AC6 are decided by reading
- **Decisions:**
  - **The two recognised responses are `y` and `n`**, held in `RIGHT_RESPONSE`/`WRONG_RESPONSE` and mapped to the grade constants. They were first derived from the constants' initials (`r`/`w`), which contradicts `plan.md`'s §"The two recognised responses" and its step 6; corrected before step 4 was committed. The plan owns message wording (`ADR-0001`), so this was not mine to re-decide.
  - **A stored `"grade": null` is `DeckUnreadable`, not "absent".** `plan.md` step 3 says only "absent on read is `None`" and leaves a literal JSON null unaddressed; `ADR-0006` §3 does address it — present and not one of the two words — so the ADR decided it. The tool never writes null, so this is reachable only by hand-editing.
  - **`run_recall`'s `stdin` defaults to an immediately-closed pipe** rather than the parent's inherited standard input, which is what "defaults to today's behaviour" literally meant. Indistinguishable for `add` and `list`, and it makes a `review` test that forgets its input fail at EOF instead of hanging the suite. Recorded as a deviation.
  - **Every criterion was checked by mutation, not by reading.** Fourteen mutations were applied to the source in turn and the suite run each time, to establish that the mapped test fails when the behaviour is removed. Which test caught which mutation is tabulated in `impl-report.md`. This was the only way to satisfy `every-criterion-has-a-test` honestly, since a test asserting a substring can pass against a great deal that is wrong.
  - **Decided *not* to make, and not escalated either, because the plan already made them:** card order (deck order), the exit code of a sitting ended early (0), and the placeholder forward step (tomorrow, `rung` untouched). Each is an `## Assumptions` entry in `plan.md` with its reversal cost, so executing it is not a decision of mine.
  - **`BUG-0001` was not fixed**, though `review` inherits the same weakness through the same `store.load`. `plan.md` §Risks requires leaving it, and the bug is already open at `ready` with its own criteria.
- **Cross-answer check:** none. This execution edited one document, `docs/process/using-recall.md`, and it carries no claim citing a stakeholder answer — no `[src: <ITEM>/Q-nnn]` appears in it before or after. The new §"Doing a review" cites acceptance criteria (`WI-0002` AC3, AC5–AC7, AC9, AC11–AC13) and ADRs, and those criteria are where the stakeholder's answers were already propagated by `answer-questions`. Nothing of theirs was paraphrased, re-cited or overtaken here. `lint-answers --changed-since main` → 0 errors.
- **Questions raised:** none — every decision this execution met was either made by `plan.md`/`ADR-0006` already, or was inside the plan's latitude and is recorded above.
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
  - `python3 -m unittest discover -s tests -t . -q` → 0, run after each of the six steps; on the branch head `Ran 32 tests ... OK`
  - `python3 -m compileall -q recall tests` → 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 7 commit(s) on main..wi/WI-0002 name WI-0002`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 6 item(s), 9 document(s) — 0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0, `checked 5 consumed human answer(s)`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → 0, board already current
  - fourteen mutation runs of the test command, each reverted with `git checkout -- recall tests` — outcomes tabulated in `impl-report.md`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` on `76b4aff`+report commit → `Ran 32 tests ... OK`, exit 0)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests` → exit 0; it is a syntax check and not a style linter, which `ADR-0003` states plainly)
  - `workspace-valid` → **pass** (`validate-workspace` → `checked 6 item(s), 9 document(s)`, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (thirteen named tests in `tests/test_review.py`, one per criterion; each proved to fail under a mutation of the behaviour it covers — the table is in `impl-report.md` §Acceptance criteria evidence)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → `all 7 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0)
  - `no-unplanned-scope` → **pass** (advisory; six source and documentation files, each hunk traceable to a numbered plan step. The remaining files in `main..wi/WI-0002` are `tracker/board.md`, `history.md`, `item.md` and `journal.md`, all written by `transition` and `board-gen` rather than by hand)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → 0 errors, 0 warnings, over the one changed document)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → 0 errors, 0 warnings. Two citations were corrected before this passed: `y`/`n` was cited to `ADR-0002`, which fixes two-way grading but not the tokens — recited to `plan.md` — and the damaged-deck paragraph now cites `WI-0002 AC7` alongside WI-0001's)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` — created
  - `recall/cli.py`, `recall/deck.py`, `recall/store.py` — extended
  - `tests/support.py` — extended; `tests/test_review.py` — created
  - `docs/process/using-recall.md` — v2 → v3, with a change-log row
  - branch `wi/WI-0002`, seven commits, `d2ca976..HEAD`
- **Status:** `in-progress` → `verifying`
- **Result:** `recall review` is built and all thirteen criteria have a test that was shown to fail when its behaviour is removed. Three deviations from the plan are recorded, all "how" and each reversible in one line. `BUG-0001` is untouched by design and a passing AC7 is not evidence about it; the schedule is still the placeholder WI-0003 replaces, and the documentation says so.

## 2026-08-30T03:00:03Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next` as the highest-ranked runnable item (priority rank 2); BUG-0001 and WI-0004 runnable at rank 3, WI-0003 blocked on `depends-on: WI-0002`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the thirteen criteria, read **before** the implementation report, so that what would settle each was derived from the criterion rather than from what was built
  - `docs/process/using-recall.md` v3 §"Doing a review" — read before any command was run, because AC3, AC5 and AC6 name their expected output by reference to the tool's own documentation. It is the standard those three were judged against: `y` and `n`, and `Nothing is due today. Come back tomorrow.`
  - `tracker/items/WI-0002/artifacts/plan.md` — the interface list and `## Assumptions`, for step 6's read of the diff
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria; used to know what was claimed, and cited as evidence for nothing
  - `tracker/items/WI-0002/history.md`, `tracker/project.yaml`
  - the code at branch head **`b51c502cb5eb5aec7b52a96468e43cb661ecaec8`** on `wi/WI-0002`, and `git diff main..HEAD` over `recall/`, `tests/` and `docs/`
- **Decisions:**
  - **All thirteen criteria pass, and all thirteen boxes are ticked.** Every verdict rests on a command this skill ran against the branch head, driving the real `recall` executable from a scratch home with input on stdin — the invocation form the criteria are written against. The suite was run too, but no verdict rests on it and none rests on `impl-report.md`.
  - **No send-back and no bug item.** Nothing failed against this item's criteria, and nothing was found in behaviour delivered elsewhere.
  - **`BUG-0001` was deliberately not re-filed.** `review` inherits the same weakness with non-content filesystem errors through the same `store.load`, but the bug is already open at `ready` with its own criteria, and duplicating it would split its verification. `plan.md` §Risks requires leaving it. Recorded so that a reader does not mistake a passing AC7 for evidence about it.
  - **The reveal prompt's missing newline was investigated rather than accepted from the report.** Piped, the answer lands on the prompt's line. Run under a pty with a typing delay — the medium `ADR-0001` fixes — the transcript reads correctly, because the person's Return supplies the newline. Not a defect: no criterion covers line layout and AC1's ordering holds either way. Evidence is quoted in the report.
  - **`a-criterion-about-criteria-is-read` is vacuous on this item** — no criterion of WI-0002 has other criteria as its subject; all thirteen are stated over observable behaviour. Rather than record that and move on, the non-intersection it exists to catch was stated in those words and checked by hand: *nothing executable exercises WI-0001's criteria and a graded deck together*, because every WI-0001 test builds its deck with `add`, which never writes `grade`. A covering test was **waived by name** — it belongs to no criterion of this item — and WI-0001 AC1, AC2 and AC3 were instead run by hand against a deck a sitting had written. All three hold.
  - **Two mutation results were kept rather than smoothed over.** The AC1 mutation "print the answer before the reveal read" is caught by AC2's test and *not* by AC1's own; AC1's test is sensitive to the other AC1 mutation. Nothing is unverified, but it is recorded so a future change that dropped AC2's test would not silently uncover that path.
  - **No criterion was judged ambiguous.** Every one named either an exact invocation or a documented message, and the documentation existed.
- **Questions raised:** none — no criterion required a reading the record did not already settle.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 32 tests in 3.423s ... OK` (run by this skill, on the branch head)
  - `python3 -m compileall -q recall tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 6 item(s), 9 document(s)`, 0 errors
  - AC1: three due cards, `recall review` on a six-line here-document → 0; question/answer indices and occurrence counts measured on the captured stdout
  - AC2: `recall review < /dev/null` with one due card → 0; `grep -c` question=1, answer=0
  - AC3: two due cards, input `↵ maybe y ↵ y` → 0; two grade prompts before the second card, one occurrence of the first question, `grade: right` read back out of the deck file
  - AC3 negative additions by this skill: response `yes` (a superstring of `y`) → rejected; a bare empty line → rejected; `  Y  ` → stored `right`
  - AC4: cards at today and today+7 → 0; `grep -c due-later` = 0
  - AC5: all cards at today+7 → 0; `grep -cF` against the documented sentence = 1
  - AC6: empty home, deck and parent absent → 0; same sentence; `find <home> -mindepth 1` returned nothing at all afterwards
  - AC7: seven damaged decks in turn → exit 3 each; deck path on stderr; stdout empty; `sha256sum` identical before and after each
  - AC8: grade in one process, then `recall review` in a second, same day → `grep -c survivor-q` = 0
  - AC9: input for the first card only → 0, stderr empty, `grep -c Traceback` = 0; second run presents the second card and not the first
  - AC10: `recall list` before and after a sitting, `diff` identical; repeated through the re-prompt path, identical again
  - AC11: 25 due cards → 25 distinct questions, 25 of 25 graded in the file; then 60 due cards → 60 of 60, exit 0
  - AC12: `recall add` then `recall review` as a second process → the added question presented
  - AC13: one card at today−7 → presented, exit 0
  - WI-0001 cross-check on a graded deck: `recall list` → both sides verbatim in order, exit 0; `recall add` → exit 0, three cards in order; blank `--question` → refused, `sha256` unchanged; a fresh `add` still writes four keys and no `grade`
  - a pty run of a sitting with a typing delay, to see the transcript as a person does
  - fourteen source mutations, each followed by the test command and `git checkout -- recall tests`; outcomes tabulated in `verify-report.md`
- **Gates:**
  - `tests-pass` → **pass** (run by this skill on `b51c502`: `Ran 32 tests ... OK`, exit 0)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0. It is a syntax check and not a style linter — `ADR-0003` says so — and `verify-report.md` §"Not verified" says what that leaves unchecked)
  - `workspace-valid` → **pass** (`validate-workspace` → 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (thirteen rows in `verify-report.md` §Criteria, each with the command this skill ran and its quoted output; no row cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (every error, empty-input and boundary case triggered: EOF at both reads, three unrecognised responses of which two are this skill's additions, nothing-due with a deck and without one, seven unreadable decks, the today−7 / today / today+7 boundaries, and 60 cards above AC11's witness size)
  - `a-criterion-about-criteria-is-read` → **pass, vacuously** (no criterion of WI-0002 has other criteria as its subject; stated as such rather than claimed as work done, with the WI-0001 non-intersection stated in the gate's own words, a covering test waived by name, and the cross-check run by hand instead)
  - `tests-would-fail-without-the-change` → **pass** (advisory; this skill's own fourteen-mutation sweep, derived from the criteria rather than from `impl-report.md`, with the one sensitivity weakness recorded rather than omitted)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — created, `Verified-commit: b51c502cb5eb5aec7b52a96468e43cb661ecaec8`
  - `tracker/items/WI-0002/item.md` — all thirteen criteria ticked
  - bug items filed: none
- **Status:** `verifying` → `in-review`
- **Result:** `recall review` meets all thirteen of its acceptance criteria, each demonstrated by a command this skill ran and quoted. No defects, no send-back, no bug filed. `BUG-0001` remains untouched and a passing AC7 is not evidence about it; the schedule is still the documented placeholder for WI-0003.

## 2026-08-30T03:04:49Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next` as the highest-ranked runnable item (priority rank 2); BUG-0001 and WI-0004 runnable at rank 3, WI-0003 blocked on `depends-on: WI-0002`
- **Inputs read:**
  - the **diff** `main..wi/WI-0002` (`d2ca976..f15d122`), hunk by hunk, over `recall/cli.py`, `recall/deck.py`, `recall/store.py`, `tests/support.py`, `tests/test_review.py` and `docs/process/using-recall.md` — the change itself, not the reports about it
  - `tracker/items/WI-0002/item.md` — the thirteen criteria and their tick state
  - `tracker/items/WI-0002/artifacts/verify-report.md` in full, including `## Not verified, and why`
  - `tracker/items/WI-0002/artifacts/impl-report.md` in full, including `## What I did not do`
  - `tracker/items/WI-0002/artifacts/plan.md` — `## Approach`, the interface list, all five `## Assumptions`
  - `tracker/items/WI-0002/journal.md` in full — ten entries — and `history.md`
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`
  - `docs/architecture/adr/ADR-0006` in full, and the cited sections of `ADR-0001`, `ADR-0002`, `ADR-0004`
  - `docs/process/using-recall.md` v3, and — for the D12 audit — each thing its new claims cite
- **Decisions:**
  - **Rejected, on D12.** One claim in `docs/process/using-recall.md` is not supported by what it cites and is not true of the code: *"Your answers are recorded against the cards in the meantime, so nothing you review now has to be reviewed again to catch the scheduler up [src: ADR-0006]."* `ADR-0006`'s only sentence about WI-0003 is that it *"inherits a field it does not have to add"* — a statement about the next author's work, not about a past answer carrying forward. `record_answer` leaves `rung` untouched and nothing reads `grade` back into scheduling, so a card graded right today earns no ladder progress and never will. `plan.md` §Assumptions arranges that deliberately; the documentation tells the reader the opposite. Recorded as **F1** with the fix spelled out: one paragraph, no code change, no criterion affected.
  - **The audit was done from the citations, not from the prose**, which is the only way it could have failed. Eleven absolute claims were listed and the cited thing opened for each; ten are supported, one is not. `lint-claims` passed and is not evidence here — it proves a citation **resolves**, not that it **supports** the sentence, and this is precisely the gap between the two.
  - **F2 accepted rather than blocking.** A `#:` block in `recall/cli.py` describing the prompts — carrying AC1's *"neither may carry the card's text"* guard — is stranded above `RIGHT_RESPONSE`/`WRONG_RESPONSE`, and the prompts have no comment. The guard is not lost: it is restated in `_read_grade`'s docstring and in `plan.md` §Approach, and `test_due_cards_are_presented_one_at_a_time` fails if a prompt ever echoes a question side. Written into the item's `## Notes`, and worth fixing alongside F1 since that file is already open.
  - **F3 is an observation, not a finding.** `Card.grade: str = None` annotates as `str` and defaults to `None`. No type checker runs — `commands.lint` is `compileall`, a syntax check, which `ADR-0003` states plainly — so nothing is broken or misreported.
  - **Five accepted gaps written into the item's `## Notes`**, not left in a report: F2; that `BUG-0001` is untouched and a passing AC7 is not evidence about it; the unexercised midnight boundary; and that deck order is unconstrained by any criterion. A gap recorded only in a verification report stops being read the moment an item closes.
  - **`verify` was right not to re-file `BUG-0001`.** It is already open at `ready`; a duplicate would split its verification.
  - **Nothing was merged.** The trial merge was run and is clean, and the branch is left intact for the next `implement` execution.
  - **Nothing contradicts an ADR**, so no question was filed. Every `ADR-nnnn section n` citation in the new code says what the ADR says; I opened each.
- **Cross-answer check:** none consumed by this execution — it answered no question and recorded no new human answer, so there is no reply to check against a prior one. The two answers this item rests on, `WI-0002/Q-001` (no cap) and `WI-0002/Q-002` (due the day added), were consumed by `answer-questions` at 02:32:20Z and were not re-read, re-quoted or edited here; `lint-answers --context work-item --changed-since main` → `checked 5 consumed human answer(s)`, 0 errors. Note for the record: F1 is a claim about **`ADR-0006`**, an architect's decision, not about anything the stakeholder said — so it is an ordinary documentation defect and not the ADR-0008 case that would have to go back to them.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → 0, *"verified at b51c502c; wi/WI-0002 has moved to f15d122e but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 9 commit(s) on main..wi/WI-0002 name WI-0002`
  - `git rev-parse main` → `d2ca9768…` (before the trial)
  - `git worktree add --detach <trial> main` → 0; `git -C <trial> merge --no-ff wi/WI-0002` → merged cleanly, trial head `294cf78`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → 0, `Ran 32 tests in 3.409s ... OK`
  - `git worktree remove --force <trial>` → 0; `git rev-parse main` → `d2ca9768…`, unchanged
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 6 item(s), 9 document(s)`
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → 0
  - `grep` over `recall/` for any code relating `grade` to `rung` → no matches, which is the evidence behind F1
- **Gates:**
  - `definition-of-done` → **FAIL** (walked D1–D12 individually; the per-criterion table is in `review.md` §"Definition of Done". D1–D8, D10, D11 pass; **D12 fails on F1**; D9 not reached, because the review rejects and nothing was merged)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the only commit after the verified `b51c502` is `f15d122`, which touches `tracker/` only. Compared mechanically rather than judged by how the last commit looked)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 9 commits)
  - `tests-pass-on-the-merge-result` → **pass** (run inside the detached trial worktree on merge result `294cf78`, not on the branch: `Ran 32 tests ... OK`, exit 0. The merge itself was then discarded, and `main` was confirmed unmoved)
  - `workspace-valid` → **pass** (0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** (answered all four from the tracker, docs and `git log` alone: *what was built and why* — `plan.md` §Problem and the nine branch commits; *which skill decided what* — `ADR-0006` is `plan`'s, the `y`/`n` tokens are `plan`'s and `implement` records correcting itself when it first derived `r`/`w`, the deck-order and placeholder choices are `plan.md` §Assumptions; *what questions arose and how they resolved* — `Q-001` and `Q-002`, answered by the stakeholder and propagated into AC11, AC12, `refinement-qa.md`, `ADR-0002` v2 and `vision.md` v3; *what verification found* — thirteen criteria demonstrated by command, a fourteen-mutation sensitivity sweep, and one recorded sensitivity weakness on AC1's own test)
  - `claims-are-sourced` → **pass as a program, and it is not the D12 answer.** Scope, quoted from the gate's own output: *"checked absolute claims: 1 document(s) in 1 path(s) differ from main (d2ca976) under docs; citations: every markdown file in the workspace"* — a scope that could have found something, and it found no unresolvable citation. F1's citation resolves; it simply does not support its sentence, which only a reader can determine
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main`, scope quoted: *"claim window: 1 path(s) differ from main (d2ca976) under docs"*, `checked 5 consumed human answer(s)`, 0 errors)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` → *"WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."* `engagement-state EP-001` reports **active**, still in flight: BUG-0001, WI-0002, WI-0003, WI-0004 — so no engagement ended here and no sign-off was due)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — created, with `## What I examined` first and the D12 claims audit table
  - `tracker/items/WI-0002/item.md` — `## Notes` extended with the four accepted gaps
  - merge commit: **none** — the review rejects; `wi/WI-0002` is left intact and unmerged
  - bug items filed: none
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected on D12. The code is sound — all thirteen criteria hold, the trial merge is clean and the record reconstructs — but `docs/process/using-recall.md` tells a person their answers are being banked towards the schedule, and the code deliberately banks nothing: `record_answer` leaves `rung` untouched and no code reads `grade` back. The fix is one paragraph plus a version bump, and F2's stranded comment is worth taking in the same pass.

## 2026-08-30T03:07:42Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` after `review-close` rejected the item on D12 (history row 2026-08-30T03:04:49Z); dispatched by `next` as the highest-ranked runnable item. No status change accompanies this entry — the item was already at `in-progress`, so this execution opens in the record rather than through a transition.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — all thirteen criteria and `## Notes`, including the four gaps `review-close` wrote there
  - `tracker/items/WI-0002/history.md` — nine rows; the last is the send-back this execution answers
  - `tracker/items/WI-0002/artifacts/review.md` — read **first**, per the procedure's step 1, because the last row is a send-back. F1 blocking, F2 accepted, F3 observation
  - `tracker/items/WI-0002/artifacts/plan.md` — `## Approach`, the interface list, all five `## Assumptions`, and step 6 which owns the document F1 is about
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, both propagated before the item reached `ready`; nothing has moved since
  - `docs/architecture/adr/ADR-0006-*.md` in full — the citation F1 says does not support the sentence
  - `docs/process/using-recall.md` v3 — the whole file, and §"What this version does not do yet" line by line
  - `recall/deck.py` `record_answer`, and `grep -rn grade recall/` — to establish for myself what the code does, rather than taking `review.md`'s word for it
  - `recall/cli.py:27–60` — the two fused `#:` blocks F2 names
  - `tracker/project.yaml` — test and lint commands, branch prefix, commit subject
- **Decisions:**
  - **Scope is F1 and F2, and nothing else.** The review says in terms that the next execution should not re-do the rest: all thirteen criteria hold and were independently demonstrated at `b51c502`. F3 is an observation the review marked no-action, and it stays that way — a type annotation with no type checker behind it is not this item's work.
  - **I confirmed F1 against the code before accepting it.** `deck.record_answer` is `dataclasses.replace(card, grade=grade, due=today + timedelta(days=1))` — `rung` untouched — and `grep -rn grade recall/` finds `grade` written, validated and round-tripped but never read back into scheduling. The documented sentence promises a person something no code does. The finding is real, not inherited.
  - **Nothing in `recall/` changes for F1.** The plan's third assumption arranged the placeholder deliberately; the document is what is wrong, so the document is what is fixed.
- **Cross-answer check:** none. `grep -n "Q-00" docs/process/using-recall.md` returns nothing — no claim in the document this execution edits carries a `[src: <ITEM>/Q-nnn]` citation, so no sentence of the stakeholder's is in the blast radius, and no later answer of theirs has overtaken anything (`ADR-0008` §4; procedure step 6a).
- **Questions raised:** none
- **Commands:**
  - `git log --oneline main..wi/WI-0002` → 10 commits, exit 0; branch head `d479eac`, matching the last history row
  - `git status --short` → empty, exit 0; no uncommitted work to reconcile
  - `grep -rn "grade" recall/` → exit 0; `grade` is stored and validated, never read into scheduling
  - `grep -n "Q-00" docs/process/using-recall.md` → exit 1 (no match), which is the cross-answer check above
- **Gates:**
  - `tests-pass` → **skipped** (not yet run; this entry opens the execution, no change has been made)
  - `lint-clean` → **skipped** (same)
  - `workspace-valid` → **skipped** (same)
  - `every-criterion-has-a-test` → **skipped** (same)
  - `commits-reference-the-item` → **skipped** (same)
  - `no-unplanned-scope` → **skipped** (same; advisory)
  - `cross-answer-consistency` → **skipped** (same)
  - `claims-are-sourced` → **skipped** (same)
- **Artifacts:** none yet. Branch `wi/WI-0002` already exists at `d479eac` and is checked out; no new commit from this entry.
- **Status:** `in-progress` → `in-progress` (no transition; the item was already here)
- **Result:** Reconciled with the branch before touching it: ten commits present, working tree clean, and the branch head is the commit the last history row names. This execution answers the review's F1 — one false claim in `docs/process/using-recall.md` — and takes F2 in the same pass. The thirteen criteria are not being re-done.

## 2026-08-30T03:11:59Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` after `review-close`'s D12 rejection; this entry closes the execution the entry above opened.
- **Inputs read:**
  - `tracker/items/WI-0002/artifacts/review.md` — findings F1 (blocking), F2 (accepted), F3 (observation), and `## Accepted gaps`
  - `tracker/items/WI-0002/artifacts/plan.md` — step 6, which owns the document, and `## Assumptions`, which arranged the placeholder F1 misdescribes
  - `docs/architecture/adr/ADR-0006-*.md` in full, to see what it does and does not say about WI-0003
  - `docs/process/using-recall.md` v3 in full
  - `recall/deck.py` (`record_answer`, `new_card`, `FIRST_RUNG`), `recall/cli.py` (the constants and `cmd_review`), and `grep -rn "rung|grade" recall/`
- **Decisions:**
  - **F1 is fixed in prose, not in code.** The plan's third assumption chose deliberately that a sitting leaves no scheduling state, so that WI-0003 has nothing to undo. Making the sentence true by making the code bank the answer would be building WI-0003's arithmetic inside WI-0002 — the item excludes it in terms. The document was the thing that was wrong.
  - **The replacement cites what supports it.** `[src: ADR-0006]` stays only on the half it does support — that the answer is written into the deck file against the card. The half about the schedule now cites `recall/deck.py:92` (`record_answer` leaves the ladder position alone) and `recall/deck.py:73` (`rung=FIRST_RUNG`, the only place outside `store`'s round-trip where `rung` is ever set). I established both by reading the code, not from `review.md`.
  - **I said the consequence out loud rather than only the mechanism.** "Every card is still on the bottom rung `recall add` put it on, and that is where it will start climbing from when the ladder lands — the ones you got right today included." The mechanism alone would leave a person to work out for themselves that today's effort earns nothing, which is the thing the old sentence got wrong.
  - **F2 taken in the same pass, as the review suggested**, because the file was already open and the guard is AC1's. Comment only.
  - **F3 left alone.** The review marked it no-action and the project runs no type checker (`ADR-0003`). Fixing an annotation nothing reads would be tidying, which is the second way this skill goes wrong.
  - **The thirteen criteria were re-run, not re-demonstrated.** `verify` established them at `b51c502` and `review-close` confirmed the record; re-deriving them here would be work nobody asked for and would not be independent anyway. I ran the suite and one mutation instead — see the gate evidence.
- **Cross-answer check:** none. `grep -n "Q-00" docs/process/using-recall.md` returns no match: the document carries no claim cited to a stakeholder answer, so the sentence rewritten this execution is not one of theirs and `ADR-0008` §3's third row does not arise. No stakeholder answer has been given since the two on this item were consumed at `2026-08-30T02:32:20Z`, so nothing of theirs has overtaken anything. `lint-answers --changed-since main` agrees over a non-degenerate window.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → `Ran 32 tests in 3.400s` / `OK`, exit 0 (on head `ef7a00d`, after both code commits)
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 6 item(s), 9 document(s)`, `0 errors, 0 warnings`, exit 0 (re-run after the report commit `577630e`)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → `all 13 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → `claim window: 1 path(s) differ from main (d2ca976) under docs`, `checked 5 consumed human answer(s)`, `0 errors, 0 warnings`, exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --context work-item` → `1 document(s) in 1 path(s) differ from main`, `0 errors, 0 warnings`, exit 0
  - `git diff d479eac..HEAD` → four hunks in two files, exit 0
  - AC1 mutation: a second `print(card.question)` added to `cmd_review`, suite re-run → `FAILED (failures=2)`, exit 1, with `test_due_cards_are_presented_one_at_a_time` reporting *"q-one must appear exactly once in the run's output"*; source restored from a copy, suite re-run → `OK`, exit 0, and `git status --short` shows `recall/cli.py` unmodified
- **Gates:**
  - `tests-pass` → **pass** (`Ran 32 tests ... OK`, exit 0, on head after the last change)
  - `lint-clean` → **pass** (`compileall -q recall tests`, exit 0)
  - `workspace-valid` → **pass** (`0 errors, 0 warnings`)
  - `every-criterion-has-a-test` → **pass** (the thirteen-row table in `impl-report.md`, one test per criterion, all green at head; plus AC1's mutation re-applied and confirmed failing this execution, because AC1's guard is the one thing F2's comment move could have disturbed)
  - `commits-reference-the-item` → **pass** (`all 13 commit(s) ... name WI-0002`, exit 0)
  - `no-unplanned-scope` → **pass** (advisory; the diff since the rejection is the version bump, the F1 paragraph, the F1 change-log row and F2's comment move — every hunk traces to a named review finding)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main`, exit 0, over a window that saw the one changed document)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --context work-item`, exit 0). Worth recording that this gate **also passed over F1's false claim**: it proves a citation resolves, not that it supports its sentence, which is why D12 caught what it caught.
- **Artifacts:**
  - `docs/process/using-recall.md` v3 → v4, with a change-log row — commit `6cd5fc1`
  - `recall/cli.py`, comment only — commit `ef7a00d`
  - `tracker/items/WI-0002/artifacts/impl-report.md`, rewritten to cover both executions — commit `577630e`
  - Branch `wi/WI-0002`, head `577630e`; this execution's range is `d479eac..577630e`, three commits
- **Status:** `in-progress` → `verifying`
- **Result:** `review-close`'s rejection is answered. The documented claim that a reviewed answer carries forward into the schedule is gone, replaced by what the code does — the answer is stored, nothing reads it back, and every card is still on the bottom rung — and F2's guard now sits on the prompts it governs. No behaviour changed, the suite is green at head, and all seven hard gates pass. What `verify` needs to satisfy itself about is the changed paragraph in `docs/process/using-recall.md`; the thirteen criteria it already demonstrated at `b51c502` are untouched and were re-run, not re-derived.

## 2026-08-30T03:19:47Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** `verifying`, entered by `implement`'s second execution answering `review-close`'s D12 rejection; dispatched by `next` as the highest-ranked runnable item.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the thirteen criteria, read **before** the implementation report, and `## Notes` including the four gaps `review-close` recorded
  - `tracker/items/WI-0002/history.md` — ten rows; the send-back and the return are rows 9 and 10
  - `tracker/items/WI-0002/artifacts/impl-report.md` — both executions' sections, read as the claim to check rather than as evidence
  - `tracker/items/WI-0002/artifacts/review.md` — findings F1, F2, F3 and the five accepted gaps, to know what the send-back was for
  - `tracker/items/WI-0002/artifacts/plan.md` — `## Approach`, the interface list, `## Assumptions`
  - `docs/process/using-recall.md` v4 — read at head **before any command was run**, because AC3, AC5 and AC6 are decided by reading it and it is what changed
  - `docs/architecture/adr/ADR-0006-*.md`, and `recall/deck.py` / `recall/cli.py` / `recall/store.py` at the citations the corrected paragraph makes
  - **The branch commit verified: `c50694d40bb4e7074b9a768494571656309ecfc6`**, the head of `wi/WI-0002`
- **Decisions:**
  - **Every criterion was re-demonstrated from scratch rather than carried over from the first verification.** Three of them — AC3, AC5, AC6 — name their expected output by reference to the tool's own documentation, and the documentation is exactly what this send-back changed. Reusing evidence gathered against v3 of a document that is now v4 would have been checking a criterion against a text that no longer exists. The other ten were re-run for the same reason the first verification ran them: they cost little and a carried-over pass is not an independent check.
  - **No verdict cites `impl-report.md`.** Each of the thirteen rows in the report is a command this execution issued against the real executable from a scratch home, with the output quoted.
  - **`a-criterion-about-criteria-is-read` is vacuous on this item, and is recorded as vacuous.** All thirteen criteria were read for the shape; none has other criteria as its subject. Rather than stop there, the non-intersection the gate exists to catch was stated in its own words — nothing executable exercises WI-0001's criteria and a *graded* deck together, because every WI-0001 test builds its deck with `recall add`, which never writes a `grade`. A covering test was **waived by name** (`tests/test_add.py`, `tests/test_list.py`) and WI-0001 AC1, AC2, AC3 and AC9 were run by hand against a deck holding `right` and `wrong` grades and a card at `rung: 2`. All four hold, and the grades and rungs survived every one.
  - **The corrected paragraph was audited from its citations, not from its prose** — the method that caught F1 in the first place. Four of its five claims are supported outright; the fifth carries a qualification, recorded as observation **O1**.
  - **O1 is an observation, not a defect, and not a send-back.** *"Every card is still on the bottom rung `recall add` put it on"* is true of every card the tool makes and defeasible by hand-editing the deck file, which `ADR-0004` contemplates. I did not send the item back for it: no acceptance criterion of this item is about the document's prose, so a send-back has no criterion to name; the sentence's operative promise holds for a hand-edited card too; and the person who set a rung by hand is not the person it could mislead. D12 belongs to `review-close`, so the observation is put in front of it in full, with the one-word fix named, rather than decided here.
  - **No bug item filed.** Nothing found belongs to behaviour another item delivered. `BUG-0001` remains untouched and was deliberately not exercised — AC7 is about deck *content* and a passing AC7 is not evidence about it.
  - **A cap probe above the criterion's witness.** AC11 names twenty-five cards, and an implementation capping at exactly twenty-five would pass it as written, so a sixty-card deck was run as well.
  - **A card was planted at `rung: 2`** in the AC10 deck so that "the ladder position does not move" could fail visibly rather than being unobservable at the default of 0.
- **Questions raised:** none. No criterion was ambiguous: the three that defer to the documentation were settled by reading it at this head first, and the reading it gives is unambiguous.
- **Commands:**
  - `git rev-parse HEAD` → `c50694d40bb4e7074b9a768494571656309ecfc6`; `git status --short` → clean
  - `python3 -m unittest discover -s tests -t . -q` → `Ran 32 tests in 3.429s` / `OK`, exit 0
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 6 item(s), 9 document(s)`, `0 errors, 0 warnings`, exit 0
  - Thirteen criterion checks driving `bin/recall` from scratch homes under `/tmp/vfy/`, each with its output quoted in `verify-report.md` §Criteria — AC1 (three due cards, index arithmetic in Python), AC2 (`review < /dev/null`), AC3 (`maybe` then `y`), AC4 (today vs today+7), AC5 (all future), AC6 (empty home, `find` before and after), AC7 (eight damaged decks with `sha256sum` either side), AC8 and AC9 (two processes each), AC10 (`recall list` diffed before and after), AC11 (25 cards, then 60), AC12 (`add` then `review`), AC13 (today−7)
  - Three extra grade-prompt negatives: `yes` → rejected; a bare empty line → rejected; `  Y  ` → accepted and stored as `right`
  - Cross-item read: `recall add` / `recall list` / a blank-side refusal / a duplicate question, all against the graded deck at `/tmp/vfy/h10`; exits 0, 0, 2, 0
  - `git diff b51c502..c50694d -- recall tests` → one file, four lines, comment only
  - `grep -rn "rung" recall/`, `grep -rn "\.grade" recall/` → the reads and writes behind the corrected paragraph
  - Sixteen mutations via two driver scripts, each restoring the source from the in-memory original → every criterion has a failing test; suite `OK` and `git status --short` clean afterwards. Three mutations reported `MUTATION DID NOT APPLY (0 matches)` on a wrong source string, were rewritten against the real text of `due_positions`, and re-run
- **Gates:**
  - `tests-pass` → **pass** (`Ran 32 tests ... OK`, exit 0, run by this skill on `c50694d`)
  - `lint-clean` → **pass** (`compileall -q recall tests`, exit 0)
  - `workspace-valid` → **pass** (`0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (thirteen rows, each a command this execution ran with its actual output; none cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (eleven conditions triggered: EOF at both reads, eight damaged decks including `"grade": "maybe"` and `"grade": null`, an unrecognised response, a superstring of a recognised one, a bare empty line, case and whitespace, the today−7 / today / today+7 boundaries, an absent deck and directory, a sitting above the witness size, and a card at a non-zero rung)
  - `a-criterion-about-criteria-is-read` → **pass, vacuously and explicitly** (no criterion of this item has criteria as its subject; the non-intersection was stated in the gate's words, a covering test waived by name, and WI-0001's criteria run by hand against a graded deck)
  - `tests-would-fail-without-the-change` → **pass** (advisory; sixteen mutations, table in the report, with the sensitivity weakness that survived it written down rather than smoothed over)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — rewritten for this verification at `c50694d`; the first verification is preserved in git at `f15d122` and pointed to from the verdict
  - `tracker/items/WI-0002/item.md` — all thirteen boxes remain ticked, and each tick is now backed by a command **this** execution ran; none was ticked on carried-over evidence
  - No bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** All thirteen criteria pass, demonstrated independently against `c50694d`. The change the send-back was for is sound: the code diff since the last verification is four lines of comment, and the corrected documentation paragraph is supported by its citations and by the decks this verification produced — a card graded `right` kept `rung: 2`, a card graded `wrong` kept `rung: 0`, and both moved to tomorrow. One observation, **O1**, is put to `review-close` rather than decided here: the sentence *"every card is still on the bottom rung `recall add` put it on"* is defeasible by hand-editing the deck, and the fix if it is read strictly is one word.

## 2026-08-30T03:26:56Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, entered by `verify`'s second execution; dispatched by `next` as the highest-ranked runnable item (priority rank 2; BUG-0001 and WI-0004 runnable at rank 3, WI-0003 not runnable on `depends-on: WI-0002`).
- **Inputs read:**
  - the **diff** `main..wi/WI-0002` (`d2ca976..1d4859a`), hunk by hunk, over `recall/cli.py`, `recall/deck.py`, `recall/store.py`, `tests/support.py`, `tests/test_review.py` and `docs/process/using-recall.md` — the change itself, not the reports about it; and the incremental diff `d479eac..1d4859a`, which is four hunks in two files
  - `tracker/items/WI-0002/item.md` — thirteen criteria, tick state, `## Out of scope`, `## Notes`
  - `tracker/items/WI-0002/journal.md` **in full** — all fourteen entries, end to end, because D5 and `record-is-reconstructible` are certified from it — and `history.md`, whose chain I verified in Python rather than by eye
  - `tracker/items/WI-0002/artifacts/verify-report.md` in full, including `## Not verified, and why` and observation **O1**, which `verify` correctly routed to me rather than deciding
  - `tracker/items/WI-0002/artifacts/impl-report.md` in full, both executions, including `## What I did not do`
  - `tracker/items/WI-0002/artifacts/plan.md` — `## Approach`, the interface list, the AC mapping, all five `## Assumptions`
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, `## Consequences` opened and the named files confirmed
  - `docs/architecture/adr/ADR-0006` in full; `ADR-0002` `## Decision` §1–§7; `ADR-0004` §1–§6; `ADR-0001`'s cited sections
  - `docs/process/using-recall.md` v4, `docs/architecture/overview.md` v2, `docs/product/vision.md` v3 — three documents for the D12 audit, not one; D12 is scoped to the behaviour touched, not to the file with the diff in it
  - `tracker/items/WI-0001/artifacts/review.md` — for the D9 ordering precedent
- **Decisions:**
  - **Accepted, merged, closed `delivered`.** The rejection is answered. The corrected paragraph is supported by both things it cites, and by evidence rather than by reading: a card planted at `rung: 2` and answered **right** was still at `rung: 2`; a card answered **wrong** was still at `rung: 0`; both moved to tomorrow.
  - **The D12 audit was run from the citations again, over twenty-one claims in three documents.** Every one is supported. It was extended past `using-recall.md` deliberately: the first review audited eleven claims in the changed file, and a claim about this item's behaviour can live in a file this item never opened. `overview.md`'s *"since `review`, the only layer that reads standard input"* was settled by `grep -rn "input(\|sys.stdin" recall/ bin/` → exactly one hit.
  - **`vision.md`'s ladder sentence is out of D12's reach, and I did not touch it.** *"the gap to its next review walks the ladder 1, 3, 7, 30 days"* cites `EP-001/Q-003` — the stakeholder's own answer, quoted with a return address. It states the target product, not today's code, and `using-recall.md` is where what is built is stated. `ADR-0008` puts that sentence beyond an ordinary repair, and no repair is needed.
  - **F1 — a real inaccuracy, accepted rather than sent back, with the reason specific.** `record_answer`'s docstring says *"For a wrong answer this already is ADR-0002's rule"*, and `plan.md` says it with *"exactly"*. `ADR-0002` §6 has two clauses — back to the first rung, **and** due one day later — and the placeholder satisfies only the second. The risk is concrete and lands on the next item: WI-0003's author, told the wrong-answer case is already right, adds only the right-answer ladder walk. Not sent back because it breaks no criterion, is not in `docs/` so D12 does not reach it, and lives in the one function `plan.md` names as WI-0003's landing site — a note on the dependency reaches the author, a reworded docstring that WI-0003 deletes does not. Written into `## Notes` as an instruction to WI-0003, not as a lament.
  - **F2 — two stale enumerations, accepted, with the line stated so it can be argued with.** `ADR-0004` §5's *"both subcommands"* and `overview.md`'s *"later, `review`"* both predate the third subcommand. I drew the line at: **a claim whose substance is true but whose incidental enumeration has aged is stale, not false** — a reader of either learns the rule correctly and acts wrongly on neither. That is the same line the first review applied when it rejected: the sentence it rejected would have changed what a person did. I wrote the distinction into `review.md` rather than leaving it as tacit leniency.
  - **F3 — `verify`'s O1, decided.** *"Every card is still on the bottom rung `recall add` put it on"* is supported by `recall/deck.py:73` for the population the paragraph is about, and its operative promise holds even for a hand-edited card. Left as written, with the tightening named in `## Notes`.
  - **D7 passes, and the F2 finding does not overturn it.** D7 asks whether the change invalidated a document. Neither sentence was invalidated — both rules still hold — so they are gaps to record, not updates that were skipped.
  - **The second verification's decision to re-demonstrate all thirteen criteria was the right one**, and I checked it rather than assuming: AC3, AC5 and AC6 name their expected output by reference to the tool's own documentation, and the documentation is precisely what this send-back changed, so carried-over evidence would have been evidence about a text that no longer exists.
  - **No bug item filed and none should be.** F1, F2 and F3 are all about this item's own artifacts, so none is another item's defect; and none breaks an acceptance criterion, so none is a send-back. `BUG-0001` stays untouched and a passing AC7 is still not evidence about it.
  - **Nothing contradicts an ADR**, so no question was filed.
  - **Closed before merging**, per the procedure: `commits-reference-the-item` reads `main..branch`, which merging empties, so a close after a merge would be refused by the gate that was its own precondition.
- **Cross-answer check:** none consumed. This execution answered no question and recorded no new human answer, so there is no reply to check against a prior one. The two answers this item rests on — `WI-0002/Q-001` (no cap) and `WI-0002/Q-002` (due the day added) — were consumed by `answer-questions` at 02:32:20Z and were neither re-read into a decision nor edited here. One thing worth recording because it is the `ADR-0008` shape and I checked it rather than assuming: `vision.md`'s ladder sentence cites `EP-001/Q-003`, a stakeholder answer, and this item delivers a placeholder that does not walk the ladder — but the sentence states the target product and `using-recall.md` now states plainly what is built, so the two coexist and no repair of theirs was made or needed. `lint-answers --context work-item --changed-since main` → `claim window: 1 path(s) differ from main (d2ca976) under docs`, `checked 5 consumed human answer(s)`, 0 errors.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → 0, *"verified at c50694d4; wi/WI-0002 has moved to 1d4859a4 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*; cross-checked with `git diff --name-only c50694d..HEAD` → five paths, every one under `tracker/`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 15 commit(s) on main..wi/WI-0002 name WI-0002`
  - `git rev-parse main` → `d2ca97680145e7ce906319994582d81e8e1d7ecf` (before the trial)
  - `git worktree add --detach /tmp/wi2-trial main` → 0; `git -C /tmp/wi2-trial merge --no-ff wi/WI-0002` → clean, trial head `24628a12bbf92d0346a359848cd78dc7443af606`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → 0, `Ran 32 tests in 3.471s` / `OK`
  - `git worktree remove --force /tmp/wi2-trial` → 0; `git rev-parse main` → `d2ca9768…`, unchanged; `git worktree list` → one entry, no leftover
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 6 item(s), 9 document(s)`
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → **active**; still in flight: BUG-0001, WI-0002, WI-0003, WI-0004
  - a Python walk of `history.md`'s eleven rows, checking each row's `from` against the previous row's `to`
  - `grep -rn "input(\|sys.stdin" recall/ bin/` → one hit; `grep -rn "rung" recall/`; `grep -rn "already is ADR-0002\|real rule" docs/ recall/ plan.md` → the two sites behind F1, neither under `docs/`
- **Gates:**
  - `definition-of-done` → **pass** (walked D1–D12 individually; the per-criterion table with its own evidence is `review.md` §"Definition of Done". All twelve pass; D9's evidence is the trial merge and the ordering, with the real merge immediately after this close)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0, and the changed-path list checked by hand rather than taking the summary's word for it)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 15 commits)
  - `tests-pass-on-the-merge-result` → **pass** (run inside the detached trial worktree on merge result `24628a1`, not on the branch: `Ran 32 tests ... OK`, exit 0; the trial was then discarded and `main` confirmed unmoved)
  - `workspace-valid` → **pass** (`validate-workspace .` → 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass**, answered from the tracker, docs and `git log` alone: *what was built and why* — `plan.md` §Problem and fifteen branch commits; *which skill decided what* — `ADR-0006` and the `y`/`n` tokens are `plan`'s, `implement` records correcting itself when it first derived `r`/`w`, deck order and the placeholder are `plan.md` §Assumptions, and the D12 rejection and its answer are two `review-close` and two `implement` entries; *what questions arose and how they resolved* — `Q-001` and `Q-002`, answered by the stakeholder and propagated into AC11, AC12, `refinement-qa.md`, `ADR-0002` v2 and `vision.md` v3; *what verification found* — two verifications, the second re-demonstrating all thirteen criteria at `c50694d` with a sixteen-mutation sweep and one observation routed to me. The three journal entries with no history row of their own each state why they have none
  - `claims-are-sourced` → **pass as a program, and it is not the D12 answer.** Scope, quoted from its own output: *"checked absolute claims: 1 document(s) in 1 path(s) differ from main (d2ca976) under docs; citations: every markdown file in the workspace"* — a scope that could have found something. It found no unresolvable citation. It passed over the false claim last time too, because it proves a citation **resolves**, not that it **supports**; the twenty-one-row audit in `review.md` is the half only a reader can do
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main`; scope quoted: *"claim window: 1 path(s) differ from main (d2ca976) under docs"*, `checked 5 consumed human answer(s)`, 0 errors)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` → *"WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."* `engagement-state EP-001` reports **active** — BUG-0001, WI-0003 and WI-0004 are still in flight — so no engagement ended here and no sign-off was due. Asked the program rather than reading the board)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — rewritten for this review, `## What I examined` first, with the twenty-one-row D12 audit; the first review's text is preserved at `git show d479eac:tracker/items/WI-0002/artifacts/review.md` and is pointed to from the verdict
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`; `## Notes` extended with F1, F2 and F3, the first of them written as an instruction to WI-0003
  - merge commit: recorded in the follow-up entry, since the merge is performed immediately after this close
  - bug items filed: none
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is done and delivered. `recall review` presents every card due today or earlier, one at a time, records right or wrong against each as it goes, keeps what was answered when a sitting is abandoned, and refuses a damaged deck the way `add` and `list` do. The item took a rejection on D12 and came back with it fixed: the documentation now says the answers are stored and that nothing reads them back, which is what the code does. Three findings are accepted and recorded in `## Notes` — the one that matters is F1, which tells WI-0003's author that the wrong-answer case is **not** already ADR-0002's rule and that the rung reset is theirs to add.

## 2026-08-30T03:27:30Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** not dispatched; this entry records the merge the close above promised, appended rather than folded into it because the merge necessarily happens after the close (`commits-reference-the-item` reads `main..branch`, which merging empties).
- **Inputs read:**
  - `tracker/items/WI-0002/artifacts/review.md` §"Definition of Done" D9, which names this entry as where the merge commit's sha would be recorded
- **Decisions:**
  - **Merged `wi/WI-0002` into `main` with `--no-ff`**, so the item's fifteen commits stay reachable as a group and `git log --grep WI-0002` reconstructs it. The merge subject carries the item ID like every other commit.
  - **The branch is left in place**, not deleted. Nothing in the record requires deleting it and `check-commit-refs` on a closed item is more useful with it than without.
- **Cross-answer check:** none — this entry records a merge and consumes no human answer.
- **Questions raised:** none
- **Commands:**
  - `git checkout main` → 0
  - `git merge --no-ff wi/WI-0002 -m "merge: the daily review sitting (refs WI-0002)"` → 0, merge commit **`65fec19c0b5583b0f2443b26a627da19d7cc931b`**
  - `python3 -m unittest discover -s tests -t . -q` **on the merged trunk** → 0, `Ran 32 tests in 3.434s` / `OK`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 6 item(s), 9 document(s)`, 0 errors, 0 warnings
- **Gates:** all nine were run and recorded on the closing entry above; this entry makes no transition and runs none of its own. The one it completes the evidence for is `definition-of-done` **D9**, whose `review.md` row promised the merge commit's sha here: it is `65fec19c`, and the suite is green on it — the merged trunk was tested, not only the trial.
- **Artifacts:**
  - merge commit `65fec19c0b5583b0f2443b26a627da19d7cc931b` on `main`
  - branch `wi/WI-0002`, retained at `ba55b1b`
- **Status:** `done` → `done` (no transition; the item was closed by the entry above)
- **Result:** `wi/WI-0002` is merged into `main` at `65fec19c` and the suite passes on the merged trunk. D9's evidence is complete: the trial merge predicted a clean result, and the real one delivered it.
