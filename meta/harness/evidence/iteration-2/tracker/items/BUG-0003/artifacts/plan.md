# Plan — BUG-0003 --help still says files are sorted by type alone, after age routing landed

## Problem

`python3 -m tidy --help` describes the tool as sorting files "into subfolders chosen by file
type", and points the reader at "the extension-to-folder table" as though there were one
[src: tidy/cli.py:22; src: tidy/cli.py:24]. Age routing landed with WI-0002: a destination is
now `<band>/<type>/<name>`, the band comes from the file's age, and `tidy/rules.py` holds two
tables [src: WI-0002 AC1; src: tidy/rules.py; src: docs/architecture/overview.md]. So a user who
reads only `--help` is not told that age takes part at all, and is not warned that `recent/` and
`old/` will appear at the top level of the folder they just tidied. The change is for that
reader, and it is constrained on three sides: WI-0001 AC1's requirements of `--help` must survive
[src: BUG-0003 AC3], the text must agree with `README.md` §"Where each file goes"
[src: BUG-0003 AC2; src: README.md], and the regression test may not pin the wording
[src: BUG-0003 AC4]. No behaviour changes: this item moves no file differently and returns no
different exit code.

## Approach

Two literal strings in `build_parser` are rewritten, and one test is added. ADR-0008 is the only
design choice the item forces, and it is about the *guard*, not the wording: the help text stays
prose rather than being generated from `DEFAULT_BANDS`, and the connection between the text and
the data lives in the test suite instead — `tests/test_cli.py` reads `DEFAULT_BANDS` and asserts
that every band name it declares occurs in the help output [src: ADR-0008]. The alternative,
building the sentences from the tables, is rejected there for a reason WI-0003 makes concrete:
`build_parser` runs before `parse_args`, so under user-supplied rules a generated help text would
describe the built-in defaults during a run that used something else [src: ADR-0008;
src: tidy/cli.py:52].

The wording this plan settles, in full. **Description:**

```
Sort the files sitting directly in a folder into subfolders chosen from how old each file is
and what kind of file it is.
```

**Epilog:**

```
Without --apply, tidy previews only: it prints every move it would make and changes nothing on
disk. Every file that moves lands in <band>/<type>/: the band is recent or old, chosen from when
the file was last modified, and the folder inside it comes from the file's extension. Both rule
tables are in README.md. Subfolders are never entered or moved, names beginning with '.' are
left alone, and no file is ever overwritten.
```

Three things about that epilog are deliberate. Its first sentence and its last are unchanged, so
`previews` and `changes nothing on disk` — the substrings the codified form of WI-0001 AC1
asserts [src: tests/test_cli.py:24; src: tests/test_cli.py:25] — survive word for word. "Both
rule tables are in `README.md`" replaces "The extension-to-folder table", which is what AC2 asks
for [src: BUG-0003 AC2]. And the middle sentence is the same shape as `README.md`'s own opening
line in §"Where each file goes", so a reader who follows the pointer meets a description they
recognise [src: README.md].

Layering is untouched. `cli.py` keeps the responsibilities the overview gives it, no module gains
an import, and `planner.py` remains the only place a destination is decided
[src: ADR-0002; src: docs/architecture/overview.md].

## Steps

1. **`tidy/cli.py` — rewrite the `description`.** Replace the two-line string at lines 22-23 with
   the description quoted under `## Approach`, keeping the existing implicit-concatenation style
   and the 96-column margin the file uses. Afterwards `python3 -m tidy --help` prints a first
   paragraph naming both how old a file is and what kind it is, and the word `type` no longer
   appears alone as the reason for a destination.

2. **`tidy/cli.py` — rewrite the `epilog`.** Replace the four-line string at lines 24-27 with the
   epilog quoted under `## Approach`. The first sentence (`Without --apply, ... changes nothing
   on disk.`) and the final sentence (`Subfolders are never entered or moved, ...`) are copied
   across unaltered; only the middle changes. Afterwards the help output contains `recent`, a
   standalone `old`, `last modified`, and no occurrence of `extension-to-folder`.

