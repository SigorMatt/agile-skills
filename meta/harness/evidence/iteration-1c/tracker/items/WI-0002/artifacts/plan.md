# Plan — WI-0002 Record an expense paid by one person and shared by several

## Problem

The tool knows who the friends are; it does not yet know that anyone spent anything. This item adds
`add-expense` and `list-expenses`, so that the person keeping the books can record — at the moment
it happens — that one friend paid an amount for something on a date, and which of the group shared
in it. Nothing here computes a balance; WI-0003 does that from the records this item writes, which
is why the *stored shape* matters more than anything else in the change.

The constraints are all recorded and none of them is this plan's to revisit: shares are always
equal and no per-person amount may be accepted (WI-0002/Q-001); every expense carries a date, and
an undated one takes the machine's **local** date (Q-002, and Q-003 which amended AC6 to say so);
money is a whole number of pence and never a float (ADR-0001); the surface is `./expenses
<subcommand>` with `--data-file` on every subcommand (ADR-0002, ADR-0004); confirmations go to
stdout with exit 0, refusals to stderr with exit 1 and store nothing (ADR-0005); and the data file
is read strictly and written atomically (ADR-0006).

## Approach

Two new modules beside the existing ones, following ADR-0008's split rather than reshaping it:

- **`expenses_tool/money.py`** — parsing an amount string into integer pence and formatting pence
  back to two decimal places. It is the only place that knows how a money string is spelled, and it
  is a value converter, not a message: it raises, it never prints.
- **`expenses_tool/expenses.py`** — the rules over an expense record: resolving names to registered
  people, checking the date, building the record ADR-0009 fixes, and returning the expenses in the
  order they are listed. Like `store.py`, it never prints and never exits.

`cli.py` gains the two subcommands and — importantly — **the single rendering function**, because
ADR-0008 clause 3 puts every user-visible string in `cli.py`. The rendering the item defines above
its criteria is used by both the confirmation and the listing, so there is one string to check and
one place it can change.

Validation happens strictly before any write, so AC9's "every refusal leaves the recorded history
intact" is a property of the control flow rather than something asserted afterwards — the same
discipline WI-0001 used, and the reason it holds there.

## Steps

1. **`expenses_tool/money.py` — parsing and formatting.** `parse_amount(text) -> int` accepts
   `re.fullmatch(r"\d+(\.\d{1,2})?", text)` and returns whole pence computed with integer
   arithmetic (`int(whole) * 100 + int(fraction padded to two digits)`); it raises
   `InvalidAmount(text)` for anything else, **including** a well-formed number with three decimal
   places and any value that comes to zero pence. `format_amount(pence) -> str` returns
   `f"{pence // 100}.{pence % 100:02d}"`. No `float` and no `Decimal` appears anywhere in the file
   (ADR-0001 clause 1). Afterwards: `30`, `30.5`, `30.00` all parse to the same integer, and
   `1.005`, `-5`, `abc`, `0` all raise.

2. **`expenses_tool/expenses.py` — resolving people.** `resolve_person(data, name) -> str` returns
   the stored display name whose `store.normalise` matches, and raises `UnknownPerson(name)` —
   carrying the name **as the user typed it**, which AC4 quotes — otherwise.
   `resolve_sharers(data, text_or_none) -> list[str]`: when the text is `None`, return every
   registered person sorted by `store.normalise` (the snapshot of ADR-0009 clause 3); otherwise
   split on `,`, strip each part, raise `NoSharers()` if the result is empty or every part is
   blank, resolve each part, and raise `DuplicateSharer(stored_name)` if two parts resolve to the
   same person — carrying the **stored** spelling, which AC8 quotes.

3. **`expenses_tool/expenses.py` — the date.** `parse_date(text) -> str` accepts only
   `YYYY-MM-DD` that `datetime.date.fromisoformat` accepts *and* whose text is exactly ten
   characters in that layout, returning it unchanged; it raises `InvalidDate(text)` otherwise.
   `today() -> str` returns `datetime.date.today().isoformat()` — the machine's local clock and
   timezone, per WI-0002/Q-003, and explicitly **not** `datetime.datetime.now(timezone.utc)`.

