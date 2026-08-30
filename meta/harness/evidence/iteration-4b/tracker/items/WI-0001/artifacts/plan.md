# Plan — WI-0001 Add a card to the deck and have it survive a restart

## Problem

A person learning vocabulary at a terminal needs a deck they can add to and come back to. This
item builds the first two subcommands of `recall` — `add` and `list` — and the storage
underneath them, and nothing else: nothing here reads a due date or runs a review sitting. The
constraints come from three places. The interface is fixed by `ADR-0001` (one executable,
subcommands, `add` taking its two sides as options). The storage medium is fixed by the
stakeholder — *"just a file on my machine that survives a reboot"* — and its format, path and
write discipline by `ADR-0004`. And one sentence of theirs shapes more of this design than any
criterion does: *"don't lose my progress — that's the one thing that would make this a failure."*
That is why the deck is written through `os.replace` and why a deck that cannot be parsed is
reported and left alone rather than replaced.

## Approach

Three modules with one rule each about what they may not do, as `docs/architecture/overview.md`
describes: `store.py` does file access and never prints; `deck.py` holds cards as values and
never touches the filesystem; `cli.py` owns argument shapes, messages and exit codes. `bin/recall`
is a launcher with no logic in it.

The interfaces this item introduces — signatures and contracts, not implementations:

- `recall/store.py`
  - `deck_path() -> pathlib.Path` — `Path.home()/".local"/"share"/"recall"/"deck.json"`. Derived
    from the home directory and nothing else.
  - `load(path) -> Deck` — returns an empty `Deck` when the file or its parent is absent; raises
    `DeckUnreadable(path, detail)` when the file exists but is not valid JSON, or is JSON that is
    not an object with a `cards` array whose entries have the four expected keys. Never writes.
  - `save(deck, path) -> None` — creates the parent directory if needed, serialises, writes to a
    temporary file in the same directory, and `os.replace`s it over `path`. Never partially
    overwrites an existing deck.
  - `DeckUnreadable(Exception)` — carries the path and a short reason, both of which `cli.py`
    puts on stderr.
- `recall/deck.py`
  - `Card` — a value with `question: str`, `answer: str`, `rung: int`, `due: datetime.date`.
  - `Deck` — an ordered sequence of `Card`, with `add(card)` appending and `cards` exposing the
    order. No file access, no printing.
  - `new_card(question, answer, today) -> Card` — `rung=0`, `due=today`, per `ADR-0002` §3.
- `recall/cli.py`
  - `main(argv) -> int` — parses, dispatches, returns the process exit code. Never calls
    `sys.exit` itself, so it is callable from a test without a subprocess.
  - `cmd_add(args) -> int`, `cmd_list(args) -> int`.

Two decisions inside that are worth stating rather than leaving to taste, because getting them
wrong is how AC2 and AC8 get quietly weakened:

- **Blank validation happens before anything is read or written.** `add` rejects a missing or
  blank side without opening the deck file at all, so a refusal cannot touch storage. That is
  what makes AC2's "byte-identical before and after" true by construction rather than by luck.
- **`DeckUnreadable` is caught in exactly one place**, at the top of each `cmd_*`, and turned
  into a message and a non-zero exit. It is never caught inside `store.py` and never converted
  into an empty deck.

## Steps

1. **Write the test helper and the first test.** Add `tests/support.py` with `run_recall(*args,
   home)` — invokes `bin/recall` as a subprocess with `bin/` prepended to `PATH` and `HOME` set
   to a `tempfile.TemporaryDirectory`, returning exit code, stdout and stderr — and
   `tests/test_add.py` with one test for AC1. This is step 1 because `commands.test` exits 5
   until a file matching `test*.py` exists (`ADR-0003` §2), so nothing else can be checked before
   it. Afterwards: `python3 -m unittest discover -s tests -t . -q` exits non-zero for the honest
   reason that the tool does not exist yet.
2. **Add `recall/deck.py`** with `Card`, `Deck` and `new_card` as above. Afterwards: the module
   imports and a card can be constructed with a rung and a due date.
3. **Add `recall/store.py`** with `deck_path`, `load`, `save` and `DeckUnreadable`. `save` writes
   through a temporary file in the destination directory and `os.replace`. Afterwards: a deck can
   be saved and loaded back with the same cards, an absent file loads as an empty deck, and a
   file containing `{` raises `DeckUnreadable`.
