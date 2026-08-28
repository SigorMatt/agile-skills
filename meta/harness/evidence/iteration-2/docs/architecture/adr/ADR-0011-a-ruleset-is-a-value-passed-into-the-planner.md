---
title: A ruleset is a value passed into the planner, not module state
version: 1
status: current
updated: 2026-08-27T21:35:54Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0011 — A ruleset is a value passed into the planner, not module state

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

ADR-0010 decides where a user's rules come from. This decides what happens to them once they are
read, and it is a separate decision because the answer would be the same in any format.

What exists today: `tidy/rules.py` holds two module-level constants and a lookup over each —
`DEFAULT_RULES` with `folder_for(filename)`, and `DEFAULT_BANDS` with `band_for(age_seconds)` —
and `build_plan(folder)` calls both [src: tidy/rules.py; src: tidy/planner.py]. `_BY_EXTENSION`,
the inverted index the lookup actually uses, is built once at import time [src: tidy/rules.py].
ADR-0005 chose that shape precisely so this item would have one mechanism for both kinds of rule
rather than two [src: ADR-0005].

The stakeholder's answer to Q-001 is what makes this more than plumbing: their entries **layer
over** the built-in table and win where they collide, and a table they say nothing about keeps its
built-in values [src: WI-0003/Q-001; src: WI-0003 AC6]. So there is a merge, it happens once, and
something has to hold the merged result.

Two existing commitments constrain the answer. Every destination is decided in `planner.py` and
nowhere else [src: ADR-0002], and `cli.py` imports nothing from `rules.py` — the `--help` text is
prose and a test is what keeps it honest [src: ADR-0008].

## Options considered

- **A — Load into the module: `rules.load(path)` rebinds `DEFAULT_RULES` and `_BY_EXTENSION`.**
  Cost: the tables become mutable global state, so what a call to `folder_for` returns depends on
  what ran before it in the same process. Tests have to undo it in `tearDown` or leak into each
  other, and the existing suite calls `folder_for` and `band_for` directly
  [src: tests/test_rules.py]. Risk: high, and of the kind that surfaces as one test failing only
  when the suite is run in a particular order.
- **B — A `Ruleset` value, built once and passed into `build_plan`.** An immutable object holding
  the merged extension index and the two bands, with the lookups as its methods;
  `build_plan(folder, ruleset=None)` takes it and falls back to the built-in one, so that
  everything which does not supply rules behaves exactly as before [src: WI-0003 AC1]. Cost: one
  new parameter on one function, and the two module-level lookups become methods, so their
  existing tests change shape. Risk: low.
- **C — Pass the two tables as two parameters.** Cost: two arguments that must always travel
  together and can be passed inconsistently, and the merge — which needs both, and which is the
  only genuinely new logic in this item — has nowhere to live except its caller. Risk: the seam
  ends up in `cli.py`, which would put part of the destination decision outside `planner.py` and
  contradict ADR-0002 [src: ADR-0002].

## Decision

**Option B.** `tidy/rules.py` gains a `Ruleset`: a frozen dataclass holding `by_extension` (a dict
of lowercase extension to folder name) and `bands` (the ordered pairs ADR-0005 defined), with
`folder_for(filename)` and `band_for(age_seconds)` as methods carrying the bodies those two
module-level functions have today [src: ADR-0005; src: tidy/rules.py].

- `BUILT_IN` is the `Ruleset` built from `DEFAULT_RULES` and `DEFAULT_BANDS`, which stay exactly
  as they are — they are what `README.md` documents and what ADR-0008's help-text guard reads
  [src: ADR-0008; src: tests/test_cli.py].
- `build_plan(folder, ruleset=None)`, resolving `None` to `BUILT_IN` in its body. Every existing
  caller passes nothing and is unaffected [src: WI-0003 AC1]. The default is `None` rather than
  `BUILT_IN` for a reason given below: it is what lets `cli.py` pass a ruleset without importing
  one.
- The merge is one function in `rules.py`, `merge(base, types, bands)`, returning a new
  `Ruleset`: the user's extension entries overwrite the base's by key and add keys it lacks, and
  the user's bands replace the base's pair outright or are absent [src: WI-0003/Q-001;
  src: WI-0003 AC2; src: WI-0003 AC3; src: WI-0003 AC6].

The layering is a dict update on the inverted index, not on `DEFAULT_RULES`. That matters and is
worth stating: `DEFAULT_RULES` maps a folder to its extensions, so redirecting `.csv` by editing
it would mean removing `.csv` from `spreadsheets` and adding a `data` key. Merging on the
extension-to-folder index is a single assignment per entry, and it is why the stakeholder's
"mine win" is one line of code [src: WI-0003/Q-001].

`apply.py` is not touched, and neither is the three-layer shape: rules are still data the planner
consults, and the planner is still the only place a destination is chosen [src: ADR-0002].

**`cli.py` gains `--rules` and a call to the loader, and still imports nothing from `rules.py`.**
ADR-0008 states its own checkable condition as a grep: `grep -n "^from\|^import" tidy/cli.py`
returns no line importing `rules` [src: ADR-0008]. Importing `BUILT_IN` there to pass as a default
would break that condition — quietly, since the help-text test would still pass — so `cli.py`
passes `ruleset=None` when no `--rules` was given and the loader's result when one was, and only
`planner.py` and `ruleset_file.py` import the tables [src: tidy/cli.py; src: ADR-0008]. This is
the single most likely way to get this item wrong in a way no gate catches.

## Consequences

What becomes easy: two runs in one process can use different rules, which is exactly what AC4's
two rule files over the same folder need [src: WI-0003 AC4]. Every rule test becomes a pure
function over a value with no filesystem and no global state. A future item that wants a third
source of rules adds a constructor, not a code path.

What becomes harder: `folder_for` and `band_for` stop being importable module functions, so
`tests/test_rules.py` changes at every call site [src: tests/test_rules.py]. That is a rename in
a test file, not a redesign, but it is real work and it is why option A looks cheaper than it is.

**Reversibility: cheap.** Reversing to A is deleting the parameter and rebinding the constants;
reversing to C is unpacking the dataclass at one call site. One module and its tests either way,
no data on disk, no change to the command line, and nothing a user can observe. What is not cheap
to reverse is the `--rules` flag itself, which is a published interface — but that is ADR-0010's
decision, not this one [src: ADR-0010].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T21:35:54Z | plan | WI-0003 | First version |
