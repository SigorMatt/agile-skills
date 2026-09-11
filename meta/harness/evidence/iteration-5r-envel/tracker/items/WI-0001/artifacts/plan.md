# Plan — WI-0001 Set up envelopes, put income into them, and see what is in each

## Problem

This item creates the tool. There is no source code in this repository yet, so `WI-0001` has to
deliver the first three commands — `envel new <name>`, `envel add <name> <amount>` and
`envel list` — and, underneath them, the two things every later item will build on: how an amount
is held and how the data survives between runs. It is for one person, at their own terminal, on
one machine [src: EP-001/Q-001], under two constraints they stated themselves: Python, no
services, and the data must survive between runs [src: EP-001].

The seventeen criteria are the contract. Most of them are about refusals rather than successes —
a name already taken, an amount of zero, a badly written number, a subcommand that does not
exist — and the design is shaped around making a refusal a value that travels up to one place
that prints it, rather than an exit scattered through the code.

## Approach

Every command is the same three beats: read the whole store, decide, write the whole store back
if anything changed. The decision layer is pure — it takes a store and arguments and returns a
new store plus either output or a refusal — so all seventeen criteria can be exercised both
through the command line and directly.

Four modules, in one dependency direction:

- `envel/money.py` — `parse_amount(text) -> int` and `format_amount(cents) -> str`, the only two
  places text and amounts meet [src: ADR-0001].
- `envel/store.py` — where the file is, loading it, and writing it atomically
  [src: ADR-0002] [src: ADR-0003].
- `envel/envelopes.py` — the three operations as decisions about a store.
- `envel/cli.py` — argument parsing, dispatch, printing, exit codes.

Nothing below `cli.py` prints or calls `sys.exit`. A refusal is a returned value carrying a
message; `cli.py` is the single place that turns one into "message on stderr, non-zero exit",
which is how AC16 is satisfied once rather than seventeen times.

Two result shapes, both defined in `envel/envelopes.py`:

- `Ok(store, lines)` — the new store, and the lines to print on stdout.
- `Refusal(message)` — the text to print on stderr; the store is not written.

`parse_amount` raises `AmountError(message)`; `store.load` raises `StoreError(message)`; `cli.py`
catches both and turns them into the same refusal shape, so an unreadable store and a badly
typed amount reach the user by the same route.

## Steps

1. **`envel/money.py`** — `parse_amount(text)` returns a whole number of cents
   [src: ADR-0001]. It accepts text matching an optional `-`, one or more digits, and optionally
   a `.` followed by one or two digits; `12.5` becomes `1250` and `12.50` becomes `1250`. It
   raises `AmountError` with a message saying the amount must be a plain number for anything else
   (`£12.50`, `1,200`, `12.5x`, `abc`, the empty string), and with a message naming the
   two-decimal-place rule for a number with three or more decimals (`12.567`). A leading `-` is
   parsed successfully into a negative number of cents — refusing it is step 3's job, not this
   one's, so that the stakeholder's decision at `WI-0001/Q-003` is not restated as a parsing
   rule. `format_amount(cents)` returns the number with exactly two decimal places and no
   currency symbol. Afterwards: `12.5` and `12.50` both give `1250`, `format_amount(1250)` is
   `"12.50"`, `format_amount(0)` is `"0.00"`, and `format_amount(100)` is `"1.00"`.
2. **`envel/store.py`** — `store_path()` resolves `ENVEL_FILE`, then `XDG_DATA_HOME`, then
   `~/.local/share/envel/envelopes.json` [src: ADR-0003]. `load(path)` returns a store object;
   a file that does not exist gives the empty store `{"format": 1, "envelopes": [], "entries":
   []}`, and a file that exists but cannot be read, cannot be parsed as JSON, or carries a
   `format` this code does not know raises `StoreError` whose message names the resolved path.
   `save(path, store)` creates missing parent directories, writes the whole document to a
   temporary file in the same directory, and moves it over the target with `os.replace`
   [src: ADR-0002]. Afterwards: loading a path that does not exist gives an empty store and
   creates nothing on disk; saving then loading round-trips; a file holding `not json` raises
   `StoreError` and leaves the file untouched.
