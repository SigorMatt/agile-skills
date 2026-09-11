---
title: Ship a package with a repository-root shim, and no installation step
version: 2
status: current
updated: 2026-09-11T02:43:44Z
updated-by: implement
updated-for: WI-0001
---

# ADR-0004 — Ship a package with a repository-root shim, and no installation step

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder chose the name `envel` over `envelope` because *"Short is what matters if I'm
typing it several times a day"* [src: EP-001/Q-006], and `WI-0001`'s criteria are written as
invocations of it — `envel new <name>`, `envel add <name> <amount>`, `envel list`
[src: WI-0001 AC1 "creates an envelope called"]. Nothing in the epic says how that name gets onto a `PATH`, and a criterion
that cannot be run is not decidable, so somebody has to decide how the thing is started.

## Options considered

- **A — a `pyproject.toml` with a console script**, run after `pip install -e .`. Cost: a
  packaging file, and a verification step that needs a working index or at least a writable
  environment. Risk: the criteria become undemonstrable anywhere `pip install` cannot run, which
  is a poor property for a tool whose only constraint is *"Python, no services"* [src: EP-001].
- **B — a single script file** containing the whole tool. Cost: none at first. Risk: one module
  for parsing, money, the store and the commands; the epic has five more items to add to it.
- **C — a package plus an executable shim at the repository root.** Cost: two entry points to
  keep in step — though the shim is a delegation and has no logic to drift. Risk: `./envel` is
  not `envel` until the user puts it on their `PATH`, which is a step this item does not do for
  them.

## Decision

Option C. The tool is the package `envel/`, and there are two ways to start it, both reaching
the same `main`:

- `python3 -m envel …`, via `envel/__main__.py`;
- `./bin/envel …`, an executable file whose body puts the repository root on `sys.path`,
  imports `envel.cli.main` and calls it under `sys.exit` [src: bin/envel].

Installing it — putting `envel` on a `PATH` — is the user's step and is out of scope for this
item. Where a criterion says `envel`, it means the tool's command line, exercised in this
repository as `./bin/envel` [src: bin/envel].

No third-party packaging or dependency is introduced [src: ADR-0005].

## Consequences

Easy: every criterion is runnable from a clone with nothing installed, and the code is a package
from the first commit, so the five later items have somewhere to go.

Hard: two entry points exist, and someone will eventually add logic to the shim. The rule that
stops it is that the shim's body is a `sys.path` line, an import and a call — anything else
belongs in `cli.py` [src: bin/envel].

**Reversibility: easy.** Adding a `pyproject.toml` later is additive and changes nothing about
the package [src: tracker/items/WI-0001/artifacts/plan.md]; deleting the shim is one file.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-09-11T02:43:44Z | implement | WI-0001 | Two errata, recorded below: the shim is `bin/envel` rather than a file at the repository root, and its body carries a `sys.path` line as well as the import and the call. The decision — a package plus a shim, with no install step — is unchanged. |
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T02:43:44Z | implement | WI-0001 | erratum | Two clauses, one fact behind both: the shim cannot live at the repository root, so it lives at `bin/envel` and needs one line to find the package. (1) `## Decision`, second bullet, said *"`./envel …`, an executable file at the repository root whose entire body imports `envel.cli.main` and calls it under `sys.exit`"*, and the sentence below it said the criteria are *"exercised in this repository as `./envel`"*. Both are false against the filesystem: a directory and a file share one namespace, so `echo hi > envel` in a directory holding `envel/` fails with *"Is a directory"*. (2) `## Consequences` said *"the shim's body is an import and a call — anything else belongs in `cli.py`"*, which is false against the code because `bin/envel` is no longer beside the package and must put the repository root on `sys.path` first. Replaced with clauses naming `bin/envel` and that line [src: bin/envel]. The decision — a package, a shim, no install step — is unchanged, and no code has to change to satisfy the new text. |
