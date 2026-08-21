# Evidence — driver restart (META-078)

The harness acceptance requires: *kill the driver mid-iteration, rerun, it resumes the same
iteration from disk state without corrupting the trail.* This directory is that run.

It was executed against a scratch copy of the iteration-1 project with **haiku** on both roles —
the cheapest way to get real turns. The models are why the worker's judgement here is not worth
reading; the point is the driver's behaviour, which is model-independent.

## What was done

1. `harness/run_iteration.py --iteration iteration-1-expenses --max-turns 2 --sim-model haiku
   --worker-model haiku`, started in the background.
2. Nine seconds in — while turn 1 (the sim's opening turn) was running — the driver process was
   sent `SIGKILL`.
3. The same command was run again, with no extra flags.

## What was observed

- The kill left the driver's `claude` child **alive**: `SIGKILL` does not reach it, and the
  orphan kept writing to the transcript of a turn nobody was waiting for. This is why
  `run_iteration.py` records each turn's child pid in `turn.pid` and why a resuming driver reaps
  what it finds. Recorded in the log line below as `"reaped-pid": 220639`.
- The rerun resumed from `state.json` rather than starting over:

      {"event": "resume", "from-turn": 0, "next-role": "sim",
       "interrupted": {"job": "open", "role": "sim", "turn": 1}, "reaped-pid": 220639}

- Turn 1 was **re-run**, not skipped: 43s, $0.05, 0 contamination violations, `IDEA.md` written.
- Turn 2 (worker) then ran normally: 479s, $0.89, 0 violations, epic `EP-001` created, `Q-001`
  filed to the human, one commit.
- The run stopped at `turn-budget` — the correct reason for `--max-turns 2`.

## The trail was not corrupted

After the restart, in the project:

    validate-workspace: checked 1 item(s), 1 document(s)
    tracker/items/EP-001/item.md: WARNING [epic.childless] the epic has no child items
    tracker/project.yaml: WARNING [project.commands.test-null] ...
    validate-workspace: 0 errors, 2 warnings

Both warnings are the honest state of a workspace whose intake has just finished. `git log`
shows two commits — the provisioning commit and intake's — with nothing half-written between
them, and `git status` was clean.

## Files here

| File | What it is |
|------|-----------|
| `iteration-log.jsonl` | the whole run: start, resume, both turns, stop |
| `state.json` | final driver state |
| `SIM-LOG.md` | the stakeholder's log — one entry, for the re-run turn 1 |
| `002-worker.status.md` | the worker's own report at the end of turn 2 |
