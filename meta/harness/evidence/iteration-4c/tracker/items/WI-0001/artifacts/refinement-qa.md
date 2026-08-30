---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`: the conversation has happened. The two questions that were the stakeholder's
were filed as `WI-0001/Q-001` and `WI-0001/Q-002`, they answered both, and their answers are
quoted verbatim below. The decisions that were **not** theirs are settled below under their
standing delegation and were not put to them.

The stakeholder is asynchronous, so the exchange happened through the question files rather than
in a conversation; `answer-questions` propagated both answers into the criteria and into `docs/`,
and returned the item to `draft` for `refine` to finish. **Round 2 below is that finish**, and it
put nothing further to the stakeholder: every remaining gap fell under the deferral they had
already given, and asking again would tell them their answer was not heard.

## Round 1 — the agenda, and where each item of it went

`refine` read WI-0001 against `spec/dor-dod.md` §1 before writing anything. What failed, and who
each failure belongs to:

| DoR | verdict as found | who it is for |
|-----|------------------|---------------|
| R1 frontmatter | pass — `type`, `epic`, `priority` all set | — |
| R2 story | pass — role, capability, and a "so that" | — |
| R3 criteria exist | pass — AC1–AC5 as found, AC1–AC8 now, labelled, checkboxes | — |
| R4 decidable by observation | **fail as found; repaired in round 2** — AC1 now names the `add` subcommand and its two arguments, and AC2 to AC4 name the observation that settles each | was ours under a standing deferral; taken in round 2 |
| R5 out of scope | pass — five entries as found, seven now, including deletion, editing, and hand-editing the file | — |
| R6 questions non-blocking | fail while suspended; **now passes** — `Q-001` and `Q-002` are both answered and no question on the item is open | the stakeholder — answered |
| R7 independently deliverable | pass — no `depends-on` | — |
| R8 Q&A recorded | **now passes** — the answers arrived and this file is `recorded` | resolved |
| R9 one coherent change | pass — one command, one file, one persistence promise | — |
| R10 combinations visible | **fail as found; passes after round 2** — a duplicate front is AC6, an empty side is AC7 with its precedence over AC6 stated, a missing card file is AC8, and the argument-count case is named in `## Notes` as deliberately unconstrained | duplicates were the stakeholder's (`Q-001`) and they answered; the rest were ours |

## Q1 — When you add a card whose front side is exactly the same as a card you already have, what should the tool do?

Filed as `WI-0001/Q-001`, blocking, addressed to the stakeholder. Why it is theirs and not ours:
they told us what they use this for — *"running through vocab"* (`EP-001/Q-001`) — and in vocab a
word with two meanings is two cards with one front, while the same card typed twice is a mistake.
The tool cannot tell those apart and they can. Options put to them: add silently; refuse; add with
a warning. Recommendation stated as ours, last, after the options: add with a warning.

**Answer:** the stakeholder chose **C**, add it and warn, in their own words:

> C — add it and warn me. I don't want it refusing a second meaning of a word, and a warning is
> enough to catch a typo.

[src: WI-0001/Q-001] Propagated as AC6 on the item, with AC3 narrowed to the distinct-front case
so that the two situations are covered separately. The tool never refuses a card for being a
duplicate, and the warning is what catches the typo they were worried about.

## Q2 — Does the card file have to be something you can open and read yourself, or is its format ours to choose?

Filed as `WI-0001/Q-002`, blocking, addressed to the stakeholder. Why it is theirs and not ours:
AC5 is intake's own addition, flagged at the time as something to put to them rather than let
stand as if they had asked for it, and it goes further than the sentence it was written from —
*"It needs to live in a file on my machine that survives a reboot"* (`EP-001/Q-004`). It is also
the one decision here that is expensive to undo: their study history accumulates in whatever the
first version writes. Options put to them: readable and hand-editable; readable but the tool's to
write; format ours. Recommendation stated as ours, last: readable but the tool's to write.

**Answer:** the stakeholder chose **B**, readable but the tool's to write, in their own words:

> B. I want to be able to open it and see my cards are still there, but I'm not asking to
> hand-edit it — that's a different thing.

