# Plan — WI-0001 Add a flashcard and have it survive a restart

## Problem

Someone at a terminal has a word and its meaning in front of them and wants it captured. This
item delivers one command — `python3 -m recall add <front> <back>` — that writes one card into a
plain-text file on their machine and tells them it did. Nothing shows a card, reviews it or
deletes it here; what this item owes the rest of the product is the file, its format, and the
guarantee that a card put into it is still there tomorrow.

The constraints are all already decided. The surface is a command line [src: ADR-0001]. The file
is readable text the tool owns and rewrites [src: ADR-0004], one card per block of labelled
lines [src: ADR-0007], at a documented path written through a temporary file and a rename
[src: ADR-0008]. A new card is written at the bottom rung with today's date as its due date
[src: ADR-0002] [src: ADR-0007]. The tool is Python 3 with the standard library only
[src: ADR-0006]. What is left to build is the parser, the writer, the argument handling, and the
three input cases the criteria name: a duplicate front [src: WI-0001 AC6], an empty side
[src: WI-0001 AC7], and a card file that does not exist yet [src: WI-0001 AC8].

## Approach

Two modules with one seam, as `docs/architecture/overview.md` describes them.

**`recall/store.py` owns the file.** It knows where the card file is, what a card is, how a card
is written down, and how the file is saved. Its interface:

- `CARD_FILE_ENV = "RECALL_CARD_FILE"` and `HEADER`, the two `#` lines the tool writes at the top
  of the file.
- `class Card(NamedTuple)` with `front: str`, `back: str`, `rung: int`, `due: datetime.date`.
- `card_file_path() -> str` — `RECALL_CARD_FILE` if set and non-empty, else
  `$XDG_DATA_HOME/recall/cards.txt` if `XDG_DATA_HOME` is set and non-empty, else
  `~/.local/share/recall/cards.txt` [src: ADR-0008].
- `load(path: str) -> list[Card]` — the cards in file order; an empty list when the file does not
  exist. Raises `CardFileError` naming the line number when the file is not in the format
  `ADR-0007` describes [src: ADR-0007].
- `save(path: str, cards: list[Card]) -> None` — creates the containing directory if needed,
  writes the header and one block per card to a temporary file in the same directory, flushes it
  to disk, renames it over `path`, and flushes the directory [src: ADR-0008].
- `class CardFileError(Exception)`.

**`recall/cli.py` owns the conversation with the person.** It parses arguments, applies the input
rules, calls the store, prints, and returns an exit code. Its interface:

- `main(argv: list[str] | None = None) -> int` — builds the parser, dispatches the subcommand,
  and returns the process's exit code. Catches `CardFileError` and `OSError` from the store,
  prints the message to standard error, and returns `1` rather than letting a traceback reach the
  person.
- `add(front: str, back: str) -> int` — the `add` subcommand, in the order the criteria fix:
  validate, then duplicate-warn, then append and save [src: WI-0001 AC7].
- `_side_error(label: str, value: str) -> str | None` — the message when a side is empty,
  whitespace-only, or contains a line break; `None` when it is acceptable
  [src: WI-0001 AC7] [src: ADR-0007].

`recall/__main__.py` is three lines that call `main()` and exit with what it returns, so that
`python3 -m recall` is the entry point every test and every criterion uses.

Exit codes: `0` when the card was added, including when a duplicate warning was printed
[src: WI-0001 AC6]; `1` when the tool refused the input or could not read or write the file; `2`
from `argparse` when the command line itself is wrong, which is the case WI-0001 leaves
deliberately unconstrained [src: WI-0001]. Confirmations go to standard output; warnings and
refusals go to standard error.

## Steps

1. **Create `recall/store.py` with the path resolution and the card record.** Add
   `CARD_FILE_ENV`, `HEADER`, `CardFileError`, `Card`, and `card_file_path()` as specified under
   Approach. Afterwards, `python3 -c "import recall.store as s; print(s.card_file_path())"`
   prints `~/.local/share/recall/cards.txt` expanded, and prints the override when
   `RECALL_CARD_FILE` is set in the environment.

