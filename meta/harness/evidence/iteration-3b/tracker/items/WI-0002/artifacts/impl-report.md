# Implementation report — WI-0002

Branch `wi/WI-0002`, three commits, `c64f374..a324868`, cut from `main` at `b4568fe`.

## What was built

`mdtab.py` now reads each column's alignment marker and places that column's cell text
accordingly, instead of always padding on the right.

- **`column_alignments(rows)`** — new, beside `column_widths`. Reads the delimiter row and returns
  one of `LEFT`, `RIGHT`, `CENTRE` or `None` per column, which is ADR-0005's decision 1
  [src: ADR-0005]. `None` is kept
  distinct from `LEFT` although the two compose identically today, because ADR-0005 decides the
  markerless case separately in decision 4 (plan.md, Assumptions).
- **`compose_row(cells, widths, alignments, prefix)`** — the signature gained `alignments`. It
  still computes `pad = width - display_width(cell)` and still writes one space either side; what
  changed is that `pad` is now split into a leading and a trailing run. `RIGHT` puts all of it
  before the text, `CENTRE` puts `pad // 2` before — integer division, so an odd leftover space
  falls to the **right** of the text, which is ADR-0005's decision 2 [src: ADR-0005] — and `LEFT`
  and `None` put all of
  it after.
- **`emit_block`** — computes the alignments once per table, beside the widths, and passes them to
  each `compose_row` call. `compose_delimiter` is untouched: which colons a delimiter cell carries
  and where they sit is ADR-0004's and out of scope here.
- **The module docstring** — gains ADR-0005, and its ADR-0004 filename is corrected (see
  Deviations 2).

The tests are renamed to ADR-0006's convention, three fixtures are added, and one fixture is
regenerated. 14 tests before, 24 after; all pass.

## Acceptance criteria evidence

