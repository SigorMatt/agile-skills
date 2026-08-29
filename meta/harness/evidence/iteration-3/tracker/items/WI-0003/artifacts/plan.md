# Plan — WI-0003 Recognise a table mdtab laid out with a right-aligned first column

## Problem

mdtab decides a run of lines is a table only if every line carries a byte-identical prefix of
spaces, tabs and `>` [src: ADR-0003]. Since WI-0002, mdtab's own layout can break that: honouring
a `---:` or `:---:` marker in the first column of a table written without outer `|` bars puts the
padding at the very start of the line, so the header and body rows acquire leading spaces the
delimiter row does not have [src: WI-0002 AC10]. The tool then refuses its own output. The bytes
are a fixed point [src: WI-0001 AC6], so nothing looks wrong until someone edits a cell and re-runs
the tool — which is the commonest reason to run it. This item makes the run's shared indentation,
rather than each line's own, the thing that must match, so that spaces past it belong to the first
cell. The stakeholder chose that in `WI-0003/Q-001` knowing its price: a bare table whose rows
carry different numbers of leading spaces starts being tidied, and comes back at the shallowest
indent in the run. Tabs and `>` must still match byte-for-byte, nothing outside a recognised run
may change, and all 33 fixture documents the project ships must produce byte-identical output.

## Approach

One new function, one two-line change to the recognition rule, and nothing else in the layout.

- **The shared prefix is a property of a run, not of a line, and it lives in `mdtab/scan.py`.**
  Add `shared_prefix(contents: list[str]) -> str | None`, beside `line_prefix`, returning the
  longest common prefix of the lines' `line_prefix` values when every line's remainder past it is
  spaces only, and `None` otherwise. `mdtab/scan.py` is where "what an indent is" already lives
  [src: docs/architecture/overview.md], and the new rule is entirely about indentation: it
  mentions no cell, no `|` and no table. Putting it in `mdtab/table.py` instead would split the
  prefix rule across two modules and leave `line_prefix` in `scan.py` with the thing that uses it
  somewhere else.

- **`lay_out`'s rule 2 becomes a call.** Today it computes `prefix = line_prefix(contents[0])` and
  refuses the run when any other line's prefix differs. It becomes `prefix = shared_prefix(contents)`
  and refuses when that is `None`. The line that follows — `bodies = [content[len(prefix):] …]` —
  is unchanged, because the shared prefix is a prefix of every line by construction. `table.py`'s
  import of `line_prefix` is replaced by one of `shared_prefix`; nothing else in that module uses
  it [src: mdtab/table.py].

- **Nothing downstream needs to know.** `bodies` may now begin with spaces, and each of the three
  remaining rules already does the right thing with that, which is why this is a two-line change
  and not a redesign:
  - `is_delimiter_row` strips spaces from each cell before matching [src: mdtab/table.py], so a
    delimiter row that was the deepest-indented line is still recognised.
  - `has_leading_pipe(body)` is `body.startswith("|")` [src: mdtab/table.py], so a row with extra
    spaces before its `|` has no leading pipe while its neighbours do, and rule 4 refuses the run
    — which is exactly the outcome that run has today, by a different route. This is what makes
    tables with outer bars unaffected [src: WI-0003 AC7].
  - `_render_cell` trims each cell with `.strip(" ")` before placing it [src: mdtab/table.py], so
    the spaces that are now part of the first cell are removed like any other cell padding
    [src: WI-0001 AC11].

- **Recorded as ADR-0008, which supersedes ADR-0003.** Rule 2's text is reversed, and
  `.claude/agile-skills/spec/doc-header.md` §4 forbids editing an ADR to change its decision.
  ADR-0008 restates all four rules with rules 1, 3 and 4 reproduced unchanged, and ADR-0003 is
  marked `superseded` with a pointer at the top. The item's `## Notes` anticipated an amendment in
  place; the spec is what decided otherwise, and the substance is identical either way.

## Steps

