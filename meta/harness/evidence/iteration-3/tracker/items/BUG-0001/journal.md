# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-28T22:35:22Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0001
- **Trigger:** filed during `review-close`'s termination review of EP-001; not dispatched on this item, which did not exist until this execution created it
- **Inputs read:**
  - `docs/architecture/overview.md` (v5) — `## Rules that live in exactly one place`, both the "Where a cell's content sits in its field" and the "How wide a column is" bullets
  - `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md` — `## Decision` items 1–5
  - `mdtab/table.py` — `_column_widths`, `_render_cell`, `_render_delimiter`, `_spaces_omitted`
  - `tracker/items/WI-0002/item.md` AC6; `tracker/items/WI-0001/item.md` AC6 and AC12, and the `### AC12 amended, round 3` section recording `WI-0001/Q-005`
  - `.claude/agile-skills/spec/dor-dod.md` §2 (bug Definition of Ready, RB1–RB5) and §4 (DE6)
- **Decisions:**
  - **Filed as a `bug`, not recorded as an accepted gap.** An accepted gap is a thing nobody did; this is a thing two documents say that is false, and DE6 makes a claim that cannot be verified from its citation a finding rather than a pass. Recording it in EP-001's `## Notes` would have closed the epic over a document that misinforms the next person to touch `_column_widths` — which is the one function `WI-0001/Q-005` exists to protect.
  - **`found-in: WI-0002`, not WI-0001.** The false sentence was written for WI-0002 (ADR-0007 decision 4, repeated into the overview at v3). The behaviour it is false about was delivered by WI-0001. `found-in` names where the defect was introduced; `## Notes` names where a fixer will have to read.
  - **Scoped to the documents, with `mdtab/` explicitly out of scope (AC6).** The code is correct and the floor it applies is forced by idempotence. The tempting fix — delete `needed` so the sentence becomes true — would break `WI-0001 AC6` for a degenerate column, so the item says in two places that it must not be taken.
  - **Priority `medium`.** It misinforms a future change to a load-bearing function, which is more than cosmetic; it changes no behaviour and nothing is blocked on it, which is less than high.
  - **Definition of Ready for a bug, applied at filing (`spec/dor-dod.md` §2):** RB1 — `## Steps to reproduce` is two `printf | python3 -m mdtab` commands and a comparison, runnable from a checkout with no further questions. RB2 — `## Actual behaviour` quotes both outputs verbatim through `cat -A` with their exit codes, and the five lines of `_column_widths` that produce them. RB3 — `## Expected behaviour` quotes both contradicted documents in full, by section and bullet. RB4 — `found-in: WI-0002` is set. RB5 — the regression test is AC4 and it is possible, because the defect is observable from the command line.
- **Questions raised:** none
- **Commands:**
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, middle column 2 columns wide
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, middle column 3 columns wide, from identical content
  - `python3 .claude/agile-skills/scripts/new-item --id BUG-0001 --type bug --status ready --actor review-close --found-in WI-0002 …` → exit 0
- **Gates:** the gates of this execution are recorded on `EP-001`'s journal entry, where the execution ran. Filing an item is not a transition of it, and this entry exists because `journal.execution.missing` requires the creation row in `history.md` to have one.
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` — summary, reproduction, expected and actual behaviour, AC1–AC6, out-of-scope and notes
  - `tracker/items/BUG-0001/history.md` — the creation row, actor `review-close`
- **Status:** `—` → `ready`
- **Result:** A false absolute in two documents, found by reading them against `mdtab/table.py` rather than against each other, is filed with a command that falsifies it. EP-001 leaves rest and does not close on this run.

## 2026-08-28T22:42:34Z — plan v0.3.1 — architect

- **Item:** BUG-0001
- **Trigger:** status `ready`, dispatched by `next` step 5 — the only runnable candidate, its status's owner being `plan`
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` (the six criteria are the contract) and `history.md`
  - no `artifacts/refinement-qa.md`: a bug enters at `ready` and is never refined, so there is no `[assumed]` or `[unresolved]` ground to read. Its equivalent is the filing journal entry, which records the Definition of Ready check `review-close` applied at RB1–RB5, and that was read instead.
  - `tracker/items/EP-001/artifacts/review.md` — the termination review that filed this item, in particular the fifteen-claim audit table and Findings 1 and 2
  - `docs/architecture/overview.md` (v5), `## Rules that live in exactly one place`, both the offending bullet and the "How wide a column is" bullet
  - `docs/architecture/adr/ADR-0007` in full; `ADR-0002`, `ADR-0005`, `ADR-0006`, `ADR-0008` consulted for the width rule, the test framework, the `.bin` fixture convention and the recognition rules
  - `tracker/items/WI-0002/item.md` AC6; `tracker/items/WI-0001/item.md` AC6, AC12 and `### AC12 amended, round 3` (`WI-0001/Q-005`)
  - **code:** `mdtab/table.py` `_column_widths`, `_render_delimiter`, `_spaces_omitted`; `tests/test_units.py` — the `pipe_columns` helper and all of `WidthIndependenceTest`; `tests/test_fixtures.py`'s discovery and `UNTOUCHED` set; `tests/fixtures/align-empty-cell.in.md` and `.out.md`
  - `.claude/agile-skills/spec/doc-header.md` §3 and §4; `spec/dor-dod.md` §2 and §3
- **Decisions:**
  - **Reading the code found a third copy of the false sentence, which the bug does not name.** `WidthIndependenceTest`'s docstring in `tests/test_units.py` says *"AC6 — a column's width is the same whatever its marker says"* — the same overstatement of `WI-0002 AC6`, and the new test required by AC4 would sit directly beneath it. Route: decided, and recorded under `## Assumptions` rather than as a new criterion, because `plan` may not amend an item's criteria. It is mapped to AC4 in the mapping table with the reasoning stated there.
  - **The existing test passes and proves less than its name suggests.** `test_the_pipes_land_in_the_same_places_under_all_four_markers` uses cells (`two`, `bb`, `e`) wide enough that `_column_widths`' floor never binds, so it is true and is evidence for the *alignment* half only. Not a defect and not amended; the new test is what covers the other half. This is why the correction narrows the prose instead of deleting the clause.
  - **`tests/fixtures/align-empty-cell` already pins the behaviour as intended.** Its hand-written `.out.md` has a 3-wide middle column under `:---:` from empty cells. Route: documented. It settles that the code is right without anyone having to re-derive it, and it is the standing evidence AC6's no-`mdtab/`-diff constraint rests on.
  - **Correct ADR-0007 in place rather than superseding it — `ADR-0009`.** Route: decided, having found the record silent. `spec/doc-header.md` §4 forbids editing an ADR *to change its decision*, and this changes no decision: option A of ADR-0007 is correct and implemented, and only a clause of item 4's justification is false. Superseding was the alternative and is rejected in the ADR at length — ADR-0007 is cited from the overview and from WI-0002, and marking it `superseded` while its decision stands would send readers looking for a change to the system that never happened. The permission is bounded by four conditions, the third of which requires the removed sentence to be quoted verbatim in the change log. Not escalated: the choice forces no code change and is cheaply reversible in the direction that matters (a document corrected under A can still be superseded later; an ADR superseded under B cannot easily be made current again).
  - **Correct the sentences rather than delete the clause.** Route: documented — DE6 requires claims in `docs/` to be true, not absent, and the overview's list exists to answer where each rule lives. Deleting would restore the silence that let the wrong answer stand across two items. Recorded in `## Approach`, not as an ADR: deletion is the only alternative and AC1's own wording already excludes it by requiring a reader to be able to predict both commands.
  - **The three document corrections are left to `implement`, on the branch.** Route: decided. `plan` commits on the trunk before any branch exists, which is why `lint-claims --changed-since main` passed vacuously on two of `WI-0003`'s executions and again on `EP-001`'s review. Making the corrections here would put them out of that gate's reach for every skill after this one. `ADR-0009` itself is unavoidably committed on the trunk by this execution, and the plan says so and tells `implement` to run `--all`.
  - **`## Scaffolding` is `none`.** The test framework is `unittest` from the standard library (`ADR-0005`), `tests/` already has its `__init__.py`, and both declared commands run today. Nothing needed creating for a command to execute.
  - **Priority, scope and `mdtab/` left alone.** The plan names the temptation to "fix" `_column_widths` explicitly and guards it three ways — AC6, a mechanical check in step 5, and a paragraph in `## Approach` — because the false sentence is itself an argument for doing it, and a change there would break `WI-0001 AC6` for a degenerate column.
