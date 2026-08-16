# Toy project — `linecount`

A complete run of the pipeline, from one under-specified sentence to closed work, kept here as
proof that the methodology works end to end and as a reference for what a correct run looks
like.

Nothing here was written by hand. Every file under `tracker/` and `docs/` was produced by a
skill during the run, and the run was executed by **context-free subagents** — fresh sessions
given only the installed skills, [`../../CONSUMER-PROMPT.md`](../../CONSUMER-PROMPT.md), and the
project path. None of them had any knowledge of how the methodology was built. Where a subagent
got confused, that was treated as a defect in the skill: the skill was fixed, re-rendered and
re-run, and the fix is recorded in [`../../meta/journal.md`](../../meta/journal.md).

## Start here

| If you want to know | Read |
|---------------------|------|
| What was asked for, in the human's own words | [`IDEA.md`](IDEA.md) |
| What the whole run produced, at a glance | [`tracker/board.md`](tracker/board.md) |
| Whether the record actually holds up | [`AUDIT.md`](AUDIT.md) — an independent reconstruction of the run by an agent given only the tracker, the docs and the git log |
| How the human's side was played | [`HUMAN-SCRIPT.md`](HUMAN-SCRIPT.md) |

Then pick any item under `tracker/items/` and read its `history.md` (what happened, in order)
followed by its `journal.md` (why, and what was run).

## Layout

```
IDEA.md            the raw idea, exactly as stated
HUMAN-SCRIPT.md    the answer key the builder used when playing the human, written before the run
tracker/           the tracker the run produced: items, history, journals, questions, artifacts
docs/              the durable knowledge the run produced: vision, architecture, ADRs
src/               the code the run produced
GIT-LOG.md         the run's real git history, as text
GIT-BRANCHES.md    the branches, and `git log --grep <ITEM-ID>` per item
AUDIT.md           the independent reconstruction (acceptance C6)
import.sh          how this directory was produced from the run repository
```

### Why there is no `.git` here

The run happened in a **real, standalone git repository**: real branches (`wi/WI-0001`, …), real
commits carrying item IDs, real merges into the trunk. That repository cannot be committed
inside this one — git would treat a nested `.git` as a submodule and a reader cloning this
repository would get an empty directory. So the history is preserved as text in
[`GIT-LOG.md`](GIT-LOG.md) and [`GIT-BRANCHES.md`](GIT-BRANCHES.md), and the code is under
`src/` rather than at this directory's root.

The reasoning, and the alternatives that were rejected, are in
[`../../meta/adr/ADR-0004-toy-project-execution.md`](../../meta/adr/ADR-0004-toy-project-execution.md).

`src/` holds the files at the paths the run used, so a path named in a plan or a journal —
`linecount.py`, `tests/test_linecount.py` — is found at `src/linecount.py`,
`src/tests/test_linecount.py`.

## Reproducing it

```bash
# in a fresh, empty git repository
python3 /path/to/agile-skills/adapters/claude-code/install.py .
python3 .claude/agile-skills/scripts/workspace-init .
# then paste CONSUMER-PROMPT.md into an agent session and state the idea from IDEA.md
```

You will not get byte-identical output — the skills leave judgement to the worker, which is the
point. What should be identical is the *shape*: the same statuses in the same order, the same
artifacts at the same stages, a question raised rather than guessed at, and a record that
answers the audit questions.
