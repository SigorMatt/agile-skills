---
status: recorded
---

# Refinement Q&A — WI-0004

`status: recorded`, as of round 2. Round 1's single question was filed as `Q-001`, the
stakeholder answered it, `answer-questions` propagated that answer, and round 2 has re-assessed
the Definition of Ready. The conversation this file records has happened, in full, and the
exchange below is what was actually said.

**Round 1's Definition of Ready table is left as it was written.** It recorded three failures at
a moment when they were real. Round 2's table, at the foot of this file, is the current one; the
two are meant to be read in order rather than as a contradiction.

Answers are tagged: `[human]` where the stakeholder said it, `[assumed]` where `refine` proposed
it or decided it under a deferral they gave, `[unresolved]` where it was asked and is not settled.

## Round 1 — one question to the stakeholder, filed 2026-08-29, answered 2026-08-29

**Q1 (`Q-001`) — When you delete a card, should the tool do it straight away, or stop and ask
you first?**

`[human]` — answered, option C: *"C — just delete it and tell me what got deleted. I'm only
ever going to run this right after I typo'd something, I don't need a prompt in my way for
that."* [src: WI-0004/Q-001]

Three options were on the file: A delete immediately, B show the card and ask `y/n`, C delete
immediately but print both sides of what was deleted. `refine` recommended C and named the
circumstance under which the recommendation would be wrong — a card that had climbed to the
30-day rung over months. The stakeholder's reason rules that circumstance out for them rather
than ignoring it: they delete only what they have just mistyped. `AC2` now states the behaviour
as a check.

What follows in this section is the reasoning that sent the question to them in the first place,
left as written because it is the record of that judgement.

Why this one reached the stakeholder, by the addressee test in the procedure's step 3, in order:

- **Product stake — yes.** It is what they do every time they delete, and it is the first
  destructive command in the tool. The answer changes what they type, what they see, and what
  happens when they mistype a digit. It differs by who the stakeholder is: someone who deletes a
  typo they made ten seconds ago wants A or C, someone protecting a card that took two months to
  reach the 30-day rung wants B. That is the same test that sent `WI-0001/Q-001` — one command
  or two prompts for `add` — to them rather than deciding it.
- **Already answered — no.** Nothing in `EP-001/Q-001`..`Q-005`, in any earlier
  `refinement-qa.md`, or in `docs/product/vision.md` addresses confirmation before a destructive
  action. There has never been a destructive action.
- **Covered by the standing deferral — no.** `WI-0001/Q-002`'s *"whatever you think is best, you
  know this better than I do"* answers the category of naming, output wording, exit codes and
  file layout. Whether the tool stops and waits for a keystroke is not wording; it is an
  interaction they perform. Deciding it under that deferral would be taking their words for more
  than they cover — the same line `WI-0003`'s refinement drew when it refused to decide the
  ladder's starting point under it.
- **Implementation-only — no.** Both options are cheap and both are testable; `review` already
  reads whole lines from a pipe, so a prompt costs nothing technically. There is no engineering
  reason to prefer either, which is what makes it a preference.

**Nothing else was filed with it.** Everything else this round settled is below, and each is
either covered by their deferral, forced by the record, or `plan`'s to decide. Filing any of it
would have told them their deferral was not heard, which is F-023.

## Decided by `refine` in round 1, not asked

1. **The command is `recall delete <number>`, taking exactly one positional argument: the card
   number `recall list` prints.** `[assumed]`, under the standing deferral on `WI-0001/Q-002`
   (the category is naming and the command surface) together with `ADR-0005`, which fixed that
   the first argument is the command name and everything after it is positional and never an
   option. The number is not a choice: it is the only handle on a card the user has ever been
   shown — `recall list` prints it and `recall add` announces it — and no other identifier
   exists in the store [src: ADR-0005; src: WI-0001 AC6].
2. **Deleting a card never renumbers the survivors.** `[assumed]`, and forced rather than
   preferred: the number is what the user types to delete, `recall list` printed it moments ago,
   and renumbering would silently change which card a number names between the listing and the
   next command. `AC3` states it as an observation on the store file.
