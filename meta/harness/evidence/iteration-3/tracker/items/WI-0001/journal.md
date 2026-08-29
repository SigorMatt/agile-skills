# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-28T18:26:38Z — intake v0.2.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** created by this execution; intake was invoked directly on the stakeholder's stated idea (`IDEA.md`), not dispatched by `next`
- **Inputs read:**
  - `IDEA.md` — the stakeholder's idea in their own words
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution; no prior epic or item to overlap with)
  - `docs/product/vision.md` (did not exist before this execution)
- **Decisions:**
  - See `EP-001`'s entry for how the work was split and why this item exists as the first of two.
  - AC2 says "the same length in characters" provisionally. That wording is a placeholder for
    whatever `EP-001/Q-003` settles about measuring width, and it is flagged in `## Notes` rather
    than left to look decided. Rationale: an acceptance criterion that reads as settled while
    resting on an unasked question is the failure mode `refine` exists to catch, and it is
    cheaper to mark it now than to have `verify` discover it.
  - Did not write an acceptance criterion for malformed tables (rows with unequal cell counts),
    because nothing in the idea says what should happen to one and any criterion would be
    invented. Recorded as an unknown in `## Notes` for `refine`.
- **Questions raised:** none on this item; `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003` all
  bear on its criteria and are open on the epic
- **Commands:**
  - `scripts/new-item --id WI-0001 --type work-item --title ... --epic EP-001 --priority high --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **fail at the time of writing** (`scripts/validate-workspace`, exit 1: `question.blocking.not-suspended` on EP-001, and `journal.execution.missing` on all three items — both are states this execution is in the middle of resolving; the epic's transition re-runs it)
  - `epic-has-success-measures` → **pass** (EP-001 `## Success measures` lists five signals, each of which is a command to run or an output to compare; see EP-001's entry)
  - `items-are-separable` → **pass** (WI-0001 can be built first and alone: it depends on nothing, and it delivers a working filter that pads columns. WI-0002 `depends-on` it.)
  - `no-solution-in-the-problem` → **pass** (this item's title and story name no language, library or data structure; the stakeholder said "filter", "stdin", "pads columns", and the story uses only those)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/history.md`, `journal.md` (new)
- **Status:** `—` → `draft`
- **Result:** The core item — read stdin, align table columns, pass everything else through
  untouched — created at `draft`. Three unknowns bearing on its criteria are open questions on
  EP-001; `refine` cannot pass this item until they are answered.

## 2026-08-28T18:39:49Z — refine v0.2.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (step 5; the only runnable candidate — WI-0002 is blocked by `depends-on: WI-0001`, and EP-001's `open` has no owner).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the draft as `intake` created it and `answer-questions` amended it
  - `tracker/items/WI-0001/history.md` — one row, `— → draft` by `intake`. This is a **fresh** draft, not an item sent back from `verifying` or `in-review`, so the whole story is in scope rather than a specific defect
  - `tracker/items/WI-0001/journal.md` — `intake`'s entry, for what it deliberately left unrecorded
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's three answers, verbatim; these are the ones not to ask again
  - `docs/product/vision.md` (v2) — checked the criteria against it; nothing here contradicts it
  - `docs/architecture/adr/ADR-0001-python-3-stdlib-only-stdin-filter.md`, `ADR-0002-cell-width-is-display-width.md` — AC1, AC2 and AC3 are written against these
  - `tracker/items/WI-0002/item.md` — to be sure the alignment-marker scope stays there and is not absorbed here
  - `tracker/items/EP-001/item.md` — the epic's success measures and out-of-scope list, which several criteria below are derived from
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md` §2 and §4, `spec/workspace-layout.md` §1.2–1.3
- **Decisions:**
  - **Asked the stakeholder three questions and no more.** Each was tested against `refine`'s routing rule before being filed. `Q-001` (malformed tables), `Q-002` (tables without outer pipes) and `Q-003` (tables indented in a blockquote or list) all decide what happens to text the stakeholder wrote, in files they will read, and no artifact records their intent — the first escalation condition in `spec/question.md` §4. Filed in one round, framed as one conversation, each with its own context, three options and a recommendation.
  - **Did not ask five further things that could have been questions.** Line endings and the trailing newline (AC9), escaped pipes (AC10), per-cell content preservation (AC11) and silence on stderr are all forced by decisions already recorded on the epic — its byte-for-byte measures, its "same rendered table" measure, its "spacing, not content" scope, and its "not a linter" exclusion. Asking would have been asking the stakeholder to repeat themselves. Each is recorded `[assumed]` in `refinement-qa.md` with the specific sentence it rests on.
  - **Decided the output's padding style (AC12) rather than asking, and flagged it as the assumption most worth their eye.** One space inside each pipe, the delimiter row filled with dashes. This is the one assumption here that decides what a document *looks* like rather than what survives in it, so the argument for asking was real. It was not asked because it is the near-universal convention for laid-out pipe tables, because the stakeholder gave a standing deferral on how the tool is built (`EP-001/Q-001`: "the rest of how it's built is your call"), and because it is a constant in one place — overturning it costs a line and a test. The Q&A says exactly this, so they can reject it on any of the three open questions.
  - **Rewrote AC7 from a definition into an observation.** It said what a table *is*, which is not something anyone can run. It now names the document to feed in — a grid table, a raw HTML table, and a run of pipe lines with no delimiter row — and the verdict that follows: all three come back byte-for-byte under AC4. The definition survives inside it as the rule being tested, and the second-line-is-a-delimiter-row wording is what makes "a run of pipe lines with no delimiter row" decidable.
  - **Made AC3's non-ASCII cases specific.** "Accented letters, emoji and CJK" named a class; it now names precomposed `é` (U+00E9), decomposed `e` + U+0301, an emoji carrying a variation selector, and CJK text. Those are the four cases that distinguish ADR-0002's rule from a naive one, so a test suite written against the criterion exercises the rule rather than agreeing with it.
  - **Added two exclusions to `## Out of scope`.** Line-length splitting of wide tables, and any diagnostic output. Both are things a reader could reasonably assume were included — the first because "pretty" suggests fitting, the second because a tool that meets a malformed table seems obliged to say so — and both are already settled against by the epic.
  - **Enumerated the behaviour combinations rather than leaving R10 to be judged.** This item has no flags, so the combinations are between document constructs: table next to a fence, two tables in a row, table at the first or last line, table in a blockquote or list, malformed table inside a fence, tab inside a cell. Five are decided by existing criteria; one is `Q-003`; the tab is recorded in `## Notes` as deliberately unconstrained by `refine`, with the reason.
  - **Routed three questions to `plan` instead of to a person**: the entry point's name and invocation, whether the document is streamed or read whole, and the test framework. The answer to each would be the same whoever the stakeholder was, and ADR-0001 delegates the first and third by name. AC1 now defers explicitly to what `plan` records, so the criterion stays decidable without pinning a design.
  - **Left `refinement-qa.md` at `status: agenda`.** The exchange has not happened: the questions are filed and unanswered, and the `[assumed]` entries are decisions rather than answers. Writing `recorded` would let Definition of Ready R8 pass on a conversation nobody had, which is precisely what that field exists to prevent (`spec/workspace-layout.md` §1.3).
  - **Suspended rather than guessed.** The stakeholder is asynchronous and not in this session (`SIMULATION-NOTICE.md`), which is `refine`'s documented "the human is not present" case: file the questions, move to `awaiting-answer` with `resume-to: draft`, stop. The alternative — recording the three recommendations as assumptions and passing the item Ready — would have made the item's most consequential behaviours look agreed when they were invented.
- **Questions raised:** `WI-0001/Q-001`, `WI-0001/Q-002`, `WI-0001/Q-003` — all blocking, all addressed to the human, all open, all filed in one round. Recorded in `artifacts/refinement-qa.md` as `[unresolved]` and carried in the item's `## Notes`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (before starting) → exit 0, 0 errors, 1 warning
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-28T18:38:13Z`, the `created` stamp on all three questions
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after writing the criteria and `## Notes`) → exit 0, 0 errors, 1 warning
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after filing the three questions) → exit 1, 2 errors: `question.blocking.not-suspended` and `board.stale`. Both are the expected transient state of an item that has questions filed and has not yet moved; this transition and the board regeneration resolve them
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exits 0 against the post-move state; the run-gate check on this transition is the authority, and the single remaining warning is the null `commands.test`, which ADR-0001 leaves to `plan`.
  - `definition-of-ready` → **fail**, deliberately, criterion by criterion. **R1 pass** — frontmatter complete, `type: work-item`, `epic: EP-001`, `priority: high`. **R2 pass** — the story names the role (someone who edits markdown by hand), the capability (pipe a document through and get the columns padded) and the outcome ("so that I can read and edit the table … without counting spaces"). **R3 pass** — twelve criteria, each labelled `AC<n>` as a checkbox. **R4 fail → fixed** — AC7 was a definition and is now an observation; AC3's "non-ASCII" is now four named cases; AC9–AC12 add the boundary behaviours nothing stated. No criterion now contains an unmeasurable adjective; "pretty" appears nowhere in them. **R5 pass** — four exclusions, two of them added here. **R6 fail** — three blocking questions are open, and this is the criterion that keeps the item out of `ready`. **R7 pass** — `depends-on` is empty. **R8 fail** — `refinement-qa.md` now exists but declares `status: agenda`, which R8 explicitly does not accept. **R9 pass** — one coherent change; the alignment markers stay in WI-0002. **R10 fail → partly fixed** — the combinations are now enumerated in `## Notes`; five are decided, the blockquote/list case is `Q-003`, and the tab case is recorded as deliberately unconstrained. R6, R8 and R10 close together when the three answers arrive.
  - `criteria-are-decidable` → **pass for the twelve criteria that exist**, and this is what the item leaves behind for `verify`. AC1: run the invocation `plan` records with a document on stdin, check `$?` is 0 and stdout is non-empty. AC2: for each table row, compute the ADR-0002 display width of the prefix before each `|`; the offsets must be equal across rows. AC3: the same check on a fixture containing `é`, `e`+U+0301, an emoji with U+FE0F and CJK text. AC4 and AC5: `diff <(grep -v ...)` of the non-table lines, and `cmp` on a table-free document. AC6: `tool < a.md > b.md`, `tool < b.md > c.md`, `cmp b.md c.md`. AC7: feed the three-negative fixture and `cmp` against the input. AC8: `cmp` on a document whose only pipe table is inside a fence. AC9: `od -c` on the last bytes, and a CRLF fixture. AC10: read the output row and count the cells. AC11: split both documents into cells, strip, compare. AC12: check the two spaces around every cell and that each column is exactly `2 + max` display columns wide. **Not yet decidable, by design:** what a malformed table does, whether a bare table is a table, and whether an indented table is laid out — the three open questions, which is why the item is suspended rather than Ready.
  - `qa-recorded-verbatim` → **pass for what exists, and honestly labelled for what does not**. No answer has been received, so nothing could be paraphrased into agreement: the three questions are `[unresolved]` and the five decisions are `[assumed]` with the recorded sentence each rests on. The file's `status: agenda` says the exchange has not happened, so the gate is satisfied by a file that does not claim more than it holds.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC3 made specific; AC7 rewritten as an observation; AC9, AC10, AC11 and AC12 added; two exclusions added to `## Out of scope`; `## Notes` rewritten with the open questions, the assumptions, what was routed to `plan`, and the R10 combinations
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — new, `status: agenda`: the DoR agenda as a table, the three questions, the five assumptions with their bases, and what went to `plan`
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — new, blocking, to the human
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0001 is not Ready and is suspended at `awaiting-answer` with `resume-to: draft`. Everything that did not depend on the stakeholder was done: twelve decidable criteria, four exclusions, the combinations enumerated, and five decisions taken and recorded as assumptions. Three questions carry the rest, and R6, R8 and R10 close when they are answered.

## 2026-08-28T18:47:22Z — answer-questions v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer` with three human-addressed questions whose `## Answer`
  sections had been filled in since the previous turn; run ahead of `next`, which stops the loop
  on any open human-addressed question.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (all three answered by
    the stakeholder, all three still `open`)
  - `tracker/items/WI-0001/item.md` (AC1–AC12 as `refine` left them)
  - `tracker/items/WI-0001/history.md` — the suspending row records `resume-to: draft`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (`status: agenda`, round 1)
  - `tracker/items/WI-0002/item.md` and `history.md`
  - `tracker/items/EP-001/questions/Q-001.md`..`Q-003.md` and `EP-001/history.md`
  - `docs/architecture/adr/ADR-0001-python-3-stdlib-only-stdin-filter.md` (v1)
  - `docs/architecture/adr/ADR-0002-cell-width-is-display-width.md` (v1)
  - `docs/product/vision.md` (v2)
  - `tracker/project.yaml`, `tracker/board.md`
  - No `artifacts/plan.md` exists yet — the item has never been planned — so there was nothing
    to propagate into there.
