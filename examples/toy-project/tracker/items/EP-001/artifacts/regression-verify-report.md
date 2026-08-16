# Verification report — EP-001 (independent regression pass over merged trunk)

Verified-commit: 6d1e437b4293571296809b322c47fb0dc83d1ad6

Branch: `main`. Run 2026-08-17, after EP-001 was closed and both work items were `done` and
merged.

This is not the `verify` execution of a single item at `verifying`. It is an independent
regression pass over what is actually on the trunk, judged against WI-0001's and WI-0002's
acceptance criteria, EP-001's `## Success measures`, and ADR-0001 to ADR-0005. It is written here
rather than at `tracker/items/WI-0001/artifacts/verify-report.md` because overwriting a closed
item's verification report would destroy the evidence `review-close` cited for D2 and D10; the
per-item journals point at this file.

Every command below was run by this execution. No claim in any `impl-report.md`, `review.md` or
existing `verify-report.md` was read as evidence; the item bodies, the ADRs, the vision and the
architecture overview were read as the standard, and the reports were read only afterwards to see
what had already been declared as a gap.

Environment: Linux 7.0.0-28-generic (Ubuntu 24.04), Python 3.12.3, ext4, non-root user (uid 1000).

## Verdict

**Three defects in delivered behaviour.** Filed as `BUG-0001` (high), `BUG-0002` (medium) and
`BUG-0003` (medium), each at `ready`, each `found-in: WI-0001`. All three were reproduced against
the `linecount.py` WI-0001 shipped (commit `5adc619`) as well as against trunk, so none of them is
WI-0002's.

Everything else held. All 24 acceptance criteria across the two items reproduced as written on
fixtures built for this pass, the 46 tests pass, and 13 targeted mutations of `linecount.py` each
made the suite fail, so the tests are sensitive rather than decorative.

One methodology conflict has no answer in the record and is filed as `EP-001/Q-001` to the
architect: filing a bug under a closed epic makes `validate-workspace` fail
`epic.closed-with-open-children`, and an epic has no legal transition out of `done`.

## Criteria

Fixtures were built from the criteria before the code was read. `·` stands for one space where a
column is being pinned.

