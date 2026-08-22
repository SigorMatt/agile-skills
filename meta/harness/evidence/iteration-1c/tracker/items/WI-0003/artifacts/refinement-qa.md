# Refinement Q&A — WI-0003

The exchange that refined this item. Three questions were put to the stakeholder as artifacts and
answered between sessions (`questions/Q-001.md`, `Q-002.md`, `Q-003.md`); all three are copied here
verbatim. Everything else was decided at refinement under conventions the stakeholder had already
delegated, and is tagged `[assumed]` with the delegation named.

Tags: `[human]` — the stakeholder said this. `[assumed]` — `refine` proposed it and the stakeholder
deferred, or it follows from a decision they delegated. `[unresolved]` — asked and not settled.

---

## Q1 (Q-001, filed by `intake`) — Does "who owes whom" mean every debt as it arose, or the payments to make so everyone ends up square?

Options offered: A, pairwise debts; B, minimal settlement; C, balances plus transfers.
Recommendation: C.

**Answer [human]:** "I just want the actual payments — who pays whom to settle up. Don't need every
individual debt listed out."

The recommendation was **rejected** and option B chosen. Propagated by `answer-questions` into AC1
and AC3, with the pairwise listing put out of scope.

---

## Q2 (Q-002, filed by `intake`) — What happens to the leftover penny when an amount does not divide evenly?

Options offered: A, the payer absorbs it; B, whole pence with the remainder spread by name order;
C, exact fractions; D, floating point. Recommendation: B.

**Answer [human]:** "Not sure yet — go ahead anyway, we'll decide later."

**Answer [assumed]** — the stakeholder declined and authorised proceeding, so the architect decided
and recorded ADR-0001: whole pence throughout, and the leftover pennies given one each to the
alphabetically first sharers. AC6 states the rule with a worked example.

---

## Q3 (Q-003, filed by `refine`) — When the report prints who pays whom, should it also print each person's overall balance?

Options offered: A, transfers only; B, balances then transfers; C, transfers annotated with the
expenses behind them. Recommendation: B.

**Answer [human]:** "Yeah, show each person's balance too, not just the payments — makes it easier
to check."

Propagated into AC7 and, in this execution, into the two-section report shape the criteria now
define.

---

## Decided at refinement

Not put to the stakeholder. Each rests on ADR-0002 and ADR-0005, which `answer-questions` wrote
under the stakeholder's delegation on WI-0001/Q-004 and recorded as binding on the later items.

- **[assumed] The command is `./expenses report`**, the name ADR-0002 clause 3 reserved, taking
  only `--data-file`.
- **[assumed] The report is two sections separated by a blank line: balances, then payments.** The
  stakeholder's reason for wanting balances — "makes it easier to check" — is the order: a reader
  works from the balances to the payments.
- **[assumed] The exact line forms**: `<name> is owed <amount>`, `<name> owes <amount>`,
  `<name> is square`, `<payer> pays <payee> <amount>`. These are the shapes Q-001 and Q-003 showed
  the stakeholder, so they are the wording they have already read.
- **[assumed] Payments are printed sorted by payer then payee.** A settlement's internal order is
  an artefact of the algorithm; sorting the output makes AC2 and AC6 comparable without telling
  `plan` how to compute it.
- **[assumed] `Nobody owes anybody` covers both empty cases** — no expenses, and expenses that
  leave everyone square. A report ending in an empty section reads as truncated output.
- **[assumed] The worked example is fixed in AC2**, with the arithmetic spelled out. AC2 asks a
  reader to reproduce the figures by hand, which is impossible against an example that changes.
- **[assumed] Someone registered who shared in nothing still gets a line**, `is square`. This is
  the only view in the tool that shows where a person stands.

## Left unconstrained

- **[unresolved] Which settlement is printed when more than one is minimal.** With three or more
  people, several settlements can satisfy AC1 and AC3. Both worked examples have a unique answer,
  and outside them the criteria require only that the payments settle and number at most `n-1`.
  Left to `plan`.
- **[unresolved] `argparse`'s usage-error wording.** Exit code 2 is fixed; the text is not.
- **[unresolved] Behaviour with a very large group.** Every criterion uses three or four people;
  nothing states or measures an upper bound.

All three are carried into the item's `## Notes` under "Left deliberately unconstrained (R10)".

## Override

None. No Definition of Ready criterion was overridden.
