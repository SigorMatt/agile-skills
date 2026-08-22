# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-21T21:10:30Z — intake v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's stated idea in `IDEA.md`; this item was
  created by that execution
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/items/` — empty before this execution, so `WI-0001` is a fresh allocation
  - `.claude/agile-skills/spec/work-item.md`, `spec/ids-and-statuses.md`, `spec/question.md`
- **Decisions:** see EP-001's entry of the same timestamp for how the work was split. Specific to
  this item: it was kept separate from WI-0002 rather than folded into it, because registering
  people is a capability the stakeholder named on its own and because it is the cheapest place to
  establish that data survives between runs — which AC2 checks and which every later item relies
  on. Its four criteria were written from the idea alone and are deliberately left rough on the
  exact command names; `refine` owns pinning those. What counts as "the same name" when case or
  spacing differs was left unsettled and flagged in `## Notes` rather than invented.
- **Questions raised:** none. This is the only item of the four that intake could shape without
  needing anything from the stakeholder, which is why it is the only one left at `draft`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0001 --type work-item …` → exit 0
- **Gates:** the four gates in intake's contract were applied to this execution as a whole and
  are recorded, with their evidence, in EP-001's entry: `workspace-valid` → pass,
  `epic-has-success-measures` → pass, `items-are-separable` → pass, `no-solution-in-the-problem`
  → pass. For this item specifically, `no-solution-in-the-problem` removed "in a JSON store" from
  the title, and `items-are-separable` places it first, depending on nothing.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/journal.md`, `history.md` (new)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` with four criteria and an explicit out-of-scope list. Ready for
  `refine`, and the only item in the epic that is not waiting on the stakeholder.

## 2026-08-21T21:37:30Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` — highest-ranked runnable item (priority
  `critical`, and WI-0002 shares that priority and `created` but sorts after it by ID).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md` (intake's entry of
    2026-08-21T21:10:30Z, which records what intake left for this skill to pin)
  - `docs/product/vision.md` (v5), `tracker/items/EP-001/item.md` (SM1, SM2, SM4 and the scope
    statement about where the data file lives)
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — sibling scope, and in
    WI-0004's case AC6's comma-separated `--shared-by`, which constrains what a person's name may
    contain
  - `docs/architecture/adr/ADR-0001-money-in-integer-pence-with-largest-remainder-split.md` (v1)
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/work-item.md`
- **Decisions:**
  - **Precondition 2 fails: the human is not present in this session and there is no interactive
    question tool.** `refine` is a direct-conversation skill and cannot do its job without one.
    Per the skill's own precondition and its `question` escalation route, this execution filed
    questions addressed to `human` and suspended the item instead of refining it. Nothing in
    `item.md` was changed: an item half-rewritten against guessed answers is worse than one left
    as intake wrote it, because the guesses would then look like requirements.
  - **The Definition of Ready agenda was built first, and the questions were derived from it**
    rather than from a general conversation. The failing criteria are R4 and R10, per the gate
    record below. Four questions were filed, each traceable to a specific failure:
    - **Q-001 — the command surface.** AC1, AC3 and AC4 all say "a documented command", which no
      one with a terminal can run (R4). Asked once here rather than four times, because WI-0002,
      WI-0003 and WI-0004 all extend the same surface.
    - **Q-002 — when two names are the same person, and what names are refused.** AC3 turns on
      "already registered" and never defines it (R4); intake flagged exactly this in `## Notes`
      and refused to invent it. The comma half of the question comes from WI-0004 AC6, where a
      comma in a name would make `--shared-by` ambiguous — cheap to close now, expensive after
      names are stored.
    - **Q-003 — where the data file lives and whether one run can be pointed elsewhere.** AC2 and
      EP-001 SM2 require persistence; EP-001's scope leaves the location open. The override half
      is not a convenience: EP-001 SM1 and every acceptance check start "from an empty data
      store", which is impossible to arrange without touching the stakeholder's own data unless
      the location can be changed for a run (R10 — a behaviour nothing currently makes visible).
    - **Q-004 — output, streams and exit codes for the four cases.** AC3's "says so rather than
      failing silently" and AC4's "a message saying so" are the kind of wording `verify` — which
      may ask nobody anything — cannot adjudicate (R4). Exit codes also decide whether the
      commands compose, which nothing currently states (R10). The list's ordering is folded in
      because AC1 is not decidable with three people registered until it is fixed.
  - **What was deliberately *not* asked.** The data file's format, the internal representation of
    a person, and the shape of the code are `plan`'s to decide, not the stakeholder's; asking
    would spend their attention on something no document needs from them. The rounding rule is
    already fixed by ADR-0001.
  - **Every question carries a recommendation.** Filing options without a recommendation pushes
    the whole cost of the thinking upstream, which is how a question protocol degrades into
    asking the human everything. Where the recommendation could be wrong for a reason only the
    stakeholder knows — a name with a comma in it, a dislike of putting things on PATH — the
    question says what to answer instead and what that would cost.
