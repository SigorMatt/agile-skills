# Plan — WI-0001 Count lines per file in a folder and print them largest first

## Problem

`python3 linecount.py <folder>` must print one row per file directly inside `<folder>` — the
line count right-aligned in a column as wide as the widest number printed, two spaces, the bare
filename — ordered by count descending then filename ascending in byte order, with a `total` row
last. It is for someone who has just opened a folder of mixed notes and code and wants the two
or three biggest files named in the first rows. The constraints are the product's: one file at
the repository root, Python 3 standard library only for both the tool and its tests, nothing to
install, stdout pipeable into `head`, and no traceback ever — awkward folder contents are
normal, and only a folder it cannot read at all is a failure (exit 2, message on stderr).

This is the first code in the repository. There is nothing to fit into: at planning time the
repository contains `README.md` (one line, the title), `docs/`, `tracker/` and `.claude/`, and
no Python file at all.

## Approach

One executable file, `linecount.py`, holding five functions with narrow responsibilities, plus a
`tests/` package beside it. The shape and the reasons are recorded in
`docs/architecture/overview.md` v1; the two decisions it does not make itself are ADR-0001
(argparse) and ADR-0002 (a file that cannot be read).

The counting rule (AC5) and the column arithmetic (AC1) are the two places where the criteria
are literally arithmetic, so they live in functions that touch neither `argv` nor the terminal —
`count_lines` and `format_report` — and are tested directly. Everything that has an exit status
or a stream lives in `main`, and is tested by running the script as a subprocess.

Files are opened in binary and never decoded. That single choice is what makes AC5 and AC9 the
same rule rather than two: no file can raise a decoding error, so no file needs a special case.

## Steps

1. **Add `.gitignore` at the repository root** containing `__pycache__/` and `*.pyc`. Running
   `python3 -m unittest discover` imports `tests` and `linecount` and writes bytecode
   directories; without this they show up as untracked files and land in commits. Observable
   result: after running the test command in a clean checkout, `git status --porcelain` is
   empty.

2. **Create `linecount.py`** at the repository root, executable as `python3 linecount.py
   <folder>`, importing only `argparse`, `os` and `sys`. Define, in this order:

   1. `count_lines(path)` → `int`. Opens `path` with `open(path, "rb")`, reads it in chunks of
      `1 << 20` bytes, and returns the number of `b"\n"` bytes plus one if the file is not empty
      and its last byte is not `b"\n"`. Never decodes. Lets `OSError` propagate to the caller —
      it does not catch it. Observable result: `count_lines` of a file holding `a\nb\n` is 2, of
      `a\nb` is 2, of `\n` is 1, of an empty file is 0, and a file larger than the chunk size
      counts the same as if it had been read whole.
   2. `list_files(folder)` → `list[str]`. Returns the *names* (not paths) of the entries of
      `folder` for which `entry.is_file(follow_symlinks=True)` is true, in whatever order
      `os.scandir` yields them — ordering is step 2.4's job. Following symlinks in that one call
      is what gives AC7 all three of its cases at once: a symlink to a file is a file, a symlink
      to a directory is not, and a broken symlink is not. No name is filtered, which is AC8.
      Lets `OSError` from `os.scandir` propagate: a missing path, a path that is a regular file
      and an unreadable directory each raise a subclass of it.
   3. `format_report(rows)` → `str`. `rows` is a list of `(count, name)` already in final order.
      With no rows it returns `"no files\n"`. Otherwise `total = sum(count for count, _ in
      rows)`, `width = max(len(str(n)) for n in [count for count, _ in rows] + [total])`, and it
      returns one line per row of `f"{count:>{width}}  {name}"` followed by
      `f"{total:>{width}}  total"`, each line terminated by `\n`. Observable result:
      `format_report([(128, "notes.md"), (7, "a.py")])` is exactly
      `"128  notes.md\n  7  a.py\n135  total\n"`.
   4. `parse_args(argv)` → the parsed namespace, using
      `argparse.ArgumentParser(prog="linecount")` with a single positional argument `folder`
      (ADR-0001). Argparse handles the no-argument case itself: message on stderr, exit 2.
   5. `main(argv)` → `int`. Calls `parse_args`; calls `list_files` inside `try/except OSError`,
      and on failure prints exactly `linecount: {folder}: {exc.strerror or exc}` to stderr,
      prints nothing to stdout and returns **2**; otherwise builds `rows` by calling
      `count_lines` per name, and on `OSError` for one name prints exactly
      `linecount: {name}: {exc.strerror or exc}` to stderr, skips that file and continues
      (ADR-0002); sorts with `rows.sort(key=lambda row: (-row[0], os.fsencode(row[1])))`;
      writes `format_report(rows)` to stdout with `end=""`; returns **0**.

   End with `if __name__ == "__main__": sys.exit(main(sys.argv[1:]))`.

   `os.fsencode` rather than plain string comparison is what makes AC2's "byte order" true for
   a non-ASCII filename as well as for `A.md` before `a.md`.

