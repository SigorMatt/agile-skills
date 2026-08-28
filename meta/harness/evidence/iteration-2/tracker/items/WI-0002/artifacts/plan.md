# Plan — WI-0002 Route files by how old they are, as well as by type

## Problem

`tidy` already sorts the files sitting directly in a folder into type folders and previews every
move before making it [src: WI-0001]. This item adds the other half of the original ask: a file's
age chooses a band above its type folder, so a tidied folder's top level is `recent/` and `old/`
and the type folders sit inside them — `recent/images/holiday.jpg`, `old/documents/taxes-2019.pdf`
[src: WI-0002 AC1]. The stakeholder chose that shape so that the top level answers "what is still
live?" without opening anything [src: WI-0002/Q-001], and chose two bands split at a year
[src: WI-0002/Q-002]; `refine` pinned "a year" at 365 days as a reversible assumption
[src: WI-0002 AC4]. The constraints are unchanged: Python 3.9+, standard library only, one terminal
command [src: ADR-0001]; no file is ever overwritten [src: EP-001/Q-002]; nothing below the target
folder's top level is entered or moved [src: EP-001/Q-003]. User-supplied bands are WI-0003 and
must not be built here [src: WI-0002].

## Approach

The change is one input more in the one place that already decides destinations. `tidy/planner.py`
remains the only module that chooses where a file goes, so preview and apply still cannot disagree
[src: ADR-0002; src: tidy/planner.py], and `tidy/apply.py` and `tidy/cli.py` need no change at all:
`apply_plan` already creates `os.path.dirname(destination)` with `os.makedirs(..., exist_ok=True)`,
which makes `old/documents/` as readily as `documents/` [src: tidy/apply.py], and `render` prints
whatever destination string the action carries [src: tidy/cli.py].

The age rule is represented as an ordered table beside the extension table, with a lookup over it —
the decision, its two rejected alternatives, and its reversibility are ADR-0005. In short:
`DEFAULT_BANDS` and `band_for(age_seconds)` in `tidy/rules.py`, mirroring `DEFAULT_RULES` and
`folder_for`, so that WI-0003 can make both kinds of rule user-supplied with one mechanism
[src: ADR-0005; src: WI-0003].

### The interfaces this plan fixes

Contracts, not implementations. How each is written is the developer's call.

```python
# tidy/rules.py  — added
DEFAULT_BANDS: tuple[tuple[str, int | None], ...]   # (band, max_age_seconds); youngest first,
                                                    # last bound is None = no upper bound
def band_for(age_seconds: float) -> str             # first band whose bound is None or > age

# tidy/planner.py — build_plan's signature does not change
def build_plan(folder: str) -> list[Action]         # reads the clock once, internally
```

`Action` is unchanged. `destination` simply carries three components instead of two, which is why
no criterion needs a new output format: the band is the first component of the path WI-0001 AC3
already prints [src: WI-0002 AC1].

### The two behaviours that need care

1. **The name a folder needs is taken by something that is not a folder.** `build_plan` already
   handles this for the type folder — it emits a `leave` action rather than letting the apply fail,
   so that preview and apply agree about it [src: WI-0001/Q-002; src: tidy/planner.py]. The
   destination now has two folder components, so the check runs over both, and the `leave` line's
   reason names the component that is blocked [src: WI-0002 AC12].
2. **Unrecognised files are not aged.** The band is computed only for a file that has a type
   folder, so the `leave` path for "no rule for '.xyz'" is reached before any age is looked at, and
   no band folder is created for it [src: WI-0002 AC6].

## Steps

1. **`tidy/rules.py` — add the band table and its lookup.** Add `DEFAULT_BANDS` as described in
   ADR-0005, with the two bands `recent` (bound `365 * 24 * 3600`) and `old` (bound `None`), and
   `band_for(age_seconds)` returning the first band whose bound is `None` or strictly greater than
   `age_seconds`. Afterwards: `band_for(0) == "recent"`, `band_for(365 * 24 * 3600) == "old"`,
   `band_for(365 * 24 * 3600 - 60) == "recent"`. Keep the module's docstring honest — it currently
   says the table is documented in `README.md`, and now there are two tables.

