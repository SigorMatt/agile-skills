# Plan — BUG-0002 A fully successful apply exits 1 on a filesystem that refuses hard links

## Problem

On a filesystem that refuses hard links, `tidy <folder> --apply` moves every file correctly and
then exits 1. `apply.py` has two routes to a completed move — `os.link` + `os.unlink`, and
ADR-0003's `shutil.move` fallback — and ADR-0003 treats the second as a success with a weaker
guarantee rather than as a failure [src: ADR-0003]. The code cannot say that: `apply_plan` returns
one flat `list[str]`, the fallback's note goes into it beside genuine failures, and `cli.main` ends
with `return 1 if failures else 0` [src: tidy/apply.py; src: tidy/cli.py]. Anything scripting the
tool on exFAT, FAT32, or an SMB/NFS/FUSE mount that refuses `os.link` therefore reads a completely
successful run as a failure. The change is for whoever runs `tidy ... --apply && something-else` on
such a filesystem, and it is constrained by BUG-0002 AC2: the stderr note that the fallback was used
must survive word for word, so only the exit status may change [src: BUG-0002 AC2].

## Approach

ADR-0007 is the decision, and it is the only design choice this item forces. `apply.py` — the one
layer that knows which route a move took — gains a two-field record and returns those instead of
bare strings:

```
@dataclass(frozen=True)
class Outcome:
    kind: str        # "failed" | "fell-back"
    message: str

def apply_plan(folder, actions) -> list[Outcome]
```

`"failed"` means the file is not where the plan said it would be (or, in the `os.unlink` case,
it got there and the original could not be removed). `"fell-back"` means it got there by ADR-0003's
weaker route and the run is saying so. An action that completed by the primary path contributes
nothing, so an empty list keeps the meaning it has today.

`cli.main` prints every outcome's `message` in list order, byte for byte as now, and exits non-zero
only if some outcome is `"failed"`. Nothing about the layering moves: `planner.py` is untouched,
`apply.py` still decides no destination, and the exit code is still chosen in `cli.py`
[src: ADR-0002].

The rejected alternatives, and why, are in ADR-0007 `## Options considered`. The one worth
repeating here is the two-list return that BUG-0002 `## Notes` suggested [src: BUG-0002]: it
regroups stderr away from action order, which a mixed run makes visible
[src: run: python3 nolink.py /tmp/bug2repro/mixed → EXIT: 1, the `doc.pdf` failure line printed
before the `photo.jpg` fallback line], and AC2 asks that nothing but the exit status change.

## Steps

1. **`tidy/apply.py` — add the record.** Import `dataclass` and define `Outcome` as a frozen
   dataclass with `kind: str` and `message: str`, above `apply_plan`. Extend the module docstring to
   cite ADR-0007 beside ADR-0003, naming the two `kind` values and what each asserts about where the
   file is. Afterwards `from tidy.apply import Outcome` works and nothing else has changed.

2. **`tidy/apply.py` — return outcomes from `apply_plan`.** Rename the local `failures` to
   `outcomes`. Wrap each of the three existing `append` calls in `Outcome("failed", ...)`, leaving
   every message string exactly as it is: the `os.makedirs` failure, the `FileExistsError` "appeared
   while tidying" message, and the `os.unlink` "was copied to ... but the original could not be
   removed" message. The `except OSError` branch appends whatever `_move_without_a_link` returns.
   Update the docstring: it returns an outcome per action that did not complete by the primary path,
   in action order, and still lets nothing raise out of it. Afterwards `apply_plan` returns
   `list[Outcome]` and an all-clean run still returns `[]`.

3. **`tidy/apply.py` — tag the fallback.** `_move_without_a_link` returns `Outcome("failed", ...)`
   for its two failure returns (the destination already exists; `shutil.move` raised) and
   `Outcome("fell-back", ...)` for its success return. The success message text is unchanged —
   `"%s was moved to %s without a hard link, because this filesystem refused one (%s)"`. Afterwards
   the only route that produces a `"fell-back"` outcome is a completed `shutil.move`.

4. **`tidy/cli.py` — print messages and decide the exit status.** In `main`, replace the last three
   lines with: `outcomes = apply_plan(folder, actions)`; a loop writing
   `"tidy: %s\n" % outcome.message` to stderr in list order; and
   `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`. Add a one-line
   comment citing ADR-0007 for why the `any` is over `kind` and not over the list's emptiness.
   Afterwards a run whose outcomes are all `"fell-back"` exits 0 with its stderr unchanged, and a
   run with any `"failed"` outcome exits 1.

