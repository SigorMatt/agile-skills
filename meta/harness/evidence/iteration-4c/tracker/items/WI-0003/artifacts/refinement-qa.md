---
status: recorded
---

# Refinement Q&A — WI-0003

`status: recorded`: the conversation has happened. Both questions that were the stakeholder's
were answered, their answers are quoted verbatim below, and Q3 — which was written here as not yet
askable — has since become answerable and is decided.

The stakeholder is asynchronous, so the exchange happened through the question files rather than
in a conversation; `answer-questions` propagated both answers into the criteria and into `docs/`,
and returned the item to `draft` for `refine` to finish. **Round 2 below is that finish**, run by
`refine` on 2026-08-30T12:57Z: it asked the stakeholder nothing, because nothing left was theirs,
and it spent Q4's standing deferral on the command name, the prompts and the keystrokes. The
Definition of Ready now passes on all ten criteria.

## Round 1 — the agenda, and where each item of it went

| DoR | verdict as found | who it is for |
|-----|------------------|---------------|
| R1 frontmatter | pass — `type`, `epic`, `priority`, and `arose-from: EP-001/Q-004` | — |
| R2 story | pass — role, capability, "so that" | — |
| R3 criteria exist | pass — AC1–AC3 as found, AC1–AC6 now, labelled, checkboxes | — |
| R4 decidable by observation | **now passes.** `Q-001` gave the identifier — the front side. Round 2 gave the command: AC1 and AC2 now name the `delete` subcommand, its one argument, the two answers its prompt takes, and the exit code of each outcome | resolved in Round 2 |
| R5 out of scope | **now passes in substance.** The undo exclusion was put to the stakeholder as `Q-002` and is now their decision, quoted; two further exclusions were added from their answers — no list command, and no way to skip the prompt | resolved |
| R6 questions non-blocking | fail while suspended; **now passes** — both are answered and no question on the item is open | resolved |
| R7 independently deliverable | **now passes in substance.** Round 2 declared `depends-on: WI-0001`, which is the truth of it, and WI-0001 is `done`, so the dependency is satisfied rather than merely recorded | resolved in Round 2 |
| R8 Q&A recorded | **now passes** — the answers arrived and this file is `recorded` | resolved |
| R9 one coherent change | pass — one command, one file, one behaviour | — |
| R10 combinations visible | **passes, and Round 2 widened it.** No match is AC5 and several matches is AC6, both decided by the architect once `Q-001` and `WI-0001/Q-001` landed. Round 2 added the combinations nobody had named: unrecognised input and a closed input stream at either prompt (AC7), an unparseable card file (AC8), the wrong number of arguments and an empty argument (AC9), an empty file and a missing file (folded into AC5), the file left behind when the last card goes (AC4), and `review` being untouched (`## Out of scope`) | resolved in Round 2 |

## Q1 — When you want to delete a card, how do you tell the tool which one?

Filed as `WI-0003/Q-001`, blocking, addressed to the stakeholder. Why it is theirs and not covered
by *"whatever you think is best"*: option B needs a way to **see** the cards' numbers, which is
work no item records, so the answer can change the shape of the epic. It also changes what they do
at the keyboard rather than what a thing is called. Options put to them: by the front side typed
out; by a number the tool assigns, with the listing that implies; by picking it during a review.
Recommendation stated as ours, last, after the options: by the front side, with B and C scoped as
their own items if wanted.

**Answer:** the stakeholder chose **A**, the front side typed out, in their own words:

> A — by typing the front side. I don't need a numbered list for this.

