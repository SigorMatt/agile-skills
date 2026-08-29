# Implementation report — WI-0004

## What was built

`recall delete <card number>` — a fourth command in the shape of the existing three, on branch
`wi/WI-0004` in three commits.

- **`delete_card(document, number)`** in `recall.py`, beside `add_card`: removes and returns the
  card object with that `number`, or returns `None`. It touches no other card and renumbers
  nothing, which is what makes AC3 a property of the design [src: tracker/items/WI-0004/artifacts/plan.md].
- **`cmd_delete(arguments)`** in `recall.py`, in the four-part order the plan fixed: judge the
  command line before opening the store, refuse a store that will not load before deciding
  anything about cards, return without saving when the number names no card, and only then save
  and print. Exit codes `0`, `1`, `2` per `ADR-0009`.
- **`_card_number(text)`**, a small private helper `cmd_delete` uses to decide whether an
  argument is a card number at all — see `## Deviations`.
- **`USAGE_DELETE`**, and `USAGE` widened to `usage: recall <add|list|review|delete>`.
- **`main`** dispatches `delete`.
- **`tests/test_delete.py`** — nine cases, one per criterion AC1–AC9, plus one defending
  `ADR-0008`.
- **`README.md`** — the `### recall delete <card number>` entry under `## Commands` (AC10), plus
  the two corrections the change makes necessary: the exit-code row for `1` and the note that a
  freed number can be reused.
- **`tests/test_docs.py`** — four cases, so AC10 and the two corrections are settled by a checker
  rather than by reading.

Nothing about `add`, `list` or `review` changed, beyond the top-level usage line naming a fourth
command. The store schema and `STORE_VERSION` are untouched, as `ADR-0008` decided.

## Acceptance criteria evidence

