# Plan — WI-0001 Create and list named envelopes that survive between runs

## Problem

Someone who budgets by dividing money into named pots needs those pots to exist in the tool
before any money can go anywhere. This item delivers exactly two commands — `envel new <name>`
and `envel list` — and the file that makes them outlive the process. It carries no notion of
money: balances, income and spending are WI-0002 [src: WI-0001].

Three constraints shape the design rather than the behaviour. The store has to be reachable from
a clean state, or four of the eleven criteria cannot be observed at all — refinement recorded
that and routed it here [src: WI-0001]. The store's format has to survive any name, because the
stakeholder refused to let us restrict the characters a name may contain [src: WI-0001/Q-002].
And the wording of the tool's messages was routed here too: the criteria fix the stream, the exit
status and, where it matters, that `groceries` appears, and deliberately leave the sentence open
[src: WI-0001].

## Approach

Four pieces in a straight line from the terminal to the file, described in
`docs/architecture/overview.md` and fixed by ADR-0002, ADR-0003 and ADR-0004:

- **`bin/envel`** — the executable the person types, a launcher with no logic in it
  [src: ADR-0002].
- **`envel/cli.py`** — reads `argv`, dispatches, writes stdout and stderr, returns the exit
  status.
- **`envel/envelopes.py`** — the domain rules, with no filesystem access [src: ADR-0004].
- **`envel/store.py`** — where the store file is and how it is read and written [src: ADR-0003].

Three things in that arrangement are decisions rather than habits, and each is worth stating
here because a step below turns on it.

**Identity is computed once, at the boundary.** `identity(name)` is `name.strip().casefold()`, and
it is what decides whether two names are the same envelope. The stored **display form** is
`name.strip()` as first created, and that is what is printed [src: ADR-0004]. The consequence
that is easy to get wrong: when a duplicate is refused, the message names the **stored** envelope
and not what was typed. `envel new Groceries` after `envel new groceries` has to put `groceries`
on stderr [src: WI-0001 AC5 "The same holds when the second invocation differs only in case"], and
echoing the input would put `Groceries` there instead.

**Order is a display concern.** The store keeps envelopes in creation order; `envel list` sorts at
the moment of printing, by the UTF-8 bytes of the display name
[src: WI-0001 AC4 "sorted by name, ascending, byte-wise"]. Sorting by the identity key instead
would give a different order for names that differ in case, and the criterion is about the name.

**An absent store is an empty store.** Reading a store file that is not there yields the empty
document rather than an error, which is what lets the tool be run for the first time
[src: WI-0001 AC6 "run before any envelope has ever been created exits 0"]. A refused `envel new`
returns before anything is written, so a store file is not created by a command that failed —
which is what makes `envel list` afterwards byte-identical to the AC6 reference
[src: WI-0001 AC9 "writes stdout byte-identical to the AC6 reference output"].

**The messages**, chosen here under the item's routing and recorded under `## Assumptions`:

| situation | stream | text | exit |
|-----------|--------|------|------|
| `new` succeeded | — | nothing at all | 0 |
| `list` with no envelopes | stdout | `No envelopes yet. Create one with: envel new <name>` | 0 |
| `list` with envelopes | stdout | one display name per line, sorted | 0 |
| name already exists | stderr | `envel: an envelope named '<stored name>' already exists` | 1 |
| name is empty once trimmed | stderr | `envel: an envelope name cannot be empty` | 1 |
| the store cannot be read | stderr | `envel: <path> could not be read as an envel store: <detail>` | 1 |
| wrong number of arguments | stderr | `usage: envel new <name>` / `usage: envel list` | 2 |
| unknown command | stderr | `envel: unknown command '<word>'` then the usage line | 2 |

## Steps

