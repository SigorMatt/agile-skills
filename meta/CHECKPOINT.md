# CHECKPOINT

## Current unit — META-076

`harness/run_iteration.py` — the driver.

**Steps**
1. Run directory `harness/runs/<run-id>/` with `state.json`, `iteration-log.jsonl`, `SIM-LOG.md`
   and `turns/<n>-<role>.stream.jsonl`.
2. Render the active persona/probe into `harness/.claude/skills/simulated-human/` so the sim
   turn can discover the skill; source of truth stays under `harness/skills/`.
3. Turn alternation: sim `open` turn first (the worker has no idea to work on otherwise), then
   worker → driver status check → sim → worker …
4. Driver-computed status: parse `tracker/items/*/item.md` and `questions/*.md`, run
   `validate-workspace`, compare against the worker's `HARNESS-STATUS.md` self-report and log
   any disagreement.
5. Stop conditions: epic done; blocked with no recourse; validator failure; turn budget
   (`--max-turns`); a stalled cycle; a failed turn.
6. Every turn logged with command, prompt version, model, duration, cost, permission denials and
   the observed status.

**Done when** — the driver runs end to end against the provisioned project for at least the
opening sim turn and one worker turn, with the log to show for it. Contamination assertions land
in META-077.

**Next unit** — META-077, the contamination audit and `harness/tests/`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
