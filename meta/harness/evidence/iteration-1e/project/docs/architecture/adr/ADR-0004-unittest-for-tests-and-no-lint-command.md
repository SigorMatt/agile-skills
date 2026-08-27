---
title: Test with unittest from the standard library, and declare no lint command
version: 1
status: current
updated: 2026-08-26T23:52:03Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — Test with unittest from the standard library, and declare no lint command

- **Status:** accepted
- **Date:** 2026-08-26
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` arrived with `commands.test`, `commands.lint` and `commands.build` all
`null`, and `validate-workspace` warns that the `tests-pass` gate will be recorded as skipped
until this skill sets them [src: run: python3 .claude/agile-skills/scripts/validate-workspace . →
exit 0, 0 errors, 1 warning project.commands.test-null]. `plan`'s contract makes filling them in
part of this job, and permits an ADR instead only where the project genuinely has none.

The binding constraint is the stakeholder's: python3 and its standard library, no external
services, no network [src: IDEA.md; tracker/items/EP-001/item.md]. Installing anything from an
index is not available, so the choice is between what ships with Python and nothing.

## Options considered

- **A — `unittest` for tests; no lint command.** Cost: `unittest` is more verbose than `pytest`
  and its discovery needs a `tests/__init__.py`. Risk: none to the constraint — it ships with
  Python.
- **B — `pytest` for tests, and `ruff` for lint.** Cost: both are installs. Risk: it breaks the
  stakeholder's stated constraint on the first `pip install`, and EP-001's fourth success measure
  requires the commands to work on a machine with no network
  [src: tracker/items/EP-001/item.md].
- **C — Declare `python3 -m compileall -q .` as the lint command.** Cost: none. Risk: this is the
  failure the `project-commands-resolved` gate names — a command that exits zero without checking
  anything worth checking. It reports that the files parse, which running the tests already
  proves, and it would read on the board as "linting passes".

## Decision

`commands.test` is:

    python3 -m unittest discover -s tests -t .

It was run in this project before being declared, twice. Against the empty `tests/` directory
this plan leaves behind, it reports no tests and exits non-zero
[src: run: python3 -m unittest discover -s tests -t . → exit 5, "Ran 0 tests ... NO TESTS RAN"],
which is the correct answer while no test exists and is what `implement` will turn green. With a
one-assertion test file temporarily present, the same command discovered and ran it
[src: run: python3 -m unittest discover -s tests -t . → exit 0, "Ran 1 test ... OK"]; that file
was then removed, because `plan` does not write tests.

Discovery requires the start directory to be importable, so `tests/__init__.py` exists and is
empty; it is recorded as scaffolding in the plan
[src: tracker/items/WI-0001/artifacts/plan.md].

`commands.lint` stays `null`, and this ADR is the record of why: the standard library ships no
linter [src: run: python3 -c 'import ruff' → exit 1, ModuleNotFoundError], the project may not
install one [src: tracker/items/EP-001/item.md], and declaring a command that checks nothing
would make a skipped gate look like a passing one
[src: .claude/skills/plan/references/contract.md]. Every skill that runs the lint gate will record it as
`skipped`, citing this ADR, which is the honest outcome.

`commands.build` stays `null`. There is nothing to build: the deliverable is run with
`python3 -m expenses` and has no packaging step in this epic
[src: tracker/items/WI-0001/artifacts/plan.md].

## Consequences

Easy: tests run anywhere python3 does, with no setup. The gate records what actually happened.

Hard: style drift has no automated check, so it is reviewed by a person or not at all. If the
constraint is ever lifted, `ruff` is the obvious candidate and this ADR should be superseded
rather than edited.

**Reversibility: high.** Both are one line in `tracker/project.yaml`
[src: tracker/project.yaml]. Test files written for `unittest` also run under `pytest`, so option
B remains open if the constraint changes.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-26T23:52:03Z | plan | WI-0001 | First version |
