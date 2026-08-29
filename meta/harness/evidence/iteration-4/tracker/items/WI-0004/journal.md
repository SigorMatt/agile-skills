# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-29T13:21:07Z — answer-questions v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** not dispatched — this item did not exist. It was created by this execution of
  `answer-questions` on `EP-001` (status `awaiting-answer`), because the stakeholder's answer to
  `EP-001/Q-005` widened the scope and no item recorded the work (SKILL.md step 3b;
  `spec/ids-and-statuses.md` §5).
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` — the sign-off question and the stakeholder's answer
  - `tracker/items/EP-001/item.md` — `## Out of scope`, which had reserved exactly this case
  - `docs/product/vision.md` (v2, now v3)
  - `docs/architecture/adr/ADR-0004-card-store-schema-and-write-protocol.md` (v1) — the store
    schema and the next-card-number rule
  - `docs/architecture/adr/ADR-0007-scheduling-state-as-an-interval-in-days.md` (v1) — the
    per-card scheduling fields a deletion has to leave alone
  - `docs/architecture/overview.md` (v3)
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — what `add`, `list` and
    `review` already promise about card numbers and about reading a plain input stream
- **Decisions:**
  - Filed the work as a `work-item` at `draft` under `EP-001` rather than as an amendment to any
    delivered item. Rationale: SKILL.md step 3b forbids widening an existing item to swallow new
    work, and all three siblings are `done`; a new item is the only way the board shows the scope
    change to the person who asked for it.
  - Wrote four acceptance criteria as a **draft** and said so in the body. Rationale: they are not
    yet decidable by someone with a terminal and no context — AC1 does not name the command or how
    a card is identified — and pretending otherwise would hand `refine` a passing item that has
    not met the Definition of Ready. `refine` owns that, not this skill.
  - Recorded the three things the stakeholder declined in `## Out of scope` with their words
    attached, rather than leaving them out. Rationale: "editing can wait" is a decision with a
    date on it, and an exclusion nobody can trace becomes a re-litigation later.
  - Recorded in `## Notes` that `ADR-0004`'s option F weighed card-number reuse as low risk
    *because nothing in the epic deleted a card*, and that this item removes that premise — but
    left `ADR-0004` itself unedited. Rationale: `spec/doc-header.md` §5 says an ADR is updated
    "superseded only", and §4 says an ADR preserves what was believed at the time. The premise is
    flagged where `plan` will actually read it, in the item it constrains.
  - Priority `medium`, not `high`. Rationale: the stakeholder called it the thing they want next,
    and also said the engagement is what they asked for; nothing is broken and nobody is blocked
    on it.
- **Questions raised:** none — the four open decisions are recorded in `## Notes` for `refine` to
  put to the stakeholder, which is where the Definition of Ready puts them.
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0004 --type work-item --title "Delete a card
    that was added by mistake" --epic EP-001 --priority medium --status draft --actor
    answer-questions --arose-from EP-001/Q-005 --reason "..."` → exit 0, created WI-0004 at draft
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, 3 errors, all three
    expected mid-execution (stale board; EP-001 still at `awaiting-answer`; this entry missing)
- **Gates:** this execution's gates are evaluated once, on `EP-001`, where the question was
  answered; they are listed in full in `tracker/items/EP-001/journal.md` for the same timestamped
  execution. The two that bear on this file:
  - `answer-is-propagated` → **pass** (this item is the first file named in `Q-005`'s
    `## Consequences`, and it exists with the follow-up the stakeholder named in it)
  - `workspace-valid` → **pass** (recorded on `EP-001`, after this entry and the epic's
    transition; see that entry for the final run)
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new) — story, four draft acceptance criteria, three recorded
    exclusions, and the four questions `refine` must settle
  - `tracker/items/WI-0004/history.md` (new) — the creation row, actor `answer-questions`
  - `tracker/items/WI-0004/journal.md` (new) — this entry
- **Status:** `draft` → `draft` (unchanged)
- **Result:** WI-0004 exists at `draft`: the one follow-up the stakeholder named when they
  accepted EP-001 — deleting a card added by mistake. It is not Ready and does not claim to be;
  `refine` is the next thing that should touch it.

## 2026-08-29T13:26:42Z — refine v0.2.2 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` — the only runnable candidate on the board
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (one row: created at `draft` by
    `answer-questions`, so this is a **fresh** draft and not an item sent back from a later
    stage), `journal.md`
  - `tracker/items/EP-001/questions/Q-005.md` — the answer that created this item, and the three
    things the stakeholder declined in it
  - `tracker/items/EP-001/item.md` — the epic's amended `## Scope` and `## Out of scope`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md`,
    `tracker/items/WI-0002/artifacts/refinement-qa.md`,
    `tracker/items/WI-0003/artifacts/refinement-qa.md` — for the standing deferral on
    `WI-0001/Q-002` and, more importantly, for where two earlier refinements drew its boundary
  - `tracker/items/WI-0001/item.md`, `WI-0002/item.md`, `WI-0003/item.md` — the criteria style
    the verifier on this project is used to, and the argument-count precedent in `WI-0001` AC9
  - `docs/product/vision.md` (v3), `docs/architecture/overview.md` (v3)
  - `docs/architecture/adr/ADR-0004` (store schema, write protocol, next card number),
    `ADR-0005` (command surface, exit codes, streams, the listing), `ADR-0007` (scheduling state)
  - `README.md` — the `## Commands` section and how `review` reads whole lines
  - `.claude/agile-skills/spec/dor-dod.md` §1, `question.md`, `work-item.md`
- **Decisions:**
  - **Filed exactly one question to the stakeholder, and decided seven things without them.**
    `Q-001` asks whether deleting confirms first. The addressee test in step 3 was applied to
    every gap in order and is written out per-gap in `artifacts/refinement-qa.md`; the summary is
    that the confirmation is the only gap with product stake, because it is an interaction the
    user performs every time and the right answer differs by who they are. Deciding it under the
    `WI-0001/Q-002` deferral would have stretched a deferral about naming and file layout over an
    interaction — the same line `WI-0003`'s refinement drew when it refused to decide the
    ladder's starting point under it.
  - **Rewrote the four draft criteria into ten.** `AC1` gains a concrete store (cards 1, 2, 3),
    a concrete command (`recall delete 2`), an exit code and a later-run observation; the old
    AC1 named no command at all. `AC3` (was AC4) states what "untouched" means as five named
    fields in the store file, because "leaves the schedule as it was" is not something a verifier
    can check. `AC5`, `AC6`, `AC8` and `AC9` are new and cover the failure modes: a number that
    names no card, no store at all, four wrong command lines, and a store that is not valid JSON.
    `AC7` is new: deleting the last card must leave a store the tool still reads. `AC10` is new
    and names `README.md`, following `WI-0001` AC5 and `WI-0003` AC4.
  - **`AC5`, `AC6` and `AC8` say "exits non-zero" rather than naming a code.** Rationale:
    `ADR-0005` assigns `2` to a malformed command line and `1` to a good command line against an
    unusable store, and `recall delete 9` against a readable store is neither; choosing between
    them is `plan`'s job and may need `ADR-0005` extending. "Non-zero" is still decidable, and
    `WI-0001` AC9 set the precedent of stating it that way.
  - **`AC2` is left as an explicit placeholder naming `Q-001`.** Rationale: writing a plausible
    confirmation behaviour now and letting the stakeholder correct it later is exactly the
    "politely accepting a vague answer and writing a criterion anyway" failure in this skill's
    self-check, and the item would look Ready while the disagreement waited for `verify`.
  - **Routed three design questions to `plan` in `## Notes` instead of asking.** Whether a
    deleted card's number is ever reused (`ADR-0004` F against G, on the premise this item
    removes); the specific exit code above; and whether the store `version` changes. Each is
    named with `refine` recorded as who left it open, which is what R10 asks for — the point is
    that the gap is findable, not that it is decided.
  - **Recorded "a deletion is final" as an assumption in two places**, `## Out of scope` and
    `Q-001`'s context. Rationale: it is the weakest of the seven unasked decisions — nobody
    declined undo, it simply was never requested — so the stakeholder gets to see it while
    answering the question it bears on, rather than discovering it after the code exists.
  - **Sought no Definition of Ready override.** An override is the stakeholder's to offer, and
    they are not here; assuming one would be `refine` passing its own item.