- **Decisions:**
  - Recorded all three answers as **one** ADR (ADR-0003) rather than three. Rationale: two of the
    stakeholder's sentences — *"if it doesn't understand one it should keep its hands off"* and
    *"same as any other table you don't understand"* — generalise past the question that produced
    them, and the stakeholder used the second to dispose of a case they were not asked about.
    That is an instruction to have one policy for unrecognised tables rather than a rule per
    construct, and splitting it across three ADRs would have hidden the connective tissue.
  - Q-001 (route: the human's reply, overruling `refine`'s recommendation A) → option C. Turned
    into AC13 and ADR-0003 rule 3, with cell counting defined by splitting on unescaped `|` and
    discarding the fields the outer pipes produce, so the criterion is decidable rather than
    a restatement of "malformed".
  - Q-002 (route: the human's reply) → option A. Turned into AC14 and ADR-0003 rule 4, plus an
    amendment to AC12 so the outer `|` appears in the output exactly when it was in the input.
  - Q-003 (route: the human's reply) → option B carrying option A's intent. Turned into AC15 and
    ADR-0003 rule 2: a line's prefix is its maximal leading run of space, tab and `>`, it must be
    byte-identical across the run, and it is stripped and restored around layout. Stated
    textually rather than structurally because the tool has no markdown block parser and
    "tangled" needs a rule a reader with a terminal can apply.
  - Decided, as architect and **not** as something the stakeholder said: a run whose rows
    disagree about their outer-pipe style is left byte-for-byte. Rationale: per-row preservation
    would keep Q-002's *"never the punctuation"* promise while breaking AC2's promise that the
    pipes line up, producing a table neither tidied nor left alone. Q-003's *"same as any other
    table you don't understand"* is the stakeholder disposing of the analogous case, which makes
    this derivable rather than a guess. It is recorded as a decision in ADR-0003 §Decision and
    flagged as ours — not theirs — in `refinement-qa.md`, and it is reversible additively.
  - Did **not** escalate any of the three, and did not file a fourth question. Every one had a
    direct reply, and the derived case above is settled by an answer already on the record, so
    none of the four conditions in `spec/question.md` §4 applies to it.
  - Left `refinement-qa.md` at `status: agenda` while writing the answers into it verbatim.
    Rationale: the file's own rule says it becomes `recorded` when the answers arrive, but the
    answers added three criteria, so DoR R4 and R10 have to be re-checked against the item as it
    now stands. Certifying a Definition of Ready is `refine`'s job, not this skill's, and marking
    the file `recorded` here would let the item reach `ready` on a check nobody performed. The
    reasoning is written into the file so `refine` finds it rather than re-deriving it.
  - Filed no new work item under step 3b. The answers narrow what the tool touches and add
    recognition rules to an item that already owns table detection; none of them implies work
    outside WI-0001's scope.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, three errors: an
    unresolved citation in `vision.md` (two `[src:]` targets in one bracket), the stale board,
    and `question.awaiting.none-open`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` (after splitting the citation) →
    exit 1, two errors, both expected before this transition and the board regeneration that
    follows it
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in a `## Consequences` section was opened
    after editing and the change confirmed present: ADR-0003 exists with rules 2, 3 and 4;
    `item.md` carries AC13, AC14 and AC15 and the amendments to AC2, AC7 and AC12;
    `refinement-qa.md` carries all three answers verbatim under `[answered]`; `vision.md` is v3
    with the new paragraph and the reduced open-questions list; `WI-0002/item.md` carries the
    note about recognition reaching it through AC6.
  - `answered-from-the-record` → **pass**. Q-001, Q-002 and Q-003 are each answered by the
    stakeholder's own words, quoted verbatim in ADR-0003 §Context and in `refinement-qa.md`. The
    one thing the record was silent on — mixed outer-pipe style within a run — is recorded as a
    new decision in ADR-0003 rather than asserted.
  - `escalation-is-justified` → **skipped**, no question was escalated or re-addressed to the
    human by this execution.
  - `workspace-valid` → **pass** at the point of transition for everything this skill owns: the
    citation error it introduced was fixed, and the two remaining errors are
    `question.awaiting.none-open` (which this transition clears) and `board.stale` (which
    `board-gen` clears immediately after).
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-28T18:39:49Z records
    `resume-to: draft`; this execution moves WI-0001 to `draft`.
  - `a-deferral-is-not-an-answer` → **skipped**, none of the three replies deferred. Each names
    a course of action and gives the reason for it.
- **Artifacts:**
  - `docs/architecture/adr/ADR-0003-lay-out-only-tables-the-tool-fully-understands.md` — created
    (v1): four recognition rules and the "changes spaces and nothing else" promise
  - `docs/product/vision.md` — v2 → v3: bare-pipe and indented tables named as tables, the
    never-change-punctuation promise stated, the malformed-table question removed from the open
    list
  - `tracker/items/WI-0001/item.md` — AC13, AC14 and AC15 added; AC2, AC7 and AC12 amended;
    `## Notes` rewritten, replacing "Open — waiting on the stakeholder" with what was settled and
    updating the R10 combinations list
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — three `[unresolved]` markers replaced by
    `[answered]` with the answers verbatim; a section added for what the answers settled beyond
    the three questions; the header explains why the file stays `agenda`
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — `status: answered`,
    `answered-by: human`, `answered-at: 2026-08-28T18:43:43Z`, each with a file-by-file
    `## Consequences`
  - `tracker/items/WI-0002/item.md` — `## Notes` records how the recognition rules reach it
    through AC6
- **Status:** `awaiting-answer` → `draft`
- **Result:** All three of WI-0001's blocking questions are answered from the stakeholder's own
  words and propagated into the criteria, the vision and a new ADR-0003; the item returns to
  `draft` for `refine` to re-run its Definition of Ready check against AC13–AC15.

## 2026-08-28T18:51:00Z — refine v0.2.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (step 5; the only runnable candidate, WI-0002
  being blocked on this item). The item reached `draft` from `awaiting-answer` twelve minutes
  earlier, when `answer-questions` propagated the stakeholder's replies to Q-001..Q-003 — so this
  is round 2 of an interrupted refinement, not a fresh draft and not a send-back from a later
  stage.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC15 as `answer-questions` left them)
  - `tracker/items/WI-0001/history.md` — three rows; the last is `awaiting-answer → draft`, so
    the send-back reading of precondition 3 does not apply
  - `tracker/items/WI-0001/journal.md` — including `intake`'s record of the stakeholder's
    original words and `answer-questions`' entry of 2026-08-28T18:47:22Z
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (`status: agenda`, round 1)
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` (all `answered`)
  - `docs/product/vision.md` (v3), `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1),
    `ADR-0003` (v1)
  - `tracker/items/WI-0002/item.md` — checked that no part of this scope belongs to the sibling;
    it owns alignment markers only
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - **Asked the stakeholder nothing.** Five gaps surfaced in the R4 and R10 re-walk, and the
    routing test in step 3 sent all five away from them: each would have the same answer whoever
    the stakeholder was, and all are covered by the standing deferral *"The rest of how it's
    built is your call, not mine"* (`EP-001/Q-001`). They had already answered three product
    questions on this item in round 1; a fourth round on mechanics is F-023 exactly.
  - **AC7 — defined "run".** A maximal sequence of two or more consecutive lines, none inside a
    fenced code block, each containing at least one unescaped `|`. Rationale: AC13, AC14 and
    AC15 are all conditions *on a run*, and none of them is decidable while the run's boundaries
    are left to the reader. No behaviour changed; a hole in the vocabulary closed.
  - **AC8 — defined when a fence opens and closes, and what an unclosed one does.** Three or
    more backticks or tildes after the AC15 prefix is stripped; closes on at least as many of the
    same character alone; unclosed runs to the end of the document. Rationale: the stakeholder
    settled the principle at `EP-001/Q-002` (a table in a fence is text somebody typed on
    purpose) and left the mechanics; the rule chosen is what a renderer does, which the epic's
    success measure already binds the tool to. Stripping the prefix first makes a quoted fence
    protect its contents exactly as an unindented one does — the combination AC8 and AC15 left
    unstated.
  - **AC9 — a line's terminator is not part of the line.** Rationale: this is a hole, not a
    tidy-up. Without it a CRLF document carries a `\r` into every row's last cell; `\r` is not a
    space, so AC11's strip leaves it, and AC14's "last non-whitespace character is an unescaped
    `|`" then fails on every row of the document. AC9 already promised the endings come back
    unchanged; this says where they live in between.
  - **AC10 — "escaped" means an odd number of preceding backslashes.** Rationale: AC10 said what
    `\|` is without saying what `\\|` is. The odd-count rule is the renderer's, so the tool and
    the renderer cannot disagree about a cell boundary.
  - **AC15 — a prefix change disqualifies a run rather than splitting it.** Rationale: AC15 as
    written could be read either way, and disqualifying is both the conservative reading and the
    one that matches ADR-0003's one-branch-for-anything-unrecognised policy. Splitting would have
    the tool rewrite lines adjacent to a construct it had just decided it could not parse.
  - **Did not touch AC1–AC6, AC11–AC14.** Round 1's answers are already in them and re-opening
    settled criteria wastes the stakeholder's earlier answers.
  - **Did not split the item (R9).** Fifteen criteria describe one pass over one stream:
    recognise runs, lay out the ones that qualify, copy the rest. AC13–AC15 are recognition
    conditions on that same pass, not separate deliverables.
