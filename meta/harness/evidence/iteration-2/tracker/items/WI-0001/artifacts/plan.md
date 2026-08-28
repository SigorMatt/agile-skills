# Plan — WI-0001 Sort a folder's files into subfolders by type, with a preview mode

## Problem

Someone points a command at a folder full of loose files and wants it sorted into subfolders by
kind of file — but wants to see the complete list of intended moves first, and to know that
nothing will be overwritten and that folders they organised themselves will not be touched. This
item builds the whole path end to end for **type only**: list the folder's top level, classify each
file by extension, resolve name collisions, print the resulting plan, and — only when explicitly
asked — carry it out. The constraints it must fit are fixed: Python 3.9+, standard library only,
one terminal command [src: ADR-0001]; nothing overwritten, ever [src: EP-001/Q-002]; nothing below
the top level touched [src: EP-001/Q-003]. Age routing (WI-0002) and user-supplied rules (WI-0003)
are separate items and must not be built here.

## Approach

Three layers, with every destination decided in exactly one of them [src: ADR-0002]:

- `tidy/rules.py` — the extension-to-folder table from AC5, and a lookup over it.
- `tidy/planner.py` — `build_plan(folder)` reads the folder's top level and returns an ordered
  list of `Action` records. It writes nothing.
- `tidy/apply.py` — `apply_plan(folder, actions)` executes an action list. It decides nothing.
- `tidy/cli.py` — argument parsing, rendering an action list as text, exit codes.

Preview is `build_plan` + render. Applying is `build_plan` + render + `apply_plan` over the same
list. That is what makes AC8 structural rather than a coincidence [src: ADR-0002].

### The interfaces this plan fixes

These are contracts, not implementations. How each is written is the developer's call.

```python
# tidy/rules.py
DEFAULT_RULES: dict[str, tuple[str, ...]]   # folder name -> extensions, lowercase, with the dot
def folder_for(filename: str) -> str | None # None when no rule matches

# tidy/planner.py
@dataclass(frozen=True)
class Action:
    kind: str           # "move" | "leave" | "skip"
    name: str           # the entry's name, as it appears in the folder
    destination: str | None   # e.g. "images/photo.jpg", relative to the folder; None unless move
    renamed_from: str | None  # the destination that was taken, when a suffix was applied
    reason: str | None        # why, for "leave" — e.g. "no rule for '.xyz'"

def build_plan(folder: str) -> list[Action]

# tidy/apply.py
def apply_plan(folder: str, actions: list[Action]) -> list[str]   # returns failure messages

# tidy/cli.py
def main(argv: list[str] | None = None) -> int                    # returns the exit status
```

### The output contract

Resolving the three questions `refine` routed here [src: WI-0001]:

- **The command** is `python3 -m tidy <folder>`. A package rather than a loose script, because
  `tests/` must import it and because `python3 -m tidy` is a real terminal command with no install
  step [src: ADR-0001].
- **The apply flag** is `--apply`. Preview is what happens without it.
- **stdout carries per-file lines only; stderr carries the banner and all errors.** This makes AC3,
  AC14 and AC15 checkable without ambiguity about extra lines, and makes the output pipeable.
  Line forms:

  ```
  move   photo.jpg -> images/photo.jpg
  move   report.pdf -> documents/report (2).pdf   [documents/report.pdf exists]
  leave  notes.xyz   [no rule for '.xyz']
  Nothing to do: no files to move in <folder>.
  ```

  A move line is exactly one whose first field is `move`, so "one line per file that would be
  moved" (AC3) is checkable by counting lines matching `^move `. `leave` lines are on stdout and
  are not move lines, which is the reading AC3 and AC6 require together. Skipped hidden files
  produce no line at all (AC13). The banner on stderr names the mode, e.g.
  `tidy: preview only — nothing will be moved. Re-run with --apply to move.`
- **The AC5 table is documented in `README.md`**, generated from nothing — written by hand and kept
  beside `rules.py`. `--help` points at it.
