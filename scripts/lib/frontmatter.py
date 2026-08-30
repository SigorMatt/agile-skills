"""Read the YAML frontmatter block out of a markdown file. Standard library only.

Every artifact in the workspace — work items, questions, docs — is markdown with a leading
``---`` fenced YAML block. The line numbers this module returns are 1-based *file* line
numbers, so a validator's findings point at the real line a human would open.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import miniyaml  # noqa: E402

from textio import read_text  # noqa: E402

__all__ = ["FrontmatterError", "split", "load_file", "render"]


class FrontmatterError(ValueError):
    def __init__(self, message: str, name: str = "<string>", line: int = 0) -> None:
        self.message = message
        self.name = name
        self.line = line
        super().__init__(f"{name}:{line}: {message}")


def split(text: str, name: str = "<string>"):
    """Return ``(fields, body, body_line)``.

    ``fields`` is the parsed frontmatter mapping, ``body`` the markdown after the closing
    fence, and ``body_line`` the 1-based line number where ``body`` starts. A file with no
    frontmatter is an error: the schemas make it mandatory, and a silently-empty mapping would
    let an unlabelled file pass validation.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("file must start with a '---' frontmatter fence", name, 1)
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            block = "\n".join(lines[1:index])
            try:
                fields = miniyaml.load(block, name=name)
            except miniyaml.YamlError as exc:
                # Re-raise with the line number shifted to the position in the whole file.
                raise FrontmatterError(exc.message, name, exc.line + 1) from None
            if fields is None:
                fields = {}
            if not isinstance(fields, dict):
                raise FrontmatterError("frontmatter must be a mapping", name, 2)
            body = "\n".join(lines[index + 1:])
            return fields, body, index + 2
    raise FrontmatterError("frontmatter fence opened but never closed", name, 1)


def load_file(path):
    # H-016: decode with replacement rather than raising. A workspace file that is not UTF-8 is a
    # finding for whoever is walking the tree, never an uncaught traceback out of a gate.
    text, _ = read_text(path)
    return split(text, name=str(path))


def render(fields: dict, body: str) -> str:
    """Inverse of :func:`split` for the flat mappings the schemas use."""
    block = miniyaml.dump_frontmatter(fields)
    # split() defines the body as everything after the closing fence *line*, so the fence's
    # own newline is not part of it. Emitting it here is what makes render/split inverses.
    return f"---\n{block}---\n{body}"
