#!/usr/bin/env python3
"""Drive one hardening iteration: alternate a worker turn and a sim turn until a stop condition.

    harness/run_iteration.py --iteration iteration-1-expenses
    harness/run_iteration.py --iteration iteration-1-expenses --max-turns 6
    harness/run_iteration.py --iteration iteration-1-expenses --fresh

The two sessions never talk to each other. They do not need to: the pipeline communicates
exclusively through the filesystem, and this script exists to take turns for them
(`meta/harness/DESIGN.md` §2).

    sim(open) → worker → [status] → sim(answer) → worker → [status] → …

Rerunning the same command resumes: the run directory is derived from the iteration id, and
`state.json` in it says whose turn it is. A turn that was killed half-way is simply run again —
every pipeline skill is written to reconcile with what it finds on disk, which is the property
this harness is built on top of. `--fresh` archives the old run and starts over.

Everything a turn did is recorded under `harness/runs/<iteration>/`:

    state.json                     whose turn it is, and why the run stopped
    iteration-log.jsonl            one line per turn: command, duration, cost, observed status
    SIM-LOG.md                     the stakeholder's own log, written by the sim
    turns/<n>-<role>.stream.jsonl  the turn's full transcript, which the audit reads
    turns/<n>-worker.status.md     the worker's self-report, copied out of the project

Standard library only (ADR-0002).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RUNS = os.path.join(HERE, "runs")
SKILL_SOURCE = os.path.join(HERE, "skills", "simulated-human")
SKILL_TARGET = os.path.join(HERE, ".claude", "skills", "simulated-human")
DEFAULT_ROOT = os.path.expanduser(
    os.environ.get("HARNESS_THROWAWAY_ROOT", "~/agile-skills-throwaway"))

STATUS_FILE = "HARNESS-STATUS.md"
WORKER_STOP_REASONS = ("human-question-open", "nothing-runnable", "epic-done",
                       "validator-failed", "blocked", "turn-budget-exhausted", "error")

# H-002: a stop is either the run finishing or the run being interrupted, and the two need
# opposite recoveries. A killed turn, or a turn the API refused, says nothing about the work —
# the workspace is intact, the trail is intact, and rerunning the same command is exactly what
# should happen (harness/USAGE.md §9 has always promised this). Everything else is a verdict on
# the run, and rerunning it would paper over the verdict.
RESUMABLE_STOPS = {
    "turn-failed": "the turn was killed or errored; the workspace and the trail are intact",
    "turn-timeout": "the turn hit --turn-timeout and was killed",
    "api-rejected": "the model API refused the turn (limit, auth, or transport)",
}
# H-010: a budget bounds *work*, not the engagement. Five times in three iterations a run hit its
# turn budget, twice landing exactly between the termination gate filing the sign-off and the
# stakeholder answering it — and the driver called that a verdict, refused a rerun with a larger
# --max-turns, and offered only --fresh. The workaround worked and its cost reached the person:
# "I was asked to sign off twice for the same engagement, six hours apart." So `turn-budget` is
# resumable unless the engagement itself is at an ending, which is the one case where "this run
# is over" and "this engagement is over" are the same sentence.
CONDITIONAL_STOPS = {
    "turn-budget": "the budget bounds this run's work, not the engagement; rerun with a larger "
                   "--max-turns and it continues in place",
}
TERMINAL_STOPS = {
    "epic-done": "the run reached its end",
    "blocked-no-recourse": "the run reached an impasse with nothing left to ask",
    "turn-budget": "the configured turn budget is spent and the engagement is at an ending",
    "contamination": "a turn read or wrote outside the boundary; --reaudit is the recovery",
    # H-022: this stop is now reached only after the repair allowance in `decide` is spent —
    # a worker that was given N consecutive turns whose only job was making the workspace
    # validate, and did not. The defect defeated the thing best placed to fix it, which is a
    # finding about the toolkit rather than an interruption of the run.
    "validator-failed": "the workspace still did not validate after its repair turns were "
                        "spent; the record needs a person, and --fresh starts a new run "
                        "against the same workspace",
    "stalled": "three turns changed nothing",
    "abandoned": "the stakeholder went silent past the threshold and the engagement ended as E4",
}


def stop_is_resumable(reason, observed=None) -> bool:
    """Is this stop an interruption rather than a verdict?

    `observed` is a `scan_project` reading. Without one, only the unconditional stops are
    resumable — a caller that cannot see the workspace does not get the benefit of the doubt.
    """
    if reason in RESUMABLE_STOPS:
        return True
    if reason in CONDITIONAL_STOPS and observed is not None:
        return not engagement_terminal(observed)[0]
    return False


API_REJECTION_MARKERS = (
    "rate limit", "rate_limit", "usage limit", "overloaded", "quota",
    "authentication", "unauthorized", "invalid api key", "credit balance",
    "connection error", "network error", "503", "529",
)


def looks_api_rejected(text: str) -> bool:
    """Did the model API refuse this turn, rather than the turn going wrong?

    Deliberately a text match, and deliberately generous: the cost of a false positive is that a
    genuinely broken turn is offered a resume it will fail again immediately and visibly, while
    the cost of a false negative is the run being declared finished because a subscription limit
    was reached at minute forty.
    """
    lowered = (text or "").lower()
    return any(marker in lowered for marker in API_REJECTION_MARKERS)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read(path, default=""):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return default


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


# H-012: the driver's console narrative used to belong to whoever launched it, and three ways of
# owning it from outside failed in one iteration — `tee` dead at launch because the run directory
# did not exist yet (the driver created it later), a `capture-pane` rescue that is a rendered,
# hard-wrapped copy, and `pipe-pane`, which is clearable without trace. A run's own account of
# itself is not a wrapper's job.
_CONSOLE = None


def open_console_log(path):
    """Own the console from the first line. Returns the path, or "" if it could not be opened."""
    global _CONSOLE
    close_console_log()
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        _CONSOLE = open(path, "a", encoding="utf-8")
    except OSError as exc:
        print(f"[{now()}] could not open the console log at {path}: {exc}", flush=True)
        return ""
    return path


def close_console_log():
    global _CONSOLE
    if _CONSOLE is not None:
        try:
            _CONSOLE.close()
        finally:
            _CONSOLE = None


def say(message):
    line = f"[{now()}] {message}"
    print(line, flush=True)
    if _CONSOLE is not None:
        try:
            _CONSOLE.write(line + "\n")
            _CONSOLE.flush()
        except OSError:
            pass


# ---------------------------------------------------------------------------------------------
# configuration and the run directory


def load_iteration(iteration_id):
    path = os.path.join(HERE, "iterations", f"{iteration_id}.json")
    if not os.path.isfile(path):
        sys.stderr.write(f"run: no iteration config at {path}\n")
        raise SystemExit(2)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def render_sim_skill(config):
    """Make the sim skill discoverable, with this iteration's persona and probe beside it.

    DESIGN §3 describes three files — SKILL.md, persona.md, probe-script.md. The first is
    written once and versioned; the other two are this iteration's choice from `personas/` and
    `probes/`. Rendering rather than symlinking keeps the source of truth in one place and makes
    the copy disposable: `harness/.claude/` is git-ignored.
    """
    persona = os.path.join(SKILL_SOURCE, "personas", f"{config['persona']}.md")
    probe = os.path.join(SKILL_SOURCE, "probes", f"{config['probe']}.md")
    for path in (os.path.join(SKILL_SOURCE, "SKILL.md"), persona, probe):
        if not os.path.isfile(path):
            sys.stderr.write(f"run: missing sim skill file {path}\n")
            raise SystemExit(2)
    if os.path.isdir(SKILL_TARGET):
        shutil.rmtree(SKILL_TARGET)
    os.makedirs(SKILL_TARGET)
    shutil.copy(os.path.join(SKILL_SOURCE, "SKILL.md"),
                os.path.join(SKILL_TARGET, "SKILL.md"))
    shutil.copy(persona, os.path.join(SKILL_TARGET, "persona.md"))
    shutil.copy(probe, os.path.join(SKILL_TARGET, "probe-script.md"))
    return (os.path.join(SKILL_TARGET, "persona.md"),
            os.path.join(SKILL_TARGET, "probe-script.md"))


def prompt_text(name):
    """The turn prompt below its `---` divider, plus the version from its first line."""
    raw = read(os.path.join(HERE, "prompts", f"{name}.md"))
    version = "unknown"
    first = raw.split("\n", 1)[0]
    if "version" in first:
        version = first.rstrip(" -->").split("version", 1)[1].strip()
    body = raw.split("\n---\n", 1)[1] if "\n---\n" in raw else raw
    return body.strip(), version


def worker_prompt_name(job):
    """Which instructions a worker turn is given.

    A repair turn is not a worker turn with a note attached: its only job is making
    `validate-workspace` green, and it must not advance the work (H-022). Separate prompt files
    mean the per-turn `prompt-version` in the iteration log says *which* instructions ran, so a
    reader can tell a repair turn from an ordinary one without opening a transcript.
    """
    return "repair-turn" if job == "repair" else "worker-turn"


def fill(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


# ---------------------------------------------------------------------------------------------
# what the project actually says (never the worker's word for it)


# ADR-0011 §1.3: the silence threshold lives in `pipeline.yaml` and three programs read it,
# because any two of them disagreeing about whether a stakeholder is gone is F-045's mechanism
# exactly. The driver is a fourth reader and it does not re-derive anything: it runs the
# *project's own* `engagement-state` and reads the verdict off its output. Nothing here knows
# what the threshold is, how a silent round is counted, or where the waiting log lives.
ENGAGEMENT_VERDICT_RE = re.compile(r"^engagement-state:\s+(?P<epic>[A-Za-z]+-\d+)\s+"
                                   r"(?P<verdict>[a-z-]+)\s*$")
# Both of `engagement-state`'s silence sentences carry the same two numbers, and they are the
# numbers it derived rather than any the driver computed:
#   "3 silent round(s) recorded against a threshold of 3"     (the clock, still ticking)
#   "3 silent round(s) against a threshold of 3: the last 3 halts on the human share ..."
SILENT_ROUNDS_RE = re.compile(r"(?P<rounds>\d+) silent round\(s\).*?threshold of "
                              r"(?P<threshold>\d+)")


def parse_engagement_state(text):
    """{epic: {verdict, reasons, silent-rounds, threshold}} from `engagement-state --all`."""
    states = {}
    current = None
    for line in (text or "").split("\n"):
        match = ENGAGEMENT_VERDICT_RE.match(line)
        if match:
            current = {"verdict": match.group("verdict"), "reasons": [],
                       "silent-rounds": 0, "threshold": None}
            states[match.group("epic")] = current
            continue
        if current is None or not line.startswith("  "):
            continue
        reason = line.strip().lstrip("- ").strip()
        current["reasons"].append(reason)
        counted = SILENT_ROUNDS_RE.search(reason)
        if counted:
            current["silent-rounds"] = max(current["silent-rounds"],
                                           int(counted.group("rounds")))
            current["threshold"] = int(counted.group("threshold"))
    return states


def engagement_states(project_dir):
    """Ask the workspace what its engagements are. Never infer it here.

    Returns {} when the project has no toolkit installed or the script fails — a driver that
    cannot ask does not get to guess, and every consumer below treats an absent reading as "no
    epic is abandoned", which is the reading that changes nothing.
    """
    script = os.path.join(project_dir, ".claude", "agile-skills", "scripts", "engagement-state")
    if not os.path.isfile(script):
        return {}
    try:
        result = subprocess.run([sys.executable, script, "--all", "--root", project_dir],
                                cwd=project_dir, capture_output=True, text=True)
    except OSError:
        return {}
    if result.returncode != 0:
        return {}
    return parse_engagement_state(result.stdout)


# `scripts/lib/report.py` prints every finding as `path:line: LEVEL [code] message`, with any
# hint on an indented continuation line and the summary count last. A finding line is the only
# thing in that output that names a defect.
VALIDATOR_FINDING = re.compile(r"^\S.*: (ERROR|WARNING) \[[^\]]+\] ")
VALIDATOR_TAIL_ERRORS = 3


def validator_tail(output, limit=VALIDATOR_TAIL_ERRORS):
    """What the driver keeps of a `validate-workspace` run: enough to name the defect.

    The last line is always kept and always last, because it is the summary
    (`validate-workspace: 1 error, 0 warnings`) and a count is what a reader counts from. But a
    count names nothing — iteration 5 stopped `validator-failed` over one line,
    `tracker/items/WI-0002/history.md:14`, and its `state.json` records only "1 error". So the
    ERROR lines come with it, bounded at `limit` and followed by a truthful "and N more" when
    there are more; hint continuation lines are dropped, since the path, the line and the code
    are the identification. Output with no ERROR line in it — a green run, a crash, a usage
    error — keeps its last line and nothing else, which is all there is to say about it.
    """
    lines = [line for line in output.strip().split("\n") if line.strip()]
    if not lines:
        return []
    errors = []
    for line in lines:
        found = VALIDATOR_FINDING.match(line)
        if found and found.group(1) == "ERROR":
            errors.append(line)
    if not errors:
        return lines[-1:]
    kept = errors[:limit]
    dropped = len(errors) - len(kept)
    if dropped:
        kept.append(f"... and {dropped} more error{'' if dropped == 1 else 's'}")
    return kept + [lines[-1]]


def validator_detail(observed):
    """The one line, or the small block, that a stop detail and a log entry carry."""
    tail = observed["validator-tail"]
    head = f"validate-workspace exits {observed['validator-exit']}:"
    if len(tail) <= 1:
        return f"{head} {''.join(tail)}".strip()
    return head + "".join(f"\n    {line}" for line in tail)


def scan_project(project_dir):
    """The workspace as the driver reads it: items, questions, and the validator's verdict."""
    items = {}
    items_dir = os.path.join(project_dir, "tracker", "items")
    if os.path.isdir(items_dir):
        for name in sorted(os.listdir(items_dir)):
            item_md = os.path.join(items_dir, name, "item.md")
            if os.path.isfile(item_md):
                fields = audit.frontmatter(read(item_md))
                items[name] = {"type": fields.get("type", "?"),
                               "status": fields.get("status", "?"),
                               "outcome": fields.get("outcome")}
    questions = []
    for path in audit.question_files(project_dir):
        text = read(path)
        fields = audit.frontmatter(text)
        answer = audit.answer_body(text)
        questions.append({
            "id": f"{fields.get('item', '?')}/{fields.get('id', '?')}",
            "path": os.path.relpath(path, project_dir),
            "addressed-to": fields.get("addressed-to", "?"),
            "status": fields.get("status", "?"),
            "blocking": fields.get("blocking", "?"),
            "answered": bool(answer),
        })
    validator = subprocess.run(
        [sys.executable, os.path.join(project_dir, ".claude", "agile-skills", "scripts",
                                      "validate-workspace"), project_dir],
        cwd=project_dir, capture_output=True, text=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project_dir,
                          capture_output=True, text=True)
    engagements = engagement_states(project_dir)
    return {
        "items": items,
        "questions": questions,
        "engagements": engagements,
        "abandoned-epics": [epic for epic, state in sorted(engagements.items())
                            if state["verdict"] == "abandoned"],
        "validator-exit": validator.returncode,
        "validator-tail": validator_tail(validator.stdout + validator.stderr),
        "head": head.stdout.strip(),
        "open-human-questions": [q["id"] for q in questions
                                 if q["addressed-to"] == "human" and q["status"] == "open"],
        "unanswered-human-questions": [q["id"] for q in questions
                                       if q["addressed-to"] == "human"
                                       and q["status"] == "open" and not q["answered"]],
        "blocked-items": [name for name, item in items.items() if item["status"] == "blocked"],
        "open-requests": open_requests(project_dir),
    }


