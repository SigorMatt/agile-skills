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
import re
import shutil
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
                "SKILLS_PER_TURN": 3, "NOW": "2026-08-21T00:00:00Z"}), name)


class StopClassification(unittest.TestCase):
    """H-002: a stop is either an interruption you resume or a verdict you do not."""

    def test_an_interrupted_turn_is_resumable(self):
        for reason in ("turn-failed", "turn-timeout", "api-rejected"):
            self.assertTrue(run_iteration.stop_is_resumable(reason), reason)

    def test_a_verdict_is_not_resumable(self):
        for reason in ("epic-done", "blocked-no-recourse", "contamination",
                       "validator-failed", "stalled"):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
