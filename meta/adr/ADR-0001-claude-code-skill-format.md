# ADR-0001 — Claude Code skill format, verified against official docs

- **Status:** accepted
- **Date:** 2026-08-16
- **Unit:** META-002
- **Context of the decision:** PROMPT.md rule 6 forbids relying on memory for runtime
  specifics. The `adapters/claude-code/` renderer (META-041/042) must target the format the
  docs describe *today*, and acceptance box B1 requires the source URLs to be recorded here.

## Sources fetched

All fetched 2026-08-16. Note the documentation host has moved: the URL given in PROMPT.md,
`https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md`, answers **301 Moved
Permanently** to `https://code.claude.com/docs/en/claude_code_docs_map.md`. All further URLs
below are on the new host.

| # | URL | Used for |
|---|-----|----------|
| S1 | `https://code.claude.com/docs/en/claude_code_docs_map.md` | page index |
| S2 | `https://code.claude.com/docs/en/skills.md` | SKILL.md frontmatter, discovery, invocation, bundled files |
| S3 | `https://code.claude.com/docs/en/hooks.md` | hook events, blocking contract, config shape |
| S4 | `https://code.claude.com/docs/en/permission-modes.md` | permission modes for long autonomous runs |

## What was confirmed

### 1. Skill file layout and discovery (S2)

A skill is a directory containing `SKILL.md`. Discovery locations and precedence:

| Level | Path | Scope |
|-------|------|-------|
| Enterprise | via managed settings | whole org |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | all the user's projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | that project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | where the plugin is enabled |

