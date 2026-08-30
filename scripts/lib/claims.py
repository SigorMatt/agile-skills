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

from textio import read_text  # noqa: E402

__all__ = ["CITATION_RE", "ABSOLUTE_RE", "CODE_TOKEN_RE", "CitationResolver",
           "looks_like_code", "paragraphs", "is_prose", "mask_code", "masked_lines"]

CITATION_RE = re.compile(r"\[src:\s*(?P<body>[^\]]+)\]")
CODE_SPAN_RE = re.compile(r"(`+)(?:(?!\1).)*?\1", re.DOTALL)
FENCE_RE = re.compile(r"^\s*(```|~~~)")

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
ITEM_AC_RE = re.compile(r"^(EP-\d{3}|WI-\d{4}|BUG-\d{4})\s+(AC\d+)$")
ITEM_QUESTION_RE = re.compile(r"^(EP-\d{3}|WI-\d{4}|BUG-\d{4})/(Q-\d{3})$")
ADR_RE = re.compile(r"^ADR-(\d{4})$")
COMMIT_RE = re.compile(r"^commit\s+([0-9a-f]{7,40})$")
RUN_RE = re.compile(r"^run:\s*(?P<command>.+?)\s*(?:→|->)\s*(?P<outcome>.+)$")
AC_LINE_RE = re.compile(r"^\s*-\s+\[( |x|X)\]\s+(AC\d+)\b")



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


def paragraphs(text: str):
    """(start-line, [lines]) for each prose paragraph, skipping fenced code."""
    lines = text.split("\n")
    found = []
    buffer, start, fenced = [], 0, False
    for index, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not line.strip():
            if buffer:
                found.append((start, buffer))
            buffer, start = [], 0
            continue
        if not buffer:
            start = index
        buffer.append(line)
    if buffer:
        found.append((start, buffer))
    return found


def is_prose(block: list) -> bool:
    """Headings, tables and list-only blocks are structure; claims live in sentences."""
    text = "\n".join(block)
    if all(line.lstrip().startswith(("#", "|", ">")) for line in block):
        return False
    return bool(text.strip())




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
        base = os.path.join(self.root, "tracker", "items")
        found = {}
        if not os.path.isdir(base):
            return found
        for name in sorted(os.listdir(base)):
            path = os.path.join(base, name, "item.md")
            if os.path.isfile(path):
                found[name] = read_text(path)[0]
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
            body = self.items.get(match.group(1))
            if body is None:
                return f"{match.group(1)} is not an item in this workspace"
            for line in body.split("\n"):
                found = AC_LINE_RE.match(line)
                if found and found.group(2) == match.group(2):
                    return ""
            return f"{match.group(1)} has no {match.group(2)}"

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
            if os.path.exists(os.path.join(self.root, candidate)):
                return ""
            return f"{candidate!r} does not exist in this workspace"

        return (f"{citation!r} is not a citation form this gate can check "
                f"(spec/doc-header.md, the citation forms table)")

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