- **Questions raised:** none. No decision here is irreversible and none depends on intent no document records: the stakeholder's intent about mdtab's behaviour is settled and this item changes no behaviour.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 71 tests (the baseline the plan's step 1 raises to 72)
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, middle column 2 columns wide
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, middle column 3 columns wide
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 1 on first run (`claim.unsourced` in the new ADR-0009), then exit 0 after the claim was cited
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → run for the contract; see Gates
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 11 documents
- **Gates:**
  - `workspace-valid` → **pass**. `validate-workspace` exit 0 with the plan and ADR-0009 written; re-run by this transition.
  - `every-criterion-is-addressed` → **pass**. The evidence is `plan.md`'s `## Acceptance criteria mapping`: AC1→step 3, AC2→step 4, AC3→steps 3 and 4, AC4→steps 1 and 2, AC5→step 5, AC6→a constraint on all five with a `git diff --name-only main` check. Every row names a specific demonstration — a command to run, a `grep` that must return nothing, a mutation that must make the new test fail — not "tests".
  - `project-commands-resolved` → **pass**. `tracker/project.yaml` already carries `commands.test: python3 -m unittest discover -s tests -t .` and `commands.lint: python3 -W error -m compileall -q mdtab tests`; both were run in this execution and both exit 0 while genuinely checking something (71 tests; `-W error` on compilation). `commands.build` stays null, honestly: there is nothing to build.
  - `decisions-recorded` → **pass**. `plan.md`'s `## Decisions and ADRs` table lists five choices, each with its route and where it lives: one in `ADR-0009` (created here), three cited to existing documents or criteria, and the branch-placement decision under `## Approach` with its reversal cost. The three `## Assumptions` each state what reversing them costs.
  - `plan-is-executable-without-you` (advisory) → **pass**. Read cold, each step names the file, the class, the sentence to remove and what must be true afterwards. The one place a reader must exercise judgement — the exact wording of three corrected sentences — is declared as an assumption rather than left as a silent gap, and the criterion that judges it is stated: a reader of the two overview bullets must be able to predict both commands in `## Steps to reproduce`.
  - `claims-are-sourced` → **pass, with the same weakness the review recorded**. `lint-claims --all` exits 0 over the whole tree; that run caught a real unsourced absolute in `ADR-0009` and it was cited before this entry was written. `--changed-since main`, which is the gate as contracted, has nothing to read on an execution that commits to the trunk — the defect `EP-001/artifacts/review.md` Finding 2 records, and the reason the plan pushes the document edits onto the branch.
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` (new) — problem, approach, five steps, the six-row AC mapping, three assumptions, five decisions, `## Scaffolding: none`, five risks, five exclusions
  - `docs/architecture/adr/ADR-0009-a-false-statement-inside-a-standing-decision-is-corrected-in-place.md` (new, v1) — options A/B/C with costs and risks, the decision with its four conditions, consequences including reversibility in both directions
  - `docs/architecture/overview.md` — **deliberately not touched**. This change alters no shape of the system, and the correction it needs is AC1, which belongs to `implement` on the branch. A version bump here would have been a bump with no substantive change.
- **Status:** `ready` → `planned`
- **Result:** BUG-0001 is planned as a documentation correction with a regression test in front of it and `mdtab/` fenced off. Planning found a third copy of the false sentence, in a test docstring, and `ADR-0009` records how a false statement inside a standing decision is corrected without superseding the decision.

## 2026-08-28T22:45:02Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `planned`, dispatched by `next` — the only runnable item on the board (EP-001 is `open` with owner `null`; WI-0001/0002/0003 are `done`).
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the six acceptance criteria, the two reproduce commands, and the three "out of scope" clauses
  - `tracker/items/BUG-0001/artifacts/plan.md` — five steps, the AC mapping table, and the instruction to make the document corrections on the branch rather than on the trunk
  - `tracker/items/BUG-0001/history.md` — two rows, `review-close` → `ready` and `plan` → `planned`; no send-back, no partial branch
  - `tracker/items/BUG-0001/questions/` — empty; nothing to reconcile
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, `conventions.branch-prefix`, `conventions.commit-subject`
  - `docs/architecture/adr/ADR-0009-*.md` — the four conditions under which ADR-0007 may be corrected in place
  - `docs/architecture/adr/ADR-0007-*.md` — `## Decision` item 4, the sentence to correct
  - `docs/architecture/overview.md` — the "Where a cell's content sits in its field" and "How wide a column is" bullets
  - `tests/test_units.py` — `WidthIndependenceTest`, its docstring and its one existing test; the `pipe_columns` helper
  - `tests/fixtures/align-empty-cell.in.md` and `.out.md` — the standing evidence that the width floor is intended behaviour
- **Decisions:**
  - Started fresh rather than reconciling: `git branch` showed no `wi/BUG-0001`, and the history's last row is `plan`, not a send-back, so there is no partial work to preserve.
  - Reproduced the defect before writing anything, with the item's own two commands, so the correction is written against observed output rather than against the bug report's transcription of it. Both exited 0; the middle column is 2 display columns wide with `---` and 3 with `:-:`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → 0
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → 0, middle column 2 wide
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → 0, middle column 3 wide
- **Gates:**
  - `tests-pass` → **skipped** (not yet run — no change has been made; this entry opens the execution)
  - `lint-clean` → **skipped** (not yet run — no change has been made)
  - `workspace-valid` → **skipped** (not yet run at the branch head; the pre-dispatch run by `next` was clean)
  - `every-criterion-has-a-test` → **skipped** (not yet run — the regression test is step 1 of the plan and is not written)
  - `commits-reference-the-item` → **skipped** (not yet run — the branch has no commits)
  - `no-unplanned-scope` → **skipped** (advisory; not yet run — there is no diff)
  - `claims-are-sourced` → **skipped** (not yet run — no document has been edited)
- **Artifacts:**
  - branch `wi/BUG-0001`, created from `main` at 5db7845, no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation started. The defect reproduces exactly as filed, so the corrected sentences have something observed to describe; the plan's five steps run next, beginning with the regression test.

## 2026-08-28T22:49:57Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress`, continuing this execution — the opening entry above created the branch; this one reports the work.
- **Inputs read:**
  - `tracker/items/BUG-0001/artifacts/plan.md` — the five steps, executed in order
  - `tracker/items/BUG-0001/item.md` — the six criteria, and AC4's wording in particular
  - `docs/architecture/adr/ADR-0009-*.md` — the four conditions for correcting an ADR in place
  - `docs/architecture/adr/ADR-0007-*.md`, `docs/architecture/overview.md` — the two sentences corrected
  - `tests/test_units.py` (`WidthIndependenceTest`, the `pipe_columns` helper, the module docstring), `tests/test_fixtures.py` (`ProcessTest`, for how this project runs the process boundary)
  - `tests/fixtures/align-empty-cell.in.md` and `.out.md` — the standing evidence that the width floor is intended
  - `.claude/agile-skills/spec/doc-header.md` §3 and §4a — change-log form and the citation forms a corrected sentence must use
- **Decisions:**
  - **The regression test runs the two commands rather than calling `lay_out`.** Plan step 1 specified `lay_out` on a four-line piped run; AC4 specifies *"runs both commands from `## Steps to reproduce`"*, and those are `printf … | python3 -m mdtab` on a bare three-line table. A plan cannot waive a criterion and this skill cannot amend one, so the criterion won. The plan's other two concerns were kept: the test sits in `WidthIndependenceTest` beside the existing one, and measures with `pipe_columns` so the measurement is display width (ADR-0002). Recorded as deviation 1 in `impl-report.md`, with its cost — `test_units.py` now holds one process-level test, which its module docstring reserves for `test_fixtures.py`.
  - **Both corrected sentences say the true narrower thing rather than dropping the false clause.** AC1 requires a reader of the overview's two bullets to be able to predict both commands, which a deletion would not give them, and the plan's `## Approach` records that the silence is what let the wrong answer stand for two items.
  - **The mutation was run, not assumed.** `widths.append(max(width, needed + omitted))` was temporarily replaced by `widths.append(width)` in `mdtab/table.py`; the new test failed `2 != 3` and three other tests fell with it; `git checkout -- mdtab/table.py` restored it. AC4 asks for a test that fails without the floor, and the only way to know that is to remove the floor.
  - **The tree-wide sweep for a fourth copy of the sentence was run and found none that is a live claim.** Every remaining hit is a required verbatim quote in a change log, `ADR-0009` ruling on the sentence, or a tracker artifact recording the finding. One hit is a **wrong verification record on a closed item** — `WI-0002/artifacts/review.md` line 64 judged the sentence to hold, having checked the guard-space half and the four-marker layout, neither of which reaches the width floor. Left alone deliberately: correcting a closed item's evidence is forbidden by this item's `## Out of scope` and covered by no criterion here. Named in `impl-report.md` under `## What I did not do` so it is a handover rather than an omission.
  - **Plan steps 1 and 2 were committed together.** The docstring describes the test directly beneath it; splitting them would have produced a commit whose class docstring contradicts its own contents.
  - **No acceptance criterion was ticked.** `spec/work-item.md` gives that to `verify`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/BUG-0001 main` → 0
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 72 tests`, `OK` (at branch head `baa567e`)
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - mutation check: `sed -i '175s/.*/        widths.append(width)/' mdtab/table.py` then the suite → `FAILED (failures=4)`, the new test reporting `AssertionError: 2 != 3`; `git checkout -- mdtab/table.py` → 0; suite back to `Ran 72 tests … OK`
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → 0, middle column 2 wide; same with `---|:-:|---` → 0, middle column 3 wide
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → 0, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0, `checked 2 document(s) changed since main`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → 0, `all 3 commit(s) … name BUG-0001`
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `git diff --name-only main | grep '^mdtab/'` → 1 (no match), which is AC6
  - `sed -n '/^## Decision/,/^## Consequences/p' docs/architecture/adr/ADR-0007-*.md | grep -c "does not depend on its marker"` → `0`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 72 tests, at branch head)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (all six rows of `impl-report.md`'s evidence table name a test function or an exact command with its output; AC4's sensitivity was demonstrated by mutation rather than claimed)
  - `commits-reference-the-item` → **pass** (`check-commit-refs BUG-0001 wi/BUG-0001` exit 0, 3 commits)
  - `no-unplanned-scope` → **pass** (advisory; seven files, each traced to a plan step in `impl-report.md`'s gate table)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 over 2 documents — not vacuous this time, because the plan deliberately left the document edits to the branch — and `--all` exit 0)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — created
  - `tests/test_units.py`, `docs/architecture/overview.md` (v6), `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md` (v2) — updated
  - branch `wi/BUG-0001`, commits `fa9f067..baa567e` (3), from `main` at `5db7845`
- **Status:** `in-progress` → `verifying`
- **Result:** The three false copies of *"a column's width does not depend on its marker"* are gone from the live text of the overview, ADR-0007 and the test docstring, each replaced by the narrower true statement plus a pointer to the minimum-width rule that owns the other half; ADR-0007 keeps `status: accepted` under `ADR-0009`'s four conditions with the removed sentence quoted in its change log. A test now runs both of the item's reproduce commands and fails if the width floor is deleted. Nothing under `mdtab/` changed.

## 2026-08-28T22:54:49Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying`, dispatched by `next` — the only runnable item on the board.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the six criteria, read before the implementation report and used to derive what would settle each one
  - `tracker/items/BUG-0001/artifacts/plan.md` — the five steps and the AC mapping, to find behaviour on the branch that no step accounts for
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — the claims, checked rather than trusted; its deviation 1 and its `## What I did not do` were both re-derived independently
  - `tracker/items/BUG-0001/history.md` — three rows; a first verification, not a re-check after a send-back
  - branch `wi/BUG-0001` at `64012f3f46e6c419d035cdb4165efaecb630e583`, the head verified
  - `tracker/items/WI-0002/item.md` AC6 and `tracker/items/WI-0001/item.md` AC12 with `WI-0001/Q-005` — the criteria the corrected sentences cite, opened to decide whether they *support* the new text and not merely whether they resolve
  - `.claude/agile-skills/spec/doc-header.md` §3 — the three change-log rules AC3 is defined by
  - `docs/architecture/adr/ADR-0009-*.md` — the four conditions AC2 requires ADR-0007's correction to meet
  - `mdtab/table.py` `_column_widths`, and `git show 3647766 -- mdtab/table.py` and `git show 3647766^:mdtab/table.py` — to decide two factual claims in the corrected ADR text rather than accept them
- **Decisions:**
  - **AC1 fails, and it is a send-back rather than a bug.** The clause written to replace the false absolute contains a new false absolute: *"a column too narrow to hold its own marker comes out one column wider for each `:` the marker carries"*. A four-marker sweep over an empty column gives widths 2, 2, 2, 3 for `---`, `--:`, `:--`, `:-:` — one colon adds nothing, only the second widens the column. AC1 requires the replacement to be *"true of the code as it stands"*, so `SKILL.md` step 7's test answers yes: a criterion of this item says the behaviour should be different. Sent back to `in-progress`; no bug item filed.
  - **The finding came from the boundary, not from the happy path.** The item's own two reproduce commands both agree with the new sentence, so checking only those would have passed AC1. The one-colon markers are the case the sentence generalises over and gets wrong, and running them is what isolated it.
  - **AC2 was checked for truth, not only for absence.** Its wording asks that item 4 "no longer assert it", which a deletion would satisfy; the replacement's two factual claims were checked anyway, since a corrected sentence that is itself false is the exact defect this item exists for. Both hold: `git show 3647766^:mdtab/table.py` contains `widths.append(max(width, needed + omitted))`, so the floor does predate WI-0002; and WI-0002's code commit does not alter `_column_widths`' body.
  - **AC2 and AC3's verbatim-quote and version conditions were decided by string comparison, not by eye.** The removed sentences were pulled from `git show main:<path>` and matched against the change-log rows after whitespace normalisation, because "quotes it verbatim" read by a human is exactly the condition that passes when it should not.
  - **AC3 is ticked but declared invalidated by the fix.** Correcting AC1 edits `docs/architecture/overview.md` again and needs a v7 row, so the tick is evidence about `64012f3` only. Recorded in the report's `## Not verified, and why` so the next verification re-checks it rather than inheriting it.
  - **`WI-0002/artifacts/review.md` line 64 — a wrong verification record on a closed item — was not filed as a bug.** `impl-report.md` declares it and the description is accurate: that verification judged the false sentence to hold, having checked the guard-space half and the four-marker layout, neither of which reaches the width floor. It is behaviour of the *record*, not of the tool; no criterion of this item covers it, and this item's `## Out of scope` forbids reopening a closed item. Left named in the report for `review-close` or a later engagement to route, rather than routed by this skill on its own initiative.
  - **The test's placement was not treated as a defect.** `impl-report.md` deviation 1 flags that a process-level test now sits in `test_units.py`, whose module docstring reserves whole documents for `test_fixtures.py` (ADR-0005). AC4 asks for a test in `tests/` that runs both commands, and this is one; no criterion decides placement, so it is flagged rather than failed.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → 0, `64012f3f46e6c419d035cdb4165efaecb630e583`
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 72 tests in 0.138s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → 0, `0 errors, 0 warnings`
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → 0, `a |  | b$` (middle column 2)
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → 0, `a |   | b$` (middle column 3)
  - four-marker sweep on an empty middle column, `for m in '---' '--:' ':--' ':-:'` → widths 2, 2, 2, 3 — **the AC1 finding**
  - the same sweep with one character in the middle column → `X | q | Y$` in all four cases, the floor never binding
  - `sed -n '/^## Rules that live in exactly one place/,/^## A property/p' docs/architecture/overview.md | grep -c "no column's width depends on its marker"` → `0`
  - `sed -n '/^## Decision/,/^## Consequences/p' docs/architecture/adr/ADR-0007-*.md | grep -c "does not depend on its marker"` → `0`
  - a Python check comparing both change-log rows against `git show main:<path>` → `verbatim quote present: True` for both, `row cites ADR-0009: True`, both rows name BUG-0001
  - a Python check of frontmatter `version` against each top change-log row → `6 == 6` and `2 == 2`
  - `python3 -m unittest tests.test_units.WidthIndependenceTest -v` → 0, `Ran 2 tests`, `OK`
  - mutation: `sed -i '175s/.*/        widths.append(width)/' mdtab/table.py`, then the new test → `AssertionError: 2 != 3`, `FAILED (failures=1)`; `git checkout -- mdtab/table.py` → 0; suite back to `Ran 72 tests … OK`; `git status --short` → empty
  - `git diff --name-only main` → eight paths, none under `mdtab/`; `| grep -c '^mdtab/'` → `0`
  - `grep -rn "does not depend" mdtab/ tests/ docs/` and a wrap-tolerant regex sweep over `mdtab/*.py` → only true statements; `mdtab/table.py:185` says *alignment*
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 72 tests, at `64012f3`)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** (every row of `verify-report.md`'s criteria table names commands run here and quotes their real output; no row cites `impl-report.md`; the AC1 sweep and the AC2/AC3 string comparisons appear nowhere in that report)
  - `negative-cases-exercised` → **pass** (both sides of the "too narrow to hold its own marker" boundary triggered: an empty column under all four markers, and the same column with one character of content under all four; the first produced the AC1 failure)
  - `tests-would-fail-without-the-change` → **pass** (advisory; the floor removed from `_column_widths`, the new test failed `2 != 3`, restored, tree clean)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — created, `Verified-commit: 64012f3f46e6c419d035cdb4165efaecb630e583`
  - `tracker/items/BUG-0001/item.md` — AC2, AC3, AC4, AC5 and AC6 ticked; AC1 left unticked
  - no bug items filed
- **Status:** `verifying` → `in-progress`
- **Result:** Five criteria pass on evidence gathered here, including the mutation that proves the regression test bites and a string comparison proving ADR-0007's change log quotes the removed sentence verbatim. AC1 fails: the sentence written to replace the false absolute states that a column widens by one column per `:`, and one colon widens it by none — the same overstatement, one generation on, and it survived `lint-claims --all` because that gate checks a citation resolves, not that it supports.

## 2026-08-28T22:57:22Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress` after `verify` sent the item back on AC1, dispatched by `next`. The branch already carried the whole first pass, so this execution reconciled with it rather than starting over.
- **Inputs read:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — read **first**, per the procedure for a send-back: `Verified-commit: 64012f3…`, AC1 `fail`, AC2–AC6 `pass` and ticked, and the four-marker sweep that produced the finding
  - `tracker/items/BUG-0001/history.md` — four rows, the last `verifying → in-progress` by `verify`
  - `tracker/items/BUG-0001/item.md` — AC1 unticked, the other five ticked; AC1's four sub-clauses are the standard this pass is held to
  - `docs/architecture/overview.md` — the v6 bullet and the *"How wide a column is"* bullet below it
  - `mdtab/table.py` `_column_widths` — `max(width, needed + omitted)`, read to derive what the sentence should say instead of paraphrasing what it said
  - `tracker/items/BUG-0001/artifacts/plan.md` — to confirm no plan step was left undone; steps 1–5 all landed on the first pass
- **Decisions:**
  - **Reconciled rather than restarted.** `git log main..HEAD` showed the first pass's five commits intact, `verify` had ticked AC2–AC6 against `64012f3`, and the send-back named exactly one criterion. Only AC1's clause was touched; `ADR-0007`, `tests/test_units.py` and every ticked criterion were left alone, because re-editing a passed criterion invalidates its tick for nothing.
  - **The send-back's finding was checked and found to be worse than reported, before fixing it.** `verify` showed that an interior column with one colon is not widened. Running the same sweep on the **first column of a bare table** shows widths 1, 2, 2, 3 for `---`, `--:`, `:--`, `:-:` — there a single colon *does* widen, because the floor is `needed + omitted` and a missing leading pipe drops a guard space. So no per-marker increment rule is true in either direction, which rules out the obvious repair of "one wider for two colons" and is why the fix defers instead of restating.
  - **The bullet defers the arithmetic rather than restating it correctly.** The alternative was to spell out the full rule — dashes, colons, and the outer-pipe clause — in this bullet too. Rejected: the section's subject is *rules that live in exactly one place*, the bullet immediately below already states it correctly, and duplicating three clauses one bullet away is how the original defect happened. What is kept is the single concrete pair AC1 requires a reader to be able to predict.
  - **Every claim in the replacement was checked against the code, not against the sentence it replaces.** Five claims, five checks, tabulated in `impl-report.md`. The one generalisation left is hedged (*"can come out wider"*) and nothing is asserted about columns whose content already exceeds the minimum, which is the case the marker cannot reach.
  - **No test was added.** AC4 passed and is untouched; the sentence's one concrete claim is exactly the pair `test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it` already pins. Adding a one-colon test would be scope this item's criteria do not ask for.
  - **AC3 was re-satisfied deliberately.** `verify` ticked it but declared the tick invalidated by any further edit to the overview. The document is now `version: 7` with a v7 row naming BUG-0001 and quoting the removed clause in full, so the criterion is met again at the new head rather than inherited.
- **Questions raised:** none
- **Commands:**
  - `for m in '---' '--:' ':--' ':-:'; do printf 'a | | b\n---|%s|---\nc | | d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done` → interior column widths 2, 2, 2, 3
  - `for m in '---' '--:' ':--' ':-:'; do printf ' |a|b\n%s|---|---\n |c|d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done` → bare first-column widths 1, 2, 2, 3 — the half the send-back did not name
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab` → 0, middle column 2; with `---|:-:|---` → 0, middle column 3
  - `python3 -m unittest discover -s tests -t .` → 0, `Ran 72 tests in 0.139s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → 0, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → 0, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → 0, `all 6 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `git diff --name-only main | grep -c '^mdtab/'` → `0`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 72 tests, at branch head `07a8966` and again after the report commit)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** (AC1's four sub-clauses are each demonstrated by a command in `impl-report.md`'s second-pass section — the two sweeps, the two reproduce commands, and the claim-by-claim table; AC2–AC6 keep the first pass's evidence, unchanged and re-run at the new head)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 6 commits)
  - `no-unplanned-scope` → **pass** (advisory; this pass changes `docs/architecture/overview.md` and this item's own tracker files, nothing else)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 and `--all` exit 0 — noted in the report that this gate passed over the false v6 sentence too, because it checks that a citation resolves and not that it supports)
- **Artifacts:**
  - `docs/architecture/overview.md` — v7, the AC1 clause corrected
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — a `## Second pass — the AC1 send-back` section added above the first pass's report, which is unchanged
  - branch `wi/BUG-0001`, commits `fa9f067..07a8966` plus the report commit
- **Status:** `in-progress` → `verifying`
- **Result:** AC1's clause no longer states an increment rule that neither an interior column nor a bare table's first column obeys. The bullet names the minimum-width rule, defers its arithmetic to the bullet that owns it, and keeps the one concrete pair a reader needs to predict both of the item's reproduce commands. Nothing else on the branch moved: ADR-0007 stays at v2, the test is unchanged, and `mdtab/` is untouched.

## 2026-08-28T23:04:46Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable item (WI-0001, WI-0002 and WI-0003 are `done`, EP-001 is `open`, both of which have a null owner). Second verification: the first sent the item back on AC1 and `implement` returned it here at `7a83da9`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the six criteria, read before the implementation report
  - `tracker/items/BUG-0001/artifacts/plan.md` — the five steps, the AC mapping, and the last risk, which asks this skill to sweep the tree for a fourth copy of the sentence before ticking AC1
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — both passes, checked rather than trusted
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — the first pass's send-back, including its note that AC3's tick would be invalidated by the AC1 fix
  - `tracker/items/BUG-0001/history.md`, `tracker/project.yaml`
  - the branch `wi/BUG-0001` at `7a83da96661a902c2d8d1dfba89b50428d2aa51d`: `mdtab/table.py` (`_column_widths`, `column_alignments`, `_render_cell`), `tests/test_units.py`, `docs/architecture/overview.md`, `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md`
  - `tracker/items/WI-0002/item.md` AC6 and `tracker/items/WI-0001/item.md` AC12 with `WI-0001/Q-005`, to decide whether the corrected sentence's citations support it rather than merely resolve
- **Decisions:**
  - **AC1 passes.** The five claims in the replacement text were checked one at a time against the code, not against the prose. The one that needed real work is *"a column's width does not depend on the alignment its marker declares"*: the discriminating evidence is that `column_alignments` maps both `---` and `:--` to `left` while the bare-table sweep gives those two markers widths 1 and 2, and that `--:` and `:--` declare different alignments and give the same width — so the width is not a function of the alignment, and `_column_widths` never reads one. Without that pair the sentence would only have been plausible.
  - **AC1's "predict the output of both commands" is passed on a stated reading**, recorded in `## Not verified, and why`: the bullets state literally the one thing the two outputs differ in, and the floor rule reproduces both numbers, but they do not contain the whole rendering arithmetic. The stricter reading is not satisfiable by any pair of bullets in a rules-live-in-one-place list, so it cannot be the intended one. Declared rather than assumed, so `review-close` can disagree with a sentence instead of with a silence. No question filed: the criterion is decidable on the record, and the first verification decided the same sub-clause the same way.
  - **AC3 was re-verified rather than carried over**, because the first pass explicitly recorded its own tick as invalidated by the AC1 fix. It now holds at v7. AC2, AC4, AC5 and AC6 were also re-run rather than inherited, since a second pass over a changed head cannot borrow the first's evidence.
  - **No defect filed and no send-back.** The two things worth recording are not this item's: the wrong evidence line in `WI-0002/artifacts/review.md` is a closed item's record and is explicitly out of scope here, and `lint-claims`' inability to see this class of bug is a toolkit property already recorded in `EP-001/artifacts/review.md`. Both are in `## Defects found` as observations.
  - No criterion was judged `ambiguous`.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.146s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 0, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 8 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, `a |  | b$` / `--|--|--$` / `c |  | d$`
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, `a |   | b$` / `--|:-:|--$` / `c |   | d$`
  - interior four-marker sweep (`---`, `--:`, `:--`, `:-:` on an empty middle column) → exit 0, widths 2, 2, 2, 3
  - bare-table four-marker sweep (same markers on the first column of ` |a|b`) → exit 0, widths 1, 2, 2, 3
  - content four-marker sweep (`a | q | b`) → exit 0, identical output under all four
  - `sed -n '/^## Rules that live in exactly one place/,/^## A property/p' docs/architecture/overview.md | grep -c "…marker…"` → `0`
  - `grep -rn "width does not depend on its marker\|width is the same whatever its marker\|no column's width depends on its marker\|one column wider for each" --include='*.md' --include='*.py' .` → exit 0; no hit under `mdtab/` or `tests/`, and every `docs/` hit is a change-log row quoting what it removed or `ADR-0009` ruling on the sentence
  - Python: frontmatter version versus top change-log row version for both documents → `overview.md 7 | 7 | equal: True`, `ADR-0007 2 | 2 | equal: True`, both rows naming BUG-0001
  - Python: the v2 change-log row's quoted text compared against `git show main:<adr>` → `verbatim quote present: True`, `row cites ADR-0009: True`
  - `sed -n '96,122p' mdtab/table.py`, `sed -n '150,200p' mdtab/table.py` → `column_alignments` maps `---` and `:--` to `left`; `_column_widths` computes `max(width, needed + omitted)` and never calls `column_alignments`
  - `python3 -m unittest tests.test_units.WidthIndependenceTest -v` → exit 0, `Ran 2 tests … OK`
  - mutation: `cp mdtab/table.py /tmp/table.py.bak`; line 175 replaced by `widths.append(width)`; `python3 -m unittest tests.test_units.WidthIndependenceTest -v` → exit 1, `AssertionError: 2 != 3`; full suite → `FAILED (failures=4)`; restored from the backup → `Ran 72 tests … OK`, `git status --short` empty
  - `git diff --name-only main` → nine paths, none under `mdtab/`; `| grep -c '^mdtab/'` → `0`
  - `git diff main -- tests/test_units.py docs/` → every hunk traces to plan steps 1–4 or to the AC1 correction; no unaccounted change
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 72 tests`, `OK`, at `7a83da9`)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (each of the six rows in `verify-report.md` names commands run in this execution and quotes their real output; no row cites `impl-report.md` as evidence; AC1 was decided by three sweeps and by reading `_column_widths` and `column_alignments`, AC2 and AC3 by string comparison in Python against `git show main:…`, AC4 by mutation)
  - `negative-cases-exercised` → **pass** (the *column too narrow to hold its own marker* boundary triggered on both sides and in both outer-pipe styles: 2/2/2/3 interior, 1/2/2/3 bare, identical under all four markers with content; AC6's negative checked against the diff and again after the mutation was reverted)
  - `tests-would-fail-without-the-change` → **pass**, advisory (the floor removed from `_column_widths`: the AC4 test failed `2 != 3` and the suite reported four failures; restored, and the tree is clean. AC1, AC2, AC3 and AC6 have no test of their own and cannot — they are criteria about document text and about a diff's contents — which is recorded in the report)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — rewritten for the second pass, `Verified-commit: 7a83da96661a902c2d8d1dfba89b50428d2aa51d`
  - `tracker/items/BUG-0001/item.md` — AC1 ticked; AC2–AC6 re-verified at this head and left ticked
  - no bug item filed
  - commit: `tracker: the second verification, the six ticked criteria, and the move to review (refs BUG-0001)`
- **Status:** `verifying` → `in-review`
- **Result:** All six criteria pass on evidence gathered here at `7a83da9`. The v6 clause the first pass rejected is gone; its replacement defers the colon arithmetic to the bullet that owns it and every claim in it survives a four-marker sweep in both the interior and the bare-table case, which is what the previous wording did not. Nothing under `mdtab/` changed, the regression test genuinely fails when the width floor is deleted, and the false sentence is absent from every live claim in the tree. The item goes to `in-review`.

## 2026-08-28T23:10:02Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0001
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable item — WI-0001, WI-0002 and WI-0003 are `done` and EP-001 is `open`, all of which have a null owner in `pipeline.yaml`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md`, `history.md` (seven rows), `journal.md` (all seven entries, in full), `artifacts/plan.md`, `artifacts/impl-report.md` (both passes), `artifacts/verify-report.md` (second pass). No `questions/` directory exists on this item
  - the diff `main..wi/BUG-0001` — `git diff main -- tests/test_units.py docs/` hunk by hunk, and `git diff --name-only main` for the changed-path list
  - `mdtab/table.py`: `_column_widths` (150–177), `column_alignments` (96–120), `_render_cell` (179–200)
  - `docs/architecture/adr/ADR-0005-…md` `## Decision`; `docs/architecture/adr/ADR-0009-…md` `## Decision`; `docs/architecture/adr/ADR-0007-…md` `## Decision` item 4 and its change log; `docs/architecture/overview.md` lines 60–140
  - `tests/test_units.py` and `tests/test_fixtures.py` module docstrings; `tests/fixtures/align-empty-cell.{in,out}.md`
  - `tracker/items/WI-0001/questions/Q-004.md` (the precedent on ADR-0005's literal rule), `tracker/items/WI-0001/item.md` AC12, `tracker/items/WI-0001/questions/Q-005.md`, `tracker/items/WI-0002/item.md` AC6
- **Decisions:**
  - **Rejected on one blocking finding**, recorded in `artifacts/review.md`: the test added for AC4 builds two whole markdown documents from Python string literals and runs them through `python3 -m mdtab`, inside `tests/test_units.py`. `ADR-0005` `## Decision` says *"Fixtures are the only place a test may express a document; a test may not build one from a Python literal"*, and `test_units.py`'s own module docstring reserves whole documents for `tests/fixtures/` and `test_fixtures.py`. Before this change that module imported no `subprocess` and had no process boundary in it.
  - **Not escalated to the architect, deliberately.** The escalation route is for a contradiction where it is unclear which side gives way, and here the record already rules: `WI-0001/Q-004` weighed five options for a document that could not be a literal and rejected option D, *"keep the literal, declare the deviation"*, as leaving ADR-0005's rule *"broken in the one place it was written for"*; `WI-0001`'s review finding 1 required exactly this conversion and it was made. No ADR needs amending either, because two fixture pairs satisfy `ADR-0005` and AC4's wording at the same time — the test still runs both commands from `## Steps to reproduce` and still asserts 2 and 3. Forwarding a question whose answer is already in the record would have cost a round trip and decided nothing.
  - **`plan.md` step 1 was the ADR-compliant route** — `lay_out` on a list of lines is a fragment, which ADR-0005 permits and which every other test in that module uses. `implement` deviated to satisfy AC4's wording, which is not amendable by `implement`, and declared the deviation and its cost rather than hiding it. That was the right thing to do with it; the fixture route is what resolves it, and it needs no criterion to change.
  - **No criterion unticked and no bug filed.** Nothing this finding touches is a failure of an acceptance criterion — AC4 is satisfied by the test as written, and the defect is that the test breaks a rule no criterion states. AC6 is unaffected: `tests/fixtures/` is not under `mdtab/`.
  - **Second, non-blocking finding, recorded so a rewritten report does not lose it:** `verify-report.md`'s bare-table sweep calls its numbers *"widths 1, 2, 2, 3"*; those are the rendered leading-field widths, and the column widths `_column_widths` computes for that table are 2, 3, 3, 4 — the difference being the guard space the missing outer pipe drops. The inference is correct under either measure, but an item about a sentence that conflated two nearby quantities should not conflate two nearby quantities in its evidence.
  - **The declared gaps were read and agreed with**, and are in `review.md` `## Accepted gaps` for the pass that closes the item: AC1's *"predict the output"* sub-clause was passed on a stated reading, which is the only satisfiable one; and `WI-0002/artifacts/review.md` line 64 holds a wrong verification record on a closed item, which is history rather than a live claim and is out of this item's scope.
  - **No merge was attempted.** `git rev-parse main` is `5db7845902546b7e38cba59af51f5095ec6a965e`, unchanged, and `git worktree list` shows only the main checkout — no trial worktree was created, so there was nothing that could have advanced the trunk (F-055).
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.139s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0, `verified at 7a83da96; wi/BUG-0001 has moved to caf8eba3 but only the record changed (5 file(s) under tracker/ or docs/)`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 9 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 2 document(s) changed since main`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-epic-signoff BUG-0001` → exit 0, `BUG-0001 is a 'bug', not an epic — the termination gate applies to an engagement's ending only. PASS.`
  - `git diff main -- tests/test_units.py docs/`; `git diff --name-only main` → nine paths, none under `mdtab/`
  - `grep -n "filtered(\|subprocess" tests/test_units.py` → the helper and its two call sites are the only ones; the module had no process boundary before this change
  - `git rev-parse main` → `5db7845902546b7e38cba59af51f5095ec6a965e`; `git worktree list` → one entry, the main checkout
- **Gates:**
  - `definition-of-done` → **pass** for D1–D8 and D10–D12, `not reached` for D9 (no merge, the item is rejected) — the per-criterion table with its evidence is `review.md` `## Definition of Done`. Recorded as a pass because every criterion that could be evaluated was evaluated and passed; the rejection rests on a finding outside D1–D12, which is what step 4 of the procedure is for
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the only movement since `7a83da9` is the record commit `caf8eba`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 9 commits)
  - `tests-pass-on-the-merge-result` → **skipped**: the item is rejected, so no trial merge was performed and there is no merge result to test. The suite passes on the branch head — `Ran 72 tests`, `OK` — which is what a rejection needs and is not the same claim
  - `workspace-valid` → **pass** (`validate-workspace` exit 0)
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep BUG-0001` alone: *what was built* — three false copies of one sentence corrected, plus a regression test, with nothing under `mdtab/` (`impl-report.md`, and the diff); *which skill decided what* — `review-close` filed the bug under DE6 at EP-001's termination review, `plan` wrote `ADR-0009` and the six-step plan, `implement` executed it twice, `verify` sent it back once and passed it once (seven history rows, seven journal entries, no gap); *what questions arose* — none on this item, and the ones it depends on (`WI-0001/Q-004`, `WI-0001/Q-005`, `WI-0002/Q-003`) are all `answered` with `## Consequences`; *what verification found* — the first pass's AC1 failure with the sweep that produced it, and the second pass's six passes with the mutation that proves the test bites
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0, 2 documents). Recorded with the caveat both verifications recorded: it proves a citation resolves, not that it supports. The supporting half is the D12 audit table in `review.md`, which was decided by opening each cited artifact
  - `epic-sign-off` → **pass**, not applicable (`check-epic-signoff BUG-0001` reports BUG-0001 is a bug, not an epic). EP-001 was not touched by this execution: it is not at rest while BUG-0001 is running, so no termination question is due
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/review.md` — what was examined, the D12 claim audit read from the citations, the twelve Definition of Done criteria, two findings, two accepted gaps and the verdict
  - `tracker/items/BUG-0001/item.md` — unchanged; no criterion was unticked and no outcome was recorded, because the item is not closing
  - no merge commit, no bug item, no question, no change under `tracker/items/EP-001/`
  - commit: `tracker: the review and the send-back on the fixture rule (refs BUG-0001)`
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected and sent back to `in-progress` on one finding. The correction this item exists to make is sound — the false sentence is gone from every live claim, what replaced it holds against `mdtab/table.py` claim by claim, ADR-0007 was corrected in place under all four of ADR-0009's conditions, and the regression test fails when the width floor is deleted — but the test keeps its two documents as Python string literals in `tests/test_units.py`, which `ADR-0005` forbids in terms and which `WI-0001/Q-004` already refused once. Two fixture pairs satisfy that rule and AC4's wording together, so no criterion and no ADR has to move.

## 2026-08-28T23:13:38Z — implement v0.2.2 — developer

- **Item:** BUG-0001
- **Trigger:** status `in-progress`, dispatched by `next`. Third pass: `review-close` rejected the item at `4025111` on one finding and returned it here. The branch `wi/BUG-0001` already existed with ten commits, so this execution reconciled with it rather than creating it, and the item was already at `in-progress` — there was no opening move to make and this is the execution's single entry.
- **Inputs read:**
  - `tracker/items/BUG-0001/artifacts/review.md` first, per the procedure for a send-back — finding 1 (blocking) and finding 2 (recorded, not mine)
  - `tracker/items/BUG-0001/item.md` (six criteria, all ticked by the second verification), `history.md` (eight rows, last one the rejection), `artifacts/plan.md`, `artifacts/impl-report.md` (both earlier passes), `artifacts/verify-report.md`
  - `tracker/project.yaml`; `tracker/items/BUG-0001/questions/` does not exist
  - `docs/architecture/adr/ADR-0005-tests-and-lint-come-from-the-standard-library.md` `## Decision` — the rule the finding rests on
  - `tests/test_fixtures.py` in full: `EXTENSIONS`/`NAMES` discovery, `UNTOUCHED`, `ALIGNED`, the eight tests that walk them, `path_of`/`read`/`run`/`pipe_columns`/`contents`, and `ProcessTest`
  - `tests/test_units.py` module docstring and `WidthIndependenceTest`
  - `tests/fixtures/align-empty-cell.{in,out}.md`, as the model for a hand-written pair
  - the branch: `git log --oneline` and `git diff --name-only main`, to reconcile before changing anything
