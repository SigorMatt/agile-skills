# Plan — WI-0001 Align markdown table columns, passing all other content through unchanged

## Problem

Someone who edits markdown by hand wants one command that takes a document on standard input and
returns it with every pipe table's columns padded to a uniform width, and everything else
byte-identical. The constraints are all recorded and none of them is negotiable here: a single
Python 3 script with no dependency and no build step [src: ADR-0001]; recognition strictly
limited to outer-piped pipe tables outside a fenced code block, optionally under a uniform
whitespace indent [src: ADR-0003]; widths measured in display columns rather than characters, one
space either side of every cell, a delimiter row that fills its column [src: ADR-0003]; alignment
markers preserved but not acted on [src: ADR-0004]. There is no existing code in this repository
— this item creates the whole tool — so the design question is not how to fit in, but how to
split the work so that each of the eleven criteria is demonstrated by something a stranger can
run.

## Approach

One module, `mdtab.py`, at the repository root, structured as four layers that can each be tested
on their own. Nothing below is an implementation; the signatures and the rules they must satisfy
are the design, and the bodies are the developer's.

**1. Edges — bytes in, bytes out.**

- `main(argv=None) -> int` — reads `sys.stdin.buffer`, writes `sys.stdout.buffer`, returns 0.
  Takes no arguments; if any are given, they are ignored rather than rejected (there is no
  interface to reject them with, and the tool has no options [src: WI-0001]).
- Decode and encode with `"utf-8"` and `errors="surrogateescape"`, so that bytes which are not
  valid UTF-8 round-trip unchanged.
- `split_lines(text: str) -> list[str]` — splits on `\r\n`, `\n` and `\r` only, **keeping each
  line's terminator on the line**. Not `str.splitlines`, which also splits on `\v`, `\f` and
  `\u2028` and would silently break a line the rest of the pipeline treats as one.
  `"".join(split_lines(t)) == t` for every `t`, which is the property the passthrough promise
  rests on.

**2. Measurement.**

- `display_width(text: str) -> int` — 2 for a character whose `unicodedata.east_asian_width` is
  `"W"` or `"F"`, 0 for one whose `unicodedata.combining` is non-zero or whose category is `Mn`
  or `Me`, 1 otherwise [src: ADR-0003]. Pure, total, and testable on its own against a table of
  known cases — which matters, because it is the one function the tests must agree with the code
  about.

**3. Recognition.** A single left-to-right scan over the lines, holding two pieces of state: the
open fence (its character and run length, or `None`), and the candidate block being collected.

- `fence_delta(line: str, open_fence) -> new_open_fence` — a line whose text, after leading
  whitespace is stripped, begins with three or more backticks or three or more tildes opens a
  fence with that character and that run length; while a fence is open, a line whose stripped
  text is only that character repeated at least that many times closes it. Lines inside a fence,
  and the two fence lines themselves, are copied.
- `candidate_parts(line: str) -> tuple[str, str] | None` — returns `(prefix, body)` when the
  line, with its terminator and trailing spaces and tabs removed, has a leading run of spaces
  and tabs followed by a `body` that starts with `|` and ends with an **unescaped** `|` and is at
  least two characters long. Otherwise `None`. A `>` is not whitespace, so a blockquoted table is
  not a candidate [src: ADR-0003].
- A **candidate block** is a maximal run of consecutive candidate lines with byte-identical
  `prefix`. A line that is not a candidate, or whose prefix differs, ends the block — and, if it
  is itself a candidate, starts the next one. That re-consideration is the part most likely to be
  missed.

**4. Validation, measurement and composition.**

- `split_cells(body: str) -> list[str]` — splits `body` on `|` characters that are not preceded
  by an odd number of backslashes, discards the first and last fields (which the outer pipes
  make empty), and strips spaces and tabs from each remaining field. `\|` stays in the cell text
  exactly as written: the tool aligns the source a person reads, not the rendered table
  [src: EP-001/Q-003].
