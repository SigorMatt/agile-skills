# Verification report — BUG-0001

Verified-commit: bb74d04a720fc298257e4bfbc7219da4ab724d05

This is the **second** verification of this item. The first, at `20bfbb3`, passed all six criteria
and sent the item back anyway for D1 — `store._refusal` raised while classifying, so a deck
*directory* at mode `000` still reached the person as a double traceback at exit 1, from code this
item had added. That report is superseded by this one; its D1 is the defect this verification
re-tests. No checkbox was ticked then. All six are ticked now.

Everything below was run by this skill against a detached worktree of `wi/BUG-0001` at
`bb74d04a720fc298257e4bfbc7219da4ab724d05` (`git worktree add --detach /tmp/verify-head HEAD`).
Nothing is cited from `impl-report.md`; where a number matches that report, it matches because it
was measured again.

## Verdict

**Pass.** All six criteria hold at the branch head, each demonstrated by a command run here. D1 is
fixed and does not recur under any of the eight boundary conditions probed. Two observations are
recorded below and neither is filed: one is unchanged behaviour that predates this item, and one
is a stale sentence in a test module's docstring.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 — reproduction A names the deck file, not the temporary file, says it could not be written, exits non-zero, no traceback | **pass** | `mkdir -p $A/.local/share/recall; chmod 500 …; HOME=$A recall add --question "capital of France" --answer Paris` | exit `3`; stderr `recall: cannot write the deck file /tmp/vrun/A/.local/share/recall/deck.json -- permission denied. Nothing has been written and the deck file is exactly as it was before this attempt. Put that right, then run recall again.`; stdout empty | `grep -c '\.tmp'` → 0 on both streams, so the temporary file is not named; `grep -c Traceback` → 0 on both |
| AC2 — reproduction B names the deck file, says it could not be read, exits non-zero, no traceback | **pass** | `mkdir -p $B/.local/share/recall/deck.json; HOME=$B recall list` | exit `3`; stderr `recall: cannot read the deck file /tmp/vrun/B/.local/share/recall/deck.json -- it is a directory, not a file. Nothing has been written and the file is exactly as it was. …` | `Traceback` absent from both streams |
| AC3 — reproduction C exits non-zero from **both** `list` and `add`, and the message names the path in the way | **pass** | `printf 'not a directory' > $C/.local/share/recall; HOME=$C recall list; HOME=$C recall add --question q --answer a` | both exit `3`; both stderr `… cannot read the deck file /tmp/vrun/C/.local/share/recall/deck.json -- /tmp/vrun/C/.local/share/recall is not a directory, and the deck's directory has to be one. …` | the criterion's own trap checked explicitly: `grep -c "deck is empty" C1.out` → **0**, so `list` is not quietly reporting an empty deck |
| AC4 — in all three cases nothing under the deck's directory is created, modified or removed | **pass** | for each of A, B, C: `find $H -mindepth 1 \| sort` with `sha256sum` per file, taken before and again after, then `diff` | `diff` empty in all three cases — the same directory entries and the same digests | the snapshot carries directories as well as files, so a created temporary file or a removed entry would show |
| AC5 — a regression test covers all three reproductions and fails if the handling is removed, demonstrated by removing it and recording which tests fail | **pass** | five mutations, each applied alone in the worktree and restored, suite run each time (table under *Test sensitivity check*) | M1 → 4 failures, M2 → 1, M3 → 3, M4 → 3, M5 → 2; suite `OK` after every restore | every one of the three reproductions is covered by at least one mutation that makes its test fail: A by M3 and M4, B by M1, C by M1 and M2 |
| AC6 — the six content cases WI-0001 AC8 covers still refuse with their existing messages | **pass** | all twelve invocations (six decks × `list`, `add`) run against a worktree of `main` at `ec112a4` and against the head, with `$HOME` masked out of both, then `diff -r` | `diff -r /tmp/ac6-head /tmp/ac6-main` → **no differences**; all twelve exit `3` on both sides | byte-for-byte, not a substring assertion. See *A criterion whose subject is another criterion* below for the reading AC6 also requires |

## A criterion whose subject is another criterion

AC6's subject is a criterion, so it is read as well as run (`spec/dor-dod.md`; the gate
`a-criterion-about-criteria-is-read`).

