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

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

HARNESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(HARNESS)
sys.path.insert(0, HARNESS)

import audit  # noqa: E402
import provision  # noqa: E402
import run_iteration  # noqa: E402
from ops import status as ops_status  # noqa: E402
from ops import watch as ops_watch  # noqa: E402

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


def worker_violations(*calls, exists=lambda path, source: True):
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
                                           exists=audit.plausible), [])
        # and the same shape, when the path is real, still fires
        self.assertEqual(rules(worker_violations(
            ("Bash", {"command": f"cat {HOME}/trips/ski"}),
            exists=lambda path, source: True)), ["W3"])

    def test_a_write_to_a_file_that_does_not_exist_yet_still_fires(self):
        """A `file_path` argument is a path the session meant; the file need not exist."""
        found = worker_violations(
            ("Write", {"file_path": f"{HOME}/notes/new-file.md", "content": "x"}),
            exists=lambda path, source: source == "key")
        self.assertEqual(rules(found), ["W3"])

    def test_a_bare_tilde_is_not_a_path(self):
        """Both of these stopped a real run before the rule was tightened."""
        self.assertEqual(worker_violations(
            ("Bash", {"command": "echo \"$out\" | head -3 | tr '\\n' '~'"}),
            exists=audit.plausible), [])
        self.assertEqual(worker_violations(
            ("Bash", {"command": "cat >> review.md <<'EOF'\n- **~~The two store paths~~** "
                                 "struck out because the finding was closed.\nEOF"}),
            exists=audit.plausible), [])
        # `~/` still means home
        self.assertEqual(rules(worker_violations(
            ("Bash", {"command": "cat ~/secrets.txt"}),
            exists=lambda path, source: True)), ["W3"])

    def test_a_heredoc_body_is_a_document_not_a_path(self):
        """H-009: the body of a heredoc is being written, not reached for.

        `plausible()` separates prose from a command by asking whether the path exists. That
        stops working the moment the prose names a real folder, which is what iteration 2 did.
        The structure is what tells them apart, so `exists` is pinned to "everything is real"
        here — this asserts the structural rule, not the existence filter standing in for it.
        """
        command = ("cd " + PROJECT + "\n"
                   "python3 - <<'PYEOF'\n"
                   "body = 'Anything scripting the tool — `tidy ~/Downloads --apply` — "
                   "treats a successful run as a failure.'\n"
                   "PYEOF")
        self.assertEqual(worker_violations(("Bash", {"command": command})), [])
        # the introducer's own line is still a command, and still scraped
        self.assertEqual(rules(worker_violations(
            ("Bash", {"command": f"cat {HOME}/notes.md <<'EOF'\n~/Downloads\nEOF"}))), ["W3"])
        # an unterminated heredoc swallows the rest rather than reopening the hole
        self.assertEqual(worker_violations(
            ("Bash", {"command": "cat <<'EOF'\n~/Downloads"})), [])
        # `<<<` is a here-string, not a heredoc
        self.assertEqual(rules(worker_violations(
            ("Bash", {"command": "grep x <<< ~/Downloads/list.txt"}))), ["W3"])

    def test_iteration_2_tidy_turn_6_is_clean(self):
        """The real transcript that stopped iteration 2, audited by the fixed rule (H-009).

        Turn 6 wrote BUG-0002's report with `python3 - <<'PYEOF'`, and the report says that
        anything scripting the tool — `tidy ~/Downloads --apply` — treats a successful run as a
        failure. W3 scraped that out of the command string, `/home/msi/Downloads` exists on the
        machine the run was on, and the driver stopped the run for contamination at turn 6.

        Pinning `exists` to "everything is real" is the point: this file must fail if the fix is
        reverted, on a machine where that folder does not exist as much as on the one where it
        does.
        """
        path = os.path.join(HARNESS, "runs", "iteration-2-tidy", "turns",
                            "006-worker.stream.jsonl")
        if not os.path.isfile(path):
            self.skipTest("iteration 2's turn-6 transcript is not in this checkout")
        tool_uses = audit.tool_uses(audit.load_transcript(path))
        self.assertTrue(tool_uses, "the transcript parsed to no tool calls")
        found = audit.audit_worker(tool_uses, "/home/msi/agile-skills-throwaway/tidy",
                                   HARNESS, REPO, home="/home/msi",
                                   exists=lambda path, source: True)
        self.assertEqual(found, [], "iteration 2 turn 6 is clean; it was stopped by H-009")

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

    def test_an_archived_run_directory_is_marked_terminal(self):
        """`--fresh` used to leave an archive saying it was still running, with a live pid."""
        with tempfile.TemporaryDirectory() as root:
            run_dir = os.path.join(root, "iteration-x.1")
            os.makedirs(run_dir)
            with open(os.path.join(run_dir, "state.json"), "w", encoding="utf-8") as handle:
                json.dump({"status": "running", "turn": 4}, handle)
            with open(os.path.join(run_dir, "driver.pid"), "w", encoding="utf-8") as handle:
                handle.write("222595\n")
            run_iteration.mark_archived(run_dir, when="2026-08-30T12:00:00Z")
            with open(os.path.join(run_dir, "state.json"), encoding="utf-8") as handle:
                state = json.load(handle)
            self.assertEqual(state["status"], "archived")
            self.assertEqual(state["archived-from-status"], "running")
            self.assertEqual(state["turn"], 4)
            self.assertFalse(os.path.exists(os.path.join(run_dir, "driver.pid")))
            self.assertTrue(os.path.isfile(os.path.join(run_dir, "ARCHIVED.md")))

    def test_marking_an_archive_survives_a_state_file_it_cannot_read(self):
        with tempfile.TemporaryDirectory() as root:
            run_dir = os.path.join(root, "iteration-y.2")
            os.makedirs(run_dir)
            with open(os.path.join(run_dir, "state.json"), "w", encoding="utf-8") as handle:
                handle.write("{ this is not json")
            run_iteration.mark_archived(run_dir, when="2026-08-30T12:00:00Z")
            self.assertTrue(os.path.isfile(os.path.join(run_dir, "ARCHIVED.md")))

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

    def test_a_status_file_stamped_for_another_turn_is_not_this_turn_s_report(self):
        """H-017: 4c's turn 16 exited cleanly having written nothing.

        No commit, no tracker change and no status file — so the mtime test H-005 added could
        not see it, and turn 17's driver consumed turn 15's heading as though it were current.
        The turn number is in the heading the prompt already asks for; the driver reads it.
        """
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, "HARNESS-STATUS.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("# Harness status — turn 15\n\nWhat turn 15 did.\n\n"
                             "```json\n{\"stop_reason\": \"nothing-runnable\"}\n```\n")
            stale, text = run_iteration.worker_report(root, turn=17)
            self.assertIsNone(stale)
            self.assertEqual(text, "")
            fresh, text = run_iteration.worker_report(root, turn=15)
            self.assertEqual(fresh["stop_reason"], "nothing-runnable")
            self.assertIn("What turn 15 did.", text)

    def test_a_status_file_with_no_turn_in_its_heading_is_refused_when_a_turn_is_named(self):
        """A heading the prompt's own template would not produce cannot be attributed."""
        with tempfile.TemporaryDirectory() as root:
            with open(os.path.join(root, "HARNESS-STATUS.md"), "w", encoding="utf-8") as handle:
                handle.write("# Harness status\n\n```json\n{\"stop_reason\": \"error\"}\n"
                             "```\n")
            report, text = run_iteration.worker_report(root, turn=3)
            self.assertIsNone(report)
            self.assertEqual(text, "")

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

    def test_every_turn_prompt_carries_a_version_and_a_body(self):
        for name in ("worker-turn", "sim-turn", "repair-turn"):
            body, version = run_iteration.prompt_text(name)
            self.assertNotEqual(version, "unknown", name)
            self.assertGreater(len(body), 200, name)
            self.assertNotIn("{{", run_iteration.fill(body, {
                "PROJECT_DIR": "/p", "TURN": 1, "STATUS_FILE": "S.md", "SIM_LOG": "/l",
                "PERSONA_FILE": "/p.md", "PROBE_FILE": "/q.md", "JOB": "answer",
                "SKILLS_PER_TURN": 3, "NOW": "2026-08-21T00:00:00Z",
                "VALIDATOR_ERROR": "e", "ORIGINAL_ERROR": "e", "ATTEMPT": 1,
                "REPAIR_TURNS": 2}), name)


class StopClassification(unittest.TestCase):
    """H-002: a stop is either an interruption you resume or a verdict you do not."""

    def test_an_interrupted_turn_is_resumable(self):
        for reason in ("turn-failed", "turn-timeout", "api-rejected"):
            self.assertTrue(run_iteration.stop_is_resumable(reason), reason)

    def test_a_verdict_is_not_resumable(self):
        for reason in ("epic-done", "blocked-no-recourse", "contamination",
                       "validator-failed", "stalled", "abandoned"):
            self.assertFalse(run_iteration.stop_is_resumable(reason), reason)

    def test_a_budget_stop_is_resumable_unless_the_engagement_ended(self):
        """H-010: a budget bounds this run's work, not the engagement.

        Five occurrences in three iterations, two of them landing between the sign-off being
        filed and the stakeholder answering it. The workaround — --fresh against the same
        project — worked, and the cost reached the person: "I was asked to sign off twice for
        the same engagement, six hours apart."
        """
        mid_run = TerminalWorkspace.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "planned"},
        })
        self.assertTrue(run_iteration.stop_is_resumable("turn-budget", mid_run))
        ended = TerminalWorkspace.observed({
            "EP-001": {"type": "epic", "status": "done"},
            "WI-0001": {"type": "work-item", "status": "done"},
        })
        self.assertFalse(run_iteration.stop_is_resumable("turn-budget", ended))

    def test_a_caller_that_cannot_see_the_workspace_gets_no_benefit_of_the_doubt(self):
        """Without a reading, only the unconditional stops resume. Silence is not evidence."""
        self.assertFalse(run_iteration.stop_is_resumable("turn-budget"))
        self.assertTrue(run_iteration.stop_is_resumable("turn-timeout"))

    def test_every_conditional_stop_is_also_described_as_terminal(self):
        """A stop that can be either has to have both explanations, or one reading is missing."""
        for reason in run_iteration.CONDITIONAL_STOPS:
            self.assertIn(reason, run_iteration.TERMINAL_STOPS, reason)

    def test_every_stop_reason_the_driver_emits_is_classified(self):
        """A stop nobody classified would silently fall through to 'terminal'."""
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        emitted = set(re.findall(r'self\.stop\(\s*"([a-z-]+)"', source))
        known = set(run_iteration.RESUMABLE_STOPS) | set(run_iteration.TERMINAL_STOPS)
        self.assertEqual(emitted - known, set(),
                         "stop reasons the driver emits but neither table names")

    def test_an_unknown_reason_is_treated_as_terminal(self):
        self.assertFalse(run_iteration.stop_is_resumable("something-new"))

    def test_a_limit_rejection_is_recognised_and_ordinary_output_is_not(self):
        self.assertTrue(run_iteration.looks_api_rejected(
            "API Error: 429 rate_limit_error: usage limit reached"))
        self.assertTrue(run_iteration.looks_api_rejected("Authentication failed"))
        self.assertFalse(run_iteration.looks_api_rejected(
            "the worker reported: tests failed, 3 of 14"))
        self.assertFalse(run_iteration.looks_api_rejected(""))


