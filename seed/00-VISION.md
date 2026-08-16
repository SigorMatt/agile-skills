# 00 — Vision

## What this project is

**agile-skills** encodes a well-defined agile software development lifecycle as a set of versioned agent skills. Each skill represents a role-activity a human team member would perform (refining a story, designing, implementing, verifying, reviewing), with a formal contract: inputs, outputs, executable quality gates, exit criteria, and escalation paths.

The result is not a prompt collection. It is an **executable methodology**: a new agent session equipped with these skills can take a raw idea, refine it with the human, and carry it to a merged, verified, documented implementation — leaving behind the same reviewable record a disciplined human team would leave in Jira, Confluence, and git.

## Who uses it and how

Two distinct sessions, in sequence:

1. **The builder session** (you, now): builds this repo — methodology, adapters, workspace schemas, validation scripts, example run, consumer docs.
2. **The consumer session** (later, separate): a fresh Claude Code session in a *different* project. The human installs the rendered skills, pastes `CONSUMER-PROMPT.md`, and states an idea. The session grills the human to refine it, then drives the pipeline autonomously, escalating questions to the human only through the defined protocol.

The human will iterate: run a consumer session on a demo application, review the paper trail, find weaknesses, return here to improve the skills, repeat. **Design everything to make that debugging loop easy** — when a consumer run goes wrong, the paper trail must show exactly which skill, which step, and which decision went wrong.

Long-term: open-sourced for the community, and extended with adapters for other runtimes (first candidate: Codex CLI).

## Guiding principles (binding)

1. **Methodology is runtime-neutral.** Skills are written once in a neutral format; adapters render them per runtime. No Claude Code specifics may leak into `methodology/`.
2. **Executable gates over vibes.** Wherever possible, "done" is a command that exits 0, not an agent's self-assessment.
3. **State is on the filesystem.** Skills communicate only through artifacts in the workspace. Any skill can be re-run idempotently; any fresh session can resume mid-pipeline.
4. **The orchestrator knows no engineering.** It schedules skills over workspace state. All engineering judgment lives inside skills.
5. **Paper trail like a human team.** Every action is journaled: what was read, what was decided and why, what was run, what resulted. Someone who was not present must be able to reconstruct and audit the work.
6. **Peers, not a monolith.** Skills are written as if executed by distinct workers (analyst, architect, developer, verifier, reviewer) who hand off through the tracker and raise questions upstream rather than silently guessing.
7. **Thin before deep.** v1 proves the full flow end-to-end. Depth comes in later iterations.
