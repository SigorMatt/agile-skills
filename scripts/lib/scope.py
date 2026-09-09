"""What a diff-scoped gate is actually looking at, and whether it could see anything.

A gate that reports success having examined nothing is the failure this toolkit exists to
prevent, and it has now happened three times in the same script. F-033: `lint-claims docs/x.md`
set the workspace root to a *file*, found no `docs/` beneath it and exited 0 announcing it had
checked the whole tree. F-066: `lint-claims --changed-since main`, run at an epic ending,
compares `main` with `main`, finds an empty diff, prints "no documents changed" and exits 0 — the
reviewer in iteration 4 wrote it down exactly: *"It passed here, but it would have passed over
anything."* F-076: `implement`'s claims gate is a window over the documents the branch changed,
and the rule in force forbade `implement` to write a document at all, so the window was empty on
every execution in every engagement — and this module called that a pass.

The three are one bug and it took three tries to say what it is. **Emptiness is not one state.**
A window has four, and each of them means something different to the gate standing on it:

  * **real and non-empty** — the window contains paths. *Examine them.*
  * **real and empty** — the window is well formed, this execution touched nothing in it, and
    something this execution was permitted to do would have appeared here if it had. *Pass, and
    say the window was searched.*
  * **out-of-scope-by-construction** — the window is well formed and empty, and **nothing this
    execution was permitted to do could have put anything in it**. The comparison did not come up
    empty; it was never able to come up otherwise. *Pass with a mark* — exit 0, because a gate
    that fails on the ordinary shape of ordinary work is a gate that gets switched off, but the
    result is a sentence of its own and is never spelled the same as a pass. This is F-076's
    state, and the earlier three-state model in this file justified passing it with the words
    *"because the comparison could have found something"* — which is exactly the sentence F-076
    falsifies.
  * **degenerate** — the window is not well formed at all: the ref does not resolve, there is no
    repository, or the ref IS the current commit and nothing is dirty. *Fail.* Nothing was
    examined, nothing could have been, and unlike the state above the fault is in the invocation
    rather than in the work. This is the state F-066 reported as a pass.

The difference between the third and the fourth is who is at fault and therefore what to do.
Degenerate: the gate was invoked wrongly — name a scope that can see. By construction: the gate
was invoked correctly and the *rules around it* guarantee an empty answer — which is a fact about
the methodology, not about this execution, and belongs in the record where the next reader of the
journal can find it.

This module cannot tell the third state from the second on its own: "what this execution was
permitted to do" is knowledge the caller has and a diff does not. So the caller supplies it —
`constrained(window, permitted, reason)` — and a caller that supplies nothing gets the old
three-state answer, honestly, rather than a fourth state guessed at.

Callers get the verdict and a sentence; what they do with it is theirs. This module makes no
findings and knows nothing about claims — it answers one question so that two gates answer it
the same way.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import subprocess

__all__ = ["DiffScope", "diff_scope", "working_tree_scope", "constrained", "git"]


def git(root: str, args: list):
    """Run git in `root`. Returns None when git is missing or the directory is not a repository."""
    try:
        result = subprocess.run(["git"] + args, cwd=root, capture_output=True, text=True)
    except (OSError, ValueError):
        return None
    return result


class DiffScope:
    """The window `--changed-since <ref>` opens, and whether it is worth anything.

    `verdict` is one of `real`, `by-construction`, `no-repository`, `unresolved-ref`,
    `same-commit`. `real` and `by-construction` are both well-formed windows; the three others
    are degenerate — the gate examined nothing and could not have examined anything, because the
    comparison itself is broken.

    `outcome` is the only thing a gate needs to branch on, and it names all four states of the
    module docstring: `examine`, `pass`, `mark`, `fail`.
    """

    __slots__ = ("ref", "verdict", "detail", "paths", "dirty", "reason")

    def __init__(self, ref, verdict, detail, paths=None, dirty=(), reason="") -> None:
        self.ref = ref
        self.verdict = verdict
        self.detail = detail
        self.paths = paths or []
        self.dirty = list(dirty)
        # Only the fourth state carries one: *why* nothing could have been in the window. It is
        # the caller's sentence, because the caller is the only thing that knows.
        self.reason = reason

    @property
    def degenerate(self) -> bool:
        """The window is broken. Not the same as empty, and it never was (F-066)."""
        return self.verdict not in ("real", "by-construction")

    @property
    def by_construction(self) -> bool:
        """The window is well formed, empty, and could not have been anything else (F-076)."""
        return self.verdict == "by-construction"

    @property
    def outcome(self) -> str:
        """What a gate standing on this window should do: examine / pass / mark / fail."""
        if self.degenerate:
            return "fail"
        if self.by_construction:
            return "mark"
        return "examine" if self.paths else "pass"

    @property
    def sentence(self) -> str:
        """One line, in the words of the state — never in the words of a pass.

        F-076's first direction, mechanically: *"'passed over nothing' is never spelled the same
        as 'passed'."* A caller printing this instead of composing its own cannot accidentally
        spell two states alike.
        """
        if self.by_construction:
            return (f"NOTHING COULD HAVE BEEN IN SCOPE — {self.detail}"
                    + (f", and {self.reason}" if self.reason else ""))
        if self.degenerate:
            return f"NOTHING — {self.detail}"
        if not self.paths:
            return f"nothing found in a window that was searched — {self.detail}"
        return self.detail

    @property
    def hint(self) -> str:
        """What the caller should do instead. Never 'ignore it'."""
        if self.verdict == "by-construction":
            return (f"the window is well formed and the comparison ran; what makes it empty is a "
                    f"rule, not this execution — {self.reason or 'nothing was permitted into it'}"
                    f". Record it in those words: a gate that examined nothing it could ever "
                    f"have examined is not a gate that passed (F-076)")
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


def constrained(window: DiffScope, permitted, reason: str) -> DiffScope:
    """Re-read an empty window against what this execution was *permitted* to put in it (F-076).

    `permitted` is the set of paths — however the caller computes it — that this execution was
    allowed or obliged to write into the window's scope. It is the caller's knowledge and not a
    diff's: no comparison of two commits can tell "nobody wrote a document" from "nobody was
    allowed to write one", and the whole of F-076 is that difference going unnoticed for three
    engagements.

    Only one transition is possible, and only in one direction:

      * a **real and empty** window with an empty `permitted` becomes `by-construction`;
      * everything else is returned untouched — a degenerate window stays a failure (the fault is
        in the invocation and no amount of permission fixes it), and a window with paths in it
        was manifestly able to contain something, whatever the caller believes about permissions.

    `reason` is the sentence that will be printed, and it should name the rule rather than the
    absence: *"the plan declares no invalidation set and no deliverable documents, so this
    execution was permitted to write no document at all"*.
    """
    if window.verdict != "real" or window.paths or permitted:
        return window
    return DiffScope(window.ref, "by-construction", window.detail,
                     paths=[], dirty=window.dirty, reason=reason)
