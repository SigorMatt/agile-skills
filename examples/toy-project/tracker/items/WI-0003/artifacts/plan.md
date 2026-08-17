# Plan — WI-0003 Add --sort to order the rows by filename instead of by count

Written by `plan` v0.1.1 (architect) on 2026-08-17T00:05:00Z.

## Problem

`linecount` prints one row per file ordered by count descending, filename ascending as the
tie-break, and that order is hard-coded in a single `rows.sort(...)` call in `main`. The human
wants a second order — by filename — because he keeps two folders that should hold the same notes
and a count-ordered listing shuffles them differently, so the two outputs cannot be compared. This
item adds `--sort name` / `--sort count` (`count` being what happens today, and the default) and
changes **nothing else**: not the row format, not the column arithmetic, not which files are
listed, not the total row, not an exit code. The constraints that shape the design are AC3 and AC4
(spelling out the default, or omitting the flag, must be byte-identical to today's output), AC7
(a bad *value* fails in one line, a missing value stays argparse's), and AC9 (the `--top`
combination must not crash, while deliberately not fixing which files it selects).

## Approach

Add one pure function that owns the order, and one validator that owns the flag's value. Both fit
the existing shape in `docs/architecture/overview.md` v4 — a pipeline of pure-ish steps behind a
thin `main` — and neither touches the two functions where the criteria are arithmetic
(`count_lines`, `format_report`), so the whole existing suite stays valid unmodified.

`parse_sort(value)` mirrors `parse_top(value)` exactly, for the reason ADR-0004 gives: the value
is validated in our own code so the message is one line, while every other usage error stays
argparse's. `sort_rows(rows, order)` returns the rows in the requested order and is the only place
in the tool that knows what either order is — today `main` holds that knowledge inline, and after
this change it holds none of it.

The `--top` slice (`rows[:top]`) is **not touched**. See `## Decisions and ADRs` and ADR-0009: the
item deliberately does not fix which files `--top N --sort name` selects, so the design spends no
code making that come out one way rather than the other.

## Steps

1. **Add `parse_sort(value)` to `linecount.py`**, directly after `parse_top`. It returns `value`
   when it is exactly `"name"` or `"count"`, and otherwise raises
   `ValueError(f"{value!r} is not 'name' or 'count'")` — the same contract as `parse_top`: the
   exception text is the reason, ready to print after `linecount: --sort: `. Afterwards the module
   has two validators of the same shape, and neither knows how to print.

2. **Declare the flag in `parse_args`**: `parser.add_argument("--sort", metavar="KEY",
   default="count", help="order the rows: count (default) or name")`. No `type=` and **no
   `choices=`** — `choices=` would make argparse reject a bad value with a usage block plus a
   message, which is two lines and fails AC7 (ADR-0004, option A). `default="count"` means
   `args.sort` is always a string, so `main` has no `None` case to branch on and AC3 falls out
   rather than being special-cased. Afterwards `--help` and the usage line carry
   `[--sort KEY]`, which is the change AC4 excepts in its own text.

3. **Add `sort_rows(rows, order)` to `linecount.py`**, after `list_files`. It returns a new list:
   for `"name"`, `sorted(rows, key=lambda row: os.fsencode(row[1]))`; otherwise
   `sorted(rows, key=lambda row: (-row[0], os.fsencode(row[1])))` — the existing key, moved, not
   rewritten. Both keys compare names as `os.fsencode`d bytes, which is what makes the order
   independent of the locale and defined for a name that is not valid UTF-8 (ADR-0008). Afterwards
   the two orders are one function, and `main` names an order instead of describing one.

4. **Validate the flag in `main`**, immediately after the existing `--top` block and before
   `list_files` is called: `parse_sort(args.sort)` inside `try`, and on `ValueError` print
   `f"linecount: --sort: {exc}"` to stderr and `return 2`, printing nothing on stdout. Afterwards
   a bad value fails before any folder is read, exactly as a bad `--top` does.

5. **Replace the inline sort in `main`** — `rows.sort(key=lambda row: (-row[0],
   os.fsencode(row[1])))` — with `rows = sort_rows(rows, order)`, leaving its position in `main`
   unchanged (after the counting loop, before the `if not rows:` branch). Leave the three
   printing branches, including `rows[:top]`, exactly as they are. Afterwards `--sort count` and
   no flag at all run identical code paths, which is AC3 and AC4.

6. **Update the module docstring** in `linecount.py`: the usage line becomes
   `python3 linecount.py [--top N] [--sort name|count] <folder>`, and one sentence records that
   the order is the count order by default and the filename order on request, both comparing names
   as bytes. Do not restate the criteria there; cite `WI-0003 AC1` as the other lines cite theirs.

7. **Add tests to `tests/test_linecount.py`**, in the file's existing style — one class for this
   item, `test_ac<n>_*` names, `run(*args)` for the end-to-end layer, `linecount.<fn>` for the unit
   layer:
   - `ParseSortTest` — `parse_sort` accepts `"name"` and `"count"`; rejects `"size"`, `"Name"`,
     `""`, and a numeric string, each raising `ValueError`.
   - `SortRowsTest` — `sort_rows` on a hand-built `[(count, name), ...]` list: count order
     unchanged from today including the tie-break; name order ascending; uppercase before
     lowercase (`Zebra.md` before `apple.md`); a name that is not valid UTF-8 sorts by its bytes
     without raising.
   - `SortTest` — the end-to-end criteria: AC1's three-file folder asserted as exact stdout bytes;
     AC2's two folders compared on their filename columns; AC3 and AC8 as byte-for-byte
     comparisons of whole runs; AC5, AC6, AC7 and AC9 as stdout/stderr/exit-code assertions.
   Afterwards every criterion has a named test, per the mapping below.

8. **Run `python3 -m unittest discover` from the repository root** and require exit 0 with the
   pre-existing 60 tests unmodified. Any edit to an existing test is a signal that step 5 changed
   behaviour it should not have, and is a reason to stop, not to edit the test.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `--sort name` orders by filename, bytes ascending | 2, 3, 5 | `SortTest.test_ac1_name_order` — folder of `Zebra.md` (2), `apple.md` (7), `notes.md` (5); asserts stdout equals the three rows in that order plus the `total` row, and exit 0. Unit half: `SortRowsTest.test_name_order_is_byte_order` |
| AC2 — two folders with the same names list in the same order | 3, 5 | `SortTest.test_ac2_two_folders_line_up` — builds `A` and `B` with `notes.md`, `todo.md`, `ideas.md` and different contents; asserts the filename column of both runs is `[ideas.md, notes.md, todo.md]` and the counts differ |
| AC3 — `--sort count` is byte-identical to no flag | 2, 5 | `SortTest.test_ac3_count_is_the_default` — runs both on one mixed folder; asserts equal stdout, stderr and returncode |
| AC4 — no `--sort` is byte-identical to today, usage text excepted | 5 | The 60 pre-existing tests passing unmodified (step 8), plus `SortTest.test_ac4_default_output_is_the_count_order` asserting the exact expected bytes on the AC1 folder without any flag |
| AC5 — no short form `-s` | 2 | `SortTest.test_ac5_no_short_form` — `run("-s", "name", folder)`: stdout empty, stderr non-empty, exit 2 (argparse's, unchanged) |
| AC6 — empty folder unchanged under either value | 5 | `SortTest.test_ac6_empty_folder` — `--sort name` and `--sort count` on an empty folder: stdout exactly `no files\n`, stderr empty, exit 0 |
| AC7 — bad value is one line; missing value is argparse's | 1, 4 | `SortTest.test_ac7_bad_value` — `--sort size`: stdout empty, stderr one line starting `linecount: --sort: `, exit 2. `SortTest.test_ac7_missing_value` — `run("--sort")` and `run("--sort", folder)`: stdout empty, stderr non-empty, exit 2. Unit half: `ParseSortTest` |
| AC8 — three spellings agree byte for byte | 2 | `SortTest.test_ac8_spellings_agree` — `--sort name <folder>`, `<folder> --sort name`, `--sort=name <folder>`: equal stdout, stderr and returncode pairwise |
| AC9 — `--top N --sort name` keeps its shape | 5 (by not changing it) | `SortTest.test_ac9_top_and_sort_together` — folder of at least three files: exit 0, at most two file rows, last line matches `total (all 3 files)`. Asserts nothing about *which* files, by design (ADR-0009) |
| AC10 — the suite passes and covers the new behaviour | 7, 8 | `python3 -m unittest discover` from the repository root exits 0, and the classes named above exist in `tests/test_linecount.py` |

## Assumptions

Each is reversible in the sense `plan`'s preference order requires — one file, no interface a
caller depends on, no data to migrate.

1. **`--sort` values are case-sensitive**, so `--sort Name` is rejected by AC7's path. Nobody was
   asked. AC7 says a value that is neither `name` nor `count` is rejected, and `Name` is neither,
   so this satisfies the criterion rather than stretching it. *Reversing it:* add `.lower()` to
   `parse_sort`'s comparison — one line, one function, no test outside `ParseSortTest` affected.
2. **When both `--top` and `--sort` are invalid, the `--top` message is the one printed**, because
   its block already stands first in `main` and step 4 adds the new one after it. No criterion
   covers the case. *Reversing it:* swap two adjacent blocks in `main`.
3. **The rejection text is `'size' is not 'name' or 'count'`.** AC7 pins the stream, the exit
   code, the one-line shape and the `linecount: --sort: ` prefix, not the words after it.
   *Reversing it:* one f-string in `parse_sort`.
4. **`sort_rows` returns a new list rather than sorting in place**, unlike the `rows.sort(...)` it
   replaces. It makes the function unit-testable without a fixture and keeps it pure, at the cost
   of one list copy on a list that is at most one folder long. *Reversing it:* sort in place and
   return `None`, changing one line in `main`.

## Decisions and ADRs

| decision | where it comes from |
|----------|--------------------|
| Validate `--sort`'s value in our own code, not with argparse `choices=` | **Answered from the documents.** ADR-0004 decided exactly this question for `--top`, and its reasoning transfers without amendment: `choices=` prints a usage block plus a message, which is two lines, and AC7 asks for one. No new ADR — a second ADR restating the first would devalue the trail. The human independently re-confirmed the same shape at refinement (Q3) |
| Names are compared as `os.fsencode`d bytes in both orders | **Answered from the documents.** ADR-0008 already made the report byte-oriented so an undecodable name cannot abort it; comparing names as bytes is the same choice applied to the ordering, and AC1 states it as a criterion |
| The `--top N --sort name` selection is left unspecified, and the slice is not touched | **ADR-0009** (new). The human was asked, refused to decide, and refused to have an assumption recorded in his name; AC9 constrains the shape of that output and nothing else |
| Every other usage error stays argparse's (`-s`, a missing value, no folder) | **Answered from the documents.** ADR-0001 gave the command line to argparse; ADR-0004 fixed the boundary between our messages and its. AC5 and AC7's second half are that boundary, unchanged |
| `commands.test` / `commands.lint` in `project.yaml` | Unchanged. `test` is already `python3 -m unittest discover`, which this plan runs at step 8; `lint` stays `null` because ADR-0003 records that no linter ships with CPython and the project may not depend on one. The `lint-clean` gate is therefore honestly `skipped`, not passed |

## Risks

- **The usage and help text changes, and AC4 is a byte-identity criterion.** `--help` and the
  usage block argparse prints on a usage error will gain `[--sort KEY]`. AC4 excepts this in its
  own words, and the exception is safe to rely on because no test in the 60 asserts either string
  — checked with `grep -n "usage\|--help" tests/test_linecount.py`, no matches. If a future test
  does assert them, this risk returns and AC4's exception is where to look.
- **`sort_rows` is called before the `if not rows:` branch**, as the inline sort was. On an empty
  list both orders are no-ops, so BUG-0002's `no files could be read` path and WI-0001's
  `no files` path cannot be affected by step 5. If step 5 is instead placed after that branch, the
  `--sort name` order silently stops applying to the normal path — the one rearrangement of this
  plan that would pass a casual reading and fail AC1.
- **`--top` with `--sort name` will do something, and this plan does not say it is right.** With
  the slice untouched it selects the alphabetically-first N. That is a consequence of not writing
  code, not a decision; AC9 is written to pass either way, and ADR-0009 records what would have to
  change if the human wants the other reading. Nothing downstream may cite the observed behaviour
  as settled.
- **A one-file folder and the `(all 1 files)` label** are untouched by this item, and WI-0002's
  known-gap list already carries that. Not a risk of this plan; named so a reader does not think
  it appeared here.

## Out of scope for this item

- Deciding which files `--top N --sort name` selects (ADR-0009, and the item's `## Out of scope`).
- Any sort key other than `name` and `count`; any descending name order; case-insensitive or
  locale-aware collation.
- Changing the default order, the row format, the column width, the total row, the empty-folder
  answer, or any exit code.
- Refactoring `format_report`, `count_lines` or `list_files`. Their signatures are fixed by
  ADR-0005 and by the tests that assert their arithmetic directly.
- Recursion, and every other exclusion inherited from EP-001.