- **Questions raised:** `Q-001` (blocking, to `human`) — whether `recall delete` confirms before
  deleting. One question, one decision, and `## Context` says it is the only one this round.
  Nothing is left `[unresolved]` except that question itself.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, 2 errors, both expected
    mid-execution: `board.stale`, and `question.blocking.not-suspended` on this item — the second
    being precisely the suspension this transition performs
  - `python3 .claude/agile-skills/scripts/board-gen .` → run after the transition
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, run by `transition` against the
    resolving move and again after it)
  - `definition-of-ready` → **fail**, criterion by criterion, and the full table with evidence is
    in `artifacts/refinement-qa.md`. `R1 pass` (frontmatter complete, `arose-from` resolves),
    `R2 pass` (role, capability, "so that" outcome), `R3 pass` (ten labelled checkboxes),
    **`R4 fail`** (`AC2` is a placeholder naming `Q-001`; the other nine each name a command and
    an observation), `R5 pass` (five exclusions, including editing and undo), **`R6 fail`**
    (`Q-001` is open and blocking), `R7 pass` (no `depends-on`; all three siblings `done`),
    **`R8 fail`** (`refinement-qa.md` declares `status: agenda`, because the conversation has not
    happened), `R9 pass` (one command, one code path, one README section), `R10 pass` (no options
    and no modes; the argument shapes are covered by `AC1`, `AC5`, `AC6`, `AC8`, `AC9`, and the
    two behaviours left unconstrained are named in `## Notes` with who left them so). Three fails,
    one cause: `Q-001` is unanswered.
  - `criteria-are-decidable` → **fail on `AC2` only**, which is why the item is not moving to
    `ready`. For the other nine, the command and the verdict are named in the criterion itself:
    `AC1` `recall delete 2` then `recall list`; `AC3` diff the store's five named fields per card;
    `AC4` `recall delete 1` then `recall review`; `AC5` `recall delete 9` and compare the file
    byte-for-byte; `AC6` `recall delete 1` with no file and check none appears; `AC7`
    `recall list` and `recall add` after emptying the pile; `AC8` four invocations, each exit
    non-zero with a usage line; `AC9` a non-JSON file, unchanged after the attempt; `AC10` open
    `README.md`.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` holds the question as it was
    filed and every decision taken instead of asking, each tagged `[assumed]` with the deferral,
    ADR or precedent it rests on, and `Q-001` tagged `[unresolved]`. Nothing is paraphrased into
    agreement, and no answer is recorded from a stakeholder who has not replied — the file
    declares `status: agenda` for exactly that reason.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — criteria rewritten from four to ten, `## Out of scope`
    extended to five entries, `## Notes` rewritten with the three questions routed to `plan`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new) — `status: agenda`, the round-1
    question with the addressee test written out, seven unasked decisions with their authority,
    and the per-criterion Definition of Ready table
  - `tracker/items/WI-0004/questions/Q-001.md` (new) — blocking, to `human`
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0004 is not Ready and says exactly why: R4, R6 and R8 fail, all three because
  `Q-001` is unanswered. Everything that did not need the stakeholder is decided and written
  down — ten criteria, five exclusions, three design questions handed to `plan` — so when the
  answer arrives, round 2 has one criterion to write.

