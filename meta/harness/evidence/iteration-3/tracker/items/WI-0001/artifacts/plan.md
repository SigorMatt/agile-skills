# Plan — WI-0001 Align table columns in a stdin-to-stdout markdown filter

## Problem

mdtab does not exist yet: this repository holds a tracker, four ADRs and a vision, and no source
code at all. WI-0001 is the first item, and it asks for the whole tool minus one feature —
a Python 3 program that reads a markdown document on stdin, rewrites the spacing inside the
tables it recognises so the columns line up on screen, and writes every other byte back
unchanged. Alignment markers are read but not yet honoured; that is WI-0002.

The constraints are already decided and this plan may not re-open them: Python 3 with no
third-party runtime dependency and no install step [src: ADR-0001]; every width is a display
width in terminal columns, not a character count [src: ADR-0002]; and a run of lines is laid out
only when it passes all four recognition rules, with anything else copied through byte-for-byte
and nothing written to stderr [src: ADR-0003]. Fifteen acceptance criteria say what that means
in observable terms [src: WI-0001].

## Approach

Four stages, each handing the next a simpler problem, laid out in
[src: docs/architecture/overview.md]. Bytes are decoded once at the edge and encoded once at the
other, and every rule in between is a function of text [src: ADR-0004]. The document is read
whole rather than streamed.

The seam every test drives is `format_document(text: str) -> str` in `mdtab/filter.py`. It is a
pure function: no I/O, no globals, no process. `mdtab/__main__.py` exists only to decode, call
it, and encode, so the process boundary needs exactly one test — AC1.

Three interfaces are fixed by this plan; their bodies are not.

- `mdtab/textio.py`
  - `decode(data: bytes) -> str` and `encode(text: str) -> bytes` — UTF-8, `surrogateescape`.
  - `split_lines(text: str) -> list[tuple[str, str]]` — each pair is `(content, terminator)`,
    where `terminator` is `"\r\n"`, `"\n"` or `""` (only ever `""` for the last pair, and only
    when the document does not end in a newline). `content` never contains a terminator.
  - `join_lines(lines: list[tuple[str, str]]) -> str` — the exact inverse.
  - `str.splitlines` is forbidden everywhere in the package: it discards the `\n` / `\r\n`
    distinction AC9 depends on [src: ADR-0004].
- `mdtab/width.py`
  - `display_width(text: str) -> int` — rules 1–3 of [src: ADR-0002], via `unicodedata`.
    Nothing outside this module may use `len()` to mean a width.
