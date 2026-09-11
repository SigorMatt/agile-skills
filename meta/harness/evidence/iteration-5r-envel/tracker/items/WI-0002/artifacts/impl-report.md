# Implementation report — WI-0002

> **Second execution, 2026-09-11.** `review-close` rejected this item and sent it back with one
> finding: `docs/architecture/overview.md` said `envelopes` knows about `store`, and it does not
> (`artifacts/review.md`, finding 1). The repair is one paragraph in one document and **no code
> change at all** — the build below is unchanged and still green at 90 tests. What this execution
> altered in this report is the `## Documents` row for that entry, which now carries the
> `to-update` audit it should have carried the first time; the wrong verdict is quoted inside it
> rather than deleted, because the mistake is the useful part. See
> `## The send-back, and what it changed` at the foot.

## What was built

`envel spend <envelope> <amount> [description] [--on YYYY-MM-DD]`, the fourth subcommand, plus
the two things underneath it that the plan's seven steps called for.

- **`envel/dates.py`** — new. `parse_date`, `format_date`, `today`, and `DateError`. It stands to
  calendar dates exactly as `envel/money.py` stands to amounts: the only place the text a person
  types and the value the tool holds meet, raising an error carrying the message the user is
  shown, and printing nothing. The full `YYYY-MM-DD` form is checked with a regex **before**
  `datetime.date.fromisoformat` reads it, because `fromisoformat` also accepts `20260907` and
  AC11 says the full form and nothing else.
- **`envelopes.record_spend(store, name, cents, on, description)`** — new. It appends one entry
  whose `cents` is negative, so a balance stays the plain sum of an envelope's entries
  [src: ADR-0002], carrying `on` — always — and `description` only when one was typed
  [src: ADR-0006]. Four refusals, checked in the plan's order: the envelope does not exist, the
  amount is not positive, the date is later than today, the envelope does not hold enough.
- **`envel/cli.py`** — the `spend` subparser, its dispatch, and `dates.DateError` joining
  `money.AmountError` and `store.StoreError` in the one `except` clause, so an unreadable date
  reaches the user by the same route as an unreadable amount.

