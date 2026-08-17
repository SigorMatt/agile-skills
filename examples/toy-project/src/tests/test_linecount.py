"""Tests for linecount, one per acceptance criterion of WI-0001.

Two layers, as `docs/architecture/overview.md` v1 describes: the unit layer calls `count_lines`
and `format_report` directly, because that is where the criteria are arithmetic; the end-to-end
layer runs the script as a subprocess, because that is the only layer where an exit code and a
stream exist. Standard library only.
"""

import os
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

import linecount

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "linecount.py")
IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0
NOT_AS_ROOT = "root can read what a non-root user cannot; AC11 says 'tested as a non-root user'"


def write(folder, name, data):
    """Create `name` inside `folder` holding `data` (bytes), and return its path."""
    path = os.path.join(folder, name)
    with open(path, "wb") as handle:
        handle.write(data)
    return path


def png_bytes():
    """A real 1x1 PNG, built here so the tests need no binary fixture in the repository."""
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    header = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(b"\x00\xff\x00\x00"))
            + chunk(b"IEND", b""))


def run(*args):
    """Run the script as a user would, and return the completed process (bytes streams)."""
    return subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True)


class CountLinesTest(unittest.TestCase):
    """AC5 — a line is a newline byte, plus one for a final line without one."""

    def count(self, data):
        with tempfile.TemporaryDirectory() as folder:
            return linecount.count_lines(write(folder, "f", data))

    def test_ac5_counting_rule(self):
        self.assertEqual(self.count(b"a\nb\n"), 2)
        self.assertEqual(self.count(b"a\nb"), 2)
        self.assertEqual(self.count(b"\n"), 1)
        self.assertEqual(self.count(b""), 0)

    def test_ac5_rule_holds_across_chunk_boundary(self):
        # Three chunks' worth, so the count cannot come from a single read, and the last byte
        # test cannot look at the first chunk.
        expected = (3 * linecount.CHUNK) // 2
        self.assertEqual(self.count(b"x\n" * expected), expected)

    def test_ac5_trailing_byte_after_a_chunk_boundary(self):
        expected = (3 * linecount.CHUNK) // 2
        self.assertEqual(self.count(b"x\n" * expected + b"tail"), expected + 1)

    def test_ac9_bytes_are_never_decoded(self):
        # Invalid UTF-8. Decoding this would raise; counting its newline bytes does not.
        self.assertEqual(self.count(b"\xff\xfe\n\x00\x80\n"), 2)


class FormatReportTest(unittest.TestCase):
    """AC1, AC3, AC10 — the row format, the total row, and the empty case."""

    def test_ac1_format_report_unit(self):
        self.assertEqual(
            linecount.format_report([(128, "notes.md"), (7, "a.py")]),
            "128  notes.md\n  7  a.py\n135  total\n")

    def test_ac1_column_is_as_wide_as_the_widest_number_printed(self):
        # The total is wider than any single count, so the total sets the column width.
        self.assertEqual(
            linecount.format_report([(6, "a"), (5, "b")]),
            " 6  a\n 5  b\n11  total\n")

    def test_ac3_total_is_the_sum_and_comes_last(self):
        report = linecount.format_report([(3, "a"), (2, "b"), (1, "c")])
        self.assertEqual(report.splitlines()[-1], "6  total")

    def test_ac10_no_rows_is_no_files_and_no_total(self):
        self.assertEqual(linecount.format_report([]), "no files\n")


