---
title: Ship recall as an executable script beside an importable module, with positional-only arguments
version: 1
status: current
updated: 2026-08-29T11:16:00Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0005 — Ship `recall` as an executable script beside an importable module, with positional-only arguments

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Every acceptance criterion on this epic is written as a command typed at a terminal — `recall
add`, `recall list`, `recall review` — and decided by that command's output and exit code
[src: WI-0001 AC1; src: EP-001/Q-001]. Nothing on the record says how the word `recall` comes to
be a command on the user's machine, and the answer determines both how the tool is documented
and how `verify` runs the criteria at all [src: WI-0001 AC5].

Two constraints narrow it. The interpreter is an externally-managed environment that refuses
`pip install` into it, so an installation step is not free
[src: ADR-0003]. And the project depends on no third-party package, for running or for testing
[src: ADR-0003].

The argument surface needs deciding with it. AC6 requires `recall add --deck german "die Katze"
"the cat"` to exit non-zero, and AC9 requires any count of positional arguments other than two
to exit non-zero with a usage line on stderr [src: WI-0001 AC6; WI-0001 AC9]. Those are two
statements of one rule, and a conventional option parser implements neither of them by accident:
it would also reject a card side that happens to begin with a dash, which no criterion asks for.

## Options considered

- **A — an executable script `recall` at the repository root, beside an importable
  `recall.py`.** Cost: the user puts the repository root on their `PATH`, or types `./recall`;
  the documentation has to say so. Risk: low, and there is no install step to go wrong.
- **B — a packaged console script, installed with `pip`.** Cost: packaging metadata, an install
  step before any criterion can be checked, and an environment that refuses the install
  [src: ADR-0003]. Risk: high for what it buys on a single-user tool.
- **C — a shell wrapper that calls `python3 recall.py`.** Cost: a second language in the tree
  and a second place the invocation can be wrong. Risk: low, but it buys nothing option A does
  not already have.

## Decision

Option A, with the argument rule stated as a contract.

**Entry point.** Two files at the repository root:

- `recall` — executable, with the shebang `#!/usr/bin/env python3`. It does three things and
  nothing else: it puts its own directory on the import path, it calls `main` with the arguments
  after the program name, and it exits with what `main` returned [src: WI-0001 AC1].
- `recall.py` — the module: `main(argv)` takes the argument list without the program name and
  returns the process exit code. It prints; it does not exit the process itself, so a test can
  call it in-process as well as by subprocess.

The documentation states both ways to run it — `./recall add ...` from the repository, or
`recall add ...` with the repository root on `PATH` — and the acceptance criteria are checked
the second way, which is the form they are written in [src: WI-0001 AC1].

**Arguments.** The first argument is the command name. Everything after it is positional and is
never interpreted as an option: `add` takes exactly two positional arguments and rejects any
other count [src: WI-0001 AC9]. `--deck german` is therefore not an option that is rejected but
two more positional arguments, which makes the count four, which is not two
[src: WI-0001 AC6]. A card side beginning with a dash is ordinary text.

**Exit codes.** `0` on success. `2` when the command line itself is wrong — an unknown command,
the wrong number of arguments, or an empty card side. `1` when the command line was fine and the
store could not be used [src: ADR-0004].

**Streams.** What the user asked for goes to stdout: the confirmation line, the listing, the
line saying there are no cards. Diagnostics go to stderr: the usage line AC9 requires, the
empty-side messages AC4 requires, and store failures [src: WI-0001 AC4; WI-0001 AC9].

**The listing.** One line per card, tab-separated: the card number, then the question side, then
the answer side, each exactly as stored [src: WI-0001 AC2]. Tabs rather than a punctuation
separator so that a card side containing any punctuation is still unambiguous to read and to
check.

## Consequences

What becomes easy: the tool runs from a clone with nothing installed, and `verify` can check a
criterion by putting one directory on `PATH`. Tests can drive `main` directly for speed or the
executable for fidelity, and both exercise the same code [src: ADR-0003].

What becomes hard: `recall` is not on the user's `PATH` until they put it there, which is a step
a packaged tool would not have. The positional-only rule means the tool can never grow a genuine
option — `--help` included — without revisiting this decision; that is the price of AC6 and AC9
being stated as counts of positional arguments [src: WI-0001 AC6; WI-0001 AC9].

**Reversibility: high.** Adding packaging later is additive: a console script entry point would
call the same `main`, and the two files stay where they are. Relaxing the positional-only rule is
a change to one function plus whichever criteria then need restating.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:16:00Z | plan | WI-0001 | First version: the executable-plus-module entry point, positional-only arguments, the exit code scheme, the stream split and the tab-separated listing |