class EngagementRest(unittest.TestCase):
    """H-008: an impasse is a fact about the engagement, not about one item.

    The driver used to stop on `any item is blocked`. That coincided with the truth in iteration
    1d, where the blocked item was the last one standing. It stopped coinciding the moment the
    deferral fix parked a blocked item at turn 4 with three items still to build — and the run
    would have ended, terminally, with most of its work unwritten.
    """

    @staticmethod
    def observed(items, questions=()):
        return {"items": items,
                "questions": [dict({"status": "open"}, **q) for q in questions]}

    def test_a_blocked_item_beside_work_in_flight_is_not_rest(self):
        observed = self.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "planned"},
            "WI-0003": {"type": "work-item", "status": "blocked"},
        })
        self.assertFalse(run_iteration.engagement_at_rest(observed))

    def test_every_child_stopped_and_nothing_open_is_rest(self):
        observed = self.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "done"},
            "WI-0003": {"type": "work-item", "status": "blocked"},
        })
        self.assertTrue(run_iteration.engagement_at_rest(observed))

    def test_an_open_question_anywhere_is_not_rest(self):
        observed = self.observed(
            {"EP-001": {"type": "epic", "status": "open"},
             "WI-0001": {"type": "work-item", "status": "done"}},
            [{"status": "open"}])
        self.assertFalse(run_iteration.engagement_at_rest(observed))

    def test_an_epic_with_no_children_is_not_rest(self):
        observed = self.observed({"EP-001": {"type": "epic", "status": "open"}})
        self.assertFalse(run_iteration.engagement_at_rest(observed))

    def test_an_open_epic_has_not_recorded_its_ending(self):
        """F-045: at rest with the epic still open is one turn short of the point."""
        observed = self.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "blocked"},
        })
        self.assertTrue(run_iteration.engagement_at_rest(observed))
        self.assertFalse(run_iteration.engagements_ended(observed))

    def test_an_epic_at_blocked_or_done_has_recorded_its_ending(self):
        for ending in ("blocked", "done"):
            observed = self.observed({
                "EP-001": {"type": "epic", "status": ending},
                "WI-0001": {"type": "work-item", "status": "blocked"},
            })
            self.assertTrue(run_iteration.engagements_ended(observed), ending)


class TerminalWorkspace(unittest.TestCase):
    """H-014: the counter never overrules the disk.

    Iteration 4 reached its terminal state — sign-off accepted at turn 21, the epic `done` and
    `delivered`, nothing open — announced the H-007 closing turn, spent the budget's last slot on
    it, and then cut before the worker turn that records epic-done, stamping a finished run
    "turn-budget: not finished". The workspace was terminal; only the label was wrong.
    """

    @staticmethod
    def observed(items, questions=(), requests=(), blocked=()):
        return {"items": items,
                "questions": [dict({"status": "open"}, **q) for q in questions],
                "open-human-questions": [q["id"] for q in questions
                                         if q.get("addressed-to") == "human"
                                         and q.get("status", "open") == "open"],
                "open-requests": list(requests),
                "blocked-items": list(blocked)}

    def test_every_item_done_is_epic_done_whatever_the_counter_says(self):
        terminal, reason, _ = run_iteration.engagement_terminal(self.observed({
            "EP-001": {"type": "epic", "status": "done"},
            "WI-0001": {"type": "work-item", "status": "done"},
        }))
        self.assertTrue(terminal)
        self.assertEqual(reason, "epic-done")

    def test_an_engagement_that_recorded_an_impasse_is_terminal_too(self):
        terminal, reason, _ = run_iteration.engagement_terminal(self.observed(
            {"EP-001": {"type": "epic", "status": "blocked"},
             "WI-0001": {"type": "work-item", "status": "blocked"}},
            blocked=["WI-0001"]))
        self.assertTrue(terminal)
        self.assertEqual(reason, "blocked-no-recourse")

    def test_work_still_in_flight_is_not_terminal(self):
        terminal, _, _ = run_iteration.engagement_terminal(self.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "verifying"},
        }))
        self.assertFalse(terminal)

    def test_an_unrecorded_ending_is_not_terminal(self):
        """F-045's shape: at rest with the epic still open is one turn short of the point."""
        terminal, _, _ = run_iteration.engagement_terminal(self.observed({
            "EP-001": {"type": "epic", "status": "open"},
            "WI-0001": {"type": "work-item", "status": "blocked"},
        }, blocked=["WI-0001"]))
        self.assertFalse(terminal)

    def test_an_open_question_to_the_human_holds_the_ending_open(self):
        terminal, _, _ = run_iteration.engagement_terminal(self.observed(
            {"EP-001": {"type": "epic", "status": "blocked"},
             "WI-0001": {"type": "work-item", "status": "blocked"}},
            [{"id": "EP-001/Q-005", "addressed-to": "human", "status": "open"}]))
        self.assertFalse(terminal)

    def test_the_closing_turn_is_exempt_from_the_budget(self):
        """The exemption is in the loop, so the test reads the loop rather than re-stating it."""
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        budget = source[source.index('if self.state["turn"] >= self.max_turns:'):]
        budget = budget[:budget.index("number = self.state")]
        self.assertIn('self.state.get("next-job") == "closing"', budget)
        self.assertIn("engagement_terminal(observed)", budget)
        self.assertLess(budget.index("engagement_terminal(observed)"),
                        budget.index('self.stop("turn-budget"'),
                        "the disk is read before the counter is believed")


class FirstJob(unittest.TestCase):
    """H-011: a fresh run's first job is read from the workspace, not assumed."""

    def project(self, **files):
        import tempfile
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        for name, text in files.items():
            path = os.path.join(directory, name.replace("|", os.sep))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
        return directory

    def test_an_empty_project_opens_with_the_sim(self):
        directory = self.project()
        with mock.patch.object(run_iteration, "scan_project",
                               return_value={"unanswered-human-questions": []}):
            role, job, why = run_iteration.first_job(directory)
        self.assertEqual((role, job), ("sim", "open"))
        self.assertIn("IDEA.md", why)

    def test_a_populated_project_goes_to_the_worker(self):
        directory = self.project(**{"IDEA.md": "an idea\n"})
        with mock.patch.object(run_iteration, "scan_project",
                               return_value={"unanswered-human-questions": []}):
            role, job, why = run_iteration.first_job(directory)
        self.assertEqual(role, "worker")
        self.assertIsNone(job)

    def test_an_unanswered_human_question_outranks_everything(self):
        directory = self.project(**{"IDEA.md": "an idea\n"})
        with mock.patch.object(run_iteration, "scan_project",
                               return_value={"unanswered-human-questions": ["EP-001/Q-005"]}):
            role, job, why = run_iteration.first_job(directory)
        self.assertEqual((role, job), ("sim", "answer"))
        self.assertIn("1 human question", why)


class ConsoleLog(unittest.TestCase):
    """H-012: the driver's account of itself is a file in the run, not a wrapper's problem."""

    def test_say_writes_to_the_log_once_it_is_open(self):
        import tempfile
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, "nested", "driver-console.log")
        self.assertEqual(run_iteration.open_console_log(path), path)
        try:
            run_iteration.say("a line the wrapper never saw")
        finally:
            run_iteration.close_console_log()
        with open(path, encoding="utf-8") as handle:
            self.assertIn("a line the wrapper never saw", handle.read())

    def test_an_unopenable_log_does_not_stop_the_run(self):
        self.assertEqual(run_iteration.open_console_log("/proc/nope/console.log"), "")
        run_iteration.say("still speaking")

    def test_the_run_directory_exists_before_the_first_line_of_output(self):
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        body = source[source.index("    def main(self):"):]
        self.assertLess(body.index("open_console_log("), body.index("another_driver("),
                        "the log is opened before anything can be printed about the run")
        self.assertLess(body.index("os.makedirs(self.turns_dir"), body.index("open_console_log("),
                        "the run directory exists before the log is opened into it")


class WipeSafety(unittest.TestCase):
    """H-003: --wipe deletes a directory, so it refuses everything it did not create."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_a_stranger_directory_is_refused(self):
        target = os.path.join(self.root, "not-ours")
        os.makedirs(target)
        open(os.path.join(target, "important.txt"), "w").close()
        self.assertEqual(provision.wipe(target, self.root, False), 2)
        self.assertTrue(os.path.isdir(target))

    def test_the_throwaway_root_itself_is_refused(self):
        os.makedirs(os.path.join(self.root, ".harness"), exist_ok=True)
        with open(os.path.join(self.root, provision.MARKER), "w") as handle:
            handle.write("{}")
        self.assertEqual(provision.wipe(self.root, self.root, False), 2)
        self.assertTrue(os.path.isdir(self.root))

    def test_a_provisioned_directory_is_wiped(self):
        target = os.path.join(self.root, "ours")
        os.makedirs(os.path.join(target, os.path.dirname(provision.MARKER)), exist_ok=True)
        with open(os.path.join(target, provision.MARKER), "w") as handle:
            handle.write("{}")
        self.assertEqual(provision.wipe(target, self.root, False), 0)
        self.assertFalse(os.path.exists(target))

    def test_a_dry_run_deletes_nothing(self):
        target = os.path.join(self.root, "ours")
        os.makedirs(os.path.join(target, os.path.dirname(provision.MARKER)), exist_ok=True)
        with open(os.path.join(target, provision.MARKER), "w") as handle:
            handle.write("{}")
        self.assertEqual(provision.wipe(target, self.root, True), 0)
        self.assertTrue(os.path.isdir(target))


class TurnAccounting(unittest.TestCase):
    """H-005: a killed turn must not be logged with someone else's status or with $0.00."""

    def setUp(self):
        self.project = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.project, True)
        self.status = os.path.join(self.project, run_iteration.STATUS_FILE)

    def write_status(self, stop_reason):
        with open(self.status, "w", encoding="utf-8") as handle:
            handle.write("# status\n\n```json\n"
                         + json.dumps({"stop_reason": stop_reason}) + "\n```\n")

    def test_a_status_older_than_the_turn_is_not_this_turns_status(self):
        self.write_status("human-question-open")
        old_time = time.time() - 7200
        os.utime(self.status, (old_time, old_time))
        report, text = run_iteration.worker_report(self.project, not_before=time.time() - 60)
        self.assertIsNone(report)
        self.assertEqual(text, "")

    def test_a_status_written_during_the_turn_is_read(self):
        started = time.time() - 60
        self.write_status("epic-done")
        report, text = run_iteration.worker_report(self.project, not_before=started)
        self.assertEqual(report["stop_reason"], "epic-done")
        self.assertTrue(text)

    def test_without_a_start_time_the_old_behaviour_is_kept(self):
        self.write_status("blocked")
        report, _ = run_iteration.worker_report(self.project)
        self.assertEqual(report["stop_reason"], "blocked")

    def test_a_killed_turn_has_an_unknown_cost_not_a_zero_one(self):
        fields = {"cost_usd": None}
        run_iteration.note_unknown_cost({"killed": "timeout", "duration": 3603.0,
                                         "tool_calls": 255}, fields)
        self.assertIsNone(fields["cost_usd"])
        self.assertTrue(fields["cost-unknown"])
        self.assertIn("255", fields["cost-note"])

    def test_a_reported_cost_is_left_alone(self):
        fields = {"cost_usd": 7.5}
        run_iteration.note_unknown_cost({"duration": 900.0, "tool_calls": 30}, fields)
        self.assertEqual(fields["cost_usd"], 7.5)
        self.assertNotIn("cost-unknown", fields)


class SimChannel(unittest.TestCase):
    """F-021: a request is the one file a stakeholder may create, so the audit must allow it."""

    def setUp(self):
        self.project = "/tmp/proj"
        self.log = "/tmp/SIM-LOG.md"

    def violations(self, path):
        return rules(audit.audit_sim([("Write", {"file_path": path})], self.project,
                                     HARNESS, self.log))

    def test_writing_a_request_is_permitted(self):
        self.assertEqual(self.violations("/tmp/proj/tracker/requests/R-001.md"), [])

    def test_answering_a_question_is_still_permitted(self):
        self.assertEqual(
            self.violations("/tmp/proj/tracker/items/WI-0001/questions/Q-001.md"), [])

    def test_writing_an_item_is_still_refused(self):
        self.assertEqual(self.violations("/tmp/proj/tracker/items/WI-0001/item.md"), ["S1"])

    def test_a_misnamed_request_is_refused(self):
        self.assertEqual(self.violations("/tmp/proj/tracker/requests/notes.md"), ["S1"])