1. **Create `envel/store.py`.** It exports `StoreError`, `store_path`, `load` and `save`.
   - `store_path(environ=os.environ)` returns `environ["ENVEL_FILE"]` used exactly as given when
     that variable is set and non-empty; otherwise `<XDG_DATA_HOME>/envel/store.json` when
     `XDG_DATA_HOME` is set and non-empty; otherwise
     `<expanduser("~")>/.local/share/envel/store.json` [src: ADR-0003].
   - `load(path)` returns `{"version": 1, "envelopes": []}` when `path` does not exist. Otherwise
     it reads the file as UTF-8 and parses it with `json.loads`, then checks the shape: a mapping
     at the top, `envelopes` a list, and each element a mapping whose `name` is a string. A read
     error, a parse error or a shape that fails those checks raises `StoreError` carrying the path
     and what was wrong.
   - `save(path, store)` creates the parent directory if it is missing, writes the document to a
     temporary file in that same directory with `json.dump(..., ensure_ascii=False, indent=2)` and
     a trailing newline, then `os.replace`s it over `path`. An `OSError` becomes a `StoreError`.
   - Afterwards: `python3 -c "import envel.store"` succeeds and nothing observable has changed.

2. **Create `envel/envelopes.py`.** It exports `InvalidName`, `DuplicateName`, `identity`,
   `display`, `find`, `add` and `listing`, and it imports nothing that touches a filesystem.
   - `identity(name)` is `name.strip().casefold()`; `display(name)` is `name.strip()`
     [src: ADR-0004].
   - `find(store, name)` returns the element of `store["envelopes"]` whose stored name has the
     same identity as `name`, or `None`.
   - `add(store, name)` raises `InvalidName` when `identity(name)` is empty; raises
     `DuplicateName`, carrying the **stored** display name of the element `find` returned, when one
     exists; otherwise appends `{"name": display(name)}` to `store["envelopes"]` and returns it.
     It mutates nothing on either failure path.
   - `listing(store)` returns the stored display names sorted by
     `lambda name: name.encode("utf-8")`, which is the byte-wise ascending order AC4 asks for.
   - Afterwards: the domain rules can be exercised with no store on disk.

3. **Create `envel/cli.py`.** It exports `main(argv=None)`, returning the process exit status, and
   holds the message constants from the table in `## Approach`.
   - With no arguments it writes the usage line to stderr and returns 2.
   - `new` with exactly one argument resolves the path with `store.store_path()`, calls
     `store.load`, calls `envelopes.add`, then `store.save`, and returns 0 having written nothing
     to either stream. `StoreError` returns 1; `InvalidName` returns 1; `DuplicateName` returns 1,
     with the message naming the stored envelope. `new` with any other number of arguments writes
     `usage: envel new <name>` to stderr and returns 2.
   - `list` with no arguments loads the store and prints `listing(store)` one name per line,
     returning 0; when that list is empty it prints the empty-store line instead and returns 0.
     With any argument it writes `usage: envel list` to stderr and returns 2.
   - Any other first word writes `envel: unknown command '<word>'` and the usage line to stderr
     and returns 2.
   - There is no option, flag or switch on either command, which is what the item's `## Out of
     scope` asks for [src: WI-0001]. That is why `argparse` is not used: it would add `-h` and
     `--help` to both.

4. **Create `bin/envel` and make it executable.** A `#!/usr/bin/env python3` shebang, then: put
   the directory above `bin/` at the front of `sys.path`, import `main` from `envel.cli`, and
   `raise SystemExit(main())`. Nothing else [src: ADR-0002]. Afterwards
   `PATH="$PWD/bin:$PATH" envel list` runs the tool.

5. **Create `tests/test_envelopes.py`** — `unittest` cases over `envel.envelopes` alone, with no
   file on disk: identity folds case and strips surrounding whitespace; `add` refuses an empty and
   an all-whitespace name; `add` refuses a name whose identity already exists and reports the
   stored spelling; `listing` returns byte-wise ascending order, including a pair such as `Zebra`
   and `apple` where byte order and alphabetical order disagree.

