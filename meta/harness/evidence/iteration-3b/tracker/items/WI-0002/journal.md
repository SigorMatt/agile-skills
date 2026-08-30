# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-29T21:15:02Z — intake v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly by the operator on the stakeholder's stated idea; no status made this runnable, because the item did not exist yet
- **Inputs read:**
  - `IDEA.md` (the stakeholder's one-sentence statement)
  - `tracker/project.yaml`
  - `tracker/items/EP-001/item.md` and `tracker/items/WI-0001/item.md` (both written earlier in this same execution)
- **Decisions:**
  - See `EP-001`'s entry for this execution for how the work was split and why this item exists.
  - Declared `depends-on: WI-0001` rather than leaving the two items unordered. Rationale: alignment is a decision about *which side* padding goes on, so it presupposes that padding exists; building this first would mean building most of `WI-0001` inside it.
  - Wrote AC4 as "a column with no marker is laid out exactly as `WI-0001` lays it out, and `WI-0001`'s tests still pass unchanged" rather than describing the unmarked layout again here. Rationale: restating it would create a second place for the same requirement to live, and the two would drift the first time either item was refined.
  - Wrote AC5 (the input's markers are still present and still mean the same thing in the output) because the stakeholder said "honours alignment markers", and a filter that read the markers and then dropped them from the delimiter row would satisfy a naive reading of that while destroying the document's meaning.
  - Did not state the exact marker syntax accepted or how a centred column splits an odd padding count. Rationale: those are Definition-of-Ready work for `refine`, and `## Notes` records them as unresolved rather than inventing them.
- **Questions raised:** none on this item; the three open questions are on `EP-001` and this item's `## Notes` points at them
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --title "..." --epic EP-001 --priority medium --status draft --actor intake` → exit 0, created the directory with its `journal.md` and `history.md` headers
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported at the end of this intake execution on `EP-001`)
  - `epic-has-success-measures` → **pass** (assessed on `EP-001`; see that item's entry)
  - `an-open-question-was-asked` → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation`, exit 0; the elicitation question is `EP-001/Q-001`)
  - `items-are-separable` → **pass** (advisory: buildable second, after `WI-0001`, which it declares in `depends-on`; it delivers a visible change on its own — cell text moving to the side its marker names)
  - `no-solution-in-the-problem` → **pass** (advisory: the story and criteria name alignment markers, delimiter rows and padding, all of which are markdown's own vocabulary and the stakeholder's; no language, library or data structure appears)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/history.md` (new, creation row)
  - `tracker/items/WI-0002/journal.md` (new, this entry)
- **Status:** `draft` → `draft` (unchanged — the item was created at draft by new-item, whose creation row is the only row in history.md)
- **Result:** Alignment-marker handling exists as a draft item with six criteria, ordered behind `WI-0001` and dependent on `EP-001/Q-003` for what a delimiter row is allowed to look like.

## 2026-08-29T21:16:40Z — intake v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** correction to this item's preceding entry, written by the same `intake` execution that wrote it; no status made this runnable
- **Inputs read:**
  - `tracker/items/WI-0002/journal.md` (the preceding entry)
  - `.claude/agile-skills/scripts/validate-workspace` (`status_claims()`, lines 178–200)
- **Decisions:**
  - **Correction.** The preceding entry's `**Status:**` bullet read: `` `draft` → `draft` (unchanged; created at `draft` by `scripts/new-item`) ``. It now reads `` `draft` → `draft` (unchanged — the item was created at draft by new-item, whose creation row is the only row in history.md) ``. **No recorded fact changed:** the claim was, and is, that this execution moved the item nowhere. What was wrong was the punctuation. `status_claims()` splits the bullet on `;` before it strips parentheticals, so the text after the semicolon was read as a second, independent claim — `draft` → `scripts/new-item` — and `validate-workspace` reported `journal.status.unmatched` on a transition nobody had ever asserted.
  - **Repaired in place rather than only by appending, which is a departure from the append-only rule in `spec/journal-and-history.md`.** Recorded here because the rule says a wrong entry is corrected by a later entry, and this is that entry. Appending alone could not work: the malformed bullet keeps failing the validator wherever it sits, `journal-entry --restamp-last` repairs only a heading's timestamp, and a workspace that cannot validate stops every downstream skill. The narrower fix was to make one prose parenthetical say the same thing without a semicolon in it.
  - Did not change `item.md`, `history.md`, or any other bullet of the preceding entry.
- **Questions raised:** none
- **Commands:**
  - `scripts/validate-workspace .` → exit 1 before the repair, reporting `journal.status.unmatched` at `tracker/items/WI-0002/journal.md:5`
  - `scripts/validate-workspace .` → exit 0 after the repair, "0 errors, 1 warning" (the remaining warning is `commands.test` being null, which is `plan`'s to resolve)
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, after the repair)
  - `epic-has-success-measures` → **skipped** — assessed on `EP-001` by the execution being corrected; this entry changes nothing about the epic's success measures
  - `an-open-question-was-asked` → **skipped** — assessed on `EP-001` by the execution being corrected; `EP-001/Q-001` is unaffected by a punctuation fix
  - `items-are-separable` → **skipped** (advisory; the split is unchanged)
  - `no-solution-in-the-problem` → **skipped** (advisory; no title or story was touched)
- **Artifacts:**
  - `tracker/items/WI-0002/journal.md` (the preceding entry's `**Status:**` bullet reworded, and this entry appended)
- **Status:** `draft` → `draft` (unchanged)
- **Result:** The preceding entry's status bullet now parses as the single no-op claim it always meant, and the workspace validates. Worth reporting upstream: a semicolon inside the sanctioned "(unchanged)" parenthetical is enough to make a correct entry fail `journal.status.unmatched`, because the clause split happens before the parenthetical is stripped.

## 2026-08-29T21:25:10Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** not dispatched on this item — appended by the `answer-questions` execution on `EP-001`, which changed this item's file. Recorded here so a reader of WI-0002 can see where its `## Notes` came from without reading the epic.
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-003.md`
  - `tracker/items/WI-0002/item.md`
- **Decisions:**
  - Q-003 narrows this item's subject: only pipe tables are recognised, so the only markers in play are the colons of a pipe delimiter row, and the marker syntax question `intake` left for `refine` is largely answered.
  - Two constraints from Q-001 land on alignment specifically. A line the filter composes ends in no whitespace, which fixes where the padding of a right-aligned or centred **final** column has to go — inside the cell, before the closing pipe. And a column's width is its widest cell with no maximum, so alignment decides only where padding sits, never how much of it there is.
  - ADR-0002 decision 3 removes a case this item would otherwise have to handle: a delimiter row whose cell count differs from the header's makes the whole block malformed and therefore copied, so alignment never meets a ragged delimiter row.
  - **No acceptance criterion was amended**, for the same reason as on WI-0001: the item is at `draft` and its criteria belong to `refine`.
- **Questions raised:** none
- **Commands:** none
- **Gates:**
  - all of `answer-questions`' gates → **assessed on `EP-001`**, which is the item this execution acted on. Its journal entry of 2026-08-29T21:24:43Z carries the evidence for each, including the file-by-file propagation check that names this item.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — `## Notes` rewritten, frontmatter `updated` bumped
- **Status:** `draft` → `draft` (unchanged)
- **Result:** WI-0002's remaining unknowns are down to three, all about the shape of the output delimiter row and how a centred column splits an odd padding count.

## 2026-08-29T22:22:51Z — refine v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, whose owner in `pipeline.yaml` is `refine`; dispatched by `next`, which reported it as the only runnable candidate (EP-001 and WI-0001 both sit in statuses with `owner: null`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md` — history has one row, the creation row, so this is a **fresh draft and not a send-back**; the journal carries `intake`'s reasoning and the `answer-questions` entry that rewrote `## Notes`
  - `tracker/items/WI-0002/artifacts/` — empty on entry; no earlier refinement to resume
  - `tracker/items/WI-0001/item.md` — the eleven delivered criteria and the `## Out of scope` entry that scopes AC4 to a markerless delimiter cell
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`; `tracker/items/WI-0001/questions/Q-001.md`, `Q-003.md`, `Q-004.md` — every human answer on record, read in full for the cross-answer check and for what they already settle
  - `docs/product/vision.md` v3, including `## What is not yet decided`
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` (decisions 3, 4, 6, 7, 8, 9, 10, 11) and `ADR-0004-delimiter-row-preserves-alignment-markers.md` (decisions 1, 2, 3)
  - `mdtab.py` — `is_delimiter_cell()`, `column_widths()`, `compose_row()`, `compose_delimiter()`, read to confirm that two of this item's three recorded unknowns are not merely decided on paper but shipped
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **Suspended the item rather than refining it, because the stakeholder is not in this session.** `refine` is a conversation and its precondition 2 names this path: file a question addressed to `human`, set `awaiting-answer` with `resume-to: draft`, stop. The alternative — writing criteria from a guess — is the failure the Definition of Ready exists to prevent.
  - **Filed exactly one question, and deliberately only one.** The Definition of Ready walk found four things R4 and R10 needed. Three of them were already answered in the record and are recorded as such rather than re-asked; re-asking a stakeholder what they have already said is the fastest way to lose them (F-023). The fourth — how a centred column splits an odd number of leftover padding spaces — is answered nowhere, is visible in every centred column of every document they own, and belongs to the same category (what the output *looks* like) in which this stakeholder has given four firm, opinionated answers already. It is theirs.
  - **Did not treat their language deferral as covering this.** *"I have opinions about languages but they are not worth much here, so take that decision yourselves"* [src: EP-001/Q-002] is a standing deferral over implementation, not over appearance. On appearance — cell padding, the delimiter row's shape, what "line up" means — they answered directly and specifically each time. Reading the deferral wider than they wrote it would have converted their most-exercised opinion into our decision.
  - **Corrected this item's `## Notes`: two of its three recorded unknowns were already settled.** `intake` left three things "still for `refine` to settle", and the `answer-questions` execution on EP-001 narrowed but did not remove them. Checked against the artifacts: where a marker's colons sit inside the delimiter cell is ADR-0004 decision 1, and whether `:-:` or a bare `-` is an acceptable delimiter cell is ADR-0003 decision 3. Both are not only decided but implemented and verified under WI-0001 (`compose_delimiter()` and `is_delimiter_cell()`). Left as they were, those two lines would have produced two more questions to the stakeholder about things the team had already decided and shipped.
  - **Recorded, in `Q-001`'s `## Cross-answer check`, why AC5 does not contradict WI-0001/Q-004.** That answer says the delimiter row is *"Dashes all the way across, pipe to pipe"*, and this item will emit `|:---:|`, which is not literally that. It is not a conflict and was not escalated as one: the question that produced the answer stated in its own `## Context` that it asked about *"only the appearance of a delimiter row that carries no marker at all"* and that the colons were *"separate from WI-0002"*, so the scope was on the page when they answered; their stated reason concerns padding, not colons; and deleting markers would contradict the epic's own sentence, *"honours alignment markers"*. Written down rather than assumed, because this is the exact shape of F-062 and the next reader should find the reconciliation, not the apparent conflict.
  - **Did not rewrite the acceptance criteria.** AC1 to AC3 must be restated in display width [src: ADR-0003] decision 7, AC4 must name by ID the criteria it covers and how their text is read against the new behaviour rather than deferring to another item's suite, and AC5 must name what "mean the same thing" is checked against. None of those depends on `Q-001` — but AC3 does, and rewriting five criteria now and the sixth next turn would leave a half-refined item that reads as finished. The gaps and their sources are recorded in `artifacts/refinement-qa.md` and in `## Notes` so the resuming execution rewrites all six in one pass without re-deriving anything.
  - **Routed nothing to `plan` as an open design question**, because nothing was left over: which function places the padding and how it is expressed are ordinary implementation and need no note to be found.
- **Questions raised:** `Q-001` (blocking, addressed to `human`) — how a centred column splits an odd number of leftover padding spaces. One question; `artifacts/refinement-qa.md` records the whole agenda including the eight things settled from the record and not asked. Nothing left `[unresolved]`.
- **Commands:**
  - `scripts/validate-workspace .` → exit 0 on entry (3 items, 6 documents, 0 errors, 0 warnings)
  - `scripts/lint-answers --item WI-0002` → exit 0 on entry ("checked 0 consumed human answer(s)")
  - `scripts/validate-workspace .` → exit 1 after the question file was written, reporting `question.blocking.not-suspended` on this item and `board.stale`; both are the pending suspension itself and both are resolved by this transition
  - `scripts/transition WI-0002 --to awaiting-answer --actor refine --resume-to draft --dry-run` → exit 0, all command-backed gates PASS against the state the move produces
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace --resolving 'WI-0002:draft->awaiting-answer'`, exit 0, run by `transition` step 2)
  - `definition-of-ready` → **fail, and correctly so — this item is not being passed to `ready`.** Walked criterion by criterion against `spec/dor-dod.md` §1; the table with the evidence for each is in `artifacts/refinement-qa.md`. R1 pass (`validate-workspace` exit 0). R2 pass (the story names the role, the capability and the "so that"). R3 pass (AC1 to AC6, labelled, checkboxes). **R4 fail** — AC1 to AC3 are stated in character offsets where ADR-0003 decision 7 and WI-0001's amended AC1/AC2 use display width; AC3 does not say which side an odd leftover space goes to, which is `Q-001`; AC4 defers to another item's test suite instead of naming what is read; AC5 does not name what "mean the same thing" is checked against. R5 pass (two exclusions already present, to be extended at the rewrite). **R6 fail by design** — `Q-001` is open and blocking, which is what this transition records. R7 pass (`depends-on: WI-0001` is `done`, outcome `delivered`, merged at `045c779`). **R8 fail** — `artifacts/refinement-qa.md` declares `status: agenda`, honestly, because the conversation has not happened. R9 pass (one change, to where padding sits within a column, in one composing function). **R10 fail** — the three markers crossed with the header row, an empty cell, a zero-width column, an indented table and a malformed block are not all stated on the item; six of those combinations are settled in the record and are listed in `refinement-qa.md` ready to become criteria or `## Notes` entries at the rewrite.
  - `criteria-are-decidable` → **fail** (this is R4 restated, and the reason the item is not moving to `ready`). AC1, AC2, AC4, AC5 and AC6 are each decidable in principle but not as written — the command is clear, the verdict is not, because "offset" and "character" name a measure the project does not use and AC4 names no criteria by ID. **AC3 is not decidable at all** until `Q-001` is answered: two implementations differing only in which side gets the leftover space would both satisfy "padding on both sides, differing by at most one character", and a verifier with a terminal and no context could not choose between them. That is the gate doing its job.
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item WI-0002`, exit 0). Rule 1 has nothing to check yet — no human answer on this item is consumed. The substantive check was done by hand and is in `Q-001`'s `## Cross-answer check`: EP-001/Q-001, WI-0001/Q-001, WI-0001/Q-003 and WI-0001/Q-004, each with a verdict of compatible and a reason. Rule 2 does not fire: no verdict is `conflicts`. No document under `docs/` was edited by this execution, so rule 3 has nothing to see.
  - `qa-recorded-verbatim` → **pass, on what there is to record.** `artifacts/refinement-qa.md` contains the question that was asked, in full, and states plainly under `## Round 1` that the answer is not yet given. It declares `status: agenda`, not `recorded`, so it cannot satisfy R8 by existing. Nothing is tagged `[human]` because the human has said nothing on this item; nothing is tagged `[assumed]` because this execution assumed nothing. The eight items under `## Settled from the record` each cite the artifact that settles them rather than being presented as answers.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` (new; blocking, addressed to `human`, with `## Options considered` listing A, B and C before the recommendation, marked as ours per `spec/question.md`, and `## Answer` and `## Consequences` present and empty)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new; `status: agenda`, the full Definition of Ready walk, the one question, and the eight things settled from the record)
  - `tracker/items/WI-0002/item.md` (`## Notes` narrowed from three open unknowns to one, with what settles the other two; the acceptance criteria are untouched and the note says so)
  - `tracker/items/WI-0002/history.md` (this move)
  - `tracker/items/WI-0002/journal.md` (this entry)
  - `tracker/board.md` (regenerated by `transition` step 6)
- **Status:** `draft` → `awaiting-answer`
- **Result:** Refinement of WI-0002 got as far as it can without the stakeholder. The Definition of Ready walk is on disk with per-criterion evidence, eight of the nine gaps are closed from the existing record — two of them things this item wrongly listed as open — and the single remaining unknown, which side of a centred cell gets an odd leftover space, is asked as `Q-001` and blocks the item. The criteria are deliberately left unrewritten so that the resuming execution rewrites all six at once against a complete set of answers.

## 2026-08-29T22:33:17Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer` with `Q-001` open and its `## Answer` filled in by the
  stakeholder; dispatched ahead of `next`, because an answered question left open stops the
  orchestrator on every subsequent run.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` (the only question on this item)
  - `tracker/items/WI-0002/item.md`, `history.md`, `artifacts/refinement-qa.md`
  - `tracker/items/WI-0002/artifacts/plan.md` — does not exist; the item has not been planned
  - `docs/product/vision.md` (v3, as read)
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003` (v1, as read), `ADR-0004`
  - `mdtab.py` — `compose_row`, `compose_delimiter`, `column_widths`, to check what the code
    actually does before writing an ADR about changing it
  - `.claude/agile-skills/spec/question.md`, `doc-header.md`, `journal-and-history.md`
- **Cross-answer check:** `WI-0002/Q-001` (the answer consumed here) checked against
  `EP-001/Q-001` — compatible, neither half changes a column's width and the padding stays inside
  the closing pipe; `WI-0001/Q-001` — compatible, the leftover is a count of display columns;
  `WI-0001/Q-003` — compatible, padding moves within the column's width and never into the two
  spaces; `WI-0001/Q-004` — compatible, and it is the pair that had to be reasoned about rather
  than asserted, because *"every row … no exceptions"* read at its widest would reach the
  delimiter row. It does not: the sentence's subject is where a cell's **text** sits, and the same
  stakeholder calls the delimiter row *"a rule under the header, not a row of content"*. No
  conflict was declared, so nothing was escalated. The full reasoning is in the question's
  `## Cross-answer check`. This bullet also covers the one paragraph under `docs/` this execution
  removed that carried `[src: WI-0001/Q-004]` — the `## What is not yet decided` entry saying the
  centring split and the delimiter colons were still for `refine` on WI-0002. It was removed
  because both are now settled — one by this very answer, one by ADR-0004 — not because a later
  answer of theirs overtook it, and the clause it cited `WI-0001/Q-004` for (that a markerless
  delimiter row is already settled) is restated unchanged in `### Round 2`.
- **Decisions:**
  - Recorded the answer as **ADR-0005** rather than only in the item, because `plan` and
    `implement` read ADRs and never the Q&A, and because the reply settled two things — the odd
    centring remainder, and that no content cell of a marked column is exempt. Route: the human
    answered an escalation; the ADR is where their decision lands so the code can be checked
    against it.
  - **Did not supersede ADR-0003.** Its decision 9 reads as though padding always follows the
    text, but ADR-0004 decision 3 already recorded, in as many words, that where a marker puts
    cell text was WI-0002's to decide and was not implemented under WI-0001. ADR-0005 takes that
    deferred decision rather than overturning a standing one, and ten of ADR-0003's eleven
    decisions are untouched, so restating the whole thing would have been ceremony.
  - Gave ADR-0003 a `provenance` correction under `spec/doc-header.md` §4b instead: decision 9's
    words are unchanged, and it now cites ADR-0004 and ADR-0005. The alternative was to leave two
    current documents that a reader could take as disagreeing, which is the failure ADR-0003 was
    itself written to remove.
  - **Amended no acceptance criterion.** The item is at `draft`, its criteria are not frozen, and
    `refine` resumes to rewrite all six in one pass — AC1 to AC3 into display width, AC3 to name
    the side an odd remainder falls on, AC4 to name what it reads. Editing AC3 alone would have
    split one DoR walk across two skills and left the other three gaps looking settled. What AC3
    must now say is recorded in `item.md` `## Notes` and in `refinement-qa.md`.
  - **Filed no new work item.** The unprompted half of the answer confirms what AC1 to AC3 already
    say — "every cell's text in that column", which includes the header row — so it closes an R10
    combination rather than widening scope. Nothing in it needs an item that does not exist.
  - Recorded one reading as the team's, marked as ours: a column with **no** marker has no marker
    saying anything, so *"every column"* does not reach it and WI-0001's right-hand padding stands
    (ADR-0005 decision 4, option F). It changes no behaviour and contradicts nothing they said, so
    it did not meet any of `spec/question.md` §4's four conditions.
  - Left `refinement-qa.md` at `status: agenda`. Round 1 is now verbatim and true, but `refine`
    owns that field and has not finished its walk; declaring somebody else's conversation complete
    would let R8 pass on our say-so.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 1 consumed human
    answer checked, 0 errors
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 first, on 11 errors: 9
    `claim.citation.unresolved`, every one of them the form `[src: ADR-0005 decision 2]`, which
    the gate does not accept, plus the two this execution expects to clear on transition. Rewrote
    every ADR citation to the bare `ADR-####` form and moved the decision number into the prose;
    re-ran → exit 1 on only `board.stale` and `question.awaiting.none-open`, both of which this
    transition and `board-gen` clear.
- **Gates:**
  - `answer-is-propagated` → **pass**. Each of the five files named in `Q-001`'s `## Consequences`
    was opened after writing: `ADR-0005` exists with six decisions; `ADR-0003` is v2 with the
    `## Corrections` row and decision 9's new citation; `vision.md` is v4 with `### Round 2` and
    without the centring-remainder entry; `item.md` `## Notes` carries the answer and what it does
    not reach; `refinement-qa.md` `## Round 1` carries the reply verbatim.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own, quoted verbatim,
    and it is recorded as ADR-0005 with its options and reversibility. The two readings that were
    ours and not theirs — the delimiter row, and a markerless column — each cite what settles them
    (`WI-0001/Q-004` and ADR-0004; `WI-0002` AC4 and ADR-0003).
  - `escalation-is-justified` → **skipped**, nothing was escalated. No cross-answer verdict was
    `conflicts`, and none of `spec/question.md` §4's four conditions applied to anything left over.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0).
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after this transition and
    `board-gen`; the two remaining errors before it were `board.stale` and
    `question.awaiting.none-open`, which are what a consumed answer looks like mid-move).
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-29T22:22:51Z records
    `resume-to: draft`; this execution returns the item to `draft`, not to `ready`.
  - `a-deferral-is-not-an-answer` → **not applicable, and stated rather than skipped**. The reply
    settles the question outright and adds a second decision; it defers nothing, so neither of
    step 3a's two moves was in play and `Q-001` is `answered`, not `deferred`.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at` stamped; `## Consequences` naming five files; `## Cross-answer check` extended
    with the consumption-time check, keeping `refine`'s filing-time check below it
  - `docs/architecture/adr/ADR-0005-alignment-markers-place-cell-text.md` — created
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` — v2, `## Corrections`
    provenance entry on decision 9
  - `docs/product/vision.md` — v4, `### Round 2 of refinement, on WI-0002`
  - `tracker/items/WI-0002/item.md` — `## Notes` rewritten around the answer
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1 recorded verbatim; R4, R6 and R8
    rows updated; the header-cell entry re-sourced to the stakeholder's own words
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's answer to `Q-001` is consumed and propagated into five files, with
  the odd centring remainder going right and no content cell of a marked column exempt, both
  recorded as ADR-0005. No criterion was amended and no new work was implied, so WI-0002 returns
  to `draft` for `refine` to rewrite its six criteria in one pass.