The store's `format` is unchanged at `1` [src: envel/store.py:11], and nothing in `WI-0001`'s
delivered behaviour was altered.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `spend` subparser with `name` then `amount`, dispatching to `record_spend` | `tests/test_cli.py::Spend::test_spend_records_against_the_named_envelope` — `spend groceries 12.50` exits 0 with empty stderr and the listing then reads `27.50` |
| AC2 | the entry's negative `cents` reaches only the named envelope's balance | `tests/test_cli.py::Spend::test_only_that_envelope_moves` — the `car` line is byte-identical before and after; `tests/test_envelopes.py::RecordSpend::test_only_the_named_envelope_changes` |
| AC3 | `record_spend`'s first check, message naming the envelope | `tests/test_cli.py::Spend::test_an_envelope_that_does_not_exist` — stderr contains `nosuch`, exit non-zero, the store file holds no spend entry; `tests/test_envelopes.py::RecordSpend::test_an_envelope_that_does_not_exist_is_refused_by_name` asserts the store it was given is unchanged |
| AC4 | the store is written by `save` and re-read by `load` each run | `tests/test_cli.py::Spend::test_a_spend_survives_into_a_later_invocation` — four separate subprocesses sharing one `ENVEL_FILE`, the fourth showing `27.50` |
| AC5 | `record_spend`'s fourth check, comparing against `balance` | `tests/test_cli.py::Spend::test_more_than_the_envelope_holds` — stderr contains `groceries` and `10.00`, exit non-zero, no spend entry written, and the listing contains no `-` at all; `tests/test_envelopes.py::RecordSpend::test_spending_exactly_what_is_left_is_allowed` fixes the boundary, since AC5 refuses only *larger than* |
| AC6 | `record_spend`'s second check | `tests/test_cli.py::Spend::test_zero_and_negative_amounts` — `spend groceries 0` and `spend groceries -5` both exit non-zero and the listing still reads `40.00` after each |
| AC7 | the `Ok` line naming the amount, the envelope and the new balance | `tests/test_cli.py::Spend::test_recording_prints_what_is_left` — `27.50` is in stdout with no `list` run |
| AC8 | `--on` defaults to `dates.today()` | `tests/test_cli.py::Spend::test_no_date_given_records_today_and_a_date_given_is_kept` — the store file is read with `json.load`; the two spend entries carry `datetime.date.today().isoformat()` and `2020-01-01` |
| AC9 | the `on` field holds the parsed date, not the moment of writing | `tests/test_cli.py::Spend::test_a_dated_spend_is_held_against_that_date` — the criterion's own invocation, `--on 2026-08-28`, gives `on == "2026-08-28"` while `at` begins with today; `tests/test_envelopes.py::RecordSpend::test_the_entry_carries_the_day_the_money_was_spent` |
| AC10 | `description` is a bare optional positional; the field is written only when non-blank | `tests/test_cli.py::Spend::test_a_description_is_optional_and_combines_with_a_date` — all four shapes of the line exit 0, and in the store file entry 1 has `description: lunch`, entries 2 and 3 have no `description` key, and entry 4 carries both `description` and `on`; `tests/test_cli.py::Spend::test_a_description_of_several_words_is_kept_as_typed` |
| AC11 | the regex in `dates.parse_date`, ahead of `fromisoformat` | `tests/test_dates.py::ParseDate` (four cases, naming `7/9`, `09-07`, `yesterday`, `2026-9-7`, `20260907`, `2026/09/07`, `07-09-2026`, `""`, `2026-13-45`, `2026-02-30`, `2026-00-10`); `tests/test_cli.py::Spend::test_only_the_full_form_of_a_date_is_accepted` — `2026-09-07` exits 0 and each bad form exits non-zero with empty stdout and an unchanged listing |
| AC12 | `record_spend`'s third check, `on > dates.today()` | `tests/test_cli.py::Spend::test_a_date_in_the_future_is_refused_and_today_is_not` — tomorrow computed from `datetime.date.today()` exits non-zero with `future` in stderr and the listing unchanged, and today exits 0; `tests/test_envelopes.py::RecordSpend::test_a_date_later_than_today_is_refused_and_today_is_not` also fixes yesterday as accepted |
| AC13 | `envel/cli.py` is the only place that prints or picks an exit code | `tests/test_cli.py::Spend::test_every_refusal_goes_to_stderr_and_every_success_to_stdout` — a table-driven test keyed by criterion ID: refusals AC3, AC5, AC6, AC11, AC12, AC14 assert stdout empty, stderr non-empty and exit non-zero; successes AC1, AC7, AC8, AC9, AC10 assert stdout non-empty, stderr empty and exit 0 |
| AC14 | the `spend` parser is returned in the subcommand-parser map, so it reports the wrong argument count | `tests/test_cli.py::Spend::test_the_wrong_number_of_words` — `spend`, `spend groceries` and `spend groceries 12.50 lunch extra` each exit non-zero with `spend` in stderr, stdout empty, and no spend entry written |

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/architecture/overview.md` | `## The parts`, the row `envel/dates.py` | cited-fact | The file exists and owns exactly what the row says — parse, format, and what today is [src: envel/dates.py]. `verified-still-true`. | 3, unchanged |
| `docs/architecture/overview.md` | `## The parts`, the dependency-direction paragraph | quantified | **Was `verified-still-true`; it was wrong, and it is now `to-update` and repaired.** The first execution wrote: *"`envel/envelopes.py` carries `from . import dates, money`, which is the first half. `verified-still-true`."* It quoted two modules and certified a claim about three. The sentence said *"`envelopes` knows about `store`, `money` and `dates`"*, and `envelopes` does not import `store` at all — `grep -n "store\." envel/envelopes.py` → one hit, the word in the docstring; `grep -rn "store\.load\|store\.save\|store\.store_path" envel/*.py` → `envel/cli.py:68`, `:70`, `:96`. **Repaired** against the code, and the enumeration the quantified half owes is now run over the right set. *Set:* the modules below `cli` — `store`, `money`, `dates`. *Enumerated by:* `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines. *Members and verdicts:* `envel/store.py` → `json`, `os`, `pathlib`, no `from .` line, knows nothing above it; `envel/money.py` → `re`, same; `envel/dates.py` → `datetime`, `re`, same. *Falsifier:* a `from . import cli` or `from . import envelopes` in any of the three, which that grep prints and did not. The dependency edges the paragraph now states are cited one by one: `envel/cli.py:13` is `from . import dates, envelopes, money, store`, and `envel/envelopes.py:12` is `from . import dates, money`. `to-update`. | **4** |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | Enumerated with `grep -n "print(\|sys.exit" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → **exit 1, no output**. The set is the four modules below `cli`, including the one this change added; verdict for each member: no match. `verified-still-true`. | 3, unchanged |
| `docs/architecture/overview.md` | `## The data`: the negative `cents` and the `on` field | cited-fact | Read against the entry `record_spend` builds [src: envel/envelopes.py:148] — `"cents": -cents` and `"on": dates.format_date(on)`, with `at` still `now()`. `verified-still-true`. | 3, unchanged |
| `docs/architecture/overview.md` | `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | quantified | Enumerated with `grep -n "add_argument" envel/cli.py` → exit 0, six arguments across the four subcommands: `new.name`, `add.name`, `add.amount`, `spend.name`, `spend.amount`, `spend.description`, and the one option `spend.--on`. Verdict per member: `--on` is the only one that takes a date, and it goes through `dates.parse_date`, which accepts the full form alone. `verified-still-true`. | 3, unchanged |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Nothing done. `review-close` restates it at the ending. `owned-by-ending`. | 3, unchanged |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`, the JSON entry and its four bullets | cited-fact | Read field for field against a real run: `ENVEL_FILE=… ./bin/envel spend groceries 12.50 lunch --on 2026-08-28` writes `{"kind": "spend", "envelope": "groceries", "cents": -1250, "on": "2026-08-28", "at": "2026-09-11T04:07:50Z", "description": "lunch"}`. `on` present without `--on` too (AC8's test); `description` absent when not typed. `verified-still-true`. | 1, unchanged |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"The document's `format` stays `1`"* | cited-fact | `grep -n "FORMAT" envel/store.py` → `FORMAT = 1` and three uses, none of them a new value [src: envel/store.py:11]. `verified-still-true`. | 1, unchanged |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`at` is when the tool recorded the entry"* | quantified | Enumerated with `grep -rn '"at":' envel/*.py` → exit 0, two members: `envel/envelopes.py:93` (income) and `envel/envelopes.py:153` (spend). Verdict per member: both write `now()`, the UTC moment of the run; neither writes a user-supplied date into `at`. `verified-still-true`. | 2 |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | `envelopes.balance` is unchanged by this branch — `git diff main -- envel/envelopes.py` shows no `-` line and no added line inside its body, only two new call sites in `record_spend` — and it sums `entry["cents"]` over every entry naming the envelope with no branch on `kind`. The family is entry kinds: `income` and `spend`, verdict for each — summed identically. `verified-still-true`. | 2 |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Consequences`: *"`WI-0002` adds an entry kind and `WI-0003` filters by `at`, neither needing a format change"* | cited-fact | **False, and repaired.** `ADR-0006` gives a spend its own `on` precisely so that `WI-0003` filters a spend by `on` and income by `at`. The sentence now names both fields and cites `ADR-0006`; the surviving half — that neither needs a format change — was checked against `envel/store.py:11`. Version bumped to 2, change-log row added, and an erratum row in `## Corrections`, which is the treatment this project already gave `ADR-0004`. All three rows are stamped `2026-09-11T04:06:14Z`, the moment this `implement` execution is recorded at in the journal: `doc.changelog.no-execution` requires the row's timestamp to fall inside an execution of the skill it names on the item it names, and the only such moment available to a repair made mid-execution is the opening entry's. `to-update`. | 2 |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | Enumerated with `grep -rn "format_amount\|parse_amount" envel/*.py` → exit 0, twelve call sites, all in `envel/envelopes.py` and `envel/cli.py` and every one of them a **call** rather than a conversion. Verdict for the module this change added: `envel/dates.py` matches neither name and touches no cents — it converts text to `datetime.date` and back. `verified-still-true`. | 1, unchanged |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`, the two commands and what lint checks | cited-fact | Both re-run on the branch head: `python3 -m unittest discover -s tests -t .` → exit 0, Ran 90 tests, OK; `python3 -m compileall -q envel tests` → exit 0. The new module and the new test file import only `datetime`, `re` and `json`, so no third-party dependency was added. `verified-still-true`. | 1, unchanged |
| `docs/product/vision.md` | `## What it is for`, item 2: *"Recording a spend against the envelope it came out of."* | cited-fact | This item is what puts behaviour behind it, and the behaviour matches: the spend names the envelope it came out of and reduces only that one (AC1, AC2 above). `verified-still-true`. | 2, unchanged |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | Enumerated with `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, eleven import lines over six files. Members and verdict: `argparse`, `sys`, `datetime`, `re`, `copy`, `dataclasses`, `json`, `os`, `pathlib` — every one standard library and none of them a network, sync or bank facility — plus the three intra-package `from .` lines. `verified-still-true`. | 2, unchanged |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Nothing done. `owned-by-ending`. | 2, unchanged |

## Deviations from the plan

- **One `WI-0001` test was adapted.** `tests/test_cli.py::CommandLine::test_no_subcommand_and_an_unknown_one` asserted that the tool's usage line contained the literal string `{new,add,list}`. Adding a fourth subcommand makes that string false while leaving the criterion it tests true: `WI-0001` AC14 asks for *"a usage message that lists the subcommands the tool does have"*. The assertion now checks that the first line is the tool's own usage — `usage: envel ` — and names each of `new`, `add`, `list` and `spend`, which is the criterion read literally. No acceptance criterion was changed, and `WI-0001`'s behaviour is unaltered. This is the only edit this branch makes to code delivered by another item.
- **Nothing else deviated.** The seven steps were executed as written, in order, with their tests in the same commit.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, Ran 90 tests, OK (52 before this branch). Re-run on the repaired state: exit 0, Ran 90 tests, OK — the repair touches no code, and the suite is the evidence of that. |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 |
| `every-criterion-has-a-test` | pass | the table above: fourteen criteria, each naming a test function, and AC8 to AC10 read out of the store file rather than out of the tool's own output |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0002 wi/WI-0002` → exit 0 — every commit on `main..wi/WI-0002` names the item |
| `no-unplanned-scope` | pass, advisory | every hunk traces to a plan step; the one hunk that is not new code is the adapted `WI-0001` assertion under `## Deviations` |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → exit 0; no sentence sourced to a stakeholder answer was edited on this branch |
| `claims-are-sourced` | pass | `lint-claims --changed-since main --plan-documents WI-0002` → exit 0, scope: the branch's `docs/` diff plus the six documents the plan names |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item WI-0002 --changed-since main` → exit 0, 1 document written under `docs/`, 6 named by the plan |

## The send-back, and what it changed

`review-close` rejected the item at `2026-09-11T04:34:43Z` on D7 and D12, both failing on one
sentence. Three things are worth recording, because the first execution and `verify` made the
same mistake independently and a third reader caught it:

- **What was wrong.** `docs/architecture/overview.md` `## The parts` read *"`cli` knows about
  `envelopes`, `envelopes` knows about `store`, `money` and `dates`, and none of those three knows
  anything above it."* The last clause is true. The middle one is not: `envel/envelopes.py:12` is
  `from . import dates, money`, and the module that knows about `store` is `envel/cli.py`, which
  loads the document at `:70` and writes it back at `:96`.
- **Why two audits missed it.** Both enumerated the imports, both printed the two-module line, and
  both then answered the falsifier they had come looking for — *does any of the three import
  something above it?* — rather than the sentence's own subject. That is why a claim's citation
  resolving is not the same as its citation supporting it, and why `lint-claims` passed over this
  document on every run.
- **What it is now**, as repaired at v4:

  > The dependency direction is one way: `cli` knows about all four modules below it
  > [src: envel/cli.py:13], `envelopes` knows about `money` and `dates`
  > [src: envel/envelopes.py:12], and none of `store`, `money` and `dates` knows anything above
  > it. Reading and writing the store file is `cli`'s work and not `envelopes`'
  > [src: envel/cli.py:68]: an operation is handed a document and returns a new one, which is
  > what keeps the decision layer a pure function of (store, arguments) and lets every criterion
  > be exercised both through the command line and directly. Nothing below `cli` prints, and
  > nothing below `cli` calls `sys.exit`; a refusal travels up as a value.

  The repaired version is **stronger** than the one it replaces, which is the part worth noticing:
  `envelopes` never opening a file is the property that makes the decision layer pure and lets
  every criterion be exercised at two levels, and the false sentence was hiding it.

No acceptance criterion, no ADR, no test and no line of `envel/` changed. `plan.md`'s invalidation
row for this sentence moved from `verified-still-true` to `to-update`, which is the disposition it
should have carried.

## What I did not do

- **No spend's date or description is ever printed back.** Nothing in this item shows them; they
  are observed in the store file, which is where `refine` deliberately put this item's
  observations [src: WI-0002 AC8 "The store file is where this item's dates are read"]. Making
  them visible is `WI-0003` and `WI-0006`.
- **No check that an entry names an envelope that still exists.** The plan records this as an
  assumption: nothing in this epic deletes an envelope, so the case arises only from a
  hand-edited file, and the delivered code already ignores such an entry in the listing. No code
  was added for it.
- **`add_income`'s refusal order was left alone.** It checks the amount before the envelope,
  where `record_spend` checks the envelope first. The plan names the difference and says
  harmonising it would change delivered `WI-0001` behaviour, so it is a separate item if anyone
  wants it.
- **Nothing was done to `## Engagement state` in either document**, at either disposition. Both
  say things this engagement has already outgrown; the ending owns them.
