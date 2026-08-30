# Usage

How to install the skills into a project, run the pipeline, read what it leaves behind, and
resume after an interruption.

If you only want the short version: install, paste [`CONSUMER-PROMPT.md`](CONSUMER-PROMPT.md),
state your idea.

---

## 1. Requirements

- **Python 3.9+** on `PATH`. Nothing else — no packages, no virtualenv, no lockfile. That is a
  deliberate design constraint ([ADR-0002](meta/adr/ADR-0002-scripting-and-dependencies.md)):
  the validator runs as a quality gate, and a gate that fails because a package is missing is
  indistinguishable, to the agent running it, from a gate that fails because the work is wrong.
- **git**, and the target project must be a git repository. An item's code history is
  reconstructed with `git log --grep <ITEM-ID>`, so the pipeline needs one. A purely local
  repository is fine; no remote is required.
- An agent runtime with an adapter. Today that is
  [`adapters/claude-code/`](adapters/claude-code/README.md).

---

## 2. Install

```bash
git clone <this repository> agile-skills
cd agile-skills

python3 adapters/claude-code/render.py                              # regenerate dist/ (optional; it is committed)
python3 adapters/claude-code/install.py /path/to/your/project --dry-run
python3 adapters/claude-code/install.py /path/to/your/project
```

The installer is idempotent, merges into an existing `.claude/settings.json` instead of
overwriting it, and prints everything it touched. What it places is listed in
[`adapters/claude-code/README.md`](adapters/claude-code/README.md) §2.

To remove it later:

```bash
python3 adapters/claude-code/install.py /path/to/your/project --uninstall
```

Uninstall leaves `tracker/` and `docs/` alone. Those are your project's record; the tooling is
replaceable, the record is not.

### Verify the install

**Skills are discovered when a session starts, so the session that ran the installer cannot see
them.** Asking it what skills are available will list whatever it loaded before the install, and
the answer will be wrong in a way that looks like a broken install (F-004). Two checks, in this
order:

**Now, in this session — the file-level check.** This is the one that tells you the install
worked:

```bash
cd /path/to/your/project
ls .claude/skills/                                        # eight directories
head -3 .claude/skills/intake/SKILL.md                    # frontmatter with name: intake
python3 .claude/agile-skills/scripts/validate-workspace .
```

`validate-workspace` on a project you have not initialised yet exits **3** and says so. That is
the expected answer at this point, not a failure — exit 1 means a workspace that exists and is
wrong, and exit 0 means a clean one.

**In a NEW session — the discovery check.** Start a fresh agent session in the project and ask
what skills are available. You should see the nine: `intake`, `refine`, `plan`, `implement`,
`verify`, `review-close`, `answer-questions`, `retro`, `next`.

Before the workspace exists it will tell you so, which is the correct answer.

---

## 3. Initialise the workspace

```bash
python3 .claude/agile-skills/scripts/workspace-init .
```

This creates `tracker/` and the `docs/` directories, and writes `tracker/project.yaml` with the
project name and trunk branch filled in and the commands left as `null`.

**Leave the `null`s alone.** `plan` fills in `commands.test` and `commands.lint` when it decides
how the project is built, and a null command makes the matching gate report **skipped** rather
than passed. Inventing a test command that does not exist would make every subsequent gate
report a pass for a check nobody runs.

Commit the workspace with your project. It belongs in the repository.

---

## 4. Permissions for long autonomous runs

The pipeline runs many commands over a long session, and the rendered skills deliberately do not
pre-approve tools for you — pre-approving shell access for a skill that runs arbitrary project
commands is a decision you should make knowingly.

Practical options, in increasing order of trust:

| Setup | Effect | Good for |
|-------|--------|----------|
| Default (Manual) | You approve each action | The first run, while you are watching |
| Allow-list specific commands in `.claude/settings.json` `permissions.allow` | Only the pipeline's own tooling runs unattended | Steady use — see the suggested list below |
| `auto` mode | Long runs with background safety checks | Multi-hour autonomous runs |
| `bypassPermissions` | No checks at all | Isolated containers only |

**Do not use `dontAsk` mode while `intake` or `refine` are expected to run.** That mode denies
the tool those skills use to question you, and the fallback — print the questions and stop —
turns an interactive refinement into a dead end.

