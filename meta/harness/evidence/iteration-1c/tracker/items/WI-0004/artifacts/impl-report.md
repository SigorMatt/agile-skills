# Implementation report — WI-0004

## What was built

`./expenses import-csv <FILE>`, on branch `wi/WI-0004`, in three commits that follow the plan's
first three steps in order.

- **`expenses_tool/bankcsv.py` (new, 186 lines).** Everything about reading a CSV and nothing else:
  `fingerprint(raw)` (the SHA-256 of the bytes, ADR-0011 clause 1) and
  `read(raw, *, date_column, amount_column, description_column, date_format)`, which returns the
  rows it accepted and the rows it skipped, or raises `NotDecodable`, `NoHeader` or
  `ColumnNotFound`. It never prints, never exits and never touches the data file. It contains no
  bank's column names, no default mapping and no auto-detection: every fact about the file arrives
  as an argument, which is what the stakeholder chose in WI-0004/Q-006.
- **`expenses_tool/store.py` (extended).** The `imports` key: `empty_data()` carries it,
  `load()` validates it as strictly as it validates people and expenses, and `imported_on()` /
  `record_import()` are the only two ways anything reads or writes it. `SCHEMA_VERSION` is
  unchanged at 1, per ADR-0006 clause 2.
- **`expenses_tool/cli.py` (extended).** `cmd_import_csv` and its subparser, with the four mapping
  options `required=True`, and every message the criteria quote. The order of the checks is the
  plan's, exactly: data file → people → bytes → decoding → header → duplicate → rows.
- **`tests/test_bankcsv.py` (new, 23 tests)** and **`tests/test_cli_import.py` (new, 28 tests)**,
  plus 7 tests added to `tests/test_store.py`. The suite went from 87 tests to 145, all passing.

Expenses are created by `expenses.record_expense` — the same function `add-expense` calls — and
written by the single existing `store.save`. That is why AC3 holds by construction and why the
import performs no write of its own (AC9).

## Acceptance criteria evidence

Every test named below was also checked to *fail* when the behaviour it covers is removed; two
mutations were run explicitly and are recorded under Gates.

