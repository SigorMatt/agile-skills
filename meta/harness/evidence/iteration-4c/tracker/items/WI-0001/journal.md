# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T11:07:33Z — intake v0.3.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was created by that execution, so the trigger is the creation itself rather than a status.
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement, verbatim)
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution — no prior items, no prior IDs)
  - `docs/product/vision.md` (did not exist before this execution)
- **Decisions:**
  - See `EP-001`'s entry of the same execution for how the work was split and why this is one of two items.
  - Acceptance criteria are deliberately left rough. AC1–AC4 name no command, screen or file, because how the person interacts with the tool is open as `EP-001/Q-001`; writing `flash add` into a criterion would have been intake inventing the answer to its own question.
  - AC5 (the stored data is inspectable without running the tool) is intake's own addition, not the stakeholder's words. Rationale: "progress persists" is otherwise only checkable on the tool's own testimony, and `WI-0002` AC2 is undecidable without it. It is flagged as intake's addition in `## Notes` so `refine` puts it to the stakeholder rather than letting it stand as if they had asked for it.
  - Priority `critical`: nothing else in the epic is deliverable until cards exist and persist, and `WI-0002` declares `depends-on: WI-0001`.
- **Questions raised:** none on this item; four were raised on `EP-001` (`Q-001`–`Q-004`), three of which this item's criteria depend on.
- **Commands:**
  - `scripts/new-item --id WI-0001 --type work-item --title "Add a flashcard and have it survive a restart" --epic EP-001 --priority critical --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` reported 0 errors after this execution's journals and the epic transition; see `EP-001`'s entry for the run)
  - `epic-has-success-measures` → **pass** (judged on `EP-001`; see that entry for the evidence — this gate is not an item-level check)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation` → exit 0; the elicitation is `EP-001/Q-004`)
  - `items-are-separable` (advisory) → **pass** — this item is buildable first and depends on nothing; `WI-0002` cannot be built before it because there would be no cards to review.
  - `no-solution-in-the-problem` (advisory) → **pass** — the story and criteria name no language, framework, command or data format. "Question side and answer side" is the stakeholder's own notion of a card, not a data structure.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/history.md`, `tracker/items/WI-0001/journal.md` (new, by `scripts/new-item`)
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The first of two work items under EP-001: add a card, and it is still there after a restart. Rough by design — three of its five criteria cannot be made decidable until the stakeholder answers `EP-001/Q-001`–`Q-003`.

## 2026-08-30T11:18:49Z — answer-questions v0.4.0 — architect

- **Item:** WI-0001
- **Trigger:** `answer-questions` consuming the stakeholder's answers to `EP-001/Q-001` to `EP-001/Q-004`; this item is named in the `## Consequences` of three of them
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (answers)
  - `tracker/items/WI-0001/item.md` (the criteria as intake left them)
  - `tracker/items/EP-001/item.md` (success measures and scope)
  - `docs/product/vision.md` (v1, as it stood)
- **Decisions:**
  - Amended AC1–AC5 rather than adding new ones. Rationale: intake wrote them deliberately vague against four open questions — "the tool", "a question side and an answer side", "recorded as due" — and every one of those gaps is now closed by a sentence the stakeholder wrote. The item is at `draft`, so no criterion was frozen; `refine` still has to take them to the Definition of Ready.
  - AC2 now says the **machine** is restarted, not the tool. Rationale: the stakeholder's words were *"a file on my machine that survives a reboot"* (`EP-001/Q-004`), which is a stronger promise than the one intake wrote, and it is the promise they made the product's first failure mode.
  - AC4 now names a due date — the day the card was added — rather than saying only that a new card is "recorded as due". Rationale: under `EP-001/Q-003`'s rule a card is due when its date is today or earlier, so "due" is not a flag but a date, and something had to state which one. This is the architect's inference and is recorded as such in `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`, not presented as the stakeholder's words.
  - Kept AC5 and kept intake's warning on it. Rationale: the stakeholder asked for a file on their machine, which is not the same as asking to be able to read it by hand; the criterion is still ours, and `refine` should put it to them rather than let it pass as theirs.
  - Moved deletion out of this item's scope to WI-0003, and left editing excluded with the stakeholder's own reason.
  - Left two things unstated for `refine`: what the commands are called, and what happens when the same front side is added twice. Rationale: the record is silent on both and neither is inferable.
- **Questions raised:** none on this item (`EP-001/Q-005` was filed on the epic and does not block this one)
- **Commands:** none
- **Gates:**
  - `answer-is-propagated` → **pass** (this file is named in the `## Consequences` of `EP-001/Q-001`, `Q-003` and `Q-004`, and each named change is in it: AC1 names a terminal command, AC1/AC5 the one-line sides and the local file, AC2 the reboot, AC4 the due date)
  - `answered-from-the-record` → **pass** (each amendment cites the stakeholder's sentence it came from, in `## Notes`; the one inference is cited to ADR-0002)
  - `escalation-is-justified` → **skipped** (the one escalation this execution made, `EP-001/Q-005`, is on the epic)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item EP-001`, exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported on the EP-001 entry for this execution)
  - `item-resumed-correctly` → **skipped** (this item was never suspended; it stays at `draft`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (AC1–AC5 rewritten, out-of-scope list rewritten, `## Notes` replaced with what each answer settled and what is left for `refine`)
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The criteria no longer say "the tool" and "recorded as due": they name a terminal command, a card of two one-line sides, a file on the machine that survives a reboot, and a due date. The item stays at `draft` for `refine`.

## 2026-08-30T11:32:14Z — refine v0.3.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (highest-ranked runnable item: priority
  `critical`, no `depends-on`, no open question at the time of selection)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md` — including `intake`'s entry, which
    is where the stakeholder's verbatim answers live, and `answer-questions`' entry, which says
    which criteria it amended and which two gaps it deliberately left for this skill
  - `tracker/items/WI-0001/artifacts/` — no `refinement-qa.md` existed; this execution created it
  - `tracker/items/EP-001/questions/Q-001.md` to `Q-005.md` — all five answers, read in full so
    that nothing already answered would be asked again
  - `tracker/items/EP-001/item.md` — scope and success measures
  - `docs/product/vision.md` (v3), `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`,
    `ADR-0002-scheduling-binary-ladder.md`, `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`
  - `tracker/project.yaml`; `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **Two questions to the stakeholder, three settled here.** The routing test in the procedure
    was applied to each Definition of Ready failure in turn, and the split is the substance of
    this execution. What went to them: what happens when the same front side is added twice
    (`Q-001`), and whether the card file must be readable by eye (`Q-002`). What did not: the
    subcommand name and how the two sides are supplied, the behaviour on an empty side, and the
    wording of the confirmation.
  - **Why the naming questions were not asked.** The stakeholder answered a category, not one
    question: *"As for how it's actually built — whatever you think is best"* (`EP-001/Q-004`).
    The procedure names that case — a standing deferral covering how it is built, what things are
    called and the wording of output — and says to decide it and say so. This item's `## Notes`
    carried a prior execution's suggestion to put the command wording to them; that suggestion is
    not followed, and the reason is recorded rather than left as a silent departure. Asking would
    have told them their answer was not heard, which is F-023.
  - **Assumed: the add operation is a subcommand `add`, taking front and back as two arguments,
    front first.** Basis: the deferral above, plus their picture of the use — *"once a day at a
    terminal"* (`EP-001/Q-001`) — which a prompt-driven flow slows down for no gain. The
    executable's own name stays `plan`'s, so the criterion will name the subcommand and not the
    binary. Reversible at zero cost before anything is built.
  - **Assumed: a card with an empty or whitespace-only side is refused**, with a message naming
    which side, a non-zero exit and nothing written. Basis: such a card cannot be reviewed at all,
    so accepting one puts an unusable row into the file that carries the persistence promise. One
    check at the entry point; reversible.
  - **Assumed: the confirmation names the card that was added.** The exact sentence is `plan`'s.
  - **Why `Q-002` is theirs and not ours, despite the same deferral.** The deferral covers the
    format; it does not cover how strong a *promise* the tool makes about the person's own data.
    AC5 was intake's addition, flagged at the time as something to put to them, and it asserts more
    than the sentence it came from. It is also the only decision on this item that is expensive to
    undo — their study history accumulates in whatever the first version writes, and losing
    progress is one of the two failures they named (`EP-001/Q-004`).
  - **Why `Q-001` is theirs.** The tool cannot distinguish a homograph from a typo and they can;
    the answer decides whether a card can ever be refused, which is a behaviour they meet the first
    time they type a word twice.
  - **The acceptance criteria were deliberately not rewritten.** AC3 and AC5 both turn on the two
    open answers, and rewriting AC1 alone would leave the item looking half-refined with no record
    of why. The rewrite happens when this skill resumes; what this execution owes the record is the
    agenda, the routing and the assumptions, and all three are on disk.
  - **No Definition of Ready override.** Nothing was passed; the item is suspended. Recording an
    override here would claim the stakeholder waived criteria they have not been asked about.
