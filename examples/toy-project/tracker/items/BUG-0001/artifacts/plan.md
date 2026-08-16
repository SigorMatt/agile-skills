# Plan — BUG-0001 A symlink that cannot be stat'ed aborts the listing and blames the folder

## Problem

A folder holding one readable file and one symlink that cannot be resolved — a loop, or a link
into a directory the user cannot traverse — produces no report at all: stdout is empty, stderr
says `linecount: <the folder>: Too many levels of symbolic links` (or `Permission denied`), and
the exit status is 2. The folder is readable and its real files are countable; the message names
the wrong thing and the failure is not one.

The cause is two lines that were correct in isolation. `list_files` resolves each entry with
`entry.is_file(follow_symlinks=True)`, which swallows `FileNotFoundError` — that is why a plain
broken symlink already works — and lets every other `OSError` out. `main` wraps the whole call in
one `except OSError` that is WI-0001 AC11's folder-failure path. Verified at the interpreter
before planning: on the reproduction folder, `ok.txt` resolves, and both legs of the loop raise
`OSError 40 Too many levels of symbolic links`.

The fix must keep three failure sites distinguishable — the folder, an entry that cannot be
resolved, and a file that cannot be read — which is what ADR-0006 records.

## Approach

One `try` / `except OSError` around the per-entry resolution in `list_files`, treating an entry
whose type cannot be determined as **not a file**: ignored in silence, exactly as WI-0001 AC7
already ignores a broken symlink (ADR-0006). Nothing else in the file changes: not `count_lines`,
not `format_report`, not the sort key, not `main`'s folder handler, which then sees only the
errors that really are the folder's.

The scope is deliberately one bug. BUG-0002 (a folder whose files are all unreadable prints
`no files`) and BUG-0003 (an undecodable filename) are separate items and are not touched here,
even where the same function is nearby.

## Steps

1. **Change `list_files` in `linecount.py`.** Replace the direct call in the loop with:

   ```python
   for entry in entries:
       try:
           resolved = entry.is_file(follow_symlinks=True)
       except OSError:
           # The entry cannot be resolved — a symlink loop, or a target we cannot stat. We
           # cannot even establish that it is a file, so it is ignored exactly as a broken
           # symlink is (BUG-0001, ADR-0006).
           resolved = False
       if resolved:
           names.append(entry.name)
   ```

   Extend the docstring to state the rule and cite ADR-0006, and to say that an `OSError` from
   `os.scandir` itself still propagates — that is the folder's failure and AC11's territory.
   Observable result: on the trigger A folder, `python3 linecount.py /tmp/bug1a` prints
   `3  ok.txt` and `3  total`, nothing on stderr, exit 0.

2. **Add regression tests to `tests/test_linecount.py`** in a new class `UnresolvableEntryTest`,
   appended after the existing classes; no existing test is modified. Each builds its folder in a
   `tempfile.TemporaryDirectory()` and runs the script as a subprocess, as the existing
   end-to-end tests do. The four tests are named in the mapping table below. The permission-based
   ones are guarded with `@unittest.skipIf(IS_ROOT, NOT_AS_ROOT)`, the guard already in the file.

3. **Demonstrate the tests fail against the code as it stands** at
   `6d1e437b4293571296809b322c47fb0dc83d1ad6`, which BUG-0001 AC6 requires. The mechanism:
   `git show 6d1e437:linecount.py > linecount.py` in a scratch worktree state, run
   `python3 -m unittest discover`, record which tests fail, then restore. Observable result: the
   three tests for AC1, AC2 and AC3 fail on the old code and pass on the new; the AC5 test passes
   on both, because AC5 is behaviour that must not change.

4. **Run the gates and write `artifacts/impl-report.md`**: `python3 -m unittest discover` exits 0
   on the branch head, `lint-clean` is recorded skipped with ADR-0003 as the reason, and the
   report maps AC1–AC6 to the evidence.