3. **Create `tests/__init__.py` (empty) and `tests/test_linecount.py`.** `__init__.py` makes
   `tests` a package, so `python3 -m unittest discover` finds it without depending on
   namespace-package discovery. `test_linecount.py` imports `linecount` directly for the unit
   layer, and for the end-to-end layer runs `subprocess.run([sys.executable, SCRIPT, folder],
   capture_output=True)` where `SCRIPT` is derived from `__file__`, not from the working
   directory. Each test builds its folder in a fresh `tempfile.TemporaryDirectory()`. The tests
   required, one per criterion, are named in the mapping table below. Observable result:
   `python3 -m unittest discover` from the repository root exits 0.

4. **Run the gates and record the evidence.** `python3 -m unittest discover` from the repository
   root exits 0 (`commands.test`); `lint-clean` is reported **skipped**, with ADR-0003 as the
   reason. Then write `artifacts/impl-report.md` mapping each AC to the test that exercises it.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — row format, column width, bare name | 2.3, 2.5 | `test_ac1_exact_output_for_two_files`: folder with `notes.md` (128 lines) and `a.py` (7 lines); asserts stdout is exactly `"128  notes.md\n  7  a.py\n135  total\n"`. Plus `test_ac1_format_report_unit` calling `format_report` directly |
| AC2 — order, tie-break, byte-identical reruns | 2.5 | `test_ac2_ties_break_on_filename_byte_order`: `A.md` and `a.md` both 3 lines → `A.md` first. `test_ac2_two_runs_are_byte_identical`: the same folder run twice, `stdout1 == stdout2` |
| AC3 — total row last, same column | 2.3 | `test_ac3_total_is_last_row_and_is_the_sum`: last stdout line equals `f"{sum:>{width}}  total"` for a folder of three files |
| AC4 — zero-byte file listed as 0 | 2.1, 2.3 | `test_ac4_empty_file_is_listed_as_zero`: folder with `empty.txt` (0 bytes) and one non-empty file; a row `0  empty.txt` is present, in sorted position |
| AC5 — the newline rule | 2.1 | `test_ac5_counting_rule`: `count_lines` over files holding `a\nb\n` → 2, `a\nb` → 2, `\n` → 1, `` → 0; `test_ac5_rule_holds_across_chunk_boundary`: a file of 3 MiB of `x\n` counts its lines exactly |
| AC6 — a subdirectory is ignored, silently, exit 0 | 2.2 | `test_ac6_subdirectory_is_ignored`: folder with `sub/` and one file; stdout names only the file and the total, stderr is empty, exit 0 |
| AC7 — symlink to file listed under its own name; to a directory, and broken, ignored | 2.2 | `test_ac7_symlink_to_file_is_listed`, `test_ac7_symlink_to_dir_is_ignored`, `test_ac7_broken_symlink_is_ignored`: each asserts stdout, empty stderr and exit 0 |
| AC8 — dotfiles listed | 2.2 | `test_ac8_dotfile_is_listed`: folder with `.gitignore` (2 lines) and `a.txt`; `.gitignore` has a row |
| AC9 — a non-text file gets a row, no traceback | 2.1, 2.5 | `test_ac9_binary_file_is_counted_like_any_other`: folder with a real PNG byte string and two text files; stdout has 4 lines (3 files + total), stderr is empty, exit 0, and `"Traceback"` is in neither stream |
| AC10 — no files at all → `no files`, no total, exit 0 | 2.3 | `test_ac10_empty_folder` and `test_ac10_folder_with_only_subdirectories`: stdout is exactly `"no files\n"`, stderr empty, exit 0 |
| AC11 — missing path, and unreadable folder → stderr, exit 2 | 2.5 | `test_ac11_missing_path`: stdout empty, exactly one line on stderr containing the path, exit 2. `test_ac11_unreadable_folder`: a directory `chmod 0o000`, same assertions, decorated `@unittest.skipIf(os.geteuid() == 0, ...)` because root can read it anyway (the criterion says "tested as a non-root user") |
| AC12 — path is a regular file, and no argument at all → stderr, exit 2 | 2.4, 2.5 | `test_ac12_path_is_a_regular_file` and `test_ac12_no_argument`: stdout empty, stderr non-empty, exit 2 |
| AC13 — `python3 -m unittest discover` from the root exits 0, nothing installed | 1, 3 | The command itself, run from the repository root with its output recorded in `impl-report.md`; `tests/__init__.py` and `tests/test_linecount.py` are what it discovers, and `linecount.py` imports only `argparse`, `os`, `sys` |

