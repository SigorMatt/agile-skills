# Verification report — WI-0001

Verified-commit: e0fd6b0026ed67acc630adb9747f99f9fad3b560

This is the **second** verification of WI-0001. `review-close` rejected the first delivery on D12
with four findings and returned the item to `in-progress`; `implement` closed all four and moved
it back to `verifying`. `check-verify-freshness` confirms why a second verification was owed:
"WI-0001 was verified at 175101a8 but code has changed since… `mdtab/scan.py`, `mdtab/table.py`,
`mdtab/textio.py`, `tests/fixtures/invalid-utf8.*.bin`, `tests/fixtures/tab-in-cell.*`,
`tests/test_fixtures.py`". So all fifteen criteria were re-checked from scratch against
`e0fd6b0`, and the four findings were checked as well.

Every document used below was written during this verification, under `.verify-scratch/`, and
none of them is a shipped fixture — a verification that re-runs the developer's own fixtures
checks that the code matches the fixtures, not that it matches the criteria. Display widths and
pipe columns were measured with an independent implementation of ADR-0002's three rules
(`unicodedata.category` / `east_asian_width`), written from the ADR and deliberately not
importing `mdtab.width`. The scratch directory was removed after the evidence below was
recorded; every command in this report reproduces from the inputs quoted in it.

## Verdict

**Pass — all fifteen criteria met. Moving to `in-review`.**

The tool is byte-exact where the criteria say it must be, aligns where they say it must, and
writes nothing to stderr. Twenty-two negative and boundary conditions were triggered, not read
about. Thirteen behaviours were deleted or inverted in turn and each deletion failed at least
one named test, so the suite is sensitive to the things it claims to protect.

Two things are recorded and neither is a criterion failure:

1. **AC12's own two clauses still contradict each other for one degenerate column.** This was
   raised by the first verification, accepted by `review-close` as a gap, and recorded in
   `item.md`'s `## Notes`; the code is right and AC12's *wording* is what should change. That
   amendment belongs to `answer-questions` and nobody has filed the question that would cause it
   to happen, so this execution filed it — `Q-005`, addressed to the architect and **non-blocking**,
   so the item is not suspended and `next` will run `answer-questions` before `review-close`.
2. **`impl-report.md` says "One fixture beyond the plan's list: `tab-prefix`" and there are
   three.** A documentation-accuracy defect in this item's own report, not a behaviour defect —
   see `## Defects found`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `printf 'Release notes\n…\n' > ac1.in.md; python3 -m mdtab < ac1.in.md > ac1.out.md 2> ac1.err` from the checkout root | `EXIT=0`, `stderr bytes: 0`, the whole document on stdout with its table aligned | the "Python 3 and nothing else installed" clause checked separately: `grep -rn '^import\|^from\|    import\|    from' mdtab/` → `unicodedata`, `sys`, `re` and intra-package imports only, no third party |
