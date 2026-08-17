---
title: The --top and --sort combination is left unspecified
version: 1
status: current
updated: 2026-08-17T00:05:00Z
updated-by: plan
updated-for: WI-0003
---

# ADR-0009 — The --top and --sort combination is left unspecified

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —

## Context

WI-0003 adds `--sort name` / `--sort count`. WI-0002 already delivered `--top N`. Both flags can
be given at once, and the two obvious readings select **different files**:

- `--top` picks the N largest and `--sort name` orders those N for display;
- the name order is applied first, so `--top N` returns the N alphabetically first.

On a folder holding `big.txt` (90 lines), `mid.txt` (50) and `apple.md` (3), `--top 2 --sort name`
gives `big.txt, mid.txt` under the first reading and `apple.md, big.txt` under the second.

The human was asked at refinement, with both readings and that worked example. He declined to
decide, and — separately — declined to have the analyst decide and record an assumption in his
name: "I don't want to pick, and I don't want you picking and then writing it down as though it
were decided … Leave it genuinely open. I'll tell you what I want the first time I actually type
both flags together, and not before." The exchange is in
`tracker/items/WI-0003/artifacts/refinement-qa.md` (Q2), tagged `[unresolved]`, and the
instruction is carried in the item's `## Notes`.

So the architect arrives at a design question whose *product* answer is deliberately absent, and
which no skill downstream may ask about: the item's `## Notes` instruct `plan` and `implement` not
to file a question, because escalating it would get it decided by someone other than him.

This ADR exists because the alternative is worse: a reader six months from now finds a tool whose
two flags interact in a way nothing explains, and cannot tell whether it was chosen, overlooked,
or a bug.

## Options considered

- **A — implement "the N largest, alphabetised".** Sort by count, slice, then re-sort the slice by
  name. Cost: three lines and a second sort, plus a criterion nobody agreed to; it is the reading
  the analyst proposed and the human specifically refused to bless. Risk: it becomes the recorded
  behaviour by default, and the record shows the analyst's preference dressed as a requirement —
  precisely the outcome the human objected to.
- **B — implement "the N alphabetically first".** Sort by the requested key, then slice, which is
  what today's `main` already does with the sort key made variable. Cost: nothing; no code is
  added. Risk: on most folders it returns small files and answers nothing useful, so it may well be
  the reading he rejects when he first types both flags.
- **C — reject the combination with an error.** Cost: a criterion and a message. Risk: it forbids
  something he might have wanted, on no authority, and is the least reversible of the three — an
  error message is an interface people script against.
- **D — specify nothing, add no code for the combination, and constrain only its *shape*.** AC9
  requires exit 0, at most N rows, and WI-0002 AC3's labelled total, all of which A and B satisfy
  equally. Cost: the tool has one input combination whose output is not defined by any criterion.
  Risk: a reader mistakes the incidental behaviour for a contract — which is what this ADR is
  written to prevent.

## Decision

**Option D.** The plan adds no code whose purpose is to make the combination come out one way. The
`rows[:top]` slice in `main` is left exactly as WI-0002 wrote it, and the only change near it is
that the sort above it now takes its key from `--sort`.

The consequence, which is a fact about today's code and **not** a commitment: with the slice
untouched, `--top N --sort name` selects the N alphabetically first files — option B's behaviour,
arrived at by writing nothing rather than by choosing it. No criterion asserts it, `verify` will
observe it under AC9 without judging it, and nothing in the tracker may cite it as settled.

## Consequences

- The tool has exactly one input combination whose output is not fixed by an acceptance criterion,
  and it is documented here, in `WI-0003/item.md` `## Notes`, and in the plan's `## Risks`.
- AC9 guarantees the combination cannot ship as a traceback or a non-zero exit, so the undefined
  region is bounded: the shape is specified even though the content is not. That is what makes it
  safe to leave open rather than reckless.
- When the human states what he wants, it is a **new item** under EP-001, not a bug — nothing here
  is being violated. If instead he reports a crash, that *is* a bug, because AC9 forbids it.
- **Reversibility: cheap, in either direction.** Reaching option A is one line — re-sort the slice
  by name before formatting, in `main`, touching no other function and no other criterion. Reaching
  option C is a guard clause in `main`. Neither requires `format_report`, `sort_rows`,
  `parse_sort`, `count_lines` or `list_files` to change, and neither affects any output that any
  existing criterion pins.
- The cost is carried by whoever reads the code without the tracker: the interaction looks
  arbitrary, because it is. This ADR is the pointer that makes it explicable, which is why the plan
  and the item both cite it by number.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-17T00:05:00Z | plan | WI-0003 | First version |