def open_requests(project_dir):
    """Stakeholder requests still waiting for a skill to respond (F-021)."""
    directory = os.path.join(project_dir, "tracker", "requests")
    if not os.path.isdir(directory):
        return []
    found = []
    for name in sorted(os.listdir(directory)):
        if not (name.startswith("R-") and name.endswith(".md")):
            continue
        fields = audit.frontmatter(read(os.path.join(directory, name)))
        if fields.get("status") == "open":
            found.append(name[:-3])
    return found


def fingerprint(observed):
    """Everything that counts as progress, so a stalled run can be recognised."""
    return json.dumps({
        "head": observed["head"],
        "items": {name: item["status"] for name, item in observed["items"].items()},
        "questions": [(q["id"], q["status"], q["answered"]) for q in observed["questions"]],
        "requests": observed.get("open-requests", []),
    }, sort_keys=True)


def epic_complete(observed):
    items = observed["items"]
    if not items:
        return False
    return all(item["status"] == "done" for item in items.values())


TERMINAL_CHILD_STATUSES = ("done", "blocked")


def engagement_at_rest(observed):
    """Is there nothing left for a worker turn to advance?

    The toolkit's own test, restated where the driver can compute it (`spec/ids-and-statuses.md`
    §3.5): every non-epic item at a terminal status, and no question open anywhere.

    H-008: this used to be `any item is blocked`. That coincided with the truth in iteration 1d,
    where the blocked item was the last one standing — and stopped coinciding the moment the
    deferral fix parked a blocked item at turn 4 with three items still to build. "An item is
    blocked" is a fact about one item; "the run reached an impasse" is a fact about the
    engagement, and they are not the same fact.
    """
    children = [item for item in observed["items"].values() if item["type"] != "epic"]
    if not children:
        return False
    if any(item["status"] not in TERMINAL_CHILD_STATUSES for item in children):
        return False
    return not [q for q in observed["questions"] if q["status"] == "open"]


