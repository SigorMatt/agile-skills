#!/usr/bin/env python3
"""The single-report watch. Run: harness/ops/watch.py --iteration <id> --on-stop

One report per invocation, on a terminal trigger or on the timeout — never a running
commentary. The rules from `meta/OPS-CONVENTIONS.md` are the design, not a checklist beside it:

* **The baseline is taken at arm time and printed at arm time.** A watch that reports a change
  without saying what it was measuring against has reported nothing checkable.
* **Anything already terminal at arm is history.** A run that stopped before the watch started
  is announced as skipped and its stop trigger is never armed, so it cannot fire. A run
  directory that was terminal at arm produces an event only if it comes back to life — which is
  what `--fresh` reusing the same path looks like from outside.
* **A parse failure never updates a baseline.** Folding 'unknown' into the baseline destroys the
  comparison the watch exists to make, so a failed read keeps both the baseline and the last
  observation that actually parsed.
* **A probe error is not silence.** It is printed the moment it happens (to stderr, so the one
  report on stdout stays one report) and it is carried verbatim into the report.
* **Every trigger emits its evidence verbatim** — the lines that made it fire, not a summary
  of them.

Trigger dispositions, because they are the difference between a watch that ends and one that
keeps looking:

    --on-stop             terminal    the run went terminal; that is the thing being waited for
    --on-file-complete    terminal    the file exists and no longer says Pending
    --on-unit-gte N       terminal    the checkpoint's current unit reached N
    --on-new-rundir       note        a run STARTED; starting is not finishing, so the watch
                                      notes it with its evidence and keeps watching

Exit codes: 0 when a terminal trigger fired, 3 when the timeout was reached with none — the
same stalled-candidate vocabulary `status.py` uses. Either way the report is written exactly
once.

Judgment stays with the session. This prints observations and which rule they matched; the
verdict prose, the deviation flags and any retraction are the session's to write.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ops import status  # noqa: E402

HARNESS = status.HARNESS
REPO = status.REPO

# A deliverable that still says Pending is a file being written, not a finished one — the same
# shape as the conventions' rule that a half-written frontmatter block is not a question. The
# emphasis markers are optional and the case is ignored, so `*Pending*`, `**PENDING**` and a
# bare `Pending` on its own all count as unfinished.
PENDING = re.compile(r"(^|[^A-Za-z])\*{0,2}pending\*{0,2}([^A-Za-z]|$)", re.IGNORECASE)


def stamp(when):
    return datetime.datetime.fromtimestamp(when).strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------------------------
# the baseline and what may update it


class Tracker:
    """Arm-time baselines, plus the last observation per subject that actually parsed.

    `observe` is where the parse-failure rule lives: a failed read returns `kept`, leaves both
    the baseline and the last good value alone, and hands back the error for the report. The
    alternative — storing the failure — makes every later comparison run against 'unknown', so
    the watch quietly loses the ability to see the change it was armed for.
    """

    def __init__(self):
        self.baseline = {}
        self.current = {}

    def arm(self, subject, ok, value, error=None):
        record = {"ok": bool(ok), "value": value, "error": error}
        self.baseline[subject] = record
        if ok:
            self.current[subject] = value
        return record

    def observe(self, subject, ok, value, error=None):
        previous = self.current.get(subject)
        if not ok:
            return {"subject": subject, "ok": False, "kept": True, "changed": False,
                    "value": previous, "previous": previous, "error": error}
        changed = subject in self.current and previous != value
        self.current[subject] = value
        return {"subject": subject, "ok": True, "kept": False, "changed": changed,
                "value": value, "previous": previous, "error": None}


def observe_run(harness, iteration):
    """`(ok, value, error)` for one run's state. The value is what a trigger compares."""
    record = status.run_record(harness, iteration)
    if record["error"]:
        return False, None, record["error"]
    return True, {"status": record["status"], "stop-reason": record["stop-reason"],
                  "turn": record["turn"], "terminal": record["terminal"]}, None


