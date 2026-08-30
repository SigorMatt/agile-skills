# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T01:41:03Z — answer-questions v0.4.0 — architect

- **Item:** WI-0004
- **Trigger:** not dispatched; created by `answer-questions` while consuming `EP-001/Q-001`, whose answer widened the scope beyond anything an existing item recorded
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md` — the stakeholder's answer, in particular *"I want to be able to delete a card I don't need anymore; editing can wait."*
  - `tracker/items/EP-001/item.md` — the `## Out of scope` list, which excluded "Editing or deleting a card once it has been added"
  - `docs/product/vision.md` (v1) — the same exclusion, stated as "no editing or deleting cards once added"
  - `.claude/agile-skills/pipeline.yaml` — the creation-authority row permitting this skill to create a `work-item` at `draft` with `arose-from`
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md` (v1) — so the criteria could be written knowing the interface is a command line
- **Decisions:**
  - **Filed the deletion work as a new item rather than widening WI-0001.** WI-0001 is "add a card and have it survive a restart"; folding deletion into it would have hidden a scope change from the board and from the person who asked for it, which is the move `spec/question.md` and this skill's procedure both refuse. A new item makes the widening visible.
  - **Excluded editing, explicitly, in this item's `## Out of scope`.** The stakeholder drew that line themselves — *"editing can wait"* — and an item about removing cards is exactly where a later reader would assume editing had been quietly included.
  - **Set `priority: medium`, not `high`.** The three existing items are the epic's stated outcome and this one is a convenience added afterwards. The stakeholder did not rank it, so the priority is this skill's and is labelled as such in the item's notes for `refine` to change.
  - **Set `depends-on: WI-0001`.** There is nothing to delete until a card can be added and stored.
  - **Did not decide how a card is named when deleting it** — by position, by question text, or by an identifier the listing shows. It is a real user-facing choice, `refine` speaks to the stakeholder directly, and guessing it would have put an invented interface into acceptance criteria. Recorded in `## Notes` as `refine`'s.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --next-id work-item` → exit 0, `WI-0004`
  - `scripts/new-item --id WI-0004 --type work-item --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from EP-001/Q-001` → exit 0
- **Gates:** the gates for this execution are recorded in full on `EP-001`'s journal, which is the item this execution was dispatched on. Creating this item is one of that execution's artifacts, and the gate that covers it is `answer-is-propagated`, which passed.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new) — story, four acceptance criteria, out-of-scope list, and notes naming what `refine` must settle
  - `tracker/items/WI-0004/history.md` (new) — the creation row
  - `tracker/items/WI-0004/journal.md` (new) — this entry
- **Status:** `—` → `draft`
- **Result:** The deletion capability the stakeholder asked for in `EP-001/Q-001` now exists as a tracked draft item with its provenance recorded, rather than living only inside a question file.

## 2026-08-30T04:25:48Z — refine v0.3.0 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` (selection key: priority rank 3 tied with BUG-0001, broken on `created` — 2026-08-30T01:37:52Z is the older)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the draft, four criteria, four exclusions, and `## Notes` naming one thing as `refine`'s to settle with the stakeholder
  - `tracker/items/WI-0004/history.md` — one row, `— → draft`, actor `answer-questions`; a fresh draft, not a send-back from a later stage
  - `tracker/items/WI-0004/journal.md` — the creation entry, which records why the naming question was left open
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — every human answer at epic level
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`; `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — the other four human answers in this workspace
  - `tracker/items/WI-0001/item.md` — AC3 (what `recall list` prints) and AC9 (duplicate questions are permitted), the two delivered criteria a delete command collides with
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — the delivered review and scheduling behaviour AC3 of this item must hold against
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md` (v1) — §2 reserves a subcommand for this item, §5 fixes exit codes
  - `docs/process/using-recall.md` (v5) — what the tool tells a person today, including that duplicate questions are a deliberate allowance
  - `recall/cli.py`, `recall/deck.py`, `recall/store.py` — what `list` actually prints, what a `Card` holds, what `Deck` can do
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Filed two questions to the human and suspended, rather than writing criteria against a guessed interface.** R4 fails on all four criteria for one reason: no criterion names an invocation, because nothing says how a card is named. The item's own `## Notes` had already routed that to `refine` as the stakeholder's — *"it is the sort of thing the stakeholder has a view on, so it is theirs to be asked"* — and guessing it would have put an invented interface into acceptance criteria that `verify` cannot later question.
  - **Folded the duplicate-question case into `Q-001` rather than filing it separately.** `WI-0001` AC9 deliberately permits two cards with the same question side, so "the card whose question is X" is not always one card. That is not a second decision: each of the three naming options answers it differently and inseparably — a position and a code identify one card by construction, the question text does not — so a separate question would have been unanswerable until this one was.
  - **Filed the confirmation question (`Q-002`) as the stakeholder's rather than deciding it.** Deletion is the only irreversible operation in the tool, this item's `## Out of scope` rules out any recovery, and the stakeholder's single named failure condition is *"don't lose my progress"* (`EP-001/Q-001`). Whether the tool guards its one destructive operation is something they would meet every time they use it, and the cost of either answer falls entirely on them. R10 records it as an introduced combination that must be visible.
  - **Did not ask about message wording or exit codes.** `ADR-0001` §5 fixes exit codes; *"nothing fancier than that"* is a standing deferral over wording whose category `EP-001/Q-002`'s consequences already routed to `plan`. Asking anyway would tell them their answer was not heard. Recorded in the Q&A's "what was deliberately not asked".
  - **Did not ask about priority.** The item's `## Notes` hand the rank to `refine` explicitly. Left at `medium`: it is the last item in the epic and nothing depends on it. Recorded as this skill's decision, not the stakeholder's.
  - **Named the whole R10 combination set in the Q&A, including the six the stakeholder is not being asked about.** Deleting the last card, deleting against an absent deck, deleting against an unreadable deck, and visibility to `list`, to `review` and across a process boundary are all `refine`'s to write once the two answers land. Writing them down now is what stops them being lost between two executions of this skill in different sessions.
  - **Named `WI-0003/Q-002` in `Q-001`'s context without treating it as a rule.** That answer chose the option that left `recall list` untouched, and two of `Q-001`'s three options change what `recall list` prints. It was a choice about dates, not a standing rule about `recall list`, so it is surfaced to the stakeholder as context rather than used to eliminate options here.
