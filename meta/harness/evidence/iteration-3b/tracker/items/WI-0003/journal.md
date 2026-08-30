# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-29T23:54:48Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** created by `answer-questions` while consuming the stakeholder's reply to `EP-001/Q-004`; the answer implied work no item recorded (SKILL §3b)
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-004.md` — the sign-off reply this item exists because of
  - `tracker/items/WI-0002/questions/Q-001.md` — the earlier answer it contradicts
  - `tracker/items/EP-001/item.md` — the epic's goal, success measures and scope
  - `docs/architecture/adr/ADR-0003-...md`, `ADR-0004-...md`, `ADR-0005-...md` — what is already settled about cell shape, the delimiter row and marker placement, so refinement does not re-ask it
- **Decisions:**
  - **Filed as a `work-item` at `draft`, not as a bug.** The delivered behaviour matches every criterion WI-0002 was verified against; what changed is what the stakeholder wants, and a new requirement is a work item.
  - **Not folded into WI-0002 as an amended criterion.** WI-0002 is `done`; widening a closed item to swallow new work hides the change from the board and from the person who asked for it (SKILL §3b).
  - **`## Notes` records the contingency loudly rather than quietly.** The item's scope depends on `EP-001/Q-005`, and the note says in as many words that if the earlier sentence wins, this item is dropped and nothing here is to be refined, planned or built first.
  - **The provisional AC1 is labelled as such.** A draft item needs at least one criterion by `spec/work-item.md` §2, and one that pretends to be Ready would be worse than none; the body says plainly that `refine` must replace it, and lists the five things it must ask.
- **Cross-answer check:** none — this entry consumes no human answer of its own. The check on the answer that produced this item is on `EP-001`'s journal and in `tracker/items/EP-001/questions/Q-004.md`.
- **Questions raised:** none on this item. The blocking question its scope depends on is `EP-001/Q-005`, filed on the epic because the contradiction is between two engagement-level answers.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0003 --type work-item --title "Leave a cell containing a line break at the left of its column" --epic EP-001 --priority high --status draft --actor answer-questions --arose-from EP-001/Q-004 --reason "..."` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass** — this item is itself one of the consequences `EP-001/Q-004` names, and it exists with the frontmatter and body the schema requires
  - `answered-from-the-record` → **skipped** — no question was answered on this item; it was created by an answer on another
  - `escalation-is-justified` → **skipped** — no question was escalated on this item
  - `cross-answer-consistency` → **pass** — `lint-answers` exit 0 over the whole workspace, which includes this item
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0
  - `item-resumed-correctly` → **skipped** — a creation, not a resumption; the `from: null → draft, actor: answer-questions` row in `pipeline.yaml` forbids `resume-to` here and `new-item` enforced it
  - `a-deferral-is-not-an-answer` → **skipped** — nothing was deferred
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — story, one provisional criterion marked as such, four out-of-scope bullets, and `## Notes` carrying the stakeholder's words verbatim, the contingency on `EP-001/Q-005`, the five questions `refine` must ask, and what is already settled and must not be re-asked
  - `tracker/items/WI-0003/history.md` — the creation row
- **Status:** `—` → `draft`
- **Result:** WI-0003 exists at `draft` to record the one thing the stakeholder said was missing at sign-off. It is deliberately not Ready and deliberately not startable: its scope hangs on `EP-001/Q-005`, and its notes say what to ask and what never to re-ask.

## 2026-08-30T00:04:11Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** no status change on this item; `EP-001` was at `awaiting-answer` and this execution consumed the human's answer to `EP-001/Q-005`, whose consequence lands here
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` (the human's answer)
  - `tracker/items/EP-001/questions/Q-004.md` (the sign-off reply this item arose from)
  - `tracker/items/WI-0003/item.md`
  - `tracker/items/WI-0003/history.md`
  - `docs/architecture/adr/ADR-0005-alignment-markers-place-cell-text.md` (v3, now v4)
  - `docs/product/vision.md` (v5, now v6)
- **Decisions:**
  - Lifted this item's contingency rather than closing or re-scoping it. The stakeholder answered option B of `EP-001/Q-005` — *"the later one wins … treat this as me superseding what I said before"* — which is the condition `## Notes` recorded for keeping the item. Under option A it would have been dropped; it was not.
  - Left the five questions in `## Notes` exactly as they were, and only removed the words *"assuming the answer is that the later sentence wins"* from the heading over them. The answer authorised the exemption, not its edges, so the questions `refine` must put to the stakeholder are unchanged in substance and none of them may be guessed.
  - Left AC1 provisional and did not amend it. The item is at `draft`; criteria here are `refine`'s to write with the stakeholder, and AC1 as it stands presumes an answer to one of the five questions (whether an exempt cell is still padded), which is precisely what must be asked rather than settled.
