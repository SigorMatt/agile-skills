#!/usr/bin/env python3
"""Self-test for guard-workspace-writes.py. Run: python3 adapters/claude-code/hooks/test_guard.py

Every rule gets a call it MUST deny and a call it MUST allow. The allowed side is the point of
this file: F-018 is a guard that denied `cat tracker/board.md > /tmp/x` because the *sentence*
contained a guarded path, and an agent that learns the guard fires on mentions starts phrasing
around it — which costs the guard everything it was for. So the must-allow table is seeded with
the exact shapes the finding names.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "guard-workspace-writes.py")

HISTORY = "tracker/items/WI-0003/history.md"
BOARD = "tracker/board.md"

# (label, payload, expected) — expected is "deny" or "allow"
CASES = [
    # ---- the write tools: the target is a parameter, so this half was always right ----------
    ("Write to history", {"tool_name": "Write", "tool_input": {"file_path": HISTORY}}, "deny"),
    ("Edit the board", {"tool_name": "Edit", "tool_input": {"file_path": BOARD}}, "deny"),
    ("Write to an absolute history path",
     {"tool_name": "Write", "tool_input": {"file_path": f"/home/u/proj/{HISTORY}"}}, "deny"),
    ("Write to an item's journal",
     {"tool_name": "Write",
      "tool_input": {"file_path": "tracker/items/WI-0003/journal.md"}}, "allow"),
    ("Write to a file merely named like the board",
     {"tool_name": "Write", "tool_input": {"file_path": "docs/board.md"}}, "allow"),

    # ---- Bash: writes ----------------------------------------------------------------------
    ("append a row by redirection",
     {"tool_name": "Bash", "tool_input": {"command": f"echo '| ... |' >> {HISTORY}"}}, "deny"),
    ("truncate the board by redirection",
     {"tool_name": "Bash", "tool_input": {"command": f"echo x > {BOARD}"}}, "deny"),
    ("attached redirection",
     {"tool_name": "Bash", "tool_input": {"command": f"echo x >>{HISTORY}"}}, "deny"),
    ("heredoc into the board",
     {"tool_name": "Bash", "tool_input": {"command": f"cat > {BOARD} <<'EOF'\nrows\nEOF"}},
     "deny"),
    ("tee into history",
     {"tool_name": "Bash", "tool_input": {"command": f"printf 'row' | tee -a {HISTORY}"}},
     "deny"),
    ("sed in place",
     {"tool_name": "Bash", "tool_input": {"command": f"sed -i 's/draft/done/' {HISTORY}"}},
     "deny"),
    ("cp over the board",
     {"tool_name": "Bash", "tool_input": {"command": f"cp /tmp/fake.md {BOARD}"}}, "deny"),
    ("mv over history",
     {"tool_name": "Bash", "tool_input": {"command": f"mv /tmp/h.md {HISTORY}"}}, "deny"),
    ("rm the board",
     {"tool_name": "Bash", "tool_input": {"command": f"rm -f {BOARD}"}}, "deny"),
    ("dd onto history",
     {"tool_name": "Bash", "tool_input": {"command": f"dd if=/tmp/x of={HISTORY}"}}, "deny"),
    ("a write in the second half of a chain",
     {"tool_name": "Bash",
      "tool_input": {"command": f"git status && echo row >> {HISTORY}"}}, "deny"),
    ("a write under sudo",
     {"tool_name": "Bash", "tool_input": {"command": f"sudo tee {BOARD} < /tmp/x"}}, "deny"),

    # ---- Bash: F-018's own examples, every one of which must be allowed --------------------
    ("read the board into a temp file",
     {"tool_name": "Bash", "tool_input": {"command": f"cat {BOARD} > /tmp/x"}}, "allow"),
    ("grep the histories into a report",
     {"tool_name": "Bash",
      "tool_input": {"command": f"grep -n WI-0003 tracker/items/*/history.md > /tmp/out"}},
     "allow"),
    ("name the board in a commit message",
     {"tool_name": "Bash",
      "tool_input": {"command": "git commit -m 'tracker: regenerate tracker/board.md "
                                "(refs WI-0003)'"}}, "allow"),
    ("print the board",
     {"tool_name": "Bash", "tool_input": {"command": f"cat {BOARD}"}}, "allow"),
    ("read history with sed, no -i",
     {"tool_name": "Bash", "tool_input": {"command": f"sed -n '1,5p' {HISTORY}"}}, "allow"),
    ("regenerate the board through the tool",
     {"tool_name": "Bash",
      "tool_input": {"command": f"python3 .claude/agile-skills/scripts/board-gen . && "
                                f"cat {BOARD}"}}, "allow"),
    ("read the board as input",
     {"tool_name": "Bash", "tool_input": {"command": f"wc -l < {BOARD}"}}, "allow"),
    ("diff two histories",
     {"tool_name": "Bash",
      "tool_input": {"command": f"diff {HISTORY} /tmp/old.md > /tmp/d"}}, "allow"),
    ("copy history somewhere else for inspection",
     {"tool_name": "Bash", "tool_input": {"command": f"cp {HISTORY} /tmp/inspect.md"}}, "allow"),
    ("the transition tool itself",
     {"tool_name": "Bash",
      "tool_input": {"command": "python3 .claude/agile-skills/scripts/transition WI-0003 "
                                "--to verifying --actor implement --reason 'gates green'"}},
     "allow"),

    # ---- degrade to allow on anything unreadable, as the module documents -------------------
    ("an unbalanced quote is not parseable",
     {"tool_name": "Bash", "tool_input": {"command": f"echo 'unterminated >> {HISTORY}"}},
     "allow"),
    ("a tool with no file_path",
     {"tool_name": "Write", "tool_input": {}}, "allow"),
    ("a tool this hook does not guard",
     {"tool_name": "Read", "tool_input": {"file_path": HISTORY}}, "allow"),
]


def decide(payload) -> str:
    result = subprocess.run([sys.executable, GUARD], input=json.dumps(payload),
                            capture_output=True, text=True)
    if result.returncode != 0:
        return f"exit {result.returncode}"
    output = result.stdout.strip()
    if not output:
        return "allow"
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        return f"unparseable output {output!r}"
    return parsed.get("hookSpecificOutput", {}).get("permissionDecision", "?")


def main() -> int:
    if not os.path.isfile(GUARD):
        print(f"test_guard: {GUARD} does not exist")
        return 1
    failures = []
    for label, payload, expected in CASES:
        actual = decide(payload)
        if actual != expected:
            failures.append(f"{label}: expected {expected}, got {actual}")
    print(f"guard self-test: {len(CASES) - len(failures)} passed, {len(failures)} failed")
    for failure in failures:
        print(f"  FAIL {failure}")

    # The guard must also be able to fail: if every case were "allow", a broken guard would pass.
    spec = importlib.util.spec_from_file_location("guard", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    denied = sum(1 for _, _, expected in CASES if expected == "deny")
    allowed = len(CASES) - denied
    print(f"  coverage: {denied} must-deny, {allowed} must-allow")
    if not denied or not allowed:
        print("  FAIL a table with only one kind of case proves nothing")
        return 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
