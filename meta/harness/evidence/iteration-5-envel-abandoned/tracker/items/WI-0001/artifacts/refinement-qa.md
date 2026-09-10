---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`, set by `refine` in round 2. Round 1's two questions were put to the
stakeholder, they answered both, and their words are below verbatim, marked `[human]`. Round 2
asked them nothing and explains below why not. This file is now what was actually said, plus the
decisions taken without them and on what authority, which is what Definition of Ready R8 asks for.

The round-1 answers were propagated into `../item.md` by `answer-questions` when they were
consumed — AC5 amended, AC7 to AC10 added — and into `WI-0002`'s AC4; see each question's
`## Consequences`. Round 2's changes are recorded here and in the item's journal.

## Round 1 — the agenda put to the stakeholder

Two questions were filed, both blocking, both addressed to the human. They are the two gaps in
this item that are genuinely theirs rather than ours.

**Q1 — what do you want to type to run this tool?** (`WI-0001/Q-001`)

> `envel` is fine — keep it. It's short and I'll be typing it several times a day; I'm not going
> to spend a round renaming things.

`[human]` — option A. Answered 2026-09-10T13:32:40Z.

Asked because every acceptance criterion on this item names a command, and the name in them —
`envel` — came from `project.name` in `tracker/project.yaml`, which the project directory was
created with. The stakeholder never said it. It also propagates to WI-0002 and WI-0003.

**Q2 — when are two envelope names the same envelope, and what may a name contain?**
(`WI-0001/Q-002`)

> B. `Groceries` and `groceries` are the same pot and I'd rather be told it already exists than
> end up with two. I want spaces — "eating out" is one of mine — so don't restrict the characters.

`[human]` — option B. Answered 2026-09-10T13:32:40Z. Three separate things are settled by it, and
each has its own criterion so that none can be lost: names match ignoring case (AC5), the
capitalisation you created an envelope with is what you get back (AC7), and spaces are allowed
while an empty or all-whitespace name is refused (AC8, AC9, AC10). The last of those — refusing an
empty name — was in the question's option B and was not separately confirmed; it is the one part
of this answer taken from the option text rather than from their sentence, and it is recorded here
so a reader can see the seam.

Asked because envelopes are identified by name and nothing else, so the comparison rule decides
whether a capitalisation slip silently creates a second envelope and puts spending in the wrong
place. AC5 turned on it, and the criterion for a rejected name was deliberately unwritten until it
was answered — AC9 and AC10 are that criterion, split in two because an empty name and a name of
spaces are different inputs and a single criterion covering both is checked twice or not at all.

## Decided without the stakeholder, and on what authority

### A1 — the listing order

**`envel list` prints its lines sorted by name, ascending, byte-wise** (AC4). `[assumed]`

Nothing licensed this, in round 1 or in round 2. There is no standing delegation anywhere in this
engagement — no answer of the stakeholder's says "whatever you think is best" about anything — so
no `**Under delegation:**` line can honestly be written here, and R12's other form applies: this
is an assumption taken under **no** licence, and a disagreement about it lands as a send-back to
`refine` on this item.

Round 2 considered putting it to them and did not. The test in the procedure is whether the answer
changes what the software is *for*, what it promises, or something irreversible; the order of a
list of names they typed is none of those, it is one line of code to change, and asking would have
halted the whole pipeline for a round. That is a judgement and it is recorded here so it can be
disagreed with.

It was taken because AC2, AC3 and AC5 are not decidable without it: with the order unstated,
"writes a line `a` and a line `b`" cannot be checked against a fixed output. The choice was forced
by the other criteria rather than by taste. If the stakeholder wants creation order, or
most-recently-used, that is a change to AC4 and it lands on this item as a send-back to `refine` —
not on `plan` and not on `implement`.

### A2 — refusing a duplicate name

**Creating an envelope whose name already exists is refused, non-zero, with a message on stderr**
(AC5). Round 1: `[assumed]`. **Round 2: `[human]`.**

Round 1 took this under no licence, because the only other option — silently doing nothing — makes
a typo indistinguishable from success, which is the class of failure this whole tool exists to
prevent.

It is no longer an assumption. Answering `WI-0001/Q-002` the stakeholder wrote, unprompted about
this half of it:

> I'd rather be told it already exists than end up with two.

That is AC5's behaviour in their own words. The tag is upgraded to `[human]` and the item's
`## Notes` records the upgrade rather than quietly dropping the old entry, so a reader can see that
the pipeline guessed and was later told it had guessed right — which is a different fact from
having been told in the first place.