- **Cross-answer check:** written on `EP-001/Q-005`, where the answer was consumed, and not repeated here. It named `WI-0002/Q-001` (compatible — this answer is the reconciliation of the contradiction that `EP-001/Q-005` itself escalated), `EP-001/Q-004`, `EP-001/Q-001`, `WI-0001/Q-001`, `WI-0001/Q-003` and `WI-0001/Q-004`.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item EP-001` → exit 0, 5 consumed human answers checked, 0 errors
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 at the time of writing, with the two errors the pending transition of `EP-001` clears (`board.stale`, `question.awaiting.none-open`)
- **Gates:**
  - `answer-is-propagated` → **pass** (`item.md` `## Notes` opened and read back: the contingency paragraph is replaced, the answer is quoted verbatim with `[src: EP-001/Q-005]`, and ADR-0007 is cited)
  - `answered-from-the-record` → **pass** (the basis is the stakeholder's own reply in `EP-001/Q-005`, quoted in full)
  - `escalation-is-justified` → **skipped** (this execution escalated nothing)
  - `cross-answer-consistency` → **pass** (`lint-answers --item EP-001`, exit 0)
  - `workspace-valid` → **pass** on this item's files; the workspace-level run is recorded on `EP-001`'s entry, where the transition that clears its two errors is made
  - `item-resumed-correctly` → **not applicable** — this item was never suspended and does not move; it stays at `draft` for `refine`
  - `a-deferral-is-not-an-answer` → **skipped** (the reply is an answer, not a deferral: it chooses option B by name and authorises the supersession)
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — `## Notes` contingency lifted, the answer quoted, ADR-0007 cited, the `refine` heading no longer conditional; `updated` restamped
- **Status:** `draft` → `draft` (unchanged)
- **Result:** WI-0003 is authorised and no longer contingent on EP-001/Q-005. It stays at `draft`; `refine` is what makes it Ready, and it must put the five questions in `## Notes` to the stakeholder before anything is planned or built.

## 2026-08-30T00:09:05Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — the only runnable candidate in the workspace
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md`, `journal.md` (both entries: the creation by `answer-questions`, and the lifting of the contingency)
  - `tracker/items/WI-0003/artifacts/` — empty on entry; no prior `refinement-qa.md`
  - `tracker/items/EP-001/questions/Q-004.md` and `Q-005.md` — the two stakeholder replies this item is made of
  - `tracker/items/WI-0002/questions/Q-001.md`; `tracker/items/WI-0001/questions/Q-001.md`, `Q-003.md`, `Q-004.md`; `tracker/items/EP-001/questions/Q-001.md`, `Q-003.md`
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/artifacts/refinement-qa.md` — for the criterion style this engagement uses and for what the earlier rounds already settled
  - `docs/product/vision.md` (v6); `docs/architecture/adr/ADR-0007-...` (v1), `ADR-0004-...`, `ADR-0003-...`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/journal-and-history.md`
- **Decisions:**
  - **Did not attempt to reach the stakeholder in this session and did not guess in their place.** They answer asynchronously in files; the precondition for a direct conversation is not met, so the escalation route in `## Failure and escalation` applies — file the questions, suspend at `awaiting-answer` with `resume-to: draft`, stop.
  - **Asked two of the five open questions, not all five.** Step 3's test was applied to each in order and the test that fired is named for each in `artifacts/refinement-qa.md` and in the item's `## Notes`. Routing everything to the stakeholder is the failure F-023 records — *"three of the four were things I'd expect a team to just decide"* — and guessing at what is theirs is the failure that costs more. Both questions asked carry product stake: `Q-001` depends on what they type in their own documents, which no document records; `Q-002` decides what every file they run the tool over looks like, and the record is genuinely silent on it.
  - **Per cell, not per column — answered from their own words, not asked.** *"Markers are for normal cells, not for those"* [src: EP-001/Q-004] and *"markers govern everything else"* [src: EP-001/Q-005] both say the marker keeps applying to the cells that are not exempt. Re-asking would tell them their answer was not heard.
  - **The delimiter row's markers — settled from ADR-0004 decision 1 and ADR-0007 decision 6, not asked.** Neither reply mentions the delimiter row, and a delimiter cell holds no text and can hold no `<br>`, so the exemption cannot reach it. Recorded as an assumption rather than a certainty, because the assumption being made is that they did not mean to reopen a decision they never mentioned.
  - **"Top-left" read as "left" — assumed, and stated in `Q-002` so they can overturn it for free.** A pipe table's cell is one physical line; "top" has no referent and no implementation. Asking would be asking them to explain their own idiom.
  - **Left AC1 exactly as it stands.** It is marked draft and is undecidable twice over — it does not name the set of things that count as a line break, and it presumes the answer to `Q-002` by asserting the cell is padded. Rewriting it now would put our reading of one of their words into a criterion, which is precisely what the two questions exist to avoid. `## Out of scope` is likewise untouched until the answers arrive.
  - **Wrote `refinement-qa.md` with `status: agenda`, deliberately.** The conversation has not happened. R8 reads that field, and writing `recorded` on a file whose two questions are unanswered would let the item reach `ready` on the strength of the file existing.
- **Questions raised:** two, both blocking, both addressed to `human`, presented as one ask — `Q-001` (which written forms of a line break make a cell exempt) and `Q-002` (whether an exempt cell is still padded out to its column's width). Both `[unresolved]`. Recorded in `artifacts/refinement-qa.md` under `## Round 1`.
- **Cross-answer check:** none was due. This execution consumed no human answer — it filed two questions and recorded no new answer — so `spec/question.md` §2's obligation does not arise. The prior answers it *relied on* to close three gaps without asking are named with their IDs in `artifacts/refinement-qa.md`, and each was read for compatibility with the two it is being used alongside: `EP-001/Q-004` and `EP-001/Q-005` agree on per-cell scope; `WI-0001/Q-003` (one space each side) and `EP-001/Q-001` (no trailing whitespace) constrain both open questions without deciding either. `lint-answers --item WI-0003` exit 0.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 on entry; exit 1 after the questions were filed, with `board.stale` and `question.blocking.not-suspended`, both of which this transition clears
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 0 consumed human answers on this item
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0 after this transition; the run before it reported only the two states this move exists to produce)
  - `definition-of-ready` → **fail, and reported rather than worked around.** Criterion by criterion: R1 **pass** (frontmatter complete, `type`/`epic`/`priority` set, validator exit 0). R2 **pass** (story names the role, the capability and the "so that"). R3 **pass** (AC1 exists as a labelled checkbox). R4 **fail** — AC1 names no set of qualifying line-break forms and presumes the answer to `Q-002`; this is what `Q-001` and `Q-002` are for. R5 **pass** on entry (four entries, including "changing a column's width" and "rendering or interpreting the line break"), to be extended when the criteria are rewritten. R6 **fail, deliberately** — two blocking questions are open, which is this round's purpose. R7 **pass** (`depends-on` empty; the item WI-0002 whose function it touches is `done`). R8 **fail** — `refinement-qa.md` is `agenda`, honestly, because the conversation has not happened. R9 **pass** (one exemption, one composing function, one test). R10 **fail** — the exemption crossed with the three markers, the header row, an empty cell, an unmarked column, an indented table and idempotence is not yet stated; most of it falls out of the two answers.
  - `criteria-are-decidable` → **fail**, and the reason is R4's. AC1 cannot be settled by any command: no input can be written that decides "at minimum a literal `<br>`", because "at minimum" names no set. This gate is why the item does not move to `ready`.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003`, exit 0)
  - `qa-recorded-verbatim` → **pass** for what exists. Every question asked is in `refinement-qa.md` and in its own file; no answer is recorded, because none has been given, and the file says so in its first paragraph and in its `status` field. Nothing is paraphrased into agreement and nothing the stakeholder did not say is tagged as though they had.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new, blocking, to human)
  - `tracker/items/WI-0003/questions/Q-002.md` (new, blocking, to human)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0003/item.md` — `## Notes` records where each of the five went and the open design question for `plan`; the stale "before the five questions below" pointer corrected; `updated` restamped. No criterion and no scope entry was changed.
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0003 is not Ready and cannot be made Ready without the stakeholder. Two blocking questions are with them; three of the five gaps were closed from their own prior answers and from recorded decisions, and the reasoning for each is on disk. The item suspends at `awaiting-answer` with `resume-to: draft`.

## 2026-08-30T00:17:23Z — answer-questions v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer` with two blocking questions addressed to `human`, both now
  carrying a reply in `## Answer`; dispatched ahead of `next` because an answered-but-unconsumed
  human question stops the orchestrator on every subsequent turn (F-011)
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` (the replies, verbatim)
  - `tracker/items/WI-0003/item.md`, `history.md` (the `resume-to: draft` on the suspending row)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (`status: agenda`, the DoR walk and the
    routing of all five edges)
  - `docs/architecture/adr/ADR-0007` v1 — decision 3 and its "what this ADR deliberately does not
    decide" paragraph, which named these two questions as its undecided edges
  - `docs/architecture/adr/ADR-0003` (decisions 4, 7, 9 and the outer-pipe recognition rule),
    `ADR-0004` (decision 1), `ADR-0005` (superseded), `ADR-0002`, `ADR-0006`, `ADR-0001`
  - `docs/product/vision.md` v6 — rounds 1 to 4 and `## What is not yet decided`
  - the prior human answers the cross-answer checks name: `EP-001/Q-001`, `Q-003`, `Q-004`,
    `Q-005`; `WI-0001/Q-001`, `Q-003`; `WI-0002/Q-001`
  - `.claude/agile-skills/spec/question.md`, `spec/doc-header.md` (§4, §4a, §4b),
    `spec/journal-and-history.md`
  - `tracker/items/WI-0002/journal.md` and `artifacts/refinement-qa.md`, for the precedent on what
    this skill may and may not do to a `refinement-qa.md` it did not write
- **Decisions:**
  - **Both answers were consumed as given; neither was interpreted.** Route 4 of SKILL.md step 3
    had already been taken by `refine` — these are escalations that came back — so this execution's
    job was propagation, not deciding. `Q-001` chose option A of four and `Q-002` option A of
    three, and both said so in as many words ("That's your A"; "Pad it — the left-hand table").
  - **Recorded both in one ADR rather than two.** ADR-0007 deferred the two edges as one
    paragraph and `WI-0003` asked them as one round; splitting the record would leave a reader of
    ADR-0007's "five undecided edges" sentence chasing two files and still not finding the three
    edges that never went to a person. ADR-0008 accounts for all five in one document, and marks
    which are the stakeholder's decisions (1 to 5), which are carried forward (6, 7) and which is
    an assumption (8).
  - **Wrote decision 1 as a shape rather than as a list of five strings.** `<`, `br` in any case,
    any whitespace, an optional `/`, `>`. The stakeholder's reason was that they do not type it
    the same way twice, so a closed list of exactly the four spellings they happened to name would
    have re-created the problem the question was asked to remove — `<br >` and `<Br/>` would behave
    differently from `<BR>` for no reason they would recognise. The shape is still exactly decidable
    from a terminal, which is what R4 needs.
  - **Recorded decision 3 — "nothing else exempts a cell" — and its cost, without asking again.**
    A cell whose text mentions `<br>` for some other reason is exempt too. None of the four options
    they were shown avoided that, so it is a consequence of their choice rather than a new question;
    it is written into ADR-0008 `## Consequences` under "hard" so nobody discovers it later and
    treats it as a defect.
  - **Kept ADR-0008 decision 8 tagged `[assumed]`, not `[human]`.** The *"top-left" means "left"*
    reading was put in front of them inside `Q-002`'s context so they could overturn it for free.
    They did not mention it. Silence on a flagged assumption is not endorsement, and recording it as
    theirs would be the fabrication the record exists to prevent.
  - **Repaired ADR-0007 in place rather than superseding it.** Adding `[src: ADR-0008]` to decision
    3's sentence is `spec/doc-header.md` §4b's `provenance` kind exactly: the assertion — that this
    ADR does not decide those two edges — is still true, no code would have to change to satisfy the
    new text, and the alternative was leaving the current exemption decision with no forward pointer
    to where its edges were settled.
  - **Amended no acceptance criterion.** The item is at `draft`, AC1 is explicitly marked
    provisional, and `refinement-qa.md` shows R4 and R10 needing one rewrite pass that covers AC1
    and the eight crossings together. Rewriting AC1 alone would split one Definition of Ready walk
    across two skills and leave the rest looking settled. What the criteria must now say is in
    `item.md` `## Notes` and in `refinement-qa.md`; `refine` writes them.
  - **Left `refinement-qa.md` at `status: agenda`.** Round 1 is now verbatim and true, but that
    field is `refine`'s and its walk is unfinished; declaring somebody else's conversation complete
    would let DoR R8 pass on our say-so. Same call, same reason, as this skill made on WI-0002.
  - **Filed no new work item.** Neither answer implies work no item records: both size an exemption
    `WI-0003` already exists to build, and neither widens the epic's scope.