class EndToEndTest(unittest.TestCase):
    """The criteria that name a stream or an exit code, checked by running the script."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def file(self, name, lines=None, data=None):
        if data is None:
            data = b"x\n" * lines
        return write(self.folder, name, data)

    def test_ac1_exact_output_for_two_files(self):
        self.file("notes.md", 128)
        self.file("a.py", 7)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"128  notes.md\n  7  a.py\n135  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac1_name_is_bare_not_a_path(self):
        self.file("only.txt", 2)
        self.assertEqual(run(self.folder).stdout, b"2  only.txt\n2  total\n")

    def test_ac2_ties_break_on_filename_byte_order(self):
        self.file("a.md", 3)
        self.file("A.md", 3)
        self.file("big.md", 9)
        self.assertEqual(run(self.folder).stdout,
                         b" 9  big.md\n 3  A.md\n 3  a.md\n15  total\n")

    def test_ac2_two_runs_are_byte_identical(self):
        for index in range(12):
            self.file(f"f{index}.txt", index % 4)
        first, second = run(self.folder), run(self.folder)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, second.stderr)
        self.assertEqual(first.returncode, second.returncode)

    def test_ac3_last_row_is_the_total_in_the_same_column(self):
        self.file("a.txt", 100)
        self.file("b.txt", 20)
        self.file("c.txt", 3)
        lines = run(self.folder).stdout.decode().splitlines()
        self.assertEqual(lines[-1], "123  total")
        self.assertEqual(len(lines), 4)

    def test_ac4_empty_file_is_listed_as_zero(self):
        self.file("empty.txt", data=b"")
        self.file("full.txt", 5)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"5  full.txt\n0  empty.txt\n5  total\n")
        self.assertEqual(result.returncode, 0)

    def test_ac6_subdirectory_is_ignored(self):
        self.file("a.txt", 4)
        os.mkdir(os.path.join(self.folder, "sub"))
        self.file(os.path.join("sub", "hidden.txt"), 99)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"4  a.txt\n4  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac7_symlink_to_a_file_is_listed_under_its_own_name(self):
        target = self.file("target.txt", 6)
        os.symlink(target, os.path.join(self.folder, "link.txt"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b" 6  link.txt\n 6  target.txt\n12  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac7_symlink_to_a_directory_is_ignored(self):
        self.file("a.txt", 4)
        os.mkdir(os.path.join(self.folder, "sub"))
        os.symlink(os.path.join(self.folder, "sub"), os.path.join(self.folder, "dirlink"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"4  a.txt\n4  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac7_broken_symlink_is_ignored(self):
        self.file("a.txt", 4)
        os.symlink(os.path.join(self.folder, "gone.txt"), os.path.join(self.folder, "broken"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"4  a.txt\n4  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac8_dotfile_is_listed(self):
        self.file(".gitignore", 2)
        self.file("a.txt", 5)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"5  a.txt\n2  .gitignore\n7  total\n")
        self.assertEqual(result.returncode, 0)

    def test_ac9_a_png_is_counted_like_any_other_file(self):
        self.file("image.png", data=png_bytes())
        self.file("a.txt", 5)
        self.file("b.txt", 3)
        result = run(self.folder)
        self.assertEqual(len(result.stdout.splitlines()), 4)  # three files plus the total
        self.assertIn(b"image.png", result.stdout)
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(b"Traceback", result.stdout)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_ac10_empty_folder(self):
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac10_folder_holding_only_subdirectories(self):
        os.mkdir(os.path.join(self.folder, "one"))
        os.mkdir(os.path.join(self.folder, "two"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac11_path_that_does_not_exist(self):
        missing = os.path.join(self.folder, "nope")
        result = run(missing)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(missing.encode(), result.stderr)
        self.assertEqual(result.returncode, 2)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac11_folder_that_cannot_be_read(self):
        unreadable = os.path.join(self.folder, "noread")
        os.mkdir(unreadable)
        os.chmod(unreadable, 0o000)
        self.addCleanup(os.chmod, unreadable, 0o700)
        result = run(unreadable)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(unreadable.encode(), result.stderr)
        self.assertEqual(result.returncode, 2)

    def test_ac12_path_is_a_regular_file(self):
        path = self.file("a.txt", 3)
        result = run(path)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr.strip())
        self.assertEqual(result.returncode, 2)

    def test_ac12_no_argument_at_all(self):
        result = run()
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr.strip())
        self.assertEqual(result.returncode, 2)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_unreadable_file_is_reported_and_skipped(self):
        """ADR-0002 — no criterion covers this, but the code must do something."""
        secret = self.file("secret.txt", 4)
        os.chmod(secret, 0o000)
        self.addCleanup(os.chmod, secret, 0o600)
        self.file("a.txt", 5)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"5  a.txt\n5  total\n")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(b"secret.txt", result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)
        self.assertEqual(result.returncode, 0)


class ParseTopTest(unittest.TestCase):
    """WI-0002 AC7 — what `--top` accepts, and what it refuses, before any folder is touched."""

    def test_parse_top_accepts(self):
        self.assertEqual(linecount.parse_top("3"), 3)
        self.assertEqual(linecount.parse_top("0"), 0)
        self.assertEqual(linecount.parse_top("99"), 99)

    def test_parse_top_rejects(self):
        for value in ("-1", "abc", "", "3.5", "3x"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError) as caught:
                    linecount.parse_top(value)
                self.assertTrue(str(caught.exception))  # the message is what main prints


class TopFormatTest(unittest.TestCase):
    """WI-0002 AC3, AC6, AC10 at the renderer, where the criteria are arithmetic.

    A separate class from `FormatReportTest` on purpose: WI-0002 AC4 requires WI-0001's tests to
    pass unmodified, and the cheapest way to prove that is to leave their classes untouched.
    """

    def test_ac3_explicit_total_and_label(self):
        self.assertEqual(
            linecount.format_report([(9, "big.txt")], 1204, "total (all 27 files)"),
            "   9  big.txt\n1204  total (all 27 files)\n")

    def test_ac10_width_covers_an_explicit_total(self):
        # The exact three lines AC10 spells out, space for space.
        self.assertEqual(
            linecount.format_report([(9, "big.txt"), (7, "next.txt")], 1204,
                                    "total (all 27 files)"),
            "   9  big.txt\n   7  next.txt\n1204  total (all 27 files)\n")

    def test_ac6_no_rows_but_an_explicit_total_prints_the_total_row(self):
        self.assertEqual(linecount.format_report([], 41, "total (all 27 files)"),
                         "41  total (all 27 files)\n")

    def test_ac4_the_old_calls_are_unchanged(self):
        # The same two calls WI-0001's tests make, asserted here too: adding parameters must not
        # have changed what the one-argument form does.
        self.assertEqual(linecount.format_report([(128, "notes.md"), (7, "a.py")]),
                         "128  notes.md\n  7  a.py\n135  total\n")
        self.assertEqual(linecount.format_report([]), "no files\n")


class TopTest(unittest.TestCase):
    """WI-0002 end to end: the script run as a user would run it, with `--top`."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def file(self, name, lines):
        return write(self.folder, name, b"x\n" * lines)

    def test_ac1_top_three_prints_three_rows_and_a_total(self):
        for name, lines in (("a.txt", 9), ("b.txt", 7), ("c.txt", 5), ("d.txt", 3), ("e.txt", 1)):
            self.file(name, lines)
        result = run("--top", "3", self.folder)
        self.assertEqual(result.stdout,
                         b" 9  a.txt\n 7  b.txt\n 5  c.txt\n25  total (all 5 files)\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac2_tie_at_the_cut_line(self):
        # The criterion's own fixture: the tie is broken by filename, so c.md is the one dropped.
        self.file("big.txt", 9)
        for name in ("a.md", "b.md", "c.md"):
            self.file(name, 5)
        result = run("--top", "3", self.folder)
        self.assertEqual(result.stdout,
                         b" 9  big.txt\n 5  a.md\n 5  b.md\n24  total (all 4 files)\n")
        self.assertNotIn(b"c.md", result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_ac3_total_counts_every_file_and_says_so(self):
        # 27 files summing to 1204 lines, as the criterion describes.
        for index in range(26):
            self.file(f"f{index:02d}.txt", 45)
        self.file("last.txt", 34)
        result = run("--top", "2", self.folder)
        self.assertEqual(result.stdout.splitlines()[-1], b"1204  total (all 27 files)")
        self.assertEqual(len(result.stdout.splitlines()), 3)
        self.assertEqual(result.returncode, 0)

    def test_ac4_without_the_flag_output_is_unchanged(self):
        self.file("notes.md", 128)
        self.file("a.py", 7)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"128  notes.md\n  7  a.py\n135  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac5_n_larger_than_the_folder(self):
        for name, lines in (("a.txt", 5), ("b.txt", 3), ("c.txt", 1)):
            self.file(name, lines)
        result = run("--top", "99", self.folder)
        self.assertEqual(result.stdout,
                         b"5  a.txt\n3  b.txt\n1  c.txt\n9  total (all 3 files)\n")
        self.assertEqual(result.returncode, 0)

    def test_ac6_top_zero_prints_only_the_total(self):
        self.file("a.txt", 5)
        self.file("b.txt", 3)
        result = run("--top", "0", self.folder)
        self.assertEqual(result.stdout, b"8  total (all 2 files)\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac7_negative_n(self):
        self.file("a.txt", 5)
        result = run("--top", "-1", self.folder)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(b"--top", result.stderr)
        self.assertEqual(result.returncode, 2)

    def test_ac7_non_numeric_n(self):
        self.file("a.txt", 5)
        result = run("--top", "abc", self.folder)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(b"--top", result.stderr)
        self.assertEqual(result.returncode, 2)

    def test_ac8_flag_position_is_free(self):
        self.file("a.txt", 5)
        self.file("b.txt", 3)
        before = run("--top", "1", self.folder)
        after = run(self.folder, "--top", "1")
        self.assertEqual(before.stdout, after.stdout)
        self.assertEqual(before.stderr, after.stderr)
        self.assertEqual(before.returncode, after.returncode)
        self.assertEqual(after.stdout, b"5  a.txt\n8  total (all 2 files)\n")

    def test_ac8_no_short_form(self):
        self.file("a.txt", 5)
        result = run("-t", "3", self.folder)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr.strip())
        self.assertEqual(result.returncode, 2)

    def test_ac9_empty_folder_whatever_n_is(self):
        for value in ("0", "3", "99"):
            with self.subTest(top=value):
                result = run("--top", value, self.folder)
                self.assertEqual(result.stdout, b"no files\n")
                self.assertEqual(result.stderr, b"")
                self.assertEqual(result.returncode, 0)

    def test_ac10_column_width_includes_the_total(self):
        # 27 files summing to 1204: the total is wider than any row shown, and the rows are
        # padded to its width so the column lines up.
        for index in range(26):
            self.file(f"f{index:02d}.txt", 46)
        self.file("small.txt", 8)
        result = run("--top", "2", self.folder)
        lines = result.stdout.splitlines()
        self.assertEqual(lines[0], b"  46  f00.txt")
        self.assertEqual(lines[1], b"  46  f01.txt")
        self.assertEqual(lines[2], b"1204  total (all 27 files)")
        self.assertEqual(result.returncode, 0)

    def test_ac10_two_largest_are_nine_and_seven(self):
        # The other half of AC10's example — 27 files whose two largest hold 9 and 7 lines. Its
        # stated total of 1204 cannot coexist with that (27 files of at most 9 lines reach 243),
        # so the two halves are checked separately; see questions/Q-001.md.
        self.file("big.txt", 9)
        self.file("next.txt", 7)
        for index in range(25):
            self.file(f"f{index:02d}.txt", 1)
        result = run("--top", "2", self.folder)
        self.assertEqual(result.stdout,
                         b" 9  big.txt\n 7  next.txt\n41  total (all 27 files)\n")
        self.assertEqual(result.returncode, 0)


class UnresolvableEntryTest(unittest.TestCase):
    """BUG-0001 — an entry that cannot be resolved must not abort the listing (ADR-0006).

    `DirEntry.is_file()` swallows only `FileNotFoundError`, so before the fix a symlink loop or a
    link into an untraversable directory escaped into the folder's error path: empty stdout, the
    folder blamed on stderr, exit 2.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def file(self, name, lines):
        return write(self.folder, name, b"x\n" * lines)

    def test_ac1_symlink_loop_does_not_abort_the_listing(self):
        self.file("ok.txt", 3)
        # q -> p -> q: following either leg raises ELOOP rather than FileNotFoundError.
        os.symlink("p", os.path.join(self.folder, "q"))
        os.symlink("q", os.path.join(self.folder, "p"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"3  ok.txt\n3  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac2_self_referential_symlink(self):
        self.file("ok.txt", 3)
        os.symlink("self", os.path.join(self.folder, "self"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"3  ok.txt\n3  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac3_symlink_into_an_untraversable_directory(self):
        vault = os.path.join(self.folder, "vault")
        os.mkdir(vault)
        write(vault, "hidden.txt", b"secret\n")
        target = os.path.join(vault, "hidden.txt")
        os.chmod(vault, 0o000)
        self.addCleanup(os.chmod, vault, 0o755)
        os.symlink(target, os.path.join(self.folder, "into-vault"))
        self.file("ok.txt", 2)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"2  ok.txt\n2  total\n")
        self.assertEqual(result.stderr, b"")  # ADR-0006 chose silence; AC3 pins the rest
        self.assertNotIn(self.folder.encode(), result.stderr)  # the folder is never blamed
        self.assertEqual(result.returncode, 0)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac5_an_unreadable_folder_still_exits_2(self):
        # The fix must not swallow the folder's own error: that one is still AC11's.
        unreadable = os.path.join(self.folder, "noread")
        os.mkdir(unreadable)
        os.chmod(unreadable, 0o000)
        self.addCleanup(os.chmod, unreadable, 0o700)
        result = run(unreadable)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertIn(unreadable.encode(), result.stderr)
        self.assertEqual(result.returncode, 2)


class AllFilesSkippedTest(unittest.TestCase):
    """BUG-0002 — stdout must not say `no files` about a folder that is full of them.

    ADR-0002 skips a file it cannot read and reports it on stderr; WI-0001 AC10 prints `no files`
    for a folder that has none. Before the fix, a folder whose files were *all* skipped took the
    second rule's branch and stdout — the stream a pipe keeps — gave the wrong answer.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def unreadable(self, name, lines):
        path = write(self.folder, name, b"x\n" * lines)
        os.chmod(path, 0o000)
        self.addCleanup(os.chmod, path, 0o600)
        return path

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac1_all_unreadable_does_not_claim_no_files(self):
        self.unreadable("one.txt", 1)
        self.unreadable("two.txt", 2)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files could be read\n")
        self.assertNotIn(b"no files\n", result.stdout)
        self.assertEqual(len(result.stderr.splitlines()), 2)  # ADR-0002's lines, unchanged
        for line in result.stderr.splitlines():
            self.assertIn(b"Permission denied", line)
        self.assertEqual(result.returncode, 0)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac2_stdout_differs_from_an_empty_folder(self):
        self.unreadable("one.txt", 1)
        self.unreadable("two.txt", 2)
        with tempfile.TemporaryDirectory() as empty:
            skipped, nothing = run(self.folder), run(empty)
            self.assertNotEqual(skipped.stdout, nothing.stdout)
            self.assertEqual(nothing.stdout, b"no files\n")
            self.assertEqual(skipped.returncode, 0)
            self.assertEqual(nothing.returncode, 0)

    @unittest.skipIf(IS_ROOT, NOT_AS_ROOT)
    def test_ac3_untraversable_folder(self):
        # Readable but not traversable: the names list, the files cannot be opened.
        write(self.folder, "f.txt", b"a\nb\n")
        write(self.folder, "g.txt", b"c\n")
        os.chmod(self.folder, 0o444)
        self.addCleanup(os.chmod, self.folder, 0o755)
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files could be read\n")
        self.assertEqual(len(result.stderr.splitlines()), 2)
        self.assertEqual(result.returncode, 0)

    def test_ac4_empty_and_subdirectory_only_folders_are_unchanged(self):
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)
        os.mkdir(os.path.join(self.folder, "sub"))
        result = run(self.folder)
        self.assertEqual(result.stdout, b"no files\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_the_renderer_still_defaults_to_no_files(self):
        # ADR-0007 put the sentence in the caller's hands without changing the default.
        self.assertEqual(linecount.format_report([]), "no files\n")
        self.assertEqual(linecount.format_report([], empty="no files could be read"),
                         "no files could be read\n")


@unittest.skipUnless(os.name == "posix", "a name that is not valid UTF-8 needs a POSIX filesystem")
class UndecodableNameTest(unittest.TestCase):
    """BUG-0003 — a filename that is not valid UTF-8 must not abort the report.

    `os.scandir` hands such a name back with surrogate escapes, and the single `print` that wrote
    the whole report could not encode them: `UnicodeEncodeError`, empty stdout, exit 1 — even for
    the ordinary files beside it. The report is now written as bytes (ADR-0008).
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)
        # Built with bytes paths: the name cannot be expressed as valid UTF-8 text.
        with open(os.path.join(os.fsencode(self.folder), b"bad\xff.txt"), "wb") as handle:
            handle.write(b"a\nb\nc\n")
        with open(os.path.join(os.fsencode(self.folder), b"good.txt"), "wb") as handle:
            handle.write(b"a\nb\n")

    def test_ac1_undecodable_name_does_not_abort_the_report(self):
        result = run(self.folder)
        self.assertEqual(result.stdout, b"3  bad\xff.txt\n2  good.txt\n5  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)
        for marker in (b"Traceback", b"UnicodeEncodeError"):
            self.assertNotIn(marker, result.stdout)
            self.assertNotIn(marker, result.stderr)

    def test_ac2_the_row_follows_the_same_rules(self):
        # count 3, first in WI-0001 AC2's order, two spaces before the name.
        first = run(self.folder).stdout.splitlines()[0]
        self.assertEqual(first, b"3  bad\xff.txt")

    def test_ac3_two_runs_are_byte_identical(self):
        first, second = run(self.folder), run(self.folder)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stderr, second.stderr)
        self.assertEqual(first.returncode, second.returncode)

    def test_ac4_top_one_on_that_folder(self):
        result = run("--top", "1", self.folder)
        self.assertEqual(result.stdout, b"3  bad\xff.txt\n5  total (all 2 files)\n")
        self.assertEqual(result.returncode, 0)

    def test_ac5_ascii_folders_are_byte_identical(self):
        # WI-0001 AC1's own example, through the new bytes path.
        with tempfile.TemporaryDirectory() as ascii_folder:
            write(ascii_folder, "notes.md", b"x\n" * 128)
            write(ascii_folder, "a.py", b"x\n" * 7)
            result = run(ascii_folder)
            self.assertEqual(result.stdout, b"128  notes.md\n  7  a.py\n135  total\n")
            self.assertEqual(result.stderr, b"")
            self.assertEqual(result.returncode, 0)


def row_names(stdout):
    """The filename column of a report, in order, without the total row.

    `lstrip` first: the count column is right-aligned, so a narrow count in a wide column starts
    the line with the same two spaces that separate the columns.
    """
    lines = stdout.splitlines()
    return [line.lstrip().split(b"  ", 1)[1] for line in lines[:-1]]


class ParseSortTest(unittest.TestCase):
    """WI-0003 AC7 at the validator: `--sort`'s value is judged in our own code (ADR-0004)."""

    def test_parse_sort_accepts(self):
        self.assertEqual(linecount.parse_sort("name"), "name")
        self.assertEqual(linecount.parse_sort("count"), "count")

    def test_parse_sort_rejects(self):
        for value in ("size", "Name", "COUNT", "", "1", "names"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    linecount.parse_sort(value)


class SortRowsTest(unittest.TestCase):
    """WI-0003 AC1 at the sorter, where the order is arithmetic rather than I/O."""

    ROWS = [(2, "Zebra.md"), (7, "apple.md"), (5, "notes.md")]

    def test_count_order_is_what_wi_0001_fixed(self):
        self.assertEqual(linecount.sort_rows(self.ROWS, "count"),
                         [(7, "apple.md"), (5, "notes.md"), (2, "Zebra.md")])

    def test_count_order_breaks_ties_by_name(self):
        rows = [(5, "b.md"), (9, "big.txt"), (5, "a.md")]
        self.assertEqual(linecount.sort_rows(rows, "count"),
                         [(9, "big.txt"), (5, "a.md"), (5, "b.md")])

    def test_name_order_is_byte_order(self):
        # Uppercase before lowercase, because bytes: 'Z' is 0x5a and 'a' is 0x61.
        self.assertEqual(linecount.sort_rows(self.ROWS, "name"),
                         [(2, "Zebra.md"), (7, "apple.md"), (5, "notes.md")])

    def test_name_order_survives_a_name_that_is_not_utf_8(self):
        # The name as `os.scandir` would hand it over. Comparing `os.fsencode`d names keeps this
        # defined; comparing `str` would order by surrogates instead (ADR-0008).
        odd = os.fsdecode(b"bad\xff.txt")
        rows = [(1, odd), (2, "bad.txt")]
        self.assertEqual(linecount.sort_rows(rows, "name"), [(2, "bad.txt"), (1, odd)])

    def test_sort_rows_does_not_mutate_its_input(self):
        rows = list(self.ROWS)
        linecount.sort_rows(rows, "name")
        self.assertEqual(rows, self.ROWS)


class SortTest(unittest.TestCase):
    """WI-0003 end to end: the script run as a user would run it, with `--sort`."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = self.tmp.name
        self.addCleanup(self.tmp.cleanup)

    def file(self, name, lines, folder=None):
        return write(folder or self.folder, name, b"x\n" * lines)

    def ac1_folder(self):
        """The folder AC1 names: Zebra.md 2 lines, apple.md 7, notes.md 5."""
        self.file("Zebra.md", 2)
        self.file("apple.md", 7)
        self.file("notes.md", 5)

    def test_ac1_name_order(self):
        self.ac1_folder()
        result = run("--sort", "name", self.folder)
        self.assertEqual(result.stdout,
                         b" 2  Zebra.md\n 7  apple.md\n 5  notes.md\n14  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac2_two_folders_line_up(self):
        # The human's own measure: same names, different contents, same order in both outputs.
        self.file("notes.md", 3)
        self.file("todo.md", 1)
        self.file("ideas.md", 2)
        with tempfile.TemporaryDirectory() as other:
            self.file("notes.md", 40, folder=other)
            self.file("todo.md", 12, folder=other)
            self.file("ideas.md", 7, folder=other)
            first = run("--sort", "name", self.folder)
            second = run("--sort", "name", other)
        expected = [b"ideas.md", b"notes.md", b"todo.md"]
        self.assertEqual(row_names(first.stdout), expected)
        self.assertEqual(row_names(second.stdout), expected)
        # The counts really do differ, so the shared order is not a coincidence of equal files.
        self.assertNotEqual(first.stdout, second.stdout)
        self.assertEqual((first.returncode, second.returncode), (0, 0))

    def test_ac3_count_is_byte_identical_to_no_flag(self):
        self.ac1_folder()
        spelled = run("--sort", "count", self.folder)
        implied = run(self.folder)
        self.assertEqual(spelled.stdout, implied.stdout)
        self.assertEqual(spelled.stderr, implied.stderr)
        self.assertEqual(spelled.returncode, implied.returncode)

    def test_ac4_default_output_is_still_the_count_order(self):
        self.ac1_folder()
        result = run(self.folder)
        self.assertEqual(result.stdout,
                         b" 7  apple.md\n 5  notes.md\n 2  Zebra.md\n14  total\n")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)

    def test_ac5_no_short_form(self):
        self.ac1_folder()
        result = run("-s", "name", self.folder)
        self.assertEqual(result.stdout, b"")
        self.assertNotEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 2)

    def test_ac6_empty_folder_whatever_the_order(self):
        for order in ("name", "count"):
            with self.subTest(order=order):
                result = run("--sort", order, self.folder)
                self.assertEqual(result.stdout, b"no files\n")
                self.assertEqual(result.stderr, b"")
                self.assertEqual(result.returncode, 0)

    def test_ac7_bad_value_is_one_line(self):
        self.ac1_folder()
        result = run("--sort", "size", self.folder)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertTrue(result.stderr.startswith(b"linecount: --sort: "), result.stderr)
        self.assertEqual(result.returncode, 2)

    def test_ac7_missing_value_is_argparse_s(self):
        self.ac1_folder()
        # `--sort` last: argparse has no value to take. `--sort <folder>`: the folder is taken as
        # the value, and the positional is then missing. Both are usage errors, and ours is not
        # involved in either.
        for args in ((self.folder, "--sort"), ("--sort", self.folder)):
            with self.subTest(args=args):
                result = run(*args)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"usage:", result.stderr)
                self.assertEqual(result.returncode, 2)

    def test_ac8_spellings_agree(self):
        self.ac1_folder()
        runs = [run("--sort", "name", self.folder),
                run(self.folder, "--sort", "name"),
                run("--sort=name", self.folder)]
        for other in runs[1:]:
            self.assertEqual(other.stdout, runs[0].stdout)
            self.assertEqual(other.stderr, runs[0].stderr)
            self.assertEqual(other.returncode, runs[0].returncode)

    def test_ac9_top_and_sort_together_keep_their_shape(self):
        # Deliberately says nothing about *which* files are selected: WI-0003 left that open and
        # ADR-0009 records why. Shape only — and a traceback here would be a defect.
        self.ac1_folder()
        result = run("--top", "2", "--sort", "name", self.folder)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, b"")
        lines = result.stdout.splitlines()
        self.assertLessEqual(len(lines) - 1, 2)
        self.assertTrue(lines[-1].endswith(b"total (all 3 files)"), lines[-1])


if __name__ == "__main__":
    unittest.main()