- **Questions raised:** `Q-001` (blocking, to human) — how a card is named when deleting it; `Q-002` (blocking, to human) — whether deleting confirms first. Both open; the exchange is in `artifacts/refinement-qa.md`, which says `status: agenda` because no answer has been given.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before the questions were filed (6 items, 11 documents, 0 errors)
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0, "checked 0 consumed human answer(s)"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 after filing, reporting `question.blocking.not-suspended` on WI-0004 and a stale board; both are this execution's own doing and both are cleared by the transition and by `board-gen`
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, on the state this execution started from; the two errors it reports mid-execution are the open blocking questions and the stale board, which this transition and `board-gen` resolve)
  - `definition-of-ready` → **fail, per criterion** — R1 pass (frontmatter complete, `type`/`epic`/`priority` set); R2 pass (role, capability, "so that" outcome); R3 pass (AC1–AC4, labelled, checkboxes); **R4 fail** (no criterion names an invocation — all four turn on "deleting a card" with no way to name a card; `Q-001`); R5 pass (four exclusions, editing among them); **R6 fail** (by this execution's own doing — `Q-001` and `Q-002` are open and blocking, which is the suspension working); R7 pass (`depends-on: WI-0001`, `done`); **R8 fail** (`refinement-qa.md` says `agenda`, and honestly so — the conversation has not happened); R9 pass (one coherent change: a `delete` subcommand, a removal on `Deck`, and the documentation); **R10 fail** (six introduced combinations, two of which are the two questions filed and four of which are recorded in the Q&A for the resuming execution to write)
  - `criteria-are-decidable` → **fail** — not one of AC1–AC4 can be given a command. Each begins "after deleting a card" and no invocation exists to put there. This is the same gap as R4 and is what `Q-001` asks
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0004`, exit 0). No human answer has been consumed by this execution — the two questions are filed and unanswered — so there is nothing to check against. The prior answers were read, and `Q-001` carries the one that looked closest to a constraint (`WI-0003/Q-002` on what `recall list` prints) into its `## Context` for the stakeholder rather than resolving it here
  - `qa-recorded-verbatim` → **pass, vacuously and declared so** — `refinement-qa.md` holds both questions as they were filed and tags both answers `[unresolved]`. Nothing is tagged `[human]` because the stakeholder has said nothing yet, and the file declares `status: agenda` so that the Definition of Ready cannot pass on it
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` (new) — blocking, to human: how a card is named when deleting it
  - `tracker/items/WI-0004/questions/Q-002.md` (new) — blocking, to human: whether deleting confirms first
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new) — `status: agenda`; what was read, the per-criterion Definition of Ready table, both questions, and what was deliberately not asked
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0004 cannot be made Ready without the stakeholder: every one of its four criteria depends on how a card is named, which the item itself routed to them, and deleting is the only irreversible thing this tool does. Two blocking questions are filed as one ask and the item is suspended at `awaiting-answer` with `resume-to: draft`.

## 2026-08-30T04:31:50Z — answer-questions v0.4.0 — architect

- **Item:** WI-0004
- **Trigger:** `awaiting-answer` since 2026-08-30T04:25:48Z, suspended by `refine` with
  `resume-to: draft`. Both blocking questions on the item are addressed to `human` and both now
  carry a `## Answer`, so this skill is the only one that may consume them. Dispatched by the
  turn's first action, ahead of `next`, because an answered-but-unconsumed human question stops
  the orchestrator on every subsequent run.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` — how a card is named when deleting it; three
    options, ours was B; answered B.
  - `tracker/items/WI-0004/questions/Q-002.md` — whether deleting confirms first; three options,
    ours was B; answered B.
  - `tracker/items/WI-0004/item.md` — the four criteria an answer may have to amend, the four
    exclusions, and the `## Notes` bullet naming the naming rule as deliberately undecided.
  - `tracker/items/WI-0004/history.md` — two rows; the suspending row carries `resume-to: draft`,
    so the field did not have to be reconstructed.
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda`, the R1–R10 verdict
    table (R4, R6, R8 and R10 failing), round 1's two agenda entries, and the list of questions
    deliberately not asked.
  - Every prior human answer in the workspace, for the cross-answer check:
    `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `WI-0002/Q-001`, `WI-0002/Q-002`,
    `WI-0003/Q-001`, `WI-0003/Q-002`.
  - `docs/architecture/adr/` — all eight ADRs listed; `ADR-0001-a-command-line-interface.md` (§2
    reserves the subcommand, §4 makes `review` a prompt conversation, §5 fixes exit codes) and
    `ADR-0004-the-deck-file.md` (§4, every write atomic) are the two either answer could have
    contradicted. Neither does.
  - `docs/product/vision.md` and `docs/process/using-recall.md` (v5) — checked for sentences
    sourced to a stakeholder answer that these two answers would overtake. There are none.
- **Decisions:**
  - `Q-001` — **answered, route 4 already taken: the human replied to an escalation.** They chose
    **B**, naming the card by its question side: `recall delete --question "<text>"`, `recall
    list` unchanged, and a text matching two or more cards refuses and removes nothing. Nothing
    was decided by this skill; the options were put and one was chosen. The hole in B — `WI-0001`
    AC9 permits two cards sharing a question, and B can remove neither — was stated in the option
    and accepted in the answer, so it is recorded as an `## Out of scope` bullet rather than left
    to be rediscovered.
  - `Q-002` — **answered, same route.** They chose **B**: `recall delete` prints both sides and
    asks `delete this card? [y/n]`, removing on `y` and leaving the deck untouched otherwise, with
    no skip flag. Option C's `--yes` is recorded as out of scope so its absence reads as a
    decision.
  - **No ADR written.** Route 3 was not used: the record was not silent and this skill chose
    nothing. Where the naming rule needs an architectural home beyond the item, that is `plan`'s
    under `ADR-0001` §2.
  - **No acceptance criterion amended, deliberately.** The item is at `draft`, where criteria are
    not yet frozen, and rewriting them against these two answers is precisely the R4 gap
    `refinement-qa.md` recorded as `refine`'s. Doing it here would perform that skill's work in
    the wrong file and without its gates. What the answers open up — the ambiguous-match refusal,
    the prompt, what `n` and an empty reply do, what a closed standard input does — is written
    into `## Notes` as a named to-do for `refine` on resume, so none of it can be lost.
  - **No new work item filed** (step 3b). Neither answer widens scope: `Q-001`'s answer explicitly
    *declines* work — *"it's not worth building for"* — and `Q-002`'s chooses among behaviours
    already inside this item.
- **Cross-answer check:**
  - `Q-001` checked against `EP-001/Q-001` (**compatible** — it is the answer that produced this
    item, and B is what *"nothing fancier than that"* looks like); `EP-001/Q-002` (**compatible** —
    a typed argument is the command-line tool they chose); `WI-0003/Q-002` (**compatible** — there
    they were offered a change to `recall list` and left it alone; here they did again, and B is
    the option that leaves it alone).
  - `Q-002` checked against `EP-001/Q-001` (**compatible, and reconciled by them in this answer** —
    that answer holds both *"don't lose my progress"* and *"nothing fancier than that"*, B serves
    the first at the second's cost, and they supplied the reconciliation themselves: *"I'd rather
    have one extra keypress than lose a card to a typo"*); `EP-001/Q-002` (**compatible** — a
    `[y/n]` prompt is `ADR-0001` §4's shape in a second place); `WI-0003/Q-002` (**compatible** —
    the same trade of small friction for confidence they made about the per-card date line);
    `WI-0004/Q-001` (**compatible and mutually supporting** — the prompt is the guard against the
    typo that typing a question invites).
  - No verdict is `conflicts`, so no question was filed under ADR-0008 §3. No sentence of theirs
    was reworded anywhere: `docs/product/vision.md`'s quotations of `EP-001/Q-001` are untouched,
    which was the specific temptation here, because B on `Q-002` sits against their *"nothing
    fancier than that"*.
- **Questions raised:** none.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0, 2 consumed human answers
    checked, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 mid-execution, with exactly the
    two errors this execution is in the middle of clearing (`board.stale`, and
    `question.awaiting.none-open` on WI-0004 now that both questions are answered); re-run to
    exit 0 after the transition and `board-gen`
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in either `## Consequences` was reopened
    and the change confirmed present: `item.md` — the `## Notes` bullet that read *"How a card is
    named when deleting it … it is theirs to be asked"* is gone, replaced by two settled decisions
    quoting the stakeholder, and `## Out of scope` has grown from four bullets to six; and
    `artifacts/refinement-qa.md` — both round-1 `**Answer:**` lines have changed from
    `[unresolved]` to the answer verbatim, tagged `[human]`. Neither `## Consequences` section is
    empty and both name files rather than intentions. What each section says was *not* changed —
    the criteria, `docs/process/using-recall.md`, and any ADR — is named with the skill that owns
    it, so the omissions are decisions on the record too.
  - `answered-from-the-record` → **pass**. Neither answer is derived: both are the stakeholder's
    reply to an escalation, quoted verbatim in `## Answer` and again where they were propagated.
    Every consequential detail beyond their words is cited — the refusal exit code to `ADR-0001`
    §5, the duplicate-question permission to `WI-0001` AC9, the prompt's shape to `ADR-0001` §4.
  - `escalation-is-justified` → **skipped**, correctly: nothing was re-addressed to the human,
    because the record now settles both questions. The gate has no subject.
  - `cross-answer-consistency` → **pass**. `lint-answers --item WI-0004` exit 0 over both consumed
    answers; both carry a `## Cross-answer check` naming the prior answers checked and a verdict
    for each, and no verdict is `conflicts`, so rule 2 has nothing to require and rule 3 nothing
    to catch.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0, 6 items and 11 documents, 0 errors
    0 warnings, after the transition and `board-gen`. The mid-execution exit 1 is recorded above
    with its two errors, both of which were this execution's own unfinished state.
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-30T04:25:48Z records
    `resume-to: draft`; both blocking questions on the item are now `answered` and none is open;
    the item is moved to `draft`. Read from the history row, not inferred from `refine` being the
    asker.
  - `a-deferral-is-not-an-answer` → **skipped**, correctly: neither reply defers. Both name an
    option letter and give a reason for it, and `Q-001`'s *"I'll deal with that separately"* is a
    refusal of further work, not a postponement of this question — the question it was asked
    about is answered in the same sentence.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: open` → `answered`, `answered-at` and
    `answered-by: human` set; `## Cross-answer check` and `## Consequences` written.
  - `tracker/items/WI-0004/questions/Q-002.md` — the same.
  - `tracker/items/WI-0004/item.md` — `## Notes` restructured into "settled by the stakeholder"
    and "still `refine`'s to do"; two `## Out of scope` bullets added (no disambiguation of
    duplicate questions, no prompt-skipping flag).
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — both round-1 answer lines filled in.
    Left at `status: agenda`: it becomes a record when `refine` rewrites the criteria, not when
    the answers arrive.
  - `tracker/board.md` — regenerated.
  - No document under `docs/` changed, so no version bump and no change-log row was due.
  - Commit: `tracker: the answered questions and every artifact you propagated into (refs
    WI-0004)`.
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of WI-0004's blocking questions are answered by the stakeholder and propagated:
  a card is named for deletion by its question side, an ambiguous match is refused rather than
  guessed at, and every deletion is confirmed at a `[y/n]` prompt with no way to skip it. The item
  returns to `draft` for `refine`, which now has an unblocked R4 and a written list of the new
  combinations these two answers open up.

## 2026-08-30T04:36:37Z — refine v0.3.0 — product-analyst

- **Item:** WI-0004
- **Trigger:** `draft`, dispatched by `next` as the highest-ranked runnable item — priority
  `medium` tied with BUG-0001, broken by `created` ascending (01:37:52Z against 02:07:30Z). This
  is the **resumption** of this skill's own round 1, not a fresh draft and not a send-back:
  `history.md` shows `draft → awaiting-answer` at 04:25:48Z filed by `refine`, and
  `awaiting-answer → draft` at 04:31:50Z by `answer-questions` with both questions answered. The
  job was therefore to close round 1's four failing criteria, not to re-open the item's story.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the four criteria to rewrite, the six `## Out of scope`
    entries, and the `## Notes` section `answer-questions` had already restructured into "settled
    by the stakeholder" and "still `refine`'s to do".
  - `tracker/items/WI-0004/history.md` — three rows, read first per precondition 3.
  - `tracker/items/WI-0004/journal.md` — `answer-questions`' creation entry and its consumption
    entry; the second names exactly what it left for this execution.
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda`, the R1–R10 table, the
    two agenda entries with the answers now filled in, and the "deliberately not asked" list,
    which is the reason no second round was needed.
  - `tracker/items/WI-0004/questions/Q-001.md`, `Q-002.md` — both answered, with their
    `## Cross-answer check` and `## Consequences`.
  - Every other recorded human answer, for §4a: `EP-001/Q-001`, `Q-002`, `Q-003`;
    `WI-0002/Q-001`, `Q-002`; `WI-0003/Q-001`, `Q-002`.
  - `tracker/items/WI-0001/item.md` — AC2 (blank-side refusal), AC3 (what `list` prints), AC6
    (empty deck), AC7 (the one file), AC8 (unreadable deck), AC9 (duplicate questions permitted).
    AC12 covers AC3 and AC6 by ID.
  - `tracker/items/WI-0002/item.md` — AC3 (re-asking on an unrecognised response), AC5–AC7,
    AC9 (part-way sitting), AC13 (what "due" means), which AC3 and AC6 here are written against.
  - `docs/architecture/adr/ADR-0001-a-command-line-interface.md` (v1) §2 (the reserved
    subcommand), §3 (options not prompts), §4 (interactive on stdin), §5 (exit codes);
    `ADR-0004-the-deck-file.md` §1–2 (path and JSON shape), §4 (atomic writes), §5 (never repair),
    §6 (absent is not unreadable); `ADR-0002` §1 (grading is two-way); `ADR-0007` (the next-review
    line).
  - `docs/product/vision.md` — checked for a statement these criteria would contradict; none.
  - `docs/process/using-recall.md` (v5) — its section list, to confirm the documented-message
    device AC10 relies on has a place to live.
  - `recall/cli.py`, `recall/store.py` — what `list` actually prints, how `_read_line` handles
    end of input, and the two existing exit codes, so the criteria describe the tool that exists
    rather than one imagined.
- **Decisions:**
  - **Four criteria became twelve.** Round 1's AC1–AC4 all began "after deleting a card" and named
    no invocation. The rewrite keeps all four intentions and makes each a command: old AC1 → AC1;
    old AC2 → AC2; old AC3 → AC3, widened to cover a card that was *not* due, which is what "whether
    or not it was due" always meant and could not be checked before; old AC4 → AC4, which can now be
    stated because "a card that does not exist" needed the naming rule to have a meaning. The eight
    new ones are the ground the two answers opened: AC5 the ambiguous match, AC6 everything that is
    not `y`, AC7 a missing or blank `--question`, AC8 an unreadable deck, AC9 an absent one, AC10 the
    last card, AC11 the surviving cards' schedules, AC12 the shape of the listing.
  - **A preamble fixes the three things every criterion leans on** — the invocation and its ADR-0001
    clauses, what "the card whose question is X" matches, and that no criterion fixes a message or a
    particular non-zero exit value. Same device as `WI-0002`'s preamble, for the same reason: a
    definition repeated in twelve criteria drifts between them.
  - **Matching is exact, byte for byte** — `[assumed]`, and the meaning of `Q-001`'s answer rather
    than an addition to it. `WI-0001` AC3 already stores and prints a question side exactly as
    given, so the typed string is the string the listing showed. Decided rather than asked because
    the failure mode is AC4 — refused, nothing removed, retype it — and because the looser
    alternatives could match a card the person did not mean, which is what `Q-002`'s answer guards
    against. Recorded in `## Notes` as reversible and, if it needs loosening, theirs.
  - **Declining exits 0** — `[assumed]`, from `ADR-0001` §5: non-zero is for a refused or failed
    operation, and `n` is neither. AC6 requires the run to say on stdout that the card was not
    deleted, so the outcome is observable whatever the code turns out to be.
  - **AC6 asks once and does not re-ask**, deliberately unlike `recall review` (`WI-0002` AC3).
    This is not an inconsistency introduced here: `Q-002` option B, as the stakeholder chose it,
    reads *"removes the card on `y` and leaves the deck untouched on anything else."* The criterion
    says so and cites it, because a reader meeting the two subcommands side by side will otherwise
    read it as a defect.
  - **AC12 is written to §6a's shape.** It names `WI-0001` AC3 and AC6 **by ID** rather than "the
    earlier criteria"; it says the assessment is a read of those criteria's text against this
    item's behaviour, with the suite as evidence rather than as the definition; and it says what to
    do if nothing executable exercises both — state the non-intersection, then add a case or waive
    it by name.
  - **Message wording and the exact non-zero values left to `plan`** — `[assumed]`, under the
    stakeholder's standing deferral (*"nothing fancier than that"*, `EP-001/Q-001`), already
    recorded as `plan`'s in `EP-001/Q-002`'s consequences. AC10 names the empty-deck message by
    reference to the tool's documentation, which obliges `plan` to document it.
  - **Priority stays `medium`.** The item's `## Notes` invited `refine` to rank it; nothing depends
    on it and the stakeholder did not rank it. Recorded as this skill's decision, not theirs.
  - **`## Out of scope` left as it stands, at six entries.** `answer-questions` added the two the
    answers implied (no way to pick between duplicate questions, no flag to skip the prompt) and the
    four from the item's creation stand. Nothing needed adding.
  - **No question filed, no second round.** Every remaining gap failed step 3's product-stake test:
    two fall inside a standing deferral and one rests on delivered behaviour. Round 1's
    "deliberately not asked" list was re-read and still holds.
  - **No split (R9).** One `delete` subcommand, one removal on the deck, one documentation change.
- **Cross-answer check:** the twelve criteria and three assumptions were checked against all seven
  prior recorded human answers — `EP-001/Q-001`, `Q-002`, `Q-003`; `WI-0002/Q-001`, `Q-002`;
  `WI-0003/Q-001`, `Q-002`. Every verdict is **compatible**, each with its reason, in
  `artifacts/refinement-qa.md` `## Cross-answer check`. The two that could have conflicted are
  `EP-001/Q-001`, where *"nothing fancier than that"* pulls against a confirmation prompt — AC6 asks
  once and never re-asks, which is the smallest guard that is not silence, and the stakeholder
  reconciled it themselves in `Q-002` — and `WI-0003/Q-001`, where capping the ladder meets a
  deletion: AC11 requires `rung` and `due` on the surviving cards to be untouched, so the cap holds
  rather than being disturbed. No verdict is `conflicts`, so no question was filed under ADR-0008
  §3, and no recorded sentence of theirs was reworded anywhere.
- **Questions raised:** none this round. Round 1's two — `Q-001` and `Q-002`, both blocking, both
  addressed to `human` — are answered, propagated and recorded verbatim in
  `artifacts/refinement-qa.md`. Nothing is left `[unresolved]`. Three answers are tagged
  `[assumed]`, each naming the deferral or delivered criterion it rests on.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 6 items, 11 documents, 0 errors,
    0 warnings
  - `.claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0, 2 consumed human answers,
    0 errors, 0 warnings
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0, 0 errors and 0 warnings, run after
    the criteria rewrite and again as the transition's own precondition.
  - `definition-of-ready` → **pass, criterion by criterion**, recorded as a second column in
    `artifacts/refinement-qa.md` `## Round 1 — the Definition of Ready at close` beside round 1's
    verdicts. R1 pass (frontmatter complete, `type`/`epic`/`priority` set). R2 pass (unchanged —
    role, capability, "so that"). R3 pass (twelve `AC<n>` checkboxes). **R4 fail → pass** (the four
    invocation-less criteria rewritten as twelve, each naming a command and an observation; no
    unmeasurable adjective survives — what would have been "safely", "gracefully" and "cleanly" are
    now "the deck file's bytes identical before and after", "names the file", and "the documented
    empty-deck message … exits 0"). R5 pass (six exclusions; editing a card and any way to pick
    between two cards sharing a question are both things a reader would assume were included).
    **R6 fail → pass** (`Q-001` and `Q-002` both `answered`; no open question on the item). R7 pass
    (`depends-on: WI-0001`, `done`). **R8 fail → pass** (this refinement's Q&A is recorded verbatim
    and the file now declares `status: recorded`). R9 pass (one coherent change). **R10 fail →
    pass** (every combination accounted for; the map is in the item's `## Notes` under the R10
    heading, covering round 1's (a)–(f) plus two that list missed — a blank `--question`, and
    delete against the shape of the listing).
  - `criteria-are-decidable` → **pass**, and here is the settling observation for each. AC1 —
    `recall delete --question <second card's question>` with `y` on stdin, then `recall list`;
    verdict from the exit code, both sides on stdout before the prompt, and the listing afterwards.
    AC2 — the same, then `recall list` in a **new** process. AC3 — write a three-card deck file with
    the dates named, delete two, run `recall review` from a here-document; verdict from whether X's
    and Y's question sides appear. AC4 — a string equal to neither question; verdict from stderr,
    a non-zero exit, no answer side on stdout, and `cmp` of the deck file. AC5 — a deck with a
    duplicated question side; same four observations plus both cards still listed. AC6 — four runs
    (`n`, a word, an empty line, `< /dev/null`); verdict from the "not deleted" line on stdout,
    exit 0, no traceback, and `cmp` each time. AC7 — four runs (omitted, `""`, spaces, tabs);
    verdict from stderr naming the option, a non-zero exit, and `cmp` — plus the file still absent
    when it started absent. AC8 — write a truncated deck file, run, `cmp`. AC9 — remove the deck
    and its parent, run, then test that both are still absent. AC10 — a one-card deck, delete it,
    then `recall list` and `recall add`; verdict from the documented empty-deck message and two
    zero exits. AC11 — a three-card deck with distinct `rung`/`due`, delete one, then compare the
    surviving entries' four fields, their order and `version`. AC12 — read `WI-0001` AC3 and AC6
    against this item's behaviour and run `recall list` after a deletion; if no test exercises both,
    the non-intersection is stated and then covered or waived by name.
  - `cross-answer-consistency` → **pass**. `lint-answers --item WI-0004` exit 0. Both consumed
    answers carry a `## Cross-answer check`; the check for what *this* execution wrote is in
    `refinement-qa.md`, covering all seven prior answers with a verdict each and none `conflicts`.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` now declares `status:
    recorded` and holds both questions and both answers in the stakeholder's own words, quoted
    whole and tagged `[human]`; three further answers are tagged `[assumed]`, each naming the
    deferral or delivered criterion it rests on; nothing is `[unresolved]`. Nothing was paraphrased
    into agreement — in particular `Q-001`'s *"I'll deal with that separately; it's not worth
    building for"* is kept as the refusal it is, and became an `## Out of scope` bullet rather than
    a criterion.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — `## Acceptance criteria` replaced: four criteria and no
    preamble became a preamble and twelve criteria, AC1–AC12. `## Notes` — the "still `refine`'s to
    do" list replaced by the three `[assumed]` decisions with their basis, the two design questions
    routed to `plan`, the priority decision, and the R10 coverage map. `## Out of scope` unchanged
    at six entries.
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; the "this
    is an agenda" paragraph replaced by what actually happened; three sections added — the
    Definition of Ready at close, what was decided here rather than asked, and the cross-answer
    check for what this execution wrote.
  - `tracker/board.md` — regenerated.
  - No document under `docs/` changed, so no version bump and no change-log row was due. No ADR was
    written: `refine` does not write them, and the design questions this raised are named in
    `## Notes` for `plan`.
  - Commit: `tracker: the refined item and its Q&A record (refs WI-0004)`.
- **Status:** `draft` → `ready`
- **Result:** WI-0004 is Ready. Deleting a card is now twelve criteria a person with a terminal and
  no context could settle: name the card by typing its question side exactly, see both its sides,
  confirm with `y`, and get a refusal that removes nothing when the name matches none or two. The
  Definition of Ready passes on all ten criteria, with R4, R6, R8 and R10 closed since round 1, and
  three decisions are recorded as assumptions rather than as things the stakeholder said.

## 2026-08-30T04:41:16Z — plan v0.4.0 — architect

- **Item:** WI-0004
- **Trigger:** `ready` since 2026-08-30T04:36:37Z, dispatched by `next` as the highest-ranked
  runnable item — tied with BUG-0001 on priority `medium`, broken by `created` ascending. A first
  plan, not a re-plan: `history.md` shows no rejection and no return from a later stage.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the twelve criteria this design is contracted to, the six
    `## Out of scope` entries, and `## Notes`, whose three `[assumed]` decisions are the design's
    soft ground and whose R10 map says where each combination is accounted for.
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (`status: recorded`) — both answers
    verbatim, the three things decided rather than asked with their basis, and the Definition of
    Ready at close.
  - `tracker/items/WI-0004/questions/Q-001.md`, `Q-002.md` — the stakeholder's two answers, which
    fix the invocation and the guard.
  - `tracker/items/WI-0004/history.md`, `journal.md` — four rows; the `answer-questions` and
    `refine` entries, which say what each left for this execution.
  - `tracker/items/WI-0001/item.md` (AC2, AC3, AC6, AC8, AC9) and `WI-0002/item.md` (AC3, AC9,
    AC10, AC13) — the delivered criteria AC6, AC8, AC10, AC11 and AC12 are written against.
  - `docs/architecture/overview.md` v4 — the three-layer split, and the sentence about `cli.py`
    holding the re-asking loop, which this item makes incomplete.
  - `docs/architecture/adr/` — all eight. Load-bearing here: `ADR-0001` §2 (the reserved
    subcommand), §3 (options not prompts), §4 (interactive on stdin), §5 (exit codes);
    `ADR-0004` §1–2 (path, JSON shape), §4 (atomic writes), §5 (never repair), §6 (absent is not
    unreadable); `ADR-0003` (standard library only). `ADR-0002`, `ADR-0006`, `ADR-0007` and
    `ADR-0008` were read and are untouched — AC11 exists to keep them so.
  - `tracker/project.yaml` — trunk `main`, and `commands.test` / `commands.lint` already set for
    WI-0001 with `ADR-0003` behind them.
  - Source: `recall/cli.py` in full (`cmd_add`'s pre-file blank check, `cmd_list`, `cmd_review`'s
    save-per-card, `_read_line`'s `EOFError` handling, `_read_grade`'s loop, `_report_unreadable`,
    the two non-zero exit codes); `recall/deck.py` in full (`Deck.add`/`replace`, `due_positions`
    as the selector precedent, `record_answer`); `recall/store.py` `load` and `save`.
  - `docs/process/using-recall.md` v5 — its section list, since AC6 and AC10 name messages by
    reference to it.
- **Decisions:**
  - **The prompt asks once; anything but `y` cancels; cancelling exits 0; the four pre-prompt
    refusals exit non-zero; `review` is left alone.** Route: **asked-shaped, recorded as an ADR** —
    `ADR-0009`, new this execution. Not escalated to the human: they already answered the question
    that has product stake (`Q-002`), and what remained was how their answer coexists with
    `review`'s re-asking loop and what `ADR-0001` §5 means for a deliberate `n`. That is
    architecture, and leaving it to `implement` would have produced either a copied loop that
    contradicts the option text they chose, or a guess about the exit code. The ADR names three
    options, and its reversibility clause is honest about the asymmetry: the exit code and the loop
    are one expression each, the guard itself is the stakeholder's to remove.
  - **Matching stays exact and is not re-decided.** Route: **documented** — `refine` recorded it in
    `item.md` `## Notes` and `refinement-qa.md` as `[assumed]` with its reversal cost. `plan` cites
    it and adds nothing.
  - **The matching and the removal go in `deck.py`; the prompt, messages and codes in `cli.py`;
    `store.py` is untouched.** Route: **documented** — `docs/architecture/overview.md`'s layer
    rules decide it, and `due_positions` is the existing precedent for a selector that returns
    positions and decides nothing. `positions_matching` returns positions rather than cards
    precisely because AC5's answer is a count.
  - **A deletion is load, remove, save — no new persistence machinery.** Route: **documented** —
    `ADR-0004` §§4–6 already give AC8 (never repair), AC9 (absent is empty) and the atomicity
    behind AC11.
  - **`Deck.remove` rather than a rebuild through `replace`.** Route: **documented** — `replace`
    preserves length by design, because that is what `WI-0002` AC10 protects. AC11 is then true by
    construction: `remove` constructs no `Card`, so no survivor's fields can change.
  - **Four reversible assumptions**, each with its reversal cost, under `plan.md` `## Assumptions`:
    the yes is compared case-folded and stripped like `review`'s two grades; the card is printed in
    a sitting's two-line shape rather than as a listing line; no new exit code; and
    `positions_matching` is not retrofitted into `add`, `list` or `review`. The last is the one
    worth naming as a decision not to act: sharing it would put three `done` items back in play
    against criteria that never asked for it.
  - **BUG-0001 is not folded in.** It touches `cli.py`'s error handling and is tempting while
    `cmd_delete` is being written. It is a separate `ready` item with its own criteria; widening
    this plan would make both unverifiable. Recorded in `## Out of scope for this item`.
  - **No question filed and no ADR superseded.** Nothing in the criteria contradicts a standing
    decision; `ADR-0009` is additive and cites `ADR-0001` rather than replacing any clause of it.
- **Cross-answer check:** this execution relied on two human answers — `WI-0004/Q-002`, quoted in
  `ADR-0009` and in the overview, and `WI-0004/Q-001`, cited for why `recall list` gains nothing.
  Checked against `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `WI-0002/Q-001`,
  `WI-0002/Q-002`, `WI-0003/Q-001`, `WI-0003/Q-002`. Every verdict **compatible**, and the two
  worth stating: `EP-001/Q-001`'s *"nothing fancier than that"* against a confirmation prompt — the
  stakeholder reconciled that themselves in `Q-002` (*"I'd rather have one extra keypress than lose
  a card to a typo"*), and `ADR-0009` quotes their reconciliation rather than making one; and
  `WI-0002` AC3's re-asking loop against `ADR-0009`'s single ask — not two of *their* statements in
  conflict, since AC3 is `refine`'s wording of a delivered behaviour, so recording the difference
  in an ADR is legitimate where reconciling two of their answers would not have been. No verdict is
  `conflicts`; no question was filed; `ADR-0009` settles no contradiction between two of their own
  answers, and no sentence of theirs was reworded — the overview's quotations of `EP-001/Q-001` and
  `WI-0002/Q-001` are untouched, and the paragraph edited there was **added to**, not rewritten.
- **Questions raised:** none. Nothing met `spec/question.md` §1's bar for `plan` — no decision here
  is irreversible, and none depends on intent no document records.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 6 items, 12 documents, 0 errors,
    0 warnings
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 2 documents in 2 uncommitted
    paths under `docs`, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 9 consumed human answers,
    0 errors, 0 warnings
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, ran 43 tests, OK
  - `python3 -m compileall -q recall tests` → exit 0
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0, 0 errors and 0 warnings, run after
    `plan.md`, `ADR-0009` and the overview bump, and again as the transition's precondition.
  - `every-criterion-is-addressed` → **pass**. `plan.md` `## Acceptance criteria mapping` has one
    row per criterion, AC1 through AC12, with no gaps: each names the numbered step or steps that
    satisfy it and the specific observation that demonstrates it — a written deck file, a command,
    and what is asserted — rather than the word "tests". The two rows that needed care are AC11,
    demonstrated by a field-by-field comparison of the surviving entries' `question`, `answer`,
    `rung`, `due`, their order and `version`; and AC12, whose criterion is a read of `WI-0001` AC3
    and AC6 and which is given an executable case at step 7 precisely so its "waive it by name"
    branch never has to be used.
  - `project-commands-resolved` → **pass**. `tracker/project.yaml` already carries
    `test: python3 -m unittest discover -s tests -t . -q` and
    `lint: python3 -m compileall -q recall tests`, set for WI-0001 with `ADR-0003` behind them.
    Both were run from the repository root during this execution — 43 tests, OK, exit 0; and exit 0
    — so the gate rests on commands observed to work rather than on ones expected to. Neither exits
    zero without checking anything. No change to the file was needed, so none was made.
  - `decisions-recorded` → **pass**. Every choice this plan makes is in `plan.md`
    `## Decisions and ADRs` as a table row naming where it is recorded and which branch of the
    preference order produced it: one **asked-shaped** decision written as `ADR-0009` with three
    options and an explicit reversibility clause; four **documented** decisions each citing the ADR
    or the overview section that settles it; and the wording and exit-code choices as
    **assumptions**, in `## Assumptions` with what reversing each would cost. Nothing is left as an
    unattributed choice inside a step.
  - `plan-is-executable-without-you` (advisory) → **pass**. The ten steps each name the file they
    touch and what is true afterwards; steps 1–5 give `cmd_delete`'s five moves in order with the
    branch and exit class for each, so no step requires a decision the plan does not make. The
    place a developer would otherwise have had to choose — whether the prompt re-asks — is decided
    in `ADR-0009` and restated in `## Approach`.
  - `cross-answer-consistency` → **pass**. `lint-answers --uncommitted` exit 0 over the two
    uncommitted documents and 9 consumed human answers. The substantive check is above under
    **Cross-answer check**: `ADR-0009` records a difference between an ADR-sourced behaviour and a
    new one, not a reconciliation of two stakeholder answers, which is the move 5a forbids.
  - `claims-are-sourced` → **pass**. `lint-claims --uncommitted` exit 0 across
    `ADR-0009-confirming-a-deletion.md` and `overview.md` v5. Every absolute in the new ADR carries
    a citation — the "no way to delete without confirming" clause to `WI-0004`, the "never learns
    where it came from" and "only reader of standard input" clauses in the overview to `ADR-0001`,
    `WI-0002` AC3 and `ADR-0009` — and every `[src:]` marker resolves.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` — created. Problem, approach layer by layer, ten
    numbered steps, the twelve-row mapping table, four assumptions, the decisions table, scaffolding
    (`none`), five specific risks, and what this item excludes.
  - `docs/architecture/adr/ADR-0009-confirming-a-deletion.md` — created, v1, `status: current`,
    three options, decision in five clauses, reversibility stated on each.
  - `docs/architecture/overview.md` — v4 → **v5**, with a change-log row. Two edits: the `deck.py`
    bullet gains the selector-and-removal clause, and the `cli.py` bullet now says it holds two
    prompt shapes and why they differ. No existing sentence was removed or reworded to agree.
  - `tracker/project.yaml` — unchanged; both commands were already real and were re-run to confirm.
  - `tracker/board.md` — regenerated.
  - No file was created outside `tracker/` and `docs/`; `## Scaffolding` says `none`, and
    `tests/test_delete.py` is step 6's work for `implement`.
  - Commit: `tracker: the plan, any ADRs, and the documents you updated (refs WI-0004)`.
- **Status:** `ready` → `planned`
- **Result:** WI-0004 is planned. Ten steps add one subcommand across two of the three layers —
  `positions_matching` and `Deck.remove` in `deck.py`, `cmd_delete`'s five moves in `cli.py`, and
  nothing at all in `store.py` — with a test module, a documentation section and one architecture
  decision. `ADR-0009` records the one thing the item made genuinely hard: a deletion asks once and
  treats everything that is not a yes as a cancellation, which is deliberately unlike `review`, and
  cancelling is not a failure.

## 2026-08-30T04:43:10Z — implement v0.3.0 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next` — highest-ranked runnable item (medium, created 2026-08-30T01:37:52Z, ahead of BUG-0001's 02:07:30Z)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC12 and the two stakeholder decisions in `## Notes`
  - `tracker/items/WI-0004/artifacts/plan.md` — the ten steps, the AC mapping, the four assumptions
  - `tracker/items/WI-0004/history.md` — five rows; last is `ready → planned` by `plan`, so this is a fresh start and no branch existed
  - `tracker/items/WI-0004/questions/Q-001.md`, `Q-002.md` — both `answered`, both already propagated into `item.md` and `refinement-qa.md` by `answer-questions`
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, test and lint commands
  - `recall/deck.py`, `recall/cli.py`, `recall/store.py`, `tests/support.py`, `tests/test_add.py`, `tests/test_list.py` — the code the plan's steps 1–7 extend
- **Decisions:**
  - none yet — this entry opens the execution. Step 3 of the procedure moves the item before any code is written so that an interruption leaves a truthful status.
- **Cross-answer check:** none — this execution has edited no `docs/` sentence yet.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0 (branch created at `152c531`)
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no change has been made; it runs on the branch head at step 7)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **skipped** (same reason; it was exit 0 immediately before this execution began)
  - `every-criterion-has-a-test` → **skipped** (no test written yet)
  - `commits-reference-the-item` → **skipped** (no commit on the branch yet)
  - `cross-answer-consistency` → **skipped** (nothing changed since `main` yet)
  - `claims-are-sourced` → **skipped** (same reason)
