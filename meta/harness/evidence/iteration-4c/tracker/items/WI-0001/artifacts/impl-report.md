# Implementation report — WI-0001

Branch `wi/WI-0001`, two commits, `d2c2432` and `5c680a8`, both on top of `main` at `5c667e0`.

## What was built

`python3 -m recall add <front> <back>`, and the card file underneath it.

- **`recall/store.py`** — the card file. `card_file_path()` resolves `RECALL_CARD_FILE`, then
  `$XDG_DATA_HOME/recall/cards.txt`, then `~/.local/share/recall/cards.txt` (ADR-0008).
  `Card` is a `NamedTuple` of `front`, `back`, `rung` and `due`. `load()` returns the cards in
  file order and an empty list when there is no file; it raises `CardFileError` naming a line
  number when the file is not in the format ADR-0007 fixed. `save()` creates the directory,
  writes the header and one block per card to a temporary file in the same directory, flushes it
  with `os.fsync`, renames it over the card file with `os.replace`, and flushes the directory.
- **`recall/cli.py`** — the conversation with the person. `_side_error()` is the input rule;
  `add()` runs it over the front and then the back, refusing before it reads or writes anything,
  then loads, warns on a front it has seen, appends the new card at `rung 0` due today, saves,
  and confirms. `main()` parses with `argparse` and turns `CardFileError` and `OSError` into a
  message and exit `1` rather than a traceback.
- **`recall/__main__.py`** — three lines, so that `python3 -m recall` is the entry point.
- **`tests/test_add.py`** — 17 tests that run the tool as a subprocess against a card file in a
  temporary directory and assert on exit codes, both streams, and the bytes on disk.
- **`tests/test_store.py`** — 9 tests for the plan's steps 1 to 3: path resolution, the
  round trip, the documented shape, and the two malformed-file cases.

A worked example of the file this writes, after `add bonjour hello` and `add chat cat`:

```
# recall cards - written by `python3 -m recall`; the tool rewrites this file
# one card per block: front, back, rung, due

front: bonjour
back: hello
rung: 0
due: 2026-08-30

front: chat
back: cat
rung: 0
due: 2026-08-30
```

## Acceptance criteria evidence

Every test below is in `tests/test_add.py` unless it names another file. Run them with
`python3 -m unittest discover -s tests -t . -q` → exit 0, 26 tests.

