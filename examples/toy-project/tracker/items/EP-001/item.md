---
id: EP-001
type: epic
title: See at a glance which files in a folder are the big ones
status: done
priority: high
created: "2026-08-16T21:13:40Z"
updated: "2026-08-17T00:27:37Z"
outcome: delivered
---

## Goal

Someone who opens a folder of mixed notes and code can find out, in one command and with no
flags to remember, how much is in each file directly in that folder — with the biggest files
at the top so the two or three that matter are visible immediately. The measure of "how much"
is lines. The command works on any folder the person can read, including folders that contain
subdirectories or files that are not text, and when it cannot do its job it says so plainly and
exits non-zero instead of producing a stack trace.

## Why now

The tools already on the machine do not answer this question well. `wc -l *` prints the counts
in whatever order the shell globbed them, so the reader has to scan every row to find the
largest, and it fails outright when the folder contains a subdirectory. The cost of not fixing
this is small but constant: it is paid every time a folder of notes or code is opened, and the
workaround (piping `wc` through `sort`) is long enough that it is retyped or misremembered each
time. The human also wants someone who inherits one of these folders to be able to run this,
which rules out a shell alias living only in their own dotfiles.

## Success measures

- Running the tool on a folder of a few dozen mixed files, passing nothing but the folder path,
  prints the file with the most lines as the first row of output.
- On a folder that contains at least one subdirectory, the command exits 0 and prints counts
  for the files, where `wc -l *` on the same folder reports an error for the subdirectory.
- The first three rows of output are enough to name the three largest files, without reading
  the rest of the output, and the output can be piped into `head` without garbling.
- A folder containing a file that is not text produces a complete listing and exits 0 — no
  traceback appears in the output.
- Pointing the tool at a path that does not exist, or one the user cannot read, prints a
  message naming that problem and exits with a non-zero status.
- A person who is handed the folder and has only Python 3 installed can run the tool, and run
  its tests, without installing anything first.
- Run over two folders that are meant to hold the same set of notes, the tool can be asked for
  an order that does not depend on the line counts, so the two listings name the files in the
  same order and can be compared row for row by eye. (Added when EP-001 was reopened for
  WI-0003; the human's own measure, verbatim in this epic's second intake entry.)

## Scope

- A single Python 3 file at the top of the repository, run as `python3 linecount.py <folder>`,
  using only the standard library.
- Counting lines of each file directly inside the given folder; subdirectories inside it are
  ignored rather than counted or reported as errors.
- Output of one row per file — the count and the filename — ordered largest first, with a total
  at the bottom, as plain text suitable for piping.
- Behaving predictably on the awkward cases the human named: an empty file, a final line with
  text but no trailing newline, a file that is not text, a folder that cannot be read.
- Tests written with the test framework that ships with Python, so no installation is needed to
  run them.
- A later, separate addition of a `--top N` option that limits the output to the N largest
  files.
- A later, separate addition of a `--sort` option that switches the row order between the
  default largest-first and filename order, changing the order of the rows and nothing else.
  (Added when EP-001 was reopened for WI-0003.)

## Out of scope

- Recursing into subdirectories. The human considered it and deferred it explicitly: "Recursion
  might be nice later but I don't want it now."
- Any measure of size other than lines — no bytes, no words, no character counts.
- Distinguishing code from comments or blank lines, and any per-language breakdown. This is not
  `cloc` or `tokei`.
- Ignore patterns, configuration files, and any awareness of git or of which files are tracked.
- Colour, progress indicators, interactive browsing, or anything resembling a TUI.
- Watching a folder for changes, or any long-running mode.
- Packaging, installation, publishing, or a console-script entry point; the file is run
  directly with `python3`.
- Any third-party dependency, for running the tool or for running its tests.
