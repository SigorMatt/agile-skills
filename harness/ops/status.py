#!/usr/bin/env python3
"""One-shot ops status. Run: harness/ops/status.py --iteration <id> [--builder]

The mechanics an ops session used to retype every time, with the traps from
`meta/OPS-CONVENTIONS.md` compiled in rather than remembered:

* **The checkpoint's current unit comes from the `## Current unit` section and nowhere else.**
  `meta/CHECKPOINT.md` also declares the session's *range* — "META-144 .. META-165" — in its
  preamble. A whole-file scan for `META-###` therefore answers confidently and wrongly: first
  match gives META-144, largest gives META-165, and the unit in flight was META-163. This is the
  converse of the silently-empty trap: the file is *loudly full*, so the naive read never looks
  empty enough to doubt.
* **A probe that reports nothing must be able to say why.** Nothing here appends `2>/dev/null`.
  Every subprocess' stderr is captured and printed when non-empty, and an unreadable file is an
  instrument failure with its own line, never an absence.
* **`find` is called with an absolute timestamp.** Relative `-newermt` arguments fail on this
  machine. The stamp is computed here and passed as `YYYY-MM-DD HH:MM:SS`, which both `bfs` and
  GNU `find` accept, and the binary that actually answered is named in the evidence — on this
  machine `find` on `PATH` is GNU findutils, while the `bfs` the conventions describe is an
  interactive shell function a subprocess never sees.

Output is the machine block first (`key=value`, one per line, values flattened to a single
line), then the human block. The exit code is a **hint** — the evidence lines are the report,
and they are printed under every code, including the error paths.

Exit codes, and the table that picks them (printed with the report):

    0  progressing              a subject is running and something moved inside the window
    1  stopped-with-reason      every subject is terminal, and the reason is recorded
    2  process-dead-state-running   state.json says running and no process owns it
    3  stalled-candidate        running but nothing moved, or the state could not be read

With several subjects the worst code wins, in the order 2 > 3 > 1 > 0: a lie about liveness
outranks a stall, and a stall outranks a clean stop.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(HARNESS)

# A run whose status is one of these is history. `archived` is set by `--fresh` moving a
# directory aside (run_iteration.mark_archived); `stopped` is a verdict the driver recorded.
TERMINAL_STATUSES = ("stopped", "archived")

# The checkpoint's current-unit section. The heading may carry trailing prose — the real file has
# read `## Current unit — the last` — so the match is on the prefix, and the section ends at the
# next `## ` heading. A `### ` subheading stays inside, because the checkpoint puts the unit's
# traps and notes there.
CURRENT_UNIT_HEADING = re.compile(r"^##[ \t]+Current unit\b.*$", re.IGNORECASE)
SECTION_BOUNDARY = re.compile(r"^##[ \t]+(?!#)")
UNIT_REF = re.compile(r"\bMETA-([0-9]+)\b")

# Cmdlines that mention an iteration but are not a driver. The scratchpad is where an agent
# session keeps its own scripts and notes, and this tool's own argv necessarily carries the
# iteration ids it was asked about — a status probe that counts itself as the driver reports the
# run as alive forever.
NOT_A_DRIVER = ("/scratchpad", "ops/status.py", "ops/watch.py")

CLOCK_TICKS = os.sysconf("SC_CLK_TCK")

DECISION_TABLE = (
    ("progressing", 0,
     "state running, a process owns it, and a file changed inside the activity window"),
    ("stopped-with-reason", 1,
     "state terminal (stopped/archived); the recorded stop-reason is the verdict"),
    ("process-dead-state-running", 2,
     "state.json says running and no matching process exists"),
    ("stalled-candidate", 3,
     "running with a live process but nothing moved in the window, or the state is unreadable"),
)

# Worst-wins order when several subjects are reported at once.
SEVERITY = (2, 3, 1, 0)


# ---------------------------------------------------------------------------------------------
# reading the record


def read_state(run_dir):
    """`(state, error)` for a run directory. Exactly one of the two is None.

    A missing directory, a missing file and a corrupt file are three different observations and
    are reported as three different sentences. None of them is 'no run'.
    """
    if not os.path.isdir(run_dir):
        return None, f"no run directory at {run_dir}"
    path = os.path.join(run_dir, "state.json")
    if not os.path.isfile(path):
        return None, f"run directory exists but has no state.json: {run_dir}"
    try:
        with open(path, "r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, ValueError) as error:
        return None, f"state.json unreadable ({type(error).__name__}: {error}): {path}"
    if not isinstance(state, dict):
        return None, f"state.json is not an object: {path}"
    return state, None


def run_record(harness, iteration):
    """The run-state line for one iteration, as data."""
    run_dir = os.path.join(harness, "runs", iteration)
    state, error = read_state(run_dir)
    record = {
        "iteration": iteration,
        "run-dir": run_dir,
        "status": None,
        "stop-reason": None,
        "turn": None,
        "project": None,
        "terminal": None,
        "error": error,
    }
    if state is None:
        return record
    record["status"] = state.get("status")
    record["stop-reason"] = state.get("stop-reason")
    record["turn"] = state.get("turn")
    record["project"] = state.get("project")
    record["terminal"] = state.get("status") in TERMINAL_STATUSES
    return record


def current_unit(text):
    """The unit in flight, read from the `## Current unit` section and nowhere else.

    Returns `{"unit", "number", "heading", "error"}`; `unit` is None whenever the section is
    absent or names no unit, and `error` then says which of the two it was. A checkpoint with no
    such section is a real state — the session that closed builder five left one — and it must
    read as 'no current unit', not as the largest number lying around elsewhere in the file.
    """
    lines = text.split("\n")
    start = None
    heading = None
    for index, line in enumerate(lines):
        if CURRENT_UNIT_HEADING.match(line):
            start = index + 1
            heading = line.strip()
            break
    if start is None:
        return {"unit": None, "number": None, "heading": None,
                "error": "no '## Current unit' section in the checkpoint"}
    end = len(lines)
    for index in range(start, len(lines)):
        if SECTION_BOUNDARY.match(lines[index]):
            end = index
            break
    section = "\n".join(lines[start:end])
    match = UNIT_REF.search(section)
    if match is None:
        return {"unit": None, "number": None, "heading": heading,
                "error": f"the {heading!r} section names no META-### unit"}
    return {"unit": match.group(0), "number": int(match.group(1)),
            "heading": heading, "error": None}


def read_checkpoint(repo):
    """`(current_unit_record, path, error)` for `meta/CHECKPOINT.md`."""
    path = os.path.join(repo, "meta", "CHECKPOINT.md")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        return ({"unit": None, "number": None, "heading": None,
                 "error": f"{type(error).__name__}: {error}"}, path, str(error))
    return current_unit(text), path, None


def head_sha(repo, run=subprocess.run):
    """`(sha, error)`. stderr is kept: a git that refused is not a repository with no head."""
    try:
        done = run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
    except OSError as error:
        return None, f"{type(error).__name__}: {error}"
    if done.returncode != 0:
        return None, (done.stderr or "").strip() or f"git exited {done.returncode}"
    return done.stdout.strip(), None


def board_summary(project):
    """The `## Summary` block of `<project>/tracker/board.md`, or an error saying why not."""
    if not project:
        return None, "no project path in state.json"
    path = os.path.join(project, "tracker", "board.md")
    if not os.path.isfile(path):
        return None, f"no board at {path}"
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except OSError as error:
        return None, f"board unreadable ({type(error).__name__}: {error}): {path}"
    collected = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip().lower() == "## summary"
            continue
        if inside and line.strip():
            collected.append(line.rstrip())
    if not collected:
        return None, f"board has no '## Summary' section: {path}"
    return {"path": path, "lines": collected}, None


# ---------------------------------------------------------------------------------------------
# processes


def cpu_ticks(pid):
    """utime+stime for a pid, in clock ticks, or None.

    `comm` can contain spaces and parentheses, so the split is on the LAST `)` — the field-index
    bug this avoids reports a random number as CPU time, which is worse than reporting none.
    """
    try:
        with open(f"/proc/{pid}/stat", "r", encoding="utf-8", errors="replace") as handle:
            raw = handle.read()
    except OSError:
        return None
    try:
        tail = raw[raw.rindex(")") + 2:]
        fields = tail.split()
        return int(fields[11]) + int(fields[12])
    except (ValueError, IndexError):
        return None


def process_cwd(pid):
    try:
        return os.readlink(f"/proc/{pid}/cwd")
    except OSError:
        return None


def process_cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as handle:
            raw = handle.read()
    except OSError:
        return None
    parts = [part.decode("utf-8", "replace") for part in raw.split(b"\0") if part]
    return parts or None


def live_processes():
    """Every readable pid on this machine as `(pid, argv)`. `/proc` only — no `ps` to parse."""
    found = []
    try:
        entries = sorted(int(name) for name in os.listdir("/proc") if name.isdigit())
    except OSError:
        return found
    for pid in entries:
        argv = process_cmdline(pid)
        if argv:
            found.append((pid, argv))
    return found


def describe(pid, argv):
    ticks = cpu_ticks(pid)
    return {
        "pid": pid,
        "argv": " ".join(argv),
        "cwd": process_cwd(pid),
        "cpu-ticks": ticks,
        "cpu-seconds": None if ticks is None else round(ticks / CLOCK_TICKS, 1),
    }


def driver_processes(iterations, processes=None, self_pid=None):
    """Driver processes for the named iterations.

    Matched on `run_iteration` / `run-iteration`, or on `iteration-<id>` for an id asked about.
    Excluded: anything under a scratchpad, this tool and its watch sibling, and our own pid —
    all three would otherwise match on argv alone and report a dead run as alive.
    """
    if processes is None:
        processes = live_processes()
    if self_pid is None:
        self_pid = os.getpid()
    wanted = ["run_iteration", "run-iteration"] + [str(name) for name in iterations]
    found = []
    for pid, argv in processes:
        if pid == self_pid:
            continue
        line = " ".join(argv)
        if any(marker in line for marker in NOT_A_DRIVER):
            continue
        hit = next((marker for marker in wanted if marker in line), None)
        if hit is None:
            continue
        record = describe(pid, argv)
        record["matched"] = hit
        found.append(record)
    return found


def transcript_dir(project_path, home=None):
    """Where `claude` keeps a project's transcripts: the path with every `/` turned into `-`."""
    root = os.path.join(home or os.path.expanduser("~"), ".claude", "projects")
    return os.path.join(root, project_path.replace("/", "-"))