[src: WI-0003/Q-001] Propagated as AC1. The second sentence is read as a decision *against* the
listing command, not a postponement of it, so no work item was filed and the item's `## Out of
scope` now excludes it explicitly.

## Q2 — What should protect you from deleting the wrong card?

Filed as `WI-0003/Q-002`, blocking, addressed to the stakeholder. Why it is theirs: it settles an
exclusion this item currently carries as ours (no undo, no trash), and it bears directly on the
thing they named as a failure of the whole product — *"losing my progress"* (`EP-001/Q-004`).
Deleting a card destroys its rung and its due date as well as its text. Options put to them:
nothing; confirm before deleting; recoverable. Recommendation stated as ours, last: confirm before
deleting.

Two decisions were deliberately **not** folded into one question. "Confirm or not" and "recoverable
or not" are two answers to the same worry, so they are one decision — *how much protection* — and
one question. What was kept out of it entirely is Q1's identification mechanism, which would have
made this a question that could be half-answered.

**Answer:** the stakeholder chose **B**, show the card and ask, in their own words:

> B — show me the card and ask first. One keystroke is worth it to not lose a month of progress by
> fat-fingering a delete.

[src: WI-0003/Q-002] Propagated as AC2, which requires the prompt to show the card's rung and due
date and not only its two sides — the schedule is the part they call progress. Their answer also
settles the undo exclusion this item carried as ours: they chose the confirmation over the trash,
so deletion being permanent is now theirs. Both answers are written up in
`docs/architecture/adr/ADR-0005-deleting-a-card-names-it-by-front-side-and-confirms.md`.

## Q3 — What happens when the identifier matches nothing, or matches several cards?

**Not asked, and now decided by the architect.** `[decided]`

It was R10's gap and it was genuinely not answerable when `refine` wrote this: what "matches
several" even means depended on `Q-001` (are we matching front text at all?) and on
`WI-0001/Q-001` (can two cards share a front side?). Both have since been answered — front text,
yes — so the case is real and it is ours, which is what `WI-0003/Q-001` said in writing when it was
filed.

**Decided, no match:** the tool prints a message naming the front side it did not find, exits
non-zero, and leaves the stored file unchanged. That is AC5, and it is word for word what this file
pre-recorded as ours to take.

**Decided, several matches:** the tool lists every match with both sides, its rung and its due
date, and asks which one to remove; exactly the chosen card goes and the others are untouched. That
is AC6. It follows `Q-002`'s protection, as this row said it would — the prompt already exists, and
this widens it from "this one, yes or no" to "which of these". The alternative, refusing on
ambiguity, was rejected because with no listing and no card numbers it would make duplicated cards
permanently undeletable, withdrawing a capability the stakeholder asked for on a case their own
answer to `WI-0001/Q-001` creates. The reasoning is in `ADR-0005`.

## Q4 — What is the delete command called, and what does the confirmation say?

**Not asked.** `[assumed]`

Covered by the stakeholder's standing deferral: *"As for how it's actually built — whatever you
think is best"* (`EP-001/Q-004`), which the procedure says applies to the category — how it is
built, what things are called, the wording of output — and not only to the question that produced
it.

**Assumed:** the operation is a subcommand named `delete`, matching the `add` subcommand assumed on
WI-0001, and the confirmation names the card that was removed. Reversible; renaming a subcommand
before anything is built costs nothing.

## A risk this item carried into `plan` — closed in Round 2

**Round 2 closed it by declaring `depends-on: WI-0001`.** WI-0001 is `done`, so the dependency is
satisfied and R7 now passes in substance rather than only in form. What follows is how it read when
Round 1 wrote it, kept because it is the reasoning the field now carries.

**R7, independent deliverability.** WI-0003 declares no `depends-on`, and in form that is a pass.
In substance, deleting a card cannot be built before there are cards: it reads and rewrites
whatever WI-0001 stores. `Q-001`'s answer has removed the other half of the risk — option C would
have made this need WI-0002's session as well, and they did not choose it — so WI-0001 is the only
real predecessor. This is not the stakeholder's decision and it is not a criterion; it is a
sequencing fact, recorded here and in `## Notes` so that `plan` meets it deliberately rather than
discovering it.


## Round 2 — no questions, and what was decided instead

`refine` ran a second time on 2026-08-30 after `answer-questions` returned the item to `draft`.
One Definition of Ready criterion was failing — R4, because AC1 and AC2 said "the tool's delete
command" and named none — and the repair had already been recorded as ours in Q4 below.

**Nothing in this round was put to the stakeholder, and the test in the procedure is why.** Every
gap left is a name, a keystroke or an exit code: the answer would be the same whoever the
stakeholder was, and `EP-001/Q-004`'s *"As for how it's actually built — whatever you think is
best"* covers the category, not only the question that produced it. Asking would have told them
their answer was not heard. Nothing in this round changes what the tool is for, what it promises,
or what happens to their data — the two things that would have made a question real, how a card is
named and whether they are asked before it goes, are `Q-001` and `Q-002` and they answered both.

### Q5 — What exactly does the confirmation take, and what do the outcomes exit with?

**Not asked.** `[assumed]`

**Assumed:** the confirmation prompt states what it takes and takes `y` to delete and `n` to keep,
matching the outcome prompt of `WI-0002`'s review session, which the stakeholder has already used.
A confirmed deletion prints a line naming the front side removed and exits zero. A declined
deletion prints a line saying nothing was deleted and exits **zero** — declining is an ordinary
outcome and not an error, which is `ADR-0005`'s wording. A front side matching nothing exits
non-zero, which is `ADR-0005` as well. That is AC1, AC2 and AC5.

Basis: the standing deferral. Reversible: nothing stored depends on any of it.

### Q6 — How does the several-match prompt let you say which one?

**Not asked.** `[assumed]`

`ADR-0005` already decided the shape — *"lists every match with both sides, its rung and its due
date, and asks which one to remove"* — under the delegation `WI-0003/Q-001` recorded. It did not
say how the person names one of the listed cards, and something has to.

**Assumed:** the matches are numbered from 1 in the order they appear in the card file, and the
prompt takes that number, or `n` to remove nothing. That is AC6.

**Checked against the stakeholder's own words, because it is the one assumption here that brushes
against them.** They wrote *"I don't need a numbered list for this"* (`WI-0003/Q-001`). That
sentence is a decision against option B of that question — a number the tool assigns to every card,
kept across runs, with a listing command to see the numbers, as the way a card is named. What AC6
numbers is the two or three cards already on screen inside a prompt that only exists when their own
chosen identifier is ambiguous, and the numbers are gone when the command exits: there is nothing
to look up, nothing to list, and no way to use a number anywhere else in the tool. They are
compatible, and the alternative is worse for them — with no listing and no card numbers, refusing
on ambiguity would leave duplicated cards permanently undeletable, which `ADR-0005` records as the
reason this rule exists at all.