### WI-0001

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | folder with `notes.md` (128 lines) and `a.py` (7): `python3 linecount.py /tmp/qa-lc/A \| cat -A` | `128  notes.md$` / `  7  a.py$` / `135  total$` | the criterion's own worked example, byte for byte; column 3 wide because of `135` |
| AC2 | pass | `A.md`/`B.md`/`a.md`/`b.md` at 2 lines, `zz.md` at 1: `python3 linecount.py /tmp/qa-lc7/tie`; then `cmd > a; cmd > b; diff a b` | `2  A.md` / `2  B.md` / `2  a.md` / `2  b.md` / `1  zz.md` / `9  total`; `diff` exit 0, no output | byte order, so `A.md` precedes `a.md`; repeat run identical |
| AC3 | pass | as AC1/AC2 above | last line `135  total`, `9  total` | total is the sum, right-aligned in the same column, last |
| AC4 | pass | folder with `empty.txt` (0 bytes) among four others: `python3 linecount.py /tmp/qa-lc7/count` | `0  empty.txt` present, last in the order | listed, not omitted, in its sorted position |
| AC5 | pass | `two_nl.txt`=`a\nb\n`, `no_trailing.txt`=`a\nb`, `just_nl.txt`=`\n`, `one_noeol.txt`=`abc`, `empty.txt`=`` | `2  no_trailing.txt` / `2  two_nl.txt` / `1  just_nl.txt` / `1  one_noeol.txt` / `0  empty.txt` / `6  total` | all four rules of the criterion, one folder |
| AC6 | pass | folder holding `sub/` plus files: `python3 linecount.py /tmp/qa-lc7/mixed` | no row for `sub`, stderr empty, exit 0 | |
| AC7 | **fail** | `link-to-file`→`real.txt`, `link-to-dir`→`sub`, `broken-link`→`nowhere.txt` | `3  link-to-file` listed; `link-to-dir` and `broken-link` absent; stderr empty; exit 0 — **but** a symlink loop or a symlink whose target cannot be stat'ed aborts the whole run: `linecount: /tmp/bug1a: Too many levels of symbolic links`, exit 2, empty stdout | the three named cases pass; two further "resolves to nothing" cases do not. **BUG-0001** |
| AC8 | pass | `.gitignore` (1 line) in `/tmp/qa-lc7/mixed` | `1  .gitignore` listed like any other row | |
| AC9 | pass | 4008-byte PNG (`\x89PNG\r\n\x1a\n` + random bytes) beside `notes.txt`: `grep -c Traceback` on both streams | `13  img.png` / `3  notes.txt` / `16  total`; stderr empty; exit 0; `Traceback` count 0 in stdout and 0 in stderr | for a **non-text file**. A non-UTF-8 **filename** does produce a traceback — see BUG-0003, filed separately because AC9's condition is the file's content |
| AC10 | pass | an empty folder, and a folder holding only `s1/` and `s2/`: `... \| cat -A` | `no files$` on stdout, stderr empty, no total row, exit 0, for both | see BUG-0002: this output is also produced for a folder that *does* have files |
| AC11 | pass | `python3 linecount.py /tmp/qa-lc8/does-not-exist`; and a directory `chmod 000` as uid 1000 | `linecount: /tmp/qa-lc8/does-not-exist: No such file or directory`, exit 2, stdout empty; `linecount: /tmp/qa-lc6/d000: Permission denied`, exit 2, stdout empty | one line on stderr each, naming path and problem |
| AC12 | pass | `python3 linecount.py /tmp/qa-lc8/plainfile.txt`; `python3 linecount.py` | `linecount: /tmp/qa-lc8/plainfile.txt: Not a directory`, exit 2; `usage: linecount [-h] [--top N] folder` + `linecount: error: the following arguments are required: folder`, exit 2 | stdout empty in both; wording is unconstrained by the criterion |
| AC13 | pass | `cd <repo root> && python3 -m unittest discover; echo $?` | `Ran 46 tests in 1.155s` / `OK` / exit 0 | no installation step; stdlib only |

### WI-0002

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | 27-file folder (26 × 46 lines, `small.txt` 8): `python3 linecount.py --top 3 /tmp/qa-lc9/f27` | `  46  f00.txt` / `  46  f01.txt` / `  46  f02.txt` / `1204  total (all 27 files)` | three rows, the first three of WI-0001 AC2's order |
| AC2 | pass | `big.txt` 9 lines, `a.md`/`b.md`/`c.md` 5 each: `--top 3` | ` 9  big.txt` / ` 5  a.md` / ` 5  b.md` / `24  total (all 4 files)` | no row for `c.md`; the cut is broken by filename |
| AC3 | pass | as AC1 | `1204  total (all 27 files)` | the criterion's own numbers; total is every file, label names M |
| AC4 | pass | `git show 5adc619:linecount.py` extracted to `/tmp/qa-lc10/lc_wi1.py`, then both binaries run on 8 folders + 2 error paths, comparing stdout, stderr and exit code | `IDENTICAL` on all 8 folders and both error paths | the one difference is the usage line with no argument (`[--top N]` added) — already recorded as an accepted gap in WI-0002 `## Notes`, and outside AC4's "on the same folder". WI-0001's 46 tests pass unmodified |
| AC5 | pass | `--top 99` on the 4-file tie folder | all four rows, then `24  total (all 4 files)`, exit 0 | AC3's label kept even though every file is shown |
| AC6 | pass | `--top 0` on the same folder | `24  total (all 4 files)`, exit 0, no file rows | not an error |
| AC7 | pass | `--top -1`, `--top abc`, `--top 3.5`, `--top ''` | `linecount: --top: -1 is negative`; `linecount: --top: 'abc' is not a whole number`; `linecount: --top: '3.5' is not a whole number`; `linecount: --top: '' is not a whole number` — each one line, stdout empty, exit 2 | one line, per ADR-0004; argparse's two-line shape avoided |
| AC8 | pass | `--top 3 <folder>` vs `<folder> --top 3`, `diff` on both streams; then `-t 3 <folder>` | streams identical, exits 0/0; `-t` gives `usage: ...` + `linecount: error: unrecognized arguments: -t /tmp/qa-lc7/tie`, stdout empty, exit 2 | |
| AC9 | pass | empty folder with `--top 0`, `--top 3`, `--top 99` | `no files$` on stdout, stderr empty, exit 0, for all three | WI-0001 AC10 wins over any N |
| AC10 | pass | the corrected example: 27 files, `--top 2` | `  46  f00.txt$` / `  46  f01.txt$` / `1204  total (all 27 files)$` | the column is 4 wide because the total is the widest number printed |
| AC11 | pass | `python3 -m unittest discover` from the repo root | exit 0, 46 tests | new behaviour covered: 19 of the 46 tests are in `ParseTopTest`, `TopFormatTest` and `TopTest`, all added by this item |

