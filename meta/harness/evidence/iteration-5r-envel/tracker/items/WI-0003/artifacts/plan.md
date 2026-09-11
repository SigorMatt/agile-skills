# Plan — WI-0003 Show a summary of a month

## Problem

The tool records income, spending and moves, and shows what is in each envelope right now. It
cannot yet answer *what happened in August*. `WI-0003` adds one subcommand, `envel summary`, which
takes an optional month as a plain word and prints one row per envelope with four figures: what
went in that month, what was spent, the net moved, and what is left at the end of it
[src: WI-0003 AC2 "each row shows four figures for that"]. The four have to **reconcile** —
carried-in + in − spent + moved = left — because the stakeholder said they would not use a report
whose rows do not add up [src: WI-0003/Q-001], and the amount left carries over from the previous
month rather than starting at zero, which they named as the thing they would least want us to get
wrong [src: EP-001/Q-001].

The constraints are the ones this project already runs under: whole cents only [src: ADR-0001],
one JSON document read whole and never rewritten by a read [src: ADR-0002], the store found
through `ENVEL_FILE` or the XDG directory [src: ADR-0003], two entry points reaching one `main`
[src: ADR-0004], the standard library and nothing else [src: ADR-0005], `on` as the day an event
happened and `at` as when it was recorded [src: ADR-0006], and a move stored as two entries of
kind `move` [src: ADR-0007]. Two more constraints are this item's own, decided here: how an entry's
month is determined and how the figures are summed [src: ADR-0008], and where the code lives
[src: ADR-0009].

Nothing this item does changes a stored byte. `envel summary` reads the document and prints;
`result.changed` is false, so `cli` does not save [src: envel/cli.py:124].

## Approach

**A month is a seven-character string, `YYYY-MM`, and it is compared as a string**
[src: ADR-0008]. Both date fields in the store are zero-padded fixed-width ISO, so their first
seven characters are a month in the same form and lexicographic order is chronological order.
*Earlier than*, *in* and *later than* are `<`, `==` and `>`. No calendar arithmetic appears
anywhere in this change.

**The month an entry falls in is `on` if it has one, otherwise `at`** [src: ADR-0008]. That one
expression is AC8's asymmetry — income by when it was typed, a spend and a move by the day the
money moved — with no branch on `kind`, and it is `ADR-0006`'s own sentence implemented rather
than paraphrased [src: ADR-0006].

**Every figure is a filtered sum** over the entries naming the envelope, in the shape `ADR-0002`
already gives `balance` [src: envel/envelopes.py:50]. That is what makes AC3's reconciliation a
property of the arithmetic rather than something a step has to arrange: the three month-M columns
partition month M's entries and `left` is the sum over months ≤ M, so `left − (in − spent + moved)`
is the sum over months < M, which is the carried-in balance by definition. **No step below
computes a carried-in figure and no step checks the identity** — there is nothing that could drift.

**Three interface decisions**, none of them implementation:

1. **`envel/dates.py` gains three functions**: `parse_month(text)` returning the `YYYY-MM` string
   or raising `DateError`; `this_month()` returning today's month in that form; and
   `month_of(text)` returning the first seven characters of a `YYYY-MM-DD` or of a
   `YYYY-MM-DDTHH:MM:SSZ`. They go there rather than anywhere else because that module is already
   *"the only place text and calendar days meet"* [src: envel/dates.py:1], which is a decision this
   item reads rather than takes.

   `parse_month`'s regex carries the month range itself — four digits, a hyphen, then `01`–`12` —
   because there is no `date.fromisoformat` equivalent for a month to check the calendar
   afterwards, which is how `parse_date` is built [src: envel/dates.py:20]. `2026-13` is refused
   by the regex, which is what AC12 names.

2. **`envel/summary.py` is a new module** holding `entry_month(entry)`, `figures(store, name,
   month)` and `summarise(store, month)` [src: ADR-0009]. `summarise` returns `envelopes.Ok` or
   `envelopes.Refusal` — the same two types every operation returns
   [src: envel/envelopes.py:1] — so `cli` dispatches it with no new branch shape.

