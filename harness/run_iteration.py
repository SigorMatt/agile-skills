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
TERMINAL_STOPS = {
    "epic-done": "the run reached its end",
    "blocked-no-recourse": "the run reached an impasse with nothing left to ask",
    "turn-budget": "the configured turn budget is spent",
    "contamination": "a turn read or wrote outside the boundary; --reaudit is the recovery",
    "validator-failed": "the workspace no longer validates; fix it, then --fresh or --reaudit",
    "stalled": "three turns changed nothing",
}


def stop_is_resumable(reason) -> bool:
    return reason in RESUMABLE_STOPS


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


def say(message):
    print(f"[{now()}] {message}", flush=True)


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


def fill(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


# ---------------------------------------------------------------------------------------------
# what the project actually says (never the worker's word for it)


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
        answer = ""
        if "\n## Answer" in text:
            body = text.split("\n## Answer", 1)[1]
            answer = body.split("\n## ", 1)[0]
        answer = "\n".join(line for line in answer.split("\n")
                           if not line.strip().startswith("<!--")).strip()
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
    return {
        "items": items,
        "questions": questions,
        "validator-exit": validator.returncode,
        "validator-tail": (validator.stdout + validator.stderr).strip().split("\n")[-1:],
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


def worker_report(project_dir, not_before=None):
    """The worker's self-report: the last fenced json block in HARNESS-STATUS.md.

    `not_before` is the turn's start time. A turn that was killed never writes the file, and the
    driver used to read whatever was there and log it as that turn's report — iteration 1's turn
    4 was killed after a full Opus-hour and is recorded carrying turn 2's status, two hours stale
    (H-005). A status file older than the turn is not this turn's status.
    """
    path = os.path.join(project_dir, STATUS_FILE)
    if not_before is not None and os.path.isfile(path):
        if os.path.getmtime(path) < not_before:
            return None, ""
    text = read(path)
    if not text:
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
        shutil.move(self.run_dir, f"{self.run_dir}.{index}")
        say(f"archived the previous run to {os.path.basename(self.run_dir)}.{index}")

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

    def worker_turn(self, number):
        body, version = prompt_text("worker-turn")
        prompt = fill(body, {"PROJECT_DIR": self.project_dir, "TURN": number,
                             "STATUS_FILE": STATUS_FILE,
                             "SKILLS_PER_TURN": self.skills_per_turn})
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
            f"{self.args.worker_permission_mode})")
        outcome = stream_turn(argv, self.project_dir, transcript, self.args.turn_timeout,
                              self.pid_path)
        uses, fields = turn_result_fields(transcript)
        note_unknown_cost(outcome, fields)
        repo_before = self.state.get("repo-snapshot") or []
        violations = audit.audit_worker(uses, self.project_dir, HERE, REPO) + \
            audit.audit_repo_tree(REPO, repo_before)
        report, status_text = worker_report(self.project_dir, not_before=started_at)
        if status_text:
            write(os.path.join(self.turns_dir, f"{number:03d}-worker.status.md"), status_text)
        elif outcome.get("killed"):
            say("    ! this turn wrote no status file; the one on disk is older than the turn "
                "and is not being attributed to it")
        return {"role": "worker", "prompt-version": version, "model": self.worker_model,
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
        outcome = stream_turn(argv, HERE, transcript, self.args.turn_timeout, self.pid_path)
        uses, fields = turn_result_fields(transcript)
        note_unknown_cost(outcome, fields)
        violations = audit.audit_sim(uses, self.project_dir, HERE, self.sim_log) + \
            audit.audit_sim_tree(self.project_dir, before)
        return {"role": "sim", "job": job, "prompt-version": version, "model": self.sim_model,
                "transcript": os.path.relpath(transcript, self.run_dir),
                "outcome": outcome, "result": fields, "violations": violations}, uses

    # -- the loop ------------------------------------------------------------------------

    def main(self):
        if not os.path.isdir(self.project_dir):
            sys.stderr.write(
                f"run: {self.project_dir} does not exist.\n"
                f"     Provision it first:  harness/provision.py --iteration {self.iteration}\n")
            return 2
        running = another_driver(self.driver_pid_path)
        if running:
            sys.stderr.write(
                f"run: driver pid {running} is already running this iteration.\n"
                "     Stop it before starting another; two drivers would interleave turns\n"
                "     into the same workspace.\n")
            return 2
        if self.args.fresh:
            self.archive()
        os.makedirs(self.turns_dir, exist_ok=True)
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
            if stop_is_resumable(reason):
                say(f"the previous run stopped on {reason!r} — {RESUMABLE_STOPS[reason]}")
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
            self.state = {"iteration": self.iteration, "project": self.project_dir,
                          "started": now(), "turn": 0, "next-role": "sim", "next-job": "open",
                          "status": "running", "fingerprints": []}
            self.save_state()
            self.log({"event": "start", "at": now(), "iteration": self.iteration,
                      "project": self.project_dir, "config": self.config,
                      "max-turns": self.max_turns, "worker-model": self.worker_model,
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
                return self.stop("turn-budget",
                                 f"{self.max_turns} turns used; the run was not finished")

            number = self.state["turn"] + 1
            role = self.state["next-role"]
            if role == "worker":
                # H-004: on a start or a resume, next-role comes from state rather than from a
                # decision, so the driver used to walk a worker turn straight into unanswered
                # human questions. The orchestrator correctly halts at step 2 and the whole turn
                # is a no-op — iteration 1's turn 2 was exactly that. The observation is free.
                pending = scan_project(self.project_dir)["unanswered-human-questions"]
                if pending:
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
                record, _ = self.worker_turn(number)
            else:
                record, _ = self.sim_turn(number, self.state.get("next-job") or "answer")

            observed = scan_project(self.project_dir)
            record.update({"event": "turn", "turn": number, "at": now(),
                           "observed": {k: observed[k] for k in
                                        ("items", "validator-exit", "head",
                                         "open-human-questions",
                                         "unanswered-human-questions", "blocked-items",
                                         "open-requests")}})
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
            return {"stop": False, "next-role": "worker", "next-job": None}

        report = record.get("worker-report") or {}
        reported = report.get("stop_reason")
        if reported and reported not in WORKER_STOP_REASONS:
            say(f"    ! worker reported an unknown stop_reason: {reported!r}")

        if observed["validator-exit"] != 0:
            return {"stop": True, "reason": "validator-failed",
                    "detail": "validate-workspace exits "
                              f"{observed['validator-exit']}: "
                              f"{' '.join(observed['validator-tail'])}"}

        if observed.get("open-requests"):
            # F-021: the stakeholder has spoken and nothing has answered yet. `next` routes an
            # open request before it selects work, so the worker is the one to run — and the run
            # is not finished no matter what the item statuses say.
            say(f"    open stakeholder request(s): "
                f"{', '.join(observed['open-requests'])} — the worker handles them next")
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
            return {"stop": True, "reason": "stalled",
                    "detail": "three turns changed nothing in the workspace"}

        if observed["open-human-questions"]:
            return {"stop": False, "next-role": "sim", "next-job": "answer"}
        return {"stop": False, "next-role": "worker", "next-job": None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--iteration", required=True)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--max-turns", type=int, default=None,
                        help="turn budget for the whole iteration (default: the config's)")
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
