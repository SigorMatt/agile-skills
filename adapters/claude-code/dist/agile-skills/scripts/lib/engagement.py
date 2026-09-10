"""Is an engagement over? One implementation, two consumers.

An **engagement** is one epic and every item whose `epic:` names it. It **ends** when no skill
can advance any item in it and none ever will without a person acting (`spec/ids-and-statuses.md`
§3.5). That condition is called **rest**, and it holds when all of:

  1. every child of the epic is at a terminal status — `done` or `blocked`;
  2. no open question in the engagement is anyone's to act on but the stakeholder's, and then
     only non-blockingly — every open question in it is a **standing ask** (ADR-0012 §1);
  3. no request in `tracker/requests/` is `open`.

Condition 2 read *no question anywhere is `open`* until ADR-0012, and it meant, in the world it
was written for, *nothing is outstanding*: every open human-addressed question stopped the loop,
so the two sentences picked out the same workspaces. They stopped doing so the moment
`spec/question.md` grew a question that must **not** stop the loop, and the old wording then made
every ending unreachable while an elicitation nobody answers stood open — E1 included (F-104).

An engagement that has ended is not yet **closed**: the retrospective is written after the
ending and before the engagement is archived (`meta/adr/ADR-0009-retrospective-reading.md` §2).
So `ended` means *the ending is recorded and the retro is still owed*, and `closed` means both
are done. The orchestrator dispatches `retro` on `ended` and reports `closed` — it does not
decide what "fully closed" means, for the same reason it does not decide what "over" means.

This module exists because rest has two consumers — the orchestrator, which dispatches
`review-close` on an epic at rest, and the termination gate, which dates the stakeholder's
acknowledgment against it. The orchestrator and the gate disagreeing about whether an engagement
is over is precisely how F-045 happened: the gate fired on `open -> done`, an epic with a blocked
child never got there, and the run ended with the stakeholder recording that nobody ever asked
them. Two readings of one rule is one reading too many.

**Silence, and the ending derived from it.** E4 has a second route — the stakeholder who never
answers at all — and it is counted rather than timed (`spec/ids-and-statuses.md` §3.5a,
`meta/adr/ADR-0011`). A **silent round** is one orchestrator halt on the human with no *inbound*
change since the previous halt, where inbound means the two channels that are the stakeholder's:
a reply written into a question's `## Answer`, and a file under `tracker/requests/`. The halts are
rows in `tracker/waiting/<EP-ID>.md` (`spec/workspace-layout.md` §1.4) and the count is the
trailing run of equal `inbound` digests — derived on every read, never stored.

Three consumers read the threshold and this module is the one implementation of all of it: the
orchestrator (through `scripts/record-halt`, which appends the row), `scripts/engagement-state`
(which reaches the `abandoned` verdict) and `scripts/check-epic-signoff` (which accepts an ending
because of it). Any two of them disagreeing about whether the threshold is met is F-045's
mechanism exactly, so `threshold_rounds()` reads `methodology/pipeline.yaml` and nothing here
carries a default of its own.

**The reader never writes.** `append_halt()` is called by `scripts/record-halt` and by nothing
else. `state()` computes the count and appends nothing — were it to record, `check-epic-signoff`
and `review-close` would each advance the clock by consulting it.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import datetime
import hashlib
import os

from record import table_rows

TERMINAL_CHILD_STATUSES = ("done", "blocked")
RETRO_ARTIFACT = "retro.md"
DELIVERED_OUTCOMES = ("delivered", "duplicate")

# The engagement's halt log (spec/workspace-layout.md §1.4). Deliberately outside
# tracker/items/: `next` writes no journal and no item artifact, and this is not the place to
# start.
WAITING_DIR = ("tracker", "waiting")
WAITING_COLUMNS = ("round", "observed", "inbound", "surfaced")
WAITING_PREAMBLE = ("# Waiting log \u2014 {epic}\n"
                    "\n"
                    "Append-only. One row per orchestrator halt on the human. Written by "
                    "`next`; never hand-edited.\n"
                    "\n"
                    "| round | observed | inbound | surfaced |\n"
                    "|-------|----------|---------|----------|\n")
DIGEST_CHARS = 8
ANSWER_SECTION = "## Answer"


class SilenceConfigError(Exception):
    """`pipeline.yaml` does not state the threshold, so no consumer may guess one."""


def find_pipeline(explicit=None):
    """Resolve `pipeline.yaml`. The adapter's installer places a copy beside the scripts."""
    if explicit:
        return explicit
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for candidate in (os.path.join(here, "pipeline.yaml"),
                      os.path.join(here, "..", "methodology", "pipeline.yaml")):
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)
    return None


