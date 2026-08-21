#!/usr/bin/env python3
"""The harness's self-test. Run: python3 harness/tests/test_harness.py

Most of it is one idea: **a contamination check that cannot fail is not a check.** Every rule in
`audit.py` gets a transcript that must be rejected and a transcript that must be accepted, so a
rule that quietly stops matching — a renamed tool, a changed stream format, an over-eager
tolerance — fails this file instead of passing a run.

The transcripts here are synthetic, in the shape `claude --output-format stream-json` really
emits (confirmed by running it, ADR-0005 §1): an `assistant` event whose `message.content`
carries `tool_use` blocks with their full input.

Standard library only (ADR-0002).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(HARNESS)
sys.path.insert(0, HARNESS)

import audit  # noqa: E402
import provision  # noqa: E402
import run_iteration  # noqa: E402

PROJECT = "/home/someone/agile-skills-throwaway/expenses"
HOME = "/home/someone"


def transcript(*calls):
    """A stream-json transcript containing the given (tool, input) calls."""
    lines = [json.dumps({"type": "system", "subtype": "init", "session_id": "x"})]
    for name, tool_input in calls:
        lines.append(json.dumps({
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "id": "t1", "name": name,
                                     "input": tool_input}]}}))
    lines.append(json.dumps({"type": "result", "subtype": "success", "is_error": False,
                             "num_turns": 3, "total_cost_usd": 1.5, "permission_denials": [],
                             "result": "done"}))
    return "\n".join(lines) + "\n"


def uses(*calls):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
        handle.write(transcript(*calls))
        path = handle.name
    try:
        events = audit.load_transcript(path)
        return audit.tool_uses(events), events
    finally:
        os.unlink(path)


def worker_violations(*calls, exists=lambda path: True):
    """`exists` defaults to "every path in the fixture is real"; W3's job is the boundary."""
    tool_uses, _ = uses(*calls)
    return audit.audit_worker(tool_uses, PROJECT, HARNESS, REPO, home=HOME, exists=exists)


def sim_violations(*calls):
    tool_uses, _ = uses(*calls)
    return audit.audit_sim(tool_uses, PROJECT, HARNESS,
                           os.path.join(HARNESS, "runs", "it", "SIM-LOG.md"))


def rules(violations):
    return sorted({violation["rule"] for violation in violations})


