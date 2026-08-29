# Plan — WI-0001 Add a card and have it persist across runs

## Problem

Someone at a terminal needs to write down a thing they are trying to memorise — a question side
and an answer side — and find it still there the next time they run the tool. This item delivers
exactly two commands, `recall add` and `recall list`, and the file the cards live in. It changes
nothing about when a card is next due; that state belongs to WI-0002 and WI-0003, and this item
must leave room for it without deciding any of it [src: WI-0003]. The constraints are already
fixed: a command-line tool [src: EP-001/Q-001], one flat pool with no decks [src: EP-001/Q-004],
both card sides given as arguments to one command [src: WI-0001/Q-001], and one JSON file at
`~/.recall.json` unless `RECALL_FILE` overrides it [src: ADR-0002]. Nothing here is
interactive, and every criterion is decided by running a command and reading its output and exit
code [src: WI-0001 AC1].

## Approach

Two files at the repository root and one directory of tests, per ADR-0005:

- **`recall`** — the executable. `#!/usr/bin/env python3`, no behaviour: put its own directory on
  the import path, call `main(sys.argv[1:])`, exit with what it returns [src: ADR-0005].
- **`recall.py`** — the module, in two layers that do not call back into each other:
  - a *store* layer that knows the file: where it is, how to read it, how to write it;
  - a *command* layer that knows the command line: what the user typed, what to print, which
    exit code to return.

  `main(argv)` returns an exit code and never calls `sys.exit`, so tests can call it in-process
  as well as by subprocess [src: ADR-0005].
- **`tests/`** — `unittest` cases run by `python3 -m unittest discover -s tests -t .`
  [src: ADR-0003]. Cases about output and exit codes drive the executable as a subprocess with
  `RECALL_FILE` pointing into a temporary directory, which is the surface the criteria are
  written against [src: WI-0001 AC5].

The interfaces this plan fixes — the developer implements them, and does not renegotiate them:

| function | contract |
|----------|----------|
| `store_path()` | Returns the store's path: `RECALL_FILE` when set and non-empty, else `~/.recall.json` [src: ADR-0002]. |
| `load(path)` | Returns the document. A file that is absent yields the empty document `{"version": 1, "cards": []}`. A file that exists but does not parse, or does not have that shape, raises — it is never treated as empty [src: ADR-0004]. |
| `save(path, document)` | Writes `document` to a temporary file in `path`'s own directory, flushes it, and renames it over `path`. UTF-8, two-space indent, non-ASCII unescaped, trailing newline [src: ADR-0004]. |
| `add_card(document, question, answer)` | Appends a card numbered one above the largest `number` present, 1 when there are none, and returns its number. Does not touch the disk [src: ADR-0004]. |
| `main(argv)` | `argv` excludes the program name. Returns 0, 1 or 2 [src: ADR-0005]. |

The command-line rule, in full: `argv[0]` is the command name; everything after it is positional
and is never read as an option. `add` requires exactly two positional arguments. That single rule
is what rejects `--deck german` (it makes the count four) and what rejects every wrong count
[src: WI-0001 AC6; WI-0001 AC9].

The output contract — the exact strings are the developer's to place, the shape is not:

| situation | stream | text | exit |
|-----------|--------|------|------|
| card added | stdout | `Added card <n>.` | 0 |
| listing, cards present | stdout | one line per card, `<number>\t<question>\t<answer>`, ascending by number | 0 |
| listing, no cards | stdout | `No cards yet.` — one line, nothing else | 0 |
| empty question side | stderr | `recall add: the question side is empty` | 2 |
| empty answer side | stderr | `recall add: the answer side is empty` | 2 |
| wrong argument count for `add` | stderr | `usage: recall add <question side> <answer side>` | 2 |
| unknown command, or none | stderr | `usage: recall <add|list>` | 2 |
| store cannot be written | stderr | `recall: cannot write <path>: <reason>` | 1 |
| store cannot be read | stderr | `recall: <path> is not a readable card store: <reason>` | 1 |

Both empty-side messages name which side is empty, which is what AC4 asks for
[src: WI-0001 AC4]. When both sides are empty, the question side is reported — the first one
wrong, checked in argument order.

## Steps

1. **Write the store layer in `recall.py`.** `store_path()`, `load(path)`, `save(path,
   document)` and `add_card(document, question, answer)` as contracted above. Afterwards:
   importing `recall` and calling `save` on a path in a temporary directory produces a file whose
   text is the schema in ADR-0004, and `load` on that file returns what was saved.