`docs/architecture/overview.md` was updated to v3 by this planning execution, not by
`implement` — the exit-status contract in its `## Boundaries that are deliberate` section is what
this bug violated, and `implement` may not write to `docs/`.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — trigger A prints `3  ok.txt` and `3  total`, nothing on stderr, exit 0 | 1 | `UnresolvableEntryTest.test_ac1_symlink_loop_does_not_abort_the_listing`: builds `ok.txt` (3 lines) and the two-legged loop `q → p → q`, asserts stdout is exactly `b"3  ok.txt\n3  total\n"`, stderr `b""`, exit 0 |
| AC2 — a self-referential symlink gives the same shape | 1 | `UnresolvableEntryTest.test_ac2_self_referential_symlink`: `ok.txt` (3 lines) and `ln -s self self`; same three assertions |
| AC3 — trigger B prints `2  ok.txt` and `2  total`, exit 0, and does not blame the folder | 1 | `UnresolvableEntryTest.test_ac3_symlink_into_an_untraversable_directory`: a `chmod 000` vault directory with a file inside it, a symlink to that file, and `ok.txt` (2 lines); asserts stdout exactly `b"2  ok.txt\n2  total\n"` and exit 0, and asserts the folder's own path never appears on stderr. Under ADR-0006 stderr is empty, which the test also asserts — the ADR is what makes that the criterion's "whether such a message is printed at all is for `plan` to decide and record" |
| AC4 — WI-0001 AC7's three named cases are unchanged | 1 | the existing `test_ac7_symlink_to_a_file_is_listed_under_its_own_name`, `test_ac7_symlink_to_a_directory_is_ignored` and `test_ac7_broken_symlink_is_ignored`, unmodified and still passing in the same run |
| AC5 — WI-0001 AC11 is unchanged: a mode `000` folder still exits 2 | 1 | the existing `test_ac11_folder_that_cannot_be_read`, plus a new `UnresolvableEntryTest.test_ac5_an_unreadable_folder_still_exits_2` that asserts the fix did not swallow the folder's own error: empty stdout, one stderr line naming the folder, exit 2 |
| AC6 — the regression tests fail against `6d1e437`, and `unittest discover` exits 0 | 2, 3 | the run recorded in step 3, quoted in `impl-report.md`: the AC1, AC2 and AC3 tests fail on the old `linecount.py` and pass on the new one; the full suite exits 0 on the branch head |

## Assumptions

1. **Silence for an unresolvable entry, rather than a stderr line.** This is ADR-0006's decision,
   forced by AC1's "prints nothing on stderr" — but it is worth naming here as the thing a reader
   might disagree with: a folder can now contain an entry the tool never mentions. Reversing it
   is a `print` in one `except` branch **plus** a change to AC1, which is `answer-questions`
   territory, not an edit.
2. **`except OSError` rather than a narrower tuple.** `DirEntry.is_file` can raise anything the
   platform's `stat` can; naming a subset would leave the next unlisted errno as a fresh instance
   of this same bug. Reversing it is one clause.
3. **The branch is `wi/BUG-0001`**, because `conventions.branch-prefix` is `wi/` and
   `spec/workspace-layout.md` §5 defines the branch as prefix + item ID. The prefix reads oddly
   for a bug; changing it is a `project.yaml` edit that would affect every future item, and it is
   not this bug's business.

## Decisions and ADRs

| decision | where recorded | branch of the preference order |
|----------|----------------|-------------------------------|
| an entry that cannot be resolved is not a file, and is ignored silently | ADR-0006 | decided here, with four options costed |
| the three `OSError` sites stay distinguishable (folder / entry / file) | ADR-0006's table, `docs/architecture/overview.md` v3 | decided here; ADR-0002 already fixed the third |
| a broken symlink, a symlink to a directory, and a symlink to a file keep their behaviour | WI-0001 AC7, BUG-0001 AC4 | documented |
| a folder that cannot be listed still exits 2 | WI-0001 AC11, BUG-0001 AC5 | documented |
| `except OSError`, the branch name, and the visibility cost of silence | `## Assumptions` | assumed, each with its reversal cost |

## Risks

- **Catching too much.** `except OSError` around the resolution could hide a failure that really
  is the folder's — if `os.scandir` reported a folder-level problem lazily, through the entry
  rather than through the iterator. AC5's test is the guard: a mode `000` folder must still exit
  2, and it is in the same run as the rest.
- **Silence hiding a real problem.** After this fix, a folder full of unresolvable symlinks prints
  `no files` and says nothing. That is BUG-0002's territory — the same false answer from a
  different cause — and it is deliberately **not** fixed here. Whoever fixes BUG-0002 should
  check this case against their fix; it is noted in `## Out of scope for this item` so that it is
  not discovered as a surprise.
- **The test for trigger B needs a `chmod 000` directory** and is meaningless as root, so it is
  skipped there. The existing `IS_ROOT` guard is reused; the run recorded in the implementation
  report must show the test executing, not skipping.

## Out of scope for this item

- **BUG-0002.** A folder whose files are *all* skipped still prints `no files`, and after this fix
  a folder whose entries are all unresolvable does too. That is the same wrong answer and it is a
  separate item with its own criteria.
- **BUG-0003.** An undecodable filename still raises on the way to stdout; nothing here touches
  printing.
- Reporting unresolvable entries on stderr, which AC1 forbids for the loop case.
- Any change to `count_lines`, `format_report`, `parse_top`, `parse_args`, the sort key, the row
  format, the total, or `--top`.
- Any change to WI-0001's or WI-0002's tests. They are the evidence that AC4 and AC5 hold.