class ScriptedSilence(unittest.TestCase):
    """ADR-0011 §6: a persona that stops replying takes its turn and answers nothing.

    That is a turn which SUCCEEDED and answered nothing. Nothing in the audit ever called it a
    failure — it called it nothing at all, which is the defect: a silent stakeholder and a broken
    sim produced identical evidence. The `Withheld:` line tagged with the probe that scripted it
    is what separates them, and these cases are the check that it still does.
    """

    QUESTION = ("---\nid: {qid}\nitem: {item}\naddressed-to: {to}\nstatus: {status}\n---\n\n"
                "## Question\n\nWhat should it do?\n\n## Answer\n\n{answer}\n")

    def workspace(self, *questions):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root, True)
        for item, qid, to, status, answer in questions:
            directory = os.path.join(root, "tracker", "items", item, "questions")
            os.makedirs(directory, exist_ok=True)
            with open(os.path.join(directory, f"{qid}.md"), "w", encoding="utf-8") as handle:
                handle.write(self.QUESTION.format(qid=qid, item=item, to=to, status=status,
                                                  answer=answer))
        return root

    def answer(self, root, item, qid, text):
        path = os.path.join(root, "tracker", "items", item, "questions", f"{qid}.md")
        with open(path, encoding="utf-8") as handle:
            body = handle.read()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body.replace("## Answer\n\n\n", f"## Answer\n\n{text}\n"))

    def log(self, text):
        handle = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        handle.write(text)
        handle.close()
        self.addCleanup(os.unlink, handle.name)
        return handle.name

    GHOSTED = ("## Turn 4 — 2026-09-10T10:00:00Z — persona: ghosting-founder\n\n"
               "- **Found:** a board with 3 items, 2 questions waiting on me\n"
               "- **Read:** tracker/board.md; WI-0001/Q-001; WI-0002/Q-001\n"
               "- **Withheld:** WI-0001/Q-001 — [PLANTED: ghosting] scripted silence — this "
               "persona does not return\n"
               "- **Withheld:** WI-0002/Q-001 — [PLANTED: ghosting] scripted silence — this "
               "persona does not return\n")

    def test_a_scripted_silence_is_a_successful_turn_that_answered_nothing(self):
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root),
                                         self.GHOSTED)
        self.assertEqual(outcome["outcome"], "scripted-silence")
        self.assertEqual(outcome["asked"], ["WI-0001/Q-001"])
        self.assertEqual(outcome["withheld"], ["WI-0001/Q-001"])
        self.assertEqual(outcome["answered"], [])
        self.assertTrue(outcome["withholding-logged"])

    def test_the_same_silence_with_no_log_entry_is_not_scripted_silence(self):
        """The non-vacuity of the whole distinction: only the log entry separates the two."""
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root), "")
        self.assertEqual(outcome["outcome"], "unexplained-silence")
        self.assertEqual(outcome["withheld"], ["WI-0001/Q-001"])
        self.assertFalse(outcome["log-entry"])
        self.assertIn("broken sim", outcome["note"])

    def test_a_log_entry_that_mentions_no_withholding_is_not_scripted_silence(self):
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        entry = ("## Turn 4 — 2026-09-10T10:00:00Z — persona: ghosting-founder\n\n"
                 "- **Found:** a board with 3 items\n- **Read:** tracker/board.md\n")
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root), entry)
        self.assertEqual(outcome["outcome"], "unexplained-silence")
        self.assertTrue(outcome["log-entry"])

    def test_a_withholding_with_no_probe_tag_is_not_scripted_silence(self):
        """`[PLANTED: ...]` is what makes it scripted rather than merely reported (SKILL §3.1)."""
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        entry = ("## Turn 4\n\n- **Withheld:** WI-0001/Q-001 — did not feel like answering\n")
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root), entry)
        self.assertEqual(outcome["outcome"], "unexplained-silence")

    def test_an_answer_is_still_an_answer(self):
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        self.answer(root, "WI-0001", "Q-001", "[human] Yes, that is fine.")
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root),
                                         "## Turn 4\n\n- **Answered:** WI-0001/Q-001\n")
        self.assertEqual(outcome["outcome"], "answered")
        self.assertEqual(outcome["answered"], ["WI-0001/Q-001"])
        self.assertEqual(outcome["withheld"], [])

    def test_a_partial_answer_names_both_halves(self):
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""),
                              ("WI-0002", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        self.answer(root, "WI-0001", "Q-001", "[human] Yes.")
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root),
                                         self.GHOSTED)
        self.assertEqual(outcome["outcome"], "answered")
        self.assertEqual(outcome["answered"], ["WI-0001/Q-001"])
        self.assertEqual(outcome["withheld"], ["WI-0002/Q-001"])

    def test_a_turn_with_nothing_addressed_to_the_human_is_not_silence(self):
        """An `open` turn, or a turn where only the architect was asked. Answering nothing
        there is not a withholding and must not be reported as one."""
        root = self.workspace(("WI-0001", "Q-001", "architect", "open", ""),
                              ("WI-0002", "Q-001", "human", "answered", "[human] Done."))
        before = audit.question_answer_snapshot(root)
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root), "")
        self.assertEqual(outcome["outcome"], "nothing-to-answer")
        self.assertEqual(outcome["asked"], [])

    def test_filing_a_request_counts_as_speaking(self):
        root = self.workspace(("WI-0001", "Q-001", "human", "open", ""))
        before = audit.question_answer_snapshot(root)
        outcome = audit.sim_turn_outcome(before, audit.question_answer_snapshot(root),
                                         self.GHOSTED, [], ["R-001"])
        self.assertEqual(outcome["outcome"], "answered")
        self.assertEqual(outcome["requests-filed"], ["R-001"])

    def test_the_log_entry_for_this_turn_is_the_one_read(self):
        log = self.log("## Turn 3 — persona: x\n\n- **Answered:** WI-0001/Q-001\n\n"
                       + self.GHOSTED + "\n## Turn 5 — persona: x\n\n- **Found:** nothing\n")
        self.assertIn("Withheld", audit.sim_log_entry(log, 4))
        self.assertNotIn("Turn 5", audit.sim_log_entry(log, 4))
        self.assertIn("Answered", audit.sim_log_entry(log, 3))
        self.assertEqual(audit.sim_log_entry(log, 9), "")

    def test_writing_no_answer_is_still_not_a_contamination(self):
        """A silent turn touches nothing, so the boundary rules must stay quiet about it."""
        self.assertEqual(audit.audit_sim([], PROJECT, HARNESS, "/tmp/SIM-LOG.md"), [])

    def test_the_sim_skill_and_the_prompt_both_permit_a_scripted_silence(self):
        """The persona says answer nothing; the skill's checklist used to say you are not
        finished until you have. Both cannot hold, and the persona is the one being tested."""
        skill = open(os.path.join(HARNESS, "skills", "simulated-human", "SKILL.md"),
                     encoding="utf-8").read()
        self.assertIn("2.2a", skill)
        self.assertIn("stop replying", skill)
        self.assertIn("Withheld:", skill)
        prompt, _ = run_iteration.prompt_text("sim-turn")
        self.assertIn("stop replying", prompt)
        self.assertIn("PLANTED:", prompt)


