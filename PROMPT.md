# Mission Kickoff Prompt

Copy everything below the line into Claude Code, launched in an empty directory that contains the `seed/` folder.

---

You are building **agile-skills**: a versioned, runtime-portable agent skill set that encodes a complete agile SDLC, so that a *future, separate* Claude Code session can take a raw product idea from a human, refine it interactively, and drive it autonomously through architecture, implementation, verification, and review — behaving like a full software team whose members document everything they do.

Read all seed documents before writing any code, in this order:

1. `seed/00-VISION.md` — what this is and why
2. `seed/01-REQUIREMENTS.md` — what must exist when you are done
3. `seed/02-ARCHITECTURE.md` — how it must be structured
4. `seed/03-ACCEPTANCE.md` — the definition of done for THIS session

## Operating rules for this session

1. **Autonomy.** Work until the acceptance checklist in `seed/03-ACCEPTANCE.md` is fully green. Do not stop to ask the human anything unless (a) you find a genuine contradiction between seed documents, or (b) an action would be irreversible outside this repo. For every other open question: make a reasonable decision, record it as an ADR in `meta/adr/`, and continue.
2. **Git discipline.** Initialize a git repo immediately. Commit in small, coherent units with messages of the form `<scope>: <summary> (refs META-###)`. Never squash away the history — the history is part of the deliverable.
3. **Dogfood the paper trail.** Before building anything, create `meta/` (per `02-ARCHITECTURE.md` §7) and track your own build there: a task list, an append-only journal, and ADRs. You are the first worker whose work must be reviewable; hold yourself to the same documentation standard the skills will impose on future agents.
4. **Verify by execution, not by reading.** A skill, schema, or adapter counts as done only when a script or a real run has exercised it. The acceptance test (a toy project driven end-to-end through the rendered skills) is mandatory, not optional.
5. **Use fresh eyes for the acceptance test.** When running the toy project through the pipeline, spawn subagents that receive ONLY the rendered skills and the consumer prompt — no memory of how you built them. If a subagent gets confused, that is a defect in the skills, not in the subagent. Fix the skill, re-render, re-run.
6. **Verify Claude Code specifics against current docs.** Before writing the adapter, fetch the current skills documentation via the docs map at https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md and confirm the exact SKILL.md frontmatter fields, skill discovery paths, hook events, and the user-question mechanism. Do not rely on memory for these details; record what you confirmed (with URLs) in `meta/adr/`.
7. **Blocked means documented.** If something is truly impossible, write it to `meta/BLOCKERS.md` with what you tried, why it failed, and a proposed workaround — then continue with everything else. An empty or near-empty BLOCKERS.md is expected at the end.
8. **Scope guard.** Thin end-to-end beats deep-and-partial. Resist gold-plating any single skill; every skill must exist and work before any skill gets deepened.
9. **Checkpoint discipline (limit resilience).** The human's subscription limits may cut this session off at any moment, without warning; structure your work so any interruption costs at most one small work unit. A work unit is ONE committable increment — one `meta/plan.md` task or less (e.g., one skill contract, one process.md, one spec file, one script). If a plan task cannot be finished in a single small commit, split it in `meta/plan.md` before starting. The unit cycle is strict: (a) BEFORE starting, overwrite `meta/CHECKPOINT.md` with the unit's META-### ref, its steps, its done-criteria, and what unit comes next; (b) do the work; (c) verify, commit, tick `meta/plan.md`, journal, and advance `meta/CHECKPOINT.md` to the next unit. Never leave the working tree dirty between units, and never depend on chat context for state: every unit must be startable by a fresh session that has read only PROMPT.md, `meta/plan.md`, and `meta/CHECKPOINT.md`.
10. **Context hygiene.** This session runs in the model's standard context window, whatever its size, and may be auto-compacted at any time; treat compaction as routine, exactly like a session restart. Immediately after any compaction, re-read `meta/CHECKPOINT.md` and `meta/plan.md` before taking further action — do not trust your summarized recollection of where you were. Keep the main context lean: rely on workspace files rather than conversation scrollback (re-read a file instead of recalling it), avoid dumping large file contents into responses, and delegate context-heavy bulk work — generating many similar files, verbose test/validation runs, the toy-project pipeline runs — to subagents, keeping only their concise results in the main thread.

## If this session is a restart

If `meta/` already exists, you are resuming an interrupted run. Do not re-plan from scratch. Read `meta/CHECKPOINT.md`, `meta/plan.md`, and the tail of `meta/journal.md`, then run `git status` and `git log --oneline | head`. If the working tree is clean, start the checkpointed unit. If it is dirty, the previous session died mid-unit: review the diff against the checkpoint's done-criteria — finish the unit only if it is trivially close to done; otherwise revert all uncommitted changes and redo the unit from the checkpoint (units are sized so a redo is cheap). Journal the recovery either way.

## Deliverable summary (details in seed docs)

- The `methodology/` layer: 7 runtime-neutral skills (intake, refine, plan, implement, verify, review-close, answer-questions) + orchestrator (`next`), each as `skill.yaml` contract + `process.md` procedure, plus `pipeline.yaml`.
- The `adapters/claude-code/` build step that renders methodology into installable Claude Code skills, plus a documented adapter contract that a future `adapters/codex-cli/` can implement.
- The filesystem workspace spec (`tracker/` = Jira-equivalent, `docs/` = Confluence-equivalent) with schemas, plus scripts that lint/validate all of it.
- `examples/toy-project/` — a completed end-to-end run with its full paper trail, kept in the repo as living proof and as reference output.
- `USAGE.md` and `CONSUMER-PROMPT.md` — everything the next Claude Code session (and eventually the community) needs to install the skills into a fresh project and start from a raw idea.

When the acceptance checklist is green, write `meta/FINAL-REPORT.md` summarizing what was built, key decisions, known weaknesses, and recommended next iterations — then stop.

Begin now: read the seed docs, set up `meta/`, write your build plan, and proceed.