- **Artifacts:**
  - branch `wi/WI-0004`, branched from `main` at `152c531`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0004 has started on `wi/WI-0004`. No code is written yet; the plan's ten steps are next, in order.

## 2026-08-30T04:49:13Z — implement v0.3.0 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress` — this execution's own opening entry at 04:43:10Z; the work of `plan.md`'s ten steps
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` (AC1–AC12), `artifacts/plan.md`, `history.md`, `questions/Q-001.md`, `questions/Q-002.md`
  - `tracker/project.yaml`; `recall/deck.py`, `recall/cli.py`, `recall/store.py`, `bin/recall`
  - `tests/support.py`, `tests/test_add.py`, `tests/test_list.py`
  - `docs/architecture/overview.md`, `docs/process/using-recall.md`
- **Decisions:**
  - **Plan step 9's bump was already made, so this execution bumped the overview to v6 instead of v5.** `plan` had already written v5 and its WI-0004 clauses as intent, cited to `plan.md`. Rather than skip the step, this followed the precedent `implement` set for WI-0003 at overview v4: restate the two clauses as description of what is built and cite `recall/deck.py` and `recall/cli.py` alongside `ADR-0009`. What the document claims is unchanged; only its sourcing moved.
  - **Two D12 repairs in `docs/process/using-recall.md` that no plan step named.** The damaged-deck paragraph named three subcommands where there are now four, and "What this version does not do yet" listed deleting a card as future work. This item's own change made both false, so both were fixed and recorded in the v6 change-log row.
  - **The tests landed in the same commit as the code** (`6aabe6f`), with the documentation second (`1d46cae`), because the procedure requires the test to come with the change rather than in a cleanup pass.
  - **Two mutations were run and reverted, to check that the two subtlest criteria bite.** A re-asking confirmation loop failed AC6 (`2 != 1` on the prompt count); a `Deck.remove` that rebuilt survivors at `FIRST_RUNG` failed AC11. Both reverted with `git checkout --`, and the full suite was green afterwards.
  - **All four of `plan.md`'s assumptions were implemented as written** — stripped and case-folded reply, question-then-indented-answer, no new exit code, `positions_matching` used only by `delete`. None was re-litigated and none needed escalating.
  - **Not decided here, and left alone:** BUG-0001's traceback on a non-`DeckUnreadable` filesystem error, which `cmd_delete` inherits; and any near-miss suggestion on a failed match, which `plan.md` records as a product decision for the stakeholder.
- **Cross-answer check:** one sentence, an ordinary repair. `docs/architecture/overview.md`'s deletion clause carries `[src: ADR-0009; WI-0004/Q-002]` — the stakeholder's own choice that a deletion shows the card and asks first, with no flag to skip. This execution added `recall/cli.py` to that citation and changed no part of what the sentence claims; the built behaviour is exactly what they chose. Nothing they have said since is incompatible with it — `Q-001` and `Q-002` are the only WI-0004 answers, they were given together on 2026-08-30, and `Q-001` (naming a card by its question side) and `Q-002` (always confirming) constrain different halves of the command. The new `## Deleting a card` section in `docs/process/using-recall.md` cites both answers, but it adds sentences rather than rewriting any. `lint-answers --changed-since main` → exit 0.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 55 tests … OK`), run on the branch head `1d46cae`
  - `python3 -m compileall -q recall tests` → 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0 (`all 2 commit(s) on main..wi/WI-0004 name WI-0004`)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (6 items, 12 documents, 0 errors, 0 warnings)
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0 (9 consumed human answers checked)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0 (2 documents differ from main)
  - two mutation runs of `python3 -m unittest tests.test_delete -q` → 1 each, both reverted (see Decisions)
  - `git commit` ×2 → 0 each
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0 on `1d46cae`; 55 tests, 12 of them new)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md` names a test function for each of AC1–AC12; two mutation runs show AC6 and AC11 fail when the behaviour is removed)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, both commits name WI-0004)
  - `no-unplanned-scope` (advisory) → **pass** (five files changed, each traceable to a plan step or to the two D12 repairs above; `recall/store.py` and the other test modules untouched)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` exit 0)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` (new)
  - branch `wi/WI-0004`, commits `6aabe6f..1d46cae` — `recall/deck.py`, `recall/cli.py`, `tests/test_delete.py`, `docs/process/using-recall.md` (v6), `docs/architecture/overview.md` (v6)
- **Status:** `in-progress` → `verifying`
- **Result:** `recall delete --question "..."` is built as planned: it names a card by its exact question side, shows both sides, asks once, and removes it only on a yes. All twelve criteria have a test, all seven hard gates pass on the branch head, and the two claims this item made false in `docs/process/using-recall.md` are repaired. BUG-0001 was left alone deliberately.

## 2026-08-30T04:54:32Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next` (medium, created 01:37:52Z, ahead of BUG-0001)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC12, read **before** the implementation report, which is the only standard used here
  - `tracker/items/WI-0004/artifacts/plan.md` (the ten steps and four assumptions), `artifacts/impl-report.md` (read after the criteria, to compare rather than to rely on), `history.md`
  - `tracker/items/WI-0001/item.md` — AC3 and AC6 verbatim, because WI-0004 AC12 has them as its subject
  - `tracker/project.yaml`; `docs/process/using-recall.md` v6 and `docs/architecture/overview.md` v6
  - the code on branch `wi/WI-0004` at **ffef942134b0c6e3304a417e51bacfc43ddb2b15**: `recall/cli.py`, `recall/deck.py`, `tests/test_delete.py`, and the whole `main..HEAD` diff
