# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-10T13:17:35Z — intake v0.5.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's idea in `IDEA.md`; no status made this runnable, because the item did not exist yet
- **Inputs read:**
  - `IDEA.md` (the stakeholder's opening statement, verbatim)
  - `tracker/project.yaml`
  - `tracker/items/` (empty — no prior items to overlap with)
- **Decisions:**
  - This item carries envelopes exist and persist. See EP-001's entry of the same execution for how the work was split and why.
- **Questions raised:** none on this item; five were filed on EP-001 (`Q-001`…`Q-005`), of which the ones this item's criteria depend on are named in its `## Notes`
- **Commands:**
  - `scripts/new-item --id WI-0001 --type work-item --epic EP-001 --status draft --actor intake` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, run to exit 0 after this execution's writes; see EP-001's entry for the run)
  - `epic-has-success-measures` → **pass** (judged on EP-001, not here; see its entry)
  - `an-open-question-was-asked` → **pass** (judged on EP-001, not here; see its entry)
  - `engagement-state-is-delimited` → **pass** (judged on `docs/product/vision.md`; see EP-001's entry)
  - `items-are-separable` → **pass** (this item is deliverable and observable on its own; its dependency, if any, is in its `depends-on`)
  - `no-solution-in-the-problem` → **pass** (the story names no technology the stakeholder did not; the provisional command name is flagged in `## Notes` rather than asserted)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (created and filled in)
  - `tracker/items/WI-0001/history.md`, `tracker/items/WI-0001/journal.md` (created)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` from the stakeholder's idea, carrying envelopes exist and persist. Its acceptance criteria are deliberately rough; `refine` is what makes them decidable.

## 2026-09-10T13:21:46Z — refine v0.6.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (only runnable item; WI-0002 and WI-0003 rejected on unfinished `depends-on`, EP-001 on its open blocking questions)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md` (one row: `— → draft` by intake; no send-back, so this is a fresh draft rather than a repair)
  - `tracker/items/WI-0001/artifacts/` — no prior `refinement-qa.md`
  - `tracker/items/EP-001/item.md` and `questions/Q-001.md`…`Q-005.md` — five open, none answered
  - `docs/product/vision.md` (v1)
  - `tracker/project.yaml` — `project.name: envel`, all commands null
  - `SIMULATION-NOTICE.md` — the stakeholder is asynchronous and was not in this session
- **Decisions:**
  - **The stakeholder is not present, so this execution asks in writing and suspends** (skill precondition 2). It did not stop at that point: everything that could be settled without them was settled first, so that when they answer, one round closes the item.
  - **AC1–AC6 rewritten from intake's five.** Each now names the stream as well as the exit status, because "creates an envelope" and "prints one line per envelope" are not observations. AC2 fixes the exact line content; AC3 states the three invocations are separate processes with nothing in between, which is what "survives between runs" actually means; AC4 is new and states the order; AC5 gained the *once and only once* check after the duplicate is refused; AC6 replaces intake's "says so" with exit 0, non-empty stdout, and no envelope name in it.
  - **AC4 (sort order) was decided under no licence, and says so.** Without a stated order, AC2, AC3 and AC5 are not decidable, so the choice was forced by the other criteria rather than by taste. Recorded as `[assumed]` in `artifacts/refinement-qa.md` with where a disagreement lands: a send-back to `refine` on this item (R12).
  - **AC5 (duplicate refused, non-zero) was decided under no licence too**, and recorded the same way. The alternative — silently doing nothing — makes a typo indistinguishable from success.
  - **Two gaps were judged the stakeholder's and only two.** The command name, because they type it and it propagates to WI-0002, WI-0003 and the docs; and the name-identity rule, because a capitalisation slip silently splitting one envelope into two is the failure that makes their numbers wrong. Both are product stake under step 3's first test.
  - **Storage location, storage format and the exact wording of the messages were routed to `plan`, not to the stakeholder** (step 3's fourth test — the answer is the same whoever the stakeholder is). They are in the item's `## Notes` as open design questions.
  - **No criterion was written for a rejected envelope name**, deliberately. It depends on `Q-002` and inventing one now would be a false requirement.
  - **`## Out of scope` gained four entries** — multiple envelopes per invocation, any option or flag on `new`/`list`, grouping or nesting, and making the storage location configurable — so R10's combination space is closed by exclusion rather than left open.
- **Questions raised:** `Q-001` (blocking, to human — the command name), `Q-002` (blocking, to human — envelope name identity and permitted characters). Both open, both `[unresolved]` in `artifacts/refinement-qa.md`. One grouped ask, two artifacts, each `## Context` naming the item, the round and which of two it is.
- **Commands:**
  - `scripts/validate-workspace .` → exit 1, 2 errors (`board.stale`, and `question.blocking.not-suspended` on this item — the second is what this move resolves)
  - `scripts/board-gen .` → exit 0, board rewritten
  - `scripts/lint-answers --item WI-0001` → exit 0, 0 errors (0 consumed human answers, 0 delegations)
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` re-run by this transition over the state the move produces; the `question.blocking.not-suspended` error above is exactly what suspending the item resolves)
  - `definition-of-ready` → **fail** (, criterion by criterion: R1 pass (frontmatter, `type`, `epic`, `priority` all set); R2 pass (role, capability, "so that" outcome); R3 pass (six `AC<n>` checkboxes); R4 pass (every criterion now names a command, a stream and an exit status — intake's "creates an envelope", "prints one line per envelope" and "says so" were the three that failed, and all three were rewritten); R5 pass (six exclusions, four of them added here); **R6 fail** — `Q-001` and `Q-002` are open and blocking, which is why this item is not going to `ready`; R7 pass (no `depends-on`); **R8 fail** — `artifacts/refinement-qa.md` exists but declares `status: agenda`, because the conversation has not happened; R9 pass (one coherent change: envelopes exist and persist); R10 pass (two behaviours, no options, and all four pairs covered by AC2, AC4, AC5, AC6 or excluded); R11 pass (no criterion counts a project artefact; AC5's "once and only once" counts lines of the tool's own output); R12 pass (both `[assumed]` answers state that nothing licensed them and where a disagreement lands))
  - `criteria-are-decidable` → **fail** (on the item as a whole, and it is the one criterion that is *missing* rather than wrong: a rejected envelope name has no criterion, and cannot have one until `Q-002` is answered. AC1–AC6 themselves are each decidable by a named command, stream and exit status)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item WI-0001`, exit 0; `## Cross-answer check` in `artifacts/refinement-qa.md` records `Checked against: none` with the reason — no question in this workspace has an answer yet)
  - `qa-recorded-verbatim` → **pass** (for what exists, and it is honest rather than complete: `artifacts/refinement-qa.md` carries the agenda, the two `[unresolved]` questions, both `[assumed]` decisions with their authority, and what was routed to `plan`. There is no human speech to record verbatim, because none has happened; the file says so and declares `status: agenda`)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — criteria rewritten AC1–AC6, `## Out of scope` extended, `## Notes` rewritten
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — filed, open, blocking, to the human
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — created, `status: agenda`
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** Everything that could be settled without the stakeholder was: six decidable criteria, four new exclusions, two assumptions recorded with their authority and their route back, and three design questions routed to `plan` instead of to a person. Two genuinely product-level gaps remain and are filed as `Q-001` and `Q-002`. The item is suspended with `resume-to: draft`, and one answered round should be enough to reach `ready`.

## 2026-09-10T13:34:01Z — answer-questions v0.6.2 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer` with both filed questions carrying replies from the human; consumed ahead of `next`, as the turn's amendment B requires
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` (both, with the human's replies)
  - `tracker/items/WI-0001/item.md`, `history.md` (the `resume-to` on the suspending row), `journal.md`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (`status: agenda`)
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — all five, answered earlier in this same turn, for the cross-answer check
  - `tracker/items/WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md`, `WI-0005/item.md`
  - `docs/product/vision.md` (v2)
  - `docs/architecture/adr/` — empty; no recorded decision could be contradicted
  - `.claude/agile-skills/spec/workspace-layout.md` §1.3, `spec/dor-dod.md` R8, `spec/doc-header.md` §4a
  - `tracker/items/WI-0001/artifacts/` otherwise empty — there is no `plan.md`, so no invalidation set exists on this item
- **Decisions:**
  - Both answers came by route 1 of step 3: the human answered them directly. Nothing was decided by this execution beyond where each answer lands.
  - `Q-001` (`envel`, option A) changed **no acceptance criterion**, here or on WI-0002 or WI-0003 — they already said `envel`. What changed is the word's provenance, and that is recorded in `## Notes` and in the question's `## Consequences` rather than left as an absence a later reader would have to explain to themselves.
  - `Q-002` (option B) was propagated as four criteria rather than one sentence in `## Notes`. Their answer settles three separable things — matching ignores case, the stored capitalisation is what comes back, and spaces are allowed while an empty name is not — and a single criterion covering all three is a criterion that gets checked once and reported as covering everything.
  - AC5 was **amended**, not replaced: the existing duplicate-refusal sentence stands and a case-differing invocation is added to it, because the answer widens when AC5 fires rather than changing what it does. The criteria were amendable here because the item is at `draft` (`resume-to: draft`), before the freeze `spec/work-item.md` §2 applies at `ready`.
  - AC9 and AC10 were written as two criteria, not one. An empty argument and an argument of spaces are different inputs to whatever validates a name, and a single criterion naming both is satisfied by a test of either.
  - AC7 to AC10 were appended rather than inserted, and nothing was renumbered. `refinement-qa.md`, the item's own `## Notes` and its `R10` paragraph all refer to AC2 to AC6 by number, and renumbering would have moved every one of those references silently (`spec/doc-header.md` §4a).
  - Propagated `Q-002` into **WI-0002 AC4** as well. Envelope lookup on a recording command is the same "is this the same envelope?" question WI-0001 answers, and had AC4 been left alone the two items would have disagreed about what an envelope is — WI-0001 refusing `Groceries` as a duplicate while WI-0002 reported it unknown.
  - Left `refinement-qa.md` at `status: agenda`. The answers are written into it verbatim, so its Q&A half is no longer an agenda, but whether refinement is *finished* is `refine`'s judgement and R8 is `refine`'s gate: the two `[assumed]` decisions in that file have still never been put to the stakeholder. Flipping the field would have satisfied a Definition of Ready check on behalf of a skill that has not run.
  - Did **not** put A1 (list ordering) or A2 (duplicate refusal) to the stakeholder now. They are `refine`'s open assumptions on an item returning to `refine`, and re-filing them from here would take the same question to the same person one round earlier while duplicating the artifact that already records them.
  - Recorded in `refinement-qa.md` that `EP-001/Q-005` — the elicitation, answered in this turn — was the stakeholder's chance to raise listing order or duplicate names unprompted and that they raised three other things instead. Recorded explicitly as **not** agreement, because silence in an elicitation is the easiest thing in this record to mistake for consent.
  - Recorded in `Q-002`'s `## Consequences` that `docs/product/vision.md` was deliberately **not** touched, with the reason. The matching rule is user-visible, but the vision says what the tool is for and the authoritative statement of this answer is the criteria; naming the omission is what keeps it a decision rather than an oversight.
- **Cross-answer check:**
  - `Q-001` — checked against `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`, `WI-0001/Q-002`; every verdict **compatible**. All six prior human answers were checked rather than a chosen subset: there are only six in this workspace, so the complete check cost less than the argument about relevance would have. `EP-001/Q-005` is the one that mattered — it invited them to raise anything unprompted and they did not raise the command name.
  - `Q-002` — checked against `EP-001/Q-001`, `EP-001/Q-003`, `EP-001/Q-005`, `WI-0001/Q-001`; every verdict **compatible**. `EP-001/Q-003` is the same instinct twice: a balance that has gone negative and a second envelope created by a capitalisation slip are both numbers that have stopped being true.
  - No verdict of `conflicts`, so no question was put back to the stakeholder. `scripts/lint-answers --item WI-0001` → exit 0.
  - The first run of that gate **failed**, and usefully: it read `EP-001/Q-002`, `Q-003` and `Q-004` out of a sentence in `Q-001` that named them as *not* checked further, and demanded a verdict for each. Rather than rephrase to hide them from the parser, all four were given real verdicts. The gate was right about the shape even though it was reading prose.
- **Questions raised:** none
- **Commands:**
  - `scripts/lint-answers --item WI-0001` → exit 1 first (`answer.cross-check.no-verdict` on `Q-001`), then exit 0 after every named ID was given a verdict
  - `scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0001 --uncommitted` → exit 0
  - `scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0
  - `scripts/validate-workspace .` → exit 1, both errors being the two this transition itself clears (`board.stale`, `question.awaiting.none-open`)
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in the two `## Consequences` sections was opened and the change is in it: `WI-0001/item.md` (AC5 amended; AC7, AC8, AC9, AC10 added; `## Notes` and the `R10` paragraph rewritten), `WI-0002/item.md` (AC4 amended), `WI-0001/artifacts/refinement-qa.md` (both `[unresolved]` placeholders replaced by the stakeholder's words, cross-answer check redone). Neither `## Consequences` section names zero files. The two entries that record a **deliberate non-change** — `tracker/project.yaml` under `Q-001`, `docs/product/vision.md` under `Q-002` — say so in as many words and are not offered as propagation.)
  - `answered-from-the-record` → **pass** (both were answered by the human directly; each `## Answer` carries their words verbatim and each is quoted again in `refinement-qa.md`. No ADR was written, because this execution decided nothing the stakeholder had not.)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human.)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents --rule propagated-claims-carry-their-obligation --item WI-0001 --uncommitted` → exit 0, over a window of zero paths under `docs/`. This execution wrote nothing into `docs/` at all, which is the reason and is recorded as such rather than as a passing check on prose that does not exist.)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0, likewise over an empty window. No `## Engagement state` section was read or written by this execution; `docs/product/vision.md`'s was already falsified and recorded earlier in this turn under `EP-001/Q-001`.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001` → exit 0 over two consumed human answers and zero delegations, after the failure described under `**Cross-answer check:**` was fixed by adding verdicts rather than by rewording.)
  - `workspace-valid` → **pass** (`validate-workspace .` reports only the pre-existing `project.commands.test-null` warning once this move lands; both errors it showed beforehand are the ones this transition resolves.)
  - `item-resumed-correctly` → **pass** (the suspending row (`2026-09-10T13:21:46Z`, `draft → awaiting-answer`, actor `refine`) records `resume-to: draft`, and this transition targets `draft`. Not `ready`: the answers unblock refinement, they do not complete it, and R8 is unsatisfied while `refinement-qa.md` says `status: agenda`.)
  - `a-deferral-is-not-an-answer` → **skipped** (neither reply defers. Each names a chosen option and gives a reason, and each is recorded `answered` with consequences containing a decision.)
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` — `answered`, `answered-by: human`, `answered-at` stamped, `## Cross-answer check` and a file-naming `## Consequences` added
  - `tracker/items/WI-0001/questions/Q-002.md` — the same
  - `tracker/items/WI-0001/item.md` — AC5 amended; AC7 to AC10 added; `## Notes` rewritten from an open-questions block into a record of what was answered and what is still `refine`'s; `R10 — combinations` extended
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — both answers recorded verbatim and marked `[human]`; the preamble rewritten to say why `status: agenda` stands; `## Cross-answer check` redone as its own round-1 paragraph had said it would be; A1's licence paragraph updated now that `EP-001/Q-005` is answered
  - `tracker/items/WI-0002/item.md` — AC4 amended
  - No document under `docs/` was written by this execution
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both of the stakeholder's answers on WI-0001 are consumed and propagated, and the item returns to `draft`. `envel` stands as the command name, now by their choice; envelope names match ignoring case, keep the capitalisation they were created with, may contain spaces, and may not be empty — four criteria that could not be written before this answer. Refinement is not finished: `refinement-qa.md` remains `status: agenda` and two assumptions in it have still never been put to the stakeholder.

