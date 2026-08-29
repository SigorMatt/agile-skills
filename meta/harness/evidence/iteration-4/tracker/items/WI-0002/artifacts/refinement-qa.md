---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`. Two rounds. Round 1 asked the stakeholder one question and received one
reply, quoted verbatim below. Round 2 asked them nothing, and the section headed
"Round 2 — nothing asked, and why" is the record of that decision rather than an omission.

Answers are tagged `[human]` when the stakeholder said it, `[assumed]` when `refine` proposed it
under a deferral or a routing rule. Nothing is left `[unresolved]`.

## Round 1 — asked of the stakeholder, reply received 2026-08-29

**Q1 (`Q-001`) — During a review, what do you press to reveal the answer, to say you got it
right, to say you got it wrong, and to stop the session early?**

> *"Enter to see the answer, y for right, n for wrong, q to stop. That's the one I can just use
> without being told the keys."*

`[human]` — option A, as recommended, and for the reason the option gave: it is the map a person
can use on the first day without being told what the keys are.

Why the stakeholder and not `refine`: it is the interaction they perform a few hundred times a
week, it is the one part of this item they will actually feel, and AC1, AC2, AC5 and AC6 all
quote it. It is not a choice that would come out the same whoever the stakeholder was — someone
who already uses Anki would answer B without hesitating.

Propagated by `answer-questions`: AC1 names Enter as the reveal; AC2 names `y` for right and `n`
for wrong; AC5 names `q` and states that it ends the session at either moment, question side or
answer side showing; AC6 states that the report is produced whether the session ran out of due
cards or was ended with `q`; AC9 gains a concrete piped invocation,
`printf '\ny\n\nn\n' | recall review`, so a whole two-card session can be driven from one
command.

Deliberately **not** asked alongside it, although both were tempting: what the session prints
around each card, and what the end-of-session line says word for word. Those would have the same
answer whoever the stakeholder was, so they are assumptions below rather than questions.


## Decided by `refine` in round 1, not asked

- **The command is `recall review`.** `[assumed]` — follows `recall add` and `recall list` in
  WI-0001; the stakeholder has named no commands.
- **Due cards come oldest-due-first, ties broken by ascending card number, and the order is
  stable across runs.** `[assumed]`, written as AC8. Something has to fix the order or AC4 and
  AC5 cannot be checked twice with the same result; oldest-first is the order that matches what
  a spaced-repetition tool is for. A random order would be a product decision, and nothing the
  stakeholder said asks for one.
- **An empty session prints one plain line and exits 0.** `[assumed]`, written into AC3 — the
  same shape as WI-0001 AC8's empty listing. Nothing due is not an error.
- **The end-of-session report is a line stating how many cards were reviewed and how many were
  right.** `[assumed]` — AC6 already required both numbers; this fixes it as one line so a
  verifier knows what to look for.
- **The session must be drivable from a pipe.** `[assumed]`, written as AC9. Without it every
  criterion on this item needs a person at a keyboard to check, which would make `verify`'s job
  impossible — it cannot ask anyone anything and it has no hands. This is the one assumption
  here that exists for the pipeline's sake rather than the user's, and it is recorded as such.
- **No cap on session length, and no way to split a session.** `[assumed]`, recorded in
  `## Out of scope`. The session is already finite because only due cards are in it.

## Round 2 — nothing asked, and why

Round 2's agenda was the Definition of Ready table at the foot of round 1, which round 1 itself
recorded as out of date once the reply arrived, plus the one thing round 1 named for round 2 to
settle: what the session does with a key outside the map.

The addressee test was applied to every remaining gap, in the order the procedure gives, and
none of them reached the stakeholder:

- **Already answered — not re-asked.** Which cards a session presents. `ADR-0001` states that a
  newly added card is due the day it is added, and `EP-001` SM2 says the same as a success
  measure. AC1 now cites that rather than restating it as a new decision.
- **Covered by a standing deferral.** *"Whatever you think is best, you know this better than I
  do."* — the stakeholder's reply on `WI-0001/Q-002`. The procedure says a deferral of that
  shape answers the *category*: naming, output wording, exit codes, file layout, and how a thing
  is checked. Where the recorded result is observed (the store file), how a mixed set of due
  dates is produced for AC8 (by hand-editing that file), what an exhausted pipe does, and what
  an unrecognised key does all fall inside it.
- **Implementation-only — routed to `plan`.** Three more design questions were added to the
  item's `## Notes` rather than asked: which fields carry the result and the next-due date and
  what the store's `version` becomes; what next-due value this item writes, given that WI-0003
  replaces it; and how the end of standard input is told apart from a `q`.

Filing a round-2 question would have stopped the loop for a decision that is not theirs, and —
on the ones their deferral covers — would have told them their answer was not heard. That is the
failure recorded as F-023.

### Decided in round 2

1. **AC1 names the setup that makes a card due.** `[assumed]`, on the record rather than on a
   judgement: `ADR-0001` and `EP-001` SM2. Before this, nothing in the item said which cards a
   session presents, so a verifier with a terminal and no context could not produce a due card
   and AC1 could not be settled at all.
2. **AC2 names where the result is observed: the store file, with the record for a `y` differing
   from the record for an `n`, and `README.md` naming the field.** `[assumed]`. "That result is
   still recorded" named no observation. AC4 shows only that a card *was* reviewed; nothing
   distinguished right from wrong, which is precisely the state WI-0003 schedules from. Reading
   the store is the observation WI-0001 AC5 was written to make possible, and it adds no command
   the stakeholder did not ask for — an alternative, some `recall history`, would have been new
   scope invented to make a criterion checkable.