2. **`tidy/planner.py` — read the clock once and route by band.** In `build_plan`, capture the
   reference instant once before the loop (one `time.time()` call for the whole run, per ADR-0005),
   and for each entry that has a type folder compute `age = now - entry.stat().st_mtime` and
   `band = band_for(age)`. The destination folder becomes `os.path.join(band, type_folder)`;
   everything downstream — the reserved-name set, `_free_destination`, the suffix rule — works on
   that path unchanged. Afterwards: a folder holding `holiday.jpg` modified today plans
   `recent/images/holiday.jpg`, and one holding `taxes.pdf` modified 400 days ago plans
   `old/documents/taxes.pdf`.

3. **`tidy/planner.py` — extend the not-a-folder check to both components.** Where the current code
   tests `folder/destination_folder` with `os.path.lexists(...) and not os.path.isdir(...)`, test
   each folder component of the destination in turn — the band, then the band-and-type path — and
   on the first that is taken by a non-folder emit a `leave` action whose reason names that
   component. Afterwards: with a regular file named `old` in the target folder, a 400-day-old
   `taxes.pdf` gets `leave  taxes.pdf   ['old' exists and is not a folder]`, in both modes, and
   nothing moves.

4. **`tests/support.py` — add one fixture helper.** A method that sets a file's modification time
   to a given age in days, via `os.utime`, and that can set the access time independently, since
   AC3 is decided by crossing the two. Afterwards: a test can write a file and age it in one line.

5. **`tests/test_rules.py` — the band lookup, without a folder.** Cases for both bands and for the
   three boundary points AC4 names: exactly 365 days, one minute under, one minute over. Also
   assert that `DEFAULT_BANDS` has exactly two entries and that their names are `recent` and `old`,
   which is the half of AC4 that says no third band exists.

6. **`tests/test_planner.py` — the destinations.** AC1 (three components, band first), AC2 (same
   type, two bands, two destinations), AC3 (mtime and atime crossed, so a tool reading `st_atime`
   fails the test), AC6 (a 400-day-old `notes.xyz` is left, with no band in its line and no `old/`
   created), AC7 (a collision inside `old/documents/` produces `old/documents/report (2).pdf`), and
   AC12 (the band name taken by a regular file).

7. **`tests/test_cli.py` — the end-to-end behaviours.** AC5 (capture PREVIEW's `(name, destination)`
   pairs with `Run.destinations()`, then APPLY on the unchanged folder and assert every file is at
   the path PREVIEW printed, `old/documents/` included), AC8 (`.hidden.jpg` aged 400 days appears
   in neither mode's output), AC9 (pre-existing `documents/`, `old/` and `recent/` each holding a
   file: unchanged afterwards, and no file inside them in either mode's output — use
   `self.listing()` for the before/after comparison), AC10 (`recent/documents/notes.txt` aged to
   400 days: no output line names it and it is still there after APPLY), AC11 (APPLY, APPLY, and a
   PREVIEW between them printing no move lines), and AC13 (read `README.md` and check it states
   the tree shape, both band names, last-modified as the field, and 365 days — parsed from the file
   rather than restated in the test, as `test_rules.py` already does for the extension table).

8. **`README.md` — document the bands (AC13).** Alongside the existing extension table: the shape
   of the tree, both band names, that age is the file's last-modified time, and the boundary as
   365 days. Update the example lines at the top of "What it does" so they show the band component,
   and the "It does not go into subfolders" bullet stays as it is — it is still true and it is what
   AC9 and AC10 rest on.

9. **`docs/architecture/overview.md` — v3, when the code lands.** Two statements go stale the
   moment step 2 is committed: the module table's `rules.py` row ("the default extension-to-folder
   table, and `folder_for(filename)`") and the bullet under "What is deliberately not here" that
   says there is no age handling. Bump the version, add the change-log row, and cite ADR-0005. This
   is D7's obligation, named here so `implement` does not have to rediscover which sentences this
   change invalidates.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — destination is `<band>/<type>/<name>` | 1, 2 | `tests/test_planner.py`: `holiday.jpg` modified now plans `recent/images/holiday.jpg`; the move line is checked in `tests/test_cli.py` against the exact string `move   holiday.jpg -> recent/images/holiday.jpg` |
