# ADR-0005 — How the two-session harness executes turns

- **Status:** accepted
- **Date:** 2026-08-21
- **Unit:** META-072

## Context

`meta/harness/DESIGN.md` fixes the architecture: a driver alternates a headless **worker**
session (running the pipeline in a throwaway project) with a headless **sim** session (playing
the human stakeholder), because the pipeline already communicates exclusively through the
filesystem. It does not fix the mechanics — which `claude` flags, which permission mode, how a
turn's file access is observed, where the throwaway project lives, or how the human's answers
physically reach the pipeline. `HARNESS-PROMPT.md` rule 4 requires those to be confirmed against
the current documentation rather than recalled, and recorded here.

Everything in §1 was confirmed twice: against the documentation at the URLs given, and against
the CLI installed on this machine (`claude 2.1.238`), by running it.

---

## 1. Confirmed Claude Code facts

Sources, fetched 2026-08-21:

- docs map — https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md, which now
  **301-redirects** to https://code.claude.com/docs/en/claude_code_docs_map.md. The
  `docs.anthropic.com` address in `PROMPT.md` rule 6 and `ADR-0001` still resolves, via that
  redirect; new work should cite `code.claude.com`.
- headless / programmatic use — https://code.claude.com/docs/en/headless.md
- CLI reference — https://code.claude.com/docs/en/cli-reference.md

| Fact | Confirmed value | How confirmed |
|------|-----------------|---------------|
| Non-interactive invocation | `claude -p "<prompt>"`; exit 0 on success, non-zero on failure | docs; run |
| Structured result | `--output-format json` → one JSON object carrying `result`, `is_error`, `subtype`, `num_turns`, `stop_reason`, `session_id`, `total_cost_usd`, `permission_denials`, `terminal_reason` | run (fields observed, not assumed) |
| Turn-by-turn transcript | `--output-format stream-json --verbose` → NDJSON; every `assistant` message carries `content[]` blocks including `tool_use` with the **full tool input** | run |
| Turn budget | `--max-turns <n>` — print mode only, errors out at the limit. **Not listed in this build's `--help`**, but accepted and honoured | docs; run |
| Spend cap | `--max-budget-usd <amount>` — print mode only | docs; `--help` |
| Permission mode | `--permission-mode` ∈ `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk`, `plan` in this build. Docs additionally list `default` as an alias for `manual`. **`-p` starts in Manual on every plan**, so a mode must be passed explicitly or every tool call stalls | docs; `--help` |
| `dontAsk` semantics | denies anything not matched by `permissions.allow` or the read-only command set, **and denies `AskUserQuestion` even when an allow rule matches** | docs |
| Model per invocation | `--model <alias-or-id>`; alias `opus`/`sonnet`/`haiku`/`fable` | docs; run |
| Tool restriction | `--tools` restricts *which tools exist*; `--allowedTools` only pre-approves them. Two different jobs | docs |
| Extra working directory | `--add-dir <dir>` grants file access outside cwd, and deliberately does **not** load `.claude/` configuration from there | docs |
| Skills in `-p` | user-invoked skills work: put `/skill-name` in the prompt string. Skills are discovered from `<cwd>/.claude/skills/` | docs |
| `--bare` | skips hooks, plugins, MCP, auto-memory and CLAUDE.md discovery | docs; `--help` |
| Session resume | `--resume <session-id>` / `--continue`; `--session-id <uuid>` to fix the ID | docs |

Two consequences worth stating separately, because the harness depends on them:

- **A `-p` session shows no workspace-trust dialog and runs the project's `.claude/settings.json`
  hooks anyway.** The toolkit's `guard-workspace-writes` hooks therefore protect a headless
  worker exactly as they protect an interactive one — the enforcement under test is really under
  test.
- **`--bare` would disable those hooks**, along with skill auto-discovery from the project. The
  harness therefore does **not** use `--bare`, and accepts that the host's `~/.claude` and any
  parent-directory `CLAUDE.md` are loaded. §2.4 is how that is contained.

---

## 2. Decisions

### 2.1 Turn zero belongs to the sim

`DESIGN.md` §2 describes the loop as worker → status → sim. Taken literally the first worker turn
has nothing to work on: the human's idea is not in the project yet. The harness therefore opens
with a **sim turn** that states the idea, exactly as a stakeholder would — it writes
`IDEA.md` in the project root and logs the statement in `SIM-LOG.md`. The idea text lives in the
iteration's probe script, not in the driver, so "what the human asked for" is versioned with the
rest of the human's behaviour.

The alternative — the driver writes `IDEA.md` mechanically — was rejected because it splits
human-authored content across two owners, and the contamination audit's rule "the sim is the
only writer of human words" then has an exception in it from the first turn.

### 2.2 The interaction channel is the toolkit's own question protocol

No new mechanism, and no toolkit change (F-008 stays deferred; this is its documented interim).

