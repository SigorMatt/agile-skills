# Journal — BUG-0003

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-16T22:30:00Z — verify v0.1.1 — qa-engineer

- **Item:** BUG-0003
- **Trigger:** filed by an independent regression pass over `main` at
  `6d1e437b4293571296809b322c47fb0dc83d1ad6`, after EP-001 closed. Created directly at `ready`
  (`spec/ids-and-statuses.md` §4, `— → ready`, actor `verify`).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC1, AC2 and AC9, and the accepted gap in `## Notes` that
    names this exact case as untested
  - `docs/architecture/overview.md` v2 — `## Boundaries that are deliberate`, "Bytes, not text"
    and the exit-status contract; `docs/product/vision.md` v1 — "A number, not a stack trace";
    `EP-001/item.md` `## Why now`
  - `linecount.py` on `main` — `main`'s `print(text, end="")` and the `os.fsencode` in the sort
    key; `git show 5adc619:linecount.py`
  - `.claude/agile-skills/spec/dor-dod.md` §2, `spec/work-item.md` §3
- **Decisions:**
  - **Not filed under WI-0001 AC9.** AC9's condition is a file that is not *text* — its contents
    — and that case passes: the PNG fixture lists cleanly with `Traceback` absent from both
    streams. This is a file whose *name* cannot be encoded on the way out, which AC9 does not
    reach. The citation used instead is `overview.md` v2's "no file can raise a decoding error"
    together with AC1, so the item is judged against a claim it actually contradicts.
  - **Exit 1 recorded as its own contradiction.** `overview.md` v2 defines only two statuses,
    0 and 2. Exit 1 is undefined by every document in this project, so a script branching on the
    exit code cannot classify it.
  - **`found-in: WI-0001`.** The same folder against `git show 5adc619:linecount.py` raises the
    same `UnicodeEncodeError` from the equivalent line. `--top` does not avoid it and did not
    introduce it.
  - **Priority `medium`.** The failure is total when it happens — empty stdout, no listing — but
    the trigger is rare on a modern system, and WI-0001's review already recorded it as a known
    untested case rather than an unknown one. `high` is reserved here for a defect on inputs the
    tool meets in ordinary use.
  - **The fix is deliberately left open, and flagged as ADR-worthy.** Writing the report through
    `sys.stdout.buffer` with `os.fsencode` and reconfiguring stdout's error handler produce
    different visible output, so the choice is the user's to see and the architect's to record.
    AC2 pins that a row exists with the right count in the right position, not how the byte is
    spelled.
- **Questions raised:** none on this item; `EP-001/Q-001` is non-blocking and unrelated to its
  content.
- **Commands:**
  - `mkdir -p /tmp/bug3` then `python3 -c "..."` creating `good.txt` (`a\nb\n`) and
    `bad\xff.txt` (`a\nb\nc\n`) with `bytes` paths → exit 0
  - `ls -b /tmp/bug3` → `bad\377.txt`, `good.txt` — two ordinary regular files
  - `python3 linecount.py /tmp/bug3` → exit 1, stdout empty, stderr a traceback ending
    `UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 6: surrogates
    not allowed`, raised at `print(text, end="")`
  - `python3 linecount.py /tmp/bug3 2>/dev/null` → exit 1, stdout empty — not even the row for
    `good.txt`
  - `python3 linecount.py --top 1 /tmp/bug3` → the same `UnicodeEncodeError`
  - `cd /tmp/bug3 && wc -l *` → exit 0, three rows, the undecodable byte written through
  - `python3 /tmp/qa-lc10/lc_wi1.py /tmp/bug3` → exit 1, the same error from
    `print(format_report(rows), end="")`
  - `.claude/agile-skills/scripts/new-item --id BUG-0003 --type bug --epic EP-001 --priority
    medium --status ready --actor verify --found-in WI-0001 …` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1; this item's own errors (stale
    `updated`, missing journal entry) fixed by this entry and a bumped timestamp