## 2026-08-29T13:30:20Z — answer-questions v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer` with `Q-001` open, `addressed-to: human` and its `## Answer` now filled in — the stakeholder replied between turns. Dispatched ahead of `next`, which stops the loop on any open human-addressed question.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` (the only question on the item; answer present)
  - `tracker/items/WI-0004/item.md` (AC1–AC10, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0004/history.md` (both rows; `resume-to: draft` on the suspending row)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (`status: agenda`, round 1, the DoR table)
  - `docs/architecture/adr/ADR-0005-command-surface-and-entry-point.md` (v1) — checked for a conflict with the chosen behaviour
  - `docs/architecture/adr/` listing — ADR-0001..ADR-0007, to confirm no recorded decision covers confirmation before a destructive command
  - `tracker/board.md`
- **Decisions:**
  - **`Q-001` answered by the human, route 4 consumed rather than route 3.** The reply chooses option C — *"just delete it and tell me what got deleted. I'm only ever going to run this right after I typo'd something, I don't need a prompt in my way for that."* That is a decision, not a deferral: it names an option and gives the reason. `answer-questions` decided nothing here; it propagated.
  - **AC2 written as a stdin-closed check rather than as prose.** `recall delete 2 < /dev/null` exits 0 without waiting, and the one stdout line carries the number and both card sides. Rationale: "never prompts" is not observable, but "does not block on a closed stdin" is, and it is the property the answer actually bought. It also keeps the item's stated rule that every criterion is decidable from a script, which `WI-0002` AC9 set for `recall review`.
  - **The exact wording of the deleted-card line is left to `plan`/`implement`, not fixed in AC2.** AC2 constrains what the line must contain — the number and both sides — because that is what option C is. The formatting is naming and wording, the category the stakeholder handed over on `WI-0001/Q-002`, and pinning it here would spend their deferral on nothing.
  - **No ADR written.** Route 3 was not taken, so there is no new architectural decision to record; the choice is a stakeholder preference about output, already recorded verbatim in `Q-001` and now in the criteria. `ADR-0005` fixes the argument surface and the stream split and is untouched and uncontradicted. Writing an ADR for a question the human answered would misattribute the decision.
  - **The three design questions in the item's `## Notes` are left open for `plan`.** Number reuse, the exit code for a number naming no card, and whether the store `version` changes are unaffected by this answer, and `refine` routed them deliberately.
  - **`refinement-qa.md` keeps `status: agenda` and its round-1 DoR verdicts.** Round 1's Q1 is updated to `[human]` with the answer quoted, because leaving it `[unresolved]` would make the record disagree with itself. Setting `recorded` and re-assessing R4/R6/R8 is `refine` round 2's job — this skill returning the item to `draft` is what dispatches that.
  - **The undo assumption is recorded as still an assumption.** The stakeholder saw it in `Q-001`'s context and did not object, and their reason explains why it does not bite for them, but they were not asked to rule on it. `## Out of scope` now says exactly that, and no more.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, before the transition: `board.stale` and `question.awaiting.none-open` on WI-0004 — both are the state this execution's transition resolves
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-29T13:28:57Z, the clock reading stamped as `answered-at`
- **Gates:**
  - `answer-is-propagated` → **pass** — `Q-001`'s `## Consequences` names two files and both were opened and checked after editing: `item.md` now carries the rewritten AC2 (verified by reading lines 18–40; the `**pending Q-001**` placeholder is gone) and the replaced pending-criterion note and `## Out of scope` entry; `refinement-qa.md` now carries the `[human]` answer and the superseded-header note.
  - `answered-from-the-record` → **pass** — the answer follows from the human's own reply quoted verbatim in `Q-001` `## Answer`; the supporting reasoning cites `ADR-0005` (argument surface unaffected) and `WI-0002` AC9 (script-drivable criteria). Nothing was inferred where the record was silent.
  - `escalation-is-justified` → **skipped** — nothing was escalated. `Q-001` was already the escalation and it has been answered; no question was re-addressed to the human.
  - `a-deferral-is-not-an-answer` → **pass** — the reply is not a deferral. It names one of the three offered options by letter and gives the reason for it, so move 1 of step 3a does not apply either: nothing had to be decided under a deferral.
  - `item-resumed-correctly` → **pass** — the suspending row (2026-08-29T13:26:42Z, `draft → awaiting-answer`, actor `refine`) records `resume-to: draft`, and this execution moves the item to `draft`. Not to `ready`: three DoR criteria are recorded as failing and only `refine` may re-assess them.
  - `workspace-valid` → **pass** — re-run after the transition and after `board-gen`, exit 0. The two pre-transition errors were `question.awaiting.none-open` (the item was awaiting an answer that had arrived) and `board.stale`.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, `answered-at: 2026-08-29T13:28:57Z`, `answered-by: human`; `## Consequences` written, naming both propagation targets and stating that no ADR was written or superseded
  - `tracker/items/WI-0004/item.md` — AC2 replaced with a decidable check; the "one criterion is not settled yet" note replaced by what was settled; the undo entry in `## Out of scope` records that the stakeholder saw the assumption and why it does not bite
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — round 1 Q1 moved from `[unresolved]` to `[human]` with the answer quoted; the header records that the file stays `agenda` and that its DoR verdicts are round 1's and superseded at round 2
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's answer to `Q-001` — delete immediately, print both sides, no prompt — is in AC2 as a check a script can run, and WI-0004 is back at `draft` for `refine` round 2 to close out R4, R6 and R8. No ADR was needed and no question remains open anywhere in the workspace.

## 2026-08-29T13:32:31Z — refine v0.2.2 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` — the item returned here from `awaiting-answer` when `answer-questions` propagated the stakeholder's reply to `Q-001`. Round 2, a send-back with one named defect, not a fresh draft.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` (AC1–AC10, `## Story`, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0004/history.md` — three rows; the row that returned the item names what was outstanding, which is what scoped this round
  - `tracker/items/WI-0004/journal.md` — round 1's `refine` entry and `answer-questions`' entry, read so round 1's decisions were not re-taken
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (`status: agenda`, round 1 and its DoR table)
  - `tracker/items/WI-0004/questions/Q-001.md` — the stakeholder's answer verbatim, and its `## Consequences`
  - `.claude/agile-skills/spec/dor-dod.md` §1 — R1..R10, walked criterion by criterion
- **Decisions:**
  - **No question was filed and none should have been.** The addressee test in step 3 was applied to the one thing round 2 touched. `AC2`'s *behaviour* was the stakeholder's and they decided it; `AC2`'s *phrasing* is not, and asking them to draft a criterion would tell them their answer was not heard (F-023). Nothing else in the item changed, so nothing else could have needed asking.
  - **`AC2` rewritten to pin both output streams.** `answer-questions` had it as "exits 0 with nothing on stdin, and the one stdout line contains both sides and the number" — faithful to the answer, but satisfiable by an implementation that prints a prompt, reads end-of-file and treats that as a yes. That implementation is exactly what *"I don't need a prompt in my way"* rules out, so the criterion now requires stderr empty **and** stdout exactly one line. A prompt has to be visible somewhere; with both streams pinned there is nowhere for it to be. Recorded `[assumed]` under the standing deferral on `WI-0001/Q-002`, and `AC5` already uses the same stream-pinning idiom, so this is the item's existing construction rather than a new one.
  - **The wording of the deleted-card line stays out of `AC2`.** The criterion says what the line must contain — the number and both sides — and not how it reads. Output wording is the category the stakeholder handed over, and spending their deferral on a format string buys nothing.
  - **The other nine criteria were re-read but not rewritten.** The history names one defect; re-opening settled criteria is the second failure mode this skill's procedure warns about, and it would also risk producing criteria that no longer match what round 1 recorded the stakeholder agreeing to.
  - **The three design questions in `## Notes` stay routed to `plan`.** Number reuse after a deletion, the exit code for a number that names no card, and whether the store `version` changes are unaffected by the answer. R10 wants them visible, not decided, and they are.
  - **`refinement-qa.md` moves to `status: recorded`, and round 1's DoR table is left standing.** It recorded three failures that were real at the time. Round 2 appends its own table rather than editing the old one, so a reader sees the sequence instead of a tidied result.
- **Questions raised:** none. Round 1's `Q-001` is answered and closed; `refinement-qa.md` holds both rounds, with the stakeholder's answer verbatim under round 1 and nothing left `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 9 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → board already current
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0)
  - `definition-of-ready` → **pass**, criterion by criterion. R1 pass `[auto]` (frontmatter complete: `type`, `epic`, `priority`, `arose-from`). R2 pass `[skill]` (role, capability and "so that" outcome, unchanged from round 1). R3 pass `[auto]` (ten `AC<n>` checkboxes). **R4 fail → pass**: the failure was `AC2` alone, a placeholder naming `Q-001`; it now names a command, an exit code and three observations, and the other nine were each re-read against the observation test. **R6 fail → pass** `[auto]`: `Q-001` is `answered`, and no question is open on this item or anywhere in the workspace. R5 pass `[skill]` (five exclusions, including editing a card and undoing a deletion). R7 pass `[auto]` (no `depends-on`; three siblings `done`). **R8 fail → pass** `[auto]`: `refinement-qa.md` now declares `status: recorded` and holds both rounds with every answer tagged. R9 pass `[skill]` (one command, one code path, one README section). R10 pass `[skill]` (no options or modes; the argument shapes are covered by AC1, AC5, AC6, AC8, AC9, and the two deliberately unconstrained behaviours are in `## Notes` naming `refine` as who left them open). The full table with evidence is at the foot of `artifacts/refinement-qa.md`. No override sought; none needed.
  - `criteria-are-decidable` → **pass**, each named with what settles it. AC1: run `recall delete 2` on a three-card store, then `recall list` — exit 0, one stdout line, listing shows 1 and 3. AC2: `recall delete 2 < /dev/null` — exit 0, stderr byte-empty, `wc -l` on stdout is 1, that line contains `2` and both of card 2's sides. AC3: diff the store's card objects before and after — cards 1 and 3 identical in `number`, `question`, `answer`, `due`, `interval`. AC4: `recall delete 1` then `recall review` — the nothing-is-due line, exit 0. AC5: `recall delete 9` — non-zero exit, stderr names `9`, stdout empty, store file bytes unchanged. AC6: no store file, `recall delete 1` — non-zero, stderr non-empty, no file created. AC7: delete the last card, then `recall list` (nothing-stored line, exit 0) and `recall add` (exit 0). AC8: four invocations, each non-zero with a usage line on stderr and the store bytes unchanged. AC9: point `RECALL_FILE` at a non-JSON file, `recall delete 1` — non-zero, stderr names the path, file bytes unchanged. AC10: open `README.md`, find `## Commands`, compare the `delete` entry against the `add`, `list` and `review` entries and confirm it states what happens when the number names no card.
  - `qa-recorded-verbatim` → **pass** — `refinement-qa.md` carries round 1's question and the stakeholder's reply word for word (*"C — just delete it and tell me what got deleted. I'm only ever going to run this right after I typo'd something, I don't need a prompt in my way for that."*) tagged `[human]`, seven round-1 `[assumed]` decisions each naming the deferral or record it rests on, and round 2's single `[assumed]` decision. Nothing was paraphrased into agreement and nothing is left `[unresolved]`.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — `AC2` rewritten to pin stderr empty and stdout to exactly one line
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; round 2 section added (why nothing was asked, what changed in `AC2` and why) and the re-assessed R1–R10 table appended below round 1's, which is left as written
- **Status:** `draft` → `ready`
- **Result:** WI-0004 is Ready. The one thing outstanding was `AC2`, and the stakeholder's answer settled it; `refine` pinned both output streams so the absence of a prompt is observable rather than asserted, and all ten Definition of Ready criteria now pass with no override. Three design questions — number reuse, the exit code for an unknown number, and the store `version` — are recorded as `plan`'s to settle.

## 2026-08-29T13:38:16Z — plan v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** status `ready`, dispatched by `next` — the only runnable candidate; `refine` passed all ten Definition of Ready criteria in round 2.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC10, `## Out of scope`, and the three design questions `## Notes` routes here
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — both rounds; the seven `[assumed]` decisions and the standing deferral each rests on
  - `tracker/items/WI-0004/questions/Q-001.md` — the stakeholder's choice of option C, verbatim
  - `tracker/items/WI-0004/history.md`, `journal.md` — a first plan, not a re-plan; no rejection to read
  - `docs/architecture/overview.md` (v3) — the three responsibilities, the stream rule, and the store-stays-in-`recall.py` decision
  - `docs/architecture/adr/ADR-0004` — the schema, the write protocol, options F and G on card numbering, and the store-failure cases
  - `docs/architecture/adr/ADR-0005` — the entry point, positional-only arguments, the exit-code scheme, the stream split
  - `docs/architecture/adr/ADR-0007` — the version-3 shape and the strict validation of `due` and `interval`
  - `tracker/project.yaml` — `commands.test` and `commands.lint`, both already set
  - `recall.py` (412 lines) — `load`, `save`, `add_card`, `due_cards`, `cmd_add`, `cmd_list`, `cmd_review`, `main`, and the `USAGE_*` constants
  - `tests/support.py`, `tests/test_docs.py`, `tests/test_review.py` — the `CommandTestCase` harness, the README assertions, and a check that no test pins the top-level `USAGE` string
  - `README.md` — `## Commands`, `## Exit codes`, `## Where your cards are kept`, `## Not yet built`
- **Decisions:**
  - **`ADR-0008` — a deleted card's number may be reused; `ADR-0004`'s option F stands.** Route: decided. `ADR-0004` chose F on the premise *"nothing in the epic deletes a card"*, and this item removes that premise, so `refine` sent the weighing back here. Re-weighed, F still wins: option G's own recorded objection — a second source of truth that can disagree with the cards after a hand edit — got **stronger** since it was written, because WI-0003 made hand-editing the documented way to move a card. G would also cost a store version 4 whose read path for existing documents would derive the counter by doing F once. A third option, tombstones, was named and rejected: it contradicts AC1 and AC3, which are checked by finding the card gone from the file. The residual risk is real and is written into the ADR and the overview as a constraint on future work — nothing that refers to a card across time may key on its number.
  - **The store schema and `STORE_VERSION` do not change.** Route: documented, from `ADR-0004` and `ADR-0007`. Deleting removes a card object and adds no field, so no shape in either ADR is different. This settles the third question `refine` routed here; folded into `ADR-0008` rather than given its own ADR, because it is a consequence of choosing F rather than a separate choice.
  - **`ADR-0009` — exit code `1` widens to "the command could not be carried out".** Route: decided. `recall delete 9` on a readable store is neither of `ADR-0005`'s failures. Three options were weighed. Returning `2` was rejected because it costs the property that `2` is decidable from the arguments alone without opening the user's data — an empty card side (already a `2`) is wrong against every store, whereas `9` is wrong only against this one and only until six more cards exist. A third code `3` was rejected as a fourth meaning in a deliberately small scheme, bought for a distinction a single-user hand-driven tool has not asked for. This extends `ADR-0005` rather than superseding it: its exit-code section names only a wrong command line and an unusable store and never contemplated this case, so no human authorisation to supersede is needed and none was sought.
  - **A missing store file and a number naming no card take one code path.** Route: documented, from `recall.py` — `load` already returns an empty document for a file that is not there, so `recall delete 1` with no store finds no card 1 and exits `1` having created nothing, which is exactly AC6. One path rather than two, matching how `list` treats a missing file as an empty pile.
  - **The order inside `cmd_delete` is fixed by the plan, not left to the developer.** Route: decided from the criteria. Validate the command line before touching the disk; refuse an unreadable store before any decision about cards; and on a number that names no card, return without calling `save`. Four of the ten criteria (AC5, AC6, AC8, AC9) are about what is *not* written, and ordering is the only thing that makes them true by construction rather than by care.
  - **Three reversible assumptions recorded rather than escalated.** Route: assumed. What counts as a card-number argument (`+1`, `01`, `1.0` are all `2`, on the precedent that `recall.py` matches review keys exactly); one save on success and none on any failure; and no count of remaining cards in the confirmation line. Each names its reversal cost in `## Assumptions` and each is one predicate or one format string.
  - **Nothing was asked of the human.** The one decision with product stake — prompt or no prompt — was already asked and answered as `Q-001`, and the wording of the new lines falls under the standing deferral on naming and output wording from `WI-0001/Q-002`. No decision here is irreversible and none depends on intent the record does not hold.
  - **The confirmation line's wording stays out of the plan.** `AC2` fixes what it must contain — the number and both card sides — and `implement` writes the string. Pinning a format here would spend the stakeholder's deferral on something no criterion checks.
  - **`docs/architecture/overview.md` bumped to v4.** The change alters the shape: a fourth command, and an exit-code meaning the document stated in its old, narrower form. A new section records that a card number is a handle rather than an identity, which is where a future reader will look for it.
  - **The README needs three edits, only one of which an AC checks.** The `## Commands` entry is AC10. The `## Exit codes` row for `1` and the `## Where your cards are kept` note on number reuse are required by D7 and D12 instead — documents the change invalidated. Both are named as a step and flagged under `## Risks`, because a hurried execution could do the AC and skip the other two and still pass verification.
- **Questions raised:** none. `Q-001` was answered before this execution began, and all three questions `refine` routed to `plan` are settled here — number reuse and the store version in `ADR-0008`, the exit code in `ADR-0009`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 first: `claim.unsourced` on ADR-0009 line 32, an absolute "never" about `ADR-0005` with no citation. Rewritten to name what `ADR-0005`'s exit-code section actually says, with `[src: ADR-0005]`; re-run → exit 0, 3 documents, 0 errors
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 11 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
  - `grep -rn "usage: recall" tests/` → one hit, `tests/test_review.py:161`, asserting `usage: recall review` only — evidence that step 1 may change the top-level `USAGE` string without breaking a delivered criterion
  - `grep -n -i "delet\|remove" README.md` → no hits; the README makes no claim about deletion that this item falsifies
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 5 items and 11 documents)
  - `every-criterion-is-addressed` → **pass** — the mapping table in `plan.md` has a row for each of AC1..AC10, each naming a step and the specific observation that settles it, not "tests". AC1→steps 2,3,4; AC2→3; AC3→2,3; AC4→3,4; AC5→3; AC6→3; AC7→2,3; AC8→3,1; AC9→3; AC10→7,8. The two pieces of the plan that map to no AC are named as such: step 6 defends `ADR-0008`, and step 7's README corrections are D7/D12 work.
  - `project-commands-resolved` → **pass** — `tracker/project.yaml` already carries `commands.test: python3 -m unittest discover -s tests -t .` and `commands.lint: python3 -m compileall -q -x '[.]claude' .`, both fixed by `ADR-0003` and both exercised by the three delivered items. Nothing needed filling in, and `## Scaffolding` is `none`: `tests/__init__.py` exists, so `unittest discover` runs against this tree as it stands.
  - `decisions-recorded` → **pass** — `plan.md`'s `## Decisions and ADRs` table lists seven choices, each with its route and its home: two ADRs (`ADR-0008`, `ADR-0009`), three reversible assumptions with their reversal cost under `## Assumptions`, one answered question (`WI-0004/Q-001`), and one covered by an existing decision (`ADR-0005` plus the standing deferral).
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0 after the one error above was fixed)
  - `plan-is-executable-without-you` (advisory) → **pass** — each step names the file it touches and what is true afterwards; `cmd_delete`'s four-part order and `delete_card`'s signature and return contract are stated, so the developer chooses implementations rather than behaviour. The one place the plan deliberately leaves a choice is the wording of the new output lines, and it says so and says why.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` (new) — problem, approach, nine steps, the AC mapping table, three assumptions, the decisions table, `## Scaffolding: none`, four risks, and out-of-scope
  - `docs/architecture/adr/ADR-0008-card-numbers-may-be-reused-after-a-deletion.md` (new, v1)
  - `docs/architecture/adr/ADR-0009-exit-code-1-means-the-command-could-not-be-carried-out.md` (new, v1)
  - `docs/architecture/overview.md` — v3 → v4, with a change-log row: the fourth command, the widened exit code, ADR-0008 and ADR-0009 in the constraints table, and the new section on a card number being a handle rather than an identity
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0004 is planned. `delete` is a fourth command in the existing shape — one pure function over the document, one command function whose ordering makes the four "nothing was written" criteria true by construction, and a registration in `main`. The two questions `refine` could not settle without an architect are now `ADR-0008` (numbers may be reused; no schema change) and `ADR-0009` (exit `1` means the command could not be carried out). No question went to the human and none needed to.