## 2026-08-29T22:37:32Z — refine v0.3.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` as the only runnable candidate
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (the agenda this execution resumed against)
  - `tracker/items/WI-0002/questions/Q-001.md` — answered by the stakeholder, consumed by
    `answer-questions` at 2026-08-29T22:33:17Z
  - `tracker/items/WI-0001/item.md` — its eleven criteria, by ID, for AC9 and AC4
  - `tracker/items/EP-001/questions/Q-001.md`, `WI-0001/questions/Q-001.md`, `Q-003.md`, `Q-004.md`
  - `docs/product/vision.md` (v4), `docs/architecture/adr/ADR-0001`, `ADR-0003` (v2), `ADR-0004`,
    `ADR-0005`
  - `mdtab.py` — `compose_row`, `compose_delimiter`, `column_widths`, to check that AC5's
    zero-width cases are arithmetic the code can actually produce rather than something invented
  - `tracker/project.yaml` for the test command AC10 names
  - `.claude/agile-skills/spec/dor-dod.md` §1, `work-item.md`, `question.md`
- **Cross-answer check:** No new answer was received by this execution — round 1's was consumed by
  `answer-questions` before it ran, and round 2 was considered and not held. The criteria written
  here from a stakeholder answer were each checked against their prior answers: AC3's remainder
  against `WI-0001/Q-001` (compatible — the leftover is display columns, not characters) and
  `WI-0001/Q-003` (compatible — the split stays inside `W`, the two surrounding spaces are
  untouched); AC1 to AC3's "the header row included" against `WI-0001/Q-004` (compatible — that
  answer scopes the **delimiter** row, which the item now puts in `## Out of scope` on the
  stakeholder's own words, *"a rule under the header, not a row of content"*); AC7 against
  `WI-0001/Q-004` again (compatible — it constrains colons, which that answer's source question
  said in writing it was not asking about); the whole set against `EP-001/Q-001` (compatible —
  nothing widens a column or hangs off the right-hand edge). No verdict was `conflicts`, so
  nothing was escalated. No sentence in `docs/` sourced to one of their answers was edited by this
  execution.
- **Decisions:**
  - **Did not hold a round 2.** Every remaining Definition of Ready gap was closed from the record
    under SKILL.md step 3 — two by their own prior answers, four as decisions that would be the
    same whoever the stakeholder was, one routed to `plan`. Each is listed individually in
    `refinement-qa.md` `## Round 2` with which test in step 3 it fell to. Asking anyway would have
    cost a round trip to be told things they had already said.
  - **Rewrote all six criteria into ten.** AC1 and AC2 (left and right) now give the composed cell
    as a formula in `W` and `w` instead of saying "the same offset", so the observation is a
    byte-comparison rather than a judgement; both name the header row explicitly, on the
    stakeholder's *"every row, every column, no exceptions"*. AC3 (centre) replaces "differing by
    at most one character" — which was true of both answers to `Q-001` and therefore decided
    nothing — with `(W - w) // 2` on the left and the remainder on the right, plus two worked
    examples. AC4 (markerless) now states the composition itself rather than deferring to another
    item's test suite. AC5 to AC8 are new and close R10 crossings that nothing stated: empty cells,
    all-empty marked columns, wide and combining characters, and idempotence over marked tables.
    AC7 replaces the old AC5's "mean the same thing" with colon-for-colon identity per column.
    AC10 replaces the old AC6 and adds the exit-status assertion WI-0001 carried and this item had
    dropped.
  - **AC9 is written as a read, not as a suite result** (SKILL.md step 6a). It names all eleven of
    WI-0001's criteria by ID, says the verdict comes from reading each criterion's text against the
    new behaviour with the suite as evidence, singles out WI-0001 AC3 as the one this item's
    behaviour changes, and requires the non-intersection case to be stated and then covered or
    waived by ID. Written this way because the alternative — "WI-0001's tests still pass unchanged",
    which is what the old AC4 said — is satisfiable by a suite that never exercises both rules at
    once, which is exactly the F-065 shape.
  - **Did not edit WI-0001 AC3.** Its text now holds only for a markerless column. It is a
    delivered item's criterion and repairing it here would rewrite the record of what was verified;
    AC9 requires the reconciliation to be recorded in this item's verify report instead.
  - **Left the indented-table crossing deliberately unconstrained**, named as such in the R10
    table with who left it so. ADR-0003 re-emits an indented block's own prefix and excludes it
    from the widths, so it cannot interact with where padding sits inside a column; writing a
    criterion for it would assert coverage of an interaction that does not exist.
  - **Added "checking that a renderer agrees" to `## Out of scope`.** It is the thing a reader of
    the title — "honour column alignment markers" — is most likely to assume is included, and no
    criterion renders anything.
