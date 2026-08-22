# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T18:52:10Z — intake v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly; created by this execution of `intake` as a child of EP-001
- **Inputs read:**
  - the stated idea, verbatim (quoted in full in EP-001's entry for this execution)
  - `tracker/items/` — empty, so this item took the next free `WI-` number
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/dor-dod.md`
- **Decisions:** see EP-001's entry for this execution for how the work was split and why this
  item is one of the parts. This item carries persistence, because "survives a restart" is the only observable way to demonstrate that the group list was stored at all. Its criteria name outcomes rather than commands, because the command surface is open as this item's `Q-001`.
- **Questions raised:** `Q-001` (blocking, to human) — is the tool a set of one-shot subcommands
  or an interactive session? Filed here rather than on the epic because it governs the acceptance
  criteria of all three items and WI-0001 is the first to need it, and because `pipeline.yaml`
  treats the epic status `open` as terminal, so an epic cannot be suspended behind a question at
  all. Its answer must be propagated to WI-0002 and WI-0003 as well. Not answered.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0001 ... --status draft` -> exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to awaiting-answer --resume-to draft ...` -> exit 0

- **Gates:** the four gates of `intake` are execution-wide and are recorded once, with their
  evidence, in EP-001's entry for this execution: `workspace-valid` **pass**,
  `epic-has-success-measures` **pass**, `items-are-separable` **pass** (this item's place in the
  order and its `depends-on` are stated there), `no-solution-in-the-problem` **pass**.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/journal.md`, `tracker/items/WI-0001/history.md` (new)
  - `tracker/items/WI-0001/questions/Q-001.md` (new, open)
- **Status:** `—` -> `draft` -> `awaiting-answer` (resume-to `draft`)
- **Result:** WI-0001 exists with a story, four rough acceptance criteria and an out-of-scope
  list, and is suspended behind one blocking question addressed to the human. It is the first item
  `refine` should take once that question is answered.

## 2026-08-21T18:56:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`, with `Q-001` open, addressed to `human`, and a `## Answer`
  written into it by the human since the previous turn.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` — the question, its three options and the human's
    answer
  - `tracker/items/WI-0001/item.md`, `history.md` (the suspending row records `resume-to: draft`),
    `journal.md` (intake's entry)
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — the question says its
    answer governs all of them, so all of them were read before deciding
  - `tracker/items/EP-001/item.md` and `questions/Q-001.md` (answered earlier in this batch)
  - `docs/product/vision.md` (v2) — "the whole interface is a terminal", and nothing narrower
  - `docs/architecture/adr/` — empty before this execution; no recorded decision to contradict
  - `.claude/agile-skills/spec/question.md` §4, `doc-header.md` §4, `work-item.md`
- **Decisions:**
  - **Treated "whatever you think is best" as a delegation and decided, rather than re-asking.**
    `spec/question.md` §4 lists four conditions for escalation and none of them is "the answer was
    vague". The human had the options, the recommendation and the consequences in front of them and
    handed the choice over; putting it back would spend the scarcest resource in this loop on a
    question they have already declined. This is the case the skill's own warning against an
    architect who forwards everything is about.
  - **Chose A, one-shot subcommands, and recorded it as ADR-0001.** The record was silent, so
    `answered-from-the-record` is satisfied the other way the gate allows: by writing the decision
    down as an ADR with its alternatives. A's decisive property is that it makes every criterion in
    this epic a command and an expected output — the exact bar `refine` has to clear on four items.
  - **Fixed the invocation, exit-status and stream contract in the ADR; left the subcommand
    spellings to `refine`.** Four criteria across the epic already say "a stated error rather than
    a traceback", which is unverifiable until someone says which stream and which exit status. That
    belongs in one shared document. The spelling of each flag does not: it would put four items'
    detail in a document none of them owns, and `refine` is the skill that pins it.
  - **Rewrote AC2 on three items from "exiting and restarting the tool" to separate invocations.**
    Under A there is nothing to exit — every invocation exits. Left as written, the criterion would
    have described a product that was not chosen. This is an amendment to acceptance criteria by
    `answer-questions` propagating an answer, which `spec/work-item.md` §2 permits and requires to
    be journalled: it is recorded here, and it narrows nothing — the same fact is being asserted in
    the vocabulary of the tool that will exist.
  - **Did not touch AC1 anywhere.** Nothing in the answer bears on it.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to draft --actor answer-questions
    --reason "..."` -> recorded under Gates
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
- **Gates:**
  - `answer-is-propagated` (hard) -> **pass** — every path in `Q-001`'s `## Consequences` was
    reopened after writing. `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` exists at v1
    with three options and a reversibility statement. `WI-0001/item.md` AC2 now reads "a separate,
    later invocation", AC3 names standard output and exit `0`, AC4 names standard error and a
    non-zero exit, and `## Notes` cites ADR-0001 instead of an open question. `WI-0002/item.md`
    AC2 and AC3, `WI-0003/item.md` AC2 and `WI-0004/item.md` AC2 and AC3 carry the same contract,
    and all three `## Notes` sections cite ADR-0001.
  - `answered-from-the-record` (hard) -> **pass, by the ADR route** — the record was silent on the
    command surface and the human delegated the choice, so the decision is recorded as ADR-0001 and
    the answer cites it. Nothing was asserted without a document behind it.
  - `escalation-is-justified` (hard) -> **not applicable, nothing escalated** — and the reason for
    not escalating is recorded above, because "the answer was vague" is not one of the four
    conditions.
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0, one pre-existing warning
    about the null test command, which `plan` owns.
  - `item-resumed-correctly` (hard) -> **pass** — the suspending row of 2026-08-21T18:45:59Z
    records `resume-to: draft`; this execution transitioned the item to `draft`. Read from the row,
    not inferred from which skill asked.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — answered; `answered-by: answer-questions`,
    `answered-at: 2026-08-21T18:56:00Z`
  - `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` — new, v1
  - `tracker/items/WI-0001/item.md` — AC2, AC3, AC4 and `## Notes`
  - `tracker/items/WI-0002/item.md` — AC2, AC3 and `## Notes`
  - `tracker/items/WI-0003/item.md` — AC2 and `## Notes`
  - `tracker/items/WI-0004/item.md` — AC2, AC3 and `## Notes`
- **Status:** `awaiting-answer` -> `draft`
- **Result:** The command surface is decided and written down where four items can cite it.
  WI-0001 is back at `draft` with no open question, ready for `refine` to pin its subcommands and
  make its criteria decidable.

## 2026-08-21T19:06:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next`. It was the only runnable candidate: WI-0002,
  WI-0003 and WI-0004 each have a `depends-on` that is not `done`, and EP-001 is an epic at `open`,
  a status with no owner in `pipeline.yaml`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the four criteria as amended by `answer-questions` earlier
    today
  - `tracker/items/WI-0001/history.md` — three rows: created at `draft`, suspended to
    `awaiting-answer` with `resume-to: draft`, returned to `draft`. **This is a fresh draft, not an
    item sent back from a later stage**, so the whole story is open for questioning rather than one
    specific defect.
  - `tracker/items/WI-0001/journal.md` — intake's entry, for what the human has already said, and
    `answer-questions`' entry for what was decided since
  - `tracker/items/WI-0001/questions/Q-001.md` — answered; the command surface
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — a sibling may already
    own part of this scope, and two of the questions below only matter because of what WI-0002 will
    need
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v1)
  - `docs/architecture/adr/ADR-0001` (v1) and `ADR-0002` (v1) — the invocation and refusal contract
    the criteria must be written against, and the sharer syntax that forces Q-004
  - `.claude/agile-skills/spec/dor-dod.md` §1, `work-item.md`, `question.md`
  - `artifacts/refinement-qa.md` — does not exist; this item has not been refined before
