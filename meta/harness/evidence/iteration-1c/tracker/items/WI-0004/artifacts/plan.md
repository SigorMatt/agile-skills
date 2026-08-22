# Plan — WI-0004 Import expenses from a bank CSV export

## Problem

The person keeping the group's books already has every transaction in their bank's CSV export and
does not want to retype it. This item adds one subcommand, `./expenses import-csv <FILE>`, that
turns rows of that file into ordinary expenses — indistinguishable from ones typed by hand, so the
report and the listing need no change at all.

The constraint that shapes everything: **the tool knows nothing about any bank.** The stakeholder
chose in WI-0004/Q-006 to state the file's shape at each import — which column holds the date, the
amount and the description, and the date format — rather than wait to send a sample. So there is no
default column name and no per-bank table anywhere; the parser is a function of (bytes, mapping),
and every acceptance criterion is checked against example files the tests write themselves. The
other constraints are inherited and not in play here: money is whole pence (ADR-0001), a refusal
prints on stderr, exits 1 and stores nothing (ADR-0005), the data file is written atomically in one
go (ADR-0006), nothing outside `cli.py` prints (ADR-0008), and an expense snapshots its sharers by
stored name (ADR-0009).

## Approach

Three layers, following the shape the project already has:

- **`expenses_tool/bankcsv.py`** (new) — everything about reading a CSV, and nothing else. Given
  the file's raw bytes and a column mapping it returns the rows it accepted and the rows it
  skipped, or raises. It never prints, never exits, never touches the data file, and holds no
  knowledge of any bank. It is a pure function of its arguments, so every parsing criterion is a
  unit test with a literal file in it.
- **`expenses_tool/store.py`** (extended) — the memory of which files have been imported, per
  ADR-0011: a new top-level `imports` key, validated as strictly as everything else.
- **`expenses_tool/cli.py`** (extended) — the subcommand, the order the checks run in, every
  message the criteria quote, and the exit codes.

Expenses are created through `expenses.record_expense`, the same function `add-expense` calls, and
written by the single `store.save` at the end. That is what makes AC3 true by construction rather
than by care: an imported expense is built by the same code as a typed one, so there is no second
place for the two to drift apart. It is also what makes AC9's atomicity free — the import performs
no write of its own.

## Steps

1. **`expenses_tool/store.py` — remember imports (ADR-0011).**
   - `empty_data()` returns `{"schema": 1, "people": [], "expenses": [], "imports": []}`. This
     follows the precedent WI-0002 set when it added `expenses`; `SCHEMA_VERSION` stays 1, because
     ADR-0006 clause 2 makes an absent key read as empty.
   - `load()` validates `imports` when the key is present — a list of objects, each with a string
     `sha256` and a string `date` — raising `DataFileError` with a reason in the same voice as the
     existing ones (`"one of its imports has no sha256"`). It does **not** insert the key when
     absent, so a file written by an earlier version still loads and `store.load` on a missing file
     is unchanged in shape apart from the new key from `empty_data()`.
   - Add `imported_on(data, digest)` → the `date` of the **last** record whose `sha256` matches, or
     `None`; and `record_import(data, digest, date)` → appends `{"sha256": digest, "date": date}`,
     via `setdefault("imports", [])`.
   - `tests/test_store.py` has one assertion that spells out the empty store
     (`{"schema": 1, "people": [], "expenses": []}`); update it to include `"imports": []`. This is
     the only existing test this item changes, and it is changed because the shape it asserts
     genuinely changed — not to make anything pass.
   - *Afterwards:* the data file can carry an import history, and a file with a malformed one is
     refused rather than read.