def newest_transcript(project_path, home=None):
    """`(path, mtime, error)` for the most recently written transcript of a project."""
    directory = transcript_dir(project_path, home=home)
    if not os.path.isdir(directory):
        return None, None, f"no transcript directory at {directory}"
    newest, stamp = None, None
    for name in os.listdir(directory):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(directory, name)
        try:
            when = os.path.getmtime(path)
        except OSError:
            continue
        if stamp is None or when > stamp:
            newest, stamp = path, when
    if newest is None:
        return None, None, f"transcript directory holds no .jsonl: {directory}"
    return newest, stamp, None


def builder_processes(repo, pid_file=None, processes=None, self_pid=None):
    """`(records, notes)` for the builder session working in `repo`.

    Two independent ways to find it, both reported: a pid file if one was left, and any process
    whose working directory is the repository or below it. Neither is authoritative — a pid file
    can name a process that died, and a cwd match can catch a shell — so the evidence carries the
    CPU ticks and the argv and lets the reader disagree.
    """
    if processes is None:
        processes = live_processes()
    if self_pid is None:
        self_pid = os.getpid()
    notes = []
    found = {}
    if pid_file:
        if not os.path.isfile(pid_file):
            notes.append(f"pid file absent: {pid_file}")
        else:
            try:
                with open(pid_file, "r", encoding="utf-8") as handle:
                    pid = int(handle.read().strip())
            except (OSError, ValueError) as error:
                notes.append(f"pid file unreadable ({type(error).__name__}: {error}): {pid_file}")
            else:
                argv = process_cmdline(pid)
                if argv is None:
                    notes.append(f"pid file names {pid}, which is not running: {pid_file}")
                else:
                    record = describe(pid, argv)
                    record["found-by"] = f"pid-file {pid_file}"
                    found[pid] = record
    root = os.path.realpath(repo)
    for pid, argv in processes:
        if pid == self_pid or pid in found:
            continue
        line = " ".join(argv)
        if any(marker in line for marker in NOT_A_DRIVER):
            continue
        if "claude" not in os.path.basename(argv[0]) and "claude" not in line:
            continue
        cwd = process_cwd(pid)
        if not cwd:
            continue
        real = os.path.realpath(cwd)
        if real != root and not real.startswith(root + os.sep):
            continue
        record = describe(pid, argv)
        record["found-by"] = "cwd match"
        found[pid] = record
    return [found[pid] for pid in sorted(found)], notes


