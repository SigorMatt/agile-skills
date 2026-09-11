# Plan — WI-0006 Look up what has been recorded against an envelope

## Problem

The tool can say what an envelope holds and what a month looked like in four figures per envelope,
and it cannot show the entries those figures are made of. The stakeholder wants to read them back:
*"when I am checking a month against the statement I need to see what is behind an envelope's
balance"* [src: WI-0006/Q-001]. This item adds one command, `envel entries`, which lists a
calendar month's income, spends and moves — the current month unless `--month` names another, one
envelope's if one is named and the envelopes together if none is
[src: WI-0006 AC1 "The command is `envel entries`"]. Each line carries a **reference**, a number
the person reads off and types back, which `WI-0005` will take as the argument to `envel fix` and
`envel remove` [src: WI-0005/Q-001].

Three constraints shape it. The listing has to add up when an envelope is named — *"a list I
cannot add up costs me an evening whichever report it is on"* [src: WI-0006/Q-004] — which is what
AC9's opening and closing lines are for. The reference is counted once across everything recorded
rather than within an envelope, and it stays with its entry [src: WI-0005/Q-008], which the store
as delivered cannot do because an entry has no identity [src: ADR-0002]. And the monthly summary
is not to change at all [src: WI-0006 AC14 "prints exactly what it printed before this item"].

## Approach

Three parts, in the order they depend on each other.

**The reference is stored, not derived** — `ADR-0010`. An entry gains `ref`, the document gains
`next-ref`, `store.FORMAT` goes to 2, and a document read at format 1 is upgraded in memory. The
alternative — numbering entries by their position when the listing runs — is correct for this item
alone and breaks silently the first time `WI-0005` removes an entry. The ADR is where that is
argued; this plan only builds it.

**The listing is a report, so it lives with the reports.** `envel/summary.py` already owns
reporting, and the overview says so in the words *"the reports: a month's four figures per
envelope, and the rows they print"* [src: docs/architecture/overview.md]. A second report over the
same entry log, keyed by the same month rule [src: envel/summary.py:27], belongs beside the first;
a new `envel/entries.py` was the alternative and was rejected because it would need to import
`summary` for the one shared expression and would make three places a reader looks for what the
tool does, which `ADR-0009` already names as the cost of two. The module's docstring is widened to
say it holds the reports rather than the summary.

**The arithmetic is the arithmetic that already exists.** An envelope's balance is the sum of
`cents` over its entries [src: ADR-0002]; `summary.figures` bounds that sum by month to get the
figure it calls `left` [src: envel/summary.py:38]. AC9's closing figure is exactly that sum for
the month being listed and its opening figure is the same sum over the months before it, so the
reconciliation AC9 asks for is a property of the sums rather than something the listing arranges —
which is the same thing `ADR-0008` says about the summary's reconciliation. Nothing new computes a
carried-in figure by subtraction.

Nothing below `envel/cli.py` prints or exits, as everywhere else in this tool
[src: docs/architecture/overview.md]; `list_entries` returns `envelopes.Ok` or
`envelopes.Refusal`, the two types `cli` already dispatches on [src: envel/cli.py:136], so the
command line gains a subparser and a branch and no new shape.

## Steps

1. **`envel/store.py` — the document's shape.** Set `FORMAT = 2`. `empty_store()` returns
   `{"format": 2, "envelopes": [], "entries": [], "next-ref": 1}`. `load()` accepts a document
   whose `format` is 1 or 2 and refuses anything else with the message it already uses; a
   document at format 1 is upgraded before it is returned — each entry in list order takes the
   next `ref` from 1 upwards, `next-ref` is set one past the last, and `format` becomes 2. The
   upgrade happens in memory only. Afterwards: `store.load` on a file written by the delivered
   code returns entries each carrying a `ref`, the file on disk is byte-identical, and
   `store.load` on a file whose `format` is 3 still raises `StoreError`.
2. **`envel/envelopes.py` — taking a reference.** Add one module-level helper that, given the
   document, returns the next reference and advances `next-ref`; call it at each of the four
   places an entry is appended — `add_income`, `record_spend`, and both halves of `move` — and put
   the number on the entry as `ref`. `move` takes two consecutive numbers, the envelope the money
   left first. Afterwards: `envel add`, `envel spend` and `envel move` each leave every entry in
   the document carrying a distinct `ref`, and the document's `next-ref` is one higher than the
   highest of them.