- **Questions raised:** `Q-001`, `Q-002`, `Q-003`, `Q-004` — all blocking, all addressed to
  `human`. No `artifacts/refinement-qa.md` was written: no exchange took place, and a Q&A file
  recording questions with no answers would misrepresent the state. It will be written by the
  execution that actually refines this item.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 pre-existing warning (`project.commands.test-null`, owned by `plan`)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to awaiting-answer --actor refine --resume-to draft --reason "..."` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 before filing; re-run after the
    transition, exit 0).
  - `definition-of-ready` → **fail**, recorded criterion by criterion. R1 pass (frontmatter
    complete; `type`, `epic`, `priority` all set). R2 pass (`## Story` names the role — the person
    keeping the group's books — the capability, and a "so that" outcome). R3 pass (four
    `AC<n>` checkboxes exist). **R4 fail** — AC1, AC3 and AC4 say "a documented command" with no
    command named; AC3's "already registered" is undefined for differing case or spacing; AC3's
    "says so" and AC4's "a message saying so" name no output and no exit code. **R5 pass**
    (`## Out of scope` names removing or renaming a person, attributes beyond a name, and more
    than one group). R6 fail at the moment of writing — the four questions this execution filed
    are blocking — which is the intended state, not a defect. R7 pass (`depends-on` is absent;
    the item is first in the delivery order). **R8 fail** — no `artifacts/refinement-qa.md`,
    because no exchange has happened. R9 pass (adding and listing people is one coherent change,
    and intake's entry records why it was kept separate from WI-0002). **R10 fail** — nothing
    states the exit codes, nothing states the list's ordering, and nothing states whether the
    data file's location can be varied for a run.
  - `criteria-are-decidable` → **fail**. AC2 is decidable as written (add in one invocation, list
    in a later one, look for the name). AC1, AC3 and AC4 are not: none of them names a command to
    run, and AC3 and AC4 name no output to inspect. This is the gate Q-001 to Q-004 exist to
    clear.
  - `qa-recorded-verbatim` → **skipped**. There is no exchange to record — the human is not in
    this session. Recording the filed questions as though they were a conversation would be
    exactly the paraphrasing-into-agreement this gate forbids.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` (new)
  - `tracker/items/WI-0001/item.md` — **unchanged**, deliberately
- **Status:** `draft` → `awaiting-answer` (`resume-to: draft`)
- **Result:** WI-0001 could not be refined because the stakeholder is not in this session. Four
  blocking questions are filed, each tied to a Definition of Ready criterion that fails; the item
  is suspended and returns to `draft` when they are answered.

## 2026-08-21T21:40:40Z — answer-questions v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`; the stakeholder answered all four questions in their
  files between turns, so this execution was run ahead of `next` — `next` step 2 would otherwise
  surface the open human-addressed questions and stop the loop without consuming their answers.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — all four
    carry a stakeholder answer in `## Answer`
  - `tracker/items/WI-0001/item.md`, `history.md` (`resume-to: draft` on the suspending row),
    `journal.md` (refine's entry, for what each question was meant to clear)
  - `tracker/items/EP-001/item.md` (SM1, SM2, SM4, `## Scope`), `tracker/items/EP-001/questions/Q-001.md`
  - `tracker/items/WI-0002/item.md` (AC4, AC5), `tracker/items/WI-0003/item.md` (AC4, AC6),
    `tracker/items/WI-0004/item.md` (AC4, AC5, AC6 — the `--paid-by`/`--shared-by` shape)
  - `docs/product/vision.md` (v5), `docs/architecture/adr/ADR-0001` (v1)
  - `.claude/agile-skills/spec/question.md` §3 and §4, `spec/doc-header.md` §4, `spec/journal-and-history.md`
  - `tracker/items/WI-0001/artifacts/plan.md` — **does not exist**; the item has never been
    planned, so there was no plan to propagate into
- **Decisions:**
  - **All four answers were delegations, so all four were decided by the architect and recorded
    as ADRs.** The stakeholder wrote "whatever you think is best" three times and "use your
    judgement on the exact rule" once. `spec/question.md` §4 lists no condition that a
    delegated-back choice meets, so re-escalating would have spent the scarcest thing in the loop
    on a choice they had just declined to make. This is the route WI-0003/Q-002 already
    established in this workspace.
  - **`answered-by` is `answer-questions` on all four, not `human`.** The stakeholder supplied
    the authorisation to decide, not the decision. Recording `human` would credit them with four
    design choices they explicitly handed back, and `SIMULATION-NOTICE.md` requires the record
    not to claim more than it can support. Where they *did* settle something — no cloud, and
    `ana` must not become a second person — that is quoted in the answer and stated as binding.
  - **Q-001 → ADR-0002, and deliberately not the recommendation as written.** `refine` recommended
    option B, `expenses` on `PATH`. Taken literally that makes every acceptance criterion in this
    epic depend on an install step, and `verify` — which may not ask anyone anything — cannot
    distinguish "not on PATH" from "broken". ADR-0002 takes option D instead: the same executable
    file, invoked `./expenses <subcommand>` from the repository root in the criteria, with the
    `PATH` install kept as documented convenience. B's ergonomics survive; the criteria become
    decidable by someone who has just cloned the repository, which is what R4 demands.
  - **Q-002 → ADR-0003, option B, inside the stakeholder's constraint.** Their sentence eliminates
    option A by instruction rather than by preference. C (accent-folding) was rejected on
    asymmetry, not frequency: a wrongly-split person is repairable by adding the missing spelling,
    a wrongly-merged pair is not, and EP-001 excludes editing and deleting.
  - **Q-003 → ADR-0004, option B.** The `--data-file` override is treated as load-bearing rather
    than convenient: every EP-001 success measure begins "from an empty data store", so without it
    `verify` could only check this epic by writing to the stakeholder's real ledger. The file's
    *format* was left to `plan` as the question promised, and AC7 was written so that `plan`'s
    choice cannot invalidate it — it states the default and the override without quoting a
    filename.
  - **Q-004 → ADR-0005, option C plus alphabetical listing, generalised.** Deciding output and
    exit codes once, for the whole epic, rather than four times: WI-0002's two refusals, WI-0003's
    empty report and WI-0004's rejected rows all need the same conventions, and four separate
    decisions would produce four dialects.
  - **Three acceptance criteria were added (AC5, AC6, AC7) and four rewritten (AC1–AC4).** This is
    one of only two skills permitted to change a criterion, and it is journalled here because of
    that. Nothing was weakened: every rewrite replaces "a documented command" or "says so" with
    the exact command, stream and exit code, and the three new criteria state behaviour the
    answers created — the refusals, the listing order, the data file option — which no existing
    criterion covered. The item is at `draft`, so `refine` will re-check all seven against the
    Definition of Ready; nothing here pre-empts that.
  - **ADR-0002 and ADR-0005 were written as project-wide decisions on a per-item question.** They
    are cited from WI-0001 but bind WI-0002 to WI-0004, and the item's `## Notes` says so, because
    a convention recorded only on the first item that needed it is a convention the later items
    will each re-invent.
- **Questions raised:** none. Nothing was re-addressed to the human: all four answers arrived, and
  each was answerable within the stakeholder's own words plus the record.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 mid-execution, as
    expected: `board.stale` and `question.awaiting.none-open` while the questions were answered
    but the item had not yet been transitioned. Re-run after the transition and the board
    regeneration → exit 0.
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to draft --actor answer-questions --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, checked file by file after writing. `ADR-0002`, `ADR-0003`,
    `ADR-0004` and `ADR-0005` all exist under `docs/architecture/adr/` with the decisions above.
    `tracker/items/WI-0001/item.md` carries AC1–AC7 in their new wording and a `## Notes` section
    naming all four ADRs. `tracker/items/EP-001/item.md` `## Scope` names the `expenses`
    executable, `~/.expenses.json`, `--data-file` and the output convention.
    `docs/product/vision.md` is at v6 with a `## How it is used` section and a change-log row.
    No `## Consequences` section names a file that was not changed, and no file was changed that a
    `## Consequences` section does not name.
  - `answered-from-the-record` → **pass**. Each answer cites what it follows from: the
    stakeholder's own words for the delegation and for the two constraints they did set, and a new
    ADR for the substance of each decision. Nothing was answered by assertion.
  - `escalation-is-justified` → **skipped**. No question was re-addressed to the human.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after the transition and the board
    regeneration; the two errors seen mid-execution are the documented consequence of answering
    the last open blocking question before transitioning, and are the reason the transition
    follows immediately).
  - `item-resumed-correctly` → **pass**. The suspending row (2026-08-21T21:30:39Z, `refine`)
    records `resume-to: draft`, and this execution transitioned WI-0001 to `draft`.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — answered,
    `answered-by: answer-questions`, each with a `## Consequences` list of files
  - `docs/architecture/adr/ADR-0002-command-line-surface-single-executable-with-verb-noun-subcommands.md` (new)
  - `docs/architecture/adr/ADR-0003-person-identity-trimmed-case-insensitive.md` (new)
  - `docs/architecture/adr/ADR-0004-data-file-in-the-home-directory-overridable-per-run.md` (new)
  - `docs/architecture/adr/ADR-0005-output-streams-and-exit-codes.md` (new)
  - `tracker/items/WI-0001/item.md` — AC1–AC4 rewritten, AC5–AC7 added, `## Notes` rewritten
  - `tracker/items/EP-001/item.md` — `## Scope` first bullet rewritten
  - `docs/product/vision.md` — v5 to v6
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** All four of WI-0001's questions are answered and their consequences are in the
  artifacts. The command surface, the identity rule, the data file and the output conventions are
  now recorded decisions the whole epic can read, and the item is back at `draft` for `refine` to
  re-check against the Definition of Ready.

## 2026-08-21T21:49:00Z — refine v0.1.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (highest-ranked runnable item: rank 1, oldest
  `created`, lowest ID)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (as rewritten by `answer-questions` earlier this turn),
    `history.md`, `journal.md` (intake's entry and the previous `refine` entry, for what each
    question was meant to clear)
  - `tracker/items/WI-0001/questions/Q-001.md` to `Q-004.md` — all four answered, and the source
    of the Q&A record this execution wrote
  - `docs/architecture/adr/ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005` (all v1) and `ADR-0001`
    (v1, for the sort key it shares with ADR-0003)
  - `docs/product/vision.md` (v9), `tracker/items/EP-001/item.md` (SM1, SM2, SM4)
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — checked for scope
    overlap; `list-people` prints names only, balances belong to WI-0003, which is now stated in
    this item's `## Out of scope`
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **This was not a fresh refinement.** `history.md` shows the item was suspended by `refine` on
    four blocking questions and returned to `draft` by `answer-questions` with all four answered.
    The job was therefore to turn those answers into criteria, not to re-open the item — and no
    question already answered was asked again.
  - **No new question was put to the stakeholder.** Every remaining gap was either settled by
    their own words, or by an ADR written under a delegation they gave explicitly. Filing a
    question would have stopped the whole loop for something the record already answers.
  - **Every criterion was rewritten to start from an empty store.** Each one now runs against
    `$T`, a path that does not exist at the start of the criterion. Without that, AC1 and AC4
    contradict each other depending on what happened to be in the data file, and EP-001 SM1's
    "from an empty data store" would not be reproducible.
  - **Refusals now assert that nothing changed**, not only that a message appeared. AC3, AC5 and
    AC8 each require the stored file to be byte-for-byte unchanged. ADR-0005 clause 2 says a
    refusal records nothing; a criterion that only checked the message would pass against an
    implementation that printed the message *and* wrote the person.
  - **AC5 pins exact message text**, where the previous wording said "a message naming what was
    wrong". "Naming what was wrong" is the kind of phrase `verify` has to interpret, and
    interpretation by `verify` is the thing this item's whole question round existed to remove.
  - **AC6 was extended to cover display of a name typed with surrounding whitespace** (` Ben ` is
    stored and shown as `Ben`). ADR-0003 clause 2 says it; nothing checked it.
  - **AC7 deliberately does not quote the default filename.** ADR-0004 clause 4 leaves the storage
    format, and therefore the extension, to `plan`. The criterion instead requires exactly one new
    file directly in `$HOME` at the path the README documents, which is checkable and survives any
    legitimate format choice.
  - **AC8 is new and was added by `refine`, not by the stakeholder.** Nothing anywhere said what
    happens when the data file exists but is not the tool's format. The natural implementation
    overwrites it, and this epic has no way to rebuild a ledger, so the criterion requires a
    refusal. Recorded as `[assumed]` in the Q&A under the stakeholder's standing delegation in
    Q-004.
  - **Two behaviours were left deliberately unconstrained and named as such (R10):** the text of
    `argparse`'s usage errors, and a `--data-file` path that cannot be written. Both are in
    `## Notes` with `refine` named as who left them so. Making them criteria would have meant
    checking `argparse`'s wording, which nobody controls, and building a permission-controlled
    fixture for a case the documented default cannot reach.
  - **`## Out of scope` gained two entries**: `--data-file` is not a multi-group feature, and
    `list-people` shows names and nothing else. Both are things a reader could reasonably assume
    were included — the first because two files look like two ledgers, the second because "list
    the people" invites "and what they owe".