- **Questions raised:** none. One question was already on file, `Q-001`, answered by the
  stakeholder and consumed before this execution began; `refinement-qa.md` records why round 2 was
  not held.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 1 consumed human
    answer checked, 0 errors
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 3 items and 7 documents,
    0 errors
  - `python3 .claude/agile-skills/scripts/board-gen .` → board regenerated
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `definition-of-ready` → **pass**, criterion by criterion, the full walk recorded in
    `refinement-qa.md` `## Definition of Ready — the walk at exit`. R1 pass (frontmatter, auto);
    R2 pass (story unchanged, names role, capability and outcome); R3 pass (AC1 to AC10, labelled
    checkboxes); **R4 fail on entry** — AC1 to AC3 said "offset" and "character", AC3 did not say
    which side an odd remainder falls on, AC4 deferred to another item's suite, AC5 did not say
    what "mean the same thing" was checked against — **now pass**, all ten rewritten as
    observations; R5 pass on entry and extended from two entries to six; R6 pass (no open
    question; it failed on entry only because `Q-001` was open); R7 pass (`WI-0001` done, merged
    `045c779`); **R8 fail on entry** (the file was an `agenda`) **now pass** (`status: recorded`,
    round 1 verbatim); R9 pass (one change, in the one function that composes a content row);
    **R10 fail on entry** — the three markers were not crossed with the header row, an empty cell,
    a zero-width column, an indented table or a malformed block — **now pass**, eleven crossings
    tabulated in `## Notes`, each pointing at a criterion, a scope entry, or a named deliberate
    non-constraint.
  - `criteria-are-decidable` → **pass**. For AC1 to AC8 the observation is the same in shape: run
    `python3 mdtab.py < <fixture>`, compare the bytes against the expected-output fixture; the
    verdict is equality or not. AC1 to AC4 additionally state the composed cell as a formula in `W`
    and `w`, so a reader can compute the expectation without running anything. AC5 and AC8 add a
    second run over the first run's output and compare the two. AC6's verdict is that every output
    line of the table has equal display width under the function ADR-0003 names. AC9 is settled by
    inspecting `artifacts/verify-report.md` for a verdict against each of eleven named WI-0001
    criteria and for the two statements it requires; the verdict is present-and-complete or not.
    AC10 is settled by `python3 -m unittest discover -s tests -t .` exiting 0 with a test named for
    each of AC1 to AC9, and by the filter's exit status.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002`, exit 0).
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` is `status: recorded` and holds the one
    question asked and the reply in full, quoted, tagged `[human]`; the seven round-2 gaps closed
    without asking are each tagged `[human]` where their own earlier words settled it and
    `[assumed]` where this skill decided, with the deferral or document relied on named. Nothing is
    tagged `[unresolved]`, because nothing is.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — `## Acceptance criteria` rewritten from six to ten with a
    definitions preamble; `## Out of scope` extended from two entries to six; `## Notes` rewritten
    around what the stakeholder settled, the R10 crossing table, what is left to `plan`, and the
    inherited non-UTF-8 fixture hazard
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; `## Round 2
    — considered, and not held` added; `## Definition of Ready — the walk at exit` added; the
    entry-state table and `## Round 1` left as they were
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Ten criteria, each settled by comparing bytes against an expected
  output or by inspecting a named artifact, and every Definition of Ready criterion met without an
  override and without a second round of the stakeholder's attention.

## 2026-08-29T22:42:42Z — plan v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` as the only runnable candidate
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` (the ten criteria this plan is a contract against),
    `history.md`, `journal.md`, `artifacts/refinement-qa.md` — including the seven round-2 entries
    tagged `[assumed]`, which is where this design's soft ground is
  - `tracker/items/WI-0002/questions/Q-001.md` — the stakeholder's answer and its cross-answer
    check
  - `tracker/items/WI-0001/item.md` — its eleven criteria by ID, for the AC9 mapping and step 5
  - `docs/architecture/overview.md` (v2, as read), `docs/product/vision.md` (v4)
  - ADR-0001, ADR-0003 (v2), ADR-0004, ADR-0005; ADR-0002 noted as superseded and not relied on
  - `mdtab.py` — `column_widths`, `compose_row`, `compose_delimiter`, `emit_block`,
    `table_or_none`, `display_width`, and the module docstring
  - `tests/test_mdtab.py` — every test method name, `INPUT_FIXTURES`, and the AC4, AC9 and AC11
    tests in full; `tests/fixtures/markers.md` and `markers.expected.md`
  - `tracker/project.yaml`
- **Cross-answer check:** This plan relies on one human answer, `WI-0002/Q-001`, and records no
  new one. Checked against `WI-0001/Q-003` — compatible: the plan's step 2 splits `pad`, which is
  computed inside the column's width, so the one space either side of the cell text is untouched.
  Checked against `WI-0001/Q-004` — compatible: `compose_delimiter` is explicitly not modified, so
  the delimiter row keeps the composition that answer and ADR-0004 fixed. Checked against
  `EP-001/Q-001` — compatible: no step changes a column's width, and a right-aligned final
  column's padding is placed before the closing space, so no composed line can end in whitespace.
  No verdict was `conflicts`, nothing was escalated, and no sentence in `docs/` sourced to one of
  their answers was edited by this execution — the overview's rule-document list and ADR-0003's
  decision-9 note are the pipeline's own prose, not theirs.
- **Decisions:**
  - **Alignment is read once per table and passed down** — a new `column_alignments(rows)` beside
    `column_widths(rows)`, with `emit_block` handing the result to `compose_row`. Route:
    documented. It mirrors the arrangement already in the file, and it keeps `compose_row` a pure
    function of its arguments so it can be tested on its own. The alternative — deriving the
    alignment inside `compose_row` from the delimiter cells — is recorded under `## Assumptions`
    with its reversal cost, because it is one signature and three call sites in one file.
  - **`None` and `LEFT` stay distinct in the code although they compose identically.** Route:
    assumed, reversible by deleting one branch. Kept because ADR-0005 decides the markerless case
    (decision 4) separately from the left-marked one (decision 1), and a reader of the code should
    be able to see two decisions where the ADR records two.
  - **ADR-0006 written: test method names carry the item ID.** Route: decided, with three options
    named. This was not optional and could not wait for `implement`: WI-0001's coverage test
    requires exactly one method containing `ac<n>_` for each n, and any test this item names
    `test_ac1_...` would make a delivered, verified criterion start failing. The alternatives — a
    separate module scoped by path, or continuing this item's numbering from WI-0001's — are in
    the ADR with their costs.
  - **The module docstring's wrong ADR-0004 filename is corrected inside step 4, and the
    correction is called out in the plan rather than folded in.** Route: decided. `mdtab.py` cites
    `ADR-0004-delimiter-row-keeps-alignment-markers.md`; the file is
    `ADR-0004-delimiter-row-preserves-alignment-markers.md`. It is a defect in a delivered
    artifact and the escalation rule says such a thing is normally a `bug` item — it is not filed
    as one here because step 4 rewrites those exact lines in order to add ADR-0005, the fix
    changes no behaviour and no criterion, and a bug item would cost four skill executions to
    correct a path in a comment. `lint-claims` cannot see it: it walks `*.md` only, so the
    citation lives in the one file class the gate does not read. Recorded so a reviewer who
    thinks a bug item was owed can say so.
  - **`markers.expected.md` is regenerated and its diff read against AC3's worked examples**
    rather than accepted from the filter's own output. Route: decided, and it is `## Risks`' first
    entry. It is the one fixture where a wrong padding rule would be frozen into the expectation
    and then confirmed by a passing test.
  - **AC9 is mapped to `verify`'s report, not to a test.** Route: assumed, with the reversal cost
    stated. The criterion asks for eleven criteria's *text* to be read against the new behaviour;
    no assertion performs a read. `implement` supplies the evidence — the suite result after the
    rename and the `markers.expected.md` diff — and states the WI-0001 AC3 reconciliation in
    `impl-report.md`.
  - **The escaped-pipe question was not decided.** `docs/product/vision.md` routes it to `plan`,
    but no criterion of this item raises it and no step touches `split_cells`. Deciding it here
    would be designing past the item; it stays open for whichever item needs it.
  - **`docs/architecture/overview.md` bumped to v3.** The change alters which documents a reader
    must read to know whether the code is right — ADR-0005 now decides cell placement and ADR-0006
    decides test naming — and the layout table's description of test names is no longer true.
- **Questions raised:** none. Every decision this plan forced was answerable from ADR-0003,
  ADR-0004, ADR-0005 and the stakeholder's recorded answers, or was reversible in one file and
  recorded under `## Assumptions`. Nothing was irreversible and nothing depended on intent no
  document records, so `spec/question.md` §1's third branch was not reached.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 14 tests, OK (the command
    `tracker/project.yaml` declares, run in this project before declaring it resolved)
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 1 first, on 3
    `claim.unsourced` errors in ADR-0006; added citations to the three paragraphs and re-ran →
    exit 0, 2 documents in scope
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 8 consumed human
    answers checked
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 3 items, 8 documents
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0).
  - `every-criterion-is-addressed` → **pass**. `plan.md` `## Acceptance criteria mapping` has one
    row for each of AC1 to AC10, each naming the numbered steps that satisfy it and the specific
    test or artifact that demonstrates it — not "tests". AC9's row says in as many words that it
    is not a code test and what `implement` supplies instead.
  - `project-commands-resolved` → **pass**. `commands.test` and `commands.lint` were already set
    by WI-0001's plan and both were run in this execution, exit 0 each. `commands.build` is `null`
    and honestly so: there is nothing to build [src: ADR-0001].
  - `decisions-recorded` → **pass**. Eight choices, each pointing at an ADR or at an
    `## Assumptions` entry with its reversal cost: alignment read per table (assumptions), `None`
    vs `LEFT` kept distinct (assumptions), test naming (ADR-0006), the docstring correction (this
    journal and plan step 4), the fixture regeneration (plan risks), AC9 mapped to the report
    (assumptions), the single-table `aligned.md` (assumptions), and the overview bump.
  - `plan-is-executable-without-you` → **advisory, pass**. Read cold, each of the nine steps names
    the file it changes and what is true afterwards; steps 1 to 3 give the arithmetic, step 6
    names three fixtures and what each must contain, and step 8 names the test-naming convention.
    The one place a reader must still choose is the slug in each test name, which ADR-0006 leaves
    free on purpose.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted`, exit 0).
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted`, exit 0, after sourcing three
    absolutes in ADR-0006). Noted and **not** repaired: the same gate under `--all` reports four
    pre-existing `claim.unsourced` errors in ADR-0001 and ADR-0003 Context paragraphs, written
    before this execution and outside its window. They are `review-close`'s to take under D12 with
    `spec/doc-header.md` §4b's `provenance` route; repairing another item's ADR from inside this
    plan would put the edit outside any scope a gate can see.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — problem, approach, nine steps, the ten-row
    criteria mapping, four assumptions, the ADR list, `## Scaffolding: none`, five risks and the
    out-of-scope list
  - `docs/architecture/adr/ADR-0006-per-item-test-name-prefixes.md` (new)
  - `docs/architecture/overview.md` — v3
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. The change is two functions in `mdtab.py` and a signature, plus
  three new fixtures, one regenerated one, and a rename of WI-0001's test methods that ADR-0006
  forced and records. Every criterion has a step and a demonstration, and nothing was left for
  `implement` to decide except the wording of test names.

