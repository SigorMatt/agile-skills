---
status: agenda
---

# Refinement Q&A — WI-0002

**`status: agenda` is deliberate.** Round 1's question is with the stakeholder and unanswered, so
the exchange below is what refinement *asked* and what it *decided on its own*, not a record of a
conversation that happened. Definition of Ready R8 reads this field, so this file cannot pass the
item to `ready` by existing. It becomes `recorded` when `Q-001` is answered and refinement
resumes at `draft` to finish the criteria.

## What refinement did not re-ask

Four of the stakeholder's answers already reach this item, and none of them was put to them
again. This list is the agenda's first half: the criteria these answers close.

| their answer | what it settles here |
|--------------|----------------------|
| `EP-001/Q-001` — *"A — the open prompt. I fire it up, keep typing rolls one after another, and close it when we're done for the night."* | A session is one run of the prompt. The history starts empty at each start, holds the rolls made since, and ends when the program does. This is AC5 and it is theirs, not an assumption |
| `EP-001/Q-003` — *"keeping the history for just the current session is fine; being able to save it across sessions would be nice someday but I don't need it now"* | Nothing is written to disk and nothing is read back by a later run. Cross-session saving is declined rather than deferred, and stays in `## Out of scope` |
| `EP-001/Q-002` — *"whatever's standard, don't overthink it"* (the dice notation delegation) | Reaches the **notation of a dice expression** and nothing here. It does not license a command word, for the reason `WI-0001`'s A3 gives; see D1 below |
| `WI-0001/Q-001` — *"A — the total plus the individual dice, plain text. That's all I need to believe the number."* | What a **roll line** contains. Whether a **history line** contains the same thing is the open question, `Q-001`, and is the one thing this round asks |

## Round 1 — the question with the stakeholder

### Q1 — When you type `history`, what should each entry show? `[unresolved]`

Filed as `tracker/items/WI-0002/questions/Q-001.md`, blocking, addressed to the human, with three
options — expression and total only; the full roll line as it printed at the time; or the short
form with detail on request — and the recommendation last and marked as ours.

**Why it went to them rather than being decided.** It changes what the user sees every time they
use the feature this item exists for, and the two plausible answers serve different things: a
transcript you can re-check, or a scoreboard you can skim. Their one recorded sentence on the
subject — *"all I need to believe the number"* — is genuinely readable both ways, and reading it
for them is what `refine`'s step 3 calls product stake.

**Not answered yet.** The item is at `awaiting-answer` with `resume-to: draft`.

## Decisions refinement took without asking

Each says plainly what licensed it. For all three, the answer is nothing — and the reason each was
still taken here rather than put to the stakeholder is given, per Definition of Ready R12's second
branch.

### D1 — the input that asks for the history is the word `history` `[assumed]`

**No delegation licensed this.** The engagement's one delegation, `EP-001/Q-002` — *"whatever's
standard, don't overthink it"* — is about the notation of a dice expression. A command word is not
dice notation, and `WI-0001`'s A3 already refused to stretch the same licence over `quit` and
`exit` for exactly that reason. Stretching it here would be the unbounded reading R12 exists to
prevent.

**Decided:** typing `history` on its own at the prompt lists the session's rolls. Case is
ignored, so `HISTORY` works, which is how `quit` and `exit` already behave in the delivered code
[src: droll/cli.py:34]. The word is not a valid dice expression under ADR-0001's grammar, so it
cannot collide with a roll.

**Why here rather than with them:** the answer would be the same whoever the stakeholder was —
`history` is what a prompt of this kind is typed at — and it is the class of call a real
stakeholder named as the thing they least wanted routed to them. It is not hidden from them
either: `Q-001`'s `## Context` states it in one sentence and says that contradicting it costs one
line.

**Where a disagreement lands:** with the stakeholder, and cheaply — it is one criterion and one
constant. If it is still standing at the ending, `review-close` names it in the sign-off.

### D2 — asking for the history does not put an entry in the history `[assumed]`

