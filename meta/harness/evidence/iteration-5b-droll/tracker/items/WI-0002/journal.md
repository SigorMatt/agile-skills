# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T21:28:43Z — intake v0.5.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** not scheduled — `intake` was invoked directly on the stakeholder's stated idea, and this item was created by that execution.
- **Inputs read:**
  - The stakeholder's stated idea, recorded verbatim in `EP-001`'s entry for this execution
  - `tracker/project.yaml` (name, trunk branch, empty commands)
  - `tracker/items/` — empty before this execution; no existing item to overlap with
- **Decisions:**
  - See `EP-001`'s entry for this execution for how the work was split and why. This item is the remembering half: the rolls of the current session, listed back on request.
  - It is a separate item from `WI-0001` rather than a criterion on it because it delivers something observable on its own — a user with rolling but no history has a working tool, and the history is a second thing they can then see.
  - `depends-on: WI-0001` is recorded rather than left implied, because it is what fixes the build order without anybody guessing the stakeholder's preference.
  - "Current session" is left undefined here on purpose. It is the stakeholder's phrase, it is the subject of `EP-001/Q-001`, and AC5 says so rather than pretending a definition was agreed.
- **Questions raised:** none on this item; `EP-001/Q-001` decides what a session is and therefore what this item stores and when it resets.
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 --title "Keep the rolls made during a session and show them back" --priority medium --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - workspace-valid → **pass** (`scripts/validate-workspace` exits 0 at the end of this execution)
  - epic-has-success-measures → **pass** (evidence on `EP-001`; this item does not carry the measures)
  - an-open-question-was-asked → **pass** (`scripts/lint-answers --item EP-001 --require-elicitation` → exit 0, reporting `EP-001/Q-003` open)
  - engagement-state-is-delimited → **pass** (`scripts/lint-documents --rule engagement-state-is-delimited --document docs/product/vision.md` → exit 0, one section)
  - items-are-separable → **pass** (built second, after `WI-0001`, which it names in `depends-on`)
  - no-solution-in-the-problem → **pass** (the story names no storage mechanism, no file and no data structure — deliberately, since `EP-001/Q-001` decides what a session is)
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — created and filled in
  - `tracker/items/WI-0002/history.md`, `tracker/items/WI-0002/journal.md` — created by `scripts/new-item`
- **Status:** `—` → `draft`
- **Result:** The history half of the epic exists at `draft` with five criteria, one of which is explicitly waiting on `EP-001/Q-001`. It is not Ready.

## 2026-09-11T23:14:01Z — refine v0.6.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` — the first pass at which this item was
  runnable, `depends-on: WI-0001` having become `done` earlier in the same turn.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the five intake criteria, `## Out of scope`, `## Notes`
  - `tracker/items/WI-0002/history.md` — one row, `— → draft` by `intake`. This is a **fresh
    draft**, not a send-back, so the whole story is open rather than one named defect
  - `tracker/items/WI-0002/journal.md` — `intake`'s entry, for what it deliberately left undefined
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md` — the stakeholder's three
    answers, read for what they already settle here and for the one delegation they contain
  - `tracker/items/WI-0001/questions/Q-001.md` — their answer on what a roll line shows, which is
    the answer adjacent to this item's open question
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — A1, A2 and A3, for how this engagement
    has already drawn the line between a decision refinement takes and one the stakeholder owns
  - `tracker/items/WI-0001/item.md` — AC1 to AC11 as delivered, so this item's criteria describe
    the tool that now exists
  - `droll/cli.py`, `droll/formatting.py`, `droll/__main__.py` — the delivered prompt loop, for
    the exact text a roll prints and for how `quit` and `exit` already treat case
  - `.claude/agile-skills/spec/dor-dod.md` §1 and `spec/question.md` §2
  - no ADR was consulted beyond ADR-0001's grammar as quoted in `WI-0001`'s criteria, and
    `docs/product/vision.md` was not needed: nothing here contradicts it
- **Decisions:**
  - **Filed exactly one question to the stakeholder, and it is the one thing that is theirs:
    what a history entry shows.** Rationale: the two plausible answers serve different purposes —
    a transcript you can re-check against a scoreboard you can skim — and their one recorded
    sentence on the subject, *"all I need to believe the number"*, is genuinely readable both
    ways. Reading it for them is the guess this protocol exists to prevent. Everything else this
    item needed was either already answered by them or was ours.
  - **Did not re-ask four things they have already answered.** `EP-001/Q-001` fixes what a
    session is, `EP-001/Q-003` confirms session-only and declines cross-session saving,
    `EP-001/Q-002` is the dice-notation delegation, and `WI-0001/Q-001` fixes what a roll line
    shows. Rationale: re-asking is the fastest way to lose a stakeholder, and the answers are in
    the record where a later reader can check them.
  - **Decided the input word `history` rather than asking (D1), under no licence.** Rationale:
    `WI-0001`'s A3 settled the identical shape of call for `quit` and `exit`, explicitly refusing
    to stretch `EP-001/Q-002`'s *"whatever's standard"* over a command word; deciding the same
    way here is consistency, and asking would be the technical-call-as-question a real
    stakeholder named as their chief complaint. Case is ignored, matching the delivered
    `droll/cli.py:34`, and the word cannot collide with ADR-0001's grammar. It is stated in
    `Q-001`'s `## Context` so they can contradict it for free in the reply they are already
    writing — one sentence of information, not a second question folded into the first.
  - **Decided D2 (asking for the history is not itself an entry) and D3 (no cap on what is
    kept), both under no licence.** Rationale: both follow from the stakeholder's own sentence
    *"remember the rolls from the current session"* — typing `history` is not a roll, and a cap
    would be remembering some of them. Recorded rather than left implicit because R10 asks that
    a combination be visible rather than discovered.
  - **Routed the listing's layout to `plan`, not to the stakeholder.** Rationale: the answer to
    `WI-0001/Q-001` drew this line itself — *"What is still not settled by this answer is the
    layout … That stays `plan`'s"* — and this is the same call applied to a list instead of a
    line. Recorded in the item's `## Notes` as an open design question.
  - **Did not rewrite the acceptance criteria in this round.** Rationale: `AC2` is the subject of
    the open question and `AC1` and `AC4` are downstream of the shape it settles. Rewriting the
    list around a guess is exactly what filing the question was for, and a half-rewritten list
    invites a renumbering under the citations `EP-001/Q-001` and `EP-001/Q-003` already make into
    `AC5` (F-094). The whole list is rewritten in round 2, in one pass, once the answer is in.
  - **Left `refinement-qa.md` at `status: agenda`.** Rationale: the conversation has not happened.
    R8 reads that field precisely so an agenda cannot pass an item to `ready` by existing, and
    writing `recorded` on a file intended to be finished later is the thing the two states exist
    to distinguish.