- **Decisions:**
  - **Every criterion was decided from a command run here, not from the report.** Twelve cases were built by hand — `recall add`/`recall list` for the ordinary decks, a written deck file for the ones needing particular `rung` and `due` values — with `HOME` in a fresh temporary directory per case and `sha256sum` for every "bytes identical" clause.
  - **AC12 was read, not run.** It names `WI-0001` AC3 and AC6 by ID, so each got its own verdict read from its own sentence against this item's behaviour, with the tests as evidence for that reading. Both are still true. **Non-intersection does not exist here** and that is stated in the report: two executable cases exercise `recall delete` and the listing together, so nothing had to be waived.
  - **BUG-0001 extends to `delete`, and that is not this item's failure.** With the deck path existing as a directory, `recall delete` exits 1 with an `IsADirectoryError` traceback. AC8 governs a file that cannot be read *as a deck* — `DeckUnreadable` — and that path passes. The classification test in the procedure gives "bug, not send-back", and the bug already exists with this exact scope, so **no new bug item was filed**; the observation is recorded in `verify-report.md` for whoever plans BUG-0001, rather than by editing another item's artifact.
  - **No criterion was judged ambiguous**, so no question was raised. AC12's "settled by reading" clause was the only one at risk, and it names what to read.
  - **Three mutations of my own were run**, not the two the implementation report describes, because a sensitivity check that reuses the developer's mutations checks the developer's choice of mutation.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 55 tests in 8.427s`, `OK`) on `ffef942`
  - `python3 -m compileall -q recall tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (6 items, 12 documents, 0 errors, 0 warnings)
  - AC1/AC2 — three `recall add`, `printf 'y\n' | recall delete --question "der Hund"` → 0, then `recall list` in a new process → 0, `grep -c "der Hund"` → `0`
  - AC3 — deck written with X today, Y today+7, Z today; two deletes → 0, 0; `recall review` from a here-document → 0, only `Z question` on stdout
  - AC4 — `recall delete --question "die Katzen"` → **2**, stderr `no card has the question 'die Katzen'`, sha256 unchanged
  - AC5 — duplicated `der See`; delete → **2**, stderr `2 cards have the question 'der See'`; and a three-way duplicate → stderr `3 cards`
  - AC6 — four runs with `n`, `maybe`, an empty line and `< /dev/null` → 0, 0, 0, 0; one `[y/n]` each; `Not deleted.` each; no `Traceback`; sha256 unchanged each
  - AC7 — four blank forms → **2** each, `--question` named on stderr, no prompt, sha256 unchanged; then the same four with no deck → **2** each, `find $HOME -type f` → `0`
  - AC8 — `not json at all` and a truncated document → **3** each, the deck path named on stderr, sha256 unchanged
  - AC9 — empty `HOME` → **2**, deck absent, parent absent, `$HOME/.local` absent
  - AC10 — delete the only card → 0 (`holds 0 card(s)`), `recall list` → 0 with the empty-deck line, deck file `{"version": 1, "cards": []}`, `recall add` → 0 and the card listed
  - AC11 — written deck with rungs 0/2/3; delete the middle → 0; parsed comparison → `version same: True`, `entries identical …: True`, `order: ['first', 'third']`, `any grade key added: False`
  - AC12 — `recall list | cat -A` after a deletion → `Der  Bahnhof | The  Station$`, `das Pferd | the horse$`, exit 0; deck emptied by deleting → empty-deck line, exit 0; `python3 -m unittest …test_listing_is_unchanged_by_a_deletion …test_deleting_the_last_card_leaves_an_empty_deck -v` → 0 (`Ran 2 tests`, `OK`)
  - beyond the criteria — ` Y ` deletes (exit 0), `yes` cancels (exit 0), confirming `plan.md` assumption 1 and the sentence `docs/process/using-recall.md` v6 prints
  - BUG-0001's class against `delete` — deck path made a directory → exit **1**, `IsADirectoryError` traceback
  - sensitivity — three mutations, each `python3 -m unittest tests.test_delete` → 1, each reverted; `git status --short recall/` → empty; full suite re-run → 0