# ---------------------------------------------------------------------------------------------
# file activity


def find_binary(which=shutil.which, run=subprocess.run):
    """`(path, version, error)` for the `find` a subprocess will actually get.

    The conventions say `find` here is `bfs`. That is true of an interactive shell, where `find`
    is a function; it is not true of a subprocess, which gets whatever is on PATH. So the
    version line goes in the report and the reader can see which one answered.
    """
    path = which("find")
    if path is None:
        return None, None, "no `find` on PATH"
    try:
        done = run([path, "--version"], capture_output=True, text=True)
    except OSError as error:
        return path, None, f"{type(error).__name__}: {error}"
    first = (done.stdout or done.stderr or "").split("\n")[0].strip()
    return path, first or None, None


def activity_stamp(when, minutes):
    """The absolute `-newermt` argument. Relative forms fail on this machine."""
    moment = datetime.datetime.fromtimestamp(when - minutes * 60)
    return moment.strftime("%Y-%m-%d %H:%M:%S")


def file_activity(path, minutes, when, binary=None, run=subprocess.run, limit=8):
    """Files under `path` modified inside the window.

    stderr is captured and returned, never discarded: an empty result from a `find` that errored
    is not an idle directory, and the two have been confused here before.
    """
    record = {"path": path, "minutes": minutes, "stamp": activity_stamp(when, minutes),
              "files": [], "count": 0, "stderr": "", "returncode": None, "argv": None,
              "error": None}
    if binary is None:
        binary, _, error = find_binary()
        if binary is None:
            record["error"] = error
            return record
    if not os.path.isdir(path):
        record["error"] = f"no directory at {path}"
        return record
    argv = [binary, path, "-name", ".git", "-prune", "-o",
            "-type", "f", "-newermt", record["stamp"], "-print"]
    record["argv"] = shlex.join(argv)
    try:
        done = run(argv, capture_output=True, text=True)
    except OSError as error:
        record["error"] = f"{type(error).__name__}: {error}"
        return record
    record["returncode"] = done.returncode
    record["stderr"] = (done.stderr or "").strip()
    files = [line for line in (done.stdout or "").split("\n") if line.strip()]
    record["count"] = len(files)
    record["files"] = files[:limit]
    return record


