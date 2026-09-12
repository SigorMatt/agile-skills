---
title: Product vision — droll
version: 4
status: current
updated: 2026-09-11T22:19:26Z
updated-by: answer-questions
updated-for: WI-0001
---

# Product vision — droll

## Who this is for

One person, at a terminal, who needs dice and does not have them — or has them and would rather
not do the arithmetic. The picture to hold is someone mid-game with a keyboard already in front of
them: they want a number now, they want to believe the number, and a minute later they want to
remember what it was.

The stated setting is the stakeholder and their gaming group on game night — *"nothing bigger
than that"* [src: EP-001/Q-003].

They are not a novice at the command line. They know what a dice expression looks like and will
type one without being prompted for each part of it. They are not administering anything, not
scripting against this, and not reading its output with another program.

## What it is for

droll is an interactive prompt: it is started once, it reads expressions one after another, and it
is quit when the person is done for the night. "A session" is one run of it [src: EP-001/Q-001].
Within a session it does three things, in this order:

1. **Turning a typed dice expression into a number.** `3d6+2` in, a total out, with no ceremony in
   between. An expression is one dice term with an optional integer modifier — `d20`, `3d6+2`,
   `4d8-2` — which is the shape of the two examples the stakeholder gave [src: ADR-0001].
2. **Showing the working.** The individual die results and the modifier are shown alongside the
   total, in plain text and in the same shape for a single `d20` as for `3d6+2`, so that a
   surprising number is believable rather than merely asserted [src: WI-0001/Q-001]. A total with
   nothing behind it is what a calculator already gives, and it is not enough.
3. **Remembering this session's rolls.** The rolls made so far can be listed back, in order, so
   that "what did I roll a minute ago?" has an answer.

The second and third are what make this worth building. Without them, what is left is a shorter
way to write `random.randint`, which is a calculator by another name and is not a product
[src: WI-0001/Q-001; EP-001].

## What it deliberately is not

- **Not a game system.** It knows about dice, not about characters, skills, saving throws, damage
  types or any published ruleset. An expression is arithmetic and nothing else.
- **Not a record keeper.** The history is for the session in front of you. Nothing is written to
  disk to be read back tomorrow, and the tool is not the place to keep a campaign log. Saving the
  history across sessions is a want for later and is outside this product [src: EP-001/Q-003].
- **Not shared.** One person, one terminal. No rolls are transmitted, published or witnessed by
  anyone else, which also means it is not a fair-play mechanism: it cannot prove to a suspicious
  table that a roll was not re-rolled.
- **Not a library.** It is a thing a person types at. Nothing here is designed as an interface for
  other programs to call.
- **Not a randomness product.** It uses what Python offers and makes no claim about statistical
  quality, reproducibility or seeding beyond that.

The exclusions above are intake's reading of what a reasonable person would otherwise assume was
included. None of them was stated by the stakeholder, and the elicitation question on the epic is
the place where any of them can be contradicted.

## Engagement state

- The stakeholder has stated the idea and has not yet been asked to accept anything.
- Three questions are open with them, all filed at intake: `EP-001/Q-001`, whether the tool is an
  interactive prompt or a one-shot shell command and therefore what "a session" is;
  `EP-001/Q-002`, how far the accepted expression syntax reaches beyond a single dice term with a
  modifier; and `EP-001/Q-003`, an open elicitation. The first two shape the product, and this
  document is written to describe it under either answer; when they are answered, the answers land
  in the work items and, where they constrain the build, in an architecture decision record.
- Two work items exist, both at `draft`; nothing has been refined, designed, built or delivered.
- Nothing in this document has been reviewed by the stakeholder.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-09-11T22:19:26Z | answer-questions | WI-0001 | Answering `WI-0001/Q-002`: `## What it is for`'s closing sentence now cites the stakeholder's own reason for wanting a breakdown, and is rephrased to say what it asserts without the bare quantifiers it used to carry — *"worth building at all"*, *"there is no product"* — which is `doc-header.md` §4a's own remedy for a sentence that reads as a universal it cannot enumerate. What it asserts is unchanged. The second unsourced claim `Q-002` reports, in `## Engagement state`, is deliberately **not** touched: that section belongs to the ending (ADR-0004) |
| 3 | 2026-09-11T21:44:56Z | answer-questions | WI-0001 | The stakeholder's answer to `WI-0001/Q-001` propagated: the breakdown is the individual dice and the modifier in plain text, in one shape for every roll |
| 2 | 2026-09-11T21:37:43Z | answer-questions | EP-001 | The stakeholder's answers to `EP-001/Q-001`, `Q-002` and `Q-003` propagated: droll is an interactive prompt and a session is one run of it; an expression is one dice term with an optional integer modifier; the audience and the not-now of cross-session saving recorded |
| 1 | 2026-09-11T21:27:39Z | intake | EP-001 | First version: who droll is for, what it is for, what it is not, and the initial engagement state |
