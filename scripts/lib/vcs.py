"""The few questions this toolkit asks git, asked in one place.

Two programs need the same answer about a recorded merge — `scripts/record-merge`, which refuses
to write a sha it cannot stand behind, and `scripts/validate-workspace`, which re-asks on every
run so that a hand-edited field is caught too. One rule in two places is two rules that will
disagree, and the way they would disagree here is the whole of F-035: a record that reports a
merge that never happened is worse than a record that reports no merge at all.

Every function degrades to "I could not look" rather than to "it is fine". A directory that is
not a repository, a trunk that does not exist, a git that is not installed: those produce `None`
and the caller says nothing, because a check that cannot see must not claim a pass
(`spec/skill-contract.md` §1.4). Standard library only (ADR-0002).
"""

from __future__ import annotations

import re
import subprocess

__all__ = ["SHA_RE", "git", "is_repo", "rev", "merge_problems", "merged_into"]

# What may be written into `merge-commit`. Short enough to be readable, long enough to be
# unambiguous; git itself decides whether it resolves, and that is the check that matters.
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def git(root: str, args: list):
    """`git -C <root> <args>`, or None when git could not be run at all."""
    try:
        return subprocess.run(["git", "-C", root] + list(args),
                              capture_output=True, text=True)
    except OSError:
        return None


def is_repo(root: str) -> bool:
    result = git(root, ["rev-parse", "--git-dir"])
    return result is not None and result.returncode == 0


def rev(root: str, reference: str):
    """The full sha `reference` names, or None when it names nothing in this repository."""
    result = git(root, ["rev-parse", "--verify", "--quiet", f"{reference}^{{commit}}"])
    if result is None or result.returncode != 0:
        return None
    return result.stdout.strip() or None


def merge_problems(root: str, sha: str, branch, trunk: str):
    """What is wrong with `sha` as the merge of `branch` into `trunk`.

    Returns a list of `(code, message)`, empty when nothing is wrong, and **None** when the
    question could not be asked — no git, or not a repository. The caller decides what to do
    with each; the codes are the validator's finding codes so that the tool's refusal and the
    validator's finding say the same words.

    The four things a recorded merge has to be, and why each is not decoration:

    * it **resolves** — a sha naming nothing is a citation to a commit that does not exist;
    * it is a **merge** — two or more parents. A fast-forward leaves no commit to name, and a
      sha with one parent is somebody's ordinary commit recorded as the close of an item;
    * it is an **ancestor of the trunk** — the merge is what puts the work on the trunk, so one
      that is not on the trunk did not happen, whatever the field says;
    * it **contains the branch** — otherwise it is a merge, on the trunk, of something else.
      Only asked while the branch ref still resolves: a branch deleted after merging is normal
      housekeeping and its absence is not evidence of anything.
    """
    if not is_repo(root):
        return None
    problems = []
    if not SHA_RE.match(sha or ""):
        return [("item.merge.malformed",
                 f"merge-commit is {sha!r}; expected 7 to 40 lowercase hex characters")]
    resolved = rev(root, sha)
    if resolved is None:
        return [("item.merge.unresolved",
                 f"merge-commit {sha} names no commit in this repository")]
    parents = git(root, ["rev-list", "--parents", "-n", "1", resolved])
    if parents is not None and parents.returncode == 0:
        if len(parents.stdout.split()) < 3:
            problems.append(("item.merge.not-a-merge",
                             f"merge-commit {sha} has fewer than two parents, so it is not a "
                             f"merge commit"))
    trunk_sha = rev(root, trunk)
    if trunk_sha is not None:
        ancestor = git(root, ["merge-base", "--is-ancestor", resolved, trunk_sha])
        if ancestor is not None and ancestor.returncode != 0:
            problems.append(("item.merge.unmerged",
                             f"merge-commit {sha} is not an ancestor of {trunk}, so the merge "
                             f"it records is not on the trunk"))
    if branch:
        branch_sha = rev(root, branch)
        if branch_sha is not None:
            contains = git(root, ["merge-base", "--is-ancestor", branch_sha, resolved])
            if contains is not None and contains.returncode != 0:
                problems.append(("item.merge.other-branch",
                                 f"merge-commit {sha} does not contain {branch}"))
    return problems


def merged_into(root: str, branch: str, trunk: str):
    """True when `branch` is on `trunk`, False when it is not, None when unanswerable.

    Distinguished from `merge_problems` because it answers the *other* direction: not "is this
    recorded merge real" but "did a merge happen that nothing recorded". A branch pointing at
    the trunk's own head has nothing on it and was not merged — the separation F-035 turned on.
    """
    if not is_repo(root):
        return None
    branch_sha, trunk_sha = rev(root, branch), rev(root, trunk)
    if branch_sha is None or trunk_sha is None:
        return None
    if branch_sha == trunk_sha:
        return False
    ancestor = git(root, ["merge-base", "--is-ancestor", branch_sha, trunk_sha])
    if ancestor is None:
        return None
    return ancestor.returncode == 0