| AC2 | pass | independent width script over the output of four different laid-out documents: `python3 -m mdtab < ac23.in.md \| python3 vwidth.py` | `27 [0, 8, 17, 26]` on all five lines of the unicode table; `32 [0, 8, 18, 31]` on all four lines of the AC1 table; `23 [0, 11, 16, 22]` on the tab-in-cell table; `18 [0, 9, 17]` on the escaped-pipe table | every row of each table has one display width and its pipes sit at one set of display columns. The script measures with its own `unicodedata` implementation of ADR-0002 and skips escaped pipes when locating separators |
| AC3 | pass | the same script on a table holding `José` precomposed (U+00E9), `José` decomposed (`e`+U+0301), `表計算`, `Tōkyō`, `⚠️ warn` (U+FE0F), `😀` and fullwidth `ＡＢ` | `27 [0, 8, 17, 26]` for all five rows — identical to the ASCII case | the decomposed and precomposed spellings both measure 1 and land in the same column; the wide and fullwidth runs measure 2 each; the variation selector measures 0 |
| AC4 | pass | `diff <(sed -n '1,5p;10,11p' ac1.in.md \| od -c) <(sed -n '1,5p;10,11p' ac1.out.md \| od -c)` | no output — the seven non-table lines are byte-identical and in the same positions | a heading, a setext underline, two blank lines and two prose lines, on both sides of the table |
| AC5 | pass | `python3 -m mdtab < ac5.in.md > ac5.out.md; cmp ac5.in.md ac5.out.md` | `cmp` silent, exit 0 — byte-for-byte identical | the document holds a heading, a list, an indented code block, a blockquote and a prose line containing a bare `\|` |
| AC6 | pass | for each of 24 verification documents: `python3 -m mdtab < f \| md5sum` against `python3 -m mdtab < f \| python3 -m mdtab \| md5sum` | `fixed point:` on all 24, no mismatch | includes the degenerate `:-:` all-empty column, the bare-pipe table, the blockquote table and the undecodable-bytes document |
| AC7 | pass | `python3 -m mdtab < ac7.in.md > ac7.out.md; cmp ac7.in.md ac7.out.md` | `cmp` silent — all three come back byte-for-byte | one document holding an rst grid table (`+---+---+` / `+===+===+`), a raw HTML `<table>`, and a three-line run of pipe lines with no delimiter row |
| AC8 | pass | `cmp ac8.in.md ac8.out.md`, then a second document `ac8b` | `cmp` silent on `ac8`; on `ac8b` the only difference is the table *after* the closing fence, which was laid out | `ac8` holds a backtick-fenced ragged table, a tilde-fenced table, a fence inside a blockquote, and an unclosed fence running to the end — all untouched. `ac8b` proves the fence really closes: a ```` ```` ```` fence is not closed by ```` ``` ````, its contents stay untouched, and the table after the real close is aligned |
| AC9 | pass | `od -c` on the output of a CRLF document, of a document with no final newline, and of a document holding a `0xFF` byte | CRLF: every line ends `\r \n`, including the laid-out rows, and the `\r` never widened a column. No final newline: output ends `\| 2 \|` with no `\n`. `0xFF`: `\| 377 \|` survives and the table lays out around it | the undecodable input was asserted undecodable first — `'utf-8' codec can't decode byte 0xff in position 8` — so the case is not vacuous |
| AC10 | pass | the criterion's two exact examples: `printf '\| a \\\| b \|\n\|---\|\n\| 1 \|\n'` and `printf '\| a \\\\\| b \|\n\|---\|---\|\n\| 1 \| 2 \|\n'` | `\| a \\\| b \|` → **one** cell, laid out to `\| a \\\| b \|` / `\|--------\|`; `\| a \\\\\| b \|` → **two** cells, laid out to `\| a \\\\ \| b \|` / `\|------\|---\|` | odd backslash count escapes, even does not, exactly as AC10 states |
| AC11 | pass | a script that splits every row of input and output on unescaped `\|` with its own splitter and compares each cell after `strip(" ")`, on a table whose middle cell content is `\tspaced\t` and whose header cells carry uneven padding | `AC11 cell-content comparison: all equal after stripping spaces (U+0020) only` | the tabs survive in the output (`\| ^Ispaced^I \|` under `cat -A`), which is what makes the check non-vacuous — `str.strip()` would have eaten them. The delimiter row is excluded: AC12 is the specific rule for it and requires it be refilled |
| AC12 | pass | `python3 -m mdtab < ac12.in.md \| cat -A` on a table with an empty header cell, empty body cells and markers `:--`, `:-:`, `--:` | `\| a  \|    \| ccc \|` / `\|:---\|:--:\|----:\|` / `\|    \| bb \|     \|` / `\| xx \|    \| d   \|` | columns measure 4, 4, 5 against `2 + max` of 4, 4, 5; each content cell has exactly one space against each pipe; an empty cell is spaces; the delimiter cells keep `:` at exactly the ends they had. One exception, below |
| AC13 | pass | `cmp ac13.in.md ac13.out.md` on a run whose body holds a three-cell row and a one-cell row among two-cell rows | `cmp` silent — the whole run, prose either side included, is byte-for-byte | the *whole* run is left alone, not just the offending rows |
| AC14 | pass | a bare-pipe table (`a \| bb` / `--- \| ---` / `1 \| 2`), a mixed-style run, and a per-line `\|`-count comparison over all 19 verification documents | bare → `a \| bb` / `--\|---` / `1 \| 2 ` — laid out, still bare, no pipe added; mixed → `cmp` silent, byte-for-byte; pipe-count comparison → `pipe-count mismatches: none` on every document | the bare table's first cell keeps no leading space and its last keeps no trailing pipe, and AC2 still holds across its three rows (all width 6, pipe at column 2) |
| AC15 | pass | a blockquote table, a two-space list-indent table, a blockquote run with one row carrying an extra space after `>`, a run that starts unindented and continues indented, and a tab-vs-space prefix run | `> \| a \| bb \|` / `> \|---\|----\|` / `> \| 1 \| 2  \|` — laid out inside the prefix, `12 [2, 6, 11]` on every row; list-indent likewise; all three disqualified runs `cmp`-silent | the run that changes prefix part-way is reproduced **whole**, not split into a laid-out part and an untouched part, which is what AC15's last sentence requires |