1. **`mdtab/scan.py` — the shared prefix.** Add `shared_prefix(contents: list[str]) -> str | None`
   below `strip_prefix`. It computes each line's `line_prefix`, takes their longest common prefix
   byte for byte, and returns it when every line's prefix past that point contains only `" "`;
   otherwise it returns `None`. Update the module docstring, which says the module "only finds; it
   never judges" — the new function answers "do these lines share an indent", which is a fact about
   the lines rather than a judgement about tables, and the docstring should say so rather than be
   left contradicting the code. Afterwards:
   `shared_prefix(["  a | b", "---|---", "  c | d"])` is `""`;
   `shared_prefix([">  a", "> b"])` is `"> "`;
   `shared_prefix(["\ta", "  b"])` is `None`;
   `shared_prefix(["> a", ">> b"])` is `None`;
   `shared_prefix(["> | a |", "> | b |"])` is `"> "`.

2. **`mdtab/table.py` — use it.** Replace the `from mdtab.scan import line_prefix` import with
   `shared_prefix`, and replace rule 2's two lines in `lay_out` with a call that returns `None`
   when `shared_prefix` does. Keep the comment above it, updated to name the rule as it now reads
   and to cite ADR-0008 rather than AC15. Afterwards, `python3 -m mdtab` on
   `'   a | bbbbb\n----:|--\nxxxx | y\n'` returns a re-aligned table rather than its input.

3. **`tests/fixtures/` — the documents.** Add these pairs, `.in.md` and `.out.md`, with the
   expected half written by hand from the criteria rather than by running the code:

   | fixture | in | out | for |
   |---|---|---|---|
   | `refeed-bare-first-column` | `   a \| bbbbb` / `----:\|--` / `xxxx \| y` | `   a \| bbbbb` / `----:\|------` / `xxxx \| y    ` | AC2 |
   | `refeed-blockquote-first-column` | the same three lines each prefixed `> `, at the widths AC3 gives | re-aligned | AC3 |
   | `refeed-list-indent-first-column` | the same three lines under a two-space indent | re-aligned | AC3 |
   | `uneven-leading-spaces` | `  a \| b` / `---\|---` / `  ccc \| d` | `a   \| b` / `----\|--` / `ccc \| d` | AC5 |
   | `uneven-delimiter-deepest` | `a \| b` / `   ---\|---` / `c \| d` | `a \| b` / `--\|--` / `c \| d` | AC5 |
   | `uneven-blockquote-space` | `>  a \| b` / `> ---\|---` / `>  c \| d` | `> a \| b` / `> --\|--` / `> c \| d` | AC5 |
   | `quote-depth` | `> a \| b` / `>> ---\|---` / `> c \| d` | identical to the input | AC6 |

   Note the trailing spaces on the last line of `refeed-bare-first-column.out.md`; they are
   required by [src: WI-0001 AC2] and are the easiest thing in this item to drop by accident.
   `tests/test_fixtures.py` discovers pairs by name [src: tests/test_fixtures.py], so no
   *assertion* changes for these — but `ALIGNED` and `UNTOUCHED` in that file are hand-written maps
   and a laid-out fixture missing from `ALIGNED` is checked against the wrong rule, so the six
   laid-out pairs go in `ALIGNED` and `quote-depth` in `UNTOUCHED`. (Corrected after the fact:
   the plan as first written said no test code changes at all.) **No existing `.out` file may be
   edited** — that is AC8.

4. **`tests/test_units.py` — the unit tests for the new rule.** Add a test class for
   `shared_prefix` asserting the five results in step 1. Afterwards, `python3 -m unittest
   tests.test_units` covers the rule directly rather than only through documents.

5. **`tests/test_units.py` — the one shipped test that changes.** In
   `PaddingPlacementTest.test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`,
   the final assertion `self.assertIsNone(lay_out(laid_out))` becomes an assertion that the run
   *is* laid out and is a fixed point — `self.assertEqual(lay_out(laid_out), laid_out)`. Its first
   two assertions and the rest of the suite are untouched. Rewrite its docstring, which currently
   says mdtab does not recognise its own output and that "when WI-0003 lands, the last assertion
   here is the one that changes"; it should now say what the assertion checks and cite ADR-0008.
   This is the first of the two pre-existing tests whose assertions change; the second is step 7
   [src: WI-0003 AC9].

