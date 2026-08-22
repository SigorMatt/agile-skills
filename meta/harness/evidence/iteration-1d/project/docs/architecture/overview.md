---
title: Architecture overview
version: 8
status: current
updated: 2026-08-22T03:57:28Z
updated-by: review-close
updated-for: BUG-0001
---

# Architecture overview

The shape of the system as it stands after WI-0001 and WI-0002 were implemented and BUG-0001 was
fixed. Everything below describes code that exists. Each version says which item wrote it in the
change log, and the two habits worth knowing are visible there: v4 described `expenses/debts.py`
and the `debts` command *in advance*, and v5 was WI-0002 re-checking that description against what
had actually been built [src: tracker/items/WI-0002/artifacts/plan.md].

## What it is

One Python package, run from a checkout, with no install step and no third-party packages
[src: ADR-0005]. Everything happens in one process, against one file, on one machine.

```
expenses/
├── __init__.py
├── __main__.py     # python3 -m expenses → cli.main(sys.argv[1:])
├── cli.py          # argparse subcommands; the only place exit codes and stderr are decided
├── model.py        # the record types and the validators: names, amounts, dates
├── debts.py        # the pairwise debt computation, a pure function over a Ledger
└── store.py        # locating, reading and writing the ledger file
tests/              # unittest, discovered from here
```

## The four modules, and what each is allowed to know

- **`store.py` — where the data lives.** Resolves the ledger path (`--file`, then
  `EXPENSES_LEDGER`, then the XDG default), reads the JSON document, writes it back atomically.
  It knows the file format and nothing about commands [src: tracker/items/WI-0001/artifacts/plan.md].
  A missing file reads as an empty ledger.
- **`model.py` — what a record is, and what is valid.** The three record kinds — person, expense,
  repayment — and the validators that decide whether an input is acceptable: name normalisation,
  `parse_amount` / `format_amount`, date parsing. It raises a validation error and does not print
  or exit. Keeping the rules here rather than in `cli.py` is what lets WI-0003's importer reuse
  them, so the import cannot accept an amount or a date the hand-entry command would refuse.
- **`debts.py` — who owes whom.** One pure function, `debts(ledger)`, returning the ordered list
  of `Debt` records the report prints, and the `Debt` type itself. It is `ADR-0006`'s five steps
  and nothing else: it imports from `model` only, reads no file, prints nothing, and defines no
  error path of its own — every ledger whose recorded amounts are the integers the store wrote has
  a debt report, including an empty one [src: ADR-0008; expenses/debts.py]. It is **not** hardened
  against a hand-edited ledger: `Ledger.from_dict` checks that the keys are present and not what
  their values are, so an amount written into the file as a string reaches
  `share = expense.amount_minor // len(expense.sharers)` and raises `TypeError`, exactly as such a
  ledger already breaks the `expenses` and `repayments` listings through `format_amount`
  [src: expenses/model.py; expenses/cli.py]. `ADR-0008` and the module's own docstring say "raises
  nothing" without that qualification; the correction is recorded as a finding in WI-0002's review
  [src: tracker/items/WI-0002/artifacts/review.md]. The remainder rule it applies has no branch
  on whether the payer is among the sharers [src: ADR-0009; expenses/debts.py]. Internally it
  holds one signed integer per unordered pair of people, so netting a pair is addition and the
  direction of a line is the sign at the end.
- **`cli.py` — the interface.** Parses arguments, calls the model to validate, calls the store to
  load and save, prints, and chooses the exit code. It is the only module that writes to stdout or
  stderr. It does not exit: `main` **returns** the code, and `__main__.py`'s single
  `raise SystemExit(main(...))` is the only statement in the package that ends the process
  [src: expenses/cli.py; expenses/__main__.py]. A handler returns `str | None` — the single line
  to print once the save has succeeded, or `None` when it changed nothing — and `main` loads,
  calls the handler, saves when there is a line, and prints the line only after `store.save` has
  returned [src: ADR-0011]. So a run whose write fails prints nothing on stdout, and the ordering
  is a property of `main` rather than something each command has to remember. The four listings
  are the deliberate exception: they print their rows directly and return `None`, because a
  listing has no save to be ordered against and printing as it goes is why `expenses` does not
  hold a whole ledger's formatted text in memory first [src: ADR-0011].

The dependency direction is one-way: `cli` → `model`, `cli` → `store`, `cli` → `debts`,
`debts` → `model`, and `store` → `model` for serialising the record types. `model` imports none
of the others [src: expenses/model.py].

## The data

One JSON document per ledger, holding a schema `version`, `people`, `expenses` and `repayments` as
three insertion-ordered arrays [src: ADR-0003]. Expenses and repayments are separate arrays and
neither is expressible as the other [src: ADR-0001]. Amounts are integer minor units under
`amount_minor`; no float ever holds money (`ADR-0004`).