Every row names a test method. `python3 -m unittest discover -s tests -t .` → `Ran 24 tests … OK`,
exit 0, run on the branch head after the last commit.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — left marker | `compose_row` leaves `pad` entirely after the text for `LEFT` | `test_wi0002_ac1_left_marker_pads_to_the_right` — asserts `aligned.expected.md` byte for byte, then, for all four rows of the left-marked column, that the field equals `" " + text + " "*(W-w) + " "` with `W` recomputed from the *input* fixture via `mdtab.display_width`, and that the text's first display column is `1` on every row including the header |
| AC2 — right marker | `RIGHT` puts all of `pad` before the text | `test_wi0002_ac2_right_marker_pads_to_the_left` — same pair, field equals `" " + " "*(W-w) + text + " "`, every row's text ends at display column `W+1`, and the header field is literally `"   R "`, so "the header row included" is not vacuous |
| AC3 — centre marker and the odd remainder | `CENTRE` puts `pad // 2` before and `pad - pad // 2` after | `test_wi0002_ac3_centre_marker_puts_the_odd_space_on_the_right` — the split asserted per row against the criterion's own arithmetic; at least one row has an odd `pad` and its leading run is asserted strictly smaller than its trailing one. Plus the worked examples against `compose_row` directly: width 3 with `ab` → `\| ab  \|` and *not* `\|  ab \|`; width 3 with `Q` → `\|  Q  \|`; width 1 with `Q` → `\| Q \|` (see Deviations 3) |
| AC4 — no marker | `None` composes exactly as `LEFT` does, which is WI-0001's rule | `test_wi0002_ac4_no_marker_is_unchanged_by_this_item` — the unmarked column of `aligned.expected.md` against the formula; `ragged.md` still byte-identical to `ragged.expected.md`, which was written under WI-0001 and is **not** regenerated here; and `compose_row(["d"],[5],[None])` equals `compose_row(["d"],[5],[LEFT])` |
| AC5 — empty cells and zero-width marked columns | `pad = W - 0 = W`, split by the marker as usual | `test_wi0002_ac5_empty_cells_and_zero_width_marked_columns` — on `aligned_empty.md`: each empty cell is `W+2` spaces in all three marked columns, and the three lengths are asserted to be `[6, 5, 7]` so "in every case" is a claim about three different widths. The second table asserts `\|  \|  \|   \|` / `\|:-\|-:\|:-:\|` literally — `:---` → `W=0`, two spaces; `---:` → the same; `:---:` → `W=1`, three spaces. Then the filter is run on that output and the result asserted byte-identical |
| AC6 — markers and display width together | widths are display widths throughout; the marker only moves where inside them the text sits | `test_wi0002_ac6_markers_and_display_width_together` — on `aligned_wide.md`: `aligned_wide.expected.md` byte for byte, all five lines one display width, and the pipe positions measured in display columns identical on every row including the delimiter row. The input is asserted genuinely ragged, and `中`, `🙂` and `e`+U+0301 asserted present, so neither half is vacuous |
| AC7 — markers survive and mean the same | `compose_delimiter` was not touched | `test_wi0002_ac7_markers_survive_and_mean_the_same_thing` — over **all 19 input fixtures**: delimiter cells are read with `pipe_blocks`/`delimiter_cells`, a parser written in the test independently of `table_or_none` so the assertion is not a tautology. Per column: output starts with `:` iff input did, ends with `:` iff input did. On the fixtures whose pipe blocks are tables the filter recognises, additionally `^:?-+:?$` and length equal to the content field's `W+2` (see Deviations 4). More than 20 columns checked, and `aligned.md`'s four are asserted to be exactly `(:,-) (:,:) (-,:) (-,-)`, so all four marker kinds are exercised |
| AC8 — idempotence over marked tables | output is a function of the delimiter row and the cell contents, both of which survive the round trip | `test_wi0002_ac8_idempotence_over_marked_tables` — filter run twice over `aligned.md`, `aligned_empty.md`, `aligned_wide.md`, `markers.md` and every other input fixture; second output asserted equal to the first, exit 0 both times |
| AC9 — WI-0001's criteria re-read by ID | partly `verify`'s (see below) | `test_wi0002_ac9_wi0001_criteria_meet_marked_columns` pins the machine-checkable half: all eleven `wi0001_ac<n>_` tests still exist after the ADR-0006 rename, and the three new marked fixtures are in `INPUT_FIXTURES`, so WI-0001 AC3's, AC9's and AC10's own loops now range over marked columns. The **verdicts** are `verify`'s to write into `artifacts/verify-report.md`; what this execution owes it is set out under "What I did not do" |
| AC10 — tests exist, exit status 0 | — | `test_wi0002_ac10_each_criterion_has_a_named_test` — exactly one discovered method contains `wi0002_ac<n>_` for n in 1..9, and each quotes `ACn ` in its docstring; then the filter is run over each of the four WI-0002 inputs and over its own output, asserting exit 0 each time |

**These tests were mutation-checked, not merely observed green.** Five mutations of `mdtab.py`,
each reverted afterwards: the odd centring remainder to the left; `RIGHT` ignored; all markers
ignored; the header row exempted from its column's marker; a delimiter colon moved to the other
end. Each failed at least one criterion's test — the header-exemption mutation failed AC1 to AC4,
which is what makes ADR-0005 decision 3 tested rather than asserted.

The stronger check, because plan.md named it as this item's top risk: the first mutation was
applied **and every expected fixture regenerated from the mutated filter**, so the wrong rule was
frozen into the fixtures exactly as a careless run would freeze it. AC3 still failed, on its
formula assertion, with `AssertionError: '  Centre ' != ' Centre  '`. The expected fixtures cannot
rubber-stamp a wrong split.

## Deviations from the plan

1. **Step 7 was executed immediately after step 4, not in numeric order.** Regenerating
   `markers.expected.md` is what makes `test_wi0001_ac4_...` pass again after `compose_row`
   changes; running steps 5 and 6 in between would have left the suite red across two commits. The
   step itself is unchanged — the diff was regenerated and read, not accepted — and it is one line:
   the Center column's `b` moves to `   b    ` and the Right column's `c` to `     c `, with the
   delimiter row byte-identical. Nothing else about the plan's ordering moved.
