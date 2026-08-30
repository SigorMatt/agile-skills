# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-30T11:18:28Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** created by `answer-questions` while consuming `EP-001/Q-004`, whose answer widened the scope past what any item recorded (spec/ids-and-statuses.md §5)
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-004.md` (the stakeholder's answer)
  - `tracker/items/EP-001/item.md` (its `## Out of scope`, which excluded deletion)
  - `tracker/items/WI-0001/item.md` (to confirm deletion belonged in neither existing item)
- **Decisions:**
  - Filed deletion as a new work item rather than adding a criterion to WI-0001. Rationale: the stakeholder asked for something the epic had recorded as out of scope, and widening an existing item to swallow it would hide the scope change from the board and from the person who asked for it.
  - Priority `medium`, not `high`. Rationale: it is real work they asked for, but nothing in the first useful version depends on it — WI-0001 then WI-0002 is the path to a tool they can use.
  - Left the three mechanics of deletion — how a card is identified, what happens on no match or several, whether a deletion is confirmed — unwritten and named in `## Notes` for `refine`. Rationale: they depend on what WI-0001 stores, which is not designed yet, and guessing them here would put invented detail in front of the stakeholder as if it were their requirement.
- **Questions raised:** none
- **Commands:**
  - `scripts/new-item --id WI-0003 --type work-item --title "Delete a card" --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from EP-001/Q-004` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass** (this item is itself a consequence named in `EP-001/Q-004`'s `## Consequences`, and it exists)
  - `answered-from-the-record` → **pass** (the stakeholder's own sentence, quoted in `## Notes`: *"I want to be able to delete a card; editing can wait"*)
  - `escalation-is-justified` → **skipped** (nothing was escalated on this item)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item EP-001`, exit 0; the check lives on the answer, on EP-001)
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported on the EP-001 entry for this execution)
  - `item-resumed-correctly` → **skipped** (this item was created, not resumed; it has no `resume-to`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply on EP-001 deferred; all four were answers)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new — story, three acceptance criteria, out of scope, and what `refine` must settle)
  - `tracker/items/WI-0003/history.md`, `tracker/items/WI-0003/journal.md` (new, by `scripts/new-item`)
- **Status:** `—` → `draft`
- **Result:** Deletion, which the stakeholder asked for in `EP-001/Q-004` against an epic that had excluded it, now exists as an item on the board instead of only as a sentence in a question file.

## 2026-08-30T11:34:55Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`. Not dispatched by `next` — the loop had already stopped on the two
  blocking questions `refine` filed on WI-0001. This execution is the harness's batching rule
  (amendment A): file every question that can already be stated before the turn ends, so one
  stakeholder round trip carries them all instead of one per turn. WI-0003 is the next item the
  selection key would reach, it has no unmet dependency, and its questions were already named in
  its own `## Notes`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md` — including `answer-questions`'
    creation entry, which names the three things it deliberately left for this skill
  - `tracker/items/WI-0003/artifacts/` — no `refinement-qa.md` existed; this execution created it
  - `tracker/items/EP-001/questions/Q-001.md` to `Q-005.md` — all five stakeholder answers
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0001/questions/Q-001.md` — filed earlier
    in this turn; its answer decides whether two cards may share a front side, which this item's
    unasked question depends on
  - `tracker/items/WI-0002/item.md` — to place option C of `Q-001` (deleting during a review)
  - `tracker/items/EP-001/item.md`, `docs/product/vision.md` (v3),
    `docs/architecture/adr/ADR-0002-scheduling-binary-ladder.md`,
    `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **Two questions to the stakeholder, one deferred as not-yet-askable, one assumed.** The three
    gaps `answer-questions` left became: how a card is identified (`Q-001`, theirs), what protects
    them from a wrong deletion (`Q-002`, theirs), and what happens on no match or several matches
    (not asked — see below).
  - **Why `Q-001` is theirs and not covered by the standing deferral.** One of its options —
    deleting by a number — only works if the person can see the numbers, which needs a listing that
    no item records. An answer that widens the epic is not a naming decision. The question says so
    plainly and says we would file that listing as its own item rather than smuggle it in here.
  - **Why `Q-002` is theirs.** It settles an `## Out of scope` exclusion that is ours — no undo, no
    trash — which was filed with an explicit note that `refine` must put it to them. And deleting a
    card destroys its rung and its due date as well as its text, which makes it a small instance of
    the failure they named for the whole product: *"losing my progress"* (`EP-001/Q-004`).
  - **Folded confirmation and undo into one question, not two.** They are two answers to one
    worry — how much protection — so splitting them would have produced two questions whose
    answers could contradict each other. Kept strictly out of it: `Q-001`'s identification
    mechanism, which is what would have made this a question that gets half-answered (F-027).
  - **Did not ask what happens when the identifier matches nothing or matches several.** It is
    R10's real gap on this item and it is not answerable yet: whether "several" is even possible
    depends on `Q-001` and on `WI-0001/Q-001`, neither of which is answered. Asking now would be
    asking the stakeholder to reason about a combination of two answers they have not given.
    Recorded in `## Notes` and in the Q&A as `[unresolved]` so that "not yet askable" stays
    distinguishable from "nobody noticed", with what settles each half when the answers land.
  - **Assumed: the subcommand is `delete`, and the confirmation names the card removed.** Basis:
    `EP-001/Q-004`'s standing deferral, and consistency with the `add` subcommand assumed on
    WI-0001 earlier in this turn. Reversible before anything is built.
  - **Recorded R7 as a pass in form and a risk in substance.** The item declares no `depends-on`,
    which is what R7 checks, but deletion cannot be built before cards exist and one answer to
    `Q-001` would make it need WI-0002's session too. That is a sequencing fact for `plan`, not a
    criterion and not a question, so it is written in `## Notes` rather than turned into either.
  - **The acceptance criteria were deliberately not rewritten.** AC1 and AC2 both turn on `Q-001`.
    Rewriting anything now would leave a half-refined item with no record of why.
  - **No Definition of Ready override.** Nothing was passed; the item is suspended.
- **Questions raised:** `WI-0003/Q-001` and `WI-0003/Q-002` — both blocking, both addressed to
  `human`, filed as one round of two and framed as one conversation. One thing left `[unresolved]`
  and not asked: the no-match / several-match behaviour, for the reason above.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 0 consumed human
    answers on this item
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
  - `python3 .claude/agile-skills/scripts/board-gen .` → run after the transition
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 for the state this move produces;
    the one remaining warning is `commands.test` null, which is `plan`'s)
  - `definition-of-ready` → **fail**, criterion by criterion, which is why the item is suspended
    rather than passed: R1 pass (frontmatter, plus `arose-from: EP-001/Q-004`); R2 pass (role,
    capability, "so that"); R3 pass (AC1–AC3, labelled, checkboxes); **R4 fail** — AC1 names no
    command and no way of saying which card, and AC2 is decidable only once AC1 is; R5 pass in
    form, three entries, with the undo exclusion now put to its owner as `Q-002`; **R6 fail** —
    this execution filed two blocking questions; R7 pass in form (no `depends-on`), with the
    sequencing risk recorded in `## Notes`; **R8 fail** — `refinement-qa.md` declares
    `status: agenda`, which by design does not satisfy R8; R9 pass (one command, one behaviour);
    **R10 fail** — the no-match and several-match cases had no stated behaviour anywhere, and are
    now visible rather than decided.
  - `criteria-are-decidable` → **fail** — AC1 is not decidable (no command, no identifier), AC2
    inherits that, AC3 is decidable as written (read the stored file after a deletion and the card
    is absent). Not repaired here because AC1's repair depends on `Q-001`.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0). No human answer
    was consumed, so rule 1 examined nothing on this item; the check that mattered ran the other
    way and is written in `refinement-qa.md` — all five recorded answers read to confirm that
    neither question re-asks something settled, and that `EP-001/Q-004`'s deferral covers the
    subcommand's name but not whether the tool may destroy a card's schedule without asking.
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` exists at `status: agenda`,
    records both questions as `[unresolved]`, the not-yet-askable one as `[unresolved]` with why,
    and the naming decision as `[assumed]` with the deferral it relies on. Every stakeholder
    sentence it uses is quoted.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new) — how a card is identified for deletion
  - `tracker/items/WI-0003/questions/Q-002.md` (new) — what protects against a wrong deletion
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0003/item.md` — `## Notes` rewritten: the two questions, the one that is not
    askable yet and why, the assumption, the R7 sequencing risk, and the per-criterion Definition
    of Ready result. Acceptance criteria untouched.
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0003 is suspended at `awaiting-answer` with `resume-to: draft`, waiting on how a
  card is named for deletion and on what protects against deleting the wrong one. Filed in the same
  turn as WI-0001's two questions so the stakeholder answers four things in one sitting rather than
  two things a turn.

## 2026-08-30T11:46:44Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** `awaiting-answer` with two blocking questions to the stakeholder, both of which now
  carry a reply in `## Answer`. Dispatched by the harness ahead of `next`, which stops the loop on
  any open human-addressed question.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` — both replied to, both blocking
  - `tracker/items/WI-0003/item.md` (AC1–AC3 as found), `history.md` (the suspending row carries
    `resume-to: draft`), `journal.md`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` at `status: agenda`, including its Q3, which
    `refine` recorded as not yet askable
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — every prior recorded stakeholder
    answer
  - `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — **consumed earlier this turn**, and
    the reason Q3 above became answerable
  - `docs/product/vision.md` v4; `ADR-0001-command-line-delivery-surface.md` v1,
    `ADR-0002-scheduling-binary-ladder.md`, `ADR-0003-session-composition-no-cap-stated-count-clean-quit.md`
    v1, `ADR-0004-card-file-is-readable-text-owned-by-the-tool.md` v1
  - `.claude/agile-skills/spec/question.md` §4
  - No `artifacts/plan.md` exists on this item; it has never been planned.
- **Decisions:**
  - **`WI-0003/Q-001` — answered by the human, route: escalation returned.** They chose A:
    *"A — by typing the front side. I don't need a numbered list for this."* Propagated as a
    rewritten AC1, which now names the front side, typed exactly as entered, as the identifier.
  - **The second sentence is read as a decision against the listing, not a postponement.** So no
    work item was filed for one, and `## Out of scope` now excludes any list or search command
    explicitly with their words on it. Filing one would have recorded scope they had just refused,
    which is the mirror of the `spec/ids-and-statuses.md` §5 failure — it hides a scope change on
    the board either way.
  - **`WI-0003/Q-002` — answered by the human, route: escalation returned.** They chose B:
    *"B — show me the card and ask first. One keystroke is worth it to not lose a month of
    progress by fat-fingering a delete."* Propagated as a **new AC2** requiring the tool to display
    the card **and its rung and due date** before removing anything, and to leave the file
    byte-identical on a negative reply. The schedule is in the prompt because the schedule is what
    they call their progress (`EP-001/Q-004`), and it is what a deletion destroys beyond the text.
  - **The undo exclusion is now theirs, not ours.** It stood on this item as intake's inference with
    a note saying `refine` had to put it to them. It has been, and they chose the confirmation over
    the recoverable trash, so `## Out of scope` is rewritten to say so and quote them. A second
    exclusion was added — no force flag, no quiet mode — because removing the prompt they asked for
    would be undoing their decision, and that needs them.
  - **Both answers recorded as `ADR-0005`**, together rather than as two, because they are one
    design: front-side naming is only safe because the tool asks first, and the prompt is the
    mechanism the ambiguity rule extends.
  - **`refinement-qa.md` Q3 — the no-match and several-match cases — decided by the architect,
    route: decided.** `refine` recorded it as genuinely not askable, because whether "several" was
    possible depended on `WI-0001/Q-001`. That answer arrived earlier this turn — two cards may
    share a front side — so the case is real, and `WI-0003/Q-001` stated when it was filed that
    resolving the interaction is ours once both answers were in.
    - **No match → AC5:** nothing removed, the front named, non-zero exit, file unchanged. Word for
      word what `refinement-qa.md` pre-recorded as the decision we would take.
    - **Several matches → AC6:** list every match with both sides, rung and due date, and ask which
      one; exactly the chosen card goes. Refusing on ambiguity was rejected because with no listing
      and no card numbers it would make duplicated cards **permanently undeletable** — withdrawing
      a capability they asked for, on a case their own answer to `WI-0001/Q-001` creates. Deleting
      all matches was rejected as the opposite of what `Q-002` asked for.
    - **Not escalated**, and the four conditions in `spec/question.md` §4 are why: the record is
      not silent (both their answers bear on it and `WI-0003/Q-001` delegated the interaction
      explicitly), the decision is reversible (terminal behaviour, nothing stored changes shape),
      and it contradicts no ADR. Escalating would have put our own reasoning back to them.
  - **The old AC2 and AC3 were renumbered to AC3 and AC4** to make room for the confirmation
    criterion, and AC3 and AC4 were sharpened while renumbering: "the remaining cards keep their
    own scheduling state" now names front, back, rung and due date, and AC4 now says the absence is
    checkable in the stored file by eye, which `ADR-0004` makes possible.
  - **The item resumes to `draft`, not `ready`.** `resume-to: draft` is what the suspending row
    records, and R4 still fails: AC1 and AC2 say "the tool's delete command" and name none. That
    repair is `refine`'s from its own recorded assumption, and this skill does not do another
    skill's work to move the board.
- **Cross-answer check:**
  - `WI-0003/Q-001` — checked against `EP-001/Q-001` (compatible: typing a front side suits *"once
    a day at a terminal"*), `EP-001/Q-004` (compatible; it is the answer this item exists for, and
    its delegation still covers the subcommand's name), `EP-001/Q-005` (compatible: the option that
    would have changed session composition is the one they declined), `WI-0001/Q-001` (compatible
    and **interacting** — shared fronts make a front-side delete ambiguous; resolved as AC6 by our
    own delegated authority, not escalated), `WI-0003/Q-002` (compatible: the prompt is what makes
    front-side matching safe). No conflict.
  - `WI-0003/Q-002` — checked against `EP-001/Q-004` (compatible, and the answer is them applying
    their own *"losing my progress"* failure to a case nobody had put to them), `EP-001/Q-002`
    (compatible, and the reason the prompt shows the rung and due date), `EP-001/Q-005`
    (**compatible, and named because the two pull in opposite directions**: there they refused the
    tool getting between them and their cards, here they asked for a prompt that does. Not a
    contradiction — one is about withholding cards they want to see, the other about destroying a
    card they may not have meant to name, and they said the keystroke is worth it. Nothing was
    reconciled by us), `WI-0001/Q-002` (compatible: a readable file shows what a deletion removed
    as well as what it left). No conflict.
  - Nothing was declared conflicting, so no question was filed under ADR-0008's obligation.
- **Questions raised:** none. Neither answer conflicted with anything the stakeholder had said
  before, and the one thing left undecided when `refine` ran was ours to take rather than theirs.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 consumed human
    answers checked
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition, with
    exactly the two errors the transition clears (`board.stale`, `question.awaiting.none-open`)
  - `python3 .claude/agile-skills/scripts/board-gen .` → run by the transition
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was reopened
    and the change confirmed present: `item.md` (AC1's front-side identifier at line 20, AC2's
    prompt at 24, AC5 at 33, AC6 at 36, and the four `## Out of scope` entries at 45–56),
    `refinement-qa.md` (both verbatim quotes replacing `[unresolved]`, Q3 marked `[decided]` with
    its reasoning, `status: recorded`, six DoR rows updated),
    `ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md` (created, version 1,
    change-log row), `docs/product/vision.md` v5 (the rewritten "Throw a card away" bullet, the new
    no-undo exclusion, the no-browser exclusion re-sourced to their words).
  - `answered-from-the-record` → **pass**. Both stakeholder answers are quoted verbatim and cited
    by question ID wherever used; nothing was paraphrased into a decision. The two things that were
    ours — the no-match rule and the several-match rule — are recorded as ours in `ADR-0005` with
    the options and the rejection reasons, and neither is presented as something they said.
  - `escalation-is-justified` → **skipped**, no question was re-addressed to the human. The one
    candidate — the several-match case — is discussed under Decisions with the §4 conditions tested
    and none met.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 for the state this move produces;
    the remaining warning is `commands.test` null, which is `plan`'s to fill).
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-30T11:34:55Z records
    `resume-to: draft`; this execution moves the item to `draft`.
  - `a-deferral-is-not-an-answer` → **skipped**, neither reply defers. Each names an option letter
    and gives a reason, and *"I don't need a numbered list for this"* is a refusal rather than a
    postponement — recorded as an exclusion, not as work waiting to be scheduled.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at`, `## Cross-answer check` and `## Consequences` written
  - `tracker/items/WI-0003/questions/Q-002.md` — the same
  - `tracker/items/WI-0003/item.md` — **AC1 rewritten**, **AC2, AC5 and AC6 added**, old AC2/AC3
    renumbered to AC3/AC4 and sharpened, three `## Out of scope` entries added or rewritten,
    `## Notes` rewritten
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; both answers
    verbatim; Q3 moved from not-askable to `[decided]`; the R3, R4, R5, R6, R8 and R10 rows updated;
    the sequencing risk narrowed now that option C is off the table
  - `docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md` —
    **created**, version 1
  - `docs/product/vision.md` — version 4 → **5**, `updated-for: WI-0003`, change-log row added
  - `tracker/board.md` — regenerated by the transition
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of the stakeholder's replies on WI-0003 are consumed and propagated: a card is
  deleted by typing its front side, the tool shows it and its schedule and asks first, and deletion
  is permanent by their choice rather than our inference. The two cases `refine` could not ask about
  are now decided as AC5 and AC6, because `WI-0001/Q-001`'s answer made them answerable. The item
  returns to `draft`, its recorded `resume-to`, with one Definition of Ready failure left for
  `refine`: AC1 and AC2 still name no command.

## 2026-08-30T13:00:10Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` as the only runnable item (WI-0001 and WI-0002
  are `done`, EP-001's `open` has no owner). This is `refine`'s second execution on this item: the
  first suspended it at `awaiting-answer`, `answer-questions` consumed both stakeholder answers and
  returned it to `draft` with one Definition of Ready criterion still failing.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (AC1–AC6 as `answer-questions` left them), `history.md` (three
    rows: created, suspended with `resume-to: draft`, resumed), `journal.md` (all three entries)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` at `status: recorded`, including Round 1's
    per-criterion table and its Q4, which pre-recorded the repair this execution owed
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` — both answers read verbatim
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — every prior stakeholder answer, for
    the standing deferral in `Q-004` and for the cross-answer check
  - `tracker/items/WI-0001/item.md` (AC1–AC8 as delivered) and `tracker/items/WI-0002/item.md`
    (AC1–AC14 as delivered) — the criteria this item's must not contradict, and the source of the
    prompt conventions it copies
  - `docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md` (v1),
    and `ADR-0007` and `ADR-0002` where AC8 and AC2 cite them
  - `recall/cli.py` and `recall/store.py` — read to state the criteria against the tool that
    exists (`_ask`'s re-prompting, `PROMPT_MARK`, the `y`/`n`/`q` vocabulary, the parse refusal in
    `main()`), so that a criterion says what would be observed rather than what might be built
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Repaired R4 without asking anyone.** AC1 and AC2 now name the `delete` subcommand, its one
    argument, the answers its prompt takes and the exit code of each outcome. Authority: the
    stakeholder's standing deferral *"As for how it's actually built — whatever you think is
    best"* (`EP-001/Q-004`), which the procedure applies to the category — names, wording, exit
    codes — and which Round 1 of the Q&A had already recorded as covering exactly this repair.
  - **Confirmation takes `y` and `n`, and says so.** Rationale: it is the vocabulary the
    stakeholder already meets at WI-0002's outcome prompt, so the two commands feel like one tool.
    Declining exits **zero**, because `ADR-0005` calls a negative reply an ordinary outcome and not
    an error.
  - **AC6's several-match prompt numbers the matches from 1 in card-file order and takes that
    number, or `n`.** `ADR-0005` decided the shape — list them and ask which — and left unsaid how
    a person names one of them. Something had to say it. Checked explicitly against the
    stakeholder's *"I don't need a numbered list for this"* (`WI-0003/Q-001`) and recorded as
    compatible with reasons rather than reconciled: their sentence refuses option B of that
    question — a persistent card number, with a listing command to see it, as the way a card is
    named — whereas these numbers exist only inside one prompt, name only the cards already on
    screen, and are unusable anywhere else. Not escalated: the sentences do not contradict, and the
    mechanism was delegated to us in writing by the same question their sentence answers.
  - **AC7 — the input stream ending at a delete prompt means "delete nothing", not "delete".**
    This deliberately differs from WI-0002, where a closed stream is a clean quit (`WI-0002` AC11),
    and the difference is recorded as ours: stopping a review costs nothing, while the act being
    confirmed here is irreversible by the stakeholder's own decision (`WI-0003/Q-002`). The
    re-prompting half of AC7 copies `WI-0002` AC13 unchanged.
  - **Added AC7, AC8 and AC9 for combinations nobody had named** — unrecognised input and a closed
    stream at either prompt; an unparseable card file; the wrong argument count and an empty
    argument. R10 does not require them to be decided, only visible; they are cheap now and each
    one is a place two implementations would otherwise diverge. AC8 states the refusal `add` and
    `review` already make rather than inventing a new one, and cites `ADR-0007` and `WI-0002` AC14
    so the three commands cannot drift apart quietly.
  - **Folded the empty file and the missing file into AC5**, and the last-card-deleted case into
    AC4, rather than making each its own criterion — they are the same observation as a no-match
    and the same observation as a survived restart, and splitting them would pad the item without
    adding a decision.
  - **Sharpened AC3 so it is decidable without reading another item's tests.** "Never offered
    again" is now a run of `review` on a date at or after the deleted card's stored due date, plus
    the session's stated count being one lower — both things a person with a terminal can see.
  - **Declared `depends-on: WI-0001`.** Round 1 recorded the sequencing as prose because the field
    was empty and the dependency was unfinished; WI-0001 is now `done`, so the field is both true
    and free. R7 moves from a pass in form to a pass in substance.
  - **Added one `## Out of scope` entry:** deleting a card from inside a review session — option C
    of `Q-001`, which the stakeholder did not choose. It says in terms that `review` is untouched
    by this item, which is what keeps `WI-0002`'s fourteen criteria true after this one ships.
  - **Asked the stakeholder nothing, and filed no question.** Every remaining gap failed the
    product-stake test in the procedure's step 3: a name, a keystroke, an exit code. The two things
    that were theirs — how a card is named and whether they are asked first — are `Q-001` and
    `Q-002`, and both are answered.
  - **No Definition of Ready override.** Nothing was waived; all ten criteria pass on their own
    terms.
  - **Wrote to no document.** Everything decided here sits under `ADR-0005` as it already stands.
    Had any of it needed that ADR changed, this skill would have filed a question to the architect
    rather than editing it.
- **Questions raised:** none. One assumption — AC6's numbering — was checked against a
  stakeholder sentence it brushes against and recorded as compatible in
  `artifacts/refinement-qa.md` under Q6 and in `## Cross-answer check`, rather than escalated.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (before editing)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, "board already current"
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → exit 0, "EP-001 active — still
    in flight: WI-0003" (run by `next`, quoted here because it is why this item was dispatched)
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 consumed human
    answers checked
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after editing, 4 items,
    11 documents, 0 errors, 0 warnings
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors and 0 warnings both before
    and after the edits)
  - `definition-of-ready` → **pass**, criterion by criterion:
    **R1 pass** — `id`, `type`, `title`, `status`, `priority`, `epic`, `created`, `updated` all
    present; `type: work-item`, `epic: EP-001`, `priority: medium` set; plus `arose-from` and now
    `depends-on`.
    **R2 pass** — "As someone studying a subject" (role), "I want to delete a card I no longer
    want" (capability), "so that a card I entered by mistake or no longer need stops coming up in
    my daily review" (outcome).
    **R3 pass** — AC1–AC9, each labelled `AC<n>`, each an unticked checkbox.
    **R4 pass** — was the failing one. Every criterion now names a command and an observation: AC1
    `delete <front>` then `y` → confirmation naming the front, exit 0; AC2 the four values printed
    and the two answers stated, `n` → file byte-identical, exit 0; AC3 a `review` run and its
    stated count; AC4 the stored file read afterwards, plus a `review` and an `add`; AC5 no prompt,
    a message naming the front, non-zero exit, file byte-identical; AC6 the numbered list and the
    number typed; AC7 the re-prompt and the closed stream; AC8 the parse refusal naming file and
    line; AC9 the usage message and the non-zero exit. No unmeasurable adjective survives — the
    words checked for were "appropriate", "reasonable", "clean", "properly", "gracefully", and none
    appears.
    **R5 pass** — `## Out of scope` has six entries, four of them things a reader could reasonably
    assume were included: editing, undo/trash, a list or search command, and deleting from inside a
    review session.
    **R6 pass** — both questions on this item are `status: answered`; none is open, blocking or
    otherwise.
    **R7 pass** — `depends-on: WI-0001`, and WI-0001 is `done`.
    **R8 pass** — `artifacts/refinement-qa.md` declares `status: recorded` and now holds both
    rounds: two stakeholder answers verbatim and tagged `[human]`, four assumptions tagged
    `[assumed]` with the deferral each rests on, one earlier item tagged `[decided]`.
    **R9 pass** — one subcommand, one file, one behaviour; nothing here splits.
    **R10 pass** — every combination this item introduces has a stated behaviour: match ×1 (AC1,
    AC2), ×0 (AC5), ×many (AC6); yes / no / unrecognised / stream-closed at each prompt (AC2, AC6,
    AC7); card file absent, empty, unparseable (AC5, AC8); argument absent, doubled, empty (AC9);
    file after the last card goes (AC4); and the interaction with `review`, named in
    `## Out of scope` as none.
  - `criteria-are-decidable` → **pass**. For each: AC1 `delete <front>` on a one-match deck,
    answer `y`, read stdout and `$?`; AC2 the same up to the prompt, answer `n`, `cmp` the file
    against a copy taken before; AC3 delete, then `review` on a date at or after the stored due
    date, count the offered cards and read the stated total; AC4 delete, exit, `cat` the card file,
    then `review` and `add` on the emptied file; AC5 `delete` a front no record holds, read stderr
    and `$?`, `cmp` the file; AC6 seed two records sharing a front, `delete` it, read the numbered
    list, type `1`, `cmp` the survivor's record; AC7 type `maybe` then Ctrl-D, read what is
    reprinted and `cmp` the file; AC8 corrupt one line of the card file, `delete`, read the message
    and `$?`; AC9 `delete` with no argument and with two, read the usage message and `$?`. Each
    yields one verdict a stranger with a terminal would reach the same way.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0, 2 consumed human
    answers). The substantive check is written out in `refinement-qa.md`'s `### Round 2's check`:
    every assumption read against `EP-001/Q-004`, `WI-0003/Q-001`, `WI-0003/Q-002`,
    `WI-0001/Q-001` and WI-0002's delivered criteria. One near-conflict — AC6's numbering against
    *"I don't need a numbered list for this"* — argued as compatible in the Q&A, by ID, with the
    scope of their sentence stated rather than assumed away. Nothing of theirs was edited.
  - `qa-recorded-verbatim` → **pass**. Both stakeholder answers are quoted word for word and
    tagged `[human]`; every decision this execution took is tagged `[assumed]` with the deferral it
    relies on named; nothing was paraphrased into agreement, and no answer was invented for a
    question that was never asked — the four Round 2 entries say "Not asked" in bold.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — AC1 and AC2 rewritten to name the command and its prompt,
    AC3–AC6 sharpened, AC7, AC8 and AC9 added, one `## Out of scope` entry added,
    `depends-on: WI-0001` declared, `## Notes` rewritten
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — Round 2 added (four `[assumed]` entries
    and what this round did not do), the R4, R7 and R10 rows of Round 1's table updated, the R7
    risk section marked closed, `### Round 2's check` appended to `## Cross-answer check`
  - `tracker/board.md` — regenerated by the transition
  - commit: `tracker: the refined item and its Q&A record (refs WI-0003)`
