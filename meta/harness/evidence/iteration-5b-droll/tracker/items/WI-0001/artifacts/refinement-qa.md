---
status: recorded
---

# Refinement Q&A — WI-0001

`status: agenda` is deliberate and is the honest state of this file. The stakeholder is
asynchronous and was not in the session in which round 1 of this refinement ran, so **the
conversation below did not happen as a conversation**. What was recorded here was the agenda for
it: the Definition of Ready criteria that fail, the question that was filed as a result, and the
decisions refinement took without asking. Definition of Ready R8 reads this field, so this file
cannot pass the item to `ready` by existing — which is the point.

The stakeholder replied to all four questions, `answer-questions` wrote those replies into the
sections below and propagated them, and **round 2 of refinement has now run** on the answers. The
field is therefore `recorded`: the exchange below is what was actually said, and the decisions
refinement took on top of it are tagged and scoped. Round 2 is the second half of this file and
the Definition of Ready table at the end is round 2's.

## Round 1 — the agenda

### Q1 — What does "the breakdown" have to contain? `[answered]`

Filed as `WI-0001/Q-001`, blocking, addressed to the stakeholder. This is a **product-stake**
question by refine's step 3 test: "breakdown" is the stakeholder's own word for a thing they asked
for by name, and what it contains is what they would notice. Three options were put to them, with
the team's preference marked as the team's and placed last.

**Answered, option A:** *"A — the total plus the individual dice, plain text. That's all I need to
believe the number."* Every die's face and the modifier are shown separately, in plain text, in
one shape for every roll — a bare `d20` prints in the same form as `3d6+2`. Written into AC2 by
`answer-questions`; the layout of the line stays `plan`'s, as the question itself said.

### Already with them, not re-asked

- `EP-001/Q-001` — what "the current session" is, and therefore whether an expression is typed at
  a prompt or passed on a shell command line. **Answered, option A:** an interactive prompt, and a
  session is one run of it. Every criterion on this item that names an observation now names the
  prompt; AC6 was added for the prompt itself.
- `EP-001/Q-002` — how far the accepted expression syntax reaches. **Answered:** one dice term
  with an optional integer modifier, recorded as ADR-0001 under the delegation their answer
  carried. AC5 is that grammar and the item's exclusions are now concrete.

Re-asking either here would have told the stakeholder their answer was not heard.

## Round 2 — the answers, and what refinement did with them

No question was put to the stakeholder in this round. Everything round 1 was waiting on had been
answered, and what remained was either inside the delegation their answer to `EP-001/Q-002`
granted or a conventional detail whose answer would be the same whoever the stakeholder was. Two
of those are recorded below as taken under **no** licence, because they are not inside that
category and nothing else covers them.

### Q2 — Does the tool accept a capital `D`, and what about spaces? `[assumed]`

Not asked. ADR-0001 named the letter case of `d` and the treatment of whitespace as the two
things it deliberately left inside the licence for refinement to settle.

**Decided:** `D` is accepted wherever `d` is, so `D20` and `3D6+2` roll exactly as `d20` and
`3d6+2` do. Leading and trailing whitespace around an expression is ignored. Whitespace *inside*
an expression is not: `3 d 6` is rejected by AC4's path. The reasoning is that a capital `D` is a
typing accident nobody means, and a surrounding space is a typing accident too, while a space in
the middle is the boundary at which "one dice term" stops being one token and the grammar would
have to say what `3 d 6 + 2` means. Written into AC9.

**Under delegation:** EP-001/Q-002 — the notation inside standard single-term dice expressions:
whether the count may be omitted, the sign and presence of the modifier, and the bounds on the
count, the die size and the modifier.

### Q3 — Is there an upper bound on the count or the die size? `[assumed]`

Not asked. ADR-0001 named the bounds as the third thing it left inside the licence.

**Decided: no bound.** `100d1000` is inside ADR-0001's grammar and the tool rolls it. A limit
nobody asked for is a rule the user has to discover, and the stakeholder's setting — one person
at a keyboard on game night — does not produce an expression large enough to matter. Recorded in
the item's `## Notes` as deliberately unconstrained under Definition of Ready R10 rather than as
a criterion, because there is nothing to observe.

**Under delegation:** EP-001/Q-002 — the notation inside standard single-term dice expressions:
whether the count may be omitted, the sign and presence of the modifier, and the bounds on the
count, the die size and the modifier.

### Q4 — How does the session end? `[assumed]`

Not asked, and this one is **not** covered by any licence. See A3 below for why it was decided
here rather than put to them.

**Decided:** `quit`, `exit`, and end-of-input (Ctrl-D on an empty line), each ending the program
with exit status 0. Written into AC10.

## Decisions refinement took without asking

