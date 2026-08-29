# Verification report — WI-0004

Verified-commit: a64ec3ef7fafd2e9ef7fa16f9fdd937f5fb9640c

**This is the second verification of this item**, run at 2026-08-29T08:11Z. The first passed
AC1–AC7 at `dff7600` on 2026-08-29T07:57Z; `review-close` then rejected the item on Definition of
Done D7 and D12 — `docs/product/vision.md` still said the behaviour was not built — and `implement`
remedied that at `00a08e8`. This report replaces the first one and stands on its own: every
criterion below was decided again, by a command run against `a64ec3e`, and nothing here is carried
over from the earlier pass. The first report is in git history at `4a2f05c` for anyone comparing
the two.

## Verdict

**Pass.** All seven criteria are met. What settles each was derived from the criterion's own
wording before `impl-report.md` was opened, and AC1, AC3, AC6 and AC7 are measured against the
**trunk's** tool — `main` extracted with `git archive` into a scratch directory — so "exactly as a
`:---` column's cells are", "as they are today" and "byte-for-byte identical" are diffs rather than
assertions. Eleven boundary cases were triggered and three mutations of the branch head confirmed
the tests are sensitive. No defect; no bug filed; no question.

`git diff dff7600..a64ec3e -- mdtab/ tests/` is **empty** — no line of code or of any test changed
since the first verification — so the behaviour re-measured here is the behaviour that passed then,
and this pass is a genuine re-run rather than an inference from it.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | the AC1 document under `\|:---:\|---:\|`, under `\|---:\|---:\|`, and under `\|:---\|---:\|` as the reference the criterion names; then the four-spelling document; then `a<BR>b` alone under `---:` | centred → `\| a<br>b          \| x \|`; right → `\| a<br>b          \| x \|`; **left-marker reference → `\| a<br>b          \| x \|`, byte-identical to both**; four spellings → `\| a<BR/>b          \| x \|`, `\| c<br />d         \| y \|`, `\| e<br class="k">f \| w \|`; `\| a<BR>b         \| x \|` | the cell is padded to its column's width with all the padding on the right, and the row is the same bytes under all three markers — which is exactly what *"exactly as a `:---` column's cells are, whatever marker the column carries"* asks. All five spellings AC1 names are placed left |
| AC2 | **pass** | the delimiter rows of all five documents above, plus the AC3 and AC6 documents | `\|:---------------:\|--:\|` from `:---:`; `\|----------------:\|--:\|` from `---:`; `\|:----------------\|--:\|` from `:---`; `\|:----------------:\|--:\|`; `\|---------------:\|--:\|`; `\|:------------:\|--:\|`; `\|:--------------:\|--------------:\|` | every marker comes back the marker the author wrote, widened to the column. No colon gained, lost or moved |
| AC3 | **pass** | `printf '\| long heading \| b \|\n\|:---:\|---:\|\n\| aa \| x \|\n\| a<br>c \| y \|\n\| bb \| z \|\n'` through the branch **and** through a `git archive main` copy, then `diff` of the two outputs with the break row removed | branch: `\|      aa      \| x \|`, `\| a<br>c       \| y \|`, `\|      bb      \| z \|`; trunk: identical except `\|    a<br>c    \| y \|`; `diff` of everything but the break row → **no output, exit 0** | the only line that differs from the shipped tool's output anywhere in the document is the one holding the break. Header, delimiter, both neighbours, the second column and the column's width (14) are byte-identical |
| AC4 | **pass** | six documents — the five named in AC1, AC6 and AC7, plus one with prose either side of the table and a `<br>` in the prose — each run, run again on its own output, `cmp`ed, with stderr sized and both exit codes captured | `doc1`…`doc6`: `exit=0/0 stderr=0B/0B twice=same`, six for six. In `doc6`, `diff` of the four non-table lines between input and output → **no output** | idempotent, silent, exit 0, and a `<br>` written in prose outside a table is not touched |
| AC5 | **pass** | `python3 -m unittest discover -s tests -t .`; then `python3 -m unittest -v` naming all **twenty** tests AC5 lists; then `git diff main..HEAD -- tests/ \| grep -cE '^-[^-]'`; then `git diff --numstat`; then a search of the tests diff for five of the named functions | suite → `Ran 84 tests … OK`, exit 0; the twenty → `Ran 20 tests … OK`, exit 0; removed lines → **`0`**; numstat → `8 0` and `113 0`; each named function searched for → `0` occurrences in the diff | the suite passes, every named test passes unmodified, and not one line was removed from or altered in either test file. WI-0001, WI-0002 and WI-0003's criteria are additionally exercised directly by boundary cases 4, 6, 7, 8, 9 and 10 below — fences, display width, escaped pipes, a bare right-aligned table and its re-feed, a blockquote table and a list-indented one |
| AC6 | **pass** | `printf '\| a<br>b \| second column \|\n\|:---:\|---:\|\n\| wide body cell \| y \|\n' \| python3 -m mdtab` on the branch and on the trunk copy, then `diff` of the last two lines | branch → `\| a<br>b         \| second column \|`; trunk → `\|     a<br>b     \| second column \|`; `diff` of the delimiter and body rows → **no output** | the header is placed by the same rule as a body cell — flush left, padding after it, exactly the row AC6 requires — and the rest of the table is byte-identical to the shipped tool's |
| AC7 | **pass** | `printf '\| heading is long \| b \|\n\|---:\|---:\|\n\| `<br>` \| x \|\n'` through the branch and through the trunk copy, compared with `cmp` | `\|          `<br>` \| x \|`; `cmp` → **exit 0, identical bytes** | a tag inside a code span leaves the cell ordinary, and the whole document is byte-for-byte what the shipped tool produced |