- **Gates:** the bug Definition of Ready, `spec/dor-dod.md` §2, criterion by criterion:
  - `RB1` steps runnable without further questions → **pass** — five numbered steps including the
    exact `python3 -c` that creates the undecodable name with `bytes` paths, an `ls -b` to confirm
    the folder, and the contrasting `wc -l *`
  - `RB2` actual behaviour quotes real output → **pass** — the full traceback verbatim, the
    stdout-only run, the `--top` variant and `wc`'s output, each with its exit code
  - `RB3` expected behaviour cites what it contradicts → **pass** — WI-0001 AC1 quoted verbatim,
    plus `overview.md` v2's "no file can raise a decoding error" and its exit-status contract,
    `vision.md` v1's "A number, not a stack trace", WI-0001 `## Notes`' stated failure condition,
    and EP-001 `## Why now`
  - `RB4` `found-in` names the delivering item → **pass** — `found-in: WI-0001`, confirmed against
    that item's shipped build at `5adc619`
  - `RB5` acceptance criteria include a regression test → **pass** — AC6 requires tests for AC1,
    AC2 and AC4 failing against `6d1e437b`; `## Notes` records that the fixture needs `bytes`
    paths and that a non-POSIX skip guard is expected, since WI-0001 already declares POSIX-only
    as an accepted gap
- **Artifacts:**
  - `tracker/items/BUG-0003/item.md` (body written; `updated` bumped for `item.updated.stale`),
    `journal.md` (this entry), `history.md` (one row: `— → ready`)
  - `tracker/items/EP-001/artifacts/regression-verify-report.md`
  - `tracker/board.md` regenerated
- **Status:** `—` → `ready`
- **Result:** Filed. The tool never decodes a file's contents, which is the design — but
  `os.scandir` decodes its *name* before the tool sees it, and a name that is not valid UTF-8
  cannot be encoded back to stdout. The whole report is lost to a `UnicodeEncodeError` traceback
  and an exit status no document defines, on a folder `wc -l *` handles without complaint.

## 2026-08-16T22:58:30Z — answer-questions v0.1.1 — architect

- **Item:** BUG-0003
- **Trigger:** answering `BUG-0001/questions/Q-001.md` (the clock disagreement). This item was
  not the question's owner, but two of its timestamps were among the artifacts the answer
  corrected, and a correction that is not recorded where it happened is a silent rewrite
- **Inputs read:** `tracker/items/BUG-0003/item.md` and `journal.md`; `BUG-0001/questions/Q-001.md`;
  `.claude/agile-skills/scripts/validate-workspace` (`item.updated.stale`)
- **Decisions:**
  - **`created`: `2026-08-17T01:30:00Z` → `2026-08-16T22:30:00Z`.** The old value was this
    machine's local time (IDT, UTC+3) labelled `Z`; true UTC at that moment was 22:30. It is
    corrected because `updated` is pushed forward by every transition, so a `created` three
    hours in the future would make `item.updated.before-created` fire on every future transition
    of this item — the state that froze BUG-0001.
  - **`updated`: corrected to `2026-08-16T22:30:00Z`, then restored to `2026-08-17T01:30:00Z`.**
    The validator refused the correction: `item.updated.stale` requires `updated` to be ≥ the
    last history row, and that row carries the same skewed value and may not be touched. It will
    be replaced by a clamped timestamp on this item's next transition.
  - **Journal heading: `## 2026-08-17T01:30:00Z` → `## 2026-08-16T22:30:00Z`** on the
    regression pass's filing entry, so the journal and the corrected `created` agree.
  - **The history row is untouched**, and still reads `2026-08-17T01:30:00Z`. It may not be
    edited by any skill. This item is not blocked by it: its only row is the first one, so the
    clamp in `scripts/transition` will stamp its next row `2026-08-17T01:30:01Z` and announce
    that it did.
- **Questions raised:** none
- **Commands:** `python3 .claude/agile-skills/scripts/validate-workspace .` → the
  `item.updated.stale` error that reversed the `updated` correction, then clean for this item