A1 and A2 are round 1's; A3 is round 2's. Each says plainly what licensed it — which, for all
three, is nothing.

### A1 — "the dice are actually rolled" is made decidable with an invented threshold `[assumed]`

**No delegation licensed this.** The one delegation they have since granted — `EP-001/Q-002`,
*"whatever's standard, don't overthink it"* — covers the notation of a dice expression and does
not reach how many times a die is rolled in a test or how varied the result has to be, so nothing
covers this. It is recorded under Definition of Ready R12's second branch — an assumption taken
under no licence, said plainly, with where a disagreement would land.

Intake's AC3 read *"repeating the same expression enough times produces results spread across the
possible range rather than a constant"*, which no two people would decide the same way. Refinement
replaced the vague part with numbers nobody agreed to: roll `1d6` 200 times, observe at least
three distinct faces, and observe no value outside 1–6. The thresholds are chosen to be
overwhelmingly unlikely to fail on a working implementation and certain to fail on a constant.

**Where a disagreement lands:** if the stakeholder wants a real statistical claim — uniformity, a
seed, reproducibility — this criterion is not it, and the epic currently puts that out of scope.
Contradicting it is what `EP-001/Q-003` is for. If they do, this criterion is replaced rather than
loosened.

### A2 — exit codes and output streams are not being put to the stakeholder `[assumed]`

**No delegation licensed this either.** It is recorded in the item's `## Notes` as an open design
question routed to `plan`, not as a decision already taken. Which stream an error message goes to
and what exit code accompanies it would have the same answer whoever the stakeholder was — the
test in refine's step 3 that routes a question to `plan` rather than to a person — and in one
recorded run a stakeholder's chief complaint was exactly this kind of technical call arriving as a
question for them.

`EP-001/Q-001` has since been answered — one long-lived prompt, not a process per roll — so the
question narrows to which stream the prompt writes on and to the exit code at quit. It remains
`plan`'s.

**Where a disagreement lands:** with `plan`, as an ADR. If the stakeholder turns out to care, the
route back is a stakeholder request or `EP-001/Q-003`.

### A3 — the words that end a session were chosen by refinement `[assumed]`

**No delegation licensed this.** The one delegation in this engagement — `EP-001/Q-002`,
*"whatever's standard, don't overthink it"* — is about the notation of a dice expression. A
command word is not dice notation, so the licence does not reach it, and saying that it does
would be exactly the unbounded reading R12 exists to prevent.

The stakeholder said *"close it when we're done for the night"* and named no input. The question
they answered, `EP-001/Q-001`, described option A as ending when *"quitting ends the session"* —
which says that quitting exists and not how it is done.

It was decided rather than asked because AC10 has to say something a person with a terminal can
observe, and because the answer would be the same whoever the stakeholder was: `quit`, `exit` and
Ctrl-D are what every command-line prompt of this kind accepts. Refinement's step 5 test — offer
a concrete default rather than ask an open question — points the same way. Three inputs rather
than one, so that a user who guesses either word is right.

**Where a disagreement lands:** with the stakeholder, at the sign-off. If they wanted something
else — a bare enter, `q`, `bye` — AC10 is one line to change and no design depends on it. It is
also the kind of thing `EP-001/Q-003`, the standing elicitation, exists to catch, and they have
already answered that one without mentioning it.

## Definition of Ready — where this item stands

