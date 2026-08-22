---
title: The tool and its tests use the standard library only
version: 1
status: current
updated: 2026-08-22T02:06:34Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0005 — The tool and its tests use the standard library only

- **Status:** accepted
- **Date:** 2026-08-22
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

This is the first item planned in the project, so the questions "what runs the CLI", "what runs
the tests" and "what checks the code" have no answer yet, and `plan`'s preconditions make
answering the second one part of this job — `tracker/project.yaml` has `commands.test: null`
[src: tracker/project.yaml].

The constraints are already recorded. The stakeholder asked for Python and "no external services"
[src: IDEA.md]. The vision goes further: nothing hosted, nothing signed up for, and the tool
answers the same way with no network available [src: docs/product/vision.md]. Neither statement is
literally about *packages*, but a tool that cannot be run without first fetching dependencies from
an index is a step away from the thing they described.

What is actually installed here was checked rather than assumed: Python 3.12.3, and none of
`pytest`, `ruff`, `pyflakes` or `flake8`
[src: run: `python3 -V` → Python 3.12.3; run: `python3 -c "import pytest"` → ModuleNotFoundError].

## Options considered

- **A — standard library only, for the tool and for its tests.** `argparse` for the CLI,
  `unittest` for the tests, `json`, `datetime` and `os` for the rest. Cost: `argparse` is more
  verbose than `typer`, and `unittest` is more verbose than `pytest`. Risk: no style linter
  exists in the standard library, so the lint gate checks less than the word "lint" implies —
  addressed in the decision below. Benefit: `git clone` and run; no lockfile, no virtualenv, no
  install step for the operator or for `verify`.
- **B — `typer` or `click` for the CLI, `pytest` for the tests.** Cost: a dependency file, an
  install step before any gate can run, and an environment where neither is currently present.
  Risk: the pipeline's own `tests-pass` gate would fail on a clean checkout for reasons that have
  nothing to do with the code. Benefit: less boilerplate, better failure output from `pytest`.
- **C — standard library for the tool, `pytest` for the tests only.** Cost: the operator needs
  nothing, but `verify` and CI need an install. Risk: the split invites "it works on my machine"
  in precisely the skill whose job is to be independent. Benefit: keeps `pytest`'s ergonomics
  where they are most felt.

## Decision

**A.** No third-party package is imported by the tool or by its tests.

- **CLI:** `argparse` with subparsers. The tool is invoked as `python3 -m expenses …`, so the
  package directory is the entry point and there is nothing to install. No console-script entry
  point and no `pyproject.toml` are added by this item; the acceptance criteria say "a command"
  and do not ask for installation [src: WI-0001].
- **Tests:** `unittest`, discovered from `tests/`. `commands.test` is
  `python3 -m unittest discover -s tests -t . -q`. This was run in this project before being
  recorded: it exits 0 with a test present and exits 5 with none
  [src: run: `python3 -m unittest discover -s tests -t . -q` on an empty `tests/` → exit 5, "NO
  TESTS RAN"; run: the same command with one placeholder test present → exit 0, "Ran 1 test"]. That is a useful property rather than an accident —
  the `tests-pass` gate cannot report a pass over an empty suite.
- **Lint:** `commands.lint` is `python3 -m compileall -q expenses tests`, which exits 0 today
  [src: run: `python3 -m compileall -q expenses tests` → exit 0]. **It is a syntax check and
  nothing more.** It does not find unused imports, shadowed names, or style problems. It is
  recorded as the lint command because a syntax check that runs beats a style check that is not
  installed, and it is written down here so that nobody reads a green `no-lint-errors` gate as
  evidence of anything more than "every file parses". If a linter is ever added to this project,
  this ADR is what should be superseded.

## Consequences

- A person with Python 3.12 and a copy of the repository can run the tool and its tests with no
  setup at all, which is the closest thing to the "nothing signed up for" property the vision
  asks for that a code-level decision can deliver.
- Tests exercise the CLI by calling `main(argv)` in-process for the common cases and through
  `subprocess` where exit codes and stderr are the thing under test — `unittest` makes both
  ordinary, and AC-level criteria are mostly about exit codes.
- The lint gate is weaker than the name suggests, permanently, until this ADR is superseded. That
  is the cost of A and it is stated rather than discovered.
- `argparse` decides some things this project would otherwise decide: usage errors exit **2**,
  and `--help` output exists for free — which AC5 relies on when it says the recording command's
  usage output shows no per-person-share option [src: WI-0001 AC5].
- **Reversibility: high.** Adding `pytest` later is a dependency file and a command change in
  `tracker/project.yaml`; the `unittest` tests keep running under `pytest` unchanged. Replacing
  `argparse` would touch one module. Nothing on disk depends on this choice.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-22T02:06:34Z | plan | WI-0001 | First version |
