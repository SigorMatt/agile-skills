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
import os
import re
import shlex
import sys

HISTORY_RE = re.compile(r"(^|/)tracker/items/[^/]+/history\.md$")
BOARD_RE = re.compile(r"(^|/)tracker/board\.md$")

WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

# A shell command that rewrites one of these files in place is the same act by another route —
# but only if the file is the command's *target*. The first version of this guard searched the
# command string for a guarded path and for anything redirect-shaped, which denied
# `cat tracker/board.md > /tmp/x`, `grep -n WI-0003 tracker/items/*/history.md > out`, and a
# commit whose message merely names the board. F-018: a guard that fires on mentions teaches the
# agent to phrase around it, which is the exact opposite of what a guard is for. So: parse.
REDIRECT_TOKEN_RE = re.compile(r"^(?:\d*|&)>>?$")
ATTACHED_REDIRECT_RE = re.compile(r"^(?:\d*|&)>>?(?P<target>.+)$")

# argv[0] -> which of its arguments it writes to.
#   "all"   every non-flag argument
#   "last"  the final non-flag argument (cp/mv/install semantics)
#   "of"    the value of an `of=` assignment (dd)
WRITERS = {
    "tee": "all", "sed": "all", "perl": "all", "patch": "all", "rm": "all", "shred": "all",
    "truncate": "all", "unlink": "all", "ed": "all",
    "cp": "last", "mv": "last", "install": "last", "ln": "last",
    "dd": "of",
}
# `sed` and `perl` only write with an in-place flag; without it they are readers.
IN_PLACE_REQUIRED = {"sed": ("-i",), "perl": ("-i",)}

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


def write_targets(command: str):
    """Every path this shell command would write to, as best as it can be read.

    Deliberately incomplete and deliberately quiet about it: a construct this cannot parse is
    not a target, because the module's standing policy is that a guard which blocks on confusion
    becomes a guard the agent routes around. What it must get right is the common ways a file is
    actually written — redirection, `tee`, an in-place edit — and it must not mistake a path that
    is being *read* or *named* for one being written.
    """
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []

    targets = []
    segment = []
    for token in tokens + [";"]:
        if token in (";", "|", "||", "&&", "&", "\n"):
            targets.extend(segment_targets(segment))
            segment = []
            continue
        segment.append(token)
    return targets


def segment_targets(tokens: list):
    """Write targets of one simple command (no operators)."""
    found = []
    words = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if REDIRECT_TOKEN_RE.match(token):
            if index + 1 < len(tokens):
                found.append(tokens[index + 1])
            index += 2
            continue
        attached = ATTACHED_REDIRECT_RE.match(token)
        if attached and not token.startswith("<"):
            found.append(attached.group("target"))
            index += 1
            continue
        if token.startswith("<"):          # input redirection and heredocs write nothing —
            index += 2                     # skip the operator and its source
            continue
        words.append(token)
        index += 1

    while words and "=" in words[0] and not words[0].startswith("-") \
            and words[0].split("=")[0].isidentifier():
        words.pop(0)                        # leading VAR=value assignments
    if not words:
        return found
    program = os.path.basename(words[0])
    if program in ("sudo", "command", "env", "nice", "time", "xargs"):
        return found + segment_targets(words[1:])
    rule = WRITERS.get(program)
    if rule is None:
        return found
    flags = IN_PLACE_REQUIRED.get(program)
    if flags and not any(word.startswith(flag) for word in words[1:] for flag in flags):
        return found
    arguments = [word for word in words[1:] if not word.startswith("-")]
    if program in ("sed", "perl") and arguments:
        arguments = arguments[1:]           # the script itself is not a file
    if rule == "all":
        found.extend(arguments)
    elif rule == "last" and arguments:
        found.append(arguments[-1])
    elif rule == "of":
        found.extend(word.split("=", 1)[1] for word in words[1:] if word.startswith("of="))
    return found


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
        for target in write_targets(str(tool_input.get("command") or "")):
            normalised = target.replace("\\", "/").strip("\"'")
            if HISTORY_RE.search(normalised):
                deny(HISTORY_REASON)
            if BOARD_RE.search(normalised):
                deny(BOARD_REASON)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
