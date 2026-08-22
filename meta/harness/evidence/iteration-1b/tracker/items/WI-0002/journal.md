# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T18:52:10Z — intake v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly; created by this execution of `intake` as a child of EP-001
- **Inputs read:**
  - the stated idea, verbatim (quoted in full in EP-001's entry for this execution)
  - `tracker/items/` — empty, so this item took the next free `WI-` number
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/dor-dod.md`
- **Decisions:** see EP-001's entry for this execution for how the work was split and why this
  item is one of the parts. Listing expenses back is part of this item rather than a fourth one, because an expense you cannot read back is not observable. `depends-on: WI-0001` is recorded because an expense names people who must already exist.
- **Questions raised:** `Q-001` (blocking, to human) — equal splits only, or explicit unequal shares? `Q-002` (blocking, to human) — how are leftover pennies assigned when a split does not divide evenly? Both change what "shared by" means, so the criteria cannot be made decidable until they are answered. Neither has been answered.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0002 ... --status draft` -> exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to awaiting-answer --resume-to draft ...` -> exit 0
- **Gates:** the four gates of `intake` are execution-wide and are recorded once, with their
  evidence, in EP-001's entry for this execution: `workspace-valid` **pass**,
  `epic-has-success-measures` **pass**, `items-are-separable` **pass** (this item's place in the
  order and its `depends-on` are stated there), `no-solution-in-the-problem` **pass**.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/journal.md`, `tracker/items/WI-0002/history.md` (new)
  - `tracker/items/WI-0002/questions/Q-001.md`, `questions/Q-002.md` (new, both open)
- **Status:** `—` -> `draft` -> `awaiting-answer` (resume-to `draft`)
- **Result:** WI-0002 exists but is suspended behind two blocking questions addressed to the human. No further work may be done on it until they are answered and propagated.

## 2026-08-21T18:58:00Z — answer-questions v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer`, with `Q-001` and `Q-002` both open, both addressed to
  `human`, and both carrying a `## Answer` written by the human since the previous turn. Handled
  together, as the skill requires: they are the same subject seen twice, and answering one without
  the other would have left the item suspended anyway.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` — context, options, recommendations,
    and the human's answers
  - `tracker/items/WI-0002/item.md`, `history.md` (the suspending row records `resume-to: draft`),
    `journal.md` (intake's entry)
  - `tracker/items/WI-0003/item.md` — AC4 is the criterion `Q-002`'s context says depends on the
    rounding rule, so it was read before deciding, not after
  - `tracker/items/WI-0004/item.md` — payments carry amounts too
  - `tracker/items/EP-001/item.md`, `docs/product/vision.md` (v2)
  - `docs/architecture/adr/ADR-0001-one-shot-subcommands.md` (v1) — the refusal contract the new
    criteria are written against
  - `.claude/agile-skills/spec/question.md` §4, `doc-header.md` §4, `work-item.md` §2
- **Decisions:**
  - **`Q-001`: recorded the human as having answered the requirement, and myself as having decided
    its shape.** They said the tool must handle both equal and unequal splits, which excludes the
    question's option A outright. They did not choose between the two ways to do that, and the
    question's own option B — every sharer carries an amount as soon as any of them does — is worse
    than option A for the case they described: recording "Bob only had a starter" would mean
    computing and typing everyone else's share by hand, which is the arithmetic the tool exists to
    do, and it contradicts "usually equal". So `ADR-0002` takes the mixed form, and `answered-by` on
    that question stays `human` because the requirement is theirs.
  - **Wrote the invalidity rules into the ADR rather than leaving them to `refine`.** The mixed form
    admits two failures equal-only did not — stated amounts that overshoot the total, and that
    undershoot it with nobody left to take the remainder. A validity rule discovered during
    implementation is a question filed mid-flight; discovered now, it is two acceptance criteria.
  - **Accepted two edge cases rather than refusing them, and said so in the ADR.** The payer need
    not be a sharer — someone can pay for a meal they did not eat. And stated amounts that already
    exhaust the total leave the remaining sharers owing zero, which is the general rule with a
    remainder of zero rather than a special case; the zero share is visible in AC4's listing, so it
    is not silent.
  - **`Q-002`: read "go ahead anyway, we'll decide later" as a deferral with a condition, and
    decided accordingly.** "Go ahead" is an instruction to proceed, so escalating again would be
    ignoring an answer. "Decide later" is a constraint on *how*: whatever is chosen has to stay
    cheap to change. That is why `ADR-0003` records, as part of the decision, that shares are
    derived on every run and never stored — with no derived figure persisted, superseding the rule
    changes one function and no data.
  - **Settled the representation before the rounding rule, which none of the question's options
    named.** "Two decimal places" is meaningless without a fixed precision, and doing this in binary
    floating point would make the reconciliation guarantee false for reasons unrelated to the rule
    (`0.1 + 0.2 != 0.3`). `ADR-0003` therefore fixes whole minor units and integer arithmetic first.
    This is a wider decision than the question asked for; it is recorded as such, and it is the one
    part of `ADR-0003` that is deliberately not cheap to reverse.
  - **Refused extra precision on entry rather than rounding it.** `12.505` is a typo, and silently
    rounding a typo is how a ledger stops being trusted.
  - **Strengthened WI-0003 AC4 rather than weakening it.** `Q-002`'s context said the criterion is
    either true by construction or false by a penny depending on this rule. Option A makes it true
    by construction, so AC4 now says "exactly, not to within a penny" and gives the reason. This is
    an amendment to another item's acceptance criterion by `answer-questions` propagating an answer,
    which `spec/work-item.md` §2 permits and requires to be journalled; it is journalled here and on
    WI-0003, and it tightens the criterion rather than loosening it.
  - **Extended WI-0002 AC4 to require each sharer's derived share in the listing.** Under
    `ADR-0002` a mis-typed explicit amount is otherwise invisible until the group settles up, which
    is the worst possible moment to discover it.
  - **Left the concrete syntax to `refine`**, consistent with `ADR-0001`. Deciding here how a sharer
    and an amount are written on a command line would put this item's detail in a document it does
    not own.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 1 warning
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to draft --actor answer-questions
    --reason "..."` -> recorded under Gates
  - `python3 .claude/agile-skills/scripts/board-gen .` -> exit 0
- **Gates:**
  - `answer-is-propagated` (hard) -> **pass** — every path in both `## Consequences` sections was
    reopened after writing. `ADR-0002` and `ADR-0003` exist at v1 with options, decisions and
    reversibility. `WI-0002/item.md` now carries AC5, AC6 and AC7, the amended AC1 and AC4, and a
    `## Notes` section that records both decisions instead of two open questions.
    `WI-0003/item.md` AC4 reads "exactly, not to within a penny" and its notes cite ADR-0003.
    `WI-0004/item.md` AC1 carries the amount rules and its notes cite ADR-0003.
  - `answered-from-the-record` (hard) -> **pass** — `Q-001`'s requirement is the human's own words,
    quoted; its shape and the whole of `Q-002` were silent in the record and are recorded as
    `ADR-0002` and `ADR-0003`, both cited from the answers. Nothing is asserted without a document
    behind it.
  - `escalation-is-justified` (hard) -> **not applicable, nothing escalated.** Worth stating why
    `Q-002` was not sent back: "not sure yet" looks like the fourth condition in
    `spec/question.md` §4 — a genuinely silent record where any choice has material consequences —
    but the human read the options and told the tool to proceed. Re-asking a question they have
    just declined to answer is not escalation, it is a loop.
  - `workspace-valid` (hard) -> **pass** — `validate-workspace .` exit 0, one pre-existing warning
    about the null test command, which `plan` owns.
  - `item-resumed-correctly` (hard) -> **pass** — the suspending row of 2026-08-21T18:46:03Z
    records `resume-to: draft`; this execution transitioned the item to `draft`. Read from the row.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — answered; `answered-by: human`
  - `tracker/items/WI-0002/questions/Q-002.md` — answered; `answered-by: answer-questions`
  - `docs/architecture/adr/ADR-0002-share-model.md` — new, v1
  - `docs/architecture/adr/ADR-0003-money-and-rounding.md` — new, v1
  - `tracker/items/WI-0002/item.md` — AC1 and AC4 amended, AC5/AC6/AC7 added, `## Notes` rewritten
  - `tracker/items/WI-0003/item.md` — AC4 strengthened, `## Notes` extended
  - `tracker/items/WI-0004/item.md` — AC1 extended, `## Notes` extended
- **Status:** `awaiting-answer` -> `draft`
- **Result:** How an expense is split, and how the pennies fall when it does not divide evenly, are
  both decided and written down. WI-0002 is back at `draft` with no open question and seven
  criteria for `refine` to pin syntax onto.

## 2026-08-21T19:56:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` once WI-0001 reached `done` and this item's
  `depends-on` was satisfied. A fresh refinement, not a send-back: the history's last row is
  `awaiting-answer → draft` by `answer-questions`, and this item has never been past `draft`.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md` (two entries: `intake` and
    `answer-questions`), `questions/Q-001.md` and `Q-002.md` with the human's answers
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`
  - `docs/product/prd.md` (v2), `docs/product/vision.md` (v3),
    `docs/architecture/overview.md` (v1)
  - `tracker/items/WI-0001/item.md` and `artifacts/review.md` — the sibling that just closed, for
    the criteria style it settled on and for the gap its review handed forward
  - `tracker/items/WI-0003/item.md`, `WI-0004/item.md` — to check no sibling already owns part of
    this scope; WI-0003 owns balances, which is why AC1 to AC14 stop at listing shares
- **Decisions:**
  - **Pinned the argument syntax**, which is what this item was left owing:
    `add-expense <total> --paid-by <name> --shared-by <name>[=<amount>][,…]`. The total is
    positional because every expense has one; the two names are flagged because two bare names in
    a row are ambiguous. The `,` and `=` forms were not free choices — `ADR-0005` point 2 reserves
    those two characters in a name precisely so that `ADR-0002`'s list-with-optional-amounts fits
    on one line.
  - **Rejected an optional `--shared-by` defaulting to everybody.** The original idea's "shared by
    some or all" would have supported it and it would save typing on the commonest case. Rejected
    because a default that silently includes somebody is a mistake this epic cannot repair: there
    is no command to edit or delete an expense and none to remove a person. Recorded in the Q&A
    as considered and rejected rather than left unmentioned, because it is the kind of thing the
    human might overturn and they should be able to see it was weighed.
  - **Rewrote all seven criteria and grew them to fourteen.** The old set named observable
    outcomes with no command to type. The split: AC1 to AC4 are the happy path and the listing
    format; AC5, AC6 and AC7 are `ADR-0002` and `ADR-0003` worked through concrete examples; AC8
    to AC12 are the five families of refusal, each with its exact message; AC13 asserts that no
    refusal records anything; AC14 asserts this item does not disturb WI-0001's data.
  - **Wrote the rounding rule as three worked examples rather than as prose**, because the rule
    has a subtlety that prose hides: the payer takes the odd penny *even when a sharer was named
    first*, and in the mixed form only the sharers without a stated share divide the remainder.
    The third example (`10.01` shared by Alice, Bob and Carol=1, paid by Bob → Alice 4.50,
    Bob 4.51, Carol 1.00) exists to pin exactly that; the first draft of it used a total that
    divided evenly and would have demonstrated nothing, which is worth recording as the near-miss
    it was.
  - **Added AC14, which no earlier item needed.** This is the first item to build on delivered
    behaviour, and "the new feature quietly corrupts the old one" is not covered by any of its own
    other criteria. Cheap to state now, invisible if left out.
  - **Answered the description question from the record rather than escalating it.** "What was
    this expense for?" is the single thing a reader is most likely to assume is here.
    `docs/product/prd.md` (v2) enumerates an expense as an amount, one payer and one or more
    sharers, and says "Nothing else", so the record settles it — and the honest place for it is
    `## Out of scope`, with the document cited, not a question that re-asks something already
    written down. The consequence is stated plainly there: `expenses` output distinguishes two
    dinners only by number, amount and people.
  - **Left the write-failure behaviour to `plan`.** WI-0001's review closed with it as an accepted
    gap and named this item's planning as where to settle it. Turning it into a criterion here
    would be `refine` deciding an architecture question in the item's name; recording it under
    `## Notes` as a decision `plan` owes keeps it visible without pretending it is a requirement.
  - **Filed nothing to the human.** Both of their answers were already on file; what remained was
    syntax and wording, which they have twice declined to be asked about. Every such choice is
    `[assumed]` in the Q&A and repeated in `## Notes`, marked as unconfirmed.
- **Questions raised:** none new. Two (`Q-001`, `Q-002`) were raised by `intake` and are answered;
  the full exchange is at `artifacts/refinement-qa.md`, where four further answers are recorded
  `[assumed]` (Q3 to Q6), one answered from the record (Q7, the description field), and one left
  `[unresolved]` by design (Q8, write failures — `plan`'s to decide).
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to ready --actor refine` → exit 0
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0.
  - `definition-of-ready` (hard) → **pass**, criterion by criterion:
    - **R1** frontmatter complete [auto] → **pass**: validator clean; `type`, `epic`, `priority`
      set; `depends-on: WI-0001`.
    - **R2** story names role, capability, outcome [skill] → **pass**: "As someone who has just
      paid for something on behalf of part of the group … so that the cost is captured at the
      moment it happened rather than reconstructed from memory later."
    - **R3** labelled checkbox criteria [auto] → **pass**: AC1–AC14.
    - **R4** every criterion decidable by observation [skill] → **fail on entry** — all seven
      criteria named an outcome but no command, and AC4 said "showing at least" the amount, payer
      and sharers, which no two verifiers would read the same way. Rewrote every one against the
      pinned syntax, gave the listing an exact line format, and pinned the text of eighteen
      messages → **pass**.
    - **R5** out-of-scope names something a reader would assume included [skill] → **fail on
      entry** (three entries, all obvious) → **pass**: five entries, including the description
      field, with `prd.md` v2 cited as what excludes it.
    - **R6** every open question non-blocking [auto] → **pass**: both are `answered`.
    - **R7** independently deliverable [auto] → **pass**: `depends-on: WI-0001`, which is `done`
      and merged into `main`.
    - **R8** Q&A recorded verbatim [auto] → **fail on entry** (no such file) → **pass**:
      `artifacts/refinement-qa.md`, with both of the human's answers quoted exactly.
    - **R9** one coherent change [skill] → **pass**: record an expense, derive its shares, list
      them back. The write side and the read side are each unobservable without the other, and
      balances are explicitly WI-0003's.
    - **R10** every combination stated, excluded, or recorded as unconstrained [skill] → **fail on
      entry** — the old criteria said nothing about a duplicate sharer, a malformed list, a
      repeated flag, or an empty listing → **pass**: AC5 to AC14 state every case the two
      subcommands introduce, and `## Notes` names the three things left open (the stored JSON
      shape of an expense, write-failure behaviour, and the fact that a future rounding change
      will restate past expenses) with `refine` recorded as the one who left them.
  - `criteria-are-decidable` (hard) → **pass**. Every criterion is settled by running one command
    line and comparing captured stdout or stderr against a string given in the criterion, plus an
    exit status. The three that are not single commands — AC2 (persistence), AC13 (nothing
    recorded on refusal), AC14 (WI-0001's data undisturbed) — each name the second command whose
    output settles them.
  - `qa-recorded-verbatim` (hard) → **pass** — `artifacts/refinement-qa.md` reproduces both filed
    questions with the reason each was asked and the human's answer word for word, including
    "Not sure yet — go ahead anyway, we'll decide later", which is recorded as the hedged answer
    it was rather than tidied into a decision. The six answers decided here are tagged `[assumed]`
    or `[unresolved]` and stated to be unconfirmed.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0002/item.md` — criteria rewritten and extended from seven to fourteen;
    the argument syntax pinned at the head of the list; `## Out of scope` widened from three
    entries to five; `## Notes` restructured into what was decided, what was assumed without the
    human, and what is deliberately unconstrained
- **Status:** `draft` → `ready`
- **Result:** WI-0002 meets the Definition of Ready on all ten criteria, with no override. The
  syntax `ADR-0001`, `ADR-0002` and `ADR-0006` all deferred to this item is pinned, and every
  criterion is now a command line, an expected output and an exit status. `plan` inherits two
  things it must decide rather than assume: the stored shape of an expense, and what happens when
  a write fails.

## 2026-08-21T20:02:00Z — plan v0.1.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next`. Not a re-plan: this item has never been past
  `ready`, and its history carries no send-back.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC14 and the pinned syntax), `history.md`,
    `artifacts/refinement-qa.md` — in particular Q3 to Q6 tagged `[assumed]` and Q8 left
    `[unresolved]`, which named this execution as the owner of the write-failure decision
  - `docs/architecture/overview.md` (v1), `docs/product/prd.md` (v2), `docs/product/vision.md` (v3)
  - every ADR: `ADR-0001` through `ADR-0008`
  - `tracker/items/WI-0001/artifacts/review.md` — the accepted gap it handed forward, and
    `artifacts/plan.md` for the shape this item has to fit
  - **the code that exists**: `expenses/cli.py`, `group.py`, `storage.py`, `__main__.py`, and
    `tests/support.py` — the last because this item reuses its `CliTestCase` unchanged
  - `tracker/project.yaml` — both commands already filled in by WI-0001's planning; nothing here
    changes them
- **Decisions:**
  - **The stored shape of an expense, `ADR-0009` (route: decided; `ADR-0007` left the key open and
    `refine` named this execution).** Total, payer, and an ordered list of shares each with a
    person and an optional stated amount — the entry, transcribed. Three earlier decisions
    removed most of the design space before the options were weighed: integers not floats,
    nothing derived is stored, and named order is an *input to the arithmetic* rather than
    presentation, because `ADR-0003` point 3 orders the remainder by it. The option worth naming
    is the one rejected: storing the derived shares alongside the entry would make this item and
    WI-0003 trivial and would silently cost the group the thing the human explicitly reserved
    when they said "we'll decide later" about rounding.
  - **Store the stored spelling of a person, not their identity key.** Rejected the key because
    nothing in this epic renames anybody, so the spelling cannot go stale, and the indirection
    would make the file harder to read by hand — which is the property `ADR-0007` picked JSON
    for. Recorded in `ADR-0009` with its cost: a future rename command must rewrite expenses too.
  - **A failed write is a stated message, `ADR-0010` (route: decided, on a gap handed forward).**
    `cli.main` catches `OSError` alongside the two existing exception types and reports
    `Cannot save to <path>: <reason>.` Explicitly **not** `Exception`: a `TypeError` in the split
    arithmetic must still crash loudly, because a bug reported as a polite refusal is a bug
    nobody finds — and it is exactly the class of error `verify` is hunting. This changes
    behaviour WI-0001 delivered, deliberately, on the authority of WI-0001's review.
  - **Declared that `ADR-0010`'s branch is unverifiable here rather than quietly building it.**
    No criterion on WI-0002 exercises a write failure and `plan` may not write criteria. So the
    change lands inside the refusal handling AC13 *does* exercise, and the gap is stated in the
    ADR and again in `plan.md` § *Risks*, so `verify` records it under "not verified" instead of
    finding it, and `review-close` sees a known gap rather than unrequested scope.
  - **A fourth module, `money.py` (route: reversible structure decision, recorded in the
    overview).** Turning `12.5` into `1250` is neither command-line syntax nor a group rule, and
    both `cli.py` and `group.py` need it. It judges precision but deliberately not sign or
    magnitude: "more than zero" is a rule about an *expense*, and it belongs with the message the
    criteria pin for it.
  - **Split the sharer-list work between two layers on a stated line.** `cli.py` owns syntax —
    splitting on the two characters `ADR-0005` reserves and rejecting `Bob=`, `Alice=1=2` and an
    empty element; `group.py` owns meaning — membership, duplicates by identity key, and whether
    the stated shares can work against the total. Written into `overview.md` v2 because it is the
    one place in this item where two layers could each plausibly own the work, and a reader
    should not have to re-derive which.
  - **Kept `argparse` out, continuing WI-0001's assumption for the same reason** and recording it
    again as an assumption rather than promoting it to an ADR: the criteria pin
    `Unknown option: --split-by.` and `--paid-by was given more than once.`, and reversing the
    decision is a rewrite of `cli.py` alone.
  - **Did not design past the item.** No expense identifier, no edit or delete, no description
    field, nothing that sums across expenses — `shares_of` is the function WI-0003 will build on
    and it is needed by AC3 today. Every step maps to at least one criterion; the only line that
    does not is `ADR-0010`'s `OSError`, and it is declared as such.
  - **Asked the human nothing.** Both of their answers on this item are on file and propagated
    into `ADR-0002` and `ADR-0003`; the two decisions this execution made are reversible (the
    write-failure catch trivially, the stored shape by migration) and neither turns on intent no
    document records.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to planned --actor plan` → exit 0
  - no test run: this execution wrote no code. The commands `ADR-0008` records were exercised
    when they were chosen, during WI-0001's planning, and `implement` runs them on the branch.
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table in `plan.md` has one row
    per criterion, AC1 to AC14, each naming the step that satisfies it and the specific assertion
    that will demonstrate it, down to the exact expected string. No row says "tests".
  - `project-commands-resolved` (hard) → **pass** — `commands.test` and `commands.lint` are the
    ones `ADR-0008` recorded and WI-0001 exercised; both were run against a deliberate failure at
    that time. Nothing about them changes here, and `commands.build` stays null because there is
    still nothing to build.
  - `decisions-recorded` (hard) → **pass** — two new ADRs (`ADR-0009`, `ADR-0010`), one document
    change (`overview.md` v2 for the module shape and the syntax-versus-meaning line), five ADRs
    cited rather than re-decided (`ADR-0002`, `ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`), and
    three entries under `## Assumptions` each with its reversal cost. The third assumption — a
    stated `0` is stored as `0` rather than omitted — is flagged there as the one that is *not*
    free to reverse, which is why it is also in the ADR.
  - `plan-is-executable-without-you` (advisory) → **pass, with one soft spot.** Every step names
    its files and the interface it must expose. Read cold, the place a developer still has to
    think is the exact ordering inside `shares_of`: `ADR-0003` point 3 composes three conditions
    — only the unstated sharers divide the remainder, the payer comes first if he is one of them,
    the rest follow in named order — and the plan states them rather than sequencing them. That
    is deliberate; sequencing them would be writing the function. AC7's third example is the test
    that catches getting it wrong, and `## Risks` says so.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — 7 steps, a 14-row mapping table, 3
    assumptions with reversal costs, 5 risks, and what is out of scope
  - `docs/architecture/adr/ADR-0009-stored-shape-of-an-expense.md` (new, v1)
  - `docs/architecture/adr/ADR-0010-failing-to-write-the-record-is-a-stated-message.md` (new, v1)
  - `docs/architecture/overview.md` — v1 → v2
- **Status:** `ready` → `planned`
- **Result:** WI-0002 has a plan whose every step maps to a criterion, and the two things `refine`
  and WI-0001's review left for this execution are decided and recorded rather than deferred
  again. The two things most likely to go wrong are named in `## Risks`: the three-condition
  remainder ordering, and the fact that `ADR-0010`'s new error path has no criterion behind it.

## 2026-08-21T20:14:00Z — implement v0.1.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`. Fresh start: `git branch --list 'wi/*'`
  showed only `wi/WI-0001`, and the history's last row was `ready → planned` by `plan`. Nothing to
  reconcile with.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (AC1–AC14 and the pinned syntax), `artifacts/plan.md`,
    `history.md`, `questions/Q-001.md` and `Q-002.md` — both `answered` well before `plan` ran, so
    nothing moved since the last journal entry and nothing needed re-reading out of them
  - `docs/architecture/overview.md` (v2), `ADR-0001` to `ADR-0010`
  - the existing source: `expenses/cli.py`, `group.py`, `storage.py`, `__main__.py`,
    `tests/support.py`, and WI-0001's test modules, to see which of them this item would disturb
  - `tracker/project.yaml`
- **Decisions:**
  - **Moved `RuleError` into a new `expenses/errors.py`.** The plan's interfaces are circular as
    written: `money.parse_amount` raises `group.RuleError` and `group.add_expense` calls
    `money.parse_amount`, so importing `group` imports `money`, which imports a half-built
    `group`. Three fixes were available — a function-local import in `money`, defining the
    exception in `money` and having `group` take it from there, or a third module both import.
    Chose the third: it is the only one where every name the plan uses keeps working
    (`group.RuleError` still resolves, via a re-export) and no import runs at a surprising time.
    This is *how*, not *what*, so it is a deviation and not a question.
  - **Added `ExpenseTestCase` to `tests/support.py`** rather than repeating a four-person setup in
    four modules. `CliTestCase` is untouched, so WI-0001's tests use exactly what they used
    before.
  - **Refused two malformed command lines the criteria do not mention** — `--paid-by` with no
    value, and `add-expense` with two positionals. Both would otherwise be an `IndexError` or a
    silently-ignored argument. Judged inside the plan's latitude rather than a question, because
    neither changes an interface, contradicts an ADR, or is expensive to reverse — but both are
    user-visible with no criterion behind them, so both are named in the implementation report
    and flagged for `verify` to record as unverified rather than as passing. That is the
    disclosure the "guessing instead of asking" trap is really about.
  - **Hardened `storage._is_expense` slightly beyond the plan's field list**: an empty `shares`
    list is rejected because `ADR-0002` requires at least one sharer, and `bool` is rejected where
    an `int` is wanted because in Python `True` passes `isinstance(x, int)` and would become a
    total of one penny.
  - **Wrote `shares_of` so the three conditions of `ADR-0003` point 3 are visible separately** —
    which sharers divide the remainder, the payer-first ordering, and the stable named order —
    because `plan.md` § *Risks* named exactly this as the item's easiest thing to get subtly
    wrong. `sorted` is used for the payer-first pass precisely because Python's sort is stable, so
    the named order survives underneath it.
  - **Measured the tests with seventeen mutations rather than trusting a green suite.** All
    seventeen were caught. The one worth reporting is that the payer-first ordering is caught by
    exactly **one** test — the AC7 example `refine` had to correct while writing it, and which
    `plan` predicted would be the only thing standing there. The report says so rather than
    quoting the reassuring aggregate.
  - **Escalated nothing.** Every decision above is one file to reverse, none contradicts an ADR,
    and the two behaviours no criterion covers are declared rather than smuggled.
  - **Fixed nothing I noticed on the way, and filed no bug.** WI-0001's delivered behaviour
    changed in exactly one respect — `OSError` is now reported instead of raised — and that is
    `ADR-0010`, decided by `plan` on WI-0001's review's instruction, not a tidy-up.
- **Questions raised:** none.
- **Commands:**
  - `git checkout -b wi/WI-0002` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 79 tests ... OK` (final run, on
    the branch head). Intermediate runs after each plan step: 7, 10, 5 and 24 tests respectively,
    all passing before the next step began
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - the AC1, AC3 and AC14 command lines run by hand against a temporary `EXPENSES_FILE` before any
    test was written, to see the output before asserting on it
  - `python3 /tmp/mutate2.py` — seventeen mutation runs, each reverted; `git status` afterwards
    shows no unintended modification
- **Gates:** all six, on the branch head after the last code change.
  - `tests-pass` (hard) → **pass** — 79 tests, exit 0.
  - `lint-clean` (hard) → **pass** — `compileall`, exit 0, with the standing caveat from
    `ADR-0008` that this is a syntax check and not a linter.
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-has-a-test` (hard) → **pass** — `impl-report.md` names a test function for
    each of AC1 to AC14. The seventeen mutations are the part of this gate a passing suite cannot
    establish: each removed one behaviour and each was caught.
  - `commits-reference-the-item` (hard) → **pass** — `check-commit-refs`, exit 0.
  - `no-unplanned-scope` (advisory) → **pass, with disclosure** — every hunk traces to a plan step
    and a criterion except five declared deviations and the `OSError` branch the plan itself
    declared in advance. Nothing was built for WI-0003 or WI-0004: no balance, no netting, no
    `payments` key.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` (new)
  - branch `wi/WI-0002`, commit `main..wi/WI-0002` — the code and tests, plus the commit carrying
    this entry and the report
  - `expenses/money.py`, `expenses/errors.py` (new); `expenses/group.py`, `expenses/storage.py`,
    `expenses/cli.py` (changed)
  - `tests/test_money.py`, `test_add_expense.py`, `test_expenses_listing.py`,
    `test_expense_refusals.py` (new); `tests/support.py`, `tests/test_persistence.py` (changed)
  - `tracker/items/WI-0002/item.md` — `branch: wi/WI-0002` set
- **Status:** `in-progress` → `verifying`
- **Result:** Both subcommands are built, with 79 tests covering all fourteen criteria and
  seventeen mutations confirming they bite. Three behaviours have no criterion behind them —
  `ADR-0010`'s write-failure message and two malformed command lines — and all three are named in
  the report so `verify` records them as unverified rather than discovering them.

## 2026-08-21T20:24:00Z — verify v0.1.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next`.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen criteria, **read first**, before the
    implementation report, so the checks test what was asked for rather than what was built
  - `history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/refinement-qa.md`
  - `ADR-0001` to `ADR-0010`, `docs/architecture/overview.md` (v2)
  - the branch `wi/WI-0002` at commit **10a6bc3948881181afc41c5d2b2c2b924f30ec86**, and the source
    of `money.py`, `errors.py`, `group.py`, `storage.py`, `cli.py` and every test module
- **Decisions:**
  - **Derived each check from its criterion and ran it**, rather than confirming the report.
    Fourteen criteria, roughly fifty `python3 -m expenses` invocations, each with stdout, stderr
    and exit status captured; the first few compared with `cat -A` so that a trailing-newline
    difference could not pass as a match.
  - **Read the stored file directly** after AC2 and checked it against `ADR-0009` field by field.
    That is the only way to confirm `ADR-0003` point 6 — that no derived share is stored — since
    no criterion prints the file, and it is the property the human's "we'll decide later" rests
    on.
  - **Chose fifteen mutations that attack different code paths from the seventeen in the
    implementation report**, deliberately: reversing the listing order, changing the sharer
    separator, halving a stated share, giving the odd penny to the *last* unstated sharer,
    sorting `people` on save. Repeating the developer's mutations would have measured their
    imagination rather than the suite.
  - **Reported the two survivors rather than the reassuring aggregate.** Saving the loaded record
    before validating, and saving in a `finally` when `add_expense` raises, both failed no test.
    Rather than record that as a coverage hole or wave it away, I established *why*: the append
    is the last thing `add_expense` does, so in both mutants the record saved is the record read.
    Then I confirmed the real property with a sharper mutation — appending the expense **before**
    the two sum checks, which does record an invalid expense — and it was caught by 13 tests. So
    AC13 is genuinely covered, and the survivors are behaviour-preserving.
  - **Found one gap in the criteria, not in the code.** The one observable a survivor would change
    is that a refusal would create the record file where none existed. WI-0001 pins that for
    `add-person`; nothing pins it for `add-expense`. The behaviour today is correct — I checked —
    but nothing would catch it changing. Recorded as a finding rather than sent back, because no
    criterion of this item says otherwise.
  - **Did not send back `shared by 1 people.`** AC5's case prints that, and it is the one piece of
    output here a user would call wrong. AC1 pins the sentence only for its own three-sharer case,
    so no criterion is violated, and sending it back would mean verification inventing a target
    after the fact — the precise failure this skill's second warning describes. It is a finding
    for `review-close` to weigh.
  - **Filed no bug item.** All three findings are behaviour *this* item delivered, so the
    classification test in step 7 routes none of them to a bug: a bug is for behaviour another
    item delivered, and a send-back is for this item's own criteria failing. Neither applies to
    behaviour no criterion covers, which is why all three are in the report and in the journal
    instead.
  - **Exercised the three behaviours the implementation report declared as uncovered** — the
    `OSError` message, `--paid-by` with no value, two positionals — so that `review-close` has
    their actual output rather than a promise. All three behave sensibly; none is claimed as a
    passing criterion.
- **Questions raised:** none. No criterion was ambiguous — `refine` pinned eighteen exact strings,
  so every verdict was a comparison rather than a judgement.
- **Commands:**
  - `git rev-parse HEAD` → `10a6bc3948881181afc41c5d2b2c2b924f30ec86` on `wi/WI-0002`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 79 tests ... OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - ~50 `python3 -m expenses …` invocations covering AC1 to AC14, quoted in `verify-report.md`
  - 9 boundary probes, including four hand-written corrupt records, a `999999999.99` split and a
    `0.01` split three ways
  - `cat "$EXPENSES_FILE"` after AC2 — the stored shape, checked against `ADR-0009`
  - 15 mutation runs, each reverted, plus 2 sharper follow-ups on AC13; `git status -- expenses
    tests` clean afterwards and the suite green
- **Gates:**
  - `tests-pass` (hard) → **pass** — run here on the branch head, 79 tests, exit 0.
  - `lint-clean` (hard) → **pass** — exit 0, with the standing `ADR-0008` caveat that it is a
    syntax check; recorded again under *Not verified* because two new modules went through this
    item with no style or dead-code check anywhere in the pipeline.
  - `workspace-valid` (hard) → **pass** — exit 0, no errors, no warnings.
  - `every-criterion-independently-checked` (hard) → **pass** — fourteen rows of commands and
    captured output, none citing the implementation report.
  - `negative-cases-exercised` (hard) → **pass** — every refusal criterion triggered: AC8 three
    cases, AC9 six, AC10 two refusals and one acceptance, AC11 six, AC12 six, AC13 twenty in
    sequence against a record that already held expenses, plus nine further probes.
  - `tests-would-fail-without-the-change` (advisory) → **pass, with two documented survivors** —
    fifteen mutations, thirteen caught; the two survivors analysed above and shown to be
    behaviour-preserving, with a sharper mutation confirming the property they appeared to
    threaten.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 10a6bc3948881181afc41c5d2b2c2b924f30ec86`
  - `tracker/items/WI-0002/item.md` — AC1 to AC14 ticked, each after its row in the report existed
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 does what its fourteen criteria say, checked by command. Three findings for
  `review-close` to weigh, none a criterion failure: `shared by 1 people.`, an unpinned
  "a refusal creates no file" for `add-expense`, and two command-line behaviours with no criterion.
  The two surviving mutations are explained rather than excused.

## 2026-08-21T20:34:00Z — review-close v0.1.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next`.
- **Inputs read:**
  - the diff `main..wi/WI-0002` for `expenses/` — five modules, hunk by hunk — and the six test
    modules
  - `tracker/items/WI-0002/item.md`, `history.md` (nine rows), `journal.md` **in full** (six
    entries), `artifacts/plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`
  - both questions on the item, with their `## Consequences`
  - `ADR-0001` through `ADR-0010`, `docs/architecture/overview.md` (v2), `docs/product/prd.md`
    (v2), `docs/product/vision.md` (v3) — read against the code for D12
  - `tracker/items/WI-0001/artifacts/review.md`, to check that the gap it handed forward was
    actually taken up rather than quietly dropped. It was: `ADR-0010`
- **Decisions:**
  - **Checked the mechanics before anything substantive.** History chains without a gap and its
    last row matched the item's status; six journal entries account for six executions; fourteen
    criteria ticked with a report row each; both questions answered with real files named.
  - **Ran `check-verify-freshness` rather than judging by the size of the last commit.** The head
    is not the verified commit, which is the situation D10 exists for; the script and an
    independent `git diff --name-only … -- expenses tests` both confirm only the record moved.
  - **Trial-merged into a `--detach`ed worktree.** WI-0001's review learned the hard way that
    `git worktree add <path> main` checks out the *real* branch and a merge inside it moves the
    trunk for real; that mistake was caught by a gate and rewound, and the correction is in
    WI-0001's journal. This time `main` was confirmed still at `3a8d9f7` after the trial was
    discarded.
  - **Finding 1, accepted, not a send-back: the reserved characters are written twice.**
    `group.RESERVED_CHARACTERS` is data that `validate_name` checks against;
    `cli._split_sharers` splits on the same two characters as control flow. They agree today.
    Reserving a third would change one and not the other, and nothing would catch it. No
    criterion covers it and the behaviour is correct, so rejecting would be inventing a
    requirement — but this is the last moment anyone reads this diff, which is exactly when a
    quiet duplication should be named.
  - **Finding 3, the one I most considered sending back: the journal's own timestamps.** Each
    entry is stamped up to twenty-seven minutes ahead of the history row it describes, because
    `transition` stamps history from the real clock while journal entries are hand-written and no
    procedure requires the two to agree. Not sent back, for two reasons: nothing about *what*
    happened is misreported, each `**Status:**` bullet matches its row; and the remedy for an
    append-only file is a later entry, not a tidy-up. Recorded as a defect in the record rather
    than absorbed, because a reader who spots it will start distrusting the whole file, and they
    should be able to find that somebody already knew.
  - **Finding 5, `shared by 1 people.`, accepted rather than rejected.** `verify` surfaced it and
    declined to send it back on the grounds that no criterion covers it; I agree, and rejecting
    here would be the reviewer inventing a criterion at the last gate. Written into `## Notes`
    with a named owner — the next `refine` execution that touches a confirmation message.
  - **Checked that WI-0001's handed-forward gap was actually taken up.** It was: `ADR-0010`
    exists, the code implements it, and `verify` exercised it. That is the one thing a review
    can check that no upstream stage can, because it spans two items.
  - **Walked `ADR-0002`'s six refusal conditions against `group.add_expense` line by line** for
    D12, rather than reading the ADR approvingly. All six are implemented and each has a test. I
    also re-read the stored JSON against `ADR-0009` rather than taking the report's word for the
    shape.
  - **Left EP-001 open.** WI-0003 and WI-0004 are still at `draft`, so DE1 fails and the epic's
    Definition of Done was not applied. Recorded on the epic's journal so the reason is findable
    from the epic.
  - **Filed no bug and no question.** Nothing contradicts an ADR; every finding is either
    behaviour no criterion covers or a blemish in the record, and none of it belongs to another
    item.
- **Questions raised:** none.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0
  - `git diff --name-only 10a6bc3..wi/WI-0002 -- expenses tests` → empty
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, 3
    commits, run **before** the merge
  - `git worktree add --detach /tmp/trial2 main` → `git merge --no-edit wi/WI-0002` → clean
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0, 79 tests;
    `python3 -m compileall -q expenses tests` → exit 0
  - `git worktree remove --force /tmp/trial2`; `git log --oneline -1 main` → `3a8d9f7`, unmoved
  - re-ran AC7's third case and AC10's accepted case by hand → same output the report records
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the close
  - `git checkout main && git merge --no-ff wi/WI-0002` → after the close
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1 to D12 each with its own result and evidence in
    `artifacts/review.md`. D5 passes with a recorded blemish (Finding 3) and D12 is the one that
    did work: six ADR conditions walked against the code and two document claims re-run.
  - `verification-postdates-the-code` (hard) → **pass** — `check-verify-freshness` exit 0, plus
    the independent diff over `expenses/` and `tests/`, which is empty.
  - `commits-reference-the-item` (hard) → **pass** — exit 0, run before the merge while the range
    was still non-empty.
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 79 tests, exit 0, on the merged tree in a
    detached throwaway worktree.
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings.
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and
    `git log --grep WI-0002` a reader can answer all five questions in
    `spec/journal-and-history.md` §3: what was asked for and how it changed (two questions, both
    answered by the person who wanted the tool, quoted verbatim in `refinement-qa.md`, plus six
    more decided by `refine` and marked `[assumed]`); which skill decided what; what was run;
    which gates passed; and where the work stopped. The timestamp drift in Finding 3 is the one
    thing that would slow such a reader down, and it is now written down.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new) — what was examined, D1–D12, five findings,
    six accepted gaps, the verdict
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`; `## Notes` extended with the five
    accepted gaps, one of them with WI-0004's refinement named as its owner
  - `tracker/items/EP-001/journal.md` — an entry recording that the epic stays open and why
  - the merge commit of `wi/WI-0002` into `main`
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is delivered and merged: `add-expense` and `expenses`, the split model and
  the rounding rule, stored as `ADR-0009` fixes and derived on every run. Five findings, all
  recorded and none blocking, and one gap handed forward with an owner — WI-0004's refinement
  should pin that a refusal creates no record file.