- **Questions raised:** `WI-0001/Q-001` and `WI-0001/Q-002` — both blocking, both addressed to
  `human`, filed as one round of two and framed as one conversation per `spec/question.md` §2.
  Nothing left `[unresolved]` beyond those two; `artifacts/refinement-qa.md` records both, plus
  the three assumptions as `[assumed]` with their basis.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition,
    with exactly the two errors the transition clears (`board.stale`,
    `question.blocking.not-suspended`)
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0, 0 consumed human
    answers on this item
  - `python3 .claude/agile-skills/scripts/board-gen .` → run by the transition
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 for the state this move produces;
    the one remaining warning is `commands.test` null, which is `plan`'s to fill)
  - `definition-of-ready` → **fail**, criterion by criterion, which is why this item is suspended
    rather than passed: R1 pass (frontmatter, `type`/`epic`/`priority` set); R2 pass (role,
    capability, "so that"); R3 pass (AC1–AC5, labelled, checkboxes); **R4 fail** — AC1 names no
    command and AC3's "each can be told apart from the others in the stored data" states no
    observation; R5 pass (five out-of-scope entries); **R6 fail** — this execution filed two
    blocking questions; R7 pass (no `depends-on`); **R8 fail** — `refinement-qa.md` exists but
    declares `status: agenda`, which by design does not satisfy R8; R9 pass (one command, one file,
    one persistence promise); **R10 fail** — neither a duplicate front nor an empty side had a
    stated behaviour anywhere, which is what `Q-001` and the empty-side assumption now close.
  - `criteria-are-decidable` → **fail** — AC1 and AC3 are the two that fail R4, and both are
    recorded above with what would make them decidable. Not repaired in this execution because
    AC3's repair depends on `Q-001`'s answer.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001`, exit 0). No human answer
    was consumed here, so rule 1 examined nothing on this item; the check that mattered was the
    other direction and it is written in `refinement-qa.md` — the five recorded answers were read
    to confirm that neither question re-asks something already settled, and that `EP-001/Q-004`'s
    deferral covers the three decisions taken without asking.
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` exists, declares
    `status: agenda` because the conversation has not happened, records both questions as
    `[unresolved]` with the stakeholder, and records the three decisions as `[assumed]` with the
    deferral each relies on. Every stakeholder sentence it quotes is quoted, not paraphrased.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` (new) — duplicate front sides
  - `tracker/items/WI-0001/questions/Q-002.md` (new) — whether the card file must be readable
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0001/item.md` — `## Notes` rewritten: what is with the stakeholder, what was
    assumed and on what basis, and the per-criterion Definition of Ready result. Acceptance
    criteria untouched.
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0001 is suspended at `awaiting-answer` with `resume-to: draft`, waiting on two
  blocking questions to the stakeholder: what a duplicate front side does, and whether the card
  file has to be readable by eye. Three further gaps were closed here under their standing
  deferral about how the tool is built, and are recorded as assumptions rather than as their
  words. The criteria are rewritten when the answers arrive.

## 2026-08-30T11:42:27Z — answer-questions v0.4.0 — architect