| AC | how it is satisfied | evidence |
|----|--------------------|----------|
| AC1 | `bankcsv.read` locates the three named columns in the header (trimmed, exact) and ignores every other column; `cmd_import_csv` prints `Imported ` + `render_expense` per accepted row, in file order | `tests/test_cli_import.py::AC1ReadsThroughTheNamedColumns` — `test_one_expense_per_accepted_row_in_file_order` asserts stdout is exactly `Imported 2026-08-14 30.00 Dinner at Luigi — paid by Ana, shared by Ana, Ben, Cass` then the `Taxi home` line, stderr `""`, exit 0; `test_a_column_nobody_named_is_ignored`; `test_the_tool_knows_nothing_about_any_bank` reads the same file with `--description-column Balance` and gets different expenses. Unit: `test_bankcsv.py::NamedColumns` (6 tests) |
| AC2 | `bankcsv._row` parses each row's own date cell with the stated format and returns it as `YYYY-MM-DD`; nothing consults the clock | `tests/test_cli_import.py::AC2EachExpenseKeepsItsOwnRowsDate::test_dates_come_from_the_rows_and_the_listing_is_in_date_order` — asserts `list-expenses` is exactly the two lines in date order with the dates written literally in the assertion, so the machine's clock cannot make it pass |
| AC3 | the import calls `expenses.record_expense` and `cli.render_expense`, the same code `add-expense` uses | `tests/test_cli_import.py::AC3IndistinguishableFromAHandEnteredExpense::test_imported_and_typed_ledgers_render_identically` — builds a second ledger with two `add-expense` runs and asserts the `list-expenses` output and the `report` output of the two ledgers are equal strings |
| AC4 | `bankcsv._row` returns `None` for the four causes; `cmd_import_csv` prints `Skipped line <n>: <raw>` on stderr and still exits 0 | `tests/test_cli_import.py::AC4AnUnusableRowIsSkippedAndReported::test_the_middle_row_is_skipped_and_the_others_are_imported` — stderr exactly `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00`, stdout the two `Imported …` lines, exit 0; `::test_a_date_format_matching_nothing_skips_every_row_and_still_exits_zero`. Unit: `test_bankcsv.py::UnusableRows` (8 tests) covering each cause, including a `--date-format` that is not a valid format at all |
| AC5 | `_locate` raises `ColumnNotFound` for the first missing column in date/amount/description order; `read` raises `NoHeader` for an empty file; a run that records nothing prints `No rows imported from <FILE>` and calls neither `record_import` nor `save` | `tests/test_cli_import.py::AC5AFileTheNamedColumnsDoNotDescribe` — `test_a_missing_column_is_refused_and_names_what_was_expected` (stderr exactly `Column not found in <path>: Value`, stdout `""`, exit 1, no `Traceback`, data file byte-identical), `test_an_empty_file_is_refused` (`<path> has no header line`), `test_a_header_with_no_data_rows_imports_nothing_and_is_not_remembered` (exit 0, and a second run does not warn). Unit: `test_bankcsv.py::NamedColumns::test_missing_column_is_reported_in_date_amount_description_order` |
| AC6 | payer and sharers are resolved through `expenses.resolve_person` / `resolve_sharers` **before the file is opened** | `tests/test_cli_import.py::AC6ThePayerAndTheSharersComeFromTheCommandLine` — `test_they_are_applied_to_every_accepted_row`, `test_omitting_shared_by_snapshots_everyone_registered` (registers `Dan` afterwards and asserts the listing is unchanged), `test_an_unknown_person_is_refused_before_any_row_is_read` (three sub-cases; `Unknown person: Dan`, exit 1, stdout `""`, data file unchanged), `test_the_first_unknown_sharer_is_the_one_named` |
| AC7 | `bankcsv.fingerprint` over the raw bytes plus `store.imported_on`; `--again` bypasses the warning; the mapping takes no part in the digest | `tests/test_cli_import.py::AC7ARepeatImportWarnsAndNeedsAgain` — 7 tests: the second import warns with the exact message and imports nothing, `--again` produces four listed expenses, a renamed copy is recognised, a file with one row added is new, a different valid mapping still warns, `--again` on a new file is an ordinary import, and the date named is today's. Unit: `test_store.py::ImportedFiles::test_imported_on_returns_the_last_matching_date` for the most-recent rule, which the CLI cannot show in one day |
| AC8 | `open(..., "rb")` with `OSError` → `Cannot read <path>: <strerror>`; `NotDecodable` → `Cannot read <path>: it is not valid UTF-8` | `tests/test_cli_import.py::AC8AMissingOrUnreadableFile` — `test_a_file_that_does_not_exist_is_refused` (path named, exit 1, no `Traceback`, data file unchanged) and `test_a_file_that_is_not_valid_utf8_is_refused` (exact message) |
| AC9 | nothing is written until every check has passed, and then once through `store.save`; `bankcsv.py` contains no write at all | `tests/test_cli_import.py::AC9RefusalsChangeNothingAndTheWriteIsAtomic::test_every_refusal_leaves_the_data_file_byte_for_byte_unchanged` — six sub-cases (AC5 missing column, AC5 empty file, AC6 unknown person, AC7 repeat, AC8 missing file, AC10 missing option), each comparing the file's bytes before and after; `::test_the_importer_never_writes_the_data_file` reads `bankcsv.py` and asserts it contains none of `open(`, `store.save`, `json.dump`, `os.replace` — the inspection AC9 names |
| AC10 | the four mapping options are `required=True`, so argparse exits 2 | `tests/test_cli_import.py::AC10TheFourMappingOptionsAreRequired::test_omitting_any_one_of_them_is_a_usage_error` — four sub-cases, each exit 2, stdout `""`, stderr non-empty, data file unchanged |
| AC11 | decoding with `utf-8-sig`, parsing with the `csv` default dialect, cells stripped before use | `tests/test_cli_import.py::AC11ReadingConventions` — `test_a_quoted_comma_and_trimmed_cells` asserts stdout is exactly `Imported 2026-08-14 30.00 Dinner, drinks and a taxi — paid by Ana, shared by Ana, Ben, Cass` from a row written `14/08/2026, 30.00 ,"Dinner, drinks and a taxi",1200.00`; `test_a_leading_byte_order_mark_changes_nothing` prefixes the same file with `\xef\xbb\xbf` and asserts the identical line. Unit: `test_bankcsv.py::ReadingConventions` (6 tests) |

## Deviations from the plan

Three, all of the "how, not what" kind, and none changing what is delivered.

1. **`Row` and `Skip` are small classes rather than the tuples the plan's sketch implied.** The plan
   wrote them as `Row = (date, amount_pence, description)`. Named attributes made the parser and
   its tests readable, and `__eq__`/`__repr__` make an assertion failure legible. No behaviour
   differs; a caller reads `row.date` instead of `row[0]`.
2. **`bankcsv.read` also skips a completely blank line inside the file, silently.** The plan and
   AC4 are about rows that cannot become expenses; a blank line is not a row at all, and reporting
   `Skipped line 5: ` for the trailing newline structure of an ordinary file would be noise. Pinned
   by `test_bankcsv.py::test_a_blank_line_inside_the_file_is_neither_imported_nor_reported`.
   Flagged here because it is a behaviour no criterion states.
3. **`NoHeader` covers a whitespace-only file as well as a zero-byte one.** AC5 names the zero-byte
   case; a file of one newline would otherwise have produced `Column not found`, which is a worse
   description of the same problem. Pinned by `test_bankcsv.py::test_an_empty_file_has_no_header`.

