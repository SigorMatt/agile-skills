---
title: A bin/recall launcher on PATH, with no install step
version: 1
status: current
updated: 2026-08-30T01:50:04Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0005 — A `bin/recall` launcher on PATH, with no install step

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Every acceptance criterion on WI-0001 is written as a literal invocation of `recall`
[src: WI-0001 AC1]. Refinement routed "how `recall` is put on `PATH` so that a verifier can run
the criteria literally" to this skill, and flagged it as mattering more than it looks
[src: tracker/items/WI-0001/artifacts/refinement-qa.md]. `ADR-0001` fixed the command's shape and
left this open [src: ADR-0001].

`ADR-0003` chose the standard library and no third-party dependency
[src: ADR-0003], which rules out anything that needs a package installed to run.

## Options considered

- **A — An executable `bin/recall` launcher, documented as "put `<repo>/bin` on your `PATH`".**
  Cost: the person has to add one directory to `PATH` once, and the documentation AC7 already
  requires has to say so. Risk: none to the gates — a test invokes the CLI as a subprocess with
  `bin/` prepended to `PATH`, so it runs exactly the string the criteria name
  [src: WI-0001 AC1; tracker/items/WI-0001/artifacts/plan.md].
- **B — A `pyproject.toml` with a `console_scripts` entry point, installed with
  `pip install -e .`.** Cost: an install step before anything runs, and a virtualenv or a
  `--user` install to avoid touching the system Python. Risk: the gates then depend on an
  environment somebody set up, which is the failure `ADR-0003` chose against.
- **C — Tell the person to run `python3 -m recall`.** Cost: nothing to build. Risk: it
  contradicts nine acceptance criteria that say `recall`, and rewriting them to match the
  implementation would be reshaping the target around the arrow.

## Decision

**A.**

1. **`bin/recall`** is an executable file with a `#!/usr/bin/env python3` shebang. It puts the
   repository root on `sys.path`, imports `recall.cli`, and calls its entry function with the
   process's arguments. It contains no application logic — everything it could contain belongs in
   the package, where it can be unit-tested without a subprocess
   [src: docs/architecture/overview.md; tracker/items/WI-0001/artifacts/plan.md].
2. **The documentation states the one setup step**: add `<repo>/bin` to `PATH`. The same document
   states the deck file's path, which AC7 requires.
3. **`python3 -m recall` also works**, because `recall/__main__.py` calls the same entry function.
   It is a convenience for anyone who would rather not touch `PATH`; it is not what the criteria
   are written against and it is not what the tests exercise.
4. **Tests invoke the CLI as a subprocess**, with `bin/` prepended to `PATH` and `HOME` pointed at
   a temporary directory. That is what makes an acceptance criterion and the test that
   demonstrates it the same observation rather than two things that resemble each other.

## Consequences

- A verifier with a checkout and Python 3 can run every criterion after exporting one variable.
  No install, no network, no virtualenv.
- Running the CLI as a subprocess in every test is slower than calling a function, and gives a
  worse failure message when something breaks — an exit code and two streams rather than a stack
  trace. That is the price of testing what the criteria actually say, and it is worth paying
  here because the criteria are the contract.
- The tool is not installable in the ordinary Python sense, so it cannot be published to an index
  or installed by a package manager. Nobody has asked for that; the epic is one person on one
  machine [src: EP-001/Q-001].
- **Reversibility: high.** Adding a `pyproject.toml` with a `console_scripts` entry point later
  changes nothing about the package's contents — `bin/recall` and the entry point would call the
  same function — and the tests would keep working unchanged.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T01:50:04Z | plan | WI-0001 | First version: a bin/recall launcher rather than an installed entry point |