2. **Write the command layer in `recall.py`.** `main(argv)` dispatching on `argv[0]` to an add
   command and a list command, applying the positional-only rule, printing per the output
   contract, and turning a store failure into exit 1 with its message on stderr. Afterwards:
   `python3 -c "import recall, sys; sys.exit(recall.main(['list']))"` prints `No cards yet.` and
   exits 0 against an empty temporary store.

3. **Write the executable `recall` at the repository root and mark it executable.** Three or four
   lines: the shebang, its own directory onto `sys.path`, `main(sys.argv[1:])`, `sys.exit`.
   Afterwards: with the repository root on `PATH`, `recall list` behaves as step 2's call did.

4. **Write `README.md` at the repository root.** What the tool is; how to run it — `./recall` or
   the repository root on `PATH`; the two commands with an example of each; and the store's
   location, naming both `~/.recall.json` and the `RECALL_FILE` override, since AC5 requires the
   documentation to name them [src: WI-0001 AC5].

5. **Write `tests/test_add.py`.** Subprocess cases against the executable with `RECALL_FILE` in a
   temporary directory, one per behaviour: a card added prints a number and exits 0; numbers
   start at 1 and increment; identical text twice gives two numbers; each empty side is rejected
   by name with nothing stored; a `--deck` argument is rejected; `add` with zero, one and three
   positional arguments is rejected with the usage line on stderr and nothing stored; non-ASCII
   text survives a round trip.

6. **Write `tests/test_list.py`.** A card added in one process is listed byte-identical by
   another; the listing is in ascending card-number order after adding out of nothing; an empty
   store prints one line and exits 0; a store file that does not exist at all behaves the same.

7. **Write `tests/test_store.py`.** `RECALL_FILE` decides the path when set; with `RECALL_FILE`
   unset and `HOME` pointed at a temporary directory, the card lands in `<HOME>/.recall.json`;
   the stored file contains non-ASCII characters unescaped; a store file containing text that is
   not JSON makes `add` exit 1 and leaves the file's bytes unchanged.

8. **Write `tests/test_docs.py`.** `README.md` contains `~/.recall.json` and `RECALL_FILE`
   [src: WI-0001 AC5].

9. **Run both gate commands from the repository root** — `python3 -m unittest discover -s tests
   -t .` and `python3 -m compileall -q -x '[.]claude' .` — and report their output in the
   implementation report [src: ADR-0003].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `recall add "<q>" "<a>"` exits 0, prints a line containing the card's number; numbers start at 1 and increment | 1, 2, 3 | `tests/test_add.py`: adding a card exits 0 and stdout contains `1`; adding a second prints `2` |
| AC2 — a fresh `recall list` prints the card byte-identical against the number AC1 reported | 1, 2, 3 | `tests/test_list.py`: `add` in one subprocess, `list` in another, the listed sides compared byte-for-byte with the arguments |
| AC3 — two identical cards get different numbers, both listed | 1, 2 | `tests/test_add.py`: the same two arguments added twice; the two printed numbers differ and `list` shows two lines |
| AC4 — an empty side exits non-zero naming that side; nothing stored | 2 | `tests/test_add.py`: `recall add "" "the cat"` exits 2 with `question` in stderr; `recall add "die Katze" ""` exits 2 with `answer` in stderr; `list` after each prints `No cards yet.` |
| AC5 — cards in one readable file: `~/.recall.json` by default, `RECALL_FILE` when set; both named in `README.md` | 1, 4 | `tests/test_store.py`: `RECALL_FILE=<tmp>/cards.json recall add "a" "b"` puts the card in `<tmp>/cards.json` and the file's text parses as JSON and reads as text; with `HOME=<tmp>` and no `RECALL_FILE`, the card lands in `<tmp>/.recall.json`. `tests/test_docs.py`: `README.md` names both |
| AC6 — flat pool: exactly two positional arguments, a `--deck` option rejected; `list` shows every card in ascending number order | 2, 3 | `tests/test_add.py`: `recall add --deck german "die Katze" "the cat"` exits 2 and stores nothing. `tests/test_list.py`: three cards added, `list` prints them in ascending number order |
| AC7 — non-ASCII text stored and listed byte-identical | 1, 2 | `tests/test_add.py`: `recall add "Grüße" "greetings"`, the listed text compared with the input. `tests/test_store.py`: the store file contains `Grüße` unescaped |
| AC8 — `recall list` with no cards prints one plain line, nothing else, exits 0 | 2 | `tests/test_list.py`: against a store path with no file, stdout is exactly one line and exit is 0; and the same against a store holding zero cards |
| AC9 — `add` with any count other than two exits non-zero, usage line on stderr naming both arguments, nothing stored | 2 | `tests/test_add.py`: `add`, `add "die Katze"`, `add "die Katze" "the cat" "extra"` each exit 2, stderr matches the usage line and mentions both sides, and `list` afterwards prints `No cards yet.` |

