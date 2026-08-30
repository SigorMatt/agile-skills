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
import claims as claims_lib  # noqa: E402
import record as record_lib  # noqa: E402
import report as report_lib  # noqa: E402
import scope as scope_lib  # noqa: E402
import workspace as workspace_lib  # noqa: E402
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


ITEM_MD = """---
id: WI-0001
type: work-item
title: Count lines per file
status: verifying
priority: high
epic: EP-001
created: 2026-08-16T09:12:04Z
updated: 2026-08-16T11:47:52Z
branch: wi/WI-0001
depends-on:
  - WI-0002
---

## Story

As a reader, I want a line count, so that I can see which file dominates.

## Acceptance criteria

- [x] AC1 — one row per regular file with its line count
- [ ] AC2 — rows sorted by descending count
- [ ]  AC3 - a missing path exits 2

## Out of scope

- Recursion.
"""

HISTORY_MD = """# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-16T09:12:04Z | — | draft | intake | — | created from idea refinement |
| 2026-08-16T09:58:11Z | draft | ready | refine | — | DoR passed |
| 2026-08-16T11:05:52Z | ready | awaiting-answer | plan | ready | Q-001 blocking |
"""

JOURNAL_MD = """# Journal — WI-0001

## 2026-08-16T09:58:11Z — refine v0.1.0 — product-analyst

- **Item:** WI-0001
- **Gates:** definition-of-ready → pass
- **Status:** `draft` → `ready`

## not a valid heading

- **Item:** WI-0001
"""

QUESTION_MD = """---
id: Q-001
item: WI-0001
from-skill: plan
addressed-to: architect
blocking: true
status: open
created: 2026-08-16T11:05:52Z
---

## Context

Tie-break order is undefined.

## Question

Which file wins a tie?
"""


def build_workspace(base: str) -> str:
    item_dir = os.path.join(base, "tracker", "items", "WI-0001")
    os.makedirs(os.path.join(item_dir, "questions"))
    os.makedirs(os.path.join(item_dir, "artifacts"))
    os.makedirs(os.path.join(base, "docs", "product"))
    writes = {
        os.path.join(base, "tracker", "project.yaml"):
            "project:\n  name: demo\n  trunk-branch: main\n  description: A demo.\n"
            "commands:\n  test: python3 -m pytest -q\n  lint: null\n  build: null\n"
            "conventions:\n  branch-prefix: wi/\n"
            '  commit-subject: "<scope>: <summary> (refs <ITEM-ID>)"\n',
        os.path.join(item_dir, "item.md"): ITEM_MD,
        os.path.join(item_dir, "history.md"): HISTORY_MD,
        os.path.join(item_dir, "journal.md"): JOURNAL_MD,
        os.path.join(item_dir, "questions", "Q-001.md"): QUESTION_MD,
        os.path.join(item_dir, "artifacts", "plan.md"): "# Plan\n",
        os.path.join(base, "docs", "product", "vision.md"):
            "---\ntitle: Vision\nversion: 2\nstatus: current\nupdated: 2026-08-16T09:12:04Z\n"
            "updated-by: intake\nupdated-for: EP-001\n---\n\n# Vision\n\nBody.\n\n"
            "## Change log\n\n| version | when | by | for | what changed |\n"
            "|---|---|---|---|---|\n| 2 | 2026-08-16T09:12:04Z | intake | EP-001 | Scope |\n"
            "| 1 | 2026-08-15T16:02:00Z | intake | EP-001 | First version |\n",
    }
    for path, text in writes.items():
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    return base