A reasonable allow-list to start from, covering the pipeline's own tooling but not your project's
build:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 .claude/agile-skills/scripts/*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git checkout:*)",
      "Bash(git branch:*)"
    ]
  }
}
```

Add your project's test and lint commands once you trust the loop.

**These entries do nothing until the project is trusted.** A `-p` / headless session never shows
the workspace-trust dialog, and Claude Code discards a `permissions.allow` block wholesale from a
workspace that has never been trusted:

```
Ignoring 8 permissions.allow entries from .claude/settings.json: this workspace has not been
trusted. Run Claude Code interactively here once and accept the trust dialog, or set
projects["<dir>"].hasTrustDialogAccepted: true in ~/.claude.json.
```

One stderr line, and then the setup recommended above is silently off — which presents as
unexplained permission prompts or denials in the middle of a long run (F-012). Two ways to
satisfy it, and you need one of them **before** the first headless run:

- open the project interactively once and accept the trust dialog; or
- set `projects["<absolute path>"].hasTrustDialogAccepted: true` in `~/.claude.json`.

`--settings` and `--allowedTools` are honoured either way, because they are supplied explicitly
on the command line rather than read out of the workspace.

### Publishing the product without the record

The workspace lives beside the code on purpose, and that is the wrong shape for a release.
Deleting `tracker/` in a later commit does not remove it — git keeps everything — so there is a
command that copies out instead:

```bash
python3 .claude/agile-skills/scripts/export ../my-project-release --profile architecture
```

It reads your workspace, writes a **new** directory, and initialises a fresh repository there
with one commit and no prior history. Your repository is not touched, rewritten or rebased.

| Profile | Ships | For |
|---------|-------|-----|
| `product` | code only; `(refs WI-0007)` stripped from the commit subject | a release where the process is nobody's business |
| `architecture` *(default)* | code + `docs/`, so the ADRs and the overview travel | open source, or handing over to maintainers |
| `full` | everything including `tracker/` | handing the whole engagement to someone else |

Before committing, it refuses outright if any workspace file reached the copy, and it *reports*
any citation pointing back at `tracker/` — those are references produced by the claim-provenance
rule, not disclosures, and they will simply not resolve in the copy. `--strict` refuses on those
too. `--dry-run` lists what would go.

---

## 5. Run it

Paste [`CONSUMER-PROMPT.md`](CONSUMER-PROMPT.md) into the session and state your idea. Then:

- **`intake` and `refine` will interrogate you.** That is the point. The questions are where
  most of the value is, and the record of your answers is what the rest of the pipeline builds
  on. Answering "whatever you think" is allowed — it is recorded as an assumption, marked as
  one, so nobody later mistakes it for a requirement.
- **After refinement, the loop runs itself.** `next` picks one action, the skill does it, `next`
  runs again.
- **It stops when it should.** A question addressed to you, nothing runnable, or the epic done.

You can also drive it by hand at any point:

```bash
python3 .claude/agile-skills/scripts/board-gen .        # refresh the board
python3 .claude/agile-skills/scripts/validate-workspace . # is the record sound?
```

and invoke a skill directly with `/plan`, `/verify`, and so on.

---

## 6. Reading the paper trail

Start at `tracker/board.md` — every item, its status, what is blocking it, and every open
question with the human-addressed ones first.

Then, for any item:

| File | Answers |
|------|---------|
| `tracker/items/<ID>/item.md` | What was asked for, and how we will know it is done |
| `tracker/items/<ID>/history.md` | The timeline: every status change, when, by which skill, why |
| `tracker/items/<ID>/journal.md` | The detail: what each skill read, decided, ran, and which gates passed |
| `tracker/items/<ID>/questions/` | What was unclear, who decided it, and which files changed as a result |
| `tracker/items/<ID>/artifacts/` | The plan, the implementation report, the verification report, the review |
| `tracker/items/<EP-ID>/artifacts/retro.md` | On an epic, after the engagement ended: what the record shows about how the work went, and the toolkit findings it proposes |
| `git log --grep <ID>` | Every commit for that item |

`docs/architecture/adr/` holds the decisions with their alternatives and their reversibility.

The rule of thumb: **`history.md` tells you what happened, `journal.md` tells you why.** Scan
the first; open the second when a line in it surprises you.

**The retrospective is worth reading twice.** Its first half is about your engagement and is
read once. Its second half — `## Proposed toolkit findings` — is written to be lifted out and
sent upstream: candidate defects in the skills, the specs or the scripts, each marked `PROPOSED`
with evidence pointing back into your own record. Nothing is filed on your behalf; a person
decides what travels. Entries classified `project-circumstance` are about your engagement rather
than the toolkit, and they stay where they are.

`examples/toy-project/` is a complete worked example, including
[`AUDIT.md`](examples/toy-project/AUDIT.md) — an independent reconstruction of the run from the
record alone.

---

## 7. Pausing and resuming

Stop whenever you like. All state is on disk.

To resume — in the same session or a new one, days later:

```bash
python3 .claude/agile-skills/scripts/validate-workspace .
python3 .claude/agile-skills/scripts/board-gen .
```

then read the board and run `/next`. Do not summarise where you were from memory; the
pipeline is built so that resuming from the files costs at most one repeated skill execution.

An item at `in-progress` means a branch exists with partial work: `implement` reconciles with
what is there rather than starting over. That distinction is exactly why `planned` and
`in-progress` are separate statuses.

---

## 8. When something goes wrong

**The validator is failing.**

```bash
python3 .claude/agile-skills/scripts/validate-workspace .
```

Every finding carries a `path:line`, a code, and usually a hint. The codes are stable; the
schema behind each one is in `.claude/agile-skills/spec/`.

**A transition is refused.** Read the gate output above the refusal. Three shapes:

- `FAIL` — a real gate failure. Fix the cause.
- `SKIP` — a command is not configured, so the gate checked nothing. Configure it in
  `tracker/project.yaml`, or accept that this check is not running.
- `MANUAL` — a judgement gate. Carry it out and record the evidence in the journal.

If the gate genuinely cannot pass and you want to proceed anyway, add `--force`. The override is
written into the history reason permanently, which is the point: an override you can see is
fine, an invisible one is not.

**An edit was blocked.** Writes to `history.md` and `board.md` are denied on purpose. Use
`transition` and `board-gen`. The block message tells you the exact command.

**The pipeline is stuck.** Run `/next`; it will say which of the four stop conditions applies. If
an item is `blocked`, its last history row says why and its journal says what was tried.

**A skill did the wrong thing.** That is a defect in the skill, not in the run. The journal
names the skill and its version, so you can find the contract that produced it. File it under
`meta/` in this repository, fix the `process.md` or `skill.yaml`, bump the version, re-render,
re-install. That loop is the whole point of the versioning.

---

## 9. Working on the methodology itself

In this repository:

```bash
./scripts/check          # the gate: library self-test, lint-skills, the must-fail fixture,
                         # render determinism, and the example workspace
```

Everything must pass before a change is done. If you change a `skill.yaml` or a `process.md`,
bump that skill's version in the same commit and re-render — `scripts/check` fails on a stale
`dist/`.
