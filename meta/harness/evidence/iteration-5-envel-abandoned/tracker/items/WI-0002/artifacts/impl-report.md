# Implementation report — WI-0002

## What was built

Two new commands and a changed one, on `wi/WI-0002`, in three commits.

- **`envel/movements.py`** (new, 127 lines) — the money half of the domain. `parse_amount` returns
  a positive whole number of pence, stripping one leading `£` and refusing more than two decimal
  places rather than rounding; `format_amount` writes a figure with exactly two decimal places
  (`ADR-0006` rule 3); `parse_date` takes `YYYY-MM-DD` and nothing else; `today` is the local date.
  `balances` computes every envelope's balance from the movements, `balance` looks one up, and
  `record` appends a movement carrying the **stored** display name rather than what was typed. It
  imports `envel.envelopes` and never `envel.store`, so nothing in it touches a filesystem.
- **`envel/store.py`** — format version 2. `empty()` carries a `transactions` list, `_check_shape`
  checks it, `load` upgrades a version 1 document **in memory** and refuses a version it does not
  know. The file is never rewritten by a read.
- **`envel/cli.py`** — `income` and `spend`, sharing one `_record` because they differ only in the
  balance check and one word of the message; `_take_date`, which extracts `--date` by hand and
  leaves a single-dash token alone so `-5` reaches the amount parser; and `envel list`'s second
  column.
- **`tests/`** — `tests/test_movements.py` (19 cases, no subprocess and no file) and 26 new cases
  in `tests/test_cli.py`, of which three are `StoreFormatTests` covering the version upgrade from
  outside the process. Eight existing cases had their `envel list` literals moved to the new line
  shape; every one is still an equality.