4. **Add `recall/cli.py`** with `main`, `cmd_add` and `cmd_list`, using `argparse` with `add` and
   `list` subparsers; `add` takes `--question` and `--answer`. Blank validation happens before
   the deck is loaded. Afterwards: `main(["add", "--question", "q", "--answer", "a"])` returns 0
   and `main(["add", "--question", ""])` returns non-zero with a message naming the missing side.
5. **Add `bin/recall`** (executable, `#!/usr/bin/env python3`) and `recall/__main__.py`, both
   calling `recall.cli.main` and passing its return value to `sys.exit`. Afterwards: with `bin/`
   on `PATH`, `recall list` runs and exits 0.
6. **Write the remaining tests**, one per criterion, in `tests/test_add.py`, `tests/test_list.py`
   and `tests/test_storage.py` — the mapping table below says which. Afterwards:
   `python3 -m unittest discover -s tests -t . -q` exits 0.
7. **Write `docs/process/using-recall.md`** — the project's own documentation for a person with a
   terminal and no context: the one setup step (`export PATH="$PWD/bin:$PATH"`), how to add a
   card, how to list the deck, and **where the deck file is kept**. AC7(a) is satisfied by this
   file and by nothing else, so it is a step rather than a courtesy.
8. **Run both gates** — `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall
   -q recall tests` — and record their exit codes in the implementation report.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — add exits 0 and the deck gains a card | 2, 3, 4, 5 | `tests/test_add.py::test_add_exits_zero_and_adds_one` — `run_recall("list")`, then `run_recall("add", "--question", "capital of France", "--answer", "Paris")` asserting exit 0, then `run_recall("list")` again asserting one more card line |
| AC2 — five refusal cases, deck byte-identical | 4, 6 | `tests/test_add.py::test_blank_sides_refused` — parametrised by hand over the five cases (`--question` omitted, `--answer` omitted, `--question ""`, `--answer ""`, `--answer "   "`); each asserts non-zero exit, the missing side's name in stderr, and `sha256` of the deck file identical before and after |
| AC3 — list shows both cards, text unaltered | 4, 6 | `tests/test_list.py::test_lists_both_cards_verbatim` — adds two cards, one with a leading capital and an internal double space, and asserts both questions and both answers appear in stdout exactly as given |
| AC4 — persistence across processes | 3, 6 | `tests/test_storage.py::test_survives_process_exit` — one `run_recall("add", ...)` subprocess, then a separate `run_recall("list")` subprocess with the same `HOME`, asserting the card is in the second's stdout |
| AC5 — first run creates file and parent | 3, 6 | `tests/test_storage.py::test_first_run_creates_storage` — `HOME` is an empty temporary directory; asserts `~/.local/share/recall/deck.json` does not exist, runs `add`, asserts exit 0 and that the file now exists |
| AC6 — empty deck says so, exit 0 | 4, 6 | `tests/test_list.py::test_empty_deck_message` — `run_recall("list")` against an empty `HOME`, asserting exit 0 and a non-empty stdout line saying the deck is empty |
| AC7 — one durable documented file | 3, 6, 7 | `tests/test_storage.py::test_one_file_under_home_not_tmp` — snapshots the `HOME` tree before and after an `add` and asserts exactly one new file, whose path is under `HOME` and matches none of `/tmp`, `/var/tmp`, `$TMPDIR`; plus `tests/test_storage.py::test_docs_state_the_path`, asserting `docs/process/using-recall.md` contains the literal `.local/share/recall/deck.json` |
| AC8 — unreadable deck refused, bytes unchanged | 3, 4, 6 | `tests/test_storage.py::test_unreadable_deck_refused` — writes `{"cards": ` into the deck file, records its `sha256`, runs `add` and `list`, asserts both exit non-zero, both name the path on stderr, and the `sha256` is unchanged |
| AC9 — duplicate questions allowed | 4, 6 | `tests/test_add.py::test_duplicate_question_allowed` — adds the same question twice with different answers, asserts both `add`s exit 0 and `list` shows two cards |

Every step above maps to at least one AC. Step 7 exists only for AC7(a); step 1 exists because
`ADR-0003` §2 measured the test command exiting 5 with no test file.

## Assumptions

- **`sha256` of the deck file is a fair reading of "byte-identical".** It is not literally a byte
  comparison, but a hash collision is not a failure mode anyone will hit. Reversing this is
  replacing one line in the helper with `Path.read_bytes()`.