2. **The ADR-0004 filename correction in the module docstring was made, as plan.md step 4
   instructs, and no bug item was filed.** The docstring named
   `ADR-0004-delimiter-row-keeps-alignment-markers.md`; the file is `…-preserves-…`. It is a defect
   in an artifact WI-0001 delivered, and the escalation rule would ordinarily make it a `bug` item.
   The plan chose to fix it inside a step that rewrites those exact lines, on the grounds that it
   changes no behaviour and no criterion. This report repeats the reasoning rather than burying it:
   **a reviewer who thinks a bug item was owed should say so.**
3. **AC3's two worked examples cannot both describe one column, and the test asserts both
   readings.** AC3 says *"a centred column of width 3 holding the text `ab` is written `| ab  |` …
   and one holding `Q` is written `| Q |` with one space of padding on each side."* For `W=3, w=1`
   the criterion's own arithmetic gives `|  Q  |` — one space of padding on each side, as the
   prose says — while the literal `| Q |` is a column of width 1, which is what AC5's
   minimum-width rule produces for a `:---:` column holding one character. The criterion's
   formula is unambiguous and **both readings agree with it**, so no behavioural decision was
   taken and no question was filed; the test asserts `|  Q  |` at width 3 and `| Q |` at width 1.
   Flagged here because `verify` reading AC3's literal text alone will find `| Q |` at width 3
   absent, and should.
4. **AC7's `W + 2` clause is scoped to the fixtures whose pipe blocks the filter recognises as
   tables.** AC7 says "every table in the output", and WI-0002's preamble defines a table as what
   ADR-0003 recognises as one; the item's `## Out of scope` says a block ADR-0003 declines to
   recognise is copied byte for byte. `fenced.md`, `indent_mismatch.md`, `blockquote.md` and
   `malformed.md` contain pipe blocks of exactly that sort, whose delimiter cells keep whatever
   length the input gave them. The colon-for-colon clause is **not** scoped — it runs over all 19
   fixtures, because "adds no colon, removes none, moves none" must hold for copied blocks too.
5. **The test module's docstring and `INPUT_FIXTURES` were edited, which plan.md step 5 said not
   to touch.** Step 5's "no docstring changes" is about the eleven renamed methods' own
   docstrings, and none of those changed. The module docstring now describes two items' tests and
   ADR-0006's convention; `INPUT_FIXTURES` gained the three new inputs, which plan.md step 6
   requires and its Risks section calls out as a silent loss of coverage if forgotten.

## Gates

Run on the branch head (`a324868`), after the last commit.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 24 tests in 4.767s` / `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace: checked 3 item(s), 8 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-has-a-test` | **pass** | the table above names a test method for each of AC1 to AC10; none is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs: all 3 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | three hunks in `mdtab.py` → plan steps 4, 1+2, 3; `tests/fixtures/markers.expected.md` → step 7; the three new fixture pairs → step 6; `tests/test_mdtab.py` → steps 5 and 8; `tracker/` and `board.md` → the transitions. No hunk without a step |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → `claim window: 0 path(s) differ from main (b4568fe) under docs` / `checked 8 consumed human answer(s)` / `0 errors, 0 warnings`, exit 0 |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → `0 errors, 0 warnings`, exit 0 |

**D12 and ADR-0008 §3.** This execution changed no file under `docs/`, so it rewrote no sentence
carrying a stakeholder's citation and the third row of ADR-0008's table was not reached. The
standing claims about this behaviour were checked and are now **true of the code** rather than
falsified by it: `docs/product/vision.md` line 121, *"No content cell of a marked column is exempt:
the header cell obeys its column's marker exactly as a body cell does"* [src: WI-0002/Q-001], is
what the header-exemption mutation above shows the suite enforces. `ADR-0003` decision 9 already
carries a `## Corrections` row pointing at ADR-0005 for the marked case, added by
`answer-questions` before this execution; nothing further was needed.

## What I did not do