4. **`expenses_tool/expenses.py` — building and reading records.**
   `record_expense(data, *, paid_by, amount_pence, description, sharers, date) -> dict` validates
   that the description is not blank (raising `BlankDescription()`), builds the record ADR-0009
   clause 4 fixes, appends it to `data.setdefault("expenses", [])` and returns it.
   `list_expenses(data) -> list[dict]` returns `sorted(data.get("expenses", []), key=date)` using a
   stable sort, so equal dates keep the order they were recorded in (AC3).

5. **`expenses_tool/store.py` — the new key.** No structural change: `load` already tolerates a
   missing key, but its strict read must now also accept and validate `expenses` — a list of
   objects, each with the five keys ADR-0009 clause 4 names, with `amount_pence` an `int`. A file
   whose `expenses` are not that shape raises `DataFileError` with a specific reason, exactly as a
   malformed `people` list does. Afterwards: a WI-0001-era file with no `expenses` key still loads,
   and a corrupted one is still refused rather than overwritten.

6. **`expenses_tool/cli.py` — the rendering.** `render_expense(expense) -> str` returns
   `f"{date} {format_amount(pence)} {description} — paid by {paid_by}, shared by {', '.join(shared_by)}"`,
   with the sharers in `store.normalise` order. It is used by both new subcommands, and it is the
   only place this string exists.