## 2026-09-10T13:38:24Z — refine v0.6.0 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` — refinement round 2, after `answer-questions` returned the item from `awaiting-answer` with both round-1 questions answered
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md` (read first: this is a return from `awaiting-answer`, not a send-back from `verifying` or `in-review`, so round 1's work stands), `journal.md` (both `refine` round 1 and `answer-questions`)
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (`status: agenda` on entry)
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered`, `answered-by: human`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — all five human answers, for the cross-answer check on the standing assumptions
  - `tracker/items/EP-001/item.md`, `WI-0002/item.md`, `WI-0003/item.md`, `WI-0004/item.md`, `WI-0005/item.md` — checked that no sibling already owns part of this scope
  - `docs/product/vision.md` (v2) — no criterion here contradicts it
  - `.claude/agile-skills/spec/dor-dod.md` §1 (R1–R12), `spec/workspace-layout.md` §1.3
- **Decisions:**
  - **Asked the stakeholder nothing, and this is the decision most worth disagreeing with.** Applying step 3's test to each remaining gap: the listing order (A1) and whitespace around a name (A3) are reversible presentation choices they would not expect to be consulted on (F-023); where the store lives, what happens to a name that would break its format, and the wording of every message are design decisions whose answer is the same whoever the stakeholder is, so they are routed to `plan`. Filing a question in order to have filed one would have halted the loop for a round and bought nothing, and inventing one is what the protocol exists to prevent. The reasoning is written into `refinement-qa.md` under "Round 2 — no question was put to the stakeholder, and why" so it can be argued with.
  - **A2 is no longer an assumption.** Round 1 chose "a duplicate name is refused, non-zero" under no licence. Answering `WI-0001/Q-002` the stakeholder wrote "I'd rather be told it already exists than end up with two" — AC5's behaviour in their own words. The tag is upgraded `[assumed]` → `[human]`, and both the Q&A and the item's `## Notes` record that it was a guess first and confirmed after, because "we were told" and "we guessed and were later told we were right" are different facts about the record.
  - **A1 stays an unlicensed assumption, and the elicitation's silence is not read as consent.** `EP-001/Q-005` invited them to raise anything unprompted; they raised three things and said nothing about listing order. That is recorded explicitly as *not* agreement. There is no standing delegation anywhere in this engagement — no answer says "whatever you think is best" about anything — so no `**Under delegation:**` line could honestly be written for A1 or A3, and R12's other form is used instead.
  - **AC11 added (A3): a name is compared and stored with surrounding whitespace removed.** `WI-0001/Q-002` settles case and says nothing about `  groceries  `. Left silent, `implement` would decide it where nobody could see; written as a criterion, the guess is visible and a disagreement has somewhere to land. The direction extends the principle they stated — being told it exists beats ending up with two — and the extension is recorded as ours.
  - **AC6 rewritten.** It said `envel list` on an empty store "writes at least one line to stdout, and that output contains no envelope name". The second clause is vacuous when no envelope exists, and it left AC9 and AC10 nothing to check. AC6 now fixes exit 0, at least one line on stdout and nothing on stderr, and names its own stdout as the reference output.
  - **AC9 and AC10 rewritten** to compare `envel list`'s stdout byte-for-byte against that reference, instead of "behaves as AC6 requires of an empty store". A criterion whose subject is another criterion must name what is read rather than gesture at it; a byte comparison is a thing a person with a terminal runs.
  - **Nothing renumbered.** AC11 was appended and AC6, AC9, AC10 rewritten in place. `grep` over `tracker/` and `docs/` found no `[src: WI-0001 ACn]` citation anywhere — the only cross-item mention is prose in `EP-001/journal.md` naming AC3, which did not move (`spec/doc-header.md` §4a).
  - **Added the store-location gap to `## Notes`, routed to `plan`.** AC3, AC6, AC9 and AC10 are unobservable unless whoever runs them can reach a clean store without destroying a real one. That is a testability constraint the criteria impose on the design, and it was not written down before; it is `plan`'s to satisfy, not the stakeholder's to answer.
