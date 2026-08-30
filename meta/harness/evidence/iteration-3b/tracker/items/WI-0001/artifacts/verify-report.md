# Verification report — WI-0001

Verified-commit: c1c79dc2639eab98a3e0d9ffce631c996e50ad2d

Branch `wi/WI-0001`, working tree clean at the time of verification.

## Verdict

**Pass.** All eleven acceptance criteria are met. Every verdict below rests on a command this
skill ran against inputs **it wrote itself**, not on the project's fixtures and not on
`impl-report.md`. Where a criterion needed a display-width measurement, it was taken with
`/tmp/vwi1/w.py`, a nine-line function written from the item's own preamble — *"2 for a character
whose `unicodedata.east_asian_width` is `W` or `F`, 0 for a combining mark, 1 otherwise"*
[src: WI-0001] — and deliberately **not** by importing `mdtab.display_width`, which would have
made AC1 and AC2 tautologies.

One thing `review-close` must read before it reads AC4: **AC4's sentence, taken alone, does not
describe this code, and that is correct.** See `## AC4 read against the item's own scope` below.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `printf '\| Region \| Lead \| Flag \|\n\|-\|-\|-\|\n\| 東京 \| Rene<U+0301>e \| 🎉 \|\n\| Oslo \| Bo \| - \|\n' \| python3 mdtab.py`, then each output line measured with the independent width function | input line widths `24, 7, 21, 17`; output line widths `25, 25, 25, 25` for `\| Region \| Lead  \| Flag \|` / `\|--------\|-------\|------\|` / `\| 東京   \| Reńee \| 🎉   \|` / `\| Oslo   \| Bo    \| -    \|` | my own table, not the project's fixture. `東` and `京` are `east_asian_width` `W`, `🎉` is U+1F389, `Reńee` is `Rene` + U+0301 + `e`. The input rows genuinely differed in width, so the criterion could not pass vacuously |
| AC2 | **pass** | display-column offset of every `\|` on each line of that same output, via `/tmp/vwi1/off.py` | `[0, 9, 17, 24]` on all four rows, delimiter row included | every column occupies the same span on every row |
| AC3 | **pass** | `printf '\|   Padded   \|Tight\|  \|\n\|---\|---\|---\|\n\|\ta\t\|b\|   \|\n' \| python3 mdtab.py \| cat -A` | `\| Padded \| Tight \|  \|$` / `\|--------\|-------\|--\|$` / `\| a      \| b     \|  \|$` | leading and trailing whitespace stripped (spaces **and** tabs), one space either side, empty cell is a pipe and exactly two spaces. `grep -nP '[ \t]$'` over the output found **none** — no composed line ends in a space or a tab |
| AC4 | **pass** | `printf '\| ab \| c \|\n\|------------------\|-\|\n\| d \| e \|\n' \| python3 mdtab.py \| cat -A` | `\| ab \| c \|$` / `\|----\|---\|$` / `\| d  \| e \|$` | width 2 → 4 hyphens, width 1 → 3 hyphens, no spaces, closed by a final pipe. The 18-hyphen input run **narrowed** to 4: the delimiter row did not contribute to the column's width. See the section below for a delimiter cell that carries a marker |
| AC5 | **pass** | four separate runs: a 4-space indent under `10. `; a tab indent; a block whose lines' indents differ; a block whose lines each begin with `> ` | indented: `    \| Key   \| V \|` / `    \|-------\|---\|` / `    \| alpha \| 1 \|` — tidied, all three lines starting with the same four spaces. Tab-indented: `^I\| a \| bb \|$` etc. Mismatched indent: `cmp` → **identical**. Blockquote: `cmp` → **identical** | all four clauses of the criterion, each with its own input |
| AC6 | **pass** | six inputs I wrote — empty (0 bytes), prose with a pipe and trailing spaces, no final newline, CRLF, invalid UTF-8 (`\x80 \xfe \xc3\x28 \xed\xa0\x80`), lone-CR line endings — each `cmp`'d against the filter's output | `byte-identical, exit 0` for all six; `md5sum` on the invalid-UTF-8 pair both `2b51efba8923e9b7de78472141951224` | the lone-CR case is beyond what the criterion names and is reported as extra assurance |
| AC7 | **pass** | a document with prose, a heading, a 4-backtick fence of pipe lines, a 5-tilde fence of pipe lines, one real table and tail prose → `diff -u` input against output | the diff touches **only** the real table's two lines (`\|-\|------\|` → `\|-----\|------\|`, `\| c \| d \|` → `\| c   \| d    \|`); every other line unchanged; `wc -l` 20 in, 20 out | also checked the fence-length boundary: a 3-backtick line inside a 4-backtick fence does **not** close it — that whole file came back `cmp`-identical |
| AC8 | **pass** | five malformed blocks I wrote: no delimiter row; a short body row among well-formed ones; a delimiter row with the wrong cell count; a delimiter row with a non-delimiter cell (`\|--- \| x \|`); a single-line block | `cmp` → byte-identical for all five | the well-formed row `\| 33333 \| 44444 \| 55555 \|` is still exactly as written in the output of the second case — the block was not partly tidied |
| AC9 | **pass** | the filter run on its own output for **22** inputs (every input above, plus the marker and degenerate cases), `cmp` of the second output against the first | `idempotent` on all 22 | includes the marked-delimiter and empty-two-colon-column cases, which are the ones most likely to produce output the recogniser would reject |
| AC10 | **pass** | the same 22 inputs, exit status recorded on both passes | `exit 0/0` on all 22; stderr empty | includes the 0-byte input and the invalid-UTF-8 input |
| AC11 | **pass** | `tests/test_mdtab.py` parsed with `ast` and its methods enumerated **from source**, then `python3 -m unittest discover -s tests -t .` | 14 methods; for each of AC1 to AC10 exactly one method carries that criterion's tag and quotes the criterion in its docstring — `AC1 -> OK` through `AC10 -> OK`, no gaps and no duplicates. Suite: `Ran 14 tests in 2.4s ... OK`, exit 0 | see `## A criterion whose subject is other criteria` |

