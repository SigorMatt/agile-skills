---
title: Architecture overview
version: 2
status: current
updated: 2026-08-21T03:28:38Z
updated-by: implement
updated-for: WI-0001
---

# Architecture overview

The shape of the system, written when the first item was planned. It is deliberately small: this
is a single-user command-line tool with one data file and no network, and the main risk to it is
being built as though it were something larger.

## The whole system, in one paragraph

A Python package, run as `python3 -m expenses <command>`, that reads and writes one JSON file
holding a friend group's people and expenses, and prints reports derived from it. There is no
server, no database, no daemon, no configuration file and no third-party dependency
(`ADR-0001-python-baseline-and-no-dependencies.md`). Every command is a single process that
loads the store, does one thing, writes the store back if it changed, and exits.

## Layers

Four layers, each of which may only call downwards. The rule matters mainly at the top and the
bottom: nothing below `cli` may print anything or call `sys.exit`, and nothing above `store` may
know where the file lives or what format it is in.

```
python3 -m expenses …
        │
        ▼
  expenses/cli.py        argument parsing, exit codes, stdout vs stderr, formatting
        │
        ▼
  expenses/people.py     roster rules          expenses/expenses.py   recording (WI-0002)
  expenses/money.py      amounts as integers   expenses/balances.py   net positions (WI-0003)
        │                                      expenses/settle.py     payments      (WI-0003)
        ▼
  expenses/store.py      load, save, atomic write, damage detection, path resolution
                         (damage detection covers the file, the JSON, the top-level
                          shape, and the type of every roster entry — see below)
        │
        ▼
  one JSON file          ADR-0002
```

- **`cli`** owns everything a user sees. It is the only layer that writes to a stream or chooses
  an exit status. Errors reach it as exceptions carrying a message; it prints them on stderr and
  exits non-zero. This is what makes "no Python traceback ever reaches the user" (WI-0001 AC8, and
  EP-001's fourth success measure) a property of one function rather than a discipline applied
  everywhere — but only because that function has **two** handlers, and the second one is the
  load-bearing half:
  - `except ExpensesError` prints the message a domain module wrote for the person at the
    terminal. This is the path every *expected* failure takes.
  - `except Exception` is the backstop. It prints one line naming the exception type and message,
    says the failure is the tool's fault, and exits non-zero. `BaseException` is deliberately not
    caught, so `KeyboardInterrupt` and `SystemExit` are unaffected.

  Without the second handler the claim above would be false, and it was: until WI-0001's third
  implementation pass, a store whose `people` list held a non-string parsed cleanly and then
  raised `AttributeError` out of `people.normalise()`, which reached the user as a traceback and
  exit 1. Stating the property as a consequence of the layering alone is the mistake — the
  layering guarantees it only if **every** module below `cli` raises nothing but `ExpensesError`,
  which is the "discipline applied everywhere" this design set out not to depend on. See
  `tracker/items/WI-0001/artifacts/review.md` F1 and F3.
- **The domain modules** are pure: they take data and return data, and raise a domain exception
  when a rule is broken. They are where the acceptance criteria actually live, and they are
  testable without a filesystem or a subprocess.
- **`store`** is the only module that knows the file's path, its format, and how to write it
  without risking a half-written file. Everything above it sees a plain dictionary — and that is
  a promise `store` has to keep at the *element* level, not just the container level. Checking
  that `people` is a list, without checking that it holds strings, hands the layer above a
  dictionary it cannot use and turns a damaged file into a crash somewhere that has no idea it is
  looking at one. Every validation a caller would otherwise have to repeat belongs here, once.

## Why the domain is split by concept rather than by command

`people`, `expenses`, `balances` and `settle` correspond to the epic's four capabilities, not to
the four commands. Two consequences are load-bearing:

- **`balances` is separate from `settle`.** Net positions per person are computed by one module
  and turned into payments by another. `ADR-0005` requires this: settling up — recording that Bob
  actually paid Alice — is deferred to a later epic (`EP-001/Q-002`), and when it arrives it is
  one more transfer applied to the nets. If payments were computed straight from expense rows,
  every criterion in WI-0003 would still pass and that promise would be quietly broken.
- **`money` is separate from everything.** Amounts are integer minor units end to end
  (`ADR-0004`), and the conversion to and from the two-decimal text form happens in exactly one
  place. A second place that parses `"12.50"` is how the never-round rule (`WI-0002/Q-003`) gets
  lost.

## What is deliberately absent

- No configuration file, no environment beyond `EXPENSES_STORE` (`ADR-0002`), no logging
  framework, no plugin mechanism.
- No abstraction over the storage format. There is one format and one file; an interface with a
  single implementation would document a flexibility nobody asked for.
- No ORM, no schema migration tool. The store carries a `version` integer so that a future format
  change can be detected, and that is the whole of the provision made for it.

## Testing

`python3 -m unittest discover -s tests -t .`, standard library only (`ADR-0001`). Tests come in
two kinds and both are expected:

- **Domain tests** call the modules directly. Fast, and where the arithmetic is pinned down.
- **End-to-end tests** run the CLI in a subprocess with `EXPENSES_STORE` pointed at a temporary
  directory, and assert on stdout, stderr and the exit status. Several criteria — WI-0001 AC2
  ("a **fresh** process"), AC8 (no traceback) — are only meaningful at this level, because they
  are claims about the process boundary itself.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-21T03:28:38Z | implement | WI-0001 | Corrected the `cli` bullet: the no-traceback property rests on a second `except Exception` backstop, not on the layering alone. The v1 claim was false against the code — `review.md` F3 found it after a damaged store reached a user as an `AttributeError`. Also recorded that `store`'s damage detection reaches element types, not just container types |
| 1 | 2026-08-21T02:44:00Z | plan | WI-0001 | First version, written while planning the first item |
