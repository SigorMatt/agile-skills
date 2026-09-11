# Plan — WI-0005 Correct a spend that was already recorded

## Problem

The stakeholder mistypes entries most weeks and wants to put them right without keeping a history
of their own typos: *"if I fix an entry, a past summary should just show the corrected figure"*
[src: EP-001/Q-005]. This item adds the two commands that do it — `envel fix <ref>`, which changes
an entry's amount, date, description or envelope, and `envel remove <ref>`, which deletes one —
both aimed with the reference `WI-0006` already prints beside every line of `envel entries`
[src: WI-0006 AC3 "The reference on a line is a number counted once across everything recorded"].

The constraints are all already decided and none of them is this plan's to reopen. A balance is the
plain sum of an envelope's entries with no branch on `kind` [src: ADR-0002]. A reference is stored
on its entry, written once, and comes only from the document's counter [src: ADR-0010]. A move is
two entries and is not correctable at all [src: ADR-0007],
[src: WI-0005 AC13 "are each refused with a message saying a move cannot be corrected or removed"].
An envelope is never shown negative, and that rule now reaches a correction and a removal as well
as a spend [src: WI-0005/Q-004]. And a correction on an income reaches its amount and its envelope
and nothing else [src: WI-0005/Q-006].

## Approach

**One decision carries the item, and it is `ADR-0011`** [src: ADR-0011]: a correction edits the
entry where it sits and a removal deletes it from the list. The alternatives — appending a
compensating entry, or flagging the old entry and appending a new one — each keep the entry log
strictly append-only and each break a criterion the stakeholder wrote, which the ADR sets out.

The payoff of that choice is that **no reader in the tool changes**. `balance`, `figures`,
`bounded_balance`, `entries_in` and `entry_line` all keep the one rule they share
[src: envel/summary.py], [src: envel/envelopes.py], so four of this item's twenty criteria — AC7,
AC8, AC14 and AC20 — are satisfied by the shape of the design rather than by code, and are
demonstrated rather than built. What gets written is two operations, two subcommands, and tests.

Everything else follows the delivered patterns without inventing anything:

- **The operations live in `envel/envelopes.py`**, because they change a store and return a new
  one, which is the line `ADR-0009` draws between an operation and a report [src: ADR-0009]. They
  return `Ok` or `Refusal` and print nothing, like the five already there.
- **Values are parsed in `envel/cli.py`**, by `money.parse_amount` and `dates.parse_date`, exactly
  as `spend` and `move` already parse theirs [src: envel/cli.py:130]. A malformed amount or date
  therefore raises `AmountError` or `DateError` and exits 1 before the operation is reached, which
  is delivered behaviour that AC2 and AC3 inherit rather than restate [src: ADR-0001], [src: ADR-0006].
- **Nothing is written on a refusal**, because a `Refusal` carries no document and `envel/cli.py`
  saves only when the result reports that it changed something [src: envel/cli.py:217]. That is
  what makes AC19's *nothing at all* a property of the existing dispatch rather than a check.
- **`format` stays `2` and `envel/store.py` is not touched.** No key is added, removed or renamed
  [src: envel/store.py:11].

**The order of the refusals is this plan's**, and it is: identity first, then applicability, then
each option's own validity, then the balance invariant. Identity leads because nothing can be said
about an entry that was not found; the income check comes next because `--on` on an income is a
refusal about the *entry*, not about the value typed; and the invariant is last because its message
quotes a balance, which means nothing until the entry and the envelopes are known. This is the same
reasoning `record_spend` and `move` were given [src: envel/envelopes.py].

## Steps

1. **`envel/envelopes.py` — `find_entry(store, reference)`.** Return the entry in
   `store["entries"]` whose `ref` equals `reference`, or `None`. `reference` is the text the person
   typed; it is compared by reading it as a decimal integer and matching `entry["ref"]` by equality,
   and text that is not a decimal integer matches nothing. Afterwards: a reference no entry has, and
   a reference that is not a number at all, both reach the same *no such entry* path.