3. **The row is a sentence, not a column layout, and there is no header line.** `refine` left
   *"whether the four figures carry a header line"* deliberately unconstrained
   [src: tracker/items/WI-0003/artifacts/refinement-qa.md], so it is decided here. Each row names
   its own four figures — `groceries  in 0.00  spent 20.00  moved 30.00  left 60.00` — and there is
   no heading above them. Two reasons, and the second is the binding one: every success line this
   tool prints is prose that says what it is [src: envel/envelopes.py:99]
   [src: envel/envelopes.py:253], and AC6 says the summary's content is *"the four columns of AC2
   and nothing else"* [src: WI-0003 AC6 "Its content is the four columns of AC2 and nothing else"],
   which a header line would have to argue its way past and a label inside a row would not.
   Recorded under `## Assumptions` with what reversing it costs.

**The order in which the refusals are checked** is settled here, as `WI-0002`'s and `WI-0004`'s
were, and it is read off the existing structure rather than chosen:

1. **the wrong command line** (AC14) — argparse's, through the `parse_known_args` path
   [src: envel/cli.py:80], before any document is opened;
2. **a month the tool cannot read** (AC12) — raised by `dates.parse_month` as the argument is
   parsed in `cli`, before `summarise` is reached, exactly as a malformed date is today
   [src: envel/cli.py:100];
3. **a month later than this one** (AC9) — the first thing `summarise` checks;
4. the report.

So `envel summary 2027-13`, which is both unreadable and in the future, reports the unreadable
month. `refine` recorded that every criterion involved is satisfied by any of the messages
[src: tracker/items/WI-0003/artifacts/refinement-qa.md], and this order is the one the delivered
structure already produces, so nothing new is decided.

**AC14 needs no new code and that was checked rather than assumed.** With `month` as an optional
positional, `parse_known_args` leaves `--month` unrecognised and `extra` unrecognised, and
`cli` then calls the **subcommand's** own parser's `error` [src: envel/cli.py:82], which prints
`usage: envel summary …` to stderr and exits 2
[src: run: python3 - (an argparse probe building the intended summary subparser and calling parse_known_args on the four command lines above) → exit 0; month is None then 2026-08 three times, and unrecognised is empty, empty, --month, extra].
The delivered behaviour was confirmed on a shipped subcommand too
[src: run: python3 bin/envel list --month 2026-08 → exit 2, "usage: envel list [-h]" and "unrecognized arguments: --month 2026-08"].