- **Exit codes:** 0 success (including nothing to do); 2 usage error — target missing or not a
  directory (AC14); 1 a move failed at apply time while others succeeded (ADR-0003).

## Steps

1. **`tidy/rules.py`** — write `DEFAULT_RULES` as a mapping from each of AC5's seven folder names
   to its tuple of extensions, exactly as AC5's table lists them, lowercase and dot-prefixed. Add
   `folder_for(filename)`: take the filename's final extension via `os.path.splitext`, lowercase
   it, return the folder whose tuple contains it, or `None`. Afterwards: `folder_for("PHOTO.JPG")`
   returns `"images"`, `folder_for("notes.xyz")` and `folder_for("README")` return `None`.

2. **`tidy/planner.py` — the `Action` record and the scan.** Add the frozen dataclass above, and
   `build_plan(folder)`. It lists `folder` with `os.scandir`, sorts entries by name for a stable
   output order, and for each entry produces exactly one `Action`, in this order of tests:
   - the name starts with `.` → **no action at all**; the entry is omitted from the list (AC13);
   - the entry is a directory → omitted from the list (AC11), and it is never descended into;
   - `folder_for(name)` is `None` → `Action(kind="leave", reason="no rule for '<ext>'")` (AC6);
   - `folder_for(name)` names a destination that already exists directly inside the target folder
     as something **other than a directory** → `Action(kind="leave", reason="'<folder>' exists and
     is not a folder")`. No criterion constrains this case; it is decided here rather than at apply
     time so that preview and apply cannot disagree about it [src: ADR-0002; src: WI-0001/Q-002].
     Demonstrated by `test_planner.test_destination_name_taken_by_a_file_yields_leave`.
   - otherwise → `Action(kind="move", destination="<folder>/<name>")`, subject to step 3.

   Afterwards: `build_plan` over a fixture folder returns one action per non-hidden top-level file
   and nothing for subfolders or dotfiles, and has created no directory and moved nothing (AC4).

3. **`tidy/planner.py` — collision resolution, inside `build_plan`.** Before emitting a `move`,
   check whether the destination path already exists on disk **or** has already been reserved by an
   earlier action in this same plan. If so, try ` (2)`, ` (3)`, … inserted before the extension —
   `report.pdf` becomes `report (2).pdf` — until one is free, then reserve it and record the
   originally intended path in `renamed_from`. Afterwards: with `report.pdf` in the folder and a
   different `report.pdf` already in `documents/`, the action's destination is
   `documents/report (2).pdf` and `renamed_from` is `documents/report.pdf` (AC9, AC10).

4. **`tidy/apply.py`** — `apply_plan(folder, actions)`. For each `move` action in order: create the
   destination's parent with `os.makedirs(..., exist_ok=True)`, then move by `os.link(src, dest)`
   followed by `os.unlink(src)` [src: ADR-0003]. `FileExistsError` from `os.link` means the folder
   changed underneath the run: leave the file alone, add a message to the returned list, and carry
   on with the remaining actions. Any other `OSError` from `os.link`: fall back to checking
   `os.path.exists(dest)` and then `shutil.move`, and add a message saying the fallback was used.
   `leave` actions do nothing. Afterwards: every destination in the list exists and holds the file,
   the sources are gone, and a pre-existing file at a colliding name is byte-for-byte untouched
   (AC7, AC9).

5. **`tidy/cli.py`** — `main(argv)`. `argparse` with one positional `folder` and one flag
   `--apply`, and help text that names both and states that without `--apply` nothing is moved
   (AC1). Validate the target: not a directory → message naming the path to stderr, nothing to
   stdout, return 2 (AC14). Otherwise call `build_plan` and print one line per action to stdout in
   the forms above — every `move` line and every `leave` line, unconditionally, because AC6's
   reporting is not conditional on anything else moving (AC3, AC6, AC10). Then, if the list holds
   no `move` action, print the "Nothing to do" line *after* those lines and return 0 (AC15); over
   an empty folder, or one holding only subfolders or only hidden files, there are no action lines
   at all, so that line is the whole of stdout. The banner goes to stderr whenever there is at
   least one `move` action. If `--apply` was given, call `apply_plan`, print any returned failure
   messages to stderr, and return 1 if there were any, else 0.
   [src: WI-0001/Q-001]

