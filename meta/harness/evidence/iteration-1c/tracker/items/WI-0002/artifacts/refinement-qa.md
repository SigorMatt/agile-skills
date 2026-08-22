# Refinement Q&A — WI-0002

The exchange that refined this item. Two questions were put to the stakeholder as artifacts and
answered by them between sessions (`questions/Q-001.md` and `Q-002.md`); both are copied here
verbatim. Everything else was decided at refinement under conventions the stakeholder had already
delegated, and is tagged `[assumed]` with the delegation it rests on named.

Tags: `[human]` — the stakeholder said this. `[assumed]` — `refine` proposed it and the
stakeholder deferred to us, or it follows from a decision they delegated. `[unresolved]` — asked
and not settled.

---

## Q1 (Q-001, filed by `intake`) — Should every person sharing an expense pay an equal share of it, or do you need to say who owes how much?

Options offered: A, always equal; B, per-person amounts; C, equal by default with an override.
Recommendation: A.

**Answer [human]:** "Equal is fine for now — most of the time we're just splitting a bill evenly.
Don't need per-person amounts."

Propagated by `answer-questions` into AC1 and the out-of-scope list: an expense stores the payer,
the amount, a description and the sharers, and the command must not accept a per-person amount —
which is why AC1 asserts that `--share-amount` is a usage error rather than silently ignored.

---

## Q2 (Q-002, filed by `refine`) — Should an expense carry a date, and if it should, what date does it get when you do not supply one?

Options offered: A, no dates; B, every expense dated, today by default, `--date` to override, the
row's own date when imported; C, imported expenses dated and hand-entered ones not.
Recommendation: B.

**Answer [human]:** "Yeah, give expenses a date. If I don't type one, just use today's date."

Propagated into AC1, AC3 and AC6 here, into WI-0004 AC2 (an imported expense takes its row's
date), into EP-001's scope, and into `docs/product/vision.md` v7.

---

## Decided at refinement

Not put to the stakeholder. Each rests on ADR-0002 and ADR-0005, which `answer-questions` wrote
under the stakeholder's delegation on WI-0001/Q-004 — "whatever you think is best here, this is
exactly the kind of thing I'm paying you to decide" — and recorded as binding on this item. None
of them decides anything the stakeholder has expressed a view about.

- **[assumed] The command is `add-expense`, with `list-expenses` to read them back**, the names
  ADR-0002 clause 3 reserved. Options: `--paid-by`, `--amount`, `--description`, `--shared-by`,
  `--date`, `--data-file`. `--paid-by` and `--shared-by` are already written into WI-0004 AC6, so
  choosing anything else would contradict a criterion that exists.
- **[assumed] One rendering for an expense**, used by both the confirmation and the listing:
  `<YYYY-MM-DD> <amount> <description> — paid by <payer>, shared by <names>`. Two renderings would
  drift apart, and every behaviour would then have two strings to check.
- **[assumed] The amount grammar** — a decimal with at most two places, no symbol, no separators.
  `1.005` is refused rather than rounded: rounding at input would change what someone owes without
  telling them, and ADR-0001 makes rounding a property of the split, not of the input.
- **[assumed] Sharers are snapshotted when the expense is recorded.** AC2's original wording, from
  intake, says the recorded expense "shows that explicitly rather than leaving it implied"; the
  snapshot is what that means in practice, and the alternative would silently rewrite who shared
  last month's dinner the next time a friend is registered.
- **[assumed] A person named twice in `--shared-by` is refused, not silently de-duplicated.** The
  stakeholder's own words about the import — "I don't want it silently doubling up" — read in
  reverse: a mistyped list should be reported, not quietly repaired.
- **[assumed] The exact refusal messages** in AC4 to AC8. `Unknown person: Dan` and
  `Amount must be a positive number …` follow the examples ADR-0005 clause 2 gives.
- **[assumed] The undated default is the machine's *local* date.** Recorded here after the fact:
  `refine` originally glossed AC6's check as `date -u +%F`, `plan` found that this contradicts the
  criterion's own first half on any machine not running UTC, and `answer-questions` amended AC6 to
  `date +%F` (WI-0002/Q-003). The substance is the stakeholder's — "just use today's date" — and
  the defect was in the check clause `refine` wrote, not in what they asked for.
- **[assumed] Listing order is date ascending, ties in the order recorded.** An unordered listing
  cannot be compared, so AC3 would not be decidable without it.

## Left unconstrained

- **[unresolved] `argparse`'s usage-error wording.** The exit code is fixed at 2 and asserted; the
  text is not. Left so by `refine`, as on WI-0001.
- **[unresolved] A description containing ` — ` or a comma.** Stored and printed verbatim, which
  makes the rendered line ambiguous to a parser. Nothing parses it — the stakeholder reads it — so
  no criterion constrains it. Left so by `refine`.

Both are carried into the item's `## Notes` under "Left deliberately unconstrained (R10)".

## Override

None. No Definition of Ready criterion was overridden.
