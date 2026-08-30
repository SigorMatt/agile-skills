"""Reading a workspace file that might not be text at all.

H-016: `validate-workspace` and `lint-claims` both walk every `*.md` file in the workspace and
decoded each one strictly, so a single file that is not valid UTF-8 crashed them with an uncaught
`UnicodeDecodeError` — a traceback where a finding belongs, and a gate that could not run rather
than one that failed. A real project hit it: the tool under test measured display width, so its
fixtures deliberately included bytes that are not UTF-8. The team renamed the file to dodge the
crash and recorded the defect, correctly, as one in the toolkit.

A gate that raises is worse than a gate that fails. So: decode with replacement, and tell the
caller it happened, so the fact reaches the record as a finding instead of as a stack trace.

Standard library only (ADR-0002).
"""

from __future__ import annotations

__all__ = ["read_text", "decodes_as_utf8"]

REPLACEMENT = "�"


def read_text(path: str):
    """Return (text, undecodable). `undecodable` is True when bytes had to be replaced."""
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        return raw.decode("utf-8"), False
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), True


def decodes_as_utf8(path: str) -> bool:
    try:
        with open(path, "rb") as handle:
            handle.read().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return True