- **Questions raised:** none this round. Round 1's three (`Q-001`, `Q-002`, `Q-003`) are answered
  and recorded verbatim in `artifacts/refinement-qa.md`; nothing is left `[unresolved]`, and the
  five decisions above are tagged `[assumed]` there with the basis each rests on.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 (1 warning:
    `commands.test` is null, which is `plan`'s to fill)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors)
  - `definition-of-ready` → **pass**, criterion by criterion against `spec/dor-dod.md` §1:
    - R1 **pass** [auto] — `id`, `type`, `epic: EP-001`, `priority: high`, `created`, `updated`
      all present; validator exit 0.
    - R2 **pass** — the story names the role ("someone who edits markdown documents by hand"),
      the capability ("pipe a document through a command and get it back with every table's
      columns padded to a common width") and the outcome ("so that I can read and edit the table
      in a plain text editor without counting spaces").
    - R3 **pass** [auto] — fifteen criteria, each labelled `AC<n>` as an unticked checkbox.
    - R4 **fail on entry → pass after this round.** AC1–AC6 and AC11–AC14 were already decidable.
      Four were not: AC7 used "run" without bounding it, AC8 named fenced code blocks without
      saying when one opens or closes, AC10 said `\|` without defining "escaped", and AC15 did
      not say whether a mid-run prefix change splits or disqualifies. AC9 was decidable but
      incomplete in a way that broke AC11 and AC14 on CRLF input. All five rewritten above; no
      criterion now contains an unmeasurable adjective.
    - R5 **pass** — six exclusions, of which "Honouring the alignment markers" and "Any
      diagnostic output" are both things a reader would reasonably assume were included.
    - R6 **pass** [auto] — no open question on this item; Q-001..Q-003 are `answered`.
    - R7 **pass** [auto] — `depends-on` is absent; nothing blocks this item. WI-0002 depends on
      it, not the reverse.
    - R8 **fail on entry → pass after this round.** `refinement-qa.md` was `status: agenda`,
      deliberately, because `answer-questions` declined to certify a Definition of Ready on this
      skill's behalf. It is now `recorded`: round 1's three questions with the stakeholder's
      answers verbatim, round 2's five `[assumed]` decisions with their bases, and the routing
      of the rest to `plan`.
    - R9 **pass** — one coherent change; see Decisions.
    - R10 **fail on entry → pass after this round.** The item introduces no flags, options or
      modes, so the combinations are between document constructs. Four were unstated and are now
      named in `## Notes`: a fenced block inside a blockquote and an indented fence (decided by
      AC8), an unclosed fence at the end of a document (AC8), a one-column table written without
      pipes (AC7), a run that changes indentation part-way (AC15), and a tab in the AC15 prefix
      (AC15, byte-for-byte comparison). The pre-existing six remain named and decided.
  - `criteria-are-decidable` → **pass**. For each criterion, the observation that settles it:
    - AC1 — run the invocation `plan` records with a document on stdin; observe stdout is
      non-empty and `$?` is 0.
    - AC2 — for each table in the output, compute each row's display width by ADR-0002's rule and
      the column of each `|`; all rows equal, all *n*th pipes equal → pass.
    - AC3 — the same computation on a fixture containing `é` (U+00E9), `e`+U+0301, an emoji with
      U+FE0F, and CJK text.
    - AC4 — `diff` the non-table lines of input and output; any difference → fail.
    - AC5 — `cmp doc <(tool < doc)` on a table-free document.
    - AC6 — `tool < doc > o1; tool < o1 > o2; cmp o1 o2`.
    - AC7 — feed the fixture the criterion names (RST grid table, HTML `<table>`, pipe lines with
      no delimiter row); `cmp` input and output.
    - AC8 — feed a document whose fenced block holds a ragged pipe table and whose final fence is
      missing; `cmp` input and output over those lines.
    - AC9 — `od -c` the last bytes of input and output; compare terminators.
    - AC10 — feed `| a \| b | c |`; count the output's unescaped pipes and read cell one.
    - AC11 — for every cell, `strip(input_cell) == strip(output_cell)` byte-for-byte.
    - AC12 — for each laid-out row, check the character after each `|` is a space, the one before
      the next `|` is a space, and each column measures `2 + max(display width)`.
    - AC13 — feed the ragged-table fixture; `cmp` input and output over the run.
    - AC14 — feed a bare-pipe table, an outer-pipe table and a mixed one; count `|` per line in
      input and output, and `cmp` the mixed run.
    - AC15 — feed the blockquote, list-indent and irregular-prefix fixtures; `cmp` for the third,
      and the AC2 computation for the first two.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` is `status: recorded` and
    carries all three round-1 questions with the stakeholder's replies quoted from the question
    files, tagged `[answered]`, plus five `[assumed]` entries from this round each naming what it
    rests on. Nothing is `[unresolved]`; nothing was paraphrased into agreement — Q-001's answer
    is recorded as overruling `refine`'s own recommendation.
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC7, AC8, AC9, AC10 and AC15 tightened; `## Notes` gained
    the round-2 assumptions and five more R10 combinations
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `agenda` → `recorded`; round-2 section
    added with the five `[assumed]` decisions and why none of them went to the stakeholder
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0001 meets the Definition of Ready on all ten criteria with no override; the
  five gaps found this round were mechanical, were decided under the stakeholder's standing
  deferral, and are recorded as assumptions rather than as answers anyone gave.

## 2026-08-28T18:57:30Z — plan v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` (step 5; the only runnable candidate). This is
  the project's first planned item — there is no source code, and `docs/architecture/overview.md`
  did not exist, so precondition 3 applies and this execution created it.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC15, the contract this design satisfies
  - `tracker/items/WI-0001/history.md` — five rows; the last is `draft → ready` from `refine`, so
    this is a first plan and not a re-plan after a rejection
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (`status: recorded`) — in particular the
    nine `[assumed]` entries, which are the design's soft ground, and the three items routed to
    `plan`: the entry point, streaming versus reading whole, and the test framework
  - `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1), `ADR-0003` (v1) — read in full; none
    is contradicted by this plan
  - `docs/product/vision.md` (v3)
  - `tracker/project.yaml` — `commands.test`, `commands.lint` and `commands.build` all null
  - `tracker/items/WI-0002/item.md` — to confirm the alignment-marker scope stays out of this plan
  - The project's source code: there is none. `find . -name '*.py'` outside `.claude/` and
    `.git/` returns nothing, so "read the code that already exists" resolved to reading the
    scripts' own layout under `.claude/agile-skills/scripts/` for conventions and nothing else.
- **Decisions:**
  - **How the document is read and written** — bytes in and out, decoded once with UTF-8 and
    `errors="surrogateescape"`, terminators split off into `(content, terminator)` pairs.
    Recorded as ADR-0004 because there is a real alternative (text mode with `newline=""`) that
    looks correct and silently breaks AC9, AC4 and AC5 on CRLF input, and because the choice of
    `surrogateescape` is what lets the tool honour AC4 on a document it cannot decode. Route:
    decided.
  - **The test and lint toolchain** — `unittest` and file fixtures, with
    `python3 -W error -m compileall -q mdtab tests` as lint. Recorded as ADR-0005. Route:
    decided. The lint choice is deliberately modest and the ADR says so: it catches invalid
    escape sequences, which is the one defect class a codebase about `\|` will actually produce,
    and nothing else. Measured rather than assumed: none of ruff, flake8, pyflakes, pycodestyle,
    pylint, mypy or pytest is importable here.
  - **Module boundaries** — six modules, with a named list of rules that live in exactly one
    place each (width, what a line is, where a cell boundary is, whether a run is a table).
    Recorded in `docs/architecture/overview.md` v1. Route: decided.
  - **A column's width excludes the delimiter row's own cell.** Route: decided, and forced —
    including it would make the column grow on each run and break AC6. Written into the plan as
    a rule the implementation may not read freely.
  - **An all-empty centred column is one character wider than AC12's formula.** Route: assumed,
    and recorded under `## Assumptions` and again under `## Risks`, because it is the single
    place where AC12 and AC6 cannot both hold literally and AC6 was given priority. Reversing it
    is an amendment to AC12 through `answer-questions`, not a code change. This is flagged rather
    than smoothed over precisely so `verify` does not discover it as a defect.
  - **Read the document whole rather than streaming it.** Route: assumed; reversible inside one
    module, and no criterion distinguishes the two. This was one of the three things `refine`
    routed here.
  - **One invocation, `python3 -m mdtab` from the checkout root.** Route: assumed. A `bin/mdtab`
    shebang script is four lines and would work from any directory, and it is deliberately left
    out because no criterion asks for it — adding it would be designing past the item. The
    assumption says what it would cost to add.
  - **Minimum interpreter CPython 3.8**, which ADR-0001 delegated here. Route: assumed, and
    explicitly recorded as asserted rather than verified: only 3.12.3 is installed, so the floor
    is a constraint on the code that review must enforce.
  - **Asked the human nothing.** Every choice above is cited to a document or recorded as a
    reversible assumption; none is irreversible and none turns on intent no document records,
    which are the only two conditions that would justify asking.
  - **Did not update the vision or ADR-0001..0003.** Nothing here changes what the product is
    for or contradicts a recorded decision, and a version bump with no substantive change
    devalues every other one.
- **Questions raised:** none
- **Commands:**
  - `python3 -c "import <pkg>"` for ruff, flake8, pyflakes, pycodestyle, pylint, mypy, pytest →
    all ImportError; no third-party tooling is available
  - `python3 -VV` → CPython 3.12.3
  - `python3 -W error -m compileall -q` on a file containing `x = "a\|b"` → exit 1,
    `SyntaxError: invalid escape sequence '\|'`; on the corrected file → exit 0. This is the
    evidence that the lint command checks something real.
  - `python3 -m unittest discover -s tests -t .` → exit 5, `NO TESTS RAN` (the honest signal:
    the command runs, and there are no tests yet). With one throwaway passing test present it
    exited 0, and the throwaway was deleted.
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 with five
    unsourced absolute claims, then exit 0 after each was sourced
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors and 0 warnings; the
    `project.commands.test-null` warning that has been present since the workspace was created is
    now gone, because this execution filled the commands in)
  - `every-criterion-is-addressed` → **pass**. `plan.md` carries a fifteen-row
    `## Acceptance criteria mapping` table, one row per AC1–AC15, each naming the numbered step
    that satisfies it and a specific demonstration — a named fixture pair, a named unit test, or
    a named command with the verdict that follows. No row says "tests". No AC is unmapped and no
    step is unreferenced by the table.
  - `project-commands-resolved` → **pass**. `commands.test` is
    `python3 -m unittest discover -s tests -t .` and `commands.lint` is
    `python3 -W error -m compileall -q mdtab tests`; both were run, see `**Commands:**`. The test
    command currently exits 5 rather than 0 because no test exists yet — that is the command
    reporting truthfully, and it was proved to exit 0 with a test present. Neither command exits
    zero without checking anything. `commands.build` stays null, with the reason in the plan's
    `## Assumptions`: there is nothing to build.
  - `decisions-recorded` → **pass**. `plan.md` `## Decisions and ADRs` is a table of every choice
    this plan makes, each pointing either at an ADR (ADR-0004, ADR-0005, the overview) or at an
    entry under `## Assumptions` that states what reversing it would cost. Three of the seven are
    citations to decisions already recorded (ADR-0001, ADR-0002, ADR-0003) rather than new ones.
  - `plan-is-executable-without-you` (advisory) → **pass**. Twelve numbered steps, each naming
    the file it creates and what is true afterwards; the three module interfaces the developer
    must not invent are given as signatures in `## Approach`, and the two layout rules that are
    not free readings of AC12 are written out with the reason AC6 forces them. The step most
    likely to need a decision the plan does not make was step 6, which is why the delimiter-row
    exclusion and the minimum-width rule are stated there rather than left to the reader.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0, after sourcing
    five absolute claims the first run caught in ADR-0004, ADR-0005 and the overview; the same
    run also surfaced that ADR-0004 named a module `mdtab/io.py` that the overview and the plan
    call `mdtab/textio.py`, and the ADR was corrected)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` (new) — problem, approach with fixed interfaces,
    twelve steps, the fifteen-row AC mapping, five assumptions, the decisions table, scaffolding,
    five risks, and what is out of scope
  - `docs/architecture/adr/ADR-0004-document-is-bytes-round-tripped-through-utf-8.md` (new, v1)
  - `docs/architecture/adr/ADR-0005-tests-and-lint-come-from-the-standard-library.md` (new, v1)
  - `docs/architecture/overview.md` (new, v1) — the four-stage shape, the module table, and the
    rules that live in exactly one place
  - `tracker/project.yaml` — `commands.test` and `commands.lint` filled in
  - `mdtab/__init__.py`, `tests/__init__.py` — scaffolding, both empty, both listed under
    `## Scaffolding` with the gate command that cannot execute without them
  - `tracker/board.md` — regenerated
- **Status:** `ready` → `planned`
- **Result:** WI-0001 is planned: twelve steps against fifteen mapped criteria, two new ADRs, the
  project's first architecture overview, and both gate commands filled in and run. The one place
  where two criteria conflict is recorded as an assumption with AC6 given priority, so
  `implement` and `verify` meet it as a decision rather than as a surprise.

## 2026-08-28T18:59:20Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next` as the only runnable item (WI-0002 waits on
  this one, EP-001's `open` has no owner)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — fifteen acceptance criteria, the out-of-scope list, and the
    notes recording what was settled by the stakeholder and what is `[assumed]`
  - `tracker/items/WI-0001/artifacts/plan.md` — twelve steps, three fixed module interfaces, the
    AC mapping, and the two layout rules AC6 forces
  - `tracker/items/WI-0001/history.md` — five rows, last one `ready` → `planned`; no send-back, so
    this is a first execution and not a resumption
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three `answered` and
    already propagated into the criteria and ADR-0003; nothing new to read out of them
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, `docs/architecture/overview.md` — the
    constraints the plan assumes but does not restate
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, `commands.test` and
    `commands.lint`
- **Decisions:**
  - none yet — this entry opens the execution. The plan's twelve steps are executed in order and
    every choice made inside their latitude is recorded in the closing entry.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001` → 0 (branched from `main`; nothing was on it, so there is no
    partial work to reconcile with)
- **Gates:**
  - `tests-pass` → **not yet run** — no code exists on the branch; the gate runs on the branch
    head after the last change
  - `lint-clean` → **not yet run** — same reason
  - `workspace-valid` → **not yet run** — runs with the other completion gates
  - `every-criterion-has-a-test` → **not yet run** — no test exists yet
  - `commits-reference-the-item` → **not yet run** — the branch has no commits yet
  - `no-unplanned-scope` (advisory) → **not yet run** — there is no diff yet
  - `claims-are-sourced` → **not yet run** — nothing has been written yet
- **Artifacts:**
  - branch `wi/WI-0001`, created from `main` at d1efa81
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0001 has started on `wi/WI-0001`. Nothing is built yet; this
  entry exists so that an interruption from here on leaves a truthful status and a reader knows
  which branch holds the work.

## 2026-08-28T19:10:21Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress` on branch `wi/WI-0001`; this entry closes the execution the
  entry above opened
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, re-read against the finished diff
  - `tracker/items/WI-0001/artifacts/plan.md` — the twelve steps, the three fixed interfaces, the
    two layout rules AC6 forces, and the five assumptions
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, `docs/architecture/overview.md`
  - `tracker/project.yaml` — both gate commands
  - the branch itself at each step, and the four commits it now carries
- **Decisions:**
  - **AC11 does not govern the delimiter row; AC12 does.** Read literally the two disagree — AC11
    says a cell's content survives, AC12 says the delimiter row is refilled with `-` to the
    column's width. AC12 is the specific rule, plan step 6 instructs it, and AC2 is unsatisfiable
    otherwise, so the delimiter row is excluded from the AC11 test and checked by the AC12 tests
    instead. Recorded loudly in `impl-report.md` because a literal reading of AC11 would find
    every laid-out table in breach.
  - **Cell content is trimmed of spaces (U+0020) only, not of all whitespace.** AC11 says
    "leading and trailing spaces". `str.strip()` would fail it literally for a cell holding a tab;
    `strip(" ")` keeps it true as written. The plan does not state which.
  - **The delimiter row's minimum width is applied to the delimiter *field*, not to the column.**
    A table written without outer pipes loses one of the two spaces on its first and last columns,
    so the field is narrower than the column by exactly the spaces that were omitted. For every
    table with outer pipes this is arithmetically the plan's own rule.
  - **A fixture beyond the plan's list, `tab-prefix`.** A mutation check found that deleting the
    prefix-equality rule broke no test: the plan's `ragged-prefix` fixture happens to be rejected
    by the outer-pipe rule first. `tab-prefix` — a blockquote table with one tab-indented row —
    and a matching unit test now isolate rule 2.
  - **`find_runs` imports `has_unescaped_pipe` inside its body**, because `mdtab.table` imports
    `line_prefix` from `mdtab.scan`. The cell-boundary rule stays in `mdtab.table`, as the
    overview requires; only the import site moved, with a comment saying why.
  - **Escalated nothing.** Every choice above is a reading of two criteria that already exist or a
    mechanical consequence of a plan step, none changes what a user gets in a way no criterion
    covers, and each is cheap to reverse. The one place a criterion is genuinely not met literally
    — the all-empty centred column, three columns wide rather than two — was decided by `plan`
    before this skill ran and is fixture `empty-cells`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001` → 0
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 54 tests ... OK` (run after the last
    commit, on the branch head)
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → 0, "all 4
    commit(s) on main..wi/WI-0001 name WI-0001"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0, no document
    changed on this branch
  - `python3 -m mdtab < tests/fixtures/basic-ascii.in.md` → 0, aligned document on stdout, stderr
    0 bytes
  - `python3 -m mdtab < tests/fixtures/crlf.in.md | od -c | tail -1` → the document ends `| \r \n`
  - `python3 -m mdtab < unicode-mixed.in.md | python3 -m mdtab | cmp - unicode-mixed.out.md` → 0
  - eleven one-line mutations of the source, each followed by the test command, to check the suite
    would notice the behaviour being removed → ten failed as they should; the eleventh is the
    prefix-rule gap under **Decisions**, which was fixed rather than reported
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 54 tests, run
    on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests`, exit 0). Claimed as
    nothing more than ADR-0005 claims for it: it compiles every module and turns syntax warnings
    into errors. Style and dead code are review's job.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 3 items and 7 documents checked)
  - `every-criterion-has-a-test` → **pass**. `impl-report.md`'s table names, for each of the
    fifteen, either a test function or a command with its output. AC1 is the one criterion that
    needs the process boundary and has two subprocess tests; every other criterion is checked
    against `format_document`, which is what `python3 -m mdtab` calls.
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001`, exit 0, four
    commits, all naming the item)
  - `no-unplanned-scope` (advisory) → **pass**. Every file in `git diff --stat main..HEAD` maps to
    a numbered plan step, and no unrelated defect was fixed on the way.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0). Vacuous here: no
    document under `docs/` changed on this branch, and the gate says so itself.
