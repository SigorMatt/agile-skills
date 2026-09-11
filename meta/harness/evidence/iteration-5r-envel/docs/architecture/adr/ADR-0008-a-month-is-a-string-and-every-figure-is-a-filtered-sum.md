---
title: A month is the YYYY-MM prefix of an entry's own date, and every figure in a summary is a filtered sum
version: 3
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0008 — A month is the `YYYY-MM` prefix of an entry's own date, and every figure in a summary is a filtered sum

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

`WI-0003` asks for four figures per envelope per month — what went in, what was spent, the net
moved, and what is left at the end of the month — and for those four to **reconcile**:
*"I won't use a report whose rows don't add up"* [src: WI-0003/Q-001], written as the identity
carried-in + in − spent + moved = left [src: WI-0003 AC3 "money in, minus money spent, plus money
moved, equals the change in that envelope's amount across the month"].

Three facts already in the record decide most of the shape, and this ADR is mostly about not
re-deciding them:

- an envelope's balance is *"the sum of `cents` over the entries naming it"* [src: ADR-0002], with
  no branch on kind;
- a spend and a move each carry `on`, the day the money moved, and income carries no date of its
  own, so income is held against `at` [src: ADR-0006] [src: ADR-0007]. `ADR-0006` already
  predicts this item's behaviour in as many words: *"`WI-0003` sums a month's spending by `on`, a
  month's moves by `on` [src: ADR-0007], and a month's income by `at`, with no branch on what a
  date means"*;
- what is left in a row is the envelope's own balance and carries over from the previous month
  [src: WI-0003 AC3 "The amount left in a row is the envelope's own balance, which carries over
  from the previous month rather than starting at zero"].

What is **not** decided anywhere is how the code knows which month an entry belongs to, and
whether anything is stored to make a month's figures cheap. `refine` routed both here rather than
to the stakeholder, because the answer would be the same whoever they were
[src: tracker/items/WI-0003/artifacts/refinement-qa.md].

## Options considered

- **A — branch on `kind`.** A table in the summary: `income` is dated by `at`, `spend` by `on`,
  `move` by `on`. Cost: a table that has to be edited every time a kind is added, in a module
  that is not the one that adds it. Risk: it makes `ADR-0006`'s sentence *"with no branch on what
  a date means"* false the day it is written, and a kind added later without touching the table is
  dated by whichever branch the `else` falls through to — silently, and in a report nobody
  cross-checks.
- **B — `on` if the entry has one, otherwise `at`.** One expression, no mention of `kind`. Cost:
  nothing visible. Risk: a future kind that carries `on` but ought to be counted by `at` would be
  put in the wrong month. No such kind is contemplated — `on` was introduced precisely as *the day
  the money moved* [src: ADR-0006] — and a kind that wanted both meanings would be a new decision
  with its own ADR.
- **C — store a month on every entry when it is written.** Cost: a new field on every entry, so a
  `format` change and code that reads the old shape and writes the new one. Risk: two sources of
  truth for the same fact, and `ADR-0002`'s shape was chosen specifically so that a balance is
  derived rather than stored — *"a balance is the sum of an envelope's entries rather than a
  stored number"* [src: docs/architecture/overview.md].
- **D — hold a month as a `(year, month)` pair, or a `datetime.date` on the first of the month.**
  Cost: a conversion at every comparison and a second date type in a tool that has one. Risk: low,
  but it buys nothing: see the decision.

## Decision

Option **B**, with months carried as strings.

1. **The month an entry falls in is `entry["on"][:7]` when the entry has an `on`, and
   `entry["at"][:7]` otherwise.** One function, no branch on `kind`. This is `ADR-0006`'s sentence
   implemented rather than paraphrased: a spend and a move carry `on` [src: ADR-0006]
   [src: ADR-0007] and income does not, so the rule produces exactly the asymmetry the stakeholder
   chose at `WI-0003/Q-003` — *"I put income in when it arrives"* — without naming a kind.

2. **A month is the seven-character string `YYYY-MM`, and it is compared as a string.** Both date
   fields are zero-padded fixed-width ISO — `YYYY-MM-DD` [src: ADR-0006] and
   `YYYY-MM-DDTHH:MM:SSZ` [src: ADR-0002] — so their first seven characters are a month in the
   same form, and lexicographic order over that form **is** chronological order. *Earlier than*,
   *in*, and *later than* are therefore `<`, `==` and `>`, with no calendar arithmetic anywhere in
   the summary and no third date type in a tool that already has two.

3. **Every figure is a filtered sum over the entries naming the envelope** [src: ADR-0002], in
   the shape `ADR-0002` already gives `balance` [src: envel/envelopes.py:63]:

   | figure | the filter | the sum |
   |--------|-----------|---------|
   | in | `kind == "income"` and month == M | `cents` |
   | spent | `kind == "spend"` and month == M | `-cents`, so the column prints positive |
   | moved | `kind == "move"` and month == M | `cents`, signed, positive when more arrived |
   | left | month <= M | `cents` |

   The columns are per kind because AC2 names them per kind
   [src: WI-0003 AC2 "each row shows four figures for that"]; what carries no branch on kind is
   *which month an entry falls in*, which is the part `ADR-0006` speaks about [src: ADR-0006].

4. **Nothing is precomputed and nothing new is stored** [src: ADR-0002]. A month's figures are
   computed from the entry log on every run, as a balance already is [src: envel/envelopes.py:63]. The document's `format` stays `1` and there is
   no migration, which is the property `ADR-0002` was shaped to have.

5. **An entry naming an envelope that is not in `envelopes` contributes to no row**, because the
   summary iterates the envelopes and asks for each one's entries. This is the same answer
   `WI-0002`'s plan gave to the same question — *"an entry naming an absent envelope is invisible,
   and this item adds no check"* [src: tracker/items/WI-0002/artifacts/plan.md] — and the situation
   cannot arise today, because no command removes an envelope.

## Consequences

**Easy: the reconciliation of AC3 is a property of the arithmetic rather than something the code
arranges** [src: WI-0003 AC3 "The figures reconcile, and reconciling is the whole point"]. Every
entry has exactly one month and exactly one kind, so the three
month-M columns partition the entries of month M; `left` is the sum over months <= M; and
`left − (in − spent + moved)` is therefore the sum over months < M, which is the carried-in
balance by definition. Nothing **derives** the carried-in figure from the other three and nothing
checks the identity — there is no arrangement that could drift out of true. `WI-0006` later put a
carried-in figure on the screen [src: WI-0006 AC9 "the listing opens with a line giving what that
envelope held"] and did it the same way: `summary.balance_before` is this table's `left` filter
with `<= M` replaced by `< M` [src: envel/summary.py], so it is a filtered sum like every other
figure here and no subtraction stands between the two numbers.

**Easy: a month that has ended reads the same for ever** [src: WI-0003 AC7 "August's report should
say the same thing in November as it did in September"], because every input to it is an entry
that already exists and a filter that does not mention today.

**Hard: the reconciliation holds only while every entry's kind is one of the three that have a
column.** A fourth kind — the `kind` field exists so that there can be one [src: ADR-0002] —
would be counted in `left` and in none of the other three, and AC3's identity would silently stop
holding. Whoever adds a fourth kind owes this ADR a fourth column or an explicit exclusion; it is
written here rather than left to be discovered from a report that does not add up.

**Hard: income's month is a UTC month and a spend's is a local one.** `at` is a UTC timestamp and
`on` is the machine's local calendar day [src: ADR-0006], so income typed late in the evening of
the last day of a month, well east or west of UTC, can fall in the next month while a spend typed
beside it does not. `ADR-0006` records this as correct rather than as a defect — *"the person's
calendar is the local one… the two fields are not convertible into each other and no code should
try"* — and this ADR does not try. It is a consequence of an existing decision, surfaced here
because this is the first item that reads both fields in one calculation.

**Reversibility: easy.** All of it is one function and one filter table in one module, over stored
data this decision does not change. Moving to option A is editing one expression; moving to option
C is the only expensive direction, and it is expensive because of `format`, not because of this.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | One `provenance` correction, recorded below: two citations in `## Decision` 3 and `## Decision` 4, both for the shape of `balance`, moved from `envel/envelopes.py:50` to `envel/envelopes.py:63`. Neither assertion is changed and no code has to change to satisfy the new text. Answering `EP-001/Q-007`. |
| 2 | 2026-09-11T08:22:40Z | implement | WI-0006 | One erratum, recorded below: *"Nothing computes the carried-in figure"* stopped being true when `WI-0006` printed one [src: WI-0006 AC9 "the listing opens with a line giving what that envelope held"]. The claim that mattered — that no code derives it by subtraction — is true and is now what the sentence says, with the function that computes it named. The decision, its five numbered items and the filter table are unchanged, and no code has to change to satisfy the new text. |
| 1 | 2026-09-11T06:20:16Z | plan | WI-0003 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T18:55:51Z | answer-questions | EP-001 | provenance | `## Decision` 3, *"in the shape `ADR-0002` already gives `balance`"*, and `## Decision` 4, *"computed from the entry log on every run, as a balance already is"*, both cited `[src: envel/envelopes.py:50]`. That was `def balance(store, name):` when this ADR was written; `WI-0006` inserted `take_ref` above it for `ADR-0010` [src: ADR-0010], so line 50 became `store["next-ref"] = reference + 1`. Both citations now read `[src: envel/envelopes.py:63]` [src: envel/envelopes.py:63]. The assertions are unchanged. Answering `EP-001/Q-007`. |
| 2026-09-11T08:22:40Z | implement | WI-0006 | erratum | `## Consequences`, first paragraph, said *"Nothing computes the carried-in figure and nothing checks the identity"*. The first half is now false: `summary.balance_before` computes exactly that figure, because `WI-0006` AC9 prints it [src: WI-0006 AC9 "the listing opens with a line giving what that envelope held"]. What the sentence was defending is that no code *derives* it from the other three figures, and that is still true — `balance_before` is this ADR's own `left` filter with the bound moved back one month [src: envel/summary.py], which is a filtered sum like every other figure here. Replaced with a clause saying *derives* rather than *computes* and naming the function. |
