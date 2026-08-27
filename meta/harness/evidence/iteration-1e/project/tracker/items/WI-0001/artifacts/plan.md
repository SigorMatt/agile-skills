# Plan — WI-0001 Record people and expenses from the command line, stored on disk

## Problem

A person who keeps track of what their friend group spends needs to name the people in the group
and record each expense — how much, who paid, who shared it, when, and what it was for — and find
all of it still there tomorrow. Nothing exists yet: this is the first code in the project, so the
plan has to create the package, the data store and the command surface as well as the behaviour.
The constraints are the stakeholder's — python3 and its standard library, no network, no external
services, one machine — and refinement's: an expense divides equally between its named sharers,
the shares must sum to exactly the amount paid, and every refusal must leave the stored data
untouched. Working out who owes whom is a later item and is not built here.

## Approach

One package, `expenses/`, run as `python3 -m expenses`, layered one way:

- **`money.py`** knows about amounts and nothing else: parse a string to minor units, format
  minor units back, split an amount equally between `n` sharers. No I/O, no printing.
- **`store.py`** knows about the dataset: where the file is, how to read it, how to write it
  atomically, and what a valid dataset looks like. It exposes `load()`, `save()`, and the
  operations `add_person`, `add_expense`, `people`, `expenses`. It raises on refusal and prints
  nothing.
- **`cli.py`** knows about the command line: the argparse surface, one handler per command, all
  formatting and all printing, and the single place where a refusal becomes a message on stderr
  and a non-zero exit code.
- **`__main__.py`** is three lines: call the CLI with `sys.argv[1:]`, exit with what it returns.

Refusals travel as one exception type, `ExpensesError`, raised by `money.py` and `store.py` and
caught in exactly one place in `cli.py`. This is what makes "a refusal changes nothing on disk"
[src: WI-0001 AC5; WI-0001 AC6] a property of the design rather than a promise repeated in each
handler: every validation happens before `store.save()` is called, and `save()` is the only
function that writes.

The four decisions this design rests on are recorded as ADRs, not buried here: the store's
location and format [src: ADR-0001], money as integer minor units [src: ADR-0002], the remainder
rule for an uneven split [src: ADR-0003], and the project's test and lint commands
[src: ADR-0004].

