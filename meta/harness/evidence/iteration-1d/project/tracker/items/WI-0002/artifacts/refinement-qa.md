# Refinement Q&A — WI-0002

> **Complete. The item is Ready as of 2026-08-22T02:56:51Z**, with no override. Round 1 was one
> question to the stakeholder, answered. Round 2 asked them nothing: everything left was either
> settled by their answer or was `refine`'s to decide, and the three decisions taken are listed
> below with their reasons.
>
> The stakeholder is asynchronous and has never been in a session with this pipeline. Every
> `[human]` line in this workspace is their written answer in a question file, quoted exactly.

## Round 1 — filed 2026-08-22T02:39:45Z, answered 2026-08-22T02:48:51Z

One question. It is one rather than a batch because everything else this item needed was either
already settled by WI-0001's refinement or is small enough for `refine` to decide and record —
see "Decided without asking" below. Inventing companion questions to fill a batch would spend the
stakeholder's attention on things I can answer myself.

| # | question | file | DoR criterion it unblocks | answer |
|---|----------|------|---------------------------|--------|
| 1 | Does the report print every debt between each pair of people, or the shortest list of payments that settles everybody up? | `questions/Q-001.md` | R4 (AC1, AC2, AC4, AC5, AC6 not decidable), R10 | **A — every debt between each pair.** `ADR-0006` |

### The exchange, so far

**1 — the shape of the report.**

- `[refine]` Asked, with a worked three-person example, whether the report is the **pairwise**
  set of debts (option A) or the **minimised** set of transfers that clears the same net
  positions (option B). Option C — one un-netted line per expense — was listed and rejected in
  the question itself. Recommendation given: **B**, because the epic's goal is settling up and B
  minimises the number of times money changes hands; with A named as the right choice if any line
  may have to be justified against a specific meal.
- `[human]` "A — I want the pairwise breakdown. If the number ever gets questioned I want it to
  trace straight back to what those two people actually shared, not to some clever routing
  through somebody else's taxi. Fewer transfers doesn't matter as much as nobody being able to
  argue about a line."
- `[answer-questions]` Recommendation **not** taken: `refine` had recommended B and the
  stakeholder chose A, giving traceability as the reason — exactly the ground on which the
  question named A as the right choice. Recorded as `ADR-0006`, which fixes the five computation
  steps and states that a printed circle is correct output rather than a defect. **AC1 was
  rewritten** to say "pairwise"; AC2–AC6 were left alone, because the answer makes each decidable
  as written and their wording belongs to the `refine` execution that will give the DoR verdict.

## Decided without asking

Six things this item needs were settled by `refine` rather than put to the stakeholder. Each is
presentation or a property that holds identically under both options in `Q-001`, each is
reversible until `implement` writes code, and none changes what the tool records or what it is
for. They are written here, and in `item.md` under `## Notes`, so that `answer-questions`, `plan`
and `verify` inherit them visibly rather than re-deriving them.

| # | assumed | why not asked |
|---|---------|---------------|
| 1 | The printed debts must account for every recorded cent exactly: the amounts on the printed lines sum, per person, to that person's net position, with no minor unit invented or lost | This is AC2's balance property made exact. `ADR-0004` holds money as integer minor units, so exactness is free under either option in `Q-001` and needs no rounding convention of its own. It is the property a test can assert equality on. |
| 2 | Only non-zero debts are printed. A pair who are square, or a person who has repaid everything, produces no line at all | AC3 and AC6 already say the report must not print zero-amount debts and must say "nobody owes anybody" instead. This is those two criteria restated as a rule rather than a new decision. |
| 3 | The report does not distinguish "settled — was owed, now repaid" from "never owed anything". Both simply produce no line | `item.md`'s `## Notes` listed this as something `refine` must settle. It is presentation, it is what assumption 2 implies, and adding a "settled" line later is a change to one print statement with no data behind it. Naming it here so a stakeholder who disagrees can find it. |
| 4 | Lines are ordered by debtor name, then by creditor name, comparing under WI-0001 AC1's matching rule — trimmed and ignoring case — so the order is stable and does not depend on the order things were recorded | AC4 requires a deterministic order but does not name one. An unstated order is untestable. Sorting by name is the only order that stays stable when an expense is added in the middle, which is what "running it twice prints the same lines" is really about. |
| 5 | The report prints debt lines and nothing else — no per-person net position summary, no totals | AC1 states the form of the output and `## Out of scope` already excludes other output formats. Adding a summary is additive and cheap later; guessing that it is wanted now is not. |
| 6 | A recorded person who has neither paid for nor shared in anything contributes no line, and their presence does not stop AC3's "nobody owes anybody" from being printed | The boundary case `verify` would otherwise have to invent an answer for. Follows from assumption 2. |