**`-h` remains on the subparser**, as it is on all five delivered subcommands. AC14's subject is
*"an option, where this subcommand takes none"* [src: WI-0003 AC14 "an option, where this
subcommand takes none"] — an option carrying the month — and `-h` is argparse's own, not one this
subcommand takes. Recorded under `## Assumptions`.

## Steps

1. **`envel/dates.py` — add `parse_month`, `this_month` and `month_of`**, below `today()`. A
   module-level `_MONTH` regex of four digits, a hyphen and `01`–`12`, mirroring `_DATE`'s shape
   [src: envel/dates.py:20]; `parse_month` returns the matched text unchanged and otherwise raises
   `DateError` with a message naming what was typed and the form wanted, in the shape
   `parse_date`'s message already has [src: envel/dates.py:27]. `this_month` is
   `datetime.date.today().isoformat()[:7]`, taken from the same local calendar `today()` uses
   [src: envel/dates.py:45]. `month_of(text)` is `text[:7]`, named so that the seven is written
   once. **Afterwards:** `python3 -c "from envel import dates; print(dates.parse_month('2026-08'), dates.this_month())"`
   prints two months, and `dates.parse_month('2026-13')` raises `DateError`.

2. **`envel/summary.py` — the new module, with `entry_month(entry)`.** Returns
   `month_of(entry["on"])` when the entry has an `on` and `month_of(entry["at"])` otherwise
   [src: ADR-0008]. No reference to `kind`. The module docstring says what the module owns and
   cites `ADR-0008` and `ADR-0009`. **Afterwards:** `python3 -c "from envel import summary"`
   imports, and `entry_month` returns `2026-08` for a spend carrying `on: "2026-08-28"` whatever
   its `at` says.

3. **`envel/summary.py` — `figures(store, name, month)`**, returning the four integers
   `(income, spent, moved, left)` in cents for one envelope: `income` the sum of `cents` over that
   envelope's `income` entries in `month`; `spent` the **negated** sum over its `spend` entries in
   `month`, so the figure is positive; `moved` the signed sum over its `move` entries in `month`;
   `left` the sum of `cents` over every entry of that envelope whose month is `<=` month. Entries
   are matched to an envelope on the case-folded name, through `envelopes.fold`
   [src: envel/envelopes.py:36], which is how `balance` already does it
   [src: envel/envelopes.py:50]. **Afterwards:** for an envelope with 50.00 carried in from an
   earlier month, nothing added, 20.00 spent and 30.00 moved in during the month,
   `figures` returns `(0, 2000, 3000, 6000)` — AC3's worked example, in cents.

4. **`envel/summary.py` — `summarise(store, month)`.** In order: refuse when
   `month > dates.this_month()`, with a message saying that month has not happened yet (AC9);
   select the envelopes whose `month_of(envelope["created"]) <= month` (AC7); if that selection is
   empty, return `Ok` with one line saying there is nothing to summarise for that month (AC4);
   otherwise return `Ok` with one line per selected envelope, sorted by `envelopes.fold(name)`
   (AC10). `changed` is left at its default, so nothing is written. **Afterwards:** `summarise`
   returns `Refusal` for a month after this one and `Ok` otherwise, printing nothing and calling
   no `sys.exit`.

5. **`envel/summary.py` — the row.** One line per envelope carrying the envelope's stored name and
   the four figures in the order of AC2 — in, spent, moved, left — each formatted by
   `money.format_amount` and by nothing else [src: ADR-0001], each labelled inside the row, with no
   header line above the rows (`## Approach`, interface decision 3). **Afterwards:** a row contains
   the name and four amounts, every amount matching `-?\d+\.\d\d`.

6. **`envel/cli.py` — add the `summary` subparser and the dispatch branch.** One optional
   positional, `month`, with `nargs="?"`, `default=None` and `metavar="YYYY-MM"`, and **no
   options** beyond argparse's `-h`. Add `summary` to the subcommand list in the top-level
   `metavar`, which is currently `{new,add,list,spend,move}` [src: envel/cli.py:26] — `WI-0001`
   requires the usage message to list the subcommands the tool has
   [src: WI-0001 AC14 "print to stderr a usage message that lists the subcommands the tool does
   have"]. The branch calls `summary.summarise(document, dates.parse_month(arguments.month) if
   arguments.month else dates.this_month())`. Nothing else in `main` changes: the existing
   `except` already turns `DateError` into a message on stderr and exit 1 (AC12), and the existing
   `Refusal` branch already does the same for a refusal (AC9, AC13)
   [src: envel/cli.py:114]. **Afterwards:** `envel` with no subcommand prints a usage line naming
   `summary`; `envel summary` runs end to end against a store at `ENVEL_FILE`; and
   `envel summary --month 2026-08` prints `summary`'s own usage to stderr and exits non-zero.

7. **`tests/test_dates.py` — add a `Month` class** for step 1: `2026-08` accepted and returned
   unchanged; `2026-8`, `08-2026`, `august`, `2026-13`, `2026-00` and `2026-08-01` each raising
   `DateError` (AC12, every form AC12 names plus the two boundaries of the month range);
   `this_month()` equal to `datetime.date.today().isoformat()[:7]`; `month_of` over both a
   `YYYY-MM-DD` and a `YYYY-MM-DDTHH:MM:SSZ`. **Afterwards:** these tests pass.

8. **`tests/test_summary.py` — a new file** exercising the module directly, in the shape
   `tests/test_envelopes.py` uses [src: tests/test_envelopes.py:10] with a helper that builds a
   document and appends entries with chosen `on` and `at` values, since a back-dated income cannot
   be produced through the operations. Cases: `entry_month` for all three kinds including an income
   with no `on` (AC8) and a spend whose `on` and `at` fall in different months; `figures` returning
   AC3's worked example (AC2, AC3); the reconciliation asserted as an identity over a document
   carrying several months and all three kinds (AC3); a row for an envelope with no activity
   showing three zeros and its carried-over balance (AC7); no row for an envelope created after the
   month ended and a row for one created within it (AC7); the ordering, including a name whose
   capitalisation differs from its neighbours' (AC10); a month after this one returning `Refusal`
   and the month today falls in returning `Ok` (AC9, at the boundary); and an empty selection
   returning `Ok` with one line (AC4). **Afterwards:** these tests pass and fail if the month rule
   changes.

9. **`tests/test_cli.py` — add a `Summary` class** running the tool as a separate process with
   `ENVEL_FILE` at a scratch path, in the shape the `Move` class uses
   [src: tests/test_cli.py:501]: `envel summary 2026-08` and bare `envel summary` (AC1, AC5); the
   four figures and their labels on a real row (AC2, AC11); a past month printing the same rows
   after a later envelope is created (AC7); AC4's nothing-to-print line with exit 0; the three
   malformed months of AC12 with nothing on stdout; a future month refused with a message on
   stderr and this month accepted (AC9); the wrong-shape lines of AC14 —
   `envel summary --month 2026-08`, `envel summary 2026-08 extra` — each printing `usage: envel
   summary` to stderr with nothing on stdout; one test capturing stdout, stderr and the exit code
   together for every criterion AC13 names (AC13); and one asserting the tool's own usage now lists
   `summary`, as the `Move` class does for its subcommand [src: tests/test_cli.py:722].
   **Afterwards:** `python3 -m unittest discover -s tests -t .` exits 0.

10. **`docs/architecture/overview.md`** — already updated by this execution to version 6: the
    `envel/summary.py` row, the dependency sentence, the command-line month in `## Conventions`,
    and `WI-0003` leaving `## What is not decided yet`. `implement` touches it again only to close a
    row of the invalidation set below. **Afterwards:** nothing for `implement` to do here unless a
    row says so.

**A note on who does what.** Ticking this item's acceptance criteria is `verify`'s and not
`implement`'s [src: toolkit: work-item.md §2 "the checkbox is verify's"]; no step above asks for
it. `implement` writes under `docs/` only to close a row of the invalidation set or to produce a
deliverable document, and this item has none.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 6 | `tests/test_cli.py` `Summary`: `envel summary 2026-08` against a scratch `ENVEL_FILE` exits 0 and prints rows; and `envel summary --month 2026-08` exits non-zero with `usage: envel summary` on stderr, which is the second half of the criterion |
| AC2 | 3, 5 | `tests/test_summary.py`: `figures` returns the four integers for an envelope with income, a spend and a move in the month, the moved figure one net number positive when more arrived; `tests/test_cli.py` `Summary`: the printed row carries all four |
| AC3 | 3 | `tests/test_summary.py`: AC3's own worked example — 50.00 carried in, 0.00 in, 20.00 spent, 30.00 moved, 60.00 left; and the identity `left == carried_in + income - spent + moved` asserted over a document spanning three months with all three kinds, where `carried_in` is computed independently in the test from months before the one summarised |
| AC4 | 4 | `tests/test_summary.py`: a store whose only envelope was created after the month ends returns `Ok` with exactly one line; `tests/test_cli.py` `Summary`: the same end to end — a line on stdout, nothing on stderr, exit 0 |
| AC5 | 1, 4, 6 | `tests/test_cli.py` `Summary`: bare `envel summary` prints rows for the month `date.today()` falls in, checked against a spend dated into that month and one dated into the previous one; `envel summary <a month that has ended>` still prints it |
| AC6 | 4, 5 | `tests/test_cli.py` `Summary`: stdout of a summary over a store with three spends in the month has exactly one line per envelope — no total line, no per-spend line, and no line that is neither |
| AC7 | 4 | `tests/test_summary.py`: an envelope with no activity in the month gets a row of `0.00 0.00 0.00 <carried-over>`; an envelope created after the month ended gets none; `tests/test_cli.py` `Summary`: a past month's output is byte-identical before and after a new envelope is created |
| AC8 | 2, 3 | `tests/test_summary.py`: an income entry with no `on` and an `at` in September counts in September, not in the August of a spend recorded in the same call; `entry_month` asserted directly for all three kinds |
| AC9 | 4 | `tests/test_summary.py`: next month returns `Refusal`, this month returns `Ok` — the boundary; `tests/test_cli.py` `Summary`: the message on stderr, nothing on stdout, non-zero exit |
| AC10 | 4 | `tests/test_summary.py`: rows for `Fun`, `apples` and `zebra` come back in that folded order; `tests/test_cli.py` `Summary` reads the same order off stdout |
| AC11 | 5 | `tests/test_cli.py` `Summary`: every amount-shaped token on every row matches `-?\d+\.\d\d`, including a zero and an amount over 1000 written without a separator |
| AC12 | 1, 6 | `tests/test_dates.py` `Month`: each of `2026-8`, `08-2026`, `august`, `2026-13`, `2026-00`, `2026-08-01` raises `DateError`; `tests/test_cli.py` `Summary`: three of them end to end, exiting non-zero with nothing on stdout |
| AC13 | 4, 5, 6 | `tests/test_cli.py` `Summary`: one test capturing stdout, stderr and the exit code on the same invocation for each criterion AC13 names — refusals at AC9, AC12 and AC14, successes at AC1, AC2, AC4, AC5, AC6, AC7 and AC8 — so its read of those criteria has an executable case behind every one of them |
| AC14 | 6 | `tests/test_cli.py` `Summary`: `envel summary --month 2026-08` and `envel summary 2026-08 extra` each print `usage: envel summary` to stderr, exit non-zero, and print nothing on stdout |

## Assumptions

- **The row is a labelled sentence and there is no header line.** *Reversal:* one format string in
  `envel/summary.py` and the tests that read a row. No stored data, no interface. `refine` left
  this unconstrained on purpose [src: tracker/items/WI-0003/artifacts/refinement-qa.md]; AC2 fixes
  which four figures and AC11 fixes their form, and neither names the wording. A disagreement lands
  on step 5 and costs one line of code.
- **`-h` stays on the `summary` subparser.** *Reversal:* `add_help=False` on one `add_parser` call.
  Every delivered subcommand has it, and AC14's subject is an option carrying the month rather than
  argparse's own help.
- **The order in which the refusals are checked** is as given under `## Approach`. *Reversal:* it
  is not a free choice to begin with — it falls out of where each check already lives — but moving
  the future-month check ahead of the month parse would be one line in `cli` and one test.
- **An entry naming an envelope that is not in `envelopes` contributes to no row, and this item
  adds no check.** *Reversal:* one pass over the entries in `summarise`, one file. This is the same
  answer `WI-0002`'s plan gave to the same question, quoted here so the two do not drift:
  *"an entry naming an absent envelope is invisible, and this item adds no check"*
  [src: tracker/items/WI-0002/artifacts/plan.md]. It cannot arise today: no command removes an
  envelope [src: envel/cli.py:88].
- **Nothing is precomputed.** *Reversal:* this is the documented branch rather than an assumption —
  `ADR-0002` makes a balance derived rather than stored, and precomputing a month would add a
  second source of truth and a `format` change [src: ADR-0008]. Listed here only so that the
  question `refine` routed to `plan` has a visible answer.

**None of these is taken under a standing delegation.** The stakeholder has granted no licence over
a category in this engagement, which is what `refine` recorded on this item
[src: tracker/items/WI-0003/artifacts/refinement-qa.md] and what `scripts/lint-answers --item
WI-0003` reports as zero delegations spent. Each says instead what reversing it costs.

## Decisions and ADRs

| decision | where | branch of the preference order |
|----------|-------|-------------------------------|
| A month is the `on`-else-`at` prefix of an entry, held as a `YYYY-MM` string and compared as one | `ADR-0008` [src: ADR-0008] | **asked of the documents, then decided** — `ADR-0006` already says which field each kind is summed by, and the alternatives are in the ADR |
| Every figure is a filtered sum, so AC3's reconciliation is a property of the arithmetic | `ADR-0008` [src: ADR-0008] | **answered from the documents** — `ADR-0002` already defines a balance that way |
| Nothing is precomputed and no new field is stored | `ADR-0008` [src: ADR-0008] | **answered from the documents** — `ADR-0002`'s shape exists so that a `format` change is not needed |
| The report lives in `envel/summary.py` rather than in `envelopes.py` | `ADR-0009` [src: ADR-0009] | **decided** — the alternative is real and is named in the ADR |
| Month parsing goes in `envel/dates.py` | `## Approach`, interface decision 1 | **answered from the documents** — that module is already the only place text and calendar days meet [src: envel/dates.py:1] |
| `summary` added to the top-level subcommand `metavar` | `## Approach` and step 6 | **answered from the documents** — `WI-0001` AC14 requires it |
| The row's wording, and no header line | `## Assumptions` | **assumed, reversibly** — one format string |
| The order of the three refusals | `## Assumptions` | **read off the existing structure** — a malformed value is raised where it is parsed, as `WI-0002` and `WI-0004` already do |
| An entry naming an absent envelope is invisible | `## Assumptions` | **assumed** — and deliberately the same answer `WI-0002`'s plan gave |

Nothing here settles a disagreement between two of the stakeholder's own recorded answers. One
place looked like it might and does not: `docs/product/vision.md` calls the balance *"the summary's
third column"* [src: EP-001/Q-001], written before `WI-0003/Q-001` added the moved column ahead of
it. Both answers stand — `EP-001/Q-001` is about the balance **carrying over**, which is untouched,
and `WI-0003/Q-001` added a column — and only the ordinal moved. It is an invalidation row for
`implement` rather than a question, and the reason is written here so the repair is not read as
choosing between two things they said.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | `## The parts`, the new `envel/summary.py` row and what it says the module owns | cited-fact | True only if the module exists with that content; a different split while implementing makes the row false |verified-still-true |
| `docs/architecture/overview.md` | `## The parts`: *"`cli` knows about all five modules below it… `envelopes` does not know about `summary`"* | quantified | An import of `summary` from `envelopes`, or a sixth module, falsifies it, and the falsifier is a module the sentence does not name |verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | This change adds a module below `cli`; a `print` or a `sys.exit` in it falsifies the sentence, and the falsifier is a function the sentence does not name |verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: the three beats, *"write the whole store back, atomically, but only if something changed"* | quantified | This change adds the first command that never changes anything; a summary that saved would falsify it |verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"An entry's `at` is when the tool recorded it, on every kind of entry. A spend and a move each carry one field more — `on`"*, and income carrying no date of its own | quantified | This is the first code that reads both fields in one calculation; if `entry_month` used either field differently the sentence would stop describing the tool |verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD`, and a month `YYYY-MM`, and nothing else"* — the clause this execution added | quantified | Accepting any other spelling of a month on `envel summary` falsifies it, and so would parsing a month outside `envel/dates.py` |verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: *"Amounts are printed with exactly two decimal places and no currency symbol"* | quantified | This change prints four new amounts per row; one rendered by anything but `money.format_amount` is the falsifier |verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: output that reports success goes to stdout with exit 0, every refusal to stderr with a non-zero exit | quantified | This change adds one success path, one nothing-to-print path and three refusals — AC13 is the same claim as a criterion |verified-still-true |
| `docs/architecture/overview.md` | `## What is not decided yet`, now naming two items | cited-fact | True only if `WI-0003`'s design really is recorded in `ADR-0008` and `ADR-0009`; it also claims the remaining two build on `ADR-0002` without changing the file's shape, which a `format` change would falsify |verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Says `WI-0001` is the first item to be designed and nothing has been implemented, verified or accepted, which three closed items already made false |owned-by-ending |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` | `## Decision`, points 1 to 5 and the filter table | cited-fact | The code has to match it expression for expression, filter for filter |verified-still-true |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` | `## Consequences`: *"Nothing computes the carried-in figure and nothing checks the identity"* | quantified | Falsified by any line in the summary that computes a carried-in figure or asserts the identity — the sentence's whole claim is that the code does not arrange the reconciliation |verified-still-true |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `## Decision`, the module's contents and the dependency edge it adds | cited-fact | True only if `envel/summary.py` holds those functions and imports in that direction |verified-still-true |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision`: *"`WI-0003`'s net figure for an envelope in a month is then the plain sum of `cents` over that envelope's `move` entries in that month — positive when more arrived than left"* | quantified | Written as a prediction about this item; this change makes it a description, and a moved column computed any other way falsifies it |verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Consequences`: *"`WI-0003` sums a month's spending by `on`, a month's moves by `on`, and a month's income by `at`, with no branch on what a date means"* | quantified | The same: a prediction about this item that this change turns into a description. The clause *"with no branch on what a date means"* is falsified by a branch on `kind` in `entry_month` |verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"`on` is present on every spend entry, including one recorded without `--on`… It is never absent and never null, so a reader never has to fall back to `at`"* | quantified | `entry_month`'s `on`-else-`at` rule depends on it exactly: a spend entry with no `on` would be silently counted in the month it was typed, and the falsifier is a spend the sentence does not name |verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | The fourth column is that sum bounded by a month; falsified if the summary has to special-case a kind to make `left` come out right |verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`entries` is append-only within a run and ordered as written"* | quantified | This change adds a command that should write nothing at all; a summary that sorted, mutated or saved the document falsifies it |verified-still-true |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | The new module handles cents and prints amounts; converting between the two forms anywhere in it falsifies the sentence |verified-still-true |
| `docs/architecture/adr/ADR-0003-store-location.md` | `## Decision` and `## Consequences`: the resolution order, and *"One function in `envel/store.py` resolves the path and nothing else knows about it"* | quantified | This change adds a module that could have wanted the path; a reference to `ENVEL_FILE` or to a store path inside `envel/summary.py` falsifies it |verified-still-true |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | `## Decision`: two entry points *"both reaching the same `main`"* | quantified | This change adds a subcommand, which is the shape that falsifies it — one reachable from `bin/envel` and not from `python3 -m envel`, or the reverse |verified-still-true |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`, the two commands and what lint checks | cited-fact | This change adds one source file and one test file and edits three more; those commands must still cover all of them with no third-party import |verified-still-true |
| `docs/product/vision.md` | `## What it is for`: *"It is why the summary's third column is a balance rather than a monthly remainder"* | cited-fact | The balance is the **fourth** column as of `WI-0003/Q-001`, which added the moved column ahead of it. The sentence's claim — that the column is a balance and not a monthly remainder — is what this item delivers and stays true; the ordinal in it does not. See `## Decisions and ADRs` for why this is a repair rather than a question |to-update |
| `docs/product/vision.md` | `## What it is for`, item 4 of four: *"Looking at a summary of a month"* | cited-fact | Until this item there is nothing behind the sentence; afterwards it describes delivered behaviour and has to match it |verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | Any import added by this change is a new place it could be falsified, and the falsifier would be a module the sentence does not name |verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`, bullets 3 and 5: *"no forecasts, no goals, no recommendations"* and *"no graphical, web or full-screen terminal interface"* | quantified | This change adds the tool's first report; a projected figure or any output that is not plain lines falsifies one of them |verified-still-true |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Says the engagement has just begun and nothing has been refined, designed, built, verified or accepted |owned-by-ending |

## Deliverable documents

`none`. No acceptance criterion of `WI-0003` has a document as its subject; all fourteen are about
what the tool prints, which months it accepts, and the streams and exit codes it uses. `implement`
may therefore write under `docs/` only to close a row of the invalidation set above.

## Binding ADRs

- `ADR-0001` — every figure in the summary is a whole number of cents until `money.format_amount`
  renders it, and only `envel/money.py` converts between the two forms.
- `ADR-0002` — the document's shape, the entry list this change reads and must not write, and a
  balance as the plain sum of `cents` over the entries naming an envelope, which the fourth column
  bounds by a month.
- `ADR-0003` — the store's path, which every criterion of this item is observed against by setting
  `ENVEL_FILE`, and which the new module must not learn.
- `ADR-0004` — the package and the `bin/envel` shim: this change adds no install step and no
  third-party dependency, and both entry points must reach the new subcommand.
- `ADR-0005` — the test and lint commands this change is checked with, both standard library, and
  both must cover the new module and the new test file.
- `ADR-0006` — `on` as the day an event is held against and `at` as when it was recorded, which is
  the whole input to `entry_month`; and its `## Consequences` sentence about what `WI-0003` sums by
  which field.
- `ADR-0007` — the move entry pair, whose two halves are ordinary members of the moved column's sum
  and of the fourth column's.
- `ADR-0008` — this item's own: the month rule, the string form, the filtered sums, nothing
  precomputed, and an entry naming an absent envelope contributing to no row.
- `ADR-0009` — this item's own: the module the report lives in and the direction of its imports.

## Scaffolding

`none`. `envel/summary.py` and `tests/test_summary.py` are named by steps 2 and 8 and are
`implement`'s to write, not this execution's: they carry the behaviour and the assertions. No
command this plan declares needs a file in order to run —
`python3 -m unittest discover -s tests -t .` already discovers `tests/` and already passes
[src: run: python3 -m unittest discover -s tests -t . → exit 0, 119 tests].

## Risks

- **A fourth entry kind would silently break AC3's reconciliation.** The three month-M columns
  partition the entries only while every kind is one of `income`, `spend` and `move`; a fourth
  would land in `left` and in none of the other three. `ADR-0002`'s `kind` field exists so that
  there can be a fourth [src: ADR-0002]. Recorded in `ADR-0008` `## Consequences` as the cost of
  the decision rather than left to be found in a report that does not add up, and there is nothing
  for this item to do about it beyond writing it down.
- **Income's month is a UTC month and a spend's is a local one.** `at` is UTC and `on` is the
  machine's local calendar day [src: ADR-0006], so on a machine well east or west of UTC, income
  typed late on the last evening of a month can fall in the next one. It is a consequence of a
  delivered decision that `ADR-0006` records as **correct**, no criterion of this item reaches it,
  and step 2 must not try to convert one into the other. The risk is that somebody implementing
  `entry_month` "fixes" it.
- **Getting the sign of the spent column wrong.** A spend's `cents` is stored negative
  [src: ADR-0006], the column is printed positive, and AC3's identity **subtracts** it. Step 3
  states the negation and step 3's afterwards names the four integers, so the test that catches it
  is written from the criterion rather than from the code.
- **Reading `today` twice.** `dates.this_month()` is consulted for the default month (step 6) and
  for the future check (step 4). They are two calls a fraction of a second apart and could straddle
  a month boundary, which would refuse the very month it had just defaulted to. Step 4 compares
  against `this_month()` and step 6 defaults to it; a run at exactly midnight on the first could
  see them differ. The cost is one refused invocation that succeeds when retried, and the
  alternative — threading one month through — is worth doing only if `implement` finds it free.
  Named so the choice is visible rather than discovered.
- **The `metavar` again.** `WI-0004` carried this same risk: adding a subcommand without adding it
  to the top-level `metavar` leaves the usage line listing five when the tool has six, falsifying a
  delivered criterion of `WI-0001` [src: WI-0001 AC14 "print to stderr a usage message that lists
  the subcommands the tool does have"] without failing any criterion of this item. Step 6 names it
  and step 9 asks for the test `WI-0004` already wrote for its own case
  [src: tests/test_cli.py:722].

## Out of scope for this item

- Any period other than a month, a total line, a listing of individual spends, projecting forward,
  colour, and comparison between months [src: WI-0003].
- Correcting a recorded spend so a past summary changes [src: WI-0005], and looking up the spends
  against one envelope [src: WI-0006]. Both are their own items and neither is read here.
- Any change to `envel add` [src: WI-0003 AC8 "`envel add` is unchanged by this item"], to
  `envel spend`, or to `envel move`. This item reads what they write and writes nothing.
- Removing an envelope, which no command does, and which is why an entry naming an absent envelope
  cannot arise [src: tracker/items/WI-0002/artifacts/plan.md].