3. **`tests/test_cli.py` — add the regression test.** At the top of the file add `import re` and
   `from tidy.rules import DEFAULT_BANDS`, and add `BUG-0003 AC1 and AC3` to the module
   docstring's list of what this file covers. Inside the existing `HelpAndModeTests` class, add:

   ```python
   def test_help_says_age_chooses_the_band_and_names_every_band(self):
       result = run("--help")
       self.assertEqual(result.status, 0)                                  # BUG-0003 AC1
       for band, _bound in DEFAULT_BANDS:
           self.assertRegex(result.stdout, r"\b%s\b" % re.escape(band))
       self.assertTrue(any(re.search(r"\b%s\b" % word, result.stdout)
                           for word in ("modified", "age", "aged", "older")))
   ```

   The band names come from the table rather than from a literal list, which is what makes this a
   guard on the claim rather than on the wording [src: ADR-0008; src: BUG-0003 AC4]. The
   age-vocabulary set deliberately excludes `old`, because `old` is already asserted as a band
   name and reusing it would let the band assertion satisfy the age assertion for free. Add
   `# BUG-0003 AC3` beside the existing `test_help_names_folder_apply_and_default`, whose four
   assertions are what AC3 asks be kept true; do not change that test's assertions. Afterwards
   `python3 -m unittest discover -s tests -t . -q` passes.

4. **Show the new test fails against the unfixed help text.** Revert steps 1 and 2 only — the two
   strings — in a scratch copy or a stash, and confirm that
   `test_help_says_age_chooses_the_band_and_names_every_band` fails while every other test in the
   file still passes; then restore. Record both outputs in `impl-report.md`. Two hazards, both of
   which have produced a false pass in this project before: run with `PYTHONDONTWRITEBYTECODE=1`
   and delete `tidy/__pycache__` and `tests/__pycache__` first, because a same-length edit can
   leave a stale `.pyc` serving the old code; and read `tidy/cli.py` back to confirm the revert is
   actually in the file before running.

5. **Run the gates and report.** From the repository root:
   `python3 -m unittest discover -s tests -t . -q`, `python3 -m compileall -q tidy tests`,
   `.claude/agile-skills/scripts/lint-claims --changed-since main`, and
   `.claude/agile-skills/scripts/validate-workspace .`. Paste the actual `python3 -m tidy --help`
   output into `impl-report.md`, since the item's evidence is what a reader sees.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `--help` exits 0 and states that a file's **age** takes part in choosing where it goes, naming both `recent` and `old` | 1, 2, 3 | `HelpAndModeTests.test_help_says_age_chooses_the_band_and_names_every_band`: `status == 0`, a word-boundary match for each band name in `DEFAULT_BANDS`, and a match for one of `modified`/`age`/`aged`/`older`. Plus the verbatim `python3 -m tidy --help` output pasted into `impl-report.md` |
| AC2 — the output no longer implies a single rule table | 2 | The epilog's "Both rule tables are in README.md", read against `README.md` §"Where each file goes", which documents a band table and a type table. Checkable as `python3 -m tidy --help \| grep -c extension-to-folder` → `0` |
| AC3 — everything WI-0001 AC1 requires of `--help` is still true | 2, 3 | `HelpAndModeTests.test_help_names_folder_apply_and_default`, unchanged and still passing: `folder`, `--apply`, `previews`, `changes nothing on disk`. Step 2 preserves the two epilog phrases it reads, which `git diff tidy/cli.py` shows |
| AC4 — a regression test asserts AC1 and AC3, fails on the old wording, and does not restate the help text as a literal | 3, 4 | The new test contains no sentence from the help output; its expected band names are read from `tidy.rules.DEFAULT_BANDS` at run time. Step 4 records the test failing against the reverted strings, which is what distinguishes a regression test from one that happens to pass |

## Assumptions