- **Questions raised:** none this execution. The four filed by the previous `refine` execution
  (`Q-001` to `Q-004`) are all answered and are recorded verbatim in
  `artifacts/refinement-qa.md`; two items in that file are tagged `[unresolved]` and are carried
  into `## Notes` as deliberately unconstrained rather than as risks to chase.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 pre-existing
    warning (`project.commands.test-null`, owned by `plan`)
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to ready --actor refine --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 before and after the transition).
  - `definition-of-ready` → **pass**, criterion by criterion:
    **R1 pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: critical`.
    **R2 pass** — `## Story` names the role (the person keeping the group's books), the capability
    (register each friend and see the list back) and the outcome ("so that … a typo does not
    silently create a fourth person").
    **R3 pass** — AC1 to AC8, each a labelled checkbox.
    **R4 pass** — was the failing criterion at the previous execution. Every criterion now names a
    command and an exact expected output, stream and exit code; no unmeasurable adjective remains.
    See `criteria-are-decidable` below for the per-criterion evidence.
    **R5 pass** — `## Out of scope` names four things, two added here: `--data-file` is not a
    group feature, and `list-people` does not show balances.
    **R6 pass** — no open question remains on this item; Q-001 to Q-004 are all `answered`.
    **R7 pass** — no `depends-on`; the item is first in the delivery order and nothing precedes it.
    **R8 pass** — was failing at the previous execution because no exchange had happened. It has
    now happened, asynchronously, and `artifacts/refinement-qa.md` records all four questions and
    answers verbatim, each tagged `[human]`, `[assumed]` or `[unresolved]`.
    **R9 pass** — adding and listing people is one coherent change against one data file; intake's
    entry records why it was kept separate from WI-0002.
    **R10 pass** — was failing at the previous execution. Every combination is now visible:
    `--data-file` with each subcommand (AC1, AC3, AC4, AC5, AC8) and without it (AC7);
    normalisation with listing (AC3, AC6); refusal with persistence (AC3, AC5, AC8). The two
    combinations deliberately left unconstrained are named in `## Notes` with who left them.
  - `criteria-are-decidable` → **pass**. AC1: run the two commands against a fresh `$T`; compare
    stdout to `Added Ana` and `Ana`, stderr to empty, `$?` to 0. AC2: run the third invocation in a
    new shell; compare stdout to `Ana`. AC3: run `add-person " ana "`; compare stderr to
    `Ana is already registered`, `$?` to 1, `cmp` the file against a copy taken before, and count
    the lines of `list-people`. AC4: `list-people` against a non-existent `$T`; compare stdout to
    `No one is registered yet`, `$?` to 0, and `test ! -e "$T"`. AC5: three invocations; compare
    each stderr string, `$?` to 1, and `list-people` output before and after. AC6: add three
    names; compare the three output lines and their order exactly. AC7: `HOME=$(mktemp -d)`; run
    `add-person`; `ls -A "$HOME"` yields exactly one entry, and the README names that path; then
    `list-people` prints `Ana`. AC8: write `not a data file` into `$T`; run each command; check
    stderr contains `$T`, contains no `Traceback`, `$?` is 1, and `cmp` shows the file unchanged.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` holds all four questions with
    the options each offered, and each answer copied from the question file without alteration —
    including the two answers that are pure delegations ("whatever you think is best"), which are
    recorded as such and tagged `[human]`, with the substance that followed tagged `[assumed]`
    beside them. Nothing was paraphrased into a firmer answer than the stakeholder gave, and the
    file says plainly that the exchange happened in files rather than in conversation.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0001/item.md` — AC1 to AC7 rewritten, AC8 added, `## Out of scope` extended
    by two entries, `## Notes` extended with what refinement decided and what it left unconstrained
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0001 is Ready. Eight criteria, each with a command to run and an exact expected
  output; the whole question round recorded verbatim; two behaviours named as deliberately
  unconstrained rather than left invisible. `plan` can design against it without asking anyone
  anything.

## 2026-08-21T21:55:00Z — plan v0.1.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC8, `## Out of scope`, `## Notes` including the two
    behaviours R10 records as deliberately unconstrained), `history.md`, `journal.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — every `[assumed]` and `[unresolved]`
    entry; the `[assumed]` message strings and the `--data-file` position are design inputs, and
    the two `[unresolved]` entries are the soft ground this plan names in `## Risks`
  - `docs/architecture/adr/ADR-0001` to `ADR-0005` (all v1); `docs/product/vision.md` (v9);
    `tracker/items/EP-001/item.md` (SM1–SM4)
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md` — read for what the data
    file will have to hold later, so that ADR-0006's envelope does not need a migration
  - `tracker/project.yaml`; `docs/architecture/overview.md` — **did not exist**, and this is the
    first planned item, so this execution created it
  - **The code:** there is none. `git ls-files` shows only `.claude/`, `docs/`, `tracker/` and the
    harness files, so nothing constrains this design from below and no existing behaviour was read.
- **Decisions:**
  - **The storage format, decided and recorded as ADR-0006** (route: decided; ADR-0004 clause 4
    explicitly reserved it for `plan`). JSON over SQLite, CSV and `pickle`. The deciding
    consideration was not convenience but that EP-001 has no edit and no delete: a ledger this tool
    corrupts cannot be rebuilt by this tool, so the format that a person can read and hand-repair
    wins over the one with transactions. The atomic write (temporary file in the same directory,
    then `os.replace`) and the strict read are part of the same decision, and they are what make
    AC3, AC5 and AC8's "byte-for-byte unchanged" a property of the control flow rather than
    something asserted after the fact.
  - **The envelope carries `schema: 1`, and a missing key reads as empty** (ADR-0006 clause 2).
    This is the one piece of this plan that looks past WI-0001, and it is deliberate and cheap: it
    is what lets WI-0002 add `expenses` and WI-0004 add its import record without a migration.
    Nothing speculative is *written* — this item writes `schema` and `people` and nothing else.
  - **The test framework, decided and recorded as ADR-0007** (route: decided). `pytest` is not
    installed here and cannot be installed, so `commands.test` is
    `python3 -m unittest discover -s tests -t . -q`, which this execution ran in this project
    before recording it. `commands.lint` is `python3 -m compileall -q expenses expenses_tool tests`
    and is labelled honestly as a syntax check rather than a style linter, because no style linter
    exists on this machine. `commands.build` stays `null` with the reason recorded, rather than
    being filled with an invented command the gate would report as a pass.
  - **The code layout, decided and recorded as ADR-0008** (route: decided; ADR-0002 clause 1
    reserved it). A thin `expenses` launcher over `expenses_tool/`, because a file named `expenses`
    with no extension cannot be imported, and ADR-0007 clause 3 wants the rules unit-tested without
    a subprocess for every assertion. The launcher resolves `os.path.realpath(__file__)` so that
    ADR-0002 clause 2's optional `PATH` install works when `expenses` is a symlink — the one fiddly
    part of this layout, decided here rather than left for `implement` to discover.
  - **`store.py` never prints and `main()` never exits** (ADR-0008 clauses 3 and 4). Every string
    the criteria quote lives in `cli.py`, so there is exactly one place where what the user sees is
    decided, and tests can call `main()` directly.
  - **Answered from the documents, not re-decided** (route: documented): the command names and the
    invocation (ADR-0002), the identity rule and listing order (ADR-0003), the default file and the
    `--data-file` override (ADR-0004), every stream and exit code (ADR-0005), and AC5's exact
    message strings (`refinement-qa.md`, `[assumed]` under the stakeholder's delegation in Q-004).
  - **Four assumptions recorded rather than escalated** (route: assumed, all reversible): the
    supported `schema` value, the `DataFileError` wording — deliberately *not* pinned, because AC8
    constrains only that the message names the file and shows no traceback — the temporary file
    living in the target's directory, and `argparse`'s usage text being accepted unchanged.
  - **Nothing was asked of the stakeholder.** Every decision here was either fixed by a document or
    reversible in the sense `spec/question.md` §1 defines: one file, no data migration, no change
    to a published interface.
  - **`docs/architecture/overview.md` created at v1.** It describes the three layers, the data
    file, the conventions every command follows, and — in one table — which ADR fixes what. It also
    names what is not there yet, so the later items extend a described system rather than an
    implied one.
- **Questions raised:** none.
- **Commands:**
  - `python3 -V` → `Python 3.12.3`; `python3 -c "import pytest"` → `ModuleNotFoundError`;
    `python3 -m ruff --version` and `python3 -m flake8 --version` → both `No module named …`.
    These are the evidence behind ADR-0007.
  - `python3 -m unittest discover -s tests -t . -q` in a scratch directory → exit 1 without
    `tests/__init__.py` (`Start directory is not importable`), exit 0 with it. That failure is why
    ADR-0007 clause 2 and plan step 1 require `tests/__init__.py` to exist.
  - `python3 -m compileall -q <dir>` → exit 0.
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, **0 warnings** — the
    standing `project.commands.test-null` warning is gone now that `commands.test` is set.
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to planned --actor plan --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors and 0 warnings).
  - `every-criterion-is-addressed` → **pass**. `artifacts/plan.md` `## Acceptance criteria mapping`
    has one row per criterion, AC1 to AC8, each naming the plan steps that satisfy it and a named
    test that demonstrates it — `test_ac1_add_then_list`, `test_ac2_persists_across_invocations`,
    `test_ac3_duplicate_refused`, `test_ac4_empty_store`, `test_ac5_invalid_names_refused`,
    `test_ac6_display_and_order`, `test_ac7_default_data_file`, `test_ac8_unreadable_data_file` —
    with the exact comparison each makes. No row says "tests".
  - `project-commands-resolved` → **pass**. `commands.test` and `commands.lint` are set to commands
    run in this project during this execution; `commands.build` is `null` with ADR-0007 clause 5
    recording why, which is the honest form rather than an invented command.
  - `decisions-recorded` → **pass**. Three ADRs created (ADR-0006, ADR-0007, ADR-0008), each with
    context, at least three options with costs and risks, the decision, and consequences including
    reversibility; each is cited from `plan.md` `## Decisions and ADRs`. The decisions that were
    *not* re-made are listed there too, with the ADR each was read from — so a later reader can
    tell what this execution decided from what it inherited.
  - **Self-check, step 1 of the skill's own list:** the step that would still have needed a decision
    was the launcher's package lookup under a `PATH` symlink; it is now ADR-0008 clause 2 and plan
    step 1, and the residual failure mode (copying `expenses` without `expenses_tool/`) is named in
    `## Risks` and mitigated by the README step.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0006-json-data-file-written-atomically.md` (new)
  - `docs/architecture/adr/ADR-0007-tests-with-the-standard-library-unittest.md` (new)
  - `docs/architecture/adr/ADR-0008-thin-launcher-over-an-importable-package.md` (new)
  - `docs/architecture/overview.md` (new, v1)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` set, with a comment naming ADR-0007
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0001 has a plan a developer can execute without deciding anything: twelve steps
  naming the files they touch and what is true afterwards, every criterion mapped to a named test,
  three ADRs for the choices that were genuinely open, and an architecture overview the next three
  items can extend rather than infer.

