---
title: envel runs from a launcher script, with no install step
version: 1
status: current
updated: 2026-09-10T13:44:29Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0002 — `envel` runs from a launcher script, with no install step

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Every acceptance criterion on WI-0001 is written as a command typed at a terminal —
`envel new groceries`, `envel list` [src: WI-0001 AC1 "exits 0 and writes nothing to stderr"].
For those criteria to be observable, something called `envel` has to be executable. Nothing in
the item says how it gets there, and the choice decides what a verifier has to do before they can
run a single criterion.

ADR-0001 rules out depending on anything that is not in the standard library, which removes the
usual answer of a packaging tool that installs an entry point.

## Options considered

- **A — A `pyproject.toml` console script, installed with `pip install -e .`.** Cost: an install
  step before a criterion can be run, a build backend, and a virtual environment to keep the
  install out of the system interpreter. Risk: the install is the first thing to break on a
  machine without an index, and it makes the criteria depend on a step they do not mention.
- **B — An executable launcher committed at `bin/envel`, put on `PATH`.** Cost: the user adds one
  directory to `PATH`, and it provides neither version metadata nor an uninstall. Risk: the
  launcher has to find the package next to itself rather than through an installed location.
- **C — `python3 -m envel` with a shell alias.** Cost: the alias is per-shell configuration that
  lives outside the repository, so the criteria would be observable just in a shell somebody had
  configured. Risk: what is being verified stops being the thing that was committed.

## Decision

Option B. The repository contains an executable file `bin/envel` with a `#!/usr/bin/env python3`
shebang. It resolves the repository root from its own location, puts it at the front of
`sys.path`, imports `envel.cli`, and exits with what `main()` returns — four statements, with
the tool's behaviour living behind that import.

A demonstration of an acceptance criterion therefore begins by putting `bin/` on `PATH`:

```
PATH="$PWD/bin:$PATH" ENVEL_FILE=<a store path> envel new groceries
```

## Consequences

- A fresh clone can run the tool immediately, which is what makes the criteria observable without
  a setup step that none of them mentions.
- The launcher carries no `.py` extension, so `commands.lint` does not reach it (ADR-0001). What
  covers it instead is that every end-to-end test invokes the tool through it, so a launcher that
  will not parse fails the test run.
- There is no version metadata, no uninstall, and nothing that would let two versions coexist on
  one machine. For one person on their own machine that is the whole of what is needed
  [src: docs/product/vision.md].
- **Reversing this is cheap.** Adding a `pyproject.toml` with a console-script entry point later
  is additive: `bin/envel` keeps working, nothing about the store changes, and the only thing that
  moves is how the command gets onto `PATH`. One new file and a line in the project's own
  instructions.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T13:44:29Z | plan | WI-0001 | First version: `bin/envel` as the launcher, and why not packaging or an alias |
