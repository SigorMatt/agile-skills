---
title: The project's test and lint commands use only the standard library
version: 1
status: current
updated: 2026-09-11T02:34:57Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0005 — The project's test and lint commands use only the standard library

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` arrived with `commands.test` and `commands.lint` both null, which
`validate-workspace` reports as a warning saying the tests-pass gate will be recorded as skipped
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 0, 1 warning
project.commands.test-null]. Filling them in is this skill's job, and choosing a test framework
is a decision rather than a detail.

What is actually available was measured rather than assumed: `which pytest ruff flake8 pylint
mypy` finds none of them on this machine
[src: run: which pytest ruff flake8 pylint mypy → exit 1, no output], and the stakeholder's
constraint is *"Python, no services"* [src: EP-001].

## Options considered

- **A — `pytest` and `ruff`.** Cost: a dependency file and an install step before any gate can
  run. Risk: neither is installed here
  [src: run: which pytest ruff flake8 pylint mypy → exit 1, no output], so the commands recorded in `project.yaml` would be
  commands nobody has run — which is the thing the `project-commands-resolved` gate exists to
  refuse.
- **B — `unittest` for tests and no lint command at all**, with this ADR recording why. Cost:
  none. Risk: the lint gate is then honestly recorded as skipped for ever, and a syntax error in
  a file no test imports goes unnoticed.
- **C — `unittest` for tests and `compileall` for lint.** Cost: none; both ship with Python.
  Risk: `compileall` checks that every module parses and nothing else — no style, no unused
  names, no types. Recording it as "lint" overstates it unless what it does is written down.

## Decision

Option C.

- `commands.test`: `python3 -m unittest discover -s tests -t .`
- `commands.lint`: `python3 -m compileall -q envel tests`

What the lint command **does** check is that every file under `envel/` and `tests/` compiles
[src: run: python3 -m compileall -q envel tests → exit 0]. It
does not check style, imports, dead code or types, and no gate in this project should be read as
claiming it does.

The test command exits 5 while no test exists
[src: run: python3 -m unittest discover -s tests -t . → exit 5, NO TESTS RAN], which is correct
behaviour for an empty suite and becomes exit 0 as soon as `implement` writes the first test.

## Consequences

Easy: both commands run from a clone with nothing installed, which is the same property
`ADR-0004` [src: ADR-0004] gives the tool itself.

Hard: the project has no style or type checking, so review is the only thing catching what a
linter would. If a linter is ever installed, this ADR is the one to supersede.

**Reversibility: easy.** Two lines in `tracker/project.yaml` [src: tracker/project.yaml] and a
superseding ADR. No code depends on either command.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version |
