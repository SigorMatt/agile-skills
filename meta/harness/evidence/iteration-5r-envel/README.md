# Iteration 5r — `envel-2`, the held-out calibration engagement

**E1 delivered, at turn 35, after a `turn-budget` resume.** The run reached turn 30, stopped on
its budget with the engagement not at an ending, was resumed in place with `--max-turns 40` on
the owner's instruction, and declared its ending five turns later. `stop-reason: epic-done`,
`stop-detail: 8 item(s), all done`.

This is the re-run of the engagement abandoned as iteration 5, whose trail is banked beside this
one at `meta/harness/evidence/iteration-5-envel-abandoned/`. That run died at turn 11 on a
`validator-failed` stop. **This one hit no validator-failed stop at any point**, and ADR-0014's
self-repair allowance was never engaged.

## The retro is deliberately withheld

`tracker/items/EP-001/artifacts/retro.md` exists in the local workspace at
`/home/msi/agile-skills-throwaway/envel-2/`, **39887 bytes**, and is **NOT in this directory**.
That is deliberate, not an oversight and not a copy failure.

This is the **held-out calibration**: the protocol is that the owner reviews this trail and
writes their findings down **before** anyone reads the retro's report, so that the retro can be
scored against an independent reading rather than against one it has already shaped. A retro
banked here would be a retro someone could read first, which destroys the measurement — so the
exclusion is by construction in the copy, not by a sweep afterwards.

Verification, at the time of banking:

```
$ find meta/harness/evidence/iteration-5r-envel -iname "*retro*"
$ echo "find-exit=$?"
find-exit=0
```

Empty output, exit 0, stderr not discarded. The same pattern run against the source workspace
returns `tracker/items/EP-001/artifacts/retro.md`, so the absence above is a real absence rather
than a pattern that matches nothing.

**The retro will be added in a follow-up commit, after the owner has posted their findings.**
Until that commit lands, this directory is the whole of what the owner is meant to have seen.

## Layout

- `tracker/` — the workspace tracker at the ending, **minus the retro artifact**.
- `docs/` — product, architecture and process documents, including the two `## Engagement state`
  sections `review-close` restated from this ending.
- `run/` — `state.json`, `SIM-LOG.md`, `iteration-log.jsonl`, `driver-console.log`.
- `stop-report.md` — the ops session's report at the stop: the watch report verbatim, the state
  line, the turn-budget stop and its resume, the ending, and the two things worth carrying into
  the review.

Per-turn `*.stream.jsonl` transcripts are not banked — 35 of them, large, and not the record.

## Reading order for the held-out review

1. `run/SIM-LOG.md` — what the stakeholder did and said.
2. `tracker/board.md` and `tracker/items/EP-001/history.md` — where it ended and how it got there.
3. `docs/product/vision.md` §`Engagement state` — the termination statement. It names **no
   deferred child**: *"None was deferred and none was abandoned."* The monthly summary was parked
   as further work, which is not the same thing, and the difference is what separates this ending
   from E2's signature.
4. The item trail for anything that looks wrong.
5. **Write the findings down. Then, and only then, read the retro.**

This directory is read-only history. Corrections to anything stated here belong in the findings
ledger, not in these files.

Retro added in this follow-up commit after the owner's held-out review (see conversation record 2026-09-11); note: the retro's journal entry in EP-001/journal.md was inadvertently banked with the trail, partially breaching the embargo — six of ten proposal classifications were visible to the owner pre-review; scoring carries that footnote.

Fuller measure (2026-09-11): the line above says six of ten. The banked journal entry also states the aggregate split outright — seven `toolkit-defect`, two `project-circumstance`, one `observation` — and enumerates all seven toolkit-defects in substance in its Result bullet, naming eight proposals by P-number (P-1 through P-5, P-8, P-9, P-10). All ten classifications were therefore derivable pre-review, not six; six is the count that carried an explicit classification by number. Scoring should discount against the larger figure.
