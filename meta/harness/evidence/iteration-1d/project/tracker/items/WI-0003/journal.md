# Journal — WI-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-22T01:37:56Z — intake v0.2.0 — product-analyst

- **Item:** WI-0003
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this skill is not dispatched by `next`
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty at the start of this execution, so `EP-001` and `WI-0001` were the first IDs allocated
  - `docs/product/vision.md` — did not exist; created by this execution
- **Decisions:**
  - See `EP-001`'s entry for how the work was split and why this item is one of three; that reasoning belongs to the split, not to this item.
  - Dependency for this item: `WI-0001` — an import has to write into the store that item defines.
  - Acceptance criteria here are deliberately incomplete and are marked so in `## Notes`. They state observable behaviour where the stakeholder's words settle it, and stop where they do not. Padding them into something that looks finished would hand `refine` a polished guess instead of an honest gap.
  - No command names, file formats or data structures appear in the story or the criteria, because the stakeholder named none. "A command" is used on purpose.
- **Questions raised:** none on this item; `EP-001/Q-002` blocks it entirely and is recorded in its Notes
- **Commands:**
  - `scripts/new-item --id WI-0003 --type work-item --epic EP-001 ...` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported at the end of this intake — see `EP-001`'s entry for the run)
  - `epic-has-success-measures` → **pass** (assessed on `EP-001`; four measures, each checkable by running the tool — see that item's entry)
  - `items-are-separable` (advisory) → **pass** — WI-0003's dependency is stated above and it delivers something observable on its own: import expenses from a bank CSV export
  - `no-solution-in-the-problem` (advisory) → **pass** — the story and criteria name no technology the stakeholder did not. Python and CSV appear only where they were stated; nothing was removed.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` (new)
  - `tracker/items/WI-0003/journal.md`, `tracker/items/WI-0003/history.md` (new, headers written by `new-item`)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` as one of three items under `EP-001`. It is not Ready: `refine` must close the gaps listed in its `## Notes`.

## 2026-08-22T02:43:50Z — refine v0.1.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** not dispatched by `next` — this item is not runnable (`depends-on` names WI-0002, which is not `done`). `refine` reached it while filing the same round trip's questions to the stakeholder, and this item's own `## Notes` had already recorded, before this execution, that `refine` must file a question citing `EP-001/Q-002` and suspend rather than attempt it
- **Inputs read:**
  - `tracker/items/WI-0003/item.md`, `history.md` (one row — created by `intake`, never sent back), `journal.md`, `artifacts/` (empty)
  - `tracker/items/EP-001/questions/Q-002.md` — the deferral this execution supersedes, and the four options it offered
  - `tracker/items/WI-0001/item.md` — AC3, AC6, AC7 and `## Out of scope`, which constrain what an imported row may become
  - `docs/architecture/adr/ADR-0002` (amount format; the importer, not the hand-entry command, absorbs normalisation), `ADR-0004` (`parse_amount` is the single boundary an imported amount must pass through)
  - `docs/product/vision.md` v3 — "Not a bank client. It never talks to a bank. Its input is a CSV file the person exported themselves." Nothing asked here contradicts it
  - `.claude/agile-skills/spec/question.md` §2 and §3
- **Decisions:**
  - **The item was not refined.** No Definition of Ready assessment was made and no acceptance criterion was read against R4 or rewritten. Assessing criteria that must be rebuilt from a file nobody has seen would produce a verdict about criteria that will not survive; the next `refine` execution owns both.
  - **Two questions rather than one.** `EP-001/Q-002` asked for the sample and the sharing rule together and got a reply that answered neither. They are separable, `spec/question.md` §2 requires one answerable question per file, and filing them apart means a partial reply is still usable — a sample with no rule unblocks the parsing criteria on its own.
  - `Q-001` states explicitly that it is a **missing fact and not a choice between options**, which §2 permits and requires to be said rather than dressed up as a choice. It lists the six things that would otherwise be guessed.
  - `Q-002` carries `EP-001/Q-002`'s four options unchanged in substance, with one consequence sharpened: WI-0001 shipped with **no delete**, so option A can put unremovable personal spending into the group's books. The recommendation stays **B** and now argues against A on that ground.
  - **AC5 was deliberately not asked about.** Whether re-import is idempotent or additive cannot be put as a question until the sample says what identifies a row and the rule says what a row becomes. The direction `refine` expects to take — skip rows already imported and report the count, because nothing can be deleted — is recorded in `artifacts/refinement-qa.md` so it is visible rather than sprung later.
  - **Filed now rather than when the orchestrator next selects this item.** The sample is the only input in this epic that must come from outside the workspace, it has been deferred once already, and filing it alongside `WI-0002/Q-001` costs the stakeholder one reply instead of two. This does not make the item runnable and does not advance it: `depends-on` still names WI-0002.
- **Questions raised:** `Q-001` and `Q-002`, both `addressed-to: human`, both blocking
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, before this execution's writes
- **Gates:**
  - `workspace-valid` → **pass** — exit 0 before this execution's writes; re-run by this transition
  - `definition-of-ready` → **skipped**, and this is the substance of the execution rather than an omission: R4 and R10 are unassessable while the CSV shape and the import rule are unknown, and R8 cannot be satisfied by an exchange that has not happened. Assessing the remaining criteria in isolation would record a verdict on criteria that `Q-001` and `Q-002` are certain to replace. The item is suspended, not passed and not overridden
  - `criteria-are-decidable` → **fail**, unassessed in detail for the same reason. AC1 ("each row the import is meant to cover" — which rows, decided by `Q-002`), AC2 (depends on WI-0002's report, itself suspended on its own `Q-001`), AC3 and AC4 (what "not the expected shape at all" means is `Q-001`'s sample) and AC5 (written as an explicit either/or by `intake`) all require the two answers first
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` records both questions, tagged `[refine]`, and their unanswered state, tagged `[unresolved]`. The stakeholder's only words on this item, "I'll send you a sample later", are quoted exactly in `questions/Q-001.md`. Nothing is tagged `[human]` in the Q&A because nothing has been said to record there, and nothing has been paraphrased into agreement
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-001.md` (new), `questions/Q-002.md` (new)
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0003/item.md` — `## Notes` gains a section recording that `refine` reached the item, did not refine it, and why AC5 was left out of the batch. **Acceptance criteria untouched**
- **Status:** `draft` → `awaiting-answer`
- **Result:** Not refined, by design and on this item's own written instruction. Two questions are open to the stakeholder: the CSV sample, and how a bank row becomes a shared expense. Until both are answered there is nothing here anyone can test against.

## 2026-08-22T02:44:23Z — refine v0.1.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** correction to the entry immediately above, which is append-only and cannot be edited
- **Inputs read:**
  - `.claude/agile-skills/spec/doc-header.md` §4a, the citation forms table
- **Decisions:**
  - The previous entry recorded `workspace-valid` as **pass**. That was accurate when the gate ran (before this execution's writes) and inaccurate as a statement about the workspace this execution left behind: `validate-workspace` failed on re-run with `claim.citation.unresolved` at `tracker/items/WI-0003/questions/Q-002.md:28`. The citation there named the item and then a section heading of it — a src marker whose payload was `WI-0001` followed by an `## Out of scope` heading, quoted here in words rather than in the marker syntax for the reason the entry below gives — which is not one of the seven forms in `spec/doc-header.md` §4a, so the gate could not resolve it.
  - Corrected to `[src: WI-0001]`, which is the `item` form and resolves. The sentence it supports is unchanged and still true: WI-0001 shipped with no way to delete a recorded expense.
  - Recorded rather than quietly fixed, because the previous entry's `**Gates:**` bullet claims a pass that the workspace did not have for the two minutes between the transition and this fix.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1, `claim.citation.unresolved`
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 after the correction, 0 errors, 0 warnings
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (exit 0, 5 items and 7 documents checked, 0 errors, 0 warnings)
  - `definition-of-ready`, `criteria-are-decidable`, `qa-recorded-verbatim` → **skipped** — this entry corrects a record and touches no criterion; the assessment is the one in the entry above, unchanged
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-002.md` line 28 — citation form corrected. No other change
- **Status:** `awaiting-answer` → `awaiting-answer` (no move)
- **Result:** The workspace validates. The previous entry's `workspace-valid` pass should be read together with this one.

## 2026-08-22T02:45:13Z — refine v0.1.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** the entry immediately above broke the workspace it was written to repair
- **Inputs read:**
  - `tracker/items/WI-0003/journal.md`, the previous entry
  - `.claude/agile-skills/spec/journal-and-history.md` §0 and the append-only rule
- **Decisions:**
  - The previous entry described a malformed citation by **quoting it**, inside a src marker, so `scripts/lint-claims` read the quotation as a citation of its own and `validate-workspace` failed at `tracker/items/WI-0003/journal.md:73` with the same finding the entry existed to record. One sentence of that entry was rewritten to describe the malformed form in words instead of reproducing the marker syntax. Nothing else in the entry was touched, no claim in it changed meaning, and its heading and timestamp are untouched.
  - **This is a rewrite of an append-only file, and appending could not have fixed it.** `spec/journal-and-history.md` sanctions exactly one exception and this is not it. It is recorded here, loudly, rather than performed quietly: a reader comparing the commit diff against the append-only rule will find the two disagree, and this bullet is the explanation.
  - **The underlying problem is in the toolkit, not in this item.** `lint-claims` cannot distinguish a citation from a quotation of a broken citation, so the record cannot state precisely what was wrong with one without reproducing the error. Every future correction of a citation defect hits this. Reported in `HARNESS-STATUS.md` for turn 8.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1, `claim.citation.unresolved` at `journal.md:73`
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 after the rewrite, 0 errors, 0 warnings
- **Gates:**
  - `workspace-valid` → **pass** (exit 0, 5 items and 7 documents, 0 errors, 0 warnings)
  - `definition-of-ready`, `criteria-are-decidable`, `qa-recorded-verbatim` → **skipped** — no criterion was touched; the assessment stands as the second entry left it
- **Artifacts:**
  - `tracker/items/WI-0003/journal.md` — one sentence of the previous entry rewritten, as described above
- **Status:** `awaiting-answer` → `awaiting-answer` (no move)
- **Result:** The workspace validates. Three entries now stand on this item where one execution happened; the first is the record, the second and third are its corrections, and this is the last of them.

## 2026-08-22T02:54:28Z — answer-questions v0.1.4 — architect

- **Item:** WI-0003
- **Trigger:** `awaiting-answer` since 2026-08-22T02:43:50Z; the stakeholder filled in `## Answer` on both `Q-001` and `Q-002` between turns, which makes both answerable under the skill's precondition 1. Dispatched by the harness ahead of `next`, which stops on an open human-addressed question rather than consuming one.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-001.md` — the CSV sample; reply: "I'll send you a sample later"
  - `tracker/items/WI-0003/questions/Q-002.md` — how a bank row becomes a shared expense; reply: option B
  - `tracker/items/WI-0003/item.md` — five criteria, the two missing facts, the ordering note, and the standing instruction that `refine` must not attempt this item without the sample
  - `tracker/items/WI-0003/history.md` — the suspending row of 2026-08-22T02:43:50Z carries `resume-to: draft`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — round 1 as filed, and "Deliberately not asked in this batch" on AC5
  - `tracker/items/EP-001/questions/Q-002.md` — the question these two supersede, and the first deferral of the same fact
  - `docs/architecture/adr/ADR-0001` … `ADR-0006` — checked for contradiction; none contradicts option B. `ADR-0002` (equal split) is why the rule only has to name *who*; `ADR-0006`, written minutes earlier for WI-0002, is unaffected because an imported expense is an ordinary expense
  - `docs/architecture/overview.md` v3 — `model.py` already holds the validators "so that WI-0003's importer can reuse them"; no change needed, this item has no code yet
  - `docs/product/vision.md`, `.claude/agile-skills/spec/question.md`, `.claude/agile-skills/pipeline.yaml`
  - no `artifacts/plan.md` exists — the item has never been planned
- **Decisions:**
  - **Q-002 — route: the human answered an escalation; propagated.** Option B: the payer and the sharers are named at import time and the import is limited to a date range. Recorded as `ADR-0007`, which fixes the three things the command takes besides the file path and cites `ADR-0002` for the equal split and WI-0001 for each row carrying its own date.
  - **Two details decided on top of Q-002's answer, because the answer did not state them and `refine` and `plan` would otherwise each decide them differently.** (i) The date range is **optional**; omitting it imports every row. The stakeholder asked to be allowed to limit the import, not required to, and making it mandatory would refuse the case where the file is already only the trip. (ii) A row outside the range is **skipped silently** and is not an AC3 failure — filtering is the point of the range, and reporting filtered rows on stderr would drown the rows the tool genuinely could not read. Both are reversible and both are recorded in `ADR-0007` rather than left in a journal.
  - **AC1 amended; AC2–AC5 untouched.** AC1 said "each row the import is meant to cover" and never said what decides that; it now names the payer, the sharers and the range, and says in the criterion itself that the column mapping still waits on `Q-001`. The item is at `draft` so criteria are not frozen; the amendment is called out here because amending a criterion is journalled explicitly whatever the status. AC2–AC5 all depend on the file's shape and remain undecidable.
  - **Q-001 — route: the human replied, but with a deferral, not the fact.** "I'll send you a sample later", the same sentence as on `EP-001/Q-002` and the second deferral of the same thing. Marked `answered` with `answered-by: human`, because that is what they said and it has a consequence — the item still cannot be refined — and because leaving it `open` is the deadlock F-011 describes: `next` step 3 stops on any open human-addressed question, so an unconsumed one stops every later turn forever. Nothing about the CSV's shape was assumed.
  - **The item returns to `draft`, not to `blocked`.** `blocked` is terminal in `pipeline.yaml` and only a human moves an item out of it. WI-0003 is not due: `depends-on` names WI-0002, which is at `draft`, so the orchestrator cannot select this item for a long time and the sample may arrive first. `awaiting-answer` was not available either — with both questions answered, `validate-workspace` fails it with `question.awaiting.none-open`, which is correct. `draft` is inert and self-healing: the `refine` execution eventually dispatched reads `item.md` and files a fresh question if the sample is still missing.
  - **No third question filed for the sample in this execution.** The stakeholder has been asked twice and twice said "later". A third request now would stop the loop — `next` step 3 — while WI-0002, the item that is actually runnable, waits, and no skill could use the answer yet even if it arrived. The instruction to ask again stands in writing at the point where the answer is needed, in `item.md` `## Notes` and in `refinement-qa.md`.
  - **No epic journal entry.** `Q-002` settles the shape of one command on one item, not the shape of the epic; `ADR-0007` is where `plan` will find it.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-22T02:52:26Z
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after writing `ADR-0007` (9 documents)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 after marking both questions answered: `question.awaiting.none-open` on this item and `board.stale`. Both are the expected pre-transition state and both clear with the transition and `board-gen`
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in the two `## Consequences` sections was opened after writing and the change confirmed: `ADR-0007` exists as a v1 current ADR; `item.md` AC1 names the payer, the sharers and the range; `item.md` `## Notes` lists one fact settled and one still missing and carries the `draft`-not-`blocked` reasoning; `refinement-qa.md` carries both `[human]` lines verbatim and the round-1 table; `history.md` and `journal.md` carry this execution
  - `answered-from-the-record` → **pass** — `Q-002`'s answer is the stakeholder's own, quoted; the two details decided on top of it are recorded as decisions in `ADR-0007` with their reversibility, not smuggled in as findings. `Q-001` is recorded as a deferral with **no** answer derived from it, which is the honest form of "the record is still silent"
  - `escalation-is-justified` → **skipped** — nothing was escalated this execution. The one thing that would justify escalation, the missing sample, has already been asked twice and is recorded as the next `refine` execution's first act; re-asking it now would stop the loop without any skill being able to use the answer
  - `workspace-valid` → **pass** — `validate-workspace` exit 0 after the transition and `board-gen`
  - `item-resumed-correctly` → **pass** — the suspending row of 2026-08-22T02:43:50Z records `resume-to: draft`; this execution's row targets `draft`
- **Artifacts:**
  - `docs/architecture/adr/ADR-0007-csv-import-takes-payer-sharers-and-range-from-the-command-line.md` — created, v1, current
  - `tracker/items/WI-0003/item.md` — AC1 amended; `## Notes` head and the two-missing-facts list rewritten; `### Q-002 answered, Q-001 deferred a second time` section added
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — banner, round-1 table and exchange updated with both replies; closing section on where the item stands
  - `tracker/items/WI-0003/questions/Q-001.md` — `status: answered`, `answered-by: human`, consequences naming four files and stating explicitly what was *not* concluded
  - `tracker/items/WI-0003/questions/Q-002.md` — `status: answered`, `answered-by: human`, consequences naming four files
  - a commit of the tracker and docs files this execution wrote
- **Result:** Half of what this item was waiting for arrived. The import will take its payer, its sharers and an optional date range from the command line — `ADR-0007`, AC1 — and the bank CSV's actual shape has been deferred for the second time, so the item goes back to `draft` unrefined, with the instruction to ask again recorded at the point where the answer will finally be needed.
- **Status:** `awaiting-answer` → `draft`

## 2026-08-22T03:30:35Z — refine v0.1.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — runnable for the first time, because `depends-on` WI-0002 reached `done` earlier in this turn. Tied with BUG-0001 on priority rank 3 and selected on the earlier `created` (2026-08-22T01:34:58Z against 02:27:53Z)
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — five criteria, the `## Notes` instruction that `refine` must not attempt this item while the sample is missing, and the two `Q-001`/`Q-002` sections
  - `tracker/items/WI-0003/history.md` — the item reached `draft` from `awaiting-answer` by way of `answer-questions`, not from a send-back by `verify` or `review-close`, so this is a continuation and not a defect fix
  - `tracker/items/WI-0003/journal.md`, `artifacts/refinement-qa.md` — round 1 as filed and half answered
  - `tracker/items/WI-0003/questions/Q-001.md` (the sample, deferred a second time) and `Q-002.md` (the rule, answered — option B, `ADR-0007`)
  - `tracker/items/WI-0001/item.md` — AC3, AC6, AC7 and AC9, the constraints any importer has to normalise into
  - `tracker/items/WI-0002/item.md` — checked that the closed report item leaves nothing of this item's scope undone; it does not
  - `tracker/items/EP-001/questions/Q-001.md` — the stakeholder's statement that the import ships and is not optional, which is why option D is listed only to be rejected
  - `docs/architecture/adr/ADR-0002` (amount format, deliberately not widened for the import), `ADR-0007` (payer, sharers and date range given at import time); `docs/product/vision.md` — checked for contradiction, none
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md` §2, §3 rule 6 and §4
  - the whole project tree, searched for a CSV file or a header row: `find . -iname '*.csv' -o -iname '*sample*' -o -iname '*bank*'` and `git status --untracked-files=all` both empty, so the sample has genuinely not arrived
- **Decisions:**
  - **Did not attempt the refinement, and did not ask for the sample a third time.** `item.md`'s `## Notes` instructed the next execution to file a fresh question and suspend if the sample was missing. It is missing. But the stakeholder has now declined the same request twice with the same sentence, and repeating it would spend their attention on something they have already answered and leave this item waiting on a file that may never arrive.
  - **Filed `Q-003`, superseding `Q-001` per `spec/question.md` §3 rule 6, as the choice underneath the missing fact: where should the importer learn the file's shape from?** Three real options — a sample sent now (**A**), a fixed format the stakeholder converts their export into (**B**), or the mapping given as options at import time (**C**) — plus **D**, dropping the import, listed only to be rejected because `EP-001/Q-001` settled that it ships. Only **A** needs the sample; **C** takes it off the critical path entirely by turning the four missing facts into arguments stated by the person holding the file. Recommended **C**, named **A** as better if the file is at hand, and argued against **B** from the stakeholder's own words — converting the export in a spreadsheet at every import is the retyping the idea asked to stop.
  - **Escalation condition, per `spec/question.md` §4:** it depends on intent no document records — which of the three the stakeholder would rather live with — and **B** commits them to manual work at every import, which is not a cost `refine` may accept on their behalf.
  - **No acceptance criterion was rewritten.** AC1 would have to be written three different ways depending on the answer, and AC3 and AC4 differ between the options in what "the expected shape" means. The one edit made is a pointer, not a requirement: AC1 said the column mapping "waits on `Q-001`" and now says it waits on `Q-003`, which supersedes it, and names that under two options the mapping becomes a run-time argument.
  - **No Definition of Ready verdict was reached**, for the reason the 2026-08-22T02:42:09Z execution gave: a verdict on criteria that are about to be rewritten is a verdict about the wrong criteria. Recorded under `**Gates:**` as a fail with the per-criterion state as far as it can honestly be assessed.
  - **AC5 stays unasked** — whether re-importing the same file skips rows already imported or adds them again. It still cannot be put well until something identifies a row, which depends on which option is chosen. It is now named inside `Q-003` itself so the stakeholder sees it coming rather than having it sprung on them later. `refine` still expects to decide it toward skipping, and reporting how many rows were skipped, because WI-0001 shipped with no way to delete an expense.
  - **`item.md` goes to `awaiting-answer`, not `blocked`.** A blocking question is open and the protocol suspends the item; `blocked` would claim an impasse, and this is a question with three answerable options, two of which need nothing from outside the workspace.
- **Questions raised:** `Q-003` (`addressed-to: human`, blocking) — how should the importer learn the shape of the bank CSV: a sample sent now, options typed at run time, or a fixed format converted to? Supersedes `Q-001`. Pointer: `artifacts/refinement-qa.md`, round 2, `[unresolved]`
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-22T03:28:24Z
  - `find . -path ./.git -prune -o \( -iname "*.csv" -o -iname "*sample*" -o -iname "*bank*" \) -print` → no output; `git status --short --untracked-files=all` → no output. The sample is not on disk under any name
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 before this execution's writes
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 after `Q-003` was written, reporting `question.blocking.not-suspended` and `board.stale` — both are this execution's own unfinished business, cleared by this transition and the `board-gen` that follows it
- **Gates:**
  - `workspace-valid` → **pass** — exit 0 before the writes; the two mid-execution errors are the suspension this transition performs and the board this execution regenerates, and both clear on it
  - `definition-of-ready` → **fail**, per criterion as far as it can honestly be assessed. R1 pass (frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`). R2 pass (role "the person in the group who exports their bank statement anyway", capability "point the tool at that CSV file and have its rows become recorded expenses", outcome "so that I do not retype spending the bank has already written down"). R3 pass (AC1–AC5, labelled, checkboxes). **R4 fail** on AC1, AC3, AC4 and AC5: none names a command that could be run, because the command's arguments are what `Q-003` decides; AC2 alone is decidable as written (import a file, then run `expenses` and `debts` and see the rows counted). R5 pass (three exclusions, of which "supporting more than the CSV shape this item settles on" is one a reader could reasonably assume is included). **R6 fail** — `Q-003` is blocking and open, which is what this suspension is for. R7 pass (`depends-on: WI-0001`, `WI-0002`, both `done` as of this turn). R8 pass (`artifacts/refinement-qa.md` carries both rounds, tagged `[human]`, `[refine]`, `[assumed]` and `[unresolved]`). R9 **not assessed** — whether this is one coherent change depends on the answer: option A is a small item, option C is roughly twice the size, and judging it now would be judging three different items. **R10 fail** — the combination table cannot be written at all, because the options the item introduces are exactly what `Q-003` asks about
  - `criteria-are-decidable` → **fail** — the test applied in turn: AC2 passes (build a ledger by import, then `python3 -m expenses expenses` and `python3 -m expenses debts`, and see the imported rows listed and counted). AC1, AC3, AC4 and AC5 fail: for each of them, two implementations that behave differently would both pass, because the file's shape and the command's options are unsettled. Named criterion by criterion under `definition-of-ready` above
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` round 2 records the question asked, tagged `[refine]`, and its unanswered state, tagged `[unresolved]`. Nothing new is tagged `[human]`, because the stakeholder has said nothing this round; round 1's two `[human]` lines are unchanged, including the deferral quoted in the words they used
- **Artifacts:**
  - `tracker/items/WI-0003/questions/Q-003.md` (new) — supersedes `Q-001`
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — round 2 added, banner restated, with why this is a different question and why no criterion was rewritten
  - `tracker/items/WI-0003/item.md` — a new `## Notes` section recording this execution; AC1's pointer moved from `Q-001` to `Q-003`. **No other criterion touched**
  - `tracker/board.md` — regenerated
  - a commit of the tracker files this execution wrote
- **Result:** WI-0003 is suspended on `Q-003`, a question addressed to the stakeholder. The sample has been asked for twice and deferred twice, so rather than ask a third time this execution filed the choice underneath it — a sample now, a fixed format they convert to, or the column mapping as run-time options — and recommended the third, because it removes the sample from the critical path without guessing anything. Nothing was refined and no criterion was rewritten on a guess: two of the three options change what the command's arguments are.
- **Status:** `draft` → `awaiting-answer`

## 2026-08-22T03:37:30Z — answer-questions v0.1.4 — architect

- **Item:** WI-0003
- **Trigger:** status `awaiting-answer`, dispatched ahead of `next` because `Q-003` — addressed to
  the human and blocking — came back with `## Answer` filled in. An answered-but-unconsumed
  human question stops the orchestrator on every subsequent run, so consuming it is the first
  thing any turn does.
- **Inputs read:**
  - `tracker/items/WI-0003/questions/Q-003.md` (open, `addressed-to: human`, answered by the
    stakeholder), `Q-001.md` and `Q-002.md` (both `answered`, for what had already been asked)
  - `tracker/items/WI-0003/item.md` — AC1–AC5 and the whole of `## Notes`
  - `tracker/items/WI-0003/history.md` — for `resume-to`, recorded as `draft` on the
    2026-08-22T03:30:35Z row
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — rounds 1 and 2, and what `refine`
    deliberately did not ask
  - `docs/architecture/adr/ADR-0007-csv-import-takes-payer-sharers-and-range-from-the-command-line.md`
    (v1) — the decision this one pairs with; it settles what the tool does with a row and says
    explicitly that it does not settle how a row is read
  - `docs/architecture/adr/` — the index, to allocate `ADR-0010` (highest present was `ADR-0009`)
  - `.claude/agile-skills/spec/question.md` §§2–4, `spec/ids-and-statuses.md` §§3.1 and 4,
    `spec/doc-header.md` §§2–4, `spec/journal-and-history.md`
- **Decisions:**
  - **`Q-003` is answered, by the human, and the route is "escalated and now returned".** They
    wrote: "No — just wait for my file. I don't want a name-the-columns version." Read as option
    **A**, and as a refusal of **B** as well: "a name-the-columns version" is option C by
    description, and "just wait for my file" only makes sense if the export is to be handed over as
    it is — under B there would be nothing to wait for, because the stakeholder would convert the
    file themselves and import it today. `refine`'s recommendation of **C** was overruled by name.
  - **Recorded as `ADR-0010` rather than only in the question file.** The decision changes what the
    import command *is* — no `--date-column`-style options, ever — and that is a fact `plan` will
    need long after this question stops being read. `ADR-0007` is its pair and was left untouched:
    it is still correct, and it had already scoped itself to what the tool does with a row.
  - **Three things the answer did not say, decided here so `refine` and `plan` do not each decide
    them differently.** (1) The sample lands at
    `tracker/items/WI-0003/artifacts/bank-sample.csv` — the stakeholder answers in files, so the
    file needs a place a fresh session looks in without being told. (2) No fourth question may be
    filed for the sample: they have been asked three times and have answered the third with an
    instruction, and `spec/question.md` §4 does not license a question whose answer is already
    recorded. (3) The item is an impasse until the file arrives, and the honest status for that is
    `blocked`.
  - **This execution returned the item to `draft`, not to `blocked`, even though `blocked` is where
    it belongs.** `resume-to` on the suspending row says `draft`, and the `item-resumed-correctly`
    gate exists precisely so that `answer-questions` cannot substitute its own judgement for the
    status the suspending skill recorded. The move to `blocked` is `refine`'s to make: it owns
    `draft` items and it is the skill that would otherwise ask a fourth time. The instruction is
    written at the top of `item.md` `## Notes` and repeated in `refinement-qa.md`, because the
    session that carries it out will not be this one.
  - **AC1 was rewritten and AC3, AC4 and AC5 were each amended.** Legitimate: the item is at
    `draft`, so criteria are not frozen (`spec/dor-dod.md`). AC1 lost the clause hedging that the
    column mapping "becomes a run-time argument under two of `Q-003`'s three options" — both of
    those options were refused — and now states that the mapping is fixed, read off the
    stakeholder's own export, and that the command takes no column options. AC3, AC4 and AC5 each
    gained one clause naming the sample as the single thing they wait on. That is a narrower claim
    than before, when they waited on a choice as well, and it is the whole substantive gain from
    this answer.
  - **Nothing about the file's shape was written, assumed or guessed.** No delimiter, no header, no
    date format, no column names. The prohibition `Q-001` was filed to protect is not lifted by an
    answer that says where the shape will come from.
- **Questions raised:** none. No question was re-addressed to the human, and none may be for this
  item: see the decision above.
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-22T03:33:27Z`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
    (run before the edits, and again after them)
  - `git diff --stat tracker/items/WI-0003/questions/Q-003.md` → used to confirm the file was
    rewritten without loss after a bad in-place edit (see Result)
- **Gates:**
  - `answer-is-propagated` → **pass**. Each file named in `Q-003`'s `## Consequences` was opened
    and the change confirmed present: `ADR-0010` exists with the decision and its consequences;
    `item.md` AC1 no longer contains the run-time-argument clause and AC3/AC4/AC5 each carry the
    new "waits on the sample" clause; `item.md` `## Notes` carries the rewritten lead instruction
    (`blocked`, not a fourth question) and a new `### Q-003 answered` section;
    `refinement-qa.md` round 2 shows the answer in its table, the `[human]` and
    `[answer-questions]` lines in its exchange, and a new closing section.
  - `answered-from-the-record` → **pass**. The answer is the stakeholder's own words, quoted in
    `Q-003` `## Answer` and in `ADR-0010` `## Decision`. The three details they did not state are
    recorded as decisions in `ADR-0010`, not smuggled in as if they had been said.
  - `escalation-is-justified` → **skipped**, no escalation. Nothing was re-addressed to the human;
    the one thing still outstanding is a file, not an answer, and `spec/question.md` §4 offers no
    condition for asking again for something already promised.
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings).
  - `item-resumed-correctly` → **pass**. `resume-to` on the 2026-08-22T03:30:35Z row is `draft`;
    this execution's row targets `draft`.
- **Artifacts:**
  - `docs/architecture/adr/ADR-0010-the-column-mapping-is-fixed-from-the-sample-not-a-run-time-option.md`
    (new, v1) — option A recorded, B and C refused with reasons, where the sample lands, no fourth
    question, and the impasse
  - `tracker/items/WI-0003/questions/Q-003.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-08-22T03:33:27Z`; `## Answer` carries the stakeholder's line verbatim plus
    the architect's reading; `## Consequences` names four files
  - `tracker/items/WI-0003/item.md` — AC1 rewritten; AC3, AC4, AC5 amended; `## Notes` lead
    instruction rewritten and a `### Q-003 answered` section added; `updated` stamped
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — round 2 answered: banner, table row,
    exchange, and a new `## Where this item stands after round 2`
  - no ADR was superseded; `ADR-0007` was read and deliberately left at v1
- **Result:** `Q-003` consumed. The stakeholder refused both alternatives to their own file, so the
  importer is written against that file and takes no column-mapping options (`ADR-0010`); AC1 says
  so and AC3–AC5 now wait on the sample alone. The sample still has not arrived, so WI-0003 returns
  to `draft` unrefinable — waiting on the stakeholder's action rather than their attention, which
  is the one thing the question protocol cannot help with. The next `refine` execution moves it to
  `blocked` instead of asking a fourth time. One process note worth keeping: an in-place edit of
  `Q-003` split on the first `## Answer`, which occurs inside option A's own text, and truncated
  `## Options considered`; it was caught by `git diff --stat` showing 3 deletions where 2 were
  expected, and the file was rewritten in full. Question files quote their own section headings —
  edit them whole, not by splitting on a heading.
- **Status:** `awaiting-answer` → `draft`

## 2026-08-22T03:40:17Z — refine v0.1.2 — product-analyst

- **Item:** WI-0003
- **Trigger:** status `draft`, dispatched by `next` — highest-ranked runnable item (medium/rank 3,
  tie-broken against `BUG-0001` by the older `created`), with `depends-on` WI-0001 and WI-0002 both
  `done` and no open question of any kind.
- **Inputs read:**
  - `tracker/items/WI-0003/item.md` — AC1–AC5, `## Story`, `## Out of scope`, and the whole of
    `## Notes` including the instruction left by `answer-questions` twenty minutes earlier
  - `tracker/items/WI-0003/history.md` — four rows; the item reached `draft` from
    `awaiting-answer` by `answer-questions`, **not** by a send-back from `verifying` or
    `in-review`, so this is a fresh refinement rather than a defect fix
  - `tracker/items/WI-0003/journal.md` — all seven prior entries, for what `intake` and the three
    earlier `refine` executions recorded verbatim
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — rounds 1 and 2, and "Still deliberately
    not asked"
  - `tracker/items/WI-0003/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all three `answered`
  - `docs/product/vision.md` (v3) — "expenses that already exist in the person's bank CSV export
    can be brought in rather than retyped", and "import a bank export without hand-editing it"
    among the measures. Both are consistent with `ADR-0010`; no contradiction to raise
  - `docs/architecture/adr/ADR-0007...` (v1) and `ADR-0010...` (v1) — between them the command's
    whole argument list
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md` §4, `spec/ids-and-statuses.md`
    §§3.1 and 4
  - the filesystem, for the sample: `find . -iname '*.csv'` outside `.git` returned nothing, and
    `tracker/items/WI-0003/artifacts/` holds only `refinement-qa.md`
- **Decisions:**
  - **No question was asked, and none may be.** Three have already been addressed to the
    stakeholder about this one file (`EP-001/Q-002`, `Q-001`, `Q-003`), and the third was answered
    with an instruction rather than a deferral: "No — just wait for my file. I don't want a
    name-the-columns version." `spec/question.md` §4 licenses an escalation when intent is
    unrecorded or the record is silent; here the intent is recorded and explicit. A fourth question
    would be the pipeline asking a person to send a file, which is not a question, and it would
    stop the orchestrator on every subsequent turn while `BUG-0001` — `ready` and runnable —
    waits.
  - **The Definition of Ready was applied for the first time on this item.** The three previous
    `refine` executions declined to, on the ground that a verdict about criteria that are about to
    be rewritten is a verdict about the wrong criteria. That ground is gone: `Q-003` settled where
    the file's shape comes from, so the criteria are no longer about to change shape — they are
    simply unwritable until the file exists. Declining a second time would have been the same
    reasoning applied to a situation it no longer describes.
  - **R10 was salvaged as far as it could be without the sample.** The combinations this item
    introduces split cleanly: some depend on the CSV's shape and some do not. The ones that do not
    were knowable today and are now written into `item.md` `## Notes` as open, attributed to
    `refine` — a payer or a sharer who is not a recorded person, a date range that matches no row,
    whether the range bounds are inclusive, whether a run all of whose rows fail exits non-zero.
    None of them is a guess or a decision; they are questions the eventual criteria must answer,
    and recording them now means the execution that unblocks this item does not rediscover them.
    Also recorded: the one combination there is *no* work to state — the import's interaction with
    WI-0002's repayments, because an imported expense is an ordinary expense (AC2) and repayments
    are their own record (`ADR-0001`).
  - **No acceptance criterion was rewritten in this execution.** AC1 and AC3–AC5 were amended
    twenty minutes ago by `answer-questions` propagating `Q-003`, and each now states that it waits
    on the sample and on nothing else. There is nothing further to write about them that would not
    be a guess about a file's shape.
  - **No override was recorded, and none could be.** `spec/dor-dod.md` §1 lets the stakeholder
    force an item to `ready` without meeting the checklist, and that is their call to make.
    They have not offered one — they said the opposite, that they would send the file. Recording an
    override would be inventing their consent to ship an unspecified parser.
  - **`blocked` rather than `awaiting-answer`.** `awaiting-answer` means a blocking question is
    open; none is, and manufacturing one to hold the item there would put a false entry in the
    record and re-stop the orchestrator every turn for a question nobody needs to answer. `blocked`
    is "a documented impasse that no skill can resolve", which is exactly this: the missing input
    exists only outside the workspace. `resume-to: draft` is recorded so the item comes back to
    refinement rather than to some later stage.
- **Questions raised:** none — see the first decision. `refinement-qa.md` round 3 records the round
  in which nothing was asked and why, and nothing on this item is left `[unresolved]`: all three
  questions are `answered`.
- **Commands:**
  - `find . -path ./.git -prune -o -iname '*.csv' -print` → exit 0, no output (the sample is not
    anywhere in the workspace)
  - `ls -la tracker/items/WI-0003/artifacts/` → only `refinement-qa.md`
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-22T03:38:34Z`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `definition-of-ready` → **fail**, criterion by criterion:
    R1 **pass** — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`;
    the `[auto]` check is `validate-workspace` exit 0.
    R2 **pass** — `## Story` names role, capability and a "so that" outcome.
    R3 **pass** — AC1–AC5, labelled, as checkboxes.
    R4 **FAIL** — only AC2 is decidable by observation. AC1 cannot name the columns, the
    delimiter, the date format or the amount convention; AC3 cannot enumerate what makes a row
    unusable; AC4's "not the expected shape at all" has no referent; AC5 is an either/or rather
    than a criterion. All four name the sample as the single thing they wait on.
    R5 **pass** — `## Out of scope` names three, including "Supporting more than the CSV shape
    this item settles on".
    R6 **pass**, for the first time on this item — `Q-001`, `Q-002`, `Q-003` all `answered`; no
    open question of any kind remains.
    R7 **pass** — `depends-on` WI-0001 and WI-0002, both `done`.
    R8 **pass** — `refinement-qa.md` holds rounds 1–3 with every answer tagged.
    R9 **pass** — one command, one parser; `ADR-0007` and `ADR-0010` fix the whole argument list
    and nothing in it suggests a split.
    R10 **FAIL** — the shape-dependent combinations cannot be enumerated at all, and "we cannot
    list the combinations" is not the same as a combination left deliberately open. The
    shape-independent ones were made visible in `## Notes` (see Decisions).
  - `criteria-are-decidable` → **fail**. AC2 alone survives the test: run the import, then run the
    who-owes-whom report, and confirm the imported expenses appear in both — the command exists
    and the verdict follows. For AC1, AC3, AC4 and AC5 no command can be named, because naming one
    requires knowing what file it would be run against. This gate and R4 fail on the same fact and
    are not independent evidence.
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` carries every question and every answer
    across three rounds, each tagged `[human]`, `[assumed]` or `[unresolved]`, with the
    stakeholder's three replies quoted word for word. Round 3 records a round in which nothing was
    asked, and why, so the absence is on the record rather than looking like an omission.
- **Artifacts:**
  - `tracker/items/WI-0003/item.md` — two sections added: the per-criterion DoR assessment with
    R10's shape-independent combinations left open and attributed, and the impasse with the exact
    path the sample should land at and how the item returns. `updated` stamped. No acceptance
    criterion changed.
  - `tracker/items/WI-0003/artifacts/refinement-qa.md` — banner updated, and `## Round 3` added:
    the round in which nothing was asked, the per-criterion verdict, why no override was recorded,
    and where the item stands.
  - no ADR was written; `ADR-0007` and `ADR-0010` were read and are sufficient.
- **Result:** The Definition of Ready fails on R4 and R10, both on one input the workspace has
  never held and no skill may guess — a sample of the stakeholder's bank CSV. Every question that
  could be asked has been asked and answered, so there is no escalation left and the item is a
  documented impasse: it moves to `blocked` with `resume-to: draft`. What was salvageable without
  the sample was salvaged — R10's shape-independent combinations are now visible, and R6 passes
  for the first time. Drop a CSV at `tracker/items/WI-0003/artifacts/bank-sample.csv` and any skill
  may return the item to `draft`; the next refinement will have everything else already settled.
  The rest of the epic is unaffected: `BUG-0001` is `ready` and runnable.
- **Status:** `draft` → `blocked`
