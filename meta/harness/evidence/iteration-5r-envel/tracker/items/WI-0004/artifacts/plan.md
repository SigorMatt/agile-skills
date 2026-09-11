# Plan — WI-0004 Move money between envelopes

## Problem

`envel` refuses an overspend rather than letting an envelope go negative
[src: EP-001/Q-002], so the person's route out of a short envelope is to take the money from one
they have decided it can come from. Nothing does that today. This item adds one subcommand,
`envel move <from> <to> <amount>` with an optional `--on <date>`, which takes an amount out of one
envelope and puts it into another, holds the move against a day the way a spend is held
[src: WI-0004 AC1 "There is an `envel` command that moves a given amount from one named envelope to"], refuses the four things the criteria name, and prints a line naming both
envelopes and what each now holds.

The constraints are the ones this project already runs under: whole cents only [src: ADR-0001],
one JSON document read and written whole [src: ADR-0002], the store found through `ENVEL_FILE` or
the XDG directory [src: ADR-0003], the standard library and nothing else [src: ADR-0005], and a
date written `YYYY-MM-DD` [src: ADR-0006]. One further constraint comes from an item that does not
exist yet: the stakeholder asked for a move to be kept out of *spent* and shown as its own net
figure per envelope per month [src: WI-0003 AC2 "The moved figure is one net number, positive when
more arrived than left"], so what this item stores has to be something `WI-0003` can filter and
sum.

## Approach

A move is two entries of kind `move`, one per envelope, with opposite signs and a shared `on` and
`at`. `ADR-0007` [src: ADR-0007] records that decision and why the one-entry alternative was
rejected: an entry names one envelope, and a balance is the plain sum of `cents` over the entries
naming it [src: ADR-0002], so an entry naming two envelopes would put a special case in the one
function every command depends on.

That choice is what makes most of this item fall out rather than be arranged. AC2 — the source
down by exactly the amount, the destination up by exactly it, and no other envelope changed — is a
consequence of appending two entries and touching nothing else; no code computes it.

The rest follows the shape the tool already has. `envel/envelopes.py` gains one operation that is
a pure function of (document, arguments) returning `Ok` or `Refusal` and printing nothing;
`envel/cli.py` gains one subparser and one dispatch branch, and remains the only module that
writes to a stream or chooses an exit code. No new module is needed: a move parses an amount
through `envel/money.py` and a date through `envel/dates.py`, both of which already exist for
exactly this.

**Three interface decisions**, none of them implementation:

1. **The operation is `envelopes.move(store, source, destination, cents, on)`**, with `cents`
   positive as the user typed it, mirroring `record_spend`'s signature
   [src: envel/envelopes.py:108]. It returns `Ok` carrying the new document and one line, or
   `Refusal`.
2. **The subparser's two envelope arguments are `dest="source"` and `dest="destination"` with
   `metavar="from"` and `metavar="to"`.** `from` is a Python keyword, so `arguments.from` will not
   parse; the metavars are what keep the usage line reading `envel move from to amount`, which is
   what the person mistyping it needs. This is stated here rather than discovered.
3. **The subcommand list in the top-level parser's `metavar` gains `move`.** It is currently
   `{new,add,list,spend}` [src: envel/cli.py:26], and `WI-0001` requires the usage message to list
   the subcommands the tool has [src: WI-0001 AC14 "print to stderr a usage message that lists the
   subcommands the tool does have"]. Adding a subcommand without adding it here would falsify a
   delivered criterion of another item.

**The order of the refusals** is settled here, as `WI-0002`'s was [src: WI-0002], because more
than one can apply to the same line and the criteria each promise a particular message. The order
is: source envelope missing, destination envelope missing, the two are the same envelope, the
amount is not positive, the date is in the future, the source does not hold enough. The reasoning:
the two existence checks lead, so that a message naming an envelope is always available — which is
what `WI-0002` decided for the same reason and what AC4 promises; the same-envelope check joins
them because it is the third question about the names rather than about the amount or the date;
and the funds check is last because it is the only one whose message has to quote a balance, which
is only meaningful once the envelope is known to exist. Within the two existence checks the source
is reported first, so `envel move nosuch alsonosuch 10` names `nosuch`.

**Two refusals happen before the operation is reached at all**, and that is the existing structure
rather than a new decision: a malformed amount and a malformed date are raised by
`envel/money.py` and `envel/dates.py` as they are parsed in `envel/cli.py`
[src: envel/cli.py:81], before any document is examined. So `envel move nosuch fun 1 --on 28/8`
reports the date, not the envelope. `envel spend` behaves the same way today, and AC7 asks only
that a malformed date be refused with nothing moved.

## Steps

1. **`envel/envelopes.py` — add `move(store, source, destination, cents, on)`**, below
   `record_spend`. It performs the six refusals in the order given above, each returning a
   `Refusal` whose message names what the criteria require: the missing envelope's name (AC4), the
   envelope's name for a same-envelope move (AC11), the amount for a non-positive one (AC10), the
   date for a future one (AC8), and the source's name with what it holds for an overdraw (AC3). On
   success it deep-copies the document, computes `at` once with `now()` and reuses the already
   formatted `on`, appends the two `move` entries of `ADR-0007` [src: ADR-0007] using the
   envelopes' stored names rather than what was typed, and returns `Ok(store, [line],
   changed=True)`. **Afterwards:** `python3 -c "from envel import envelopes"` imports, and the
   function returns `Refusal` or `Ok` without printing or exiting.
2. **`envel/envelopes.py` — the success line.** One line containing, in this order, the amount
   moved, the source's stored name, what the source now holds, the destination's stored name, and
   what the destination now holds — reading in the direction the money went, so a reversed pair is
   visible in the same breath (AC9). Amounts are formatted by `money.format_amount` and by nothing
   else [src: ADR-0001]. **Afterwards:** the line contains all four values and names the two
   envelopes in source-then-destination order.
3. **`envel/cli.py` — add the `move` subparser.** Three positionals — `source` with
   `metavar="from"`, `destination` with `metavar="to"`, and `amount` — plus
   `--on` with `metavar="YYYY-MM-DD"` and `default=None`, matching `spend`'s
   [src: envel/cli.py:50]. Add `move` to the subcommand list in the top-level `metavar`.
   **Afterwards:** `envel` with no subcommand prints a usage line naming `move`, and
   `envel move groceries fun 20 extra` prints `move`'s own usage to stderr and exits non-zero
   through the existing `parse_known_args` path [src: envel/cli.py:60].
4. **`envel/cli.py` — add the dispatch branch**, beside the `spend` branch, calling
   `envelopes.move` with `money.parse_amount(arguments.amount)` and
   `dates.parse_date(arguments.on) if arguments.on else dates.today()`. Nothing else in `main`
   changes: the existing `except` already turns `AmountError` and `DateError` into a message on
   stderr and exit 1, and the existing `Refusal` branch already does the same for a refusal.
   **Afterwards:** `envel move a b 10` runs end to end against a store at `ENVEL_FILE`.
5. **`tests/test_envelopes.py` — add a `Move` class** exercising the operation directly, with the
   `with_envelope` helper this file already has [src: tests/test_envelopes.py:10]: both entries
   appended with the right signs and the same `on` and `at`; the stored names used rather than the
   typed capitalisation; each of the six refusals in isolation; and one test that fixes the order,
   asserting that a line which is wrong in two ways reports the earlier refusal — the shape
   `test_the_envelope_is_checked_before_the_amount_and_the_date` already has for `record_spend`
   [src: tests/test_envelopes.py:242]. **Afterwards:** these tests pass and fail if the order
   changes.
6. **`tests/test_cli.py` — add a `Move` class** running the tool as a separate process with
   `ENVEL_FILE` pointing at a scratch file, in the shape the `Spend` class already uses
   [src: tests/test_cli.py:274]: the success line's four values; the listing before and after; a
   move surviving into a later invocation; the stored `on` with and without `--on`; the three
   malformed date forms and one accepted one; a future date and today; each refusal's stream and
   exit code; and the four wrong-argument-count lines including `envel move groceries fun 20
   extra`. **Afterwards:** `python3 -m unittest discover -s tests -t .` exits 0.
7. **`docs/architecture/overview.md`** — already updated by this execution to version 5 (the
   `envelopes.py` row, `## The data` on what a move stores, and `WI-0004` leaving `## What is not
   decided yet`). `implement` touches it again only to close a row of the invalidation set below.
   **Afterwards:** nothing for `implement` to do here unless a row says so.

**A note on who does what.** Ticking this item's acceptance criteria is `verify`'s and not
`implement`'s [src: toolkit: work-item.md §2 "the checkbox is verify's"]; no step above asks for
it. `implement` writes under `docs/` only to close a row of the invalidation set or to produce a
deliverable document, and this item has none.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 1, 3, 4 | `tests/test_cli.py` `Move`: run `envel move groceries fun 20 --on 2026-08-28` against a scratch `ENVEL_FILE` and read the store — two `move` entries, both carrying `on: "2026-08-28"` |
| AC2 | 1 | `tests/test_cli.py` `Move`: the listing before and after — source down by exactly 20.00, destination up by exactly 20.00, every other line byte-identical; and `tests/test_envelopes.py` `Move` on the document directly |
| AC3 | 1 | `tests/test_envelopes.py` `Move`: a move larger than the source holds returns `Refusal`, the message contains the source's name and its balance, and the document is unchanged; `tests/test_cli.py` `Move` for the stream and exit code |
| AC4 | 1 | `tests/test_envelopes.py` `Move`: `move` with a missing source, and again with a missing destination, each refused with that name in the message and nothing appended |
| AC5 | 1, 4 | `tests/test_cli.py` `Move`: the move in one subprocess, `envel list` in a second — the amounts are as the move left them |
| AC6 | 1, 4 | `tests/test_cli.py` `Move`: one move with no `--on` and one with `--on 2020-01-01`; the store's two moves carry today's date and `2020-01-01` respectively |
| AC7 | 4 | `tests/test_cli.py` `Move`: `--on` given `28/8`, `08-28` and `yesterday` each exit non-zero with a message and leave the listing unchanged; `--on 2026-08-28` is accepted |
| AC8 | 1 | `tests/test_envelopes.py` `Move`: tomorrow refused with a message naming the date, today accepted; `tests/test_cli.py` `Move` for the stream and exit code |
| AC9 | 2 | `tests/test_cli.py` `Move`: stdout of a successful move contains both envelope names, the amount moved, and the amount now in each, and the exit code is 0 |
| AC10 | 1 | `tests/test_envelopes.py` `Move`: `0` and a negative amount each refused with a message and nothing appended; `tests/test_cli.py` `Move` for the stream and exit code |
| AC11 | 1 | `tests/test_envelopes.py` `Move`: `groceries` to `groceries` and `groceries` to `Groceries` each refused with the envelope's name in the message and nothing appended |
| AC12 | 1, 2, 3, 4 | `tests/test_cli.py` `Move`: one test capturing stdout, stderr and the exit code for the case each named criterion specifies — refusals at AC3, AC4, AC7, AC8, AC10, AC11 and AC13; successes at AC1, AC2, AC6 and AC9 — so the criterion's read of those criteria has an executable case behind every one of them, which is what AC12 asks for |
| AC13 | 3 | `tests/test_cli.py` `Move`: `envel move`, `envel move groceries`, `envel move groceries fun` and `envel move groceries fun 20 extra` each print a usage line for `move` to stderr, exit non-zero, and leave the listing unchanged |

## Assumptions

- **The two entries of one move are not linked to each other**, so nothing can later identify the
  pair. *Reversal:* add one field, written in `envelopes.move` and read wherever the pair is
  wanted — one file, no `format` change, no migration to read the file. The honest cost is that
  moves recorded before the change would not carry it, so only newer ones could be paired. Nothing
  in this epic needs the pair: `WI-0003` wants a net figure, `WI-0005` is scoped to spends
  [src: WI-0005], and `WI-0006` is scoped to the spends recorded against an envelope
  [src: WI-0006]. Recorded in `ADR-0007` [src: ADR-0007] as well, because it is the cost of the
  decision rather than a detail of it.
- **The order of the six refusals** is as given under `## Approach`. *Reversal:* one function, one
  file, and the test that fixes the order. No stored data and no interface changes. It is
  `refine`'s question routed here [src: WI-0004] and it is taken on the precedent `WI-0002` set.
- **A move's balance check reads the balance now, not the balance on the day given.** *Reversal:*
  one comparison in one function. This is not a free choice: `refine` recorded it as the delivered
  spend's own behaviour [src: WI-0002 AC5 "Recording a spend larger than the amount currently in
  the envelope is refused"] and the stakeholder asked for a move *"datable, same as a spend"*
  [src: WI-0004/Q-001].

**None of these is taken under a standing delegation.** The stakeholder has granted no licence
over a category in this engagement, which is what `refine` recorded on this item and what
`scripts/lint-answers --item WI-0004` reports as zero delegations spent. Each says instead what
reversing it costs.

## Decisions and ADRs

| decision | where | branch of the preference order |
|----------|-------|-------------------------------|
| A move is two entries of kind `move`, one per envelope, opposite signs, shared `on` and `at` | `ADR-0007` [src: ADR-0007] | **asked of the documents, then decided** — `ADR-0002`'s balance rule forced the shape, and the alternatives are in the ADR |
| A move's date lives in `on`, `YYYY-MM-DD`, as a spend's does | `ADR-0007` [src: ADR-0007], folded into the entry shape | **answered from the documents** — `ADR-0006` already defines `on`, and `WI-0004` AC1 says a move is dated the same way |
| No new module; `envelopes` gains one operation and `cli` one branch | `## Approach` | **answered from the documents** — the module table and the dependency direction in `docs/architecture/overview.md` already say where an operation goes |
| `dest="source"` / `dest="destination"` with `metavar="from"` / `metavar="to"` | `## Approach`, interface decision 2 | **decided** — `from` is a Python keyword; there is no alternative worth an ADR |
| `move` added to the top-level subcommand `metavar` | `## Approach`, interface decision 3 | **answered from the documents** — `WI-0001` AC14 requires it |
| The order of the six refusals | `## Assumptions` | **assumed, reversibly** — one function and one test |
| The balance check reads the present balance | `## Assumptions` | **answered from the documents** — the delivered spend's rule, cited |

Nothing here settles a disagreement between two of the stakeholder's own recorded answers; where
this item had one — a spend can be back-dated, income cannot — it was put to them as
`WI-0004/Q-001` and they answered it [src: WI-0004/Q-001].

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | `## The parts`, the `envel/envelopes.py` row, now naming five operations including moving money | cited-fact | True only if the operation exists in that module under that description; a different split while implementing makes the row false |verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | This change adds an operation below `cli`; a `print` or a `sys.exit` in it falsifies the sentence, and the falsifier is a function the sentence does not name |verified-still-true |
| `docs/architecture/overview.md` | `## The data`, the new sentences on what a move stores — two entries, opposite signs, shared `on` and `at` | cited-fact | True only if the entries `move` appends have those fields with those meanings and signs |verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | quantified | Falsified by any entry kind `balance` has to special-case; `move` is the first new kind since a spend |verified-still-true |
| `docs/architecture/overview.md` | `## Conventions this project has adopted`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | quantified | This change adds a second command-line date; accepting any other form on `envel move --on` falsifies it |verified-still-true |
| `docs/architecture/overview.md` | `## What is not decided yet`, now naming three items rather than four | cited-fact | True only if `WI-0004`'s design really is recorded; it also claims `ADR-0002` is being built on without changing the file's shape, which a `format` change would falsify |verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Says `WI-0001` is the first item to be designed and nothing has been implemented, verified or accepted, which two closed items already made false | owned-by-ending |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision`, the JSON pair and the six bullets under it | cited-fact | The entries this item writes have to match it field for field, sign for sign |verified-still-true |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision`: *"The document's `format` stays `1`"* | cited-fact | True only if `envel/store.py`'s `FORMAT` is unchanged and nothing branches on a new value |verified-still-true |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Consequences`: *"the tool gains one entry kind and no field that some other kind does not already carry"* | quantified | Falsified by any field on a `move` entry that no other entry kind carries |verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"`at` keeps the meaning `ADR-0002` gave it — when the tool recorded the entry — on every entry of every kind"* | quantified | This change adds a kind; writing the event date into `at` on a `move` entry falsifies it, and `move` is a kind the sentence does not name |verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Consequences`: *"`WI-0003` sums a month's spending by `on` and a month's income by `at`, with no branch on what a date means"* | quantified | A third kind now carries `on`. The sentence stays true only if `on` means the same day-it-happened on a move as on a spend; it is also now incomplete, since it enumerates two of three kinds |to-update |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | Falsified by any entry whose sign or kind `balance` has to special-case; this change is the first to append two entries at once |verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`entries` is append-only within a run and ordered as written"* | quantified | This change appends two entries in one operation; writing them in either order is fine, but rewriting or reordering an existing entry falsifies it |verified-still-true |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | The new operation handles cents and the new subparser takes an amount as text; either converting between the two forms outside `money.py` falsifies it |verified-still-true |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`, the two commands and what lint checks | cited-fact | This change adds to two test files and two source files, all of which those commands must still cover with no third-party import |verified-still-true |
| `docs/product/vision.md` | `## What it is for`: *"moving an amount from one envelope to another"*, and *"Moving money is what they want to do when an envelope runs short"* | cited-fact | Until this item there is nothing behind the sentence; afterwards it describes delivered behaviour and has to match it |verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | Any import added by this change is a new place it could be falsified, and the falsifier would be a module the sentence does not name |verified-still-true |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Says the engagement has just begun and nothing has been refined, designed, built, verified or accepted | owned-by-ending |

## Deliverable documents

`none`. No acceptance criterion of `WI-0004` has a document as its subject; all thirteen are about
the tool's behaviour, the store file it writes, and the streams and exit codes it uses.
`implement` may therefore write under `docs/` only to close a row of the invalidation set above.

## Binding ADRs

- `ADR-0001` — every amount in this change is a whole number of cents, and only `envel/money.py`
  converts between cents and text.
- `ADR-0002` — the document's shape, the append-only entry list, the balance as the plain sum of
  `cents` over the entries naming an envelope, and that no `format` change is needed.
- `ADR-0003` — the store's path, which every criterion of this item is observed against by setting
  `ENVEL_FILE`.
- `ADR-0004` — the package and the `bin/envel` shim: this change adds no install step and no
  third-party dependency, and both entry points must reach the new subcommand.
- `ADR-0005` — the test and lint commands this change is checked with, both standard library.
- `ADR-0006` — `on` as the day an event is held against, written `YYYY-MM-DD`, and `at` keeping
  its meaning on every kind of entry.
- `ADR-0007` — the move entry pair: two entries of kind `move`, opposite signs, shared `on` and
  `at`, no description, `format` unchanged.

## Scaffolding

`none`. Both test files and both source files this change touches already exist, and
`python3 -m unittest discover -s tests -t .` already runs [src: run: python3 -m unittest discover
-s tests -t . → exit 0, 90 tests].

## Risks

- **Forgetting the subcommand `metavar`.** Adding `move` to the parser without adding it to the
  top-level `metavar` leaves the usage line listing four subcommands when the tool has five, which
  falsifies a delivered criterion of `WI-0001` [src: WI-0001 AC14 "print to stderr a usage message
  that lists the subcommands the tool does have"] without failing any criterion of this item.
  `WI-0002` hit the same risk and answered it with a test
  [src: tests/test_cli.py:493]; step 6 asks for the same.
- **The two entries drifting apart.** If `at` is computed twice or `on` is formatted twice, the
  two halves of one move can carry different values, which nothing in the criteria would catch
  and which would show up as a move counted in two months by `WI-0003`. Step 1 computes each once
  and writes it twice, and step 5 asserts the two entries agree.
- **The refusal order being wrong rather than merely different.** AC3 and AC4 each promise a
  message naming an envelope, and a line that is wrong in two ways can only produce one message.
  The order in `## Approach` satisfies both; a different order could satisfy one and not the
  other. Step 5 fixes it with a test rather than leaving it to reading.
- **Deep-copying and then reading the original.** `record_spend` computes its balances after the
  copy and from the copy [src: envel/envelopes.py:164]; a move has two balances to report and the
  same trap twice. Step 2's line is built from the new document.

## Out of scope for this item

- Correcting or deleting a recorded move. `WI-0004` records the gap and why it is left open
  [src: WI-0004]; a mistake is undone by moving the money back, dated into the month it landed in.
- A description on a move [src: WI-0004].
- Anything `WI-0003` does with `move` entries. This item stores them so that `WI-0003` can filter
  and sum them; computing the fourth column is `WI-0003`'s work and none of it is written here.
- Pairing the two entries of a move, or any identifier on an entry [src: ADR-0007].