`envel/envelopes.py` and `bin/envel` are untouched.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `envel income <envelope> <amount>` parses, records and saves, then prints one line | `tests/test_cli.py::RecordingTests::test_ac1_income_records_into_the_named_envelope` — asserts exit 0, `stderr == ""`, exactly one stdout line, and `groceries` + `400.00` on the listing line afterwards |
| AC2 | `envel spend` records against the envelope | `test_ac2_spend_records_against_the_named_envelope` — exit 0, empty stderr, `340.00` afterwards |
| AC3 | a balance is what went in minus what went out, read from `envel list` | `test_ac3_and_ac5_a_balance_is_what_went_in_minus_what_went_out` — four separate subprocesses; the third is `envel list` and its stdout carries `groceries` and `340.00` |
| AC4 | an unknown envelope is refused and creates nothing; an existing one is found ignoring case | `test_ac4_an_unknown_envelope_is_refused_and_nothing_is_created` (both commands, `rent` on stderr, no `rent` line afterwards) and `test_ac4_an_envelope_is_found_ignoring_case` (`envel spend Groceries 10` on a store where `groceries` holds 40 → exit 0, empty stderr, `30.00`) |
| AC5 | balances survive a later, separate invocation | the fourth invocation in `test_ac3_and_ac5_a_balance_is_what_went_in_minus_what_went_out` |
| AC6 | a spend larger than the balance is refused and nothing is recorded | `test_ac6_a_spend_larger_than_the_balance_is_refused` — non-zero, `groceries` on stderr, `340.00` still on the line |
| AC7 | `--date YYYY-MM-DD` is accepted; a malformed date is refused and records nothing | `test_ac7_a_well_formed_date_is_accepted` and `test_ac7_a_malformed_date_is_refused_and_records_nothing` (subTests `2026-13-01` and `31/08/2026`, each comparing the listing line before and after); unit cases `test_a_month_that_does_not_exist_is_refused` and `test_another_notation_is_refused_even_when_the_day_is_real` |
| AC8 | a spend of exactly the balance is recorded and leaves `0.00` | `test_ac8_a_spend_of_exactly_the_balance_is_recorded` |
| AC9 | zero and negative are refused on both commands | `test_ac9_zero_and_negative_amounts_are_refused_on_both_commands` — four subTests, each comparing the listing line before and after; unit cases `test_zero_is_refused` and `test_a_negative_amount_is_refused` |
| AC10 | `abc` and `""` are refused | `test_ac10_what_is_not_an_amount_is_refused`; unit case `test_what_is_not_a_number_at_all_is_refused` |
| AC11 | a missing argument is refused | `test_ac11_a_missing_argument_is_refused` — `envel income groceries` and `envel spend`, each non-zero with a stderr line and an unchanged listing |
| AC12 | a read of WI-0001's eleven criteria, six waived by name | the eleven-row read below, under `## WI-0001's eleven criteria, read against this change`. `verify` makes the assessment; this is the evidence it reads |
| AC13 | one line carrying envelope, amount, date and balance | `test_ac13_a_successful_recording_says_what_it_recorded` — exit 0, empty stderr, exactly one line, and each of `groceries`, `12.50`, `2026-08-31`, `387.50` in it as a subTest. By hand: `envel spend groceries 12.50 --date 2026-08-31` on a store holding 400 prints `spend 12.50 from groceries on 2026-08-31 — 387.50 left` |
| AC14 | with no `--date` the printed date is today's | `test_ac14_with_no_date_the_printed_date_is_todays` — asserts `datetime.date.today().isoformat()` is in the single stdout line, computed in the test process |
| AC15 | `envel list` carries a balance on each line, in order, byte-stably | `test_ac15_list_carries_a_balance_on_every_line_in_order_and_byte_stably` — exactly two lines, `groceries`+`340.00` first, `rent`+`0.00` second, and byte-identical stdout on a second run |
| AC16 | a new envelope shows `0.00` | `test_ac16_a_new_envelope_shows_a_zero_balance`; unit case `test_an_envelope_with_no_movements_is_zero` |
| AC17 | a single leading `£` is accepted and ignored; the plain forms too | `test_ac17_a_single_leading_currency_symbol_is_accepted_and_ignored` and `test_ac17_the_plain_amount_forms_are_accepted` (`12`, `12.5`, `12.50` as subTests); unit case `test_a_single_leading_pound_sign_is_stripped` |
| AC18 | more than two decimal places is refused rather than rounded | `test_ac18_more_than_two_decimal_places_is_refused_not_rounded` — both commands, the listing line captured before and compared after, and the before line asserted to contain `340.00` so a silent round to `12.34` or `12.35` cannot pass; unit case `test_more_than_two_decimal_places_is_refused_and_says_why` |
| AC19 | the substance of the six waived criteria against the new line shape | `test_ac19_capitalisation_survives_the_new_line_shape` (`Groceries  0.00\n`), `test_ac19_a_name_with_a_space_survives_the_new_line_shape` (`eating out  0.00\n`), `test_ac19_two_envelopes_are_two_lines_in_order` (`a  0.00\nb  0.00\n`) and `test_ac19_a_trimmed_duplicate_is_refused_and_one_line_is_left` (`groceries  0.00\n`). Each asserts the whole of stdout, which is what makes "and nothing else on the line" checkable |

**The suite can fail.** Six deliberate mutations were made one at a time and reverted; each is a
behaviour a criterion names:

| mutation | result |
|---|---|
| `envel list` prints the name without the balance | `FAILED (failures=23)` |
| `spend` stops checking the balance | `FAILED (failures=1)` |
| `parse_amount` accepts any number of decimal places (rounds instead of refusing) | `FAILED (failures=3)` |
| the recording line drops the date | `FAILED (failures=2)` |
| `format_amount` writes one decimal place | `FAILED (failures=23)` |
| a version 1 store is not upgraded | `FAILED (failures=2)` |

## WI-0001's eleven criteria, read against this change

AC12 asks for a verdict per criterion, from a read of the criterion's text rather than from its
test. Six are waived by name because `WI-0002/Q-001` replaced what they require.

| WI-0001 AC | verdict | evidence |
|---|---|---|
| AC1 — `envel new groceries` exits 0, nothing on stderr | **holds** | `test_ac1_new_exits_zero_and_writes_nothing_to_stderr`, unchanged and passing. `_new` is untouched by this item |
| AC2 — a `list` line's only content is `groceries` | **waived — superseded by `WI-0002/Q-001`** | the substance is WI-0002 AC15's; `test_ac2_list_after_new_writes_the_name` now asserts `"groceries  0.00\n"` |
| AC3 — two envelopes, two lines, one name each | **waived — superseded by `WI-0002/Q-001`** | substance re-checked by `test_ac19_two_envelopes_are_two_lines_in_order` |
| AC4 — the lines are byte-wise sorted and two runs are byte-identical | **holds — NOT waived** | `test_ac4_listing_is_sorted_byte_wise_and_repeatable`, whose literal moved to `"Zebra  0.00\napple  0.00\n"` and whose subject — the order and the byte-stability — is unchanged by a second column. Byte-stability is asserted a second time in `test_ac15_...` |
| AC5 — a repeated name is refused, one line left | **waived — superseded by `WI-0002/Q-001`** | substance re-checked by `test_ac19_a_trimmed_duplicate_is_refused_and_one_line_is_left` |
| AC6 — `envel list` before anything exists exits 0 with a line | **holds** | `test_ac6_list_before_anything_exists`, untouched. The `EMPTY_LINE` branch of `_list` returns before the balance column is reached |
| AC7 — capitalisation survives the round trip | **waived — superseded by `WI-0002/Q-001`** | substance re-checked by `test_ac19_capitalisation_survives_the_new_line_shape` |
| AC8 — a name with a space is accepted | **waived — superseded by `WI-0002/Q-001`** | substance re-checked by `test_ac19_a_name_with_a_space_survives_the_new_line_shape` |
| AC9 — an empty name is refused and the store is untouched | **holds** | `test_ac9_an_empty_name_is_refused_and_leaves_the_store_untouched`, untouched. It compares `envel list`'s stdout against a reference captured in the same case, so the new column moves both sides together |
| AC10 — an all-whitespace name is refused likewise | **holds** | `test_ac10_an_all_whitespace_name_is_refused_and_leaves_the_store_untouched`, untouched, same reference-capture shape |
| AC11 — surrounding whitespace is trimmed before comparing | **waived — superseded by `WI-0002/Q-001`** | substance re-checked by `test_ac19_a_trimmed_duplicate_is_refused_and_one_line_is_left` |

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|---|---|---|---|---|
| `docs/architecture/overview.md` | the `envel/cli.py` row, "dispatches to `new` or `list`" `[src: envel/cli.py:27]` | cited-fact | there are four commands after step 5. Row rewritten to name all four; citation moved to `envel/cli.py:42`, which is `def main`, verified by `sed -n 42p envel/cli.py` → `def main(argv=None) -> int:`. A second citation `envel/cli.py:104` was added for `_take_date`, verified the same way → `def _take_date(rest):` | 3 |
| `docs/architecture/overview.md` | the table has four rows and there is a fifth module | cited-fact | a fifth row added for `envel/movements.py`, citing `:50`, `:68`, `:77` and `:97`. Each verified with `sed -n <n>p` → `def parse_amount`, `def format_amount`, `def parse_date`, `def balances` | 3 |
| `docs/architecture/overview.md` | the dependency-direction sentence | **quantified** | the enumeration is below, under `## The dependency-direction enumeration` | 3 |
| `docs/architecture/overview.md` | the `envel/store.py` row's citations `:27; :39; :58` | cited-fact | step 3 inserted lines above them. Moved to `:28`, `:40`, `:79`; verified → `def store_path`, `def load`, `def save` | 3 |
| `docs/architecture/overview.md` | `## State`, "a JSON document holding the store-format version and the envelopes in creation order" | cited-fact | it also holds the movements now, and the version is 2. Rewritten, citing `ADR-0007` and `envel/store.py:25` (`return {"version": VERSION, "envelopes": [], "transactions": []}`) and `envel/store.py:65` (`def _upgrade`). A second paragraph records that a balance is computed rather than stored, citing `envel/movements.py:97` | 3 |
| `docs/architecture/overview.md` | `## Conventions`, `[src: ... run: ... → exit 0, 24 tests, OK]` | cited-fact | re-ran the command: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests`, `OK`. Recorded outcome updated to 69 | 3 |
| `docs/architecture/overview.md` | `## Conventions`, `[src: tests/test_cli.py:29]` — **the row this execution added to the set** | cited-fact | the helper moved when step 9's imports were added. `sed -n 35p tests/test_cli.py` → `return subprocess.run(["envel", *arguments], env=environment,`. Citation moved to `:35` | 3 |
| `docs/product/vision.md` | `## Engagement state`, all three bullets | engagement-state | **nothing done, and nothing may be.** `spec/doc-header.md` §4a gives it to `review-close` at the ending. Not read, not tidied, not repaired | — |
| `docs/architecture/adr/ADR-0003-...md` | the `{"version": 1, ...}` block and "Its shape at this version" | cited-fact | reopened at lines 62–74. The sentence is scoped *at this version* and a version 1 document on disk still looks exactly like the block: `_upgrade` changes the returned dict and never the file, which `test_reading_a_version_one_store_does_not_rewrite_the_file` asserts by comparing the file's bytes before and after `envel list`. **Not falsified** | unchanged (1) |
| `docs/architecture/adr/ADR-0006-...md` | rule 3, "every amount and every balance the tool prints is written with exactly two decimal places" | **quantified** | the enumeration is below, under `## ADR-0006 rule 3's enumeration`. Rule 3 itself is **not falsified — this item is the first to make it true — and was not edited.** The document did change after this report was first written: `answer-questions`, resolving `Q-004`, added a citation to option B of `## Options considered` through an append-only `## Corrections` entry of kind `provenance`. That is a different sentence from this row's subject and it changed no assertion | 2 (by `answer-questions`, for `Q-004`) |
| `docs/process/ways-of-working.md` | the whole document | cited-fact | reopened both sections. `## When a pipeline gate refuses something no actor is permitted to fix` is about `scripts/lint-claims` and the four override conditions; `## Where an accepted test-coverage gap goes` is about how a review's accepted gap is carried. Neither mentions the tool's behaviour, its store, its commands or its output. **Not falsified by this item's code**, and this execution used the first section rather than changing it. `answer-questions` then changed the second section for `Q-004`: one sentence gained the two citations it owed and its opening clause was weakened from *"If no dispatchable item opens that code"* to *"Absent a dispatchable item that opens that code"*. What the convention requires is unchanged | 3 (by `answer-questions`, for `Q-004`) |