- **Decisions:**
  - **Two fixture pairs rather than one.** AC4 is stated over *both* commands, so both documents have to exist as documents; a single pair plus one literal would leave the rule half-broken in the same file.
  - **The pairs go in `ALIGNED`, not `UNTOUCHED`.** They hold a table mdtab lays out, so their halves differ; `UNTOUCHED` asserts the two halves are identical. Registering them in `ALIGNED` also puts them through the eight document-level tests that walk that map, which is more coverage than the one test asked for and costs nothing.
  - **The assertion moved into `ProcessTest` in `test_fixtures.py`, not into a new class or into `test_units.py`.** AC4 requires the two *commands*, so the test needs the process boundary, and `ProcessTest` is where this project already puts that. Its docstring said *"AC1 — the one test that needs the process boundary"*, which a second test would have made false, so it is widened to name both reasons.
  - **`WidthIndependenceTest`'s docstring keeps both facts and points outward.** Plan step 2 exists because a class docstring asserting the opposite of its own test un-pins the criterion; the fix for that is not to delete the corrected docstring but to make its second half name where that half is now checked. The class keeps the test that is genuinely a fragment test.
  - **The expected outputs were derived by hand from the rules first, then compared with the tool** — `test_fixtures.py`'s docstring requires that order, because an output produced by running the code under test is a snapshot and not evidence. Both derivations are written out in `impl-report.md` and both matched.
  - **Nothing in `docs/` was touched.** The finding is about a test file. AC1, AC2 and AC3 were passed against `overview.md` v7 and `ADR-0007` v2, and re-editing a passed document would invalidate three ticks to fix none of them.
  - **No question filed and no criterion changed.** The finding named a route that satisfies `ADR-0005` and AC4's wording together, so nothing had to be escalated and nothing had to be re-litigated.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline -8 wi/BUG-0001`, `git diff --name-only main`, `git status --short` → reconciled: ten commits on the branch, the two documents and `tests/test_units.py` changed, tree clean
  - `printf … > tests/fixtures/width-marker-dashes.in.md` and three more, then `cat -A` on all four → the exact bytes, verified against the hand-derivation
  - `python3 -m unittest tests.test_fixtures.ProcessTest -v` → exit 0, `Ran 3 tests … OK`
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.139s`, `OK` — the same count as before, one test having left `test_units.py` and one arrived in `test_fixtures.py`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - mutation: `cp mdtab/table.py /tmp/t.bak`; line 175 → `widths.append(width)`; the moved test → `AssertionError: 2 != 3`, full suite → `FAILED (failures=5)`; restored from the backup → `Ran 72 tests … OK`, `git status --short` clean
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 11 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 2 document(s)`; `--all` → exit 0, `checked the whole tree`, `0 errors, 0 warnings`
  - `git diff --name-only main | grep -c '^mdtab/'` → `0`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 72 tests`, `OK`, at `d6d2ecb`)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0)
  - `every-criterion-has-a-test` → **pass**. AC4 is `tests/test_fixtures.py`, `ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it`, plus the eight document-level tests the two new pairs now enter through `ALIGNED`; its sensitivity was demonstrated by mutation, not asserted. AC1, AC2 and AC3 are document criteria demonstrated by exact commands over the documents together with the two `python3 -m mdtab` runs whose output AC1 requires a reader to predict; AC5 is the two gate commands; AC6 is `git diff --name-only main | grep -c '^mdtab/'` → `0`
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 11 commits)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0, and `--all` exit 0)
  - `no-unplanned-scope` → **pass** (advisory). Five files move on this pass: four new fixtures under `tests/fixtures/` and `tests/test_fixtures.py`, which are plan step 1 relocated to where `ADR-0005` requires, and `tests/test_units.py`, which loses what moved and keeps plan step 2's docstring correction. Nothing else, and nothing under `mdtab/` or `docs/`
- **Artifacts:**
  - `tests/fixtures/width-marker-dashes.{in,out}.md`, `tests/fixtures/width-marker-colons.{in,out}.md` — new
  - `tests/test_fixtures.py` — two `ALIGNED` entries, `ProcessTest`'s widened docstring, and the moved test
  - `tests/test_units.py` — three imports, `ROOT`, `filtered()` and the moved test removed; `WidthIndependenceTest`'s docstring repointed
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — a `## Third pass` section, the AC4 evidence row superseded, deviation 1 marked resolved, and four new `## What I did not do` bullets
  - branch `wi/BUG-0001`, commits `fa9f067..d6d2ecb`; this pass is `d6d2ecb`
