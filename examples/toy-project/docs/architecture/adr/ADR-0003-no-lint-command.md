---
title: The project has no lint command, and no build command
version: 1
status: current
updated: 2026-08-16T21:33:10Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — The project has no lint command, and no build command

- **Status:** accepted
- **Date:** 2026-08-16
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`tracker/project.yaml` ships with `commands.test`, `commands.lint` and `commands.build` all
`null`, and `plan` must either fill each in with a command that really runs here or record why
the project has none. `implement`'s `lint-clean` gate runs `{{commands.lint}}`; a `null` value
makes it report **skipped**, which is honest, while a command that exits 0 without checking
anything would report a pass for a check nobody ran.

`commands.test` is not in question: WI-0001 AC13 fixes it as `python3 -m unittest discover` from
the repository root, and it is set to that.

The constraint that decides the other two is the product's, not the developer's: EP-001 puts
"any third-party dependency, for running the tool or for running its tests" out of scope, and
`docs/product/vision.md` makes "nothing to install" a property of the product. Nothing that
lints Python ships with CPython. Checked on this machine at planning time: `ruff`, `flake8`,
`pyflakes` and `pylint` are all absent, so a lint command naming one would fail the
`project-commands-resolved` gate's "a command that does not exist" clause immediately.

## Options considered

- **A — `commands.lint: null`, with this ADR.** Cost: the `lint-clean` gate is recorded as
  skipped on every `implement` run of every item, forever. Risk: a style problem no test catches
  goes unnoticed; for one file of roughly a hundred lines, read at review, that is a small
  exposure.
- **B — `python3 -m compileall -q linecount.py tests` as a stand-in linter.** Cost: it writes
  `__pycache__` directories as a side effect, so a gate would dirty the working tree. Risk: it
  reports a passing lint while checking only that the files parse — which the test command
  already proves, since `unittest discover` imports every module in the suite and the suite
  imports `linecount`. A gate whose result is implied by another gate is decoration, and this
  one would be decoration labelled "lint-clean".
- **C — adopt a third-party linter and add a dev dependency.** Cost: a dependency manifest, an
  install step, and a project that no longer runs on "only Python 3". Risk: it contradicts
  EP-001's out-of-scope list and the vision, which only the human may authorise.

## Decision

**Option A.** `commands.test: python3 -m unittest discover`. `commands.lint: null` and
`commands.build: null`, with this ADR as the record of why.

`build` is `null` for a simpler reason than `lint`: there is nothing to build. The deliverable
is a source file that is run directly, so no build step exists to name.

Reviewers should expect to see `lint-clean` reported as **skipped**, with this ADR as the
reason, in every `implement` journal entry in this project. A `lint-clean` reported as **pass**
would be the anomaly worth investigating.

## Consequences

- Style is enforced by review, not by a tool. `review-close` reads the diff; there is no second
  opinion from a linter behind it.
- Every `implement` execution carries a skipped gate. That is visible in the journal by design —
  the record shows what was not checked rather than hiding it behind a green gate.
- **Reversibility: cheap, and it is the kind of decision expected to be revisited.** Reversing it
  is one line in `tracker/project.yaml` plus whatever install step the chosen tool needs. No code
  and no test depends on it. What is *not* cheap to reverse is option C's premise — making the
  project depend on an installed tool — because that contradicts a product constraint, so
  reversing this ADR toward C needs the human, while reversing it toward a stdlib-only checker
  does not.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T21:33:10Z | plan | WI-0001 | First version |