- The worker, when it needs the human, files a question artifact per `spec/question.md` with
  `addressed-to: human`, suspends the item (`awaiting-answer`, `resume-to` recorded), and stops.
  Both `intake` and `refine` already specify this as their "the human is not present" path, so
  the harness is using a documented path rather than inventing one.
- The sim answers by writing the human's words into that file's `## Answer` section, tagged
  `[human]` — the tag `refine` already uses in `refinement-qa.md`. It changes nothing else: no
  frontmatter, no status, no other file.
- The worker's **next** turn consumes those answers through `answer-questions`, which propagates
  them into the artifacts and closes the question. `spec/question.md` §3 specifies exactly this
  ("human answers in the file → answer-questions propagates").

The sim never runs a script, never transitions an item, and never commits — it has no `Bash`
tool at all (§2.5). A stakeholder who could run `transition` would not be a stakeholder.

### 2.3 The human is simulated, and the project says so

`provision.py` writes `SIMULATION-NOTICE.md` into the project: the stakeholder is an automated
simulation, and answers arrive asynchronously in question files. This is the same honesty the toy
run practised with `[human — simulated by the builder]` tags, moved onto disk so it survives a
fresh turn. It reveals *that* the human is simulated — which the worker must know anyway to use
the async path — and nothing about the persona or the probes.

### 2.4 The throwaway root defaults outside `~/git`

`HARNESS-PROMPT.md` suggests a sibling `throwaway/` root. A sibling of this repository is
`/home/msi/git/throwaway`, and `/home/msi/git/CLAUDE.md` exists and would be auto-discovered as a
parent memory file by every worker turn — a worker briefed about `trifecta-lens` is a worker
running a contaminated experiment. The default root is therefore
`~/agile-skills-throwaway/<project>`, outside any repository, overridable with `--root` or
`HARNESS_THROWAWAY_ROOT`. The requirement "outside this repo" is met either way; this choice also
meets "outside anything else's context".

### 2.5 Permission modes: the worker is trusted, the sim is caged

- **Worker:** `--permission-mode bypassPermissions`, plus `--disallowedTools AskUserQuestion`.
  The project is a throwaway in an isolated directory, and the run's purpose is to observe the
  *pipeline*, not to observe Claude Code's permission matching. Removing `AskUserQuestion`
  structurally enforces the async protocol: the worker cannot ask a human who is not there, so
  "it asked in chat and the answer vanished" is not a failure mode this harness can produce.
  Overridable with `--worker-permission-mode`; `permission_denials` from the result JSON is
  logged on every turn regardless of mode.
- **Sim:** `--tools "Read,Write,Edit,Glob,Grep"` (no `Bash`, no `Agent`) with
  `--permission-mode acceptEdits` and `--add-dir <project>`. The cage is what makes the
  "sim writes only permitted files" assertion cheap to hold: the only writing tools it has are
  file writes, which the audit reads straight out of the transcript.

### 2.6 Contamination is audited from the transcript, not inferred

Every turn runs with `--output-format stream-json --verbose`, tee'd to
`runs/<run-id>/turns/<n>-<role>.stream.jsonl`. The audit reads every `tool_use` block's input:

- a **worker** turn must not name the harness directory, this repository, or any of the tokens
  that only harness content contains (`simulated-human`, `probe-script`, `PROJECT-QUEUE`,
  `SIM-LOG`);
- a **sim** turn must not *write* outside `<project>/IDEA.md`,
  `<project>/tracker/items/*/questions/Q-*.md` and `<run>/SIM-LOG.md`. Reads outside its
  permitted set are logged as advisory, not fatal.

This is the "real check on the turns' file access" the mission asks for: it observes what the
session actually did, and it is followed by a post-turn audit of the project tree (git status,
validator, and the permitted-write set) so that a violation committed through a channel the
transcript missed is still caught.

### 2.7 The driver computes status itself

`HARNESS-STATUS.md` is the worker's *self-report* (stop reason, open human questions, a fenced
JSON block for the driver). It is recorded and compared, never trusted: the driver derives the
real state by reading `tracker/items/*/item.md` and `questions/*.md` and by running
`validate-workspace`. A disagreement between the two is logged, and is itself a finding about the
worker prompt or the toolkit.

### 2.8 Models

`--worker-model` defaults to `opus` and `--sim-model` to `sonnet`: the worker is the thing whose
competence the run is measuring, the sim is reciting a persona. Both are flags because a finding
that only reproduces on one model is a different finding from one that reproduces on both, and
the iteration log records the model used for every turn.

---

## Consequences

- The harness depends on `stream-json` staying a stable transcript format. If it changes, the
  contamination audit degrades to the post-turn tree audit, which is weaker but not absent —
  `harness/tests/` fixtures pin the format the audit expects, so the break is loud.
- Nothing in `methodology/` or `spec/` changes. The async protocol is assembled entirely out of
  paths those documents already specify, which is why F-008 can remain deferred.
- The harness is not a fair test of `permissions.allow` (the worker bypasses it). F-006 must be
  settled by its own targeted probe, not by this run.