## 2026-08-29T22:44:47Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next` as the only runnable item (EP-001 and WI-0001 have no status owner; `engagement-state EP-001` reports active).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the ten acceptance criteria, `## Out of scope`, `## Notes`
  - `tracker/items/WI-0002/artifacts/plan.md` — nine steps, the AC mapping table, assumptions and risks
  - `tracker/items/WI-0002/history.md` — five rows; the last is `ready → planned` by `plan`, so this is a fresh start and no branch existed
  - `tracker/items/WI-0002/questions/Q-001.md` — `answered`, propagated by `answer-questions` into ADR-0005 and the item before `refine` resumed
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both non-null; branch prefix `wi/`, commit subject convention
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md`, `ADR-0004-delimiter-row-preserves-alignment-markers.md`, `ADR-0005-alignment-markers-place-cell-text.md`, `ADR-0006-per-item-test-name-prefixes.md`
  - `mdtab.py` — `compose_row`, `compose_delimiter`, `column_widths`, `emit_block`, the module docstring
  - `tests/test_mdtab.py` — the eleven WI-0001 criterion tests, `INPUT_FIXTURES`, the coverage test's `ac%d_` tag
  - `tests/fixtures/markers.md` and `markers.expected.md` — the fixture pair plan.md step 7 regenerates
- **Decisions:**
  - none yet — this entry opens the execution. The branch `wi/WI-0002` was cut from `main` at `b4568fe` before any file was changed, so an interruption from here leaves a truthful `in-progress` with an empty branch.
- **Cross-answer check:** none — this execution has changed no file yet, and so has edited no claim in `docs/` sourced to a stakeholder answer.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0 (Switched to a new branch 'wi/WI-0002')
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no change has been made; run on the branch head at step 7)
  - `lint-clean` → **skipped** (not yet run, same reason)
  - `workspace-valid` → **skipped** (not yet run for this execution; `next` validated the workspace clean immediately before dispatch)
  - `every-criterion-has-a-test` → **skipped** (not yet run: no test written yet)
  - `commits-reference-the-item` → **skipped** (not yet run: no commit on the branch yet)
  - `cross-answer-consistency` → **skipped** (not yet run: nothing changed since `main`)
  - `claims-are-sourced` → **skipped** (not yet run: nothing changed since `main`)
- **Artifacts:**
  - branch `wi/WI-0002`, cut from `main` at `b4568fe`, no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started. The plan's nine steps will be executed in order on `wi/WI-0002`; the closing entry at the move to `verifying` is the one that reports the work and runs the gates.

## 2026-08-29T22:55:47Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, continuing this execution's own opening entry; the plan's nine steps are complete.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `artifacts/plan.md`, `history.md`, `questions/Q-001.md`
  - `tracker/project.yaml` — `commands.test` and `commands.lint`, both non-null
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` (decision 9 and its `## Corrections` row), `ADR-0004-delimiter-row-preserves-alignment-markers.md`, `ADR-0005-alignment-markers-place-cell-text.md`, `ADR-0006-per-item-test-name-prefixes.md`
  - `docs/product/vision.md` — the "Round 2 of refinement, on WI-0002" section, for the D12 check
  - `mdtab.py`, `tests/test_mdtab.py`, and every fixture under `tests/fixtures/`
- **Decisions:**
  - **Plan step 7 was brought forward to run immediately after step 4**, so the suite is green at every commit instead of red across two. Regenerating `markers.expected.md` is what makes `test_wi0001_ac4_...` pass again once `compose_row` changes. The step itself is unchanged: the diff was regenerated and read, and it is one line — the Center column's `b` becomes `   b    `, the Right column's `c` becomes `     c `, the delimiter row byte-identical.
  - **AC3's two worked examples were both asserted, and no question was filed.** AC3's literal `| Q |` and its "a centred column of width 3 … one space of padding on each side" cannot describe the same column: at `W=3, w=1` the criterion's own arithmetic gives `|  Q  |`, and `| Q |` is the width-1 column AC5's minimum-width rule produces. Both readings agree with AC3's formula, so **no behavioural decision was available to take** — this is a defect in an illustration, not a silence in the specification, and the escalation test ("a user would notice it and no criterion covers it") is not met. The test asserts `|  Q  |` at width 3 and `| Q |` at width 1, and `impl-report.md` Deviations 3 flags it for `verify`, which will find `| Q |` at width 3 absent and should.
  - **AC7's `W + 2` clause was scoped to fixtures whose pipe blocks the filter recognises as tables**; its colon-for-colon clause was not scoped and runs over all 19. WI-0002's preamble defines a table as what ADR-0003 recognises as one, and its `## Out of scope` says an unrecognised block is copied byte for byte, so a fenced, blockquoted, indent-mismatched or malformed block keeps its input delimiter length. My first version asserted the span over everything and failed on three fixtures; the fix narrowed the assertion to what the criterion actually claims rather than weakening it.
  - **AC7's delimiter-row parser was written independently of `table_or_none`** rather than calling it. Using the module's own recognition to check the module's own output would have made the criterion a tautology.
  - **The ADR-0004 filename correction in the module docstring was made and no bug item was filed**, following plan.md step 4. It is a defect in an artifact WI-0001 delivered; it is fixed inside a step that rewrites those exact lines, changes no behaviour and no criterion. Recorded loudly in `impl-report.md` Deviations 2 rather than folded in — a reviewer who thinks a bug item was owed should say so.
  - **Decided not to decide:** nothing about escaped pipes inside a cell. `docs/product/vision.md` routes that to `plan`, no criterion of this item raises it, and `split_cells` is unmodified.
