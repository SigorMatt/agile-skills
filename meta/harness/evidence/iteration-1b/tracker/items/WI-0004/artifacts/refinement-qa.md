# Refinement Q&A — WI-0004

`[human]` means they said it; `[assumed]` means `refine` proposed it and it was not contradicted;
`[unresolved]` means asked and not settled.

**No question was ever filed on this item.** It has none in `questions/`, and that is not an
omission: the item exists *because of* an answer the human gave on the epic, and everything else
it needed was already decided in ADRs written for its three siblings. This file therefore opens
with the exchange that created it, quoted from where it happened.

---

## Round 0 — the answer that created this item

Filed by `intake` as `EP-001/Q-001`, answered before 2026-08-21T18:51:11Z.

### Q0 (`EP-001/Q-001`) — Is settling up part of the product?

> **Asked because:** every verb in the stated idea is about recording what was spent and deriving
> the consequence; nothing said what happens when somebody hands over the money. Options offered:
> **A** out of scope — "who owes whom" is a pure function of the expense list; **B** payments are
> a fourth kind of fact, recorded and netted off; **C** a "settle everybody" reset.

**Answer** `[human]`:

> Being able to mark that someone's paid up matters. Otherwise the numbers just keep racking up
> forever and stop meaning anything.

**Recorded as** `[human]`. That is option B, and it created this item — `answer-questions`
propagated the scope change into `vision.md` (v2) and ran `intake`'s creation procedure. The
second sentence is the one that decides two things in this refinement: **overpayment is accepted**
(Q4 below) and **there is no reset** (`## Out of scope`), because both follow from "record what
actually happened" rather than "adjust the numbers until they look right".

---

## Round 1 — decided by `refine`, not put to the human

Syntax and wording. The human has twice answered this class of question with "whatever you think
is best" (`WI-0001/Q-001` and `Q-003`), so a third would stop the pipeline for a round trip and,
on that evidence, return nothing. Each is `[assumed]`: proposed here, **not** confirmed, and
carried in `## Notes`.

### Q1 — What is the argument syntax of `add-payment`?

**Answer** `[assumed]`: `add-payment <amount> --from <name> --to <name>`. The positional amount
mirrors `add-expense`, which is the only other recording command that takes one. `--from` and
`--to` rather than `--paid-by` and `--paid-to`: a payment has a direction, and those are the two
words for it. Rejected `add-payment <from> <to> <amount>` — three bare positionals in a fixed
order is exactly the shape that gets typed wrong, and money is the thing not to get wrong.

### Q2 — What does a listed payment look like?

**Answer** `[assumed]`: `1. Bob paid Alice 10.00` — numbered from 1 in the order recorded, like
`expenses`. **Past tense**, where `who-owes-whom` says `Bob pays Alice 10.00`: one records what
happened, the other proposes what to do, and a reader looking at both should be able to tell them
apart at a glance.

### Q3 — Is a payment from somebody to themselves allowed?

**Answer** `[assumed]`: refused, with `A payment must be between two different people.`, and
sameness is the identity key so `--from ALICE --to Alice` is refused too. It changes no net
position, so accepting it would put a line in `payments` that no arithmetic can see — a fact the
tool holds and never uses. It is almost certainly a typo for a real payment.

### Q4 — Is an overpayment allowed? Bob owes 10 and pays 30.

**Answer** `[assumed]` — and this is the one closest to being a question for the human. It is not
asked because their answer to `EP-001/Q-001` already contains the principle: the tool exists to
record the payments the group actually made, so that the numbers keep meaning something. Refusing
an overpayment would be the tool declining to record something that happened, and the group would
have no way to express it.

So it is accepted, and `who-owes-whom` reverses the direction: after Bob overpays, the group owes
Bob. AC8 pins that with the exact output. If the human wants a warning instead, that is a
one-criterion change and this paragraph is where they should look.

### Q5 — Are the amount rules the same as an expense's?

**Answer** — **not assumed; answered from the record.** `ADR-0003` points 1 and 2 fix amounts for
the whole tool: whole minor units, at most two decimal places on entry, exactly two on display.
The only thing this item adds is the message when the amount is zero or negative
(`A payment must be for more than zero.`), which is the payment-shaped wording of the rule
`ADR-0002` already applies to an expense total.

---

## Round 2 — three things handed to this item by two earlier reviews

These were not questions. WI-0002's and WI-0003's reviews closed with gaps recorded in their
items' `## Notes`, each naming **this item** as where to address them. All three are dealt with,
and two of them deliberately **not** as acceptance criteria:

| inherited from | what it is | how it is pinned here |
|----------------|------------|----------------------|
| WI-0002 `## Notes` 3 | "a refusal creates no record file" is pinned for `add-person` and not for `add-expense`; two mutations survived on WI-0002 because of it | **AC13's last clause** — a criterion, because it is observable: look for the file |
| WI-0003 `## Notes` 2 | `net_positions` returns everybody in the order they were added, and nothing asserts it | **an instruction to `plan`** in `## Notes`, not a criterion: the order is not observable through any command, so no criterion could be decidable |
| WI-0003 `## Notes` 3 | the purity test for `who-owes-whom` uses a one-expense record, so a reordering rewrite would pass it | **an instruction to `plan`** in `## Notes`, for the same reason |

Recording the last two as instructions rather than criteria is a deliberate choice and worth
naming: a criterion that cannot be decided by observation fails R4, and writing one anyway to look
thorough would be the exact failure the Definition of Ready exists to prevent. They are still
binding — `plan` reads `## Notes`, and `review-close` will see whether they were done.

---

## Definition of Ready — where each criterion stands

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic`, `priority` set; `depends-on: WI-0003`, which is `done` |
| R2 | pass | `## Story` names the role, the capability and the "so that" |
| R3 | pass | AC1–AC15, each a labelled checkbox |
| R4 | pass | every criterion names a command line and the exact output that settles it. The five criteria that assert a *changed* `who-owes-whom` (AC5, AC6, AC7, AC8, AC15) were each computed against the delivered settlement before being written down, so none of them asserts an output the tool cannot produce |
| R5 | pass | `## Out of scope` names six things, of which refusing an overpayment and correcting a mistaken payment are the two a reader would most reasonably assume are included |
| R6 | pass | no question has ever been open on this item |
| R7 | pass | `depends-on: WI-0003`, `done` and merged |
| R8 | pass | this file |
| R9 | pass | one coherent change: record a payment, list payments back, and let the existing settlement net them off. The write side and the effect on `who-owes-whom` are unobservable without each other |
| R10 | pass | every case the two subcommands introduce is stated — recorded (AC1), listed (AC3), empty (AC4), full payment (AC5), part payment (AC6), fully settled (AC7), overpayment (AC8), unknown person (AC9), self-payment (AC10), bad amounts (AC11), bad command line (AC12), nothing recorded on refusal (AC13), no damage to earlier data (AC14), a payment with no expense behind it (AC15) — and the two things left open are named in `## Notes` with `refine` recorded as who left them |

No override was needed or taken.