- **Gates:** this execution's gates are recorded in full on BUG-0001, the item that owns the
  question. For this item: `workspace-valid` → **pass for BUG-0003`s own files** (no finding names
  this item); `answer-is-propagated` → **pass** (both corrections verified by re-reading)
- **Artifacts:** `tracker/items/BUG-0003/item.md` (`created` corrected), `journal.md` (heading
  corrected; this entry)
- **Status:** `ready` → `ready` (unchanged)
- **Result:** BUG-0003 carries a corrected `created`, an `updated` deliberately left anchored to its
  untouchable history row, and a corrected journal heading. Nothing about the defect it reports
  changed. It is ready to be planned as soon as the workspace validates again.

## 2026-08-16T23:19:00Z — plan v0.1.1 — architect

- **Item:** BUG-0003
- **Trigger:** status `ready`, dispatched by `next` — the last open bug under EP-001
- **Inputs read:**
  - `tracker/items/BUG-0003/item.md` — the summary, the reproduction script, `## Expected
    behaviour` with its five quotations, AC1–AC6, and the `## Notes` suggestion of two candidate
    mechanisms
  - `tracker/items/BUG-0001` and `BUG-0002` — both `done`; read to be sure this fix does not
    disturb ADR-0006's silent skips or ADR-0007's new sentence
  - `docs/architecture/adr/ADR-0002` and `ADR-0005` … `ADR-0007`;
    `docs/architecture/overview.md` v3 (its "bytes, not text" boundary in particular);
    `docs/product/vision.md` v1 ("a number, not a stack trace")
  - `tracker/items/WI-0001/item.md` AC1, AC2, AC9 and `WI-0002/item.md` AC3 — what AC2, AC4 and
    AC5 make binding
  - the code on `main` at `2946f57`: `main`'s final `print`, and the sort key in particular
- **Decisions:**
  - **Reproduced the bug and its contrast first.** `python3 linecount.py /tmp/bug3` →
    `UnicodeEncodeError … exit=1`, stdout empty even for the ordinary file beside it; `wc -l *` on
    the same folder → three lines and exit 0. The tool this replaces does better, which is the
    argument the epic was founded on.
  - **Established the mechanism at the interpreter rather than from the traceback**:
    `entry.name` is `'bad\udcff.txt'`, `os.fsencode(entry.name)` is `b'bad\xff.txt'`, and
    `os.fsencode` round-trips a whole rendered line, not just a name. That is what makes option A
    a one-line change.
  - **The report is written to `sys.stdout.buffer` as `os.fsencode`d bytes** (ADR-0008). Route:
    **decided here** — the item's `## Notes` offered two candidates and left the choice to `plan`.
    Chose bytes over reconfiguring stdout's error handler because the latter fixes only the
    surrogate case: a name that is valid UTF-8 but unencodable in the terminal's encoding —
    `café.txt` under `LC_ALL=C` — would still raise, and the bug would return in a different
    costume. Writing bytes makes the output locale-independent, which is what `ls -b` and `wc` do.
  - **Rejected escaping the byte for display** (ADR-0008 option C): the name on screen would no
    longer be the name on disk, so it could not be pasted into another command — and the tool's
    one job is to report what is in the folder.
  - **Extended the overview's "bytes, not text" boundary to names** and bumped it to v4. The
    document already said contents are never decoded; after this change the same principle covers
    the way out, and the single-write constraint it creates belongs where the next person will
    read it.
  - **Left stderr on `print`** (assumption 2). Those are the tool's own sentences; a name appears
    in them only in `linecount: <name>: <problem>`, and a file that is both undecodable and
    unreadable could still raise there. No criterion covers it; recorded rather than absorbed,
    because fixing it would be a second change with no criterion of its own.
  - **Required a POSIX guard on the new test class** (assumption 3): such a name cannot be created
    on every filesystem, and WI-0001's notes already record that only POSIX has been exercised.
- **Questions raised:** none. The one open choice — how the byte is spelled on screen — is
  explicitly `plan`'s by AC2's own words, and it is reversible at a single boundary.
- **Commands:**
  - the item's reproduction script, verbatim → `ls -b` shows `bad\377.txt`;
    `python3 linecount.py /tmp/bug3` → `UnicodeEncodeError`, exit 1, empty stdout;
    `wc -l *` → `3 bad?.txt` / `2 good.txt` / `5 total`, exit 0
  - `python3 -c "os.scandir; os.fsencode"` over that folder → `'bad\udcff.txt'` →
    `b'bad\xff.txt'`, and `os.fsencode('  3  bad\udcff.txt\n')` → `b'  3  bad\xff.txt\n'`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
    (10 documents: ADR-0008 is new, overview at v4)
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table in `artifacts/plan.md` has
    one row per criterion AC1–AC6, each naming the step and the named test. AC2's three clauses
    (count, position, spacing) are pinned by one exact-bytes assertion rather than by prose
  - `project-commands-resolved` (hard) → **pass** — `commands.test` is `python3 -m unittest
    discover`, demonstrably runnable (55 tests pass on `main` today); lint and build stay null with
    ADR-0003 recording why
  - `decisions-recorded` (hard) → **pass** — five choices in `## Decisions and ADRs`: two point at
    ADR-0008 (one also at overview v4), two at existing criteria, and three assumptions carry their
    reversal costs
  - `plan-is-executable-without-you` (advisory) → **pass** — step 1 gives the replacement lines and
    the observable result; step 3 names the test class, its guard, how to build a bytes-named file,
    and every test; step 4 gives the mechanism for proving they fail on the old code