### The dependency-direction enumeration

The claim is: *"`cli` imports the other three; `movements` imports `envelopes` for the identity
rule and does not import `store`; `envelopes` imports nothing of this project's and touches no
filesystem; and `store` names no envelope rule and no money rule."*

The set is every module under `envel/`, enumerated with
`ls envel/*.py` → `envel/__init__.py  envel/cli.py  envel/envelopes.py  envel/movements.py
envel/store.py`. `envel/__init__.py` is empty (0 lines) and is not a piece of the system; the
other four are the members.

Imports, from `grep -n "^from envel\|^import \|^from " envel/*.py`:

```
envel/cli.py           10:from __future__ import annotations  12:import sys  14:from envel import envelopes, movements, store
envel/envelopes.py      7:from __future__ import annotations
envel/movements.py      8:from __future__ import annotations  10:import datetime  11:import re  13:from envel import envelopes
envel/store.py          8:from __future__ import annotations  10:import json  11:import os  12:import tempfile
```

Filesystem, from `grep -ln "open(\|os\.\|tempfile" envel/*.py` → `envel/store.py`, and nothing else.

| member | verdict |
|---|---|
| `envel/cli.py` | **true** — imports `envelopes`, `movements` and `store`, which is the other three |
| `envel/movements.py` | **true** — imports `envelopes` (for `identity`) and does not import `store`; not in the filesystem grep |
| `envel/envelopes.py` | **true** — imports nothing of this project's and nothing at all beyond `__future__`; not in the filesystem grep |
| `envel/store.py` | **true** — imports `json`, `os` and `tempfile` and no module of this project's, so it can name no envelope rule and no money rule |

