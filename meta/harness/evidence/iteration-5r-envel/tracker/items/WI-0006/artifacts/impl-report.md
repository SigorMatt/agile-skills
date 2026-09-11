# Implementation report — WI-0006

## What was built

One command, `envel entries`, and the thing it prints beside each line.

**A reference on every entry.** `store.FORMAT` is `2`; `store.load` reads `1` and `2` and returns
a format-1 document upgraded — each entry taking a reference in the order the list already holds
them, `next-ref` set one past the last — **in memory only**, so a listing never rewrites a file it
was asked to read. `envelopes.take_ref` is the only source of a new reference and is called at each
of the four places an entry is appended; a move takes two consecutive numbers, the side the money
left first. This is `ADR-0010` built as written.

**The listing, in `envel/summary.py` beside the summary**, as `ADR-0009` implies and the plan
decided from the documents. `list_entries(store, name, month)` returns `Ok` or `Refusal`; with an
envelope named it brackets the entries with what that envelope held at the start of the month and
holds at the end of it, both `summary.bounded_balance` at two bounds, so AC9 reconciles by
arithmetic rather than by anything the listing arranges. With no envelope named it prints the
entry lines alone.

**One subparser and one branch in `envel/cli.py`.** `--month` is parsed by `dates.parse_month`,
which is where an unreadable month is refused, exactly as for `envel summary`.

`envel summary` is not touched. AC14 is the criterion that makes that observable and it was read
as well as run — see `## AC14, read` below.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cli.build_parser` gains an `entries` subparser with an optional positional `name` and `--month`; `main` dispatches to `summary.list_entries` | `tests/test_cli.py` `Entries.test_bare_entries_lists_this_month_across_the_envelopes`, `test_entries_with_an_envelope_lists_that_envelope_this_month`, `test_a_month_can_be_named_with_and_without_an_envelope` (all four forms, exit 0), `test_the_tools_own_usage_names_the_new_subcommand` |
| AC2 | `summary.entry_line` renders ref, date, kind, envelope, amount, and a description where the entry has one | `tests/test_entries.py` `Line.test_every_line_carries_reference_date_kind_envelope_and_amount`, `test_a_description_is_on_the_line_that_has_one_and_not_on_the_others`, `test_no_amount_carries_a_currency_symbol_or_a_separator` |
| AC3 | `envelopes.take_ref` reads one counter in the document; nothing is per-envelope | `tests/test_envelopes.py` `References.test_the_counter_does_not_restart_at_the_second_envelope`, `test_four_entries_over_one_document_take_consecutive_numbers`; `tests/test_entries.py` `Line.test_no_two_lines_of_one_listing_carry_the_same_reference` |
| AC4 | `ref` is written once when the entry is appended and never recomputed; the format-1 upgrade is a function of the entry list alone | `tests/test_envelopes.py` `References.test_recording_more_does_not_move_an_earlier_number`; `tests/test_entries.py` `ReferencesStay.test_a_reference_read_before_still_names_the_same_entry_after`; `tests/test_store.py` `FormatOneIsUpgradedOnRead.test_reading_it_twice_gives_the_same_references`, `test_entries_take_references_in_the_order_the_list_holds_them` |
| AC5 | `summary.entry_date` is `on` where present and `at` otherwise, through `dates.day_of` | `tests/test_entries.py` `TheDateOnALine.test_income_falls_under_the_day_it_was_typed_and_a_spend_under_its_own` |
| AC6 | `summary.entry_kind` reads the direction off the sign of `cents` | `tests/test_entries.py` `AMove.test_the_source_sees_one_line_going_out`, `test_the_destination_sees_one_line_coming_in`, `test_with_no_envelope_named_both_appear_with_the_same_date_and_opposite_signs` |
| AC7 | `summary.entries_in` filters by `entry_month`, which is `entry_date`'s month | `tests/test_entries.py` `OneMonthOnly.test_a_past_month_reads_the_same_after_a_later_entry_is_recorded`, `test_an_entry_appears_in_its_own_month_and_no_other` |
| AC8 | `sorted(chosen, key=entry_date)` — stable, so the tie-break is the storage order | `tests/test_entries.py` `TheOrder.test_lines_are_oldest_first_with_ties_in_recording_order`, `test_two_calls_over_one_document_give_the_same_lines` |
| AC9 | `summary.balance_before` and `balance_through`, the same filtered sum at two bounds | `tests/test_entries.py` `ItAddsUp.test_the_opening_line_is_what_was_carried_in`, `test_the_closing_line_is_what_it_holds_at_the_end`, `test_the_opening_plus_the_lines_between_equals_the_closing` (opening 5000, between +1000, closing 6000), `test_for_the_current_month_the_closing_figure_is_what_list_shows` |
| AC10 | with `name` None, `list_entries` returns the entry lines alone | `tests/test_entries.py` `WithNoEnvelopeNamed.test_every_line_is_an_entry_line`, `test_each_line_names_the_envelope_it_belongs_to`, `test_it_covers_the_envelopes_together` |
| AC11 | the empty cases return `Ok` with a line saying so; with an envelope the brackets are still printed | `tests/test_entries.py` `NothingToShow` (three tests); `tests/test_cli.py` `Entries.test_a_month_with_nothing_in_it_says_so_on_stdout_and_exits_zero`, `test_an_envelope_with_nothing_in_the_month_still_shows_its_balance`, `test_a_store_that_has_never_been_written_lists_rather_than_failing` |
| AC12 | `list_entries` refuses a name `envelopes.find` does not resolve, quoting what was typed | `tests/test_cli.py` `Entries.test_an_envelope_that_does_not_exist_is_refused_by_name`, `test_an_envelope_named_in_another_capitalisation_is_the_same_envelope`; `tests/test_entries.py` `AnEnvelopeThatDoesNotExist` (four tests, including that the month is refused before the envelope) |
| AC13 | a month later than `dates.this_month()` is refused in `list_entries`; an unreadable one is refused by `dates.parse_month` in `cli` | `tests/test_cli.py` `Entries.test_the_five_months_ac13_names_are_each_refused` (the next month, `2026-8`, `august`, `2026-13`, `2026-08-01`), `test_the_month_today_falls_in_is_not_refused` |
| AC14 | nothing in `summary.summarise`, `figures` or `row` was changed; `entry_month` was re-expressed through `entry_date` and returns the same value for every entry | `tests/test_cli.py` `Entries.test_one_store_listed_and_then_summarised_gives_both_answers` (summary output asserted line for line against what `Summary.test_a_month_named_as_a_plain_word_is_summarised` says it printed before this item), `test_the_summary_lists_no_individual_entry_and_has_no_running_balance`, `test_listing_writes_nothing_to_the_store`; plus `## AC14, read` below and `tests/test_summary.py` passing unchanged |
| AC15 | every refusal returns a `Refusal`, which `cli` prints to stderr with exit 1; every success returns `Ok`, printed to stdout with exit 0; a wrong shape is the subcommand parser's | `tests/test_cli.py` `Entries.test_every_answer_goes_to_the_stream_ac15_promises` (four refusals, five successes, one invocation each), `test_the_three_wrong_shapes_print_this_subcommands_usage` |

