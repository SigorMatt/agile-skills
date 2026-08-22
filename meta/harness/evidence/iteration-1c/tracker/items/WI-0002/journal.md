# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T21:10:30Z — intake v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was
  created by that execution
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/items/` — empty before this execution, so `WI-0002` is a fresh allocation
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/question.md`
  - `tracker/items/WI-0002/questions/Q-001.md` — filed by this execution
- **Decisions:** see EP-001's entry of the same timestamp for how the work was split. Specific to
  this item: AC2 requires that an expense with no named sharers records "everyone registered"
  *explicitly* rather than leaving it implied, because a stored expense that means "whoever
  existed at the time" cannot be recomputed after a person is added. AC4 and AC5 were added
  without the stakeholder asking for them — refusing an unknown person and a non-positive amount
  is the difference between a record that can be trusted and one that cannot. Nothing about how
  the data is stored appears in the item; that is `plan`'s decision. Dates were left out of the
  criteria and flagged in `## Notes` instead, because the stakeholder did not mention them and
  the CSV export in WI-0004 will force the question anyway.
- **Questions raised:** `Q-001` (blocking, to human) — whether shares are always equal or can be
  unequal. Unanswered. It is blocking because it decides what an expense record contains, and
  retrofitting a share field onto expenses already written to disk is not reversible cheaply.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0002 --type work-item …` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --actor intake
    --resume-to draft --reason "Q-001 blocking: …"` → exit 0
- **Gates:** the four gates in intake's contract were applied to this execution as a whole and
  are recorded, with their evidence, in EP-001's entry: `workspace-valid` → pass,
  `epic-has-success-measures` → pass, `items-are-separable` → pass, `no-solution-in-the-problem`
  → pass. For this item specifically, `items-are-separable` places it second, needing the people
  WI-0001 registers.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/questions/Q-001.md` (new)
  - `tracker/items/WI-0002/journal.md`, `history.md` (new)
- **Status:** `—` → `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Created at `draft` and immediately suspended on Q-001. `refine` cannot sharpen the
  criteria until the stakeholder says whether a share can be unequal.

## 2026-08-21T21:27:10Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`; the stakeholder answered Q-001 in the question file
  between turns, so this execution was run before `next`, which would otherwise have surfaced it
  as an open human-addressed question and stopped the loop.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` (with the stakeholder's `## Answer` filled in)
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0003/questions/Q-002.md` and
    `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md` (v1) —
    the division rule the equal-share answer hands off to
  - `docs/product/vision.md` (v2)
  - `tracker/items/EP-001/item.md` — the epic's scope boundary this answer moves
  - `tracker/items/WI-0002/artifacts/` — empty; no `plan.md` exists yet, so nothing to propagate into
- **Decisions:**
  - **Q-001 — shares are always equal (option A).** Route: recorded intent. The stakeholder took
    the recommendation and refused the per-person amount in as many words. No ADR: nothing was
    derived here, and an ADR would record the architect deciding what the stakeholder decided.
  - **AC1 says a per-person amount is not *accepted*, not merely not recorded.** Rationale: an
    option that is silently ignored is worse than one that does not exist, because the user
    believes they recorded an uneven split and the report quietly disagrees with them. This
    strengthens a criterion rather than loosening one, and it follows directly from "Don't need
    per-person amounts".
  - **The boundary was written onto the epic as well as the item.** Rationale: "no unequal
    shares" is a product-shape decision, and a reader of EP-001 who never opens WI-0002 would
    otherwise assume the restaurant case is covered. Recorded on `EP-001/item.md` and on the
    epic's journal, per this skill's instruction to journal scope-shaped answers on the epic.
  - **"for now" was recorded as a boundary, not designed around.** Rationale: the temptation is
    to have `plan` build a share-shaped record "in case", which would put an unused concept into
    the stored data — the one place ADR-0001 says is expensive to change. The note says what
    adding unequal shares later would cost instead.
  - **The rounding half of the division was left to ADR-0001.** Rationale: WI-0002 stores the
    amount, WI-0003 divides it. Cross-referenced from `## Notes` so either half is findable from
    the other.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (before the transition) → exit 1,
    2 errors: `board.stale` (the board had not been regenerated since EP-001's `updated` was
    bumped; `transition` regenerates it) and `question.awaiting.none-open` on WI-0002 — the
    protocol-required interval between
    answering the last blocking question and resuming the item; see the same note on WI-0003's
    journal entry of 2026-08-21T21:23:00Z.
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to draft --actor answer-questions --reason "Q-001 answered and propagated: shares are always equal (item.md AC1, out-of-scope, EP-001 scope)"` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after the transition) → exit 0, 0 errors, 1 pre-existing warning (`project.commands.test-null`, owned by `plan`)
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `## Consequences` was reopened after
    writing: `tracker/items/WI-0002/item.md` carries the amended AC1, the new out-of-scope bullet
    and the rewritten notes; `tracker/items/EP-001/item.md` carries the unequal-shares bullet
    under `## Out of scope`; `docs/product/vision.md` is at v3 with "Not a way to split a bill
    unevenly" and this question moved out of the open list.
  - `answered-from-the-record` → **pass**. The answer cites the stakeholder's own words in
    Q-001's `## Answer`; the division rule it defers to cites ADR-0001 v1.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human by this
    execution.
  - `workspace-valid` → **pass**, checked after the transition (exit 0).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:12:35Z, `draft` →
    `awaiting-answer`, actor `intake`) records `resume-to: draft`; this execution transitioned to
    `draft`.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/WI-0002/item.md` — AC1 amended; out-of-scope and notes extended
  - `tracker/items/EP-001/item.md` — `## Out of scope` extended; `updated` bumped
  - `tracker/items/EP-001/journal.md` — entry recording the epic-level scope consequence
  - `docs/product/vision.md` — v2 to v3
- **Status:** `awaiting-answer` → `draft`
- **Result:** Shares are equal, and an expense stores no per-person amount. WI-0002 returns to
  `draft` for `refine`, which still has to settle name matching, whether an expense carries a
  date, and the exact command wording the criteria call "documented".