### AC12's one exception, unchanged from the first verification

For a column whose header and body cells are **all empty** and whose delimiter marker is `:-:`,
AC12's "exactly `2 + max(display width of its cells)`" gives 2, and AC12's own next clause — "the
delimiter row's cells are filled with `-` to the same width, keeping any `:` at the ends they had"
— cannot be met at 2, because `::` is not a delimiter cell and a second run would not recognise
the table, failing AC6.

Triggered here rather than argued about:

```
$ printf '| a |  |\n|---|:-:|\n| b |  |\n' | python3 -m mdtab | cat -A
| a |   |$
|---|:-:|$
| b |   |$
$ printf '| a |  |\n|---|:-:|\n| b |  |\n' | python3 -m mdtab | python3 -m mdtab | cat -A
| a |   |$
|---|:-:|$
| b |   |$
```

The tool renders 3, which is the only width satisfying the delimiter clause and AC6 together.
`plan.md` decided this under `## Assumptions` before implementation, the first verification
confirmed it, and `review-close` accepted it as a gap and recorded that **AC12's wording is what
should change, not the code**, and that the amendment belongs to `answer-questions`. Nothing has
changed about the behaviour since, so the verdict is unchanged: AC12 passes, with this documented
exception. What has changed is that the amendment is now overdue — see `## Defects found`.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 55 tests in 0.077s`, `OK`, run by this skill on `e0fd6b0` |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, `checked 3 item(s), 8 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the `## Criteria` table above: every row names a command this skill ran against documents written for this verification, and quotes its actual output. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | 22 conditions triggered, listed below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | 13 mutations, listed below; every one failed at least one test |

## Negative and boundary cases exercised

Each of these was produced and its output inspected, not reasoned about.

1. An empty document (0 bytes in) → 0 bytes out, exit 0.
2. A document that is a single `\n` → a single `\n`.
3. A single line containing pipes, with nothing after it → untouched (a run needs two lines).
4. A three-line run of pipe lines with **no** delimiter row → byte-for-byte.
5. An rst grid table → byte-for-byte.
6. A raw HTML `<table>` → byte-for-byte.
7. A ragged table inside a backtick fence → byte-for-byte.
8. A table inside a tilde fence → byte-for-byte.
9. A table inside a fence that is itself inside a blockquote → byte-for-byte.
10. An unclosed fence at the end of the document → everything after it byte-for-byte.
11. A four-backtick fence containing a three-backtick line → not closed by the shorter fence.
12. A table immediately after a *closed* fence → laid out, proving the fence really closes.
13. A run whose rows disagree about cell count, one too many and one too few → whole run byte-for-byte.
14. A run whose rows disagree about outer-pipe style → byte-for-byte.
15. A blockquote run with one row carrying an extra space after `>` → byte-for-byte.
16. A run that starts unindented and continues indented → whole run byte-for-byte, not split.
17. A tab-indented row among space-indented rows → byte-for-byte.
18. A document whose lines end `\r\n` → `\r\n` preserved on every line, no `\r` inside a cell.
19. A document whose last line has no terminator → none added.
20. A document containing a `0xFF` byte, asserted undecodable under strict UTF-8 → byte preserved, table laid out around it.
21. A column whose header and body cells are all empty, marker `:-:` → the AC12 exception above, and idempotent.
22. Every one of the above checked for stderr → 0 bytes in all cases, per the epic's "not a linter" scope.

## Test sensitivity check