5. **`tests/test_apply.py` — update the two assertions that read the returned entries.** In
   `NeverOverwriteTests.test_link_refuses_an_existing_destination`, keep the length assertion and
   change `assertIn("report.pdf", failures[0])` to read `failures[0].message`, adding
   `assertEqual(failures[0].kind, "failed")`. In
   `test_one_failure_does_not_stop_the_remaining_actions`, add the same `kind` assertion for the one
   entry. The two `assertEqual(apply_plan(...), [])` assertions need no change and must not be
   changed — that they still hold is the evidence that the empty list kept its meaning.

6. **`tests/test_apply.py` — a new `HardLinkFallbackTests(FolderTestCase)` class,** with
   `unittest.mock.patch("tidy.apply.os.link", side_effect=OSError(18, "Invalid cross-device link"))`
   as a context manager in each test, so the patch is scoped and restored:
   - *every fallback move lands and is not a failure* — write `photo.jpg` and `doc.pdf`, apply
     `build_plan`'s actions under the patch, assert every returned outcome has `kind ==
     "fell-back"`, that each message contains `"without a hard link"` and `"Invalid cross-device
     link"`, that both destinations hold the original contents, and that neither source name
     remains. (BUG-0002 AC1, AC2 at the unit level.)
   - *a fallback that cannot land is a failure* — under the same patch, hand `apply_plan` a
     fabricated colliding `Action` the way `test_link_refuses_an_existing_destination` does, with the
     destination file already written, and assert the single outcome has `kind == "failed"` and that
     the existing file is byte-identical afterwards. (BUG-0002 AC3.)

7. **`tests/test_cli.py` — a new `FallbackExitStatusTests(FolderTestCase)` class,** using
   `tests.cli_support.run` and the same patch, and add BUG-0002 to the module docstring's list of
   what this file covers:
   - *a run that falls back for every file exits 0* — `photo.jpg` and `doc.pdf` at the top level,
     `run(self.folder, "--apply")` under the patch; assert `status == 0`, that both files are at the
     destinations the move lines named, and that stderr contains, for each file, the exact line
     `"tidy: %s was moved to %s without a hard link, because this filesystem refused one ([Errno 18]
     Invalid cross-device link)"`. This is the reproduction in BUG-0002 `## Steps to reproduce`,
     turned into a test. (BUG-0002 AC1, AC2.)
   - *a genuine failure alongside a fallback still exits 1* — create `recent/documents/` before the
     run and `chmod` it to `0o500`, registering `addCleanup(os.chmod, path, 0o700)` **before** the
     `chmod`, exactly as `BadTargetTests.test_an_unreadable_folder_exits_2_without_a_traceback`
     does. Guard with a `skipTest` if a write into that directory succeeds anyway — running as root,
     or a filesystem not enforcing the mode — mirroring that test's guard. Under the patch,
     `doc.pdf`'s `shutil.move` then fails with `EACCES` while `photo.jpg` falls back cleanly. Assert
     `status == 1`, that `doc.pdf` is still at the top level and `photo.jpg` is at
     `recent/images/photo.jpg`, that stderr carries both messages, and that the `doc.pdf` failure
     line appears **before** the `photo.jpg` fallback line, which is the action ordering ADR-0007
     kept. (BUG-0002 AC3.)

8. **Show the tests fail against the unfixed code.** Before reporting, revert steps 1-4 in a
   scratch copy — or stash them — and confirm that the two tests from step 7 and the first from
   step 6 fail, then restore. Record the two outputs in `impl-report.md`. Two hazards, both of which
   have produced a false pass in this project before: run with `PYTHONDONTWRITEBYTECODE=1` and
   remove `__pycache__` first, because a same-length edit can leave a stale `.pyc` serving the old
   code; and read the file back to confirm the revert is actually present before running.

9. **Run the gates and report.** `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q tidy tests`, both from the repository root, then
   `scripts/lint-claims --changed-since main` and `scripts/validate-workspace`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — an APPLY run in which every move landed exits 0, by either route | 1, 2, 3, 4 | `test_cli.FallbackExitStatusTests` *a run that falls back for every file exits 0*: `status == 0` with both files found at the destinations the move lines named. Plus the item's own reproduction re-run by hand: `python3 nolink.py /tmp/...` prints `EXIT: 0` |
