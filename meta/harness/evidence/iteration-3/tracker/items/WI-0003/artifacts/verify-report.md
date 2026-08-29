# Verification report — WI-0003

Verified-commit: 63e072d375f0edd178c5b6af8049b6f5d4b2031d

This is the **second** verification of WI-0003. The first, at `0129b1d`, passed all ten criteria
and sent the item to review; `review-close` rejected it at `fb43b93` on **D7 and D12** — two
documents still described the pre-change tool — and `implement` cleared that send-back in
documents only. Between the two verified commits the tree changed in `docs/architecture/overview.md`,
`docs/product/vision.md`, the record, and **two bytes of code**: the module docstring of
`tests/test_units.py`, where `ADR-0003` became `ADR-0008`.

That is not a reason to verify less. Every criterion below was decided again by a command run at
`63e072d` — none of it is carried over, and none of it is taken from `impl-report.md`, which was
read after the criteria and after the evidence was gathered. The differential in AC7/AC8 is a
fresh corpus with a different seed from the first verification's, so the two runs are independent
measurements rather than one repeated.

## Verdict

**Pass — all ten acceptance criteria met.** No defect found, no bug item filed, no question
raised. The item moves to `in-review`.

## Criteria

The invocation throughout is `python3 -m mdtab` with the document on stdin, per WI-0001's plan.
Output is shown through `cat -A` where trailing spaces are part of the claim; `$` marks end of line.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | five clause probes, below | see `### AC1, clause by clause` | the definition; each of its five clauses probed separately |
| AC2 | **pass** | `printf 'a \| b\n---:\|---\nxxxx \| y\n' \| python3 -m mdtab` then the transcript's second command | `   a \| b$` / `----:\|--$` / `xxxx \| y$`, then `   a \| bbbbb$` / `----:\|------$` / `xxxx \| y    $` | both transcripts reproduced byte for byte, including the trailing spaces AC2 warns about on `xxxx \| y`; exit 0 |
| AC3 | **pass** | the same two steps on `> a \| b` / `> ---:\|---` / `> xxxx \| y` and on the two-space indent | step 1: `>    a \| b$` / `> ----:\|--$` / `> xxxx \| y$` and `     a \| b$` / `  ----:\|--$` / `  xxxx \| y$`. step 2 (with `b` → `bbbbb`): `>    a \| bbbbb$` / `> ----:\|------$` / `> xxxx \| y    $` and `     a \| bbbbb$` / `  ----:\|------$` / `  xxxx \| y    $` | both forms re-aligned rather than returned unchanged; both step-1 outputs are what AC3 predicts |
| AC4 | **pass** | every document of AC2, AC3, AC5, AC6, AC7 and all 40 fixture inputs run twice and `cmp`-ed; then the 6000-document corpus | `documents checked: 56; non-idempotent: 0` and `AC4 over the 6000-document corpus — non-idempotent: 0` | 6056 documents, no fixed-point failure |
| AC5 | **pass** | the three documents AC5 names | `a   \| b$` / `----\|--$` / `ccc \| d$`; `a \| b$` / `--\|--$` / `c \| d$`; `> a \| b$` / `> --\|--$` / `> c \| d$` | all three match the criterion's text exactly, including the blockquote coming back at the shared prefix `> ` |
| AC6 | **pass** | `diff` of input against output for `\ta \| b` / `  ---\|---` / `\tc \| d` and for `> a \| b` / `>> ---\|---` / `> c \| d` | `IDENTICAL (exit 0)` for both | a tab and a quote-depth difference still refuse the run |
| AC7 | **pass** | `ragged-prefix`, `outer-pipes`, `blockquote-table`, `list-indent-table`, `mixed-pipes` each run under `main`'s build and the branch's and `cmp`-ed; then 2978 all-outer-barred documents from the corpus | `branch == main byte-for-byte` five times; `documents whose every line is outer-barred: 2978 \| branch != main among them: 0` | `ragged-prefix` also confirmed unchanged against its own input |
| AC8 | **pass** | `python3 -m unittest tests.test_fixtures`; `git diff --name-status main..HEAD -- tests/fixtures/`; a per-fixture differential over the 33 pre-existing pairs | `Ran 19 tests`, `OK`, exit 0; fourteen `A` lines and no `M`; `pre-existing fixtures compared: 33; differing branch vs main: 0` | no `.out` file edited — `git status --short tests/fixtures/` empty after the run |
| AC9 | **pass** | `python3 -m unittest discover -s tests -t .` on `main` and on the branch; test inventories compared by name; `git diff main..HEAD -- tests/` read | `Ran 65 tests`/`OK` on `main`, `Ran 71 tests`/`OK` on the branch; 6 added, **0 removed**; assertion changes in exactly the two tests AC9 names | see `### AC9, reconciled` — the two relocations AC9 declares are present and both still pass |
| AC10 | **pass** | the same 56-document sweep as AC4, capturing stderr and the exit status of both passes | `stderr non-empty: 0; non-zero exit: 0` | includes every document mdtab declines to lay out |

