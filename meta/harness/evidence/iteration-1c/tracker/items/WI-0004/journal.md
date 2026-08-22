# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T21:10:30Z — intake v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was
  created by that execution
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/items/` — empty before this execution, so `WI-0004` is a fresh allocation
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/question.md`
  - `tracker/items/WI-0004/questions/Q-001.md` — filed by this execution
- **Decisions:** see EP-001's entry of the same timestamp for how the work was split. Specific to
  this item: intake deliberately invented no CSV format. "My bank's CSV export" names a file only
  the stakeholder has seen, and a guessed column layout would produce an importer for a file that
  does not exist, with acceptance criteria and a test fixture built on the guess. AC4 (a bad row
  is reported and does not stop the rest) and AC5 (a wrong file is refused with an explanation,
  not a stack trace) were added without being asked for, because an importer that dies on row 40
  of 200 is worse than no importer. Whether re-importing the same file duplicates its expenses
  was explicitly left undecided and named in `## Out of scope` rather than assumed either way,
  so that `refine` can find it instead of discovering it late.
- **Questions raised:** `Q-001` (blocking, to human) — what the bank's CSV export actually
  contains, and how a bank row (which knows only that money left an account) becomes an expense
  with a payer and a set of sharers. Unanswered. Blocking on both counts: the format is a fact
  nobody else has, and the payer/sharer rule is not a reversible guess — the criteria, the
  fixture and the parser all follow from it.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0004 --type work-item …` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to awaiting-answer --actor intake
    --resume-to draft --reason "Q-001 blocking: …"` → exit 0
- **Gates:** the four gates in intake's contract were applied to this execution as a whole and
  are recorded, with their evidence, in EP-001's entry: `workspace-valid` → pass,
  `epic-has-success-measures` → pass, `items-are-separable` → pass, `no-solution-in-the-problem`
  → pass. For this item specifically, `no-solution-in-the-problem` removed a reference to
  `csv.DictReader` from an earlier draft of the story, and `items-are-separable` places it
  fourth — while noting that its position is the one genuinely free choice in the epic, which is
  what EP-001/Q-001 asks about.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new)
  - `tracker/items/WI-0004/questions/Q-001.md` (new)
  - `tracker/items/WI-0004/journal.md`, `history.md` (new)
- **Status:** `—` → `draft` → `awaiting-answer` (resume-to `draft`)
- **Result:** Created at `draft` and immediately suspended on Q-001. Nothing further can be
  written about this item until the stakeholder supplies a sample of the export.

## 2026-08-21T21:31:40Z — answer-questions v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer`; the stakeholder answered Q-001 in the question file
  between turns, so this execution was run before `next`, which would otherwise have surfaced it
  as an open human-addressed question and stopped the loop.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` (with the stakeholder's `## Answer` filled in)
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/item.md` — AC2, for what "same idea as adding one by hand" means for
    an import that names no sharers
  - `tracker/items/EP-001/questions/Q-001.md` — the delivery order, because it decides how long
    the missing format can wait
  - `docs/product/vision.md` (v3), `docs/architecture/adr/ADR-0001-...` (v1)
  - `tracker/items/WI-0004/artifacts/` — empty; no `plan.md` exists yet
  - `.claude/agile-skills/spec/question.md` §4, `spec/dor-dod.md`
- **Decisions:**
  - **Half the question is answered and half is not, and the file is closed anyway.** Route for
    the answered half: recorded intent — the stakeholder chose option B in their own words. Route
    for the unanswered half: neither answered nor escalated now; recorded as an outstanding fact
    and handed to `refine`. The reasoning is written out in the question's `## Answer` so that a
    reader who only opens the question file gets it too.
  - **The default when no sharers are named is "everyone currently registered".** Rationale: the
    stakeholder said "same idea as adding one by hand", and WI-0002 AC2 defines what adding one
    by hand does with unnamed sharers. Deriving it from an existing criterion rather than
    inventing it is the difference between propagating an answer and designing one.
  - **Unknown people are refused before any row is imported, not per row.** Rationale: WI-0004
    AC4 deliberately lets a bad *row* be skipped without stopping the import, but a bad
    `--paid-by` is not a property of a row — it is wrong for the whole file, and discovering it
    after half the rows are in would leave a partial import the epic offers no way to undo
    (deleting expenses is out of scope). Stated in AC6 so `implement` cannot reasonably read it
    the other way.
  - **The format was not invented, and no importer may be designed against a guess.** Rationale:
    AC5 requires refusing a file that is not in the expected format; if the expected format is an
    invention, AC5 checks the invention against itself and passes while telling nobody anything.
    Written into AC1 and `## Notes` as an instruction to `refine`, not left as an assumption.
  - **The item was resumed to `draft` rather than left at `awaiting-answer`, and no new question
    was filed this turn.** This is the judgement call in this execution, so it is recorded in
    full. `spec/question.md` §4 conditions 1 (intent/fact no document records) and 4 (the record
    is genuinely silent and the consequences are material) do apply to the missing CSV format —
    the escalation would be justified in substance. What made filing it now the wrong move is
    timing: the stakeholder has already been asked this exact thing in this exact file and
    answered that they do not have it to hand, so re-filing immediately would stop the entire
    pipeline on a question whose answer is known to be "not yet". WI-0004 is last in the delivery
    order the stakeholder gave in EP-001/Q-001, and the next skill to act on it is `refine`,
    which may put the question to them directly at the moment the answer is actually needed.
    Nothing proceeds on a guess in the meantime: `draft` is exactly the status that says the item
    is not yet proven fit to start, and AC1 now carries the gap on its face.
  - **Risk accepted, and named so it is not lost:** if `refine` reaches WI-0004 and treats the
    format as a detail it can assume, this decision will have converted a blocking question into
    a silent assumption. The three numbered instructions in `## Notes` and the wording of AC1
    exist to make that failure loud rather than quiet, and `docs/product/vision.md` v4 records
    the same fact at product level where a reader who never opens WI-0004 will still see it.
- **Questions raised:** none this execution. The outstanding CSV-format question is `refine`'s to
  file when it acts on WI-0004, per the decision above.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (before the transition) → exit 1,
    `question.awaiting.none-open` on WI-0004 and `board.stale` — the protocol-required interval
    between answering the last blocking question and resuming the item; same note as WI-0003's
    journal entry of 2026-08-21T21:23:00Z.
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to draft --actor answer-questions --reason "Q-001 answered in part and propagated: payer and sharers given at import (AC6); CSV format still unknown, recorded in AC1 and notes for refine"` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after the transition) → exit 0, 0 errors, 1 pre-existing warning
- **Gates:**
  - `answer-is-propagated` → **pass**. Both files named in `## Consequences` were reopened after
    writing: `tracker/items/WI-0004/item.md` carries the amended AC1, the new AC6, the new
    out-of-scope bullet and the rewritten `## Notes`; `docs/product/vision.md` is at v4 with the
    import rule under "Not a bank integration" and the missing format named as the one
    outstanding fact.
  - `answered-from-the-record` → **pass** for the answered half — the stakeholder's own words,
    with the sharer default derived from WI-0002 AC2 and cited there. For the unanswered half the
    entry states explicitly that the record is silent, that nothing was decided in its place, and
    where the obligation now sits. No ADR was written, because no decision was made.
  - `escalation-is-justified` → **skipped**. This execution re-addressed nothing to the human, so
    the gate has nothing to check. The conditions that *would* justify an escalation, and why it
    was deferred to `refine` rather than filed now, are under **Decisions**.
  - `workspace-valid` → **pass**, checked after the transition (exit 0).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:12:36Z, `draft` →
    `awaiting-answer`, actor `intake`) records `resume-to: draft`; this execution transitioned to
    `draft`.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — answered, `answered-by: human`, consequences listed
  - `tracker/items/WI-0004/item.md` — AC1 amended, AC6 added, out-of-scope and notes rewritten
  - `docs/product/vision.md` — v3 to v4
- **Status:** `awaiting-answer` → `draft`
- **Result:** How a bank row becomes an expense is settled and written into AC6. What the bank's
  file looks like is still unknown, is recorded as such on the item and in the vision, and is
  `refine`'s to obtain before WI-0004 can be called Ready.

## 2026-08-21T21:38:30Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** not dispatched by `next` — `next` dispatched `refine` on WI-0001 this run. This
  entry records two questions filed as part of that execution's batch, under the standing rule
  for this project that when the pipeline is about to stop on a human-addressed question, every
  question already known to be needed is filed in the same round trip. `item.md` is untouched.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md`, `questions/Q-001.md` (answered
    in part earlier this session)
  - `tracker/items/EP-001/item.md` — the delivery order and the exclusion of editing and deleting
  - `docs/product/vision.md` (v5), which records the missing CSV sample as the one outstanding
    fact the product depends on
  - `.claude/agile-skills/spec/question.md` §4 and §6, `spec/dor-dod.md` §1
- **Decisions:**
  - **Q-002 re-asks the outstanding half of Q-001: the CSV format.** This item's `## Notes` — as
    rewritten by `answer-questions` — instruct `refine` to obtain the sample, not to invent a
    format, and to file a question and suspend if it has not arrived. It has not arrived. Filed
    as a new question citing Q-001 rather than by reopening it, per `spec/question.md` §6.
    Escalation conditions: §4.1 (a fact no document records) and §4.4 (the record is genuinely
    silent and the consequences are material).
  - **Q-002 offers a way out that is not "wait indefinitely".** Rationale: the stakeholder has
    already said once that they do not have the file to hand, so an option set consisting only of
    "please send it" risks the same answer and another stalled round trip. Option C — drop
    WI-0004 from this epic and refile it when the file exists — is offered because an item nobody
    can start is more honest as a deferred item than as one permanently on the board. Option B,
    working from the bank's published format, is offered with its real cost stated: everything
    would rest on a documented guess and would need verifying twice.
  - **Q-003 asks what happens when the same file is imported twice.** This is an R10 failure the
    item names on itself: the out-of-scope list says explicitly that re-import behaviour is *not*
    decided and is refinement's. It is worth the stakeholder's attention rather than an
    assumption because EP-001 excludes deleting or editing an expense, so an accidental double
    import cannot be undone by any means the tool offers — the remedy is deleting the data file.
  - **Both were filed now rather than when WI-0004 is dispatched.** Rationale: WI-0004 is last in
    the delivery order, so if these waited they would be asked several round trips from now, and
    the CSV sample is the long-lead item — the stakeholder has to go and find it. Asking early
    costs nothing, because the loop is stopping on WI-0001's questions regardless.
  - **The format was still not invented, and no importer was designed against a guess.** AC5
    requires refusing a file that is not in the expected format; if the expected format were an
    invention, AC5 would check the invention against itself.
- **Questions raised:** `Q-002`, `Q-003` (both blocking, to `human`). No
  `artifacts/refinement-qa.md`: no exchange has taken place, and this item has not been refined.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to awaiting-answer --actor refine --resume-to draft --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after all four suspensions) → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 once every item carrying a new
    blocking question had been suspended).
  - `definition-of-ready` → **not evaluated in full**. This execution did not attempt to make
    WI-0004 Ready, and it could not: **R4 fails** on AC1, AC2 and AC5, every one of which turns
    on a file format nobody has seen, and **R10 fails** on re-import behaviour. Those two
    failures are what Q-002 and Q-003 exist to clear. Recording the remaining criteria as passed
    would claim checks this execution did not perform.
  - `criteria-are-decidable` → **fail**, for the three criteria named above. AC3, AC4 and AC6 are
    decidable once a sample exists.
  - `qa-recorded-verbatim` → **skipped**. There is no exchange to record.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-002.md`, `Q-003.md` (new)
  - `tracker/items/WI-0004/item.md` — **unchanged**, deliberately
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** The bank CSV sample is asked for again, with an explicit option to defer the item
  instead; and the unanswered re-import behaviour is put to the stakeholder. WI-0004 is suspended
  and returns to `draft` when they answer.

## 2026-08-21T21:47:20Z — answer-questions v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer`; the stakeholder filled in both questions' `## Answer`
  between turns, so this execution was run ahead of `next`.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-002.md` and `Q-003.md` (both answered by the stakeholder),
    `Q-001.md` (answered earlier, half of it deferred into Q-002)
  - `tracker/items/WI-0004/item.md` (AC1–AC6, `## Out of scope`, `## Notes`), `history.md`
    (`resume-to: draft`), `journal.md`
  - `tracker/items/EP-001/item.md` (SM3, `## Scope`, the delivery order), `tracker/items/WI-0002/item.md`
    (AC2 and the date rule propagated earlier this turn)
  - `docs/product/vision.md` (v8), `docs/architecture/adr/ADR-0005` (v1, refusals and exit codes)
  - `.claude/agile-skills/pipeline.yaml` (orchestrator step 2 — what an open human question costs)
  - `tracker/items/WI-0004/artifacts/plan.md` — **does not exist**; nothing planned yet