An expense stores its total and the names of its sharers, never a per-person amount
[src: WI-0001 AC5]. Each sharer's share is arithmetic performed when the debts are reported,
which is WI-0002's job, under the rule that the payer absorbs the remainder (`ADR-0002`).

People are matched by `name.strip().casefold()` and displayed in the form first typed
[src: WI-0001 AC1]. The normalised form is never stored: `Ledger.find_person` computes it on each
comparison and scans `people` in order [src: expenses/model.py]. That is a linear scan rather than
an index, which for a friend group is a handful of comparisons; the note in `ADR-0003` about the
scale at which whole-file rewrites stop being cheap applies here too.

## The commands

```
python3 -m expenses [--file PATH] <command> [options]

  add-person   NAME
  people
  add-expense  --payer NAME --amount AMOUNT --description TEXT
               [--shared-by NAME ]... [--date YYYY-MM-DD]
  expenses
  repay        --from NAME --to NAME --amount AMOUNT [--date YYYY-MM-DD]
  repayments
  debts
```

`debts` takes no options of its own and writes nothing: it prints one `<debtor> owes <creditor>
<amount>` line per pair of people whose balance is not zero, ordered by debtor then creditor
under the trimmed, case-folded comparison, or the single line `Nobody owes anybody.` when no pair
has one [src: WI-0002 AC1; WI-0002 AC4; WI-0002 AC5]. The debts are pairwise: nothing is re-routed
between pairs, so a circle of debts is printed rather than collapsed into fewer transfers
[src: ADR-0006].

`--file` is global and must appear **before** the subcommand; placed after it, `argparse` reports
an unrecognised argument and exits 2 [src: expenses/cli.py]. `--shared-by` is repeatable and takes
one name per occurrence, so a name containing a comma is not a problem. Omitting `--shared-by`
entirely is what AC4 means by "without naming any sharers" [src: WI-0001 AC4].

## Exit codes

| code | meaning |
|------|---------|
| 0 | the command did what was asked |
| 2 | the input was refused — a bad argument, an unknown person, a malformed amount or date, a duplicate. `argparse` already uses 2 for usage errors, so validation joins it rather than inventing a third code |
| 1 | the ledger could not be read or written |

Every refusal prints its reason to stderr and leaves the recorded data unchanged
[src: WI-0001 AC1; WI-0001 AC3].

## What is not here yet

- The bank CSV import (WI-0003), which consumes what this package records and has not been
  planned.
- Any packaging, entry point, or installation. `python3 -m expenses` is the whole invocation
  story (`ADR-0005`).
- Any editing or deletion of a recorded person, expense or repayment [src: WI-0001].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 8 | 2026-08-22T03:57:28Z | review-close | BUG-0001 | D12 audit: the opening paragraph still read "this version is step 5 of WI-0002's plan", which was true at v6 and became false when v7 was written for BUG-0001. Rewritten so the lede describes the document rather than whichever version last touched it, which is the form that stops going stale |
| 7 | 2026-08-22T03:49:31Z | implement | BUG-0001 | Step 6 of the plan: the `cli.py` bullet now states the handler contract and the load-handle-save-print ordering `ADR-0011` decided, which is what a fourth mutating command — WI-0003's importer — needs in order not to rediscover it |
| 6 | 2026-08-22T03:23:54Z | review-close | WI-0002 | D12 audit: v5 said `debts.py` "raises nothing — every ledger the store can load has a debt report". A hand-edited ledger whose amount is a JSON string loads and then raises `TypeError` out of the share division, so the claim was qualified to what the code supports |
| 5 | 2026-08-22T03:11:44Z | implement | WI-0002 | Step 5 of the plan: `debts.py` and the `debts` command are built and this document now describes code that exists; added the signed-pair-accumulator sentence and cited the module itself |
| 4 | 2026-08-22T03:03:14Z | plan | WI-0002 | Added `debts.py` and the `debts` command as WI-0002 plans them, with the new dependency edge; the three layers became four |
| 3 | 2026-08-22T02:33:32Z | review-close | WI-0001 | D12 audit: v1 and v2 said `cli.py` is "the only one that exits"; `cli.main` returns an int and `__main__.py` is what raises `SystemExit`. Corrected |
| 2 | 2026-08-22T02:20:40Z | implement | WI-0001 | Corrected the claim that the normalised name is an index built on load — `find_person` scans; added the command list and the fact that `--file` must precede the subcommand |
| 1 | 2026-08-22T02:06:34Z | plan | WI-0001 | First version, written while planning the first item |
