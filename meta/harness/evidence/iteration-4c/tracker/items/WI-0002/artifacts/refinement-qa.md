---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`: this file is what was actually decided, not an agenda for a conversation
still to come. **Nothing was put to the stakeholder in this round, and that is the finding of the
round rather than an omission.** Every gap the Definition of Ready found on this item was either
already answered by them — in `EP-001/Q-002`, `Q-003`, `Q-004` or `Q-005`, quoted verbatim below
with its ID — or fell inside the standing delegation they gave for how the tool is built. The
decisions in the second class are marked `[assumed]` and name the deferral they rest on; none of
them is recorded as something the stakeholder said.

A stakeholder in an earlier run of this methodology wrote that three of four questions on one work
item were *"things I'd expect a team to just decide on their own"* (F-023). The test applied to
each gap below was the one `refine`'s procedure states: does the answer change what the software
is for, what it promises, or what they would notice — or would the answer be the same whoever the
stakeholder was?

## The agenda — WI-0002 read against `spec/dor-dod.md` §1 before anything was written

| DoR | verdict as found | who it was for |
|-----|------------------|----------------|
| R1 frontmatter | pass — `type`, `epic`, `priority`, `depends-on` all set | — |
| R2 story | pass — a role, a capability, and a "so that" naming the outcome | — |
| R3 criteria exist | pass — AC1 to AC11 as found, labelled, checkboxes; AC1 to AC14 now | — |
| R4 decidable by observation | **fail as found** — AC1 said the back is revealed "after the person asks for it", AC4 said "the person records right or wrong", AC11 said there is "an explicit way to stop", and none of the three named anything anyone could type. `verify` cannot ask; a criterion whose action is unnamed is undecidable | ours, under the standing deferral — taken below as Q1 |
| R5 out of scope | pass as found — five entries; nine now | — |
| R6 questions non-blocking | pass — no question is open on this item | — |
| R7 independently deliverable | pass — `depends-on: WI-0001`, which is `done` and merged | — |
| R8 Q&A recorded | **fail as found** — no `refinement-qa.md` existed; this file, at `recorded`, is the repair | resolved here |
| R9 one coherent change | pass — one subcommand, one loop, one file. See the note below | — |
| R10 combinations visible | **fail as found** — nothing said what an unrecognised key does, what happens with no cards or no card file, what a rung-0 card does when answered right, in what order two cards due the same day are offered, or what an unparsable file does | ours — taken below as Q2 to Q6 |

**On R9, because eleven criteria became fourteen.** This item is one coherent change and was not
split. Everything here is one command holding one loop over one list, writing one file: showing a
card without recording an answer delivers nothing a person could use, and recording answers
without showing cards is not a session. The criteria are many because the session has many
observable moments, not because it is several items.

## Q1 — What does the person actually type: to see the back, to say right or wrong, and to stop?

**Who it is for: ours.** `answer-questions` left this in `## Notes` for `refine` rather than
deciding it, and the test says it is a build decision — the answer would be the same whoever the
stakeholder was, and it is a key each, reversible in one line. The stakeholder has already
described the setting, *"it's just me, once a day at a terminal, running through vocab"*
(`EP-001/Q-001`), which is someone who wants the fewest keystrokes that can still be unambiguous.

**Options considered:** (a) Enter to reveal, then `y` / `n`, with `q` to stop; (b) typing the
words `right` and `wrong`; (c) a number per outcome, as several spaced-repetition tools use;
(d) space to reveal and the arrow keys to grade, which needs raw terminal input.

**Decision — (a), and it is the team's, not theirs.** `[assumed]`, under
*"As for how it's actually built — whatever you think is best"* (`EP-001/Q-004`). Words (b) are
four to five keystrokes per card for a person doing this daily; numbers (c) have to be learnt and
mean nothing on their own; raw terminal input (d) is a dependency on the terminal's mode that
`ADR-0006`'s standard-library-only decision would have to pay for, and it cannot be driven by a
pipe, which would make AC9 and AC11 untestable. Written into AC1 (Enter reveals), AC4 (`y` and
`n`), AC11 (`q`), and AC13 (anything else re-asks).

## Q2 — When the input stream ends rather than the person typing `q`, what happens?

**Who it is for: ours.** Nobody would state this in a requirement; it is what makes the item
testable at all, since every test drives the tool through a pipe.

**Options considered:** (a) treat end of input as the same clean stop as `q`; (b) treat it as an
error and exit non-zero; (c) treat it as a wrong answer for the card on screen.

**Decision — (a).** `[assumed]`, same deferral. (c) would record an answer the person never gave,
which is the one thing this item must not do; (b) would make an ordinary Ctrl-D look like a
failure. Written into AC11, which also makes AC9 checkable without a terminal.

## Q3 — In what order are the due cards offered when several are due?

**Who it is for: ours — but it was the closest call on this item.** Order is something the person
sees every day, so it was tested against the product question rather than assumed into the
deferral. What settles it is their own request in `EP-001/Q-005`:

