# Review — BUG-0004

This review ran in two rounds. **Round 1** examined the change, found the code sound and two
documents wrong, and suspended the item to the architect as Q-001 and Q-002 rather than closing
over them. **Round 2** resumed after both were answered, re-audited the corrected documents against
the code, trial-merged, and closed the item. Each section below carries round 1's text unchanged —
it is what the reviewer believed at the time — followed by a `### Round 2` subsection. Where the
two disagree, round 2 says so explicitly and says why.

## What I examined

The change on `wi/BUG-0004` at `5b5b92c9` (code unchanged since `ab644840`, which is what `verify`
verified), against `main` at `73bb1f4`.

- **The diff, hunk by hunk** — `git diff main..wi/BUG-0004`, four files outside `tracker/` and four
  hunks. `tidy/planner.py`: the `try`/`except OSError` around the loop body and the
  `_unexaminable_reason` helper → plan step 1, serving AC1, AC2 and AC3. `tests/test_cli.py`: the
  `UnexaminableEntryTests` class and one docstring line → step 2, serving AC4 and asserting AC1-AC3.
  `tests/test_planner.py`: the second `UnexaminableEntryTests`, `import errno`, one docstring line →
  step 3, serving AC4. `README.md`: the example `leave` line with its sentence, and the exit-status
  paragraph's `0` clause → step 4, serving AC3. No hunk serves neither a criterion nor a plan step.
- **The record** — `item.md`, `history.md` (5 rows, chaining `— → ready → planned → in-progress →
  verifying → in-review`, last row matching the item's status), `journal.md` in full (5 entries, one
  per execution the history implies), `plan.md`, `impl-report.md`, `verify-report.md`, and the
  item's `questions/` directory, which was empty when this review opened.
- **The ADRs the change touches or relies on** — ADR-0009 in full, ADR-0006 in full, and the
  relevant sections of ADR-0002 (every destination decided in `planner.py`) and ADR-0007 (the exit
  status turns on a `"failed"` outcome).
- **`docs/architecture/overview.md` v7** — the two-error-boundaries paragraph, the module table, and
  the "every destination is decided in `planner.py`" commitment.
- **The declared gaps** — `verify-report.md` `## Not verified, and why` (four items) and
  `impl-report.md` `## What I did not do` (five items).

**Claims audited for D12, each by opening what it cites** — not by reading the sentence, and not by
trusting a neighbouring document that repeats it:

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| "A failure to list *the target folder* belongs to `cli.py` — one line on stderr, an empty stdout, exit 2" | `overview.md` v7 | `tidy/cli.py:60-70`, and the three target-level failures run during verification (missing folder, a file, mode 000) — all exit 2 | **true** |
| "A failure to interrogate *one entry inside it* belongs to `planner.py`, which turns it into the `leave` action that entry gets and carries on" | `overview.md` v7 | `tidy/planner.py:47-64`, and the item's fixture run in both modes | **true** |
| "Before BUG-0004 there was only the first boundary, so one dangling symlink was reported as a folder that could not be read, and no file in that folder was tidied" | `overview.md` v7 | the reverted-planner run made during this item's verification, which reproduces exactly that | **true** |
| "**Every destination is decided in `planner.py` and nowhere else**" | `overview.md` line 34 | `tidy/planner.py` `build_plan`, `_blocking_component`, `_free_destination`; `tidy/apply.py` | **true** — the guard appends a `leave`, it does not decide a destination anywhere else |
| "`build_plan(folder) -> list[Action]` (reads; writes nothing)" | `overview.md` module table | `tidy/planner.py` in full — no write call anywhere in it | **true** |
| "The guard covers `entry.is_dir()` and `entry.stat()`, and nothing else" | ADR-0009 detail 1 | `tidy/planner.py:47-64` — the `try` opens at 47 and closes before `destination_folder` at 65 | **true**, but its citations no longer point at the calls — Finding 2 |
| "The collision helpers use `os.path.lexists` and `os.path.isdir`, which return rather than raise" | ADR-0009 detail 1 | `tidy/planner.py:94` and `:133` | **true**, citations stale — Finding 2 |
| "`os.scandir(folder)` stays outside the guard" | ADR-0009 detail 2 | `tidy/planner.py:41-42`, outside the `for` loop entirely | **true** |
| "only a `"failed"` outcome from `apply_plan` makes the process exit non-zero [src: tidy/cli.py:93]" | ADR-0009, ADR-0007 | `tidy/cli.py:93` — `return 1 if any(outcome.kind == "failed" ...) else 0` | **true**, citation still exact (`cli.py` is untouched by this item) |
| "a genuine defect inside `build_plan` that surfaced as an `OSError` would now be reported as an unusable target rather than crashing loudly" | ADR-0006 `## Consequences` | `tidy/planner.py:47-64` and `tidy/cli.py:66-69` | **no longer true for the guarded region** — Finding 1 |
| "`tidy/cli.py:52`" for what `parse_args` reports | ADR-0008 | `tidy/cli.py:52` | **true** — unaffected, this item does not touch `cli.py` |