3. **`envel/envelopes.py`** — the three operations, each taking a store and returning `Ok` or
   `Refusal`, plus the two helpers they share: `fold(name)` returning `name.casefold()`, and
   `find(store, name)` returning the stored envelope whose folded name matches, or `None`.
   - `create(store, name)` refuses an empty name, and a name that begins or ends with a space
     (U+0020), with a message; refuses a name whose folded form already exists, with a message
     naming it and leaving the store untouched; otherwise appends `{"name": name, "created":
     <now>}` to `envelopes`.
   - `add_income(store, name, cents)` refuses when `cents <= 0`, with a message; refuses when no
     envelope matches, with a message naming the envelope; otherwise appends
     `{"kind": "income", "envelope": <the stored name>, "cents": cents, "at": <now>}` to
     `entries` and returns a line naming the envelope and its new balance.
   - `balance(store, envelope)` sums `cents` over the entries naming that envelope.
   - `listing(store)` returns one line per envelope — the name as stored and its balance
     formatted — ordered by folded name, with no total line; on an empty store it returns a
     single line saying there are no envelopes.
   Afterwards: each of the three returns `Refusal` in exactly the cases AC5, AC7, AC10 and AC13
   name, and the store it was given is unchanged in every one of them.
4. **`envel/cli.py`** — `main(argv)` builds an `argparse` parser with three subparsers, `new`
   (one positional `name`), `add` (positionals `name` and `amount`) and `list` (no arguments),
   with the subcommand required. Parsing failures — no subcommand, an unknown subcommand, a wrong
   number of arguments — are left to `argparse`, which prints usage to stderr and exits 2;
   `main` does not intercept them. For a parsed command, `main` resolves the path, loads the
   store, calls the operation, and then: on `Ok`, prints the lines to stdout, saves the store if
   the operation changed it, and returns 0; on `Refusal`, prints the message to stderr and
   returns 1 without saving. `AmountError` and `StoreError` are caught and become the same
   stderr-and-1 path. Afterwards: every command in this item writes success to stdout with
   exit 0 and every refusal to stderr with a non-zero exit.
5. **`envel/__main__.py`** — `sys.exit(main(sys.argv[1:]))`, so `python3 -m envel …` works. And
   **`envel`** at the repository root — an executable file whose body is the same two lines,
   importing `envel.cli.main` [src: ADR-0004]. Afterwards: `./envel list` and
   `python3 -m envel list` produce identical output and identical exit codes.
6. **`tests/test_money.py`, `tests/test_store.py`, `tests/test_envelopes.py`** — unit tests for
   steps 1 to 3, including every refusal case by name.
7. **`tests/test_cli.py`** — end-to-end tests that run the tool as a subprocess with `ENVEL_FILE`
   pointed at a temporary path, asserting on stdout, stderr and exit code separately. These are
   the tests that demonstrate the criteria about persistence across invocations (AC4, AC9), the
   streams and exit codes (AC16), and the usage failures (AC14, AC15). Assert on the stream and
   the exit code, and on a substring the criterion names — never on argparse's exact wording.
8. **Close the invalidation set below.** Each row is either repaired, or recorded
   `verified-still-true` after reading it against the code that now exists, or left to the
   ending where the table says so. No new document is written by this item; `## Deliverable
   documents` is `none`, so `implement` may not create one.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 3 (`create`), 4 | `tests/test_cli.py`: `./envel new groceries` → stdout contains `groceries` and says created, exit 0 |
| AC2 | 1, 3 (`add_income`), 4 | `tests/test_cli.py`: `./envel add groceries 400` → stdout contains `groceries` and `400.00`, exit 0 |
| AC3 | 3 (`listing`), 4 | `tests/test_cli.py`: three envelopes created out of order → `./envel list` prints them `car`, `eating out`, `groceries`, one line each with name and amount, no total line, exit 0 |
| AC4 | 2, 4 | `tests/test_cli.py`: three separate subprocess runs sharing one `ENVEL_FILE` — new, add, list — the third showing the envelope and the amount |
| AC5 | 3 (`add_income`) | `tests/test_envelopes.py` and `tests/test_cli.py`: `./envel add nosuch 10` → stderr names `nosuch`, exit non-zero, and a following `./envel list` does not list it |
| AC6 | 3 (`listing`), 2 | `tests/test_cli.py`: `./envel list` against an `ENVEL_FILE` that does not exist → one line saying there are none, exit 0 |
| AC7 | 3 (`create`) | `tests/test_cli.py`: new, add 400, new again → stderr says it exists and names it, exit non-zero, and `./envel list` still shows `400.00` |
| AC8 | 1 | `tests/test_money.py`: `parse_amount("12.5") == 1250`, `parse_amount("12.567")` raises; `tests/test_cli.py`: `./envel add g 12.567` refused and `./envel list` unchanged |
| AC9 | 1, 2, 3 | `tests/test_cli.py`: a hundred separate `./envel add g 0.01` runs against one `ENVEL_FILE`, then `./envel list` shows `1.00` |
| AC10 | 3 (`add_income`) | `tests/test_cli.py`: `./envel add g 0` and `./envel add g -40` both refused, `./envel list` unchanged |
| AC11 | 3 (`fold`, `find`, `create`) | `tests/test_cli.py`: new `groceries`, add to `Groceries` 10, list → one line, `10.00`; and new `Groceries` refused |
| AC12 | 3 (`create`, `listing`) | `tests/test_cli.py`: the same sequence — the listed line reads `groceries` |
| AC13 | 3 (`create`) | `tests/test_cli.py`: `./envel new "eating out"` and `./envel new "car & bike"` exit 0; `./envel new ""` and `./envel new " x"` refused and neither appears in `./envel list` |
| AC14 | 4 | `tests/test_cli.py`: `./envel` and `./envel frobnicate` → stderr non-empty and mentions `new`, `add` and `list`, exit non-zero, `ENVEL_FILE` still absent |
| AC15 | 4 | `tests/test_cli.py`: the five invocations the criterion names → stderr non-empty, exit non-zero, `./envel list` unchanged |
| AC16 | 4 | `tests/test_cli.py`: a table-driven test walking the cases AC5, AC7, AC8, AC10, AC13, AC14, AC15 asserting stderr non-empty, stdout empty and exit non-zero; and AC1, AC2, AC3, AC6 asserting stdout non-empty, stderr empty and exit 0 |
| AC17 | 1 | `tests/test_money.py`: `400`, `12.5`, `12.50` parse; `£12.50`, `1,200`, `12.5x`, `abc` raise; `tests/test_cli.py`: each refused with `./envel list` unchanged, and no printed amount contains a currency symbol |

