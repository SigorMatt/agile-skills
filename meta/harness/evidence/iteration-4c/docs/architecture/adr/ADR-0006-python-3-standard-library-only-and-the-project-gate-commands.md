---
title: Python 3 with the standard library only, and the project's own gate commands
version: 1
status: current
updated: 2026-08-30T11:55:01Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0006 — Python 3 with the standard library only, and the project's own gate commands

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 is the first item to be planned, and nothing in the repository is product code yet
[src: WI-0001]. Two things have to be settled before a line of it is written: what the tool is
built in, and what `tracker/project.yaml` names as this project's test and lint commands — which
`plan` is required to fill in rather than leave null.

The constraints in play are narrow and all recorded. The surface is a command-line tool run by
one person at a terminal [src: ADR-0001]. The technology was delegated: *"As for how it's
actually built — whatever you think is best."* [src: EP-001/Q-004] The storage is a file on the
local machine, readable as text [src: ADR-0004]. Nothing in any item asks for concurrency, a
network, a database, or a package to be published.

The environment this project is developed in was read rather than assumed. `python3 --version`
reports 3.12.3 [src: run: python3 -V → Python 3.12.3]. The interpreter is externally managed in
the PEP 668 sense, so `python3 -m pip install <tool>` refuses without either a virtual
environment or `--break-system-packages`
[src: run: python3 -m pip install --dry-run ruff → error: externally-managed-environment]. A
network is reachable, so a virtual environment with a third-party linter *could* be created
[src: run: python3 -c urllib.request.urlopen('https://pypi.org/simple/ruff/') → HTTP 200].

That last fact is what makes the lint command a real decision rather than a forced move.

## Options considered

- **A — Python 3, standard library only; `unittest` for tests and `compileall` for lint.**
  Cost: the lint command checks that every source file parses and compiles and nothing more —
  it does not see an unused import, an undefined name, or a style violation. Risk: a class of
  defect a real linter would catch has to be caught by review and by tests instead.
- **B — Python 3, with a virtual environment holding a pinned third-party linter** (`ruff` or
  `flake8`), lint being `.venv/bin/ruff check .`. Cost: an environment-setup step that every
  later execution depends on, and roughly thirty megabytes of third-party code inside a project
  whose product is one text file and a few hundred lines. Risk: the higher one. `implement`,
  `verify` and `review-close` each run the lint command from `tracker/project.yaml`; on any
  checkout where the virtual environment has not been recreated the command does not exist, and
  a missing gate command costs a round trip through a question to a stakeholder who is not the
  cause of it. The gate would be stronger and less reliable.
- **C — A compiled language** (Go, Rust), which brings a formatter and a vetting tool in the
  toolchain. Cost: a build step, and neither toolchain is installed here. Risk: it buys
  distribution properties — a single static binary — that nobody asked for, for one person on
  one machine [src: ADR-0001].

## Decision

**The tool is written in Python 3, using the standard library only.** No third-party runtime
dependency, and no third-party development dependency. Basis: the delegation
[src: EP-001/Q-004], an interpreter already present at 3.12.3
[src: run: python3 -V → Python 3.12.3], and a product whose entire I/O is argument parsing and
one text file [src: ADR-0004].

**The package lives at the repository root** as `recall/`, run as `python3 -m recall`, so that no
installation step stands between a checkout and a working command [src: recall/__init__.py].

**`commands.test` is `python3 -m unittest discover -s tests -t . -q`.** Discovery is rooted at
the repository so test modules import as `tests.*` and can `import recall` without a path shim
[src: tests/__init__.py]. Run against the empty suite that exists at the time of this decision it
exits 5 with `NO TESTS RAN`
[src: run: python3 -m unittest discover -s tests -t . -q → exit 5, NO TESTS RAN], which is the
honest result: the command works and the project has no tests yet. WI-0001's implementation is
what makes it exit 0.

**`commands.lint` is `python3 -m compileall -q recall tests`**, which exits zero when every
module under those two directories compiles
[src: run: python3 -m compileall -q recall tests → exit 0]. This ADR states plainly what that
gate does and does not check, so that no later reader mistakes a green lint for a stronger
statement than it is: it catches a syntax error and a file that cannot be imported at all; it
does not catch an unused import, an undefined name, or a formatting inconsistency.

**`commands.build` stays null.** There is nothing to build: the tool is run from source with the
interpreter that is already installed [src: run: python3 -V → Python 3.12.3]
[src: recall/__init__.py].

## Consequences

Easy: a checkout runs and is tested with nothing installed, which is what makes the pipeline's
own gates dependable across the sessions that will run them. Every acceptance criterion on
WI-0001 is checkable with `python3` and a text tool, which is the shape the criteria were written
in [src: WI-0001 AC2].

Hard: the lint gate is weak, and this ADR is where that is written down rather than discovered
later. Defects it would have caught — a name that is never defined on a path no test exercises —
have to be caught by the tests and by review. If that turns out to be insufficient, option B is
what to reach for.

Reversibility: **cheap, in both parts.** Adding a linter later is a virtual environment, a pinned
version, one line in `tracker/project.yaml` and a superseding ADR; no code changes and no data
moves. Changing language is not cheap, but nothing about the stored file depends on it — the card
file is plain text with no language-specific encoding [src: ADR-0004] — so even that is a rewrite
of the tool, not a migration of the person's study history.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T11:55:01Z | plan | WI-0001 | First version: Python 3 standard library only, package at the repository root, and the test and lint commands recorded in `tracker/project.yaml` with what the lint command does not check. |
