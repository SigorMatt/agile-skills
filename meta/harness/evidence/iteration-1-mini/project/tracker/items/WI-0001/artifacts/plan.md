# Plan — WI-0001 Keep a roster of people that survives between runs

## Problem

This is the first code in the project: there is no `expenses` package, no `tests` directory and
no store. WI-0001 must deliver two commands — add a person, list the people — and, underneath
them, the file store that WI-0002 and WI-0003 will both use. For a member of the friend group,
what changes is that they can name their friends once and have the names still there tomorrow.

The constraints are all already recorded and none of them is negotiable here: Python 3.9+ and
standard library only, in tests as well as at runtime (`ADR-0001`); one JSON file at a fixed
per-user path, created on first write, written atomically, and **fatal to every command** if it
exists and cannot be parsed (`ADR-0002`); `python3 -m expenses <command>` with `add-person` and
`people` as the two commands here (`ADR-0006`); names case-insensitively unique, whitespace
stripped, first spelling wins (AC3, from the stakeholder's own answer). The shape of the whole
system is `docs/architecture/overview.md` v1, written as part of this plan.

## Approach

Four modules and two test files, in the layering the overview describes: `cli` is the only place
that prints or exits, the domain module is pure, and `store` is the only place that knows the
path and the format.

The one design idea worth stating is how AC8 — *no failure prints a Python traceback* — is made
true by construction rather than by remembering. `store` and `people` raise a single exception
type, `ExpensesError`, carrying a message written for a person. `cli.main()` wraps the whole
dispatch in one `except ExpensesError` that prints `str(exc)` to stderr and returns 2. Nothing
below `cli` imports `sys` or prints. There is then exactly one place to check, and adding a new
failure later cannot forget the rule.

The second is that the store is loaded and saved as a whole. The file holds a friend group's
dinners; it will never be large enough for anything cleverer to be worth the risk, and reading
the whole document is what makes the atomic replace in `ADR-0002` simple enough to be obviously
correct.

## Steps

1. **`expenses/__init__.py`, `expenses/__main__.py`, `tests/__init__.py`.** `__main__.py` is two
   lines: import `main` from `expenses.cli` and `sys.exit(main())`. Afterwards `python3 -m
   expenses` runs and `python3 -m unittest discover -s tests -t .` exits 0 with zero tests
   collected, which is what `tracker/project.yaml`'s `commands.test` needs in order to be a
   command that runs rather than one that errors.

2. **`expenses/errors.py`** — `class ExpensesError(Exception)`. One type, whose `str()` is the
   message the user sees. Nothing else in it.

3. **`expenses/store.py`** — the only module that knows the path or the format. Public surface:
   - `store_path() -> pathlib.Path` — `EXPENSES_STORE` if set and non-empty, else
     `$XDG_DATA_HOME/expenses/store.json`, else `~/.local/share/expenses/store.json`
     (`ADR-0002` decisions 1–2).
   - `load() -> dict` — returns `{"version": 1, "people": [], "expenses": []}` when the file does
     not exist. Raises `ExpensesError` naming the path and what was wrong when the file exists
     but cannot be read or parsed, or parses to something that is not a dict with the expected
     keys. It must not repair, ignore, or truncate anything (`ADR-0002` decision 6).
   - `save(data: dict) -> None` — creates missing parent directories, writes to a temporary file
     in the same directory, then `os.replace`s it over the store (`ADR-0002` decisions 4 and 7).
   Afterwards the store's whole lifecycle exists and is testable on its own.

4. **`expenses/people.py`** — pure roster rules, no I/O, no printing. Public surface:
   - `normalise(name: str) -> str` — strips surrounding whitespace; raises `ExpensesError` if the
     result is empty or contains a control character (`< U+0020` or `U+007F`), per `ADR-0006`
     rules 4–5. This is the *only* place a name is validated.
   - `match_key(name: str) -> str` — the normalised name lowercased. AC3's comparison key.
   - `add(data: dict, name: str) -> None` — normalises, and raises `ExpensesError` naming the
     existing person if `match_key` collides with one already present. Otherwise appends the
     normalised spelling to `data["people"]`, which is a list, so insertion order is the storage
     order and AC1/AC2's ordering needs no separate field.
   - `listing(data: dict) -> list[str]` — the stored spellings, in order.

5. **`expenses/cli.py`** — `argparse` with two subcommands, `add-person NAME` and `people`, both
   reachable from `python3 -m expenses --help` (AC1). `main(argv=None) -> int`:
   - dispatches, catching `ExpensesError` once: message to stderr, return 2;
   - `add-person` calls `store.load()`, `people.add()`, `store.save()`, prints a confirmation on
     stdout, returns 0. The order matters: `load` first means a damaged store aborts before
     anything is written (AC6);
   - `people` calls `store.load()` and prints one name per line, or the empty-group message when
     the roster is empty (AC1, AC4);
   - argparse's own errors — a missing `NAME` — already exit 2 with a message on stderr and no
     traceback, which is AC7's third case; do not re-implement it.

6. **`tests/test_store.py`** — the store in isolation, using `EXPENSES_STORE` pointed into a
   `tempfile.TemporaryDirectory`: a missing file loads as an empty group; `save` creates missing
   parents; a file of invalid JSON raises and, after the attempt, is **byte-for-byte unchanged**;
   a `save` against a damaged store raises without replacing it.

7. **`tests/test_cli.py`** — the CLI end to end, running `python3 -m expenses …` with
   `subprocess.run` and a temporary `EXPENSES_STORE`, asserting stdout, stderr and exit status.
   A subprocess is required, not preferred: AC2 is a claim about a **fresh process** and AC8 is a
   claim about what reaches the user's terminal, and neither can be tested by calling `main()`
   in-process.

8. **Run the gates.** `python3 -m unittest discover -s tests -t .` must exit 0. There is no lint
   command by `ADR-0001` §4, so `implement` records `no-lint-errors` as **skipped** citing that
   ADR — not as passed.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 5 | `tests/test_cli.py`: `--help` output contains `add-person` and `people`; after adding Alice then Bob, `people` prints exactly `"Alice\nBob\n"` on stdout with exit 0 |
| AC2 | 3, 4, 5 | `tests/test_cli.py`: `add-person` twice in two `subprocess.run` calls, then `people` in a **third**, asserting `"Alice\nBob\n"` — three separate interpreters, so nothing survives in memory |
| AC3 | 4 | `tests/test_cli.py`: after `add-person Alice`, each of `add-person alice`, `add-person ALICE` and `add-person "  Alice  "` exits non-zero, names `Alice` on stderr, and leaves `people` printing exactly `"Alice\n"` |
| AC4 | 5 | `tests/test_cli.py`: `people` against a temporary directory with no store exits 0 and prints the empty-group message on stdout |
| AC5 | 3, 5 | `tests/test_store.py`: `save` into a path whose parent does not exist creates it. `tests/test_cli.py`: `add-person Alice` into an empty temporary directory exits 0, and `people` in a fresh process prints `"Alice\n"` |
| AC6 | 3, 5 | `tests/test_cli.py`: write `not json` to the store, then assert **both** `people` and `add-person Bob` exit non-zero with the path on stderr, and that the file's bytes are unchanged after both |
| AC7 | 4, 5 | `tests/test_cli.py`: `add-person ""`, `add-person "   "` and `add-person` with no argument each exit non-zero, print to stderr, and leave `people` reporting an empty group |
| AC8 | 2, 5 | `tests/test_cli.py`: for every failing invocation above, assert `"Traceback"` is absent from both streams, stderr is non-empty, stdout is empty, and the exit status is non-zero; and that every succeeding invocation prints on stdout with exit 0 |

## Assumptions

Each is reversible in the sense `plan` step 4 requires — one file, no data migration, no
published interface:

1. **The store's top-level shape is `{"version": 1, "people": [...], "expenses": [...]}`,** with
   `expenses` present and empty from the start. Reversing: `store.load()`'s default and its
   validation, one file. `version` is carried so a later format change is detectable; nothing
   reads it yet, and nothing should pretend to.
2. **`people` is a list of strings**, not of objects. WI-0001's `## Out of scope` says a person
   has no attribute other than their name. Reversing costs a migration, so if any attribute is
   ever wanted this assumption is the thing to revisit first — it is the least reversible choice
   in this plan and is called out for that reason.
3. **The failure exit status is 2**, matching what `argparse` already uses for a usage error, so
   the tool does not have two different meanings for "you got it wrong". No criterion depends on
   the number; all of them say "non-zero".
4. **The confirmation and empty-group wording** — "Added Alice.", "Nobody in the group yet." No
   criterion fixes the text, only the stream and the exit status. Tests must assert on those and
   on a substring, not on the whole sentence, or the wording becomes an untouchable interface.

## Decisions and ADRs

- `ADR-0006-cli-surface-and-what-a-name-may-contain.md` — **new, written for this item.**
  `refine` handed `plan` one explicit gap: what characters a name may contain. It is answered by
  deciding the sharer syntax first (a repeated `--with` flag, never a delimiter), which is what
  makes the permissive name rule possible. Route: *decided*.
- `ADR-0002` — the store's path, format, creation, damage rule and atomicity. Route: *documented*;
  steps 3 and 5 implement it and add nothing to it.
- `ADR-0001` — Python 3.9+, standard library only, `unittest`. Route: *documented*. It is why
  `tests/` uses `subprocess` and `tempfile` rather than a fixture library.
- `ADR-0004` decision 1 — money as integer minor units. Not exercised by this item, which stores
  no amounts, but `expenses/money.py` is reserved for it in the overview so WI-0002 does not
  invent a second place to parse `"12.50"`.
- **Nothing was asked of the human.** No decision here is irreversible or depends on intent the
  record does not hold, so `question.md` §1's third branch did not apply.

## Risks

- **`str.lower()` is not full Unicode case-folding.** AC3 matches case-insensitively; for names
  in scripts with multi-character case mappings, `lower()` and `casefold()` differ. `ADR-0006`
  records this as accepted for a friend group. It would surface as two people the tool considers
  distinct who a human would not — visible in the listing, not silent, which is why it is
  acceptable.
- **`os.replace` is atomic only within one filesystem.** The temporary file must be created in
  the store's own directory, not in `/tmp`. Step 3 says so; getting it wrong turns the atomic
  write into a copy and reintroduces exactly the half-written file `ADR-0002` decision 7 exists
  to prevent. It would pass every test in this item.
- **Assumption 2 (`people` as bare strings) is the one thing here that costs a migration.** If
  anything is ever wanted alongside a name, the store's shape changes and existing files must be
  read in the old form. Recorded because it is the only irreversible-ish choice in this plan, and
  because WI-0001's `## Out of scope` is currently what justifies it.
- **`commands.test` does not run until step 1 exists.** `python3 -m unittest discover -s tests
  -t .` currently raises `ImportError: Start directory is not importable: 'tests'`, because there
  is no `tests/` yet. Step 1 creates `tests/__init__.py`, after which it exits 0. This is stated
  rather than glossed: the command is written into `project.yaml` by this plan and is not yet
  green, and the first thing `implement` does must be to make it so.

## Out of scope for this item

- Recording expenses, computing balances, and the `add-expense`, `expenses` and `settle`
  commands. `ADR-0006` fixes their spelling so the CLI stays coherent; WI-0002 and WI-0003 build
  them.
- Removing or renaming a person, and any attribute of a person beyond their name — WI-0001's own
  `## Out of scope`.
- `expenses/money.py`, `balances.py`, `expenses.py` and `settle.py`. Named in the overview as
  the system's shape; **not created empty by this item.** A placeholder module with nothing in it
  reads as a decision already taken.

---

## Correction — appended 2026-08-21T03:39:41Z by `review-close`

**Nothing above this line has been changed.** This section is appended, not edited, for the
reason `spec/journal-and-history.md` gives for correcting a wrong entry: a later entry that says
what was wrong preserves the evidence, and a rewrite destroys it. What this plan believed when it
was written is the most useful thing in WI-0001's record for whoever plans WI-0002, and that
includes the part that turned out to be wrong.

### The claim

`## Approach`, the paragraph beginning *"The one design idea worth stating…"*:

> `cli.main()` wraps the whole dispatch in one `except ExpensesError` that prints `str(exc)` to
> stderr and returns 2. Nothing below `cli` imports `sys` or prints. There is then exactly one
> place to check, and adding a new failure later cannot forget the rule.

### Why it is false

One `except ExpensesError` makes AC8 true only for failures somebody remembered to raise as an
`ExpensesError`. It is not "true by construction"; it is true by a discipline applied in every
module below `cli`, which is the thing the sentence claims not to depend on.

The counter-example is on the record. `store.load()` validated that `people` was a list but not
what was in it, so `{"version": 1, "people": [123], "expenses": []}` parsed cleanly and then
raised `AttributeError` out of `people.normalise()`. It escaped the single handler and reached the
user as a traceback with exit 1 — a direct violation of the AC8 this paragraph was explaining how
to guarantee. See `artifacts/review.md` F1 and F3, and `artifacts/impl-report.md`
`## Third pass — the review's F1, F2 and F3`.

### What corrected it

- `expenses/cli.py` now has a **second** handler, `except Exception`, behind the first. It reports
  the exception type and message on one line, says the failure is the tool's fault, exits
  non-zero, and does not catch `BaseException`. That handler, not the layering, is what makes AC8
  unconditional. It is a declared deviation from step 5 of this plan.
- `expenses/store.py` `load()` now checks the type of every roster entry, so the damaged store
  that produced the traceback is rejected with a named error from both commands instead.
- `docs/architecture/overview.md` is at **v2** and is the current authority on how AC8 is
  guaranteed. `expenses/errors.py`'s docstring carried the same false sentence and was corrected
  too.

### Why it was worth appending here rather than only pointing at it from elsewhere

The failure mode `spec/dor-dod.md` D12 exists to catch is a sentence being **re-quoted rather than
re-checked**, and this one had already spread to three files before anyone read it against the
code. A correction that lives only in `item.md` is one file away from the reader who is being
misled by the paragraph above. It belongs in the file being quoted.

`plan.md` is not among `review-close`'s declared outputs, so this is a deliberate step outside
that list; it is flagged as such in `artifacts/review.md` `## The plan.md handover` and in the
journal entry for this execution, rather than done quietly. `implement` declined to make the edit
itself and handed the decision here by name, which was the right call — this artifact belongs to
`plan`, and only an append leaves `plan`'s reasoning intact.
