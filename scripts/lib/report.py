"""Findings collection and stable output for every validator in this repo.

One format for every script, because these run as gates: an agent reading the output must be
able to tell *which file, which line, which rule* without prose parsing, and a human must be
able to grep it. Findings are sorted before printing so two runs over the same tree produce
byte-identical output — the property that lets `scripts/check` diff a render against its
committed copy.

    path/to/file.md:12: ERROR [item.status.unknown] status "reviewing" is not a known status
    validate-workspace: 1 error, 0 warnings
"""

from __future__ import annotations

import os
import sys

__all__ = ["Finding", "Report"]

ERROR = "ERROR"
WARNING = "WARNING"


class Finding:
    __slots__ = ("path", "line", "level", "code", "message", "hint")

    def __init__(self, path: str, line: int, level: str, code: str, message: str,
                 hint: str = "") -> None:
        self.path = path
        self.line = line
        self.level = level
        self.code = code
        self.message = message
        self.hint = hint

    @property
    def sort_key(self):
        return (self.path, self.line, self.code, self.message)

    def format(self, root: str = "") -> str:
        shown = self.path
        if root and shown.startswith(root):
            shown = os.path.relpath(shown, root)
        location = f"{shown}:{self.line}" if self.line else shown
        text = f"{location}: {self.level} [{self.code}] {self.message}"
        if self.hint:
            text += f"\n    hint: {self.hint}"
        return text


class Report:
    """Collects findings for one validator run.

    ``root`` is stripped from printed paths so output does not depend on where the repo
    lives — otherwise the golden-output comparisons in `scripts/check` would be machine
    specific.
    """

    def __init__(self, name: str, root: str = "") -> None:
        self.name = name
        self.root = os.path.abspath(root) if root else ""
        self.findings: list = []
        self.notes: list = []

    # ---- recording ----------------------------------------------------------------

    def error(self, path, line, code: str, message: str, hint: str = "") -> None:
        self.findings.append(Finding(str(path), int(line or 0), ERROR, code, message, hint))

    def warn(self, path, line, code: str, message: str, hint: str = "") -> None:
        self.findings.append(Finding(str(path), int(line or 0), WARNING, code, message, hint))

    def note(self, message: str) -> None:
        """A line of context printed above the findings. Never affects the exit code."""
        self.notes.append(message)

    # ---- results ------------------------------------------------------------------

    @property
    def errors(self) -> int:
        return sum(1 for f in self.findings if f.level == ERROR)

    @property
    def warnings(self) -> int:
        return sum(1 for f in self.findings if f.level == WARNING)

    def ok(self) -> bool:
        return self.errors == 0

    def emit(self, stream=None) -> int:
        """Print every finding and the summary. Returns the process exit code."""
        stream = stream or sys.stdout
        for note in self.notes:
            print(f"{self.name}: {note}", file=stream)
        for finding in sorted(self.findings, key=lambda f: f.sort_key):
            print(finding.format(self.root), file=stream)
        errors, warnings = self.errors, self.warnings
        summary = (f"{self.name}: {errors} error{'' if errors == 1 else 's'}, "
                   f"{warnings} warning{'' if warnings == 1 else 's'}")
        print(summary, file=stream)
        return 0 if errors == 0 else 1
