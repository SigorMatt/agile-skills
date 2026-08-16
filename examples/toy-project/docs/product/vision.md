---
title: linecount vision
version: 1
status: current
updated: 2026-08-16T21:13:44Z
updated-by: intake
updated-for: EP-001
---

# linecount vision

## Who it is for

The person who has just opened a directory of mixed notes and code and does not know where the
bulk of the material is. Primarily the author, on their own machine — but not only them: the
author asked that someone who inherits one of these folders be able to run it too. That
requirement is what keeps this a file in the repository rather than a shell alias, and what
makes "no installation, standard library only" a property of the product rather than a
preference.

## What it is for

Answering one question, quickly and without configuration: **which files here are the big
ones?** Size means lines. The tool is pointed at a folder, lists the files directly inside it
with their line counts, largest first, and prints a total. The answer arrives in the first two
or three rows, which is the entire point — the existing alternative, `wc -l *`, produces the
same numbers in glob order and leaves the reader to scan for the largest, and it fails
outright when the folder contains a subdirectory.

Two properties matter as much as the counting itself:

- **No flags for the common case.** If the obvious output needs several arguments, the tool has
  failed on its own terms.
- **A number, not a stack trace.** Folders contain unusual things. Encountering one is not an
  error condition; being unable to read the folder at all is, and that is reported plainly with
  a non-zero exit so it is noticed inside a script.

## What it deliberately is not

It is not a code-analysis tool. There is no per-language breakdown, no code-versus-comment
distinction, no blank-line handling — it is not `cloc` or `tokei`, and it should not grow in
that direction. It reports lines and nothing else: no bytes, no words. It has no configuration
file, no ignore patterns, no colour, and no interactive mode. It does not know about git. It
does not recurse — the author considered recursion and deferred it deliberately, so a future
version adding it would be a change of scope, made on purpose, not a natural extension. It is
not packaged or published; it is a single script run with `python3`.

The governing phrase from the author is "nothing fancy". Every feature this document rules out
was ruled out by him at intake, not assumed.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-16T21:13:44Z | intake | EP-001 | First version, from the intake conversation for EP-001 |
