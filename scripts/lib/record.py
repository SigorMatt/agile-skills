"""The workspace's record *structures*, parsed once, in one place.

Every file this project's tools read is one of a small number of shapes: a document with
`## sections`, a section holding **blocks** (bullets, labelled declarations, paragraphs, tables,
fenced code), a pipe table of rows, and a log of **entries** — a heading followed by labelled
bullets, which is what `journal.md`, the findings ledger and a retro report all are.

Those shapes were being re-decided per script, and it went wrong twice in one session:

  * **F-069** tested whether a `## Corrections` section *exists* where the rule was about when it
    was written — a rule about a record's structure decided against a state.
  * **F-073** read a bullet to the next bullet, so a section's closing sentence was swallowed into
    the last entry and a gate failed on correct work; and read `Checked against:` as one line, so
    six of nine named answers were never examined and the gate passed over what it had not read.

`meta/FINAL-REPORT-3.md` §6.3 named the shape: *a rule about a record's structure, implemented
against lines or against a state.* This module is where that rule gets implemented once. Callers
ask for a block or an entry; they do not ask about lines. `scripts/lib/workspace.py` builds the
workspace's *domain* model (items, questions, documents) on top of it, and every lint reads the
same blocks the validator does.

Two granularities are exposed on purpose, and the difference between them is not accidental:

  * `blocks()` — the fine unit. A bullet **and its continuation lines** is one block; the next
    bullet is a different block. This is what a rule about "one entry in a list" needs.
  * `paragraphs()` — the coarse unit. Everything between two blank lines, fenced code skipped.
    This is what a rule about "a sentence a person wrote" needs, because a claim and the clause
    that qualifies it live in one paragraph however the author laid it out.

Line numbers are 1-based and every structure carries the line it starts on, so a finding can
point at the record rather than describe it. Standard library only (ADR-0002).
"""

from __future__ import annotations

import re

__all__ = [
    "Block", "Entry",
    "blocks", "paragraphs", "sections", "duplicate_headings", "table_rows", "entries",
    "labelled", "subtree", "split_row", "is_prose",
    "BULLET_RE", "HEADING_RE", "FENCE_RE", "TABLE_ROW_RE", "split_label",
]