- **Artifacts:**
  - `tracker/items/BUG-0003/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0008-writing-the-report-as-bytes.md` (new, v1)
  - `docs/architecture/overview.md` (v3 → v4, with a change-log row)
  - `tracker/items/BUG-0003/journal.md` (this entry), `history.md` (one row), `board.md`
- **Status:** `ready` → `planned`
- **Result:** BUG-0003 has a five-step plan whose code change is one write and its flush. All six
  criteria map to a step and a named test, with AC2's three clauses pinned by exact bytes. The
  decision the item left to `plan` — how the undecodable byte reaches the terminal — is ADR-0008,
  chosen over three alternatives, and the boundary it moves is now in the architecture overview.

## 2026-08-16T23:22:00Z — implement v0.1.0 — developer

- **Item:** BUG-0003
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/BUG-0003/item.md` (AC1–AC6, the reproduction script, the `## Notes` on
    candidate mechanisms), `artifacts/plan.md` (steps 1–5 and the mapping table), `history.md`,
    `questions/` (empty)
  - `docs/architecture/adr/ADR-0008` — the rule this executes — and `ADR-0002`, `ADR-0006`,
    `ADR-0007`, whose outputs now travel through the new write; `docs/architecture/overview.md` v4
  - `tracker/items/WI-0001/item.md` AC1/AC2 and `WI-0002/item.md` AC3 — what AC2, AC4 and AC5 make
    binding
  - the code on `main` at `f1b7524`: `main`'s final write, and the sort key
- **Decisions:**
  - **Executed plan step 1 verbatim**, and nothing near it. The report is still assembled as `str`;
    only the boundary changed, from `print` to `sys.stdout.buffer.write(os.fsencode(text))` plus a
    flush.
  - **Split AC2 into its own test** rather than leaning on AC1's exact-bytes assertion. AC2 makes
    three claims — count, position, spacing — and a criterion whose only evidence is another
    criterion's assertion is hard to check later.
  - **Built the fixture with bytes paths**, `os.path.join(os.fsencode(folder), b"bad\xff.txt")`,
    because the name cannot be expressed as valid UTF-8 text, and guarded the class with
    `skipUnless(os.name == "posix", …)` as plan assumption 3 requires.
  - **Recorded two things the criteria do not require but a reader would want.** At `6d1e437`,
    `test_ac2` reports **ERROR**, not FAIL — stdout is empty there, so `splitlines()[0]` raises
    before any assertion. And `test_ac3` **passes** at `6d1e437`: two runs of a consistently
    crashing tool are byte-identical. AC6 lists AC1, AC2 and AC4 and not AC3, which is right, but
    both facts belong in the report rather than in a reader's inference.
  - **Left stderr on `print`** (plan assumption 2): a file that is both undecodable and unreadable
    could still raise while composing `linecount: <name>: <problem>`. Outside this item's criteria;
    declared rather than absorbed.
  - **Did not test the locale claim.** ADR-0008 chose bytes over `reconfigure` partly because the
    output stops depending on `LANG`/`LC_ALL`; nothing here runs the tool under `LC_ALL=C`, so that
    is argued and not measured. Declared in the report's `## What I did not do`.
- **Questions raised:** none. The one open choice was AC2's spelling of the byte, which ADR-0008
  already made.
- **Commands:**
  - `git checkout -b wi/BUG-0003`; `scripts/transition BUG-0003 --to in-progress` → applied
  - `python3 linecount.py /tmp/bug3 | cat -v` → `3  badM-^?.txt` / `2  good.txt` / `5  total`,
    exit 0; `--top 1` → `3  badM-^?.txt` / `5  total (all 2 files)`
  - `python3 -m unittest discover` → exit 0, `Ran 60 tests in 1.794s`, `OK`
  - `git show 6d1e437:linecount.py > linecount.py; python3 -m unittest discover -v` →
    `FAIL: test_ac1_undecodable_name_does_not_abort_the_report`,
    `ERROR: test_ac2_the_row_follows_the_same_rules`,
    `FAIL: test_ac4_top_one_on_that_folder`; `test_ac3` and `test_ac5` pass there. Restored → 60
    tests, `OK`
  - `git commit` → `8634781`; `scripts/check-commit-refs BUG-0003 wi/BUG-0003` → exit 0
