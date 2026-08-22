#!/usr/bin/env python3
"""Provision a throwaway project for one harness iteration. Mechanical; no agent session.

Usage:
  harness/provision.py --iteration <id> [--root DIR] [--dry-run]
  harness/provision.py --project <name>  [--root DIR] [--dry-run]
  harness/provision.py --iteration <id> --force      # adopt a non-empty stranger directory

What it does, in order:

  1. create <root>/<project>, `git init` it, and give it a repo-local identity so the worker's
     commits are distinguishable from the owner's;
  2. write the project's `.gitignore` and `SIMULATION-NOTICE.md`, and copy `CONSUMER-PROMPT.md`
     in from this repository — the worker is driven by the real consumer prompt, not by a
     harness paraphrase of it;
  3. run `adapters/claude-code/install.py`;
  4. run `.claude/agile-skills/scripts/workspace-init`;
  5. merge the `USAGE.md` §4 allow-list into `.claude/settings.json`, leaving the installer's
     hooks alone (and, with `--trust`, register the project in `~/.claude.json` so that a
     headless session honours that allow-list at all — see `trust_project`);
  6. commit everything as one initial commit.

Idempotent: running it again on a project it provisioned re-runs the installer (which is itself
idempotent), re-merges the allow-list, and commits only if something changed.

It refuses to touch a directory that is non-empty and does not carry its marker
(`.harness/provision.json`) — provisioning is destructive in the sense that it drops a `.claude/`
tree and a git repository into whatever it is pointed at, and pointing it at the wrong path is a
one-character mistake.

Standard library only (ADR-0002), like everything else in this repository.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MARKER = os.path.join(".harness", "provision.json")
DEFAULT_ROOT = os.path.expanduser(
    os.environ.get("HARNESS_THROWAWAY_ROOT", "~/agile-skills-throwaway"))

# Copied verbatim from USAGE.md §4. harness/tests/ asserts they are still identical: if the
# owner's advice to consumers and the harness's own setup drift apart, the harness stops being
# evidence about the documented path.
ALLOW_LIST = [
    "Bash(python3 .claude/agile-skills/scripts/*)",
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git branch:*)",
]

GITIGNORE = """\
__pycache__/
*.pyc
.venv/
/HARNESS-STATUS.md
/.harness/
"""

SIMULATION_NOTICE = """\
# The stakeholder in this project is simulated

This project is a throwaway, created by an automated harness to exercise the agile-skills
pipeline. Two facts about it are load-bearing, and both are here rather than in a prompt so that
they survive a fresh session:

1. **The human is a simulation.** The person who states the idea and answers questions is an
   automated stand-in. Their answers are still the authoritative statement of what is wanted —
   treat them exactly as you would a real stakeholder's — but never record that a real person
   said something. The record must not claim more than it can support.

2. **The human is asynchronous and is not in this session.** They cannot be asked a question
   directly, and there is no interactive question tool. When you need them, file a question
   artifact per `.claude/agile-skills/spec/question.md` with `addressed-to: human`, suspend the
   item, and stop. The answer will appear in that file's `## Answer` section before you are run
   again.

