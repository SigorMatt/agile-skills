# CHECKPOINT

## Current unit — META-075

`harness/prompts/` — the two versioned turn prompts.

**Steps**
1. `worker-turn.md` — points at the project's own `CONSUMER-PROMPT.md` (the real thing under
   test) and states the async amendments: the human is not in the session and has no question
   tool; questions go through the question mechanism addressed to `human`, item suspended, stop;
   filled-in `## Answer` sections are consumed through `answer-questions` FIRST, before `/next`;
   state on disk only, never chat; stop reason and open human questions to `HARNESS-STATUS.md`
   with a fenced JSON block for the driver; never read outside the project.
2. `sim-turn.md` — invoke `/simulated-human`, name the project path, the SIM-LOG path, the turn
   number, and which job this is (open the engagement / answer).
3. Both files carry a version line; the driver logs which version it used.

**Done when** — both prompts exist, `scripts/check` passes, tree clean.

**Next unit** — META-076, `harness/run_iteration.py`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