**Criteria it covers, by ID: `WI-0001` AC8** — and only that one. AC6 names it explicitly and
enumerates the six cases, so it is decidable as written.

**`WI-0001` AC8 read against the new behaviour — verdict: still true.** Its sentence is: *"If the
deck file exists but the tool cannot read it as a deck — it is truncated, malformed, or not the
format the tool writes — then `recall add` and `recall list` both write a message to stderr saying
so, name the file, and exit non-zero. Neither rewrites, truncates or repairs the file: its bytes
are identical before and after."* Read against what this item built: the condition AC8 describes is
about the file's *contents*, and every `raise DeckUnreadable(...)` that produces it is unmodified,
as is `_report_unreadable`'s sentence and its exit value. What changed on that path is one token in
each of four `except` clauses — `store.DeckUnreadable` widened to `store.DeckError`, a superclass —
which cannot narrow what is caught. AC8's own "identical before and after" clause is re-measured
here too, by the twelve-invocation comparison, which includes the deck's bytes.

**Tests as evidence for that verdict, not as its definition:**
`tests.test_deck_file_errors.ContentFaultsStillRefusedTests` passes at the head (12 subtests), and
independently of the suite, the twelve invocations are byte-identical to `main`'s. Neither is the
reason for the verdict; the reason is the sentence above.

**Non-intersection, stated in those words: nothing executable exercises `WI-0001` AC8's condition
and this execution's changed line together.** `_refusal` is reachable only from an `except OSError`
handler around the read or the write; a content fault is diagnosed *after* a successful read. A
deck can be both malformed and inside a directory the operating system refuses, but only one of the
two can be observed on a given `read_bytes` — the read either succeeds and the contents are parsed,
or it fails and the contents are never seen.

**Waived by name: `WI-0001` AC8.** No covering case is written, because the two conditions are
mutually exclusive at the one `read_bytes` call and a test that provoked both would still observe
only one. What *is* covered, and was run: AC8's condition through the four widened `except` clauses
this item did change, which is the intersection that does exist.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` in the worktree at `bb74d04` → exit 0, `Ran 63 tests in 9.549s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` in the same worktree → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 6 item(s), 13 document(s)`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the Criteria table names the command this skill ran for each of AC1–AC6 and quotes its actual output. `impl-report.md` is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | every criterion of this item describes an error condition, and all three reproductions were provoked here rather than read about; eight further boundary conditions are in the next section |
| `a-criterion-about-criteria-is-read` | **pass** | the section above: `WI-0001` AC8 named by ID, its sentence read against the new behaviour with a verdict, tests recorded as evidence for that verdict, non-intersection stated in those words and waived by name |
| `tests-would-fail-without-the-change` | **pass** (advisory) | five mutations, below |

## Negative and boundary cases exercised

The item is entirely about error paths, so every criterion above is already a negative case. These
are the ones beyond the criteria, run to look for what the first verification found this way.

| # | condition | result |
|---|-----------|--------|
| N1 | **the deck's directory at mode `000`, with a deck in it — the first verification's D1** | `list`, `add`, `review` and `delete` all exit `3` with `cannot read the deck file …/deck.json -- permission denied. …`; `Traceback` absent from all four; the deck's bytes identical after the mode is restored. **Fixed** |
| N2 | the deck **file** itself at mode `000`, directory readable | `list` and `add` exit `3`, `-- permission denied`, no traceback |
| N3 | a symlink loop at the deck file | exit `3`, `-- too many levels of symbolic links` — `_refusal`'s third branch, the operating system's own words, on an errno `pathlib` does swallow |
| N4 | a symlink loop where the deck's **directory** belongs | `list` and `add` exit `3`, naming `…/.local/share/recall` as the thing that is not a directory |
| N5 | `$HOME` is a regular file | `list` and `add` exit `3`, naming `$HOME` itself as the obstruction — `_obstruction` walks from the filesystem root, so it finds the shallowest one |
| N6 | the deck's directory at mode `300` (write and traverse, not readable) with a deck in it | `list` prints the card and exits 0; `add` succeeds and the deck holds 2 cards. Correct: the file is named directly, so the directory's read bit is not needed |
| N7 | a **dangling symlink** where the deck's directory belongs | `list` reports `The deck is empty…` at exit **0**; `add` exits `3` naming the symlink. Unchanged by this item — observation, not filed; see below |
| N8 | the six content faults, on `main` and on the head | twelve invocations each side, byte-identical (AC6) |