## 2026-08-21T21:38:10Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** not dispatched by `next` — `next` dispatched `refine` on WI-0001 this run. This
  entry records a question filed as part of that execution's batch, under the standing rule for
  this project that when the pipeline is about to stop on a human-addressed question, every
  question already known to be needed is filed in the same round trip. Filing a question is not
  advancing an item, so no work was dispatched here: `item.md` is untouched and no criterion was
  rewritten.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`, `questions/Q-001.md`
  - `tracker/items/WI-0004/item.md` — AC1 and AC6, because the bank rows this item's expenses
    will be created from all carry a date
  - `tracker/items/WI-0003/item.md` — to confirm the report does not depend on the answer
  - `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md` (v1)
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **One question filed: Q-002, whether an expense carries a date.** Intake named this gap in
    `## Notes` and left it for refinement; it is a real Definition of Ready failure under R10,
    because nothing in the item states whether a date exists, which makes the field neither
    required nor excluded.
  - **Asked now rather than when WI-0002 is dispatched.** Rationale: the loop is stopping on
    WI-0001's questions regardless, and this one is already fully stated — its context is
    intake's note, and it needs nothing this execution has not read. Holding it back would spend
    a second round trip on a letter already written.
  - **The question was framed as a storage question, not a reporting one.** Rationale: WI-0003
    nets everything ever recorded and date filtering is out of scope there, so a date changes no
    number the report prints. Saying so in the question stops the stakeholder from weighing a
    consequence that does not exist.
  - **Nothing else on this item was asked.** The remaining looseness — the exact command wording
    in AC1 to AC5 — is the same "documented command" gap as WI-0001, and WI-0001/Q-001 asks it
    once for the whole tool. Asking again per item would waste the stakeholder's attention on a
    question already in front of them.
- **Questions raised:** `Q-002` (blocking, to `human`). No `artifacts/refinement-qa.md`: no
  exchange has taken place, and this item has not been refined.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --actor refine --resume-to draft --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after all four suspensions) → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 once every item carrying a new
    blocking question had been suspended; between filing and suspending it reports
    `question.blocking.not-suspended`, which is the expected transient).
  - `definition-of-ready` → **not evaluated in full**. This execution did not attempt to make
    WI-0002 Ready, so recording a per-criterion verdict would claim a check that was not
    performed. The one criterion that was assessed is **R10 fail** — the presence or absence of a
    date on an expense is stated nowhere, neither as behaviour, nor as out of scope, nor as
    deliberately unconstrained. That failure is what Q-002 exists to clear.
  - `criteria-are-decidable` → **not evaluated**. Same reason: no criterion was rewritten.
  - `qa-recorded-verbatim` → **skipped**. There is no exchange to record; the stakeholder is not
    in this session.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-002.md` (new)
  - `tracker/items/WI-0002/item.md` — **unchanged**, deliberately
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** One blocking question filed on whether an expense carries a date. The item is
  suspended and returns to `draft` for a full refinement once the stakeholder answers.

## 2026-08-21T21:45:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`; the stakeholder filled in Q-002's `## Answer` between
  turns, so this execution was run ahead of `next`, which would otherwise have stopped on the open
  human-addressed question without consuming it.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-002.md` (answered by the stakeholder), `Q-001.md`
    (answered earlier: shares are always equal)
  - `tracker/items/WI-0002/item.md`, `history.md` (`resume-to: draft`), `journal.md`
  - `tracker/items/WI-0004/item.md` (AC1, AC2, AC6 and `## Notes` — the import is where a date
    would otherwise be thrown away), `tracker/items/WI-0004/questions/Q-002.md` (the CSV sample is
    still outstanding)
  - `tracker/items/WI-0003/item.md` (`## Out of scope`: no filtering by date), `tracker/items/EP-001/item.md`
  - `docs/product/vision.md` (v6), `docs/architecture/adr/ADR-0001` (v1), `ADR-0002`, `ADR-0005`
    (both v1, written earlier this turn for WI-0001)
  - `tracker/items/WI-0002/artifacts/plan.md` — **does not exist**; the item has never been
    planned, so there was no plan to propagate into
- **Decisions:**
  - **Q-002 answered by the stakeholder, option B, verbatim.** "Yeah, give expenses a date. If I
    don't type one, just use today's date." Route: recorded intent; `answered-by: human`, because
    the decision is theirs. No ADR was written for the choice itself — an ADR records an
    architect's decision, and recording the stakeholder's own words as one would misattribute it.
  - **The default is the current date on the machine running the command.** The alternative
    readings — the date the file was created, the date of the last expense — are not what "today"
    means to someone typing the command, and AC6 states it so that `verify` need not guess.
  - **A bad `--date` is a refusal, not a silent fallback to today.** ADR-0005 clause 2 already
    fixes the shape (stderr, exit 1, nothing recorded); this decision is that an unparseable date
    is a refusal at all. Substituting today would store a date the user never intended and would
    never see, which is the same class of failure as WI-0001's duplicate-name case.
  - **The date propagates to WI-0004 now, not when WI-0004 is refined.** WI-0004 AC2 was amended
    to require the row's own date rather than the import's date. This is the reason the question
    was worth asking before the import was built, and leaving it in WI-0002's notes only would
    have meant WI-0004's criteria never learned it. Which CSV column carries the date is still
    unknown and is explicitly left to the outstanding sample.
  - **No query capability was added.** Nothing filters, sorts or searches by date, and the item's
    notes say so, so `plan` does not build an index for a requirement nobody has stated. WI-0003
    already excludes filtering the report by date.
  - **Criteria changed:** AC1 and AC3 amended, AC5 restated in ADR-0005's terms, **AC6 added** on
    WI-0002, and AC2 amended on WI-0004. Journalled here because this skill is one of only two
    permitted to change a criterion. Nothing was weakened: every change adds a requirement the
    stakeholder's answer created.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → run before and after; exit 0
    after the transition (mid-execution it reports `question.awaiting.none-open`, which is the
    expected window between answering the last blocking question and transitioning).
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to draft --actor answer-questions --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, each file reopened after writing. `tracker/items/WI-0002/item.md`
    AC1 lists the date, AC3 requires the listing to show it, AC6 states `--date` and the today
    default; `## Notes` no longer says the question is open. `tracker/items/WI-0004/item.md` AC2
    requires the row's own date. `tracker/items/EP-001/item.md` `## Scope` says "when it happened".
    `docs/product/vision.md` is at v7 with the change-log row.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own sentence, quoted in
    the question file; the consequences that go beyond it (the refusal on a bad date, the stream
    and exit code) follow from ADR-0005, which is cited.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:31:44Z, `refine`)
    records `resume-to: draft`; this execution transitioned WI-0002 to `draft`.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-002.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/WI-0002/item.md` — AC1, AC3, AC5 amended, AC6 added, `## Notes` rewritten
  - `tracker/items/WI-0004/item.md` — AC2 amended to require the row's date
  - `tracker/items/EP-001/item.md` — `## Scope` expense bullet amended
  - `docs/product/vision.md` — v6 to v7
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** Expenses carry a date: today by default, `--date` to override, the bank row's own
  date when imported. WI-0002 and WI-0004 both record it, and WI-0002 returns to `draft` for
  `refine`.