- **Cross-answer check:** none — this execution changed no file under `docs/`, so it rewrote no sentence carrying a stakeholder's citation and ADR-0008 §3's third row was not reached. The standing claims about this behaviour were checked under D12 and are now **true of the code** rather than falsified by it: `docs/product/vision.md` line 121, *"No content cell of a marked column is exempt: the header cell obeys its column's marker exactly as a body cell does"* [src: WI-0002/Q-001], is exactly what the header-exemption mutation below shows the suite enforces. `ADR-0003` decision 9 already carries a `## Corrections` row pointing at ADR-0005, added by `answer-questions` before this execution, so no repair was owed there either.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
  - `python3 -c "…mdtab.column_alignments(rows of markers.md)"` → 0, printed `['left', 'centre', 'right', None]` (plan step 1's own check)
  - `python3 -c "…mdtab.compose_row(['ab'], [3], [CENTRE], '')"` → 0, printed `'| ab  |'` (plan step 2's check)
  - `python3 mdtab.py < tests/fixtures/markers.md` → 0, Center's `b` centred and Right's `c` against its right-hand space (plan step 3's check)
  - `python3 -c "…every docs/ path in mdtab.__doc__ exists"` → 0, three paths, all OK (plan step 4's check)
  - `diff -u tests/fixtures/markers.expected.md /tmp/markers.new` → 1 (one changed line, delimiter rows identical) (plan step 7's check)
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 24 tests in 4.767s` / `OK` — run on the branch head after the last code commit, and again after the report commit
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → 0, no output
  - `.claude/agile-skills/scripts/validate-workspace .` → 1 first, then 0. The first run rejected `[src: ADR-0005 decision 1]` and `[src: ADR-0005 decision 2]` in `impl-report.md` with `claim.citation.unresolved`; both were rewritten to the bare `ADR-0005` with the decision number in the prose, and it then reported `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 4 commit(s) on main..wi/WI-0002 name WI-0002`
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → 0, `checked 8 consumed human answer(s)`, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0, `0 errors, 0 warnings`
  - **Five mutation runs of `mdtab.py`, each reverted:** odd centring remainder to the left; `RIGHT` ignored; all markers ignored; the header row exempted from its column's marker; a delimiter colon moved to the other end. Each failed at least one criterion's test — the header-exemption mutation failed AC1 to AC4, which is what makes ADR-0005's decision 3 tested rather than asserted.
  - **A sixth run applying the first mutation *and* regenerating every expected fixture from the mutated filter**, which is plan.md's top risk made concrete: `test_wi0002_ac3_…` still failed, on its formula assertion, `AssertionError: '  Centre ' != ' Centre  '`. A wrong split cannot be frozen into the fixtures.
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 24 tests` / `OK`, on branch head `a324868` and again after the report commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` exit 0)
  - `workspace-valid` → **pass** (`checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings`, exit 0 — after the two citations were rewritten)
  - `every-criterion-has-a-test` → **pass** (AC1 `test_wi0002_ac1_left_marker_pads_to_the_right`; AC2 `…ac2_right_marker_pads_to_the_left`; AC3 `…ac3_centre_marker_puts_the_odd_space_on_the_right`; AC4 `…ac4_no_marker_is_unchanged_by_this_item`; AC5 `…ac5_empty_cells_and_zero_width_marked_columns`; AC6 `…ac6_markers_and_display_width_together`; AC7 `…ac7_markers_survive_and_mean_the_same_thing`; AC8 `…ac8_idempotence_over_marked_tables`; AC9 `…ac9_wi0001_criteria_meet_marked_columns`, whose machine-checkable half only — the verdicts are `verify`'s; AC10 `…ac10_each_criterion_has_a_named_test`. No criterion is demonstrated by reading the code, and every one of them was shown to fail under at least one mutation)
  - `commits-reference-the-item` → **pass** (`all 4 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0)
  - `no-unplanned-scope` (advisory) → **pass** (three hunks in `mdtab.py` → plan steps 4, 1+2, 3; `markers.expected.md` → step 7; the three new fixture pairs → step 6; `tests/test_mdtab.py` → steps 5 and 8; `tracker/` and `board.md` → the transitions. No hunk without a step, and no neighbouring defect fixed except the one plan step 4 names)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` exit 0; the window is legitimately empty because this execution changed nothing under `docs/`, and the `**Cross-answer check:**` bullet above records why)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0, citations checked over every markdown file in the workspace)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` — new
  - `mdtab.py` — `column_alignments` added, `compose_row` and `emit_block` changed, module docstring corrected and extended
  - `tests/test_mdtab.py` — WI-0001's eleven criterion methods renamed per ADR-0006, its coverage tag narrowed, module docstring rewritten, `INPUT_FIXTURES` extended, ten WI-0002 criterion tests added
  - `tests/fixtures/aligned.md`, `aligned.expected.md`, `aligned_empty.md`, `aligned_empty.expected.md`, `aligned_wide.md`, `aligned_wide.expected.md` — new
  - `tests/fixtures/markers.expected.md` — regenerated, one line changed
  - branch `wi/WI-0002`, commits `c64f374..3 more`, range `main..wi/WI-0002` = 4 commits
- **Status:** `in-progress` → `verifying`
- **Result:** WI-0002 is implemented on `wi/WI-0002` in four commits. A column's alignment marker now places its cell text — left keeps the padding right, right moves it all left, centre splits it with the odd space going right, and a markerless column is untouched — for every content cell including the header. All ten criteria have a named test, all eight gates pass on the branch head, and every test was shown to fail under a mutation that removes the behaviour it covers. Three things are handed to `verify` rather than left to be discovered: AC9's eleven verdicts are its artifact to write and `impl-report.md` sets out the evidence it needs, AC3's literal `| Q |` describes a width-1 column and not the width-3 one its sentence begins with, and the ADR-0004 filename correction in the module docstring was made without a bug item on plan step 4's instruction.

## 2026-08-29T23:04:17Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable item (EP-001 and WI-0001 have no status owner; `engagement-state EP-001` reports active).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the ten acceptance criteria and the preamble that defines "running the filter", "display width", "a table", `W` and `w`. **Read before `impl-report.md`**, so that what would settle each criterion was derived from the criterion.
  - `tracker/items/WI-0002/artifacts/plan.md` — the nine steps and the AC mapping, for the diff read
  - `tracker/items/WI-0002/artifacts/impl-report.md` — the claimed evidence, checked rather than trusted; nothing in this verification cites it
  - `tracker/items/WI-0002/history.md`, `questions/Q-001.md`
  - `tracker/items/WI-0001/item.md` — all eleven acceptance criteria verbatim, for AC9's read
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` (decision 9 and its `## Corrections` row), `ADR-0004-delimiter-row-preserves-alignment-markers.md`, `ADR-0005-alignment-markers-place-cell-text.md`, `ADR-0006-per-item-test-name-prefixes.md`
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - the code at branch head **`867ef75115237bf3eb920ca5bb828e459412a2a9`** on `wi/WI-0002`: `mdtab.py` in full, `tests/test_mdtab.py`, and `git diff main..HEAD -- mdtab.py`
- **Decisions:**
  - **The verification harness was written not to import `mdtab`.** `/tmp/vfy/probe.py` reimplements display width from the criteria preamble's own words and runs the filter as a subprocess. Every input used below is one I wrote for this verification; none of the item's own fixtures is evidence for any verdict. Reusing `mdtab.display_width` or the delivered fixtures would have made several criteria tautologies.
  - **AC3 is `pass`, and its second worked example is a defect in the criterion's prose.** AC3 says *"a centred column of width 3 … one holding `Q` is written `| Q |` with one space of padding on each side."* Ran both readings: width 3 with `Q` → `'|  Q  |'`, width 1 with `Q` → `'| Q |'`. At `W=3, w=1` the criterion's own arithmetic gives `|  Q  |`, which *is* one space of padding on each side; `| Q |` is the width-1 column. **I considered `ambiguous` and rejected it**, because the record settles it decisively rather than leaving it open: ADR-0005 keeps the one space either side untouched, so dropping the padding at width 3 is not an available reading, and the criterion's governing sentence is arithmetic that the filter satisfies exactly. A criterion that is decidable from the record is not ambiguous, so no question was filed. Recorded in `verify-report.md` `## Defects found` 1 so a reader who checks AC3's literal text and finds `| Q |` absent at width 3 sees it was adjudicated, not missed.
  - **No bug item filed for the ADR-0004 filename correction, and the reasoning is written out to be overturned.** `impl-report.md` Deviations 2 asks a reviewer to rule on it. The escalation rule would route a defect in another item's delivered artifact to a `bug` at `ready` — but the defect does not exist at `867ef75`; it was repaired in `c64f374`, and I verified the repair (every `docs/` path in `mdtab.__doc__` resolves). A bug item describing an already-fixed defect would be closeable on sight and would misdescribe the tree. It is also not behaviour: no criterion covers a docstring path. Whether the *process* owed a bug item is a Definition-of-Done question and is `review-close`'s.
  - **No send-back.** Nothing failed any of this item's own criteria.
  - **WI-0001 AC3 was not unticked and nothing in WI-0001 was edited.** Its padding-position clause is now true only of markerless columns. That is the reconciliation WI-0002 AC9 instructs be *recorded*, not repaired: ADR-0004 stated in as many words that marker placement was WI-0002's decision and not implemented under WI-0001, ADR-0005 takes it, and ADR-0003 decision 9 already carries a `## Corrections` row pointing at ADR-0005. No sentence of the stakeholder's was narrowed to fit another, so ADR-0008's third row is not reached and no question is owed to them. **Checked explicitly for the F-065 shape and it is not present**: there, a coverage gap hid a conflict between two criteria both meant to hold; here the two were never meant to hold together and the supersession is on the record in three documents.
  - **Non-intersection is stated for exactly one criterion.** For WI-0001 AC3's padding-position clause, nothing executable exercises the old criterion and the new behaviour together **and nothing should** — the clause is false of a marked column by design. The covering case is WI-0002 AC4. Nothing is waived, and every other WI-0001 criterion was intersected with a marked column by a probe I ran.
- **Questions raised:** none
- **Commands:** every command below was run by this skill against `867ef75`.
  - `git rev-parse HEAD` → 0, `867ef75115237bf3eb920ca5bb828e459412a2a9`; `git status --short` → clean
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 24 tests in 4.918s` / `OK`
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → 0, no output
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings` (run again after writing the report and ticking the criteria, same result)
  - `python3 /tmp/vfy/ac1234.py` → 0. AC1 `first display column of the text, per row: {1}`, `text-then-padding everywhere: True`; AC2 `last display column: {9}`, `padding-then-text everywhere: True`, header field `'       Rt '`; AC3 rows `pad=6 before=3 after=3 even`, `pad=6 before=3 after=3 even`, `pad=0`, `pad=5 before=2 after=3 ODD -> extra on the RIGHT`; AC4 fields `[' Pl      ', ' m       ', ' plainer ', ' dddd    ']`; `fields disagreeing with the criteria's arithmetic: []`, `W per column, computed independently: [8, 7, 8, 7]`
  - AC3's worked examples as real tables → 0: `width 3 holding 'ab' W=3 header -> '| ab  |'`; `width 3 holding 'Q' W=3 header -> '|  Q  |'`; `width 1 holding 'Q' W=1 header -> '| Q |'`
  - AC5 probes → 0: with three marked columns at different widths, `W: [2, 8, 9]` and `empty-row field lengths: [4, 10, 11] vs W+2: [4, 10, 11]`; all-empty table → output `|  |  |   |` / `|:-|-:|:-:|`, `W: [0, 0, 1]`, field lengths `2, 2, 3`, re-run `byte-identical: True`
  - AC6 probe → 0: `display width of each output line: [21, 21, 21, 21, 21] -> all equal: True`; pipe positions `[0, 7, 14, 20]` on all five rows; `input was genuinely ragged: True {17, 18, 14, 15}`
  - AC7 probe over nine tables → 0: `AC7 all columns of all tables preserve their colons and fill W+2: True`, including widening `:-` → `:---` and narrowing `:--------:` → `:-:`
  - AC8 probe over the same nine → 0: `second run byte-identical: True` for all nine, `exit 0/0`
  - AC10: independent `unittest` discovery → `discovery errors: []`, `total discovered test methods: 24`; exactly one method per `wi0002_ac<n>_` for n in 1..10, each quoting `ACn ` in its docstring; exactly one per `wi0001_ac<n>_` for n in 1..11; filter exit codes over every AC1–AC8 input → `[0]`
  - **Fourteen negative and boundary conditions triggered** → all exit 0: right-marked final column, centre-marked final column with an odd remainder, centre-marked final column with an empty final cell (all three `lines ending in a space or tab: none`), empty input, marked table with no body rows, single `:-:` column at minimum width, all-empty marked columns, malformed block with markers, second row not a delimiter row, blockquoted marked table, fenced marked table, CRLF marked table, marked table with no final newline, non-UTF-8 bytes inside and outside a marked table (`b'plain \x80 bytes\n'` survived byte for byte), delimiter cells written with surrounding spaces
  - **AC9 crossings** → 0: indented **marked** table tidied with its three-space run reproduced on every line; indent-mismatch with markers byte-identical; blockquoted and fenced marked tables byte-identical; prose containing `|:---:|` byte-identical; marked table with non-UTF-8 bytes round-tripped; indented marked table idempotent
  - **Ten mutations**, each applied to the working tree and reverted immediately: M1 `LEFT`/no-marker pad left; M2 `RIGHT` ignored; M3 odd remainder left; M4 `CENTRE` ignored; M5 empty cells unpadded; M6 display width ignores wide characters; M7 leading delimiter colon dropped; M8 extra trailing space per cell; M9 marked fixtures dropped from `INPUT_FIXTURES`; M10 a criterion's test renamed. Every criterion AC1–AC10 failed under at least one; **M9 failed only AC9's test and M10 only AC10's**. M8 deliberately did **not** fail AC8 — widening every cell by one trailing space is still idempotent, so AC8 correctly did not fire; AC8's sensitivity comes from M7. After the last revert `git status --short` was clean and `git rev-parse HEAD` still `867ef75…`, and the suite was green again
  - `git diff main..HEAD -- mdtab.py` → 0, three hunks read in full: the docstring, `LEFT`/`RIGHT`/`CENTRE` + `column_alignments` + the rewritten `compose_row`, and the `emit_block` call site. Every hunk traces to AC1–AC4 and to plan steps 1 to 4. **No unaccounted behaviour**: `pad` cannot go negative because `width` is the maximum over exactly the rows `compose_row` is called for, and `compose_delimiter` is untouched
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 24 tests` / `OK`, run by this skill on `867ef75`)
  - `lint-clean` → **pass** (`python3 -m compileall …` exit 0)
  - `workspace-valid` → **pass** (`0 errors, 0 warnings`, exit 0, before and after this execution's writes)
  - `every-criterion-independently-checked` → **pass** (each of the ten criteria has a command in `verify-report.md` that this skill ran, with its actual output quoted, on inputs written for this verification and with display width reimplemented; no verdict cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (fourteen conditions triggered and their output read, tabulated in `verify-report.md`; the three that matter most are the right- and centre-marked **final** columns, the one shape that could reintroduce trailing whitespace, and it does not)
  - `a-criterion-about-criteria-is-read` → **pass** (AC9 names WI-0001 AC1 to AC11 by ID and each carries a verdict reached from its own sentence, with a probe I ran as evidence; the single non-intersection is stated in those words for AC3's padding-position clause with WI-0002 AC4 named as the covering case and nothing waived; the F-065 shape was checked for and is absent)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (ten mutations, every criterion named in at least one, M9 and M10 isolating AC9 and AC10 exactly; the one deliberate non-failure explained)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — new, carrying `Verified-commit: 867ef75115237bf3eb920ca5bb828e459412a2a9`
  - `tracker/items/WI-0002/item.md` — all ten criteria ticked, each on evidence recorded above; none ticked without a command I ran
  - no bug item filed, and no criterion sent back
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 passes verification at `867ef75`. All ten criteria were checked with commands this skill ran on inputs it wrote, using arithmetic reimplemented from the criteria rather than from the code; fourteen negative and boundary conditions were triggered, including the right- and centre-marked final columns that could have reintroduced trailing whitespace and do not; and ten mutations confirm every criterion's test fails when its behaviour is removed. WI-0001's eleven criteria were re-read by ID — ten still true, and AC3's padding-position clause now true only of markerless columns, which is the recorded supersession by ADR-0005 and not a defect. Two things go to `review-close` rather than back to the developer: AC3's second worked example contradicts the sentence it sits in and the record settles it in favour of `|  Q  |`, and the ADR-0004 filename repair was made without a bug item with the reasoning written out to be overturned.

## 2026-08-29T23:09:49Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable item (EP-001 and WI-0001 have no status owner; `engagement-state EP-001` reports active).
- **Inputs read:**
  - the diff **`main..ef2da0c`**, hunk by hunk — `git diff main..HEAD -- mdtab.py` read in full, plus `--stat` for the fixtures and tests. Three `mdtab.py` hunks, one line of `markers.expected.md`, three new fixture pairs, `tests/test_mdtab.py`
  - `tracker/items/WI-0002/item.md` (criteria and their tick state), `history.md` (eight rows), `journal.md` **in full** (ten entries), `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`, `questions/Q-001.md` including its `## Consequences`
  - `tracker/items/WI-0001/item.md` — all eleven criteria, to check `verify`'s AC9 read
  - `docs/product/vision.md`, `docs/architecture/overview.md`, and `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006` — the last two in full, `ADR-0003`'s decision 9 and its `## Corrections` section
  - `mdtab.py` at the branch head, `compose_row` at line 244 and `column_alignments` at line 217
  - `.claude/agile-skills/scripts/lib/claims.py`, `Resolver._resolve` — to establish what a `file:line` citation is actually checked against
- **Decisions:**
  - **Rejected. `in-review` → `in-progress`.** D7 and D12 fail on one root cause: `ADR-0005` describes `compose_row` in the present tense as it was *before* this item changed it. `## Context` says *"Read on its own it says the padding always follows the text, which is what `compose_row` does today"*. At `ef2da0c` `compose_row` splits the padding by the column's marker, so **the sentence is false of the code this item delivers**. It was true when `answer-questions` wrote it; nothing updated it.
  - **Classified as an ordinary repair, not a question to the stakeholder.** The sentence carries a code citation, not a `[src: ITEM/Q-nnn]`; it is the ADR's own description of the code rather than anything the stakeholder said; no decision changes and nothing is superseded. That is row 2 of ADR-0008's table, so `ADR-0008` §3's third row is not reached and no human-addressed question is owed.
  - **Classified as this item's own defect, so a send-back rather than a bug item.** The false sentence is about the behaviour this item delivers, and `implement`'s D12 duty covered it. Its journal recorded the D12 read as done and named `vision.md` line 121 and `ADR-0003`'s `## Corrections` row — both of which I re-checked and both of which are correct — but did not open `ADR-0005`'s own prose, the document most about this behaviour. That is the gap, and it is named in `review.md` so `implement` does not have to guess.
  - **Did not repair it myself**, although it is three sentences. D12 exists for precisely this shape — the spec records a wrong claim reaching seven documents because every skill re-quoted it instead of re-checking it — and a reviewer who writes the fix and then approves it leaves nobody checking it. The ADR also needs a version bump and a change-log row, which is discipline the owning skill applies.
  - **Second finding, same send-back: four `[src: mdtab.py:207]` citations no longer point at `compose_row`.** It was at 207 on `main` and is at 244 now; line 207 is a comment about the alignment constants. `ADR-0005` lines 22, 53 and 133 and `ADR-0003` line 195 all cite it. Three of the four sentences are still **true** and only their pointers rot, which is still a D12 failure: a citation whose job is to let a reader check a claim in one hop now sends them to a comment. `ADR-0003`'s `## Corrections` is append-only, so its repair is a new row, not an edit.
  - **Ruled on the question `impl-report.md` put to this review: no bug item was owed for the ADR-0004 filename correction, and none should be filed now.** A wrong path inside a comment is not delivered *behaviour* — nothing a user runs changes, no criterion of any item covers it, and it cannot carry the reproduction a bug item requires. It was repaired inside a plan step that rewrote those lines, made visible in the plan, the report and the journal rather than folded in, and I verified the repair rather than the claim of it: all three `docs/` paths in `mdtab.__doc__` resolve. A bug at `ready` for a defect that no longer exists would be closeable on sight and would misdescribe the tree. Recorded as a ruling so the next close does not re-litigate it.
  - **Agreed with `verify` that AC3 is a pass despite its second worked example being wrong**, and required the reading be written into `item.md`'s `## Notes` before the close. AC3's *"a centred column of width 3 … one holding `Q` is written `| Q |`"* cannot describe a width-3 column; the arithmetic gives `|  Q  |` and `| Q |` is the width-1 case. It is not an ambiguity, because `ADR-0005` decision 6 keeps the one space either side untouched, so `| Q |` at width 3 is not an available reading of the record. `## Notes` is not an acceptance criterion, so `implement` may write there; the criterion itself is `refine`'s and stays as it is. An accepted reading that lives only in a report is forgotten the moment the item closes.
  - **Accepted six declared gaps**, each because it already lives somewhere that survives the item — not because it sounded minor. Tabulated in `review.md` `## Accepted gaps` with where each survives.
  - **No merge, and no trial merge.** Step 8 is the accept path; the item is rejected at step 7. `git rev-parse main` is unchanged at `b4568fe` because nothing was merged and no worktree was created.
- **Cross-answer check:** none — this execution consumed no new human answer. `Q-001` was consumed by `answer-questions` on 2026-08-29T22:33:17Z and I re-read it only as evidence for `vision.md` line 121, which it supports. The false claim I found is sourced to code, not to an answer, so it is an ordinary repair and `ADR-0008` §3's third row is not reached. No sign-off is in play: `check-epic-signoff` reports WI-0002 is a work-item, not an epic.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → 0, `ef2da0c`; `git rev-parse main` → 0, `b4568fe`, unchanged
  - `git diff main..HEAD -- mdtab.py` and `git diff main..HEAD --stat` → 0, read in full
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → 0, `WI-0002 verified at 867ef751; wi/WI-0002 has moved to ef2da0c7 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 6 commit(s) on main..wi/WI-0002 name WI-0002`
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0002` → 0, `WI-0002 is a 'work-item', not an epic … PASS`
  - `.claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0, and its scope verbatim: **`checked absolute claims: 0 document(s) in 0 path(s) differ from main (b4568fe) under docs; citations: every markdown file in the workspace`**, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0, scope verbatim: **`claim window: 0 path(s) differ from main (b4568fe) under docs`**, `checked 8 consumed human answer(s)`, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/validate-workspace .` → 1 then 0. The first run reported `claim.citation.unresolved: an empty citation` at `review.md:71`, because a blockquote reproducing `[src: mdtab.py:207]` had the path in backticks and the inline-code mask left `[src: ]` behind. Rewritten so the whole marker is the code span, which is the quotation form; then `0 errors, 0 warnings`
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 24 tests` / `OK`; `python3 -m compileall …` → 0
  - `python3 -c "…re.findall(r'docs/\S+\.md', mdtab.__doc__)…"` → 0, all three paths `OK`, verifying the ADR-0004 filename repair
  - `sed -n` over `ADR-0005` lines 18–25, 47–60, 128–140 and `ADR-0003` line 195 → the four `mdtab.py:207` claims read in context
  - `grep -n "^def compose_row" mdtab.py` → 0, `244:`; `git show main:mdtab.py | grep -n "^def compose_row"` → 0, `207:` — the pointer rot demonstrated rather than asserted
- **Gates:**
  - `definition-of-done` → **fail** (D1 pass, D2 pass, D3 pass, D4 pass, D5 pass, D6 pass, **D7 fail**, D8 pass, D9 not reached, D10 pass, D11 pass, **D12 fail**. The full table with per-criterion evidence is `review.md` `## Definition of Done`; D7 and D12 fail on Findings 1 and 2)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the branch moved after verification but only five files under `tracker/`, so the verification still covers the code)
  - `commits-reference-the-item` → **pass** (`all 6 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0)
  - `tests-pass-on-the-merge-result` → **not run** — the item is rejected at step 7, and step 8's trial merge is the accept path. Merging or trial-merging a change that is going back would be wrong, and `main` is deliberately untouched at `b4568fe`. The suite does pass on the branch head (`Ran 24 tests` / `OK`), which is not the same claim and is not offered as one
  - `workspace-valid` → **pass** (`0 errors, 0 warnings`, exit 0, after the `review.md` citation was rewritten)
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep WI-0002` alone: **what was built and why** — `plan.md` `## Problem`/`## Approach` and the four code commits; **which skill decided what** — `ADR-0005` is the stakeholder's, recorded by `answer-questions`, `ADR-0006` is `plan`'s, and the four assumptions are `plan`'s with their reversal costs; **what questions arose and how they were resolved** — `Q-001`, one question, answered by the human, with `## Consequences` naming five files that all exist at the versions it claims; **what verification found** — `verify-report.md`, ten criteria with the commands `verify` ran, fourteen boundary conditions and ten mutations. I could answer all four without asking anyone
  - `claims-are-sourced` → **pass, over a scope that could not have found anything, and that is Finding 3.** Scope quoted verbatim above: `0 document(s) in 0 path(s) differ from main under docs`. The window is empty because this item legitimately changed no file under `docs/` — which is exactly when D12's question is most alive, since the documents that went stale are the ones it did *not* touch. The `epic` context was given a whole-document-set scope for this reason; the `work-item` context still has the hole, so an item that changes only code can never trip the automated half of D12. The human read caught what the gate could not
  - `cross-answer-consistency` → **pass** (exit 0; scope quoted above, also empty for the same reason. The `## Cross-answer check` bullet records why there was nothing for it to find: no human answer was consumed by this execution)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` → `WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS.`). Separately, `engagement-state EP-001` reports `active — still in flight: WI-0002`, so EP-001 is not at rest and nothing about the ending is due
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — new: what was examined, the D1–D12 table, five findings, six accepted gaps, and the three things required to close
  - no merge commit, no bug item, no question filed, and `main` unmoved at `b4568fe`
- **Status:** `in-review` → `in-progress`
- **Result:** WI-0002 is rejected and goes back to `implement`. The change itself is sound — the diff maps hunk for hunk to AC1–AC4 and the plan's steps, the verification is genuinely independent and mutation-checked, and the record answers every reconstruction question — but D7 and D12 fail: `ADR-0005` still says `compose_row` puts the padding after the text, which this item made false, and four `[src: mdtab.py:207]` citations point at a line that no longer holds that function. Three things close it: fix the sentence and bump `ADR-0005` to v2 with a change-log row; repair the four pointers, appending rather than editing in `ADR-0003`'s `## Corrections`; and record the AC3 reading in `item.md`'s `## Notes` so it survives the close. No test needs to change and no criterion needs re-earning, though whether to re-verify is `verify`'s call. Two things this review settled for the record: no bug item was owed for the ADR-0004 filename repair, and the claims gate passed here over a scope that could not have seen anything — a hole in the `work-item` context, not in this item.

## 2026-08-29T23:16:09Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` after `review-close` rejected the item on D7 and D12; dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (nine rows, last one the send-back), `journal.md`, `questions/Q-001.md`
  - `tracker/items/WI-0002/artifacts/review.md` first, per the procedure's send-back rule — its `## Verdict` is the whole of my job this execution
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - `tracker/project.yaml` for the branch prefix, the commit subject and the gate commands
  - `docs/architecture/adr/ADR-0005-alignment-markers-place-cell-text.md` and `ADR-0003-recognition-and-output-shape.md`, the two documents the verdict requires repaired
  - `.claude/agile-skills/spec/doc-header.md` §4b and §5, `spec/question.md` §1 and §2, `spec/dor-dod.md` D7 and D12
  - the branch: `wi/WI-0002` at `c26e1af`, working tree clean, seven commits ahead of `main`
- **Decisions:**
  - **Took the verdict's third repair and no more of it.** `review.md` Findings 4 rules that AC3's second worked example (`| Q |` at `W = 3, w = 1`) describes a width-1 column, that the criterion's arithmetic and `ADR-0005` decision 6 govern, and that the reading must survive the close in `item.md`'s `## Notes`. Written and committed as `e4dd5c6`. The reviewer named `## Notes` as the place `implement` may write, and the criterion's own text is `refine`'s and is untouched.
  - **Did not apply the verdict's first two repairs, and escalated instead — Q-002.** Both are edits to standing ADRs under `docs/`. `spec/doc-header.md` §5 says `implement` does not write to `docs/` and names `answer-questions` as the skill that makes the edit when `implement` finds a document wrong; `spec/question.md` §1 puts `implement` in the same row as `verify` and `review-close`. My own `SKILL.md` §6a routes this exact case — the code changed and the sentence describes the code — to "ordinary repair — fix it". The two disagree about who types it, and the answer decides which skill's name goes in the `by` column of two append-only `## Corrections` sections. Escalated rather than guessed, with a recommendation.
  - **Did not treat this as an impasse.** Option C in `Q-002` — setting the item to `blocked` — was considered and rejected: the repair itself is agreed and specified line by line, no approach has been tried and failed, and an architect can settle it from the record.
  - **Changed no code and no test.** The verdict says the code is not in question and no criterion needs re-earning. The diff since `c26e1af` is one paragraph in `item.md`.
- **Cross-answer check:** none — this execution wrote no file under `docs/`, so it edited no claim sourced to one of the stakeholder's answers. The one file it did write, `item.md`'s `## Notes`, discusses AC3, whose text cites `WI-0002/Q-001`; the note adds a reading alongside the criterion and does not rewrite the criterion or the answer, and `lint-answers --changed-since main` reports 0 errors over 8 consumed human answers.
- **Questions raised:** Q-002, blocking, addressed to the architect.
- **Commands:**
  - `git log --oneline main..wi/WI-0002` → exit 0, seven commits at entry
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`, `OK`
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 8 commit(s) on main..wi/WI-0002 name WI-0002`
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 after the `## Notes` commit; exit 1 once `Q-002` was filed, with `question.blocking.not-suspended`, which this transition is what resolves
  - `git commit` → exit 0, `e4dd5c6`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 24 tests, OK)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0)
  - `workspace-valid` → **pass** on the state this move produces; it fails on the state the move leaves, because an open blocking question with the item at `in-progress` is `question.blocking.not-suspended` by construction
  - `every-criterion-has-a-test` → **pass**, unchanged from `a324868` and not re-earned here: this execution added no criterion and no behaviour. The eleven `test_wi0002_ac<n>_` functions in `tests/test_mdtab.py` stand as `impl-report.md` recorded them
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 8 commits)
  - `no-unplanned-scope` (advisory) → **pass**; the only hunk since `c26e1af` is the `## Notes` paragraph `review.md` Findings 4 asks for
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0), but it examined a window of 0 paths under `docs/`, because this item still changes no file there
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0) with the same empty window — `0 document(s) in 0 path(s) differ from main (b4568fe) under docs`. This is `review.md` Findings 3 reproduced exactly: the gate passed having examined nothing, on the execution whose whole remaining work is a claims repair
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — `## Notes` gains the AC3 reading
  - `tracker/items/WI-0002/questions/Q-002.md` — filed, blocking, addressed to the architect
  - commit `e4dd5c6` on `wi/WI-0002`; branch range `main..wi/WI-0002` now eight commits
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** Closed the third of `review-close`'s three required repairs and suspended on the other two. `Q-002` asks the architect which skill applies an `erratum` and three `provenance` corrections to standing ADRs, because `spec/doc-header.md` §5 forbids `implement` from writing to `docs/` while this skill's own `SKILL.md` §6a instructs the repair. The repairs themselves are not in dispute and are specified in the question so that whoever applies them need not re-derive anything.

