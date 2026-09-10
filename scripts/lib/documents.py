"""What a document obligation is *about*, read once, for every gate that decides one.

`ADR-0010` derives twenty obligations from one question — who may write a sentence in a
document, and what they owe when they do — and marks twelve of them `[auto]`. Eight of those
twelve had no implementation and were written into six skill contracts as `manual_check`, which
is the shape this project exists to distrust: an instruction is a gate nobody runs (ROADMAP §1,
F-001).

This module is the reading half. It knows four things and judges none of them:

  * the **invalidation set** as rows rather than paths — `scripts/lib/workspace.py` parses the
    table, this module says which cells are enums and what the enums are (§5.1);
  * the **`## Engagement state` section** — where it is in a document, whether a document has
    more than one, and what its text was at some earlier commit (§4.3);
  * a **quantified** sentence — the subset of the absolutes that ranges over a family, which is
    the kind whose obligation a citation cannot discharge (§4.2);
  * the **enumeration entry** that discharges one, as a shape a script can find.

`scripts/lint-documents` holds the rules and does the reporting, exactly as `lint-claims` stands
on `claims.py`. Two implementations of "is this disposition legal" would disagree eventually and
the disagreement would surface as a gate that passes work another gate refuses.

**What this module cannot see, said here rather than discovered later.** ADR-0010's obligation 10
— whether a sentence that *is* an engagement-state claim was written **into** the section rather
than left loose in the body — has no mechanical half at all, and everything here that reads a
`## Engagement state` section rests on somebody having put the sentence in one. F-093's own
sentence was written loose. Nothing in this file detects that, and no caller may spell its result
as though it did.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import os
import re
import subprocess

from claims import CODE_TOKEN_RE, looks_like_code  # noqa: E402
from record import HEADING_RE, blocks, paragraphs, sections as split_sections  # noqa: E402
from textio import read_text  # noqa: E402
import frontmatter  # noqa: E402

__all__ = [
    "KINDS", "DISPOSITIONS", "OPEN_DISPOSITION_RE", "ADR_VERDICTS", "ENGAGEMENT_SECTION",
    "ENUMERATION_LABEL", "ENUMERATION_PARTS", "NO_MEMBERS_RE", "Enumeration",
    "EngagementSection",
    "document_body", "documents_under", "engagement_sections", "engagement_state_text",
    "quantified_paragraphs", "enumerations_in", "artifact_rows", "artifact_section",
    "show", "new_paragraphs", "ADR_ID_RE", "QUESTION_DISPOSITION_RE", "QUANTIFIER_RE",
]

# ADR-0010 §5.1. `kind` is what the sentence is about; `disposition` is what happened to it.
KINDS = ("cited-fact", "quantified", "engagement-state")
DISPOSITIONS = ("to-update", "verified-still-true", "owned-by-ending")
QUESTION_DISPOSITION_RE = re.compile(
    r"^question-filed:\s*(EP-\d{3}|WI-\d{4}|BUG-\d{4})/Q-\d{3}$")
# `plan` fills four columns and *leaves the disposition open* for `implement`
# [src: methodology/skills/plan/process.md]. So the plan-shape rule and the disposal rule read
# the same cell against different alphabets: an open marker is a legal answer at `planned` and
# an unclosed entry at `verifying`. Collapsing the two is how a gate ends up demanding, at the
# stage that writes the row, the answer only the next stage can give.
OPEN_DISPOSITION_RE = re.compile(r"^(|-|–|—|open|tbd|todo|\.\.\.)$", re.IGNORECASE)

ADR_VERDICTS = ("conforms", "violates", "not-engaged")
ADR_ID_RE = re.compile(r"\bADR-\d{4}\b")

ENGAGEMENT_SECTION = "## Engagement state"

# The enumeration entry's shape. `spec/doc-header.md` §4a names the five things a quantified
# claim's audit row records — (a) the set, (b) how the set was enumerated, with the command's
# output, (c) the members by name, (d) the verdict per member, (e) the falsifier: what a member
# that made the sentence false would look like, and why the members examined could have exhibited
# one. A shape check needs those five to be *findable*, so they are written as labels, the way
# ADR-0008 §4 made `Checked against:` the findable half of the cross-answer check. Without a label
# nothing mechanical can tell "I opened the fixture" from "I enumerated the members", and telling
# those two apart is the whole of F-095.
#
# `falsifier` is F-088's part and it is last on purpose: the other four say what was looked at,
# and this one says whether looking there could have produced a `false`. A row without it records
# a verdict and destroys the method, which is the sentence §4a already used about "I read it and
# it is true" — the label is that sentence made findable.
ENUMERATION_LABEL = "enumeration"
ENUMERATION_PARTS = ("set", "enumerated by", "members", "verdict", "falsifier")

# What `Members:` has to *say* for the enumeration to have been able to fail. An audit over a set
# with no members is the audit-row form of `scope.py`'s out-of-scope-by-construction: it did not
# come up empty, it could not have come up otherwise. Recognised, marked, and passed — never
# failed, because a family that is genuinely empty makes the sentence vacuously true and the
# legal repair for that is to weaken the sentence, which is a read (F-088, F-076).
NO_MEMBERS_RE = re.compile(r"^(|-|–|—|none|nothing|n/?a|empty|no members)[.\s]*$", re.IGNORECASE)

# The quantifiers, which are a *subset* of the absolutes `lint-claims` detects. `never`,
# `cannot`, `always` and `guaranteed` are absolutes about a named thing — cited facts, whose
# obligation is the citation. Demanding an enumeration for those would be demanding the wrong
# evidence, loudly, on sentences that already carry the right evidence (ADR-0010 §4.1 vs §4.2).
QUANTIFIER_RE = re.compile(r"(?<![\w-])(every|all|no|none|only|each)(?![\w-])", re.IGNORECASE)


class EngagementSection:
    """One `## Engagement state` section, and where it is."""

    __slots__ = ("path", "line", "text", "count")

    def __init__(self, path, line, text, count) -> None:
        self.path = path
        self.line = line
        self.text = text
        self.count = count          # how many such sections this document has

    @property
    def empty(self) -> bool:
        return not self.text.strip()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"EngagementSection({self.path!r}, line={self.line}, count={self.count})"


class Enumeration:
    """An enumeration entry found in an audit row, and which of its five parts are present."""

    __slots__ = ("path", "line", "document", "parts", "text", "values")

    def __init__(self, path, line, document, parts, text, values=None) -> None:
        self.path = path
        self.line = line
        self.document = document
        self.parts = set(parts)
        self.text = text
        # label -> what it said, for the one part whose *content* is decidable (F-088).
        self.values = dict(values or {})

    @property
    def missing(self) -> list:
        return [part for part in ENUMERATION_PARTS if part not in self.parts]

    @property
    def complete(self) -> bool:
        return not self.missing

    @property
    def vacuous(self) -> bool:
        """`Members:` names nobody, so no counterexample could have turned up (F-088).

        Not a failure and not an ordinary pass. The caller marks it; the read it leaves open —
        whether a family with no members means the sentence should be weakened — is a person's.
        """
        return "members" in self.parts and bool(
            NO_MEMBERS_RE.match(self.values.get("members", "").strip()))

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Enumeration({self.document!r}, line={self.line}, missing={self.missing})"


def document_body(text: str, name: str = ""):
    """(body, first-line) with the frontmatter split off, or the whole text when there is none."""
    try:
        _, body, line = frontmatter.split(text, name=name)
        return body, line
    except Exception:
        return text, 1


def documents_under(root: str, subdir: str = "docs"):
    """(relative-path, text) for every markdown document under `<root>/<subdir>`."""
    base = os.path.join(root, subdir)
    found = []
    if not os.path.isdir(base):
        return found
    for where, dirs, files in os.walk(base):
        dirs[:] = [entry for entry in dirs if not entry.startswith(".")]
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(where, name)
            found.append((os.path.relpath(path, root).replace(os.sep, "/"),
                          read_text(path)[0]))
    return sorted(found)


def _count_headings(body: str, heading: str) -> int:
    wanted = heading.strip().lower()
    total = 0
    for raw in body.split("\n"):
        match = HEADING_RE.match(raw)
        if match and len(match.group(1)) == 2:
            if ("## " + match.group(2).strip()).lower() == wanted:
                total += 1
    return total


def engagement_state_text(text: str, name: str = ""):
    """The `## Engagement state` section of one document, or None.

    Returns `(section-text, line, count)`. `count` is how many such sections the document holds:
    the convention is **exactly one per document** so that the set of them in a workspace is
    enumerable, and a second one is a defect a reader would never see (`spec/doc-header.md` §4a,
    and F-056 for why counting headings is not the same as looking one up in a dictionary).
    """
    body, first = document_body(text, name)
    count = _count_headings(body, ENGAGEMENT_SECTION)
    section = split_sections(body, first).get(ENGAGEMENT_SECTION)
    if section is None:
        return None, 0, count
    return section["text"], section["line"], count


def engagement_sections(root: str, subdir: str = "docs"):
    """Every `## Engagement state` section in the workspace, in path order.

    This is the enumeration ADR-0010 §4.3 rule 1 exists to make possible: the ending's job is
    bounded precisely because the sections are findable, and a `review-close` asked to re-read
    all of `docs/` at the ending is a gate that gets switched off (§8).
    """
    found = []
    for relative, text in documents_under(root, subdir):
        section, line, count = engagement_state_text(text, relative)
        if section is None:
            continue
        found.append(EngagementSection(relative, line, section, count))
    return found


def quantified_paragraphs(text: str, name: str = ""):
    """(line, paragraph, quantifier, token) for paragraphs making a quantified claim.

    A quantifier over something named as code — the same detection `lint-claims` rule 2 performs
    for absolutes, narrowed to the words that range over a family. ADR-0010's obligation 5 is
    honest about the reach and so is this: `every`, `all`, `no`, `only` and `each` catch most of
    them, and a universal phrased without one — *"each handler validates its input"* written as
    *"handlers validate their input"* — is caught by nothing here or anywhere else.
    """
    body, first = document_body(text, name)
    found = []
    for start, block in paragraphs(body, first):
        joined = "\n".join(block)
        if all(line.lstrip().startswith(("#", "|", ">")) for line in block):
            continue
        quantifier = QUANTIFIER_RE.search(joined)
        if not quantifier:
            continue
        tokens = [token for token in CODE_TOKEN_RE.findall(joined) if looks_like_code(token)]
        if not tokens:
            continue
        found.append((start, joined.strip(), quantifier.group(1), tokens[0]))
    return found


def enumerations_in(path: str, text: str, line: int):
    """Every enumeration entry in one audit section, with the document it hangs under.

    The association is by **nesting**, not by proximity: an `Enumeration:` block belongs to the
    nearest less-indented bullet above it, which is the bullet naming the file that was changed
    (`answer-questions`' `## Consequences` shape). Reading it any other way would let one
    enumeration under one document discharge a claim written into another.
    """
    found = []
    document = ""
    all_blocks = blocks(text, line)
    for position, block in enumerate(all_blocks):
        if block.kind not in ("bullet", "text"):
            continue
        label = (block.label or "").strip().lower()
        if label != ENUMERATION_LABEL:
            if block.indent == 0:
                match = re.search(r"[A-Za-z0-9_][A-Za-z0-9_./\-]*\.md", block.joined)
                document = match.group(0) if match else ""
            continue
        parts = set()
        values = {}
        body = [block]
        for following in all_blocks[position + 1:]:
            if following.indent <= block.indent:
                break
            body.append(following)
        for entry in body:
            entry_label = (entry.label or "").strip().lower()
            if entry_label in ENUMERATION_PARTS:
                parts.add(entry_label)
                values.setdefault(entry_label, entry.body)
        found.append(Enumeration(path, block.start, document, parts,
                                 " ".join(item.joined for item in body), values))
    return found


def artifact_section(root: str, item: str, artifact: str, heading: str):
    """One `## Section` of an item artifact — `(text, line)`, or `(None, 0)`.

    Item artifacts carry no frontmatter (`spec/workspace-layout.md`), so line 1 is line 1.
    """
    path = os.path.join(root, "tracker", "items", item, "artifacts", artifact)
    if not os.path.isfile(path):
        return None, 0
    text = read_text(path)[0]
    section = split_sections(text, 1).get(heading)
    if section is None:
        return None, 0
    return section["text"], section["line"]


def artifact_rows(root: str, item: str, artifact: str, heading: str):
    """(cells, line) for the pipe table under one heading of an item artifact."""
    from record import table_rows
    text, line = artifact_section(root, item, artifact, heading)
    if text is None:
        return None
    return table_rows(text, line)


def show(root: str, ref: str, relative: str):
    """The content of one path at `ref`, or None when it was not there (or git is not)."""
    try:
        result = subprocess.run(["git", "-C", root, "show", f"{ref}:{relative}"],
                                capture_output=True, text=True)
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def new_paragraphs(before: str, after: str, name: str = ""):
    """Paragraphs present in `after` that are not, verbatim, in `before`.

    "What this execution wrote" as a diff can be answered two ways and only one of them is fair.
    Reading *every* paragraph of a changed document charges an execution with sentences it
    inherited — the shape CHECKPOINT's edge (a) is about, a defect with no legal repair. Reading
    only the paragraphs that are new charges it with what it actually put there. This is the same
    survival comparison `lint-answers` rule 3 performs, run the other way round.
    """
    body, first = document_body(after, name)
    if before is None:
        old = set()
    else:
        old_body, _ = document_body(before, name)
        old = {"\n".join(block).strip() for _, block in paragraphs(old_body)}
    found = []
    for start, block in paragraphs(body, first):
        joined = "\n".join(block).strip()
        if joined in old:
            continue
        found.append((start, joined))
    return found
