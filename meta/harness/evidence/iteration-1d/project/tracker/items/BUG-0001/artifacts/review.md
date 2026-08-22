# Review — BUG-0001

## What I examined

- **The item**: `item.md` — both criteria and their tick state, the six reproduction steps, and the
  `## Notes` reasoning for why this was filed as a bug rather than sent back to WI-0001.
- **The record**: `history.md` (five rows, chaining `— → ready → planned → in-progress →
  verifying → in-review`, the last matching `item.md`), and `journal.md` in full — seven entries,
  one per transition plus two self-declared corrections. No question was ever filed on this item.
- **The upstream artifacts**: `plan.md`'s seven steps and its AC mapping, `impl-report.md`'s three
  declared deviations, and `verify-report.md`'s criteria table, gate table, five boundary cases,
  sensitivity check and four declared gaps.
- **The diff**, `main..wi/BUG-0001`, hunk by hunk — three files, 82 insertions and 28 deletions.
  Not the reports about it; the mapping in `## Findings` was made by reading the hunks against the
  plan's numbered steps.
- **`docs/architecture/adr/`** — all eleven. `ADR-0011` in full, as the decision this change
  executes; `ADR-0007` and `ADR-0010` checked because they govern WI-0003's import command, which
  `ADR-0011` argues will inherit this contract. Neither mentions output or ordering, so neither is
  contradicted.

**The D12 claim audit, from the citations rather than from the prose.** Three absolute claims in
`docs/` describe behaviour this item touched. Each was checked by opening the thing it cites:

| claim | cited | what I opened | result |
|-------|-------|---------------|--------|
| `overview.md`: "`cli.py` … is the only module that writes to stdout or stderr" | `expenses/cli.py`; `expenses/__main__.py` | `grep -n "print(\|sys.stdout\|sys.stderr" expenses/*.py` excluding `cli.py` → no matches | **holds** |
| `ADR-0011`: "the handler is reached only through `args.set_defaults(handler=...)` and the single call in `main`; no test and no other module reads a handler's return value" | `expenses/cli.py` | `grep -rn "handler" expenses/ tests/` → seven `set_defaults(handler=…)` lines, one `line = args.handler(args, ledger)` at `cli.py:129`, one docstring mention; nothing under `tests/` | **holds** — and it holds *after* the change, which is what makes it worth re-checking rather than re-quoting |
| `overview.md`: "`main` … prints the line only after `store.save` has returned" | `ADR-0011` | `expenses/cli.py`'s `main`: `print(line)` is inside `if line is not None:` and below the `try/except StoreError` block, which `return EXIT_STORE`s | **holds** |

One claim did **not** hold, and is the finding below.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox is ticked | **pass** | `item.md` lines 64 and 67: `- [x] AC1`, `- [x] AC2`. Ticked by `verify`, not by `implement` — `impl-report.md`'s deviation 1 declares that it deliberately left them for the verifier, which is what `spec/work-item.md` requires |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | AC1 cites the six reproduction steps run in verification, with `exit=1`, `stdout=<<>>` and the `Permission denied` stderr line quoted per command, plus a byte-exact re-run giving `stdout_bytes=0`. AC2 cites reading the test body, running it (`Ran 1 test … ok`), and sabotaging `main` (`FAILED (failures=3)`). Neither row cites `impl-report.md` |
| D3 | All declared quality gates passed on the **final** state of the code | **pass** | The last commit touching code is `ad961d7`; the last touching `docs/` is this execution's. `implement`'s seven gates ran at branch head `d727aba`, after the last code change. `verify`'s six ran at `758c0af`. `check-verify-freshness` confirms the two commits since verification changed only files under `tracker/` and `docs/`. Re-run here on the merge result: `Ran 116 tests … OK`, exit 0, and `compileall` exit 0 |
| D4 | No open blocking question remains | **pass** | `tracker/items/BUG-0001/questions/` is empty — no question was filed at any stage of this item |
| D5 | A journal entry for every skill execution; `history.md` chains without a gap | **pass** | Five history rows and seven journal entries: one per transition (02:28:45 `verify` filing it, 03:44:14 `plan`, 03:48:14 and 03:51:18 `implement`, 03:55:59 `verify`) plus two correction entries that declare themselves as such (03:44:54, 03:51:55). The last row's `to` is `in-review`, matching `item.md` before this execution |
| D6 | Every design-changing decision is in an ADR, cited from the plan or journal | **pass** | One design decision: the handler contract. `ADR-0011`, cited from `plan.md`'s `## Decisions and ADRs`, from its `## Problem` and steps, and from the `plan` journal entry at 03:44:14. The three rejected alternatives — `(changed, line)`, buffering stdout, saving before the handler — are named in the ADR with their costs, so the shape of the decision is recoverable and not just its outcome |
| D7 | Documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` v7 (by `implement`, step 6 of the plan) added the handler contract and the ordering to the `cli.py` bullet, with a change-log row. v8 (this execution) is the D12 correction below. Both bump the header version and add a row |
| D8 | Every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → `all 5 commit(s) on main..wi/BUG-0001 name BUG-0001`, exit 0 |
| D9 | The change is merged into the trunk | **pass** | Trial-merged into a throwaway branch off `main` first: `git merge --no-ff` succeeded with no conflict, 9 files changed, and `python3 -m unittest discover -s tests -t . -q` on the merge result gave `Ran 116 tests in 3.000s / OK`, exit 0. The trial branch was then deleted and the real merge follows this close, in this execution — `git log main --merges --grep BUG-0001` finds it |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0: "verified at `758c0af9`; `wi/BUG-0001` has moved to `ac5ff050` but only the record changed (5 file(s) under `tracker/` or `docs/`)". Run, not assumed — and `verify-report.md`'s `Verified-commit:` line is the full hash, which is what makes the comparison mechanical |
| D11 | `review.md` exists and states what was examined | **pass** | This document; `## What I examined` is first and names the artifacts, the diff range, the ADRs opened and the three claims audited with what each was checked against |
| D12 | Every claim in `docs/` about the behaviour this item touched is still true; absolute claims this execution wrote carry a resolvable citation | **pass, after a correction** | The audit table above: three claims checked against the code they cite, all three hold. A fourth did not and was fixed — see `## Findings`. `lint-claims --changed-since main` → `0 errors, 0 warnings`, exit 0 |

