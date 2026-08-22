---
title: A command handler returns its success line rather than printing it
version: 1
status: current
updated: 2026-08-22T03:41:30Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0011 — A command handler returns its success line rather than printing it

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

`cli.py`'s module docstring states the shape every command has: "resolve the ledger path, load,
apply one change, save atomically, print, return 0" [src: expenses/cli.py]. The code does the
print and the save the other way round. Each mutating handler calls `print` itself and returns a
`bool` saying whether the ledger changed; `main` then saves, and reports a `StoreError` on stderr
with exit 1 [src: expenses/cli.py]. So a run whose save fails prints its success line **and** its
error line and exits 1, which is what `BUG-0001` is [src: BUG-0001].

The data is genuinely unchanged and the exit code is genuinely non-zero, so no WI-0001 criterion
catches it: WI-0001 defines a refusal as a stderr message, a non-zero exit and unchanged data, and
all three hold [src: BUG-0001]. What is wrong is the contradiction on stdout, and a script reading
stdout is told the wrong one of the two things.

The fix has to survive `WI-0003`'s importer, which will be a fourth mutating command
[src: WI-0003 AC1]. So this is a decision about the handler contract, not a decision about three
`print` calls: whatever shape is chosen here is the shape the import command implements. The
constraint that makes it a decision at all is the property WI-0001's plan set out and this project
has kept — every command is the same skeleton, so "a refusal changes no recorded data" is true by
construction rather than by remembering it in six places
[src: tracker/items/WI-0001/artifacts/plan.md].

## Options considered

- **A — the handler returns the line; `main` prints it after a successful save.** The return type
  becomes `str | None`: a string is "the ledger changed, save it, then print this"; `None` is
  "nothing to save". Cost: every handler's signature changes, including the four read-only ones.
  Risk: the return value means *the success line*, not *everything this command prints* — the
  listings still print their own rows directly — and a later reader could mistake it for the
  latter and try to buffer them too.
- **B — the handler returns `(changed: bool, line: str | None)`.** Cost: a two-element tuple at
  every call site and every `return`, for a second element that would be `None` exactly when the
  first is `False` — every handler that mutates the ledger prints exactly one line, and no handler
  prints a success line without mutating it [src: expenses/cli.py]. Risk: two fields that cannot
  disagree invite code that checks the wrong one.
- **C — `main` buffers stdout and flushes it after the save.** Cost: an output-redirection
  mechanism in the one module whose job is to be the simple edge of the program. Risk: it buffers
  the listings as well, so `expenses` on a large ledger stops streaming, and it makes the ordering
  a property of a buffer rather than of the code anyone reads.
- **D — `main` saves before calling the handler.** Not possible: the handler is what produces the
  change to be saved. It would require splitting every handler into a mutate phase and a print
  phase, which is B with more steps.

## Decision

**A.** A command handler returns `str | None`:

- **a string** — the ledger was changed and this is the single line to print once the save has
  succeeded. `main` saves, and reaches the `print` only on the path where `store.save` returned
  without raising [src: expenses/cli.py; BUG-0001 AC1].
- **`None`** — nothing was changed and there is nothing for `main` to print. The read-only
  commands return `None` after printing their own output.

`main` therefore reads: load, call the handler, save when there is a line, print the line. A
`StoreError` from the save returns `EXIT_STORE` before anything reaches stdout
[src: BUG-0001 AC1].

**The return value is the success line, not the command's output.** `people`, `expenses`,
`repayments` and `debts` keep printing their rows directly and return `None`, and that is
deliberate rather than an inconsistency left over from the change: a listing has no save to be
ordered against, and printing rows as they are produced is why `expenses` does not hold a whole
ledger's worth of formatted text in memory before emitting any of it. Option C is the version that
does not make this distinction, and it was rejected for exactly that.

## Consequences

- **The docstring's stated order becomes true.** "resolve the ledger path, load, apply one change,
  save atomically, print, return 0" describes the code after this change; today it describes the
  intent only [src: expenses/cli.py].
- **A failed write says nothing on stdout, for every mutating command at once.** The ordering is a
  property of `main`, so it cannot be got wrong per-command — which is the same argument that put
  the save in `main` in the first place [src: tracker/items/WI-0001/artifacts/plan.md].
- **`WI-0003`'s importer inherits it.** The import command returns its summary line and gets the
  ordering for free, rather than having to remember it [src: WI-0003 AC1]. This is the main reason
  the contract was changed rather than the three `print` calls moved.
- **Nothing outside `cli.py` is affected.** The handler is reached only through
  `args.set_defaults(handler=...)` and the single call in `main`; no test and no other module
  reads a handler's return value [src: expenses/cli.py].
- **A handler that changes the ledger but has nothing to say cannot be expressed**, because
  `None` means both "nothing changed" and "nothing to print". No command is like that today and
  none is planned; if one appears, that is the moment to revisit this, and B is what it becomes.
- **Reversibility: high.** One file, no data migration, no change to the ledger format, and no
  change to any command's arguments, output or exit codes when the save succeeds. The observable
  difference is confined to the failing-write path, which is the defect.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T03:41:30Z | plan | BUG-0001 | Created, deciding the handler contract that fixes BUG-0001: a handler returns its success line and `main` prints it after the save succeeds. |