### ADR-0006 rule 3's enumeration

The claim is: *"every amount and every balance the tool prints is written with exactly two decimal
places"*. The set is every place the tool prints a money figure. Enumerated with
`grep -n "print(" envel/cli.py` (21 print statements, the only prints in the project) and then
`grep -rn "format_amount(" envel/` for the sites that carry a figure:

```
envel/cli.py:100:        print(f"{name}  {movements.format_amount(totals.get(envelopes.identity(name), 0))}")
envel/cli.py:167:        print(f"envel: {entry['name']} holds {movements.format_amount(held)}, which is less "
envel/cli.py:168:              f"than {movements.format_amount(pence)}", file=sys.stderr)
envel/cli.py:177:    print(f"{kind} {movements.format_amount(pence)} {preposition} {entry['name']} on {date}"
envel/cli.py:178:          f" — {movements.format_amount(left)} left")
```

Three print sites, five figures, which is the count `plan`'s invalidation row predicted:

| member | verdict |
|---|---|
| the `envel list` line (`cli.py:100`) — the balance | **true**, through `format_amount` |
| the shortfall refusal (`cli.py:167–168`) — the balance held and the amount asked for | **true**, both through `format_amount` |
| the successful-recording line (`cli.py:177–178`) — the amount and what is left | **true**, both through `format_amount` |