- **Status:** `draft` → `ready`
- **Result:** WI-0003 is Ready. Delete is a `delete` subcommand taking the front side, which shows
  the card and its schedule and asks before removing anything, and nine criteria say what happens
  when there is no match, several matches, an unrecognised keystroke, a closed input stream, a
  broken card file or a wrong argument count. The one Definition of Ready failure the item came
  back with — criteria naming no command — is repaired from the stakeholder's standing deferral,
  and no new question was put to them.

## 2026-08-30T13:04:28Z — plan v0.4.1 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` as the only runnable item — WI-0001 and
  WI-0002 are `done`, EP-001's `open` has no owner, and `engagement-state EP-001` reports the
  engagement active with WI-0003 still in flight.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1 to AC9 as `refine` left them an hour earlier, the six
    `## Out of scope` entries, `depends-on: WI-0001`, and the `## Notes` list of what was assumed
    under the stakeholder's standing deferral
  - `tracker/items/WI-0003/history.md` (four rows) and `journal.md` (four entries). This item was
    never rejected by `verify` or `review-close`, so this is a first plan and not a re-plan.
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — both rounds. Round 2's four `[assumed]`
    entries are the soft ground this design stands on and each is carried forward explicitly.
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — the two stakeholder answers verbatim
  - `tracker/items/EP-001/questions/Q-004.md` — the standing deferral this plan's wording
    assumptions rest on
  - `tracker/items/WI-0001/item.md` (AC1–AC8 delivered), `tracker/items/WI-0002/item.md` (AC1–AC14
    delivered, plus the four accepted gaps in its `## Notes`), and
    `tracker/items/WI-0001/artifacts/review.md` for the `main()` dispatch trap
  - `docs/architecture/overview.md` v4, and the ADRs by number: `ADR-0001` (command line),
    `ADR-0002` (the ladder and the due rule), `ADR-0004` (a readable file the tool owns),
    `ADR-0005` (all of deletion's behaviour), `ADR-0006` (Python 3, stdlib only, and the gate
    commands), `ADR-0007` (the file format), `ADR-0008` (where the file lives and how it is
    written), `ADR-0009` (the ladder lives in its own module)
  - the code this change touches and what it depends on: `recall/cli.py` in full — `_ask()`'s
    re-prompt and EOF behaviour, `add()`'s use of the loaded list, `_parser()`, `main()`'s
    dispatch and its `CardFileError` handler; `recall/store.py` in full — `card_file_path()`,
    `load()` returning `[]` for a missing file, `save()`'s temp-file-and-rename, `_parse()`'s
    error messages; `recall/schedule.py` (positions, not cards, and why); `recall/__main__.py`;
    `tests/test_review.py`'s harness, which `tests/test_delete.py` will copy
  - `tracker/project.yaml` — both commands already resolved