| AC | how it is satisfied | evidence |
|----|--------------------|----------|
| AC1 — two arguments add one card, confirm naming the front, exit zero | `add()` prints `Added: <front>` on standard output and returns `0`; `argparse` fixes the two positional arguments, front first | `test_add_prints_confirmation_and_exits_zero` — exit 0, `bonjour` in standard output, exactly one `front: ` in the file. Removing the append made 2 tests fail |
| AC2 — the card is in the file after the process exited, both sides byte-identical | `save()` writes each side verbatim after `front: ` / `back: `, then fsyncs and renames | `test_card_is_on_disk_after_the_process_exits` — the subprocess exits, then the test reads the file's **bytes** and finds `front: l'été "chaud"` and `back: the "hot" summer` exactly, quotes and accents included. See `## What I did not do` for the half of AC2 no test can perform |
| AC3 — three different fronts are three separate records | `add()` appends to the list `load()` returned, and `save()` writes every card | `test_three_cards_are_three_records` — three `front: `, three `rung: `, three `due: ` lines, and each front sits directly above its own back. Replacing the append with an assignment failed this test |
| AC4 — a new card's due date is the day it was added | `add()` writes `datetime.date.today()`, and `save()` renders it `YYYY-MM-DD` | `test_new_card_is_due_today_at_the_bottom_rung` — the file contains `due: <today>` computed independently in the test, and `rung: 0` |
| AC5 — the data is at a documented path and is readable text | `card_file_path()`; the format of ADR-0007, which `docs/architecture/overview.md` states | `test_default_path_is_the_documented_one` (writes `$XDG_DATA_HOME/recall/cards.txt`), `test_default_path_without_a_data_directory_is_under_home` (writes `$HOME/.local/share/recall/cards.txt`), `test_the_file_is_readable_text_in_the_documented_shape` (every non-comment line is one of the four labels and its value), and `tests/test_store.py::test_the_file_is_the_documented_shape` |
| AC6 — a duplicate front adds a second card, warns, exits 0 | `add()` compares the new front with each existing `card.front` and prints the warning to standard error before carrying on | `test_duplicate_front_adds_a_second_card_and_warns` — exit 0, `already exists` on standard error, two `front: bonjour` records with the two different backs. Removing the comparison failed this test |
| AC7 — an empty or whitespace-only side adds nothing, names the side, exits non-zero, leaves the file untouched | `_side_error()` runs over the front and then the back, before `load()` and `save()` are reached | `test_an_empty_or_whitespace_side_is_refused_and_nothing_is_written` (four cases: empty front, empty back, spaces, tab-and-space — each exits non-zero, names the side, and leaves no file), `test_a_refusal_leaves_an_existing_file_byte_identical` (the file's bytes are unchanged), and `test_an_empty_back_with_a_duplicate_front_prints_no_duplicate_warning`, which is AC7's stated precedence over AC6. Removing the emptiness check failed 6 tests |
| AC8 — `add` when the card file does not exist creates it and writes the card | `save()` calls `os.makedirs(..., exist_ok=True)` on the containing directory | `test_the_first_add_creates_the_file_and_its_directory` — `RECALL_CARD_FILE` points three directories deep into nothing; exit 0, the confirmation names the front, and the file afterwards holds AC1's and AC2's assertions |

Three further tests cover behaviour the plan decided but no criterion states:
`test_a_side_with_a_line_break_is_refused` (ADR-0007), `test_the_wrong_number_of_arguments_is_a_usage_error`
and `test_no_subcommand_is_a_usage_error` (exit 2, the case the item left deliberately
unconstrained), and `test_an_unreadable_card_file_stops_the_command` (the plan's assumption 4).

## Deviations from the plan

- **`add()` prints a second line, `Nothing was added.`, when it refuses a side.** The plan
  required the message to name the side; this adds one sentence saying the file was not touched,
  because the refusal message alone does not say whether the card got in. Within assumption 2's
  latitude over wording.
- **`main()`'s error message prefixes the card file's path** to what `CardFileError` or `OSError`
  says, so a person who has `RECALL_CARD_FILE` set to the wrong thing can see it. Same latitude.
- **The plan's `_side_error(label, value)` signature is exactly as written**; nothing in either
  module's interface changed from `plan.md`'s `## Approach`.
- **`tests/test_store.py` was not named in the plan**, which said `tests/test_add.py`. The plan's
  steps 1 to 3 each state an observable result about the store, and those results are what this
  file checks; step 6's file covers the criteria through the command line. No criterion depends
  on it.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests`, OK |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 4 items and 10 documents, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function per criterion; AC2's row states what its test does and does not demonstrate |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 2 commits on `main..wi/WI-0001` name WI-0001 |
| `no-unplanned-scope` | **pass (advisory)** | `git diff main --stat`: three modules and two test files, plus this item's own tracker files. Every hunk traces to a plan step; nothing under `docs/` changed |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0, 9 consumed human answers checked, 0 documents in the window |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |

Three mutations were run against the branch to check the tests bite, and each was reverted:
removing the emptiness check failed 6 tests, removing the duplicate comparison failed 1, and
replacing the append with an assignment failed 2.

## What I did not do

- **AC2 says the machine has been restarted, and no test restarts a machine.** What is
  demonstrated is that the card file holds the right bytes after the writing process has exited,
  and that `save()` fsyncs the file and its directory before returning (ADR-0008). Whether that
  satisfies the criterion is `verify`'s call, and `plan.md`'s `## Risks` flagged it before any
  code was written. Nothing was changed about the criterion.
- **No acceptance criterion was ticked.** The checkboxes in `item.md` are `verify`'s.
- **Nothing outside this item was touched.** No document under `docs/` was edited, no other
  item's files, and no defect elsewhere was fixed — none was found.
- **The `review` and `delete` subcommands do not exist.** They are WI-0002 and WI-0003;
  `argparse` refuses them with a usage message and exit 2.