- **Decisions:**
  - **Stopped and asked, because the human is not in this session.** `refine`'s second precondition
    is that they are present. They are not, and they answer asynchronously in files, so the skill's
    own escalation applies: file questions addressed to `human`, suspend at `awaiting-answer` with
    `resume-to: draft`, stop. Nothing was rewritten first — rewriting criteria around a guess and
    then asking would produce an item that reads as refined and is not.
  - **Filed three questions, not one and not seven.** Each traces to a Definition of Ready
    criterion that fails, and each carries a concrete recommendation so that "whatever you think"
    is a usable answer rather than another round trip. The agenda below says which criterion each
    one is for.
  - **Decided the empty-name rule myself rather than asking.** A name that is empty or only
    whitespace is refused — message on standard error, non-zero exit, nothing added. No reasonable
    answer differs, and `spec/question.md` §4 does not admit a question whose options are all the
    same. It is stated in Q-004's context so the human can contradict it if they want to.
  - **Did not ask where the data file lives.** AC2 needs "a separate, later invocation" to see the
    same people, which is decidable without knowing the path; choosing the path is a design
    decision and belongs to `plan`, which may ask if it must.
  - **Did not file questions on WI-0002, WI-0003 or WI-0004.** None of them is runnable — each has
    an unfinished dependency — and the questions their refinement will need genuinely depend on the
    answers to these three: the sharer syntax in WI-0002 has to reserve a separator that Q-004
    settles, and the subcommand style that Q-003 settles is the pattern the other three follow.
    Asking now would be asking about work not yet reached, and half the questions would be wrong.
- **Questions raised:** three, all blocking, all addressed to `human`:
  - `Q-002` — when is a name being added a person already in the group, and what should the tool do
    then? For **R4** (AC4 is not decidable) and **R10** (the duplicate-add case is not stated).
  - `Q-003` — what should this item's two subcommands be called? For **R4**: every criterion here
    has to name a command a person can type, and `ADR-0001` explicitly left the spelling to this
    step. It also sets the pattern for the other three items.
  - `Q-004` — may a name contain spaces, and is it acceptable to reserve `,` and `=`? For **R4**
    (AC1 and AC4 say "a name" without saying what one is) and **R10**. Asked now rather than during
    WI-0002 because reserving the separator while the group is empty is free, and doing it after
    people have been recorded means renaming somebody, which this epic has no command for.

  `artifacts/refinement-qa.md` does not exist yet, deliberately: the file must hold the exchange
  verbatim, and there is no exchange until the answers arrive. It is written by the execution that
  consumes them.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning (null test
    command), before filing
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to awaiting-answer --resume-to draft
    --actor refine --reason "..."` -> recorded under Gates
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
- **Gates:**
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0, one pre-existing warning
    about the null test command, which `plan` owns.
  - `definition-of-ready` (hard) -> **fail**, criterion by criterion:
    - **R1** frontmatter and `type`/`epic`/`priority` [auto] -> **pass**.
    - **R2** story names a role, a capability and an outcome [skill] -> **pass**: "As someone
      keeping track of a friend group's shared costs, I want to add people … so that later expenses
      can name them and the group's membership is recorded in one place."
    - **R3** at least one labelled checkbox criterion [auto] -> **pass**: AC1–AC4.
    - **R4** every criterion decidable by observation [skill] -> **fail**. AC1 and AC2 name no
      command to run (Q-003). AC4's "a stated outcome" does not say what the outcome is, and it
      cannot until "already in the group" is defined (Q-002). AC1 and AC4 say "a person" and "a
      name" without saying what a name may be (Q-004). AC3 alone would pass: standard output, exit
      `0`, a message rather than silence — but it still lacks the command.
    - **R5** out of scope names something a reader could assume is included [skill] -> **pass**:
      removing and renaming a person, any attribute beyond the name, and anything to do with
      expenses.
    - **R6** every open question is non-blocking [auto] -> **fail**, by construction: this execution
      filed three blocking ones. It passes when they are answered.
    - **R7** independently deliverable, dependencies sequenced [auto] -> **pass**: no `depends-on`.
    - **R8** refinement Q&A recorded verbatim [auto] -> **fail**: no exchange has happened yet.
    - **R9** one coherent change [skill] -> **pass**: add a person, list the group, persist both.
      The read side and the write side are each unobservable without the other, which is why
      `intake` kept them together.
    - **R10** every combination of introduced behaviours stated, excluded, or recorded as
      unconstrained [skill] -> **fail**: adding a duplicate (Q-002), a name with a space or a
      reserved character (Q-004), and listing an empty group (AC3, stated) are the three cases this
      item introduces; two of them are unstated.
  - `criteria-are-decidable` (hard) -> **fail** — the same finding as R4, and the reason this
    execution did not transition to `ready`. For AC3 I can name the observation and the verdict; for
    AC1, AC2 and AC4 I cannot, because the command and the duplicate rule are unknown.
  - `qa-recorded-verbatim` (hard) -> **not yet applicable** — `refinement-qa.md` is not written
    because no exchange has occurred. Writing a Q&A file listing questions with empty answers would
    make the gate pass on a file with no content in it, which is worse than an honest absence.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-002.md` — new, blocking, to human
  - `tracker/items/WI-0001/questions/Q-003.md` — new, blocking, to human
  - `tracker/items/WI-0001/questions/Q-004.md` — new, blocking, to human
  - `tracker/items/WI-0001/item.md` — unchanged. Nothing was rewritten on a guess.
- **Status:** `draft` -> `awaiting-answer` (`resume-to: draft`)
- **Result:** WI-0001 is not Ready and cannot be until three things are settled that only the person
  who will use the tool can settle: what makes two people the same, what the two subcommands are
  called, and what a name may contain. Each question carries a recommendation, so a one-word answer
  to each is enough to finish the refinement.