- **Artifacts:**
  - branch `wi/WI-0001`, commits `d4cfb38..f7fe1c5` (four, all referencing WI-0001)
  - `mdtab/textio.py`, `mdtab/width.py`, `mdtab/scan.py`, `mdtab/table.py`, `mdtab/filter.py`,
    `mdtab/__main__.py` (all new)
  - `tests/test_fixtures.py`, `tests/test_units.py` (new) — 54 tests
  - `tests/fixtures/` — 21 pairs, all bytes, all expected outputs written by hand
  - `.gitattributes` (new) — `tests/fixtures/** -text -diff`, so the CRLF and no-final-newline
    fixtures survive a clone
  - `tracker/items/WI-0001/artifacts/impl-report.md` (new)
- **Status:** `in-progress` → `verifying`
- **Result:** mdtab is built and every one of the fifteen criteria has a test or a reproducible
  command behind it: 54 tests over 21 hand-written fixture pairs, all seven gates green on the
  branch head. Three readings that the plan left open are recorded as decisions rather than
  buried — the delimiter row being AC12's business and not AC11's is the one most likely to look
  like a defect to a literal reading of AC11.

## 2026-08-28T19:16:18Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, read **before** the implementation
    report, so that what would settle each one was derived from the criterion and not from what
    was built
  - `tracker/items/WI-0001/history.md` — six rows; no send-back, so this is a first verification
  - `tracker/items/WI-0001/artifacts/plan.md` — the twelve steps and the five assumptions, read
    for step 6, "anything in the code no criterion or plan step accounts for"
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read as a claim to check, cited as evidence
    for nothing
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — read because AC11's wording is contested
    against AC12's; it settles the tension, framing AC11 as the guard against a tool that "quietly
    trims, escapes or rewraps something inside a cell"
  - `tracker/project.yaml` — both gate commands
  - the code on branch `wi/WI-0001` at `175101a828e7fc71437c20cdb74171bd56c3e651`
- **Decisions:**
  - **AC12: pass, with the tension between its own two clauses recorded rather than escalated.**
    For a column whose cells are all empty and whose marker is `:---:`, AC12's "exactly `2 + max`"
    gives 2 and AC12's own "the delimiter row's cells are filled with `-` to the same width,
    keeping any `:`" cannot be satisfied at 2. The tool renders 3, which is the only width
    satisfying the delimiter clause and AC6 together, and `plan.md` decided that before
    implementation and recorded it under `## Assumptions` and `## Risks`. No question was filed
    because the escalation condition is "ambiguous **and** the record does not settle it", and the
    record settles it; escalating would stop the pipeline without producing new information. The
    wording of AC12 is what should be amended, and `verify-report.md` says so under
    `## Defects found` for `review-close` to act on.
  - **AC11: pass, and the delimiter row is excluded from its scope.** AC11 read absolutely would
    forbid refilling the delimiter row with `-`, which AC12 requires and AC2 depends on.
    `refinement-qa.md` frames AC11 as a per-cell restatement of the epic's "changes spacing, not
    content" boundary, which is about content cells. Verified on a laid-out table containing a
    tab, `*bold*`, an escaped pipe and a trailing backslash.
  - **The insensitive test is a recorded finding, not a send-back and not a bug.** Replacing
    `cell.strip(" ")` with `cell.strip()` — which would eat a tab at either end of a cell — leaves
    all 54 tests passing, because no fixture has such a cell. But AC11 itself is met, demonstrated
    by a command here, so no acceptance criterion of this item fails; a send-back is defined by a
    failing criterion. It is not another item's behaviour either, so it is not a bug item. The
    gate it fails, `tests-would-fail-without-the-change`, is advisory, and recording it is what
    that gate is for.
  - **The first AC11 attempt was thrown away and redone.** The document I first wrote contained
    `` `x|y` `` in a header, whose unescaped `|` made the run ragged, so the table was never laid
    out and the assertion passed vacuously. The replacement asserts the table changed before
    comparing cells. Noted because a vacuous pass is exactly what this skill exists to catch.
  - **No criterion was judged `ambiguous`,** and no criterion was ticked on the strength of a
    fixture the implementation shipped with — every document used as evidence was written during
    this execution.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `175101a828e7fc71437c20cdb74171bd56c3e651`; `git status --short` clean
    for `mdtab/` and `tests/`
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 54 tests in 0.068s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, 0 errors, 0 warnings
  - AC1: `python3 -m mdtab < ac1.md > out 2> err` → exit 0, stderr 0 bytes, aligned document on
    stdout; `grep -hE '^import |^from ' mdtab/*.py` → only `re`, `sys`, `unicodedata`, `__future__`;
    `ls setup.py pyproject.toml requirements.txt` → all three absent
  - AC2, AC3, AC15: `python3 /tmp/vfy/check.py <output> <lo> <hi>` — a display-width and
    pipe-column checker written for this verification that imports nothing from `mdtab` → all rows
    28 columns wide, pipes at 0, 7, 22, 27 in every row of the unicode table; the same check on the
    blockquote table
  - AC4: `diff` of the eleven non-table lines of a mixed document, input against output → no output
  - AC5: `python3 -m mdtab < ac5.md | cmp - ac5.md` → 0
  - AC6: four documents each run twice and `cmp`'d → identical; the degenerate `:---:` column too
  - AC7: `python3 -m mdtab < ac7.md | cmp - ac7.md` (RST grid, HTML table, pipe run with no
    delimiter row, near-delimiter `|--x-|---|`) → 0; plus the two-line-run and
    first-and-last-line boundaries
  - AC8: `python3 -m mdtab < ac8.md | cmp - ac8.md` (ragged table in a fence, fence in a
    blockquote, indented `~~~`, unclosed ` ```` `) → 0; plus table-after-fence and
    longer-fence-not-closed-by-shorter
  - AC9: `od -c` on the output of a CRLF document, a document with no final newline, a mixed
    document, an empty document, a lone `\n`, and a bare `\r` inside a cell → every terminator
    preserved, none invented
  - AC10: `python3 -m mdtab` on `| a \| b | one cell |` → two cells, first still `a \| b`; on
    `| a \\| b | c |` → laid out as three columns
  - AC11: a script asserting the table was laid out, then comparing every content cell
    space-stripped → `True`
  - AC12: `python3 -m mdtab < ac12.md | cat -A` plus a script recomputing `2 + max` per column
    from an independent width function → `[7,7,7]`, `[3,3,3]`, `[4,4,4]`; delimiter cells
    `':------'`, `':-:'`, `'---:'`; all-empty plain column renders `|--|` with two-space cells
  - AC13: `cmp` on a table with a long row and a short row, and on one whose delimiter row is
    short → both byte-for-byte
  - AC14: the tool on bare, leading-only, trailing-only and mixed documents; `tr -cd '|' | wc -c`
    on seven documents, input against output → 3→3, 6→6, 6→6, 7→7, 15→15, 13→13, 24→24
  - AC15: six documents — `> `, two-space list indent, `>` plus extra spaces, tab-for-space,
    nested `>>`, and a prefix that changes part-way → two laid out inside their prefix, four
    byte-for-byte, the last as a whole run
  - step 6: an `ast` walk listing every module-level name in `mdtab/`, and
    `grep -nE "open\(|os\.environ|getenv|socket|urllib|subprocess|sys\.argv|stderr|input\("
    mdtab/*.py` → two docstring matches and no code match
  - sensitivity: fourteen one-line mutations, each followed by `python3 -m unittest discover -s
    tests -t .`, each file restored afterwards → thirteen `FAILED`, one `OK`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 54 tests, run
    here on the branch head)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests`, exit 0; claimed as
    nothing more than ADR-0005 claims for it — syntax and syntax warnings only)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass**. `verify-report.md`'s table records, for
    each of the fifteen, a command run in this execution and its actual output. Every input
    document was written here; no shipped fixture and no line of `impl-report.md` is cited as
    evidence for any criterion.
  - `negative-cases-exercised` → **pass**. Twenty boundary and negative conditions were produced
    and run, listed in `verify-report.md`: empty input, a lone newline, no final newline, a bare
    `\r` in a cell, mixed terminators, a two-line run, a table at the document's first and last
    line, a lone pipe line, a short delimiter row, long and short body rows, a near-delimiter row,
    a table after a closing fence, an unclosed fence, a long fence "closed" by a short one, a
    quoted fence, an indented fence, both all-empty-column cases, `\\|`, and an argument the tool
    has no meaning for.
  - `tests-would-fail-without-the-change` (advisory) → **partial**. Fourteen behaviours removed
    one at a time; thirteen were caught. The fourteenth — re-trimming cell content with
    `str.strip()` instead of `strip(" ")` — left all 54 tests passing. Recorded in
    `verify-report.md` under `## Defects found`.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` (new) — the verdict, the fifteen-row
    criteria table with commands and actual output, the gates, twenty negative and boundary cases,
    the fourteen-row sensitivity table, two findings, and four things not verified
  - `tracker/items/WI-0001/item.md` — all fifteen checkboxes ticked, each on the strength of a
    command in the table above
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0001 passes verification against `175101a`. All fifteen criteria were checked with
  commands run here on documents written here, twenty negative and boundary cases were triggered
  rather than read about, and thirteen of fourteen behaviour removals were caught by the suite.
  Two things go to `review-close` rather than back to the developer: AC12's "exactly `2 + max`"
  wording contradicts AC12's own delimiter clause for one degenerate column and should be amended
  rather than coded around, and one test would not notice cell content being re-trimmed of all
  whitespace.

## 2026-08-28T19:21:09Z — review-close v0.5.0 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, all ticked, and the out-of-scope list
  - `tracker/items/WI-0001/history.md` — eight rows, chaining without a gap, last row matching the
    item's status
  - `tracker/items/WI-0001/journal.md` — all eight entries **in full**, one per history row
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all `answered`; I opened
    the files each `## Consequences` list names and confirmed the changes are there
  - `tracker/items/WI-0001/artifacts/plan.md`, `impl-report.md`, `verify-report.md` — including
    `## Deviations from the plan`, `## What I did not do` and `## Not verified, and why`
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` and `docs/architecture/overview.md`, opened for
    the D12 claim audit rather than skimmed
  - `docs/product/vision.md`
  - **the diff `main..a23c799`**, hunk by hunk — six modules under `mdtab/`, two test modules, 21
    fixture pairs and `.gitattributes`
- **Decisions:**
  - **Rejected on D12.** Two of the eleven absolute claims I audited are false against the code.
    (1) ADR-0005 says "Fixtures are the only place a test may express a document; a test may not
    build one from a Python literal", and `test_ac9_undecodable_bytes_survive_the_round_trip`
    builds both the document and its expected output as bytes literals and runs them through the
    whole-document entry. (2) `docs/architecture/overview.md` says the cell-boundary rule is "one
    function, used by the cell-count rule, **the outer-pipe test** and the layout alike, so the
    three cannot disagree", and `has_trailing_pipe` bypasses `split_row` for a second expression of
    the escaping rule. Both were found by opening the cited code, not by reading the sentences.
  - **The undeclared deviation is what makes finding 1 a rejection rather than a note.**
    `impl-report.md` declares five deviations and this is not among them, and `test_fixtures.py`'s
    own docstring asserts "Every document in this file comes from `tests/fixtures/`", which is
    false. A rule broken silently on the project's first item is a rule that is gone.
  - **The insensitive test goes back with it.** `verify` recorded under its advisory gate that
    replacing `strip(" ")` with `strip()` leaves all 54 tests green. That is `implement`'s own
    self-check 1 unmet for AC11. Since the item is returning anyway, it is listed as a must-fix
    rather than carried forward as an accepted gap.
  - **Finding 3 is a should-fix, not a separate bug item.** It is this item's own code and this
    item's own architecture document, so it belongs in the send-back; a bug item is for behaviour
    another item delivered, and no other item has delivered any.
  - **AC12's wording is an accepted gap, not a defect, and `implement` is told not to touch it.**
    No width satisfies both of AC12's own clauses for an all-empty `:---:` column; the tool renders
    the only one satisfying the delimiter clause and AC6 together, which `plan` decided and
    `verify` confirmed. Amending an acceptance criterion belongs to `answer-questions`, not to the
    developer and not to me. Written into `item.md`'s `## Notes` so it survives the item.
  - **The verification is not stale, so this is `in-progress` and not `verifying`.**
    `check-verify-freshness` reports the branch has moved past the verified commit but only under
    `tracker/`, so the verification still covers the code. The rejection is about the tests and the
    record, not about a stale check.
  - **Not merged.** The trial merge was run and was clean, and `commands.test` passed on the merge
    result, but a rejected item is not merged; the trial was discarded and `main` confirmed
    unmoved at `d1efa81`.