Interfaces this plan fixes (signatures are the architect's; the bodies are not):

```python
# money.py
parse_amount(text: str) -> int          # minor units; raises ExpensesError
format_amount(minor: int) -> str        # "1250" -> "12.50"
split_equally(minor: int, n: int) -> list[int]   # len == n, sums to minor

# store.py
store_path() -> pathlib.Path
load(path) -> dict                      # missing file -> {"version": 1, "people": [], "expenses": []}
save(path, data) -> None                # atomic replace
add_person(data, name: str) -> None     # raises on empty or duplicate
add_expense(data, amount_minor, paid_by, shared_by, date, description) -> None
```

## Steps

1. **Create the package skeleton.** `expenses/__init__.py` (empty) and `expenses/__main__.py`.
   `__main__.py` contains `from expenses.cli import main` and
   `sys.exit(main(sys.argv[1:]))` under `if __name__ == "__main__":`. Afterwards
   `python3 -m expenses` runs and fails only because `cli.py` does not exist yet.

2. **Write `expenses/money.py`.** Define `ExpensesError(Exception)` here, since it is the lowest
   layer. `parse_amount` matches the whole string against `^\d+(\.\d{1,2})?$` after stripping
   surrounding whitespace, converts to minor units, and raises `ExpensesError` for anything else
   or for a result of zero — so `0`, `-4`, `abc`, `1.005`, `1e3`, `nan` and `` all raise
   [src: ADR-0002]. `format_amount` returns `f"{minor // 100}.{minor % 100:02d}"`.
   `split_equally(minor, n)` returns `n` integers: `minor // n` each, with one extra unit added
   to the first `minor % n` of them [src: ADR-0003]; it raises for `n <= 0`. Afterwards the
   arithmetic of the whole tool is in one file and is testable without touching disk.

3. **Write `expenses/store.py`.** `store_path()` resolves `EXPENSES_STORE`, then
   `XDG_DATA_HOME/expenses/expenses.json`, then `~/.local/share/expenses/expenses.json`
   [src: ADR-0001]. `load()` returns the empty dataset for a missing file and raises
   `ExpensesError` for a file that is not JSON, is not an object, or whose `version` is not 1.
   `save()` writes to a temporary file in the same directory and `os.replace`s it over the
   target, creating parent directories first. `add_person(data, name)` strips the name, raises
   for an empty result [src: WI-0001 AC6] and for a name already present compared exactly
   [src: WI-0001 AC1], and appends it. `add_expense(...)` validates in this order — payer known,
   every sharer known (naming the first unknown one) [src: WI-0001 AC5], at least one sharer, no
   repeated sharer [src: WI-0001 AC6] — then computes the shares with `split_equally` and appends
   the record shaped as in ADR-0001. Afterwards the dataset's rules live in one file and no
   caller can write an invalid record through this interface.

4. **Write `expenses/cli.py` — the parser.** `build_parser()` creates an `argparse.ArgumentParser`
   with `prog="python3 -m expenses"` and required subparsers: `person add NAME`, `person list`,
   `expense add --amount --paid-by --shared-by [--description] [--date]`, `expense list`.
   `--shared-by` takes one comma-separated string and is split on commas by the handler, not by
   argparse. `--description` defaults to `""` and `--date` to `None`. Afterwards
   `python3 -m expenses` with no arguments, or with an unknown subcommand, exits non-zero with
   argparse's own usage message on stderr.

5. **Write `expenses/cli.py` — the handlers and the single failure path.** `main(argv)` parses,
   dispatches to a handler, and wraps the call in one `try/except ExpensesError` that writes
   `str(err)` to stderr and returns 2; on success it returns 0.
   - `person add` calls `store.add_person` then `store.save`, and prints `added <name>`.
   - `person list` prints one name per line in recorded order [src: WI-0001 AC3], or `no people`
     when there are none [src: WI-0001 AC9].
   - `expense add` parses the amount with `money.parse_amount`, resolves the date — `--date` must
     match `^\d{4}-\d{2}-\d{2}$` *and* be accepted by `datetime.date.fromisoformat`, so
     `2026-13-01` and `yesterday` both raise [src: WI-0001 AC6] — defaulting to
     `datetime.date.today().isoformat()` when omitted [src: WI-0001 AC7], then calls
     `store.add_expense` and `store.save`, and prints a one-line confirmation.
   - `expense list` prints one line per expense in recorded order, showing the date, the
     formatted amount, `paid by <payer>`, `shared by <sharers, comma-separated in recorded
     order>`, and the description [src: WI-0001 AC3]; or `no expenses` when there are none
     [src: WI-0001 AC9]. The description is printed last so that an empty one leaves the line
     otherwise unchanged.

   Afterwards every acceptance criterion has an executable path.

6. **Write the tests under `tests/`.** One module per source module plus one for the commands:
   `tests/test_money.py` (parsing, formatting, splitting, including 10.00 over three sharers),
   `tests/test_store.py` (path resolution via `EXPENSES_STORE`, missing file, round-trip, every
   refusal in `add_person` and `add_expense`, and that the file is unchanged after a refusal),
   and `tests/test_cli.py` (each command end to end, with `EXPENSES_STORE` pointed at a
   `tempfile.TemporaryDirectory`, asserting on exit code, stdout and stderr — including the two
   byte-identical-repeat-run criteria [src: WI-0001 AC4; WI-0001 AC8]). `tests/__init__.py`
   already exists (see `## Scaffolding`). Afterwards
   `python3 -m unittest discover -s tests -t .` exits 0 [src: ADR-0004].

7. **Write `README.md` at the repository root**, or add to it if it exists: the four commands with
   an example of each, and where the data file lives including the `EXPENSES_STORE` override.
   EP-001's success measures require a person to work the tool from documented commands without
   hand-editing anything [src: tracker/items/EP-001/item.md], and every acceptance criterion
   says "a documented command" — this step is what makes that word true.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — add a person, list them, duplicate refused, `Ana` and `ana` distinct | 3, 5 | `tests/test_cli.py`: `person add Ana` → exit 0; `person list` stdout contains `Ana`; second `person add Ana` → exit non-zero with `Ana` on stderr and `person list` still containing exactly one `Ana`; `person add ana` → exit 0 and `person list` containing both |
| AC2 — an expense records amount, payer, sharers and an equal 10.00 share each summing to 30.00 | 2, 3, 5 | `tests/test_store.py`: after `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara`, the JSON at `EXPENSES_STORE` has `amount_minor == 3000` and `shares_minor == {"Ana": 1000, "Ben": 1000, "Cara": 1000}`, and `sum(shares_minor.values()) == 3000` |
| AC3 — `expense list` shows amount, payer, sharers, date and description, in recorded order | 5 | `tests/test_cli.py`: two expenses recorded in a known order; stdout asserted line by line, each line containing all five fields, in the order they were added |
| AC4 — byte-identical stdout from a new process | 3, 5 | `tests/test_cli.py`: capture `person list` and `expense list` stdout, then run each again in a fresh `subprocess.run([sys.executable, "-m", "expenses", ...])` with the same `EXPENSES_STORE`, and assert the bytes are equal |
| AC5 — unknown sharer, and unknown payer, refused with the name on stderr and nothing changed | 3, 5 | `tests/test_cli.py`: capture `expense list` stdout, run `--shared-by Ana,Dan` → exit non-zero with `Dan` on stderr, re-run `expense list` and assert stdout is byte-identical; repeat with `--paid-by Dan` |
| AC6 — ten invalid inputs refused, nothing changed | 2, 3, 5 | `tests/test_cli.py`, parameterised over all ten (`--amount 0`, `-4`, `abc`, `1.005`, `--shared-by ""`, `Ana,Ana`, `--date 2026-13-01`, `--date yesterday`, `person add ""`, `person add "   "`): each exits non-zero, writes to stderr, and leaves both listings byte-identical |
| AC7 — description and date default independently and round-trip | 5 | `tests/test_cli.py`: four `expense add` calls — neither flag (date is `datetime.date.today().isoformat()`, description empty), `--description taxi` only, `--date 2026-08-01` only, `--description ""` — each exit 0, with `expense list` asserted for each |
| AC8 — 10.00 over three sharers sums exactly, and repeat runs agree | 2, 3 | `tests/test_money.py`: `split_equally(1000, 3) == [334, 333, 333]` and sums to 1000. `tests/test_cli.py`: the same command sequence run twice against two fresh `EXPENSES_STORE` directories produces byte-identical `expense list` stdout |
| AC9 — empty store prints `no people` and `no expenses`, exit 0 | 3, 5 | `tests/test_cli.py`: with `EXPENSES_STORE` pointing at a path in an empty temporary directory, `person list` → exit 0 with `no people` in stdout, `expense list` → exit 0 with `no expenses` in stdout |

Every criterion has a step and a specific demonstration; no step exists that no criterion maps
to, except step 7, which exists because the criteria say "documented" and EP-001's success
measures require it.

## Assumptions

- **The confirmation lines printed by `person add` and `expense add` are not fixed by any
  criterion**, so the developer may word them as they like. Reversing: change one f-string;
  nothing asserts on them. The two strings that *are* fixed — `no people` and `no expenses` — are
  refinement's, and AC9 asserts them [src: WI-0001 AC9].
- **The refusal exit code is 2.** Nothing requires a particular non-zero value
  [src: WI-0001 AC5], and 2 is what argparse already uses for a usage error, so every failure
  from this tool leaves the same code. Reversing: one `return` in `cli.py`.
- **`expense list` prints one line per expense** rather than a block. Reversing: one function in
  `cli.py`; AC3 constrains the fields and the order, not the layout.
- **The dataset is small enough to hold in memory and rewrite whole.** Recorded in ADR-0001;
  reversing it means a different store, which is why it is an ADR rather than only an assumption.

## Decisions and ADRs

| Decision | Where |
|----------|-------|
| One JSON file for people and expenses, located by `EXPENSES_STORE` then XDG, written atomically | [src: ADR-0001] |
| Money as integer minor units, parsed by an exact string match, never floats | [src: ADR-0002] |
| An indivisible remainder goes to the first-named sharers | [src: ADR-0003] |
| `unittest` as the test command; no lint command, and why | [src: ADR-0004] |
| The four-module layout and its one-way layering | `docs/architecture/overview.md` v1 |
| Confirmation wording, exit code 2, one-line listing entries | `## Assumptions` above |

The two things `refine` explicitly routed here are both now decided: the remainder rule
[src: ADR-0003] and where the store lives [src: ADR-0001] [src: tracker/items/WI-0001/item.md].

## Scaffolding

- `tests/__init__.py` — empty. `python3 -m unittest discover -s tests -t .` fails with
  `ImportError: Start directory is not importable` without it, so the command declared in
  `tracker/project.yaml` could not otherwise execute [src: ADR-0004]. It contains no behaviour.

Nothing else outside `tracker/` and `docs/` was created by this execution.

## Risks

- **`datetime.date.today()` makes AC7 depend on the clock.** A test that records an expense
  without `--date` and asserts on today's date will fail if it runs across midnight. The
  mitigation is in the plan: assert against `datetime.date.today().isoformat()` computed in the
  test rather than against a literal.
- **AC4 and AC8 compare bytes, so any incidental nondeterminism breaks them** — dictionary
  ordering in output, or a locale-dependent format. The design avoids both by printing from the
  recorded lists in recorded order [src: ADR-0003] and formatting amounts with an explicit
  f-string [src: ADR-0002], but it is the failure mode to check first if either criterion fails.
- **`EXPENSES_STORE` is how the tests stay hermetic.** A test that forgets to set it writes to the
  developer's real data file. Every test that touches the store must set it to a path inside a
  `tempfile.TemporaryDirectory`.
- **Storing the computed shares means the record can disagree with itself if the file is
  hand-edited.** Accepted and recorded in ADR-0003's consequences.

## Out of scope for this item

- Working out who owes whom, in any form — WI-0002.
- Reading a bank CSV export — WI-0003.
- Deleting or editing a person or an expense — WI-0004, and editing is not scheduled at all
  [src: WI-0001/Q-003].
- Any packaging, entry point or installation step. `python3 -m expenses` is the interface, and
  `commands.build` stays `null` [src: ADR-0004].
- Currency of any kind [src: ADR-0002].