Not escalated as a conflict under ADR-0008 §3: the two sentences do not contradict, and the
mechanism they might be read to touch was delegated to us in writing by the same question their
sentence answers.

### Q7 — What happens at the prompt when the answer is neither `y` nor `n`, or the input runs out?

**Not asked.** `[assumed]`

**Assumed, as AC7:** an unrecognised answer removes nothing and asks the same question again,
reprinting the card or the numbered list so nobody is asked about text that has scrolled away —
this is `WI-0002` AC13's rule, and copying it is what keeps the two commands feeling like one tool.
The input stream ending removes nothing, prints that nothing was deleted, and exits zero.

**The one place this deliberately differs from `WI-0002`.** There, a closed input stream is a clean
quit, because stopping a review costs nothing. Here the act being confirmed is irreversible by the
stakeholder's own decision (`WI-0003/Q-002`, `ADR-0005`), so the reflex has to fall on the side of
not deleting. Recorded as ours; it is behaviour at the terminal and costs nothing to change.

### Q8 — What about a card file that will not parse, and a `delete` called wrongly?

**Not asked.** `[assumed]`

**Assumed:** AC8 — an unparseable card file stops `delete` before any card is shown and before any
prompt, naming the file and the line, exiting non-zero, file untouched. This is not a new rule; it
is the refusal `add` and `review` already make (`ADR-0007`, `WI-0002` AC14), and writing it as a
criterion is what stops `delete` quietly acquiring a different one. AC9 — no argument or several
arguments is a usage message and a non-zero exit; an empty or whitespace-only argument is AC5's
no-match, because `WI-0001` AC7 makes an empty front side unstorable, so no card can have one.

### What Round 2 did not do

It did not touch `ADR-0005` or any other document. Everything above sits under an ADR that already
exists, and `refine` does not write architecture documents — had any of it needed the ADR changed,
the procedure would have had this execution file a question to the architect instead.

It filed no question to the stakeholder, and it recorded no Definition of Ready override. All ten
criteria pass on their own terms; the per-criterion record is in this execution's journal entry.

## Cross-answer check

Checked against: EP-001/Q-001; EP-001/Q-002; EP-001/Q-003; EP-001/Q-004; EP-001/Q-005.

Written by `refine` when no answers had arrived, checking that neither question re-asked something
already settled. Both have since been answered; the check on those two answers against the prior
record is on the question files themselves and in the item's journal, and neither conflicted with
anything the stakeholder had said before.

- `EP-001/Q-004` — the answer this item came from, and the one both questions lean on. It asked for
  deletion and it named losing progress as a failure; it did not say how a card is named, and its
  *"whatever you think is best"* covers the subcommand's name but not whether the tool may destroy
  a card's schedule without asking. That line is why Q4 was assumed and Q1 and Q2 were not.
- `EP-001/Q-003` — compatible: a deleted card is not a card that came due, so nothing here changes
  the due rule. AC2's "never offered again" is a consequence of the card being gone, not a new
  scheduling rule.
- `EP-001/Q-005` — compatible: it is about how many due cards a session offers. Option C of Q1
  would put a delete key inside a session, which is a change to WI-0002's session and would be
  scoped as its own item; it would not change how many cards that session offers.
- `EP-001/Q-001` — compatible: the command line. All three options in Q1 are things a
  command-line tool does.
- `EP-001/Q-002` — compatible: the ladder. Q2 says out loud that deleting a card destroys its rung
  and due date, which is a consequence of that answer rather than a change to it.

### Round 2's check

Checked against: EP-001/Q-004; WI-0003/Q-001; WI-0003/Q-002; WI-0001/Q-001; WI-0002 (its delivered
criteria). Round 2 consumed no new human answer — it wrote criteria from assumptions — so the check
runs the other way: every assumption read against what the stakeholder has already said.

- `EP-001/Q-004` — *"whatever you think is best"* is the authority for all four assumptions, and
  the same answer's *"losing my progress"* is why AC7's closed input stream deletes nothing.
- `WI-0003/Q-001` — *"I don't need a numbered list for this"*. The one assumption that touches it
  is AC6's numbered prompt; compatible, argued in full under Q6 above, not reconciled by editing
  anything of theirs.
- `WI-0003/Q-002` — *"show me the card and ask first"*. AC2 keeps the prompt on every deletion and
  AC7 makes every ambiguous input keep the card; nothing here weakens it, and the `## Out of scope`
  refusal of a force flag still stands.
- `WI-0001/Q-001` — two cards may share a front side. That is what makes AC6 a real case rather
  than a hypothetical, and AC6 cites it.
- `WI-0002` — the session. This item adds no key to it and removes none; the new
  `## Out of scope` entry says so, and it is why `WI-0002`'s AC1–AC14 all still read true.

No conflict was found, so no question was filed under ADR-0008's obligation.