## 2026-08-21T21:58:00Z — implement v0.1.1 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next`; no branch existed, so this is a fresh
  implementation rather than a resumption.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC8, `## Notes` — including the two behaviours R10
    records as deliberately unconstrained), `history.md`, `artifacts/plan.md` (all twelve steps and
    the mapping table), `artifacts/refinement-qa.md` (the `[assumed]` message strings AC5 quotes)
  - `tracker/items/WI-0001/questions/Q-001.md` to `Q-004.md` — all four `answered`, and their
    consequences already propagated into `item.md` and the ADRs, so nothing was read out of a
    question file and acted on directly
  - `docs/architecture/overview.md` (v1), `docs/architecture/adr/ADR-0002`, `ADR-0003`, `ADR-0004`,
    `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008` (all v1)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` both set by `plan`, so neither had
    to be invented
  - **Source files:** none existed. `git ls-files` before this execution showed no production code.
- **Decisions:** all inside the plan's latitude; none of them changes what is delivered.
  - **`store.load` raises with a specific `reason` per failure mode** rather than one generic
    "not an expenses data file". The reason is interpolated into AC8's message, and a message that
    names *how* the file is wrong is the difference between a user fixing it and a user deleting
    their ledger.
  - **`save` calls `os.fsync` before `os.replace`.** The plan said flush and close. `flush()` moves
    bytes to the OS, not to disk; without `fsync` a crash can leave a renamed but empty file, which
    is precisely what the atomic write exists to prevent. Recorded as a deviation in the report.
  - **`save` deletes its temporary file on any failure**, including `KeyboardInterrupt` (hence
    `except BaseException`). AC7 asserts that a default-path run leaves exactly one file in `$HOME`,
    so debris from a failed write would fail a criterion — which is the behaviour I wanted from
    that assertion.
  - **The duplicate message names the *stored* spelling, not the one just typed.** `add-person ana`
    against a stored `Ana` says `Ana is already registered`, which is what AC3 quotes and also the
    more useful of the two: it tells the user which spelling the ledger holds.
  - **`--data-file` is a parent parser shared by both subcommands**, so it is written after the
    subcommand, as every criterion does. `os.path.expanduser` is applied to whatever value arrives,
    so `--data-file ~/x.json` works from a shell that does not expand it.
  - **Two tests were written that map to no criterion** (the usage-error exit codes). ADR-0005
    clause 3 fixes that exit code and nothing else holds it in place. They are declared in the
    report's `## Deviations` rather than left for a reviewer to find in the diff.
  - **Decided *not* to handle an unwritable `--data-file` path.** ADR-0005 clause 2 suggests what it
    should look like, but the item's `## Notes` records it as deliberately unconstrained by
    `refine`, and no criterion covers it. Building it would be behaviour nobody asked for and
    nobody verifies; it is named in the report's `## What I did not do` instead, with the honest
    consequence that such a path produces a traceback.
