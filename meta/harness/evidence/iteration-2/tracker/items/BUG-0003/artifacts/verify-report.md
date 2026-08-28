# Verification report — BUG-0003

Verified-commit: f575fc9caad0042d4d55bf3e05231fd2031dbfb5

## Verdict

**Pass.** All four criteria are met, each demonstrated by a command run in this execution against
the branch head. Every experiment that could have falsified them was run in a detached worktree at
`f575fc9`, which has been removed; the branch itself was never modified.

One thing is declared rather than hidden: under a strict reading of AC4's phrase "when the
**description** is reverted", the delivered test does not fail — reverting `description` alone,
while leaving the new epilog in place, leaves the suite green. AC4 is recorded as **pass** because
the record settles which reading was meant, not because the strict one was ignored. The experiment
and the reasoning are in `## Defects found`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — `--help` exits 0, says age takes part, names `recent` and `old` | **pass** | `python3 -m tidy --help; echo $?` then `python3 -m tidy --help \| grep -o '\b<w>\b' \| wc -l` for `recent`, `old`, `modified`, `age` | exit `0`; description reads `Sort the files sitting directly in a folder into subfolders chosen from how old each file is and what kind of file it is.`; epilog reads `... the band is recent or old, chosen from when the file was last modified ...`. Counts: `\brecent\b` → 1, `\bold\b` → 2, `\bmodified\b` → 1, `\bage\b` → 0 | The age claim is made twice — "how old each file is" in the description and "when the file was last modified" in the epilog — and both band names are present as whole words. `\bage\b` is 0, which is why the test's vocabulary is four words rather than one |
| AC2 — no longer implies a single rule table | **pass** | `python3 -m tidy --help \| grep -c 'extension-to-folder'`; then the epilog read against `README.md` §"Where each file goes" | `0`, grep exit `1`. The epilog now says `Both rule tables are in README.md.` | `README.md` §"Where each file goes" carries exactly two tables — `### The band: how old the file is` (`recent`/`old`) and `### The type folder, inside the band` (seven folders). "Both rule tables" states the count the section documents, and the qualifier the criterion names is gone |
| AC3 — everything WI-0001 AC1 requires is still true | **pass** | `python3 -m tidy --help \| grep -n 'folder\|--apply\|previews\|changes nothing on disk'` — the same grep WI-0001's verification recorded | `usage: tidy [-h] [--apply] folder`; `  folder      the folder to tidy; only the files directly inside it are considered`; `  --apply     actually move the files; without this flag tidy only previews and moves nothing`; `Without --apply, tidy previews only: it prints every move it would make and changes nothing on disk.` | All three requirements hold: `folder` is the sole positional and appears first in the usage line, `--apply` is named as the flag, and preview-by-default is stated twice. Independently sensitive — see `## Test sensitivity check`, experiment 3 |
| AC4 — a regression test asserts AC1 and AC3, fails on the old wording, restates no literal | **pass** | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -t .` against a full revert of both strings; plus an AST extraction of every string literal in the new test compared against the live help output | Reverted: `Ran 69 tests ... FAILED (failures=1)`, the one failure being `test_help_says_age_chooses_the_band_and_names_every_band` with `AssertionError: Regex didn't match: '\brecent\b' not found in ...`. Restored: `Ran 69 tests ... OK`. Literals in the test: `'--help'`, `'\b%s\b'` ×2, `'modified'`, `'age'`, `'aged'`, `'older'` — longest 8 characters, no phrase or clause from the help text | The test asserts AC1 (status, every band in `DEFAULT_BANDS`, an age word) and AC3 is asserted by `test_help_names_folder_apply_and_default`, in the same class and file, which AC4 asks be kept true. The strict-reading gap is in `## Defects found` |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` run by me on `f575fc9` → exit 0, `Ran 69 tests ... OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 9 items, 10 documents, 0 errors 0 warnings |
| `every-criterion-independently-checked` | **pass** | Each of the four rows above names a command I ran and quotes its real output. No row cites `impl-report.md`; the checks were derived from the criteria before the report was read for its deviations |
| `negative-cases-exercised` | **pass** | Five listed below, including the two the plan named as risks (terminal width, and the substring trap) |

## Negative and boundary cases exercised