Thirteen behaviours were removed or inverted one at a time in the source, the suite re-run, and
the source restored with `git checkout -- mdtab/`. The mutator asserts the literal it is
replacing is actually present and exits non-zero if it is not — a `sed` that silently matches
nothing reports a false "the test is sensitive", and one did during this verification before the
assertion was added.

| criterion | mutation | result |
|-----------|----------|--------|
| AC2, AC3 | `display_width`: wide characters count 1 instead of 2 | 3 failures |
| AC2, AC3 | `display_width`: zero-width characters count 1 instead of 0 | 4 failures |
| AC6 | column width measured over the delimiter row's own cell too | 29 failures, `test_ac6_running_the_tool_on_its_own_output_changes_nothing` among them |
| AC7 | the "second line is a delimiter row" rule removed | 4 failures, incl. `test_rule_1_a_run_whose_second_line_is_not_a_delimiter_row` |
| AC7 | a run of one line accepted | 1 failure, `test_a_run_needs_at_least_two_consecutive_pipe_lines` |
| AC8 | the fence mask replaced by all-`False` | 3 failures |
| AC9 | `\r\n` recorded as `\n` | 4 failures |
| AC9 | a final unterminated line given a `\n` | 5 failures |
| AC10 | `split_row` ignores the backslash count | 6 failures, incl. `test_a_trailing_pipe_that_is_escaped_is_not_a_trailing_pipe` and `test_an_escaped_pipe_is_not_a_separator` |
| AC11 | `_TRIM = " "` → `_TRIM = None`, i.e. `strip(" ")` → `strip()` | 2 failures |
| AC12 | the delimiter minimum-width rule dropped | 2 failures, incl. `test_ac12_an_empty_cell_renders_as_spaces_between_the_pipes` |
| AC12 | cells given no padding | 46 failures |
| AC13 | the cell-count agreement rule removed | 1 failure, 6 errors, incl. `test_rule_3_…` |
| AC14 | the outer-pipe agreement rule removed | 5 failures, incl. `test_rule_4_…` |
| AC15 | the prefix-equality rule removed | 4 failures, incl. `test_rule_2_…` |

`git status --porcelain mdtab/ tests/` was empty afterwards, so the tree the gates ran against is
the committed one.

## The four review findings, re-checked

`review-close` rejected on these; this skill checked each independently rather than reading the
implementation report's claim about it.

| finding | check this skill ran | verdict |
|---------|----------------------|---------|
| 1 — a test built a document from a Python literal, against ADR-0005 | `grep -n 'b"' tests/test_fixtures.py`, then read `test_ac9_undecodable_bytes_survive_the_round_trip` in full | **closed** — the document comes from `read("invalid-utf8", "in")`. The only bytes literals left are assertions about the output (`\r\n` counts, `endswith`, a `\xff` count), which is not expressing a document. The test also asserts the fixture really is undecodable, so it cannot pass vacuously |
| 2 — the AC11 test was insensitive | the `_TRIM = " "` → `None` mutation above, run by this skill | **closed** — 2 failures. Independently, the AC11 evidence above uses a document with `\tspaced\t` in a cell and the tabs survive |
| 3 — the escaping rule expressed twice, `has_trailing_pipe` bypassing the splitter | read `mdtab/table.py` lines 57–69; ran the "split_row ignores the backslash count" mutation | **closed** — `has_trailing_pipe` now decides from `split_row(body)`'s last field; `_escaped_at` is gone (`grep -n _escaped_at mdtab/` → no match). Breaking `split_row`'s escaping now fails `test_a_trailing_pipe_that_is_escaped_is_not_a_trailing_pipe`, which is the drift the finding named |
| 4 — six signatures weaker than `plan.md` fixed them | read the six definitions | **closed** — `split_lines(text: str) -> list[tuple[str, str]]`, `join_lines(lines: list[tuple[str, str]]) -> str`, `split_row(content: str) -> list[str]`, `in_fence(contents: list[str]) -> list[bool]`, `find_runs(contents: list[str], fenced: list[bool]) -> list[tuple[int, int]]`, `lay_out(contents: list[str]) -> list[str] \| None` |

## The diff against the plan

`git diff --name-only main..HEAD` outside `tracker/` and `docs/`: `.gitattributes`,
`mdtab/{__main__,filter,scan,table,textio,width}.py`, `tests/test_fixtures.py`,
`tests/test_units.py`, and 23 fixture pairs. Every one maps to a numbered plan step, and nothing
in the code serves neither a criterion nor a step.