**No delegation licensed this**, and none is needed: it follows from the stakeholder's own
sentence. They asked for *"the rolls from the current session"*, and typing `history` is not a
roll. It is recorded here rather than left implicit because it is a combination two behaviours of
this item produce together, which Definition of Ready R10 requires be visible rather than
discovered.

**Where a disagreement lands:** nowhere plausible; the alternative is a list that grows a line
every time it is read.

### D3 — nothing is forgotten: the session's whole history is kept `[assumed]`

**No delegation licensed this**, and it is the plain reading of *"remember the rolls from the
current session"* — a cap would be remembering some of them. No upper bound is imposed, and the
criteria will not name a number, because a number here would be one nobody agreed to.

**Where a disagreement lands:** with the stakeholder, if a game night ever produces a list too
long to be useful. That is a new want rather than a defect in this one, and `tracker/requests/` is
the route.

## Routed to `plan` rather than decided or asked

- **The layout of the listing** — indentation, whether entries are numbered, how columns line up,
  what separates the entries. This is the same call that `WI-0001/Q-001`'s answer explicitly left
  open — *"What is still not settled by this answer is the layout — spacing, brackets, where the
  total sits … That stays `plan`'s"* — applied to a list instead of a line. It goes in the item's
  `## Notes` as an open design question, not into a criterion.
- **How the rolls are held in memory** — a list, a deque, an attribute on the loop. No criterion
  can see the difference, and the answer would be the same whoever the stakeholder was.

## Definition of Ready — where it stands at the suspension

Walked criterion by criterion. This is the state at `awaiting-answer`, not a pass.

| # | result | evidence |
|---|--------|----------|
| R1 | pass | `item.md` frontmatter carries `id`, `type`, `title`, `status`, `priority`, `epic`, `created`, `updated` and `depends-on`; `type`, `epic` and `priority` are all set. `validate-workspace` exits 0 |
| R2 | pass | `## Story` names the role (*"someone making a series of rolls"*), the capability (*"remember the rolls … and show them to me on request"*) and the outcome (*"so that I can answer 'what did I roll a minute ago?' without having written anything down"*) |
| R3 | pass | Five criteria, `AC1` to `AC5`, each a `- [ ]` checkbox |
| R4 | **fail** | `AC1` says *"there is something the user can type at the prompt that lists those rolls. Refinement settles what that input is"* — a criterion that names its own incompleteness cannot be observed. `AC2` and `AC4` name what is shown in terms (*"the expression … and the total"*, *"a message saying there are none"*) that two readers would settle differently. `AC1` closes under D1; `AC2` is the subject of `Q-001` and closes with their answer; `AC4` closes when the listing's shape is fixed |
| R5 | pass | `## Out of scope` names three things, of which cross-session saving is one a reader would reasonably assume was included — the stakeholder said so themselves [src: EP-001/Q-003] |
| R6 | **fail, by this execution's own act** | `Q-001` is open and `blocking: true`. It is what R6 is for: the item may not be Ready while a question this size is unanswered |
| R7 | pass | `depends-on: WI-0001`, and `WI-0001` is `done` — closed as `delivered` and merged at `c52c3a6` |
| R8 | **fail** | This file declares `status: agenda`. The conversation has not happened, and saying otherwise is what the field exists to prevent |
| R9 | pass | One coherent change: hold the accepted rolls of a run and print them on one input. It is not two items — there is no half of it that delivers on its own |
| R10 | **fail, and identified** | The combinations this item introduces are enumerated in `## Notes` and in D2: `history` against an empty history, against a session containing only rejected input, and against itself. Two of the three have a criterion already; the third is D2. They become criteria in round 2 |
| R11 | pass | No criterion states a count of anything this item may move. The round-2 rewrite must keep it that way: *"the list has as many lines as rolls were made"* is the shape to avoid, and naming the rolls typed in the observation is the shape to use |
| R12 | pass | Three assumptions, D1 to D3, each saying in terms that **no** licence covered it and where a disagreement lands. No `**Under delegation:**` line is written on this item, because the engagement's one delegation does not reach anything here — see the table above |
