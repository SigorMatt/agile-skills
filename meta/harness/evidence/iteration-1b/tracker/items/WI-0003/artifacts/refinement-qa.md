# Refinement Q&A — WI-0003

Every question put to the person who stated the idea, and every answer, in order and verbatim.
`[human]` means they said it; `[assumed]` means `refine` proposed it and it was not contradicted;
`[unresolved]` means asked and not settled.

The stakeholder answers **asynchronously, in the question files**, and is not present in the
session that refines an item. Round 1 was filed by `intake` as `questions/Q-001.md`, suspended
this item, and was answered and propagated by `answer-questions` into `ADR-0004`, `prd.md` and
`vision.md` (v3) before this refinement ran. It is reproduced here because this file, not the
question directory, is what `verify` and `review-close` are pointed at.

---

## Round 1 — filed 2026-08-21T18:46:03Z by `intake`, answered before 2026-08-21T19:03:32Z

### Q1 (`Q-001`) — Should "who owes whom" net each pair, or print the fewest payments?

> **Asked because:** "show who owes whom" has two correct answers that print different things,
> and nothing in the record chose between them. Options offered: **A** netted pairwise debts,
> every line traceable to expenses those two people shared; **B** a settling set of transfers,
> fewest payments, possibly pairing people who never shared anything; **C** both, pairwise by
> default and minimised behind a flag. No recommendation was given — the question said explicitly
> that there was no basis in the record to choose.

**Answer** `[human]`:

> Just tell us the fewest payments needed to settle up — that's what actually happens at the end
> of a trip.

**Recorded as** `[human]`, and as **ADR-0004** with the human named as the decider, because it is
a statement of intent that no document could have supplied. Two things had to be pinned before
criteria could be written against it, and both are in the ADR: "fewest" promises less than it
sounds like — provable minimality is NP-hard, so what is promised is exact settlement, at most
`n - 1` transfers, and determinism — and a transfer may name two people who never shared an
expense. AC6 and AC8 on this item are those two facts made checkable.

---

## Round 2 — decided by `refine`, not put to the human

Output format and tie-breaking. The human has twice answered this class of question with
"whatever you think is best" (`WI-0001/Q-001` and `Q-003`), so filing a third would stop the
pipeline for a round trip and, on that evidence, return nothing. Each answer below is `[assumed]`:
proposed by `refine`, **not** confirmed, and carried in `## Notes` so `plan`, `implement` and
`verify` inherit them as assumptions.

### Q2 — What does a printed transfer look like?

**Answer** `[assumed]`: `<debtor> pays <creditor> <amount>`, one per line — `Bob pays Alice
10.00`. Two decimal places always (`ADR-0003` point 2), the stored spelling of each name
(`ADR-0005` point 4). Rejected `Bob → Alice: 10.00` and a table: the sentence form is what someone
reads aloud at the end of a meal, which is the moment the product exists for.

### Q3 — What is printed when nobody owes anything?

**Answer** `[assumed]`: exactly `Everybody is settled up.`, on standard output, exit `0`. The same
message in all three of the cases that reach it — nothing recorded at all (AC1), people but no
expenses (AC2), and expenses that balance (AC3) — because a user cannot act differently on the
three and distinguishing them would only invite a criterion about which is which.

### Q4 — `ADR-0004` says ties are broken "by the person's name". By which form of the name?

**Answer** `[assumed]`: by the **identity key** (`ADR-0005` point 3 — whitespace-normalised,
case-folded), ascending. Comparing raw spellings would make the printed order depend on who
happened to type a capital letter, which is the same failure `ADR-0005` already rules out for
identity. This matters in AC4, where Bob and Carol have equal debts and the order is the only
thing distinguishing two otherwise valid outputs.

### Q5 — Which valid settlement is printed?

**Answer** `[assumed]`, and it is the largest thing decided here. `ADR-0004` promises three
properties, not a particular output; but a criterion cannot name an expected output without
fixing *which* valid settlement is produced. So the criteria pin the procedure the ADR itself
names when justifying its `n - 1` bound: the largest debtor pays the largest creditor the smaller
of the two amounts, repeatedly, ties by identity key.

The alternative was to write the criteria as properties only — "the transfers settle everybody,
and there are at most `n - 1`" — with no expected output anywhere. That is more faithful to the
ADR and materially weaker as a specification: `verify` would have to write its own settlement
checker to decide anything, and two implementations that disagreed would both pass. Pinning the
procedure is recorded here as the cost it is: **if `plan` finds a better settlement algorithm, it
must come back to this item's criteria, not just change the code.**

### Q6 — Does `who-owes-whom` write anything?

**Answer** `[assumed]`: no — AC10 asserts the record file is byte-identical afterwards. Nothing in
the record says so; it follows from `ADR-0003` point 6 (nothing derived is stored), and it is
cheap to assert now and awkward to discover later, when some future caching change makes a read
command a writer.

---

## Definition of Ready — where each criterion stands

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic`, `priority` set; `depends-on: WI-0002`, which is `done` |
| R2 | pass | `## Story` names the role, the capability and the "so that" |
| R3 | pass | AC1–AC12, each a labelled checkbox |
| R4 | pass | every criterion names a command and the exact output that settles it; the four `[assumed]` answers above are what removed the last of the vagueness, and the three properties ADR-0004 promises are each turned into a checkable instance (AC7, AC8, AC9) rather than left as prose |
| R5 | pass | `## Out of scope` names five things, of which the pairwise breakdown is the one a reader would most reasonably assume is included — it is what "who owes whom" means in most other tools |
| R6 | pass | the one question on this item is `answered` |
| R7 | pass | `depends-on: WI-0002`, which is `done` and merged |
| R8 | pass | this file |
| R9 | pass | one coherent change: derive net positions, produce transfers, print them. There is no half of it that is separately useful |
| R10 | pass | every case the one subcommand introduces is stated — nothing recorded (AC1), people but nothing spent (AC2), balanced (AC3), one creditor (AC4), uneven (AC5), strangers (AC6), a zero-position person (AC12), an argument (AC11) — and the three things left open are named in `## Notes` with `refine` recorded as who left them |

No override was needed or taken.
