# Verification report — WI-0002

Verified-commit: c73f039b31bdc676ab6815755d18d3a6ef1f25ab

## Verdict

**Pass.** All eleven acceptance criteria are met. Every verdict below rests on a command run
against the branch head `wi/WI-0002` at `c73f039`, driving `python3 -m expenses` over scratch
ledgers built with the real `add-person`, `add-expense` and `repay` commands — not on the test
suite and not on `impl-report.md`. AC3 was checked with an independent script that parses the
printed report and recomputes the arithmetic from the JSON ledger without importing
`expenses.debts`. No defect was found in this item, and no bug item was filed against another.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | the AC2 ledger, then `python3 -m expenses --file /tmp/v2/ac2.json debts`; `md5sum` of the ledger before and after; a second ledger recording an expense as `--payer " ANA " --shared-by ana --shared-by BEN` | three lines, each `<name> owes <name> <n>.<nn>`, exit 0, stderr empty; `f082a57c…` both times; `Ben owes Ana 5.00` | the form, the exit code, the positive amounts, the untouched data, and names printed as first typed |
| AC2 | **pass** | the six commands the criterion states, then `debts` | `Ben owes Ana 10.00` / `Cara owes Ana 10.00` / `Cara owes Ben 6.00`, exit 0 | byte-for-byte the three lines in the stated order |
| AC3 | **pass** | `python3 /tmp/v2/check_ac3.py <ledger>` over thirteen ledgers — AC2, AC6, AC7, AC8, AC9, AC10, AC11, an empty file, a missing file, both ordering ledgers, the mixed-case one and `ADR-0009`'s | e.g. `ac2.json: 3 line(s); net sum = 0; mismatched people = none`, and the same for every other ledger | the script parses stdout back into minor units and recomputes each person's net position from the JSON by `ADR-0002`'s rule as `ADR-0009` reads it. It imports nothing from `expenses.debts` |
| AC4 | **pass** | `debts` against (a) a path with no file, (b) a ledger holding three people and nothing else, (c) the AC2 ledger with every debt repaid | `Nobody owes anybody.` and exit 0 in all three | the exact string, and it is printed rather than nothing |
| AC5 | **pass** | two purpose-built ledgers where a sort on the display forms would give a different answer: people `ana`/`Ben`/`Cara` (debtor column) and `Ben`/`ana`/`Cara` (creditor column); plus `debts` twice over unchanged data, diffed | `ana owes Ben 10.00` / `ana owes Cara 6.00` / `Cara owes Ben 10.00`; `Cara owes ana 10.00` / `Cara owes Ben 15.00`; the two runs `diff`ed clean | `C` sorts before `a` in ASCII, so both ledgers would come out reversed under a display-form sort. They do not |
| AC6 | **pass** | the AC2 ledger plus `repay --from Ben --to Ana --amount 10.00` and `repay --from Cara --to Ana --amount 12.00`, then `debts` | `Ana owes Cara 2.00` / `Cara owes Ben 6.00`, exit 0 | the Ben/Ana pair disappears, the Cara/Ana pair has reversed |
| AC7 | **pass** | the AC2 ledger with all three debts repaid exactly, then `debts`, then `debts \| grep -c "0.00"` | `Nobody owes anybody.`; grep count `0` | no zero-amount line anywhere in the output |
| AC8 | **pass** | the three-expense circle, then `debts`; separately, the net positions recomputed from that ledger | `Ana owes Cara 10.00` / `Ben owes Ana 10.00` / `Cara owes Ben 10.00`; `{'ana': 0, 'ben': 0, 'cara': 0}` | every net position is zero and three lines are still printed, which is the case AC4 must not swallow |
| AC9 | **pass** | `--payer Ana --amount 10.00 --shared-by Ana --shared-by Ben --shared-by Cara`, then `debts` | `Ben owes Ana 3.33` / `Cara owes Ana 3.33` | 6.66 printed, 3.34 left with Ana |
| AC10 | **pass** | Ana and Ben, no expenses, `repay --from Ana --to Ben --amount 5.00`, then `debts` | `Ben owes Ana 5.00` | the debt is the other way round from the repayment |
| AC11 | **pass** | (a) three people, nothing else, `debts`; (b) `add-person Dan` on the AC2 ledger, then `debts` | (a) `Nobody owes anybody.`, exit 0; (b) the same three AC2 lines, no mention of `Dan` | an uninvolved person neither adds a line nor suppresses the empty-report message |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK`, run by this skill on the branch head |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. It is a syntax check and nothing more (`ADR-0005`), so a green result here says every file parses |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 5 items, 11 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the Criteria table: each row names a command this skill ran and quotes its actual output. `impl-report.md` is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | see the section below — six conditions triggered, not read about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | seven mutations, below |

## Negative and boundary cases exercised

| condition | command | result |
|-----------|---------|--------|
| the ledger file does not exist | `python3 -m expenses --file /tmp/v2/missing.json debts` | `Nobody owes anybody.`, exit 0 — a missing file reads as an empty ledger, as for every other command |
| the ledger is not valid JSON | `echo '{not json' > broken.json`; `debts` on it | `error: the ledger at …/broken.json is not valid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)` on stderr, exit 1 |
| the ledger cannot be read | `chmod 000` on a good ledger, then `debts` | `error: cannot read the ledger at …/locked.json: [Errno 13] Permission denied`, exit 1 — the report does not treat an unreadable file as empty |
| people recorded, nothing else | `debts` on a three-person ledger | `Nobody owes anybody.`, exit 0 |
| every debt repaid | three exact repayments, then `debts` | `Nobody owes anybody.`, and no `0.00` in the output |
| `--file` placed after the subcommand | `python3 -m expenses debts --file …` | `error: unrecognized arguments: --file …`, exit 2 — the documented global-option rule holds for `debts` too |
| an option `debts` does not have | `python3 -m expenses --file … debts --all` | `error: unrecognized arguments: --all`, exit 2 |
| an uneven split whose payer is not a sharer | `--payer Ana --amount 10.01 --shared-by Ben --shared-by Cara`, then `debts` | `Ben owes Ana 5.00` / `Cara owes Ana 5.00`; the AC3 script reports `net sum = 0`, `mismatched people = none`. This is `ADR-0009`'s case, and it behaves as the ADR says |

## Test sensitivity check

Seven mutations, each applied to the branch-head source and reverted afterwards. Every one was
caught, and the failures land on the criteria they should:

| # | behaviour disabled | tests that failed |
|---|--------------------|-------------------|
| M1 | sort on the display forms rather than the case-folded ones | 2 — both `TestOrdering` case tests (AC5) |
| M2 | ignore every repayment | 11 — `TestBalance` on `AC6`/`AC7`/`AC10`/`MIXED_CASE`, and the AC6, AC7 and AC10 worked examples at both levels |
| M3 | keep the zero balances, so a squared-up pair prints a `0.00` line | 8 — `test_no_debt_is_zero_or_negative`, and the AC6 and AC7 examples |
| M4 | round the share up, so the sharers absorb the remainder instead of the payer | 5 — AC9 at both levels, `ADR-0009`'s case, and `TestBalance` on the two uneven ledgers (AC3, AC9) |
| M5 | print nothing instead of `Nobody owes anybody.` | 4 — all three `TestNobodyOwesAnybody` cases plus the missing-file case (AC4, AC7, AC11) |
| M6 | print the case-folded key rather than the form first typed | 17 — every exact-output test (AC1, AC2, AC5, AC6, AC8, AC9, AC10) |
| M7 | invert the direction of every line | 22 — every exact-output test and `TestBalance` on six ledgers (AC1, AC2, AC3, AC6, AC8, AC9, AC10) |

Every criterion is covered by at least one mutation: AC1 by M6/M7, AC2 by M6/M7, AC3 by M2/M4/M7,
AC4 by M5, AC5 by M1/M6, AC6 by M2/M3, AC7 by M2/M3/M5, AC8 by M6/M7, AC9 by M4, AC10 by M2/M7,
AC11 by M5.

One hazard worth recording, because it is a property of mutation testing here rather than of this
item: M7's replacement line is the same length as the original and was reverted within the same
second, so `__pycache__` kept serving the mutated bytecode and the suite reported 22 failures
against a working tree `git status` called clean. Removing `expenses/__pycache__` and `tests/__pycache__`
restored `Ran 115 tests … OK`. Anyone repeating this check should clear the caches between
mutations rather than trusting the timestamp invalidation.

## Defects found

None. No criterion of this item failed, and nothing in the diff reaches behaviour delivered by
another item, so no bug was filed.

Two observations that are **not** defects and were deliberately not filed:

- `expenses/cli.py`'s module docstring still opens "the only module that prints, and the only one
  that exits", and the second half is false — `main` returns an `int` and `__main__.py` raises the
  `SystemExit` [src: expenses/cli.py; expenses/__main__.py]. `impl-report.md` declares this under
  `## What I did not do`, and `docs/architecture/overview.md` v3 records `review-close` correcting
  the same sentence in the overview for WI-0001. It is a comment, not behaviour, so no acceptance
  criterion of any item is violated and there is nothing to reproduce.
- `debts.py` handles two states no criterion reaches — an expense with an empty sharer list, and a
  name on a record that is not in `people`. Both are only reachable by hand-editing the ledger, and
  both are recorded as reversible assumptions in `plan.md`. They are declared, not undeclared
  scope, so they are not a `no-unplanned-scope` finding.

## Not verified, and why

- **Concurrency.** Two processes running `debts` against the same ledger while a third writes to it
  was not tested. No criterion of this item mentions it, and `ADR-0003`'s single-process,
  single-file model does not claim it.
- **Scale.** The largest ledger exercised has four people and three expenses. AC3's identity was
  checked on thirteen small ledgers, not on a generated large one, so "accounts for every recorded
  minor unit" is verified in the cases the criteria name plus a few boundary ones — not
  exhaustively. `plan.md`'s risks and `ADR-0003` both note that scale is out of this project's
  frame.
- **The default ledger location.** Every check used `--file`, so `EXPENSES_LEDGER` and the XDG
  default path were not exercised for `debts`. They are WI-0001 AC9's territory and `debts` shares
  the same `store.resolve_path` call as every other command [src: expenses/cli.py].
- **Terminal rendering.** Output was captured through a pipe. No criterion mentions colour, width
  or a terminal, and the implementation prints plain lines.
