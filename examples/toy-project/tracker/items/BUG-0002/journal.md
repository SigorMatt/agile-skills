# Journal — BUG-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-16T22:30:00Z — verify v0.1.1 — qa-engineer

- **Item:** BUG-0002
- **Trigger:** filed by an independent regression pass over `main` at
  `6d1e437b4293571296809b322c47fb0dc83d1ad6`, after EP-001 closed. Created directly at `ready`
  (`spec/ids-and-statuses.md` §4, `— → ready`, actor `verify`).
- **Inputs read:**
  - `tracker/items/WI-0001/item.md` — AC10 (what `no files` means) and AC1
  - `tracker/items/WI-0002/item.md` — AC3 (the `(all M files)` label) and AC9
  - `docs/architecture/adr/ADR-0002` (skip and report) and `ADR-0005` (`format_report`'s `None`
    sentinel and its stated misuse); `docs/architecture/overview.md` v2; `EP-001/item.md`
    `## Goal`
  - `linecount.py` on `main` (`main`'s `if top is None or not rows`, `format_report`) and
    `tests/test_linecount.py` (`test_unreadable_file_is_reported_and_skipped`)
  - `git show 5adc619:linecount.py`
  - `.claude/agile-skills/spec/dor-dod.md` §2, `spec/work-item.md` §3
- **Decisions:**
  - **Filed as a bug rather than a question, though no criterion covers the case directly.** The
    reading is not in doubt: stdout asserts `no files` about a folder that has files, and the
    assertion is byte-identical to the one made about a folder that really is empty. What is
    open is the wording of the replacement, and that is `plan`'s to choose — the same freedom
    WI-0001 AC11 and AC12 leave — not an ambiguity that stops the defect being a defect.
  - **`found-in: WI-0001`, not WI-0002.** `/tmp/bug2a` and `/tmp/bug2b` produce byte-identical
    stdout, stderr and exit code under `git show 5adc619:linecount.py`. WI-0002's `or not rows`
    short-circuit inherits the behaviour rather than causing it.
  - **Priority `medium`.** The tool exits 0 and the per-file `Permission denied` lines are on
    stderr, so the truth is available to a person at a terminal; only a pipe or a redirect hides
    it. That is a wrong answer, not a lost one, which ranks below BUG-0001.
  - **The `(all M files)` observation folded into this item's `## Notes` rather than filed.**
    `--top 5` on a two-file folder with one skipped file prints `total (all 1 files)`. WI-0002
    AC3 defines M twice in one sentence and a skipped file makes the halves disagree; the
    implementation follows the operative gloss, so the record settles it. It shares this bug's
    root cause and will move when this is fixed, which is why it is recorded here rather than as
    a fourth item nobody would connect to this one.
  - **AC4, AC5 and AC6 fence the behaviour that must not move** — the genuinely empty folder,
    the empty folder under any `--top`, and the mixed readable/unreadable folder — because the
    obvious fixes to AC1 are the ones that break those three.
- **Questions raised:** none on this item; `EP-001/Q-001` is non-blocking and unrelated to its
  content.
- **Commands:**
  - `mkdir -p /tmp/bug2a; printf 'a\n' > /tmp/bug2a/one.txt; printf 'b\nc\n' >
    /tmp/bug2a/two.txt; chmod 000 /tmp/bug2a/one.txt /tmp/bug2a/two.txt` → exit 0
  - `python3 linecount.py /tmp/bug2a` → exit 0; stderr `linecount: one.txt: Permission denied`
    and `linecount: two.txt: Permission denied`; stdout `no files`
  - `python3 linecount.py /tmp/bug2a 2>/dev/null` → exit 0, stdout `no files` alone
  - `python3 linecount.py /tmp/bug2c` (empty control folder) → exit 0, stdout `no files` —
    byte-identical to the line above
  - `chmod 444 /tmp/bug2b; python3 linecount.py /tmp/bug2b` → exit 0, two `Permission denied`
    lines on stderr, `no files` on stdout
  - `python3 linecount.py --top 3 /tmp/bug2a` → exit 0, same output; `--top` does not change it
  - `python3 linecount.py --top 5 /tmp/bug2d` (one readable, one not) → exit 0, `3  ok.txt` /
    `3  total (all 1 files)`, one stderr line
  - `python3 /tmp/qa-lc10/lc_wi1.py` on `/tmp/qa-lc5/allbad` and `/tmp/qa-lc5/mix` → byte-identical
    to trunk on all three streams
  - `.claude/agile-skills/scripts/new-item --id BUG-0002 --type bug --epic EP-001 --priority
    medium --status ready --actor verify --found-in WI-0001 …` → exit 0
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1; this item's own errors (stale
    `updated`, missing journal entry) fixed by this entry and a bumped timestamp