### Round 2 — resumed 2026-08-27, after Q-001 and Q-002 were answered

The change on `wi/BUG-0004` at `d8582121`, against `main` still at `73bb1f4`. Round 1's prediction
that answering the questions would move `main` was wrong and `answer-questions` corrected it in its
journal: this project puts a document correction on the item's own branch (the precedent is
ADR-0007 v2 at `d0a7ebd`, made on `wi/BUG-0002`), so both remedies are commits on this branch and
the trunk has not moved since round 1. That is why the trial merge is possible now.

- **The diff again, in full, hunk by hunk** — `git diff main..wi/BUG-0004`, now fifteen files, four
  of them outside `tracker/`. The four code and README hunks are byte-identical to round 1's and
  map to the same plan steps and criteria; the two new non-tracker files are the ADR corrections
  below. Re-read rather than assumed, because the branch moved twice since round 1 opened.
- **`docs/architecture/adr/ADR-0006` v2** — the rewritten `## Consequences` cost paragraph, the
  frontmatter, and change-log row 2. This is Finding 1's remedy.
- **`docs/architecture/adr/ADR-0009` v2** — every changed citation, the new `## Consequences`
  bullet, the frontmatter, and change-log row 2. This is Finding 2's remedy.
- **Both question files** — `Q-001.md` and `Q-002.md`, `status: answered`, `answered-by:
  answer-questions`, each with a `## Consequences` section, and each named file opened to confirm
  the change is in it rather than only described.
- **`answer-questions`' journal entry** at 21:09:01Z, in full, and the resuming history row.
- **The behaviour, run rather than read** — the item's own fixture in both modes on the branch head
  (below), because a review that resumes after two document edits should still confirm the code it
  is about to merge does what the documents now say.
- **The merge result** — a detached trial worktree at `54251e84`, with the test suite and the lint
  run inside it, and `main` compared before and after.

