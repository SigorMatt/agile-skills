# Implementation report — WI-0001

## What was built

Two files at the repository root and four test modules, exactly as `plan.md` lays them out.

- **`recall.py`** — the module, in the two layers the plan contracted. The store layer is
  `store_path()`, `load(path)`, `save(path, document)` and `add_card(document, question,
  answer)`; the command layer is `cmd_add`, `cmd_list` and `main(argv)`. `main` returns an exit
  code and never calls `sys.exit` [src: ADR-0005].
- **`recall`** — the executable, four lines: shebang, its own directory onto `sys.path`, `main`,
  exit.
- **`README.md`** — what the tool is, both ways to run it, the two commands with examples, the
  store's location and the `RECALL_FILE` override, the exit codes, and the test command
  [src: WI-0001 AC5].
- **`tests/`** — `tests/support.py`, `tests/test_add.py`, `tests/test_list.py`,
  `tests/test_store.py`, `tests/test_docs.py`. 21 tests. Everything about output and exit codes
  drives the executable as a subprocess with `RECALL_FILE` pointing into a per-test temporary
  directory, so no test can touch the checker's own cards.

Behaviour, as delivered: `recall add "<q>" "<a>"` writes a card and prints `Added card <n>.`;
`recall list` prints `<number>\t<question>\t<answer>` per card in ascending number order, or
`No cards yet.`; the store is one JSON document created by the first add, written by rename;
exit 0 for success, 2 for a wrong command line, 1 for a store that cannot be used
[src: ADR-0004; ADR-0005].

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_add` prints `Added card <n>.` and returns 0; `add_card` numbers a card one above the largest present, 1 when there are none | `tests/test_add.py::AddTest::test_add_exits_zero_and_prints_the_card_number`; `::test_card_numbers_start_at_one_and_increment` (asserts the printed 1, 2, 3 and the stored numbers `[1, 2, 3]`) |
| AC2 | `cmd_list` reads the store in a fresh process and prints the sides unchanged | `tests/test_list.py::ListTest::test_a_card_added_in_one_process_is_listed_by_another` — add in one subprocess, list in another, stdout compared to `1\tdie Katze\tthe cat` |
| AC3 | the card number comes from the pile, not from the text, so identical text yields two cards | `tests/test_add.py::AddTest::test_identical_text_twice_gives_two_cards_with_different_numbers` — stored numbers `[1, 2]`, two lines listed |
| AC4 | `cmd_add` rejects an empty side before touching the store, naming that side | `tests/test_add.py::AddTest::test_empty_question_side_is_rejected_by_name` (stderr contains `question` and not `answer`); `::test_empty_answer_side_is_rejected_by_name`; both then assert `recall list` prints `No cards yet.` |
| AC5 | `store_path()` returns `RECALL_FILE` when set and non-empty, else `~/.recall.json`; the file is pretty-printed UTF-8 JSON; `README.md` names both | `tests/test_store.py::StoreTest::test_recall_file_decides_the_path`; `::test_the_default_store_is_dot_recall_json_in_the_home_directory` (runs with `HOME` in a temporary directory and no `RECALL_FILE`); `::test_the_store_is_readable_text_with_non_ascii_left_alone`; `tests/test_docs.py::ReadmeTest::test_the_readme_names_the_default_store_and_the_override` |
| AC6 | everything after the command name is positional, `add` requires exactly two, `list` sorts by card number | `tests/test_add.py::AddTest::test_a_deck_option_is_rejected_and_stores_nothing` (`recall add --deck german "die Katze" "the cat"` exits 2, nothing stored); `tests/test_list.py::ListTest::test_listing_is_in_ascending_card_number_order` (the stored order is deliberately reversed first, so the sort is what produces the order); `::test_list_takes_no_filter_argument` |
| AC7 | the store is written with `ensure_ascii=False` and read as UTF-8; nothing transforms card text | `tests/test_add.py::AddTest::test_non_ascii_text_survives_a_round_trip` (`recall add "Grüße" "greetings"`, listing compared to `1\tGrüße\tgreetings`); `tests/test_store.py::StoreTest::test_the_store_is_readable_text_with_non_ascii_left_alone` (the file contains `Grüße`, and no `\u` escape) |
| AC8 | `cmd_list` prints `No cards yet.` and returns 0 when the pile is empty, whether or not a file exists | `tests/test_list.py::ListTest::test_a_store_with_no_cards_prints_one_line_and_exits_zero`; `::test_no_store_file_at_all_prints_one_line_and_exits_zero` — both assert exactly one line on stdout and empty stderr |
| AC9 | `cmd_add` returns 2 with `usage: recall add <question side> <answer side>` on stderr for any count but two, before any store access | `tests/test_add.py::AddTest::test_wrong_argument_counts_are_rejected_with_a_usage_line` — a sub-test for each of zero, one and three arguments, each asserting exit non-zero, empty stdout, `usage` plus both argument names on stderr, and `No cards yet.` afterwards |

The tests were checked against a mutant rather than assumed to bite: in a throwaway copy of the
tree under `/tmp`, removing the empty-question check, relaxing the argument-count check from
`!= 2` to `< 2`, and dropping the sort from `cmd_list` produced three failures
[src: run: python3 -m unittest discover -s tests -t . against the mutated copy → FAILED (failures=3)].
The copy was deleted; nothing in this repository was mutated.

## Deviations from the plan

1. **`tests/support.py` exists, and the plan's step list does not name it.** It holds the
   subprocess runner, the per-test temporary store, and the `assertNothingStored` helper that
   AC4, AC6 and AC9 all use. Without it the same twenty lines would be copied into three test
   modules. It contains no product behaviour, and it is test code rather than scaffolding — the
   plan's `## Scaffolding` section still lists only `tests/__init__.py` [src: WI-0001].
