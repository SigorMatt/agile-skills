# Implementation report — BUG-0001

## What was built

Two rendering functions in `envel/summary.py`, and four call sites changed to use them. Nothing
else in the tool changed: no sum, no stored figure, no file format, no command line, no refusal.

- `left_column(cents)` [src: envel/summary.py:72] returns a summary row's last column —
  `left 60.00` when the balance is at or above zero, `short 250.00` when it is below.
- `balance_line(name, cents, moment, verb, month)` [src: envel/summary.py:222] returns the
  sentence that brackets a listing — `groceries held 0.00 at the start of 2026-08` and
  `groceries holds 50.00 at the end of 2026-09` unchanged, and
  `groceries was 250.00 short at the end of 2026-08` when the month closed short.
- `row()` calls `left_column()` for the fourth column and formats the other three itself
  [src: envel/summary.py:104]; `list_entries()` calls `balance_line()` for its opening and closing
  lines [src: envel/summary.py:279] [src: envel/summary.py:294].

Both helpers pass the **magnitude** to `money.format_amount`, so an amount still becomes text in
exactly one place [src: ADR-0001] and the figure stays readable rather than being clamped
[src: BUG-0001 AC6 "The worded closing line still reconciles"]. `figures()`, `bounded_balance()`,
`balance_before()` and `balance_through()` are untouched and still return signed cents, which is
`ADR-0012`'s first decision and the reason `WI-0003` AC3's reconciliation is still a property of
the arithmetic [src: ADR-0008].

Transaction figures keep their signs, deliberately: a spend's own line still reads `-250.00`, the
side a move left still reads `-30.00`, and the summary's `moved` column still reads `-20.00` for
an envelope that only gave money away [src: ADR-0012].

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — no amount below zero on either balance line of `envel entries` | `balance_line()` words the case below zero; both bracket lines of `list_entries()` go through it | `tests.test_entries.AMonthThatClosedShort.test_the_closing_line_says_how_short_it_was_instead_of_a_minus`, `...test_no_balance_line_carries_a_negative_amount`, `...test_the_opening_line_of_the_next_month_says_it_too`, `...test_a_month_that_did_not_close_short_is_unchanged`. At the command line, the bug's steps 1–6 → `groceries held 0.00 at the start of 2026-08` / `groceries was 250.00 short at the end of 2026-08`, exit 0 |
| AC2 — no amount below zero in any column of the `envel summary` row | `left_column()` words the fourth column; the other three are unchanged and are `0.00`, `250.00` and `0.00` in this scenario | `tests.test_summary.AMonthThatClosedShort.test_the_row_says_how_short_the_month_closed`, `...test_no_column_of_the_row_carries_a_negative_amount`. At the command line, steps 1–4 plus step 7's `created` probe → `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`, exit 0 |
| AC3 — the input is not refused | no step touched the write path; `envel/envelopes.py` and `envel/cli.py` are absent from the diff | `git diff main...wi/BUG-0001 --name-only` → `envel/summary.py`, `tests/test_entries.py`, `tests/test_summary.py` and files under `tracker/`, and nothing else. At the command line, step 4 → `spent 250.00 from groceries, which now holds 50.00` on stdout, nothing on stderr, exit 0; `envel list` afterwards → `groceries  50.00` |
| AC4 — a test for AC1 and a test for AC2, both failing at `127664a` and passing after | two new classes, both written against `summary.list_entries` and `summary.summarise` rather than against the helpers, so they fail on behaviour and not on an `AttributeError` | `git stash push envel/summary.py` then `python3 -m unittest tests.test_entries.AMonthThatClosedShort tests.test_summary.AMonthThatClosedShort` → **FAILED (failures=6)** of 11; `git stash pop` and the same command → **OK**, 11 tests |
| AC5 — the four delivered test modules run unmodified | the new tests are appended classes; the only other change to a test file is one `import re` line inserted in `tests/test_entries.py` | `git diff 127664a --stat -- tests/` → `tests/test_entries.py | 69 +++`, `tests/test_summary.py | 55 +++`, *2 files changed, 124 insertions(+)* and no deletions; `git diff 127664a -- tests/ \| grep -c "^-[^-]"` → `0`, so no assertion existing at `127664a` was edited and `tests/test_envelopes.py` and `tests/test_corrections.py` are untouched. `python3 -m unittest discover -s tests -t .` → exit 0, 310 tests, OK |
| AC6 — the worded line still names `250.00`, not `0.00` | the helpers render `abs()` of the figure the arithmetic produced; nothing clamps | `tests.test_summary.AMonthThatClosedShort.test_the_arithmetic_was_not_clamped` asserts `figures()` still returns `left == -25000` and that `got_in - spent + moved == left`; `tests.test_entries.AMonthThatClosedShort.test_the_worded_figure_is_the_one_the_arithmetic_produced` asserts `balance_before + sum(entry lines) == balance_through` and that the printed line carries the magnitude of that closing figure |