All seven checkboxes in `item.md` were already ticked by the first verification. Each was
re-demonstrated here by a command in this table before being left ticked; none was accepted on the
strength of the earlier pass.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run by this skill on `a64ec3e` → exit 0, `Ran 84 tests in 0.149s … OK` |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, 6 items, 12 documents |
| `every-criterion-independently-checked` | **pass** | every row of the table above names a command this skill ran and quotes its output. No row cites `impl-report.md` or the first verification. AC1, AC3, AC6 and AC7 are measured against a `git archive main` copy, which the implementation report did not do |
| `negative-cases-exercised` | **pass** | eleven cases below, each triggered rather than reasoned about |
| `tests-would-fail-without-the-change` | **pass** (advisory) | three mutations of the branch head, below, each restored afterwards |

## Negative and boundary cases exercised

| # | case | what happened |
|---|------|---------------|
| 1 | tag lookalikes `<brx>` and `</br>` under `---:` | both stayed **right-aligned**: `\|        a<brx>b \| x \|`, `\|        c</br>d \| y \|`. The plan's assumption 1 holds in the code |
| 2 | a cell that is *only* `<br>`, beside an empty cell, under `:---:` | `\| <br>           \| x \|` — left; the empty cell `\|                \| y \|` unchanged, so an empty cell in a break cell's column is untouched |
| 3 | a `br` tag in the **delimiter row** | the whole document came back **byte-for-byte unchanged** — the run is not a table, so nothing was rewritten and no marker was touched |
| 4 | a table with a break **inside a fenced code block** | `cmp` of input and output → **exit 0**, byte-for-byte unchanged. The epic's fence exclusion is not disturbed |
| 5 | ADR-0010 §3's three unconstrained cases in one `---:` table | `\| a`<br>b        \| x \|` (left — the run never closes), `\|       ``<br>`` \| y \|` (right — the span holds it), `\| a`<br>`b<br>c  \| z \|` (left — the second tag is outside). All three match ADR-0010 §3 exactly |
| 6 | a **wide character** in a break cell, with a wider body cell so the placement is visible | `\| 漢<br>字          \| x \|` flush left, `\|       plain       \| z \|` still centred, and every `\|` lands at display columns 20 and 24 on all four lines. Width is display width and the override does not disturb it |
| 7 | an **escaped pipe** in a cell with a break | `\| a\\\|b<br>c      \| x \|` — one cell, placed left, the escape intact. WI-0001 AC10's rule is untouched |
| 8 | a **bare table** (no outer pipes), right-aligned first column holding a break, then **re-fed** | `a<br>c       \| x` — the break cell starts at the line margin instead of being pushed right, so the run keeps a shared prefix; re-feeding the output `cmp`s **identical**. WI-0003's recognition property survives the new rule |
| 9 | a table inside a **blockquote** with a break | `> \| a<br>c       \| y \|` — only the break cell moved, `>` prefix preserved on every line, `\|      aa      \| x \|` still centred |
| 10 | a table under a **list bullet** with a break | `  \| a<br>c       \| y \|` — same, with the two-space indent preserved |
| 11 | the `<br` + code span + `>` shape that `impl-report.md` deviation 1 names | `\| a<br `>` b     \| x \|` — placed **left**, confirming the implemented start-index reading. No criterion decides this shape; see `## Not verified, and why` |

## Test sensitivity check