## Assumptions

- **Where a criterion says `envel`, it means the tool's command line, exercised in this
  repository as `./envel`** — identically `python3 -m envel` [src: ADR-0004]. Putting the name on
  a `PATH` is an install step this item does not perform. Reversal: add a `pyproject.toml` with a
  console script; one new file, no change to the package, no data migration.
- **Names are matched with `str.casefold()`** rather than `str.lower()`, which is the stricter
  reading of *"Groceries and groceries are the same envelope"* [src: WI-0001/Q-004] and differs
  only for scripts the stakeholder is unlikely to use. Reversal: one function in
  `envel/envelopes.py`; no stored data changes, because the store holds the name as typed
  [src: ADR-0002].
- **AC13 is read literally**: only the space character U+0020 at either end is refused, so a name
  ending in a tab is accepted. The criterion says "begins or ends with a space" and
  `refine` recorded that internal whitespace is deliberately unconstrained [src: WI-0001].
  Reversal: one predicate in `envel/envelopes.py`.
- **Amounts are held as whole cents.** **Under delegation:** WI-0001/Q-002 — how an amount is
  held internally. Their words were *"How you keep it under the hood is yours to decide"*, and
  the licence is taken to cover the internal representation only; what is accepted and what is
  printed they specified themselves and neither is assumed here. Recorded as [src: ADR-0001].
  Reversal: `envel/money.py` plus a conversion of any stored file.
- **`created` on an envelope and `at` on an entry are written but never read by this item**
  [src: ADR-0002]. Reversal: deleting the fields is one line each — but doing so after the
  stakeholder has a file is a migration, which is the reason they are there now.

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| Amounts are whole numbers of cents | [src: ADR-0001] | assumed, under the stakeholder's delegation at `WI-0001/Q-002` |
| The store is one JSON document holding envelopes and a dated entry log, written atomically; a missing file is empty and a damaged one is refused without being overwritten | [src: ADR-0002] | decided — `refine` routed it here, and `EP-001/Q-003` and `EP-001/Q-004` are what rule out storing a balance |
| The store is located by `ENVEL_FILE`, then `XDG_DATA_HOME`, then `~/.local/share` | [src: ADR-0003] | decided |
| The tool is a package plus a repository-root shim, with no install step | [src: ADR-0004] | decided |
| Tests are `unittest` and lint is `compileall`, both standard library | [src: ADR-0005] | decided, against a measurement of what is installed |
| A refusal is a returned value, and `envel/cli.py` is the only place that prints one or chooses an exit code | `## Approach` above, and `docs/architecture/overview.md` | assumed — reversal is moving the printing into `envel/envelopes.py`, one module, no interface anybody outside the package sees |
| Argument-shape failures are left to `argparse` rather than hand-written | step 4 | assumed — reversal is a hand-rolled parser in `envel/cli.py`; AC14 and AC15 constrain the stream and the exit code, not the wording |

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/product/vision.md` | `## Engagement state`, bullet 1: *"The engagement has just begun. `intake` has run; nothing has been refined, designed, built, verified or accepted."* | engagement-state | This item is designed and about to be built, so the sentence is false | owned-by-ending |
| `docs/product/vision.md` | `## Engagement state`, bullet 2: *"A first round of questions was filed on `EP-001` and the stakeholder has not answered yet, so `EP-001` is suspended at `awaiting-answer` until they do"* | engagement-state | They answered; `EP-001` is at `open` | owned-by-ending |
| `docs/product/vision.md` | `## What it is for`, last line: *"The command is `envel`"* | cited-fact | This item creates the command line; until now the sentence had nothing behind it | verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`, bullet 2: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | This item writes the first code; a single import would falsify it, and the falsifier is a module the sentence does not name | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`, the module table | cited-fact | It names six files that do not exist yet; a different split while implementing makes the table false | to-update |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | A `print` anywhere in `money.py`, `store.py` or `envelopes.py` falsifies it | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | cited-fact | True only if `envelopes.balance` is what the listing calls | verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Written when nothing was implemented | owned-by-ending |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | Any other module converting between text and cents falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`, the JSON document and the atomic-write clause | cited-fact | The implemented document has to match the one written here, field for field | verified-still-true |
| `docs/architecture/adr/ADR-0003-store-location.md` | `## Decision`, the three-step path resolution | cited-fact | True only if `envel/store.py` resolves in that order | verified-still-true |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | `## Decision`, the two entry points | cited-fact | True only if both exist and reach the same `main` | to-update |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`: *"The test command exits 5 while no test exists"* | cited-fact | This item writes the first tests, after which the same command exits 0 — the sentence is written to survive that, and needs re-reading once it has | verified-still-true |
| `docs/product/vision.md` | `## What it is for`, last paragraph: *"the tool starts, does one thing, and exits, leaving its data on the local machine; nothing runs between invocations"* | quantified | Added by `implement`: this item writes the first code, so the sentence about how the tool runs acquires something that can falsify it | verified-still-true |