3. **A number that names no card, a missing store, a wrong argument count and an unreadable store
   file each exit non-zero with a message on stderr, print nothing on stdout, and leave what is
   on disk untouched.** `[assumed]`, under the same deferral for the wording, and following
   `ADR-0004`'s established rule that a store the tool cannot read is reported and left alone
   rather than repaired or overwritten [src: ADR-0004]. `AC5`, `AC6`, `AC8` and `AC9`.
4. **`AC8`'s four wrong command lines — no argument, two arguments, `two`, and `0`.**
   `[assumed]`. `WI-0001` AC9 established that any count of positional arguments other than the
   expected one exits non-zero with a usage line; a non-integer and a `0` are the two ways an
   argument of the right count is still not a card number.
5. **Deleting the last remaining card leaves a store the tool still reads.** `[assumed]`. The
   alternative — removing the file when the pile empties — would make `recall list` report "no
   cards" for two different reasons and would lose nothing useful. `AC7`.
6. **`README.md` is the documentation `AC10` names.** `[assumed]`, same deferral, and the same
   resolution `WI-0001` AC5 and `WI-0003` AC4 took for the same phrase.
7. **Deletion is final: no undo, no trash, no way to recover an earned schedule.** `[assumed]`,
   and the weakest of these, which is why it is not left silent: nobody asked for undo, and
   adding it would be scope the stakeholder did not request from a person who has just declined
   three other things by name. It is written into `## Out of scope` **and** into `Q-001`'s
   context, so they see the assumption while they answer the question it bears on.

## Routed to `plan`, not to the stakeholder

Three design questions are in the item's `## Notes` rather than in a question file, because the
answer would be the same whoever the stakeholder was: whether a deleted card's number is ever
reused (`ADR-0004` option F against option G, on a premise this item removes); which exit code a
number that names no card gets, given `ADR-0005` assigns `2` and `1` to two cases this is neither
of; and whether the store's `version` changes. `AC5` and `AC6` say *non-zero* so that they stay
decidable while the value is open.

## Definition of Ready — assessed at the end of round 1

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | `[auto]` — `validate-workspace` exit 0; `type: work-item`, `epic: EP-001`, `priority: medium`, `arose-from: EP-001/Q-005` all present |
| R2 | pass | `[skill]` — role "someone keeping a pile of flashcards", capability "delete a card I added by mistake", outcome "so that a typo or a duplicate stops coming round in my daily review without my having to hand-edit the store file" |
| R3 | pass | `[auto]` — ten criteria, `AC1`..`AC10`, each a checkbox |
| R4 | **fail** | `[skill]` — nine of the ten name a command and an observable result. `AC2` names neither: it is a placeholder that says what `Q-001` will decide. That is honest rather than passing, and it is the reason this item is not Ready |
| R5 | pass | `[skill]` — `## Out of scope` names five things, including editing a card and undoing a deletion, both of which a reader could reasonably assume came with "delete a card" |
| R6 | **fail** | `[auto]` — `Q-001` is open and `blocking: true` |
| R7 | pass | `[auto]` — no `depends-on`; the three sibling items are all `done` |
| R8 | **fail** | `[auto]` — this file declares `status: agenda`, because the conversation it records has not happened. R8 exists precisely to stop an agenda passing as a record |
| R9 | pass | `[skill]` — one command, one code path, one section of `README.md`. Nothing here splits |
| R10 | pass | `[skill]` — the command takes no options and has no modes, so the combinations are the argument shapes, and `AC1`, `AC5`, `AC6`, `AC8` and `AC9` cover them. The two behaviours left unconstrained — number reuse and the specific exit code — are named in `## Notes` with `refine` recorded as who left them open, which is what R10 asks for |

Three criteria fail and all three are the same fact: the stakeholder has not answered `Q-001`
yet. No override was sought and none should be — nobody is present to give one, and an override
is the stakeholder's to offer, not `refine`'s to assume.

---

## Round 2 — no questions asked, and why

**Nothing was put to the stakeholder in this round.** Round 2 exists because `Q-001` came back
answered, and the item's history says exactly what was outstanding: `AC2`, and the two criteria
that failed because of it. That is the whole job. Re-opening the rest would be re-refining a
send-back as though it were a fresh draft — the item's other nine criteria, its scope and its
three routed design questions were settled in round 1 and nothing in the answer disturbs them.

