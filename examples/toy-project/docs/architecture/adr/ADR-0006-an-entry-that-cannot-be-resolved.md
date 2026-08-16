---
title: An entry whose type cannot be determined is not a file, and is ignored silently
version: 1
status: current
updated: 2026-08-17T01:50:00Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0006 — An entry whose type cannot be determined is not a file, and is ignored silently

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

`list_files` decides what to list with `entry.is_file(follow_symlinks=True)`. That call resolves
the entry, and `DirEntry.is_file()` swallows exactly one error — `FileNotFoundError` — returning
`False`. Every other `OSError` escapes. Confirmed at the interpreter, on the folder BUG-0001
describes:

```
ok.txt is_file -> True
q raises OSError 40 Too many levels of symbolic links
p raises OSError 40 Too many levels of symbolic links
```

`main` wraps the whole of `list_files` in one `except OSError` that reports the failure as the
*folder's* and returns 2 — the AC11 path. So a single unresolvable entry destroys the report for
every readable file beside it, and the message names a folder that is perfectly readable.

The tool therefore has two `OSError` sources that mean different things and are currently caught
by one handler:

1. **`os.scandir(folder)` fails, or iteration over it fails.** The folder cannot be listed. That
   is WI-0001 AC11: nothing on stdout, one line on stderr naming the path, exit 2.
2. **`entry.is_file()` fails for one entry.** The folder is fine; one thing in it cannot be
   resolved. Nothing in the record decided what this should do, because WI-0001 AC7 only named
   symlinks to a file, to a directory, and to nothing — and `FileNotFoundError` made the third
   work by accident.

There is also a third, already decided: **`count_lines` fails for an entry already established to
be a file** — ADR-0002, which skips it, prints one line on stderr, and keeps the exit status 0.

BUG-0001's criteria constrain the answer more tightly than they may appear to. AC1 requires that a
folder holding a symlink loop print **nothing on stderr**, so "report every unresolvable entry" is
not available. AC3 leaves it open whether the untraversable-target case says anything, but pins
that it must not be fatal and must not blame the folder.

## Options considered

- **A — treat an unresolvable entry as "not a file", silently, exactly as a broken symlink is.**
  Cost: a folder can contain something the tool never mentions. Risk: low, and already accepted
  by WI-0001 AC7 for the three symlink cases it named — a broken symlink is invisible today.
- **B — treat it as "not a file" and print one line on stderr**, ADR-0002's shape. Cost: it fails
  BUG-0001 AC1, which requires an empty stderr for the symlink-loop folder. Risk: it also makes
  the tool noisy about entries the user cannot act on, which is why AC7 chose silence for the
  cases it did name.
- **C — split by `errno`**: silent for `ELOOP`, a stderr line for `EACCES`. Cost: a rule that
  cannot be stated without naming operating-system error numbers, in a tool whose entire
  behaviour is otherwise expressible in one sentence per case. Risk: it invents a distinction no
  criterion asks for and that no user could predict.
- **D — keep the current behaviour and narrow AC7 instead.** Cost: it makes the tool's own vision
  false ("being unable to read the folder at all is" the error condition — the folder here is
  readable). Not a real option; it is listed because rejecting it is what makes this a bug rather
  than a documentation fix.

## Decision

**Option A.** `list_files` resolves each entry inside `try` / `except OSError`, and an entry whose
type cannot be determined is treated as **not a file**: not listed, not counted, nothing printed
about it on either stream, and the run continues and exits 0.

The three `OSError` sites are now distinct, and the rule that separates them is what the listing
step knows:

| where it fails | what it means | behaviour |
|----------------|---------------|-----------|
| `os.scandir(folder)`, or iterating it | the folder cannot be listed | AC11: stderr, exit 2 |
| `entry.is_file()` | one entry cannot be resolved | **this ADR**: ignored silently, exit 0 |
| `count_lines(path)` | a known file cannot be read | ADR-0002: skipped, one stderr line, exit 0 |

The middle row is silent and the bottom row speaks because of what each one knows. When
`is_file()` fails, the tool cannot even say the entry is a file — reporting it would be reporting
something it has not established. When `count_lines` fails, the entry *is* a file the user can
see, and omitting it silently would make the total quietly wrong.

## Consequences

- WI-0001 AC7's three named symlink cases are unchanged: a symlink to a file is still listed under
  its own name, and a symlink to a directory or to nothing is still ignored in silence. This
  decision extends the same treatment to the cases AC7 did not name, which is what BUG-0001 says
  it should have meant all along.
- WI-0001 AC11 is unchanged and is now reachable only by a genuine folder failure, which is what
  its own wording always said.
- A folder can hold an entry that never appears in the output or in any message. That is the
  price of AC1's empty stderr, and it is the same price WI-0001 already paid for broken symlinks.
- **Reversibility: cheap.** One `try` / `except OSError` in `list_files`. Moving to option B is
  adding a `print` to that branch — and would need BUG-0001 AC1 changed first, which is a question
  for the architect, not an edit. Moving to option C is a check on `exc.errno` in the same branch.
- The fix does not touch `count_lines`, `format_report`, `parse_top`, `parse_args`, the sort key,
  or any output format, so nothing WI-0001 or WI-0002 verified can change behaviour.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-17T01:50:00Z | plan | BUG-0001 | First version |
