# Implementation report — WI-0004

## What was built

Two changes, on `wi/WI-0004`, in the plan's order.

**`mdtab/inline.py` (new, 97 lines).** One public function, `contains_line_break(text)`, plus the
private code-span scan it needs. It answers whether a cell's text holds an HTML `br` tag that
begins outside every code span: the tag pattern is `<`, `br` in either case, then `>` at once or
one of space, tab or `/` and any run up to the next `>`; a code span is a run of *n* backticks
closed by the next run of exactly *n*, and a run with no matching closer is literal text. Nothing
else about markdown is modelled, and nothing on the recognition path calls it.

**`mdtab/table.py` (+20 lines, −2).** `_render_row` now passes `"left"` to `_render_cell` in place
of `alignments[column]` when the cell's stripped text contains a line break, and the column's own
alignment otherwise. `column_alignments`, `_column_widths`, `_render_cell` and `_render_delimiter`
are unchanged, so widths, guard spaces and markers are as WI-0002 left them.

**Tests (+113 lines in `tests/test_units.py`, +8 in `tests/test_fixtures.py`, four new fixture
files).** `LineBreakTest` drives the detection rule directly; `LineBreakPlacementTest` asserts
whole laid-out documents through `lay_out`; two fixture pairs put the rule into whole documents
and, by being registered in `ALIGNED`, into the four document-level invariant classes.

**`docs/architecture/overview.md` v8 → v9.** Plan step 7: the four sentences saying this design was
"Planned for WI-0004, not yet in the code" were true when `plan` wrote them and false once the code
landed, so they are gone. Nothing else about v8's description changed.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — any spelling of the tag outside a code span puts the cell left | `contains_line_break` matches all five spellings; `_render_row` overrides the column's alignment for that cell | `tests.test_units.LineBreakTest.test_every_spelling_ac1_names_counts` (7 texts, including `<br>`, `<BR>`, `<br/>`, `<br />`, `<br class="k">`); `LineBreakPlacementTest.test_ac1_a_break_cell_sits_left_in_a_centred_column` and `…_in_a_right_aligned_column`. Both AC1 transcripts re-run: `printf '\| heading is long \| b \|\n\|:---:\|---:\|\n\| a<br>b \| x \|\n' \| python3 -m mdtab` → last row `\| a<br>b          \| x \|`, and the same under `---:` → the same row, each matching what AC1 requires. The four-spelling transcript now returns `\| a<BR/>b          \| x \|`, `\| c<br />d         \| y \|`, `\| e<br class="k">f \| w \|` — each flush left with its padding after it |
| AC2 — the delimiter row's marker is unchanged | the delimiter row leaves `_render_row` through the other branch and never reaches the override | `LineBreakPlacementTest.test_ac2_ac3_only_the_row_with_the_break_moves` asserts the whole document, delimiter row `\|:------------:\|--:\|` included; the AC1 transcripts come back with `:---------------:` and `----------------:` as before; `tests.test_fixtures.LayoutShapeTest.test_ac12_the_delimiter_row_keeps_its_colons_and_fills_the_column` unmodified and passing |
| AC3 — only the cell with the break moves | the override is decided per cell inside the row loop; no column-level state exists | `LineBreakPlacementTest.test_ac2_ac3_only_the_row_with_the_break_moves`: a centred column of three body rows returns `\|      aa      \|`, `\| a<br>c       \|`, `\|      bb      \|` — the first and third centred exactly as today, the middle one flush left, the column 14 wide in all three. The `line-break-cells` fixture repeats it with a real document (`\|      plain       \|` between break cells) |
| AC4 — idempotence, non-table lines, silence, exit 0 | nothing outside the renderer changed, and the override reads only the cell's own text | each of the five documents named in AC1, AC6 and AC7 run through the tool: `exit=0`, `stderr=0 bytes`, and running the tool on its own output produces the same bytes (`twice-vs-once=same`, five times). Both new fixtures likewise. `tests.test_fixtures.FixtureRoundTripTest.test_ac6_running_the_tool_on_its_own_output_changes_nothing` and `test_ac4_lines_outside_a_table_are_untouched_in_the_fixtures_that_have_one` now run over both new documents — the prose lines either side of `line-break-cells`' table are what the second one reads. Also `LineBreakPlacementTest.test_ac4_a_laid_out_table_with_a_break_is_a_fixed_point` at the `lay_out` level |
| AC5 — the suite passes and no existing test changes | new tests were added; none was edited | `python3 -m unittest discover -s tests -t .` → exit 0, **84 tests, OK** (72 before). `git diff --numstat main..HEAD -- tests/test_units.py tests/test_fixtures.py` → `8 0` and `113 0`: **no line removed from either file**, so none of the twenty tests AC5 names is altered, and `git diff main..HEAD -- tests/ \| grep -E '^-[^-]'` returns nothing. `tests/test_fixtures.py`'s eight added lines are the two `ALIGNED` entries and their comments — the diff is quoted below |
| AC6 — a header cell with a break sits left too | the header is an ordinary non-delimiter row and needs no clause | `LineBreakPlacementTest.test_ac6_a_header_cell_with_a_break_sits_left_too`; the AC6 transcript re-run returns `\| a<br>b         \| second column \|`, exactly the row AC6 requires, with the rest of the table unchanged; the `line-break-cells` fixture's header is `\| what<br>it is    \|` |
| AC7 — a tag inside a code span is not a break | code spans are found first and a tag beginning inside one is not counted | `LineBreakTest.test_ac7_a_tag_inside_a_code_span_is_the_author_showing_it`, `…_a_multi_backtick_span_holds_its_tag`; `LineBreakPlacementTest.test_ac7_a_cell_showing_the_tag_still_obeys_its_marker`; the `line-break-code-span` fixture. The AC7 transcript comes back **byte-for-byte identical** to the shipped tool's output: `\|          `<br>` \| x \|` |