## 2026-08-29T13:40:07Z — implement v0.2.2 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next` as the only runnable item — the other three work items are `done` and EP-001 is `open` with no owner
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the ten acceptance criteria, the out-of-scope list, and the three design questions `refine` routed to `plan`
  - `tracker/items/WI-0004/artifacts/plan.md` — nine steps, the interfaces it fixes (`delete_card`, `cmd_delete`), the four-part order inside `cmd_delete`, and the AC mapping table
  - `tracker/items/WI-0004/history.md` — five rows; the last is `ready → planned` by `plan`, so this is a fresh start and no branch existed
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`; its consequence is AC2 as written in `item.md`, which is what this execution builds against
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, the `wi/` branch prefix and the commit-subject convention
  - `docs/architecture/adr/ADR-0008-*.md` and `ADR-0009-*.md` — the two decisions written for this item: numbers may be reused and the schema is unchanged; exit `1` widened to "the command could not be carried out"
  - `docs/architecture/adr/ADR-0004-*.md` and `ADR-0005-*.md` (via the plan's citations) — the write protocol and the positional-argument command surface
  - `recall.py`, `tests/support.py`, `tests/test_docs.py`, `tests/test_list.py`, `tests/test_review.py` — the shape this change has to match
  - `README.md` — the three places step 7 must edit
- **Decisions:**
  - Branched from `main` at `6e9e5cc` rather than from any of `wi/WI-0001..0003`: all three are merged, and the plan's steps are written against the trunk's `recall.py`.
  - No reconciliation was needed. `history.md`'s last row is `ready → planned`, `git branch` showed no `wi/WI-0004`, and the plan's steps are all outstanding — so this is a fresh execution, not a resumption.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0 (branch created at 6e9e5cc)
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no change has been made; the gate runs on the branch head at step 7)
  - `lint-clean` → **skipped** (not yet run, same reason)
  - `workspace-valid` → **skipped** (not yet run, same reason)
  - `every-criterion-has-a-test` → **skipped** (not yet run: no test exists yet for any of the ten criteria)
  - `commits-reference-the-item` → **skipped** (not yet run: the branch has no commits of its own)
  - `no-unplanned-scope` (advisory) → **skipped** (not yet run: there is no diff)
  - `claims-are-sourced` → **skipped** (not yet run, same reason)
- **Artifacts:**
  - branch `wi/WI-0004`, created at `6e9e5cc`, no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0004 has started on a fresh branch. Nothing is built yet; the closing entry reports the work and the gates.

## 2026-08-29T13:46:38Z — implement v0.2.2 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress` — this execution's own opening entry created the branch; no send-back and no interruption preceded it
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `artifacts/plan.md`, `history.md`, `questions/Q-001.md` — read at the opening entry and not re-read since, as nothing changed them
  - `recall.py` — the three existing commands, `load`/`save`/`add_card`, and the exactness with which the review session matches its keys
  - `tests/support.py`, `tests/test_docs.py`, `tests/test_list.py`, `tests/test_review.py` — the suite's shape, and `grep -rn "usage: recall"` to confirm nothing pins the top-level `USAGE` string that step 1 widens
  - `README.md` — the three places step 7 edits
  - `docs/architecture/adr/ADR-0008-*.md`, `ADR-0009-*.md` — the reuse decision and the widened exit code, both executed as written