2. **`envel/envelopes.py` — `envelopes_below_zero(store, names)`.** Return the first name in `names`
   whose `balance(store, name)` is negative, or `None`, preserving the order given. Afterwards:
   both operations have one place that asks the question AC9 and AC18 ask, over the candidate
   document rather than the live one.

3. **`envel/envelopes.py` — `correct(store, reference, cents, on, description, envelope)`.** The
   `envel fix` operation. Each of the four value parameters is `None` when its option was not given;
   `description` given as an empty or blank string means *remove the description*. In order:
   - `find_entry` returns `None` → `Refusal` naming the reference as typed (AC1);
   - the entry's `kind` is `"move"` → `Refusal` saying a move cannot be corrected (AC13);
   - the entry has no `on` — it is an income — and `on` or `description` was given → `Refusal`
     saying an income carries no date and no description (AC16);
   - `envelope` was given and `find` returns `None` for it → `Refusal` naming it as typed (AC5);
   - `cents` was given and is `<= 0` → `Refusal` naming the amount (AC10);
   - `on` was given and is later than `dates.today()` → `Refusal` naming the date (AC3);
   - otherwise deep-copy the store, locate the same entry in the copy, and apply every option that
     was given: `cents` is written negative for a spend and positive for an income, preserving the
     sign the entry already carries [src: ADR-0002]; `on` is written with `dates.format_date`;
     `description` is set, or the key is deleted when the text is blank [src: ADR-0006]; `envelope`
     is written as the stored envelope's own spelling, the way `record_spend` writes it
     [src: envel/envelopes.py];
   - then `envelopes_below_zero(candidate, [the entry's envelope before, the entry's envelope after])`
     → if it returns a name, `Refusal` naming that envelope, what it holds in the **original**
     store, and how much short the change would leave it (AC9, AC18);
   - otherwise `Ok(candidate, [one line], changed=True)`.

   Afterwards: `correct` is a pure function of (store, arguments) that returns either a new document
   or a refusal, and the caller's document is never mutated.

4. **`envel/envelopes.py` — `remove(store, reference)`.** In order: `find_entry` returns `None` →
   `Refusal` naming the reference (AC12); the entry's `kind` is `"move"` → `Refusal` (AC13);
   otherwise deep-copy, delete that entry from the copy's `entries` list, leave `next-ref` alone
   [src: ADR-0010], run `envelopes_below_zero(candidate, [the entry's envelope])` → `Refusal` on a
   name (AC18); otherwise `Ok(candidate, [one line], changed=True)`. Afterwards: removing the
   highest-numbered entry does not lower `next-ref`, so the next entry recorded takes a number that
   has never been on the screen.

5. **`envel/envelopes.py` — the two success lines.** `correct` prints the entry's envelope after the
   change and what that envelope holds afterwards; when `--envelope` moved the entry, the line also
   names the envelope it came from and what that holds (AC2). `remove` prints what it took out — the
   envelope, the amount, and the date when the entry has an `on` and no date when it does not — and
   what the envelope holds afterwards (AC11, AC17). Both amounts go through `money.format_amount`
   and nothing else [src: ADR-0001]. Afterwards: nothing below `envel/cli.py` prints; both return
   their line inside `Ok`.

6. **`envel/cli.py` — two subparsers in `build_parser`.** `fix` takes `ref` as a plain positional
   and `--amount`, `--on YYYY-MM-DD`, `--description` and `--envelope` as named options, each
   defaulting to `None`; `remove` takes `ref` alone. Both are added to the returned
   `subcommand_parsers` map and to the `metavar` on `add_subparsers`. Afterwards:
   `envel fix --help` and `envel remove --help` print their own usage, and `envel fix 7 extra`
   is reported by the `fix` parser (AC6, AC15).

