# Adapter — Claude Code

Renders `methodology/` into installable skills for Claude Code, and wires the quality gates to
the strongest enforcement this runtime offers.

Read [`../README.md`](../README.md) first: it defines the contract this adapter implements. This
file records how *this* runtime satisfies it, and — just as importantly — where it does not.

---

## 1. Format facts, and when they were confirmed

Everything this renderer assumes about SKILL.md, hooks and permissions was verified against the
official documentation on **2026-08-16**, and the URLs and findings are recorded in
[`../../meta/adr/ADR-0001-claude-code-skill-format.md`](../../meta/adr/ADR-0001-claude-code-skill-format.md).
That ADR also lists what could **not** be confirmed, so the design does not quietly depend on a
guess.

The short version:

| Fact | Value |
|------|-------|
| Skill file | `<name>/SKILL.md`, frontmatter + markdown body |
| Project-level discovery path | `.claude/skills/<name>/SKILL.md` |
| Command name comes from | the **directory** name (not the frontmatter `name`) at this level |
| Description budget | `description` + `when_to_use` truncated at 1,536 characters in the listing |
| Body guidance | keep `SKILL.md` under 500 lines; put reference material in bundled files |
| Portable frontmatter fields | `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` |
| Blocking hook | `PreToolUse`, via exit code 2 **or** `permissionDecision: "deny"` with exit 0 |
| Non-blocking | `PostToolUse` cannot block — no gate is designed around it |

Formats change. If this table is stale, re-verify before trusting the renderer, and update the
ADR with the new date.

---

## 2. Usage

```bash
# from this repository
python3 adapters/claude-code/render.py                 # regenerate dist/
python3 adapters/claude-code/render.py --check         # fail if dist/ is not what methodology renders to

python3 adapters/claude-code/install.py /path/to/project            # install (idempotent)
python3 adapters/claude-code/install.py /path/to/project --dry-run  # say what would change
python3 adapters/claude-code/install.py /path/to/project --uninstall
```

### What install places

```
<project>/
├── .claude/skills/<skill>/SKILL.md            one per skill, invocable as /<skill>
├── .claude/skills/<skill>/references/contract.md
├── .claude/agile-skills/
│   ├── VERSION                                methodology + per-skill versions
│   ├── pipeline.yaml                          the status graph
│   ├── skills/<skill>/skill.yaml              machine-readable contracts, read by run-gate
│   ├── spec/                                  the schemas, as reference material
│   ├── scripts/                               the executable gates and workspace tooling
│   └── hooks/guard-workspace-writes.py        the PreToolUse guard
└── .claude/settings.json                      two PreToolUse entries, merged into whatever was there
```

It touches nothing else. `--uninstall` removes exactly those paths and its own hook entries, and
deliberately leaves `tracker/` and `docs/` alone — the workspace is the project's record, not
the tooling's.

### Note on skill name collisions

Project-level skills lose a name collision to a same-named **personal** skill in
`~/.claude/skills/`. That is the safe direction (your own override wins) but it is worth knowing:
if `/verify` behaves unexpectedly, check whether you have a personal skill of that name.

---

## 3. Capability mapping (C1–C5)

| # | Capability | How this runtime provides it | Gaps |
|---|-----------|------------------------------|------|
| **C1** | Skill discovery and triggering | Skills in `.claude/skills/` are invocable as `/<skill>` and can be loaded by relevance from `description`. The renderer folds `when_to_use` into `description`, situations first. | Descriptions are shortened when many skills are installed. The renderer fails the build if a description would exceed the 1,536-character cap, but cannot prevent the listing budget from trimming it in a project with very many skills. `CONSUMER-PROMPT.md` therefore names `/next` explicitly rather than relying on relevance alone. |
| **C2** | Asking the human | The built-in `AskUserQuestion` tool. `intake`, `refine`, `plan` and `answer-questions` may use it. | **Enforced, not merely stated:** every skill whose contract says `human_interaction` is `none` or `via-questions` is rendered with `disallowed-tools: AskUserQuestion`, which removes the tool while that skill is active. Fallback when the tool is unavailable (for example in `dontAsk` mode, which denies it): print the batched questions and stop. Never proceed on an invented answer. |
| **C3** | Gate execution | `run-gate` resolves placeholders and runs each gate's real command; `transition` refuses a status change whose actor has a failing hard gate; a `PreToolUse` hook denies the writes that would bypass `transition`. | See the enforcement table below — not every gate is hard-enforced, and the ones that are not are named. |
| **C4** | Install and uninstall | `install.py`, idempotent, merging into `settings.json` rather than overwriting it. | Refuses to touch a `settings.json` it cannot parse, rather than rewriting it. |
| **C5** | Isolated execution | Subagents can run a skill in a fresh context. | Not wired automatically. The acceptance run drives skills through context-free subagents; a consumer may do the same for `verify`, and `USAGE.md` says how. |

---

## 4. Gate enforcement — what is actually blocked

This is the honest table the adapter contract requires. **Hard** means something refuses;
**convention** means the procedure says so and nothing stops an agent that ignores it.

### Enforcement mechanisms in play

1. **`transition` refuses.** A status change runs the actor skill's command-backed hard gates
   first and exits non-zero without writing anything if one fails. This is where most hard
   enforcement lives.

   It refuses only the skill's **completion** transition — the move to its own `next_status`
   (`spec/skill-contract.md` §1.3). On any other move the gates still run and are still
   reported, but they do not block. Otherwise `implement` could never reach `in-progress`
   (`tests-pass` cannot pass before any code exists) and no skill could file a question about
   the gate that was blocking it.