- `mdtab/scan.py`
  - `line_prefix(content: str) -> str` — the maximal leading run of `" "`, `"\t"` and `">"`.
  - `in_fence(contents: list[str]) -> list[bool]` — one flag per line, `True` for a line inside a
    fenced code block **and** for the fence lines themselves. A fence opens where the
    prefix-stripped content starts with three or more `` ` `` or three or more `~`, and closes at
    the next line whose prefix-stripped content is at least that many of the same character and
    nothing else; an unclosed fence runs to the end [src: WI-0001 AC8].
  - `find_runs(contents: list[str], fenced: list[bool]) -> list[tuple[int, int]]` — half-open
    index ranges of maximal sequences of two or more consecutive non-fenced lines each containing
    at least one unescaped `|` [src: WI-0001 AC7].
- `mdtab/table.py`
  - `split_row(content: str) -> list[str]` — the fields between unescaped `|`, outer empties
    included. A `|` is escaped when an odd number of `\` immediately precedes it
    [src: WI-0001 AC10]. This is the only cell-splitting function; the cell-count rule, the
    outer-pipe test and the layout all call it, so they cannot disagree.
  - `is_delimiter_row(content: str) -> bool` — every cell matches `:?-+:?` after spaces are
    stripped, and there is at least one cell.
  - `lay_out(contents: list[str]) -> list[str] | None` — the whole of [src: ADR-0003]: returns
    the rewritten lines, or `None` if the run fails any recognition rule. `None` is what makes
    "copy the bytes through" a single branch in the caller.

Two layout rules are **not** free readings of AC12 and must be implemented as written here,
because AC6 forces them:

1. **A column's width is computed over the header and body cells only — never over the delimiter
   row's own cell.** Including it would make the column grow on every run: run one sets the
   delimiter cell to the column width, run two would then take that as the new maximum, and
   `mdtab | mdtab` would not be a fixed point. AC6 says it must be [src: WI-0001 AC6].
2. **A column is never narrower than its delimiter cell can be written.** The delimiter cell is
   filled with `-` across the whole column width, with a `:` occupying the first character if the
   input's delimiter cell began with one and the last if it ended with one. That needs
   `1 + leading_colon + trailing_colon` characters at minimum. For every ordinary column
   `2 + max(display width)` already exceeds it; for a column whose cells are all empty and whose
   marker is `:---:`, it does not, and the width is raised to 3. Both rules are now stated by the
   criterion itself: AC12 was amended to carry them [src: WI-0001 AC12; src: WI-0001/Q-005], so
   this is no longer a place where a criterion is not met literally.

## Steps

1. **`mdtab/textio.py`** — implement `decode`, `encode`, `split_lines`, `join_lines` to the
   signatures above. Afterwards: `join_lines(split_lines(decode(b)))` re-encodes to exactly `b`
   for any bytes `b`, including invalid UTF-8, mixed `\n` / `\r\n`, an empty document, and a
   document with no final terminator.
2. **`mdtab/width.py`** — implement `display_width` per rules 1–3 of [src: ADR-0002] using
   `unicodedata.category` and `unicodedata.east_asian_width`. Afterwards: `display_width("é")`
   is 1 for both the precomposed and the decomposed spelling, `display_width("表")` is 2, and an
   emoji followed by `U+FE0F` measures the same as the emoji alone.
3. **`mdtab/table.py`, cell layer** — implement `split_row` and `is_delimiter_row`. Afterwards:
   `split_row("| a \\| b | c |")` yields the outer empties plus `" a \\| b "` and `" c "`, and
   `is_delimiter_row(" :--- | ---: ")` is true while `is_delimiter_row("| a | b |")` is false.
4. **`mdtab/scan.py`** — implement `line_prefix`, `in_fence` and `find_runs`. Afterwards: on a
   document whose fenced block holds a pipe table, every line of that block is flagged and
   `find_runs` returns no range inside it; an unclosed fence flags every line to the end.
5. **`mdtab/table.py`, recognition layer** — implement the four rules of [src: ADR-0003] as
   predicates over a run, and have `lay_out` return `None` when any fails: a delimiter row second
   [src: WI-0001 AC7], one byte-identical `line_prefix` across the run [src: WI-0001 AC15],
   one cell count across every row including the delimiter row [src: WI-0001 AC13], and one
   outer-pipe style — leading and trailing judged separately but both agreed — across every row
   [src: WI-0001 AC14]. Afterwards: `lay_out` returns `None` for each of the ragged, mixed-style
   and mixed-prefix fixtures.
6. **`mdtab/table.py`, layout layer** — implement the rewriting: strip the shared prefix, compute
   each column's width by the two rules in `## Approach`, render each cell as one space, the
   stripped content, padding to the column width, one space; render the delimiter cells; restore
   each row's own outer pipes only where the input had them; re-attach the prefix. Afterwards:
   the pipes of every laid-out fixture sit at the same display column in every row, and no line
   gained or lost a `|`.
7. **`mdtab/filter.py`** — implement `format_document(text) -> str`: split lines, compute the
   fence mask, find runs, call `lay_out` on each, splice the result back where it is not `None`,
   and join. Afterwards: a document with no table comes back identical, and running the output
   through again produces identical text.
8. **`mdtab/__main__.py`** — read `sys.stdin.buffer`, `decode`, `format_document`, `encode`,
   write `sys.stdout.buffer`, flush, return 0. Nothing is written to `sys.stderr` on any input.
   Afterwards: `printf '...' | python3 -m mdtab` from the checkout root prints the document and
   exits 0.
9. **`.gitattributes`** — add `tests/fixtures/** -text -diff` so git never normalises a fixture's
   line endings. Afterwards: a CRLF fixture survives a clone on any platform, which is what makes
   the AC9 test meaningful [src: ADR-0005].
10. **`tests/fixtures/`** — create the fixture pairs named in the mapping table below, each as
    `<name>.in.md` and `<name>.out.md`, written as bytes. A test may not build a document from a
    Python literal [src: ADR-0005]. A pair whose bytes are deliberately **not** valid UTF-8
    carries `<name>.in.bin` and `<name>.out.bin` instead — that is the whole of the exception,
    and the reason it exists is that `validate-workspace` reads every `.md` file in the project
    as UTF-8 [src: ADR-0006; src: WI-0001/Q-004]. One such pair is required by this plan:
    `invalid-utf8`, holding a table one of whose cells contains a `0xFF` byte, which is the
    evidence for AC9's undecodable-bytes clause and for `surrogateescape` [src: ADR-0004].
