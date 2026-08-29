# Verification report — WI-0002

Verified-commit: a8b5a4bb2b2c5ecd4baed6bb959b88233d7ef80a

## Verdict

**Pass.** All fourteen acceptance criteria hold, each demonstrated by a command run in this
execution against the branch head, on documents written here rather than taken from the item's
own fixtures. One non-blocking question is filed to the architect (`Q-003`) about the wording of
AC14, whose two clauses cannot both hold; AC14's substance was checked independently and does
hold. No defect was found and nothing is sent back.

## Criteria

Every command below was run from the repository root with `wi/WI-0002` checked out at
`a8b5a4b`. The documents live in `/tmp/vwi2/` and are quoted inline; none of them is a fixture
this item shipped, so a wrong fixture could not make a criterion pass here.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `printf '\| alpha \| beta \| gamma \| delta \|\n\| :--- \| ---: \| :---: \| --- \|\n\| x \| x \| x \| x \|\n\| wwwww \| wwwww \| wwwww \| wwwww \|\n' \| python3 -m mdtab` | `\| alpha \|  beta \| gamma \| delta \|` / `\|:------\|------:\|:-----:\|-------\|` / `\| x     \|     x \|   x   \| x     \|` / `\| wwwww \| wwwww \| wwwww \| wwwww \|` | one column per marker: `:---` pads after, `---:` pads before, `:---:` splits it, `---` pads after. Spaced markers checked separately: `\|  :---  \| ---:  \|` over `\|  ab  \|  cd  \|` gives `\| ab    \|    cd \|`, the same two alignments |
| AC2 | **pass** | the AC1 document, with each cell's first non-space character measured in display columns | `col1 :--- first-char cols=[2, 2, 2]`; `col4 --- first-char cols=[26, 26, 26]` | header row included in each set |
| AC3 | **pass** | the same measurement on the last non-space character | `col2 ---: last-char cols=[14, 14, 14]` | and the character at the next column is the guard space, per AC7 below |
| AC4 | **pass** | `printf '\| ab \|\n\|:---:\|\n\| xyz \|\n' \| python3 -m mdtab`, then the same with `\| xyzwv \|` | `\| ab  \|` / `\|:---:\|` / `\| xyz \|`; and `\|  ab   \|` / `\|:-----:\|` / `\| xyzwv \|` | AC4's own document gives `\| ab  \|`, not `\|  ab \|`. The second document has three spare columns and gives one before, two after — `floor`/`ceil` with the extra on the right, and it is what tells centring from left-padding, which AC4's own document cannot |
| AC5 | **pass** | a `---:` column holding `表`, `é` (U+00E9), `e`+U+0301 and `seven7`, with the last non-space character measured in display columns | `row 0 … = 11`, `row 2 … = 11 表`, `row 3 … = 11 ['0xe9']`, `row 4 … = 11 ['0x65', '0x301']`, `row 5 … = 11 seven7` | codepoints printed to prove the decomposed cell really is two codepoints |
| AC6 | **pass** | the same four-column table laid out four times, once per marker in column 2, with every `\|`'s display column collected | `:--- → [[0, 7, 13, 21], …]` and identically for `---:`, `:---:` and `---`; `all four identical: True` | `_column_widths` is untouched in the diff, which is the mechanism |
| AC7 | **pass** | `python3 -m mdtab < ac7r.md \| sed '2d' \| grep -n '\|[^ ]'` and `… \| grep -n '[^ ]\|'`, for a right-aligned (`\|---:\|---:\|`) and a centred (`\|:---:\|:---:\|`) table | no match, grep exit 1, in all four runs | the delimiter row is excluded with `sed '2d'`: AC9 fills it with dashes, so it has no guard spaces to keep |
| AC8 | **pass** | `printf '\| a \|  \| c \|\n\| --- \| :---: \| --- \|\n\| 1 \|  \| 3 \|\n' \| python3 -m mdtab` | `\| a \|   \| c \|` / `\|---\|:-:\|---\|` / `\| 1 \|   \| 3 \|` | exactly the `\|   \|` over `\|:-:\|` AC8 names. An empty cell in a `---:` column beside a four-wide one gives `\|      \|`, identical to a left column's |
| AC9 | **pass** | `printf '\| abcd \| x \|\n\|  :---  \| ---:  \|\n\| e \| y \|\n' \| python3 -m mdtab`, then the delimiter row's cell widths and colon positions | `\|:-----\|--:\|`; `col0=[:-----] len=6  col1=[--:] len=3`; colon ends in `[(True, False), (False, True)]` both before and after | the `\|:-----\|--:\|` over columns 6 and 3 wide that AC9 names, with no `:` added, moved or removed |
| AC10 | **pass** | `printf 'a \| b\n---:\|---\nxxxx \| y\n' \| python3 -m mdtab` | `   a \| b` / `----:\|--` / `xxxx \| y` | first column's cells both end at display column 3; leading spaces present; pipe counts per line identical to the input (`[1, 1, 1]`), so no outer `\|` was added; `cmp` of the output against the output run again → identical, so WI-0001 AC6 holds |
| AC11 | **pass** | `printf 'a \| bbbb\n---\|---:\nxxxx \| y\n' \| python3 -m mdtab \| awk '{print length($0)}'` | `a    \| bbbb` / `-----\|----:` / `xxxx \|    y`; widths `11`, `11`, `11` | `grep -n ' $'` on the output → no match, exit 1: the line ends at the content |
| AC12 | **pass** | a `---:` table under `> ` on every line, and a `--:`/`:--:` table indented two spaces under a list item | `> \| k    \|    v \|` … (4 lines, all matching `^> `); and `  \|    k \|  v   \|` / `  \|-----:\|:----:\|` / `  \|    a \| bbbb \|` / `  \| cccc \|  d   \|` | for the list-indent document, lines 0, 1, 6, 7, 8 are byte-identical in and out; only the four table lines changed |
| AC13 | **pass** | four documents fed through `python3 -m mdtab` and `diff`ed against themselves: ragged cell count, mixed outer pipes, ragged prefix, and a table inside a fence — every one carrying `:` markers | all four "identical byte-for-byte (diff exit 0, no output)"; and `lay_out` returns `None` for the first three when called directly | the fenced case never reaches `lay_out`; `find_runs` excludes it |
| AC14 | **pass on its substance; see `Q-003`** | fifteen separate checks of WI-0001's criteria on marker-bearing documents, listed below | `AC1 exit=0 stderr=b''`; `AC2/AC3 row display widths = [33]`, `[14]`, `[17]` (one value each); `AC4 lines changed: [4]`; `AC5 … identical: True`; `AC6 … idempotent: True` on nine documents including AC10's and AC11's; `AC9 CRLF preserved: True`, `no final newline added: True`, `undecodable byte survives: True`; `AC10 escaped pipe: '\| a \\\| b \|    or \|'`; `AC11 cells differing after stripping spaces: none` | AC14's second clause — "running WI-0001's shipped test suite **unchanged**" — is **not** satisfied and cannot be: two places in that suite encode the very clause AC14's first half excepts. Both were changed by `implement`. That contradiction is `Q-003`, filed to the architect, non-blocking |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run in this execution against `a8b5a4b` → exit 0, "Ran 65 tests in 0.082s / OK" |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → "checked 4 item(s), 9 document(s) … 0 errors, 0 warnings" (it failed once mid-execution with `board.stale` after `Q-003` was filed; `board-gen` fixed it and it was re-run clean) |
| `every-criterion-independently-checked` | **pass** | the Criteria table names, for all fourteen, a command run here and its actual output. No row cites `impl-report.md`, and no row's document is one of this item's fixtures |
| `negative-cases-exercised` | **pass** | see the section below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | see the section below |