- **Gates:** (full evidence in `artifacts/impl-report.md` `## Gates`)
  - `tests-pass` (hard) → **pass** — 60 tests, exit 0, on branch head `8634781`
  - `lint-clean` (hard) → **skipped** — null command; ADR-0003. Not a pass
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors
  - `every-criterion-has-a-test` (hard) → **pass** — AC1–AC6 each mapped to a named test with exact
    bytes or an exit code; the ERROR-versus-FAIL detail is stated rather than smoothed
  - `commits-reference-the-item` (hard) → **pass** — 1 of 1
  - `no-unplanned-scope` (advisory) → **pass** — six lines of `linecount.py` and one appended test
    class
- **Artifacts:**
  - `linecount.py` (185 → 191 lines), `tests/test_linecount.py` (587 → 642 lines, 55 → 60 tests)
  - `tracker/items/BUG-0003/artifacts/impl-report.md` (new)
  - branch `wi/BUG-0003`, commit `8634781`, plus this execution's tracker commit
  - `journal.md` (this entry), `history.md` (two rows), `board.md`
- **Status:** `planned` → `in-progress` → `verifying`
- **Result:** The tool now prints a folder containing a name that is not valid UTF-8 — two rows, a
  total, exit 0, the byte reaching stdout exactly as `ls -b` and `wc` write it — and ASCII folders
  are byte-identical to before. Three regression tests fail against `6d1e437`, and two facts AC6
  does not ask about (an ERROR rather than a FAIL, and AC3's test passing on a consistently
  crashing tool) are recorded rather than left for a reader to notice.

## 2026-08-16T23:26:00Z — verify v0.1.1 — qa-engineer

- **Item:** BUG-0003
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/BUG-0003/item.md` — the six criteria, read **first**, and the reproduction
    script; `history.md`; `artifacts/plan.md`; then `artifacts/impl-report.md`, read last
  - `docs/architecture/adr/ADR-0008` — including its `## Options considered`, which is what this
    verification ended up measuring — plus `ADR-0002`, `ADR-0006`, `ADR-0007`, whose outputs now
    travel through the new write; `docs/architecture/overview.md` v4
  - `tracker/items/WI-0001/item.md` AC1/AC2 and `WI-0002/item.md` AC3
  - the code on `wi/BUG-0003` at `21d583d` (last code commit `8634781`) and the diff against `main`
- **Decisions:**
  - **Captured stdout to files and compared bytes**, rather than reading a terminal. The whole item
    is about a byte no terminal renders faithfully, so `repr` of the captured bytes is the only
    honest evidence.
  - **Ran AC3's `diff` command as the criterion writes it**, on stdout and on stderr.
  - **Tested the locale claim `implement` declared untested.** ADR-0008 chose bytes partly for
    locale-independence; under `LC_ALL=C` the undecodable name prints intact and exits 0, and so
    does `café.txt`.
  - **Measured ADR-0008's rejected option instead of taking its word.** Option B
    (`sys.stdout.reconfigure(errors="surrogateescape")`) passes the entire suite — which is not a
    defect, since the suite is not required to distinguish two correct implementations — and, under
    `LC_ALL=C`, handles `café.txt` fine. **The ADR's example does not reproduce**: `LC_ALL=C`
    enables CPython's UTF-8 mode, so stdout is UTF-8 there. Under `PYTHONIOENCODING=ascii` the risk
    is real and stark: option B exits 1 with `UnicodeEncodeError` where the chosen implementation
    exits 0. So the decision is right and better supported than before, and only the illustration
    is wrong.
  - **Filed `Q-001` (non-blocking, to architect) rather than editing the ADR or letting it pass.**
    `verify` does not write to `docs/`, and a rationale that a future reader can disprove in one
    command invites them to "simplify" the write back to `print`. Recommended amending in place
    with the measured example, since the decision does not change and `doc-header.md` §4 forbids
    only changing a decision by edit.
  - **Did not file a bug.** Nothing in the code, the criteria or the tests is wrong; an ADR's
    supporting example is. Filing correct behaviour into a defect queue would misroute it.
  - **Checked the two neighbouring bugs' outputs through the new write** — `no files`,
    `no files could be read`, and BUG-0001's silent skips all now travel through
    `sys.stdout.buffer`, so assuming they were unaffected would have been exactly the wrong move.
