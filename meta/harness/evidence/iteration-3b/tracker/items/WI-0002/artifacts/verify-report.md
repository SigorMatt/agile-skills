# Verification report — WI-0002

Verified-commit: e533928e704deb8f7a67a0f5c90e688412971158

This is the **second** verification of WI-0002. The first ran at `867ef75` and passed; `review-close`
then rejected the item on D7 and D12 — two standing ADRs carried a clause and four citations that
this item had made false — and sent it back to `in-progress`
[src: tracker/items/WI-0002/history.md]. Those repairs are now in `8c58ac1` and `e4dd5c6`, and the
item returned to `verifying` at `e533928`.

No code and no test changed between the two verifications (`git diff a324868..e533928 -- mdtab.py
tests/` is empty, checked below), so this run could have cited the earlier report. It does not.
Every verdict below rests on a command run in this session against `e533928`; the earlier report is
superseded, not extended. Where this run reached a different conclusion from the first, it says so.

## Verdict

**Pass.** All ten acceptance criteria are confirmed with evidence gathered in this session. No
defect of this item's own criteria was found, and no bug item was filed against another item. The
item moves to `in-review`.

Two observations that are not defects are recorded under `## Observations`; neither blocks the
verdict and neither is a criterion failure.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 24 tests in 4.719s` / `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → no output, exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 3 item(s), 8 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | every row of `## Criteria` names a command this skill ran and quotes its actual output. `impl-report.md` is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | 21 negative and boundary cases triggered, listed in full below |
| `a-criterion-about-criteria-is-read` | **pass** | AC9: all eleven WI-0001 criteria given a per-criterion verdict read from their own text; three non-intersections stated in those words, covering cases run, committed-test additions waived by ID with reasons |
| `tests-would-fail-without-the-change` (advisory) | **pass** | seven mutations of `mdtab.py`, each caught; per-criterion table below |

Neither gate command is null, so neither is skipped.

## Criteria

