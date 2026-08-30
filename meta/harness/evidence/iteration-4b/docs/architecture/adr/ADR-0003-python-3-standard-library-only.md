---
title: Python 3 with the standard library only, tested with unittest
version: 1
status: current
updated: 2026-08-30T01:49:02Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — Python 3 with the standard library only, tested with unittest

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 is the first item to be planned and the repository contains no source code
[src: run: git ls-files | grep -v '^tracker/\|^docs/\|^.claude/' → .gitignore, CONSUMER-PROMPT.md, IDEA.md, SIMULATION-NOTICE.md].
Nothing constrains the language. `tracker/project.yaml` carried `commands.test: null` and
`commands.lint: null`, which `validate-workspace` reports as a warning against this skill
[src: tracker/project.yaml].

What the choice has to serve: a single person running a command at a terminal once a day
[src: EP-001/Q-001], nine acceptance criteria that are all "run a command and read what happened"
[src: WI-0001], and a verifier who must be able to run the gates on this machine.

What is actually installed was measured, not assumed:

- `python3` is present at 3.12.3 [src: run: python3 -V → Python 3.12.3].
- `pytest` is **not** installed [src: run: python3 -c 'import pytest' → ModuleNotFoundError: No module named 'pytest'].
- `ruff` is **not** installed [src: run: python3 -m ruff --version → No module named ruff].

## Options considered

- **A — Python 3, standard library only, tested with `unittest`.** Cost: `unittest` is more
  verbose than `pytest`, and the standard library gives no argument-parsing or storage
  conveniences beyond `argparse` and `json`. Risk: low — every part of it is already on the
  machine [src: run: python3 -V → Python 3.12.3; run: python3 -m unittest --help → exit 0].
- **B — Python 3 with `pytest` and `ruff`.** Cost: an install step before any gate can run,
  and this project's gates would then depend on network access or on a preinstalled virtualenv.
  Risk: a verifier on a clean machine cannot run `commands.test` at all, which turns a hard gate
  into an environment question.
- **C — A compiled language (Go, Rust).** Cost: a build step, a toolchain to install, and a
  larger distance between "the plan says add a function" and what a reviewer can check. Risk:
  nothing in the epic needs the performance, and the toolchain is not present.
- **D — A shell script.** Cost: JSON handling in POSIX shell needs an external tool such as
  `jq`, which is the dependency problem of B without B's benefits. Risk: the atomic-write and
  refuse-do-not-repair behaviour AC8 demands is fiddly and easy to get wrong in shell.

## Decision

**A.**

1. **Python 3, standard library only.** No third-party runtime dependency, at all, for the
   application. `argparse` for the command line and `json` for storage (see `ADR-0004`).
2. **`commands.test` is `python3 -m unittest discover -s tests -t . -q`.** Tests live in
   `tests/`, in files matching `test*.py`, which is `unittest`'s default discovery pattern.
   Measured behaviour of that exact command in this repository: exit 0 with a passing test, exit
   1 with a failing one, and exit **5** when no file matches the pattern
   [src: run: python3 -m unittest discover -s tests -t . -q, with one passing test → exit 0; with one failing test → exit 1; with tests/ holding only __init__.py → exit 5, "NO TESTS RAN"].
   The exit-5 case is why the plan's first step is to write a test.
3. **`commands.lint` is `python3 -m compileall -q recall tests`.** This is a syntax check, not
   a style linter, and it is recorded as such rather than dressed up: no style linter is
   installed, and making a hard gate depend on installing one would make the gate an environment
   question. Measured: exit 0 on the tree as it stands, exit 1 on a file with a syntax error
   [src: run: python3 -m compileall -q recall tests → exit 0; with a deliberately malformed tests/_bad.py → exit 1].
4. **Layout.** The package is `recall/` at the repository root, so it is importable from the
   root with no path configuration; tests are in `tests/`. How the `recall` command itself
   reaches `PATH` is `ADR-0005`.

## Consequences

- Every gate this project declares runs on a clean machine with nothing installed but Python 3
  [src: tracker/project.yaml; run: python3 -m unittest discover -s tests -t . -q, with one passing test → exit 0; run: python3 -m compileall -q recall tests → exit 0].
  That is the property being bought, and it is worth more here than `pytest`'s ergonomics.
- Tests are more verbose. `unittest` has no fixtures and no parametrisation, so the subprocess
  helpers the acceptance criteria need will be written by hand once and reused.
- `commands.lint` catches syntax errors and nothing else. It will not catch an unused import, a
  shadowed name or a style drift, and no one should read a green lint gate as more than it is.
  If a style linter is later installed, replacing the command is a one-line change to
  `tracker/project.yaml` and a superseding ADR.
- **Reversibility: high.** Swapping `unittest` for `pytest` is a change to test files and one
  line of `tracker/project.yaml`; no application code imports either. Changing language is not
  reversible in any useful sense, which is why the option list above is explicit about why the
  other three were rejected.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T01:49:02Z | plan | WI-0001 | First version: language, test command, lint command and layout, each measured on this machine |