- **Decisions:**
  - **No new module, and no new ADR.** `delete` is a third subcommand on the seam that already
    exists: `cli.py` owns the conversation and the exit code, `store.py` owns the file, and
    `schedule.py` is not touched because deletion applies no rule of the ladder's. Branch of the
    preference order: **documented** — `docs/architecture/overview.md` v4 already says later items
    are expected to add subcommands rather than reshape the tool, and `ADR-0005` already decides
    every behaviour this item has. Writing an ADR to record "the third subcommand goes where the
    first two are" would pad the trail and hide the real decisions in it.
  - **The matching lives in `cli.py` as a list of positions, not as a new `store` function.**
    Branch: **assumed**, recorded as `## Assumptions` 1 with its reversal cost — moving one list
    comprehension and one `del` into `store.remove()`, one file, no stored data, no published
    interface. Rationale: `add()` already mutates the loaded list in place, so this keeps the seam
    where the overview describes it.
  - **Positions rather than card objects, carried across the prompt.** Branch: **documented** —
    `WI-0001` AC6 allows two cards to share a front side, and `recall/schedule.py` already solved
    the identical hazard the identical way for the review session. This is the one thing in the
    item that could silently delete the wrong record, and it is the reason `## Problem` names it.
  - **Front matching is exact string equality on the stored value** — no strip, no case folding,
    no normalisation. Branch: **documented, then recorded as an assumption** (`## Assumptions` 2)
    because the code has to state it: `ADR-0007` stores a side verbatim and `WI-0001` AC2 promises
    it reads back byte-identical, so a looser match would find a card the person did not type.
    Loosening it later would change which card a typed front finds, which is the stakeholder's
    call, not ours.
  - **`_ask()` is reused unchanged, and that is what makes AC7 nearly free.** It already re-asks by
    reprinting the whole prompt string it was given, so putting the card block inside the prompt
    satisfies AC7's "reprint the card" without new code. Branch: **documented** — read out of
    `recall/cli.py`.
  - **`delete` treats the end of the input stream as `n`, where `review` treats it as `q`.**
    Branch: **documented** — this is `WI-0003` AC7, decided by `refine` under the standing
    deferral and recorded in the Q&A with its reason: stopping a review costs nothing, while the
    act being confirmed here is irreversible by the stakeholder's own decision. The plan does not
    re-decide it; it implements it.
  - **No validation of the argument.** An empty or whitespace-only front falls through to AC5's
    no-match, because `WI-0001` AC7 makes an empty side unstorable. Branch: **documented** —
    `WI-0003` AC9 says exactly this. A second refusal path would produce a message for a case AC5
    already covers.
  - **argparse owns the wrong-argument-count behaviour** (usage message naming `delete`, exit 2),
    as it already does for `add`. Branch: **documented**, from `recall/cli.py`.
  - **`main()` is rewritten as an explicit three-way dispatch** rather than a chain ending in a
    bare `return add(...)`. Branch: **documented** — `WI-0001`'s review recorded that trap and
    `WI-0002` had to disarm it; leaving the shape in place would re-arm it for the fourth
    subcommand.
  - **Prompt wording and the numbering from 1** are assumptions 3 and 4, resting on the
    stakeholder's *"whatever you think is best"* and on AC6 respectively. The criteria constrain
    what the text must contain — the four values, the accepted answers, the front side — not the
    exact sentences, so rewording later breaks no criterion.
  - **`docs/architecture/overview.md` was deliberately not touched.** This change adds no module,
    moves no seam and changes no stored format, so there is nothing to bump. The document already
    names `delete` as the third subcommand and says it is not yet built, which is still true while
    this item is only planned. Updating it to describe behaviour that does not exist is exactly the
    staleness `WI-0002`'s close had to repair. When `delete` is merged, D7 and D12 put the update
    at `review-close`'s gate, which is where `spec/doc-header.md` §5 allows it.
  - **`tracker/project.yaml` was not changed.** `commands.test` and `commands.lint` were filled in
    at `WI-0001`'s planning and both are commands this project actually runs; `commands.build` is
    `null` and honestly so, since there is nothing to build (`ADR-0006`).
  - **No step tells a downstream skill to do something its contract forbids.** Step 9 says in
    terms that `implement` leaves the criteria unticked because ticking is `verify`'s, and no step
    asks `implement` or `verify` to write to `docs/`.