Every criterion above is now ticked in `item.md`.

## AC4 read against the item's own scope

AC4 says the delimiter row is *"for each column, `|` followed by (that column's width + 2) hyphens
and no spaces"* [src: WI-0001 AC4]. Run against a table whose delimiter row carries alignment
markers, the code does something else:

```
$ printf '| Left | Middle | Right |\n|:---|:--:|---:|\n| a | b | c |\n' | python3 mdtab.py
| Left | Middle | Right |
|:-----|:------:|------:|
| a    | b      | c     |
```

This was checked rather than assumed, and the verdict is **pass**, for reasons in the record and
not in the code:

1. The item's own `## Out of scope`, in the same file as the criterion, scopes it: *"This item may
   leave marker characters in place unchanged, and AC4's hyphen rule describes a delimiter cell
   that carries no marker."* [src: WI-0001]
2. [src: ADR-0003] decision 10 says the same: *"Alignment markers are WI-0002's subject and are
   out of scope here; this rule describes a delimiter cell that carries no marker."*
3. [src: ADR-0004] decides the composition rule and why the literal reading was rejected.
4. **The stakeholder's own question was explicitly about a markerless row.** `Q-004`'s `## Context`
   reads: *"What is being asked here is only the appearance of a delimiter row that carries no
   marker at all."* Their answer — *"Dashes all the way across, pipe to pipe. That row is a rule
   under the header, not a row of content"* [src: WI-0001/Q-004] — is about that row and says
   nothing about markers.

So this is not two criteria contradicting each other on the page; it is a criterion and its own
scope statement, written by the same skill in the same document, and the stakeholder's recorded
answer is consistent with both. No question was filed, because the record settles it in four
places — and the reading was **not** chosen because it makes the code pass: the markerless case,
which is AC4's actual subject, was verified separately and independently in the table above.

`review-close` should nonetheless treat this as the most likely way this item is wrongly rejected,
which is what `plan.md`'s `## Risks` says too.

## A criterion whose subject is other criteria

AC11's subject is AC1 to AC10. It names them by ID, so it is decidable. Per-criterion verdict,
read from `tests/test_mdtab.py`'s source rather than inferred from a green suite:

| covered criterion | is there a test naming it? | verdict |
|---|---|---|
| AC1 | `test_ac1_every_table_line_has_the_same_display_width`, docstring quotes AC1 | true |
| AC2 | `test_ac2_every_column_starts_at_the_same_display_offset` | true |
| AC3 | `test_ac3_cells_carry_one_space_either_side` | true |
| AC4 | `test_ac4_delimiter_row_fills_its_column` | true |
| AC5 | `test_ac5_indent_is_restored_byte_for_byte` | true |
| AC6 | `test_ac6_no_table_is_byte_identical` | true |
| AC7 | `test_ac7_fenced_pipe_lines_are_left_alone` | true |
| AC8 | `test_ac8_malformed_block_is_copied_whole` | true |
| AC9 | `test_ac9_running_the_filter_on_its_own_output_changes_nothing` | true |
| AC10 | `test_ac10_exit_status_is_zero` | true |