- **`artifacts/verify-report.md` — not written, by design.** AC9 requires a verdict for each of
  WI-0001 AC1 to AC11 reached by reading that criterion's own text, and that report is `verify`'s
  artifact. Three things this execution owes it, stated here so they are a handover and not a
  discovery:
  - **WI-0001 AC3 is the criterion this item's behaviour changes.** Its text — a content cell is
    `|`, one space, the text, "spaces padding it to the column's width", one space — reads as
    padding always following the text. That now holds **only for a column whose delimiter cell
    carries no marker**; the marked case is decided by ADR-0005 decisions 1 to 3 and asserted by
    WI-0002 AC4 for the markerless case and AC1 to AC3 for the marked ones. WI-0001's criteria
    were **not** edited, and `test_wi0001_ac3_...` was renamed but not otherwise altered — no
    assertion, no fixture, no docstring.
  - **No WI-0001 criterion needs waiving for non-intersection.** `aligned.md`, `aligned_empty.md`
    and `aligned_wide.md` were added to `INPUT_FIXTURES`, which is what WI-0001 AC3's
    no-trailing-whitespace loop, AC9's idempotence loop and AC10's exit-status loop range over, so
    each of those three now runs against marked columns. WI-0001 AC1, AC2, AC4, AC5, AC6, AC7, AC8
    and AC11 are exercised on their own fixtures; AC4 additionally reads `markers.expected.md`,
    which this item regenerated. That is the "adds a covering case" branch of AC9's second bullet;
    nothing is being waived.
  - **The `markers.expected.md` diff**, which is the single clearest artifact of what this item
    changes, is quoted in commit `c64f374` and reproduced under Deviations 1.
- **Nothing was measured on a large document**, exactly as WI-0001 recorded. The change adds one
  list of small strings per table and no extra pass over the input.
- **The escaped-pipe question `docs/product/vision.md` routes to `plan` was not touched.**
  `split_cells` is unmodified; no criterion of this item raises it.
- **No fixture other than `markers.expected.md` was regenerated.** In particular
  `ragged.expected.md`, `wide_chars.expected.md`, `wide_delimiter.expected.md`,
  `indented.expected.md`, `fenced.expected.md`, `crlf_table.expected.md` and
  `table_no_final_newline.expected.md` are byte-identical to what WI-0001 delivered, which is
  itself evidence for AC4 and for WI-0001's verdicts.

---

## The send-back from `review-close`, and what closed it

`review-close` rejected this item on D7 and D12 and returned it to `in-progress`
[src: tracker/items/WI-0002/artifacts/review.md]. Everything above this line describes the code
execution that produced `a324868` and is unchanged; this section reports the second execution,
which changed **no code and no test**. `git diff --stat c26e1af..HEAD` touches only
`docs/architecture/adr/`, `tracker/`, and nothing else; `mdtab.py` and `tests/` are byte-identical
to `a324868`.

### The three repairs the verdict required

| # | what the verdict asked for | who did it | where |
|---|---------------------------|------------|-------|
| 1 | past-tense `ADR-0005`'s `## Context` clause about what `compose_row` does, bump the version, add a change-log row | `answer-questions` | `8c58ac1`; `ADR-0005` v1 → v3, one `erratum` entry in a new `## Corrections` section |
| 2 | repair the four `[src: mdtab.py:207]` citations, appending a new row in `ADR-0003`'s `## Corrections` rather than editing the existing one | `answer-questions` | `8c58ac1`; three repaired in `ADR-0005` as one `provenance` entry, the fourth by a new append-only row in `ADR-0003` v2 → v3 |
| 3 | record `review.md` Findings 4 — AC3's second worked example describes a width-1 column — in `item.md`'s `## Notes` | `implement` | `e4dd5c6` |

### Why repairs 1 and 2 were not made by this skill