**Claims re-audited for D12, each by opening what it cites.** Round 1's nine passing rows are not
re-listed; what follows is every row round 1 failed or flagged, plus the claims the two ADR
corrections newly assert, plus one row round 1 got wrong.

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| "An `OSError` from `os.scandir` — or from anywhere outside the per-entry guard — still arrives here and is reported as an unusable target, exit 2" | ADR-0006 v2 `## Consequences` | `tidy/cli.py` lines 61-69 (`try: actions = build_plan(folder)` / `except OSError` / `return 2`), and `tidy/planner.py` — `os.scandir` is at the top of `build_plan`, outside the `for` loop and outside the `try` | **true** |
| "One raised while interrogating a single entry no longer reaches this handler at all: it becomes that entry's `leave` line and the run continues, exit unchanged" | ADR-0006 v2 `## Consequences` | `tidy/planner.py` `build_plan`'s `except OSError` → `Action(kind="leave", …)` then `continue`; `tidy/cli.py`'s `return 1 if any(outcome.kind == "failed" …) else 0`; and the fixture run, exit 0 in both modes | **true** |
| "a defect in the guarded region surfaces more quietly than an unusable target, not less" | ADR-0006 v2 `## Consequences` | the same two files, plus the fixture output — the `leave` line goes to stdout among the others and the status is 0 | **true**, and it is the inversion of what v1 said, which is Finding 1 closed |
| Finding 2's six `tidy/planner.py:NN` citations | ADR-0009 v2 | `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` → three hits remain in the whole of `docs/`, none of them in `planner.py` | **resolved** — the six are gone, replaced by file-level citations |
| "The guard covers `entry.is_dir()` and `entry.stat()`, and nothing else" | ADR-0009 v2 detail 1 | `tidy/planner.py` `build_plan` — the `try` opens after the dotfile `continue` and closes at `band = band_for(...)`; `destination_folder` and everything after it are outside | **true**, and now citing the file, with both calls named in the prose |
| "The collision helpers use `os.path.lexists` and `os.path.isdir`, which return rather than raise" | ADR-0009 v2 detail 1 | `_blocking_component` and `_free_destination` in `tidy/planner.py` — both use `os.path.lexists`/`os.path.isdir` only | **true** |
| "The citations in this record name files and symbols, not line numbers … every one of them was exact against `main`" | ADR-0009 v2 `## Consequences` | `git show main:tidy/planner.py` at the four line numbers v1 cited — `if entry.is_dir():`, `band = band_for(now - entry.stat()…)`, `if os.path.lexists(path) and not os.path.isdir(path):`, `return destination in reserved or os.path.lexists(…)` | **true** |
| "only a `\"failed\"` outcome from `apply_plan` makes the process exit non-zero [src: tidy/cli.py:93]" | ADR-0009 v2, ADR-0007 | `tidy/cli.py:93` — `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0` | **true**, citation still exact |
| "`build_parser` runs before `parse_args` has told anyone where the user's rules came from [src: tidy/cli.py:52]" | ADR-0008 line 48 | `grep -n "" tidy/cli.py | sed -n '52,54p'` → line 52 is **blank**; the statement is at line 54 | **claim true, citation points at nothing** — Finding 3, filed as BUG-0006 |

**One correction to round 1's own audit.** Round 1's last row marked the ADR-0008 citation "**true**
— unaffected, this item does not touch `cli.py`". The second half is right and the verdict is not:
"unaffected by this change" is not the same question as "supports its sentence", and answering the
first satisfies D12 only when the second has also been asked. Opening it settles it, which is what
Finding 3 records. `answer-questions` made the same call the same way — its journal says
"`ADR-0008`'s `[src: tidy/cli.py:52]` is still exact" — and both checks were run as
`sed -n '52p' tidy/cli.py`, which prints a blank line and reads as agreement when the expected
content is not held up beside it.
## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox ticked | **pass** | AC1-AC4 all `[x]` in `item.md`; `validate-workspace .` exit 0, 0 errors 0 warnings |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` has one row per AC, each naming the command run and quoting its actual output; no row cites `impl-report.md` |
| D3 | Declared quality gates passed on the **final** state of the code | **pass** | Re-run in this execution on `5b5b92c9`: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests ... OK`; `lint-claims --changed-since main` → exit 0. Code identical to the verified `ab644840` |
| D4 | No open blocking question remains | **fail** | Q-001 and Q-002, filed by this review, both `blocking: true`, `status: open`. This is why the item is suspended rather than closed |
| D5 | `journal.md` has an entry per execution; `history.md` chains to the current status | **pass** | 5 history rows, 5 journal entries, one per row; `— → ready` (verify), `ready → planned` (plan), `planned → in-progress` and `in-progress → verifying` (implement), `verifying → in-review` (verify). Last row matches `status: in-review` |
| D6 | Every design-changing decision is in an ADR, cited from the plan or journal | **pass** | ADR-0009 is the one decision; cited from `plan.md` `## Decisions and ADRs`, from `plan`'s and `implement`'s journal entries, and from the code comment at `tidy/planner.py:60` |
| D7 | Documents the change invalidated updated, with a version bump and change-log row | **fail** | `overview.md` v6 → v7 with its row, done by `plan` ✓; `README.md` amended ✓. **ADR-0006's `## Consequences` was not updated and this change makes one of its paragraphs untrue** — Finding 1, escalated as Q-001 because `review-close` may not edit an ADR (`spec/doc-header.md` §5) |
| D8 | Every commit references the item ID | **pass** | `check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 5 commit(s) on main..wi/BUG-0004 name BUG-0004" |
| D9 | Merged into the trunk | **not yet** | Deliberately not merged. Answering Q-001 and Q-002 will move `main` (both remedies edit documents there), so the trial merge and the merge-result test belong to the execution that resumes this review |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0004 wi/BUG-0004` → exit 0: "verified at `ab644840`; `wi/BUG-0004` has moved to `5b5b92c9` but only the record changed (5 file(s) under tracker/ or docs/)" |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | This file; `## What I examined` lists the diff hunks, the record, the ADRs and the eleven claims audited with what was opened for each |
| D12 | Every claim in `docs/` about the behaviour this item touched is still true; absolute claims carry a resolvable citation | **fail** | Eleven claims audited from their citations (table above). Nine hold. One is now false for the region this item guards (Finding 1). One class of citation stays true but no longer points at what it names (Finding 2). The `[auto]` half passes — `lint-claims --changed-since main` exit 0 |


