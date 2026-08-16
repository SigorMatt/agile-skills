#!/usr/bin/env python3
"""Self-test for scripts/lib. Run: python3 scripts/lib/selftest.py

Two layers:
  1. Fixed cases — every supported construct parses to an expected value, and every rejected
     construct raises YamlError with a line number.
  2. Cross-check — when PyYAML happens to be importable, every accepted fixture and every
     .yaml/.yml file in the repo is parsed by both readers and the results must be equal.
     PyYAML's absence skips this layer (see ADR-0002); it never fails the run.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import frontmatter  # noqa: E402
import miniyaml  # noqa: E402
import report as report_lib  # noqa: E402
from miniyaml import YamlError  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ACCEPT = [
    ("empty document", "", None),
    ("comments only", "# just a comment\n\n# another\n", None),
    ("flat mapping", "name: intake\nversion: 3\n", {"name": "intake", "version": 3}),
    ("leading doc marker", "---\nname: intake\n", {"name": "intake"}),
    ("trailing doc end", "name: intake\n...\n", {"name": "intake"}),
    ("null forms", "a: null\nb: ~\nc:\nd: NULL\n",
     {"a": None, "b": None, "c": None, "d": None}),
    ("booleans", "a: true\nb: False\nc: TRUE\n", {"a": True, "b": False, "c": True}),
    ("numbers", "a: 7\nb: -3\nc: 1.5\nd: 2e3\ne: 0.0\nf: 1.0e+3\n",
     {"a": 7, "b": -3, "c": 1.5, "d": "2e3", "e": 0.0, "f": 1000.0}),
    ("version-like string stays a string", "version: 0.1.0\n", {"version": "0.1.0"}),
    ("quoted scalars", "a: 'it''s'\nb: \"line\\nbreak\"\nc: \"7\"\n",
     {"a": "it's", "b": "line\nbreak", "c": "7"}),
    ("plain scalar with colon inside", "expr: item.status == \"planned\"\n",
     {"expr": 'item.status == "planned"'}),
    ("hash inside a word is not a comment", "url: http://x/#frag\n",
     {"url": "http://x/#frag"}),
    ("trailing comment stripped", "a: value  # note\nb: 2 # note\n", {"a": "value", "b": 2}),
    ("sequence indented under key", "inputs:\n  - one\n  - two\n",
     {"inputs": ["one", "two"]}),
    ("sequence flush with key", "inputs:\n- one\n- two\n", {"inputs": ["one", "two"]}),
    ("empty sequence", "inputs: []\n", {"inputs": []}),
    ("flow sequence", "tools: [Read, Write, Bash]\n",
     {"tools": ["Read", "Write", "Bash"]}),
    ("flow mapping", "limits: {max: 5, strict: true}\n",
     {"limits": {"max": 5, "strict": True}}),
    ("nested mapping", "a:\n  b:\n    c: 1\n", {"a": {"b": {"c": 1}}}),
    ("maps inside a sequence",
     "gates:\n  - name: tests\n    command: pytest\n  - name: lint\n    command: ruff\n",
     {"gates": [{"name": "tests", "command": "pytest"},
                {"name": "lint", "command": "ruff"}]}),
    ("nested structure inside a sequence item",
     "steps:\n  - name: one\n    args:\n      - a\n      - b\n  - name: two\n",
     {"steps": [{"name": "one", "args": ["a", "b"]}, {"name": "two"}]}),
    ("sequence of sequences", "grid:\n  - - 1\n    - 2\n  - - 3\n",
     {"grid": [[1, 2], [3]]}),
    ("literal block scalar", "body: |\n  line one\n  line two\n",
     {"body": "line one\nline two\n"}),
    ("literal block, strip chomping", "body: |-\n  line one\n  line two\n",
     {"body": "line one\nline two"}),
    ("folded block scalar", "body: >\n  line one\n  line two\n",
     {"body": "line one line two\n"}),
    ("folded block with a paragraph break", "body: >-\n  one\n  two\n\n  four\n",
     {"body": "one two\nfour"}),
    ("block scalar keeps blank interior lines", "body: |\n  one\n\n  three\n",
     {"body": "one\n\nthree\n"}),
    ("block scalar followed by a sibling key", "body: |\n  text\nafter: 2\n",
     {"body": "text\n", "after": 2}),
    ("top-level sequence", "- a\n- b\n", ["a", "b"]),
    ("blank lines between keys", "a: 1\n\n\nb: 2\n", {"a": 1, "b": 2}),
    ("key with dashes and dots", "when_to_use: x\nallowed-tools: y\nv.1: z\n",
     {"when_to_use": "x", "allowed-tools": "y", "v.1": "z"}),
]

REJECT = [
    ("anchor", "a: &anchor 1\n", 1),
    ("alias", "a: *anchor\n", 1),
    ("tag", "a: !!str 1\n", 1),
    ("tab indentation", "a:\n\tb: 1\n", 2),
    ("multiple documents", "a: 1\n---\nb: 2\n", 2),
    ("complex key", "? [a, b]\n: 1\n", 1),
    ("merge key", "a:\n  <<: *base\n", 2),
    ("duplicate key", "a: 1\na: 2\n", 2),
    ("garbage line", "a: 1\nthis is not a mapping\n", 2),
    ("bad indentation in mapping", "a: 1\n   b: 2\n", 2),
    ("unterminated flow sequence", "a: [1, 2\n", 1),
    ("unterminated quote", 'a: "abc\n', 1),
    ("bad escape", 'a: "x\\qy"\n', 1),
    ("sequence where a key is expected", "a: 1\n- b\n", 2),
]

DUMP_CASES = [
    ({"name": "intake"}, "name: intake\n"),
    ({"version": "0.1.0"}, "version: 0.1.0\n"),
    ({"flag": True, "count": 3, "nothing": None}, "flag: true\ncount: 3\nnothing: null\n"),
    ({"tools": ["Read", "Write"]}, "tools:\n  - Read\n  - Write\n"),
    ({"tools": []}, "tools: []\n"),
    ({"description": "Use when: a thing happens"},
     'description: "Use when: a thing happens"\n'),
    ({"yes_like": "yes"}, 'yes_like: "yes"\n'),
    ({"metadata": {"a": "b"}}, "metadata:\n  a: b\n"),
]


class Results:
    def __init__(self) -> None:
        self.passed = 0
        self.failures: list = []

    def check(self, label: str, got, want) -> None:
        if got == want:
            self.passed += 1
        else:
            self.failures.append(f"{label}\n    expected: {want!r}\n    got:      {got!r}")

    def fail(self, label: str, detail: str) -> None:
        self.failures.append(f"{label}\n    {detail}")


def run_accept(results: Results) -> None:
    for label, text, expected in ACCEPT:
        try:
            got = miniyaml.load(text, name=label)
        except YamlError as exc:
            results.fail(f"accept/{label}", f"unexpected YamlError: {exc}")
            continue
        results.check(f"accept/{label}", got, expected)


def run_reject(results: Results) -> None:
    for label, text, expected_line in REJECT:
        try:
            got = miniyaml.load(text, name=label)
        except YamlError as exc:
            if exc.line == expected_line:
                results.passed += 1
            else:
                results.fail(f"reject/{label}",
                             f"raised on line {exc.line}, expected {expected_line}: {exc.message}")
            continue
        results.fail(f"reject/{label}", f"parsed instead of failing: {got!r}")


def run_dump(results: Results) -> None:
    for mapping, expected in DUMP_CASES:
        results.check(f"dump/{list(mapping)[0]}", miniyaml.dump_frontmatter(mapping), expected)
    # Round trip: whatever we emit, we must be able to read back.
    for mapping, _ in DUMP_CASES:
        text = miniyaml.dump_frontmatter(mapping)
        results.check(f"roundtrip/{list(mapping)[0]}", miniyaml.load(text), mapping)
    try:
        miniyaml.dump_frontmatter({"body": "two\nlines"})
    except ValueError:
        results.passed += 1
    else:
        results.fail("dump/multiline", "multi-line scalar should be refused")


def run_frontmatter(results: Results) -> None:
    text = "---\nid: WI-0001\nstatus: draft\n---\n\n# Title\n\nBody line.\n"
    fields, body, body_line = frontmatter.split(text, name="item.md")
    results.check("frontmatter/fields", fields, {"id": "WI-0001", "status": "draft"})
    results.check("frontmatter/body", body, "\n# Title\n\nBody line.\n")
    results.check("frontmatter/body_line", body_line, 5)

    empty_fields, _, _ = frontmatter.split("---\n---\nbody\n", name="empty.md")
    results.check("frontmatter/empty-block", empty_fields, {})

    for label, bad, line in [
        ("no fence", "# Title\n", 1),
        ("unclosed fence", "---\nid: WI-0001\n", 1),
        ("not a mapping", "---\n- a\n- b\n---\n", 2),
    ]:
        try:
            frontmatter.split(bad, name=label)
        except frontmatter.FrontmatterError as exc:
            results.check(f"frontmatter/reject-{label}", exc.line, line)
        else:
            results.fail(f"frontmatter/reject-{label}", "parsed instead of failing")

    # A YAML error inside the block must report the line number in the *file*, not the block.
    try:
        frontmatter.split("---\nid: WI-0001\n\tbad: 1\n---\n", name="tabs.md")
    except frontmatter.FrontmatterError as exc:
        results.check("frontmatter/yaml-error-line", exc.line, 3)
    else:
        results.fail("frontmatter/yaml-error-line", "tab indentation should have been refused")

    # render() is the inverse of split() for flat mappings.
    rendered = frontmatter.render({"id": "WI-0001", "status": "draft"}, "\n# Title\n")
    again, again_body, _ = frontmatter.split(rendered, name="round.md")
    results.check("frontmatter/roundtrip", (again, again_body),
                  ({"id": "WI-0001", "status": "draft"}, "\n# Title\n"))


def run_report(results: Results) -> None:
    rep = report_lib.Report("demo", root="/tmp/root")
    rep.warn("/tmp/root/b.md", 2, "b.code", "second")
    rep.error("/tmp/root/a.md", 10, "a.code", "first", hint="do the thing")
    results.check("report/ok-with-warning-only", report_lib.Report("x").ok(), True)
    results.check("report/errors", rep.errors, 1)
    results.check("report/warnings", rep.warnings, 1)
    results.check("report/not-ok", rep.ok(), False)
    results.check("report/format-relativised", rep.findings[1].format(rep.root),
                  "a.md:10: ERROR [a.code] first\n    hint: do the thing")

    import io
    buffer = io.StringIO()
    code = rep.emit(buffer)
    lines = buffer.getvalue().strip().split("\n")
    results.check("report/exit-code", code, 1)
    # Sorted by path, so a.md precedes b.md regardless of the order they were recorded in.
    results.check("report/sorted", lines[0].startswith("a.md:10:"), True)
    results.check("report/summary", lines[-1], "demo: 1 error, 1 warning")


def repo_yaml_files() -> list:
    found = []
    for base, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".venv")]
        for name in sorted(files):
            if name.endswith((".yaml", ".yml")):
                found.append(os.path.join(base, name))
    return sorted(found)


def run_crosscheck(results: Results) -> str:
    try:
        import yaml  # type: ignore
    except ImportError:
        return "skipped (PyYAML not installed; see ADR-0002)"

    checked = 0
    for label, text, _ in ACCEPT:
        try:
            reference = yaml.safe_load(text)
        except Exception as exc:  # pragma: no cover - fixture bug, not a parser bug
            results.fail(f"crosscheck/{label}", f"PyYAML could not parse the fixture: {exc}")
            continue
        results.check(f"crosscheck/{label}", miniyaml.load(text, name=label), reference)
        checked += 1
    for path in repo_yaml_files():
        rel = os.path.relpath(path, REPO_ROOT)
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        try:
            reference = yaml.safe_load(text)
        except Exception as exc:
            results.fail(f"crosscheck/{rel}", f"PyYAML could not parse it: {exc}")
            continue
        try:
            got = miniyaml.load(text, name=rel)
        except YamlError as exc:
            results.fail(f"crosscheck/{rel}", f"miniyaml rejected a real repo file: {exc}")
            continue
        results.check(f"crosscheck/{rel}", got, reference)
        checked += 1
    return f"ran against PyYAML {yaml.__version__} on {checked} inputs"


def main() -> int:
    results = Results()
    run_accept(results)
    run_reject(results)
    run_dump(results)
    run_frontmatter(results)
    run_report(results)
    crosscheck_note = run_crosscheck(results)

    print(f"miniyaml self-test: {results.passed} passed, {len(results.failures)} failed")
    print(f"  cross-check: {crosscheck_note}")
    for failure in results.failures:
        print(f"  FAIL {failure}")
    return 1 if results.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