## 2026-08-21T19:11:21Z — answer-questions v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`; the human had filled in `## Answer` on all three open
  questions since the previous turn. Dispatched ahead of `next`, because the orchestrator stops on
  any open human-addressed question and would have had nothing else to offer.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` (answered), `Q-002.md`, `Q-003.md`, `Q-004.md`
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md`
  - `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` (v1),
    `ADR-0002-share-model.md` (v1), `ADR-0003-money-and-rounding.md` (v1),
    `ADR-0004-minimum-transfers.md` (v1)
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v1)
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md`,
    `spec/journal-and-history.md`
  - no `artifacts/plan.md` and no `refinement-qa.md` exist on this item yet; the item has never
    been planned and refinement was suspended before any exchange was recorded
- **Decisions:**
  - **Q-002 (route: the human answered).** They chose option B and gave their reason — "I don't
    want two half-right versions of the same person messing up the totals". Recorded as `ADR-0005`
    rather than as a line in `item.md`, because identity is what every other fact in the epic
    points at: an expense names a payer and sharers, a payment names two people, and WI-0003 prints
    nothing but names. A rule that lived on WI-0001 alone would be re-derived three times.
  - **Two derivations beyond that answer, made as architect and marked as such in ADR-0005.**
    First, internal runs of whitespace are collapsed for the identity comparison, not only
    surrounding whitespace as option B said: a doubled internal space is the one variant that no
    printed output would reveal, so it produces precisely the split person they objected to, and
    silently. Second, the identity key applies wherever a person is named, not only in
    `add-person` — a tool that refuses to add `sam` because `Sam` exists and then refuses `sam` as
    a payer because he does not would be incoherent. Both are cheap to state now and would
    otherwise be guesses made by `implement`.
  - **Q-004 (route: the human answered).** Option B: names may contain spaces, `,` and `=` stay
    reserved. Folded into the same ADR as Q-002, because "what a name may be" and "when two names
    are one person" are one rule with two halves and a later reader must not be able to change one
    without seeing the other. Their second sentence — the group contains two people with the same
    first name — is a durable product fact, so it went into `prd.md`, not only into the ADR.
  - **Q-003 (route: decided by this skill, on delegated authority).** "Whatever you think is best"
    is a delegation, and the second one on this subject: `Q-001` was answered the same way and
    produced `ADR-0001`. `spec/question.md` §4 admits no condition that a vague answer satisfies,
    so re-asking would have spent their attention on a question they had twice handed over.
    Decided option A and recorded `ADR-0006`.
  - **ADR-0006 settles the vocabulary for the whole epic, where ADR-0001 had deferred the names to
    each item's refinement.** That deferral is right for one command and wrong for seven: the
    question itself observed that choosing here is choosing four times, and re-deriving the
    pattern on WI-0002, WI-0003 and WI-0004 is how an `add-expense` ends up beside a `payment
    add`. ADR-0006 states the rule that generates the names rather than only listing them, and
    leaves each command's *arguments* to `refine`, which is the part that genuinely differs per
    item. It does not supersede ADR-0001; nothing ADR-0001 decided is changed.
  - **Amended acceptance criteria on all four items, and added three to WI-0001.** WI-0001 AC1,
    AC3 and AC4 were rewritten to name commands and the duplicate rule; AC5, AC6 and AC7 are new
    and carry behaviour the answers introduced (empty and reserved-character names, accents kept
    distinct, unknown subcommand). This is `answer-questions` exercising its permission to change
    criteria: every item is at `draft` or `awaiting-answer`, none is frozen at `ready`, and each
    amendment narrows a criterion to what the human asked for rather than widening it to fit some
    code. Nothing was made easier to pass.
  - **Did not touch `docs/product/vision.md`.** Its decision list is explicitly scoped to the five
    questions `intake` asked; these three came from `refine` and are item-level detail. Adding them
    would push the wrong altitude of fact into the wrong document. `prd.md` took them instead.
  - **Did not write `refinement-qa.md`.** That is `refine`'s artifact and its gate; this execution
    unblocks refinement rather than performing it.
- **Questions raised:** none. Nothing here needed escalating: two questions the human answered
  outright, and the third they delegated, which `spec/question.md` §4 does not make a condition
  for asking again.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before transitioning, as
    expected: `question.awaiting.none-open` (every blocking question now answered) and a stale
    board. Both are the state this execution exists to clear.
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to draft --actor answer-questions`
    → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after transitioning
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` (hard) → **pass**. Each file named in a `## Consequences` section was
    opened after writing and checked to contain the change: `ADR-0005` and `ADR-0006` exist at v1
    with the decisions above; `WI-0001/item.md` carries AC1–AC7 as described and a rewritten
    `## Notes`; `WI-0002/item.md` names `add-expense`/`expenses` in AC1 and AC4 and the identity
    rule in AC3; `WI-0003/item.md` names `who-owes-whom` in AC1 and AC2; `WI-0004/item.md` names
    `add-payment`/`payments` in AC1 and AC6 and the identity rule in AC3; `prd.md` is at v2 with
    both new sections and a change-log row.
  - `answered-from-the-record` (hard) → **pass**. Q-002 and Q-004 cite the human's own words,
    quoted verbatim in the answer and in `ADR-0005`. Q-003 records that the record was silent —
    no code, no convention, no stated preference — and the new decision is `ADR-0006`, cited from
    the answer. The two derivations on Q-002 are labelled as the architect's in both the answer and
    the ADR, so no reader can mistake them for something the human said.
  - `escalation-is-justified` (hard) → **skipped, nothing escalated**. No question was
    re-addressed to the human by this execution.
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exits 0 after the transition and the
    board regeneration; one pre-existing warning remains (`project.commands.test-null`), which
    belongs to `plan` and is not this execution's to clear.
  - `item-resumed-correctly` (hard) → **pass**. The suspending row (2026-08-21T19:08:02Z,
    `draft` → `awaiting-answer`, actor `refine`) records `resume-to: draft`, and this execution
    returned WI-0001 to `draft`.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-002.md` — answered by `human`, with consequences
  - `tracker/items/WI-0001/questions/Q-003.md` — answered by `answer-questions` on delegated
    authority, with consequences
  - `tracker/items/WI-0001/questions/Q-004.md` — answered by `human`, with consequences
  - `docs/architecture/adr/ADR-0005-person-identity-and-names.md` — new (v1)
  - `docs/architecture/adr/ADR-0006-subcommand-names.md` — new (v1)
  - `tracker/items/WI-0001/item.md` — AC1, AC3, AC4 amended; AC5, AC6, AC7 added; `## Notes`
    rewritten
  - `tracker/items/WI-0002/item.md` — AC1, AC3, AC4 amended; `## Notes` extended with ADR-0005 and
    ADR-0006
  - `tracker/items/WI-0003/item.md` — AC1, AC2 amended; `## Notes` extended
  - `tracker/items/WI-0004/item.md` — AC1, AC3, AC6 amended; `## Notes` extended
  - `docs/product/prd.md` — v1 → v2
  - `tracker/items/EP-001/journal.md` — an entry recording the two epic-wide decisions
  - the board, regenerated by `board-gen`
- **Status:** `awaiting-answer` → `draft`
- **Result:** All three of `refine`'s questions are answered and propagated into two new ADRs, four
  items and the PRD. WI-0001 is back at `draft` with criteria that name real commands and a real
  duplicate rule, and `refine` can now run the Definition of Ready pass it was suspended in the
  middle of.

