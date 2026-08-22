# Review — WI-0003

## What I examined

- **The record's mechanics.** `history.md` — nine rows chaining without a gap (two of them the
  `intake`→`answer-questions` suspensions from before this turn), the last matching `item.md`.
  `journal.md` — eight entries against eight actors. Three questions, all `answered` with
  `## Consequences` naming files that exist. Nine criteria, nine ticks.
- **Verification freshness.** `check-verify-freshness WI-0003 wi/WI-0003` → *"verified at
  e8a82310; wi/WI-0003 has moved to 0a0312a9 but only the record changed (5 file(s) under tracker/
  or docs/)"*.
- **The diff, hunk by hunk:** `expenses_tool/settle.py` (new — `shares`, `balances`, `settle`),
  `expenses_tool/cli.py` (+`render_balance`, `render_payment`, `cmd_report`, `NOBODY_OWES`, one
  subparser), `tests/test_settle.py`, `tests/test_cli_report.py`, `README.md`, and the tracker.
- **The declared gaps:** `verify-report.md` `## Not verified, and why` (six entries) — read
  closely, because one of them is a finding about a criterion rather than about the code — and
  `impl-report.md` `## What I did not do` (five) and `## Deviations from the plan` (two).
- **The trial merge:** `wi/WI-0003` into a throwaway branch off `main`, both project commands run
  on the merge result.

Where each hunk earns its place:

| hunk | serves |
|------|--------|
| `settle.shares` | plan step 2; AC6; ADR-0001 clause 2 |
| `settle.balances` | plan step 1; AC1, AC3, AC7, AC8; ADR-0001 clause 3, ADR-0009 clause 3 |
| `settle.settle` | plan step 3; AC1, AC3; ADR-0010 clause 2 |
| `cli.render_balance`, `cli.render_payment` | plan step 4; AC2, AC6, AC7; ADR-0008 clause 3 |
| `cli.cmd_report` and `NOBODY_OWES` | plan step 5; AC1–AC9 |
| the `report` subparser | plan step 6; AC1 |
| `tests/test_settle.py` | plan step 7, including three property tests |
| `tests/test_cli_report.py` | plan step 8; one class per criterion |
| `README.md` | plan step 9 |

Nothing is unaccounted for, and nothing contradicts an ADR: no float touches an amount (ADR-0001),
every user-visible string is in `cli.py` (ADR-0008 clause 3), `settle.py` neither prints nor exits,
the sort key is `store.normalise` throughout (ADR-0003 clause 4), and the printed order is the one
ADR-0010 clause 4 fixes.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | nine `- [x] AC`, no `- [ ] AC` |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | nine rows, each with a command and quoted output, including `cat -A` output showing the blank line and the absence of trailing whitespace |
| D3 | gates passed on the final state of the code | **pass** | `implement` on `a830980`, `verify` on `e8a8231`, this review on the trial merge result: `Ran 87 tests … OK`, `compileall` exit 0 |
| D4 | no open blocking question | **pass** | Q-001, Q-002, Q-003 all `answered` |
| D5 | a journal entry per execution; history chains | **pass** | eight entries, eight actors; `validate-workspace` exit 0 |
| D6 | design decisions in ADRs, cited | **pass** | ADR-0010 created by `plan`, cited from `plan.md`, from the overview's table, and from `settle.py`'s module docstring |
| D7 | documents the change invalidated are updated | **pass** | `overview.md` v2→v3 (the `settle` module, the `report` command, and a new section stating the report stores nothing); `README.md` gained "Who owes whom" and its "what it does not do yet" line now names only the import |
| D8 | every commit references the item | **pass** | `check-commit-refs` → *all 3 commit(s) on main..wi/WI-0003 name WI-0003* |
| D9 | merged into the trunk | **pass** | merged after this review and after closing |
| D10 | verification postdates the code | **pass** | `check-verify-freshness`, quoted above |
| D11 | the review record says what was examined | **pass** | this section, with the per-hunk table |
| D12 | claims in `docs/` about this behaviour are still true | **pass** | re-read `overview.md` §"What the report does" against `cmd_report`: it loads, computes, prints and returns, and calls no writer — `grep -n "store.save" expenses_tool/cli.py` finds it only in `cmd_add_person` and `cmd_add_expense`. The README's worked example was run as written and produced the output it shows, and its claim about the penny rule matches ADR-0001 and AC6 |