- **Questions raised:** `Q-001` (non-blocking, to architect) — ADR-0008's `LC_ALL=C` example does
  not reproduce; three options and a recommendation, with the measurement table, are in the file
- **Commands:**
  - AC1: bytes-path folder → stdout `b'3  bad\xff.txt\n2  good.txt\n5  total\n'`, stderr 0 bytes,
    exit 0; `grep -c -E "Traceback|UnicodeEncodeError"` on both streams → 0
  - AC2: first stdout line → `b'3  bad\xff.txt'`
  - AC3: `cmd > a; cmd > b; diff a b` on stdout and stderr → no output, exit 0
  - AC4: `--top 1` → `b'3  bad\xff.txt\n5  total (all 2 files)\n'`, exit 0
  - AC5: WI-0001 AC1's folder → `128  notes.md$` / `  7  a.py$` / `135  total$`, exit 0
  - AC6: `6d1e437` → `FAIL: test_ac1_…`, `ERROR: test_ac2_…`, `FAIL: test_ac4_…`; branch head →
    `Ran 60 tests`, `OK`
  - locale matrix, both implementations × {`LC_ALL=C`, `PYTHONIOENCODING=ascii`} ×
    {undecodable name, `café.txt`} → the only failure in eight runs is option B with `café.txt`
    under `PYTHONIOENCODING=ascii`: exit 1, `UnicodeEncodeError`
  - `python3 $L /tmp/bug1a`, `/tmp/bug2a`, `/tmp/bug2c` → BUG-0001's and BUG-0002's behaviour
    unchanged through the new write
  - `scripts/validate-workspace .` → exit 0
- **Gates:**
  - `tests-pass` (hard) → **pass** — 60 tests, exit 0, run here on the branch head
  - `lint-clean` (hard) → **skipped** — null command (ADR-0003); not a pass
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `every-criterion-independently-checked` (hard) → **pass** — six rows, each a command run here
    with the captured bytes quoted
  - `negative-cases-exercised` (hard) → **pass** — six conditions including two locale settings and
    both neighbouring bugs' outputs
  - `tests-would-fail-without-the-change` (advisory) → **pass** — the revert-to-`print` mutation is
    caught by three tests; the ADR-option-B mutation is recorded as passing, with what that does
    and does not mean spelled out
- **Artifacts:**
  - `tracker/items/BUG-0003/artifacts/verify-report.md` (new), carrying
    `Verified-commit: 21d583dfbb8317982aaae420ca0c6dcfe7054794`
  - `tracker/items/BUG-0003/item.md` — all six criteria ticked
  - `tracker/items/BUG-0003/questions/Q-001.md` (new, open, non-blocking)
  - `journal.md` (this entry), `history.md` (one row); no bug items
- **Status:** `verifying` → `in-review`
- **Result:** All six criteria pass on `21d583d`: the folder that used to produce a traceback now
  prints two rows, a total and exit 0, with the undecodable byte intact, and ASCII output is
  byte-identical. The fix survives two locale settings that the implementation only argued about.
  One finding, filed as a question: ADR-0008's reason for rejecting the alternative is illustrated
  with an example that does not reproduce, though a corrected example makes the same case more
  strongly.

## 2026-08-16T23:30:00Z — answer-questions v0.1.1 — architect

- **Item:** BUG-0003
- **Trigger:** `Q-001` open and addressed to `architect`; dispatched by `next` at step 3, ahead of
  `review-close`. The item stayed at `in-review` — the question was filed non-blocking
- **Inputs read:**
  - `tracker/items/BUG-0003/questions/Q-001.md` and its measurement table
  - `docs/architecture/adr/ADR-0008` v1 in full, `## Options considered` in particular
  - `.claude/agile-skills/spec/doc-header.md` **§4** — the ADR rules, read verbatim rather than
    from memory, because the question turned on which of them applies
  - `tracker/items/BUG-0003/artifacts/plan.md` (its `## Approach` repeats the same claim),
    `verify-report.md`, `impl-report.md`; `docs/architecture/overview.md` v4