7. **`envel/cli.py` — the *no option given* check.** Immediately after the existing `unrecognised`
   check and **before** `store.load`, if the command is `fix` and all four options are `None`, call
   `subcommand_parsers["fix"].error(...)`, which prints `usage: envel fix …` to stderr and exits 2.
   Afterwards: `envel fix 7` alone prints the subcommand's usage, exits non-zero and cannot have
   changed anything, because the store was never read (AC6).

8. **`envel/cli.py` — the two dispatch branches.** `fix` calls `envelopes.correct` with
   `money.parse_amount(arguments.amount)` when `--amount` was given, `dates.parse_date(arguments.on)`
   when `--on` was given, and the raw strings for `--description` and `--envelope`; `remove` calls
   `envelopes.remove`. Afterwards: a malformed amount or date is `AmountError`/`DateError` on stderr
   with exit 1, as `spend` already does, and no new branch shape appears in `main` (AC15).

9. **`tests/test_corrections.py` — a new module, the operations directly.** Classes covering:
   correcting each field on a spend; the four options together; correcting an income's amount and
   envelope and the two refusals on one; every refusal path of both operations, each asserting the
   returned object is a `Refusal` **and** that the document passed in is unchanged; `next-ref` after
   a removal; and the reference of a move refused from both operations. Afterwards: every refusal
   named by AC1, AC3, AC5, AC6, AC9, AC10, AC12, AC13, AC16, AC18 and AC19 has a case at this level.

10. **`tests/test_cli.py` — end-to-end cases, appended.** Using the module's existing `envel()`
    helper, which runs the shim as a separate process with `ENVEL_FILE` pointing at a scratch path:
    the success paths of `fix` and `remove` on a spend and on an income; `envel fix 7` with no
    option; the stream and exit code of every refusal; `--description ""` leaving the stored entry
    with no `description` key at all; a correction followed by `envel list`, `envel summary` and
    `envel entries` **in separate invocations**; and a `--on` correction that moves a spend between
    two months, asserted against both months' summaries and both months' listings. Afterwards:
    AC7, AC8, AC14 and AC20 have their evidence, and AC15 is checked case by case rather than
    asserted.

11. **Close the invalidation set.** Give every row below a disposition, repairing what this change
    made false. `docs/architecture/overview.md` was already taken to v9 by this plan and
    `ADR-0011` was written; what is left for `implement` is to read each row against the code it
    actually wrote and to repair `ADR-0002`'s append-only sentence, which is the one row that
    certainly needs an edit. `implement` may write under `docs/` only to close a row of this set
    [src: docs/architecture/overview.md].

12. **Run the gates.** `python3 -m unittest discover -s tests -t .` and
    `python3 -m compileall -q envel tests`, both from `tracker/project.yaml` [src: ADR-0005].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 1, 3, 6 | `tests/test_corrections.py`: `correct` on a reference no entry has, and on `"abc"`, each returns a `Refusal` naming what was typed and leaves the document unchanged. `tests/test_cli.py`: `envel fix 999 --amount 1` — stderr names `999`, exit non-zero, `envel list` byte-identical before and after |
