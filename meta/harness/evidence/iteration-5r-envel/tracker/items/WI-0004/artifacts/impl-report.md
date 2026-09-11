# Implementation report — WI-0004

## What was built

One subcommand, `envel move <from> <to> <amount>` with an optional `--on YYYY-MM-DD`, and the
operation behind it.

- **`envel/envelopes.py`** gains `move(store, source, destination, cents, on)`, below
  `record_spend`. It performs six refusals in the plan's order and, on success, deep-copies the
  document and appends the two entries of `ADR-0007` — one naming each envelope, `cents` negative
  on the side the money left and positive on the side it arrived, with the same `on` and the same
  `at` on both. `at` is computed once and `on` formatted once, then each written twice, so the two
  halves cannot disagree. It returns one line naming the amount, the source, what the source now
  holds, the destination, and what the destination now holds.
- **`envel/cli.py`** gains the `move` subparser and one dispatch branch. The two envelope
  arguments are `source` and `destination` on the namespace and `from` and `to` on the usage line,
  because `from` is a Python keyword. The top-level subcommand `metavar` gains `move`.
- **`tests/test_envelopes.py`** gains a `Move` class, 14 tests against the operation directly.
- **`tests/test_cli.py`** gains a `Move` class, 13 tests running the tool as a separate process
  with `ENVEL_FILE` at a scratch path.

`envel/store.py`, `envel/money.py` and `envel/dates.py` are untouched: a move parses its amount and
its date through the two modules that already exist for exactly that, and `FORMAT` stays `1`.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `envel move <from> <to> <amount>` with an optional `--on <date>`; the move is held against the date given | `tests.test_cli.Move.test_a_dated_move_is_held_against_that_date` — runs `envel move groceries fun 20 --on 2026-08-28` against a scratch `ENVEL_FILE` and reads the store: two `move` entries, both `on: "2026-08-28"`, `cents` `-2000` and `2000`, envelopes `groceries` and `fun`. Also `tests.test_envelopes.Move.test_two_entries_one_per_envelope_with_opposite_signs` |
| AC2 | the two entries are the whole of the change, so the balances follow from the storage | `tests.test_cli.Move.test_only_the_two_named_envelopes_move` — listing before and after: `groceries  27.50`, `fun  12.50`, and `car  10.00` identical in both. Also `tests.test_envelopes.Move.test_the_balances_move_by_exactly_the_amount_and_nothing_else_does` |
| AC3 | the funds check, last of the six, quoting the source's balance | `tests.test_envelopes.Move.test_more_than_the_source_holds_is_refused_and_says_what_is_left` — message contains `groceries` and `40.00`, and the document is equal to a deep copy taken before the call. Boundary at `tests.test_envelopes.Move.test_moving_exactly_what_the_source_holds_is_allowed`. Stream and exit code at `tests.test_cli.Move.test_more_than_the_source_holds` |
| AC4 | the two existence checks, first of the six, each naming the envelope it could not find | `tests.test_envelopes.Move.test_a_source_that_does_not_exist_is_refused_by_name` and `...test_a_destination_that_does_not_exist_is_refused_by_name`; end to end at `tests.test_cli.Move.test_an_envelope_that_does_not_exist_on_either_side`, which asserts both sides and that the store holds no `move` entry afterwards |
| AC5 | the whole document is written back atomically, as every command does | `tests.test_cli.Move.test_a_move_survives_into_a_later_invocation` — the move in one subprocess, `envel list` in a second: `groceries  20.00`, `fun  20.00` |
| AC6 | `dates.today()` when `--on` is absent, in `cli` | `tests.test_cli.Move.test_no_date_given_records_today_and_a_date_given_is_kept` — one move with no `--on` and one with `--on 2020-01-01`; the four stored entries carry `[today, today, "2020-01-01", "2020-01-01"]` |
| AC7 | `dates.parse_date`, which accepts the full form and nothing else, raising before the operation is reached | `tests.test_cli.Move.test_only_the_full_form_of_a_date_is_accepted` — `28/8`, `08-28`, `yesterday` and `2026-13-01` each exit non-zero with something on stderr and nothing on stdout; the store holds no `move` entry and the listing still shows `groceries  40.00`; `2026-08-28` is then accepted |
| AC8 | `on > dates.today()`, the fifth of the six refusals | `tests.test_cli.Move.test_a_date_in_the_future_is_refused_and_today_is_not` — tomorrow refused with `future` on stderr and the listing unchanged, today accepted. Also `tests.test_envelopes.Move.test_a_date_later_than_today_is_refused_and_today_is_not`, which checks yesterday too |
| AC9 | the success line, built from the new document | `tests.test_cli.Move.test_the_line_names_both_envelopes_the_amount_and_what_each_holds` — stdout contains `12.50`, `groceries`, `27.50` and `fun`, stderr is empty, exit 0, and `groceries` appears before `fun` so the direction is readable. Also `tests.test_envelopes.Move.test_the_line_names_both_envelopes_and_what_each_now_holds`, which checks the destination's new balance too |
| AC10 | `cents <= 0`, the fourth of the six refusals | `tests.test_envelopes.Move.test_zero_and_negative_amounts_are_refused` — `0.00` and `-5.00` in the messages, document unchanged against a deep copy. End to end at `tests.test_cli.Move.test_zero_and_negative_amounts` |
| AC11 | `fold(source) == fold(destination)`, the third of the six | `tests.test_envelopes.Move.test_the_same_envelope_on_both_sides_is_refused` — `groceries`→`groceries` and `groceries`→`Groceries` both refused with the name in the message. End to end at `tests.test_cli.Move.test_the_same_envelope_on_both_sides` |
| AC12 | `cli` is the only module that writes a stream or chooses an exit code, and it is unchanged in that respect | `tests.test_cli.Move.test_every_refusal_goes_to_stderr_and_every_success_to_stdout` — a table with one case per criterion AC12 names, keyed by criterion: refusals `AC3`, `AC4`, `AC7`, `AC8`, `AC10`, `AC11`, `AC13`, each asserted non-zero with stderr non-empty and stdout empty; successes `AC1/AC2/AC9`, `AC6`, `AC6-today`, each exit 0 with stdout non-empty and stderr empty; and `AC5`'s listing. **Every criterion AC12 names has an executable case**, so the non-intersection clause of AC12 is not reached and nothing is waived |
| AC13 | argparse, through the existing `parse_known_args` path that reports a wrong argument count on the subcommand's own parser | `tests.test_cli.Move.test_the_wrong_number_of_words` — `envel move`, `envel move groceries`, `envel move groceries fun`, `envel move groceries fun 20 extra`: each exits non-zero, stderr contains `usage: envel move`, stdout is empty, and the store holds no `move` entry. The fourth is what makes *a move carries no description* observable |