- **Questions raised:** none. Finding 1 is not "unclear which should give way" — ADR-0005 is a
  deliberate decision three skills old and the test is trivially convertible to a fixture, so the
  change is what is wrong. Finding 3 offers superseding the overview's sentence as the alternative
  if two expressions of the rule are genuinely wanted, which would then be a question for
  `answer-questions` rather than a decision for me.
- **Commands:**
  - `check-verify-freshness WI-0001 wi/WI-0001` → 0: "verified at 175101a8; wi/WI-0001 has moved
    to a23c799d but only the record changed (5 file(s) under tracker/ or docs/)"
  - `check-commit-refs WI-0001 wi/WI-0001` → 0, "all 6 commit(s) on main..wi/WI-0001 name WI-0001"
  - `lint-claims --changed-since main` → 0, "checked no documents changed since main"
  - `check-epic-signoff WI-0001` → 0, "WI-0001 is a 'work-item', not an epic … PASS"
  - `validate-workspace .` → 0, 0 errors, 0 warnings
  - `python3 -m unittest discover -s tests -t .` on the branch head → 0, `Ran 54 tests`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `git rev-parse main` → `d1efa811…` before the trial
  - `git worktree add --detach /tmp/trial main` → 0; `git -C /tmp/trial merge --no-ff wi/WI-0001`
    → 0, trial HEAD `e5045820…`; `python3 -m unittest discover -s tests -t .` **inside the trial**
    → 0, `Ran 54 tests`, `OK`; `git worktree remove --force /tmp/trial` → 0
  - `git rev-parse main` → `d1efa811…` after the trial — unchanged; `git worktree list` shows only
    the main checkout
  - D12 audit: `grep -rn "normalize\|normalise" mdtab/` → no match; `grep -n splitlines mdtab/
    tests/` → one docstring only; every `len(` in `mdtab/` outside `width.py` read individually
    (sixteen, none a display width); `display_width` run on the precomposed and decomposed `é` →
    1 and 1; `sed -n '229,242p' tests/test_fixtures.py` → the literal document quoted in
    `review.md`; `grep -n "def has_trailing_pipe" -A 5 mdtab/table.py` → the second escaping rule
  - `git diff main..HEAD -- mdtab/` read in full, and `git diff --stat main..HEAD` mapped file by
    file to the plan's twelve steps
- **Gates:**
  - `definition-of-done` → **fail**. Walked D1–D12 individually; the per-criterion table is in
    `review.md`. D1–D8, D10 and D11 pass with the evidence recorded there; **D12 fails** on two
    false claims; D9 is not met because a rejected item is not merged.
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness`, exit 0 — the only
    commits after the verified `175101a8` touch `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, six commits)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` run
    inside the detached trial worktree after `merge --no-ff`, exit 0, `Ran 54 tests`, `OK`). The
    merge result is sound; it is simply not being published, because the item is rejected.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0001`
    alone: *what was built and why* — `item.md`'s fifteen criteria and `plan.md`'s problem
    statement; *which skill decided what* — eight journal entries with persona and version, and
    ADR-0001–0005 each naming its decider; *what questions arose and how they were resolved* —
    three questions on this item and three on the epic, each with the stakeholder's answer verbatim
    and a `## Consequences` list whose named files I opened; *what verification found* — the
    fifteen-row criteria table, twenty boundary cases and the fourteen-row sensitivity table in
    `verify-report.md`. Nothing I needed was missing.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0). Vacuous on this
    branch — no document under `docs/` changed on it — and the gate says so itself. It proves
    citations *resolve*; the reading that decides whether they *support* their sentences is the
    D12 audit above, and that is what failed.
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0001` → 0: "WI-0001 is a
    'work-item', not an epic — the termination gate applies to an engagement's ending only"). The
    engagement is not at rest: `engagement-state EP-001` reports **active**, still in flight
    WI-0001 and WI-0002.
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, an eleven-row claim
    audit, the twelve-row Definition of Done table, four findings and three accepted gaps
  - `tracker/items/WI-0001/item.md` — a new `## Notes` section, "Gaps review accepted, and one
    criterion that needs amending", carrying the AC12 wording issue, the untested 3.8 floor and
    the display-width limitation out of the reports and into the item
  - no merge commit; no bug item filed; `main` unchanged at `d1efa81`
  - the trial worktree `/tmp/trial`, created detached and removed
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected on D12. The tool is behaviourally right — fifteen criteria met, the trial
  merge clean and green — but a test contradicts ADR-0005 and the deviation was never declared, a
  second test would not notice the behaviour it guards being removed, and the architecture
  overview's one-place-per-rule claim is false of `has_trailing_pipe`. Four findings go back, none
  of which should change a single fixture's expected output. AC12's wording, which cannot be
  satisfied literally for one degenerate column, is recorded in the item as work for
  `answer-questions` rather than for the developer.

## 2026-08-28T19:29:41Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, dispatched by `next` after `review-close` rejected the item on D12
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, the `## Notes`, and the three gaps review accepted
  - `tracker/items/WI-0001/artifacts/review.md` — read first, per the procedure: the send-back's four findings are this execution's job, not the whole item
  - `tracker/items/WI-0001/artifacts/plan.md` — `## Approach`, for the six interfaces finding 4 says were weakened
  - `tracker/items/WI-0001/history.md` — nine rows; the last is `in-review → in-progress`, so this is a send-back and not a fresh start
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all `answered`, none since the last journal entry, so nothing new to re-read
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, the branch prefix and the commit subject
  - `docs/architecture/adr/ADR-0005-tests-and-lint-come-from-the-standard-library.md` — in full, because findings 1 and 2 both turn on what it says about fixtures
  - `mdtab/table.py`, `mdtab/scan.py`, `mdtab/textio.py`, `tests/test_fixtures.py`, `tests/test_units.py` — the code the findings name
  - `.claude/agile-skills/scripts/validate-workspace` lines 1239–1273 (`check_claim_citations`), to locate the crash this execution ran into
- **Decisions:**
  - **Finding 3, fixed by deleting `_escaped_at` rather than by calling it from `split_row`.** Review offered both. Deleting it leaves exactly one loop that knows what an escaped `|` is; making `split_row` call it would have left two functions to keep in step. `has_trailing_pipe` now reads the answer off `split_row`'s last field. Rationale for the specific test: a row ending in a separator has an empty-or-whitespace last field, and a row whose final `|` is escaped keeps that `|` inside the last field, so the field is not empty.
  - **Checked the refactor differentially rather than trusting it.** Compared the new `has_trailing_pipe` against the deleted two-rule version over every string up to six characters long drawn from `{ | \ a space tab }` — 19531 bodies, 0 disagreements. Review said the fix should not change a single fixture's expected output, and this is what makes that checkable rather than hoped for.
  - **Finding 4 also restored `lay_out`'s signature**, which review's list of five omits but `plan.md`'s `## Approach` fixes as `list[str] | None`. Left the private helpers (`_outer_style`, `_column_widths`, `_render_row`) and `row_cells` alone: `plan.md` does not fix those, so annotating them would be scope this item did not ask for.
  - **Finding 2 fixed with a fixture, not a unit test.** Review allowed either. ADR-0005's rule is that a document belongs in `tests/fixtures/`, and the mutation review named (`strip(" ")` → `strip()`) is a document-level effect, so the fixture is the closer evidence. `tab-in-cell` has a cell whose content is `\tb\t`: under the mutation the tabs are eaten, the column narrows from 5 to 3, and both the round-trip and the AC11 test fail.
  - **Did not decide how to store the AC9 undecodable-bytes document.** Fixing finding 1 as review specified produces `tests/fixtures/invalid-utf8.in.md`, a `.md` file holding a `0xFF` byte, and that makes `validate-workspace` — a hard gate of this skill — crash with a `UnicodeDecodeError` traceback. ADR-0005 requires the fixture and fixes the `.md` extension; the gate requires every `.md` file in the project to decode as UTF-8. Every way out amends an ADR, edits the pipeline's own machinery, or leaves a must-fix finding unfixed, so it is `Q-004` rather than a guess. My recommendation is recorded there; I did not act on it.
  - **Backed the fixture pair out of the tree before suspending**, in `a2059b7`, restoring the literal test with the exception named in the module docstring and in a comment pointing at `Q-004`. A crashed validator is a hard gate failure for *every* skill, so leaving it in place would have stopped `answer-questions` from running at all and stalled the pipeline rather than suspending one item. The commits that made the fix (`cc0eea6`) and that backed it out (`a2059b7`) both stay on the branch, so what was tried is legible.
  - **Did not rewrite `impl-report.md`.** It belongs to the execution that reaches `verifying`; this one stops at step 6. Rewriting it now would report a completion that has not happened. The next `implement` execution writes it, and must declare the AC9 storage decision as a deviation whichever way `Q-004` goes.
