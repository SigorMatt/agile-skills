# Verification report — BUG-0005

Verified-commit: 4835edfcb24c8af424332b754298ea19e704f3d8

## Verdict

**Pass.** All three acceptance criteria are met, each demonstrated by a command run here rather
than by anything the implementation report claims. The item goes to `in-review`.

The check was built the way the criteria ask for it: AC1 and AC2 are claims about a paragraph, so
they were settled by running the tool and reading what it printed against what the paragraph
promises — not by reading the diff and agreeing with it. AC2 in particular was verified as a claim
about **behaviour**, not only as a claim about an unchanged diff: every exit status the paragraph
enumerates was produced on this branch, including all four of the exit-2 cases.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| **AC1** — the paragraph describes the exit code of a run in which no file moved | **pass** | The item's own `## Steps to reproduce`, rebuilt under `.harness/vfy/allfail`: `mkdir -p …/recent`, two files, `chmod 0500 …/recent`, then `python3 -m tidy .harness/vfy/allfail --apply; echo "EXIT: $?"` and `find … -type f` | `tidy: could not create the folder for recent/documents/doc.pdf: [Errno 13] Permission denied: …; doc.pdf was left where it is`, the same for `photo.jpg`, `move` lines for both, `EXIT: 1`; `find` listed `.harness/vfy/allfail/doc.pdf` and `.harness/vfy/allfail/photo.jpg` — both still at the top level | The run prints a `move` line for each file, so both **were going to move**; neither did; the run exits 1. `README.md:38-39` now reads "and 1 when a file that was going to move could not be — whether that is one of them, some of them, or all of them", and "all of them" is this run named explicitly. A reader predicts 1 by reading the clause, not by inferring from a clause that excludes the case, which is what the old wording forced. One competing reading was considered and rejected — see `## Defects found` |
| **AC2** — 0, 2 and the partial case still described correctly | **pass** | Two checks. (a) `git diff --word-diff=plain main..wi/BUG-0005 -- README.md`. (b) every status the paragraph claims, produced on this branch: empty folder; a folder with `notes.xyz` (no rule) and `photo.jpg`; a path that does not exist; a regular file; a folder at `chmod 000`; a malformed `--rules` file; and a partial failure built with `recent/documents` existing at mode `0o500` so one file moves and one cannot | (a) `be used — and 1 when [-some-]{+a+} file {+that was going to move+} could not be [-moved while others were.-]{+— whether that is one of them,+} {+some of them, or all of them.+}` — every changed word is inside the third clause; the 0 clause, the 2 clause and the closing sentence are word-identical. (b) `Nothing to do: no files to move in .harness/vfy/empty.` → `EXIT: 0`; `leave notes.xyz [no rule for '.xyz']` + `move photo.jpg …` → `EXIT: 0`; `tidy: .harness/vfy/nosuch is not a folder` → `EXIT: 2`; `tidy: .harness/vfy/afile is not a folder` → `EXIT: 2`; `tidy: .harness/vfy/unreadable cannot be read: Permission denied` → `EXIT: 2`; `tidy: .harness/vfy/bad.ini cannot be used: File contains no section headers…` → `EXIT: 2`; `tidy: doc.pdf could not be moved to recent/documents/doc.pdf: [Errno 13] Permission denied…` → `EXIT: 1` with `find` showing `doc.pdf` at the top level and `recent/images/photo.jpg` landed | The criterion asks whether the other three descriptions are **still correct**, and the word-diff proves they are unchanged while the runs prove they are true. All four of the 2 cases the paragraph enumerates — does-not-exist, not-a-folder, cannot-be-read, and the `--rules` file WI-0003 added — were triggered. BUG-0001 AC2, the criterion this one is checkable against, is about the exit-2 clause: it is word-identical across the diff. WI-0003 AC12's requirement that this paragraph name `--rules` also survives — the string `--rules` is in the untouched second clause. The partial case is not merely still described, it is now the **first** thing the new clause says ("one of them") |
| **AC3** — a regression test pins the all-fail exit 1, and skips rather than fails where mode `0o500` is not enforced | **pass** | Three checks. (a) `python3 -m unittest tests.test_cli.AllMovesFailExitStatusTests -v`. (b) the skip path, exercised by temporarily changing the test's own `os.chmod(band, 0o500)` to `0o700` so the probe write succeeds, then restoring the file. (c) sensitivity: `tidy/cli.py`'s `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0` temporarily replaced by `return 0`, then restored | (a) `test_a_run_in_which_every_move_fails_exits_1 … ok` / `Ran 1 test … OK`, exit 0 — **`ok`, not `skipped`**, so the guard did not swallow the case here. (b) `… skipped 'the write succeeded at mode 0o500: running as root, or on a filesystem that does not enforce the mode'` / `OK (skipped=1)` — it **skips**, and the run is still OK rather than a failure. (c) `AssertionError: 0 != 1` at `self.assertEqual(result.status, 1)` / `FAILED (failures=1)` | (b) is the half of AC3 that is easy to assert and hard to demonstrate, and it was demonstrated rather than read: with the blocking mode removed the test does not quietly pass, it declares itself skipped. `git status --porcelain` reported both files clean after each restore |

