"""Render tracker/board.md from workspace state.

Kept separate from the `board-gen` executable so that `validate-workspace` can render a board
in memory and compare it with the committed one. That comparison is the whole reason a
generated file is allowed to live in the repository at all: a board that disagrees with the
tracker is caught rather than believed.

Every byte of the output is a function of tracker state, except the single generated-at line,
which the staleness comparison ignores. Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workspace import BOARD_MARKER  # noqa: E402

__all__ = ["render", "board_path", "differs", "strip_generated_line"]

TITLE_PREFIX = "# Board — generated "


def board_path(workspace) -> str:
    return os.path.join(workspace.tracker, "board.md")


def _escape(text) -> str:
    """Pipe characters would break the table; nothing else needs escaping here."""
    return str(text if text is not None else "").replace("|", "\\|").strip()


def _blocked_by(workspace, item) -> str:
    reasons = []
    for question in item.blocking_questions():
        reasons.append(question.identifier)
    for dependency in item.fields.get("depends-on") or []:
        other = workspace.items.get(dependency)
        if other is None:
            reasons.append(f"{dependency} (missing)")
        elif other.status != "done":
            reasons.append(f"{dependency} ({other.status})")
    return ", ".join(reasons) if reasons else "—"


def _item_row(workspace, item) -> str:
    return (f"| {_escape(item.identifier)} | {_escape(item.fields.get('title'))} "
            f"| {_escape(item.type)} | {_escape(item.status)} "
            f"| {_escape(item.priority)} | {_blocked_by(workspace, item)} |")


def render(workspace, generated_at: str) -> str:
    lines = [BOARD_MARKER, f"{TITLE_PREFIX}{generated_at}", ""]

    epics = sorted(workspace.epics(), key=lambda item: item.identifier)
    grouped = set()
    for epic in epics:
        children = sorted(workspace.children_of(epic.identifier),
                          key=lambda item: item.identifier)
        grouped.update(child.identifier for child in children)
        lines.append(f"## {epic.identifier} — {_escape(epic.fields.get('title'))}  "
                     f"({_escape(epic.status)})")
        lines.append("")
        if not children:
            lines.append("_No items yet._")
            lines.append("")
            continue
        lines.append("| id | title | type | status | priority | blocked by |")
        lines.append("|----|-------|------|--------|----------|------------|")
        for child in children:
            lines.append(_item_row(workspace, child))
        lines.append("")

    orphans = sorted(
        (item for item in workspace.items.values()
         if item.type != "epic" and item.identifier not in grouped),
        key=lambda item: item.identifier)
    if orphans:
        lines.append("## Not under any epic")
        lines.append("")
        lines.append("| id | title | type | status | priority | blocked by |")
        lines.append("|----|-------|------|--------|----------|------------|")
        for item in orphans:
            lines.append(_item_row(workspace, item))
        lines.append("")

    lines.append("## Open questions")
    lines.append("")
    open_questions = []
    for item in workspace.sorted_items():
        for question in sorted(item.open_questions(), key=lambda q: q.identifier):
            open_questions.append((item, question))
    # Human-addressed first: when the loop stops, this is what a returning human reads.
    open_questions.sort(key=lambda pair: (
        0 if pair[1].fields.get("addressed-to") == "human" else 1,
        pair[0].identifier, pair[1].identifier))

    if not open_questions:
        lines.append("_None._")
        lines.append("")
    else:
        lines.append("| item | question | to | blocking | created |")
        lines.append("|------|----------|----|----------|---------|")
        for item, question in open_questions:
            heading = question.sections.get("## Question", {}).get("text", "").strip()
            summary = next((line.strip() for line in heading.split("\n") if line.strip()), "")
            lines.append(
                f"| {_escape(item.identifier)} | {_escape(question.identifier)} — "
                f"{_escape(summary)} | {_escape(question.fields.get('addressed-to'))} "
                f"| {'yes' if question.is_blocking else 'no'} "
                f"| {_escape(question.fields.get('created'))} |")
        lines.append("")

    lines.append("## Summary")
    lines.append("")
    counts = {}
    tracked = [item for item in workspace.items.values() if item.type != "epic"]
    for item in tracked:
        counts[item.status] = counts.get(item.status, 0) + 1
    breakdown = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))
    lines.append(f"- {len(tracked)} item(s)" + (f": {breakdown}" if breakdown else ""))
    lines.append(f"- {len(epics)} epic(s): "
                 + (", ".join(f"{epic.identifier} {epic.status}" for epic in epics) or "none"))
    human = sum(1 for _, question in open_questions
                if question.fields.get("addressed-to") == "human")
    lines.append(f"- {len(open_questions)} open question(s), {human} addressed to the human")
    blocked = [item.identifier for item in tracked if item.status == "blocked"]
    lines.append(f"- blocked: {', '.join(blocked) if blocked else 'none'}")
    return "\n".join(lines) + "\n"


def strip_generated_line(text: str) -> str:
    """Drop the one line that is a function of the clock rather than of tracker state."""
    return "\n".join(line for line in text.split("\n")
                     if not line.startswith(TITLE_PREFIX))


def differs(rendered: str, existing: str) -> bool:
    return strip_generated_line(rendered) != strip_generated_line(existing)
