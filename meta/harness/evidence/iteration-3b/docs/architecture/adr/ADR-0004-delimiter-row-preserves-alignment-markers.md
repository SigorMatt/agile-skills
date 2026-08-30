---
title: The delimiter row keeps its alignment markers even though WI-0001 does not act on them
version: 1
status: current
updated: 2026-08-29T21:47:00Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — The delimiter row keeps its alignment markers even though WI-0001 does not act on them

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 rewrites the delimiter row. Its AC4 says that row is, for each column, a pipe followed by
the column's width plus two hyphens and no spaces [src: WI-0001 AC4]. Read on its own, that
sentence says a delimiter cell written `:---:` in the input comes back as `-----`, and the
document now renders with a different alignment than the author wrote. That is not a formatting
change; it is a silent semantic one, on the one construct this tool exists to touch.

Three documents say it must not happen, and none of them is AC4:

- WI-0001's own `## Out of scope`: *"This item may leave marker characters in place unchanged,
  and AC4's hyphen rule describes a delimiter cell that carries no marker."* [src: WI-0001]
- ADR-0003 decision 10: *"Alignment markers are WI-0002's subject and are out of scope here; this
  rule describes a delimiter cell that carries no marker."* [src: ADR-0003]
- WI-0002's `## Out of scope`: *"The filter reads markers; it never adds, removes or alters
  them."* [src: WI-0002]

The stakeholder's question that produced AC4 was explicitly about *"a delimiter row that carries
no marker at all"* [src: WI-0001/Q-004]. So the record is not silent and the answer is not ours to
invent — this ADR records the reading, and the composition rule that follows from it, because
`implement` and `verify` both need it stated in one place rather than assembled from three.

A second thing follows and has to be decided here, because nothing on record covers it: a marked
delimiter cell has a **minimum width**. `:` + at least one hyphen + `:` is three characters, so a
column whose content is entirely empty and whose marker is `:-:` cannot be written at
width + 2 = 2 without producing `::`, which is not a delimiter row at all. The filter would emit
a table it would refuse to recognise on the next run, and AC9's idempotence would fail on it
[src: WI-0001 AC9].

## Options considered

- **A —** Follow AC4 literally: every delimiter cell becomes hyphens. Cost: any table with an
  alignment marker renders differently after the tool runs, which is the exact failure the
  stakeholder said would end their use of it — *"I will stop using it the first time it edits a
  paragraph"* [src: EP-001/Q-001] — applied to a table instead of a paragraph. Risk: high, and
  worst on the documents that are most carefully written.
- **B —** Preserve each delimiter cell's colons exactly as the input had them, and fill the rest
  of the cell with hyphens so it still occupies the column's width plus two characters with no
  spaces. Cost: AC4's literal text is satisfied only for a markerless cell, which is what its
  source question asked about and what the item's `## Out of scope` says it means. Risk: low.
  WI-0002 then decides where a marker's colons *sit*, which is a change to a rule that already
  preserves them rather than a rescue.
- **C —** Copy any table containing a marker untouched until WI-0002 lands. Cost: the stakeholder
  writes ordinary pipe tables and markers are common in them, so a large share of their documents
  would silently do nothing — the failure mode ADR-0003 already calls the cost of conservatism,
  paid here for no reason. Risk: low for damage, high for usefulness.

## Decision

1. A delimiter cell is composed as: its **leading colon if the input cell had one**, then
   hyphens, then its **trailing colon if the input cell had one**, occupying exactly
   `width + 2` characters with no spaces. A cell with no colons is therefore `width + 2`
   hyphens, which is AC4's literal text.
2. A column's width is raised to a minimum of **1** when its delimiter cell carries two colons,
   so that `:`, at least one hyphen and `:` always fit. No other case needs raising: one colon
   needs two characters and no colons needs one, and `width + 2` is at least 2.
3. The filter never adds a colon, never removes one, and never moves one to the other end of a
   cell. Whether the markers *mean* anything for where cell text sits is WI-0002's decision and
   is not implemented here.

## Consequences

Easy: a document with alignment markers survives WI-0001 with its rendering unchanged, and
WI-0002 becomes a change to where padding goes rather than a repair of something WI-0001 broke.
Idempotence holds for marked tables too, because decision 2 keeps every composed delimiter row
recognisable by the same recogniser that produced it.

Hard: `verify` must read AC4 against WI-0001's `## Out of scope` rather than on its own, and a
reader who checks only the criterion will think the code disagrees with it. The mitigation is
this ADR and the `## Risks` entry in `artifacts/plan.md`; the honest note is that AC4 would have
been better written with the words "a delimiter cell that carries no marker" in it, and `plan`
may not edit a criterion after `ready` [src: WI-0001].

Reversibility: high. All three decisions live in one delimiter-composing function; changing them
changes one file and no data. Decision 2's minimum width is visible only in a table with an empty
marked column, which is why it is recorded rather than left to be rediscovered.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T21:47:00Z | plan | WI-0001 | First version, resolving AC4's literal text against WI-0001's Out of scope, ADR-0003 decision 10 and WI-0002's Out of scope |
