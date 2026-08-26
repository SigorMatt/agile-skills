"""Is an engagement over? One implementation, two consumers.

An **engagement** is one epic and every item whose `epic:` names it. It **ends** when no skill
can advance any item in it and none ever will without a person acting (`spec/ids-and-statuses.md`
§3.5). That condition is called **rest**, and it holds when all of:

  1. every child of the epic is at a terminal status — `done` or `blocked`;
  2. no question anywhere in the engagement — on the epic or on a child — is `open`;
  3. no request in `tracker/requests/` is `open`.

This module exists because rest has two consumers — the orchestrator, which dispatches
`review-close` on an epic at rest, and the termination gate, which dates the stakeholder's
acknowledgment against it. The orchestrator and the gate disagreeing about whether an engagement
is over is precisely how F-045 happened: the gate fired on `open -> done`, an epic with a blocked
child never got there, and the run ended with the stakeholder recording that nobody ever asked
them. Two readings of one rule is one reading too many.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import os

TERMINAL_CHILD_STATUSES = ("done", "blocked")
DELIVERED_OUTCOMES = ("delivered", "duplicate")


class Engagement:
    """The state of one epic and its children, and why."""

    __slots__ = ("epic", "children", "verdict", "reasons", "rest_since", "undelivered")

    def __init__(self, epic, children) -> None:
        self.epic = epic
        self.children = children
        self.verdict = "active"
        self.reasons = []
        self.rest_since = None
        self.undelivered = []

    @property
    def at_rest(self) -> bool:
        return self.verdict == "at-rest"

    def describe(self) -> str:
        lines = [f"engagement-state: {self.epic.identifier} {self.verdict}"]
        for reason in self.reasons:
            lines.append(f"  - {reason}")
        if self.rest_since:
            lines.append(f"  rest reached at {self.rest_since}")
        return "\n".join(lines)


def _open_requests(workspace) -> list:
    directory = os.path.join(workspace.root, "tracker", "requests")
    if not os.path.isdir(directory):
        return []
    import frontmatter
    found = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md"):
            continue
        fields, _, _ = frontmatter.load_file(os.path.join(directory, name))
        if (fields or {}).get("status") == "open":
            found.append(name[:-3])
    return found


def rest_boundary(children) -> str:
    """When the engagement last stopped moving.

    The maximum over the children's last history rows and their questions' reply times. The
    epic's own history and questions are deliberately excluded: the acknowledgment itself is a
    question on the epic, answered after rest, and including it would push the boundary past the
    very question it is used to date.
    """
    latest = ""
    for child in children:
        if child.history:
            latest = max(latest, child.history[-1].when or "")
        for question in child.questions:
            latest = max(latest, str(question.fields.get("answered-at") or ""))
    return latest or None


def undelivered_children(children) -> list:
    """Every child that did not deliver, by ID. What a termination statement must name."""
    return sorted(
        child.identifier for child in children
        if not (child.status == "done"
                and child.fields.get("outcome") in DELIVERED_OUTCOMES)
    )


def state(workspace, epic) -> Engagement:
    """`active` | `at-rest` | `suspended` | `ended`, with the reasons that decided it."""
    children = sorted(workspace.children_of(epic.identifier), key=lambda i: i.identifier)
    engagement = Engagement(epic, children)
    engagement.undelivered = undelivered_children(children)
    engagement.rest_since = rest_boundary(children)

    if epic.status in ("done", "blocked"):
        engagement.verdict = "ended"
        engagement.reasons.append(f"the epic is {epic.status!r}; the engagement has ended")
        return engagement
    if epic.status == "awaiting-answer":
        engagement.verdict = "suspended"
        engagement.reasons.append("the epic is awaiting an answer; nothing to dispatch")
        return engagement
    if not children:
        engagement.reasons.append("the epic has no child items yet; the engagement has not "
                                  "started")
        return engagement

    blockers = []
    active = [child.identifier for child in children
              if child.status not in TERMINAL_CHILD_STATUSES]
    if active:
        blockers.append("still in flight: " + ", ".join(active))
    open_questions = []
    for item in [epic] + children:
        for question in item.questions:
            if question.is_open:
                open_questions.append(f"{item.identifier}/{question.identifier}")
    if open_questions:
        blockers.append("open questions: " + ", ".join(sorted(open_questions)))
    requests = _open_requests(workspace)
    if requests:
        blockers.append("open requests: " + ", ".join(requests))

    if blockers:
        engagement.reasons.extend(blockers)
        return engagement

    engagement.verdict = "at-rest"
    engagement.reasons.append(
        "every child has stopped, no question is open, no request is open")
    if engagement.undelivered:
        engagement.reasons.append("not delivered: " + ", ".join(engagement.undelivered))
    return engagement
