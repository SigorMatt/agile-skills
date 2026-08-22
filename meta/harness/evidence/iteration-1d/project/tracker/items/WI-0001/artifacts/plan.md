# Plan — WI-0001 Record people and shared expenses that survive between runs

## Problem

Build the part of the tool that **records and keeps** the group's data: the people, the expenses
(who paid, how much, what for, who shared it, on what date) and the repayments (who paid whom
back). It must be usable from a terminal by one person, it must still have everything the next
time the process runs, and it must be able to keep more than one set of books because the
stakeholder wants a trip's expenses separate from the flat's [src: WI-0001/Q-004].

It must **not** compute who owes whom — that is WI-0002 — but it must store an expense in a shape
from which WI-0002 can compute it exactly: one total and a set of sharers, never a per-person
amount [src: WI-0001 AC5]. Twelve acceptance criteria constrain it, most of them about what is
refused rather than what is accepted, because refusals are where this kind of tool goes wrong.

Constraints already fixed and not reopened here: repayments are their own record kind
(`ADR-0001`); amounts are plain two-decimal numbers and the payer absorbs an uneven split's
remainder (`ADR-0002`); splits are always equal [src: WI-0001/Q-001]; names match case- and
space-insensitively [src: WI-0001/Q-005].

## Approach

One Python package, `expenses/`, run as `python3 -m expenses`, in three modules whose
responsibilities do not overlap. `docs/architecture/overview.md` v1 describes the shape;
`ADR-0003`, `ADR-0004` and `ADR-0005` record the three decisions this plan had to make.

The design's one real idea is that **validation lives in `model.py`, not in `cli.py`.** Every rule
about what an acceptable name, amount or date is becomes a function the CLI calls. That costs
nothing now and is the reason WI-0003's CSV importer cannot end up accepting an amount or a date
the hand-entry command refuses — the two will call the same function or they will not agree, and
"the two parsers drifted" is the failure `ADR-0002` explicitly worried about.

The second idea is that **every command is the same shape**: resolve the ledger path, load, apply
one change, save atomically, print, exit 0 — or raise a validation error that `cli.py` turns into
a stderr line and exit 2, having saved nothing. Six commands sharing one skeleton is what makes
"a refusal changes no recorded data" true by construction rather than by remembering it six times.

### The interface this item delivers

```
python3 -m expenses [--file PATH] <command> [options]

  add-person   NAME
  people
  add-expense  --payer NAME --amount AMOUNT --description TEXT
               [--shared-by NAME ]... [--date YYYY-MM-DD]
  expenses
  repay        --from NAME --to NAME --amount AMOUNT [--date YYYY-MM-DD]
  repayments
```

`--shared-by` is repeatable and takes one name each time; a comma-separated list would break on a
name containing a comma. Omitting it entirely is what AC4 means by "without naming any sharers" —
distinct from passing it with no value, which `argparse` refuses on its own.

`--file` is global and precedes the subcommand. `EXPENSES_LEDGER` does the same job for a whole
shell session (`ADR-0003`).

## Steps

Each step ends with something observable. Tests come with the step that makes them pass, not at
the end: `commands.test` exits **5** while `tests/` is empty
[src: run: `python3 -m unittest discover -s tests -t . -q` → exit 5, "NO TESTS RAN"], so the
`tests-pass` gate cannot go green on an empty suite.

1. **`expenses/model.py` — the validators.** Add `normalise_name(text) -> str`
   (`text.strip().casefold()`, for matching only), `parse_amount(text) -> int` and
   `format_amount(minor) -> str` per `ADR-0004`, and `parse_date(text) -> datetime.date` which
   requires `^\d{4}-\d{2}-\d{2}$` **before** calling `datetime.date.fromisoformat`. The regex is
   not redundant: `fromisoformat` accepts `20260822`, which AC7 does not
   [src: run: `date.fromisoformat("20260822")` → 2026-08-22]. Add one exception type,
   `ValidationError`, carrying the message the user will see. Nothing in this module prints or
   exits. **After:** `tests/test_model.py` covers every accepted and refused string named in AC6
   and AC7, and `commands.test` exits 0.
