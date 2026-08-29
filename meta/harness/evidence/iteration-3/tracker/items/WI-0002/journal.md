# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-28T18:26:52Z — intake v0.2.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** created by this execution; intake was invoked directly on the stakeholder's stated idea (`IDEA.md`), not dispatched by `next`
- **Inputs read:**
  - `IDEA.md` — the stakeholder's idea in their own words
  - `tracker/project.yaml`
  - `tracker/items/` (empty before this execution)
  - `tracker/items/WI-0001/item.md` — written moments earlier by this same execution, to set the boundary between the two items
- **Decisions:**
  - See `EP-001`'s entry for how the work was split and why alignment markers are a separate
    item rather than part of WI-0001.
  - Set `depends-on: [WI-0001]`. Rationale: there is no padding to make alignment-aware until
    padding exists, so the order is forced by the work rather than chosen. The stakeholder stated
    no priority ordering and none was invented — both items are `high` and the sequence comes
    from this dependency.
  - AC5 restates that WI-0001's criteria must still hold, rather than assuming it. Rationale:
    the most likely way this item breaks the product is by regressing the passthrough guarantee
    while changing the padding code, and a criterion nobody wrote is a criterion `verify` will
    not check.
  - Did not write a criterion for how a centred cell with an odd number of spare spaces splits
    them, because either split is defensible and the stakeholder has expressed no preference.
    Recorded as an unknown in `## Notes` for `refine`.
