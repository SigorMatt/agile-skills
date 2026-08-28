# Plan — WI-0003 Let the user supply the sorting rules instead of using built-in ones

## Problem

The tool sorts a folder by two tables it holds as constants: extension to type folder, and age to
band [src: tidy/rules.py]. This item hands both to the user. A rule file's type entries layer over
the built-in table and win where they collide, so a two-line file redirects one extension and
leaves the other seventy alone [src: WI-0003/Q-001]; the age side stays at exactly two bands,
whose names and single boundary become the user's [src: WI-0003/Q-002]. A file that says nothing
about one of the two tables keeps that table's built-in values [src: WI-0003 AC6].

The constraints are all already recorded. Standard library only, Python 3.9 floor
[src: ADR-0001]. Every destination is decided in `planner.py` and nowhere else [src: ADR-0002].
`cli.py` imports no table, and a test is what keeps the `--help` text honest [src: ADR-0008]. An
event that ends the run before there is a run belongs to `cli.py` and exits 2 [src: ADR-0006].
Nothing here may weaken the never-overwrite rule or make the tool descend into subfolders: both
are invariants the stakeholder settled, not configurables [src: EP-001/Q-002; src: EP-001/Q-003].

## Approach

Two decisions, both recorded as ADRs, and the shape falls out of them.

**Rules arrive as one INI file named with `--rules PATH`, with no default location**
[src: ADR-0010]. Two optional sections: `[types]`, extension to one folder name; `[bands]`, with
exactly the three keys `newer`, `older` and `boundary-days`. Fixed band keys rather than a list is
what makes a third band unrepresentable rather than merely rejected, which is the stakeholder's
answer A expressed in the format itself [src: WI-0003/Q-002]. A rule file that will not load is
reported at the CLI boundary, before the target folder is examined, and exits 2 [src: ADR-0006].

**A `Ruleset` is a value passed into the planner** [src: ADR-0011]. `rules.py` gains a frozen
`Ruleset` holding the merged extension index and the two bands, with the two existing lookups as
its methods; `BUILT_IN` is the one built from `DEFAULT_RULES` and `DEFAULT_BANDS`, which do not
change; `build_plan(folder, ruleset=None)` takes it and resolves `None` to `BUILT_IN`. The merge is a
dict update on the extension-to-folder index, which is why "mine win" is one assignment per
entry.

The layering falls out: `merge` starts from `BUILT_IN`, overwrites the extensions the file names,
and replaces the band pair only if `[bands]` is present. Omit a section and nothing about that
table changes.

New module, `tidy/ruleset_file.py`: read the file, validate it, return a `Ruleset` or raise a
`RuleFileError` carrying one sentence. It is separate from `rules.py` because `rules.py` is the
tables and their lookups and has never touched the filesystem [src: tidy/rules.py], and separate
from `cli.py` because `cli.py` renders and exits but decides nothing.

## Steps

1. **`tidy/rules.py` — add the `Ruleset` value.** Add a frozen dataclass `Ruleset` with fields
   `by_extension` (dict, lowercase extension → folder name) and `bands` (tuple of
   `(name, max_age_seconds or None)` pairs), and methods `folder_for(filename)` and
   `band_for(age_seconds)` carrying the bodies the two module-level functions have now. Keep
   `DEFAULT_RULES`, `DEFAULT_BANDS` and `extension_of` exactly as they are. Add
   `BUILT_IN = Ruleset(by_extension=_BY_EXTENSION, bands=DEFAULT_BANDS)`. Remove the module-level
   `folder_for` and `band_for`. Afterwards: `Ruleset(...).folder_for("A.CSV") == "spreadsheets"`
   and `BUILT_IN.band_for(400 * 24 * 3600) == "old"`.

2. **`tidy/rules.py` — add the merge.** `merge(base, types=None, bands=None) -> Ruleset`, returning
   a new `Ruleset`: `by_extension` is `base.by_extension` updated with `types` (so a named
   extension is redirected and an unnamed one is untouched); `bands` is `bands` when given and
   `base.bands` otherwise. Neither argument is mutated. Afterwards:
   `merge(BUILT_IN, types={".csv": "data"}).folder_for("x.csv") == "data"` and
   `.folder_for("x.jpg") == "images"`, and its `.bands` is `DEFAULT_BANDS`.