- **Cross-answer check:**
  - `Q-001` checked against `EP-001/Q-004` (compatible — this answer is its missing half: it said
    "a line break or a `<br>`" without naming the forms), `EP-001/Q-005` (compatible — it settled
    which sentence governs an exempt cell, not which cells are exempt, and ADR-0007 listed this as
    an edge it did not decide), `WI-0002/Q-001` (compatible — its "every row, every column, no
    exceptions" was withdrawn by its own author at `EP-001/Q-005` and superseded by ADR-0007 before
    this question was filed; the conflict was escalated and settled then, and sizing the exemption
    does not reopen it), `EP-001/Q-003` (compatible — a fenced block is copied byte for byte by
    ADR-0003 decision 4 before any cell is composed, so a textual break-tag test cannot reach one).
  - `Q-002` checked against `EP-001/Q-004` (compatible and clarifying — it says what their word
    *"plain"* meant, and it is the narrower of the two readings), `EP-001/Q-001` (compatible — the
    leftover spaces sit before the cell's closing space and pipe, and this filter recognises only
    tables with outer pipes, so "nothing hangs off the right-hand edge" holds; it is *not* padding
    that would have been in tension with "columns are as wide as the widest cell in them"),
    `WI-0001/Q-001` (compatible, and they gave the same reason again unprompted — "it has to line up
    on the screen" there, "the closing pipes lining up is the whole reason I want this tool" here),
    `WI-0001/Q-003` (compatible — one space each side is the cell's border, not the leftover padding
    inside the column's width).
  - **No conflict declared, so no question was filed.** Nothing was resolved by editing a document.
  - **On the one paragraph under `docs/` this execution removed:** `vision.md`'s bullet listing the
    five undecided edges carried `[src: EP-001/Q-005]`. Removing it is an ordinary repair, not an
    overtaking: it asserted that five things were *not yet decided*, which stopped being true because
    the pipeline decided them — not because the stakeholder said anything incompatible with
    `EP-001/Q-005`. Their round-2, round-3 and round-4 paragraphs, which are their own words, are
    untouched. `lint-answers --uncommitted` over the three changed `docs/` paths → exit 0.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 consumed human answers
    checked, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 3 changed `docs/` paths in
    the claim window, 12 consumed human answers checked, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 on exactly two errors, both of
    which this transition and `board-gen` clear: `board.stale`, and `question.awaiting.none-open`
    on WI-0003 (the item is `awaiting-answer` with no open blocking question left, which is the
    state this execution created and is now resolving)
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in both `## Consequences` sections was
    opened after writing: `ADR-0008` exists with eight decisions (1 and 4 checked by name);
    `ADR-0007` is v2 with the `## Corrections` row and `[src: ADR-0008]` on decision 3;
    `vision.md` is v7 with `### Round 5` and without the five-edges bullet (`grep -c` → 0);
    `item.md` carries `**What the stakeholder answered**` with both replies verbatim;
    `refinement-qa.md` `## Round 1` carries both replies verbatim with the R4, R6 and R8 rows
    updated.
  - `answered-from-the-record` → **pass**, in the strongest form available: both answers are the
    stakeholder's own words, quoted verbatim in `## Answer`, in the ADR, in the vision, in
    `item.md` and in `refinement-qa.md`. Nothing was inferred. The three edges *not* answered by
    them are each sourced separately in ADR-0008 — decisions 6 and 7 to their earlier words and to
    ADR-0004/ADR-0007, decision 8 marked as an assumption.
  - `escalation-is-justified` → **skipped, no escalation.** Nothing was re-addressed to the human;
    both questions arrived answered and neither reply deferred or raised anything new.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` exit 0, 2 answers checked;
    `lint-answers --uncommitted` exit 0 over the changed `docs/` paths). Eight prior human answers
    were checked across the two questions, every verdict `compatible`, none declared `conflicts`.
  - `workspace-valid` → **pass on transition.** `validate-workspace` exit 1 before it, on
    `board.stale` and `question.awaiting.none-open` only; both are artefacts of this move not yet
    having been made and are cleared by it plus `board-gen`. Re-run recorded on the next entry.
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft` on the
    `draft → awaiting-answer` move made by `refine`; this execution returns the item to `draft`,
    read from that row rather than inferred from which skill asked.
  - `a-deferral-is-not-an-answer` → **skipped, no deferral.** Both replies decide: `Q-001` names an
    option ("That's your A") and `Q-002` names a table ("Pad it — the left-hand table"). Neither
    postpones anything, so neither of step 3a's two moves was in play.
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` — `answered`, `answered-by: human`,
    `answered-at: 2026-08-30T00:16:01Z`; five files named under `## Consequences`; a
    `## Cross-answer check` against four prior human answers
  - `tracker/items/WI-0003/questions/Q-002.md` — the same, against four prior human answers
  - `docs/architecture/adr/ADR-0008-edges-of-the-multiline-cell-exemption.md` (new, v1) — eight
    decisions closing all five of ADR-0007's edges, with both option sets as the stakeholder saw
    them and reversibility stated per decision
  - `docs/architecture/adr/ADR-0007-a-cell-containing-a-line-break-is-exempt-from-its-marker.md` —
    v1 → v2, one `provenance` correction, one `## Corrections` row, one change-log row
  - `docs/product/vision.md` — v6 → v7, `### Round 5 of refinement, on WI-0003` added, the
    five-edges bullet removed from `## What is not yet decided`
  - `tracker/items/WI-0003/item.md` — `## Notes` extended with both answers verbatim, the four
    things `refine` writes criteria from, and why no criterion was amended
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — preamble, R4/R6/R8 rows, `## Round 1` with
    both replies verbatim, `## Override` in the past tense; still `status: agenda`
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of round 1's blocking questions came back answered by the stakeholder and are
  now in the artifacts that decide the work: every spelling of an HTML break tag exempts a cell, a
  trailing backslash does not, and an exempt cell is still padded out to its column's width.
  ADR-0008 records that with the other three edges ADR-0007 left open, and WI-0003 returns to
  `draft` with nothing on it waiting on a person — `refine` has a Definition of Ready walk to
  finish, not a conversation to hold.

## 2026-08-30T00:22:15Z — refine v0.3.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` as the only runnable candidate
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` (the provisional AC1 and the whole of `## Notes`)
  - `tracker/items/WI-0003/history.md` — read first, per SKILL.md precondition 3. This item did
    **not** come back from `verifying` or `in-review`; it reached `draft` from `awaiting-answer`
    when `answer-questions` consumed the two replies, so this is the second half of one
    Definition of Ready walk, not a send-back and not a fresh draft
  - `tracker/items/WI-0003/journal.md` (round 1's walk, and the propagation entry before this one)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (`status: agenda`, the entry walk, the
    routing of all five edges, and both replies verbatim)
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` — both `answered`,
    `answered-by: human`, with their `## Cross-answer check` sections
  - `docs/architecture/adr/ADR-0008` (all eight decisions), `ADR-0007`, `ADR-0004`, `ADR-0003`,
    `ADR-0006` (test-name prefixes), `ADR-0001`
  - `docs/product/vision.md` v7, `### Round 5` and `## What is not yet decided`
  - `tracker/items/WI-0002/item.md` — its ten criteria and its criteria preamble, for the
    vocabulary this item's criteria reuse and for the three AC10 has to name as narrowed
  - `tracker/items/WI-0001/item.md` — its eleven criteria by ID, and its open escaped-pipe
    question routed to `plan`
  - `tracker/project.yaml` (`commands.test`), `mdtab.py:244` `compose_row` — read for the exact
    shape of a composed cell so the criteria describe the same object the code does
  - the prior human answers the round-1 cross-answer checks name: `EP-001/Q-001`, `Q-003`,
    `Q-004`, `Q-005`; `WI-0001/Q-001`, `Q-003`; `WI-0002/Q-001`
- **Decisions:**
  - **Held no round 2, and asked nothing.** The stakeholder is not in this session, and this is
    the case SKILL.md precondition 2 does *not* cover: nothing left on this item carries product
    stake. Both product questions were asked in round 1 and answered. Every remaining gap closed
    from the record or from those two answers, and the five that were checked one at a time are
    listed under `## Round 2 — considered, and not held` with the step-3 test that fired for each.
    Filing a question in order to satisfy a precondition would have cost a round trip and asked
    them nothing they could answer.
  - **Replaced the provisional AC1 with AC1 to AC11 in one pass**, rather than amending it. AC1
    was marked draft, was undecidable twice over, and R10's crossings had to land in the same
    rewrite; amending it alone would have left the rest of the walk looking settled.
  - **Wrote five criteria as a byte-exact expected output quoted in full** (AC1, AC2, AC3, AC5,
    AC6). The R4 test is "hand this to someone with a terminal and no context" — a criterion that
    says "the exempt cell is laid out left" makes that person re-derive column widths, the odd
    centring remainder and the delimiter fill before they can judge anything. A quoted table makes
    the verdict a diff. Each expected output was computed from the decisions in ADR-0008 and the
    width rules in ADR-0003/ADR-0004, and AC2's — which contains no exempt cell and therefore must
    match today's behaviour exactly — was checked against the shipped filter and matches byte for
    byte, which is evidence that the arithmetic in the other four is the same arithmetic.
  - **AC2 exists to pin the negative.** The stakeholder declined the trailing backslash in as many
    words, and a rule stated only positively ("a break tag exempts") is satisfied by an
    implementation that exempts far more. `C:\dir\`, `<b>bold</b>`, `<break>` and `brr` are the
    four ways a too-eager pattern goes wrong — a second backslash context, another tag, a tag
    whose name merely starts with `br`, and a bare word.
  - **AC3 carries three assertions in one table and says so.** Header-row reach, per-cell rather
    than per-column, and an untouched neighbouring column are one observation of one output; three
    criteria over three tables would have been three diffs of the same thing. R4 is satisfied
    because the criterion names what to read off the output rather than leaving it implied.
  - **AC4 states a case with no observable difference, deliberately.** A markerless column laid
    out left and an exempt cell laid out left are the same bytes. Writing it down is R10's job:
    the combination is visible, and a reader who wonders whether the exemption does something odd
    to an unmarked column finds the answer instead of assuming.
  - **AC10 names 21 prior criteria by ID and demands a read of their text**, per SKILL.md step 6a.
    It also names in advance the three — WI-0002 AC1, AC2 and AC3 — whose *"every content cell of
    that column"* this item narrows, and says explicitly that they are **not** to be edited: their
    author narrowed them at `EP-001/Q-005`, and rewriting a criterion because its author has since
    said something else is the move F-062 exists to stop.
  - **Left one R10 crossing deliberately unconstrained, with who left it so**: an exempt cell that
    also contains an escaped pipe. That is WI-0001's open design question, routed to `plan` and
    unsettled; deciding it inside this item would settle another item's question. Recorded in
    `## Notes` and in the crossings table, not in a criterion.
  - **Recorded the *"top-left" means "left"* reading as `[assumed]`, not `[human]`.** They left it
    standing in a question that flagged it for them; silence on a flagged assumption is not
    endorsement, and the criteria are written so it stays free to overturn.
  - **Extended `## Out of scope` from four entries to six**, adding rendering/wrapping the break
    tag and "any other convention for a line break" — the second because a reader who knows
    markdown's backslash syntax would otherwise reasonably assume it was included, and the
    stakeholder explicitly declined it.
  - **Split nothing.** R9 holds: one exemption, one test of a cell's text, one composing function.
- **Cross-answer check:**
  - The two answers this round's criteria are written from were consumed and checked by
    `answer-questions` in the entry immediately above, against eight prior human answers, every
    verdict `compatible` and none `conflicts`. This execution introduced no new answer and
    recorded no new condition, so it has nothing further to check and filed no question.
  - `lint-answers --item WI-0003` → exit 0, 2 consumed human answers checked.
  - **No document, criterion or vision statement was repaired because a recorded answer of theirs
    was overtaken.** WI-0002 AC1 to AC3 are the criteria this item narrows and they are left
    exactly as written; AC10 requires the narrowing to be *stated in the verify report*, which is
    the recording move, not the editing one.
- **Questions raised:** none this round. Round 1's two — `Q-001` and `Q-002`, both blocking, both
  to `human` — are `answered` and are recorded verbatim in `artifacts/refinement-qa.md`. Nothing
  is left `[unresolved]`; one thing is left `[assumed]` (the "top" reading) and one crossing is
  left deliberately unconstrained (an escaped pipe in an exempt cell), both named in `## Notes`.
- **Commands:**
  - `printf '| text |\n|:-:|\n| freeze\ |\n| C:\dir\ |\n| <b>bold</b> |\n| <break> |\n| brr |\n' | python3 mdtab.py`
    → exit 0, output byte-identical to AC2's quoted expected output (the check that AC2 asserts
    unchanged behaviour, and that the widths used in AC1, AC3, AC5 and AC6 are computed the same
    way the filter computes them)
  - `.claude/agile-skills/scripts/lint-answers --item WI-0003` → exit 0, 2 answers checked, 0
    errors, 0 warnings
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 10 documents, 0 errors
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings).
  - `definition-of-ready` → **pass, criterion by criterion**, the full table with evidence being in
    `artifacts/refinement-qa.md` `## Definition of Ready — the walk at exit`. R1 pass (frontmatter,
    auto). R2 pass (the story names the role, the capability and the "so that", and is still true
    of the criteria as rewritten). R3 pass (AC1 to AC11, labelled, checkboxes). **R4 pass — this is
    the criterion that failed on entry and the one this execution exists to close:** AC1, AC2, AC3,
    AC5 and AC6 quote a byte-exact expected output in full; AC4, AC7, AC8 and AC9 name the
    comparison and the verdict; AC10 names 21 criteria by ID and the read to perform; AC11 names
    the test command from `project.yaml`. No criterion contains an unmeasurable adjective. R5 pass
    (six exclusions, two of which a reader of the title could assume were included). **R6 pass** —
    no question on this item is open. R7 pass (`depends-on` empty; WI-0002 `done`/`delivered`).
    **R8 pass** — `refinement-qa.md` is `status: recorded`, holds both questions and both replies
    verbatim, and tags every answer. R9 pass (one coherent change). **R10 pass** — eighteen
    crossings tabulated in `refinement-qa.md`, each stated in a criterion, excluded, or recorded as
    deliberately unconstrained with who left it so.
  - `criteria-are-decidable` → **pass**, criterion by criterion. AC1, AC2, AC3, AC5, AC6: run the
    filter on the named input, `diff` against the quoted output — equal is pass. AC4: run on a
    table with a colon-free delimiter cell and confirm every content cell of that column is one
    space, text, `W - w` spaces, one space, with and without a break tag. AC7: inspect every
    delimiter cell of the AC1/AC2/AC3/AC5/AC6 outputs for the colon-for-colon identity and the
    `W + 2` length, and one empty cell against WI-0002 AC5's shape. AC8: three runs, three
    byte-comparisons (indent reproduced; fenced block identical; malformed block identical). AC9:
    feed each of AC1 to AC8's outputs back in and compare. AC10: read `artifacts/verify-report.md`
    for 21 named verdicts and the three required statements. AC11: run
    `python3 -m unittest discover -s tests -t .` and read the exit status.
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0003` exit 0). No new answer was
    consumed by this execution and no conflict was declared; the round-1 checks stand.
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` is `status: recorded` and holds
    both questions and both replies word for word as the stakeholder wrote them, each tagged
    `[human]`. The one `[assumed]` tag is the "top" reading and it is labelled as ours. Nothing is
    `[unresolved]`. Round 2's five non-questions are recorded as decisions not to ask, with the
    test that fired, rather than as answers.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — the provisional AC1 replaced by AC1 to AC11 with a criteria
    preamble defining "break tag", "exempt cell" and "laid out left"; `## Out of scope` extended
    from four entries to six; `## Notes` gains the round-2 record, the discharge of the
    "nothing may be built until Q-001 and Q-002 are answered" constraint, and the deliberately
    unconstrained escaped-pipe crossing
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; preamble
    rewritten; `## Round 2 — considered, and not held` with five entries; `## The R10 crossings`
    table with eighteen rows; `## Definition of Ready — the walk at exit` with all ten verdicts;
    `## Override` restated
