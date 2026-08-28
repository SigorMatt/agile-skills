# Review — WI-0002

## What I examined

**The record.** `item.md` with all thirteen criteria; `history.md`'s eight rows;
`journal.md`'s eight entries in full; `plan.md`; `impl-report.md`; `verify-report.md`;
`questions/Q-001.md` and `Q-002.md` including their `## Consequences`.

- **History chains without a gap** and its last row matches `item.md`: `—` → `draft` →
  `awaiting-answer` → `draft` → `ready` → `planned` → `in-progress` → `verifying` → `in-review`.
  The two `refine` rows are two rounds, not a repeat: the first suspended the item to ask the
  stakeholder, the second rewrote AC1–AC5 into AC1–AC13 against their answers.
- **Eight history rows, eight journal entries**, one per execution: `intake`, `refine`,
  `answer-questions`, `refine`, `plan`, `implement` (branch), `implement` (report), `verify`.
- **Both questions are `answered`**, `answered-by: human`, with `## Consequences` naming four
  files each. I opened all of them rather than trusting the list: `item.md` `## Notes` carries the
  layout decision and the two-band decision with the question cited; `refinement-qa.md` is
  `status: recorded`; `docs/product/vision.md` is at v4 with the change-log row naming
  `answer-questions` and WI-0002; `tracker/items/WI-0003/item.md` `## Notes` carries both
  consequences for the rule format.

**The change.** `git diff main..wi/WI-0002`, hunk by hunk, 14 files.

- `tidy/rules.py` — `DEFAULT_BANDS` and `band_for`: plan step 1, ADR-0005 `## Decision`.
- `tidy/planner.py` — the once-per-run clock, `now - st_mtime`, `os.path.join(band, type_folder)`,
  and `_blocking_component`: plan steps 2 and 3, serving AC1–AC5, AC12.
- `tidy/apply.py` and `tidy/cli.py` — **absent from the diff stat**, which is what the plan
  predicted and what makes ADR-0002's layering claim still true.
- `tests/support.py` — the `age()` helper: plan step 4.
- `tests/test_rules.py`, `tests/test_planner.py`, `tests/test_cli.py` — plan steps 5–7, plus the
  three declared deviations.
- `README.md` — plan step 8; `docs/architecture/overview.md` v3 — plan step 9.
- **Every hunk maps to a plan step or a criterion.** The one hunk `impl-report.md` flagged as
  judgement rather than a step — two extra bullets under README's "What it will not do" — states
  AC10 and the accepted mixed tree, both of which the item already fixes. Not unrequested scope:
  it is documentation of behaviour a criterion already requires.

**The eleven pre-existing tests that changed** (`impl-report.md` deviation 2), read line by line
rather than taken on trust, because "the change made the old tests fail, so the old tests changed"
is the shape a defect hides in. Every removed line is a path with the band added
(`documents/report.pdf` → `recent/documents/report.pdf`), a docstring, or an import. No assertion
was deleted or weakened, and one was **strengthened**:
`test_destination_folders_are_created_as_needed` now asserts both `recent/` and `recent/images/`
where it asserted one folder before.

**The claims (D12), from their citations rather than from the prose.**

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| "`build_plan` reads the clock once, ages each recognised file by `now - st_mtime`, and puts the band above the type folder" | `overview.md` §"What is deliberately not here" | `tidy/planner.py:40`, `:55`, `:56` | true — one `time.time()` before the loop, `now - entry.stat().st_mtime`, `os.path.join(band, type_folder)` |
| "`apply_plan` already created the destination's parent with `os.makedirs`" | `overview.md` §"Where the remaining item will touch this" | `tidy/apply.py:24` | true — `os.makedirs(os.path.dirname(destination), exist_ok=True)` |
| "`apply.py` and `cli.py` were not touched at all" | same | `git diff main..wi/WI-0002 --stat` | true — neither file appears |
| "Every destination is decided in `planner.py` and nowhere else" | `overview.md` §"The shape of the system"; ADR-0002 | `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py` | still true — `apply.py` consumes `action.destination`, `cli.py` renders it, neither composes one |
| "the two bands and the 365-day boundary are a constant table" | `overview.md`, ADR-0005 | `tidy/rules.py:34-37` | true — `(("recent", 365 * 24 * 3600), ("old", None))`, no configuration read |
| "the comparison is half-open, so a file exactly on the boundary falls into the older band" | ADR-0005 `## Decision` §1 | `tidy/rules.py:48` (`age_seconds < bound`) and `verify-report.md`'s `band_for(31536000) = 'old'` | true |
| "A malformed table with no `None` bound would classify a sufficiently old file as no band" | ADR-0005 `## Consequences` | `tidy/rules.py:47-49` | true — the loop falls through and returns `None` implicitly |
| "The top level of a tidied folder is `recent/` and `old/`, and the type folders sit inside" | `vision.md` v4 §"What it is for" | the AC1 and AC5 runs in `verify-report.md`, re-read against `tidy/planner.py` | true |
| "It does not go looking inside subfolders … including the ones it made on an earlier run" | `vision.md` §"What it is not" | `tidy/planner.py:47`, and AC9–AC11's runs | true |
| the `os.link` / `_move_without_a_link` paragraph and its BUG-0002 citation | `overview.md` §"The shape of the system" | `tidy/apply.py:30`, `:49-63` | still true — untouched by this item, and still honest about the fallback |