class Abandonment(unittest.TestCase):
    """The E4 half: the driver stops on the ending, not on a stall.

    H-008 again, one level out. A stall is a fact about this driver's own progress; an ending is
    a fact about the engagement. They coincided for four iterations and stop coinciding exactly
    here: a ghosting stakeholder leaves the workspace unchanged turn after turn, so the
    fingerprint check fires and calls a finished engagement "three turns changed nothing".
    """

    ABANDONED = ("engagement-state: EP-001 abandoned\n"
                 "  - 3 silent round(s) against a threshold of 3: the last 3 halts on the human "
                 "share one inbound digest (ee47bf97), so nothing the stakeholder could have "
                 "changed has changed\n"
                 "  - still open and unanswered: EP-001/Q-001, WI-0002/Q-001\n"
                 "  - the ending is E4 by silence and it is not recorded; review-close declares "
                 "it\n"
                 "  rest reached at 2026-09-07T11:00:00Z\n")
    DECLARED = ("engagement-state: EP-001 ended\n"
                "  - 3 silent round(s) recorded against a threshold of 3\n"
                "  - the epic is 'done'; the engagement has ended and the retrospective has not "
                "been written\n")
    TICKING = ("engagement-state: EP-001 active\n"
               "  - 2 silent round(s) recorded against a threshold of 3\n"
               "  - WI-0001 is in flight\n")
    # E4 by withdrawal (`spec/ids-and-statuses.md` §3.5): an act the stakeholder performs, so it
    # brings the engagement to rest like any other reply and no silent round is ever recorded.
    WITHDRAWN = ("engagement-state: EP-001 ended\n"
                 "  - the epic is 'done'; the engagement has ended and the retrospective has "
                 "not been written\n")

    # The two records an `ended` verdict can sit on top of. `engagement-state` prints the same
    # sentences over both, which is the whole of H-020: the count is derived from a log nothing
    # resets, so it outlives the silence it describes and cannot say which ending was written.
    E4_RECORD = {"EP-001": {"type": "epic", "status": "done", "outcome": "dropped"},
                 "WI-0001": {"type": "work-item", "status": "blocked", "outcome": None}}
    RECOVERED_RECORD = {"EP-001": {"type": "epic", "status": "done", "outcome": "delivered"},
                        "WI-0001": {"type": "work-item", "status": "done",
                                    "outcome": "delivered"}}

    @staticmethod
    def observed(text, **overrides):
        reading = {"items": {"EP-001": {"type": "epic", "status": "open"},
                             "WI-0001": {"type": "work-item", "status": "awaiting-answer"}},
                   "questions": [], "open-human-questions": [], "open-requests": [],
                   "unanswered-human-questions": [], "blocked-items": [],
                   "validator-exit": 0, "validator-tail": [], "head": "abc123",
                   "engagements": run_iteration.parse_engagement_state(text)}
        reading["abandoned-epics"] = [epic for epic, state
                                      in sorted(reading["engagements"].items())
                                      if state["verdict"] == "abandoned"]
        reading.update(overrides)
        return reading

    # -- what the driver asks, and what it refuses to work out for itself -----------------

    def test_the_verdict_and_both_numbers_come_from_the_script(self):
        parsed = run_iteration.parse_engagement_state(self.ABANDONED)
        self.assertEqual(parsed["EP-001"]["verdict"], "abandoned")
        self.assertEqual(parsed["EP-001"]["silent-rounds"], 3)
        self.assertEqual(parsed["EP-001"]["threshold"], 3)

    def test_a_declared_ending_still_carries_the_count_that_caused_it(self):
        parsed = run_iteration.parse_engagement_state(self.DECLARED)
        self.assertEqual(parsed["EP-001"]["verdict"], "ended")
        self.assertEqual((parsed["EP-001"]["silent-rounds"], parsed["EP-001"]["threshold"]),
                         (3, 3))

    def test_the_driver_holds_no_threshold_of_its_own(self):
        """F-045's mechanism is two programs with two opinions about one number. The driver's
        source may not contain the threshold, the waiting log, or the word for a silent round."""
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        code = "\n".join(line for line in source.split("\n")
                         if not line.lstrip().startswith("#"))
        self.assertNotIn("threshold_rounds", code)
        self.assertNotIn("tracker/waiting", code)
        self.assertNotIn("pipeline.yaml", code)

    def test_a_project_with_no_toolkit_installed_yields_no_verdicts(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root, True)
        self.assertEqual(run_iteration.engagement_states(root), {})

    def test_the_real_script_is_read_the_way_the_driver_parses_it(self):
        """Against the fixture the toolkit ships, so a change to either side fails here."""
        fixture = os.path.join(REPO, "fixtures", "abandoned-engagement", "right")
        if not os.path.isdir(fixture):
            self.skipTest("fixtures/abandoned-engagement is not present")
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(REPO, "scripts", "engagement-state"),
             "--all", "--root", fixture], capture_output=True, text=True)
        parsed = run_iteration.parse_engagement_state(result.stdout)
        self.assertEqual(parsed["EP-003"]["verdict"], "abandoned")
        self.assertGreaterEqual(parsed["EP-003"]["silent-rounds"], parsed["EP-003"]["threshold"])
        self.assertEqual(parsed["EP-001"]["verdict"], "ended")
        self.assertEqual(run_iteration.engagements_abandoned(
            {"engagements": parsed}), ["EP-003"])
        # And the other half of the reading, off the same fixture: the endings the epics record
        # about themselves. `scan_project` reads exactly these three fields (H-020).
        record = {}
        for name in sorted(os.listdir(os.path.join(fixture, "tracker", "items"))):
            fields = audit.frontmatter(
                open(os.path.join(fixture, "tracker", "items", name, "item.md"),
                     encoding="utf-8").read())
            record[name] = {"type": fields.get("type"), "status": fields.get("status"),
                            "outcome": fields.get("outcome")}
        self.assertEqual(record["EP-001"]["outcome"], "dropped")
        self.assertEqual(record["EP-002"]["outcome"], "dropped")
        self.assertEqual([epic for epic, _, _ in run_iteration.abandonment_declared(
            {"engagements": parsed, "items": record})], ["EP-001", "EP-002"])

    # -- the ending is terminal, and it is not the other endings -------------------------

    def test_a_declared_abandonment_is_terminal_and_named_as_itself(self):
        terminal, reason, detail = run_iteration.engagement_terminal(
            self.observed(self.DECLARED, items=self.E4_RECORD))
        self.assertTrue(terminal)
        self.assertEqual(reason, "abandoned")
        self.assertIn("silent for 3 round(s)", detail)
        self.assertIn("'dropped'", detail)

    def test_e4_over_a_finished_board_is_not_reported_as_epic_done(self):
        """H-014's shape: the most specific true thing wins. Every item done and the sign-off
        never answered is an abandonment, not a delivery. The child delivered — ADR-0011 §2.2's
        first class — and the epic still recorded E4."""
        finished = self.observed(self.DECLARED, items={
            "EP-001": {"type": "epic", "status": "done", "outcome": "dropped"},
            "WI-0001": {"type": "work-item", "status": "done", "outcome": "delivered"}})
        self.assertTrue(run_iteration.epic_complete(finished))
        _, reason, _ = run_iteration.engagement_terminal(finished)
        self.assertEqual(reason, "abandoned")

    def test_e4_over_orphaned_children_is_not_reported_as_an_impasse(self):
        orphaned = self.observed(self.DECLARED, items={
            "EP-001": {"type": "epic", "status": "done", "outcome": "dropped"},
            "WI-0001": {"type": "work-item", "status": "blocked", "outcome": None}},
            blocked=["WI-0001"])
        _, reason, _ = run_iteration.engagement_terminal(orphaned)
        self.assertEqual(reason, "abandoned")

    def test_an_ending_with_no_silence_behind_it_is_the_ordinary_ending(self):
        ordinary = self.observed(
            "engagement-state: EP-001 ended\n  - the epic is 'done'\n",
            items={"EP-001": {"type": "epic", "status": "done"},
                   "WI-0001": {"type": "work-item", "status": "done"}})
        _, reason, _ = run_iteration.engagement_terminal(ordinary)
        self.assertEqual(reason, "epic-done")

    def test_the_clock_still_ticking_is_not_an_ending(self):
        terminal, _, _ = run_iteration.engagement_terminal(self.observed(self.TICKING))
        self.assertFalse(terminal)
        self.assertEqual(run_iteration.abandonment_declared(self.observed(self.TICKING)), [])

    def test_the_stop_is_a_verdict_rather_than_an_interruption(self):
        self.assertFalse(run_iteration.stop_is_resumable("abandoned"))
        self.assertIn("abandoned", run_iteration.TERMINAL_STOPS)

    def test_a_budget_spent_on_an_abandoned_engagement_is_the_ending_not_the_budget(self):
        self.assertFalse(run_iteration.stop_is_resumable(
            "turn-budget", self.observed(self.DECLARED, items=self.E4_RECORD)))

    # -- H-020: which ending was recorded, and what the count can and cannot say -----------

    def test_the_declaration_is_read_off_the_record_not_off_the_count(self):
        """H-020, at the smallest scale it can be shown. One `engagement-state` output, two
        workspaces: the count is the trailing run of equal digests in an append-only log that
        nothing resets, so a recovered engagement (ADR-0011 §7) still reports it under a verdict
        of `ended`. What differs is the ending the epic records about itself."""
        declared = self.observed(self.DECLARED, items=self.E4_RECORD)
        recovered = self.observed(self.DECLARED, items=self.RECOVERED_RECORD)
        self.assertEqual(declared["engagements"], recovered["engagements"])
        self.assertEqual([epic for epic, _, _
                          in run_iteration.abandonment_declared(declared)], ["EP-001"])
        self.assertEqual(run_iteration.abandonment_declared(recovered), [])

    def test_a_recovered_engagement_that_delivered_is_a_delivery(self):
        """The whole path, not just the predicate: silence past the threshold, a stakeholder who
        came back through `tracker/requests/`, and a delivery. The run ended `epic-done`."""
        recovered = self.observed(self.DECLARED, items=self.RECOVERED_RECORD)
        terminal, reason, _ = run_iteration.engagement_terminal(recovered)
        self.assertTrue(terminal)
        self.assertEqual(reason, "epic-done")

    def test_a_recovered_delivery_still_gets_its_closing_sim_turn(self):
        """And the sim is not locked out of it. E4 skips the closing turn because there is
        nobody to show the ending to (H-007); a delivery has somebody, and mislabelling one as
        the other took that turn away as well as the label."""
        decision = self.decide(self.observed(self.DECLARED, items=self.RECOVERED_RECORD),
                               self.STUCK)
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "sim")
        self.assertEqual(decision["next-job"], "closing")

    def test_e4_by_withdrawal_is_recognised_with_no_silence_behind_it(self):
        """`spec/ids-and-statuses.md` §3.5 gives E4 two routes. A withdrawal is an act the
        stakeholder performs, so it arrives as an answer or a request and the waiting log never
        gets a row. Requiring the count missed this ending entirely."""
        withdrawn = self.observed(self.WITHDRAWN, items=self.E4_RECORD)
        self.assertEqual(withdrawn["engagements"]["EP-001"]["silent-rounds"], 0)
        terminal, reason, detail = run_iteration.engagement_terminal(withdrawn)
        self.assertTrue(terminal)
        self.assertEqual(reason, "abandoned")
        self.assertNotIn("silent for", detail)

    def test_an_epic_still_open_under_an_ended_verdict_is_not_a_declaration(self):
        """The record has to agree that the ending happened. `ended` over an epic that is not
        `done` is a reading of two different moments, and the driver takes neither."""
        mid = self.observed(self.DECLARED, items={
            "EP-001": {"type": "epic", "status": "open", "outcome": None},
            "WI-0001": {"type": "work-item", "status": "blocked", "outcome": None}})
        self.assertEqual(run_iteration.abandonment_declared(mid), [])

    # -- and the asymmetry, decided by running `decide` ----------------------------------

    def decide(self, observed, fingerprints, record=None):
        run = run_iteration.Run.__new__(run_iteration.Run)
        run.state = {"fingerprints": list(fingerprints)}
        run.repair_turns = 2
        run.log = lambda record: None
        return run.decide("worker", observed, record or {"worker-report": {}})

    STUCK = ["same", "same", "same"]

    def test_abandoned_not_stalled(self):
        """The case that used to lie. Three turns changed nothing AND the engagement ended by
        silence: the old driver said `stalled`, "three turns changed nothing", which is true of
        the run and says nothing about what happened — the person left."""
        decision = self.decide(self.observed(self.DECLARED, items=self.E4_RECORD), self.STUCK)
        self.assertTrue(decision["stop"])
        self.assertEqual(decision["reason"], "abandoned")
        self.assertIn("This is not a stall", decision["detail"])

    def test_stalled_not_abandoned(self):
        """The other half, and without it the first proves nothing: three turns changed nothing
        and NO engagement is abandoned. This must still be `stalled`."""
        decision = self.decide(self.observed(self.TICKING), self.STUCK)
        self.assertTrue(decision["stop"])
        self.assertEqual(decision["reason"], "stalled")
        self.assertIn("not about the engagement", decision["detail"])
        self.assertIn("EP-001 active", decision["detail"])

    def test_an_abandoned_engagement_that_has_not_declared_yet_does_not_stop_the_run(self):
        """F-045's branch in a second place: `abandoned` means review-close is owed, and the
        worker's next turn is the one that records it. Stopping here would stop one turn before
        the thing the run exists to observe."""
        decision = self.decide(
            self.observed(self.ABANDONED,
                          **{"unanswered-human-questions": ["EP-001/Q-001"]}),
            self.STUCK)
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "worker")

    def test_the_undeclared_abandonment_never_routes_another_turn_to_the_sim(self):
        """ADR-0011 Context (b): asking a stakeholder who is gone, getting nothing, and
        repeating until the budget is spent is the loop E4 exists to end."""
        observed = self.observed(self.ABANDONED)
        observed["unanswered-human-questions"] = ["EP-001/Q-001", "WI-0002/Q-001"]
        observed["open-human-questions"] = ["EP-001/Q-001", "WI-0002/Q-001"]
        decision = self.decide(observed, [])
        self.assertEqual(decision["next-role"], "worker")

    def test_an_unanswered_question_with_no_abandonment_still_routes_to_the_sim(self):
        """The non-vacuity of the branch above: the ordinary case must be unchanged."""
        observed = self.observed(self.TICKING)
        observed["unanswered-human-questions"] = ["EP-001/Q-001"]
        observed["open-human-questions"] = ["EP-001/Q-001"]
        decision = self.decide(observed, [])
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "sim")

    def test_a_stakeholder_request_is_still_the_workers_first_business(self):
        observed = self.observed(self.ABANDONED, **{"open-requests": ["R-001"]})
        decision = self.decide(observed, self.STUCK)
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "worker")

    def test_a_broken_workspace_is_still_the_first_thing_the_driver_reacts_to(self):
        """The validator branch outranks the ending, as it always did. What changed is what it
        does with the first failure: it grants a repair turn rather than stopping (H-022)."""
        observed = self.observed(self.DECLARED, items=self.E4_RECORD)
        observed["validator-exit"] = 1
        observed["validator-tail"] = ["nope"]
        decision = self.decide(observed, self.STUCK)
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-job"], "repair")

    def test_the_reschedule_guard_reads_the_abandonment(self):
        """The loop's H-004 guard hands a worker turn to the sim when human questions are open.
        Under an abandonment that is the wrong move, and the guard is in the loop, so the test
        reads the loop rather than restating it."""
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        body = source[source.index("# H-004: on a start or a resume"):]
        body = body[:body.index('self.state["repo-snapshot"]')]
        self.assertIn("engagements_abandoned(reading)", body)
        self.assertLess(body.index("if pending and gone:"), body.index("elif pending:"))