3. **AC8 names how a mixed set of due dates is produced: by hand, in the store file.**
   `[assumed]`. Every card in a fresh pile is equally due, so within this item alone the
   oldest-due-first ordering had nothing to order. `verify` hand-edited the store for WI-0001
   AC6 for the same reason, and the criterion is stronger for it: the order is then demonstrably
   produced by the tool rather than inherited from the file.
4. **AC9 settles the exhausted pipe: input ending mid-session ends it exactly as `q` does.**
   `[assumed]`. AC9 asks a verifier to drive sessions from `printf`, so input running out early
   is the ordinary case rather than an edge one, and every AC5 check would otherwise depend on
   an unstated behaviour.
5. **AC10 is new: a key outside the map is ignored and the prompt repeats.** `[assumed]`. Round
   1 recorded this as deliberately unconstrained *because `Q-001` had not fixed the map*; it has,
   so the reason is gone. Of the two candidate behaviours, ignoring cannot destroy anything,
   while counting a stray key as a wrong answer would record a result the reviewer did not give
   — and undo is out of scope.
6. **Input is read a line at a time**, so a key is followed by Enter. `[assumed]`, and recorded
   as a consequence rather than a choice: AC9 has required pipe-drivability since round 1, and a
   reader that demanded a terminal could not satisfy it. Stated at the head of the criteria so
   that AC1, AC2, AC5 and AC10 all mean one thing. The matching exclusion — no raw keypress
   mode, no screen control — is now in `## Out of scope`.

### Recorded for WI-0003's refinement, not decided here

`ADR-0001` says a newly added card is due the day it is added and that a right answer moves a
card up one rung, but does not say which rung a new card is *on*. So "next due in 3 days" and
"next due in 1 day" are both readings of the first correct answer on a new card. It is WI-0003
AC2's to fix and this item does not touch it; it is written into WI-0002's `## Notes` under the
seam with WI-0003 because this item is what first puts a next-due value on a card.

## Definition of Ready — state at the end of round 2

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `depends-on: WI-0001`, `blocks: WI-0003` |
| R2 | pass | `## Story` names the role (someone reviewing daily), the capability (be shown only due cards, one at a time, and record each result), and the outcome ("so that a day's review is finite and my answers are remembered") |
| R3 | pass | AC1–AC10, each a labelled checkbox |
| R4 | **was failing, now pass** | at the end of round 1, AC1, AC2 and AC5 named no keys. `answer-questions` fixed AC1, AC2, AC5, AC6 and AC9 from the stakeholder's reply; round 2 then fixed the three that were still not decidable — AC1 (no way to produce a due card), AC2 (no observation for "still recorded"), AC8 (no way to produce differing due dates) — and added AC10. Every criterion now names a command and the verdict that follows: AC1 `printf '\ny\n\nn\n' \| recall review` and the order of the four strings in its output; AC2 the same session plus a read of the store file; AC3 an empty store and a just-emptied one; AC4 a second `recall review`; AC5 two piped sessions and a following `recall review`; AC6 the last line of each; AC7 `recall review --deck german` and a three-card session; AC8 hand-set due dates and a restored copy; AC9 `printf '\ny\n' \| recall review`; AC10 `printf 'x\n\nz\ny\n' \| recall review`. No criterion carries an unmeasurable adjective |
| R5 | pass | `## Out of scope` names nine exclusions, including three a reader would assume were included: scheduling itself, a terminal-controlling interface, and any way to see a card's results other than the store file |
| R6 | pass | `Q-001` is `answered`; no question on this item is open |
| R7 | pass | `depends-on: WI-0001` is recorded and WI-0001 is now `done`, so the dependency is both sequenced and finished |
| R8 | pass | this file is `status: recorded` and holds both rounds — the stakeholder's reply verbatim, six round-2 decisions each tagged `[assumed]` with the deferral or routing rule it rests on, and this table |
| R9 | pass | one coherent change: due-card selection, a session loop over standard input, and a recorded result per card. It is not two items — the schedule is already WI-0003 and the store is already WI-0001 |
| R10 | pass | the item's R10 paragraph enumerates eleven combinations, each covered by a criterion, excluded in `## Out of scope`, or named as deliberately unconstrained with `refine` as the one who left it so |

No Definition of Ready override was recorded, and none was needed: every criterion passes on its
own terms. Noted because an override is the stakeholder's to request and they are not in this
session, so one could not have been obtained even if it had been wanted.

## Definition of Ready — state at the end of round 1, kept as the record of where the item was

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `depends-on: WI-0001`, `blocks: WI-0003` |
| R2 | pass | `## Story` names the role, the capability and the outcome |
| R3 | pass | AC1–AC9, each a labelled checkbox |
| R4 | **fail** | AC1, AC2 and AC5 name "the reveal key", "right" and "wrong" and stopping early without saying which keys those are — `Q-001` decides it. AC3, AC4, AC7, AC8 and AC9 are decidable as written; AC6 is decidable once the session can be ended, which is part of the same key map |
| R5 | pass | `## Out of scope` names scheduling, forcing or shuffling a session, undo, timing, session caps, and any command other than reviewing |
| R6 | **fail** | `Q-001` is open and blocking — deliberately, and this is what the item is suspended on |
| R7 | pass | `depends-on: WI-0001` is recorded and this item is sequenced after it; DoR R7 is satisfied by the dependency being recorded and ordered, not by it being finished |
| R8 | **fail** | this file was `status: agenda`; the conversation had not happened |
| R9 | pass | one coherent change: a due-card selection, a session loop, and a recorded result per card |
| R10 | pass | the combinations are enumerated in `## Notes`, each covered by a criterion, excluded, or named as deliberately unconstrained |

R4, R6 and R8 failed together, for one reason: at the end of round 1 the stakeholder had not
replied yet.