- **Decisions:**
  - The confirmation line is `Deleted card <n>\t<question>\t<answer>` — the number and both sides in the same tab-separated shape `recall list` prints, so a user can compare the two at a glance. Wording is `implement`'s under the stakeholder's standing deferral on naming and output wording [src: WI-0001/Q-002]; AC2 fixes only what the line must contain.
  - The not-found message is `recall delete: there is no card <n>`, on stderr, naming the number as AC5 requires.
  - Argument validation was written as a named helper `_card_number`, and against ASCII digits explicitly rather than with `str.isdigit` — `isdigit` accepts other scripts' digits and superscripts such as `²`, which `int()` then rejects, so it would have turned an AC8-shaped input into a traceback. Behaviour is exactly the plan's `## Assumptions`.
  - `cmd_delete` catches `StoreError` around `save` as well as around `load`, which the plan's four-part order does not name. `cmd_add` and `cmd_review` both do; leaving it out would make an unwritable directory a traceback rather than a message. No criterion covers it.
  - `recall.py`'s module docstring updated from three commands to four — a claim the change makes wrong, not a plan step.
  - `cmd_delete` placed after `cmd_list`, as the plan said, rather than after `cmd_review`, so that `cmd_review` and its `_await_key` helper stay adjacent.
  - After the first attempt at this transition was refused: the report's four `[src: plan.md]` markers were rewritten to `[src: tracker/items/WI-0004/artifacts/plan.md]`. A bare filename is not a workspace-relative path, so it resolved to nothing — the gate's phrase for that is "the appearance of evidence, which is worse than none", and it is right. The report's own `claims-are-sourced` line, which said the gate had nothing to check, was corrected in the same commit: only the *sourcing* rule was looking at an empty set, while the *citation* rule runs over every markdown file in the workspace whatever `--changed-since` says.
  - Decided **not** to make: whether `AC8`'s "changes nothing on disk" should also be asserted for shapes the criteria do not name (`01`, `+1`, `1.0`). The plan settled these as assumptions and they are covered by the same predicate; adding criteria for them would be editing the item, which this skill may not do.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0
  - `git commit` ×4 → 0 each (`310e8a7`, `4fce151`, `9a0db11`, `3e53444`)
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 101 tests ... OK`
  - `python3 -m compileall -q -x '[.]claude' .` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `checked 5 item(s), 11 document(s) ... 0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, `all 3 commit(s) on main..wi/WI-0004 name WI-0004` (run before the report commit; the fourth commit names the item too, and the gate re-runs on this transition)
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0 before `impl-report.md` existed; → **1** on the first attempt at this transition, with four `claim.citation.unresolved` errors against the report; → 0 again after the fix, in commit `1b1c674`
  - `.claude/agile-skills/scripts/transition WI-0004 --to verifying ...` → **1**, refused on `workspace-valid` and `claims-are-sourced`; no history row and no journal entry were written by the refused run
  - `git diff main..wi/WI-0004 --stat` → 0, 4 files, +310/−5
  - four mutation runs of `python3 -m unittest tests.test_delete` / `tests.test_docs` against deliberately broken copies → 1, 2, 1 and 2 failing cases respectively; sources restored from copies and the suite re-run green
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 101 tests, run on the branch head)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '[.]claude' .` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (impl-report.md names a test function for each of AC1–AC10; mutation runs confirmed the AC1, AC3, AC5, AC8 and AC10 tests fail when the behaviour is removed — `test_deleting_a_card_removes_it_from_the_pile` and `test_the_surviving_cards_are_untouched_and_are_not_renumbered` on the renumbering mutation, `test_a_number_that_names_no_card_is_refused_and_changes_nothing` on the save-on-not-found mutation, `test_a_wrong_command_line_is_refused_and_changes_nothing` on the loose-`int()` mutation, and both README cases on the removed-entry mutation)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0004 wi/WI-0004` exit 0, re-run by this transition over all five commits)
  - `no-unplanned-scope` (advisory) → **pass** (every hunk traced in impl-report.md `## Gates`: `recall.py` to plan steps 1–4 plus three recorded deviations, `tests/test_delete.py` to steps 5–6, `README.md` to step 7's three edits, `tests/test_docs.py` to step 8 and step 7's second half)
  - `claims-are-sourced` → **pass, at the second attempt** (`lint-claims --changed-since main` exit 0). Its sourcing rule passed over an empty set — nothing under `docs/` changed on this branch, because `plan` wrote ADR-0008, ADR-0009 and the overview bump and nothing built here contradicts them. Its citation rule did not: it failed this transition once, on four unresolvable `plan.md` citations in `impl-report.md`, which is recorded under `**Decisions:**` and fixed in `1b1c674`.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md`
  - `recall.py`, `tests/test_delete.py`, `tests/test_docs.py`, `README.md`
  - branch `wi/WI-0004`, commits `310e8a7..1b1c674` (five, `main..wi/WI-0004`)
- **Status:** `in-progress` → `verifying`
- **Result:** `recall delete <card number>` is built, tested and documented; all six hard gates and the advisory one pass on the branch head, and every one of the ten criteria maps to a named test function. Three deviations from the plan are recorded, all of them "how" rather than "what". This transition was refused once, on four unresolvable citations in the report, and the fix is commit `1b1c674`. Two things a verifier should look at rather than take on trust: AC3 is exercised only on a two-survivor store, which is how AC3 is worded but is narrower than `delete_card`'s contract; and `claims-are-sourced`'s sourcing rule ran over no documents at all.

## 2026-08-29T13:53:15Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the ten criteria, read **first** and used as the only standard; each check below was derived from a criterion's own wording before the implementation report was opened
  - `tracker/items/WI-0004/artifacts/plan.md` — the nine steps and the three assumptions, for the diff read
  - `tracker/items/WI-0004/artifacts/impl-report.md` — read after the criteria, and checked rather than trusted; one of its claims did not survive that check (finding F1)
  - `tracker/items/WI-0004/history.md` — five rows plus the two `implement` moves
  - `.claude/agile-skills/spec/dor-dod.md` — D2, D3 and D10, to decide how the two findings should be routed
  - `tracker/project.yaml` — the two gate commands
  - branch `wi/WI-0004` at **`0a26e4ae8ee5fa216fe205e3e24332fc58f5efde`**, working tree clean; `git diff main..wi/WI-0004 -- recall.py` read hunk by hunk
  - `README.md` — the `## Commands` section, for AC10