### EP-001 success measures

| measure | verdict | evidence |
|---------|---------|----------|
| biggest file is the first row, no flags | pass | `/tmp/qa-lc3/big` (200 files): first row `  200  f199.txt` |
| folder with a subdirectory exits 0 where `wc -l *` errors | pass | on `/tmp/qa-lc7/mixed`, `wc -l *` prints `wc: sub: Is a directory` and `wc: link-to-dir: Is a directory` and `wc: broken-link: No such file or directory`; `linecount.py` prints four clean rows and exits 0 |
| first three rows name the three largest; output pipes into `head` | pass, with a bound | `python3 linecount.py /tmp/qa-lc3/big \| head -3` gives the three largest, exit 0. See `## Not verified, and why` for the size at which it stops holding |
| a non-text file gives a complete listing, exit 0, no traceback | pass | the PNG fixture: 2 rows + total, `Traceback` count 0 on both streams, exit 0 |
| a missing or unreadable path names the problem and exits non-zero | pass | AC11 above, both cases |
| only Python 3 needed to run the tool and its tests | pass | `python3 linecount.py` and `python3 -m unittest discover` both run with no install step, on Python 3.12.3; `linecount.py`'s only imports are `argparse`, `os` and `sys`, and the repository holds no dependency manifest |

### ADRs

| ADR | verdict | evidence |
|-----|---------|----------|
| ADR-0001 (argparse) | pass | usage errors exit 2 on stderr; the stated consequences hold — `--top=2` and the abbreviation `--to 2` are both accepted and both produce `2  A.md` / `2  B.md` / `9  total (all 5 files)`, which the ADR predicts and no criterion forbids |
| ADR-0002 (unreadable file) | **partial** | one unreadable file among readable ones behaves exactly as decided: `linecount: no.txt: Permission denied` on stderr, the file omitted, exit 0. But the ADR's own boundary — "It does not apply to the folder itself, which is AC11's territory and exits 2" — is crossed by BUG-0001, and the all-skipped case is BUG-0002 |
| ADR-0003 (no lint) | pass, as a skip | `tracker/project.yaml` has `lint: null`; there is no lint command to run, so `lint-clean` is recorded skipped below, not passed |
| ADR-0004 (parse_top) | pass | AC7's four cases each produce exactly one stderr line; the stated consequences hold — `--top 3_0` yields 30 and `--top ' 3 '` yields 3, both printing `9  total (all 5 files)`, and `--top +2` prints two rows |
| ADR-0005 (format_report signature) | **partial** | the three branches behave as decided (AC4, AC6, AC9 above). Its named misuse — "If a third caller ever forgets, it prints `no files` for a folder that had some" — is reached by `main` itself: BUG-0002 |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover` from the repo root → exit 0, `Ran 46 tests ... OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` (ADR-0003). No command exists to run. Recorded as skipped, never as passed |
| `workspace-valid` | **fail** | `.claude/agile-skills/scripts/validate-workspace` → exit 1, one remaining error: `tracker/items/EP-001/item.md: ERROR [epic.closed-with-open-children] the epic is done but BUG-0001, BUG-0002, BUG-0003 are not`. This is caused by filing the bugs, which this skill is required to do, and no legal transition clears it. Filed as `EP-001/Q-001` to the architect. The other seven errors this pass created (a title over 80 characters, stale `updated` timestamps, missing journal entries, a stale board) were all fixed |
| `every-criterion-independently-checked` | **pass** | all 24 criteria have a row above with the command this pass ran and its actual output |
| `negative-cases-exercised` | **pass** | see the next section |
| `tests-would-fail-without-the-change` | **pass** | see `## Test sensitivity check` |