def threshold_rounds(pipeline_path=None) -> int:
    """`termination.silence.threshold_rounds`, from pipeline.yaml. The single source.

    There is no fallback on purpose. A consumer that carried its own default would be a second
    opinion about when an engagement is abandoned, and two opinions is one too many (F-045).
    """
    path = find_pipeline(pipeline_path)
    if not path or not os.path.isfile(path):
        raise SilenceConfigError(
            "cannot find pipeline.yaml, so termination.silence.threshold_rounds is unreadable")
    import miniyaml
    pipeline = miniyaml.load_file(path) or {}
    silence = ((pipeline.get("termination") or {}).get("silence") or {})
    value = silence.get("threshold_rounds")
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise SilenceConfigError(
            f"{path}: termination.silence.threshold_rounds is {value!r}; it must be a positive "
            f"integer, and no program may supply one for it")
    return value


class Engagement:
    """The state of one epic and its children, and why."""

    __slots__ = ("epic", "children", "verdict", "reasons", "rest_since", "undelivered",
                 "silent_rounds", "threshold", "surfaced", "outstanding", "waiting_rows")

    def __init__(self, epic, children) -> None:
        self.epic = epic
        self.children = children
        self.verdict = "active"
        self.reasons = []
        self.rest_since = None
        self.undelivered = []
        self.silent_rounds = 0
        self.threshold = None
        self.surfaced = []
        self.outstanding = []
        self.waiting_rows = []

    @property
    def at_rest(self) -> bool:
        return self.verdict == "at-rest"

    @property
    def abandoned(self) -> bool:
        return self.verdict == "abandoned"

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


# ---- silence: the halt log, the inbound digest, and the count derived from them ----------
#
# spec/workspace-layout.md §1.4 is the format; spec/ids-and-statuses.md §3.5a is the rule. The
# functions below are the whole of it, so that the writer and the two readers cannot hold
# different ideas of what a round is.


class WaitingRow:
    """One recorded halt. `round` is written for a human reader and no program reads it."""

    __slots__ = ("round", "observed", "inbound", "surfaced", "line")

    def __init__(self, round_number, observed, inbound, surfaced, line) -> None:
        self.round = round_number
        self.observed = observed
        self.inbound = inbound
        self.surfaced = surfaced
        self.line = line

    def render(self) -> str:
        return (f"| {self.round} | {self.observed} | {self.inbound} | "
                f"{', '.join(self.surfaced)} |")

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<WaitingRow {self.round} {self.observed} {self.inbound}>"


def waiting_dir(root: str) -> str:
    return os.path.join(root, *WAITING_DIR)


def waiting_log_path(root: str, epic_id: str) -> str:
    return os.path.join(waiting_dir(root), f"{epic_id}.md")


def answer_body(question) -> str:
    """The `## Answer` section's text, as the digest hashes it.

    Trailing whitespace is stripped and nothing else is: an answer is the stakeholder's own
    words, and a digest that normalised them would be a digest over our idea of what they said.
    """
    section = (question.sections or {}).get(ANSWER_SECTION) or {}
    return (section.get("text") or "").rstrip()


def short_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:DIGEST_CHARS]


def human_questions(workspace, epic) -> list:
    """Every `addressed-to: human` question in the engagement, whatever its status.

    Returned as `(<ITEM>/<Q-ID>, question)` pairs, ascending — the order the digest renders in.
    """
    holders = [epic] + sorted(workspace.children_of(epic.identifier),
                              key=lambda item: item.identifier)
    found = []
    for holder in holders:
        for question in holder.questions:
            if question.fields.get("addressed-to") != "human":
                continue
            found.append((f"{holder.identifier}/{question.identifier}", question))
    return sorted(found, key=lambda pair: pair[0])


def surfaced_questions(workspace, epic) -> list:
    """The human-addressed questions that are `open` — what a halt puts in front of a person."""
    return [name for name, question in human_questions(workspace, epic) if question.is_open]