## Deliverable documents

`none`. No acceptance criterion of `WI-0001` has a document as its subject; the seventeen are all
about the tool's behaviour. `implement` may therefore write to `docs/` only to close a row of the
invalidation set above.

## Binding ADRs

- `ADR-0001` — every amount in this change is a whole number of cents, and only `envel/money.py`
  converts between cents and text.
- `ADR-0002` — the stored document's fields, the append-only entry list, the derived balance, the
  atomic write, and the treatment of a missing or damaged file.
- `ADR-0003` — the three-step resolution of the store's path.
- `ADR-0004` — the package plus repository-root shim, and that no install step is introduced.
- `ADR-0005` — the test and lint commands this change is checked with, and that no third-party
  dependency is added.

## Scaffolding

- `envel/__init__.py` — empty. Without the directory and the marker, `python3 -m compileall -q
  envel tests` cannot execute, and that command is now declared in `tracker/project.yaml`.
- `tests/__init__.py` — empty. Same reason, and `python3 -m unittest discover -s tests -t .`
  needs the directory to exist before it can report an empty suite rather than an error.

Neither file contains any behaviour. Deleting them would break the two declared commands and no
acceptance criterion.

## Risks

- **The `at` and `created` fields are carried on the strength of a sibling item.** No criterion in
  `WI-0001` observes either [src: WI-0001]. If `WI-0003`'s refinement settles on something other
  than a per-month sum over dated entries, they are dead weight — cheap weight, but the
  justification in `ADR-0002` would then be wrong and the ADR would need correcting rather than
  quietly leaving.
- **`argparse`'s wording is not ours.** AC14 and AC15 are satisfied by the stream and the exit
  code, so a test that asserts argparse's exact message would break on a Python upgrade for no
  product reason. Step 7 says to assert on the stream, the exit code and the substring the
  criterion itself names.
- **AC9 is a hundred process starts.** It is the criterion most likely to be quietly weakened
  into a single in-process loop, which would not test what it is for — that the total survives
  being written to disk and read back a hundred times [src: WI-0001 AC9 "No amount is rounded or truncated"].
- **The test command exits 5 until the first test exists**
  [src: run: python3 -m unittest discover -s tests -t . → exit 5, NO TESTS RAN]. An
  `implement` execution that runs the gate before writing a test will see a failure that is not
  one.
- **One JSON document read and written whole on every command.** Fine for a household budget and
  wrong for anything larger; `ADR-0002` names it as the thing to revisit if that ever changes.

## Out of scope for this item

- Recording spending and anything that reduces an envelope's amount — `WI-0002`.
- The monthly summary — `WI-0003`. This item writes the `at` field it will need and reads none
  of it.
- Moving money between envelopes — `WI-0004` — and correcting a recorded spend — `WI-0005`.
- Listing the spends recorded against an envelope — `WI-0006`.
- Installing the tool: no `pyproject.toml`, no console script, no packaging [src: ADR-0004].
- Migrating a store written by an older `format` — there is no older format.