The other 18 prints carry no money figure: they are `USAGE*`, `EMPTY_LINE`, and `envel:` refusals
naming a command, a name, a date or a `StoreError`. The amount refusals print `{problem.text!r}`,
which is the text the person typed and not a figure the tool computed — `envel spend groceries
12.345` says `'12.345'`, not `12.35`, which is the point of `ADR-0006` rule 2.

`format_amount` is `f"{pence // 100}.{pence % 100:02d}"`, exercised at `12.50`, `0.00` and
`400.00` by `test_format_amount_writes_two_decimal_places`, and the mutation to one decimal place
failed 23 tests.

## Deviations from the plan

1. **`InvalidAmount` carries a `reason`.** Plan step 1 lists `parse_amount` raising
   `InvalidAmount(text)`, and plan step 5 asks for a *different* refusal message when the text was
   a number with too many decimal places. Nothing in the plan says how `_record` learns which it
   was. Rather than duplicate the amount grammar in `envel/cli.py` — where it would be a second
   copy of the rule that could drift from the first — `InvalidAmount` gained an optional `reason`,
   set to `movements.OVER_PRECISE` on that one path and `None` otherwise. This is *how*, not
   *what*: the messages are exactly the plan's two. `test_a_refusal_that_is_not_about_precision_carries_no_reason`
   is what stops the reason being set everywhere.
2. **`_take_date` raises rather than returning a sentinel.** Plan step 4 says it raises
   "`MISUSE`-shaped handling in its caller". It raises a module-private `_BadOption`, which
   `_record` catches and turns into the usage line and `MISUSE`.
3. **`_check_shape` skips the `transactions` key only on a version 1 document**, not on any
   document lacking the key. Plan step 3 says "check the key only when it is present"; taken
   literally, a *version 2* document that had lost its `transactions` would pass the shape check
   and then raise a `KeyError` in `balances`. Narrowing the tolerance to `version == 1` keeps
   assumption P4 (check what is on disk, before the upgrade) and closes that hole.
4. **The AC3 and AC5 cases are one test, not two.** AC5 is defined as "after AC3's two
   invocations, a fourth invocation" — it is the same store, and splitting it would mean building
   the same state twice to assert the same line. Named `test_ac3_and_ac5_...` so neither criterion
   is invisible to a reader searching for it.
5. **`StoreFormatTests` was added and the plan does not name it.** Plan step 3's "afterwards"
   sentence is a by-hand check — *"`envel list` against a store file written by WI-0001 exits 0"* —
   and steps 7 and 9 say nothing about the upgrade. Three end-to-end cases assert it instead of a
   person doing it once, which is what `every-criterion-has-a-test` asks for everywhere else. The
   third of them covers the "written by a newer `envel`" refusal, which is plan step 3's other half.