2. **`expenses_tool/bankcsv.py` — read a CSV through a stated mapping.** New module. Its whole
   surface:

   ```
   class BankCsvError(Exception)          # base
   class NotDecodable(BankCsvError)       # the bytes are not UTF-8
   class NoHeader(BankCsvError)           # the file is empty
   class ColumnNotFound(BankCsvError)     # .column — a named column is not in the header

   Row  = (date, amount_pence, description)      # date is YYYY-MM-DD, amount is whole pence
   Skip = (line, text)                           # line is 1-based in the file; text is raw

   def fingerprint(raw: bytes) -> str
   def read(raw: bytes, *, date_column, amount_column, description_column, date_format)
           -> (rows: list[Row], skips: list[Skip])
   ```

   - `fingerprint` is `hashlib.sha256(raw).hexdigest()`, over the bytes exactly as on disk
     (ADR-0011 clause 1).
   - `read` decodes with the **`utf-8-sig`** codec — one choice that delivers both of AC11's
     remaining conventions: a leading byte-order mark is consumed, and bytes that are not UTF-8
     raise `NotDecodable`. Parsing is `csv` with its default dialect, which is RFC 4180, so a
     quoted field containing a comma arrives whole.
   - Empty input raises `NoHeader`. Otherwise the header cells are stripped and each of the three
     named columns is located in it, **checked in the order date, amount, description**, raising
     `ColumnNotFound` for the first that is missing (AC5). Columns nobody named are ignored.
   - Each data record becomes a `Row` when all four of these hold, and a `Skip` otherwise (AC4):
     it has at least as many cells as the header; its amount cell parses with
     `money.parse_amount` (which is WI-0002 AC5's rule, and rejects blank, zero, negative and
     non-numeric without any new code); its date cell parses with
     `datetime.datetime.strptime(cell, date_format)`, whose `ValueError` also covers a
     `date_format` that is not a valid format string at all; and its description cell is non-blank.
     Cells are stripped before use.
   - A `Skip` carries the record's **first** line number and its raw source text; `csv`'s
     `line_num` gives both even when a quoted field spans lines.
   - *Afterwards:* every parsing criterion (AC1's column matching, AC4's four skip cases, AC5's
     three refusals, AC11's three conventions) is decidable by a unit test with no filesystem and
     no CLI.

3. **`expenses_tool/cli.py` — the `import-csv` subcommand.** Add `cmd_import_csv(args)` and its
   parser. The parser takes the file as a positional argument and
   `--paid-by` (required), `--shared-by`, `--date-column`, `--amount-column`,
   `--description-column`, `--date-format` (all four required, which is exactly AC10 — argparse
   exits 2 for a missing required option), `--again` (a flag), and `--data-file` from the existing
   `common` parent. **The order of the checks is the design**, because several criteria are about
   what happens when two things are wrong at once:

   1. `store.load` — a data file that is not ours refuses with the existing `Cannot read …`.
   2. Resolve `--paid-by` and `--shared-by` through `expenses.resolve_person` and
      `expenses.resolve_sharers`, refusing with the existing `Unknown person: <name>` — **before
      the file is opened**, which is AC6's "the check happens before any row is read", and gives
      AC6's first-offender order for free, since `resolve_sharers` walks the list left to right.
   3. Read the file's bytes; `OSError` refuses with `Cannot read <path>: <strerror>` (AC8), reusing
      the `_cannot_read` shape WI-0001 established.
   4. `bankcsv.read`; `NotDecodable` refuses with `Cannot read <path>: it is not valid UTF-8`
      (AC8), `NoHeader` with `<path> has no header line` and `ColumnNotFound` with
      `Column not found in <path>: <column>` (AC5).
   5. `bankcsv.fingerprint`, then `store.imported_on`. If it returns a date and `--again` was not
      given, refuse with
      `This file was already imported on <date>. Pass --again to import it anyway` (AC7).
   6. Record every accepted row with `expenses.record_expense`, using the resolved payer and
      sharers and the row's own date (AC2), then — only if at least one expense was recorded —
      `store.record_import(data, digest, expenses.today())`, then **one** `store.save` (AC9).
   7. Print: every `Skipped line <n>: <text>` on stderr in file order, then either every
      `Imported <rendered>` on stdout in file order, or, when nothing was recorded,
      `No rows imported from <path>` on stdout. Exit 0. `render_expense` is the existing function,
      so an imported line and an `Added` line cannot differ (AC1, AC3, AC4, AC5).

   `<path>` in every message is the path as typed on the command line, not an absolute or expanded
   form.
   - *Afterwards:* the command exists and every message an acceptance criterion quotes is in
     `cli.py`, where ADR-0008 clause 3 requires it.

4. **`tests/test_bankcsv.py` (new) — the parser's unit tests.** One case per behaviour in step 2,
   each with a literal CSV in the test: the two-row example, a `Balance` column ignored, a quoted
   description containing a comma, a BOM-prefixed file, untrimmed cells, each of the four skip
   causes, a `--date-format` matching nothing, an empty file, a missing column in each of the three
   positions, non-UTF-8 bytes, and `fingerprint` being equal for equal bytes and different for a
   one-row change.

5. **`tests/test_cli_import.py` (new) — WI-0004's acceptance criteria through `./expenses`.** One
   test per AC, named for it, calling `cli.main([...])` with a temporary `--data-file` in the style
   of `tests/test_cli_expenses.py`. AC3 builds the second ledger by hand and compares the captured
   `list-expenses` and `report` output of the two. AC9 copies the data file before each refusal and
   compares bytes after, and asserts by inspection that `bankcsv.py` contains no write to the data
   file.

6. **Run the project's gates**: `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q expenses expenses_tool tests`, both green on the final state.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — reads through the named columns, one expense per accepted row, exact stdout | 2, 3 | `test_cli_import.py::test_ac1_imports_each_row_through_the_named_columns` — imports the two-row `$F` with `$M`, asserts stdout is exactly the two `Imported …` lines in file order, stderr empty, exit 0; `test_bankcsv.py::test_named_columns_are_located_and_others_ignored` for the `Balance` column |
| AC2 — each expense carries its own row's date | 2, 3 | `test_cli_import.py::test_ac2_each_expense_keeps_its_own_rows_date` — after the import, `list-expenses` is exactly the two lines in date order, with the dates frozen in the assertion so the machine's clock cannot make it pass |
| AC3 — indistinguishable from a hand-entered expense | 3 | `test_cli_import.py::test_ac3_imported_and_typed_ledgers_render_identically` — builds `$U` with two `add-expense` runs and asserts the captured `list-expenses` and `report` output of the two ledgers are equal strings |
| AC4 — an unusable row is reported by line and skipped, exit 0 | 2, 3 | `test_cli_import.py::test_ac4_middle_row_is_skipped_and_reported` — the three-row `$G`, stdout the two `Imported …` lines, stderr exactly `Skipped line 3: …`, exit 0; `test_bankcsv.py::test_each_cause_of_an_unusable_row` (bad amount incl. blank/zero/negative/non-numeric, unparseable date, blank description, short row) and `::test_a_date_format_matching_nothing_skips_every_row` |
| AC5 — a file the named columns do not describe is refused; empty file; header-only file | 2, 3 | `test_cli_import.py::test_ac5_missing_column_is_refused`, `::test_ac5_empty_file_is_refused`, `::test_ac5_header_only_file_imports_nothing_and_is_not_remembered` — each asserting the exact message, stream, exit code and that `$T` is byte-for-byte unchanged; the last re-runs the same import and asserts no `--again` warning; `test_bankcsv.py::test_missing_column_is_reported_in_date_amount_description_order` |
| AC6 — payer and sharers from the command line; first unknown reported; nothing imported | 3 | `test_cli_import.py::test_ac6_applies_the_payer_and_sharers_to_every_row`, `::test_ac6_omitting_shared_by_snapshots_everyone`, `::test_ac6_unknown_person_is_refused_before_any_row_is_read` — the last using a file that would otherwise import, asserting `Unknown person: Dan`, exit 1, `$T` unchanged |
| AC7 — a repeat import warns and needs `--again`; identity is the contents | 1, 3 | `test_cli_import.py::test_ac7_second_import_of_the_same_file_warns`, `::test_ac7_again_imports_it_anyway`, `::test_ac7_a_renamed_copy_is_recognised`, `::test_ac7_a_changed_file_is_new`, `::test_ac7_a_different_mapping_still_warns`, `::test_ac7_again_on_a_new_file_is_an_ordinary_import`, `::test_ac7_reports_the_most_recent_import_date`; `test_store.py::test_imported_on_returns_the_last_matching_date` |
| AC8 — a missing or unreadable file is refused, no traceback | 3 | `test_cli_import.py::test_ac8_missing_file_is_refused` and `::test_ac8_non_utf8_file_is_refused` — message names the path as typed, exit 1, `$T` unchanged, no exception escapes `main()` |
| AC9 — every refusal leaves the data file byte-identical; one atomic write | 1, 3 | `test_cli_import.py::test_ac9_every_refusal_leaves_the_data_file_unchanged` — a `cmp`-style byte comparison after each of AC5, AC6, AC7 and AC8's refusals and after AC10's usage error; `::test_ac9_the_importer_never_writes_the_data_file` — asserts `bankcsv.py` contains no `open(`/`save(` against the data path, the inspection AC9 names |
| AC10 — the four mapping options are required | 3 | `test_cli_import.py::test_ac10_each_mapping_option_is_required` — four runs, each omitting one, each `SystemExit(2)` with stdout empty and `$T` unchanged |
| AC11 — RFC 4180 quoting, trimmed cells, BOM ignored | 2, 3 | `test_cli_import.py::test_ac11_quoted_comma_trimmed_cells_and_a_bom` — imports `$H` and its BOM-prefixed copy and asserts the same single `Imported …` line for both; `test_bankcsv.py::test_reading_conventions` |

Every step maps to at least one criterion: step 1 to AC7 and AC9, step 2 to AC1, AC4, AC5 and AC11,
step 3 to all eleven, steps 4 and 5 are their demonstrations, step 6 is the project's own gates.
Nothing in the plan exists that no criterion needs.

## Assumptions

Each is `plan`'s, each is reversible, and each exists because the item deliberately left it open or
because two criteria meet in a case neither states.

1. **The order of the checks** is the one in step 3: data file, then people, then the file's bytes,
   then decoding, then the header, then the duplicate check, then the rows. The two orderings the
   criteria do not fix are people-before-file (chosen because AC6 says the person check happens
   before any row is read, and because a mistyped name is the likelier mistake) and
   columns-before-duplicate (chosen because telling someone their file is a duplicate, when the
   command they typed could never have read it, sends them to fix the wrong thing). Reversing
   either is moving lines within `cmd_import_csv`: one file, no interface, no stored data.
2. **A header containing the same column name twice** resolves to the first occurrence. The item
   records this as deliberately unconstrained (R10); this is the cheapest reading and matches
   `list.index`. Reversal is one line in `bankcsv.read`.
3. **A record spanning several lines** — a quoted field containing a newline — is reported by the
   line it *starts* on, and its raw text is its source lines joined by `\n`. AC4 says "line number"
   without contemplating this; both readings are defensible and this one matches what an editor
   shows when you jump to that line. Reversal is one expression.
4. **An import that records no expenses prints `No rows imported from <FILE>` and is not
   remembered.** AC5 states both for the header-only file; this extends the same treatment to a
   file whose every row was skipped, so that the two cases cannot diverge. Reversal is one branch.
5. **Skipped-row messages are printed before the imported lines**, both after the save. The item
   leaves the interleaving unconstrained (R10); printing after the save means nothing is announced
   that was not stored. Reversal is moving two loops.
6. **`empty_data()` gains `imports` and one existing unit-test assertion changes with it.** The
   alternative — never inserting the key — would leave `imports` the only key absent from a fresh
   store and invite `KeyError`s later. This follows WI-0002's own precedent for `expenses`.
   Reversal is one line in each place.

## Decisions and ADRs

- **ADR-0011 — Imported files are remembered by the SHA-256 of their bytes** (new). Written because
  AC7 makes file identity a real decision with real alternatives, and because the choice of what to
  store is one the item explicitly handed to `plan`. Records that the path is deliberately not
  stored, and that the code is reversible while the stored digests are not.
- **From the documents, no ADR needed.** The subcommand name and its option style (ADR-0002 clause
  3, which reserved `import-csv`); a refusal exits 1 and stores nothing while an empty answer exits
  0 (ADR-0005 clauses 2 and 4); one atomic write and a new top-level key with no schema bump
  (ADR-0006 clauses 2 and 5); nothing outside `cli.py` prints or exits (ADR-0008 clause 3); the
  import writes the same record shape as `add-expense` with the sharers snapshotted (ADR-0009
  clause 3, which anticipated this item by name); amounts through `money.parse_amount` (ADR-0001);
  tests with `unittest`, in two layers (ADR-0007).
- **No ADR for the parser's shape.** That the tool holds no bank format and takes the mapping per
  import is the stakeholder's decision, recorded in WI-0004/Q-006 and in
  `docs/architecture/overview.md` v4; restating it as an architect's decision would misattribute
  it.
- **Nothing was asked of the human.** No decision here is irreversible, and none depends on intent
  no document records: the one question that did — whether to type the mapping at every import —
  was Q-006 and is answered.

## Risks

- **`store.save` raising is still an uncaught traceback**, as it is for every existing command: an
  unwritable directory or a full disk would print a Python trace, which AC5 and AC8 forbid for
  *their* cases but nothing forbids for this one. Pre-existing across the whole tool and out of
  scope here; if it matters it is a bug item against WI-0001, not a widening of this plan.
- **The whole file is read into memory** to hash and parse it. A bank statement is kilobytes, and
  the data file is already read and written whole on every command, so this changes nothing about
  the tool's profile. It would be wrong for a file of millions of rows; nothing in the item
  contemplates one.
- **`money.parse_amount` rejects thousands separators**, so a statement writing `1,200.00` has
  every large row skipped and reported. That is correct per AC4 as written — the amount is not a
  number this tool accepts — and it is exactly the kind of thing the stakeholder's real sample
  would reveal. It is called out here so that, if it turns up, it is recognised as a known
  consequence and a new criterion rather than a defect in this one.
- **A statement whose amounts are negative for spending** — some banks write charges as negatives —
  would have every row skipped under AC4's assumption. The item records that assumption as the
  stakeholder's to correct; this is where it would bite.

## Out of scope for this item

- Any per-bank shortcut, default column name or auto-detection. The stakeholder's sample buys a new
  item; nothing here anticipates it beyond ADR-0011 noting that a shortcut cannot change file
  identity.
- Remembering the mapping between imports, in the data file or a config file (AC10, and the item's
  out-of-scope list — the stakeholder chose option C over option D).
- Row-level duplicate detection, refunds and negative expenses, and any change to `report`,
  `list-expenses`, `add-expense` or `add-person`. AC3 requires the downstream commands to need no
  change, so touching them would be evidence the design is wrong.
- Any change to `tests/test_cli_people.py`, `tests/test_cli_expenses.py` or
  `tests/test_cli_report.py`. The single existing assertion this item may change is the empty-store
  shape in `tests/test_store.py` (step 1); if any other existing test needs changing, that is a
  signal to stop and file a question, not to change it.
