"""A reader for the YAML subset this project uses. Standard library only.

Why this exists: see meta/adr/ADR-0002-scripting-and-dependencies.md. The gates that use it
run inside a consumer's project, where no third-party package can be assumed.

Supported subset
----------------
* block mappings           ``key: value`` / nested by indentation
* block sequences          ``- item`` (at or below the parent key's indent)
* maps inside sequences    ``- key: value`` with aligned continuation lines
* scalars                  plain, 'single quoted', "double quoted" (\\n \\t \\" \\\\ escapes)
* block scalars            ``|``, ``|-``, ``|+``, ``>``, ``>-``, ``>+``
* flow collections         ``[a, b]`` and ``{a: 1, b: 2}``, single line, scalar members
* literals                 ``true`` / ``false`` (any case), ``null`` / ``~`` / empty
* numbers                  integers and floats (anything else stays a string)
* comments                 ``#`` at line start, or preceded by whitespace outside quotes
* one optional leading ``---`` and an optional trailing ``...``

Deliberately rejected, each with a line number
----------------------------------------------
anchors ``&a``, aliases ``*a``, tags ``!t``, multiple documents, tab indentation,
complex keys (``? ``), merge keys, and multi-line flow collections.

A construct outside the subset raises :class:`YamlError`. It is never guessed at: a validator
that silently mis-reads a contract would pass a gate on a lie.
"""

from __future__ import annotations

import re

__all__ = ["YamlError", "load", "load_file", "dump_frontmatter"]


class YamlError(ValueError):
    """Raised for anything this reader will not parse. Carries source name and line."""

    def __init__(self, message: str, name: str = "<string>", line: int = 0) -> None:
        self.message = message
        self.name = name
        self.line = line
        super().__init__(f"{name}:{line}: {message}")


# A mapping key: bare word, or a quoted string, followed by ':' and whitespace-or-EOL.
_KEY_RE = re.compile(r"""^(?P<key>[A-Za-z0-9_][A-Za-z0-9_.\-/+]*|"[^"]*"|'[^']*')\s*:(?=\s|$)""")
_INT_RE = re.compile(r"^[-+]?[0-9]+$")
# A dot is required. Exponent-only forms such as "2e3" stay strings, which is what YAML 1.1
# readers do; matching them keeps the cross-check in selftest.py meaningful.
_FLOAT_RE = re.compile(r"^[-+]?(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?$")
_BLOCK_RE = re.compile(r"^(?P<style>[|>])(?P<chomp>[-+]?)(?P<indent>[0-9]*)\s*(?P<trail>#.*)?$")


def load_file(path):
    """Parse a YAML file. ``path`` may be a str or os.PathLike."""
    with open(path, "r", encoding="utf-8") as handle:
        return load(handle.read(), name=str(path))


def load(text: str, name: str = "<string>"):
    """Parse a YAML string. Returns dict, list, scalar, or None for an empty document."""
    return _Parser(text, name).parse()


