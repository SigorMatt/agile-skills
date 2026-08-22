# Refinement Q&A — WI-0002

Every question put to the person who stated the idea, and every answer, in order and verbatim.
Answers are tagged `[human]` when they said it, `[assumed]` when `refine` proposed it and it was
not contradicted, and `[unresolved]` when it was asked and not settled.

The stakeholder answers **asynchronously, in the question files**, and is not present in the
session that refines an item. Round 1 below was filed by `intake` as `questions/Q-001.md` and
`Q-002.md`, suspended this item at `awaiting-answer`, and was answered and propagated by
`answer-questions` into `ADR-0002` and `ADR-0003` before this refinement ran. It is reproduced
here in full because this file, not the question directory, is what `verify` and `review-close`
are pointed at.

---

## Round 1 — filed 2026-08-21T18:46:03Z by `intake`, answered before 2026-08-21T19:01:10Z

### Q1 (`Q-001`) — Is a shared expense always split equally?

> **Asked because:** the idea says "shared by some or all" and nothing about how. Options offered:
> **A** equal split only; **B** every sharer carries an explicit amount as soon as any of them
> does, and the amounts must sum to the total; **C** neither, ask later.

**Answer** `[human]`:

> Usually equal, but sometimes someone only had part of it and wants to put in a different amount
> — so it needs to handle both.

**Recorded as** `[human]` for the requirement, `[assumed]` for the shape. The requirement rules
out option A outright. It does not by itself pick option B, and `answer-questions` decided against
B for a reason worth keeping visible: B would force the user to compute everyone else's share by
hand the moment one person's differs, which is the arithmetic the tool exists to do. **ADR-0002**
records the mixed form instead — any subset of sharers may carry a stated share, and the
remainder is split equally among the rest. AC5, AC6 and AC10 on this item are that decision.

### Q2 (`Q-002`) — When a split does not come out evenly, who carries the odd penny?

> **Asked because:** three people sharing 10.00 owe 3.333… each, and WI-0003 AC4 promises that
> paying the printed amounts leaves everybody at zero — which is either true by construction or
> false by a penny. Options offered: **A** the payer takes the remainder; **B** spread over the
> sharers in a fixed order; **C** keep exact fractions and round only when printing.

**Answer** `[human]`:

> Not sure yet — go ahead anyway, we'll decide later.

**Recorded as** `[human]` — it is an instruction to proceed, not a refusal, and "we'll decide
later" is a constraint on *how* it is decided rather than a deferral of the decision. **ADR-0003**
is the result: whole minor units, at most two decimal places on entry, the odd pennies to the
payer first — and, the part that answers "later", **shares are derived on every run and never
stored**, so changing the rule later changes one function and no recorded data. AC7 is that rule,
worked through three examples.

---

## Round 2 — decided by `refine`, not put to the human

Everything below is syntax and wording. The human has twice declined to be asked about exactly
this kind of detail — `WI-0001/Q-001` and `WI-0001/Q-003`, both answered "whatever you think is
best" — so filing a third question on the same subject would stop the pipeline for a round trip
and, on that evidence, return nothing. Each answer is `[assumed]`: proposed by `refine`, **not**
confirmed by the human, and carried in `## Notes` so that `plan`, `implement` and `verify` inherit
them as assumptions rather than as requirements.

### Q3 — What is the exact argument syntax of `add-expense`?

**Answer** `[assumed]`:

```
python3 -m expenses add-expense <total> --paid-by <name> --shared-by <name>[=<amount>][,...]
```

The total is positional because it is the one argument every expense has and the one the user is
looking at when they reach for the tool; `--paid-by` and `--shared-by` are named because two bare
names in a row would be ambiguous. The `,` and `=` forms are not a free choice — `ADR-0005`
point 2 reserves exactly those two characters in a name, and it reserves them *because*
`ADR-0002` needs a list of sharers with an optional amount each on one line.