- **Cross-answer check:** this execution recorded no new human answer and took no decision that
  rests on one it had not already been given. Checked against by ID anyway, because the plan quotes
  and relies on them: `EP-001/Q-004` — the standing deferral, which authorises assumptions 1 to 3
  and nothing more; `WI-0003/Q-001` — *"by typing the front side… I don't need a numbered list for
  this"*, compatible with the design, which adds no listing command and no persistent card number,
  and whose one point of contact with AC6's in-prompt numbering was checked and recorded as
  compatible by `refine` rather than reconciled here; `WI-0003/Q-002` — *"show me the card and ask
  first"*, which the single-match and several-match prompts both implement and which nothing in the
  plan weakens; `WI-0001/Q-001` — two cards may share a front, which is why the design carries
  positions and not cards; `WI-0001/Q-002` — a readable file, unchanged by this item. No conflict
  found, so nothing was escalated under ADR-0008 §3 and no document of theirs was edited.
- **Questions raised:** none. Nothing this design forced was irreversible or depended on intent the
  record does not hold — the two things that were theirs were answered before `refine` finished,
  and the rest is wording, placement and a comparison operator, each recorded as a reversible
  assumption with its reversal cost.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (before writing)
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, "0 uncommitted
    path(s) under docs", 9 consumed human answers checked across the workspace
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, "0 document(s) in 0
    uncommitted path(s) under docs; citations: every markdown file in the workspace"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 11 documents,
    0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors and 0 warnings, before and
    after)
  - `every-criterion-is-addressed` → **pass**. `plan.md`'s `## Acceptance criteria mapping` has one
    row per criterion, AC1 to AC9, nine rows for nine criteria, each naming the step that satisfies
    it and a specific demonstration rather than the word "tests": AC1 → steps 4, 6, stdout
    `Deleted:` and the survivor in the file; AC2 → 2, 4, the prompt's four values and a byte
    comparison after `n`; AC3 → 4, 5, `review`'s stated count dropping to 2 and the survivors'
    fields; AC4 → 4, no `front:` line left plus a working `review` and `add` on the emptied file;
    AC5 → 3, three seedings (populated, empty, absent) each asserting no prompt and unchanged
    bytes; AC6 → 5, three cards sharing a front, answer `2`, the other two byte-identical; AC7 →
    4, 5, `maybe\nn\n` producing the card block twice, and a closed stdin at both prompts; AC8 → 3,
    a corrupt `rung:` line, the path and line number in stderr, no prompt; AC9 → 6, 3, argparse's
    usage message and the empty-argument no-match. No criterion is unmapped and no step is
    unmapped to a criterion.
  - `project-commands-resolved` → **pass**, and unchanged by this execution.
    `commands.test: python3 -m unittest discover -s tests -t . -q` and
    `commands.lint: python3 -m compileall -q recall tests` are both real commands that run in this
    checkout — they were run green sixty tests over at `WI-0002`'s close and step 8 requires them
    green on this branch head. `commands.build: null` is honest: `ADR-0006` records that the
    project is standard-library Python run from a checkout with no build step.
  - `decisions-recorded` → **pass**. `plan.md`'s `## Decisions and ADRs` is a table with a row per
    choice and the branch of the preference order it came from: five rows resolved from documents
    and cited by ADR number, one row pointing at `## Assumptions` 1 to 4, each of which states what
    reversal would cost, and one row recording that nothing was asked of the human and why. No
    decision in the plan is absent from that table.
  - `plan-is-executable-without-you` (advisory) → **pass**. Read cold, each of the nine steps names
    the file it touches and what is true afterwards; the three functions it adds are given their
    signatures and their return values; the three branches of `delete()` are enumerated with the
    exact exit code and stream for each. The one place a reader could still have to choose — the
    literal prompt sentences — is fixed in `## Approach` and marked in `## Assumptions` 3 as
    wording rather than contract. No implementation body is written into the plan.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0). The substantive
    check is the `**Cross-answer check:**` bullet above: five prior answers read by ID, all
    compatible, nothing reconciled here.
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0). Worth a reader's
    attention: the absolute-claim half of that gate examined **zero documents**, because this
    execution wrote nothing under `docs/` — the F-066 shape reported at both of `WI-0002`'s gates,
    seen here from the other side. The citation half did run across every markdown file in the
    workspace, so `plan.md`'s roughly forty `[src: …]` pointers were each resolved. The claims in
    `docs/` about the behaviour this item touches were read by hand instead: `overview.md` v4's
    `## How it is run` names `delete` as a subcommand of WI-0003 that is not yet built, which is
    still true, and its `## Where the cards live` and `## What the card file looks like` describe a
    file this item reads and rewrites without changing.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new) — problem, approach, nine steps, the AC mapping
    table, four assumptions with reversal costs, the decisions table, `## Scaffolding` = none, four
    risks, and what is out of scope for this item
  - `tracker/board.md` — regenerated by the transition
  - no ADR created, no document under `docs/` touched, `tracker/project.yaml` unchanged
  - commit: `tracker: the plan for delete, no new ADR, no document changed (refs WI-0003)`