- **Gates:** the bug Definition of Ready, `spec/dor-dod.md` §2, criterion by criterion:
  - `RB1` steps runnable without further questions → **pass** — two numbered triggers and a
    numbered control, each with `mkdir`/`printf`/`chmod`/`python3` on absolute paths, a step that
    discards stderr to show what a pipe keeps, and a cleanup step
  - `RB2` actual behaviour quotes real output → **pass** — five verbatim blocks with commands,
    both streams identified, and exit codes, from the runs above
  - `RB3` expected behaviour cites what it contradicts → **pass** — WI-0001 AC10 quoted verbatim,
    plus `overview.md` v2's "Exit 0 means 'here is the answer'", ADR-0005's own statement of this
    misuse, and EP-001 `## Goal`
  - `RB4` `found-in` names the delivering item → **pass** — `found-in: WI-0001`, confirmed against
    that item's shipped build at `5adc619`
  - `RB5` acceptance criteria include a regression test → **pass** — AC7 requires tests for AC1
    to AC4, with those for AC1–AC3 failing against `6d1e437b`
- **Artifacts:**
  - `tracker/items/BUG-0002/item.md` (body written; `updated` bumped for `item.updated.stale`),
    `journal.md` (this entry), `history.md` (one row: `— → ready`)
  - `tracker/items/EP-001/artifacts/regression-verify-report.md`
  - `tracker/board.md` regenerated
- **Status:** `—` → `ready`
- **Result:** Filed. Two rules that are each correct — ADR-0002 skips a file it cannot read,
  WI-0001 AC10 prints `no files` for a folder with none — combine into a false answer when the
  skip list is everything. On stdout, a folder of unreadable files is indistinguishable from an
  empty one, and stdout is the stream that survives the pipe this tool exists to feed.

## 2026-08-16T22:58:30Z — answer-questions v0.1.1 — architect

- **Item:** BUG-0002
- **Trigger:** answering `BUG-0001/questions/Q-001.md` (the clock disagreement). This item was
  not the question's owner, but two of its timestamps were among the artifacts the answer
  corrected, and a correction that is not recorded where it happened is a silent rewrite
- **Inputs read:** `tracker/items/BUG-0002/item.md` and `journal.md`; `BUG-0001/questions/Q-001.md`;
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
  question. For this item: `workspace-valid` → **pass for BUG-0002`s own files** (no finding names
  this item); `answer-is-propagated` → **pass** (both corrections verified by re-reading)
- **Artifacts:** `tracker/items/BUG-0002/item.md` (`created` corrected), `journal.md` (heading
  corrected; this entry)
- **Status:** `ready` → `ready` (unchanged)
- **Result:** BUG-0002 carries a corrected `created`, an `updated` deliberately left anchored to its
  untouchable history row, and a corrected journal heading. Nothing about the defect it reports
  changed. It is ready to be planned as soon as the workspace validates again.

## 2026-08-16T23:12:00Z — plan v0.1.1 — architect

- **Item:** BUG-0002
- **Trigger:** status `ready`, dispatched by `next` — runnable once BUG-0001 closed; BUG-0002 and
  BUG-0003 share priority `medium`, and BUG-0002 wins on the selection key's third term, the ID
- **Inputs read:**
  - `tracker/items/BUG-0002/item.md` — the summary, both triggers, the control, the expected
    behaviour with its quotations, AC1–AC7, and the `## Notes` observation about `--top`'s label
  - `tracker/items/BUG-0001/item.md` and its `artifacts/review.md` — what the just-merged fix did
    and, more importantly, what it deliberately left alone here
  - `tracker/items/BUG-0003/item.md` — to know where this item's scope ends
  - `docs/architecture/adr/ADR-0002` (the skip rule), **`ADR-0005`** (which predicted this exact
    misuse), `ADR-0006`, `ADR-0001`, `ADR-0003`, `ADR-0004`;
    `docs/architecture/overview.md` v3; `docs/product/vision.md` v1
  - `tracker/items/WI-0001/item.md` AC10 and `WI-0002/item.md` AC9 — the criteria AC4 and AC5 make
    binding; `tracker/project.yaml`
  - the code on `main` at `15a0216`: `main` and `format_report` in full