[src: WI-0001/Q-002] AC5 was already written to that promise by intake, so it stands and is now
sharpened to say what readable excludes; hand-editing is out of scope on the item. Because the
commitment binds every later version and is expensive to reverse once real study history exists,
it is recorded as `docs/architecture/adr/ADR-0004-card-file-is-readable-text-owned-by-the-tool.md`
rather than only as a criterion.

## Q3 — What is the add command called, and how are the two sides supplied?

**Not asked.** `[assumed]`

The stakeholder answered this category, not just one question in it: *"As for how it's actually
built — whatever you think is best"* (`EP-001/Q-004`). `refine`'s procedure names exactly this
case — a standing deferral over how it is built, what things are called, and the wording of
output — and says to decide it and say so, because asking anyway tells them their answer was not
heard.

**Assumed:** the add operation is a subcommand named `add`, and the two sides are supplied as two
arguments on the command line, front first, so that one line of typing adds one card without a
prompt. The name of the executable itself is `plan`'s to choose along with the language and the
packaging; this criterion will name the subcommand, not the binary.

Basis: `EP-001/Q-004`'s deferral, and `EP-001/Q-001`'s picture of the use — *"once a day at a
terminal"* — which a prompt-driven flow would slow down for no gain. Reversible: renaming a
subcommand before anything is built costs nothing.

## Q4 — What happens if the front or the back is empty?

**Not asked.** `[assumed]`

Same deferral. A card with an empty side cannot be reviewed — there is nothing to show or nothing
to check against — so accepting one would put an unusable row in the file the stakeholder is
promised will hold their progress.

**Assumed:** the tool refuses a card with an empty or whitespace-only front or back, prints a
message saying which side was empty, exits non-zero, and writes nothing. Reversible: it is one
check at the entry point.

## Q5 — What exactly does the confirmation say?

**Not asked.** `[assumed]`

Same deferral; the wording of output is named in it explicitly.

**Assumed:** the criterion will require that the confirmation names the card that was added — the
front side, at least — so that a person who mistyped sees it immediately. The exact sentence is
`plan`'s and `implement`'s.

## Round 2 — finishing the refinement, with nothing new put to the stakeholder

`refine` ran again after `answer-questions` returned the item to `draft`. Two Definition of Ready
criteria were still failing: R4, because AC1 named no command and AC2 to AC4 named no observation,
and R10, because the empty-side behaviour lived in Q4 below as an assumption rather than in a
criterion where `verify` would read it.

**Nothing in round 2 was put to the stakeholder, and this is the reasoning for that.** Each
remaining gap was tested against `refine`'s routing order. None had a product stake: none changes
what the tool is for, what it promises, or what they would notice about their own cards. Every one
falls inside *"As for how it's actually built — whatever you think is best"* (`EP-001/Q-004`),
which is a standing deferral over a whole category — how it is built, what things are called, the
wording of output, exit codes, file layout. They have already answered four questions on the epic
and two on this item; asking a seventh about the name of a subcommand would tell them their answer
was not heard.

### Q6 — What settles AC1, AC2, AC3 and AC4, for someone with a terminal and no context?

**Not asked.** `[assumed]`

The criteria asserted the right things and named no observation, which is R4's exact failure. What
changed, and why:

- **AC1** now names the `add` subcommand, says there are exactly two arguments and which order
  they go in, and requires exit zero. That is Q3's assumption below, promoted from a note into the
  criterion, which is where `verify` will look for it.
- **AC2** said the card "is still there" and did not say how anyone would see it. It now says the
  observation: read the card file with an ordinary text tool. That reading is only possible
  because of the stakeholder's own answer to `WI-0001/Q-002` and `ADR-0004`; before that answer
  the criterion could not have been written this way.
- **AC3** said the three cards are "present in the stored file", which was already decidable, and
  now names the same reading explicitly so that all four criteria are settled the same way.
- **AC4** asserted that the card "is due in that day's review session and remains due until it is
  answered". That is a claim about WI-0002's session, which this item does not deliver, so nobody
  could settle it here. It is narrowed to what this item actually writes — the due date in the
  record equals the date the card was added — with a parenthesis saying where the rest lives.