2. **Add the reader to `recall/store.py`.** `load(path)` returns `[]` when `path` does not exist;
   otherwise it skips `#` lines and blank lines between blocks, reads each block's four labelled
   lines in the fixed order, takes each value as everything after the first `: ` to the end of
   the line without trimming, parses `rung` as an integer and `due` with
   `datetime.date.fromisoformat`, and raises `CardFileError` naming the line number when a block
   is short, mislabelled, out of order, or carries an unparsable `rung` or `due`
   [src: ADR-0007]. Afterwards, a file written by hand in the documented shape loads into the
   cards it shows, and a file with a mangled line raises with that line's number.

3. **Add the writer to `recall/store.py`.** `save(path, cards)` creates the containing directory,
   writes `HEADER` then one block per card separated by a blank line, to a temporary file in the
   same directory; flushes and `os.fsync`s it; `os.replace`s it over `path`; then opens the
   containing directory and `os.fsync`s that too [src: ADR-0008]. Afterwards,
   `save` followed by `load` returns the cards that were saved, byte for byte on both sides, and
   no temporary file is left behind.

4. **Create `recall/cli.py` and `recall/__main__.py` with the parser.** `main()` builds an
   `argparse` parser whose program name is `recall`, with an `add` subcommand taking exactly two
   positional arguments, `front` then `back` [src: WI-0001 AC1]. Afterwards,
   `python3 -m recall add one two` reaches `add()`, `python3 -m recall add one` exits `2` with a
   usage message on standard error, and `python3 -m recall` with no subcommand exits `2`.

5. **Implement `add()` in `recall/cli.py`, in the fixed order.** First `_side_error` on the front
   and then on the back: on the first message, print it to standard error and return `1` without
   reading or writing the card file [src: WI-0001 AC7]. Then `load(card_file_path())`. Then, if
   any existing card's `front` is equal to the new front, print the duplicate warning to standard
   error and carry on [src: WI-0001 AC6]. Then append `Card(front, back, 0, date.today())`
   [src: ADR-0007] [src: WI-0001 AC4], `save` the list, print a confirmation naming the front
   side to standard output, and return `0` [src: WI-0001 AC1]. Afterwards, each of the criteria's
   commands behaves as its criterion says.

6. **Write `tests/test_add.py`.** Every test sets `RECALL_CARD_FILE` to a path inside a fresh
   `tempfile.TemporaryDirectory`, so no test touches a real deck [src: ADR-0008]. The cases, one
   per criterion, are listed in the mapping table below; each drives `python3 -m recall` as a
   subprocess with `subprocess.run` and asserts on the exit code, on standard output and standard
   error, and on the bytes of the card file read afterwards — never on the store's internals,
   because what the criteria describe is what a person sees at a terminal
   [src: WI-0001 AC1].

7. **Run the project's gates and write the implementation report.**
   `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q recall tests`
   both exit zero [src: ADR-0006], and `tracker/items/WI-0001/artifacts/impl-report.md` records
   which test demonstrates which criterion. The criteria's checkboxes are `verify`'s to tick, not
   this item's implementation's.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `add` with two arguments adds a card, confirms naming the front, exits 0 | 4, 5 | `test_add_prints_confirmation_and_exits_zero`: `python3 -m recall add bonjour hello` → exit 0, standard output contains `bonjour`, and the card file afterwards holds one block |