- **Decisions:**
  - **Reproduced both triggers and the control before designing.** Trigger A → two stderr lines and
    `no files` on stdout, exit 0; with stderr discarded, stdout is byte-identical to the empty
    folder's. Trigger B (`chmod 444` folder) → the same. The `--top` observation in the item's
    notes reproduces too: `3  ok.txt` / `3  total (all 1 files)` for a two-file folder.
  - **The count of skipped files chooses the sentence** (ADR-0007). Route: **decided here** — the
    criteria pin that stdout must not claim there are no files and leave the wording to `plan`,
    exactly as WI-0001 AC11 left its stderr wording. Four options costed: silence, a zero total, a
    distinct sentence, a sentence carrying the count. Chose `no files could be read`: silence is
    not an answer, a zero total is a wrong number, and a count on stdout duplicates what stderr
    already itemises and would need its own criterion.
  - **The judgement stays in `main`, the rendering in `format_report`** via one more optional
    parameter. Rationale: ADR-0005 assigned "was the folder empty" to the caller and predicted in
    writing that a caller who forgot would print `no files` for a folder that had some — this bug
    is that prediction coming true. Extending the renderer the same way `--top` extended it keeps
    every byte of stdout produced in one function without moving the judgement into it.
  - **`--top` is not consulted when there are no rows** (assumption 3): there is nothing to limit,
    and WI-0002 AC9 already fixes the empty case for every N.
  - **A folder mixing unreadable files with unresolvable entries prints `no files could be read`**
    (assumption 2). At least one entry was a file; the unresolvable ones stay silent under
    ADR-0006. No criterion covers the mixture, so it is recorded rather than assumed silently.
  - **No overview version bump.** The function table's line for `format_report` still reads true
    with one more optional parameter, and no boundary in that document changes. ADR-0007 carries
    the decision. A version bump with no substantive change devalues every other one.
  - **Did not widen scope to `--top`'s label.** A folder of two files with one skipped still reads
    `total (all 1 files)`. The item's own notes call that an observation about WI-0002 AC3's two
    definitions of M, not a defect; the plan requires `implement` to state that the fix did not
    change what M counts.
- **Questions raised:** none. The one open point — the replacement wording — is the architect's to
  choose by the criterion's own words, and it is reversible in a default parameter value.
- **Commands:**
  - the item's two triggers, its control, and the `--top` case from `## Notes`, run verbatim →
    outputs quoted above
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
    (9 documents: ADR-0007 is new)
- **Gates:**
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `every-criterion-is-addressed` (hard) → **pass** — the mapping table in `artifacts/plan.md` has
    one row per criterion AC1–AC7. AC5 and AC6 map to existing tests that must keep passing, which
    is the honest evidence for "unchanged"; AC1–AC4 map to four new named tests
  - `project-commands-resolved` (hard) → **pass** — `commands.test` is `python3 -m unittest
    discover`, demonstrably runnable (50 tests pass on `main` today); lint and build stay null with
    ADR-0003 recording why
  - `decisions-recorded` (hard) → **pass** — five choices in `## Decisions and ADRs`: one points at
    ADR-0007, one at ADR-0007 plus ADR-0005, two at existing criteria, and three assumptions carry
    their reversal costs
  - `plan-is-executable-without-you` (advisory) → **pass** — steps 1–3 give the exact replacement
    code and the observable result of each; step 4 names every test; step 5 gives the mechanism for
    proving they fail on the old code