Assumptions 1, 2, 4, 5 and 6 hold whichever option `Q-001` selects. Assumption 3 is the only one
a stakeholder is likely to have a view on, and it is the cheapest of the six to reverse.

## Definition of Ready — still not assessed to a verdict

`refine` reached no verdict, and `answer-questions` does not give one: R4 and R10 are `refine`'s
to judge, and it may not assess a Definition of Ready it did not run. What changed on
2026-08-22T02:48:51Z is that the obstacle is gone — the answer to `Q-001` makes AC1 concrete and
settles the two R10 rows that depended on it. **No override was recorded**, then or now. The
next `refine` execution takes the item from `draft` and owns the verdict.

## Round 2 — 2026-08-22T02:56:51Z, no questions put to the stakeholder

`refine` was dispatched again once `Q-001` came back answered. **Nothing was asked this round.**
The Definition of Ready failed on R4 and R10, and after the pairwise answer every remaining gap
was either arithmetic that follows from `ADR-0002`, `ADR-0004` and `ADR-0006`, or presentation
that `refine` may decide and record. Inventing questions to fill a round would have stopped the
loop for nothing, and the stakeholder has an unanswered request outstanding on WI-0003 already.

### What R4 actually needed, and what closed it

The six inherited criteria were rewritten into eleven. The old-to-new map, and the reason for
each change, is in `item.md` under "The criteria were renumbered — old to new"; it is not
duplicated here. In summary: four criteria that stated a *property* now also carry a complete
ledger and the exact stdout it must produce, and three of `refine`'s round-1 assumptions became
criteria in their own right.

### The one thing that was wrong rather than merely vague

- `[refine]` Old AC3 said the report announces that nobody owes anybody when "every person's net
  position is zero". Under the **minimised** report `refine` had recommended, that condition is
  equivalent to "there is nothing to print". Under the **pairwise** report the stakeholder chose,
  it is not: a circle — Ana owes Ben, Ben owes Cara, Cara owes Ana, all for the same amount — has
  every net position at zero and three debts that must still be printed. Carried forward
  unchanged, AC3 would have contradicted AC1 on precisely the case `ADR-0006` calls out.
- `[refine]` Corrected without asking: AC4 now triggers on "no **pair** has a non-zero balance",
  and AC8 fixes the circle with a worked example. This is a contradiction between two criteria,
  which is `refine`'s to resolve; it takes nothing away from what the stakeholder asked for, and
  it is recorded loudly because a criterion changed meaning.

### Decided, not asked

| # | decision | tag | why not asked |
|---|----------|-----|---------------|
| 1 | The command is `debts`: `python3 -m expenses debts` | `[assumed]` | R4 cannot pass without naming what a reader types. `people`, `expenses` and `repayments` are already plural nouns for listings, so `debts` is the shape the CLI already has. One line of `argparse` to change |
| 2 | The empty-report line is exactly `Nobody owes anybody.` | `[assumed]` | An exact string is what makes AC4 decidable. It matches `No people recorded.` in tone. It is `refine`'s wording, not the stakeholder's |
| 3 | AC4 triggers on pairs, not on net positions | `[assumed]` | The correction above |
| 4 | Three new exclusions: minimised settlement, per-person summary, per-line explanation | `[assumed]` | R5. The first is the option the stakeholder explicitly rejected; the other two are the things a reader of "shows who owes whom" might assume are included |

Round 1's six decisions stand unchanged. Every one of them was chosen to hold under either option
in `Q-001`, and the pairwise answer did not disturb any of them.

## Definition of Ready — **Ready**, no override

Assessed criterion by criterion; the table is in `item.md` under "Definition of Ready, as
assessed by `refine` at 2026-08-22T02:56:51Z", and the same verdicts are in this execution's
journal entry under `**Gates:**`. R1–R3 and R5–R9 pass. R4 passes after the rewrite. R10 passes
against a fourteen-row combination table.

**Nothing was waived and no `## Override` section exists**, because none was needed.