- **Questions raised:** none. Round 1's two are answered and consumed; no new question was filed, for the reasons recorded in `refinement-qa.md` under "Round 2 — no question was put to the stakeholder, and why". Nothing is left `[unresolved]`; A1 and A3 are `[assumed]` under no licence, which is a recorded decision rather than an open one.
- **Commands:**
  - `grep -rn "AC[0-9]" tracker/ docs/ --include=*.md` → exit 0; no `[src:]` citation to this item's criteria exists, so the in-place rewrites of AC6, AC9 and AC10 moved nothing
  - `scripts/lint-answers --item WI-0001` → exit 0
  - `scripts/validate-workspace .` → exit 0 (one pre-existing warning, `project.commands.test-null`)
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0; the only output is the pre-existing `project.commands.test-null` warning, which is `plan`'s to clear when it sets `commands.test`)
  - `definition-of-ready` → **pass** (, criterion by criterion. **R1** pass — frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: critical`. **R2** pass — role ("someone who budgets by dividing money into named pots"), capability (set up envelopes by name and list them back), outcome ("so that the set of pots I budget into exists in the tool before I start putting money anywhere"). **R3** pass — eleven `AC<n>` checkboxes. **R4** pass — every criterion names a command, a stream and an exit status; the three that did not are AC6, AC9 and AC10, all rewritten in this execution, and no criterion contains an unmeasurable adjective. **R5** pass — six exclusions, among them renaming and deleting an envelope, which a reader would reasonably assume were included. **R6** pass — no question on this item is open; `Q-001` and `Q-002` are both `answered`. **R7** pass — `depends-on` is empty. **R8** pass — `artifacts/refinement-qa.md` declares `status: recorded`, carries both questions and both answers verbatim, and tags every entry `[human]` or `[assumed]`. **R9** pass — one coherent change: envelopes exist, are listed, and survive a restart; nothing about money. **R10** pass — two behaviours, `new <name>` and `list`, neither taking an option; the pairs are AC2, AC4, AC5, AC6, and the name-shape dimension `Q-002` introduced is covered by AC5, AC7, AC8, AC9, AC10 and AC11. **R11** pass — no criterion counts a project artefact; the only counts are "once and only once" in AC5 and AC11, which count lines of the tool's own output rather than tests or files this item may move, so no measurement citation is owed. **R12** pass — A1 and A3 each state that **nothing** licensed them and where a disagreement lands; A2 is now `[human]` and needs no licence; no `**Under delegation:**` line is written anywhere, because no standing delegation exists in this engagement to write one against.)
  - `criteria-are-decidable` → **pass** (, and here is the command for each. **AC1** `envel new groceries`; read the exit status and stderr. **AC2** then `envel list`; read stdout for a line whose only content is `groceries`, and the exit status. **AC3** `envel new a`, `envel new b`, `envel list` as three processes; read stdout for both lines. **AC4** `envel list` twice; `diff` the two stdouts, and check the lines are in ascending byte order. **AC5** `envel new groceries` twice, then `envel new Groceries`; read the exit status and stderr each time, then `envel list` and count the `groceries` lines. **AC6** `envel list` on a clean store; read exit status, stdout line count and stderr, and keep the stdout. **AC7** `envel new Groceries` on a clean store, then `envel list`; read the line. **AC8** `envel new "eating out"`, then `envel list`; read the line. **AC9** `envel new ""`, read exit status and stderr, then `envel list` and `diff` against AC6's kept stdout. **AC10** the same with `" "`. **AC11** `envel new groceries` then `envel new " groceries "`; read exit status and stderr, then `envel list` and count. Every one of these needs a clean store to start from, which is the gap now recorded in `## Notes` for `plan`.)
  - `cross-answer-consistency` → **pass** ((`lint-answers --item WI-0001` exit 0). No new answer was received this round, so the check ran backwards: A2 against `WI-0001/Q-002`, which **confirms** it; A1 against all six recorded human answers, none of which touches listing order; A3 against `WI-0001/Q-002`, which it extends without contradicting. No conflict, so nothing was put back to the stakeholder. Recorded in `refinement-qa.md`'s `## Cross-answer check` under **Round 2**.)
  - `qa-recorded-verbatim` → **pass** (`refinement-qa.md` carries both questions as asked and both answers in the stakeholder's own words, block-quoted, neither paraphrased nor tidied; every decision taken without them is tagged `[assumed]` and says what licensed it, which in all three cases is nothing. The one seam — that "refuse an empty name" came from option B's text rather than from their sentence — is called out in the file rather than smoothed over.)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC6, AC9 and AC10 rewritten; AC11 added; `## Notes` restructured into what the stakeholder answered, what is routed to `plan` (now including the store-location testability constraint), and what was decided here and on whose authority; the `R10 — combinations` paragraph extended
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `status: agenda` → `status: recorded`; A1 restructured with its unlicensed status restated; A2 upgraded to `[human]` quoting the stakeholder; A3 added; two new sections recording why round 2 asked nothing and what changed in the criteria; `## Cross-answer check` extended with round 2
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0001 is Ready. Eleven criteria, each with a command that settles it, and every Definition of Ready criterion passes without an override. Round 2 asked the stakeholder nothing and says why; three decisions on this item were taken without them, of which one (AC5) has since been confirmed in their own words and two (AC4's ordering, AC11's whitespace trimming) remain assumptions under no licence with a named landing place. `plan` inherits one constraint the criteria impose: the store's location must be reachable from a clean state, or nothing here is observable.

## 2026-09-10T13:54:30Z — plan v0.6.2 — architect

- **Item:** WI-0001
- **Trigger:** status `ready`, dispatched by `next` — the only runnable candidate; the other four work items all depend on something that is not `done`, and the epic's status has no owner
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the eleven acceptance criteria, `## Out of scope`, and `## Notes`, which is where refinement routed three design questions here rather than to the stakeholder
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — both `[human]` answers verbatim, and the three entries under "Decided without the stakeholder": A1 (listing order, unlicensed), A2 (duplicate refused, upgraded to `[human]`), A3 (whitespace trimming, unlicensed)
  - `tracker/items/WI-0001/history.md` and `journal.md` — this is a first plan, not a re-plan; no review or verification record exists to read
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-005.md` — all five, for the cross-answer check
  - `docs/product/vision.md` v2 — read in full, and read again to write the invalidation set rather than recalled
  - `docs/architecture/` and `docs/architecture/adr/` — both empty on entry apart from `.gitkeep`, so no standing ADR constrained this design and none was silently re-decided
  - `docs/process/` — empty
  - `tracker/project.yaml` — `commands.test` and `commands.lint` were both `null` on entry
  - the project's source code — there is none. `find . -name "*.py" -not -path "./.git/*"` returns only files under `.claude/`, which is the toolkit rather than this project
  - `.claude/agile-skills/spec/doc-header.md` §2, §3, §4, §4a; `spec/dor-dod.md` D7 and D13; `spec/workspace-layout.md` §5
- **Decisions:**
  - **Python 3, standard library only — `ADR-0001`.** *(decided here; the documents constrain it but do not settle it.)* The stakeholder said "Python, no services" and the vision reads "no services" at its widest, which settles the runtime and not whether the project may depend on an index. Recorded because it decides what `tracker/project.yaml` can name: `commands.test` is `python3 -m unittest discover -s tests -t .` and `commands.lint` is `python3 -m compileall -q envel tests`, and both were run before being written down. The lint command is a **syntax check and not a linter**, recorded as one rather than dressed up — `which pytest ruff flake8 pyflakes` exits 1 with no output on this machine.
  - **`envel` is reached through an executable `bin/envel`, with no install step — `ADR-0002`.** *(decided here; nothing settled it.)* Every criterion is written as a command typed at a terminal, so something called `envel` has to exist before any of them is observable. Packaging was rejected because it makes the criteria depend on a step none of them mentions and on an index that the "no services" reading says we should not need.
  - **One JSON store, and `ENVEL_FILE` before XDG before `~/.local/share` — `ADR-0003`.** *(decided here, from constraints refinement routed to `plan`.)* Two of them: AC3, AC6, AC9 and AC10 are unobservable unless a clean store is reachable without destroying a real one, which is what the override is for; and the stakeholder forbade restricting the characters in a name, which is a constraint on the **format** — one name per line dies on a name containing a newline, and JSON does not.
  - **Identity is `name.strip().casefold()`, display form is `name.strip()` as created — `ADR-0004`.** *(answered from the record; the ADR records the mechanism.)* `WI-0001/Q-002` and AC7 fix the substance. What the ADR adds is `casefold` over `lower`, and one consequence that is easy to get wrong and that the plan states explicitly: when a duplicate is refused the message names the **stored** envelope, because AC5 requires `groceries` on stderr after `envel new Groceries`, and echoing the input would put `Groceries` there.
  - **Unicode normalisation is deliberately not applied**, and is written into `ADR-0004`'s consequences and the plan's `## Out of scope` so that it reads as seen rather than missed. No criterion could observe it, and deciding it here would be deciding past the item.
  - **Six things are assumptions rather than ADRs — plan `## Assumptions` P1–P6:** the message wording, the split of exit statuses into 1 for a refusal and 2 for a usage error, using no argument-parsing library so that neither command takes an option, reporting an unreadable store rather than treating it as empty, leaving the output encoding as the environment's, and splitting three modules rather than one. Each names what reversing it costs, and each is one file. **No `**Under delegation:**` line is written against any of them**: refinement established that there is no standing delegation anywhere in this engagement, and the narrower licence for the first three is the item's own `## Notes`, which routes message wording to `plan`.
  - **AC4's ordering is implemented as refinement wrote it, and its status is carried forward rather than quietly settled.** The plan's `## Risks` records that it is an assumption the stakeholder has never confirmed and that a disagreement lands as a send-back to `refine`, not here.
  - **`docs/architecture/overview.md` was created**, because none existed and this is the first item to be planned. It describes the shape as designed and cites ADRs and criteria rather than source lines, because the source does not exist yet; step 7 of the plan gives `implement` the licence and the obligation to repair it once it does.
  - **The invalidation set has two entries and was written from a read of `docs/`.** `docs/product/vision.md`'s `## Engagement state` is `engagement-state` and belongs to the ending — three of its sentences are already false and none of them is ours to touch. `docs/architecture/overview.md` is `cited-fact`, because its table asserts what four files that do not yet exist are responsible for.
- **Cross-answer check:** Checked against: `EP-001/Q-001`, `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`, `WI-0001/Q-001`, `WI-0001/Q-002` — **compatible** in every case. This execution relied on two of them: `WI-0001/Q-002` (identity and permitted characters), which `ADR-0003` and `ADR-0004` both build on, and `WI-0001/Q-001` (the command name `envel`), which `ADR-0002` builds on. Neither ADR chooses between two things the stakeholder said; `ADR-0004` records a mechanism for what `Q-002` already decided, and no document written here reconciles one of their answers against another. `EP-001/Q-003` (an overspend is refused) and `EP-001/Q-004` (a transaction carries a date) are about money and are WI-0002's, so nothing here touches them; `EP-001/Q-005` widened the product by two items and says nothing about naming or listing.
- **Questions raised:** none. Every decision this design forced was answerable from the record or was a reversible assumption recorded under `## Assumptions`; none was irreversible or turned on intent no document records, so the third branch of the preference order was not reached.
- **Commands:**
  - `python3 -V` → exit 0, `Python 3.12.3`
  - `which pytest ruff flake8 pyflakes` → exit 1, no output — the evidence behind `ADR-0001`
  - `python3 -m unittest discover -s tests -t .` → exit 5, `NO TESTS RAN` — the recorded `commands.test`, run before being recorded; exit 5 is the runner reporting that it found nothing, which is this project's state until `implement` writes the tests
  - `python3 -m unittest discover -s tests -t .` without `tests/__init__.py` → exit 1, `ImportError: Start directory is not importable` — why that file is scaffolding rather than a convenience
  - `python3 -m compileall -q envel tests` → exit 0 clean, and exit 1 against a file containing `def f(:` — the recorded `commands.lint`, and the evidence that it checks something
  - `python3 -m compileall -q envel tests nosuchdir` → exit 0, `Can't list 'nosuchdir'` — why `envel/__init__.py` is scaffolding too
  - `python3 -c "import os, subprocess; subprocess.run(['zzprobe'], env={**os.environ, 'PATH': ...})"` → exit 0, `hi` — confirms a child process resolves a bare command name through the `PATH` in the environment it is handed, which is what lets the tests invoke `envel` in the form the criteria are written in
  - `scripts/lint-documents --rule documents-at-risk-are-enumerated --item WI-0001` → exit 0
  - `scripts/lint-answers --uncommitted` → exit 0
  - `scripts/lint-claims --uncommitted` → exit 0, after nine absolute claims in the four ADRs were repaired — seven by rewording and two by citing the command run that establishes them
  - `scripts/run-gate --skill plan --item WI-0001 --all` → exit 1, one hard gate failing: `workspace-valid`, on five instances of `doc.changelog.no-execution` and nothing else
  - `scripts/validate-workspace .` → exit 1 before the transition, exit 0 after it
- **Gates:**
  - `workspace-valid` → **fail** (`run-gate --skill plan --item WI-0001 --all` reported exactly one hard failure, `validate-workspace` exit 1 with five `doc.changelog.no-execution` errors — one for each document this execution wrote. Each says the change-log row names `plan` on WI-0001 at 2026-09-10T13:44:29Z and "WI-0001's journal has no execution of plan at all". It cannot: the journal entry is appended by the same `transition` command that runs this gate first, so the check is unsatisfiable for `plan`'s first execution on any project — and `plan` is required to create `docs/architecture/overview.md` before an item may reach `planned`. `resolved_by_move` does not list this code, so the pending move does not downgrade it, and `ready → planned` is `gated: true`, so the transition refuses. This move was therefore made with `--force`, which is why the verdicts in this bullet are the ones `run-gate` printed a moment earlier rather than ones `transition` produced. `validate-workspace .` run immediately after the move reports **0 errors**, which is the evidence that the failure was the ordering and not the workspace. This is F-084's shape, reported a second time — turn 4's `answer-questions` execution hit it on an ungated move and could carry it; a gated move cannot.)
  - `every-criterion-is-addressed` → **pass** (`## Acceptance criteria mapping` in `plan.md` has one row for each of AC1–AC11, and every row names the steps that satisfy it and the observation that demonstrates it — a specific `subprocess` result, an exact expected stdout, or a byte comparison against the AC6 reference. AC4 additionally maps to a unit test over `listing`, and the mapping records the `Zebra`/`apple` pair, where byte-wise order and alphabetical order disagree, so the criterion is checked where it could fail rather than where it cannot.)
  - `project-commands-resolved` → **pass** (`commands.test` is `python3 -m unittest discover -s tests -t .` and `commands.lint` is `python3 -m compileall -q envel tests`; both were run in this execution before being written into `tracker/project.yaml`, and both are recorded under `**Commands:**` with their outcomes. Neither exits zero without checking anything: the test runner exits 5 when it finds no tests, and the lint command exits 1 on a file that will not parse. The `project.commands.test-null` warning that has stood since workspace initialisation is cleared. `ADR-0001` records what the lint command is and is not.)
  - `decisions-recorded` → **pass** (`plan.md`'s `## Decisions and ADRs` is a table listing every choice this plan makes with where it is recorded and which branch of the preference order it came from. Four point at `ADR-0001` … `ADR-0004`; two point at answers already in the record; the remaining six point at `## Assumptions` P1–P6, each stating what reversing it costs and why that cost is one file with no data migration and no published interface.)
  - `plan-is-executable-without-you` → **pass** (advisory. Read as a stranger: each of the seven steps names the files it creates, the functions those files export, what each function does with what input, and what is true afterwards. The three things a developer would otherwise have to decide are decided in `## Approach` — that the duplicate message names the stored envelope rather than the input, that sorting is on the display name's UTF-8 bytes rather than on the identity key, and that a refused `new` returns before anything is written so no store file appears. What is deliberately left open is implementation: no function body is written here.)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule documents-at-risk-are-enumerated --item WI-0001` exit 0: 2 invalidation rows, 0 deliverable documents, 4 binding ADRs. The set was written by reading `docs/product/vision.md` and the `docs/` tree, not by recalling them; both rows leave `disposition` open for `implement`. `## Deliverable documents` says `none` because no acceptance criterion on this item is about a document, and `## Binding ADRs` names `ADR-0001` … `ADR-0004` with the clause of each that binds this change.)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0, over 5 uncommitted paths under `docs/` and 7 consumed human answers. The reading behind it is in the `**Cross-answer check:**` bullet above: every pair compatible, no contradiction to put back to the stakeholder, and no sentence in `docs/` edited because a newer answer overtook an older one.)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0. It first reported nine `claim.unsourced` errors across the four ADRs. Two were repaired by adding the citation that establishes them — `[src: run: which pytest ruff flake8 pyflakes → no output, exit 1]` and `[src: run: python3 -m compileall -q envel tests → exit 1 on a file containing def f(:]`. The other seven were absolutes in options blocks and consequence lists that were **weakening**, not repairs: "the only available syntax check", "no version metadata", "must never be shown" and the like were rewritten to say what had actually been checked. `validate-workspace`'s own citation-resolution pass over the whole workspace is clean after the transition.)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` — created: problem, approach, seven steps, the AC1–AC11 mapping, six assumptions, the decision table, a two-row invalidation set, deliverable documents (`none`), four binding ADRs, two scaffolding files, five risks, and what is out of scope
  - `docs/architecture/adr/ADR-0001-python-standard-library-only.md` v1 — created
  - `docs/architecture/adr/ADR-0002-envel-runs-from-a-launcher-script.md` v1 — created
  - `docs/architecture/adr/ADR-0003-one-json-store-and-where-it-lives.md` v1 — created
  - `docs/architecture/adr/ADR-0004-envelope-identity-is-the-folded-trimmed-name.md` v1 — created
  - `docs/architecture/overview.md` v1 — created, because none existed and this is the first item to reach `planned`
  - `tracker/project.yaml` — `commands.test` and `commands.lint` set, both run first
  - `tests/__init__.py`, `envel/__init__.py` — empty scaffolding, listed in the plan under `## Scaffolding` with the command each one lets execute
  - `tracker/board.md` — regenerated
  - a commit of the above, subject `tracker: the plan, the four ADRs and the architecture overview (refs WI-0001)`
- **Status:** `ready` → `planned`
- **Result:** WI-0001 is planned. Seven steps that name their files and their observable results, eleven criteria each mapped to a step and to a specific observation, four ADRs for the decisions that had alternatives worth naming, and six recorded assumptions for the ones that did not. `tracker/project.yaml` now names a test and a lint command that were both run before they were written down. One hard gate failed and could not pass from inside this execution: `workspace-valid` refuses a change-log row until the journal entry naming its skill exists, and that entry is written by the transition the gate guards — so the move was forced, the failure is recorded above in full, and the workspace validates cleanly the moment the entry lands.

## 2026-09-10T13:55:25Z — implement v0.6.0 — developer

- **Item:** WI-0001
- **Trigger:** status `planned`, dispatched by `next` — the only runnable candidate; no branch existed, so this is a fresh start rather than a resumption, and `history.md` shows no send-back from `verifying` or `in-review`
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC11 and `## Out of scope`
  - `tracker/items/WI-0001/artifacts/plan.md` — seven steps, the AC mapping, six assumptions, the two-row invalidation set, `## Deliverable documents` (`none`), four binding ADRs, and `## Scaffolding`
  - `tracker/items/WI-0001/history.md` — last row is `ready → planned` by `plan`; no send-back to work from
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered` and already propagated into the criteria; nothing has moved since the last journal entry
  - `docs/architecture/adr/ADR-0001` … `ADR-0004` — the four the plan names as binding
  - `docs/product/vision.md` and `docs/architecture/overview.md` — the two documents the invalidation set names
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, `commands.test` and `commands.lint`, both non-null
- **Decisions:**
  - none yet. This entry opens the execution; the work begins at plan step 1.
- **Cross-answer check:** none. This execution has edited no sentence in `docs/` yet, so no claim sourced to a human answer has been touched.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0001 main` → exit 0, branch created from the trunk at `ff0022f`
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition of this execution, against the branch head; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `lint-clean` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range on this branch is empty at this moment; there is nothing for it to inspect until the work is committed; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (advisory; there is no diff yet; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (same; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/WI-0001`, created from `main` at `ff0022f`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0001 has started on `wi/WI-0001`. Nothing has been built yet; the next entry reports the work.

## 2026-09-10T14:01:23Z — implement v0.6.0 — developer

- **Item:** WI-0001
- **Trigger:** status `in-progress`, this execution's own opening transition at 13:55:25Z; the branch `wi/WI-0001` was created from `main` at `ff0022f` and the plan's seven steps were worked in order
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC11 and `## Out of scope`; not edited, and no criterion changed
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps, `## Approach`'s three named decisions, the six assumptions, the invalidation set, `## Deliverable documents` (`none`), the four binding ADRs, and `## Scaffolding`
  - `tracker/items/WI-0001/history.md` — no send-back to work from
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md` — both `answered` and already propagated; nothing moved since the opening entry
  - `docs/architecture/adr/ADR-0001` … `ADR-0004` — the binding four; `ADR-0003` for the path order and the store shape, `ADR-0004` for identity and for the rule that a duplicate message names the stored envelope
  - `docs/product/vision.md` and `docs/architecture/overview.md` — the two documents the invalidation set names, both reopened at the point the set locates
  - `tracker/project.yaml` — `wi/` prefix, the commit convention, `commands.test`, `commands.lint`
- **Decisions:**
  - **`store.empty()` is a function rather than a module-level constant.** `load` hands its result to callers that mutate it, and a shared dict would leak one command's envelope into the next test. Inside the plan's latitude; recorded as a deviation in the report.
  - **`_check_shape` is a private helper.** The plan asked `load` to check the document's shape; putting the three failure messages in one place is how, not what.
  - **`DuplicateName` carries `existing` as an attribute.** The plan described the behaviour in prose — the message names the stored display name — without naming the mechanism. The attribute is what makes the CLI unable to reach for the input by accident.
  - **The suite was mutation-checked rather than merely run.** Four mutations, one at a time, each reverted: `identity` not folding case → 4 failures; `listing` returning the store's order → 2; `add` not refusing an empty identity → 4; the duplicate message echoing the input → 1. Self-check 1 asks whether each criterion's test would fail if the behaviour were removed, and running a green suite does not answer it.
  - **`docs/architecture/overview.md`'s dependency-direction sentence was weakened, not just re-cited.** It said `envelopes` "does not read or write files" and `store` "does not know what an envelope means" — two absolutes about what code does *not* do, which a citation cannot discharge. It now says what was checked: `cli` imports both, at `envel/cli.py:13`.
  - **`docs/product/vision.md` was not touched**, and the failing gate did not change that. Its row is `owned-by-ending`, and this skill may not write a `## Engagement state` section at any disposition.
  - **The one decision I declined to make is `Q-003`.** `claims-are-sourced` refuses the move to `verifying` over that section. Repairing it would decide who may write an engagement-state sentence, which is `spec/doc-header.md` §4a's answer and not mine, so the question is filed with four options rather than guessed at.
- **Cross-answer check:** none. This execution edited one document under `docs/` — `docs/architecture/overview.md` — and no sentence in it carries a `[src: <ITEM>/Q-nnn]` citation to a question the stakeholder answered. `scripts/lint-answers --changed-since main` → exit 0 over 7 consumed human answers. Nothing was rewritten because a later answer of theirs overtook it.
- **Questions raised:** `WI-0001/Q-003`, blocking, addressed to the architect — `claims-are-sourced` cannot pass while `docs/product/vision.md`'s `## Engagement state` section carries an unsourced absolute that `implement` is forbidden to repair.
- **Commands:**
  - `git checkout -b wi/WI-0001 main` → exit 0
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`, `OK` (on the branch head)
  - four mutation runs of the same command → exit 1 with 4, 2, 4 and 1 failures respectively; each mutation reverted with `git checkout -- <file>` and the suite returned to 24 passing
  - `python3 -m compileall -q envel tests` → exit 0
  - `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 1 commit(s) on main..wi/WI-0001 name WI-0001` at the time it was run; two commits now, both naming the item
  - `scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0, 1 document written under `docs/`, 2 named by the plan
  - `scripts/lint-answers --changed-since main` → exit 0
  - `scripts/lint-claims --changed-since main --plan-documents WI-0001` → **exit 1**, one error: `docs/product/vision.md:79 [claim.unsourced]`
  - `scripts/validate-workspace .` → exit 1 with `board.stale` and `question.blocking.not-suspended`, both resolved by this suspension
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 24 tests`, `OK`, run on the branch head after the last change. The suite is mutation-checked: four separate one-line mutations each broke between 1 and 4 tests, so it is not a suite that passes against an empty implementation.)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0. `ADR-0001` records that this is a syntax check rather than a linter, and that it does not reach `bin/envel`, which carries no `.py` extension — what covers the launcher is that every end-to-end test invokes the tool through it.)
  - `workspace-valid` → **fail** (after this move. Before it, `validate-workspace` reported `board.stale` and `question.blocking.not-suspended`; both are this suspension being made, and `resolved_by_move` downgrades the second for a move to `awaiting-answer`. The board is regenerated by the transition.; the run reported FAIL: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel/.claude/agile-skills/scripts/validate-workspace --root /home/msi/agile-skills-throwaway/envel --resolving 'WI-0001:in-progress->awaiting-answer+journal'` exited 1)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md`'s `## Acceptance criteria evidence` names a test function for each of AC1–AC11, with the assertion it makes. Two are worth naming here because they are the ones that could have been passed by an example that cannot fail: AC4 uses `apple` and `Zebra`, where byte-wise order and case-insensitive alphabetical order disagree, and AC5's case variant asserts `"groceries" in stderr` after `envel new Groceries`, which fails if the message echoes the input rather than the stored name. The mutation runs are the evidence that each can fail.)
  - `commits-reference-the-item` → **pass** (`scripts/check-commit-refs WI-0001 wi/WI-0001` exit 0. Two commits on `main..wi/WI-0001`: `34b69df` the code and the tests, `38e0a31` the report, the overview repair and this question. Both subjects carry `(refs WI-0001)`.)
  - `no-unplanned-scope` → **pass** (advisory. Every hunk traces to a plan step: steps 1–4 are `envel/store.py`, `envel/envelopes.py`, `envel/cli.py` and `bin/envel`; steps 5–6 the two test modules; step 7 the overview. Outside those, the diff touches `plan.md`'s two disposition cells, `impl-report.md` and `Q-003`. Nothing was tidied, and nothing unrelated was fixed.)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --changed-since main` exit 0 over 1 changed path under `docs/` and 7 consumed human answers. See the `**Cross-answer check:**` bullet: no sentence sourced to a stakeholder answer was edited.)
  - `claims-are-sourced` → **fail** (`scripts/lint-claims --changed-since main --plan-documents WI-0001` exit 1. **Scope, as the run printed it:** 2 documents in 2 paths — 1 path differing from `main` under `docs/`, plus 2 documents named by WI-0001's plan; citations resolved over every markdown file in the workspace. That is a window that could have contained something and did, so this is not F-076's shape. The single error is `docs/product/vision.md:79 [claim.unsourced] an absolute claim ('no') about 'EP-001/Q-001' with no citation`, inside `## Engagement state`. The sentence is an engagement-state claim, whose obligation under `spec/doc-header.md` §4a is to be owned at the ending rather than to carry a citation; `implement` may not write that section at any disposition; and `review-close` is several items away. There is no repair available to this skill, so the item is suspended on `Q-003` rather than forced or guessed at.)
  - `document-writes-are-declared` → **pass** (`scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` exit 0: 1 document written under `docs/` on this branch, 2 named by the plan. Both invalidation entries are closed — `docs/architecture/overview.md` `to-update`, `docs/product/vision.md` `owned-by-ending` — and no `## Engagement state` section was edited.)
- **Artifacts:**
  - branch `wi/WI-0001`, commits `34b69df..38e0a31`, both naming the item
  - `envel/store.py`, `envel/envelopes.py`, `envel/cli.py`, `bin/envel` — created
  - `tests/test_envelopes.py`, `tests/test_cli.py` — created, 24 cases
  - `docs/architecture/overview.md` v1 → v2, with a change-log row
  - `tracker/items/WI-0001/artifacts/plan.md` — the two `disposition` cells, and nothing else
  - `tracker/items/WI-0001/artifacts/impl-report.md` — created
  - `tracker/items/WI-0001/questions/Q-003.md` — created, blocking, addressed to the architect
- **Status:** `in-progress` → `awaiting-answer`
- **Result:** WI-0001's code is finished, committed and green: 24 tests, every one of AC1–AC11 mapped to a named test function, and the suite shown to fail under four separate mutations. Eight of the nine gates pass on the branch head. The ninth, `claims-are-sourced`, refuses over an unsourced absolute in a section of `docs/product/vision.md` that this skill is forbidden to touch, so the item is suspended at `awaiting-answer` on `Q-003` with `resume-to: in-progress` rather than forced through.

## 2026-09-10T14:06:54Z — answer-questions v0.6.2 — architect

- **Item:** WI-0001
- **Trigger:** status `awaiting-answer`, dispatched by `next` step 3 — `WI-0001/Q-003` is `open` and `addressed-to: architect`, and it is the only answerable question in the workspace
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-003.md` — the whole question, including its four options and its recommendation; `Q-001.md` and `Q-002.md`, both `answered` and both consumed in an earlier turn, re-read for the cross-answer check
  - `tracker/items/WI-0001/item.md`, `history.md` (the suspending row carries `resume-to: in-progress`), `journal.md` (both `implement` entries)
  - `tracker/items/WI-0001/artifacts/plan.md` — the invalidation set and its two closed dispositions; `artifacts/impl-report.md` — the gate section and the document audit rows; `artifacts/refinement-qa.md`
  - `docs/architecture/adr/ADR-0001` … `ADR-0004` — checked that no recorded decision is contradicted by this answer; none of the four is about documents or gates
  - `docs/product/vision.md` v2 — read, and specifically the `## Engagement state` section the gate reports on; **not edited**
  - `docs/architecture/overview.md` v2
  - `.claude/agile-skills/spec/doc-header.md` §4a and §5, `spec/dor-dod.md` D7, D12 and DE6, `spec/question.md` §2 and §4, `.claude/agile-skills/pipeline.yaml`, and `scripts/lib/claims.py`
- **Decisions:**
  - **`Q-003` is answered from the record, and the record settles it the other way from the gate.** Route 1 of the preference order, twice over. `spec/doc-header.md` §4a puts an **engagement-state statement** in its own row of the three-kinds table: it is falsified by "the engagement's own act, not any code change", so what it owes is to be owned at the ending rather than a citation. `spec/dor-dod.md` D12 — the criterion `lint-claims` rule 2 mechanises — says "Engagement-state sentences are out of scope: no item audit is charged with one", and scopes the citation obligation to "absolute claims **this execution** wrote", which WI-0001 did not: `intake` wrote that section four executions ago. The sentence owes nothing it is missing.
  - **The gate is wider than the rule it enforces, for two independent reasons, and each was verified rather than asserted.** `scripts/lint-claims` rule 2 does not skip paragraphs inside a delimited `## Engagement state` section, although `scripts/lint-documents` finds one for three other rules. And its code-token test asks whether a backticked token contains `/` (`scripts/lib/claims.py:148`), so a question ID reads as a named code object — `looks_like_code("EP-001/Q-001")` returns `True`, run and confirmed.
  - **Option A is refused, not merely discouraged.** It proposes that the architect repair the sentence. This skill's step 5b forbids writing an engagement-state sentence "not even when their answer made one false", and `engagement-state-is-left-to-the-ending` is a **hard gate on this execution** — so the architect who took option A would fail their own gate on the execution that answered the question.
  - **Option B does not survive being written down**, which the asker had already said. `envel new` and `envel list` now exist, so "Nothing has been designed or built" is false *because of this change*, which is precisely what D7 requires the set to record. Dropping the row to narrow the window would hide a real invalidation in order to pass a check about invalidations.
  - **Option C, on option D's diagnosis.** `implement` records `claims-are-sourced` as **failed**, with the scope line the run printed and the error verbatim, names `Q-003` as its evidence, and makes the `in-progress → verifying` move with `--force` so the override lands in the history reason. The finding stays open and clears when `review-close` restates every `## Engagement state` section at the engagement's ending (`spec/dor-dod.md` DE4) — the actor and the moment that own it.
  - **The convention is written into `docs/process/ways-of-working.md` rather than left in a question file.** `verify` and `review-close` will meet the same error on this item — `review-close` runs `lint-claims --all` — and the plans of WI-0002 through WI-0005 will name `docs/product/vision.md` for the same D7 reason and be refused the same way. The asker re-reads the documents, not the Q&A, which is the whole of why propagation is a step. The section states four conditions and says plainly what the convention is not.
  - **The enumeration falsified my own sentence before it was published, and that is worth recording.** Condition 2 was first drafted as "no skill this pipeline defines is permitted to make the change that would clear it". Enumerating the nine skills `pipeline.yaml` declares showed that **two** of them may: `intake` writes the initial `## Engagement state` section and did write this one, and `review-close` restates every such section at an ending. Neither is dispatchable now — there is no open request to route and no ending to declare with five children in flight — but "forbidden" and "not dispatchable" are different facts. The sentence was weakened to what was actually checked before it was written down, and `## Consequences` carries the enumeration with its command's output.
  - **No ADR.** Nothing here decides anything about `envel`. This is a process convention, which is what `docs/process/` is for, and an ADR trail padded with non-decisions is unreadable.
  - **No new item.** The answer widens nothing: no work is implied that no item records. The toolkit defect is not this project's to fix, and filing a `work-item` against `envel` for a change to `scripts/lint-claims` would put work on this board that this board cannot do.
- **Cross-answer check:** Checked against: none — no human answer was consumed by this execution. `Q-003` is `addressed-to: architect` and is answered by `answer-questions`, so ADR-0008 §4's obligation does not arise. The two human answers on this item, `WI-0001/Q-001` and `WI-0001/Q-002`, were re-read anyway to confirm this answer contradicts neither: the first fixes the command name and the second the identity rule, and neither is about documents, gates or the engagement's state. `scripts/lint-answers --item WI-0001` → exit 0 over 2 consumed human answers. No sentence sourced to one of their answers was edited by this execution.
- **Questions raised:** none. Nothing was re-addressed to the human: no condition in `spec/question.md` §4 applies, because the record is not silent — it answers this twice, in `doc-header.md` §4a and in `dor-dod.md` D12 — and nothing here is irreversible or contradicts a recorded decision.
- **Commands:**
  - `python3 -c "from claims import looks_like_code; print(looks_like_code('EP-001/Q-001'))"` → `True` — the second half of the diagnosis
  - `python3 -c "... miniyaml.load(pipeline.yaml)['skills']"` → `['next', 'intake', 'refine', 'plan', 'implement', 'verify', 'review-close', 'answer-questions', 'retro']` — the enumeration's own command
  - `scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0001 --uncommitted` → exit 0; 3 quantified sentences newly written into `docs/`, against 1 enumeration entry, 0 unanswered
  - `scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → exit 0; 1 document in the window, compared region by region against HEAD
  - `scripts/lint-answers --item WI-0001` → exit 0
  - `scripts/lint-claims --uncommitted` → exit 0, after three unsourced absolutes in the new document were repaired — two by citing the spec clauses they rest on and one by weakening a sentence the enumeration had shown to be false
  - `scripts/validate-workspace .` → exit 1 before this move on `board.stale`, `question.awaiting.none-open` and one `doc.changelog.no-execution`; the first two are this move being made
- **Gates:**
  - `answer-is-propagated` → **pass** (`Q-003`'s `## Consequences` names four files and each was opened afterwards. `docs/process/ways-of-working.md` exists at v1 and contains the four conditions. `plan.md`'s invalidation set now has three rows: the `vision.md` row records the unsourced absolute and who clears it, and the new `ways-of-working.md` row is disposed `to-update`. `item.md`'s `## Notes` carries the answer and states that no criterion changed. `docs/product/vision.md` is named as **deliberately unchanged**, which is a consequence a reader has to be able to see.)
  - `answered-from-the-record` → **pass** (route 1, from two documents that agree: `spec/doc-header.md` §4a's three-kinds table gives an engagement-state statement the obligation "own it at the ending", and `spec/dor-dod.md` D12 puts such sentences out of scope for an item audit and scopes the citation obligation to claims "this execution wrote". Both are quoted in `## Answer`. The record was not silent, so no ADR was owed — and none was written, deliberately: nothing here decides anything about `envel`.)
  - `escalation-is-justified` → **skipped** (no question was re-addressed to the human by this execution. `spec/question.md` §4's four conditions were each considered and none applies: the record is not silent, nothing is irreversible, no ADR is contradicted, and no intent of the stakeholder's is at stake — this is a question about the pipeline's own rules, which is the one kind the human has no privileged view of.)
  - `propagated-claims-carry-their-obligation` → **pass** (`scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0001 --uncommitted` exit 0: 3 quantified sentences newly written into `docs/`, 1 enumeration entry, 0 unanswered. The entry is nested under the file's own row in `Q-003`'s `## Consequences` and carries all five labels. Its `Falsifier:` is not decorative — the boundary it names is `intake` and `review-close`, the two skills that *may* write the section, and checking there is what showed the sentence to be false and got it weakened before publication.)
  - `engagement-state-is-left-to-the-ending` → **pass** (`scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` exit 0, comparing region by region against HEAD. `docs/product/vision.md` was not opened for writing at all, and the new `docs/process/ways-of-working.md` has no `## Engagement state` section. The three false sentences in `vision.md` are recorded in `plan.md`'s invalidation set as `owned-by-ending` and in `Q-003`'s consequences, and nothing else was done to them.)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --item WI-0001` exit 0 over 2 consumed human answers. See the `**Cross-answer check:**` bullet — no human answer was consumed here, and the two standing ones were re-read and contradict nothing in this answer.)
  - `workspace-valid` → **fail** (`validate-workspace` reports three errors before this move. Two — `board.stale` and `question.awaiting.none-open` — are this move being made and are downgraded by `resolved_by_move`. The third is `docs/process/ways-of-working.md:71 [doc.changelog.no-execution]`: the change-log row names `answer-questions` on WI-0001 at 14:03:56Z, and this item's journal has no `answer-questions` entry closing after 13:34:01Z, because the entry that would is the one this command appends. That is F-084 again, on the second skill in two turns; `plan` hit it at 13:54 and recorded it too. This move is not `gated`, so the transition carries it, and `validate-workspace` run immediately afterwards is the evidence that the failure was the ordering.)
  - `item-resumed-correctly` → **pass** (the suspending row, `2026-09-10T14:01:23Z in-progress → awaiting-answer`, records `resume-to: in-progress`, and that is where this move returns the item — read off the history row rather than inferred from which skill asked. `Q-003` was the only blocking question on the item and it is now `answered`, so nothing holds the suspension open.)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply deferred anything. `Q-003` was addressed to the architect, not to the human, and it is answered outright with a decision and four named consequences; step 3a's two moves were not reached.)
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-003.md` — `status: open` → `answered`, `answered-by: answer-questions`, with `## Answer` and a `## Consequences` carrying the enumeration
  - `docs/process/ways-of-working.md` — **created**, v1
  - `tracker/items/WI-0001/artifacts/plan.md` — the `vision.md` invalidation row extended; a third row added for `ways-of-working.md`, disposed `to-update`
  - `tracker/items/WI-0001/item.md` — `## Notes` extended; no acceptance criterion touched
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `in-progress`
- **Result:** `Q-003` is answered from the record, and the record disagrees with the gate: an engagement-state sentence owes its restatement at the ending rather than a citation, so `docs/product/vision.md:79` is not in breach of anything and is not this item's to repair. `implement` resumes at `in-progress` to record `claims-are-sourced` as failed with `Q-003` as its evidence and force the move to `verifying`. The convention that licenses that, and the two-part diagnosis of the toolkit defect underneath it, are written into `docs/process/ways-of-working.md` so the four items behind this one do not each rediscover them.

## 2026-09-10T14:10:45Z — implement v0.6.0 — developer

- **Item:** WI-0001
- **Trigger:** `in-progress`, dispatched by `next` — the only runnable candidate; WI-0002 to WI-0005 are all `draft` behind a `depends-on` that is not `done`, and EP-001's `open` has `owner: null`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC11, unchanged by this execution
  - `tracker/items/WI-0001/history.md` — the send-back is not a send-back: `answer-questions` returned the item to its recorded `resume-to` of `in-progress` at 14:06:54Z
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps, the three-row invalidation set, the four binding ADRs, `## Deliverable documents` (none)
  - `tracker/items/WI-0001/artifacts/impl-report.md` — written by the previous round of this skill
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all `answered`
  - `docs/process/ways-of-working.md` v1 — the convention `Q-003`'s answer established
  - `docs/architecture/overview.md` v2, `docs/product/vision.md` (read only)
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`
  - the branch `wi/WI-0001` at `cce3852`: `bin/envel`, `envel/store.py`, `envel/envelopes.py`, `envel/cli.py`, `tests/test_cli.py`, `tests/test_envelopes.py`
- **Decisions:**
  - **Reconciled rather than restarted.** The branch already carried every one of the plan's seven steps, complete and committed by the previous round of this skill. Nothing was rebuilt. What this execution added is the discharge of `Q-003` and the report at the branch head.
  - **Recorded `claims-are-sourced` as failed and forced the move**, which is `Q-003`'s answer word for word and is the convention in `docs/process/ways-of-working.md`. Each of its four conditions was checked against this run rather than assumed: (1) `spec/dor-dod.md` D12 — *"Engagement-state sentences are out of scope: no item audit is charged with one"* — puts the finding outside the rule rule 2 mechanises; (2) the enumeration of all nine skills in `pipeline.yaml` is in `Q-003`'s `## Consequences`, and the two that may write such a section, `intake` and `review-close`, are not dispatchable with five children in flight; (3) `Q-003` carries the diagnosis, four options and the decision; (4) this entry carries the verdict as `fail` with the run's own output, and the history reason names the question.
  - **Did not repair `docs/product/vision.md:79`, at any disposition.** The row stays `owned-by-ending`. The override is not a repair and the finding stays open until `review-close` restates the section at the ending (`spec/dor-dod.md` DE4).
  - **Did not narrow the plan's invalidation set** to shrink `--plan-documents`' window. That was `Q-003`'s option B and it does not survive: `envel new` and `envel list` are built, so *"Nothing has been designed or built"* is false because of this change, which is exactly what D7 requires the set to record.
  - Escalated and did **not** decide: nothing new. `Q-003` was the only decision this item met that was not the developer's, and it is answered.
- **Cross-answer check:** none. This execution edited no sentence in `docs/` at all — `docs/architecture/overview.md` was repaired by the previous round and `docs/process/ways-of-working.md` written by `answer-questions`; the only files it wrote are `artifacts/impl-report.md` and this record. `scripts/lint-answers --changed-since main` → exit 0 over 7 consumed human answers, 0 delegations.
- **Questions raised:** none. `Q-003` was raised by the previous round and is `answered`.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests in 1.108s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `scripts/validate-workspace .` → exit 0, `checked 6 item(s), 7 document(s)`, `0 errors, 0 warnings`
  - `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 4 commit(s) on main..wi/WI-0001 name WI-0001` (5 after this entry's commit)
  - `scripts/lint-answers --changed-since main` → exit 0, `0 errors, 0 warnings`
  - `scripts/lint-claims --changed-since main --plan-documents WI-0001` → **exit 1**, `1 error, 0 warnings`
  - `scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0, `2 document(s) written under docs/ on this branch; 3 named by the plan`
  - `git diff --stat main...wi/WI-0001` → 15 files, every one traceable to a plan step or to the invalidation set
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`, `OK`, on the branch head; four one-line mutations each broke between one and four of those tests, so the suite can fail)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md` `## Acceptance criteria evidence` names a test function for each of AC1–AC11 — `test_ac1_new_exits_zero_and_writes_nothing_to_stderr` through `test_ac11_surrounding_whitespace_is_trimmed_before_comparing` — and the mutation runs are the evidence each of them can fail)
  - `commits-reference-the-item` → **pass** (`scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0)
  - `no-unplanned-scope` → **pass**, advisory (the branch's 15 paths: four source files are steps 1–4, two test modules steps 5–6, `docs/architecture/overview.md` step 7, `docs/process/ways-of-working.md` invalidation row 3, and the rest is this item's own tracker record)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --changed-since main` → exit 0, 7 consumed human answers, 0 delegations)
  - `claims-are-sourced` → **fail**, recorded and overridden per `WI-0001/Q-003`. **Scope the run printed:** `3 document(s) in 3 path(s) in scope — 2 path(s) differ from main (ff0022f) under docs, plus 3 document(s) named by WI-0001's plan; citations: every markdown file in the workspace`. **The single error, verbatim:** `docs/product/vision.md:79: ERROR [claim.unsourced] an absolute claim ('no') about 'EP-001/Q-001' with no citation`. Line 79 is inside a `## Engagement state` section this item did not write and did not falsify, and `implement` may not write one at any disposition. Evidence for the override: `WI-0001/Q-003`, answered by the architect, and the four conditions in `docs/process/ways-of-working.md`. The finding is **not repaired** and clears only when `review-close` restates the section at the ending (`spec/dor-dod.md` DE4)
  - `document-writes-are-declared` → **pass** (`scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/impl-report.md` — updated at the branch head: the gate's own output, the four conditions discharged, and a `## Documents` row for `docs/process/ways-of-working.md`
  - branch `wi/WI-0001`, commit range `ff0022f..cce3852` — five commits, all naming WI-0001; not merged
- **Status:** `in-progress` → `verifying`
- **Result:** WI-0001 is built, green and reported, and moves to `verifying` with eight of nine hard gates passing on the branch head. The ninth, `claims-are-sourced`, is recorded as failed with its own output and the move forced, which is what `WI-0001/Q-003` decided; `verify` inherits a known, named failure over a sentence no dispatchable skill may repair, rather than a surprise.

## 2026-09-10T14:17:31Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** `verifying`, dispatched by `next` — the only runnable candidate, WI-0002 to WI-0005 all sitting behind a `depends-on` that is not `done`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1–AC11, read **first** and before the implementation report, so that what would settle each criterion was derived from its own sentence
  - `tracker/items/WI-0001/artifacts/plan.md` — the binding ADR list, the three-row invalidation set, `## Assumptions` P1–P6, `## Risks`
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the criteria and after the runs, as the claim to be checked rather than the evidence
  - `tracker/items/WI-0001/history.md`, `questions/Q-001.md`, `Q-002.md`, `Q-003.md`
  - `docs/architecture/adr/ADR-0001` … `ADR-0004`, each in full, `## Decision` quoted
  - `docs/architecture/overview.md` v2, `docs/process/ways-of-working.md` v1, `docs/product/vision.md` — the three invalidation-set documents, reopened, none written
  - `tracker/project.yaml` — `commands.test`, `commands.lint`
  - the branch head **`6aacc951fbd9fa1b82ec797869a7065d097d7d20`**, and the code on it: `bin/envel`, `envel/cli.py`, `envel/envelopes.py`, `envel/store.py`, `tests/test_cli.py`, `tests/test_envelopes.py`
- **Decisions:**
  - **No send-back and no bug item.** All eleven criteria pass on evidence this execution produced. WI-0001 is the epic's first item, so there is no behaviour delivered elsewhere that this change could have broken — the send-back/bug classification had only one live branch.
  - **No criterion judged `ambiguous` and none `substituted`.** Every one of AC1–AC11 names an observation this environment can actually make: a process invocation, its exit status, and its bytes on stdout or stderr. AC3's "each a separate invocation of the process" was honoured literally — three real invocations — rather than approximated in-process, and AC6's reference stdout was captured to a file and reused verbatim for AC9 and AC10, which is what "byte-identical" asks for.
  - **Chose the discriminating case over the happy path, twice.** AC4 was exercised with `Ant`, `Zebra`, `apple`, where byte-wise order and case-insensitive alphabetical order **disagree**, so a wrong sort cannot pass. AC5's case half was checked for the **absence** of `Groceries` from stderr, which is what ADR-0004 rule 1 turns on and the one thing an implementation that echoed its input would fail.
  - **`ADR-0002`'s "four statements" aside was recorded, not repaired and not sent back.** The file has five Python statements; the four acts the clause names are each satisfied and each cited, so the decision holds and the verdict is `conforms`. `verify` writes no document, no acceptance criterion covers it, and it is not behaviour delivered elsewhere, so it is an observation in `## Defects found` for `review-close` rather than a round of its own.
  - **Declared a coverage gap rather than ticking around it.** Mutation M3 showed that no end-to-end test creates an envelope from a name with surrounding whitespace — AC11's storage half. The behaviour is correct and this execution demonstrated it by hand, and the unit test `test_add_stores_the_trimmed_name_as_typed` is sensitive to it, so it is written into `## Test sensitivity check` for WI-0002 rather than sent back.
  - **Re-ran `implement`'s forced gate rather than taking the override on trust.** `lint-claims` still fails on the same single line, and `git diff main...HEAD -- docs/product/vision.md` is empty — so the finding is independently confirmed to be about a document this branch never wrote.
- **Questions raised:** none. No criterion was ambiguous, and the two observations recorded are neither ambiguities nor defects.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests in 1.014s`, `OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`
  - `git rev-parse HEAD` → `6aacc951fbd9fa1b82ec797869a7065d097d7d20`; `git status --short` → empty
  - AC1–AC11, each in a fresh `mktemp -d` with `PATH="$PWD/bin:$PATH"` and `ENVEL_FILE` inside it: `envel new groceries` → exit 0, empty stderr (0 bytes); `envel list` → exit 0, `od -c` `g r o c e r i e s \n`; `envel new a`/`envel new b`/`envel list` → `a \n b \n`; `envel new Zebra`/`apple`/`Ant` then `envel list` twice → `Ant`,`Zebra`,`apple`, `cmp` identical; `envel new groceries` repeated → exit 1, `envel: an envelope named 'groceries' already exists`; `envel new Groceries` → exit 1, same message; `envel list` on a store confirmed absent with `test -e` → exit 0, one line, empty stderr; `envel new Groceries` fresh → `G r o c e r i e s \n`; `envel new "eating out"` → `e a t i n g   o u t \n`; `envel new ""` → exit 1, then `cmp -s` against the AC6 reference → identical; `envel new "   "` → the same; `envel new "  groceries  "` after `groceries` → exit 1, one exact `groceries` line, no surrounding space
  - beyond the criteria: `envel` → exit 2; `envel new` → exit 2; `envel new a b` → exit 2; `envel list extra` → exit 2; `envel frobnicate` → exit 2, `envel: unknown command 'frobnicate'`; `printf 'not json at all' > $ENVEL_FILE; envel list` → exit 1, `is not valid JSON`; `envel new x` on the same → exit 1 **and the file left byte-for-byte unchanged**
  - `python3 -c` over `ast` for every `Import`/`ImportFrom` in `envel/`, `tests/` and `bin/envel` against `sys.stdlib_module_names` → `non-stdlib, non-local imports: none`
  - six mutations, each applied and reverted: M1 `listing` sorts by `casefold` → 2 failures; M2 `identity` drops `casefold` → 4; M3 `display` drops `strip` → 2; M4 the duplicate message echoes the input → 1; M5 `load` raises on an absent file → 10; M6 `add` stops refusing an empty identity → 4. `git status --short` empty and `Ran 24 tests`, `OK` after each
  - `sed -n '<n>p'` on all ten citations in `docs/architecture/overview.md` `## The shape`, and `wc -l < bin/envel` → 11
  - `scripts/lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 1 before the report existed (`document.adr.section.missing`), then exit 1 on two rows lacking a `file.ext:line` token, then **exit 0**, `4 binding ADR(s), 4 conformance row(s)`
  - `scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0001` → **exit 0**, `3 invalidation entr(y/ies) against 3 row(s)`
  - `scripts/lint-claims --changed-since main --plan-documents WI-0001` → exit 1, the same single `docs/product/vision.md:79` error `implement` recorded; `git diff main...HEAD -- docs/product/vision.md` → empty
- **Gates:**
  - `tests-pass` → **pass** (this execution ran `python3 -m unittest discover -s tests -t .` on `6aacc95` → exit 0, `Ran 24 tests`, `OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md` `## Criteria` carries, for each of AC1–AC11, the command this execution ran and its actual output — `od -c` and `cmp` where the criterion says "only content" or "byte-identical". `impl-report.md` is cited nowhere as evidence)
  - `negative-cases-exercised` → **pass** (AC5 duplicate exact and by case, AC6 missing store confirmed missing first, AC9 empty name, AC10 whitespace-only, AC11 duplicate after trimming — each triggered; plus seven boundary conditions no criterion covers, including a corrupt store on both commands with the file checked afterwards)
  - `a-criterion-about-criteria-is-read` → **pass** (, vacuously and by enumeration (AC1–AC11 were enumerated and the subject of every one is a command's exit status, stdout or stderr; none has an acceptance criterion as its subject, and this is the epic's first item so there are no earlier criteria to cover))
  - `adr-conformance-is-decided` → **pass** (`scripts/lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 0; four rows, each quoting the clause and naming a `file.ext:line`, including the boundary case for ADR-0004 rule 1)
  - `invalidation-set-is-disposed` → **pass** (`scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0001` → exit 0; three entries, three rows. The `owned-by-ending` row is backed by an empty `git diff main...HEAD -- docs/product/vision.md`, and both `to-update` rows were reopened citation by citation)
  - `tests-would-fail-without-the-change` → **pass** (, advisory (six mutations, every one caught, at least one per criterion; the one gap M3 exposed is named in the report rather than glossed))
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — created, with `Verified-commit: 6aacc951fbd9fa1b82ec797869a7065d097d7d20`
  - `tracker/items/WI-0001/item.md` — AC1 through AC11 ticked `- [x]`, all eleven, each against a command in this report. No criterion was reworded
  - no bug item filed, no question filed, nothing written under `docs/`
- **Status:** `verifying` → `in-review`
- **Result:** WI-0001 passes verification on every one of its eleven acceptance criteria, checked independently against commit `6aacc95` with the commands and outputs recorded, six mutations confirming the suite is sensitive, and one conformance verdict for each of the four binding ADRs. It moves to `in-review` carrying two recorded observations and one known-failing gate of the previous stage — `claims-are-sourced`, over an engagement-state sentence this branch never wrote, which `review-close` owns at the ending.

## 2026-09-10T14:25:34Z — review-close v0.14.0 — reviewer

- **Item:** WI-0001
- **Trigger:** `in-review`, dispatched by `next` — the only runnable candidate; WI-0002 to WI-0005 all sit behind a `depends-on` that is not `done`, and EP-001's `open` has `owner: null`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, all ten rows of `history.md`, all ten entries of `journal.md`
  - `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/verify-report.md`
  - `questions/Q-001.md`, `Q-002.md`, `Q-003.md` — all `answered`, each with `## Consequences` naming real files
  - the diff **`main..wi/WI-0001`**, hunk by hunk, fifteen paths; and the branch at `26b1be6`
  - `docs/architecture/adr/ADR-0001` … `ADR-0004` in full, `## Decision` and `## Consequences`
  - `docs/architecture/overview.md` v2, `docs/process/ways-of-working.md` v1, `docs/product/vision.md` v2 — enumerated with `find docs -name "*.md"` → seven documents, all seven opened
  - `tracker/project.yaml`
- **Decisions:**
  - **Accept, outcome `delivered`.** All eleven criteria are ticked with evidence, the record chains without a gap, and every hunk in the diff traces to a criterion or a plan step.
  - **Filed `BUG-0001` rather than sending the item back.** `envel new "café"` raises an unhandled `UnicodeEncodeError` out of `store.save` and prints a traceback under a locale that decodes `argv` with surrogate escapes. The classification test is whether an acceptance criterion of *this* item says the behaviour should be different: none of AC1–AC11 does, so it is a bug against delivered behaviour with `found-in: WI-0001`, not a send-back. Two things came with it — the store is **not** corrupted, so `ADR-0003`'s atomic write holds under the failure it was written for; and the plan predicted this area and predicted the **wrong failure**, calling it a display problem when `envel list` under the same locale is fine.
  - **Filed `Q-004`, non-blocking, to make two accepted gaps dispatchable.** `store_path`'s XDG and home branches are exercised by no test, and nothing end-to-end creates an envelope from a name with surrounding whitespace. Neither is a defect and neither is `review-close`'s to fix — its only creation authority is a `bug` at `ready`, which neither of these is. A gap that names an owner and lives only in `review.md` is inert, so the owner is named and the question is what dispatches them.
  - **Two gaps disposed `no-owner`, and meant.** The message wording (plan assumption P1 owns it, and the criteria deliberately leave the sentence open) and concurrent writes (the vision scopes the product to one person at one terminal). Neither is work deferred.
  - **Recorded `ADR-0002`'s "four statements" against a five-statement file, and did not act on it.** `verify` found it; I agree with its `conforms` verdict, because the four *acts* the clause names are each satisfied and each cited. `review-close` does not supersede ADRs, and this is a loose sentence in a decision's prose rather than a contradiction between the change and the decision.
  - **Named the one hunk that will drift and filed nothing for it.** `print(f"envel: {problem}", file=sys.stderr); return REFUSED` appears three times in `envel/cli.py` (`:47`, `:61`, `:71`), and WI-0002, WI-0004 and WI-0005 each add a command. Nothing is wrong today; inventing a refactor item is the scope creep this review exists to catch rather than commit, so it is a finding for WI-0002's plan to decide before there are six copies.
  - **Trial-merged before closing, and checked the trunk had not moved.** `git rev-parse main` → `ff0022f` before and `ff0022f` after, and the worktree was created `--detach` so it could not fast-forward the real branch.
- **Cross-answer check:** none — this execution consumed no human answer and wrote nothing under `docs/`. It quoted `WI-0001/Q-002` (*"don't restrict the characters"*) inside `BUG-0001` and inside `Q-004`, both of which are new tracker artifacts rather than edits to a sentence sourced to an answer, so ADR-0008's third row cannot apply. The seven human answers already consumed in this workspace were re-read together while auditing the claims and nothing in them conflicts; `scripts/lint-answers --context work-item --changed-since main` → exit 0 over all seven.
- **Questions raised:** `WI-0001/Q-004`, non-blocking, addressed to the architect — whether the two test-coverage gaps become work or are accepted as limitations.
- **Commands:**
  - `git worktree add --detach <trial> main` → exit 0; `git -C <trial> merge --no-ff wi/WI-0001` → clean; `git -C <trial> rev-parse HEAD` → `17993b5`; `python3 -m unittest discover -s tests -t .` **inside the trial** → exit 0, `Ran 24 tests in 0.986s`, `OK`; `python3 -m compileall -q envel tests` inside the trial → exit 0; `git worktree remove --force <trial>` → exit 0
  - `git rev-parse main` → `ff0022f0cc3321af4c3918089c09dd8499934601`, before **and** after the trial
  - `scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0, *"verified at 6aacc951; wi/WI-0001 has moved to e92d188a but only the record changed"*
  - `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 7 commit(s) on main..wi/WI-0001 name WI-0001`
  - `scripts/check-epic-signoff WI-0001` → exit 0, *"WI-0001 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."*
  - `scripts/lint-claims --context work-item --changed-since main` → exit 0
  - `scripts/lint-answers --context work-item --changed-since main` → exit 0, 7 consumed human answers, 0 delegations
  - `scripts/lint-documents --rule engagement-state-is-restated --item WI-0001 --context work-item` → exit 0, *"NOT APPLICABLE — an item close is not an ending"*
  - `scripts/lint-documents --rule accepted-gaps-are-dispatchable --item WI-0001` → exit 0, `4 accepted gap(s)`
  - `scripts/validate-workspace .` → exit 0, `checked 7 item(s), 7 document(s)`, `0 errors, 0 warnings`
  - `scripts/new-item --id BUG-0001 --type bug --found-in WI-0001 --actor review-close --status ready` → exit 0; `scripts/journal-entry BUG-0001 --skill review-close` → exit 0
  - the D12 audit's own runs: an `ast` walk over every import in `envel/`, `tests/` and `bin/envel` against `sys.stdlib_module_names` → `none`; `bin/envel` replaced with `def f(:` → suite **exit 1, 10 failing cases** while `compileall` stayed **exit 0**, then restored; `envel/_broken.py` containing `def f(:` → `compileall` **exit 1**, then removed; `envel new "  eating out  "` on a fresh store → `eating out` listed and `"name": "eating out"` in the store file
  - the boundary that found the bug: `env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C ... envel new "café"` → exit 1 with an unhandled `UnicodeEncodeError` at `envel/store.py:66`; the same under `LC_ALL=C` alone → exit 0; `envel list` under the broken locale against a store holding `café` → exit 0
- **Gates:**
  - `definition-of-done` → **pass** (D1–D13 walked one at a time in `review.md` `## Definition of Done`, each with its own result and its own evidence. D7 is confirmed against the plan's enumerated set plus the question the set cannot answer for itself; D13 asks completeness only, conformance being `verify`'s and already recorded)
  - `engagement-state-is-restated` → **pass** (applicable — an item close.** WI-0001 is a work item, EP-001 is `active` with five children in flight, and the workspace's only `## Engagement state` section — `docs/product/vision.md` — was not touched by this close. `lint-documents` says the same in its own words)
  - `accepted-gaps-are-dispatchable` → **pass** (`scripts/lint-documents --rule accepted-gaps-are-dispatchable --item WI-0001` → exit 0. Five rows: one `item-filed:BUG-0001`, two `question-filed:WI-0001/Q-004`, two `no-owner` that are limitations rather than deferrals)
  - `verification-postdates-the-code` → **pass** (`scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `6aacc95`, and everything since is `tracker/` and `docs/`. Run, not judged by how the last commits looked)
  - `commits-reference-the-item` → **pass** (`scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 7 commits on `main..wi/WI-0001`)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` run **inside the trial worktree** at `17993b5`, the merge result rather than the branch → exit 0, `Ran 24 tests`, `OK`. `compileall` there too → exit 0)
  - `workspace-valid` → **pass** (`scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`)
  - `record-is-reconstructible` → **pass** (, answered from the tracker, `docs/` and `git log` alone. *What was built and why:* two commands and a JSON store, because the stakeholder budgets into named pots and wanted the pots to exist before any money moves — `item.md` `## Story`, `docs/product/vision.md`. *Which skill decided what:* `refine` fixed AC4's ordering and AC11's trimming under no licence and said so; `plan` decided the launcher, the store path and the identity rule in `ADR-0001` … `ADR-0004` and took P1–P6 as recorded assumptions; `implement` chose three private mechanisms it names in `## Deviations`; `answer-questions` decided `Q-003` from `spec/` and wrote `docs/process/ways-of-working.md`. *What questions arose and how they resolved:* `Q-001` the command name and `Q-002` envelope identity, both answered by the human and propagated into AC5 and AC7–AC10; `Q-003` the forced gate, answered by the architect; `Q-004` open and non-blocking. *What verification found:* eleven passes on its own commands, six mutations, and one coverage gap it declared rather than glossed)
  - `claims-are-sourced` → **pass** (. **Scope, quoted from the run:** `checked absolute claims: 2 document(s) in 2 path(s) differ from main (ff0022f) under docs; citations: every markdown file in the workspace` → exit 0. That is a scope that could have found something — the two documents this branch actually wrote. It is also the reason this gate passes here while `implement`'s failed: `--plan-documents` widened that one to `docs/product/vision.md`, which this branch never touched)
  - `cross-answer-consistency` → **pass** (`scripts/lint-answers --context work-item --changed-since main` → exit 0, `checked 7 consumed human answer(s) and 0 delegation(s)`)
  - `epic-sign-off` → **pass** (`scripts/check-epic-signoff WI-0001` → exit 0 — a work item, not an epic; the termination gate applies to an engagement's ending only. EP-001 was asked separately and reports `active`, so there is no ending to declare)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` — what was examined, the seven-claim D12 audit with a falsifier on each, D1–D13, the invalidation-set confirmation and its closing question, three findings, five disposed gaps, and the verdict
  - `tracker/items/WI-0001/questions/Q-004.md` — open, non-blocking, to the architect
  - `tracker/items/BUG-0001/` — the bug, at `ready`, with its own journal entry
  - `tracker/items/WI-0001/item.md` — the outcome, written by this transition
- **Status:** `in-review` → `done`
- **Result:** WI-0001 is accepted and closed as `delivered`. The branch trial-merged cleanly into `main` with the suite green on the merge result and the trunk unmoved; the real merge follows this transition and `scripts/record-merge` puts its sha in `item.md`. It closes carrying one bug filed against it, one open non-blocking question, and three findings a reader can act on — and the engagement stays `open` with four children still to build.

## 2026-09-10T14:34:08Z — answer-questions v0.6.2 — architect

- **Item:** WI-0001
- **Trigger:** `WI-0001/Q-004` is `status: open` and `addressed-to: architect`, which is
  `next` step 3's answerable shape; dispatched by `next`. The item itself is `done` and was never
  suspended for this question, because it is non-blocking — `review-close` filed it as it closed
  the item.
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-004.md` — the question, its two gaps and its three options
  - `tracker/items/WI-0001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the answered ones, read
    for the cross-answer check and for what the stakeholder said about names
  - `tracker/items/WI-0001/item.md`, `history.md`, `artifacts/review.md` (`## Accepted gaps`,
    `## Invalidation set confirmation`, D11–D13)
  - `tracker/items/BUG-0001/item.md` — criteria AC1–AC4 and `## Notes`, to decide whether it is
    the code the gaps cover
  - `tracker/items/WI-0002/item.md` — criteria AC1–AC7, to test the question's recommendation
  - `docs/process/ways-of-working.md` (v1), `docs/architecture/overview.md` (v2),
    `docs/product/vision.md` (v2)
  - `envel/store.py` (`store_path`, `load`, `save`), `tests/` (two test modules, 199 lines; there
    is no `tests/test_store.py`)
  - `.claude/agile-skills/pipeline.yaml` — the creation rows, for `review-close`'s authority;
    `.claude/agile-skills/spec/question.md`, `spec/journal-and-history.md`,
    `spec/dor-dod.md` D11 and §3
- **Decisions:**
  - **Q-004 — decided here (route 3: the architect decides), as option B with the host item
    corrected from `WI-0002` to `BUG-0001`.** Option B's shape is right — a gap of this size
    belongs on an item that is already opening the code — but its named host was wrong on the
    record's own evidence: WI-0002's seven criteria act on envelopes that already exist and name
    neither the creation path nor `store_path`, while `BUG-0001` is `found-in: WI-0001`, fixes a
    defect inside `envel/store.py`, re-verifies all eleven of WI-0001's criteria in its AC4, and
    already asks in AC2 for an end-to-end `envel new` case with an awkward name. Rejected A
    because a full five-skill round for roughly fifteen lines of test spends the pipeline on
    process while four of the six things the tool is for are unbuilt; rejected C because gap 1's
    risk — a silent regression sending a person's store to the wrong path — becomes live in the
    very item that opens that file.
  - **The two cases land as plan steps on `BUG-0001`, not as new acceptance criteria.** Widening
    an existing item's criteria to swallow work found elsewhere hides the change from the board
    and is forbidden this skill (SKILL.md step 3b). Its `## Notes` carry them, which is what
    `plan` reads, and the note says explicitly that AC1–AC4 are unchanged.
  - **No new work item was filed.** Step 3b's route is for an answer that implies work no item
    records; this answer assigns already-recorded work to an item that exists, so filing a fifth
    sibling would have been option A under another name.
  - **The decision is recorded as a convention in `docs/process/ways-of-working.md`, not as an
    ADR.** An ADR enters every later plan's `binding-adrs` question and every later `verify`'s
    per-ADR conformance verdict, which is machinery for decisions about how the product is built.
    This is a decision about where a test lands. The precedent is this project's own: `Q-003` was
    answered the same way and `review-close` confirmed that document in WI-0001's invalidation set.
  - **`artifacts/review.md` was deliberately left unedited.** Its two gap rows are disposed
    `question-filed:WI-0001/Q-004`, which is still exactly what happened; the outcome lives at the
    end of that link. Rewriting a closed item's review to restate a later answer would replace a
    true record of the review with a summary of it.
  - **No acceptance criterion was amended, on any item.** WI-0001 is `done` and its criteria are
    frozen; BUG-0001's stay about the traceback.
- **Cross-answer check:** none — `Q-004` is `addressed-to: architect` and is answered by this
  skill from the record, so no stakeholder answer was consumed and there is nothing of theirs this
  could contradict. The two nearest stakeholder answers were read anyway, because the gaps touch
  behaviour they decided: `WI-0001/Q-002` ("I want spaces — 'eating out' is one of mine — so don't
  restrict the characters") is what gap 2's whitespace case is about, and this answer adds a test
  for it and changes no criterion; `EP-001/Q-001` ("no network for anything") is untouched. Neither
  conflicts, and neither is amended. `lint-answers --item WI-0001` reports the two consumed human
  answers on this item and no error.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → the clock behind `answered-at` and the change-log row
  - `grep -nE "^- \[ \] AC[0-9]+" tracker/items/WI-0002/item.md` → seven lines, AC1–AC7
  - `grep -nE "creat|new envelope|store_path" tracker/items/WI-0002/item.md` → one line, the
    frontmatter `created:` field; no criterion
  - a scan of every `- from: null` block in `.claude/agile-skills/pipeline.yaml` → six creation
    rows, one of them `review-close`'s (`to: ready`, `applies_to: [bug]`)
  - `ls tests/`, `wc -l tests/*.py` → two modules, 199 lines, no `tests/test_store.py`
  - `.claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation
    --item WI-0001 --uncommitted` → exit 0
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending
    --uncommitted` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 (`board.stale`), then exit 0
  - `.claude/agile-skills/scripts/board-gen .` → exit 0, wrote `tracker/board.md`
- **Gates:**
  - `answer-is-propagated` → **pass** — `Q-004`'s `## Consequences` names four files and each was
    opened after the edit: `tracker/items/BUG-0001/item.md` carries the two new `## Notes` bullets
    and `updated: 2026-09-10T14:31:05Z`; `docs/process/ways-of-working.md` carries
    `## Where an accepted test-coverage gap goes` at `version: 2` with its change-log row;
    `tracker/items/WI-0001/item.md` carries the new `**Answered by the architect, after this item
    closed:**` bullet; the fourth entry records `artifacts/review.md` as deliberately unedited and
    says why, which is a consequence and not an omission
  - `answered-from-the-record` → **pass** — the answer cites `tracker/items/WI-0002/item.md`
    AC1–AC7, `tracker/items/BUG-0001/item.md` AC2 and AC4 and its `found-in`, `envel/store.py:27`
    and `:58`, `docs/product/vision.md`, and `spec/dor-dod.md` §3's *"An accepted gap is
    dispatchable or it is nothing"*. Where the record was silent — which of three dispositions to
    take — the decision is recorded, as a convention in `docs/process/ways-of-working.md` rather
    than an ADR, with the reason for that choice written in the answer
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human. None of
    `spec/question.md` §4's four conditions applies: this is a reversible engineering disposition
    of test coverage, it contradicts no ADR, and it commits the project to nothing that a later
    plan cannot undo by moving the two cases elsewhere and saying so
  - `propagated-claims-carry-their-obligation` → **pass** — `lint-documents --rule
    propagated-claims-carry-their-obligation --item WI-0001 --uncommitted` → exit 0, "5 quantified
    sentence(s) newly written into docs/, against 3 enumeration entr(y/ies) … 0 unanswered". Two
    enumerations were written by hand for the two sentences in the new section that are claims over
    a family — `review-close`'s single creation row, and WI-0002's seven criteria naming neither
    the creation path nor `store_path` — each with its set, the command's own output, the members,
    a verdict and a falsifier that could have appeared, since both enumerating commands printed
    every row and every match rather than searching for the expected one
  - `engagement-state-is-left-to-the-ending` → **pass** — `lint-documents --rule
    engagement-state-is-left-to-the-ending --uncommitted` → exit 0, one document in the window
    compared region by region against HEAD. No `## Engagement state` section was written, amended,
    or moved into or out of; this answer falsified no engagement-state sentence, because it is
    about where a test lands and not about the state of the engagement
  - `cross-answer-consistency` → **pass** — `lint-answers --item WI-0001` → exit 0, "checked 2
    consumed human answer(s) and 0 delegation(s)". The `## Cross-answer check` section records
    `none` with the reason, which is the honest result for a question the architect answered
  - `workspace-valid` → **pass** — `validate-workspace .` → exit 0, 7 items and 7 documents, after
    `board-gen` cleared the one `board.stale` error the three `updated` bumps caused
  - `item-resumed-correctly` → **skipped** — this item was never suspended for `Q-004`. The
    question is `blocking: false` and was filed by `review-close` in the same execution that closed
    the item; WI-0001's last history row is `in-review → done`, carries `resume-to: —`, and this
    execution appends no row. There is no `resume-to` for the gate to compare against
  - `a-deferral-is-not-an-answer` → **skipped** — no reply defers. `Q-004` was answered by this
    skill from the record, not by a stakeholder saying "later"
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-004.md` — `## Answer`, `## Cross-answer check` and
    `## Consequences` written, the latter with two enumeration entries;
    `status: answered`, `answered-at: 2026-09-10T14:30:41Z`, `answered-by: answer-questions`
  - `tracker/items/BUG-0001/item.md` — two `## Notes` bullets: the two test cases its plan carries
    as steps, and the statement that they are steps and its AC1–AC4 are unchanged. `updated` bumped
  - `docs/process/ways-of-working.md` — v1 → v2, `## Where an accepted test-coverage gap goes`
    added, with a `## Change log` row naming this skill and WI-0001
  - `tracker/items/WI-0001/item.md` — one `## Notes` bullet recording where this item's two
    accepted gaps went. `updated` bumped. No criterion changed
  - `tracker/board.md` — regenerated
  - `tracker/items/WI-0001/artifacts/review.md` — unchanged, deliberately
- **Status:** `done` → `done` (unchanged)
- **Result:** WI-0001's last open question is answered. Its two accepted test-coverage gaps are
  now `BUG-0001`'s to close, as steps in the plan that item does not yet have, and the convention
  that put them there is written down where the next review can find it. Nothing is open on
  WI-0001 and no item's status changed.