Every criterion was already ticked in `item.md` by the first verification. All ten pass again at
`63e072d`, so all ten stay ticked; none was ticked on the strength of the earlier run.

### AC1, clause by clause

AC1 is a definition, so it was decomposed into the five things it asserts and each was probed with
a document chosen to distinguish it from the obvious wrong implementation.

| clause | document | output | verdict |
|--------|----------|--------|---------|
| the shared prefix is the **longest common prefix of the lines' prefixes**, not any one line's | `>   a \| b` / `>  ---\|---` / `>    ccc \| d` — prefixes `> ␣␣␣`, `> ␣␣`, `> ␣␣␣␣` | `>  a   \| b$` / `>  ----\|--$` / `>  ccc \| d$` | **pass** — output sits at `> ␣␣`, the common part, not at the first line's prefix and not at the delimiter's |
| what follows the shared prefix must be **spaces and nothing else** | `  a \| b` / `\t---\|---` / `  c \| d` | byte-for-byte | **pass** |
| the spaces past it **belong to the first cell** and go with its other leading spaces | `    a \| b` / `---\|---` / `  cc \| d` | `a  \| b$` / `---\|--$` / `cc \| d$` | **pass** — column 1 is 2 wide, the width of `cc`; had the four spaces counted as content it would be 5 |
| a run with **any other difference** is reproduced byte-for-byte | AC6's two documents | unchanged | **pass** |
| a run's **extent is fixed by WI-0001 AC7 before prefixes are compared** — so a prefix change disqualifies the run rather than splitting it | `a \| b` / `---\|---` / `c \| d` / `\tx \| y` | `whole run left byte-for-byte (not split)` | **pass** — the first three lines are a perfectly good table and are still not laid out |

### AC9, reconciled

`main` runs **65** tests and the branch runs **71**; the six added are all of `SharedPrefixTest`,
and comparing the two inventories by name shows **nothing removed**, so every one of the 65
pre-existing tests still exists and still passes.

Four pre-existing tests have a changed body. AC9 names two and declares the other two:

1. `PaddingPlacementTest.test_ac10_…` — final assertion `assertIsNone(lay_out(laid_out))` becomes
   `assertEqual(lay_out(laid_out), laid_out)`. AC9 entry 1. Its first two assertions are untouched.
2. `ContentPreservationTest.test_ac11_…` — splits on `|` after removing each line's leading run of
   space, tab and `>`, via a locally defined `without_indent`. AC9 entry 2.
3. `RejectionTest.test_rule_2_…` — loses its extra-space assertion.
4. `RejectionTest.test_rule_4_…` — gains exactly that assertion.

3 and 4 are the relocation AC9's *"Unchanged in substance though it moves"* paragraph declares.
`git diff` confirms the moved line is character-identical, that no assertion is deleted, and that
both tests pass. **Recorded slip, not a defect:** AC9's checking clause says *"exactly two of its
65 tests change; all other 63 pass unmodified"* while its own prose accounts for four changed
tests, two of which it declares not to count. Both readings pick out the same code, because AC9
*names* every test involved, so the criterion is still decidable and passes on either. The wording
is worth fixing the next time this item's criteria are touched; it is the fourth criterion in
EP-001 to count artefacts and need reconciling afterwards (WI-0001/Q-005, WI-0002/Q-003,
WI-0003/Q-002, and now this), and the first verification recorded it too.