## 2026-08-29T23:21:29Z — answer-questions v0.4.0 — architect

- **Item:** WI-0002
- **Trigger:** `awaiting-answer` on `Q-002`, blocking, addressed to the architect; dispatched by `next` at step 4 as the only open architect question in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` (answered) and `Q-002.md` (the open one)
  - `tracker/items/WI-0002/item.md`, `history.md` (fourteen rows; the suspending row carries `resume-to: in-progress`), `journal.md`
  - `tracker/items/WI-0002/artifacts/review.md` — the verdict whose three repairs are the whole of the work — and `plan.md`, `impl-report.md`, `verify-report.md`
  - `docs/architecture/adr/ADR-0005-alignment-markers-place-cell-text.md` v1 and `ADR-0003-recognition-and-output-shape.md` v2, read against `mdtab.py` at the branch head
  - `docs/architecture/adr/ADR-0001` v1, `ADR-0004` and `ADR-0006`, to check that nothing else cites the moved line
  - `.claude/agile-skills/spec/doc-header.md` §3, §4, §4a, §4b and §5; `spec/question.md` §1 and §4; `spec/dor-dod.md` D7 and D12
  - `mdtab.py` — `compose_row` at line 244, `column_widths` ending at line 207
- **Decisions:**
  - **`Q-002` answered A, from an existing document — route 3.1, no ADR written.** `spec/doc-header.md` §5 says `implement` and `verify` do not write to `docs/` and names this skill as the one that makes the edit when either finds a document wrong; `spec/question.md` §1 puts `implement` in the same row as `verify` and `review-close`. The rule carries its rationale — the authoritative record must not be updated by the execution being judged against it — and that rationale is live, because the two sentences at issue *are* WI-0002's D7 and D12 failure. `implement`'s `SKILL.md` §6a classifies the repair (ours, not the stakeholder's) without assigning the typist, so read that way the two documents do not conflict. Nothing here needed deciding, so nothing was recorded as a decision of mine.
  - **Applied `review-close`'s two repairs as written; re-litigated neither.** `ADR-0005` `## Context`'s *"which is what `compose_row` does today"* is past-tensed as an `erratum`; the three `[src: mdtab.py:207]` pointers are replaced with citations that name the function instead of a line. `ADR-0003`'s stale pointer is repaired by a **new** `## Corrections` row, because that section is append-only and the existing row stands.
  - **Recorded the ADR-0005 repairs as two `## Corrections` entries rather than three.** `spec/doc-header.md` §4b requires one change-log row and one version bump per entry, and `validate-workspace` enforces the count (`adr.correction.changelog`). One `erratum` for the false clause and one `provenance` entry quoting each citation site keeps the evidence intact without minting a version per sentence. `ADR-0005` → `version: 3`, `ADR-0003` → `version: 3`.
  - **Repaired four pre-existing `claim.unsourced` errors that editing the ADRs exposed.** Touching the two documents pulled them into `lint-claims --changed-since main`, which had been examining an empty window (`review.md` Findings 3), and it immediately failed on three `ADR-0003` `## Context` absolutes and one in `ADR-0005` — none of them mine, all of them true, each needing only the citation the sentence already names in prose. Left alone they would have blocked `implement`'s `claims-are-sourced` gate on resume, and `implement` may not fix them. `doc-header.md` §4a puts the obligation on the next execution that edits the document, and F-067 is this exact shape, so they are `provenance` corrections in the same pass.
  - **Did not escalate to the human, and did not file a bug.** None of `spec/question.md` §4's four conditions applies: no intent is missing, nothing is irreversible, no ADR is contradicted, and the record is not silent. No delivered behaviour is wrong — `mdtab.py` is untouched by this execution and the suite is green.
  - **Returned the item to `in-progress`**, read from the `resume-to` column of the row that suspended it, not inferred from which skill asked.
- **Cross-answer check:** Checked against: `WI-0001/Q-003`; `WI-0002/Q-001`; `WI-0001/Q-004`. No human answer was consumed by this execution — `Q-002` is an architect question answered from the spec — so this bullet reports what the edits were checked against instead.
  - `WI-0001/Q-003` — **compatible**, and named here because `lint-answers --changed-since main` flags it: the `ADR-0005` `## Consequences` *"Hard"* paragraph carries `[src: WI-0001/Q-003]` for the stakeholder's *"the size of the first diff is not a concern"*, and this execution changed a different sentence in that paragraph — the `compose_row` code pointer. Their sentence, its meaning and its citation are all untouched, and nothing they have since said bears on it. This is `ADR-0008` §3's first row: a citation repair, not a claim overtaken by a later answer.
  - `WI-0002/Q-001` — compatible: the erratum is about what `compose_row` did before this item, not about where the marker puts the text. Their *"every row, every column, no exceptions"* and the odd-remainder rule are quoted verbatim in `## Context` and are unchanged, as are decisions 1 to 6.
  - `WI-0001/Q-004` — compatible: newly cited in `ADR-0003` for *"the delimiter row carries no content"*, which is what they said of it — *"a rule under the header, not a row of content"*. The citation is added to a sentence that already named the question in prose; the assertion is unchanged.