- **Status:** `draft` → `ready`
- **Result:** WI-0003 is Ready. Eleven criteria replace the one provisional draft, five of them
  settled by diffing against an expected table quoted in full, and every one of the eighteen R10
  crossings is stated, excluded or recorded as unconstrained. No question was asked this round and
  none needed to be: round 1 got both things only the stakeholder could say, and everything else
  was already on the record. `plan` has an unambiguous target and one open design question waiting
  for it — where the break-tag test lives, and how it meets WI-0001's escaped pipe.

## 2026-08-30T00:26:51Z — plan v0.4.0 — architect

- **Item:** WI-0003
- **Trigger:** status `ready`, dispatched by `next` as the only runnable candidate
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1 to AC11 and the criteria preamble; the criteria are the
    contract this design answers to
  - `tracker/items/WI-0003/history.md` — read for a send-back. There is none: the item reached
    `ready` from `draft` on `refine`'s own walk, so this is a first plan, not a re-plan
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — in particular the one `[assumed]` entry
    (the *"top-left" means "left"* reading) and the one deliberately unconstrained R10 crossing
    (an escaped pipe inside an exempt cell), which are this design's soft ground
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md`
  - `docs/architecture/overview.md` v3 — the shape, the layout table and the rule-document list
  - `docs/architecture/adr/`: ADR-0008 (all eight decisions — the rule this plan implements),
    ADR-0007 (the current marker decision), ADR-0006 (test naming), ADR-0005 (superseded, read to
    confirm what ADR-0007 carried forward), ADR-0004 (the delimiter row), ADR-0003 (recognition,
    width, cell shape), ADR-0002 (superseded), ADR-0001 (the runtime)
  - `docs/product/vision.md` v7 — round 5, and the escaped-pipe entry still under `## What is not
    yet decided`
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`
  - **the code:** `mdtab.py` — `compose_row` (244), `column_alignments` (220), `emit_block` (287),
    `split_cells` (143), `candidate_parts` (124), `_is_escaped` (114), `column_widths` (190),
    `compose_delimiter` (270), `display_width` (65), `_DELIMITER_CELL` (90), and the module
    docstring; `tests/test_mdtab.py` — WI-0002's ten methods and its coverage test at 702;
    `tests/fixtures/` — the naming and pairing convention
  - `tracker/items/WI-0002/artifacts/plan.md` and `item.md`, for the criteria this item narrows