Nothing else about this project is unusual. The code, the tracker and the docs are real work.
"""


def run(argv, cwd, dry_run=False, check=True):
    if dry_run:
        print(f"  would run: {' '.join(argv)}  (in {cwd})")
        return subprocess.CompletedProcess(argv, 0, "", "")
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.stderr.write(f"provision: command failed: {' '.join(argv)}\n")
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(1)
    return result


def load_iteration(iteration_id):
    path = os.path.join(HERE, "iterations", f"{iteration_id}.json")
    if not os.path.isfile(path):
        available = []
        directory = os.path.join(HERE, "iterations")
        if os.path.isdir(directory):
            available = sorted(name[:-5] for name in os.listdir(directory)
                               if name.endswith(".json"))
        sys.stderr.write(f"provision: no iteration config at {path}\n")
        if available:
            sys.stderr.write(f"           known iterations: {', '.join(available)}\n")
        raise SystemExit(2)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def directory_state(project_dir):
    """(state, detail) where state is one of empty | ours | stranger."""
    if not os.path.isdir(project_dir):
        return "empty", "does not exist"
    entries = [name for name in os.listdir(project_dir) if name not in (".", "..")]
    if not entries:
        return "empty", "exists and is empty"
    if os.path.isfile(os.path.join(project_dir, MARKER)):
        return "ours", "carries .harness/provision.json"
    return "stranger", f"contains {len(entries)} entry/entries and no provisioning marker"


def wipe(project_dir, root, dry_run) -> int:
    """Delete a provisioned project so the next provision starts from nothing (H-003).

    `--fresh` on the driver archives the *run* — logs, state, transcripts — and leaves the
    project workspace exactly as the last run left it. That is a reasonable thing for it to do
    and it was not what anyone expected: iteration 1 silently resumed the mini run's epic, so
    turn 1's sim found IDEA.md already present and turn 2's worker found thirteen of sixteen
    questions already answered. One flag, one meaning. This is the other meaning.

    Two refusals, both deliberate. The directory must carry this tool's own marker, so a wipe
    cannot land on a directory somebody else made; and it must sit under the throwaway root, so
    a mistyped --root cannot turn this into a general-purpose delete.
    """
    state, detail = directory_state(project_dir)
    if state == "empty":
        print(f"provision: nothing to wipe at {project_dir} ({detail})")
        return 0
    if state != "ours":
        sys.stderr.write(
            f"provision: refusing to wipe {project_dir}\n"
            f"           it {detail}, so this tool did not create it.\n"
            f"           --wipe deletes a directory; it will only ever delete one that carries\n"
            f"           {MARKER}.\n")
        return 2
    if os.path.commonpath([os.path.abspath(project_dir), root]) != root \
            or os.path.abspath(project_dir) == root:
        sys.stderr.write(
            f"provision: refusing to wipe {project_dir}\n"
            f"           it is not a directory *inside* the throwaway root {root}.\n")
        return 2
    if dry_run:
        print(f"  would delete {project_dir} and everything under it")
        return 0
    shutil.rmtree(project_dir)
    print(f"provision: wiped {project_dir} — the next provision starts from nothing")
    return 0


def write_file(path, content, dry_run):
    if dry_run:
        print(f"  would write {path}")
        return False
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as handle:
            if handle.read() == content:
                return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    print(f"  wrote {os.path.basename(path)}")
    return True


def trust_project(project_dir, dry_run):
    """Register the project as trusted in ~/.claude.json.

    A `-p` session never shows the workspace-trust dialog, and an untrusted workspace's
    `permissions.allow` entries are **ignored wholesale** — observed, not assumed:

        Ignoring 8 permissions.allow entries from .claude/settings.json: this workspace has
        not been trusted.

    So the allow-list this script merges in step 5 does nothing at all in a headless run unless
    the project is trusted first. This is opt-in (`--trust`) because it writes to the owner's
    machine-level config, outside both this repository and the throwaway root.
    """
    path = os.path.expanduser("~/.claude.json")
    config = {}
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as handle:
            try:
                config = json.load(handle)
            except (json.JSONDecodeError, ValueError):
                sys.stderr.write(f"provision: {path} is not valid JSON; not touching it\n")
                return False
    projects = config.setdefault("projects", {})
    entry = projects.setdefault(project_dir, {})
    if entry.get("hasTrustDialogAccepted") is True:
        return False
    entry["hasTrustDialogAccepted"] = True
    if dry_run:
        print(f"  would mark {project_dir} trusted in ~/.claude.json")
        return False
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=2)
        handle.write("\n")
    print("  marked the project trusted in ~/.claude.json (--trust)")
    return True


def merge_allow_list(project_dir, dry_run):
    """Add USAGE §4's allow-list to .claude/settings.json without disturbing the hooks."""
    path = os.path.join(project_dir, ".claude", "settings.json")
    settings = {}
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as handle:
            settings = json.load(handle)
    permissions = settings.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])
    added = [rule for rule in ALLOW_LIST if rule not in allow]
    allow.extend(added)
    if dry_run:
        print(f"  would merge {len(added)} allow-list entry/entries into .claude/settings.json")
        return False
    if not added:
        return False
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(settings, handle, indent=2)
        handle.write("\n")
    print(f"  merged {len(added)} allow-list entry/entries into .claude/settings.json")
    return True