6. **`tidy/__main__.py`** — `from .cli import main` and `raise SystemExit(main())`. Afterwards:
   `python3 -m tidy --help` exits 0 and prints the usage from step 5 (AC1).

7. **`README.md`** — the AC5 table as a markdown table, how to run both modes, what happens on a
   collision, and the statement that subfolders and hidden files are left alone. This is the "file
   in the repository a user can read" AC5 requires, and it is what makes EP-001's fourth success
   measure checkable [src: EP-001].

8. **`tests/`** — one test module per layer: `tests/test_rules.py`, `tests/test_planner.py`,
   `tests/test_apply.py`, `tests/test_cli.py`. Build fixture folders with `tempfile.TemporaryDirectory`
   and set timestamps explicitly where a test needs them. The mapping table below names the test
   each criterion is demonstrated by. Afterwards:
   `python3 -m unittest discover -s tests -t . -q` exits 0 with every criterion covered
   [src: ADR-0004].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `--help` names the folder argument, the apply flag, and preview-by-default | 5, 6 | `test_cli.test_help_names_folder_apply_and_default` — run `main(["--help"])`, capture stdout, assert it contains `folder`, `--apply`, and the preview sentence; assert exit 0 |
| AC2 — preview is the default; bare invocation moves nothing | 5 | `test_cli.test_bare_invocation_moves_nothing` — snapshot the fixture tree, run `main([folder])`, assert the tree is identical and no subfolder was created |
| AC3 — one `move` line per moved file, naming file and destination; exit 0 | 5 | `test_cli.test_preview_prints_one_move_line_per_moved_file` — fixture with 3 recognised + 1 unrecognised file; assert exactly 3 stdout lines match `^move `, each containing its name and destination; exit 0 |
| AC4 — a preview changes nothing on disk | 2, 5 | `test_cli.test_preview_leaves_tree_byte_identical` — recursive (path, size, sha256) listing before and after; assert equal, and assert no destination folder exists |
| AC5 — the exact extension table, case-insensitive, documented | 1, 7 | `test_rules.test_every_extension_maps_to_its_folder` — parameterised over every row of the AC5 table, one fixture file per extension, asserting `folder_for` and the planned destination; plus `test_rules.test_extension_match_is_case_insensitive` for `PHOTO.JPG`; plus `test_rules.test_readme_documents_every_rule` reading `README.md` and asserting each extension appears under its folder |
| AC6 — unrecognised and extensionless files are left, reported, and distinguishable | 2, 5 | `test_planner.test_unrecognised_file_yields_leave_action` and `test_cli.test_leave_line_is_not_a_move_line` — assert the stdout line for `notes.xyz` and for `README` starts with `leave `, names the file, and that after `--apply` both are still at their original paths; plus `test_cli.test_leave_lines_are_printed_when_nothing_moves` — a folder holding only `notes.xyz` and `README`, asserting a `leave ` line for each, the nothing-to-do line after them, no `^move ` lines, and exit 0, which is the fixture AC6 and AC15 were read as disagreeing over [src: WI-0001/Q-001] |
| AC7 — apply lands every previewed destination and loses no file | 4, 5 | `test_cli.test_apply_lands_every_destination_and_loses_nothing` — multiset of (basename, size) recursively before and after, allowing only basenames the collision rule changed; assert each destination exists and holds the file |
| AC8 — preview and apply agree | 2, 4, 5 | `test_cli.test_apply_matches_the_preview_it_printed` — run preview, parse its (file, destination) pairs, run `--apply` on the unchanged fixture, parse its pairs, assert the two sets are equal |
| AC9 — no file is ever overwritten | 3, 4 | `test_apply.test_existing_file_is_untouched_on_collision` — `documents/report.pdf` with known contents, a different `report.pdf` at top level; after apply assert the original's sha256 is unchanged and the incoming file is at `documents/report (2).pdf`; plus `test_apply.test_link_refuses_an_existing_destination` asserting a fabricated colliding action is reported and not executed |
| AC10 — both modes report the collision and the suffixed name | 3, 5 | `test_cli.test_collision_line_names_the_suffixed_name_in_both_modes` — same fixture; assert the preview line and the apply line both contain `documents/report (2).pdf` |
| AC11 — subfolders untouched, not entered, not moved | 2, 5 | `test_cli.test_subfolder_and_contents_are_untouched` — fixture with `holiday/pic.jpg`; assert the recursive listing under `holiday/` is identical before and after `--apply`, and that neither `holiday` nor `pic.jpg` appears in either mode's output |
| AC12 — applying twice is idempotent; the second preview lists no moves | 2, 4, 5 | `test_cli.test_second_apply_is_a_no_op` — run `--apply` twice, assert the recursive listing after each is identical, then run preview and assert no `^move ` lines and exit 0 |
| AC13 — hidden files skipped entirely | 2 | `test_planner.test_hidden_files_produce_no_action` and `test_cli.test_hidden_files_appear_in_no_output` — `.bashrc` and `.hidden.jpg`; assert no action, no output line in either mode, and both still at their original paths after `--apply` |
| AC14 — missing path or a regular file: stderr, empty stdout, exit 2 | 5 | `test_cli.test_missing_path_and_non_directory_exit_2` — two cases; assert exit 2, stdout empty, stderr contains the offending path, and nothing on disk changed |
| AC15 — nothing to move: one line, no move lines, exit 0 | 5 | `test_cli.test_nothing_to_do_cases` — three fixtures (empty; only a subfolder; only hidden files) × both modes; assert exactly one stdout line, that it states there is nothing to do, no `^move ` lines, exit 0 |