## 2026-08-21T22:10:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` — WI-0001 closed, making this the
  highest-ranked runnable item (rank 1, oldest `created`, lowest remaining ID)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (a fresh draft returned by `answer-questions`,
    not a send-back), `journal.md` (all four prior entries, for the stakeholder's verbatim answers)
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` — both answered by the stakeholder
  - `docs/architecture/adr/ADR-0001` (integer pence and the split rule), `ADR-0002` (the surface,
    including the `add-expense` and `list-expenses` names it reserves), `ADR-0003` (identity and
    ordering), `ADR-0004` (`--data-file`), `ADR-0005` (streams, exit codes, and its own example
    messages), `ADR-0006` (the envelope's missing-key rule)
  - `docs/architecture/overview.md` (v1), `docs/product/vision.md` (v9)
  - `tracker/items/WI-0001/item.md` and `artifacts/refinement-qa.md` — for the criterion style that
    passed and for the exact option spellings already in use; `tracker/items/WI-0003/item.md` and
    `WI-0004/item.md` — for scope overlap and for `--paid-by`/`--shared-by`, which WI-0004 AC6
    already commits to
  - The delivered code from WI-0001 (`expenses_tool/cli.py`, `store.py`) — to check that the
    options and messages this item specifies fit the surface that now exists rather than an
    imagined one
- **Decisions:**
  - **No question was filed, and this was the close call of the execution.** The gaps were the
    command's spelling, the amount grammar, the message strings, the listing order and the
    snapshot semantics — all of them the kind of thing the stakeholder delegated on WI-0001/Q-004,
    which `answer-questions` recorded as ADR-0002 and ADR-0005 and stated as binding on this item.
    Re-asking would have spent a whole turn of the loop on conventions already delegated. The
    Q&A record names that delegation explicitly rather than implying a fresh one.
  - **AC1 asserts that a per-person amount is a *usage error*, not merely absent.** WI-0002/Q-001's
    propagation says the command "neither records nor accepts" one. A flag that is silently ignored
    would leave the stakeholder believing they had recorded an uneven split, which is precisely the
    failure the answer was written to prevent.
  - **AC2 was turned into a snapshot criterion.** "Shows that explicitly rather than leaving it
    implied" was intake's wording and could be read two ways. The criterion now names the
    observable difference: register `Dan` after the fact and the expense still lists `Ana, Ben,
    Cass`. The alternative reading — resolving "everyone" at report time — would silently change
    who shared a past expense, and in an epic with no editing that is unrecoverable.
  - **`1.005` is refused rather than rounded.** Rounding at input would change what someone owes
    with no message; ADR-0001 deliberately puts rounding in the *split*, where WI-0003 AC6 checks
    it. This is the one place where refusing looks less friendly and is still right.
  - **A person named twice in `--shared-by` is refused.** Deduplicating quietly would repair a
    typed mistake without saying so — the same shape the stakeholder rejected for the import ("I
    don't want it silently doubling up").
  - **One rendering, defined once above the criteria and reused by AC1, AC2 and AC3.** Repeating
    the format in each criterion is how two formats end up in the code.
  - **Three criteria were added beyond the six that existed** — AC7 (description required and
    non-blank), AC8 (a duplicate or empty `--shared-by`), AC9 (every refusal leaves the history
    intact) — and AC9 is the one that matters most: it makes "records nothing" observable through
    the command line rather than through the data file's internals, which no criterion should
    depend on.
  - **`## Out of scope` gained two entries**: no filtering, searching or totalling in
    `list-expenses`, and nothing attached to an expense beyond the five fields AC1 names. Both are
    things a reader could reasonably assume were included — "list the expenses" invites "and the
    total", which is exactly WI-0003's job and would double-count if built here too.
  - **Two behaviours left unconstrained and named as such (R10):** `argparse`'s usage wording, and
    a description containing ` — ` or a comma. The second is a real ambiguity in the rendered line
    and it is left because nothing parses that output; saying so is the point of R10.
- **Questions raised:** none this execution. The two prior questions (`Q-001` from `intake`,
  `Q-002` from this skill's earlier execution) are answered and are recorded verbatim in
  `artifacts/refinement-qa.md`, along with seven `[assumed]` decisions and two `[unresolved]`
  entries carried into `## Notes`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to ready --actor refine --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, before and after the transition).
  - `definition-of-ready` → **pass**, criterion by criterion:
    **R1 pass** — frontmatter complete; `type`, `epic`, `priority: critical` all set.
    **R2 pass** — `## Story` names the role, the capability and the "so that".
    **R3 pass** — AC1 to AC9, each a labelled checkbox.
    **R4 pass** — was failing: AC1 and AC3 said "a documented command", and AC4's and AC5's
    messages were unnamed. Every criterion now names a command, its exact expected output, its
    stream and its exit code, with one rendering defined once and reused.
    **R5 pass** — `## Out of scope` names seven things, two added here.
    **R6 pass** — no open question on this item; `Q-001` and `Q-002` are both `answered`.
    **R7 pass** — no `depends-on` field. WI-0002 needs people to exist, and WI-0001 is `done`, so
    the ordering is satisfied in fact as well as in the epic's stated delivery order.
    **R8 pass** — was failing: no `artifacts/refinement-qa.md` existed. It now records both
    stakeholder answers verbatim, seven `[assumed]` decisions with the delegation each rests on,
    and two `[unresolved]` entries.
    **R9 pass** — recording an expense and listing expenses back is one coherent change against one
    data file; the report that consumes them is WI-0003 and is excluded here.
    **R10 pass** — the combinations are visible: `--shared-by` present (AC1), absent (AC2),
    duplicated and empty (AC8); unknown people in either role and a case-different sharer (AC4);
    four rejected amount forms and two accepted ones (AC5); `--date` present, absent and malformed
    (AC6); `--description` missing and blank (AC7); an empty listing and a two-expense listing
    (AC3); every refusal against the recorded history (AC9). Four combinations are named as
    deliberately unconstrained in `## Notes`, and two are recorded there as unable to arise.
  - `criteria-are-decidable` → **pass**. AC1: run the command, compare stdout to the rendered
    string, stderr to empty, `$?` to 0; then run it with `--share-amount` and compare `$?` to 2.
    AC2: record without `--shared-by`, compare the confirmation; `add-person Dan`; re-run
    `list-expenses` and compare the line. AC3: record two expenses with the given dates in separate
    invocations, compare the two lines and their order; then compare `list-expenses` against a
    fresh file to `No expenses recorded yet`. AC4: two invocations, compare stderr strings, `$?`,
    and `cmp` the data file; plus `--shared-by ana` succeeding. AC5: six invocations, four compared
    against the refusal string and two against the rendered amounts. AC6: compare the leading date
    to `date -u +%F`, then three malformed values against the refusal string. AC7: one usage error
    (`$?` = 2) and one refusal compared exactly. AC8: two refusals compared exactly, with `cmp`.
    AC9: capture `list-expenses` before and after each refusal and compare.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` carries both questions with the
    options they offered and the stakeholder's answers copied from the question files unaltered,
    then separates what was decided at refinement from what they said — including naming which
    delegation each assumption rests on, rather than implying the stakeholder chose it.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0002/item.md` — AC1 to AC6 rewritten, AC7 to AC9 added, the rendering defined
    once above the criteria, `## Out of scope` extended, `## Notes` extended with what refinement
    decided, on whose authority, and what it left unconstrained
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Nine criteria, each with a command and an exact expected output;
  one rendering of an expense shared by the confirmation and the listing; the snapshot semantics of
  "everyone registered" made observable; and four behaviours named as deliberately unconstrained
  rather than left to be discovered.

## 2026-08-21T22:12:30Z — plan v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC9, the rendering defined above them, `## Notes`
    including the four behaviours left unconstrained), `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — the seven `[assumed]` entries are this
    design's soft ground, and one of them turned out to be the problem
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` (both answered by the stakeholder)
  - `docs/architecture/adr/ADR-0001` to `ADR-0008`, `docs/architecture/overview.md` (v1),
    `docs/product/vision.md` (v9, "Who it is for")
  - **The code:** `expenses_tool/store.py` and `expenses_tool/cli.py` as delivered by WI-0001, and
    `tests/test_cli_people.py` for the shape the end-to-end tests take
  - `date`, `date +%F`, `date -u +%F` and `python3 -c "import time; time.tzname"` on this machine