def provision(project_dir, project_name, dry_run, force, trust):
    state, detail = directory_state(project_dir)
    print(f"provision: {project_dir}  [{state}: {detail}]")
    if state == "stranger" and not force:
        sys.stderr.write(
            f"provision: refusing to provision {project_dir}\n"
            f"           it {detail}.\n"
            "           Provisioning writes a git repository and a .claude/ tree into this\n"
            "           directory. If that is really what you want, pass --force.\n")
        raise SystemExit(2)

    if not dry_run:
        os.makedirs(project_dir, exist_ok=True)

    # 1. git
    if not os.path.isdir(os.path.join(project_dir, ".git")):
        run(["git", "init", "-q", "-b", "main"], project_dir, dry_run)
        if not dry_run:
            print("  git init (branch main)")
    run(["git", "config", "user.name", "agile-skills harness worker"], project_dir, dry_run)
    run(["git", "config", "user.email", "worker@harness.invalid"], project_dir, dry_run)

    # 2. the files the project starts life with
    write_file(os.path.join(project_dir, ".gitignore"), GITIGNORE, dry_run)
    write_file(os.path.join(project_dir, "SIMULATION-NOTICE.md"), SIMULATION_NOTICE, dry_run)
    with open(os.path.join(REPO, "CONSUMER-PROMPT.md"), "r", encoding="utf-8") as handle:
        write_file(os.path.join(project_dir, "CONSUMER-PROMPT.md"), handle.read(), dry_run)

    # 3. the toolkit
    run([sys.executable, os.path.join(REPO, "adapters", "claude-code", "install.py"),
         project_dir], REPO, dry_run)
    if not dry_run:
        print("  installed the rendered skills")

    # 4. the workspace
    workspace_init = os.path.join(project_dir, ".claude", "agile-skills", "scripts",
                                  "workspace-init")
    run([sys.executable, workspace_init, project_dir], project_dir, dry_run)
    if not dry_run:
        print("  initialised the workspace")

    # 5. the documented allow-list
    merge_allow_list(project_dir, dry_run)
    if trust:
        trust_project(project_dir, dry_run)

    # 6. the marker, then one commit
    toolkit_version = "unknown"
    version_file = os.path.join(project_dir, ".claude", "agile-skills", "VERSION")
    if os.path.isfile(version_file):
        with open(version_file, "r", encoding="utf-8") as handle:
            toolkit_version = handle.readline().strip()
    marker = {
        "provisioned-by": "harness/provision.py",
        "toolkit-version": toolkit_version,
        "project": project_name,
    }
    write_file(os.path.join(project_dir, MARKER),
               json.dumps(marker, indent=2) + "\n", dry_run)

    if dry_run:
        print("provision: dry run, nothing was written")
        return 0

    run(["git", "add", "-A"], project_dir)
    staged = run(["git", "diff", "--cached", "--name-only"], project_dir).stdout.strip()
    if staged:
        run(["git", "commit", "-q", "-m",
             "chore: provision the project (skills installed, workspace initialised)"],
            project_dir)
        print(f"  committed {len(staged.splitlines())} file(s)")
    else:
        print("  nothing to commit (already provisioned)")

    validator = os.path.join(project_dir, ".claude", "agile-skills", "scripts",
                             "validate-workspace")
    result = run([sys.executable, validator, project_dir], project_dir, check=False)
    print("  validate-workspace: " + ("clean" if result.returncode == 0
                                      else f"exit {result.returncode}"))
    for line in (result.stdout + result.stderr).rstrip().split("\n"):
        if line.strip():
            print(f"    {line}")
    if not trust:
        print("provision: note — this project is NOT trusted, so Claude Code ignores the "
              "permissions.allow")
        print("           entries in .claude/settings.json for every headless run. That is "
              "harmless while")
        print("           the worker runs with bypassPermissions; pass --trust if you want the "
              "allow-list")
        print("           to be the thing under test.")
    print(f"provision: ready — {project_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--iteration", help="iteration config id under harness/iterations/")
    parser.add_argument("--project", help="project directory name (instead of --iteration)")
    parser.add_argument("--root", default=DEFAULT_ROOT,
                        help=f"throwaway root (default {DEFAULT_ROOT})")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="provision into a non-empty directory that is not ours")
    parser.add_argument("--wipe", action="store_true",
                        help="delete the project directory first, so provisioning starts from "
                             "nothing. Only works on a directory this tool provisioned, and "
                             "only under the throwaway root")
    parser.add_argument("--trust", action="store_true",
                        help="mark the project trusted in ~/.claude.json, so that the "
                             "allow-list in .claude/settings.json is honoured in headless runs")
    args = parser.parse_args()

    if not args.iteration and not args.project:
        parser.error("one of --iteration or --project is required")
    project_name = args.project
    if args.iteration:
        config = load_iteration(args.iteration)
        project_name = args.project or config["project"]
    root = os.path.abspath(os.path.expanduser(args.root))
    project_dir = os.path.join(root, project_name)
    if args.wipe:
        code = wipe(project_dir, root, args.dry_run)
        if code:
            return code
    return provision(project_dir, project_name, args.dry_run, args.force, args.trust)


if __name__ == "__main__":
    raise SystemExit(main())