| AC2 — same type, different bands, different destinations | 1, 2 | `tests/test_planner.py`: `a.pdf` (now) → `recent/documents/a.pdf`, `b.pdf` (400 days) → `old/documents/b.pdf` in one plan |
| AC3 — age is `st_mtime`, not another field | 2, 4 | `tests/test_planner.py`: two files with mtime and atime crossed by the step 4 helper; a planner reading `st_atime` places both the other way round and fails |
| AC4 — two bands, boundary 365 days, `>=` is old | 1, 5 | `tests/test_rules.py`: `band_for` at exactly 365 days → `old`, one minute under → `recent`, one minute over → `old`; plus `DEFAULT_BANDS` has exactly the two names |
| AC5 — PREVIEW and APPLY agree, folders created | 2, 7 | `tests/test_cli.py`: `Run.destinations()` from PREVIEW equals the set of paths found on disk after APPLY; `old/documents/` exists afterwards having not existed before |
| AC6 — an unrecognised file is not aged | 2, 6 | `tests/test_planner.py`: `notes.xyz` at 400 days gets a `leave` action whose reason is `no rule for '.xyz'`; `tests/test_cli.py`: after APPLY the file is at its original path and no `old/` exists |
| AC7 — never-overwrite inside the band path | 2, 6 | `tests/test_planner.py` and `tests/test_cli.py`: a pre-existing `old/documents/report.pdf` of different contents; the plan says `old/documents/report (2).pdf`, and the pre-existing file's sha256 is unchanged after APPLY |
| AC8 — hidden files still skipped whatever their age | 2, 7 | `tests/test_cli.py`: `.hidden.jpg` aged 400 days produces no line in either mode and is not moved |
| AC9 — existing subfolders untouched, including `old/` and `recent/` | 3, 7 | `tests/test_cli.py`: `self.listing()` over the three pre-existing folders is identical before and after APPLY, and no file inside them appears in either mode's output |
| AC10 — a file that ages after sorting is never re-filed | 7 | `tests/test_cli.py`: `recent/documents/notes.txt` aged to 400 days; no output line names `notes.txt` and it is at the same path after APPLY |
| AC11 — a second APPLY is a no-op | 7 | `tests/test_cli.py`: `self.listing()` after the second APPLY equals the one after the first, and the PREVIEW between them has no move lines |
| AC12 — band folder name taken by a regular file | 3, 6 | `tests/test_planner.py` and `tests/test_cli.py`: a regular file named `old` beside a 400-day-old `taxes.pdf`; a `leave` line whose reason names `old`, nothing moved, the regular file's sha256 unchanged, exit status 0 |
| AC13 — `README.md` states tree, bands, field and boundary | 8 | `tests/test_cli.py`: `README.md` is read and parsed for both band names, the `<band>/<type>/<name>` shape, "last modified", and `365`; the test fails if the documentation and `DEFAULT_BANDS` disagree |

Every criterion has a step and a demonstration; no step exists that no criterion maps to.

## Assumptions

Four are inherited from `refine`, which recorded them as assumptions the stakeholder did not
overrule rather than as their decisions [src: WI-0002]. This plan adopts all four and adds two of
its own. Reversal cost is stated for each, because that is what a later `plan` execution needs in
order to know whether it may revisit one.

1. **Age is `st_mtime`.** [src: WI-0002 AC3] To reverse: one expression in `build_plan` and the
   crossed-timestamp test. Cheap.
2. **"One year" is 365 days = 31 536 000 seconds.** [src: WI-0002 AC4] To reverse: one value in
   `DEFAULT_BANDS`, AC4's three test cases, and the number in `README.md`. Cheap.
3. **A file exactly on the boundary is `old`.** [src: WI-0002 AC4] To reverse: the comparison
   operator in `band_for`, and one test case. Cheap.
4. **The bands are documented in `README.md`.** [src: WI-0002 AC13] To reverse: move a section.
   Cheap.
5. **`now` is read once per run**, so all files in one run are measured against the same instant
   [src: ADR-0005]. To reverse: move one call. Cheap — but reversing it reintroduces the split
   boundary described in ADR-0005.