Basis: `EP-001/Q-004`'s deferral for the naming; `WI-0001/Q-002` and `ADR-0004` for the readable
file that makes the observations possible; `ADR-0002` for the scheduling state a card carries.
Reversible: renaming a subcommand before anything is built costs nothing.

### Q7 — Where do the empty-side, missing-file and wrong-argument-count cases go?

**Not asked.** `[assumed]`

R10 asks that every combination this item introduces is visible — in a criterion, in
`## Out of scope`, or in `## Notes` as deliberately unconstrained with who left it so. Three were
not:

- **An empty or whitespace-only side** was Q4 below, an assumption in prose. It is now **AC7**,
  with one thing added that nobody had stated: it happens **before** AC6's duplicate check, so an
  empty back side with a duplicate front is refused by AC7 and prints no duplicate warning.
  Without that ordering, AC6 and AC7 both claim the same case and an implementation could satisfy
  either.
- **The card file not existing yet** was stated nowhere at all. It is now **AC8**. This is the
  first thing that happens on a clean machine, and without it AC1 was not decidable there.
- **The wrong number of arguments** is named in the item's `## Notes` as deliberately
  unconstrained, left by `refine` to `plan` and `implement` under the same deferral. A usage
  message and a non-zero exit is what every command-line tool does; no observation of the exact
  wording would tell anyone whether this item delivered what was asked for.

Basis: `EP-001/Q-004`'s deferral. Reversible: all three are checks at the entry point.

### Q8 — Is the criterion set still one coherent change?

**Not asked.** `[assumed]`

R9. The item grew from five criteria to eight, and none of the three new ones is a second piece of
work: AC7 and AC8 are the failure and first-run cases of the same `add` command, and AC6 came from
the stakeholder. There is still one command, one file, and one promise about persistence. No split
is warranted and none was made.

## What was deliberately left to `plan`

- The language, the file format, the packaging and the executable's name. The stakeholder
  delegated all of it (`EP-001/Q-004`), and none of it changes what a criterion asserts — except
  the format, which `Q-002`'s answer now constrains: any format `plan` likes, provided a person
  can read the cards and their schedule out of it (`ADR-0004`).
- Where the file lives by default. AC5 already requires the path to be documented; which path it
  is is a design decision with no product stake, and `plan` settles it.

## Cross-answer check

Checked against: EP-001/Q-001; EP-001/Q-002; EP-001/Q-003; EP-001/Q-004; EP-001/Q-005.

Written by `refine` in round 1, when no answers had arrived, and checking the other direction:
that the two questions being asked were not things the stakeholder had already answered. Both have
since been answered, and the check on those two answers against the prior record is on the question
files themselves and in the item's journal. Neither conflicted with anything they had said before.

**Round 2 recorded no new stakeholder answer**, so there is nothing on this pass for a cross-answer
check to run against — `lint-answers --item WI-0001` sees the same two consumed answers it saw
before. What round 2 did check, in the other direction, is that none of its three assumptions
contradicts a recorded answer: AC7's precedence over AC6 does not weaken `WI-0001/Q-001`'s *"add it
and warn me"*, because it applies only where the card is refused for being empty and no card is
added at all; AC8 adds nothing to `WI-0001/Q-002`'s promise beyond creating the file it describes;
and AC4's narrowing removes a claim about WI-0002's session that this item could not settle,
leaving `EP-001/Q-003`'s due rule untouched and unrestated.

- `EP-001/Q-004` — the closest call, and the reason Q3 to Q5 above are not being asked. Its
  standing deferral covers naming, wording and how it is built; it does **not** cover what happens
  to a duplicate card (a behaviour, not a mechanism) and it does not cover how strong the
  promise about the file's readability is, which is why those two are being put to them.
- `EP-001/Q-003` — compatible: it decides when a card is due, and AC4 already carries the
  consequence for a new card. Neither question touches it.
- `EP-001/Q-005` — compatible: it is about how many due cards a session offers, which is WI-0002.
  Nothing here changes it.
- `EP-001/Q-001`, `EP-001/Q-002` — compatible: the command line, and the ladder. Neither question
  reopens either.
