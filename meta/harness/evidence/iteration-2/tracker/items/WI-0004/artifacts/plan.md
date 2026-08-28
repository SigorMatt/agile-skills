# Plan — WI-0004 Pick up a rules file from a default location, without --rules

## Problem

Someone who has written a `tidy` rule file has to name it on every run: `--rules PATH`, every
time. They asked for the file to have "a default spot it just picks up on its own"
[src: EP-001/Q-005], and when asked which kind of place, chose their own config directory rather
than a file sitting in the folder being tidied [src: WI-0004/Q-001]. What changes is *which* rule
file a run reads and one line of what it prints; what does not change is anything about the rules
themselves, the planner, the mover, or the promises the tool already makes. The constraints are
that a run must still say what it is doing before it does it, so the run names the rule file it
used [src: ADR-0014]; that stdout stays one line per file, so that line goes to stderr
[src: tidy/cli.py]; and that a file the user did not put there must never shape a run, which is why
the folder being tidied is not a rule source [src: WI-0004].

## Approach

`tidy/ruleset_file.py` is already the only module that reads a rule file [src: ADR-0011]. It gains
the decision of *which* file to read, as two small functions beside `load`:

- **`default_path(environ)` → `str` or `None`.** `<XDG_CONFIG_HOME>/tidy/rules.ini` when that key
  is present and non-empty in `environ`; otherwise `<HOME>/.config/tidy/rules.ini` when `HOME` is
  present and non-empty; otherwise `None`. It reads the mapping it is handed and touches neither
  `os.environ` directly nor `os.path.expanduser`, so what a run will read is a function of its
  environment and a test can state it [src: ADR-0014].
- **`resolve(argument, environ)` → `(Ruleset, path)` or `(None, None)`.** When `argument is not
  None` — `--rules` was given, empty string included — it is `(load(argument), argument)`.
  Otherwise it computes `default_path(environ)`; when that is `None`, or when nothing exists at
  it, the answer is `(None, None)`; when something is there, it is `(load(path), path)`.
  `RuleFileError` propagates untouched in every case.

Presence at the default path is tested with `os.path.lexists`, not `os.path.exists`: a symlink
pointing nowhere is something the user put there, and `load` will then refuse it with the operating
system's own reason. That is the difference AC2 and AC6 require between *absent* — a no-rules run —
and *present but unusable* — exit 2 [src: ADR-0014].

`tidy/cli.py` changes in three ways and no more: it calls `resolve` instead of guarding `load` with
`if args.rules:`; it writes `tidy: using rules from <path>` to stderr immediately after a
successful load, which is before the folder is examined and therefore before any per-file line; and
its `--rules` help text and its epilog stop saying there is no default location. Nothing else in
the layering moves: `build_plan` still receives a `Ruleset` or `None` and cannot tell where it came
from [src: ADR-0011].

The `Ruleset` `resolve` returns is the one `load` returns today [src: tidy/ruleset_file.py], so
`planner.py`, `rules.py` and `apply.py` are not touched.

## Steps

1. **`tidy/ruleset_file.py` — add `default_path(environ)`.** Returns the joined path per ADR-0014's
   point 1, or `None`. Module-level constants for the two pieces (`CONFIG_SUBDIRECTORY = "tidy"`,
   `RULE_FILE_NAME = "rules.ini"`) so the path exists in one place. Afterwards:
   `default_path({"XDG_CONFIG_HOME": "/tmp/c"})` is `/tmp/c/tidy/rules.ini`,
   `default_path({"HOME": "/home/u"})` is `/home/u/.config/tidy/rules.ini`, `default_path({})` is
   `None`, and an empty-string value for either key is treated as absent.