The one substantive spot-check of WI-0002 outside the suite, because AC9's claim is about criteria
and not only about tests: `| left | centre | right |` under `|:---|:---:|---:|` comes back
`| left   | centre |  right |` / `|:-------|:------:|-------:|` / `| a      |   b    |      c |`,
and `x|y` under `:---:|---:` comes back `  x    | y$` / `:-----:|-:$` / `longer | z$` — left,
centred and right all honoured, markers kept.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 71 tests in 0.090s`, `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -W error -m compileall -q mdtab tests` → no output, exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 4 item(s), 10 document(s)`, `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | the `## Criteria` table gives, for all ten, a command run in this execution and its actual output. `impl-report.md` was opened only after the table was complete, and is cited nowhere in it |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` |
| `tests-would-fail-without-the-change` (advisory) | **pass** | see `## Test sensitivity check` |

## Negative and boundary cases exercised

Every one of these was **run**, not read about.

| case | command | what happened |
|------|---------|---------------|
| a tab where the other rows have spaces | `printf '\ta \| b\n  ---\|---\n\tc \| d\n' \| python3 -m mdtab \| diff - -` | byte-for-byte; the run is refused |
| a difference in quote depth | `printf '> a \| b\n>> ---\|---\n> c \| d\n'` | byte-for-byte |
| a non-space difference **past** the shared prefix | `printf '  a \| b\n\t---\|---\n  c \| d\n'` | byte-for-byte |
| a prefix change part-way through a longer run | `printf 'a \| b\n---\|---\nc \| d\n\tx \| y\n'` | the **whole** run left alone — not split into a laid-out head and an untouched tail |
| an outer-barred row with an extra space before its `\|` (`ragged-prefix`) | the fixture through both builds | unchanged, and identical to `main` — refused now by WI-0001 AC14 rather than by the prefix rule, which is what AC7 predicts |
| a run whose delimiter row is the **deepest**-indented line | `printf 'a \| b\n   ---\|---\nc \| d\n'` | `a \| b` / `--\|--` / `c \| d` — laid out at the shared prefix, which here is empty |
| the empty run (`shared_prefix([])`) | `SharedPrefixTest.test_an_empty_run_is_total_rather_than_an_error` | returns `""`; does not raise. Unreachable through `lay_out`, which is why it is a unit test |
| a document with a blank, pipe-free line after the table | the corpus' first differing document, `' a \| a\n  -\|---\n  \n'` | run ends at the blank line, the two-line table above it is laid out |
| every document the tool declines to lay out, for stderr and exit status | the 56-document sweep, both passes | `stderr non-empty: 0; non-zero exit: 0` |

## Differential against the trunk

`main` is `2884f53` — this branch's base — and both builds were driven through
`mdtab.filter.format_document` on the same 6000 generated documents (seed `20260829`; prefixes
drawn from `""`, `" "`, `"  "`, `"   "`, `"> "`, `">  "`, `">"`, `"\t"`, `"> > "`, `"  > "`,
one to three columns, outer bars 60% of the time, mixed alignment markers, ragged rows).

```
documents: 6000 | branch differs from main: 54
  of those, main copied through unchanged: 54
  of those, branch changed the document:   54
documents main laid out: 28 | of those, branch output differs from main: 0
documents whose every line is outer-barred: 2978 | branch != main among them: 0
differing documents where a tab or a `>` changed: 0
```

Four claims, measured rather than argued:

- **Nothing `main` laid out changes.** All 28 are byte-identical — the "out of scope" promise that
  a run already laid out comes out unchanged.
- **Every document that changes moves out of the copy-through branch**, in that direction only.
  54 of 54 were reproduced unchanged by `main` and are laid out by the branch. There is no
  document the branch copies through that `main` laid out.
- **AC7 holds generally, not only on five fixtures.** Of 2978 documents whose every line is
  outer-barred, none differs between the two builds.
- **AC6 holds generally.** In no differing document does a line's prefix differ from its input's by
  anything but spaces.

## Test sensitivity check

Three mutations, each applied to a working copy, the suite run, and the file restored from a
pristine copy. `git status --short mdtab/` is empty afterwards.

| mutation | tests that failed | reads on |
|----------|-------------------|----------|
| rule 2 in `mdtab/table.py` reverted to `line_prefix(contents[0])` with the byte-identical check — i.e. ADR-0003's rule | **15 failures** across `FixtureRoundTripTest` and `AlignmentTest` on all six new documents, plus `PaddingPlacementTest.test_ac10_…` | AC1, AC2, AC3, AC5 |
| `shared_prefix`'s space-only guard deleted, so any prefix difference is accepted | **2 failures**: `test_a_tab_one_line_has_and_another_does_not_is_no_shared_indent`, `test_a_difference_in_quote_depth_is_no_shared_indent` | AC6 |
| `shared_prefix` takes the longest common prefix of the **lines** instead of their prefixes | **92 failures, 5 errors** — including `test_the_shared_prefix_stops_where_the_indent_does`, which is the test written for exactly this | AC1, and the layout criteria of WI-0001 |