# ---- the four classes of open question, and who owns each (ADR-0012 §1) ------------------
#
# Every open question is exactly one of these, decided by three frontmatter fields and one
# section's emptiness so that the classification is a program's and not a reader's:
#
#   ours to answer     addressed-to: architect                   -> answer-questions
#   a reply to consume addressed-to: human, `## Answer` written  -> answer-questions
#   an outstanding ask addressed-to: human, blocking, no answer  -> THEIRS; the loop stops here
#   a standing ask     addressed-to: human, non-blocking, none   -> theirs, and nothing waits
#
# The loop stops on the human when, and only when, an outstanding ask exists. Rest is the
# complement: an open question holds rest unless it is a standing ask. Before ADR-0012 the halt
# fired on every open human-addressed question and rest was held by every open question at all,
# which made an elicitation — the one question `spec/question.md` §2 declares nobody is waiting
# on — halt the workspace for ever and put every ending out of reach (F-104), and left a reply
# the stakeholder had already written looking like a reason to stop and show it to them again
# (F-011's unfixed half, F-109).


def answer_text(question) -> str:
    """The reply as a reader sees it: the `## Answer` body without its filed-empty placeholder.

    A question is filed with `## Answer` present and empty but for an HTML comment, because the
    answerer needs somewhere to write (F-032). That comment is not a reply, and a predicate that
    counted it would call every freshly filed question answered.
    """
    return "\n".join(line for line in answer_body(question).split("\n")
                      if not line.strip().startswith("<!--")).strip()


def is_outstanding(question) -> bool:
    """The pipeline is waiting on a person, and cannot go on until they act."""
    return bool(question.is_open
                and question.fields.get("addressed-to") == "human"
                and question.fields.get("blocking") is True
                and not answer_text(question))


def is_standing(question) -> bool:
    """Asked, and nobody is waiting on it — `spec/question.md` §2's `blocking: false`."""
    return bool(question.is_open
                and question.fields.get("addressed-to") == "human"
                and question.fields.get("blocking") is not True
                and not answer_text(question))


def holds_rest(question) -> bool:
    """Does this question keep the engagement short of rest? Everything open but a standing ask."""
    return bool(question.is_open) and not is_standing(question)


def outstanding_asks(workspace, epic) -> list:
    """The asks this engagement is stopped on, by `<ITEM>/<Q-ID>`, ascending.

    One predicate, three consumers — `scripts/record-halt` (does this pass halt?), the rest
    condition below (is the engagement over?) and the abandonment trigger (is the count against
    anything?). Any two of them disagreeing about what the pipeline is waiting for is F-045's
    mechanism, which is why they read one function rather than three copies of a sentence.
    """
    return [name for name, question in human_questions(workspace, epic)
            if is_outstanding(question)]


def standing_asks(workspace, epic) -> list:
    """The asks that were put to a person and stop nothing, by `<ITEM>/<Q-ID>`, ascending."""
    return [name for name, question in human_questions(workspace, epic)
            if is_standing(question)]


def is_answerable(question) -> bool:
    """A question a skill can act on now — `answer-questions`' precondition 1, as a predicate.

    Addressed to the architect, or addressed to the human with a reply already written into
    `## Answer`. The second shape is the one `next` never learned: a reply the stakeholder has
    written is ours to propagate, not a reason to stop and show it to them again (F-011, F-109).
    """
    if not question.is_open:
        return False
    if question.fields.get("addressed-to") == "architect":
        return True
    return (question.fields.get("addressed-to") == "human" and bool(answer_text(question)))


def _status_owners(pipeline_path=None) -> dict:
    path = find_pipeline(pipeline_path)
    if not path or not os.path.isfile(path):
        return {}
    import miniyaml
    pipeline = miniyaml.load_file(path) or {}
    owners = {}
    for status in pipeline.get("statuses") or []:
        if isinstance(status, dict) and status.get("name"):
            owners[status["name"]] = status.get("owner")
    return owners