- **Questions raised:** none. No decision arose that was not either fixed by an ADR or reversible
  within one file.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 27 tests … OK` (run after the
    store tests, again after the CLI tests, and finally on the branch head `1dd3f09`)
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001 --root . --trunk main`
    → `all 1 commit(s) on main..wi/WI-0001 name WI-0001`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to in-progress --actor implement --branch wi/WI-0001 --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to verifying --actor implement --reason "..."` → exit 0
- **Gates:** run on the branch head, after the last change.
  - `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t . -q`, exit 0, 27 tests.
  - `lint-clean` → **pass**. `python3 -m compileall -q expenses expenses_tool tests`, exit 0.
    ADR-0007 clause 4 records that this is a syntax check rather than a style linter — no style
    linter is installed and none can be installed here — so this gate is weaker than its name
    suggests, and saying so is the point of recording it this way.
  - `workspace-valid` → **pass**. `validate-workspace`, exit 0, 0 errors and 0 warnings.
  - `every-criterion-has-a-test` → **pass**. AC1 to AC8 each map to a named test class in
    `tests/test_cli_people.py`: `AC1::test_ac1_add_then_list`,
    `AC2::test_ac2_persists_across_invocations`, `AC3::test_ac3_duplicate_refused`,
    `AC4::test_ac4_empty_store`, `AC5::test_ac5_invalid_names_refused`,
    `AC6::test_ac6_display_and_order`, `AC7::test_ac7_default_data_file`,
    `AC8::test_ac8_unreadable_data_file`. Each compares exact strings and exit codes, and the three
    refusal criteria additionally compare the data file's bytes before and after, so none of them
    would pass against an implementation that printed the right words and stored the wrong thing.
  - `commits-reference-the-item` → **pass**. `check-commit-refs`, as above.
- **Artifacts:**
  - `expenses` (new, executable), `expenses_tool/__init__.py`, `expenses_tool/store.py`,
    `expenses_tool/cli.py` (new)
  - `tests/__init__.py`, `tests/test_store.py`, `tests/test_cli_people.py` (new)
  - `README.md` (new) — load-bearing for AC7, which refers to the path it documents
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0001/item.md` — `branch: wi/WI-0001` recorded
  - branch `wi/WI-0001`, commit range `main..wi/WI-0001` = `1dd3f09` (one commit)
  - `tracker/board.md` — regenerated
