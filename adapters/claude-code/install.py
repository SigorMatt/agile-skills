#!/usr/bin/env python3
"""Install the rendered skills into a project. Idempotent.

Usage:
  adapters/claude-code/install.py <project-root>              install or update
  adapters/claude-code/install.py <project-root> --uninstall   remove exactly what was installed
  adapters/claude-code/install.py <project-root> --dry-run     say what would change

What it places, and nowhere else:

  <project>/.claude/skills/<skill>/            one directory per skill
  <project>/.claude/agile-skills/              pipeline.yaml, spec/, scripts/, contracts, hooks
  <project>/.claude/settings.json              two PreToolUse hook entries, merged in

It never touches the project's source code, its git history, or `tracker/` and `docs/` — the
workspace is the project's record, not the adapter's, so uninstalling the tooling must never
remove the paper trail (adapters/README.md capability C4).

Standard library only (ADR-0002).
"""

from __future__ import annotations

import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
HOOKS_SOURCE = os.path.join(HERE, "hooks")

SKILLS_DIR = os.path.join(".claude", "skills")
SHARED_DIR = os.path.join(".claude", "agile-skills")
SETTINGS = os.path.join(".claude", "settings.json")

# Marker so an update can find and replace our own hook entries without disturbing anyone
# else's. Editing a shared settings file blind is how an installer earns a bad reputation.
HOOK_MARKER = "agile-skills:guard-workspace-writes"
HOOK_COMMAND = ("python3 \"${CLAUDE_PROJECT_DIR}/.claude/agile-skills/hooks/"
                "guard-workspace-writes.py\"")


def hook_entry(matcher: str) -> dict:
    return {
        "matcher": matcher,
        "hooks": [{
            "type": "command",
            "command": HOOK_COMMAND,
            "timeout": 10,
            "statusMessage": HOOK_MARKER,
        }],
    }


def is_ours(entry) -> bool:
    if not isinstance(entry, dict):
        return False
    for hook in entry.get("hooks") or []:
        if isinstance(hook, dict) and (
            hook.get("statusMessage") == HOOK_MARKER
            or HOOK_MARKER in str(hook.get("command", ""))
            or "guard-workspace-writes.py" in str(hook.get("command", ""))
        ):
            return True
    return False