- **Questions raised:** `Q-004` (blocking, to architect)
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 54 tests ... OK` (branch head `a2059b7`)
  - `python3 -W error -m compileall -q mdtab tests` → exit 0, after clearing `__pycache__`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 with a `UnicodeDecodeError` traceback while the `invalid-utf8` pair was in the tree; exit 0, `0 errors, 0 warnings`, with the pair moved out; exit 1 with the two expected transitional errors (`board.stale`, `question.blocking.not-suspended`) once `Q-004` was filed and before this move
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 10 commit(s) on main..wi/WI-0001 name WI-0001`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked no documents changed since main`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 1, 2 `claim.unsourced` errors at `ADR-0003` lines 46 and 62, both about `Q-002` and both predating this execution. Not this gate: rule 2 is scoped to what an execution touched, and `--all` is documented as an audit rather than the gate. Reported, not acted on.
  - differential check of `has_trailing_pipe` against the deleted implementation → 19531 bodies compared, 0 disagreements
  - mutation `_TRIM = " "` → `_TRIM = None` → 2 failures, `test_ac11_cell_content_survives_apart_from_the_spaces_around_it` and the `tab-in-cell` round trip (before this execution: 0 failures)
  - mutation `split_row`: `if char == "|" and backslashes % 2 == 0` → `if char == "|"` → 6 failures including `test_a_trailing_pipe_that_is_escaped_is_not_a_trailing_pipe`. The same mutation applied to the code as `review-close` rejected it (`git archive HEAD` into `/tmp/pre`) leaves that test passing → exit 0, `OK`. That difference is finding 3's drift, demonstrated rather than asserted.
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 54 tests, on branch head `a2059b7`)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests`, exit 0)
  - `workspace-valid` → **fail at the moment of running, resolved by this move** (exit 1 with `board.stale` and `question.blocking.not-suspended`; the second is precisely the state this transition corrects, and the board is regenerated with it. The crash that `Q-004` is about is gone from the tree as of `a2059b7`.)
  - `every-criterion-has-a-test` → **pass, with one test in a form ADR-0005 forbids** (all fifteen criteria keep the tests `impl-report.md` maps them to; AC11's is now sensitive to the trimming rule, which it was not, and AC9's undecodable-bytes clause is still a Python literal pending `Q-004`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001`, exit 0, 10 commits)
  - `no-unplanned-scope` (advisory) → **pass** (every hunk traces to a numbered finding in `review.md`: `mdtab/table.py` to 3 and 4, `mdtab/scan.py` and `mdtab/textio.py` to 4, `tests/fixtures/tab-in-cell.*` to 2, `tests/test_fixtures.py` to 1 and 2. Nothing else was touched; the two pre-existing `ADR-0003` claim errors were left alone.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0)
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-004.md` (new, blocking, to architect)
  - `tests/fixtures/tab-in-cell.in.md`, `tests/fixtures/tab-in-cell.out.md` (new)
  - `mdtab/table.py`, `mdtab/scan.py`, `mdtab/textio.py`, `tests/test_fixtures.py` (updated)
  - branch `wi/WI-0001`, commits `78c7bf4`, `cc0eea6`, `a2059b7` — the range `256260f..a2059b7`
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** Findings 2, 3 and 4 are fixed, with the fix for 3 shown to be behaviour-preserving over 19531 inputs and the fix for 2 shown to catch the mutation that motivated it. Finding 1 cannot be fixed as written without taking `validate-workspace` down, because ADR-0005 wants the document in a `.md` fixture and the gate wants every `.md` file to decode as UTF-8; `Q-004` puts that to the architect and the item suspends.

## 2026-08-28T19:34:49Z — answer-questions v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`, dispatched by `next` step 4 — `Q-004` is the only open question on any item and it is addressed to the architect
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-004.md` — the only open question; `Q-001`–`Q-003` are `answered` and were re-read to confirm nothing in them bears on this
  - `tracker/items/WI-0001/item.md` — the fifteen criteria, to establish that none of them names a fixture format and so none needs amending
  - `tracker/items/WI-0001/history.md` — the suspending row `2026-08-28T19:29:41Z in-progress → awaiting-answer` carries `resume-to: in-progress`, read from the row rather than inferred from which skill asked
  - `tracker/items/WI-0001/artifacts/plan.md` — steps 9–12 and the `## Acceptance criteria mapping`, the artifacts the answer had to reach
  - `tracker/items/WI-0001/artifacts/review.md` — finding 1, which is what made this a must-fix rather than a preference
  - `docs/architecture/adr/ADR-0005-tests-and-lint-come-from-the-standard-library.md` (v1) — in full, including the sentence naming "one containing invalid UTF-8" as a case it intends to support
  - `docs/architecture/adr/ADR-0004-document-is-bytes-round-tripped-through-utf-8.md` (v1) — the `surrogateescape` decision the fixture is evidence for
  - `docs/architecture/adr/ADR-0001` (v1), `ADR-0002` (v1), `ADR-0003` (v2), `docs/architecture/overview.md` (v1) — checked for anything the answer would contradict; none of them mentions the test layout
  - `tracker/items/EP-001/questions/Q-001.md` — for the stakeholder's standing deferral on build decisions, quoted in the answer
  - `.claude/agile-skills/spec/question.md` §4 and `.claude/agile-skills/spec/doc-header.md` §4, to check the escalation conditions and the rule on editing an ADR
- **Decisions:**
  - **`Q-004` answered by deciding it, route 3 (architect's own decision), recorded as `ADR-0006`.** A fixture whose bytes are deliberately not valid UTF-8 carries `<name>.in.bin` / `<name>.out.bin`; every other fixture keeps `.md`; `tests/test_fixtures.py` discovers pairs by the `.in.` infix. That is the asker's option A.
  - **Not escalated, and the reasoning is on the record rather than implied.** None of `spec/question.md` §4's four conditions holds: intent is recorded — the stakeholder deferred build decisions in `EP-001/Q-001` (*"The rest of how it's built is your call, not mine"*); it is reversible — two filenames and one expression, and no module under `mdtab/` refers to `tests/` at all; it contradicts no ADR; and the record is not silent, since ADR-0005 names this very case as one it expects to support. Escalating would have cost a whole round trip to the human for a decision they had already delegated.
  - **`ADR-0006` amends `ADR-0005` rather than superseding it, and `ADR-0005` stays `current`.** `spec/doc-header.md` §4 says an ADR is never edited to change its decision. The extension is not part of what ADR-0005 decided in the sense that rule protects: its four options weigh `unittest` against `pytest`, files against literals, and lint against nothing — the extension was fixed in passing and never compared with an alternative. Everything ADR-0005 weighed stands, so marking it `superseded` would misdescribe it and would leave every `[src: ADR-0005]` citation in the tests and the plan pointing at a dead decision. ADR-0005 gets a v2 pointer instead, which is a content change and carries its change-log row.
  - **Rejected option C — patching `validate-workspace`.** The crash is a genuine toolkit defect and I say so below, but fixing it inside a work item puts a local edit to the pipeline's own machinery in a repository where no reviewer of mdtab can audit it, no criterion covers it, and the next toolkit install discards it. Routing around it in the project and reporting the defect is the division that keeps both records honest.
  - **No acceptance criterion was amended.** AC9 says nothing about how a fixture is named, so the decision reaches the plan and the ADRs and stops there. This is the one place this skill is most likely to go wrong and it did not: `git diff tracker/items/WI-0001/item.md` shows no changed `- [ ]`/`- [x]` line.
  - **AC12's outstanding amendment was deliberately not folded in.** `item.md`'s `## Notes` and `review.md` both record that AC12's "exactly `2 + max`" clause cannot hold for an all-empty `:---:` column and needs amending. It is a different decision on a different basis, it changes what the stakeholder was told they would get, and `spec/question.md` §2 requires one decision per question. It stays outstanding and is named as such in `Q-004`'s answer and in `item.md`, so the next skill to reach it cannot miss it.
  - **A toolkit defect worth reporting, and not filed as a bug item.** `validate-workspace`'s `check_claim_citations` opens every non-ignored `.md` file in the project with `encoding="utf-8"` and catches only `OSError`, so a `.md` file holding a byte it cannot decode aborts the validator with a `UnicodeDecodeError` traceback instead of producing a finding. Since `workspace-valid` is a hard gate of every skill, one such file stops the whole pipeline. A `bug` item belongs to behaviour this project delivered; this is the harness's own machinery, outside EP-001's goal and outside anything a criterion covers, so putting it on mdtab's board would misfile it. It is recorded here, in `ADR-0006`'s `## Consequences`, and in `HARNESS-STATUS.md`.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 on the first draft of `ADR-0006` (4 `claim.unsourced` errors at lines 42, 87, 98 and 102), then exit 0 after each absolute was sourced or rewritten. Recorded because the gate caught real unsourced absolutes in a document this execution wrote, which is what it is for.
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 with `board.stale` and `question.awaiting.none-open`, both of which are the transitional state this move corrects
  - `grep -rn "tests" mdtab/` → no match, which is the evidence behind `ADR-0006`'s reversibility claim
  - `git diff -- tracker/items/WI-0001/item.md | grep -E "^[-+]- \["` → no output, confirming no acceptance criterion changed
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in `Q-004`'s `## Consequences` was opened and checked: `ADR-0006` exists at v1 with the `.bin` rule in its `## Decision`; `ADR-0005` is at `version: 2` with the amendment paragraph after `## Decision` and a change-log row; `plan.md` step 10 requires the `invalid-utf8` pair and states the rule, step 11 specifies `.in.` discovery, and the AC9 mapping row names the pair; `item.md`'s `## Notes` carries "Settled by the architect, round 2". Nothing was named that is not there, and nothing was changed that is not named.
  - `answered-from-the-record` → **pass**. The answer follows from `ADR-0005`'s own stated intent ("Cases that cannot be written as literals at all, such as … one containing invalid UTF-8, become ordinary fixtures") plus the measured behaviour of `validate-workspace`; the part the record did not settle — which extension — is the new decision and is recorded as `ADR-0006` with five options and a reversibility statement, as `spec/doc-header.md` §4 requires.
  - `escalation-is-justified` → **skipped, nothing was escalated** — with the reason recorded rather than assumed: all four of `spec/question.md` §4's conditions were checked against this question and none holds, and the check is written into `Q-004`'s `## Answer` so a reader can disagree with it.
  - `workspace-valid` → **fail at the moment of running, resolved by this move** (exit 1, `board.stale` and `question.awaiting.none-open` — the second is precisely the state this transition corrects, and the board is regenerated with it)
  - `item-resumed-correctly` → **pass**. The suspending row `2026-08-28T19:29:41Z | in-progress | awaiting-answer | implement | in-progress` records `resume-to: in-progress`, and this move targets `in-progress`. Read from the row, not inferred.
  - `a-deferral-is-not-an-answer` → **not applicable, no deferral**. `Q-004` was addressed to the architect and answered by the architect; no reply from a human was involved, so neither of step 3a's two moves arises.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-004.md` — `open` → `answered`, `answered-by: answer-questions`, with `## Answer` and a five-file `## Consequences`
  - `docs/architecture/adr/ADR-0006-fixtures-that-are-not-valid-utf-8.md` — created, v1, `status: current`, `Supersedes: —`
  - `docs/architecture/adr/ADR-0005-tests-and-lint-come-from-the-standard-library.md` — v1 → v2, `updated-by: answer-questions`, `updated-for: WI-0001`; decision unchanged, amendment pointer added
  - `tracker/items/WI-0001/artifacts/plan.md` — steps 10 and 11 and the AC9 mapping row
  - `tracker/items/WI-0001/item.md` — `## Notes` only; no acceptance criterion touched
- **Status:** `awaiting-answer` → `in-progress`
- **Result:** `Q-004` is answered and propagated into four artifacts: fixtures that are not valid UTF-8 carry `.bin`, discovery keys on the `.in.` infix, and `implement` has the exact byte content and the exact edits written into the answer. WI-0001 returns to `in-progress` with review finding 1 now executable and findings 2, 3 and 4 already fixed on the branch. The `validate-workspace` crash that forced the question is a toolkit defect, reported and not patched here.

## 2026-08-28T19:38:28Z — implement v0.2.2 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, dispatched by `next` step 5 — the only runnable item; WI-0002 is blocked on it and EP-001's status has no owner
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-004.md` — `answered` since the previous entry, so its `## Consequences` named what to re-read
  - `tracker/items/WI-0001/artifacts/plan.md` — steps 10 and 11 and the AC9 mapping row, re-read from disk rather than from the answer: the artifacts are authoritative and the question file is not
  - `docs/architecture/adr/ADR-0006-fixtures-that-are-not-valid-utf-8.md` (v1) and `ADR-0005` (v2) — the decision and the amended clause
  - `tracker/items/WI-0001/item.md` — the fifteen criteria and the new `### Settled by the architect, round 2`
  - `tracker/items/WI-0001/artifacts/review.md` — findings 1–4 again, to check each is closed rather than only the one that was outstanding
  - `tracker/items/WI-0001/history.md` — fifteen rows; the last is `awaiting-answer → in-progress` by `answer-questions`, so this is a resumption
  - `tracker/items/WI-0001/artifacts/impl-report.md` — the previous round's report, updated rather than replaced
  - `.gitattributes`, `tests/test_fixtures.py`, `tests/test_units.py`, `mdtab/table.py`
- **Decisions:**
  - **Read the decision out of `plan.md`, not out of `Q-004`.** The answer file also spells out what to do, but the rule is that artifacts are authoritative; had the two disagreed, that disagreement would itself have been a question. They agree.
  - **`EXTENSIONS` replaces the old `NAMES` glob**, mapping each fixture's name to its own extension, so `read` resolves the pair by name and nothing else in the module knows an extension exists. That is what makes `.bin` invisible to the round trip, the AC6 idempotence test, AC11 and AC14 — the property `plan.md` step 11 asks for, rather than a special case for one fixture.
  - **Added `test_every_fixture_is_a_complete_pair_with_one_extension`, which is not in the plan.** Keying discovery on an infix creates a failure the suffix version did not have: a half-renamed pair is silently unread and every test keeps passing against a document nobody compared. Declared as deviation 7. I judged this inside the plan's latitude rather than a question, because it adds no behaviour and changes nothing a user would notice — it closes a hole the plan's own step 11 opened.
  - **The AC9 test asserts the fixture is undecodable rather than assuming it.** `original.decode("utf-8")` must raise, and `EXTENSIONS["invalid-utf8"]` must be `bin`. Without those the fixture could quietly become valid UTF-8 — by an editor, a rename, a bad merge — and the test would pass while testing nothing, which is the same class of defect as finding 2.
  - **Did not touch AC12, and did not touch the code for it.** `review.md`'s accepted gap 1 says so explicitly and routes the amendment to `answer-questions`. It remains outstanding and is named in `## What I did not do`.
  - **Did not patch `validate-workspace`.** The crash is real and is reported in three places, but it is the pipeline's own machinery: a local edit would be audited by nobody, covered by no criterion, and discarded by the next install. Deviation 6 records the reasoning where a reviewer will meet it.
  - **Left the three intermediate commits on the branch** rather than rewriting history to hide the `.md` attempt. `cc0eea6` (as `.md`), `a2059b7` (backed out), `459123c` (as `.bin`) are what makes the route legible to anyone reading `git log --grep WI-0001`, and the record is append-only in spirit as well as in the tracker.
- **Questions raised:** none. `Q-004` was raised by the previous execution and answered before this one.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 55 tests ... OK` (branch head `459123c`, and again after `impl-report.md` was written)
  - `python3 -W error -m compileall -q mdtab tests` → exit 0, after clearing `__pycache__`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 3 item(s), 8 document(s)`, 0 errors, 0 warnings — **with the `invalid-utf8.bin` pair in the tree**, which is the whole point of ADR-0006
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 13 commit(s) on main..wi/WI-0001 name WI-0001`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 2 document(s) changed since main`
  - `git check-attr text diff -- tests/fixtures/invalid-utf8.in.bin` → `text: unset`, `diff: unset` — `.gitattributes`'s existing `tests/fixtures/** -text -diff` already covers the new extension, so no change was needed there
  - mutation: rename `invalid-utf8.out.bin` → `.out.md` → 2 failures and 2 errors, `test_every_fixture_is_a_complete_pair_with_one_extension` among them
  - mutation: `_TRIM = " "` → `_TRIM = None` → 2 failures (`test_ac11_cell_content_survives_apart_from_the_spaces_around_it`, `tab-in-cell` round trip)
  - mutation: `split_row`'s `and backslashes % 2 == 0` removed → 6 failures including `test_a_trailing_pipe_that_is_escaped_is_not_a_trailing_pipe`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 55 tests, on the branch head after the last code change)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass**. `impl-report.md`'s `## Acceptance criteria evidence` names a test function or a command with its output for all fifteen. The two that were weak are now not: AC11 gains `tab-in-cell` and fails under the trimming mutation, and AC9's undecodable-bytes clause is a fixture that asserts its own undecodability.
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, 13 commits)
  - `no-unplanned-scope` (advisory) → **pass**. Every hunk in `git diff 256260f..HEAD` traces to a numbered finding in `review.md` or to `Q-004`'s propagation: `mdtab/table.py` to findings 3 and 4, `mdtab/scan.py` and `mdtab/textio.py` to finding 4, `tests/fixtures/tab-in-cell.*` to finding 2, `tests/fixtures/invalid-utf8.*.bin` and `tests/test_fixtures.py` to finding 1, and the `docs/` and `tracker/` files to `Q-004`. No hunk changes the tool's behaviour and no fixture's expected output changed, which is what `review.md` predicted a correct fix would look like.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0, 2 documents)
- **Artifacts:**
  - `tests/fixtures/invalid-utf8.in.bin`, `tests/fixtures/invalid-utf8.out.bin` (new)
  - `tests/test_fixtures.py` (updated — discovery, the pair-completeness test, the AC9 test, the module docstring)
  - `tracker/items/WI-0001/artifacts/impl-report.md` (updated — a `### What this round changed` table mapping each finding to its evidence, deviations 6 and 7, the gate results, and two new entries under `## What I did not do`)
  - branch `wi/WI-0001`, commit `459123c`; this round's range is `256260f..HEAD`
- **Status:** `in-progress` → `verifying`
- **Result:** All four of `review.md`'s findings are closed, each with a mutation or a differential check behind it rather than an assertion, and no fixture's expected output changed. `validate-workspace` now passes with the undecodable-bytes fixture in the tree, which is what ADR-0006 was for. Handing to verification with two things named for it: AC12's wording is still unamended by design, and the `validate-workspace` crash is a toolkit defect that was reported rather than patched.

## 2026-08-28T19:56:18Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0001
- **Trigger:** status `verifying` — `next` step 5 dispatched `verify` as the status owner; WI-0001 won the selection key over WI-0002 (both `high`, created three seconds earlier)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen acceptance criteria, read **before** the implementation report
  - `tracker/items/WI-0001/history.md` — twelve rows; this is the item's second pass through `verifying`
  - `tracker/items/WI-0001/artifacts/plan.md` — the twelve steps, the fixed interfaces, the AC-to-evidence mapping and `## Assumptions`
  - `tracker/items/WI-0001/artifacts/impl-report.md` — the claimed evidence, seven deviations, the `### What this round changed` table
  - `tracker/items/WI-0001/artifacts/review.md` — the four findings and the three accepted gaps that sent the item back
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - `docs/architecture/adr/ADR-0002-cell-width-is-display-width.md` — to write an independent display-width implementation from the rule rather than from the code
  - the code on branch `wi/WI-0001` at `e0fd6b0026ed67acc630adb9747f99f9fad3b560`: `mdtab/table.py`, `mdtab/scan.py`, `mdtab/textio.py`, `mdtab/width.py`, `mdtab/filter.py`, `mdtab/__main__.py`, `tests/test_fixtures.py`
- **Decisions:**
  - **AC12 is a `pass`, not `ambiguous`, and this is not a send-back.** AC12's arithmetic clause and its own delimiter clause cannot both hold for a column whose header and body cells are all empty and whose marker is `:-:`; the tool renders 3, the only width satisfying the delimiter clause and AC6 together. The behaviour is settled by the record — `plan.md` decided it under `## Assumptions` before implementation, the first verification confirmed it, and `review-close` accepted it as a gap and wrote that the *wording* is what should change. `verify`'s escalation trigger is "a criterion is ambiguous **and the record does not settle it**"; the record settles the behaviour, so the honest verdict is pass-with-the-exception-recorded, which is also what the first verification returned and what review accepted.
  - **But the amendment the record calls for was filed as `Q-005`, non-blocking.** Four artifacts say AC12's wording must be amended and that the amendment belongs to `answer-questions`; `answer-questions` runs only when a question is open, and no skill had filed one. Had this execution passed the item on in silence, the obligation would have died when `review-close` closed the item, and WI-0002 — whose whole subject is the delimiter row's markers — would have been refined against the arithmetic `review.md` warned about by name. `blocking: false` is the load-bearing part: WI-0001 is not blocked on it, so the item goes to `in-review`, and `next` step 4 dispatches `answer-questions` on an open architect question before step 5 dispatches `review-close`, so the amendment lands before the review that would close the item. `verify` may not amend a criterion itself — the criteria are the standard it judges against.
  - **The `empty-cells` fixture discrepancy is a note for review, not a send-back and not a bug item.** `impl-report.md` declares "One fixture beyond the plan's list: `tab-prefix`"; three are beyond the plan's mapping table, and `empty-cells` is declared nowhere. No acceptance criterion is affected and no behaviour is in question, so it fails the send-back test ("does a criterion of *this* item say the behaviour should be different?" — no) and it is not another item's delivered behaviour, so it is not a bug. It is recorded in `## Defects found` because an undeclared deviation is what got this item rejected the first time and `review-close`'s D12 reads reports for accuracy.
  - **All fifteen criteria were re-checked from scratch rather than trusted from the first verification.** `check-verify-freshness` reports the first verification does not apply to what would be merged — four commits changed `mdtab/scan.py`, `mdtab/table.py`, `mdtab/textio.py` and three fixtures after `175101a8`.
  - **Evidence came from documents written for this verification, never from the shipped fixtures**, and widths were measured with an independent implementation of ADR-0002's three rules that does not import `mdtab.width`. Re-running the developer's fixtures would check that the code matches the fixtures, not that it matches the criteria.
  - **The mutation harness asserts its target literal is present before mutating.** One `sed`-based mutation silently matched nothing during this execution and reported a clean suite, which would have been recorded as "the test is sensitive" when nothing had been changed. It was caught and re-run; the assertion is now the harness's first act.
- **Questions raised:** WI-0001/Q-005 (architect, non-blocking)
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 55 tests in 0.077s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 1, "verified at 175101a8 but code has changed since" — the reason this second verification was owed
  - `git rev-parse HEAD` → `e0fd6b0026ed67acc630adb9747f99f9fad3b560`
  - `python3 -m mdtab < <document>` on 24 documents written for this verification → exit 0 on every one, 0 bytes on stderr on every one
  - an independent ADR-0002 width script over four laid-out outputs → every row of each table one display width, every pipe at one display column
  - `cmp <in> <out>` on the eleven documents that must come back byte-for-byte → silent, exit 0, on all eleven
  - `python3 -m mdtab < f | python3 -m mdtab` compared by `md5sum` on all 24 documents → fixed point on all 24
  - `od -c` on the CRLF, no-final-newline and `0xFF` outputs → `\r\n` preserved, no `\n` added, `\377` preserved
  - 13 source mutations, each asserted present before applying, suite re-run, `git checkout -- mdtab/` after → every one failed at least one test; `git status --porcelain mdtab/ tests/` empty afterwards
  - `grep -n _escaped_at mdtab/` → no match (review finding 3)
  - `grep -rn '^import|^from| import| from' mdtab/` → `unicodedata`, `sys`, `re` and intra-package imports only (AC1's "nothing else installed")
  - `git diff --name-only main..HEAD` outside `tracker/` and `docs/` → 9 files plus 23 fixture pairs, every one mapping to a numbered plan step
  - `python3 .claude/agile-skills/scripts/board-gen .` → `wrote tracker/board.md`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 55 tests`, `OK`, run by this skill on `e0fd6b0`)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0, no output)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (each of the fifteen rows of `verify-report.md`'s `## Criteria` names a command this skill ran against a document written for this verification and quotes its actual output; no row cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (22 conditions triggered and their output inspected, listed in `verify-report.md`)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (13 mutations, each failing at least one named test)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — rewritten for this verification, `Verified-commit: e0fd6b0026ed67acc630adb9747f99f9fad3b560`
  - `tracker/items/WI-0001/questions/Q-005.md` — created, architect, non-blocking, AC12's wording amendment
  - `tracker/items/WI-0001/item.md` — all fifteen criteria remain ticked; every tick is backed by a command in this report, so none was removed and none was added
  - `tracker/board.md` — regenerated
  - the commit of these workspace files
- **Status:** `verifying` → `in-review`
- **Result:** All fifteen criteria pass against `e0fd6b0`, each demonstrated by a command run here on documents written here, with 22 negative and boundary cases triggered and 13 mutations confirming the suite is sensitive. All four of `review-close`'s findings are independently confirmed closed. AC12 passes with the degenerate all-empty `:-:` column exception the record already settled, and `Q-005` was filed non-blocking so `answer-questions` amends AC12's wording before `review-close` closes the item and before WI-0002 inherits the arithmetic.

## 2026-08-28T20:01:15Z — answer-questions v0.3.1 — architect

- **Item:** WI-0001
- **Trigger:** `next` step 4 — `WI-0001/Q-005` is `addressed-to: architect` and `status: open`, and it is the only open question in the workspace. The item is at `in-review`, not `awaiting-answer`, because `Q-005` is **non-blocking**: `verify` filed it without suspending the item, so this execution triages a question on a running item rather than unblocking a suspended one.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-005.md` — the question, its five options and its recommendation
  - `tracker/items/WI-0001/questions/Q-001.md`…`Q-004.md` — checked for other open questions on the item; all four are `answered`, so `Q-005` is the whole of this execution's work
  - `tracker/items/WI-0001/item.md` — AC12 as written, AC6, AC14, and the whole of `## Notes`
  - `tracker/items/WI-0001/history.md` — thirteen rows; no row suspended the item for `Q-005`, so there is no `resume-to` to honour
  - `tracker/items/WI-0001/artifacts/plan.md` — `## Approach` rules 1 and 2, and the `## Assumptions` bullet on the all-empty centred column
  - `tracker/items/WI-0001/artifacts/review.md` — `## Accepted gaps` 1, which says in terms that the wording is what should change
  - `tracker/items/WI-0001/artifacts/verify-report.md` — the second verification's AC12 row and its `### AC12's one exception` section
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — AC12's basis, recorded `[assumed]` and "not asked"
  - `docs/architecture/adr/ADR-0002-cell-width-is-display-width.md` (v1), `ADR-0003-lay-out-only-tables-the-tool-fully-understands.md`, `ADR-0004`, `ADR-0005` (v2), `ADR-0006` — checked that the amendment contradicts none of them
  - `docs/architecture/overview.md` v1 — `## Rules that live in exactly one place`
  - `docs/product/vision.md` — the stakeholder's "never the punctuation" statement in its recorded form
- **Decisions:**
  - **`Q-005` answered from the record — route 1, an existing document — not decided fresh and not escalated.** Every element of the amendment is already written down: `plan.md`'s `## Approach` rule 2 states the delimiter-cell floor and says AC6 forces it; `plan.md`'s `## Approach` rule 1 states the delimiter-cell exclusion and says AC6 forces that too; `review.md`'s `## Accepted gaps` 1 says the wording is what should change, not the code; `refinement-qa.md` records AC12 as `[assumed]`, "not asked", which is the authority to amend it; and the stakeholder's *"I only want the spacing changed, never the punctuation"* (`WI-0001/Q-002`) is what rules out the option that would have dropped a `:`. What was missing was never a decision — it was the amendment itself.
  - **The answer is the question's option A, plus a second qualification the question did not name.** `Q-005` asked only about the floor. AC12's `max(display width of its cells)` also does not say *which* cells, and AC6 forces the answer — a column measured over a delimiter cell that was itself widened to the column grows on every run, which the second verification demonstrated by mutation (`if index != 1` → `if index != -1` fails 29 tests, `test_ac6_…` among them). Amending only the floor would have left AC12 still not decidable from its own text, which is precisely what the question existed to fix, so both are amended in one edit and the addition is declared in `## Answer` rather than made quietly.
  - **Not escalated, and the four conditions were checked one at a time.** Not intent no document records — five documents record it. Not irreversible — it is one paragraph of a criterion whose behaviour has been shipped, verified twice and reviewed once. Not a contradiction with a recorded decision — ADR-0002 fixes how a *character* is measured and is silent about a column's floor; ADR-0003 governs which runs are laid out at all. Not a silent record. Effort was not a factor in either direction.
  - **This is not "amending a criterion to match what was built", and the distinction was tested rather than asserted.** Both qualifications are obligations of **AC6**, a criterion of this item, not of `mdtab/table.py`: the code satisfies them because AC6 requires them, and a hypothetical implementation that ignored them would fail AC6 rather than reveal AC12 to be wrong. What the amendment changes is that AC12 no longer contradicts AC6. The alternative — amending the delimiter clause instead, so that a narrow column drops a `:` — would have been reshaping the target, and it was rejected on the stakeholder's own words and because WI-0002 is about to start honouring exactly those markers.
  - **The durable half of the answer went into `docs/architecture/overview.md`, not only into `item.md`.** `item.md` stops being read when WI-0001 closes, and the whole reason `Q-005` was filed was that WI-0002 must inherit this arithmetic. The overview's `## Rules that live in exactly one place` is where a rule that must not be duplicated belongs, and it is what WI-0002's `plan` will read.
  - **No item was filed and no scope widened.** The amendment implies no work: the code already does what the amended text says, no test or fixture changes, and WI-0002's scope is untouched. `spec/question.md` step 3b does not apply.
  - **No transition.** WI-0001 was never suspended for `Q-005` — the question is non-blocking — so there is no `resume-to` to return it to and no status change to make. It stays at `in-review`, where `verify` left it, and the next `next` run dispatches `review-close` on it.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/board-gen .` → `wrote tracker/board.md`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 3 document(s) changed since main`, `0 errors, 0 warnings` — run on this skill's own initiative, as it was for ADR-0006; `claims-are-sourced` is still not in this skill's gate list even though it is one of only two skills that author documents under `docs/`
  - `printf '| a |  |\n|---|:-:|\n| b |  |\n' | python3 -m mdtab` → column 3 wide, `|:-:|` — the amended text's `:---:` case
  - `printf '| a |  |\n|---|---|\n| b |  |\n' | python3 -m mdtab` → column 2 wide, `|--|` — the amended text's `---` case
  - `printf '| a |  |\n|---|:--|\n| b |  |\n' | python3 -m mdtab` → column 2 wide, `|:-|` — the amended text's `:---` case
  - `printf 'a |  | c\n--- | :-: | ---\nb |  | d\n' | python3 -m mdtab` → `a |   | c` / `--|:-:|--` / `b |   | d` — the bare-row case, which is what the "less whichever of the two surrounding spaces the row's outer-pipe style drops" clause is for
  - `grep -c "never over the delimiter" tracker/items/WI-0001/item.md docs/architecture/overview.md` → 1 and 1; `grep -c "Q-005" tracker/items/WI-0001/artifacts/plan.md` → 2 — the propagation check for `answer-is-propagated`
- **Gates:**
  - `answer-is-propagated` → **pass** — each of the three files named in `Q-005`'s `## Consequences` was opened after the edit and the change is in it: `item.md` carries the amended AC12 and the new `### AC12 amended, round 3` section (`grep` above); `plan.md`'s `## Approach` rule 2 and `## Assumptions` bullet both cite `WI-0001/Q-005`; `docs/architecture/overview.md` carries "How wide a column is" in `## Rules that live in exactly one place`. No file is named that does not contain its change, and no change was made that is not named.
  - `answered-from-the-record` → **pass** — the answer cites `plan.md` `## Approach` rules 1 and 2, `plan.md` `## Assumptions`, `review.md` `## Accepted gaps` 1, `verify-report.md`, `refinement-qa.md`'s `[assumed]` note, `WI-0001/Q-002` and `EP-001/Q-001`. The record was not silent, so no new ADR was written; ADR-0002 and ADR-0003 were read and neither is contradicted.
  - `escalation-is-justified` → **skipped, nothing was escalated** — the four conditions in `spec/question.md` §4 were each checked against `Q-005` and none applies; the check is recorded under `## Decisions` rather than omitted, because "no escalation" is a judgement that should be auditable.
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 0 errors, 0 warnings, run after the board was regenerated
  - `item-resumed-correctly` → **skipped, no suspension to resume from** — `Q-005` is `blocking: false`, so no history row suspended WI-0001 for it, there is no `resume-to` to compare against, and this execution makes no transition. The item stays at `in-review`. Recording it as `pass` would claim a comparison that had nothing to compare.
  - `a-deferral-is-not-an-answer` → **skipped, no deferral** — `Q-005` was addressed to the architect and answered by the architect; no reply deferred anything and no question on this item is at `deferred`.
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-005.md` — answered: `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-28T19:59:23Z`, with `## Answer` and a three-file `## Consequences`
  - `tracker/items/WI-0001/item.md` — **AC12 amended** (see below); `## Notes` heading "Gaps review accepted, and one criterion that needs amending" → "Gaps review accepted", its AC12 bullet rewritten to point at the amendment instead of describing an open gap, the round-2 section's closing sentence updated, and `### AC12 amended, round 3` added
  - `tracker/items/WI-0001/artifacts/plan.md` — `## Approach` rule 2 no longer claims AC12 and AC6 cannot both hold literally; `## Assumptions` reclassifies the all-empty centred column from an open assumption to a criterion
  - `docs/architecture/overview.md` — v1 → v2, "How wide a column is" added to `## Rules that live in exactly one place`, change-log row added
  - `tracker/board.md` — regenerated
  - the commit of these workspace files
- **The acceptance criterion this execution amended, stated explicitly.** AC12. Before: "every column is **exactly** `2 + max(display width of its cells)` columns wide". After: the same formula, qualified by two rules AC6 already forced — the maximum is over the header and body rows only, never the delimiter row's own cell; and a column is never narrower than its delimiter cell's field can be written (one `-`, plus one character for each `:` the input had, plus whichever of the two surrounding spaces the row's outer-pipe style drops). The only column affected is one whose header and body cells are all empty: `:---:` → 3, `---` and `:---` → 2. The reason is recorded above and in `Q-005`; the basis is `refinement-qa.md`'s `[assumed]`/"not asked" and `EP-001/Q-001`'s standing deferral; no behaviour, test or fixture changed, and the criterion still describes what the stakeholder asked for — a tool that changes spacing and never punctuation.
- **Status:** `in-review` → `in-review` (unchanged — the question was non-blocking, so nothing was suspended and nothing is resumed)
- **Result:** `Q-005` answered from the record and propagated into three files. AC12 now states the two rules AC6 forces, so it is decidable from its own text and no longer contradicts itself for an all-empty `:---:` column; `plan.md` no longer carries it as an open assumption; and `docs/architecture/overview.md` v2 carries the column-width rule where WI-0002's `plan` will read it. No code changed, no test changed, no fixture changed, and the second verification stands. WI-0001 stays at `in-review` — it was never suspended, because the question was non-blocking.

## 2026-08-28T20:06:15Z — review-close v0.5.0 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review` — `next` step 5 dispatched `review-close` as the status owner; WI-0001 beat WI-0002 on `created` (both `high`). This is the item's **second** review; the first rejected it on D12 at 19:21:09Z.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the fifteen criteria and their tick state, `## Out of scope`, and the whole of `## Notes` including this turn's AC12 amendment
  - `tracker/items/WI-0001/history.md` — thirteen rows, chaining without a gap and matching the item's status
  - `tracker/items/WI-0001/journal.md` — all fourteen entries in full
  - `tracker/items/WI-0001/questions/Q-001.md`…`Q-005.md` — all five, and every file each `## Consequences` names
  - `tracker/items/WI-0001/artifacts/plan.md`, `impl-report.md`, `verify-report.md` in full, including the seven deviations, `## What I did not do` and the four entries under `## Not verified, and why`
  - `tracker/items/WI-0001/artifacts/review.md` — the first review's four findings and three accepted gaps, to check each is closed or carried
  - `docs/architecture/overview.md` v2, `docs/product/vision.md` v3, ADR-0001 through ADR-0006
  - **the diff `main..wi/WI-0001`** — 16 commits, 68 files, +2802/−45; the six modules under `mdtab/` read line by line, both test modules, 23 fixture pairs and `.gitattributes`
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.commit-subject`
- **Decisions:**
  - **Accepted, and merged.** All twelve Definition of Done criteria pass, each recorded with its own evidence in `review.md`'s table rather than as one verdict. Fifteen of fifteen criteria are ticked and each tick is backed by a command the verifier ran on a document written for the purpose, with widths measured by an implementation of ADR-0002 that does not import `mdtab.width` — so no tick is circular.
  - **The whole change was reviewed again, not only the delta since the rejection.** A reviewer who reads only what moved is trusting the previous review's reading of everything else, and the previous review's reading is precisely what produced two false claims. Thirteen claims were re-audited from the code, including the two that were FALSE the first time.
  - **Both first-review D12 failures are confirmed closed from the code, not from the report saying so.** ADR-0005's "a test may not build a document from a Python literal" — checked by reading all twenty `run(` call sites in `tests/test_fixtures.py`; every argument is `read(name, side)` or a prior output. The overview's "one function, used by the cell-count rule, the outer-pipe test and the layout alike" — checked by `grep -n "split_row(" mdtab/table.py` → lines 49, 68, 74, and `grep -rn _escaped_at mdtab/` → no match.
  - **One finding, accepted rather than sent back: `impl-report.md` miscounts the fixtures beyond the plan.** It declares one (`tab-prefix`); three are not in `plan.md`'s mapping table, and `empty-cells` is declared nowhere. `verify` raised it and routed it here. It is not the same species as the first review's finding 1, which was an undeclared deviation that contradicted an ADR and came with a false module docstring: nothing in `docs/` is false here, no ADR is contradicted, no behaviour is in question, and `empty-cells` is what plan step 10 requires anyway — a test may not build a document from a literal, so AC12's empty-cell assertion has nowhere but a fixture to put its document. A third implement-and-verify cycle would produce one corrected sentence and no other change. The correction is written into `item.md`'s `## Notes`, where a reader of a closed item looks; the developer's own sentence is left as they wrote it, because a reviewer rewriting the developer's report leaves the record less honest, not more.
  - **Six gaps accepted, and every one written into `item.md`'s `## Notes` rather than left in a report.** The three the first review carried (the untested CPython 3.8 floor, terminal rendering, and — now closed — the AC12 wording), plus three the second verification declared: the shipped fixtures' expected outputs were not independently re-derived, there is no README, and concurrency and large inputs are unexercised. The `validate-workspace` toolkit defect is recorded there too. Once an item is `done` nobody reads its verification report again.
  - **No bug item filed.** No defect belonging to another item was found; WI-0001 is the first item to deliver any behaviour at all. The one toolkit defect belongs to `.claude/agile-skills/scripts/`, which is not this project's code and is covered by no criterion.
  - **Trial merge first, then close, then merge — in that order, and with `--detach`.** `git worktree add --detach .trial main` gives the trial no branch to advance; `main` was `d1efa811` before and `d1efa811` after, confirmed rather than assumed. Closing precedes merging because `check-commit-refs` inspects `main..wi/WI-0001`, which merging would empty.
  - **Two design notes recorded in `review.md` that are not findings**, because they are where this design could rot later: `format_document` splices line ranges by index, which is safe only because `lay_out` returns exactly as many lines as it was given; and `find_runs` imports `has_unescaped_pipe` inside the function body to break a cycle, with the rule still living in `mdtab.table`.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0, "verified at e0fd6b00; wi/WI-0001 has moved to 03e63660 but only the record changed (8 file(s) under tracker/ or docs/), so the verification still covers the code"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 16 commit(s) on main..wi/WI-0001 name WI-0001"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 3 document(s) changed since main`, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0001` → exit 0, "WI-0001 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 3 item(s), 8 document(s)`, 0 errors, 0 warnings
  - `git rev-parse main` before the trial → `d1efa811bbfe6b802e32b508bd009e7880859aa0`
  - `git worktree add --detach .trial main` → detached at `d1efa81`
  - `git -C .trial merge --no-ff wi/WI-0001` → clean, merge head `92aea90b0129ef053c2412c0e52c9a63f0ed5dba`
  - `python3 -m unittest discover -s tests -t .` **inside the trial worktree** → exit 0, `Ran 55 tests in 0.071s`, `OK`
  - `python3 -W error -m compileall -q .trial/mdtab .trial/tests` → exit 0
  - `git worktree remove --force .trial`; `git rev-parse main` after → `d1efa811…`, unchanged
  - `grep -c "^- \[x\] AC" item.md` → 15; `grep -c "^- \[ \] AC" item.md` → 0
  - `grep -n "split_row(" mdtab/table.py` → 49, 68, 74; `grep -rn _escaped_at mdtab/` → no match
  - `grep -n "len(" mdtab/*.py | grep -v width.py` → sixteen matches, each read: list lengths, prefix lengths, index bounds, one character count in `_fence_closes`; none is a display width
  - `grep -rn splitlines mdtab/ tests/` → one match, the docstring stating the rule
  - `grep -rn "open(\|os\.\|socket\|urllib\|sys\.argv" mdtab/` → no match
  - `grep -rn "normalize\|normalise" mdtab/` → no match
  - `python3 -c "from mdtab.width import display_width; …"` on both spellings of `é`, on `U+FE0F`, `表` and `ＡＢ` → 1, 1, 0, 2, 4
  - `printf 'a | bb\n--- | ---\n1 | 2\n\n| x | yy |\n|---|---|\n| 3 | 4 |\n' | python3 -m mdtab` with a per-line `|`-count comparison → no line differs; the bare table stays bare
  - `printf '+---+\n| a |\n+===+\n| 1 |\n+---+\n' | python3 -m mdtab` → byte-for-byte
  - the four cases the amended AC12 names, run through the tool → `:---:` all-empty → 3, `---` → 2, `:---` → 2, bare-row interior `:-:` → field 3
  - `python3 .claude/agile-skills/scripts/board-gen .` → board regenerated
- **Gates:**
  - `definition-of-done` → **pass** — D1 to D12 each recorded with its own result and evidence in `review.md`'s `## Definition of Done` table; all twelve pass. D5's fourteenth journal entry against thirteen history rows is correct, not a gap: `answer-questions` at 20:01:15Z made no transition because `Q-005` was non-blocking, which `spec/journal-and-history.md` §2.2 provides for with `X → X (unchanged)`
  - `verification-postdates-the-code` → **pass** — `check-verify-freshness` exit 0; the eight files changed since the verified commit are all under `tracker/` or `docs/`
  - `commits-reference-the-item` → **pass** — `check-commit-refs` exit 0, all 16 commits
  - `tests-pass-on-the-merge-result` → **pass** — `Ran 55 tests … OK` inside the detached trial worktree, on the merge result rather than on the branch; `commands.lint` exit 0 there too
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone: *what was built and why* — `plan.md` and `impl-report.md`, with `docs/product/vision.md` v3 for the goal; *which decisions were made and by which skill* — ADR-0001–0003 predate the item, ADR-0004 and ADR-0005 by `plan`, ADR-0006 by `answer-questions`, each cited from the plan or a question; *what questions arose and how they were resolved* — five, three answered by the human with quoted words and two by the architect from the record, each with a `## Consequences` naming files that contain the change; *what verification found* — two verification reports, the first with two findings and the second with fifteen commands, 22 boundary cases and 13 mutations. `git log --grep WI-0001` returns all 16 commits
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0 over the three documents this branch changed
  - `epic-sign-off` → **pass (not applicable)** — `check-epic-signoff WI-0001` exit 0: WI-0001 is a work item, not an epic. EP-001 is not at rest either: WI-0002 is still at `draft`, so the engagement has somewhere to go and this execution does not end it
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` — rewritten for this review: what was examined, thirteen audited claims, the twelve Definition of Done rows, one accepted finding, six accepted gaps, the verdict
  - `tracker/items/WI-0001/item.md` — six accepted gaps written into `## Notes`, including the corrected fixture count; `status: done`, `outcome: delivered`
  - the merge of `wi/WI-0001` into `main`
  - the commit of these workspace files
- **Status:** `in-review` → `done`
- **Result:** WI-0001 accepted and closed as `delivered`. All twelve Definition of Done criteria pass with per-criterion evidence; the two claims that failed D12 at the first review are true against the code, checked from the code; the trial merge was clean with both gate commands green on the merge result, and `main` was confirmed unmoved by the trial. mdtab now exists: a stdin-to-stdout filter that lays out the pipe tables it fully understands, copies through byte-for-byte everything it does not, and writes nothing to stderr. WI-0002 inherits an AC12 that is correct about the arithmetic it will build on and an architecture overview that says where a column's width is decided.