## Assumptions

1. **Only the empty string is an empty side.** A side of `" "` is content and is stored as typed.
   Reversing: one condition in the add command plus AC4's wording. Cheap — one file, no stored
   data changes. Chosen because AC4 says "empty" and rejecting whitespace is behaviour nobody
   asked for [src: WI-0001 AC4].
2. **The confirmation line is `Added card <n>.`**, the empty listing is `No cards yet.`, and the
   usage line is `usage: recall add <question side> <answer side>`. `refine` left this wording
   deliberately unconstrained, requiring only that each line exists and names the right thing
   [src: WI-0001]. Reversing: string constants in one file, plus any test that asserts on them.
3. **The listing separator is a tab.** Reversing: one format string and the tests that split on
   it; nothing stored changes [src: ADR-0005].
4. **`~` is resolved with the standard expansion**, which honours `HOME` where it is set. This
   is what lets AC5's default-path case be tested without writing into the checker's real home
   directory. Reversing: one call.
5. **The tests may set `RECALL_FILE` and `HOME` for a subprocess.** If that turned out to be
   forbidden, AC5 would need a different observation; nothing in the product changes
   [src: WI-0001 AC5].

## Decisions and ADRs

| decision | where | branch of the preference order |
|----------|-------|-------------------------------|
| Test command, lint command, and no third-party dependency | ADR-0003 | decided here, after measuring what the environment has |
| Store schema, write protocol, creation on first add, behaviour when the store cannot be read or written | ADR-0004 | decided here — ADR-0002 named all four as `plan`'s [src: ADR-0002] |
| Entry point, positional-only arguments, exit codes, streams, listing format | ADR-0005 | decided here |
| Store location and JSON format | ADR-0002, already recorded | answered from the documents |
| Interval ladder — not touched by this item | ADR-0001, already recorded | answered from the documents |
| Message wording, the tab separator, whitespace-only sides | `## Assumptions` above | reversible assumption |

Nothing in this plan was asked of the stakeholder. Everything open at the start of it was either
settled in a document already, or a reversible choice recorded above, or one of the four
questions ADR-0002 explicitly left to the architect [src: ADR-0002].

## Scaffolding

- `tests/__init__.py` — empty. Created so that `python3 -m unittest discover -s tests -t .`, the
  command this plan puts in `tracker/project.yaml`, can execute at all; discovery needs `tests`
  to be an importable package. It contains no behaviour, and deleting it breaks no acceptance
  criterion [src: ADR-0003].

## Risks

- **`os.replace` is atomic only within one filesystem.** The temporary file is created in the
  store's own directory, so this holds for any store the user can write. If a later change moved
  the temporary file elsewhere — `/tmp`, say — the guarantee would silently disappear
  [src: ADR-0004].
- **`compileall` is a compile check, not a linter.** Unused imports, shadowed names and dead code
  reach review unflagged, and the reviewer is what catches them [src: ADR-0003].
- **The default-path test depends on `HOME`.** If the checker's environment resolves `~` some
  other way, AC5's default-path observation fails while the product is correct. The
  `RECALL_FILE` half of AC5 does not depend on it [src: WI-0001 AC5].
- **`unittest discover` exits 5 when it finds nothing** [src: ADR-0003]. If the developer runs
  the gate before writing a test and reads 5 as a defect, the failure is in the reading, not the
  code.
- **The store is rewritten whole on every add.** Fine for one person's vocabulary; wrong at a
  scale nobody in this epic has asked for [src: ADR-0004].

## Out of scope for this item

- The `review` command, and every scheduling field on a card. WI-0003 adds them to the card
  objects and bumps the store's `version`; this item stores none of them [src: WI-0002;
  src: WI-0003].
- Editing or deleting a card [src: WI-0001].
- Decks, tags, categories, and any filtering of the pile [src: EP-001/Q-004].
- Card sides that are not plain text, or that span more than one line [src: WI-0001].
- Any behaviour when the store file has been hand-edited into a shape that is valid JSON but not
  this schema, beyond refusing to use it [src: ADR-0004].