- `is_delimiter_cell(cell: str) -> bool` — matches `^:?-+:?$`.
- `table_or_none(block) -> Table | None` — a block of two or more rows is a table when its second
  row is entirely delimiter cells and every row has the same cell count, which is at least one.
  Anything else returns `None` and the block is copied whole [src: ADR-0003].
- `column_widths(header, body_rows, markers) -> list[int]` — for each column, the maximum
  `display_width` over the header and body cells only, never the delimiter row; then raised to a
  minimum of 1 for a column whose delimiter cell carries two colons [src: ADR-0004].
- `compose_row(cells, widths, prefix) -> str` — `prefix + "|" + "|".join(" " + cell + " " *
  (w - display_width(cell)) + " ")+ "|"`. An empty cell in a zero-width column is two spaces.
- `compose_delimiter(markers, widths, prefix) -> str` — for each column, the leading colon if the
  input cell had one, then hyphens, then the trailing colon if it had one, occupying exactly
  `width + 2` characters with no spaces [src: ADR-0004].
- Every composed line is emitted with **the line terminator of the input line it replaces**, and
  a table's rows map one-to-one onto the input's, so nothing has to be invented for the last line
  of a file that ends without a newline.

## Steps

1. **Create `mdtab.py`** with a shebang, a module docstring naming ADR-0003 and ADR-0004 as the
   rules it implements, `main()`, and the `if __name__ == "__main__": sys.exit(main())` tail.
   Make it executable. Afterwards: `printf 'hello\n' | python3 mdtab.py` prints `hello` and exits
   0, and `./mdtab.py </dev/null` prints nothing and exits 0.
2. **Add `split_lines()` and the byte edges** to `mdtab.py`, so that `main` is
   decode → `split_lines` → (identity, for now) → join → encode. Afterwards: any file, including
   one with CRLF endings, one with no final newline, and one containing the byte `0x80`, comes
   back byte-identical under `cmp`.
3. **Add `display_width()`** to `mdtab.py`. Afterwards: it returns 2 for `"中"` and `"🙂"`, 0 for
   `"́"`, 1 for `"a"`, and 4 for `"a中é"`.