- **Cross-answer check:** `Checked against: EP-001/Q-001; EP-001/Q-002; EP-001/Q-003;
  WI-0001/Q-001` — the four human answers this engagement holds. No conflict, and nothing was
  reconciled by editing anything of theirs.
  - `EP-001/Q-001` (a session is one run of the prompt) — compatible and load-bearing: it is what
    gives the history a lifetime. Nothing decided here changes it.
  - `EP-001/Q-002` (*"whatever's standard, don't overthink it"*) — compatible, and deliberately
    **not** spent: it covers the notation of a dice expression, and no decision on this item is
    about dice notation. No `**Under delegation:**` line was written, because writing one would
    be the unbounded reading R12 exists to prevent.
  - `EP-001/Q-003` (session-only is fine; saving across sessions is a want for later) —
    compatible: this item stores nothing on disk and the exclusion stays in `## Out of scope` in
    their own words.
  - `WI-0001/Q-001` (a roll line shows every die's face and the modifier) — **adjacent, not
    conflicting, and that distinction is the reason `Q-001` exists.** Their answer is about what
    a roll prints at the moment it is rolled; intake's draft `AC2` here says a history entry
    shows the expression and the total, which is less. Two readings of one preference is not a
    contradiction between two of their statements, so the §4a "quote both and ask which wins"
    form does not apply — but neither is it ours to settle, so it is asked plainly, with their
    sentence quoted in the context and both readings offered as options.
  - `lint-answers --item WI-0002` → exit 0, *"0 consumed human answer(s) and 0 delegation(s)
    spent on WI-0002"* — which is the correct count: this execution consumed none and spent none.
- **Questions raised:** `WI-0002/Q-001` — blocking, addressed to `human`, one decision, three
  options with the recommendation last and marked as the team's preference. One question in the
  round, and its `## Context` says so. Recorded in `artifacts/refinement-qa.md` as `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0002` → exit 0, 0 errors
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, wrote `tracker/board.md`
  - `python3 .claude/agile-skills/scripts/run-gate --skill refine --item WI-0002 --all
    --resolving 'WI-0002:draft->awaiting-answer'` → exit 0, no hard gate failed, 3 manual
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 under the resolving move
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace --resolving 'WI-0002:draft->awaiting-answer'` exited 0. Run without the resolving flag it reports `question.blocking.not-suspended`, which is this execution's own open question waiting for the move being made)
  - `definition-of-ready` → **fail** (walked R1-R12 one at a time; the table is in `artifacts/refinement-qa.md` `## Definition of Ready`. R1 pass, R2 pass, R3 pass, **R4 fail** — `AC1` names its own incompleteness and `AC2` and `AC4` are settled differently by two readers — R5 pass, **R6 fail** by this execution's own act of filing a blocking question, R7 pass — `WI-0001` is `done`, merged at `c52c3a6` — **R8 fail**, the Q&A declares `status: agenda`, R9 pass, **R10 fail but identified**, the four combinations enumerated in `## Notes`, R11 pass with the round-2 trap named, R12 pass, three assumptions each saying no licence covered it. Four failures, all of them closable in round 2 once `Q-001` is answered)
  - `criteria-are-decidable` → **fail** (`AC1` cannot be settled by any command: it says refinement will decide what the input is. `AC2` — *"shows … the expression that was rolled and the total"* — has no observable form until `Q-001` says what an entry contains. `AC4` — *"a message saying there are none"* — names no text. `AC3` and `AC5` are decidable as written: `AC3` by typing `3x6` then `history` and reading no entry, `AC5` by starting a second run and reading an empty history plus `git status` showing no new file. Two of five)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0002` exited 0. The read behind it is in `**Cross-answer check:**` above: four prior answers named, one adjacency identified and asked rather than resolved)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` carries the stakeholder's four prior answers quoted word for word in the table of what was not re-asked, the one question of this round tagged `[unresolved]` because it is, and three `[assumed]` decisions each stating that **no** delegation licensed it and where a disagreement lands. Nothing is paraphrased into agreement — there is no agreement yet to paraphrase, which is why the file says `agenda`)
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` (new — blocking, to the human)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new — `status: agenda`)
  - `tracker/items/WI-0002/item.md` (updated — `## Notes — refinement round 1`: the three
    assumptions, the design question routed to `plan`, and the R10 combinations. The acceptance
    criteria are deliberately untouched)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0002 is not Ready and suspends on one question with the stakeholder: what a
  history entry shows. Four Definition of Ready criteria fail and all four close in round 2 on
  that one answer. Everything that was ours to settle was settled — the input word, what is not
  an entry, that nothing is forgotten, and that the listing's layout is `plan`'s — and nothing
  the stakeholder has already answered was put to them twice.