### Round 2 — the full walk, on `d8582121` and on the merge result

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox ticked | **pass** | AC1-AC4 all `[x]` in `item.md`; `validate-workspace .` → exit 0, "checked 9 item(s), 11 document(s), 0 errors, 0 warnings" |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` has one row per AC naming the command and quoting its output. Re-confirmed by running the item's own fixture here: preview and `--apply` both print `leave  broken.pdf   [cannot be examined: No such file or directory]` and `move   photo.jpg -> recent/images/photo.jpg`, exit 0, and `find` shows `photo.jpg` under `recent/images/` with `broken.pdf` still a link in place |
| D3 | Declared quality gates passed on the **final** state of the code | **pass** | On the merge result `54251e84`, not on the branch: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 72 tests in 0.065s`, `OK`; `python3 -m compileall -q tidy tests` → exit 0. `lint-claims --changed-since main` → exit 0, "checked 2 document(s) changed since main" |
| D4 | No open blocking question remains | **pass** | Q-001 and Q-002 both `status: answered`, `answered-by: answer-questions`, `answered-at: 2026-08-27T21:07:06Z`, each with a `## Consequences` section whose named files were opened and contain the change. No third question was filed |
| D5 | `journal.md` has an entry per execution; `history.md` chains to the current status | **pass** | 7 history rows, 7 journal entries, one per row: `— → ready` (verify), `ready → planned` (plan), `planned → in-progress` and `in-progress → verifying` (implement), `verifying → in-review` (verify), `in-review → awaiting-answer` (review-close), `awaiting-answer → in-review` (answer-questions). Last row matches `status: in-review`; no gap |
| D6 | Every design-changing decision is in an ADR, cited from the plan or journal | **pass** | ADR-0009 is the one design decision, cited from `plan.md` `## Decisions and ADRs`, from three journal entries, and from the code comment in `build_plan`. The two document corrections are not design decisions — `answer-questions` recorded why in its entry, and neither changes what the system does |
| D7 | Documents the change invalidated updated, with a version bump and change-log row | **pass** | `overview.md` v6 → v7 with its row (`plan`) ✓; `README.md` amended (`implement`) ✓; **ADR-0006 v1 → v2** with `updated-by: answer-questions`, `updated-for: BUG-0004` and change-log row 2 ✓ — Finding 1 closed; **ADR-0009 v1 → v2** likewise ✓ — Finding 2 closed |
| D8 | Every commit references the item ID | **pass** | `check-commit-refs BUG-0004 wi/BUG-0004` → exit 0, "all 7 commit(s) on main..wi/BUG-0004 name BUG-0004" |
| D9 | Merged into the trunk | **pass** | Trial-merged first into a detached worktree at `54251e84` with the suite green; `main` confirmed unmoved at `73bb1f4` afterwards; item closed while the branch was still unmerged, then merged for real as `cea3b907`, moving `main` from `73bb1f45`. The suite is green on the merged trunk |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0004 wi/BUG-0004` → exit 0: "verified at `ab644840`; `wi/BUG-0004` has moved to `d8582121` but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code". Run, not assumed: the branch moved twice since verification |
| D11 | `artifacts/review.md` exists and says what was examined | **pass** | This file, both rounds. `## What I examined` names the diff hunks, the record, the ADRs, the trial merge, and every claim audited with what was opened for it |
| D12 | Every claim in `docs/` about the behaviour this item touched is still true; absolute claims carry a resolvable citation | **pass, with a finding filed elsewhere** | Round 1's two failures are closed against the corrected documents, each verified by opening the code rather than by reading the correction. Finding 3 — ADR-0008's `[src: tidy/cli.py:52]`, a blank line — is a claim about `tidy/cli.py`, which this item does not touch and no criterion of it covers; it is BUG-0006 at `ready`, not a bar to this close. The `[auto]` half passes: `lint-claims --changed-since main` exit 0 |
## Findings