## 2026-08-21T19:22:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next`. This is the resumption of the refinement pass
  suspended at 2026-08-21T19:08:02Z, not a fresh one: the item returned to `draft` from
  `awaiting-answer` because `answer-questions` consumed Q-002, Q-003 and Q-004.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — all answered,
    with their `## Consequences`
  - `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` (v1),
    `ADR-0005-person-identity-and-names.md` (v1), `ADR-0006-subcommand-names.md` (v1)
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v2)
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — to check no sibling
    already owns part of this scope
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/work-item.md`
- **Decisions:**
  - **Rewrote every criterion against a real command line.** The previous set named observable
    outcomes but not what to type. AC1 and AC2 now name `add-person "Sam Okafor"` and `people`
    with their exact output; AC3 states persistence as three separate invocations of the process,
    which is the only form of it a verifier can check without knowing where the data is kept.
  - **Split the old AC4 into five.** "A stated outcome rather than a silent duplicate" is now AC6
    (duplicate refused, with the three identity-key variants spelled out as commands), AC7 (empty
    or whitespace-only name), AC8 (comma or equals sign), AC9 (accents distinct) and AC10 (argument
    arity). Each of the five is a different observation with a different verdict; as one criterion
    they could only be judged as a whole, which is how a partially-implemented rule passes.
  - **Added a general definition of "exits non-zero" above the list**, including that standard
    error must contain no `Traceback (most recent call last)`. Four criteria across this epic say
    "not a traceback"; stating the check once makes each of them decidable without repeating it.
  - **Pinned the exact text of five messages** (`[assumed]`, Q4 in the Q&A). "A stated message" is
    not decidable — two verifiers can disagree about whether some output counts as stated. The
    wording is cosmetic and reversible; leaving it unstated is not, because then `verify` invents
    the standard after the code exists, which is the failure mode the whole pipeline is built to
    avoid.
  - **`people` lists in insertion order** (`[assumed]`, Q5). Alphabetical order would need a
    tie-break rule for names differing in case or carrying accents — both of which ADR-0005 has
    just made significant — and that is a third decision about names on top of two the human has
    already had to make. Insertion order needs none.
  - **`add-person` with two arguments is refused, not joined** (`[assumed]`, Q6). Rejected the
    friendlier reading on the same grounds as the human's own reason for the duplicate rule: a
    mistyped `add-person Sam Okafor Smith` would silently create a third spelling of somebody, and
    this epic has no command to remove them.
  - **Left the storage location and format unconstrained**, and said so in `## Notes` with who
    left it so (R10). It has no observable consequence at this item's level, AC3 covers the only
    thing the human asked for, and it governs all four items — so deciding it here would put an
    epic-wide choice on the item that happens to be first. `plan` records it as an ADR. The
    behaviour when the stored file is unreadable or malformed is left with it, for the same
    reason: it is a property of whatever storage `plan` chooses, not a combination of this item's
    own behaviours.
  - **Widened `## Out of scope` from three entries to five**, adding the two things a reader would
    most reasonably assume are here: where the data lives, and what happens when two people run the
    tool at once. The second is excluded by `vision.md` (v3) at product level and was not stated on
    any item.
  - **Did not re-file anything to the human.** The three questions this pass was suspended on are
    answered; nothing else on this item turns on intent no document records. Q4 to Q6 are detail
    the human declined twice to be asked about — `Q-001` and `Q-003` were both answered "whatever
    you think is best" — so they were decided here and marked `[assumed]`, unconfirmed, in both the
    Q&A and `## Notes`. Inventing a question to fill a round trip would have stopped the pipeline
    and, on that evidence, returned nothing.
- **Questions raised:** none new. Three (`Q-002`, `Q-003`, `Q-004`) were raised by the previous
  execution of this skill and are answered; the full exchange is at
  `artifacts/refinement-qa.md`. Three answers are recorded there as `[assumed]` (Q4, Q5, Q6) and
  one as `[unresolved]` by design (Q7, storage), carried into `## Notes` as unconstrained rather
  than as a risk.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (1 pre-existing warning,
    `project.commands.test-null`, which belongs to `plan`)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to ready --actor refine` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exits 0.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion:
    - **R1** frontmatter complete [auto] → **pass**: validator clean; `type: work-item`,
      `epic: EP-001`, `priority: high`.
    - **R2** story names role, capability, outcome [skill] → **pass**: "As someone keeping track of
      a friend group's shared costs, I want … so that later expenses can name them and the group's
      membership is recorded in one place rather than assumed."
    - **R3** at least one labelled checkbox criterion [auto] → **pass**: AC1–AC11.
    - **R4** every criterion decidable by observation [skill] → **fail on entry**, and the reason
      this pass had been suspended: AC1, AC2 and AC4 named no command, and AC4's "stated outcome"
      named no rule. Rewrote all of them against `add-person` and `people`, pinned the message
      text, and defined "exits non-zero" once for the list → **pass**. No criterion now contains an
      adjective without a threshold; the only judgement left to a verifier is string comparison and
      an exit status.
    - **R5** out-of-scope names something a reader would assume is included [skill] → **pass**:
      five entries, of which the storage location and concurrent use are both things a reader would
      reasonably expect this item to cover.
    - **R6** every open question non-blocking [auto] → **pass**: all four questions on this item
      are `answered`; validator reports no open blocking question.
    - **R7** independently deliverable [auto] → **pass**: no `depends-on`.
    - **R8** Q&A recorded verbatim [auto] → **fail on entry** (the file did not exist) →
      **pass**: `artifacts/refinement-qa.md` now carries all three filed questions with the
      human's answers quoted exactly, plus four decided here, each tagged.
    - **R9** one coherent change [skill] → **pass**: add a person, list the group, persist both.
      The read side and the write side are each unobservable without the other.
    - **R10** every combination stated, excluded, or recorded as unconstrained [skill] → **fail on
      entry** (duplicate, invalid name and empty-group behaviour were unstated) → **pass**: the two
      subcommands' cases are now AC5 (empty listing), AC6 (duplicate), AC7 and AC8 (invalid names),
      AC9 (accents), AC10 (arity, including a listing command given an argument) and AC11 (unknown
      or missing subcommand); the two things left open — storage, and an unreadable stored file —
      are named in `## Notes` as deliberately unconstrained, by `refine`.
  - `criteria-are-decidable` (hard) → **pass**. Each criterion names the command and the verdict:
    AC1 `add-person "Sam Okafor"` → stdout equals `Added Sam Okafor.`, exit 0. AC2 `people` →
    stdout is the single line `Sam Okafor`, exit 0. AC3 three separate invocations → the third
    prints `Alice` and `Bob`. AC4 add `Carol`, `alice`, `Bob` → `people` prints those three names
    in that order and nothing else. AC5 `people` on an empty group → stdout equals `No one is in
    the group yet.`, exit 0. AC6 three duplicate spellings → stderr equals `Sam Okafor is already
    in the group.`, exit ≠ 0, and `people` still prints one line. AC7 `add-person ""` and
    `add-person "   "` → stderr equals `A name cannot be empty.`, exit ≠ 0. AC8 `add-person
    "Anna,Karin"` and `add-person "a=b"` → stderr equals the reserved-character message, exit ≠ 0.
    AC9 `add-person "Jose"` after `José` → exit 0 and `people` prints two lines. AC10 three
    malformed invocations → exit ≠ 0 with the stated stderr message each time, and nobody added.
    AC11 `no-such-command` and no subcommand → exit ≠ 0, stderr names the unknown subcommand in the
    first case. Every one of them is settled by comparing captured output and an exit status, with
    no traceback on stderr.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` reproduces each of the
    three filed questions with the reason it was asked, and each answer exactly as the human wrote
    it, including the delegation on Q1 which is recorded as the delegation it was rather than
    tidied into a preference. The four answers decided here are tagged `[assumed]` or
    `[unresolved]` and explicitly marked as not confirmed by the human.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new) — the full exchange, the assumptions,
    and the per-criterion DoR table
  - `tracker/items/WI-0001/item.md` — criteria rewritten and extended from four to eleven;
    `## Out of scope` widened from three entries to five; `## Notes` restructured into what was
    decided, what was assumed without the human, and what is deliberately unconstrained
- **Status:** `draft` → `ready`
- **Result:** WI-0001 meets the Definition of Ready on all ten criteria, with no override. Every
  criterion is a command, an expected output and an exit status, so `verify` can do its job from
  this item alone. Three assumptions and one deliberate non-decision are recorded in `## Notes`
  for `plan` to inherit rather than rediscover.