def run_workspace(results: Results) -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as base:
        build_workspace(base)
        ws = workspace_lib.Workspace(base).load()

        results.check("workspace/project-name", (ws.project or {}).get("project", {}).get("name"),
                      "demo")
        results.check("workspace/command-test", ws.command("test"), "python3 -m pytest -q")
        results.check("workspace/command-lint-null", ws.command("lint"), None)
        results.check("workspace/branch-prefix", ws.convention("branch-prefix"), "wi/")
        results.check("workspace/items", sorted(ws.items), ["WI-0001"])

        item = ws.items["WI-0001"]
        # Deliberately inconsistent with the last history row, so validate-workspace has
        # something real to catch later; the loader itself must not "fix" it.
        results.check("workspace/item-status", item.status, "verifying")
        results.check("workspace/item-type", item.type, "work-item")
        results.check("workspace/depends-on", item.fields.get("depends-on"), ["WI-0002"])
        results.check("workspace/sections",
                      sorted(item.sections), ["## Acceptance criteria", "## Out of scope",
                                              "## Story"])

        criteria = item.acceptance_criteria()
        results.check("workspace/ac-count", len(criteria), 3)
        results.check("workspace/ac-ticked", [c["checked"] for c in criteria],
                      [True, False, False])
        results.check("workspace/ac-labels", [c["label"] for c in criteria],
                      ["AC1", "AC2", "AC3"])
        # Line numbers must point at the real file line a human would open.
        with open(item.path, "r", encoding="utf-8") as handle:
            file_lines = handle.read().split("\n")
        results.check("workspace/ac-line-accurate",
                      file_lines[criteria[0]["line"] - 1].strip().startswith("- [x] AC1"), True)

        results.check("workspace/history-rows", len(item.history), 3)
        results.check("workspace/history-first-from",
                      item.history[0].normalised(item.history[0].from_status), None)
        results.check("workspace/history-resume-to", item.history[2].resume_to, "ready")
        results.check("workspace/history-actor", item.history[1].actor, "refine")

        results.check("workspace/journal-entries", len(item.journal), 1)
        results.check("workspace/journal-skill", item.journal[0].skill, "refine")
        results.check("workspace/journal-version", item.journal[0].version, "0.1.0")
        results.check("workspace/journal-bullets", item.journal[0].bullets.get("Item"), "WI-0001")
        # The malformed heading must be reported, not silently skipped.
        codes = [code for _, _, code, _, _ in ws.load_errors]
        results.check("workspace/journal-bad-heading-reported", "journal.heading" in codes, True)

        results.check("workspace/questions", [q.identifier for q in item.questions], ["Q-001"])
        results.check("workspace/blocking", len(item.blocking_questions()), 1)
        results.check("workspace/question-sections",
                      sorted(item.questions[0].sections), ["## Context", "## Question"])

        results.check("workspace/docs", len(ws.docs), 1)
        results.check("workspace/doc-version", ws.docs[0].fields.get("version"), 2)
        results.check("workspace/doc-changelog-rows", len(ws.docs[0].changelog), 2)
        results.check("workspace/doc-changelog-top", ws.docs[0].changelog[0][0][0], "2")

        results.check("workspace/artifacts", item.artifacts, ["plan.md"])
        results.check("workspace/has-artifact", item.has_artifact("plan.md"), True)
        results.check("workspace/statuses-reached", sorted(item.statuses_reached()),
                      ["awaiting-answer", "draft", "ready"])

    # A workspace that is not there at all reports it rather than raising.
    with tempfile.TemporaryDirectory() as empty:
        ws = workspace_lib.Workspace(empty).load()
        codes = {code for _, _, code, _, _ in ws.load_errors}
        results.check("workspace/empty-reports-missing",
                      {"project.missing", "items.missing"} <= codes, True)


def run_root_resolution(results: Results) -> None:
    """F-019: a script run from inside a workspace must find the workspace, not a fragment."""
    import tempfile

    with tempfile.TemporaryDirectory() as base:
        root = build_workspace(base)
        deep = os.path.join(root, "tracker", "items", "WI-0001", "questions")
        os.makedirs(deep, exist_ok=True)
        results.check("root/from-deep", workspace_lib.find_workspace_root(deep), root)
        results.check("root/from-root", workspace_lib.find_workspace_root(root), root)
        results.check("root/explicit-wins",
                      workspace_lib.resolve_root(deep, announce=False), deep)
        cwd = os.getcwd()
        try:
            os.chdir(deep)
            results.check("root/implicit-walks-up",
                          os.path.realpath(workspace_lib.resolve_root(announce=False)),
                          os.path.realpath(root))
        finally:
            os.chdir(cwd)
    # Outside any workspace, resolution falls back to the working directory rather than
    # reaching for someone else's tracker.
    with tempfile.TemporaryDirectory() as stranger:
        cwd = os.getcwd()
        try:
            os.chdir(stranger)
            results.check("root/no-workspace-falls-back",
                          os.path.realpath(workspace_lib.resolve_root(announce=False)),
                          os.path.realpath(stranger))
        finally:
            os.chdir(cwd)