| AC2 | 3, 5, 8 | `tests/test_cli.py`: `envel fix <ref> --amount 14.00` on a spend of 12.50 — stdout names the envelope and its new balance, exit 0, `envel list` shows the envelope 1.50 lower |
| AC3 | 3, 8 | `tests/test_cli.py`: `envel fix <ref> --on 2026-08-28` succeeds; `--on 7/9` is `DateError` on stderr with exit 1; `--on <tomorrow>` is a `Refusal` on stderr with exit 1; the store is unchanged after each failure |
| AC4 | 3 | `tests/test_corrections.py`: `--description "lunch"` sets the key; `--description ""` leaves the entry dict with no `description` key at all, asserted with `assertNotIn`. `tests/test_cli.py`: the same read back out of the JSON file |
| AC5 | 3, 5 | `tests/test_cli.py`: `envel fix <ref> --envelope "eating out"` — `envel list` shows the destination down by the spend and the source up by it, a third envelope unchanged; `--envelope nosuch` on stderr with exit non-zero and nothing changed; `--envelope GROCERIES` matches `groceries` |
| AC6 | 3, 6, 7 | `tests/test_cli.py`: all four options in one invocation apply all four; `envel fix 7` with none prints `usage: envel fix` to stderr, exits non-zero, and the store file is byte-identical |
| AC7 | none — it falls out of `ADR-0011` | `tests/test_cli.py`: `envel list` captured before and after a correction; only the envelopes the correction names differ, and by exactly the corrected amounts |
| AC8 | none — it falls out of `ADR-0011` | `tests/test_cli.py`: `envel summary 2026-08` and `envel summary 2026-09` around an `--on` correction that crosses the boundary; the amount appears in exactly one, the month of the date after the correction |
| AC9 | 2, 3 | `tests/test_cli.py`: `envel fix <ref> --amount 140.00` where the envelope holds 30.00 — stderr names the envelope, `30.00` and `110.00`; exit non-zero; `envel list` unchanged |
| AC10 | 3 | `tests/test_corrections.py` and `tests/test_cli.py`: `--amount 0` and `--amount -5`, each a refusal on stderr with a non-zero exit and nothing changed |
| AC11 | 4, 5 | `tests/test_cli.py`: `envel remove <ref>` on a spend — stdout names the envelope, the date and the amount removed and the new balance; exit 0; the subprocess is run with `stdin` closed and reads nothing |
| AC12 | 4 | `tests/test_cli.py`: `envel remove 999` — stderr names `999`, exit non-zero, nothing changed |
| AC13 | 3, 4 | `tests/test_corrections.py`: both halves of a move, by their two references, refused by `correct` and by `remove`, each message saying a move cannot be corrected or removed. `tests/test_cli.py`: the same through the command line |
| AC14 | none — it falls out of `ADR-0011` | `tests/test_cli.py`: a correction and a removal, then `envel list`, `envel summary` and `envel entries` each as a separate subprocess |
| AC15 | 5, 6, 7, 8 | `tests/test_cli.py`: one assertion per case listed in AC15 itself — refusals at AC1, AC3, AC5, AC6, AC9, AC10, AC12, AC13, AC16, AC18 and AC19 each with empty stdout and a non-zero exit; successes at AC2, AC4, AC5, AC7, AC11, AC16, AC17 and AC20 each with empty stderr and exit 0 |
| AC16 | 3, 8 | `tests/test_cli.py`: on an income's reference, `--amount 80.00` and `--envelope "eating out"` succeed and move the figures; `--on 2026-09-01` and `--description x` are each refused with nothing changed; `--amount 0` on an income is still AC10's refusal |
| AC17 | 4, 5 | `tests/test_cli.py`: `envel remove <ref>` on an income — stdout names the envelope and the amount and the new balance, no date, exit 0, no flag accepted or required |
| AC18 | 2, 3, 4 | `tests/test_cli.py`: an envelope holding 100.00 of income with 90.00 spent from it — `envel remove <income-ref>`, `envel fix <income-ref> --amount 50.00` and `envel fix <income-ref> --envelope "eating out"` each refused naming the envelope and the shortfall, `envel list` identical after all three |
| AC19 | 3, 4 | `tests/test_corrections.py`: `correct` called with one accepted and one refused option asserts the document passed in is unchanged, by deep equality against a copy taken first. `tests/test_cli.py`: `envel fix <income-ref> --amount 20.00 --on 2026-09-01` — the `envel entries` line for that reference and the whole of `envel list` are identical before and after |
| AC20 | none — it falls out of `ADR-0011` | `tests/test_cli.py`: `envel entries --month <m>` captured around each of a `--amount` fix, an `--on` fix into another month, an `--envelope` fix and a `remove`; and with an envelope named, the opening figure plus the lines between equals the closing figure in each case |

