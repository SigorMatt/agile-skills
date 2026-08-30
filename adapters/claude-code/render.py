#!/usr/bin/env python3
"""Render methodology/ into installable skills for this runtime.

Usage:
  adapters/claude-code/render.py            write dist/
  adapters/claude-code/render.py --check    render to a temp dir and diff against dist/

Reads only what the adapter contract allows (adapters/README.md §1): each skill's `skill.yaml`
and `process.md`, `methodology/pipeline.yaml`, and `spec/`. It contains no per-skill knowledge —
every difference between rendered skills comes from a declared contract field. If you are
tempted to add `if name == "implement"`, add a field to `spec/skill-contract.md` instead.

Rendering is byte-deterministic: no timestamps, no host paths, no set iteration order. The
repository gate re-renders and diffs, which only means anything if that holds.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import filecmp
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts", "lib"))

import miniyaml  # noqa: E402

# Format facts confirmed against the runtime's documentation; see
# meta/adr/ADR-0001-claude-code-skill-format.md for the URLs and the date they were fetched.
DESCRIPTION_LIMIT = 1536
BODY_LINE_LIMIT = 500

# Where the installer puts shared material inside a consumer project. Skills refer to these by
# project-relative path, which is unambiguous however the runtime resolves a skill's own
# directory.
SHARED_DIR = ".claude/agile-skills"

SCRIPTS_TO_SHIP = [
    "validate-workspace", "board-gen", "workspace-init", "new-item",
    "check-commit-refs", "check-verify-freshness", "run-gate", "transition",
    "journal-entry", "lint-claims", "lint-answers", "check-epic-signoff",
    "engagement-state", "export",
]
LIB_TO_SHIP = ["miniyaml.py", "frontmatter.py", "report.py", "record.py",
               "workspace.py", "board.py", "claims.py", "engagement.py", "scope.py",
               "textio.py"]
SPEC_TO_SHIP = [
    "README.md", "ids-and-statuses.md", "work-item.md", "journal-and-history.md",
    "question.md", "request.md", "doc-header.md", "dor-dod.md", "skill-contract.md",
    "workspace-layout.md", "retro.md",
]

# A skill that must not be able to ask the human has the capability removed by the runtime,
# not merely discouraged in prose (adapters/README.md capability C2).
NO_HUMAN_TOOLS = "AskUserQuestion"


class RenderError(Exception):
    pass


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def load_contracts():
    pipeline = miniyaml.load_file(os.path.join(ROOT, "methodology", "pipeline.yaml"))
    skills = []
    for name in pipeline.get("skills") or []:
        directory = os.path.join(ROOT, "methodology", "skills", name)
        contract = miniyaml.load_file(os.path.join(directory, "skill.yaml"))
        process = read(os.path.join(directory, "process.md"))
        skills.append((name, contract, process))
    return pipeline, skills


def build_description(contract: dict) -> str:
    """purpose + the concrete situations, situations first-ish and never truncated silently.

    The runtime matches a request against this text and shortens it when many skills are
    installed, so the situations must be early and the whole thing must stay under the cap.
    """
    situations = "; ".join(situation.rstrip(".") for situation in contract["when_to_use"])
    description = (f"{contract['purpose']} Use when: {situations}. "
                   f"Part of the agile-skills pipeline "
                   f"(persona: {contract['persona']}).")
    if len(description) > DESCRIPTION_LIMIT:
        raise RenderError(
            f"{contract['name']}: description is {len(description)} characters, over the "
            f"{DESCRIPTION_LIMIT} limit; shorten purpose or when_to_use in skill.yaml")
    return description


def render_frontmatter(contract: dict) -> tuple:
    """Return (frontmatter text, list of runtime-only fields used).

    Only the fields that are portable outside this runtime are emitted by default, so a
    rendered skill is also a valid package elsewhere (ADR-0001). A runtime-only field is used
    only where a contract genuinely requires it, and is reported in the manifest.
    """
    fields = {
        "name": contract["name"],
        "description": build_description(contract),
    }
    runtime_only = []
    if contract["human_interaction"] != "direct":
        # Structural enforcement of R2: these skills file questions, they do not ask people.
        fields["disallowed-tools"] = NO_HUMAN_TOOLS
        runtime_only.append("disallowed-tools")
    fields["metadata"] = {
        "methodology-skill": contract["name"],
        "methodology-version": contract["version"],
        "persona": contract["persona"],
        "human-interaction": contract["human_interaction"],
    }
    return miniyaml.dump_frontmatter(fields), runtime_only


def gate_command(command: str) -> str:
    """Map a methodology gate command onto its installed location."""
    if command.startswith("scripts/"):
        return f"{SHARED_DIR}/{command}"
    return command


def render_contract_reference(contract: dict) -> str:
    lines = [
        f"# Contract — {contract['name']} v{contract['version']}",
        "",
        "Rendered from `methodology/skills/"
        f"{contract['name']}/skill.yaml`. This is the authoritative list of what this skill "
        "must read, must produce, and must not skip. Open it when you need the exact gate "
        "list or the exit criteria; the procedure in SKILL.md is the how.",
        "",
        f"- **Persona:** {contract['persona']}",
        f"- **Purpose:** {contract['purpose']}",
        f"- **Human interaction:** {contract['human_interaction']}",
        f"- **Dispatched on statuses:** "
        + (", ".join(f"`{s}`" for s in contract["dispatch"]["on_status"]) or "none — this skill is invoked directly, not scheduled"),
        f"- **Item types:** "
        + (", ".join(f"`{t}`" for t in contract["dispatch"]["item_types"]) or "not applicable"),
        f"- **On success:** " + (f"`{contract['next_status']}`" if contract["next_status"]
                                 else "no status transition of its own"),
        f"- **On unrecoverable failure:** "
        + (f"`{contract['failure_status']}`" if contract["failure_status"] else "none"),
        "",
        "## Inputs — every one of these must actually be read",
        "",
        "| path | required | why |",
        "|------|----------|-----|",
    ]
    for entry in contract["inputs"]:
        lines.append(f"| `{entry['path']}` | {'yes' if entry['required'] else 'no'} "
                     f"| {entry['why']} |")

    lines += ["", "## Outputs", "", "| path | kind | when |", "|------|------|------|"]
    for entry in contract["outputs"]:
        lines.append(f"| `{entry['path']}` | {entry['kind']} | {entry['when']} |")

    lines += ["", "## Quality gates", "",
              "Every gate below appears in the journal entry for every execution — including "
              "gates that were skipped, with the reason. A gate silently omitted is the "
              "failure the journal format exists to prevent.",
              "", "| gate | enforcement | how it is checked | on failure |",
              "|------|-------------|-------------------|------------|"]
    for gate in contract["quality_gates"]:
        if gate.get("command"):
            how = f"run `{gate_command(gate['command'])}`, expect {gate.get('expect', 'exit-zero')}"
        else:
            how = gate["manual_check"]
        lines.append(f"| `{gate['name']}` | {gate['enforcement']} | {how} "
                     f"| {gate['on_failure']} |")

    lines += ["", "## Escalation", ""]
    for key in ("question", "defect", "impasse"):
        lines.append(f"- **{key}:** {contract['escalation'][key]}")

    lines += ["", "## Exit criteria — all must be true before transitioning", ""]
    for criterion in contract["exit_criteria"]:
        lines.append(f"- [ ] {criterion}")

    lines += [
        "",
        "## Schemas this skill writes against",
        "",
        f"- Item and body schema — `{SHARED_DIR}/spec/work-item.md`",
        f"- Journal and history formats — `{SHARED_DIR}/spec/journal-and-history.md`",
        f"- Question protocol — `{SHARED_DIR}/spec/question.md`",
        f"- Document headers and ADRs — `{SHARED_DIR}/spec/doc-header.md`",
        f"- Definition of Ready and Done — `{SHARED_DIR}/spec/dor-dod.md`",
        f"- IDs, statuses, transitions — `{SHARED_DIR}/spec/ids-and-statuses.md`",
        f"- Workspace layout — `{SHARED_DIR}/spec/workspace-layout.md`",
        "",
    ]
    return "\n".join(lines)


def render_skill_body(contract: dict, process: str) -> str:
    name = contract["name"]
    gates = contract["quality_gates"]
    hard = [gate["name"] for gate in gates if gate["enforcement"] == "hard"]

    header = [
        f"You are running the **{name}** skill of the agile-skills pipeline, "
        f"as the **{contract['persona']}**.",
        "",
        "**Before you start, read these two files. They are the contract you are held to:**",
        "",
        f"- [references/contract.md](references/contract.md) — inputs, outputs, gates, "
        f"exit criteria for this skill.",
        f"- `{SHARED_DIR}/spec/journal-and-history.md` — the format of the record you must "
        f"leave behind.",
        "",
        "At a glance:",
        "",
        f"- Runs on items at status: "
        + (", ".join(f"`{s}`" for s in contract["dispatch"]["on_status"])
           or "_not scheduled — invoked directly_"),
        f"- Human interaction: **{contract['human_interaction']}**"
        + ("" if contract["human_interaction"] == "direct"
           else " — you may not ask a person; file a question artifact instead"),
        f"- Hard gates: " + (", ".join(f"`{g}`" for g in hard) or "none"),
        f"- On success: " + (f"`{contract['next_status']}`" if contract["next_status"]
                             else "no transition of its own"),
        "",
        "Gate commands, when this skill runs them, live under "
        f"`{SHARED_DIR}/scripts/`. Run them; do not simulate them. They find the workspace "
        "root themselves, so run them from wherever you are — never `cd` in order to run one, "
        "and never join one to another command with `&&` or `;`. "
        f"**`{SHARED_DIR}/scripts/transition` is a checkpoint:** issue it alone, read its exit "
        "code, and journal the move only after it has reported success (spec/skill-contract.md "
        "\u00a72.3).",
        "",
        "---",
        "",
    ]

    # process.md's first line is its own title; the rendered file supplies its own.
    body_lines = process.split("\n")
    if body_lines and body_lines[0].startswith("# "):
        body_lines = body_lines[1:]
    while body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    footer = [
        "",
        "---",
        "",
        "## Additional resources",
        "",
        "- [references/contract.md](references/contract.md) — this skill's full contract: "
        "inputs, outputs, every gate, and the exit criteria checklist.",
        f"- `{SHARED_DIR}/spec/` — the schemas every artifact must satisfy.",
        f"- `{SHARED_DIR}/pipeline.yaml` — the status graph and the orchestrator's algorithm.",
        f"- `{SHARED_DIR}/scripts/` — the executable gates. `validate-workspace` is the one "
        "every skill runs.",
        "",
    ]

    text = "\n".join(header + body_lines + footer)
    line_count = len(text.split("\n"))
    if line_count > BODY_LINE_LIMIT:
        raise RenderError(
            f"{name}: SKILL.md body is {line_count} lines, over the {BODY_LINE_LIMIT} limit; "
            f"move reference material out of process.md into spec/")
    return text


def render_manifest(pipeline: dict, rendered: list) -> str:
    lines = [
        "# Rendered skills — manifest",
        "",
        "Generated by `adapters/claude-code/render.py` from `methodology/`. Do not edit by "
        "hand: `scripts/check` re-renders and diffs, so an edit here fails the build.",
        "",
        f"- Pipeline version: `{pipeline['version']}`",
        f"- Skills rendered: {len(rendered)}",
        "",
        "| skill | version | persona | human interaction | runtime-only frontmatter |",
        "|-------|---------|---------|-------------------|--------------------------|",
    ]
    for name, contract, runtime_only in rendered:
        lines.append(f"| `{name}` | {contract['version']} | {contract['persona']} "
                     f"| {contract['human_interaction']} "
                     f"| {', '.join(runtime_only) if runtime_only else '— (portable)'} |")
    lines += [
        "",
        "**Runtime-only frontmatter** means a field outside the portable Agent Skills field "
        "set. A skill with none is also a valid package for other distribution paths; a skill "
        "with some is not, and that is a deliberate trade recorded in "
        "`meta/adr/ADR-0001-claude-code-skill-format.md`. `disallowed-tools` is used to remove "
        "the ability to question a human from every skill whose contract says it must file a "
        "question instead — enforcement rather than instruction.",
        "",
        "## Installed layout",
        "",
        "```",
        "<project>/",
        "├── .claude/skills/<skill>/SKILL.md",
        "├── .claude/skills/<skill>/references/contract.md",
        f"└── {SHARED_DIR}/",
        "    ├── VERSION",
        "    ├── pipeline.yaml",
        "    ├── spec/",
        "    └── scripts/",
        "```",
        "",
    ]
    return "\n".join(lines)


def render_into(destination: str) -> list:
    pipeline, skills = load_contracts()
    rendered = []

    for name, contract, process in skills:
        frontmatter_text, runtime_only = render_frontmatter(contract)
        body = render_skill_body(contract, process)
        write(os.path.join(destination, "skills", name, "SKILL.md"),
              f"---\n{frontmatter_text}---\n\n{body}")
        write(os.path.join(destination, "skills", name, "references", "contract.md"),
              render_contract_reference(contract))
        rendered.append((name, contract, runtime_only))

    shared = os.path.join(destination, "agile-skills")
    write(os.path.join(shared, "VERSION"),
          f"pipeline {pipeline['version']}\n"
          + "".join(f"{name} {contract['version']}\n" for name, contract, _ in rendered))
    shutil.copyfile(os.path.join(ROOT, "methodology", "pipeline.yaml"),
                    os.path.join(shared, "pipeline.yaml"))
    for name in SPEC_TO_SHIP:
        os.makedirs(os.path.join(shared, "spec"), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, "spec", name),
                        os.path.join(shared, "spec", name))
    os.makedirs(os.path.join(shared, "scripts", "lib"), exist_ok=True)
    for name in SCRIPTS_TO_SHIP:
        source = os.path.join(ROOT, "scripts", name)
        if not os.path.isfile(source):
            # run-gate arrives with META-042; a missing script must be visible, not silent.
            print(f"render: WARNING scripts/{name} does not exist yet; not shipped",
                  file=sys.stderr)
            continue
        target = os.path.join(shared, "scripts", name)
        shutil.copyfile(source, target)
        os.chmod(target, 0o755)
    for name in LIB_TO_SHIP:
        shutil.copyfile(os.path.join(ROOT, "scripts", "lib", name),
                        os.path.join(shared, "scripts", "lib", name))
    # validate-workspace looks for pipeline.yaml beside itself before ../methodology/.
    shutil.copyfile(os.path.join(ROOT, "methodology", "pipeline.yaml"),
                    os.path.join(shared, "scripts", "pipeline.yaml"))
    # run-gate needs the machine-readable contracts, not the rendered prose form of them.
    for name, _, _ in rendered:
        os.makedirs(os.path.join(shared, "skills", name), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, "methodology", "skills", name, "skill.yaml"),
                        os.path.join(shared, "skills", name, "skill.yaml"))

    write(os.path.join(destination, "MANIFEST.md"), render_manifest(pipeline, rendered))
    return rendered


def tree_differences(left: str, right: str, prefix: str = "") -> list:
    """Recursive comparison that reports paths, not a boolean."""
    differences = []
    comparison = filecmp.dircmp(left, right)
    for name in sorted(comparison.left_only):
        differences.append(f"only in the fresh render: {os.path.join(prefix, name)}")
    for name in sorted(comparison.right_only):
        differences.append(f"only in the committed dist: {os.path.join(prefix, name)}")
    for name in sorted(comparison.diff_files):
        differences.append(f"differs: {os.path.join(prefix, name)}")
    for name in sorted(comparison.common_dirs):
        differences += tree_differences(os.path.join(left, name), os.path.join(right, name),
                                        os.path.join(prefix, name))
    return differences


def main(argv: list) -> int:
    dist = os.path.join(HERE, "dist")
    check_only = "--check" in argv

    if check_only:
        if not os.path.isdir(dist):
            print("render: dist/ does not exist; run adapters/claude-code/render.py",
                  file=sys.stderr)
            return 1
        with tempfile.TemporaryDirectory() as temporary:
            try:
                render_into(temporary)
            except RenderError as exc:
                print(f"render: {exc}", file=sys.stderr)
                return 1
            differences = tree_differences(temporary, dist)
        if differences:
            print("render: the committed dist/ is not what methodology/ renders to:",
                  file=sys.stderr)
            for line in differences:
                print(f"  {line}", file=sys.stderr)
            print("  run adapters/claude-code/render.py and commit the result",
                  file=sys.stderr)
            return 1
        print("render: dist/ is current")
        return 0

    if os.path.isdir(dist):
        shutil.rmtree(dist)
    try:
        rendered = render_into(dist)
    except RenderError as exc:
        print(f"render: {exc}", file=sys.stderr)
        return 1
    print(f"render: wrote {len(rendered)} skill(s) to "
          f"{os.path.relpath(dist, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