- **Decisions:**
  - **Stopped and filed `Q-003` rather than designing past a defective criterion.** AC6 says the
    date with no `--date` is "the current date on the machine running it" and then, in the same
    sentence, that the rendered line begins with `date -u +%F`. On this machine those are different
    days right now (local `2026-08-22`, UTC `2026-08-21`; timezone IDT). Any implementation fails
    one half of the criterion.
  - **Why this is an escalation and not an assumption.** `plan`'s preference order allows a
    reversible assumption, but this is not a design choice with a criterion to check it against —
    it *is* the criterion, and only `refine` and `answer-questions` may amend one. Choosing the
    reading that suits the implementation is the specific failure the question protocol exists to
    prevent, and it would surface at `verify` as a failure nobody could attribute.
  - **Addressed to `architect`, not to the human.** The record settles the substance: the
    stakeholder said "just use today's date", and `docs/product/vision.md` says the tool is run by
    one person on their own laptop. `answer-questions` can resolve it from that and amend AC6's
    check clause; none of `spec/question.md` §4's four conditions applies, so the stakeholder's
    attention is not needed and the loop is not stopped.
  - **Nothing else was written.** No `plan.md`, no ADR, no `project.yaml` change. The rest of the
    design is unaffected by the answer, but writing half a plan against a criterion that is about
    to change would leave an artifact whose provenance nobody could reconstruct. The design work
    already done — the expense record shape, the money parsing, where the rendering lives — is
    stated in `Q-003`'s context only as far as it bears on the question, and will be recorded
    properly when this item resumes at `ready`.
- **Questions raised:** `Q-003` — blocking, addressed to `architect`. Two readings of AC6, with the
  consequence of each and a recommendation (option A: the local date, with AC6's check clause
  amended to `date +%F`).
- **Commands:**
  - `date` → `Sat Aug 22 01:11:38 AM IDT 2026`; `date +%F` → `2026-08-22`; `date -u +%F` →
    `2026-08-21`; `python3 -c "…"` → `('IST', 'IDT') 2026-08-22 2026-08-21`
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --actor plan --resume-to ready --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after this entry was
    written; it reported `journal.execution.missing` in the window between the transition and the
    journal, which is the expected ordering cost of transitioning before journalling
- **Gates:** none of `plan`'s four gates was reached, because the item was suspended before any
  design artifact was produced. Recorded individually rather than omitted:
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 with this entry in place).
  - `every-criterion-is-addressed` → **skipped**: no `plan.md` was written, and the criterion this
    execution stopped on is the one that would have to be addressed.
  - `project-commands-resolved` → **skipped**: `commands.test` and `commands.lint` were already
    filled in by the WI-0001 planning execution and needed no change.
  - `decisions-recorded` → **skipped**: no decision was recorded, because the one decision this
    execution reached was escalated rather than made.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-003.md` (new)
  - `tracker/items/WI-0002/artifacts/plan.md` — **deliberately not written**
- **Status:** `ready` → `awaiting-answer` (`resume-to: ready`)
- **Result:** WI-0002 is suspended on one question: whether an undated expense takes the machine's
  local date or its UTC date, and whether AC6's check clause is amended to match. The answer is
  available from the record, so `answer-questions` can resolve it without the stakeholder.

## 2026-08-21T22:15:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`, dispatched by `next` (orchestrator step 3: an open
  question addressed to `architect`)
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-003.md` (from `plan`, blocking), `Q-001.md` and `Q-002.md`
    (both answered earlier by the stakeholder — Q-002 is the one that settles this)
  - `tracker/items/WI-0002/item.md` (AC6 and the rendering above the criteria), `history.md`
    (`resume-to: ready` on the suspending row), `journal.md` (`plan`'s entry, for what it found)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md`; `artifacts/plan.md` — **does not exist**,
    deliberately: `plan` stopped before writing it, so there was no plan to propagate into
  - `docs/product/vision.md` (v9, "Who it is for"), `docs/architecture/adr/ADR-0001` (v1),
    `ADR-0005` (v1), `ADR-0006` (v1) — checked for a contradiction; none of them says anything
    about clocks or timezones
  - `tracker/items/WI-0004/item.md` (AC2 — an imported expense takes its row's date, which is a
    banking date rather than a UTC instant)
- **Decisions:**
  - **Q-003 answered as option A: the machine's local date, with AC6's check clause amended.**
    Route: **recorded intent**. The stakeholder's own sentence in Q-002 — "just use today's date" —
    plus the vision's "one person, on their own laptop" settles whose today it is. No ADR: nothing
    here was the architect's to decide, and writing one would dress a stakeholder's answer up as a
    design decision.
  - **An acceptance criterion was amended, and this is the record of it.** AC6's check clause said
    `date -u +%F` while the same sentence said "the current date on the machine running it". On a
    UTC machine those coincide, which is why the contradiction survived refinement; on a UTC+3
    machine at 01:11 they were different days. The amendment names the local date explicitly and
    names `date -u +%F` as what it is *not*, so the same mistake cannot be reintroduced by a reader
    who skims.
  - **The amendment moves the criterion toward what the stakeholder asked for, not toward what is
    convenient to build.** Nothing was built yet — `plan` stopped before writing `plan.md`, and no
    code for this item exists — so there is no implementation this could have been bent around.
    That is worth stating, because "amending a criterion to match what was built" is the specific
    failure this skill is warned about, and the timeline here rules it out.
  - **The implementation consequence was written into the answer** (`datetime.date.today()`, not
    `datetime.datetime.now(timezone.utc).date()`; no conversion applied to a user-supplied
    `--date`) so that `plan` resumes with the decision rather than re-deriving it.
  - **Not escalated to the stakeholder.** None of `spec/question.md` §4's four conditions applies:
    the intent is recorded, the choice is reversible in one call, it contradicts no ADR, and the
    record is not silent. Escalating would have stopped the loop to have them repeat themselves.
  - **`plan` filing this rather than assuming it was correct**, and is worth noting as a working
    example: the alternative — a reversible assumption in `plan.md` — would have produced code that
    failed AC6 at `verify`, and the failure would have looked like a defect in the code.