### A3 — surrounding whitespace on a name

**A name is compared and stored with leading and trailing whitespace removed** (AC11).
`[assumed]`, new in round 2.

Nothing licensed this. No `**Under delegation:**` line can be written, for the same reason as A1:
there is no standing delegation in this engagement.

It was taken because `WI-0001/Q-002` settles that `Groceries` and `groceries` are one envelope and
says nothing about `  groceries  `, and leaving it unstated would hand the decision to `implement`
where nobody would see it. The direction follows the principle the stakeholder did state — being
told an envelope already exists beats ending up with two — applied to a difference they did not
mention. That extension is ours, not theirs.

Written as a criterion rather than as a note precisely so the guess is visible: if they want
`  groceries  ` to be a second envelope, that is a change to AC11 and lands as a send-back to
`refine`.

## Round 2 — no question was put to the stakeholder, and why

Round 2 ran after their round-1 answers had been consumed. It asked them nothing. Applying the
procedure's test to each remaining gap:

- **The listing order (A1)** — considered and not asked. See A1 above for the reasoning and for
  the fact that it stays an unlicensed assumption.
- **Whitespace around a name (A3)** — not asked. It is the same shape as A1: reversible, invisible
  until it bites, and derivable from a principle they already stated. Recorded as an assumption
  and written into AC11 so it is visible.
- **Where the store lives (routed to `plan`)** — the answer would be the same whoever the
  stakeholder was, so it is a design decision. It is in the item's `## Notes`, and round 2 added
  the part that matters: AC6, AC9 and AC10 all begin "before any envelope has ever been created",
  and none of them is observable unless the store's location can be reached from a test without
  destroying a real one.
- **A name that would break the store's format (routed to `plan`)** — they forbade restricting the
  characters, so the constraint falls on the format, not on the name. No criterion, because there
  is no observable behaviour to state.
- **Message wording (routed to `plan`)** — the criteria fix the stream, the exit status and, where
  it matters, that `groceries` appears. The sentence is not ours to fix here.

Filing a question in order to have filed one would have halted the pipeline for a round and bought
nothing. Two things they *would* care about — A1 and A3 — are recorded above as unlicensed
assumptions with a named landing place, which is the honest alternative to asking.

## Round 2 — what changed in the criteria

- **AC6** now fixes exit 0, at least one line on stdout and nothing on stderr, and names its own
  stdout as the reference output AC9 and AC10 compare against. It previously said the output
  "contains no envelope name", which on an empty store is vacuous and gave AC9 and AC10 nothing to
  check.
- **AC9 and AC10** now compare `envel list`'s stdout byte-for-byte against that reference, instead
  of saying they "behave as AC6 requires". A criterion whose subject is another criterion has to
  name what is read; these now name a comparison anyone can run (`spec/dor-dod.md`, R4).
- **AC11** is new: see A3.
- Nothing was renumbered. AC11 was appended, and AC6, AC9 and AC10 were rewritten in place, so
  every existing reference to a criterion of this item still points where it did.

## Cross-answer check

**Round 1, as filed.** Checked against: none. No question anywhere in this workspace had an answer
yet — the five on EP-001 and the two filed here were all open, and `## Answer` was empty in every
one. There was therefore no prior human answer for these criteria to contradict.

**Round 1, as consumed** (`answer-questions`, 2026-09-10). The answers have now landed and the
check was redone, as that paragraph said it would be. Each question carries its own
`## Cross-answer check`; in summary, `WI-0001/Q-001` and `WI-0001/Q-002` were checked against
`EP-001/Q-001`…`EP-001/Q-005` and against each other, and every verdict was **compatible**. No
conflict was declared, so no question was put back to the stakeholder.

**Round 2** (`refine`). No new answer was received, so there was nothing new to check. What round 2
did check is the standing assumptions against the answers that had since landed, which is the same
obligation pointing backwards:

- A2 was checked against `WI-0001/Q-002` and found to be **confirmed** by it, in the stakeholder's
  own words, and its tag was upgraded from `[assumed]` to `[human]`.
- A1 was checked against all six recorded human answers and none of them touches listing order.
  `EP-001/Q-005` — the elicitation — was their opportunity to raise it unprompted; they raised
  three other things instead and said nothing about the order. **That is not agreement and is not
  recorded as any**: A1 remains an assumption taken under no licence.
- A3 was checked against `WI-0001/Q-002`, which is the answer it extends. It is compatible with it
  and is not licensed by it, and both halves of that are recorded above.

No conflict was found, so no question was put back to the stakeholder.