- **Item:** WI-0001
- **Trigger:** `awaiting-answer` with two blocking questions to the stakeholder, both of which
  now carry a reply in `## Answer`. Dispatched by the harness ahead of `next`, because `next`
  stops the loop on any open human-addressed question and this skill is the only one that may
  consume a reply to one.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — both replied to by the
    stakeholder, both blocking
  - `tracker/items/WI-0001/item.md` (AC1–AC5 as found), `history.md` (the suspending row carries
    `resume-to: draft`), `journal.md` (`refine`'s entry, including the three assumptions)
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` at `status: agenda`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — every prior recorded stakeholder
    answer, read in full for the cross-answer check
  - `docs/product/vision.md` v3; `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`
    v1, `ADR-0002-scheduling-binary-ladder.md`, `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`
    v1
  - `tracker/items/WI-0003/questions/Q-001.md` — read because it interacts with `Q-001` here; its
    reply is not yet consumed and is WI-0003's to take
  - `.claude/agile-skills/spec/question.md` §2 and §4
  - No `artifacts/plan.md` exists on this item; it has never been planned.
- **Decisions:**
  - **`WI-0001/Q-001` — answered by the human, route: escalation returned.** They chose C, add a
    duplicate front and warn: *"C — add it and warn me. I don't want it refusing a second meaning
    of a word, and a warning is enough to catch a typo."* Propagated as a **new AC6** stating the
    whole observable — a second distinct card, both kept with their own back and schedule, a
    warning naming the duplicated front, exit zero — and **AC3 amended** to say "three cards with
    different front sides", so the distinct case and the duplicate case are covered by one
    criterion each. Before this, AC3 was the only text in the item that touched duplicates and it
    stated no observation, which is what failed R4 and R10.
  - **No ADR for Q-001.** It is a product behaviour the stakeholder decided themselves; the
    criterion and the vision are the authoritative places for it, and an ADR would record as our
    decision something that was not.
  - **`WI-0001/Q-002` — answered by the human, route: escalation returned, recorded as an ADR.**
    They chose B: *"B. I want to be able to open it and see my cards are still there, but I'm not
    asking to hand-edit it — that's a different thing."* Written up as
    `ADR-0004-card-file-is-readable-text-owned-by-the-tool.md` rather than only as a criterion,
    because the commitment binds every later version — their real study history accumulates in
    whatever the first one writes — and reversing it later means migrating or losing that history,
    which is a named failure of the product (`EP-001/Q-004`).
  - **AC5 stands rather than being rewritten.** Intake had already written it to the promise the
    stakeholder has now confirmed, and flagged at the time that it went further than their words
    and had to be put to them. Their answer ratifies it, so the amendment is a sharpening — it now
    says what "readable" excludes (nothing compressed, binary or otherwise needing decoding) and
    cites the question and the ADR. Recording it as unchanged would hide that a criterion which
    had been provisional is now theirs.
  - **Hand-editing is out of scope and no work item was filed for it.** Option A would have
    implied one; they declined it in the same sentence. Filing work for it would record a scope
    they did not ask for, which is the opposite failure to the one `spec/ids-and-statuses.md` §5
    guards against.
  - **A second out-of-scope line was added: no list or find command.** The duplicate warning is
    what tells the person they already have that card; nothing in either answer implies a way to
    browse the deck, and leaving it unsaid would let a later reader assume AC6 needs one.
  - **The delete-by-front interaction was not escalated and was not settled here.** Allowing two
    cards to share a front means `WI-0003/Q-001`'s *"by typing the front side"* can match more
    than one. `WI-0003/Q-001` stated in writing that resolving this is ours once both answers were
    in, so it is an architect decision, not a contradiction between two stakeholder statements. It
    belongs on WI-0003 and is recorded as a hand-off in this item's `## Notes`.
  - **The item resumes to `draft`, not `ready`.** `resume-to: draft` is what the suspending row
    records, and it is also correct on the merits: R4 still fails on AC1, which names no command.
    That repair is `refine`'s, from the assumption `refine` already recorded, and this skill does
    not do another skill's work in order to move the board.
- **Cross-answer check:**
  - `WI-0001/Q-001` — checked against `EP-001/Q-001` (compatible, and the reason the question was
    theirs: *"running through vocab"* is where homographs live), `EP-001/Q-004` (compatible; its
    delegation covers mechanism, not behaviour, and its *"losing my progress"* failure is untouched
    because option C refuses and overwrites nothing), `WI-0001/Q-002` (compatible; legibility puts
    no constraint on how many cards share a front). No conflict.
  - `WI-0001/Q-002` — checked against `EP-001/Q-004` (compatible; the stakeholder extending their
    own *"a file on my machine that survives a reboot"* rather than contradicting it, and their
    *"whatever you think is best"* delegation survives, narrowed only on legibility),
    `EP-001/Q-002` (compatible, and it makes true a claim `ADR-0002` had already relied on — that
    a card's rung and date are *"readable by eye in the stored file"*), `WI-0001/Q-001`
    (compatible). No conflict.
  - Not checked against, and why: `WI-0003/Q-001` and `WI-0003/Q-002` carry replies from the
    stakeholder that have **not been consumed** yet, and `lint-answers` rejects a check citing a
    reply in that state (`answer.cross-check.unresolved`). The Q-001/WI-0003 interaction is
    written out in prose on the question file instead, outside the citation list, and is settled
    on WI-0003 where those replies are consumed.
- **Questions raised:** none. Neither answer conflicted with anything the stakeholder had said
  before, and nothing in either needed to go back to them.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 1 first
    (`answer.cross-check.unresolved`, citing `WI-0003/Q-001`), then exit 0 after the citation was
    moved out of the checked-against list into prose
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition,
    with exactly the two errors the transition clears (`board.stale`,
    `question.awaiting.none-open`)
  - `python3 .claude/agile-skills/scripts/board-gen .` → run by the transition
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was
    reopened and the change confirmed present: `item.md` (AC6 at line 34, AC3's "different front
    sides" at line 24, AC5's "compressed, binary" clause at line 31, hand-editing and the no-list
    line in `## Out of scope`), `refinement-qa.md` (both verbatim quotes replacing `[unresolved]`,
    `status: recorded`), `ADR-0004-…md` (created, 1 version, change-log row),
    `docs/product/vision.md` v4 (the warning clause in "Write a card down", the readable-file
    paragraph in "How it is used", two new exclusions).
  - `answered-from-the-record` → **pass**. Neither answer was derived; both are the stakeholder's
    own words, quoted verbatim and cited by question ID everywhere they were used. The one
    decision that was ours — writing Q-002's answer up as an ADR rather than only a criterion —
    is justified in the ADR itself by the irreversibility test in `spec/question.md` §4.
  - `escalation-is-justified` → **skipped**, no question was re-addressed to the human by this
    execution. Both escalations being consumed here were justified when `refine` filed them and
    the stakeholder has now answered both.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001`, exit 0, 2 consumed human
    answers checked).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 for the state this move produces;
    the remaining warning is `commands.test` null, which is `plan`'s to fill).
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-30T11:32:14Z records
    `resume-to: draft`; this execution moves the item to `draft`.
  - `a-deferral-is-not-an-answer` → **skipped**, neither reply defers. Both name an option letter
    and give a reason for it, and each settles the question it was asked.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at`, `## Cross-answer check` and `## Consequences` written
  - `tracker/items/WI-0001/questions/Q-002.md` — the same
  - `tracker/items/WI-0001/item.md` — **AC6 added**, **AC3 and AC5 amended**, two `## Out of
    scope` entries added, `## Notes` rewritten to record both answers, the delete-by-front
    hand-off to WI-0003, and the Definition of Ready as it now stands
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; both
    answers quoted verbatim; the R3, R4, R5, R6, R8 and R10 rows updated to their post-answer
    verdicts
  - `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md` — **created**,
    version 1
  - `docs/product/vision.md` — version 3 → **4**, `updated-for: WI-0001`, change-log row added
  - `tracker/board.md` — regenerated by the transition
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of the stakeholder's replies on WI-0001 are consumed and propagated. The
  duplicate-front behaviour is now AC6 and the readable-file commitment is `ADR-0004` with AC5
  ratified against it; the vision carries both. The item returns to `draft`, its recorded
  `resume-to`, with one Definition of Ready failure left for `refine`: AC1 still names no command.

## 2026-08-30T11:49:54Z — refine v0.3.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** `draft`, dispatched by `next` as the highest-ranked runnable item (priority
  `critical`; WI-0002 rejected on `depends-on WI-0001` not `done`, WI-0003 rejected on priority
  `medium`). This is a **resumed** refinement, not a fresh one: `history.md` shows the item was
  suspended by `refine` on 2026-08-30T11:32:14Z and returned to `draft` by `answer-questions` at
  11:42:27Z once the stakeholder's two answers were propagated. The agenda was therefore the two
  Definition of Ready criteria that entry recorded as still failing — R4 and R10 — and not the
  whole item.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC6 as found), `history.md`, `journal.md` — including
    `refine`'s round-1 entry and `answer-questions`' entry naming what it left
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` at `status: recorded`, rounds 1 and its
    five questions
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — both `answered`, the stakeholder's
    words read as given rather than as summarised in the item
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — every prior recorded stakeholder
    answer, to establish what had already been said before asking anything
  - `docs/product/vision.md` v5; `ADR-0002-scheduling-binary-ladder.md`,
    `ADR-0004-card-file-is-readable-text-owned-by-the-tool.md` v1
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Nothing was put to the stakeholder, and that was the first decision, not the last.** Each
    remaining gap was tested against the routing order in `refine`'s step 3. None has a product
    stake: none changes what the tool is for, what it promises, or anything they would notice
    about their own cards. Every one falls inside *"As for how it's actually built — whatever you
    think is best"* (`EP-001/Q-004`), a standing deferral over the category — naming, wording,
    exit codes, file layout. They have answered six questions already; a seventh about the name of
    a subcommand would tell them their answer was not heard (F-023).
  - **AC1 rewritten** — it said "the tool's add command" and named none, which was R4's failure.
    It now names the `add` subcommand, says there are exactly two arguments and which order they
    take, requires the confirmation to name the front side, and requires exit zero. This promotes
    `refinement-qa.md` Q3's assumption out of prose and into the criterion, which is where `verify`
    will look for it. The **executable's** name is deliberately still absent: that is `plan`'s,
    along with the language and packaging.
  - **AC2 rewritten** — "the card is still there" named no observation. It now says: read the card
    file with an ordinary text tool. That is only writable as a criterion because of the
    stakeholder's answer to `WI-0001/Q-002` and `ADR-0004`; before that answer the file's contents
    were not promised to be legible and this criterion could not have been settled without asking
    the tool.
  - **AC3 rewritten** to name the same reading, so all of AC2, AC3 and AC4 are settled the same
    way. Its substance is unchanged.
  - **AC4 narrowed, and this is the one meaning-changing edit.** It asserted the card "is due in
    that day's review session and remains due until it is answered" — a claim about WI-0002's
    session, which this item does not deliver and which nobody could settle here. It now asserts
    only what this item writes: the record's due date equals the calendar date the card was added,
    read from the file. A parenthesis says where the rest lives. This narrows what WI-0001
    promises; it does not narrow what the stakeholder was promised, because `EP-001/Q-003`'s due
    rule is untouched and WI-0002 carries it.
  - **AC7 added — the empty side.** It was `refinement-qa.md` Q4, an assumption in prose, which is
    exactly the R10 shape: a behaviour the tool must have that no criterion stated. It now says
    nothing is added, the message names which side was empty, the exit is non-zero, and the file is
    byte-identical (or still absent). **One thing was added that nobody had stated**: this check
    runs *before* AC6's duplicate check, so an empty back with a duplicate front is refused by AC7
    and prints no duplicate warning. Without that ordering both criteria claim the same case and an
    implementation could satisfy either while contradicting the other.
  - **AC8 added — the card file does not exist yet.** Stated nowhere at all, and it is the first
    thing that happens on a clean machine. Without it AC1 was not decidable there, which is a poor
    thing to discover during verification.
  - **The wrong-argument-count case was left deliberately unconstrained**, named in `## Notes` with
    `refine` recorded as who left it and `plan`/`implement` as who settles it. R10 permits this and
    it is the honest route: a usage message and a non-zero exit is what every command-line tool
    does, and no observation of the exact wording would tell anyone whether this item delivered
    what was asked for. Writing a criterion for it would have been ceremony.
  - **No split (R9).** Five criteria became eight and none of the three new ones is a second piece
    of work: AC7 and AC8 are the failure and first-run cases of the same command, and AC6 came from
    the stakeholder. One command, one file, one persistence promise.
  - **No Definition of Ready override.** No criterion was waived and the stakeholder was not asked
    to waive one; every one is met on its own terms.