## Assumptions

- **A reference that is not a decimal integer matches no entry**, and takes AC1's and AC12's
  refusal path rather than a new error type of its own. `envel fix abc --amount 1` therefore says
  there is no entry `abc`. Reversing it means adding a `RefError` in a new module beside
  `money.AmountError` and `dates.DateError` and one branch in `envel/cli.py`: one function and one
  branch, no data change, no stored shape change. Taken under **no** delegation. AC1 promises a
  message naming the reference for *a `<ref>` that matches no entry*, and `abc` is one; a
  disagreement lands on the message a person sees and on nothing else.
- **The `fix` success line names the envelope the entry is in afterwards and what it holds, and
  names the source envelope too when `--envelope` moved the entry.** AC2 requires only the first
  half. Reversing it is one `format` call in one function. Taken under **no** delegation — the
  standing licence at `WI-0003/Q-004` is about argument style and the naming of commands and
  options, and a success line's content is not that, so this is written down as ours rather than
  claimed as theirs.
- **`envel fix` with no option is caught in `envel/cli.py` before the store is loaded**, and
  reported by the `fix` subparser's own `error()`. `argparse` cannot express *at least one of these
  four*, and AC6 asks for the subcommand's usage specifically. The precedent is the `unrecognised`
  check already in `main` for the same reason [src: envel/cli.py:107]. Reversing it is one branch.
- **The new test module is `tests/test_corrections.py`**, beside `tests/test_entries.py`, which is
  the shape this project already uses — one module per item's own behaviour, with the end-to-end
  cases in `tests/test_cli.py`. Reversing it is a rename.

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| A correction edits the entry in place; a removal deletes it; `next-ref` is never decreased; `format` stays 2; the invariant is checked against the candidate document | `ADR-0011`, written by this execution | **asked of nobody and assumed by nobody** — it is irreversible in its *effects* and it falsifies a standing sentence of `ADR-0002`, so it is an ADR |
| The operations go in `envel/envelopes.py` and not in `envel/summary.py` | `ADR-0009`, cited | **from the documents** |
| Values are parsed in `envel/cli.py` by `money` and `dates`, so a malformed one never reaches the operation | `ADR-0001`, `ADR-0006`, `ADR-0008`, cited; step 8 | **from the documents** |
| A refusal writes nothing, because `Ok.changed` gates the save | `envel/cli.py:217`, cited; step 3 | **from the documents** |
| The order of the refusals within each operation | `## Approach`, with the reasoning | **from the documents** — the same reasoning `record_spend` and `move` carry in their own docstrings |
| A non-numeric reference matches no entry | `## Assumptions` | **reversible assumption** |
| What the `fix` success line says | `## Assumptions` | **reversible assumption** |
| Where *no option given* is detected | `## Assumptions` | **reversible assumption** |
| The new test module's name | `## Assumptions` | **reversible assumption** |