class _Parser:
    def __init__(self, text: str, name: str) -> None:
        # A mutable copy: sequence items are rewritten in place as synthetic lines so that
        # "- key: value" can be re-entered as a mapping without a pushback buffer. Line
        # numbers are preserved because rewriting never changes the line count.
        self.lines = text.split("\n")
        self.name = name
        self.i = 0

    # ---- diagnostics -------------------------------------------------------------

    def fail(self, message: str, index: int | None = None):
        line = (self.i if index is None else index) + 1
        raise YamlError(message, self.name, line)

    # ---- line handling -----------------------------------------------------------

    @staticmethod
    def _is_skippable(raw: str) -> bool:
        stripped = raw.strip()
        return stripped == "" or stripped.startswith("#")

    def _indent_of(self, raw: str, index: int) -> int:
        measured = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:measured] or raw.lstrip(" ").startswith("\t"):
            self.fail("tab used for indentation; use spaces", index)
        return measured

    def next_significant(self):
        """Index of the next content line, or None. Does not consume."""
        j = self.i
        while j < len(self.lines):
            raw = self.lines[j]
            if self._is_skippable(raw):
                j += 1
                continue
            if raw.strip() == "...":
                return None
            return j
        return None

    def at(self, index: int):
        raw = self.lines[index]
        return self._indent_of(raw, index), raw.strip()

    # ---- entry point -------------------------------------------------------------

    def parse(self):
        first = self.next_significant()
        if first is not None and self.lines[first].strip() == "---":
            self.i = first + 1
            # A second '---' would start another document, which the subset excludes.
            for j in range(self.i, len(self.lines)):
                if self.lines[j].strip() == "---":
                    self.fail("multiple YAML documents are not supported", j)
        index = self.next_significant()
        if index is None:
            return None
        indent, _ = self.at(index)
        value = self.parse_node(indent)
        trailing = self.next_significant()
        if trailing is not None:
            self.fail("unexpected content after the end of the document", trailing)
        return value

    def parse_node(self, indent: int):
        index = self.next_significant()
        if index is None:
            return None
        _, content = self.at(index)
        self._reject_unsupported(content, index)
        if content == "-" or content.startswith("- "):
            return self.parse_sequence(indent)
        return self.parse_mapping(indent)

    def _reject_unsupported(self, content: str, index: int) -> None:
        if content.startswith("? "):
            self.fail("complex mapping keys ('? ') are not supported", index)
        if content.startswith("<<:"):
            self.fail("merge keys ('<<') are not supported", index)

    # ---- mappings ----------------------------------------------------------------

    def parse_mapping(self, indent: int) -> dict:
        result: dict = {}
        while True:
            index = self.next_significant()
            if index is None:
                break
            line_indent, content = self.at(index)
            if line_indent < indent:
                break
            if line_indent > indent:
                self.fail("unexpected indentation inside a mapping", index)
            if content == "-" or content.startswith("- "):
                self.fail("sequence item where a mapping key was expected", index)
            self._reject_unsupported(content, index)
            match = _KEY_RE.match(content)
            if not match:
                self.fail(f"expected 'key: value', found {content!r}", index)
            key = _unquote_key(match.group("key"))
            if key in result:
                self.fail(f"duplicate key {key!r}", index)
            rest = content[match.end():].strip()
            self.i = index + 1
            result[key] = self._value_for_key(indent, rest, index)
        return result

    def _value_for_key(self, indent: int, rest: str, index: int):
        if rest.startswith(("|", ">")):
            return self.parse_block_scalar(indent, rest, index)
        if rest and not rest.startswith("#"):
            return self.parse_scalar(rest, index)
        # Empty value: either a nested block, a sequence at the same indent, or null.
        nxt = self.next_significant()
        if nxt is None:
            return None
        nxt_indent, nxt_content = self.at(nxt)
        if nxt_indent > indent:
            return self.parse_node(nxt_indent)
        if nxt_indent == indent and (nxt_content == "-" or nxt_content.startswith("- ")):
            return self.parse_sequence(indent)
        return None

    # ---- sequences ---------------------------------------------------------------

    def parse_sequence(self, indent: int) -> list:
        items: list = []
        while True:
            index = self.next_significant()
            if index is None:
                break
            line_indent, content = self.at(index)
            if line_indent < indent:
                break
            if line_indent > indent:
                self.fail("unexpected indentation inside a sequence", index)
            if not (content == "-" or content.startswith("- ")):
                break
            rest = content[1:].strip()
            self.i = index + 1
            if rest == "" or rest.startswith("#"):
                nxt = self.next_significant()
                if nxt is not None and self.at(nxt)[0] > line_indent:
                    items.append(self.parse_node(self.at(nxt)[0]))
                else:
                    items.append(None)
                continue
            inner_indent = line_indent + (len(content) - len(content[1:].lstrip(" ")))
            if _KEY_RE.match(rest):
                # Rewrite "- key: value" as an aligned mapping line and re-enter.
                self.lines[index] = " " * inner_indent + rest
                self.i = index
                items.append(self.parse_mapping(inner_indent))
            elif rest.startswith("- "):
                self.lines[index] = " " * inner_indent + rest
                self.i = index
                items.append(self.parse_sequence(inner_indent))
            elif rest.startswith(("|", ">")):
                items.append(self.parse_block_scalar(line_indent, rest, index))
            else:
                items.append(self.parse_scalar(rest, index))
        return items

    # ---- scalars -----------------------------------------------------------------

    def parse_block_scalar(self, indent: int, header: str, index: int) -> str:
        match = _BLOCK_RE.match(header)
        if not match:
            self.fail(f"unsupported block scalar header {header!r}", index)
        style = match.group("style")
        chomp = match.group("chomp")
        if match.group("indent"):
            self.fail("explicit block scalar indentation indicators are not supported", index)

        raw_lines: list[str] = []
        content_indent = None
        j = self.i
        while j < len(self.lines):
            raw = self.lines[j]
            if raw.strip() == "":
                raw_lines.append("")
                j += 1
                continue
            line_indent = self._indent_of(raw, j)
            if content_indent is None:
                if line_indent <= indent:
                    break
                content_indent = line_indent
            if line_indent < content_indent:
                break
            raw_lines.append(raw[content_indent:])
            j += 1
        self.i = j

        # Trailing blank lines belong to the chomping rules, not to the content.
        while raw_lines and raw_lines[-1] == "":
            raw_lines.pop()
        if not raw_lines:
            return "" if chomp == "-" else "\n" if chomp == "+" else ""

        if style == "|":
            body = "\n".join(raw_lines)
        else:
            body = _fold(raw_lines)
        if chomp == "-":
            return body
        return body + "\n"

    def parse_scalar(self, raw: str, index: int):
        text = _strip_comment(raw)
        if text == "":
            return None
        if text[0] in "&*!":
            self.fail(f"anchors, aliases and tags are not supported ({text[:8]!r})", index)
        if text[0] == "[":
            return self._flow_sequence(text, index)
        if text[0] == "{":
            return self._flow_mapping(text, index)
        return _coerce(text, self, index)

    def _flow_sequence(self, text: str, index: int) -> list:
        if not text.endswith("]"):
            self.fail("multi-line flow sequences are not supported", index)
        inner = text[1:-1].strip()
        if inner == "":
            return []
        return [_coerce(part.strip(), self, index) for part in _split_flow(inner, self, index)]

    def _flow_mapping(self, text: str, index: int) -> dict:
        if not text.endswith("}"):
            self.fail("multi-line flow mappings are not supported", index)
        inner = text[1:-1].strip()
        result: dict = {}
        if inner == "":
            return result
        for part in _split_flow(inner, self, index):
            match = _KEY_RE.match(part.strip())
            if not match:
                self.fail(f"expected 'key: value' in flow mapping, found {part.strip()!r}", index)
            key = _unquote_key(match.group("key"))
            result[key] = _coerce(part.strip()[match.end():].strip(), self, index)
        return result