2. **`tidy/ruleset_file.py` — add `resolve(argument, environ)`.** As described in `## Approach`,
   returning the pair. The docstring states why the test is `argument is not None` rather than
   truthiness, and why presence is `lexists` — both are ADR-0014's, and both are the kind of
   one-character choice that gets "corrected" later by someone who does not know it was a decision.
   Afterwards: `resolve(None, {})` is `(None, None)`; `resolve(None, env)` with a valid file at the
   default path returns that file's `Ruleset` and its path; `resolve("", {})` raises
   `RuleFileError`; `resolve(p, env)` ignores `env` entirely.
3. **`tidy/cli.py` — use `resolve`, and name the file.** Replace the `if args.rules:` block with a
   `resolve(args.rules, os.environ)` call inside the same `try`/`except RuleFileError` that already
   turns a bad rule file into one stderr line and exit 2 [src: ADR-0006; src: ADR-0010]. On
   success, when the returned path is not `None`, write `tidy: using rules from %s\n` to stderr.
   This stays above the `os.path.isdir` check, so a rule file is still resolved before the target
   folder is examined [src: tidy/cli.py]. Afterwards: a run with a rule file from either source
   prints that one extra stderr line and nothing new on stdout; a run with none prints exactly what
   it prints today.
4. **`tidy/cli.py` — the help text.** The `--rules` argument's `help` and the parser's `epilog`
   both say there is no default location today [src: tidy/cli.py]. Rewrite both to name the default
   path in its two forms and to say `--rules` overrides it. Afterwards: `python3 -m tidy --help`
   contains no occurrence of "no default location" and does contain `rules.ini`.
5. **`tests/support.py` — make the suite hermetic.** `FolderTestCase.setUp` gains a second
   temporary directory and points `XDG_CONFIG_HOME` at it for the duration of the test, with
   `HOME` removed, using `unittest.mock.patch.dict(os.environ, ...)` and `addCleanup`. Add a helper
   `write_default_rules(text)` that creates `<that dir>/tidy/rules.ini`. **No assertion in any
   existing test changes.** This is not a test edited to accommodate the item: without it, every
   test in the suite would read whatever rule file the person running it happens to have in their
   own home directory, which is a new environment dependency the item introduces. Named in
   `## Risks` because AC2 is the criterion a reviewer will read it against.
6. **`tests/test_ruleset_file.py` — unit tests for the two new functions.** The four `default_path`
   cases of step 1 including both empty-string cases; `resolve`'s five cases from step 2. These are
   the cheap tests: no folder, no CLI, just the mapping and the pair.
7. **`tests/test_cli.py` — end to end, one test per criterion.** Using the existing `run()` helper
   and the sample folder the criteria define [src: WI-0004]: AC1 (`F1` and `F4` at the default
   path, both modes, compared against the `--rules` result on the same file), AC2 (nothing there,
   and separately an environment with neither variable), AC3 (`F1` at the default path plus
   `--rules F3`), AC4 (stderr carries the path, stdout does not, and a no-rules run carries
   neither), AC5 (one file per WI-0003 AC8 class at the default path), AC6 (a mode-`000` file, and
   a dangling symlink), AC7 (a zero-byte file), AC8 (the invariants under a default rule file),
   AC10 (`--help`). AC5's six classes reuse whatever `tests/test_ruleset_file.py` already builds for
   WI-0003 AC8 rather than restating them.
8. **`README.md` — the "Your own rules" section.** Delete "**There is no default location.**" and
   the sentence after it, and put in its place: where the default file is in both its forms, that
   `--rules` overrides it, that a run says on stderr which rule file it used and says nothing when
   it used none, that a file there which is malformed or unreadable stops the run with exit 2 and
   moves nothing, and that an empty file there is read and changes nothing. Afterwards: AC9 can be
   checked by reading that section against AC1–AC7.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — a file at `D` sorts the folder, both modes | 1, 2, 3 | `tests/test_cli.py`: `F1` at the default path, PREVIEW stdout equals WI-0003 AC2's lines; APPLY over an unchanged `S` puts every file where PREVIEW said; repeated with `F4`; and each compared against the same file passed with `--rules` |