class RepairAllowance(unittest.TestCase):
    """H-022: a fixable record defect is not a verdict on the engagement.

    Iteration 5 died at turn 11 because one prose mention of a citation form was scraped as a
    citation — with every acceptance criterion of the item passing and 69 tests green. The stop
    asked a human to repair a record the worker could have repaired itself. So the driver now
    grants a bounded, consecutive allowance of repair turns, and only spending it is terminal.

    Both halves are tested here, because either one alone is satisfiable by a mistake: a driver
    that never stops, and a driver that never repairs.
    """

    def driver(self, repair_turns=2, **state):
        run = run_iteration.Run.__new__(run_iteration.Run)
        run.state = {"fingerprints": [], **state}
        run.repair_turns = repair_turns
        run.logged = []
        run.log = run.logged.append
        return run

    @staticmethod
    def observed(exit_code=0, tail="", **overrides):
        """A live engagement, with the validator's verdict as the only thing under test.

        `tail` is one line or the list of lines the driver kept (META-171b).
        """
        reading = Abandonment.observed(Abandonment.TICKING, **overrides)
        reading["validator-exit"] = exit_code
        if isinstance(tail, str):
            tail = [tail] if tail else []
        reading["validator-tail"] = list(tail)
        return reading

    def decide(self, run, observed):
        return run.decide("worker", observed, {"worker-report": {}})

    def events(self, run):
        return [entry["event"] for entry in run.logged]

    BROKEN = "validate-workspace: 1 error, 0 warnings"
    OTHER = "validate-workspace: 2 errors, 0 warnings"

    # Iteration 5's stop, as `validate-workspace` actually printed it: one finding line naming
    # the defect, its hint, and the summary the driver used to keep instead.
    ITERATION_5_OUTPUT = (
        "tracker/items/WI-0002/history.md:14: ERROR [claim.citation.unresolved] 'path:line' "
        "is not a citation form this gate can check\n"
        "    hint: quote the form rather than writing it bare\n"
        "validate-workspace: 1 error, 0 warnings\n")

    # -- what the driver keeps of the validator's output (META-171b) ----------------------

    def test_the_kept_tail_names_the_failing_line_and_still_carries_the_count(self):
        kept = run_iteration.validator_tail(self.ITERATION_5_OUTPUT)
        self.assertEqual(len(kept), 2)
        self.assertIn("tracker/items/WI-0002/history.md:14", kept[0])
        self.assertIn("claim.citation.unresolved", kept[0])
        self.assertEqual(kept[-1], self.BROKEN)
        self.assertNotIn("hint:", " ".join(kept))

    def test_forty_errors_do_not_balloon_the_tail_and_what_was_dropped_is_stated(self):
        """The bound, and the line that keeps it from being a silent truncation."""
        output = "\n".join(f"tracker/items/WI-{n:04d}/item.md:3: ERROR [item.status.unknown] "
                           f"status \"reviewing\" is not a known status" for n in range(40))
        kept = run_iteration.validator_tail(output + "\nvalidate-workspace: 40 errors, 0 warnings")
        self.assertEqual(len(kept), run_iteration.VALIDATOR_TAIL_ERRORS + 2)
        self.assertEqual(kept[-2], "... and 37 more errors")
        self.assertEqual(kept[-1], "validate-workspace: 40 errors, 0 warnings")

    def test_output_that_is_not_a_report_keeps_its_last_line_and_nothing_more(self):
        """A crash, a usage error or a green run has no ERROR line to name. Reading structure
        into output that does not have it is the silent half of a silent truncation."""
        self.assertEqual(
            run_iteration.validator_tail("Traceback (most recent call last):\n"
                                         "  File \"validate-workspace\", line 9\n"
                                         "KeyError: 'status'"),
            ["KeyError: 'status'"])
        self.assertEqual(
            run_iteration.validator_tail("docs/x.md:2: WARNING [doc.changelog.for] stale\n"
                                         "validate-workspace: 0 errors, 1 warning"),
            ["validate-workspace: 0 errors, 1 warning"])
        self.assertEqual(run_iteration.validator_tail(""), [])

    # -- the recovery path ---------------------------------------------------------------

    def test_the_first_failure_grants_a_repair_turn_instead_of_stopping(self):
        run = self.driver()
        decision = self.decide(run, self.observed(1, self.BROKEN))
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "worker")
        self.assertEqual(decision["next-job"], "repair")
        self.assertEqual(run.state["repair-turns-used"], 1)
        self.assertIn("repair-granted", self.events(run))

    def test_what_a_resume_needs_is_in_the_state_and_not_in_the_driver(self):
        """`state.json` is the whole of what survives a killed driver, so the count and the
        original error live there or they do not survive at all."""
        run = self.driver()
        self.decide(run, self.observed(1, self.BROKEN))
        self.assertEqual(run.state["repair-original-detail"].endswith(self.BROKEN), True)
        self.assertEqual(run.state["repair-last-detail"].endswith(self.BROKEN), True)
        json.dumps(run.state)  # whatever is stored has to survive the round trip

    def test_a_workspace_that_validates_again_resets_the_counter_and_the_run_continues(self):
        """The recovery acceptance criterion: no stop, the counter back to zero, and the next
        step re-derived from disk rather than forced back to the worker."""
        run = self.driver(**{"repair-turns-used": 1, "repair-original-detail": self.BROKEN,
                             "repair-last-detail": self.BROKEN})
        decision = self.decide(run, self.observed(
            0, **{"unanswered-human-questions": ["EP-001/Q-001"],
                  "open-human-questions": ["EP-001/Q-001"]}))
        self.assertFalse(decision["stop"])
        self.assertEqual(decision["next-role"], "sim")
        self.assertEqual(run.state["repair-turns-used"], 0)
        self.assertNotIn("repair-original-detail", run.state)
        self.assertIn("repair-succeeded", self.events(run))

    def test_an_ordinary_turn_over_a_valid_workspace_says_nothing_about_repairs(self):
        """Non-vacuity for the reset: the log line only appears when something was repaired."""
        run = self.driver()
        self.decide(run, self.observed(0))
        self.assertEqual(self.events(run), [])
        self.assertNotIn("repair-turns-used", run.state)

    # -- the exhaustion path -------------------------------------------------------------

    def test_the_allowance_is_exhausted_by_n_plus_one_consecutive_failures(self):
        run = self.driver(repair_turns=2)
        first = self.decide(run, self.observed(1, self.BROKEN))
        second = self.decide(run, self.observed(1, self.BROKEN))
        third = self.decide(run, self.observed(1, self.BROKEN))
        self.assertFalse(first["stop"])
        self.assertFalse(second["stop"])
        self.assertTrue(third["stop"])
        self.assertEqual(third["reason"], "validator-failed")
        self.assertEqual(self.events(run),
                         ["repair-granted", "repair-granted", "repair-exhausted"])

    def test_the_exhausted_stop_preserves_the_original_error(self):
        """The first error is the finding; the last one may be a symptom of the repair. A stop
        that reported only the last would report the wrong defect — which is the whole value of
        iteration 5's trail."""
        run = self.driver(repair_turns=1)
        self.decide(run, self.observed(1, self.BROKEN))
        stop = self.decide(run, self.observed(1, self.OTHER))
        self.assertTrue(stop["stop"])
        self.assertIn(self.BROKEN, stop["detail"])
        self.assertIn(self.OTHER, stop["detail"])
        exhausted = [entry for entry in run.logged if entry["event"] == "repair-exhausted"][0]
        self.assertIn(self.BROKEN, exhausted["original"])
        self.assertIn(self.OTHER, exhausted["last"])

    def test_the_exhausted_stop_names_the_original_defect_and_not_only_the_count(self):
        """META-171b takes ADR-0014's deferral. The promise was *the original error*, and a
        stop that can only say "1 error, 0 warnings" keeps it nominally: iteration 5's whole
        value as evidence is that the first error was one nameable line."""
        run = self.driver(repair_turns=1)
        granted = self.decide(run, self.observed(
            1, run_iteration.validator_tail(self.ITERATION_5_OUTPUT)))
        self.assertEqual(granted["next-job"], "repair")
        # What the repair turn itself is handed has to name the line too — it is the prompt's
        # VALIDATOR_ERROR.
        self.assertIn("history.md:14", run.state["repair-last-detail"])

        stop = self.decide(run, self.observed(1, self.OTHER))
        self.assertTrue(stop["stop"])
        self.assertEqual(stop["reason"], "validator-failed")
        self.assertIn("tracker/items/WI-0002/history.md:14", stop["detail"])
        self.assertIn("claim.citation.unresolved", stop["detail"])
        self.assertIn(self.BROKEN, stop["detail"])
        exhausted = [entry for entry in run.logged
                     if entry["event"] == "repair-exhausted"][0]
        self.assertIn("tracker/items/WI-0002/history.md:14", exhausted["original"])

    def test_a_success_between_two_failures_gives_the_second_a_fresh_allowance(self):
        """What "consecutive" buys: N bounds this defect, not the run's lifetime supply of
        them. Under a lifetime counter the last decision here would be the stop."""
        run = self.driver(repair_turns=1)
        self.decide(run, self.observed(1, self.BROKEN))
        self.decide(run, self.observed(0))
        again = self.decide(run, self.observed(1, self.OTHER))
        self.assertFalse(again["stop"])
        self.assertEqual(again["next-job"], "repair")
        self.assertEqual(run.state["repair-turns-used"], 1)
        self.assertIn(self.OTHER, run.state["repair-original-detail"])

    def test_a_sim_turn_neither_burns_nor_resets_the_allowance(self):
        """The contamination boundary confines the sim to answers and requests: it can neither
        break the record nor repair it, so "consecutive" counts worker turns."""
        run = self.driver(**{"repair-turns-used": 1})
        decision = run.decide("sim", self.observed(1, self.BROKEN), {})
        self.assertFalse(decision["stop"])
        self.assertEqual(run.state["repair-turns-used"], 1)
        self.assertEqual(self.events(run), [])

    # -- how many, and what the turn is told ---------------------------------------------

    def test_the_allowance_defaults_to_two_and_no_config_has_to_carry_it(self):
        run = run_iteration.Run(self.args(iteration="iteration-5-envel"))
        self.assertEqual(run.repair_turns, 2)
        self.assertNotIn("repair-turns", run.config)

    def test_the_config_and_then_the_flag_win_over_the_default(self):
        with mock.patch.object(run_iteration, "load_iteration",
                               lambda ident: {"id": ident, "project": "p", "repair-turns": 5}):
            self.assertEqual(run_iteration.Run(self.args()).repair_turns, 5)
            self.assertEqual(run_iteration.Run(self.args(repair_turns=1)).repair_turns, 1)

    @staticmethod
    def args(**overrides):
        fields = {"iteration": "iteration-5-envel", "root": "/tmp/nowhere", "max_turns": None,
                  "repair_turns": None, "worker_model": None, "sim_model": None,
                  "skills_per_turn": None}
        fields.update(overrides)
        return argparse.Namespace(**fields)

    def test_a_repair_turn_gets_its_own_instructions(self):
        self.assertEqual(run_iteration.worker_prompt_name("repair"), "repair-turn")
        for job in (None, "", "answer", "closing"):
            self.assertEqual(run_iteration.worker_prompt_name(job), "worker-turn", job)

    def test_the_repair_prompt_says_its_only_job_and_forbids_advancing_the_work(self):
        body, _ = run_iteration.prompt_text("repair-turn")
        self.assertIn("validate-workspace", body)
        self.assertIn("Do not advance the work", body)
        self.assertIn("/next", body)
        self.assertLess(body.index("Do not advance the work"), body.index("/next"))

    # -- the two places the loop, not the decision, has to get right ----------------------

    def loop_body(self, start, end):
        source = open(os.path.join(HARNESS, "run_iteration.py"), encoding="utf-8").read()
        body = source[source.index(start):]
        return body[:body.index(end)]

    def test_a_repair_turn_is_not_rescheduled_to_the_sim(self):
        """H-004 hands a worker turn to the sim when human questions are open, because that turn
        would halt at orchestrator step 2 having done nothing. A repair turn does not run the
        orchestrator, so the premise is false — and a sim turn here would spend one of a bounded
        number of repair turns without repairing anything."""
        body = self.loop_body('if role == "worker" and self.state.get("next-job") == "repair"',
                              'self.state["repo-snapshot"]')
        self.assertLess(body.index("repair-keeps-the-turn"),
                        body.index("# H-004: on a start or a resume"))
        self.assertIn('elif role == "worker":', body)

    def test_repair_turns_are_not_exempt_from_the_turn_budget(self):
        """A repair turn is work, and a budget bounds work (H-010). The closing turn is exempt
        for a different reason — it exists for the engagement's benefit rather than the
        budget's, it is one turn, and it is given once — and that reason does not reach here."""
        budget = self.loop_body("while True:", 'number = self.state["turn"] + 1')
        self.assertIn('== "closing"', budget)
        self.assertNotIn("repair", budget)

    def test_the_terminal_recovery_sentence_describes_a_spent_allowance(self):
        """The stop it describes now only happens after the allowance is gone."""
        sentence = run_iteration.TERMINAL_STOPS["validator-failed"]
        self.assertIn("repair turns were spent", sentence)
        self.assertNotIn("--reaudit", sentence)
        self.assertFalse(run_iteration.stop_is_resumable(
            "validator-failed", self.observed(1, self.BROKEN)))