- **Artifacts:**
  - `tracker/items/BUG-0002/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0007-a-folder-whose-files-were-all-skipped.md` (new, v1)
  - `tracker/items/BUG-0002/journal.md` (this entry), `history.md` (one row), `board.md`
- **Status:** `ready` → `planned`
- **Result:** BUG-0002 has a six-step plan whose code change is a counter, a parameter and a
  branch. All seven criteria map to a step and a named test. The decision the criteria left open —
  what stdout should say when a folder's files were all skipped — is ADR-0007, chosen from four
  costed options, and the two neighbouring temptations (`--top`'s label, BUG-0003's printing path)
  are named as out of scope rather than absorbed.

## 2026-08-16T23:16:00Z — implement v0.1.0 — developer

- **Item:** BUG-0002
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/BUG-0002/item.md` (AC1–AC7, both triggers, the control, the `## Notes`
    observation about `--top`'s label), `artifacts/plan.md` (steps 1–6 and the mapping table),
    `history.md`, `questions/` (empty)
  - `docs/architecture/adr/ADR-0007` — the rule this executes — plus `ADR-0002`, `ADR-0005` and
    `ADR-0006`, whose behaviours this must leave intact; `docs/architecture/overview.md` v3
  - `tracker/items/WI-0001/item.md` AC10, `WI-0002/item.md` AC9, `BUG-0001/item.md` — the criteria
    AC4, AC5 and the ADR-0006 boundary make binding
  - the code on `main` at `558eaaa`: `main` and `format_report` in full
- **Decisions:**
  - **Executed plan steps 1–3 verbatim.** The counter sits beside the stderr line that already
    existed, so ADR-0002's output is untouched; the branch asks *why* there are no rows before
    choosing a sentence; the renderer's default is unchanged, which is what keeps AC4 and every
    WI-0001 test true.
  - **Added one test the plan did not name** —
    `test_the_renderer_still_defaults_to_no_files` — asserting both halves of ADR-0007's contract
    at the unit layer: the default is still `no files`, and the parameter produces the new
    sentence. AC4's only mapped evidence was end-to-end; this pins the default itself.
  - **Verified the neighbouring behaviours by hand rather than assuming the tests covered them**:
    `--top 5` on a folder with one skipped file still prints `3  total (all 1 files)`; the same
    folder without the flag still prints `3  ok.txt` / `3  total`; `--top 0`, `3` and `99` on an
    empty folder still print `no files`.
  - **Did not touch `--top`'s label**, which the plan required me to check and report. It counts
    the files that were listed, exactly as before; BUG-0002's notes call the `(all 1 files)`
    reading an observation about WI-0002 AC3's two definitions of M, not a defect.
  - **Did not put the skipped count on stdout.** ADR-0007 costed and rejected that; stderr already
    names each file.
  - **Left BUG-0003 alone**, though this fix edits the function two lines from where BUG-0003's
    `UnicodeEncodeError` is raised. This item changes *which* text is printed, never *how* text
    reaches stdout.
- **Questions raised:** none. Every criterion was decidable, and the one open choice — the wording
  — was already made by ADR-0007.
