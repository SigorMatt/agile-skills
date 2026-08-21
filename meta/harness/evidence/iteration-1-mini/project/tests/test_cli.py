"""The CLI end to end, in real subprocesses.

A subprocess is required rather than preferred: AC2 is a claim about a *fresh*
process, and AC8 is a claim about what reaches the user's terminal. Calling
``main()`` in-process would test neither.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CliTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name) / "store.json"

    def run_cli(self, *args):
        env = dict(os.environ)
        env["EXPENSES_STORE"] = str(self.store)
        env["PYTHONPATH"] = str(ROOT)
        return subprocess.run(
            [sys.executable, "-m", "expenses", *args],
            capture_output=True, text=True, env=env, cwd=str(ROOT),
        )

    def assertFailedCleanly(self, result):
        """AC8, applied to every failing invocation in this file."""
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn("Traceback", result.stdout)
        self.assertTrue(result.stderr.strip(), "a failure must say what was wrong")
        self.assertEqual(result.stdout, "", "a failure must not print on stdout")

    # ---- AC1 -------------------------------------------------------------
    def test_help_lists_both_commands(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("add-person", result.stdout)
        self.assertIn("people", result.stdout)

    def test_listing_prints_one_bare_name_per_line_in_insertion_order(self):
        # Zoe is added before Carol on purpose: alphabetical order would swap
        # them, so this asserts insertion order rather than merely agreeing
        # with it. Alice/Bob alone could not tell the two apart.
        for name in ("Alice", "Zoe", "Carol"):
            self.run_cli("add-person", name)
        result = self.run_cli("people")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Alice\nZoe\nCarol\n")

    # ---- AC2 -------------------------------------------------------------
    def test_the_roster_survives_into_a_fresh_process(self):
        self.assertEqual(self.run_cli("add-person", "Alice").returncode, 0)
        self.assertEqual(self.run_cli("add-person", "Zoe").returncode, 0)
        self.assertEqual(self.run_cli("add-person", "Carol").returncode, 0)
        # A fourth, separate interpreter: nothing can have survived in memory.
        # Not alphabetical, so "in the same order" is actually asserted.
        self.assertEqual(self.run_cli("people").stdout, "Alice\nZoe\nCarol\n")

    # ---- AC3 -------------------------------------------------------------
    def test_a_duplicate_is_refused_however_it_is_spelled(self):
        self.run_cli("add-person", "Alice")
        for spelling in ("Alice", "alice", "ALICE", "  Alice  "):
            with self.subTest(spelling=spelling):
                result = self.run_cli("add-person", spelling)
                self.assertFailedCleanly(result)
                self.assertIn("Alice", result.stderr)
                self.assertEqual(self.run_cli("people").stdout, "Alice\n")

    def test_matching_goes_through_one_key_function(self):
        # match_key is AC3's comparison rule, and add() must compare through it
        # rather than lowercasing inline -- otherwise the rule lives in two
        # places and WI-0002, which matches sharers against the roster, will
        # adopt the copy that nobody changes. Asserting on the function keeps
        # it referenced; asserting through the CLI keeps add() honest.
        from expenses import people
        self.assertEqual(people.match_key("  ALICE  "), people.match_key("alice"))
        self.assertEqual(self.run_cli("add-person", "Alice").returncode, 0)
        self.assertFailedCleanly(self.run_cli("add-person", "  ALICE  "))

    def test_the_first_spelling_is_the_one_kept(self):
        self.run_cli("add-person", "  Alice  ")
        self.assertEqual(self.run_cli("people").stdout, "Alice\n")

    # ---- AC4 -------------------------------------------------------------
    def test_listing_an_empty_group_succeeds_and_says_so(self):
        result = self.run_cli("people")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Nobody", result.stdout)

    # ---- AC5 -------------------------------------------------------------
    def test_the_store_is_created_on_first_use_with_no_setup_step(self):
        self.assertFalse(self.store.exists())
        self.assertEqual(self.run_cli("add-person", "Alice").returncode, 0)
        self.assertTrue(self.store.exists())
        self.assertEqual(self.run_cli("people").stdout, "Alice\n")

    # ---- AC6 -------------------------------------------------------------
    def test_a_damaged_store_is_fatal_to_reads_and_writes_and_is_left_alone(self):
        self.store.write_bytes(b"{ this is not json")
        before = self.store.read_bytes()
        for args in (("people",), ("add-person", "Bob")):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertFailedCleanly(result)
                self.assertIn(str(self.store), result.stderr)
                self.assertEqual(self.store.read_bytes(), before,
                                 "the damaged file must be left for the user to rescue")

    def test_a_roster_entry_that_is_not_a_name_is_fatal_to_both_commands(self):
        # review.md F1. store.load() checked that `people` was a list but not
        # what was in it, so these parsed and then raised AttributeError out of
        # people.normalise() -- a traceback, exit 1, which AC8 forbids. AC6 and
        # ADR-0002 decision 6 want a named error from *both* commands instead.
        for junk in (123, {"name": "Alice"}, ["Alice"], None, 1.5, True):
            with self.subTest(junk=junk):
                self.store.write_text(json.dumps(
                    {"version": 1, "people": [junk], "expenses": []}))
                before = self.store.read_bytes()
                for args in (("people",), ("add-person", "Carol")):
                    result = self.run_cli(*args)
                    self.assertFailedCleanly(result)
                    self.assertIn(str(self.store), result.stderr)
                    self.assertEqual(self.store.read_bytes(), before)

    def test_a_stored_name_todays_rules_would_reject_does_not_blame_the_new_name(self):
        # review.md F2. add() compared through match_key(existing), and
        # match_key validated, so a stored name containing a control character
        # made `add-person Carol` fail claiming *Carol* held one.
        bad = "Al" + chr(7) + "ice"
        self.store.write_text(json.dumps(
            {"version": 1, "people": [bad, "Bob"], "expenses": []}))
        result = self.run_cli("add-person", "Carol")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("control character", result.stderr)
        self.assertEqual(self.run_cli("people").stdout, bad + "\nBob\nCarol\n")

    def test_an_unexpected_exception_is_reported_not_dumped(self):
        # AC8 as a property of cli.main rather than of every module below it
        # agreeing to raise only ExpensesError (review.md F3). Driven through
        # main()'s out/err parameters, which is also the only thing that
        # exercises them.
        driver = (
            "import io, sys\n"
            "sys.path.insert(0, %r)\n"
            "from expenses import cli, store\n"
            "store.load = lambda: (_ for _ in ()).throw(RuntimeError('boom'))\n"
            "out, err = io.StringIO(), io.StringIO()\n"
            "code = cli.main(['people'], out=out, err=err)\n"
            "print('CODE', code)\n"
            "print('OUT', repr(out.getvalue()))\n"
            "print('ERR', repr(err.getvalue()))\n"
        ) % str(ROOT)
        result = subprocess.run([sys.executable, "-c", driver],
                                capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Traceback", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("CODE 2", result.stdout)
        self.assertIn("OUT ''", result.stdout)
        self.assertIn("RuntimeError", result.stdout)
        self.assertIn("bug in the tool", result.stdout)

    # ---- AC7 -------------------------------------------------------------
    def test_an_empty_or_missing_name_is_refused(self):
        for args in (("add-person", ""), ("add-person", "   "), ("add-person",)):
            with self.subTest(args=args):
                self.assertFailedCleanly(self.run_cli(*args))
                self.assertIn("Nobody", self.run_cli("people").stdout)

    def test_a_name_containing_a_newline_is_refused(self):
        # ADR-0006 rule 5: it would break AC1's one-name-per-line listing.
        self.assertFailedCleanly(self.run_cli("add-person", "Alice\nBob"))

    def test_a_name_may_contain_a_comma_and_non_ascii_text(self):
        # ADR-0006 rule 4: nothing is split on a delimiter, so nothing is reserved.
        self.assertEqual(self.run_cli("add-person", "Bob, Jr").returncode, 0)
        self.assertEqual(self.run_cli("add-person", "Zoë").returncode, 0)
        self.assertEqual(self.run_cli("people").stdout, "Bob, Jr\nZoë\n")

    # ---- AC8 -------------------------------------------------------------
    def test_no_command_at_all_fails_cleanly(self):
        self.assertFailedCleanly(self.run_cli())

    def test_an_unknown_command_fails_cleanly(self):
        self.assertFailedCleanly(self.run_cli("frobnicate"))


if __name__ == "__main__":
    unittest.main()