def run_escaping(results: Results) -> None:
    """F-044 and F-037: the two escapes, both of which need a reader as well as a writer."""
    import claims as claims_lib

    # A reason containing a union type used to split its history row into extra cells.
    row = r"| 2026-01-01T00:00:00Z | draft | ready | refine | \u2014 | accepts str \| None |"
    cells = record_lib.split_row(row)
    results.check("escape/row-cell-count", len(cells), 6)
    results.check("escape/row-reason", cells[5], "accepts str | None")
    results.check("escape/row-plain",
                  record_lib.split_row("| a | b | c |"), ["a", "b", "c"])
    results.check("escape/row-backslash",
                  record_lib.split_row(r"| a | back\\slash |"), ["a", r"back\slash"])

    # A citation inside code is a quotation. Masking preserves line numbers.
    masked = claims_lib.mask_code("one `[src: bogus]` two")
    results.check("escape/mask-keeps-length", len(masked), len("one `[src: bogus]` two"))
    results.check("escape/mask-removes-marker", "[src:" in masked, False)
    results.check("escape/mask-keeps-newlines",
                  claims_lib.mask_code("a\n`x`\nb").count("\n"), 2)
    # The fence itself is a backtick run, so mask_code blanks it first and the line arrives as
    # spaces rather than as an empty string. Column positions are preserved on purpose, so the
    # property to assert is that no marker survives — not the exact whitespace.
    results.check("escape/masked-lines-fence",
                  "[src:" in claims_lib.masked_lines("a\n```\n[src: bogus]\n```\nb")[2], False)
    results.check("escape/masked-lines-prose",
                  claims_lib.masked_lines("a [src: WI-0001] b")[0], "a [src: WI-0001] b")


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


def run_scope(results) -> None:
    """A diff window has three states, and only one of them is a pass (F-066, scope.py).

    Built in a throwaway repository rather than against this one, so the test does not depend on
    where HEAD happens to be when `scripts/check` runs.
    """
    import shutil
    import subprocess
    import tempfile
    if shutil.which("git") is None:
        results.check("scope/skipped-no-git", True, True)
        return
    with tempfile.TemporaryDirectory() as base:
        repo = os.path.join(base, "repo")
        os.makedirs(os.path.join(repo, "docs"))

        def git(*args):
            return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)

        results.check("scope/outside a repository", scope_lib.diff_scope(repo, "main").verdict,
                      "no-repository")
        git("init", "--initial-branch=main")
        git("config", "user.email", "selftest@example.invalid")
        git("config", "user.name", "selftest")
        with open(os.path.join(repo, "docs", "a.md"), "w", encoding="utf-8") as handle:
            handle.write("one\n")
        git("add", "-A")
        git("commit", "-m", "base")

        results.check("scope/a ref that does not resolve",
                      scope_lib.diff_scope(repo, "no-such-ref", ["docs"]).verdict,
                      "unresolved-ref")
        results.check("scope/the ref IS the current commit, tree clean",
                      scope_lib.diff_scope(repo, "main", ["docs"]).verdict, "same-commit")

        # Dirty *outside* the paths this gate reads is still a window that cannot see: the
        # distinction is what stops a review that wrote tracker/ from claiming it checked docs/.
        with open(os.path.join(repo, "other.txt"), "w", encoding="utf-8") as handle:
            handle.write("two\n")
        results.check("scope/dirty elsewhere does not rescue the window",
                      scope_lib.diff_scope(repo, "main", ["docs"]).verdict, "same-commit")
        results.check("scope/dirty elsewhere is a real window for a gate that reads it",
                      scope_lib.diff_scope(repo, "main").verdict, "real")

        with open(os.path.join(repo, "docs", "a.md"), "w", encoding="utf-8") as handle:
            handle.write("one, changed\n")
        window = scope_lib.diff_scope(repo, "main", ["docs"])
        results.check("scope/an uncommitted edit under the path is real", window.verdict, "real")
        results.check("scope/and it names the path", "docs/a.md" in window.paths, True)

        git("add", "-A")
        git("commit", "-m", "the change")
        git("checkout", "-q", "-b", "wi/WI-0001")
        with open(os.path.join(repo, "docs", "b.md"), "w", encoding="utf-8") as handle:
            handle.write("three\n")
        git("add", "-A")
        git("commit", "-m", "on the branch")
        window = scope_lib.diff_scope(repo, "main", ["docs"])
        results.check("scope/a branch ahead of the trunk is real", window.verdict, "real")
        results.check("scope/degenerate is the negation of real", window.degenerate, False)


