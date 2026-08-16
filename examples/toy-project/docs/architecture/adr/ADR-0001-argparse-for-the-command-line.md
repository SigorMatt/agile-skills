---
title: Parse the command line with argparse
version: 1
status: current
updated: 2026-08-16T21:33:10Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0001 — Parse the command line with argparse

- **Status:** accepted
- **Date:** 2026-08-16
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 AC11 and AC12 require that every wrong invocation — a missing path, an unreadable
folder, a path that is a regular file, and no argument at all — print nothing on stdout, print a
message on stderr, and exit **2**. The exact wording is deliberately left open by AC11 and
AC12; the stream and the exit code are not.

WI-0002, already `ready`, adds `--top N` with the same failure shape (its AC7), requires the
flag to be accepted both before and after the folder (its AC8), and requires the short form
`-t` to be rejected rather than merely undocumented. So the argument layer chosen here has to
survive one more item without being rewritten.

The item's `## Notes` observes that AC12 "matches what `argparse` does by default", which is an
observation about a candidate, not a decision — this ADR is where the decision is taken.

## Options considered

- **A — `argparse` from the standard library.** Cost: the error wording is argparse's, not
  ours, and it prints a usage line before the message. It also accepts long-option
  abbreviations (`--to 3`) and `--top=3`, neither of which any criterion mentions. Risk: low —
  argparse exits 2 on a usage error and writes to stderr, which is exactly the shape both items
  demand, and it handles flag-after-positional and `type=int` rejection for WI-0002 with no
  extra code.
- **B — hand-rolled `sys.argv` parsing.** Cost: every case in AC11, AC12, AC7 and AC8 becomes
  code we write and test ourselves, including flag position and the rejection of `-t`. Risk:
  medium — it is more code with no criterion asking for it, and the first mistake in it is a
  wrong exit code, which is precisely what the criteria pin down.

## Decision

`linecount.py` uses `argparse.ArgumentParser(prog="linecount")` with one positional argument
`folder`. Usage errors are left to argparse, which prints to stderr and exits 2.

Errors that argparse cannot know about — the path does not exist, is not a directory, or cannot
be read — are raised by our own code, which prints exactly one line `linecount: <path>: <what
went wrong>` to stderr, prints nothing to stdout, and returns 2. The two paths therefore agree
on stream and exit code while differing in wording, which is all the criteria require.

`prog="linecount"` is set explicitly so the message does not vary with how the script was
invoked, which keeps the end-to-end tests from depending on the caller's path.

## Consequences

- WI-0002 adds `--top` as `parser.add_argument("--top", type=int)` with no new failure
  machinery: the non-integer case, the flag-after-positional case and the rejection of `-t` all
  fall out of argparse, and only the negative-N case needs a check of our own.
- Two different message styles reach stderr (argparse's usage block; our one-liner). No
  criterion constrains the wording, and unifying them would mean suppressing argparse's output.
- The tool accepts `--top=3` and unambiguous long-option abbreviations. Nothing asks for these
  and nothing forbids them.
- **Reversibility: cheap.** `parse_args` is one function in one file with no callers outside
  `main`; replacing it with hand-rolled parsing would change no other function's signature and
  no test that goes through the CLI, because those tests assert the exit code and the streams
  rather than the wording.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T21:33:10Z | plan | WI-0001 | First version |
