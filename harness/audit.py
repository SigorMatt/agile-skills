#!/usr/bin/env python3
"""The contamination boundary, enforced by observation.

`meta/harness/DESIGN.md` §4 states the boundary in one line each:

  - the worker must never read `harness/` — a worker that can see the probe script is studying
    the exam answers;
  - the sim touches only what a real human could — the board, the question files, its own log.

Enforcing that by good intentions is not enforcement. Every turn is run with
`--output-format stream-json`, which emits every `tool_use` block with its **full input**, so
this module can read what the session actually did and say whether it stayed inside its
boundary. `run_iteration.py` then adds a second, independent check on the project tree, so a
violation that reached disk through a channel the transcript did not describe is still caught.

Two rules of construction, both learned the hard way in this repository:

  - a check that cannot fail is not a check — `harness/tests/` feeds this module transcripts
    that must be rejected, and fails if they are accepted;
  - a violation is reported with the evidence that produced it (tool, input, matched token), so
    that a false positive can be recognised as one instead of being argued about.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import json
import os
import re

# Tokens that only harness content contains. A worker turn that names one of these has read, or
# is about to read, something it must not see. `HARNESS-STATUS.md` is deliberately absent: the
# worker writes that file itself, and `harness` as a bare word may legitimately appear in a
# journal entry describing the run's own conditions.
WORKER_FORBIDDEN_TOKENS = (
    "simulated-human",
    "probe-script",
    "PROJECT-QUEUE",
    "SIM-LOG",
    "run_iteration",
    "provision.py",
    "harness/prompts",
    "harness/skills",
    "harness/runs",
)

WRITE_TOOLS = ("Write", "Edit", "MultiEdit", "NotebookEdit")
PATH_KEYS = ("file_path", "path", "notebook_path", "filePath")

# Absolute paths appearing inside a Bash command string. Deliberately conservative: it matches
# home-rooted paths, which is where everything interesting on this machine lives, and ignores
# /usr, /bin, /tmp and friends. Markdown punctuation is excluded because a Bash command is very
# often a heredoc writing a *document*, and a backtick or a comma is where the path ends. The
# tilde form requires a following slash: a bare `~` is a separator (`tr '\n' '~'`) or markdown
# strikethrough far more often than it is a home directory, and both stopped a real run.
HOME_PATH_RE = re.compile(r"(?:~/|/home/)[^\s\"'`,<>;:|)&]+")


def plausible(path, source):
    """Could this path be read or written at all?

    A string that looks like a path but names nothing cannot leak anything — it is prose. The
    distinction is not pedantry: the first real worker turn wrote a question whose `## Context`
    quoted the stakeholder's own example folders (`~/trips/ski`, `~/flat`), and a rule without
    this filter stopped the run for contamination over a sentence. A check that fires on quoted
    text gets switched off, and then it checks nothing.

    The two sources are treated differently, because the evidence differs:

    - `key`  — the path is a tool's `file_path` argument. The session named it as a path and
               meant it; a write to a file that does not exist yet is still a write, so the
               parent existing is enough.
    - `bash` — the path was scraped out of a command string, which is as likely to be a heredoc
               writing a document as a command reading a file. Require the path itself to exist.
    """
    if source == "bash":
        return os.path.exists(path)
    return os.path.exists(path) or os.path.exists(os.path.dirname(path) or "/")


def load_transcript(path):
    """Every JSON event in a stream-json transcript, skipping unparseable lines."""
    events = []
    if not os.path.isfile(path):
        return events
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
    return events


def tool_uses(events):
    """[(tool_name, input_dict)] in order, main session and subagents alike."""
    uses = []
    for event in events:
        if event.get("type") != "assistant":
            continue
        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                uses.append((block.get("name") or "?", block.get("input") or {}))
    return uses


def result_event(events):
    for event in reversed(events):
        if event.get("type") == "result":
            return event
    return None


def _blob(tool_input):
    try:
        return json.dumps(tool_input, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(tool_input)


TRAILING = "\\.,;:)]}'\"`*_"


# A heredoc introducer: `<<WORD`, `<<'WORD'`, `<<"WORD"`, `<<-WORD`. `<<<` is a here-string and
# is deliberately excluded, and the introducer must end the word cleanly — otherwise `echo "a <<
# b"` would be read as opening a heredoc and swallow the rest of the command.
HEREDOC_RE = re.compile(r"<<(-?)\s*(?:'([^']*)'|\"([^\"]*)\"|([A-Za-z_][A-Za-z0-9_]*))"
                        r"(?=$|[\s>|&;])")


def strip_heredoc_bodies(command):
    """A Bash command string with the *contents* of its heredocs removed.

    A heredoc body is a document, not a command. `python3 - <<'PYEOF'` writing a bug report is
    the ordinary way a worker turn produces a file, and the report can perfectly well contain a
    sentence with a path in it — turn 6 of iteration 2 wrote *"anything scripting the tool —
    `tidy ~/Downloads --apply` — silently treats a completely successful run as a failure"*, and
    W3 scraped `~/Downloads` out of the command string and stopped the run (H-009).

    This is the same principle as `plausible()`'s prose filter, one step further in. That filter
    separates a document from a command by asking whether the path exists; here the path was
    real, so existence could not tell them apart. The structure can: everything between an
    introducer and its delimiter was being *written*, not reached for.

    Only the body is removed. The line carrying the introducer keeps its own paths — `cd`,
    redirect targets, the interpreter's arguments — because those are commands.

    **What this gives up, plainly.** A heredoc body may also be a program: `bash <<'EOF'` and
    `python3 - <<'PYEOF'` both execute what they are handed. A read of an outside path performed
    from inside one is no longer visible to this scrape. It was never reliably visible — a regex
    over a program's source cannot tell a string literal from an `open()` — and the alternative
    is a rule that fires on prose, which is a rule that gets switched off. W1 and W2 still read
    the whole input, so naming harness content inside a document is still caught, and
    `audit_repo_tree` still catches a write that reaches the toolkit repository by any route.
    """
    lines = command.split("\n")
    kept, index = [], 0
    while index < len(lines):
        line = lines[index]
        kept.append(line)
        index += 1
        delimiters = [(match.group(2) if match.group(2) is not None
                       else match.group(3) if match.group(3) is not None
                       else match.group(4), match.group(1) == "-")
                      for match in HEREDOC_RE.finditer(line)]
        for delimiter, strips_tabs in delimiters:
            while index < len(lines):
                body = lines[index]
                index += 1
                candidate = body.lstrip("\t") if strips_tabs else body
                if candidate.strip() == delimiter:
                    break
    return "\n".join(kept)


def _paths_in(tool_name, tool_input):
    """[(path, source)] this tool call names, as written. `source` is "key" or "bash"."""
    found = []
    for key in PATH_KEYS + ("pattern", "glob"):
        value = tool_input.get(key)
        if isinstance(value, str) and value and (key in PATH_KEYS
                                                 or value.startswith(("/", "~"))):
            found.append((value, "key"))
    if tool_name == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str):
            # Heredoc bodies are documents this command writes, not paths it reaches for
            # (H-009). The introducer line itself is kept and still scraped.
            found.extend((match.rstrip(TRAILING), "bash")
                         for match in HOME_PATH_RE.findall(strip_heredoc_bodies(command)))
    return [(path, source) for path, source in found if path]


def _resolve(path, cwd, home=None):
    """Absolute form of a path as the session would have meant it.

    `home` is a parameter rather than a call to `os.path.expanduser` so that the tests can audit
    a transcript from a machine that is not this one: `~` means the *audited* session's home.
    """
    expanded = path
    if expanded.startswith("~"):
        expanded = (home or os.path.expanduser("~")) + expanded[1:]
    if not os.path.isabs(expanded):
        expanded = os.path.join(cwd, expanded)
    return os.path.normpath(expanded)


def _inside(path, directory):
    directory = os.path.normpath(directory)
    return path == directory or path.startswith(directory + os.sep)


def violation(rule, tool, detail, evidence):
    return {"rule": rule, "tool": tool, "detail": detail,
            "evidence": evidence[:400]}


def audit_worker(uses, project_dir, harness_dir, repo_dir, home=None, exists=None):
    """Violations of "the worker never leaves the project".

    W1  named the harness directory or this repository by absolute path
    W2  named a token that only harness content contains
    W3  reached for a real path outside the project (excluding the agent's own ~/.claude state)

    `exists` is injectable so the tests can audit a transcript from a machine that is not this
    one; it defaults to `plausible`, which is what keeps W3 off quoted prose.
    """
    exists = exists or plausible
    project_dir = os.path.normpath(os.path.abspath(project_dir))
    harness_dir = os.path.normpath(os.path.abspath(harness_dir))
    repo_dir = os.path.normpath(os.path.abspath(repo_dir))
    home = os.path.normpath(home or os.path.expanduser("~"))
    tolerated = (os.path.join(home, ".claude"), os.path.join(home, ".cache"),
                 os.path.join(home, ".config"), os.path.join(home, ".local"))
    found = []
    for tool, tool_input in uses:
        blob = _blob(tool_input)
        for directory in (harness_dir, repo_dir):
            if directory in blob:
                found.append(violation(
                    "W1", tool, f"named {directory}, which is outside the project", blob))
                break
        lowered = blob.lower()
        for token in WORKER_FORBIDDEN_TOKENS:
            if token.lower() in lowered:
                found.append(violation(
                    "W2", tool, f"named {token!r}, which only harness content contains", blob))
                break
        for raw, source in _paths_in(tool, tool_input):
            resolved = _resolve(raw, project_dir, home)
            if _inside(resolved, project_dir):
                continue
            if not _inside(resolved, home):
                continue
            if any(_inside(resolved, allowed) for allowed in tolerated):
                continue
            if not exists(resolved, source):
                continue
            found.append(violation(
                "W3", tool, f"reached for {resolved}, which is outside the project", blob))
    return found


def sim_permitted_writes(project_dir, sim_log):
    """(absolute IDEA.md, path matcher, absolute SIM-LOG) — the only writable paths.

    The matcher covers a question's answer file and a stakeholder request. A request is a file
    the stakeholder writes unprompted (`spec/request.md`, F-021), so it is the one thing the sim
    may create rather than only fill in — which is the point of the artifact.
    """
    project_dir = os.path.normpath(os.path.abspath(project_dir))
    writable_re = re.compile(
        "(?:"
        + re.escape(os.path.join(project_dir, "tracker", "items"))
        + r"/[A-Za-z]+-\d+/questions/Q-\d+\.md"
        + "|"
        + re.escape(os.path.join(project_dir, "tracker", "requests"))
        + r"/R-\d+\.md"
        + ")$")
    return (os.path.join(project_dir, "IDEA.md"), writable_re,
            os.path.normpath(os.path.abspath(sim_log)))


def audit_sim(uses, project_dir, harness_dir, sim_log):
    """Violations of "the sim writes only what a stakeholder could".

    S1  wrote to a path outside {IDEA.md, a question file, a request, its own log}
    S2  used a tool it is not supposed to have at all (a shell, an agent, the network)
    """
    idea, writable_re, log = sim_permitted_writes(project_dir, sim_log)
    harness_dir = os.path.normpath(os.path.abspath(harness_dir))
    found = []
    for tool, tool_input in uses:
        if tool in ("Bash", "Agent", "Task", "WebFetch", "WebSearch", "KillShell"):
            found.append(violation("S2", tool, "the sim has no business using this tool",
                                   _blob(tool_input)))
            continue
        if tool not in WRITE_TOOLS:
            continue
        for raw, _source in _paths_in(tool, tool_input):
            resolved = _resolve(raw, harness_dir)
            if resolved == idea or resolved == log or writable_re.match(resolved):
                continue
            found.append(violation(
                "S1", tool, f"wrote to {resolved}, which a stakeholder may not touch",
                _blob(tool_input)))
    return found


def frontmatter(text):
    """The `key: value` block between the leading `---` fences. Values stay strings."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def question_files(project_dir):
    items = os.path.join(project_dir, "tracker", "items")
    if not os.path.isdir(items):
        return []
    found = []
    for item in sorted(os.listdir(items)):
        directory = os.path.join(items, item, "questions")
        if not os.path.isdir(directory):
            continue
        for name in sorted(os.listdir(directory)):
            if name.startswith("Q-") and name.endswith(".md"):
                found.append(os.path.join(directory, name))
    return found


def question_frontmatter_snapshot(project_dir):
    """{path: frontmatter} — what the sim is forbidden to change."""
    snapshot = {}
    for path in question_files(project_dir):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            snapshot[path] = frontmatter(handle.read())
    return snapshot


def audit_sim_tree(project_dir, before_snapshot):
    """S3: the sim changed a question's frontmatter, or deleted a question outright.

    Independent of the transcript on purpose. The transcript says what the session asked for;
    this says what is on disk afterwards.
    """
    found = []
    after = question_frontmatter_snapshot(project_dir)
    for path, before in before_snapshot.items():
        if path not in after:
            found.append(violation("S3", "-", f"question file {path} disappeared", path))
            continue
        if after[path] != before:
            changed = sorted(set(before.items()) ^ set(after[path].items()))
            found.append(violation(
                "S3", "-", f"question frontmatter changed in {os.path.basename(path)}",
                json.dumps(changed)))
    return found


def repo_tree_snapshot(repo_dir):
    """The toolkit repository's dirty set, as `git status --porcelain` lines."""
    import subprocess
    result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir,
                            capture_output=True, text=True)
    return sorted(line for line in result.stdout.split("\n") if line.strip())


# What a run must never change: the toolkit that is under test. `meta/` and `harness/` are
# excluded because the owner reviewing or editing them while a run is in flight is ordinary, and
# a rule that fires on the owner's own typing gets switched off within one iteration. A turn
# reaching into `harness/` is caught by W1 and W2 from the transcript, where it belongs.
TOOLKIT_PATHS = ("methodology/", "spec/", "adapters/", "scripts/", "examples/", "fixtures/",
                 "README.md", "USAGE.md", "CONSUMER-PROMPT.md", "PROMPT.md")


def audit_repo_tree(repo_dir, before):
    """W4: a turn must not change the toolkit it is running.

    Compared against a snapshot taken immediately before the turn rather than against "clean":
    what is forbidden is a *new* change appearing while a turn is running.
    """
    after = repo_tree_snapshot(repo_dir)
    appeared = [line for line in after if line not in set(before)]
    guarded = [line for line in appeared
               if any(part.startswith(TOOLKIT_PATHS) for part in line[2:].strip().split(" -> "))]
    if not guarded:
        return []
    return [violation("W4", "-", "the toolkit changed while a turn was running",
                      "\n".join(guarded))]