The three cases WI-0004 left unconstrained are decided by ADR-0010 §3 and each has its own test:
`test_an_unbalanced_backtick_opens_nothing` (left), `test_a_multi_backtick_span_holds_its_tag`
(marker), `test_a_tag_inside_a_span_and_another_outside_it_counts` (left).

`git diff main..HEAD -- tests/test_fixtures.py`, in full — the only change to a file AC5 wants
left alone:

```diff
@@ -80,6 +80,14 @@ ALIGNED = {
     "invalid-utf8": (2, 5),
+    # A break in the header and in three body cells, spelled four ways, in a
+    # centred column beside a right-aligned one — and one row with no break, to
+    # show that it is the cell rather than the column that declines the marker
+    # (WI-0004 AC1, AC3, AC6). The prose either side is what AC4 is read over.
+    "line-break-cells": (2, 8),
+    # The other half of the same rule: cells that only *show* the tag, in single
+    # and double backticks, go on obeying `---:` (WI-0004 AC7).
+    "line-break-code-span": (0, 4),
     "list-indent-table": (2, 5),
```

## Deviations from the plan

1. **How a span is excluded from the search.** The plan and ADR-0010 §2 say code spans are found
   first and "excluded from the search". Implemented as: find the spans, then take a tag match
   only when its **start index** lies outside every span. The alternative reading — blank the
   spans out of the text and search the result — differs on one shape only, a tag that *begins*
   outside a span and *ends* inside one (`<br` + a span + `>`), which blanking would turn into a
   match and this does not. Every case AC1, AC7 and ADR-0010 §3 name answers identically either
   way, and not inventing a match out of characters the author did not write in that order is the
   safer of the two. No criterion distinguishes them.
2. **One test beyond the plan's step 4 list.**
   `LineBreakPlacementTest.test_ac4_a_laid_out_table_with_a_break_is_a_fixed_point` — the plan
   maps AC4 to the fixtures alone. It costs three lines and puts idempotence next to the rule that
   could break it, which is where a later reader will look.