def observe_rundirs(harness):
    """`(ok, {name: {...}}, error)` for every run directory under `harness/runs`."""
    root = os.path.join(harness, "runs")
    if not os.path.isdir(root):
        return False, None, f"no runs directory at {root}"
    observed = {}
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            continue
        state, error = status.read_state(path)
        if state is None:
            observed[name] = {"status": None, "terminal": None, "started": None, "error": error}
            continue
        observed[name] = {"status": state.get("status"),
                          "terminal": state.get("status") in status.TERMINAL_STATUSES,
                          "started": state.get("started"), "error": None}
    return True, observed, None


def observe_file(path):
    """`(ok, {...}, error)` for a `--on-file-complete` target.

    A missing file is a legitimate observation, not a probe error: it is the normal state before
    the work is done. An unreadable file IS a probe error — the difference is the whole point of
    the rule that a command returning nothing is not evidence until its error is known.
    """
    if not os.path.isfile(path):
        return True, {"exists": False, "pending": None, "complete": False}, None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError as error:
        return False, None, f"{type(error).__name__}: {error}: {path}"
    pending = PENDING.search(text) is not None
    return True, {"exists": True, "pending": pending, "complete": not pending}, None


def observe_unit(repo):
    """`(ok, {...}, error)` for the checkpoint's current unit.

    A checkpoint with no `## Current unit` section is a parse failure for this purpose: the
    watch cannot tell 'the section is gone' from 'the unit has not been written yet', so it
    keeps the previous observation rather than inventing a number from the rest of the file.
    """
    record, path, _ = status.read_checkpoint(repo)
    if record["unit"] is None:
        return False, None, f"{record['error']} ({path})"
    return True, {"unit": record["unit"], "number": record["number"],
                  "heading": record["heading"]}, None


def new_rundir_events(baseline, observed):
    """`(events, probe_errors)` — a run directory that is new, or one that came back to life.

    Terminal-at-arm directories are history. Their mere presence is never an event; they become
    one only by going non-terminal again, which is what `--fresh` reusing the same path looks
    like from outside. A directory whose state cannot be read yields a probe error and no
    event — a run that is mid-write must not be announced as a new run.
    """
    events, errors = [], []
    for name in sorted(observed):
        now = observed[name]
        if now["error"]:
            errors.append(f"{name}: {now['error']}")
            continue
        was = baseline.get(name)
        if was is None:
            events.append({"name": name,
                           "evidence": f"{name}: absent at arm; now status "
                                       f"{now['status']!r}, started {now['started']}"})
            continue
        if was.get("error"):
            continue
        if was["terminal"] and now["terminal"] is False:
            events.append({"name": name,
                           "evidence": f"{name}: terminal at arm ({was['status']!r}) and now "
                                       f"{now['status']!r} — the path was reused"})
            continue
        if was["started"] and now["started"] and was["started"] != now["started"]:
            events.append({"name": name,
                           "evidence": f"{name}: started {was['started']} at arm, now "
                                       f"{now['started']} — a different run in the same path"})
    return events, errors


# ---------------------------------------------------------------------------------------------
# triggers