## Findings

1. **`docs/architecture/overview.md`'s opening paragraph had gone stale, and was corrected (v8).**
   It read "this version is step 5 of WI-0002's plan re-checking that description against what was
   actually built". That was true at v6; v7 was written by `implement` for BUG-0001, so the lede
   attributed the current version to the wrong item and the wrong plan step. `verify` found this
   and routed it here rather than filing a bug or sending the item back, which is the correct
   call: no acceptance criterion of this item covers the overview, and it is not behaviour
   delivered by another item — it is a stale claim in a document this item touched, which is D12.
   Fixed in this execution: the lede now describes the document and points at the change log for
   which item wrote which version, rather than naming "this version" — the form that goes stale
   every time anyone edits the file. Header bumped to v8 with a change-log row.

2. **The diff maps cleanly onto the plan; no unrequested scope.** Hunk by hunk:
   `expenses/cli.py` — the docstring paragraph (step 4), seven signature changes to `str | None`
   and the four `return False` → `return None` (steps 1–2), the three `print`-to-`return`
   conversions (step 1), and `main`'s `changed` → `line` with the moved `print` (step 3).
   `tests/test_persistence.py` — one added class (step 5). `docs/architecture/overview.md` —
   the `cli.py` bullet, header and change log (step 6). Nothing serves neither a criterion nor a
   step.

3. **`impl-report.md`'s three declared deviations are all accepted, and one was right to make.**
   Deviation 1 — refusing plan step 7's instruction to tick the criteria, on the grounds that
   `spec/work-item.md` gives ticking to `verify` — is the correct reading and the correct thing to
   have done: a box ticked by the developer would have told the verifier that something had
   already been independently confirmed, which is the one thing the separation of those two skills
   exists to prevent. It is also declared rather than done quietly, which is what makes it
   reviewable. Deviations 2 (a stricter `people` assertion than the plan's wording) and 3 (a
   docstring paragraph rather than a sentence) are inside the plan's latitude.

4. **Maintainability, read as someone who will have to live with this.** `main` now branches on
   `if line is not None:` rather than on a boolean. A handler returning `""` would therefore save
   and print a blank line — no handler does, and `ADR-0011` names the neighbouring case ("a
   handler that changes the ledger but has nothing to say cannot be expressed") along with what to
   do if one ever appears, which is option B. Recorded as an observation, not a defect: the
   condition is unreachable from any command that exists, and the ADR already says where the
   design would move. The four listings carrying `-> str | None` while only ever returning `None`
   is deliberate uniformity (plan step 2), and both the module docstring and `ADR-0011` say why,
   in the two places someone adding a command would look.

5. **One thing noticed and deliberately not filed as a bug.**
   `tests/test_persistence.PersistenceTestCase.setUp` calls `tempfile.mkdtemp()` with no cleanup,
   so every test in the file leaves a directory behind. That predates this item — it is WI-0001's
   code and every existing test in the file does it — and the new test inherits it rather than
   introducing it. It is test hygiene, not delivered behaviour, so it fails the "defect in
   behaviour delivered by another item" test that would make it a bug item. Recorded here so the
   judgement is visible rather than silent.

## Accepted gaps

Each of these was declared upstream, is accepted rather than sent back, and has been written into
`item.md`'s `## Notes` — because once this item is `done` nobody reads its verification report
again, and a gap that lives only in a report stops being true without anyone noticing.

- **Neither criterion is verified under `root`**, since the regression test skips itself there and
  verification ran as uid 1000. Accepted: the skip guard is the honest option, because without it
  the test would pass vacuously as root.
- **`ADR-0011`'s central argument — that WI-0003's importer inherits the ordering — is
  unverified**, because no import command exists. It cannot be checked until WI-0003 is built, and
  the note asks its implementer to confirm rather than assume.
- **`CliTestCase.assertRefused` still does not assert empty stdout.** The plan put it out of scope
  and review agrees; carried into `## Notes` so it stays findable once the plan belongs to a
  closed item.
- **A ledger at mode 400 in a writable directory is still overwritten**, because atomic replace
  renames over the target. Correct, contradicts no criterion, and surprising enough to write down.

Verification also declared that exotic filesystems and the `--help` / `EXPENSES_LEDGER` / XDG
paths were not re-exercised. Those need no note: the first is outside what this project targets
[src: ADR-0005], and the second is WI-0001's criteria over code this diff does not reach.

## Verdict

**Accepted, merged, and closed as `delivered`.** The defect is fixed at the level `ADR-0011`
chose — in `main`, once, rather than in each command — so a failed write says nothing on stdout
for all three recording commands and the next mutating command inherits that. All twelve
Definition of Done criteria pass, one after a correction I made under D12. The record is
reconstructible from the tracker, `docs/` and `git log --grep BUG-0001` alone.

The epic is **not** closed by this item. `EP-001` still has `WI-0003` at `blocked`, so DE1 fails
and the stakeholder sign-off question of DE7 is not due yet; `check-epic-signoff BUG-0001` passes
for the unrelated reason that this is a bug rather than an epic.