3. **The plan's step 5 asked for "a row with no break in the same columns"** in
   `line-break-cells`; the fixture has one (`plain`), and it is centred, which is what makes the
   fixture demonstrate AC3 as well as AC1.

Nothing else departs from the plan. The plan's seven steps were executed in order, and the two
files the plan named as the only production changes are the only production files touched.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, 84 tests, OK, run on the branch head |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 6 items, 12 documents |
| `every-criterion-has-a-test` | **pass** | the table above: every AC names test functions, or exact commands with their output; none is satisfied by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, "all 3 commit(s) on main..wi/WI-0004 name WI-0004" (four with the report commit) |
| `no-unplanned-scope` | **pass** (advisory) | `git diff --stat main..HEAD`: `mdtab/inline.py` (plan step 1), `mdtab/table.py` (step 2), `tests/test_units.py` (steps 3–4), four fixture files and `tests/test_fixtures.py` (step 5), `docs/architecture/overview.md` (step 7). No other file, and no hunk that is not one of those steps |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, 1 document |

## What I did not do

- **Nothing in the plan was left undone.** All seven steps landed.
- **`grep -rniE '<br' tests/` no longer exits 1** — it now matches 33 lines, which are the new
  tests and fixtures. AC5 quotes that command as evidence that no *existing* expectation is about
  a document this rule reaches, and that was true of the trunk; on this branch the evidence for
  AC5 is the diff quoted above, which is what the plan's risk 3 said to expect. Nothing about the
  trunk's tests changed.
- **No CommonMark refinement of the code-span rule.** A span's content is not stripped of a
  leading and trailing space, and a backslash does not escape a backtick, per ADR-0010 §2 and the
  plan's assumption 3. Neither changes any answer this item needs.
- **No diagnostic, no flag, no README.** Out of scope for the item and declined as work by the
  stakeholder in EP-001/Q-004.
- **No bug filed against another item.** Nothing in the existing behaviour looked wrong while
  working here.

---

# Second execution — the send-back remedy, 2026-08-29T08:05Z

`review-close` rejected the item at 08:04:33Z on Definition of Done D7 and D12 and returned it to
`in-progress` (`artifacts/review.md`, finding 1). Everything above stands: it describes the first
execution and is still true of it. This section reports only the defect that was sent back.

## What was built (second execution)

**No production code changed.** `git diff --stat dff7600..HEAD` touches `docs/product/vision.md`
and files under `tracker/` and nothing else, so the code `verify` passed at `dff7600` is
byte-for-byte the code on this branch head.

**`docs/product/vision.md` v8 → v9.** Two false claims, not one.

1. **The one the review named.** `## Open at the time of writing` described this item's behaviour
   as outstanding in four places — *"One behaviour is wanted and is not built"*, *"Today mdtab does
   not know a cell can contain a line break … under `:---:` it is centred and under `---:` it is
   pushed right"*, *"filed as [src: WI-0004], at `ready`"*, and *"The behaviour is still wanted and
   still not built"*. The section now opens with the behaviour built, shows it with a transcript,
   records what the tool used to do as the past rather than the present, and states that what is
   open is the stakeholder's acceptance rather than any behaviour.
2. **A second one, found while fixing the first, in the same document.** The `## What it does`
   section read: *"The alignment markers in a delimiter row are honoured in every column without
   exception: 'Whatever the marker says, that's where the text sits in the cell — every row, every
   column, no exceptions' [src: WI-0002/Q-001]."* A cell holding a `br` tag is precisely an
   exception to that sentence, so this item made it false too. The paragraph now keeps
   `WI-0002/Q-001`'s words as what the stakeholder asked for first and what mdtab does for every
   ordinary cell, and carries the one exception they asked for afterwards
   [src: WI-0004 AC1; src: ADR-0010].

