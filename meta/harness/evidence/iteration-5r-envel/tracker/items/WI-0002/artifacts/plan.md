# Plan — WI-0002 Record spending against an envelope and see what is left

## Problem

`WI-0001` delivered a tool that can create envelopes, put income into them and list what is in
each [src: WI-0001]. This item adds the other half of the ledger: a command that takes money out
of a named envelope and says what is left. It is for the same person at the same terminal, and
the fourteen criteria are mostly about what the tool **refuses** — an envelope that does not
exist, an amount of zero, a spend larger than the envelope holds, a date it cannot read, a date
that has not happened yet, and the wrong number of words on the line.

Two constraints shape it rather than the arithmetic. The first is the stakeholder's: an overspend
is refused rather than shown as a negative envelope — *"if the money has to come from somewhere
else then I want to move it there myself and record the spend after"* [src: EP-001/Q-002] — so
this command reads a balance before it writes anything. The second is that a spend may be dated
[src: WI-0002/Q-001] while income may not [src: WI-0003/Q-003], which is what forces the one
genuinely non-obvious decision here and is recorded as `ADR-0006` [src: ADR-0006].

## Approach

Nothing about the shape of the tool changes. This is a fourth operation in the same three beats —
read the whole store, decide, write it back if anything changed — added in the places the
existing three already live [src: docs/architecture/overview.md].

One new module, `envel/dates.py`, standing in exactly the relation to dates that
`envel/money.py` stands in to amounts [src: ADR-0001]: the only place where the text a person
types and the value the tool holds meet. It parses `YYYY-MM-DD` and nothing else
[src: WI-0002 AC11 "form and nothing else"], formats a date back, and answers what today is. Like
`money.parse_amount`, a text it cannot read raises an error carrying the message the user is
shown, and `envel/cli.py` is the only thing that prints it.

One new operation, `envelopes.record_spend(store, name, cents, on, description)`, returning the
existing `Ok` or `Refusal` [src: envel/envelopes.py]. It appends one entry whose `cents` is
**negative**, so that `envelopes.balance` — the plain sum of `cents` over an envelope's entries
[src: ADR-0002] — keeps working untouched, and so does the listing AC2 is written against.

One new subcommand in `envel/cli.py`: `envel spend <envelope> <amount> [description] [--on DATE]`.
The description is a bare optional positional and the date is a named option, which is the
stakeholder's own choice and their own reason — *"The description is the bit I'll actually type,
so make that the cheap one"* [src: WI-0002/Q-003].

**The order in which refusals are checked** is settled here, because four of them can apply to one
line and `refine` left the order to this skill [src: WI-0002]. Two layers, and within each a fixed
order:

1. **Reading text**, in `envel/cli.py`, in the order the words appear on the line: the shape of
   the arguments (argparse), then the amount, then `--on`. A value has to exist before any policy
   can be applied to it, so this layer is always first.
2. **Deciding**, in `envel/envelopes.py`, in this order: the envelope does not exist (AC3), the
   amount is not positive (AC6), the date is in the future (AC12), the envelope does not hold
   enough (AC5).

The envelope check leads the second layer deliberately. AC3 promises a message **naming the
envelope**, and putting it first is what makes that promise hold on
`envel spend nosuch 0 --on 2099-01-01`, where three criteria refuse at once. The insufficient-funds
check comes last because it is the only one that needs a valid positive amount and a real
envelope before it means anything.

This differs from `add_income`, which checks the amount before the envelope
[src: envel/envelopes.py]. That is delivered, verified behaviour of `WI-0001` and no criterion of
this item touches it, so it is left alone rather than harmonised — see `## Risks`.

## Steps

1. **`envel/dates.py`** — a new module with three functions and one exception, and no dependency
   on anything else in the package.
   - `class DateError(Exception)` — the message is what the user is shown, exactly as
     `money.AmountError` [src: envel/money.py].
   - `parse_date(text)` returns a `datetime.date`. It accepts text matching
     `^\d{4}-\d{2}-\d{2}$` and then parseable by `datetime.date.fromisoformat`; anything else
     raises `DateError` whose message says a date is written as `YYYY-MM-DD`, such as
     `2026-09-07`. The regex is checked **before** `fromisoformat` because on Python 3.12
     `fromisoformat` also accepts `20260907` and other ISO forms
     [src: run: python3 -c "print(__import__('datetime').date.fromisoformat('20260907'))" → exit 0, prints 2026-09-07],
     and AC11 says the full form and nothing else.
   - `format_date(date)` returns `date.isoformat()`.
   - `today()` returns `datetime.date.today()` — the machine's **local** calendar day, which is
     the calendar the person lives in [src: ADR-0006].

   Afterwards: `parse_date("2026-09-07")` is `datetime.date(2026, 9, 7)`; each of `7/9`, `09-07`,
   `yesterday`, `2026-9-7`, `20260907`, `2026-13-45` and `""` raises `DateError`;
   `format_date(datetime.date(2026, 9, 7))` is `"2026-09-07"`.