- **Gates:**
  - `tests-pass` → **pass** (exit 0 on the branch head `ffef942`, 55 tests)
  - `lint-clean` → **pass** (`compileall` exit 0)
  - `workspace-valid` → **pass** (0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md`'s table gives a command and its real output for each of AC1–AC12; no row cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (no match, two matches, three matches, four cancelling replies, four blank forms with and without a deck, a malformed deck, a truncated deck, an absent deck with an absent parent, and the empty deck a deletion leaves — all triggered)
  - `a-criterion-about-criteria-is-read` → **pass** (AC12: `WI-0001` AC3 and AC6 named by ID, each with a verdict read from its sentence, tests cited as evidence, non-intersection stated as absent with the two covering cases named)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (substring matching → AC4's test fails; confirmation ignored → AC6's four sub-tests fail; survivors reversed → AC11's three and AC12's fail)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` (new), carrying `Verified-commit: ffef942134b0c6e3304a417e51bacfc43ddb2b15`
  - `tracker/items/WI-0004/item.md` — AC1 to AC12 all ticked, each against a command in the report
  - no bug item filed (see Decisions)
- **Status:** `verifying` → `in-review`
- **Result:** WI-0004 passes on all twelve criteria, checked independently against `ffef942`: a card is named by its exact question side, both sides are shown, the prompt is asked once, only a yes removes anything, and every refusal leaves the deck byte-identical. The one defect found belongs to BUG-0001, which already covers it.

## 2026-08-30T04:59:51Z — review-close v0.6.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next` (medium, created 01:37:52Z, ahead of BUG-0001's 02:07:30Z)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (8 rows), `journal.md` (8 entries, read in full), `questions/Q-001.md` and `Q-002.md` including their `## Consequences`
  - `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md` — including `## What I did not do` and `## Not verified, and why`
  - the diff `main..wi/WI-0004`, hunk by hunk: `recall/deck.py`, `recall/cli.py`, `tests/test_delete.py`, `docs/process/using-recall.md`, `docs/architecture/overview.md`
  - `docs/architecture/adr/ADR-0009-confirming-a-deletion.md` in full; `ADR-0001` §Decision; `WI-0001` AC3, AC6, AC8, AC9; `WI-0002` AC7 — each opened because a claim cited it, not quoted from memory
  - `tracker/project.yaml`
- **Decisions:**
  - **Accepted and closed as `delivered`.** Every hunk traces to a plan step or a declared deviation; nothing contradicts an ADR; `recall/store.py` is untouched, which is the plan's central claim standing up.
  - **F1, a false claim, repaired here rather than sent back.** `docs/architecture/overview.md` said the load path serves *"`add`, `list` and, later, `review`"* — stale since WI-0002, carried forward by WI-0003's review as outside its scope, and made staler by this item, whose `cmd_delete` is a fourth caller. That put it inside **this** item's D12 scope. Repaired in place to name all four subcommands, citing `recall/cli.py`; overview to **v7** with a change-log row. Documentation, one clause, and the project has the precedent (`using-recall.md` v2, a review correcting a citation in place) — a send-back would have cost an implement-verify-review cycle for a sentence.
  - **F2, three over-width prose lines** (160, 115 and 111 characters where both files otherwise keep ≤ 100), re-wrapped in the same v7 bumps. No claim changed, and the change-log rows say so.
  - **F3, `verify-report.md`'s `Verified-commit:` line did not parse** — `Verified-commit: <sha> (branch …)` — and `check-verify-freshness` matches the sha to end of line, so it reported the line as missing, which is the same message it gives a report that names nothing. The sha was right and the verification genuinely current, so this was a formatting defect and not a stale verification: the branch name was moved to its own line and the report says what changed. **Recorded as a toolkit finding too:** `verify` prescribes that line but runs no gate that parses it, so a malformed one survives to the next skill and presents as a D10 failure.
  - **No send-back and no new bug.** The one defect reproduced — `recall delete` exiting 1 with an `IsADirectoryError` traceback when the deck path is a directory — is BUG-0001's class, already filed with that scope; the classification test gives "bug, not send-back", and the bug exists. What is new is that its fix now covers four subcommands, which is written into `item.md` `## Notes`.
  - **Four gaps accepted**, each written into `item.md` `## Notes` so they survive the item closing: BUG-0001's reach into `delete`; concurrency unverified; exact matching's usability cost; AC7's tab case delivered through shell quoting rather than a terminal.
  - **Merge order kept deliberately**: trial-merge in a detached worktree, tests on the merge result, discard, confirm the trunk did not move, close, then merge for real. `git rev-parse main` was `152c5318…` before the trial and `152c5318…` after it.
  - **The engagement was not ended**, because `scripts/engagement-state EP-001` says so — `active`, *"still in flight: BUG-0001, WI-0004"* — not because the board looked unfinished. No sign-off is due.
- **Cross-answer check:** no sentence carrying a stakeholder answer's citation was rewritten by this execution, so there is nothing of theirs to reconcile. The two edits made here are F1 — a sentence about `store.py`'s load path that cited nothing and now cites `recall/cli.py` — and F2's re-wraps, which moved line breaks and no words. The stakeholder's two answers on this item were consumed upstream and were **read** here rather than edited: `WI-0004/Q-001` (*"B — let me just type the question"*) against `cmd_delete`'s exact match and its refusal naming the count, and `WI-0004/Q-002` (*"B — show me the card and ask first"*) against `ADR-0009` and the single-read confirmation. Both are honoured as given and neither conflicts with the other or with `EP-001/Q-001`'s standing deferral over wording. `lint-answers --changed-since main` → exit 0 over a window it reported as *"2 path(s) differ from main (152c531) under docs"*, so the window could have found something.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0 (*"all 4 commit(s) on main..wi/WI-0004 name WI-0004"*)
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 1 first (`Verified-commit` line unparseable — F3), then 0 after the repair: *"verified at ffef9421; wi/WI-0004 has moved to 3b80a6bc but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0, scope quoted from the tool: *"2 document(s) in 2 path(s) differ from main (152c531) under docs; citations: every markdown file in the workspace"*
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0 (*"claim window: 2 path(s) differ from main"*, 9 consumed human answers checked)
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → 0, *"EP-001 active — still in flight: BUG-0001, WI-0004"*
  - `git rev-parse main` → `152c5318bfecf20c1f6044648f9714c1b8c3d449` (before the trial)
  - `git worktree add --detach /tmp/wi4-trial main` → 0; `git -C /tmp/wi4-trial merge --no-ff wi/WI-0004` → 0; `git -C /tmp/wi4-trial rev-parse HEAD` → `04c5a38fc594496f504c4a238939af243032aca2`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → 0 (`Ran 55 tests in 8.525s`, `OK`); `python3 -m compileall -q recall tests` there → 0
  - `git worktree remove --force /tmp/wi4-trial` → 0; `git rev-parse main` → `152c5318…`, unchanged
  - `python3 -m unittest discover -s tests -t . -q` on the branch after the two document repairs → 0 (55 tests, OK)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (6 items, 12 documents, 0 errors, 0 warnings)
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each with its own result and evidence in `review.md`'s table; D12 passes after F1's repair)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; only `tracker/` and `docs/` moved since `ffef942`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 4 commits)
  - `tests-pass-on-the-merge-result` → **pass** (55 tests OK inside the detached trial worktree at `04c5a38`, plus `compileall` exit 0 there)
  - `workspace-valid` → **pass** (0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** (8 history rows, 8 journal entries, both questions answered with real `## Consequences`; `plan.md`, `impl-report.md`, `verify-report.md` and `review.md` present; `git log --grep WI-0004` returns the item's whole story — refinement, plan, code, record and merge)
  - `claims-are-sourced` → **pass** (`lint-claims --context work-item --changed-since main` exit 0 over the scope quoted above, and the ten-claim audit read from the cited sources, one of which failed and was repaired)
  - `cross-answer-consistency` → **pass** (`lint-answers` exit 0; see the Cross-answer check bullet)
  - `epic-sign-off` → **not applicable this execution** — `engagement-state EP-001` reports `active` with BUG-0001 still in flight, so the engagement is not at rest and no sign-off is due
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` (new)
  - `tracker/items/WI-0004/item.md` — `status: done`, `outcome: delivered`, and four accepted gaps plus the two document repairs written into `## Notes`
  - `tracker/items/WI-0004/artifacts/verify-report.md` — `Verified-commit:` line reformatted (F3), sha unchanged
  - `docs/architecture/overview.md` v7 (F1, F2) and `docs/process/using-recall.md` v7 (F2)
  - the merge of `wi/WI-0004` into `main`, made after this close, and named in the commit that follows this entry
  - no bug item filed, and no question
- **Status:** `in-review` → `done`
- **Result:** WI-0004 is accepted and closed as delivered. `recall delete` names a card by its exact question side, shows both sides, asks once, removes only on a yes, and leaves the deck byte-identical on every refusal — verified independently, and the merge result passes the suite. Three findings were repaired in review rather than sent back, four gaps are recorded in the item, and the engagement stays open with BUG-0001 the last item in flight.