- **Decisions:**
  - **All ten criteria pass**, each on a command this skill ran against a store it created under `/tmp/vfy4/`, with `HOME` redirected so no real card store could be reached. No verdict cites `impl-report.md`.
  - **AC2 was checked harder than it asks.** The criterion says `< /dev/null`, which only shows that a closed stdin is survivable. It was re-run as `timeout 5 ... recall delete 2 < <(sleep 30)` — stdin held open for 30 seconds — and still exited 0 rather than 124, which establishes the "never asks" the criterion is actually about.
  - **AC10 was checked by execution, not by reading.** The README's worked example was run verbatim and its output compared to what the file prints; it matches byte for byte. The three behavioural claims in its "If the number names no card" paragraph were each checked against AC5's and AC6's runs.
  - **F1 — `impl-report.md` overstates its mutation evidence.** It attributes its mutation A to AC5 and lists AC5 among the tests the mutations turned red. Re-running that exact mutation turned red only `test_deleting_with_no_store_file_at_all_creates_nothing`, which is AC6's. Classified as **neither a send-back nor a bug**: AC5's delivered behaviour is correct and was verified directly, so no criterion of this item fails, and the claim is about this item rather than another's behaviour. Recorded in `verify-report.md` `## Defects found` for `review-close`, which owns D2 and D3.
  - **F2 — AC5's test cannot distinguish the correct implementation from a crashing one.** Under mutation M1 the test still passes against code that raises `TypeError`: exit is non-zero because the exception is, stdout is empty because the crash precedes the print, the store's bytes match because a spurious `save` of an unmodified document is idempotent, and `assertIn("9", stderr)` is satisfied by the traceback's line numbers `489` and `402`. Same classification and same reason as F1 — the criterion is sound, the code satisfies it, the test is weak. The narrow fix is recorded in the report.
  - **Considered and rejected: sending the item back to `in-progress`.** The rule is a failure of *this item's own* acceptance criteria, and AC5 does not fail — it was demonstrated directly, twice. `review-close` can reject with reasons if it judges F1 and F2 to bear on D2 or D3; that is the designed route for a defect in the record rather than in the behaviour, and taking it here would have been this skill substituting its judgement for that gate's.
  - **The diff accounts for itself.** Every hunk in `recall.py` traces to plan steps 1–4 or to one of the three deviations `impl-report.md` declares. Nothing is unrequested and nothing is unspecified-but-shipped. Deviation 3 — the `try/except` around `save`, which no criterion covers — was exercised rather than read: with the store's directory at `chmod 500`, `recall delete 1` exits 1 with `recall: cannot write ... Permission denied`, leaves the store byte-identical and leaves no temp file. It behaves as `add` and `review` already do.