Nothing on this item was put to the stakeholder. Every question that needed them was asked during
refinement and answered: eight questions across two rounds, all `status: answered`
[src: tracker/items/WI-0005/artifacts/refinement-qa.md]. No decision here is irreversible in a way
the documents do not already cover, and none of them depends on intent no document records.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`: *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it"* | quantified | The first clause is exactly what `ADR-0011` falsifies — a correction edits an entry and a removal deletes one — and the second must survive untouched. This is the row this item exists around | to-update |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Consequences`: *"the file is readable and repairable in any text editor"*, and **Reversibility**: *"any change to the document needs code that reads the old `format` and writes the new one"* | cited-fact | This change edits and deletes entries without changing the document's shape, which is a case the reversibility sentence does not describe; whether either sentence survives is a read | verified-still-true |
| `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` | `## Consequences`: *"A reference survives a removal because it is stored rather than derived, so `WI-0005` inherits the property rather than having to arrange it"* | cited-fact | Written as a prediction about this item; this item is where it becomes true or false | verified-still-true |
| `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` | `## Decision` 5: *"The counter is the only source of a new reference. Nothing derives one from a position, a length or a maximum"* | quantified | A removal that lowered `next-ref`, or an operation that recomputed a `ref`, falsifies it; step 4 is written so that neither happens | verified-still-true |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `## Decision` and `## Consequences`: the two-entry shape, and what nothing in the file links | quantified | AC13 refuses a correction aimed at either half; a refusal implemented by reading the two halves as a pair would falsify the *nothing links them* clause | verified-still-true |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` | `## Decision`: *"`on` is present on every spend entry… It is never absent and never null"*, and *"`description` is present only when one was typed. Absent means there was none"* | quantified | A correction writes both fields. `--description ""` must delete the key rather than store an empty string, and no correction may clear an `on`; the falsifier is a spend the sentence does not name | verified-still-true |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `## Decision`: reporting is in `envel/summary.py` and the operations are in `envel/envelopes.py` | cited-fact | The two new operations go to `envelopes.py`; putting either in `summary.py`, or importing `summary` from `envelopes` to reuse `entry_date`, falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` | `## Decision`: a month is the string `YYYY-MM` compared as a string, and every figure is a filtered sum | quantified | AC8's *exactly one month* is that arithmetic with a changed `on` and nothing else; a special case anywhere for a corrected entry falsifies it | verified-still-true |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | Two success lines and three refusal messages print amounts; one rendered anywhere else is the falsifier | verified-still-true |
| `docs/architecture/adr/ADR-0003-store-location.md` | `## Decision` and `## Consequences`: one function in `envel/store.py` resolves the path and nothing else knows about it | quantified | The new operations are new code; a store path referenced from `envel/envelopes.py` would falsify it | verified-still-true |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | `## Decision`: two entry points *"both reaching the same `main`"* | quantified | Two new subcommands are the shape that falsifies it — reachable from `bin/envel` and not from `python3 -m envel`, or the reverse | verified-still-true |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`: the two commands, and what the lint command does and does not check | cited-fact | This change edits two source files and one test file and adds one; both commands must still cover them, with no third-party import | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`: the `envel/envelopes.py` row, now naming seven operations | cited-fact | Rewritten by this plan from the design; if either operation lands elsewhere the row is false | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`: the dependency direction — *"`cli` knows about all five modules below it… `envelopes` does not know about `summary`"* | quantified | This change edits `envelopes.py` and `cli.py`; an import added from `envelopes` to `summary` is the obvious falsifier and the obvious temptation | verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | Two new operations sit below `cli`; a `print` or a `sys.exit` in either falsifies it | verified-still-true |
| `docs/architecture/overview.md` | `## The shape of it`: the three beats, *"write the whole store back, atomically, but only if something changed"* | quantified | AC19 is this sentence for an invocation carrying several changes; a refusal that wrote would falsify both | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: the entries paragraph as rewritten at v9 — *"The list was append-only until `WI-0005`… no key is added, removed or renamed, so `format` stays `2`"* | cited-fact | Written from the design before the code exists; a stray key or a `format` bump falsifies it | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: *"Each entry also carries `ref`, a positive integer written when the entry is appended and never changed afterwards"* | quantified | A correction writes an entry; writing its `ref` falsifies the sentence, and the falsifier is an entry the sentence does not name | verified-still-true |
| `docs/architecture/overview.md` | `## The data`: the move paragraph — *"the two consecutive references they take"*, and *"No code reads that adjacency as a link"* | quantified | AC13 is the first code to be handed one half of a move and asked about it | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: success to stdout with exit 0, every refusal to stderr with a non-zero exit | quantified | This change adds two success paths and ten refusals; AC15 is the same claim written as a criterion | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: *"Amounts are printed with exactly two decimal places and no currency symbol"* | quantified | Every line and message this change prints carries an amount | verified-still-true |
| `docs/architecture/overview.md` | `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD`… both are parsed in `envel/dates.py` and nowhere else"* | quantified | `--on` on `envel fix` is a new command-line date; parsing it anywhere else falsifies the second clause | verified-still-true |
| `docs/architecture/overview.md` | `## What is not decided yet`: *"Nothing. Every item of `EP-001` has had its design taken"*, as rewritten at v9 | quantified | A universal over the epic's items, written by this execution; a bug item filed during implementation or verification would falsify it | verified-still-true |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Says `WI-0001` is the first item to be designed and that nothing has been implemented, verified or accepted, which five closed items already made false; and that no document has been checked against running code | owned-by-ending |
| `docs/product/vision.md` | `## What it is for`: the correction paragraph — what a correction reaches on a spend, removal by a command that says what it took, the below-zero refusal with the shortfall named, and moves staying outside it | cited-fact | This item is what the paragraph describes; anything the two commands do differently makes it false | verified-still-true |
| `docs/product/vision.md` | `## What it is for`: the income paragraph — the amount and the envelope and no date, removal by the same command with no flag, and the shortfall rule reaching a removal | cited-fact | Same: the paragraph is this item's AC16, AC17 and AC18 written in the stakeholder's words | verified-still-true |
| `docs/product/vision.md` | `## What it is for`: *"the number an entry is given stays that entry's, so a number written down last week still means what it meant"* | quantified | A removal is the event this sentence was written against; renumbering, or reissuing a number from a lowered counter, falsifies it | verified-still-true |
| `docs/product/vision.md` | `## What it deliberately is not`: *"Not connected to anything: no server, no sync, no bank import, no network"* | quantified | Any import this change adds is a place it could be falsified, and the falsifier is a module the sentence does not name | verified-still-true |
| `docs/product/vision.md` | `## Engagement state` | engagement-state | Says the engagement has just begun, that nothing has been refined, designed, built, verified or accepted, and that `EP-001` is suspended awaiting an answer | owned-by-ending |

