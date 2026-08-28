---
title: Compute the whole set of moves before making any of them
version: 2
status: current
updated: 2026-08-27T16:40:00Z
updated-by: review-close
updated-for: WI-0001
---

# ADR-0002 — Compute the whole set of moves before making any of them

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 has two modes, and three of its criteria are about the relationship *between* them:
AC8 requires that applying produces exactly the set of destinations the preview printed, AC10
requires that a collision rename is visible in the preview before it happens, and AC12 requires a
second apply to be a no-op. The vision states the preview is the product's central promise rather
than a convenience flag [src: docs/product/vision.md].

The naive shape — walk the folder and, per file, either print a line or move it — satisfies each
mode separately and makes the relationship between them a coincidence: the two paths compute
destinations with two pieces of code, and the collision suffix in particular is easy to compute in
the mover and forget in the printer. A preview that is *usually* right is worse than no preview,
because the user has been invited to trust it.

## Options considered

- **A — One function computes an ordered list of actions for a folder; both modes consume that
  list.** Preview renders it; apply renders it and executes it. Cost: an intermediate data type
  and one more module. Risk: low; the risk it removes is the two modes drifting apart, which is
  the failure the product cannot survive.
- **B — One walk with a boolean `dry_run` parameter threaded through it.** Cost: none up front.
  Risk: every future branch has to remember to check the flag, and WI-0002 and WI-0003 both add
  branches to exactly this code. This is the shape that produces a preview which is right for the
  simple cases and wrong for collisions — the case WI-0001 requires the preview to get right
  [src: WI-0001 AC10].
- **C — Preview by running the real thing against a copy of the folder.** Cost: copying the whole
  folder. Risk: unusable on a folder of any size, and it would report destinations computed on a
  copy whose collision state can differ from the original's.

## Decision

The tool is built in two layers, and destinations are computed in exactly one of them.

1. `tidy/planner.py` exposes `build_plan(folder) -> list[Action]`. It reads the directory and
   computes, for every entry directly inside it, one `Action` describing what would happen:
   its kind (`move` or `leave`), the source name, and — for a `move` — the destination
   path relative to the folder, **including the collision suffix already resolved**, and whether a
   suffix was applied. It performs no writes of any kind, which is what makes it safe for the
   preview to call [src: WI-0001 AC4].
2. `tidy/apply.py` exposes `apply_plan(folder, actions)`. It executes an action list it is given
   and computes nothing: it never decides a destination.
3. Preview is `build_plan` followed by rendering. Apply is `build_plan`, rendering, then
   `apply_plan` over the same list produced by the same call.

A third kind, `skip`, was specified here and never built: `build_plan` emits **no action at all**
for a hidden file or a subfolder rather than an action saying it skipped one
[src: tidy/planner.py; src: WI-0001 AC11; src: WI-0001 AC13]. That is stronger than what this ADR
asked for — AC13 requires a hidden file to appear in neither mode's output, and an entry that
produces no `Action` cannot be rendered by mistake — so the omission stands and this paragraph
records it. Nothing else in the decision changes.

Because apply builds its plan from the folder's state at the moment it runs, AC8 holds by
construction for the case it states — preview, then apply over an unchanged folder — rather than
by two pieces of code agreeing.

## Consequences

What becomes easy: AC8 and AC10 become properties of the structure rather than things to test for
separately [src: WI-0001 AC8; src: WI-0001 AC10]; the collision suffix is computed once, so the
preview cannot name one thing and the move do another; `build_plan` is a pure function over a
directory listing, so most of WI-0001's criteria can be tested without moving a file; and WI-0002
and WI-0003 both change destination *selection* only, which is one function in one module.

What becomes hard: the whole action list is held in memory before anything moves, so a folder with
millions of entries would need a different shape. WI-0001's criteria describe a downloads folder or
a desktop [src: docs/product/vision.md], so this is recorded as a risk in the plan rather than
designed around.

Reversibility: **cheap.** Collapsing the two layers back into one walk is a local change to two
modules with no interface outside the package and no on-disk format to migrate. The reason not to
is the drift this prevents, not the cost of undoing it. The direction that would be expensive to
reverse is the opposite one — discovering after WI-0002 and WI-0003 have added branches that the
preview and the mover disagree.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-27T16:40:00Z | review-close | WI-0001 | D12 audit at close: the decision named a `skip` action kind the implementation never emits. Recorded what was built instead and why it is stronger; the decision itself is unchanged |
| 1 | 2026-08-27T16:03:05Z | plan | WI-0001 | First version |