2. **The `PreToolUse` hook denies.** Direct writes to `tracker/items/*/history.md` and
   `tracker/board.md` are blocked, including shell redirects, so `transition` cannot be routed
   around. Without this, mechanism 1 would be advice.
3. **`disallowed-tools` removes a capability.** Skills that may not question a human cannot.
4. **Convention.** The procedure states it and the journal records it; nothing enforces it.

### Per gate

| Skill | Gate | Enforcement declared | Actually enforced by | Hard? |
|-------|------|---------------------|----------------------|-------|
| intake | `workspace-valid` | hard | command; no transition to gate it | convention |
| intake | `epic-has-success-measures` | hard | judgement | convention |
| intake | `items-are-separable`, `no-solution-in-the-problem` | advisory | judgement | convention |
| refine | `workspace-valid` | hard | `transition` (1) | **hard** |
| refine | `definition-of-ready`, `criteria-are-decidable`, `qa-recorded-verbatim` | hard | judgement | convention |
| plan | `workspace-valid` | hard | `transition` (1) | **hard** |
| plan | `every-criterion-is-addressed`, `project-commands-resolved`, `decisions-recorded` | hard | judgement | convention |
| plan | `plan-is-executable-without-you` | advisory | judgement | convention |
| implement | `tests-pass`, `lint-clean` | hard | `transition` (1) | **hard** |
| implement | `workspace-valid` | hard | `transition` (1) | **hard** |
| implement | `commits-reference-the-item` | hard | `transition` (1) | **hard** |
| implement | `every-criterion-has-a-test` | hard | judgement | convention |
| implement | `no-unplanned-scope` | advisory | judgement | convention |
| verify | `tests-pass`, `lint-clean`, `workspace-valid` | hard | `transition` (1) | **hard** |
| verify | `every-criterion-independently-checked`, `negative-cases-exercised` | hard | judgement | convention |
| verify | `tests-would-fail-without-the-change` | advisory | judgement | convention |
| review-close | `verification-postdates-the-code` | hard | `transition` (1), via `check-verify-freshness` | **hard** |
| review-close | `commits-reference-the-item`, `tests-pass-on-the-merge-result`, `workspace-valid` | hard | `transition` (1) | **hard** |
| review-close | `definition-of-done`, `record-is-reconstructible` | hard | judgement | convention |
| answer-questions | `workspace-valid` | hard | `transition` (1) | **hard** |
| answer-questions | `answer-is-propagated`, `answered-from-the-record`, `escalation-is-justified`, `item-resumed-correctly` | hard | judgement, except `item-resumed-correctly` which `transition` checks against the recorded `resume-to` | mixed |
| next | `workspace-valid`, `board-current` | hard | command, run by the skill | convention |
| next | `selection-is-deterministic` | hard | judgement | convention |

Two honest observations about this table:

- **Every gate that a machine can decide is hard-enforced.** The ones marked convention are the
  ones that require reading and judging — "did you actually check each acceptance criterion
  independently?" cannot be settled by an exit code, and pretending otherwise would be the exact
  dishonesty the adapter contract forbids.
- **`intake`'s and `next`'s gates are convention because neither owns a status transition.**
  `intake` creates items rather than moving them, and `next` moves nothing at all. Mechanism 1
  has no hook to hang on. `validate-workspace` still runs, and its failure is visible; nothing
  refuses on their behalf.

### Demonstrating the block

`meta/evidence/gate-failure-demo.md` records a run where a failing test kept an item at
`planned`, and a direct edit to `history.md` was denied by the hook. Reproduce it with
`meta/evidence/gate-failure-demo.sh`.

---

## 5. Permissions for long autonomous runs

The renderer deliberately does **not** emit `allowed-tools`. Pre-approving `Bash` for skills that
run arbitrary project commands is a broad grant, and it should be a decision the person running
the pipeline makes knowingly rather than one an installer makes for them. `USAGE.md` covers the
options; the short version is that `auto` mode suits long runs, and `dontAsk` must not be used
while `intake` or `refine` are expected to run, because it denies `AskUserQuestion`.

---

## 6. Conformance against `../README.md` §5

| Box | Status | Evidence |
|-----|--------|----------|
| A1 renderer reads only the allowed inputs | ✅ | `render.py` opens `methodology/` and `spec/` only |
| A2 no per-skill special cases | ✅ | behaviour varies by `human_interaction`, `dispatch`, `quality_gates` |
| A3 byte-deterministic | ✅ | `render.py --check` is a step in `scripts/check` |
| A4 all eight render and are invocable | ✅ | `dist/MANIFEST.md`; each installs as `/<skill>` |
| A5 `when_to_use` reaches the matcher | ✅ | folded into `description`; over-length fails the build |
| A6 non-`direct` skills cannot ask the human | ✅ | `disallowed-tools: AskUserQuestion`, per the manifest |
| A7 gates run with placeholders resolved; null ⇒ reported skip | ✅ | `run-gate`, outcome `SKIP` |
| A8 a hard gate demonstrably blocks a transition | ✅ | `meta/evidence/gate-failure-demo.md` |
| A9 idempotent install; uninstall removes exactly what it added | ✅ | verified, including merging into a pre-existing `settings.json` |
| A10 validator runs with no extra dependencies | ✅ | standard-library Python only (ADR-0002) |
| A11 README carries the enforcement table and C1–C5 | ✅ | §3 and §4 above |
| A12 no methodology change was needed to make the adapter work | ✅ | the two spec additions made during this build (`Verified-commit:`, the board's `created` column) are runtime-neutral and improve the methodology for every adapter |
