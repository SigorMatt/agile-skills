# Implementation report — WI-0001

Branch `wi/WI-0001`, branched from `main` at `5e92294`. Every hard gate was run on the branch
head, after the last change. The last commit that changes code or a document is `bac3c67`;
everything after it touches only `tracker/`, and the closing transition re-runs every gate
against the head as it finally stands.

## What was built

`recall`, a command-line program with two subcommands, and the storage underneath them. Nothing
that reads a due date and nothing that runs a review sitting: `add` writes `rung` and `due` and
nothing in this item reads them back.

Four source files and a launcher, in the three-layer split `docs/architecture/overview.md`
specifies, each layer keeping the rule about what it may not do:

- `recall/deck.py` — `Card` (question, answer, rung, due), `Deck` (ordered, `add`, `cards`,
  `__len__`) and `new_card(question, answer, today)`, which puts a new card at rung 0 and due
  today per `ADR-0002` §3. No file access, no printing.
- `recall/store.py` — `deck_path()`, `load(path)`, `save(deck, path)` and `DeckUnreadable`. No
  printing, no policy: it returns a deck or it raises. `save` serialises to a temporary file in
  the destination directory and `os.replace`s it over the deck, so an interrupted write leaves
  the previous deck whole. `load` returns an empty `Deck` when the file or its parent is absent
  and raises `DeckUnreadable` when the file is present but is not a deck — never both collapsed
  into one branch.
- `recall/cli.py` — `build_parser`, `main(argv) -> int`, `cmd_add(args) -> int`,
  `cmd_list(args) -> int`. The only layer that prints, and the only place `DeckUnreadable` is
  caught. `main` returns the exit code rather than calling `sys.exit`.
- `bin/recall` (executable, `#!/usr/bin/env python3`) and `recall/__main__.py` — launchers with
  no logic, both calling `recall.cli.main` and passing its return to `sys.exit`.
- `docs/process/using-recall.md` — the document AC7(a) requires, stating the deck file's path,
  the one `PATH` setup step, and what the tool does with a damaged deck.

Two decisions the plan singled out as the ones that get quietly weakened, and how each landed:

- **Blank validation precedes any file access.** `cmd_add` builds its `missing` list and returns
  before `store.deck_path()` is ever called, so AC2's "the deck is exactly as it was" is true by
  construction rather than because nothing happened to go wrong.
- **`DeckUnreadable` is caught in exactly one place**, at the top of each `cmd_*`, and turned
  into a message and a non-zero exit. `store.py` catches it nowhere and never converts it into
  an empty deck.

## Acceptance criteria evidence

