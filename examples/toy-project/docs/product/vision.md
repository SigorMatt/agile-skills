---
title: linecount vision
version: 3
status: current
updated: 2026-08-17T00:20:02Z
updated-by: answer-questions
updated-for: WI-0003
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

Two flags exist, and both narrow or re-angle that same answer rather than adding a second job:

- **`--top N`** (delivered, WI-0002) shows only the N largest files. The total row still counts
  every file in the folder and says so, because "how much is in this folder" is the question
  being answered and the number must not shrink when fewer rows are asked for.
- **`--sort name` / `--sort count`** (delivered, WI-0003) chooses the row order. `count` is the default and needs no flag. `name` orders the
  rows by filename instead, which answers a second question the author actually has: run over
  two folders that are meant to hold the same notes, a count-ordered listing shuffles
  differently in each, and a name-ordered one lines up so the two can be compared by eye.

Two properties matter as much as the counting itself:

- **No flags for the common case.** The flags above are for narrowing and for comparing; the
  question the tool exists for is answered with nothing but a folder path. If the obvious output
  needs several arguments, the tool has failed on its own terms.
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
| 3 | 2026-08-17T00:20:02Z | answer-questions | WI-0003 | `--sort` recorded as delivered rather than "being added … not delivered at the time of writing". The bullet's description of what the flag does is unchanged — it was written from the refined criteria and matches what shipped. Answering `WI-0003/Q-001`, filed by `review-close` because merging the branch made v2's wording stale and D7/DE4 test for exactly that, and `doc-header.md` §5 does not permit `review-close` to edit this document |
| 2 | 2026-08-16T23:50:12Z | intake | EP-001 | Recorded the two flags: `--top N` as delivered, and `--sort name` / `--sort count` as being added for WI-0003 and not yet delivered. Named the second question the tool now answers — comparing two folders that should hold the same files — and restated "no flags for the common case" so it survives the flags existing. Asked for by the human when EP-001 was reopened: "I'd rather the vision described what the tool actually does … nobody ever added `--top` to that vision either, so put that in too" |
| 1 | 2026-08-16T21:13:44Z | intake | EP-001 | First version, from the intake conversation for EP-001 |