2. **`recall list` with an argument is rejected**, printing `usage: recall list` on stderr and
   exiting 2. The plan fixed the positional-only rule and `add`'s argument count and said
   nothing about `list`'s [src: WI-0001]. Some behaviour had to be chosen, since accepting the
   argument silently would suggest a filter exists, and one flat pool with no filtering is the
   stakeholder's decision [src: EP-001/Q-004]. Reversal is one condition in `cmd_list`. It is
   recorded here rather than escalated because AC6 requires `list` to show every card, and
   rejecting a narrowing argument is the reading of that criterion, not a departure from it
   [src: WI-0001 AC6].
3. **Three tests beyond the plan's list.**
   `tests/test_add.py::AddTest::test_a_card_side_may_begin_with_a_dash` pins the consequence of
   ADR-0005's positional-only rule that would otherwise be invisible;
   `tests/test_store.py::StoreTest::test_the_store_is_created_by_the_first_add_and_not_before`
   pins ADR-0004's creation rule; `tests/test_list.py::ListTest::test_list_takes_no_filter_argument`
   pins deviation 2. No product code exists for these three alone.
4. **`load` validates the document's shape**, not only that it parses — a card must have a
   whole-number `number` and string sides. ADR-0004 says a file that "does not have the shape
   above" is refused [src: ADR-0004]; this is that sentence, implemented.

Nothing else departed from the plan. The nine steps were worked in order.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 21 tests`, `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0 errors, 0 warnings |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC9; none is demonstrated by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → `all 2 commit(s) on main..wi/WI-0001 name WI-0001`, exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | the diff is `recall`, `recall.py`, `README.md` and five test modules. Every hunk traces to a plan step or to a deviation recorded above |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 (no document under `docs/` changed on this branch; the ADRs it would check were written and checked by `plan`) |

All seven were run against the branch head, after the last commit.

## What I did not do

- **No `review` command and no scheduling state.** A stored card carries `number`, `question`
  and `answer` and nothing else. WI-0003 adds the scheduling fields and bumps the store's
  `version`; WI-0001 was explicitly told to store what they need without deciding any of it
  [src: WI-0001; WI-0003].
- **No editing or deleting a card**, which is out of scope for the whole epic [src: WI-0001].
- **Nothing about multi-line card text.** A newline inside an argument is stored and listed as
  given, and the listing's one-line-per-card shape would then be wrong. The item puts multi-line
  sides out of scope and no criterion covers it, so there is no test and no handling
  [src: WI-0001].
- **No behaviour for a store file that is valid JSON in some other schema**, beyond refusing to
  use it and saying which file it is [src: ADR-0004].
- **`compileall` is the lint gate and is a compile check**, so unused imports and dead code in
  what I wrote were not machine-checked; ADR-0003 records that, and the reviewer is what catches
  it [src: ADR-0003].
