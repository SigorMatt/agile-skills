---
title: Money is pounds and pence, and is written with two decimal places
version: 2
status: current
updated: 2026-09-10T15:34:21Z
updated-by: answer-questions
updated-for: WI-0002
---

# ADR-0006 — Money is pounds and pence, and is written with two decimal places

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** answer-questions (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0002 adds the first commands that take an amount, and the stakeholder settled what may be
typed [src: WI-0002/Q-002]: option C, in their words — "Take a `£` if I type one and ignore it,
and refuse anything with more than two decimals rather than rounding it — same reason as the
overspend, I don't want the tool storing a number I didn't type. It's one currency, pounds and
pence, and that's not changing."

That settles the input. It leaves one thing the criteria cannot be written without, and it is not
a wording choice: **how a number appears when the tool prints it back**. WI-0002 now prints an
amount and a balance when a recording succeeds [src: WI-0002/Q-003] and a balance beside the name
on `envel list` [src: WI-0002/Q-001], so a criterion has to be able to say what the screen must
contain. "The balance is 340" is not checkable at a terminal until `340`, `340.0` and
`340.00` stop being three answers to the same question.

The question was not put back to the stakeholder. They have already said the tool deals in pounds
and pence and that it is not changing; how many digits that renders as is a consequence of their
sentence rather than a further decision about their money. This execution's journal entry walks the
four escalation conditions in `spec/question.md` §4 against it and records a verdict on the four.

## Options considered

- **A — print the shortest faithful form.** `340`, `12.5` and `12.50` print as typed, or as
  the arithmetic leaves them. Cost: it is the cheapest of the three to write. Risk: the same balance prints two ways on two
  days, columns do not line up, and a criterion about a printed number then has to admit several
  spellings — which is how a criterion stops being decidable.
- **B — always two decimal places**, on every amount and every balance the tool prints
  [src: envel/movements.py:68; WI-0002/Q-004]. Cost: a
  balance of 340 prints as `340.00`, which is two characters nobody asked for. Risk: none that
  is visible from here; it is what a bank statement and a receipt both do.
- **C — leave it to `plan`, as message wording was left.** Cost: none now. Risk: it is not
  wording. WI-0002's criteria have to name a substring to look for before `plan` runs, so
  deferring it means writing criteria that cannot be checked, which is the state refinement just
  spent a round getting out of.

## Decision

Option B, in three rules.

1. An **amount** is a quantity of pounds and pence in the one currency the person budgets in
   [src: WI-0002/Q-002]. This product has a second currency nowhere in it, and the store holds
   amounts without a currency label [src: WI-0002].
2. On **input**, a single leading `£` is accepted and ignored, so `£12.50` and `12.50` are the
   same amount; an amount with more than two decimal places is refused rather than rounded, and
   the refusal takes the shape this item's other refusals take — non-zero exit, a line on
   stderr, and a store left as it was [src: WI-0002/Q-002].
3. On **output**, every amount and every balance the tool prints is written with exactly two
   decimal places. A balance of 340 prints `340.00`; a spend of `12.5` prints `12.50`.

Rule 3 is what makes WI-0002's criteria decidable, and they are written against it: they name the
substring the screen must contain.

## Consequences

- WI-0002's criteria may say "contains `340.00`" and mean one thing. Without rule 3 the most they
  could say is "contains a rendering of 340", which `verify` would have to interpret.
- WI-0003's monthly summary, WI-0004's transfer and WI-0005's correction print money too, and rule
  3 binds them. That is the point of putting it in an ADR rather than in one item's plan.
- **What this does not decide** is how an amount is held in the store or in memory. Decimal
  arithmetic, integer pence and anything else are open, and `plan` owns the choice for WI-0002
  [src: WI-0002]. Rule 2 does constrain it: an implementation that parses `12.345` and rounds is
  refused whatever it stores, and one that cannot tell `12.345` from `12.35` cannot satisfy it.
- **Reversing rule 3 is cheap and stays cheap.** It is one formatting function and the criteria
  that name its output; nothing is persisted in the printed form. Reversing rule 2 is cheap for
  the `£` and expensive for the decimals, because a store that has accepted rounded amounts
  cannot afterwards say which of its numbers the person actually typed — which is the reason the
  stakeholder gave for refusing them.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-09-10T15:34:21Z | answer-questions | WI-0002 | A `provenance` correction: option B's assertion in `## Options considered` now cites the function that implements it. Nothing decided changed |
| 1 | 2026-09-10T14:57:17Z | answer-questions | WI-0002 | First version: amounts are pounds and pence, a leading `£` is accepted and ignored, more than two decimal places is refused rather than rounded, and every printed amount and balance carries exactly two decimal places |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-10T15:34:21Z | answer-questions | WI-0002 | provenance | `## Options considered`, option B: *"always two decimal places, on every amount and every balance the tool prints"* now cites [src: envel/movements.py:68] — `format_amount`, which is the single function every printed figure passes through — and [src: WI-0002/Q-004], which asked whether the sentence owed a citation. The assertion is unchanged, and no code would have to change to satisfy the new text. Written because the sentence was an absolute over a family with no source on it, which is the shape `spec/doc-header.md` §4a exists for and which `claims-are-sourced` refused on `WI-0002`'s branch |