def arm_triggers(args, tracker, harness, repo):
    """`(armed, skipped, baseline_lines)`. Nothing already satisfied at arm is ever armed."""
    armed, skipped, lines = [], [], []

    for iteration in args.iteration:
        ok, value, error = observe_run(harness, iteration)
        tracker.arm(f"run:{iteration}", ok, value, error)
        if not ok:
            lines.append(f"  run {iteration}: UNREADABLE — {error}")
            if args.on_stop:
                armed.append({"kind": "stop", "subject": iteration, "terminal": True})
            continue
        lines.append(f"  run {iteration}: status={value['status']!r} "
                     f"stop-reason={value['stop-reason']!r} turn={value['turn']}")
        if not args.on_stop:
            continue
        if value["terminal"]:
            skipped.append(f"--on-stop {iteration}: terminal at arm "
                           f"(status {value['status']!r}, stop-reason "
                           f"{value['stop-reason']!r}) — history, not an event")
        else:
            armed.append({"kind": "stop", "subject": iteration, "terminal": True})

    if args.on_new_rundir:
        ok, value, error = observe_rundirs(harness)
        tracker.arm("rundirs", ok, value, error)
        if not ok:
            lines.append(f"  run directories: UNREADABLE — {error}")
            armed.append({"kind": "new-rundir", "subject": "runs", "terminal": False})
        else:
            live = [name for name, item in value.items() if item["terminal"] is False]
            terminal = [name for name, item in value.items() if item["terminal"]]
            unreadable = [name for name, item in value.items() if item["error"]]
            lines.append(f"  run directories: {len(value)} at arm "
                         f"({len(terminal)} terminal, {len(live)} live, "
                         f"{len(unreadable)} unreadable)")
            for name in sorted(value):
                item = value[name]
                mark = "terminal" if item["terminal"] else (
                    "unreadable" if item["error"] else "live")
                lines.append(f"    · {name}: {mark} ({item['status']!r})")
            if terminal:
                skipped.append(f"--on-new-rundir: {len(terminal)} directory(ies) terminal at "
                               f"arm are history and cannot fire by existing: "
                               f"{', '.join(sorted(terminal))}")
            armed.append({"kind": "new-rundir", "subject": "runs", "terminal": False})

    for path in args.on_file_complete:
        ok, value, error = observe_file(path)
        tracker.arm(f"file:{path}", ok, value, error)
        if not ok:
            lines.append(f"  file {path}: UNREADABLE — {error}")
            armed.append({"kind": "file-complete", "subject": path, "terminal": True})
            continue
        lines.append(f"  file {path}: exists={value['exists']} pending={value['pending']}")
        if value["complete"]:
            skipped.append(f"--on-file-complete {path}: already complete at arm "
                           "(exists, says nothing pending) — history, not an event")
        else:
            armed.append({"kind": "file-complete", "subject": path, "terminal": True})

    if args.on_unit_gte is not None:
        ok, value, error = observe_unit(repo)
        tracker.arm("unit", ok, value, error)
        if not ok:
            lines.append(f"  current unit: UNREADABLE — {error}")
            armed.append({"kind": "unit-gte", "subject": args.on_unit_gte, "terminal": True})
        else:
            lines.append(f"  current unit: {value['unit']} (from {value['heading']!r})")
            if value["number"] >= args.on_unit_gte:
                skipped.append(f"--on-unit-gte {args.on_unit_gte}: already satisfied at arm "
                               f"({value['unit']}) — history, not an event")
            else:
                armed.append({"kind": "unit-gte", "subject": args.on_unit_gte, "terminal": True})

    if args.builder:
        builders, notes = status.builder_processes(repo, pid_file=args.builder_pid_file)
        lines.append(f"  builder: {len(builders)} process(es) in {repo}")
        for note in notes:
            lines.append(f"    · {note}")
        for builder in builders:
            lines.append(f"    · pid {builder['pid']} cpu {builder['cpu-seconds']}s "
                         f"({builder['found-by']}) {builder['argv']}")
        tracker.arm("builder", True, {"count": len(builders)}, None)

    return armed, skipped, lines


def poll_trigger(trigger, tracker, harness, repo):
    """`(fired, evidence_lines, probe_errors)` for one armed trigger."""
    kind = trigger["kind"]

    if kind == "stop":
        iteration = trigger["subject"]
        ok, value, error = observe_run(harness, iteration)
        tracker.observe(f"run:{iteration}", ok, value, error)
        if not ok:
            return False, [], [f"run {iteration}: {error}"]
        if value["terminal"]:
            return True, [f"run {iteration} went terminal: status={value['status']!r} "
                          f"stop-reason={value['stop-reason']!r} turn={value['turn']}",
                          f"  at arm: {tracker.baseline[f'run:{iteration}']['value']}"], []
        return False, [], []

    if kind == "new-rundir":
        ok, value, error = observe_rundirs(harness)
        if not ok:
            return False, [], [f"run directories: {error}"]
        base = tracker.baseline.get("rundirs", {})
        baseline_value = base.get("value") or {}
        events, errors = new_rundir_events(baseline_value, value)
        fresh = [event for event in events if event["name"] not in trigger.setdefault("seen", [])]
        for event in fresh:
            trigger["seen"].append(event["name"])
        return bool(fresh), [event["evidence"] for event in fresh], errors

    if kind == "file-complete":
        path = trigger["subject"]
        ok, value, error = observe_file(path)
        tracker.observe(f"file:{path}", ok, value, error)
        if not ok:
            return False, [], [f"file {path}: {error}"]
        if value["complete"]:
            return True, [f"{path}: exists and says nothing pending",
                          f"  at arm: {tracker.baseline[f'file:{path}']['value']}"], []
        return False, [], []

    if kind == "unit-gte":
        threshold = trigger["subject"]
        ok, value, error = observe_unit(repo)
        tracker.observe("unit", ok, value, error)
        if not ok:
            return False, [], [f"current unit: {error}"]
        if value["number"] >= threshold:
            return True, [f"current unit {value['unit']} >= META-{threshold} "
                          f"(from {value['heading']!r})",
                          f"  at arm: {tracker.baseline['unit']['value']}"], []
        return False, [], []

    return False, [], [f"unknown trigger kind {kind!r}"]


