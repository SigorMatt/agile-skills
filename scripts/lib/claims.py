"""Claim provenance: the citation forms, and whether one resolves.

Shared by `scripts/lint-claims` (the gate) and `scripts/validate-workspace` (the resting-state
check), because two implementations of "does this citation resolve" would disagree eventually and
the disagreement would surface as a gate that passes on a record the validator rejects.

The convention itself is specified in `spec/doc-header.md`. Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import re
import subprocess

import frontmatter  # noqa: E402
from record import FENCE_RE  # noqa: E402
from textio import read_text  # noqa: E402

__all__ = ["CITATION_RE", "ABSOLUTE_RE", "CODE_TOKEN_RE", "CitationResolver",
           "AC_LINE_RE", "AC_RENUMBERABLE_STATUSES", "ac_state", "criteria_in",
           "normalise_anchor",
           "looks_like_code", "mask_code", "masked_lines", "split_sources"]

CITATION_RE = re.compile(r"\[src:\s*(?P<body>[^\]]+)\]")
# The `:NNN` suffix of a workspace-path citation, and nothing else after it.
PATH_LINE_RE = re.compile(r"^:(\d+)$")
CODE_SPAN_RE = re.compile(r"(`+)(?:(?!\1).)*?\1", re.DOTALL)

# The words that turn a description into a claim nothing can hedge.
ABSOLUTES = [
    "no", "none", "never", "always", "only", "every", "all", "any", "nothing", "cannot",
    "can't", "impossible", "guaranteed", "guarantees", "exactly", "must not", "mustn't",
]
ABSOLUTE_RE = re.compile(r"(?<![\w-])(" + "|".join(re.escape(word) for word in ABSOLUTES)
                         + r")(?![\w-])", re.IGNORECASE)

# A backticked token that looks like a code object rather than a word: an identifier with an
# underscore or a call, a path, a dotted name, or a SHOUTING constant.
CODE_TOKEN_RE = re.compile(r"`([^`]+)`")
PATH_RE = re.compile(r"^[\w.\-/]+\.(py|md|yaml|yml|json|toml|txt|sh|js|ts|rs|go|c|h|cpp)$")

ITEM_RE = re.compile(r"^(EP-\d{3}|WI-\d{4}|BUG-\d{4})$")
# An acceptance criterion, optionally anchored to the criterion's own words (F-094). The anchor
# is what a renumbering cannot move; the number, on its own, is a position in a list.
ITEM_AC_RE = re.compile(r"^(EP-\d{3}|WI-\d{4}|BUG-\d{4})\s+(AC\d+)"
                        r"(?:\s+[\"\u201c](?P<anchor>[^\"\u201d]+)[\"\u201d])?$")
ITEM_QUESTION_RE = re.compile(r"^(EP-\d{3}|WI-\d{4}|BUG-\d{4})/(Q-\d{3})$")
ADR_RE = re.compile(r"^ADR-(\d{4})$")
COMMIT_RE = re.compile(r"^commit\s+([0-9a-f]{7,40})$")
RUN_RE = re.compile(r"^run:\s*(?P<command>.+?)\s*(?:→|->)\s*(?P<outcome>.+)$")
# The acceptance-criterion line, in one place. `workspace.py` imports it rather than keeping a
# second copy: two regexes for one line disagree the first time a state is added to it, and one
# just was. The three states are `[ ]` not settled, `[x]` settled by the observation the
# criterion names, and `[~]` settled by a **substitution** — the environment could not perform
# that observation and something else was observed in its place (F-096, spec/work-item.md §2).
AC_LINE_RE = re.compile(r"^\s*-\s+\[(?P<state>[ x~X])\]\s+(?P<label>AC\d+)"
                        r"\s*(?:—|-|:)?\s*(?P<text>.*)$")

# The statuses at which `spec/work-item.md` §2 still permits the criteria to be rewritten, so a
# criterion's *number* is a position in a list rather than a name for it (F-094).
AC_RENUMBERABLE_STATUSES = ("draft", "ready")


def ac_state(mark: str) -> str:
    """`unticked` | `ticked` | `substituted`, from the character between the brackets."""
    mark = mark.strip().lower()
    if mark == "x":
        return "ticked"
    if mark == "~":
        return "substituted"
    return "unticked"


def criteria_in(text: str):
    """Every acceptance criterion in `text`, as `{label, state, text, offset}`.

    `text` is the criterion's whole list item, continuation lines included — a criterion long
    enough to need a citation is usually long enough to wrap, and a rule that reads only the
    first line would be satisfied or defeated by where the author pressed return. `offset` is the
    0-based line index of the criterion's **first** line, which is where a finding points.
    """
    found = []
    lines = text.split("\n")
    index = 0
    while index < len(lines):
        match = AC_LINE_RE.match(lines[index])
        if not match:
            index += 1
            continue
        parts = [match.group("text").strip()]
        offset, index = index, index + 1
        while index < len(lines):
            following = lines[index]
            if not following.strip() or not following[:1].isspace() \
                    or AC_LINE_RE.match(following):
                break
            parts.append(following.strip())
            index += 1
        found.append({"label": match.group("label"),
                      "state": ac_state(match.group("state")),
                      "text": " ".join(part for part in parts if part).strip(),
                      "offset": offset})
    return found


def normalise_anchor(text: str) -> str:
    """Compare an anchor with a criterion the way a reader would: words, not whitespace.

    Backticks are dropped from both sides — this repository's prose writes every path and every
    identifier in them, and whether the quoting author kept them is not a fact about the
    criterion.
    """
    return " ".join(text.replace("`", " ").split()).casefold()



def mask_code(text: str) -> str:
    """Blank out inline code spans, preserving length and newlines.

    Replacing rather than deleting keeps every line number and every column intact, so a finding
    still points at the right place.
    """
    def blank(match):
        return "".join("\n" if character == "\n" else " " for character in match.group(0))
    return CODE_SPAN_RE.sub(blank, text)


def masked_lines(text: str):
    """Lines of `text` with code spans and fenced blocks blanked out."""
    lines = mask_code(text).split("\n")
    fenced = False
    out = []
    for line in lines:
        if FENCE_RE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return out


def looks_like_code(token: str) -> bool:
    """Is this backticked token a thing in the system, rather than a quoted English word?"""
    token = token.strip()
    if not token:
        return False
    if PATH_RE.match(token) or "/" in token:
        return True
    if "(" in token or "_" in token or "::" in token:
        return True
    if token.isupper() and len(token) > 2:
        return True
    if "." in token and " " not in token:
        return True
    return False


def _shorten(text: str, words: int = 12) -> str:
    """The opening words of a criterion, for a message that has to quote it back."""
    parts = text.split()
    return " ".join(parts[:words]) + ("…" if len(parts) > words else "")


def split_sources(body: str):
    """The separate sources inside one `[src: ...]` marker.

    Several are separated by `;` (`doc-header.md` §4a) — but a `run:` citation carries a whole
    command, and a command may contain a semicolon of its own. F-070: a reviewer wrote
    `[src: run: python3 -c "import sys; print(...)" → …]`, got two `claim.citation.unresolved`
    errors, and replaced the command citation with a weaker `[src: <path>]` rather than leave an
    unresolvable pointer standing. The tool was nudging the author away from the citation form
    that carries the most evidence, which is the opposite of the point.

    So a `run:` part runs to the end of the marker. That is a real limit and it is the honest one:
    a `run:` citation cannot be followed by a second source inside the same marker, and it does
    not need to be — write a second marker.
    """
    parts, current = [], []
    tokens = body.split(";")
    while tokens:
        token = tokens.pop(0)
        current.append(token)
        joined = ";".join(current)
        stripped = joined.strip().strip("`")
        if stripped.lower().startswith("src:"):
            stripped = stripped[4:].strip()
        if stripped.lower().startswith("run:") and tokens:
            # Swallow the rest of the marker: the command owns every remaining semicolon.
            current.extend(tokens)
            tokens = []
        parts.append(";".join(current))
        current = []
    return parts or [body]


class CitationResolver:
    """Resolves `[src: ...]` citations against one workspace."""

    def __init__(self, root: str) -> None:
        self.root = os.path.abspath(root)
        self.items = self._load_items()

    def _load_items(self) -> dict:
        """`{ID: {"body": text, "status": str or None}}`.

        The status is read because it decides whether a criterion's *number* is an identity yet
        (F-094), and it is read tolerantly: a malformed item.md is somebody else's finding, not a
        traceback out of the citation resolver.
        """
        base = os.path.join(self.root, "tracker", "items")
        found = {}
        if not os.path.isdir(base):
            return found
        for name in sorted(os.listdir(base)):
            path = os.path.join(base, name, "item.md")
            if os.path.isfile(path):
                text = read_text(path)[0]
                status = None
                try:
                    fields, _body, _line = frontmatter.split(text, name=path)
                    value = fields.get("status")
                    status = value if isinstance(value, str) else None
                except Exception:
                    status = None
                found[name] = {"body": text, "status": status}
        return found

    def git(self, args: list):
        try:
            return subprocess.run(["git", "-C", self.root] + args,
                                  capture_output=True, text=True)
        except OSError:
            return None

    def resolve(self, citation: str) -> str:
        """An error message, or '' when the citation resolves."""
        raw = citation
        citation = citation.strip().strip("`")
        # F-040: several sources are separated by ';' inside one marker, so the second part
        # arrives without the prefix. Writing it anyway is the obvious mistake, and reporting it
        # as an unrecognised citation sends the author looking at the wrong thing.
        repeated_prefix = False
        if citation.lower().startswith("src:"):
            citation = citation[4:].strip()
            repeated_prefix = True
        if not citation:
            return "an empty citation"
        message = self._resolve(citation)
        if message and repeated_prefix:
            return (f"{message} — note that {raw.strip()!r} repeats the 'src:' prefix; inside one "
                    f"marker, sources are separated by ';' and only the first carries it")
        return message

    def _resolve(self, citation: str) -> str:

        match = RUN_RE.match(citation)
        if match:
            if not match.group("outcome").strip():
                return f"{citation!r} records a command with no outcome"
            return ""

        match = COMMIT_RE.match(citation)
        if match:
            result = self.git(["cat-file", "-e", f"{match.group(1)}^{{commit}}"])
            if result is None:
                return f"{citation!r} cannot be checked — this workspace is not a git repository"
            if result.returncode != 0:
                return f"commit {match.group(1)} is not in this repository"
            return ""

        match = ITEM_QUESTION_RE.match(citation)
        if match:
            path = os.path.join(self.root, "tracker", "items", match.group(1), "questions",
                                f"{match.group(2)}.md")
            return "" if os.path.isfile(path) else f"{citation} does not exist"

        match = ITEM_AC_RE.match(citation)
        if match:
            return self._resolve_criterion(match.group(1), match.group(2),
                                           match.group("anchor"))

        if ITEM_RE.match(citation):
            return "" if citation in self.items \
                else f"{citation} is not an item in this workspace"

        match = ADR_RE.match(citation)
        if match:
            adr_dir = os.path.join(self.root, "docs", "architecture", "adr")
            if os.path.isdir(adr_dir):
                for name in os.listdir(adr_dir):
                    if name.startswith(f"ADR-{match.group(1)}-"):
                        return ""
            return f"{citation} is not an ADR in docs/architecture/adr/"

        candidate = citation.split(":")[0].split(" ")[0]
        if "/" in candidate or "." in candidate:
            target = os.path.join(self.root, candidate)
            if not os.path.exists(target):
                return f"{candidate!r} does not exist in this workspace"
            # `path:line` is the most precise citation form the convention offers, and it was the
            # only one whose precision was not checked: the resolver split the line number off
            # and asked whether the *file* existed, so `store.py:412` resolved for ever against a
            # forty-line file. It is the pointer most likely to go stale — code moves — and the
            # one a reader is least likely to re-check, because it looks exact (F-077).
            rest = citation[len(candidate):]
            match = PATH_LINE_RE.match(rest)
            if match and os.path.isfile(target):
                wanted = int(match.group(1))
                with open(target, "r", encoding="utf-8", errors="replace") as handle:
                    lines = sum(1 for _ in handle)
                if wanted > max(lines, 1):
                    return (f"{citation} points past the end of the file, which has "
                            f"{lines} line{'' if lines == 1 else 's'}")
            return ""

        return (f"{citation!r} is not a citation form this gate can check "
                f"(spec/doc-header.md, the citation forms table)")

    def _resolve_criterion(self, item_id: str, label: str, anchor) -> str:
        """`ITEM ACn`, and what makes it point at the same criterion tomorrow (F-094).

        The number is a **position in a list**, not a name. Criteria may legally be renumbered
        while an item is being refined, and when they are, every standing `ITEM ACn` citation
        goes on resolving against whatever has moved into that position — a citation that still
        resolves is worse than one that fails, because the gate reports success.

        This is F-077's disease and **not** F-077's cure. There the fix was a bound: a
        `path:line` citation is checked against the file's length, so a pointer past the end
        stops resolving. The equivalent bound here — *does the item declare an ACn?* — is the
        check that was already in place, and it is exactly the one being fooled. A bound cannot
        tell a moved target from a standing one; only the target's own content can. So the
        citation may carry that content, quoted, and two rules follow:

          * an **anchored** citation is checked against the criterion's words, at any status —
            renumber, and it fails loudly instead of resolving quietly;
          * an **unanchored** citation is refused while the cited item is at a status where the
            list may still be rewritten, because there the number has not yet become an identity.

        Past that point an unanchored citation still resolves, and the residue is stated where
        the rule is (`spec/doc-header.md` §4a) rather than left for a reader to discover: a
        criterion edited by `answer-questions` propagating an answer can still move under an
        unanchored citation, and nothing here detects it.
        """
        record = self.items.get(item_id)
        if record is None:
            return f"{item_id} is not an item in this workspace"
        criterion = None
        for found in criteria_in(record["body"]):
            if found["label"] == label:
                criterion = found["text"]
                break
        if criterion is None:
            return f"{item_id} has no {label}"

        if anchor is not None:
            if normalise_anchor(anchor) in normalise_anchor(criterion):
                return ""
            return (f"{item_id} {label} does not say {anchor.strip()!r} — it reads "
                    f"{_shorten(criterion)!r}. A criterion cited by number moves when the list "
                    f"is renumbered; the quoted words are the part that does not move")

        status = record["status"]
        if status in AC_RENUMBERABLE_STATUSES:
            return (f"{item_id} is at {status}, where its criteria may still be renumbered, so "
                    f"{label!r} does not yet name one — quote the criterion's words too, as "
                    f"[src: {item_id} {label} \"{_shorten(criterion, words=6)}\"]")
        return ""

    def problems_in(self, text: str):
        """(line, message) for every citation in `text` that does not resolve.

        A marker inside an inline code span or a fenced block is a **quotation**, not a citation,
        and is skipped. F-037: without this, a journal entry could not describe a malformed
        citation without reproducing it — and since `journal.md` is append-only, the only way to
        satisfy the linter was to rewrite an entry, which is the one thing the audit trail forbids.
        A rule that forces a record to break the append-only invariant is worse than no rule.
        """
        found = []
        # F-054: masking protects a *quoted* citation from being read as one (F-037), and it also
        # blanked the inside of a real citation whose path was written in backticks — which is how
        # this repository's prose writes every path. The author got "an empty citation" and went
        # looking for a stray marker rather than a stray backtick. Masking preserves offsets, so a
        # marker that survives in the masked line is a real one, and its body is read from the raw
        # line where the backticks still are.
        raw_lines = text.split("\n")
        for index, line in enumerate(masked_lines(text), start=1):
            raw = raw_lines[index - 1] if index - 1 < len(raw_lines) else line
            for match in CITATION_RE.finditer(raw):
                if line[match.start():match.start() + 5] != "[src:":
                    continue        # the whole marker sits inside a code span: a quotation
                for part in split_sources(match.group("body")):
                    problem = self.resolve(part)
                    if problem:
                        found.append((index, problem))
        return found
