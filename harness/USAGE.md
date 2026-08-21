# Running an iteration

The harness runs a hardening iteration unattended: one headless session executes the pipeline in
a throwaway project (the **worker**), another plays the human stakeholder (the **sim**), and a
driver takes turns for them until a stop condition. You review the result afterwards — the
project's own paper trail, the stakeholder's log, and the iteration log — then adjust the human
and run the next one.

Design and rationale: [`../meta/harness/DESIGN.md`](../meta/harness/DESIGN.md).
Queue of projects: [`../meta/harness/PROJECT-QUEUE.md`](../meta/harness/PROJECT-QUEUE.md).
Execution decisions (flags, permission modes, contamination):
[`ADR-0005`](../meta/adr/ADR-0005-harness-execution-model.md).

---

## 1. Before the first run

- `claude` on `PATH`, logged in. The driver runs `claude -p`; it does not manage credentials.
- Python 3.9+. Nothing else — no packages (ADR-0002).
- A clean toolkit: `./scripts/check` passes, and `adapters/claude-code/dist/` is current. The
  worker runs the **rendered** skills, so an unrendered change to `methodology/` is not in the
  run.

Each iteration costs two sessions' worth of quota per turn pair, and a turn is a full agent
session. Budget with `--max-turns` and, if you want a hard ceiling, `--max-budget-usd`.

---

## 2. Provision the throwaway project

```bash
harness/provision.py --iteration iteration-1-expenses
```

It creates `~/agile-skills-throwaway/expenses` (override with `--root` or
`HARNESS_THROWAWAY_ROOT`), makes it a git repository with its own identity, installs the
rendered skills, initialises the workspace, merges the `USAGE.md` §4 allow-list, and commits.
Re-running it is safe; pointing it at a directory that already has someone else's work in it is
refused unless you pass `--force`.

Two flags worth knowing:

- `--dry-run` prints what it would do.
- `--trust` registers the project in `~/.claude.json`. Without it, Claude Code **ignores the
  `permissions.allow` entries** in the project's `.claude/settings.json` for every headless run,
  because a `-p` session never shows the workspace-trust dialog. That does not matter while the
  worker runs with `bypassPermissions` (the default), and it matters entirely if you want the
  allow-list itself to be what the run tests.

---

## 3. Run the iteration

```bash
harness/run_iteration.py --iteration iteration-1-expenses
```

Turn order: the sim opens the engagement by writing `IDEA.md`, then worker and sim alternate.
The driver prints each turn's tool calls as they happen, and after every turn prints the exit
code, duration, tool count and cost.

Useful flags:

