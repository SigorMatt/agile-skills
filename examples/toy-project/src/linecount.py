#!/usr/bin/env python3
"""List the files directly inside a folder with their line counts, largest first.

Usage: python3 linecount.py [--top N] <folder>

A line is a newline byte, plus one for a final line that has text but no newline after it, so
every file is counted by the same rule and none of them is decoded (WI-0001 AC5, AC9). Names are
bytes too: the report is written to `sys.stdout.buffer` as `os.fsencode`d bytes, so a name that is
not valid UTF-8 prints as `ls -b` prints it (ADR-0008).
Subdirectories, symlinks to directories and broken symlinks are ignored (AC6, AC7); dotfiles
are not (AC8). stdout carries the report and nothing else, so it stays pipeable; anything that
went wrong goes to stderr. Exit 0 means there is an answer, exit 2 means there is not (AC11,
AC12, ADR-0001).

Standard library only, and run directly rather than installed: a person handed one of these
folders must be able to run it with nothing but Python 3.
"""

from __future__ import annotations

import argparse
import os
import sys

CHUNK = 1 << 20


def count_lines(path):
    """The number of lines in the file at `path`, by WI-0001 AC5's byte rule.

    Newline bytes, plus one if the file is not empty and does not end in a newline. The file is
    read as bytes and never decoded, so a PNG counts like anything else. Raises OSError, which
    the caller decides what to do about (ADR-0002).
    """
    lines = 0
    last = b""
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                break
            lines += chunk.count(b"\n")
            last = chunk[-1:]
    if last and last != b"\n":
        lines += 1
    return lines


def list_files(folder):
    """The names of the entries of `folder` that are files, symlinks followed.

    `is_file(follow_symlinks=True)` is false for a directory, for a symlink to a directory and
    for a broken symlink, which is AC6 and all three cases of AC7 from one predicate. No name is
    filtered, which is AC8.

    An entry that cannot be *resolved* — a symlink loop, a link whose target sits in a directory
    we may not traverse — is treated as not a file and ignored in silence, exactly as a broken
    symlink is (BUG-0001, ADR-0006). `DirEntry.is_file` swallows only `FileNotFoundError`, so
    without this every other `OSError` escaped into the caller's folder handler and one bad
    symlink aborted the whole report.

    An `OSError` from `os.scandir` itself still propagates: that one is the folder's failure,
    which is AC11 and AC12's territory and exits 2.
    """
    names = []
    with os.scandir(folder) as entries:
        for entry in entries:
            try:
                resolved = entry.is_file(follow_symlinks=True)
            except OSError:
                resolved = False
            if resolved:
                names.append(entry.name)
    return names


def format_report(rows, total=None, label="total", empty="no files"):
    """The exact text to print for `rows`, a list of (count, name) already in final order.

    The count is right-aligned in a column as wide as the widest number printed — the total
    included — then two spaces, then the bare name (WI-0001 AC1). The total row comes last, and
    carries `label` (WI-0002 AC3).

    `total` defaults to the sum of `rows`, which is the whole story when every file is shown.
    A caller that shows only some of them passes the total it means, and it may be larger than
    anything above it — the column is sized to whichever number is widest (WI-0002 AC10). Rows
    may then be empty while the total is not: that prints the total row alone (WI-0002 AC6).

    With no rows *and* no explicit total there is nothing to report, and the answer is `empty` —
    `no files` by default (WI-0001 AC10), or whatever the caller passes when the folder did hold
    files and none of them could be read (BUG-0002, ADR-0007). Deciding *why* there are no rows is
    the **caller's** job, not this function's: it only knows what it was handed (ADR-0005).
    """
    if not rows and total is None:
        return f"{empty}\n"
    if total is None:
        total = sum(count for count, _ in rows)
    width = max(len(str(number)) for number in [count for count, _ in rows] + [total])
    lines = [f"{count:>{width}}  {name}" for count, name in rows]
    lines.append(f"{total:>{width}}  {label}")
    return "".join(line + "\n" for line in lines)


def parse_top(value):
    """The non-negative whole number `value` means, for `--top`.

    Raises ValueError whose message is the reason, ready to print after `linecount: --top: `.
    The value is validated here rather than by argparse's `type=`, because WI-0002 AC7 wants a
    single line on stderr and argparse writes a usage block above its message (ADR-0004).
    """
    try:
        number = int(value)
    except ValueError:
        raise ValueError(f"{value!r} is not a whole number") from None
    if number < 0:
        raise ValueError(f"{number} is negative")
    return number


def parse_args(argv):
    """Parse `argv` into the folder to report on and the raw `--top` value.

    argparse handles every usage error it owns: a message on stderr and exit 2, which is the
    failure shape AC11 and AC12 require (ADR-0001). `--top` carries no `type=`, so its value
    arrives as a string for `parse_top` to judge; an unknown option such as `-t` is still
    argparse's to reject (WI-0002 AC8).
    """
    parser = argparse.ArgumentParser(
        prog="linecount",
        description="List the files in a folder with their line counts, largest first.")
    parser.add_argument("folder", help="the folder to report on")
    parser.add_argument("--top", metavar="N", help="show only the N largest files")
    return parser.parse_args(argv)


def main(argv):
    """Run the tool. Returns the exit status: 0 with a report, 2 with nothing on stdout."""
    args = parse_args(argv)

    top = None
    if args.top is not None:
        try:
            top = parse_top(args.top)
        except ValueError as exc:
            print(f"linecount: --top: {exc}", file=sys.stderr)
            return 2

    try:
        names = list_files(args.folder)
    except OSError as exc:
        print(f"linecount: {args.folder}: {exc.strerror or exc}", file=sys.stderr)
        return 2

    rows, unreadable = [], 0
    for name in names:
        try:
            rows.append((count_lines(os.path.join(args.folder, name)), name))
        except OSError as exc:
            # The folder is readable but this one file is not. Say so, leave it out, carry on
            # with the rest of the folder — ADR-0002. The count is what lets stdout tell "the
            # folder held no files" apart from "I could not read any of them" — ADR-0007.
            unreadable += 1
            print(f"linecount: {name}: {exc.strerror or exc}", file=sys.stderr)

    rows.sort(key=lambda row: (-row[0], os.fsencode(row[1])))

    if not rows:
        # `no files` means the folder held none — empty, or only subdirectories, or only entries
        # that could not be resolved (ADR-0006). If it held files and every one of them failed to
        # read, stdout says that instead (ADR-0007). `--top` has nothing to limit either way, so
        # WI-0002 AC9 holds for any N.
        text = format_report(rows, empty="no files could be read") if unreadable \
            else format_report(rows)
    elif top is None:
        # Unchanged from WI-0001 (WI-0002 AC4).
        text = format_report(rows)
    else:
        # The rows shown are the first N of the order above; the total is still every file in
        # the folder, and says so (WI-0002 AC1, AC3, AC6).
        text = format_report(rows[:top], sum(count for count, _ in rows),
                             f"total (all {len(rows)} files)")
    # The report is data, not text: a file's name is echoed as the bytes the filesystem gave us,
    # so a name that is not valid UTF-8 prints as `ls -b` and `wc` print it, and the output does
    # not depend on the locale (BUG-0003, ADR-0008).
    sys.stdout.buffer.write(os.fsencode(text))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