11. **`tests/test_fixtures.py`** — one `unittest.TestCase` that, for each fixture pair, asserts
    `encode(format_document(decode(in_bytes))) == out_bytes`, and additionally asserts
    idempotence by re-running on the output. Pairs are discovered by the `.in.` infix, not by the
    `.md` suffix, so a `.bin` pair is picked up by every fixture-wide test without being
    registered a second time [src: ADR-0006]. Afterwards:
    `python3 -m unittest discover -s tests -t .` exits 0.
12. **`tests/test_units.py`** — unit tests for `display_width`, `split_row`, `is_delimiter_row`,
    `line_prefix`, `in_fence` and `find_runs`, and one test asserting `lay_out` returns `None` for
    each rejection rule. Afterwards: both gate commands in `tracker/project.yaml` exit 0.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 8 | `printf 'a\|b\n-\|-\n' \| python3 -m mdtab` from the checkout root: document on stdout, `$?` is 0, stderr empty |
| AC2 | 2, 6 | fixture `basic-ascii`; a test computing each row's `display_width` and each `\|`'s column, asserting all rows equal and each *n*th pipe equal |
| AC3 | 2, 6 | fixture `unicode-mixed` (precomposed `é`, decomposed `e`+U+0301, emoji+U+FE0F, CJK) run through the same AC2 assertion |
| AC4 | 5, 7 | fixtures `prose-around-table`, `rst-grid`, `html-table`: the non-table lines byte-identical between `.in.md` and `.out.md` |
| AC5 | 7 | fixture `no-table` — `.in.md` and `.out.md` are the same bytes |
| AC6 | 6, 7, 11 | every fixture: `format_document` applied twice equals applied once, asserted for all pairs by the shared test |
| AC7 | 4, 5 | fixtures `rst-grid`, `html-table`, `pipes-no-delimiter` come back byte-identical; unit test on `find_runs` and `is_delimiter_row` |
| AC8 | 4 | fixtures `fenced-table` (ragged table inside a fence) and `fence-unclosed` come back byte-identical; unit test on `in_fence` |
| AC9 | 1 | fixtures `crlf` and `no-final-newline`; `od -c` on the last bytes of each output equals the input's. The undecodable-bytes clause is fixture `invalid-utf8` (`.in.bin` / `.out.bin`), asserted as bytes [src: ADR-0006] |
| AC10 | 3, 6 | fixture `escaped-pipe`: the laid-out row has two cells and the first still reads `a \| b`; unit test on `split_row` for `\|` and `\\|` |
| AC11 | 6 | a test asserting, for every fixture pair, that each output cell stripped of spaces equals the corresponding input cell stripped of spaces |
| AC12 | 6 | fixture `basic-ascii` plus a test asserting one space inside each `\|`, an empty cell rendering as two spaces, each column measuring `2 + max`, and the delimiter row keeping its `:` |
| AC13 | 5 | fixture `ragged-rows` (one row with an extra cell, one short) comes back byte-identical; unit test that `lay_out` returns `None` |
| AC14 | 5, 6 | fixtures `bare-pipes` (laid out, still bare), `outer-pipes` (laid out, still outer) and `mixed-pipes` (byte-identical); a test asserting each line's `\|` count is unchanged across every fixture |
| AC15 | 4, 5, 6 | fixtures `blockquote-table`, `list-indent-table` (both laid out, prefix intact, AC2 assertion applied) and `ragged-prefix` (byte-identical) |

## Assumptions

- **The document is read whole, not streamed.** Reversing it means rewriting `format_document`
  to consume an iterator and buffering only the current run — one module, no interface change
  outside it, no fixture change. It is cheap because no criterion can tell the two apart, and it
  is chosen because the fence-to-end-of-document rule and the final-terminator rule are both
  simpler over a list. Would need revisiting only for the batch mode [src: ADR-0001] names as a
  separate item.
- **The single supported invocation is `python3 -m mdtab`, run from the checkout root.** AC1
  defers the invocation to this plan [src: WI-0001 AC1]. A `bin/mdtab` shebang script that works
  from any directory is four lines and no interface change, and should be added the moment
  anyone wants to run mdtab in a shell loop over files; it is left out here because no criterion
  asks for it.