## 2026-08-21T19:26:00Z — plan v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next`. First item in the project to be planned, so
  this execution also creates the architecture overview and fills in the project's commands.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (11 criteria), `history.md`, `journal.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — in particular the four `[assumed]` and
    `[unresolved]` entries, which are where the design's soft ground is
  - `docs/architecture/adr/` — all six existing: `ADR-0001` (invocation, exit codes, streams),
    `ADR-0002` (share model), `ADR-0003` (money, derived-not-stored), `ADR-0004` (settling
    transfers), `ADR-0005` (name identity), `ADR-0006` (subcommand names)
  - `docs/product/vision.md` (v3), `docs/product/prd.md` (v2)
  - `tracker/project.yaml`, `.gitignore`
  - `docs/architecture/overview.md` — **did not exist**; created by this execution
  - the project's source code — **there is none**. `git ls-files` outside `.claude/` returns only
    `docs/`, `tracker/`, `.gitignore` and the two harness markdown files. This item creates the
    first line of Python in the project, so there was nothing to read and nothing to fit into.
- **Decisions:**
  - **Storage: one JSON file, `ADR-0007` (route: decided, no document covered it).** `refine`
    left this open on purpose. Chose JSON over `sqlite3`, line-oriented text and `pickle`: the
    record is a friend group's expenses, so it is small, and the properties that matter are that a
    person can open it, read it, back it up and repair it. The two parts worth more than the
    format itself are (a) reads treat a missing key as empty, so WI-0002 and WI-0004 add their
    kinds of fact with no migration, and (b) a file that exists but does not parse is a refusal
    that **writes nothing**, so a damaged record can still be repaired by hand.
  - **Location `EXPENSES_FILE` → `$XDG_DATA_HOME` → `~/.local/share`, resolved at call time.** The
    override is not a convenience: without it, no acceptance criterion could be checked without
    writing to the machine's real data directory. Rejected a working-directory default because it
    would give every directory its own group, which is not the product `vision.md` describes.
  - **Testing: `unittest` and no linter, `ADR-0008` (route: decided, forced by a recorded
    constraint).** The stdlib-only constraint in `prd.md` v2 rules out `pytest` and `ruff`, and
    both are in fact absent on this machine. Recorded `python3 -m compileall` as `commands.lint`
    while saying plainly in the ADR that it is a syntax check and not a linter — a weak gate
    documented as weak beats a gate skipped on every item forever, which carries no information
    about whether anybody looked. Both commands were **run** before being recorded, including
    against a deliberately failing test and a deliberately broken source file, to confirm they
    exit `1` rather than passing vacuously.
  - **Three modules with one direction of dependency**, recorded in `docs/architecture/overview.md`
    v1: `cli.py` owns the streams and the exit status, `group.py` owns the rules, `storage.py`
    owns the file. Each is the only place one kind of change lands. This is what lets eleven
    criteria be asserted by calling one function and inspecting what came back.
  - **Errors carry their own message text and `cli.py` prints them.** `RuleError` and
    `RecordError` are caught once, around the whole dispatch, which is the single place that makes
    "never a traceback" true for those paths rather than something each handler must remember.
  - **Hand-rolled dispatch rather than `argparse` (route: reversible assumption).** The criteria
    pin exact message text; `argparse` writes its own messages and exits `2` from inside the
    parser. Recorded as an assumption rather than an ADR because reversing it is one file,
    `cli.py`, with no data change, no interface change and no criterion change — the criteria
    describe behaviour, not mechanism. Named WI-0002 as the item to revisit it on, since it is the
    first to carry flags.
  - **Exit status `1` for every refusal (route: reversible assumption).** `ADR-0001` requires only
    "non-zero" and every criterion says "exits non-zero", so nothing depends on the value.
  - **AC3 must be tested with real subprocesses (route: decided, from the criterion's meaning).**
    Three in-process calls to `main()` would pass even if the record lived in a module-level
    variable, which is precisely what AC3 exists to rule out. Wrote it into the plan as a
    requirement on step 6 and into `## Risks` as the way this plan could pass falsely.
  - **Did not design past the item.** No README, no packaging metadata, no console-script entry
    point, no migration machinery, and no `expenses`/`payments` keys written into the file before
    anything puts data in them — `ADR-0007` point 2 makes adding them free later, which is what
    removes the temptation. Every step in the plan maps to at least one AC.
  - **Asked the human nothing.** Nothing here is irreversible or turns on intent no document
    records: the storage decision is the one that comes closest, and `refine` had already recorded
    it as unconstrained-by-design with `plan` named as its owner.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` in a scratch layout → exit 0 with a passing
    test, exit 1 with a failing one
  - `python3 -m compileall -q expenses tests` in the same scratch layout → exit 0 clean, exit 1
    with a file containing a syntax error
  - `python3 -m pytest --version` → `No module named pytest`; `python3 -m ruff --version` →
    `No module named ruff` (the evidence behind `ADR-0008`)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, and now **0 warnings**:
    filling in `commands.test` cleared `project.commands.test-null`, which had been standing since
    the workspace was created
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to planned --actor plan` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — `validate-workspace` exits 0 with no errors and no
    warnings.
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table in `plan.md` has one row
    per criterion, AC1 to AC11, each naming the step that satisfies it and the specific assertion
    that demonstrates it (the exact stdout, stderr and exit status, and the test module it lives
    in). No row says "tests". A twelfth row carries the no-traceback clause that heads the criteria
    list, since it applies to every refusal path rather than to one criterion.
  - `project-commands-resolved` (hard) → **pass** — `commands.test` is
    `python3 -m unittest discover -s tests -t . -q` and `commands.lint` is
    `python3 -m compileall -q expenses tests`. Both were executed on this machine before being
    recorded, and both were shown to exit non-zero on a real failure, so neither is a command that
    passes vacuously. `ADR-0008` records why they are these and not `pytest` and `ruff`.
  - `decisions-recorded` (hard) → **pass** — every choice this plan makes is either an ADR
    (`ADR-0007` storage, `ADR-0008` tooling), an existing ADR cited rather than re-decided
    (`ADR-0001`, `ADR-0005`, `ADR-0006`), a documented shape (`overview.md` v1), or one of the
    three entries under `## Assumptions`, each stating what reversing it would cost.
  - `plan-is-executable-without-you` (advisory) → **pass, with one soft spot.** Every step names
    the files it creates and the interface it must expose — function names, arguments, return
    types, exception types, and the exact message strings. Read cold, the one place a developer
    still has to think is the ordering of checks inside the `add-person` handler (validate the
    name before looking for a duplicate, so that `add-person ","` reports the reserved character
    rather than anything about membership); the plan implies it by listing the criteria's messages
    but does not state it as an ordering rule. Left as is rather than turning the plan into the
    implementation, and noted here so `implement` can see it was noticed rather than missed.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new) — 7 steps, the 12-row mapping table, 3
    assumptions with reversal costs, 5 risks, and what is out of scope
  - `docs/architecture/adr/ADR-0007-json-file-storage.md` (new, v1)
  - `docs/architecture/adr/ADR-0008-tests-are-unittest-and-there-is-no-linter.md` (new, v1)
  - `docs/architecture/overview.md` (new, v1) — the three-layer shape, why it is that shape, the
    table of where each decision lives, and how tests are isolated
  - `tracker/project.yaml` — `commands.test` and `commands.lint` filled in; `commands.build` left
    null, because there is nothing to build and a fabricated build command would be the vacuous
    pass the gate warns about