## Negative and boundary cases exercised

Each was triggered, not read about.

- **A run that is not a table, with markers on it** (AC13) — four separate documents, one per
  rejection route. Ragged cell count `\| 1 \| 2 \| 3 \|` under a two-cell header; mixed outer pipes
  `a | b` under `| a | b |`; a prefix of `>  ` on one line where the others have `> `; a table
  between two ``` fences. All four came back byte-for-byte; `lay_out` returns `None` for the
  three that reach it.
- **An empty cell, and a whole column of them** (AC8) — `| a |  | c |` under
  `| --- | :---: | --- |` gives `|   |` over `|:-:|`. The column's width is 3 rather than the 2
  the `2 + max(...)` formula gives, which is WI-0001 AC12's minimum-width qualification, not
  something alignment changed.
- **A row with no pipe to align against, at both ends** (AC10, AC11) — a bare table with a `---:`
  first column, whose padding lands at the start of the line; and one with a `---:` last column
  and no trailing pipe, whose line ends at the content. Both checked for the thing that would
  have gone wrong: no `|` added (pipe counts identical in and out), and no trailing space
  (`grep -n ' $'` → no match).
- **mdtab refusing to recognise its own output** (AC10) — the bare right-aligned document's
  output fed back in. It is refused, and the bytes are unchanged, so idempotence holds. This is
  the deliberate cost ADR-0007 records and WI-0003 exists to remove; it is not a defect of this
  item.
- **A delimiter cell with no dash in it** — `| : | --- |` is not a delimiter row at all, so the
  marker reader is never reached: `is_delimiter_row("| : | --- |")` is `False` and `lay_out`
  returns `None`.
- **Characters whose width is not their length** (AC5) — CJK, a precomposed accent, the same
  accent decomposed into two codepoints, and an undecodable byte `\xff` carried through by
  surrogateescape. All measured by display column, all surviving the round trip.
- **Line terminators at the boundary** (AC14/WI-0001 AC9, on marker-bearing tables) — a CRLF
  document keeps all three CRLFs and gains no bare `\r`; a document with no final newline gains
  none.

## Test sensitivity check

Three mutations, each applied to `mdtab/table.py`, the suite run, then `mdtab/table.py` restored
from a copy taken beforehand. `git status --short` was empty after the last restore and the suite
returned to "OK".

| mutation | tests that failed |
|----------|-------------------|
| `_render_cell`'s three branches replaced by WI-0001's single `before, after = 0, padding` | 13 failures across 6 named tests: `test_every_fixture_produces_its_expected_output`, `test_ac1_python3_m_mdtab_writes_the_document_and_exits_zero`, `test_ac3_every_cell_of_a_right_column_ends_at_the_same_display_column`, `test_ac4_a_centred_cell_leans_left_when_the_spare_column_is_odd`, `test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`, `test_ac11_a_right_aligned_last_column_ends_the_line_at_its_content` |
| `column_alignments` always answering `"left"` | 16 failures across 9 named tests — the six above plus all three of `ColumnAlignmentTest`'s marker-reading tests |
| centring rounded the other way (`after = padding // 2`), so the odd column falls on the left | 4 failures across 2 named tests: `test_ac4_a_centred_cell_leans_left_when_the_spare_column_is_odd` and `test_every_fixture_produces_its_expected_output` |