- **Questions raised:** none. Nothing was re-addressed to the human.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (mid-execution it reports
    `question.awaiting.none-open`, the expected window between answering the last blocking question
    and transitioning)
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to ready --actor answer-questions --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, both files reopened after writing.
    `tracker/items/WI-0002/item.md` AC6 now reads "read from that machine's own clock and timezone
    … the output of `date +%F` — the local date, not `date -u +%F`", and `## Notes` carries the
    bullet recording the amendment. `tracker/items/WI-0002/artifacts/refinement-qa.md` carries the
    new `[assumed]` entry attributing the original gloss to `refine`.
  - `answered-from-the-record` → **pass**. The answer cites WI-0002/Q-002 (the stakeholder's
    words), `docs/product/vision.md` v9 ("Who it is for"), and WI-0004 AC2 for why a banking date
    is a local date. No new ADR, and the answer says why one would have been wrong.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human; the reasoning
    for not escalating is recorded in the answer against all four of §4's conditions.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T22:12:xxZ, `plan`) records
    `resume-to: ready`, and this execution transitioned WI-0002 to `ready` — not to `draft`, even
    though a criterion changed, because the item had already passed the Definition of Ready and the
    amendment made one criterion *more* decidable rather than reopening refinement.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-003.md` — answered, `answered-by: answer-questions`,
    consequences listed
  - `tracker/items/WI-0002/item.md` — AC6 amended; `## Notes` extended
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — one `[assumed]` entry added
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `ready`
- **Result:** An undated expense takes the laptop's local date, and AC6 now says so in terms that
  are exact on any machine. WI-0002 returns to `ready` for `plan`, which stopped rather than
  guessing and can now design against a criterion that does not contradict itself.

## 2026-08-21T22:17:30Z — plan v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next`; this is the **second** `plan` execution on
  this item — the first suspended it on `Q-003` rather than designing past a criterion that
  contradicted itself, and `answer-questions` has since amended AC6 and returned it to `ready`.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC9 with AC6 as amended, the rendering defined above them,
    `## Out of scope`, `## Notes` including the four behaviours left unconstrained), `history.md`
    (the suspend-and-resume pair), `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (eight `[assumed]` entries, two
    `[unresolved]`), `questions/Q-001.md`, `Q-002.md`, `Q-003.md` (all answered)
  - `docs/architecture/adr/ADR-0001` to `ADR-0008` (all v1), `docs/architecture/overview.md` (v1),
    `docs/product/vision.md` (v9)
  - `tracker/items/WI-0003/item.md` (AC1, AC3, AC6 — what the report will need from these records)
    and `tracker/items/WI-0004/item.md` (AC2, AC6, AC7 — what the import will write)
  - **The code:** `expenses_tool/store.py`, `expenses_tool/cli.py`, `tests/test_store.py` and
    `tests/test_cli_people.py` as merged from WI-0001 — read for the shapes this item extends
    (`load`'s strict guards, `_refuse`, the parent-parser pattern for `--data-file`)
- **Decisions:**
  - **ADR-0009 written: expenses name people by their stored display name, and snapshot their
    sharers.** Route: decided. This is the only decision here that is expensive to reverse — it is
    the stored shape WI-0003 and WI-0004 both build on — which is exactly the test for whether
    something is an ADR or a plan step. IDs were rejected because people have none, renaming is out
    of scope for the epic, and `"paid_by": 3` would destroy the hand-repairability that ADR-0006
    chose JSON for. Storing the normalised name was rejected because it would break ADR-0006 clause
    3's rule that the normalised form is derived and never stored.
  - **The sharers are snapshotted, and that is half of ADR-0009.** AC2 requires it, and the lazy
    implementation — storing a marker meaning "everyone" — silently rewrites who shared a past
    expense the next time a friend is registered, in an epic with no undo.
  - **`render_expense` lives in `cli.py`, not in `expenses.py`.** ADR-0008 clause 3 puts every
    user-visible string in `cli.py`. The item defines one rendering for both the confirmation and
    the listing, so there is one function, one string and one place it can change.
  - **`money.py` is a new module but not a new decision.** ADR-0001 already fixes integer pence;
    this is where that rule is implemented. No ADR was written for it, deliberately — an ADR trail
    padded with non-decisions hides the real ones.
  - **The order of operations inside `add-expense` is specified in step 7**, because AC9 depends on
    it: every validation precedes the save, so "a refusal changes nothing" is a property of the
    control flow rather than something a test hopes for.
  - **Five assumptions recorded rather than escalated** (route: assumed, all reversible in one
    file with no stored data): splitting `--shared-by` on commas only, refusing a zero amount under
    AC5's message, the stored order of the sharer list, requiring the exact ten-character date
    layout, and updating the README without a criterion demanding it.
  - **`parse_date` is stricter than `date.fromisoformat`.** In Python 3.11+ the library accepts
    `20260814` and full timestamps; AC6 names the `YYYY-MM-DD` layout, so step 3 checks the layout
    as well as the value. Named in `## Risks` because it is the kind of permissiveness that passes
    every test and surprises a reader later.
  - **`docs/architecture/overview.md` bumped to v2 in this execution** rather than left to
    `implement`: two new modules and a new top-level key in the data file are a change to the shape
    of the system, which is the condition this skill's step 8 sets.
  - **`tracker/project.yaml` untouched.** Both commands were filled in for WI-0001, both still run,
    and the new tests are found by the same discovery command.