Every row names a test function. `python3 -m unittest discover -s tests -t . -q` runs all 16 and
exits 0. The nine acceptance tests invoke `bin/recall` as a child process with `HOME` pointed at
a temporary directory, so what the test observes and what the criterion says are the same
observation rather than two things that resemble each other.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_add` appends one card and saves; `cmd_list` prints one line per card | `tests/test_add.py::AddTests::test_add_exits_zero_and_adds_one` — `list`, then `add --question "capital of France" --answer "Paris"` asserting exit 0, then `list` again asserting exactly one more card line and both sides present |
| AC2 | the `missing` check in `cmd_add`, run before the deck path is resolved | `tests/test_add.py::AddTests::test_blank_sides_refused` — six sub-tests (`--question` omitted, `--answer` omitted, `--question ""`, `--answer ""`, `--answer "   "`, `--question " \t "`); each asserts non-zero exit, the missing option's name in stderr, byte-identical `list` output before and after, and an unchanged `sha256` of the deck file |
| AC3 | `cmd_list` prints `f"{card.question} \| {card.answer}"` with no normalisation anywhere on the path | `tests/test_list.py::ListTests::test_lists_both_cards_verbatim` — adds `"Der  Bahnhof"` / `"The  Station"` (leading capital, internal double space) and `"die Katze"` / `"the cat"`, asserts two card lines and each of the four strings present exactly as given |
| AC4 | `save` on every `add` and `load` on every `list`; no save step exists to forget | `tests/test_storage.py::StorageAcceptanceTests::test_survives_process_exit` — one `add` child process, which has exited by the time a separate `list` child process runs with the same `HOME`, asserting the card is in the second's stdout |
| AC5 | `save` calls `path.parent.mkdir(parents=True, exist_ok=True)`; `load` returns an empty deck for an absent file | `tests/test_storage.py::StorageAcceptanceTests::test_first_run_creates_storage` — asserts the file and its parent are both absent, runs `add`, asserts exit 0 and the file now exists |
| AC6 | `cmd_list` prints `EMPTY_DECK_MESSAGE` and returns 0 when the deck holds nothing | `tests/test_list.py::ListTests::test_empty_deck_message` — asserts exit 0, the marker `deck is empty` in stdout, and zero card lines |
| AC7(a) | `docs/process/using-recall.md` §"Where the deck is kept" | `tests/test_storage.py::StorageAcceptanceTests::test_docs_state_the_path` — asserts the file exists and contains the literal `.local/share/recall/deck.json` |
| AC7(b) | the atomic write renames the temporary file onto the deck, so nothing is left beside it | `tests/test_storage.py::StorageAcceptanceTests::test_one_file_under_home_not_tmp` — snapshots every file under `HOME` before and after one `add`, asserts the difference is exactly `{.local/share/recall/deck.json}`, and that the file contains the card |
| AC7(c) | `deck_path()` is `Path.home() / ".local" / "share" / "recall" / "deck.json"` and reads nothing else | `tests/test_storage.py::StorageAcceptanceTests::test_deck_path_is_under_home_and_not_boot_cleared` — asserts the resolved path is under the resolved ambient home and under none of `/tmp`, `/var/tmp`, `$TMPDIR` |
| AC8 | `load` raises rather than returning empty, and `_report_unreadable` prints the path and returns 3 without writing | `tests/test_storage.py::StorageAcceptanceTests::test_unreadable_deck_refused` — writes `{"cards": ` into the deck file, records its `sha256`, runs `add` and `list` as sub-tests, asserts both exit non-zero, both name the path on stderr, and the `sha256` is unchanged |
| AC9 | `Deck.add` appends unconditionally; nothing compares questions | `tests/test_add.py::AddTests::test_duplicate_question_allowed` — adds `"der See"` twice with different answers, asserts both exit 0 and `list` shows two card lines with both answers |

Five further unit tests in `tests/test_storage.py::StoreUnitTests` exercise `store` with the path
passed explicitly and `HOME` never consulted: absent-loads-empty, save/load round-tripping every
field including `rung`, `due` and `version`, malformed JSON raising rather than returning empty,
JSON without a `cards` array raising, and `load` leaving the file and its directory untouched on
the failure path.

**These tests were checked against removal of the behaviour, not merely run.** Four mutations
were applied to the working tree in turn, the suite run, and the tree restored:

| mutation | tests that failed |
|---|---|
| `load` returns an empty deck for malformed JSON instead of raising | `test_unreadable_deck_refused` (both sub-tests), `test_load_never_writes`, `test_malformed_json_raises_rather_than_returning_empty` |
| `cmd_add` accepts a whitespace-only side | `test_blank_sides_refused`, all four blank sub-cases |
| `cmd_list` lowercases and collapses whitespace | `test_lists_both_cards_verbatim` (2 sub-tests), `test_add_exits_zero_and_adds_one` |
| `Deck.add` deduplicates by question | `test_duplicate_question_allowed` |

The first mutation is the one the plan named as the single most likely defect in this item — the
easy way to satisfy AC5 that silently destroys a deck. It is caught by four tests.

## Deviations from the plan

Three, all inside the plan's latitude — the *how*, not the *what*. None changes what is
delivered and none needed a question.

1. **AC2 gets a sixth case, not five.** The mapping table names five; AC2's own text names tabs
   explicitly and none of the five demonstrates a tab. Added `--question " \t "`. Strictly more
   evidence for the same criterion.
2. **AC7 is three tests rather than the two the mapping table names.** The table's
   `test_one_file_under_home_not_tmp` was to assert both "exactly one new file" and "not under
   `/tmp`". It cannot do both honestly: the temporary `HOME` the acceptance tests use is itself
   inside `/tmp`, so asserting "not under `/tmp`" against it would test the harness rather than
   the tool. AC7(b) stayed in that test; AC7(c) became
   `test_deck_path_is_under_home_and_not_boot_cleared`, which computes `deck_path()` against the
   *ambient* home — the path a real user actually gets. This is the risk `plan.md` recorded under
   "AC7's `$TMPDIR` check is only as good as the environment it runs in", resolved the way that
   note pointed.
3. **`store.py` has one helper the plan did not name**, `_card_from(entry, position, path)`,
   which validates a stored card's four keys and their types. The plan specified `load`'s
   contract ("entries have the four expected keys") without saying where the check lives. The
   path is threaded into it rather than added by the caller, because AC8 requires the message to
   name the file and a message naming the file *and* the card is what a person repairing a deck
   by hand needs.

Two smaller choices the plan left to taste, recorded because a reader would otherwise have to
infer them: `list`'s line format is `<question> \| <answer>`, and the non-zero exit codes are 2
for a refused argument and 3 for an unreadable deck. Every criterion asks only for "non-zero";
the split exists so a caller can tell the two apart.

## Gates

Run on the branch head, after the last change, and re-run by `scripts/transition` as part of
the closing move — that second run is the authoritative one and its output is in the journal.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 16 tests ... OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0, `checked 5 item(s), 8 document(s)`, 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC9, and the mutation table shows each would fail if the behaviour were removed |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 5 commit(s) on main..wi/WI-0001 name WI-0001` |
| `no-unplanned-scope` (advisory) | **pass** | 14 files differ from `main`. `recall/deck.py` → step 2; `recall/store.py` → step 3; `recall/cli.py` → step 4; `bin/recall`, `recall/__main__.py` → step 5; `tests/support.py`, `tests/test_add.py` → steps 1 and 6; `tests/test_list.py`, `tests/test_storage.py` → step 6; `docs/process/using-recall.md` → step 7; `tracker/items/WI-0001/{item,history,journal}.md` and `tracker/board.md` → the transition record. No hunk is untraceable |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0, `checked 3 consumed human answer(s)`, 0 errors |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0, 0 errors |

## What I did not do

- **Nothing in the plan was left undone.** All eight steps were executed in order.
- **The acceptance criteria checkboxes in `item.md` are still unticked.** Ticking them is
  `verify`'s judgement, not this skill's claim.
- **No interactive prompt for `recall add` when the options are absent.** `ADR-0001` §3 left it
  to `plan`, and `plan.md` did not adopt it — so it is not built. `add` with a side omitted is a
  refusal naming the side, which is what AC2 requires.
- **No `review` subcommand and no `delete`.** `ADR-0001` names both; they are WI-0002/WI-0003 and
  WI-0004.
- **Nothing reads `rung` or `due` back.** They are written from the first card so WI-0002 and
  WI-0003 do not have to reopen this item, and no code in WI-0001 consumes them.
- **`bin/recall` is not covered by `commands.lint`.** The declared command is
  `python3 -m compileall -q recall tests`, and `bin/recall` has no `.py` extension so it is in
  neither directory. It is exercised by all nine acceptance tests, which invoke it as the child
  process, so it is not untested — but the syntax gate does not see it. Recorded because it is
  not obvious from reading the gate result.
- **`commands.lint` remains a syntax check only.** `ADR-0003` says so; a green lint gate on this
  project means less than it does on most, and nothing here changes that.
