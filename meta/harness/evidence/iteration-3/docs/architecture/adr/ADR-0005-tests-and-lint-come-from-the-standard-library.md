---
title: Tests and lint come from the standard library, and tables are tested as golden files
version: 2
status: current
updated: 2026-08-28T19:32:15Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0005 — Tests and lint come from the standard library, and tables are tested as golden files

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

[src: ADR-0001] left the test framework to `plan` and drew the line explicitly: a developer-only
test dependency does not breach the stakeholder's *"nothing I have to install first"*, but a
runtime one does. `tracker/project.yaml` has carried `commands.test: null` since the workspace
was created, and `validate-workspace` has been emitting a warning about it on every run
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 0, 1 warning
project.commands.test-null]. Filling both commands in is part of this execution.

What is actually available was measured rather than assumed. This machine has CPython 3.12.3 and
none of `ruff`, `flake8`, `pyflakes`, `pycodestyle`, `pylint`, `mypy` or `pytest`
[src: run: python3 -c "import ruff" etc. → all ImportError]. So any third-party choice is an
install step for whoever runs the gates next, including the pipeline itself.

The testing problem this item poses is specific. Almost every criterion is of the form "feed this
document in, compare the bytes that come out" — AC4, AC5, AC6, AC7, AC8, AC9, AC13, AC14 and AC15
are all byte comparisons, and AC2, AC3 and AC12 are computed properties of the output text
[src: WI-0001]. Writing those as inline string literals in Python source is where the escaping
gets wrong: a fixture containing `\\|`, tabs, CRLF endings and a file that ends without a newline
cannot be written as a readable literal, and a test whose fixture is wrong reports a defect that
is not there.

## Options considered

- **A — `unittest` from the standard library, with document fixtures as files on disk, and
  `compileall` under `-W error` as the lint command.** Cost: `unittest` is more verbose than
  `pytest`, and `compileall` checks far less than a real linter — syntax and syntax warnings, and
  nothing about unused names or style. Risk: low, and the risk that remains is understatement:
  the lint gate will pass code a linter would reject.
- **B — `pytest`, with the same fixtures.** Cost: an install step for every contributor and for
  the pipeline. Risk: it is permitted by [src: ADR-0001] as a developer-only dependency, but it
  makes `commands.test` a command that does not currently run on this machine, which the
  `project-commands-resolved` gate treats as a failure — correctly, because a gate command
  nobody can run is a gate nobody runs.
- **C — Record an ADR saying the project has no test command.** Cost: nothing. Risk: it would be
  a false economy for a tool whose entire specification is input-output pairs, and the
  `tests-pass` gate would be recorded as skipped for the life of the project.
- **D — Fixtures as inline string literals rather than files.** Cost: none up front. Risk: the
  escaping problem above. A fixture asserting behaviour on `\\|` is exactly where a literal
  misleads, and it is one of the cases the criteria call out [src: WI-0001 AC10].

## Decision

Tests are written with `unittest` from the standard library and run with
`python3 -m unittest discover -s tests -t .`. That becomes `commands.test` in
`tracker/project.yaml`.

Lint is `python3 -W error -m compileall -q mdtab tests`, which becomes `commands.lint`. It is a
narrow check and it is claimed as nothing more: it compiles every module and turns warnings into
errors. It was chosen over doing nothing because it catches one class of defect this codebase is
unusually likely to produce — an invalid escape sequence in a string literal, such as writing
`"\\|"` as `"\|"`, which CPython 3.12 reports as a `SyntaxWarning` and which `-W error` turns
into a failure [src: run: python3 -W error -m compileall -q on a file containing x = "a\|b" →
exit 1, SyntaxError: invalid escape sequence]. A codebase whose subject matter is escaped pipes
will write that mistake.

Document fixtures live under `tests/fixtures/` as pairs: `<name>.in.md` and `<name>.out.md`,
byte-for-byte, read in binary. A test case reads the input, runs it through the tool's own entry
function, and compares bytes with the expected output. Fixtures are the only place a test may
express a document; a test may not build one from a Python literal
[src: tracker/items/WI-0001/artifacts/plan.md].

**Amended by [src: ADR-0006] for the one case this decision did not anticipate.** A fixture whose
bytes are deliberately not valid UTF-8 — the "one containing invalid UTF-8" named two paragraphs
below — carries `.bin` rather than `.md`, because `validate-workspace` reads every `.md`
file in the project as UTF-8 and cannot survive one that does not decode
[src: WI-0001/Q-004]. Nothing else here changes: the rule that a test may not build a document
from a Python literal is what that amendment exists to make executable.

No third-party package is used for tests, for lint, or at runtime, so a clone of this repository
plus `python3` runs both gates with no install step — which is the constraint [src: ADR-0001]
records, applied to the developer as well as to the user.

## Consequences

What becomes easy: every byte-equality criterion becomes one fixture pair and one line of test
code, and the fixture is readable — a person reviewing "does this table come back untouched?"
opens two files and diffs them. Cases that cannot be written as literals at all, such as a file
whose last line has no terminator or one containing invalid UTF-8, become ordinary fixtures.
Adding a case is adding two files.

What becomes hard: the lint gate is thin, and its journal entries must not claim more than it
does. Style and dead code are not checked by anything, so review is the only place they are
caught. If the project later accepts a developer-only dependency, this ADR is what should be
revisited first, and doing so does not touch the runtime.

Fixtures also have to be protected from the tools that would rewrite them. A fixture whose whole
purpose is a CRLF ending or a missing final newline is destroyed by an editor that normalises on
save; the plan therefore requires `.gitattributes` marking `tests/fixtures/**` as binary
[src: tracker/items/WI-0001/artifacts/plan.md].

**Reversibility: high.** Swapping `unittest` for `pytest` leaves the fixtures untouched and
rewrites the test modules, which are the least valuable part of the arrangement; `commands.test`
is one line of `tracker/project.yaml` [src: tracker/project.yaml]. Replacing the lint command is
one line and no code.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T19:32:15Z | answer-questions | WI-0001 | Recorded that ADR-0006 amends the fixture extension for a pair that is not valid UTF-8; the decision itself is unchanged |
| 1 | 2026-08-28T18:53:01Z | plan | WI-0001 | First version, choosing unittest, file fixtures, and compileall under -W error |