| AC2 — nothing readable at `D` is a no-rules run | 1, 2, 5 | `tests/test_cli.py`: an empty config directory gives WI-0003 AC1's output and tree; a second test with `environ` carrying neither `XDG_CONFIG_HOME` nor `HOME` gives the same and exits 0. Plus `python3 -m unittest discover -s tests -t . -q` exit 0 with no assertion changed |
| AC3 — `--rules` beats `D` | 2, 3 | `tests/test_cli.py`: `F1` at the default path with `--rules F3`; stdout names `recent/tables/budget.csv` and the stderr line names `F3`'s path |
| AC4 — the run names the file it used, on stderr, and says nothing when it used none | 3 | `tests/test_cli.py`: `result.stderr` contains the path and `result.stdout` does not, for a default-path run and a `--rules` run, in both modes; and a no-rules run's stderr contains no such line |
| AC5 — a malformed file at `D` is refused as a named one is | 2, 3 | `tests/test_cli.py`: one file per WI-0003 AC8 class at the default path; stderr one line, stdout empty, exit 2, `self.listing()` unchanged, both modes |
| AC6 — present and unreadable is exit 2, not a no-rules run | 2 | `tests/test_cli.py`: a mode-`000` file and a dangling symlink at the default path; same four observations as AC5 |
| AC7 — an empty file at `D` is a rule file that was used | 2, 3 | `tests/test_cli.py`: a zero-byte file at the default path; stdout equals AC2's, stderr names the path, exit 0 |
| AC8 — a default rule file changes nothing else the tool promises | 3 | `tests/test_cli.py`: `F1` at the default path over `S` with a colliding `recent/data/budget.csv` — the `(2)` line in both modes, the pre-existing file's sha unchanged after APPLY, `.hidden.jpg` absent from both streams, a pre-existing subfolder untouched, `notes.xyz` still a `leave` line |
| AC9 — `README.md` states all of it | 8 | Reading the rewritten "Your own rules" section against AC1–AC7, and `grep -c "There is no default location" README.md` → 0 |
| AC10 — `--help` no longer says there is no default location | 4 | `tests/test_cli.py`: `run("--help")` stdout contains `rules.ini` and does not contain "no default location" — a test, so it cannot go stale unnoticed the way BUG-0003 did [src: ADR-0008; src: BUG-0003] |

## Assumptions

- **A1 — `XDG_CONFIG_HOME` is used exactly as given, without checking that it is absolute.** The
  XDG convention says a relative value should be ignored; honouring that would be one more branch
  and one more error case for a situation nobody in this project has. Reversing it is one condition
  in `default_path` and one test. Nothing else depends on it.
- **A2 — the line's wording is `tidy: using rules from <path>`,** with the path exactly as
  `resolve` returned it: as typed for `--rules`, and the joined default path otherwise. Not
  normalised, not made absolute — showing the user something other than what they typed would make
  the line harder to act on, not easier. `refine` left the wording to this skill
  [src: WI-0004]; AC4 constrains the stream, the ordering and that the path is in it, and no test
  should assert the surrounding words beyond the path itself. Reversing it is one format string.
- **A3 — a rule file that resolves but whose *directory* cannot be listed behaves like any other
  unusable file.** `lexists` returns `False` when a parent directory is unsearchable, so such a run
  is a no-rules run rather than exit 2. This is the one place where "present but unusable" is
  reported as "absent", and it is accepted because the alternative is `stat`-ing parents to tell the
  two apart for a case no criterion names. Reversing it means catching `OSError` from `lexists`.
- **A4 — `tests/support.py`'s environment isolation belongs in the shared base class** rather than
  in each new test. It changes no assertion; see `## Risks`.

## Decisions and ADRs