1. **Narrow terminal, `COLUMNS=20`.** `argparse` re-wrapped the epilog to nine words a line; `\brecent\b` → 1, `\bold\b` → 2, `\bmodified\b` → 1. The plan's risk that wrapping could split an asserted word does not materialise — `textwrap` breaks on whitespace, not inside words.
2. **Wide terminal, `COLUMNS=200`.** Same three counts. The assertions are width-independent in both directions.
3. **Short flag.** `python3 -m tidy -h \| diff - <(python3 -m tidy --help)` → no differences, exit 0. The criteria name `--help`; `-h` gives the identical text.
4. **The substring trap, measured rather than assumed.** In the delivered help output the substring `age` occurs twice (inside `usage`) and `older` five times (inside `folder`), while `\bage\b` and `\bolder\b` each occur **zero** times. A substring-based age check would therefore have been satisfied by the word `usage:` alone, on any help text ever printed. The word boundaries are load-bearing, not stylistic.
5. **The command still works.** A preview over a folder holding a fresh `holiday.jpg` and a `2020-01-01` `ancient.pdf` printed `move   ancient.pdf -> old/documents/ancient.pdf` and `move   holiday.jpg -> recent/images/holiday.jpg`, exit 0; a non-directory target still printed `tidy: <path> is not a folder` and exited 2. `cli.py` was edited, so its two behavioural responsibilities were re-checked rather than assumed.

## Test sensitivity check

Three experiments, all in a detached worktree at `f575fc9`, each with `tidy/__pycache__` and
`tests/__pycache__` removed and `PYTHONDONTWRITEBYTECODE=1` set, and each reverted afterwards.

1. **Both strings reverted to the pre-fix wording** → `Ran 69 tests ... FAILED (failures=1)`. The
   only failure is the new test, on `'\brecent\b' not found`. The other 68 tests are unaffected in
   both directions, so the new test is the whole of the difference.
2. **A third band added to `DEFAULT_BANDS`** — `("ancient", 3650 * 24 * 3600)` — with the help text
   untouched → `FAILED (failures=1)`, `AssertionError: Regex didn't match: '\bancient\b' not found
   in ...`. This is the guard ADR-0008 promises and that `docs/architecture/overview.md` v6 tells
   WI-0003 to expect, demonstrated rather than asserted.
3. **The preview sentence removed from the epilog** → `test_help_names_folder_apply_and_default`
   fails on `'changes nothing on disk' not found`. AC3's evidence is a live assertion, not a
   sentence that happens to still be there.

## Defects found

None that belong to another item, so no bug was filed. One finding is recorded here for the
review, and it is about this item's own criterion rather than about the code.

**AC4 has two readings, and the delivered test satisfies one of them.**

- *Strict:* "fails when the `description` is reverted" means the `description=` argument
  specifically. The item's `## Summary` does use `description` as the name of one of two strings,
  distinguishing it from `epilog` by line number.
- *Loose:* it means the tool's description of itself — the help text quoted whole under
  `## Actual behaviour`.

Measured: reverting **only** `description` to `"...chosen by file type."`, keeping the new epilog,
leaves the suite green — `Ran 69 tests ... OK`. Under the strict reading AC4 fails; under the loose
one it passes, as experiment 1 shows.

I took the loose reading, because the record settles it rather than because it is the one that
passes. `verify`'s own entry filing this item glosses AC4 as asking "for a test that does not
restate the help string verbatim, so it guards the claim rather than the wording"
[src: tracker/items/BUG-0003/journal.md] — the entry of 2026-08-27T19:11:48Z, `## Decisions`
bullet 4; AC1's own checkable clause says "grepping the help
**output**"; and `plan.md` read it the same way without anyone objecting. Three artifacts agree and
none supports the strict reading.

The gap is real all the same, and narrow: if a future edit reverts the description while leaving
the epilog correct, the help text would contradict itself and no test would object. It is not a
defect in delivered behaviour — the text is right today — so it is neither a send-back nor a bug.
It is put here so that `review-close` decides knowingly, and so that whoever widens the guard later
finds the measurement rather than repeating it.

## Not verified, and why

- **That the wording is *good*, as opposed to true and complete.** The criteria constrain what the
  text must state; none of them constrains readability, and I did not substitute my judgement for
  the plan's on a decision it was asked to settle.
- **The extension table against the help text.** The help names no extensions, so there is nothing
  to compare. ADR-0008 records this as an accepted gap and says what should happen if a later item
  makes the help list them. Unchanged by this item and out of its scope.
- **Locales and encodings.** `--help` was run under this environment's default locale only. Nothing
  in the change is locale-sensitive — the strings are ASCII and `argparse` does not translate them —
  but that is an inference, not an observation.
- **`README.md` itself.** AC2 asks that the help agree with §"Where each file goes"; I read that
  section and confirmed it documents two tables. Whether the rest of `README.md` is accurate was not
  in scope, and BUG-0005 is open against a different part of it.
