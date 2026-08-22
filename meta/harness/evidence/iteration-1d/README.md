# Iteration 1d — the post-fix regression run

Run 2026-08-22T01:33:23Z … 04:01:33Z against the toolkit as of commit `d4b80e9`+ (builder session
two, clusters 1/2/3/6 complete). Config: `harness/iterations/iteration-1d-expenses.json`.
Probe: `harness/skills/simulated-human/probes/iteration-1d-expenses.md`. Persona:
`cooperative-pm`. Project: `expenses-1d`, provisioned from nothing with `provision.py --wipe`.

## What it was for

The regression test for clusters 1, 2 and 6 at once, and the fifth attempt at reaching `blocked`.
1c's probe already made the import non-negotiable and the sample never arrive; 1d adds the one
escape 1c found — the stakeholder now also refuses **every alternative to the sample**, including
a design that needs no sample at all.

## Outcome

**STOP: `blocked-no-recourse`** at turn 16 — `blocked: WI-0003; no question is open to the human`.

| | |
|---|---|
| turns | 16 (10 worker, 6 sim) |
| wall clock | 148 minutes |
| cost | **$71.75**, no turn with unknown cost |
| tool calls | 837 |
| contamination violations | **0** |
| final board | WI-0001 `done`, WI-0002 `done`, BUG-0001 `done`, WI-0003 `blocked`, EP-001 `open`, 0 open questions |

Worker turns averaged 854s / 76 tool calls / $7.05, against iteration 1's turn 4 alone at 3603s
and 255 tool calls. Worker stop reasons seen were `turn-budget-exhausted` and
`human-question-open` — never `error`, never `validator-failed`.

## What it proved

- **`blocked` executed.** Five runs, first time. The row and the reasoning are in
  `project/tracker/items/WI-0003/history.md`; `resume-to: draft` is recorded and the recovery is
  written down.
- **The Definition of Ready override probe fired** for the first time (SIM-LOG turn 5).
- **`claims-are-sourced` (F-001) refused real prose and passed after 12 citations were added**
  (turn 6), and `review-close`'s claim audit caught a false claim that had already reached three
  documents (turn 12).
- **F-013's epic suspension executed** on turn 2 — `EP-001 open → awaiting-answer, resume-to: open`.
- **H-006's turn bound fired** repeatedly and cleanly; **H-007's impasse closing turn** (added
  while configuring this run) fired on its first real occasion.
- Timestamps throughout are clock reads; no fabricated headers, and no `journal.status.unmatched`.

## What it found

Twenty-plus findings, filed as F-025 … F-048 in `meta/findings/FINDINGS.md`. The two that matter
most: **F-045** — the epic sign-off gate does not fire on a run that ends in an impasse, confirmed
by the stakeholder going looking for the question and not finding it — and **F-037**, where a rule
added in this same session made the append-only invariant unsatisfiable.

## Layout

| Path | What |
|------|------|
| `run/SIM-LOG.md` | the stakeholder's own log, `[PLANTED:` vs `[ORGANIC]` |
| `run/iteration-log.jsonl` | the driver's record: every turn, its cost, its observed workspace |
| `run/state.json` | the final driver state, including the stop |
| `run/*.status.md` | each worker turn's self-report, including `skills_run` |
| `project/tracker/`, `project/docs/` | the workspace as the run left it |
| `project/git-log.txt` | the project's commit history |

Read-only history. Do not edit anything under this directory.
