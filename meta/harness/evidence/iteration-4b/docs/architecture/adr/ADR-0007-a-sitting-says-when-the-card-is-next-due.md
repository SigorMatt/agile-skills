---
title: A sitting says when each card is next due, and nothing else shows the schedule
version: 1
status: current
updated: 2026-08-30T03:38:18Z
updated-by: answer-questions
updated-for: WI-0003
---

# ADR-0007 — A sitting says when each card is next due, and nothing else shows the schedule

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** the stakeholder, answering `WI-0003/Q-002`; recorded by answer-questions
  (architect), for WI-0003
- **Supersedes:** — (extends `ADR-0001`, which fixes the interface and the subcommands, and
  `ADR-0002`, which fixes the arithmetic this decision makes visible; nothing in either is
  reversed [src: ADR-0001; ADR-0002])

## Context

`ADR-0002` fixes what an answer does to a card's next-review date. Nothing fixed whether the
person is ever told. As the tool stands, a sitting prints the question, waits, prints the answer,
asks `y` or `n` and moves straight to the next card [src: recall/cli.py:140], and
`recall list` prints `question | answer` and nothing else [src: recall/cli.py:119]. So
once WI-0003 lands, the scheduling would be real and entirely imperceptible: the only way to see
it would be to open `~/.local/share/recall/deck.json`.

That mattered enough to be the stakeholder's decision rather than ours, for two reasons recorded
in the question. The scheduling *is* the product — "it decides when I next see this" is the thing
being built — and nothing would ever confirm to the person that it happened. And WI-0003 AC4,
written at intake, requires the new date to be applied so that it is *"visible without any
further run or command"*, while nobody had ever decided what **visible** means
[src: tracker/items/WI-0003/item.md AC4].

Two things bounded the answer and were not reopened: *"nothing fancier than that"*
[src: EP-001/Q-001], and the epic's exclusion of statistics, streaks and dashboards
[src: docs/product/vision.md]. So the widest option on the table was one extra line per card.

## Options considered

The three the question put to the stakeholder [src: WI-0003/Q-002].

- **A — say nothing.** The sitting stays as it is. Cost: none; the sitting stays as terse as it
  is now. Risk: the scheduling is invisible, a working ladder is indistinguishable from a broken
  one without opening the deck file, and getting a card wrong feels exactly like getting it
  right.
- **B — one line after each answer**, naming when the card is next due. Cost: one line of output
  per card, and one date to format; it adds nothing to how long a sitting takes. Risk: a
  twenty-five card sitting gains twenty-five lines, against a stakeholder who wants a sitting to
  be quick. **Chosen.**
- **C — a silent sitting, and the date added to `recall list`.** Cost: the most of the three, and
  it changes behaviour already delivered and signed off under WI-0001. Risk: the feedback arrives
  when the person is no longer thinking about the card, though it answers "what is coming up this
  week" in a way B does not.

The stakeholder chose B: *"Option B — show the next date after each answer. I want to actually
see it's working, and one line isn't going to slow me down."* [src: WI-0003/Q-002]. Their second
clause is the reconciliation with *"a review session that drags on more than a couple minutes"*
[src: EP-001/Q-001], made by them rather than by us.

## Decision

1. **After each graded card, a sitting prints one line saying when that card is next due.** It is
   printed for every graded card, right and wrong alike — seeing that a wrong answer costs the
   progress on that card is half of what the stakeholder asked for.
2. **The line carries the next-review date**, the date `ADR-0002` §4–§6 just computed and stored
   for that card. How it is phrased — whether it also says the gap in days, and in what
   words — is `plan`'s, under `ADR-0001` §5: this ADR fixes that the fact is shown and which fact
   it is, not the sentence.
3. **One line, not more.** No tally, no summary at the end of a sitting, no per-card history. The
   epic excludes statistics [src: docs/product/vision.md] and the stakeholder's *"nothing fancier
   than that"* stands [src: EP-001/Q-001].
4. **`recall list` is unchanged**, and keeps printing `question | answer`. Option C was the
   option that would have changed it and it was not chosen; delivered WI-0001 behaviour therefore
   stays as it is.
5. **This is what WI-0003 AC4's word *visible* means.** The date is visible because the sitting
   says it, at the moment the answer is recorded — not because the deck file can be opened.

## Consequences

- WI-0003 AC4 becomes decidable from a terminal: a sitting's output names the date, so a verifier
  reads it back without inspecting `deck.json`. `refine` writes that into the criterion.
- The arithmetic in `ADR-0002` becomes checkable by the person using the tool rather than only by
  a test. The worked example in WI-0003 AC3 — days 0, 1, 4, 11, 41, 71, 101 — is something they
  can watch happen.
- A sitting gets one line longer per card. On the largest pile the stakeholder described — a week
  away, no cap on the sitting [src: WI-0002/Q-001] — that is the only cost, and they accepted it
  in the same sentence in which they chose it.
- `docs/process/using-recall.md` will have to describe the line when WI-0003 is implemented; its
  current "What this version does not do yet" section is written on the premise that scheduling
  is unbuilt [src: docs/process/using-recall.md].
- Nothing new is stored. The date printed is the one already written to the card
  [src: ADR-0002], so this adds no field and no format change [src: ADR-0004; ADR-0006].
- **Reversibility: high.** Removing the line is deleting one `print`; adding the date to
  `recall list` later (option C) is not made harder by this and does not require undoing it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T03:38:18Z | answer-questions | WI-0003 | First version, recording the stakeholder's answer to `WI-0003/Q-002`: a sitting names each card's next-review date, `recall list` is unchanged, and that is what AC4's "visible" means |