4. **Add `fence_delta()` and the copy-through scan** to `mdtab.py`: the scan now classifies each
   line as inside or outside a fence and copies everything. Afterwards: a document with a
   ```` ``` ```` block and a `~~~` block, each full of pipe lines, is byte-identical after the
   filter.
5. **Add `candidate_parts()` and block collection** to `mdtab.py`, still copying every block.
   Afterwards: blocks are being grouped — provable by a temporary test that asserts a document
   with two tables separated by prose yields two blocks. Delete that test before step 9 if it
   asserts on an internal shape no criterion needs.
6. **Add `split_cells()`, `is_delimiter_cell()` and `table_or_none()`** to `mdtab.py`; a block
   that fails validation is copied byte for byte, as a whole. Afterwards: a block with a missing
   delimiter row, a block with a short row, and a two-line block whose second line is prose are
   all unchanged in the output, including the rows of them that were well formed.
7. **Add `column_widths()`, `compose_row()` and `compose_delimiter()`** and emit composed lines
   for a valid table. Afterwards: the ragged fixture comes back aligned; the indented fixture
   comes back aligned with its indent intact; a table with `:---:` keeps its colons.
8. **Create the fixtures** under `tests/fixtures/`, one input and one expected-output file per
   criterion group, written as literal documents rather than generated: `ragged`, `wide_chars`,
   `indented`, `indent_mismatch`, `blockquote`, `fenced`, `malformed`, `markers`, `crlf`,
   `no_final_newline`, `not_utf8`, `empty`, `prose_only`.
9. **Write `tests/test_mdtab.py`** (and split it if it grows past readability): one test method
   per acceptance criterion, each named for the criterion it covers — `test_ac1_...` — with the
   criterion's text as the method docstring. `tests/__init__.py` already exists.
10. **Run `python3 -m unittest discover -s tests -t .` and the lint command** from
    `tracker/project.yaml`, and record both outcomes in the implementation's journal entry.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 3, 7 | `test_ac1_display_width_rows_equal`: run the filter on `fixtures/wide_chars.md` (a ragged table containing `中`, `🙂` and `é`), assert every line of the output table has an equal `display_width`, and `cmp` the whole output against `fixtures/wide_chars.expected.md` |
| AC2 | 7 | `test_ac2_columns_start_at_same_offset`: for the same output, assert that for each column the display width of the prefix up to its opening pipe is the same on every row, delimiter row included |
| AC3 | 7 | `test_ac3_cell_padding`: `cmp` the output of `fixtures/ragged.md` against its expected file, which is written with one space either side of every cell and a two-space empty cell; plus an assertion that no output line ends in a space or a tab |
| AC4 | 7 | `test_ac4_delimiter_row`: the expected file for `fixtures/ragged.md` has `\|` + (width+2) hyphens per column; and `fixtures/wide_delimiter.md`, whose input delimiter row is longer than any content cell, comes back narrowed |
| AC5 | 5, 7 | `test_ac5_indented`: `cmp` against expected for `fixtures/indented.md` (tidied, indent byte-identical), `fixtures/indent_mismatch.md` (unchanged) and `fixtures/blockquote.md` (unchanged) |
| AC6 | 2 | `test_ac6_passthrough`: `cmp` output against input for `fixtures/prose_only.md`, `fixtures/empty.md`, `fixtures/no_final_newline.md`, `fixtures/crlf.md` and `fixtures/not_utf8.md`, the last two compared as bytes |
| AC7 | 4, 7 | `test_ac7_fences`: `fixtures/fenced.md` contains a ```` ``` ```` block and a `~~~` block of pipe lines plus one real table; assert every non-table line is byte-identical to its input line and the real table is aligned |
| AC8 | 6 | `test_ac8_malformed`: `cmp` output against input for `fixtures/malformed.md`, which holds a table with no delimiter row, one with a short body row, and one whose delimiter row has the wrong cell count |
| AC9 | 7 | `test_ac9_idempotent`: for each of the AC1 and AC5–AC8 fixtures, run the filter on its own output and `cmp` the second output against the first |
| AC10 | 1, 2 | `test_ac10_exit_status`: run the filter as a subprocess on every fixture above and assert `returncode == 0` |
| AC11 | 9, 10 | `python3 -m unittest discover -s tests -t .` exits 0 and reports one test per criterion; each method's name and docstring name the criterion it covers. The command is `commands.test` in `tracker/project.yaml`, and it exits 5 rather than 0 if no test ran |

## Assumptions

Each of these is reversible in the sense step 4 of the `plan` procedure requires: one file, no
data migration, no published interface.

- **The script is `mdtab.py` at the repository root**, executable, with a
  `#!/usr/bin/env python3` shebang, so both `python3 mdtab.py` and `./mdtab.py` work. Reversing:
  rename one file and update `commands.lint` and the tests. The stakeholder delegated this whole
  category — *"take that decision yourselves"* [src: EP-001/Q-002].
- **`unittest` from the standard library, discovered under `tests/`**, because ADR-0001 already
  named it and nothing else is installed in this environment. Reversing: change one line of
  `tracker/project.yaml` and the test file layout.
- **Lint is `python3 -m compileall`, excluding `.claude/`**, because no linter is available and
  ADR-0001 forbids installing one. It is a syntax check and nothing more, and it is recorded as
  such rather than dressed up as a style gate. Reversing: change one line of
  `tracker/project.yaml`.
- **An escaped pipe `\|` is cell content, and both characters count towards the cell's display
  width.** GitHub-flavoured markdown makes it content [src: EP-001/Q-003], and the width follows
  from the tool aligning the source text a person reads rather than the rendered output. Reversing
  the width half — counting `\|` as one column — is a change to `display_width`'s caller in one
  place, but it would make the tool's own output not line up in an editor, which is what the
  stakeholder asked for [src: WI-0001/Q-001].