- **Questions raised:** none — nothing was filed, and nothing is left `[unresolved]` in
  `artifacts/refinement-qa.md`. Round 2's three decisions are recorded there as `[assumed]` (Q6,
  Q7, Q8), each naming `EP-001/Q-004`'s deferral as its basis and each stated as reversible. The
  two `[unresolved]` entries from round 1 became the stakeholder's answers and are quoted verbatim.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0, 2 consumed human
    answers, both from round 1
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before the transition
  - `python3 .claude/agile-skills/scripts/board-gen .` → run by the transition
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0; the one warning is
    `commands.test` null, which `plan` must fill or write an ADR against — it is not this item's).
  - `definition-of-ready` → **pass**, criterion by criterion:
    - **R1 pass** [auto] — frontmatter complete; `type: work-item`, `epic: EP-001`,
      `priority: critical`.
    - **R2 pass** — `## Story` has the role ("someone studying a subject"), the capability
      ("write down a question and its answer as a flashcard") and the outcome ("so that the thing
      I want to remember is captured in the tool instead of in my head").
    - **R3 pass** [auto] — AC1 to AC8, each labelled and a checkbox.
    - **R4 fail as found → repaired → pass.** AC1 named no command; AC2, AC3 and AC4 named no
      observation; AC4 additionally asserted behaviour this item does not deliver. All four are
      rewritten above. Taking them in turn: AC1 is settled by running `add` with two arguments and
      reading stdout and `$?`; AC2 by restarting and reading the card file; AC3 by adding three
      cards and reading it; AC4 by reading the due date out of the record and comparing it with
      today's date; AC5 by reading the file and inspecting the documented path; AC6 by adding a
      duplicate front and reading stdout, `$?` and the file; AC7 by passing an empty argument and
      comparing the file before and after; AC8 by deleting the file and running `add`. No criterion
      contains an unmeasurable adjective — the ones that could have ("readable") are pinned by
      AC5's explicit exclusion of anything compressed, binary or encoded.
    - **R5 pass** — seven `## Out of scope` entries, including three a reader could reasonably
      assume were in: editing a card, hand-editing the card file, and any way to list the cards.
    - **R6 pass** [auto] — no question on this item is open; both are `answered`.
    - **R7 pass** [auto] — no `depends-on`. WI-0002 depends on this item, not the reverse.
    - **R8 pass** [auto] — `artifacts/refinement-qa.md` declares `status: recorded` and holds both
      rounds, with the stakeholder's two answers quoted verbatim and every assumption tagged
      `[assumed]` with its basis.
    - **R9 pass** — one command, one file, one persistence promise; the split test is written out
      under Decisions above.
    - **R10 fail as found → repaired → pass.** The combinations this item introduces: a duplicate
      front (AC6, the stakeholder's own answer), an empty or whitespace side (AC7, with its
      precedence over AC6 now stated), a card file that does not exist yet (AC8), and the wrong
      number of arguments (named in `## Notes` as deliberately unconstrained, by `refine`, for
      `plan`). The empty-with-duplicate intersection is the case R10 exists to surface, and it is
      now decided rather than merely visible.
  - `criteria-are-decidable` → **pass** — the observation that settles each of the eight is listed
    under R4 above. Each is a command to run and an output, an exit status or a file to inspect.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001`, exit 0). Round 2 recorded
    no new stakeholder answer, so rule 1 had nothing new to examine. The check that mattered ran in
    the other direction and is written into `refinement-qa.md`: none of the three assumptions
    contradicts a recorded answer. AC7's precedence does not weaken *"add it and warn me"*, because
    it applies only where no card is added at all; AC8 adds nothing to `WI-0001/Q-002` beyond
    creating the file it describes; AC4's narrowing leaves `EP-001/Q-003`'s due rule untouched and
    unrestated, in WI-0002 where it belongs.
  - `qa-recorded-verbatim` → **pass** — `refinement-qa.md` is `status: recorded`, both stakeholder
    answers are block quotes of their exact words with `[src:]` citations, and round 2's three
    decisions are `[assumed]` with the deferral each relies on named. Nothing was paraphrased into
    a firmer statement than was made.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC1, AC2, AC3 and AC4 rewritten; **AC7 and AC8 added**;
    `## Notes` rewritten to record what each assumption became, the deliberately unconstrained
    argument-count case with `refine` named as who left it, and the full Definition of Ready result
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — **round 2 added** as Q6, Q7 and Q8, each
    `[assumed]` with its basis and its reversibility; the R3, R4 and R10 rows updated from "as
    found" to their repaired verdicts; the cross-answer section extended with round 2's
    other-direction check
  - `tracker/board.md` — regenerated by the transition
  - No question file was created. No document under `docs/` was touched: this execution recorded no
    new stakeholder answer and had nothing to propagate there.
- **Status:** `draft` → `ready`
- **Result:** WI-0001 is `ready`. Eight acceptance criteria, each settled by a command and an
  observation; seven exclusions; one case deliberately left unconstrained and named as such. The
  two failures `answer-questions` left — R4 on AC1 and R10 on the empty side — are repaired, and
  two gaps nobody had noticed are now criteria: the precedence of the empty-side check over the
  duplicate warning, and what happens on the first ever run when no card file exists.

## 2026-08-30T12:00:31Z — plan v0.4.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` as the highest-ranked runnable item
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (all eight acceptance criteria, the out-of-scope list and the notes)
  - `tracker/items/WI-0001/history.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (the six `[assumed]` entries, Q3 to Q7)
  - `tracker/items/WI-0002/item.md` and `tracker/items/WI-0003/item.md` (what this item must leave possible, and what it must not deliver)
  - `docs/product/vision.md` (v5)
  - `docs/architecture/adr/ADR-0001-command-line-delivery-surface.md`
  - `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`
  - `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md`
  - `docs/architecture/adr/ADR-0003-...` and `ADR-0005-...` (read for scope; neither constrains this item)
  - `tracker/project.yaml` (both commands were `null`)
  - `.claude/agile-skills/spec/doc-header.md` §4, §4a, §4b; `spec/workspace-layout.md` §5
  - the project's source code: there is none — the repository held no product code before this execution
- **Decisions:**
  - **Python 3, standard library only, package at the repository root** (`ADR-0006`). From the documents: the stakeholder delegated the technology outright, so this was decided rather than asked. Rationale for stdlib-only over a virtual environment with a linter: `implement`, `verify` and `review-close` each run `commands.lint` from `tracker/project.yaml`, and a command that depends on an environment somebody has to recreate is a gate that fails for a reason unrelated to the work.
  - **`commands.test` = `python3 -m unittest discover -s tests -t . -q`, `commands.lint` = `python3 -m compileall -q recall tests`** (`ADR-0006`). Both were run before being recorded. The ADR states in as many words what the lint command does not catch, because a weak gate that is not written down reads as a strong one.
  - **The card file format: one card per block of labelled lines, values taken verbatim to end of line** (`ADR-0007`). Decided against AC2's byte-identical requirement, which is what eliminated JSON: a front containing a quotation mark would appear escaped, so what the reader sees would not be what they typed. Tab-separated values lost on readability and on needing to refuse tabs as well as line breaks.
  - **`rung: 0` for a card that has never been answered; 1 to 4 are `ADR-0002`'s intervals** (`ADR-0007`). Derived from the ladder, not a change to it: `ADR-0002` makes the first rung a day away, which a card nobody has answered is not on. This item must write *some* initial value, so leaving it to `implement` would have buried the decision.
  - **A side containing a line break is refused, like an empty side** (`ADR-0007`). The format cannot hold one, and every criterion describes one-line sides. Recorded as a decision rather than an assumption because it is a property of the file, which is the expensive thing to change.
  - **The card file's location, the `RECALL_CARD_FILE` override, and creating the directory on first use** (`ADR-0008`). A path in the current working directory was rejected: a tool run from wherever the terminal happens to be would silently accumulate several decks. The override is what lets the tests drive the real entry point without touching a real deck.
  - **Every save goes through a temporary file, a flush and a rename** (`ADR-0008`). AC2 asks for survival across a machine restart and AC7 asks that a refused run leave the file byte-identical; writing in place satisfies neither in the case that matters.
  - **Five reversible assumptions, recorded in the plan under `## Assumptions`** rather than as ADRs: the exit codes, the message wording, which stream each goes to, what happens when the card file does not parse, and the in-memory type of the due date. Each is one file to reverse and none is visible outside the tool. The fourth is the one that mattered — `load` cannot avoid deciding what to do with a file it cannot read, and no criterion covers it, so it is named where `implement` and `verify` will both see it.
  - **Nothing was put to the stakeholder.** The preference order was applied to each decision: the surface, the schedule and the file's readability were answered from `ADR-0001`, `ADR-0002` and `ADR-0004`; everything left falls inside their standing delegation, *"As for how it's actually built — whatever you think is best"*. The one irreversible commitment on this item — the shape of the file their history accumulates in — was escalated by an earlier execution and answered by them as `WI-0001/Q-002`, and this plan is written to that answer rather than around it.
- **Cross-answer check:** this execution relied on two recorded human answers and recorded no new one. Checked against: `EP-001/Q-004` — compatible; its delegation of how the tool is built is what authorises `ADR-0006`, `ADR-0008` and the five assumptions, and none of them touches what the tool is for. Checked against: `WI-0001/Q-002` — compatible; `ADR-0007`'s format is a narrowing of the readable-text commitment they chose, and it makes their promise stronger rather than weaker, since a value is stored with no escaping at all. Checked against: `EP-001/Q-002` and `EP-001/Q-003` — compatible; `ADR-0007` defines the `rung` field against their ladder and changes neither the intervals nor the grading rule. No conflict was found between any two of their answers, so no question was filed. No paragraph under `docs/` carrying a `[src: ITEM/Q-nnn]` marker was changed or removed by this execution: every document it wrote is new, except `docs/architecture/overview.md`, which did not exist before it.
- **Questions raised:** none
- **Commands:**
  - `python3 -V` → exit 0, `Python 3.12.3`
  - `python3 -m pip install --dry-run ruff` → `error: externally-managed-environment` (PEP 668); recorded in `ADR-0006` as why a third-party linter would need a virtual environment
  - `python3 -c "urllib.request.urlopen('https://pypi.org/simple/ruff/')"` → HTTP 200; recorded so that `ADR-0006`'s option B is weighed as available rather than impossible
  - `python3 -m unittest discover -s tests -t . -q` → exit 5, `NO TESTS RAN` — the command works against the empty suite; `implement` is what makes it exit 0
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1, 3 `claim.unsourced` errors; then exit 0 after citing each
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 4 items and 10 documents, 0 errors 0 warnings)
  - `every-criterion-is-addressed` → **pass** (the `## Acceptance criteria mapping` table in `plan.md` has a row for each of AC1 to AC8, each naming the steps that satisfy it and the named test that demonstrates it; AC2's row states plainly that no test can restart a machine and what the available evidence is instead)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` now names a test and a lint command, both run in this project before being recorded; `ADR-0006` records what the lint command does not check and why the project has no third-party linter)
  - `decisions-recorded` → **pass** (seven decisions in `ADR-0006`, `ADR-0007` and `ADR-0008`, each with at least two options and a reversibility statement; five reversible assumptions under `## Assumptions` in `plan.md`, each with what reversing it costs; the `## Decisions and ADRs` table maps every one to where it is recorded)
  - `plan-is-executable-without-you` → **advisory, pass** (each of the seven steps names the file it touches, the interface it adds, and what is observably true afterwards; the two module interfaces are given as signatures in `## Approach` so no step requires an undecided design choice)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0, 9 consumed human answers checked; the `**Cross-answer check:**` bullet above names the four answers this execution relied on and the verdict for each)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0, after repairing the three `claim.unsourced` errors its first run reported, in `ADR-0006`, `ADR-0008` and `docs/architecture/overview.md`)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new)
  - `docs/architecture/overview.md` (new, v1)
  - `docs/architecture/adr/ADR-0006-python-3-standard-library-only-and-the-project-gate-commands.md` (new, v1)
  - `docs/architecture/adr/ADR-0007-card-file-format-one-card-per-block-of-labelled-lines.md` (new, v1)
  - `docs/architecture/adr/ADR-0008-where-the-card-file-lives-and-how-it-is-written.md` (new, v1)
  - `tracker/project.yaml` (updated: `commands.test` and `commands.lint`, both previously `null`)
  - `recall/__init__.py` and `tests/__init__.py` (new, empty; scaffolding, listed under `## Scaffolding` in the plan with the command each one lets execute)
  - `tracker/board.md` (regenerated)