- **Status:** `in-progress` → `verifying`
- **Result:** The review's finding 1 is fixed. AC4's two documents are `tests/fixtures/width-marker-dashes` and `width-marker-colons`, hand-derived and byte-exact; the assertion runs both commands from `ProcessTest`, which is where this project keeps tests stated over `python3 -m mdtab`; and `tests/test_units.py` is a fragment-only module again, keeping the docstring correction plan step 2 asked for. The moved test still fails with `AssertionError: 2 != 3` when the width floor is deleted. Nothing in `docs/` and nothing under `mdtab/` changed, so AC1, AC2, AC3 and AC6 stand where the second verification left them.

## 2026-08-28T23:19:24Z — verify v0.1.4 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** status `verifying`, reached from `in-progress` at `4d8f630` after `implement`'s
  third pass fixed `review.md` finding 1; dispatched by `next` as the only runnable item (the
  three work items are `done` and EP-001's `open` has no owner).
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — all six criteria, read before anything else and before the
    implementation report, so each verdict is derived from the criterion rather than from what was
    built
  - `tracker/items/BUG-0001/history.md` — nine rows, `— → ready → planned → in-progress →
    verifying → in-progress → verifying → in-review → in-progress → verifying`
  - `tracker/items/BUG-0001/artifacts/plan.md` — the six-step plan, the AC mapping table, and its
    last risk, which asks verify to sweep the tree for a fourth copy of the false sentence
  - `tracker/items/BUG-0001/artifacts/impl-report.md` — all three passes, read after the criteria
    and cited as evidence nowhere
  - `tracker/items/BUG-0001/artifacts/review.md` — finding 1 (the send-back) and finding 2 (the
    mislabelled sweep quantity this report was asked to fix)
  - `tracker/project.yaml` — the test and lint commands
  - the branch `wi/BUG-0001` at `4d8f6306d69c7b0ebb35d9e5f02c4e775a02a741`, working tree clean:
    `docs/architecture/overview.md` v7 §"Rules that live in exactly one place",
    `docs/architecture/adr/ADR-0007-…md` v2 `## Decision` and change log, the four
    `tests/fixtures/width-marker-*` files, `tests/test_fixtures.py` and `tests/test_units.py` as
    diffed against `main`, and `mdtab/table.py` lines 145–205 (`_column_widths`, `_render_cell`)
- **Decisions:**
  - **Every verdict re-derived rather than carried over.** The second verification passed all six
    criteria at `7a83da9` and only `tests/` moved since. Carrying AC1–AC3 forward would have been
    defensible and was rejected: the report is the record, `review.md` finding 2 required part of
    it rewritten anyway, and a criterion whose evidence is "it passed last time" is not
    independently checked. All six were re-run against this head.
  - **AC1's colon arithmetic checked in three regimes, not one.** The v6 wording passed the two
    reproduce commands and was still false; what caught it was the one-colon interior column. So
    AC1 was decided against the interior sweep, the bare-table sweep and a content-exceeds-the-
    minimum sweep, plus `_column_widths` called directly for the widths behind the printed bytes.
    The v7 sentence survives all three because it hedges and defers instead of restating.
  - **The lost blank line in `tests/test_units.py` is a finding, not a send-back.** `git diff main`
    has a hunk removing one blank line above `parsed()`, which no plan step and no criterion
    accounts for and which contradicts `impl-report.md`'s claim that the file "returns to what it
    was". Classification, by the rule in the procedure: no acceptance criterion of this item says
    the behaviour should be different (AC6 constrains `mdtab/` only), so it is not a send-back; and
    nothing another item delivered is wrong, so it is not a bug item. Recorded in
    `verify-report.md` `## Defects found` for `review-close`, which is the skill that can require
    it fixed before merge.
  - **`review.md` finding 2 fixed by measuring both quantities.** The previous report called the
    bare-table sweep's printed leading fields "widths 1, 2, 2, 3". They are the rendered fields;
    `_column_widths` returns 2, 3, 3, 4 for that table, the difference being the guard space the
    missing outer pipe drops. Both are now computed and named in the report — the printed form from
    the sweep, the widths from calling the function.
  - **Two mutations rather than one.** The floor mutation proves the AC4 test is sensitive. It does
    not prove the two new fixture pairs are reached by the `ALIGNED` map's document-level tests, so
    `width-marker-colons.out.md` was corrupted separately and produced its own failure. Both were
    reverted in this execution and the tree is clean.
  - No criterion was judged ambiguous, so no question was filed.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.140s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/lint-claims --all` → exit 0, `0 errors, 0 warnings`
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, `a |  | b$`
  - `printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, `a |   | b$`
  - `for m in '---' '--:' ':--' ':-:'; do printf 'a | | b\n---|%s|---\nc | | d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done` → exit 0, widths 2, 2, 2, 3
  - `for m in '---' '--:' ':--' ':-:'; do printf ' |a|b\n%s|---|---\n |c|d\n' "$m" | python3 -m mdtab | sed -n '1p' | cat -A; done` → exit 0, rendered leading fields 1, 2, 2, 3
  - `for m in '---' '--:' ':--' ':-:'; do printf 'a | q | b\n---|%s|---\nc | r | d\n' "$m" | python3 -m mdtab | sed -n '1p'; done` → exit 0, `a | q | b` four times
  - `python3 -c` calling `_column_widths` on both sweeps → interior `[2,2,2,3]`, bare first column `[2,3,3,4]`
  - `sed -n '/^## Decision/,/^## Consequences/p' docs/architecture/adr/ADR-0007-*.md | grep -c "does not depend on its marker"` → `0`
  - `grep -n '^- \*\*Status:\*\*' docs/architecture/adr/ADR-0007-*.md` → `12:- **Status:** accepted`
  - `sed -n '/^## Change log/,$p' docs/architecture/overview.md` → exit 0, top row `| 7 | … | implement | BUG-0001 | …`, frontmatter `version: 7`
  - `cat -A tests/fixtures/width-marker-{dashes,colons}.{in,out}.md` → exit 0, bytes identical to the two reproduce commands and their outputs
  - `git diff main -- tests/test_fixtures.py tests/test_units.py` → exit 0, two hunks in each file
  - `git diff --name-only main` → exit 0, 15 paths; `| grep -c '^mdtab/'` → `0`
  - mutation: `widths.append(max(width, needed + omitted))` → `widths.append(width)`, then `python3 -m unittest tests.test_fixtures.ProcessTest.test_a_marker_with_colons_widens_a_column_too_narrow_to_hold_it` → `AssertionError: 2 != 3`, `FAILED (failures=1)`; full suite → `FAILED (failures=5)`; restored from backup → `Ran 72 tests … OK`, `git status --short` empty
  - mutation: `tests/fixtures/width-marker-colons.out.md` widened by one column, full suite → `FAILED (failures=1)`; restored → `git status --short` empty
  - `grep -rn "width does not depend on its marker\|width is the same whatever its marker\|no column's width depends on its marker" --include='*.md' --include='*.py' .` → exit 0, no hit under `mdtab/` or `tests/`; every `docs/` hit is a required change-log quote or `ADR-0009` ruling on the sentence
  - `grep -n -B2 '^def \|^class ' tests/test_units.py` → exit 0, `parsed` at line 25 preceded by one blank line where every other top-level definition has two
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests`, `OK`, at `4d8f630` with a clean tree)
  - `lint-clean` → **pass** (`python3 -W error -m compileall -q mdtab tests` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, `0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (six rows in `verify-report.md`, each naming commands run in this execution with their real output; `impl-report.md` is cited as evidence nowhere)
  - `negative-cases-exercised` → **pass** (six cases in `## Negative and boundary cases exercised`: the one-colon interior column, the bare-table outer-pipe case, content past the minimum, the floor mutation, the corrupted fixture, and the tree-wide sweep for a fourth copy)
  - `tests-would-fail-without-the-change` (advisory) → **pass** (two independent mutations, both run and both reverted)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/verify-report.md` — rewritten from scratch for the third pass, with `review.md` finding 2's quantity correction folded in
  - `tracker/items/BUG-0001/item.md` — all six criteria ticked; every tick re-demonstrated in this execution, none carried over
  - no bug item filed; no question filed
  - commit of this execution's record, per `conventions.commit-subject`
- **Status:** `verifying` → `in-review`
- **Result:** All six criteria pass at `4d8f6306d69c7b0ebb35d9e5f02c4e775a02a741`. The two AC4
  documents are now `tests/fixtures/width-marker-{dashes,colons}` pairs read by
  `ProcessTest`, which satisfies `review.md` finding 1 and `ADR-0005` together; the test still
  fails `2 != 3` when the width floor is deleted, and the pairs are genuinely walked by the
  document-level tests. Nothing in `docs/` and nothing under `mdtab/` moved on this pass. One
  finding no criterion covers is recorded for `review-close`: a blank line above `parsed()` in
  `tests/test_units.py` was lost, so that file did not quite return to what it was.

## 2026-08-28T23:23:53Z — review-close v0.5.0 — reviewer

- **Item:** BUG-0001
- **Trigger:** status `in-review`, dispatched by `next` step 5 as the only runnable item — WI-0001,
  WI-0002 and WI-0003 are `done` and EP-001 is `open`, all of which have a null owner in
  `pipeline.yaml`. Second review of this item; the first rejected it at `4025111`.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md`, `history.md` (ten rows), `journal.md` (all ten entries, in
    full), `artifacts/plan.md`, `artifacts/impl-report.md` (all three passes),
    `artifacts/verify-report.md` (the third pass), and the previous `artifacts/review.md`
  - `tracker/items/BUG-0001/questions/` — does not exist; no question was filed on this item
  - the diff range `main..wi/BUG-0001` (`5db7845..67b2957`), hunk by hunk: `git diff main --
    docs/`, `git diff main -- tests/test_fixtures.py tests/test_units.py`, `cat -A` on the four
    new fixture files, and `git diff --name-only main` for the full path list
  - `mdtab/table.py` — `_column_widths` (149–176), `_render_cell` (179–205), `_spaces_omitted`
  - `docs/architecture/adr/ADR-0009-*.md` `## Decision` (the four conditions),
    `docs/architecture/adr/ADR-0007-*.md` `## Decision` item 4 and its change log,
    `docs/architecture/adr/ADR-0005-*.md` `## Decision`
  - `docs/architecture/overview.md` — the corrected bullet and the "How wide a column is" bullet
  - `tests/test_fixtures.py` in full (`ALIGNED`, the discovery helpers, `ProcessTest`) and
    `tests/test_units.py`'s module docstring and `WidthIndependenceTest`
  - `tracker/items/WI-0002/item.md` AC6; `tracker/items/WI-0001/item.md` AC12 and
    `tracker/items/WI-0001/questions/Q-004.md` and `Q-005.md` — opened for the D12 audit, so each
    claim was decided from what it cites rather than from the sentence
  - `.claude/agile-skills/spec/dor-dod.md` §3 and §4
- **Decisions:**
  - **Accepted, and merged.** The previous rejection named one thing — the two AC4 documents must
    live in `tests/fixtures/` rather than in Python literals — and the third pass did exactly that
    and no more. The correction the item exists to make was already sound and is unchanged: three
    copies of a false absolute gone from live text, ADR-0007 corrected in place under all four of
    `ADR-0009`'s conditions, nothing under `mdtab/`.
  - **The lost blank line is an accepted gap, not a rejection.** `verify` found a hunk in
    `tests/test_units.py` that removes one blank line above `parsed()`, which no plan step and no
    criterion accounts for and which makes `impl-report.md`'s "returns to what it was" one line
    short of true. Routed as an accepted gap because the project has no style gate to have caught
    it — `commands.lint` compiles rather than lints — and because a rejection would cost a full
    `implement` → `verify` → `review-close` cycle for one whitespace character that changes no
    behaviour, no output and no document. Recorded in `review.md` `## Findings` 1 and written into
    `item.md`'s `## Notes`, with the reasoning, so a later reviewer can disagree with a sentence
    rather than with a silence.
  - **`verify`'s routing of that finding was correct and is endorsed.** It is not a send-back (no
    criterion of this item is about it) and not a bug item (nothing another item delivered is
    wrong), which is the classification the procedure's own test gives.
  - **The D12 audit was re-run from the citations rather than inherited.** The previous review's
    audit table covered the same claims, but the report is the record and an audit whose evidence
    is "it passed last time" is not an audit. Seven claims, each decided by opening the cited
    artifact and `mdtab/table.py`; the one that needed real work is the alignment claim, where the
    discriminating evidence is that `---` and `:--` declare the same alignment and give different
    widths while `--:` and `:--` declare different alignments and give the same width.
  - **Two gaps carried forward rather than filed as items.** AC1's stated reading of "predict the
    output" is agreed for the second time. `WI-0002/artifacts/review.md` line 64's wrong
    verification record is accepted as history: filing a follow-up would put a correction to a
    closed item's paperwork in front of the stakeholder as an undelivered child of the epic, which
    is worse than the thing it fixes. Both are now in `item.md`'s `## Notes`, not only in reports.
  - **The trial merge was made in a detached worktree and `main` was checked before and after.**
    `git rev-parse main` returned `5db7845…` both times, so the trial moved nothing (F-055).
  - **The item was closed before the branch was merged**, so `commits-reference-the-item` had a
    non-empty range to inspect; the real merge follows the close.