# ---- helpers ---------------------------------------------------------------------


def _unquote_key(key: str) -> str:
    if len(key) >= 2 and key[0] == key[-1] and key[0] in "\"'":
        return key[1:-1]
    return key


def _strip_comment(text: str) -> str:
    """Remove a trailing ``# comment``, respecting quotes and brackets."""
    quote = None
    depth = 0
    for pos, char in enumerate(text):
        if quote:
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        elif char == "#" and depth == 0 and (pos == 0 or text[pos - 1] in " \t"):
            return text[:pos].rstrip()
    return text.rstrip()


def _split_flow(inner: str, parser: _Parser, index: int) -> list:
    parts: list[str] = []
    depth = 0
    quote = None
    current = ""
    for char in inner:
        if quote:
            current += char
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
            current += char
        elif char in "[{":
            depth += 1
            current += char
        elif char in "]}":
            depth -= 1
            current += char
        elif char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    if quote:
        parser.fail("unterminated quoted string in flow collection", index)
    parts.append(current)
    return parts


def _fold(lines: list) -> str:
    """Folded (``>``) semantics: single newlines become spaces, blank lines stay newlines.

    Limitation: YAML preserves literal newlines around *more-indented* lines inside a folded
    scalar. This reader folds them like any other line, so do not use ``>`` with ragged
    indentation. ``|`` covers that case exactly and is what the specs use.
    """
    out = ""
    for line in lines:
        if line == "":
            out += "\n"
        elif out == "" or out.endswith("\n"):
            out += line
        else:
            out += " " + line
    return out