No condition probed here produces a traceback, and none exits 0 while failing, except N7.

## Test sensitivity check

Each mutation was applied alone to the worktree at `bb74d04`, the suite run, and the file restored
from a copy taken first; the suite was confirmed `OK` again after the last restore, and
`git status --short` in the worktree was empty at the end.

| # | what was removed or reverted | which tests failed |
|---|------------------------------|--------------------|
| M1 | `load`'s `except OSError` clause | `test_directory_at_the_deck_path_is_refused`, `test_file_where_the_deck_directory_belongs_is_refused`, `test_listing_an_unreadable_deck_directory_is_refused`, `test_adding_to_an_unreadable_deck_directory_is_refused` — 4 |
| M2 | `load`'s absent-catch widened back to `(FileNotFoundError, NotADirectoryError)` | `test_file_where_the_deck_directory_belongs_is_refused` — 1 |
| M3 | `save`'s wrapper re-raises the `OSError` instead of `DeckInaccessible` | `test_unwritable_deck_directory_is_refused`, `test_a_sitting_whose_save_is_refused_says_so`, `test_a_deletion_whose_save_is_refused_says_so` — 3 |
| M4 | the three `except store.DeckInaccessible` clauses in `cli.py` no longer catch it | the same 3 |
| M5 | `_refusal`'s middle branch back to `path.is_dir()` — D1's defect, reinstated | `test_listing_an_unreadable_deck_directory_is_refused`, `test_adding_to_an_unreadable_deck_directory_is_refused` — 2, **and no others** |

M5 is the one that matters for the send-back: the two new tests are sensitive to exactly the line
that was wrong, and nothing else in the suite noticed it — which is why the first implementation
passed 61 tests with the defect in place.

## Defects found

**None.** D1 from the first verification is fixed: N1 above is its reproduction, run again here,
and it now produces a message rather than a double traceback, on all four subcommands.

Two observations, neither filed and neither a defect against this item's criteria:

**O1 — a dangling symlink where the deck's directory belongs still reports an empty deck at exit 0
(N7).** This is the *shape* of failure reproduction C names, and it is unchanged by this item —
`read_bytes` raises `FileNotFoundError` for it before and after, and `ADR-0004` §6 makes *"a
missing parent directory"* an empty deck, which a dangling symlink's target is. It was recorded by
the first verification and is repeated here so it does not vanish with the superseded report.
Whether a dangling symlink is "missing" or "in the way" is a question about `ADR-0004` §6's
wording, for whoever refines a criterion about the deck's directory.

**O2 — `tests/test_deck_file_errors.py`'s module docstring is now one case short.** It says the
file is about *"a directory that cannot be written, a directory where the deck file belongs, a file
where the deck's directory belongs"* and that *"the three reproductions here are BUG-0001's"*. There
are now four classes, the fourth being the mode-`000` directory. The class carries its own
docstring saying where it came from, so nothing is unexplained, but the module docstring's
enumeration is stale. It is a comment in a test file, not a claim under `docs/`, and it fails no
criterion — recorded for `review-close` to weigh under D12 rather than sent back.

## Not verified, and why

- **Whether the six content messages are *right***, only that they are **unchanged**. That is what
  AC6 asks, and it is what was measured.
- **A write that fails *after* the temporary file is opened** — `ENOSPC` during `json.dump`, a
  refused `fsync`, a refused `os.replace`. `save`'s wrapper covers them by construction and
  `_refusal` would fall through to the operating system's words, but provoking a full filesystem is
  beyond what could be set up here. `impl-report.md` declares the same gap.
- **`_refusal`'s `strerror is None` fallback** — the branch that names the exception's class. No
  condition reached here produced an `OSError` without a `strerror`.
- **Behaviour as root.** The three mode-dependent test classes skip when `os.geteuid() == 0`; this
  verification ran as uid `1000` (`id -u`), so nothing skipped, and the root path itself was not
  exercised. Mode bits do not restrain a privileged process, so the reproductions would not
  reproduce there.
- **Concurrency.** Two `recall` processes against one deck is untested here as everywhere else in
  this epic.
- **A real terminal.** Every run went through a shell with `HOME` redirected, as BUG-0001's own
  reproduction steps are written. Nothing was typed at a tty.