Round 1's table is preserved below it; this one is round 2's, and it is the verdict that carries
the item to `ready`.

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic` and `priority` are all set |
| R2 | pass | The story names the role (someone who needs dice at a keyboard), the capability (type an expression, be shown total and dice), and the outcome ("so that I can use the number straight away and still see where it came from") |
| R3 | pass | Eleven `AC<n>` checkboxes exist |
| R4 | pass | Round 1's failure closed. Every criterion names text typed at the prompt and something printed in response, and each is settled by starting the tool and reading: AC1/AC2 the breakdown of `3d6+2`, AC3 a count over two hundred `1d6` rolls, AC4 eight named rejected inputs, AC5 four named accepted ones, AC6 two rolls in one run, AC7-AC9 what `d20`, `2d10`, `4d8-2`, `D20`, `3D6+2`, a padded expression and `3 d 6` print, AC10 three ways of ending the session and the exit status, AC11 a rejection followed by a roll. No unmeasurable adjective survives: round 1's *"spread across the possible range"* was replaced in round 1 (A1) and nothing of that shape was added |
| R5 | pass | Three exclusions: the whole of `WI-0002`'s remembering and the way it is asked for, every expression form outside ADR-0001's grammar named individually, and the choice of random number generator |
| R6 | pass | Round 1's failure closed. `WI-0001/Q-001` is `answered`; no question on this item is open |
| R7 | pass | `depends-on` is empty; nothing sequences before this item |
| R8 | pass | Round 1's failure closed. This file declares `status: recorded`, and the exchange above it is what was actually said: four questions to the stakeholder with their replies quoted verbatim, and three round-2 decisions tagged `[assumed]` with their licence or its absence named |
| R9 | pass | One coherent change: read an expression at a prompt, evaluate it, print it, loop. No part of it delivers separately, and the remembering half is already a separate item |
| R10 | pass | Round 1's failure closed, because `EP-001/Q-002` made the behaviours enumerable. The item introduces a prompt loop, a count that may be present or absent, a modifier that may be positive, negative or absent, letter case, surrounding whitespace, a rejection path and a quit. All four count-by-modifier combinations have a criterion — AC7 (`d20`, neither), AC8 (`2d10`, count only; `4d8-2`, count with a negative modifier) and AC1/AC2 (`3d6+2`, count with a positive modifier). Case is crossed with a modifier in AC9 (`3D6+2`) rather than left to be inferred. Rejection is crossed with the loop in AC11, and the loop with two accepted rolls in AC6. The one thing left unconstrained — an upper bound on the count and the die size — is named as such in `## Notes` with who left it so, which is what R10 asks for |
| R11 | pass | No criterion counts a project artefact. AC3's `200` and `3`, and the die counts in AC7-AC9, are parameters of an observation of the tool's own output rather than counts of tests, files or cases; the `200` and `3` are declared as invented in A1. AC4 and AC5 name their inputs individually instead of counting them, which is what R11 asks for |
| R12 | pass | Five assumptions, each scoped. Q2 and Q3 carry `**Under delegation:** EP-001/Q-002` with the category it is taken to cover, and the same line stands in the item's `## Notes`. A1, A2 and A3 each say in terms that **no** licence covered them and where a disagreement lands — A1 with the stakeholder if they want a statistical claim, A2 with `plan`, A3 with the stakeholder at the sign-off |

Twelve criteria, twelve passes. The item is Ready.

## Definition of Ready — round 1

Kept because it is the record of what refinement found before the answers arrived. Round 2's
table above supersedes it; nothing here is amended except the one cell whose factual claim went
false, which says so in place.

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic` and `priority` are all set |
| R2 | pass | The story names the role (someone who needs dice at a keyboard), the capability (type an expression, be shown total and dice), and the outcome ("so that I can use the number straight away and still see where it came from") |
| R3 | pass | Five `AC<n>` checkboxes exist |
| R4 | **fail** | AC1, AC2 and AC4 each name an observation whose *form* depends on `EP-001/Q-001`; AC2's content is `WI-0001/Q-001`; AC5 is a placeholder for `EP-001/Q-002` and is not a criterion at all. AC3 was the one failure refinement could close on its own and it did — see A1 |
| R5 | pass | Three exclusions, each something a reader could assume was included |
| R6 | **fail** | `WI-0001/Q-001` is open and blocking. This is the criterion that carries the item to `awaiting-answer`, and it is failing on purpose |
| R7 | pass | `depends-on` is empty; nothing sequences before this item |
| R8 | **fail** | This file declares `status: agenda`, because the conversation has not happened |
| R9 | pass | One coherent change: read an expression, evaluate it, print it. No part of it delivers separately, and the remembering half is already a separate item |
| R10 | **fail** | The behaviours this item introduces are not yet enumerable: `EP-001/Q-002` decides which expression forms exist, and their combinations cannot be stated before that |
| R11 | pass | No criterion counts a project artefact. The `200` and the `3` in AC3 are parameters of an observation rather than counts of tests, files or cases, and they are declared as invented in A1 |
| R12 | pass | Two assumptions, A1 and A2, each saying under R12's second branch that **no** licence covers it and where a disagreement lands. No standing delegation existed in this engagement to name at the time of this verdict; one has since been granted and A1 now names it and says why it does not reach |

Four failures, and none of them was closable without the stakeholder. The item was suspended.

**Round 1's verdicts are round 1's.** All four answers have since arrived and are propagated into
`item.md`, ADR-0001 and the vision, which is what R4, R6 and R10 were waiting for. The table above
is not amended: it records what refinement found in round 1 and the record is append-only in
spirit. R8 still fails, and this file still declares `status: agenda`, because the conversation is
not finished — AC5 has to be split into one criterion per accepted form, and whether that is all
of it is `refine`'s judgement in round 2, not `answer-questions`'. Flipping this field is how R8
would be passed by the wrong skill. R12's verdict cell has been extended in place for the one fact
it asserts that has since changed — a delegation now exists — because leaving "no standing
delegation exists" standing would be a false sentence rather than a stale verdict.
