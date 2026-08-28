# Verification report — WI-0003

Verified-commit: d870cb1649333e90af727b26cf5d8b1c1f483b06

## Verdict

**Pass.** All twelve acceptance criteria are met. Every verdict below rests on a command this
skill ran against the branch head and its quoted output, not on `impl-report.md`.

The evidence was gathered by building the sample folder `S` from **the item's own preamble**
(`/tmp/v/mkS.py` — six files, `taxes.pdf` aged 400 days with `os.utime`, everything else written
now) and driving `python3 -m tidy` as a real command, outside the test suite. The rule files
`F1`–`F6` were written from the item's own descriptions of them, and kept beside `S` rather than
inside it. The suite was then used separately, as the sensitivity check in §Test sensitivity.

No defect was found, and no bug item was filed.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 -m tidy /tmp/v/S`, then `find` before/after, then `--apply` | preview printed exactly the item's table: `move   budget.csv -> recent/spreadsheets/budget.csv` / `move   holiday.jpg -> recent/images/holiday.jpg` / `leave  notes.xyz   [no rule for '.xyz']` / `move   report.pdf -> recent/documents/report.pdf` / `move   taxes.pdf -> old/documents/taxes.pdf`, exit 0. `diff before.txt after.txt` empty. After `--apply` the tree is `recent/spreadsheets/budget.csv`, `recent/images/holiday.jpg`, `recent/documents/report.pdf`, `old/documents/taxes.pdf`, `notes.xyz`, `.hidden.jpg` | `.hidden.jpg` produced no line and did not move. The suite's second half of this criterion checked separately: `git diff -U0 main..HEAD -- tests/` removes lines in **one** pre-existing file, `tests/test_rules.py`, and every removal is paired with the identical assertion prefixed `BUILT_IN.` — `band_for(0), "recent"` → `BUILT_IN.band_for(0), "recent"`, and so on for all twelve. `test_cli.py`, `test_apply.py`, `support.py` and `cli_support.py` have **zero** removed lines. No expected value anywhere was altered, which is the reviewer's test that `plan` Risk 1 asked for. `python3 -m unittest tests.test_rules.BandTableTests tests.test_rules.ExtensionTableTests tests.test_apply tests.test_planner.ScanTests` → `Ran 26 tests / OK` |
| AC2 | **pass** | `python3 -m tidy /tmp/v/S --rules F1.ini` where `F1` is `[types]\n.csv = data` | `move   budget.csv -> recent/data/budget.csv`, and the other four lines byte-identical to AC1's | `.hidden.jpg` still absent; the "other five files" are the four printed plus the hidden one, which AC1 gives no line for either |
| AC3 | **pass** | same, with `F2` = `[types]\n.xyz = notes` | `move   notes.xyz -> recent/notes/notes.xyz` where AC1 gives `leave  notes.xyz   [no rule for '.xyz']`; the other four lines unchanged | |
| AC4 | **pass** | `--rules F1.ini > o1.txt`, then `--rules F3.ini > o3.txt` over the same `S`, no `--apply` between; `diff o1.txt o3.txt` | `1c1 / < move   budget.csv -> recent/data/budget.csv / --- / > move   budget.csv -> recent/tables/budget.csv` — exactly one differing line | `find` afterwards confirmed `S` still held all six original files, so nothing moved between the runs |
| AC5 | **pass** | `--rules F4.ini` (`newer = current`, `older = archive`, `boundary-days = 90`); then three files added at 90 days, 90 days − 60 s and 90 days + 60 s and the run repeated | four movable files to `current/…` except `move   taxes.pdf -> archive/documents/taxes.pdf`. Boundary files: `exactly.pdf -> archive/documents/exactly.pdf`, `under.pdf -> current/documents/under.pdf`, `over.pdf -> archive/documents/over.pdf` | The boundary keeps WI-0002 AC4's sense: the older band wins at the boundary |
| AC6 | **pass** | `--rules F1.ini` (types only) and `--rules F4.ini` (bands only) | `F1` → `move   taxes.pdf -> old/documents/taxes.pdf`, the built-in bands. `F4` → `move   budget.csv -> current/spreadsheets/budget.csv`, the built-in type table | Both directions of the layering |
| AC7 | **pass** | a `[bands]` with four keys, and one with a single `newer` key, each run in **both** modes; and the band names in `F4`'s output in both modes | three bands → `tidy: …bad-threebands.ini cannot be used: 'middling' in [bands] is not a setting tidy has; there are exactly two bands, so [bands] takes 'newer', 'older' and 'boundary-days' and nothing else`. One band → `…is missing 'older'; all of 'newer', 'older' and 'boundary-days' are required when the section is present`. Both: exit 2, stdout 0 bytes, 1 stderr line, `S` unchanged. Under `F4` the set of first path components is exactly `{current, archive}` in both modes, and `ls S` after apply is `archive current notes.xyz` | |
| AC8 | **pass** | 12 rule files covering all six classes, each run in **both** modes; `sha256sum` over `S` before and after all twelve `--apply` runs | every one: `rc=2 stdout=0 bytes stderr_lines=1 S=unchanged`. The twelve messages are quoted in §Negative and boundary cases. `diff sum-before.txt sum-after.txt` empty — `S` byte-for-byte identical after twelve rejected `--apply` runs | Classes covered: unparseable; destination with `/`; empty destination; extension without `.`; band count three and band count one; boundary non-numeric, zero and negative; band name empty, containing `/`, and equal to the other |
| AC9 | **pass** | `F5` = `[types]\n.pdf = papers` with `S/recent/papers/report.pdf` pre-existing and holding different bytes; both modes | both printed `move   report.pdf -> recent/papers/report (2).pdf   [recent/papers/report.pdf exists]`. After apply: pre-existing file size 30 → 30, sha256 identical, contents still `the one that was already there`; the suffixed file holds `contents of report.pdf` | |
| AC10 | **pass** | `--rules F1.ini` over an `S` with `already-filed/pic.jpg` added; both modes; then `F2` against an `F2` with `.xyz` removed | `.hidden.jpg` matched 0 lines of either mode's stdout and is still at `S/.hidden.jpg`. `already-filed` matched 0 lines; `already-filed/pic.jpg` sha256 unchanged after apply. `leave  notes.xyz   [no rule for '.xyz']` still printed under `F1`. Removing `.xyz` from the rule file turned `move   notes.xyz -> recent/notes/notes.xyz` back into `leave  notes.xyz   [no rule for '.xyz']` | No catch-all folder appeared in any run |
| AC11 | **pass** | for each of `F1`, `F2`, `F4`, `F5`, `F6`: capture PREVIEW's `(name, destination)` pairs, `--apply` over the unchanged `S`, then check each promised path exists and each source name is gone | all five: every promised destination present, no source name left → `preview and apply agree`. `F6` (`.pdf = old`): `taxes.pdf -> old/old/taxes.pdf` and `report.pdf -> recent/old/report.pdf`, both landed as printed | The band-name collision resolves as `plan` assumption A1 says, and `README.md` documents it, which is what AC11 and AC12 jointly require |
| AC12 | **pass** | extracted the README's `ini` block with a script and **ran it** against `S`; then checked each required statement in the text | The README's own example produced `move   budget.csv -> current/data/budget.csv` and `move   taxes.pdf -> archive/documents/taxes.pdf` — AC2's redirect and AC5's band rename, exactly as the prose beside it claims. The text states: `--rules PATH` and "There is no default location"; the format and the worked example; "They layer on top, and yours win" and "You cannot remove a built-in mapping"; "There are exactly two bands, whatever you call them"; "**one line on stderr** … **nothing on stdout**, and an **exit status of 2**"; and `old/old/report.pdf`. The exit-status paragraph now names `--rules` | The README's quoted error line is the real one: I produced `tidy: …/bad-nodot.ini cannot be used: 'csv' in [types] is not an extension: it must begin with a '.'`, character-identical to the README's example after the path |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | I ran `python3 -m unittest discover -s tests -t . -q` on `d870cb1` → `Ran 157 tests in 0.161s` / `OK`, exit 0 |
| `lint-clean` | **pass** | I ran `python3 -m compileall -q tidy tests` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 10 item(s), 13 document(s)` / `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | Every row above names a command I ran and quotes its output. The sample folder and the six rule files were built from the item's preamble, not from the test suite; the CLI was driven as a subprocess |
| `negative-cases-exercised` | **pass** | See §Negative and boundary cases: 12 malformed rule files × 2 modes, three files at the age boundary, a pre-existing destination file, a missing rule file, a rule path that is a directory |
| `tests-would-fail-without-the-change` | **pass**, advisory | Seven independent breakages, each restored afterwards; see §Test sensitivity |

## Negative and boundary cases exercised

**Twelve malformed rule files, each in both modes** (24 runs). Every one: exit 2, `stdout` 0
bytes, exactly one `stderr` line naming the file and the problem. The messages, verbatim:

```
tidy: …/bad-bandempty.ini cannot be used: 'newer' in [bands] has no band name
tidy: …/bad-bandsame.ini cannot be used: 'newer' and 'older' in [bands] are both 'same'; the two bands need different names
tidy: …/bad-bandslash.ini cannot be used: 'newer' in [bands] names a band 'a/b' that is more than one folder deep; a band is a single folder name
tidy: …/bad-boundarynan.ini cannot be used: 'boundary-days' in [bands] is 'soon', which is not a number of days
tidy: …/bad-boundaryneg.ini cannot be used: 'boundary-days' in [bands] is '-30'; it must be more than zero
tidy: …/bad-boundaryzero.ini cannot be used: 'boundary-days' in [bands] is '0'; it must be more than zero
tidy: …/bad-destempty.ini cannot be used: '.csv' in [types] has no folder to send it to
tidy: …/bad-destslash.ini cannot be used: '.csv' in [types] sends 'work/pdfs' somewhere more than one folder deep; a destination is a single folder name
tidy: …/bad-nodot.ini cannot be used: 'csv' in [types] is not an extension: it must begin with a '.'
tidy: …/bad-oneband.ini cannot be used: [bands] is missing 'older'; all of 'newer', 'older' and 'boundary-days' are required when the section is present
tidy: …/bad-threebands.ini cannot be used: 'middling' in [bands] is not a setting tidy has; there are exactly two bands, so [bands] takes 'newer', 'older' and 'boundary-days' and nothing else
tidy: …/bad-unparseable.ini cannot be used: File contains no section headers. file: '…/bad-unparseable.ini', line: 1 'this is not an INI file at all\n'
```

Every one of those is a single line — the multi-line `configparser` string is collapsed, which
AC8 needs and which is easy to get wrong.

**`S` after all twelve `--apply` rejections:** `diff` of `sha256sum` listings before and after is
empty. Nothing moved, nothing was created, no byte changed.

**The age boundary**, under a user-supplied `boundary-days = 90`: `exactly.pdf` → `archive`,
`under.pdf` (60 s younger) → `current`, `over.pdf` (60 s older) → `archive`.

**A destination that already exists:** `F5` with `recent/papers/report.pdf` present — `(2)` in
both modes, and the pre-existing file's sha256 unchanged.

**Two rule paths that are not rule files:**

```
tidy: /tmp/v/absent.ini cannot be used: No such file or directory     (exit 2)
tidy: /tmp/v cannot be used: Is a directory                            (exit 2)
```

**A file matching neither the rule file nor the built-in table:** `leave` line, no catch-all
folder, under rules as without them.

## Test sensitivity check

Seven behaviours disabled one at a time on a copy, the suite run, then the file restored. The
working tree was confirmed identical to `d870cb1` afterwards (`git diff --quiet HEAD` → clean).

| behaviour disabled | suite result |
|--------------------|--------------|
| `merge` ignores the user's `[types]` entries | `FAILED (failures=21, errors=1)` |
| `merge` ignores the user's `[bands]` section | `FAILED (failures=11)` |
| `build_plan` ignores its `ruleset` parameter | `FAILED (failures=16, errors=1)` |
| the loader stops rejecting unknown sections and dotless extensions | `FAILED (failures=7)` |
| the loader stops rejecting a third band | `FAILED (failures=3)` |
| `cli.py` ignores `--rules` and never rejects a rule file | `FAILED (failures=27, errors=1)` |
| `README.md`'s "Your own rules" section deleted | `FAILED (failures=6)` |
| everything restored | `OK` |

No behaviour this item delivers survives its own removal silently. The README check is worth
naming: AC12 is a documentation criterion, and deleting the section it asks for does fail the
suite, so the criterion is not self-certifying.

## Defects found

**None.** No criterion of this item failed, and nothing was found in behaviour delivered by
another item, so no bug was filed and no send-back was made.

Four things the implementation report **declared**, which I reproduced and confirmed are not
criterion failures:

1. **`boundary-days = inf` is accepted.** `--rules` with `boundary-days = inf` gives
   `move   budget.csv -> a/spreadsheets/budget.csv` — everything falls in the newer band. AC8
   requires rejecting a boundary that is "not a positive number of days", and `inf` **is** a
   positive number, so this is inside the criterion rather than outside it. Not a defect; noted
   because a reader would otherwise wonder.
2. **A well-formed but meaningless entry is accepted.** `.csv = .csv` gives
   `move   budget.csv -> recent/.csv/budget.csv`. `plan`'s own Risks section predicted exactly
   this and called it "odd, not wrong"; no criterion constrains it, and the preview shows it.
3. **A `#` part-way through a line is part of the value.** `.csv = data  # note` gives
   `move   budget.csv -> recent/data  # note/budget.csv`, and `--apply` creates that folder, so
   the two modes still agree. `README.md` tells the user to put comments on their own line.