## Deliverable documents

`none`. No acceptance criterion of `WI-0005` has a document as its subject: AC1 to AC20 are about
what `envel fix` and `envel remove` change, refuse and print, and about what `envel list`,
`envel summary` and `envel entries` show afterwards. `implement` may therefore write under `docs/`
only to close a row of the invalidation set above — which step 11 expects it to do for
`ADR-0002` at least.

## Binding ADRs

- `ADR-0001` — amounts are integer cents and `envel/money.py` is the only place the two forms meet.
  Every amount these two commands print goes through `format_amount`; `--amount` is parsed by
  `parse_amount` in `envel/cli.py` and nowhere else.
- `ADR-0002` — one JSON document, entries ordered as written, a balance the plain sum of `cents`
  with no branch on `kind`. The sum is what makes AC7, AC8 and AC20 fall out; the append-only
  clause is the one sentence this change falsifies, and `ADR-0011` says so.
- `ADR-0003` — one function in `envel/store.py` resolves the store's path and nothing else knows
  about it. Neither new operation sees a path; `ENVEL_FILE` is how every criterion is observed.
- `ADR-0004` — `python3 -m envel` and `bin/envel` both reach the same `main`, so the two new
  subcommands are reachable from both without either entry point being edited.
- `ADR-0005` — the test and lint commands are standard library only; the new test module and the
  edited one import nothing outside it.
- `ADR-0006` — a spend carries `on` and income does not; `description` is present only when one was
  typed. AC3, AC4 and AC16 are all that ADR read as rules about writing rather than about reading:
  `--description ""` deletes the key, and an entry with no `on` is the income AC16 refuses two
  options on.