| Flag | Why |
|------|-----|
| `--max-turns N` | the turn budget for the whole iteration (default: the iteration config's) |
| `--worker-model` / `--sim-model` | default `opus` and `sonnet` |
| `--max-budget-usd X` | per-turn spend cap, passed to `claude` |
| `--turn-timeout S` | kill a single turn after this many seconds (default 3600) |
| `--worker-permission-mode` | default `bypassPermissions`; the project is a throwaway |
| `--fresh` | archive the existing run for this iteration and start over |
| `--root DIR` | where the throwaway projects live |

**Stopping and resuming.** Rerun the same command. The run directory is derived from the
iteration id and `state.json` says whose turn it is; a turn that was interrupted is simply run
again, because every pipeline skill reconciles with what it finds on disk. If the driver was
killed hard enough to orphan its `claude` child, the next run kills the orphan before resuming
and says so. Two drivers cannot run the same iteration at once — the second refuses.

---

## 4. Where everything lands

```
harness/runs/<iteration>/
  state.json                      whose turn it is, and why the run stopped
  iteration-log.jsonl             one JSON object per turn
  SIM-LOG.md                      the stakeholder's own log
  turns/NNN-<role>.stream.jsonl   the turn's full transcript
  turns/NNN-<role>.stderr.txt     whatever the CLI wrote to stderr
  turns/NNN-worker.status.md      the worker's self-report for that turn
```

Run directories are git-ignored. Copy the ones worth keeping into
`meta/harness/evidence/<run>/` and commit them there.

---

## 5. Reading a run

In this order, because each answers a different question:

1. **`tracker/board.md` in the project** — where the work got to.
2. **`SIM-LOG.md`** — what the stakeholder was asked, what they answered, and what they
   withheld. Every action carries `[PLANTED: <probe>]` or `[ORGANIC]`: planted actions that the
   pipeline handled are **coverage**, and anything that went wrong without a planted cause is a
   **defect**. Do not file a finding without checking which one you are looking at.
3. **`iteration-log.jsonl`** — the mechanical view: durations, costs, denials, the driver's
   observed status after each turn, and any line where the worker's self-report disagreed with
   the workspace.
4. **The item trail** — `history.md` for what happened, `journal.md` for why, `questions/` for
   what was unclear and where the answer landed.

The last one is the point of the exercise. The harness proves the pipeline ran; only the trail
shows whether it ran *honestly*.

---

## 6. Adjusting the human between iterations

Everything about the stakeholder is in files, so a change is reviewable in git:

- `harness/skills/simulated-human/SKILL.md` — how any human behaves.
- `harness/skills/simulated-human/personas/<name>.md` — this iteration's character.
- `harness/skills/simulated-human/probes/<name>.md` — the idea, and the planted probes.
- `harness/iterations/<id>.json` — which persona and probe an iteration uses, its turn budget
  and models.

The driver renders the chosen persona and probe into `harness/.claude/skills/simulated-human/`
before each sim turn, so the sim always reads exactly the files you edited.

Adding an iteration: write the probe script, add the config, and add the queue entry to
`meta/harness/PROJECT-QUEUE.md` with its rationale.

---

## 7. The contamination boundary

The worker must never see the harness; the sim must never do anything a stakeholder could not.
Both are checked after every turn from the turn's own transcript, and again against the project
tree:

| Rule | Fires when |
|------|-----------|
| W1 | a worker tool call names the harness directory or this repository |
| W2 | a worker tool call names a token only harness content contains |
| W3 | a worker tool call names a path outside the project |
| W4 | this repository changed while a turn was running |
| S1 | the sim wrote outside `IDEA.md`, a question's `## Answer`, or its own log |
| S2 | the sim used a shell, an agent, or the network |
| S3 | a question's frontmatter changed, or a question disappeared |

A violation stops the run with `stop_reason: contamination` and the offending tool input in the
log. `harness/tests/test_harness.py` — a step in `./scripts/check` — feeds each rule a
transcript that must be rejected and one that must be accepted, so a rule that stops working
fails the gate instead of passing a run.

---

## 8. After an iteration

1. Read the run (§5) and decide, action by action, coverage or defect.
2. Append findings to `meta/findings/FINDINGS.md` as F-011 onward, each citing evidence in the
   committed run.
3. If they warrant a toolkit change: fix `methodology/` or `spec/`, bump the skill version,
   re-render, `./scripts/check`.
4. Move to the next `PROJECT-QUEUE` entry. A re-run of the same entry after fixes is a new
   iteration with the same entry.

---

## 9. When something goes wrong

**The run stops immediately with `turn-failed`.** Read
`turns/NNN-<role>.stderr.txt` and the `result_text` in the log line. Authentication, an invalid
flag and a spend cap all land here.

**`blocked-no-recourse`.** An item is `blocked` and nothing is open to the stakeholder, so no
sim turn could help. This is a legitimate end to an iteration — check whether it was a planted
probe (`SIM-LOG`) before treating it as a defect.

**`stalled`.** Three turns in a row changed nothing in the workspace. Usually the worker is
stopping without doing anything: read its `HARNESS-STATUS.md` files in order.

**The worker's status file disagrees with the tracker.** The driver logs it and believes the
tracker. It is a finding about the worker prompt or about the toolkit, not something to fix by
hand in the project.

**A turn hangs.** `--turn-timeout` kills it; the driver records `exit=-1` and stops. Resume with
the same command.