The third mutation is the one worth having: it is a one-character change that no fixture with an
even remainder and no equal-width-rows assertion would catch, and the stakeholder decided that
tie-break themselves (`WI-0002/Q-001`).

## Defects found

**None.** No criterion of this item failed, so nothing is sent back, and no behaviour delivered
by another item was found to be broken, so no bug item was filed.

Two things were looked for specifically and are not defects:

- **mdtab no longer recognises a bare right- or centre-aligned table it laid out itself.** This
  is required by AC10, decided by the stakeholder in `WI-0002/Q-002` with the cost in front of
  them, recorded in ADR-0007, and owned by WI-0003, which already exists at `draft` with
  `arose-from: WI-0002/Q-002`. Filing a bug for it would duplicate WI-0003.
- **The diff against the plan holds nothing unaccounted for.** `git diff main -- mdtab/` is four
  hunks, all in `mdtab/table.py`: the new `column_alignments`, the `alignment` parameter and
  three branches in `_render_cell`, the `alignments` parameter in `_render_row`, and the one
  extra line in `lay_out`. `_column_widths`, `_render_delimiter`, `_spaces_omitted` and the four
  recognition rules are byte-identical to `main`. Every hunk traces to plan step 1, 2 or 3.

`impl-report.md`'s five declared deviations were each checked against the item rather than
accepted: deviation 1 is the subject of `Q-003`; deviations 2, 3 and 5 add fixtures or assertions
that AC11, AC12 and AC4 name and the plan omitted, so they close gaps rather than open them;
deviation 4 adds a unit test for AC11 that the plan left to a fixture. None widens what the item
delivers.

## Not verified, and why

- **AC14's literal second clause is not satisfied and was not verified as written.** "Running
  WI-0001's shipped test suite unchanged" is impossible while AC14's own first half excepts the
  padding-position clause, because two places in that suite encode exactly that clause. What was
  verified instead is AC14's substance — every WI-0001 criterion, re-checked here on documents
  carrying markers — and it holds. The wording is `Q-003`, non-blocking, addressed to the
  architect, and it should be answered before `review-close` reads AC14 against D2.
- **The independence of this verification is weaker than the pipeline intends.** The same session
  ran `implement` on this item earlier in the same turn. The defences used were to derive each
  check from the criterion before reading `impl-report.md`, to write fresh documents rather than
  reuse the item's fixtures, and to put the one real judgement call — deviation 1 — in front of
  a different persona through `Q-003` rather than let it stand on this skill's say-so. A reader
  should treat the Criteria table's commands as the evidence and this paragraph as its limit.
- **No performance, concurrency or large-input behaviour was checked.** No criterion of this item
  or of WI-0001 mentions any, and the tool has no such requirement recorded anywhere.
- **`column_alignments` is public and unguarded against a `rows` list shorter than two.** It is
  called only from `lay_out`, which has already rejected any run of fewer than two lines, so no
  reachable input hits it. No criterion covers it and it is not a defect; it is recorded here so
  that WI-0003, which will change the recognition rules, knows the guard lives in the caller.