7. **`expenses_tool/cli.py` — `add-expense`.** Options `--paid-by`, `--amount`, `--description`
   (all three `required=True`, so omitting one is `argparse`'s exit 2), `--date`, `--shared-by`,
   plus the shared `--data-file`. Order of operations, which is what AC9 depends on: load; parse
   the amount; parse or default the date; resolve the payer; resolve the sharers; check the
   description; build the record; **then** save; then print `Added <render_expense(...)>`. Map each
   failure to exactly these, on stderr, returning 1 with nothing written:
   - `InvalidAmount(value)` → `Amount must be a positive number with at most two decimal places: <value>`
   - `InvalidDate(value)` → `Date must be a calendar date in YYYY-MM-DD form: <value>`
   - `UnknownPerson(name)` → `Unknown person: <name>`
   - `DuplicateSharer(stored)` → `<stored> is named twice in --shared-by`
   - `NoSharers()` → `--shared-by must name at least one person`
   - `BlankDescription()` → `An expense needs a description`
   - `store.DataFileError` → `Cannot read <path>: <reason>` (unchanged from WI-0001)

8. **`expenses_tool/cli.py` — `list-expenses`.** Load; if there are no expenses print exactly
   `No expenses recorded yet` on stdout and return 0 (ADR-0005 clause 4); otherwise print
   `render_expense` for each, in `list_expenses` order, and return 0. A `DataFileError` is refused
   as everywhere else.

9. **`tests/test_money.py`.** `parse_amount` on `30`, `30.5`, `30.00`, `0.01`; the raising cases
   `0`, `0.00`, `-5`, `abc`, `1.005`, `""`, `30.`, `1,000`, ` 30 `; `format_amount` on `3000`,
   `3050`, `1`, `0`; and a round-trip over a range of values asserting `parse_amount(format_amount(p)) == p`.

10. **`tests/test_expenses.py`.** `resolve_person` for an exact match, a case-different match and
    an unknown name (checking the exception carries the name as typed); `resolve_sharers` for the
    omitted case (snapshot, normalised order), an explicit list, a case-different duplicate
    (checking the exception carries the *stored* spelling), an empty string and a whitespace-only
    entry; `parse_date` for a valid date and for `2026-13-01`, `14/08/2026`, `today`, `2026-8-1`;
    `record_expense` appending exactly one record with the five keys ADR-0009 names and rejecting a
    blank description; `list_expenses` ordering two dates and preserving insertion order on a tie.

11. **`tests/test_cli_expenses.py`.** One class per acceptance criterion, AC1 to AC9, each running
    `./expenses` in a subprocess from the repository root against a data file in a
    `TemporaryDirectory`, registering the people it needs first, and comparing stdout, stderr and
    the exit code exactly. AC6's default-date test compares the rendered line's first field against
    Python's own `datetime.date.today().isoformat()`, which is the same clock `date +%F` reads.
    AC4, AC8 and AC9 additionally read the data file's bytes before and after.

12. **`README.md`.** Add the two commands to the command table with a worked example, the amount
    grammar, what `--shared-by` defaults to and that it is snapshotted, and the date default. The
    README is documentation, not a criterion, for this item — but leaving it describing a tool that
    only knows people would make it wrong.

13. **Run both project commands** — `python3 -m unittest discover -s tests -t . -q` and
    `python3 -m compileall -q expenses expenses_tool tests` — from the repository root, on the
    final state of the code (`spec/dor-dod.md` D3).

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the recorded expense and its confirmation; `--share-amount` is a usage error | 1, 2, 4, 6, 7 | `test_cli_expenses.py::AC1::test_records_and_confirms` — asserts stdout is exactly `Added 2026-08-14 30.00 dinner — paid by Ana, shared by Ana, Ben, Cass\n`, stderr empty, exit 0; and `::test_share_amount_is_a_usage_error` asserting exit 2 |
| AC2 — omitted `--shared-by` snapshots everyone registered | 2, 4, 7 | `AC2::test_defaults_to_everyone_and_snapshots` — confirmation names all three; then `add-person Dan`; then `list-expenses` still shows `Ana, Ben, Cass` |
| AC3 — persistence, date order, and the empty listing | 4, 8 | `AC3::test_lists_in_date_order_across_invocations` — two records in separate invocations, the later date recorded first, asserting the two lines and their order; `::test_empty_listing` asserting `No expenses recorded yet\n` and exit 0 |
| AC4 — unknown payer or sharer; a case-different sharer is known | 2, 7 | `AC4::test_unknown_person_refused` — stderr exactly `Unknown person: Dan\n`, exit 1, `cmp` of the file before and after; `::test_case_different_sharer_resolves` asserting exit 0 and the stored spelling in the output |
| AC5 — the amount grammar | 1, 7 | `AC5::test_bad_amounts_refused` — four sub-tests comparing stderr exactly; `::test_accepted_amounts_render` asserting `30.00` and `30.50` |
| AC6 — `--date`, the local-date default, and malformed dates | 3, 7 | `AC6::test_default_date_is_todays_local_date` — compares the line's first field to `datetime.date.today().isoformat()`; `::test_bad_dates_refused` — three sub-tests comparing stderr exactly |
| AC7 — description required and non-blank | 4, 7 | `AC7::test_missing_description_is_a_usage_error` (exit 2); `::test_blank_description_refused` — stderr exactly `An expense needs a description\n`, exit 1 |
| AC8 — a duplicated or empty `--shared-by` | 2, 7 | `AC8::test_duplicate_sharer_refused` — stderr exactly `Ana is named twice in --shared-by\n`; `::test_empty_shared_by_refused` — stderr exactly `--shared-by must name at least one person\n`; both exit 1 with `cmp` unchanged |
| AC9 — every refusal leaves the history intact | 5, 7 | `AC9::test_refusals_do_not_change_the_listing` — captures `list-expenses` output, runs one refusal from each of AC4 to AC8, and asserts the listing is byte-identical after each |

## Assumptions

- **`--shared-by` is split on commas only**, with surrounding whitespace stripped from each part.
  A name cannot contain a comma (ADR-0003 clause 3), so nothing is ambiguous. Reversal — a
  repeatable `--shared-by` option — is one parser change and no stored data, and ADR-0003 already
  names it as the escape hatch if a comma in a name is ever needed.
- **An amount of exactly zero pence is refused as "not a positive number"**, so `0`, `0.00` and
  `0.001` all take AC5's message. Reversal is one comparison.
- **The expanded sharer list is stored in normalised order; an explicit list is stored in the order
  given.** Rendering sorts either way (step 6), so the stored order is not observable through any
  criterion. Reversal is one line.
- **`parse_date` requires the exact `YYYY-MM-DD` layout**, so `2026-8-1` is refused even though
  `date.fromisoformat` accepts it in Python 3.11+. AC6's own wording names that layout, and a
  ten-character check is cheap. Reversal is one condition.
- **The README is updated without a criterion demanding it.** AC7 of WI-0001 tied the README to a
  criterion; nothing here does. It is still updated, because a README that describes only half the
  tool is wrong, and because WI-0003 and WI-0004 will both extend it.

## Decisions and ADRs

- **ADR-0009 — an expense references people by their stored name, and snapshots its sharers.**
  Route: decided. Options considered were stored names, introduced IDs and normalised names, and —
  separately for the sharers — snapshotting versus a stored "everyone" marker. It is the one
  decision here that is expensive to reverse, because it is the stored shape that WI-0003 and
  WI-0004 both build on, which is why it is an ADR rather than a plan step.
- **Answered from existing documents, not re-decided:** integer pence and the split rule
  (ADR-0001 — this item stores the amount, WI-0003 divides it), the subcommand names and the option
  style (ADR-0002 clauses 3 and 4), name identity and ordering (ADR-0003), `--data-file` on every
  subcommand (ADR-0004), streams and exit codes (ADR-0005), the envelope's missing-key rule
  (ADR-0006 clause 2), the test layers (ADR-0007 clause 3), and where a user-visible string may
  live (ADR-0008 clause 3, which is why `render_expense` is in `cli.py` and not in `expenses.py`).
- **Answered from the item's own record:** the local-date default (WI-0002/Q-003, answered by
  `answer-questions` after `plan` filed it), the refusal messages and the amount grammar
  (`artifacts/refinement-qa.md`, tagged `[assumed]`).