## Negative and boundary cases exercised

Triggered, not read about:

- Empty folder; folder holding only subdirectories; folder holding only subdirectories with
  `--top 0`, `--top 3`, `--top 99`.
- Zero-byte file; file of exactly `\n`; file with no trailing newline; file with no newline at
  all; a 4 KB binary PNG.
- A path that does not exist; a path that is a regular file; no argument at all; a directory of
  mode `000` as uid 1000.
- A directory of mode `444` — readable, not traversable. Every file in it is skipped and stdout
  reads `no files`. **BUG-0002.**
- A folder in which every file is mode `000`. Same result. **BUG-0002.**
- `--top -1`, `--top abc`, `--top 3.5`, `--top ''`, `--top` with no value, `-t 3`, `--top=2`,
  `--to 2`, `--top 3_0`, `--top ' 3 '`, `--top +2`, `--top 100000000000000000000`.
- `--top 0` on a folder that has files (total row alone) and on one that has none (`no files`).
- Symlink to a regular file; symlink to a directory; broken symlink; **two-link symlink loop**;
  **self-referential symlink**; **symlink into a `chmod 000` directory**. The last three abort the
  entire run with exit 2. **BUG-0001.**
- A FIFO and a symlink to `/dev/zero` in the listed folder — correctly ignored, though no
  criterion names them.
- A filename that is not valid UTF-8 (`bad\xff.txt`). **BUG-0003.**
- Folder argument given as `.`, and with a trailing slash — both fine.
- Piping into `head -1` and `head -3` at 200, 250, 300, 320 and 5000 files; and a folder path
  containing a file whose name is 200 characters long.

## Test sensitivity check

`linecount.py` was copied to a scratch tree with `tests/`, mutated one change at a time, and
`python3 -m unittest discover` run against each mutation. Every one was caught; the count is the
number of failing tests.

| mutation | suite result |
|----------|--------------|
| sort ascending instead of descending | FAILED (failures=11) |
| tie-break dropped from the sort key | FAILED (failures=3) |
| the "+1 for a final line with no newline" rule disabled | FAILED (failures=2) |
| two spaces between column and name reduced to one | FAILED (failures=22) |
| column width computed without the total | FAILED (failures=9) |
| `is_file(follow_symlinks=False)` | FAILED (failures=1) |
| dotfiles filtered out of the listing | FAILED (failures=1) |
| `no files` replaced by a zero total row | FAILED (failures=7) |
| folder-error exit status 2 → 1 | FAILED (failures=3) |
| `--top` negative check removed | FAILED (failures=2) |
| `total (all M files)` label reduced to `total` | FAILED (failures=8) |
| the `rows[:top]` slice ignored | FAILED (failures=7) |
| ADR-0002's stderr line removed (skip silently) | FAILED (failures=1) |

