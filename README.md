# agile-skills

An agile software development lifecycle, encoded as versioned agent skills.

Give an agent session these skills and a raw idea. It will interrogate you until the idea is
actually specified, then design, implement, verify, review and close the work — leaving behind
the record a disciplined human team would leave in a tracker, a wiki and git.

This is not a prompt collection. Each skill has a machine-readable contract: what it must read,
what it must produce, which gates must pass, and where the work goes next. A validator enforces
the schemas, and a transition script refuses to move an item whose gates are failing.

---

## Why

Agents are good at doing the work and bad at leaving evidence of it. Ask one to build a feature
and you get a feature; ask it what it decided and why, six steps later, and you get a
plausible reconstruction. That is fine for a script and useless for anything a team has to
maintain.

The bet here is that the discipline of a well-run team — refine before building, design before
coding, verify independently of implementing, review before merging, and write it all down —
is largely *procedural*, and procedure is exactly the thing you can encode.

Three properties follow, and everything in this repository serves them:

1. **State is on the filesystem, never in the conversation.** Any session can resume mid-pipeline
   by reading files. An interruption costs at most one repeated step.
2. **"Done" is a command that exits 0 wherever it can be.** Where it genuinely cannot — "did you
   check each acceptance criterion independently?" — the gate says so and demands recorded
   evidence, rather than pretending to be executable.
3. **Every action is attributable to a skill.** When a run goes wrong you can find which skill,
   at which step, made the decision that caused it — and fix the skill.

---

## How it works

Eight skills over a status graph:

```
      intake ─────► draft ──refine──► ready ──plan──► planned ──implement──► in-progress
                                                                                 │
                                                                            implement
                                                                                 ▼
   done ◄──review-close── in-review ◄──verify── verifying
                                        │
                                        └─ verify fails → back to in-progress
                                        └─ verify finds a defect elsewhere → new BUG item

   any non-terminal status ──(blocking question filed)──► awaiting-answer
                                                                │
                                              answer-questions ─┘ → back to the recorded status
```

- **`next`** is the orchestrator. It reads statuses, questions, priorities and dependencies,
  consults `pipeline.yaml`, and dispatches exactly one skill. It knows no engineering
  whatsoever — that constraint is why a scheduling decision can never hide a judgement nobody
  can audit.
- **`intake`** and **`refine`** talk to the human. Everyone else does not: `implement`,
  `verify` and `review-close` file a question artifact addressed to the architect and stop, and
  **`answer-questions`** resolves it from the record, deciding where it can and escalating only
  under four stated conditions.
- Answers must land in artifacts — the plan, the criteria, an ADR — not in chat. A question
  marked answered whose consequences changed no file is the most damaging thing this design can
  produce, so a gate checks for it.

The workspace it creates inside your project:

```
tracker/
├── project.yaml            commands and conventions the gates resolve
├── board.md                generated; a stale board is a build failure
└── items/<ID>/
    ├── item.md             what is wanted, and the acceptance criteria
    ├── history.md          every status change: when, by which skill, why
    ├── journal.md          every execution: what was read, decided, run, and which gates passed
    ├── questions/          what was unclear, and which files the answer changed
    └── artifacts/          plan, implementation report, verification report, review
docs/
├── product/                vision, PRD
├── architecture/           overview and ADRs
└── process/
```

---

## Layout of this repository

| Path | What it is |
|------|-----------|
| [`methodology/`](methodology/) | The runtime-neutral method: 8 skills as `skill.yaml` + `process.md`, and `pipeline.yaml`. No runtime, vendor or product is named here, and a linter enforces that. |
| [`spec/`](spec/) | The schemas: IDs and statuses, item, journal and history, questions, doc headers, Definition of Ready and Done, the skill contract, the workspace layout. |
| [`adapters/`](adapters/README.md) | The adapter contract, and [`claude-code/`](adapters/claude-code/README.md): a renderer, an installer, gate wiring, and an honest table of what is hard-enforced versus convention. |
| [`scripts/`](scripts/) | Standard-library Python only. Validator, board generator, gate runner, gated transition, workspace and item scaffolding, and `check` — the repository's own gate. |
| [`examples/toy-project/`](examples/toy-project/) | A complete run from idea to done, with its whole paper trail, plus an independent audit of it. |
| [`meta/`](meta/) | How this repository was built: an append-only journal, ADRs, and the evidence for each acceptance claim. |
| [`USAGE.md`](USAGE.md) · [`CONSUMER-PROMPT.md`](CONSUMER-PROMPT.md) | Install it, and the prompt that drives it. |

---

## Try it

```bash
python3 adapters/claude-code/install.py /path/to/your/project
cd /path/to/your/project
python3 .claude/agile-skills/scripts/workspace-init .
```

Then paste [`CONSUMER-PROMPT.md`](CONSUMER-PROMPT.md) into an agent session and state your idea.
[`USAGE.md`](USAGE.md) covers permissions for long runs, reading the record, and resuming.

To see what a finished run looks like before committing to one, read
[`examples/toy-project/`](examples/toy-project/) — and in particular its
[`AUDIT.md`](examples/toy-project/AUDIT.md), which is a reconstruction of the whole run by an
agent given nothing but the tracker, the docs and the git log.

---

## What this is not

- **Not a coding agent.** It is the process around one. The `implement` skill assumes something
  competent is writing the code; the value here is what happens before and after.
- **Not sprint ceremonies.** No planning poker, no estimates, no retrospectives yet. v1 proves
  the flow end to end; depth comes after.
- **Not multi-item parallelism.** `next` dispatches one action at a time, on purpose: two skills
  running before state is written leaves a workspace nobody can reconstruct.
- **Not a guarantee of quality.** It guarantees that the checks were run and the reasoning was
  recorded. Those are different things, and conflating them would be exactly the overclaim the
  whole design exists to avoid.

---

## Roadmap

The intended loop is: run it on something real, read the paper trail, find where a skill misled
itself, fix that skill, bump its version, re-render, run again. Skills carry semantic versions
precisely so that loop is trackable.

Next, roughly in order:

1. **A second adapter** (Codex CLI first). The contract in [`adapters/README.md`](adapters/README.md)
   is written so this needs no change to `methodology/`; if it does, that is a defect to fix
   there.
2. **Deepen the thin spots.** `plan` and `review-close` carry the most judgement and the least
   machine support.
3. **Retro-driven self-improvement** — a skill that reads a completed epic's paper trail and
   proposes contract changes.
4. **Sprint ceremonies and estimation**, once single-item flow is boring.
5. **Multi-item parallelism**, which needs a real answer to conflicting branches first.

Weaknesses we already know about are listed in
[`meta/FINAL-REPORT.md`](meta/FINAL-REPORT.md) rather than left for you to discover.

---

## Contributing

Change `methodology/` or `spec/`, never the rendered output. Then:

```bash
./scripts/check
```

It runs the library self-test, lints every contract against the spec, asserts the validator
still catches all 44 findings in the deliberately broken fixture, re-renders the adapter and
diffs it against what is committed, and validates the example workspace. If you change a skill,
bump its version in the same commit.
