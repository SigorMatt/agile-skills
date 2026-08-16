#!/usr/bin/env python3
"""PreToolUse hook: refuse writes that would bypass a gate.

Two paths in a workspace are not the agent's to edit:

  tracker/items/<ID>/history.md   a status change must go through scripts/transition, which
                                  checks the transition against pipeline.yaml and runs the
                                  acting skill's hard gates first
  tracker/board.md                generated; hand-editing it makes the board disagree with the
                                  tracker while looking authoritative

Denying the write is what turns "the gates must pass first" from an instruction in a procedure
into something the runtime enforces. Without it, an agent under pressure can append a history
row directly and every downstream check will believe it.

Contract (confirmed against the runtime docs; see meta/adr/ADR-0001):
  * stdin is a JSON object with `tool_name` and `tool_input`
  * printing {"hookSpecificOutput": {"hookEventName": "PreToolUse",
             "permissionDecision": "deny", "permissionDecisionReason": "..."}} and exiting 0
    blocks the call
  * exiting 0 with no output allows it

Anything this hook cannot parse is **allowed**. A guard that blocks on confusion would make the
tool unusable the first time an input shape changes; a guard that allows on confusion degrades
to the documented convention, which is where we would have been anyway.
"""

from __future__ import annotations

import json
import re
import sys

HISTORY_RE = re.compile(r"(^|/)tracker/items/[^/]+/history\.md$")
BOARD_RE = re.compile(r"(^|/)tracker/board\.md$")

WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# A shell command that rewrites one of these files in place is the same act by another route.
REDIRECT_RE = re.compile(r">>?|\btee\b|\bsed\b\s+-i|\bpatch\b|\bdd\b")

HISTORY_REASON = (
    "Blocked: tracker/items/*/history.md is append-only and is written by "
    ".claude/agile-skills/scripts/transition, which checks the transition against pipeline.yaml "
    "and runs the acting skill's hard gates first. Run:\n"
    "  python3 .claude/agile-skills/scripts/transition <ITEM-ID> --to <status> "
    "--actor <skill> --reason \"...\"\n"
    "If a gate legitimately cannot pass, add --force; the override is then recorded in the "
    "history reason instead of being invisible."
)

BOARD_REASON = (
    "Blocked: tracker/board.md is generated. Run "
    "`python3 .claude/agile-skills/scripts/board-gen` instead. A hand-edited board disagrees "
    "with the tracker while looking authoritative, and validate-workspace will report it as "
    "board.stale."
)


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0

    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0

    if tool in WRITE_TOOLS:
        path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        normalised = path.replace("\\", "/")
        if HISTORY_RE.search(normalised):
            deny(HISTORY_REASON)
        if BOARD_RE.search(normalised):
            deny(BOARD_REASON)
        return 0

    if tool == "Bash":
        command = str(tool_input.get("command") or "")
        if not REDIRECT_RE.search(command):
            return 0
        # Only object when the command both mentions a protected file and looks like it writes.
        if re.search(r"tracker/items/[^\s]*history\.md", command):
            deny(HISTORY_REASON)
        if re.search(r"tracker/board\.md", command):
            deny(BOARD_REASON)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