6. **Create `tests/test_cli.py`** — end-to-end `unittest` cases, one per acceptance criterion,
   each invoking the tool the way the criterion is written. A helper builds a child environment
   from `os.environ` with `PATH` prefixed by the repository's `bin/` directory and `ENVEL_FILE`
   set to `store.json` inside a fresh `tempfile.TemporaryDirectory()`, then calls
   `subprocess.run(["envel", ...], env=..., capture_output=True, text=True)`. Each test gets its
   own temporary directory, so every one of them starts from a store that has never existed.
   The AC6 test keeps its stdout and the AC9 and AC10 tests compare against it, so the three read
   the same reference the criteria describe.

7. **Update `docs/architecture/overview.md`.** Replace the paragraph in `## What this is` that
   says the document names modules the plan has not yet created, and give the four rows of the
   `## The shape` table citations to the files that now exist. Bump `version` to 2 and add a
   change-log row. This document is entry 2 of the invalidation set, which is what permits this
   edit [src: WI-0001].

Nothing in these steps asks a downstream skill to tick an acceptance criterion, to write a
document outside the invalidation set, or to make a statement about the engagement. Ticking the
criteria is `verify`'s [src: WI-0001].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 1, 2, 3, 4 | `tests/test_cli.py` — `envel new groceries` on a fresh `ENVEL_FILE`: `returncode == 0` and `stderr == ""` |
| AC2 | 1, 2, 3, 4 | `tests/test_cli.py` — after AC1's command, `envel list`: `returncode == 0` and `stdout == "groceries\n"` |
| AC3 | 1, 3, 4 | `tests/test_cli.py` — three separate `subprocess.run` calls sharing one `ENVEL_FILE`: `envel new a`, `envel new b`, `envel list`; `stdout == "a\nb\n"` and `returncode == 0` |
| AC4 | 2, 3 | `tests/test_cli.py` — create `Zebra` and `apple`, run `envel list` twice; the two stdouts are equal and the single stdout is `"Zebra\napple\n"`, which is byte-wise ascending and is not alphabetical order. Plus `tests/test_envelopes.py` on `listing` directly |
| AC5 | 2, 3 | `tests/test_cli.py` — `envel new groceries`, then `envel new groceries`, then `envel new Groceries`: each repeat has `returncode != 0` and `"groceries" in stderr`; a following `envel list` has `stdout == "groceries\n"`, one line |
| AC6 | 1, 3 | `tests/test_cli.py` — `envel list` with `ENVEL_FILE` pointing at a path that has never existed: `returncode == 0`, `stderr == ""`, `stdout.splitlines()` has at least one entry. The test keeps this stdout as `REFERENCE` |
| AC7 | 2, 3 | `tests/test_cli.py` — `envel new Groceries` on a fresh store, then `envel list`: `stdout == "Groceries\n"` |
| AC8 | 2, 3 | `tests/test_cli.py` — `envel new "eating out"`: `returncode == 0`; then `envel list`: `stdout == "eating out\n"` |
| AC9 | 2, 3 | `tests/test_cli.py` — `envel new ""`: `returncode != 0` and `stderr.splitlines()` is non-empty; then `envel list`: `stdout` equals AC6's `REFERENCE` byte for byte |
| AC10 | 2, 3 | `tests/test_cli.py` — the same with `"   "` in place of `""` |
| AC11 | 2, 3 | `tests/test_cli.py` — `envel new groceries`, then `envel new "  groceries  "`: `returncode != 0` and `"groceries" in stderr`; then `envel list`: `stdout == "groceries\n"`, with no leading or trailing space on the line |

Every one of these runs under `python3 -m unittest discover -s tests -t .`, which is
`commands.test` in `tracker/project.yaml`. A criterion can also be run by hand in the form it is
written in, for example:

```
T=$(mktemp -d); PATH="$PWD/bin:$PATH" ENVEL_FILE="$T/store.json" envel new groceries; echo $?
```

## Assumptions

Each is reversible in the sense `plan`'s procedure uses — one file, no data migration, no change
to an interface anybody outside this repository has seen. **No standing delegation exists in this
engagement**: no answer of the stakeholder's says "whatever you think is best" about anything, so
no `**Under delegation:**` line is written against any of these [src: WI-0001]. What licenses the
first three is narrower and named: the item's own `## Notes` routes message wording to `plan`
[src: WI-0001].