6. **`tests/test_units.py` — one comment correction, no assertion change.**
   `RejectionTest.test_rule_2_a_run_whose_prefixes_are_not_byte_identical` has two assertions and
   both still pass. Its second — `lay_out(["> | a | b |", ">  |---|---|", "> | 1 | 2 |"])` is
   `None` — is now refused by rule 4 rather than by rule 2, so the comment above it, which explains
   the case as isolating rule 2, is wrong after this change. Correct the comment and, so that the
   test still does what its name says, keep the tab case as rule 2's isolation and move the extra-space
   case to `test_rule_4_a_run_whose_rows_disagree_about_their_outer_pipes` where it now belongs.
   No assertion is deleted.

7. **`tests/test_fixtures.py` — the second pre-existing test that changes.** Added by
   `answer-questions` on 2026-08-28, answering `Q-002`; the plan as first written did not foresee
   it. `ContentPreservationTest.test_ac11_cell_content_survives_apart_from_the_spaces_around_it`
   compares `[cell.strip(" ") for cell in line.split("|")]` before and after, over the raw line.
   That counts a line's indentation as part of its first field, which was exact while rule 2
   required byte-identical prefixes and is not exact under ADR-0008: for a run whose shared prefix
   ends in a `>`, the spaces after it are the first cell's and are re-laid-out
   [src: WI-0003 AC1]. Remove each line's leading run of space, tab and `>` before splitting it,
   and compare as before. Do **not** import `strip_prefix` to do it: this file's expected values
   are hand-written precisely so that no test asks the code under test where something is
   [src: tests/test_fixtures.py], and `pipe_columns` in the same file already restates the
   escaping rule locally for the same reason. Afterwards, `uneven-blockquote-space` passes and the
   test still fails if any cell's characters change. `item.md` AC9 records this as the second of
   its two expected changes.

8. **Run the gates.** `python3 -m unittest discover -s tests -t .` and
   `python3 -W error -m compileall -q mdtab tests`, both from the repository root, and both must
   exit 0.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the relaxed rule, stated | 1, 2 | `tests/test_units.py` shared-prefix class (step 4), asserting the five results in step 1, including the tab and `>` refusals |
| AC2 — first form of the fault | 2 | fixture `refeed-bare-first-column`, plus the amended final assertion of `test_ac10_…` (step 5) |
| AC3 — second form, blockquote and indent | 2 | fixtures `refeed-blockquote-first-column` and `refeed-list-indent-first-column` |
| AC4 — idempotence still holds | 2 | `tests/test_fixtures.py`'s existing idempotence check over every pair, which now includes the six new ones |
| AC5 — uneven leading spaces are tidied | 2 | fixtures `uneven-leading-spaces`, `uneven-delimiter-deepest`, `uneven-blockquote-space` |
| AC6 — a tab or `>` is still byte-for-byte | 1 | fixture `quote-depth` (new) and `tab-prefix` (existing, unchanged); the two `None` assertions in step 4 |
| AC7 — outer-bar tables unaffected | 1, 2 | fixtures `ragged-prefix`, `outer-pipes`, `blockquote-table`, `list-indent-table`, `mixed-pipes`, all existing and all unedited |
| AC8 — the 33 shipped fixtures do not change | 3 | `python3 -m unittest tests.test_fixtures` passing with no `.out` file modified; `git diff --stat tests/fixtures/` on the branch shows only additions |
| AC9 — WI-0001 and WI-0002 still hold, two tests change | 5, 6, 7, 8 | `python3 -m unittest discover -s tests -t .` exits 0; `git diff` over `tests/` shows assertion changes in exactly the two pre-existing tests AC9 names, `test_ac10_…` and `test_ac11_…` |
| AC10 — silent, exit 0 | 2 | `__main__` is untouched [src: mdtab/__main__.py]; checked by running `python3 -m mdtab` on each new fixture input with stderr captured and `echo $?` |

## Amended after Q-002

