# Review — WI-0002

## What I examined

- **The item** — `item.md`'s fourteen criteria, its `## Out of scope`, and both `refine` notes;
  `history.md`'s six rows; `journal.md` in full, all eight entries (`intake`, two
  `answer-questions`, `refine`, `plan`, two `implement`, `verify`).
- **The reports** — `plan.md`'s eight steps, AC mapping, five assumptions and four risks;
  `impl-report.md`'s three declared deviations and its `## What I did not do`;
  `verify-report.md`'s fourteen rows, fourteen negative cases and fifteen mutations.
- **The diff**, `git diff main..wi/WI-0002`, hunk by hunk — 686 added lines across
  `recall/schedule.py` (new), `recall/cli.py`, `tests/test_schedule.py` (new) and
  `tests/test_review.py` (new). Each hunk mapped to a plan step; the mapping is in `## Findings`.
- **The ADRs the change touches** — `ADR-0002` (the ladder and the due comparison), `ADR-0003`
  (no cap, the stated count, the clean quit), `ADR-0006` (standard library only, the two gate
  commands), `ADR-0007` (`rung` 0–4 and the file's format), `ADR-0008` (the path and the
  write discipline), `ADR-0009` (the schedule module's purity). None is contradicted; the
  reasoning is under `## Findings`.

### The claims audit — from the citations, not from the prose

Each absolute or load-bearing claim in `docs/` about what this item touched, with the thing its
citation points at **opened and read**:

| the claim | what I opened | verdict |
|-----------|---------------|---------|
| `overview.md`: *"`add` is built; `review` is planned"* `[src: recall/cli.py]` `[src: …/plan.md]` | `recall/cli.py` — `_parser()` registers `add` **and** `review`; `main()` branches on `arguments.subcommand` | **false** → repaired, v4 |
| `overview.md`'s opening: *"as it stands after WI-0001 was planned and before any of it was built"* `[src: WI-0001]` | `tracker/items/WI-0001/item.md` — `status: done`, `outcome: delivered`; `git log main` shows the merge `1dfbeb6` | **false** → repaired, v4 |
| `overview.md`: *"WI-0002 is the item that puts it in"* `[src: …/plan.md]` | this item's branch — `recall/schedule.py` exists and is merged here | **false** (tense) → repaired, v4 |
| `overview.md`: *"Pure functions: no file, no environment, no printing, and the day is passed in by the caller"* `[src: ADR-0009]` | `recall/schedule.py` in full — imports `datetime` and `recall.store` only; no `open`, no `os`, no `print`, no `date.today()`; `is_due`, `due_positions`, `after_right`, `after_wrong` all take `today` | **true** → citation extended to `[src: recall/schedule.py]`, v4 |
| `overview.md`: *"Nothing above it knows the format"* `[src: recall/store.py]` `[src: ADR-0007]` | `recall/cli.py` and `recall/schedule.py` — neither mentions `front: `, `back: `, `rung: ` or `due: `; both work on the `Card` record | **true**, unchanged |
| `overview.md`: *"a test run does not touch a real deck"* `[src: ADR-0008]` | all four test modules — `test_add`, `test_store`, `test_review` set `RECALL_CARD_FILE` into a `TemporaryDirectory` and pop `XDG_DATA_HOME`; `test_schedule` opens no file at all | **true**, but the sentence around it said tests "drive the command-line entry point", which `test_schedule.py` does not → wording repaired, v4 |
| `overview.md`: *"three modules with two seams"* `[src: WI-0001]` `[src: ADR-0009]` | `recall/` — `cli.py`, `schedule.py`, `store.py` | **true** as of this item |
| `overview.md`: *"A subcommand exits `0` when it did what was asked, and non-zero when it did not"* `[src: WI-0001 AC7]` | `recall/cli.py` — `review()` returns `EXIT_OK` when it finished, was stopped, or found nothing due; an unparsable file reaches `main()`'s handler and returns `EXIT_REFUSED`; `argparse` exits 2 on a bad command line | **true** |
| `vision.md`: *"Every due card is offered and none is withheld; the session says how many there are before the first one; and they can stop part-way without losing what they have answered."* `[src: WI-0002]` `[src: EP-001/Q-005]` `[src: ADR-0003]` | `verify-report.md`'s AC2, AC10 and AC9 rows, and the criteria they cite | **true** — proposed when written, delivered now |
| `vision.md`: *"Still to be put to them: what the person types … and in what order due cards are offered"* `[src: WI-0002]` | `tracker/items/WI-0002/artifacts/refinement-qa.md` and WI-0002's `refine` history row — every one is marked `[assumed]` under `EP-001/Q-004`; nothing was put to the stakeholder | **false** → repaired, v6 |
| `vision.md`: *"A card is due when its date is today or earlier, so a missed day costs nothing"* `[src: EP-001/Q-003]` | `EP-001/Q-003`'s `## Answer`, verbatim, and `schedule.is_due` | **true** — the code matches the stakeholder's own sentence |
| `overview.md` `## Where the cards live` (set-and-non-empty) `[src: recall/store.py]` | `card_file_path()` — `if override:` and `if not data_home:` both treat an empty value as unset | **true**, corrected at WI-0001's close and still true |

`lint-claims --context work-item --changed-since main` then ran over a **non-empty** window —
*"2 document(s) in 2 path(s) differ from main"* — and exited 0. That window is only non-empty
because this execution edited those two documents; before the repair it read *"0 document(s) in 0
path(s)"* and would have passed over anything. The gate's verdict is therefore evidence about the
new text, not about the audit; the audit is the table above.

No standing ADR needed a §4b correction: every ADR sentence read here was true and already
sourced, and `lint-claims --all` reports 0 errors over the whole document set.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | `grep -c '^- \[x\] AC'` → `14`; `grep -c '^- \[ \] AC'` → `0` |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | fourteen rows, each naming a command `verify` ran against a hand-seeded card file with its actual output quoted; none cites `impl-report.md`. Spot-checked three by re-reading the quoted output against the criterion's sentence: AC8's three seeds, AC11's four runs, AC14's `line 5` message |
| D3 | gates passed on the final state | **pass** | `implement`'s eight on `e595079`, the last code commit; `verify`'s six on `c706d83`; mine on the merge result `9027dc4`. Nothing after `e595079` touches `recall/` or `tests/` — `git diff e595079..229a49f8 --stat` is `tracker/` and `docs/` only |
| D4 | no open blocking question | **pass** | `tracker/items/WI-0002/questions/` does not exist; no question was filed on this item at any point |
| D5 | a journal entry per execution, history chains | **pass** | six history rows chaining `— → draft → ready → planned → in-progress → verifying → in-review`, last row matching `item.md`; eight journal entries, two of them (`answer-questions`, 11:19 and 11:27) recording epic-level answers propagated into this item with no status change. `validate-workspace` → 0 errors |
| D6 | design decisions in an ADR, cited | **pass** | `ADR-0009` is new for this item and is cited from `plan.md`'s decisions table and from `plan`'s journal entry. Everything decided during implementation — the refusal wording derived from `accepted`, the prompt text, `PROMPT_MARK` — is inside `plan.md`'s stated latitude (assumption 4) and is recorded in `impl-report.md` `## Deviations from the plan`, not silently |
| D7 | invalidated documents updated, version bump, change-log row | **pass, by this execution** | `overview.md` v3 → **v4** and `vision.md` v5 → **v6**, each with a change-log row naming what was overtaken. `implement` and `verify` both declared the staleness and correctly declined to fix it — `spec/doc-header.md` §5 names those two skills as ones that do not write to `docs/` — so it arrived here, which is where D7 is checked |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, *"all 5 commit(s) on main..wi/WI-0002 name WI-0002"* |
| D9 | merged into the trunk | **pass** | merged after this review was written and after the item was closed, in that order — `check-commit-refs` reads `main..branch`, which is empty once merged |
| D10 | verification postdates the code | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: *"verified at c706d837; wi/WI-0002 has moved to 229a49f8 but only the record changed (7 file(s) under tracker/ or docs/)"*. The last commit touching `recall/` or `tests/` is `e595079`, which precedes `c706d83` |
| D11 | the review record exists and says what was examined | **pass** | this file; `## What I examined` is first and names the diff range, the eight journal entries, the six ADRs and twelve audited claims |
| D12 | claims in `docs/` still true, absolutes sourced | **pass** | the audit table above — twelve claims, each decided by opening what it cites. Four were false and are repaired; one was true but its surrounding sentence was incomplete and is repaired; `lint-claims --context work-item --changed-since main` → exit 0 over 2 documents, and `--all` → exit 0 |

## Findings

**The diff, hunk by hunk.** Every hunk traces to a plan step, and nothing else is in it:

| hunk | serves |
|------|--------|
| `recall/schedule.py`: `INTERVALS`, `FIRST_RUNG`, `is_due`, `after_right`, `after_wrong`, `_rescheduled` | plan step 1; AC5, AC6, AC3 |
| `recall/schedule.py`: `due_positions` | plan step 2; AC2, AC12 |
| `recall/cli.py`: `PROMPT_MARK`, `_named`, `_ask` | plan step 3; AC11, AC13 |
| `recall/cli.py`: the `review` subparser and `main()`'s branch | plan step 4; AC1 |
| `recall/cli.py`: `review`, `_stopped` | plan step 5; AC1, AC4, AC7–AC11, AC14 |
| `tests/test_review.py` | plan step 6 |
| `tests/test_schedule.py` | plan step 7 |
| the `schedule` import and the corrected comment above `parse_args` | plan steps 4 and 5 |

Nothing in the diff touches `add()`, `store.py`, `tests/test_add.py` or `tests/test_store.py`;
`git diff main..HEAD` over those three files is empty.

**No ADR is contradicted.** `ADR-0009`'s purity requirement is met literally — `schedule.py`
imports `datetime` and `recall.store` and calls no clock. `ADR-0007`'s format is unchanged: no
field was added, and `store.py` is untouched. `ADR-0002`'s ladder appears exactly once, as
`INTERVALS`, rather than being restated in `cli.py`. `ADR-0006`'s standard-library-only rule holds
(`datetime`, `argparse`, `sys` in the tool; `subprocess`, `tempfile`, `unittest`, `time`,
`hashlib` in tests). `ADR-0003`'s three properties are AC2, AC10 and AC11, all verified.

**One maintainability finding, accepted rather than sent back.** What each prompt accepts is
stated in **two** places: the literal hint inside the prompt string in `review()` (*"Enter to see
the back, q to stop."*) and `_named(accepted)`, which builds the refusal line from the tuple. Add
a third accepted key and only the second would follow. It is accepted rather than fixed because
the drift is caught: `test_each_prompt_names_what_it_takes` pins both prompt strings and
`test_an_unrecognised_key_re_asks_the_same_card` pins both refusal strings, so a change to
`accepted` without a change to the hint fails the suite. Recorded in the item's `## Notes` so it
survives this review.

**Two things I checked specifically because they are easy to get wrong, and both are right.**
`due_positions()` returns **positions**, and a deck with two cards sharing a front side was driven
through a session with the two answered differently: the file afterwards holds `first-back` at
rung 2 due +3 and `second-back` at rung 1 due +1, so the session wrote back the card it asked
about rather than the first match — which `WI-0001 AC6` makes a real case. And `_stopped()` is
reached from four distinct paths (`q` and end-of-input, at each of two prompts), all four of which
`verify` exercised with the card file byte-identical afterwards.

**`review()`'s `OSError` path is undescribed but correct.** A failure inside `store.save()`
mid-session propagates to `main()`'s existing handler, which prints the path and the error to
standard error and exits 1, leaving the answers already written intact. No criterion covers it and
none needs to; noted so the next reader does not have to work it out.

## Accepted gaps

Each is written into `item.md`'s `## Notes` by this execution, because a gap that lives only in a
report nobody reopens has stopped being on the record:

1. **A session and a concurrent writer.** `plan.md` assumption 5: the session does not re-read the
   card file after it starts, so anything another process writes mid-session is overwritten at the
   next save. No criterion covers it; `ADR-0001` makes the tool single-user. Same shape as the gap
   WI-0001 accepted for concurrent writers.
2. **WI-0001's AC2, the literal machine restart.** Out of reach here as it was there, and already
   an accepted gap on that item. What stands in for it is that a *new process* the same day reads
   what an earlier process wrote — AC7, demonstrated three times.
3. **No measurement at backlog scale.** `plan.md` names the cost — one whole-file rewrite and two
   `fsync` calls per answer — and no criterion bounds a session's length, deliberately, because
   the stakeholder traded that bound for the honest count (`EP-001/Q-005`). It was observed at
   three-card scale and at no larger one.
4. **The prompt hint is stated twice**, as above.

## Verdict

**Accepted and closed, `outcome: delivered`.**

Fourteen criteria, each demonstrated by `verify` with a command and its output and each
independently traceable to a hunk of the diff. The trial merge into a detached worktree of `main`
(`9027dc4`) ran 60 tests green and `compileall` clean on the merge result, and `git rev-parse
main` returned `45f8d039…` both before and after the trial. Nothing was sent back and no bug item
was filed.

The one thing this review had to do rather than check was D7: `overview.md` and `vision.md` each
carried a sentence that what was built had made false. Both were repaired here, with a version
bump and a change-log row, and every repaired sentence is in the audit table above with the file
I opened to decide it.
