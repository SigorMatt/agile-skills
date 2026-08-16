# Verification report — BUG-0003

Verified-commit: 21d583dfbb8317982aaae420ca0c6dcfe7054794

Branch `wi/BUG-0003`, head `21d583d`; the last code commit is `8634781` and the one after it
touches only `tracker/`. Fixtures were built fresh under `/tmp/vbug3-nC1s/` with bytes paths, not
the `/tmp/bug3` folder the item names and the earlier steps reused. Criteria were read before the
implementation report.

## Verdict

**Pass — all six criteria.** Each decided by a command run here. No defect in the delivered
behaviour; nothing sent back. One finding about ADR-0008's *reasoning* — not its decision, and not
the code — is filed as `questions/Q-001.md` and summarised below.

## Criteria

Byte strings are shown as Python `repr`, because the whole point of this item is a byte no terminal
renders faithfully.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | a fresh folder built with bytes paths — `good.txt` (2 lines) and `bad\xff.txt` (3) — then `python3 $L $F`, with stdout captured to a file and read back as bytes | stdout `b'3  bad\xff.txt\n2  good.txt\n5  total\n'`, stderr **0 bytes**, exit **0**; `grep -c -E "Traceback\|UnicodeEncodeError"` over both streams → 0 | two file rows and the total, and the undecodable byte reaches stdout intact. Before the fix this folder produced a traceback, empty stdout and exit 1 |
| AC2 | **pass** | the first line of that stdout | `b'3  bad\xff.txt'` | count 3 ✓, first in WI-0001 AC2's order ✓ (3 before 2), two spaces before the name ✓. The spelling is ADR-0008's: the raw byte, as `ls -b` and `wc` write it |
| AC3 | **pass** | `cmd > a; cmd > b; diff a b` on stdout **and** on stderr | `diff` produced no output and exited 0 for both | the criterion's own command, run as written |
| AC4 | **pass** | `python3 $L --top 1 $F` | stdout `b'3  bad\xff.txt\n5  total (all 2 files)\n'`, exit 0 | one file row and WI-0002 AC3's labelled total, both intact through the new write |
| AC5 | **pass** | WI-0001 AC1's own folder (`notes.md` 128 lines, `a.py` 7); plus the whole existing suite | `128  notes.md$` / `  7  a.py$` / `135  total$` under `cat -A`, exit 0; and all 55 pre-existing tests pass unmodified in the 60-test run | ASCII output is byte-identical through the bytes path, which is what `os.fsencode` guarantees for an ASCII string |
| AC6 | **pass** | `git show 6d1e437:linecount.py > linecount.py`, suite, restore; then the suite on the branch head | at `6d1e437`: `FAIL: test_ac1_undecodable_name_does_not_abort_the_report`, `ERROR: test_ac2_the_row_follows_the_same_rules`, `FAIL: test_ac4_top_one_on_that_folder` — the three tests AC6 names, none of them passing. On the branch head: `Ran 60 tests`, `OK`, exit 0 | re-run here. `implement` already declared that AC2's is an ERROR rather than a FAIL, and that `test_ac3` passes there because a consistently crashing tool is byte-identical to itself; both are true and both are outside what AC6 asks |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` (hard) | **pass** | run here on the branch head: `Ran 60 tests`, `OK`, exit 0 |
| `lint-clean` (hard) | **skipped** | `{{commands.lint}}` is null; ADR-0003. Checked nothing; not a pass |
| `workspace-valid` (hard) | **pass** | `scripts/validate-workspace` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` (hard) | **pass** | six rows above, each a command run here on fixtures no earlier step had touched |
| `negative-cases-exercised` (hard) | **pass** | six conditions, including two locale settings and the two neighbouring bugs' outputs — see below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | three mutations plus a fourth that tested the ADR's own argument; table below |

## Negative and boundary cases exercised

1. **A name that is not valid UTF-8**, alongside an ordinary file → both rows, the total, exit 0.
2. **`--top 1` on that folder** → one row and the labelled total.
3. **The same folder twice** → byte-identical stdout and stderr.
4. **`LC_ALL=C LANG=C`** on that folder → `b'3  bad\xff.txt\n2  good.txt\n5  total\n'`, exit 0.
   This is the claim ADR-0008 makes and `impl-report.md` declared untested; it holds.
5. **A name that is valid UTF-8 but non-ASCII (`café.txt`) under `LC_ALL=C`, and again under
   `PYTHONIOENCODING=ascii`** → `b'4  caf\xc3\xa9.txt\n4  total\n'`, exit 0 in both. The chosen
   implementation is independent of stdout's encoding, which is the property ADR-0008 chose it for.
6. **BUG-0001's and BUG-0002's outputs through the new write** → a symlink-loop folder still prints
   `3  ok.txt` / `3  total` and exits 0; an all-unreadable folder still prints
   `no files could be read`; an empty folder still prints `no files`. Every sentence in the tool
   now travels through `sys.stdout.buffer`, so this had to be checked rather than assumed.

## Test sensitivity check

Each mutation applied, suite run, file restored; `git status` clean afterwards.

| mutation | result |
|----------|--------|
| the code as it stood at `6d1e437` (AC6's demonstration) | 10 tests fail — this item's three, plus BUG-0001's and BUG-0002's, which that commit also predates |
| the bytes write reverted to `print(text, end="")` | **caught**: `test_ac1_undecodable_name_does_not_abort_the_report`, `test_ac2_the_row_follows_the_same_rules`, `test_ac4_top_one_on_that_folder` |
| **ADR-0008's option B** — `sys.stdout.reconfigure(errors="surrogateescape")` plus `print` | **the suite passes.** Not a defect in the fix: option B is a different valid implementation of the same criteria, and the suite is not required to distinguish two correct implementations. What it does show is that no test protects the *reason* the chosen one was preferred — see below |
| option B under a genuinely non-UTF-8 stdout (`PYTHONIOENCODING=ascii`) with `café.txt` | **exit 1, `UnicodeEncodeError`** — while the chosen implementation exits 0 and prints `b'4  caf\xc3\xa9.txt\n4  total\n'`. The preference recorded in ADR-0008 is correct |

## Finding: ADR-0008's example does not reproduce, though its conclusion holds

ADR-0008 rejects option B on the grounds that `café.txt` under `LC_ALL=C` "still raises". Measured
here, `LC_ALL=C` makes CPython enable UTF-8 mode (PEP 540), `sys.stdout.encoding` becomes `utf-8`,
and option B handles that folder fine. The risk the ADR describes is real, but it needs
`PYTHONIOENCODING=ascii` — a genuinely non-UTF-8 stdout — to appear, and there the difference
between the two options is exit 0 versus exit 1.

The decision the ADR takes is therefore **right, and better supported after this measurement than
before it**. Only the illustration is wrong. Filed as `questions/Q-001.md` (non-blocking, to the
architect) recommending the ADR be amended in place with the measured example, since its decision
does not change. This is a defect in a document's reasoning, not in the code, and no criterion of
this item touches it.

## Diff review against the plan

`linecount.py` +9/−3, `tests/test_linecount.py` +55/−0. Two code hunks: the module docstring
sentence (plan step 2) and the write with its flush and comment (step 1). The test file's diff has
**0** deleted lines. `count_lines`, `list_files`, `format_report`, `parse_top`, `parse_args`, the
sort key, the branch structure of `main` and every stderr `print` are byte-identical to `main`.

`impl-report.md`'s two volunteered observations were checked rather than accepted: AC2's test does
report ERROR at `6d1e437` (empty stdout, so `splitlines()[0]` raises), and `test_ac3` does pass
there.

## Defects found

None in the delivered behaviour. One documentation finding, filed as `Q-001` rather than as a bug,
because nothing in the code, the criteria or the tests is wrong — an ADR's supporting example is.

## Not verified, and why

- **Lint.** No lint command (ADR-0003); the nine changed lines were read at review and by no tool.
- **Non-POSIX platforms.** The new test class is `skipUnless(os.name == "posix")` and every fixture
  here uses a POSIX filesystem. Unchanged from WI-0001, and the item's own notes expect the guard.
- **stderr's encoding.** Plan assumption 2 and `impl-report.md` both declare it: a file that is
  both undecodable *and* unreadable would compose `linecount: <name>: <problem>` through `print`
  and could still raise. I did not build that folder — it is outside this item's criteria — so the
  gap is confirmed as declared, not closed.
- **Interleaving.** ADR-0008 notes that stdout is now written once as bytes and that any later
  `print` to stdout would interleave. Nothing prints to stdout today; the constraint is untestable
  until something does.
- **Very large reports.** The write is a single buffered call; only three-file folders were
  exercised here.
