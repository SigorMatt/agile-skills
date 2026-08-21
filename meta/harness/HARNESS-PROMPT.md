# Harness builder — mission kickoff prompt

Paste everything below the line into Claude Code, launched at the root of the
agile-skills repository (which must contain meta/harness/DESIGN.md and
meta/harness/PROJECT-QUEUE.md before you start).

---

You are building the **two-session iteration harness** for this repository, per
the agreed design in `meta/harness/DESIGN.md`. Read that document and
`meta/harness/PROJECT-QUEUE.md` in full before writing anything. The harness
lets the owner run hardening iterations unattended: a driver script alternates
a headless worker session (running the rendered pipeline in a throwaway
project) with a headless simulated-human session (answering as a stakeholder),
until a stop condition.

## Operating rules

1. This repository's standing discipline applies to you: CLAUDE.md, checkpoint
   discipline (meta/CHECKPOINT.md before each unit, small commits, clean tree
   between units), the meta/ journal and ADRs, restart protocol if you are
   resuming. Continue the existing META-### numbering for your build tasks.
2. Autonomy as before: decide and record ADRs; ask the human only for seed-doc
   contradictions or irreversible external actions.
3. Verify by execution. Nothing counts as done until a script or a real run
   exercised it.
4. Verify current Claude Code headless specifics (claude -p flags, permission
   modes for non-interactive runs, model selection per invocation) against the
   official docs before writing the driver; record confirmations in an ADR.

## Deliverables (structure per DESIGN.md; decide details, record ADRs)

- `harness/provision.py` — mechanical throwaway-project setup, no agent
  session: create the project directory (location configurable, default a
  sibling `throwaway/` root outside this repo), git init + initial commit,
  run the toolkit installer, workspace-init, merge the USAGE §4 allow-list,
  commit. Idempotent; refuses to touch a non-empty unexpected directory.
- `harness/run_iteration.py` — the driver per DESIGN §2: worker turn / status
  check / sim turn loop; stop conditions (epic done; blocked with no recourse
  in the probe script; validator failure; max-turns budget — make the budget a
  flag); iteration log recording every turn's command, duration, and observed
  status; the contamination assertions from DESIGN §4 (worker never reads
  harness/, sim writes only permitted files) — implement them as real checks
  on the turns' file access where feasible, and at minimum as post-turn audits
  of the project tree and logs.
- `harness/skills/simulated-human/` — the sim skill per DESIGN §3: SKILL.md
  (how to be a human), plus `personas/` and the per-project probe scripts
  supplied by PROJECT-QUEUE.md. The sim consumes the project's board and open
  human-addressed questions, answers through the pipeline's question/answer
  files exactly as a human would, and appends to SIM-LOG.md. It must mark
  every planted-probe action as planted in SIM-LOG.md, so findings can
  separate coverage hits from organic failures.
- Turn prompts for worker and sim as versioned files under `harness/prompts/`,
  including the F-008 interim protocol for the worker (write human questions
  via the question mechanism and stop; consume answers next turn). The worker
  prompt must instruct: state on disk only, no reliance on chat context, stop
  reasons to HARNESS-STATUS.md.
- `harness/USAGE.md` — how the owner runs an iteration end to end: provision,
  run, where the logs are, how to review (project trail + SIM-LOG + iteration
  log), how to adjust personas/probes between iterations, quota notes
  (two sessions per iteration; budget max-turns).

## Acceptance (all verified by execution, evidence committed)

- [ ] provision.py produces a project that passes validate-workspace and has
      the skills discoverable by a fresh session.
- [ ] One **mini end-to-end iteration** against the real toolkit on
      PROJECT-QUEUE iteration 1 (expense splitter), run to at least: intake +
      refinement completed through the async protocol, one work item reaching
      `done`, and at least one planted probe consumed — or to a stop condition
      with the reason correctly reported. Full artifacts committed under
      meta/harness/evidence/ (project trail copy, SIM-LOG, iteration log).
- [ ] Contamination assertions demonstrably fire on a deliberate violation
      (test fixture), and pass on the real run.
- [ ] Driver restart works: kill the driver mid-iteration, rerun, it resumes
      the same iteration from disk state without corrupting the trail.
- [ ] harness/USAGE.md verified by following it literally for the mini run.
- [ ] scripts/check still passes; nothing in methodology/ or spec/ was
      modified. If the harness work surfaces toolkit defects, file them as
      findings (continue F-011 onward) — do NOT fix the toolkit in this
      session; the harness must work against the toolkit as it is, or stop at
      a stop condition and say so.

When the checklist is green: meta/harness/FINAL-REPORT.md — what was built,
key decisions, defects found (as findings), and the exact command sequence for
the owner to launch full iteration 1. Then stop.

Begin: read the two harness documents, plan your units in meta/plan.md, and
proceed.
