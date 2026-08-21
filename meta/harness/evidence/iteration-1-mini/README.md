# Evidence — the mini end-to-end iteration (META-080)

PROJECT-QUEUE entry 1, `expenses`, run against the real toolkit at
`~/agile-skills-throwaway/expenses` by following `harness/USAGE.md` literally. Worker: `opus`,
`bypassPermissions`, `AskUserQuestion` removed. Sim: `sonnet`, persona `cooperative-pm`, probe
`iteration-1-expenses`, no shell. Per-turn spend cap `--max-budget-usd 12`.

**It was stopped deliberately at the turn budget once the acceptance targets were met**, not
because the epic finished. Two of three work items are still open. The rest of iteration 1 is
the owner's to run.

## The run, turn by turn

| # | role | job | s | tools | $ | worker's stop_reason | unanswered human Qs after | validator |
|---|------|-----|---|-------|---|----------------------|---------------------------|-----------|
| 1 | sim | open | 14 | 5 | 0.15 | — | 0 | 0 |
| 2 | worker | — | 909 | 53 | 5.34 | human-question-open | 12 | 0 |
| 3 | sim | answer | 128 | 31 | 0.81 | — | 0 | 0 |
| 4 | worker | — | 1700 | 106 | 11.27 | human-question-open | 1 | 0 |
| 5 | sim | answer | 36 | 8 | 0.20 | — | 0 | 0 |
| 6 | worker | — | 1318 | 111 | 10.90 | error* | 0 | 0 |
| 7 | worker | — | 1345 | 113 | 10.85 | error* | 0 | 0 |
| 8 | worker | — | 1278 | 78 | 9.01 | human-question-open | 3 | 0 |

**$48.51 total.** \* Turns 6 and 7 ended cleanly at the per-turn spend cap; the worker reported
`error` because the `stop_reason` enum has no value for "the budget ran out" and said so in
prose. That is a defect in the harness's own prompt, recorded as H-001 in
`meta/findings/FINDINGS.md`.

## What the acceptance asked for, and what happened

| Required | Result |
|----------|--------|
| intake + refinement completed through the async protocol | yes — an epic, three work items, **16 questions** filed to the human across turns 2, 4 and 8, all answered by the sim in the question files and propagated by `answer-questions` |
| one work item reaching `done` | **WI-0001 is `done`** and merged to `main` |
| at least one planted probe consumed | **both** were: `dor-override-rounding` (WI-0003/Q-002, turn 3) and `blocked-bank-csv` (introduced turn 3, sample withheld turn 5) |
| contamination assertions pass on the real run | yes — all eight transcripts, re-audited under the corrected rules, report **0 violations** |

The workspace ends at **0 errors, 0 warnings** from `validate-workspace`, with 4 items and 8
documents.

## What the run exercised that had never executed before

- **`in-review → in-progress`, the review send-back** — three times, organically. `review-close`
  rejected WI-0001 for a dead function and a duplicated rule, and later for an `AC8` violation
  (a store whose people list held a non-string parsed cleanly, then raised `AttributeError` past
  `cli.main`'s `except ExpensesError` — exit 1 with a traceback) that **two verify passes had
  missed**. `implement` fixed each, `verify` re-checked, and the item then closed. This path was
  listed as unexecuted in `meta/FINAL-REPORT.md`; it is not any more.
- **The Definition of Ready override**, seeded by the `dor-override-rounding` probe.
- **The async human protocol end to end**, on every one of the eight turns.

## Findings the run produced

Six, all filed in `meta/findings/FINDINGS.md` with this directory as their evidence: F-011
(`answer-questions`' precondition excludes the human-answered case), F-013 (a blocking question
on an epic is unrepresentable), F-014 (`transition` gates the pre-move workspace), F-015
(`implement` must pass through a red validator), F-016 (epic-level record commits have no home
branch), F-017 (the restamp deadlock exists in `journal.md`, and skills invent timestamps), F-018
(the write guard matches the command string, not the target). Every one was found by the worker
itself and journalled where it happened; F-013 and F-014 were then reproduced by hand.

## Files here

| Path | What it is |
|------|-----------|
| `run/iteration-log.jsonl` | every turn: command shape, prompt version, model, duration, cost, denials, the driver's observed status, the worker's self-report, violations |
| `run/state.json` | the driver's final state |
| `run/SIM-LOG.md` | the stakeholder's log — every action tagged `[PLANTED: …]` or `[ORGANIC]` |
| `run/turns/*.status.md` | each worker turn's own report, including its findings in prose |
| `project/tracker/`, `project/docs/` | the paper trail, as the pipeline left it |
| `project/expenses/`, `project/tests/` | the code, for reading the trail against |
| `project/GIT-LOG.md` | the commit history of `main` and of the merged `wi/WI-0001` |
| `project/IDEA.md` | the sim's opening statement |

The full `stream-json` transcripts (5.1 MB) are **not** committed; they live in
`harness/runs/iteration-1-expenses/turns/` on the machine that ran it. The audit verdicts derived
from them are in `run/iteration-log.jsonl`, which is.