- **Decisions:**
  - **The exemption is applied per cell inside `compose_row`, as the first branch of the existing
    before-padding chain** — preference order branch 1, answered from the documents. ADR-0008
    decision 6 and the stakeholder's *"markers govern everything else"* [src: EP-001/Q-005] make
    the rule per cell, and `compose_row` is the only function that already sees one cell at a time
    [src: mdtab.py:244]. Recorded as **ADR-0009**, with two alternatives named: a per-cell
    alignment matrix built in `emit_block`, and — the reason the ADR is worth writing — nulling a
    whole column's alignment when any of its cells carries a tag. That last is the smallest diff
    of the three and is **wrong**: it would make the exemption per column. It is named and refused
    in writing so a developer who reaches for it finds the refusal instead of the silence.
  - **`column_alignments` and `emit_block` are not touched** — from the documents. A column's
    alignment stays a property of the delimiter row, which is what keeps ADR-0004 decision 1 and
    AC7's colon-for-colon identity true without anyone having to defend them.
  - **The predicate takes cell text as `split_cells` produced it, not a line** — from the
    documents. `split_cells` has already dropped the outer pipes and stripped whitespace
    [src: mdtab.py:143], and a delimiter cell that `table_or_none` accepted matches `^:?-+:?$` and
    can contain no `<` [src: mdtab.py:90], so the exemption is structurally unable to reach the
    delimiter row rather than being kept away from it by a check.
  - **Three reversible assumptions, recorded under `## Assumptions` with their reversal cost** —
    preference order branch 2: that six spellings and five counter-examples adequately sample
    ADR-0008 decision 1's pattern; that `re.IGNORECASE` over ASCII `b` and `r` is what "any letter
    case" means; and that compiling the pattern once is a preference rather than a measured need,
    because no performance requirement exists anywhere in the record.
  - **Asked the human nothing** — preference order branch 3 was not reached. The two decisions that
    depended on their intent were asked in refinement and answered; everything else followed from a
    document or is a reversible assumption. Escalating here would have been the "human as design
    service" failure the preference order exists to prevent.
  - **Wrote AC3's neighbour assertions into the plan explicitly**, rather than trusting its byte
    comparison. AC1, AC2, AC5 and AC6 would all still pass against ADR-0009's refused option C;
    AC3 is the one criterion that catches it, and only if the test reads the *other* cells of the
    two marked columns. That is recorded as the first entry under `## Risks`.
  - **Did not settle WI-0001's escaped-pipe question**, although this is the skill it was routed
    to. It belongs to another item, no criterion of this one needs it, and deciding it inside this
    plan would hide the decision where nobody looking at WI-0001 would find it. Recorded under
    `## Risks` with what today's code does, and under `## Out of scope for this item`.
  - **Updated `docs/architecture/overview.md` to v4.** Its rule-document list still presented
    ADR-0005 as the current statement of where a marker puts cell text, which ADR-0007 superseded
    two executions ago; the list now names ADR-0007, ADR-0008 and ADR-0009. This is an ordinary
    currency repair of our own prose — the sentence cites `[src: ADR-0005]`, not one of the
    stakeholder's answers, and nothing they said was rewritten.
  - **Wrote no production code and no scaffolding.** `tests/` already carries `__init__.py`, so
    `commands.test` executes without anything being created; `## Scaffolding` records `none`.
- **Cross-answer check:** this execution recorded no new human answer and relied on two already
  consumed — `WI-0003/Q-001` and `Q-002` — which `answer-questions` checked against eight prior
  answers two entries ago, every verdict `compatible`. Checked again here for the specific claims
  this plan rests on: `EP-001/Q-005` (*"markers govern everything else"*) — **compatible**, and it
  is the authority for refusing ADR-0009's option C; `EP-001/Q-001` (*"nothing hangs off the
  right-hand edge"*) — **compatible**, the exemption adds no trailing whitespace because the
  leftover spaces sit before the cell's closing space and pipe; `WI-0001/Q-003` (*"one space each
  side, always"*) — **compatible**, `compose_row`'s two surrounding spaces are untouched by every
  step in this plan. No conflict declared, so no question was filed, and no ADR written here
  reconciles two of their statements. `lint-answers --uncommitted` → exit 0.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 24 tests, OK (the `commands.test` value
    verified as a command that actually runs in this project, before it was relied on)
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0 (`commands.lint`)
  - `.claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 2 documents in 2 uncommitted
    paths under `docs`, 0 errors
  - `.claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 12 consumed human answers
    checked, 0 errors
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 4 items, 11 documents, 0 errors
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 11 documents, 0 errors).
  - `every-criterion-is-addressed` → **pass**. `plan.md` `## Acceptance criteria mapping` carries
    eleven rows, one per criterion, each naming the steps that satisfy it and the named test method
    that demonstrates it. Nothing maps to "tests": AC1 to AC6 and AC8 name a byte comparison
    against a specific fixture pair, AC7 names the two assertions and the five outputs they run
    over, AC9 names the re-feed, AC10 names the split between the covering-case test and `verify`'s
    21 per-ID verdicts, and AC11 names the coverage tag. Applied the reverse check too: every step
    in `## Steps` maps to at least one criterion, so nothing in the plan is unrequested.
  - `project-commands-resolved` → **pass, on commands run in this execution rather than assumed.**
    `commands.test` = `python3 -m unittest discover -s tests -t .` → exit 0, 24 tests OK.
    `commands.lint` = `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → exit 0. `commands.build`
    is `null`, honestly: ADR-0001 fixes this project as a single script with no build step, so
    there is nothing for it to name. `project.yaml` was not edited — both values were already
    correct and re-verified.
  - `decisions-recorded` → **pass**. `plan.md` `## Decisions and ADRs` is a six-row table: one new
    ADR (ADR-0009), four decisions cited to standing documents rather than re-decided (ADR-0006,
    ADR-0004/ADR-0007, ADR-0003/ADR-0008, and ADR-0008 itself), and three reversible assumptions
    each with its reversal cost stated under `## Assumptions`. No choice in this plan is unaccounted
    for in that table.
  - `plan-is-executable-without-you` (advisory) → **pass, on a re-read from cold.** Every step names
    the file it touches and what is true afterwards; the two expected outputs the criteria do not
    already quote (AC4's and AC8's indented table) are quoted inside step 5, so no step requires
    deriving a column width. The interfaces are given (`_BREAK_TAG`, `has_break_tag(text)` and its
    contract) and the bodies are not, which is the line this skill is not to cross. The one place a
    developer could still go wrong — reaching for the per-column shortcut — is named in `## Risks`
    and refused in ADR-0009.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0 over the two changed
    `docs/` paths; 12 consumed human answers checked). The per-answer reasoning is in the
    `**Cross-answer check:**` bullet above.
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0, 2 documents, 0 errors).
    Every absolute claim this execution wrote about named code carries a resolvable `[src: ...]` —
    the `mdtab.py:<line>` citations in ADR-0009, `plan.md` and the overview all resolve to the file.
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/plan.md` (new) — problem, approach, seven numbered steps, the
    eleven-row criteria mapping, three assumptions, the decisions table, `## Scaffolding` = none,
    four risks, six out-of-scope entries
  - `docs/architecture/adr/ADR-0009-break-tag-exemption-is-applied-per-cell-at-composition.md`
    (new, v1) — five decisions, three options with the wrong one named and refused, reversibility
    stated per decision
  - `docs/architecture/overview.md` — v3 → v4, the rule-document list brought up to date with
    ADR-0007, ADR-0008 and ADR-0009
  - `tracker/project.yaml` — unchanged; both commands were already correct and were re-verified
