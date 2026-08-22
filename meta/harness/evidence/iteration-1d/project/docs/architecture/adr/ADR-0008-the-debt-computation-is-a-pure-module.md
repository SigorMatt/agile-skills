---
title: The debt computation is a pure module, not code inside the CLI
version: 1
status: current
updated: 2026-08-22T03:03:14Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0008 — The debt computation is a pure module, not code inside the CLI

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0002 adds the first piece of arithmetic in this project that is neither validation nor
storage: turning a ledger of expenses and repayments into the pairwise debts `ADR-0006`
describes. The existing package has three modules with responsibilities that were written down
before any code existed — `store.py` holds the file, `model.py` holds the record types and the
validators, `cli.py` parses arguments, prints and chooses the exit code
[src: docs/architecture/overview.md]. None of the three is where a report computation obviously
belongs, so this item either bends one of them or adds a fourth.

Two properties of WI-0002 bear on the choice. Its AC3 is an arithmetic identity that has to be
checkable in a test without going through argument parsing or stdout [src: WI-0002 AC3]. And
`ADR-0006`'s five computation steps are a rule other work will read back: WI-0003 imports
expenses that this computation then has to account for [src: WI-0003].

## Options considered

- **A — a new module `expenses/debts.py`, holding a pure function from a `Ledger` to an ordered
  list of debts, with `cli.py` doing nothing but printing what it returns.** Cost: a fourth
  module and a fourth entry in the overview's layer description, for roughly sixty lines of
  code. Risk: low; the dependency direction stays one-way, `debts` → `model`, and nothing else
  imports it.
- **B — a `cmd_debts` handler in `cli.py` that computes and prints in one pass.** Cost: none up
  front, and it matches how the six existing commands are written. Risk: the computation becomes
  reachable only through `argparse` and `redirect_stdout`, so AC3's identity has to be asserted
  by parsing printed lines back into numbers — a test that fails for formatting reasons and
  reports an arithmetic failure. It also puts the project's only non-trivial arithmetic in the
  module the overview says exists to parse, print and choose exit codes.
- **C — methods on `Ledger` in `model.py`.** Cost: none up front. Risk: `model.py` is described
  as the record types and the validators, and is the module WI-0003's importer will reuse for
  exactly that reason [src: docs/architecture/overview.md]. Growing a report into it makes that
  sentence false, and the next reader has to discover the real boundary by reading the code.

## Decision

**A.** `expenses/debts.py` holds the computation, and exports two names:

- `Debt` — a frozen dataclass of `debtor: str`, `creditor: str`, `amount_minor: int`, where
  `amount_minor` is always greater than zero and the names are display forms
  [src: WI-0001 AC1].
- `debts(ledger) -> list[Debt]` — `ADR-0006`'s five steps, returning the lines the report
  prints, already ordered by debtor then creditor under `normalise_name`
  [src: WI-0002 AC5]. An empty list means no pair has a non-zero balance, which is the condition
  AC4 prints its one-line message for [src: WI-0002 AC4].

The module imports from `model` and from nothing else in the package. It does not read the
store, does not print, and does not raise: every ledger the store can load has a debt report,
including an empty one [src: WI-0002 AC4; tracker/items/WI-0002/artifacts/plan.md]. `cli.py`
gains a `debts` subcommand whose handler calls it, prints, and returns `False` for
"nothing to save" [src: tracker/items/WI-0002/artifacts/plan.md].

## Consequences

- AC3's identity is asserted against a list of `Debt` objects and integers, so a failure of the
  arithmetic is reported as one, and a change to the printed wording cannot break it
  [src: WI-0002 AC3].
- The overview gains a fourth module and its dependency edge. The layer sentence stops being
  "three layers" and becomes four, which is a documentation change this item pays for.
- A later minimised-settlement view, which `ADR-0006` says would be a separate command over the
  same data, has a function to build on rather than a handler to copy.
- **Reversibility: high.** Nothing is stored, no interface leaves the package, and the whole
  module is one file with one caller. Folding it back into `cli.py`, or forward into `model.py`,
  is a move of two definitions and their imports. This is why the decision is recorded rather
  than escalated.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T03:03:14Z | plan | WI-0002 | First version |