The suite passing is **evidence for** that table, not its definition: the table was built by
parsing the file, and a green suite would have said nothing about whether a method named for AC3
tests AC3. That second question was answered by the sensitivity check below, which disables each
behaviour in turn and watches the criterion's own test fail.

**Non-intersection:** none to declare. There is something executable that exercises AC11 together
with the criteria it covers — `SuiteCoverageTest.test_ac11_each_criterion_has_a_named_test`
re-derives the same mapping at run time — and it was confirmed sensitive (mutation M11 below).

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 14 tests in 2.409s ... OK`, run by this skill on branch head `c1c79dc` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, `checked 3 item(s), 6 document(s)`, 0 errors 0 warnings |
| `every-criterion-independently-checked` | **pass** | the Criteria table above records, for all eleven, a command this skill ran and its actual output. No row cites `impl-report.md`. Every input in it was written by this skill; the project's own fixtures were not used as evidence for any verdict |
| `negative-cases-exercised` | **pass** | see the section below — 0-byte input, invalid UTF-8, five malformed blocks, three whitespace-boundary cases, two degenerate tables, unexpected arguments, and a fence-length boundary, each triggered and its output recorded |
| `a-criterion-about-criteria-is-read` | **pass** | AC11's covered criteria named by ID with a per-criterion verdict read from source; non-intersection considered and explicitly none |
| `tests-would-fail-without-the-change` (advisory) | **pass** | eleven mutations, one per criterion, each confirmed to fail that criterion's own test — see below |

## Negative and boundary cases exercised

| case | command | what happened |
|------|---------|---------------|
| empty input (0 bytes) | `python3 mdtab.py < /dev/null` | no output, exit 0 |
| bytes that are not valid UTF-8 | `printf 'bytes: \x80\xfe\xc3\x28 \xed\xa0\x80 done\n...'` through the filter | byte-identical, same md5, exit 0 |
| last line with no terminator | `printf 'last line has no newline'` | byte-identical; and a **table** as the last line with no newline came back tidied with no newline invented |
| CRLF, and lone CR | two files | both byte-identical; a CRLF **table** came back tidied with `^M$` on every composed line |
| five malformed pipe blocks | see AC8 row | all five copied whole |
| indent that differs between lines | `printf '\| a \| bb \|\n  \|---\|---\|\n\| c \| d \|\n'` | byte-identical — no block of two or more forms |
| blockquoted table | `printf '> \| a \| bb \|\n> \|---\|---\|\n...'` | byte-identical |
| tab-indented table | `printf '\t\| a \| bb \|\n\t\|-\|-\|\n...'` | tidied, tab restored |
| escaped pipe inside a cell | `printf '\| a \\\| b \| c \|\n\|-\|-\|\n\| d \| e \|\n'` | `\|` kept as cell content, column widened to 6 to hold it — the plan's assumption, confirmed |
| row ending in an **escaped** pipe | `printf '\| a \| b\\\|\n\|-\|-\|\n'` | not a candidate; both lines copied unchanged |
| unexpected command-line arguments | `python3 mdtab.py --nonsense -x` | arguments ignored, table still tidied, exit 0, stderr empty — the plan's assumption, confirmed |
| single-column table | `printf '\| a \|\n\|---\|\n\| bbbb \|\n'` | tidied to width 4 |
| two adjacent tables one blank line apart | one file | both tidied independently, blank line preserved |
| fence-length boundary | 3-backtick line inside a 4-backtick fence | does not close the fence; whole file byte-identical |
| header row that itself looks like a delimiter row | `printf '\|---\|---\|\n\|---\|---\|\n\| a \| b \|\n'` | treated as a table with header text `---`; output `\| --- \| --- \|` / `\|-----\|-----\|` / `\| a   \| b   \|`, and idempotent. Renders the same as the input; not a defect under [src: ADR-0003] decision 3 |
| degenerate one-column table of empty cells (`\|\|`) | `printf '\|\|\n\|-\|\n\|\|\n'` | `\|  \|` / `\|--\|` / `\|  \|`, idempotent |
| empty column whose delimiter carries two colons | `printf '\| x \|  \|\n\|:-:\|:-:\|\n\|  \|  \|\n'` | `\|:-:\|:-:\|` — the minimum width of 1 holds, so the output is still recognised on the next run. [src: ADR-0004] decision 2, confirmed by triggering it |

## Test sensitivity check

Eleven mutations were applied to the branch head one at a time, the suite re-run against each, and
the working tree restored (`git status --short` empty afterwards, suite green again). Every
criterion has at least one test that fails when its behaviour is removed.

| # | mutation | criterion's own test failed? | total failing |
|---|----------|------------------------------|---------------|
| M1 | `emit_block` copies instead of composing | AC1–AC5, AC7 all failed | 7 |
| M2 | `column_widths` measures `len()` instead of display width | `test_ac1_…` **and** `test_ac2_…` failed | 2 |
| M3 | `compose_row` drops the framing spaces | `test_ac3_…` failed | 7 |
| M4 | `compose_delimiter` emits spaces instead of hyphens | `test_ac4_…` failed | 6 |
| M5 | `emit_block` drops the block's indent prefix | `test_ac5_…` failed | 1 |
| M6 | `main` returns 1 | `test_ac10_…` failed | 45 |
| M7 | edge decoding uses `errors="replace"` instead of `surrogateescape` | `test_ac6_…` failed | 1 |
| M8 | fence state ignored | `test_ac7_…` failed | 1 |
| M9 | the cell-count consistency check removed | `test_ac8_…` failed | 4 |
| M10 | an extra `\|x\|` line appended to every composed table | `test_ac9_…` failed | 8 |
| M11 | one test method renamed so it no longer carries its AC tag | `test_ac11_…` failed | 1 |

M2 is worth naming: it is precisely the tautology `plan.md`'s `## Risks` warned AC1 could hide, and
it fails, so AC1 and AC2 are measuring something the code could get wrong.