All three boxes — AC1, AC2 and AC3 — are now ticked in `item.md`, each against the evidence in its row.

## Gates

Run by this skill, on `4835edf`, the head of `wi/BUG-0005`.

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 158 tests in 0.160s / OK`. The implementation report claims 158 and `Ran 158` is what came back, so the report's gates were not run against an earlier state |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 10 items, 14 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | Every row of `## Criteria` names a command run in this execution and quotes its real output. No row cites `impl-report.md`. AC1's and AC2's checks were derived from the criteria before the diff was read, which is why AC2's evidence is seven runs of the tool and not only a diff — the criterion says "correctly", and a diff can only show "unchanged" |
| `negative-cases-exercised` | **pass** | Every error and boundary the paragraph names was triggered, not read about: a folder that does not exist, a path that is a regular file, a folder at `chmod 000`, a `--rules` file that is not valid INI, an empty folder, a file with no rule, an all-fail run, and a partial-failure run. Listed with their output below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Two independent mutations, both restored: the exit predicate replaced by `return 0` → `AssertionError: 0 != 1`; and the blocking mode relaxed to `0o700` → `skipped`, not a spurious pass |

## Negative and boundary cases exercised

| case | command | result |
|------|---------|--------|
| every intended move fails | `python3 -m tidy .harness/vfy/allfail --apply` with `recent/` at `0o500` | `EXIT: 1`, two `could not create the folder …; <file> was left where it is` lines, both files unmoved |
| one move fails, one succeeds | `python3 -m tidy .harness/vfy/partial --apply` with `recent/documents/` existing at `0o500` | `EXIT: 1`, `doc.pdf could not be moved to recent/documents/doc.pdf: [Errno 13] Permission denied`, `photo.jpg` landed at `recent/images/photo.jpg` |
| nothing to do | `python3 -m tidy .harness/vfy/empty --apply` | `Nothing to do: no files to move in .harness/vfy/empty.`, `EXIT: 0` |
| a successful run that leaves a file where it is | `python3 -m tidy .harness/vfy/leaves --apply` with `notes.xyz` and `photo.jpg` | `leave notes.xyz [no rule for '.xyz']`, `move photo.jpg …`, `EXIT: 0` |
| the folder does not exist | `python3 -m tidy .harness/vfy/nosuch --apply` | `tidy: .harness/vfy/nosuch is not a folder`, `EXIT: 2` |
| the target is not a folder | `python3 -m tidy .harness/vfy/afile --apply` | `tidy: .harness/vfy/afile is not a folder`, `EXIT: 2` |
| the folder cannot be read | `python3 -m tidy .harness/vfy/unreadable --apply` at `chmod 000` | `tidy: .harness/vfy/unreadable cannot be read: Permission denied`, `EXIT: 2` |
| the `--rules` file cannot be used | `python3 -m tidy .harness/vfy/r --rules .harness/vfy/bad.ini --apply` | `tidy: .harness/vfy/bad.ini cannot be used: File contains no section headers…`, `EXIT: 2` |
| the regression test's own skip guard | the test's `os.chmod(band, 0o500)` temporarily made `0o700` | `skipped '…running as root, or on a filesystem that does not enforce the mode'`, `OK (skipped=1)` |

Every fixture was created under `.harness/`, which is git-ignored, and removed afterwards
(`chmod -R 0700 .harness/vfy; rm -rf .harness/vfy`). `git status --porcelain` was empty afterwards.

## Test sensitivity check

`tests.test_cli.AllMovesFailExitStatusTests.test_a_run_in_which_every_move_fails_exits_1` was
attacked twice.

1. **The behaviour removed.** `tidy/cli.py:114`, `return 1 if any(outcome.kind == "failed" for
   outcome in outcomes) else 0`, temporarily replaced by `return 0`. The test failed:
   `AssertionError: 0 != 1` at the line carrying the `# BUG-0005 AC3` marker. `tidy/cli.py` was
   restored from a copy and `git status --porcelain tidy/cli.py` reported no changes.