class TranscriptShape(unittest.TestCase):
    def test_tool_uses_are_recovered_with_their_input(self):
        tool_uses, events = uses(("Bash", {"command": "git status"}),
                                 ("Read", {"file_path": f"{PROJECT}/tracker/board.md"}))
        self.assertEqual([name for name, _ in tool_uses], ["Bash", "Read"])
        self.assertEqual(tool_uses[0][1]["command"], "git status")
        self.assertEqual(audit.result_event(events)["total_cost_usd"], 1.5)

    def test_a_truncated_transcript_does_not_explode(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            handle.write(transcript(("Read", {"file_path": "a"}))[:-40])
            path = handle.name
        try:
            audit.tool_uses(audit.load_transcript(path))
        finally:
            os.unlink(path)


class WorkerBoundary(unittest.TestCase):
    """The worker must never read `harness/` (DESIGN §4)."""

    def test_ordinary_work_is_clean(self):
        self.assertEqual(worker_violations(
            ("Bash", {"command": "python3 .claude/agile-skills/scripts/board-gen ."}),
            ("Read", {"file_path": f"{PROJECT}/tracker/items/WI-0001/item.md"}),
            ("Write", {"file_path": f"{PROJECT}/src/expenses.py", "content": "..."}),
            ("Bash", {"command": "git commit -m 'feat: add people (refs WI-0001)'"}),
            ("Bash", {"command": "python3 -m pytest src/tests -q"}),
        ), [])

    def test_reading_the_harness_directory_fires(self):
        found = worker_violations(
            ("Read", {"file_path": f"{HARNESS}/skills/simulated-human/probe-script.md"}))
        self.assertIn("W1", rules(found))
        self.assertIn("W2", rules(found))

    def test_reading_the_toolkit_repository_fires(self):
        found = worker_violations(("Read", {"file_path": f"{REPO}/methodology/pipeline.yaml"}))
        self.assertIn("W1", rules(found))

    def test_a_forbidden_token_fires_even_without_a_path(self):
        found = worker_violations(
            ("Grep", {"pattern": "PROJECT-QUEUE", "path": f"{PROJECT}"}))
        self.assertEqual(rules(found), ["W2"])

    def test_escaping_the_project_by_relative_path_fires(self):
        found = worker_violations(("Bash", {"command": "cat ~/notes/other-project.md"}))
        self.assertIn("W3", rules(found))

    def test_reading_a_sibling_project_fires(self):
        found = worker_violations(
            ("Read", {"file_path": f"{HOME}/agile-skills-throwaway/tidy/IDEA.md"}))
        self.assertEqual(rules(found), ["W3"])

    def test_a_path_that_is_only_prose_does_not_fire(self):
        """The false positive that stopped a real run: a heredoc writing a question whose
        context quoted the stakeholder's own example folders."""
        command = ("cat > tracker/items/EP-001/questions/Q-001.md <<'EOF'\n"
                   "## Context\n\nYou said you split costs on trips (`~/trips/ski`) and on "
                   "the flat (`~/flat`).\nEOF")
        self.assertEqual(worker_violations(("Bash", {"command": command}),
                                           exists=lambda path: False), [])
        # and the same shape, when the path is real, still fires
        self.assertEqual(rules(worker_violations(("Bash", {"command": "cat ~/trips/ski"}),
                                                 exists=lambda path: True)), ["W3"])

    def test_the_agents_own_state_directory_is_tolerated(self):
        self.assertEqual(worker_violations(
            ("Bash", {"command": f"cat {HOME}/.claude/settings.json"})), [])

    def test_a_new_change_in_the_toolkit_repository_fires(self):
        """W4, against a real git repository — a dirty toolkit tree during a turn is a fault."""
        import subprocess
        with tempfile.TemporaryDirectory() as root:
            subprocess.run(["git", "init", "-q", root], check=True)
            os.makedirs(os.path.join(root, "spec"))
            os.makedirs(os.path.join(root, "meta"))
            with open(os.path.join(root, "spec", "tracked.md"), "w", encoding="utf-8") as h:
                h.write("one\n")
            with open(os.path.join(root, "meta", "notes.md"), "w", encoding="utf-8") as h:
                h.write("one\n")
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                            "commit", "-qm", "init"], cwd=root, check=True)

            before = audit.repo_tree_snapshot(root)
            self.assertEqual(before, [])
            self.assertEqual(audit.audit_repo_tree(root, before), [])

            # the owner editing meta/ during a run is not a contamination event
            with open(os.path.join(root, "meta", "notes.md"), "w", encoding="utf-8") as h:
                h.write("two\n")
            self.assertEqual(audit.audit_repo_tree(root, before), [])

            # a change to the toolkit under test is
            with open(os.path.join(root, "spec", "tracked.md"), "w", encoding="utf-8") as h:
                h.write("two\n")
            found = audit.audit_repo_tree(root, before)
            self.assertEqual(rules(found), ["W4"])
            self.assertIn("spec/tracked.md", found[0]["evidence"])

            # a change that was already there before the turn is the owner's, not the turn's
            self.assertEqual(audit.audit_repo_tree(root, audit.repo_tree_snapshot(root)), [])