- **Status:** `ready` → `planned`
- **Result:** WI-0003 is planned. `delete` is a third subcommand in `recall/cli.py` reusing
  `_ask()` and `store.save()` unchanged, carrying card **positions** across the confirmation so
  that two cards sharing a front side cannot be confused, with nine steps and a demonstration for
  each of the nine criteria. No new module, no new ADR, no document updated, and no question put to
  the stakeholder — every decision was either already recorded or is a reversible assumption with
  its reversal cost written down.

## 2026-08-30T13:05:12Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next`. A fresh start, not a resumption:
  `git branch` listed only `main`, `wi/WI-0001` and `wi/WI-0002` before this execution, and
  `history.md`'s last row is `plan`'s `ready → planned`, not a send-back from `verifying` or
  `in-review`.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1 to AC9, the six `## Out of scope` entries,
    `depends-on: WI-0001`
  - `tracker/items/WI-0003/artifacts/plan.md` — the whole of it: nine steps, the AC mapping table,
    four assumptions with their reversal costs, the decisions table, `## Scaffolding` = none
  - `tracker/items/WI-0003/history.md` (five rows) and `journal.md` (five entries)
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both `answered` before `refine`
    finished, both already propagated into the criteria and into `ADR-0005`; nothing has moved to
    `answered` since the last journal entry, so there is no new answer to re-read
  - `docs/architecture/adr/ADR-0005` (all of deletion's behaviour), `ADR-0007` (the file format),
    `ADR-0008` (the path and the atomic rewrite), `ADR-0002` (the ladder the prompt displays)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` both set, `conventions.branch-prefix`
    `wi/`, `conventions.commit-subject`
  - the code to be changed: `recall/cli.py`, `recall/store.py`, `recall/schedule.py`, and
    `tests/test_review.py` for the test harness this item's tests will copy
- **Decisions:**
  - Branched `wi/WI-0003` from `main` at `3e9c1df`, which is `plan`'s commit and the trunk head —
    step 1 of the plan.
  - Moving to `in-progress` before writing any code, so that an interruption leaves a status that
    matches the branch rather than one that claims nothing has started.
  - No deviation from the plan decided yet; any that arises will be recorded in `impl-report.md`
    and in the closing entry.
- **Cross-answer check:** none — this execution has edited nothing under `docs/` and has written no
  claim sourced to a stakeholder answer.
- **Questions raised:** none
- **Commands:**
  - `git switch -c wi/WI-0003` → exit 0, branch created at `3e9c1df`
  - `git branch --show-current` → `wi/WI-0003`
- **Gates:** none of the completion gates has run yet, which is the truth at this point in the
  execution; all eight are recorded on the closing entry.
  - `tests-pass` → **not yet run** (no code has changed)
  - `lint-clean` → **not yet run**
  - `workspace-valid` → **not yet run** for the completing state; it passed for the state this move
    produces, as the transition's own hard gate
  - `every-criterion-has-a-test` → **not yet run** (no test written)
  - `commits-reference-the-item` → **not yet run**; the branch has no commit of its own yet, so the
    check has nothing to look at
  - `no-unplanned-scope` (advisory) → **not yet run** (empty diff)
  - `cross-answer-consistency` → **not yet run**
  - `claims-are-sourced` → **not yet run**
- **Artifacts:**
  - branch `wi/WI-0003`, created at `3e9c1df`, no commit of its own yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0003 has started on `wi/WI-0003`. Nothing is built; the next
  entry reports the work.

## 2026-08-30T13:11:45Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, this execution's own opening move. The nine steps of
  `plan.md` are executed and the report is written.
- **Inputs read:**
  - `tracker/items/WI-0003/artifacts/plan.md` — worked step by step, in order
  - `tracker/items/WI-0003/item.md` — AC1 to AC9, unchanged by this execution
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md` — both `answered` before `refine`
    finished; nothing moved to `answered` during this execution, so no artifact needed re-reading
  - `recall/cli.py`, `recall/store.py`, `recall/schedule.py`, `recall/__main__.py`
  - `tests/test_review.py` — the harness `tests/test_delete.py` copies
  - `docs/architecture/adr/ADR-0005`, `ADR-0007`, `ADR-0008`, `ADR-0002`;
    `docs/architecture/overview.md` v4 and `docs/product/vision.md` v6, read for the D12 hand check
  - `tracker/project.yaml` — both gate commands
- **Decisions:** all inside the plan's latitude; each is in `impl-report.md` too.
  - **Split the prompting out of `delete()` into `_confirmed()` and `_chosen_among()`.** The plan
    described three inline branches. Both prompts return the same thing — a position or nothing —
    and folding them in made the removal path read as though it might run twice. Nothing observable
    changes: same prompts, same accepted answers, same exit codes. `how`, not `what`, so no
    question. Recorded as the execution's one deviation.
  - **`main()` ends in an unreachable `AssertionError` rather than a bare `return`.** The plan asked
    for an explicit branch per subcommand with no fall-through; something has to be at the end, and
    falling off the end of `main()` would return `None` and exit 0. Failing loudly is the honest
    version of what the plan asked for, and it is the trap `WI-0001`'s review recorded.
  - **`_rung()` prints `"0 of 4 (never answered)"` rather than a bare `0`.** AC2 says the prompt
    shows "the rung it has reached"; a card `add` has just written has reached none, and `0` alone
    would read as a rung. Wording, under the standing deferral the plan's assumption 3 records.
  - **The near-miss test is four sub-tests, not one.** `Bonjour`, ` bonjour`, `bonjour ` and
    `bonjou` each pin one thing the plan's assumption 2 rules out — case folding, leading and
    trailing whitespace, and a prefix. One test would have passed with three of the four still
    broken.
  - **Decided nothing that was not mine.** No decision arose that the plan does not make: every
    behaviour is in a criterion or in `ADR-0005`. Nothing was escalated because nothing needed to
    be, not because escalating felt like failure — the one thing this execution found that is not
    mine to do is the `overview.md` repair, and that is declared as a handover rather than guessed
    at.
- **Cross-answer check:** `none`. This execution edited no file under `docs/` at all, so it
  rewrote no sentence sourced to a stakeholder answer and ADR-0008 §3's refused repair did not
  arise. The two sentences it found false — in `docs/architecture/overview.md` v4 — are sourced to
  `WI-0003` and to `recall/cli.py`, not to any answer of theirs, and they are false because the
  code changed, which is the ordinary D12 repair; it is handed to `review-close` only because
  `spec/doc-header.md` §5 forbids this skill from writing to `docs/`, not because it is contested.
- **Questions raised:** none.
- **Commands:**
  - `git switch -c wi/WI-0003` → exit 0 (opening entry), branch at `3e9c1df`
  - `python3 -m unittest discover -s tests -t . -q` → run repeatedly through the work; final run on
    the branch head `fe70136`: `Ran 90 tests in 4.45s … OK`, exit 0
  - `python3 -m compileall -q recall tests` → exit 0, no output
  - seven mutation runs of the test command against a deliberately broken `recall/cli.py`, the file
    restored from a copy after each → `FAILED` with 8, 2, 4, 1, 9, 3 and 30 failures respectively;
    the restored file → `OK`
  - `git commit` → `fe70136 feat: delete a card by its front side, after showing it and asking
    (refs WI-0003)`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 1
    commit(s) on main..wi/WI-0003 name WI-0003"
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, "0 path(s)
    differ from main (3e9c1df) under docs", 9 consumed human answers checked
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, "0
    document(s) in 0 path(s) differ from main"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 11 documents
  - manual runs of the tool against a hand-seeded deck before the tests were written: single-match
    `y`, several-match with an unrecognised key then `2`, no match, end-of-stream, no argument, and
    `add`/`review` afterwards — each behaving as the criteria describe
- **Gates:** all eight, on the branch head `fe70136`, after the last change.
  - `tests-pass` → **pass** (`Ran 90 tests … OK`, exit 0; 60 inherited, 30 new)
  - `lint-clean` → **pass** (`compileall`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass**. `impl-report.md`'s table gives AC1 to AC9 a named test
    method each, never "see the code": AC1 → `DeletingTests.test_a_confirmed_delete_removes_the_card_and_names_it`;
    AC2 → five `ConfirmationTests`, including one that reads the card file from **outside** the
    running process while the prompt waits; AC3 → `NeverOfferedAgainTests`, which runs a real
    `review` before and after and compares the stated counts; AC4 → `PersistenceTests`, including a
    `review` and an `add` against the file left behind when the last card goes; AC5 → four
    `NoMatchTests` covering a populated file, an empty file, no file, and four near misses; AC6 →
    five `SeveralMatchesTests`; AC7 → five `PromptInputTests`; AC8 →
    `UnparsableFileTests.test_an_unparsable_file_stops_before_any_prompt`; AC9 → three
    `ArgumentTests`. **And the tests were checked for bite**: seven mutations of `recall/cli.py`
    each turned the suite red, and the restored file green.
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0)
  - `no-unplanned-scope` (advisory) → **pass**. `main..wi/WI-0003` is two files: `recall/cli.py`
    (+97, five new functions and two edits, every hunk traceable to plan step 2, 3, 4, 5 or 6) and
    `tests/test_delete.py` (new). No neighbouring code tidied, no unrelated defect fixed, no file
    outside `recall/`, `tests/` and `tracker/` created.
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main`, exit 0)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0) — **and it looked
    at nothing.** It reported "0 document(s) in 0 path(s) differ from main" and exited 0, which is
    the F-066 shape reported at both of `WI-0002`'s gates and now at this one: a work item's branch
    changes no document by construction, because `plan` writes its ADRs on the trunk before the
    branch exists and `spec/doc-header.md` §5 forbids this skill from writing to `docs/` at all.
    The twelve documents were therefore read by hand against the branch, and the result is in
    `impl-report.md`: `vision.md` v6's deletion bullet and its exclusions are true and now
    demonstrably so, `ADR-0005`, `ADR-0007` and `ADR-0008` are true in every clause, and
    **`overview.md` v4 has two sentences that are now false** — its opening line saying `delete` is
    *"not yet started"*, and `## How it is run` saying `delete` is *"named here so a reader can see
    where it will attach"*. Declared as a D7/D12 obligation for `review-close` rather than repaired,
    because §5 names this skill as one that does not write to `docs/`.
- **Artifacts:**
  - `recall/cli.py` — `_rung()`, `_described()`, `_confirmed()`, `_chosen_among()`, `delete()`; the
    `delete` subparser; `main()` rewritten as one explicit branch per subcommand
  - `tests/test_delete.py` (new) — 30 methods in 10 classes over AC1 to AC9, plus one regression
    guard for the rewritten `main()`
  - `tracker/items/WI-0003/artifacts/impl-report.md` (new)
  - branch `wi/WI-0003`, commit range `main..wi/WI-0003` = `fe70136` (one commit)
- **Status:** `in-progress` → `verifying`
- **Result:** `delete` is built, tested and green on `wi/WI-0003`. Nine criteria, thirty tests, all
  eight gates passing on the branch head, and seven mutations confirming the tests bite. One
  deviation from the plan, recorded: the prompting is two helper functions rather than two inline
  branches. Nothing is ticked in `item.md` — that is `verify`'s — and `docs/architecture/overview.md`
  needs two sentences repaired at `review-close`'s D7 and D12, which this skill is not permitted to
  do and has declared instead.

## 2026-08-30T13:20:01Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying` — `implement` reported the build complete on `wi/WI-0003`; `next` dispatched this skill as the owner of that status, with no request open and no question open anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the nine acceptance criteria, read **first and in full**, before the implementation report was opened, so that what would settle each one was derived from the criterion rather than from what was built.
  - `tracker/items/WI-0003/artifacts/plan.md` — the nine steps, the criteria mapping and the four reversible assumptions, read to judge the diff against something.
  - `tracker/items/WI-0003/artifacts/impl-report.md` — read **after** the criteria and after the commands had been run; cited as evidence nowhere.
  - `tracker/items/WI-0003/history.md` and `journal.md` — how the item reached `verifying`.
  - `tracker/items/WI-0002/item.md` — the fourteen criteria the item's `## Out of scope` claims still read true.
  - `tracker/project.yaml` — the test and lint commands.
  - `recall/cli.py`, `recall/store.py` and `git diff main...HEAD` at commit `1ebf08efef963568d2f61eb1e8b1b1806958ea55`, the branch head this verification is against.
  - `docs/architecture/overview.md` — to check the documentation obligation `implement` declared and handed on.
- **Decisions:**
  - **All nine criteria pass, and the item goes to `in-review`.** Every verdict rests on a command this execution ran against the branch head, quoted with its real output in `verify-report.md`. No criterion was judged `ambiguous`; the record settled every reading that came up.
  - **AC9 passes, with the difference between its two halves recorded rather than smoothed over.** `delete` with no argument prints the subparser's own usage, `usage: recall delete [-h] front`. `delete alpha extra` prints the **top-level** usage, `usage: recall [-h] {add,review,delete} ...`, where `delete` appears inside the choice list and the error line names the surplus argument instead of the subcommand. The criterion asks for a usage message naming the `delete` subcommand; the token is present in both, so both satisfy it as written. The second is weaker than the first, and that is written into the report so a reader can judge it — but tightening it would be a change to AC9, which is not this skill's to make, and it is not a defect in the code.
  - **AC2's `rung:  3 of 4` rendering is a pass, not a deviation.** The criterion asks for the rung and the due date *"as that card's record holds it in the card file"*. The due date is printed as the stored `YYYY-MM-DD` verbatim; the rung prints the stored integer inside `N of 4`, adding the ladder's height without transforming the value. The sentence guards against a converted display — `due` as *"in three days"*, `rung` as a name — and this is not one.
  - **The interleaved-match case was constructed deliberately**, because it is the one place a wrong answer would destroy a card the person never saw. A file seeded `dup`/`other`/`dup`/`dup`, answered `2`, removed the second `dup` and left `other` untouched — so the number is an index into the matches and the removal an index into the file. `plan.md` names this as the design's one real hazard and it is closed.
  - **No bug item, and no send-back.** Nothing failed against this item's own criteria, and nothing was found that belongs to `WI-0001` or `WI-0002`'s delivered behaviour.
  - **`docs/architecture/overview.md`'s two false sentences are recorded as a `review-close` obligation, not repaired here.** Lines 12 and 35–36 say `delete` is not yet started; they become false in the trunk at the merge. `implement` declared this and correctly left it, and `spec/doc-header.md` §5 restricts this skill the same way. Repairing it inside verification would also mean the verifier checking its own edit.
  - **The `a-criterion-about-criteria-is-read` gate is not applicable, and the underlying read was done anyway.** None of AC1–AC9 has other criteria as its subject; the citations to `WI-0001` AC2/AC6/AC7 and `WI-0002` AC13/AC14 are provenance for a decision, not a subject. The item's `## Out of scope` does make a claim of that shape in prose, so it was read out per-criterion in `verify-report.md` rather than assumed, and the non-intersection question was answered explicitly: things executable **do** exercise WI-0002's criteria together with the new behaviour, so nothing had to be added or waived.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0 (`Ran 90 tests` / `OK`), on the branch head before any local change
  - `python3 -m compileall -q recall tests` → 0 (no output)
  - `.claude/agile-skills/scripts/validate-workspace .` → 0 (`checked 4 item(s), 11 document(s)`, `0 errors, 0 warnings`)
  - `git rev-parse HEAD` → 0 (`1ebf08efef963568d2f61eb1e8b1b1806958ea55`)
  - `git diff main...HEAD --name-status` and `git diff main...HEAD -- recall/cli.py` → 0 (three code/test/tracker groups; `review`, `add`, `_ask`, `_stopped`, `_side_error` unchanged byte for byte)
  - AC1: `printf 'y\n' | RECALL_CARD_FILE=… python3 -m recall delete "capital of France"` → 0 (`Deleted: capital of France`; only the other card left in the file)
  - AC2: `printf 'n\n' | … delete "capital of France"` → 0 (`Nothing was deleted.`; `cmp` IDENTICAL) and the same against a rung-0 card → 0 (`rung:  0 of 4 (never answered)`)
  - AC3: `printf 'q\n' | … review` on a pre-deletion copy → 0 (`3 cards due.`); `printf 'y\n' | … delete "beta"` → 0; `printf '\ny\n\ny\n' | … review` → 0 (`2 cards due.`, offering `alpha` and `gamma`, `beta` nowhere in the output)
  - AC4: `… delete "only card"` with `y` → 0; `grep -c '^front:'` → 1 (zero matches); `… review` → 0 (`Nothing is due.`); `… add "new front" "new back"` → 0 (`Added: new front`)
  - AC5: `… delete` against a populated file, a card-less file and a missing file → 1, 1, 1 (`No card has the front '…'.` on stderr; `md5sum -c` OK; the missing file still missing; `grep -c "About to delete"` → 0 in all three)
  - AC6: `printf '2\n' | … delete "dup"` over `dup`/`other`/`dup`/`dup` → 0 (three matches listed and numbered, exactly the second removed, `other` intact); `printf 'n\n' | … delete "dup"` → 0 (`cmp` BYTES_IDENTICAL)
  - AC7: `printf 'maybe\nn\n' | …` → 0 (card block printed twice, `This prompt takes: y, n.`, bytes identical); `printf 'maybe\ny\n' | …` → 0 (still deleted, so not counted as a no); `printf '0\n9\nyes\nn\n' | …` → 0 (four listings for three refusals, bytes identical); `… delete … < /dev/null` at both prompts → 0, 0 (`Nothing was deleted.`, bytes identical)
  - AC8: `… delete "alpha"` against a file with `rung: not-a-number` on line 11 → 1 (`line 11: 'rung: not-a-number' is not a whole number`; no prompt; bytes identical); against a mislabelled `bak:` line → 1 (`line 5: expected a line starting 'back: '`)
  - AC9: `… delete` → 2 (`usage: recall delete [-h] front`); `… delete alpha extra` → 2 (`usage: recall [-h] {add,review,delete} ...`); `… delete ""` → 1; `… delete "   "` → 1; `… add "" B` and `… add "   " B` → 1, 1 (`The front side is empty.`), all six leaving the file byte-identical
  - nine mutations of `recall/cli.py`, each applied alone, the full suite run, then restored from a copy — M1 save removed → `failures=9`; M2 confirmation not asked → 8; M3 no-match exits zero → 9; M4 the choice always picks the first → 2; M5 a closed stream deletes → 2; M6 the re-ask stops reprinting → 3; M7 an unparsable file exits zero → 3; M8 the `front` argument becomes optional → 1; M9 the prompt drops rung and due → 3
  - `cmp` of the restored `recall/cli.py` against the pre-mutation copy → 0, and `python3 -m unittest discover -s tests -t . -q` re-run afterwards → 0 (`Ran 90 tests` / `OK`), so nothing was left mutated
- **Gates:**
  - `tests-pass` → **pass** (`Ran 90 tests` / `OK`, exit 0, on `1ebf08e` and again after the last mutation was reverted)
  - `lint-clean` → **pass** (`python3 -m compileall -q recall tests`, exit 0, no output)
  - `workspace-valid` → **pass** (`0 errors, 0 warnings` over 4 items and 11 documents)
  - `every-criterion-independently-checked` → **pass** (each of AC1–AC9 has a command this skill ran and that command's real output quoted in `verify-report.md`; the implementation report is cited as evidence nowhere, and was read only after the commands had been run)
  - `negative-cases-exercised` → **pass** (thirteen conditions triggered rather than read about — three no-match cases including a missing file, four unrecognised inputs including the `0` and `9` boundaries of the numbered prompt, two closed streams, two unparsable files, the two wrong argument counts, and the empty and whitespace-only arguments — plus two beyond the criteria: the interleaved non-match and deleting the last card in the file)
  - `a-criterion-about-criteria-is-read` → **skipped, not applicable** (no criterion of WI-0003 has other criteria as its subject; the prose claim in `## Out of scope` about WI-0002's fourteen criteria was nonetheless read out per-criterion, with the non-intersection question answered in the negative — `tests/test_review.py`, `NeverOfferedAgainTests`, `OtherSubcommandsTests` and this execution's own AC3 runs all exercise the old criteria together with the new behaviour)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (nine mutations, every one red, at least one per criterion: AC1/AC3/AC4 by M1, AC2 by M2 and M9, AC5 by M3, AC6 by M4, AC7 by M5 and M6, AC8 by M7, AC9 by M8)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` — created; the verdict, the nine criteria with their commands and output, the gates, the boundary cases, the mutation table, the WI-0002 read, the documentation obligation, and five declared gaps
  - `tracker/items/WI-0003/item.md` — AC1 to AC9 ticked, all nine, each against a command in the report
  - no bug item filed, and no question filed
  - the commit of these files, subject `tracker: the verification of delete, nine criteria and nine mutations (refs WI-0003)`
- **Status:** `verifying` → `in-review`
- **Result:** `delete` does what WI-0003 asked for. All nine acceptance criteria pass against commands run on `1ebf08e` — including the case the plan called the design's one real hazard, where a non-matching card sits between the matches and answering `2` still removes the second match and nothing else. Nine mutations, one per criterion at least, each turned the suite red, so no criterion is covered only by a test that would pass against an absent implementation. Nothing was sent back and no bug was filed. One thing is handed to `review-close`: `docs/architecture/overview.md` v4 still says `delete` is not yet started, which the merge makes false, and the spec forbids both `implement` and this skill from repairing it.

## 2026-08-30T13:26:28Z — review-close v0.6.0 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review` — `verify` passed all nine criteria and moved the item here; `next` dispatched this skill as the owner of that status, with no request open and no question open anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (eight rows, chaining without a gap), `journal.md` (read in full — eight entries, one per execution the history implies), `questions/Q-001.md` and `questions/Q-002.md`.
  - `tracker/items/WI-0003/artifacts/plan.md`, `impl-report.md` including `## What I did not do`, and `verify-report.md` including `## Not verified, and why`.
  - **The diff itself**, `git diff main...wi/WI-0003` (`3e9c1df..677aac3`), hunk by hunk — four code hunks in `recall/cli.py`, `tests/test_delete.py` read in full, and the tracker files. Not the reports about it.
  - `recall/store.py` and `recall/cli.py` in full, which is where finding 1 came from.
  - `docs/architecture/adr/ADR-0005-…` clause by clause, `docs/architecture/overview.md` v4, `docs/product/vision.md` v6.
  - `tracker/project.yaml` for the gate commands.
- **Decisions:**
  - **Accepted and closed, `outcome: delivered`.** Every hunk maps to a plan step and a criterion; there is no unrequested scope; `review()`, `_stopped()`, `_ask()`, `add()` and `_side_error()` are byte-identical to `main` and `recall/schedule.py` and `recall/store.py` are not in the diff at all.
  - **Finding 1 — `recall/store.py` never appended and never removed — repaired, not sent back.** `overview.md` had said since v1 that the store *"reads it into cards, appends or removes, and writes it back atomically"*, citing `recall/store.py`. Opening the module shows `card_file_path`, `load` and `save` and no third public operation: `cards.append(...)` is in `cli.add` and `del cards[chosen]` in `cli.delete`. The sentence puts a seam one module to the left of where it is, which is exactly what would send the next skill looking in the wrong place. It is not a send-back because `spec/doc-header.md` §5 forbids `implement` and `verify` to write to `docs/` and no criterion of this item is about the overview; D7 makes it mine. `overview.md` → v5.
  - **Finding 2 — `ADR-0005` described a dependency the item no longer lacked — repaired in place, not superseded.** Its `## Consequences` said *"The item declares no `depends-on` and passes Definition of Ready R7 in form"*; the second `refine` execution added `depends-on: WI-0001` and nothing went back to the ADR. Recorded as an `erratum` through the append-only `## Corrections` section per `spec/doc-header.md` §4b, with the removed clause quoted verbatim and the replacement citing the item and its history. Nothing in `## Decision` moves and no reader would have to change any code to satisfy the new sentence, which is §4b's line between a correction and a supersession. `ADR-0005` → v2.
  - **The two false sentences `implement` declared and left were the right ones to hand over, and there was a third it could not have known about.** `overview.md`'s *"`delete` not yet started"* and *"named here so a reader can see where it will attach"* were declared by `implement` as a D7/D12 obligation and correctly not fixed. Reading the document against the code for D12 found the store sentence as well, which no declaration named and no gate could have caught.
  - **AC9's two halves name `delete` differently, and that is not a defect.** No argument gives the subparser's own usage; two arguments give the top-level usage with `delete` inside `{add,review,delete}`. Both contain the token the criterion asks for. `verify` recorded the difference rather than smoothing it; tightening it would be a change to AC9, which is not this skill's to make. Recorded in `review.md` finding 3 so it is not rediscovered as news.
  - **`main()`'s unreachable `AssertionError` is kept.** It serves no criterion, but plan step 6 accounts for it and it exists so a fourth subparser added without a handler fails loudly instead of falling through — the trap `WI-0001`'s review recorded. Being unreachable it is untested, which is the correct state for a guard of that kind.
  - **Six declared gaps accepted, and all six written into the item's `## Notes`** rather than left inside `verify-report.md`: the default card-file location never exercised by `delete`, the concurrent-writer gap, no unicode-normalisation case, no `Ctrl-D` at a real terminal, no wrapping of a long side, and AC4's restart being separate subprocess invocations. An accepted gap that lives only in a report is invisible the moment the item closes.
  - **No bug item filed.** Nothing was found that `WI-0001` or `WI-0002` delivered and got wrong.
  - **The epic is not ended by this execution.** `scripts/engagement-state EP-001` reports `at-rest` now that this item is `done`; ending the engagement is its own dispatch on EP-001 and its own action, and this run had already taken one.
- **Questions raised:** none — nothing in the change contradicted a recorded decision, and the two documentation defects had a repair route in the spec (D7, and `doc-header.md` §4b) rather than needing the architect's ruling.
- **Cross-answer check:** none consumed by this execution — it consumed no human answer, because `review-close` on a work item asks nobody. The two human answers on this item (`WI-0003/Q-001`, `WI-0003/Q-002`) were consumed by `answer-questions` on 2026-08-30, and `lint-answers --context work-item --changed-since main` was run here as the hard gate over all nine consumed answers in the workspace: `0 errors, 0 warnings`. The one place two of the stakeholder's answers meet — *"I don't need a numbered list for this"* (`Q-001`) against AC6's numbered several-match prompt — was checked again by hand against `ADR-0005`'s `## Decision`, which states the scope of their sentence: the numbers exist only inside that prompt and are not an identifier they can use anywhere else, so the two are compatible and no document of theirs was harmonised.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (`checked 4 item(s), 11 document(s)`, `0 errors, 0 warnings`), run before the doc repairs, once during them (2 errors: the change-log row I appended was newest-last — fixed) and after
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → 0 (`verified at 1ebf08ef; wi/WI-0003 has moved to 677aac33 but only the record changed (7 file(s) under tracker/ or docs/), so the verification still covers the code`)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → 0 (`all 4 commit(s) on main..wi/WI-0003 name WI-0003`)
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0, **run twice**: before the repairs `0 document(s) in 0 path(s) differ from main (3e9c1df) under docs`, after them `2 document(s) in 2 path(s) differ from main (3e9c1df) under docs`
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0 (`claim window: 2 path(s) differ from main`; `checked 9 consumed human answer(s) in the workspace`)
  - `git diff main...HEAD --name-status` and `git diff main...HEAD -- recall/cli.py` → 0
  - `git rev-parse main` → 0 (`3e9c1dfb012c27a292cd033ab8b9192c708c39d9`), taken **before** the trial merge
  - `git worktree add --detach .trial main` → 0 (`Preparing worktree (detached HEAD 3e9c1df)`)
  - `git -C .trial merge --no-ff wi/WI-0003` → 0; `git -C .trial rev-parse HEAD` → 0 (`24c503bf236f6303fcbaa5ff55d5b60157d74b6c`)
  - `python3 -m unittest discover -s tests -t . -q` **inside `.trial`** → 0 (`Ran 90 tests in 4.564s` / `OK`)
  - `python3 -m compileall -q .trial/recall .trial/tests` → 0
  - `git worktree remove --force .trial` → 0; `git rev-parse main` → 0, **the same sha as before the trial** — the trunk did not move
  - `git commit` of the two repaired documents → 0 (`677aac3 docs: delete is built, and the store never appended or removed (refs WI-0003)`)
  - `git merge --no-ff wi/WI-0003` into `main`, and `python3 -m unittest discover -s tests -t . -q` on the merged trunk — run after this entry was written, in the order step 8 requires
- **Gates:**
  - `definition-of-done` → **pass** (D1 to D12 each with its own result and evidence, in `review.md` `## Definition of Done`. D7 and D12 passed only after two repairs; D3 was checked on the merge result, not on the branch)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the last change to `recall/` or `tests/` is `fe70136`, which predates the verification at `1ebf08e`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 4 commits; run **before** the merge, because `main..branch` is empty afterwards)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 90 tests` / `OK` inside the detached trial worktree at `24c503b`, which is the merge result and not the branch)
  - `workspace-valid` → **pass** (`0 errors, 0 warnings` over 4 items and 11 documents)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log --grep WI-0003` alone. *What was built and why*: `plan.md` and `ADR-0005`, from the stakeholder's own two sentences. *Which skill decided what*: eight journal entries, each stamped with its skill, version and persona, and a decisions table in the plan naming what was documented, what was assumed and what was asked. *What questions arose and how they were resolved*: `Q-001` and `Q-002`, both answered by the human, both with `## Consequences` naming files that exist. *What verification found*: `verify-report.md`'s nine criteria with their commands, nine mutations, and five declared gaps. `git log --grep WI-0003` returns nine commits spanning creation to close
  - `claims-are-sourced` → **pass**, and the **scope matters more than the verdict**. Quoted from the gate's own output: the first run reported *"checked absolute claims: 0 document(s) in 0 path(s) differ from main (3e9c1df) under docs"* — green over nothing, because a work item's branch changes no document by construction. After the D7/D12 repairs it reported *"2 document(s) in 2 path(s)"*, still `0 errors, 0 warnings`, which is a green over something. Both repairs came from a hand read; the gate proved my new citations resolve, and could not have found the sentences
  - `cross-answer-consistency` → **pass** (`lint-answers` exit 0 over all 9 consumed human answers; see `**Cross-answer check:**` for the one pair read by hand)
  - `epic-sign-off` → **not applicable to this execution** (this is a work item, not an epic; `check-epic-signoff` takes an epic ID). `scripts/engagement-state EP-001` was run afterwards and reports `at-rest`, which is `next`'s step 6 and a separate dispatch
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` — created: what was examined including an eleven-row D12 claims audit, D1 to D12 one by one, six findings, six accepted gaps, the verdict
  - `tracker/items/WI-0003/item.md` — `outcome: delivered`, and the six accepted gaps and the two documentation repairs written into `## Notes`
  - `docs/architecture/overview.md` — v4 → **v5**, three false sentences repaired, change-log row written
  - `docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md` — v1 → **v2**, one `erratum` in a new append-only `## Corrections` section, with a matching change-log row
  - commit `677aac3` (the two documents), the commit of this record, and the merge of `wi/WI-0003` into `main`
  - no bug item filed, and no question filed
- **Status:** `in-review` → `done`
- **Result:** `delete` is accepted and merged. The change is confined to `recall/cli.py` plus a new test file, every hunk maps to a plan step and a criterion, and nothing in `review`, the ladder or the stored format moved. What this review adds to what verification already found is two false sentences in `docs/`, both caught by opening what they cite rather than by a gate: `overview.md` said `delete` had not been started, and — since v1, through four versions and three items — that `recall/store.py` *"appends or removes"*, when the module offers `load` and `save` and both operations live in `cli.py`. That claim carried a resolving citation the whole time, which is the difference between a citation that resolves and a citation that supports. Both are repaired at this close, `ADR-0005`'s stale dependency clause with it. `engagement-state EP-001` now reports `at-rest`; ending the engagement is the next dispatch.