2. **`expenses/model.py` — the record types.** Add `Person`, `Expense` and `Repayment` as
   dataclasses matching `ADR-0003`'s field names, plus `to_dict`/`from_dict` for each. Add
   `Ledger`, holding the three ordered lists and a `find_person(name)` that looks up by
   normalised name and returns the stored display form or `None`. **After:** `tests/test_model.py`
   shows `find_person` matching `ana`, ` Ana ` and `ANA` against a stored `Ana`, per AC1.
3. **`expenses/store.py` — locating and moving the ledger.** Add `resolve_path(cli_file)` with
   `ADR-0003`'s precedence, `load(path) -> Ledger` (a missing file returns an empty ledger; an
   unreadable one or one whose JSON is malformed raises a distinct `StoreError`), and
   `save(path, ledger)` writing UTF-8 JSON with a trailing newline via a same-directory temporary
   file and `os.replace`, creating parent directories as needed. **After:** `tests/test_store.py`
   round-trips a ledger through a `tmp` path, shows a missing file loads empty, shows two
   different paths do not see each other's data (AC9), and shows an unwritable directory raises
   `StoreError`.
4. **`expenses/cli.py` — the skeleton and `add-person` / `people`.** Build the argparse parser
   with the global `--file` and the six subcommands; add `main(argv=None) -> int` that dispatches,
   catches `ValidationError` → stderr + return 2, catches `StoreError` → stderr + return 1, and
   returns 0 otherwise. Implement `add-person` (refusing an empty or whitespace-only name, and a
   name whose normalised form is already present) and `people` (one per line, insertion order, the
   "none recorded" line when empty). Add `expenses/__main__.py` as
   `raise SystemExit(main(sys.argv[1:]))`. **After:** `tests/test_cli_people.py` covers AC1 and
   AC2 including the duplicate and empty-name refusals, and `python3 -m expenses people` runs.
5. **`cli.py` — `add-expense` and `expenses`.** Validate in this order and stop at the first
   failure: amount (AC6), date (AC7), description non-blank, payer is a recorded person, each
   `--shared-by` name is a recorded person, no name repeats among the sharers under
   `normalise_name`. With no `--shared-by`, the sharers are every person currently recorded, by
   name, resolved at this moment (AC4). Store the display forms, not the normalised ones. Then
   `expenses` prints date, payer, amount, description and sharers per record in insertion order,
   with the "none recorded" line when empty. **After:** `tests/test_cli_expenses.py` covers AC3,
   AC4, AC5, AC6, AC7 and AC8, including that a refused command leaves the file byte-identical.
6. **`cli.py` — `repay` and `repayments`.** Same shape: amount, date, both people recorded, and
   `--from` and `--to` must not normalise to the same person. A repayment between people with no
   shared expense is accepted. `repayments` prints date, from, to and amount in insertion order,
   with the "none recorded" line when empty, and never prints an expense; `expenses` never prints
   a repayment. `--from`/`--to` need explicit `dest=` because `from` is a Python keyword.
   **After:** `tests/test_cli_repayments.py` covers AC11 and AC12 including the self-repayment
   refusal and the two-listings separation.
7. **Persistence and the location, end to end.** Add `tests/test_persistence.py` driving the
   installed commands through `subprocess` — a real second process, not a second call to `main()`
   — recording people, expenses and repayments under a temporary `--file`, then listing them from
   a fresh process and comparing output exactly, including order (AC10). Include a run where
   `EXPENSES_LEDGER` points at one path and `--file` at another, asserting `--file` wins
   (`ADR-0003`). **After:** every AC has at least one test, and `commands.test` and
   `commands.lint` both exit 0.
8. **README-level usage, if and only if it is short.** Add the six invocations and the two ways to
   choose a ledger to `docs/architecture/overview.md`'s successor only if implementation changed
   the shape; otherwise leave the docs alone. A version bump with no substantive change devalues
   every other one [src: .claude/agile-skills/spec/doc-header.md].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — add a person; empty and duplicate names refused, matching trimmed and case-ignoring | 2, 4 | `tests/test_cli_people.py`: add `Ana` → exit 0; add `ana`, ` Ana `, `ANA` → exit 2 each, stderr names the duplicate, `people` still prints one line; add `""` and `"   "` → exit 2 |