- **Status:** `in-progress` → `verifying`
- **Result:** The tool exists and does what WI-0001 asks. 27 tests pass on the branch head, every
  criterion has a test that would fail if its behaviour were removed, and the three deviations from
  the plan and the one behaviour deliberately left unbuilt are declared in `impl-report.md` rather
  than left for verification to find.

## 2026-08-21T22:03:30Z — verify v0.1.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next`
- **Verified commit:** `5288776aeb93ae5d80a74323ba016adda2e49f46`, the head of `wi/WI-0001`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the criteria, read **first and in full**, and what would
    settle each one was written down before `impl-report.md` was opened
  - `history.md` (a straight run, no send-back to narrow the job), `artifacts/plan.md`,
    `artifacts/impl-report.md` (read after deriving the checks, and used only to look for claims
    worth challenging), `artifacts/refinement-qa.md` (for AC5's exact message strings and for the
    two behaviours recorded as unconstrained)
  - `docs/architecture/adr/ADR-0003`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008`;
    `tracker/project.yaml` for both command strings
  - The code and the diff: `expenses`, `expenses_tool/store.py`, `expenses_tool/cli.py`, both test
    modules, `README.md`, and `git diff --stat main..HEAD`
- **Decisions:**
  - **Every criterion was checked by running it, not by running the test that claims it.** The
    tests were run too, as the `tests-pass` gate, but the evidence in the report's Criteria table
    is this skill's own shell commands and their quoted output. A criterion whose only evidence was
    a passing test would establish that the test passes, not that the criterion holds.
  - **AC7 was checked against the README, not against the code's default constant.** The criterion
    says "the path the README documents as the default", so the check is `ls -A $HOME` yielding
    exactly one entry plus `grep` finding that path in `README.md` (line 54). Checking the constant
    would have verified the code against itself.
  - **No criterion was judged ambiguous**, so no question was filed. The wording left by `refine`
    named a command and an exact expected string in every case; the only judgement needed was
    `$T`'s value, which the criteria define as "a path that does not exist".
  - **Nothing was classified as a bug.** Nothing failed, and nothing was found in behaviour
    delivered by another item — there is no other delivered item yet, WI-0001 being the first.
  - **The two known gaps were recorded rather than tested around.** The unwritable `--data-file`
    path and the `PATH`-symlink install have no criterion, so verifying them would have been
    inventing a standard; both are in `## Not verified, and why`, which is where a reader of this
    item should look for what a green verdict does not cover.
  - **`lint-clean` was recorded as passing *and* as weak.** `compileall` proves the files parse.
    Calling that "lint" without qualification would misrepresent what was checked, so both the gate
    table and `## Not verified, and why` say what it does and does not establish.