- **Decisions:**
  - **Amended ADR-0008 in place to v2 rather than superseding it.** `doc-header.md` §4 forbids
    editing an ADR *to change its decision*, and the decision here is untouched — the report is
    still written as `os.fsencode`d bytes. Superseding would advertise a revision that did not
    happen and send a reader hunting for a change in the decision.
  - **Left the wrong claim visible instead of replacing it.** The same rule says the point of the
    file is to preserve what was believed at the time. v2 therefore *adds* a `**Correction, v2**`
    block stating what v1 claimed, what was measured, and which is right, and corrects the option
    B bullet and the matching consequence. Deleting the `LC_ALL=C` sentence would have erased the
    fact that the decision rested on a partly wrong premise — while still reaching the right
    conclusion, which is itself worth knowing.
  - **Corrected `plan.md`'s `## Approach`**, which repeated the same example. An artifact is the
    current answer, not a historical record, so it is edited; the `plan` journal entry that also
    repeats the claim is **not** edited, because journals are append-only and this entry is the
    correction the spec asks for.
  - **Changed no code.** The implementation was already the right one; only the argument for it was
    mis-illustrated. A "fix" to the code here would have been the failure this protocol exists to
    prevent — reshaping the artifact around a documentation defect.
  - **Left `docs/architecture/overview.md` v4 alone.** Its sentence — the output "does not depend
    on `LANG`/`LC_ALL`" — is true as measured; it makes no claim about option B.
  - **Did not escalate.** None of `spec/question.md` §4's conditions applies: the intent is in the
    ADR and unchanged, the edit is reversible, it contradicts no decision, and a measurement rather
    than a preference settled it.
- **Questions raised:** none
- **Commands:**
  - `sed`/`grep` over `.claude/agile-skills/spec/doc-header.md` §4 → the two sentences the answer
    turns on, quoted verbatim in it
  - the edit script, asserting an exact single match for each replacement before writing (it
    refused once on a whitespace mismatch and was corrected rather than loosened)
  - `python3 .claude/agile-skills/scripts/board-gen .`; `validate-workspace .` → **exit 0**,
    0 errors, 0 warnings, 10 documents
- **Gates:**
  - `answer-is-propagated` (hard) → **pass** — both files named in `Q-001`'s `## Consequences` were
    written and re-read: ADR-0008 (v2, frontmatter, option B, the consequence bullet, the change
    log) and `plan.md`. The four listed as deliberately unchanged each name the reason
  - `answered-from-the-record` (hard) → **pass** — the answer quotes `doc-header.md` §4 and rests
    on `verify`'s measurement table, not on preference
  - `escalation-is-justified` (hard) → **pass, vacuously** — nothing escalated
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `item-resumed-correctly` (hard) → **pass, not applicable** — non-blocking question, no
    `resume-to` recorded or owed; BUG-0003 stays at `in-review`
- **Artifacts:**
  - `docs/architecture/adr/ADR-0008-writing-the-report-as-bytes.md` (v1 → v2)
  - `tracker/items/BUG-0003/artifacts/plan.md` (the `## Approach` sentence)
  - `tracker/items/BUG-0003/questions/Q-001.md` (answered), `journal.md` (this entry),
    `tracker/board.md` (regenerated)
- **Status:** `in-review` → `in-review` (unchanged)
- **Result:** ADR-0008 now rejects option B with an example that reproduces, and records that its
  first example did not. The decision is unchanged and better evidenced: `PYTHONIOENCODING=ascii`
  on `café.txt` is exit 0 for the chosen implementation and exit 1 for the alternative. No code
  changed, and the belief the decision was originally made on is still in the file.

## 2026-08-16T23:33:00Z — review-close v0.1.1 — reviewer

- **Item:** BUG-0003
- **Trigger:** status `in-review`, dispatched by `next` — the last open child of EP-001
- **Inputs read:** `item.md` (six criteria, the reproduction script, five quotations under
  `## Expected behaviour`), `history.md` (five rows), `journal.md` (all six entries, in full),
  `artifacts/plan.md`, `impl-report.md`, `verify-report.md`, `questions/Q-001.md` with both files
  its `## Consequences` names, `ADR-0008` **v2**, `ADR-0002`, `ADR-0006`, `ADR-0007`,
  `docs/architecture/overview.md` v4, `docs/product/vision.md` v1, and the diff `main..wi/BUG-0003`
  hunk by hunk