**Finding 1 — ADR-0006's `## Consequences` describes a behaviour the merged code no longer has.**
The paragraph reads "a genuine defect inside `build_plan` that surfaced as an `OSError` would now
be reported as an unusable target rather than crashing loudly". After this change, an `OSError`
raised between `try:` and the `band = band_for(...)` line becomes that entry's `leave` line and the
run exits 0; it never reaches `cli.py`. The sentence holds only for an `OSError` from `os.scandir`
or from outside the guard. ADR-0006's **decision** is untouched — all three of its cases still exit
2, run during verification — and ADR-0009 and `overview.md` v7 describe the new boundary correctly;
what is stale is one consequence paragraph, and it is the paragraph a future `plan` would read to
judge whether the guard may be widened. Escalated as **Q-001**, because `spec/doc-header.md` §5
makes an ADR "superseded only" for every skill but `plan` and `answer-questions`. The precedent is
BUG-0002/Q-002, which corrected a factual clause inside a current ADR with a version bump.

**Finding 2 — ADR-0009's six line-number citations into `tidy/planner.py` point at the wrong lines
once this merges.** `:47` (cited twice for `entry.is_dir()`) is now `try:`; `:55` (twice, for
`entry.stat()`) is now `continue`; `:85` is a docstring line where `os.path.lexists` was; `:114`
lands in `_free_destination`, nineteen lines from the call it names. Every one was exact against
`main` — the guard inserts nine lines above them. The claims stay true and `lint-claims` passes,
because §4a's table makes a path citation resolve when the *file* exists; what breaks is the D12
§9a procedure itself, which says to open what a sentence cites and decide from what is there.
Escalated as **Q-002**, with the general question attached: an ADR whose subject is a change to a
file cites that file, and the change is what invalidates its own line numbers, so this recurs for
every item of this shape.

**No finding against the code.** The diff is exactly the four hunks the plan specifies. The two
choices `plan` delegated were both checked against the properties it fixed rather than taken on
trust: the single `try` keeps `os.scandir` outside and contains only `entry.is_dir()` and
`entry.stat()` as `OSError` sources, and `except OSError` rather than `except FileNotFoundError` is
load-bearing for the symlink-loop member of the class. The verification is thorough — six boundary
conditions triggered rather than read about, and the revert experiment re-run rather than quoted
from `impl-report.md`.


### Round 2

**Finding 1 — closed.** ADR-0006 v2's `## Consequences` now states the cost as the two halves it
became: an `OSError` from outside the per-entry guard still reaches `cli.py` and exits 2, one from
inside becomes a `leave` line and the run exits 0, and — the sentence round 1 wanted and v1 had
inverted — "a defect in the guarded region surfaces more quietly than an unusable target, not
less". Checked against `tidy/cli.py` and `tidy/planner.py` rather than against the correction's own
prose, and against a run of the fixture. The frontmatter is `version: 2` with change-log row 2, per
`spec/doc-header.md` §3. ADR-0006's decision is untouched, which is what made the in-place
correction legitimate rather than a supersession.

