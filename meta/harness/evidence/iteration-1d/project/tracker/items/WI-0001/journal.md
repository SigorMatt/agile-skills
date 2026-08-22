# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-22T01:37:56Z — intake v0.2.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this skill is not dispatched by `next`
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty at the start of this execution, so `EP-001` and `WI-0001` were the first IDs allocated
  - `docs/product/vision.md` — did not exist; created by this execution
- **Decisions:**
  - See `EP-001`'s entry for how the work was split and why this item is one of three; that reasoning belongs to the split, not to this item.
  - Dependency for this item: none — this is the first item; the other two depend on it.
  - Acceptance criteria here are deliberately incomplete and are marked so in `## Notes`. They state observable behaviour where the stakeholder's words settle it, and stop where they do not. Padding them into something that looks finished would hand `refine` a polished guess instead of an honest gap.
  - No command names, file formats or data structures appear in the story or the criteria, because the stakeholder named none. "A command" is used on purpose.
- **Questions raised:** none on this item; `EP-001/Q-002` and `EP-001/Q-003` constrain it and are listed in its Notes
- **Commands:**
  - `scripts/new-item --id WI-0001 --type work-item --epic EP-001 ...` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported at the end of this intake — see `EP-001`'s entry for the run)
  - `epic-has-success-measures` → **pass** (assessed on `EP-001`; four measures, each checkable by running the tool — see that item's entry)
  - `items-are-separable` (advisory) → **pass** — WI-0001's dependency is stated above and it delivers something observable on its own: record people and shared expenses that survive between runs
  - `no-solution-in-the-problem` (advisory) → **pass** — the story and criteria name no technology the stakeholder did not. Python and CSV appear only where they were stated; nothing was removed.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/journal.md`, `tracker/items/WI-0001/history.md` (new, headers written by `new-item`)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` as one of three items under `EP-001`. It is not Ready: `refine` must close the gaps listed in its `## Notes`.

## 2026-08-22T01:51:35Z — refine v0.1.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority `critical`, no `depends-on`, no open question at dispatch time)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eight acceptance criteria, including AC7 and AC8 added by `answer-questions` earlier today
  - `tracker/items/WI-0001/history.md` — one row, `— → draft` by `intake`. **This is a fresh draft, not a send-back**, so the whole item is in scope rather than one named defect
  - `tracker/items/WI-0001/journal.md` — `intake`'s entry, which records that the criteria are deliberately incomplete and names the gaps
  - `tracker/items/WI-0001/artifacts/` — empty; no prior refinement to build on
  - `docs/product/vision.md` (v2) — nothing in the batch contradicts it
  - `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` (v1) — AC7 and AC8 follow it, so they were not reopened
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — to check no sibling already owns part of this scope, and to see which of this item's gaps also constrain them
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's answers, which changed what this item needs to ask
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Precondition 2 failed and the skill stopped there.** `refine` requires the human to be present; they are asynchronous and not in this session. The procedure's own instruction for that case is to file a question addressed to `human`, suspend with `resume-to: draft`, and stop. No acceptance criterion was rewritten. This matters: the failure mode this skill warns about is writing a criterion on a vague answer, and writing one on *no* answer is the same failure with less excuse.
  - **The Definition of Ready was assessed in full before anything was filed**, so the batch is an agenda rather than an interrogation. Result recorded criterion by criterion under Gates.
  - **Five questions, each tied to a failing criterion.** `Q-001` equal vs uneven splits (R4, AC3); `Q-002` amount format and rounding remainder (R4 AC3, R10); `Q-003` whether an expense carries a date (R4, R10); `Q-004` fixed data file or pointable (R4 AC6, R10); `Q-005` whether `ana` is `Ana` (R4, AC1 and AC3). Each carries real options and a recommendation, so a one-word confirmation is a usable answer — the stakeholder's attention is the scarce resource and a question that makes them do the analysis wastes it.
  - **`Q-003` exists because `EP-001/Q-002` did not settle it.** The date question was parked at intake expecting the CSV sample to force it; the stakeholder deferred that question, while `EP-001/Q-001` confirmed the import ships regardless. So the question is live, cannot wait for the sample, and had to be asked directly rather than inferred from a file nobody has seen.
  - **Four things were deliberately not asked**, recorded in `refinement-qa.md` so the next execution does not re-derive them: command names and invocation shape (design, `plan` owns it); the storage format and exact path (the architect's, which is why `Q-004` asks only whether the *location* is the stakeholder's to choose); the currency (already an assumption recorded on `EP-001`); and anything belonging to WI-0002 or WI-0003, neither of which is runnable, so neither has been reached. `Q-001` and `Q-002` do constrain WI-0002's arithmetic; that is noted inside those files rather than duplicated as questions on an item nobody is working on.
  - **`artifacts/refinement-qa.md` was created with no answers in it**, opening with a banner saying it is not yet a refinement record and that the next execution must rewrite it verbatim before the item may go `ready`. Written rather than deferred because the next turn is a fresh session with none of this context, and the agenda plus the reasoning about what was excluded is exactly what would otherwise be lost. The risk it carries — that R8 is an `[auto]` check and a file that merely exists could read as satisfying it — is why the banner is the first thing in the file.
  - **`item.md`'s acceptance criteria were left untouched.** A `### Definition of Ready` section was appended to `## Notes` recording which criteria fail, on which ACs, and that nothing was rewritten on a guess.
- **Questions raised:** five, all `blocking: true`, all `addressed-to: human` — `Q-001`, `Q-002`, `Q-003`, `Q-004`, `Q-005`. All five are `[unresolved]`; none has an answer. Index in `artifacts/refinement-qa.md`.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning (`project.commands.test-null`, `plan`'s to clear) — run before filing
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 before filing; re-run by the transition below)
  - `definition-of-ready` → **fail**, which is why this item is not going to `ready`. Criterion by criterion: **R1 pass** — frontmatter complete, `type`, `epic` and `priority` all set. **R2 pass** — the story names the role (someone who pays on behalf of the group), the capability (record people and each expense) and the outcome ("so that the group has one record … still there the next time"). **R3 pass** — AC1–AC8, labelled, checkboxes. **R4 fail** — AC1 does not say whether `ana` duplicates `Ana` (→ `Q-005`); AC3 says "an amount" with no accepted format, no rejection rule, and no split proportion (→ `Q-001`, `Q-002`); AC6 asserts persistence without saying whether the location is the stakeholder's to choose (→ `Q-004`). **R5 pass** — four out-of-scope entries, including editing and deleting, which a reader would reasonably assume is included. **R6 fail as of this execution** — the five questions just filed are blocking; they were not open when `next` dispatched. **R7 pass** — `depends-on` is empty. **R8 fail** — `refinement-qa.md` exists but holds no answers, by design. **R9 pass** — eight criteria over one store and one set of recording commands is one coherent change; repayments were folded in here by `ADR-0001` and share the same storage, so splitting them out would split one file's design across two items. **R10 fail** — the combinations are unstated: an expense recorded with no sharers when no people exist yet (AC4 × AC1), an amount that does not divide evenly (→ `Q-002`), a repayment larger than any debt (AC7 × WI-0002 AC5), and whether an expense has a date at all (→ `Q-003`).
  - `criteria-are-decidable` → **fail** — the gate this execution exists to stop on. AC2, AC4, AC5, AC7 and AC8 each name an observable command and verdict. AC1, AC3 and AC6 do not, per R4 above. Passing the item with three criteria a `verify` run could not settle is precisely the failure this gate prevents.
  - `qa-recorded-verbatim` → **fail, and correctly so** — there is no exchange to record. `refinement-qa.md` states that plainly rather than presenting my recommendations as agreed answers. Recorded as a failure and not as "skipped": the file exists, and calling it skipped would understate what a later reader has to fix.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` — created, all open, all to the human
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — created, incomplete by design, banner at the top
  - `tracker/items/WI-0001/item.md` — `## Notes` gained the Definition of Ready assessment; acceptance criteria unchanged
- **Result:** WI-0001 is not Ready and was not made to look Ready. Five questions are open to the stakeholder, each tied to a named Definition of Ready criterion and each carrying options and a recommendation so it can be answered in a word. The item is suspended at `awaiting-answer`, returning to `draft` when they are answered.
- **Status:** `draft` → `awaiting-answer`

## 2026-08-22T01:59:50Z — answer-questions v0.1.4 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`; the stakeholder filled in `## Answer` on all five open
  human-addressed questions between turns, which is the case `spec/question.md` §3 gives this
  skill exclusive rights to consume
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` (all five, with their options and the
    stakeholder's answers)
  - `tracker/items/WI-0001/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (already answered; `Q-002`'s
    deferral is why `Q-003` on this item had to be asked at all)
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md`
  - `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` (v1)
  - `docs/product/vision.md` (v2, before this execution bumped it)
  - no `artifacts/plan.md` exists — this item has never been planned
- **Decisions:**
  - `Q-001` — **from the stakeholder.** "Equal split's fine for now" is option A. Recorded as a
    new AC5 stating that no per-person share is entered or stored, so the criterion is decidable
    by someone with a terminal, and as an explicit `## Out of scope` entry plus a vision boundary
    rather than a silence — a future reader wanting uneven splits should find the decision.
  - `Q-002` — **half from the stakeholder, half decided.** "No symbols or commas" is option A on
    format. "Not sure yet, go ahead anyway" is a delegation, not a deferral, so it was **not**
    re-escalated: `spec/question.md` §4 lists four conditions and none applies — intent was stated
    (proceed), the rule is reversible because the store holds totals and sharers rather than
    per-person shares, and it contradicts nothing recorded. Decided as the architect: the payer
    absorbs the remainder, recorded with both option sets and the reversibility argument in
    `ADR-0002`. Chosen over spreading cents alphabetically because the amount someone owes should
    not depend on their name, and over refusing indivisible amounts because that refuses a real
    €10 split three ways.
  - `Q-003` — **from the stakeholder.** A date on every expense, defaulting to today, malformed
    dates refused (option A). Extended, as the architect, to repayments as well: `ADR-0001`
    deliberately settled both record kinds before any data exists so the second is not
    retrofitted, and adding a date to repayments after the store holds real money is a migration.
    The stakeholder was asked about expenses and answered about expenses, so this extension is
    flagged as the architect's in `item.md` and tagged `[assumed]` in the refinement Q&A for
    `refine` to put back to them.
  - `Q-004` — **from the stakeholder.** A default location, overridable per run (option B). The
    default path and the override mechanism were deliberately left to `plan`: the question itself
    said it was not asking that, and writing a flag name into a criterion now would be design
    dressed as analysis.
  - `Q-005` — **from the stakeholder.** Trimmed, case-ignoring matching; display as first typed
    (option A).
  - Criteria were amended rather than appended-to, which is permitted because this item is at
    `draft` and its criteria are not frozen. Renumbering was unavoidable — five new criteria sit
    among the old ones — so `item.md` carries a was/now table so that a reader following an older
    reference is not stranded.
  - Deliberately **not** done: no assessment of the Definition of Ready. R4 and R10 are `refine`'s
    to judge, and judging them on criteria this execution wrote would be marking its own work.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1, 2 errors — `board.stale` and
    `question.awaiting.none-open`. Both are artefacts of the moment: the item was still at
    `awaiting-answer` with every question just marked answered, and the board still described the
    pre-answer state. The transition below cures the second, `board-gen` the first.
  - `.claude/agile-skills/scripts/transition WI-0001 --to draft ... --dry-run` → exit 0;
    `workspace-valid` passed under `--resolving 'WI-0001:awaiting-answer->draft'`
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was opened
    and checked: `WI-0001/item.md` (AC1 matching rule, AC5 equal split, AC6 amount format, AC7
    date, AC9 data location, AC11/AC12 repayment date and amount, `## Out of scope`, `## Notes`
    amendment table); `docs/architecture/adr/ADR-0002-amount-format-and-rounding.md` (created);
    `docs/product/vision.md` (v3, two boundaries added); `WI-0002/item.md` (rounding note narrowed,
    "Settled inputs" added); `WI-0003/item.md` ("Settled inputs" added);
    `WI-0001/artifacts/refinement-qa.md` (five verbatim answers, tagged).
  - `answered-from-the-record` → **pass**. Four of the five answers cite the stakeholder's own
    words in the question file, quoted verbatim in `refinement-qa.md`. The fifth — `Q-002`'s
    remainder rule — is the case where the record was silent and the stakeholder handed the
    decision over, so it is recorded as `ADR-0002` and cited from the question, exactly as the
    gate requires.
  - `escalation-is-justified` → **skipped**: no question was re-addressed to the human by this
    execution. The one candidate, `Q-002`'s remainder rule, was tested against all four conditions
    in `spec/question.md` §4 and met none; re-escalating would have cost a whole round trip to ask
    something the stakeholder had already declined to decide.
  - `workspace-valid` → **pass** (`validate-workspace --resolving 'WI-0001:awaiting-answer->draft'`
    → exit 0, run by the transition's own gate check). The unresolved run above fails only on the
    two conditions this transition and the following `board-gen` remove.
  - `item-resumed-correctly` → **pass**. `history.md` row 2 suspended the item with
    `resume-to: draft`; this execution moves it to `draft`. Not inferred from which skill asked —
    read off the row.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` — each `status: answered`,
    `answered-by: human`, `answered-at: 2026-08-22T01:55:49Z`, with `## Consequences` naming files
  - `tracker/items/WI-0001/item.md` — 8 criteria became 12; `## Out of scope` and `## Notes`
    rewritten; the amendment recorded with a was/now table
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — rewritten: the five answers verbatim,
    tagged `[human]` / `[recorded]` / `[assumed]` / `[unresolved]`, replacing the "no answer has
    been received" banner
  - `docs/architecture/adr/ADR-0002-amount-format-and-rounding.md` — created (v1)
  - `docs/product/vision.md` — v2 → v3
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — `## Notes` gain the settled
    inputs that reach them
- **Result:** All five of WI-0001's blocking questions are answered and propagated; the item
  returns to `draft` for `refine` to re-assess the Definition of Ready against the amended
  criteria. One new decision was made rather than escalated — who absorbs the rounding remainder,
  `ADR-0002` — because the stakeholder explicitly delegated it.
- **Status:** `awaiting-answer` → `draft`

## 2026-08-22T02:04:47Z — refine v0.1.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` as the only runnable item (priority
  `critical`, empty `depends-on`, no open question after `answer-questions` closed all five)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the twelve criteria as `answer-questions` left them
  - `tracker/items/WI-0001/history.md` — three rows. Row 2 suspended this item for the question
    batch and row 3 resumed it, so this is **the same refinement continuing**, not a send-back
    from `verifying` or `in-review`. The whole item is in scope because it has never been Ready
  - `tracker/items/WI-0001/journal.md` — `intake`'s entry (the gaps it left deliberately), the
    previous `refine` entry (the agenda, and what it decided not to ask), and
    `answer-questions`' entry (what the stakeholder settled and what the architect decided)
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` — the stakeholder's answers verbatim
  - `tracker/items/WI-0001/artifacts/refinement-qa.md`
  - `docs/product/vision.md` (v3) — checked against the rewritten criteria; nothing contradicts
    it, and two of its boundaries (equal splits, the per-run data file) came from this batch
  - `docs/architecture/adr/ADR-0001-repayments-are-their-own-record.md` (v1),
    `docs/architecture/adr/ADR-0002-amount-format-and-rounding.md` (v1)
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — to check no sibling owns
    part of this scope, and to keep AC5 and AC12 aligned with what they expect to consume
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **The criteria were rewritten a second time, keeping the numbering.** AC1–AC12 mean what the
    `answer-questions` amendment made them mean; what changed is that each now names what would
    be observed and what a refusal looks like. The was/now table in `## Notes` is therefore still
    accurate and was not rewritten.
  - **"Refused" was defined once, above the list, as three things together** — a message on
    stderr, a non-zero exit code, and no change to the recorded data. Nine criteria use the word;
    defining it in each would have been nine chances to define it differently, and the "no change
    to the recorded data" half is the part an implementation actually gets wrong.
  - **AC5 was moved off a negative and onto an observation.** It previously said no command
    accepts a per-person share, which `verify` cannot check without inventing a syntax to try. It
    now says what the *data* holds after a stated recording — one amount and three sharers — plus
    what the command's usage output shows. That also gives `plan` the storage constraint that
    `ADR-0002`'s reversibility argument depends on.
  - **Error cases were written in, not left implied**: unknown names, duplicate sharers, empty
    names and descriptions, malformed dates, eleven specific rejected amount strings, an
    unwritable data location. These are where implementations diverge from intent and they cost
    nothing to state now — `verify` cannot ask anyone what `12.` should do.
  - **Nine decisions were taken without asking the stakeholder**, listed in `## Notes` and tagged
    `[assumed]` in `refinement-qa.md` round 2, each with why it was not worth a round trip. All
    nine are presentation or input syntax; all are reversible until `implement` writes a store;
    all follow the stakeholder's own standing instructions on this item ("whatever's easiest to
    type", "just use a sensible default"). The line drawn: anything changing *what the tool
    records or what it is for* would have been a question, and nothing here does.
  - **The one assumption that could genuinely be rejected is flagged as such** — that a repayment
    carries a date (AC11, AC12). `answer-questions` extended `Q-003`'s expense-only answer to
    repayments and explicitly flagged it for this skill to put back to the stakeholder. It was
    not put back: `ADR-0001` settled both record kinds before any data exists precisely to avoid
    retrofitting the second, the change is free until `implement` runs, and stopping the pipeline
    for a round trip on it would cost more than reversing it later. Recorded in two places so
    that the choice is visible rather than absorbed.
  - **R10 was answered with a table rather than a claim.** Thirteen combinations of this item's
    behaviours are enumerated in `## Notes`, each pointing at the criterion that settles it or at
    the item that owns it. Two of the four gaps the previous execution named are now closed here
    (the rounding remainder, the date); one cannot arise (an expense with no sharers when nobody
    is recorded — AC3 refuses it first); one belongs to WI-0002 (a repayment larger than the debt).
  - **`## Out of scope` grew from four entries to seven.** Added: that there is no undo, that the
    listings are the only output, and that there is no migration of an older data file. The first
    is the one a reader would most reasonably assume is included, and it is the reason AC1's
    duplicate rule and AC3's duplicate-sharer rule matter — a mistake cannot be taken back.
  - **Not split.** Twelve criteria is large for one item, but they are one store and one set of
    recording commands; `ADR-0001` put repayments here deliberately so that both record kinds are
    designed before any file exists. Splitting them would split one file's design across two
    items, which is the failure `ADR-0001` was written to avoid.
- **Questions raised:** none. Round 1's five are all answered (`Q-001`–`Q-005`, `answered-by:
  human`); round 2's nine `[assumed]` entries were decided rather than asked, with the reasoning
  in `artifacts/refinement-qa.md`. Nothing is left `[unresolved]` except the stakeholder's own
  deferral on who absorbs the odd cent, which `ADR-0002` decided under their explicit permission.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning
    (`project.commands.test-null`, which is `plan`'s to clear)
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0; re-run by the transition)
  - `definition-of-ready` → **pass**, criterion by criterion, no override.
    **R1 pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: critical`;
    `validate-workspace` exit 0.
    **R2 pass** — role: someone who pays on behalf of the friend group; capability: record the
    people and each expense; outcome: "so that the group has one record of shared spending that
    is still there the next time I open the tool".
    **R3 pass** — AC1–AC12, each labelled and a checkbox.
    **R4 pass** — every criterion names an observation. The three that failed last time now pass:
    AC1 states the matching rule with worked examples (`ana`, ` Ana `, `ANA` vs `Ana`); AC3 and
    AC6 state the amount form and eleven rejected strings; AC9 and AC10 state persistence against
    a named location rather than in the abstract. No criterion contains an unmeasurable adjective
    — checked by reading for "appropriate", "reasonable", "clean", "properly", "fast", "simple":
    none appears.
    **R5 pass** — seven out-of-scope entries. At least three are things a reader would reasonably
    assume included: editing or deleting a record, filtering the listings, and computing who owes
    whom.
    **R6 pass** — no open question on this item; all five are `status: answered`.
    **R7 pass** — `depends-on` is absent; nothing blocks this item, and WI-0002 and WI-0003
    depend on it rather than the reverse.
    **R8 pass** — `artifacts/refinement-qa.md` holds round 1 verbatim, tagged `[human]` on five
    answers, and round 2's nine `[assumed]` entries, each stating it was not put to the
    stakeholder. Nothing was paraphrased into agreement; `Q-002`'s hesitation ("not sure yet") is
    quoted as hesitation and carried as `[unresolved]`.
    **R9 pass** — one coherent change; see the "not split" decision above.
    **R10 pass** — the thirteen-row combination table in `## Notes`. Each row resolves to a
    criterion, to `## Out of scope`, or to the sibling item that owns it; none is left to be
    discovered by an implementer.
  - `criteria-are-decidable` → **pass**. Observation named for each: **AC1** add `Ana`, then add
    `ana` → exit non-zero, stderr names the duplicate, AC2's listing still shows one person.
    **AC2** run the listing with nothing recorded → exit 0 with a "none" line; add two people in a
    known order → two lines, that order, original spellings. **AC3** record an expense naming an
    unrecorded sharer → non-zero, nothing stored; repeat a sharer → non-zero; empty description →
    non-zero; payer not among sharers → exit 0. **AC4** record two people, record an expense with
    no sharers, add a third person, list → the expense names exactly the first two. **AC5** record
    60 shared by three, read the file at the location given → one amount `60` and three sharer
    names, no per-person amounts; the command's usage output lists no share option. **AC6** run
    each of the eleven rejected strings → non-zero each; `12`, `12.5`, `12.50` → exit 0, and the
    last two produce the same stored amount. **AC7** omit the date → today's local date is stored;
    pass `2026-02-30` → non-zero. **AC8** record two expenses → both listed in order with date,
    payer, amount, description, sharers. **AC9** record under a temporary location, then run with
    no location → the temporary data is absent; run again with that location → present; point at a
    path in a non-existent directory → refused; at a read-only path → refused. **AC10** record,
    let the process exit, run the three listings in a new process against the same location →
    identical content and order. **AC11** repay from an unrecorded name → non-zero; repay to
    oneself under a different capitalisation → non-zero; repay between two people with no shared
    expense → exit 0. **AC12** record one expense and one repayment → each appears in its own
    listing and in neither of the other's.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` quotes all five stakeholder
    answers exactly as written in the question files, including the parts that settle nothing.
    Round 2 is tagged `[assumed]` throughout and its banner states plainly that nothing there was
    confirmed by the stakeholder.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — criteria rewritten (numbering unchanged), `## Out of scope`
    grown to seven entries, `## Notes` gains the passing DoR assessment, the nine-row assumption
    table and the thirteen-row R10 combination table
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — round 2 added; the banner now records
    that the item passed without an override, and that the stakeholder has never been in session
  - `tracker/board.md` — regenerated
- **Result:** WI-0001 is Ready. Twelve criteria, each with a named observation; nine assumptions
  recorded as `refine`'s own rather than the stakeholder's; no Definition of Ready override. The
  one assumption a stakeholder might reject — that repayments carry a date — is flagged in both
  `## Notes` and the Q&A, and is free to reverse until `implement` writes a store.
- **Status:** `draft` → `ready`

## 2026-08-22T02:12:01Z — plan v0.2.0 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` as the only runnable item (priority
  `critical`, no `depends-on`, no open questions)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — twelve criteria, the seven-entry `## Out of scope`, the
    nine-row assumption table and the thirteen-row R10 combination table
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — round 1's five `[human]` answers and
    round 2's nine `[assumed]` entries. The `[assumed]` ones are this design's soft ground and
    are treated as such: the date format, the listing order and the empty-listing behaviour all
    come from there, not from the stakeholder
  - `tracker/items/WI-0001/history.md` — four rows, no rejection. This is a first plan, not a
    re-plan
  - `tracker/items/WI-0001/journal.md` — `intake`, `refine`, `answer-questions`, `refine`
  - `docs/architecture/adr/ADR-0001` (v1) and `ADR-0002` (v1) — both followed, neither reopened
  - `docs/product/vision.md` (v3), `tracker/items/EP-001/item.md`
  - `tracker/items/WI-0002/item.md`, `tracker/items/WI-0003/item.md` — to keep the storage shape
    usable by the report and the importer that will consume it
  - `tracker/project.yaml`, `IDEA.md`, `.gitignore`
  - `docs/architecture/overview.md` — **did not exist**; this is the first planned item, so this
    execution created it
  - **The code:** there is none. `find . -name "*.py"` outside `.claude/` and `.git/` returned
    nothing, so this is a greenfield package rather than a change to existing code