They are edits under `docs/`, and `spec/doc-header.md` §5 says `implement` does not write there:
*"If either concludes that a document is wrong, that is a question (`question.md`), and
`answer-questions` makes the edit."* `spec/question.md` §1 puts `implement` in the same row as
`verify` and `review-close`. This skill's own `SKILL.md` §6a routes the same case to "ordinary
repair — fix it", so the two documents disagree about who types it, and the answer decides which
skill's name appears in the `by` column of two append-only `## Corrections` sections.

Escalated as `Q-002`, blocking, addressed to the architect, rather than guessed. It was answered
**A** from the record — no ADR was needed — and `answer-questions` then applied both repairs
exactly as the verdict specified. The full reasoning is in
`tracker/items/WI-0002/questions/Q-002.md`.

**A toolkit finding for the owner, not a defect in this item:** `spec/doc-header.md` §5 and
`implement`'s `SKILL.md` §6a should be made to agree in writing. A future `implement` will read
§6a, find its case in the second row, and edit an ADR without ever reaching §5.

### What `answer-questions` had to repair beyond the verdict

Editing the two ADRs pulled them into `lint-claims --changed-since main`, which until then had
been examining an empty window — `review.md` Findings 3, reproduced exactly on this item's first
gate run. With a non-empty window it immediately failed on **four pre-existing `claim.unsourced`
errors**: three `## Context` absolutes in `ADR-0003` citing `Q-002`, `Q-001` and `Q-004` in prose
without a `[src: ...]` marker, and one in `ADR-0005`. None was introduced by this item, all four
are true, and each needed only the citation its own sentence already names. `implement` could not
have fixed them and its `claims-are-sourced` gate would have failed on them, so they were sourced
as `provenance` corrections in the same pass. This is `spec/doc-header.md` §4a's rule that the next
execution to edit a document is the one that must source what it writes.

### Acceptance criteria

Unchanged. No criterion was re-earned, because no behaviour moved: the ten rows in
`## Acceptance criteria evidence` above still name the tests that satisfy them, and
`check-verify-freshness WI-0002 wi/WI-0002` exits 0 with *"only the record changed (9 file(s)
under tracker/ or docs/), so the verification still covers the code"*. Whether to re-verify is
`verify`'s call; the verdict declined to pre-authorise it and so does this report.

### Gates, re-run on the branch head `8c58ac1`

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `3 item(s), 8 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | unchanged from `a324868`; the eleven `test_wi0002_ac<n>_` functions listed above, none of them edited since |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 10 commit(s) on main..wi/WI-0002 name WI-0002` |
| `no-unplanned-scope` (advisory) | **pass** | `git diff --stat c26e1af..HEAD` is seven files: the two ADRs, and `board.md`, `history.md`, `item.md`, `journal.md`, `questions/Q-002.md`. Every one traces to a numbered item of the verdict or to the escalation it required |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0. It first reported `answer.claim-rewritten-unasked` on `ADR-0005:132` for `WI-0001/Q-003`, because the repaired code pointer sits in the same paragraph as their *"the size of the first diff is not a concern"*; `ADR-0008` §3's first response was taken and the `**Cross-answer check:**` bullet in `answer-questions`' journal entry names the answer and states why the edit is compatible. Their sentence and its citation are untouched |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 over `2 document(s) in 2 path(s)` — a window that is no longer empty, which is what let it find the four unsourced absolutes |

### What I did not do

- **No code, no test, no fixture.** The verdict says the code is not in question, and nothing
  above changed it. `## What I did not do` in the first execution's report still stands in full.
- **Did not repair `ADR-0001:58`**, the one `claim.unsourced` error `lint-claims --all` still
  reports — an absolute about `./mdtab.py` in a document no item in this engagement has touched.
  It is outside WI-0002's window, outside D12's scope, and fixing it here would be the unrelated
  tidying this skill is told not to do. It is visible to `lint-claims --all` and to `--context
  epic`, so it will be picked up when the epic is closed.
- **Did not re-verify.** That is `verify`'s call, as the verdict says.
- **Filed no bug item.** `review.md` Findings 5 already ruled that none was owed for the
  `ADR-0004` filename repair the first execution's Deviations 2 asked a reviewer about; that
  question is settled and is not re-opened here.