def run_record(results) -> None:
    """The record model — the two shapes F-069 and F-073 got wrong, and the entry reader.

    Every case here is a specimen from the ledger rather than an invented one. A parser whose
    tests are all invented passes on the shapes its author imagined.
    """
    # F-073, first half: a bullet ends at a blank line or at unindented prose, not only at the
    # next bullet. The closing sentence of a section was swallowed into the last entry and
    # failed a gate on correct work.
    wrapped = ("- WI-0002/Q-001 — compatible, because the marker rule and the break rule\n"
               "  do not describe the same cell\n"
               "- WI-0003/Q-002 — compatible\n"
               "No verdict is `conflicts`, so no question is filed.\n")
    parsed = record_lib.blocks(wrapped, 1)
    results.check("record/bullet-count", [b.kind for b in parsed],
                  ["bullet", "bullet", "text"])
    results.check("record/bullet-wraps", parsed[0].end, 2)
    results.check("record/bullet-keeps-its-continuation",
                  "do not describe the same cell" in parsed[0].joined, True)
    results.check("record/closing-prose-is-not-in-the-last-bullet",
                  "conflicts" in parsed[1].joined, False)
    results.check("record/closing-prose-is-its-own-block", parsed[2].start, 4)

    # F-073, second half: `Checked against:` naming nine answers over four lines was read as one
    # line, so six were never resolved and the gate passed over what it had not read.
    declaration = ("Checked against: EP-001/Q-001; EP-001/Q-002; WI-0001/Q-001;\n"
                   "  WI-0001/Q-002; WI-0002/Q-001; WI-0002/Q-002;\n"
                   "  WI-0003/Q-001; WI-0003/Q-002; WI-0004/Q-001\n"
                   "- a bullet ends the declaration\n")
    parsed = record_lib.blocks(declaration, 1)
    results.check("record/declaration-label", parsed[0].label, "Checked against")
    results.check("record/declaration-spans-its-wraps", parsed[0].end, 3)
    results.check("record/declaration-names-all-nine",
                  parsed[0].body.count("Q-0"), 9)
    results.check("record/a-bullet-ends-a-declaration", parsed[1].kind, "bullet")

    # The three label spellings the record actually uses, and the one that is not a label.
    results.check("record/label-colon-inside-bold",
                  record_lib.split_label("- **Status:** `draft` \u2192 `ready`"),
                  ("Status", "`draft` \u2192 `ready`"))
    results.check("record/label-colon-outside-bold",
                  record_lib.split_label("**Severity**: structural"),
                  ("Severity", "structural"))
    results.check("record/label-plain", record_lib.split_label("Component: scripts/lint-claims"),
                  ("Component", "scripts/lint-claims"))
    results.check("record/a-url-is-not-a-declaration",
                  record_lib.split_label("see http://example.com/x for the map"), (None, None))

    # A fence is kept whole and never read as prose — a document under test may legitimately
    # contain a line that looks like a bullet or a table.
    fenced = ("Before the fence.\n\n```\n- not a bullet\n| not | a table |\n```\n\nAfter.\n")
    kinds = [b.kind for b in record_lib.blocks(fenced, 1)]
    results.check("record/fence-is-one-block", kinds, ["text", "fence", "text"])
    results.check("record/paragraphs-skip-fences",
                  [start for start, _ in record_lib.paragraphs(fenced, 1)], [1, 8])

    # `paragraphs` is the coarse unit and must NOT split on a bullet: a claim and the clause
    # qualifying it live in one paragraph however the author laid it out.
    mixed = "A sentence that never recurses.\n- and a list item under it\n\nAnother.\n"
    results.check("record/paragraph-keeps-a-list-with-its-sentence",
                  [len(lines) for _, lines in record_lib.paragraphs(mixed, 1)], [2, 1])

    # Entries: one shape, three records. A journal execution entry is the specimen.
    entry_text = ("## 2026-08-16T11:47:52Z \u2014 implement v0.1.0 \u2014 developer\n"
                  "\n"
                  "- **Item:** WI-0007\n"
                  "- **Decisions:**\n"
                  "  - Sorted with a stable sort so the tie-break falls out of the\n"
                  "    comparator rather than a second pass.\n"
                  "- **Status:** `in-progress` \u2192 `verifying`\n"
                  "\n"
                  "## 2026-08-16T12:02:00Z \u2014 verify v0.1.0 \u2014 qa-engineer\n"
                  "\n"
                  "- **Item:** WI-0007\n")
    found = record_lib.entries(entry_text, 1, level=2)
    results.check("record/entries-count", len(found), 2)
    results.check("record/entry-line", found[0].line, 1)
    results.check("record/entry-field", found[0].value("Item"), "WI-0007")
    results.check("record/entry-field-is-case-insensitive", found[0].value("item"), "WI-0007")
    results.check("record/entry-missing-field", found[0].value("Gates", "absent"), "absent")
    results.check("record/entry-does-not-run-past-the-next-heading",
                  found[0].end < found[1].line, True)
    # A label whose content is the bullets beneath it: reading its own line answers nothing.
    position = [i for i, b in enumerate(found[0].blocks) if b.label == "Decisions"][0]
    children = record_lib.subtree(found[0].blocks, position)
    results.check("record/subtree-picks-up-the-nested-bullets", len(children), 2)
    results.check("record/subtree-stops-at-the-next-sibling",
                  "Status" not in " ".join(b.label or "" for b in children), True)

    # F-056 at block scope: a repeated label is kept, never silently replaced.
    twice = record_lib.labelled(record_lib.blocks("- **Note:** one\n- **Note:** two\n", 1))
    results.check("record/a-repeated-label-is-not-silently-replaced", len(twice["Note"]), 2)

    # Section and table readers agree with the workspace loader that used to own them.
    body = "## One\n\ntext\n\n## Two\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"
    found_sections = record_lib.sections(body, 1)
    results.check("record/sections", sorted(found_sections), ["## One", "## Two"])
    results.check("record/section-line", found_sections["## Two"]["line"], 5)
    rows = record_lib.table_rows(found_sections["## Two"]["text"],
                                 found_sections["## Two"]["line"])
    results.check("record/table-rows", rows, [(["1", "2"], 9)])
    results.check("record/duplicate-headings",
                  [h for h, _ in record_lib.duplicate_headings("## Notes\n\n## Notes\n", 1)],
                  ["## Notes"])
    results.check("record/escaped-pipe-is-one-cell",
                  record_lib.split_row("| a | str \\| None | b |"),
                  ["a", "str | None", "b"])