- **Questions raised:** none — `Q-002` was answered from the record, and nothing was re-addressed to the human.
- **Commands:**
  - `sed -n` over `mdtab.py` to read `compose_row` (line 244) and what line 207 now holds (the last line of `column_widths`) → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 twice while the edits were in flight (`adr.correction.changelog`, then `question.awaiting.none-open` with the board stale), exit 0 once the change-log rows matched the corrections
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 on four `claim.unsourced` errors, then exit 0 after they were sourced; window `2 document(s) in 2 path(s)`
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 1, one remaining error at `ADR-0001:58`, outside this item's window and untouched here
  - `.claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, `checked 1 consumed human answer(s)`
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → exit 1, `answer.claim-rewritten-unasked` on `ADR-0005:132` for `WI-0001/Q-003`, which the `**Cross-answer check:**` bullet above is the sanctioned response to
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in `Q-002`'s `## Consequences` was reopened: `ADR-0005` carries the past-tensed clause at `## Context`, `[src: WI-0001 AC3]` and `[src: mdtab.py]` where the stale pointers were, `version: 3`, two new change-log rows and a `## Corrections` section with two entries; `ADR-0003` carries the new append-only row, three sourced absolutes, `version: 3` and one new change-log row; `item.md` is back at `in-progress` by this transition
  - `answered-from-the-record` → **pass**. `Q-002` follows from `spec/doc-header.md` §5 and `spec/question.md` §1, both quoted in `## Answer`. The record was not silent, so no ADR was written
  - `escalation-is-justified` → **skipped** — nothing was escalated to the human, so no condition had to be named
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` → exit 0). The `--changed-since main` scope reports `answer.claim-rewritten-unasked` on `ADR-0005:132`; `ADR-0008` §3 offers two responses and this execution took the first, the `**Cross-answer check:**` bullet above naming `WI-0001/Q-003` and stating why the edit is compatible
  - `workspace-valid` → **pass** on the state this move produces (`validate-workspace` → exit 0 immediately before the transition; the two errors outstanding at this instant, `question.awaiting.none-open` and the stale board, are what the move itself resolves)
  - `item-resumed-correctly` → **pass**. The suspending row of 2026-08-29T23:16:09Z carries `resume-to: in-progress`; this move goes to `in-progress`
  - `a-deferral-is-not-an-answer` → **not applicable**. No reply deferred anything: `Q-002` is an architect question answered in full from the spec, and no question on this item is at `deferred`
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-002.md` — `## Answer` and `## Consequences` written, `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-29T23:17:37Z`
  - `docs/architecture/adr/ADR-0005-alignment-markers-place-cell-text.md` — v1 → v3; one erratum, three citations repaired, one absolute sourced, `## Corrections` created
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` — v2 → v3; one new append-only correction row, three absolutes sourced
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md` — the resume and this entry
  - no code, no test and no acceptance criterion was touched; `mdtab.py` and `tests/` are byte-identical to `e4dd5c6`
- **Status:** `awaiting-answer` → `in-progress`
- **Result:** `Q-002` is answered A from `spec/doc-header.md` §5: this skill, not `implement`, writes to `docs/`, and both of `review-close`'s ADR repairs are now applied — the false `compose_row` clause past-tensed as an erratum, and every `mdtab.py:207` pointer replaced with a citation that names the function. Four pre-existing unsourced absolutes that the edit exposed were sourced in the same pass, because `implement` could not have fixed them and its `claims-are-sourced` gate would have failed on them. WI-0002 resumes at `in-progress` with nothing left to write under `docs/`.

## 2026-08-29T23:24:01Z — implement v0.3.0 — developer

- **Item:** WI-0002
- **Trigger:** `in-progress` after `answer-questions` resumed the item on `Q-002`; dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0002/artifacts/review.md` — the send-back verdict, read first, as the procedure requires; its three numbered repairs are the whole of the job
  - `tracker/items/WI-0002/questions/Q-002.md`, now answered, and its `## Consequences`
  - `tracker/items/WI-0002/item.md`, `history.md` (fifteen rows), `journal.md` including `answer-questions`' entry of 23:21:29Z, `plan.md`, `impl-report.md`, `verify-report.md`
  - `docs/architecture/adr/ADR-0005` at v3 and `ADR-0003` at v3 — the repaired artifacts, not the answer file, per the procedure's rule that the artifacts are authoritative
  - `mdtab.py`, `compose_row` at line 244, read against the repaired sentences
  - `tracker/project.yaml` for the gate commands
- **Decisions:**
  - **Re-read the two ADRs rather than trusting `Q-002`'s answer.** `ADR-0005` `## Context` now says `compose_row` *"did when this ADR was written, before WI-0002 changed it"* — true, the ADR is stamped 22:29:29Z and the behaviour changed in `c64f374`. `## Consequences`' *"a reader who checks `compose_row` ... will conclude the code is right when it is now incomplete"* cites `[src: mdtab.py]` and is true of line 244. `ADR-0003`'s stale row is untouched and a new append-only row carries the replacement pointer, which is what the verdict asked for.
  - **Confirmed no `[src: mdtab.py:207]` citation survives outside a quotation.** `grep -rn "mdtab.py:" docs/` returns five hits: three are inside code spans in `## Corrections` entries, where quoting the stale marker verbatim is what §4b requires as evidence; one is the pre-existing `ADR-0003` correction row that is append-only and may not be edited; and the fifth is a change-log row describing the repair. None is a live claim pointing at a line that has moved.
  - **Did not re-verify and did not touch a criterion.** No behaviour moved, so nothing is re-earned. `check-verify-freshness WI-0002 wi/WI-0002` → exit 0, *"only the record changed (9 file(s) under tracker/ or docs/), so the verification still covers the code"*. Whether to re-run verification is `verify`'s call; the verdict declined to pre-authorise it.
  - **Did not repair `ADR-0001:58`**, the one remaining `lint-claims --all` error. It is outside this item's window and outside D12's scope, and fixing it would be the unrelated tidying this skill is told not to do. Recorded in `impl-report.md` `## What I did not do` so it is visible at the epic close, where `--context epic` will see it.
  - **Filed no bug item and no question.** `review.md` Findings 5 already settled the `ADR-0004` filename ruling; `Q-002` is answered; nothing in the repaired documents contradicts a criterion or an ADR.
- **Cross-answer check:** none — this execution wrote no file under `docs/`, so it edited no claim sourced to one of the stakeholder's answers. The `WI-0001/Q-003` compatibility finding that `lint-answers --changed-since main` raised belongs to `answer-questions`' entry of 23:21:29Z, which made the edit; re-asserting it here would claim a check this execution did not perform. `lint-answers --changed-since main` exits 0 on the branch head.
- **Questions raised:** none this execution. `Q-002` was filed by the previous `implement` execution at 23:16:09Z and is answered.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests in 4.662s`, `OK`
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 10 commit(s) on main..wi/WI-0002 name WI-0002`
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, `3 item(s), 8 document(s)`, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, window `2 document(s) in 2 path(s)`
  - `.claude/agile-skills/scripts/lint-claims --all` → exit 1, one error at `ADR-0001:58`, outside this item's window and deliberately not repaired
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0
  - `git diff --stat c26e1af..HEAD` → seven files, none under `mdtab.py` or `tests/`
  - `git commit` → exit 0, `a911c83`