The second mutation's result is worth stating plainly, because it is a **negative** finding about
coverage and not a reassuring one: it is caught by two unit tests and by **no fixture**. A document
built to isolate rule 2 is refused by rule 1 or rule 4 in the mutated build as well, so it passes
either way. That is precisely the reason `SharedPrefixTest` calls the function directly, and it
means AC6's document-level evidence (the `quote-depth` and `tab-prefix` fixtures) demonstrates the
behaviour without isolating the rule that produces it. The first verification recorded the same
result; it reproduces.

## Diff read against the plan

`git diff main..HEAD -- mdtab/ tests/` read hunk by hunk. Every hunk maps to a plan step:
`shared_prefix` and its module docstring → step 1; the import swap and rule 2 in `lay_out`, plus
the `has_leading_pipe` and `_outer_style` docstrings → step 2; fourteen fixture files → step 3;
`SharedPrefixTest` → step 4; `test_ac10_…` → step 5; the rule 2 / rule 4 comment and relocation →
step 6; `without_indent` and `test_ac11_…` → step 7.

**One hunk traces to nothing in `plan.md`**, and it is declared here rather than left for the next
reader to find: the module docstring of `tests/test_units.py` (`ADR-0003` → `ADR-0008`) and
`RejectionTest`'s class docstring, changed at `2c39bc4`. They trace to `review.md`'s D12 audit,
which found four citations pointing at a superseded ADR, and `implement`'s SKILL.md makes the
review's finding list the authority for a resumed run. No assertion, no behaviour and no test name
is affected, and the new text is true: ADR-0008 restates all four recognition rules and owns rule 2.
Recorded, not raised — but the mismatch between `no-unplanned-scope`'s wording ("every hunk traces
to an AC or a plan step") and what a post-send-back run can offer is real, and it is in the journal.

Nothing else in the diff is unaccounted for. No behaviour is present that no criterion describes.

## Defects found

None. No bug item filed, no send-back.

## Not verified, and why

1. **`docs/` is not verified here, by design.** Whether `overview.md` and `vision.md` now describe
   the merged tool is **D7 and D12**, which belong to `review-close`; they are not acceptance
   criteria of this item, and a verifier who passed judgement on them would be pre-empting the
   gate that rejected this item last cycle. Worth knowing for whoever runs that gate:
   `lint-claims --changed-since main` is **structurally vacuous for this item** — `plan` committed
   ADR-0008 and the `overview.md` edits on the trunk at `2884f53`, before the branch was cut, so
   the branch changes no document the gate can see. It passed for me on that basis both times.
2. **The shipped fixtures' expected outputs were not independently re-derived.** The suite asserts
   the code reproduces them. This run bounds the risk differently from the first: the 33
   pre-existing pairs were also driven through `main`'s build and the branch's and compared to each
   other, so a wrong expected output would have to be wrong in a way that predates this branch
   *and* that none of the ten criteria detects. Not removed — bounded. Carried from WI-0001's
   `## Notes`.
3. **The CPython 3.8 floor in `plan.md` is asserted, not tested.** Only CPython 3.12.3 is
   installed. Unchanged from WI-0001, and this item's diff adds no 3.9+ construct.
4. **AC9's arithmetic slip is recorded, not repaired.** See `### AC9, reconciled`. Repairing a
   criterion is not a verifier's move, and no question was filed because both readings of the
   clause select the same code and the criterion is decidable on either.
5. **The corpus is generated, not exhaustive.** 6000 documents of one to four lines with a fixed
   seed. It supports AC7's and AC6's general claims far better than five fixtures do, and it is
   still a sample: it contains no fenced code block, no CRLF, no undecodable byte and no document
   longer than four lines. Those are covered by the shipped fixtures, which all pass, but not by
   the differential.
6. **Concurrency, very large inputs and pathological documents remain unexercised.** No criterion
   mentions them; the longest document any run of mdtab has seen in this project is 27 lines.