def run_citations(results) -> None:
    """`path:line` is the most precise citation form, and it was the least checked (F-077)."""
    import tempfile
    with tempfile.TemporaryDirectory() as root:
        os.makedirs(os.path.join(root, "tracker", "items"), exist_ok=True)
        target = os.path.join(root, "notes.md")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write("one\ntwo\nthree\n")
        resolver = claims_lib.CitationResolver(root)
        results.check("citations/a path with no line resolves", resolver.resolve("notes.md"), "")
        results.check("citations/a line inside the file resolves",
                      resolver.resolve("notes.md:2"), "")
        results.check("citations/the last line resolves", resolver.resolve("notes.md:3"), "")
        beyond = resolver.resolve("notes.md:400")
        results.check("citations/a line past the end does not resolve", bool(beyond), True)
        results.check("citations/the message says what is wrong",
                      "points past the end" in beyond, True)
        results.check("citations/a missing file still reports the file",
                      "does not exist" in resolver.resolve("gone.md:2"), True)


def main() -> int:
    results = Results()
    run_accept(results)
    run_reject(results)
    run_dump(results)
    run_frontmatter(results)
    run_report(results)
    run_record(results)
    run_citations(results)
    run_workspace(results)
    run_root_resolution(results)
    run_escaping(results)
    run_scope(results)
    crosscheck_note = run_crosscheck(results)

    print(f"miniyaml self-test: {results.passed} passed, {len(results.failures)} failed")
    print(f"  cross-check: {crosscheck_note}")
    for failure in results.failures:
        print(f"  FAIL {failure}")
    return 1 if results.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
