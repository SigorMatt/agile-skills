---
title: Reject a bad --top value in our own code, not through argparse
version: 1
status: current
updated: 2026-08-17T00:05:00Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0004 — Reject a bad --top value in our own code, not through argparse

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

ADR-0001 gave the command line to `argparse`, because AC11 and AC12 of WI-0001 only required a
message on stderr and exit 2, which is argparse's own behaviour.

WI-0002 AC7 asks for more than that. `--top -1` and `--top abc` must "print nothing on stdout,
print **one line** on stderr naming the problem, and exit 2 — the same failure shape as WI-0001
AC11". Argparse's failure shape is two lines: a `usage:` block, then `linecount: error: …`. So
the obvious implementation — `parser.add_argument("--top", type=int)` plus a range check — fails
the criterion on the line count, not on the exit code.

The constraint that rules out the tidiest fix is WI-0002 AC4: without `--top`, "stdout, stderr
and the exit code are byte-identical to what WI-0001 delivered on the same folder", and WI-0001's
tests must pass unmodified. Anything that changes how argparse reports *existing* errors puts
that at risk.

## Options considered

- **A — `type=int` on the argument, plus a check for negatives after parsing.** Cost: the
  non-integer case never reaches our code, so its message is argparse's two-line one and AC7
  fails. Risk: none to the rest of the tool; it simply does not meet the criterion.
- **B — subclass `ArgumentParser` and override `error()`** to print one line and exit 2. Cost: it
  changes the message for *every* usage error, including WI-0001's "no argument at all" (AC12).
  Risk: that is the case AC4's byte-identity clause is least clear about, and a change there
  buys nothing — AC12 never asked for one line.
- **C — take `--top` as a string and validate it ourselves**, in a `parse_top(value)` helper that
  raises `ValueError` carrying the message. Cost: we hand-write an `int()` call and its error
  message, which argparse would otherwise have done. Risk: low and contained — the helper is
  four lines and unit-testable, and argparse keeps every error path it already owned.

## Decision

**Option C.** `parse_args` declares `--top` with no `type=`, so it arrives as a string or `None`.
`parse_top(value)` returns a non-negative `int` or raises `ValueError` whose text is the reason.
`main` catches that and prints exactly one line, `linecount: --top: <reason>`, on stderr, prints
nothing on stdout, and returns 2 — the same shape and the same prefix as ADR-0001's
`linecount: <path>: <problem>`.

Every other usage error stays argparse's: no argument at all, an unknown option such as `-t`
(WI-0002 AC8), a `--top` with no value. Those are constrained only to be "a message on stderr"
with exit 2, which is what they already are.

## Consequences

- Failure output is deliberately of two kinds: one-line messages for the conditions a criterion
  pins to one line (a bad path, a bad `--top` value), and argparse's usage block for wrong
  invocations. That is not an inconsistency to tidy away later; tidying it is what option B does,
  and it would put WI-0002 AC4 at risk.
- `parse_top` accepts everything Python's `int()` accepts from a string, including a leading `+`,
  surrounding whitespace, and underscore separators (`3_0` → 30). No criterion mentions these,
  and nothing in the tool behaves surprisingly on them.
- **Reversibility: cheap.** `parse_top` is one function with one caller. Reverting to option A is
  deleting it and adding `type=int`, at the cost of AC7. Moving to option B is a subclass in the
  same file. Neither touches `format_report`, `list_files`, `count_lines`, or any output format.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-17T00:05:00Z | plan | WI-0002 | First version |