- **Questions raised:** none this execution. `Q-003`, filed by the previous `plan` execution, is
  answered and its consequence — the local-date default — is written into step 3 and cited there.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to planned --actor plan --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `every-criterion-is-addressed` → **pass**. `artifacts/plan.md` `## Acceptance criteria mapping`
    has one row per criterion, AC1 to AC9, each naming the steps that satisfy it and the specific
    test that demonstrates it — `AC1::test_records_and_confirms`,
    `AC1::test_share_amount_is_a_usage_error`, `AC2::test_defaults_to_everyone_and_snapshots`,
    `AC3::test_lists_in_date_order_across_invocations`, `AC3::test_empty_listing`,
    `AC4::test_unknown_person_refused`, `AC4::test_case_different_sharer_resolves`,
    `AC5::test_bad_amounts_refused`, `AC5::test_accepted_amounts_render`,
    `AC6::test_default_date_is_todays_local_date`, `AC6::test_bad_dates_refused`,
    `AC7::test_missing_description_is_a_usage_error`, `AC7::test_blank_description_refused`,
    `AC8::test_duplicate_sharer_refused`, `AC8::test_empty_shared_by_refused`,
    `AC9::test_refusals_do_not_change_the_listing` — with the exact comparison each makes. No row
    says "tests".
  - `project-commands-resolved` → **pass**. `commands.test` and `commands.lint` are set and both
    were run in this project during the WI-0001 planning and implementation executions;
    `commands.build` remains `null` with ADR-0007 clause 5 recording why.
  - `decisions-recorded` → **pass**. One ADR created (ADR-0009) with context, five options across
    two axes with their costs and risks, the decision, and consequences including a per-clause
    reversibility statement. Everything else this plan rests on is cited to an existing ADR or to
    the item's own answered questions in `## Decisions and ADRs`, so a reader can tell what was
    decided here from what was inherited.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — thirteen steps, nine mapped criteria, five
    assumptions, five named risks
  - `docs/architecture/adr/ADR-0009-expenses-reference-people-by-stored-name.md` (new)
  - `docs/architecture/overview.md` — v1 to v2
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0002 has a plan that decides everything a developer would otherwise guess at: the
  stored record shape (ADR-0009), the money grammar, where the one rendering lives, and the order
  of operations that makes "a refusal changes nothing" structural. The criterion that stopped the
  first attempt is settled, and nothing in the plan works around it.

## 2026-08-21T22:22:00Z — implement v0.1.1 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`; no branch existed, so this is a fresh
  implementation rather than a resumption.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC9 with AC6 as amended, the rendering above them,
    `## Notes`), `history.md` (the `plan` suspend-and-resume pair, so the amended AC6 was read as
    the current criterion), `artifacts/plan.md` (all thirteen steps and the mapping table),
    `artifacts/refinement-qa.md`
  - `questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all answered, and their consequences already in
    `item.md` and `plan.md`, so nothing was read out of a question file and acted on directly
  - `docs/architecture/adr/ADR-0001`, `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0008`, `ADR-0009`;
    `docs/architecture/overview.md` (v2)
  - **The code:** `expenses_tool/store.py`, `expenses_tool/cli.py`, `tests/test_store.py`,
    `tests/test_cli_people.py` as merged from WI-0001
- **Decisions:** all inside the plan's latitude.
  - **`resolve_sharers` drops empty parts before deciding the list is empty**, so `--shared-by ","`
    reports "must name at least one person" rather than an unknown person named `""`. The plan
    allowed either reading; this one produces the message a user can act on.
  - **`parse_date` checks the layout with three character comparisons**, then lets
    `date.fromisoformat` do the calendar validation. Less machinery than a regex for the same
    effect, and it keeps the reason the check exists visible in one place.
  - **`store.load`'s new guard returns a *reason* per failure mode** (`has no description`, `has an
    amount that is not a whole number of pence`), matching the specificity the WI-0001 guards
    already had. A file refused with a vague reason is a file the owner deletes.
  - **`_bad_expense` rejects a `float` `amount_pence`.** ADR-0001 clause 1 says no float ever holds
    an amount; without this, a hand-edited file would put fractional pence into WI-0003's
    arithmetic, and the failure would surface as a wrong balance rather than as a refusal.
  - **An existing WI-0001 unit test was updated**, and this is the decision most worth defending:
    `test_a_missing_file_is_an_empty_store` asserted the exact dict `empty_data()` returns, which
    this item extends with `"expenses": []`. No WI-0001 acceptance criterion mentions that shape,
    every WI-0001 end-to-end test still passes untouched, and two tests were *added* to pin the
    compatibility that matters — a WI-0001-era file with no `expenses` key still loads. Treating it
    as a defect in delivered behaviour and filing a bug would have been the wrong call: nothing
    delivered is wrong.
  - **A bug in my own test helper was fixed, not worked around.** It dropped a `None` value while
    keeping its option name, turning AC2's and AC6's "omit the option" cases into usage errors.
    Both tests failed loudly, which is what a test that maps to a criterion should do.
  - **Nothing was built for the later items.** `record_expense` is the path WI-0004's import will
    reuse, but no import key, no balance and no total exists.
- **Questions raised:** none. The decision that would have needed one — which clock dates an
  undated expense — was settled by `Q-003` before this execution began.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → run after each module: exit 1 once with
    `FAILED (failures=1)` (WI-0001's `empty_data` assertion, fixed as recorded above), once with
    `FAILED (failures=2)` (the test-helper bug, fixed), and finally exit 0 with `Ran 62 tests`, `OK`
    on the branch head
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002 --root . --trunk main`
    → `all 1 commit(s) on main..wi/WI-0002 name WI-0002`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to in-progress --actor implement --branch wi/WI-0002 --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to verifying --actor implement --reason "..."` → exit 0
- **Gates:** run on the branch head, after the last change.
  - `tests-pass` → **pass**. 62 tests, exit 0.
  - `lint-clean` → **pass**. `compileall`, exit 0; ADR-0007 clause 4 records that this is a syntax
    check rather than a style linter, so the gate is weaker than its name suggests.
  - `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
  - `every-criterion-has-a-test` → **pass**. One test class per criterion in
    `tests/test_cli_expenses.py`: `AC1` (two tests), `AC2`, `AC3` (two), `AC4` (two), `AC5` (two),
    `AC6` (two), `AC7` (two), `AC8` (two), `AC9`. Each compares exact strings and exit codes; AC4,
    AC8 and AC9 additionally compare the data file's bytes before and after, so none would pass
    against an implementation that printed the right words and stored the wrong thing.
  - `commits-reference-the-item` → **pass**, as above.
- **Artifacts:**
  - `expenses_tool/money.py`, `expenses_tool/expenses.py` (new)
  - `expenses_tool/store.py` — `_bad_expense` and the `expenses` guard added, `empty_data` extended
  - `expenses_tool/cli.py` — `render_expense`, `cmd_add_expense`, `cmd_list_expenses`, two subparsers
  - `tests/test_money.py`, `tests/test_expenses.py`, `tests/test_cli_expenses.py` (new);
    `tests/test_store.py` — one assertion updated, two tests added
  - `README.md` — "Recording expenses" section
  - `tracker/items/WI-0002/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0002/item.md` — `branch: wi/WI-0002` recorded
  - branch `wi/WI-0002`, commit range `main..wi/WI-0002` = `aa611b6` (one commit)
  - `tracker/board.md` — regenerated