- **P1 — the exact message text**, as tabulated in `## Approach`. The criteria fix the stream, the
  exit status, and that `groceries` appears in two of them; the sentences are chosen here.
  Reversing: the constants in `envel/cli.py`, one file, nothing else.
- **P2 — the exit statuses: 1 for a refusal the person can act on, 2 for a usage error.** The
  criteria ask only for non-zero. Splitting them makes "you typed the command wrong" and "the tool
  will not do that" distinguishable by a script. Reversing: one file.
- **P3 — no argument-parsing library, so neither command accepts any option**, including `--help`.
  The item puts options out of scope, and `argparse` would add two. Reversing: one file, and it
  becomes the natural choice the moment an option is actually wanted.
- **P4 — a store file that cannot be read is reported and the command exits 1.** No criterion
  covers a corrupt store. The alternative — treating an unreadable file as empty — would overwrite
  the person's data on the next `new`, which is the one outcome this tool exists to prevent.
  Reversing: one function in `envel/store.py`.
- **P5 — output is written with the encoding Python picks for the environment.** Under a
  non-UTF-8 locale, printing a name with a non-ASCII character would fail. No criterion exercises
  it, and forcing UTF-8 on stdout would change behaviour under a locale nobody has stated a
  preference about. Reversing: one line in `envel/cli.py`. Carried into `## Risks` as well,
  because this one can bite the stakeholder rather than only a reader.
- **P6 — three modules rather than one file.** At this item's size one file would do. The split is
  along the line later items keep adding to, and it is what lets the domain rules be tested with
  no filesystem. Reversing: mechanical, and would lose nothing.

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| Python 3, standard library only; the test and lint commands that follow | `ADR-0001` | assumed, then recorded as a decision — the vision constrains it but does not settle it |
| `envel` reached through `bin/envel` rather than an install step | `ADR-0002` | decided here; no document settled it |
| One JSON store, and `ENVEL_FILE` / XDG path resolution | `ADR-0003` | decided here, from the constraints refinement routed to `plan` [src: WI-0001] |
| Identity is the trimmed casefolded name; the display form is the trimmed name as created | `ADR-0004` | answered from the record — `WI-0001/Q-002` and AC7 fix the substance; the ADR records the mechanism |
| A duplicate is refused and the message names the stored envelope | AC5, and `ADR-0004` `## Decision` rule 1 | answered from the record — the stakeholder's own words [src: WI-0001/Q-002] |
| Messages, exit statuses, no option parser, corrupt-store behaviour, output encoding, module split | `## Assumptions` P1–P6 above | assumed and recorded, with the reversal cost stated |

No ADR written by this execution reconciles two of the stakeholder's recorded answers against each
other. `WI-0001/Q-001` and `WI-0001/Q-002` were read together with `EP-001/Q-001` … `EP-001/Q-005`
and nothing in them conflicts; ADR-0004 records a mechanism for what `WI-0001/Q-002` already
decided rather than choosing between two things they said.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/product/vision.md` | the `## Engagement state` section — the bullets beginning "The stakeholder stated this idea and has not been asked to accept anything yet", "Five questions from intake are open with them" and "Nothing has been designed or built" | engagement-state | this item is being designed and then built, the five intake questions have been answered and consumed, and the epic now has five children rather than three — so each of those sentences stops being true. They are sentences about the engagement, not about the product, so they belong to the ending. The same section additionally carries the unsourced absolute `claims-are-sourced` reports at `docs/product/vision.md:79` (`WI-0001/Q-003`); that is not this change's to repair either, and `review-close`'s restatement at the ending is where it clears | owned-by-ending |
| `docs/process/ways-of-working.md` | the whole document — it did not exist before `WI-0001/Q-003` was answered | cited-fact | the answer to `Q-003` had to land somewhere a later execution re-reads, and the plans of WI-0002 to WI-0005 will name `docs/product/vision.md` for the same reason and meet the same refusal. Created by `answer-questions` on this branch, so the set has to name it or the branch diff carries a document nobody accounted for | to-update |
| `docs/architecture/overview.md` | the `## What this is` paragraph saying the document "names the modules the plan creates rather than citing lines in them", and the four rows of the `## The shape` table | cited-fact | the table asserts what `bin/envel`, `envel/cli.py`, `envel/envelopes.py` and `envel/store.py` are responsible for, and none of those files exists yet. The execution that writes them is what makes the assertions point at something, and a different split or different names would make the table false | to-update |