- **Decisions:**
  - **Accepted.** Two hunks at exactly one boundary; everything that builds the report is
    byte-identical to `main`, which is what makes AC5 checkable rather than hopeful.
  - **Opened both files named in `Q-001`'s consequences** rather than trusting the answer: ADR-0008
    is at v2 with the correction block, the corrected option B bullet, the rewritten consequence
    and a change-log row saying the decision is unchanged; `plan.md`'s `## Approach` carries the
    corrected example. Both are as the answer describes.
  - **Endorsed the routing of that correction.** `verify` found the ADR's example did not
    reproduce, filed a question rather than editing `docs/`, and `answer-questions` amended in
    place while keeping the wrong claim visible under `doc-header.md` §4. Had the finder made the
    edit, nobody would have reviewed it.
  - **Accepted the single-write constraint as a recorded rule**, not a defect: stdout is one
    buffered byte write; anything later that `print`s to stdout would interleave. I checked that
    nothing does today. It is in ADR-0008's consequences, in overview v4, and now in `## Notes`.
  - **Noted `test_ac3`'s weakness as declared, not hidden.** Two runs of a consistently crashing
    tool are byte-identical, so AC3's test alone would not have caught this bug; `implement`
    volunteered that and `verify` confirmed it. AC6 does not list it, which is correct.
  - **Closed before merging**, then fast-forwarded — `check-commit-refs` fails an empty range. The
    merge result was proved first on a throwaway branch: tree-identical, 60 tests green.
  - **Closed `EP-001` in the same execution**, this being its last child not `done`. The epic
    Definition of Done and the six success measures are applied in the epic's own journal entry,
    where a reader of the epic will find them.
  - **Filed no bug and no question.**
- **Questions raised:** none
- **Commands:**
  - `check-verify-freshness BUG-0003 wi/BUG-0003` → exit 0 ("only the record changed, 8 file(s)")
  - `check-commit-refs BUG-0003 wi/BUG-0003` → exit 0, 4 of 4
  - `git branch tmp/mc main; git merge --no-ff wi/BUG-0003` → `git diff --stat wi/BUG-0003 HEAD`
    empty; `python3 -m unittest discover` → 60 tests, `OK`; branch deleted
  - `git diff main..wi/BUG-0003 -- linecount.py` → two hunks, read line by line
  - `scripts/transition BUG-0003 --to done --actor review-close --outcome delivered` → applied
  - `git checkout main && git merge --ff-only wi/BUG-0003`; suite on `main` → 60 tests, exit 0
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1–D11 each with its own result and evidence in
    `review.md` `## Definition of Done`
  - `verification-postdates-the-code` (hard) → **pass** — exit 0
  - `commits-reference-the-item` (hard) → **pass** — 4 of 4
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 60 tests on the proved merge result and
    again on `main`
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and `git log`: *what
    was built and why* (the reproduction script, `plan.md`, ADR-0008 v2, four commits); *which
    skill decided what* (six journal entries with personas, the actor column); *what questions
    arose and how they were resolved* (`Q-001`: an ADR's example measured, disproved, corrected in
    place, with the original belief preserved); *what verification found* (six criteria with
    captured bytes, a locale matrix, and one documentation defect)
- **Artifacts:**
  - `tracker/items/BUG-0003/artifacts/review.md` (new)
  - `tracker/items/BUG-0003/item.md` — `status: done`, `outcome: delivered`, five accepted gaps in
    `## Notes`
  - `main` fast-forwarded to the branch head; `tracker/board.md` regenerated
  - `tracker/items/EP-001/item.md` and `journal.md` — the epic closed, with DE1–DE5 and the six
    success measures re-run
  - `journal.md` (this entry), `history.md` (one row)
- **Status:** `in-review` → `done` (outcome `delivered`)
- **Result:** BUG-0003 is delivered and merged: the folder that used to produce a traceback and
  exit 1 now prints two rows, a total and exit 0, with the undecodable byte reaching stdout exactly
  as `ls -b` and `wc` write it. The ADR behind it was tested rather than believed, found wrong in
  its illustration, and corrected without touching its decision. EP-001 closes with this item.