`python3 -m unittest discover -s tests -t .` → exit 0, **231 tests** (176 before this item, 55
added).

### The tests were checked against removal

Self-check 1 asks whether a test would fail if the behaviour were removed. Four mutations were
applied to the branch and reverted, each run against `tests/test_entries.py`,
`tests/test_envelopes.py` and `tests/test_cli.py::Entries`:

| mutation | result |
|----------|--------|
| `entry_kind` returns `"moved"` for both halves of a move | 5 failures |
| `balance_before` bounded with `<=` instead of `<` | 4 failures |
| `"ref": take_ref(store)` removed from every entry | 5 errors |
| `entries_in` returns the entries unsorted | 1 failure |

## Documents

Six documents were written, all of them named by the plan's invalidation set. Nothing was written
that the set does not name, and no `## Engagement state` section was touched. The twenty-nine
rows of the set are disposed in `plan.md`; the repairs and the enumerations are below.

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/architecture/overview.md` | `## The parts`: the `envel/summary.py` row | cited-fact | Reopened `overview.md:31` against the module. `plan` widened it to *"the reports, both of them"* at v7 and the code now matches: `summary.py` holds `summarise` and `list_entries` and nothing else that reports. Still true | — |
| `docs/architecture/overview.md` | `## The parts`: the dependency direction | quantified | Set: every module under `envel/`. Enumerated with `grep -n '^import \|^from ' envel/*.py` → `cli`: dates, envelopes, money, store, summary (five); `summary`: dates, envelopes, money; `envelopes`: dates, money; `store`: json, os, pathlib; `money`: re; `dates`: datetime, re; `__main__`: sys, envel.cli. Verdict per member: no import was added by this change, and `envelopes` still does not import `summary`. Still true | — |
| `docs/architecture/overview.md` | `## The shape of it`: nothing below `cli` prints or exits | quantified | Set: every module under `envel/`. `grep -n 'print(\|sys\.exit' envel/*.py` → one hit outside `envel/cli.py`: `envel/__main__.py:8`, the entry point **above** `cli`, unchanged by this item. `store.upgraded`, `summary.entry_line`, `entries_in`, `bounded_balance` and `list_entries` return values. Still true | — |
| `docs/architecture/overview.md` | `## The shape of it`: the three beats | quantified | Set: every write of the store. `grep -rn 'save(' envel/` → `store.save` defined once, called once, at `envel/cli.py` under `if result.changed`. `list_entries` returns `Ok` with `changed` false; `store.upgraded` names no path. Demonstrated by `test_the_file_on_disk_is_not_touched` and `test_listing_writes_nothing_to_the_store`. Still true | — |
| `docs/architecture/overview.md` | `## The data`: one JSON document, derived balance | cited-fact | All three assertions hold. The part it stopped describing — `ref`, `next-ref` — `plan` added as its own paragraph at v7; reopened and it agrees with `envel/store.py` and `envel/envelopes.py`. Still true | — |
| `docs/architecture/overview.md` | `## The data`: `at` on every kind, *"one field more"* | quantified | Set: the three entry kinds. Enumerated from the code that writes them — income `kind, envelope, cents, at, ref`; spend the same plus `on` and optionally `description`; move the same plus `on`. Verdict: `ref` is on every kind, so the differential the sentence counts, which it names as `on` in the same breath, is untouched. (A spend's optional `description` predates this item; the sentence is about the date.) Still true | — |
| `docs/architecture/overview.md` | `## The data`: *"Nothing in the file links the two halves of a move"* | quantified | **False.** A move now takes two consecutive references, and this document said so four lines later. Repaired: no **field** names the pair, the adjacency is the nearest thing to a link, and no code reads it as one | **8** |
| `docs/architecture/overview.md` | `## Conventions`: dates and months parsed in `envel/dates.py` alone | quantified | Set: every parse of a date or a month. `grep -rn 'parse_date\|parse_month\|fromisoformat' envel/*.py` → `envel/cli.py` calls `dates.parse_date` twice and `dates.parse_month` twice; the regexes and `fromisoformat` are in `envel/dates.py` alone. `--month` is one of those `parse_month` calls. `dates.day_of` was added beside `dates.month_of`, which keeps the rule rather than breaking it. Still true | — |
| `docs/architecture/overview.md` | `## Conventions`: two decimal places, no symbol | quantified | Set: every amount this change prints. `grep -rn 'format_amount\|parse_amount\|// 100\|\* 100' envel/*.py` → in `summary.py` the new code has exactly three: `entry_line` once and `list_entries` twice for the bracket figures, all `money.format_amount`. No arithmetic conversion outside `envel/money.py`. Asserted from the outside by `test_no_amount_carries_a_currency_symbol_or_a_separator`. Still true | — |
| `docs/architecture/overview.md` | `## Conventions`: stdout/0, stderr/non-zero | quantified | Set: the two success paths and three refusals this change adds. Each is one invocation in `test_every_answer_goes_to_the_stream_ac15_promises` — four refusals with empty stdout and non-zero exit, five successes with empty stderr and exit 0. Still true | — |
| `docs/architecture/overview.md` | `## What is not decided yet` | cited-fact | Reopened. `plan` rewrote it at v7: `WI-0006` has left the list and the `ADR-0002` prediction is replaced by what `ADR-0010` does to it. Both match what was built. Still true | — |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Not read for repair and not touched. `review-close` owns it | — |
| `docs/architecture/adr/ADR-0002-…` | `## Decision`: the worked document and the `format` bullet | cited-fact | The bullet itself is **true** — `store.load` still checks `format` and this change is the branch it anticipated. What was missing is where the branch went. Repaired as a `provenance` correction: the bullet now cites `ADR-0010` and says the worked document above it is this ADR's shape and not the current one. The worked document is left exactly as it was, because it is the record of what was decided | **3** |
| `docs/architecture/adr/ADR-0002-…` | `## Corrections`: the `WI-0002` entry's *"still reads and writes `FORMAT = 1`"* | cited-fact | **Found mid-change and added to the set before being disposed.** Not repaired, and not repairable: `## Corrections` is append-only and an entry is never edited. Read as what it is — a dated record of what a sentence said and why it changed on 2026-09-11T04:06:14Z — rather than as a standing claim about the code. Where the format bump is recorded is the `provenance` entry directly below it | — |
| `docs/architecture/adr/ADR-0002-…` | `## Decision`: append-only, ordered as written, balance as a sum | quantified | Set: everything this change does to the entry list. `entries_in` reads `store['entries']` and returns `sorted(...)`, a new list; nothing sorts, mutates or saves the document — `test_nothing_is_marked_changed_and_the_document_is_the_same` asserts the document is equal and identical afterwards. AC9's two figures are `bounded_balance`, a plain sum of `cents` with a month bound and no branch on `kind`. Still true | — |
| `docs/architecture/adr/ADR-0002-…` | `## Consequences`: *"neither needing a format change"* | cited-fact | Read against this change. The sentence is a claim about `WI-0002` and `WI-0003` and is true of both; it is not a claim about later items. Where the prediction it implies is corrected is the overview's `## What is not decided yet` (v7, `plan`) and this ADR's own `format` bullet (v3, above). Still true | — |
| `docs/architecture/adr/ADR-0009-…` | `## Decision`: *"holds the summary"*; `## Consequences`: *"two places"* | cited-fact | The `## Decision` enumeration stopped being complete when this item put a second report in the module. Repaired as an `erratum`: the module holds this project's reports, with what it held when the ADR was written and what was added. The decision is unchanged and is what this item followed. `## Consequences` is untouched and still true — this change added a report, not a third module | **2** |
| `docs/architecture/adr/ADR-0008-…` | `## Consequences`: *"Nothing computes the carried-in figure"* | quantified | **False.** `summary.balance_before` computes exactly that, because AC9 prints it. The claim worth keeping — that nothing **derives** it from the other three — is true: `balance_before` is this ADR's own `left` filter with `<= M` replaced by `< M`, and `test_the_opening_plus_the_lines_between_equals_the_closing` asserts the identity holds without any code checking it. Repaired as an `erratum` saying *derives* and naming the function | **2** |
| `docs/architecture/adr/ADR-0007-…` | `## Decision` and `## Consequences`: the two-entry shape and what nothing links | quantified | **False in four clauses.** `## Decision` said the halves are *"not linked"* and gave `WI-0006` and `WI-0005` scopes neither item now has; `## Consequences` said *"nothing in the file says so"* and that the other half *"cannot"* be found. Repaired as two `erratum` entries: no **field** names the pair, both items' real scope, and the consecutive references stated with the fact that nothing in the tool pairs by them | **3** |
| `docs/architecture/adr/ADR-0006-…` | `## Decision`: `on` never absent on a spend | quantified | Set: every place a spend entry is created. `grep -n '"kind": "spend"' envel/*.py` → exactly one, `envelopes.record_spend`, which writes `on` unconditionally from the day `cli` resolved; no branch omits it and nothing writes `None`. Verdict: `summary.entry_date` never falls back to `at` for a spend, which `test_income_falls_under_the_day_it_was_typed_and_a_spend_under_its_own` asserts from the outside. Still true | — |
| `docs/architecture/adr/ADR-0003-…` | `## Decision`: one function resolves the path | quantified | Set: everywhere a store path could be known. `grep -rn 'store_path\|ENVEL_FILE\|XDG_DATA_HOME\|pathlib' envel/*.py` → `store_path` defined in `envel/store.py`, called from one place, `envel/cli.py`; the environment variables appear only in `store.py`. `store.upgraded` takes a document, not a path; `summary.py` names no path and imports no path module. Still true | — |
| `docs/architecture/adr/ADR-0001-…` | `## Decision`: two functions are the only meeting place | quantified | The enumeration two rows above is this row's: every cents-to-text conversion in the new code is a `money.format_amount` call, and no digit arithmetic on an amount exists outside `envel/money.py`. Still true | — |
| `docs/architecture/adr/ADR-0004-…` | `## Decision`: both entry points reach the same `main` | quantified | Set: the two entry points. `Entries.test_the_two_entry_points_agree` runs `envel entries --month 2026-08` through `bin/envel` and through `python3 -m envel` over one store and asserts equal stdout and equal exit code. Neither file was edited; the subcommand was added in `cli.main`, which both reach. Still true | — |
| `docs/architecture/adr/ADR-0005-…` | `## Decision`: the two commands, stdlib only | cited-fact | Both commands still cover every file this item touched: `discover -s tests -t .` picks up `tests/test_entries.py` by name, `compileall -q envel tests` by directory. No import outside the standard library was added anywhere — the dependency enumeration above is the evidence; the new test module imports `copy`, `unittest` and `envel`. Still true | — |
| `docs/product/vision.md` | `## What it is for`: the reference is one number, and stays that entry's | quantified | Set: every place a reference is produced. `envelopes.take_ref` is the only one, reading one counter in the document, so numbering does not restart per envelope; nothing rewrites an existing `ref`. Verdict per member: `test_the_counter_does_not_restart_at_the_second_envelope`, `test_recording_more_does_not_move_an_earlier_number`, `test_no_two_lines_of_one_listing_carry_the_same_reference`. Until this item nothing stood behind the sentence; now the code does. Still true | — |
| `docs/product/vision.md` | `## What it is for`: the listing paragraph | cited-fact | Read clause by clause. Income, spends and moves with the kind on the line: AC2, AC6. One month, the current one unless named, spelled as `envel summary` spells one: AC1, AC7, AC13. Envelope optional: AC1, AC10. *"so that the lines add up to the balance"*: true of the form the stakeholder's rule was given about — with an envelope named, opening plus the lines equals closing. The all-envelopes form prints no bracket figures, and that is `refine`'s decision at AC10 under **no** delegation; the sentence does not claim otherwise and was deliberately not edited to make it read as though the stakeholder had settled it. Still true | — |
| `docs/product/vision.md` | `## What it is for`: *"a listing of an envelope's entries"* | cited-fact | Our paraphrase of the example put to the stakeholder at `WI-0005/Q-001`, before they made the envelope optional at `WI-0006/Q-003`. Repaired to name both forms, citing their own later answer. See `## Cross-answer check` below for why this is an ordinary repair and not a decision of theirs | **7** |
| `docs/product/vision.md` | `## What it deliberately is not`: not connected to anything | quantified | Set: every import in `envel/`. The enumeration above is the evidence, and its verdict here is stronger than *still true*: this change added **no** import to any module. The whole of `envel/` is `copy, dataclasses, datetime, json, os, pathlib, re, argparse, sys` and none of them opens a socket. Still true | — |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Not read for repair and not touched. `review-close` owns it | — |

## Cross-answer check

One sentence in `docs/` carrying `[src: <ITEM>/Q-nnn]` for a question the **stakeholder** answered
was edited: `docs/product/vision.md` `## What it is for`, *"An entry is named by a short reference
the tool prints and the person types back, read off a listing of an envelope's entries rather than
remembered"* `[src: WI-0005/Q-001]`.

It is an ordinary repair and not a decision that was theirs, because the two answers coexist:

- `WI-0005/Q-001` settled **that there is a printed reference**, and the example in front of them
  while they answered was `envel spends groceries`. *"of an envelope's entries"* is our paraphrase
  of that example, not a clause they wrote.
- `WI-0006/Q-003` settled **whether an envelope must be named**, and they chose that it need not:
  *"The case I actually have is a 34.99 on the statement I cannot place, and that is precisely the
  moment I cannot name an envelope."*

Neither answer contradicts the other — one is about the reference existing, the other about the
command's arguments — and the vision already carried both, two paragraphs apart. The edit widens
our paraphrase to match their own later answer and cites it. Nothing was reinterpreted and no
clause of `WI-0006/Q-004` about the lines adding up was touched.

`scripts/lint-answers --changed-since main` → exit 0, 33 consumed human answers and 2 delegations
checked, window 6 paths under `docs/`.

## AC14, read

AC14 asks for `WI-0003`'s criteria to be **re-read** against this item's behaviour, not merely for
its tests to pass. Read one at a time against `envel summary` as it now stands:

| WI-0003 AC | what it says | verdict against `envel entries` |
|---|---|---|
| AC1 | the command is `envel summary`, printing a calendar month | untouched — a new subparser is a sibling, not a change |
| AC2 | four labelled figures per row, moved as one net number | untouched — `summary.figures` and `summary.row` are unedited |
| AC3 | the figures reconcile | untouched; and the two reports agree about the figure they share, asserted in `test_one_store_listed_and_then_summarised_gives_both_answers` |
| AC4 | the row names the envelope | untouched |
| AC5 | a month is `YYYY-MM` | reinforced — `envel entries --month` uses the same `dates.parse_month` |
| AC6 | no total line and no individual spends | held, and now observable: `test_the_summary_lists_no_individual_entry_and_has_no_running_balance` asserts every summary line matches the four-figure row shape |
| AC7 | a past month reads the same afterwards | untouched — `summarise` mentions no entry this change adds |
| AC8 | income by `at`, a spend by `on` | `entry_month` now reads `entry_date`, which is the same expression with `dates.day_of` in front of `dates.month_of`. Both are prefixes of the same fixed-width string, so the value is identical for every entry; `tests/test_summary.py` passes unchanged |
| AC9 | a month later than this one is refused | untouched; `envel entries` refuses the same case separately |
| AC10 | rows ordered by name, case-insensitively | untouched |
| AC11 | a month with no envelopes says so | untouched |
| AC12 | an unreadable month is refused | untouched; `envel entries` refuses the same spellings |
| AC13 | streams and exit codes | untouched |
| AC14 | the summary writes nothing to the store | untouched, and `test_listing_writes_nothing_to_the_store` asserts the same of the listing, including over a format-1 file that the upgrade rewrote in memory |

The plan asked for a case exercising both commands over one store where none intersected. There
was none, and `Entries.test_one_store_listed_and_then_summarised_gives_both_answers` is it: one
format-1 store, listed and then summarised, with the summary's two lines asserted character for
character against what `Summary.test_a_month_named_as_a_plain_word_is_summarised` says it printed
before this item.

## Deviations from the plan

1. **`envel/dates.py` was edited, and the plan named four modules.** The listing needs the
   calendar **day** an entry counts under, and `ADR-0006` makes `dates.py` the only place text and
   calendar days meet. Writing `entry["at"][:10]` in `summary.py` would have put a date conversion
   in a second module. `dates.day_of` and `DAY_LENGTH` were added beside `month_of` and
   `MONTH_LENGTH`, which is the same shape for the same reason. This changes *how*, not *what*.
2. **`summary.entry_month` was re-expressed** as `dates.month_of(entry_date(entry))` rather than
   left as a second copy of AC5's rule. The value is identical for every entry — both are prefixes
   of the same fixed-width ISO string — and `tests/test_summary.py` passes unchanged. The reason is
   the invalidation set's `ADR-0006` row: one rule in one place cannot drift.
3. **The two halves of plan step 3's bracket function are two functions**, `balance_before` and
   `balance_through`, over one `bounded_balance`. The plan asked for the *before* case only, and
   the *through* case is `figures`' `left` needed on its own; writing it out beside its twin is
   clearer than calling `figures` and discarding three sums.
4. **One commit carries plan steps 1 to 4 rather than one commit per step.** Nothing lists a
   reference until the store holds one, so the intermediate states do not build a working tool.
   The commit message names all four steps.
5. **One row was added to the invalidation set** — `ADR-0002`'s `## Corrections` entry — and
   disposed rather than repaired, because that section is append-only.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, 231 tests |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `scripts/validate-workspace` → exit 0 |
| `every-criterion-has-a-test` | pass | the table above names a test function or an exact command for each of AC1–AC15; four mutations were applied and each was caught |
| `commits-reference-the-item` | pass | `scripts/check-commit-refs WI-0006 wi/WI-0006` → exit 0, all 2 commits on `main..wi/WI-0006` name WI-0006 |
| `no-unplanned-scope` (advisory) | pass | every hunk traces to a plan step or an AC; the five deviations above are the only places the diff is not literally the plan |
| `cross-answer-consistency` | pass | `scripts/lint-answers --changed-since main` → exit 0; the one edited answer-sourced sentence is accounted for under `## Cross-answer check` |
| `claims-are-sourced` | pass | `scripts/lint-claims --changed-since main --plan-documents WI-0006` → exit 0; scope: 11 documents in 11 paths — 6 differing from `main` under `docs/` plus 11 named by the plan |
| `document-writes-are-declared` | pass | `scripts/lint-documents --rule document-writes-are-declared --item WI-0006 --changed-since main` → exit 0; 6 documents written, 11 named by the plan, 29 rows all disposed |

### `workspace-valid` was forced at the transition, and re-run after it

`scripts/transition` runs the gates **before** it appends the journal entry, and
`doc.changelog.no-execution` asks whether an execution of the named skill was running when a
document version row claims it was — answered from that same journal. The six documents this
execution repaired carry rows stamped `08:22:40Z`/`08:22:41Z`, and the entry that puts those
inside this execution's window is the one the transition had not written yet. The gate therefore
reported seven errors, all of that one code, and could not have reported otherwise. `plan` hit the
same ordering on this item and recorded the same thing in its history row.

The move was taken with `--force`, which skips **every** gate, so the `**Gates:**` bullet in the
journal is the one written by hand and the program vouched for none of it. All nine were therefore
re-run on the branch head immediately after the transition, and this is what they said:

| gate | after the transition |
|------|----------------------|
| `tests-pass` | exit 0, 231 tests |
| `lint-clean` | exit 0 |
| `workspace-valid` | **exit 0, 0 errors, 0 warnings** — the journal entry resolved all seven |
| `commits-reference-the-item` | exit 0, all 3 commits on `main..wi/WI-0006` name WI-0006 |
| `cross-answer-consistency` | exit 0 |
| `claims-are-sourced` | exit 0 |
| `document-writes-are-declared` | exit 0 |

`every-criterion-has-a-test` and `no-unplanned-scope` are judged rather than run, and their
evidence is the two tables above.

## What I did not do

- **`envel fix` and `envel remove`.** They are `WI-0005`, which depends on this item. This branch
  implements no correction and no removal; it stores the reference they will be aimed with.
- **Nothing about a hand-damaged `next-ref`.** `ADR-0010` records that a file edited to carry a
  `next-ref` below an existing `ref` would produce a duplicate reference and that no repair is
  being built. No criterion asks for one. If it ever matters it is a bug item.
- **No repair of `ADR-0002`'s worked JSON document**, which still shows `"format": 1` and an entry
  with no `ref`. It is the record of what was decided there, and the `provenance` correction says
  so in the document rather than leaving a reader to notice.
- **No repair of the `ADR-0002` correction entry that says `envel/store.py` still reads and writes
  `FORMAT = 1`.** `## Corrections` is append-only by `spec/doc-header.md` §4b and an entry is never
  edited. It is a dated record, and it is in the invalidation set with that reading written down.
- **No decision about AC10's missing bracket figures.** `refine` took it under no delegation and
  recorded that a disagreement costs one criterion and one test. Building it was the right move and
  the vision was deliberately not edited to make it read as the stakeholder's.
- **No `## Engagement state` section was written**, in either document that has one.

---

# Round 2 — the send-back from `review-close` (F1)

`review-close` rejected this item back to `in-progress` on one finding and merged nothing. Everything
above is the round-1 report and still stands; this section is the round-2 execution, and it is the
whole of it.

## What was built

Nothing. One docstring was corrected.

`envel/summary.py`, `entry_kind`, said of a move's two entries:

> A move is stored as two entries with opposite `cents` and nothing linking them
> (ADR-0007), so which side of one this is is read off the sign and from nowhere
> else …

That sentence is the one this same item struck from `ADR-0007` as an erratum an hour earlier —
`ADR-0007` `## Corrections` records *"`## Decision` … said the two entries are `not linked to each
other` … All three are false"* — because `ADR-0010`, which this item wrote, gives a move's two
halves consecutive references. The docstring shipped the struck claim and cited the amended ADR as
its authority.

It now says what `ADR-0007` `## Decision` and `docs/architecture/overview.md` `## The data` say:

> A move is stored as two entries with opposite `cents` (ADR-0007). No field names the
> pair; since ADR-0010 the two halves do take consecutive references, and no code reads
> that adjacency as a link. Which side of a move this is comes off the sign because the
> sign is all this function needs — the same thing that makes a balance a plain sum
> with no branch on the kind — and not because the other half could not be found.

Commit `fb9d14a`, one file, one hunk, five lines of comment. No behaviour, no test, no document.

**The three claims in the new sentence, each against what it restates.**

| claim | where it comes from | checked |
|-------|--------------------|---------|
| *No field names the pair* | `ADR-0007` `## Decision`: *"**No field links the two entries to each other**"*; `overview.md` `## The data`: *"No field in the file names the pair"* | a store written by the tool at this branch head — `envel new groceries; envel new fun; envel add groceries 100; envel spend groceries 10; envel spend groceries 5; envel move groceries fun 20` — whose two `move` entries carry exactly `kind`, `envelope`, `cents`, `on`, `at`, `ref` and no pairing field: `{"kind": "move", "envelope": "groceries", "cents": -2000, "on": "2026-09-11", "at": "…", "ref": 4}` and the same with `"envelope": "fun"`, `"cents": 2000`, `"ref": 5` |
| *since ADR-0010 the two halves do take consecutive references* | `ADR-0007` `## Decision`: *"Since `ADR-0010` … the two halves do carry **consecutive references**"*; `overview.md`: *"A move takes two consecutive references, one for each of its two entries"* | `envel/envelopes.py` `move` calls `take_ref` twice in succession; the store below took `ref` **4** and **5** for the two halves, with `next-ref` at 6 |
| *no code reads that adjacency as a link* | `ADR-0007`: *"no code pairs them by it [src: envel/summary.py]"*; `overview.md`: *"No code reads that adjacency as a link"* | `grep -rn "ref" envel/ \| grep -E "ref *[-+] *1"` → exit 1, no output; `entry_kind` branches on the sign of `cents` and on nothing else |

## Acceptance criteria evidence

Unchanged, and unchanged for a reason that is checkable rather than asserted: this round's diff
contains no executable line.

```
$ git diff 80040a7..fb9d14a --stat -- envel/summary.py
 envel/summary.py | 8 +++++---
 1 file changed, 5 insertions(+), 3 deletions(-)

$ git diff 80040a7..fb9d14a --stat
 envel/summary.py | 8 +++++---        <- the only file outside tracker/
 (the other five paths are tracker/board.md and WI-0006's review.md,
  history.md, item.md and journal.md, all written by review-close)

$ python3 -m unittest discover -s tests -t .
Ran 231 tests in 26.5s — OK
```

The eight changed lines are the three removed and five added lines of the `entry_kind` docstring,
which the two quotations above reproduce in full. The `"""` opening line, the `if` below it and
the `return`s are untouched.

The AC table above is therefore the evidence for AC1–AC15 in this round too: the same 231 tests, the
same commands, the same outputs. `every-criterion-has-a-test` is judged on that table.

## Documents

None. This round wrote nothing under `docs/`, so no entry of the plan's invalidation set changed and
none was added. All 29 rows were disposed in round 1 and are unchanged.

That is the correct disposition and not an oversight: the two documents this docstring restates —
`ADR-0007` and `overview.md` — were **already** repaired by round 1 and are already `to-update` rows
in the set. The defect was that the source did not follow them. No `## Engagement state` section was
written.

## Cross-answer check

`none`. This round edited no sentence under `docs/`, and so no claim sourced to one of the
stakeholder's answers. `lint-answers --changed-since main` → exit 0, and its window is unchanged
from round 1 at six paths.

## Deviations from the plan

None. This round executed a send-back, not a plan step. The fix is exactly the one
`artifacts/review.md` F1 names under *"What would fix it"* — *"One docstring … No behaviour changes
and no test changes"* — and nothing else was touched.

## Gates

All nine on the branch head `fb9d14a`, after the last change. **None was forced**, because this round
wrote no document and so created no version row for `doc.changelog.no-execution` to fire on.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 231 tests … OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | **pass** | `checked 7 item(s), 12 document(s); 0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | round 1's `## Acceptance criteria evidence` table, still current: this round's diff has no executable line and the same 231 tests pass |
| `commits-reference-the-item` | **pass** | `check-commit-refs WI-0006 wi/WI-0006` → *"all 7 commit(s) on main..wi/WI-0006 name WI-0006"* |
| `no-unplanned-scope` (advisory) | **pass** | one hunk, traced to `artifacts/review.md` F1 — the send-back reason in the `in-review → in-progress` history row |
| `cross-answer-consistency` | **pass** | `lint-answers --changed-since main` → exit 0; *"checked 33 consumed human answer(s) and 2 delegation(s)"* |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main --plan-documents WI-0006` → exit 0. **Scope, from its own output:** *"11 document(s) in 11 path(s) in scope — 6 path(s) differ from main (52a6237) under docs, plus 11 document(s) named by WI-0006's plan; citations: every markdown file in the workspace"* |
| `document-writes-are-declared` | **pass** | `lint-documents --rule document-writes-are-declared --item WI-0006 --changed-since main` → exit 0; *"6 document(s) written under docs/ on this branch; 11 named by the plan"* |

## What I did not do

- **I did not widen the fix to the rest of the file.** Before the change,
  `grep -rn "nothing linking\|not linked\|linking them\|no link" envel/ tests/` returned exactly one
  line — `envel/summary.py:123`, the one F1 names; after it, the same grep exits 1 with no output. So
  there was nothing else of this shape to find. I did not go looking for unrelated stale comments —
  that is F2's subject, not this send-back's.
- **I did not act on F2, F3, F4 or F5 in `review.md`.** All four are recorded there as observations
  with no action, and F2 is explicitly *"Recorded here for the retrospective"*.
- **I did not re-run round 1's mutation checks.** They are evidence about behaviour and no behaviour
  changed; `git diff 80040a7..fb9d14a` shows one comment hunk.
