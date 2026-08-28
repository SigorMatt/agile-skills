---
title: The project's test and lint commands, and why there is no style linter
version: 3
status: current
updated: 2026-08-27T20:36:57Z
updated-by: review-close
updated-for: BUG-0003
---

# ADR-0004 — The project's test and lint commands, and why there is no style linter

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` had `commands.test`, `commands.lint` and `commands.build` all `null`, which
`validate-workspace` reports as a warning on every run: a null test command means the `tests-pass`
gate is recorded as skipped rather than passed
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 0, 1 warning
project.commands.test-null]. `plan` owns filling these in, and ADR-0001 already
fixed the runtime and the intended test runner but deliberately left `project.yaml` alone until a
`tests` directory existed to run against.

ADR-0001 confines the project to the Python standard library, for a reason the stakeholder gave:
they asked for whatever is easiest to build and test [src: EP-001/Q-001]. That rules out every
style linter — `ruff`, `flake8`, `pylint` and `black --check` are all third-party.

## Options considered

- **A — `unittest` for tests, `compileall` as the lint command, no style linter.** Cost: style is
  enforced by review rather than by a tool, so it can drift. Risk: low; `compileall` catches the
  class of error that would otherwise reach `verify` as a confusing failure — a syntax error in a
  module no test happens to import.
- **B — `unittest` for tests, `commands.lint: null` with this ADR recording why.** Cost: the lint
  gate is honestly recorded as skipped on every execution. Risk: a syntax error in an unimported
  module is caught by nothing.
- **C — Adopt `ruff`.** Cost: contradicts ADR-0001, and adds an install step to a project whose
  selling point is that it needs none. Risk: it would have to be either vendored or installed,
  and the stakeholder would meet a setup failure before they met the tool.

## Decision

```yaml
commands:
  test: python3 -m unittest discover -s tests -t . -q
  lint: python3 -m compileall -q tidy tests
  build: null
```

- `-t .` sets the top-level directory so `tests` can `import tidy` from the repository root.
- `commands.lint` is a **syntax check, not a style check**, and this ADR is the record of that
  [src: ADR-0004]: anything reading a passing lint gate on this project should read it as "every
  module compiles", not as "the code conforms to a style". Style is a matter for `review-close`.
- `commands.build` stays `null`, honestly: there is nothing to build. A Python package run with
  `python3 -m tidy` has no build step, and inventing one would make a gate report a pass for work
  nobody does.

## Consequences

What becomes easy: both gates are real commands that run in this repository from the first commit,
so `implement` and `review-close` report evidence rather than skips.

What becomes hard: nothing yet. If the codebase grows to where style drift matters, reversing this
means adopting a third-party linter, which means superseding ADR-0001 first — that is the decision
with the weight, not this one.

**Superseded by fact, 2026-08-27.** `implement` wrote WI-0001's tests, so the paragraph below no
longer describes this repository: `tests/` holds four test modules and two helpers, and
`python3 -m unittest discover -s tests -t . -q` exits **0** with the whole suite passing
[src: run: python3 -m unittest discover -s tests -t . -q → exit 0, "Ran 69 tests ... OK";
src: tests/test_cli.py]. It happened exactly as this note predicted; it is kept rather than
deleted because the reasoning — a project claiming a test command it cannot satisfy should fail,
not pass — is the part worth having.

The standing claim here is the **exit status**, not a test count. It said "runs 37 tests" from
WI-0001 until BUG-0003, and three items in between — WI-0002, BUG-0001 and BUG-0002 — each added
tests without anyone noticing the number had gone false; the count in the citation above is a
dated measurement, taken while closing BUG-0003, and every later item is expected to move it
[src: tests/test_cli.py].

Note on what the test command did **when this ADR was written**: `tests/` contained only an empty package marker, so
`python3 -m unittest discover -s tests -t . -q` reports `NO TESTS RAN` and exits **5**
[src: run: python3 -m unittest discover -s tests -t . -q → exit 5, "NO TESTS RAN"]. It is
recorded here rather than smoothed over, and it is the right behaviour: a project that claims a
test command and has no tests should not report success. It becomes a passing gate the moment
`implement` writes the first test, which the plan for WI-0001 requires before any criterion can be
demonstrated. Nothing runs this command between now and then — the `tests-pass` gate belongs to
`implement` and `review-close`.

Reversibility: **trivial** for the two commands — they are two lines in `tracker/project.yaml`,
and the only things that depend on their values are the gates that run them
[src: tracker/project.yaml].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-27T20:36:57Z | review-close | BUG-0003 | D12 audit at close: "runs 37 tests" had been false since WI-0002 and this item made it 69. The standing claim is now the exit status, with the count marked as a dated measurement |
| 2 | 2026-08-27T16:40:00Z | review-close | WI-0001 | D12 audit at close: the \"NO TESTS RAN, exit 5\" note had become false. Marked it superseded by fact and recorded the command's actual outcome |
| 1 | 2026-08-27T16:03:05Z | plan | WI-0001 | First version |