# =============================================================================================
# harness/ops — the mechanics layer (status.py, watch.py)
#
# The traps these cover are the ones meta/OPS-CONVENTIONS.md was written from. Each is paired
# with its non-vacuity case, because a rule that cannot be seen failing is not being tested.


def ops_args(**overrides):
    """The argparse.Namespace the ops entry points expect, with every field defaulted."""
    fields = {"iteration": [], "builder": False, "builder_pid_file": None,
              "window_minutes": 20, "on_stop": False, "on_file_complete": [],
              "on_unit_gte": None, "on_new_rundir": False, "poll_minutes": 15,
              "timeout_hours": 6, "report_file": None}
    fields.update(overrides)
    return argparse.Namespace(**fields)


def ops_run_dir(root, iteration, **state):
    directory = os.path.join(root, "runs", iteration)
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "state.json"), "w", encoding="utf-8") as handle:
        json.dump(state, handle, sort_keys=True)
    return directory


# The checkpoint that produced the false positive, in the shape the real file had at bd5e392:
# a preamble that declares the session's RANGE, a `## Current unit` section naming the unit
# actually in flight, a `###` subheading inside it, and a later `##` section naming other units.
CHECKPOINT_WITH_A_RANGE = """# CHECKPOINT

## Session: builder five (`meta/BUILDER-5-PROMPT.md`). Phase VI, in flight.

Phase VI's unit list is `meta/plan.md` §Phase VI, META-144 .. META-165.

## The gate is GREEN at 8e61fdb — 44 steps; 108 codes

**CLUSTERS 1-5 COMPLETE.** Remaining: cluster 6's triage, then the report.

## Current unit

**META-163** — cluster 6: every remaining open finding gets a decision.

### A trap in this ledger, found while preparing this unit

The ledger is append-only, so read the LAST status bullet of each entry, not the first.

## What comes after

META-164 stages the two regression configs and META-165 writes the report.
"""


class OpsCurrentUnit(unittest.TestCase):
    """The current unit is read from one section, and the rest of the file is not evidence.

    The converse of the silently-empty trap in `meta/OPS-CONVENTIONS.md`: this file is *loudly
    full* of `META-###`, so a whole-file scan never looks empty enough to doubt and answers
    confidently with the wrong number.
    """

    def test_a_range_declaration_does_not_become_the_current_unit(self):
        found = ops_status.current_unit(CHECKPOINT_WITH_A_RANGE)
        self.assertEqual(found["unit"], "META-163")
        self.assertEqual(found["number"], 163)
        self.assertIsNone(found["error"])

    def test_the_naive_reads_this_fixture_defeats_really_are_wrong(self):
        """Non-vacuity: without this, the test above passes on a file with no trap in it.

        Both obvious whole-file reads are computed here and both must miss — first match gives
        the low end of the declared range, largest gives the high end, and the unit in flight is
        neither.
        """
        numbers = [int(match) for match in
                   re.findall(r"\bMETA-([0-9]+)\b", CHECKPOINT_WITH_A_RANGE)]
        self.assertEqual(numbers[0], 144, "the fixture must open with the range's low end")
        self.assertEqual(max(numbers), 165, "the fixture must carry a higher number elsewhere")
        self.assertNotIn(163, (numbers[0], max(numbers)))

    def test_a_checkpoint_with_no_current_unit_section_reads_as_none(self):
        """The state the repository is actually in between sessions. `None`, with the reason —
        not the largest number lying around in the prose."""
        text = CHECKPOINT_WITH_A_RANGE.replace("## Current unit\n", "## Nothing in flight\n")
        found = ops_status.current_unit(text)
        self.assertIsNone(found["unit"])
        self.assertIn("no '## Current unit' section", found["error"])

    def test_the_heading_may_carry_trailing_prose(self):
        """The real file has read `## Current unit — the last`."""
        text = CHECKPOINT_WITH_A_RANGE.replace("## Current unit\n",
                                               "## Current unit — the last\n")
        found = ops_status.current_unit(text)
        self.assertEqual(found["unit"], "META-163")
        self.assertEqual(found["heading"], "## Current unit — the last")

    def test_the_section_ends_at_the_next_top_level_heading(self):
        """`META-164` and `META-165` live in a later `##` section and must stay out of it."""
        text = CHECKPOINT_WITH_A_RANGE.replace("**META-163** — cluster 6: every remaining "
                                               "open finding gets a decision.\n", "")
        found = ops_status.current_unit(text)
        self.assertIsNone(found["unit"])
        self.assertIn("names no META-### unit", found["error"])

    def test_a_subheading_stays_inside_the_section(self):
        text = CHECKPOINT_WITH_A_RANGE.replace(
            "**META-163** — cluster 6: every remaining open finding gets a decision.",
            "The unit's notes follow.").replace(
            "### A trap in this ledger, found while preparing this unit",
            "### META-163 — a trap found while preparing this unit")
        self.assertEqual(ops_status.current_unit(text)["unit"], "META-163")


class OpsRunState(unittest.TestCase):
    """Three ways to have no state, reported as three different sentences."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def test_a_stopped_run_reports_its_reason_and_turn(self):
        ops_run_dir(self.root, "it", status="stopped", **{"stop-reason": "epic-done"},
                    turn=12, project="/tmp/p")
        record = ops_status.run_record(self.root, "it")
        self.assertEqual((record["status"], record["stop-reason"], record["turn"]),
                         ("stopped", "epic-done", 12))
        self.assertTrue(record["terminal"])
        self.assertIsNone(record["error"])

    def test_a_missing_directory_a_missing_file_and_a_corrupt_file_differ(self):
        missing = ops_status.run_record(self.root, "absent")["error"]
        os.makedirs(os.path.join(self.root, "runs", "bare"))
        bare = ops_status.run_record(self.root, "bare")["error"]
        directory = os.path.join(self.root, "runs", "corrupt")
        os.makedirs(directory)
        with open(os.path.join(directory, "state.json"), "w", encoding="utf-8") as handle:
            handle.write("{not json")
        corrupt = ops_status.run_record(self.root, "corrupt")["error"]
        self.assertIn("no run directory", missing)
        self.assertIn("no state.json", bare)
        self.assertIn("unreadable", corrupt)
        self.assertEqual(len({missing, bare, corrupt}), 3)


class OpsClassification(unittest.TestCase):
    """The decision table, one case per row, plus the worst-wins order."""

    RUNNING = {"status": "running", "stop-reason": None, "turn": 4, "error": None}
    TERMINAL = {"status": "stopped", "stop-reason": "turn-budget", "turn": 9, "error": None}

    def test_running_owned_and_moving_is_progressing(self):
        self.assertEqual(ops_status.classify_run(self.RUNNING, 1, 3)[:2], (0, "progressing"))

    def test_terminal_is_stopped_with_reason(self):
        code, name, why = ops_status.classify_run(self.TERMINAL, 0, 0)
        self.assertEqual((code, name), (1, "stopped-with-reason"))
        self.assertIn("turn-budget", why)

    def test_running_with_nothing_owning_it_is_the_dead_process_state(self):
        self.assertEqual(ops_status.classify_run(self.RUNNING, 0, 0)[:2],
                         (2, "process-dead-state-running"))

    def test_running_and_owned_but_idle_is_a_stall_candidate(self):
        self.assertEqual(ops_status.classify_run(self.RUNNING, 1, 0)[:2],
                         (3, "stalled-candidate"))

    def test_an_unreadable_state_is_a_stall_candidate_not_a_stop(self):
        """A state that could not be read is not a run that finished. The distinction is the
        conventions' rule that empty output has at least two causes."""
        broken = dict(self.RUNNING, error="state.json unreadable")
        code, _, why = ops_status.classify_run(broken, 1, 5)
        self.assertEqual(code, 3)
        self.assertIn("could not be read", why)

    def test_a_terminal_stop_with_no_recorded_reason_still_says_so(self):
        record = dict(self.TERMINAL, **{"stop-reason": None})
        self.assertIn("(none recorded)", ops_status.classify_run(record, 0, 0)[2])

    def test_the_worst_code_wins_in_the_stated_order(self):
        self.assertEqual(ops_status.worst([0, 1, 3, 2]), 2)
        self.assertEqual(ops_status.worst([0, 1, 3]), 3)
        self.assertEqual(ops_status.worst([0, 1]), 1)
        self.assertEqual(ops_status.worst([0]), 0)
        self.assertEqual(ops_status.worst([]), 0)

    def test_a_live_builder_outranks_a_recent_transcript(self):
        self.assertEqual(ops_status.classify_builder(1, 0.5, 20)[:2], (0, "progressing"))

    def test_a_gone_builder_with_a_warm_transcript_is_the_dead_process_state(self):
        self.assertEqual(ops_status.classify_builder(0, 2.0, 20)[:2],
                         (2, "process-dead-state-running"))

    def test_a_gone_builder_with_a_cold_transcript_is_only_a_stall_candidate(self):
        self.assertEqual(ops_status.classify_builder(0, 90.0, 20)[:2], (3, "stalled-candidate"))