def dispatchable(workspace, pipeline_path=None):
    """Is there anything the pipeline could be doing instead of halting? The reason, or None.

    This is the **existence** question behind orchestrator steps 2, 3 and 4 — an open request,
    an answerable question, a runnable item — and never the selection question. Which item, in
    what order, stays the selection key's and the orchestrator's alone; nothing here ranks
    anything.

    It exists because ADR-0012 moved the halt below every dispatching step. While the halt was
    step 3, "an ask is open" and "this pass halted" were the same statement, so `record-halt`'s
    condition was sufficient by itself. After the reordering a pass may hold an outstanding ask
    **and** dispatch work, and a row written on that pass would be a silent round that never
    happened — the count an ending rests on, inflated by the pipeline's own busyness
    (ADR-0012 §2.1).
    """
    requests = _open_requests(workspace)
    if requests:
        return f"an open stakeholder request: {', '.join(sorted(requests))}"
    answerable = sorted(f"{item.identifier}/{question.identifier}"
                        for item in workspace.items.values()
                        for question in item.questions if is_answerable(question))
    if answerable:
        return f"an answerable question: {', '.join(answerable)}"
    owners = _status_owners(pipeline_path)
    runnable = []
    for item in sorted(workspace.items.values(), key=lambda i: i.identifier):
        if not owners.get(item.status):
            continue
        if item.blocking_questions():
            continue
        dependencies = item.fields.get("depends-on") or []
        if any((workspace.items.get(other) is None
                or workspace.items[other].status != "done") for other in dependencies):
            continue
        runnable.append(f"{item.identifier} ({item.status} -> {owners[item.status]})")
    if runnable:
        return f"a runnable item: {', '.join(runnable)}"
    return None


def request_lines(workspace) -> list:
    """The stakeholder's other channel, as digest lines. `.gitkeep` is not a request."""
    directory = os.path.join(workspace.root, "tracker", "requests")
    if not os.path.isdir(directory):
        return []
    import frontmatter
    lines = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md"):
            continue
        try:
            fields, _, _ = frontmatter.load_file(os.path.join(directory, name))
        except Exception:                       # noqa: BLE001 - an unreadable request is state
            fields = None
        lines.append(f"{name} {(fields or {}).get('status')}")
    return lines


def inbound_rendering(workspace, epic) -> str:
    """The canonical text the `inbound` digest is taken over.

    Everything in it is something the **stakeholder** could have changed, and nothing else is:
    a reply written into a `## Answer` (with its `status` and `answered-at`), and a file under
    `tracker/requests/`. A question *we* file changes no line here, which is why our own asking
    cannot reset the clock.
    """
    lines = []
    for name, question in human_questions(workspace, epic):
        answered_at = str(question.fields.get("answered-at") or "") or "-"
        lines.append(f"{name} {question.fields.get('status')} {answered_at} "
                     f"{short_digest(answer_body(question))}")
    lines.extend(request_lines(workspace))
    return "".join(line + "\n" for line in lines)


def inbound_digest(workspace, epic) -> str:
    return short_digest(inbound_rendering(workspace, epic))


def parse_waiting_log(text: str, first_line: int = 0) -> list:
    """The log's rows, in file order. Malformed rows are returned with what is there.

    A row is `| round | observed | inbound | surfaced |`. The header and its underline are
    skipped; `validate-workspace` is what judges the shape.
    """
    rows = []
    for cells, line in table_rows(text, first_line):
        if len(cells) < 4:
            rows.append(WaitingRow(cells[0] if cells else "", "", "", [], line))
            continue
        surfaced = [token.strip() for token in cells[3].split(",") if token.strip()]
        rows.append(WaitingRow(cells[0].strip(), cells[1].strip(), cells[2].strip(),
                               surfaced, line))
    return rows


def read_waiting_log(root: str, epic_id: str) -> list:
    path = waiting_log_path(root, epic_id)
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        return parse_waiting_log(handle.read())


def silent_rounds(rows: list) -> int:
    """The number of trailing rows sharing the last row's `inbound` digest.

    The count, entire. An absent log is zero. There is no stored counter: a counter is a second
    source of truth that drifts the first time a run is interrupted between the increment and
    the act, which is the argument ADR-0003 made against a counter file (§1.2).
    """
    if not rows:
        return 0
    last = rows[-1].inbound
    count = 0
    for row in reversed(rows):
        if row.inbound != last:
            break
        count += 1
    return count


def next_round_number(rows: list, digest: str) -> int:
    """What the human-facing `round` column says on the row about to be appended."""
    if rows and rows[-1].inbound == digest:
        return silent_rounds(rows) + 1
    return 1