class Installer:
    def __init__(self, target: str, dry_run: bool) -> None:
        self.target = os.path.abspath(target)
        self.dry_run = dry_run
        self.actions = []

    def say(self, action: str) -> None:
        self.actions.append(action)
        print(f"  {'would ' if self.dry_run else ''}{action}")

    def copy_tree(self, source: str, relative: str) -> None:
        destination = os.path.join(self.target, relative)
        if self.dry_run:
            self.say(f"copy {os.path.relpath(source, HERE)} -> {relative}")
            return
        if os.path.isdir(destination):
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        for base, _, files in os.walk(destination):
            for name in files:
                if os.path.splitext(name)[1] in ("", ".py", ".sh"):
                    path = os.path.join(base, name)
                    with open(path, "rb") as handle:
                        if handle.read(2) == b"#!":
                            os.chmod(path, 0o755)
        self.say(f"installed {relative}")

    def remove(self, relative: str) -> None:
        path = os.path.join(self.target, relative)
        if not os.path.exists(path):
            return
        if self.dry_run:
            self.say(f"remove {relative}")
            return
        shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
        self.say(f"removed {relative}")

    # ---- settings ------------------------------------------------------------------

    def load_settings(self) -> dict:
        path = os.path.join(self.target, SETTINGS)
        if not os.path.isfile(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"install: {SETTINGS} is not valid JSON ({exc}); refusing to rewrite it.",
                  file=sys.stderr)
            print("        Fix or move it, then run install again.", file=sys.stderr)
            raise SystemExit(1)

    def write_settings(self, settings: dict) -> None:
        path = os.path.join(self.target, SETTINGS)
        if self.dry_run:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(settings, handle, indent=2, sort_keys=False)
            handle.write("\n")

    def install_hooks(self) -> None:
        settings = self.load_settings()
        hooks = settings.setdefault("hooks", {})
        pre = hooks.setdefault("PreToolUse", [])
        kept = [entry for entry in pre if not is_ours(entry)]
        removed = len(pre) - len(kept)
        kept.extend([hook_entry("Edit|Write|MultiEdit|NotebookEdit"), hook_entry("Bash")])
        hooks["PreToolUse"] = kept
        self.write_settings(settings)
        self.say(f"registered 2 PreToolUse hook(s) in {SETTINGS}"
                 + (f" (replacing {removed} previous entry/entries)" if removed else ""))

    def uninstall_hooks(self) -> None:
        path = os.path.join(self.target, SETTINGS)
        if not os.path.isfile(path):
            return
        settings = self.load_settings()
        hooks = settings.get("hooks") or {}
        pre = hooks.get("PreToolUse") or []
        kept = [entry for entry in pre if not is_ours(entry)]
        if len(kept) == len(pre):
            return
        if kept:
            hooks["PreToolUse"] = kept
        else:
            hooks.pop("PreToolUse", None)
        if not hooks:
            settings.pop("hooks", None)
        self.write_settings(settings)
        self.say(f"removed {len(pre) - len(kept)} hook entry/entries from {SETTINGS}")

    # ---- drivers -------------------------------------------------------------------

    def install(self) -> int:
        if not os.path.isdir(DIST):
            print("install: dist/ does not exist; run adapters/claude-code/render.py first",
                  file=sys.stderr)
            return 1
        print(f"install: agile-skills -> {self.target}")

        for name in sorted(os.listdir(os.path.join(DIST, "skills"))):
            self.copy_tree(os.path.join(DIST, "skills", name),
                           os.path.join(SKILLS_DIR, name))
        self.copy_tree(os.path.join(DIST, "agile-skills"), SHARED_DIR)
        self.copy_tree(HOOKS_SOURCE, os.path.join(SHARED_DIR, "hooks"))
        self.install_hooks()

        version_file = os.path.join(self.target, SHARED_DIR, "VERSION")
        if os.path.isfile(version_file) and not self.dry_run:
            with open(version_file, "r", encoding="utf-8") as handle:
                first = handle.readline().strip()
            print(f"install: installed methodology {first}")
        print(f"install: {len(self.actions)} action(s)")
        print("install: next, initialise the workspace with")
        print(f"           python3 {SHARED_DIR}/scripts/workspace-init .")
        return 0

    def uninstall(self) -> int:
        print(f"install: removing agile-skills from {self.target}")
        skills_root = os.path.join(self.target, SKILLS_DIR)
        installed = []
        if os.path.isdir(os.path.join(DIST, "skills")):
            installed = sorted(os.listdir(os.path.join(DIST, "skills")))
        for name in installed:
            if os.path.isdir(os.path.join(skills_root, name)):
                self.remove(os.path.join(SKILLS_DIR, name))
        self.remove(SHARED_DIR)
        # Leave .claude/skills/ only if someone else's skills live there.
        if os.path.isdir(skills_root) and not os.listdir(skills_root) and not self.dry_run:
            os.rmdir(skills_root)
            self.say(f"removed {SKILLS_DIR} (it was left empty)")
        self.uninstall_hooks()
        print("install: tracker/ and docs/ were left untouched — they are the project's "
              "record, not the tooling's")
        print(f"install: {len(self.actions)} action(s)")
        return 0


def main(argv: list) -> int:
    positional = [arg for arg in argv[1:] if not arg.startswith("--")]
    flags = {arg for arg in argv[1:] if arg.startswith("--")}
    if not positional:
        print("usage: install.py <project-root> [--uninstall] [--dry-run]", file=sys.stderr)
        return 2
    target = positional[0]
    if not os.path.isdir(target):
        print(f"install: {target} is not a directory", file=sys.stderr)
        return 1
    installer = Installer(target, "--dry-run" in flags)
    return installer.uninstall() if "--uninstall" in flags else installer.install()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
