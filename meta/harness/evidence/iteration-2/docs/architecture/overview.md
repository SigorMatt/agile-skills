---
title: Architecture overview — tidy
version: 11
status: current
updated: 2026-08-28T15:41:00Z
updated-by: review-close
updated-for: WI-0004
---

# Architecture overview — tidy

## The shape of the system

`tidy` is a single Python package run as a command: `python3 -m tidy <folder>`. There is no
server, no daemon, no state on disk between runs, and no dependency outside the Python standard
library [src: ADR-0001].

It is built as three layers, and the boundary between the first two is the one architectural
commitment that matters:

```
  tidy/cli.py        argument parsing, rendering lines, exit codes
        |
        v
  tidy/planner.py    build_plan(folder) -> list[Action]      (reads; writes nothing)
        |    ^
        |    |
        |  tidy/rules.py   two tables and a lookup over each: extension -> type
        |                  folder, and age -> band
        v
  tidy/apply.py      apply_plan(folder, actions)             (writes; decides nothing)
```

**Every destination is decided in `planner.py` and nowhere else** [src: ADR-0002;
src: tidy/planner.py]. `apply.py` executes an action list it is handed. `cli.py` turns an action
list into text. Preview is "plan and render"; applying is "plan, render, and execute". The two
modes therefore cannot disagree about where a file goes, which is what makes the preview
trustworthy — and the preview is the product's central promise rather than a flag on the side of
it [src: docs/product/vision.md].

The second commitment is about how a file is actually moved. `apply.py` uses `os.link` followed by
`os.unlink`, because `os.link` fails when the destination exists, so the never-overwrite guarantee
is enforced by the kernel rather than by a check a future call site has to remember
[src: ADR-0003; src: EP-001/Q-002].

Read that as the *primary* path rather than the only one. Where a filesystem refuses hard links —
some network mounts, exFAT and FAT32 — `apply.py` falls back to `_move_without_a_link`, which
checks `os.path.lexists(destination)` and then calls `shutil.move`; the promise still holds there,
but it holds by a check-then-act with a race window rather than by the kernel
[src: ADR-0003; src: tidy/apply.py]. No test reached that path until BUG-0002, which is what let
a defect survive in it: a run using the fallback exited 1 even when every file had moved. It is
reached now — `tests/test_apply.py` and `tests/test_cli.py` each enter it by patching
`tidy.apply.os.link` to raise the `OSError` such a filesystem raises, which is the only way in
without a volume of that kind to hand [src: tests/test_apply.py; src: tests/test_cli.py;
src: BUG-0002].

ADR-0007 settles what the two routes report, because the exit status was the place the difference
between them was lost. `apply_plan` returns an `Outcome` — a `kind` and a `message` — for each
action that did not complete by the primary path, tagged `"failed"` when the file is not where the
plan said it would be and `"fell-back"` when it got there by ADR-0003's weaker route; only a
`"failed"` outcome makes the process exit non-zero, and the stderr wording of both is unchanged.
BUG-0002 carried that change into the code, together with the first regression tests that reach
the fallback branch at all [src: ADR-0007; src: BUG-0002 AC4].

There is a third commitment, and it is about failure rather than about moving files: **the system
has two error boundaries, at different levels, and they answer different questions.** A failure to
list *the target folder* belongs to `cli.py` — one line on stderr, an empty stdout, exit 2 — because
at that point there is no run to continue [src: ADR-0006; src: tidy/cli.py]. A failure to
interrogate *one entry inside it* belongs to `planner.py`, which turns it into the `leave` action
that entry gets and carries on with the rest of the folder [src: ADR-0009; src: BUG-0004]. Before
BUG-0004 there was only the first boundary, so one dangling symlink was reported as a folder that
could not be read, and no file in that folder was tidied [src: BUG-0004]. The rule that separates
them is worth stating as a rule: an event that ends the run is the CLI's, and an event that is
merely one entry's fate is data the planner returns.

## Modules