def _coerce(text: str, parser: _Parser, index: int):
    if text == "":
        return None
    first = text[0]
    if first == '"':
        if len(text) < 2 or not text.endswith('"'):
            parser.fail("unterminated double-quoted string", index)
        return _unescape(text[1:-1], parser, index)
    if first == "'":
        if len(text) < 2 or not text.endswith("'"):
            parser.fail("unterminated single-quoted string", index)
        return text[1:-1].replace("''", "'")
    if first in "&*!":
        parser.fail(f"anchors, aliases and tags are not supported ({text[:8]!r})", index)
    if first == "[":
        return parser._flow_sequence(text, index)
    if first == "{":
        return parser._flow_mapping(text, index)
    lowered = text.lower()
    if lowered in ("null", "~"):
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if _INT_RE.match(text):
        return int(text)
    if _FLOAT_RE.match(text):
        return float(text)
    return text


_ESCAPES = {
    "n": "\n", "t": "\t", "r": "\r", "0": "\0",
    '"': '"', "\\": "\\", "/": "/", " ": " ",
}


def _unescape(text: str, parser: _Parser, index: int) -> str:
    out: list = []
    pos = 0
    while pos < len(text):
        char = text[pos]
        if char != "\\":
            out.append(char)
            pos += 1
            continue
        pos += 1
        if pos >= len(text):
            parser.fail("string ends with a dangling backslash", index)
        code = text[pos]
        if code in _ESCAPES:
            out.append(_ESCAPES[code])
            pos += 1
        elif code == "u":
            hexits = text[pos + 1:pos + 5]
            if len(hexits) != 4:
                parser.fail("truncated \\u escape", index)
            try:
                out.append(chr(int(hexits, 16)))
            except ValueError:
                parser.fail(f"invalid \\u escape {hexits!r}", index)
            pos += 5
        else:
            parser.fail(f"unsupported escape '\\{code}'", index)
    return "".join(out)


# ---- emitting --------------------------------------------------------------------

_PLAIN_SAFE_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9 _.,/()+'-]*$")
_RESERVED_PLAIN = {"true", "false", "null", "yes", "no", "on", "off", "~"}


def _needs_quotes(text: str) -> bool:
    if text == "" or text != text.strip():
        return True
    if text.lower() in _RESERVED_PLAIN:
        return True
    if _INT_RE.match(text) or _FLOAT_RE.match(text):
        return True
    return not _PLAIN_SAFE_RE.match(text)


def _emit_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if "\n" in text:
        raise ValueError("dump_frontmatter does not emit multi-line scalars")
    if _needs_quotes(text):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def dump_frontmatter(mapping: dict) -> str:
    """Emit a flat mapping (scalars and lists of scalars) as YAML inside the subset.

    Insertion order is preserved so rendered output is byte-stable across runs.
    """
    out: list = []
    for key, value in mapping.items():
        if not _KEY_RE.match(f"{key}:"):
            raise ValueError(f"key {key!r} is not representable in the YAML subset")
        if isinstance(value, (list, tuple)):
            if not value:
                out.append(f"{key}: []")
                continue
            out.append(f"{key}:")
            for member in value:
                out.append(f"  - {_emit_scalar(member)}")
        elif isinstance(value, dict):
            out.append(f"{key}:")
            for sub_key, sub_value in value.items():
                out.append(f"  {sub_key}: {_emit_scalar(sub_value)}")
        else:
            out.append(f"{key}: {_emit_scalar(value)}")
    return "\n".join(out) + "\n"