class OpsProcesses(unittest.TestCase):
    """Who counts as a driver — and, more to the point, who does not.

    The rule is the invocation, not the mention. Matching `run_iteration` or `iteration-<id>`
    anywhere in a joined cmdline was wrong on a live run: the ops session's own `bash -c`
    monitor carried both strings in the script text it was about to interpret, and was counted
    as the driver of a run whose real driver had already exited.
    """

    DRIVER = (11, ["python3", "harness/run_iteration.py",
                   "--iteration", "iteration-5-envel", "--turn-timeout", "7200"])
    SCRATCHPAD = (12, ["python3", "/tmp/claude-1000/x/scratchpad/probe.py", "iteration-5-envel"])
    STATUS_TOOL = (13, ["python3", "harness/ops/status.py", "--iteration", "iteration-5-envel"])
    WATCH_TOOL = (14, ["python3", "harness/ops/watch.py", "--iteration", "iteration-5-envel"])
    UNRELATED = (15, ["bash", "-c", "echo unrelated"])

    # Recorded from the live run, trimmed: an ops monitor polling the iteration. Its argv holds
    # the whole loop as ONE string, so `run_iteration` and `iteration-5-envel` are both inside
    # it — and neither says anything about what this process is.
    OPS_MONITOR = (1244620, [
        "/bin/bash", "-c",
        "source /home/msi/.claude/shell-snapshots/snapshot-bash-1788988217359-70tc0z.sh "
        "2>/dev/null || true && eval 'WATCH=1244501; DRIVER=1243961; "
        "REPORT=/home/msi/git/agile-skills/harness/runs/iteration-5-envel/watch-report.txt\n"
        "while true; do\n"
        "  if [ -f \"$REPORT\" ]; then echo \"WATCH-FIRED\"; break; fi\n"
        "  if ! pgrep -af run_iteration >/dev/null; then echo gone; fi\n"
        "  sleep 60\ndone'"])

    ALL = [DRIVER, SCRATCHPAD, STATUS_TOOL, WATCH_TOOL, UNRELATED, OPS_MONITOR]

    def drivers(self, processes, iterations=("iteration-5-envel",), self_pid=99):
        return ops_status.driver_processes(list(iterations), processes=list(processes),
                                           self_pid=self_pid)

    def test_the_driver_is_found(self):
        found = self.drivers(self.ALL)
        self.assertEqual([record["pid"] for record in found], [11])
        self.assertEqual(found[0]["matched"], "iteration-5-envel")

    def test_the_ops_sessions_own_shell_wrapper_is_not_the_driver(self):
        """The live false positive, reproduced. This argv contains both `run_iteration` and
        `iteration-5-envel`; it is a shell holding a script, and the run's real driver was
        already dead when it was reported alive."""
        self.assertEqual(self.drivers([self.OPS_MONITOR]), [])

    def test_a_phantom_driver_would_have_hidden_the_dead_process_case(self):
        """Why it mattered, by execution rather than assertion. With the phantom counted, a run
        whose state still says `running` classifies as a stall instead of a dead driver — the
        one case the probe exists to catch."""
        running = {"status": "running", "stop-reason": None, "turn": 4, "error": None}
        phantom = len(self.drivers([self.OPS_MONITOR]))
        self.assertEqual(phantom, 0)
        self.assertEqual(ops_status.classify_run(running, phantom, 0)[:2],
                         (2, "process-dead-state-running"))
        self.assertEqual(ops_status.classify_run(running, 1, 0)[:2], (3, "stalled-candidate"))

    def test_a_scratchpad_process_that_names_the_iteration_is_not_a_driver(self):
        self.assertEqual(self.drivers([self.SCRATCHPAD]), [])

    def test_a_scratchpad_copy_of_the_driver_itself_is_still_excluded(self):
        """The guard the script-name rule does not subsume: somebody's experiment under the
        scratchpad is a real invocation, and still not this run's driver."""
        copy = (16, ["python3", "/tmp/claude-1000/x/scratchpad/run_iteration.py",
                     "--iteration", "iteration-5-envel"])
        self.assertEqual(self.drivers([copy]), [])

    def test_the_ops_tools_do_not_count_themselves_as_the_driver(self):
        """`status.py --iteration X` carries X in its own argv."""
        self.assertEqual(self.drivers([self.STATUS_TOOL, self.WATCH_TOOL]), [])

    def test_our_own_pid_is_excluded(self):
        self.assertEqual(self.drivers(self.ALL, self_pid=11), [])

    def test_a_driver_for_another_iteration_is_not_this_ones(self):
        other = (17, ["python3", "harness/run_iteration.py", "--iteration", "iteration-4-recall"])
        self.assertEqual(self.drivers([other]), [])
        self.assertEqual([record["pid"] for record in
                          self.drivers([other], iterations=("iteration-4-recall",))], [17])

    def test_the_iteration_is_read_from_the_flag_not_from_the_whole_cmdline(self):
        """A driver for one run whose argv mentions another — a log path, say — belongs to the
        run its `--iteration` flag names, and to no other."""
        confusing = (18, ["python3", "harness/run_iteration.py",
                          "--iteration", "iteration-4-recall",
                          "--note", "supersedes iteration-5-envel"])
        self.assertEqual(self.drivers([confusing]), [])

    def test_the_shebang_invocation_counts(self):
        """`harness/run_iteration.py --iteration X`, run through its own shebang, is how the
        tmux launch actually starts it."""
        shebang = (19, ["harness/run_iteration.py", "--iteration", "iteration-5-envel"])
        self.assertEqual([record["pid"] for record in self.drivers([shebang])], [19])

    def test_the_iteration_flag_is_read_in_both_spellings(self):
        self.assertEqual(ops_status.argv_iterations(
            ["python3", "x.py", "--iteration", "a", "--iteration=b"]), ["a", "b"])

    def test_is_driver_argv_isolated_the_script_name_rule(self):
        """Isolating the rule, because the iteration-flag rule masks it in the end-to-end case.

        The first version of this test file asserted only that the ops monitor was excluded —
        which stayed true when `is_driver_argv` was reverted to the substring match, because the
        flag rule caught it instead. A rule with no test that fails when it is removed is not
        being tested, so each half is pinned here directly.
        """
        # A shell holding the driver's name in the text it is about to interpret.
        self.assertFalse(ops_status.is_driver_argv(
            ["/bin/bash", "-c", "while true; do pgrep -af run_iteration; sleep 60; done"]))
        # A shell asked to interpret the script itself: argv[0] decides, not the argument.
        self.assertFalse(ops_status.is_driver_argv(["bash", "harness/run_iteration.py"]))
        # Anything else merely naming the file.
        self.assertFalse(ops_status.is_driver_argv(["grep", "-n", "x", "run_iteration.py"]))
        self.assertFalse(ops_status.is_driver_argv(["python3", "harness/audit.py"]))
        # And the two shapes that are real, so the rule is not simply "always no".
        self.assertTrue(ops_status.is_driver_argv(
            ["python3", "harness/run_iteration.py", "--iteration", "it"]))
        self.assertTrue(ops_status.is_driver_argv(
            ["harness/run_iteration.py", "--iteration", "it"]))

    def test_a_shell_wrapper_is_excluded_even_when_it_names_the_iteration_by_flag(self):
        """The end-to-end pair for the rule above: an argv that would satisfy the flag rule and
        is still not a driver, so the script-name rule is what has to refuse it."""
        wrapper = (20, ["/bin/bash", "-c", "run the thing", "--iteration", "iteration-5-envel"])
        self.assertEqual(self.drivers([wrapper]), [])

    def test_a_shell_is_recognised_by_argv_zero(self):
        self.assertTrue(ops_status.is_shell(["/bin/bash", "-c", "anything"]))
        self.assertTrue(ops_status.is_shell(["sh", "-c", "anything"]))
        self.assertFalse(ops_status.is_shell(["python3", "harness/run_iteration.py"]))

    def test_an_ops_shell_wrapper_in_the_repo_is_not_a_builder_session(self):
        """Where `is_shell` is load-bearing. `builder_processes` matches the word `claude`
        anywhere in a cmdline, so this session's own `bash -c` wrapper — running in the
        repository, with `claude` inside the script text — is the same false positive one layer
        over. argv[0] alone cannot refuse it here, because the match is not on argv[0]."""
        repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        wrapper = (21, ["/bin/bash", "-c", "pgrep -af claude | wc -l"])
        real = (22, ["claude", "--dangerously-skip-permissions"])
        with mock.patch.object(ops_status, "process_cwd", lambda pid: repo):
            found, _ = ops_status.builder_processes(repo, pid_file=None,
                                                    processes=[wrapper, real], self_pid=99)
        self.assertEqual([record["pid"] for record in found], [22])

    def test_cpu_ticks_survive_a_comm_containing_parentheses(self):
        """Splitting on the first `)` reports a field that is not CPU time at all."""
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        fields = [str(index) for index in range(1, 21)]
        fields[1] = "(od)d (name)"   # a comm with spaces AND parentheses
        fields[13] = "500"           # utime, field 14
        fields[14] = "40"            # stime, field 15
        with mock.patch("builtins.open",
                        mock.mock_open(read_data=" ".join(fields) + "\n")):
            self.assertEqual(ops_status.cpu_ticks(7), 540)

    def test_the_transcript_directory_is_the_project_path_with_slashes_flattened(self):
        self.assertTrue(ops_status.transcript_dir("/home/msi/git/agile-skills", home="/h")
                        .endswith("-home-msi-git-agile-skills"))


class OpsFileActivity(unittest.TestCase):
    """The `find` probe: an absolute stamp, and a stderr that is never thrown away."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def test_the_stamp_is_absolute(self):
        """Relative `-newermt` arguments fail on this machine — the conventions' first rule."""
        stamp = ops_status.activity_stamp(1757520000.0, 20)
        self.assertRegex(stamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        self.assertNotIn("-", stamp.split(" ")[1])

    def test_the_stamp_reaches_find_as_the_newermt_argument(self):
        seen = {}

        def fake(argv, **kwargs):
            seen["argv"] = argv
            return subprocess.CompletedProcess(argv, 0, "one\ntwo\n", "")

        record = ops_status.file_activity(self.root, 20, 1757520000.0, binary="/usr/bin/find",
                                          run=fake)
        self.assertIn("-newermt", seen["argv"])
        self.assertEqual(seen["argv"][seen["argv"].index("-newermt") + 1], record["stamp"])
        self.assertEqual(record["count"], 2)

    def test_a_find_that_errored_reports_its_stderr_rather_than_an_empty_result(self):
        """Empty output has at least two causes. A probe that discards stderr fails toward the
        wrong verdict, which is exactly how the `bfs` trap was missed."""
        def fake(argv, **kwargs):
            return subprocess.CompletedProcess(argv, 1, "", "find: bad -newermt argument\n")

        record = ops_status.file_activity(self.root, 20, 1757520000.0, binary="/usr/bin/find",
                                          run=fake)
        self.assertEqual(record["count"], 0)
        self.assertEqual(record["returncode"], 1)
        self.assertIn("bad -newermt argument", record["stderr"])


class OpsBoard(unittest.TestCase):
    def setUp(self):
        self.project = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.project, ignore_errors=True)
        os.makedirs(os.path.join(self.project, "tracker"))

    def write_board(self, text):
        with open(os.path.join(self.project, "tracker", "board.md"), "w",
                  encoding="utf-8") as handle:
            handle.write(text)

    def test_the_summary_section_is_read_and_stops_at_the_next_heading(self):
        self.write_board("# Board\n\n## EP-001 — a thing  (done)\n\nrows\n\n## Summary\n\n"
                         "- 6 item(s): 6 done\n- blocked: none\n\n## After\n\n- not this\n")
        summary, error = ops_status.board_summary(self.project)
        self.assertIsNone(error)
        self.assertEqual(summary["lines"], ["- 6 item(s): 6 done", "- blocked: none"])

    def test_a_missing_board_is_an_error_not_an_empty_summary(self):
        summary, error = ops_status.board_summary(self.project)
        self.assertIsNone(summary)
        self.assertIn("no board at", error)

    def test_no_project_path_says_so(self):
        self.assertIn("no project path", ops_status.board_summary(None)[1])