Three fixtures are not named in the plan's AC-to-evidence mapping: `empty-cells`, `tab-in-cell`
and `tab-prefix`. All three are legitimate additions that serve criteria the plan does map —
`empty-cells` is how plan step 10 requires AC12's empty-cell assertion to be expressed, since a
test may not build a document from a literal; `tab-in-cell` is finding 2's fix; `tab-prefix` is
declared as deviation 3. What is wrong is the report's arithmetic — see `## Defects found`.

## Defects found

Neither is a criterion failure, so neither is a send-back and neither is a bug item against
another item's delivered behaviour. Both are for `review-close`.

1. **`Q-005` filed: AC12's wording amendment is overdue.** *(process, not behaviour)*
   `plan.md`'s `## Assumptions`, the first verification report, `review.md`'s `## Accepted gaps`
   and `item.md`'s `## Notes` all say the same thing: AC12's arithmetic clause and its delimiter
   clause cannot both hold for an all-empty `:-:` column, the code is right, **the criterion's
   wording is what should change**, and the change belongs to `answer-questions`. No skill had
   filed the question that causes `answer-questions` to run, so the obligation could only have
   died when the item closed — with WI-0002 then built on AC12's arithmetic, which is precisely
   what `review.md` warned against. This execution filed
   `tracker/items/WI-0001/questions/Q-005.md`, addressed to the architect and **non-blocking**:
   the behaviour is settled, so nothing about WI-0001 is blocked, and the item continues to
   `in-review`. `next` step 4 dispatches `answer-questions` on an open architect question before
   step 5 dispatches `review-close`, so the amendment lands before the review that would close
   the item.
2. **`impl-report.md` overstates how much of the fixture set the plan named.** *(minor,
   documentation)* Its `## Deviations from the plan` says "**One fixture beyond the plan's list:
   `tab-prefix`**". Three fixtures are beyond the plan's mapping table: `empty-cells`,
   `tab-in-cell` and `tab-prefix`. `tab-in-cell` is declared elsewhere in the same report (the
   `### What this round changed` table, finding 2's row), so the practical gap is `empty-cells`,
   which no artifact declares. Reproduce with:

   ```
   $ for f in tests/fixtures/*.in.*; do n=$(basename "$f"); n="${n%%.in.*}"; \
       grep -q -- "$n" tracker/items/WI-0001/artifacts/plan.md || echo "NOT IN PLAN: $n"; done
   NOT IN PLAN: empty-cells
   NOT IN PLAN: tab-in-cell
   NOT IN PLAN: tab-prefix
   ```

   The fixture itself is right and is what plan step 10 asks for. It is raised because an
   undeclared deviation is exactly what got this item rejected the first time (finding 1), and
   because `review-close`'s D12 reads reports for accuracy. A one-sentence correction to
   `impl-report.md` closes it; it does not warrant a send-back, since no criterion is affected
   and no behaviour is in question.

## Not verified, and why

- **The CPython 3.8 floor `plan.md` sets.** Only CPython 3.12.3 is installed here
  (`python3 -V`), so no run can prove the code works on 3.8. Unchanged from the first
  verification and from `review.md`'s accepted gap 2; this execution did not re-inspect for it,
  because `review-close` already read for it and nothing in `mdtab/` changed this round except
  annotations and one function body.
- **How a terminal or an editor actually draws the output.** AC2 and AC3 are met against
  ADR-0002's rule, which is what they name. Whether a given terminal draws an emoji ZWJ sequence
  or an ambiguous-width character the way ADR-0002 counts it is outside anything a command here
  can settle; ADR-0002 records the limitation and it is unchanged.
- **The shipped fixtures' expected outputs were not independently re-derived.** The suite asserts
  the code reproduces them and this report's evidence comes from documents written here instead,
  so a fixture whose hand-written expected output is wrong in a way none of the fifteen criteria
  detect would not be caught by either. `review-close` read them hunk by hunk in the first cycle
  and no fixture's expected output changed this round, which bounds the risk rather than removing
  it.
- **Concurrency, large inputs and pathological documents** — no criterion mentions them and none
  was tried. The largest document run through the tool during this verification was 27 lines.