| AC2 — the card is in the file after the process has exited, both sides byte-identical | 2, 3, 5 | `test_card_is_on_disk_after_the_process_exits`: the subprocess exits, then the test reads the file's bytes and finds `front: bonjour` and `back: hello` exactly; durability past a reboot rests on the flush-and-rename discipline of `save` [src: ADR-0008], which no test can restart a machine to show |
| AC3 — three cards with different fronts are three separate records | 2, 3, 5 | `test_three_cards_are_three_records`: three `add` runs, then the file holds three blocks, each with its own four lines, and `load` returns three cards with the three fronts and the three backs |
| AC4 — a new card's due date is the calendar date it was added | 5 | `test_new_card_is_due_today`: after `add`, the file's `due:` line equals `datetime.date.today().isoformat()` computed in the test |
| AC5 — the card data is at the documented path and is readable text | 1, 3 | `test_default_path_is_the_documented_one`: with `RECALL_CARD_FILE` unset and `HOME` and `XDG_DATA_HOME` pointed at a temporary directory, `add` writes `<XDG_DATA_HOME>/recall/cards.txt`; and `test_file_is_readable_text`: the file decodes as UTF-8 and every line of every block is one of the four labels followed by its value, matching `docs/architecture/overview.md`'s statement of the path and the format |
| AC6 — a duplicate front adds a second card, warns, exits 0 | 5 | `test_duplicate_front_adds_and_warns`: two `add` runs with the same front and different backs → both exit 0, the second prints a warning on standard error, and the file afterwards holds two blocks with the same front and the two different backs |
| AC7 — an empty or whitespace-only side adds nothing, names the side, exits non-zero, leaves the file untouched | 5 | `test_empty_side_is_refused`, parametrised over an empty front, an empty back and a whitespace-only side → exit non-zero, standard error names which side, and the card file's bytes are unchanged (and, in the case where it did not exist, still does not exist); and `test_empty_back_with_duplicate_front_prints_no_duplicate_warning`, which is AC7's precedence over AC6 |
| AC8 — `add` when the card file does not exist creates it and writes the card | 3, 5 | `test_first_add_creates_the_file`: `RECALL_CARD_FILE` points into a directory that does not exist, `add` exits 0, the file exists afterwards, and AC1's and AC2's assertions hold on it |

## Assumptions

Each of these is settled under the stakeholder's standing delegation — *"As for how it's actually
built — whatever you think is best"* [src: EP-001/Q-004] — and each is reversible in the sense
`plan`'s procedure requires: one file, no data migration, no promise to anyone outside the tool.

1. **A refused card exits `1`; a malformed command line exits `2`.** `2` is `argparse`'s own
   usage exit and is not worth fighting. The criteria ask only for non-zero
   [src: WI-0001 AC7]. Reversing this is one constant in `recall/cli.py`.
2. **The wording of the confirmation, the duplicate warning and the refusal messages is
   `implement`'s**, within what the criteria require them to name: the front side
   [src: WI-0001 AC1], that a card with that front already exists [src: WI-0001 AC6], and which
   side was empty [src: WI-0001 AC7]. Reversing any of them is a string.
3. **Confirmations go to standard output and everything else to standard error**, so that a
   person piping the output gets the confirmation and not the warning. No criterion names a
   stream. Reversing it is two calls.
4. **A card file that does not parse stops the command** with the message and the line number,
   rather than being repaired or partly loaded. The tool owns the file [src: ADR-0004], so a file
   it cannot read has been changed by something else, and quietly dropping the cards it cannot
   read would destroy exactly what the person was promised [src: EP-001/Q-004]. No criterion
   covers this case; it is named here because `load` cannot avoid deciding it. Reversing it is
   the `except` clause in `main()`.
5. **`Card.due` is a `datetime.date` in memory** and `YYYY-MM-DD` on disk [src: ADR-0007], so the
   comparison WI-0002 will make is a date comparison and not a string one. Reversing it is the
   record definition and its two uses.

## Decisions and ADRs