- **Status:** `ready` → `planned`
- **Result:** WI-0003 is planned. The change is one compiled pattern, one predicate, one branch in
  `compose_row`, nine fixture pairs and eleven tests; `column_alignments` and `emit_block` are
  deliberately untouched, so recognition, width and the delimiter row cannot move. ADR-0009 records
  the siting decision together with the smaller, wrong alternative that would have made the
  exemption per column, because that is the mistake this design is most likely to be implemented as.

## 2026-08-30T00:28:47Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `planned`, dispatched by `next` as the only runnable candidate (EP-001 `open` and WI-0001/WI-0002 `done` all have a null owner).
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the eleven acceptance criteria, the out-of-scope list and the Notes recording what the stakeholder answered
  - `tracker/items/WI-0003/artifacts/plan.md` — the seven steps, the AC-to-test mapping, the three assumptions and the risks
  - `tracker/items/WI-0003/history.md` — five rows; the last is `ready` → `planned` by `plan`, so this is a fresh start with no branch
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` — both `answered`, `answered-by: human`, both propagated into ADR-0008 before this execution
  - `docs/architecture/adr/ADR-0008-edges-of-the-multiline-cell-exemption.md` — decisions 1 to 8: which cells are exempt, and that an exempt cell is still padded
  - `docs/architecture/adr/ADR-0009-break-tag-exemption-is-applied-per-cell-at-composition.md` — decisions 1 to 5: the exemption goes in `compose_row`, option C is refused
  - `docs/architecture/adr/ADR-0006-per-item-test-name-prefixes.md` — the `test_wi0003_ac<n>_<slug>` naming this item's tests must use
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, the `wi/` branch prefix and the commit-subject convention
  - `mdtab.py` — `compose_row`, `column_alignments`, `emit_block`, `split_cells`, `display_width`, and the module docstring's rule-document list
  - `tests/test_mdtab.py` and `tests/fixtures/` — the existing WI-0001 and WI-0002 tests and the twenty-nine fixture files the new ones sit beside
- **Decisions:**
  - Started fresh rather than reconciling: `git branch` showed no `wi/WI-0003`, and the last history row is `plan`'s, not a send-back from `verifying` or `in-review`.
  - Moved to `in-progress` before writing any code, so an interruption leaves a truthful status and a branch a later execution can reconcile with.
- **Cross-answer check:** none — this entry edits no `docs/` sentence at all.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0003 main` → 0 (branch created from trunk at `fbf9fce`)
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no change has been made, so a run would report on code that is about to change)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **skipped** (`next` ran it clean immediately before dispatching; this skill runs it as a completion gate)
  - `every-criterion-has-a-test` → **skipped** (no test written yet)
  - `commits-reference-the-item` → **skipped** (no commit on the branch yet)
  - `cross-answer-consistency` → **skipped** (nothing changed since trunk yet)
  - `claims-are-sourced` → **skipped** (nothing changed since trunk yet)
  - `no-unplanned-scope` (advisory) → **skipped** (the diff is empty)
- **Artifacts:**
  - branch `wi/WI-0003`, created from `main`; no commit yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0003 has started on `wi/WI-0003`. The plan's seven steps are unstarted; the closing entry reports the work and runs every gate on the branch head.

## 2026-08-30T00:38:33Z — implement v0.3.0 — developer

- **Item:** WI-0003
- **Trigger:** status `in-progress`, continuing this turn's own execution — the opening entry above created the branch and the plan's seven steps were unstarted.
- **Inputs read:**
  - `tracker/items/WI-0003/artifacts/plan.md` — steps 1 to 7, the AC-to-test mapping, the three assumptions and the four risks
  - `tracker/items/WI-0003/item.md` — AC1 to AC11, including the five expected tables quoted in full
  - `docs/architecture/adr/ADR-0008-edges-of-the-multiline-cell-exemption.md` and `ADR-0009-break-tag-exemption-is-applied-per-cell-at-composition.md` — the rule, and where it is applied
  - `docs/architecture/adr/ADR-0006-per-item-test-name-prefixes.md` — the `test_wi0003_ac<n>_<slug>` convention and the per-item coverage tag
  - `docs/architecture/overview.md` v4 and `docs/product/vision.md` v7 — read for D12, to decide whether any claim about the behaviour this item changes had become false
  - `mdtab.py` and `tests/test_mdtab.py` in full, and `tests/fixtures/` — the code being changed and the twenty-nine fixtures the sixteen new ones sit beside
  - `.claude/agile-skills/spec/doc-header.md` §4 citation forms — after `validate-workspace` rejected four citations in the first draft of `impl-report.md`
- **Decisions:**
  - **Extended `INPUT_FIXTURES` with WI-0003's nine inputs** rather than giving them a list of their own. `INPUT_FIXTURES` is what WI-0001 AC3, AC9 and AC10 and WI-0002 AC8 loop over, so this is the mechanism by which four prior criteria come to range over break-tag content — which is exactly what AC10's third bullet asks for, and the same move WI-0002 made for its own inputs.
  - **Added one assertion to AC3's test beyond the plan's list.** Every exempt cell in AC3's own quoted table is its column's widest, so `W - w` is zero for each and that table is equally the output of a filter with no exemption at all — confirmed by deleting the `compose_row` branch and re-running, which failed AC1, AC6 and AC9 but passed AC3. AC3's stated claim is about a header cell under a right marker, so the test now also runs an inline table whose exempt header is narrower than its column. No criterion text and no expected file was changed. Recorded as deviation 1 in `impl-report.md`.
  - **Built AC10's three inline covering cases as byte literals in the test** rather than as fixtures, so `tests/fixtures/` holds exactly the nine inputs plan step 5 lists.
  - **Left `docs/` untouched.** D12 was asked and answered no-change-needed: the overview's rule-document list already names ADR-0007, ADR-0008 and ADR-0009, and the vision already carries the stakeholder's round-2 absolute verbatim with the paragraph recording that its author narrowed it. There was no false sentence to repair.
  - **Did not settle WI-0001's escaped-pipe question**, which the item and the plan both leave deliberately unconstrained. Nothing in steps 1 to 7 required it: the exemption decides where a cell's text sits, never what its text is or how wide it is.
  - **Moved four citations in `impl-report.md` out of their `[src: ...]` markers** — `[src: ADR-0009 decisions 1 and 4]` and three like it — after `validate-workspace` rejected the form. `spec/doc-header.md`'s citation table admits `[src: ADR-0009]` and not a decision-numbered variant, so the decision numbers are now prose beside a bare ADR citation.
