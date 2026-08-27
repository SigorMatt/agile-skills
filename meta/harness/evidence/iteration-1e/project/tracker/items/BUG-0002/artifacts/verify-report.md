# Verification report — BUG-0002

Verified-commit: d8b4c4e89af854a2894097af195a423d24213b0e

## Verdict

**Pass.** All five acceptance criteria are met, each decided by a command run in this session
against the head of `wi/BUG-0002` and quoted below. The bug's own reproduction was re-run by hand
and no longer reproduces: one line on stderr, nothing on stdout, exit 2, and an empty directory
afterwards. One non-blocking finding is recorded under `## Defects found` — a sentence in the test
module's docstring that this change made inaccurate. It fails no criterion and is left for the
reviewer.

Every criterion was decided from its own text before `impl-report.md` was opened. The scratch
fixtures below are mine, not the implementation's: `/tmp/vb2/a` (a mode-500 directory holding a
dataset recorded while it was still writable) and `/tmp/vb2/b` (a mode-500 directory with no
dataset at all, which is the bug's literal reproduction).

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — unwritable store, `person add Ana`: exit 2, nothing on stdout, one stderr line containing the path and no `Traceback` | **pass** | `chmod 500 /tmp/vb2/a; EXPENSES_STORE=/tmp/vb2/a/expenses.json python3 -m expenses person add Ana >out 2>err`, then `wc -c < out`, `wc -l < err`, `grep -c -F <path> err`, `grep -c Traceback err` | `exit=2`; `stdout bytes: 0`; `stderr lines: 1`; stderr verbatim `cannot write /tmp/vb2/a/expenses.json: [Errno 13] Permission denied: '/tmp/vb2/a/.expenses-n_otdx3u.tmp'`; `contains the path: 1`; `contains Traceback: 0` | all four clauses checked separately, not by eye. Run a second time against `/tmp/vb2/b`, an empty mode-500 directory with no dataset — the bug's literal reproduction: `exit=2`, `stdout bytes: 0`, `stderr lines: 1`, `cannot write /tmp/vb2/b/expenses.json: [Errno 13] Permission denied: ...`, `Traceback count: 0` |
| AC2 — the same for `expense add` | **pass** | `EXPENSES_STORE=/tmp/vb2/a/expenses.json python3 -m expenses expense add --amount 12.50 --paid-by Zoe --shared-by Zoe --date 2026-08-01 --description dinner >out 2>err` with the same four measurements | `exit=2`; `stdout bytes: 0`; `stderr lines: 1`; `cannot write /tmp/vb2/a/expenses.json: [Errno 13] Permission denied: '/tmp/vb2/a/.expenses-riuzuxmj.tmp'`; `contains the path: 1`; `contains Traceback: 0` | the payer and sharer are a person who is already recorded, so the refusal comes from the write and not from `add_expense` validating names — otherwise the criterion would pass for the wrong reason |
| AC3 — the previous dataset byte-identical afterwards, no `.expenses-` file left | **pass** | `md5sum` and `wc -c` on the dataset before the two refusals and after them; `ls -a /tmp/vb2/a`; `ls -a /tmp/vb2/a \| grep -c '^\.expenses-'` | before: `c21ac18dc401812361a7da5baec700af`, `66` bytes. After both refused commands: `c21ac18dc401812361a7da5baec700af`, `66` bytes. Listing: `.`, `..`, `expenses.json`; `entries beginning .expenses- : 0` | the hash brackets *two* refusals, not one |
| AC4 — a regression test covers AC1 by making a temporary directory read-only, fails if the handling is removed, and skips when the process can write regardless | **pass** | three separate checks, below | (i) `python3 -m unittest -v tests.test_cli.BUG0002AnUnwritableStoreIsRefusedNotATraceback` → three tests, all `ok`, `Ran 3 tests`, `OK`; the fixture's `TemporaryDirectory`, `self.directory.chmod(0o500)` and `skipTest` are at `tests/test_cli.py:657`, `:666`, `:678`. (ii) `cp expenses/store.py /tmp/vb2/store.branch.py; git show main:expenses/store.py > expenses/store.py` (`grep -c "cannot write"` → `0`, so the handling really is gone) then the same class → `Ran 3 tests`, `FAILED (failures=3)`; restored and `md5sum -c` → `expenses/store.py: OK`. (iii) `sed -i 's/chmod(0o500)/chmod(0o700)/'` on the fixture, making the probe succeed → all three `skipped 'this process writes to a mode-500 directory anyway; nothing to test'`, `OK (skipped=3)`; restored and `md5sum -c` → `tests/test_cli.py: OK` | (iii) is the root case reproduced by construction rather than by becoming root: the criterion's condition is "the test process can write regardless of the permission bits", and that is exactly what the injection creates. The suite reports `OK`, not a failure — which is the point of the criterion |
| AC5 — `python3 -m unittest discover -s tests -t .` exits 0 | **pass** | `python3 -m unittest discover -s tests -t .` | `Ran 123 tests in 1.479s`, `OK`, `exit=0` | run on the restored tree after every injection above; `git status --short` empty and `git rev-parse HEAD` = `d8b4c4e…`, so this is the branch head and not a mutated copy |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 123 tests`, `OK`, run by this skill on `d8b4c4e` |
| `lint-clean` | **skipped** | `tracker/project.yaml:16` is `lint: null`; ADR-0004 records that this project installs nothing and the standard library ships no linter. Nothing ran, so nothing is claimed — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 7 items, 10 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | every row above names a command run in this session and quotes its output; no row cites `impl-report.md`. The criteria were read and the checks designed before that report was opened |
| `negative-cases-exercised` | **pass** | every criterion here *is* a negative case, and each was triggered rather than read about; four further conditions are listed in the next section |
| `tests-would-fail-without-the-change` (advisory) | **pass** | AC4 (ii): with `expenses/store.py` reverted to `main`'s version, the three tests fail, each with `AssertionError: 1 != 2 : expected a refusal; stderr was b'Traceback ... PermissionError: [Errno 13] Permission denied'` |

## Negative and boundary cases exercised

- **The parent directory cannot be created at all.** `EXPENSES_STORE=/tmp/vb2/a/sub/expenses.json`
  with `/tmp/vb2/a` at mode 500 → `exit=2`, `stdout bytes: 0`, `stderr lines: 1`,
  `cannot write /tmp/vb2/a/sub/expenses.json: [Errno 13] Permission denied: '/tmp/vb2/a/sub'`,
  `Traceback count: 0`. This is ADR-0008's first clause — the `mkdir` inside the boundary —
  demonstrated rather than assumed. No criterion covers it.
- **The wrapper did not widen.** With the directory writable again,
  `person add Ana` on a dataset that already has Ana → `Ana is already in the group`, exit 2: an
  ordinary refusal still passes through with its own message and names no path, so
  `ExpensesError` is not being caught and re-wrapped by the new clause.
- **The read path is untouched.** `EXPENSES_STORE=/tmp/vb2/isdir/expenses.json python3 -m expenses
  person list` where the path is a directory → `cannot read /tmp/vb2/isdir/expenses.json:
  [Errno 21] Is a directory: ...`, exit 2 — byte-identical in shape to the bug's own contrast case.
- **Recovery.** `chmod 700` and then `person add Ana` → `added Ana`, exit 0; `person list` → `Zoe`,
  `Ana`. The refusals left the tool working and the earlier record intact, rather than leaving the
  store in a state that needed repair.

## Test sensitivity check

Done twice, in both directions, with the tree restored and checksummed each time:

- **Behaviour removed → tests red.** `git show main:expenses/store.py > expenses/store.py`
  (verified by `grep -c "cannot write" expenses/store.py` → `0`), then the three tests →
  `FAILED (failures=3)`. Restored from a copy taken beforehand; `md5sum -c` → `OK`.
- **Skip condition forced → tests skip, suite stays green.** The fixture's `chmod(0o500)` changed
  to `chmod(0o700)`, so the probe succeeds → `OK (skipped=3)` with the reason printed on each.
  Restored; `md5sum -c` → `OK`.

After both, `git status --short` is empty and `git rev-parse HEAD` is `d8b4c4e89af…`, so every
verdict above stands against the committed branch head.

## Defects found

- **Non-blocking, this item's own diff, no criterion covers it.** `tests/test_cli.py`'s module
  docstring says "each test starts from a store that does not exist yet". That was true of every
  class before this change; `BUG0002AnUnwritableStoreIsRefusedNotATraceback.setUp` records `Zoe`
  before taking the write permission away, so three tests now start from a store that does exist.
  It is a sentence in a test file, not behaviour, and nothing in AC1 to AC5 speaks to it — so it
  is neither a send-back (no criterion of this item fails) nor a bug against another item (the
  sentence was made inaccurate by this diff). It is recorded here for the reviewer to decide.
- Nothing else. No criterion failed, and no behaviour delivered by another item was found wrong.

## Not verified, and why

- **`lint-clean` checked nothing.** `commands.lint` is null by ADR-0004, so no linter ran and no
  statement is made about style, unused imports or anything else a linter would catch in the new
  code. This is the same gap every item in this project carries.
- **Only the permission case was triggered.** A full disk, a read-only mount and a filename too
  long for the file system reach the same `except OSError` by the exception hierarchy, but none of
  them was produced here — there is no way to create them in this environment that would not cost
  more than it proves. The plan names this as a known risk.
- **The skip path was demonstrated by injection, not by running as root.** The condition was
  created by making the directory writable, which is what the criterion's condition amounts to;
  this session did not run the suite as a user for whom mode 500 is not binding.
- **`os.replace` failing after a successful write was not triggered.** The cleanup it would run is
  the same one AC3 exercises through the `NamedTemporaryFile` failure, but the specific ordering —
  temporary file written, rename refused — has no test and was not produced by hand.
- **Nothing was verified about `person delete` or `expense delete` against an unwritable store.**
  They share `save`, and `impl-report.md` says so, but no criterion asks for it and this skill did
  not check it.