Commands were run from the repository root on branch `wi/WI-0002` at `e533928`, working tree clean
(`git status --porcelain` → empty).

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — left marker | **pass** | `printf '%s\n' '\| Name \| Qty \| Note \|' '\|:-----\|:--\|:---\|' '\| bolt \| 12 \| a \|' '\| longcell \| 3 \| bb \|' \| python3 mdtab.py \| cat -A` | `\| Name     \| Qty \| Note \|$` / `\|:---------\|:----\|:-----\|$` / `\| bolt     \| 12  \| a    \|$` / `\| longcell \| 3   \| bb   \|$` | Column 1 has `W=8` (`longcell`); `Name` is written `\|`, one space, `Name`, `8-4=4` spaces, one space. Separately, on a three-column left/right/centre table, the left column's text **start** display offsets over header and all body rows are `{2}` — one value, so "the same on every row … the header row included" holds and is not vacuous (the cells differ in width). All padding is to the right |
| AC2 — right marker | **pass** | `printf '%s\n' '\| Name \| Qty \| Note \|' '\|-----:\|--:\|---:\|' '\| bolt \| 12 \| a \|' '\| longcell \| 3 \| bb \|' \| python3 mdtab.py \| cat -A` | `\|     Name \| Qty \| Note \|$` / `\|---------:\|----:\|-----:\|$` / `\|     bolt \|  12 \|    a \|$` / `\| longcell \|   3 \|   bb \|$` | `Name` is `\|`, one space, `8-4=4` spaces, `Name`, one space. On the three-column table the right column's text **end** display offsets over header and all body rows are `{14}` — one value. All padding is to the left |
| AC3 — centre marker, odd remainder to the right | **pass** | odd: `printf … '\| Item \| Qtr \|' '\|------\|:---:\|' '\| bolt \| ab \|' '\| nut \| Q \|' \| python3 mdtab.py \| cat -A`; even: same with header `Quar` and `\|:----:\|`; width-1: `'\| Item \| Q \|' '\|------\|:-:\|' '\| bolt \| Q \|'` | odd → `\| bolt \| ab  \|$` and `\| nut  \|  Q  \|$`; even (`W=4,w=2`) → `\| bolt \|  ab  \|$`; width-1 → `\| bolt \| Q \|$` | `W=3, w=2`: `pad=1`, `1//2=0` before and `1` after → `\| ab  \|`, which is the criterion's first worked example verbatim, and **not** `\|  ab \|`. `W=3, w=1`: `pad=2` → one space each side, `\|  Q  \|`. Both parities exercised. See `## Observations` 1 for AC3's second illustration |
| AC4 — no marker | **pass** | `printf '%s\n' '\| Name \| Qty \|' '\|---\|---\|' '\| bolt \| 12 \|' '\| longcell \| 3 \|' \| python3 mdtab.py \| cat -A` | `\| Name     \| Qty \|$` / `\|----------\|-----\|$` / `\| bolt     \| 12  \|$` / `\| longcell \| 3   \|$` | Text then padding, byte-identical in shape to what WI-0001 AC3 requires. Independently: `ragged.md` → `ragged.expected.md` byte for byte, and that expected file was written under WI-0001 and is unchanged on this branch (`git diff main...wi/WI-0002 -- tests/fixtures/ragged.expected.md` is empty) |
| AC5 — empty cells and zero-width marked columns | **pass** | (a) `printf … '\| L \| R \| C \|' '\|:--\|--:\|:-:\|' '\| aaa \| bbb \| ccc \|' '\|  \|  \|  \|' \| python3 mdtab.py \| cat -A`; (b) `printf … '\|  \|  \|  \|' '\|:---\|---:\|:---:\|' '\|  \|  \|  \|' \| python3 mdtab.py \| cat -A`; (c) the same piped through `python3 mdtab.py` twice | (a) row 4 → `\|     \|     \|     \|$` — five spaces (`W+2 = 3+2`) in the left-, right- and centre-marked column alike; (b) → `\|  \|  \|   \|$` / `\|:-\|-:\|:-:\|$` / `\|  \|  \|   \|$`; (c) byte-identical to (b) | (b) is exactly the criterion's second sentence: `:---` → `W=0`, two spaces; `---:` → `W=0`, two spaces; `:---:` → `W=1` by ADR-0004's two-colon minimum, three spaces. Delimiter cells are `W+2` characters: `:-`, `-:`, `:-:` |
| AC6 — markers and display width together | **pass** | `python3` harness running the filter on `\| L \| R \| C \|` / `\|:--\|--:\|:-:\|` / `\| 漢字 \| 🙂x \| e+U+0301 b \|` / `\| a \| bb \| ccc \|` and measuring each line's display width and each `\|`'s display offset | every line display width `20`; pipe offsets `[0, 7, 13, 19]` on all four lines including the delimiter row; character lengths `[20, 20, 18, 20]` | Run twice: once with a precomposed `é` and once with a genuine NFD `e`+U+0301 (3 characters, display width 2) so the combining-mark branch is actually taken. The differing character lengths confirm the criterion is about display columns, not characters |
| AC7 — markers survive and mean the same thing | **pass** | `python3` harness over the ten AC1–AC7 inputs: per column, output delimiter cell starts with `:` iff input's did, ends with `:` iff input's did, matches `^:?-+:?$`, contains no space, and has length `W+2` (with ADR-0004's minimum of 1 for a two-colon column) | `AC7 violations: none`. Negative direction: markerless table `\|---\|---\|---\|` → `'\|---\|---\|---\|'`, colons present: `False` | My first pass reported one violation on the all-empty `:---:` column; that was my harness omitting ADR-0004's minimum from `W`, not the filter. The criteria preamble defines `W` with that minimum, so the corrected harness is the one that answers AC7. The filter's output was right both times |
| AC8 — idempotence over marked tables | **pass** | the same harness re-feeding each of the ten AC1–AC7 inputs' output to the filter | `idempotent=True` for all ten. Separately, all 30 files under `tests/fixtures/` (including `not_utf8.markdown`): `exit=0 idem=True` for every one | |
| AC9 — WI-0001's criteria re-read by ID | **pass** | see `## AC9 — WI-0001's eleven criteria, re-read` below | eleven per-criterion verdicts; three non-intersections named | This criterion is about this report, so this report is its evidence |
| AC10 — tests | **pass** | `grep -n 'def test' tests/test_mdtab.py`; `python3 -m unittest discover -s tests -t .` | one method per criterion: `test_wi0002_ac1_…` through `test_wi0002_ac9_…`, plus `test_wi0002_ac10_each_criterion_has_a_named_test`, each carrying its criterion's text as its docstring. `Ran 24 tests … OK`, exit 0. Exit status 0 confirmed on every input named in AC1 to AC8 — all ten AC-inputs above, all 30 fixtures, and all 21 boundary cases below | |

## AC9 — WI-0001's eleven criteria, re-read

Each verdict below was reached by reading that criterion's own sentence against what the filter does
at `e533928`. The suite is cited as evidence for a verdict, never as its definition.

| WI-0001 AC | verdict | the reading |
|------------|---------|-------------|
| AC1 — every line of the output table has the same display width | **still true** | Placing padding by marker moves spaces inside a cell; it never changes how many there are, because `pad = width - display_width(cell)` is computed before the split and both runs are emitted. Evidence: my AC6 run — a left/right/centre-marked table with wide, emoji and combining characters, every line display width `20` |
| AC2 — every column occupies the same span of display columns on every row, delimiter row included | **still true** | Same reason. Evidence: pipe offsets `[0, 7, 13, 19]` identical on all four rows of that marked table, delimiter row included |
| AC3 — content cell is `\|`, one space, text, padding to the column's width, one space; empty cell is `\|` and two spaces; no composed line ends in a space or tab | **narrowed — see below** | This is the one criterion this item's behaviour changes. Its middle clause reads as *padding always following the text*; that now holds **only for a column whose delimiter cell carries no marker**. The markerless case is asserted by **WI-0002 AC4** above, verified byte-identical to WI-0001's own `ragged.expected.md`. The marked case is decided by **ADR-0005** and asserted by WI-0002 AC1, AC2 and AC3. **WI-0001's criteria are not edited.** Two sub-clauses read separately: (i) *"empty cell is `\|` followed by two spaces"* is narrowed by ADR-0004's two-colon minimum — an all-empty `:---:` column gives three, not two — but that is a **WI-0001-era** rule (`ADR-0004` was added in `ac16080`, under WI-0001), restated by WI-0002 AC5, not something this item changed; (ii) *"no line the filter composes ends in a space or a tab"* is **still true** under every marker, evidenced by three runs with an empty cell in the last column under a left, a right and a centre marker → `trailing-ws lines: []` in each |
| AC4 — delimiter row is `\|` + (width + 2) hyphens and no spaces, narrowed when the input's is longer | **still true** | `compose_delimiter` is untouched by this item (`git diff main...wi/WI-0002 -- mdtab.py` shows no change inside it). Evidence: `\| a \| b \|` / `\|:----------\|---------:\|` / `\| x \| y \|` → `\|:--\|--:\|`, narrowed from 10 hyphens to `W+2 = 3`, with the colons kept and no space. (The "hyphens" clause was already narrowed by ADR-0004 under WI-0001; this item does not touch that) |
| AC5 — a uniformly indented table is tidied with its prefix restored byte for byte; mismatched indent and `> `-prefixed blocks pass through | **still true** | **Non-intersection in the committed suite** — see below. Read against the code: `emit_block` re-emits `prefix` on every composed line and `column_widths` never sees it, so a marker cannot reach the prefix. Evidence I ran: an indented marked table → all four table lines begin `'   '` and the columns are correctly marked; a blockquoted marked table → byte-identical; a mismatched-indent marked block → byte-identical |
| AC6 — input containing no table is byte-identical (empty, no final newline, CRLF, non-UTF-8) | **still true, vacuously w.r.t. markers** | A marker lives in a delimiter row, and a delimiter row only exists inside a table, so "input containing no table" and "a marked column" cannot intersect — this is a **vacuous** crossing, not a coverage gap. Evidence: empty input, prose with `\xff\xfe`, all byte-identical, exit 0. I additionally ran the *stronger* case AC6 does not ask for — a **marked table** with CRLF, with no final newline, and with non-UTF-8 bytes in a cell — and all three round-trip correctly and idempotently, gaining no newline |
| AC7 — fenced blocks and surrounding prose pass through byte-identical while a real table outside them is tidied | **still true** | **Non-intersection in the committed suite** — see below. Read against the code: `transform` flushes and copies inside a fence before `candidate_parts` is ever consulted, so marker handling is unreachable there. Evidence I ran: a ``` fence containing a marked table plus a marked table outside it → the five fenced lines byte-identical, the outside table aligned by its markers |
| AC8 — a block that is not a well-formed table is copied whole, including its well-formed rows | **still true** | **Non-intersection in the committed suite** — see below. Read against the code: `table_or_none` returns `None` and `emit_block` copies the raw lines before `column_alignments` is called. Evidence I ran: a ragged marked block (`\|:--\|--:\|:-:\|` with a two-cell body row) → byte-identical; a marked-looking block whose second row is `\| :x \| y: \|` → byte-identical |
| AC9 — idempotence over the AC1 and AC5–AC8 inputs | **still true** | Intersects: `INPUT_FIXTURES` now includes `markers.md`, `aligned.md`, `aligned_empty.md` and `aligned_wide.md`, all marked, and `test_wi0001_ac9_…` loops over it. Evidence: my own sweep — all 30 fixture files, `idem=True` |
| AC10 — exit status 0 for every input named in AC1 to AC9 | **still true** | Same loop, same fixtures. Evidence: `exit=0` on all 30 fixtures, on their own output, on all ten AC-inputs and on all 21 boundary cases |
| AC11 — a test exists for each of AC1 to AC10, each naming its criterion, and the suite passes | **still true** | This is the criterion ADR-0006's rename was written to protect. `grep -n 'def test'` shows `test_wi0001_ac1_…` through `test_wi0001_ac11_…` all present under the new `wi0001_` tag, and WI-0002's methods carry `wi0002_`, so WI-0001's "exactly one method per tag" assertion still finds one. Suite green at 24 tests |

### Non-intersection, stated in those words

**Nothing executable in the committed suite exercises WI-0001 AC5, WI-0001 AC7 or WI-0001 AC8
together with a marked column.** Their own tests use `indented.md`, `indent_mismatch.md`,
`blockquote.md`, `fenced.md` and `malformed.md`, and every one of those fixtures is unmarked
(checked by reading them). WI-0001 AC6's crossing is **vacuous** rather than uncovered, for the
reason given in its row.

Two crossings that might look like gaps are not. WI-0001 **AC1** and **AC2** have their own tests on
the unmarked `wide_chars.md`, but `test_wi0002_ac6_markers_and_display_width_together` asserts both
of their sentences — one display width per line, and equal column spans on every row including the
delimiter row — against `aligned_wide.md`, which carries `:-----`, `:---:` and `------:`. So a
committed test does exercise AC1 and AC2 with marked columns; it is simply not their own test.

For the three real non-intersections I **ran covering cases in this verification** rather than
inferring the verdicts — the commands and their actual output are in the AC5/AC7/AC8 rows above and
in `## Negative and boundary cases exercised`. Adding those cases to the **committed** suite is
**waived, by ID**:

- **WI-0001 AC5** — waived. WI-0002's `## Out of scope` puts "indentation" among the four things
  WI-0001 established and this item changes none of, and `item.md`'s R10 table records the indented
  crossing as "unconstrained by this item **on purpose**", because ADR-0003 re-emits the block's own
  prefix on every composed line and excludes it from the widths. A committed test would assert a
  structural independence the code makes unreachable, and would be maintained against this item
  rather than against the item that owns indentation.
- **WI-0001 AC7** — waived, same reason: "fenced blocks" is named in the same Out-of-scope clause,
  and `transform` copies a fenced line before candidacy is ever tested, so no marker code runs.
- **WI-0001 AC8** — waived, same reason: "Alignment inside anything that is not a well-formed
  table" is its own Out-of-scope bullet, and `table_or_none` short-circuits before
  `column_alignments` is reached.

The waiver is of a *committed regression test*, not of the check itself: each of the three was
exercised by hand in this run and passed.

## Negative and boundary cases exercised

Every one was triggered, not read about. All 21 exited 0 and were idempotent.

| # | case | result |
|---|------|--------|
| 1 | empty input | byte-identical |
| 2 | prose containing non-UTF-8 bytes `\xff\xfe`, no table | byte-identical |
| 3 | non-UTF-8 bytes **inside a marked table cell** | round-trips, `\| \xff\xfe \|` kept, idempotent |
| 4 | marked table with CRLF terminators | `\r\n` preserved on every composed line |
| 5 | marked table whose last line has no final newline | no newline gained |
| 6 | one empty cell in a left-, a right- and a centre-marked column | `W+2 = 5` spaces in each |
| 7 | every content cell empty, `:---` column | `W=0`, two spaces |
| 8 | every content cell empty, `---:` column | `W=0`, two spaces |
| 9 | every content cell empty, `:---:` column | `W=1` by ADR-0004, three spaces |
| 10 | centre marker, odd `W-w` | extra space to the right (`\| ab  \|`) |
| 11 | centre marker, even `W-w` | split evenly (`\|  ab  \|`) |
| 12 | centre marker, `W=1` | `\| Q \|` |
| 13 | blockquoted marked table | byte-identical |
| 14 | mismatched-indent marked block | byte-identical |
| 15 | ragged marked block (body row short a cell) | byte-identical, whole block |
| 16 | marked-looking block whose second row is not a delimiter row (`\| :x \| y: \|`) | byte-identical |
| 17 | delimiter cells `\|::\|::\|` — colons but no hyphen, so not a delimiter row | block copied whole |
| 18 | fenced block containing a marked table, plus a marked table outside | fenced lines byte-identical, outside table aligned |
| 19 | marked table with an escaped pipe `x\\\|y` in a cell | escape kept in the cell text, column widened to fit it |
| 20 | tab-padded cells in a marked table | tabs stripped as whitespace, cells composed with single spaces |
| 21 | two-row marked table (header and delimiter only, no body) | aligned, no crash |
| — | single-column tables under `:-`, `-:` and `:-:` | all three composed correctly |
| — | delimiter row longer than any content cell, marked | narrowed to `W+2`, colons kept |

## Test sensitivity check

Seven mutations of `mdtab.py`, applied one at a time and each reverted afterwards (`git status
--porcelain` empty at the end, and the file compared byte-for-byte to the original: `restored:
True`). The full suite was run under each.

| mutation | suite exit | criterion tests that failed |
|----------|-----------|------------------------------|
| M1 — `LEFT`/no-marker padding moved to the left | 1 | wi0002 AC1, AC2, AC3, AC4, AC5, AC6; wi0001 AC1, AC3, AC4, AC5, AC7 |
| M2 — `RIGHT` padding moved to the right | 1 | wi0002 AC1, AC2, AC3, AC4, AC5, AC6; wi0001 AC4 |
| M3 — odd centring remainder moved to the **left** | 1 | wi0002 AC1, AC2, AC3, AC4, AC6; wi0001 AC4 |
| M4 — `CENTRE` never detected (all markers fall through) | 1 | wi0002 AC1, AC2, AC3, AC4, AC6; wi0001 AC4 |
| M5 — ADR-0004's two-colon minimum width removed | 1 | wi0002 AC5, AC7; wi0001 AC4 |
| M6 — leading delimiter colon dropped | 1 | wi0002 AC1–AC8; wi0001 AC4, AC9 |
| M7 — `display_width` stops counting wide characters as 2 | 1 | wi0002 AC6; wi0001 AC1 |

Every criterion from AC1 to AC8 has at least one mutation that its own named test catches. **M3 is
the decisive one**: it is the single behaviour the stakeholder was asked about, and
`test_wi0002_ac3_centre_marker_puts_the_odd_space_on_the_right` fails under it.

**Two tests are insensitive to all seven mutations, correctly.**
`test_wi0002_ac9_…` and `test_wi0002_ac10_…` are coverage assertions about the *suite* — which
criterion tags exist, which fixtures are in `INPUT_FIXTURES` — so no change to `mdtab.py` can move
them. The AC9 test's own docstring says as much ("the verdicts themselves are `verify`'s to
record"), and the verdicts are in this report. `test_wi0001_ac2_…` is also insensitive to M1–M3, and
that is right: moving padding *within* a cell cannot change where the columns start.

## Defects found

**None.** No acceptance criterion of WI-0002 failed, so there is no send-back. No behaviour
delivered by another item was found broken, so no bug item was filed.

`found-in` therefore has no subject in this report.

## Observations

Neither is a criterion failure; both are recorded so `review-close` can decide whether either is
owed anything.

1. **`plan.md` step 2's "Afterwards" line carries AC3's illustration error.** It reads *"a centred
   column of width 3 holding `ab` composes as `\| ab  \|` and holding `Q` as `\| Q \|`"*. The first
   half is right; the second describes a width-**1** column — at width 3, `Q` composes as
   `\|  Q  \|`, which is what the filter does and what AC3's governing arithmetic requires. This is
   the same misreading `review-close` already adjudicated in AC3 itself, and `item.md`'s `## Notes`
   now records the resolution [src: commit e4dd5c6]. `plan.md` is an item artifact rather than a
   standing document, and no criterion depends on its "Afterwards" wording, so this verification
   does not treat it as a defect. `impl-report.md`'s AC3 row already states the arithmetic
   correctly (width 3 with `Q` → `\|  Q  \|`; width 1 with `Q` → `\| Q \|`).
2. **`impl-report.md`'s opening line is stale about the branch.** It says "three commits,
   `c64f374..a324868`" and the branch now carries twelve. The range it names is still the correct
   range for the *code and test* commits, and nothing downstream reads that line as a claim about
   the branch head — `Verified-commit` above is what pins the state. Recorded, not filed.

## Not verified, and why

- **That any markdown renderer agrees with the filter's output.** WI-0002's `## Out of scope`
  excludes it in as many words, and no criterion mentions a renderer. Nothing here establishes that
  a centred column *looks* centred in any particular viewer; every criterion compares bytes.
- **`commands.build`.** It is `null` in `tracker/project.yaml`, so there is no build gate to run.
  This is honest rather than skipped: the project has no build step. Nothing is left unchecked by it,
  because the deliverable is a single script that is not compiled.
- **Display width beyond the three classes ADR-0003 names.** The criteria define display width as
  the `east_asian_width` W/F rule, and I verified the filter against exactly that definition. I did
  **not** verify that the definition matches any real terminal — zero-width joiner emoji sequences,
  regional-indicator flags and `A` (ambiguous) width characters would all be counted differently by
  different terminals. WI-0001/Q-001 records the stakeholder accepting the approximation, so this is
  a known and accepted limit, not a gap this item opened.
- **Performance, memory, and very large inputs.** No criterion mentions any of them. The largest
  input exercised in this run was a 30-file fixture sweep; nothing was measured for time or space.
- **Behaviour under concurrent or interleaved invocation.** Not applicable to a stdin filter and not
  mentioned by any criterion.
- **The three waived committed regression tests** (WI-0001 AC5, AC7, AC8 crossed with markers). The
  behaviour *was* verified, by hand, in this run; what is not verified is that a **future** change
  would be caught by the suite. That is the exact cost of the waiver, stated so it is visible.