# ---------------------------------------------------------------------------------------------
# classification


def classify_run(record, driver_count, activity_count):
    """`(code, name, why)` for one iteration. The `why` is the table row that fired."""
    if record["error"]:
        return 3, "stalled-candidate", f"the run state could not be read — {record['error']}"
    status = record["status"]
    if status in TERMINAL_STATUSES:
        reason = record["stop-reason"] or "(none recorded)"
        return 1, "stopped-with-reason", f"status {status!r}, stop-reason {reason}"
    if driver_count == 0:
        return 2, "process-dead-state-running", (
            f"status {status!r} and no driver process matches this iteration")
    if activity_count == 0:
        return 3, "stalled-candidate", (
            f"status {status!r}, {driver_count} process(es), and nothing changed in the window")
    return 0, "progressing", (
        f"status {status!r}, {driver_count} process(es), {activity_count} file(s) in the window")


def classify_builder(count, transcript_age_minutes, window_minutes):
    """`(code, name, why)` for the builder session."""
    if count:
        return 0, "progressing", f"{count} builder process(es) alive"
    if transcript_age_minutes is not None and transcript_age_minutes <= window_minutes:
        return 2, "process-dead-state-running", (
            f"no builder process, but its transcript was written "
            f"{transcript_age_minutes:.1f} min ago — inside the {window_minutes} min window")
    if transcript_age_minutes is None:
        return 3, "stalled-candidate", "no builder process and no transcript to date it by"
    return 3, "stalled-candidate", (
        f"no builder process; the newest transcript is {transcript_age_minutes:.1f} min old")