Applying the addressee test to what round 2 actually did:

- **`AC2`'s final wording** — decided by `refine`, `[assumed]`, under the standing deferral on
  `WI-0001/Q-002`. The stakeholder decided the *behaviour* (act immediately, no prompt, tell me
  what went); how a criterion is phrased so a checker can settle it is not theirs to draft.
- **Nothing else changed**, so there was nothing else that could have needed asking.

### What round 2 changed in `AC2`, and why

`answer-questions` had written `AC2` as: exits 0 with nothing on stdin, and the one stdout line
contains both card sides and the number. That is faithful to the answer but it has a hole a
`verify` execution would have had to argue about: an implementation that *does* print a prompt,
reads end-of-file, and takes that as a yes would satisfy every clause of it. The stakeholder's
answer rules that implementation out — *"I don't need a prompt in my way"* — so the criterion
should too.

`refine` therefore pinned both streams, which is what makes the absence of a prompt observable:

> `recall delete 2 < /dev/null` exits 0 without waiting for input, writes nothing on stderr, and
> writes **exactly one line** on stdout, containing the number `2`, card 2's question text and
> card 2's answer text.

A prompt has to be shown to the user somewhere. With stdout fixed at one line and stderr empty,
there is nowhere for it to appear. `AC5` already pins a stream the same way (*"prints nothing on
stdout"*), so this is the item's existing idiom rather than a new one. The exact wording of the
line is still `plan`'s and `implement`'s, under the same standing deferral — `AC2` says what the
line must *contain*, not how it must read.

## Definition of Ready — re-assessed at the end of round 2

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | `[auto]` — `validate-workspace` exit 0; `type: work-item`, `epic: EP-001`, `priority: medium`, `arose-from: EP-001/Q-005` all present |
| R2 | pass | `[skill]` — unchanged from round 1: role "someone keeping a pile of flashcards", capability "delete a card I added by mistake", outcome "so that a typo or a duplicate stops coming round in my daily review without my having to hand-edit the store file" |
| R3 | pass | `[auto]` — ten criteria, `AC1`..`AC10`, each a checkbox |
| R4 | **pass** (was fail) | `[skill]` — the failure was `AC2` and only `AC2`. It now names a command (`recall delete 2 < /dev/null`), an exit code (0), and three observations (stderr empty, stdout exactly one line, that line containing `2` and both of card 2's sides). Each of the other nine was re-read against the test and each still names what would be observed; `AC5`, `AC6` and `AC8` say *non-zero* rather than a value, which is decidable, and `## Notes` records that the value is `plan`'s. No criterion carries an unmeasurable adjective. `AC10`'s "in the same form as `add`, `list` and `review`" is settled by comparing against three entries that already exist in `README.md`, and it states its own content requirement — what happens when the number names no card — which is the same construction `WI-0001` AC5 and `WI-0003` AC4 passed on |
| R5 | pass | `[skill]` — `## Out of scope` names five things, including editing a card and undoing a deletion, both of which a reader could reasonably assume came with "delete a card" |
| R6 | **pass** (was fail) | `[auto]` — `Q-001` is `status: answered`; no question is open on this item, and none is open anywhere in the workspace |
| R7 | pass | `[auto]` — no `depends-on`; the three sibling items are all `done` |
| R8 | **pass** (was fail) | `[auto]` — this file now declares `status: recorded`, and it holds both rounds: round 1's question with the stakeholder's verbatim answer tagged `[human]`, and every `[assumed]` decision with the deferral it was taken under |
| R9 | pass | `[skill]` — one command, one code path, one section of `README.md`. Nothing here splits |
| R10 | pass | `[skill]` — the command takes no options and has no modes, so the combinations are the argument shapes, and `AC1`, `AC5`, `AC6`, `AC8` and `AC9` cover them. The two behaviours left unconstrained — number reuse and the specific exit code — are named in `## Notes` with `refine` recorded as who left them open, which is what R10 asks for |

All ten pass. **No override was sought and none was needed** — the three round-1 failures were
one missing answer, and the answer arrived.