3. **`tidy/planner.py` — take the ruleset as a parameter.** `build_plan(folder, ruleset=None)`,
   resolving `None` to `BUILT_IN` in the body — **not** a `BUILT_IN` default in the signature, so
   that `cli.py` never has to import it (ADR-0011, and the risk below);
   replace the two module-level calls with `ruleset.folder_for(name)` and
   `ruleset.band_for(...)`. Nothing else in the function changes — the collision handling, the
   `leave` reasons, the per-entry `OSError` boundary and the single clock read all stay
   [src: ADR-0005; src: ADR-0009]. Afterwards: `build_plan(folder)` behaves exactly as before,
   and `build_plan(folder, ruleset=other)` uses `other`'s tables.

4. **`tidy/ruleset_file.py` — new module: load and validate.** `load(path) -> Ruleset` and
   `class RuleFileError(Exception)`. Read with `configparser.ConfigParser` with `optionxform`
   set to `str` so values and keys keep their case; catch `configparser.Error` and `OSError` and
   re-raise as `RuleFileError` with the parser's or the operating system's own words. Then
   validate, raising `RuleFileError` with one sentence naming what is wrong, in this order:
   - a section other than `[types]` or `[bands]`;
   - in `[types]`: a key not beginning with `.`; a value that is empty or contains `/` or
     `os.sep`;
   - in `[bands]`: a key other than `newer`, `older`, `boundary-days`; any of the three missing;
     `boundary-days` not parsing as a number or not strictly positive; `newer` or `older` empty,
     containing a separator, or equal to each other.

   Then return `merge(BUILT_IN, types=..., bands=...)`, lowercasing extension keys and converting
   `boundary-days` to `(newer, days * 24 * 3600), (older, None)`. Afterwards: a good file yields a
   `Ruleset`; each malformed class raises `RuleFileError` whose message names the file and the
   problem; nothing touches the target folder.

5. **`tidy/cli.py` — add `--rules` and report a bad one.** Add
   `parser.add_argument("--rules", metavar="PATH", help=...)` and extend the epilog with one
   sentence naming `--rules` and pointing at `README.md`. In `main`, **before** the
   `os.path.isdir` check: if `args.rules`, call `ruleset_file.load`, and on `RuleFileError` write
   `"tidy: %s\n" % error` to stderr and return 2; otherwise leave the ruleset as `None`. Pass it
   to `build_plan` either way. **`cli.py` must not import anything from `tidy/rules.py`**: ADR-0008
   states its condition as a grep over this file's imports, and a `from .rules import BUILT_IN`
   would break it silently [src: ADR-0008]. Afterwards: a bad rule file prints one stderr line,
   nothing on stdout, exits 2, in both modes; a good one changes where files go, and
   `grep -n "^from\|^import" tidy/cli.py` still returns no line naming `rules`.

6. **`tests/test_rules.py` — move the lookups onto the value, and test the merge.** Update every
   call of `folder_for`/`band_for` to go through a `Ruleset` (mostly `BUILT_IN`), and add tests
   for `merge`: an override, an addition, an untouched extension, bands replaced, bands absent,
   and that `BUILT_IN` is unchanged after a merge.

7. **`tests/test_ruleset_file.py` — new: the loader.** One test per malformed class from step 4,
   each asserting `RuleFileError` and that the message names the offending key or value; plus a
   well-formed file with both sections, one with `[types]` only, one with `[bands]` only, one with
   comments and blank lines, and one checking `optionxform` keeps `Photos` capitalised.

8. **`tests/test_planner.py` — the ruleset parameter.** Add tests that `build_plan(folder)` is
   unchanged and that `build_plan(folder, ruleset=merge(BUILT_IN, types={".xyz": "notes"}))` turns
   the `leave` for `notes.xyz` into a move, and that a type folder named `old` produces
   `old/old/report.pdf` for an old file — the destination is used verbatim (Assumption A1).

9. **`tests/test_cli.py` — the flag, end to end, over the sample folder.** Build sample folder `S`
   from the item's preamble with `os.utime`, using the helpers in `tests/support.py` and
   `tests/cli_support.py`. Cover: AC1 (no `--rules`, output and tree unchanged); AC2, AC3, AC4
   (rule files `F1`, `F2`, `F3` and the one differing line); AC5 (`F4`, plus three files at the
   90-day boundary, minus and plus a minute); AC6 (each section alone); AC7 (a fourth band key);
   AC8 (one file per class, both modes, stderr line, empty stdout, exit 2, folder untouched); AC9
   (`F5` and a pre-existing `recent/papers/report.pdf`); AC10 (`.hidden.jpg`, a pre-existing
   subfolder, and an extension in neither table); AC11 (preview pairs against the tree after
   apply, for `F1`, `F2`, `F4`, `F5`, `F6`).

