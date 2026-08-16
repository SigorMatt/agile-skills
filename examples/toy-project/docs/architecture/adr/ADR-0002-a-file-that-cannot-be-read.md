---
title: A file that cannot be read is reported on stderr and left out of the listing
version: 1
status: current
updated: 2026-08-16T21:33:10Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0002 — A file that cannot be read is reported on stderr and left out of the listing

- **Status:** accepted
- **Date:** 2026-08-16
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 rules on a folder that cannot be read (AC11: stderr, exit 2) and on entries that are not
files (AC6, AC7: ignored silently, exit 0). It says nothing about the case in between: the
folder opens, the entry is a regular file, and reading *that file* fails — mode `000`, a file
removed between the listing and the read, a device node that raises on read.

The code must do something, and doing nothing is a traceback, which AC9 forbids as an
observable and which `docs/product/vision.md` names as one of the two ways this tool fails on
its own terms ("a number, not a stack trace"). No document decides it, so this ADR does.

The refinement Q&A for WI-0001 does not cover it either: Q3 settled how a file that is not
*text* is counted (by the same byte rule as everything else), which is a different question —
that file can be read.

## Options considered

- **A — skip it silently, as AC6 and AC7 skip a subdirectory.** Cost: the file is visible in
  `ls` but missing from the listing and from the total, with no explanation anywhere. Risk: the
  total is then quietly wrong, and the tool's one job is to say how much is in the folder.
- **B — skip it, and print one line to stderr naming the file and the problem; still exit 0.**
  Cost: a folder with such a file writes to stderr on a run that succeeded. Risk: low. stdout
  stays exactly as AC1–AC3 specify and stays pipeable, so nothing that is piped is disturbed.
- **C — treat it as a fatal error: exit 2, print nothing.** Cost: one unreadable file in a
  folder of two hundred destroys the answer for the other 199. Risk: it contradicts the spirit
  of AC9 and AC6 — the tool is meant to survive awkward contents, and to fail only when it
  cannot do its job at all.
- **D — list it with a count of 0.** Cost: indistinguishable from an empty file, which AC4 gives
  a real meaning to. Risk: silently wrong numbers, the worst outcome available here.

## Decision

**Option B.** When `count_lines` raises `OSError` for an entry, `main` prints exactly one line
to stderr — `linecount: <name>: <strerror>` — omits that file from the listing and from the
total, and continues. The exit status stays 0.

The rule holds for exactly one thing: an `OSError` raised while opening or reading an entry that
the listing step already established is a file. It does not apply to the folder itself, which is
AC11's territory and exits 2.

## Consequences

- Every acceptance criterion in WI-0001 that asserts "prints nothing on stderr" is stated about
  a folder whose files are all readable, so none of them is affected by this decision.
- A folder in this state produces a total that does not account for every file in it. The stderr
  line is the only signal of that, which is why silence (option A) was rejected.
- `count_lines` may raise; it does not swallow errors. The choice of what to do about a failure
  lives in `main`, next to the other exit-status decisions, rather than being spread across the
  counting code.
- **Reversibility: cheap.** One `except OSError` branch in `main` and one test. Switching to
  option A means deleting the stderr line; switching to option C means returning 2 instead of
  continuing. Neither touches a function signature or the output format.
- If a later item wants these files listed with a marker instead of skipped, that changes the
  row format, which is fixed by AC1 — so it would be a new item with its own criteria, and this
  ADR would be superseded rather than edited.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T21:33:10Z | plan | WI-0001 | First version |
