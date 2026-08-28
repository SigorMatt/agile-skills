---
title: Build tidy as a Python 3 command-line tool using only the standard library
version: 1
status: current
updated: 2026-08-27T15:52:43Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0001 — Build tidy as a Python 3 command-line tool using only the standard library

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

The repository contained no source code, no build file and no test command when this decision was
taken: `tracker/project.yaml` had `commands.test`, `commands.lint` and `commands.build` all set to
`null`, and `intake` deliberately named no technology anywhere in the tracker so that the choice
would not be smuggled in as analysis [src: EP-001/Q-001].

`intake` escalated the choice to the stakeholder as EP-001/Q-001, because it fixes what "run it"
means in every acceptance criterion and therefore what a reviewer can check. The stakeholder's
reply delegated the decision and endorsed a direction: *"Whatever's easiest for you to build and
test — you know this better than me. Python's fine if that's your call. Yeah, a terminal command
is fine, nothing fancier needed."* [src: EP-001/Q-001]

That reply settles two things by itself — it is a terminal command, and Python is acceptable — and
leaves the rest (which Python, which test runner, whether third-party packages may be used) to the
architect. This ADR records what was chosen under that delegation, so that `plan` and `implement`
read the decision from a document rather than from a question file.

## Options considered

- **A — Python 3, one command-line entry point, standard library only.** Cost: interpreter startup
  is slower than a compiled binary, which is irrelevant for a tool whose work is filesystem I/O.
  Risk: low — `os`, `pathlib`, `argparse`, `shutil`, `datetime`, `json` and `unittest` cover
  everything the epic's scope needs (directory listing, extension matching, date arithmetic, a rule
  file, moving files, and tests), so no dependency has to be installed to build or to test.
- **B — Python 3 with third-party packages** (`pytest` for tests, a YAML or TOML library for the
  rules of WI-0003). Cost: an install step, a lockfile, and a virtual environment before anything
  can be run. Risk: the stakeholder asked for whatever is easiest to build and test, and the first
  thing this adds is a setup failure mode that has nothing to do with tidying folders.
- **C — A shell script.** Cost: date arithmetic and a user-supplied rule file are painful in shell.
  Risk: high — the preview/apply split is the product's central promise, and shell makes it easy to
  get subtly wrong.
- **D — A compiled language producing a single binary** (Go, Rust). Cost: a toolchain has to be
  installed before a line can be compiled. Risk: disproportionate effort for a tool of this size,
  and it contradicts the stakeholder's "nothing fancier needed".

## Decision

`tidy` is a Python 3 program, invoked as a command in a terminal, written against the Python
standard library only.

Checkable against the code:

1. The source imports nothing outside the Python standard library, in the tool or in its tests.
2. There is a single command-line entry point. A user runs it by typing one command with the target
   folder as an argument; preview versus real running is selected by an argument to that command,
   whose exact spelling is `plan`'s to choose.
3. The minimum supported interpreter is Python 3.9. Nothing in the epic's scope needs a later
   feature, and 3.9 or newer is what a current Linux or macOS machine already has.
4. Tests are written with `unittest` from the standard library and run with
   `python3 -m unittest discover -s tests -q`, so that testing needs no installation either.

`tracker/project.yaml`'s `commands.*` are deliberately still `null` at the time of this ADR: the
`tests` directory does not exist yet, so recording the command now would record one that cannot
run. `plan` sets `commands.test` to the command in point 4 when it lays out the first item's test
directory, which is the responsibility `project.yaml`'s own header assigns it
[src: tracker/project.yaml].

## Consequences

What becomes easy: running the tool on any machine that already has Python 3, with no install
step; writing the date arithmetic WI-0002 needs and the rule parsing WI-0003 needs, both from the
standard library; and running the test suite as a gate from the first commit.

What becomes hard: distributing a single self-contained file to a machine without Python; and
using a YAML rule format in WI-0003, since no YAML parser is in the standard library — WI-0003's
rule format will have to be one the standard library can read (JSON, INI via `configparser`, or
TOML via `tomllib` on 3.11+, which would raise the floor from point 3).

Reversibility: **cheap while the tool is small, and it will not get much larger.** Rewriting a
few hundred lines of filesystem code in another language is an afternoon; nothing outside this
repository depends on the choice, because the tool is invoked as a command and has no API. The
one part that is awkward to reverse is any rule-file format WI-0003 publishes, since a user who
has written a rule file would have to rewrite it. Point 4 (the test runner) and point 3 (the
version floor) are individually reversible without touching the rest.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T15:52:43Z | answer-questions | EP-001 | First version, deciding EP-001/Q-001 under the stakeholder's delegation |