- **Questions raised:** none on this item. A `kind: sign-off` question is due on **EP-001**, which
  re-reaches rest as this item closes — that is a separate transition of the epic and is journalled
  there.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.140s`, `OK`
  - `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings`
  - `python3 .claude/agile-skills/scripts/check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0, `verified at 4d8f6306; wi/BUG-0001 has moved to 67b2957f but only the record changed (5 file(s) under tracker/ or docs/)`
  - `python3 .claude/agile-skills/scripts/check-commit-refs BUG-0001 wi/BUG-0001` → exit 0, `all 13 commit(s) on main..wi/BUG-0001 name BUG-0001`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 2 document(s)`; `--all` → exit 0, `0 errors, 0 warnings`
  - `git rev-parse main` → `5db7845902546b7e38cba59af51f5095ec6a965e` (before the trial)
  - `git worktree add --detach /tmp/mdtab-trial-bug1 main` → exit 0, `HEAD is now at 5db7845`
  - `git -C /tmp/mdtab-trial-bug1 merge --no-ff wi/BUG-0001` → exit 0, clean; `git -C … rev-parse HEAD` → `24807544791428e6a94611d66bd4385bebedb66b`
  - in the trial: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 72 tests in 0.145s`, `OK`; `python3 -W error -m compileall -q mdtab tests` → exit 0
  - `git worktree remove --force /tmp/mdtab-trial-bug1` → exit 0; `git worktree list` → one entry
  - `git rev-parse main` → `5db7845902546b7e38cba59af51f5095ec6a965e` (after the trial — unmoved)
  - `git diff main -- docs/` and `git diff main -- tests/test_fixtures.py tests/test_units.py` → every hunk traced; the only unaccounted one is finding 1
  - `git diff --name-only main` → fifteen paths; `| grep -c '^mdtab/'` → `0`
  - `cat -A tests/fixtures/width-marker-{dashes,colons}.{in,out}.md` → the exact bytes of the two reproduce commands and their outputs
  - `printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab | cat -A` → exit 0, `a |  | b$`; with `---|:-:|---` → exit 0, `a |   | b$`
  - `python3 -c` calling `_column_widths` on the interior and bare-table sweeps → `[3,2,3]`/`[3,2,3]`/`[3,2,3]`/`[3,3,3]` and `[2,3,3]`/`[3,3,3]`/`[3,3,3]`/`[4,3,3]`
  - a Python check comparing ADR-0007's v2 change-log row against `git show main:<adr>` → `verbatim quote present in v2 row: True`, `row names BUG-0001: True`, `row cites ADR-0009: True`, `status accepted: True`, `frontmatter version: 2`
  - `grep -n -B2 '^def \|^class ' tests/test_units.py` → `parsed` at line 25 with one blank line above it, every other top-level definition with two — finding 1