> Don't cap it at some arbitrary number, but let me quit partway through without losing anything
> ... I'd rather see the honest number of cards waiting than have the tool quietly decide which
> ones I don't get to see today.

[src: EP-001/Q-005] They asked to be able to see and check what a session is doing. AC2 and AC10
turn that into a hand-check against the stored file, and a hand-check has to be repeatable.

**Options considered:** (a) oldest due date first, ties in card-file order; (b) the order the
cards appear in the file; (c) shuffled, so the person learns the cards rather than the sequence.

**Decision — (a).** `[assumed]`, same deferral. (c) is the one with a real argument behind it —
order effects are a genuine cost in a deck reviewed daily — and it is recorded here as the option
not taken, because it makes the order unpredictable from the file and so makes AC2's and AC10's
hand-check unrepeatable, which is the property the stakeholder asked for. (b) ignores that a card
missed for a week is more urgent than one due today. Written into AC12, which states the order as
a function of the stored file alone.

## Q4 — What happens when there is nothing to review: no due cards, no cards at all, or no card file?

**Who it is for: ours.** AC8 already said "when nothing is due"; what it did not say is whether an
empty deck and a missing file are that case or a different one. On a clean machine the missing
file is the first thing anyone will meet.

**Options considered:** (a) one case — say nothing is due, exit zero, write nothing; (b) three
messages, one per situation; (c) create the card file on `review` as `add` does, so the states
converge.

**Decision — (a).** `[assumed]`, same deferral. (b) is more information than the moment carries.
(c) was rejected deliberately: `review` has nothing to write, and a command that creates a file
just by being run is a surprise on a machine the person is only trying out. Written into AC8,
which requires the card file to be byte-identical afterwards or still absent.

## Q5 — What does a card at rung 0 do when it is answered, and what does an unparsable file do?

**Who it is for: ours, and mostly already recorded.** WI-0001 writes a new card at `rung: 0`,
meaning never answered, and `ADR-0002`'s ladder starts at 1 day; `ADR-0007` defines the field.
Nothing in WI-0002's criteria said what "moves up one rung" means for a card on rung 0, which is
every card's first review.

**Decision — the ladder is walked as `ADR-0002` and `ADR-0007` already define it**, and AC5 and
AC6 now spell out all five rungs rather than leaving the first one to be inferred. `[assumed]`,
and it is a restatement of recorded decisions rather than a new one. An unparsable card file stops
the session before the first card, which is the refusal WI-0001's `add` already makes on the same
file; that is AC14, added so the case is stated somewhere rather than discovered.

## Q6 — Does an answer reach the file at the moment it is given, or at the end of the session?

**Who it is for: ours in mechanism, theirs in consequence — and they have already answered the
consequence.** They named losing progress as one of two things that would make the tool a failure
(`EP-001/Q-004`), and asked to *"quit partway through without losing anything"* (`EP-001/Q-005`).

**Decision — each answer is in the card file before the next card's front side is printed.**
`[assumed]` as to mechanism, but it is the only mechanism that satisfies AC9 for the case AC9
names — the tool being killed at a prompt — since a session that saves at the end loses
everything to a kill. Written into AC4 as an observation a reader can make from another terminal
part-way through a session.

## Cross-answer check

Checked against: `EP-001/Q-002`, `EP-001/Q-003`, `EP-001/Q-004`, `EP-001/Q-005`. **No conflict
found, and nothing was harmonised.**

- `EP-001/Q-002` fixed the rule — *"Just right or wrong — no difficulty scale ... a day, then
  three days, then a week, then a month. Get it wrong and it goes back to the start."* AC4, AC5
  and AC6 restate it and add no third outcome and no interval.
- `EP-001/Q-003` fixed what is due — *"A card's due if its date is today or earlier. If I miss a
  day it's just still due — nothing lost, nothing punished. A second session the same day should
  only show me whatever's still due, not everything again."* AC2, AC3 and AC7 are unchanged in
  substance; AC3 now says explicitly that the new date is counted from the day of the review, which
  is the only reading under which nothing is punished.
- `EP-001/Q-004` gave the delegation every `[assumed]` decision above rests on, and named losing
  progress as a failure — which AC4 and AC9 together now make observable.
- `EP-001/Q-005` chose no cap plus visibility. AC12's ordering was chosen **because** of it rather
  than against it: no card is withheld, only sequenced, and the sequence is predictable from the
  file so the hand-check they asked for gives the same answer twice. No session-length or
  session-size bound was added, as `## Notes` instructs.

No answer of theirs was overtaken by anything decided here, so neither move in
`meta/adr/ADR-0008-cross-answer-consistency.md` §3 was needed beyond citing compatibility.

## What is left open, and for whom

Nothing is `[unresolved]`. The wording of every prompt and message, whether a card's rung and due
date are shown alongside its sides, and the behaviour of `review` when given arguments it does not
take are named in the item's `## Notes` as deliberately unconstrained by `refine` — they are
`plan`'s and `implement`'s, and no observation of them would tell anyone whether this item
delivered what was asked for.