2. **`envel/envelopes.py`** — add `record_spend(store, name, cents, on, description)`, importing
   `dates` alongside `money`. `cents` is a positive whole number of cents as parsed by
   `money.parse_amount`; `on` is a `datetime.date`; `description` is the text typed or `None`.
   In order:
   - `find(store, name)` is `None` → `Refusal` naming `name` and saying nothing has been recorded
     (AC3);
   - `cents <= 0` → `Refusal` saying a spend has to be more than zero, naming the amount (AC6);
   - `on > dates.today()` → `Refusal` saying that date is in the future, naming the date (AC12);
   - `cents > balance(store, name)` → `Refusal` naming the stored envelope name and the amount
     left in it, formatted by `money.format_amount` (AC5);
   - otherwise append to `entries`
     `{"kind": "spend", "envelope": <the stored name>, "cents": -cents, "on": format_date(on),
     "at": now()}`, plus `"description": <text>` **only** when a description was given
     [src: ADR-0006], and return `Ok` with one line naming the amount spent, the envelope and its
     new balance (AC7), `changed=True`.

   A `description` that is `None`, empty, or only whitespace is recorded as no description — the
   field is absent from the entry. Whitespace at either end of a description that has other
   characters is kept as typed.

   Afterwards: `record_spend` returns `Refusal` in exactly the four cases above and the store it
   was given is unchanged in every one of them; on success the store it returns has one more
   entry and `balance` over that envelope has fallen by exactly `cents`.

3. **`envel/cli.py`** — add the subcommand and its dispatch.
   - In `build_parser`, a `spend` subparser with positionals `name`, `amount` and
     `description` (`nargs="?"`), and an option `--on` taking one value, returned in the
     subcommand-parser dictionary under `"spend"` so that a wrong argument count is reported by
     it (AC14, the mechanism `WI-0001` already built [src: envel/cli.py]). The subparsers'
     `metavar` becomes `{new,add,list,spend}`.
   - In `main`, a branch calling
     `envelopes.record_spend(document, arguments.name, money.parse_amount(arguments.amount),
     dates.parse_date(arguments.on) if arguments.on else dates.today(), arguments.description)`.
   - `dates.DateError` joins `money.AmountError` and `store.StoreError` in the `except` clause
     that prints to stderr and returns 1, so an unreadable date reaches the user by the same
     route as an unreadable amount (AC11, AC13).

   Afterwards: `./bin/envel spend g 12.50 "lunch" --on 2026-08-28` exits 0 with its line on
   stdout; every refusal this item specifies exits non-zero with its message on stderr and
   nothing on stdout (AC13); `./bin/envel spend`, `./bin/envel spend groceries` and
   `./bin/envel spend groceries 12.50 "lunch" extra` each exit non-zero with a usage message for
   `spend` on stderr (AC14).

4. **`tests/test_dates.py`** — a new unit-test module for step 1, naming each rejected form from
   AC11 as its own case.

5. **`tests/test_envelopes.py`** — add cases for step 2: each of the four refusals, the store
   left unchanged in each, the entry's shape on success including `on` and the presence or
   absence of `description`, and the negative `cents`.

6. **`tests/test_cli.py`** — add end-to-end cases for step 3, run as subprocesses against a
   temporary `ENVEL_FILE` [src: ADR-0003], in the style the file already uses
   [src: tests/test_cli.py]. These are the tests that demonstrate the criteria about separate
   invocations (AC4), the store file's contents (AC8, AC9, AC10), the streams and exit codes
   (AC13) and the usage failures (AC14). Assert on the stream, the exit code and a substring the
   criterion itself names — never on argparse's wording.