3. **`envel/summary.py` — the listing.** Widen the module docstring to say it holds this
   project's reports and name both. Add, beside `entry_month` and `figures`:
   - a function returning the entries of one month, optionally restricted to one envelope,
     ordered by the date `entry_month`'s rule gives them and, within a date, by the order the
     `entries` list already holds them [src: ADR-0002];
   - a function returning the balance of one envelope over the months **before** a given month,
     which is the same filtered sum `figures` computes for `left` with the bound moved back one
     month;
   - a function rendering one entry as a line: its `ref`, its date, its kind — `income`, `spend`,
     `moved in` or `moved out`, the last two read off the sign of `cents` [src: ADR-0007] — the
     envelope, the amount through `money.format_amount` and nothing else, and the description
     where the entry has one;
   - `list_entries(store, name, month)` returning `Ok` or `Refusal`: refuse a month later than
     the month today falls in, and refuse a `name` no envelope has, in that order; with a `name`,
     print the opening line, the entry lines, a line saying there is nothing in the month where
     there are none, and the closing line; with no `name`, print the entry lines alone and a
     single line saying so where there are none.
   Afterwards: `list_entries` is a function of (document, name, month) that changes nothing and
   returns `changed` false, and every amount in its lines has been through `money.format_amount`.
4. **`envel/cli.py` — the command line.** Add an `entries` subparser: an optional positional
   `name`, and `--month` taking `YYYY-MM`. Add `entries` to the subcommand metavar list and to the
   dict `build_parser` returns, so a wrong argument count is reported by this subcommand's own
   parser. Dispatch to `summary.list_entries`, parsing `--month` with `dates.parse_month` when it
   is given and using `dates.this_month()` when it is not — which is where an unreadable month is
   refused, as it already is for `envel summary` [src: envel/cli.py:126]. Afterwards:
   `envel entries --help` prints this subcommand's usage, `envel --help` lists `entries`, and
   `envel entries groceries extra` prints `usage: envel entries …` to stderr and exits non-zero.
5. **Tests for the store and the reference.** In `tests/test_store.py`: a format-1 document with
   three entries loads with references 1, 2 and 3 and `next-ref` 4, the file is unchanged on disk,
   and loading it twice gives the same three numbers; a `format` of 3 is still refused. In
   `tests/test_envelopes.py`: income, a spend and a move over one document take four distinct
   consecutive references; a move's two entries take two of them with the outgoing side first.