class SimBoundary(unittest.TestCase):
    """The sim touches only what a real human could (DESIGN §4)."""

    LOG = os.path.join(HARNESS, "runs", "it", "SIM-LOG.md")

    def test_answering_a_question_is_clean(self):
        self.assertEqual(sim_violations(
            ("Read", {"file_path": f"{PROJECT}/tracker/board.md"}),
            ("Edit", {"file_path": f"{PROJECT}/tracker/items/WI-0002/questions/Q-001.md",
                      "old_string": "## Answer\n", "new_string": "## Answer\n\n[human] Yes.\n"}),
            ("Write", {"file_path": f"{PROJECT}/IDEA.md", "content": "an idea"}),
            ("Write", {"file_path": self.LOG, "content": "## Turn 3"}),
        ), [])

    def test_writing_to_the_source_tree_fires(self):
        found = sim_violations(
            ("Write", {"file_path": f"{PROJECT}/src/expenses.py", "content": "print(1)"}))
        self.assertEqual(rules(found), ["S1"])

    def test_editing_an_item_fires(self):
        found = sim_violations(
            ("Edit", {"file_path": f"{PROJECT}/tracker/items/WI-0002/item.md",
                      "old_string": "draft", "new_string": "ready"}))
        self.assertEqual(rules(found), ["S1"])

    def test_editing_a_question_on_another_project_fires(self):
        found = sim_violations(
            ("Edit", {"file_path": "/home/someone/agile-skills-throwaway/tidy/tracker/items/"
                                   "WI-0001/questions/Q-001.md",
                      "old_string": "a", "new_string": "b"}))
        self.assertEqual(rules(found), ["S1"])

    def test_a_shell_fires_even_when_it_does_nothing(self):
        found = sim_violations(("Bash", {"command": "ls"}))
        self.assertEqual(rules(found), ["S2"])

    def test_running_a_transition_fires(self):
        found = sim_violations(
            ("Bash", {"command": "python3 .claude/agile-skills/scripts/transition WI-0002 "
                                 "--to ready --actor refine --reason x"}))
        self.assertEqual(rules(found), ["S2"])


