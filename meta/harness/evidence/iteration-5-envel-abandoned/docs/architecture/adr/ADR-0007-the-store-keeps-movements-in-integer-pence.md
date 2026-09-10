---
title: The store keeps the movements, and an amount is an integer number of pence
version: 1
status: current
updated: 2026-09-10T15:11:11Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0007 — The store keeps the movements, and an amount is an integer number of pence

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** — (extends `ADR-0003`, which is not superseded: one JSON document, at that
  path, replaced atomically, still stands. What changes is the document's contents at a new
  `version`, which `ADR-0003` provided for)

## Context

WI-0002 is the first item that puts money in the store. Two questions have to be answered before
any of its nineteen criteria can be built, and refinement routed both here rather than to the
stakeholder because the answer would be the same whoever they were [src: WI-0002].

**Does the store keep the movements, or only a running balance?** WI-0002 alone needs only the
balance: every criterion it states is satisfied by a number per envelope [src: WI-0002 AC15 "each
line it writes carries the envelope's name and that envelope's balance"]. Two later items need
more. WI-0003 summarises a month — "for each envelope, what it took in and what went out of it"
[src: EP-001/Q-005] — which is a statement about individual movements and their dates. WI-0005
corrects or removes a spend already recorded [src: WI-0005], which needs the spend to still exist
as a thing.

**What is an amount, in the file?** The stakeholder refused rounding: an amount with more than two
decimal places is refused rather than stored [src: WI-0002/Q-002], and every printed figure
carries exactly two decimal places [src: ADR-0006]. A promise not to store a number they did not
type is a promise about arithmetic as well as about parsing, and JSON has one numeric type.

`ADR-0003` decided the surrounding question and left this one open on purpose: "`envelopes` is a
list of **objects** rather than of strings because the items that follow this one add money to an
envelope" [src: ADR-0003]. It also fixed the window this decision has to be taken in — the format
"is cheap to reverse while `version` is 1 and no real data exists" [src: ADR-0003].

## Options considered

For what the store holds:

- **A — a running balance per envelope, with the movements discarded.** Each envelope object
  gains a balance field, updated in place. Cost: the least code in this item, and the balance is
  read rather than computed. Risk: WI-0003 and WI-0005 cannot be built on it
  [src: WI-0003; WI-0005]. Adding movements afterwards means a migration of a file that has
  months of the person's real spending in it and nothing saying where any of it came from, so the
  migration has no history to reconstruct. That is the expensive half of the reversal `ADR-0003`
  warned about.
- **B — a list of movements, and the balance computed from it.** Each recording appends an object;
  a balance is the income minus the spending for that envelope. Cost: the whole list is walked to
  print a listing, and the store grows with use rather than staying one line per envelope. Risk:
  at one person's scale — a few movements a day — the walk is nothing, and `ADR-0003` already
  rewrites the whole document on every change for the same reason.
- **C — both: movements, and a cached balance kept beside them.** Cost: two representations of
  one fact. Risk: they can disagree, and the first time they do the person's money is wrong in a
  way nothing detects. A cache is worth its risk when the computation is expensive; here it is a
  sum over a list that fits in a screenful.

For what an amount is, in the file:

- **D — a JSON number, written as the person typed it.** `12.50` becomes the float closest to
  12.50. Cost: nothing to write. Risk: floats are the standard way to lose a penny. Summing
  0.10 three times does not give 0.30 in binary floating point, and the stakeholder's stated
  reason for this whole area is that the number should be the truth [src: EP-001/Q-003]. A
  balance that has drifted also cannot satisfy AC6, which refuses a spend by comparing it against
  a balance [src: WI-0002 AC6 "recording a spend larger than the balance of its envelope is
  refused"].
- **E — a JSON string, parsed with `decimal.Decimal` on the way in.** Cost: `decimal` is in the
  standard library, so `ADR-0001` permits it. Risk: the exactness depends on the context's
  precision and on nobody dividing; it is more machinery than this needs, and the store's numbers
  stop being numbers to anything reading the file.
- **F — an integer number of pence.** `12.50` is stored as `1250`. Cost: a parse and a format at
  the boundary, and a reader of the raw file sees `1250` rather than `12.50`. Risk: none at this
  scale — every amount this product handles is a whole number of pence by the stakeholder's own
  rule, and integer arithmetic in Python is exact and unbounded.

## Decision

**Options B and F.** The store's format version becomes 2 and the document gains a
`transactions` key:

```json
{
  "version": 2,
  "envelopes": [{"name": "groceries"}],
  "transactions": [
    {"envelope": "groceries", "kind": "income", "amount": 40000, "date": "2026-09-10"},
    {"envelope": "groceries", "kind": "spend", "amount": 1250, "date": "2026-08-31"}
  ]
}
```

1. `transactions` is a list in the order the movements were recorded. Appending is the only write
   WI-0002 makes to it; nothing here removes or edits an entry, which is WI-0005's.
2. `envelope` holds the **stored display name** of the envelope, exactly as it appears in the
   `envelopes` list. A movement is matched to an envelope by comparing identities, which is
   `ADR-0004`'s rule and not a second one: `identity("Groceries") == identity("groceries")`
   [src: ADR-0004]. The display name is stored rather than the identity so that the file stays
   readable by the person whose money it is, which is why it is JSON at all [src: ADR-0003].
3. `kind` is `"income"` or `"spend"`. Two kinds rather than one signed amount, because a signed
   amount gives two ways to write the same movement and makes WI-0005 ambiguous about what it is
   correcting [src: WI-0002].
4. `amount` is a **positive integer number of pence**. It is never zero and never negative
   [src: WI-0002 AC9 "an amount of zero, and a negative amount, are refused on both commands"].
5. `date` is the string `YYYY-MM-DD` [src: WI-0002 AC7 "The date is given as `--date YYYY-MM-DD`"].
6. An envelope's **balance** is the sum of its `income` amounts minus the sum of its `spend`
   amounts, in pence. An envelope with no movements has a balance of 0
   [src: WI-0002 AC16 "an envelope that has had nothing put into it shows a zero balance"].

**Reading a version 1 store.** `envel/store.py`'s `load` upgrades a `version: 1` document in
memory: it gains an empty `transactions` list and its `version` becomes 2. The upgrade stays in
memory until the next `save` [src: envel/store.py:58], so reading an old store leaves the file as
it was. A document whose `version` is
greater than the one this build knows raises `StoreError` rather than being read on the guess that
the fields it knows are still the fields that are there.

## Consequences

- WI-0003 and WI-0005 are buildable against this file without a migration of anybody's real data.
  That is the whole of why decision B is taken in the item that does not need it.
- Every amount that crosses into the store is a whole number of pence, so the arithmetic AC3, AC6
  and AC8 rest on is exact rather than nearly exact.
- A person reading their own store file sees `1250` where they typed `12.50`. That is the price of
  F, and it is paid in a file they rarely open rather than on the screen they read every day,
  where `ADR-0006` rule 3 puts `12.50`.
- The store grows with use. A person recording ten movements a day for five years has about
  eighteen thousand entries in one JSON document, which `json` reads in a few milliseconds. If
  this product ever needed more, it would need a different store, which `ADR-0003` already says.
- **Reversing the shape is cheap now and stops being cheap the moment the stakeholder has real
  data**, which is the same window `ADR-0003` named and is the reason this is decided in WI-0002
  rather than deferred to WI-0003. Reversing the pence decision is cheaper for longer: it is a
  parse and a format in one module, and a rewrite of the `amount` field of every entry, which a
  migration can do exactly because integers to two decimal places lose nothing.
- `ADR-0003` is **not superseded**. Its decision was one JSON document at an overridable path,
  replaced atomically, with a `version` field so that "a later item that adds fields can tell an
  old file from a new one without guessing" [src: ADR-0003]. This is that later item, using that
  field for that purpose. Its illustration of the shape is labelled "at this version" and stays
  true of version 1.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T15:11:11Z | plan | WI-0002 | First version: store format version 2 with a `transactions` list, an amount held as a positive integer number of pence, the balance computed rather than cached, and the in-memory upgrade of a version 1 document |