def engagements_ended(observed):
    """Every epic has recorded its ending — `done` or `blocked`.

    An engagement at rest whose epic is still `open` is over and *unrecorded*: the worker's next
    turn is what asks the stakeholder and writes the ending down (F-045). Stopping there is
    stopping one turn before the thing the run exists to observe.
    """
    epics = [item for item in observed["items"].values() if item["type"] == "epic"]
    return bool(epics) and all(item["status"] in TERMINAL_CHILD_STATUSES for item in epics)


def engagements_abandoned(observed):
    """Epics `engagement-state` calls `abandoned`: E4 is due and it is not recorded.

    ADR-0011 §5: `abandoned` sits parallel to `at-rest` — both mean "review-close is owed on this
    epic". So this is not a stop. It is the F-045 branch in a second place: the run is one worker
    turn short of the thing it exists to observe, and that turn is the declaration.
    """
    return list(observed.get("abandoned-epics")
                or [epic for epic, state in sorted((observed.get("engagements") or {}).items())
                    if state.get("verdict") == "abandoned"])


# `spec/ids-and-statuses.md` §3.5 and ADR-0011 §3: an epic that closed `done` carrying this
# outcome ended at E4 and at no other ending — E1 records `delivered`, E2 `delivered-partial`,
# and E3 leaves the epic `blocked`. It is the ending the toolkit wrote down about itself, and it
# is *current state*, which is the property that matters here: a stakeholder who comes back
# reopens the epic (ADR-0011 §7) and whatever the engagement does next overwrites it.
E4_EPIC_OUTCOME = "dropped"
E4_EPIC_STATUS = "done"


def abandonment_declared(observed):
    """Epics whose *recorded* ending is E4 — the stop this driver was missing.

    Two readings, in their proper roles (H-020).

    The **test** is the ending the toolkit recorded: `engagement-state` says the engagement has
    ended (`ended`, or `closed` once the retro is written), and the epic it ended is `done` with
    `outcome: dropped`. The first half stays the toolkit's judgement — the driver does not decide
    when an engagement is over — and the second is the record stating which of the four endings
    happened, read off the same frontmatter every other branch here reads.

    The silent-round count is **corroboration**, and it moved out of the test on purpose. It is
    the trailing run of equal digests in an append-only log that nothing resets, so it outlives
    the engagement it describes: E4 is deliberately recoverable (ADR-0011 §7), and an engagement
    that went silent, was recovered through `tracker/requests/` and then *delivered* still
    reports "3 silent round(s) recorded against a threshold of 3" under a verdict of `ended`.
    The old reading — that verdict and that count, and nothing about the record — stamped such a
    run `abandoned`. The count says the clock struck, never which ending was written afterwards.
    Requiring it also missed the other route to E4 entirely: a withdrawal (§3.5) is an act the
    stakeholder performs, so it ends the engagement at E4 with no silent round behind it at all.

    The driver still holds no threshold of its own. Where a count is reported, both numbers come
    out of one sentence of `engagement-state`'s, and they are quoted in the detail line as the
    evidence they are.
    """
    found = []
    items = observed.get("items") or {}
    for epic, state in sorted((observed.get("engagements") or {}).items()):
        if state.get("verdict") not in ("ended", "closed"):
            continue
        record = items.get(epic) or {}
        if record.get("status") != E4_EPIC_STATUS:
            continue
        if record.get("outcome") != E4_EPIC_OUTCOME:
            continue
        threshold = state.get("threshold")
        found.append((epic, state.get("silent-rounds") or 0, threshold))
    return found


def abandonment_detail(declared):
    said = []
    for epic, rounds, threshold in declared:
        line = (f"{epic}: the ending recorded is E4 — the epic is {E4_EPIC_STATUS!r} with "
                f"outcome {E4_EPIC_OUTCOME!r}")
        if threshold and rounds >= threshold:
            line += (f", and the stakeholder was silent for {rounds} round(s) against a "
                     f"threshold of {threshold}")
        said.append(line)
    return "; ".join(said)


def engagement_terminal(observed):
    """Is the workspace itself at an ending? Returns (terminal, stop-reason, detail).

    H-014: iteration 4 reached its terminal state — sign-off accepted, the epic `done` and
    `delivered`, nothing open — spent the budget's last slot on the closing sim turn, and then
    stamped the finished run "turn-budget: not finished". The workspace was terminal and only the
    label was wrong. The counter is a bound on work; what happened to the engagement is read off
    the disk.
    """
    # First, because E4 is the most specific thing that can be true of a finished engagement and
    # every other branch here would describe it as something else. An epic ended by silence over
    # an answered board reads as `epic-done`; one ended by silence over orphaned children reads
    # as `blocked-no-recourse`, "an impasse with nothing left to ask" — and there was plenty left
    # to ask. Nobody answered.
    #
    # H-020: "most specific" is only safe while the reading is exact. This branch reads the
    # ending the epic records about itself, so an engagement that went silent and then recovered
    # and delivered falls through to `epic-done` below, where it belongs.
    declared = abandonment_declared(observed)
    if declared:
        return True, "abandoned", abandonment_detail(declared)
    if epic_complete(observed):
        return True, "epic-done", f"{len(observed['items'])} item(s), all done"
    if (engagement_at_rest(observed) and engagements_ended(observed)
            and not observed.get("open-human-questions")
            and not observed.get("open-requests")):
        blocked = observed.get("blocked-items") or []
        return True, "blocked-no-recourse", (
            f"the engagement recorded its ending"
            + (f"; blocked: {', '.join(blocked)}" if blocked else ""))
    return False, "", ""


def first_job(project_dir):
    """Whose turn opens a fresh run, read from the workspace rather than assumed.

    H-011: every fresh run led with `sim job=open` whatever the project held. In iteration 2's
    continuations that cost a near-no-op turn once, and once the open-job sim absorbed a pending
    sign-off answer by accident — the right outcome by the wrong route. H-004 fixed
    answers-first for resumes; a fresh start never read the disk at all. This is the same
    decision the mid-run scheduler makes, in the same order.
    """
    observed = scan_project(project_dir)
    if observed["unanswered-human-questions"]:
        return "sim", "answer", (
            f"{len(observed['unanswered-human-questions'])} human question(s) are open and "
            f"unanswered")
    if not os.path.isfile(os.path.join(project_dir, "IDEA.md")):
        return "sim", "open", "the project has no IDEA.md, so the engagement has not been opened"
    return "worker", None, "the workspace is already populated and nothing is waiting on the "\
                           "stakeholder"


STATUS_HEADING_RE = re.compile(r"^#\s*Harness status\s*[—-]\s*turn\s*(?P<turn>\d+)\s*$",
                               re.IGNORECASE | re.MULTILINE)


