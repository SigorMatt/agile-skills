# Setup Report — agile-skills toolkit

Prepared by a throwaway setup session on 2026-08-21. This session installed and verified the
toolkit only. It did **not** start the pipeline, invoke any skill, or discuss the project idea.

---

## 1. Environment

| Check | Result |
|-------|--------|
| `python3 --version` | 3.12.3 (USAGE.md §1 requires 3.9+) |
| `git --version` | 2.43.0 |
| Target is a git repository | Yes — `/home/msi/git_2/flying_squirrel` |

The repository existed but had **zero commits** and an empty working tree. USAGE.md §1 requires
more than a `.git` directory: an item's code history is reconstructed with `git log --grep
<ITEM-ID>`, and `workspace-init` reads the trunk branch. A minimal `README.md` was created and
committed as `Initial commit` to give the repository a real HEAD on `main`.

---

## 2. What was installed, and where

**Toolkit source** — cloned to `/home/msi/git_2/agile-skills` (a sibling of this project, not
inside it, so the installer's output and the project's own record stay separate).

| | |
|-|-|
| Origin | `https://github.com/SigorMatt/agile-skills.git` |
| Commit | `60c5457` — *meta: mission complete (refs META-071)* |
| Pipeline version | `0.1.0` |

`python3 adapters/claude-code/render.py` was **not** run. USAGE.md §2 marks it optional
("regenerate dist/ (optional; it is committed)"), and the committed `dist/` was installed as-is.

**Dry run** (USAGE.md §2), executed first and shown in full:

```
install: agile-skills -> /home/msi/git_2/flying_squirrel
  would copy dist/skills/answer-questions -> .claude/skills/answer-questions
  would copy dist/skills/implement -> .claude/skills/implement
  would copy dist/skills/intake -> .claude/skills/intake
  would copy dist/skills/next -> .claude/skills/next
  would copy dist/skills/plan -> .claude/skills/plan
  would copy dist/skills/refine -> .claude/skills/refine
  would copy dist/skills/review-close -> .claude/skills/review-close
  would copy dist/skills/verify -> .claude/skills/verify
  would copy dist/agile-skills -> .claude/agile-skills
  would copy hooks -> .claude/agile-skills/hooks
  would registered 2 PreToolUse hook(s) in .claude/settings.json
install: 11 action(s)
```

**Real install** performed the same 11 actions and reported `installed methodology pipeline
0.1.0`. Installed paths in this project:

```
.claude/skills/<skill>/SKILL.md + references/contract.md   × 8
.claude/agile-skills/VERSION | pipeline.yaml | skills/ | spec/ | scripts/ | hooks/
.claude/settings.json                                      2 PreToolUse hook entries
```

Per-skill versions from `.claude/agile-skills/VERSION`:
`next 0.1.0`, `intake 0.1.1`, `refine 0.1.1`, `plan 0.1.1`, `implement 0.1.0`, `verify 0.1.1`,
`review-close 0.1.2`, `answer-questions 0.1.1`.

---

## 3. Verification results

**The eight skills** are present under `.claude/skills/`, each with a `SKILL.md` carrying valid
frontmatter (`name`, `description`, `metadata.methodology-skill`, `methodology-version`):

`answer-questions`, `implement`, `intake`, `next`, `plan`, `refine`, `review-close`, `verify` — 8/8.

The adapter README warns that a same-named **personal** skill in `~/.claude/skills/` wins a
collision. That directory does not exist on this machine, so no skill is shadowed.