- **Decisions:**
  - **Q-002: the missing fact is still missing, and nothing was invented.** The stakeholder has now
    said twice that they do not have the CSV export to hand. AC1, AC2 and AC5 stay undecidable, and
    the item's notes repeat the instruction not to guess a format, because an importer written
    against a plausible layout would parse a file that does not exist.
  - **Q-002: the scope half is a real answer, and it is a refusal of option C.** "The import stays
    part of this... I'm not signing off on a version without it." Recorded as intent in
    `tracker/items/EP-001/item.md` rather than only here, because its consequence belongs to the
    epic: EP-001's Definition of Done needs every child `done`, so **the epic cannot close until
    the sample arrives**. An epic that looks closeable while one of its success measures is
    unbuildable is precisely the quiet lie the record exists to prevent.
  - **Q-002 was closed rather than left open, deliberately.** An open human-addressed question stops
    the entire loop at orchestrator step 2, and this one's answer is known to be "not yet". Leaving
    it open would have stopped WI-0001 to WI-0003 — none of which needs the sample — to wait for a
    fact the stakeholder does not have. Closing it returns the chase to `refine`, which owns it and
    may ask directly; the item's notes now say that when the orchestrator reaches WI-0004 (last, by
    priority) `refine` should expect to re-ask and suspend, and that this is the correct outcome
    rather than a failure. This is the same reasoning that closed Q-001's unanswered half, recorded
    again because the situation recurred.
  - **Q-003: option C, in the stakeholder's own words.** A repeat import warns, names when the file
    was imported before, imports nothing and exits 1; `--again` lets the deliberate case through.
    Option B (outright refusal) costs the same to build and makes a decision the user cannot undo,
    which is the wrong trade in an epic that cannot delete an expense.
  - **"The same file" was defined as the same contents, not the same path.** Without that, AC7 is
    not checkable and a rename would defeat the safeguard. What identifies the contents is left to
    `plan`, with a hash named as the obvious candidate — the criterion constrains the property, not
    the mechanism.
  - **The new stored state was flagged for `plan` explicitly.** Remembering which files have been
    imported is the first thing this epic stores that is not derivable from the expenses, so it
    changes the shape of the data file and not just one command's behaviour.
  - **Criteria changed:** **AC7 added**; AC2 was amended earlier in this turn under WI-0002/Q-002
    (the row's own date); the `## Out of scope` entry that left re-import behaviour undecided was
    replaced by one that decides it and keeps only row-level detection out.
- **Questions raised:** none. Nothing was re-addressed to the human, and specifically the CSV
  sample was **not** re-escalated a third time in this turn: `spec/question.md` §4.1 and §4.4 do
  apply to it in substance, but the stakeholder has just answered that they do not have it, so the
  escalation belongs to the moment `refine` reaches the item rather than to now.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to draft --actor answer-questions --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, every file reopened after writing.
    `tracker/items/WI-0004/item.md` carries AC7, the rewritten out-of-scope entry, and notes
    recording both answers and their consequences for `plan` and `refine`.
    `tracker/items/EP-001/item.md` `## Scope` carries "The import is not optional and this epic
    cannot close without it", quoting the stakeholder. `docs/product/vision.md` is at v9 with both
    answers and the change-log row.
  - `answered-from-the-record` → **pass**. Both answers are the stakeholder's own sentences, quoted
    in the question files; the exit code and stream on AC7 follow from ADR-0005, cited; the
    consequence for closing EP-001 follows from the epic Definition of Done in `spec/dor-dod.md`.
  - `escalation-is-justified` → **skipped**. Nothing was re-addressed to the human this execution.
    The reasoning for *not* re-escalating the CSV sample is recorded under Questions raised.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:31:44Z, `refine`)
    records `resume-to: draft`; this execution transitioned WI-0004 to `draft`.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-002.md`, `Q-003.md` — answered, `answered-by: human`, each
    with a `## Consequences` list of files
  - `tracker/items/WI-0004/item.md` — AC7 added, `## Out of scope` re-import entry rewritten,
    `## Notes` extended with both answers
  - `tracker/items/EP-001/item.md` — `## Scope` gains the "import is not optional" paragraph
  - `docs/product/vision.md` — v8 to v9
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of WI-0004's open questions are closed. Re-importing a file now has a defined
  behaviour (warn, refuse, `--again` to confirm), and the import is confirmed as non-negotiable
  scope — which means EP-001 cannot be closed until the stakeholder supplies the CSV sample. The
  item returns to `draft` at the back of the delivery order; `refine` will have to ask for the
  sample again when it gets there.

## 2026-08-21T22:47:30Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next`; WI-0001, WI-0002 and WI-0003 are all `done`, so
  this is the last child of EP-001 and the last runnable item.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` (AC1–AC7, `## Out of scope`, `## Notes` — including the three
    instructions the previous `answer-questions` execution left for this one), `history.md` (four
    rows: two suspensions, two resumptions), `journal.md`
  - `tracker/items/WI-0004/questions/Q-001.md` (half answered), `Q-002.md` (the sample re-asked and
    still not supplied; the scope half answered), `Q-003.md` (re-import: answered)
  - `docs/architecture/adr/ADR-0002`, `ADR-0003`, `ADR-0005` (clause 2 and its note about partial
    imports), `ADR-0006`, `ADR-0009`; `docs/architecture/overview.md` (v3);
    `docs/product/vision.md` (v9); `tracker/items/EP-001/item.md` (`## Scope`, SM3)
  - `tracker/items/WI-0002/item.md` (AC2 and the `--shared-by` semantics the import must match) and
    `WI-0003/item.md` (what the report needs from an imported expense)
  - The delivered code: `expenses_tool/cli.py`, `expenses.py`, `store.py` — to check that the
    criteria this item can state now fit the tool that exists
- **Decisions:**
  - **Refined everything that does not depend on the bank's format, then filed the question.** Six
    of the nine criteria are now decidable: the command and its options (AC6), the re-import warning
    and `--again` (AC7), a skipped row (AC4), a missing or unreadable file (AC8), refusals leaving
    the ledger untouched and the write being atomic (AC9), and the downstream-indistinguishability
    of an imported expense (AC3). Doing this now means that when the sample arrives, only the three
    format-dependent criteria need writing.
  - **AC1, AC2 and AC5 are marked "blocked on the sample" in the criteria themselves**, rather than
    left looking finishable. A reader of the item can see exactly which three fail R4 and why.
  - **A skipped row exits 0; a rejected file exits 1.** ADR-0005 clause 2 makes a refusal exit 1 and
    store nothing, and its consequences section explicitly flagged the partial-import case as
    needing a decision. This is that decision: most of the file imported, so the command succeeded
    and reports what it skipped. Getting this wrong the other way would make every statement with
    one odd row look like a failed import.
  - **A skipped row is named by line number and quoted.** "Reported to the user, naming the row" was
    not something `verify` could check.
  - **AC7's message names the date of the previous import and the flag that overrides it.** A
    warning that does not say how to proceed makes the user guess, and this is the one warning in
    the tool that stands between them and a doubled ledger they cannot undo.
  - **No `--date` option, and it is now out of scope.** Every imported expense takes its row's date
    (WI-0002/Q-002); an option overriding all of them would throw away exactly what that answer was
    given to preserve. This is the kind of option that gets added later "for convenience" and
    quietly defeats a decision, so it is excluded rather than merely absent.
  - **AC8 and AC9 were added.** A missing file is the first thing anyone hits and nothing said what
    happens; and atomicity matters more here than anywhere else in the epic, because one import
    creates many expenses at once and an interruption could otherwise leave half a statement in the
    ledger.
  - **`Q-004` was filed rather than the Definition of Ready being overridden.** An override would
    mean building against an invented format, which the item's own notes forbid and which AC5 would
    then be unable to check. The question shows the stakeholder what already works, says why the
    ask cannot be worked around, names `spec/question.md` §4.1 as the condition, and offers a
    one-row version if pasting three is the friction — the third ask should cost them less than the
    first, not more.
  - **The stakeholder was not asked anything else.** Everything else on this item is either settled
    by their earlier answers or delegated by them, and adding questions to a batch they did not need
    would spend the one thing this protocol is careful with.
- **Questions raised:** `Q-004` — blocking, addressed to `human`. The item is suspended on it.
  `artifacts/refinement-qa.md` records all four questions with the stakeholder's words verbatim, six
  `[assumed]` decisions and three `[unresolved]` entries.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before filing; **exit 1
    between filing and transitioning** (`question.blocking.item-not-awaiting`), which is the
    expected window; exit 0 after the transition.
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to awaiting-answer --actor refine --resume-to draft --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition).
  - `definition-of-ready` → **fail**, criterion by criterion:
    **R1 pass** — frontmatter complete; `priority: medium`, `epic: EP-001`.
    **R2 pass** — the story names the role, the capability and the outcome.
    **R3 pass** — AC1 to AC9, each a labelled checkbox.
    **R4 fail** — AC1, AC2 and AC5 are not decidable by observation, because the file format they
    describe is unknown. AC3, AC4, AC6, AC7, AC8 and AC9 now name commands, exact messages and exit
    codes and would pass on their own.
    **R5 pass** — `## Out of scope` names nine things, three added here.
    **R6 fail** — `Q-004` is open and blocking, which is the intended state, not a defect.
    **R7 pass** — no `depends-on`; WI-0001 to WI-0003 are all `done`, so everything this item builds
    on exists.
    **R8 pass** — `artifacts/refinement-qa.md` records the whole exchange verbatim, including the
    two answers that did not supply the fact and the open fourth question.
    **R9 pass** — importing a statement is one coherent change, reusing the record path
    `add-expense` already provides.
    **R10 pass** — the combinations that can be stated are stated: `--shared-by` present and absent
    (AC6), a repeat import with and without `--again` (AC7), a bad row among good ones (AC4), a
    missing file (AC8), each refusal against the stored ledger (AC9). Three are named as
    deliberately unconstrained in `## Notes`.
  - `criteria-are-decidable` → **fail**, for AC1, AC2 and AC5 only, and by design: they are marked
    "blocked on the sample" in the criteria themselves. For the other six: AC3 — import anything,
    run `report` and `list-expenses`, compare against the same expenses added by hand. AC4 — a
    three-row file with an unusable middle row: two expenses recorded, one message naming line 2,
    exit 0. AC6 — `--paid-by Dan` with Dan unregistered: stderr `Unknown person: Dan`, exit 1,
    nothing imported. AC7 — import, import again: the quoted message with the date, exit 1, then
    `--again`: the expenses appear twice. AC8 — a path that does not exist: a message naming it,
    exit 1, no traceback. AC9 — `cmp` the data file across each refusal.
  - `qa-recorded-verbatim` → **pass**. All four questions with the stakeholder's answers copied
    unaltered, including both "I'll send you a sample later" replies, and their scope statement
    quoted in full. What refinement decided is separated from what they said.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-004.md` (new)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0004/item.md` — AC1 to AC7 rewritten, AC8 and AC9 added, three criteria marked
    blocked, `## Out of scope` extended by three entries, `## Notes` extended with what refinement
    decided, what is still blocked and what is left unconstrained
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** WI-0004 is as Ready as it can be without the stakeholder: six of nine criteria are
  decidable, the command surface and every non-format behaviour are pinned, and the three criteria
  that need the bank's export format are marked as blocked rather than guessed. `Q-004` asks for the
  sample a third time, with a one-row fallback. This is the last item in the epic, so the pipeline
  now has nothing else to run.

---

## 2026-08-21T22:52:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer`; the stakeholder filled in `## Answer` on `Q-004` between
  sessions, so the question is answered and its consequences have to reach the artifacts before the
  item can move. Run ahead of `next`, which would otherwise have stopped on an open human question
  that is no longer open.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md`
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md`
  - `tracker/items/EP-001/item.md`, `tracker/items/EP-001/questions/Q-001.md`
  - `docs/product/vision.md` (v9)
  - `docs/architecture/adr/` — all ten ADRs listed; ADR-0002 (command surface) and ADR-0005
    (streams and exit codes) read, being the two WI-0004's settled criteria rest on. None of them
    speaks to the bank's file format, so nothing this answer records contradicts a recorded
    decision.
  - There is no `artifacts/plan.md`: WI-0004 has never been Ready, so nothing has been planned.