2. **The condition the test builds removed.** The band folder's mode changed from `0o500` to
   `0o700`, so that the moves would succeed. The test did not pass — it reported `skipped`,
   which is the guard doing exactly what AC3 asks. `tests/test_cli.py` was restored and confirmed
   clean.

The second is the more interesting one: a test whose fixture stops working could otherwise pass
for the wrong reason, and this one refuses to.

## Defects found

**None filed.** One competing reading was examined and deliberately not filed, and one wording
question was checked and found sound. Both are recorded here so a reviewer can take a different
view with the evidence in front of them rather than re-deriving it.

1. **The 0 clause's "some files were left where they are" is echoed word-for-word by a failure
   message on a run that exits 1.** `tidy/apply.py:46` emits `could not create the folder for %s:
   %s; %s was left where it is` for exactly the run AC1 is about, and `README.md:35-36` says
   `0 on success — including when there was nothing to do, and when some files were left where
   they are`. A reader who matches on that phrase rather than on the clause it sits in could
   reach 0 for a run that exits 1.

   Not filed, for two reasons. The 0 clause is governed by **"on success"**, and its two
   "including" items are elaborations of what counts as a success, not independent triggers; the
   all-fail run is visibly not a success — it printed two error lines to stderr. And the new third
   clause names the case unambiguously, so the paragraph does give the right answer to a reader
   who reads it. Nothing here is false, which is the bar for a defect; the risk is that a skimmer
   stops at a familiar phrase.

   It is also not a send-back. AC2 and `plan.md` step 2 both **forbid** this item from touching
   the 0 clause — BUG-0001 AC2 and WI-0003 AC12 are verified against the rest of the paragraph —
   so BUG-0005 could not have fixed it even if it should be fixed. Provenance, if anyone does
   file it: the phrase entered at `1156654` (BUG-0004) and the failure message at `49be3d7`
   (WI-0001), so it belongs to neither item alone.

2. **"a file that was going to move could not be" versus the copied-but-not-removed outcome.**
   `tidy/apply.py:64-68` records `%s was copied to %s but the original could not be removed` as
   `kind="failed"`, so that run exits 1 — and the file *is* at its destination, which reads
   oddly against "could not be [moved]". Checked and sound: ADR-0007 and the comment above that
   line both hold that a file at its destination **and** still at its source is "a duplicate, not
   a completed move", so calling it a move that could not be completed is the project's settled
   position, not a slip. The old wording ("could not be moved") had the identical property, so
   this item neither introduced nor worsened it.

## Not verified, and why

- **That the new clause reads well to a first-time user.** AC1 is decidable — can a reader predict
  the exit code of a specific run — and that was decided. Whether the sentence is *good prose* is
  not a criterion and is not this skill's call. The implementation report volunteers one
  observation about it (the clause-internal em dash sitting inside a sentence whose top-level
  clauses are also em-dash separated); this verification neither endorses nor disputes it, and
  flags it as something `review-close` may want a view on.
- **Behaviour under root, or on a filesystem that does not enforce mode `0o500`.** Every all-fail
  and partial-failure case here depends on the mode being enforced, and it was: the test reported
  `ok` rather than `skipped`, which is the probe telling us so. On a machine where it is not
  enforced, AC1's reproduction and AC3's test would both skip, and this report's AC1 and AC3 rows
  would have no evidence behind them. That is a property of the criteria, which say so themselves,
  not a gap introduced here.
- **The exit-status paragraph against a reader who has not read the rest of the README.** The
  `leave` concept the 0 clause leans on is defined earlier in the document (`README.md:26-29`);
  this verification read the paragraph in the context of the whole file, which is how a user meets
  it.
- **Anything under `tidy/`.** The branch changes no production file — `git diff main..wi/BUG-0005
  --stat` is `README.md | 5` and `tests/test_cli.py | 52` — so there is no new behaviour to verify
  beyond the exit statuses re-confirmed above. `tidy/cli.py` and `tests/test_cli.py` were each
  mutated and restored during this execution, and both were confirmed clean afterwards.
- **One structural caveat about independence.** This verification ran in the same session as the
  implementation, which is a property of how this pipeline is being driven and not a choice made
  here. Every command in this report was re-run by this skill and its real output quoted; AC2's
  evidence was deliberately built from the criterion (seven runs of the tool) rather than from the
  diff the implementation produced, and AC3's guard was attacked in a way the implementation
  report did not try. It is recorded so no reader mistakes the report for two people's work.