Every test below is run by `python3 -m unittest discover -s tests -t .`, which exited 0 with 101
tests. Test names are given in full so a checker can run one on its own with
`python3 -m unittest tests.test_delete.DeleteTest.<name>`.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cmd_delete` saves and prints one line on success; `delete_card` removes only that card | `tests.test_delete.DeleteTest.test_deleting_a_card_removes_it_from_the_pile` — asserts exit 0, `len(stdout.splitlines()) == 1`, and that a following `recall list` prints exactly `["1\tdie Katze\tthe cat", "3\tdas Pferd\tthe horse"]` |
| AC2 | no prompt and no read from stdin anywhere in `cmd_delete`; the success line carries the number and both sides | `tests.test_delete.DeleteTest.test_deleting_acts_immediately_and_says_what_went` — run with `stdin=""`; asserts exit 0, `stderr == ""`, exactly one stdout line, and that the line contains `2`, `der Hund` and `the dog` |
| AC3 | `delete_card` pops one element and writes to no other card; `add_card` is unmodified | `tests.test_delete.DeleteTest.test_the_surviving_cards_are_untouched_and_are_not_renumbered` — reads the store before and after and compares `number`, `question`, `answer`, `due`, `interval` for cards 1 and 3, and asserts the surviving numbers are `[1, 3]` |
| AC4 | the card object is gone from `cards`, so `due_cards` cannot return it | `tests.test_delete.DeleteTest.test_a_deleted_card_is_never_offered_for_review_again` — one card due today, `delete 1`, then `review` exits 0 and prints `Nothing is due today.` |
| AC5 | the `card is None` branch returns 1 without calling `save` | `tests.test_delete.DeleteTest.test_a_number_that_names_no_card_is_refused_and_changes_nothing` — asserts non-zero, `9` in stderr, `stdout == ""`, and the file's **bytes** identical to those read before the run |
| AC6 | `load` reads a missing file as an empty document, so card 1 is not found and the same no-save branch is taken | `tests.test_delete.DeleteTest.test_deleting_with_no_store_file_at_all_creates_nothing` — asserts non-zero, non-empty stderr, and `os.path.exists(self.store)` still false afterwards |
| AC7 | the emptied document is saved through the existing `save`, so it is a valid version-3 store with no cards | `tests.test_delete.DeleteTest.test_deleting_the_last_card_leaves_a_store_the_tool_still_reads` — `list` exits 0 printing `No cards yet.` (via `assertNothingStored`), and a following `add` exits 0 |
| AC8 | argument validation runs before `store_path()` and `load()`, so no failing command line reaches the disk | `tests.test_delete.DeleteTest.test_a_wrong_command_line_is_refused_and_changes_nothing` — four subtests (no argument, `1 2`, `two`, `0`); each asserts non-zero, `usage: recall delete` in stderr, and the file's bytes unchanged |
| AC9 | `load` raises `StoreError`, which is caught before any card decision and before any `save` | `tests.test_delete.DeleteTest.test_a_store_that_cannot_be_read_is_refused_rather_than_repaired` — a store containing `{ not json`; asserts non-zero, the store path in stderr, and the bytes unchanged |
| AC10 | the `### recall delete <card number>` entry under `## Commands`, with an example run and a paragraph on a number that names no card | `tests.test_docs.ReadmeTest.test_the_readme_documents_the_delete_command_beside_the_others` (the heading is inside `## Commands` alongside `list` and `review`, and the entry shows `$ recall delete` and `Deleted card`) and `tests.test_docs.ReadmeTest.test_the_readme_says_what_delete_does_when_the_number_names_no_card` |

Two further tests cover decisions no criterion constrains, so that they are not broken in
silence: `tests.test_delete.DeleteTest.test_the_number_of_the_highest_card_is_reused_by_the_next_add`
(`ADR-0008`) and `tests.test_docs.ReadmeTest.test_the_readme_exit_code_table_gives_the_widened_meaning_of_one`
plus `...test_the_readme_says_a_deleted_cards_number_can_be_reused` (`ADR-0009`, `ADR-0008`).

**The criteria tests bite.** Three mutations of `recall.py` were run against `tests/test_delete.py`
and each turned it red: saving on the not-found path (1 failure, AC5), renumbering the survivors
after a delete (2 failures, AC1 and AC3), and replacing the argument check with a bare `int()`
(1 failure, AC8's `0` case). A fourth, removing the README entry, turned `tests/test_docs.py`
red (1 failure, 1 error). `recall.py` and `README.md` were restored from copies afterwards and
the suite re-run green; no mutation is in any commit.

## Deviations from the plan

Three, all within "how" rather than "what", and none changing what is delivered:

1. **`_card_number(text)` is a named helper rather than an expression inside `cmd_delete`.** The
   plan said only that "argument parsing rejects a count other than one, a non-digit string, and
   a value below 1" [src: tracker/items/WI-0004/artifacts/plan.md]. The behaviour is exactly what the plan and its
   `## Assumptions` specify — a plain decimal integer of 1 or more, so `0`, `two`, `01`, `+1`,
   ` 1` and `1.0` are all refused. `str.isdigit` was **not** used, deliberately: it accepts
   digits from other scripts and superscripts such as `²`, which `int()` then rejects, so the
   check is written against the ASCII digits explicitly.
2. **`recall.py`'s module docstring was updated** from "Three commands live here" to four. Not a
   plan step; it is a claim in a file this change makes wrong, which D12 asks be kept true.
3. **`cmd_delete` catches `StoreError` around `save` as well as around `load`.** The plan's
   four-part order names the `try/except` only at step 2 [src: tracker/items/WI-0004/artifacts/plan.md]. `cmd_add` and
   `cmd_review` both handle a failing write the same way — message on stderr, exit 1 — and
   leaving it out would have made an unwritable directory a traceback rather than a message. No
   criterion covers it; it is consistency with the two commands that already write.

The plan's step 5 asked for a `CommandTestCase` subclass driving the built executable through
`run_recall`, one method per criterion, each naming its AC in the docstring; step 6's reuse case
and steps 7 and 8 were done as written.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 101 tests ... OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0 |
| `workspace-valid` | **pass** | `scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s) ... 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for each of AC1–AC10; none is demonstrated by reading the code, and the mutation runs recorded above show the AC1, AC3, AC5, AC8 and AC10 tests failing when the behaviour is removed |
| `commits-reference-the-item` | **pass** | `scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 3 commit(s) on main..wi/WI-0004 name WI-0004` |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/WI-0004 --stat` → 4 files, +310/−5. `recall.py` = steps 1–4 plus deviations 1–3; `tests/test_delete.py` = steps 5–6; `README.md` = step 7's three edits; `tests/test_docs.py` = step 8 plus the two ADR-defending cases step 7's second half implies. No hunk traces to anything else. |
| `claims-are-sourced` | **pass** | `scripts/lint-claims --changed-since main` → exit 0. It reports `checked no documents changed since main`, which is about its second rule only: no file under `docs/` changed on this branch, so no paragraph was checked for being sourced. Its first rule — every citation resolves — runs over every markdown file in the workspace whatever `--changed-since` says, and it caught this report on its first run: four `[src: plan.md]` markers were not workspace-relative and did not resolve. They now read `tracker/items/WI-0004/artifacts/plan.md`, and the gate passes. |

## What I did not do

- **No `docs/` document was changed.** `ADR-0008` and `ADR-0009` were written by `plan` and the
  overview was bumped to v4 then; nothing this execution built contradicts them, so nothing
  needed correcting. So `claims-are-sourced`'s *sourcing* rule passed over an empty set, which is
  worth saying plainly; its *citation* rule did run, over this report among other files, and
  failed it once before the paths above were made workspace-relative.
- **The plan's risk that `AC3` is only checked on a two-survivor store still stands.** The test
  deletes card 2 of three and compares cards 1 and 3, exactly as `AC3` words it. Nothing
  exercises deleting from the middle of a large pile; the evidence that position is irrelevant is
  `delete_card`'s shape, not a test [src: tracker/items/WI-0004/artifacts/plan.md `## Risks`].
- **The branch is not merged.** `review-close` merges.
- **`README.md`'s `## Not yet built` section was left as written.** It says the tool has no decks,
  no statistics and no schedule command, all still true; deleting a card is not something it
  claimed was missing, so there was nothing to correct there.