- **Status:** `ready` → `planned`
- **Result:** WI-0001 is planned. Seven steps, two modules with one seam, and a test per acceptance criterion driving `python3 -m recall` as a real subprocess. Three ADRs record the decisions that outlive this item — the language and the project's gate commands, the card file's format, and where it lives and how it is saved — and the architecture overview now exists and states the documented path AC5 asks for.

## 2026-08-30T12:01:08Z — implement v0.3.0 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1 to AC8, the out-of-scope list, the notes)
  - `tracker/items/WI-0001/artifacts/plan.md` (seven steps, the two module interfaces, five assumptions)
  - `tracker/items/WI-0001/history.md` — four rows, the last `ready → planned`; this is a fresh start, not a resumption, and no send-back preceded it
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — both `answered`, both already propagated into the criteria and into `ADR-0004`; nothing to re-read as new
  - `docs/architecture/adr/ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0007`, `ADR-0008`
  - `docs/architecture/overview.md` (v1)
  - `tracker/project.yaml` — branch prefix `wi/`, and both commands now non-null
  - the branch: `wi/WI-0001` did not exist; `git branch` showed `main` alone
- **Decisions:**
  - Branched from `main` at `5c667e0`, the commit that carries the plan, so the branch's first parent is the state the plan was written against.
  - Nothing else is decided yet. The work follows `plan.md`'s steps in order, and any choice made inside their latitude is recorded in the closing entry rather than guessed at here.
