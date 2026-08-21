"""The store in isolation: WI-0001 AC5 and AC6, and ADR-0002."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from expenses import store
from expenses.errors import ExpensesError


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "nested" / "deeper" / "store.json"
        previous = os.environ.get("EXPENSES_STORE")
        os.environ["EXPENSES_STORE"] = str(self.path)
        self.addCleanup(self._restore, previous)

    def _restore(self, previous):
        if previous is None:
            os.environ.pop("EXPENSES_STORE", None)
        else:
            os.environ["EXPENSES_STORE"] = previous

    def test_missing_store_loads_as_an_empty_group(self):
        # AC5: reading against a store that does not exist succeeds.
        self.assertFalse(self.path.exists())
        self.assertEqual(store.load(), {"version": 1, "people": [], "expenses": []})
        self.assertFalse(self.path.exists(), "load must not create the file")

    def test_save_creates_missing_parent_directories(self):
        # AC5: the first write creates the file and its parents, no setup step.
        data = store.empty()
        data["people"].append("Alice")
        store.save(data)
        self.assertTrue(self.path.exists())
        self.assertEqual(json.loads(self.path.read_text())["people"], ["Alice"])

    def test_damaged_store_is_fatal_to_reads_and_is_left_alone(self):
        # AC6.
        self.path.parent.mkdir(parents=True)
        self.path.write_bytes(b"not json at all")
        before = self.path.read_bytes()
        with self.assertRaises(ExpensesError) as caught:
            store.load()
        self.assertIn(str(self.path), str(caught.exception))
        self.assertEqual(self.path.read_bytes(), before)

    def test_a_store_that_is_json_but_not_a_store_is_fatal(self):
        # AC6: valid JSON is not enough; it must be an expenses store.
        self.path.parent.mkdir(parents=True)
        self.path.write_text('["Alice", "Bob"]')
        with self.assertRaises(ExpensesError):
            store.load()

    def test_a_roster_entry_that_is_not_a_string_is_fatal(self):
        # AC6, ADR-0002 decision 6, review.md F1: the containers being lists is
        # not enough, because everything above this module treats an entry as a
        # string. The message names the path and the offending type.
        self.path.parent.mkdir(parents=True)
        self.path.write_text('{"version": 1, "people": ["Alice", 123], "expenses": []}')
        before = self.path.read_bytes()
        with self.assertRaises(ExpensesError) as caught:
            store.load()
        self.assertIn(str(self.path), str(caught.exception))
        self.assertIn("int", str(caught.exception))
        self.assertEqual(self.path.read_bytes(), before)

    def test_the_temporary_file_is_not_left_behind(self):
        store.save(store.empty())
        leftovers = [p.name for p in self.path.parent.iterdir() if p.name != self.path.name]
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
