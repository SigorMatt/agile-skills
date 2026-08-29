# CHECKPOINT

## Current unit: META-129 — waiting on regression 3b, then 4b

**Session:** builder 3. Phase IV of `meta/plan.md`. META-119..128 done and pushed;
`meta/FINAL-REPORT-3.md` §1–§3 written.

**In flight:** `iteration-3b-mdtab`, relaunched 2026-08-29T21:10Z from an empty project after
being stopped at turn 2 and its two brittle `lint-answers` rules fixed (journalled). Project
`~/agile-skills-throwaway/mdtab-3b`; run `harness/runs/iteration-3b-mdtab/`; `--max-turns 30`.
A background waiter reports when `state.json` reaches `stopped`.

**The two runs are sequential, not parallel — H-015.** `render_sim_skill` rewrites one global
directory, `harness/.claude/skills/simulated-human/`, at the start of every sim turn. Two drivers
would interleave a contradictory stakeholder and a cooperative one into both trails. Do not
launch 4b until 3b has stopped.

## What to do next, in order

1. **When 3b stops:** its trail is read-only evidence from that moment. Read
   `harness/runs/iteration-3b-mdtab/SIM-LOG.md` first — the pass condition is the sim saying its
   reserved line, *"the multiline case wins; I over-spoke before"*, in answer to a question that
   quotes both stakeholder answers by ID. Then the item trail, then the console log.
2. **Launch 4b:** `python3 harness/provision.py --iteration iteration-4b-recall` is already done;
   `nohup python3 harness/run_iteration.py --iteration iteration-4b-recall --max-turns 30 &`.
   (Wipe and `--fresh` first if anything has touched `~/agile-skills-throwaway/recall-4b`.)
3. **META-129:** findings pass over both trails; file F-069+ / H-016+; bank both trails under
   `meta/harness/evidence/iteration-3b/` and `iteration-4b/`.
4. **META-131:** the five small fixes accepted in META-128's triage — F-035, F-048, F-054, F-056,
   F-059. Only once no run is in flight: `scripts/` is guarded by the W4 rule.
5. **META-130:** `meta/FINAL-REPORT-3.md` §4, §5, §6 — the ROADMAP §2 verdict, condition by
   condition, with an evidence line for each.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten.
- Toolkit commits and harness commits stay separate.
- **A harness run is in flight.** `meta/` and `harness/` are exempt from the W4 rule; everything
  else trips it and stops the run.
