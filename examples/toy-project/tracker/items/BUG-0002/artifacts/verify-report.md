# Verification report — BUG-0002

Verified-commit: e1e29850d6923ecfd7b05bf29a6694a36c333e46

Branch `wi/BUG-0002`, head `e1e2985`; the last code commit is `277c89c` and the one after it
touches only `tracker/`. Fixtures were built fresh under `/tmp/vbug2-9bJv/` — not the `/tmp/bug2a`
… `/tmp/bug2d` folders the item names and the earlier steps reused. Criteria were read before the
implementation report.

## Verdict

**Pass — all seven criteria.** Each decided by a command run here. No defect found, no bug filed,
nothing sent back. Both neighbouring rules the fix could have broken — ADR-0002's stderr line and
ADR-0006's silent skips — were exercised and hold. One coverage observation is recorded below; it
is a gap in the tests, not a fault in the behaviour.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | a fresh folder with `one.txt` (1 line) and `two.txt` (2), both `chmod 000`; `python3 $L $F` | stdout `no files could be read`; stderr exactly **2 lines** — `linecount: one.txt: Permission denied`, `linecount: two.txt: Permission denied`; exit 0 | stdout no longer claims the folder is empty, and ADR-0002's per-file lines are unchanged in wording, stream and count |
| AC2 | **pass** | the same folder and a genuinely empty one, both with stderr discarded, compared with `cmp` | skipped folder → `no files could be read`; empty folder → `no files`; `cmp` reports them **different** | the criterion's own test: a reader who sees only stdout can now tell the two apart. Before the fix these were byte-identical |
| AC3 | **pass** | a folder `chmod 444` holding `f.txt` (2 lines) and `g.txt` (1); `python3 $L $F` | stdout `no files could be read`, stderr 2 lines, exit 0 | readable but not traversable — the names list, the opens fail — and it behaves exactly as trigger A |
| AC4 | **pass** | an empty folder, then a folder holding only `one/` and `two/` | both: stdout exactly `no files`, stderr **0 bytes**, no total row, exit 0 | WI-0001 AC10 intact. This is the criterion the fix most easily breaks, and mutations 2 and 3 below show four tests catch it if it does |
| AC5 | **pass** | `--top 0`, `--top 3`, `--top 99` on the empty folder | `no files` each time, exit 0 each time | WI-0002 AC9 intact for every N |
| AC6 | **pass** | a folder with `ok.txt` (3 lines) and a `chmod 000` `no.txt` | stdout `3  ok.txt$` / `3  total$`; stderr `linecount: no.txt: Permission denied`; exit 0 | the mixed folder is untouched: a row, the plain total, one stderr line |
| AC7 | **pass** | `git show 6d1e437:linecount.py > linecount.py`, `python3 -m unittest discover`, restore; then the suite on the branch head | at `6d1e437`: **exit 1**, with `test_ac1_all_unreadable_does_not_claim_no_files`, `test_ac2_stdout_differs_from_an_empty_folder` and `test_ac3_untraversable_folder` among the failures. On the branch head: `Ran 55 tests`, `OK`, exit 0 | re-run here rather than accepted from `impl-report.md`. The AC4 test passes at `6d1e437`, as AC7's scoping expects — it asserts behaviour that must not change |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | run here on the branch head: `Ran 55 tests`, `OK`, exit 0 |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` (hard) | **pass** | seven rows above, each a command run here on fixtures no earlier step had touched |
| `negative-cases-exercised` (hard) | **pass** | seven conditions triggered — see below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | five mutations, all caught; table below |

## Negative and boundary cases exercised

1. **Every file `chmod 000`** → `no files could be read`, two stderr lines, exit 0 (AC1).
2. **Folder `chmod 444`** — listable, not openable → the same (AC3).
3. **A genuinely empty folder** → `no files`, nothing on stderr (AC4).
4. **A folder of only subdirectories** → `no files` (AC4).
5. **`--top 0`, `3`, `99` on an empty folder** → `no files` each time (AC5).
6. **One readable file beside one unreadable** → the row, the plain total, one stderr line (AC6).
7. **ADR-0006's boundary: a folder of only symlink loops** → `no files`, stderr empty, exit 0.
   Not a criterion of this item, but the case where the two bugs meet: an entry that cannot be
   *resolved* is still not a file, so the counter never sees it and stdout correctly says the
   folder held none.