- **Status:** `in-progress` → `verifying`
- **Result:** Expenses can be recorded and read back. The record shape is ADR-0009's, the sharers
  are snapshotted, every refusal happens before the write, and 62 tests pass on the branch head.
  Four deviations from the plan are declared in `impl-report.md`, including the one existing test
  this item legitimately changed and why that is not a defect.

## 2026-08-21T22:26:30Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next`
- **Verified commit:** `c59b1342471b8c9c6dc1edfe2013d6171d8f544b`, the head of `wi/WI-0002`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the nine criteria, **read first and in full**, with what
    would settle each written down before `impl-report.md` was opened; `history.md` (the `plan`
    suspend-and-resume, so the amended AC6 is the criterion in force); `artifacts/plan.md`;
    `artifacts/impl-report.md` (afterwards, and used to look for claims worth challenging);
    `artifacts/refinement-qa.md`; `questions/Q-003.md`
  - `docs/architecture/adr/ADR-0001`, `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0009`;
    `docs/architecture/overview.md` (v2); `tracker/project.yaml`
  - The code and the diff: `expenses_tool/money.py`, `expenses.py`, `store.py`, `cli.py`, the four
    test modules, `README.md`, `git diff --stat main..HEAD`, and
    `git diff main..HEAD -- tracker/items/WI-0002/item.md`
- **Decisions:**
  - **Every criterion was checked by running it**, not by running the test that claims it. The
    tests were run as the `tests-pass` gate; the evidence in the Criteria table is this skill's own
    shell commands and their quoted output.
  - **AC6 was the criterion worth the most attention**, because it is the one `plan` stopped the
    pipeline over. The check is not "a date appeared": it compares the rendered date against
    `date +%F` **and** records that `date -u +%F` was a different day at that moment
    (`2026-08-22` versus `2026-08-21`). On this machine, today, a UTC implementation would have
    been caught.
  - **AC2 was checked by the sequence that makes the snapshot observable** — record without
    `--shared-by`, register a fourth person, list again — rather than by inspecting the stored
    JSON. A criterion checked against the file's internals would pass against an implementation
    that stored the right thing and rendered the wrong one.
  - **`implement`'s change to a WI-0001 test was investigated rather than accepted.** The question
    is whether delivered behaviour was altered to make this item pass, which would be a bug item
    against WI-0001 and a send-back here. It was not: no WI-0001 criterion mentions the dict shape,
    WI-0001's end-to-end tests pass untouched, and I loaded a WI-0001-era file through the tool
    myself and got `No expenses recorded yet`, exit 0. Recorded in the report under Defects found,
    because "I looked and it was fine" is only useful if it is written down.
  - **A false negative in my own sensitivity check was recorded, not swept up.** My first edit for
    the amount case did not match the file, so the suite passed and the check proved nothing. That
    is precisely the failure mode step 5 exists to catch; the report says so and shows the second,
    real edit.
  - **Nothing was classified as a bug.** Nothing failed, and nothing was found in behaviour
    delivered by WI-0001.
  - **Six gaps were declared rather than tested around**, including two nobody has mentioned
    before: the listing at scale, and two `add-expense` processes racing on the same file. Neither
    has a criterion; both are real, and the second is the one a reader should know was considered.
- **Questions raised:** none.
- **Commands:** (all run by this skill, on the verified commit)
  - `git rev-parse HEAD` → `c59b134…`; `python3 -m unittest discover -s tests -t . -q` → exit 0,
    `Ran 62 tests`, `OK`; `python3 -m compileall -q expenses expenses_tool tests` → exit 0;
    `validate-workspace` → exit 0
  - AC1: `add-expense … --date 2026-08-14` → `exit=0`, `stdout=[Added 2026-08-14 30.00 dinner — paid
    by Ana, shared by Ana, Ben, Cass]`, `stderr=[]`; with `--share-amount 10.00` → `exit=2`
  - AC2: record with no `--shared-by` → `Added 2026-08-14 9.00 taxi — paid by Ana, shared by Ana,
    Ben, Cass`; `add-person Dan`; `list-expenses` → unchanged sharers
  - AC3: two records in separate shells → `2026-08-02 …` printed before `2026-08-14 …`, `exit=0`;
    empty file → `No expenses recorded yet`, `exit=0`
  - AC4: `--paid-by Dan` and `--shared-by Ana,Dan` → `exit=1`, `stderr=[Unknown person: Dan]`,
    `cmp` unchanged; `--paid-by ana --shared-by ana,BEN` → `exit=0` rendering `Ana, Ben`
  - AC5: `0`, `-5`, `abc`, `1.005` → four × `exit=1` with the exact message; `30` and `30.5` →
    `30.00` and `30.50` in the listing
  - AC6: no `--date` → `Added 2026-08-22 …` with `date +%F` = `2026-08-22`, `date -u +%F` =
    `2026-08-21`; `2026-13-01`, `14/08/2026`, `today` → three × `exit=1` with the exact message
  - AC7: omitted `--description` → `exit=2`; `"   "` → `exit=1`, `stderr=[An expense needs a
    description]`
  - AC8: `Ana,ana` → `exit=1`, `stderr=[Ana is named twice in --shared-by]`; `""` → `exit=1`,
    `stderr=[--shared-by must name at least one person]`; `cmp` unchanged
  - AC9: five refusals against a non-empty ledger → `exit=1 listing and bytes unchanged` each
  - Boundary: a WI-0001-era file → `No expenses recorded yet`, `exit=0`; a fractional
    `amount_pence` → `exit=1`, `Cannot read …: one of its expenses has an amount that is not a
    whole number of pence`
  - Sensitivity: four edits, each followed by the test command and `git checkout -- expenses_tool`
    → `FAILED (failures=1)`, `FAILED (failures=4)`, `FAILED (failures=2)`,
    `FAILED (failures=11, errors=6)`; `git status` clean afterwards and the suite back to `OK`
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to in-review --actor verify --reason "..."` → exit 0
- **Gates:**
  - `tests-pass` → **pass**. 62 tests, exit 0, on the verified commit.
  - `lint-clean` → **pass**, with the standing qualification: `compileall` is a syntax check
    (ADR-0007 clause 4).
  - `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
  - `every-criterion-independently-checked` → **pass**. AC1–AC9 each have a command this skill ran
    and its quoted output in `artifacts/verify-report.md`; the nine checkboxes were ticked only
    after that run.
  - `negative-cases-exercised` → **pass**. Six of the nine criteria are negative cases and were all
    triggered, plus a WI-0001-era file, a fractional `amount_pence`, `--share-amount`, and a
    case-different sharer.
  - **Test sensitivity** (step 5, not a named gate) → **pass**, after one false negative that is
    recorded in the report rather than hidden.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` (new), carrying `Verified-commit:`
  - `tracker/items/WI-0002/item.md` — all nine criteria ticked
  - bug items filed: none
  - `tracker/board.md` — regenerated
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 does what its criteria say, checked command by command against `c59b134`.
  AC6 in particular is now demonstrated on a machine where the local and UTC dates differ, which is
  the whole reason that criterion was amended. Six gaps a green verdict does not cover are declared,
  two of them new to this item.

## 2026-08-21T22:29:30Z — review-close v0.1.1 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (nine criteria, `## Out of scope`, `## Notes`), `history.md`
    (twelve rows, including two suspend-and-resume pairs), `journal.md` **in full** (ten entries),
    `questions/Q-001.md`, `Q-002.md`, `Q-003.md`
  - `artifacts/plan.md`, `artifacts/impl-report.md` (`## Deviations from the plan`, `## What I did
    not do`), `artifacts/verify-report.md` (`## Not verified, and why`), `artifacts/refinement-qa.md`
  - `docs/architecture/overview.md` (v2) re-read against the code for D12; `docs/architecture/adr/`
    ADR-0001, ADR-0003, ADR-0005 to ADR-0009; `docs/product/vision.md` (v9); `README.md`
  - **The diff:** `git diff main..HEAD` hunk by hunk over nine source, test and documentation files,
    plus `git diff main..HEAD -- tracker/items/WI-0002/item.md` to confirm `implement` touched no
    criterion