- **Decisions:**
  - **Q-004 — answered by the human, propagated.** Route: **escalated, and the escalation came
    back.** The stakeholder wrote: *"I'll send you a sample later — still haven't got to it. I'd
    rather you wait for my actual file than guess at the format."* The fact itself is still missing,
    so AC1, AC2 and AC5 stay undecidable — but the answer is not empty. The second sentence declines
    option B (work from the bank's *published* export format), which was the only route offered that
    would have let building start now. Waiting therefore stops being `refine`'s judgement and
    becomes the stakeholder's instruction, which is a materially stronger footing and is the thing
    worth propagating. Option C — the header line and one real row — is untouched by the objection,
    since they refused a guess and not a smaller paste, so the minimum ask is narrowed to that.
  - **No ADR written.** The answer records the absence of a fact plus a constraint on how to
    proceed without it. It decides no design and closes no option that code depends on, so there is
    nothing an ADR would hold. `answered-from-the-record` is satisfied by the stakeholder's own
    words rather than by a document, which is the strongest of the four routes.
  - **One acceptance criterion amended.** AC1's embedded instruction to `refine` now reads "the
    header line and at least one representative row" where it read "two or three representative
    rows". This does not change what the stakeholder asked for or what the importer must do — it
    changes how much sample material `refine` must obtain before AC1 becomes decidable, and it
    follows directly from their answer. The item has never been at `ready`, so no frozen criterion
    was touched. Recorded here because amending a criterion is one of the two things this skill is
    uniquely permitted to do and must never do quietly.
  - **The item returns to `draft`, not to `awaiting-answer`.** Every blocking question on WI-0004 is
    now answered, and `answer-questions` has no question left to escalate — it would be filing
    `refine`'s question for it. Chasing the sample belongs to `refine`, which may put a question to
    the stakeholder directly and is the skill the item's own notes already delegate it to. The
    expected next event is that `refine` files a standing request and suspends the item again; that
    is the pipeline waiting correctly, not the pipeline failing.
  - **Nothing was re-opened.** The scope decision from Q-002 — the import stays in, EP-001 does not
    close without it — was refused once by the stakeholder and is not asked again. `refine` is told
    so explicitly in `## Notes`, so the next asking spends their attention on the one missing fact.
- **Questions raised:** none. Nothing was re-addressed to the human by this execution: the one open
  question was answered by them, and there is no second question this skill could not settle.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before the transition,
    reporting `question.awaiting.none-open` and a stale board — the expected intermediate state once
    the last blocking question is answered but the item has not yet been resumed
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to draft --actor answer-questions
    --reason "..."` → applied; this skill has no completion transition of its own, so the move was
    not gated
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in `Q-004`'s `## Consequences` was opened
    after writing and the change confirmed present:
    `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q4 carries the verbatim answer tagged
    `[human]` and the two findings (guessing refused; one row is enough);
    `tracker/items/WI-0004/item.md` — line 29 AC1 reads "at least one representative row", line 217
    "Waiting is now the stakeholder's instruction", line 160 forbids the published-format route,
    line 168 tells `refine` to keep the next question short and standing;
    `tracker/items/EP-001/item.md` — line 76 "The wait is the stakeholder's own decision";
    `docs/product/vision.md` — line 135 the Q-004 bullet, line 155 the v10 change-log row.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own words, quoted in the
    question file and in `refinement-qa.md`. Checked against `docs/architecture/adr/` for
    contradiction: none of ADR-0001 to ADR-0010 constrains the bank's file format.
  - `escalation-is-justified` → **not applicable, recorded rather than skipped.** No question was
    escalated by this execution. `Q-004` was already addressed to the human when it was filed, and
    it has been answered; `spec/question.md` §3 rule 6 forbids reverting its status, so it is closed
    as answered rather than re-opened.
  - `workspace-valid` → **pass**. `python3 .claude/agile-skills/scripts/validate-workspace .`
    exit 0 after the transition and the board regeneration. Before the transition it reported
    `question.awaiting.none-open` and a stale board, both of which are the expected intermediate
    state between answering the last blocking question and resuming the item.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T22:42:01Z, actor `refine`)
    records `resume-to: draft`; this execution's row targets `draft`. They match.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-004.md` — `## Answer` and `## Consequences` written;
    `status: answered`, `answered-by: human`, `answered-at: 2026-08-21T22:52:00Z`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q4 rewritten from `[unresolved]` to the
    answer as given
  - `tracker/items/WI-0004/item.md` — AC1 amended; "Still blocked, and on what (R4)" extended with
    the third deferral and the instruction to wait; the instructions to `refine` renumbered to four,
    narrowing the ask and forbidding the published-format route
  - `tracker/items/EP-001/item.md` — the paragraph on why the epic cannot close now records that
    waiting is the stakeholder's decision
  - `docs/product/vision.md` — v9 → v10, one new bullet and one change-log row
  - the generated board, regenerated by its script
- **Status:** `awaiting-answer` → `draft` (`resume-to` on the suspending row)
- **Result:** The stakeholder's third deferral is consumed and on disk. The bank CSV format is still
  unknown and WI-0004 still cannot be Ready — but the record now says that waiting is their
  instruction rather than our inference, that the published-format workaround is closed, and that a
  header line plus one real row is enough. WI-0004 is back at `draft` for `refine` to chase.

---

## 2026-08-21T22:58:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md`
  - `tracker/items/WI-0004/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1
  - `docs/product/vision.md` (v10)
  - History read first, per precondition 3: this item did not come back from `verifying` or
    `in-review`. It has never been Ready. It reached `draft` from `awaiting-answer` three times, each
    time because the same fact was missing, most recently at 2026-08-21T22:52:00Z when
    `answer-questions` propagated the stakeholder's answer to Q-004.
- **Decisions:**
  - **Precondition 2 fails: the human is not present in this session**, and there is no interactive
    question tool. This skill's own failure path applies — file a question addressed to `human`
    naming what is needed, suspend the item with `resume-to: draft`, stop.
  - **No criterion was rewritten and no scope was changed.** The previous execution
    (2026-08-21T22:47:30Z) already refined everything that does not depend on the bank's format, and
    `answer-questions` amended AC1 at 22:52 to accept a single row. There is nothing left this skill
    can decide without the stakeholder, and re-refining settled criteria would only churn the
    record.
  - **Q-005 is a standing request, deliberately smaller than Q-004.** Q-004's answer instructed us
    to wait rather than guess and closed off the published-format route, so the only remaining
    variable is how much of their file is being asked for. The ask is now the header line and **one**
    real row — the smallest thing that satisfies "my actual file" — with the file's path offered as
    an alternative. The two decisions the stakeholder has already made (the import is not dropped,
    Q-002; the payer and sharers come from the command line, Q-001) are named in the question as
    explicitly not re-opened, per instruction 4 in the item's `## Notes`.
  - **No Definition of Ready override was sought, and none may be.** An override here would mean
    passing AC1, AC2 and AC5 against an invented format — the one outcome the item's notes and the
    stakeholder's own answer to Q-004 forbid.
  - **The item is not `blocked`.** `blocked` is terminal and means an impasse only a human can
    move. This is a wait, not an impasse: the stakeholder has said the file is coming, and
    `awaiting-answer` with an open question addressed to them is exactly how this pipeline
    represents waiting on a person.
- **Questions raised:** 1 — `Q-005` (blocking, to `human`), recorded in `artifacts/refinement-qa.md`
  as Q5 `[unresolved]`. Carried forward from Q-001, Q-002 and Q-004, all of which are `answered`.
  This is the fourth asking of the same fact.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to awaiting-answer --actor refine
    --resume-to draft --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after the transition.
  - `definition-of-ready` → **fail**, on R4 alone, and not passed by override. Criterion by
    criterion, unchanged from the previous execution except where noted:
    **R1 pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`.
    **R2 pass** — role (the person keeping the group's books), capability (feed the bank's CSV
    export in and have it create expenses), outcome ("so that I stop retyping transactions").
    **R3 pass** — AC1 to AC9, labelled and checkboxed.
    **R4 fail** — AC1, AC2 and AC5 are not decidable by observation, because the column names, the
    date format and the sign convention of the stakeholder's bank export are unknown. Each says so
    in its own text. The other six are decidable and were checked as such last execution; AC1's
    embedded instruction now accepts a single row (amended by `answer-questions` when Q-004 was
    answered).
    **R5 pass** — `## Out of scope` names eight things, including reading the payer from the file
    and any row-level duplicate detection.
    **R6 fail** — `Q-005` is open and blocking. This is the mechanical consequence of suspending
    the item and is expected; it clears when the sample arrives.
    **R7 pass** — no `depends-on`; WI-0001 to WI-0003 are `done`.
    **R8 pass** — `artifacts/refinement-qa.md` records all five questions with the stakeholder's
    answers verbatim and every assumption tagged.
    **R9 pass** — one coherent change: an import path onto the record path `add-expense` already
    provides.
    **R10 pass** — every option and flag has a stated behaviour or is named out of scope, and three
    gaps are recorded in `## Notes` as deliberately unconstrained by `refine`.
  - `criteria-are-decidable` → **fail**, for AC1, AC2 and AC5 only, by design and unchanged: they
    are marked "blocked on the sample" in the criteria themselves. AC3, AC4, AC6, AC7, AC8 and AC9
    each name a command and a verdict, recorded in the previous execution's entry.
  - `qa-recorded-verbatim` → **pass**. Five questions, four answered by the stakeholder with their
    words copied unaltered — including all three "I'll send you a sample later" replies and the
    Q-004 sentence that closed off guessing — and the fifth recorded as filed and open. What
    refinement decided is kept separate from what they said.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-005.md` (new)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q5 section added
  - `tracker/items/WI-0004/item.md` — "Still blocked, and on what (R4)" notes Q-005 as the fourth
    asking, reduced to the header line and one row
  - the generated board, regenerated by its script
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** Nothing could be refined that had not been refined already. The item is suspended on
  `Q-005`, a standing request for the header line and one real row of the stakeholder's bank export.
  No format was invented, no Definition of Ready override was sought, and the item is not marked
  blocked, because the stakeholder has said the file is coming. WI-0004 is the last item in EP-001,
  so the pipeline now has nothing runnable and stops on this question.

## 2026-08-21T23:05:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer`; the stakeholder filled in `## Answer` on `Q-005` between
  sessions, so the question is answered and its consequences have to reach the artifacts before the
  item can move. Run ahead of `next`, which stops at step 2 on any open human-addressed question and
  would have spent the whole turn stopped on one that is no longer open.

- **Inputs read:** `questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (all `answered`) and
  `Q-005.md` (open, and now carrying an answer written by the stakeholder); `item.md`;
  `history.md`; `artifacts/refinement-qa.md`; `tracker/items/EP-001/item.md`;
  `docs/product/vision.md` v10; all ten ADRs, ADR-0002 (command surface) and ADR-0005 (streams and
  exit codes) in detail, because they are what the six decidable criteria rest on. No `plan.md`
  exists — this item has never been planned.
- **Decisions:**
  - **Q-005 — answered by the human**, route **escalated / answered by the human**. Their words,
    copied unaltered: *"I'll send you a sample later — still haven't got to it. I'd rather you wait
    for my actual file than guess."* This is the fifth deferral of the same fact. Consuming it is
    this skill's job even though the question was addressed to `human`: the precondition about
    architect-addressed questions is written for the case where the human has **not** answered, the
    skill's own step 4 provides for `answered-by: human`, and nothing else in the pipeline can
    propagate a human's answer. An answered question left open stops the orchestrator at step 2
    forever, so leaving it would have cost the whole turn.
  - **What the answer settles, and it is not nothing.** Two things beyond "still waiting". First,
    the wait is now a *confirmed standing* instruction rather than a remark: Q-004 said "guess **at
    the format**", this one says "guess", so it covers any layout the stakeholder did not supply,
    however arrived at. Second, Q-005 deliberately shrank the ask — the header line and one row, or
    just the path — and got the same answer, which is evidence that the size of the ask is not the
    obstacle. That is the fact this execution propagated.
  - **No design decision was taken and no ADR written.** The answer defers a design rather than
    making one. Amending an acceptance criterion to route around the gap was considered and refused:
    AC1, AC2 and AC5 are undecidable because a fact is missing, and rewriting them to be decidable
    without that fact would be reshaping the target around the arrow.
  - **The item was not marked `blocked`.** `blocked` is terminal and means an impasse only a human
    can lift; this is a wait the stakeholder says will end, and marking it terminal would close the
    only channel through which the sample can arrive.
- **Questions raised:** none. Nothing was re-addressed to the human by this execution. The next
  refinement will have to ask again, and the item now instructs it not to ask the same question a
  sixth time — see `## Notes`, `refine` instruction 3 as amended.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (before)
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to draft --actor answer-questions
    --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (after)
- **Gates:**
  - `answer-is-propagated` → **pass**. Both files named in Q-005's `## Consequences` were re-opened
    after writing and the change confirmed present:
    `artifacts/refinement-qa.md` — the Q5 section now carries the stakeholder's answer verbatim,
    keeps the fact `[unresolved]`, and records the two new `[human]` findings;
    `item.md` — "Still blocked, and on what (R4)" now reads five askings and five deferrals with
    Q-005's answer quoted, plus a new paragraph stating that reducing the ask did not work, and
    `refine` instruction 3 is amended to forbid a sixth identical asking. The `Not changed, and why`
    list in the same section records `docs/product/vision.md` staying at v10 and the absence of an
    ADR, with reasons, so the gate can tell a deliberate non-change from an omission.
  - `answered-from-the-record` → **pass**, in the strongest form available: the answer is the
    human's own text in the question file, quoted rather than interpreted. The surrounding
    reasoning cites `refinement-qa.md` Q4 (the earlier, qualified wording) and Q-002's scope
    refusal, both already in the record.
  - `escalation-is-justified` → **not applicable this execution**; no question was escalated or
    re-addressed. Recorded rather than omitted. (Q-005 itself was escalated by `refine` under
    `spec/question.md` §4.1 — intent no document records — and that justification stands.)
  - `workspace-valid` → **pass**. `validate-workspace .` exit 0, before and after.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T22:50:03Z, `refine`) records
    `resume-to: draft`; the item was returned to `draft` and to nothing else.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-005.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-08-21T23:05:00Z`; `## Consequences` written naming two changed files and
    three deliberate non-changes.
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q5 section rewritten with the verbatim
    answer and the two new `[human]` findings.
  - `tracker/items/WI-0004/item.md` — R4 section updated to five askings; new paragraph on the ask
    having been reduced without effect; `refine` instruction 3 amended.
  - `docs/product/vision.md` — deliberately **not** bumped; v10 already states the wait as the
    stakeholder's instruction and this answer repeats rather than changes it.
- **Status:** `awaiting-answer` → `draft` (the recorded `resume-to`)
- **Result:** The stakeholder's fifth deferral is consumed and propagated, so the orchestrator is no
  longer stopped on an answered-but-open question. The bank CSV format is still unknown, no format
  has been invented, and AC1, AC2 and AC5 are still undecidable. WI-0004 returns to `draft` with one
  new instruction on it: the next asking must offer a way out of the wait that guesses nothing.

## 2026-08-21T23:12:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** dispatched by `next` as the owner of status `draft`; the only runnable item in the
  workspace — EP-001 is `open` with a null owner and WI-0001 to WI-0003 are `done`. The item
  returned to `draft` minutes earlier when `answer-questions` consumed the stakeholder's answer to
  `Q-005`.
- **Inputs read:** `item.md` (including the `## Notes` instruction written this turn by
  `answer-questions`), `history.md` — nine rows, none of them a send-back from `verifying` or
  `in-review`, so this is a fresh refinement and not a defect fix — `journal.md`,
  `artifacts/refinement-qa.md` (Q1–Q5), all six question files, `tracker/items/EP-001/item.md`,
  `docs/product/vision.md` v10, `docs/architecture/adr/ADR-0002` and `ADR-0005`,
  `.claude/agile-skills/spec/dor-dod.md` §1.
- **Decisions:**
  - **Nothing in the item was rewritten.** The fourth refinement already refined everything that
    does not depend on the bank's format, and AC3, AC4, AC6, AC7, AC8 and AC9 are unchanged and
    decidable. Re-refining settled criteria would churn the record without improving it.
  - **The one thing this execution had to decide was what to ask, given that asking again in the
    same words has failed five times.** Precondition 2 fails — the stakeholder is not in this
    session — so the escalation path applies either way; the choice was between re-filing the
    standing request unchanged and putting something new. The item's own notes, amended when Q-005
    was answered, require the latter, and the reasoning is in the evidence: Q-005 reduced the ask to
    the header line and a single row, or merely the file's path, and got the same answer as the
    three larger askings, so the size of the ask is not what is stopping it.
  - **`Q-006` asks whether the tool should take the file's shape from the stakeholder at import
    time** — named date, amount and description columns plus a date format — rather than knowing
    their bank's layout in advance. This is not the guessing they forbade in Q-004 and Q-005: under
    that route the tool holds no assumption about any bank, every fact about the file comes from the
    stakeholder about the file in front of them, and AC5 becomes "refuse a file whose header does
    not contain the columns you named", which is a check against something stated rather than an
    invention checked against itself. It is a question and not a decision `refine` could take,
    because it trades typing at every import for having the feature now, and only they can price
    that trade.
  - **The standing request is preserved, not replaced.** Option A of Q-006 is "keep waiting", stated
    as a legitimate answer rather than a failure, and the sample stays useful under option C.
  - **Nothing already decided is reopened.** Q-006 says so explicitly for both: dropping or
    deferring the import (refused in Q-002) and where the payer and sharers come from (settled in
    Q-001).
  - **No Definition of Ready override was sought**, and none should be: an override here means
    building an importer against a format nobody has, which this item's notes forbid and the
    stakeholder has twice forbidden in their own words.