7. **Close the invalidation set below.** Every row is repaired, or recorded
   `verified-still-true` after reading it against the code that now exists, or left where the
   table says the ending owns it. `## Deliverable documents` is `none`, so no new document is
   written by this item and the only edits permitted under `docs/` are the ones that close a row
   [src: toolkit: doc-header.md §5 "Which skill writes what"].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 2, 3 | `tests/test_cli.py`: after `new groceries` and `add groceries 40`, `./bin/envel spend groceries 12.50` exits 0 and a following `list` shows `27.50` |
| AC2 | 2, 3 | `tests/test_cli.py`: two envelopes funded 40.00 and 10.00, one spend of 12.50 from the first → `list` shows `27.50` and `10.00`, the second line byte-identical to before the spend |
| AC3 | 2 | `tests/test_envelopes.py` and `tests/test_cli.py`: `./bin/envel spend nosuch 5` → stderr contains `nosuch`, exit non-zero, store file unchanged |
| AC4 | 2, 3 | `tests/test_cli.py`: four separate subprocess runs sharing one `ENVEL_FILE` — new, add 40, spend 12.50, list — the fourth showing `27.50` |
| AC5 | 2 | `tests/test_cli.py`: envelope funded 10.00, `spend groceries 12.50` → stderr contains `groceries` and `10.00`, exit non-zero, `list` still shows `10.00` and no `-` anywhere in its output |
| AC6 | 2 | `tests/test_cli.py`: `spend groceries 0` and `spend groceries -5` both exit non-zero with stderr non-empty, and `list` shows the envelope unchanged after each |
| AC7 | 2 | `tests/test_cli.py`: envelope funded 40.00, `spend groceries 12.50` → stdout contains `27.50`, with no `list` run |
| AC8 | 1, 2, 3 | `tests/test_cli.py`: in a fresh `ENVEL_FILE`, new + add + `spend groceries 1.00` + `spend groceries 1.00 --on 2020-01-01`; the file is then read with `json.load` and its two spend entries carry `on` equal to `datetime.date.today().isoformat()` and `"2020-01-01"` respectively |
| AC9 | 1, 2, 3 | `tests/test_cli.py`: the same store, `spend groceries 12.50 --on 2026-08-28` → that entry's `on` is `"2026-08-28"`, and its `at` begins with a different date |
| AC10 | 2, 3 | `tests/test_cli.py`: `spend groceries 12.50 "lunch"`, `spend groceries 1.00`, `spend groceries 1.00 --on 2020-01-01` and `spend groceries 1.00 "lunch" --on 2020-01-01` all exit 0; in the store file the first entry's `description` is `lunch`, the second has no `description` key, and the fourth has both `description` and `on` |
| AC11 | 1, 3 | `tests/test_dates.py` for the forms; `tests/test_cli.py`: `spend groceries 1.00 --on 2026-09-07` exits 0, and each of `--on 7/9`, `--on 09-07`, `--on yesterday`, `--on 2026-9-7` exits non-zero with stderr non-empty and leaves `list` unchanged |
| AC12 | 1, 2 | `tests/test_cli.py`: `--on` set to `datetime.date.today() + timedelta(days=1)` → exit non-zero, stderr contains `future`, `list` unchanged; `--on` set to today → exit 0 |
| AC13 | 3 | `tests/test_cli.py`: a table-driven test walking the refusals of AC3, AC5, AC6, AC11, AC12 and AC14 asserting stderr non-empty, stdout empty and exit non-zero; and the successes of AC1, AC7, AC8, AC9 and AC10 asserting stdout non-empty, stderr empty and exit 0 |
| AC14 | 3 | `tests/test_cli.py`: `spend`, `spend groceries` and `spend groceries 12.50 "lunch" extra` each exit non-zero with `spend` appearing in stderr, and the store file's entry count is the same afterwards |

## Assumptions

- **Refusals are checked in the order given under `## Approach`.** `refine` left it deliberately
  unconstrained and said `plan` may settle it [src: WI-0002]. Reversal: reordering four `if`
  statements in one function in `envel/envelopes.py`; no stored data and no interface changes,
  and every criterion involved is satisfied either way.
- **An empty or whitespace-only description is recorded as no description**, rather than as a
  description that happens to be blank. Left unconstrained by `refine` [src: WI-0002]. It is the
  reading that keeps AC10's *"it can be recorded without one"* true for
  `spend groceries 1.00 ""`, which is what a shell expands an unset variable to. Reversal: one
  predicate in `envel/envelopes.py`.
- **`--on` given twice takes the last one**, which is what `argparse` does with a repeated option
  and costs nothing to leave. Left unconstrained by `refine` [src: WI-0002]. Reversal: one
  `action` argument on the option in `envel/cli.py`.
