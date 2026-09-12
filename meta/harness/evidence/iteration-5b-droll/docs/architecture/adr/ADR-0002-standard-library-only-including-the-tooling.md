---
title: Standard library only, including the test and lint tooling
version: 1
status: current
updated: 2026-09-11T21:58:28Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0002 — Standard library only, including the test and lint tooling

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` carried `commands.test: null` and `commands.lint: null`, which
`validate-workspace` reports as a warning on every run
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 0, WARNING project.commands.test-null]
and which `plan` is required to resolve before the first item is built. Choosing what runs the tests is a design decision, so it is
recorded here rather than typed into a configuration file.

What was actually available was measured rather than assumed:

- `pytest` is not importable on this machine
  [src: run: python3 -c "import pytest" → ModuleNotFoundError: No module named 'pytest'].
- The system interpreter refuses a direct install, as PEP 668 environments do
  [src: run: python3 -m pip install ruff → error: externally-managed-environment].
- A virtual environment can be created and a third-party linter installed into it, so the
  network is not the obstacle
  [src: run: python3 -m venv /tmp/.droll-probe && /tmp/.droll-probe/bin/pip install ruff → ruff on the venv's bin/].

So both options below are actually reachable, and the decision is about which one this project
should carry rather than about what the machine permits.

The product this serves is a single-user command-line dice roller that is started, typed at and
quit [src: EP-001/Q-001]. The vision records that it is not a library and that nothing else reads
its output [src: docs/product/vision.md].

## Options considered

- **A — standard library only: `unittest` for tests, `compileall` for the lint command.**
  Cost: the lint command checks that every module compiles and nothing else — no unused imports,
  no undefined names, no style
  [src: run: python3 -m compileall -q droll tests → exit 0 on clean sources, exit 1 on a module with an unclosed parenthesis]. Risk: a class of defect a real linter would name goes unnamed,
  and "lint passed" says less here than a reader may expect it to.
- **B — `pytest` and `ruff` installed into a project virtual environment, with
  `commands.lint: .venv/bin/ruff check droll tests`.**
  Cost: a setup step before any gate can run, and a network fetch to perform it. Risk: the venv
  is not in version control, so the gate commands stop existing in a fresh clone of this
  repository — and this pipeline reconstructs an item's story from `git log`, which means a later
  `verify` or `review-close` could find the command it is contractually required to run missing.
  That failure is silent in the worst way: the command is absent rather than failing.
- **C — leave the commands null and record that the project has no tests.**
  Cost: none up front. Risk: `WI-0001` has eleven acceptance criteria about observable behaviour
  and no automated way to check any of them stays true when `WI-0002` is built on top. Refused:
  the tests-pass gate would be recorded `skipped` for the whole engagement, which is an honest
  record of a bad choice rather than a good one.

## Decision

droll takes no third-party package, for the product or for its own tooling.

```yaml
commands:
  test: python3 -m unittest discover -s tests -t .
  lint: python3 -m compileall -q droll tests
```

- Tests are `unittest.TestCase` classes under `tests/`, discovered from the repository root. The
  discovery root is `.` so that `import droll` resolves during a test run without a package
  install.
- The lint command compiles every module under `droll/` and `tests/` and reports a non-zero exit
  on a syntax error. It was checked in both directions rather than only the passing one
  [src: run: python3 -m compileall -q droll tests → exit 0 on clean sources, exit 1 on a module with an unclosed parenthesis].
- The test command does **not** pass vacuously. With no test module present it exits 5, not 0
  [src: run: python3 -m unittest discover -s tests -t . → exit 5, "NO TESTS RAN"], so an
  implementation that ships no test cannot report a green tests-pass gate.

**What the lint command does not do, stated here so nobody has to infer it.** It is a syntax and
bytecode-compilation check. It will not report an unused import, an undefined name, a shadowed
builtin, a line length or any style question. A reviewer reading `lint → pass` in a journal entry
should read it as *"every module compiles"* and take the rest of the code read on themselves.

## Consequences

- `droll/` and `tests/` are importable packages, so each needs an `__init__.py`. `plan` created
  both as empty files, because neither command above can execute without them; they are listed
  under `## Scaffolding` in `tracker/items/WI-0001/artifacts/plan.md` and contain no behaviour
  [src: tracker/items/WI-0001/artifacts/plan.md].
- `implement` may write tests without installing anything, which is the property that makes the
  gates runnable in any later session on any machine with Python 3.
- A correctness defect that only a linter would catch has to be caught by a reader or by a test.
- **Reversible, cheaply, in one direction.** Adopting `pytest` later costs nothing that is
  written now: a `unittest.TestCase` runs unchanged under `pytest`, so the test suite is
  portable and the change is one line of `tracker/project.yaml` plus whatever installs it.
  Adopting `ruff` later is the same one line plus a fix-up pass over whatever it reports. What is
  not reversible for free is the opposite direction — code written against a third-party test
  framework's fixtures would have to be rewritten to come back — which is part of why A is
  chosen first.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T21:58:28Z | plan | WI-0001 | First version: the test and lint commands, and the decision that droll takes no third-party dependency for the product or for its tooling |