| AC2 — list people, one per line, first-typed form, insertion order, "none" line when empty | 4 | `tests/test_cli_people.py`: `people` on an empty ledger → exit 0 and the none-recorded line; add `Ana`, `ben`, `Cara` → exactly those three lines, in that order, with that capitalisation |
| AC3 — record an expense; unknown name, repeated sharer, blank description refused; payer need not share | 5 | `tests/test_cli_expenses.py`: happy path → exit 0; `--payer Dan` (unrecorded) → exit 2; `--shared-by Ana --shared-by ana` → exit 2; `--description ""` → exit 2; payer not in `--shared-by` → exit 0 and the stored sharers exclude them |
| AC4 — no `--shared-by` shares among everyone recorded at that moment | 5 | `tests/test_cli_expenses.py`: with Ana and Ben recorded, record with no `--shared-by`; add Cara; `expenses` shows sharers `Ana, Ben` and not Cara |
| AC5 — one amount and a set of sharers on disk, no per-person amount; usage shows no share option | 3, 5 | `tests/test_cli_expenses.py`: record 60 shared by three, then `json.load` the ledger file — `expenses[0]` has `amount_minor == 6000`, `sharers` of length 3, and no key holding a per-sharer amount; `add-expense --help` output contains no share/split option |
| AC6 — the amount grammar, and eleven named refusals | 1, 5 | `tests/test_model.py` asserts `parse_amount` on `12`, `12.5`, `12.50` → `1200`, `1250`, `1250`, and raises on `0`, `0.00`, `-5`, `+5`, `12.`, `.5`, `12.505`, `1,234.56`, `€12.50`, `abc`, `""`; `tests/test_cli_expenses.py` runs three of them through the CLI → exit 2, ledger unchanged |
| AC7 — a date, defaulting to today, `YYYY-MM-DD` only | 1, 5 | `tests/test_model.py`: `parse_date` accepts `2026-08-22`, raises on `22/08/2026`, `2026-8-1`, `2026-13-01`, `2026-02-30`, `today` **and** `20260822`; `tests/test_cli_expenses.py`: omitting `--date` stores `datetime.date.today().isoformat()` |
| AC8 — list expenses with all five fields, insertion order, "none" line when empty | 5 | `tests/test_cli_expenses.py`: empty → the none-recorded line, exit 0; two expenses → two entries in order, each containing the date, payer, formatted amount, description and every sharer name |
| AC9 — one default location; `--file` picks another; the two are independent; created on first write; unusable location refused | 3, 7 | `tests/test_store.py` + `tests/test_persistence.py`: record under `tmp/a.json`, list with `--file tmp/b.json` → the none-recorded line; list with `--file tmp/a.json` → the record; `--file` into a non-existent nested directory → created; into a read-only directory → exit 1 with a stderr message |
| AC10 — everything survives process exit, same fields, same order | 7 | `tests/test_persistence.py`: one `subprocess` run records two people, two expenses and one repayment; a **second** `subprocess` run of each listing command produces byte-identical output to a third run |
| AC11 — record a repayment; unknown name and self-repayment refused; allowed with no shared expense | 6 | `tests/test_cli_repayments.py`: `repay --from Ana --to Ben --amount 20` with no expenses recorded → exit 0; `--from Ana --to ana` → exit 2; `--from Dan` (unrecorded) → exit 2 |
| AC12 — list repayments; insertion order; "none" line; neither listing shows the other's records | 6 | `tests/test_cli_repayments.py`: with one expense and one repayment recorded, `expenses` output contains the description and not the repayment amount, and `repayments` output contains the repayment and not the description |

## Assumptions

Each is reversible in the sense `spec/question.md` §1 means: one file, no data migration, no
published interface anyone else depends on yet.

1. **`python3 -m expenses` is "a command".** The criteria deliberately say "a command" and name
   no invocation [src: WI-0001]. Reversing: adding a console-script entry point later is a
   `pyproject.toml` and no change to any module.
2. **Exit code 2 for every refusal, 1 for a ledger that cannot be read or written.** The criteria
   only require "non-zero". `argparse` already exits 2 for usage errors, so this makes the tool
   self-consistent rather than having two kinds of bad input exit differently. Reversing: one
   constant in `cli.py`.
