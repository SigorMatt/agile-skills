---
title: Python 3 with the standard library only
version: 1
status: current
updated: 2026-09-10T13:44:29Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0001 — Python 3 with the standard library only

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder asked for "Python, no services" [src: EP-001/Q-001], and `docs/product/vision.md`
reads "no services" at its widest — no server, no daemon, no account, no sync, and no reason to
reach the network [src: docs/product/vision.md]. What it does not settle is whether the tool may
depend on packages from an index, which is a different question from whether it talks to a
network at runtime: installing a dependency is a network act at build time, and it is a step the
one person who uses this tool has to perform on every machine they want it on.

The decision has to be taken now rather than later, because it decides what
`tracker/project.yaml` can name as this project's test and lint commands, and `plan` is required
to record commands it has actually run.

What was read to establish the constraints: `docs/product/vision.md` v2, `tracker/project.yaml`,
and the interpreter and tooling actually present — `python3 -V` reports 3.12.3, and `pytest`,
`ruff`, `flake8` and `pyflakes` are all absent
[src: run: python3 -c "import pytest" → ModuleNotFoundError: No module named 'pytest'].

## Options considered

- **A — Standard library only.** No `pyproject.toml` dependency list, no virtual environment, no
  install step. Tests are `unittest`; the syntax check reachable without an install is
  `compileall` [src: run: which pytest ruff flake8 pyflakes → no output, exit 1].
  Cost: no third-party test runner, no real linter, and any convenience a library would have
  given has to be written or done without. Risk: the temptation later to reach for a package and
  quietly re-open this.
- **B — A small dependency set (`pytest`, `ruff`), installed into a virtual environment.**
  Cost: an install step that needs an index the first time, a `.venv` to keep working, and a
  second way to run the tool depending on whether the environment is active. Risk: the acceptance
  criteria are about typing `envel` at a terminal, and every layer between the terminal and the
  code is a layer that can be wrong on the stakeholder's machine and right on ours.
- **C — Standard library at runtime, third-party for development only.** Cost: the runtime stays
  clean but the gate commands stop working on a machine that has not run the install, which is
  the machine every verification of this project so far has run on. Risk: a test command recorded
  in `project.yaml` that a fresh checkout cannot execute.

## Decision

Option A. This project is written against the Python 3 standard library and declares no
third-party dependency, for its runtime, its tests or its checks.

Two consequences are written into `tracker/project.yaml` as commands, and both were run before
being recorded:

- `commands.test` is `python3 -m unittest discover -s tests -t .`
  [src: run: python3 -m unittest discover -s tests -t . → exit 5, "NO TESTS RAN"]. The exit-5 is
  the command reporting that it found nothing to run, which is the state the project is in until
  `implement` writes the tests.
- `commands.lint` is `python3 -m compileall -q envel tests`
  [src: run: python3 -m compileall -q envel tests → exit 1 on a file containing `def f(:`].

The second is a **syntax check and not a linter**, and it is recorded as one rather than dressed
up: it byte-compiles every `.py` file under `envel/` and `tests/` and fails on one that will not
parse [src: run: python3 -m compileall -q envel tests → exit 1 on a file containing def f(:]. It is the strongest check available without an install, and calling it `lint` in
`project.yaml` is a naming convention of the toolkit rather than a claim about its strength.

## Consequences

- The test command runs from a fresh clone with no setup beyond a Python 3 interpreter.
- `compileall` reports "Can't list" and still exits 0 when a directory it was given does not
  exist [src: run: python3 -m compileall -q envel tests nosuchdir → exit 0, "Can't list 'nosuchdir'"],
  so the lint command is silent about a package that has not been created yet. It becomes
  meaningful the moment `envel/` contains a file, and nothing rests on it before then.
- `bin/envel` (ADR-0002) has no `.py` extension, so `compileall` does not see it. It is a
  launcher of a few lines with no logic in it, and every end-to-end test invokes the tool
  *through* it, so a launcher that will not parse fails the test suite rather than passing the
  lint.
- **Reversing this is cheap and localised.** Adding a dependency means a `pyproject.toml`, an
  install step in the project's own instructions, and two edited lines in `tracker/project.yaml`.
  No data migrates and no interface the stakeholder sees changes. It is reversible; it is
  recorded as a decision anyway, because the alternative is each item re-deciding it in silence.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T13:44:29Z | plan | WI-0001 | First version: standard library only, and the test and lint commands that follow from it |