**The declared gaps** — `verify-report.md` `## Not verified, and why` (six) and `impl-report.md`
`## What I did not do` (five). Each is dispositioned under `## Accepted gaps`.

**The merge**, on a detached worktree: `git worktree add --detach /tmp/tidy-trial main`,
`git -C /tmp/tidy-trial merge --no-ff wi/WI-0002` → merge commit `f0adf5e0`, tests and lint run
**inside the trial**, worktree removed, and `git rev-parse main` compared before and after —
`47c2dd8a568dc4a1d4ff498574de11c2d4d058f9` both times.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox ticked | **pass** | 13 of 13 `- [x]` in `item.md`, 0 unticked (`grep -c`) |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table has one row per AC1–AC13, each naming a command run during verification and quoting its actual output; no row cites `impl-report.md` |
| D3 | gates passed on the **final** state of the code | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 63 tests … OK`, and `python3 -m compileall -q tidy tests` → exit 0, both re-run by this review on the trial merge result `f0adf5e0` — the state the project actually gets, not the branch |
| D4 | no open blocking question | **pass** | both questions on the item are `status: answered`; `validate-workspace` reports 0 open across 7 items |
| D5 | a journal entry per execution, history chains | **pass** | eight rows, eight entries, listed above; last row `verifying → in-review` matches `status: in-review` |
| D6 | design decisions in an ADR, cited | **pass** | ADR-0005 records the age rule's shape with three options and the three details it fixes; cited from `plan.md` `## Decisions and ADRs`, from `impl-report.md`, from `overview.md` v3 and from `tidy/rules.py`'s and `planner.py`'s docstrings. Read in full: its `## Decision` matches the code line for line |
| D7 | invalidated documents updated, version bumped, change-log row | **pass** | `docs/architecture/overview.md` v2 → v3 with the row `3 \| 2026-08-27T18:15:50Z \| implement \| WI-0002 \| …`; both statements the change falsified — the `rules.py` module row and "No age handling" — are rewritten. `README.md` is not versioned (it is user documentation, and AC13 governs it) |
| D8 | every commit on the branch references the item | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 11 commit(s) on main..wi/WI-0002 name WI-0002` |
| D9 | merged into the trunk | **pass** | merged after this review was written and the item closed, in the order the procedure requires (`commits-reference-the-item` inspects `main..wi/WI-0002`, which merging empties). Merge commit `84605d9bf2c810a37114abfd16196c2d9c25fbb2` on `main`; the suite re-run on `main` afterwards → exit 0, `Ran 63 tests … OK` |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: "verified at 93a95859; wi/WI-0002 has moved to c72f62e1 but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code" |
| D11 | `review.md` exists and says what was examined | **pass** | this file; `## What I examined` is its first section |
| D12 | claims in `docs/` about the touched behaviour are still true; new absolute claims carry resolvable citations | **pass** | the ten-row table above, each decided by opening the cited code rather than by re-reading the sentence. `lint-claims --changed-since main` → exit 0, 1 document checked |

## Findings

1. **`--help` had gone stale — already filed as BUG-0003 by `verify`, and I agree with the
   routing.** `python3 -m tidy --help` still says "chosen by file type" and names one rule table.
   I ran it rather than reading about it. No WI-0002 criterion covers the help text and WI-0001
   AC1's three requirements of it still hold, so it is neither this item's failure nor WI-0001's.
   `found-in: WI-0002` is right: the sentence is WI-0001's, but what it is wrong about is age
   routing. **Not a send-back.**

