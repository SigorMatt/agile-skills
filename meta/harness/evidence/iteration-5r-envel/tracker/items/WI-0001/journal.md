# Journal — WI-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T02:00:18Z — intake v0.5.2 — product-analyst

- **Item:** WI-0001
- **Trigger:** invoked directly on the stakeholder's stated idea; this skill is not dispatched on a status
- **Inputs read:**
  - `IDEA.md` — the stakeholder's statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty of items before this execution
- **Decisions:**
  - See `EP-001`'s entry of this execution for how the work was split and why. This item is the 'money in' half: naming envelopes, funding them, and reading what is in each. It is first because nothing else can be recorded until envelopes exist.
  - Its acceptance criteria are deliberately rough and some are explicit placeholders for answers not yet given; padding them into something that looked finished would have invented requirements the stakeholder never stated.
- **Questions raised:** none on this item; `EP-001/Q-001` through `EP-001/Q-006` were filed on the epic and several of them decide criteria here
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0001 --type work-item --title ... --epic EP-001` → exit 0, item created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`.claude/agile-skills/scripts/validate-workspace .` run after the whole execution; see `EP-001`'s entry)
  - `epic-has-success-measures` → **pass** (decided once for this execution against `EP-001`'s `## Success measures`; see `EP-001`'s entry)
  - `an-open-question-was-asked` → **pass** (`lint-answers --item EP-001 --require-elicitation` → exit 0)
  - `engagement-state-is-delimited` → **pass** (`lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md` → exit 0)
  - `items-are-separable` → **pass** (this item's place in the build order and what it depends on are stated under **Decisions:** above)
  - `no-solution-in-the-problem` → **pass** (the story and criteria name no technology the stakeholder did not; see `EP-001`'s entry for what was removed)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` (new)
  - `tracker/items/WI-0001/journal.md`, `tracker/items/WI-0001/history.md` (new, by `new-item`)
- **Status:** — → `draft`
- **Result:** Created at `draft` by this intake execution. It is not Ready: `refine` is what makes each criterion decidable, and some of them wait on the stakeholder's answers to the questions on `EP-001`.

## 2026-09-11T02:04:54Z — refine v0.6.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** status `draft`, dispatched by `next` (step 4, the runnable item with the best selection key)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md`, `history.md`, `journal.md` — a fresh draft created by `intake`, not a send-back; `history.md` has one row, `— → draft`
  - `tracker/items/WI-0001/artifacts/` — no `refinement-qa.md` existed
  - `tracker/items/EP-001/item.md` and `questions/Q-001.md` … `Q-006.md` — what is already open with the stakeholder, so that this round does not re-ask it
  - `docs/product/vision.md` (v1)
  - `spec/dor-dod.md` §1 — walked criterion by criterion
- **Decisions:**
  - **The stakeholder is not in this session, so this execution files rather than converses** (precondition 2). Everything below is an agenda and a set of asks; `artifacts/refinement-qa.md` carries `status: agenda` and says in its first paragraph that nothing in it was said by anyone. Writing `recorded` on it would have made R8 pass on a conversation that never happened, which is the failure F-031 named.
  - **Four questions, each tied to a failing Definition of Ready criterion, and each one the stakeholder's rather than ours.** `Q-001` (a name that already exists) because one plausible answer silently destroys a balance; `Q-002` (how amounts are written and shown) because it decides whether a month's figures can add up exactly and it is visible in every line of output; `Q-003` (zero and negative income) because a negative income is a correction route arriving by the back door while corrections are still an open scope question; `Q-004` (how names are matched) because getting it wrong splits one envelope into two. They share one opening frame and the fourth says it is the last, so three files read as one conversation (F-020).
  - **Two things `WI-0001` needs were deliberately not asked, because they are already open on the epic**: the command's name (`EP-001/Q-006`) and whether corrections and transfers are in this version (`EP-001/Q-005`). Re-asking tells a stakeholder their answer was not heard (F-023).
  - **Two things were decided here rather than asked, and both say plainly that nothing licensed them** (R12's no-licence form): envelopes list alphabetically, and listing with no envelopes prints a line saying so and exits 0. Neither changes what the tool can do, each costs one line of code to change, and `refinement-qa.md` names where a disagreement lands — AC3 and AC6. There is no standing delegation in this engagement to spend, and none was claimed.
  - **Two questions were routed to `plan`, not to a person**: where the data is stored and in what format (including what happens when that file is missing, empty or unreadable), and whether the store is written atomically. The answer would be the same whoever the stakeholder was, so they are design, and they are in `## Notes` for `plan`'s preference order.
  - **Added AC6** so that the empty-listing case is a criterion rather than an assumption nobody can check, and recorded in `## Notes` exactly which answer settles each of AC1–AC3. The criteria were **not** rewritten into decidable form this round: every rewrite depends on an answer that has not arrived, and inventing the wording now would produce criteria that read as settled and were not.
  - **Checked the renumbering obligation** before adding AC6: `grep -rn 'WI-0001 AC' tracker docs` found no citation of this item's criteria anywhere, and AC6 was appended rather than inserted, so nothing moved under an existing citation.
- **Questions raised:** `WI-0001/Q-001`, `Q-002`, `Q-003`, `Q-004` — all blocking, all addressed to the human, all open; recorded in `artifacts/refinement-qa.md`. None is `[unresolved]` yet, because none has been asked twice.
- **Commands:**
  - `grep -rn 'WI-0001 AC' tracker docs` → exit 1, no matches (no citation of this item's criteria to re-read after adding AC6)
  - `.claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0, 0 consumed human answers, 0 delegations
  - `.claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition against the state the move produces)
  - `definition-of-ready` → **fail** (, criterion by criterion: R1 pass (frontmatter complete, `type`/`epic`/`priority` set); R2 pass (role, capability and "so that" outcome all present); R3 pass (AC1–AC6, labelled, checkboxes); **R4 fail** — AC1, AC2 and AC3 name no observation, because what to type is `EP-001/Q-006` and what is accepted is `Q-002`/`Q-003`; R5 pass (`## Out of scope` names spending, reporting, renaming and transfers, and the storage format); **R6 fail by design** — four blocking questions were filed by this execution, which is what suspends the item; R7 pass (`depends-on` empty); **R8 fail** — `refinement-qa.md` exists but declares `status: agenda`, honestly, because no conversation has happened; R9 pass (one coherent change: create, fund, list); **R10 fail** — the combinations are now *visible* (duplicate name, zero and negative amounts, amount format, name matching) but four of them are open questions rather than stated behaviours; R11 pass (no criterion counts anything); R12 pass (two assumptions, both declared as taken under no licence, each naming where a disagreement lands))
  - `criteria-are-decidable` → **fail** (AC4 is decidable today (run the three commands in separate invocations and compare the listing), AC5 is decidable today (add income to a name that was never created; expect a refusal naming it and no new envelope), AC6 is decidable today (list on a fresh store; expect a line saying there are none and exit 0). AC1, AC2 and AC3 are not: nobody can say what to type until `EP-001/Q-006` is answered, and nobody can say what is accepted until `Q-002` and `Q-003` are.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001` → exit 0; no human answer has been consumed on this item yet, so there was nothing to check anything against — `Checked against: none` is the honest state and the questions filed carry no answers)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` records the four questions, what was assumed and under what authority, and what was routed to `plan`; nothing is tagged `[human]` because nothing was said by a human, and the file says so in its opening paragraph)
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` (new)
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` (new, `status: agenda`)
  - `tracker/items/WI-0001/item.md` (AC6 added; `## Notes` rewritten with what each open question settles, the two unlicensed assumptions, and the design questions for `plan`)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0001` is not Ready and this execution did not pretend otherwise: R4, R6, R8 and R10 fail, and every one of them is waiting on the stakeholder. Four questions went to them as one ask, the item is suspended at `awaiting-answer`, and it resumes at `draft` for a second refinement round when the answers arrive.

## 2026-09-11T02:21:32Z — answer-questions v0.6.3 — architect

- **Item:** WI-0001
- **Trigger:** `awaiting-answer` with four replies in the question files; the stakeholder answered all four between turns, so they are answerable rather than outstanding (`spec/question.md` §3 rule 4b)
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — all four, each with the stakeholder's `## Answer` filled in
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0001/history.md` — the criteria the answers land in, and the row that suspended the item, whose `resume-to` is `draft`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `refine` round 1's agenda: which DoR criteria failed, what was assumed under no delegation, and what was routed to `plan`
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — the six epic answers consumed earlier today, for the cross-answer checks and because two of them (`Q-005`, `Q-006`) were named in this item's `## Notes` as things it was waiting on
  - `tracker/items/EP-001/item.md`, `tracker/items/WI-0002/item.md` — where the cross-cutting rules and the symmetric criterion had to be recorded
  - `docs/product/vision.md` v2 — checked; nothing in these four answers changes a sentence in it
  - `docs/architecture/adr/` — still empty, so no answer here could contradict a recorded decision
  - `.claude/agile-skills/spec/dor-dod.md` §1 (R8), `spec/workspace-layout.md` §1.3, `spec/question.md` §2
- **Decisions:**
  - **`Q-001` — a create of a name already taken is refused.** Route: the human answered, option A. `WI-0001` AC7 says it, including the part the option spelled out and the answer insisted on: the existing envelope is left exactly as it was, amount included. They gave a reason `refine` had not had — they will be setting up eight or ten envelopes by hand, so the second run of a create is a mistake rather than a re-run — and that reason is what rules out option B as well as option C.
  - **`Q-002` — two decimal places both ways, nothing rounded.** Route: the human answered, option A. AC8 is the accept-and-print rule; AC9 is the no-rounding rule written as something a person with a terminal can carry out — a hundred separate invocations adding `0.01` must leave exactly `1.00`, which is the observation that actually fails if amounts are held as binary floating point. Their last sentence, *"How you keep it under the hood is yours to decide"*, is a delegation of the **internal representation only**; it is recorded as that in `refinement-qa.md` and it is `plan`'s to spend, not a licence over what is accepted or printed.
  - **`Q-003` — zero and negative income are both refused.** Route: the human answered, option A, and cited their own answer to `EP-001/Q-005` as the reason there is no need for the back door. AC10.
  - **`Q-004` — names match case-insensitively, are shown as first typed, and are not restricted.** Route: the human answered, option A, and pushed back explicitly on option C's character restriction. AC13 therefore refuses only what option A itself refused — the empty name, and a leading or trailing space — and allows `eating out` and `car & bike`, which are the kind of name they said they use.
  - **Two of these four are rules that hold across the whole epic, and they are recorded once.** The amount rule (`Q-002`) and the name rule (`Q-004`) govern `WI-0002` … `WI-0005` as much as this item. Copying them into five `## Notes` sections would make five places for them to drift apart, so they are recorded on `EP-001` `## Notes` with their citations and pointed at from `WI-0002`. `refine` reads the epic when it refines a child.
  - **`WI-0002` AC6 was rewritten here, and the assumption behind it was not discharged.** `refine` had written AC6 against `WI-0001/Q-003` by symmetry, so this answer had to reach it; it now states the rule instead of naming the question. But the stakeholder was asked about **income** and answered about income. The symmetry to **spending** is still `refine`'s assumption under no delegation, and `WI-0002` `## Notes` now says so rather than letting an answered question look like it covered both.
  - **No ADR.** All four answers are the stakeholder's own words; nothing was decided by the architect. The record was not silent on any of them.
- **Cross-answer check:** `WI-0001/Q-001` checked against `EP-001/Q-002` (compatible — the same refuse-rather-than-damage posture), `EP-001/Q-005` (compatible; the apparent tension between *"nothing should ever be able to wipe money out of an envelope by accident"* and asking to correct a recorded entry turns on the word *accident*, and `WI-0005` is the deliberate route) and `WI-0001/Q-004` (compatible and interlocking — one refuses a duplicate name, the other decides which names are duplicates). `WI-0001/Q-002` checked against `EP-001/Q-003` (compatible), `EP-001/Q-001` (compatible and mutually reinforcing) and `EP-001/Q-005` (compatible). `WI-0001/Q-003` checked against `EP-001/Q-005` (compatible, and the stakeholder joined them up themselves), `EP-001/Q-002` (compatible) and `WI-0001/Q-002` (compatible — one says how an amount is written, the other which amounts mean something). `WI-0001/Q-004` checked against `WI-0001/Q-001` (compatible), `EP-001/Q-003` (compatible) and `EP-001/Q-001` (compatible). No verdict is `conflicts`, so no question was filed.
- **Questions raised:** none — all four were answered by the stakeholder and none needed re-addressing. What this item still lacks is not a stakeholder question: R4 fails because nobody has settled what to type below `envel`, what it prints and what exit code it gives, and that is `refine` round 2's to put to them as one ask.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0, 4 consumed human answers, 0 errors
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning (`commands.test` null, which is `plan`'s)
- **Gates:**
  - `answer-is-propagated` → **pass** (every file named in the four `## Consequences` sections was opened and contains the change: `WI-0001` AC7–AC13 are the four answers written as criteria; `WI-0002` AC6 is the rule instead of a placeholder and its `## Notes` records the remaining assumption; `EP-001` `## Notes` carries the two cross-cutting rules with their citations; `refinement-qa.md` is `status: recorded` with all four answers quoted verbatim and marked `human`. No `## Consequences` section names zero files)
  - `answered-from-the-record` → **pass** (each answer is the stakeholder's own text in that question's `## Answer`, quoted verbatim in `refinement-qa.md` `## Answers` and cited from every criterion it produced; the record was not silent, so no ADR was written)
  - `escalation-is-justified` → **skipped** (nothing was re-addressed to the human by this execution)
  - `propagated-claims-carry-their-obligation` → **pass** (this execution wrote nothing under `docs/`; `docs/product/vision.md` was read and left at v2. The claims it wrote are acceptance criteria and tracker notes, and the two epic-level notes carry `[src: WI-0001/Q-002]` and `[src: WI-0001/Q-004]`)
  - `engagement-state-is-left-to-the-ending` → **pass** (no `## Engagement state` section was written or amended; none of these four answers falsifies a sentence in one that the `EP-001` execution had not already recorded)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001` → exit 0, 4 consumed human answers, 0 errors; every named ID resolves and carries a verdict, and no verdict is `conflicts`)
  - `workspace-valid` → **pass** (/fail per the run this transition made** (evidence: `validate-workspace` immediately before this command reported 0 errors and the one standing warning about `commands.test` being null))
  - `item-resumed-correctly` → **pass** (the row that suspended `WI-0001` at 2026-09-11T02:04:54Z records `resume-to: draft`; this move is to `draft`. Read from the history row, not inferred)
  - `a-deferral-is-not-an-answer` → **skipped** (none of the four replies defers; each picks an option and gives a reason)
- **Artifacts:**
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — all four `answered`, `answered-by: human`, `answered-at: 2026-09-11T02:20:30Z`, each with a `## Cross-answer check` and a `## Consequences`
  - `tracker/items/WI-0001/item.md` — AC7 … AC13 added; `## Notes` rewritten from "waiting on four answers" to what each settled and what is still missing
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; all four answers quoted verbatim under `## Answers`; the round-1 table now reads `answered`; a new `## What round 1 did not settle` section names R4 as round 2's job
  - `tracker/items/EP-001/item.md` — `## Notes` gains the two epic-wide rules
  - `tracker/items/WI-0002/item.md` — AC6 rewritten; `## Notes` updated
  - no ADR created; `docs/` unchanged by this execution
- **Status:** `awaiting-answer` → `draft`
- **Result:** `WI-0001`'s four refinement answers are consumed and propagated. The item returns to `draft` with thirteen criteria instead of six: what happens on a duplicate create, how amounts are written and shown, that nothing is rounded, that zero and negative income are refused, and how names are matched and displayed. It is **not** Ready — nobody has yet settled what to type below `envel`, which is DoR R4 and `refine` round 2's ask.

## 2026-09-11T02:32:29Z — refine v0.6.1 — product-analyst

- **Item:** WI-0001
- **Trigger:** `draft` — dispatched by `next`, which picked it as the highest-ranked runnable item (priority rank 2, created 2026-09-11T01:57:11Z) after `answer-questions` returned it from `awaiting-answer` with round 1's four answers propagated.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` (AC1–AC13 as round 1's answers left them, `## Out of scope`, `## Notes`)
  - `tracker/items/WI-0001/history.md` — three rows, and the read that mattered: this is **not** a send-back from `verifying` or `in-review`. It is a fresh draft resumed at its recorded `resume-to` after an escalation, so round 2 is the continuation of round 1's agenda and not a re-opening of the story.
  - `tracker/items/WI-0001/journal.md` — `intake`'s record and round 1's, so nothing already answered was re-asked
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — round 1, including its closing sentence naming exactly what was left
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — the four answers verbatim
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` — the epic's six answers, for the cross-answer check and because `Q-006` is what the subcommand choice was made against
  - `tracker/items/WI-0002/item.md` — the sibling that cites this item's AC3, and the sibling that owns the scope this item excludes
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/doc-header.md` §4a *Citation forms*
- **Decisions:**
  - **Nothing was put to the stakeholder this round.** Round 1 left exactly one criterion failing — R4, the command surface — and step 3's test routes it away from them: it is not product stake (it changes nothing about what the tool is for, promises, or does with their money), it is not already answered, and no standing delegation covers it. `WI-0001/Q-002`'s *"How you keep it under the hood is yours to decide"* was read narrowly, as round 1 read it: the internal representation of an amount, not the surface. That leaves step 3's fourth branch, implementation-only — normally routed to `plan`, which was **rejected here** because R4 is a hard gate on this skill and *"there is some subcommand that creates an envelope"* is not decidable by someone with a terminal. So it was decided and recorded, five decisions, every one `[assumed]` under **no delegation**, each naming where a disagreement lands (`artifacts/refinement-qa.md` `## Decided in round 2`).
  - **AC1, AC2 and AC3 rewritten** from "there is an `envel` command that …" to `envel new <name>`, `envel add <name> <amount>` and `envel list`, each naming the stream it writes to and the exit code. What changed about their meaning: they went from naming a capability to naming an invocation. The verbs were chosen against `EP-001/Q-006` — they took `envel` over `envelope` because *"Short is what matters if I'm typing it several times a day"* — and for a set the rest of the epic extends without collision (`WI-0002` a spend, `WI-0003` a summary, `WI-0004` a move).
  - **AC3 also gained two things round 1 had left in `## Notes` rather than in a criterion:** the alphabetical, capitalisation-ignoring order (round 1's own assumption, which was decidable nowhere), and that there is no total line. The total line is an inference from `EP-001/Q-003`, where they refused one on the monthly summary — *"I don't need a total line for the month"* — read across to the listing rather than asked again, and marked `[assumed]` because an inference from an answer is not the answer.
  - **AC14, AC15, AC16 and AC17 added** — appended, not inserted, so no existing number moved. AC14 an unrecognised or absent subcommand; AC15 a wrong argument count, with the five concrete invocations named; AC16 the stream-and-exit-code rule stated once and checked case by case against the criteria that name each case; AC17 the form of a written amount. AC14, AC15 and AC17 are R10 gaps found by re-walking the combinations this item introduces; AC16 generalises what the stakeholder had already decided half of at `Q-001`.
  - **AC17 deliberately does not take over AC10.** A leading `-` is read as a negative amount and refused by AC10 — which is the stakeholder's decision at `Q-003` — rather than being refused as a malformed number, which would have restated their decision as a parsing rule and hidden it.
  - **The renumbering obligation was discharged.** `grep -rn 'WI-0001 AC' tracker docs` found one live citation: `WI-0002` AC2 quotes this item's AC3 by its words. AC3's wording changed under it, so the citation was requoted to the new text — `[src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and the amount currently in it"]` — and `lint-claims` re-run to confirm it resolves. Every other match is prose in journals and question files, which name AC numbers as narrative rather than citing them; each was re-read against the criterion it now points at and still says what it said.
  - **One thing left unconstrained on purpose, and recorded as such (R10):** whether two names differing only in *internal* whitespace (`eating out` against `eating  out`) are one envelope or two. AC11 settles capitalisation and AC13 settles which characters are allowed; neither reaches this. Too thin for a stakeholder round trip, too arbitrary to assume quietly, so it is named in `## Notes` with where a decision would land (AC11).
  - **Scope excluded:** creating and funding in one command (`envel new groceries 400`), and flags or options of any kind on these three commands. Both are things a reader could reasonably assume are included; both are `refine`'s call, on the authority that neither is anything the stakeholder asked for.
- **Questions raised:** none. Round 1's `Q-001`–`Q-004` are all `answered`; round 2 filed nothing, and `artifacts/refinement-qa.md` `## Round 2` records why, including the branch of step 3 that was taken and the one that was rejected.
- **Commands:**
  - `grep -rn "WI-0001 AC" tracker/ docs/` → exit 0, 19 matches, one of them a citation (`WI-0002` AC2)
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0001` → exit 0, 4 consumed human answers, 0 delegations spent
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 1 warning (`project.commands.test-null`, which is `plan`'s to settle)
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, board current
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors; the single warning is `project.commands.test-null`, addressed to `plan`, not to this item)
  - `definition-of-ready` → **pass** (, criterion by criterion. R1 pass — frontmatter complete, `type`, `epic` and `priority` set, `validate-workspace` decides it. R2 pass — the story names the role (*a person budgeting my own money at a terminal*), the capability (*create named envelopes and put income into them*) and the outcome (*so that my money is divided up the way I have decided before I start spending it*). R3 pass — AC1–AC17, labelled, as checkboxes. **R4 fail → pass**: it was the one criterion round 1 left failing, and AC1, AC2 and AC3 now name an invocation, a stream and an exit code, with AC14–AC17 covering the surface's edges; no criterion carries an unmeasurable adjective. R5 pass — `## Out of scope` now names six things, two of which a reader would reasonably assume were in (creating and funding in one command; any flags at all). R6 pass — no open question on this item; round 1's four are `answered`. R7 pass — `depends-on` is empty. R8 pass — `refinement-qa.md` exists and declares `status: recorded`, and what is in it is what happened. **R9 pass** — one coherent change: one store, one argument parser, three subcommands; spending, summaries, moving and correcting are four other items. **R10 fail → pass**: re-walking the combinations produced three that had no stated behaviour — an unrecognised or absent subcommand, a wrong argument count, and a malformed amount — now AC14, AC15 and AC17; and one deliberately left unconstrained, internal whitespace in a name, named in `## Notes` with `refine` recorded as having left it so. R11 pass — no criterion counts an artefact this item may move; AC9's *one hundred times* counts invocations of the tool under test, which is the tool's own behaviour and not a project artefact, so no measurement citation is owed. R12 pass — five assumed decisions this round, each carrying **Under no delegation** and where a disagreement lands, plus round 1's two unchanged; `lint-answers` reports 0 delegations spent on this item, which matches, because the one delegation the stakeholder did grant (`WI-0001/Q-002`, the internal representation) was deliberately not spent here.)
  - `criteria-are-decidable` → **pass** (. AC1: `envel new groceries` → a stdout line containing *groceries*, exit 0. AC2: `envel add groceries 400` → a stdout line containing *groceries* and *400.00*, exit 0. AC3: `envel list` → one line per envelope, name and amount, ordered `car`, `eating out`, `groceries` ignoring case, no total line, exit 0. AC4: run the three in three shells, then `envel list` → the envelope and its amount are there. AC5: `envel add nosuch 10` → stderr names *nosuch*, exit non-zero, and `envel list` does not list it. AC6: `envel list` on an empty store → a line saying there are none, exit 0. AC7: `envel new groceries` twice with income in between → second run stderr says it exists and names it, exit non-zero, and `envel list` still shows the same amount. AC8: `envel add g 12.5` → `12.50`; `envel add g 12.567` → refused, and `envel list` unchanged. AC9: `envel add g 0.01` a hundred times → `envel list` shows `1.00`. AC10: `envel add g 0` and `envel add g -40` → refused, `envel list` unchanged. AC11: `envel new groceries` then `envel add Groceries 10` then `envel list` → one line, 10.00. AC12: same, and the line reads `groceries`. AC13: `envel new "eating out"`, `envel new "car & bike"` → exit 0; `envel new ""` and `envel new " x"` → refused, and neither is listed. AC14: `envel` and `envel frobnicate` → stderr usage listing the subcommands, exit non-zero. AC15: the five invocations the criterion names → stderr usage, exit non-zero, `envel list` unchanged. AC16: for each case named in AC5, AC7, AC8, AC10, AC13, AC14, AC15 check `2>` is non-empty and `$?` non-zero; for AC1, AC2, AC3, AC6 check `1>` is non-empty and `$?` is 0. AC17: `envel add g 400`, `12.5`, `12.50` → accepted; `£12.50`, `1,200`, `12.5x`, `abc` → refused with `envel list` unchanged; no printed amount contains a symbol.)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0001` exit 0. The read behind it is `refinement-qa.md` `## Cross-answer check — round 2`: every criterion written this round was read against `EP-001/Q-006`, `EP-001/Q-003`, `WI-0001/Q-001`, `Q-002`, `Q-003` and `Q-004`. No contradiction was found, nothing was put back to them, and no recorded sentence of theirs was edited.)
  - `qa-recorded-verbatim` → **pass** (`refinement-qa.md` carries round 1's four answers word for word from the `## Answer` sections, marked `human`, and round 2's five decisions marked `[assumed]`, each stating **Under no delegation** and where a disagreement lands. No answer was paraphrased and no assumption is tagged as an answer.)
- **Artifacts:**
  - `tracker/items/WI-0001/item.md` — AC1, AC2 and AC3 rewritten; AC14–AC17 appended; `## Out of scope` gained two exclusions; `## Notes` rewritten to carry round 2's five assumptions, the unconstrained case, and the reason the subcommand choice was made
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — `## Round 2`, `## Decided in round 2, and by what authority`, `## Left deliberately unconstrained in round 2 (R10)` and `## Cross-answer check — round 2` added; round 1's content unchanged apart from its section heading
  - `tracker/items/WI-0002/item.md` — AC2's citation of `WI-0001` AC3 requoted to AC3's new wording, so it goes on resolving; nothing else touched
  - `tracker/board.md` — regenerated (no change; the status move is recorded by the transition that appends this entry)
  - commit: `tracker: the refined item and its Q&A record (refs WI-0001)`
- **Status:** `draft` → `ready`
- **Result:** `WI-0001` is Ready. Round 1 settled the behaviour with the stakeholder and round 2 settled the surface without them, on the ground that the surface is not theirs to decide — seventeen criteria, each with a command and a verdict, five assumptions recorded under no delegation with where each disagreement lands, and one combination left unconstrained on purpose. `plan` inherits two design questions from `## Notes`: where the data lives and what happens when that file is missing or unreadable, and whether the store is written atomically.

## 2026-09-11T02:41:29Z — plan v0.6.3 — architect

- **Item:** WI-0001
- **Trigger:** `ready` — dispatched by `next` as the highest-ranked runnable item (priority rank 2) after `refine` round 2 took it out of `draft`.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the seventeen criteria, which are this design's contract
  - `tracker/items/WI-0001/history.md` — four rows; this is a first plan, not a re-plan after a rejection
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — in particular the seven `[assumed]` entries, which are the design's soft ground, and the two questions `refine` routed here rather than to the stakeholder
  - `tracker/items/WI-0002/item.md` … `WI-0006/item.md` — what the store has to be able to carry later, which is what rules out storing a balance
  - `tracker/items/EP-001/questions/Q-001.md` … `Q-006.md` and `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — the stakeholder's twelve answers
  - `docs/product/vision.md` v2 — read in full, for the invalidation set and for the two constraints it records as requirements
  - `docs/architecture/adr/` — **empty**; there was no ADR in this project before this execution, so nothing was re-decided
  - `docs/architecture/overview.md` — **did not exist**; created by this execution, as the first planned item requires
  - `tracker/project.yaml` — `commands.test` and `commands.lint` both null
  - the project's source code — **there is none**. `find . -name '*.py'` outside the toolkit returns nothing, which is why this plan starts with the package itself.
- **Decisions:**
  - **Amounts are a whole number of cents** — `ADR-0001`. Branch: *assumed*, under the stakeholder's own delegation at `WI-0001/Q-002` (*"How you keep it under the hood is yours to decide"*), taken to cover the internal representation and nothing else. `AC9` is what rules out `float`; `Decimal` is the live alternative and the ADR says what reversing to it would cost.
  - **The store is one JSON document holding the envelopes and an append-only list of dated entries, with the balance derived by summing** — `ADR-0002`. Branch: *decided*, and it is the decision this whole plan turns on. `WI-0001` alone would be satisfied by storing a number per envelope; `EP-001/Q-003` asks the summary for *"what went in that month"* and `EP-001/Q-004` fixes that month as a calendar month namable after it has ended, and neither is derivable from a balance. The stakeholder is one person with real data in the file from the first week, so the cheap shape now is a migration of their money later.
  - **The same ADR settles the two questions `refine` routed here**: writes are atomic (temporary file in the same directory, then `os.replace`), a missing file is the empty store rather than an error — which is what makes `AC6` true on a fresh machine — and a damaged file is refused without being overwritten.
  - **The store is located by `ENVEL_FILE`, then `XDG_DATA_HOME`, then `~/.local/share`** — `ADR-0003`. Branch: *decided*. The variable is not a test hook: it is how a second budget is kept, and it happens also to make every criterion runnable against a scratch file instead of the stakeholder's own.
  - **The tool is a package plus a two-line executable shim at the repository root, with no install step** — `ADR-0004`. Branch: *decided*. A `pyproject.toml` and `pip install -e .` was the alternative and was rejected because it makes the criteria undemonstrable wherever `pip` cannot run, for a tool whose only constraint is *"Python, no services"*.
  - **Tests are `unittest` and lint is `compileall`** — `ADR-0005`. Branch: *decided, against a measurement*: `which pytest ruff flake8 pylint mypy` finds none of them here, so recording `pytest` would have recorded a command nobody has run. The ADR states plainly what `compileall` does and does not check, so no gate in this project reads as claiming more than it does.
  - **A refusal is a returned value and `envel/cli.py` is the only thing that prints one or picks an exit code.** Branch: *assumed*, recorded under `## Assumptions` with its reversal. This is what satisfies `AC16` once rather than seventeen times.
  - **Argument-shape failures are left to `argparse`** — no subcommand, an unknown one, a wrong argument count. Branch: *assumed*. `AC14` and `AC15` constrain the stream and the exit code, not the wording, and step 7 says to test them that way so a Python upgrade cannot break a test for a non-product reason.
  - **Nothing was asked of the human.** Every decision above came from the first or second branch of the preference order. None is irreversible before the stakeholder has a file, and the one that becomes irreversible afterwards — the document's shape — is exactly why it is decided now rather than deferred.
  - **`## Deliverable documents` is `none`**, deliberately: no criterion of this item has a document as its subject, so `implement` may write to `docs/` only to close a row of the invalidation set.
- **Cross-answer check:** this execution recorded no new human answer, and relied on six. Checked against each, by ID. `WI-0001/Q-002` — relied on for `ADR-0001`, and read narrowly: the licence covers how an amount is held, while what is accepted and printed is theirs and is untouched. `WI-0001/Q-003` — compatible and protected: `parse_amount` deliberately accepts a leading `-` so that a negative income is refused by the rule they gave, not by the parser. `WI-0001/Q-004` — relied on for case-folded matching and as-typed display; `ADR-0002` stores the name as typed, which is the only way both halves of their answer can hold. `EP-001/Q-003` and `EP-001/Q-004` — relied on together for `ADR-0002`: the summary's three columns over a namable calendar month are what a stored balance cannot answer. `EP-001/Q-006` — relied on for `ADR-0004`; the shim keeps the short name they chose. No two of these disagree, so nothing was put back to them and no ADR here settles anything between two things they said.
- **Questions raised:** none.
- **Commands:**
  - `which pytest ruff flake8 pylint mypy` → exit 1, no output
  - `python3 -V` → exit 0, Python 3.12.3
  - `python3 -m unittest discover -s tests -t .` → exit 5, NO TESTS RAN (correct for an empty suite; exit 0 once `implement` writes the first test)
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item WI-0001` → exit 0, 13 invalidation rows, 0 deliverable documents, 5 binding ADRs
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0 after repair, 0 errors (first run: 25 errors)
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 12 consumed human answers, 0 delegations spent
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the journal entry existed; see the note under `workspace-valid`
- **Gates:**
  - `workspace-valid` → **pass when run directly, and the transition was taken with `--force`.** Read this one in full, because the record must not overstate it.
    - Run on its own against the state this entry describes, `validate-workspace` reports **0 errors** — the state is sound.
    - It could not be made to report that *from inside the transition*, and the deadlock is F-084's, reached here for the third time in this engagement. Writing the plan's five ADRs and the architecture overview puts six `doc.changelog` rows in the workspace saying *plan changed this for WI-0001*. `doc.changelog.no-execution` checks `WI-0001`'s journal for an execution of `plan`, and the only entry that can satisfy it is the one `transition` appends **after** its gates have already run. `--resolving 'WI-0001:ready->planned+journal'` does not cover it — tested directly, same six errors.
    - Writing this entry first with `scripts/journal-entry` clears those six and produces exactly one error in their place: `journal.status.unmatched`, because the entry states a move whose history row does not exist yet. `--resolving` does not cover that one either, and dropping the `**Status:**` bullet is refused by `journal.bullet.missing` — standalone entries must carry it (`spec/journal-and-history.md` §2.2). Three positions, no legal one.
    - So the move was made with `--force`, which skips the gate run and records `[gates forced]` in the history reason for ever. **Every gate below was run by hand before that, and each passed**; the commands and their exit codes are under `**Commands:**` and can be re-run. `validate-workspace` was re-run after the transition and reports 0 errors, which is the state a reader can check now.
    - `intake` hit this in turn 2 and `answer-questions` in turn 4; `plan` is the third skill, and the three have one thing in common — the skill's propagation includes a `docs/` change on the very item it is transitioning. `implement` will not hit it, because its first move (`planned → in-progress`) is ungated and lands a journal entry before any document is written. `plan` has no ungated first move, so for the first item it plans it cannot avoid this.
  - `every-criterion-is-addressed` → **pass** (`artifacts/plan.md` `## Acceptance criteria mapping` has one row per criterion, AC1 to AC17, each naming the step that satisfies it and the specific test that will demonstrate it — never "tests". AC16 is the one that needed care: its subject is other criteria, so its row names a table-driven test walking the seven refusal cases and the four success cases by criterion ID.)
  - `project-commands-resolved` → **pass** (`tracker/project.yaml` now carries `test: python3 -m unittest discover -s tests -t .` and `lint: python3 -m compileall -q envel tests`. Both have been run in this project: the lint command exits 0, and the test command exits 5 on an empty suite, which is correct behaviour and becomes 0 with the first test. `ADR-0005` records why these two and not `pytest` and `ruff`, and measures the reason.)
  - `decisions-recorded` → **pass** (seven choices, listed in `## Decisions and ADRs` with the branch of the preference order each came from. Five are ADRs — `ADR-0001` through `ADR-0005` — and two are entries under `## Assumptions` with what reversing them costs. No choice in this plan is unaccounted for.)
  - `plan-is-executable-without-you` → **pass**, advisory (read back cold: every step names the files it touches, the functions it adds, and what is true afterwards. The place a developer would still have to decide something is message wording, which `refine` left unconstrained on purpose and the criteria constrain only by content.)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule documents-at-risk-are-enumerated --item WI-0001` exit 0: 13 rows, 0 deliverable documents, 5 binding ADRs. The set was written from a read of `docs/`, not from memory — `docs/product/vision.md` in full and every ADR this execution wrote. Four rows are `engagement-state` and are disposed `owned-by-ending`; three are `quantified`, including the vision's *"Not connected to anything"*, whose falsifier is an import the sentence does not name; the rest are `cited-fact` and left open for `implement`.)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exit 0. The read behind it is the `**Cross-answer check:**` bullet above: six answers relied on, each checked, none in conflict, and no ADR here reconciles two of their statements.)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exit 0. The first run found 25 errors and both halves are worth recording: eleven `claim.citation.unresolved` because a bare `[src: WI-0001 ACn]` is refused while the item is at `ready` and its criteria may still move — the fix is to quote the criterion's words, which is `spec/doc-header.md` §4a working as intended — and fourteen `claim.unsourced` on absolutes I had written without a source in the same paragraph. Every one was repaired by adding a citation that resolves, not by softening the sentence.)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/plan.md` — created
  - `docs/architecture/overview.md` — created, v1
  - `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — created, v1
  - `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — created, v1
  - `docs/architecture/adr/ADR-0003-store-location.md` — created, v1
  - `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` — created, v1
  - `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — created, v1
  - `tracker/project.yaml` — `commands.test` and `commands.lint` filled in
  - `envel/__init__.py`, `tests/__init__.py` — empty scaffolding, listed in the plan under `## Scaffolding`, present only so the two declared commands can execute
  - `tracker/board.md` — regenerated
  - commit: `tracker: the plan, five ADRs and the architecture overview (refs WI-0001)`
- **Status:** `ready` → `planned`
- **Result:** `WI-0001` is planned. Seven numbered steps build the package from nothing — `money`, `store`, `envelopes`, `cli`, the two entry points, and the tests — and all seventeen criteria map to a step and to a named test. Five ADRs record the decisions the rest of the epic will be built on, and the one that matters most is `ADR-0002`: the data is an entry log rather than a balance, because `WI-0003` cannot be built on a balance and changing the shape after the stakeholder has used the tool is a migration of their own money.

## 2026-09-11T02:43:44Z — implement v0.6.1 — developer

- **Item:** WI-0001
- **Trigger:** `planned` — dispatched by `next` as the highest-ranked runnable item (priority rank 2); `artifacts/plan.md` is written and carries its invalidation set, its deliverable documents and its binding ADRs.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the seventeen acceptance criteria
  - `tracker/items/WI-0001/history.md` — five rows; the last is `ready → planned`, so this is a fresh implementation and not a send-back from `verifying` or `in-review`
  - `tracker/items/WI-0001/artifacts/plan.md` — seven steps, the AC mapping table, the assumptions, the thirteen-row invalidation set, `## Deliverable documents: none`, and five binding ADRs
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — all four `answered`, all four propagated into the criteria before this execution; nothing moved since the last journal entry
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both set, so neither gate has to be invented
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` and `docs/architecture/overview.md` — the five binding ADRs and the shape they describe
  - the branch: `git branch -a` shows only `main`, so no partial work exists to reconcile with
- **Decisions:** none yet. This entry opens the execution; the work and its choices are in the closing entry.
- **Cross-answer check:** none — this execution has edited no document yet, so no claim sourced to a stakeholder answer has been touched.
- **Questions raised:** none.
- **Commands:**
  - `git branch -a` → exit 0, only `main`; no partial branch to reconcile
  - `git checkout -b wi/WI-0001` → exit 0, branched from `main`
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `lint-clean` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range is empty at this moment; there is nothing yet for it to inspect; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (, advisory; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:** branch `wi/WI-0001`, created from `main` at `7f27e61`. No file written yet.
- **Status:** `planned` → `in-progress`
- **Result:** Implementation has started on `wi/WI-0001`. Nothing is built; the next entry reports the work.

## 2026-09-11T02:52:40Z — implement v0.6.1 — developer

- **Item:** WI-0001
- **Trigger:** `in-progress` — this skill's own opening transition at 2026-09-11T02:43:44Z; the same execution, closing.
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/plan.md` — the seven steps, the AC mapping, the assumptions, the invalidation set, `## Deliverable documents: none`, the five binding ADRs
  - `tracker/items/WI-0001/item.md` — the seventeen criteria, re-read before each test was written
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — none moved since the opening entry
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` and `docs/architecture/overview.md` — read in full, both to build against and to close the invalidation set
  - `docs/product/vision.md` v2 — read in full for the same reason
  - `tracker/project.yaml` — the two commands
  - the branch `wi/WI-0001` — reconciled at the opening entry: it was at `main`, with nothing on it
- **Decisions:**
  - **The shim is `bin/envel`, not `./envel`** — the plan's step 5 and `ADR-0004` both name the repository root, and that arrangement cannot exist: a file named `envel` and the package directory `envel/` share one name. `echo hi > envel` in a directory holding `envel/` fails with *"Is a directory"*, exit 1, which is the measurement this rests on. Judged a *how* rather than a *what*: the deliverable is a runnable `envel` with no install step, and `bin/envel` delivers it — better, in fact, since putting `bin/` on a `PATH` exposes the command and nothing else. Not escalated, because nothing a user would notice changes and nothing another item depends on moves. `ADR-0004` was corrected by **erratum**, not superseded: the decision it records — a package, a shim, no install step — is untouched, and no code has to change to satisfy the new wording (`spec/doc-header.md` §4b).
  - **`Ok` carries a `changed` flag** the plan did not name. Without it `envel list` would save the store it had just read, creating the file during a read and contradicting `ADR-0003`'s *"created when the store is first written, and never on a read"*. Inside the plan's latitude; the test asserts the file is still absent after a listing.
  - **The operations deep-copy before changing anything.** The plan says each returns a new store; this makes that literally true and lets every refusal test assert the caller's document is unchanged, which is what `AC7` and `AC10` are really about.
  - **`tests/test_cli.py` runs the tool with `PATH` and `ENVEL_FILE` and nothing else**, so a stray `HOME` or `XDG_DATA_HOME` on the machine running the suite cannot reach a real store. `ADR-0003`'s three-step resolution is tested directly instead.
  - **Argument-shape failures were left to `argparse`**, as planned, and the tests assert the stream, the exit code and the substrings `AC14` names — never argparse's wording, which is not ours and changes between Python versions.
  - **Nothing was ticked in `item.md`.** The checkboxes are `verify`'s.
  - **Two toolkit workarounds were taken and written down** rather than hidden; both are in `artifacts/impl-report.md` under `## Two things the toolkit forced`. The change-log rows this execution wrote carry the execution's **opening** timestamp, because `doc.changelog.no-execution` treats an execution as closing at its last journal entry and `implement`'s second entry is written after the gates run; and `ADR-0004`'s two errata are one `## Corrections` entry, because `adr.correction.changelog` requires a version per correction and the two have one cause between them.
- **Cross-answer check:** one sentence this execution edited is sourced to a stakeholder answer, and it was **not** the repair. `docs/product/vision.md` `## What it is for` says *"The command is `envel`"* [src: EP-001/Q-006]; it was reopened, read against `bin/envel` and against `ArgumentParser(prog="envel")`, found still true, and left alone. The two documents actually repaired — `docs/architecture/overview.md` and `ADR-0004` — carry no citation to any `Q-###`, and both were false because the **code** could not be as written, which is the ordinary repair (`ADR-0008` §3, second row). No answer of theirs was overtaken by another, so nothing was put back to them.
- **Questions raised:** none.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 51 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 3 commits name WI-0001
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0001` → exit 0, 7 documents in scope
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0, 2 documents written, 7 named by the plan
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0
  - `echo hi > envel` in a directory holding `envel/` → exit 1, *"Is a directory"* (the measurement behind the shim deviation)
  - `grep -rn "^import \|^from " envel/ bin/envel` → exit 0, 15 lines (the enumeration behind the vision's network claim)
  - `grep -rnE "socket|urllib|http|requests|ssl|asyncio|subprocess" envel/ bin/envel` → exit 1, no matches
  - `grep -rn "print(\|sys\.exit\|sys\.stdout\|sys\.stderr" envel/money.py envel/store.py envel/envelopes.py` → exit 1, no matches
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 51 tests, OK, run on the branch head after the last commit)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (`artifacts/impl-report.md` `## Acceptance criteria evidence` names a test function for all seventeen; none is demonstrated by reading the code. The two that needed care are `AC9`, which is a hundred separate subprocesses rather than an in-process loop — the point is that the total survives being written and read back — and `AC16`, whose subject is other criteria, tested as subtests keyed by criterion ID so a failure names the criterion it breaks.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 3 commits on `main..wi/WI-0001` name the item)
  - `no-unplanned-scope` → **pass** (, advisory (the diff is the plan's seven steps plus four recorded deviations. Nothing for `WI-0002` to `WI-0006` was built: no spend, no summary, no move, no correction. The one hunk that looks forward is the `at` and `created` fields, which `ADR-0002` and the plan's `## Risks` both declare.))
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0, over the 2 documents this branch changed. The read behind it is the `**Cross-answer check:**` bullet above.)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0001` → exit 0. **Scope, stated because a window that could contain nothing is not a pass:** 7 documents — the 2 that differ from `main` under `docs/` plus the 7 named by the plan, deduplicated — and citations checked across every markdown file in the workspace.)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0: 2 documents written under `docs/` on this branch, both in the plan's invalidation set; every one of the now-14 entries carries a disposition; no entry disposed `owned-by-ending` had its `## Engagement state` section edited.)
- **Artifacts:**
  - `envel/money.py`, `envel/store.py`, `envel/envelopes.py`, `envel/cli.py`, `envel/__main__.py`, `bin/envel` — created
  - `tests/test_money.py`, `tests/test_store.py`, `tests/test_envelopes.py`, `tests/test_cli.py` — created, 51 tests
  - `tracker/items/WI-0001/artifacts/impl-report.md` — created
  - `tracker/items/WI-0001/artifacts/plan.md` — the `disposition` column filled in for all 13 entries, and one row appended for a vision sentence that had nothing behind it until there was code
  - `docs/architecture/overview.md` — v2, the shim row repaired
  - `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` — v2, one erratum in a new `## Corrections` section
  - branch `wi/WI-0001`, commits `7f27e61..HEAD` — 3 commits: the code and its tests, the closed invalidation set and the report, and the correction-shape fix
- **Status:** `in-progress` → `verifying`
- **Result:** `WI-0001` is built and ready to be judged. All seventeen criteria have a test that would fail if the behaviour were removed, all nine gates pass on the branch head, and the two documents this change made false are repaired while the four engagement-state sentences are left for the ending. The one thing `verify` should look at hardest is the shim deviation: the plan and `ADR-0004` both named an arrangement that cannot exist on a filesystem, and the ADR was corrected by erratum rather than superseded.

## 2026-09-11T03:05:10Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** `verifying` — `next` dispatched `verify` as the status owner; highest-ranked
  runnable item (priority `high`, no open question, no dependency).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the seventeen criteria, read **before** the implementation
    report so that what settles each one was derived from the criterion and not from the code.
  - `tracker/items/WI-0001/artifacts/plan.md` — the binding ADR list (five) and the invalidation
    set (fourteen entries).
  - `tracker/items/WI-0001/artifacts/impl-report.md` — read after the criteria, and checked
    rather than cited. Its AC14/AC15/AC16 rows are what pointed at the weakened assertion.
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` `## Round 2` — consulted because AC15's
    wording is the thing in dispute; it records the command surface as five assumptions taken
    under no delegation, and says nothing that would loosen "a usage message for that subcommand".
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, each in full.
  - The nine documents behind the `verified-still-true` entries: `docs/product/vision.md`,
    `docs/architecture/overview.md`, and the five ADRs.
  - The code at branch `wi/WI-0001`, commit `26d25ce0ee5a2b66d938163d35598c48b75ec039`.
  - `tracker/project.yaml` — the test and lint commands.
- **Decisions:**
  - **AC15 fails, and it is a send-back rather than a bug item.** The test that decides it is the
    contract's own: does an acceptance criterion of *this* item say the behaviour should be
    different? AC15 is WI-0001's, so the item is not finished and goes back to `in-progress`. No
    bug was filed.
  - **AC15 is `fail`, not `ambiguous`.** The competing reading — that any usage message printed in
    response to misusing a subcommand counts — was considered and rejected, because the criterion
    is self-disambiguating: two of the five invocations it names produce `usage: envel new [-h]
    name` and three produce the top-level `usage: envel [-h] {new,add,list} ...`. A criterion whose
    own enumerated cases split that way is decidable, so no question was filed to the architect.
  - **The sixteen passing criteria were ticked, with the risk recorded.** AC14 and AC16 are
    satisfied by the same argparse path AC15 fails on, so `verify-report.md` `## Defects found`
    states that the next verification must treat AC14, AC15 and AC16 as unverified whatever the
    ticks say.
  - **The AC16 read was done as a criterion about criteria, not as "the suite is green".** Its
    eleven named criteria were each re-run and given a verdict; the non-intersection was stated in
    those words and the covering case was demanded rather than waived.
  - **The `format_amount` insensitivity is advisory, not a criterion failure.** The behaviour is
    right — checked directly with `12.57` — so AC8 and AC9 pass. What is missing is a test, and it
    was added to the send-back rather than filed as a defect against the behaviour.
  - **Nothing under `docs/` was written.** The two `to-update` entries were read, not touched.
  - No criterion was judged `ambiguous` and none was `substituted`; every one of the seventeen was
    decided by an observation this environment could actually make.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0 (`Ran 51 tests … OK`)
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 (7 items, 7 documents, 0 errors)
  - `bin/envel new|add|list` in roughly sixty invocations across seven scratch stores under
    `/tmp/vrf/`, covering all seventeen criteria; every command, its stdout, its stderr and its
    exit code are in `verify-report.md` `## Criteria`
  - `bin/envel add pennies 0.01` × 100 separate processes, then `bin/envel list` → `pennies  1.00`,
    exit 0; the store held 100 entries
  - `python3 -m envel list` compared against `bin/envel list` on one store → byte-identical stdout,
    identical exit 0
  - `python3 -c "from envel import store; print(store.store_path())"` → the `~/.local/share` branch,
    resolved without being written to
  - `python3 -m unittest discover -s tests -t .` in an empty scratch suite → exit 5, `NO TESTS RAN`
    (ADR-0005's boundary)
  - twelve source mutations, each followed by the full suite and `git checkout -- .` → eleven
    turned the suite red, one did not; working tree confirmed clean afterwards
  - `.claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0001`
    → exit 1 on the first run (ADR-0005's row lacked a file and line), exit 0 after
  - `.claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0001`
    → exit 1 on the first run (five ADR rows keyed by ID rather than by path), exit 0 after
  - `.claude/agile-skills/scripts/lint-claims --uncommitted --context work-item` → exit 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 51 tests, run here on `26d25ce` — not taken from the implementation report)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests`, exit 0, run here)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `every-criterion-independently-checked` → **pass** (seventeen rows in `## Criteria`, each with a command this execution ran and its actual output; no row's evidence is `impl-report.md`)
  - `negative-cases-exercised` → **pass** (`## Negative and boundary cases exercised`: every refusal triggered, both edges of AC13, the boundary `0` of AC10, `12.5`/`12.567` either side of AC8's limit, a damaged store and an unknown `format`, and `ENVEL_FILE` set *alongside* `XDG_DATA_HOME` to test precedence rather than presence)
  - `a-criterion-about-criteria-is-read` → **pass** (AC16's eleven criteria named by ID with a verdict each, read from their sentences; the non-intersection stated in those words — nothing executable exercises AC15's "usage message for that subcommand" clause together with AC16's stream rule — and the covering case demanded in the send-back rather than waived)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0001`, exit 0: five verdicts for five binding ADRs, all `conforms`, each quoting a clause of `## Decision` with a file and line. `## ADR conformance` is the evidence)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0001`, exit 0: fourteen rows against fourteen entries. Nine `verified-still-true` entries reopened and read against the branch head, each quantified one with its enumeration, its per-member verdict and its falsifier; three `owned-by-ending` entries left untouched and confirmed unedited by this branch's `docs/` diff; two `to-update` entries confirmed updated with a version bump and a change-log row. `## Invalidation set` is the evidence)
  - `tests-would-fail-without-the-change` → **fail** (advisory. Eleven of twelve mutations turned the suite red. The twelfth — `format_amount` rounding the units-of-cents digit away, so `12.57` would print `12.50` — left all 51 tests passing, because every amount anywhere in the suite is a whole multiple of ten cents. AC8 and AC9 are correct in the code and undefended by the tests; recorded in `## Test sensitivity check` and carried into the send-back)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — created
  - `tracker/items/WI-0001/item.md` — sixteen criteria ticked; AC15 left unticked
  - no bug items filed; no file under `docs/` written
  - the commit of this execution's workspace files
- **Status:** `verifying` → `in-progress`
- **Result:** Sixteen of seventeen criteria pass on evidence gathered here. AC15 fails: three of
  the five invocations it names print the top-level usage rather than a usage message for the
  subcommand that was misused, and the test that should have caught it asserts only that stderr is
  non-empty. The item goes back to `in-progress` with three things to fix — the usage messages, the
  test that was weaker than its criterion, and a missing test at the cent that lets AC8 and AC9 be
  broken silently.

## 2026-09-11T03:11:14Z — implement v0.6.1 — developer

- **Item:** WI-0001
- **Trigger:** `in-progress` — `next` dispatched `implement` as the status owner. This is a
  **resumed** execution, not a fresh one: `verify` sent the item back from `verifying` at
  `2026-09-11T03:05:10Z`, so the branch already existed and the item was already at `in-progress`.
  No opening transition was taken, because there is no `in-progress → in-progress` move and the
  status was already truthful. This execution therefore writes one journal entry, at its close.
- **Inputs read:**
  - `tracker/items/WI-0001/history.md` — the last row is the send-back, which is what sent me to
    the verification report before anything else.
  - `tracker/items/WI-0001/artifacts/verify-report.md` `## Defects found` — read **first**, per
    step 1. Three defects; this execution is those three and nothing else.
  - `tracker/items/WI-0001/item.md` — AC15's exact wording, which is the thing in dispute, and
    AC14's and AC16's, which `verify` warned move with it.
  - `tracker/items/WI-0001/artifacts/plan.md` — step 4, the `## Decisions and ADRs` row about
    argparse, the invalidation set (fourteen entries, all disposed by the first execution) and the
    binding ADR list.
  - `tracker/items/WI-0001/questions/` — twelve questions, all `answered` before this execution
    began; none moved since the last journal entry, so nothing new to propagate.
  - `docs/architecture/overview.md` in full, and `docs/product/vision.md`, to decide whether this
    change falsified anything. `grep -rn "argparse\|usage\|subcommand\|argument" docs/` returns two
    lines, both in the overview, both still true.
  - `envel/cli.py`, `tests/test_cli.py`, `tests/test_money.py` — the files this execution changes.
  - `tracker/project.yaml` — the commands and the commit-subject convention.
- **Decisions:**
  - **Fixed AC15 inside the plan's decision rather than against it.** The plan says argument-shape
    failures are argparse's and not hand-written, and that stands: there is no hand-rolled parser
    and `main` validates no argument counts itself. `parse_args` became `parse_known_args`, and
    anything left over is reported through `subcommand_parsers[arguments.command].error(...)` —
    six lines. What changed is *which parser reports the failure*, which is a `how`.
  - **Did not file a question, and the reason is that AC15 already decides this.** Step 6's signs
    were walked: no interface another item depends on (nothing outside `cli.py` moves); no ADR
    contradicted (no ADR speaks about argument parsing); not behaviour a user would notice with no
    criterion covering it — AC15 covers it exactly and in words; not expensive to reverse.
  - **The plan's gloss on AC15 is wrong and I did not edit it.** The `## Decisions and ADRs` row
    says *"AC14 and AC15 constrain the stream and the exit code, not the wording"*. AC15 also says
    *"a usage message for that subcommand"* — which message, not how it reads. The criterion is
    the contract and a plan cannot narrow it, so the code follows the criterion; the design is not
    this skill's to rewrite, so the row stands and deviation 5 records it.
  - **AC14 was given the opposite assertion on purpose.** AC14 wants the tool's usage and AC15
    wants a subcommand's, so `test_no_subcommand_and_an_unknown_one` now asserts `{new,add,list}`
    is in the first line of stderr and `test_the_wrong_number_of_arguments` asserts it is not.
    The two messages cannot drift back together without a test failing.
  - **The AC15 test asserts the criterion, not argparse's prose.** The plan's step 7 warns against
    asserting argparse's exact wording, which would break on a Python upgrade for no product
    reason. The test asserts three things a usage message for a subcommand must have — the line
    starts `usage:`, it names the subcommand, it is not the tool's — and quotes none of argparse's
    sentences.
  - **Re-checked AC14 and AC16 rather than assuming them.** `verify-report.md` said they come from
    the same code path and should be treated as unverified after any fix. Both were re-run.
  - **Wrote no document.** Nothing under `docs/` was falsified by this change, so no entry was
    added to the invalidation set and no version was bumped. Recording that I looked is the work.
- **Cross-answer check:** none. This execution wrote no file under `docs/`, so no claim sourced to
  a stakeholder answer was edited. `lint-answers --changed-since main` → exit 0 over the twelve
  consumed answers.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 52 tests, OK (on branch head `81441cd`)
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 (7 items, 7 documents)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 6 commits
  - `.claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0001` → exit 0
  - `.claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0001
    --changed-since main` → exit 0
  - `bin/envel new|add|list` — the five AC15 invocations and both AC14 invocations, run by hand
    against a scratch `ENVEL_FILE`; output quoted in `impl-report.md`
  - `grep -rn "argparse\|usage\|subcommand\|argument" docs/` → 2 lines, both still true
  - three source mutations, each followed by the full suite and `git checkout -- .` → all three
    turned the suite red
  - `git commit` → `81441cd`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 52 tests, run after the last commit, on branch head `81441cd`)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests`, exit 0, same head)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (all seventeen named in `impl-report.md` `## Acceptance criteria evidence`; none rests on reading the code. AC15's test now asserts what AC15 says rather than what AC16 says, which is the defect that got here. Each of the three fixes was confirmed by mutation: reverting `parse_known_args` fails `test_the_wrong_number_of_arguments`; rounding the last cent digit away fails `test_an_amount_whose_cents_are_not_a_round_ten_is_exact` and `test_exactly_two_decimal_places`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001`, exit 0 — all 6 commits on `main..wi/WI-0001` name the item)
  - `no-unplanned-scope` → **pass** (advisory. The diff of this execution is three files: `envel/cli.py` — six lines for AC15; `tests/test_cli.py` — the AC15 and AC14 assertions and one new test; `tests/test_money.py` — two cases. Every hunk traces to AC15, AC14, AC8 or AC9. I fixed nothing I noticed on the way)
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main`, exit 0: 12 consumed human answers, 0 delegations spent. This execution edited no sourced sentence)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0001`, exit 0. **Scope the run printed:** 7 documents in 7 paths — 2 differing from `main` under `docs/`, plus the 7 named by WI-0001's plan. A non-empty window, which is the thing the gate can otherwise pass vacuously on)
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main`, exit 0: 2 documents written on the branch, both named by the plan, both from the first execution. This execution wrote none, and all fourteen invalidation entries carry a disposition. No `## Engagement state` section was touched)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/impl-report.md` — updated: a `## The second execution` section,
    amended evidence for AC8, AC9, AC14 and AC15, deviation 5, a `## Documents` paragraph for this
    execution, and a re-run gate table
  - branch `wi/WI-0001`, commits `26d25ce..81441cd` — this execution added `81441cd` (code and
    tests) and the commit of this record
  - no document under `docs/` written; no bug item filed; no question filed
- **Status:** `in-progress` → `verifying`
- **Result:** AC15's defect is fixed and the two tests that let it through are fixed with it.
  A wrong argument count is now reported by the subcommand's own parser, so all five invocations
  the criterion names print `usage: envel <subcommand> …`; AC14 still prints the tool's usage and
  its test now asserts so. The suite is 52 tests and all nine gates pass on the branch head.

## 2026-09-11T03:18:12Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0001
- **Trigger:** `verifying` — `next` dispatched `verify` as the status owner. This is the **second**
  verification of this item; the first, at `26d25ce`, failed AC15 and sent it back.
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — the seventeen criteria, read before the implementation
    report, as on the first round.
  - `tracker/items/WI-0001/history.md` — the send-back row and the return.
  - `tracker/items/WI-0001/artifacts/impl-report.md` — its new `## The second execution` section
    and deviation 5, checked rather than cited.
  - `tracker/items/WI-0001/artifacts/plan.md` — the five binding ADRs and the fourteen-entry
    invalidation set.
  - `docs/architecture/adr/ADR-0001` … `ADR-0005`, each in full, and the nine documents behind the
    `verified-still-true` entries.
  - The code at branch `wi/WI-0001`, commit `2f025c5c45b039c8c563bcbc46884e3e8b14efc4`.
  - `tracker/project.yaml` — the commands the gates run.
- **Decisions:**
  - **Re-ran all seventeen criteria, not only the three at risk.** The last report named AC14,
    AC15 and AC16 as sharing a code path with the fix, but the fix is in `main`'s first statements
    and every criterion enters through `main`, so treating the other fourteen as still verified
    would have been trusting a report rather than the code. Every row of `## Criteria` carries a
    command run against `2f025c5`.
  - **AC15 passes and is ticked.** All five invocations the criterion names print a usage message
    for the subcommand that was misused. The three that failed last time — `new a b`,
    `add groceries 10 20`, `list extra` — were each re-run.
  - **Checked the fix by mutation, not by reading the new assertions.** A test that asserts the
    right thing and a test that bites are different claims. Reverting `parse_known_args` fails
    exactly one test, which is the precise signal AC15 was missing when it shared AC16's
    assertion.
  - **Added a fourteenth mutation as a control.** The first round only ever mutated `fold()`
    wholesale, which breaks four criteria at once, so AC3's ordering clause had never been
    isolated. Ordering by the raw name instead of the folded one fails exactly
    `test_one_line_per_envelope_ordered_by_folded_name`.
  - **Re-read every invalidation entry against the new head rather than accepting the
    dispositions.** A disposition is a claim about code and the code moved. The one that could
    most plausibly have broken is the overview's *"nothing below `cli` prints"*, because the fix
    adds an error path and the tempting place for it is a lower module; it is at
    `envel/cli.py:51`, inside `cli`.
  - **Re-decided ADR-0004 with the failure path, not only the success path.** `build_parser` now
    returns a tuple and `main` changed, so `bin/envel list extra` was compared against
    `python3 -m envel list extra` as well as the `list` that both already agreed on.
  - **Filed no bug and no question.** Nothing failed, and nothing was ambiguous. No criterion was
    `substituted`; every one was decided by an observation this environment could make.
  - **Wrote no file under `docs/`.** `git diff --name-only 26d25ce..HEAD -- docs/` is empty, so
    neither this execution nor the implementation it judges touched a document.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0 (`Ran 52 tests … OK`)
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0 (7 items, 7 documents)
  - roughly fifty `bin/envel` invocations across seven scratch stores under `/tmp/vrf2/`, covering
    all seventeen criteria; every command with its stdout, stderr and exit code is in
    `verify-report.md` `## Criteria`
  - the five AC15 invocations and both AC14 invocations, run individually and quoted in full
  - `bin/envel add pennies 0.01` × 100 separate processes → `pennies  1.00`, 100 entries on disk
  - `bin/envel list extra` against `python3 -m envel list extra` → identical stderr and exit 2
  - `python3 -c "from envel import store; print(store.store_path())"` → the `~/.local/share`
    branch resolved without being written to
  - `python3 -m unittest discover -s tests -t .` in an empty scratch suite → exit 5, `NO TESTS RAN`
  - `git diff --name-only 26d25ce..HEAD -- docs/` → empty
  - fourteen source mutations, each followed by the full suite and `git checkout -- .` → all
    fourteen turned the suite red; working tree confirmed clean afterwards
  - `.claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0001`
    → exit 0
  - `.claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item
    WI-0001` → exit 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .`, exit 0, 52 tests, run here on `2f025c5`, not taken from the implementation report)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests`, exit 0, same head)
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 0 errors 0 warnings)
  - `every-criterion-independently-checked` → **pass** (seventeen rows, each a command this execution ran and its actual output; nothing carried over from the first verification and no row's evidence is `impl-report.md`)
  - `negative-cases-exercised` → **pass** (every refusal triggered: both edges of AC13, the boundary `0` of AC10, `12.5`/`12.567`/`12.57` around AC8's limit, a damaged store and an unknown `format` with both files confirmed byte-identical afterwards, `ENVEL_FILE` set alongside `XDG_DATA_HOME` to test precedence, and both entry points on a *failing* path because that is the path this round changed)
  - `a-criterion-about-criteria-is-read` → **pass** (AC16's eleven criteria named by ID with a verdict each, read from their sentences. The non-intersection the first round declared in those words is shown **closed**: AC15 now has its own covering case, confirmed by the mutation that fails exactly one test. No waiver claimed, because none is needed)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0001`, exit 0: five verdicts for five binding ADRs, all `conforms`, each quoting a clause of `## Decision` with a file and line on the new head)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0001`, exit 0: fourteen rows against fourteen entries, every one re-read against `2f025c5`, each quantified one with its enumeration, per-member verdict and falsifier; the three `owned-by-ending` entries untouched and confirmed so by an empty `docs/` diff)
  - `tests-would-fail-without-the-change` → **pass** (advisory, and it failed last round. Fourteen mutations, fourteen red suites. The two that previously survived — the AC15 fix and `format_amount`'s last cent digit — now fail, and a fourteenth was added to isolate AC3's ordering clause, which had never been mutated on its own)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/verify-report.md` — replaced. It is a statement about
    `2f025c5`; the first round's statement was about `26d25ce` and is in git history
  - `tracker/items/WI-0001/item.md` — AC15 ticked; all seventeen now ticked
  - no bug items filed; no question filed; no file under `docs/` written
  - the commit of this execution's workspace files
- **Status:** `verifying` → `in-review`
- **Result:** All seventeen acceptance criteria pass on evidence gathered here against `2f025c5`.
  AC15's defect is gone and its test now bites on its own. The advisory sensitivity gate, which
  failed last round, passes: fourteen mutations, fourteen red suites. The item goes to
  `in-review`.

## 2026-09-11T03:28:08Z — review-close v0.14.1 — reviewer

- **Item:** WI-0001
- **Trigger:** status `in-review`, dispatched by `next` (highest-ranked runnable candidate; priority `high`, created `2026-09-11T01:57:11Z`)
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — seventeen criteria, all ticked; `## Out of scope`; `## Notes`
  - `tracker/items/WI-0001/history.md` — 11 rows, chaining without a gap to `in-review`
  - `tracker/items/WI-0001/journal.md` — all 10 entries, in full
  - `tracker/items/WI-0001/artifacts/plan.md` — the design, the invalidation set, `## Deliverable documents` (`none`), `## Binding ADRs` (five)
  - `tracker/items/WI-0001/artifacts/impl-report.md` — both executions, the five deviations, `## What I did not do`
  - `tracker/items/WI-0001/artifacts/verify-report.md` — the seventeen criteria rows, `## ADR conformance`, `## Test sensitivity check`, `## Not verified, and why`
  - `tracker/items/WI-0001/questions/Q-001.md` … `Q-004.md` — all `answered`, each `## Consequences` naming files that exist
  - **the diff** `main..wi/WI-0001`, hunk by hunk: 8 commits, 19 files, 1728 insertions — `envel/money.py`, `envel/store.py`, `envel/envelopes.py`, `envel/cli.py`, `envel/__main__.py`, `bin/envel`, four test files, and the branch's changes to `docs/` and `tracker/`
  - `docs/product/vision.md`, `docs/architecture/overview.md`, and all five ADRs — end to end, for D7's own question and D12's audit
  - `tracker/project.yaml` — the trunk and the two declared commands
- **Decisions:**
  - **Accepted, with two findings and neither a send-back.** Every hunk of the diff maps to a plan step or to the AC15 send-back, so there is no unrequested scope; the five declared deviations are each a *how* rather than a *what*. Rationale for accepting deviation 5 in particular — the wrong-argument-count failure is now reported by the subcommand's parser rather than the tool's — is that it follows AC15's *"a usage message for that subcommand"* over the plan's gloss *"AC14 and AC15 constrain the stream and the exit code, not the wording"*. The criterion is the contract and a plan cannot narrow it; `implement` recorded the discrepancy instead of editing the plan to match, which is the right way round.
  - **Finding 1 is not a falsification, and I say why rather than harmonising it.** `docs/architecture/overview.md` `## The parts` says *"`cli` knows about `envelopes`, `envelopes` knows about `store` and `money`"*; the real imports are `cli` → `envelopes`, `money`, `store` and `envelopes` → `money` only. Read as an edge list its first clause is inaccurate too, so an edge list is not what it is; read as the layering statement its cited source (`plan.md` `## Approach`, *"four modules, in one dependency direction"*) supports, it is true, and its load-bearing half — nothing below reaches up — is checked at the boundary. Recorded in `review.md` `## Findings` with the real graph, so a later reader cannot take it for an edge list.
  - **Finding 2 is a boundary of a recorded decision, not a defect.** `envel new "-savings"` is refused by argparse; `envel new -- "-savings"` creates it. AC13 says a name *may contain* any character and names two examples, both accepted, so the criterion holds. Fixing it means hand-rolling the parser or special-casing a leading `-`, which overturns `plan.md`'s recorded decision to leave argument shape to `argparse` — not this skill's to do. Recorded as a finding and as an accepted gap.
  - **Four criteria were re-run rather than read**: AC15 (the one that was sent back), AC14 (the one it is the opposite of), AC7 (the one where money could be lost) and AC9 at the cent. Rationale: those are the criteria where trusting the report would have been countersigning, and AC14 in particular shares a code path with the fix.
  - **All six accepted gaps are disposed `no-owner`, and I mean it.** None names a skill or the human as owner: three are limitations of what can be observed on this machine (the real home directory, an interrupted `os.replace`, argparse's prose), one is a wording observation about AC16 whose universal sentence was checked and holds, and two are behaviours `refine` deliberately left unconstrained or that follow from a recorded design decision. Filing a question or an item for any of them would be manufacturing work nobody owes.
  - **The trial merge ran in a `--detach`ed worktree** so the trunk could not fast-forward, and `main` was confirmed still `7f27e61` after the trial was discarded.
- **Cross-answer check:** `none` — this execution consumed no human answer. The four answers on this item (`Q-001`…`Q-004`) were consumed by `answer-questions` at `2026-09-11T02:21:32Z` and propagated then; this review read them as context for what the criteria mean and took no new one. `lint-answers --context work-item --changed-since main` → exit 0 over 12 consumed answers and 0 delegations spent.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` (branch head) → exit 0, 52 tests, OK
  - `python3 -m compileall -q envel tests` → exit 0
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0
  - `.claude/agile-skills/scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 8 commits
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0001` → exit 0 (not an epic)
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated --item WI-0001 --context work-item` → exit 0, NOT APPLICABLE
  - `.claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable --item WI-0001` → exit 0, 6 gaps
  - `.claude/agile-skills/scripts/lint-claims --context work-item --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/lint-answers --context work-item --changed-since main` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 7 documents
  - `git worktree add --detach /tmp/rvw/trial main` → `7f27e61`; `git -C /tmp/rvw/trial merge --no-ff wi/WI-0001` → `aada90c`; `python3 -m unittest discover -s tests -t .` **in the trial** → exit 0, 52 tests, OK; `git worktree remove --force /tmp/rvw/trial`; `git rev-parse main` → `7f27e61`, unmoved
  - the tool itself, against a scratch `ENVEL_FILE`: AC15's five invocations, AC14's two, AC7, AC9 at `12.57 + 0.03`, AC13's five names, eight AC16 refusal cases, and five malformed invocations no criterion names (`-x`, `--foo`, `new --foo x`, `list --foo`, `add g 10 --foo`) → no traceback, every refusal on stderr with stdout empty and a non-zero exit
  - `grep -rn "ENVEL_FILE\|XDG_DATA_HOME\|store_path" envel/ bin/envel` → 4 lines; `grep -n "^import \|^from \|^\s*import \|^\s*from " envel/*.py bin/envel` → 13 lines; `ls docs/architecture/adr/` → five ADRs
- **Gates:**
  - `definition-of-done` → **pass** (`review.md` `## Definition of Done`: D1–D13, thirteen rows, each with its own result and evidence. D7 confirmed against the plan's fourteen-entry set, D13 against `ls docs/architecture/adr/` — five ADRs exist and the plan names all five)
  - `engagement-state-is-restated` → **pass** (applicable — an item close** (`lint-documents --rule engagement-state-is-restated --item WI-0001 --context work-item` → exit 0, printing *"NOT APPLICABLE — an item close is not an ending, and the sections are the ending's"*. Neither `## Engagement state` section was read for restatement or touched; `review.md` records `not an ending`))
  - `accepted-gaps-are-dispatchable` → **pass** (`lint-documents --rule accepted-gaps-are-dispatchable --item WI-0001` → exit 0, 6 gaps at status `in-review`. All six: owner `none`, disposition `no-owner`. None names a skill or the human, so none is inert)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `2f025c5`, head `fa2ffd3`, only the record moved — 5 files under `tracker/` or `docs/`. Last code commit `81441cd`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 8 commits on `main..wi/WI-0001` name WI-0001; run before the merge, while the range is still non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` run **inside** the detached trial worktree at merge commit `aada90c` → exit 0, 52 tests, OK — the merge result, not the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 7 items, 7 documents, 0 errors, 0 warnings)
  - `record-is-reconstructible` → **pass** (answered from `tracker/`, `docs/` and `git log --grep WI-0001` alone. *What was built and why:* three commands, a store and two entry points, because `WI-0001` is the first item of `EP-001` and the stakeholder's two constraints are Python and no services. *Which skill decided what:* `refine` settled the criteria over two rounds, four stakeholder answers and five recorded assumptions; `plan` recorded five ADRs and the invalidation set; `implement` deviated five times and recorded each; `verify` found AC15 and sent it back. *What questions arose and how they resolved:* `Q-001`…`Q-004`, all answered by the stakeholder at `02:20:30Z` and propagated into AC7–AC13 with the consequences named. *What verification found:* sixteen criteria passing and AC15 failing on the first round, all seventeen on the second, with fourteen mutations turning the suite red)
  - `claims-are-sourced` → **pass** (`lint-claims --context work-item --changed-since main` → exit 0. **Scope, quoted from its own run:** *"checked absolute claims: 2 document(s) in 2 path(s) differ from main (7f27e61) under docs; citations: every markdown file in the workspace"* — a non-empty window, and the two documents are the two this item edited)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0, 12 consumed human answers and 0 delegations spent. This execution consumed no answer of its own; see `**Cross-answer check:**`)
  - `epic-sign-off` → **pass** (WI-0001 is a `work-item`, not an epic** (`check-epic-signoff WI-0001` → exit 0, reporting *"the termination gate applies to an engagement's ending only"*. `engagement-state EP-001` → `active`, six children in flight, so no engagement is ending here); the run reported PASS: `/usr/bin/python3 /home/msi/agile-skills-throwaway/envel-2/.claude/agile-skills/scripts/check-epic-signoff WI-0001 --root /home/msi/agile-skills-throwaway/envel-2 --resolving 'WI-0001:in-review->done+journal'` exited 0)
- **Artifacts:**
  - `tracker/items/WI-0001/artifacts/review.md` (new) — what was examined, D1–D13, the invalidation-set confirmation, two findings, six accepted gaps, the verdict
  - `tracker/items/WI-0001/item.md` — `outcome: delivered`, written by this transition
  - the merge of `wi/WI-0001` into `main` follows this entry; its sha cannot be named here because it does not exist yet, and `scripts/record-merge` puts it in `item.md`'s `merge-commit`
  - no bug filed, no question filed, no document written
- **Status:** `in-review` → `done`
- **Result:** Accepted and closed as `delivered`. All seventeen criteria hold on evidence, four of them re-gathered by this review; all thirteen Definition of Done criteria pass; the suite passes on the merge result rather than only on the branch. Two findings are recorded and neither is a defect in the change — a documentation sentence looser than the code it describes, and a name beginning with `-` needing the `--` separator.