- **Cross-answer check:** none — this execution has edited no document under `docs/` and so has touched no sentence sourced to one of the stakeholder's answers.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001` → exit 0, switched to a new branch
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no code and no tests exist on the branch; this is the opening entry)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **skipped** (run by the transition that appends this entry; the closing entry reports it on the branch head)
  - `every-criterion-has-a-test` → **skipped** (no test exists yet)
  - `commits-reference-the-item` → **skipped** (the branch has no commits of its own yet)
  - `no-unplanned-scope` → **skipped** (advisory; there is no diff yet)
  - `cross-answer-consistency` → **skipped** (nothing changed since `main`)
  - `claims-are-sourced` → **skipped** (nothing changed since `main`)
- **Artifacts:**
  - branch `wi/WI-0001`, created from `main` at `5c667e0`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0001 has started on `wi/WI-0001`. The plan's seven steps are next, in order, each with the test that demonstrates it in the same commit.

## 2026-08-30T12:05:13Z — implement v0.3.0 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, this execution's own opening entry of 2026-08-30T12:01:08Z
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps, the two module interfaces, the five assumptions
  - `tracker/items/WI-0001/item.md` — AC1 to AC8, unchanged by this execution
  - `docs/architecture/adr/ADR-0002` (the ladder), `ADR-0004` (the readable file), `ADR-0007` (the format), `ADR-0008` (the location and the write discipline)
  - `tracker/project.yaml` — the two commands and the commit subject convention
  - the branch `wi/WI-0001` at `5c667e0`, which held no product code
- **Decisions:** all inside the plan's latitude; none of them changes what is delivered.
  - **A refusal prints a second line, `Nothing was added.`** The criterion requires the message to name the side; it does not say whether the card got in, and a person who has just been told "The back side is empty." cannot tell. Assumption 2 of the plan gives the wording to this skill.
  - **An unreadable card file is reported with its path in front of the message.** `main()` catches `CardFileError` and `OSError` and prints `<path>: <message>`, because the commonest cause is `RECALL_CARD_FILE` pointing somewhere unintended and the path is the thing that shows it.
  - **A second test file, `tests/test_store.py`.** The plan named `tests/test_add.py` for the criteria, and its steps 1 to 3 each state an observable result about the store that the command line does not reach directly — the round trip, the documented shape, the two malformed-file cases. Splitting them keeps the criterion tests to what a person at a terminal sees.
  - **The duplicate check compares fronts with `==` on the exact string**, no trimming and no case folding, because AC6 says a front *exactly equal* to an existing one, and anything looser would silently refuse to warn about a card the person would call a duplicate — or warn about one they would not.
  - **The tests drive `python3 -m recall` as a subprocess** rather than calling `main()` in-process. It costs about a second across the suite and it is the only way the exit code, the two streams and the file are all the real ones. AC1 describes a terminal.
  - **Not decided here, and not guessed:** nothing. No decision arose that the plan or an ADR did not already settle, so no question was filed.