class OpsWatchArming(unittest.TestCase):
    """What the watch refuses to arm, and why."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        os.makedirs(os.path.join(self.repo, "meta"))

    def checkpoint(self, text):
        with open(os.path.join(self.repo, "meta", "CHECKPOINT.md"), "w",
                  encoding="utf-8") as handle:
            handle.write(text)

    def arm(self, args):
        tracker = ops_watch.Tracker()
        armed, skipped, lines = ops_watch.arm_triggers(args, tracker, self.root, self.repo)
        return tracker, armed, skipped, lines

    def test_a_run_terminal_at_arm_is_announced_and_never_armed(self):
        """A run that stopped before the watch started is history. Arming it would let the watch
        'fire' on a stop that happened yesterday."""
        ops_run_dir(self.root, "it", status="stopped", **{"stop-reason": "epic-done"}, turn=9)
        _, armed, skipped, lines = self.arm(ops_args(iteration=["it"], on_stop=True))
        self.assertEqual([trigger for trigger in armed if trigger["kind"] == "stop"], [])
        self.assertEqual(len(skipped), 1)
        self.assertIn("terminal at arm", skipped[0])
        self.assertIn("epic-done", skipped[0])
        self.assertTrue(any("status='stopped'" in line for line in lines))

    def test_a_running_run_is_armed(self):
        """Non-vacuity for the exclusion above: without it, nothing proves the skip is
        conditional rather than a watch that never arms anything."""
        ops_run_dir(self.root, "it", status="running", turn=3)
        _, armed, skipped, _ = self.arm(ops_args(iteration=["it"], on_stop=True))
        self.assertEqual([trigger["kind"] for trigger in armed], ["stop"])
        self.assertEqual(skipped, [])

    def test_an_unreadable_state_at_arm_is_armed_rather_than_skipped(self):
        """A state that could not be read is not a run known to be terminal. Skipping it would
        turn an instrument failure into a decision."""
        _, armed, skipped, lines = self.arm(ops_args(iteration=["gone"], on_stop=True))
        self.assertEqual([trigger["kind"] for trigger in armed], ["stop"])
        self.assertEqual(skipped, [])
        self.assertTrue(any("UNREADABLE" in line for line in lines))

    def test_a_file_already_complete_at_arm_is_skipped(self):
        path = os.path.join(self.root, "report.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# Report\n\nAll done.\n")
        _, armed, skipped, _ = self.arm(ops_args(on_file_complete=[path]))
        self.assertEqual(armed, [])
        self.assertIn("already complete at arm", skipped[0])

    def test_a_file_that_still_says_pending_is_armed(self):
        path = os.path.join(self.root, "report.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("# Report\n\n## Verdict\n\n*Pending*\n")
        _, armed, skipped, _ = self.arm(ops_args(on_file_complete=[path]))
        self.assertEqual([trigger["kind"] for trigger in armed], ["file-complete"])
        self.assertEqual(skipped, [])

    def test_a_unit_threshold_already_met_at_arm_is_skipped(self):
        self.checkpoint(CHECKPOINT_WITH_A_RANGE)
        _, armed, skipped, _ = self.arm(ops_args(on_unit_gte=160))
        self.assertEqual(armed, [])
        self.assertIn("already satisfied at arm", skipped[0])
        self.assertIn("META-163", skipped[0])

    def test_a_unit_threshold_not_yet_met_is_armed_against_the_section_not_the_file(self):
        """META-165 appears in this checkpoint's prose. If the threshold were read from the
        whole file, `--on-unit-gte 165` would be satisfied at arm and could never fire."""
        self.checkpoint(CHECKPOINT_WITH_A_RANGE)
        _, armed, skipped, lines = self.arm(ops_args(on_unit_gte=165))
        self.assertEqual([trigger["kind"] for trigger in armed], ["unit-gte"])
        self.assertEqual(skipped, [])
        self.assertTrue(any("META-163" in line for line in lines))

    def test_a_checkpoint_with_no_section_arms_rather_than_guessing(self):
        self.checkpoint("# CHECKPOINT\n\nNothing in flight. META-165 closed the session.\n")
        _, armed, skipped, lines = self.arm(ops_args(on_unit_gte=165))
        self.assertEqual([trigger["kind"] for trigger in armed], ["unit-gte"])
        self.assertTrue(any("UNREADABLE" in line for line in lines))


class OpsWatchBaseline(unittest.TestCase):
    """The rule that keeps a watch able to see anything: a parse failure updates nothing."""

    def test_a_parse_failure_keeps_the_baseline_and_the_last_good_observation(self):
        tracker = ops_watch.Tracker()
        tracker.arm("run:it", True, {"status": "running", "turn": 3})
        moved = tracker.observe("run:it", True, {"status": "running", "turn": 4})
        self.assertTrue(moved["changed"])

        failed = tracker.observe("run:it", False, None, "state.json unreadable")
        self.assertTrue(failed["kept"])
        self.assertFalse(failed["changed"])
        self.assertEqual(failed["error"], "state.json unreadable")
        # Neither store moved: the baseline is still what arm saw, and the current observation
        # is still the last one that parsed.
        self.assertEqual(tracker.baseline["run:it"]["value"], {"status": "running", "turn": 3})
        self.assertEqual(tracker.current["run:it"], {"status": "running", "turn": 4})

    def test_the_next_good_observation_is_still_compared_against_the_kept_value(self):
        """The consequence the rule exists for. Folding the failure in would make this
        comparison run against `None`, and the watch would report a change that is really just
        the instrument recovering."""
        tracker = ops_watch.Tracker()
        tracker.arm("run:it", True, {"turn": 4})
        tracker.observe("run:it", False, None, "unreadable")
        again = tracker.observe("run:it", True, {"turn": 4})
        self.assertFalse(again["changed"])
        self.assertEqual(again["previous"], {"turn": 4})

    def test_an_arm_that_failed_to_parse_holds_no_current_value(self):
        tracker = ops_watch.Tracker()
        tracker.arm("unit", False, None, "no '## Current unit' section")
        self.assertNotIn("unit", tracker.current)
        self.assertFalse(tracker.baseline["unit"]["ok"])


class OpsNewRunDir(unittest.TestCase):
    """Terminal-at-arm directories are history, not events."""

    ARM = {"old": {"status": "stopped", "terminal": True, "started": "A", "error": None},
           "live": {"status": "running", "terminal": False, "started": "B", "error": None}}

    def test_a_terminal_directory_that_is_still_terminal_fires_nothing(self):
        events, errors = ops_watch.new_rundir_events(self.ARM, dict(self.ARM))
        self.assertEqual(events, [])
        self.assertEqual(errors, [])

    def test_a_directory_absent_at_arm_is_an_event(self):
        observed = dict(self.ARM)
        observed["new"] = {"status": "running", "terminal": False, "started": "C", "error": None}
        events, _ = ops_watch.new_rundir_events(self.ARM, observed)
        self.assertEqual([event["name"] for event in events], ["new"])
        self.assertIn("absent at arm", events[0]["evidence"])

    def test_a_terminal_directory_that_came_back_to_life_is_an_event(self):
        """What `--fresh` reusing the same path looks like from outside: the name was in the
        baseline, so a name-only comparison would miss the new run entirely."""
        observed = dict(self.ARM)
        observed["old"] = {"status": "running", "terminal": False, "started": "D", "error": None}
        events, _ = ops_watch.new_rundir_events(self.ARM, observed)
        self.assertEqual([event["name"] for event in events], ["old"])
        self.assertIn("the path was reused", events[0]["evidence"])

    def test_a_restarted_run_in_a_live_directory_is_an_event(self):
        observed = dict(self.ARM)
        observed["live"] = {"status": "running", "terminal": False, "started": "Z", "error": None}
        events, _ = ops_watch.new_rundir_events(self.ARM, observed)
        self.assertEqual([event["name"] for event in events], ["live"])
        self.assertIn("a different run in the same path", events[0]["evidence"])

    def test_an_unreadable_directory_is_a_probe_error_and_not_a_new_run(self):
        """A run mid-write must not be announced as a new run — and the read that failed must
        not vanish either."""
        observed = dict(self.ARM)
        observed["half"] = {"status": None, "terminal": None, "started": None,
                            "error": "state.json unreadable"}
        events, errors = ops_watch.new_rundir_events(self.ARM, observed)
        self.assertEqual(events, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("half", errors[0])


class OpsWatchLoop(unittest.TestCase):
    """One report per invocation, and the trigger's evidence verbatim inside it."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        os.makedirs(os.path.join(self.repo, "meta"))

    def drive(self, args, steps):
        """Run the loop over a fake clock; `steps` runs before each poll."""
        ticks = iter(range(0, 100000, 60))
        state = {"n": 0}

        def clock():
            return float(next(ticks))

        def sleeper(_):
            if state["n"] < len(steps):
                steps[state["n"]]()
            state["n"] += 1

        out, err = io.StringIO(), io.StringIO()
        code = ops_watch.run_watch(args, out=out, err=err, clock=clock, sleeper=sleeper,
                                   harness=self.root, repo=self.repo)
        return code, out.getvalue(), err.getvalue()

    def test_a_stop_fires_once_with_its_evidence_and_writes_one_report(self):
        ops_run_dir(self.root, "it", status="running", turn=3)
        report_file = os.path.join(self.root, "watch-report.txt")

        def stop_it():
            ops_run_dir(self.root, "it", status="stopped",
                        **{"stop-reason": "epic-done"}, turn=7)

        code, out, _ = self.drive(
            ops_args(iteration=["it"], on_stop=True, poll_minutes=1, timeout_hours=1,
                     report_file=report_file),
            [lambda: None, stop_it])
        self.assertEqual(code, 0)
        self.assertEqual(out.count("# watch report"), 1)
        self.assertIn("TRIGGER         stop it", out)
        self.assertIn("stop-reason='epic-done'", out)
        self.assertIn("at arm: {'status': 'running'", out)
        with open(report_file, encoding="utf-8") as handle:
            self.assertIn("stop-reason='epic-done'", handle.read())

    def test_a_timeout_with_no_trigger_still_writes_exactly_one_report(self):
        ops_run_dir(self.root, "it", status="running", turn=3)
        code, out, _ = self.drive(
            ops_args(iteration=["it"], on_stop=True, poll_minutes=1, timeout_hours=0.05), [])
        self.assertEqual(code, 3)
        self.assertEqual(out.count("# watch report"), 1)
        self.assertIn("TRIGGER         none — the timeout was reached", out)
        self.assertIn("elapsed", out)

    def test_a_probe_error_is_printed_and_carried_into_the_report_not_read_as_silence(self):
        ops_run_dir(self.root, "it", status="running", turn=3)

        def corrupt():
            with open(os.path.join(self.root, "runs", "it", "state.json"), "w",
                      encoding="utf-8") as handle:
                handle.write("{broken")

        code, out, err = self.drive(
            ops_args(iteration=["it"], on_stop=True, poll_minutes=1, timeout_hours=0.05),
            [corrupt])
        self.assertEqual(code, 3)
        self.assertIn("probe error", err)
        self.assertIn("probe error", out)
        self.assertIn("unreadable", out)

    def test_a_new_run_directory_notes_and_the_watch_keeps_going(self):
        """`--on-new-rundir` is note-and-continue: a run STARTING is not the thing a watch of a
        run is waiting for, so the report is still written by the timeout."""
        ops_run_dir(self.root, "old", status="stopped", **{"stop-reason": "epic-done"}, turn=2)

        def start():
            ops_run_dir(self.root, "fresh", status="running", turn=1, started="now")

        code, out, err = self.drive(
            ops_args(on_new_rundir=True, poll_minutes=1, timeout_hours=0.08), [start])
        self.assertEqual(code, 3)
        self.assertIn("note — new-rundir", err)
        self.assertIn("fresh: absent at arm", out)
        self.assertIn("TRIGGER         none", out)

    def test_a_watch_with_nothing_left_to_arm_says_so_at_arm(self):
        ops_run_dir(self.root, "it", status="stopped", **{"stop-reason": "epic-done"}, turn=2)
        code, out, _ = self.drive(
            ops_args(iteration=["it"], on_stop=True, poll_minutes=1, timeout_hours=0.05), [])
        self.assertEqual(code, 3)
        self.assertIn("this watch can only time out", out)


class OpsWatchArguments(unittest.TestCase):
    def test_a_watch_with_no_trigger_is_refused(self):
        with self.assertRaises(SystemExit):
            with mock.patch("sys.stderr", io.StringIO()):
                ops_watch.parse_args(["--iteration", "it"])

    def test_on_stop_without_an_iteration_is_refused(self):
        with self.assertRaises(SystemExit):
            with mock.patch("sys.stderr", io.StringIO()):
                ops_watch.parse_args(["--on-stop"])

    def test_the_defaults_are_the_documented_ones(self):
        args = ops_watch.parse_args(["--iteration", "it", "--on-stop"])
        self.assertEqual((args.poll_minutes, args.timeout_hours), (15, 6))

    def test_status_needs_a_subject(self):
        with self.assertRaises(SystemExit):
            with mock.patch("sys.stderr", io.StringIO()):
                ops_status.parse_args([])

if __name__ == "__main__":
    unittest.main(verbosity=2)
