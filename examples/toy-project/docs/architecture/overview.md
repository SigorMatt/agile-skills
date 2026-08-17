---
title: linecount architecture overview
version: 5
status: current
updated: 2026-08-17T00:05:00Z
updated-by: plan
updated-for: WI-0003
---

# linecount architecture overview

## Shape of the system

One executable Python 3 file at the repository root, plus a test package beside it:

```
linecount.py            # the whole tool: argument parsing, listing, counting, formatting
tests/
├── __init__.py         # makes tests/ a package so `unittest discover` finds it on any 3.x
└── test_linecount.py   # unittest tests, standard library only
```

There is no package, no entry point, no configuration file and no dependency manifest. The tool
is run as `python3 linecount.py <folder>` and its tests as `python3 -m unittest discover` from
the repository root. That is a product requirement, not an implementation convenience: a person
who inherits one of these folders must be able to run both with nothing but Python 3 installed
(`docs/product/vision.md` v1).

## Internal structure of `linecount.py`

The file is a pipeline of pure-ish steps behind a thin `main`, so each step is testable on its
own and the failure behaviour lives in exactly one place:

| Function | Responsibility |
|----------|----------------|
| `parse_args(argv)` | turn `argv` into the folder path and the raw `--top` and `--sort` values; usage errors exit 2 (ADR-0001) |
| `parse_top(value)` | the non-negative integer `--top` means, or a `ValueError` carrying the message to print (ADR-0004) |
| `parse_sort(value)` | the order `--sort` names — `name` or `count` — or a `ValueError` carrying the message to print. Same contract as `parse_top`, for the same reason (ADR-0004) |
| `list_files(folder)` | the entries in `folder` that are files, symlinks followed |
| `sort_rows(rows, order)` | `[(count, name), ...]` in the order to print: count descending then name ascending, or name ascending. The only place either order is defined (WI-0003) |
| `count_lines(path)` | the line count of one file, by the byte rule the item fixes |
| `format_report(rows, total=None, label="total")` | the text to print, given `[(count, name), ...]`; the caller may override the total and its label, which is how `--top` shows a total larger than the rows above it (ADR-0005) |
| `main(argv)` | wires them together, decides how many rows to show, prints, and returns the exit status |

Only `main` knows what `--top` is. `format_report` renders whatever rows and total it is handed —
which is what keeps the row format, the column width and the total row in one place for both the
plain and the limited output. In the same way, only `sort_rows` knows what an *order* is: `main`
names one and prints what comes back, so "count descending, then name ascending" appears exactly
once in the tool rather than once per call site.

The split matters for one reason beyond taste: `count_lines` and `format_report` are the two
places where the acceptance criteria are literally arithmetic (the newline rule, the column
width), and keeping them free of I/O and of argument handling is what lets a test assert them
without a directory on disk.

## Boundaries that are deliberate

- **Nothing recurses.** `list_files` looks only at the entries directly inside the folder, and
  a directory — real or reached through a symlink — is not an entry it returns. Recursion was
  deferred by the author on purpose, so adding it later is a change of scope, not a natural
  extension.
- **Bytes, not text — on the way in and on the way out.** Files are opened in binary and never
  decoded, so no file can raise a decoding error and every file gets a count by the same rule
  (`tests/`, WI-0001 AC5/AC9). A file's *name* is data too: the report is assembled as `str` and
  written to `sys.stdout.buffer` as `os.fsencode`d bytes, so a name that is not valid UTF-8 reaches
  stdout as the bytes the filesystem gave us — what `ls -b` and `wc` write — and the output does
  not depend on `LANG`/`LC_ALL` (BUG-0003, ADR-0008). stdout is therefore written exactly once, at
  the end of `main`; anything that `print`s to stdout would interleave with it.
- **Ordering is a byte comparison too.** Both orders compare names as `os.fsencode`d bytes, so the
  sort is defined for a name that is not valid UTF-8 and does not depend on `LANG`/`LC_ALL` — the
  same choice as the output side, applied to the ordering (ADR-0008, WI-0003 AC1).
- **One input combination is deliberately unspecified.** `--top N --sort name` has no criterion
  fixing *which* files it selects: the author was asked and chose to leave it open, so the design
  adds no code to decide it and the `rows[:top]` slice is untouched (ADR-0009). Its *shape* is
  pinned — exit 0, at most N rows, the labelled total (WI-0003 AC9) — so the undefined region is
  bounded. Whatever the code does there today is incidental and is not a contract.
- **stdout carries the answer, stderr carries the trouble.** The report goes to stdout and
  nothing else ever does, so stdout stays pipeable into `head`. Every message about a problem
  goes to stderr. Exit 0 means "here is the answer"; exit 2 means "I could not produce one".
- **Three `OSError` sites, three meanings.** Exit 2 is reserved for the folder. The tool fails
  differently depending on what it has established when the error arrives, and conflating the
  three is what BUG-0001 was:

  | where it fails | what it means | behaviour |
  |----------------|---------------|-----------|
  | `os.scandir(folder)`, or iterating it | the folder cannot be listed | one line on stderr, exit **2** (WI-0001 AC11) |
  | `entry.is_file()` | one entry cannot be resolved — a symlink loop, an unstattable target | ignored in silence, exit 0 (ADR-0006) |
  | `count_lines(path)` | a known file cannot be read | skipped, one line on stderr, exit 0 (ADR-0002) |

  The middle row is silent and the bottom row speaks because of what each knows: a failed
  `is_file()` has not established that the entry is a file at all, while a failed `count_lines`
  is about a file the user can see.

## Verification shape

Tests are `unittest` and live in `tests/`. They come in two layers:

- **unit** — `count_lines` and `format_report` called directly, for the counting rule and the
  column arithmetic;
- **end-to-end** — the script run as a subprocess with `sys.executable`, asserting exact
  stdout, stderr and exit code. Every acceptance criterion that names an exit code or a stream
  is checked at this layer, because that is the only layer where those things exist.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 5 | 2026-08-17T00:05:00Z | plan | WI-0003 | Added `parse_sort` and `sort_rows` to the function table and made ordering a named step rather than an inline call in `main`; recorded that both orders compare names as bytes, and that the `--top`/`--sort` combination is deliberately unspecified in content and bounded in shape (ADR-0009) |
| 4 | 2026-08-17T01:36:00Z | plan | BUG-0003 | Extended the bytes-not-text boundary to file names: the report is written to stdout as bytes, after BUG-0003 showed a name that is not valid UTF-8 aborting the whole report |
| 3 | 2026-08-17T01:50:00Z | plan | BUG-0001 | Recorded the three `OSError` sites and which exit status each produces, after BUG-0001 showed two of them being caught by one handler |
| 2 | 2026-08-17T00:05:00Z | plan | WI-0002 | Added `parse_top` and the optional `total`/`label` parameters of `format_report` to the function table, and said which function knows about `--top` |
| 1 | 2026-08-16T21:33:10Z | plan | WI-0001 | First version: the single-file layout, the function split inside `linecount.py`, and the two-layer test shape |