- **Questions raised:** none.
- **Commands:** (every one run by this skill, on the verified commit)
  - `git rev-parse HEAD` → `5288776aeb93ae5d80a74323ba016adda2e49f46`; `git branch --show-current`
    → `wi/WI-0001`
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 27 tests in 1.042s`, `OK`
  - `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - AC1: `./expenses add-person Ana --data-file "$T"` → `stdout=[Added Ana] stderr=[] exit=0`;
    `./expenses list-people --data-file "$T"` → `stdout=[Ana] stderr=[] exit=0`
  - AC2: `bash -c './expenses list-people --data-file /tmp/vwi1/store.json'` → `Ana`, `exit=0`
  - AC3: `./expenses add-person " ana " --data-file "$T"` → `exit=1 stdout=[] stderr=[Ana is
    already registered]`; `cmp` → unchanged; `./expenses list-people … | wc -l` → `1`
  - AC4: `./expenses list-people --data-file /tmp/vwi1/absent.json` → `exit=0 stdout=[No one is
    registered yet] stderr=[]`; `test -e` → not created
  - AC5: three invocations → `exit=1` each, with `A person's name cannot be blank` twice and
    `A person's name cannot contain a comma` once, all on stderr; `cmp` → unchanged
  - AC6: three adds then `./expenses list-people | cat -A` → `ana$`, `Ben$`, `Cass$`
  - AC7: `env HOME=/tmp/vwi1/home ./expenses add-person Ana` → `exit=0 stdout=[Added Ana]`;
    `ls -A` → `.expenses.json`, count 1; `env HOME=… ./expenses list-people` → `Ana`, exit 0;
    `grep -n "expenses.json" README.md` → line 54
  - AC8: both commands against a file containing `not a data file` → `exit=1`, stderr
    `Cannot read /tmp/vwi1/garbage.json: it is not valid JSON`, no `Traceback`, `cmp` → unchanged
  - Boundary: `{"schema": 2, …}` → `exit=1`, `… it uses data file schema 2, and this version
    understands 1`; `[]` → `exit=1`, `… its top level is not a JSON object`; `./expenses
    add-nobody`, `./expenses add-person`, `./expenses` → exit 2 each
  - Sensitivity: three edits, each followed by the test command and `git checkout -- expenses_tool`
    → `FAILED (failures=5)`, `FAILED (failures=6)`, `FAILED (failures=3)`; final `git status` clean
    and the suite back to `OK`
  - `git diff --stat main..HEAD` and `git diff main..HEAD -- tracker/items/WI-0001/item.md`
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to in-review --actor verify --reason "..."` → exit 0
- **Gates:**
  - `tests-pass` → **pass**. 27 tests, exit 0, on the verified commit.
  - `lint-clean` → **pass**, with the qualification above: `compileall` is a syntax check, not a
    style linter, per ADR-0007 clause 4.
  - `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
  - `every-criterion-independently-checked` → **pass**. AC1 to AC8 each have a command this skill
    ran and its quoted output in `artifacts/verify-report.md`; the eight checkboxes in `item.md`
    were ticked only after that run.
  - `negative-cases-exercised` → **pass**. AC3, AC4, AC5 and AC8 are negative cases and were
    triggered; plus a future schema number, a JSON list, three usage errors, and the
    case-plus-whitespace duplicate.
  - **Test sensitivity** (the skill's step 5, not a named gate) → **pass**. Removing case-folding,
    making refusals exit 0, and making an unreadable file read as empty each produced failures.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new), carrying `Verified-commit:`
  - `tracker/items/WI-0001/item.md` — all eight criteria ticked
  - bug items filed: none
  - `tracker/board.md` — regenerated
- **Status:** `verifying` → `in-review`
- **Result:** WI-0001 does what its criteria say, checked command by command against commit
  `5288776`. Five things a green verdict does not cover are declared in the report: style linting,
  the `PATH` install, an unwritable `--data-file`, crash-during-write atomicity, and non-ASCII
  names through the command line.

## 2026-08-21T22:06:30Z — review-close v0.1.1 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (all eight criteria, `## Out of scope`, `## Notes`),
    `history.md` (eight rows), `journal.md` (**in full**, all seven entries — this skill certifies
    the record, which cannot be done from a skim), `questions/Q-001.md` to `Q-004.md`
  - `artifacts/plan.md`, `artifacts/impl-report.md` (including `## Deviations from the plan` and
    `## What I did not do`), `artifacts/verify-report.md` (including `## Not verified, and why`),
    `artifacts/refinement-qa.md`
  - `docs/architecture/overview.md` (v1) re-read against the code for D12; `docs/architecture/adr/`
    ADR-0001 to ADR-0008; `docs/product/vision.md` (v9)
  - **The diff:** `git diff main..HEAD` over `main..wi/WI-0001`, hunk by hunk — `expenses`,
    `expenses_tool/cli.py`, `expenses_tool/store.py`, both test modules, `README.md` — plus
    `git diff main..HEAD -- tracker/items/WI-0001/item.md` to confirm `implement` changed no
    criterion