- **Decisions:**
  - **Storage — one JSON document per ledger, at an XDG default, chosen per run
    (`ADR-0003`).** Route: decided. SQLite was the alternative worth naming and was rejected
    because AC5 requires `verify` to read the stored form and check that no per-person amount is
    there; JSON makes that a file read, SQL makes it a tool. Writes go through a temporary file
    and `os.replace`, so a crash cannot truncate a ledger.
  - **Money — integer minor units everywhere (`ADR-0004`).** Route: decided. `float` cannot make
    WI-0002 AC2's balance property exactly true; `Decimal` can but adds a type and still needs the
    same normalisation. `divmod` gives `ADR-0002`'s floor-and-remainder in one operation, so the
    remainder rule becomes one line rather than an argument about rounding modes.
  - **Standard library only (`ADR-0005`).** Route: decided, from constraints already recorded —
    "no external services" in the idea, "nothing signed up for" in the vision. Checked rather than
    assumed what is installed: Python 3.12.3, no `pytest`, no `ruff`, no `pyflakes`, no `flake8`.
  - **`commands.test` = `python3 -m unittest discover -s tests -t . -q`.** Run in this project
    before being recorded. It exits **5** on an empty suite and **0** with one test present, which
    means the `tests-pass` gate cannot report a pass over zero tests — worth having, and the
    reason the plan attaches tests to each step rather than to a final one.
  - **`commands.lint` = `python3 -m compileall -q expenses tests`, recorded as a syntax check and
    not a linter.** Route: decided under protest, and the protest is written into `ADR-0005`,
    `tracker/project.yaml`'s comments and the plan's `## Risks`. No linter is installed and the
    project takes no third-party dependencies; a syntax check that runs beats a style check that
    does not exist, but a green `no-lint-errors` gate here means "every file parses" and nothing
    more. Leaving it `null` was the alternative — honest, but it discards a real check that costs
    nothing.
  - **Validation lives in `model.py`, not in `cli.py`.** This is the design's one real idea. It
    costs nothing now and is what stops WI-0003's importer from accepting an amount or a date the
    hand-entry command refuses — the drift `ADR-0002` explicitly worried about becomes impossible
    rather than merely discouraged.
  - **`parse_date` checks `^\d{4}-\d{2}-\d{2}$` before `date.fromisoformat`.** Not redundant:
    `fromisoformat` accepts `20260822`, which AC7's "written `YYYY-MM-DD`" does not. Verified by
    running it rather than by remembering what 3.11 changed. It correctly refuses all five strings
    AC7 names.
  - **Six assumptions recorded rather than escalated**, each with what reversing costs: the
    `python3 -m expenses` invocation, exit 2 for refusals and 1 for a ledger that cannot be read,
    a repeatable `--shared-by`, the empty-listing line on stdout with exit 0, a malformed ledger
    raising rather than silently reading as empty, and sharer names stored in display form. The
    fifth is the one that matters — treating a corrupt file as empty would let the tool overwrite
    real data with nothing. The sixth is the only one that stops being cheap once data exists, and
    it says so.
  - **Nothing was asked of the human.** No decision here is irreversible before `implement` runs,
    and none depends on intent no document records — the five that did were asked by `refine` and
    answered. Escalating any of these would have been using the stakeholder as a design service.
  - **`plan` created two empty `__init__.py` files** (`expenses/`, `tests/`) so that
    `commands.test` and `commands.lint` could actually be run before being written into
    `project.yaml`, as this skill's self-check requires. That is the only thing this execution
    wrote outside `tracker/` and `docs/`, it contains no behaviour, and it is recorded in the
    plan's `## Risks` so a later execution that finds them missing knows why the commands broke.
  - **Deliberately not designed:** the who-owes-whom arithmetic (WI-0002 owns it, though
    `ADR-0004` states the remainder rule in integer terms so that item does not re-derive it), the
    CSV shape (WI-0003, still waiting on the stakeholder's sample), and any packaging. Applying
    this skill's own test — delete any step no AC maps to — removed nothing, because no step was
    written that no criterion asked for.
- **Questions raised:** none
- **Commands:**
  - `python3 -V` → exit 0, `Python 3.12.3`
  - `python3 -c "import pytest"` → `ModuleNotFoundError`; `python3 -m ruff --version`,
    `python3 -m pyflakes --version` → no such module
  - `python3 -m unittest discover -s tests -t . -q` → exit 5 ("NO TESTS RAN") on an empty suite;
    exit 0 ("Ran 1 test") with a placeholder present, which was then removed
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 -c "date.fromisoformat(...)"` over AC7's five refused strings plus `20260822` → all
    five refused, `20260822` accepted, which is why the plan adds a regex before the parse
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings (the
    `project.commands.test-null` warning is cleared by this execution)
  - `.claude/agile-skills/scripts/lint-claims <five file paths>` → exit 0, but it printed
    "checked the whole tree" and **ignored the paths**, so the exit code meant nothing about the
    new documents. Noted as a toolkit wrinkle rather than trusted
  - `.claude/agile-skills/scripts/transition WI-0001 --to planned ...` → **exit 1**, hard gate
    `claims-are-sourced` failed: `lint-claims --changed-since main` found 12 unsourced absolute
    claims across `ADR-0003`, `ADR-0004` and `docs/architecture/overview.md`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main --root .` → exit 0, 0 errors,
    after citations were added to all 12
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings; re-run by
    the transition)
  - `every-criterion-is-addressed` → **pass**. The mapping table in `plan.md` has one row per
    criterion, AC1 through AC12, each naming the step that satisfies it and a specific
    demonstration — a named test file with the inputs and the expected exit code, not the word
    "tests". Checked by counting: twelve criteria in `item.md`, twelve rows in the table, no AC
    without a row and no row without an AC.
  - `project-commands-resolved` → **pass**. `commands.test` and `commands.lint` are set to
    commands run in this project during this execution, with their exit codes above.
    `commands.build` stays `null` because nothing is built — the tool runs from the checkout — and
    that is recorded in `ADR-0005` and in a comment beside the key rather than left to be inferred.
  - `decisions-recorded` → **pass**. Three ADRs created (`ADR-0003`, `ADR-0004`, `ADR-0005`), each
    with at least two options and their costs, a decision stated so code can be checked against
    it, and a reversibility statement. Two existing ADRs (`ADR-0001`, `ADR-0002`) were followed
    and cited rather than reopened. Decisions not worth an ADR are in `plan.md`'s `## Assumptions`
    with their reversal cost, which is the middle branch of the preference order.
  - `claims-are-sourced` → **pass on the second attempt.** The first transition was refused: this
    gate runs `lint-claims --changed-since main`, which found 12 absolute claims — "never", "every",
    "no", "nothing", "exactly" — asserted about a backticked identifier or an ADR with no citation
    in the same paragraph. Each was fixed by citing what it actually rests on (`ADR-0001`'s record
    separation, `WI-0001` AC6's amount grammar, `WI-0002` AC2's balance property, `WI-0001` AC9 and
    AC10) rather than by softening the sentence, which would have hidden the claim instead of
    sourcing it. Re-run → exit 0, 0 errors. `validate-workspace` independently resolves every
    citation in the tree → 0 errors, 0 warnings.
    **Worth recording about the toolkit:** running `lint-claims` with explicit file paths reports
    "checked the whole tree" and exits 0 regardless — it ignores the paths. Only the
    `--changed-since` form the gate uses actually checks new work, so a `plan` execution that
    self-checks with file arguments will believe it has passed a gate it has not run.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new)
  - `docs/architecture/overview.md` (new, v1)
  - `docs/architecture/adr/ADR-0003-one-json-ledger-file-chosen-per-run.md` (new, v1)
  - `docs/architecture/adr/ADR-0004-amounts-are-integer-minor-units.md` (new, v1)
  - `docs/architecture/adr/ADR-0005-no-third-party-dependencies.md` (new, v1)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` filled in, `commands.build`
    documented as deliberately null
  - `expenses/__init__.py`, `tests/__init__.py` (new, empty — the skeleton that makes the two
    commands runnable)
  - `tracker/board.md` — regenerated
- **Result:** WI-0001 is planned. Eight steps, each ending in something observable and each
  carrying its own tests; twelve criteria mapped to specific demonstrations; three ADRs for the
  three decisions this greenfield forced — storage, money representation, and dependencies. The
  project now has runnable test and lint commands, and the lint one is recorded as the weak check
  it actually is.
- **Status:** `ready` → `planned`

## 2026-08-22T02:12:20Z — plan v0.2.0 — architect

- **Item:** WI-0001
- **Trigger:** correction to the immediately preceding entry, written without a status change. The
  record is append-only, so an omission is repaired by a later entry rather than by editing.
- **Inputs read:**
  - `tracker/items/WI-0001/journal.md` — the `plan` entry at 2026-08-22T02:12:01Z
  - `tracker/items/WI-0001/artifacts/plan.md`
  - the `run-gate` output of the transition that wrote that entry
- **Decisions:**
  - **What was wrong:** the preceding entry recorded the five hard gates from
    `references/contract.md` and omitted the advisory gate `plan-is-executable-without-you`, which
    `run-gate` listed. `spec/journal-and-history.md` §2.2 requires every gate in the contract to
    appear, advisory included; recording only the hard ones is the silent omission that rule
    exists to prevent.
  - **The gate, assessed now:** `plan-is-executable-without-you` → **pass, with one soft spot.**
    Read as someone who had never seen the item: steps 1–7 each name the file to change, the
    functions to add and what is observable afterwards, and every decision they depend on is made
    in `## Approach`, `## Assumptions`, or one of `ADR-0003`, `ADR-0004`, `ADR-0005`. The soft spot
    is **step 8**, which says to update the architecture document "if and only if implementation
    changed the shape" — a judgement the plan does not make for the developer. It is left that way
    deliberately: whether the shape changed is not knowable until the code exists, and the
    alternative — mandating a version bump — would produce exactly the empty bump
    `spec/doc-header.md` §3 warns devalues every other one. If `implement` finds it ambiguous, that
    is a question for `answer-questions`, not a guess.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, run
    immediately before this entry)
  - `every-criterion-is-addressed` → **pass** (unchanged; evidence in the preceding entry)
  - `project-commands-resolved` → **pass** (unchanged; evidence in the preceding entry)
  - `decisions-recorded` → **pass** (unchanged; evidence in the preceding entry)
  - `claims-are-sourced` → **pass** (unchanged; `lint-claims --changed-since main` → exit 0)
  - `plan-is-executable-without-you` (advisory) → **pass**, assessed above. This is the gate the
    preceding entry omitted.