- **Cross-answer check:** none — this execution edited no document under `docs/`, so it touched no sentence carrying a `[src: ITEM/Q-nnn]` marker for one of the stakeholder's answers. `lint-answers --changed-since main` reports 0 paths in the window and 0 errors over the 9 consumed answers in the workspace.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests`, OK (final run, on the branch head)
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 2 commits on `main..wi/WI-0001` name WI-0001
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - `git diff main --stat` → three modules, two test files, and this item's tracker files
  - three mutation runs, each reverted with `git checkout -- recall/cli.py`: emptiness check removed → 6 failures; duplicate comparison removed → 1 failure; append replaced by assignment → 2 failures
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q`, exit 0, 26 tests, run on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 4 items and 10 documents)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md`'s evidence table names a test function for each of AC1 to AC8; the three mutations above are the check that those tests would fail if the behaviour were removed)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001`, exit 0)
  - `no-unplanned-scope` → **pass, advisory** (every hunk in `git diff main` is a plan step or its test; nothing under `docs/` and no other item's files were touched)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main`, exit 0; the window is well-formed and empty because this execution changed no document)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0)
- **Artifacts:**
  - `recall/store.py`, `recall/cli.py`, `recall/__main__.py` (new)
  - `tests/test_add.py`, `tests/test_store.py` (new)
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
  - commits `d2c2432` and `5c680a8` on `wi/WI-0001`
- **Status:** `in-progress` → `verifying`
- **Result:** `python3 -m recall add <front> <back>` works, with 26 tests, and each of AC1 to AC8 has a named test that fails when its behaviour is removed. One thing is handed to `verify` openly: AC2 names a machine restart, and the evidence available is the file's bytes after the writing process exited plus `save()`'s fsync-and-rename — `impl-report.md`'s `## What I did not do` says so, and `plan.md` flagged it before any code existed.

## 2026-08-30T12:09:30Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1 to AC8, read **first**, and the checks below derived from them before the implementation report was opened
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the checks were derived; it is cited nowhere as evidence
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps and five assumptions, for the diff read
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — Q6 and Q7, on what AC1 to AC4, AC7 and AC8 were meant to settle
  - `tracker/items/WI-0001/history.md`, `tracker/project.yaml`
  - the code at `f22f9c0b0dace18718b02c819984e49d131c8648`, the head of `wi/WI-0001`: `recall/store.py`, `recall/cli.py`, `recall/__main__.py`, and both test modules
- **Decisions:**
  - **AC2 is ticked, with its gap declared rather than hidden.** The criterion names a machine restart and no machine can be restarted here. Rather than record a pass on the code's say-so or an `ambiguous` that costs a round trip on a criterion whose observable content is fully decidable, the durability claim was checked directly: `strace -f -e trace=fsync,rename` on a real `add` shows `fsync` → `rename` → `fsync`, so the bytes and the directory entry are both flushed before the process exits, and a separate process then read the exact bytes. `## Not verified, and why` states the substitution in full and says what would have to happen if anyone reads AC2 as requiring a literal reboot: the wording is revisited with the stakeholder, not this implementation.
  - **No question was filed.** No criterion turned out ambiguous. AC7's "empty" covering the whitespace-only case is settled by its own wording, and its precedence over AC6 is stated in the criterion itself; both were exercised.
  - **No bug item was filed and nothing was sent back.** Every check passed, so neither classification arose.
  - **The three things in the code beyond the plan's literal text were classified as accounted-for, not as findings**: the extra refusal line and the path-prefixed error message fall under the plan's assumption 2 on wording and are declared in `impl-report.md`; `store._card`'s rung range check is `ADR-0007`'s definition of the field. None adds behaviour a criterion contradicts.
  - **Evidence was gathered with the tool's own command line in scratch directories**, not by calling functions in-process, because every criterion describes what a person at a terminal sees. The scratch directories were removed afterwards.
- **Cross-answer check:** none — this execution edited no document under `docs/`, and no criterion it read was found to contradict any recorded answer of the stakeholder's. AC5 and AC6, which carry their answers' IDs (`WI-0001/Q-002`, `WI-0001/Q-001`), were checked against the behaviour and both hold: the file is readable text the tool owns, and a duplicate front is added with a warning.
- **Questions raised:** none
- **Commands:** (every one run by this execution, against `f22f9c0`)
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests in 1.177s`, `OK`
  - `python3 -m compileall -q recall tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - AC1: `python3 -m recall add bonjour hello` → exit 0, `Added: bonjour`; `grep -c '^front: '` → 1
  - AC2: `python3 -m recall add 'l'"'"'été "chaud" \ ünïcode<TAB>tab' 'the "hot" summer'` → exit 0; then `od -c cards.txt` and an independent byte comparison → `front line byte-identical: True`, `back line byte-identical: True`
  - AC2: `strace -f -e trace=fsync,rename python3 -m recall add chat cat` → `fsync(3) = 0`, `rename(".cards-6_dyg8vy.tmp", "cards.txt") = 0`, `fsync(3) = 0`
  - AC3: three `add` runs → `front=3 back=3 rung=3 due=3`
  - AC4: `date +%F` → `2026-08-30`; `grep '^due: ' | sort -u` → `due: 2026-08-30`
  - AC5: `env -u RECALL_CARD_FILE XDG_DATA_HOME=<dir> python3 -m recall add …` → wrote `<dir>/recall/cards.txt`; `env -u XDG_DATA_HOME HOME=<dir> …` → wrote `<dir>/.local/share/recall/cards.txt`; `file` → `ASCII text`; UTF-8 decode → `control characters other than newline: []`
  - AC6: two `add` runs with the same front, streams separated → exit 0, warning on standard error, `Added:` on standard output, two records with the two backs
  - AC7: four refusals → exit 1 each, side named, no file created; `sha256sum` before and after a refusal on an existing file → `ef49f065…c26` both times; `add bonjour ""` on a duplicate front → the empty-side message only, one record
  - AC8: `RECALL_CARD_FILE=<dir>/deep/deeper/cards.txt` with `<dir>` absent (`ls` → `No such file or directory`) → exit 0, `Added: bonjour`, one record, both sides byte-identical
  - negatives: `add only-one` → exit 2 with usage; `python3 -m recall` → exit 2; `python3 -m recall review` → exit 2, `invalid choice: 'review'`; a side with a line break → exit 1, no file; a hand-mangled card file → exit 1, `line 2: expected a line starting 'back: '`, file unchanged; an unwritable directory → exit 1, `[Errno 13] Permission denied`; a 500-character back and a space-padded front → exit 0, both kept verbatim
  - eight mutations, each reverted with `git checkout --`: AC1 confirmation → 1 failure; AC2 escaped values → 1; AC3 append→assign → 1; AC4 frozen date → 1; AC5 default path → 3; AC6 duplicate check → 1; AC7 emptiness check → 6; AC8 `makedirs` → 1. Suite green again afterwards, `git status` clean
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q`, exit 0, 26 tests, run by this skill on the branch head)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0)
  - `every-criterion-independently-checked` → **pass** (each of AC1 to AC8 has a row in `verify-report.md` naming the command this execution ran and quoting its actual output; the implementation report is not cited as evidence anywhere)
  - `negative-cases-exercised` → **pass** (nine conditions triggered and recorded: four empty and whitespace sides, a refusal against an existing file, the duplicate-and-empty precedence case, a line break, two argument-count cases and an unknown subcommand, a hand-mangled card file, an unwritable location, and the long and space-padded sides)
  - `a-criterion-about-criteria-is-read` → **pass** (AC8 names AC1 and AC2; each was read against the no-file behaviour and given its own verdict — both hold — and the intersecting executable case is named: `test_the_first_add_creates_the_file_and_its_directory` asserts the new behaviour and both older criteria's observations together, so no non-intersection exists and nothing needed waiving)
  - `tests-would-fail-without-the-change` → **pass, advisory** (eight mutations, one per criterion, each failing the criterion's own named test)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new; `Verified-commit: f22f9c0b0dace18718b02c819984e49d131c8648`)
  - `tracker/items/WI-0001/item.md` — AC1 to AC8 ticked, each on evidence in the report; nothing else in the file changed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0001 passes verification on `f22f9c0`. All eight criteria hold with commands and quoted output; nine negative and boundary conditions were triggered; eight mutations confirmed the tests bite. No defect, no bug item, no send-back. The one declared gap is AC2's literal machine restart, for which the fsync-and-rename syscalls and a post-exit read by another process were substituted.

## 2026-08-30T12:17:47Z — review-close v0.6.0 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` (the only candidate at priority rank 1; EP-001 has no owner at `open`, WI-0002 and WI-0003 rank below it)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1 to AC8 and their tick state
  - `tracker/items/WI-0001/artifacts/verify-report.md` — the evidence behind each tick, and `## Not verified, and why`
  - `tracker/items/WI-0001/artifacts/impl-report.md` — the four declared deviations and `## What I did not do`
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps, the AC mapping, the five assumptions and `## Risks`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md`
  - `tracker/items/WI-0001/journal.md` — all 9 entries, in full — and `history.md` — all 8 rows
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md`
  - the diff `main..wi/WI-0001` (`5c667e02..d12754a7`), hunk by hunk: `recall/store.py`, `recall/cli.py`, `recall/__main__.py`, `tests/test_add.py`, `tests/test_store.py`
  - `docs/architecture/overview.md` and `docs/architecture/adr/` — `ADR-0001`, `ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0007`, `ADR-0008`, each read against the code that implements it
  - `tracker/project.yaml`, `.claude/agile-skills/spec/dor-dod.md` §3, `.claude/agile-skills/spec/doc-header.md` §4b
- **Decisions:**
  - **Accepted and closed as `delivered`.** Every hunk in the diff traces to a plan step and a criterion; the code implements `ADR-0007`'s format and `ADR-0008`'s location and write discipline as written, and contradicts no ADR. The record reconstructs the item end to end without a gap.
  - **Two documented sentences were found false and repaired in place, not parked as a gap.** `overview.md` and `ADR-0008` both said the card file is `$XDG_DATA_HOME/recall/cards.txt` when `XDG_DATA_HOME` is *set*, and that setting `RECALL_CARD_FILE` overrides it. `card_file_path()` treats a variable set to an empty value as unset, which two runs confirmed. The code is right — it is what `plan.md` specified and what the XDG Base Directory Specification asks for — so the prose was the defect. Repaired under `doc-header.md` §4b: `ADR-0008` v1→v3 with two `erratum` entries quoting the removed clauses verbatim in its new append-only `## Corrections` section, and `overview.md` v1→v2. Neither is a supersession, because no reader has to change any code to satisfy the new text. AC5 is unaffected: the path the documentation states and the path the tool uses were, and are, the same.
  - **`cli.main()` not dispatching on the parsed subcommand was recorded, not sent back.** It calls `add()` unconditionally, which is correct while `add` is the only registered subcommand and `argparse` refuses the rest with exit `2` — the behaviour `verify` exercised. No criterion is affected, so it is not a defect in this item; it is a trap for WI-0002, which registers the second subcommand, so it is written into `item.md`'s `## Notes` where WI-0002's plan will meet it.
  - **Three gaps accepted, each written into `item.md`** rather than left in a report nobody reopens: AC2's literal machine restart (substituted by a post-exit read of the exact bytes by a separate process and by `strace` showing `fsync` → `rename` → `fsync`); two `recall` processes writing at once; and a filesystem with no directory `fsync`, together with non-UTF-8 arguments. AC2's substitution was declared by `plan`, `implement` and `verify` in turn, and the review's position is recorded: if anyone reads AC2 as requiring a reboot, the wording is what is revisited with the stakeholder, not the implementation.
  - **No bug item was filed.** The documentation defect belonged to this item's own delivery and was repairable in place; nothing else was found.
  - **The trial merge came before the close, and the close before the real merge.** `commits-reference-the-item` inspects `main..wi/WI-0001`, which is empty once the branch is merged, so merging first would have made the gate refuse the close it is a precondition for.
- **Cross-answer check:** no human answer was consumed by this execution — the two on this item (`WI-0001/Q-001`, `WI-0001/Q-002`) were consumed by `answer-questions` at 11:42:27Z and were read here only as the criteria's provenance. The two documents this execution edited were checked against them and against `EP-001/Q-004`: the correction narrows *when* an environment variable takes effect and touches no commitment the stakeholder was given — the file is still readable text the tool owns (`WI-0001/Q-002`), still at a path the documentation states (`WI-0001 AC5`), and the how-it-is-built delegation (`EP-001/Q-004`) still covers it. `lint-answers --context work-item --changed-since main` → exit 0 over 9 consumed answers, with 2 documents now in the claim window.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0 (verified at `f22f9c0b`; the branch moved to `d12754a7` but the 5 changed files are all under `tracker/`)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 4 commits name WI-0001
  - `git rev-parse main` → `5c667e021aeba6963b59d5cf7d62f050dc963466` (before the trial)
  - `git worktree add --detach /tmp/wi0001-trial main` → exit 0, detached at `5c667e0`
  - `git -C /tmp/wi0001-trial merge --no-ff wi/WI-0001` → exit 0, trial head `c3b2f609467fc83ca8287665261fc1cfb74cd03d`
  - `python3 -m unittest discover -s tests -t . -q` **in the trial worktree** → exit 0, `Ran 26 tests in 1.133s`, `OK`
  - `python3 -m compileall -q recall tests` **in the trial worktree** → exit 0
  - `git worktree remove --force /tmp/wi0001-trial` → exit 0; `git rev-parse main` → `5c667e02` again, unmoved
  - `env -u RECALL_CARD_FILE XDG_DATA_HOME= HOME=/tmp/xdgprobe/home python3 -m recall add bonjour hello` → exit 0, wrote `/tmp/xdgprobe/home/.local/share/recall/cards.txt` — the run that falsified the first documented sentence
  - `env RECALL_CARD_FILE= XDG_DATA_HOME=/tmp/xdgprobe/home2/data python3 -m recall add chat cat` → exit 0, wrote `/tmp/xdgprobe/home2/data/recall/cards.txt` — the run that falsified the second
  - `.claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items and 10 documents, 0 errors 0 warnings
- **Gates:**
  - `definition-of-done` → **pass** (D1 to D12 walked one at a time, each with its own result and evidence, in `artifacts/review.md` `## Definition of Done`. D7 and D12 are the two that did work: D12's nine-claim audit found two false sentences, and D7 records the version bumps and change-log rows that repaired them)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0001 wi/WI-0001` → exit 0; verified at `f22f9c0b`, branch at `d12754a7`, only the record changed between them)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 4 commits on `main..wi/WI-0001`; run before the merge, while that range is still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, 26 tests, run inside the detached trial worktree at `c3b2f60`, which is the merge result and not the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors 0 warnings; it caught two real defects in my own doc repair first — a change log not newest-first, and a correction without its own version — and both were fixed before this entry)
  - `record-is-reconstructible` → **pass** (from the tracker and `git log --grep WI-0001` alone: *what was built* — `plan.md` and the four commits; *which skill decided what* — 9 journal entries across intake, answer-questions ×2, refine ×2, plan, implement ×2, verify; *what questions arose and how they resolved* — `Q-001` and `Q-002`, both answered by the stakeholder with `## Consequences` naming files that exist; *what verification found* — `verify-report.md`, eight criteria with commands and quoted output, nine negative cases, eight mutations)
  - `claims-are-sourced` → **pass** (scope quoted from the gate itself: `lint-claims --context work-item --changed-since main` → *"checked absolute claims: 2 document(s) in 2 path(s) differ from main (5c667e0) under docs; citations: every markdown file in the workspace"*, 0 errors. That window was **empty** when this execution began — this item's branch changed no document — so `--all` was also run, over *"every document under docs"*, likewise 0 errors. The window is non-empty now only because the D12 audit's repairs put two documents in it; the audit itself was a read, not a gate)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0, 9 consumed human answers checked, 2 paths in the claim window)
  - `epic-sign-off` → **skipped** (this is a work item, not an epic; the gate reads an engagement's termination question and there is none to read. EP-001 stays `open` with two children still in flight, and `engagement-state EP-001` reported `active` when `next` dispatched this run)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, the nine-claim D12 audit, D1 to D12, three findings, three accepted gaps, the verdict
  - `tracker/items/WI-0001/item.md` — `status: done`, `outcome: delivered`, and a new `### Carried out of review` block in `## Notes` holding the three accepted gaps and the WI-0002 trap
  - `docs/architecture/adr/ADR-0008-where-the-card-file-lives-and-how-it-is-written.md` v1→v3 — two errata in `## Decision`, a new append-only `## Corrections` section, two change-log rows
  - `docs/architecture/overview.md` v1→v2 — `## Where the cards live` corrected, one change-log row
  - the merge of `wi/WI-0001` into `main`, made immediately after this entry with the subject `merge: the add subcommand and the card file it writes (refs WI-0001)`
  - the record commit `tracker: the review, the closed item and the corrected documents (refs WI-0001)`
- **Status:** `in-review` → `done`
- **Result:** WI-0001 is accepted and closed as `delivered`. All eight criteria hold on evidence a reader can re-run, the trial merge is green on the project's own commands, and the branch is merged into `main`. The review's own work was the D12 claims audit: two sentences in `overview.md` and `ADR-0008` were false for an environment variable set to an empty value, and both were repaired in place with the removed text quoted rather than recorded as a gap the project would carry.