- **The minimum interpreter is CPython 3.8**, which [src: ADR-0001] left to this plan. Nothing in
  the design needs anything newer, and the implementation must not use syntax or builtins
  introduced after 3.8 — notably `str.removeprefix`, which is 3.9. This is asserted, not tested:
  the only interpreter present here is 3.12.3 [src: run: python3 -VV → CPython 3.12.3], so the
  floor is a constraint on the code rather than a verified claim, and `verify` should treat it
  that way.
- **An all-empty centred column is one character wider than AC12's original formula — no longer
  an assumption.** When this plan was written AC12 said a column is *exactly*
  `2 + max(display width of its cells)`, while AC6 says the tool is idempotent
  [src: WI-0001 AC6]. For a column whose header and body cells are all empty and whose delimiter
  cell is `:---:`, the formula gives 2, into which `::` fits but no `-` does — and `::` is not a
  delimiter cell, so the second run would not recognise the table and the output would differ
  from the first run's. The width is therefore 3 in that one case. This was recorded here as an
  assumption because it was the only place a criterion was not met literally; `answer-questions`
  has since amended AC12 to state the rule, so it is now a criterion rather than an assumption
  and nothing about it is open [src: WI-0001 AC12; src: WI-0001/Q-005].
- **`commands.build` stays null.** There is nothing to build: the tool is source that
  `python3` runs directly [src: ADR-0001].

## Decisions and ADRs

| decision | where it is recorded | route |
|----------|---------------------|-------|
| Bytes in and out, UTF-8 with `surrogateescape`, terminators split off | [src: ADR-0004] (new) | decided |
| `unittest` plus file fixtures, `compileall -W error` as lint | [src: ADR-0005] (new) | decided |
| Module boundaries and the one-place-per-rule list | [src: docs/architecture/overview.md] (new) | decided |
| Python 3, standard library only, stdin-to-stdout | [src: ADR-0001] | documented |
| Display width, not character count | [src: ADR-0002] | documented |
| The four recognition rules and "never the punctuation" | [src: ADR-0003] | documented |
| Read whole vs stream; sole invocation; 3.8 floor; the centred-empty-column width | `## Assumptions` | assumed |

Nothing was asked of the stakeholder. Every choice above is either cited to a document or
recorded as a reversible assumption, which is the preference order this skill is held to; none
of them is irreversible and none turns on intent no document records.

## Scaffolding

- `mdtab/__init__.py` — empty. `python3 -W error -m compileall -q mdtab tests` cannot run against
  a directory that does not exist, and `commands.lint` names it.
- `tests/__init__.py` — empty. `python3 -m unittest discover -s tests -t .` raises
  `ImportError: Start directory is not importable` without it, and `commands.test` names it.

Both files are empty and contain no behaviour. Deleting them breaks a gate command; it breaks no
acceptance criterion.

## Risks

- **The width rule and the fixtures can be wrong together.** If `display_width` mis-measures a
  character and the expected fixture was generated by running the tool, the test passes and the
  table is still ragged in an editor. Mitigation: the `unicode-mixed` fixture's `.out.md` must be
  written by hand, or checked by eye in a fixed-width font, not produced by the code under test.
  This is the one fixture that cannot be generated.
- **`in_fence` and `find_runs` can disagree about a line.** Both consume the same list of
  contents; if a future change lets `find_runs` re-derive fence state instead of taking the mask,
  a table adjacent to a fence will be mis-grouped. The overview names this as a one-place rule
  [src: docs/architecture/overview.md]; the unit test in step 12 is what keeps it honest.
- **AC12 and AC6 conflict in one degenerate case**, resolved in `## Assumptions` in AC6's favour.
  If `verify` reads AC12 literally it will file a defect against a deliberate choice. The
  assumption is written so that the answer is an amendment, not a code change.
- **The lint gate is thin.** `compileall -W error` checks syntax and syntax warnings and nothing
  else [src: ADR-0005]; no journal entry may report it as more. Style and dead code are caught
  only in review.
- **The 3.8 floor is untested.** Only 3.12.3 is installed, so a 3.9-only builtin would pass every
  gate here and fail on the stakeholder's machine if it is older. Review is the only check.

## Out of scope for this item

- Honouring the alignment markers when padding. This item preserves them and pads every column
  the same way; WI-0002 makes them mean something [src: WI-0002].
- A `bin/mdtab` entry point, batch mode, or any way of naming files. See `## Assumptions` and
  [src: ADR-0001].
- Any diagnostic on stderr, and any behaviour that depends on a flag or an environment variable.
  The tool has no options [src: EP-001].
- A markdown parser. Structure is textual [src: docs/architecture/overview.md].