- **Command-line arguments are ignored rather than rejected.** The tool has no options
  [src: WI-0001], and exiting non-zero on an unexpected argument would be an interface decision
  nobody asked for. Reversing: one branch in `main`.

## Decisions and ADRs

| decision | where it is recorded | route |
|----------|---------------------|-------|
| What counts as a table, how wide a column is, what a tidied table looks like | ADR-0003, decisions 1–11 | documented — read and cited, not re-decided |
| A delimiter row keeps its alignment markers, and a two-colon column has a minimum width of 1 | **ADR-0004, created by this execution** | decided here: the item's AC4, its `## Out of scope` and ADR-0003 decision 10 had to be read together, and the literal reading of AC4 alone would silently change how a document renders |
| Python 3, standard library only, `unittest` | ADR-0001 | documented |
| Bytes at the edges with `surrogateescape` | this plan, `## Approach` §1; the reason is in `docs/architecture/overview.md` | assumed — reversible, one function each side |
| `split_lines` rather than `str.splitlines` | this plan, `## Approach` §1 | decided here; the alternative silently breaks the passthrough promise on `\f` and `\u2028` |
| Script path, test command, lint command, argument handling, escaped-pipe width | `## Assumptions` above | assumed, each with its reversal named |

No decision in this execution reconciles two of the stakeholder's own answers. The one place two
of their sentences bear on the same rule — *"as wide as the widest cell in them"*
[src: EP-001/Q-001] against *"a rule under the header, not a row of content"*
[src: WI-0001/Q-004] — was consumed as a clarification by `answer-questions`, is recorded in
`Q-004`'s own cross-answer check, and is used here as ADR-0003 already states it.

## Scaffolding

- `tests/__init__.py` — empty. `python3 -m unittest discover -s tests -t .` raises
  `ImportError: Start directory is not importable` without it, so the command recorded in
  `tracker/project.yaml` could not otherwise be run at all. No behaviour, and deleting it makes
  no acceptance criterion fail — it makes the command that demonstrates them refuse to start.

## Risks

- **AC4 read on its own contradicts ADR-0004 and the item's own `## Out of scope`.** A verifier
  who checks the criterion's literal text against a table containing `:---:` will find the code
  disagreeing with it. ADR-0004 records why, and its fixture is `markers`. This is the single
  most likely way this item is wrongly rejected.
- **The tests must agree with the code about `display_width`.** If a test imports the function it
  is checking, AC1 becomes a tautology. The mitigation is in step 9: the `wide_chars` expected
  file is written by hand, so the comparison is against a document a person wrote, and the
  `display_width` unit test asserts specific integers rather than calling the function twice.
- **Emoji width is approximate.** `unicodedata.east_asian_width` reports `W` for most emoji but
  not all, so a fixture with an unlucky emoji could encode a width the stakeholder's terminal
  disagrees with. They accepted this in advance [src: WI-0001/Q-001]. Choose an emoji that
  `unicodedata` reports as `W`, and note the chosen code point in the test.
- **A surrogate-escaped byte has no meaningful display width** and will count as 1. That only
  matters inside a table cell in a document that is not valid UTF-8, where the alignment may be
  off; the passthrough promise is unaffected. Not covered by any criterion, and not worth one.
- **The tool will tidy a pipe table sitting inside an *indented* code block.** ADR-0003 accepts
  this deliberately; it is in the item's `## Out of scope` so that it is not filed as a bug.

## Out of scope for this item

- Positioning cell text according to alignment markers — WI-0002. This plan preserves markers and
  acts on none of them.
- Blockquoted tables, tables without outer pipes, grid and rst tables, any maximum column width,
  any argument, flag or configuration file, and any file I/O by path. All are in the item's
  `## Out of scope` and none appears in any step above.
- Reporting to the user that a table was skipped. The tool is silent by design [src: ADR-0003].