- **Gates:**
  - `definition-of-done` → **pass**, D1–D12 all pass. The per-criterion table with its evidence is `review.md` `## Definition of Done`; D9 is passed on the trial merge plus the real merge that follows this transition
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0; the last code change is `d6d2ecb` and the verification is at `4d8f630`, after it; everything since is record)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, 13 commits, run before the merge so the range is non-empty)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` inside the detached trial worktree at merge commit `2480754` → exit 0, `Ran 72 tests`, `OK`; `compileall` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, `0 errors, 0 warnings`)
  - `record-is-reconstructible` → **pass**. From the tracker, `docs/` and `git log --grep BUG-0001` alone: *what was built and why* — three false copies of one sentence corrected and a regression test added, with nothing under `mdtab/`, because the tool was right and the documents were wrong (`item.md`, `plan.md`, `impl-report.md`, the diff); *which skill decided what* — `review-close` filed the bug under DE6 at EP-001's termination review, `plan` wrote `ADR-0009` and the six-step plan, `implement` executed it three times, `verify` sent it back once and passed it twice, `review-close` rejected it once and closed it once — ten history rows, ten journal entries, no gap; *what questions arose and how they were resolved* — none on this item; the ones it depends on (`WI-0001/Q-004`, `WI-0001/Q-005`, `WI-0002/Q-002`) are `answered` with `## Consequences` naming real files; *what verification found* — the AC1 increment-rule failure with the sweep that produced it, then two passes, the second re-derived from scratch with the mutations quoted
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 over 2 documents, `--all` exit 0). Recorded with the caveat every execution on this item has recorded: it proves a citation resolves, not that it supports. The supporting half is the seven-row D12 audit in `review.md`, decided by opening each cited artifact
  - `epic-sign-off` → **not applicable to this transition** (`check-epic-signoff` is a gate on an epic's ending; BUG-0001 is a bug). EP-001 re-reaches rest as this item closes, and the sign-off due there is filed in the same execution, on the epic, with its own gate run
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/review.md` — rewritten for this pass: what was examined, the seven-row D12 audit read from the citations, twelve Definition of Done criteria, one finding, four accepted gaps, the verdict
  - `tracker/items/BUG-0001/item.md` — `## Notes` gains the three accepted gaps that must survive the item; `status: done`, `outcome: delivered` written by this transition
  - the merge of `wi/BUG-0001` into `main`, made after this transition so the commit-ref range was non-empty
  - no bug item filed, no question filed on this item
- **Status:** `in-review` → `done`
- **Result:** BUG-0001 is delivered. The false absolute is gone from `docs/architecture/overview.md`
  and `ADR-0007` and from a test docstring; what replaced it survives a claim-by-claim check against
  `_column_widths` and three four-marker sweeps; ADR-0007 kept `status: accepted` under all four of
  `ADR-0009`'s conditions with the removed sentence quoted verbatim, confirmed by string comparison
  against `main`; and the behaviour is pinned by a test that fails `2 != 3` without the width floor
  and by two fixture pairs walked by the document-level tests. Nothing under `mdtab/` changed. One
  cosmetic finding — a blank line lost in `tests/test_units.py` — is accepted and recorded in the
  item's `## Notes` rather than sent back.