- **Decisions:**
  - **Accepted.** Every hunk maps to a plan step and a criterion; the table is in
    `artifacts/review.md` `## What I examined`. The only code the plan does not name is the two
    added `store` tests, which `impl-report.md` declares as a deviation.
  - **The changed WI-0001 test was checked a second time, independently of `verify`.** Both
    `implement` and `verify` say it is an extension rather than altered behaviour. I re-read
    WI-0001's criteria: none mentions the dict `empty_data` returns, and WI-0001's end-to-end tests
    are unmodified in this diff. Confirmed, not taken on trust — this is the one change in the diff
    that could have been a quiet weakening of a closed item.
  - **Three findings, all accepted and recorded**: the description is stripped before storing
    (nobody specified it; it matches how names are handled and the alternative looks like a bug);
    the six-way exception mapping in `cmd_add_expense` is long but is exactly where ADR-0008 clause
    3 wants the strings; and the order of operations in that function is load-bearing but enforced
    only by tests, which the sensitivity check confirms is enough to catch.
  - **Six gaps copied into the item**, including one new and worth naming: two `add-expense`
    processes racing on the same data file could lose a record. Nothing in the epic mentions
    concurrency and no criterion covers it, so it is accepted — but it is now on the item rather
    than only in a verification report nobody reads after closing.
  - **D12 was performed as a read, not a recollection.** The overview's module list, envelope
    example and snapshot claim were checked against the code, and its "a missing key reads as
    empty" claim was checked by loading a WI-0001-era file through the tool. `README.md`'s new
    section was compared line by line against real output, including the em dash.
  - **The order was trial-merge, discard, close, then merge**, for the reason the skill states:
    `commits-reference-the-item` inspects `main..wi/WI-0002`, which is empty once merged.
  - **The epic stays `open`.** WI-0003 and WI-0004 are both at `draft`, so DE1 fails and the epic
    Definition of Done was not applied. WI-0004 additionally cannot close until the stakeholder
    supplies the CSV sample, which `tracker/items/EP-001/item.md` `## Scope` already records.
- **Questions raised:** none. Nothing in the change contradicts an ADR.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002 --root .` →
    *"verified at c59b1342; wi/WI-0002 has moved to c662cab5 but only the record changed (5 file(s)
    under tracker/ or docs/), so the verification still covers the code"*
  - `git branch -f trial-wi0002 main; git checkout trial-wi0002; git merge --no-edit wi/WI-0002` →
    clean; on the merge result `python3 -m unittest discover -s tests -t . -q` → exit 0, `OK`, and
    `python3 -m compileall -q expenses expenses_tool tests` → exit 0; then
    `git checkout wi/WI-0002; git branch -D trial-wi0002`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002 --root . --trunk main`
    → *all 3 commit(s) on main..wi/WI-0002 name WI-0002*
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to done --actor review-close --outcome delivered --reason "..."` → exit 0
  - then `git checkout main; git merge --no-ff wi/WI-0002`
- **Gates:**
  - `definition-of-done` → **pass**, criterion by criterion, with the evidence table in
    `artifacts/review.md`: D1 nine ticks; D2 nine evidence rows with commands and output; D3 gates
    run on `aa611b6`, `c59b134` and the merge result; D4 three answered questions; D5 ten journal
    entries against ten history rows; D6 ADR-0009 cited from the plan, the overview and two
    docstrings; D7 overview v1→v2 and the README extended, with the vision needing no change; D8
    `check-commit-refs` clean; D9 merged after closing; D10 `check-verify-freshness` clean; D11 this
    review's `## What I examined`; D12 the overview and README re-read against the code.
  - `verification-postdates-the-code` → **pass**, quoted above.
  - `commits-reference-the-item` → **pass**, run while the branch was still unmerged.
  - `tests-pass-on-the-merge-result` → **pass**. 62 tests and `compileall`, both exit 0, on the
    throwaway merge — not on the branch head.
  - `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0002`:
    what was asked (`item.md`, `refinement-qa.md`, and the stakeholder's two answers), who decided
    what (ten journal entries; ADR-0009; Q-003 answered by `answer-questions` after `plan` filed
    it), what was built (`plan.md`, `impl-report.md` with four declared deviations), what
    verification found (`verify-report.md`, with commands, quoted output, four sensitivity checks
    and one recorded false negative), and what remains unchecked (six accepted gaps on the item).
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new)
  - `tracker/items/WI-0002/item.md` — `status: done`, `outcome: delivered`, `## Notes` gains
    "Accepted gaps at close"
  - merge commit on `main`: see `git log --grep WI-0002 --merges`
  - epic: **not** closed; EP-001 stays `open` with two children at `draft`
  - `tracker/board.md` — regenerated
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** WI-0002 is delivered and merged. Expenses can be recorded and read back, with the
  sharers snapshotted, money in whole pence, and every refusal leaving the ledger untouched. Three
  findings accepted and six gaps recorded on the item. EP-001 remains open on WI-0003 and WI-0004.