| decision | where |
|----------|-------|
| A default location exists at all, and it is the user's config directory rather than the folder being tidied | **ADR-0014**, superseding ADR-0010's "where the file comes from" half on the stakeholder's authorisation [src: EP-001/Q-005; src: WI-0004/Q-001] |
| `XDG_CONFIG_HOME`, then `HOME`, then no default location — read from the environment mapping, never from `expanduser` | **ADR-0014** §Decision point 1, with the rejected `expanduser` option and why |
| One path, no search chain | **ADR-0014** §Decision point 2 [src: WI-0004] |
| `--rules` wins by being *given*, so `--rules ""` is a path that cannot be opened and exits 2 rather than silently meaning "no rules" | **ADR-0014** §Decision point 3. This settles the gap `review-close` recorded against WI-0003 [src: tracker/items/WI-0003/item.md]; the item left it to this skill and no criterion depends on it [src: WI-0004] |
| Present-and-unusable ≠ absent, and presence is `lexists` | **ADR-0014** §Decision point 4 |
| The run names the rule file it used, on stderr, and says nothing when it used none | **ADR-0014** §Decision point 5, and AC4 |
| `XDG_CONFIG_HOME` used as given; the line's exact wording; the `lexists`-and-unsearchable-parent corner; where the test isolation lives | `## Assumptions` A1–A4, each with what reversing it costs |

## Scaffolding

`none`. Every file this plan touches already exists, and `commands.test` and `commands.lint` are
already real commands that run in this project [src: tracker/project.yaml; src: ADR-0004].

## Risks

- **Step 5 is the one that could be read as gaming AC2.** AC2 requires the existing suite to pass
  "with no existing test edited to accommodate this item", and step 5 edits `tests/support.py`. The
  edit adds environment isolation and changes no assertion; without it the suite's result depends on
  whether the person running it happens to have `~/.config/tidy/rules.ini`. If `verify` judges that
  this violates AC2, the fix is not to weaken AC2 — it is to put the isolation in a new base class
  that only the new tests use, and accept that the old tests remain environment-dependent. Naming
  the choice here so the argument happens in review rather than in silence.
- **`--rules ""` changes behaviour that something might rely on.** Today it is silently a no-rules
  run; after step 3 it is exit 2. No test asserts the current behaviour and no criterion of any item
  requires it [src: tracker/items/WI-0003/item.md], but it is a user-visible change made by this
  item and not asked for by the stakeholder. It is recorded in ADR-0014 rather than left to be
  discovered.
- **A rule file at the default path makes every run in the suite non-hermetic if step 5 is wrong.**
  The failure mode is silent and machine-dependent: green on CI, red on one developer's laptop, or
  the reverse. Step 6's `default_path` tests are pure and cannot catch it; the check is that
  `tests/support.py` sets `XDG_CONFIG_HOME` for *every* `FolderTestCase`, not only the new ones.
- **The stderr line lands in runs that then fail for another reason.** A valid rule file plus an
  unusable target folder now prints two stderr lines rather than one. No criterion forbids it and
  it is honest — the rules were read, then the folder was not usable — but WI-0003 AC8's "one line
  on stderr" phrasing is about rule-file rejection, and a reader could misapply it.

## Out of scope for this item

- A rule file in the folder being tidied, and any chain of locations. Refused by the stakeholder in
  their own words [src: WI-0004/Q-001].
- Any way to turn the default off for one run — no `--no-rules`, and `--rules ""` is not documented
  as one [src: WI-0004].
- An environment variable naming the rule *file*. `XDG_CONFIG_HOME` names a directory and is the
  standard way of finding one [src: WI-0004].
- Anything about what a rule file may contain: the format, the layering, and the two-band rule are
  ADR-0010's and are not reopened [src: ADR-0010; src: WI-0003/Q-001; src: WI-0003/Q-002].
- Which error wins when both the rule file and the target folder are unusable. The order is
  unchanged — the rule file is resolved first [src: tidy/cli.py] — and no criterion of this item
  turns on it [src: WI-0004].
- Subfolder recursion and undo, declined by name at sign-off [src: EP-001/Q-005].