| decision | where it is recorded | how it was reached |
|----------|---------------------|--------------------|
| Python 3, standard library only; the package at the repository root | `ADR-0006` | decided here, on the standing delegation [src: EP-001/Q-004] |
| `commands.test` and `commands.lint`, and what the lint command does not check | `ADR-0006`, `tracker/project.yaml` | decided here; both commands were run before being recorded |
| The card file format: one card per block of labelled lines, values verbatim to end of line | `ADR-0007` | decided here, against AC2's byte-identical reading [src: WI-0001 AC2] and `ADR-0004`'s commitment |
| `rung: 0` for a card that has never been answered; `1`-`4` are the ladder's intervals | `ADR-0007` | derived from `ADR-0002`'s ladder; it defines a field, it does not change the rule |
| A side containing a line break is refused, like an empty side | `ADR-0007` | decided here; the format has no way to hold one, and every criterion describes one-line sides [src: WI-0001 AC1] |
| The card file's location, the `RECALL_CARD_FILE` override, and creating the directory on first use | `ADR-0008` | decided here, to satisfy AC5's documented path [src: WI-0001 AC5] and AC8 [src: WI-0001 AC8] |
| Every save goes through a temporary file, a flush and a rename | `ADR-0008` | decided here, to satisfy AC2 [src: WI-0001 AC2] and AC7's untouched file [src: WI-0001 AC7] |
| Exit codes, message wording, streams, unparsable-file behaviour, in-memory date type | this plan, `## Assumptions` | reversible assumptions under the standing delegation [src: EP-001/Q-004] |

Nothing on this item was put to the stakeholder. Every decision above is either answered by a
document — `ADR-0001`, `ADR-0002` and `ADR-0004` between them settle the surface, the schedule and
the file's readability — or falls inside the delegation they stated in their own words
[src: EP-001/Q-004]. No decision here is irreversible in the way `ADR-0004`'s was: the one
expensive commitment on this item, the shape of the file the person's history accumulates in, was
escalated by an earlier execution and answered by them [src: WI-0001/Q-002].

## Scaffolding

Two files, both empty, both created by this `plan` execution because the commands it is required
to have run cannot execute without them:

- `recall/__init__.py` — `python3 -m compileall -q recall tests` needs the directory to exist and
  be a package [src: recall/__init__.py].
- `tests/__init__.py` — `python3 -m unittest discover -s tests -t . -q` discovers from the
  repository root, and the package marker is what makes a test module import as `tests.test_add`
  with the root on `sys.path`, so that it can `import recall` [src: tests/__init__.py].

Neither holds any behaviour, and no acceptance criterion depends on either.

## Risks

- **AC2 names a machine restart, and no test can perform one.** The evidence available is that
  the file is on disk with the right bytes after the writing process has exited, plus `save`'s
  flush-and-rename discipline [src: ADR-0008]. If `verify` reads AC2 as requiring an actual
  reboot, this item cannot pass in any automated environment and the criterion needs the
  stakeholder rather than a defect report. It is named here so that judgement is made
  deliberately rather than at the end of a verification run.
- **The lint gate is weak by decision** [src: ADR-0006]. A defect it would have caught — an
  undefined name on a path no test walks — will reach `verify` instead. The mitigation is that
  every criterion above is covered by a test that runs the real command.
- **The duplicate check is a linear scan of every card's front.** At one person's deck that is
  nothing; it is named because it is the one place in this item whose cost grows with the file,
  and because WI-0003 will need the same scan [src: WI-0003].
- **`RECALL_CARD_FILE` pointing somewhere unwritable** surfaces as an `OSError` caught in
  `main()`, a message and exit `1`. No criterion covers it and none is being invented for it.

## Out of scope for this item

- Showing, reviewing or rescheduling cards, and any movement along the ladder — that is WI-0002
  [src: WI-0002].
- Deleting a card — that is WI-0003 [src: WI-0003].
- Listing or searching cards, editing a card, and any grouping into decks or tags
  [src: WI-0001].
- Accepting a hand-edited card file. The stakeholder declined it [src: WI-0001/Q-002] and
  `ADR-0004` records that no item is filed for it [src: ADR-0004]. Assumption 4 above says what
  the tool does when it meets one anyway, which is to stop and say so.
- Any third-party dependency, runtime or development [src: ADR-0006].
