# Two-session iteration harness — design

Status: agreed design, not yet built. This document seeds a future harness
builder session. Location when adopted: meta/harness/DESIGN.md.

## 1. Purpose

Run hardening iterations unattended: one Claude Code session executes the
pipeline on a throwaway project using the rendered skills (the **worker**); a
second session plays the human stakeholder (the **sim**). The owner reviews
only end results — project trail, sim log, iteration log — then adjusts and
reruns. Several throwaway projects, until runs are boring.

## 2. Architecture: a driver owns turn alternation

Sessions cannot talk to each other, and they do not need to: the pipeline
already communicates exclusively through the filesystem. A small driver script
(`run_iteration.py`) alternates two headless turns until a stop condition:

- **Worker turn.** Fresh `claude -p` in the throwaway project directory
  (skills installed, workspace initialised). Standard turn prompt: read the
  workspace; if unconsumed human answers exist, record them through the proper
  skill; run /next until a stop condition; write the stop reason and open
  human-addressed questions to HARNESS-STATUS.md. Fresh-per-turn is viable
  precisely because all pipeline state is on disk; the harness is a direct
  consumer of that design guarantee.
- **Sim turn.** Fresh `claude -p` in `harness/`, whose .claude/skills/
  contains the `simulated-human` skill. Input: the project path. It reads
  tracker/board.md and open human-addressed questions the way a stakeholder
  would, answers per its persona and probe script through the answer files,
  and appends to SIM-LOG.md — the automated counterpart of a human tester's
  EXPERIENCE-LOG.md.
- **Driver loop.** worker → check status → (questions for human?) → sim →
  worker → … Stop conditions: epic done; `blocked` with no recourse in the
  probe script; validator failure; max-turns budget. Every turn's command,
  duration, and observed status goes to the iteration log.

## 3. The simulated-human skill project

The sim's behavior must live in versioned files, not prompt text — prompt-borne
persona instructions are the first thing compaction or a fresh turn loses.
Three files:

- **SKILL.md** — how to be a human: terse; answers only what was asked; never
  volunteers unrequested detail; occasionally vague; imperfect memory of own
  earlier answers is permitted, contradictions are not (unless the persona
  says otherwise).
- **persona.md** — this iteration's character: cooperative PM, impatient
  founder, contradictory stakeholder, silent non-answerer. Swapped between
  iterations to widen coverage.
- **probe-script.md** — per-project test plan: which requirement stays
  ambiguous (DoR-override seed), which item's answer is withheld (`blocked`
  seed), which answers are wrong-then-corrected (send-back seed). The
  HUMAN-SCRIPT.md discipline from the toy run, formalised.

"Adjusting the human" between iterations = editing these files, reviewable in
git. Findings must distinguish "the system hit my planted failure" from "the
system failed on its own" — only the second is a defect; the first is coverage.

## 4. Contamination boundary

The worker must never read `harness/` — a worker that can see the probe script
is studying the exam answers. The sim touches only what a real human could:
the board, question files, its own answer files. Enforced by the directory each
turn runs in; the driver asserts (and logs) that no worker turn accessed the
harness directory and no sim turn wrote outside the permitted files.

## 5. Dependency: async human interaction (F-008)

intake/refine are interactive by design; headless runs have no question tool,
and the documented fallback is print-and-stop. Harness v1 handles this at the
prompt level (worker: write questions via the question mechanism and stop;
consume answers next turn) — no toolkit change. F-008 makes async a
first-class toolkit mode later; when it lands, the harness's turn prompts
shrink accordingly.

## 6. Honest scope

The harness exercises pipeline logic, gates, escalation, and the paper trail.
It does NOT test the interactive grilling UX — a scripted sim cannot be
surprised, annoyed, or confused the way the peer can. Manual peer-style runs
remain a complementary track, not a superseded one.

Cost note: each iteration burns two sessions' worth of quota. Budget max-turns
accordingly, and prefer small throwaway projects (see the probe-friendly
project criteria: naturally ambiguous requirements, a plausible missing
external dependency, edge-case-rich logic, stdlib-only).

## 7. Build plan (when scheduled)

A harness builder session receives this document plus a compact mission prompt,
builds `harness/` (driver, sim skill, turn prompts, logs), and proves it with
one mini end-to-end iteration against the real toolkit on a trivial project —
same acceptance philosophy as everything else: verified by execution, trail
committed.
