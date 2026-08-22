# Review — WI-0004

This is the **second** review of this item. The first rejected it on **D7** — `README.md` had never
been touched, so the tool's front door said the CSV import was "the next piece of work" and its
command table omitted the command. That review's findings, F1 to F6, are reproduced under
`## First review, and what happened to it` below, so the whole exchange is legible from one file.

## What I examined

- `item.md` (eleven criteria, all ticked), `history.md` (19 rows), `journal.md` (**all 21 entries**,
  including both self-corrections and both passes of `implement` and `verify`), `plan.md`,
  `impl-report.md` with its second-pass section, the rewritten `verify-report.md`, and all six
  questions.
- **The `README.md` diff, hunk by hunk** — the change this pass exists to judge. Nine hunks.
- **The source diff `main..80809a2`** re-read: `expenses_tool/cli.py`, `store.py`, `bankcsv.py` and
  the three test files, confirmed unchanged since the first review by
  `git diff 89cce7e..HEAD -- expenses expenses_tool tests` and by the fact that the last commit
  touching source or the README is `a49b5d3`, which precedes the verified commit.
- `docs/architecture/adr/ADR-0011`, ADR-0002, ADR-0005, ADR-0006, ADR-0009,
  `docs/architecture/overview.md` v5, `docs/product/vision.md` v11.
- The trial merge of `wi/WI-0004` into a throwaway copy of `main`, and the project's test and lint
  commands run **on the merge result**.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every AC ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 11; no unticked criterion remains |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | eleven rows, each naming a command run at the second verification against `89cce7e` and quoting its output. The report says explicitly that none was carried over from the first verification despite the source diff being empty — the verifier re-ran all eleven rather than infer them, and I checked that claim against the outputs quoted, which are this session's paths (`/tmp/reverify/…`), not the first pass's |
| D3 | gates passed on the **final** state of the code | **pass** | run by me, twice: on the branch head, and again on the trial-merge result — `python3 -m unittest discover -s tests -t . -q` → `Ran 145 tests … OK`, `python3 -m compileall -q expenses expenses_tool tests` → exit 0 |
| D4 | no open blocking question | **pass** | all six `status: answered` |
| D5 | a journal entry per execution; history chains | **pass** | history chains from `— → draft` to `verifying → in-review` with no gap and its last row matches `item.md`; `validate-workspace` exit 0, which decides both mechanically |
| D6 | design decisions in an ADR, cited | **pass** | ADR-0011, four options, reversibility stated in both directions; cited from `plan.md`, the plan journal entry, and comments in `store.py` and `bankcsv.py` |
| D7 | invalidated documents updated | **pass — this is what was fixed** | `docs/` was already right (`overview.md` v5, `vision.md` v11, each versioned and change-logged). `README.md` now carries the `import-csv` row, a full `### Importing from your bank` section, and the five corrected sentences. `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` returns nothing outside the `## What it does not do yet` heading |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → `all 10 commit(s) on main..wi/WI-0004 name WI-0004`, exit 0 |
| D9 | merged into the trunk | **pass** | trial-merged into a throwaway copy of `main` and tested there first, the trial discarded, the item closed while the branch was still unmerged, and then merged for real — the order step 8 requires, because `check-commit-refs` inspects `main..branch` and that range is empty once merged |
| D10 | verification postdates the last code change | **pass** | `Verified-commit: 89cce7e6…`. The last commit touching `expenses`, `expenses_tool/`, `tests/` or `README.md` is `a49b5d3`, which precedes it. The single commit after it, `80809a2`, was inspected with `git diff --stat` and touches only `tracker/`. Compared, not assumed — and this is the criterion the first review's rejection moved, so it mattered here |
| D11 | `review.md` states what was examined | **pass** | this file, and it carries the first review's findings rather than replacing them silently |
| D12 | every claim in `docs/` about this item's behaviour is still true | **pass** | re-read against the code: ADR-0002's reserved `import-csv` name is what shipped; ADR-0005's "a skipped row is a report, the import still exits 0" matches AC4; ADR-0006 clause 2's "no migration, no schema bump" holds — `SCHEMA_VERSION` is 1 and `load` does not insert `imports` when absent; ADR-0009's "the same record shape" holds, with AC3's byte-identical comparison as proof; `overview.md` v5's `{"sha256", "date"}` matches a real imported data file. **The scope finding from the first review stands**: D12 covers `docs/` only, and this project's user-facing documentation is `README.md`, which no Definition-of-Done criterion names |

## First review, and what happened to it