- **Status:** `ready` → `planned`
- **Result:** WI-0001 has a plan a developer can execute without deciding anything the plan does
  not decide, and the project has an architecture document, a storage decision, and commands that
  actually run. The two things most likely to go wrong are named in `## Risks`: confusing the
  identity rule with the display rule, and testing AC3 in-process, where it would pass without
  proving anything.

## 2026-08-21T19:34:00Z — implement v0.1.0 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next`. Fresh start: `git branch` showed no
  `wi/WI-0001`, the last history row was `ready → planned` by `plan`, and no send-back from
  `verifying` or `in-review` had ever happened. Nothing to reconcile with.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC11), `artifacts/plan.md`, `history.md`
  - `tracker/items/WI-0001/questions/` — four questions, all `answered`, all propagated before
    `plan` ran; nothing moved to `answered` since the last journal entry, so nothing to re-read
  - `docs/architecture/overview.md` (v1), `ADR-0001`, `ADR-0005`, `ADR-0006`, `ADR-0007`,
    `ADR-0008`
  - `tracker/project.yaml` — branch prefix `wi/`, and both commands filled in by `plan`
  - the project's source code — none existed; this execution wrote the first Python in the repo
- **Decisions:**
  - **Stream injection on `cli.main`** (`main(argv, out=None, err=None)`, defaults resolved at
    call time). Inside the plan's latitude: the signature the plan named still works for every
    caller and the behaviour is identical. It lets the test helper capture stdout and stderr by
    passing them in rather than patching module globals, which is the difference between a helper
    that is obviously correct and one that has to be reasoned about.
  - **`group.find_person` extracted rather than inlined.** AC6's message has to name the *stored*
    spelling of the person collided with, so the lookup had to return it; ADR-0005 point 5 says
    the same resolution applies wherever a person is named, so WI-0002 and WI-0004 need this
    function and would otherwise each write their own. It adds no behaviour beyond AC6.
  - **`storage.load` also rejects a `people` that is not a list of strings.** The plan named the
    other shape checks. Added because a record whose `people` held a number would otherwise reach
    `identity_key` and crash with a traceback, contradicting ADR-0001 point 3 — a refusal has to
    be a message, and this is the only place that can tell.
  - **Renamed the test helper from `run` to `run_cli`.** `unittest.TestCase.run` is what the
    framework calls to execute a test; defining a helper with that name would have replaced it.
    A name, not a behaviour, so renamed rather than escalated.
  - **Validate the name before checking membership**, which is the ordering `plan`'s own journal
    flagged as the one thing its steps implied but did not state. `add-person ","` therefore
    reports the reserved character rather than anything about the group. Recorded here because
    `plan` recorded noticing it.
  - **Measured the tests instead of trusting them.** Three deliberate mutations were made and
    reverted: exact-match `identity_key` (7 failures), `add_person` never saving (13 failures),
    and `display_name` collapsing internal whitespace like `identity_key` (**0 failures**). The
    third is the first risk `plan.md` names, and the suite as first written did not catch it —
    nothing distinguished the display rule from the identity rule on internal whitespace. Added
    `test_internal_whitespace_is_kept_in_the_stored_spelling`, confirmed it fails against that
    mutation, and left the finding in the implementation report rather than quietly fixing it.
  - **Escalated nothing, and there was nothing to escalate.** No decision here changes an
    interface another item depends on, contradicts an ADR, or decides user-visible behaviour no
    criterion covers — the criteria pin the exact text of every message, which is precisely what
    removes the temptation.
  - **Fixed nothing I noticed on the way, and filed no bug.** There is no prior delivered
    behaviour to have defects in; this is the project's first code.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0001` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 28 tests ... OK` (final run,
    on the branch head)
  - `python3 -m compileall -q expenses tests` → exit 0, no output
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 1
    commit(s) on main..wi/WI-0001 name WI-0001"
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - the eleven criteria run by hand as real commands against a temporary `EXPENSES_FILE`, output
    quoted in the implementation report
  - three mutation runs, each reverted → exit 1, exit 1, exit 0 (the last being the hole)
- **Gates:** all six, run on the branch head after the last code change.
  - `tests-pass` (hard) → **pass** — `python3 -m unittest discover -s tests -t . -q`, exit 0, 28
    tests.
  - `lint-clean` (hard) → **pass** — `python3 -m compileall -q expenses tests`, exit 0. Note what
    this gate does and does not mean here: `ADR-0008` records it as a syntax check, not a linter,
    because the stdlib-only constraint leaves no linter available. A green `lint-clean` on this
    project says every file parses and nothing more.
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-has-a-test` (hard) → **pass** — the table in `impl-report.md` names a test
    function for each of AC1–AC11 and for the head-of-list no-traceback clause. The mutation runs
    are the evidence that those tests would fail if the behaviour were removed, which is the part
    of this gate that a passing suite alone does not establish.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs`, exit 0.
  - `no-unplanned-scope` (advisory) → **pass** — every hunk traces to a plan step and a criterion.
    The three additions beyond the plan's interface list are named as deviations, each with the
    criterion or ADR that required it. Nothing was built for WI-0002 in advance: no `expenses` or
    `payments` key is written, because ADR-0007 point 2 makes adding them free later.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
  - branch `wi/WI-0001`, commits `main..wi/WI-0001` — `b05c034` (the package and the tests) plus
    the commit carrying this journal entry and the report
  - `expenses/__init__.py`, `expenses/__main__.py`, `expenses/storage.py`, `expenses/group.py`,
    `expenses/cli.py`
  - `tests/__init__.py`, `tests/support.py`, `tests/test_people.py`, `tests/test_duplicates.py`,
    `tests/test_invalid_names.py`, `tests/test_cli_surface.py`, `tests/test_persistence.py`
  - `tracker/items/WI-0001/item.md` — `branch: wi/WI-0001` set, per the procedure
- **Status:** `in-progress` → `verifying`
- **Result:** Both subcommands are built, stored in one JSON file, with 28 tests covering all
  eleven criteria and the corrupt-record behaviour ADR-0007 requires. The one thing `verify`
  should look at hardest is the display-versus-identity distinction: it is the item's stated risk,
  the suite initially missed it, and the test that now covers it was written after the hole was
  found rather than before.

