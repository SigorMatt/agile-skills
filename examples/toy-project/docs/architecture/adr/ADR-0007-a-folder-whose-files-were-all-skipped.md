---
title: A folder whose files were all skipped says so on stdout
version: 1
status: current
updated: 2026-08-17T01:34:00Z
updated-by: plan
updated-for: BUG-0002
---

# ADR-0007 — A folder whose files were all skipped says so on stdout

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for BUG-0002
- **Supersedes:** —

## Context

Two rules that are each correct combine into a false answer. ADR-0002 skips a file that cannot be
read, reports it on **stderr**, and keeps the exit status 0. WI-0001 AC10 prints exactly
`no files` when a folder contains none. When *every* file in a folder is skipped, `rows` is empty,
`main` takes its `not rows` branch, and stdout — the stream the tool exists to produce, and the
only one a pipe or a redirect keeps — says `no files` about a folder that is full of them.

Reproduced on `main` before planning:

```
$ python3 linecount.py /tmp/bug2a 2>/dev/null   # two files, both chmod 000
no files
$ python3 linecount.py /tmp/bug2c 2>/dev/null   # a genuinely empty folder
no files
```

Byte-identical stdout for two folders that differ in the only thing the tool is asked about.

ADR-0005 predicted this exact failure when it chose `format_report`'s `None` sentinel: "Deciding
that a folder held no files is the **caller's** job… If a third caller ever forgets, it prints `no
files` for a folder that had some — the one way this design can be misused." `main` is that
caller, and it never distinguished "there were none" from "I could not read any".

BUG-0002 leaves the replacement wording to `plan`, as WI-0001 AC11 and AC12 leave the wording of
their stderr messages open, and pins three things: stdout must not claim there are no files, the
per-file stderr lines and the exit status of ADR-0002 are unchanged, and a genuinely empty folder
still prints exactly `no files`.

A neighbouring case must **not** change, and it is what keeps this ADR narrow: after ADR-0006, an
entry the tool cannot *resolve* is not a file as far as the tool knows, so a folder of nothing but
symlink loops correctly still prints `no files`. This decision is about entries that **are** files
and could not be **read**.

## Options considered

- **A — print nothing on stdout, exit 0.** Cost: stdout does differ from the control folder, so it
  satisfies AC2 literally, but silence is not an answer — a reader who redirected stderr sees an
  empty file and cannot tell it from a crash. Risk: it makes the tool's most-used stream say
  nothing in a case where it has something to say.
- **B — print a total row of zero**, e.g. `0  total`. Cost: it claims a total over no rows, and a
  folder of two unreadable files then reads as a folder of zero lines. Risk: quietly wrong
  numbers, which is worse than the bug being fixed.
- **C — print a distinct sentence**, `no files could be read`. Cost: one more string in the
  vocabulary of a tool whose whole output is rows plus `no files`. Risk: low; it is unmistakably
  different from `no files`, it is true, and it points the reader at the stderr lines that name
  each file.
- **D — count the skipped files in the sentence**, e.g. `no files could be read (2 skipped)`. Cost:
  a number on stdout that duplicates what stderr already itemises, and a format that would then
  need its own criterion. Risk: it invites a second question — why is *this* count on stdout when
  the file names are not?

## Decision

**Option C.** When a folder yields no countable rows, stdout depends on why:

| the folder held | stdout | exit |
|-----------------|--------|------|
| no files at all (empty, or only subdirectories, or only entries that cannot be resolved) | `no files` | 0 |
| files, but every one of them failed to read | `no files could be read` | 0 |

`main` makes the distinction, because only `main` knows how many files it skipped;
`format_report` renders whichever sentence it is handed, through a new optional parameter
`empty="no files"`. That keeps every byte of the report produced in one function — the property
ADR-0005 chose optional parameters to preserve — while leaving the judgement with the caller, as
that ADR requires.

The per-file stderr lines are untouched, the exit status stays 0, and `--top` changes nothing:
with no rows to limit there is nothing for N to do, whatever it is.

## Consequences

- The two folders in the bug report now produce different stdout, which is BUG-0002 AC2 and the
  point of the fix.
- The tool's stdout vocabulary grows by one sentence, to three shapes: rows plus a total,
  `no files`, and `no files could be read`. A parser of this output — which nothing in the record
  asks for — would need to know all three.
- A folder holding *both* unreadable files and unresolvable entries prints `no files could be
  read`, because at least one entry was a file. That is the honest half of the answer; the
  unresolvable entries remain silent under ADR-0006.
- **Reversibility: cheap.** One counter in `main`, one branch, one default parameter. Changing the
  wording is one string. Moving to option A is deleting the branch; moving to option D is adding
  the count to the same string. None of it touches `count_lines`, `list_files`, the row format,
  the total, or `--top`.
- **What this does not fix, deliberately:** the `--top` label counts the files that were *listed*,
  so a folder of two files where one is skipped still reads `total (all 1 files)`. BUG-0002's own
  notes raise that as an observation about WI-0002 AC3's two definitions of M, not as a defect,
  and this decision changes neither definition.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-17T01:34:00Z | plan | BUG-0002 | First version |