- **The band assertion uses a word boundary, not a substring.** `old` occurs inside `folder`, so
  `assertIn("old", stdout)` passes against today's broken help text and would guard nothing
  [src: run: python3 -m tidy --help | grep -c 'old' → exit 0, 5 matches; src: run: python3 -m tidy
  --help | grep -c '\bold\b' → exit 1, 0 matches]. `assertRegex` with `\b...\b` is the form. Reversing to plain substring
  matching costs one line and loses the guarantee, so it should not be reversed; it is recorded
  here because it is a choice a reader would otherwise take for a stylistic one.
- **The age vocabulary is the fixed set `modified`, `age`, `aged`, `older`.** Any of them
  satisfies AC1's "a word for age"; none of them is a band name. Reversing — widening the set, or
  replacing it with a check that `README.md`'s wording appears — is one line in one test, with no
  production consequence.
- **`README.md` is not touched.** Its §"Where each file goes" already describes exactly what the
  new help text summarises, and BUG-0003 names it as the standard the help should agree with
  [src: BUG-0003; src: README.md]. The document is right and the code is being brought to it.
  Reversing is one sentence in a file no code reads.
- **The two strings stay in `build_parser` rather than moving to module constants** beside
  `PREVIEW_BANNER` and `APPLY_BANNER` [src: tidy/cli.py:15; src: tidy/cli.py:16]. Those two are
  constants because `main` and the tests both need them; nothing outside `build_parser` reads the
  description or the epilog. Reversing is a cut and paste within one file.

## Decisions and ADRs

| decision | where |
|----------|-------|
| The help text stays prose in `cli.py` and is guarded by a test that reads `DEFAULT_BANDS`, rather than generated from the tables | ADR-0008 (new), `## Decision` |
| Generating the text from the tables is rejected, and why WI-0003 makes that decisive | ADR-0008 `## Options considered`, option A |
| Pinning the wording with a literal assertion is rejected | ADR-0008 option C; `BUG-0003 AC4` |
| The exact description and epilog wording | `## Approach` above — settled here, as BUG-0003 `## Expected behaviour` asks |
| Word-boundary matching; the age vocabulary; `README.md` untouched; the strings stay in `build_parser` | `## Assumptions` above |

`docs/architecture/overview.md` goes to version 6 in this execution: one sentence in
`## Where the remaining item will touch this`, recording that ADR-0008 leaves WI-0003 a test that
will object when the help text and the tables disagree. Nothing else about the document changes,
because nothing about the shape of the system does.

`tracker/project.yaml` already names a real test and lint command, both set by `plan` for WI-0001
and both re-run in step 5; this execution does not change it [src: tracker/project.yaml;
src: ADR-0004].

## Scaffolding

none.

## Risks

- **The `old`-inside-`folder` trap.** It is the one way this item can be delivered with a test
  that proves nothing, and it is invisible in review: the assertion reads correctly and passes
  against the unfixed code. Step 4 is what catches it if step 3 is written carelessly — a
  substring test does not fail against the reverted strings.
- **The guard covers band names and nothing else.** If a later item makes the help text list
  extensions, `DEFAULT_RULES` gets no such protection, and the text can go stale again in the way
  BUG-0003 describes [src: ADR-0008].
- **`argparse` re-wraps the description and epilog** to the terminal width, so the help output has
  no stable line structure. Every assertion here is over words in the whole capture rather than
  over lines, which is why `COLUMNS` cannot affect the result; a future assertion written against
  a line would be fragile [src: tests/cli_support.py].
- **AC3 is a constraint on prose the tests read as substrings.** An incidental reword of the
  epilog's first or last sentence while editing the middle would fail
  `test_help_names_folder_apply_and_default` — which is the guard working, but it is the likeliest
  way step 2 goes wrong.

## Out of scope for this item

- Generating the help text from the rule tables. ADR-0008 records it as considered and rejected;
  reopening it is WI-0003's business if it turns out to need it.
- BUG-0004 (one dangling symlink stops the whole folder) and BUG-0005 (the README does not say
  what `tidy` exits with when every move fails). Both are open, BUG-0005 touches documentation of
  the same command, and neither is touched here.
- WI-0003 (user-supplied rules), which changes where the tables come from.
- `README.md`, and any change to what the tool does: no destination, no exit status and no output
  line changes in this item.