- **Questions raised:** one — `Q-006`, blocking, addressed to `human`, recorded in
  `artifacts/refinement-qa.md` as Q6 `[unresolved]`. Q1, Q2, Q4 and Q5 are `answered`; Q3 is
  `answered`. This is the fifth refinement of this item and the sixth question on it.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to awaiting-answer --actor refine
    --resume-to draft --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after the transition.
  - `definition-of-ready` → **fail**, on R4 and R6 only, and not passed by override. Criterion by
    criterion:
    **R1 pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`.
    **R2 pass** — role (the person keeping the group's books), capability (feed the bank's CSV
    export in and have it create expenses), outcome ("so that I stop retyping transactions").
    **R3 pass** — AC1 to AC9, each labelled and checkboxed.
    **R4 fail** — AC1, AC2 and AC5 are still not decidable by observation: the column names, the
    date format and the sign convention of the stakeholder's export are unknown. Each criterion says
    so in its own text. The other six were checked decidable in earlier executions and are unchanged.
    Q-006 offers the route that would make all three decidable without the sample; until it is
    answered, R4 fails.
    **R5 pass** — `## Out of scope` names eight things.
    **R6 fail** — `Q-006` is open and blocking. Mechanical consequence of suspending the item.
    **R7 pass** — no `depends-on`; WI-0001 to WI-0003 are `done`.
    **R8 pass** — `artifacts/refinement-qa.md` records all six questions with the stakeholder's
    answers verbatim and every assumption tagged.
    **R9 pass** — one coherent change.
    **R10 pass** — three gaps recorded in `## Notes` as deliberately unconstrained.
  - `criteria-are-decidable` → **fail**, for AC1, AC2 and AC5 only, by design and unchanged; each is
    marked "blocked on the sample" in its own text. AC3, AC4, AC6, AC7, AC8 and AC9 each name a
    command and a verdict.
  - `qa-recorded-verbatim` → **pass**. Six questions; the stakeholder's five answers copied
    unaltered, including all four "I'll send you a sample later" replies and both sentences refusing
    a guess. What refinement decided is kept separate from what they said, and Q6 is recorded as
    filed and open rather than as an answer.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-006.md` (new)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q6 section added
  - `tracker/items/WI-0004/item.md` — "Still blocked, and on what (R4)" records Q-006, what it
    offers, and what would change under each answer
  - the generated board, regenerated by its script
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** Nothing could be refined that had not been refined already, and the sample has not
  arrived. Rather than ask for it a sixth time in the same words, this execution put the stakeholder
  a choice they have never been offered — let the tool learn the file's shape from them at import
  time, or keep waiting — which is the only way found to make AC1, AC2 and AC5 decidable without
  guessing a format. No format was invented, no Definition of Ready override was sought, and the
  item is not `blocked`, because a wait the stakeholder can end is not an impasse. WI-0004 is the
  last item in EP-001, so the pipeline now has nothing runnable and stops on this question.

## 2026-08-22T09:05:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer` with `Q-006` open and blocking. Not dispatched by `next`:
  the stakeholder had filled in `## Answer` since the previous turn, and `next` stops the loop on an
  open human-addressed question rather than dispatching anything, so this execution was run first
  and deliberately. This skill's first precondition is written for the case where the human has
  *not* answered; a human-addressed question they *have* answered is squarely this skill's job — its
  own step 4 provides for `answered-by: human` — and no other skill in the pipeline can consume it.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-006.md` — the question and the stakeholder's answer
  - `tracker/items/WI-0004/questions/Q-001.md` … `Q-005.md` — checked for anything still open; all
    five are `answered`, so `Q-006` was the only open question on this item and the only one in the
    workspace
  - `tracker/items/WI-0004/item.md` — the nine criteria, three of them marked "blocked on the
    sample", and the `## Notes` instructions to `refine`
  - `tracker/items/WI-0004/history.md` — `resume-to: draft`, recorded on the row of
    2026-08-21T22:56:53Z where `refine` suspended the item
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the six-question exchange and its tagging
    convention
  - `tracker/items/EP-001/item.md` — SM3 and the two paragraphs asserting the epic was blocked on
    the sample
  - `tracker/items/WI-0002/item.md` — AC1 to AC9, for the rendering form and the amount rule that
    the new AC1, AC2 and AC4 reuse rather than reinvent
  - `docs/product/vision.md` (v10) and `docs/architecture/overview.md` (v3)
  - `docs/architecture/adr/` — all ten. ADR-0002 (the `import-csv` name and the option style),
    ADR-0005 (streams and exit codes, including its note about partial imports), ADR-0006 (atomic
    write, and its anticipation of an import record as a third top-level key) and ADR-0009 (the
    import writes the same expense records) all bear on this answer. **None of them is contradicted
    by it** — checked explicitly, because an answer that contradicts a recorded decision would be an
    escalation and not an answer.
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`, `spec/journal-and-history.md`,
    `spec/work-item.md`
- **Decisions:**
  - **Q-006 — answered by the human; this execution consumed and propagated it.** The stakeholder
    chose option C: build the import against columns they name at import time, and keep the sample
    for a per-bank shortcut later. Their words are copied verbatim into the question, the item and
    `refinement-qa.md`. Reading it as three decisions plus one non-decision is the substance of the
    propagation:
    1. *Option C.* AC1, AC2 and AC5 rewritten against the named columns. They were the only three
       criteria failing R4, and they now name a command and a verdict like the other six. The
       criteria carry their own example file `$F` and mapping `$M`, labelled in the preamble as an
       example the checker writes — because a reader who mistook `$F` for the stakeholder's real
       statement would reintroduce exactly the invented format this item forbids.
    2. *Option D refused.* "Typing four options each time is fine" is a direct answer to the option
       that offered a config file. Recorded as new **AC10** (all four options required, exit 2 if
       one is missing) and as two out-of-scope entries. This matters beyond tidiness: Q-006's own
       option B said whether the tool remembers the mapping "would be settled separately, as a
       design detail", so without this the answer would have left `plan` an open decision the
       stakeholder had in fact already closed.
    3. *The sample stops blocking.* It is still expected and still useful, but what it buys is a
       shortcut, and that is a **new item** when it arrives. Propagated into EP-001, whose notes
       claimed "the only thing that will move EP-001 is the sample itself", and into `vision.md`,
       which claimed one thing was still outstanding. Both were true when written and are now
       false; leaving either would have stalled the epic on a dependency that no longer exists.
    4. *One assumption, recorded as an assumption.* Q-006's option B named one thing option C would
       leave open — a row whose amount is not a positive charge — and proposed skipping it like any
       other unusable row. The stakeholder did not address it. Silence is not agreement, so it is
       written into AC4 as an assumption they can correct and tagged `[assumed]` in
       `refinement-qa.md`, not attributed to them.
  - **No ADR written, deliberately.** The gate `answered-from-the-record` requires each answer to
    cite what it follows from *or* to record a new decision as an ADR. This answer follows from the
    stakeholder's own words, which are the strongest thing in the record and are now quoted in three
    artifacts; nothing here was decided by the architect. The one durable *architectural* fact — the
    parser takes a column mapping and the tool contains no bank format — is recorded in
    `docs/architecture/overview.md` v4, where `plan` reads it. Writing an ADR would either restate
    the stakeholder's decision as though this skill had made it, or pre-empt design choices that are
    `plan`'s to make and to record when it runs.
  - **Acceptance criteria were amended, and this is one of the two skills permitted to.** AC1, AC2
    and AC5 rewritten; AC4 extended with the definition of an unusable row; AC10 added. Recorded
    loudly here because criteria are frozen after `ready` — this item is at `draft`, so the freeze
    does not bite, but the rule that an amendment is journaled with its reason is not conditional.
    None of these amendments reshapes the target around anything already built: **no import code
    exists**. They replace three criteria that could not be checked at all with three that can, and
    what is being asked for is unchanged — feed a CSV in, get expenses out.
  - **A stale sentence in `## Notes` was removed rather than left.** It said re-importing the same
    file was "still undecided and is also `refine`'s"; Q-003 settled it and AC7 states it. The
    removal is described in place, because a note claiming an open decision is exactly the kind of
    thing a later reader acts on.
- **Questions raised:** none. Nothing in the answer needs the stakeholder again, and `Q-006` was the
  last open question in the workspace: all sixteen across five items are now `answered`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, before the edits
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 mid-execution, reporting
    `question.awaiting.none-open` on WI-0004 and a stale board — the expected transient state
    between answering the question and transitioning the item
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to draft --actor answer-questions
    --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, after the transition
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `Q-006`'s `## Consequences` was reopened
    after writing and the change confirmed present:
    `tracker/items/WI-0004/item.md` — AC1, AC2 and AC5 no longer contain the string "blocked on the
    sample"; AC4 carries the unusable-row definition; AC10 exists; three new out-of-scope entries;
    the `## Notes` block instructing `refine` to ask a sixth time is gone and the R4 heading now
    reads "No longer blocked".
    `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q6's `[unresolved]` line is replaced by the
    stakeholder's verbatim answer and four tagged consequences; `## Override` rewritten.
    `tracker/items/EP-001/item.md` — SM3 no longer names the bank's format; the "blocked on a fact
    only the stakeholder holds" paragraph is replaced.
    `docs/product/vision.md` — frontmatter `version: 11`, change-log row present, "One thing is
    still outstanding" gone.
    `docs/architecture/overview.md` — frontmatter `version: 4`, change-log row present, the
    no-bank-format paragraph present under "What is not here yet".
  - `answered-from-the-record` → **pass**, in its strongest form: the answer is the stakeholder's
    own words, quoted verbatim in the question, the item and the Q&A artifact. The record was not
    silent, so no ADR was required; why none was written anyway is under Decisions.
  - `escalation-is-justified` → **pass, vacuously**. No question was re-addressed to the human by
    this execution. The escalation being consumed here was `refine`'s, and it named its condition
    (`spec/question.md` §4.1, intent no document records) — correctly, since no document could have
    said whether typing four options per import was acceptable to them.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before the edits and exit 0 after the
    transition and board regeneration. The exit-1 in between is recorded above rather than hidden:
    it is the mechanical consequence of a question ceasing to be open while the item is still
    `awaiting-answer`, and it is why answering and transitioning belong to one execution.
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T22:56:53Z, `draft` →
    `awaiting-answer`, actor `refine`) records `resume-to: draft`; this execution transitioned
    WI-0004 to `draft`. Read from that row, not inferred from which skill asked.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-006.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-08-22T09:05:00Z`; `## Answer` extended with what the choice settles and what
    it deliberately does not; `## Consequences` written, naming six files
  - `tracker/items/WI-0004/item.md` — AC1, AC2 and AC5 rewritten; AC4 extended; AC10 added; the
    criteria preamble now defines `$F` and `$M`; three out-of-scope entries added; `## Notes`
    rewritten where it was stale or instructed a sixth asking
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — Q6 answered verbatim and tagged;
    `## Override` rewritten
  - `tracker/items/EP-001/item.md` — SM3 rewritten; the two "blocked on the sample" paragraphs
    replaced
  - `docs/product/vision.md` — v10 → v11, with a change-log row
  - `docs/architecture/overview.md` — v3 → v4, with a change-log row
  - the generated board, regenerated by its script
- **Status:** `awaiting-answer` → `draft` (the recorded `resume-to`)
- **Result:** The stakeholder answered the sixth question and it is the one that unblocks the item:
  the import will be built against columns they name at import time, so the CSV sample no longer
  gates WI-0004 or EP-001. Six artifacts carry the answer, three previously undecidable criteria are
  decidable, one new criterion records what they refused, and one open point is recorded as an
  assumption rather than attributed to them. WI-0004 returns to `draft` for `refine` to judge
  against the Definition of Ready; no question anywhere in the workspace is now open.