# A list marker: `-`, `*`, or `1.` / `1)`. The marker set is deliberately small — a record whose
# lists need more shapes than this is prose pretending to be a structure.
BULLET_RE = re.compile(r"^(?P<indent>\s*)(?P<marker>[-*]|\d+[.)])\s+(?P<rest>.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_ROW_RE = re.compile(r"^\s*\|")
# `Label: value` — with or without the `**bold**` the record formats use, with the colon inside
# the bold markers or outside them, and with or without a list marker in front. The label is read
# off the text **before** the first colon, so `run: python3 -c "a: b"` in a value is never
# mistaken for a second label.
LABEL_CHARS_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 '/\-\u2014&()]*$")
LABEL_MAX = 60
_BOLD_RE = re.compile(r"\*\*|__")


def split_label(line: str):
    """`(label, value)` for a line that declares one, else `(None, None)`.

    The value is returned from the **raw** line — only the closing bold marker of a
    `**Label:**` is dropped — so a caller reading content is not handed a line this module
    quietly reformatted.
    """
    match = BULLET_RE.match(line)
    head = match.group("rest") if match else line.lstrip()
    colon = head.find(":")
    if colon <= 0:
        return None, None
    label = _BOLD_RE.sub("", head[:colon]).strip()
    if not label or len(label) > LABEL_MAX or not LABEL_CHARS_RE.match(label):
        return None, None
    value = head[colon + 1:]
    if value[:2] in ("**", "__"):
        value = value[2:]          # the closing marker of `**Label:**`
    if value and not value[:1].isspace():
        return None, None          # `http://x` is not a declaration
    return label, value.strip()


class Block:
    """One structural unit of a section, with the lines it actually occupies.

    `kind` is one of `bullet`, `text`, `table`, `fence`, `heading`. `label` is set when the
    block's first line reads `Label:` or `- **Label:**` — a bullet can be a labelled declaration
    and usually is, so the label is an attribute rather than a kind of its own.
    """

    __slots__ = ("kind", "lines", "start", "indent", "label", "marker")

    def __init__(self, kind, lines, start, indent=0, label=None, marker=None) -> None:
        self.kind = kind
        self.lines = list(lines)
        self.start = start
        self.indent = indent
        self.label = label
        self.marker = marker

    @property
    def end(self) -> int:
        """The last line this block occupies (1-based, inclusive)."""
        return self.start + len(self.lines) - 1

    @property
    def text(self) -> str:
        """Every line of the block, verbatim, newline-joined."""
        return "\n".join(self.lines)

    @property
    def joined(self) -> str:
        """The block as one line: continuations folded in, whitespace collapsed.

        This is what a rule that reads *content* wants. F-073's second half was a rule reading
        `Checked against:` off one line while the author had wrapped nine IDs over four; folding
        is the fix, and doing it here means no caller has to remember to.
        """
        return " ".join(line.strip() for line in self.lines if line.strip())

    @property
    def body(self) -> str:
        """A labelled block's value — everything after `Label:`, continuations folded in."""
        if self.label is None:
            return self.joined
        _, first = split_label(self.lines[0])
        first = first or ""
        rest = " ".join(line.strip() for line in self.lines[1:] if line.strip())
        return (first + " " + rest).strip() if rest else first

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (f"Block({self.kind!r}, start={self.start}, end={self.end}, "
                f"label={self.label!r})")


def blocks(text: str, first_line: int = 1):
    """Every block in `text`, in order, each carrying the lines it occupies.

    The rules, stated once so that no caller re-decides them:

    * a **bullet** starts at a list marker and continues through every following line that is
      indented further than the marker and is neither blank nor a bullet of its own. It ends at
      the next bullet (of any depth), a blank line, a heading, a fence, or prose that is not
      indented under it. A nested bullet is its own block; `subtree()` puts a parent back
      together with its children when a caller wants the pair.
    * a **paragraph** (`text`) runs until a blank line, a bullet, a heading, a fence or a table
      row. A labelled declaration is a paragraph with a label, so `Checked against: A; B` wrapped
      over four lines is one block, which is F-073's second half.
    * a **table** is a run of consecutive `|` rows; a **fence** is everything between two fence
      markers, kept whole and never read as prose.
    """
    found = []
    lines = text.split("\n")
    index = 0
    total = len(lines)
    while index < total:
        raw = lines[index]
        number = first_line + index

        if not raw.strip():
            index += 1
            continue

        if FENCE_RE.match(raw):
            body = [raw]
            index += 1
            while index < total:
                body.append(lines[index])
                closed = FENCE_RE.match(lines[index])
                index += 1
                if closed:
                    break
            found.append(Block("fence", body, number))
            continue

        heading = HEADING_RE.match(raw)
        if heading:
            found.append(Block("heading", [raw], number, indent=len(heading.group(1))))
            index += 1
            continue

        if TABLE_ROW_RE.match(raw):
            body = []
            while index < total and TABLE_ROW_RE.match(lines[index]):
                body.append(lines[index])
                index += 1
            found.append(Block("table", body, number))
            continue

        bullet = BULLET_RE.match(raw)
        if bullet:
            indent = len(bullet.group("indent"))
            body = [raw]
            index += 1
            while index < total:
                nxt = lines[index]
                if not nxt.strip():
                    break
                if BULLET_RE.match(nxt) or HEADING_RE.match(nxt) or FENCE_RE.match(nxt):
                    break
                if len(nxt) - len(nxt.lstrip()) <= indent:
                    break            # prose that is not a continuation of this bullet
                body.append(nxt)
                index += 1
            found.append(Block("bullet", body, number, indent=indent,
                               label=split_label(raw)[0], marker=bullet.group("marker")))
            continue

        body = [raw]
        indent = len(raw) - len(raw.lstrip())
        index += 1
        while index < total:
            nxt = lines[index]
            if not nxt.strip():
                break
            if (BULLET_RE.match(nxt) or HEADING_RE.match(nxt) or FENCE_RE.match(nxt)
                    or TABLE_ROW_RE.match(nxt)):
                break
            body.append(nxt)
            index += 1
        found.append(Block("text", body, number, indent=indent, label=split_label(raw)[0]))
    return found


def subtree(block_list: list, position: int):
    """`block_list[position]` together with every block nested under it.

    A journal's `- **Decisions:**` bullet is a label whose content is the bullets beneath it;
    reading the label's own line answers nothing.
    """
    parent = block_list[position]
    collected = [parent]
    for block in block_list[position + 1:]:
        if block.indent > parent.indent:
            collected.append(block)
            continue
        break
    return collected


def labelled(block_list: list):
    """`{label: [blocks]}` — every labelled block, keyed by label, in order of appearance.

    A list, not a single block: a record may legitimately declare the same label twice, and the
    dictionary that silently keeps the last one is F-056's mistake at block scope.
    """
    found = {}
    for block in block_list:
        if block.label:
            found.setdefault(block.label, []).append(block)
    return found


def paragraphs(text: str, first_line: int = 1):
    """(start-line, [lines]) for each blank-line-separated chunk, skipping fenced code.

    The coarse unit. A claim and the clause qualifying it belong to one paragraph however the
    author wrapped it, so this deliberately does **not** split on bullets: a rule reading
    sentences wants the sentence, and `is_prose()` is how a caller drops the chunks that are
    structure rather than prose.
    """
    lines = text.split("\n")
    found = []
    buffer, start, fenced = [], 0, False
    for index, line in enumerate(lines, start=first_line):
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
    """Headings, tables and quote blocks are structure; claims live in sentences."""
    text = "\n".join(block)
    if all(line.lstrip().startswith(("#", "|", ">")) for line in block):
        return False
    return bool(text.strip())


def sections(body: str, first_line: int, level: int = 2):
    """`{'## Heading': {'text', 'line'}}` for headings at exactly `level`.

    `line` is the heading's own line; `text` is everything up to the next heading at that level,
    which is what a rule scoped to a section must read.
    """
    found = {}
    current = None
    buffer = []
    line_number = first_line
    prefix = "#" * level + " "
    for raw in body.split("\n"):
        match = HEADING_RE.match(raw)
        if match and len(match.group(1)) == level:
            if current is not None:
                found[current]["text"] = "\n".join(buffer)
            current = prefix + match.group(2).strip()
            found[current] = {"text": "", "line": line_number}
            buffer = []
        elif current is not None:
            buffer.append(raw)
        line_number += 1
    if current is not None:
        found[current]["text"] = "\n".join(buffer)
    return found


def duplicate_headings(body: str, first_line: int = 0, level: int = 2):
    """(heading, line) for every heading at `level` that appears more than once.

    F-056: `sections()` keys a dict on the heading, so a second `## Notes` silently replaces the
    first and every reader — the validator included — sees one of them. A real edit produced
    exactly that: an item spliced against the wrong anchor grew three `## Notes` sections, the
    workspace validated clean, and it was caught only by a human re-reading the whole file. A
    document that reads correctly in one place and wrongly in another is the F-001 shape in
    miniature.
    """
    seen, repeated = {}, []
    line_number = first_line
    prefix = "#" * level + " "
    for raw in body.split("\n"):
        match = HEADING_RE.match(raw)
        if match and len(match.group(1)) == level:
            heading = prefix + match.group(2).strip()
            if heading in seen:
                repeated.append((heading, line_number))
            else:
                seen[heading] = line_number
        line_number += 1
    return repeated


def split_row(line: str):
    """Cells of a markdown table row, splitting on **unescaped** pipes only (F-044).

    `history.md` is a table and a `reason` is prose, so a reason naming a union type — `str |
    None` — used to split its row into extra cells. The writer escapes the pipe; this is the
    reader that understands the escape. Without both halves the escape is decoration: the row
    renders correctly and parses wrong, which is how the corruption stayed invisible until the
    validator failed on something that looked fine.
    """
    cells, current, index = [], [], 0
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|"):
        stripped = stripped[:-1]
    while index < len(stripped):
        character = stripped[index]
        if character == "\\" and index + 1 < len(stripped):
            following = stripped[index + 1]
            if following in ("|", "\\"):
                current.append(following)
                index += 2
                continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
            index += 1
            continue
        current.append(character)
        index += 1
    cells.append("".join(current).strip())
    return cells


def table_rows(text: str, first_line: int):
    """(cells, line) for every data row of a pipe table — header and separator dropped."""
    rows = []
    line_number = first_line
    seen_header = False
    for raw in text.split("\n"):
        line_number += 1
        stripped = raw.strip()
        if not stripped.startswith("|"):
            continue
        cells = split_row(stripped)
        if not seen_header:
            seen_header = True
            continue
        if all(set(cell) <= set("-: ") and cell for cell in cells):
            continue
        rows.append((cells, line_number))
    return rows


class Entry:
    """A heading and the labelled bullets under it.

    One shape, three records: a `journal.md` execution entry, a findings-ledger entry, and a
    retro report's observation or proposal. They differ in which labels are required, which is
    the caller's rule, not this module's.
    """

    __slots__ = ("heading", "title", "line", "blocks", "level")

    def __init__(self, heading, title, line, block_list, level) -> None:
        self.heading = heading
        self.title = title
        self.line = line
        self.blocks = block_list
        self.level = level

    def fields(self):
        """`{label: [blocks]}` for this entry."""
        return labelled(self.blocks)

    def field(self, label: str):
        """The first block declaring `label`, or None. Case-insensitive."""
        wanted = label.strip().lower()
        for block in self.blocks:
            if block.label and block.label.strip().lower() == wanted:
                return block
        return None

    def value(self, label: str, default: str = "") -> str:
        """A labelled field's folded value, or `default` when the label is absent."""
        block = self.field(label)
        return block.body if block is not None else default

    @property
    def end(self) -> int:
        return max([self.line] + [block.end for block in self.blocks])

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Entry({self.title!r}, line={self.line})"


def entries(text: str, first_line: int = 1, level: int = 2):
    """Every `Entry` in `text` — headings at `level`, each with the blocks beneath it.

    Content before the first heading belongs to no entry and is dropped; a caller that needs a
    document's preamble reads it with `blocks()`.
    """
    found = []
    lines = text.split("\n")
    starts = []
    for index, raw in enumerate(lines):
        match = HEADING_RE.match(raw)
        if match and len(match.group(1)) == level:
            starts.append((index, match.group(2).strip()))
    for position, (index, title) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "\n".join(lines[index + 1:stop])
        found.append(Entry("#" * level + " " + title, title, first_line + index,
                           blocks(body, first_line + index + 1), level))
    return found