**Finding 2 — closed.** ADR-0009 v2's six `tidy/planner.py:NN` citations are file-level, the
duplicated pair is collapsed, and the named symbols (`entry.is_dir()`, `entry.stat()`,
`os.path.lexists`, `os.path.isdir`) carry the precision in the prose. `grep -rn "src:
[a-z/]*\.py:[0-9]" docs/` finds three `path:line` citations left in the whole of `docs/`, none of
them into `planner.py`. The general question round 1 attached is answered in the ADR's own
`## Consequences` rather than in a standing convention, and `answer-questions` recorded why:
`spec/doc-header.md` §5 makes `process/ways-of-working.md` a document `plan` creates, so minting it
was outside what that skill may write. That is a defensible line and the reasoning is where the
next `plan` will find it.

**Finding 3 — ADR-0008 line 48 cites `tidy/cli.py:52`, which is a blank line. Filed as BUG-0006 at
`ready`; not a bar to this close.** The claim is true — `build_parser` does run before `parse_args`
— but the statement it names moved to line 54 when BUG-0003's own `46e5fd0` edited `cli.py`, two
commits after `b76b27c` wrote the ADR. Established by running `git show` at both commits, not
inferred. It belongs to BUG-0003, not to this item: `tidy/cli.py` is not in this item's diff, no
criterion of BUG-0004 covers it, and sending BUG-0004 back would put the fix with `implement`,
which may not write to `docs/`. `spec/ids-and-statuses.md` §5 gives this skill the authority to
file the item it observed the need for, so that is what happened. It is the last surviving
citation of the exact class Q-002 was about, which is why it is worth an item rather than a note.

**Still no finding against the code.** The four code and README hunks are unchanged since round 1
and were re-read here, not carried over: the guard contains only `entry.is_dir()` and
`entry.stat()`, `os.scandir` stays outside it, `except OSError` rather than `except
FileNotFoundError` is what covers the symlink-loop member of the class, and `_unexaminable_reason`
reports `error.strerror` without guessing at a cause. The suite is green on the merge result, which
is the state the project actually gets.
## Accepted gaps

Recorded here **and** copied into `item.md` `## Notes`, so they survive the item being closed:

1. **No test covers an entry failing with `EACCES`, `EIO` or `ENOTDIR`.** Declared in both reports.
   The guard is one `except OSError` and two members of the class are exercised (`ENOENT`, `ELOOP`);
   a per-entry permission failure needs an unreadable parent, which is ADR-0006's target-level case,
   and could not be constructed without root. Accepted: the untested members differ only in the
   words `error.strerror` supplies.
2. **A file deleted between `os.scandir` and `entry.stat()` is not tested.** It needs a race this
   suite cannot schedule. Its output is identical to the dangling-symlink case, since the reason
   string names no cause — which is why `_unexaminable_reason` was written not to guess at one.
3. **The tests' skip path was read but never executed**, because symlinks work in this environment.
   What is verified is that it is gated on `os.symlink` raising rather than on a platform name.
4. **`README.md`'s exit-status paragraph was re-wrapped.** No word of the `1` clause changed but its
   line breaks moved, and that clause is BUG-0005's subject. Whoever implements BUG-0005 must
   re-read the paragraph rather than apply a remembered diff. Already in `impl-report.md`
   `## Deviations`; repeated in `item.md` `## Notes` so it is visible from BUG-0005's neighbourhood.
5. **The mode banner is suppressed when nothing moves**, so a folder whose every entry is
   unexaminable prints `leave` lines and `Nothing to do:` with no banner. Pre-existing behaviour
   decided at WI-0001/Q-001 and commented at `tidy/cli.py:72`; it reproduces on a folder with no
   symlinks at all. Not a defect of this item and not filed as one.


