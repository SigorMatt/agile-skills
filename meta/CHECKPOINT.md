# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Standing instructions (survive session restarts)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
  Journaled under META-035.

## Where the toy run lives

`$CLAUDE_JOB_DIR/tmp/toy/linecount` — a standalone git repository with the rendered skills
installed (ADR-0004). If `$CLAUDE_JOB_DIR` is gone, the run must be re-executed from
`examples/toy-project/IDEA.md` + `HUMAN-SCRIPT.md`; nothing about it depends on this session.

**State as of META-061:** `EP-001` open; `WI-0001` (high) and `WI-0002` (medium, depends-on
WI-0001) both at `ready`; two commits; `validate-workspace` exit 0 with one expected warning
(`commands.test` null until `plan` fills it in).

## Current unit: META-062..067 — the autonomous pipeline run

A single context-free subagent is looping `/next` unattended, with instructions to stop the
moment an item reaches `awaiting-answer`, a human-addressed question opens, nothing is runnable,
or the epic closes.

**Expected shape, and what each stop means:**

| Stop | Unit | What the builder does next |
|------|------|---------------------------|
| `implement` files a blocking question | META-063 done | Dispatch `answer-questions` (META-064) — as the architect, from the record; escalate to the human only under `spec/question.md` §4 |
| `verify` files a BUG | META-065 done | Let the loop carry the bug through plan → implement → verify → review-close (META-066) |
| Epic closed | META-067 done | Import and validate (META-068), then the audit (META-069) |

**After every stop:** journal the unit in `meta/journal.md` with what the skills produced and any
defect the run exposed, tick `meta/plan.md`, commit, push. A skill defect found here is fixed in
`methodology/`, versioned, re-rendered and re-installed — that is META-061a's precedent and the
loop the whole project exists to support.

**Next unit after the run:** META-068 — `examples/toy-project/import.sh`, then
`validate-workspace` on the imported tree and `scripts/check` with the example step no longer
skipped.