- **Cross-answer check:** none — this execution edited no file under `docs/` at all, so it rewrote no sentence sourced to one of the stakeholder's answers. `docs/product/vision.md` lines 118-125 are the case ADR-0008 §3 is about, and they were already correct: the round-2 absolute *"every row, every column, no exceptions"* [src: WI-0002/Q-001] is kept as its author wrote it, with a following paragraph recording that they have since narrowed it [src: EP-001/Q-005]. Nothing there needed repairing and nothing needed asking.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → 0 (`Ran 37 tests in 7.934s`, `OK`) on the branch head
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (4 items, 11 documents, 0 errors) — after the citation repair; it exited 1 on the first draft of `impl-report.md`
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → 0 (`all 2 commit(s) on main..wi/WI-0003 name WI-0003`)
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → 0 (12 consumed human answers checked, 0 paths differ under `docs`)
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0 (citations checked over every markdown file in the workspace)
  - mutation checks, both reverted: with the `compose_row` branch deleted → `FAILED (failures=5)`, AC1, AC3, AC6 and AC9 failing; with ADR-0009's refused option C in its place → `FAILED (failures=9)`, AC1, AC3, AC5, AC8, AC9 and AC10 failing
  - a byte comparison of each of the seven expected fixtures against the fenced block quoted in its criterion (`item.md` for AC1, AC2, AC3, AC5, AC6; `plan.md` step 5 for AC4 and AC8) → all seven MATCH
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 37 tests, run on the branch head after the last change)
  - `lint-clean` → **pass** (`python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md`'s evidence table names one test method per criterion for AC1 to AC11; `test_wi0003_ac11_each_criterion_has_a_named_test` enforces exactly one method per tag mechanically)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0003 wi/WI-0003` exit 0, 2 commits)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` exit 0; see the cross-answer check above)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0)
  - `no-unplanned-scope` (advisory) → **pass** (`git diff main..HEAD --stat`: `mdtab.py` for steps 1 to 4, `tests/test_mdtab.py` for step 6 and the `INPUT_FIXTURES` extension AC10 requires, sixteen files under `tests/fixtures/` for step 5. The one hunk not in the plan's list is AC3's extra assertion, traced to AC3 and recorded as deviation 1)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/impl-report.md` — what was built, the AC-to-evidence table, the twenty-one-row covering map AC10 needs, the deviations and the gates
  - `mdtab.py` — `_BREAK_TAG`, `has_break_tag`, the `compose_row` branch, and two docstrings
  - `tests/test_mdtab.py` — eleven criterion tests, one untagged predicate test, and the `INPUT_FIXTURES` extension
  - sixteen files under `tests/fixtures/` — nine inputs and seven expected outputs
  - branch `wi/WI-0003`, commits `2968ac2` and `1100203` (`main..wi/WI-0003`)
- **Status:** `in-progress` → `verifying`
- **Result:** The break-tag exemption is implemented per cell inside `compose_row`, as ADR-0009 requires, and all eleven criteria have a named test with byte-exact evidence. Two things `verify` should not take on trust: AC10's twenty-one per-ID verdicts are not written here, only the covering cases they are to be read against; and AC3, AC5 and AC8 quote tables whose exempt cells are their columns' widest, so a green run of those three alone is not evidence that the exemption exists — AC1, AC3's second table and AC6 are what discriminate.

## 2026-08-30T00:47:38Z — verify v0.2.0 — qa-engineer

- **Item:** WI-0003
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1 to AC11, read **before** the implementation report, and the five expected tables quoted in them
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/item.md` — the twenty-one prior criteria AC10 names, read by ID from their own text
  - `tracker/items/WI-0003/artifacts/plan.md` — the seven steps and the AC-to-test mapping, read to find undeclared behaviour in the diff
  - `tracker/items/WI-0003/artifacts/impl-report.md` — the claimed evidence, checked rather than trusted; no verdict below rests on it
  - `tracker/items/WI-0003/history.md` — five rows plus this execution's two; no send-back precedes it
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - the code at branch head `a93db5fe5e045533f610890bdc479e5c4d213fc4` — `git diff main..HEAD` over `mdtab.py` and `tests/`, read hunk by hunk
- **Decisions:**
  - **Settled AC1 to AC9 against inputs I wrote from the criteria's prose**, ragged differently from the implementation's fixtures, diffed against the expected tables extracted programmatically from `item.md` (AC1, AC2, AC3, AC5, AC6) and `plan.md` (AC4, AC8). Running the developer's fixtures would have checked that the code does what it does.
  - **Wrote three discriminating cases of my own**, because AC3, AC5 and AC8 quote tables whose exempt cells are their columns' widest — `W - w` is zero for each, so those three tables are equally the output of a filter with no exemption at all. All three produced the exempt layout. This is recorded as an observation, not a defect: the behaviour is present and the criteria are the stakeholder-facing statements agreed at refinement. `impl-report.md` had already declared it for AC3 and AC5; it was re-derived here independently.
  - **Recorded WI-0002 AC1 as narrowed although the narrowing has no observable consequence.** A left-marked cell and an exempt cell compose identically, so every output byte is unchanged — but WI-0003 AC10 requires the verdict on AC1, AC2 and AC3 to say the sentence now holds only of a cell containing no break tag, and the sentence's *reason* has changed. Recorded as narrowed, with the no-consequence finding stated beside it rather than instead of it.
  - **Waived three prior criteria by ID for non-intersection** — WI-0001 AC11, WI-0002 AC9 and WI-0002 AC10. Each is a claim about the record or about test method names, for which "a covering case carrying a break tag" has no meaning. Stated in those words, and what could actually break them was checked instead: every `wi0001_ac1..11` and `wi0002_ac1..10` tag still matches exactly one method after eleven `wi0003_` methods were added.
  - **No criterion judged ambiguous, and no question filed.** Every criterion named an input and an output precisely enough to be settled by a diff or by arithmetic on the output.
  - **No defect classified either way**, because none was found: nothing in this item's own criteria failed, and nothing in behaviour delivered by WI-0001 or WI-0002 failed either. No send-back, no bug item.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → `a93db5fe5e045533f610890bdc479e5c4d213fc4`; `git status --short` → clean
  - `python3 -m unittest discover -s tests -t .` → 0 (`Ran 37 tests in 7.986s`, `OK`), and again with `-v` to read every test's name and docstring
  - `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (4 items, 11 documents, 0 errors) — run before the report was written and again after
  - five inputs written here from AC1, AC2, AC3, AC5 and AC6's prose, each filtered and `diff -u`'d against the block extracted from `item.md` → no diff on any, exit 0 on all
  - the prose clauses of AC1, AC2, AC3, AC5 and AC6 read off those outputs by arithmetic (`(W-w)//2` before, remainder after; `" " + text + (W-w) spaces + " "`) → 14 clause checks, all PASS
  - AC4 by an unmarked-column run plus a substitution run replacing the break tag with a same-width plain text → the two outputs identical modulo the text
  - AC7 by an empty-cell run (empty cells came back `'   '`, `W + 2` with `W = 1`) and a delimiter sweep over five break-tag tables, `W` recomputed from each input's own content rows → all PASS
  - AC8 by an indented run, a two-fence run and a malformed-block run → indent kept on every line, both non-tables byte-identical
  - AC9 by filtering ten inputs twice → byte-identical, exit 0 on both passes
  - AC11 by `grep -c "def test_wi0003_ac<n>_"` for n in 1..11, deliberately not the suite's own coverage test → exactly one each
  - fourteen negative and boundary cases, each triggered: empty input, prose with `<br>`, a blockquoted table, an indent-mismatched block, a cell whose whole text is `<br>`, `<br` / `br>` / `< br >` / `<b r>`, `<br\t/>`, trailing backslashes, a wholly empty marked column, empty cells across three markers, a delimiter row containing `<br>`, invalid UTF-8, CRLF, and no final newline → all exit 0, all as the criteria require
  - six mutations of the branch head, each reverted immediately: delete the `compose_row` branch → `FAILED (failures=5)`; ADR-0009's refused option C → `FAILED (failures=9)`; widen `_BREAK_TAG` to bare `br` → `FAILED (failures=7)`; make an unmarked column centre → `FAILED (failures=11)`; drop the leading colon from `compose_delimiter` → `FAILED (failures=51)`; rename `test_wi0003_ac6_...` out of ADR-0006's convention → `FAILED (failures=1)`. `git status --short` clean afterwards, suite `OK`
  - `git diff main..HEAD -- mdtab.py` and `-- tests/` read hunk by hunk; `git diff main..HEAD -- tests/test_mdtab.py | grep "^-"` → three removed lines, all docstring
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 37 tests, run by this skill on `a93db5f`)
  - `lint-clean` → **pass** (`python3 -m compileall ...` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (each row of `verify-report.md`'s `## Criteria` names a command this skill ran and quotes its actual output; AC1 to AC9 settled against inputs written here, not against the implementation's fixtures)
  - `negative-cases-exercised` → **pass** (fourteen cases in `## Negative and boundary cases exercised`, each triggered with its outcome recorded)
  - `a-criterion-about-criteria-is-read` → **pass** (twenty-one per-ID verdicts read from each criterion's own text; AC10's three required statements made explicitly; two non-intersections stated in those words and three criteria waived by ID)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (six mutations, each reverted; every one of AC1 to AC11 has at least one mutation that fails its own named test)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/verify-report.md` — the verdicts, the twenty-one-row AC10 read, the gates, the fourteen negative cases, the six mutations and the three discriminating cases
  - `tracker/items/WI-0003/item.md` — AC1 to AC11 all ticked, each against a command recorded above
  - no bug item filed; no question filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0003 passes on all eleven criteria, verified at `a93db5f` against inputs derived from the criteria rather than from the implementation. Three things `review-close` should carry forward: AC3, AC5 and AC8 quote tables that a filter with no exemption would also produce, so their green state is not by itself evidence the feature exists — three discriminating cases were run and are in the report; WI-0002 AC1, AC2 and AC3 are recorded as narrowed by this item, AC1's narrowing having no observable consequence; and WI-0001 AC11, WI-0002 AC9 and WI-0002 AC10 are waived by ID for non-intersection, which is the only waiving in the report.

## 2026-08-30T00:52:41Z — review-close v0.6.0 — reviewer

- **Item:** WI-0003
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — the eleven criteria and their tick state, `## Out of scope`, and the whole of `## Notes`
  - `tracker/items/WI-0003/journal.md` — all nine entries in full, not skimmed; `history.md` — all eight rows
  - `tracker/items/WI-0003/artifacts/plan.md`, `impl-report.md`, `verify-report.md` — the design, the declared deviations, and the evidence behind every tick
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-002.md` — including their `## Consequences` and `## Cross-answer check`
  - the diff `main..dea2b53`, hunk by hunk: two regions of `mdtab.py`, four hunks of `tests/test_mdtab.py`, sixteen new fixture files
  - `docs/architecture/adr/ADR-0007`, `ADR-0008`, `ADR-0009`, `ADR-0005` (header), `docs/architecture/overview.md` v4 and `docs/product/vision.md` v7 — opened for the D12 audit, from the citations rather than from the prose
  - `.claude/agile-skills/spec/dor-dod.md` §3, walked criterion by criterion
- **Decisions:**
  - **Accepted.** Every hunk of the diff maps to an acceptance criterion or a plan step; nothing contradicts an ADR; the record answers all four reconstructibility questions from the tracker, `docs/` and `git log` alone.
  - **Recorded three findings, none blocking.** (a) AC3, AC5 and AC8 quote expected tables whose exempt cells are their columns' widest, so `W - w` is zero and each is equally the output of a filter with no exemption; both `implement` and `verify` found this independently and both wrote discriminating cases, so the behaviour is demonstrated even though those three criteria do not demonstrate it. It is not grounds to edit a criterion — they are the stakeholder-facing statements agreed at refinement. (b) `widths_of` in the test module re-implements `column_widths`' rule deliberately, to keep AC7 from being a tautology, and will drift if ADR-0004 decision 2 changes; its docstring names the ADR, which is the mitigation. (c) the suite's wall time roughly doubled as `INPUT_FIXTURES` grew from twenty to twenty-nine entries; an observation, no action.
  - **Judged five declared gaps acceptable**, each because it already has a home that survives this item closing: the sampling assumption lives in `plan.md`; the escaped-pipe question lives in `docs/product/vision.md` `## What is not yet decided` at engagement level as well as in `item.md` `## Notes`; the renderer exclusion lives in `## Out of scope`; the absence of a performance measurement lives in ADR-0009 decision 4; the context-blindness of the rule lives in ADR-0008's and ADR-0009's consequences. None needed a new note or a follow-up item.
  - **D7 passes vacuously and on purpose.** The change invalidated no document: ADR-0007 v2, ADR-0008, ADR-0009, overview v4 and vision v7 were all written for this item before the code and already describe it. Established by reading each claim against the code, not by remembering.
  - **Did not repair `docs/product/vision.md`'s round-2 absolute.** *"Every row, every column, no exceptions"* [src: WI-0002/Q-001] is the stakeholder's own sentence and the item this review closes is what narrowed it — but the narrowing was already put to them as `EP-001/Q-005`, they authorised it, and the vision already carries the paragraph recording that. ADR-0008 §3's third row does not apply because the reconciliation has already happened; editing their sentence would be the F-062 failure.
  - **Did not end the engagement.** `engagement-state EP-001` reported `active`, *"still in flight: WI-0003"*, when this review began. Closing WI-0003 brings it to rest, and ending an engagement is its own dispatch on the epic at the orchestrator's step 6. Ending it here would be two actions in one run and would file a sign-off question on an engagement that was still running when this execution started.
  - **No bug filed and no send-back**, because nothing was found that belongs to another item or that fails this item's own criteria.
- **Cross-answer check:** none consumed by this execution. This review resolved no question and recorded no new human answer; the two on this item, `Q-001` and `Q-002`, were consumed by `answer-questions` before refinement finished, and their own `## Cross-answer check` sections are in their files. The one place a contradiction could still have been live — the vision's round-2 absolute against the round-4 exemption — was checked and is already reconciled by `EP-001/Q-005` and recorded in ADR-0007. `lint-answers --context work-item --changed-since main` exited 0 over twelve consumed human answers.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0003 wi/WI-0003` → 0 (*"verified at a93db5fe; wi/WI-0003 has moved to dea2b535 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*)
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0003 wi/WI-0003` → 0 (*"all 4 commit(s) on main..wi/WI-0003 name WI-0003"*)
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → 0
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0003` → 0 (*"WI-0003 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."*)
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → 0, verdict **`active`**, *"still in flight: WI-0003"*, rest reached at 2026-08-30T00:47:38Z
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (4 items, 11 documents, 0 errors), run before and after writing `review.md`
  - `git rev-parse main` → `fbf9fcea93d65478a5cd14e32e8f6456edf3d331` before the trial
  - `git worktree add --detach /tmp/wi3-trial main` → 0; `git -C /tmp/wi3-trial merge --no-ff wi/WI-0003` → 0, trial HEAD `b6555e8af8e594397b2a13716c8a8c1556852aa2`
  - `python3 -m unittest discover -s tests -t .` **inside the trial worktree** → 0 (`Ran 37 tests in 7.884s`, `OK`); `python3 -m compileall -q -x '(^|/)\.claude(/|$)' .` inside it → 0
  - `git worktree remove --force /tmp/wi3-trial` → 0; `git rev-parse main` → `fbf9fce`, unchanged: the trial did not move the trunk
  - `git diff main..HEAD -- tests/test_mdtab.py | grep "^-"` → three lines, all docstring; no assertion removed
  - `grep -c "^- \[x\] AC" item.md` → 11; `grep -c "^- \[ \] AC" item.md` → 0
  - `transition WI-0003 --to done` **refused once**, and correctly: `outcome: delivered` had been
    written into `item.md` before the move, and `validate-workspace` reported
    `item.outcome.premature` — *"outcome is set to 'delivered' but the item is not done"*. The
    field was removed and the outcome passed to the transition as `--outcome delivered` instead,
    which is the sanctioned path: `scripts/transition` writes status and outcome together in one
    step, so the workspace never holds the intermediate state the validator refuses. No override
    was used and no gate was forced.
- **Gates:**
  - `definition-of-done` → **pass** (D1 to D12 each recorded with its own result and evidence in `review.md`'s `## Definition of Done` table; D7 passes vacuously, established by reading rather than by memory; D9 by the merge that follows this close)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the last *code* commit is `1100203` and both the implementation's and the verification's gate runs postdate it)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 4 commits — run while the branch was still unmerged, which is why the close precedes the merge)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` inside the detached trial worktree at `b6555e8`: `Ran 37 tests`, `OK`, exit 0 — on the merge result, not on the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** (all four questions answered in `review.md` `## What I examined`, from the tracker, `docs/` and `git log --grep WI-0003` alone: what was built and why, which skill decided what, which questions arose and how they resolved, what verification found)
  - `claims-are-sourced` → **pass**. Scope, quoted from the gate's own output: *"checked absolute claims: 0 document(s) in 0 path(s) differ from main (fbf9fce) under docs; citations: every markdown file in the workspace"*. This item's diff genuinely contains no file under `docs/`, so the automatic half examined nothing under that heading and the citation half examined the whole workspace; the substantive audit is therefore the fourteen-row table in `review.md`, each row opened from its citation and read against the code
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` exit 0, *"checked 12 consumed human answer(s) in the workspace"*)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0003` exit 0 with the reason that WI-0003 is a work item; the termination gate belongs to the epic's ending, which this execution did not perform and which `engagement-state` said was not yet available when it began)
- **Artifacts:**
  - `tracker/items/WI-0003/artifacts/review.md` — what was examined, the eight-row diff map, the fourteen-row claims audit, D1 to D12, three findings, five accepted gaps, the verdict
  - `tracker/items/WI-0003/item.md` — `outcome: delivered`, status closed by this transition
  - the merge of `wi/WI-0003` into `main`, made **after** this close; the trial merge at `b6555e8` was discarded and published nothing
  - no bug item, no question, no change under `docs/`
- **Status:** `in-review` → `done`
- **Result:** WI-0003 is accepted and closed as delivered. The break-tag exemption is applied per cell inside `compose_row`, ADR-0009's refused per-column shortcut is demonstrably not what was built, and every claim in `docs/` about the behaviour was re-read against the code from its citation. The three findings are recorded rather than actioned, and the five declared gaps each already live somewhere that outlives this item. `engagement-state EP-001` said `active` while this ran; with WI-0003 closed the engagement reaches rest, and ending it — filing the sign-off question that names every child — is the orchestrator's next dispatch, on the epic.