- **Commands:**
  - `git checkout -b wi/BUG-0002`; `scripts/transition BUG-0002 --to in-progress` → applied
  - the item's triggers on the branch head → trigger A: two stderr lines and
    `no files could be read`, exit 0; with stderr discarded, stdout is `no files could be read`;
    trigger B: the same; the control: `no files`, exit 0
  - `python3 -m unittest discover` → exit 0, `Ran 55 tests in 1.437s`, `OK`
  - `git show 6d1e437:linecount.py > linecount.py; python3 -m unittest discover -v` →
    `FAILED (failures=6, errors=1)`, including this item's `test_ac1_all_unreadable_does_not_claim
    _no_files`, `test_ac2_stdout_differs_from_an_empty_folder` and `test_ac3_untraversable_folder`.
    Restored; suite green at 55
  - by hand: `--top 5` on `/tmp/bug2d` → `3  total (all 1 files)`; no flag → `3  total`;
    `--top 0|3|99` on the empty folder → `no files` three times
  - `git commit` → `277c89c`; `scripts/check-commit-refs BUG-0002 wi/BUG-0002` → exit 0
- **Gates:** (full evidence in `artifacts/impl-report.md` `## Gates`)
  - `tests-pass` (hard) → **pass** — 55 tests, exit 0, on branch head `277c89c`
  - `lint-clean` (hard) → **skipped** — null command; ADR-0003. Not a pass
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors
  - `every-criterion-has-a-test` (hard) → **pass** — AC1–AC7 each mapped to a named test with the
    exact bytes or exit code it asserts; AC5 and AC6 rest on existing tests that must keep passing
  - `commits-reference-the-item` (hard) → **pass** — 1 of 1
  - `no-unplanned-scope` (advisory) → **pass** — nine lines of `linecount.py` and one appended test
    class; no other function, no other bug's symptom
- **Artifacts:**
  - `linecount.py` (175 → 184 lines), `tests/test_linecount.py` (515 → 587 lines, 50 → 55 tests)
  - `tracker/items/BUG-0002/artifacts/impl-report.md` (new)
  - branch `wi/BUG-0002`, commit `277c89c`, plus this execution's tracker commit
  - `journal.md` (this entry), `history.md` (two rows), `board.md`
- **Status:** `planned` → `in-progress` → `verifying`
- **Result:** stdout now distinguishes a folder that held no files from one whose files could not
  be read, and says which. The empty folder, the subdirectory-only folder, `--top` on both, the
  mixed readable/unreadable folder, ADR-0002's stderr lines and ADR-0006's silent skips are all
  unchanged — three of them checked by hand as well as by test. Three regression tests fail against
  `6d1e437`, which is what AC7 asks for.

## 2026-08-16T23:20:00Z — verify v0.1.1 — qa-engineer

- **Item:** BUG-0002
- **Trigger:** status `verifying`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/BUG-0002/item.md` — the seven criteria, read **first**, including the `## Notes`
    observation about `--top`'s label
  - `history.md`, `artifacts/plan.md`, then `artifacts/impl-report.md` — read last and treated as
    claims to check
  - `docs/architecture/adr/ADR-0007` (the rule), `ADR-0002` and `ADR-0006` (the neighbours it must
    not disturb), `ADR-0005` (which predicted this bug); `docs/architecture/overview.md` v3
  - `tracker/items/WI-0001/item.md` AC10 and `WI-0002/item.md` AC9 — what AC4 and AC5 make binding
  - the code on `wi/BUG-0002` at `e1e2985` (last code commit `277c89c`) and the diff against `main`
