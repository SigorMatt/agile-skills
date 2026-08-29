"""What a diff-scoped gate is actually looking at, and whether it could see anything.

A gate that reports success having examined nothing is the failure this toolkit exists to
prevent, and it has now happened twice in the same script. F-033: `lint-claims docs/x.md` set the
workspace root to a *file*, found no `docs/` beneath it and exited 0 announcing it had checked
the whole tree. F-066: `lint-claims --changed-since main`, run at an epic ending, compares `main`
with `main`, finds an empty diff, prints "no documents changed" and exits 0 — the reviewer in
iteration 4 wrote it down exactly: *"It passed here, but it would have passed over anything."*

The two are one bug. A diff window has three states, not two, and only the middle one was ever
modelled:

  * **real and non-empty** — the window contains documents; check them.
  * **real and empty** — the window is well formed and this execution touched nothing in it.
    That is a pass, and it is honest, because the comparison could have found something.
  * **degenerate** — the window cannot contain this execution's work *whatever it did*: the ref
    does not resolve, there is no repository, or the ref IS the current commit and nothing is
    dirty. Nothing was examined and nothing could have been. That is a **failure**, and it is
    the state F-066 reported as a pass.

Callers get the verdict and a sentence; what they do with it is theirs. This module makes no
findings and knows nothing about claims — it answers one question so that two gates answer it
the same way.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import subprocess

__all__ = ["DiffScope", "diff_scope", "working_tree_scope", "git"]


def git(root: str, args: list):
    """Run git in `root`. Returns None when git is missing or the directory is not a repository."""
    try:
        result = subprocess.run(["git"] + args, cwd=root, capture_output=True, text=True)
    except (OSError, ValueError):
        return None
    return result


class DiffScope:
    """The window `--changed-since <ref>` opens, and whether it is worth anything.

    `verdict` is one of `real`, `no-repository`, `unresolved-ref`, `same-commit`. Everything
    except `real` is degenerate: the gate examined nothing and could not have examined anything.
    """

    __slots__ = ("ref", "verdict", "detail", "paths", "dirty")

    def __init__(self, ref, verdict, detail, paths=None, dirty=()) -> None:
        self.ref = ref
        self.verdict = verdict
        self.detail = detail
        self.paths = paths or []
        self.dirty = list(dirty)

    @property
    def degenerate(self) -> bool:
        return self.verdict != "real"

    @property
    def hint(self) -> str:
        """What the caller should do instead. Never 'ignore it'."""
        if self.verdict == "same-commit":
            return (f"{self.ref} IS the current commit and nothing is modified, so this "
                    f"comparison could not have found anything whatever this execution did — "
                    f"name the scope explicitly (--all, or a base this execution moved from) "
                    f"rather than accepting a window that cannot see")
        if self.verdict == "unresolved-ref":
            return (f"{self.ref} does not name a commit in this repository; a scope that cannot "
                    f"be resolved is not an empty scope")
        if self.verdict == "no-repository":
            return ("--changed-since needs a git repository to compare against; pass --all to "
                    "check the whole tree instead")
        return ""


def _dirty_under(root: str, subpaths: list) -> list:
    """Files with uncommitted changes under any of `subpaths` (relative, may be empty = all)."""
    # `--untracked-files=all` matters: git collapses a wholly-untracked directory to `docs/`,
    # so a brand-new document under a brand-new directory would otherwise be invisible to a gate
    # scoped by this window — present in the count, absent from the file list.
    argv = ["status", "--porcelain", "--untracked-files=all"]
    if subpaths:
        argv += ["--"] + list(subpaths)
    result = git(root, argv)
    if result is None or result.returncode != 0:
        return []
    found = []
    for line in result.stdout.split("\n"):
        if len(line) > 3:
            found.append(line[3:].strip().strip('"'))
    return found


def diff_scope(root: str, ref: str, subpaths=None) -> DiffScope:
    """Classify the window `ref..working-tree`, restricted to `subpaths` when given.

    `subpaths` scopes the dirtiness test as well as the diff, because "the tree is clean" has to
    mean "clean where this gate looks". A review that has written tracker/ but not docs/ has a
    degenerate window for a gate that reads docs/, and saying otherwise is how a gate passes
    having seen nothing.
    """
    subpaths = list(subpaths or [])
    inside = git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside is None or inside.returncode != 0 or inside.stdout.strip() != "true":
        return DiffScope(ref, "no-repository", f"{root} is not a git repository")

    resolved = git(root, ["rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"])
    if resolved is None or resolved.returncode != 0 or not resolved.stdout.strip():
        return DiffScope(ref, "unresolved-ref", f"{ref} does not resolve to a commit")
    base = resolved.stdout.strip()

    head = git(root, ["rev-parse", "--verify", "--quiet", "HEAD^{commit}"])
    head_sha = head.stdout.strip() if head is not None and head.returncode == 0 else ""

    dirty = _dirty_under(root, subpaths)
    if head_sha and head_sha == base and not dirty:
        return DiffScope(ref, "same-commit",
                         f"{ref} is the current commit ({base[:7]}) and nothing is modified"
                         + (f" under {', '.join(subpaths)}" if subpaths else ""))

    argv = ["diff", "--name-only", ref]
    if subpaths:
        argv += ["--"] + subpaths
    changed = git(root, argv)
    names = set(dirty)
    if changed is not None and changed.returncode == 0:
        names.update(line.strip() for line in changed.stdout.split("\n") if line.strip())
    return DiffScope(ref, "real",
                     f"{len(names)} path(s) differ from {ref} ({base[:7]})"
                     + (f" under {', '.join(subpaths)}" if subpaths else ""),
                     paths=sorted(names), dirty=dirty)


def working_tree_scope(root: str, subpaths=None) -> DiffScope:
    """The window for a skill that works on the trunk and commits once, at the end.

    `plan` is the case. It writes an ADR and an overview into `docs/`, runs its gates, and only
    then journals, transitions and commits — so at gate time its work is uncommitted, and the
    honest window is the working tree. Asking `--changed-since <trunk>` there compares the trunk
    with itself, which is the degenerate window F-066 is about: it would fail on an execution
    that legitimately wrote no document, and it would say nothing about one that had already
    committed.

    This window is never degenerate. It can be empty, and an empty one means what it says: this
    execution has written no document that is not already committed. Its limit is the mirror
    image of `diff_scope`'s and belongs in the open: work already committed is invisible to it,
    so it is the right scope only for a skill whose contract commits once, after its gates.
    """
    subpaths = list(subpaths or [])
    inside = git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside is None or inside.returncode != 0 or inside.stdout.strip() != "true":
        return DiffScope("the working tree", "no-repository",
                         f"{root} is not a git repository")
    dirty = _dirty_under(root, subpaths)
    return DiffScope("the working tree", "real",
                     f"{len(dirty)} uncommitted path(s)"
                     + (f" under {', '.join(subpaths)}" if subpaths else ""),
                     paths=sorted(dirty), dirty=dirty)