3. **`--shared-by` is repeatable rather than comma-separated.** Reversing: one `argparse` line,
   though it would be a user-visible change if anyone had scripted against it.
4. **The "none recorded" line goes to stdout, not stderr, and the exit code is 0.** It is not an
   error; it is the answer. Reversing: three print statements.
5. **A ledger whose JSON is malformed is a `StoreError` (exit 1), not a crash and not an empty
   ledger.** Silently treating a corrupt file as empty would let the tool overwrite real data with
   nothing, which is the worst outcome available. Reversing: one `except` clause — but the
   direction that matters is that it must never be "start over silently".
6. **Sharer names are stored in display form, not normalised form.** AC8 must print names as the
   person typed them, and the normalised form is a lookup key rather than data [src: WI-0001 AC1].
   Reversing: would be a data migration once a ledger exists, so this one is only cheap now.

## Decisions and ADRs

| decision | route | record |
|----------|-------|--------|
| The ledger is one JSON document at an XDG default, chosen per run by `--file` / `EXPENSES_LEDGER`, written atomically | decided | `ADR-0003` |
| Money is integer minor units everywhere; no float, no `Decimal` | decided | `ADR-0004` |
| Standard library only — `argparse`, `unittest`, and a `compileall` syntax check standing in for a linter | decided | `ADR-0005` |
| A repayment is its own record kind, not a negative expense | documented | `ADR-0001`, followed |
| Amount format, and the payer absorbing the split remainder | documented | `ADR-0002`, followed; `ADR-0004` restates the remainder rule as integer `divmod` for WI-0002 |
| Splits are always equal; names match case- and space-insensitively; a date defaults to today | documented | the stakeholder's answers on `Q-001`, `Q-005`, `Q-003`, already in the criteria |
| The three-module split, and validation living in `model.py` | decided | `docs/architecture/overview.md` v1 |

Nothing was asked of the human. Every decision above was either already recorded or reversible in
the sense above, which is the middle branch of `plan`'s preference order rather than the top or
the bottom of it.

## Risks

- **The lint gate checks less than its name says.** `compileall` finds syntax errors and nothing
  else (`ADR-0005`). A `no-lint-errors` pass on this project means every file parses. The
  mitigation is that it is written down in three places; the residual risk is a reviewer reading
  more into a green gate than is there.
- **Whole-file rewrite on every command.** Fine for a friend group; wrong somewhere around tens of
  thousands of records, where the rewrite becomes noticeable. `ADR-0003` records the threshold
  reasoning and `version` is the field a change would key on. Nothing in the epic suggests that
  scale [src: docs/product/vision.md].
- **AC5 asks `verify` to read the ledger file.** That makes `ADR-0003`'s JSON shape part of the
  contract, not an internal detail — a later change to the field names would break an acceptance
  criterion rather than only some code. Stated so that the coupling is deliberate.
- **AC7's default date is the machine's local date**, so a test that records an expense at
  23:59:59 and asserts the date at 00:00:00 will fail once a day. The test must capture
  `date.today()` in the same run rather than hard-coding a date.
- **`argparse` owns some behaviour this plan does not.** Unknown options, missing required
  arguments and `--help` are its output, in its wording, exiting 2. No AC constrains that wording,
  and AC5 depends on its `--help` listing the real options — which it does by construction.
- **The plan assumes `tests/` and `expenses/` exist as packages.** `plan` created both as empty
  `__init__.py` files so that `commands.test` and `commands.lint` could be run before being
  recorded. If a later execution finds them missing, the two commands will fail for a reason that
  has nothing to do with the code.

## Out of scope for this item

- Computing who owes whom, and netting repayments into it. WI-0002, which consumes the ledger
  this item writes.
- Reading a bank CSV. WI-0003, which will reuse `model.py`'s validators (`ADR-0005`).
- Editing or deleting a recorded person, expense or repayment; there is no undo [src: WI-0001].
- Packaging, an installable entry point, or a `pyproject.toml` (`ADR-0005`).
- Any output beyond the three listings — no filtering, no sorting, no export [src: WI-0001].
- Migrating an older ledger format. `version` exists so that a future change has somewhere to
  branch; nothing is on disk to migrate (`ADR-0003`).