- **A spend's `on` is the machine's local calendar day and its `at` stays a UTC timestamp**
  [src: ADR-0006]. Reversal: one function in `envel/dates.py`; it changes no stored file's shape,
  though it would change which day a late-evening spend lands on.
- **An entry naming an envelope that is not in `envelopes` is invisible rather than an error.**
  This is the second thing `refine` routed here [src: WI-0002]. Nothing in this epic deletes an
  envelope — `WI-0004`, `WI-0005` and `WI-0006` add moving, correcting and looking up
  [src: WI-0003] [src: WI-0004] [src: WI-0005] [src: WI-0006] — so the case arises only from a
  hand-edited file, and the existing code already behaves this way: `listing` iterates
  `envelopes` and `balance` sums by name [src: envel/envelopes.py]. It is recorded rather than
  coded, and this item adds no check for it. Reversal: a validation pass in `envel/store.py`;
  one function, no stored data change.
- **Where a criterion says `envel`, it means `./bin/envel` in this repository** [src: ADR-0004],
  identically `python3 -m envel`. Unchanged from `WI-0001`
  [src: tracker/items/WI-0001/artifacts/plan.md].

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| A spend carries `on`, the day it happened, as its own field; `at` keeps meaning when the entry was recorded | [src: ADR-0006] | decided — `refine` routed it here, and `WI-0003/Q-003` is what rules out the uniform-field option |
| A spend's `cents` is stored negative | [src: ADR-0002] and `## Approach` above | documented — `ADR-0002` defines a balance as the sum of `cents` over an envelope's entries, so a positive spend would falsify it |
| A date is written `YYYY-MM-DD` and nothing else | [src: WI-0002 AC11 "form and nothing else"] | the stakeholder's, at `WI-0002/Q-004`; nothing is decided here |
| `--on` for the date, a bare word for the description | [src: WI-0002 AC10 "a plain word after the amount and needing no option before it —"] | the stakeholder's, at `WI-0002/Q-003` |
| Dates get their own module, `envel/dates.py`, mirroring `envel/money.py` | `## Approach` above and `docs/architecture/overview.md` | assumed — reversal is moving two functions into `envel/envelopes.py`, one file, nothing published |
| The order in which refusals are checked | `## Assumptions` above | assumed, under no delegation |
| An empty description is no description; `--on` twice takes the last | `## Assumptions` above | assumed, under no delegation |
| An entry naming an absent envelope is invisible, and this item adds no check | `## Assumptions` above | assumed — `refine` routed it here and no criterion of any item observes it |

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | `## The parts`, the module table row `envel/dates.py` | cited-fact | Names a file that does not exist yet; a different split while implementing makes the row false | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`: *"`envelopes` knows about `store`, `money` and `dates`, and none of those three knows anything above it"* | quantified | An import of `envelopes` or `cli` from any of the three falsifies it, and the falsifier is a module the sentence does not name | to-update |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | This change adds a module and an operation below `cli`; a `print` or a `sys.exit` in either falsifies it | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"a spend's `cents` is negative so that the sum keeps working"* and *"A spend carries one field more — `on`, the calendar day the money was spent"* | cited-fact | True only if the entry `record_spend` appends has those two fields with those two meanings | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions this project has adopted`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | quantified | Falsified by any command-line date this tool accepts in another form; `--on` is the first and only one | verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Says nothing has been implemented, verified or accepted, which `WI-0001` reaching `done` already made false, and this item makes further false | owned-by-ending |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`, the JSON entry and the four bullets under it | cited-fact | The entry this item writes has to match it field for field, including `on` always present and `description` present only when typed | verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"The document's `format` stays `1`"* | cited-fact | True only if `envel/store.py`'s `FORMAT` is unchanged and nothing branches on a new value | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`at` is when the tool recorded the entry"* | quantified | This change adds a second date-shaped field; writing an event date into `at` on any kind of entry falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | Falsified by any entry whose sign or kind the balance has to special-case | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Consequences`: *"`WI-0002` adds an entry kind and `WI-0003` filters by `at`, neither needing a format change"* | cited-fact | The first half is this item; and the second half is now wrong in a way this change causes, because `WI-0003` filters a spend by `on` rather than by `at` [src: ADR-0006] | to-update |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | This change adds a module that parses text and an operation that handles cents; either converting between the two forms falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`, the two commands and what lint checks | cited-fact | This change adds a module and a test file, both of which those commands must still cover with no third-party import | verified-still-true |
| `docs/product/vision.md` | `## What it is for`, item 2 of the list: *"Recording a spend against the envelope it came out of."* | cited-fact | Until this item there is nothing behind the sentence; afterwards it describes delivered behaviour and has to match it | verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | A new module is a new place an import could falsify it, and the falsifier is a module the sentence does not name | verified-still-true |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Says the engagement has just begun and nothing has been refined, designed, built, verified or accepted | owned-by-ending |