- **Artifacts:** none; this entry changes no file other than `journal.md` itself
- **Status:** `planned` → `planned` (unchanged)
- **Result:** The advisory gate omitted from the `plan` entry is recorded, with its assessment and
  the one place the plan deliberately leaves a judgement to the developer.

## 2026-08-22T02:14:33Z — implement v0.2.1 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next` as the only runnable candidate (EP-001 has a
  null owner; WI-0002 and WI-0003 both depend on this item, which is not `done`).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the twelve acceptance criteria, the out-of-scope list, and
    the nine assumptions `refine` recorded as its own
  - `tracker/items/WI-0001/artifacts/plan.md` — the eight steps, the interface, the six
    assumptions, and the AC-to-step mapping this execution follows
  - `tracker/items/WI-0001/history.md` — five rows, last one `ready → planned` by `plan`; no
    send-back from `verifying` or `in-review`, so this is a fresh execution rather than a defect fix
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` — all five `answered`, all five
    propagated into `item.md` before `refine` passed the Definition of Ready, so nothing is read
    out of a question file and acted on directly
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, and the two real
    commands `plan` recorded
  - `docs/architecture/overview.md` v1, `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`
  - the working tree: `expenses/__init__.py` and `tests/__init__.py` exist and are empty, exactly
    as `plan`'s last risk bullet said; nothing else has been written
- **Decisions:**
  - Branched from `main` at `5d23d40` rather than reconciling with existing work: `git branch -a`
    shows no `wi/WI-0001`, and `git status` is clean, so there is nothing to reconcile.
  - The plan's eight steps are executed in the order written, each with its tests in the same
    commit. No step is reordered and no step is merged into another.
- **Questions raised:** none
- **Commands:**
  - `git branch -a` → exit 0 (only `main`)
  - `git status --short` → exit 0, empty
  - `git checkout -b wi/WI-0001 main` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (0 errors, 0 warnings)
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no code and no tests exist on the branch; the suite
    currently exits 5 on an empty `tests/`, which is why the plan attaches tests to each step)
  - `lint-clean` → **skipped** (not yet run: nothing has been written on this branch)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings — run
    before the branch was cut, as the state this execution starts from)
  - `every-criterion-has-a-test` → **skipped** (not yet run: no test exists yet)
  - `commits-reference-the-item` → **skipped** (not yet run: the branch has no commits of its own)
  - `claims-are-sourced` → **skipped** (not yet run: no prose has been written on this branch)
- **Artifacts:**
  - branch `wi/WI-0001`, created from `main` at `5d23d40`, no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0001 has started on a fresh branch. The completion gates have
  not run; the closing entry for this execution reports them.

## 2026-08-22T02:23:29Z — implement v0.2.1 — developer

- **Item:** WI-0001
- **Trigger:** continuation of this execution — the item was moved to `in-progress` at
  2026-08-22T02:14:33Z by the opening entry above, and this is the same execution reporting.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/plan.md` — the eight steps, executed in order
  - `tracker/items/WI-0001/item.md` — the twelve criteria, unchanged by this execution
  - `docs/architecture/overview.md` v1, `ADR-0001` … `ADR-0005`
  - `tracker/project.yaml` — the two commands the gates run
  - the branch itself, after each commit