Three mutations, each applied to the branch head, the suite run, and the file restored from a copy
taken before the mutation. `git status --short` afterwards shows only the pre-existing `IDEA.md`.

| mutation | tests that failed |
|----------|-------------------|
| the per-cell override removed from `_render_row` — `alignments[column]` used for every cell | `test_ac1_a_break_cell_sits_left_in_a_centred_column`, `test_ac1_a_break_cell_sits_left_in_a_right_aligned_column`, `test_ac2_ac3_only_the_row_with_the_break_moves`, `test_ac6_a_header_cell_with_a_break_sits_left_too`, `test_every_fixture_produces_its_expected_output` (fixture `line-break-cells`) — **5 failures** |
| the code-span exclusion disabled (`spans = []`) | `test_ac7_a_cell_showing_the_tag_still_obeys_its_marker`, `test_ac7_a_tag_inside_a_code_span_is_the_author_showing_it`, `test_a_multi_backtick_span_holds_its_tag`, `test_every_fixture_produces_its_expected_output` (fixture `line-break-code-span`) — **4 failures** |
| the tag pattern's lookahead dropped, so `<brx>` matches | `test_text_that_only_looks_like_the_tag_does_not_count` (at `text='<brx>'`) — **1 failure** |

AC1, AC3 and AC6 are covered by tests that die with the first mutation, AC7 by the second, and
AC1's spelling boundary by the third. AC2 and AC4 survive all three, which is correct: they assert
that something did **not** change, so breaking the new behaviour need not break them. Their
evidence is the trunk comparison and the six double-run measurements above.

## The diff, read against the plan

`git diff --stat main..a64ec3e` — seventeen files, two of them production. `mdtab/inline.py` whole
is plan step 1; `mdtab/table.py`'s four hunks are one import, two docstrings and the four changed
lines of plan step 2; `tests/test_units.py` is steps 3–4, the four fixtures and
`tests/test_fixtures.py` step 5, `docs/architecture/overview.md` step 7. There is no hunk that no
criterion and no plan step accounts for.

The one thing that is **not** in the plan is `docs/product/vision.md`, and it is the send-back
remedy: five hunks — the version header, the `## What it does` "no exceptions" paragraph, the
`## Open at the time of writing` opening, its closing paragraph, and the v9 change-log row. No
acceptance criterion covers documentation, so this is not verified as an AC; what this skill did
check is that the document does not now assert something untrue:

- the transcript v9 prints was `diff`ed against the tool's actual output on `a64ec3e` → **no
  output**, so the document shows what the tool really prints;
- the two rows v9 attributes to the past — `|     a<br>b      | x |` under `:---:` and
  `|          a<br>b | x |` under `---:` — were reproduced from the `git archive main` copy and
  match character for character.

`impl-report.md`'s three original deviations were re-checked rather than accepted: deviation 1 is
exercised by boundary cases 1, 5, 6 and 11; deviation 2's extra test is traceable to AC4;
deviation 3's break-free fixture row is what makes `line-break-cells` demonstrate AC3.

## Defects found

None.

## Not verified, and why

- **The `<br` + code span + `>` shape**, boundary case 11. It is decided by no acceptance
  criterion and by no clause of ADR-0010, so there is nothing to verify it *against*; the case was
  triggered and its behaviour recorded (left-aligned) rather than judged. `review-close` has
  recorded it as an accepted gap in the item's `## Notes`, and this report is where the observed
  behaviour lives.
- **`docs/product/vision.md` as a Definition of Done matter.** This skill checked that v9's
  factual claims about the tool are true, which is what it can check. Whether the document now
  satisfies D7 and D12 — whether *every* claim it makes about behaviour this item touched is
  true, and whether the version bump and change-log row are adequate — is `review-close`'s
  judgement, and it is the criterion that sent the item back.
- **`git diff --stat` reports the four fixture files as `Bin`** because `.gitattributes` marks
  fixtures binary, so their content is not visible through the diff. Verified directly instead:
  `python3 -m mdtab < tests/fixtures/<name>.in.md` `diff`s clean against the `.out.md` half for
  both pairs, which is also what `test_every_fixture_produces_its_expected_output` asserts and
  what two of the three mutations broke.
- **Rendering.** No criterion asks how a break cell *looks* in a markdown renderer, and none was
  consulted. AC1's "sits at the left of its column" is checked as byte placement, which is all
  mdtab controls; `refinement-qa.md` records the same reading as an assumption.
- **Performance, large inputs, and Python versions other than 3.12.** Declined as work by the
  stakeholder in `EP-001/Q-004`; no criterion covers them and none was measured.
