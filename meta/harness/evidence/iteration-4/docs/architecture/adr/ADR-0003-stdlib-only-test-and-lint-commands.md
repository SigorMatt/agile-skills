---
title: Test with the standard library's unittest, and gate syntax with compileall
version: 1
status: current
updated: 2026-08-29T11:16:00Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — Test with the standard library's `unittest`, and gate syntax with `compileall`

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` carries `commands.test: null` and `commands.lint: null`, which the
workspace validator reports as a standing warning: a null command is honest, and it means the
tests-pass gate is recorded as skipped rather than passed
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → 0 errors, 1 warning: project.commands.test-null].
WI-0001 is the first item to be planned, so choosing what those commands are is part of this
execution [src: WI-0001].

What is available was measured rather than assumed. The interpreter is Python 3.12.3
[src: run: python3 -V → Python 3.12.3]. `pytest` is not importable
[src: run: python3 -c "import pytest" → ModuleNotFoundError: No module named 'pytest'], and no
`ruff`, `flake8` or `pyflakes` is on the path
[src: run: which ruff flake8 pyflakes → no output]. The interpreter is an
externally-managed environment, so installing one with `pip` into it is refused
[src: run: python3 -m pip install --user ruff → error: externally-managed-environment, PEP 668].
A package can still be downloaded, so the network is reachable
[src: run: python3 -m pip download ruff -d /tmp/x → Successfully downloaded ruff]; what is not
available is a supported way to put it where a bare `ruff check .` would find it.

This matters beyond convenience. `verify` and `review-close` run the declared commands as gates,
and a gate command that is absent on the machine that runs it fails the item rather than the
code [src: WI-0001].

## Options considered

- **A — stdlib `unittest`, and `compileall` as the syntax gate.** Cost: `compileall` is a
  compile check, not a linter — it catches syntax and indentation errors and nothing else, so
  unused imports, shadowed names and dead code pass it silently. Risk: low; both commands ship
  with the interpreter, so they run wherever the tool itself runs.
- **B — a virtual environment holding `pytest` and `ruff`.** Cost: a `.venv/` directory that
  every later skill must create before it can run a gate, on every machine, plus a network fetch
  in a pipeline whose other gates need none. Risk: medium — the gate then fails when the network
  is down, and the failure looks like a defect in the item under test.
- **C — `pip install --break-system-packages`.** Cost: modifies the system interpreter of the
  machine the pipeline happens to be running on, for a toy single-file tool. Risk: high, and out
  of proportion to what is being built.
- **D — declare that the project has no test command and record why.** Cost: WI-0001 has nine
  acceptance criteria that are all decided by running a command and reading its output
  [src: WI-0001 AC1; WI-0001 AC9], so there is plainly something to automate; declaring
  otherwise would be false. Risk: high — the tests-pass gate would be recorded as skipped for
  the whole epic.

## Decision

Option A.

- `commands.test` is `python3 -m unittest discover -s tests -t .`, run from the repository root.
- `commands.lint` is `python3 -m compileall -q -x '[.]claude' .`, which compiles every `.py`
  file in the repository except the pipeline's own installed scripts under `.claude/`.
- Tests live in `tests/`, are written with `unittest`, and drive the delivered command as a
  subprocess where the criterion is about exit codes and output — which, on WI-0001, is all nine
  of them [src: WI-0001].
- No third-party package is a dependency of this project, for running it or for testing it.

Two properties of the chosen commands were checked rather than assumed. `unittest discover`
exits **5**, not 0, when it finds no test at all
[src: run: python3 -m unittest discover -s tests -t . (empty tests package) → NO TESTS RAN, exit 5],
so the test gate cannot pass by finding nothing — it fails until `implement` writes the first
test. And `compileall` exits 1 on a file that does not parse and 0 on one that does
[src: run: python3 -m compileall -q over a file with an unclosed bracket → Error compiling ./bad.py, exit 1].

## Consequences

What becomes easy: any machine with Python 3 can run both gates with nothing installed and no
network. The tests are subprocess-level, so they check the same surface the acceptance criteria
name — the command, its output and its exit code [src: WI-0001 AC1].

What becomes hard: style and dead-code problems that a real linter finds will reach review
unflagged, and the reviewer is the only thing catching them. `compileall` is named `lint` in
`tracker/project.yaml` because that is the slot the pipeline reads; it is weaker than the name
suggests, and this paragraph is the warning [src: WI-0001].

**Reversibility: high.** Both are one line in `tracker/project.yaml` [src: tracker/project.yaml].
Adopting `pytest` later costs nothing in the test files themselves — `pytest` runs
`unittest`-style cases unchanged — and adopting a real linter is a change to that one line plus
whatever it then reports.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:16:00Z | plan | WI-0001 | First version: stdlib unittest as the test command and compileall as the lint command, with the measurements that ruled out pytest and ruff |