## Findings

Three. One is a defect in a **criterion** rather than in the code, and it is the reason this review
took longer than the last.

1. **AC9 cannot detect the regression it exists to prevent, and that is now recorded on the item.**
   `verify` found it and said so plainly: adding `store.save(path, data)` to `cmd_report` breaks no
   test, because the file is rewritten with identical bytes and AC9 asks only that `cmp` show it
   unchanged. I checked the finding rather than accepting it — the sensitivity edit is one line and
   the criterion's wording is unambiguous — and it is real.
   **This is not a send-back.** The delivered behaviour is correct: `cmd_report` contains no
   `store.save`, and `verify` established that independently by inode and mtime. Nothing is wrong
   with the code, so returning it to `in-progress` would ask a developer to fix nothing. Nor is it
   mine to amend: only `refine` and `answer-questions` may change a criterion, and the honest
   record is that the criterion is weaker than its own heading. It is written into the item's
   `## Notes` so that a future execution touching `report` knows the test suite will not catch this
   class of change.
2. **`cmd_report` has two exits that print the same sentence.** It reads slightly oddly on the page
   and it is correct: AC4 asks for the sentence alone when nothing is recorded, and after the
   balances when everything cancels. The constant `NOBODY_OWES` is what keeps the two in step, and
   the comments say which criterion each branch serves. Noted so nobody "simplifies" it into one
   branch that prints balances in both cases.
3. **`settle.settle` returns payments in emission order and the caller sorts them.** Declared as a
   deviation-adjacent choice in `impl-report.md`; ADR-0010 clause 4 puts the print order in the
   caller deliberately, so the algorithm's shape never reaches the screen. Reviewed as correct, and
   the sensitivity check confirms the sort is load-bearing (removing it failed a test).

Nothing here would be uncomfortable to maintain. `settle.py` is thirty lines of arithmetic with the
two ADRs it implements named in its docstring, and the property tests — shares always sum to the
amount, payments always clear the balances, the count never exceeds `n-1` — are exactly the claims
the criteria make about all data rather than about an example.

## Accepted gaps

Recorded in the item's `## Notes` under "Accepted gaps at close":

- **AC9's insensitivity**, as above: no test in the suite would fail if `report` began writing the
  file back with identical content. The behaviour is right today and was checked by inode and
  mtime.
- **Which settlement is printed when several are minimal.** ADR-0010 decides it; no criterion
  constrains it. Greedy can occasionally emit one payment more than a perfect solver.
- **Behaviour with a very large group** — every check used three or four people.
- **A hand-edited ledger naming a sharer who is not registered** would be reported rather than
  refused. ADR-0009 clause 5 says it cannot arise through the tool; a text editor can produce it.
- **`argparse`'s usage wording** is unchecked; only exit code 2 is fixed.
- **Style, as opposed to syntax** — `commands.lint` is `compileall` (ADR-0007 clause 4).
- **The report describes the ledger, not the settling-up.** After Cass pays Ana, the report still
  says Cass owes Ana, because recording a settlement is out of scope for EP-001. The README says
  so; it is repeated here because it is the thing a real user is most likely to be surprised by.

## Verdict

**Accepted.** The report does what WI-0003's criteria say, both quoted reports are reproduced
exactly, and the arithmetic was re-derived by hand on a ledger the criteria do not mention. The one
finding that matters is about a criterion rather than the code, and it is now on the item where the
next execution will see it rather than in a verification report nobody reopens.