- **Decisions:**
  - **Subcommands are registered in the step that implements them**, not all six in step 4 as the
    plan's wording says. Four of the six handlers do not exist until steps 5 and 6, so a step-4
    commit registering all six would not import. The parser at the head is the plan's parser.
  - **`parse_name` and `parse_description` were added to `model.py`.** AC1 and AC3 require blank
    inputs to be refused, and the plan's own principle is that every input rule lives in
    `model.py` so WI-0003 reuses it. Putting them in `cli.py` would have been the deviation.
  - **`model.today()` wraps `date.today()`** so `cli.py` does not import `datetime` for one
    default and WI-0003 gets the same entry point. One line, trivially reversible.
  - **`store.load` raises `StoreError` for a document that is valid JSON but not shaped like a
    ledger**, not only for malformed JSON. Plan assumption 5 says a corrupt file must never read
    as empty; a wrongly-shaped document is the same hazard by another route, and the alternative
    was an unhandled `KeyError` traceback.
  - **`docs/architecture/overview.md` went to v2** although step 8 said to leave the docs alone
    unless the shape changed. The shape did not change, but v1 stated that the normalised name
    "is an index built when the ledger is loaded" and `find_person` scans and computes the key per
    comparison — a document asserting something false about the code is worth the bump on its own.
  - **Two dead branches were deleted rather than kept as defence.** `_resolve_sharers` had a
    guard for "no people recorded" and one for "an empty sharer list"; the payer check runs first
    and `argparse`'s `append` never yields an empty list, so neither was reachable. Unreachable
    code that looks like a rule invites a reader to believe the rule exists.
  - **Decided *not* to make, and not escalated either, because the plan already made it:** the
    position of `--file` before the subcommand. `python3 -m expenses people --file X` is a usage
    error. The plan fixed `--file` as global-and-preceding, no criterion constrains the position,
    and widening it would have been re-litigating the plan. It is now stated in `overview.md` v2
    and in the report's `## What I did not do` so it is visible rather than discovered.
  - **Nothing was escalated.** No decision met the tests for one: none changes an interface
    another item depends on beyond what `ADR-0003` and `ADR-0004` already fix, none contradicts an
    ADR, none decides user-visible behaviour no criterion covers, and each is one file to reverse.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 83 tests in 2.339s`, `OK`
    (run again on the final head after the report was committed)
  - `python3 -m compileall -q expenses tests` → exit 0
  - `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 9 commit(s)
    on main..wi/WI-0001 name WI-0001"
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `git diff --name-only main..wi/WI-0001` → 16 files
  - intermediate: `python3 -m unittest ...` after each of steps 1–7, exit 0 each time
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, 83 tests, OK)
  - `lint-clean` → **pass** (`python3 -m compileall -q expenses tests` → exit 0. `ADR-0005` records
    that this is a syntax check standing in for a linter: green means every file parses, no more)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md`'s evidence table names at least one
    test method for each of AC1–AC12; the eleven refused amounts and the six refused dates are
    subtests, and every CLI refusal goes through `assertRefused`, which checks the exit code, the
    stderr line and the ledger file's bytes together)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → exit 0, 9 of 9 commits)
  - `no-unplanned-scope` → **pass**, advisory (16 files: five under `expenses/`, six under
    `tests/`, `docs/architecture/overview.md`, and four tracker files that are this execution's
    own record. Every hunk traces to a plan step; the five deviations in the report are the only
    places the diff exceeds the plan's letter)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/impl-report.md`
  - `docs/architecture/overview.md` v2
  - `expenses/model.py`, `expenses/store.py`, `expenses/cli.py`, `expenses/__main__.py`
  - `tests/cli_harness.py`, `tests/test_model.py`, `tests/test_store.py`,
    `tests/test_cli_people.py`, `tests/test_cli_expenses.py`, `tests/test_cli_repayments.py`,
    `tests/test_persistence.py`
  - branch `wi/WI-0001`, commits `5d23d40..5e83721` (nine)