The plan's six assumptions were all implemented as written, including the two whose alternatives
were plausible: `--again` on a never-imported file is an ordinary import, and an import that
records nothing is not remembered.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 145 tests … OK`, on the branch head after the last commit |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses expenses_tool tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 |
| `every-criterion-has-a-test` | **pass** | the table above: AC1 to AC11, each mapped to named tests. Two mutations were run to confirm the tests are not vacuous — changing `utf-8-sig` to `utf-8` failed 2 tests, and suppressing the write (`if recorded and False:`) failed 8; the suite is green again with both reverted |
| `commits-reference-the-item` | **pass** | `git log --oneline main..HEAD` → three commits, each ending `(refs WI-0004)` |

## What I did not do

- **I did not touch `tests/test_cli_people.py`, `tests/test_cli_expenses.py` or
  `tests/test_cli_report.py`**, and none of them needed touching — which is the evidence that AC3's
  "indistinguishable" holds at the code level and not only in the comparison test.
- **The one existing assertion the plan permitted changing was changed**: the empty-store shape in
  `tests/test_store.py`, now `{"schema": 1, "people": [], "expenses": [], "imports": []}`. Nothing
  else in that file was altered; 7 tests were added to it.
- **I did not fix the pre-existing traceback on a failing `store.save`**, which the plan's risks
  name: an unwritable directory still raises out of `main()` for `import-csv` exactly as it does
  for `add-person`. It is not this item's, and widening the change to cover it would have shipped
  a fix with no criterion and no verification.
- **I did not add anything for the stakeholder's bank.** No default column names, no config file,
  no remembered mapping. When their sample arrives it is a new item, per the item's out-of-scope
  list.
- **`money.parse_amount` refuses a quoted thousands separator (`"1,200.00"`)**, so such a row is
  skipped and reported. That is AC4 as written and the plan's risks called it out in advance; it is
  pinned by a test so that it is visibly a known consequence rather than an accident. If the
  stakeholder's real export writes amounts that way, that is a new criterion, not a defect in this
  one.

---

## Second pass — the review's send-back (D7)

`review-close` rejected the first pass on **D7**, not on the code: `README.md` was never touched,
so the tool's front door said under `## What it does not do yet` that *"Importing a bank CSV export
is the next piece of work"*, and its command table listed five commands where six exist. The review
named six defects with line numbers, F1 to F6, and said explicitly that no code change was required.

**No code changed.** `git diff --stat` for this pass is one file: `README.md`, +79 −11. The eleven
criteria, the tests, the modules and the branch's earlier commits are untouched, so everything in
the evidence table above still stands as written.

What was fixed, against the review's own labels:

- **F1 — line 158.** The sentence claiming the CSV import was still to come is gone. The paragraph
  it lived in kept its true half (no removing or renaming a person, no editing or deleting an
  expense) and gained the two things that genuinely are *not* done: there is no shortcut for any
  particular bank, and nothing about a file's shape is remembered between runs.
- **F2 — the `### Commands` table.** A row for `import-csv` with its full option list, matching the
  style of the five already there — and a new `### Importing from your bank` section placed after
  `### Who owes whom`, which is where the epic's own delivery order puts it. It explains why the
  four options exist (the tool holds no bank's format, which is the stakeholder's choice in Q-006)
  so that a reader does not read them as an oversight, and it documents the three behaviours a user
  will actually meet: skipped rows with their line numbers and exit 0, an outright refusal when the
  named columns are not in the file, and the duplicate-file warning with `--again`.
- **F3 — line 108.** *"the import command **will take** its people as a comma-separated list"* →
  *"takes"*.
- **F4 — line 65.** *"Nothing here works out who owes whom yet — that is the next piece of work"*,
  which was false since WI-0003 and was contradicted two lines later by the `### Who owes whom`
  heading, is now *"Working out who owes whom is the next section."*
- **F5 — line 4.** *"— once the report lands —"* removed from the opening sentence, which now also
  says expenses can be typed in or imported.
- **F6 — line 36.** *"Both accept `--data-file PATH`"* → *"Every command accepts …"*. The review
  noted that adding a sixth row would have made an already-wrong sentence wronger.

One thing the review did not ask for and this pass did anyway: the **output and exit codes** table
gained a row for an import that skipped rows (skips on stderr, the rest on stdout, exit 0) and
names a file already imported among the refusals. Without it the table said only "It worked → exit
0" and "Refused → exit 1", which does not describe an import that partly worked — the one exit-code
case in this item that is not obvious. Declared here rather than slipped in.

**Every console block in the new section was executed and reproduces verbatim**, rather than being
written from memory:

- the full import command → the two `Imported …` lines exactly as printed in the README;
- the skip example → `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00` followed by the one
  `Imported …` line;
- the duplicate example → `This file was already imported on 2026-08-22. Pass --again to import it
  anyway`, exit 1.

Gates on this pass, run after the commit: `python3 -m unittest discover -s tests -t . -q` → exit 0,
`Ran 145 tests … OK`; `python3 -m compileall -q expenses expenses_tool tests` → exit 0;
`grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` → no matches
outside the `## What it does not do yet` heading itself.

**Still not done, and still declared:** everything in `## What I did not do` above is unchanged —
the pre-existing traceback on a failing `store.save`, the absence of anything bank-specific, and
`money.parse_amount`'s refusal of a quoted thousands separator.