### Round 2

The five gaps above stand as accepted and are already in `item.md` `## Notes`; nothing in the two
document corrections touches any of them. Two more are recorded here, and both are added to
`## Notes` for the same reason as the first five — a gap that lives only in a review stops being
read the moment the item closes.

6. **The remedy for Finding 2 forfeits nothing a gate measures, and nothing a gate would have
   caught either.** `spec/doc-header.md` §4a makes `path` and `path:line` one citation form with
   one test — that the file exists — so dropping the line numbers costs no accuracy `lint-claims`
   can see. The flip side is that it costs no accuracy `lint-claims` can see in the *other*
   direction: the three `path:line` citations still in `docs/` are unguarded, and Finding 3 is
   what that looks like. Accepted here and carried by BUG-0006.
7. **`answer-questions` corrected round 1's `## Verdict` in its journal rather than in this file,
   and this file was left as written.** Round 1 predicted that answering the questions would move
   `main`; it did not, because the corrections landed on this branch. That is the right handling —
   a review records what the reviewer believed at the time — but it means `## Verdict` above
   contains a prediction that did not hold, and a reader who stops at the end of round 1 will
   carry it away. This section, and the round-2 verdict below, are where it is put right.
## Verdict

**Suspended, not decided.** The change itself would be accepted: the code is right, every criterion
is ticked with evidence a reviewer can re-run, the diff has no unrequested scope, and D1, D2, D3,
D5, D6, D8, D10 and D11 all pass. What fails is the record in `docs/` — D7 and D12 — and neither
failure is repairable by this skill or by sending the item back, because `implement` may not write
to `docs/` and an ADR is "superseded only" outside `plan` and `answer-questions`
(`spec/doc-header.md` §5).

So the item goes to `awaiting-answer` with `resume-to: in-review`, carrying Q-001 and Q-002. It is
**not** merged: both remedies edit documents on `main`, so the trunk will move before this review
resumes, and a trial merge run now would be a trial of something else. When the questions are
answered, this review continues at step 8 — trial-merge into a detached worktree, confirm `main`
did not move, close, then merge.


### Round 2 — accepted, merged, closed

**Accepted.** All twelve Definition of Done criteria pass on the final state of the code, walked
one by one in the round-2 table above. Round 1's two failures are closed against corrected
documents that were checked by opening the code they describe, not by reading the corrections. The
change is merged into `main` as `cea3b907` and BUG-0004 is `done`, `outcome: delivered`.

What the user gets: a folder containing a dangling symlink is tidied. The entry that cannot be
examined gets a `leave` line carrying the operating system's own words, every other file is moved
as it would have been, and the run exits 0 — where before this item the same folder produced either
a `FileNotFoundError` traceback or, after BUG-0001, the calm false sentence "cannot be read" and an
empty stdout.

Round 1's prediction that the trunk would move before this review resumed did not hold: this
project puts a document correction on the item's own branch, so `main` stood at `73bb1f4` for both
rounds and the trial merge ran against the same base round 1 would have used. The trial was
detached (`git worktree add --detach`), the suite and the lint were run inside it, `main` was
confirmed unmoved at `73bb1f4` after it was discarded, and the item was closed before the real
merge — because `check-commit-refs` inspects the commits not yet on the trunk, and merging first
would empty that range and refuse the close it is a precondition for.

**One thing leaves this review unfinished, deliberately and elsewhere.** BUG-0006 records that
ADR-0008 cites a blank line. It is a defect in another item's document, it does not touch anything
BUG-0004 delivered, and it sits at `ready` for `plan` to decide the remedy — repoint, or apply
ADR-0009 v2's own rule and cite the file. This review does not decide that, because an ADR is
"superseded only" for this skill.

**The engagement is not over.** `scripts/engagement-state EP-001` was run after this close, not
inferred from the board, and it reports the epic still `active`: BUG-0005, WI-0003 and now BUG-0006
have not stopped. No sign-off question is filed, and none is due yet.