- **No new ADR for the money module.** ADR-0001 already fixes integer pence; `money.py` is where
  that rule is implemented, not a decision about it.
- **`tracker/project.yaml` needs no change.** `commands.test` and `commands.lint` were filled in
  for WI-0001 and both still run; the new tests are discovered by the same command.
- **`docs/architecture/overview.md` will need a bump**, because this item adds two modules and a
  top-level key to the data file — that is a change to the shape of the system, which step 8 of
  this skill's procedure requires be recorded. It is updated as part of this execution rather than
  left to `implement`.

## Risks

- **`date.fromisoformat` is more permissive in newer Pythons.** In 3.11+ it accepts `20260814` and
  `2026-08-14T00:00:00`. Step 3's ten-character layout check is what keeps AC6 exact; without it,
  `--date 20260814` would be accepted and the rendered line would still read `2026-08-14`, which no
  criterion forbids but nobody intended.
- **A description that contains ` — ` makes the rendered line ambiguous to a parser.** The item's
  `## Notes` records this as deliberately unconstrained. It becomes a real problem only if
  something later parses the listing; WI-0003 reads the stored records, not the output, so nothing
  in this epic does.
- **The snapshot is invisible until someone adds a person.** AC2 tests it explicitly, and it is the
  one behaviour here that a reasonable implementation gets wrong by being lazy — storing `null` for
  "everyone" is less code today and silently rewrites history tomorrow.
- **Two people whose names differ only by accent remain two people** (ADR-0003 option C, declined).
  In this item that means `--shared-by José,Jose` is *not* a duplicate and records a four-way split
  among three people. It follows from a recorded decision and is not a defect, but it is the case
  where that decision is most visible.
- **`amount_pence` in a hand-edited data file could be a float.** Step 5's strict read requires an
  `int`, so a file edited to `"amount_pence": 30.5` is refused rather than silently producing
  fractional pence in WI-0003's arithmetic.

## Out of scope for this item

- Balances, settlements and any total (WI-0003). `list-expenses` prints records; it does not add
  them up, and the item's `## Out of scope` says so.
- The CSV import (WI-0004). It will write the same records through the same `record_expense`, but
  nothing here anticipates its file format or its import history.
- Editing or deleting an expense (EP-001).
- Filtering or searching the listing, and any output format other than the rendered line.
- Referential integrity checks at read time (ADR-0009 clause 5): only this tool writes the file,
  and nothing in this epic can remove a person.
