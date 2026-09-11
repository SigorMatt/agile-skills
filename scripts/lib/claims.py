"""Claim provenance: the citation forms, whether one resolves, and whether it is one at all.

Shared by `scripts/lint-claims` (the gate) and `scripts/validate-workspace` (the resting-state
check), because two implementations of "does this citation resolve" would disagree eventually and
the disagreement would surface as a gate that passes on a record the validator rejects.

The same argument reaches one step further back, and did not used to (F-113, F-075). A marker
inside an inline code span or a fenced block is a **mention** of the form, not a use of it, and
that is decided in exactly one place: `masked_lines()`, read by `citations_in()` and by the
`carries_citation()` predicate over it. Every site that scrapes the vocabulary calls one of the
two. Where a bare `CITATION_RE` was used instead, the same class of defect appeared in whichever
direction the rule ran — a *resolution* rule refused a backticked example as a broken citation,
and a *presence* rule accepted one as a real one.

The mask is only half the answer, because a writer may reasonably name a form **without**
backticks, and one did: the run this is filed from ended on a history row that wrote `path:line`
bare, in prose, describing four citations it had just found falsified. So severity follows
knowledge as well — `Problem` splits a marker the resolver *checked* and rejected from one it
could not check at all, and the second is a warning, not a verdict.

The surfaces the vocabulary is read on, and the site that reads each (`record.py` holds the
structures they are cut out of — entries, table rows, list items, paragraphs):

  * every `*.md` body            `validate-workspace.check_claim_citations`, `lint-claims`
                                 rule 1 — `problems_in()`; resolution
  * a `docs/` prose paragraph    `lint-claims` rule 2 — `carries_citation()`; presence, a cited
                                 paragraph is exempt from the absolutes rule
  * a `docs/` prose paragraph    `lint-answers` rule 3 — `citations_in()`; which human answers
                                 a paragraph is sourced to, before it is rewritten
  * an acceptance-criterion      `validate-workspace.check_substituted_criterion` —
    list item                    `citations_in()`; presence of a question on this
                                 item (F-096)
  * an ADR `## Corrections` row  `validate-workspace.check_adr_corrections` —
                                 `carries_citation()`; presence (doc-header.md §4b)
  * a retro report `###` entry   `lint-retro.check_citations` — `citations_in()`;
                                 presence and resolution

A citation also has a **boundary**, and it is the walk's own (ADR-0013). The two `*.md` walks
above prune `.git`, `__pycache__`, `.claude` and `node_modules`; by the tool's own definition
nothing in those is part of the record, so `_resolve` refuses a citation that points into one —
`claim.citation.outside-the-record`, an ERROR, because the gate knows both what is wrong and what
to write instead. `PRUNED_DIRS` is read by the walks and by the resolver so the rule and the
exclusion cannot come apart. The installed toolkit is the case that forced the ruling: twelve
`[src: .claude/agile-skills/...]` citations resolved by `os.path.exists` in a real run and every
one of them stopped resolving the moment the record left the machine. Its replacement is the
`toolkit:` form, which carries its evidence inside the marker instead.

`arose-from` is deliberately not in that list: it is a frontmatter scalar, not prose, so there is
no code span to mask and `check_provenance` resolves it against the tree directly.

The convention itself is specified in `spec/doc-header.md`. Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import re
import subprocess

import frontmatter  # noqa: E402
from record import FENCE_RE  # noqa: E402
from textio import read_text  # noqa: E402

__all__ = ["CITATION_RE", "ABSOLUTE_RE", "CODE_TOKEN_RE", "CitationResolver", "Problem",
           "AC_LINE_RE", "AC_RENUMBERABLE_STATUSES", "ac_state", "criteria_in",
           "normalise_anchor", "carries_citation", "citations_in",
           "looks_like_code", "mask_code", "masked_lines", "split_sources",
           "PRUNED_DIRS", "TOOLKIT_RE", "pruned_segment"]

# The directories the record walk prunes. Stated once, because two sites read it for opposite
# purposes and they must not drift apart (ADR-0013): `validate-workspace.check_claim_citations`
# and `lint-claims.all_markdown` skip these when they walk a workspace looking for citations, and
# `CitationResolver._resolve` refuses a citation that points inside one. A citation may not point
# where the record does not go — if the walk will not open the directory, nothing in it is
# evidence a reader can check, and `os.path.exists` there answers a question about the machine the
# citation was written on rather than a question about the record.
PRUNED_DIRS = (".git", "__pycache__", ".claude", "node_modules")

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
# `toolkit: <document> <section> "<quoted words>"` — how a record cites the toolkit that is
# running it (ADR-0013). The toolkit is installed outside the record and upgrades underneath it,
# so this citation carries its evidence *inside* the marker rather than pointing at a file:
# `<document>` is how the toolkit document names itself and is never resolved against the
# filesystem, `<section>` is everything between it and the quote, and the quoted words are
# mandatory and non-empty. Like the acceptance-criterion anchor, the quote may contain neither
# `]` (it ends the marker) nor `;` (it separates sources).
TOOLKIT_RE = re.compile(r"^toolkit:\s*(?P<document>\S+)\s+(?P<section>.+?)\s*"
                        r"[\"\u201c](?P<words>[^\"\u201d]*)[\"\u201d]\s*$")
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


def citations_in(text: str, first_line: int = 1):
    """Every marker in `text` that is a **use** of the citation form, as (line, body).

    One reader for every surface, because "is this a citation or an example of one" is one
    question and two answers to it is F-113: a rule that wants a real citation was satisfied by a
    backticked example, while a rule that checks citations refused the same example as a broken
    one — the same defect, once in each direction, on surfaces that sit a few lines apart.

    F-054: masking protects a *quoted* citation from being read as one (F-037), and it also
    blanks the inside of a real citation whose path is written in backticks — which is how this
    repository's prose writes every path. The author got "an empty citation" and went looking for
    a stray marker rather than a stray backtick. Masking preserves offsets, so a marker that
    survives in the masked line is a real one, and its body is read from the raw line where the
    backticks still are. Every caller gets that discipline by calling this rather than
    reimplementing it; `lint-retro` had reimplemented half of it and reported the empty citation.

    `first_line` numbers the first line of `text`, for a caller reporting into a larger file.
    """
    found = []
    raw_lines = text.split("\n")
    for index, line in enumerate(masked_lines(text), start=first_line):
        raw = raw_lines[index - first_line] if index - first_line < len(raw_lines) else line
        for match in CITATION_RE.finditer(raw):
            if line[match.start():match.start() + 5] != "[src:":
                continue            # the whole marker sits inside a code span: a quotation
            found.append((index, match.group("body")))
    return found


def carries_citation(text: str) -> bool:
    """Does `text` cite anything at all?

    The predicate every *presence* rule asks. It has to be this one and not `CITATION_RE.search`,
    or a requirement to cite something is satisfied by prose that merely shows what a citation
    looks like — which is the reading a record most likely to explain the convention (a
    retrospective, an ADR correction, a criterion saying why it was substituted) is most likely
    to produce.
    """
    return bool(citations_in(text))


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


def pruned_segment(path: str):
    """The first segment of `path` that the record walk prunes, or None.

    Read by the resolver, and by nothing else that has to re-derive it. Any segment, at any
    depth: `os.walk` prunes the directory wherever it appears, so `a/b/node_modules/c` is as far
    outside the record as `node_modules/c` is.
    """
    for segment in path.replace("\\", "/").split("/"):
        if segment in PRUNED_DIRS:
            return segment
    return None


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


class Problem:
    """One citation that did not check out, and **which kind** of not-checking-out it is.

    Severity follows knowledge (F-113, F-075). A body that matches a known citation form and
    fails to resolve is a wrong citation: the gate looked, and the appearance of evidence is
    worse than none, so it is an ERROR. A body that matches no form at all is a different fact —
    the gate has not looked at anything, and it cannot tell a **mention** of the form from a typo
    in a citation. Reporting that as an error is the gate announcing a verdict it does not hold,
    and it is how an engagement ended at turn 11: a history row naming the form `path:line` in
    prose, in a sentence about four citations the same skill had just found falsified.

    The kind, the severity and the code all live here and nowhere else. A caller that re-derived
    "was this recognised?" from the message text would be the two-readers-one-vocabulary defect
    this module exists to prevent — so `report()` files the finding and the caller supplies only
    its own code namespace (`claim` for the two claim gates, `retro` for the retrospective one),
    because the two name their findings differently and the split is the same in both.
    """

    UNRESOLVED = "unresolved"
    UNRECOGNISED = "unrecognised"
    # A third kind, and an ERROR like the first (ADR-0013). The gate knows exactly what is wrong
    # *and* what to write instead, so there is none of the mention-vs-typo ambiguity that makes
    # UNRECOGNISED a warning. It is not UNRESOLVED either, because "does not exist in this
    # workspace" is the wrong sentence: the file may exist perfectly well on the machine the
    # citation was written on, and that is the problem rather than the exception to it.
    OUTSIDE = "outside-the-record"

    __slots__ = ("kind", "message")

    def __init__(self, kind: str, message: str) -> None:
        self.kind = kind
        self.message = message

    def __repr__(self) -> str:
        return f"Problem({self.kind!r}, {self.message!r})"

    def __eq__(self, other) -> bool:
        return (isinstance(other, Problem) and other.kind == self.kind
                and other.message == self.message)

    def __hash__(self):
        return hash((self.kind, self.message))

    @classmethod
    def unresolved(cls, message: str) -> "Problem":
        """A known form that does not resolve. The gate looked."""
        return cls(cls.UNRESOLVED, message)

    @classmethod
    def outside_the_record(cls, citation: str, directory: str) -> "Problem":
        """A path into a directory the record walk prunes. The gate looked, and it knows the fix."""
        return cls(cls.OUTSIDE,
                   f"{citation!r} points inside {directory!r}, which the walk that reads this "
                   f"record prunes — so it is not part of the record, and whether the file is "
                   f"there is a fact about this machine rather than about the record. Quote the "
                   f"source instead of pointing at it: for the toolkit, "
                   f"[src: toolkit: <document> <section> \"<quoted words>\"]")

    @classmethod
    def unrecognised(cls, citation: str) -> "Problem":
        """No form at all. The gate did not look, and says so instead of ruling."""
        return cls(cls.UNRECOGNISED,
                   f"{citation!r} matches no citation form, so this gate cannot tell a mention "
                   f"of one from a typo in one — put it in backticks if it is naming the form, "
                   f"or write one of the forms in spec/doc-header.md's citation forms table if "
                   f"it is a citation")

    def report(self, report, path, line, namespace: str, prefix: str = "") -> None:
        """File this problem on `report` as `<namespace>.citation.<kind>`, at its own level."""
        code = f"{namespace}.citation.{self.kind}"
        message = f"{prefix}{self.message}"
        if self.kind == self.UNRECOGNISED:
            report.warn(path, line, code, message,
                        hint="a warning, because nothing was checked: only a marker that "
                             "matches a form and then fails is an error")
            return
        if self.kind == self.OUTSIDE:
            report.error(path, line, code, message,
                         hint="an error rather than a warning: the gate knows what is wrong and "
                              "what to write instead, so there is nothing here it cannot tell "
                              "apart (spec/doc-header.md, the citation forms table)")
            return
        report.error(path, line, code, message,
                     hint="a citation that does not resolve is the appearance of evidence, "
                          "which is worse than none")


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

    def resolve(self, citation: str):
        """The `Problem` with this citation, or None when it resolves."""
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
            # `[src: ]` is a citation, not a mention of one: the marker was made in prose and
            # left empty. The gate knows that much, so this keeps the error severity.
            return Problem.unresolved("an empty citation")
        problem = self._resolve(citation)
        if problem and repeated_prefix:
            return Problem(problem.kind,
                           f"{problem.message} — note that {raw.strip()!r} repeats the 'src:' "
                           f"prefix; inside one marker, sources are separated by ';' and only "
                           f"the first carries it")
        return problem

    def _resolve(self, citation: str):

        if RUN_RE.match(citation):
            return None
        if citation.lower().startswith("run:"):
            # `run:` names the form, so this is a citation and not a mention of one, and the
            # gate can say exactly what is missing. Without this the split below would file it
            # as unrecognised — a warning — and a command citation with its outcome dropped is
            # the one that loses the most evidence (F-070).
            return Problem.unresolved(
                f"{citation!r} records a command with no outcome — a run citation is "
                f"'run: <command> → <outcome>'")

        if citation.lower().startswith("toolkit:"):
            # Same reasoning as `run:` above: naming the form is enough to make this a citation
            # rather than a mention of one, so an incomplete `toolkit:` body is an error with a
            # message that says what is missing, not an unrecognised-marker warning.
            return self._resolve_toolkit(citation)

        match = COMMIT_RE.match(citation)
        if match:
            result = self.git(["cat-file", "-e", f"{match.group(1)}^{{commit}}"])
            if result is None:
                return Problem.unresolved(f"{citation!r} cannot be checked — this workspace is "
                                          f"not a git repository")
            if result.returncode != 0:
                return Problem.unresolved(f"commit {match.group(1)} is not in this repository")
            return None

        match = ITEM_QUESTION_RE.match(citation)
        if match:
            path = os.path.join(self.root, "tracker", "items", match.group(1), "questions",
                                f"{match.group(2)}.md")
            return None if os.path.isfile(path) \
                else Problem.unresolved(f"{citation} does not exist")

        match = ITEM_AC_RE.match(citation)
        if match:
            return self._resolve_criterion(match.group(1), match.group(2),
                                           match.group("anchor"))

        if ITEM_RE.match(citation):
            return None if citation in self.items \
                else Problem.unresolved(f"{citation} is not an item in this workspace")

        match = ADR_RE.match(citation)
        if match:
            adr_dir = os.path.join(self.root, "docs", "architecture", "adr")
            if os.path.isdir(adr_dir):
                for name in os.listdir(adr_dir):
                    if name.startswith(f"ADR-{match.group(1)}-"):
                        return None
            return Problem.unresolved(f"{citation} is not an ADR in "
                                      f"docs/architecture/adr/")

        candidate = citation.split(":")[0].split(" ")[0]
        if "/" in candidate or "." in candidate:
            # ADR-0013. Before asking whether the file is there, ask whether the record goes
            # there at all. `PRUNED_DIRS` is the walk's own list, read from the one place it is
            # written, so the rule and the exclusion cannot drift apart: the installed toolkit
            # under `.claude/` is the case that made this a ruling, and `.git`,
            # `__pycache__` and `node_modules` are outside the record for the same reason.
            pruned = pruned_segment(candidate)
            if pruned is not None:
                return Problem.outside_the_record(citation, pruned)
            target = os.path.join(self.root, candidate)
            if not os.path.exists(target):
                return Problem.unresolved(f"{candidate!r} does not exist in this workspace")
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
                    return Problem.unresolved(
                        f"{citation} points past the end of the file, which has "
                        f"{lines} line{'' if lines == 1 else 's'}")
            return None

        return Problem.unrecognised(citation)

    def _resolve_toolkit(self, citation: str):
        """`toolkit: <document> <section> "<quoted words>"` — resolves when the shape is complete.

        Said plainly, because the honest boundary is narrow: this gate **cannot** tell whether the
        toolkit really says those words. Nothing here opens a file — the toolkit is installed
        outside the record, it upgrades underneath a record that is not allowed to become
        retroactively invalid (`spec/doc-header.md` §4a), and a version pin would make every
        standing citation fail on the next upgrade. What is checked is that the citation carries
        enough for a **reader** to check it: which document, which section, and the words claimed.

        That is strictly more than the path form it replaces carried. `[src: .claude/agile-skills/
        spec/dor-dod.md]` was checked by `os.path.exists` in a directory the record walk prunes,
        so it verified the writer's own installation and nothing else, and a reader who received
        the record could not follow it at all.
        """
        match = TOOLKIT_RE.match(citation)
        if match is None:
            return Problem.unresolved(
                f"{citation!r} names the toolkit form and does not complete it — a toolkit "
                f"citation is 'toolkit: <document> <section> \"<quoted words>\"', and all three "
                f"parts are required because nothing here is looked up")
        if not match.group("words").strip():
            return Problem.unresolved(
                f"{citation!r} quotes nothing — the quoted words are the whole of the "
                f"evidence a toolkit citation carries, so an empty quote is the appearance of "
                f"one")
        return None

    def _resolve_criterion(self, item_id: str, label: str, anchor):
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
            return Problem.unresolved(f"{item_id} is not an item in this workspace")
        criterion = None
        for found in criteria_in(record["body"]):
            if found["label"] == label:
                criterion = found["text"]
                break
        if criterion is None:
            return Problem.unresolved(f"{item_id} has no {label}")

        if anchor is not None:
            if normalise_anchor(anchor) in normalise_anchor(criterion):
                return None
            return Problem.unresolved(
                f"{item_id} {label} does not say {anchor.strip()!r} — it reads "
                f"{_shorten(criterion)!r}. A criterion cited by number moves when the list "
                f"is renumbered; the quoted words are the part that does not move")

        status = record["status"]
        if status in AC_RENUMBERABLE_STATUSES:
            return Problem.unresolved(
                f"{item_id} is at {status}, where its criteria may still be renumbered, so "
                f"{label!r} does not yet name one — quote the criterion's words too, as "
                f"[src: {item_id} {label} \"{_shorten(criterion, words=6)}\"]")
        return None

    def problems_in(self, text: str):
        """(line, `Problem`) for every citation in `text` that does not check out.

        The `Problem` carries its own severity and code, so all three callers report the same
        split without any of them re-deriving it (F-113): a marker matching a known form and
        failing is an error, and a marker matching no form is a warning, because the gate cannot
        tell a mention of a form from a typo in a citation.

        A marker inside an inline code span or a fenced block is a **quotation**, not a citation,
        and `citations_in()` has already dropped it. F-037: without that, a journal entry could
        not describe a malformed citation without reproducing it — and since `journal.md` is
        append-only, the only way to satisfy the linter was to rewrite an entry, which is the one
        thing the audit trail forbids. A rule that forces a record to break the append-only
        invariant is worse than no rule.
        """
        found = []
        for line, body in citations_in(text):
            for part in split_sources(body):
                problem = self.resolve(part)
                if problem is not None:
                    found.append((line, problem))
        return found
