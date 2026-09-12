# Iteration 5b — `droll`, the E4 regression that found a deadlock instead

**Stopped on `turn-budget` at turn 20. E4 was not reached.** This directory is the live evidence
for **H-023**.

The run's purpose was the first live test of E4 — the abandonment ending declared after a
stakeholder goes silent. The persona is `ghosting-founder`, and the silence worked: turns 9
through 20 were twelve consecutive `sim` turns, every one a scripted refusal to answer
`WI-0002/Q-001`. The ending did not follow.

## What this is evidence of

`run/iteration-log.jsonl` holds **eleven identical reschedule events**, turns 10–20 —
`worker → sim`, `because: "unanswered human questions"`, `questions: ["WI-0002/Q-001"]`. The
driver scheduled a worker turn eleven times and the answers-first guard sent every one to the
sim.

Halt rounds are written by `next`, which runs only on a worker turn. So:

- `tracker/waiting/EP-001.md` records **one** round — at `21:33:38Z`, *before* the silence
  began, and broken by the `answer-questions` at `21:43:51Z`. Against the silence that mattered,
  the count is zero.
- The threshold is **3** (`pipeline.yaml`, `silence.threshold_rounds`).
- `engagement-state` therefore never reported `abandoned`, and the guard's own release condition
  — pending *and* gone — could never become true, because detecting "gone" needs the worker turn
  the guard is withholding.

A closed loop, and precisely the one ADR-0011 names as E4's reason to exist: *asking a
stakeholder who is gone, getting nothing, and repeating until the budget is spent.*

The harness test `test_the_undeclared_abandonment_never_routes_another_turn_to_the_sim` asserts
the correct behaviour and passes — by constructing `observed` with the abandonment already
detectable, which is the one state a live run cannot reach unaided. A green test over an
unreachable precondition; F-105's shape, relocated into the driver.

## What is NOT here

- **No E4, no termination statement, no `review-close`.** EP-001 is still `open` with three
  history rows. Nothing lists delivered or orphaned children, because nothing ended.
- **No retro artifact.** `next` never dispatched `retro`, because the engagement never ended.
  The post-E4 retro path is still uncovered, and this run did not cover it.

## Layout

- `tracker/` — the workspace tracker at the stop, including `waiting/EP-001.md`, the finding's
  own evidence.
- `docs/` — the product, architecture and process documents as they stood.
- `run/` — `state.json`, `SIM-LOG.md`, `iteration-log.jsonl`, `driver-console.log`.
- `stop-report.md` — the ops session's report at the stop, with the watch report verbatim, the
  E4 items answered one by one, and the OOM diagnosis that confirmed the stop was clean.

Per-turn `*.stream.jsonl` transcripts are not banked — 20 of them, large, not the record.
No retro exists in this workspace to withhold or to bank.

## This run is the live regression for H-023's fix

The run is stopped on `turn-budget`, which is **resumable**: its own stop detail says so, and
the engagement is not at an ending. That makes it the regression case. Once the guard yields
after a fruitless sim turn, a plain resume with a raised budget must reach E4 from exactly this
state — a silent stakeholder, an unchanged unanswered set, and one stale round in the waiting
log. If it does not, the fix is not done.

This directory is read-only history. Corrections to anything stated here belong in the findings
ledger, not in these files.