## 2026-08-22T09:22:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` as the only runnable item in the workspace
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — ten criteria, none any longer marked "blocked on the sample",
    plus the notes left by the execution of `answer-questions` that consumed Q-006
  - `tracker/items/WI-0004/history.md` — fourteen rows. **This is not a send-back:** the item
    reached `draft` from `awaiting-answer` by `answer-questions`, not from `verifying` or
    `in-review`, so this is the ordinary refinement job and not a repair of a specific defect
  - `tracker/items/WI-0004/journal.md` — six prior executions, including the stakeholder's verbatim
    answers to Q-001 to Q-006
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the six-question exchange and its tags
  - `tracker/items/WI-0004/questions/Q-001.md` … `Q-006.md` — all six `answered`
  - `tracker/items/WI-0001/item.md` (AC8's refusal shape), `tracker/items/WI-0002/item.md` (AC1's
    rendered form, AC3's date order, AC4's `Unknown person:` message, AC5's amount rule),
    `tracker/items/WI-0003/item.md` (the report's output, for AC3's comparison)
  - `docs/product/vision.md` (v11) and `docs/architecture/overview.md` (v4)
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/work-item.md`, `spec/question.md`
- **Decisions:**
  - **Nothing was asked of the stakeholder, and that is recorded as a decision** in
    `refinement-qa.md` under "Q7 — nothing was asked this time, and why that is the right call".
    Every gap found this pass was a matter of wording or of a combination nobody had stated, not a
    fact about what they want; the conventions they delegated in WI-0001/Q-004 (ADR-0002, ADR-0005)
    settle all of them. Re-asking for the sample would have been a seventh request for something no
    longer blocking, and re-asking about refunds would have re-litigated Q-006.
  - **AC1 now names its exact two lines of output** instead of describing them. `Imported ` plus
    WI-0002's rendered form, one line per accepted row, in file order, nothing else on stdout —
    chosen to match `add-expense`'s `Added <rendered>` rather than to invent a summary line, which
    would have been a second output format for the same fact.
  - **AC3 was turned into a comparison rather than a claim.** "Indistinguishable from a
    hand-entered one" cannot be checked as written; it now requires the same two expenses entered by
    hand into a second ledger `$U` to produce byte-identical `list-expenses` and `report` output.
    That is both decidable and a stronger check than any wording, because it fails on any difference
    at all. It says explicitly that the two *data files* are not compared — the imported ledger also
    remembers the import (AC7) — so a verifier does not read it as requiring identical bytes on disk.
  - **AC4 was the weakest criterion on the item and got the most work.** It defined an unusable row
    as "a row the tool cannot turn into an expense", which defines itself, and required "one message
    about the middle row" without saying what the message is. It now names a concrete three-row file
    `$G`, the exact stderr line `Skipped line 3: <raw line>`, the header-is-line-1 rule, and an
    exhaustive four-case definition of unusable that reuses WI-0002's own rules rather than adding
    any. One consequence is stated rather than left to be derived: a `--date-format` no row parses
    under — including one that is not a valid `strptime` format — skips every row and still exits 0.
    That is the most likely thing to go wrong in real use.
  - **Two "which one?" ambiguities were closed** — the column reported when several named columns
    are missing (date, then amount, then description) and the name reported when several people are
    unregistered (payer, then sharers left to right). Neither changes what a user can do; both are
    needed for two runs to report the same thing, which is what `verify` compares.
  - **Three interactions between this item's own options were found and stated (R10).** An import
    that records nothing is not remembered, so it can be retried without `--again`; `--again` on a
    never-imported file is an ordinary import rather than an error; and the column mapping is not
    part of a file's identity, so re-importing the same statement under different column names still
    warns. Each had two plausible readings and no criterion covered it.
  - **AC11 is new and covers the three reading conventions**: RFC 4180 quoting, trimmed cells, and a
    leading UTF-8 BOM ignored. These are properties of real CSV files rather than of any bank, so
    stating them does not reintroduce the invented format this item forbids — the BOM case is the
    one that matters, because without it the tool reports "column not found" on a file that visibly
    contains the column.
  - **AC8 gained the not-valid-UTF-8 case** — refused, not repaired with substitutions — and AC9
    gained the way its atomicity claim is actually checked: by inspection, that no module this item
    adds opens the data-file path for writing, with ADR-0006 clause 5 supplying the rest. An
    atomicity claim checkable only by racing the process is not decidable by observation.
  - **Three more R10 gaps were left open on purpose and written down**: a header with a duplicated
    column name, how stdout and stderr interleave, and whether the file is read once or twice. The
    test applied before leaving one is that no acceptance criterion depends on it.
  - **No scope was removed and none of the stakeholder's decisions was reopened.** The criteria
    count went from ten to eleven; nothing was weakened to make it passable.
- **Questions raised:** none — see `artifacts/refinement-qa.md` "Q7". Six questions were asked on
  this item across earlier executions and all six are answered; three answers are `[unresolved]`
  nowhere. Twelve new items are tagged `[assumed]` in the Q&A and six are tagged `[unresolved]` as
  deliberately unconstrained.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, before and after each edit
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to ready --actor refine
    --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before this execution's edits and exit
    0 after them and after the transition.
  - `definition-of-ready` → **pass**, criterion by criterion:
    **R1 pass** [auto] — frontmatter complete; `type: work-item`, `epic: EP-001`,
    `priority: medium`. `validate-workspace` exit 0.
    **R2 pass** — role ("the person keeping the group's books"), capability ("feed my bank's CSV
    export into the tool and have it create expenses"), outcome ("so that I stop retyping
    transactions I have already been charged for").
    **R3 pass** [auto] — eleven criteria, AC1 to AC11, each a checkbox.
    **R4 pass** — this is the criterion that failed at every previous execution, on AC1, AC2 and
    AC5, and it now passes for all eleven. See `criteria-are-decidable` below for the command and
    verdict of each. No criterion contains an unmeasurable adjective: the words that used to carry
    the weight — "the expected format", "reported to the user, naming the row", "indistinguishable"
    — have each been replaced by a command and an expected output. `$F`, `$G`, `$H` and `$M` are
    fully written out in the criteria, so a checker with a terminal and no context can create them.
    **R5 pass** — `## Out of scope` names eleven things, including three added when Q-006 was
    answered (no built-in bank knowledge, no remembered mapping, no refund handling), each of which
    a reader could reasonably have assumed was included.
    **R6 pass** [auto] — no open question on this item; all six are `answered`.
    **R7 pass** [auto] — no `depends-on`; WI-0001, WI-0002 and WI-0003 are `done`, and this item is
    last in the stakeholder's delivery order.
    **R8 pass** [auto] — `artifacts/refinement-qa.md` records all six questions with the
    stakeholder's answers verbatim, this pass's decision to ask nothing, twelve `[assumed]` entries
    and six `[unresolved]` ones.
    **R9 pass** — one coherent change: one subcommand, one parsing module, one new key in the data
    file. It was considered whether duplicate detection (AC7) is a second item; it is not
    separable, because the stakeholder's answer to Q-003 makes it part of what importing *means*
    here, and an import shipped without it cannot be undone in a tool with no delete.
    **R10 pass** — every combination of this item's options is now stated in a criterion, named in
    `## Out of scope`, or recorded in `## Notes` under "Left deliberately unconstrained (R10)" with
    why it is safe. Three combinations were found unstated during this pass and are now stated (see
    Decisions); six are recorded as unconstrained.
  - `criteria-are-decidable` → **pass**, all eleven. AC1: run the import against `$F` with `$M`,
    compare stdout to the two named lines, stderr empty, exit 0. AC2: `list-expenses`, compare to
    the two named lines in date order, on any day. AC3: build `$U` by hand, `diff` the
    `list-expenses` outputs and the `report` outputs — empty or not. AC4: import `$G`, compare
    stdout to two lines, stderr to one named line, exit 0. AC5: three runs — a wrong
    `--amount-column`, a zero-byte file, a header-only file — each with a named message, stream and
    exit code. AC6: an unregistered payer and an unregistered sharer, each `Unknown person: <name>`,
    exit 1, `$T` unchanged. AC7: import twice, then with `--again`, then a copy, then a modified
    copy, then a different mapping — each with a named outcome. AC8: a missing path and a
    non-UTF-8 file, message names the path, exit 1, no traceback. AC9: `cmp` against a pre-command
    copy after each refusal, plus a grep of the modules this item adds for a write to the data-file
    path. AC10: four runs each omitting one option, exit 2 each. AC11: import `$H` and its
    BOM-prefixed copy, compare stdout to the named line.
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` holds all six questions and the
    stakeholder's five answers unaltered, including the four "I'll send you a sample later" replies,
    both sentences refusing a guess, and Q-006's answer in full. What this pass decided is kept in
    its own section and tagged `[assumed]`, never merged into their words. The one thing they did
    *not* say — how a non-positive row is treated — is tagged `[assumed]` and flagged inside AC4
    itself rather than being paraphrased into agreement.
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — AC1 to AC5 and AC7 to AC10 rewritten with exact commands,
    outputs and exit codes; AC11 added; the criteria preamble now defines `$F`, `$M` and the three
    reading conventions; `## Notes` gained "Decided by this refinement pass, once the sample stopped
    mattering"; the R10 list grew from three entries to six
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — "Q7" records that nothing was asked and
    why; twelve new `[assumed]` decisions; the unconstrained list extended to six
  - the generated board, regenerated by its script
- **Status:** `draft` → `ready`
- **Result:** WI-0004 is Ready, six executions after it was created and one after the stakeholder's
  answer removed the dependency that held it. All ten Definition of Ready criteria pass with no
  override sought and none needed; eleven criteria each name a command and a verdict. The item can
  now be planned, and it is the last one between EP-001 and closure.

## 2026-08-22T09:45:00Z — plan v0.1.1 — architect

- **Item:** WI-0004
- **Trigger:** status `ready`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the eleven criteria, which are the contract this plan is
    written against, plus the six R10 gaps left deliberately unconstrained
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — twelve `[assumed]` entries and six
    `[unresolved]` ones. Those are the plan's soft ground and three of them became assumptions here
  - `tracker/items/WI-0004/history.md` — fifteen rows. **Not a re-plan:** the item reached `ready`
    from `draft` by `refine`, never from `verifying` or `in-review`, so there is no rejection record
    to read first
  - `tracker/items/WI-0004/journal.md` — seven prior executions, including the stakeholder's
    verbatim answers to Q-001 to Q-006
  - `docs/architecture/overview.md` (v4) and `docs/product/vision.md` (v11)
  - `docs/architecture/adr/` — ADR-0001 (money as whole pence), ADR-0002 (the `import-csv` name and
    the option style, clause 3), ADR-0005 (streams and exit codes, clauses 2 and 4, and its own note
    that partial imports are the case needing care), ADR-0006 (atomic write, clause 2's absent-key
    rule and clause 5), ADR-0007 (unittest, two layers), ADR-0008 (nothing outside `cli.py` prints,
    clause 3), ADR-0009 (the import writes the same record shape, clause 3). ADR-0003, ADR-0004 and
    ADR-0010 read and found not to bear on this item
  - **The code:** `expenses_tool/cli.py` (all 260 lines — the parser, `render_expense`,
    `cmd_add_expense`'s check order, `_refuse` and `_cannot_read`), `expenses_tool/store.py` (all
    195 — `load`'s strictness, `save`'s atomicity, `empty_data`), `expenses_tool/expenses.py` (all
    135 — `resolve_person`, `resolve_sharers`, `record_expense`, `today`),
    `expenses_tool/money.py` (all 48 — `parse_amount`'s grammar, which is why AC4 needed no new
    amount rule), and `tests/test_store.py` for the one assertion this item has to change
  - `tracker/project.yaml` — `commands.test` and `commands.lint` already set by WI-0001's plan
- **Decisions:**
  - **A new module, `expenses_tool/bankcsv.py`, holding everything about reading a CSV and nothing
    else** (documented — ADR-0008's layering, and the shape `money.py`/`settle.py` already set). It
    is a pure function of (bytes, mapping): it never prints, never exits, never touches the data
    file. The payoff is that AC1, AC4, AC5 and AC11 become unit tests over literal strings, with no
    filesystem and no CLI in the way.
  - **Expenses are created through `expenses.record_expense` and written by the single existing
    `store.save`** (documented — ADR-0009 clause 3, ADR-0006 clause 5). This is what makes AC3 true
    by construction rather than by care, and it makes AC9's atomicity free: the import performs no
    write of its own. It also means AC3's test is a real check — two ledgers' rendered output
    compared byte for byte — rather than a restatement of the design.
  - **File identity is the SHA-256 of the raw bytes; the data file gains an `imports` list of
    `{sha256, date}` and the path is deliberately not stored — ADR-0011 (new).** Written because
    AC7 forces a genuine choice with genuine alternatives (path plus mtime, hashing the parsed rows,
    storing a copy) and because the item explicitly handed `plan` the question of what is stored.
    Two of the four options are ruled out by criteria rather than by taste: a path cannot recognise
    a renamed copy, and hashing the parsed rows would make identity depend on the mapping, which
    AC7 forbids in as many words. The ADR records that the code is trivially reversible while the
    stored digests are not — changing the algorithm makes every past import warn as new — because
    that asymmetry is what a future `plan` needs in order to decide whether it may revisit this.
  - **No ADR for the parser's shape.** That the tool holds no bank format and takes the mapping per
    import is the *stakeholder's* decision (Q-006), already recorded in `overview.md` v4. Writing an
    ADR would misattribute it to the architect, and an ADR trail padded with non-decisions is where
    real decisions hide.
  - **Six reversible assumptions, recorded in the plan under `## Assumptions`** rather than escalated
    or buried in a step. Three fill gaps the item left unconstrained on purpose (a duplicated header
    name, a record spanning several lines, how the two streams interleave); three fill cases where
    two criteria meet and neither states the answer (the order of the checks, what happens when
    every row is skipped, and whether `empty_data()` gains the new key). Each names what reversing
    it costs, and none costs more than moving lines within one file.
  - **The order of the checks is treated as design, not as detail** — data file, people, bytes,
    decoding, header, duplicate, rows. Two of those orderings are visible to a user with two things
    wrong at once, and leaving them to `implement` would be exactly the "defer the decision that
    made the item hard" failure: people before the file because AC6 says the person check happens
    before any row is read, and columns before the duplicate check because telling someone their
    file is a duplicate, when the command they typed could never have read it, sends them to fix the
    wrong thing.
  - **`utf-8-sig` is one choice that settles two of AC11's three conventions** — the byte-order mark
    is consumed and undecodable bytes raise, which is AC8's "cannot be read". Recorded because it
    would otherwise look like an arbitrary codec name in step 2.
  - **`money.parse_amount` is reused for AC4's amount rule** (documented — WI-0002 AC5, ADR-0001).
    Its grammar has no sign and no separator, so blank, zero, negative and non-numeric amounts are
    all skipped with no new code — and, as the plan's risks say, so is `1,200.00`. That last is a
    known consequence and a future criterion, not a defect to design around now.
  - **One existing test changes and it is named**: the empty-store assertion in `tests/test_store.py`,
    because `empty_data()` gains `imports` exactly as WI-0002 added `expenses`. The plan says
    explicitly that any *other* existing test needing a change is a signal to stop and file a
    question, so that the developer cannot quietly reshape WI-0001 to WI-0003 around this item.
  - **Nothing was asked of the human.** No decision here is irreversible, and none depends on intent
    no document records — the one that did was Q-006 and it is answered.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 87 tests, OK (the project's
    `commands.test`, run on the current trunk to confirm the baseline this plan builds on is green)
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0 (`commands.lint`)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to planned --actor plan
    --reason "..."` → applied
  - `python3 .claude/agile-skills/scripts/board-gen .` → regenerated
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after; 13 documents now,
    ADR-0011 being the thirteenth.
  - `every-criterion-is-addressed` → **pass**. The plan's `## Acceptance criteria mapping` has one
    row per criterion, AC1 to AC11, with no gaps: each names the step that satisfies it and a
    *specific* named test that demonstrates it rather than "tests". The reverse check was also run —
    every step maps to at least one criterion, so nothing in the plan is unrequested: step 1 → AC7,
    AC9; step 2 → AC1, AC4, AC5, AC11; step 3 → all eleven; steps 4 and 5 are the demonstrations;
    step 6 is the project's own gates.
  - `project-commands-resolved` → **pass**. `tracker/project.yaml` already carries
    `commands.test: python3 -m unittest discover -s tests -t . -q` and
    `commands.lint: python3 -m compileall -q expenses expenses_tool tests`, set by WI-0001's plan
    under ADR-0007; both were run in this execution and both exit 0, so they are commands that work
    here rather than commands that ought to. `commands.build` stays `null`, which is honest: there
    is nothing to build.
  - `decisions-recorded` → **pass**. One decision needed an ADR and got one (ADR-0011, with four
    options, the decision, and reversibility stated in both directions). Ten decisions were answered
    from existing documents and are listed in the plan's `## Decisions and ADRs` with the ADR and
    clause each follows from. Six were made as reversible assumptions and are in `## Assumptions`
    with the cost of reversing each. One decision was explicitly *not* recorded as an ADR, with the
    reason, because it was the stakeholder's rather than the architect's.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` (new) — problem, approach, six steps naming their
    files and what is true afterwards, the eleven-row mapping table, six assumptions, the decisions
    with their sources, four risks and the out-of-scope list
  - `docs/architecture/adr/ADR-0011-imported-files-remembered-by-the-sha-256-of-their-bytes.md`
    (new, v1)
  - `docs/architecture/overview.md` — v4 → v5: `bankcsv.py` and the two new test files in the
    layout, the `imports` key and its record shape in "The data", a new "The CSV import" section
    covering the parser's contract and the order of the checks, and "What is not here yet" reduced
    to the one thing that is (the per-bank shortcut, a future item)
  - the generated board, regenerated by its script
- **Status:** `ready` → `planned`
- **Result:** WI-0004 has a plan a developer who has never seen the item can execute: three files to
  change or add, two test files to write, every message named, the order of the checks fixed, and
  every criterion mapped to a named test. One ADR was needed and written; the rest came from the
  documents or is recorded as a reversible assumption. The baseline is green at 87 tests.

## 2026-08-22T09:47:00Z — plan v0.1.1 — architect (correction to the entry above)

- **Item:** WI-0004
- **Trigger:** correcting the immediately preceding entry, which is append-only and so is corrected
  by this one rather than edited
- **Inputs read:** the `run-gate` output printed by the `ready → planned` transition, which lists
  five gates for this skill
- **Decisions:** none. This entry adds a gate result that the entry above omitted.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - `plan-is-executable-without-you` (advisory) → **pass**, and it was missing from the entry above,
    which recorded only the four hard gates. Evidence, applying the self-check honestly: reading
    `plan.md` as someone who has never seen the item, the places a developer would otherwise have to
    decide something are all decided — the module's whole public surface is written out in step 2
    (four exception classes, two tuple shapes, two function signatures), every message string is
    given verbatim in step 3 with the criterion it belongs to, the order of the checks is a numbered
    list rather than a description, and the six cases the criteria leave open are settled under
    `## Assumptions`. What the plan deliberately does **not** decide is implementation: how `read`
    loops, how the raw text of a record is recovered from `csv`, how the tests are structured
    internally. Those are the developer's. The one place a reader could still stall is the exact
    `DataFileError` reason strings for a malformed `imports` key; step 1 gives the voice
    (`"one of its imports has no sha256"`) and `store.py`'s existing reasons give the pattern, and
    no criterion quotes them, so it is left as wording rather than as a decision.
- **Artifacts:** this journal entry only; no file was changed and no status moved
- **Status:** unchanged — WI-0004 stays `planned`
- **Result:** The gate record for the plan execution is now complete at five gates. Recorded as a
  correction because a silently omitted gate is exactly what the journal format exists to prevent,
  and noticing it after the transition does not make it acceptable to leave out.

## 2026-08-22T10:15:00Z — implement v0.1.1 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next`. **Not a resumption and not a send-back:** no
  `wi/WI-0004` branch existed (`git branch -a` showed only `main` and the three closed items'
  branches), `item.md` had no `branch:` field, and the last history row was `plan`'s, not a
  rejection from `verifying` or `in-review`. Nothing existing had to be reconciled with.
- **Inputs read:**
  - `tracker/items/WI-0004/artifacts/plan.md` — the six steps, the eleven-row mapping table, the
    six assumptions and the four risks. This was executed, not re-litigated
  - `tracker/items/WI-0004/item.md` — the eleven criteria, which are the contract
  - `tracker/items/WI-0004/history.md` and `journal.md` — sixteen rows, nine executions
  - `tracker/items/WI-0004/questions/` — all six `answered`, nothing open, nothing newly answered
    since the last journal entry, so there was no propagation to re-read
  - `tracker/project.yaml` — `commands.test` and `commands.lint` both set and non-null
  - `docs/architecture/adr/ADR-0011` (file identity and the `imports` record), and ADR-0001,
    ADR-0002, ADR-0005, ADR-0006, ADR-0008, ADR-0009 as the plan cites them
  - **The code, before writing any:** `expenses_tool/cli.py` (all of it — `_refuse`,
    `_cannot_read`, `render_expense`, `cmd_add_expense`'s check order, `_build_parser`),
    `expenses_tool/store.py` (`load`'s strictness, `save`'s atomicity, `empty_data`),
    `expenses_tool/expenses.py` (`resolve_person`, `resolve_sharers`, `record_expense`, `today`),
    `expenses_tool/money.py` (`parse_amount`'s grammar), `tests/test_store.py` and
    `tests/test_cli_expenses.py` (the harness style the new CLI tests follow)
- **Decisions:** all within the plan's latitude; the three that changed anything observable are in
  `impl-report.md` under Deviations.
  - **`Row` and `Skip` are small classes, not tuples.** The plan sketched them as tuples; named
    attributes make `_row` and its tests readable and give a legible assertion failure. Behaviour
    identical.
  - **A completely blank line inside the file is skipped silently**, not reported. AC4 is about
    rows that cannot become expenses; a blank line is not a row, and reporting one for ordinary
    file structure would be noise. Recorded as a deviation because no criterion states it, and
    pinned by a test so it is a decision rather than an accident.
  - **`NoHeader` covers a whitespace-only file too**, not just a zero-byte one. AC5 names the
    zero-byte case; the alternative for a one-newline file was `Column not found`, which describes
    the same problem worse.
  - **`csv.reader` over `text.splitlines()`, with `reader.line_num` bracketing each record.** This
    is how the plan's assumption 3 was met — a record whose quoted field spans lines is reported by
    the line it starts on, and its raw text is its own source lines. Tested directly.
  - **`utf-8-sig` decoding**, as the plan specified: one codec choice that both drops a leading BOM
    (AC11) and refuses non-UTF-8 bytes (AC8).
  - **Nothing was escalated, and nothing needed to be.** No decision met the plan's own test for
    "not yours": nothing changes an interface another item depends on, nothing contradicts an ADR,
    and the three behaviours no criterion covers are each cheap to reverse and are declared in the
    report rather than buried.
  - **Two things were deliberately left alone.** The pre-existing traceback when `store.save`
    fails, which the plan's risks name and which belongs to no criterion here; and
    `money.parse_amount`'s refusal of a quoted thousands separator, which is AC4 as written. Both
    are in `## What I did not do` rather than fixed on the way past.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004` → branch created from `main`
  - `python3 -m unittest discover -s tests -t . -q` → run after each of the three steps; final run
    on the branch head **exit 0, `Ran 145 tests … OK`** (87 before this item)
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0, final run on the branch head
  - a manual end-to-end run of the criteria's own commands against a scratch data file: the import,
    `list-expenses`, a second import, and `report` — output matched AC1, AC2, AC7 and AC3 exactly
  - two mutation checks, each reverted immediately: `utf-8-sig` → `utf-8` (2 tests failed),
    `if recorded:` → `if recorded and False:` (8 tests failed); the suite is green with both
    reverted
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to verifying --actor implement
    --reason "..."` → applied
- **Gates:**
  - `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t . -q`, exit 0, 145 tests, run
    **after** the last commit on the branch head, not before it.
  - `lint-clean` → **pass**. `python3 -m compileall -q expenses expenses_tool tests`, exit 0, same
    branch head.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0.
  - `every-criterion-has-a-test` → **pass**. AC1 to AC11 each map to named tests in
    `impl-report.md`'s evidence table — 28 CLI tests over the eleven criteria, 23 parser unit tests,
    7 store tests. The self-check was applied honestly rather than assumed: two mutations were run
    to confirm the tests would fail if the behaviour were removed, and both did.
  - `commits-reference-the-item` → **pass**. `git log --oneline main..HEAD` gives three commits,
    each subject matching `conventions.commit-subject` and ending `(refs WI-0004)`:
    `9034fe0 store: remember which files have been imported`,
    `8aacb23 bankcsv: read a CSV through a mapping stated at import time`,
    `99eed3e cli: import-csv, and WI-0004's acceptance criteria end to end`.
  - Diff reviewed hunk by hunk against the plan: `git diff --stat main..HEAD` is six source files
    plus the tracker. Every hunk traces to a plan step, and no acceptance criterion in `item.md`
    was touched by this execution — the only change to `item.md` is the `branch:` field, which
    step 3 of the procedure requires.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` (new)
  - `expenses_tool/bankcsv.py` (new), `expenses_tool/store.py` and `expenses_tool/cli.py`
    (extended), `tests/test_bankcsv.py` and `tests/test_cli_import.py` (new),
    `tests/test_store.py` (7 tests added, one existing assertion updated as the plan permits)
  - branch `wi/WI-0004`, commits `9034fe0..99eed3e` (three), branched from `main`
- **Status:** `in-progress` → `verifying`
- **Result:** `./expenses import-csv` is built and every criterion has evidence. The suite is 145
  tests green and the lint command is clean on the branch head. Three deviations from the plan are
  declared, all "how not what", and three things were deliberately not done and are named. Nothing
  was escalated because nothing needed to be.

## 2026-08-22T10:45:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the eleven criteria, **read first and in full**, before the
    implementation report, so that what would settle each one was derived from the criterion rather
    than from what was built
  - `tracker/items/WI-0004/artifacts/impl-report.md` — read afterwards, and used only to check that
    nothing it declares was missed. Not one verdict in `verify-report.md` cites it
  - `tracker/items/WI-0004/artifacts/plan.md` — the six steps and the six assumptions, for the
    diff-against-the-plan read
  - `tracker/items/WI-0004/history.md` and `journal.md`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — consulted for AC4's and AC7's wording,
    both of which turned out to be unambiguous
  - **the branch:** `wi/WI-0004` at commit `909b394e9154657a04908128163513ccd890f908`, which is what
    every command below was run against
  - the diff `main..909b394` over `expenses_tool/` and `tests/`, and `expenses_tool/bankcsv.py` and
    `expenses_tool/cli.py` as source, for AC9's inspection and the scope read
- **Decisions:**
  - **No send-back and no bug item.** Every one of the eleven criteria passed on its own terms, so
    the classification question in step 7 never arose. Recorded explicitly because "no defects" is a
    finding that deserves the same scrutiny as a defect: the negative cases below are what makes it
    a conclusion rather than an absence.
  - **Nothing was judged `ambiguous`.** Two criteria were candidates while reading — AC4's
    definition of an unusable row, and AC9's atomicity clause — and both turned out to state their
    own check. AC4 enumerates its four causes exhaustively, and AC9 names the inspection to run, so
    neither needed the reading that happened to make the code pass.
  - **Two mutations survived on the first attempt and both were re-aimed rather than re-rolled.**
    The AC6 mutation patched `cmd_add_expense` because `paid_by=paid_by,` occurs there first; the
    AC9 mutation wrote byte-identical JSON, so there was nothing for `cmp` to detect. Both are
    written up in `verify-report.md` with the corrected mutation and its result. A survived mutation
    quietly retried until it passes is how this check turns into theatre, so the first attempts are
    in the record.
  - **Three unstated behaviours were found in the diff and none is a defect.** A blank line inside
    the file is skipped silently; a whitespace-only file gets "has no header line" where AC5 names
    only the zero-byte case; and `--shared-by Ana,ana` / `--shared-by ""` are refused with WI-0002
    AC8's messages. All three are declared in `impl-report.md`, all three were triggered here, and
    each is consistent with a criterion rather than beyond one. They are recorded under Defects
    found so that the next reader can see they were noticed and judged, not missed.
  - **The traceback on a failing `store.save` was deliberately not filed as a bug.** It is
    pre-existing across every command in the tool, and no criterion of any delivered item says the
    behaviour should differ — which is exactly the test step 7 sets for bug-versus-nothing. It is
    named in `## Not verified, and why` instead, so it is visible without being misrouted.
- **Questions raised:** none
- **Commands:** every one run against `909b394`, from the repository root, with scratch data files
  under `/tmp/verify4/`.
  - `git rev-parse HEAD` → `909b394e9154657a04908128163513ccd890f908`; `git branch --show-current` →
    `wi/WI-0004`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests in 14.215s`, `OK`
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - AC1/AC2: the import with `$M`, then `list-expenses`; `date +%F` → `2026-08-22`, which appears on
    neither expense
  - AC3: three `add-person` and two `add-expense` runs building `$U`, then
    `diff <(list-expenses "$T") <(list-expenses "$U")` → empty, and the same for `report` → empty
  - AC4: the three-row `$G`; then an eight-row file triggering all four causes separately; then the
    same file with `--date-format "%Y-%m-%d"`
  - AC5: `--amount-column Value`; `--date-column When --amount-column Value` together; a zero-byte
    file; a header-only file imported twice
  - AC6: `--paid-by Ben --shared-by Ben,Cass`; an import with `--shared-by` omitted followed by
    `add-person Dan` and `list-expenses`; four unknown-person combinations
  - AC7: the import repeated; `--again`; `cp` to a new name; a copy with one row appended; the same
    file with `--description-column Balance`; `--again` on a fresh ledger
  - AC8: a non-existent path; `chmod 000` on a real file; a file containing `\xff\xfe\x00`
  - AC9: `cmp` against a pre-command copy after each of six refusals;
    `grep -nE "open\(|store\.save|json\.dump|os\.replace" expenses_tool/bankcsv.py` → **no matches**;
    `grep -n "store.save" expenses_tool/cli.py` → three call sites, one per writing command
  - AC10: four runs, each omitting one mapping option
  - AC11: a row with a quoted comma and padded cells; the same file prefixed with `\xef\xbb\xbf`
  - eleven mutations, each with the matching test class and each reverted: AC1 FAILED(1), AC2
    FAILED(1), AC3 FAILED(1), AC4 FAILED(2), AC5 FAILED(1), AC6 FAILED(1) after re-aiming, AC7
    FAILED(4), AC8 FAILED(1), AC9 FAILED(3) after re-aiming, AC10 FAILED(1), AC11 FAILED(1)
  - `python3 -m unittest discover -s tests -t . -q` after the last revert → exit 0, `OK`;
    `git status --short` → clean
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to in-review --actor verify
    --reason "..."` → applied
- **Gates:**
  - `tests-pass` → **pass**. Run by this execution, not quoted from the report: exit 0, 145 tests.
  - `lint-clean` → **pass**. `compileall` exit 0.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after.
  - `every-criterion-independently-checked` → **pass**. All eleven have a row in
    `verify-report.md` naming the command *I* ran and quoting its actual output. The eleven ticks in
    `item.md` were added by this execution and each rests on one of those rows; none rests on a test
    name or on the implementation report.
  - `negative-cases-exercised` → **pass**. Thirteen error and boundary paths triggered, listed
    individually in the report: every cause of a skipped row, both empty-file shapes, a header-only
    file run twice, four unknown-person combinations, five duplicate-detection variants, three
    unreadable-file kinds, four missing options, and the three parsing conventions.
  - `no-unplanned-scope` (advisory) → **pass with three notes**. The diff is six source files and
    every hunk traces to a plan step; the three behaviours no criterion states are recorded above
    and in the report.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 909b394e9154657a04908128163513ccd890f908`
  - `tracker/items/WI-0004/item.md` — all eleven checkboxes ticked, AC1 to AC11, each on the
    evidence in that report
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0004 does what its criteria say. Eleven criteria checked by running their own
  commands against `909b394`, thirteen negative paths triggered, eleven mutations confirming the
  tests are sensitive, and no defect found. Four things are declared as not verified — the
  most-recent-import date through the CLI, atomicity under a real interruption, behaviour against
  the stakeholder's actual bank file, and a pre-existing traceback on a failed save — so that a
  clean pass is not mistaken for a complete one.

## 2026-08-22T10:47:00Z — verify v0.1.1 — qa-engineer (correction to the entry above)

- **Item:** WI-0004
- **Trigger:** correcting the immediately preceding entry, which is append-only and so is corrected
  by this one rather than edited
- **Inputs read:** the `run-gate` output printed by the `verifying → in-review` transition, which
  names this skill's six gates
- **Decisions:** none. The entry above named the wrong advisory gate and omitted the right one.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - `tests-would-fail-without-the-change` (advisory, and this skill's sixth gate) → **pass**. It was
    omitted from the entry above, which instead listed `no-unplanned-scope` — that is `implement`'s
    advisory gate, not this skill's. The diff read it records was genuinely done and its three
    findings stand; it was simply filed under a name that does not belong to `verify`.
    The evidence for the gate that *does* belong here is the eleven mutations listed under
    **Commands** in that entry and tabulated in `verify-report.md` under "Test sensitivity check":
    one mutation per criterion, each aimed at the behaviour that criterion describes, each killing
    the matching test class, each reverted, with the full suite green and `git status` clean
    afterwards. Two first attempts survived and both are recorded with why they were ineffective
    and what the corrected mutation did, rather than being retried until they passed.
- **Artifacts:** this journal entry only; no file was changed and no status moved
- **Status:** unchanged — WI-0004 stays `in-review`
- **Result:** The gate record for the verification is now complete and correctly named at six gates.
  Recorded as a correction because a gate filed under another skill's name is indistinguishable, to
  a later reader, from a gate that was never run.

## 2026-08-22T11:10:00Z — review-close v0.1.1 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (16 rows), `journal.md` (**all 16 entries, in
    full**, including the two correction entries), `artifacts/plan.md`, `artifacts/impl-report.md`,
    `artifacts/verify-report.md`, and all six questions
  - **the diff `main..8466f60`, hunk by hunk** — `expenses_tool/cli.py`, `expenses_tool/store.py`,
    `expenses_tool/bankcsv.py`, `tests/test_bankcsv.py`, `tests/test_cli_import.py`,
    `tests/test_store.py`. Read as a diff, not as the reports about it
  - `docs/architecture/adr/ADR-0011`, and ADR-0002, ADR-0005, ADR-0006, ADR-0009 — the four whose
    text makes claims about this item's behaviour, each read against the code it describes
  - `docs/architecture/overview.md` (v5), `docs/product/vision.md` (v11)
  - **`README.md`, in full** — 160 lines
  - `/tmp/verify4/data.json`, a data file produced by a real import, to check the stored shape
    against what `overview.md` v5 and ADR-0011 claim it is
- **Decisions:**
  - **Rejected, back to `in-progress`, on D7.** `README.md` was not touched by this item and now
    carries claims the change made false — the worst of them being, under `## What it does not do
    yet`, "Importing a bank CSV export is the next piece of work". The command table omits
    `import-csv` entirely. Everything else about the change is sound, which is precisely why this
    is worth a round trip rather than a note: a clean accept here would ship a README telling the
    user the delivered feature does not exist, in the item that unblocked an epic the stakeholder
    held open for six askings to get it.
  - **The root cause is the plan, not the implementation.** `plan.md` has no step for `README.md`,
    and `impl-report.md` executed the plan faithfully. Recorded in `review.md`'s verdict so that
    `implement` reads the send-back as a scope correction rather than as a criticism of its work,
    and so that a later reader can see where the omission entered. Three previous items each
    updated the README inside their implementation commit (`1dd3f09`, `aa611b6`, `a830980`), so the
    practice existed and the plan simply failed to carry it.
  - **Three inherited README defects were folded into the same send-back rather than filed as a
    bug**, with each attributed to the item that introduced it (F4 and F5 to WI-0003, F6 to
    WI-0002/WI-0003). Two reasons, both recorded in `review.md`. First, the mechanism the skill
    prescribes is unavailable: `pipeline.yaml` allows `null → ready` for actor `verify` only, and
    `scripts/transition`'s `legal()` compares the actor exactly, so `review-close` cannot create a
    bug item without `--force`; forcing a gate override to file a two-sentence prose fix is worse
    than the alternative. Second, all six defects are in one file, in three adjacent passages, all
    about the command surface and what the tool "does not do yet" — which is what this item
    completes. The widening is mine as reviewer, deliberate, and attributed so that no other item
    is credited with a fix it did not make.
  - **D12 passes for `docs/` and its scope is itself a finding.** Every claim in `docs/` about this
    item's behaviour was read against the code and is true. But D12 and DE4 are scoped to `docs/`,
    and this project's user-facing documentation is `README.md` at the repository root, which no
    Definition-of-Done criterion covers. That is how F4, F5 and F6 survived three closes with every
    machine-checkable gate green — the exact failure mode the spec's own note under D12 describes,
    reproduced here in a document the criterion cannot see.
  - **D10 was compared, not assumed.** `Verified-commit: 909b394…`; the last commit touching
    `expenses_tool/` or `tests/` is `99eed3e`, which precedes it; the two commits after it were
    inspected with `git show --stat` and touch only `tracker/`. The verification is current, and
    this rejection does not invalidate it — but the head will move when the README is fixed, so
    `verify` will run again.
  - **One maintenance observation on the code, recorded and not sent back.**
    `cmd_import_csv`'s list comprehension calls `expenses.record_expense`, which can raise
    `BlankDescription`. It cannot raise today because `bankcsv._row` already rejects blank
    descriptions; if that rule were ever relaxed, the exception would become an uncaught traceback
    where every other error path in the command is a clean refusal. No ledger is at risk, since
    nothing is written at that point.
  - **No trial merge was performed and nothing was merged.** Step 8's sequence is only reached on
    an accept. The branch is intact and `main` is untouched.
  - **The epic was not assessed.** WI-0004 is not `done`, so EP-001 is not at its last-child
    moment; DE1 fails trivially and nothing about DE3–DE6 was certified.
- **Questions raised:** none. Nothing here needs a decision that is not the reviewer's: the ADRs are
  not contradicted, and no acceptance criterion is in dispute.
- **Commands:**
  - `git rev-parse HEAD` → `8466f6065a2d69b187473b903304888c8c3e9d22`
  - `git log --oneline main..HEAD` → six commits, each `(refs WI-0004)`
  - `git show --stat 9bd9660` and `git show --stat 8466f60` → `tracker/` only, no source
  - `git log -1 --format='%H %s' -- expenses_tool tests expenses` → `99eed3e`, before the verified
    commit
  - `git log --format=%H -- README.md` → `a830980` (WI-0003), `aa611b6` (WI-0002), `1dd3f09`
    (WI-0001) — the precedent that every item updates it
  - `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` → lines
    4, 36, 65, 108, 158
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests … OK`
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - three of `verify-report.md`'s recorded commands re-run and reproduced exactly: AC5's
    `Column not found in …: Value`, AC7's `This file was already imported on 2026-08-22. …`,
    AC11's BOM import
  - `python3 -c "import json; …"` on a real imported data file → keys
    `['expenses', 'imports', 'people', 'schema']`, the import record exactly
    `{'date': '2026-08-22', 'sha256': '727db804…'}`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to in-progress --actor review-close
    --reason "..."` → applied
- **Gates:**
  - `definition-of-done` → **FAIL on D7**, and the per-criterion table is in `review.md`. D1 pass,
    D2 pass (three verdicts re-run and reproduced), D3 pass, D4 pass, D5 pass, D6 pass, **D7 fail**,
    D8 pass, D9 not reached, D10 pass, D11 pass, D12 pass for `docs/` with its scope recorded as a
    finding.
  - `verification-postdates-the-code` → **pass**. Compared: `909b394` postdates `99eed3e`, and the
    two later commits are tracker-only.
  - `commits-reference-the-item` → **pass**. `check-commit-refs` exit 0 over `main..HEAD`.
  - `tests-pass-on-the-merge-result` → **skipped, with the reason**: the item is rejected, so step
    8's trial merge was never reached. Recorded as skipped rather than passed, because no merge
    result exists to have tested. It will be run on the next pass.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after the transition.
  - `record-is-reconstructible` → **pass**. Using only the tracker, `docs/` and `git log --grep
    WI-0004`, a reader can follow: what was asked (item.md and six questions, five of them the same
    request for a CSV sample and the sixth the one that ended it), which skill decided what (16
    history rows, 17 journal entries with this one), what verification found (`verify-report.md`
    with its verified commit, thirteen negative paths and eleven mutations), and what the code does
    (six commits, all grep-able). The two self-corrections in the journal are part of why this
    passes rather than a blemish on it.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` (new) — what was examined, the twelve-row Definition
    of Done table, six README findings with each attributed, one code observation, four accepted
    gaps, and the verdict
  - no merge commit; `main` is untouched and `wi/WI-0004` is intact
  - no bug item filed — the actor table does not permit this skill to create one; recorded above
  - EP-001 unchanged and still `open`
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected on the record, not on the code. The change meets all eleven criteria and the
  verification is sound and current, but `README.md` still tells the user that importing a bank CSV
  export is the next piece of work, and does not list the command that does it. Six documentation
  defects are named with exact line numbers and attributions; three are this item's and three are
  inherited from items already closed, which is a finding about the Definition of Done's scope as
  much as about any item. No code change is required.

## 2026-08-22T11:30:00Z — implement v0.1.1 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress`, dispatched by `next`. **This is a send-back, not a fresh
  implementation.** The last history row is `in-review → in-progress` by `review-close`, so per this
  skill's step 1 the job is that defect and not the whole item.
- **Inputs read:**
  - `tracker/items/WI-0004/artifacts/review.md` — **read first**, before anything else. Six defects,
    F1 to F6, each with a line number, an attribution and a stated fix; the verdict says explicitly
    that no code change is needed and none should be made
  - `tracker/items/WI-0004/history.md` — the send-back row and its reason
  - `tracker/items/WI-0004/artifacts/impl-report.md` — this pass's own first half, so that the
    second-pass section says what actually changed rather than repeating it
  - `README.md`, all 160 lines, and specifically lines 4, 36, 65, 108 and 158 and the
    `### Commands` table
  - `git log --format=%H -- README.md` — the three earlier commits the review cites as the project's
    precedent for documenting a command in the item that ships it
  - the item's criteria were **not** re-read as a design input: none of them changed and none is in
    dispute
- **Decisions:**
  - **No code was touched, deliberately.** The review's verdict says the change itself is good and
    that no code change is required, and the diff for this pass is one file: `README.md`, +79 −11.
    The temptation on a send-back is to tidy something else while the branch is open; nothing else
    was touched, so the eleven criteria, the 145 tests and the earlier commits are all still exactly
    what `verify` checked.
  - **The new `### Importing from your bank` section sits after `### Who owes whom`**, not at the
    end. That is where the epic's own delivery order puts the import, and it means a reader meets
    the sections in the order they would use them.
  - **It says why the four options exist**, citing the stakeholder's own choice: the tool holds no
    bank's format. Without that, a reader meets four required options that every other command
    manages without and reads them as an oversight rather than as the decision that made the
    feature possible.
  - **It documents the three things a user will actually hit** — a skipped row with its line number
    and exit 0, an outright refusal when the named columns are not in the file, and the duplicate
    warning with `--again` — rather than only the happy path. The duplicate paragraph says plainly
    that `--again` really does double the expenses and that there is no way to delete one, because
    that is the consequence the stakeholder asked to be protected from in Q-003.
  - **One thing was done that the review did not ask for, and is declared** in `impl-report.md`: the
    output-and-exit-codes table gained a row for a partly-successful import. The table previously
    offered only "It worked → 0" and "Refused → 1", neither of which describes an import that
    skipped three rows and still exited 0 — the one exit-code case in this item a reader cannot
    guess. It is a one-row documentation addition in the file already being edited, and it is named
    here rather than slipped in.
  - **Every console block in the new section was executed rather than written from memory**, and
    each reproduces verbatim: the full import command, the skip example, and the duplicate warning
    with its exit 1. A README example that has never been run is a claim, and this item was rejected
    for exactly that class of untrue claim.
  - **F4, F5 and F6 were fixed although they are not this item's**, because the review authorised
    the widening explicitly and attributed each to WI-0002/WI-0003. This is not the "fixing things
    you noticed on the way" failure: it was scoped by the reviewer, in writing, before this pass
    started, and it is in the same three passages of the same file as F1 to F3.
  - **Nothing was escalated.** The send-back was specific enough to act on without a single
    judgement call about what was meant.
- **Questions raised:** none
- **Commands:**
  - `grep -n "^#\|^##\|^###" README.md` → the section list, to place the new section
  - `git log --format=%H -- README.md` → `a830980` (WI-0003), `aa611b6` (WI-0002), `1dd3f09`
    (WI-0001)
  - the three console blocks in the new section, run for real against a scratch data file under
    `/tmp/readme/`: the import printed the two `Imported …` lines exactly as documented; the
    three-row file printed `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00` and one `Imported …`
    line; the repeat import printed
    `This file was already imported on 2026-08-22. Pass --again to import it anyway` and `exit=1`
  - `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` → no
    matches except the `## What it does not do yet` heading itself
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests in 14.155s`, `OK`
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `git diff --stat` before committing → `README.md | 90 +++--`, one file
  - `git commit` → `a49b5d3 docs: README documents import-csv and no longer says it is unbuilt
    (refs WI-0004)`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to verifying --actor implement
    --reason "..."` → applied
- **Gates:**
  - `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t . -q`, exit 0, 145 tests, run
    on the branch head after the README commit. Unchanged from the first pass, as expected: no code
    moved.
  - `lint-clean` → **pass**. `compileall` exit 0 on the same head.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0.
  - `every-criterion-has-a-test` → **pass, unchanged**. No criterion, test or module was touched by
    this pass, so the evidence table in `impl-report.md` stands exactly as `verify` found it. The
    honest statement of this gate for this pass is that it was inherited intact, not re-earned.
  - `commits-reference-the-item` → **pass**. `check-commit-refs` exit 0; the new commit `a49b5d3`
    ends `(refs WI-0004)` like the six before it.
  - `no-unplanned-scope` (advisory) → **pass**. `git diff --stat` for this pass is one file. Every
    hunk traces to a numbered finding in `review.md`, except the exit-codes row, which is declared
    above and in the report.
- **Artifacts:**
  - `README.md` — the `import-csv` row in the command table, a new `### Importing from your bank`
    section, the exit-codes row for a partial import, and the five stale sentences corrected
  - `tracker/items/WI-0004/artifacts/impl-report.md` — a `## Second pass — the review's send-back
    (D7)` section appended, mapping each fix to the review's own F-labels. The first-pass content is
    left as written rather than rewritten, so both passes are legible
  - commit `a49b5d3` on `wi/WI-0004`; the branch is now `9034fe0..a49b5d3`, seven commits
- **Status:** `in-progress` → `verifying`
- **Result:** The README now documents `import-csv`, shows it working, and no longer tells the
  reader that importing a bank CSV export is the next piece of work. All six of the review's
  findings are fixed, no code was touched, and the gates are green on the new head. Verification
  will need to run again because the head moved (D10), but the eleven criteria and their evidence
  are untouched, so it is a documentation re-read rather than a repeat.

## 2026-08-22T11:50:00Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next`. **This is a re-verification after a
  send-back.** The history shows `in-review → in-progress` by `review-close` and then
  `in-progress → verifying` by `implement`, so `review.md` was read first: the rejection was D7, a
  documentation defect, and the verdict said no code change was needed.
- **Inputs read:**
  - `tracker/items/WI-0004/artifacts/review.md` — **first**, per this skill's step 1. Six findings,
    F1 to F6, with line numbers and attributions
  - `tracker/items/WI-0004/item.md` — the eleven criteria, unchanged and still my only standard
  - `tracker/items/WI-0004/artifacts/impl-report.md`, including its new
    `## Second pass — the review's send-back (D7)` section
  - the previous `verify-report.md` (at `909b394`), for what it declared unverified
  - **`README.md` in full**, and `git diff 909b394..89cce7e`
  - the branch at `89cce7e6bae6a2538d97ab13b4e1e5de70813159`
- **Decisions:**
  - **Every criterion was re-run rather than carried over.** `git diff --stat 909b394..89cce7e --
    expenses expenses_tool tests` is empty, so the code is byte-identical and carrying the eleven
    verdicts forward would have been defensible. It would also have been an inference, and this
    skill exists to run commands. All eleven were re-run end to end against the new head and all
    eleven pass; the empty diff is recorded as the reason the *result* was expected, not as the
    reason it was not checked.
  - **The README was verified the way a criterion is** — by running it. Every console block in the
    new section was executed and compared to what the file says; the command table's option list was
    checked against `./expenses import-csv --help`; and "Every command accepts `--data-file PATH`"
    was checked by grepping all six subcommands' help output. A documentation fix accepted by
    reading it approvingly is how the original defect passed three reviews.
  - **Two pre-existing README console blocks were re-checked too**, though nothing asked for it,
    because three of the six findings were sentences that went stale under items that had already
    closed. The `### Who owes whom` block reproduces exactly. The `### Recording expenses` block
    shows `2026-08-14` where a run today prints `2026-08-22`, and I judged that **not** a defect: it
    is a dated transcript of an example that omits `--date`, and the behaviour it illustrates is
    stated correctly in the bullet above it. Recorded in the report so that it is visible this was
    examined and judged rather than missed.
  - **Two of the eleven mutations were re-run, and the other nine were not.** The nine were run at
    the first verification against byte-identical code, so they apply unchanged; re-running all
    eleven would have been repetition. Re-running two — `utf-8-sig` → `utf-8`, and replacing AC7's
    warning text — keeps this pass's sensitivity claim from being a claim about a previous pass.
    Both killed their tests, both were reverted, and the nine that were not re-run are declared
    under `## Not verified, and why` rather than left to be assumed.
  - **A finding was recorded that is not a defect and not a send-back:** `grep -rn "README" tests/`
    finds one comment and nothing else. No test asserts anything about `README.md`, so the class of
    defect that caused this send-back is invisible to every automated gate the project has — which
    is why it survived three closes until a reviewer read the file. Fixing the README does not
    remove the exposure. This belongs in the record because the next person to add a command will
    hit exactly the same gap.
  - **No bug item and no send-back.** Nothing failed.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `89cce7e6bae6a2538d97ab13b4e1e5de70813159`
  - `git diff --stat 909b394..HEAD` → `README.md` and tracker files;
    `git diff --stat 909b394..HEAD -- expenses expenses_tool tests` → **no output**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests in 15.391s`, `OK`
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - AC1 to AC11 re-run end to end; the outputs are quoted in `verify-report.md`. Highlights:
    AC5's header-only file printed `No rows imported from …` on **both** runs; AC7's renamed copy
    warned and `--again` produced a 4-line listing; AC9's grep over `bankcsv.py` returned `0`;
    AC10 gave `exit2` four times out of four
  - `./expenses import-csv --help` → usage line matching the README's new table row exactly
  - `--help | grep -- --data-file` for all six subcommands → six of six
  - the README's three new console blocks, run verbatim → output identical to the file
  - the README's two pre-existing console blocks, run → `report` identical; `add-expense` differs
    only in the transcript's date, judged above
  - `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` → no
    matches outside the heading
  - `grep -rn "README" tests/` → one comment
  - two mutations, each reverted: AC11 `FAILED (failures=1)`, AC7 `FAILED (failures=4)`; then
    `git status --short` clean and the suite `OK`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to in-review --actor verify
    --reason "..."` → applied
- **Gates:**
  - `tests-pass` → **pass**. Run here on `89cce7e`: exit 0, 145 tests.
  - `lint-clean` → **pass**. `compileall` exit 0.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after.
  - `every-criterion-independently-checked` → **pass**. Eleven rows in `verify-report.md`, each
    naming a command run in *this* execution against `89cce7e`. None carried over, none citing the
    implementation report, none citing the previous verification.
  - `negative-cases-exercised` → **pass**. Fourteen error and boundary paths re-triggered, listed
    in the report.
  - `tests-would-fail-without-the-change` (advisory) → **pass on a sample, with the reasoning
    declared**. Two mutations re-run here; the other nine were run against byte-identical code at
    the first verification, and the fact that they were not re-run is written into
    `## Not verified, and why`.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` — **rewritten** for this pass, carrying
    `Verified-commit: 89cce7e6bae6a2538d97ab13b4e1e5de70813159`. The first report remains in git
    history and is what `review.md` cites; the file had to carry the current commit because a
    verification older than the code it verifies does not count
  - `tracker/items/WI-0004/item.md` — the eleven ticks stand; none was removed and none was added,
    because every criterion was re-demonstrated
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** The send-back is cleared and the item still meets all eleven criteria at `89cce7e`.
  The README now documents `import-csv`, and every claim it makes about this item was checked by
  running it, including three console blocks reproduced verbatim. One finding is recorded that no
  gate will catch: nothing in the test suite protects the README, so the defect that caused this
  round trip can recur silently.

## 2026-08-22T12:15:00Z — review-close v0.1.1 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next`. **Second review of this item**; the first
  rejected it on D7 and its findings are carried into the rewritten `review.md` rather than being
  replaced silently.
- **Inputs read:**
  - `tracker/items/WI-0004/artifacts/review.md` as it stood — my own first review, re-read so that
    this pass judges the six findings it raised rather than starting a new opinion
  - `item.md` (eleven criteria, all ticked), `history.md` (19 rows), `journal.md` (**all 21
    entries**, in full, including both self-corrections and both passes of `implement` and
    `verify`), `plan.md`, `impl-report.md` with its second-pass section, the rewritten
    `verify-report.md`, and all six questions
  - **the `README.md` diff `main..80809a2`, hunk by hunk** — nine hunks, the change this pass exists
    to judge
  - the source diff, re-read and then shown unchanged since the first review
  - ADR-0011, ADR-0002, ADR-0005, ADR-0006, ADR-0009, `overview.md` v5, `vision.md` v11
- **Decisions:**
  - **Accepted, merged, closed with `outcome: delivered`.** All twelve Definition of Done criteria
    pass, each recorded with its own evidence in `review.md`. D7 — the criterion that failed last
    time — is the one that changed: the README now documents `import-csv`, and the four stale
    sentences are gone.
  - **All six findings verified as fixed, individually**, against the diff rather than against the
    report claiming they were fixed. F1 and F3 by reading the lines; F2 by the new table row and the
    new section; F4, F5 and F6 by reading their replacements. The verifier had already run every
    console block in the new section and checked the table row against `./expenses import-csv
    --help`, and I checked *that* claim by confirming the quoted outputs come from this session's
    paths rather than being copied forward.
  - **`implement`'s one unrequested addition is accepted** — a row in the output-and-exit-codes
    table for a partly-successful import. It was declared rather than slipped in, it is one line of
    documentation in a file already being edited, and without it the table described only "It
    worked → 0" and "Refused → 1", neither of which covers an import that skipped three rows and
    exited 0.
  - **The trial merge came before the close, and the close before the merge.** `main` was copied to
    a throwaway branch, `wi/WI-0004` merged into it, and `unittest` and `compileall` run **on the
    merge result** — 145 tests, `OK`, and exit 0. The trial was then deleted unpublished, the item
    closed while the branch was still unmerged, and only then was the branch merged for real. That
    order is forced: `check-commit-refs` inspects `main..wi/WI-0004`, and merging first empties that
    range and makes the gate refuse the close it was a precondition for.
  - **Five accepted gaps were written into `item.md`'s `## Notes`**, not left in the reports. Once
    an item is `done` nobody reads its verification report again, so an accepted gap that lives only
    there stops being true without anyone noticing. The one that matters most is the last: no test
    protects `README.md`, so the defect that cost this item a round trip can recur silently.
  - **Two observations carried and not escalated.** The `BlankDescription` coupling in
    `cmd_import_csv` — unreachable today because `bankcsv._row` rejects blank descriptions first,
    and a traceback the day that rule is relaxed. And the pre-existing traceback on a failing
    `store.save`, which belongs to no criterion of any item and which I still cannot file as a bug,
    because `pipeline.yaml` permits `null → ready` for actor `verify` only.
  - **The epic is NOT closed by this execution, deliberately.** WI-0004 is EP-001's last child, so
    this is the moment step 10 describes — and applying the epic Definition of Done found DE4
    wanting. `docs/product/vision.md` v11 records the *decision* Q-006 produced but its "How it is
    used" section still describes the command surface as it stood before this item: it names
    `add-person` and `list-people`, not `import-csv`, and its rule that "every command confirms what
    it did on stdout and exits 0; a refusal goes to stderr, exits 1" does not describe a partial
    import, which writes skips to stderr and exits 0. That is not false, but DE4 asks whether
    `docs/product/` reflects **what was actually built**, and it does not yet.
    I may not fix it myself: `spec/doc-header.md` §5 gives `vision.md` to `intake`, `refine` and
    `answer-questions`, and `review-close` is not among them. So `EP-001/Q-002` is filed, addressed
    to the architect and **non-blocking**, naming the two passages and what each needs. `next` step
    3 dispatches `answer-questions` on any open architect question, so the loop continues without a
    human and the epic closes on the pass after. Closing the epic today and noting the gap was
    available and I declined it: I rejected this very item once for documentation that did not match
    what shipped, and certifying DE4 over the same class of gap one transition later would make the
    criterion mean nothing.
- **Questions raised:** `EP-001/Q-002` — non-blocking, addressed to `architect`. Asks for
  `vision.md` to describe the delivered import command and the partial-import exception to its
  output rule. Non-blocking because nothing is waiting on it: WI-0004 is `done` and merged, and the
  only thing it gates is the epic's own closure.
- **Commands:**
  - `git rev-parse HEAD` → `80809a2e57598d3f11a4bcd12c05322f8a79c554`
  - `git log --oneline 89cce7e..HEAD` → one commit, tracker-only by `git diff --stat`
  - `git log -1 --format='%h %s' -- expenses expenses_tool tests README.md` → `a49b5d3`, before the
    verified commit
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004 --root .` →
    `all 10 commit(s) on main..wi/WI-0004 name WI-0004`, exit 0
  - `git checkout -b trial-merge main && git merge --no-ff --no-edit wi/WI-0004` → merged;
    `python3 -m unittest discover -s tests -t . -q` → `Ran 145 tests in 14.544s`, `OK`;
    `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `git checkout wi/WI-0004 && git branch -D trial-merge` → `Deleted branch trial-merge (was
    560bfe9)`; `git branch` confirms nothing left behind
  - `git diff main..HEAD -- README.md` → nine hunks, read individually
  - `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` → no
    matches outside the `## What it does not do yet` heading
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0004 --to done --actor review-close
    --reason "..."` → applied, then `git checkout main && git merge --no-ff wi/WI-0004`
- **Gates:**
  - `definition-of-done` → **pass**, criterion by criterion, with the twelve-row table in
    `review.md` as the evidence. D1 pass, D2 pass, D3 pass (run on the branch head **and** on the
    merge result), D4 pass, D5 pass, D6 pass, **D7 pass — the criterion that failed last time**,
    D8 pass, D9 pass, D10 pass, D11 pass, D12 pass with its scope finding restated.
  - `verification-postdates-the-code` → **pass**. `Verified-commit: 89cce7e…`; the last commit
    touching source or the README is `a49b5d3`, which precedes it; the single commit after it
    touches only `tracker/`. Compared, not assumed — and this is the criterion the rejection moved,
    so it was the first thing checked.
  - `commits-reference-the-item` → **pass**. `check-commit-refs` exit 0 over all ten commits, run
    while the branch was still unmerged.
  - `tests-pass-on-the-merge-result` → **pass**, and this time it was actually reached: 145 tests
    `OK` and `compileall` exit 0 on a real merge of `wi/WI-0004` into a copy of `main`, before
    anything was published. Last pass this gate was recorded `skipped` because the rejection never
    reached step 8.
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 before and after.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0004`
    alone a reader can answer all four questions: what was built and why (the item, and six
    questions of which five were the same request for a CSV sample and the sixth the one that ended
    the wait); which skill decided what (19 history rows, 22 journal entries); what questions arose
    and how they were resolved (six, all `answered`, each with `## Consequences` naming real files);
    and what verification found (two reports, each with its own verified commit, thirteen and
    fourteen negative paths, eleven and two mutations). The two self-corrections and the rejection
    are part of why this passes rather than blemishes on it — a record that shows only successes is
    a record that has been tidied.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — rewritten for this pass, carrying the first
    review's six findings and their disposition rather than replacing them
  - `tracker/items/WI-0004/item.md` — `status: done`, `outcome: delivered`, and a new
    `### Accepted at closure, and still open (review-close)` section carrying the five gaps
  - `tracker/items/EP-001/questions/Q-002.md` (new) — non-blocking, to the architect, for DE4
  - the merge of `wi/WI-0004` into `main`; the branch is left intact
  - EP-001 **not** closed; the reason is under Decisions and repeated on the epic's journal
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** WI-0004 is delivered, merged and closed. `./expenses import-csv` reads a CSV through
  columns the user names at import time, records one ordinary expense per row, reports what it
  skipped, refuses a file it cannot read and warns before importing the same file twice — and the
  README now says so. The epic stays open one more pass: `vision.md` still describes the command
  surface as it was before this item, and fixing that belongs to `answer-questions`, which
  `EP-001/Q-002` now asks.