- **Questions raised:** none — no criterion was ambiguous. AC5's wording is precise; what is weak is the test behind it, which is a finding rather than a question.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 101 tests in 7.318s ... OK`
  - `python3 -m compileall -q -x '[.]claude' .` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - AC1/AC3: three `recall add`s, `recall delete 2` → 0 with one stdout line, `recall list` → 0 printing cards 1 and 3; the store parsed before and after and cards 1 and 3 compared on all five named fields
  - AC2: `recall delete 2 < /dev/null` → 0, stdout 1 line, stderr 0 bytes; then `timeout 5 env ... recall delete 2 < <(sleep 30)` → 0
  - AC4: `recall delete 1` → 0, `recall review < /dev/null` → 0 printing `Nothing is due today.`
  - AC5: `recall delete 9` → 1, stderr `recall delete: there is no card 9`, stdout 0 bytes, md5 `6fffae2e262d9995c29bdf5a1ac36616` unchanged
  - AC6: `recall delete 1` at an absent path → 1, stderr `recall delete: there is no card 1`, path still absent
  - AC7: `recall delete 1` → 0, `recall list` → 0 `No cards yet.`, `recall add` → 0 `Added card 1.`
  - AC8: `recall delete`, `delete 1 2`, `delete two`, `delete 0` → 2, 2, 2, 2; each `usage: recall delete <card number>` on stderr; md5 unchanged after each; `ls -a` showed no stray `.recall-*.tmp`
  - AC9: `recall delete 1` against `{ not json` → 1, stderr naming the path, md5 unchanged
  - AC10: the README's worked example run verbatim → output identical to the documented output; `recall review` after a delete → 0, showing only the surviving card
  - beyond the criteria: `chmod 500` on the store directory then `recall delete 1` → 1, `Permission denied` on stderr, store unchanged
  - seven mutations of `recall.py`/`README.md`, each followed by `python3 -m unittest discover -s tests -t .` → 1 each (1, 2, 1, 2, 1, 2 and 5 failing tests respectively), each reverted with `git checkout -- recall.py README.md`; the suite re-run → 0 `OK` and `git status --short` clean
  - the implementation report's own mutation A re-run → 1, with `test_deleting_with_no_store_file_at_all_creates_nothing` as the sole failure, which is finding F1
- **Gates:**
  - `tests-pass` → **pass** (run by this skill on `0a26e4ae`, exit 0, 101 tests)
  - `lint-clean` → **pass** (run by this skill, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors 0 warnings, re-run after the ten boxes were ticked)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md` `## Criteria` gives a command and its actual output for each of AC1–AC10; no cell cites the implementation report)
  - `negative-cases-exercised` → **pass** (eleven cases listed in `verify-report.md`, all triggered: the eight the criteria name — the two not-found cases, the four wrong command lines, the unreadable store, the emptying boundary — plus a stdin held open, an unwritable directory, and a sweep for stray temp files)
  - `tests-would-fail-without-the-change` (advisory) → **pass, with a qualification** (seven mutations; six turned the intended criterion's test red, and the seventh, M1, is finding F2 — AC5's test survives an implementation that raises)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md`, with `Verified-commit: 0a26e4ae8ee5fa216fe205e3e24332fc58f5efde`
  - `tracker/items/WI-0004/item.md` — all ten checkboxes ticked, each against a command in the report
  - no bug item filed, and none warranted: neither finding is behaviour delivered by another item
- **Status:** `verifying` → `in-review`
- **Result:** WI-0004 passes verification at `0a26e4ae`. All ten criteria were demonstrated by commands this skill ran, and every negative and boundary case the criteria describe was triggered rather than read about. Two findings go to `review-close` rather than back to the developer: `impl-report.md` misattributes one of its mutation runs to AC5 (F1), and AC5's test would pass against an implementation that crashes (F2). The criterion itself is sound and the delivered code meets it.

## 2026-08-29T13:58:31Z — review-close v0.5.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the ten criteria and their tick state
  - `tracker/items/WI-0004/journal.md` — **in full**, all eight entries; certifying the record complete is not something a skim supports
  - `tracker/items/WI-0004/history.md` — eight rows, checked for a gap and against `item.md`'s status
  - `tracker/items/WI-0004/artifacts/plan.md`, `impl-report.md`, `verify-report.md`, and `questions/Q-001.md`
  - **the diff itself**, `git diff main..wi/WI-0004`, hunk by hunk — 4 non-tracker files, +310/−5 — not the reports about it
  - `docs/architecture/adr/ADR-0004-*.md`, `ADR-0005-*.md`, `ADR-0008-*.md`, `ADR-0009-*.md`, and `docs/architecture/overview.md` §1, §2 and "A card number is a handle, not an identity"
  - `README.md` — the three edits, and `## Not yet built`, which this change does not falsify
  - `.claude/agile-skills/spec/dor-dod.md` §3 — D1 to D12, applied one at a time
