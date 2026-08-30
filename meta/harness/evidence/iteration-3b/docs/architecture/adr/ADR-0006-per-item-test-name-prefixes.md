---
title: Test method names carry the item ID as well as the criterion number
version: 1
status: current
updated: 2026-08-29T22:39:36Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0006 — Test method names carry the item ID as well as the criterion number

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0001 AC11 requires that an automated test exists for each of its criteria, *"each naming the
criterion it covers"*, and the suite enforces that requirement on itself: a coverage test walks
every discovered test method and asserts that exactly one method name contains the tag `ac<n>_`
for each n from 1 to 10 [src: tests/test_mdtab.py; src: WI-0001 AC11].

WI-0002 AC10 asks for the same thing for its own criteria [src: WI-0002 AC10]. The two collide,
mechanically and immediately. A method named `test_ac1_left_marker` for this item's AC1 also
contains the substring `ac1_`, so WI-0001's coverage test would find two methods where it
requires exactly one, and a criterion that is delivered and verified would start failing because
a **later** item added a test. The tag is not unique across items, and nothing about it was ever
going to be — it was written when one item existed.

This has to be settled before any test for WI-0002 is written, which is why it is here rather
than left to `implement`.

## Options considered

- **A — Give every test method an item prefix: `test_<item-id-lowercased>_ac<n>_<slug>`, and
  give each item's coverage test its own tag, `wi0001_ac<n>_` and `wi0002_ac<n>_`
  [src: tests/test_mdtab.py; WI-0001 AC11; WI-0002 AC10].** Cost:
  WI-0001's eleven test methods are renamed and its coverage test's tag string changes — a
  mechanical edit to a delivered file, with no change to a single assertion. Risk: low, and it is
  visible in a diff. The convention then scales to every future item without another decision.
- **B — Put WI-0002's tests in a separate module and scope each coverage test to its own
  module.** Cost: the coverage test stops reading test *names* and starts reading module paths,
  which is a weaker check — a test in the wrong module silently stops counting. It also splits
  fixtures and helpers across modules, or forces a shared helper module for four functions.
  Risk: moderate, and it defers the collision rather than removing it: two criteria numbered the
  same in one module would collide again.
- **C — Number WI-0002's criteria continuing from WI-0001's, so AC1 here is `ac12`.** Cost: an
  item's criteria would no longer start at AC1, and every reference to "AC3" would need to say
  which item's. It makes the tracker harder to read in order to keep one test tag working.
  Risk: low technically, high for the record's legibility, which is the thing this project is
  for.
- **Chosen: A.** It is the only option that leaves the coverage check as strong as it was, it
  costs one mechanical rename, and it states a convention rather than a workaround.

## Decision

1. **A test method that covers an acceptance criterion is named
   `test_<item-id-lowercased-without-hyphen>_ac<n>_<slug>`** — for example
   `test_wi0001_ac3_cells_carry_one_space_either_side` and
   `test_wi0002_ac1_left_marker_pads_on_the_right`.
2. **An item's coverage test searches for its own tag**, `wi0001_ac<n>_` or `wi0002_ac<n>_`,
   and still requires exactly one match per criterion. The check is unchanged in strength; only
   the tag is narrowed [src: tests/test_mdtab.py].
3. **WI-0001's eleven test methods are renamed to match, and its coverage test's tag string is
   changed.** No assertion, fixture or docstring in those tests is altered, so WI-0001 AC11
   remains true of the suite by exactly the reading it always had.
4. Tests that cover no criterion — helpers, and the invariants `split_lines` and
   `display_width` are checked against — keep their descriptive names and carry no `ac` tag.

## Consequences

Easy: adding an item stops being able to break a delivered item's coverage test, which is the
failure this ADR exists to remove. Every future item gets its own namespace with no further
decision, and `git grep wi0002_ac` answers "what covers this item" in one command
[src: tests/test_mdtab.py; WI-0002 AC10].

Hard: WI-0001's test file is edited by an item that is not WI-0001, so `git log` for WI-0001
no longer contains every change to its tests. The mitigation is that the change is a rename with
no behaviour in it, this ADR is cited from WI-0002's plan, and WI-0002 AC9 requires WI-0001's
criteria to be re-read by ID and the result recorded — so the edit is examined rather than
assumed harmless.

Reversibility: high. The convention lives in test method names and two tag strings; reversing it
is a rename in one file and touches no production code and no fixture.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T22:39:36Z | plan | WI-0002 | First version. Resolves the collision between WI-0001 AC11's `ac<n>_` tag and WI-0002 AC10's need for the same tags |
