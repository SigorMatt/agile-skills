# Implementation report — WI-0005

## What was built

Two subcommands, `envel fix <ref>` and `envel remove <ref>`, and the two operations behind them.

- `envel/envelopes.py` gains four functions: `find_entry` (locate an entry by the reference the
  person typed), `envelopes_below_zero` (the one place AC9 and AC18's question is asked), `correct`
  and `remove`.
- `envel/cli.py` gains the two subparsers, the two dispatch branches, and the check that
  `envel fix <ref>` with no option prints the subcommand's own usage **before the store is read**.
- `tests/test_corrections.py` is new — 34 cases over the operations as functions.
- `tests/test_cli.py` gains a `Corrections` class — 26 cases running the tool as a separate
  process with `stdin` closed.

Nothing else was touched. `envel/summary.py`, `envel/store.py`, `envel/money.py` and
`envel/dates.py` are byte-identical to `main`, which is the plan's own test of whether the design
held: AC7, AC8, AC14 and AC20 are satisfied because `ADR-0011` leaves every reader unchanged, and
they are demonstrated rather than built.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|--------------------|----------|
| AC1 | `find_entry` reads the reference as a decimal integer and matches `entry["ref"]` by equality; text that is not a number names no entry and takes the same refusal | `tests/test_corrections.py::FindingAnEntry` (3 cases), `CorrectingIsRefused::test_a_reference_no_entry_has`, `::test_a_reference_that_is_not_a_number`; `tests/test_cli.py::Corrections::test_a_reference_no_entry_has_is_refused_and_changes_nothing` — stderr names `999`, exit 1, `envel list` identical before and after |
| AC2 | `correct` writes `cents` keeping the entry's own sign, and reports the envelope and its new balance | `tests/test_cli.py::Corrections::test_correcting_the_amount_reports_the_envelope_and_its_new_balance` — `envel fix <ref> --amount 14.00` on a 12.50 spend prints `corrected entry 3 in groceries, which now holds 86.00`, exit 0; `tests/test_corrections.py::CorrectingASpend::test_the_amount_keeps_the_negative_sign_a_spend_stores` |
| AC3 | `--on` is parsed by `dates.parse_date` in `envel/cli.py`, and a date later than `dates.today()` is refused in `correct` | `tests/test_cli.py::Corrections::test_correcting_the_date_accepts_the_full_form_only` — `--on 2026-08-28` succeeds, `--on 7/9` and `--on <tomorrow>` are each refused and the stored `on` is unchanged after both |
| AC4 | blank or empty `--description` deletes the key; anything else sets it | `tests/test_cli.py::Corrections::test_a_description_is_set_and_then_taken_off_entirely` — reads the JSON file and asserts `description` is absent, not empty; `tests/test_corrections.py::CorrectingASpend::test_an_empty_description_takes_the_key_off_entirely` and `::test_a_blank_description_takes_the_key_off_too` |
| AC5 | `correct` writes the stored envelope's own spelling; a name no envelope has is refused | `tests/test_cli.py::Corrections::test_correcting_the_envelope_moves_the_amount_between_exactly_two` — three envelopes, `envel list` afterwards is exactly `eating out 37.50 / fun 20.00 / groceries 100.00`; `::test_an_envelope_that_does_not_exist_is_refused`; `tests/test_corrections.py::CorrectingASpend::test_the_envelope_is_matched_without_regard_to_capitalisation` |
| AC6 | the four options are independent and are applied in one pass; none given is caught in `envel/cli.py` | `tests/test_cli.py::Corrections::test_all_four_options_in_one_invocation_apply_all_four` (asserts all four stored fields), `::test_no_option_at_all_prints_the_subcommands_usage_and_changes_nothing` (stderr contains `usage: envel fix`, the store file is byte-identical), `::test_a_trailing_argument_is_reported_by_the_fix_parser` |
| AC7 | falls out of `ADR-0011` — the entry is edited where it sits and every reader is unchanged | `tests/test_cli.py::Corrections::test_only_the_envelopes_the_correction_names_change` — `envel list` parsed before and after; the untouched envelope's figure is equal and `groceries` is `86.00` |
| AC8 | falls out of `ADR-0011` — the summary reads the same entries, and a corrected `on` moves the entry between months with nothing left behind | `tests/test_cli.py::Corrections::test_a_corrected_date_moves_the_spend_into_exactly_one_month` — August goes to `spent 0.00` and September to `spent 12.50`; `::test_a_corrected_amount_shows_in_a_past_months_summary` — August shows `spent 14.00` and the string `12.50` appears nowhere in it |
| AC9 | `envelopes_below_zero` over the candidate document, refusing with the envelope, what it holds and the shortfall | `tests/test_cli.py::Corrections::test_a_correction_below_zero_names_the_envelope_and_the_shortfall` — stderr carries `groceries`, `17.50` and `110.00`, exit 1, `envel list` identical and containing no `-`; `tests/test_corrections.py::CorrectingIsRefused::test_an_amount_that_would_take_the_envelope_below_zero` |
| AC10 | `cents <= 0` is refused before the copy is taken | `tests/test_cli.py::Corrections::test_a_zero_or_negative_amount_is_refused` (both, as sub-tests); `tests/test_corrections.py::CorrectingIsRefused::test_an_amount_of_zero`, `::test_a_negative_amount` |
| AC11 | `remove` deletes the entry and reports the envelope, the amount, the date and the new balance | `tests/test_cli.py::Corrections::test_removing_a_spend_says_what_went_and_asks_nothing` — every invocation in the class runs with `stdin=subprocess.DEVNULL`, so a prompt could not pass; stdout carries `groceries`, `12.50`, `2026-09-06` and `100.00` |
| AC12 | the same identity refusal as AC1, in `remove` | `tests/test_cli.py::Corrections::test_removing_a_reference_no_entry_has_is_refused`; `tests/test_corrections.py::RemovingAnEntry::test_a_reference_no_entry_has_is_refused` |
| AC13 | both operations refuse on `entry["kind"] == "move"` alone, never by finding the other half | `tests/test_cli.py::Corrections::test_neither_half_of_a_move_can_be_corrected_or_removed` — the two references are read off the listing and each is refused by both commands; `tests/test_corrections.py::AMoveIsNeitherCorrectedNorRemoved` (3 cases) |
| AC14 | falls out of `ADR-0011` — the store is written whole and read back by the next process | `tests/test_cli.py::Corrections::test_a_correction_survives_between_invocations` — a fix, then `envel list`, `envel summary 2026-08` and `envel entries --month 2026-08` as separate processes, then a remove and two more |
| AC15 | every refusal returns a `Refusal`, which `envel/cli.py` prints to stderr with exit 1, or is argparse's own usage with exit 2 | the `succeeded()` and `refused()` helpers in `tests/test_cli.py::Corrections` assert the stream, the emptiness of the other stream and the exit code on **every** case in the class — refusals at AC1, AC3, AC5, AC6, AC9, AC10, AC12, AC13, AC16, AC18 and AC19; successes at AC2, AC4, AC5, AC7, AC11, AC16, AC17 and AC20 |
| AC16 | an entry with no `on` is income; `--on` and `--description` on one are refused, `--amount` and `--envelope` behave as AC2 and AC5 | `tests/test_cli.py::Corrections::test_an_incomes_amount_and_envelope_can_be_corrected`, `::test_an_incomes_envelope_takes_the_whole_amount_with_it`, `::test_a_date_or_a_description_on_an_income_is_refused` (the store file is byte-identical after both), `::test_a_zero_amount_on_an_income_is_still_refused` |
| AC17 | `remove` takes no flag and prints a date only when the entry has one | `tests/test_cli.py::Corrections::test_removing_an_income_uses_the_same_command_with_no_flag` — stdout carries `groceries` and `100.00` and not ` on `; `tests/test_corrections.py::RemovingAnEntry::test_an_income_goes_by_the_same_command_and_its_line_carries_no_date` |
| AC18 | the same `envelopes_below_zero` call in `remove`, and in `correct` over both the entry's old and new envelope | `tests/test_cli.py::Corrections::test_the_three_income_changes_that_would_leave_an_envelope_short` — removing it, correcting it downwards and moving it, each refused naming `groceries` and `10.00`, with `envel list` identical after all three; `tests/test_corrections.py::CorrectingAnIncome::test_an_envelope_change_that_would_leave_the_source_short_is_refused` |
| AC19 | every refusal returns before or without a document, and `envel/cli.py` saves only what an `Ok` carries | `tests/test_corrections.py::UnchangedOnRefusal` (3 cases) compares the document passed in against a deep copy taken first; `tests/test_cli.py::Corrections::test_a_refused_invocation_applies_none_of_its_accepted_options` — the entry's own listing line and the whole of `envel list` are identical before and after `--amount 20.00 --on 2026-09-01` on an income |
| AC20 | falls out of `ADR-0011` — `envel/summary.py` reads the same entries | `tests/test_cli.py::Corrections::test_the_listing_shows_a_corrected_amount_envelope_and_month` (asserts the exact line after each of three corrections, and that the line appears once in the new month and not at all in the old), `::test_a_removed_entry_is_in_no_months_listing`, `::test_the_listing_still_adds_up_after_a_correction` |

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|-----------|----------------------------------|-------------|
| `ADR-0002` | `## Decision`: *"`entries` is append-only within a run and ordered as written…"* | quantified | **Repaired as an erratum.** The first clause is false against the code: `remove` filters the entry out of the list [src: envel/envelopes.py:451]. The other two clauses were re-read and are true — the entry keeps its place (`tests/test_corrections.py::CorrectingASpend::test_the_entry_keeps_its_place_in_the_list`) and `balance` still sums `cents` with no branch on `kind` [src: envel/envelopes.py:63]. The decision is untouched and no code has to change to satisfy the new text | 4 |
| `ADR-0002` | `## Consequences`: *"readable and repairable in any text editor"*, and the reversibility paragraph | cited-fact | Still true, and not engaged. The reversibility paragraph is about changing the document's **shape** — *"any change to the document needs code that reads the old `format` and writes the new one"* sits under *"changing the shape is one module"* — and `ADR-0011` changes no key: `git diff main..HEAD -- envel/store.py` is empty, so `FORMAT` is still `2` and no migration exists to be needed | — |
| `ADR-0010` | `## Consequences`: *"A reference survives a removal because it is stored rather than derived, so `WI-0005` inherits the property"* | cited-fact | Still true, and now demonstrated rather than predicted: `tests/test_corrections.py::RemovingAnEntry::test_the_counter_is_not_lowered_by_a_removal` records an entry after a removal and asserts it takes the counter's number, that the removed reference is not reissued, and that no reference repeats | — |
| `ADR-0010` | `## Decision` 5: *"The counter is the only source of a new reference. Nothing derives one from a position, a length or a maximum"* | quantified | Still true. **Set:** every place a `ref` or `next-ref` is written in `envel/`, enumerated with `grep -n '\["ref"\]\|"ref":\|next-ref\|take_ref' envel/*.py` → 21 lines in three files. **Members and verdicts:** `envelopes.py:41–50` `take_ref` — the counter, reads and advances it, unchanged; `envelopes.py:111`, `:173`, `:270`, `:276` — the four appends, each taking `take_ref(store)`, unchanged; `store.py:36` `empty_store` and `store.py:53–55` `upgraded` — the format-1 upgrade, unchanged. **Added by this change:** `envelopes.py:309` (`find_entry`, reads), `:354`, `:359`, `:409`, `:415`, `:445`, `:474` (messages, read), `:451` (`remove`'s filter, compares). Not one of them writes a `ref` or touches `next-ref`, and none derives a number from a position, a length or a maximum | — |
| `ADR-0007` | `## Decision` and `## Consequences`: the two-entry shape and what nothing links | quantified | Still true. **Set:** every mention of the move kind in `envel/`, enumerated with `grep -n '"move"' envel/*.py` → 11 lines. **Members and verdicts:** `cli.py:59`, `:127`, `:171` — the `move` subcommand, unchanged; `envelopes.py:207`, `:269`, `:275` — the two appends, unchanged; `summary.py:67`, `:129` — the moved figure and the direction on a line, unchanged. **Added:** `envelopes.py:351` and `:442`, the AC13 refusals, each reading `entry["kind"]` on the entry it was handed. Neither looks for the other half, so nothing new reads the adjacency as a link | — |
| `ADR-0006` | `## Decision`: *"`on` is present on every spend entry… never absent and never null"*, and *"`description` is present only when one was typed"* | quantified | Still true. **Set:** every write or delete of either key, `grep -n '\["on"\]\|"on":' envel/*.py` → 6 lines and `grep -n 'description' envel/envelopes.py` → 3 assignment lines. **Members and verdicts:** `on` is written at `envelopes.py:171` (`record_spend`), `:269`, `:275` (the two move halves) and `:386` (`correct`, which only ever **sets** it — nothing deletes an `on` anywhere in the tool); it is read at `:469` and `summary.py:39`. `description` is written at `:176` (`record_spend`) and `:391` (`correct`), and removed at `:389` — by `pop`, so the key is absent rather than empty, which `tests/test_cli.py::Corrections::test_a_description_is_set_and_then_taken_off_entirely` asserts against the JSON file | — |
| `ADR-0009` | `## Decision`: reporting in `envel/summary.py`, operations in `envel/envelopes.py` | cited-fact | Still true. Both new operations are in `envel/envelopes.py`; `git diff --stat main..HEAD` shows `envel/summary.py` is not in the diff at all. `envel/envelopes.py`'s imports are `copy`, `dataclasses`, `datetime` and `from . import dates, money` [src: envel/envelopes.py:12] — no `summary`, which was the temptation the plan's risk list named | — |
| `ADR-0008` | `## Decision`: a month is the string `YYYY-MM` compared as a string, every figure is a filtered sum | quantified | Still true. **Set:** every month computation and every figure in `envel/`. **Verdict:** the diff adds none — `envel/summary.py` and `envel/dates.py` are unchanged, and neither `correct` nor `remove` mentions a month. AC8's *exactly one month* is `entry_month` applied to a changed `on` and nothing else, which is why it needed no code | — |
| `ADR-0001` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | Still true. **Set:** every text/amount conversion added by this branch, enumerated over the diff's added lines → `money.format_amount` ×10, `money.parse_amount` ×1, and no other conversion of any kind. **Members:** the ten renderings are the two success lines and the amounts inside the five refusal messages; the one parse is `--amount` in `envel/cli.py`. No arithmetic on a string and no formatting outside `envel/money.py` | — |
| `ADR-0003` | `## Decision`/`## Consequences`: one function in `envel/store.py` resolves the path | quantified | Still true. **Set:** any reference to a store path outside `envel/store.py`. `grep -n 'store_path\|ENVEL_FILE\|pathlib\|\.json' envel/envelopes.py` → no matches. `envel/store.py` is not in the diff | — |
| `ADR-0004` | `## Decision`: two entry points *"both reaching the same `main`"* | quantified | Still true. **Set:** the two entry points, `bin/envel` and `python3 -m envel`. **Verdict:** both reach the new subcommands — `tests/test_cli.py::Corrections::test_both_entry_points_reach_the_same_commands` runs a `fix` and a `list` through `python3 -m envel` while every other case in the class runs through the shim. Neither entry point was edited | — |
| `ADR-0005` | `## Decision`: the two commands and what lint checks | cited-fact | Still true. Both run over everything this change touched: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 299 tests`, `OK`; `python3 -m compileall -q envel tests` → exit 0. No import outside the standard library was added — `envel/envelopes.py` adds none at all and `tests/test_cli.py` adds `re` | — |
| `docs/architecture/overview.md` | `## The parts`: the `envel/envelopes.py` row naming seven operations | cited-fact | Still true, and now true of code rather than of a design: `create`, `add_income`, `listing`, `record_spend`, `move`, `correct`, `remove` are the seven, all in `envel/envelopes.py` | — |
| `docs/architecture/overview.md` | `## The parts`: the dependency direction | quantified | Still true. **Set:** every import in `envel/`, enumerated with `grep -n '^from \. import\|^import ' envel/*.py` → 15 lines. **Members and verdicts:** `cli.py:13` imports all five below it; `summary.py:28` imports `dates`, `envelopes`, `money`; `envelopes.py:12` imports `dates`, `money` **and not `summary`**; `store.py`, `money.py` and `dates.py` import nothing from the package. The direction is unchanged and `envelopes` still does not know about `summary` | — |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | Still true. **Set:** the five modules below `cli`. `grep -n 'print(\|sys.exit' envel/envelopes.py envel/summary.py envel/store.py envel/money.py envel/dates.py` → no matches. `correct` and `remove` return their line inside `Ok` and their message inside `Refusal` | — |
| `docs/architecture/overview.md` | `## The shape of it`: the three beats, *"only if something changed"* | quantified | Still true. **Set:** the paths through `main` that can write. **Verdict:** a `Refusal` has no `changed` attribute and never reaches `store.save`, and `envel fix <ref>` with no option exits before `store.load` is called at all — `tests/test_cli.py::Corrections::test_no_option_at_all_prints_the_subcommands_usage_and_changes_nothing` compares the file's bytes | — |
| `docs/architecture/overview.md` | `## The data`: the entries paragraph as rewritten at v9 | cited-fact | Still true. It says the list was append-only until `WI-0005`, that a correction edits an entry where it sits and a removal deletes it, that the entries are still ordered as written and summed with no branch on `kind`, and that `format` stays `2` — every clause is what was built, and `envel/store.py` is not in the diff | — |
| `docs/architecture/overview.md` | `## The data`: *"`ref`… written when the entry is appended and never changed afterwards"* | quantified | Still true; the same enumeration as `ADR-0010`'s row above. `tests/test_corrections.py::CorrectingASpend::test_the_reference_the_kind_and_the_recording_moment_are_untouched` asserts it after a four-option correction | — |
| `docs/architecture/overview.md` | `## The data`: the move paragraph, *"No code reads that adjacency as a link"* | quantified | Still true; the same enumeration as `ADR-0007`'s row. The two refusals added read `entry["kind"]` on the one entry they were handed | — |
| `docs/architecture/overview.md` | `## Conventions`: stdout with exit 0, stderr with a non-zero exit | quantified | Still true. **Set:** every path this change adds — two successes and ten refusals (AC1 ×2 commands, AC3, AC5, AC6, AC9, AC10, AC12, AC13 ×2, AC16 ×2, AC18). **Verdict:** asserted case by case; the `succeeded()` and `refused()` helpers check both streams and the exit code on every one | — |
| `docs/architecture/overview.md` | `## Conventions`: amounts with two decimals and no symbol | quantified | Still true; the same enumeration as `ADR-0001`'s row — every amount printed goes through `money.format_amount` | — |
| `docs/architecture/overview.md` | `## Conventions`: dates parsed in `envel/dates.py` and nowhere else | quantified | Still true. **Set:** every command-line date. **Verdict:** `--on` is parsed by `dates.parse_date` in `envel/cli.py` and the future check uses `dates.today()`; the write uses `dates.format_date`. `envel/dates.py` is not in the diff and no date string is sliced or compared anywhere in `envel/envelopes.py`'s new code | — |
| `docs/architecture/overview.md` | `## What is not decided yet`: *"Nothing. Every item of `EP-001` has had its design taken"* | quantified | Still true. **Set:** the items of `EP-001`, enumerated from `tracker/board.md` → `WI-0001` … `WI-0006`, six. **Verdict:** five `done` and this one `in-progress` with its plan written. No bug item was filed by this execution and no item was created, so the family the sentence quantifies over has not grown | — |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Not touched, at any disposition. `review-close` restates it at the ending | — |
| `docs/product/vision.md` | `## What it is for`: the correction paragraph | cited-fact | Still true, and now delivered. Each clause has a criterion and a test: a correction reaches all four fields of a spend (AC2–AC5), a spend can be removed by a command that says what it took (AC11), a below-zero correction is refused with the shortfall named (AC9), and moves stay outside it (AC13). **Not edited** — every sentence in it cites one of the stakeholder's answers and none of them has been overtaken | — |
| `docs/product/vision.md` | `## What it is for`: the income paragraph | cited-fact | Still true, and now delivered: AC16, AC17 and AC18. **Not edited**, for the same reason — it is `WI-0005/Q-006` and `Q-007` in their own words, and what was built is what they said | — |
| `docs/product/vision.md` | `## What it is for`: *"the number an entry is given stays that entry's"* | quantified | Still true. **Set:** the events that could break it — a removal, and an entry recorded after one. **Verdict:** `tests/test_corrections.py::RemovingAnEntry::test_the_counter_is_not_lowered_by_a_removal` covers both and additionally asserts that no reference repeats across the whole list | — |
| `docs/product/vision.md` | `## What it deliberately is not`: *"no server, no sync, no bank import, no network"* | quantified | Still true. **Set:** every import added by this branch, enumerated over the diff → `envel/envelopes.py` adds none; `envel/cli.py` adds none; `tests/test_corrections.py` imports `copy`, `datetime`, `unittest` and the package; `tests/test_cli.py` adds `re`. All standard library, none of them a network or a service | — |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Not touched, at any disposition | — |

## Deviations from the plan

- **None in what was built.** All twelve steps were executed as written, in order, and no step was
  found impossible or differently shaped than the plan assumed.
- **One thing the plan did not foresee about the *tests*.** Two criteria — AC8 and AC14's
  month-crossing half — cannot be observed against a store the delivered commands build, because
  `envel new` stamps `created` with the moment it runs and `WI-0003` AC4 gives a summary row only
  to an envelope that existed by the end of the month. Those two cases therefore seed the store
  file directly, with envelopes created in July and at `format: 1`, which is what
  `tests/test_cli.py::Entries` already does for the same reason. No production behaviour changed;
  the deviation is in how the evidence is set up, and it is recorded here because a reader of the
  test module would otherwise wonder why one class has two ways of seeding a store.
- **One assumption spent as the plan wrote it.** The `fix` success line names the source envelope
  as well when `--envelope` moved the entry — `corrected entry 3, moving it from groceries, which
  now holds 100.00, to eating out, which now holds 37.50`. That is the plan's `## Assumptions`
  entry, taken under no delegation, and it costs one `format` call to reverse.

## Gates

All nine were run on the branch head, after the last commit.

- `tests-pass` → **pass**: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 299 tests`,
  `OK`. 231 of those were passing on `main`; this item adds 68.
- `lint-clean` → **pass**: `python3 -m compileall -q envel tests` → exit 0.
- `workspace-valid` → **pass**: `scripts/validate-workspace` → exit 0.
- `every-criterion-has-a-test` → **pass**: the table above names a test function for every one of
  AC1 to AC20. Six mutations were applied and reverted to check the tests would fail if the
  behaviour were removed — storing an empty description rather than deleting the key, checking the
  invariant against the live store rather than the candidate, lowering `next-ref` on a removal,
  dropping the sign of a corrected amount, allowing a move to be corrected, and allowing `--on` on
  an income — failing 3, 7, 1, 11, 5 and 7 tests respectively. Every mutation was caught.
- `commits-reference-the-item` → **pass**: `scripts/check-commit-refs WI-0005 wi/WI-0005` → exit 0.
- `no-unplanned-scope` → **pass** (advisory): `git diff --stat main..HEAD` touches
  `envel/cli.py`, `envel/envelopes.py`, `tests/test_cli.py`, `tests/test_corrections.py`,
  `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` and this item's own tracker files.
  Every hunk traces to a plan step: steps 1–5 to `envelopes.py`, 6–8 to `cli.py`, 9–10 to the two
  test modules, 11 to `ADR-0002`. Nothing unrelated was fixed or tidied.
- `cross-answer-consistency` → **pass**: `scripts/lint-answers --changed-since main` → exit 0.
- `claims-are-sourced` → **pass**: `scripts/lint-claims --changed-since main --plan-documents
  WI-0005` → exit 0, over a window the run printed as *"12 document(s) in 12 path(s) in scope — 1
  path(s) differ from main under docs, plus 12 document(s) named by WI-0005's plan"*. The window is
  not empty and it contains the document this execution wrote.
- `document-writes-are-declared` → **pass**: `scripts/lint-documents --rule
  document-writes-are-declared --item WI-0005 --changed-since main` → exit 0, reporting *"1
  document(s) written under docs/ on this branch; 12 named by the plan"*.

## What I did not do

- **I did not tick any acceptance criterion.** The boxes in `item.md` are `verify`'s.
- **I did not file a bug item, and nothing called for one.** The one thing a reader might expect
  one for — `envel entries <envelope>` printing a negative opening figure when income is undated —
  was recorded by `refine` in the item's `## Notes` with the measurement, is a consequence of two
  decisions the stakeholder has already taken and been told the cost of, and is not a defect in
  delivered behaviour.
- **I did not repair a claim sourced to one of the stakeholder's answers.** The two `vision.md`
  paragraphs about correcting are theirs, and they are now true rather than overtaken, so they were
  read and left exactly as they are.
- **I did not touch either `## Engagement state` section**, at any disposition. Both are false
  today and both are `review-close`'s at the ending.
- **I did not add a repair for a hand-damaged `next-ref`.** `ADR-0010` left that to whoever meets
  one, and nothing here meets one.
- **I left three combinations deliberately unconstrained**, as `refine` recorded them in the item's
  R10 table: a correction that changes nothing, `--envelope` naming the envelope the entry is
  already in, and `--on` setting a date before the envelope existed. All three succeed and print;
  none has a test, because none has a criterion.