## 2026-08-21T19:42:00Z — verify v0.1.0 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eleven criteria, **read first**, before the
    implementation report, so that the checks below were derived from what was asked for rather
    than from what was built
  - `tracker/items/WI-0001/history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`,
    `artifacts/refinement-qa.md`
  - `docs/architecture/adr/ADR-0001`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008`
  - the branch `wi/WI-0001` at commit **1c65c4f9cffe90192d598301f58474bd5f4d086b**, and the source
    of all five modules and all six test modules
- **Decisions:**
  - **Verified by running commands, not by reading the report.** Every row of the criteria table
    in `verify-report.md` is a command run during this execution with its captured output; none
    cites the implementation report. Where the two agree, they agree independently.
  - **Checked the exact bytes, not just the text.** AC1, AC2 and AC5 pin exact strings, so the
    first captures were taken through `od -c` and `cat -A`, and `wc -l` was used where a criterion
    says "exactly one line". A trailing-newline difference would otherwise have passed a visual
    comparison.
  - **Mutated once per criterion rather than once per item.** Eleven mutations, each attacking a
    different criterion, each applied to the real source, run against the whole suite, and
    reverted. All eleven were caught. This is the part of `every-criterion-independently-checked`
    that a passing suite cannot establish on its own: it says whether the tests would notice the
    behaviour disappearing.
  - **Two mutations were chosen because the record pointed at them.** `plan.md` names the
    display-versus-identity confusion as this item's first risk, and `impl-report.md` admits the
    suite as first written did not catch it. Both directions were mutated here — collapsing
    internal whitespace in `display_name`, and removing the case-folding from `identity_key` — and
    both are caught now. The developer's disclosure was confirmed rather than trusted.
  - **Exercised seven boundary probes no criterion requires**, because ADR-0007 point 5 makes
    claims that only a running command can settle: a record that is not JSON, one that is a JSON
    array, one whose `people` holds a number, one declaring a future format version, one carrying
    an unknown `expenses` key, `EXPENSES_FILE` pointing at a directory, and the `XDG_DATA_HOME`
    branch of the path resolution. None produced a traceback; none overwrote a file it could not
    read; the unknown key survived a save, which is ADR-0007 point 2's forward-compatibility claim
    demonstrated rather than assumed.
  - **Read the diff against the plan.** Every symbol in the five modules traces to a plan step or
    to one of the three deviations the implementation report declares. The only symbol I would add
    to that list is `storage.empty_record`, an internal helper of `load` that the plan's interface
    list does not name; it introduces no behaviour and is covered by AC5. Not a finding, recorded
    so the next reader does not have to re-derive it.
  - **No send-back and no bug filed.** Nothing failed. Had something failed, the classification
    would have been a send-back rather than a bug in every case available here: this item's own
    criteria cover all the behaviour that exists, because this item delivered all of it — there is
    no prior item whose delivered behaviour could be at fault.
  - **Recorded five things as not verified rather than passing them quietly**, the substantive two
    being the `~/.local/share` default (which cannot be exercised without writing to a real home
    directory) and the atomicity of the write (which would need the process killed mid-`save`).
    Both are argued in the report; neither is claimed as checked.
- **Questions raised:** none. No criterion was ambiguous — the exact-string wording `refine` pinned
  is what made every verdict a comparison rather than a judgement.
- **Commands:**
  - `git rev-parse HEAD` → `1c65c4f9cffe90192d598301f58474bd5f4d086b`, on `wi/WI-0001`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 28 tests ... OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - 24 `python3 -m expenses ...` invocations covering AC1 to AC11, each with its stdout, stderr and
    exit status captured; the outputs are quoted in `verify-report.md`
  - 7 boundary probes against hand-written record files
  - 11 mutation runs of the full suite, each reverted; exit 1 every time, with the failing test
    names recorded in the report
  - `git status --short` after the last revert → no modified tracked file; suite green again
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here, on the branch head, exit 0, 28 tests.
  - `lint-clean` (hard) → **pass** — exit 0, with the caveat ADR-0008 records: it is a syntax
    check, not a linter, so it says every file parses and nothing more. Noted in the report's
    `## Not verified, and why` so the gate's name cannot be read as stronger than the check.
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-independently-checked` (hard) → **pass** — twelve rows of commands and
    captured output, one per criterion plus the head-of-list no-traceback clause, none of them
    citing the implementation report; plus the eleven mutations that show the tests behind them
    are sensitive.
  - `negative-cases-exercised` (hard) → **pass** — all six refusal criteria triggered rather than
    read about (AC6 three spellings, AC7 three empty forms, AC8 both reserved characters, AC10
    three arity failures, AC11 both forms), and seven further boundary probes beyond them.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 1c65c4f9cffe90192d598301f58474bd5f4d086b`
  - `tracker/items/WI-0001/item.md` — AC1 to AC11 ticked, each after its row in the report existed
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0001 does what its criteria say. Eleven criteria checked by command, eleven
  mutations caught, seven boundary probes clean, and five gaps declared rather than glossed. The
  one thing `review-close` should weigh is what `lint-clean` actually covers on this project: it
  is a syntax check, and no style or dead-code check exists anywhere in the pipeline.

- **Gates (addendum, appended immediately after the entry above).** The entry listed five gates
  and omitted the sixth in `verify`'s contract by name:
  - `tests-would-fail-without-the-change` (advisory) → **pass** — eleven mutations, one per
    criterion, each applied to the real source, run against the whole suite, and reverted; all
    eleven caused failures, and the failing test names are tabulated in
    `artifacts/verify-report.md` § *Test sensitivity check*. The evidence was gathered and
    recorded under `**Decisions:**` and in the report, but the gate was not named in the list,
    which is the omission the journal format exists to prevent. Corrected here by appending rather
    than by editing the entry above.

## 2026-08-21T19:50:00Z — review-close v0.1.0 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next`.
- **Inputs read:**
  - the diff `main..wi/WI-0001` for `expenses/` — all five modules, hunk by hunk — and the six
    test modules, read for what they assert
  - `tracker/items/WI-0001/item.md`, `history.md` (ten rows), `journal.md` **in full** (eight
    entries plus the appended gate correction on `verify`'s), `artifacts/plan.md`,
    `artifacts/impl-report.md`, `artifacts/verify-report.md`, `artifacts/refinement-qa.md`
  - all four questions on the item, including their `## Consequences`
  - `ADR-0001`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008`,
    `docs/architecture/overview.md` (v1), `docs/product/prd.md` (v2), `docs/product/vision.md`
    (v3) — read against the code for D12, not from memory
  - `tracker/project.yaml`
- **Decisions:**
  - **Checked the record's mechanics before reading anything substantive**, because they are cheap
    and decisive: the history chains without a gap and its last row matched the item's status;
    eight journal entries account for every actor in ten rows (`intake` and `implement` each
    produced two rows from one execution); all eleven criteria are ticked; all four questions are
    answered with `## Consequences` naming real files.
  - **Ran `check-verify-freshness` rather than eyeballing the last commit.** The branch head
    (`d40ad609`) is not the verified commit (`1c65c4f9`), which is exactly the situation D10 exists
    for. The script reports that only the record moved, and I confirmed it independently:
    `git diff --name-only 1c65c4f..wi/WI-0001 -- expenses tests` is empty. Verification stands.
  - **Finding 1 — a false claim in two reports, corrected rather than propagated.**
    `impl-report.md` states the record file gets whatever permissions the umask allows, and
    explicitly that it is *not* mode 600; `verify-report.md` repeats it as "Confirmed by reading
    the code". Both are wrong. `tempfile.mkstemp` creates at `0600` regardless of umask and
    `os.replace` preserves the mode; I ran it under umask 0002 and `stat` reports `600`. The code
    is better than its record claims, so this is a defect in the record, not the change — and it is
    the exact shape `spec/dor-dod.md` D12 was added for, a claim re-quoted rather than re-checked.
    Stopped it at the second document: corrected in `review.md` and in the item's `## Notes`, with
    the two reports left as written because they are the evidence of what those executions
    believed. Rewriting them would destroy the only trace that this happened.
  - **Finding 2 — write failures traceback; accepted as a gap, not a rejection.** With the target
    directory unwritable, `add-person` exits non-zero but prints a traceback: `cli.main` catches
    `RuleError` and `RecordError`, and a `PermissionError` is neither. Classified as an accepted
    gap after checking both candidate routes and rejecting them. It is not a send-back, because no
    criterion of this item says anything about it and sending it back would mean retrofitting a
    twelfth criterion — the move this pipeline exists to prevent. It is not a question to the
    architect either, because nothing recorded is contradicted: `ADR-0001` point 3's no-traceback
    rule is written about refusals, with an unknown person, a duplicate and a malformed amount as
    its examples, and `ADR-0007` point 5 covers a record that cannot be *read*, not one that
    cannot be *written*. Recorded in the item's `## Notes` with a name on it: `storage.save` is
    inherited unchanged by WI-0002 and WI-0004, so **WI-0002's `plan` execution should decide the
    write-failure behaviour**. I could not file it as a bug item even had I wanted to —
    `pipeline.yaml` admits `null → ready` only for actor `verify` — which is itself worth noting
    as a limitation of the toolkit rather than of this item.
  - **Finding 3 — an ordering observation, recorded as not-a-defect.** `_add_person` loads the
    record before the name is validated, so a reserved-character name against a corrupt record
    reports the corrupt record. Both messages are true, the user cannot add anybody either way,
    and recording it stops the next reader mistaking it for a bug.
  - **Read the diff rather than the reports about it.** Every hunk traces to a plan step and a
    criterion. `storage.empty_record` is the only symbol absent from the plan's interface list —
    an internal helper of `load`, no behaviour — and `verify` had already flagged it. Nothing
    contradicts an ADR, and nothing was built ahead for WI-0002: no `expenses` or `payments` key
    is written, and the forward compatibility that makes adding them free later was demonstrated
    by probe rather than asserted.
  - **Re-ran the two claims in `docs/` that only a command can settle** — `ADR-0007` point 2's
    forward compatibility and point 3's path resolution — instead of reading them approvingly.
    That is what D12 asks for and it is the difference between checking a document and admiring
    it.
  - **Trial-merged before closing, and closed before merging.** The trial went into a throwaway
    `git worktree` on `main`; the project's test command passed on the merge result (28 tests,
    exit 0) and so did lint; the worktree was then removed. The item was closed while
    `wi/WI-0001` was still unmerged, because `check-commit-refs` inspects the commits on the
    branch that are not yet on the trunk and that range is empty once the merge lands.
  - **Left EP-001 open, deliberately.** WI-0002, WI-0003 and WI-0004 are all still at `draft`, so
    DE1 fails; the epic's Definition of Done was not applied and no epic-closing decision was
    made. Recorded on the epic's journal as well, so a reader of the epic can see why its first
    child closing did not close it.
  - **Corrected my own procedural slip.** I first set `status: done` by editing `item.md`
    directly; `validate-workspace` caught it (`history.tail-mismatch`), and I reverted the field
    and let the `transition` script make the move, which is the only sanctioned way. `outcome:
    delivered` and the `## Notes` additions are this skill's to write and were kept.