| module | responsibility | may write to disk |
|--------|----------------|-------------------|
| `tidy/__main__.py` | entry point; calls `cli.main()` and exits with its status | no |
| `tidy/cli.py` | `argparse` setup, rendering an action list as lines, exit codes | no |
| `tidy/rules.py` | the two default tables, `DEFAULT_RULES` and `DEFAULT_BANDS`; the `Ruleset` value that carries a run's tables and their two lookups; `BUILT_IN`; and `merge`, the layering | no |
| `tidy/ruleset_file.py` | `load(path)`: read one INI rule file, validate it, and return a `Ruleset` merged over `BUILT_IN`, or raise `RuleFileError`. Also `default_path(environ)` and `resolve(argument, environ)`, which decide *which* file a run reads — the one `--rules` names, or the one in the user's config directory, or none [src: ADR-0014] | no |
| `tidy/planner.py` | `build_plan(folder, ruleset=None)`: list the folder, classify by the ruleset, resolve collisions | no |
| `tidy/apply.py` | `apply_plan(folder, actions)`: perform the moves | yes |

## What is deliberately not here

- **No rule file inside the folder being tidied.** Rule loading landed with WI-0003 as ADR-0010
  forecast: one INI file, read by `tidy/ruleset_file.py`, producing the same `Ruleset` the planner
  takes from the built-in tables when no rules are given [src: ADR-0010; src: ADR-0011;
  src: tidy/ruleset_file.py]. ADR-0010 also refused it a *default* location, and WI-0004 reverses
  that half on the stakeholder's authorisation: a run with no `--rules` reads
  `$XDG_CONFIG_HOME/tidy/rules.ini`, or `$HOME/.config/tidy/rules.ini`, and names on stderr
  whichever rule file it used [src: ADR-0014; src: WI-0004]. What stays deliberately absent is the
  thing ADR-0010 was actually worried about, and the stakeholder refused it in their own words: a
  rule file sitting in the folder you were handed is not a rule source, and neither is a chain of
  places to look [src: WI-0004/Q-001].
- No rule that can weaken the tool's promises. A rule file changes where files go and nothing
  else: it cannot make the tool overwrite, recurse, pick up hidden files, or sweep unmatched files
  into a catch-all folder. Those are invariants the stakeholder settled rather than things a user
  configures [src: EP-001/Q-002; src: EP-001/Q-003; src: WI-0003].
- No way to *remove* a built-in mapping, and no band count other than two. Both are consequences
  of the stakeholder's own answers — layering with their entries winning, and two bands — and both
  are recorded as known gaps on WI-0003's out-of-scope list rather than as defects
  [src: WI-0003/Q-001; src: WI-0003/Q-002].
- No use of a file's age beyond choosing its destination. Age routing landed with WI-0002 and it
  does exactly one thing: `build_plan` reads the clock once, ages each recognised file by
  `now - st_mtime`, and puts the band above the type folder, so a destination is
  `<band>/<type>/<name>` [src: ADR-0005; src: WI-0002 AC1]. Nothing deletes, archives or reports
  on old files [src: EP-001].
- No band the user did not ask for. The two bands and the 365-day boundary are the *default*
  table now, not a constant one: `[bands]` in a rule file replaces both names and the one bound
  [src: tidy/ruleset_file.py]. ADR-0005's prediction held exactly — the table stays two entries
  long, and one `merge` replaces either kind of rule through the same value [src: ADR-0005;
  src: ADR-0011]. The format has three fixed keys, so a third band is not something the loader
  rejects but something the file cannot say [src: ADR-0010; src: WI-0003/Q-002].
- No recursion, no undo log, no content sniffing, and no daemon. All four are on the epic's
  out-of-scope list [src: EP-001].

## What the items did to this shape