- **Decisions:**
  - **Accept and close as `delivered`.** All ten criteria are met, demonstrated by commands rather than asserted, and the change is in the shape the rest of `recall.py` already has — a pure function beside `add_card`, a command function beside `cmd_list`, and the same validate-load-decide-write order that makes "changes nothing on disk" structural rather than careful.
  - **Every hunk maps to a criterion or a plan step.** No unrequested scope. The three deviations `impl-report.md` declares are all "how" rather than "what", and the only one that adds uncovered behaviour — catching a failing `save` — makes `delete` consistent with `add` and `review` rather than novel. I exercised it rather than reading it: with the store's directory at `chmod 500`, `recall delete 1` exits 1 with `Permission denied`, leaves the store byte-identical and leaves no temp file.
  - **D12 audited from the citations, not the prose.** Six absolute claims in `docs/` about behaviour this item touched were checked by opening what each cites and running the code. Five hold, one does not — finding R1.
  - **R1 — `ADR-0004`'s option F still reads "Risk: low; nothing in the epic deletes a card".** Recorded as an accepted gap, not a send-back: it sits in `## Options considered`, which is the reasoning at the time, and `ADR-0008` was written precisely to re-weigh that premise and kept option F. What is real is that the link runs one way — `ADR-0004` is marked `current` and points nowhere — which is D12's failure shape. The fix is a forward pointer with a version bump, and amending an ADR is the architect's call, not this skill's, so I record it rather than perform it.
  - **R2 and R3 — the two findings `verify` raised — confirmed and accepted, not sent back.** `impl-report.md` attributes a mutation to AC5 when the test that failed was AC6's, and AC5's own test passes against an implementation that raises. Neither is a failure of this item's criteria: AC5's delivered behaviour is correct and was demonstrated directly, and I spot-checked that demonstration against the report's quoted md5 rather than taking the tick on trust. R3 is the more useful of the two — it is *why* R2 could be written unnoticed — and the narrow fix is recorded.
  - **Considered and rejected: sending back over R2 and R3.** A rejection has to be actionable against a criterion, and no criterion fails. Considered and also rejected: filing R3 as a bug item. `spec/dor-dod.md` RB2 wants actual behaviour contradicting something, and the behaviour is correct — the test is what is weak. Misfiling it as a bug would put a defect record against code that has none.
  - **All six accepted gaps written into `item.md`'s `## Notes`.** A gap that lives only in a report nobody reopens has stopped being recorded.
  - **Closed before merging, deliberately.** `commits-reference-the-item` reads `main..wi/WI-0004`, which merging empties, so the close has to come first. The merge was proved safe before the close rather than after: a detached trial worktree, a clean `--no-ff` merge, the full suite green on the merge result, the worktree removed, and `git rev-parse main` confirmed unchanged at `6e9e5cc`.
  - **The epic was not touched by this execution.** EP-001 reaches rest only once WI-0004 is `done`, and ending an engagement is its own dispatch on the epic. `engagement-state` is recorded below for what it said *before* this close, which is the honest reading: this skill was dispatched on the work item, not on the epic.
- **Questions raised:** none — no reading of the change contradicts an ADR, so there was nothing to escalate. R1 is a stale sentence in an ADR, not a conflict with its decision.
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 0, `verified at 0a26e4ae; wi/WI-0004 has moved to 5dfc6eb2 but only the record changed (5 file(s) under tracker/ or docs/)`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, `all 7 commit(s) on main..wi/WI-0004 name WI-0004`
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0004` → 0, `WI-0004 is a 'work-item', not an epic`
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `git worktree add --detach /tmp/trial-wi4 main` → 0; `git -C /tmp/trial-wi4 merge --no-ff wi/WI-0004` → 0, trial head `fef04574`
  - `python3 -m unittest discover -s tests -t .` **inside the trial worktree** → 0, `Ran 101 tests in 7.399s ... OK`
  - `git worktree remove --force /tmp/trial-wi4` → 0; `git rev-parse main` → `6e9e5ccd9f5cc046e04f9745fde7b8a0fc106ecc`, the same sha as before the trial
  - D12 audit: three `recall add`s, `recall delete 3`, `recall add "die Maus" "the mouse"`, `recall list` → `3\tdie Maus\tthe mouse`, confirming the overview's freed-number claim; the store's keys read back as `['cards', 'version']` and `['answer', 'due', 'interval', 'number', 'question', 'result']`, confirming "no history and no second copy"; `recall delete 9` → 1
  - `chmod 500` on a store directory then `recall delete 1` → 1, `recall: cannot write ...: Permission denied`, store unchanged, no temp file
  - `.claude/agile-skills/scripts/transition WI-0004 --to done ...` → **1** on the first attempt: `workspace-valid` reported `item.outcome.premature`, because this skill had written `outcome: delivered` into the frontmatter by hand before the status was `done`. Correct refusal — the outcome is `transition --outcome`'s to write, at the moment of the move. The hand-written field was removed and the flag used instead
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each recorded with its own result and evidence in `review.md` `## Definition of Done`; D7 and D12 pass with finding R1 attached. Not a single verdict)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0 — run, not judged by eye; the gate itself established that every commit after `0a26e4ae` touches only `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0 over all seven commits, run while the branch is still unmerged so the range is non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (101 tests, exit 0, run inside the detached trial worktree on the merge result — not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, re-run after the `## Notes` and `outcome` edits)
  - `record-is-reconstructible` → **pass**. Answered from the tracker, `docs/` and `git log` alone: *what was built and why* — `recall delete <card number>`, because the stakeholder named it as the one follow-up they wanted at EP-001 sign-off (`item.md` `## Notes`, `EP-001/Q-005`); *which skill decided what* — `refine` settled the criteria and routed three design questions onward, `plan` settled them in ADR-0008 and ADR-0009, `implement` made three declared deviations, `verify` decided the ten verdicts, this review accepted six gaps; *what questions arose and how they were resolved* — `Q-001`, whether `delete` confirms first, answered by the human as "act immediately and tell me what went", propagated into AC2; *what verification found* — ten passes on commands it ran, plus two findings it declined to send back, both carried forward here as R2 and R3
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0; it had already refused this item once, on four unresolvable citations in `impl-report.md`, fixed in `1b1c674`)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0004` exit 0: "WI-0004 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only"). EP-001 was **not** at rest while this execution ran, because WI-0004 was still `in-review`; it reaches rest as a consequence of this close, and ending it is its own dispatch on the epic, which this skill did not perform and must not fold into a work item's review.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — what was examined, D1–D12 one at a time, three findings, six accepted gaps, the verdict
  - `tracker/items/WI-0004/item.md` — `outcome: delivered`, set by `transition --outcome` rather than by hand, and a new `## Notes` section carrying all six accepted gaps so they survive the close
  - the merge of `wi/WI-0004` into `main`, made immediately after this transition
  - no bug item filed, and none warranted
- **Status:** `in-review` → `done`
- **Result:** WI-0004 is accepted and closed as `delivered`. All ten criteria hold, D1–D12 each pass with their own evidence, and the merge was proved clean on a detached trial that left `main` where it was. Three findings are recorded rather than sent back — a stale premise in `ADR-0004` with no forward pointer, an overstated evidence claim in `impl-report.md`, and an AC5 test that would pass against a crashing implementation — and all six accepted gaps are now in the item's `## Notes` rather than only in reports. EP-001 reaches rest with this close; ending the engagement is a separate dispatch on the epic and was deliberately not done here.