def worst(codes):
    for code in SEVERITY:
        if code in codes:
            return code
    return 0


# ---------------------------------------------------------------------------------------------
# reporting


def flat(value):
    """One line, always. A machine block whose values can wrap is not machine-parseable."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    return text.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace(
        "\t", "\\t")


class Report:
    """The two blocks. Machine lines are collected as they are learned and printed first."""

    def __init__(self):
        self.machine = []
        self.human = []

    def pair(self, key, value):
        self.machine.append(f"{key}={flat(value)}")

    def say(self, line=""):
        self.human.append(line)

    def render(self):
        return "\n".join(["# machine"] + self.machine + ["", "# human"] + self.human)


def build_report(args, now, repo=REPO, harness=HARNESS, home=None):
    """Everything the probe knows, as a `(Report, exit_code)` pair. Nothing is printed here."""
    report = Report()
    codes = []

    sha, sha_error = head_sha(repo)
    report.pair("head.sha", sha or "")
    if sha_error:
        report.pair("head.error", sha_error)
    unit, unit_path, _ = read_checkpoint(repo)
    report.pair("checkpoint.path", unit_path)
    report.pair("checkpoint.current-unit", unit["unit"] or "")
    report.pair("checkpoint.current-unit-number", "" if unit["number"] is None else unit["number"])
    report.pair("checkpoint.section", unit["heading"] or "")
    if unit["error"]:
        report.pair("checkpoint.error", unit["error"])

    report.say(f"head              {sha or '(unknown)'}"
               + (f"   [{sha_error}]" if sha_error else ""))
    if unit["unit"]:
        report.say(f"current unit      {unit['unit']}   (from {unit['heading']!r}, "
                   f"{os.path.relpath(unit_path, repo)})")
    else:
        report.say(f"current unit      (none) — {unit['error']}")
    report.say()

    processes = live_processes()
    binary, version, binary_error = find_binary()
    report.pair("find.binary", binary or "")
    report.pair("find.version", version or "")
    if binary_error:
        report.pair("find.error", binary_error)
    report.say(f"find              {binary or '(none)'}   {version or ''}"
               + (f"   [{binary_error}]" if binary_error else ""))
    report.say(f"activity window   {args.window_minutes} min "
               f"(-newermt {activity_stamp(now, args.window_minutes)!r})")
    report.say()

    for iteration in args.iteration:
        record = run_record(harness, iteration)
        key = f"run.{iteration}"
        report.pair(f"{key}.run-dir", record["run-dir"])
        report.pair(f"{key}.status", record["status"] or "")
        report.pair(f"{key}.stop-reason", record["stop-reason"] or "")
        report.pair(f"{key}.turn", "" if record["turn"] is None else record["turn"])
        report.pair(f"{key}.project", record["project"] or "")
        report.pair(f"{key}.terminal", "" if record["terminal"] is None else record["terminal"])
        if record["error"]:
            report.pair(f"{key}.error", record["error"])

        report.say(f"--- {iteration} ---")
        if record["error"]:
            report.say(f"  state           UNREADABLE — {record['error']}")
        else:
            report.say(f"  status          {record['status']}")
            report.say(f"  stop-reason     {record['stop-reason'] or '(none)'}")
            report.say(f"  turn            {record['turn']}")
            report.say(f"  run dir         {record['run-dir']}")

        drivers = driver_processes([iteration], processes=processes)
        report.pair(f"{key}.drivers", len(drivers))
        if drivers:
            for index, driver in enumerate(drivers):
                report.pair(f"{key}.driver.{index}.pid", driver["pid"])
                report.pair(f"{key}.driver.{index}.cpu-seconds", driver["cpu-seconds"])
                report.pair(f"{key}.driver.{index}.argv", driver["argv"])
                report.say(f"  driver          pid {driver['pid']} "
                           f"cpu {driver['cpu-seconds']}s  matched {driver['matched']!r}")
                report.say(f"                  cwd  {driver['cwd']}")
                report.say(f"                  argv {driver['argv']}")
        else:
            report.say("  driver          no process matches "
                       f"run_iteration or {iteration!r} (scratchpads and this tool excluded)")

        activity = file_activity(record["run-dir"], args.window_minutes, now, binary=binary)
        report.pair(f"{key}.activity.count", activity["count"])
        report.pair(f"{key}.activity.stamp", activity["stamp"])
        if activity["error"]:
            report.pair(f"{key}.activity.error", activity["error"])
        if activity["stderr"]:
            report.pair(f"{key}.activity.stderr", activity["stderr"])
        report.say(f"  activity        {activity['count']} file(s) under the run dir newer than "
                   f"{activity['stamp']}")
        if activity["argv"]:
            report.say(f"                  $ {activity['argv']}")
        for name in activity["files"]:
            report.say(f"                  · {name}")
        if activity["error"]:
            report.say(f"                  ! {activity['error']}")
        if activity["stderr"]:
            for line in activity["stderr"].split("\n"):
                report.say(f"                  ! stderr: {line}")

        board, board_error = board_summary(record["project"])
        if board:
            report.pair(f"{key}.board.path", board["path"])
            report.pair(f"{key}.board.summary", " | ".join(
                line.strip("- ").strip() for line in board["lines"]))
            report.say(f"  board           {board['path']}")
            for line in board["lines"]:
                report.say(f"                  {line}")
        else:
            report.pair(f"{key}.board.error", board_error)
            report.say(f"  board           (none) — {board_error}")

        code, name, why = classify_run(record, len(drivers), activity["count"])
        codes.append(code)
        report.pair(f"{key}.classification", code)
        report.pair(f"{key}.classification.name", name)
        report.pair(f"{key}.classification.why", why)
        report.say(f"  classification  {code} {name} — {why}")
        report.say()

    if args.builder:
        builders, notes = builder_processes(repo, pid_file=args.builder_pid_file,
                                            processes=processes)
        report.pair("builder.count", len(builders))
        report.say("--- builder ---")
        report.say(f"  repo            {repo}")
        for note in notes:
            report.pair("builder.note", note)
            report.say(f"  pid file        {note}")
        for index, builder in enumerate(builders):
            report.pair(f"builder.{index}.pid", builder["pid"])
            report.pair(f"builder.{index}.cpu-seconds", builder["cpu-seconds"])
            report.pair(f"builder.{index}.found-by", builder["found-by"])
            report.pair(f"builder.{index}.argv", builder["argv"])
            report.say(f"  process         pid {builder['pid']} cpu {builder['cpu-seconds']}s "
                       f"({builder['found-by']})")
            report.say(f"                  cwd  {builder['cwd']}")
            report.say(f"                  argv {builder['argv']}")
        if not builders:
            report.say("  process         none found by pid file or cwd match")

        path, stamp, transcript_error = newest_transcript(repo, home=home)
        age = None if stamp is None else (now - stamp) / 60.0
        report.pair("builder.transcript", path or "")
        report.pair("builder.transcript.age-minutes", "" if age is None else round(age, 1))
        if transcript_error:
            report.pair("builder.transcript.error", transcript_error)
            report.say(f"  transcript      (none) — {transcript_error}")
        else:
            report.say(f"  transcript      {path}")
            report.say(f"                  mtime {datetime.datetime.fromtimestamp(stamp)} "
                       f"({age:.1f} min ago)")

        code, name, why = classify_builder(len(builders), age, args.window_minutes)
        codes.append(code)
        report.pair("builder.classification", code)
        report.pair("builder.classification.name", name)
        report.pair("builder.classification.why", why)
        report.say(f"  classification  {code} {name} — {why}")
        report.say()

    overall = worst(codes)
    report.pair("classification", overall)
    report.pair("classification.name",
                next(name for name, code, _ in DECISION_TABLE if code == overall))
    report.say("--- decision table applied ---")
    for name, code, rule in DECISION_TABLE:
        mark = "*" if code == overall else " "
        report.say(f" {mark} {code}  {name:<28} {rule}")
    report.say("   worst-wins order across subjects: 2 > 3 > 1 > 0")
    report.say()
    report.say("The exit code is a hint. The evidence above is the report, and the verdict "
               "is the session's to write.")
    return report, overall


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="harness/ops/status.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="One-shot ops status: run state, head and current unit, process liveness, "
                    "file activity and board summary, as evidence lines.",
        epilog="Exit codes (a hint; the evidence lines are the report, and they print under "
               "every code):\n"
               "  0  progressing                   running, owned by a process, files moved\n"
               "  1  stopped-with-reason           terminal, and the reason is recorded\n"
               "  2  process-dead-state-running    state.json says running, nothing owns it\n"
               "  3  stalled-candidate             running but idle, or the state is unreadable\n"
               "With several subjects the worst code wins: 2 > 3 > 1 > 0.\n\n"
               "The current unit is read from the checkpoint's `## Current unit` section only. "
               "A whole-file scan for META-### answers confidently and wrongly, because the "
               "checkpoint also declares the session's range.\n\n"
               "Judgment stays with the session: verdict prose, deviation flags and retraction "
               "on contradiction are not this tool's output (meta/OPS-CONVENTIONS.md).")
    parser.add_argument("--iteration", action="append", default=[], metavar="ID",
                        help="an iteration to report on; repeatable")
    parser.add_argument("--builder", action="store_true",
                        help="also report the builder session working in this repository")
    parser.add_argument("--builder-pid-file", metavar="PATH",
                        default=os.path.join(REPO, "meta", ".builder.pid"),
                        help="pid file to consult for the builder (default: %(default)s); "
                             "its absence is reported, not assumed")
    parser.add_argument("--window-minutes", type=int, default=20, metavar="N",
                        help="the file-activity window, in minutes (default: %(default)s)")
    args = parser.parse_args(argv)
    if not args.iteration and not args.builder:
        parser.error("nothing to report on: pass --iteration <id> and/or --builder")
    return args


def main(argv=None):
    import time
    args = parse_args(argv)
    report, code = build_report(args, time.time())
    print(report.render())
    return code


if __name__ == "__main__":
    sys.exit(main())