# ---------------------------------------------------------------------------------------------
# the loop


def run_watch(args, out=sys.stdout, err=sys.stderr, clock=time.time, sleeper=time.sleep,
              harness=None, repo=None):
    harness = harness or HARNESS
    repo = repo or REPO
    started = clock()
    timeout = args.timeout_hours * 3600.0
    poll = args.poll_minutes * 60.0
    tracker = Tracker()

    header = [
        "# watch armed",
        f"armed at        {stamp(started)}",
        f"poll            every {args.poll_minutes} min",
        f"timeout         {args.timeout_hours} h (at {stamp(started + timeout)})",
        "baseline at arm:",
    ]
    armed, skipped, baseline_lines = arm_triggers(args, tracker, harness, repo)
    header.extend(baseline_lines)
    if skipped:
        header.append("skipped (already terminal or already satisfied at arm):")
        header.extend(f"  · {line}" for line in skipped)
    header.append("armed triggers:")
    if armed:
        for trigger in armed:
            disposition = "terminal" if trigger["terminal"] else "note-and-continue"
            header.append(f"  · {trigger['kind']} {trigger['subject']} ({disposition})")
    else:
        header.append("  · none — every requested trigger was satisfied at arm; "
                      "this watch can only time out")
    print("\n".join(header), file=out, flush=True)

    notes = []
    fired = None
    polls = 0
    while True:
        elapsed = clock() - started
        if elapsed >= timeout:
            break
        remaining = timeout - elapsed
        sleeper(min(poll, remaining))
        polls += 1
        now = clock()
        for trigger in list(armed):
            hit, evidence, errors = poll_trigger(trigger, tracker, harness, repo)
            for error in errors:
                line = f"[{stamp(now)}] probe error — {error}"
                notes.append(line)
                print(line, file=err, flush=True)
            if not hit:
                continue
            if trigger["terminal"]:
                fired = {"trigger": trigger, "evidence": evidence, "at": now}
                break
            line = f"[{stamp(now)}] note — {trigger['kind']} {trigger['subject']}"
            notes.append(line)
            print(line, file=err, flush=True)
            for item in evidence:
                notes.append(f"    {item}")
                print(f"    {item}", file=err, flush=True)
        if fired:
            break
        if clock() - started >= timeout:
            break

    ended = clock()
    elapsed = ended - started
    report = ["", "# watch report (one per invocation)",
              f"armed at        {stamp(started)}",
              f"ended at        {stamp(ended)}",
              f"timeout         {args.timeout_hours} h ({timeout / 3600:.2f} h)",
              f"elapsed         {elapsed / 3600:.2f} h ({elapsed / 60:.1f} min)",
              f"polls           {polls}",
              "baseline at arm:"]
    report.extend(baseline_lines)
    if skipped:
        report.append("skipped at arm:")
        report.extend(f"  · {line}" for line in skipped)
    if notes:
        report.append("notes and probe errors, in order:")
        report.extend(f"  {line}" for line in notes)
    else:
        report.append("notes and probe errors: none")
    if fired:
        trigger = fired["trigger"]
        report.append(f"TRIGGER         {trigger['kind']} {trigger['subject']} "
                      f"at {stamp(fired['at'])}")
        report.append("evidence, verbatim:")
        report.extend(f"  {line}" for line in fired["evidence"])
        code = 0
    else:
        report.append("TRIGGER         none — the timeout was reached")
        code = 3
    report.append("")
    report.append("Mechanics only: the verdict is the session's to write "
                  "(meta/OPS-CONVENTIONS.md).")
    text = "\n".join(report)
    print(text, file=out, flush=True)
    if args.report_file:
        with open(args.report_file, "w", encoding="utf-8") as handle:
            handle.write(text.lstrip("\n") + "\n")
        print(f"report written to {args.report_file}", file=out, flush=True)
    return code


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="harness/ops/watch.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Watch a harness run or a builder session and emit exactly one report, "
                    "on a terminal trigger or on the timeout.",
        epilog="Trigger dispositions:\n"
               "  --on-stop            terminal          the run went terminal\n"
               "  --on-file-complete   terminal          the file exists and says nothing "
               "pending\n"
               "  --on-unit-gte N      terminal          the checkpoint's current unit reached "
               "N\n"
               "  --on-new-rundir      note-and-continue a run STARTED; starting is not "
               "finishing\n\n"
               "Rules compiled in, from meta/OPS-CONVENTIONS.md:\n"
               "  · the baseline is taken at arm and printed at arm\n"
               "  · anything terminal or already satisfied at arm is announced as skipped and "
               "never armed\n"
               "  · a parse failure keeps the baseline AND the last good observation\n"
               "  · a probe error is printed to stderr when it happens and carried into the "
               "report; it is never read as silence\n"
               "  · every trigger emits its evidence verbatim\n\n"
               "Exit codes: 0 a terminal trigger fired; 3 the timeout was reached with none.\n"
               "The report is written exactly once, to stdout and to --report-file if given.\n\n"
               "Judgment stays with the session: verdict prose, deviation flags and retraction "
               "on contradiction are not this tool's output.")
    parser.add_argument("--poll-minutes", type=float, default=15, metavar="N",
                        help="minutes between polls (default: %(default)s)")
    parser.add_argument("--timeout-hours", type=float, default=6, metavar="H",
                        help="hours before the watch reports and gives up (default: %(default)s)")
    parser.add_argument("--iteration", action="append", default=[], metavar="ID",
                        help="an iteration to watch; repeatable")
    parser.add_argument("--builder", action="store_true",
                        help="record the builder session's processes in the arm baseline")
    parser.add_argument("--report-file", metavar="PATH",
                        help="also write the single report here")
    parser.add_argument("--builder-pid-file", metavar="PATH",
                        default=os.path.join(REPO, "meta", ".builder.pid"),
                        help="pid file to consult for the builder (default: %(default)s)")
    parser.add_argument("--on-stop", action="store_true",
                        help="terminal: fire when a watched run goes terminal")
    parser.add_argument("--on-file-complete", action="append", default=[], metavar="PATH",
                        help="terminal: fire when PATH exists and says nothing pending; "
                             "repeatable")
    parser.add_argument("--on-unit-gte", type=int, metavar="N",
                        help="terminal: fire when the checkpoint's Current-unit section names "
                             "META-N or higher")
    parser.add_argument("--on-new-rundir", action="store_true",
                        help="note-and-continue: note a run directory that is new since arm, or "
                             "one that was terminal at arm and came back to life")
    args = parser.parse_args(argv)
    if not (args.on_stop or args.on_file_complete or args.on_unit_gte is not None
            or args.on_new_rundir):
        parser.error("no trigger: pass at least one of --on-stop, --on-file-complete, "
                     "--on-unit-gte, --on-new-rundir")
    if args.on_stop and not args.iteration:
        parser.error("--on-stop needs at least one --iteration to watch")
    if args.poll_minutes <= 0 or args.timeout_hours <= 0:
        parser.error("--poll-minutes and --timeout-hours must both be positive")
    return args


def main(argv=None):
    return run_watch(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