4. **ADR-0008's grep needs its word-boundary form.** `cli.py`'s six imports are `argparse`, `os`,
   `sys`, `.apply`, `.planner`, `.ruleset_file`; `grep -nE "^(from|import).*\brules\b" tidy/cli.py`
   exits 1 with no output. `cli.py` imports no rule table, which is what ADR-0008 decided.
   `--help` still names both built-in bands and the word `modified`, so ADR-0008's guard is green.

## Not verified, and why

- **Behaviour on a non-POSIX filesystem or on Windows.** `os.altsep` is checked in the loader's
  separator test, but this run was on Linux where `os.altsep` is `None`, so the `\`-as-separator
  path is unexercised. Nothing in the criteria asks for it; recorded so it is not mistaken for
  covered.
- **`--rules` against a file the process may not read.** I exercised a missing path and a
  directory, both of which give the intended one-line exit 2. A permission-denied file takes the
  same `OSError` branch as those two by inspection, but I did not construct one — the run is
  under a user for whom `chmod 000` is not reliably enforced.
- **Concurrent modification of `S` during a run.** Out of scope for every criterion, and the
  no-recursion invariant makes it uninteresting here.
- **Anything about `apply.py`.** It is byte-for-byte unchanged on this branch
  (`git diff main..HEAD -- tidy/apply.py` is empty), so WI-0001's and BUG-0002's verification of
  it still stands and this run did not re-do it.
- **The diff was read against the plan** (step 6) and produced no finding: 4 files under `tidy/`,
  249 insertions, and every hunk traces to a plan step — `cli.py`'s diff is exactly step 5's
  three edits, `apply.py` is untouched, and `tidy/ruleset_file.py` is step 4's new module. No
  unrequested scope was found.