- **Decisions:**
  - **Accepted, not countersigned.** Every hunk was mapped to a criterion or a plan step, and the
    mapping table is in `artifacts/review.md` `## What I examined`. Nothing in the diff is
    unaccounted for; the only code the plan does not name is the two usage-error tests, which
    `impl-report.md` had already declared as a deviation.
  - **Finding 1 — the unwritable `--data-file` traceback — was accepted, not sent back.** The
    behaviour is what the item's `## Notes` records as deliberately unconstrained by `refine`, and
    `impl-report.md` declares it. Sending it back would mean asking for behaviour no criterion
    covers, which is how scope grows without verification. It is written into the item's
    `## Notes` under "Accepted gaps at close", because a gap that lives only in a verification
    report stops being read the moment the item closes.
  - **Finding 2 — `except BaseException` in `save` — was noted rather than raised.** It re-raises
    immediately and exists so that an interrupt does not leave a temporary file behind, which AC7
    would then fail on. A reviewer skimming for bare-except smells will stop at it, so it is worth
    a line in the review; it is not a defect.
  - **All six declared gaps were copied into the item.** Five come from `verify-report.md`
    `## Not verified, and why` and one from the R10 note. This is the step the skill warns is
    skipped, and it is the only reason the gaps survive `done`.
  - **The verification was checked for staleness mechanically, not by eye.**
    `check-verify-freshness` reports that the branch moved from `5288776a` to `77a0ad4a` but only
    under `tracker/`, and `git log --name-only` over that range confirms it. D10 therefore holds
    on evidence rather than on the last commit looking harmless.
  - **The order was trial-merge, discard, close, then merge.** `commits-reference-the-item`
    inspects `main..wi/WI-0001`, which is empty once the branch is merged, so merging first would
    have made the gate refuse the close it gates.
  - **The epic stays `open`.** WI-0002, WI-0003 and WI-0004 are all at `draft`, so DE1 fails and
    the epic Definition of Done was not applied. Recorded here rather than left implicit, because
    this is the skill that owns epic closure.
- **Questions raised:** none. Nothing in the change contradicts an ADR, so there was nothing to
  put to the architect.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001 --root .` →
    *"verified at 5288776a; wi/WI-0001 has moved to 77a0ad4a but only the record changed (5 file(s)
    under tracker/ or docs/), so the verification still covers the code"*
  - `git log --oneline --name-only 5288776..HEAD` → one commit, five files, all under `tracker/`
  - `git branch -f trial-merge-wi0001 main; git checkout trial-merge-wi0001; git merge --no-edit wi/WI-0001`
    → clean merge
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0,
    `Ran 27 tests in 1.016s`, `OK`; `python3 -m compileall -q expenses expenses_tool tests` → exit 0
  - `git checkout wi/WI-0001; git branch -D trial-merge-wi0001` → trial discarded before closing
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001 --root . --trunk main`
    → *all 3 commit(s) on main..wi/WI-0001 name WI-0001*
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/transition WI-0001 --to done --actor review-close --outcome delivered --reason "..."` → exit 0
  - then, and only then, `git checkout main; git merge --no-ff wi/WI-0001`
- **Gates:**
  - `definition-of-done` → **pass**, criterion by criterion. The full table with evidence is in
    `artifacts/review.md` `## Definition of Done`: D1 eight ticks and no unticked criterion; D2
    eight evidence rows carrying commands and actual output; D3 gates run on `1dd3f09`, `5288776`
    and the merge result; D4 four answered questions; D5 seven journal entries against seven
    history rows; D6 eight ADRs cited from the plan and the notes; D7 the overview created at v1
    and not contradicted; D8 `check-commit-refs` clean; D9 merged after closing; D10
    `check-verify-freshness` clean; D11 this review's `## What I examined`; D12 the overview's
    three sections re-read against the code, including the launcher's `realpath` claim.
  - `verification-postdates-the-code` → **pass**. `check-verify-freshness`, quoted above.
  - `commits-reference-the-item` → **pass**. `check-commit-refs`, quoted above, run while the
    branch was still unmerged.
  - `tests-pass-on-the-merge-result` → **pass**. 27 tests and `compileall`, both exit 0, on the
    throwaway merge of `wi/WI-0001` into a copy of `main` — not on the branch head.
  - `workspace-valid` → **pass**. `validate-workspace`, exit 0, 0 errors and 0 warnings.
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0001`
    alone: what was asked (`item.md` and `refinement-qa.md`, including the four questions the
    stakeholder answered and which parts they delegated), who decided what (seven journal entries
    naming their skill and persona; ADR-0002 to ADR-0008), what was built (`plan.md`'s twelve steps
    and `impl-report.md`'s deviations), what verification found (`verify-report.md`'s commands and
    quoted output, and its sensitivity check), and what is still unchecked (six accepted gaps in
    the item's `## Notes`).
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new)
  - `tracker/items/WI-0001/item.md` — `status: done`, `outcome: delivered`, `## Notes` gains
    "Accepted gaps at close"
  - merge commit on `main`: see `git log --grep WI-0001 --merges`
  - epic: **not** closed; EP-001 stays `open` with three children at `draft`
  - `tracker/board.md` — regenerated
- **Status:** `in-review` → `done` (`outcome: delivered`)
- **Result:** WI-0001 is delivered and merged: the tool exists, `add-person` and `list-people` do
  what the stakeholder asked, and the ledger is refused rather than overwritten when it is not
  ours. Two findings, both accepted and both now recorded on the item. The epic remains open on
  WI-0002, WI-0003 and WI-0004.