Every criterion AC1–AC15 has a row. No step is unmapped: steps 1–6 each appear above, step 7 is
required by AC5's "stated in a file in the repository a user can read", and step 8 is what the
`demonstrated by` column is made of.

## Assumptions

1. **The collision suffix is ` (2)`, ` (3)`, … inserted before the extension** — `report (2).pdf`,
   not `report.pdf (2)`. The stakeholder left the form open [src: EP-001/Q-002] and `refine` left
   it to this plan [src: WI-0001]. It goes before the extension because the tool classifies by
   extension: `report.pdf (2)` would have the extension `.pdf (2)`, so a re-run could not recognise
   its own output. **To reverse:** one function in `tidy/planner.py`, plus the tests that assert the
   name. No data migration — nothing persists between runs. Cheap.
2. **`os.scandir` output is sorted by name before planning**, so output order is stable and tests
   can assert on it. Nothing requires it; it costs one call and makes every criterion easier to
   check. **To reverse:** delete the sort. Cheap.
3. **A destination reserved earlier in the same plan counts as taken** (step 3), even though two
   files in one flat folder cannot share a name today, so it cannot yet trigger. It is there because
   WI-0003 lets a user write rules that could map two different names to one destination. **To
   reverse:** delete the reservation set. Cheap — but reversing it would put the hole back.
4. **`README.md` is where the rule table is written down.** AC5 says "a file in the repository a
   user can read" and does not name one. **To reverse:** move the table and update the `--help`
   pointer. Cheap.
5. **Exit status 1 is reserved for a partial apply failure**, alongside AC14's 2 for a usage error.
   Nothing in the criteria requires a distinct code for it; without one, a run in which three files
   moved and one did not would exit 0. **To reverse:** return 0 instead. Cheap, and it changes no
   criterion.