`implement` reached step 7 with one test failing that neither this plan nor [src: WI-0003 AC9]
expected: `test_ac11_cell_content_survives_apart_from_the_spaces_around_it`, on the new
`uneven-blockquote-space` fixture. The approach above is unchanged and correct — the failure is in
a document-level test whose way of finding a cell was only ever exact under the rule this item
reverses. Step 7 above is new and step 8 is the old step 7. The alternative, dropping the fixture
so that the stale test keeps passing, was rejected in `Q-002`: it would have bought a green suite
by removing the one document that shows the problem.

## Assumptions

- **`shared_prefix` returns `str | None` rather than raising or returning a sentinel string.**
  `lay_out` already speaks `None` for "not a table" [src: mdtab/table.py], so this matches the one
  convention the module has. Reversing it is a change to two call sites in one file and no
  behaviour; cost is minutes.
- **The longest common prefix is computed over the lines' `line_prefix` values, not over the raw
  lines.** Over raw lines, a table whose first cells happen to share a letter would fold that
  letter into the prefix. This is not a free choice — [src: WI-0003 AC1] states it — but it is
  worth writing down as the thing to check first if the fixtures come out wrong.
- **No new fixture needs a non-UTF-8 or CRLF variant.** The existing `invalid-utf8` and `crlf`
  pairs cover those axes and are unaffected: a terminator is removed before a line is examined
  [src: ADR-0004], so it can never be part of a prefix. Reversing this costs one more fixture pair.

## Decisions and ADRs

| decision | where | route |
|---|---|---|
| Rule 2 becomes a shared-prefix rule; rules 1, 3, 4 unchanged | ADR-0008 | asked — the stakeholder chose option A in `WI-0003/Q-001` after being shown the documents it changes |
| A tab or a `>` still matches byte-for-byte | ADR-0008 §Context and rule 2 | asked — confirmed in the same answer; [src: ADR-0002] defines no width for a tab |
| ADR-0003 is superseded rather than amended in place | ADR-0008 §Context; ADR-0003 header | documented — `.claude/agile-skills/spec/doc-header.md` §4: "An ADR is never edited to change its decision" |
| `shared_prefix` lives in `mdtab/scan.py` | `## Approach`; overview's one-place-per-rule list | documented — the overview already puts "what an indent is" in `scan.py` |
| `str \| None` as the signature | `## Assumptions` | assumed, reversible in one file |

## Scaffolding

none.

## Risks

- **The one place this can go wrong silently is a `.out` fixture edited to match new behaviour.**
  AC8 exists for it, and step 3 says no existing `.out` may change, but the failure would look
  like a passing suite. `git diff --stat tests/fixtures/` on the branch is the check, and it
  belongs in the implementation report rather than only in verification.
- **Trailing spaces in expected output.** `refeed-bare-first-column.out.md` ends its last line
  with four spaces, required by [src: WI-0001 AC2]. An editor that strips trailing whitespace on
  save will delete them and the failure will read as a bug in the code.
- **The scope of the behaviour change is wider than the item's title suggests.** This changes
  documents nobody asked to have changed — bare tables with uneven leading spaces — and the only
  authority for that is one answer in `WI-0003/Q-001`. If verification finds a document class that
  changes and is not one of AC5's three shapes, that is a question for the architect, not a fixture
  to adjust.
- **`shared_prefix` on a run of one line.** `lay_out` returns `None` before rule 2 for runs shorter
  than two lines [src: mdtab/table.py], and `find_runs` never emits one [src: mdtab/scan.py], so
  the empty-input case is unreachable — but the function should still be total rather than raising
  on an empty list, because a unit test will call it directly.

## Out of scope for this item

- Any change to layout, width, alignment or punctuation. Every one of those is WI-0001's or
  WI-0002's and must come out byte-identical [src: WI-0003 AC7; src: WI-0003 AC8].
- Relaxing any other recognition rule. Cell count, outer-pipe style and fenced blocks are refused
  exactly as they are today [src: ADR-0008].
- Deciding a tab's display width, or any diagnostic output [src: EP-001].