- **Questions raised:** none on this item; `EP-001/Q-001` and `EP-001/Q-003` bear on it and are
  open on the epic
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --title ... --epic EP-001 --priority high --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **fail at the time of writing** (`scripts/validate-workspace`, exit 1: `question.blocking.not-suspended` on EP-001 and `journal.execution.missing`; both are states this execution is in the middle of resolving, and the epic's transition re-runs the gate)
  - `epic-has-success-measures` → **pass** (see EP-001's entry; the measures are on the epic, not on this item)
  - `items-are-separable` → **pass** (WI-0002 is built second, after WI-0001, and delivers something a user can see on its own: a right-aligned column that is actually right-aligned)
  - `no-solution-in-the-problem` → **pass** (title and story name only what the stakeholder named — alignment markers, the delimiter row, padding — and no technology)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/history.md`, `journal.md` (new)
- **Status:** `—` → `draft`
- **Result:** The alignment-marker item created at `draft`, depending on WI-0001. Two unknowns
  bearing on it are open questions on EP-001, plus one local unknown (odd-space centring) for
  `refine`.

## 2026-08-28T20:13:39Z — refine v0.2.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`; dispatched by `next` (pipeline.yaml owner of `draft`) as the only runnable candidate
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md` — the draft, its single creation row, and `intake`'s verbatim record of what it deliberately left unspecified
  - `tracker/items/WI-0002/artifacts/` — empty before this execution; no prior refinement round
  - `tracker/items/WI-0001/item.md` — the fifteen delivered criteria this item's AC6 promises still hold
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's answers on runtime, table syntax and display width, verbatim, so none is re-asked
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's answers on malformed tables, outer pipes and indented tables, verbatim
  - `docs/product/vision.md` v3 — which names the odd-remainder centring question as the one thing `refine` must put to the stakeholder before this item can be Ready
  - `docs/architecture/overview.md` v2 — "How wide a column is", which this item must not duplicate or change
  - `mdtab/table.py`, `mdtab/scan.py` — read to establish what the delivered layout actually does, rather than to judge it: `_render_cell` keeps a cell's trailing padding when the outer-pipe style drops the trailing space, and `line_prefix` is the maximal leading run of space, tab and `>`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **Filed `Q-001` (odd-remainder centring) to the human rather than assuming it.** Rationale: `intake` recorded that it declined to invent the criterion because either split is defensible and the stakeholder had expressed no preference, and `docs/product/vision.md` v3 states in terms that this is `refine`'s to ask. It is a difference visible in every centred cell of every run. Recommendation A (extra column on the right) is offered so the reply can be one word.
  - **Filed `Q-002` (right/centre alignment of the first column of a table with no leading `|`) to the human.** Rationale: it is the R10 combination `alignment marker x outer-pipe style`, which nothing in the record decides. It is a product question and not a design one because every option loses something the stakeholder can see: mdtab ceasing to recognise its own output, one cell position's alignment not being shown, a well-formed table never being tidied, or punctuation appearing that they did not write — and they have already ruled on adjacent trade-offs in `WI-0001/Q-001` and `Q-002` in ways that do not settle this one. The failure mode was confirmed against the shipped tool (`printf ' a | b\n---:|---\nxx | y\n' | python3 -m mdtab` returns its input untouched because the prefixes differ), not reasoned about.
  - **Did not file four other candidate gaps**, deciding each from the record instead and writing the reasoning into `artifacts/refinement-qa.md` under "Settled without asking": where the padding sits relative to WI-0001 AC12's guard spaces (inside the field; forced by AC6 and by AC2's same-display-column promise); that this item changes no column's width (`docs/architecture/overview.md` v2 states the rule is to be kept, and Q-001 option C is where the stakeholder gets to see the only variant that would change one); that a column's marker applies to its header cell too (every renderer does this and the draft criteria already say "in every row"); and that the delimiter row is untouched because WI-0001 AC12 already fills it with dashes across the field. Rationale: the routing test in step 3 — none of the four changes what the software promises, and the stakeholder's attention is the scarce resource in this loop.
  - **Diagnosed AC6 as contradicting AC1, AC2 and AC3** and decided the fix without asking: AC6 will except, by name, the clause of WI-0001 AC12 that fixes padding to the right of the content, and will keep the rest of AC12 explicitly required. `docs/product/vision.md` v3 already promises the alignment markers will be reflected in the padding, so this is a drafting defect in this item, not an open decision.
  - **Did not edit WI-0001's `item.md`.** Its criteria are the record of what was delivered and the item is closed; the supersession is recorded in this item and in the Q&A instead.
  - **Recorded the three diagnosed criterion defects rather than fixing them this round.** Rationale: two of the three touch the same sentences the answers will rewrite, and rewriting them twice would leave a version of the criteria in the history that nobody ever built against.
  - Routed one design question to `plan` via `## Notes` rather than to a person: how the alignment value travels from the delimiter-row parse to the cell renderer.
- **Questions raised:** `Q-001`, `Q-002` — both `addressed-to: human`, both `blocking: true`, filed as one round of two per `spec/question.md`; neither previously asked
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` -> exit 0, 3 items, 8 documents, 0 errors 0 warnings
  - `printf ' a | b\n---:|---\nxx | y\n' | python3 -m mdtab` -> input returned byte-for-byte, confirming Q-002's premise against the shipped tool
  - `printf 'a | b\n---:|---\nxx | yyy\n' | python3 -m mdtab | cat -A` -> `a  | b  $` / `--:|----$` / `xx | yyy$`, the current left-padded layout of the exact table Q-002 is about
- **Gates:**
  - `workspace-valid` -> **pass** (`validate-workspace`, exit 0)
  - `definition-of-ready` -> **fail**, per criterion: R1 pass (frontmatter complete, `type`/`epic`/`priority` set); R2 pass (role, capability and "so that" all present); R3 pass (AC1-AC6, labelled, checkboxes); **R4 fail** (AC1 and AC2 do not place the padding relative to AC12's guard spaces; AC2 has no verdict for an odd remainder; AC6 contradicts AC1-AC3); R5 pass (`## Out of scope` excludes changing an alignment marker and excludes table detection); **R6 fail** (Q-001 and Q-002 are open and blocking — the intended state of a suspended item); R7 pass (`depends-on: WI-0001`, which is `done`/`delivered`); **R8 fail** (`refinement-qa.md` declares `status: agenda`, which R8 explicitly refuses); R9 pass (one coherent change to one padding decision); **R10 fail** (the alignment-marker x outer-pipe-style combination has no stated behaviour anywhere — this is Q-002, and R10 is what made it visible)
  - `criteria-are-decidable` -> **fail** (AC2 names no observation for an odd remainder; AC1 and AC2 do not determine the output bytes; AC6 cannot be evaluated while it contradicts AC1-AC3. AC3, AC4 and AC5 are decidable as written)
  - `qa-recorded-verbatim` -> **skipped** — no answer has been received, so there is nothing to record verbatim yet. `artifacts/refinement-qa.md` declares `status: agenda` precisely so that this cannot be mistaken for a recorded exchange
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` (new)
  - `tracker/items/WI-0002/questions/Q-002.md` (new)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0002/item.md` — `## Notes` gained a "Refinement round 1" section recording the two questions, the three diagnosed criterion defects and their decided fixes, and the design question routed to `plan`
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0002 is suspended on two blocking questions to the stakeholder: how a centred cell divides an odd spare column (carried since intake, and named in the vision as `refine`'s to ask), and what a right- or centre-aligned first column does in a table written without a leading `|`, where the padding becomes leading whitespace and mdtab stops recognising its own output. Everything else the item needed is settled from the record and written into `artifacts/refinement-qa.md`, including the fix for AC6 contradicting AC1-AC3, so the next round rewrites the criteria once.

## 2026-08-28T20:21:33Z — answer-questions v0.3.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer` with two answered human questions; dispatched ahead of `next` because an answered-but-unconsumed question stops the orchestrator on every subsequent run
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `addressed-to: human`, both with `## Answer` filled in
  - `tracker/items/WI-0002/item.md`, `history.md` (the row carrying `resume-to: draft`), `artifacts/refinement-qa.md`
  - `tracker/items/WI-0001/item.md` — AC6 (idempotence), AC12 (cell shape), AC14 (outer pipes), AC15 (prefix)
  - `docs/architecture/adr/` — ADR-0001 to ADR-0006, in particular ADR-0002 (display width) and ADR-0003 (recognition, rule 2)
  - `docs/product/vision.md` (v3), `docs/architecture/overview.md` (v2)
- **Decisions:**
  - `Q-001` — answered by the stakeholder, route *escalated and answered*: the odd spare display column goes on the **right**, so text leans left and mdtab agrees byte-for-byte with `prettier` and `pandoc`. Option A, as recommended. Amended **AC2** to state it rather than leaving it for round 2 — the item is at `draft`, where criteria are not frozen, and an answer that has not reached a criterion has not been given.
  - The same reply states a rule wider than the question — *"Whatever the marker says, that's where the text sits in the cell — every row, every column, no exceptions"* — which independently confirms `Q-002`'s direction. Recorded in `item.md` and in `refinement-qa.md` because it constrains every criterion on this item, not just AC2.
  - `Q-002` — answered by the stakeholder, option A **against** the recommendation of B: the first column of a bare table is aligned like any other, leading whitespace and all; no outer bar is added and the table is not left alone. Added **AC7** to say so, and named in it that WI-0001 AC6 (idempotence) still holds — a second run reproduces such a table byte-for-byte — so AC7 does not put this item in conflict with AC6 of WI-0001.
  - The last clause of that reply — *"that's a fault in the tool and I'd want it sorted rather than worked around"* — is not something WI-0002 can absorb. Filed as **WI-0003** at `draft`, `arose-from: WI-0002/Q-002`, per step 3b: an answer that widens the scope becomes an item, never an amendment to the criteria of the item that was asked about.
  - Did **not** amend ADR-0003, though its rule 2 is what the fault sits in. Relaxing a recognition rule is a design decision with a stakeholder-visible consequence (which runs stop being left alone), it belongs to WI-0003's `plan`, and doing it here would put an architectural decision in a triage step. The stakeholder's sentence is the authorisation ADR-0003's Consequences section requires, and it is quoted in WI-0003.
  - Did **not** apply the three drafting defects `refine` recorded under "Settled without asking" — the guard-space wording, AC6's contradiction with AC1–AC3, and the empty-cell case. They are `refine`'s to apply in round 2 and it deliberately deferred them so the criteria are rewritten once; touching them here would duplicate that rewrite. AC6 therefore still reads as contradicting AC1–AC3 and AC7, which is the state round 2 inherits and is recorded as such in `item.md`.
  - Set `artifacts/refinement-qa.md` to `status: recorded`: DoR R8 reads that field, and the file's own rule is that it becomes `recorded` when the answers are in it verbatim, which they now are. It does not assert the item is Ready — R4, R6 and R10 are `refine`'s to re-audit.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/new-item --id WI-0003 …` → exit 0
  - `python3 .claude/agile-skills/scripts/journal-entry WI-0003 --skill answer-questions` → exit 0
  - `python3 .claude/agile-skills/scripts/journal-entry EP-001 --skill answer-questions` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 mid-execution (`board.stale`, `question.awaiting.none-open`, `item.title.length`, `journal.execution.missing`), each expected and each cleared before this transition
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in a `## Consequences` section opened and checked: `item.md` carries the tie-break in AC2 and the new AC7; `refinement-qa.md` carries both replies verbatim and `status: recorded`; `tracker/items/WI-0003/item.md` exists with `arose-from: WI-0002/Q-002`; `docs/product/vision.md` is v4 with both answers in the body and a change-log row
  - `answered-from-the-record` → **pass** — both answers are the stakeholder's own words in the question files, quoted where they were propagated; no answer of this skill's own was needed, so no ADR was written
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human by this execution; both questions arrived answered
  - `workspace-valid` → **pass** — `validate-workspace` run by this transition
  - `item-resumed-correctly` → **pass** — the suspending row (2026-08-28T20:13:39Z, actor `refine`) records `resume-to: draft`, and this move is `awaiting-answer` → `draft`
  - `a-deferral-is-not-an-answer` → **pass, vacuously** — neither reply defers: each chooses a listed option and gives its reason, and `Q-002` goes further by refusing the cost of the option it chose
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — `answered`, `answered-by: human`, `answered-at`, Consequences filled in
  - `tracker/items/WI-0002/questions/Q-002.md` — the same
  - `tracker/items/WI-0002/item.md` — AC2 amended; AC7 added; the stale "still not decided" note replaced; a round-1 answers section added to `## Notes`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — both replies verbatim; `status: agenda` → `recorded`
  - `tracker/items/WI-0003/` — new work item at `draft`
  - `docs/product/vision.md` — v3 → v4
  - `tracker/items/EP-001/journal.md` — entry recording the scope change
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both blocking questions consumed and propagated; the answer that widened the scope became WI-0003. The item returns to `draft` for `refine` round 2, which now has both stakeholder answers and its own three recorded defects to apply in one rewrite.

## 2026-08-28T20:26:35Z — refine v0.2.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` (highest-ranked runnable item; WI-0003 rejected because `depends-on: WI-0002` is not `done`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md`, `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (round 1, `status: recorded`)
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both answered by the stakeholder
  - `tracker/items/WI-0001/item.md` — AC2, AC6, AC7, AC8, AC12, AC13, AC14, AC15
  - `tracker/items/WI-0003/item.md` — to check this item is not specifying WI-0003's work
  - `docs/product/vision.md` (v4), `docs/architecture/adr/ADR-0002`, `ADR-0003`
  - `.claude/agile-skills/spec/dor-dod.md` §1
- **Decisions:**
  - This is round 2 of the same refinement, not a fresh one: history shows `draft → awaiting-answer → draft`, the suspension was round 1's own two questions, and the agenda was already written. Applied the answers and closed the three recorded defects; did not re-open anything settled.
  - **Rewrote the criteria once**, as round 1 planned: AC1–AC14 replace AC1–AC7. The rewrite is what makes the guard-space defect, the AC6 contradiction and the odd-remainder gap all disappear in one pass rather than three.
  - AC4 carries the stakeholder's tie-break as arithmetic — `floor` before, `ceil` after — because "sits in the middle" has no verdict for an odd remainder and an adjective in a criterion is where the disagreement happens.
  - AC14 (was AC6) now excepts by name the one clause of WI-0001 AC12 this item supersedes, and lists what of AC12 is still required. The old wording asserted every WI-0001 criterion held, which contradicted this item's whole purpose.
  - Defined "field" once in the preamble instead of qualifying every criterion with where the guard spaces go. AC7 then makes the guard spaces checkable on their own.
  - **Asked the stakeholder nothing.** Two new points arose and both were settled from their own words rather than filed: how a marker is read from a delimiter cell (AC1) — mechanical, and the recognition of a delimiter row is WI-0001's and unchanged, confirmed by feeding `| : | --- |` to the shipped tool and watching the run come back untouched; and what a right-aligned *last* column does in a table with no trailing `|` (AC11) — the same shape as `Q-002`, which they answered by accepting the cosmetic cost, and cheaper, since no leading whitespace is produced. Both recorded `[assumed]` in the Q&A with the deferral they rest on.
  - Enumerated the R10 combinations as criteria rather than leaving them implicit: marker × outer-pipe style (AC10, AC11), × prefix (AC12), × empty cell (AC8), × non-ASCII width (AC5), × delimiter row (AC9), × an unrecognised run (AC13).
  - One combination is left deliberately unconstrained and is named in `## Notes` with who left it so: a right-aligned first column *inside a blockquote prefix* produces the same recognition failure as AC10 by a different route. It belongs to WI-0003, and constraining it here would pre-empt an item that has not been refined.
  - Added a third and fourth exclusion to `## Out of scope`: changing which runs mdtab recognises (WI-0003's), and diagnostics.
- **Questions raised:** none this round. Round 1's `Q-001` and `Q-002` are answered and their Consequences now name where each answer landed after the renumbering.
- **Commands:**
  - `printf '| a | b |\n| : | --- |\n| xxxx | y |\n' | python3 -m mdtab` → run reproduced byte-for-byte (a delimiter cell with no `-` is not a delimiter row)
  - `printf '| a | b |\n|  :---  | ---:  |\n| xxxx | y |\n' | python3 -m mdtab` → `|:-----|--:|`, confirming AC9's example and that spaces around a marker are tolerated
  - `printf '| a |  |\n| --- | :---: |\n| xxxx |  |\n' | python3 -m mdtab` → `|   |` over `|:-:|`, confirming AC8's example
  - `printf 'a | bbbb\n---|---\nxxxx | y\n' | python3 -m mdtab | cat -A` → trailing padding is kept today, which is what AC11 must preserve
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, and again inside this transition)
  - `definition-of-ready` → **pass**, criterion by criterion: R1 pass (frontmatter complete, validator exit 0); R2 pass (story names role, capability, outcome — unchanged); R3 pass (AC1–AC14 labelled checkboxes); R4 **was fail, now pass** — the three defects are fixed: the guard-space ambiguity by the preamble and AC7, the odd remainder by AC4's arithmetic, the AC6 contradiction by AC14's named exception; R5 pass (four exclusions); R6 **was fail, now pass** (both questions `answered`, none open); R7 pass (`depends-on: WI-0001`, `done`, merged `5138b52`); R8 **was fail, now pass** (`refinement-qa.md` is `status: recorded` with both replies verbatim); R9 pass (one change to where content sits in a field it already has; the separable part became WI-0003); R10 **was fail, now pass** (combinations enumerated above, the one left open named in `## Notes`)
  - `criteria-are-decidable` → **pass** — each of AC1–AC14 names the document to feed and the output to observe; four of the observations were run against the shipped tool during this execution and are quoted in the Q&A, so the expected outputs are measured rather than imagined
  - `qa-recorded-verbatim` → **pass** — `refinement-qa.md` carries both stakeholder replies word for word under "Round 1", each tagged, and round 2's two new points tagged `[assumed]` with the deferral they rest on. Nothing was paraphrased into agreement; `Q-002` in particular is recorded as chosen *against* the recommendation.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — criteria rewritten AC1–AC14; two exclusions added; `## Notes` rewritten around what the stakeholder settled, what was assumed, what goes to `plan`, and what WI-0003 should pick up
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 2 appended: what each answer became, the three defects closed, two new `[assumed]` entries with evidence, and the per-criterion DoR audit
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — Consequences updated to name the criteria the answers now live in
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Fourteen criteria, every one with a stated observation, both stakeholder answers applied, nothing left open that this item owns.

## 2026-08-28T20:30:51Z — plan v0.3.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` (the only runnable item; WI-0003 is behind it on `depends-on`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC14, the preamble defining "field", and `## Notes`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — nine `[assumed]` entries, especially §1 (guard spaces), §3 (widths do not change) and round 2's §8 and §9
  - `tracker/items/WI-0002/history.md`, `questions/Q-001.md`, `Q-002.md`
  - `tracker/items/WI-0003/item.md` — to keep this plan out of its scope
  - `docs/architecture/overview.md` (v2), `docs/product/vision.md` (v4)
  - ADR-0001 (stdlib-only), ADR-0002 (display width), ADR-0003 (recognition and punctuation), ADR-0004 (bytes and line endings), ADR-0005 (tests from the standard library), ADR-0006 (non-UTF-8 fixtures)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are already filled in by WI-0001's plan
  - source: `mdtab/table.py` (all of it), `mdtab/width.py`, `mdtab/filter.py`, `mdtab/scan.py` (prefix and fence handling), `tests/test_fixtures.py`, `tests/test_units.py`, `tests/fixtures/` (the 21 pairs)
- **Decisions:**
  - **Alignment is one value per column, computed once from the delimiter row beside the widths** (`column_alignments(rows)`), rather than re-derived inside the renderer per cell. From the documents: the overview's one-place-per-rule list is the project's stated shape, and a second reading of the delimiter row would be a second place the marker rule lives. ADR-0007 §Decision 1.
  - **The padding moves inside the field; the guard spaces and `_column_widths` do not move.** From the documents plus the criteria: WI-0001 AC12 fixes the cell shape and AC6 (idempotence) forces the two width rules the overview names; AC6 and AC7 of this item say in terms that neither may change. This is what makes AC10 and AC11 fall out of the arithmetic instead of being special cases. ADR-0007 §Decision 2 and 3.
  - **The odd centred column goes right, and the ends of a bare row are aligned anyway** — asked and answered by the stakeholder in round 1 (`Q-001`, `Q-002`), not re-decided here. Recorded in ADR-0007 with the options they were shown, because a design document that omits the rejected options documents a conclusion rather than a decision.
  - **ADR-0007 exists mainly for what the decision costs:** mdtab may now emit a bare table it will not recognise. That is a property the tool had and no longer has, it is invisible at runtime because there are no diagnostics, and WI-0003 is the item that restores it. Recorded in the ADR and in a new section of the overview so a reader meets it before they meet the symptom.
  - **Assumed, reversibly** (`## Assumptions` in the plan): the three alignments are the strings `"left"`, `"right"`, `"centre"`; `column_alignments` is public so `tests/test_units.py` can drive it as it drives the other rules; and one fixture carries all four rejection routes for AC13. Each is one file to reverse and changes no output byte.
  - **Nothing was asked of the stakeholder.** Every open point this plan met was either answered in round 1, settled in the Q&A, or a reversible representation choice. The one place I would have asked — whether to accept unrecognisable output — they had already been asked and had answered.
  - **No bug filed.** Planning found no defect in delivered behaviour: the recognition gap does not exist until this item ships, which is why it is WI-0003 at `draft` rather than a bug against WI-0001.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 55 tests, OK (the baseline this item must not break)
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `printf '| a | b |\n| : | --- |\n| xxxx | y |\n' | python3 -m mdtab` → unchanged, confirming a dashless delimiter cell is not a delimiter row before AC1 was written against it
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 2 documents
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, and again inside this transition)
  - `every-criterion-is-addressed` → **pass** — the mapping table in `plan.md` has a row for each of AC1–AC14, each naming the step that implements it and the fixture or test that demonstrates it; no AC maps to "tests" alone, and no step exists that no AC maps to
  - `project-commands-resolved` → **pass** — `commands.test` and `commands.lint` were filled in by WI-0001's plan and both were run during this execution, exit 0 each; `commands.build` stays `null`, which is honest for a package with no build step (ADR-0001)
  - `decisions-recorded` → **pass** — the plan's `## Decisions and ADRs` table lists five choices: three point at ADR-0007, two at the stakeholder's answers it cites, and the three representation choices point at `## Assumptions` with what reversing each costs
  - `plan-is-executable-without-you` (advisory) → **pass** — read back cold, each of the eight steps names the file, the function and what is true afterwards; step 1 states the four marker cases explicitly and step 2 gives a worked example of the centred case
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 over ADR-0007 and the overview; the first run failed on a citation to `plan.md` before it existed, and passed once it did)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — problem, approach, eight steps, the AC mapping, three assumptions, three risks
  - `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md` (new, v1)
  - `docs/architecture/overview.md` — v2 → v3: the new one-place-per-rule entry and the section recording the recognition property this costs
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. The change is one new function and one changed renderer in `mdtab/table.py`, eight fixtures and two test classes; nothing else in `mdtab/` is touched, and the recognition rules come out of this item unchanged for WI-0003 to alter.

## 2026-08-28T20:33:03Z — implement v0.2.2 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`; dispatched by `next` as the only runnable candidate (WI-0001 done, WI-0003 blocked on this item).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the fourteen acceptance criteria and the out-of-scope list
  - `tracker/items/WI-0002/artifacts/plan.md` — eight steps, the AC mapping, the assumptions and the risks
  - `tracker/items/WI-0002/history.md` — five rows; the last is `ready → planned` by `plan`, so this is a fresh start, not a resume
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, both propagated into `item.md` before `plan` ran
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, branch prefix `wi/`, commit subject convention
  - `mdtab/table.py` — the layout the plan changes (`_render_cell`, `_render_row`, `_column_widths`, `lay_out`)
  - `tests/test_fixtures.py`, `tests/test_units.py`, `tests/fixtures/` — the shipped suite AC14 requires still hold
- **Decisions:**
  - None yet. The plan is executed as written; anything it does not decide is recorded in the closing entry or escalated.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0 (branched from `571cac2`)
- **Gates:**
  - `tests-pass` → **skipped** (not yet run; no change has been made — the closing entry reports it)
  - `lint-clean` → **skipped** (not yet run, same reason)
  - `workspace-valid` → **skipped** (not yet run, same reason)
  - `every-criterion-has-a-test` → **skipped** (no test written yet)
  - `commits-reference-the-item` → **skipped** (no commit on the branch yet)
  - `claims-are-sourced` → **skipped** (nothing written yet to source)
- **Artifacts:**
  - branch `wi/WI-0002` at `571cac2`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started on a fresh branch off `main`. No code has changed yet; the closing entry at `in-progress → verifying` is the one that reports the work.

## 2026-08-28T20:41:23Z — implement v0.2.2 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`, opened by this skill's own entry at 2026-08-28T20:33:03Z; the plan's eight steps are complete.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC14
  - `tracker/items/WI-0002/artifacts/plan.md` — steps 1–8, the AC mapping, the assumptions and the risks
  - `tracker/items/WI-0002/history.md`, `questions/Q-001.md`, `questions/Q-002.md`
  - `docs/architecture/adr/ADR-0007-*.md` and `docs/architecture/overview.md` (v3) — checked against what was built; neither needed an edit
  - `mdtab/table.py`, `tests/test_units.py`, `tests/test_fixtures.py`, `tests/fixtures/*`, `.gitattributes`
  - `tracker/project.yaml`
- **Decisions:**
  - Executed the plan's steps 1–3 verbatim: `column_alignments` reading the delimiter row, `_render_cell` distributing its existing padding, `_render_row` and `lay_out` threading one alignments list. `_column_widths` and the four recognition rules were not touched.
  - **Updated `tests/fixtures/basic-ascii.out.md` and narrowed one assertion in `test_ac12_every_cell_has_exactly_one_space_against_each_pipe`.** The plan asserts WI-0001's suite runs unchanged; it does not, because `basic-ascii`'s delimiter row is `|---|:---|---:|` and its `id` column is therefore right-aligned. Both places encode the single clause of WI-0001 AC12 that WI-0002 AC14 excepts by name and AC3 supersedes. Judged mine to make rather than a question, on this skill's own test: the behaviour is covered by an acceptance criterion (AC3), and the change is two lines in one fixture and four in one test — cheap to reverse. WI-0001's `item.md` was not edited and no criterion of either item was changed. Recorded as deviation 1 in `impl-report.md`, flagged there as the one judgement a reviewer should check.
  - Added `align-leading-pipe-only` and `align-list-indent` beyond the plan's fixture list, because AC11's own worked document has no leading pipe while the plan's description of that fixture does, and because AC12 names a list-indented table the plan's step 4 omitted. Deviations 2 and 3.
  - Strengthened AC4's unit test with two further documents after a mutation check showed AC4's own document cannot tell a centred cell from a left-padded one when the spare space is a single column. Deviation 5.
  - Decided **not** to work around the recognition fault AC10 creates, in either form; the AC10 unit test asserts `lay_out` returns `None` for mdtab's own output and names WI-0003 in its docstring.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
  - `python3 -m unittest discover -s tests -t .` → 0, "Ran 65 tests ... OK" (run after every step; three failures after the code change, all from the superseded clause, all resolved before the first commit)
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, "all 3 commit(s) on main..wi/WI-0002 name WI-0002"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0, "checked no documents changed since main"
  - `python3 -m mdtab < tests/fixtures/align-no-trailing-pipe.in.md | awk '{print length($0)}'` → `11`, `11`, `11` (AC11)
  - `python3 -m mdtab < tests/fixtures/align-markers.in.md | sed -n '1p;3,4p' | grep -n '|[^ ]'` → 1, no match (AC7)
  - mutation check, twice: `_render_cell` reduced to WI-0001's left-only padding → six named tests fail
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0 on branch head `2829b50`; 65 tests)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0; 4 items, 9 documents, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (all fourteen mapped to a named test function or an exact command in `impl-report.md`'s evidence table; the mutation check confirms none passes against the unchanged renderer)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 3 commits)
  - `no-unplanned-scope` (advisory) → **pass** (`git diff main --stat`: `mdtab/table.py`, the two test modules, twenty new fixture files, `basic-ascii.out.md`, and this execution's tracker files; the four hunks that trace to a criterion rather than to a plan step are deviations 1–3 and 5)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0; no file under `docs/` changed, so it checked none)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md`
  - branch `wi/WI-0002`, commits `571cac2..2829b50` — `3647766` the renderer and its unit tests, `34c0c73` the ten fixture pairs and their registration, `2829b50` the report
  - `mdtab/table.py`, `tests/test_units.py`, `tests/test_fixtures.py`, `tests/fixtures/basic-ascii.out.md`, and twenty new files under `tests/fixtures/`
- **Status:** `in-progress` → `verifying`
- **Result:** mdtab now places a cell's padding where the delimiter row's marker says, in every row and every column, with the column widths and the guard spaces untouched and the four recognition rules unchanged. All seven gates pass on the branch head. The one thing verification should look at first is deviation 1: two places in WI-0001's shipped suite encoded the padding-position clause AC14 excepts, and this execution moved them.

## 2026-08-28T20:47:56Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`; dispatched by `next` as the only runnable candidate.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC14, read in full **before** the implementation report, so each check was derived from the criterion rather than from what was built
  - `tracker/items/WI-0002/history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`
  - `tracker/items/WI-0001/item.md` (its fifteen criteria, which AC14 refers to) and `tracker/items/WI-0001/questions/Q-005.md`
  - `docs/architecture/adr/ADR-0007-*.md`
  - the code on `wi/WI-0002` at `a8b5a4bb2b2c5ecd4baed6bb959b88233d7ef80a`: `mdtab/table.py`, `git diff main -- mdtab/`, `git diff main -- tests/`
  - `tracker/project.yaml`
- **Decisions:**
  - **AC14 recorded as `pass` on its substance, with `Q-003` filed rather than a send-back or a silent tick.** Its two clauses cannot both hold: it excepts the clause of WI-0001 AC12 that fixes padding to the right of the content, and it also requires WI-0001's shipped suite to run *unchanged* — but two places in that suite encode precisely the excepted clause, both reached through the fixture `basic-ascii`, whose delimiter row is `|---|:---|---:|`. The substantive claim was checked independently, on documents written here, and holds: all fifteen of WI-0001's criteria are satisfied on marker-bearing input. A send-back was rejected because there is nothing `implement` could do differently — the criterion is self-contradictory, not the code. Following `WI-0001/Q-005`, which was the same shape in this workspace: non-blocking, so the item proceeds, and `next` step 4 puts `answer-questions` ahead of `review-close`.
  - **No bug item filed for the recognition fault AC10 creates.** Test applied: does an acceptance criterion of *this* item say the behaviour should be different? AC10 says the opposite — it requires it, and puts it out of scope explicitly. WI-0003 already exists at `draft` with `arose-from: WI-0002/Q-002`. A bug would duplicate it.
  - **No criterion judged ambiguous other than AC14**, and AC14 was not left at `ambiguous` because its claim is decidable and was decided; only its evidence recipe is impossible. That distinction is stated in the report and in `Q-003`.
  - Verified with documents written in this execution under `/tmp/vwi2/`, not with the item's own fixtures, so a wrong fixture could not carry a criterion.
  - Recorded in `## Not verified, and why` that this verification's independence is weaker than the pipeline intends, because the same session ran `implement` earlier this turn, together with the three defences used against that.
- **Questions raised:** `Q-003` (architect, non-blocking) — how AC14's checking clause should be worded so it and AC14's own exception clause are jointly satisfiable.
- **Commands:**
  - `git rev-parse HEAD` → 0, `a8b5a4bb2b2c5ecd4baed6bb959b88233d7ef80a`
  - `python3 -m unittest discover -s tests -t .` → 0, "Ran 65 tests in 0.082s ... OK"
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1 once (`board.stale`, after `Q-003` was filed), then 0 after `board-gen`
  - `python3 .claude/agile-skills/scripts/board-gen .` → 0, "wrote tracker/board.md"
  - AC1–AC13: fourteen `python3 -m mdtab < …` runs over documents written in this execution, each with its output quoted in the report; plus `diff`, `cmp`, `awk '{print length($0)}'`, `grep -n '|[^ ]'`, `grep -n ' $'`, and two Python programs measuring display columns and codepoints
  - AC14 substance: one Python program re-checking WI-0001's fifteen criteria on marker-bearing documents → every check true
  - sensitivity: three mutations of `mdtab/table.py`, each followed by `python3 -m unittest discover -s tests -t .` → 13, 16 and 4 failures; `cp` restore after each; `git status --short` empty afterwards and the suite back to "OK"
- **Gates:**
  - `tests-pass` → **pass** (exit 0 on `a8b5a4b`, 65 tests, run in this execution)
  - `lint-clean` → **pass** (exit 0)
  - `workspace-valid` → **pass** (0 errors, 0 warnings, after `board-gen` resolved the `board.stale` error that filing `Q-003` caused)
  - `every-criterion-independently-checked` → **pass** (all fourteen rows of the report's Criteria table name a command run here and its actual output; none cites `impl-report.md`; none uses one of this item's fixtures as its document)
  - `negative-cases-exercised` → **pass** (seven classes triggered: the four rejection routes, an empty cell and an all-empty column, both ends of a row with no outer pipe, mdtab refusing its own output, a delimiter cell with no dash, non-ASCII and undecodable bytes, and CRLF/no-final-newline)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (three mutations, each caught; the centre-rounding mutation is caught only by the AC4 test and the `align-centre-odd` fixture)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md`
  - `tracker/items/WI-0002/questions/Q-003.md` (architect, non-blocking, open)
  - `tracker/items/WI-0002/item.md` — all fourteen criteria ticked, each against a command in the report
  - `tracker/board.md` regenerated
  - no bug item filed
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 meets all fourteen of its acceptance criteria against branch head `a8b5a4b`, demonstrated with commands run here on documents written here. AC14 passes on its substance only: its "run WI-0001's suite unchanged" clause contradicts its own exception clause, which is `Q-003` to the architect, non-blocking, and should be answered before `review-close` reads AC14 against D2.

## 2026-08-28T20:52:15Z — answer-questions v0.3.1 — architect

- **Item:** WI-0002
- **Trigger:** `Q-003` open and addressed to the architect; dispatched by `next` step 4, which precedes the status owner (`review-close`) at step 5. The item was not suspended — the question is non-blocking — so there is no `resume-to` to honour.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-003.md` — the only open question on this item; `Q-001.md` and `Q-002.md` re-read and confirmed still `answered` with their consequences in place
  - `tracker/items/WI-0002/item.md` — AC1–AC14, and `## Notes`
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md` (deviation 1), `verify-report.md` (the AC14 row and `## Not verified, and why`)
  - `tracker/items/WI-0002/history.md` — five rows plus this execution's predecessors; no suspension row for `Q-003`
  - `tracker/items/WI-0001/item.md` (AC12 and AC14 as amended in round 3) and `tracker/items/WI-0001/questions/Q-005.md` — the precedent, answered the same way
  - `docs/architecture/adr/ADR-0007-*.md` v1 (§Decision 2 and §Consequences), and `docs/architecture/overview.md` v3 (`## Rules that live in exactly one place`, `## A property the tool no longer has`) — checked so that the answer could not contradict a recorded decision
  - `git diff main -- tests/fixtures/basic-ascii.out.md tests/test_fixtures.py` — to establish that the two named places are the whole of the change to WI-0001's shipped suite, rather than take `impl-report.md`'s word for it
- **Decisions:**
  - **`Q-003` answered: option A — amend AC14's checking clause, not its substance.** Route 1 of `spec/question.md` §3, an answer from an existing document: AC14's own first half already excepts "the single clause of its AC12 that fixes a cell's padding to the right of its content", and the two places named are that clause in the only two forms WI-0001's suite states it. No ADR was written because none is needed — ADR-0007 §Decision 2 already fixes where the padding goes, and this answer contradicts nothing in it. B was rejected because dropping the word "unchanged" also drops the guarantee the clause exists for; C because reverting the two places would force an edit to `basic-ascii.in.md`, a larger change to a WI-0001 fixture than the two output cells it avoids; D because leaving a known-false criterion in the record is what `WI-0001/Q-005` was filed to stop happening a second time.
  - **An acceptance criterion was amended, and it is named as such.** What changed is a *check*, not a *requirement*: no clause about what the tool must do was touched, no behaviour, test or fixture changed as a result, and AC14 stays ticked on `verify`'s own evidence. The two places the amended clause names had already been updated by `implement` (its declared deviation 1) and re-verified independently by `verify` before the question was filed, so this is not the target being reshaped around the arrow — it is a sentence that described an impossible check being made to describe a possible one. Had the amendment altered what the tool must do, the correct move would have been to escalate to the stakeholder.
  - **Not escalated.** None of `spec/question.md` §4's four conditions applies: intent is recorded (AC14's own exception clause, and the stakeholder's *"whatever the marker says, that's where the text sits in the cell — every row, every column, no exceptions"*, `WI-0002/Q-001`); the change is a sentence and is reversible; it contradicts no ADR; the record is not silent.
  - **No new item filed and no bug filed.** The answer widens nothing — the delivered code already does what the amended text says — and it reveals no defect in delivered behaviour. The recognition fault AC10 creates is required by AC10, recorded in ADR-0007, and already owned by WI-0003.
  - **`verify-report.md` and `impl-report.md` deliberately left alone.** A report is the record of what one execution found, and rewriting it afterwards would destroy the trail this answer rests on.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 1 (`board.stale`, after the question file changed), then 0 after `board-gen`
  - `python3 .claude/agile-skills/scripts/board-gen .` → 0, "wrote tracker/board.md"
  - `git diff main -- tests/fixtures/basic-ascii.out.md tests/test_fixtures.py` → 0; the whole diff is two cells in the fixture, one narrowed assertion, and the additive `ALIGNED`/`UNTOUCHED` registration
  - `grep -c` over each file named in `## Consequences`, to confirm the change is present rather than intended → 1 for each of the five edits, 0 unticked criteria remaining
- **Gates:**
  - `answer-is-propagated` → **pass** (each of the three files named in `Q-003`'s `## Consequences` was opened and the change confirmed present: `item.md`'s amended AC14 clause and its new `### AC14's checking clause amended, round 3` section; `plan.md`'s step 5, its AC14 mapping row, and its `## Risks` bullet; `Q-003` itself. `## Consequences` also names, with reasons, the four files deliberately not changed)
  - `answered-from-the-record` → **pass** (the answer cites AC14's own exception clause, ADR-0007 §Decision 2, `WI-0002/Q-001`'s recorded stakeholder sentence, `verify-report.md`'s independent re-check of WI-0001's fifteen criteria, and the `WI-0001/Q-005` precedent with `review.md`'s "the wording of AC12 is what should change, not the code". The record was not silent, so no new ADR was written)
  - `escalation-is-justified` → **skipped** (nothing was escalated; no question was re-addressed to the human. The reason it was not is recorded above against all four of `spec/question.md` §4's conditions)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 4 items, 9 documents, 0 errors, 0 warnings, after `board-gen`)
  - `item-resumed-correctly` → **skipped** (`Q-003` is non-blocking, so it never suspended WI-0002: there is no `awaiting-answer` row in `history.md` for it and therefore no `resume-to` to match. The item stays at `in-review`, where `verify` left it. This is the same shape as `WI-0001/Q-005`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred anything; `Q-003` was addressed to the architect and answered here, not put to a person)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-003.md` — `## Answer` and `## Consequences` written; `status: answered`, `answered-at: 2026-08-28T20:49:15Z`, `answered-by: answer-questions`
  - `tracker/items/WI-0002/item.md` — AC14's checking clause amended; `## Notes` gains `### AC14's checking clause amended, round 3`. No other criterion edited, none unticked
  - `tracker/items/WI-0002/artifacts/plan.md` — step 5 extended with the two places that had to move; the AC14 mapping row no longer claims the suite runs unchanged and records the ten-versus-eight fixture count as `implement`'s declared deviation; the `## Risks` bullet gains the second face the plan missed
  - `tracker/board.md` regenerated
  - no ADR created, no document version bumped, no new item filed, no bug filed
- **Status:** `in-review` → `in-review` (unchanged — the question was non-blocking, so nothing was suspended and nothing is resumed)
- **Result:** `Q-003` answered from the record with option A: AC14's checking clause now says what it actually requires, and its substance is untouched. No behaviour, test or fixture changed as a result, AC14 stays ticked on `verify`'s evidence, and WI-0002 stays at `in-review` with no question open — so `next` will now dispatch `review-close`.

## 2026-08-28T21:03:12Z — review-close v0.5.0 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable candidate — WI-0003 is behind this item on `depends-on`, and no question is open anywhere in the workspace.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC14, the "field" preamble, `## Out of scope`, and the whole of `## Notes` including the round-3 AC14 amendment
  - `tracker/items/WI-0002/history.md` — eight rows, chaining without a gap, last row matching the item's status
  - `tracker/items/WI-0002/journal.md` — all nine entries in full
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md` (five deviations, `## What I did not do`), `verify-report.md` (fourteen criteria, `## Not verified, and why`), `refinement-qa.md`
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, and the files each `## Consequences` names
  - `tracker/items/WI-0001/item.md` and `artifacts/review.md` — AC12 and AC14 as amended, and the precedent for accepting a minor record finding rather than sending an item back
  - `tracker/items/WI-0003/item.md` — to check that what this item leaves undone is owned
  - the diff `main..wi/WI-0002`: `mdtab/table.py` hunk by hunk, `tests/test_units.py`, `tests/test_fixtures.py`, all ten new fixture pairs and `tests/fixtures/basic-ascii.out.md` read as bytes with `cat -A`
  - `docs/architecture/adr/ADR-0007-*.md` v1, `docs/architecture/overview.md` v3, `docs/product/vision.md` v4, and ADR-0002/ADR-0003 for the claims this item's behaviour touches
  - `tracker/project.yaml` — trunk, `commands.test`, `commands.lint`, the commit convention
- **Decisions:**
  - **Accepted, and merged.** All twelve Definition of Done criteria pass, recorded one by one in `review.md`. Every hunk in the code diff maps to a criterion and a plan step, and the ten functions the item must not have touched were checked byte-identical to `main` by extracting each from both revisions — not inferred from the diff's shape.
  - **Finding 1 accepted, not sent back: `docs/product/vision.md` v4 states the recognition property in the present tense one clause before conceding it.** *"A table mdtab has laid out is a table mdtab still recognises: making that true where those leading spaces appear is WI-0003…"* is true read whole and false read to the colon, and this item is what makes it false. Rationale: nothing in it is wrong about behaviour, the sentence carries its own correction, and a send-back would re-run fourteen uncontested criteria to reorder one clause. The wording that would settle it is in `review.md`, and both the finding and the edit are in `item.md`'s `## Notes` where WI-0003 will find them.
  - **Finding 2 accepted, not sent back: ADR-0007 §Decision 1 and `column_alignments`' docstring both claim the delimiter row's markers are read in exactly one place, and three places read them.** The claim each is actually making — that the *alignment* is derived once — holds, and I checked it (`column_alignments`: one definition, one call site). `_column_widths:166` and `_render_delimiter:202` read the same cell for the minimum-width rule and for re-rendering, both WI-0001's and both unchanged here. The duplication an absolute would warn about does not exist, so the defect is two missing words, not a design fault.
  - **Both findings are the same shape, and the review says so.** Each puts an absolute first and its qualification second — true to the end of the sentence, false quoted at the comma, which is F-001's shape. Two in one item is recorded as a pattern to watch rather than two unrelated acceptances.
  - **No bug item filed.** The recognition fault AC10 creates is required by AC10, chosen by the stakeholder with the cost in front of them (`Q-002`), recorded in ADR-0007, and owned by WI-0003 at `draft`. A bug would duplicate it. Nothing else in the diff or the probes was a defect.
  - **`lint-claims` over the whole tree fails on a document this item never touched** — two `claim.unsourced` errors in ADR-0003 where a backticked question ID `Q-002` is treated as a named code object. Judged a mis-classification in the pipeline's own gate, not an unsourced claim in mdtab's record: the contracted gate form (`--changed-since main`) passes, ADR-0003 was delivered under WI-0001, and patching `.claude/agile-skills/scripts/` from inside a work item is what WI-0001's review already declined to do. Reported to the toolkit owner instead of filed as an item.
  - **Six adversarial probes of my own** beyond the criteria — a bare *centred* first column (ADR-0007 names `:---:` and no criterion demonstrates it), an escaped `|` in a right-aligned cell, a CRLF document, an all-empty `---:` column, a document with no final newline, and an undecodable byte in a right-aligned column. None is a finding; all six are in `review.md`.
  - **Two structural observations recorded rather than raised as findings:** `padding` cannot go negative because `_column_widths` floors every column at `2 + max(content)`, and `_render_row` indexes `alignments[column]` on the assumption recognition rule 1 has already enforced. Both are places WI-0003 could break something, so they are written down where it will look.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → 0, "verified at a8b5a4bb; wi/WI-0002 has moved to 308145b0 but only the record changed (7 file(s) under tracker/ or docs/)"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, "all 6 commit(s) on main..wi/WI-0002 name WI-0002"
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0; `lint-claims .` (whole tree, not the contracted form) → 1, two errors in ADR-0003, recorded as finding 3
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0 (and once 1, `item.outcome.premature`, when `outcome: delivered` was written by hand before the status moved — corrected by letting `transition --outcome` write it)
  - `git worktree add --detach /tmp/wi2-trial main` → 0; `git -C /tmp/wi2-trial merge --no-ff wi/WI-0002` → 0, trial head `baf9fe88`
  - `python3 -m unittest discover -s tests -t .` **in the trial worktree** → 0, "Ran 65 tests in 0.089s … OK"
  - `python3 -W error -m compileall -q mdtab tests` **in the trial worktree** → 0
  - `git worktree remove --force /tmp/wi2-trial` → 0; `git rev-parse main` → `571cac2a`, unchanged from before the trial
  - claim audit: twelve claims, each opened against the code or behaviour it cites — four-marker layouts compared for pipe positions, both bare-table cases run twice through the tool with `cmp` and `lay_out(...) is None`, `grep -n 'startswith(":")' mdtab/*.py`, and a function-by-function byte comparison of ten functions against `git show main:mdtab/table.py`
  - six probes: `python3 -m mdtab` on a centred bare table, an escaped pipe, a CRLF document, an all-empty `---:` column, a document with no final newline, and an undecodable byte
- **Gates:**
  - `definition-of-done` → **pass** — all twelve criteria recorded one by one with their evidence in `review.md`'s `## Definition of Done` table. D7 and D12 pass *with findings 1 and 2*, which are recorded rather than waved through
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the two commits after the verified one touch only `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 6 commits — run before the merge, because merging first empties the range it inspects)
  - `tests-pass-on-the-merge-result` → **pass** (`commands.test` and `commands.lint` both exit 0 inside the detached trial worktree, on the merge commit rather than on the branch head)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 4 items, 9 documents)
  - `record-is-reconstructible` → **pass** — from the tracker, `docs/` and `git log --grep WI-0002` alone: *what was built and why* is `item.md`'s story with ADR-0007's four rejected options; *which skill decided what* is nine journal entries naming skill, version and persona, with the two stakeholder decisions attributed to them rather than to `plan`; *what questions arose* is `Q-001`/`Q-002` to the human and `Q-003` to the architect, each with `## Consequences` naming files I opened; *what verification found* is fourteen criteria with the commands and their actual output, plus four declared gaps
  - `claims-are-sourced` → **pass** in its contracted form (`lint-claims --changed-since main` exit 0). The whole-tree run's two errors are finding 3 and belong to the gate, not to this item
  - `epic-sign-off` → **skipped** — this execution closes a work item, not an engagement. EP-001 is not at rest until WI-0003 stops, so no sign-off question is due yet and none was filed
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new) — what was examined, the hunk-to-criterion table, twelve audited claims, the twelve Definition of Done rows, three findings, six accepted gaps, the verdict
  - `tracker/items/WI-0002/item.md` — `outcome: delivered`; `## Notes` gains three sections: what the review accepted rather than sent back, what WI-0003 must edit when it lands, and the gaps accepted at close
  - merge commit on `main` merging `wi/WI-0002`
  - no bug item filed, no question filed, no document under `docs/` changed by this execution
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is accepted and closed as delivered. mdtab now places each cell's padding where the delimiter row's marker says — in the header row and every body row, measured in display columns, without moving a guard space, changing a column's width or rewriting a marker. Two findings were accepted rather than sent back, both sentences that state an absolute before their own qualification, and both are recorded in `## Notes` for WI-0003, which is now the only item left in EP-001 and becomes runnable at `draft` the moment this merge lands.