And the case the plan predicted and the implementation report declared untested:

- **A folder mixing an unreadable file with a symlink loop** → stdout `no files could be read`,
  stderr `linecount: secret.txt: Permission denied`, exit 0. Exactly what plan assumption 2 says
  should happen: at least one entry was a file, so that is the half stdout reports; the loop stays
  silent under ADR-0006.

## Test sensitivity check

Each mutation applied to `linecount.py`, suite run, file restored; `git status` clean afterwards.
**Five mutations, five caught.**

| mutation | caught by |
|----------|-----------|
| the code as it stood at `6d1e437` (AC7's own demonstration) | this item's AC1, AC2, AC3 tests and the renderer test — plus BUG-0001's three, which that commit also predates |
| the new branch removed, so every empty result says `no files` again | `test_ac1_all_unreadable_does_not_claim_no_files`, `test_ac2_stdout_differs_from_an_empty_folder`, `test_ac3_untraversable_folder` |
| the new sentence used for **every** empty result, including a truly empty folder | `test_ac4_empty_and_subdirectory_only_folders_are_unchanged`, `test_ac2_stdout_differs_from_an_empty_folder`, and WI-0001's `test_ac10_empty_folder`, `test_ac10_folder_holding_only_subdirectories`, `test_ac9_empty_folder_whatever_n_is` |
| `format_report`'s **default** changed to the new sentence | eight tests, including WI-0001's `test_ac10_no_rows_is_no_files_and_no_total` and WI-0002's `test_ac4_the_old_calls_are_unchanged` |
| the `unreadable` counter never incremented | the same three as the second mutation |

The third and fourth are the ones worth having: they are how this fix would most plausibly have
been written wrong — by making the new sentence the general case — and between them five of
WI-0001's and WI-0002's own tests object.

## Diff review against the plan

`linecount.py` +14/−5, `tests/test_linecount.py` +72/−0. Every hunk traces to a plan step: the
`empty` parameter and its docstring (step 1), the counter (step 2), the branch (step 3), the
appended `AllFilesSkippedTest` (step 4). The test file's diff has **0** deleted lines, so all 50
earlier tests are intact and in the passing run. `count_lines`, `list_files`, the sort key, the row
format, the total and `--top`'s slice and label are byte-identical to `main`.

The report's claim that `--top`'s label is unchanged was checked rather than accepted: on a folder
with one readable and one skipped file, `--top 5` prints `3  total (all 1 files)`, exactly as it
did before this item.

## Defects found

None. No criterion of this item failed, and nothing delivered by another item was found broken —
WI-0001 AC10, WI-0002 AC9, ADR-0002's stderr behaviour and ADR-0006's silent skips were each
exercised directly.

## Not verified, and why

- **Lint.** No lint command exists (ADR-0003); the fourteen changed lines were read at review and
  by no tool.
- **A coverage gap, recorded rather than filed:** no test asserts that a folder containing *only*
  unresolvable entries still prints `no files`. I verified it by hand (case 7 above) and it is
  correct, but nothing in the suite would notice if a future change made the counter include
  entries that were never established to be files. No criterion of BUG-0002 requires that case —
  AC4 names an empty folder and a subdirectory-only folder — so this is a gap in tests, not a
  failure, and it belongs in the item's notes rather than in a bug item.
- **The wording itself.** `no files could be read` is ADR-0007's choice; no criterion fixes it, so
  there is nothing to verify it against beyond "it is not `no files`", which AC1 and AC2 pin.
- **Non-POSIX platforms**, unchanged from WI-0001: every fixture here uses Unix permissions.
- **A folder with thousands of unreadable files** — the counter is an integer and the stderr lines
  are one per file, so the shape does not change with scale, but only two-file and three-file
  folders were exercised.