- **Decisions:**
  - **Built fixtures under `/tmp/vbug2-9bJv/`**, not the `/tmp/bug2a`…`/tmp/bug2d` folders the item
    names and `implement` reused. A `chmod` left in a helpful state by an earlier run is the
    easiest way to verify nothing.
  - **Used `cmp` for AC2 rather than eyeballing.** The criterion is that two stdouts differ; the
    honest check is a byte comparison of the two, with stderr discarded exactly as a pipe would.
  - **Exercised both ADR boundaries deliberately.** A folder of only symlink loops still prints
    `no files` (ADR-0006's skips are not files, so the counter never sees them), and a folder
    mixing an unreadable file with a loop prints `no files could be read` with one stderr line —
    which is plan assumption 2, declared untested by `implement` and now tested by hand here.
  - **Checked the implementation report's claim about `--top`'s label rather than accepting it**:
    `--top 5` on a folder with one skipped file still prints `3  total (all 1 files)`. Unchanged,
    as the item's notes require it to be.
  - **Recorded a coverage gap without filing a bug.** Nothing in the suite asserts that a folder of
    *only* unresolvable entries prints `no files`. The behaviour is correct — I ran it — and no
    criterion of this item covers that case, so it is a gap in tests, not a defect. Filing a bug
    for correct behaviour would misroute the work; it belongs in the item's notes at review.
  - **Nothing judged `ambiguous`**, no question filed.
- **Questions raised:** none
- **Commands:**
  - AC1: two `chmod 000` files → stdout `no files could be read`, stderr 2 lines both
    `Permission denied`, exit 0
  - AC2: the same folder and an empty one, both `2>/dev/null`, compared with `cmp` → **different**;
    empty prints `no files`
  - AC3: `chmod 444` folder with two files → stdout `no files could be read`, 2 stderr lines, exit 0
  - AC4: empty folder and subdirectory-only folder → stdout exactly `no files`, stderr 0 bytes,
    exit 0, both
  - AC5: `--top 0|3|99` on the empty folder → `no files`, exit 0, each
  - AC6: `ok.txt` (3 lines) + `chmod 000 no.txt` → `3  ok.txt` / `3  total`, one stderr line, exit 0
  - ADR-0006 boundary: folder of only symlink loops → `no files`, stderr 0 bytes, exit 0
  - mixed folder (unreadable file + loop) → `no files could be read`, one stderr line, exit 0
  - AC7: `git show 6d1e437:linecount.py > linecount.py; python3 -m unittest discover` → exit 1 with
    this item's three tests among the failures; restored → `Ran 55 tests`, `OK`
  - five mutations, each restored after: branch removed → 3 failures; sentence used for every empty
    result → 5 failures including three of WI-0001's and WI-0002's; renderer default changed → 8
    failures; counter never incremented → 3 failures; `6d1e437` → 7 failures
  - `git diff main..wi/BUG-0002 -- tests/test_linecount.py | grep -c "^-[^-]"` → `0`
  - `scripts/validate-workspace .` → exit 0
- **Gates:**
  - `tests-pass` (hard) → **pass** — 55 tests, exit 0, run here on the branch head
  - `lint-clean` (hard) → **skipped** — null command (ADR-0003); not a pass
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `every-criterion-independently-checked` (hard) → **pass** — seven rows, each a command run here
    with quoted output
  - `negative-cases-exercised` (hard) → **pass** — seven conditions plus the two ADR boundaries
  - `tests-would-fail-without-the-change` (advisory) → **pass** — five mutations, five caught
- **Artifacts:**
  - `tracker/items/BUG-0002/artifacts/verify-report.md` (new), carrying
    `Verified-commit: e1e29850d6923ecfd7b05bf29a6694a36c333e46`
  - `tracker/items/BUG-0002/item.md` — all seven criteria ticked
  - no bug items; `journal.md` (this entry), `history.md` (one row)
- **Status:** `verifying` → `in-review`
- **Result:** stdout now tells a folder that held no files apart from one whose files could not be
  read, and every rule this fix sits between — WI-0001 AC10, WI-0002 AC9, ADR-0002's stderr line,
  ADR-0006's silent skips — was exercised and holds. Five mutations, all caught, including the two
  that make the new sentence the general case. One coverage gap recorded for the reviewer.

## 2026-08-16T23:23:00Z — review-close v0.1.1 — reviewer

- **Item:** BUG-0002
- **Trigger:** status `in-review`, dispatched by `next`
- **Inputs read:** `item.md` (seven criteria, both triggers, the `--top` observation in `## Notes`),
  `history.md` (four rows), `journal.md` (all four entries, in full), `artifacts/plan.md`,
  `impl-report.md`, `verify-report.md`, `questions/` (empty), `ADR-0007`, `ADR-0002`, `ADR-0005`,
  `ADR-0006`, `docs/architecture/overview.md` v3, and the diff `main..wi/BUG-0002` hunk by hunk
- **Decisions:**
  - **Accepted.** Three code hunks, each traceable to a plan step and a criterion; the `elif top is
    None` and `else` arms are the previous code unchanged, so WI-0002's slice, total and label are
    byte-identical.
  - **Judged the fix's placement against its specific risk** — making the new sentence the general
    case for any empty result. `verify` mutated it into that shape twice and five tests objected,
    three of them WI-0001's and WI-0002's own. That is the strongest available evidence that AC4
    and AC5 are protected by more than this item's own tests.
  - **Accepted `no files could be read` as a new interface**, recorded in ADR-0007's consequences:
    stdout now has three shapes rather than two. Nothing in this project parses it.
  - **Accepted D7 as "no document needed updating", with the reason stated** rather than treated as
    an absence. The overview's line for `format_report` still reads true with one more optional
    parameter; ADR-0007 carries the decision. A version bump with no substantive change devalues
    every other one.
  - **Accepted the coverage gap `verify` recorded** — no test for a folder of only unresolvable
    entries — and carried it into `## Notes`. The behaviour is right and was run by hand; only the
    test is missing, so filing a bug would misroute correct behaviour into a defect queue.
  - **Closed before merging**, then fast-forwarded, for the same reason as the previous items:
    `check-commit-refs` fails an empty range. The merge result was proved first on a throwaway
    branch — tree-identical, 55 tests green.
  - **Left `EP-001` open**: BUG-0003 is still `ready`, so epic DE1 is not met.
  - **Filed no bug and no question.**
- **Questions raised:** none
- **Commands:**
  - `check-verify-freshness BUG-0002 wi/BUG-0002` → exit 0 ("only the record changed, 5 file(s)")
  - `check-commit-refs BUG-0002 wi/BUG-0002` → exit 0, 3 of 3
  - `git branch tmp/mc main; git merge --no-ff wi/BUG-0002` → `git diff --stat wi/BUG-0002 HEAD`
    empty; `python3 -m unittest discover` → 55 tests, `OK`; branch deleted
  - `git diff main..wi/BUG-0002 -- linecount.py` → read hunk by hunk, quoted in `review.md`
  - `scripts/transition BUG-0002 --to done --actor review-close --outcome delivered` → applied
  - `git checkout main && git merge --ff-only wi/BUG-0002`; suite on `main` → 55 tests, exit 0
- **Gates:**
  - `definition-of-done` (hard) → **pass** — D1–D11 each with its own result and evidence in
    `review.md` `## Definition of Done`
  - `verification-postdates-the-code` (hard) → **pass** — exit 0
  - `commits-reference-the-item` (hard) → **pass** — 3 of 3
  - `tests-pass-on-the-merge-result` (hard) → **pass** — 55 tests on the proved merge result and
    again on `main`
  - `workspace-valid` (hard) → **pass** — exit 0, 0 errors, 0 warnings
  - `record-is-reconstructible` (hard) → **pass** — from `tracker/`, `docs/` and `git log`: *what
    was built and why* (the item's triggers, `plan.md`, ADR-0007, three commits); *which skill
    decided what* (four journal entries with personas, the actor column); *what questions arose*
    (none on this item — the wording was the architect's to choose by the criterion's own words);
    *what verification found* (seven criteria with quoted output, five mutations, two ADR
    boundaries exercised, one coverage gap)
- **Artifacts:**
  - `tracker/items/BUG-0002/artifacts/review.md` (new)
  - `tracker/items/BUG-0002/item.md` — `status: done`, `outcome: delivered`, five accepted gaps in
    `## Notes`
  - `main` fast-forwarded to the branch head; `tracker/board.md` regenerated
  - `journal.md` (this entry), `history.md` (one row)
- **Status:** `in-review` → `done` (outcome `delivered`)
- **Result:** BUG-0002 is delivered and merged. A folder whose files were all skipped now says so
  on stdout instead of claiming to be empty, and every rule the fix sits between — WI-0001 AC10,
  WI-0002 AC9, ADR-0002's stderr line, ADR-0006's silent skips — is intact and was exercised.
  EP-001 stays open behind BUG-0003.