def mark_archived(run_dir, when=None):
    """Make an archived run directory terminal, so nothing can read it as one in flight.

    `--fresh` moved a run aside and left it exactly as it was — including a `state.json` saying
    `"status": "running"` and a `driver.pid` naming a process that has not existed for days. Two
    of the seven archives on this machine were in that state. Nothing acts on them today, which
    is why this is cheap now and would not be later: a sweep, a resume, or a person reading the
    directory has no way to tell an archive from a live run except by its name.

    So the archive says what it is, in the file a program reads and in a file a person reads,
    and the pid — which can only mislead once the process is gone — is removed.
    """
    state_path = os.path.join(run_dir, "state.json")
    stamp = when or now()
    previous = None
    try:
        with open(state_path, "r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, ValueError):
        state = None
    if isinstance(state, dict):
        previous = state.get("status")
        state["status"] = "archived"
        state["archived"] = stamp
        if previous is not None:
            state["archived-from-status"] = previous
        with open(state_path, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
    write(os.path.join(run_dir, "ARCHIVED.md"),
          f"# Archived run\n\nThis directory was moved aside by `--fresh` at {stamp}. It is a "
          f"record, not a run:\nnothing here is in flight, the driver process it names is gone, "
          f"and no tool resumes it.\nIts last live status was "
          f"`{previous if previous is not None else 'unknown'}`.\n")
    pid_path = os.path.join(run_dir, "driver.pid")
    if os.path.isfile(pid_path):
        os.remove(pid_path)
    return True


def worker_report(project_dir, not_before=None, turn=None):
    """The worker's self-report: the last fenced json block in HARNESS-STATUS.md.

    Two independent ways the file on disk can fail to be *this* turn's report, and both have
    happened:

    `not_before` is the turn's start time. A turn that was killed never writes the file, and the
    driver used to read whatever was there and log it as that turn's report — iteration 1's turn
    4 was killed after a full Opus-hour and is recorded carrying turn 2's status, two hours stale
    (H-005). A status file older than the turn is not this turn's status.

    `turn` is the turn just run, and it is checked against the file's own heading. 4c's turn 16
    exited cleanly having written nothing at all — no commit, no tracker change, no status — and
    the file still carried turn 15's heading when turn 17 began, so the mtime test could not see
    it and the driver consumed the previous turn's report as current (H-017). The prompt already
    makes the worker write `# Harness status — turn N`; the driver now reads that number rather
    than trusting the file's presence.
    """
    path = os.path.join(project_dir, STATUS_FILE)
    if not_before is not None and os.path.isfile(path):
        if os.path.getmtime(path) < not_before:
            return None, ""
    text = read(path)
    if not text:
        return None, ""
    if turn is not None:
        match = STATUS_HEADING_RE.search(text)
        if match is None or int(match.group("turn")) != int(turn):
            return None, ""
    blocks = []
    marker = "```json"
    index = text.find(marker)
    while index != -1:
        end = text.find("```", index + len(marker))
        if end == -1:
            break
        blocks.append(text[index + len(marker):end])
        index = text.find(marker, end)
    for block in reversed(blocks):
        try:
            return json.loads(block), text
        except ValueError:
            continue
    return None, text


# ---------------------------------------------------------------------------------------------
# running a turn


def reap_orphan(pid_path):
    """Kill a turn whose driver was killed out from under it.

    A `kill -9` on the driver does not reach the `claude` process it started — observed, not
    assumed (META-078). The orphan keeps writing to the transcript of a turn nobody is waiting
    for, and the resumed run would then have two sessions in the same project at once, which is
    the one thing a filesystem-state pipeline cannot survive. So every turn records its child's
    pid, and a resuming driver kills whatever it finds still breathing.
    """
    if not os.path.isfile(pid_path):
        return None
    try:
        pid = int(read(pid_path).strip())
    except ValueError:
        os.unlink(pid_path)
        return None
    alive = False
    try:
        os.kill(pid, 0)
        with open(f"/proc/{pid}/cmdline", "rb") as handle:
            alive = b"claude" in handle.read()
    except (OSError, ProcessLookupError, PermissionError):
        alive = False
    if alive:
        try:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                os.kill(pid, signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass
        time.sleep(1)
    try:
        os.unlink(pid_path)
    except OSError:
        pass
    return pid if alive else None


def another_driver(driver_pid_path):
    """The pid of a driver already running this iteration, or None.

    Two drivers in one project would interleave turns into the same workspace, which is the
    corruption the restart requirement exists to prevent.
    """
    if not os.path.isfile(driver_pid_path):
        return None
    try:
        pid = int(read(driver_pid_path).strip())
    except ValueError:
        return None
    if pid == os.getpid():
        return None
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as handle:
            if b"run_iteration" in handle.read():
                return pid
    except OSError:
        return None
    return None


def stream_turn(argv, cwd, transcript_path, timeout, pid_path=None):
    """Run a headless turn, tee its transcript to disk, and report what came back.

    stderr goes straight to a file rather than a pipe: the transcript is read line by line while
    the turn runs, and a second pipe nobody drains is how a long turn deadlocks at the worst
    possible moment.
    """
    started = time.time()
    tool_calls = 0
    stderr_path = transcript_path.replace(".stream.jsonl", ".stderr.txt")
    with open(transcript_path, "w", encoding="utf-8") as sink, \
            open(stderr_path, "w", encoding="utf-8") as errors:
        process = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE,
                                   stderr=errors, text=True, bufsize=1,
                                   start_new_session=True)
        if pid_path:
            write(pid_path, f"{process.pid}\n")

        def terminate(signum, frame):
            """Ctrl-C, or a supervisor's SIGTERM: take the turn down with us."""
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except (OSError, ProcessLookupError):
                pass
            raise SystemExit(130)

        previous = {sig: signal.signal(sig, terminate)
                    for sig in (signal.SIGINT, signal.SIGTERM)}
        try:
            for line in process.stdout:
                sink.write(line)
                sink.flush()
                if '"tool_use"' in line:
                    tool_calls += 1
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    for block in (event.get("message") or {}).get("content") or []:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            first = ""
                            for key in ("command", "file_path", "pattern", "prompt"):
                                if isinstance(block.get("input"), dict) and \
                                        block["input"].get(key):
                                    first = str(block["input"][key])[:90]
                                    break
                            say(f"    · {block.get('name')}  {first}")
                if time.time() - started > timeout:
                    process.kill()
                    raise TimeoutError
            process.wait(timeout=60)
        except TimeoutError:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except (OSError, ProcessLookupError):
                process.kill()
            return {"exit": -1, "killed": "timeout",
                    "stderr": "turn exceeded the timeout and was killed",
                    "duration": time.time() - started, "tool_calls": tool_calls}
        finally:
            for sig, handler in previous.items():
                signal.signal(sig, handler)
            if pid_path and os.path.isfile(pid_path):
                os.unlink(pid_path)
    return {"exit": process.returncode, "stderr": read(stderr_path)[-2000:],
            "duration": time.time() - started, "tool_calls": tool_calls}


def note_unknown_cost(outcome, fields) -> None:
    """A killed turn has no result event, so its cost reads as 0.00 and understates the run.

    Iteration 1's turn 4 ran 3603 seconds and 255 tool calls — a full Opus-hour — and is logged
    at $0.00, because the cost is reported in the result event and a killed turn never emits one
    (H-005). Zero is a number a reader will add up; unknown is not. Where the transcript carries
    per-message usage, a floor is derived from it and labelled as a floor.
    """
    if fields.get("cost_usd") is not None:
        return
    fields["cost_usd"] = None
    fields["cost-unknown"] = True
    fields["cost-note"] = (f"the turn ended without a result event "
                           f"({outcome.get('killed') or 'no result'}), so no cost was reported; "
                           f"it ran {outcome.get('duration', 0):.0f}s and "
                           f"{outcome.get('tool_calls', 0)} tool call(s)")


def turn_result_fields(transcript_path):
    events = audit.load_transcript(transcript_path)
    result = audit.result_event(events) or {}
    return audit.tool_uses(events), {
        "is_error": result.get("is_error"),
        "subtype": result.get("subtype"),
        "num_turns": result.get("num_turns"),
        "stop_reason": result.get("stop_reason"),
        "session_id": result.get("session_id"),
        "cost_usd": result.get("total_cost_usd"),
        "permission_denials": result.get("permission_denials"),
        "result_text": (result.get("result") or "")[-1200:],
    }


# ---------------------------------------------------------------------------------------------
# the driver


class Run:
    def __init__(self, args):
        self.config = load_iteration(args.iteration)
        self.iteration = self.config["id"]
        self.project_dir = os.path.join(os.path.abspath(os.path.expanduser(args.root)),
                                        self.config["project"])
        self.run_dir = os.path.join(RUNS, self.iteration)
        self.turns_dir = os.path.join(self.run_dir, "turns")
        self.log_path = os.path.join(self.run_dir, "iteration-log.jsonl")
        self.state_path = os.path.join(self.run_dir, "state.json")
        self.sim_log = os.path.join(self.run_dir, "SIM-LOG.md")
        self.pid_path = os.path.join(self.run_dir, "turn.pid")
        self.driver_pid_path = os.path.join(self.run_dir, "driver.pid")
        self.args = args
        self.max_turns = args.max_turns or self.config.get("max-turns", 24)
        # H-022: how many consecutive turns the worker gets to make a broken workspace validate
        # again before the stop stands. Read exactly the way --max-turns is read, so no existing
        # iteration config has to carry the key to get the allowance.
        self.repair_turns = args.repair_turns or self.config.get("repair-turns", 2)
        self.worker_model = args.worker_model or self.config.get("worker-model", "opus")
        self.sim_model = args.sim_model or self.config.get("sim-model", "sonnet")
        # H-006: a turn is "as much as fits" unless something says otherwise, and iteration 1's
        # turn 4 legally ran answer-questions, refine, plan, implement and most of verify across
        # two items — 255 tool calls — so --turn-timeout killed a healthy run precisely because
        # it was going well. Bounding the turn makes turns comparable, makes the timeout mean
        # something, and bounds the blast radius of every kill.
        self.skills_per_turn = (args.skills_per_turn
                                or self.config.get("worker-skills-per-turn", 3))
        self.state = None
        self.console_log = ""

    # -- state ---------------------------------------------------------------------------

    def load_state(self):
        if os.path.isfile(self.state_path):
            with open(self.state_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        return None

    def save_state(self):
        write(self.state_path, json.dumps(self.state, indent=2, sort_keys=True) + "\n")

    def log(self, record):
        os.makedirs(self.run_dir, exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    def archive(self):
        if not os.path.isdir(self.run_dir):
            return
        index = 1
        while os.path.isdir(f"{self.run_dir}.{index}"):
            index += 1
        destination = f"{self.run_dir}.{index}"
        shutil.move(self.run_dir, destination)
        mark_archived(destination)
        say(f"archived the previous run to {os.path.basename(destination)}")

    def stop(self, reason, detail=""):
        self.state["status"] = "stopped"
        self.state["stop-reason"] = reason
        self.state["stop-detail"] = detail
        self.state["stopped"] = now()
        self.save_state()
        self.log({"event": "stop", "at": now(), "reason": reason, "detail": detail})
        say("")
        say(f"STOP — {reason}")
        if detail:
            for line in detail.split("\n"):
                say(f"       {line}")
        say(f"run directory: {self.run_dir}")
        return 0

    # -- turns ---------------------------------------------------------------------------

    def worker_turn(self, number, job=None):
        name = worker_prompt_name(job)
        body, version = prompt_text(name)
        values = {"PROJECT_DIR": self.project_dir, "TURN": number,
                  "STATUS_FILE": STATUS_FILE, "SKILLS_PER_TURN": self.skills_per_turn}
        if name == "repair-turn":
            values.update({"VALIDATOR_ERROR": self.state.get("repair-last-detail", ""),
                           "ORIGINAL_ERROR": self.state.get("repair-original-detail", ""),
                           "ATTEMPT": self.state.get("repair-turns-used", 1),
                           "REPAIR_TURNS": self.repair_turns})
        prompt = fill(body, values)
        started_at = time.time()
        argv = ["claude", "-p", prompt,
                "--model", self.worker_model,
                "--permission-mode", self.args.worker_permission_mode,
                "--disallowedTools", "AskUserQuestion",
                "--output-format", "stream-json", "--verbose"]
        if self.args.max_budget_usd:
            argv += ["--max-budget-usd", str(self.args.max_budget_usd)]
        transcript = os.path.join(self.turns_dir, f"{number:03d}-worker.stream.jsonl")
        say(f"turn {number} — worker ({self.worker_model}, "
            f"{self.args.worker_permission_mode}"
            + (f", repair {values['ATTEMPT']}/{self.repair_turns}"
               if name == "repair-turn" else "") + ")")
        outcome = stream_turn(argv, self.project_dir, transcript, self.args.turn_timeout,
                              self.pid_path)
        uses, fields = turn_result_fields(transcript)
        note_unknown_cost(outcome, fields)
        repo_before = self.state.get("repo-snapshot") or []
        violations = audit.audit_worker(uses, self.project_dir, HERE, REPO) + \
            audit.audit_repo_tree(REPO, repo_before)
        report, status_text = worker_report(self.project_dir, not_before=started_at,
                                            turn=number)
        if status_text:
            write(os.path.join(self.turns_dir, f"{number:03d}-worker.status.md"), status_text)
        else:
            say(f"    ! turn {number} wrote no status file of its own; whatever is on disk is "
                f"older than this turn or is stamped for another one, and is not being "
                f"attributed to it")
        return {"role": "worker", "job": job, "prompt": name,
                "prompt-version": version, "model": self.worker_model,
                "transcript": os.path.relpath(transcript, self.run_dir),
                "outcome": outcome, "result": fields, "violations": violations,
                "status-written": bool(status_text),
                "worker-report": report}, uses

    def sim_turn(self, number, job):
        persona_file, probe_file = render_sim_skill(self.config)
        body, version = prompt_text("sim-turn")
        prompt = fill(body, {"PROJECT_DIR": self.project_dir, "TURN": number,
                             "SIM_LOG": self.sim_log, "PERSONA_FILE": persona_file,
                             "PROBE_FILE": probe_file, "JOB": job, "NOW": now()})
        argv = ["claude", "-p", prompt,
                "--model", self.sim_model,
                "--permission-mode", "acceptEdits",
                "--add-dir", self.project_dir,
                "--tools", "Read,Write,Edit,Glob,Grep",
                "--output-format", "stream-json", "--verbose"]
        if self.args.max_budget_usd:
            argv += ["--max-budget-usd", str(self.args.max_budget_usd)]
        transcript = os.path.join(self.turns_dir, f"{number:03d}-sim.stream.jsonl")
        say(f"turn {number} — sim ({self.sim_model}, job={job}, "
            f"persona={self.config['persona']})")
        before = audit.question_frontmatter_snapshot(self.project_dir)
        answers_before = audit.question_answer_snapshot(self.project_dir)
        requests_before = open_requests(self.project_dir)
        outcome = stream_turn(argv, HERE, transcript, self.args.turn_timeout, self.pid_path)
        uses, fields = turn_result_fields(transcript)
        note_unknown_cost(outcome, fields)
        violations = audit.audit_sim(uses, self.project_dir, HERE, self.sim_log) + \
            audit.audit_sim_tree(self.project_dir, before)
        silence = audit.sim_turn_outcome(
            answers_before, audit.question_answer_snapshot(self.project_dir),
            audit.sim_log_entry(self.sim_log, number),
            requests_before, open_requests(self.project_dir))
        self.report_sim_outcome(number, silence)
        return {"role": "sim", "job": job, "prompt-version": version, "model": self.sim_model,
                "transcript": os.path.relpath(transcript, self.run_dir),
                "outcome": outcome, "result": fields, "violations": violations,
                "sim-outcome": silence}, uses

    @staticmethod
    def report_sim_outcome(number, silence):
        """Say what the stakeholder did with what was asked of them — including nothing.

        A sim turn that writes no `## Answer` is not a failed turn and never was: nothing in the
        audit calls it one, and a persona whose whole script is to stop replying produces one
        every turn (ADR-0011 §6). What it *is* had no name until now, and no line in the trail.
        Both silences get one, and they are not the same line: the scripted one is a turn that
        succeeded, the unaccounted one is the driver saying it cannot tell a silent stakeholder
        from a broken sim and refusing to pick.
        """
        if silence["outcome"] == "answered":
            spoke = silence["answered"] + [f"request {name}"
                                           for name in silence["requests-filed"]]
            say(f"    the stakeholder spoke: {', '.join(spoke)}"
                + (f"; withheld {', '.join(silence['withheld'])}" if silence["withheld"] else ""))
        elif silence["outcome"] == "scripted-silence":
            say(f"    scripted silence — the stakeholder answered nothing and logged the "
                f"withholding of {', '.join(silence['withheld'])} against the probe that "
                f"scripted it. A successful turn that answered nothing.")
        elif silence["outcome"] == "unexplained-silence":
            say(f"    ! turn {number} answered nothing and its SIM-LOG entry does not record "
                f"withholding {', '.join(silence['withheld'])}"
                + ("" if silence["log-entry"] else " — and there is no entry for this turn")
                + "; this may be a broken sim rather than a silent stakeholder")
        else:
            say("    nothing was open and addressed to the stakeholder; the turn had nothing "
                "to answer")

    # -- the loop ------------------------------------------------------------------------

    def main(self):
        if not os.path.isdir(self.project_dir):
            sys.stderr.write(
                f"run: {self.project_dir} does not exist.\n"
                f"     Provision it first:  harness/provision.py --iteration {self.iteration}\n")
            return 2
        # H-012. Before the first line of output: the run directory exists and the console log
        # is open, so the driver's own narrative is a file in the run rather than something a
        # wrapper was supposed to catch. `--fresh` archives first, or the log would be written
        # into the directory that is about to move.
        if self.args.fresh:
            self.archive()
        os.makedirs(self.turns_dir, exist_ok=True)
        self.console_log = open_console_log(self.args.console_log
                                            or os.path.join(self.run_dir, "driver-console.log"))
        if self.console_log:
            say(f"console log: {self.console_log}")

        running = another_driver(self.driver_pid_path)
        if running:
            sys.stderr.write(
                f"run: driver pid {running} is already running this iteration.\n"
                "     Stop it before starting another; two drivers would interleave turns\n"
                "     into the same workspace.\n")
            return 2
        write(self.driver_pid_path, f"{os.getpid()}\n")

        self.state = self.load_state()
        if self.state and self.args.reaudit:
            code = self.reaudit()
            if code:
                return code
        if self.state and self.state.get("project") != self.project_dir:
            sys.stderr.write(
                f"run: the existing run for {self.iteration} is against\n"
                f"       {self.state.get('project')}\n"
                f"     but this invocation resolves to\n"
                f"       {self.project_dir}\n"
                "     Resuming would mix two projects in one log. Pass --fresh to archive the\n"
                "     old run, or point --root at the project the run belongs to.\n")
            return 2
        if self.state and self.state.get("status") == "stopped" and not self.args.fresh:
            reason = self.state.get("stop-reason")
            if stop_is_resumable(reason, scan_project(self.project_dir)):
                say(f"the previous run stopped on {reason!r} — "
                    f"{RESUMABLE_STOPS.get(reason) or CONDITIONAL_STOPS[reason]}")
                if reason in CONDITIONAL_STOPS:
                    say(f"resuming in place at turn {self.state['turn'] + 1} of "
                        f"{self.max_turns}; nothing was interrupted and nothing is archived")
                    if self.state["turn"] >= self.max_turns:
                        say("     the budget is still spent — pass a larger --max-turns")
                else:
                    say("resuming: the interrupted turn runs again, and every skill reconciles "
                        "with what it finds on disk")
                self.log({"event": "resume-after-stop", "at": now(), "stop-reason": reason,
                          "stop-detail": self.state.get("stop-detail")})
                self.state["status"] = "running"
                for field in ("stop-reason", "stop-detail", "stopped"):
                    self.state.pop(field, None)
                self.state["resumed-after"] = reason
                self.save_state()
            else:
                say(f"this run already stopped: {reason} — "
                    f"{TERMINAL_STOPS.get(reason, 'a terminal stop')}")
                say("that is a verdict on the run, not an interruption, so rerunning will not "
                    "continue it.")
                say(f"  --fresh   archives {os.path.basename(self.run_dir)} (the driver's logs, "
                    f"state and transcripts) and starts a new run")
                say(f"            against the SAME project workspace at {self.project_dir},")
                say("            which keeps whatever the last run built. To start from an "
                    "empty project as well,")
                say(f"            run  harness/provision.py --iteration {self.iteration} --wipe "
                    f" first.")
                if reason == "contamination":
                    say("  --reaudit re-runs the contamination rules over the stored "
                        "transcripts and clears")
                    say("            the stop if today's rules find them clean")
                return 0
        if self.state is None:
            role, job, why = first_job(self.project_dir)
            say(f"first turn: {role}" + (f" ({job})" if job else "") + f" — {why}")
            self.state = {"iteration": self.iteration, "project": self.project_dir,
                          "started": now(), "turn": 0, "next-role": role, "next-job": job,
                          "status": "running", "fingerprints": []}
            self.save_state()
            self.log({"event": "start", "at": now(), "iteration": self.iteration,
                      "first-role": role, "first-job": job, "first-job-because": why,
                      "project": self.project_dir, "config": self.config,
                      "max-turns": self.max_turns, "repair-turns": self.repair_turns,
                      "worker-model": self.worker_model,
                      "sim-model": self.sim_model,
                      "worker-permission-mode": self.args.worker_permission_mode})
        else:
            orphan = reap_orphan(self.pid_path)
            if orphan:
                say(f"reaped an orphaned turn process (pid {orphan}) left by the previous driver")
            in_flight = self.state.get("in-flight")
            say(f"resuming {self.iteration} at turn {self.state['turn'] + 1} "
                f"({self.state['next-role']})")
            if in_flight:
                say(f"turn {in_flight['turn']} ({in_flight['role']}) was interrupted; "
                    "running it again — every skill reconciles with what it finds on disk")
            self.log({"event": "resume", "at": now(), "from-turn": self.state["turn"],
                      "next-role": self.state["next-role"], "interrupted": in_flight,
                      "reaped-pid": orphan})

        while True:
            if self.state["turn"] >= self.max_turns:
                # H-014, first half: the counter never overrules the disk. A workspace at a
                # terminal ending has finished, and saying otherwise mislabels a completed run.
                observed = scan_project(self.project_dir)
                terminal, reason, detail = engagement_terminal(observed)
                if terminal:
                    return self.stop(reason, f"{detail}; the turn budget was spent at the same "
                                             f"moment and the workspace is what says what "
                                             f"happened")
                # H-014, second half: the H-007 closing turn exists for the engagement's benefit,
                # not the budget's. It is one turn, it is given once, and refusing it means the
                # stakeholder never sees the ending of exactly the runs that ran long.
                if self.state.get("next-job") == "closing":
                    say(f"    the {self.max_turns}-turn budget is spent, and the closing turn is "
                        f"not the budget's to spend — giving it")
                    self.log({"event": "budget-exempt", "at": now(),
                              "turn": self.state["turn"] + 1, "job": "closing"})
                else:
                    return self.stop("turn-budget",
                                     f"{self.max_turns} turns used; the engagement is not at an "
                                     f"ending, so this stop is resumable — rerun with a larger "
                                     f"--max-turns and it continues in place")

            number = self.state["turn"] + 1
            role = self.state["next-role"]
            if role == "worker" and self.state.get("next-job") == "repair":
                # H-022, against H-004. The reschedule below exists because a worker turn taken
                # with unanswered human questions open halts at orchestrator step 2 having done
                # nothing. A repair turn does not run the orchestrator at all — its only job is
                # making `validate-workspace` green, which no stakeholder answer can help with —
                # so the premise of the reschedule is false here. Handing this turn to the sim
                # would spend one of a bounded number of repair turns on something that cannot
                # repair anything, and hand the repair instruction to nobody: `decide` re-derives
                # `next-job` from the sim turn, and the repair job would be lost with it.
                say("    a repair turn is owed and it is not reschedulable — no answer makes a "
                    "broken workspace validate")
                self.log({"event": "repair-keeps-the-turn", "at": now(), "turn": number})
            elif role == "worker":
                # H-004: on a start or a resume, next-role comes from state rather than from a
                # decision, so the driver used to walk a worker turn straight into unanswered
                # human questions. The orchestrator correctly halts at step 2 and the whole turn
                # is a no-op — iteration 1's turn 2 was exactly that. The observation is free.
                reading = scan_project(self.project_dir)
                pending = reading["unanswered-human-questions"]
                gone = engagements_abandoned(reading)
                if pending and gone:
                    # The one case where handing the turn to the sim is the wrong move for the
                    # same reason it is usually the right one. The questions are open and
                    # unanswered because the stakeholder is gone; the worker keeps the turn and
                    # declares the ending (ADR-0011 §5).
                    say(f"    {len(pending)} human question(s) are open and unanswered, and "
                        f"engagement-state reports abandoned ({', '.join(gone)}); the worker "
                        f"keeps the turn — another sim turn would ask a stakeholder the "
                        f"pipeline has already established is gone")
                    self.log({"event": "abandonment-pending", "at": now(), "turn": number,
                              "epics": gone, "questions": pending})
                elif pending:
                    say(f"    {len(pending)} human question(s) are open and unanswered "
                        f"({', '.join(pending)}); giving the turn to the sim instead — a worker "
                        f"turn would halt at orchestrator step 2 having done nothing")
                    self.log({"event": "reschedule", "at": now(), "turn": number,
                              "from-role": "worker", "to-role": "sim",
                              "because": "unanswered human questions", "questions": pending})
                    role = "sim"
                    self.state["next-role"] = "sim"
                    self.state["next-job"] = "answer"
            self.state["repo-snapshot"] = audit.repo_tree_snapshot(REPO)
            self.state["in-flight"] = {"turn": number, "role": role,
                                       "job": self.state.get("next-job")}
            self.save_state()

            if role == "worker":
                record, _ = self.worker_turn(number, self.state.get("next-job"))
            else:
                record, _ = self.sim_turn(number, self.state.get("next-job") or "answer")

            observed = scan_project(self.project_dir)
            record.update({"event": "turn", "turn": number, "at": now(),
                           "observed": {k: observed[k] for k in
                                        ("items", "validator-exit", "head",
                                         "open-human-questions",
                                         "unanswered-human-questions", "blocked-items",
                                         "open-requests", "engagements",
                                         "abandoned-epics")}})
            self.log(record)
            self.state["turn"] = number
            self.state["in-flight"] = None
            self.state.setdefault("fingerprints", []).append(fingerprint(observed))
            self.save_state()

            cost = record["result"].get("cost_usd")
            summary = (f"exit={record['outcome']['exit']} "
                       f"{record['outcome']['duration']:.0f}s "
                       f"tools={record['outcome']['tool_calls']} "
                       + (f"cost=${cost:.2f}" if cost is not None else "cost=unknown"))
            say(f"turn {number} done: {summary}")

            if record["violations"]:
                detail = "\n".join(f"{v['rule']} {v['tool']}: {v['detail']}"
                                   for v in record["violations"])
                return self.stop("contamination", detail)

            if record["outcome"]["exit"] != 0 or record["result"].get("is_error"):
                text = (f"{record['outcome']['stderr'][-400:] or ''}"
                        f"{record['result'].get('result_text', '')[-400:]}")
                # All three are interruptions rather than verdicts, so all three are resumable
                # (H-002). Naming them apart is what makes the iteration log answer "why did
                # this run stop" without opening a transcript.
                if record["outcome"].get("killed") == "timeout":
                    reason = "turn-timeout"
                elif looks_api_rejected(text):
                    reason = "api-rejected"
                else:
                    reason = "turn-failed"
                return self.stop(reason,
                                 f"turn {number} ({role}) exited "
                                 f"{record['outcome']['exit']}: {text}\n"
                                 f"This stop is resumable: rerun the same command and the "
                                 f"interrupted turn runs again.")

            decision = self.decide(role, observed, record)
            if decision["stop"]:
                return self.stop(decision["reason"], decision["detail"])
            self.state["next-role"] = decision["next-role"]
            self.state["next-job"] = decision.get("next-job")
            self.save_state()

    def reaudit(self):
        """Re-run the contamination audit over every stored transcript, with today's rules.

        A stop for contamination is either a real violation or a defect in a rule. The second
        happens — the first real worker turn of iteration 1 was stopped by a rule that matched a
        path quoted inside a document the worker was writing. The recovery must not be "edit
        state.json by hand": it must be to fix the rule, re-audit the evidence that is still on
        disk, and let the run continue only if the evidence is now clean. That is what this is.
        """
        say("re-auditing every stored transcript with the current rules")
        remaining = []
        for name in sorted(os.listdir(self.turns_dir)):
            if not name.endswith(".stream.jsonl"):
                continue
            path = os.path.join(self.turns_dir, name)
            uses = audit.tool_uses(audit.load_transcript(path))
            if name.endswith("worker.stream.jsonl"):
                found = audit.audit_worker(uses, self.project_dir, HERE, REPO)
            else:
                found = audit.audit_sim(uses, self.project_dir, HERE, self.sim_log)
            say(f"  {name}: {len(found)} violation(s)")
            for item in found:
                say(f"    {item['rule']} {item['tool']}: {item['detail']}")
            remaining.extend(found)
        self.log({"event": "reaudit", "at": now(), "violations": remaining})
        if remaining:
            sys.stderr.write("run: the stored transcripts still violate the boundary; "
                             "not resuming.\n")
            return 2
        if self.state.get("stop-reason") == "contamination":
            self.state["status"] = "running"
            self.state["stop-reason"] = None
            self.state["stop-detail"] = "cleared by --reaudit: the rules that fired were fixed"
            # A contamination stop happens *before* the turn's decision is taken, so `next-role`
            # still says whatever it said before that turn. Re-deriving it from the workspace is
            # not a nicety: resuming without it repeats the turn that was already completed, and
            # a repeated worker turn costs real money to reach the same stop.
            last = self.last_turn()
            if last:
                observed = scan_project(self.project_dir)
                decision = self.decide(last["role"], observed, last)
                if decision["stop"]:
                    say(f"the workspace itself now says: {decision['reason']}")
                else:
                    self.state["next-role"] = decision["next-role"]
                    self.state["next-job"] = decision.get("next-job")
                    say(f"next turn re-derived from the workspace: {decision['next-role']}"
                        f" ({decision.get('next-job') or '-'})")
            self.save_state()
            say("the contamination stop is cleared; the run continues")
        return 0

    def last_turn(self):
        """The most recent completed turn record in the iteration log."""
        record = None
        if not os.path.isfile(self.log_path):
            return None
        with open(self.log_path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if entry.get("event") == "turn":
                    record = entry
        return record

    def decide(self, role, observed, record):
        """What happens after a turn — the stop conditions of DESIGN §2, computed from disk."""
        if role == "sim":
            # A sim turn neither burns nor resets the repair allowance below: the contamination
            # boundary confines the stakeholder to answers and requests, so it can neither break
            # the record nor repair it. "Consecutive" counts worker turns.
            return {"stop": False, "next-role": "worker", "next-job": None}

        report = record.get("worker-report") or {}
        reported = report.get("stop_reason")
        if reported and reported not in WORKER_STOP_REASONS:
            say(f"    ! worker reported an unknown stop_reason: {reported!r}")

        if observed["validator-exit"] != 0:
            # H-022: a fixable record defect is not a verdict on the engagement. Iteration 5 died
            # here at turn 11 over one prose mention scraped as a citation (F-113) — with all
            # nineteen of the item's acceptance criteria passing, all seven binding ADRs
            # conforming and 69 tests green. That stop read a fact about one line of prose as a
            # verdict on the work, and asked a human to repair a record the worker could have
            # repaired itself.
            #
            # H-010 settled the same question one level up: a budget bounds *work*, not the
            # engagement. So the worker gets a bounded allowance — N consecutive turns whose only
            # job is making the workspace validate — and only spending it is terminal. Bounded,
            # because an unbounded allowance is ADR-0011 Context (b)'s loop in another costume:
            # try, fail, repeat until the turn budget is gone. Consecutive, because a repair that
            # worked is progress: N bounds *this* defect, not the run's lifetime supply of them.
            detail = validator_detail(observed)
            used = self.state.get("repair-turns-used", 0) + 1
            self.state["repair-turns-used"] = used
            self.state["repair-last-detail"] = detail
            if used == 1:
                self.state["repair-original-detail"] = detail
            original = self.state.get("repair-original-detail") or detail
            if used > self.repair_turns:
                # The original error is the finding; whatever it exits on now may be a symptom of
                # the repair. A stop reporting only the last error reports the wrong defect —
                # and the value of iteration 5's trail is entirely in the first one.
                self.log({"event": "repair-exhausted", "at": now(), "granted": used - 1,
                          "allowed": self.repair_turns, "original": original, "last": detail})
                if original == detail:
                    said = (f"The error that opened the allowance is the one it still exits on: "
                            f"{original}")
                else:
                    said = (f"The error that opened the allowance: {original}\n"
                            f"The error it exits on now:           {detail}")
                return {"stop": True, "reason": "validator-failed",
                        "detail": f"{self.repair_turns} repair turn(s) did not make the "
                                  f"workspace validate.\n{said}"}
            say(f"    the workspace does not validate: {detail}")
            say(f"    granting repair turn {used} of {self.repair_turns} — the next worker turn's "
                f"only job is making validate-workspace green, and nothing advances until it is")
            self.log({"event": "repair-granted", "at": now(), "attempt": used,
                      "allowed": self.repair_turns, "original": original, "detail": detail})
            return {"stop": False, "next-role": "worker", "next-job": "repair"}

        if self.state.get("repair-turns-used"):
            # Green again: the counter resets and the engagement resumes where it was — every
            # branch below re-derives that from disk, as it does on any other turn.
            say(f"    the workspace validates again after "
                f"{self.state['repair-turns-used']} repair turn(s); the engagement resumes")
            self.log({"event": "repair-succeeded", "at": now(),
                      "granted": self.state["repair-turns-used"],
                      "original": self.state.get("repair-original-detail")})
            self.state["repair-turns-used"] = 0
            for field in ("repair-original-detail", "repair-last-detail"):
                self.state.pop(field, None)

        if observed.get("open-requests"):
            # F-021: the stakeholder has spoken and nothing has answered yet. `next` routes an
            # open request before it selects work, so the worker is the one to run — and the run
            # is not finished no matter what the item statuses say.
            say(f"    open stakeholder request(s): "
                f"{', '.join(observed['open-requests'])} — the worker handles them next")
            return {"stop": False, "next-role": "worker", "next-job": None}

        declared = abandonment_declared(observed)
        if declared:
            # H-008's lesson, applied to an ending rather than to an impasse: a stall is a fact
            # about this driver's own progress and an ending is a fact about the engagement, and
            # the two coincided here until they didn't. E4 used to fall through every branch
            # below and land on `stalled` — "three turns changed nothing" — which is true of the
            # run and says nothing about what happened, which is that the person left.
            #
            # No closing sim turn, and that is the one place E4 departs from H-007. The closing
            # turn exists so the stakeholder sees the ending of every run; this ending is the
            # recorded finding that there is no stakeholder to show it to, established over the
            # threshold's worth of halts and readable in the waiting log.
            return {"stop": True, "reason": "abandoned",
                    "detail": abandonment_detail(declared)
                    + "\nThis is not a stall: the driver kept making progress and the "
                      "engagement ended. Both facts are in the log."}

        awaiting_declaration = engagements_abandoned(observed)
        if awaiting_declaration:
            # `abandoned` is `at-rest`'s twin (ADR-0011 §5): the ending is due and unrecorded, and
            # the worker's next turn is the one that records it. Routing to the sim here — which
            # every branch below would do, because human questions are open and unanswered by
            # definition of this verdict — is the loop ADR-0011's Context (b) describes: ask a
            # stakeholder who is gone, get nothing, repeat until the budget is spent.
            say(f"    engagement-state reports abandoned: "
                f"{', '.join(awaiting_declaration)} — the ending is E4 and it is not recorded; "
                f"the worker runs review-close to declare it. No sim turn: the pipeline has "
                f"already established there is nobody to ask.")
            return {"stop": False, "next-role": "worker", "next-job": None}

        if epic_complete(observed):
            # H-007: a self-sufficient worker used to end the engagement unilaterally — run 1b
            # went epic-done at turn 6 with the sim locked out from turn 5 onward, so a mid-run
            # probe edit could never fire and the sim never saw the endgame of a clean run.
            # F-022's sign-off question usually opens a human question at closure and routes a
            # sim turn anyway; this is the belt to that pair of braces, and it is what makes
            # "the sim sees every ending" true rather than usually true.
            if not self.state.get("closing-turn-given"):
                say("    the epic is done; giving the sim one closing turn before accepting it")
                self.state["closing-turn-given"] = True
                return {"stop": False, "next-role": "sim", "next-job": "closing"}
            return {"stop": True, "reason": "epic-done",
                    "detail": f"{len(observed['items'])} item(s), all done"}

        if observed["unanswered-human-questions"]:
            if reported and reported != "human-question-open":
                say(f"    ! the worker reported {reported!r} but "
                    f"{len(observed['unanswered-human-questions'])} human question(s) are open")
            return {"stop": False, "next-role": "sim", "next-job": "answer"}

        if observed["blocked-items"] and not observed["open-human-questions"]:
            # The impasse DESIGN §2 calls "blocked with no recourse": nothing is outstanding for
            # the human, so there is nothing another sim turn could *answer*.
            #
            # H-008: the test is whether the ENGAGEMENT is over, not whether an item is blocked.
            # Those coincided in 1d, where the blocked item was the last one standing. They stop
            # coinciding as soon as an item is parked early — and then this branch ends a run
            # with most of its work unbuilt.
            if not engagement_at_rest(observed):
                say(f"    blocked: {', '.join(observed['blocked-items'])} — but the engagement "
                    f"is not at rest; there is still work for a worker turn")
            elif not engagements_ended(observed):
                # F-045: at rest with the epic still `open` means the engagement is over and its
                # ending is not recorded. The worker's next turn is the one that asks the
                # stakeholder and writes it down. Stopping here is stopping one turn before the
                # thing the run exists to observe — which is what 1d did.
                say("    the engagement is at rest and its ending is not recorded; the worker "
                    "runs to end it through the stakeholder")
                return {"stop": False, "next-role": "worker", "next-job": None}
            else:
                # H-007, extended: there is still something a sim turn can *say*. An impasse is
                # an ending, and the stakeholder should see the ending of every run rather than
                # only the ones that finish cleanly — the same argument that gave `epic-done` a
                # closing turn. One turn, once, then the stop stands.
                if not self.state.get("closing-turn-given"):
                    say("    the engagement has ended at an impasse; giving the sim one closing "
                        "turn before accepting it")
                    self.state["closing-turn-given"] = True
                    return {"stop": False, "next-role": "sim", "next-job": "closing"}
                return {"stop": True, "reason": "blocked-no-recourse",
                        "detail": f"blocked: {', '.join(observed['blocked-items'])}; "
                                  "no question is open to the human"}

        fingerprints = self.state.get("fingerprints", [])
        if len(fingerprints) >= 3 and fingerprints[-1] == fingerprints[-2] == fingerprints[-3]:
            # Reached only with no epic abandoned and no E4 declared — both are handled above —
            # so this stop can say what it is not. A run can stall while the engagement is
            # perfectly alive, and an engagement can be abandoned while the driver is still
            # making progress; the two branches exist because those are different facts about
            # different things (H-008).
            verdicts = ", ".join(f"{epic} {state['verdict']}"
                                 for epic, state in
                                 sorted((observed.get("engagements") or {}).items()))
            return {"stop": True, "reason": "stalled",
                    "detail": "three turns changed nothing in the workspace — a fact about this "
                              "run's progress, not about the engagement.\n"
                              "No epic is abandoned and no ending is recorded: "
                              + (verdicts or "engagement-state reported no epic")}

        if observed["open-human-questions"]:
            return {"stop": False, "next-role": "sim", "next-job": "answer"}
        return {"stop": False, "next-role": "worker", "next-job": None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--iteration", required=True)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--max-turns", type=int, default=None,
                        help="turn budget for the whole iteration (default: the config's)")
    parser.add_argument("--repair-turns", type=int, default=None,
                        help="consecutive turns the worker may spend making a broken workspace "
                             "validate again before the run stops (default: the config's, or 2)")
    parser.add_argument("--console-log", default=None,
                        help="where the driver writes its own console narrative "
                             "(default: <run-dir>/driver-console.log)")
    parser.add_argument("--turn-timeout", type=int, default=3600,
                        help="wall-clock seconds before a single turn is killed")
    parser.add_argument("--max-budget-usd", type=float, default=None,
                        help="per-turn spend cap passed to claude")
    parser.add_argument("--worker-model", default=None)
    parser.add_argument("--sim-model", default=None)
    parser.add_argument("--worker-permission-mode", default="bypassPermissions")
    parser.add_argument("--reaudit", action="store_true",
                        help="re-run the contamination audit over the stored transcripts with "
                             "the current rules; clears a contamination stop if they are clean")
    parser.add_argument("--skills-per-turn", type=int,
                        help="how many skill executions a worker turn may run before it stops "
                             "and reports (default: the iteration config's, or 3)")
    parser.add_argument("--fresh", action="store_true",
                        help="archive any existing run for this iteration and start over")
    args = parser.parse_args()
    return Run(args).main()


if __name__ == "__main__":
    raise SystemExit(main())