The scratch tree was discarded and `linecount.py` in the repository is untouched by this pass
(`git status` shows no modification to it).

## Defects found

| id | priority | what | found-in |
|----|----------|------|----------|
| BUG-0001 | high | a symlink that cannot be stat'ed — a loop, or one pointing into an unreadable directory — makes `entry.is_file()` raise, which `main` catches as a folder-level error: nothing on stdout, exit 2, and a stderr line blaming the folder. Contradicts WI-0001 AC7 | WI-0001 |
| BUG-0002 | medium | when every file in a folder is skipped under ADR-0002, stdout prints `no files` — byte-identical to a folder that really is empty. Contradicts WI-0001 AC10's meaning and ADR-0005's stated misuse | WI-0001 |
| BUG-0003 | medium | a filename that is not valid UTF-8 makes `print` raise `UnicodeEncodeError`: a traceback on stderr, empty stdout, exit 1. Contradicts overview v2's "no file can raise a decoding error" and its exit-status contract, and the vision's "a number, not a stack trace" | WI-0001 |

All three were classified as bugs rather than send-backs because both work items are `done` and
merged, and because each reproduces against the `linecount.py` WI-0001 shipped at `5adc619` as
well as against trunk. The `verify` test — "does an acceptance criterion of *this* item say the
behaviour should be different?" — has no send-back target when no item is in flight.

BUG-0001's two triggers are one bug: one uncaught `OSError` class from one call, with two ways to
reach it. They share a reproduction and will share a fix, so they are not split.

## Not verified, and why

- **`BrokenPipeError` when stdout is closed early.** WI-0001's `## Notes` records this as an
  accepted gap inviting "an actual sighting". A sighting exists, but only outside the size
  envelope the human stated ("a few dozen files, occasionally a couple of hundred, never
  thousands"). At 5000 files, `python3 linecount.py /tmp/qa-lc4/f5000 | head -1` prints
  `BrokenPipeError: [Errno 32] Broken pipe` under a traceback and the pipeline's first stage
  exits 1. At 200, 250, 300 and 320 files — including 320 files with 200-character names,
  68 491 bytes, past the 65 536-byte pipe buffer — it did not reproduce. No bug is filed,
  because the only reproduction is at a size the item explicitly excludes; the gap stands as
  WI-0001 recorded it, now with a measured boundary.
- **`lint-clean`.** No linter exists in this project by decision (ADR-0003), so nothing checked
  style, unused imports, or the inert `from __future__ import annotations` that WI-0001's review
  already recorded. That remains unchecked by any tool.
- **Non-POSIX platforms.** Unchanged from WI-0001's accepted gap. Everything here was run on
  Linux as uid 1000. AC7, AC11, ADR-0002 and all three bugs are written in terms of symlinks and
  Unix permissions; none has been run on Windows, and BUG-0003 depends on a filename that Windows
  cannot create.
- **Scale and file size.** The largest folder counted was 5000 small files; the largest single
  file was about 4 KB. Files past `count_lines`'s 1 MiB chunk boundary were exercised only by the
  existing unit tests, not by this pass on disk.
- **Concurrency.** A file deleted or replaced between `list_files` and `count_lines` reaches
  ADR-0002's handler in principle; it was not raced deliberately.
- **The `(all M files)` count when files are skipped.** Judged **not a defect** rather than
  verified clean. `--top 5` on a folder of two files, one unreadable, prints
  `3  total (all 1 files)`. WI-0002 AC3 defines M twice in one sentence — "the number of files in
  the folder — that is, the number of rows the same command would print without `--top`" — and a
  skipped file makes the two halves disagree. The implementation follows the second, which is the
  operative gloss, so no question was filed; the observation is recorded in BUG-0002 `## Notes`
  for whoever fixes the underlying skip behaviour.
- **`workspace-valid` cannot be made to pass** while these bugs sit under a closed epic. See
  `EP-001/Q-001`. Nothing about the three bug items depends on the answer.