## Diff read against the plan

`main..c1c79dc` is 32 files. `mdtab.py` and `tests/` are plan steps 1 to 9; the 26 fixture files
are step 8; `docs/architecture/overview.md` v2 is the D12 repair the implementation declared; the
rest is this item's own tracker record.

`mdtab.py` defines 15 functions. Eleven are named in `plan.md`'s `## Approach`; the four that are
not — `strip_terminator`, `_is_escaped`, `emit_block`, `transform` — are each required by prose in
that same section (the inverse of `split_lines`; *"a `|` … not preceded by an odd number of
backslashes"*; *"a single left-to-right scan"*; the block-emission rules). **No behaviour was found
that no criterion and no plan step accounts for**, and no unrequested feature: there is no
argument parsing, no file I/O by path, no configuration, no logging and no output on stderr, all
of which the item's `## Out of scope` forbids.

## Defects found

**None.** No criterion of this item failed, so there is no send-back; no behaviour delivered by
another item failed, so no bug item was filed. WI-0001 is the first item in this project and no
other item has delivered anything yet.

One thing was found that is **not** a defect in this item and is recorded rather than filed: the
pipeline's own `.claude/agile-skills/scripts/validate-workspace` and `scripts/lint-claims` crash
with an uncaught `UnicodeDecodeError` on any non-UTF-8 `*.md` file in the repository. The
implementation hit this and worked around it by naming the fixture `not_utf8.markdown`; this skill
confirmed the workaround holds — `validate-workspace` exits 0 on the branch head. No `bug` item
was filed because a bug in this tracker is filed against behaviour an **item** delivered, and no
item owns the toolkit's scripts. It belongs to whoever maintains agile-skills.

## Not verified, and why

- **How the output looks in the stakeholder's actual terminal.** Every width judgement here uses
  `unicodedata`, which is what the criteria define display width to mean. The stakeholder accepted
  in advance that a rare emoji may be off by one somewhere [src: WI-0001/Q-001]. Not checkable
  from this session, and not a criterion.
- **Alignment inside a table in a document that is not valid UTF-8.** A surrogate-escaped byte
  counts as one display column, so a table's columns may not line up there. `plan.md`'s `## Risks`
  names this, no criterion covers it, and the passthrough promise is unaffected — which *was*
  verified (AC6). Left unverified deliberately.
- **A pipe table inside an *indented* code block is tidied.** Triggered and confirmed via AC5's
  indented case, which is the same code path. It is accepted behaviour, not a defect
  [src: ADR-0003] decision 2 and WI-0001's `## Out of scope` — so it is recorded here rather than
  as a finding.
- **Behaviour under an argument that names a file**, or under a closed stdin. No criterion covers
  either; arguments are specified as ignored, which was exercised.
- **Performance on a large document.** No criterion mentions it and nothing was measured.