This is the same document, the same section and the same two Definition of Done criteria that
sent WI-0003 back — `vision.md`'s own v5 change-log row ends *"Sent back by review-close on D7 and
D12"*. It is recorded here because a pattern that has now cost two send-backs on the same document
belongs in the record rather than in a reviewer's memory.

## Acceptance criteria evidence (second execution)

No acceptance criterion of this item changed and none was touched. AC1–AC7 are satisfied exactly
as the table above records, by the same code at the same commit; `verify` re-measures them. The
work of this execution is documentation, which D7 and D12 gate rather than any AC.

Two commands were run to make sure the document does not now assert something else untrue:

| claim written | command | actual output |
|---------------|---------|---------------|
| the v9 transcript of what mdtab does now | `printf '\| heading is long \| b \|\n\|:---:\|---:\|\n\| a<br>b \| x \|\n' \| python3 -m mdtab` on the branch head | `\| heading is long \| b \|` / `\|:---------------:\|--:\|` / `\| a<br>b          \| x \|`, exit 0 — byte-for-byte what v9 shows |
| the two "before" rows, `\|     a<br>b      \| x \|` under `:---:` and `\|          a<br>b \| x \|` under `---:` | the same two documents through a `git archive main` copy of the trunk in a scratch directory | exactly those two rows — the past tense in v9 is measured against the trunk, not remembered |

## Deviations from the plan (second execution)

1. **This work is not in `plan.md`.** The plan's step 7 named `docs/architecture/overview.md` and
   no other document, and the first execution carried it out exactly. `docs/product/vision.md` was
   invalidated by the same change and no step named it. Nothing about *what* is delivered changed —
   no code, no criterion, no interface — so this was executed rather than escalated as a question;
   it is the Definition of Done's D7 applied to a document the plan did not enumerate.
2. **Two claims fixed, where the review named one.** The review's finding 1 named
   `## Open at the time of writing`. The `## What it does` sentence was found while editing the
   same file and is false for the same reason. Leaving it would have failed D12 at the next review
   and, worse, would have left the contradiction in the section a stakeholder reads first.

## Gates (second execution)

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` on the branch head → exit 0, `Ran 84 tests … OK` |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 6 items, 12 documents |
| `every-criterion-has-a-test` | **pass** | unchanged from the first execution — the table above names a test function or an exact command for each of AC1–AC7, and no criterion's evidence moved, because no code moved |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, "all 8 commit(s) on main..wi/WI-0004 name WI-0004" |
| `no-unplanned-scope` | **pass** (advisory) | `git diff --stat dff7600..HEAD` → `docs/product/vision.md` and `tracker/` only. The single production-adjacent hunk set is the document D7 requires; there is no code hunk at all |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, 2 documents (the second being `vision.md`, newly changed) |

## What I did not do (second execution)

- **I did not touch the code, a test, a fixture or an acceptance criterion.** `git diff
  dff7600..HEAD` contains no hunk under `mdtab/` or `tests/`, which is the point: `verify` should
  find the same behaviour it passed and the same evidence for it.
- **I did not rewrite `vision.md`'s v5–v8 change-log rows.** They are records of what those
  versions said at the time and remain true as such, including v8's *"The behaviour is still not
  built and this section still says so"*.
- **I did not touch `## Accepted as delivered`.** It already carries its own correction — the
  2026-08-28 acceptance was withheld on the second ask — and that is still exactly the state of
  the engagement.
- **I did not act on `review.md`'s finding 2.** The ADR-0010 §2 rule 2 wording is recorded as an
  accepted gap in the item's `## Notes`, and correcting a standing decision's text is the
  architect's act under ADR-0009, not the developer's. It is left where the reviewer put it.
- **I did not file a bug item or a question.** The defect is this item's own, no decision needed
  making that the plan or the review had not already made, and nothing in another item's delivered
  behaviour looked wrong.
