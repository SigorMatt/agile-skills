---
title: Keep the help text as prose, and guard it with a test that reads the rule tables
version: 3
status: current
updated: 2026-08-28T13:57:57Z
updated-by: implement
updated-for: BUG-0006
---

# ADR-0008 — Keep the help text as prose, and guard it with a test that reads the rule tables

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0003
- **Supersedes:** —

## Context

`python3 -m tidy --help` still tells the reader that a destination is "chosen by file type", and
points at "the extension-to-folder table" as though there were one table. Age routing landed with
WI-0002 and made both sentences wrong: a file's age now chooses the top-level band folder, and
`tidy/rules.py` holds two tables rather than one [src: BUG-0003; src: tidy/rules.py;
src: WI-0002 AC1].

What makes this worth a decision rather than a two-string edit is *how* the text went wrong.
`tidy/cli.py` was not edited by WI-0002 at all — the strings are literals in `build_parser`, no
gate reads them, and nothing connects them to the tables whose content they summarise
[src: tidy/cli.py; src: WI-0002]. The wording became false while every test stayed green, and it
was found by someone reading the help text rather than by the suite.

The next item repeats the setup. WI-0003 makes both tables user-supplied, through the one
mechanism ADR-0005 chose for them [src: WI-0003; src: ADR-0005]. Whatever is decided here is what
WI-0003 inherits, so the question is not "what should the two sentences say" but "what stops them
being wrong again". BUG-0003 already rules out the laziest guard: its AC4 asks for a regression
test that does not restate the help text as a literal, so that it fails on the claim going stale
rather than on the next rewording [src: BUG-0003 AC4].

## Options considered

- **A — Generate the help text from the tables.** `cli.py` imports `tidy/rules.py` and formats
  `DEFAULT_BANDS` and `DEFAULT_RULES` into the description and epilog, so the text is derived from
  the data it describes and cannot contradict it. Cost: the top layer takes on a responsibility the
  overview does not give it — `cli.py` parses arguments, renders an action list and chooses the
  exit code, and would now also read rule data and compose prose about it
  [src: docs/architecture/overview.md]. Prose assembled from an arbitrary table also reads worse
  than prose written for a reader: two bands make a sentence, five make a list. Risk, and the
  decisive one: under WI-0003 the tables in force are the *user's*, and `build_parser` runs before
  `parse_args` has told anyone where the user's rules came from [src: tidy/cli.py], so generated
  text would describe the built-in defaults during a run that used something else — a quieter
  version of exactly the bug being fixed here.

- **B — Keep the text as prose, and guard it with a test that reads the tables.** The description
  and epilog stay literal strings in `build_parser`, written for a reader. `tests/test_cli.py`
  imports `DEFAULT_BANDS` from `tidy.rules` and asserts that every band name the table declares
  appears in the `--help` output, alongside a word for age and everything WI-0001 AC1 requires
  [src: BUG-0003 AC1; src: BUG-0003 AC3]. Cost: the guard covers the claims it encodes and nothing
  else — the extension table's contents are not checked this way, because the help text refers the
  reader to `README.md` for them instead of listing them. Risk: when a future item adds a band, the
  alarm rings in `tests/test_cli.py` rather than next to the edit that caused it, which is a
  worse-placed signal than a compile error but a signal all the same.

- **C — Fix the two strings and pin the wording with a literal assertion.** Cost: the test then
  fails on every future rewording and passes on every future staleness, which is the opposite of
  what is wanted. Excluded by the item itself [src: BUG-0003 AC4].

## Decision

**B.** The help text is prose, held as literal strings in `build_parser` in `tidy/cli.py`, and
`tidy/cli.py` imports nothing from `tidy/rules.py` [src: tidy/cli.py; src: run: grep -nE
"^(from|import).*\brules\b" tidy/cli.py → exit 1, no output]. The connection between the text
and the data lives in the test suite instead: `tests/test_cli.py` imports `DEFAULT_BANDS` and
asserts that each band name it declares occurs in the `--help` output.

Checkable against the code as: that same anchored `grep` over `tidy/cli.py` returns no line
importing `rules` [src: run: grep -nE "^(from|import).*\brules\b" tidy/cli.py → exit 1, no
output], and `tests/test_cli.py` contains an import of `DEFAULT_BANDS` used in an assertion over
the help output.

## Consequences

- The help text can be reworded freely; no test asserts its wording [src: BUG-0003 AC4].
- Adding a band to `DEFAULT_BANDS` fails the suite until the help text mentions it. That is the
  intended alarm, and it is the one thing WI-0003 most needs, since it changes where those tables
  come from [src: WI-0003].
- The extension table stays unguarded in this direction: the help text names no extensions, so
  there is nothing to compare. If a later item makes the help list extensions, the same guard
  should be extended to `DEFAULT_RULES` or the claim should not be made.
- The layering is untouched. `cli.py` keeps the responsibilities the overview gives it, and the
  destination is still decided in `planner.py` alone [src: ADR-0002; src: docs/architecture/overview.md].
- **Reversibility: cheap.** Moving to A is one helper function inside `tidy/cli.py` plus an edit to
  the same test, with no interface, data format or on-disk consequence; the two strings are read
  only where they are written [src: run: grep -rn "epilog\|description=" tidy tests --include=*.py
  → exit 0, two hits, both `tidy/cli.py`]. Nothing outside that module would have to change.
- **The two citations in `## Decision` record a check, not a snapshot, and that is deliberate.**
  They were first written as `grep -n "^from\|^import" tidy/cli.py → exit 0, five imports:
  argparse, os, sys, .apply, .planner`, and WI-0003 made that output unreproducible by adding a
  sixth import — a `from .ruleset_file import …` line whose first five letters are `rules`, sitting
  directly under the one claim in this record most likely to be misread [src: WI-0003;
  src: WI-0003/Q-003]. The claim never became false; its evidence had become a dated observation
  of a file that keeps changing. The anchored form decides the claim instead: it stays true when a
  seventh import is added and fails exactly when someone imports the rule table, which is the
  event this decision exists to prevent. The general rule this record follows, and which the next
  one should: cite an absolute claim with a command that tests it, not with one whose output
  happened to be true on the day it was run [src: BUG-0004/Q-002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-28T13:57:57Z | implement | BUG-0006 | The `## Decision` citation supporting option A's decisive risk became file-level: the `tidy/cli.py:NN` form dropped its line number. It named line 52, which was `args = build_parser().parse_args(argv)` when this record was written and is now a docstring inside `render`; the sentence already names `build_parser` and `parse_args`, and `grep -n "parse_args" tidy/cli.py` resolves that to one line. Per ADR-0013 |
| 2 | 2026-08-27T22:07:34Z | answer-questions | WI-0003 | The two `run:` citations in `## Decision` replaced with the anchored `grep -nE "^(from|import).*\\brules\\b"` check, whose outcome the claim survives; a `## Consequences` bullet added recording that a `run:` citation here tests the claim rather than snapshotting the file |
| 1 | 2026-08-27T20:20:23Z | plan | BUG-0003 | First version: the help text stays prose and is guarded by a test that reads `DEFAULT_BANDS`, rather than being generated from it |