## Documents

No document under `docs/` was written on this branch: `git diff main...wi/BUG-0001 --name-only -- docs/`
prints nothing. Every row of the plan's invalidation set was reopened and read against the change.

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/product/vision.md` | the v8 paragraph: *"`envel entries` and `envel summary` say how short the month closed, in words, rather than printing a negative"* | cited-fact | `verified-still-true`, and this change is what made it true. Its citation `[src: BUG-0001/Q-001]` resolves to `tracker/items/BUG-0001/questions/Q-001.md`, whose answer names the sentence *"Groceries was 250.00 short at the end of 2026-08"*. The delivered closing line is that sentence exactly [src: envel/summary.py:238], and the delivered summary column is `short 250.00` [src: envel/summary.py:82] — which the paragraph describes rather than quotes, so it stays true of both | — |
| `docs/product/vision.md` | the paragraph sourced to `WI-0005/Q-004`: *"A correction that would take an envelope below zero is refused and says how short the envelope is"* | cited-fact | `verified-still-true`. It is about the **current** balance and the refusal that guards it, and this change touches neither: `envel/envelopes.py` is absent from the diff, and `tests/test_corrections.py` runs with no edit. Read against `ADR-0011` §Decision 5, which is the refusal it describes | — |
| `docs/product/vision.md` | `## Engagement state`, all four bullets | engagement-state | `owned-by-ending`. Not read for repair and not edited. `review-close` restates it at the ending | — |
| `docs/architecture/overview.md` | `## Conventions this project has adopted`: *"Amounts are printed with exactly two decimal places and no currency symbol"* | quantified | `verified-still-true` | — |
| | **Enumeration:** *"Amounts are printed with exactly two decimal places and no currency symbol"* | | | |
| | **Set:** every call in `envel/` that turns a number of cents into printed text | | | |
| | **Enumerated by:** `grep -rn "format_amount" envel/ --include=*.py` → 35 hits: `money.py:38` (the definition), 25 call sites in `envelopes.py`, 8 in `summary.py` (lines 82, 83, 101, 102, 103, 171, 238, 241), and `money.py:42` (the one arithmetic-to-text expression, inside the definition). Cross-checked for any conversion that bypasses it: `grep -rn "parse_amount\|:.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → only `money.py:20`, `money.py:42` and four `parse_amount` call sites in `cli.py` | | | |
| | **Members:** the two call sites this change added — `summary.py:82` (`short`) and `summary.py:238` (`was … short`) — plus the six that already existed in `summary.py` and the 25 in `envelopes.py` | | | |
| | **Verdict:** true of each. Both new members call `money.format_amount`, whose only expression is `"{}{}.{:02d}".format(sign, cents // 100, cents % 100)` [src: envel/money.py:42], so the amount has exactly two decimal places and no symbol. `tests.test_summary.AMonthThatClosedShort.test_the_row_says_how_short_the_month_closed` asserts the literal `short 250.00` | | | |
| | **Falsifier:** a member that builds an amount string itself — an f-string, a `round()`, a `:.2f` — instead of calling the formatter. The two new members are exactly where one would be, because each had to decide how to render a magnitude and could have written `str(-cents / 100)`; the grep above is what rules it out across all 35, and it is a grep over the whole package rather than a read of the two lines I wrote | | | |
| `docs/architecture/overview.md` | `## The parts`, the `envel/money.py` row: *"the only two places text and amounts meet: parse and format"* | quantified | `verified-still-true` | — |
| | **Enumeration:** *"the only two places text and amounts meet"* | | | |
| | **Set:** every function in `envel/` that converts between an amount and text, in either direction | | | |
| | **Enumerated by:** the same two greps as the row above. `grep -rn "parse_amount\|:.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → `money.py:20` (`parse_amount`), `money.py:42` (inside `format_amount`), and `cli.py:161`, `cli.py:167`, `cli.py:176`, `cli.py:183`, which are **calls** to `parse_amount` and not conversions | | | |
| | **Members:** `money.parse_amount` and `money.format_amount`, and no third | | | |
| | **Verdict:** true. The two functions this change added produce text *containing* an amount but do not convert one: each hands its cents to `money.format_amount` and concatenates words around the result [src: envel/summary.py:82] [src: envel/summary.py:238]. The sentence is about where the conversion lives, and it still lives in one module | | | |
| | **Falsifier:** a third place doing the arithmetic — `cents // 100` outside `money.py`. The grep covers the package and finds none; `summary.py` is where one would have appeared, because both new functions handle a sign and could have negated after formatting instead of before | | | |
| `docs/architecture/overview.md` | `## The parts`, the `envel/summary.py` row: *"the reports, both of them"* | cited-fact | `verified-still-true`. The module still owns exactly two reports — `summarise()` [src: envel/summary.py:108] and `list_entries()` [src: envel/summary.py:245]. The two functions added are rendering helpers called by those reports, not a third report: neither takes a `store` and neither is called from `envel/cli.py`, which is absent from the diff | — |
| `docs/architecture/overview.md` | `## What is not decided yet` | cited-fact | `to-update`, and **discharged by `plan`**, not by this execution: the section was repaired to v10 on `main` at `51a0a62`, in the commit that created `ADR-0012`. The row is in the set so that it names every path under `docs/` the item touched. Nothing on this branch changed it | 10 (by `plan`) |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | `owned-by-ending`. Not read for repair and not edited | — |
| `docs/architecture/adr/ADR-0008-...md` | `## Decision` 3's filter table and `## Consequences` first paragraph | cited-fact | `verified-still-true`. The table says `left` is the sum over months `<= M` and `spent` is `-cents` *"so the column prints positive"*; both still describe `figures()`, which is unchanged [src: envel/summary.py:51]. `## Consequences` says nothing **derives** the carried-in figure by subtraction — still true, `balance_before` is still the bounded sum [src: envel/summary.py:212]. Checked against `tests.test_summary.AMonthThatClosedShort.test_the_arithmetic_was_not_clamped`, which asserts the identity directly on the short month | — |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Consequences`: *"a module that prints an amount without going through the formatter shows the wrong thing"* | quantified | `verified-still-true`. Same set, same enumeration and same verdict as the `## Conventions` row above: `grep -rn "format_amount" envel/ --include=*.py` → 35 hits, the two new ones among them; no member bypasses the formatter; the falsifier is the same self-built amount string and the same grep rules it out | — |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `## Consequences`: *"`summary` prints nothing and calls no `sys.exit`"* | quantified | `verified-still-true` | — |
| | **Enumeration:** *"`summary` prints nothing and calls no `sys.exit`"* | | | |
| | **Set:** every statement in `envel/summary.py` | | | |
| | **Enumerated by:** `grep -n "print\|sys\.exit\|import sys" envel/summary.py` → 4 hits, at lines 25, 46, 75 and 226, every one of them prose inside a docstring (*"this module prints nothing"*, *"the date the listing prints beside it"*, *"never printed with a minus sign"* twice). No `print(` call, no `sys.exit`, no `import sys` | | | |
| | **Members:** the two functions added, `left_column` and `balance_line` | | | |
| | **Verdict:** true of both. Each is a single `return` of a `format()` expression and touches no stream | | | |
| | **Falsifier:** a `print(` in the module, or an `import sys`. The two new functions are where one would have been, because both were written to produce user-visible output and the temptation in that position is to print it; the grep is over the whole file rather than over what I wrote | | | |
| `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` | `## Decision` 5, the below-zero refusal on `fix` and `remove` | cited-fact | `verified-still-true`. It describes a refusal in `envel/envelopes.py`, which is absent from this branch's diff, and `tests/test_corrections.py` runs unmodified as part of the 310-test suite | — |

No row was added: `git diff main...wi/BUG-0001 --name-only -- docs/` prints nothing, so no document
outside the set was written and none was discovered mid-change.

## Deviations from the plan

- **Plan step 2 said the format string's trailing `left {}` becomes a bare `{}` filled by
  `left_column(left)`, with the other three columns *"unchanged and still coming from
  `money.format_amount`"`.** The existing `row()` produced all four with a starred generator over
  `figures()`, which cannot be mixed with a fifth argument of a different shape, so the three are
  now formatted by three explicit `money.format_amount` calls. This changes *how*, not *what*: the
  same three strings from the same function. `tests.test_summary.AMonthThatClosedShort.test_a_month_that_did_not_close_short_reads_as_before`
  and the delivered `tests/test_summary.py` assertions on whole rows are what hold that.
- **Plan step 5 asked for an assertion that no line matches `-\d`.** Written literally, that
  assertion fails on the *date*: `2026-08` contains `-0`. The test asserts instead that no
  whitespace-delimited **word** on a balance line begins with a minus and a digit, which is the
  same claim about amounts without being a claim about hyphens, and it required one
  `import re` in `tests/test_entries.py`.
- Nothing else. The four code edits are the plan's steps 1–4 as written.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, 310 tests, OK |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `validate-workspace .` → exit 0 |
| `every-criterion-has-a-test` | pass | the table above names a test function for AC1, AC2, AC4 and AC6, and an exact command with its output for AC3 and AC5. No criterion is demonstrated by reading code |
| `commits-reference-the-item` | pass | `check-commit-refs BUG-0001 wi/BUG-0001` → exit 0 |
| `no-unplanned-scope` | pass (advisory) | the diff is `envel/summary.py` (two functions added, four call sites changed), two appended test classes with one import, and `tracker/`. Every hunk traces to plan step 1, 2, 3, 4, 5 or 6 |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → exit 0 |
| `claims-are-sourced` | pass | `lint-claims --changed-since main --plan-documents BUG-0001` → exit 0 |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item BUG-0001 --changed-since main` → exit 0; 0 documents written under `docs/` on this branch, 6 named by the plan |

## What I did not do

- **I did not repair a single document**, and that is the honest outcome rather than an omission:
  every row of the invalidation set reopened as still true, and the one row that needed a repair
  was discharged by `plan` on `main` before this branch existed.
- **I did not touch `envel/money.py`.** `format_amount` keeps its minus sign, because transaction
  figures still need one [src: ADR-0012].
- **I did not tick any acceptance criterion in `item.md`.** That is `verify`'s
  [src: .claude/agile-skills/spec/work-item.md].
- **I did not change the `moved` column, the entry-line amounts, `envel list`, or any *"which now
  holds …"* message.** All four are named out of scope by the plan, and two new tests exist
  precisely to fail if a later change reaches them:
  `tests.test_entries.AMonthThatClosedShort.test_the_entry_line_still_carries_its_sign` and
  `tests.test_summary.AMonthThatClosedShort.test_the_moved_column_keeps_its_sign`.
- **I did not address the neighbouring finding** that a spend dated before its envelope existed
  appears in no summary row. It is recorded in `EP-001`'s `artifacts/review.md` and is not this
  bug.