Precedence on a name clash: **enterprise > personal > project**; any of these overrides a
bundled skill of the same name (but not the bundled skill's aliases). Plugin skills are
namespaced `plugin-name:skill-name` and therefore cannot clash. `.claude/commands/<x>.md` has
merged into skills and creates the same `/x` command, with the skill winning a name clash.

**Decision for this project:** the installer targets **project level**
(`<target>/.claude/skills/<name>/`). Rationale: the methodology is per-project (it owns that
project's `tracker/` and `docs/`), the workspace is committed with the project, and project
level loses a name clash to a same-named personal skill — which is the *safe* direction (a
user's own override wins) and is documented in `USAGE.md` as a caveat.

### 2. Frontmatter (S2, "Frontmatter reference")

**All frontmatter fields are optional**; only `description` is *recommended*, because Claude
uses it to decide when to apply the skill. If `description` is omitted the first paragraph of
the body is used instead.

Fields relevant to this project, verbatim semantics:

- `name` — display name in skill listings; **defaults to the directory name**. For personal and
  project skills, `name` sets only the display label — **the invocation command comes from the
  directory name** (`.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging`). Only for
  *plugin* skills does `name` set the command's last segment.
- `description` — what the skill does and when to use it. The combined `description` +
  `when_to_use` text is **truncated at 1,536 characters** in the skill listing. Put the key use
  case first.
- `when_to_use` — extra trigger phrases / example requests; appended to `description` and
  counts toward the same 1,536-char cap.
- `argument-hint` — autocomplete hint, e.g. `[issue-number]`.
- `arguments` — named positional arguments for `$name` substitution in the body.
- `disable-model-invocation` — `true` prevents Claude from auto-loading the skill (manual
  `/name` only). Default `false`.
- `user-invocable` — `false` hides it from the `/` menu (Claude-only). Default `true`.
- `allowed-tools` — tools pre-approved for the turn that invokes the skill; grant clears on the
  user's next message. Space/comma-separated string or YAML list.
- `disallowed-tools` — tools removed from the pool while the skill is active. Explicitly
  suggested for "autonomous skills that should never call certain tools, such as
  `AskUserQuestion` for a background loop".
- `model`, `effort`, `context: fork`, `agent`, `background` — execution controls; `context: fork`
  runs the skill in a forked subagent.
- `hooks` — "Hooks that Claude Code registers when the skill is invoked and keeps running for
  the rest of the session", using the same configuration format as `settings.json` hooks, plus
  a `once` option.
- `paths`, `shell`, `metadata`, `license`, `compatibility` — not needed by this renderer,
  except `metadata` (free-form map, Claude Code does not act on it) which we use to carry the
  methodology skill version.

Booleans accept `yes/no/on/off/1/0` in any case as well as `true`/`false` (since v2.1.218).

**Portability caveat (S2, "Using skill frontmatter outside Claude Code"):** outside Claude Code
— claude.ai uploads, the Skills API, `package_skill.py` — only six fields are legal: `name`,
`description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Any other field is a
**hard error**, not an ignored key.

**Decision:** the renderer emits only `name`, `description`, `allowed-tools`, `metadata` by
default, so rendered skills are also valid Agent-Skills-spec packages. `when_to_use`,
`disable-model-invocation`, `disallowed-tools` and `hooks` are emitted **only** where a skill's
contract genuinely needs them, and the renderer records in the dist manifest which skills are
therefore Claude-Code-only. This is recorded separately as ADR-0004.

### 3. Body size and bundled resources (S2, "Add supporting files")

Docs tip: **keep `SKILL.md` under 500 lines**; move detailed reference material to separate
files in the skill directory. Supporting files are referenced from `SKILL.md` by relative
markdown link so Claude knows what each contains and when to load it:

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
```

Scripts under the skill directory are *executed, not loaded*. This is exactly the progressive
disclosure R5 demands: SKILL.md carries the procedure, `references/` carries the contract and
schemas, `scripts/` carries the gate commands.

### 4. Triggering (S2, "Troubleshooting → Skill not triggering / descriptions cut short")

Confirmed guidance: the description must "include keywords users would naturally say"; if it
triggers too often, make it more specific. Descriptions can be **truncated when many skills are
installed** — the listing budget defaults to 1% of the model's context window and Claude Code
drops descriptions of least-used skills first. Hence: front-load the trigger situations in the
first sentence of `description`, and never rely on text past ~1,536 characters.

### 5. Explicit invocation

`/skill-name` invokes a skill directly (directory name for project-level skills). This is the
mechanism `CONSUMER-PROMPT.md` uses to drive the loop (`/next`), rather than hoping for
model-invoked triggering.

### 6. Asking the human (S4)

The built-in **`AskUserQuestion`** tool is the runtime's structured
question-the-human mechanism; S4 names it explicitly when describing `dontAsk` mode, which
"denies the built-in `AskUserQuestion` tool ... because their approval card needs an answer this
mode never collects". It follows that:

- `intake`/`refine` (human_interaction: `direct`) may use it, but must **also** work when it is
  unavailable — the fallback is to print the batched questions as plain text and stop.
- `implement`/`verify` (human_interaction: `none`) set `disallowed-tools: AskUserQuestion` in
  their rendered frontmatter, which is the runtime-level enforcement of R2's "never ask the
  human directly" rule. This is a genuine hard enforcement, not a convention.

### 7. Gate enforcement (S3)

Hook events exist for `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `UserPromptSubmit`,
`SessionStart`, and many others. Blocking contract:

- **Exit code 2 blocks**, and blocks on its own — "JSON can't override it". The message shown
  comes from stderr.
- Equivalent structured form, with **exit code 0**:
  `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}`
  (`permissionDecision` ∈ `allow` | `deny` | `ask`).
- `PreToolUse` blocks the tool call. `PostToolUse` **cannot** block (the tool already ran) —
  exit 2 only shows stderr to Claude. `Stop`/`SubagentStop` can prevent stopping.
- Matchers filter on tool name: exact, `A|B`, comma lists, or regex. Handlers additionally
  accept an `if` permission-rule filter, e.g. `"Bash(git *)"`, `"Edit(*.ts)"`.
- Config lives in `.claude/settings.json` under `hooks.<Event>[].hooks[]`, with
  `{"type":"command","command":"...","timeout":N}`; `${CLAUDE_PROJECT_DIR}` expands to the
  project root.

**Decision for gate enforcement (detailed in ADR-0003):** a `PreToolUse` hook matching `Bash`
with `if: "Bash(git commit *)"` and a `PreToolUse` hook on the status-transition script are the
two hard chokepoints. A status transition that has not passed its gates is *denied at the tool
call*, not merely discouraged in prose.

### 8. Permission modes for long autonomous runs (S4)

Exact mode values: `default` (labelled **Manual** in the UI, alias `manual`), `acceptEdits`,
`plan`, `auto`, `dontAsk`, `bypassPermissions`. Set by `--permission-mode <mode>` at startup or
`permissions.defaultMode` in a settings file (with the caveat that an `"auto"` value in
`.claude/settings.json` / `settings.local.json` does **not** take effect). `auto` is documented
as "Best for: long tasks, reducing prompt fatigue"; `dontAsk` runs only pre-approved tools and
never waits for input — and, importantly, **denies `AskUserQuestion`**, so `USAGE.md` must warn
that `dontAsk` breaks `intake`/`refine`. Deny and explicit-ask permission rules still apply in
every mode, including `bypassPermissions`.

## What could NOT be confirmed

- **Whether a `PreToolUse` hook can see, and therefore gate on, the *arguments* of a skill
  invocation itself.** The docs describe matchers on tool names and an `if` filter using
  permission-rule syntax for tool events; nothing states that invoking `/skill-name` surfaces as
  a gateable tool call. The renderer therefore does **not** assume it: gates are attached to the
  observable side effects (`Bash` running the transition script, `git commit`) instead, which the
  docs do fully specify.
- **The exact JSON `tool_input` shape for every tool** beyond `Bash` (the doc's example). The
  gate hook is written defensively: it reads `tool_input.command` when present and allows
  anything it cannot parse, so an unexpected shape degrades to "no opinion" rather than to a
  false block.
- **Long-run session limits** (context/compaction behaviour under multi-hour autonomous loops)
  are out of the docs consulted; `USAGE.md` handles this by making the pipeline resumable from
  filesystem state, which is a design requirement anyway (VISION principle 3).

## Consequences

1. The renderer targets `<project>/.claude/skills/<name>/SKILL.md` with `references/` and
   `scripts/` subdirectories.
2. Descriptions are generated from the methodology contract with trigger situations first, and
   the renderer **fails the build** if `description` + `when_to_use` exceeds 1,536 characters.
3. `SKILL.md` bodies are kept under 500 lines by the renderer, which fails the build otherwise.
4. `AskUserQuestion` availability is a documented adapter capability
   (`adapters/README.md` capability **C2**), with a plain-text fallback so no methodology skill
   depends on a runtime-specific tool.
5. Gate hardness is documented per gate rather than claimed globally (R5).