| AC2 — the fallback is still reported, unchanged | 3, 4 | The same test asserts the full stderr line for each file, character for character including `[Errno 18] Invalid cross-device link`; and `test_apply.HardLinkFallbackTests` asserts the message content at the unit level. Step 3 changes no message string, which `git diff` shows |
| AC3 — a run in which a move genuinely did not land still exits non-zero | 4, 6, 7 | `test_cli.FallbackExitStatusTests` *a genuine failure alongside a fallback still exits 1*: `status == 1`, `doc.pdf` still at the top level while `photo.jpg` landed. At the unit level, `test_apply.HardLinkFallbackTests` *a fallback that cannot land is a failure* and the upgraded `test_link_refuses_an_existing_destination`, which assert `kind == "failed"` on the `FileExistsError` and destination-exists paths |
| AC4 — a regression test in `tests/` patches `os.link` to raise a non-`FileExistsError` `OSError`, asserts AC1-AC3, and fails when the fix is reverted | 6, 7, 8 | The two new classes, both patching `tidy.apply.os.link` with `OSError(18)`. Step 8 records the failing output against the reverted code in `impl-report.md`, which is what distinguishes a regression test from a test that happens to pass |

## Assumptions

- **`unittest.mock` is in scope.** ADR-0001 confines the project to the standard library, and
  `unittest.mock` is part of it [src: ADR-0001]. Reversing costs one edit in each new test class: a
  `try` / `finally` that swaps `apply.os.link` by hand. No production code depends on it.
- **The `kind` vocabulary is two plain strings, `"failed"` and `"fell-back"`,** compared literally,
  matching how `Action.kind` is used [src: tidy/planner.py]. Reversing to an enum or to module
  constants is one module and its tests, with no on-disk or interface consequence.
- **The `os.unlink` case stays `"failed"`.** When the link succeeded and the original could not be
  removed, the file is at its destination *and* still at its source: a duplicate, not a completed
  move, and it exits non-zero today. Nothing in BUG-0002 asks to change that, and AC3 asks that real
  failures keep exiting non-zero. Reversing is one `Outcome` kind on one line.
- **`README.md` is not touched.** Its exit-status paragraph already states the contract this item
  implements — 0 on success, 1 when some file could not be moved while others were — so the code is
  being brought to the document rather than the reverse [src: README.md]. Reversing is one sentence.

## Decisions and ADRs

| decision | where |
|----------|-------|
| The two routes to a completed move are distinguishable in `apply_plan`'s return, via a tagged `Outcome` in action order | ADR-0007 (new), `## Decision` |
| The exit status turns on `kind`, not on the list being non-empty, and stays in `cli.py` | ADR-0007 `## Decision`; ADR-0002 for the layering |
| ADR-0003 is **not** superseded — its decision was already what this implements | ADR-0007 `## Consequences` |
| ADR-0006's sentence describing the old `list[str]` return is left as written, as a record of what was true then | ADR-0007 `## Consequences`; `spec/doc-header.md` §4 |
| `unittest.mock`; the `kind` strings; the `os.unlink` case; `README.md` untouched | `## Assumptions` above |

`docs/architecture/overview.md` goes to version 4 in this execution: its fallback paragraph said the
defect was live and said nothing about what replaces it.

## Scaffolding

none.

## Risks

- **Patching `tidy.apply.os.link` patches the `os` module's attribute, not a private alias**, so for
  the duration of the patch every caller in the process sees it. Nothing else in the suite calls
  `os.link` — `shutil.move` uses `os.rename` then copy-and-unlink, and `os.makedirs` does not link —
  and `unittest discover` runs single-threaded, so the scope is the `with` block. If a later item
  adds a linking code path, this is the test that will surprise it.
- **The `0o500` directory test proves nothing under root or on a filesystem that ignores the mode**,
  and skips there. On such a platform AC3's end-to-end leg is unproven and only the unit-level
  assertions carry it. This is the same limitation `BadTargetTests` already accepts, and it should be
  named in `impl-report.md` rather than discovered at verification.
- **The injection reproduces the branch, not the platform.** No test here runs on exFAT, FAT32 or an
  SMB mount, so what is proven is that the code behaves correctly when `os.link` raises — which is
  what those filesystems do, but by inference from the errno rather than by observation.
- **AC2 is a byte-for-byte constraint on prose**, so an incidental reword of the fallback message
  while editing around it fails the item. Step 3 changes no message string; a `git diff` that shows
  one is the signal.

## Out of scope for this item

- BUG-0003 (`--help` still describes sorting by type alone) and BUG-0004 (one dangling symlink stops
  the whole folder). Both are open, both are in `apply`/`cli` territory, and neither is touched here.
- The fallback's TOCTOU window between `os.path.lexists` and `shutil.move`. ADR-0003 accepted it
  knowingly [src: ADR-0003] and BUG-0002 does not reopen it.
- Any new exit status. The vocabulary stays 0, 1 and 2 as `README.md` documents it.
- WI-0003 (user-supplied rules), which touches `rules.py` and not this module.