2. **AC13's regression test is weakly sensitive to its "last modified" clause.** `verify` found
   it and I reproduced it: changing `**last modified**` → `**last opened**` on `README.md`'s line
   43 — the sentence a user reads — leaves the suite green, because the assertion is a whole-file
   substring and the phrase occurs three times. `impl-report.md` claims that exact mutation fails
   the test; it does not, and that inaccuracy is worth naming because the report is what a later
   reader would otherwise trust. The **criterion** passes — the README does state the field, which
   I confirmed by reading it. Recorded as an accepted gap rather than filed: it is a weakness in
   the regression net, not a defect in delivered behaviour. **Not a send-back.**

3. **Nothing in the diff contradicts an ADR.** ADR-0002's "every destination decided in
   `planner.py`" survives because the band is composed there; ADR-0003's `os.link` path is
   untouched; ADR-0005 is this item's own and matches the code. No question needed.

4. **The code is one I would be comfortable maintaining.** `_blocking_component` walks components
   in order and returns the first blocked one, so the `leave` reason names the component a user
   can actually act on — I ran the two-component case (`old/documents` as a regular file) and got
   `['old/documents' exists and is not a folder]`. The one convention a reader must learn is the
   `None` bound on `DEFAULT_BANDS`' last entry, and ADR-0005 `## Consequences` says so explicitly
   including what a malformed table would do. No duplicated rule that can drift: the band names
   exist once, in `DEFAULT_BANDS`, and `README.md`'s table is parsed against it by a test.

5. **The three declared deviations from the plan are all sound.** AC13's test moved to
   `test_rules.py` where the README-parsing helper already lives, which avoids duplicating three
   things into a module that imports nothing from `tidy`. The eleven edited tests are faithful,
   checked line by line. The extra test `test_the_whole_run_is_measured_against_one_instant`
   covers ADR-0005 §3, which no criterion reaches — an addition that closes a gap rather than
   widening scope.

## Accepted gaps

Each is now in `item.md` `## Notes`, because a gap recorded only in a report stops being read the
moment the item closes.

| gap | source | disposition |
|-----|--------|-------------|
| symlinks are aged by their target's `mtime` | `impl-report.md` 3; `verify-report.md` 5 | **accepted** — consistent with WI-0001's `entry.is_dir()`, no criterion covers it, changing it would be unrequested behaviour |
| clock skew and copied/restored files are aged by the date the filesystem reports | `impl-report.md` 4; `verify-report.md` 4; `plan.md` `## Risks` | **accepted** — inherent in "anything I haven't touched in a year"; there is no other field to read |
| AC4's universal "no third band name" clause decided by its grounds, not by exhaustion | `verify-report.md` 1 | **accepted** — unexhaustible by construction; the grounds are checkable and were checked |
| the exact 365-day boundary settled through `band_for`, not through a folder | `verify-report.md` 2 | **accepted** — `build_plan` reads its own clock, so no fixture can pin the instant; the two measurements together decide AC4 |
| AC13's test is weakly sensitive to its "last modified" clause | this review, finding 2 | **accepted** — the criterion passes; WI-0003 rewrites this documentation and its tests |
| no migration of a folder the pre-band version tidied | `impl-report.md` 2 | **already recorded** — `item.md` `## Out of scope`, AC9 fixes the behaviour, and `README.md` tells the user it will not happen and why |
| other filesystems not exercised | `verify-report.md` 3 | **already recorded** — BUG-0002 is the open item about a filesystem that behaves differently |
| `overview.md` v3's completeness not judged by `verify` | `verify-report.md` 6 | **resolved here** — D7 and D12 above, decided by reading the document against the code |
| BUG-0001 and BUG-0002 untouched | `impl-report.md` 5 | **correct** — separate items with their own criteria; not this item's to fix |

## Verdict

**Accepted, merged and closed. `outcome: delivered`.**

All thirteen acceptance criteria are met and independently evidenced, every Definition of Done
criterion passes with its own evidence, the record is complete enough that a reader with only
`tracker/`, `docs/` and `git log --grep WI-0002` can reconstruct what was built, who decided what,
which questions the stakeholder answered and what verification found. `apply.py` and `cli.py`
were not touched, which is the architectural prediction this item was the first real test of.

Merged into `main` as `84605d9bf2c810a37114abfd16196c2d9c25fbb2`, after the item was closed —
that order is required, because `check-commit-refs` reads `main..wi/WI-0002` and merging empties
the range. The suite was re-run on `main` after the merge: exit 0, `Ran 63 tests … OK`.

One defect belongs elsewhere and is filed as **BUG-0003**; nine gaps are accepted with reasons,
and all of them now live in `item.md` `## Notes` rather than only in a report.