**Validator before initialisation** (USAGE.md §2 — "Before the workspace exists it will tell you
so, which is the correct answer"):

```
validate-workspace: checked 0 item(s), 0 document(s)
tracker/items: ERROR [items.missing] tracker/items/ does not exist
tracker/project.yaml: ERROR [project.missing] tracker/project.yaml does not exist
    hint: run scripts/workspace-init to create the workspace skeleton
validate-workspace: 2 errors, 0 warnings
EXIT: 1
```

Substantively the correct answer — the workspace is uninitialised and it says so. See finding
§5.2 for how it is presented.

**Validator after initialisation:**

```
validate-workspace: checked 0 item(s), 0 document(s)
tracker/project.yaml: WARNING [project.commands.test-null] commands.test is null, so the tests-pass gate will be recorded as skipped
    hint: plan must set it or record an ADR saying why the project has no tests
tracker/project.yaml: WARNING [project.description] project.description is empty
    hint: workspace-init leaves it null; intake fills it in
validate-workspace: 0 errors, 2 warnings
EXIT: 0
```

0 errors. Both warnings are the documented pre-intake/pre-plan state: `intake` fills the
description, `plan` fills `commands.test`.

---

## 4. Workspace and permissions

`workspace-init` created 8 paths: `tracker/`, `tracker/items/`, `docs/`, `docs/product/`,
`docs/architecture/`, `docs/architecture/adr/`, `docs/process/`, and `tracker/project.yaml`.

**The `null` command fields in `tracker/project.yaml` were not touched** — `commands.test`,
`commands.lint`, and `commands.build` are all still `null`, and `project.description` is `null`.
`plan` and `intake` own those.

**Permissions** (USAGE.md §4): the suggested 8-entry allow-list was merged into
`.claude/settings.json` under `permissions.allow`, preserving the installer's 2 `PreToolUse` hook
entries verbatim. `dontAsk` was **not** enabled and `bypassPermissions` was **not** added.

---

## 5. Findings for the toolkit author

Deviations from USAGE.md, or places where following it exactly does not produce what it promises.
Passages are quoted verbatim.

### 5.1 §3's "commit the workspace" cannot be done as written

> Commit the workspace with your project. It belongs in the repository.

`workspace-init` creates six directories with no files in them — `tracker/items/`,
`docs/product/`, `docs/architecture/adr/`, `docs/process/`, and the `docs/`, `docs/architecture/`
parents (which survive only because of their children). Git does not track empty directories, so
of the 8 paths created, **only `tracker/project.yaml` is committable**. On a fresh clone the
skeleton is missing and the very first `validate-workspace` fails with `items.missing` — the same
error this report shows in §3 for an uninitialised workspace.

No `.gitkeep` was added here, because that would mean inventing files the toolkit does not
create. A `.gitkeep` in each leaf directory, written by `workspace-init`, would fix it.

### 5.2 §2's "correct answer" is indistinguishable from a fault

> Before the workspace exists it will tell you so, which is the correct answer.

What actually arrives is two hard `ERROR` findings and **exit status 1**, immediately after the
installer printed success. Only the `hint: run scripts/workspace-init to create the workspace
skeleton` line distinguishes "you have not initialised yet" from "your workspace is broken". A
distinct exit code, or an `INFO`-level `workspace.uninitialised` finding, would make the expected
state readable without prose.

### 5.3 §2's skill-listing verification cannot run in the installing session

> In the project, start your agent session and ask what skills are available.

Skills are loaded at session start. The session that runs the installer cannot see what it just
installed — the check silently reports *nothing installed* in exactly the situation the reader is
in when they reach that line. Verification here was done by directory listing plus frontmatter
inspection instead. The instruction should say to restart the session first, or offer the
filesystem check as the primary method.

### 5.4 §2's clone command does not name the repository

> ```bash
> git clone <this repository> agile-skills
> ```

`<this repository>` is a placeholder in a document that lives inside the repository it refers to.
The actual URL (`https://github.com/SigorMatt/agile-skills.git`) is not given in USAGE.md, so a
reader following it literally has to go find it. Minor, but it is the first command in the file.

### 5.5 The allow-list's first entry uses a different glob form from the other seven

> ```json
> "Bash(python3 .claude/agile-skills/scripts/*)",
> ```

The other seven entries use the `:*` argument form (`Bash(git status:*)`). This one uses a bare
`*` with no `:` separator. It was merged **verbatim** as USAGE.md gives it and was **not** tested
against a real invocation, so this finding is low confidence — but if the two forms are not
equivalent, the entry that matters most (the pipeline's own tooling, the one command the pipeline
runs constantly) is the one that would fail to match.

### 5.6 Running the validator writes bytecode into the installed tree

`validate-workspace` imports from `.claude/agile-skills/scripts/lib/`, which produces
`__pycache__/*.pyc` inside the installed tooling. A plain `git add -A` after the documented
verification steps sweeps five `.pyc` files into the project's first commit.

The toolkit's own repository ignores these (its `.gitignore` has `__pycache__/` and `*.pyc`), but
the installer does not carry that protection into the target project. A `.gitignore` with those
two lines was added here before the first commit, so no bytecode was ever tracked. The installer
could append the same two patterns to the project's `.gitignore`, or set
`sys.dont_write_bytecode` in the script entry points.

---

## 6. Your next step

**Do not continue in this session.** Skills load at session start, so this session cannot see the
eight skills it just installed.

1. Start a **new** Claude Code session in `/home/msi/git_2/flying_squirrel`.
2. Paste the full contents of `/home/msi/git_2/agile-skills/CONSUMER-PROMPT.md`.
3. State your idea.

`intake` and `refine` will then interrogate you — that is the intended behaviour, and per USAGE.md
§5 the questions are where most of the value is. Answering "whatever you think" is allowed; it is
recorded as an assumption, marked as one.

`EXPERIENCE-LOG.md` is at the project root with empty sections to fill during the run. The
manual-interventions section is worth filling **as things happen** rather than reconstructing
afterwards.

Useful by hand at any point:

```bash
python3 .claude/agile-skills/scripts/validate-workspace .   # is the record sound?
python3 .claude/agile-skills/scripts/board-gen .            # refresh tracker/board.md
```
