# Implementation report — BUG-0003

## What was built

Two literal strings in `build_parser` were rewritten, and one test was added. Nothing else in the
package changed: `planner.py`, `rules.py` and `apply.py` are byte-for-byte identical to `main`, no
destination or exit status moved, and `tidy/cli.py` still imports only `argparse`, `os`, `sys`,
`.apply` and `.planner` — which is ADR-0008's decision holding rather than an accident.

The help output now reads:

```
$ python3 -m tidy --help
usage: tidy [-h] [--apply] folder

Sort the files sitting directly in a folder into subfolders chosen from how
old each file is and what kind of file it is.

positional arguments:
  folder      the folder to tidy; only the files directly inside it are
              considered

options:
  -h, --help  show this help message and exit
  --apply     actually move the files; without this flag tidy only previews
              and moves nothing

Without --apply, tidy previews only: it prints every move it would make and
changes nothing on disk. Every file that moves lands in <band>/<type>/: the
band is recent or old, chosen from when the file was last modified, and the
folder inside it comes from the file's extension. Both rule tables are in
README.md. Subfolders are never entered or moved, names beginning with '.' are
left alone, and no file is ever overwritten.
```

The wording is the plan's, quoted from `plan.md` `## Approach` and used verbatim. The epilog's
first sentence and its final sentence were copied across untouched, which is what keeps
`previews` and `changes nothing on disk` — the two substrings the codified form of WI-0001 AC1
reads — present.

The test, `tests/test_cli.HelpAndModeTests.test_help_says_age_chooses_the_band_and_names_every_band`,
reads the band names out of `tidy.rules.DEFAULT_BANDS` rather than listing them, and matches each
with `\b...\b`. Both properties are load-bearing and neither is stylistic: reading the table is what
makes the test fail if a band is added and the prose is not updated, and the word boundary is what
stops `old` matching inside `folder`.

Branch `wi/BUG-0003`, two commits: `46e5fd0` (the code and the test) and `01e0879` (the opening
tracker entry). Branched from `main` at `b76b27c`.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `--help` exits 0 and says age takes part, naming `recent` and `old` | The description says the subfolders are chosen from "how old each file is and what kind of file it is"; the epilog names both bands and says the band comes from "when the file was last modified" | `test_help_says_age_chooses_the_band_and_names_every_band` → ok. It asserts `status == 0`, then one `assertRegex` per entry in `DEFAULT_BANDS`, then a match for one of `modified`/`age`/`aged`/`older`. By hand: `python3 -m tidy --help \| grep -c '\brecent\b'` → 1, `'\bold\b'` → 2, `'\bmodified\b'` → 1 |
| AC2 — the output no longer implies a single rule table | The epilog says "Both rule tables are in README.md", which matches `README.md` §"Where each file goes": a band table and a type-folder table | `python3 -m tidy --help \| grep -c 'extension-to-folder'` → exit 1, `0` matches. The phrase the criterion names is gone, and the replacement states the count |
| AC3 — everything WI-0001 AC1 requires of `--help` is still true | Only the middle of the epilog and the description changed; the folder positional, the `--apply` option and the preview sentence are untouched | `test_help_names_folder_apply_and_default` → ok, unchanged except for a comment naming BUG-0003 AC3. It asserts `folder`, `--apply`, `previews` and `changes nothing on disk` in the output. `git diff main..wi/BUG-0003 -- tests/test_cli.py` shows no assertion in that test was altered |
| AC4 — a regression test asserts AC1 and AC3, fails on the old wording, and does not restate the help text as a literal | The new test contains no sentence, clause or fragment of the help output; its expected band names come from `DEFAULT_BANDS` at run time, and its age check is a four-word vocabulary | Reverted `tidy/cli.py` to the pre-fix strings with the test in place, cleared both `__pycache__` directories and ran with `PYTHONDONTWRITEBYTECODE=1`: `Ran 69 tests ... FAILED (failures=1)`, the single failure being `AssertionError: Regex didn't match: '\\brecent\\b' not found in ...` — the whole old help text is in the failure message. Restored, `Ran 69 tests ... OK` |

## Deviations from the plan

None in substance. Two notes on how the steps were carried out:

1. **Plan steps 1 and 2 were made in one edit and one commit** rather than two, because they are
   two arguments of the same call and splitting them would have produced a commit whose help
   output contradicted itself. The plan does not require a commit per step.
2. **Step 4's revert was done with `git checkout <trunk> -- tidy/cli.py`** rather than a stash,
   which reverts exactly the file the two strings live in and leaves the new test in place. The
   plan's two hazards were both honoured: `tidy/__pycache__` and `tests/__pycache__` were removed
   and `PYTHONDONTWRITEBYTECODE=1` was set, and the reverted file was read back — `grep -n
   "extension-to-folder\|by file type" tidy/cli.py` printed lines 23 and 25 — before the suite was
   run.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 69 tests ... OK`, on the branch head after the last commit |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 9 items, 10 documents, 0 errors 0 warnings |
| `every-criterion-has-a-test` | **pass** | AC1 and AC3 each name a test function; AC2 and AC4 each name an exact command with its output. No criterion is carried by reading the code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0003 wi/BUG-0003` → exit 0, "all 2 commit(s) on main..wi/BUG-0003 name BUG-0003". It had failed earlier in this execution for a reason that is not about these commits — see `## What I did not do`, item 3 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..wi/BUG-0003 -- tidy tests` is three hunks: the two strings (plan steps 1-2, AC1-AC3), and the test file's imports/docstring plus the new test (plan step 3, AC4). Nothing else |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0. It reports "checked no documents changed since main", which is correct: this branch changes no file under `docs/`. ADR-0008 and the overview were linted on `main` when `plan` wrote them |

## What I did not do

1. **The extension table is still unguarded in the direction this item guards the bands.** The
   help text names no extensions — it points at `README.md` — so there is nothing for a test to
   compare. ADR-0008 records this and says what should happen if a later item makes the help list
   them. It is a known gap, not an oversight.
2. **`README.md` was not touched**, per the plan's assumption. It already describes what the new
   epilog summarises. BUG-0005, which is open, is about a different gap in the same file.
3. **`check-commit-refs` reported a false failure at the start of this execution**, and it is
   worth recording because it is a defect in the toolkit rather than in this item. At the
   `planned → in-progress` transition the branch had just been created and held zero commits, so
   `main..wi/BUG-0003` was empty; the script read that as "already merged into `main`" and printed
   advice to rewind a merge that never happened. The gate does not block that move, so nothing was
   lost. The same false report was recorded against BUG-0002 (`review.md` Finding 5) and predicted
   to recur; it has. One condition would fix it: when the branch head equals the trunk head, say
   "no commits yet" instead.
4. **Nothing was fixed that BUG-0003 did not ask for.** BUG-0004 and BUG-0005 are both open and
   both were left alone. `git diff --stat main..wi/BUG-0003` lists six files: two under `tidy/`
   and `tests/`, and four the tracker wrote.
