---
title: Represent the age bands as an ordered table beside the extension table
version: 1
status: current
updated: 2026-08-27T18:05:57Z
updated-by: plan
updated-for: WI-0002
---

# ADR-0005 — Represent the age bands as an ordered table beside the extension table

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

WI-0002 adds a second input to the destination choice: a file's age, which routes it into
`recent/` or `old/` above its type folder [src: WI-0002 AC1; src: WI-0002/Q-001]. The stakeholder
chose two bands with one boundary at a year [src: WI-0002/Q-002], and `refine` pinned the boundary
at 365 days as a reversible assumption [src: WI-0002 AC4].

Two bands and one boundary need almost no structure, so the decision is not "how do we compute
this" — it is **what shape the age rule has in the code**, and that question was routed here
rather than to the stakeholder because the answer is the same whoever they are
[src: tracker/items/WI-0002/artifacts/refinement-qa.md]. What makes it worth an ADR is the next
item: WI-0003 makes the sorting rules user-supplied, and it explicitly has no dependency on this
item, so whatever shape lands here is what WI-0003 will have to make configurable
[src: WI-0003]. A shape that does not match the extension table's shape means WI-0003 designs its
rule format twice, once per kind of rule.

What already exists: `tidy/rules.py` holds `DEFAULT_RULES`, a `dict` of folder name to a tuple of
extensions, and `folder_for(filename)`, a lookup over it returning `None` when nothing matches
[src: tidy/rules.py]. `tidy/planner.py` is the only module that decides a destination
[src: ADR-0002; src: tidy/planner.py].

## Options considered

- **A — A constant and a comparison in the planner.** `OLD_AFTER_SECONDS = 365 * 24 * 3600` in
  `rules.py`, and `"old" if age >= OLD_AFTER_SECONDS else "recent"` inline in `build_plan`. Cost:
  the two band names become string literals in control flow, so WI-0003 has to invent a
  representation for something that has none, and the planner acquires a second kind of decision
  in its body rather than a second lookup. Risk: low for this item, and the whole cost lands on
  the next one.
- **B — An ordered table beside the extension table.** `DEFAULT_BANDS = (("recent", 365 * 24 *
  3600), ("old", None))` in `rules.py`, and `band_for(age_seconds)` as a lookup over it, mirroring
  `DEFAULT_RULES` and `folder_for`. The last entry's `None` means "no upper bound", so a table
  always classifies. Cost: a tuple of two entries where an `if` would do, and a reader has to
  learn one small convention. Risk: it looks like generality nobody asked for — the mitigation is
  that the table has exactly the two bands the stakeholder chose, and adding a third is
  `## Out of scope` for this item [src: WI-0002].
- **C — A rule engine: predicates, or a small expression language over `os.stat` fields.** Cost:
  far more than two bands justify, and it makes WI-0003 harder rather than easier, because
  callables do not serialise into a configuration file. Risk: the classic over-build; rejected.

## Decision

**Option B.** `tidy/rules.py` gains:

- `DEFAULT_BANDS`, an ordered sequence of `(band_name, max_age_seconds)` pairs, youngest first,
  whose final entry carries `None` as its bound — `(("recent", 365 * 24 * 3600), ("old", None))`
  for this item [src: WI-0002 AC4];
- `band_for(age_seconds)`, returning the name of the first band whose bound is `None` or strictly
  greater than `age_seconds` [src: WI-0002 AC4; src: tidy/rules.py].

Three details are fixed here because each is checkable against code and each would otherwise be
decided silently:

1. **The comparison is half-open, `age < bound`.** A file exactly on the boundary therefore falls
   into the older band, which is what the criterion requires [src: WI-0002 AC4].
2. **Age is `now - st_mtime`**, and nothing else [src: WI-0002 AC3].
3. **`now` is read once per `build_plan` call** and passed to the classification, so every file in
   one run is measured against the same instant. Reading the clock per file would let a slow run
   split a boundary between two files of identical age.

`build_plan` composes the destination as `os.path.join(band, type_folder, name)`. Every
destination is still decided in `tidy/planner.py` and nowhere else, so ADR-0002 is untouched
[src: ADR-0002].

## Consequences

What becomes easy: WI-0003 gets one mechanism for both kinds of rule — replace `DEFAULT_RULES`,
replace `DEFAULT_BANDS`, and the lookups do not change [src: WI-0003]. The band boundary becomes
a number in a data structure rather than a branch, which is what a configuration file can carry.
Testing the boundary needs no folder at all: `band_for` takes seconds and returns a name.

What becomes harder: nothing structural, but there is one more small convention to learn — the
`None` bound on the last entry. A malformed table with no `None` bound would classify a
sufficiently old file as no band; WI-0003 is where validating a user-supplied table belongs
[src: WI-0003 AC4], and this item's table is a constant.

**Reversibility: cheap.** Reversing to option A is deleting `DEFAULT_BANDS`, inlining one
comparison in `band_for`'s caller, and changing the tests that call `band_for` directly. One
module, no data on disk, no change to the command-line interface or to any file the tool writes.
The 365-day boundary is a single value in that table and is itself recorded as a reversible
assumption [src: WI-0002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T18:05:57Z | plan | WI-0002 | First version |