- **Gates:** all eight run on the branch head `a911c83`, after the last change.
  - `tests-pass` → **pass** (exit 0, 24 tests, OK)
  - `lint-clean` → **pass** (exit 0)
  - `workspace-valid` → **pass** (exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass**, unchanged from `a324868` and not re-earned: this execution added no criterion and no behaviour. `impl-report.md` `## Acceptance criteria evidence` names the eleven `test_wi0002_ac<n>_` functions, none edited since
  - `commits-reference-the-item` → **pass** (`all 10 commit(s)`)
  - `no-unplanned-scope` (advisory) → **pass**. Every file in `git diff c26e1af..HEAD` traces to a numbered item of `review.md`'s verdict or to the escalation it required; `mdtab.py` and `tests/` are byte-identical to `a324868`
  - `cross-answer-consistency` → **pass** (exit 0)
  - `claims-are-sourced` → **pass** (exit 0) — and this time over a **non-empty** window of two documents, unlike the run `review.md` Findings 3 reports. The window is non-empty precisely because the item finally changed something under `docs/`, which is what exposed the four pre-existing unsourced absolutes `answer-questions` then repaired
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` — new section `## The send-back from review-close, and what closed it`: the three repairs and who made each, why 1 and 2 went to `answer-questions`, the four extra unsourced absolutes, the eight gates on the head, and four declared omissions. Everything above that section is unchanged
  - commit `a911c83` on `wi/WI-0002`; the branch is ten commits on `main..wi/WI-0002`, of which this execution and the previous one added `e4dd5c6`, `d9378cb`, `8c58ac1` and `a911c83`
  - no code, no test, no fixture and no acceptance criterion was written by this execution
- **Status:** `in-progress` → `verifying`
- **Result:** All three of `review-close`'s required repairs are done — two by `answer-questions` under `Q-002`, the third by this skill in `e4dd5c6` — and all eight gates pass on the branch head with the claims gate finally examining a non-empty window. `ADR-0005` is at v3 with the false `compose_row` clause past-tensed as an erratum, `ADR-0003` at v3 with an appended correction row, and no live citation anywhere in `docs/` points at a line `compose_row` has left. Back to `verifying`.

## 2026-08-29T23:34:38Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying` — `next` dispatched `verify` as the status owner, the only runnable candidate (EP-001 and WI-0001 have `owner: null`; no question is open). This is the item's **second** verification: the first passed at `867ef75`, `review-close` rejected on D7/D12, and `implement` returned it to `verifying` at `e533928` after the ADR repairs.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the ten acceptance criteria, read before the implementation report
  - `tracker/items/WI-0001/item.md` — WI-0001's eleven criteria, which AC9 requires be re-read by ID
  - `tracker/items/WI-0002/history.md` — why the item is at `verifying` a second time
  - `tracker/items/WI-0002/artifacts/plan.md` — to read the diff against it
  - `tracker/items/WI-0002/artifacts/impl-report.md` — the claimed evidence, checked rather than trusted
  - `tracker/items/WI-0002/artifacts/review.md` and `questions/Q-002.md` — what the send-back required
  - `tracker/project.yaml` — the gate commands
  - the code at branch head `e533928e704deb8f7a67a0f5c90e688412971158`: `mdtab.py`, `tests/test_mdtab.py`, all 30 files under `tests/fixtures/`
- **Decisions:**
  - **Re-verified from scratch rather than citing the first report.** `git diff a324868..e533928 -- mdtab.py tests/` is empty, so the code is byte-identical to what `867ef75` was verified against, and citing that report would have been cheap. It would also have made this a second opinion about the same claim, which is the failure this skill exists to prevent. Every verdict rests on a command run in this session.
  - **AC9's three non-intersections are waived by ID, not papered over.** Nothing executable in the committed suite exercises WI-0001 AC5, AC7 or AC8 together with a marked column — their fixtures (`indented.md`, `indent_mismatch.md`, `blockquote.md`, `fenced.md`, `malformed.md`) are all unmarked. I stated that in those words, ran covering cases by hand for all three (all passed), and waived adding committed regression tests, citing WI-0002's `## Out of scope` and `item.md`'s R10 table, which record those crossings as deliberately unconstrained by this item. What the waiver costs — no regression cover for a *future* change — is written in `## Not verified, and why`.
  - **WI-0001 AC1 and AC2 are not gaps.** Their own tests use the unmarked `wide_chars.md`, but `test_wi0002_ac6_…` asserts both of their sentences against the marked `aligned_wide.md`. Recorded so the distinction is visible rather than inferred.
  - **WI-0001 AC3 recorded as narrowed, not failed.** Its "padding follows the text" clause now holds only for a markerless column; AC4 of this item is where that case is asserted and ADR-0005 governs the marked case. WI-0001's criteria were not edited. Its "empty cell is two spaces" sub-clause is narrowed by ADR-0004's two-colon minimum, which I traced to commit `ac16080` — WI-0001-era, so not something this item changed.
  - **WI-0001 AC6's crossing classified as vacuous, not uncovered.** A marker lives in a delimiter row and a delimiter row only exists inside a table, so "input containing no table" and "a marked column" cannot intersect. I additionally ran the stronger case AC6 does not ask for — CRLF, no-final-newline and non-UTF-8 bytes inside a *marked* table — and all three round-trip.
  - **My own AC7 harness was wrong before the filter was.** It first reported a violation on the all-empty `:---:` column because it computed `W` without ADR-0004's minimum of 1. The criteria preamble defines `W` with that minimum. I corrected the harness rather than the verdict, and recorded both passes in the report.
  - **Two observations filed as observations, not defects.** `plan.md` step 2's "Afterwards" line repeats AC3's width-3/width-1 illustration error, and `impl-report.md`'s opening line names a three-commit range on a twelve-commit branch. No criterion depends on either; `item.md`'s `## Notes` already records AC3's reading. Left for `review-close` to weigh.
  - No criterion was judged `ambiguous`. AC3's second worked example is the one that could have been: `item.md`'s `## Notes` settles it, so I ran both parities and passed AC3 on the arithmetic the criterion states.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (`checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings`)
  - `python3 -m unittest discover -s tests -t .` → 0 (`Ran 24 tests in 4.719s`, `OK`)
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → 0 (no output)
  - `git status --porcelain` → 0 (empty; clean tree at branch head)
  - `git rev-parse HEAD` → 0 (`e533928e704deb8f7a67a0f5c90e688412971158`)
  - `git diff a324868..e533928 -- mdtab.py tests/` → 0 (empty: no code or test changed since the first verification)
  - `git diff main...wi/WI-0002 -- tests/fixtures/ragged.expected.md` → 0 (empty: WI-0001's expected output is untouched, which is AC4's evidence)
  - `git diff main...wi/WI-0002 -- mdtab.py` / `-- docs/` / `--stat` → 0 (the diff read against `plan.md`)
  - `git log --oneline --diff-filter=A -- docs/architecture/adr/ADR-0004-*.md` → 0 (`ac16080`, under WI-0001 — dating the two-colon minimum)
  - ten filter runs, one per AC1–AC7 input, via `printf … | python3 mdtab.py | cat -A` → 0 each
  - a Python harness asserting AC7's colon-for-colon identity and AC8's idempotence over all ten inputs → 0 (`AC7 violations: none`; `idempotent=True` ×10)
  - a Python harness measuring per-line display width and per-pipe display offset on a marked wide/emoji/NFD-combining table → 0 (all lines width 20; offsets `[0, 7, 13, 19]` on all four rows)
  - a Python harness measuring per-column text start/end display offsets across header and body → 0 (left column starts `{2}`, right column ends `{14}`)
  - 21 negative and boundary runs (empty input, non-UTF-8 in and out of a table, CRLF, no final newline, empty cells, all-empty marked columns, both centring parities, blockquote, mismatched indent, ragged block, non-delimiter second row, `|::|::|`, fenced block, escaped pipe, tab-padded cells, header-only table, single-column `:-`/`-:`/`:-:`, over-long delimiter row) → 0 each, all idempotent
  - a 30-file sweep of `tests/fixtures/` through the filter and its own output → 0 each, `idem=True` each
  - seven mutations of `mdtab.py`, each with `python3 -m unittest discover -s tests -t .` and each reverted → 1 each (all caught), file restored byte-for-byte and `git status --porcelain` empty afterwards
  - `grep -n 'def test' tests/test_mdtab.py` → 0 (24 methods; one per WI-0001 AC1–AC11 and per WI-0002 AC1–AC10)
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → `Ran 24 tests`, `OK`, exit 0, run by this skill on the branch head)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0, no output)
  - `workspace-valid` → **pass** (`validate-workspace` → 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (all ten AC rows in `verify-report.md` name a command this skill ran and quote its actual output; `impl-report.md` is cited nowhere as evidence)
  - `negative-cases-exercised` → **pass** (21 boundary and error cases triggered and tabulated, each with its result)
  - `a-criterion-about-criteria-is-read` → **pass** (AC9: all eleven WI-0001 criteria named by ID with a per-criterion verdict read from their own text; three non-intersections stated in those words; covering cases run; committed tests waived by ID with reasons)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (seven mutations, each caught by the named test of at least one criterion; the two insensitive tests identified and explained as coverage assertions)
  - `commands.build` → **skipped** (null in `tracker/project.yaml`; recorded in `## Not verified, and why`, and nothing is left unchecked by it — the deliverable is a single uncompiled script)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — rewritten for this verification, superseding the `867ef75` report
  - `tracker/items/WI-0002/item.md` — all ten criteria remain ticked; each tick is re-earned by a command in this run, and none was ticked without evidence
  - no bug item filed, no question filed
  - commit of the workspace files this execution wrote
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 passes all ten acceptance criteria at `e533928`, on evidence gathered in this session rather than carried over from the first verification. Seven mutations confirm the suite is sensitive to every behaviour AC1–AC8 describe, 21 boundary cases were triggered, and WI-0001's eleven criteria were re-read by ID with one narrowing (AC3) and three non-intersections named and waived. Two non-blocking observations are left for `review-close`.

## 2026-08-29T23:41:41Z — review-close v0.6.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review` — `next` dispatched `review-close` as the status owner, the only runnable candidate. This is the **second** review of the item; the first, at `23:09:49Z`, rejected it on D7 and D12.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the ten criteria, their tick state, and the `## Notes`
  - `tracker/items/WI-0002/history.md` — 13 rows, chaining `— → draft → … → in-review`
  - `tracker/items/WI-0002/journal.md` — all 15 entries, `21:15:02Z` through `23:34:38Z`, read in full
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md` (both executions' sections), `verify-report.md` (the second verification), and the previous `review.md`
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md`
  - `tracker/items/WI-0001/item.md` — the eleven criteria AC9 re-reads
  - the diff `main..wi/WI-0002` (`b4568fe..57e10f0`, 19 files), read hunk by hunk
  - `mdtab.py` at lines 190, 207, 220 and 244; `tests/test_mdtab.py`; the fixtures the audit needed
  - `docs/architecture/adr/` — ADR-0003, ADR-0004, ADR-0005, ADR-0006; `docs/product/vision.md` line 121
  - `spec/dor-dod.md` §3, `spec/doc-header.md` §4b and §5
- **Decisions:**
  - **Accepted the item.** All twelve Definition of Done criteria pass with their own evidence, recorded per criterion in `review.md` rather than as one verdict.
  - **D12 found one false claim, and I repaired it here rather than sending the item back.** `ADR-0003` decision 9 said *"An empty cell is written as two spaces."* Read against `compose_row`, an empty cell is written as `width + 2` spaces; two is only the zero-width case. Demonstrated: a width-3 column gives five spaces, and an all-empty `:---:` column gives three, because ADR-0004 decision 2 raises its width to 1 — which is exactly the case WI-0002 AC5 covers, and why this item's audit is where it surfaced. **The clause predates WI-0002** (it was equally false under WI-0001, and `git log --diff-filter=A` dates ADR-0004 to `ac16080`, a WI-0001 commit), so it is not a defect in this item's delivery and a send-back would return WI-0002 to `in-progress` for a sentence it did not write and that `spec/doc-header.md` §5 forbids `implement` from fixing — the `Q-002` loop this item already paid four executions for. `§5` does not list `review-close` among the skills barred from `docs/`, and `§4b`'s worked example shows `review-close` in the `by` column of a `## Corrections` row, so I applied it as an `erratum`: `ADR-0003` v3 → v4, removed text quoted verbatim, change-log row, append-only correction. `§4b`'s non-negotiable condition holds — no code would change to satisfy the new text. Both lints re-run green afterwards.
  - **No bug item filed for the finding.** There is no code to fix and no item under EP-001 it belongs to; `§4b` exists so that a documentation erratum does not become a work item. The repair is attributable in an append-only ledger with this skill's name on it.
  - **Confirmed no bug item was owed for the ADR-0004 filename correction**, which `impl-report.md` Deviations 2 explicitly asks a reviewer to rule on. Plan step 4 rewrote those exact lines for a required reason; the correction changes no behaviour and no criterion. I re-reached this rather than inheriting the first review's conclusion.
  - **Accepted `verify`'s waiver of three committed regression tests** (WI-0001 AC5, AC7, AC8 against a marked column). The non-intersection is stated in those words, all three were exercised by hand and passed, and the code makes marker handling structurally unreachable in each path. The cost — no regression cover for a future change — is written in `verify-report.md` `## Not verified, and why`, which survives the close.
  - **Left `plan.md`'s and `impl-report.md`'s two stale lines uncorrected.** Both are item artifacts recording what a past execution believed; neither is a standing document a reader acts on, and `item.md`'s `## Notes` carries the authoritative AC3 reading. Editing a superseded report damages the record more than it repairs.
  - **Named `ADR-0001:58`'s unsourced absolute as the one accepted gap whose home is a future execution** — the epic close, where `--context epic` will see it and F-066 will not let it pass silently.
  - **Merge decision:** merge, after closing. The order is forced: `check-commit-refs` inspects `main..branch`, which merging first would empty.
  - **Epic decision:** none this execution. `engagement-state EP-001` reports `active` — *"still in flight: WI-0002"* — because the item is still open at the moment the gate runs. Closing it puts the engagement at rest, and `next` will dispatch `review-close` on EP-001 for the ending. I did not pre-empt that: step 6 belongs to the orchestrator, and deciding from the board that the engagement looks finished is the failure F-045 records.
- **Cross-answer check:** This execution consumed no new human answer — no question was answered into it, and the two on this item (`Q-001`, `Q-002`) were consumed by `answer-questions` before it. The one stakeholder answer my D12 repair sits near is `WI-0001/Q-003` (*"one space between the pipe and the text on each side of every cell"*), checked against the corrected `ADR-0003` decision 9: the erratum changes only the count of spaces an **empty** cell occupies, from a false absolute to `width + 2`, and leaves the one-space-either-side rule and its citation untouched — the two are compatible, and `lint-answers --context work-item --changed-since main` exits 0 over a 2-path window confirming no consumed answer was rewritten unasked. I also re-read `WI-0002/Q-001` (*"every row, every column, no exceptions"*) against `ADR-0005` decision 3 and `emit_block`, and against `WI-0001/Q-004` (*"a rule under the header, not a row of content"*) which scopes it away from the delimiter row: no contradiction, and the scoping is recorded in `ADR-0005` decision 5 rather than harmonised silently.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → 0 (*"verified at e533928e; wi/WI-0002 has moved to 57e10f0f but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0 (*"all 13 commit(s) on main..wi/WI-0002 name WI-0002"*)
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → 0 (*"WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."*)
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → 0 (`EP-001 active`; *"still in flight: WI-0002"*)
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0, before and after the erratum, over *"2 document(s) in 2 path(s) differ from main (b4568fe) under docs"*
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0 (*"claim window: 2 path(s)"*; *"checked 8 consumed human answer(s)"*), before and after the erratum
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (`3 item(s), 8 document(s)`, `0 errors, 0 warnings`), before and after the erratum
  - `git rev-parse main` → 0 (`b4568fe8dc04edaae26dd72e106f22e288ed998b`), run before and after the trial
  - `git worktree add --detach .trial main` → 0 (`Preparing worktree (detached HEAD b4568fe)`)
  - `git -C .trial merge --no-ff wi/WI-0002` → 0 (trial head `96fd4773f7fc0655a74370cee34ed563479ca7b5`)
  - `python3 -m unittest discover -s tests -t .` **inside the trial worktree** → 0 (`Ran 24 tests in 4.725s`, `OK`)
  - `git worktree remove --force .trial` → 0
  - `git diff a324868..e533928 -- mdtab.py tests/` → 0 (empty: no code or test changed between the two verifications)
  - `git diff main...wi/WI-0002 --stat` and `-- mdtab.py` / `-- docs/` → 0 (the hunk-by-hunk read)
  - `grep -n 'def compose_row\|def column_widths' mdtab.py` → 0 (190, 244); `sed -n '207p' mdtab.py` → 0 (`    return widths`)
  - `grep -rn 'mdtab\.py:[0-9]' docs/` → 0 (four hits, all inside `## Corrections` rows quoting the pointer they repair)
  - `printf '| L | R |\n|---|---|\n| aaa | bbb |\n|  |  |\n' | python3 mdtab.py` → 0 (last row `|     |     |` — five spaces)
  - `printf '|  |\n|:---|\n|  |\n' | python3 mdtab.py` → 0 (last row `|  |` — two spaces, W=0)
  - `printf '|  |\n|:---:|\n|  |\n' | python3 mdtab.py` → 0 (last row `|   |` — three spaces, W=1)
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each recorded with its own result and evidence in `review.md` `## Definition of Done`; D12 passes on the repaired state, with the finding and the repair both named)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0, output quoted above; confirmed independently by the empty `a324868..e533928` code diff rather than assumed)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 13 commits)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 24 tests`, `OK`, exit 0, run **inside the detached trial worktree** at `96fd477`, not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, re-run after the erratum)
  - `record-is-reconstructible` → **pass** (from tracker, docs and `git log --grep WI-0002` alone: *what was built* — `plan.md` and the `mdtab.py` diff; *which skill decided what* — ADR-0005 by `answer-questions` for the remainder, ADR-0006 by `plan` for test naming, the doc repairs by `answer-questions` under `Q-002`, this erratum by `review-close`; *what questions arose and how they resolved* — `Q-001` to the stakeholder on the odd remainder, `Q-002` to the architect on who repairs a document, both `answered` with `## Consequences` naming real files; *what verification found* — two `verify-report.md` executions, the second superseding the first with its own commands)
  - `claims-are-sourced` → **pass** — **scope examined, quoted from the gate:** *"checked absolute claims: 2 document(s) in 2 path(s) differ from main (b4568fe) under docs; citations: every markdown file in the workspace"*. A non-empty window, which is what let the audit mean something (F-066)
  - `cross-answer-consistency` → **pass** — scope quoted: *"claim window: 2 path(s) differ from main (b4568fe) under docs"*, *"checked 8 consumed human answer(s) in the workspace"*, 0 errors
  - `epic-sign-off` → **pass** (`check-epic-signoff WI-0002` exit 0 — not an epic, so the termination gate does not apply to this close)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — rewritten for this review, with `## What I examined` first
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`
  - `docs/architecture/adr/ADR-0003-recognition-and-output-shape.md` — v3 → v4: decision 9's empty-cell clause corrected, one `## Change log` row, one append-only `## Corrections` erratum quoting the removed text verbatim
  - the merge of `wi/WI-0002` into `main`, made immediately after this close
  - no bug item filed, no question filed
- **Status:** `in-review` → `done`
- **Result:** WI-0002 accepted and closed as `delivered`. All twelve Definition of Done criteria pass with per-criterion evidence, the diff was read hunk by hunk with every hunk tracing to a criterion or a plan step, and the suite is green on the merge result rather than only on the branch. The D12 audit found one genuinely false claim in a standing ADR — `ADR-0003` decision 9's *"An empty cell is written as two spaces"* — which predates this item and is repaired here as an erratum rather than routed through a send-back the item did not earn.
