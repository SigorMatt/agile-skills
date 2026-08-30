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
- **`retro`** runs once after the engagement ends, and it is the only skill that reads the
  record rather than the work. It writes two things and touches nothing else: an
  engagement-local retrospective, every observation cited to the file and line it came from, and
  a set of candidate toolkit findings marked `PROPOSED` for a human to send upstream. The
  stakeholder is not waiting on it — their engagement ended at sign-off. It is the team studying
  itself, and it is how a consumer's real run becomes feedback on the method.

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

## Prior art, and where this sits

**[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** is the established project in
"agile methodology as AI agents": role personas, 34+ lifecycle workflows, planning artifacts,
cross-tool installers, a module ecosystem, MIT-licensed, tens of thousands of stars. If you have
been looking in this space, you have seen it, and anything here that reads as novel should be
measured against it rather than against nothing.

The difference is not features; it is what the process *is*.

| | BMAD-METHOD | agile-skills |
|---|---|---|
| Operating mode | **collaborate and facilitate** — expert personas guide a human through workflows | **delegate and verify** — interrogate the human once at refinement, then run autonomously |
| Process is | instructions, templates and checklists the agent is asked to follow | a status graph, a transition program, hooks that deny bypass writes, gates that exit non-zero |
| The human's seat | throughout, by design | at intake, at refinement, at every escalation, and at epic sign-off |
| What you get at the end | planning documents | a record a stranger can reconstruct the run from — journals, history, question provenance, cited claims |
| Breadth | 34+ workflows across the lifecycle | 9 skills, one flow, deliberately narrow |

Concretely, "enforcement as a program" means: an item cannot reach `done` while a gate is
failing, because the only sanctioned way to change a status is a script that checks the transition
against the state machine and runs the gates first. An override is possible and is recorded in the
history reason forever. Hand-editing the file that holds the status is denied by a hook. None of
that is discipline; it is software, and it behaves the same on the hundredth run as the first.

**Which one you want:**

- You want to stay in the loop, shape the work as it goes, and have expert-shaped agents help you
  think — **use BMAD-METHOD.** It is more mature, far broader, and built for that.
- You want to hand work over, walk away, and be able to audit exactly what happened and on what
  basis — **this.** The narrowness is the point: nine skills, hardened by running them.

They are converging: their roadmap carries "Dev Loop Automation", which is our territory. Our bet
is that autonomy is only worth having if it is trustworthy by construction, and that the way to
keep that is to harden the enforcement kernel faster than automation gets bolted onto
instruction-shaped process.

*BMad™ and BMAD-METHOD™ are trademarks of BMad Code, LLC. This project is independent of it and
contains no code or content derived from it.*

---

## Layout of this repository

| Path | What it is |
|------|-----------|
| [`methodology/`](methodology/) | The runtime-neutral method: 9 skills as `skill.yaml` + `process.md`, and `pipeline.yaml`. No runtime, vendor or product is named here, and a linter enforces that. |
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
- **Not sprint ceremonies.** No planning poker, no estimates, no velocity. There *is* a
  retrospective, but it is a reading of the record rather than a meeting: `retro` runs after the
  engagement ends and reports what the trail shows. Depth on the rest comes after.
- **Not multi-item parallelism.** `next` dispatches one action at a time, on purpose: two skills
  running before state is written leaves a workspace nobody can reconstruct.
- **Not a guarantee of quality.** It guarantees that the checks were run and the reasoning was
  recorded. Those are different things, and conflating them would be exactly the overclaim the
  whole design exists to avoid.
- **Not proven yet, and the bar is written down.** `meta/ROADMAP.md` §2 defines what "proven"
  means here, `meta/findings/FINDINGS.md` is the open list, and
  `meta/harness/evidence/` holds the trails of every run that produced it — including the ones
  that went badly. Read those before trusting any of the above.

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
