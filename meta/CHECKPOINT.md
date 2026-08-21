# CHECKPOINT

## Current unit — META-074

`harness/skills/simulated-human/` — the sim's behaviour, in versioned files.

**Steps**
1. `SKILL.md` — how to be a human: terse, answers only what was asked, never volunteers, may be
   vague, imperfect memory allowed but contradictions only when the persona says so. Plus the
   mechanics: read the board and the open `addressed-to: human` questions, write the answer into
   `## Answer` tagged `[human]`, change nothing else, append to `SIM-LOG.md`.
2. `personas/` — `cooperative-pm.md`, `impatient-founder.md`, `contradictory-stakeholder.md`
   (PROJECT-QUEUE names all three).
3. `probes/` — one per queue entry, each carrying the idea as the human will state it and the
   planted probes with their trigger conditions, and the instruction to tag every planted action
   `[PLANTED: <probe>]` in SIM-LOG.
4. The driver renders the active persona/probe to `persona.md` / `probe-script.md` inside the
   discoverable skill directory (DESIGN §3's three files); source of truth stays in
   `personas/` and `probes/`.

**Done when** — the files exist, `scripts/check` passes, tree clean. (Execution evidence for the
sim arrives with the driver, META-076.)

**Next unit** — META-075, `harness/prompts/`.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.