- `ADR-0007` — a move is two entries with opposite `cents` and the same `on` and `at`, and nothing
  in the file names the pair. AC13 refuses either half on its own `kind`, not by finding its
  partner.
- `ADR-0008` — a month is the string `YYYY-MM`, compared as a string, and every figure is a
  filtered sum. AC8's *exactly one month* is that arithmetic applied to an entry whose `on` changed.
- `ADR-0009` — reporting lives in `envel/summary.py` and the operations in `envel/envelopes.py`,
  both returning `Ok` or `Refusal` so `envel/cli.py` gains no new branch shape. It is why the two
  new functions go where they go.
- `ADR-0010` — an entry carries its own `ref`, written once and never changed, and `next-ref` is
  the only source of a new one. AC1's *nothing is renumbered* is inherited from it; step 4's
  *leave `next-ref` alone* is the clause that keeps it true through a removal.
- `ADR-0011` — a correction edits the entry in place and a removal deletes it. Written by this
  execution; it is what AC7, AC8, AC14 and AC20 rest on, and the reason they need no code.

## Scaffolding

`none`. Both declared commands already execute in this project — `python3 -m unittest discover -s
tests -t .` runs 231 tests and `python3 -m compileall -q envel tests` exits 0
[src: run: python3 -m unittest discover -s tests -t . → exit 0, Ran 231 tests, OK]. `tests/` has
its `__init__.py` and every module this item touches exists already.

## Risks

- **A correction is destructive and there is no copy.** A bug in step 3 that writes the wrong field,
  or step 4 deleting the wrong entry, damages the stakeholder's real figures with nothing in the
  tool to restore them. The mitigation is the one already in the design — the store is written
  whole and atomically [src: ADR-0002], so a *failed* run leaves the previous file — and the tests
  in step 9 that assert the input document is unchanged on every refusal path. A *successful* wrong
  correction is not recoverable, and `ADR-0011` says so rather than softening it.
- **The temptation to import `summary` from `envelopes`.** `remove`'s output wants the date the
  entry counts under, and `envel/summary.py` already has `entry_date`. Taking it would reverse the
  dependency direction the overview states. Step 5 avoids it by reading `entry.get("on")` directly,
  which is the only date AC11 asks for — an income has none and AC17 prints none.
- **`--amount` on an income and on a spend store opposite signs.** A spend's `cents` is negative and
  an income's is positive [src: ADR-0002], so a correction that wrote the typed number as-is would
  turn a spend into an income-shaped entry and quietly double an envelope's balance. Step 3
  preserves the sign the entry already carries rather than branching on `kind`, and step 9 has a
  case for each kind.
- **A removal and `next-ref`.** Lowering the counter, or deriving a reference from the list's
  length, reissues a number the person may have written down. `ADR-0010` forbids it and step 4
  states it; the risk is that it looks like tidying up.
- **AC19 is a property, not a check, and could be broken by accident.** Any operation that mutated
  the caller's document before its last refusal would break it invisibly, because the refusal path
  would still print the right message. Step 3 deep-copies only after every refusal that does not
  need the candidate, and step 9 asserts deep equality against a copy taken first.

## Out of scope for this item

- Any history of corrections, or any way to see what an entry used to say. The stakeholder chose
  against it [src: EP-001/Q-005] and `ADR-0011` option B is where that choice was weighed again.
- Changing an entry's `kind`, `at` or `ref`. The item excludes the first
  [src: WI-0005 AC16 "changes its amount with"] and `ADR-0010` and `ADR-0002` fix the other two.
- Any change to `envel/summary.py`, `envel/store.py`, `envel/money.py` or `envel/dates.py`. If a
  step seems to need one, the design has gone wrong — four criteria depend on those modules being
  untouched.
- A repair for a hand-damaged `next-ref`. `ADR-0010` left that to whoever meets one and nothing
  here meets one.
- Correcting or removing a move. `WI-0004` owns moves and AC13 makes the exclusion observable.