## Gates

| gate | verdict | evidence |
|---|---|---|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests`, `OK` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `validate-workspace` → `checked 7 item(s), 10 document(s)`, 0 errors, before this execution's closing transition. It failed with `doc.changelog.no-execution` on each earlier pass of this item — the change-log row is made true by the journal entry the transition itself appends — and cleared each time the entry landed |
| `every-criterion-has-a-test` | pass | the nineteen rows above, each naming a test function; plus six mutations, each of which broke the suite |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0002 wi/WI-0002` → `all 6 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| `no-unplanned-scope` (advisory) | pass | `git diff --stat main..HEAD` → five files, all named by the plan: `envel/cli.py`, `envel/movements.py`, `envel/store.py`, `tests/test_cli.py`, `tests/test_movements.py`. Every hunk traces to a plan step; the five deviations above are the ones a reader would not predict from the plan text |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → `claim window: 3 path(s) differ from main (ce87246) under docs`, `checked 10 consumed human answer(s) and 0 delegation(s)`, 0 errors. No sentence sourced to a stakeholder answer was edited, by this execution or by `answer-questions` on this branch |
| `claims-are-sourced` | **fail, forced** | `lint-claims --changed-since main --plan-documents WI-0002` → **1 error**, down from 3. The one left is `docs/product/vision.md:85`, inside that document's `## Engagement state` section, which no skill may repair before the ending. The other two were answered and repaired by `answer-questions` on `Q-004`. Forced under `docs/process/ways-of-working.md`, `## When a pipeline gate refuses something no actor is permitted to fix`; the four conditions are walked in this execution's journal entry |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → `3 document(s) written under docs/ on this branch; 5 named by the plan`, 0 errors. It failed once in between with `document.disposition.unknown` on both rows `answer-questions` re-disposed, which had written its reasoning into the disposition cell rather than into `why`; the cell is `implement`'s to write and the prose was moved |

## What I did not do

- **`docs/product/vision.md` was not touched**, at any disposition. Its invalidation row is
  `owned-by-ending` and `review-close` restates every `## Engagement state` section at the ending.
  Its `claim.unsourced` error is one of the three `claims-are-sourced` reported, and it is the one
  `WI-0001/Q-003` and `docs/process/ways-of-working.md` already own.
- **`ADR-0006` and `docs/process/ways-of-working.md` were not edited by this skill**, and their two
  `claim.unsourced` errors were not cleared by it. `spec/doc-header.md` §5 gives an ADR's document
  half to an append-only `## Corrections` section and `ways-of-working.md` to `review-close` and
  `answer-questions`; neither is `implement`'s. `questions/Q-004.md` was filed blocking, the item
  suspended, and `answer-questions` made both repairs — refusing this report's recommendation to
  leave `ADR-0006` alone, on §4b's ground that a `provenance` correction changes no assertion.
  Both documents are now `to-update` in the invalidation set, discharged by that execution.
- **`BUG-0001`'s fix is not on this branch**, and this branch does not anticipate it. Under a
  non-UTF-8 locale the success line's `—` cannot be encoded and would raise where the old code
  raised on a non-ASCII envelope name — the same out-hop `ADR-0005` already records as broken for
  `envel list` today. `ADR-0005` decision B fixes both at once by setting stdout's error handler,
  and that is `BUG-0001`'s step to make. Whoever merges second must read `main` rather than take
  either side, which is `plan`'s first risk.
- **Nothing was cached.** `balances` walks the movements on every command (assumption P3). With a
  personal budget's number of transactions that is not measurable; `ADR-0007` decision C is where
  the alternative is recorded.
- **`format_amount` is not written for a negative balance** and would print `-1.50` for `-50`
  pence. Nothing in this item can produce one — AC6 and AC9 are what prevent it — and WI-0005,
  which can reduce a balance by correcting a spend, is where it must be looked at again. This is
  `plan`'s last risk, carried forward unchanged.