| # | finding | attributed to | status now |
|---|---------|---------------|-----------|
| F1 | line 158: "Importing a bank CSV export is the next piece of work" | WI-0004 | **fixed** — the sentence is gone; the paragraph kept its true half and gained the two things that genuinely are not done (no per-bank shortcut, nothing remembered between runs) |
| F2 | the `### Commands` table omitted `import-csv` | WI-0004 | **fixed** — a row with the full option list, verified by the verifier against `./expenses import-csv --help`, plus a new `### Importing from your bank` section placed after `### Who owes whom` |
| F3 | line 108: "the import command **will take** its people…" | WI-0004 | **fixed** — present tense |
| F4 | line 65: "Nothing here works out who owes whom yet", contradicted two lines later | WI-0003 | **fixed** — "Working out who owes whom is the next section" |
| F5 | line 4: "— once the report lands —" | WI-0003 | **fixed** — and the opening sentence now also says expenses can be typed in or imported |
| F6 | line 36: "**Both** accept `--data-file PATH`" with five commands listed | WI-0002/WI-0003 | **fixed** — "Every command accepts…", checked by the verifier against all six subcommands' `--help` |

The widening to F4–F6 was authorised in the first review and each is attributed above, so no other
item is credited with a fix it did not make. `implement` also added one row to the output-and-exit-
codes table for a partly-successful import, which nobody asked for and which it declared rather than
slipped in — I accept it: the table previously offered only "It worked → 0" and "Refused → 1",
neither of which describes an import that skipped three rows and still exited 0.

## Findings

**None that block.** Reading the nine README hunks against the code, every one traces to a numbered
finding above or to the declared exit-codes row, and every factual claim in the new prose was
executed by the verifier rather than read approvingly — the three console blocks reproduce verbatim,
which is the standard the first review's rejection set.

Two observations carried forward, neither a defect:

- **The code observation from the first review still stands.** `cmd_import_csv` builds its expenses
  in a comprehension over `expenses.record_expense`, which can raise `BlankDescription`. It cannot
  today, because `bankcsv._row` already rejects blank descriptions; if that rule were relaxed, the
  exception would become an uncaught traceback where every other error path is a clean refusal. No
  ledger is at risk, since nothing is written at that point.
- **Nothing in the test suite protects `README.md`.** The verifier found this and recorded it:
  `grep -rn "README" tests/` returns one comment. The defect that cost this item a round trip is
  invisible to every automated gate the project has, and fixing the README does not remove the
  exposure. Carried into the item's `## Notes` so it survives this closure, because it is the next
  person's problem as much as it was this one's.

## Accepted gaps

All are recorded in the item's `## Notes` as well as here, so they survive the item's closure.

- **AC7's "most recent import date" is not demonstrated end to end.** Every import in a session
  happens on one day. Covered by
  `tests/test_store.py::ImportedFiles::test_imported_on_returns_the_last_matching_date`.
- **Atomicity is not tested under a real interruption.** AC9 asks for an inspection, and the
  inspection passes: `bankcsv.py` contains no `open(`, `store.save`, `json.dump` or `os.replace`.
  Interrupting a write would test `store.save`, which is WI-0001's and unchanged.
- **Nothing is tested against the stakeholder's real bank export**, by their own decision. The two
  likeliest surprises are a quoted thousands separator (`"1,200.00"`) and charges written as
  negative amounts; both are skipped-and-reported under AC4 rather than silently mishandled, which
  is the safe failure. Either would be a new criterion, not a defect in this one.
- **A failing `store.save` still raises a traceback out of `main()`**, for every command in the
  tool. Pre-existing, covered by no criterion of any item, and not filed as a bug because
  `pipeline.yaml` permits `null → ready` for actor `verify` only — `review-close` cannot create a
  bug item without forcing a gate override.
- **The README has no automated guard**, as above.

## Verdict

**Accepted. Merged and closed, outcome `delivered`.**

The change does what the item asked and the record supports it. Eleven criteria, each verified twice
against two different commits by commands the report quotes; a design decision with an ADR that
states its reversibility honestly, including the part that is *not* reversible; a diff in which every
hunk traces to a criterion or a numbered finding; and 145 tests green on the merge result, not only
on the branch.

The round trip was worth its cost. What the first review caught was not a code defect — the code was
right both times — but a README that told the reader this feature did not exist, in the item that
completed an epic the stakeholder had held open through six askings to get it. That is the failure
mode D12 exists to name, occurring in the one document D12 does not cover.