- **Status:** `in-progress` → `verifying`
- **Result:** All eight plan steps are done and all seven gates pass on the branch head. The tool
  records people, expenses and repayments to one JSON ledger chosen per run and lists them back
  from a new process; 83 tests cover all twelve criteria, with the eleven refused amounts and the
  six refused dates exercised through the command line as well as the parser. Five deviations from
  the plan and five things deliberately not done are in `impl-report.md`; the two a reviewer
  should not miss are that concurrent writes can lose an update, and that the on-disk `version`
  field is written but never read.

## 2026-08-22T02:31:02Z — verify v0.1.2 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the twelve criteria, read **first** and used to derive every
    check before `impl-report.md` was opened
  - `tracker/items/WI-0001/artifacts/plan.md` — to read the diff against it
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the criteria, to check its
    claims rather than to source evidence from them
  - `tracker/items/WI-0001/history.md`, `tracker/project.yaml`,
    `docs/architecture/overview.md` v2, `ADR-0001` … `ADR-0005`
  - the code at branch `wi/WI-0001`, commit `49dd2a0cffdabf33fd4976f9d93bfc62edbc591f`, working
    tree clean
- **Decisions:**
  - **The success-line-on-failed-write defect is BUG-0001, not a send-back.** `verify`'s rule is
    that a send-back is for a failure of this item's *own* acceptance criteria. WI-0001 defines a
    refusal as three things — a stderr message naming what was wrong, a non-zero exit code, and no
    change to the recorded data — and all three hold on a failed write; the md5 comparison confirms
    the data is untouched. No criterion constrains stdout in that case, so the item is not failing
    and the defect needed an item of its own rather than a quiet mention.
  - **One bug for all three commands.** `add-person`, `add-expense` and `repay` share one root
    cause and one fix. Three items would be three reproductions of the same line.
  - **AC5 was judged `pass`, not `ambiguous`.** The criterion says the data "holds the single
    amount 60" and the file holds `6000`. `ADR-0004` fixes minor units as the representation, and
    the criterion's decidable content — one amount, three sharers, no per-sharer amount — is
    identical under either reading. An `ambiguous` verdict here would have suspended the item over
    a distinction that changes no observation. Recorded in the report's `## Not verified, and why`
    so the judgement is visible rather than silent.
  - **AC9's default location was verified with `XDG_DATA_HOME` and then `HOME` redirected**, not
    by writing to the operator's real `~/.local/share`. That is still "no location given" from the
    tool's point of view; the literal default path was confirmed by observing which path the tool
    chose under a redirected `HOME`. Declared in `## Not verified, and why`.
  - **`20260822` was tested against AC7 although the criterion does not name it.** It is the form
    `date.fromisoformat` accepts on its own, so it is the one way a plausible implementation would
    quietly widen the criterion. It is refused.
  - **Three expenses were recorded deliberately out of date order for AC8**, so that a listing
    which silently sorted by date would be caught rather than looking correct.
  - No criterion was judged `ambiguous`, so no question was filed.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 83 tests in 2.333s`, `OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `git rev-parse HEAD` → `49dd2a0cffdabf33fd4976f9d93bfc62edbc591f`; `git status --short` → empty
  - AC1: 1 accepted + 7 refusals through `python3 -m expenses … add-person` → exits 0 / 2
  - AC2: `people` empty and with four people → exit 0 both
  - AC3: 2 accepted + 4 refusals through `add-expense` → exits 0 / 2
  - AC4: record with no `--shared-by`, then `add-person Cara`, then read the file → sharers
    `['Ana', 'Ben']`
  - AC5: read the ledger JSON; `add-expense --help` → five options, no share option
  - AC6: 3 accepted + 11 refusals, md5 before/after each → exit 2 and unchanged each time
  - AC7: 2 accepted + 6 refusals (including `20260822`) → exit 2 and unchanged each time
  - AC8: `expenses` empty and with three out-of-date-order records → exit 0
  - AC9: 12 invocations covering the default, a redirected `HOME`, two `--file` paths, a nested
    path, a never-written path, mode 500, mode 000 and a corrupt file → exits 0 / 1 as appropriate
  - AC10: 6 recording processes then 6 listing processes; `cmp` on each pair → identical
  - AC11: 2 accepted + 7 refusals through `repay` → exits 0 / 2
  - AC12: `repayments` empty and with three records; `grep` across both listings → 0 crossovers
  - defect reproduction: `add-person`, `add-expense` and `repay` into a mode-500 directory → exit
    1 with a success line on stdout, three times
  - test sensitivity: 12 source mutations, full suite after each, source restored → 12 × FAILED,
    then exit 0 restored, `git status --short` empty
  - `.claude/agile-skills/scripts/new-item --id BUG-0001 --type bug … --found-in WI-0001` → exit 0
  - `.claude/agile-skills/scripts/journal-entry BUG-0001 --skill verify --body-file …` → exit 0
  - `.claude/agile-skills/scripts/board-gen .` → wrote `tracker/board.md`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, 83 tests, OK)
  - `lint-clean` → **pass** (`python3 -m compileall -q expenses tests` → exit 0. Per `ADR-0005`
    this is a syntax check, not a style linter; the report says so in `## Not verified, and why`)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, with
    BUG-0001 now in the tree)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md`'s criteria table gives
    the command this skill ran and its actual output for each of AC1–AC12; no row cites
    `impl-report.md`)
  - `negative-cases-exercised` → **pass** (41 distinct refusals triggered across AC1, AC3, AC6,
    AC7, AC9 and AC11, plus the three empty listings; each checked for a stderr line, a non-zero
    exit, and — where a ledger already existed — an unchanged md5)
  - `tests-would-fail-without-the-change` → **pass**, advisory (twelve mutations, one per
    criterion, every one turned the suite red; table in the report)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md`, carrying
    `Verified-commit: 49dd2a0cffdabf33fd4976f9d93bfc62edbc591f`
  - `tracker/items/WI-0001/item.md` — all twelve criteria ticked, each against a command in the
    report
  - `tracker/items/BUG-0001/` — a new bug at `ready` under `EP-001`, `found-in: WI-0001`, with six
    reproduction steps and verbatim output
  - `tracker/board.md`, regenerated