Two behaviours below are in the plan but map to no AC, and are here deliberately rather than by
oversight: the `.gitignore` of step 1 (a hygiene consequence of AC13's test command, with no
observable behaviour of its own) and the skip-and-report branch of ADR-0002, which is a case no
criterion rules on but the code must nonetheless handle. ADR-0002's branch gets one test,
`test_unreadable_file_is_reported_and_skipped` (also skipped when running as root), so that a
decision recorded in an ADR is not left unexercised.

## Assumptions

1. **`tests/` is a package.** `__init__.py` is added so discovery does not depend on
   namespace-package behaviour, which has varied across Python 3 releases. Reversing it: delete
   the file and re-run the test command on the target interpreter. One file, no interface.
2. **A 1 MiB read chunk.** Any chunk size gives the same counts; this one bounds memory for a
   large file without being an interesting number. Reversing it: change one constant.
3. **The stderr wording** `linecount: <name>: <strerror>` is the analyst's, not the human's —
   AC11 and the item's `## Notes` deliberately leave wording open and constrain only the stream,
   the exit code, and that the message names the path and the problem. Reversing it: one f-string
   in `main`; the tests assert the stream, the exit code and that the path appears, not the
   sentence.
4. **A folder whose every file fails to read prints `no files`** — `rows` is empty, so
   `format_report` takes its no-rows branch, and the stderr lines from ADR-0002 are the only
   record. No criterion covers this combination (AC10 is about a folder that *contains* no
   files). Reversing it: a separate branch in `main`. Left as it is because the alternative is a
   message no criterion asks for.

## Decisions and ADRs

| decision | where recorded | branch of the preference order |
|----------|----------------|-------------------------------|
| argparse parses the command line; usage errors exit 2 on stderr | ADR-0001 | decided here, with the alternative costed |
| a file that cannot be read is skipped, reported on stderr, exit stays 0 | ADR-0002 | decided here — no document rules on it, and the code must do something |
| `commands.lint` and `commands.build` stay null; `commands.test` is `python3 -m unittest discover` | ADR-0003, `tracker/project.yaml` | documented — AC13 fixes the test command; the product constraint against installing anything fixes the other two |
| single file at the root, stdlib only, run as `python3 linecount.py <folder>` | `docs/product/vision.md` v1, EP-001 scope, WI-0001 `## Notes` | documented — stated by the human at intake, not decided here |
| bytes not text; one counting rule for every file | WI-0001 AC5/AC9, refinement Q3 | documented — the human chose it when the alternative was put to him |
| tie-break on filename, byte order | WI-0001 AC2, refinement Q1 | documented |
| the shape of `linecount.py` and the two test layers | `docs/architecture/overview.md` v1 | decided here; no alternative worth an ADR for one file of this size |
| `tests/` is a package; 1 MiB chunk; stderr wording; all-files-unreadable prints `no files` | `## Assumptions` above | assumed, each with its reversal cost |

## Risks

- **Discovery layout.** If `python3 -m unittest discover` does not pick up `tests/` as laid out
  in step 3, AC13 fails on a technicality unrelated to the tool. The mitigation is that step 4
  runs the exact command from the exact directory the criterion names, before the item leaves
  `implement`; a failure there is visible immediately rather than at review.
- **`os.scandir` error mapping.** AC11 and AC12 assume a missing path, a regular file and an
  unreadable directory all surface as `OSError` from `os.scandir`. That holds on POSIX; if any
  of the three raised something else, `main` would traceback instead of exiting 2 — which is the
  failure the criteria most want to prevent. The three end-to-end tests are what catch it, and
  they are not optional.
- **The criteria assume POSIX.** AC7 uses symlinks and AC11 a mode-`000` directory. On a
  platform without them these tests cannot run, and the root case is already handled with a
  skip. The tool is being built and run on Linux; nothing in the item asks for portability
  beyond that.
- **Determinism across filesystems (AC2).** `os.scandir` order is arbitrary, so byte-identical
  reruns rest entirely on the sort. If the sort key were partial — two files with the same count
  *and* the same name is impossible, so it is total — reruns could differ. Named here because
  "it passed twice on my machine" is not evidence that the order is defined.
- **Scale.** Everything is held in memory and sorted in one pass. Refinement fixed the folder
  size at a few dozen files, occasionally a couple of hundred, never thousands, so this is
  correct at the sizes the item claims and would be wrong at a million files.

## Out of scope for this item

- `--top N`. It is WI-0002, whose criteria are already `ready`. Nothing in this plan may
  anticipate it: `format_report` takes rows and computes the total from them, and if WI-0002
  needs a different total it will change that signature under its own criteria.
- Recursion into subdirectories, any measure other than lines, ignore patterns, colour,
  packaging, and every other exclusion in EP-001's `## Out of scope`.
- Handling `BrokenPipeError` when stdout is closed early by `head`. At the folder sizes this
  item claims, the whole report fits in a pipe buffer, so the case is not reachable in practice
  and no criterion mentions it. If it is ever observed, it is a bug item.
- A `-t` short form, and any behaviour of a flag that does not exist yet.
