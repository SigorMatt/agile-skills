# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Standing instructions (survive session restarts)

- **The unit cycle ends with `git push`, not `git commit`.** The human instructed on
  2026-08-16: add `git@github.com:SigorMatt/agile-skills.git` as `origin`, push everything, and
  push after every commit from then on. `origin` is configured and `main` tracks it. Journaled
  under META-035.

## Current phase: META-060..069 — the end-to-end proof

**Where the run happens:** in a standalone git repository at `$CLAUDE_JOB_DIR/tmp/toy/linecount`
(outside this repo, because a nested `.git` cannot be committed here — see ADR-0004). When the
run is complete it is imported into `examples/toy-project/` **without** `.git`, together with
`GIT-LOG.md` and `GIT-BRANCHES.md` so the git evidence survives the import.

**How each step is run:** a context-free subagent, given only the installed skills, the
consumer prompt, and the project path — never any memory of how the methodology was built
(PROMPT rule 5). If a subagent gets confused, that is a defect in the skill: fix the skill,
re-render, re-run, and journal the fix.

**Current unit: META-060** — choose the toy project and write the inputs the run needs.

**Steps**
1. Write `meta/adr/ADR-0004-toy-project-execution.md`: where the run happens, why `.git` is not
   imported, and how the git evidence is preserved instead.
2. Create the scratch repository and install the rendered skills into it.
3. Write `examples/toy-project/IDEA.md` — the raw, deliberately under-specified idea, exactly as
   a human would state it.
4. Write `examples/toy-project/HUMAN-SCRIPT.md` — the answer key the builder uses when playing
   the human, with the standing rules for how to answer (be vague where a real person would be,
   so `refine` has something to actually push back on).
5. Commit and push.

**Done criteria**
- ADR-0004, `IDEA.md` and `HUMAN-SCRIPT.md` committed; scratch repo exists with skills installed
  and `validate-workspace` reporting an uninitialised workspace.
- `./scripts/check` still green; tree clean; pushed.

**Next unit:** META-061 — `intake` + `refine` via a context-free subagent, with the builder
answering as the human.