## Deliverable documents

`none`. No acceptance criterion of `WI-0002` has a document as its subject; the fourteen are all
about the tool's behaviour and the store file it writes. `implement` may therefore write under
`docs/` only to close a row of the invalidation set above.

## Binding ADRs

- `ADR-0001` — every amount in this change is a whole number of cents, and only `envel/money.py`
  converts between cents and text.
- `ADR-0002` — the stored document's shape, the append-only entry list, the balance as a plain
  sum of `cents`, and that no `format` change is needed.
- `ADR-0003` — the store's path, which every criterion of this item is observed against by
  setting `ENVEL_FILE`.
- `ADR-0004` — the package and the `bin/envel` shim, and that no install step and no third-party
  dependency is introduced.
- `ADR-0005` — the test and lint commands this change is checked with, both standard library.
- `ADR-0006` — the spend entry's `on` field, the meaning `at` keeps, the negative `cents`, and
  that `format` stays `1`.

## Scaffolding

`none`. Both directories and both package markers exist [src: envel/__init__.py]
[src: tests/__init__.py], so the declared commands already execute
[src: run: python3 -m unittest discover -s tests -t . → exit 0, Ran 52 tests OK]. `envel/dates.py`
and `tests/test_dates.py` are behaviour and tests, and are `implement`'s to write, not this
skill's.

## Risks

- **`add_income` and `record_spend` will check their refusals in different orders.** The
  delivered `add_income` tests the amount before the envelope [src: envel/envelopes.py]; step 2
  tests the envelope first, for AC3's sake. Nobody typing one command at a time will notice, but
  the next person reading the module will, and may harmonise them — which would change delivered
  `WI-0001` behaviour that `WI-0001` AC5 and AC10 both constrain. If it is worth harmonising, it
  is a separate item.
- **The two date fields can be written into each other.** `on` and `at` are both date-shaped
  strings and nothing in this item prints `on` back [src: WI-0002 AC8 "The store file is where this item's dates are read"],
  so a swap would pass every test that only reads the tool's output. The AC8 to AC10 tests read
  the store file with `json.load` precisely so that this cannot hide.
- **AC12 and AC8 are tests whose expected value is the clock.** Both compute today from
  `datetime.date.today()` at run time; one written with a literal date passes today and fails
  tomorrow. Step 6 says to compute, not to hard-code.
- **`datetime.date.fromisoformat` is more permissive than AC11.** On Python 3.12 it accepts
  `20260907` [src: run: python3 -c "print(__import__('datetime').date.fromisoformat('20260907'))" → exit 0, prints 2026-09-07].
  An implementation that reaches for it alone quietly accepts a form the stakeholder was asked
  about and did not choose [src: WI-0002/Q-004]. Step 1 puts the regex first for that reason.
- **AC5 is read before every write.** The balance that decides an overspend is a sum over the
  whole entry list [src: ADR-0002], so a bug in the summation refuses valid spends and permits
  invalid ones with one mistake. It is the same function the listing already uses, which is why
  step 2 calls it rather than counting again.

## Out of scope for this item

- Correcting or deleting a spend once recorded — `WI-0005` [src: WI-0005].
- Moving money between envelopes — `WI-0004` [src: WI-0004] — which is the route the stakeholder
  wants when AC5 refuses a spend [src: EP-001/Q-002].
- The monthly summary — `WI-0003` [src: WI-0003]. This item writes the `on` field it will read
  and reads none of it.
- Listing or querying the spends against an envelope — `WI-0006` [src: WI-0006]. Nothing in this
  item prints a spend back.
- Dating income. Income carries no date of its own, by the stakeholder's decision
  [src: WI-0003/Q-003], and `envel add` is untouched by this item.
- Changing how `add_income` orders its refusals, or anything else `WI-0001` delivered.
- A short date form such as `7/9`. The stakeholder said what it would mean to them if one were
  ever added [src: WI-0002/Q-004]; nobody has asked for one and this item does not build one.