def append_halt(root: str, epic_id: str, observed: str, digest: str, surfaced: list):
    """Append exactly one row, and nothing else. Called by `scripts/record-halt` alone.

    The file's preamble is written once, when the file is created; every later write appends a
    single table row. Nothing already in the file is read for the count except the digests, so a
    hand-edited `round` cannot make an abandonment happen sooner.
    """
    path = waiting_log_path(root, epic_id)
    rows = read_waiting_log(root, epic_id)
    row = WaitingRow(next_round_number(rows, digest), observed, digest, list(surfaced), 0)
    if not os.path.isfile(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(WAITING_PREAMBLE.format(epic=epic_id))
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(row.render() + "\n")
    return row


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def state(workspace, epic, pipeline_path=None) -> Engagement:
    """`active` | `at-rest` | `abandoned` | `suspended` | `ended` | `closed`, and why.

    **This function appends nothing.** It reads the waiting log `scripts/record-halt` wrote and
    derives the count; a reader that recorded would advance the clock every time the gate or
    `review-close` consulted it (§1.2).
    """
    children = sorted(workspace.children_of(epic.identifier), key=lambda i: i.identifier)
    engagement = Engagement(epic, children)
    engagement.undelivered = undelivered_children(children)
    engagement.rest_since = rest_boundary(children)
    engagement.waiting_rows = read_waiting_log(workspace.root, epic.identifier)
    engagement.silent_rounds = silent_rounds(engagement.waiting_rows)
    engagement.surfaced = surfaced_questions(workspace, epic)
    engagement.outstanding = outstanding_asks(workspace, epic)
    try:
        engagement.threshold = threshold_rounds(pipeline_path)
    except SilenceConfigError as exc:
        engagement.threshold = None
        engagement.reasons.append(f"the silence threshold is unreadable: {exc}")
    # The threshold is measured against an **outstanding** ask, never against any open
    # human-addressed question. A standing ask produces no halt, so it accrues no rounds, so a
    # count standing beside one is a count of halts on something else; declaring an abandonment
    # over the one question nobody is waiting on would be F-104's defect wearing the ending's
    # clothes (ADR-0011 §4 as narrowed by ADR-0012 §3).
    reached = bool(engagement.threshold is not None and engagement.outstanding
                   and engagement.silent_rounds >= engagement.threshold)
    # Every verdict carries the count while it is above zero, so the clock is visible before it
    # strikes rather than only afterwards (ADR-0011 §5).
    if engagement.silent_rounds and not reached:
        engagement.reasons.append(
            f"{engagement.silent_rounds} silent round(s) recorded against a threshold of "
            f"{engagement.threshold}")

    if epic.status in ("done", "blocked"):
        if epic.has_artifact(RETRO_ARTIFACT):
            engagement.verdict = "closed"
            engagement.reasons.append(
                f"the epic is {epic.status!r} and artifacts/{RETRO_ARTIFACT} exists; the "
                f"engagement is fully closed")
        else:
            engagement.verdict = "ended"
            engagement.reasons.append(
                f"the epic is {epic.status!r}; the engagement has ended and the retrospective "
                f"has not been written")
        return engagement
    # E4 by silence, and it is checked before every verdict that describes a live engagement.
    # The epic may be at `open` (the silence began before rest) or at `awaiting-answer` (it began
    # after the sign-off was filed), and neither of those is what is true of it: what is true is
    # that the pipeline came to a person `threshold_rounds` times and got nothing back
    # (spec/ids-and-statuses.md §3.5a).
    if reached:
        engagement.verdict = "abandoned"
        engagement.reasons.append(
            f"{engagement.silent_rounds} silent round(s) against a threshold of "
            f"{engagement.threshold}: the last {engagement.silent_rounds} halts on the human "
            f"share one inbound digest ({engagement.waiting_rows[-1].inbound}), so nothing the "
            f"stakeholder could have changed has changed")
        engagement.reasons.append(
            "still open and unanswered: " + ", ".join(engagement.outstanding))
        standing = standing_asks(workspace, epic)
        if standing:
            engagement.reasons.append(
                "also asked, and stopping nothing: " + ", ".join(standing))
        engagement.reasons.append(
            "the ending is E4 by silence and it is not recorded; review-close declares it")
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
    open_questions, standing = [], []
    for item in [epic] + children:
        for question in item.questions:
            if holds_rest(question):
                open_questions.append(f"{item.identifier}/{question.identifier}")
            elif question.is_open:
                standing.append(f"{item.identifier}/{question.identifier}")
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
        "every child has stopped, nothing open is ours to act on, no request is open")
    if standing:
        engagement.reasons.append(
            "open and stopping nothing — a standing ask is nobody's to compel, and the ending "
            "closes it as 'abandoned' if no reply ever comes (ADR-0012 §4.1): "
            + ", ".join(sorted(standing)))
    if engagement.undelivered:
        engagement.reasons.append("not delivered: " + ", ".join(engagement.undelivered))
    return engagement