**Rejected: making `--shared-by` optional, defaulting to everybody in the group.** The idea's own
words ("shared by some or all") would have supported it and it would save typing on the commonest
case. It is rejected because a default that silently includes a person is a mistake this epic
cannot repair: there is no command to edit or delete an expense, and no command to remove a
person. The cost of the rejection is real — every expense names every sharer — and it is the kind
of thing the human might well overturn.

### Q4 — Are both flags required, and may either be repeated?

**Answer** `[assumed]`: both required, each at most once. A repeated `--paid-by` is refused rather
than last-one-wins, because silently discarding one of two names the user typed is how an expense
ends up against the wrong payer.

### Q5 — What exactly does each message say, and what does a listed expense look like?

**Answer** `[assumed]`: exact text, as in the criteria. "A stated message" is not decidable — two
verifiers could disagree about whether some output counts. A listed expense is

```
1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00
```

one line per expense, numbered from 1 in the order recorded, every amount with two decimal places
(`ADR-0003` point 2), every person with the spelling first entered for them (`ADR-0005` point 4).
The numbers are display only: nothing accepts an expense number as an argument, because nothing
edits or deletes an expense.

### Q6 — May the same person be named twice in `--shared-by`?

**Answer** `[assumed]`: no — refused, and "the same person" means the identity key, so
`Alice,alice` is refused too. The two alternatives both answer an arithmetic question nobody
asked: merging the entries decides that a person named twice owes one share, and allowing it
decides they owe two. A refusal is the only option that cannot be quietly wrong, and it costs the
user one retype.

### Q7 — Can an expense say what it was for?

**Answer** — **not assumed; answered from the record.** `docs/product/prd.md` (v2) § *The facts
the tool holds* enumerates an expense as "An amount, the one person who paid it, and one or more
sharers", and item 4 of the same list says "Nothing else. No dates chosen by the user, no
categories, no attachments". So there is no description field, and this refinement did not invent
one or ask again.

It is written into `## Out of scope` rather than left silent, because it is the single thing a
reader is most likely to assume is here: without it, `expenses` output distinguishes two dinners
only by their number, amount and people. If the group finds that unusable, the place to change it
is the PRD and a new item — not this one.

### Q8 — What happens when a write fails?

**Answer** `[unresolved]`, deliberately, and recorded in `## Notes` as a decision `plan` owes
rather than a criterion. WI-0001's review closed with exactly this as an accepted gap and named
this item's `plan` execution as where to settle it, because `storage.save` is inherited unchanged
from WI-0001. Turning it into an acceptance criterion here would be `refine` deciding an
architecture question in the item's name.

---

## Definition of Ready — where each criterion stands

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic`, `priority` set; `depends-on: WI-0001`, which is `done` |
| R2 | pass | `## Story` names the role, the capability and the "so that" |
| R3 | pass | AC1–AC14, each a labelled checkbox |
| R4 | pass | every criterion names a command line and the exact output that settles it; the syntax pinned in Q3 to Q5 is what removed the last of the vagueness |
| R5 | pass | `## Out of scope` names five things, of which "what an expense was for" is the one a reader would most reasonably assume is included, with the document that excludes it cited |
| R6 | pass | both questions on this item are `answered`; no open question remains |
| R7 | pass | `depends-on: WI-0001` is `done` and merged |
| R8 | pass | this file |
| R9 | pass | one coherent change: record an expense, derive its shares, list them back. The write side and the read side are unobservable without each other |
| R10 | pass | the two subcommands' cases are all stated — equal split (AC5), mixed (AC6), uneven (AC7), unknown person (AC8), bad amounts (AC9), impossible stated shares (AC10), malformed list (AC11), malformed command line (AC12), nothing recorded on refusal (AC13), no interference with WI-0001's data (AC14) — and the three things left open are named in `## Notes` with who left them so |

No override was needed or taken.