6. **A destination folder name already taken by a non-directory at the top level demotes that
   file to `leave`** — see step 2. `refine` left this unconstrained and routed the decision to this
   plan; the plan's first version did not take it, and `implement` filed WI-0001/Q-002 rather than
   guessing. It is decided at plan time rather than caught at apply time because ADR-0002 makes
   preview and apply agree by construction, and handling it in `apply_plan` would have made AC8
   true only with an exception. **To reverse:** delete one branch in `build_plan` and decide
   instead how `apply_plan` should report the `FileExistsError` that `os.makedirs` would then
   raise. Cheap. [src: ADR-0002; src: WI-0001/Q-002]

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| Python 3.9+, one CLI entry point, standard library only | ADR-0001 | already documented — read, not re-decided |
| Planning and applying are separate layers; destinations decided once | ADR-0002 (new) | decided |
| Moves use `os.link` + `os.unlink`, so the kernel enforces never-overwrite | ADR-0003 (new) | decided |
| `commands.test` and `commands.lint`; no style linter | ADR-0004 (new) | decided |
| `python3 -m tidy`, `--apply`, stdout/stderr split, the line forms | this plan, `## Approach` | routed here by `refine`; decided |
| The collision suffix form; sorted scan; reservation set; README; exit 1 | `## Assumptions` 1–5 | assumed, each with its reversal cost |
| An AC5 destination name already taken by a non-directory; the output rule when nothing moves but something is left alone | `## Assumptions` 6 and step 5 | decided by `answer-questions` for WI-0001/Q-001 and Q-002 |
| Preview is the default; the AC5 table; unrecognised files left alone; hidden files skipped; exit 2 | `WI-0001/item.md` `## Notes`, `artifacts/refinement-qa.md` | already decided by `refine` under the stakeholder's standing deferral — inherited, not re-opened |

Nothing here contradicts an existing ADR. ADR-0001 is the only one that predates this execution and
this plan sits inside it: no third-party package appears anywhere above.

## Scaffolding

- `tidy/__init__.py` — empty. Created so `python3 -m compileall -q tidy tests` has a package to
  compile; the lint command cannot execute against a directory that does not exist.
- `tests/__init__.py` — empty. Created so `python3 -m unittest discover -s tests -t . -q` has a
  discoverable package.

Both are empty files containing no behaviour. Nothing else outside `tracker/` and `docs/` was
created by this execution: no module, no stub, no function body.

## Risks

- **The action list is held in memory before anything moves** [src: ADR-0002]. A folder with
  millions of entries would need a streaming design. The vision describes a downloads folder or a
  desktop [src: docs/product/vision.md], and no criterion mentions scale, so this is accepted rather
  than designed around. If it turns out to matter it is a new item, not a change to this one.
- **The plan is computed from the folder as it is at that instant.** If the folder changes between
  a preview and an apply, the apply's own plan will differ from what the user read. ADR-0003's
  `FileExistsError` path is what stops that becoming data loss, but the user's mental model would
  still be wrong. AC8 only requires agreement over an unchanged folder, so this is out of scope and
  is recorded here so nobody reads AC8 as a stronger promise than it is.
- **`os.link` is not available on every filesystem** — some network mounts and some Windows
  configurations refuse it. Step 4's fallback covers it, but the fallback is the weaker guarantee
  [src: ADR-0003], and no test in the mapping table exercises it, because provoking it needs a
  filesystem the test suite cannot create. This is the one place where a criterion (AC9) rests on
  code that automated tests do not reach, and `verify` should be told so rather than discovering it.
- **Five assumptions are load-bearing and none was confirmed by the stakeholder** — they were
  decided by `refine` under a standing deferral [src: EP-001/Q-001] and are listed in the item's
  `## Notes`. The one with the most product weight is that unrecognised files are left rather than
  swept into a catch-all: it means a correct run over a folder of unusual extensions can move
  nothing at all, which could read as the tool being broken.

## Out of scope for this item

- Age-based routing, in any form. `planner.py` must not grow a timestamp branch here; that is
  WI-0002, and the overview records where it will land [src: docs/architecture/overview.md].
- Loading rules from a file, and any argument for doing so. That is WI-0003.
- Recursion, undo, deletion, content sniffing, watching a folder — all excluded by the epic
  [src: EP-001].
- Making the never-overwrite behaviour configurable [src: EP-001/Q-002].
- Anything the mapping table's `demonstrated by` column does not need. If a step's output is not
  demonstrating a criterion, it should not be written.