WI-0004 (a default location for the rule file) is delivered, and it held the forecast this section
made before it was built. `ruleset_file.py` gained the two functions that decide *which* file a run
reads — `default_path(environ)` and `resolve(argument, environ)` — and `cli.py` gained one stderr
line and lost both places its help text said there is no default location
[src: tidy/ruleset_file.py; src: tidy/cli.py]. `planner.py`, `rules.py` and `apply.py` were not
touched at all: `git diff` over the item's branch reaches only those two modules, so a `Ruleset` is
still a value passed into `build_plan` and where it came from is not something the planner can tell
[src: ADR-0011; src: tracker/items/WI-0004/artifacts/verify-report.md].

WI-0002 (routing by age) is delivered, and it held the prediction this section made: destination
selection lives entirely in `planner.py` and `rules.py`, so `apply.py` and `cli.py` were not
touched at all. `apply_plan` already created the destination's parent with `os.makedirs`, which
makes a two-component path as readily as a one-component one [src: tidy/apply.py].

WI-0003 (user-supplied rules) is delivered, and it changed where the tables in `rules.py` come
from — both of them [src: WI-0003; src: tidy/ruleset_file.py]. The two ADRs below were written
before any of that code existed; both held, and what follows is now a description rather than a
forecast [src: ADR-0010; src: ADR-0011].

**ADR-0010: rules arrive as one INI file. Its "no default location" half is superseded by
ADR-0014** — a run with no `--rules` now reads `$XDG_CONFIG_HOME/tidy/rules.ini`, or
`$HOME/.config/tidy/rules.ini`, and says on stderr which rule file it used; nothing in the folder
being tidied is ever a rule source [src: ADR-0014; src: WI-0004/Q-001]. The **format** half of
ADR-0010 is unchanged and is what follows. Two optional sections, `[types]` and `[bands]`; the band section has three fixed keys,
so a third band is not something the format can express rather than something the loader rejects
[src: ADR-0010; src: WI-0003/Q-002]. A rule file that will not load is reported at the CLI
boundary and exits 2, which is ADR-0006's rule applied unchanged: it ends the run before there is
a run [src: ADR-0006]. The loader is read *before* the target folder is examined, so a mistyped
`--rules` path is reported even when the folder is unusable too [src: tidy/cli.py].

**ADR-0011: the loaded rules become a `Ruleset` value passed into `build_plan`**, rather than
module state rebound at load time. `folder_for` and `band_for` become its methods, `BUILT_IN` is
the one built from the constants, and the layering the stakeholder chose — their entries winning,
an omitted section keeping its built-in values — is a dict update inside one `merge` function
[src: ADR-0011; src: WI-0003/Q-001]. The prediction this section made for WI-0002 holds again:
`apply.py` is untouched and the three layers do not move.

One thing the code decided that neither ADR did: a type folder named after a band is used
verbatim, so a rule sending `.pdf` to `old` puts an old PDF at `old/old/report.pdf` rather than
raising. `refine` left it deliberately unconstrained and `plan` recorded it as assumption A1;
nothing can be overwritten either way and the preview shows the real destination before anything
moves, so the cost of being wrong about it is a folder name, not a file
[src: tracker/items/WI-0003/artifacts/plan.md; src: README.md].

One trap is worth naming here because no gate catches it. ADR-0008 states its checkable condition
as a grep: `tidy/cli.py` imports nothing from `tidy/rules.py` [src: ADR-0008]. Passing `BUILT_IN`
from `cli.py` as a default would break that quietly, with every test still green, so
`build_plan`'s parameter defaults to `None` and resolves it internally [src: ADR-0011].

One thing it will have to touch is the command's own description of itself. `cli.py` holds the
`--help` text as prose and imports nothing from `rules.py` [src: tidy/cli.py], so the text went
stale when WI-0002 changed where files go, and every gate stayed green [src: BUG-0003].
ADR-0008 decides to keep it as prose and to put the connection in the test suite instead: a band
name that `DEFAULT_BANDS` declares and the help output omits should be a test failure
[src: ADR-0008]. BUG-0003 carried that decision into the code, and WI-0003 left the guard green
because it did not change `DEFAULT_BANDS` — it made the tables replaceable rather than different
[src: tests/test_cli.py].