- **The empty-deck message and the refusal messages have no fixed wording.** Criteria require a
  message that names the missing side (AC2) or the path (AC8); tests assert those substrings, not
  a sentence. Reversal cost: none — nobody is depending on exact text.
- **`list` prints one line per card.** The mapping table's "one more card line" for AC1 depends on
  it. AC3 requires only that both sides appear; one-line-per-card is this plan's choice because it
  makes AC1 countable. Reversal cost: one function in `cli.py` and the two assertions that count
  lines.
- **`today` is the local calendar date.** `ADR-0002` talks in days and the stakeholder reviews
  once a day at a terminal; nothing in this item reads the date back, so no criterion depends on
  it. WI-0002 and WI-0003 will, and if a timezone question arises it is theirs, not this item's.

## Decisions and ADRs

- `ADR-0003` — Python 3, standard library only; `unittest` for tests and `compileall` for lint,
  both measured on this machine. Route: decided here; the record was silent and the alternatives
  needed naming.
- `ADR-0004` — the deck is one JSON file at `~/.local/share/recall/deck.json`, written atomically,
  and never repaired when unreadable. Route: decided here under the stakeholder's standing
  deferral over storage (`EP-001/Q-001`), which refinement had already routed to `plan`.
- `ADR-0005` — `bin/recall` on `PATH`, no install step. Route: decided here; `ADR-0001` had
  explicitly left it open and every criterion depends on it.
- `ADR-0001` and `ADR-0002` are read, not revisited. `ADR-0002` reaches this item only as the
  fields `add` has to write (`rung`, `due`).
- `tracker/project.yaml` — `commands.test` and `commands.lint` filled in, with the ADR's
  measurements behind them; `commands.build` left null because there is no build step.
- `docs/architecture/overview.md` — created at version 1, as the first planned item requires.

Nothing here needed the stakeholder. No decision in this plan is irreversible, and none of them
depends on intent no document records — the two conditions that would have made a question the
right move.

## Scaffolding

- `recall/__init__.py` — empty package marker. Without it `python3 -m compileall -q recall tests`
  has no `recall` directory to compile and the declared lint command cannot run.
- `tests/__init__.py` — empty package marker, same reason.

Both are empty files and contain no behaviour. No other file outside `tracker/` and `docs/` was
created by this execution.

## Risks

- **The easy way to satisfy AC5 breaks AC8.** "Create storage when it is absent" and "refuse when
  it is unreadable" collapse into one branch if `load` treats a parse failure as an empty deck,
  and the result passes AC5, AC1 and AC4 while silently destroying a person's deck. This is the
  single most likely defect in this item; `store.load` raising rather than returning is the
  design decision that prevents it, and AC8's test is the one that catches it.
- **`HOME` redirection leaks if a test calls `main()` directly.** `Path.home()` is read at call
  time, so an in-process test that patches `os.environ["HOME"]` would work by accident and break
  when something caches it. Every acceptance test runs the CLI as a subprocess for this reason
  (`ADR-0005` §4); a unit test that calls `main()` must pass a path explicitly or not touch the
  deck at all.
- **AC7's `$TMPDIR` check is only as good as the environment it runs in.** If a machine sets
  `TMPDIR` inside `$HOME`, the assertion "not under `$TMPDIR`" could fail for a correct
  implementation. The test compares against the *resolved* paths and asserts the deck is under
  `HOME`; if that ever conflicts, it is a defect in the test, not in the tool.
- **Cards have no stable identifier.** WI-0004 must name a card to delete one and may want an id
  rather than a position. That would be a schema change; `version` in the deck file is what makes
  it a migration rather than a break (`ADR-0004`). Recorded, not solved — it is WI-0004's
  decision and its refinement has not happened.
- **`commands.lint` catches only syntax errors.** A green lint gate on this project means less
  than it does on most. `ADR-0003` says so in its consequences so that nobody reads it as more.

## Out of scope for this item

- Anything about when a card is next seen. `add` writes `rung` and `due`; nothing in this item
  reads them. Review sittings are WI-0002, the interval arithmetic is WI-0003.
- Deleting a card (`WI-0004`) and editing one (excluded from the epic entirely).
- Making the deck's location configurable — no flag, no environment variable of the tool's own,
  no config file. Excluded by the item and by `ADR-0004`.
- A `review` subcommand. `ADR-0001` names it; this item does not build it.
- Packaging, publishing or installing (`ADR-0005`).