- **Questions raised:** none. Neither finding meets a condition in `spec/question.md` §4: nothing
  contradicts an ADR, nothing here is irreversible, and neither depends on intent no document
  records — the write-failure path is unspecified rather than contested, and it is named for the
  item whose planning will next touch that code.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0
  - `git diff --name-only 1c65c4f..wi/WI-0001 -- expenses tests` → empty
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 3
    commits name the item
  - `git worktree add /tmp/trial-merge main` → `git merge --no-edit wi/WI-0001` → clean
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0, 28 tests;
    `python3 -m compileall -q expenses tests` → exit 0
  - `git worktree remove --force /tmp/trial-merge` → trial discarded
  - `python3 -m expenses add-person Alice && stat -c '%a %n' "$EXPENSES_FILE"` → `600`, under
    umask 0002 (Finding 1)
  - `chmod 500 <dir>; EXPENSES_FILE=<dir>/sub/expenses.json python3 -m expenses add-person Bob` →
    exit 1 with a traceback (Finding 2)
  - re-ran AC4, AC6 and AC10 by hand to spot-check the verification's evidence → same output as
    the report records
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `git checkout main && git merge --no-ff wi/WI-0001` → after the close
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1 to D12 each with its own result and evidence, in
    `artifacts/review.md` § *Definition of Done*. D12 is the one that found something: the false
    permissions claim, which is in the tracker artifacts rather than in `docs/`, and which is
    corrected rather than carried forward.
  - `verification-postdates-the-code` (hard) → **pass** — `check-verify-freshness` exit 0, plus
    the independent `git diff --name-only` over `expenses/` and `tests/`, which is empty.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs` exit 0, run **before**
    the merge, while the range `main..wi/WI-0001` was still non-empty.
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 28 tests, exit 0, on the merged tree in a
    throwaway worktree, not on the branch.
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings, after the transition and
    the board regeneration.
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and
    `git log --grep WI-0001` alone a reader can answer all five of the questions
    `spec/journal-and-history.md` §3 asks: what was asked for and how the understanding changed
    (four questions, three of them answered by the person who wanted the tool, quoted verbatim in
    `refinement-qa.md`); which skill decided what (eight journal entries and ten history rows, and
    the two delegated decisions attributed to the architect rather than to the human); what was
    run and what it produced (every execution's `**Commands:**`); which gates passed and what
    happened next; and where the work stopped.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, the D1–D12 table, three
    findings, five accepted gaps, the verdict
  - `tracker/items/WI-0001/item.md` — `outcome: delivered`; `## Notes` extended with the four
    accepted gaps and the permissions correction
  - `tracker/items/EP-001/journal.md` — an entry recording that the epic stays open and why
  - the merge commit of `wi/WI-0001` into `main`
- **Status:** `in-review` → `done`
- **Result:** WI-0001 is delivered and merged: `add-person` and `people`, persisted in one JSON
  file, with eleven criteria verified by command and eleven mutations caught. Two findings, both
  recorded rather than fixed here — a false permissions claim that stops propagating at this
  review, and an unspecified write-failure path handed to WI-0002's planning. EP-001 stays open
  with three children still at `draft`.

- **Correction, appended immediately after the entry above.** The entry says the trial merge went
  into "a throwaway `git worktree`" and "the worktree was then removed", implying the trunk was
  untouched. That is not what happened, and the record must say so:
  - `git worktree add /tmp/trial-merge main` checked out the **real** `main` branch in the new
    worktree. A worktree shares the repository's refs, so the `git merge --no-edit wi/WI-0001` run
    inside it fast-forwarded `refs/heads/main` for real. Removing the worktree removed the working
    copy and left the moved ref behind.
  - The consequence surfaced immediately, at the gate that exists for it: `check-commit-refs`
    failed with "wi/WI-0001 is already merged into main, so main..wi/WI-0001 is empty… Rewind the
    merge, close, then merge." The close was refused rather than waved through.
  - Rewound with `git update-ref refs/heads/main d51bfd5` (the pre-merge commit, from
    `git reflog show main`), re-ran `check-commit-refs` → exit 0, then closed, then merged for
    real. Nothing was published in between and no commit was lost; the trial's *result* — 28 tests
    green on the merged tree — was genuine and stands.
  - Two things worth recording for whoever maintains the toolkit. First, `review-close`'s step 8
    says to trial-merge into "a throwaway copy of the trunk"; a worktree on the trunk branch is
    not that, and the safe forms are a detached checkout (`git worktree add --detach`) or a
    scratch branch. Second, the gate caught it, which is the system working — but it caught it one
    step later than it could have.
  - A second, smaller one from the same execution: `outcome: delivered` cannot be set before the
    transition, because `transition` runs `validate-workspace` first and the validator rejects an
    outcome on an item that is not yet `done` (`item.outcome.premature`); nor can it be omitted
    afterwards, because the same validator then reports `item.outcome.missing`. The only order
    that works is transition first, outcome second, which no procedure states.