Ticking the boxes in `item.md` is `verify`'s and was not done here.

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/architecture/overview.md` | `## The parts`, the `envelopes.py` row naming five operations including moving money | cited-fact | `envel/envelopes.py` defines `create`, `add_income`, `record_spend`, `listing` and now `move` [src: envel/envelopes.py:184]. The split is the one the row describes; no new module was added | unchanged (v5) |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | **quantified** | The set is the modules below `cli`: `envelopes`, `store`, `money`, `dates` — enumerated from the import line [src: envel/cli.py:13]. `grep -rn "print(\|sys.exit\|sys\.std" envel/*.py` with `envel/cli.py` excluded returns exactly one line, `envel/__main__.py:8: sys.exit(main())` [src: run: grep -rn "print(\|sys.exit\|sys\.std" envel/\*.py, excluding cli.py → exit 0, 1 line: envel/__main__.py:8]. `__main__` is **above** `cli`, not below it — it imports and calls `main` [src: envel/__main__.py:5] — so it is not a member of the set. Verdict per member: `envelopes` no, `store` no, `money` no, `dates` no | unchanged (v5) |
| `docs/architecture/overview.md` | `## The data`, the new sentences on what a move stores | cited-fact | The two appended entries carry `kind`, `envelope`, `cents`, `on`, `at`, with `-cents` on the source and `+cents` on the destination and one `at` and one `day` written twice [src: envel/envelopes.py:244]. Asserted by `tests.test_envelopes.Move.test_two_entries_one_per_envelope_with_opposite_signs` and `...test_both_halves_carry_the_same_day_and_the_same_moment` | unchanged (v5) |
| `docs/architecture/overview.md` | `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | **quantified** | The family is the entry kinds: `income`, `spend`, `move` — enumerated by `grep -n '"kind"' envel/*.py`, which returns four write sites and no read site [src: run: grep -n '"kind"' envel/\*.py → exit 0, 4 lines, all of them writes at envelopes.py:93, 149, 245, 248]. `balance` contains no reference to `kind` at all [src: envel/envelopes.py:50], so there is no member it special-cases. Verdict per member: `income` no special case, `spend` no special case, `move` no special case | unchanged (v5) |
| `docs/architecture/overview.md` | `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | **quantified** | The family is the command-line dates this tool reads. `grep -rn "parse_date" envel/*.py` gives two call sites, both in `cli` and both `--on` — `spend` and `move` [src: run: grep -rn parse_date envel/\*.py → exit 0, 3 lines: cli.py:100, cli.py:109, and the definition at dates.py:25]. Both go through `dates.parse_date`, whose regex admits only four digits, two and two [src: envel/dates.py:20]. Verdict per member: `envel spend --on` conforms, `envel move --on` conforms — the latter asserted by `tests.test_cli.Move.test_only_the_full_form_of_a_date_is_accepted` | unchanged (v5) |
| `docs/architecture/overview.md` | `## What is not decided yet`, now naming three items | cited-fact | `WI-0004`'s design is recorded in `ADR-0007` [src: ADR-0007] and `tracker/items/WI-0004/artifacts/plan.md`. `envel/store.py` still reads and writes `FORMAT = 1` [src: envel/store.py:12] and nothing branches on another value | unchanged (v5) |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | **Nothing was done.** `review-close` restates it at the ending | unchanged (v5) |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision`, the JSON pair and the six bullets | cited-fact | Read field for field against the appended entries [src: envel/envelopes.py:244]: `kind` `move` on both, one envelope each, `cents` negative then positive, `on` as `YYYY-MM-DD` from `dates.format_date`, one `at` on both, and no `description` key — the last asserted by `tests.test_envelopes.Move.test_a_move_carries_no_description` | unchanged (v1) |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision`: *"The document's `format` stays `1`"* | cited-fact | `envel/store.py` line 12 is `FORMAT = 1`, unchanged on this branch [src: envel/store.py:12], and `git diff main -- envel/store.py` is empty | unchanged (v1) |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Consequences`: *"one entry kind and no field that some other kind does not already carry"* | **quantified** | The family is the fields on a `move` entry: `kind`, `envelope`, `cents`, `on`, `at` [src: envel/envelopes.py:245]. Verdict per member, against the other two kinds: `kind`, `envelope`, `cents` and `at` are on an income entry [src: envel/envelopes.py:93]; `on` is on a spend entry [src: envel/envelopes.py:152]. No member is new | unchanged (v1) |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"`at` keeps the meaning `ADR-0002` gave it — on every entry of every kind"* | **quantified** | The family is the entry kinds, enumerated as above: `income`, `spend`, `move`. Verdict per member: income writes `"at": now()` [src: envel/envelopes.py:93]; spend writes `"at": now()` [src: envel/envelopes.py:153]; move computes `at = now()` once and writes it on both halves [src: envel/envelopes.py:242]. `now()` is the recording moment [src: envel/envelopes.py:31] and no kind writes an event date into `at` | **v2** |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Consequences`: *"`WI-0003` sums a month's spending by `on` and a month's income by `at`"* | **quantified**, disposed `to-update` | The family is the sums `WI-0003` makes, one per kind. The sentence named two of what are now three, so a reader taking the list as complete would conclude a move has no date of its own. Repaired as an **erratum** — a clause naming moves, citing `ADR-0007`, with a `## Corrections` row and a change-log row. The surviving clause *"with no branch on what a date means"* was checked and holds: `on` is the day the money moved on a spend [src: envel/envelopes.py:152] and on a move [src: envel/envelopes.py:245] alike. No decision changed and no code changed | **v2** |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | **quantified** | Same enumeration as the overview row above, and the same verdict: `balance` reads `cents` and `envelope` and nothing else [src: envel/envelopes.py:50]. The two entries a move appends are ordinary members of that sum, which is why AC2 needed no arithmetic | unchanged (v2) |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`entries` is append-only within a run and ordered as written"* | **quantified** | The family is the writes to `store["entries"]`, enumerated by `grep -n 'entries"\]' envel/*.py`: every one is `.append` [src: envel/envelopes.py:245] and none is an assignment, a `del`, a `sort` or a slice. Verdict per member: `add_income` appends, `record_spend` appends, `move` appends twice. Nothing reorders or rewrites | unchanged (v2) |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | **quantified** | The family is every site where cents and text meet. `grep -rn "format_amount\|parse_amount\|int(\|/ 100\|\* 100" envel/*.py` returns the two conversions inside `money.py` — `int(whole) * 100 + …` [src: envel/money.py:34] and `"{}{}.{:02d}".format(…)` [src: envel/money.py:42] — and everything else is a **call** to one of those two. Verdict per member: the new `move` calls `money.format_amount` five times and converts nothing itself [src: envel/envelopes.py:254]; the new subparser hands its `amount` to `money.parse_amount` in `cli` [src: envel/cli.py:108] | unchanged |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`, the two commands and what lint checks | cited-fact | Both commands were run on the branch head: `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests; `python3 -m compileall -q envel tests` → exit 0. Every import added by this change is standard library or intra-package — see the vision row below | unchanged |
| `docs/product/vision.md` | `## What it is for`: *"moving an amount from one envelope to another"* | cited-fact | The sentence now describes delivered behaviour, and it matches: one amount, one source, one destination, and the stakeholder's stated use — the route out of a refused overspend — works, because `envel move` is what `record_spend`'s own refusal message already pointed at [src: envel/envelopes.py:139] | unchanged (v2) |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"no server, no sync, no bank import, no network"* | **quantified** | The family is every import in the package, enumerated by `grep -rn "^import \|^from " envel/*.py` → 12 lines [src: run: grep -rn "^import \|^from " envel/\*.py → exit 0, 12 lines]. Verdict per member: `argparse`, `sys`, `copy`, `dataclasses`, `datetime`, `re`, `json`, `os`, `pathlib` are standard library and none opens a socket; `from . import …` and `from envel.cli import main` are intra-package. This change added **no** import at all | unchanged (v2) |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | **Nothing was done.** `review-close` restates it at the ending | unchanged (v2) |

No row was disposed `question-filed`, and no row was added to the set: every document this change
touched was already enumerated by the plan.

## Deviations from the plan

Two, both inside the plan's latitude, and neither changes what is delivered.

1. **The plan's step 5 asked for one test fixing the refusal order; two were written.**
   `test_the_envelopes_are_checked_before_the_amount_and_the_date` covers the plan's case, and
   `test_the_same_envelope_is_checked_before_the_amount` covers the half it did not: when both
   names resolve, the same-envelope refusal is reached rather than the amount one. The plan
   decided that ordering explicitly, so leaving it unasserted would have left half the decision
   unprotected.
2. **`test_only_the_full_form_of_a_date_is_accepted` tests a fourth form, `2026-13-01`.** The
   plan named three. The fourth is a date of the right *shape* that is not a day that exists, and
   `envel/dates.py` refuses it on a different branch [src: envel/dates.py:31]; a test of the form
   check alone would not have reached it.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests, run on the branch head after the last change |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `validate-workspace` → 0 errors, 0 warnings |
| `every-criterion-has-a-test` | pass | the table above names a test function for each of AC1–AC13; none is demonstrated by reading the code |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, all 2 commits on `main..wi/WI-0004` name `WI-0004` |
| `no-unplanned-scope` | pass (advisory) | the diff is `envel/envelopes.py` (one function), `envel/cli.py` (a subparser, a metavar, a dispatch branch), the two test files, and `ADR-0006`'s erratum. Every hunk traces to a plan step or to an invalidation row |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → exit 0 |
| `claims-are-sourced` | pass | `lint-claims --changed-since main --plan-documents WI-0004` → exit 0; scope was 7 documents — 1 changed on the branch plus the 7 named by the plan |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item WI-0004 --changed-since main` → exit 0; 1 document written on the branch, 7 named by the plan |

## What I did not do

- **I did not tick any acceptance criterion in `item.md`.** That is `verify`'s.
- **I did not add a pairing identifier to the two entries of a move.** The plan records it as an
  assumption with its cost, and nothing in this epic reads the pair.
- **I did not touch either `## Engagement state` section**, at any disposition.
- **I did not write anything `WI-0003` will need beyond the stored entries.** Computing the net
  moved figure is `WI-0003`'s work; this item only makes it possible, and no test here asserts
  anything about a summary.
- **I did not verify the timezone edge in `ADR-0006`** — that `at` is UTC while `on` is the local
  calendar day, so they can differ late in the evening. It is unchanged by this item, a move
  inherits it exactly as a spend has it, and no criterion of this item reaches it.