10. **`README.md` — document all of it.** A "Your own rules" section after "Where each file goes":
    where a rule file comes from (`--rules PATH`, and that there is no default location), a
    complete worked example producing AC2's and AC5's results, that entries layer over the
    built-in table and that a mapping can be redirected but not removed, that there are exactly
    two bands whatever they are called, what a rejected file does and that it exits 2, and that a
    type folder named the same as a band gives `old/old/report.pdf` rather than an error. Extend
    the existing exit-status sentence so 2 covers a rule file that cannot be used.

11. **`docs/architecture/overview.md` — record what landed.** Update the module table with
    `tidy/ruleset_file.py`, replace the two "deliberately not here" entries that say rule loading
    and band configuration do not exist, and replace the WI-0003 forecast with what was done.
    Bump to version 8 with a change-log row. (`plan` has already made the forecast edits it may;
    this row is `implement`'s, at the point the code exists.)

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — no rules, nothing changes | 3, 5 | `build_plan`'s parameter defaults to `BUILT_IN` and `--rules` is optional; the whole existing suite passes unedited (`python3 -m unittest discover -s tests -t . -q`), plus a `test_cli.py` case running PREVIEW and APPLY over `S` with no flag and comparing against the item's table |
| AC2 — a named extension is redirected, others are not | 2, 9 | `test_cli.py`: `F1` (`.csv = data`) over `S`, asserting `move   budget.csv -> recent/data/budget.csv` and the other five lines byte-equal to the AC1 run |
| AC3 — an extension the built-in table lacks | 2, 9 | `test_cli.py`: `F2` (`.xyz = notes`) over `S`, asserting `move   notes.xyz -> recent/notes/notes.xyz` where AC1 gives a `leave` line |
| AC4 — two rule files, two previews, one differing line | 9 | `test_cli.py`: `F1` then `F3` (`.csv = tables`) over the same unmoved `S`; diff the two stdouts and assert exactly one line differs and what it says |
| AC5 — bands renamed, boundary moved | 4, 9 | `test_cli.py`: `F4` (`newer=current`, `older=archive`, `boundary-days=90`) over `S`, plus three files with mtimes at exactly 90 days, 90 days − 1 min, 90 days + 1 min, asserting `archive/`, `current/`, `archive/` |
| AC6 — either section alone | 2, 9 | `test_cli.py`: `F1` alone puts `taxes.pdf` at `old/documents/taxes.pdf`; `F4` alone puts `budget.csv` at `current/spreadsheets/budget.csv` |
| AC7 — exactly two bands | 4, 7, 9 | `test_ruleset_file.py`: a `[bands]` with a fourth key raises `RuleFileError` naming it; `test_cli.py`: the same file exits 2 with one stderr line and empty stdout |
| AC8 — six malformed classes, both modes | 4, 5, 7, 9 | `test_ruleset_file.py`: one test per class asserting the message names the offending key or value; `test_cli.py`: one file per class run in both modes, asserting exit 2, one stderr line, empty stdout, and `S` unchanged (compare a recursive listing before and after) |
| AC9 — never-overwrite on a user destination | 3, 9 | `test_cli.py`: `F5` (`.pdf = papers`) with `recent/papers/report.pdf` pre-existing; assert the `(2)` destination in both modes and that the pre-existing file's bytes are identical afterwards |
| AC10 — hidden files, subfolders, no catch-all | 3, 9 | `test_cli.py` under `F1`: `.hidden.jpg` in neither mode's output and unmoved; a pre-existing `documents/` and its contents untouched and unlisted; `notes.xyz` still a `leave` line |
| AC11 — preview and apply agree, collision included | 3, 8, 9 | `test_cli.py`: for each of `F1`, `F2`, `F4`, `F5`, `F6` (`.pdf = old`), capture PREVIEW's (name, destination) pairs, run APPLY on an unchanged copy, assert every file is at the printed path — `taxes.pdf` at `old/old/taxes.pdf` for `F6` |
| AC12 — `README.md` says all of it | 10 | Read `README.md` against AC2, AC5, AC7, AC8 and AC11; the worked example is the one from ADR-0010 and produces AC2's and AC5's results |

## Assumptions

- **A1 — a type folder whose name equals a band name is used verbatim.** `F6` sending `.pdf` to
  `old` gives `old/old/taxes.pdf` for an old file, not an error. `refine` left this deliberately
  unconstrained and routed it here [src: WI-0003]. Rejecting it would be wrong for a user who
  renamed their bands to `current`/`archive` and legitimately wants a type folder called `old`,
  and nothing can be overwritten either way — the preview shows the real destination before
  anything moves. **Reversing** means adding one check in `ruleset_file.load` and its test: one
  module, no data on disk, no interface change. AC11 and AC12 already bind whichever behaviour to
  be consistent across modes and documented.
- **A2 — `boundary-days` may be fractional.** `configparser` returns a string and the loader
  converts it with `float`; `0.5` is a valid half-day boundary. Nothing requires it and nothing
  forbids it, and rejecting non-integers would be a rule the user has to discover. **Reversing**
  is changing `float` to `int` in one line plus one test.
- **A3 — the sample folder `S` is built by the tests, not shipped.** The item fixes its contents
  and mtimes [src: WI-0003]; the tests construct it with `os.utime` as the existing suite already
  does [src: tests/support.py]. **Reversing** — shipping a fixture directory — is not reversal so
  much as a different choice, and it would cost the ability to set mtimes relative to the run.

## Decisions and ADRs

| decision | where it is recorded |
|----------|----------------------|
| INI via `configparser`, over JSON and TOML | ADR-0010 |
| `--rules PATH`, no default location | ADR-0010 |
| `[bands]` has three fixed keys, so a third band is unrepresentable | ADR-0010 |
| A bad rule file is the CLI's, exits 2, and is checked before the folder | ADR-0010, applying ADR-0006 |
| A `Ruleset` value passed into `build_plan`, over module state or two parameters | ADR-0011 |
| The merge is a dict update on the extension index, not on `DEFAULT_RULES` | ADR-0011 |
| A type folder named like a band is used verbatim | Assumption A1 above |
| `boundary-days` may be fractional | Assumption A2 above |
| One rule file with two sections, not two files | ADR-0010 (the format), ADR-0011 (the merge takes both) |

## Scaffolding

None. `commands.test` and `commands.lint` are already real and already run in this project
[src: tracker/project.yaml], and every file this plan adds is behaviour that belongs to
`implement`.

## Risks

- **Step 6 touches tests that currently pass.** Moving `folder_for` and `band_for` onto `Ruleset`
  changes every call site in `tests/test_rules.py` [src: tests/test_rules.py]. A reviewer should
  read those edits as a rename, and be suspicious of any that changes an assertion rather than a
  call. If an assertion has to change, the parameter did more than it was supposed to.
- **The quietest way to get this wrong is an import.** If `cli.py` imports `BUILT_IN` to pass as
  a default, every test still passes and ADR-0008's stated checkable condition — that
  `grep -n "^from\|^import" tidy/cli.py` returns no line importing `rules` — becomes false
  [src: ADR-0008]. Step 3's `ruleset=None` exists to make that unnecessary. A reviewer should run
  that grep.
- **ADR-0008's help guard will object.** `tests/test_cli.py` asserts every name in
  `DEFAULT_BANDS` appears in the `--help` output [src: ADR-0008; src: tests/test_cli.py]. This
  item does not change `DEFAULT_BANDS`, so the guard should stay green — if it does not, something
  made the built-in bands user-dependent, which contradicts AC1 and is worth stopping for.
- **`configparser` has sharp edges beyond `optionxform`.** Duplicate keys raise by default;
  interpolation treats `%` specially, which a destination folder could contain. The loader should
  use `ConfigParser(interpolation=None)` — a folder named `100%` is not the user's problem to
  know about. This is a note for `implement`, not a decision: it changes no behaviour anyone
  specified.
- **AC8's "one line on stderr" is a real constraint on the loader.** `configparser`'s exception
  strings can be multi-line. `RuleFileError` messages must be collapsed to one line, or the
  criterion fails on formatting rather than on behaviour.
- **The plan assumes the six malformed classes are exhaustive enough.** They came from `refine`
  and match the format ADR-0010 chose [src: WI-0003 AC8]. A file that is well-formed INI and
  passes all six checks but still means nothing sensible — `.csv = .csv`, say — is accepted and
  filed under a folder called `.csv`. That is odd, not wrong, and the preview shows it.

## Out of scope for this item

Everything on the item's own list [src: WI-0003], and specifically: removing a built-in mapping,
a band count other than two, turning age routing off, a catch-all folder, and a destination more
than one folder deep. Also not here: a default rule-file location (ADR-0010 chose against it and
records adding one as cheap), and re-filing anything an earlier run already tidied, which the
no-recursion invariant settles [src: EP-001/Q-003].