6. **A file whose modification time is in the future counts as `recent`.** This falls out of the
   ordered table — a negative age is below every bound — and no criterion constrains it. It is the
   only sane reading of "not touched in a year", so it is recorded here rather than escalated; a
   future-dated file is not an error the tool has any business reporting. To reverse: one guard in
   `band_for`. Cheap.

## Decisions and ADRs

| decision | where it is recorded | route |
|----------|---------------------|-------|
| The age rule's shape: an ordered table plus a lookup, not a constant and not a rule engine | **ADR-0005** (new) | decided here; this is the design question `refine` routed to `plan` [src: WI-0002] |
| `now` read once per `build_plan` call | ADR-0005 `## Decision` §3 | decided here |
| Half-open comparison, so the boundary belongs to the older band | ADR-0005 `## Decision` §1, implementing [src: WI-0002 AC4] | documented — the criterion already fixes it |
| Every destination still decided in `planner.py` alone | ADR-0002, unchanged | documented [src: ADR-0002] |
| `apply.py` and `cli.py` unchanged | this plan `## Approach` | documented — `os.makedirs` on the destination's dirname already handles a nested path [src: tidy/apply.py] |
| The four inherited assumptions | `## Assumptions` 1–4, and `item.md` `## Notes` | assumed, with reversal cost |
| A future modification time counts as `recent` | `## Assumptions` 6 | assumed, with reversal cost |
| No new ADR for the destination string's composition | — | it is one `os.path.join` under ADR-0002 and ADR-0005; an ADR for it would be padding |

Nothing was asked of the stakeholder. Nothing needed to be: the two decisions that had product
stake were asked in round 1 of refinement and are answered [src: WI-0002/Q-001;
src: WI-0002/Q-002], and every remaining choice is either fixed by a criterion, cited to an
existing document, or recorded above as a reversible assumption.

## Scaffolding

`none`. This plan creates no file outside `tracker/` and `docs/`. `tracker/project.yaml` already
carries working commands — `python3 -m unittest discover -s tests -t . -q` and
`python3 -m compileall -q tidy tests`, both run in this execution [src: ADR-0004] — and `tests/` is
an existing package with 37 passing tests, so nothing needs a marker file to be runnable.

## Risks

- **Clock skew and copied files.** Age is wall-clock arithmetic on a timestamp the filesystem
  reports, so a file restored from a backup or copied with a preserved mtime is aged by its
  original date, and one copied without preservation looks new. This is inherent in the
  stakeholder's own framing ("anything I haven't touched in a year") and is not a defect, but it is
  the first thing a confused user will hit. If it matters later it is a WI-0003-shaped
  conversation, not a fix here.
- **`entry.stat()` follows symlinks.** A symlink to an old file would be aged by the target's
  mtime, not the link's. The existing `entry.is_dir()` call has the same property
  [src: tidy/planner.py], so this plan keeps the behaviour consistent rather than introducing a
  second convention; no criterion covers symlinks, and WI-0001 did not either.
- **The mixed tree is real and visible.** A folder tidied by the shipped version and re-tidied
  after this item holds both `documents/` and `old/documents/`. It is accepted, not overlooked
  [src: WI-0002]; AC9 fixes the behaviour that produces it. The risk is that it reads as a bug in
  review — which is why the out-of-scope entry says so explicitly.
- **`README.md` and `DEFAULT_BANDS` drifting apart.** WI-0001 had the same exposure with the
  extension table and answered it with a test that parses the README [src: tidy/rules.py;
  src: WI-0001 AC5]. Step 7 does the same for the bands, so AC13 cannot pass while the
  documentation disagrees with the table.

## Out of scope for this item

- A third band, user-supplied bands, and a user-supplied boundary [src: WI-0002; src: WI-0003].
- Migrating a folder the previous version tidied: the top-level type folders stay where they are
  [src: WI-0002].
- Any change to `tidy/apply.py`, `tidy/cli.py` or the exit-code contract. If the developer finds a
  reason to touch either, that is a signal the layering was drawn in the wrong place and is worth a
  question rather than a workaround [src: docs/architecture/overview.md].
- Re-filing a file whose age crosses the boundary after it was sorted — specified as *not*
  happening [src: WI-0002 AC10], not left open.