- **Status:** `verifying` → `in-review`
- **Result:** All twelve criteria pass against commit `49dd2a0`, each demonstrated by a command
  run here rather than by the implementation report, and all twelve are ticked. Every mutation of
  the twelve behaviours turns the suite red, so nothing is covered only in appearance. One defect
  outside the criteria — a success line printed on stdout when the ledger write fails — is filed
  as BUG-0001 against this item's delivered behaviour; it loses no data and returns the right exit
  code, which is precisely why the criteria do not catch it.

## 2026-08-22T02:36:32Z — review-close v0.3.1 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` as the highest-priority runnable item
  (critical, ahead of BUG-0001 at medium).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the twelve criteria and their tick state
  - `tracker/items/WI-0001/artifacts/verify-report.md` — the evidence per tick and the declared
    gaps; two rows spot-checked by re-running them
  - `tracker/items/WI-0001/artifacts/impl-report.md` — the five declared deviations, each judged
  - `tracker/items/WI-0001/artifacts/plan.md` — the design the diff is judged against
  - `tracker/items/WI-0001/journal.md` — all nine entries, in full, including the `plan`
    correction at 02:12:20Z
  - `tracker/items/WI-0001/history.md` — eight rows, chain checked row by row
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-005.md` — all `answered`; two consequence
    lists opened and the named files checked
  - the diff `main..4c31fb9` — every hunk, plus `expenses/model.py`, `expenses/store.py`,
    `expenses/cli.py` and `expenses/__main__.py` read in full
  - `docs/architecture/overview.md`, `docs/product/vision.md`, `ADR-0001` … `ADR-0005`
- **Decisions:**
  - **Accepted, `outcome: delivered`.** All twelve Definition of Done criteria pass, one of them
    after a correction made in this review.
  - **D12 found a wrong claim and I corrected it here rather than sending the item back.**
    `overview.md` said `cli.py` is "the only one that exits"; `cli.main` returns an int and
    `__main__.py` is the only statement in the package that ends the process. It is one clause in
    a document, no code is wrong, and a send-back would cost a full
    `implement` → `verify` → `review-close` cycle to change a sentence. Recorded as `overview.md`
    v3 with its own change-log row and as finding 1 in `review.md`. The correction was reached by
    opening the four modules, which is the only way this check can fail.
  - **`--file ""` falls through to the default rather than being refused.** Confirmed by running
    it. Not a send-back: no criterion covers an empty path, and the behaviour mirrors `ADR-0003`'s
    explicit rule for an empty `EXPENSES_LEDGER`. Recorded as an accepted gap and flagged for
    WI-0003, which is the first item that will pass paths programmatically.
  - **Five declared gaps accepted, and written into `item.md`'s `## Notes`** rather than left in
    the two reports. Once an item is `done` nobody reopens its verification report, so a gap that
    lives only there is lost rather than accepted. Each row names who should pick it up.
  - **BUG-0001's classification agreed with, after re-running its reproduction.** With the ledger
    directory at mode 500, `add-person` prints `Added Cara.` on stdout, the failure on stderr, and
    exits 1. WI-0001 defines a refusal as a stderr message, a non-zero exit and unchanged data;
    all three hold, so the defect is genuinely outside this item's criteria and belongs in its own
    item rather than as a send-back.
  - **One claim left as written and flagged instead of corrected:** `overview.md` says the shared
    validators mean WI-0003's import "cannot accept an amount or a date the hand-entry command
    would refuse". WI-0003 does not exist, so nothing enforces it. It reads as design intent in
    context; recorded in `review.md`'s `## What I examined` so whoever closes WI-0003 re-audits it
    rather than re-quoting it — which is the propagation D12 exists to stop.
  - **Merge order:** trial-merged into a throwaway branch off `main` and ran the suite on the
    merge result; deleted the trial; closed the item while the branch was still unmerged; then
    merged for real. Closing first is required because `check-commit-refs` reads
    `main..wi/WI-0001`, and merging empties that range.
  - **The epic is not closed.** WI-0001 is not `EP-001`'s last open child: WI-0002 and WI-0003 are
    `draft` and BUG-0001 is `ready`. No epic Definition of Done assessment and no `sign-off`
    question are due yet; `check-epic-signoff` confirms the gate applies to epic closure only.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "verified
    at 49dd2a0c; wi/WI-0001 has moved to 4c31fb96 but only the record changed (9 file(s) under
    tracker/ or docs/), so the verification still covers the code"
  - `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 12
    commit(s) on main..wi/WI-0001 name WI-0001"
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0001` → exit 0 (work-item, not an epic)
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
  - `git checkout -b trial-merge main; git merge --no-ff wi/WI-0001` → clean, no conflicts
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 83 tests`,
    `OK`; `python3 -m compileall -q expenses tests` → exit 0; `validate-workspace .` → exit 0
  - `git checkout wi/WI-0001; git branch -D trial-merge` → deleted, unmerged
  - D12 audit: `grep` for `print`/`SystemExit`/`stderr` and for the import lines across all four
    modules; `grep` for `float`/`Decimal`/`round`; `python3 -m expenses people --file /tmp/x.json`
    → `error: unrecognized arguments`, exit 2; `python3 -m expenses --file "" add-person Ana` →
    exit 0, wrote to the XDG default; `add-expense --payer ANA --shared-by "  ben  "` → stored
    `Ana` and `Ben`; the mode-500 reproduction of BUG-0001
  - `grep -c "^- \[x\] AC" tracker/items/WI-0001/item.md` → 12
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each recorded with its own result and evidence in
    `review.md`'s Definition of Done table; D12 passes after the `overview.md` v3 correction)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` → exit 0; the
    comparison was run, not assumed)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` → exit 0, 12 of 12, run before
    the merge while `main..wi/WI-0001` was still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t . -q`
    on the trial merge of `wi/WI-0001` into a copy of `main` → exit 0, 83 tests, OK)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass**. From the tracker and `git log --grep WI-0001` alone:
    *what was built and why* — `plan.md`'s eight steps and `impl-report.md`'s twelve-row evidence
    table, against a story and twelve criteria; *which skill decided what* — `intake` split the
    work, `refine` recorded nine assumptions as its own and passed the DoR with no override,
    `answer-questions` propagated five stakeholder answers and decided `ADR-0002`'s remainder rule
    as a delegation, `plan` wrote `ADR-0003`/`0004`/`0005`, `implement` declared five deviations,
    `verify` filed BUG-0001, this review corrected one documentation claim; *what questions arose
    and how they were resolved* — five, all `answered-by: human`, each with a `## Consequences`
    list naming files I opened; *what verification found* — twelve passes with the command and
    output for each, twelve mutation checks, and one defect outside the criteria
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0, including
    `review.md` and `overview.md` v3)
  - `epic-sign-off` → **pass** (`check-epic-signoff WI-0001` → exit 0: the gate applies to epic
    closure, and WI-0001 is a work-item. `EP-001` has three children not yet `done`, so its
    closure and its sign-off question are not due)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md`
  - `tracker/items/WI-0001/item.md` — `## Notes` gains "Gaps accepted at close"; closed
    `delivered`
  - `docs/architecture/overview.md` v3 — the D12 correction
  - the merge of `wi/WI-0001` into `main`, recorded in the commit that follows this entry
- **Status:** `in-review` → `done`
- **Result:** Accepted and closed as delivered. Twelve criteria met, twelve Definition of Done
  criteria passed, the suite green on the merge result, and the record complete enough to
  reconstruct the item from the tracker and `git log` alone. The D12 audit caught one false
  sentence in `overview.md` — `cli.py` does not exit — which is fixed in v3; five declared gaps
  are accepted and written into the item where they will still be read; BUG-0001 carries the one
  defect that no criterion of this item covers. `EP-001` stays `open` with three children to go.