## Deliverable documents

- none. No acceptance criterion on this item is about a document.

## Binding ADRs

- `ADR-0001` — the standard-library-only clause binds every step: no step may reach for a package,
  and the test and lint commands the steps are checked with come from it.
- `ADR-0002` — the launcher clause binds step 4 and the shape of every demonstration in the
  criteria mapping, which reaches the tool through `PATH` rather than through an install.
- `ADR-0003` — the path-resolution order and the store's shape bind step 1, and the
  absent-file-is-an-empty-store clause binds AC6, AC9 and AC10.
- `ADR-0004` — the identity rules bind step 2 and step 3: rule 1 (the message names the stored
  envelope) and rule 2 (an empty identity is refused) are what AC5, AC9, AC10 and AC11 check.

## Scaffolding

Two empty files, both created by this execution, both outside `tracker/` and `docs/`, neither
containing behaviour, and no acceptance criterion depends on either:

- `tests/__init__.py` — without it, `python3 -m unittest discover -s tests -t .` does not fail, it
  errors: `ImportError: Start directory is not importable`. The command recorded as
  `commands.test` could not be run at all.
- `envel/__init__.py` — without it, `python3 -m compileall -q envel tests` prints `Can't list
  'envel'` and exits 0, so the command recorded as `commands.lint` would report success having
  examined nothing under the package.

## Risks

- **A non-UTF-8 locale.** Assumption P5. The stakeholder was promised the characters in a name
  would not be restricted [src: WI-0001/Q-002], and under `LC_ALL=C` printing a name with a
  non-ASCII character raises `UnicodeEncodeError`. The store itself is safe — it is written UTF-8
  with `ensure_ascii=False` [src: ADR-0003] — so this is a display failure and not a data one. If
  it turns out to matter it is one line, and it is written here so it is a known gap rather than a
  surprise.
- **A manual check with `ENVEL_FILE` unset writes to the person's real store**, at
  `~/.local/share/envel/store.json`. The automated tests set it for every invocation, and the
  by-hand form in the criteria mapping sets it too. Anyone running a criterion by hand without it
  is editing real data.
- **`commands.lint` is a syntax check, not a linter** [src: ADR-0001], and it does not reach
  `bin/envel`, which has no `.py` extension. What covers the launcher instead is that the
  end-to-end tests invoke the tool through it.
- **AC4's ordering is an assumption the stakeholder has never confirmed** — refinement recorded it
  as taken under no licence [src: WI-0001]. This plan implements it. If they want creation order,
  the change lands on the item as a send-back to `refine` and step 2's `listing` is the one line
  that moves.
- **Two `envel` processes running at the same instant can lose one of the two writes.** The
  replacement is atomic, so the file is never half-written [src: ADR-0003], but there is no lock:
  the second save overwrites a document the first had already changed. One person at one terminal
  is what this is for [src: docs/product/vision.md], and adding a lock is not free.

## Out of scope for this item

- Anything to do with money. Balances, income and spending are WI-0002 [src: WI-0001].
- Renaming, deleting or archiving an envelope; creating more than one in a single invocation;
  grouping or nesting; any option, flag or switch — all excluded by the item itself
  [src: WI-0001].
- Unicode normalisation of names, and therefore whether a combining accent and a precomposed
  character are one envelope. Recorded and deliberately not decided [src: ADR-0004].
- Locking, or any behaviour for two processes writing at once. See `## Risks`.
- A `pyproject.toml`, a packaged install, or a `--version` flag [src: ADR-0002].
