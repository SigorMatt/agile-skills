# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Current unit: META-002 — confirm Claude Code skill format against official docs

**Why:** PROMPT.md rule 6 forbids relying on memory for runtime specifics. The adapter
(META-041/042) must render against the *current* format.

**Steps**
1. Fetch `https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md`.
2. From it, fetch the pages covering: Agent Skills (SKILL.md frontmatter fields, discovery
   paths, progressive disclosure), hooks (event names + matcher/JSON contract), settings
   (`.claude/settings.json` permissions), and subagents if covered.
3. Write `meta/adr/ADR-0001-claude-code-skill-format.md` recording, with source URLs and the
   date fetched: exact frontmatter fields (required/optional), discovery directories and
   precedence, description-triggering guidance, bundled-resource conventions, hook events
   usable for gate enforcement, and the mechanism available for asking the human a question.
4. Commit `meta: record verified Claude Code skill format (refs META-002)`.

**Done criteria**
- ADR-0001 exists, every claim carries a URL, and it states explicitly what could NOT be
  confirmed (so the adapter does not silently guess).
- Working tree clean; plan.md META-002 ticked; journal entry appended.

**Next unit:** META-003 — ADR-0002 scripting/dependency policy + `scripts/lib/` skeleton.