6. **Tests for the listing.** A new `tests/test_entries.py` exercising `list_entries` as a
   function: AC5's income-dated-by-`at` and spend-dated-by-`on` pair; AC6's move seen from each
   envelope and from neither; AC8's ordering including two entries on one date and the same call
   twice; AC9's worked case — an envelope holding 50.00 at the end of July with 20.00 spent and
   30.00 moved in during August, opening 50.00, closing 60.00, lines summing to +10.00, and the
   closing figure equal to `envelopes.balance` when the month is the current one; AC10's absence
   of an opening and closing figure; AC11's two empty cases; AC12's unknown envelope including the
   case-folded match [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"].
7. **Tests for the command line.** In `tests/test_cli.py`, alongside the cases the other
   subcommands already have: the four invocations of AC1; AC13's five refused months; AC15's
   streams and exit codes for each refusal and each success, and the three wrong shapes it names.
8. **AC14, which is read as well as run.** Re-read `WI-0003` AC1 through AC14 against what
   `envel entries` does and record the verdict per criterion in `impl-report.md`, with
   `tests/test_summary.py` and `test_cli.py`'s summary cases passing unchanged as the evidence
   rather than as the definition. Where no test exercises `envel summary` and `envel entries` over
   one store, add one that does — a store listed and then summarised, with the summary's output
   asserted against what it printed before this item.
9. **`docs/architecture/overview.md` is already updated to v7 by this execution** — the
   `envel/summary.py` row now names both reports, `## The data` has a paragraph for `ref`,
   `next-ref`, the `format` at 2 and the in-memory upgrade, and `## What is not decided yet` drops
   `WI-0006` and says what `ADR-0010` does to `ADR-0002`'s prediction. What is left for
   `implement` is to **close every row of the invalidation set below against the code it wrote**,
   including those three, and to repair any of them the code makes false — a module split it
   changed, a sentence about dependency direction an import breaks. The `## Engagement state`
   section is disposed `owned-by-ending` and nothing in this item may write it
   [src: toolkit: doc-header.md §4a "an engagement-state sentence"].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 4 | `tests/test_cli.py`: the four invocations — bare, with an envelope, with `--month`, with both — each exit 0 and print a listing, the first two covering the month today falls in |
| AC2 | 3, 6 | `tests/test_entries.py`: a store holding an income, a described spend, an undescribed spend and a move; each line asserted to carry a reference, a date, a kind, the envelope and an amount matching `\d+\.\d\d`, with the description present on one line and absent on the other |
| AC3 | 1, 2, 6 | `tests/test_envelopes.py`: entries recorded into two envelopes carry distinct references that do not restart at the second envelope. `tests/test_entries.py`: no two lines of one listing carry the same reference |
| AC4 | 1, 2, 5 | `tests/test_entries.py`: a listing is read, one more spend is recorded, the listing is read again, and every reference from the first read still names the same entry while the new one carries a reference none of them had |
| AC5 | 3, 6 | `tests/test_entries.py`: an income with only an `at`, and a spend with `on` a day in the previous month, appear in the listings of different months and under those two dates |
| AC6 | 3, 6 | `tests/test_entries.py`: a move listed from the source envelope, from the destination, and with no envelope named — one line, one line, and two lines with the same date and opposite directions |
| AC7 | 3, 4, 6 | `tests/test_entries.py`: the same month listed before and after an entry is recorded in a later month prints the same lines |
| AC8 | 3, 6 | `tests/test_entries.py`: four entries whose dates and recording order are known produce lines in that order, and two calls over one document produce identical lists |
| AC9 | 3, 6 | `tests/test_entries.py`: the worked case of step 6 — opening 50.00, closing 60.00, the lines between summing to +10.00 — and the closing figure equal to `envelopes.balance` for the current month |
| AC10 | 3, 6 | `tests/test_entries.py`: a listing with no envelope named contains no opening or closing line, and every entry line names its envelope |
| AC11 | 3, 6, 7 | `tests/test_entries.py`: an existing envelope with nothing in the month prints its opening and closing lines with a nothing-in-between line; a month in which nothing was recorded prints one line. `tests/test_cli.py`: both exit 0 with an empty stderr |
| AC12 | 3, 7 | `tests/test_cli.py`: `envel entries nosuch` writes to stderr naming `nosuch`, exits non-zero and prints nothing on stdout; `envel entries GROCERIES` prints what `envel entries groceries` prints |
| AC13 | 4, 7 | `tests/test_cli.py`: the five months AC13 names, each on stderr with a non-zero exit and an empty stdout |
| AC14 | 3, 8 | `tests/test_cli.py`: a store listed with `envel entries` and then summarised, the summary's output asserted against what it printed before this item; plus the per-criterion read of `WI-0003` AC1–AC14 recorded in `impl-report.md`, with `tests/test_summary.py` passing unchanged as its evidence |
| AC15 | 3, 4, 7 | `tests/test_cli.py`: each refusal named in AC15 checked for an empty stdout, a non-empty stderr and a non-zero exit; each success for an empty stderr and exit 0; and the three wrong shapes printing `usage: envel entries` |

## Assumptions

- **The listing's line is one line per entry, labelled in the line rather than under a header**,
  in the shape `summary.row` already uses [src: envel/summary.py:70]. Reversing it means changing
  one function and its tests; no stored data and no interface. **Under delegation:**
  `WI-0003/Q-004` — argument style and the naming of commands and options, which `refine` spent on
  this item for the command's arguments and which covers the wording of what it prints in the same
  way it covered `envel summary`'s.
- **The opening and closing lines of AC9 are lines of the listing rather than a separate report**,
  printed first and last. Reversing it is the same one function. **Under delegation:**
  `WI-0003/Q-004` — as above.
- **`next-ref` is the key's name and `ref` the entry's.** Reversing it is a rename in two modules
  and the format-1 upgrade, before the stakeholder has a file carrying either; afterwards it would
  need a third `format`. Named here rather than in `ADR-0010` because the ADR's decision is that
  the number is *stored and counted*, and the spelling of the two keys is not part of it.
- **A move's outgoing side takes the lower of its two references.** Reversing it is one line.
  Nothing observable depends on it: AC6 asserts that both lines exist with opposite directions,
  not which number is smaller.

## Decisions and ADRs

- **`ADR-0010` — an entry carries its own reference, and the document counts them.** The decision
  this item forces and the only one on it that is expensive to undo. Three options are argued
  there: a position computed at read time, a stored `ref` with `max + 1`, and a stored `ref` with
  a counter. Taken by **deciding**, branch 3 of the preference order is not engaged — the record
  is not silent and the stakeholder already answered what the number counts [src: WI-0005/Q-008];
  what they did not answer, and could not, is how the file keeps that promise.
- **The listing goes in `envel/summary.py`.** Answered **from the documents**: the overview's
  module table already says that module owns *"the reports"*
  [src: docs/architecture/overview.md], and `ADR-0009` names the distinction it is drawn on —
  `envelopes` changes things, `summary` reports on them. The alternative, a new
  `envel/entries.py`, is recorded in `## Approach` with why it was rejected. No ADR: the answer
  follows from a cited sentence, and an ADR here would pad the trail rather than record a choice.
- **The opening figure is a filtered sum, not a subtraction.** Answered **from the documents**:
  `ADR-0008`'s consequence says *"Nothing here computes a carried-in figure and nothing here
  checks the identity"*, and computing AC9's opening line as closing-minus-the-month would make
  that sentence false. The same bound `figures` uses for `left`, moved back one month, keeps it
  true.
- **The two month refusals are `envel summary`'s, applied here.** Answered **from the record**:
  `refine` took them under no delegation and recorded where a disagreement lands
  [src: WI-0006 AC13 "A month this command will not accept is refused"]. `plan` builds them as
  written and puts the parse in `envel/cli.py` so that months are parsed in `envel/dates.py` and
  nowhere else [src: ADR-0008].
- **Nothing was asked of the human.** No decision on this item is irreversible *and* unrecorded:
  the one irreversible decision, `ADR-0010`, implements a choice they already made, and its
  alternatives differ in how the file keeps their promise rather than in what the promise is.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | `## The parts`: the `envel/summary.py` row, *"the reports: a month's four figures per envelope, and the rows they print"* | cited-fact | The module gains a second report; the row as written describes only the first | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`: *"`cli` knows about all five modules below it… `envelopes` does not know about `summary`"* | quantified | This change edits four of the six modules; an import added in the wrong direction falsifies it, and the falsifier is an import the sentence does not name | verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | This change adds a report function and a store upgrade below `cli`; a `print` or a `sys.exit` in either falsifies it | verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: the three beats, *"write the whole store back, atomically, but only if something changed"* | quantified | The format-1 upgrade changes a document in memory during the **read** beat; if it also wrote, the sentence would be false and a read-only command would rewrite the stakeholder's file | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"One JSON document holding the envelopes and an append-only list of dated entries; a balance is the sum of an envelope's entries rather than a stored number"* | cited-fact | The document gains `next-ref` and each entry gains `ref`; the sentence does not become false but stops describing the file | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"An entry's `at` is when the tool recorded it, on every kind of entry. A spend and a move each carry one field more"* | quantified | After this change an entry carries `ref` as well, so *"one field more"* is a count of fields that this change moves | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"A move between two envelopes is stored as **two** entries of kind `move`… Nothing in the file links the two halves of a move to each other"* | quantified | The two halves now carry consecutive references, which is the nearest thing to a link the file has had; whether the sentence survives is a read somebody has to make rather than assume | to-update |
| `docs/architecture/overview.md` | `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD`, and a month `YYYY-MM`, and nothing else"*, and *"both are parsed in `envel/dates.py` and nowhere else"* | quantified | This change adds the second command that takes a month; parsing `--month` anywhere but `envel/dates.py` falsifies the second clause | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: *"Amounts are printed with exactly two decimal places and no currency symbol"* | quantified | The listing prints an amount on every line plus two balances; one rendered by anything but `money.format_amount` is the falsifier | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: success to stdout with exit 0, every refusal to stderr with a non-zero exit | quantified | This change adds two success paths and three refusals; AC15 is the same claim written as a criterion | verified-still-true |
| `docs/architecture/overview.md` | `## What is not decided yet`: *"`ADR-0002` is the decision the remaining two are expected to build on without changing the file's shape, and `ADR-0006`, `ADR-0007` and `ADR-0008` have each now extended it once without doing so"*, and the clause naming `WI-0006` | cited-fact | `ADR-0010` changes the file's shape and the `format`, which is precisely what this sentence predicts will not happen; and `WI-0006` leaves the undecided list | verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Says `WI-0001` is the first item to be designed and that nothing has been implemented, verified or accepted, which four closed items already made false; and that no document has been checked against running code | owned-by-ending |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: the worked document, and *"`format` is an integer this tool checks on load, so a future change has somewhere to branch"* | cited-fact | The branch this sentence anticipated is now taken; the worked document shows neither `ref` nor `next-ref` | to-update |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | The listing must not sort, mutate or save the document, and AC9's two balances must be that same sum bounded by month; a special case on `kind` to make either come out right falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Consequences`: *"`WI-0002` adds an entry kind and a field, and `WI-0003` filters income by `at`… neither needing a format change"* | cited-fact | True of those two items and written as a prediction about the shape of later work; this item **does** need a format change, and the sentence should be read against that rather than left as though nothing had happened | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Corrections`: the `WI-0002` entry's closing sentence, *"The claim that neither item needs a format change survives and is true: `envel/store.py` still reads and writes `FORMAT = 1`"* | cited-fact | Found by `implement` on `WI-0006`, not by `plan`: this change sets `FORMAT = 2`, so the observation is no longer true of today's code. Added to the set before it was disposed, per the rule that a document found mid-change is written down first | verified-still-true |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `## Decision`: *"`envel/summary.py` holds the summary"*, and `## Consequences`: *"there are now two places a reader might look for 'what the tool does'"* | cited-fact | The module gains a second report, so what it holds is no longer only the summary | to-update |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` | `## Consequences`: *"Nothing computes the carried-in figure and nothing checks the identity"* | quantified | AC9 puts a carried-in figure on the screen; the sentence survives only if it is the same filtered sum with the bound moved back, and is falsified by a subtraction | to-update |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision` and `## Consequences`: the two-entry shape and what nothing links | quantified | AC6 shows a move from either side and `WI-0005` AC13 will refuse a correction aimed at one; consecutive references are new information in the file about the pair | to-update |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"`on` is present on every spend entry… It is never absent and never null, so a reader never has to fall back to `at`"* | quantified | AC5's date is `entry_month`'s rule applied to a line rather than a sum; a spend entry with no `on` would be listed under the day it was typed, and the falsifier is a spend the sentence does not name | verified-still-true |
| `docs/architecture/adr/ADR-0003-store-location.md` | `## Decision` and `## Consequences`: *"One function in `envel/store.py` resolves the path and nothing else knows about it"* | quantified | The format-1 upgrade is new code in `store.py`; a store path referenced from `summary.py` would falsify it | verified-still-true |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | The listing renders an amount per line and two balances; a conversion written anywhere in `summary.py` falsifies the sentence | verified-still-true |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | `## Decision`: two entry points *"both reaching the same `main`"* | quantified | A new subcommand is the shape that falsifies it — reachable from `bin/envel` and not from `python3 -m envel`, or the reverse | verified-still-true |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`: the two commands and what lint checks | cited-fact | This change edits four source files and three test files and adds one; both commands must still cover them with no third-party import | verified-still-true |
| `docs/product/vision.md` | `## What it is for`: *"That reference is one number counted once across everything recorded… so a number on its own names at most one entry whichever envelope that entry sits in"* and *"the number an entry is given stays that entry's"* | quantified | Until this item nothing stands behind either sentence; afterwards they describe delivered behaviour, and a duplicate or a reused number falsifies them | verified-still-true |
| `docs/product/vision.md` | `## What it is for`: the listing paragraph — what it shows, the month it covers, the optional envelope, *"so that the lines add up to the balance"* | cited-fact | This item is what the paragraph describes; anything the command does differently makes it false | verified-still-true |
| `docs/product/vision.md` | `## What it is for`: *"An entry is named by a short reference the tool prints and the person types back, read off a listing of an envelope's entries rather than remembered"* | cited-fact | The listing may name no envelope [src: WI-0006/Q-003], so *"of an envelope's entries"* is the clause to read against what is built | to-update |
| `docs/product/vision.md` | `## What it deliberately is not`: *"Not connected to anything: no server, no sync, no bank import, no network"* | quantified | Any import this change adds is a place it could be falsified, and the falsifier is a module the sentence does not name | verified-still-true |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Says the engagement has just begun, that nothing has been refined, designed, built, verified or accepted, and that `EP-001` is suspended awaiting an answer | owned-by-ending |

## Deliverable documents

`none`. No acceptance criterion of `WI-0006` has a document as its subject: AC1 to AC15 are about
what `envel entries` prints, which months and envelopes it accepts, and the streams and exit codes
it uses. `implement` may therefore write under `docs/` only to close a row of the invalidation set
above — which step 9 expects it to do for `docs/architecture/overview.md`.

## Binding ADRs

- `ADR-0001` — amounts are integer cents, and `envel/money.py` is the only place the two forms
  meet. Every amount the listing prints goes through `format_amount` and no other conversion is
  written.
- `ADR-0002` — the store is a JSON entry log with a `format` to branch on, the entries append-only
  and ordered as written, and a balance the sum of `cents`. This change takes the branch the
  `format` sentence anticipated, and AC8's tie-break and AC9's two balances are both that order
  and that sum.
- `ADR-0003` — the store's path is resolved by one function in `envel/store.py` and nothing else
  knows about it. The upgrade added in step 1 stays inside that module and the listing never sees
  a path.
- `ADR-0004` — `python3 -m envel` and `bin/envel` both reach the same `main`, so the new
  subcommand is reachable from both without either being edited.
- `ADR-0005` — the test and lint commands are standard library only; the new test module and the
  edited ones import nothing outside it.
- `ADR-0006` — a spend carries `on`, income does not, and no reader falls back to `at` for a
  spend. AC5's date is that rule applied to a line.
- `ADR-0007` — a move is two entries with opposite `cents` and the same `on` and `at`. AC6 is that
  shape shown from either side, and step 2 gives the two halves consecutive references.
- `ADR-0008` — a month is the string `YYYY-MM` compared as a string, every figure is a filtered
  sum, and months are parsed in `envel/dates.py` alone. AC7's month rule, AC9's two balances and
  step 4's `--month` parse are each bound by it.
- `ADR-0009` — reporting lives in its own module, returning `Ok` or `Refusal` so that `cli` gains
  no new branch shape. The listing is put in that module for the reason the ADR gives.
- `ADR-0010` — an entry carries its own reference and the document counts them. Written by this
  execution; AC3 and AC4 are what it exists for.

## Scaffolding

`none`. Both declared commands already run in this project — `python3 -m unittest discover -s
tests -t .` and `python3 -m compileall -q envel tests`
[src: run: python3 -m unittest discover -s tests -t . → exit 0, 176 tests] — and `tests/` already
carries its `__init__.py`, so no file outside `tracker/` and `docs/` was created to make a gate
command executable.

## Risks

- **The format-1 upgrade is the step that touches the stakeholder's existing file.** If it wrote
  to disk, a read-only command would rewrite a file the person had not asked to change, and an
  interrupted `envel entries` could leave them worse off than before they ran it. Step 1 upgrades
  in memory only and `envel/cli.py` saves only when a command reports a change
  [src: envel/cli.py:140]; this is the risk the invalidation set's third-beat row is watching.
- **The reference and the counter can disagree.** `ADR-0010` records that a hand-edited file with
  a low `next-ref` would produce a duplicate reference and that no repair is being built for it.
  If that turns out to matter it is a bug item, not a widening of this plan.
- **AC14 is the criterion most likely to be answered by a test that could not have failed.** The
  summary's tests passing tells you the summary still works; it does not tell you the criteria
  were read. Step 8 asks for the per-criterion read and for a case that exercises both commands
  over one store, because a non-intersecting suite is exactly the shape F-065 is about.
- **`refine` decided AC10, AC13 and AC8 under no delegation**, each recording where a disagreement
  lands. If the stakeholder disputes any of them the cost is one criterion and one test, and the
  design does not move — that is what makes them safe to have built rather than asked about.

## Out of scope for this item

- `envel fix` and `envel remove`. They are `WI-0005`, which depends on this item for the reference
  and is refined and waiting. Nothing in this plan implements a correction or a removal, and the
  reference is stored the way it is precisely so that `WI-0005` inherits its stability rather than
  arranging it.
- Repairing a `next-ref` that a hand edit has left below an existing `ref`. Named as a risk above
  and as a consequence in `ADR-0010`; no criterion asks for it.
- Any change to `envel summary`. AC14 is the criterion that makes its unchangedness observable.