ADR-0008's condition needs reading with one word of care now. It is stated as a grep over
`tidy/cli.py`'s imports for `rules`, and `cli.py` does import `.ruleset_file`, whose name begins
with those five letters. What ADR-0008 decided is that `cli.py` imports no rule *table*, and that
still holds: the anchored form `grep -nE "^(from|import).*\brules\b" tidy/cli.py` finds nothing
[src: ADR-0008; src: tidy/cli.py].

One consequence of the band being the *top* component is worth stating here, because it is
structural rather than incidental: a folder tidied by the pre-band version keeps its type folders
at the top level, and a later run adds band folders beside them rather than migrating them. That
is the existing-subfolders rule doing what it was asked to [src: EP-001/Q-003], and it is recorded
as accepted rather than overlooked [src: WI-0002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 11 | 2026-08-28T15:41:00Z | review-close | WI-0004 | WI-0004 is delivered, so the section forecasting it is now a description: the prediction that only `ruleset_file.py` and `cli.py` would change held, and the diff is the evidence [src: tidy/ruleset_file.py; src: tidy/cli.py] |
| 10 | 2026-08-28T15:15:08Z | plan | WI-0004 | `ruleset_file.py` gains `default_path` and `resolve`: which rule file a run reads is now a decision with a home, and the config-directory default replaces "no default location" [src: ADR-0014] |
| 9 | 2026-08-27T22:05:00Z | implement | WI-0003 | User-supplied rules landed. Added `tidy/ruleset_file.py` to the module table and restated `rules.py` and `planner.py` around `Ruleset`, `BUILT_IN` and `merge`. Replaced the two "deliberately not here" entries that said rule loading and band configuration do not exist, and the WI-0003 forecast, with what was built. Recorded assumption A1's `old/old/report.pdf` and the one word of care ADR-0008's grep now needs |
| 8 | 2026-08-27T21:39:47Z | plan | WI-0003 | Recorded ADR-0010 and ADR-0011 in the section forecasting WI-0003: rules arrive as one INI file named with `--rules`, and become a `Ruleset` value the planner takes as a parameter. Named the import that would break ADR-0008's condition silently |
| 7 | 2026-08-27T20:46:03Z | plan | BUG-0004 | Recorded ADR-0009 as the system's second error boundary: the target folder failing is `cli.py`'s and exits 2, one entry failing is `planner.py`'s and becomes a `leave` action |
| 6 | 2026-08-27T20:20:23Z | plan | BUG-0003 | Recorded ADR-0008 in the section forecasting WI-0003: the `--help` text stays prose in `cli.py`, and a test that reads `DEFAULT_BANDS` is what will catch it going stale again |
| 5 | 2026-08-27T20:11:11Z | answer-questions | BUG-0002 | Answering BUG-0002/Q-001: the fallback paragraph said the path was unreachable from the test suite and that a fallback run exits 1. BUG-0002's code and its four tests make both false, and the next paragraph already said so. Restated as what is now true, with the defect kept as history |
| 4 | 2026-08-27T19:46:29Z | plan | BUG-0002 | Recorded ADR-0007: the fallback and a genuine failure are separate outcomes, and only a failure exits non-zero. The paragraph about the fallback said the defect was live and said nothing about what replaces it |
| 3 | 2026-08-27T18:15:50Z | implement | WI-0002 | Age routing landed: rules.py now holds two tables, a destination is `<band>/<type>/<name>`, and the "no age handling" entry was false the moment the code was committed. Cites ADR-0005 |
| 2 | 2026-08-27T16:40:00Z | review-close | WI-0001 | D12 audit at close: the os.link paragraph read as though never-overwrite were always kernel-enforced. Recorded ADR-0003's fallback, what it costs, and BUG-0002 |
| 1 | 2026-08-27T16:03:05Z | plan | WI-0001 | First version: the three-layer shape, the module table, and the two commitments (plan/apply separation, os.link) |