class SimTreeBoundary(unittest.TestCase):
    """The disk-side check: the sim may fill in `## Answer` and nothing else."""

    QUESTION = """---
id: Q-001
item: WI-0002
from-skill: refine
addressed-to: human
blocking: true
status: {status}
created: 2026-08-21T10:00:00Z
---

## Context

c

## Question

q

## Answer

{answer}

## Consequences

"""

    def make_project(self, root, status="open", answer=""):
        directory = os.path.join(root, "tracker", "items", "WI-0002", "questions")
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, "Q-001.md"), "w", encoding="utf-8") as handle:
            handle.write(self.QUESTION.format(status=status, answer=answer))
        return os.path.join(directory, "Q-001.md")

    def test_filling_in_the_answer_is_clean(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.make_project(root)
            before = audit.question_frontmatter_snapshot(root)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(self.QUESTION.format(status="open", answer="[human] Yes."))
            self.assertEqual(audit.audit_sim_tree(root, before), [])

    def test_closing_the_question_fires(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.make_project(root)
            before = audit.question_frontmatter_snapshot(root)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(self.QUESTION.format(status="answered", answer="[human] Yes."))
            found = audit.audit_sim_tree(root, before)
            self.assertEqual(rules(found), ["S3"])

    def test_deleting_the_question_fires(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.make_project(root)
            before = audit.question_frontmatter_snapshot(root)
            os.unlink(path)
            self.assertEqual(rules(audit.audit_sim_tree(root, before)), ["S3"])


class WorkspaceReading(unittest.TestCase):
    def test_frontmatter_stops_at_the_closing_fence(self):
        parsed = audit.frontmatter("---\nid: Q-001\nstatus: open\n---\n\nstatus: not-this\n")
        self.assertEqual(parsed, {"id": "Q-001", "status": "open"})

    def test_an_answered_question_is_recognised_and_an_empty_one_is_not(self):
        with tempfile.TemporaryDirectory() as root:
            directory = os.path.join(root, "tracker", "items", "WI-0002", "questions")
            os.makedirs(directory)
            empty = SimTreeBoundary.QUESTION.format(status="open", answer="")
            filled = SimTreeBoundary.QUESTION.format(status="open", answer="[human] Yes.")
            with open(os.path.join(directory, "Q-001.md"), "w", encoding="utf-8") as handle:
                handle.write(empty.replace("\n\n\n", "\n<!-- filled in by the human -->\n"))
            with open(os.path.join(directory, "Q-002.md"), "w", encoding="utf-8") as handle:
                handle.write(filled.replace("id: Q-001", "id: Q-002"))
            # scan_project runs the validator, which this fixture has no toolkit for; the
            # question reading is what is under test, so call it the way scan_project does.
            states = {}
            for path in audit.question_files(root):
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
                body = text.split("\n## Answer", 1)[1].split("\n## ", 1)[0]
                body = "\n".join(line for line in body.split("\n")
                                 if not line.strip().startswith("<!--")).strip()
                states[audit.frontmatter(text)["id"]] = bool(body)
            self.assertEqual(states, {"Q-001": False, "Q-002": True})

    def test_the_worker_status_block_is_read_from_the_last_json_fence(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "HARNESS-STATUS.md"), "w", encoding="utf-8") as handle:
                handle.write("# Harness status\n\nSome prose.\n\n"
                             "```json\n{\"stop_reason\": \"nothing-runnable\"}\n```\n\n"
                             "```json\n{\"stop_reason\": \"human-question-open\", "
                             "\"open_human_questions\": [\"WI-0002/Q-001\"]}\n```\n")
            report, text = run_iteration.worker_report(root)
            self.assertEqual(report["stop_reason"], "human-question-open")
            self.assertIn("Some prose.", text)

    def test_a_status_file_with_no_json_block_is_not_fatal(self):
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "HARNESS-STATUS.md"), "w", encoding="utf-8") as handle:
                handle.write("I stopped because I felt like it.\n")
            report, text = run_iteration.worker_report(root)
            self.assertIsNone(report)
            self.assertTrue(text)


class Configuration(unittest.TestCase):
    def test_the_allow_list_still_matches_usage_section_4(self):
        """provision.py copies USAGE §4's allow-list. If the document changes, so must it."""
        with open(os.path.join(REPO, "USAGE.md"), encoding="utf-8") as handle:
            usage = handle.read()
        block = usage.split("```json", 1)[1].split("```", 1)[0]
        documented = json.loads(block)["permissions"]["allow"]
        self.assertEqual(documented, provision.ALLOW_LIST)

    def test_every_iteration_config_names_files_that_exist(self):
        directory = os.path.join(HARNESS, "iterations")
        configs = [name for name in sorted(os.listdir(directory)) if name.endswith(".json")]
        self.assertTrue(configs)
        for name in configs:
            with open(os.path.join(directory, name), encoding="utf-8") as handle:
                config = json.load(handle)
            self.assertEqual(config["id"], name[:-5])
            for kind, key in (("personas", "persona"), ("probes", "probe")):
                path = os.path.join(HARNESS, "skills", "simulated-human", kind,
                                    f"{config[key]}.md")
                self.assertTrue(os.path.isfile(path), f"{name}: missing {path}")

    def test_both_turn_prompts_carry_a_version_and_a_body(self):
        for name in ("worker-turn", "sim-turn"):
            body, version = run_iteration.prompt_text(name)
            self.assertNotEqual(version, "unknown", name)
            self.assertGreater(len(body), 200, name)
            self.assertNotIn("{{", run_iteration.fill(body, {
                "PROJECT_DIR": "/p", "TURN": 1, "STATUS_FILE": "S.md", "SIM_LOG": "/l",
                "PERSONA_FILE": "/p.md", "PROBE_FILE": "/q.md", "JOB": "answer",
                "NOW": "2026-08-21T00:00:00Z"}), name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
