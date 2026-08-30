## 2026-08-30T18:53:12Z — retro v0.1.0 — process-analyst

- **Item:** EP-001
- **Trigger:** invoked directly on the ended engagement; `scripts/engagement-state EP-001` reports
  `ended` — the epic is `done`, rest was reached at 2026-08-28T15:41:23Z, and no
  `artifacts/retro.md` existed. This skill is not dispatched on a status.
- **Inputs read:**
  - `tracker/items/EP-001/item.md` — the goal, the five success measures, the scope and
    out-of-scope lists, both sign-off sections and the recorded ending
  - `tracker/items/*/item.md` — all eleven, with their criteria, tick state, outcomes and the
    accepted gaps in `## Notes`
  - `tracker/items/*/history.md` — all eleven, 88 rows, read end to end and checked against the
    journals and the items' statuses
  - `tracker/items/*/journal.md` — all eleven, **88 entries, every one read in full**: EP-001 8,
    WI-0001 9, WI-0002 9, WI-0003 11, WI-0004 9, BUG-0001 6, BUG-0002 8, BUG-0003 6, BUG-0004 8,
    BUG-0005 8, BUG-0006 6
  - `tracker/items/*/questions/Q-*.md` — all 19, read as exchanges: who asked, who was asked,
    the options, the reply and what changed
  - `tracker/items/*/artifacts/*.md` — all 45: every `plan.md`, `impl-report.md`,
    `verify-report.md`, `review.md` and `refinement-qa.md`, plus `EP-001/artifacts/review.md`
  - `docs/product/vision.md` v9, `docs/architecture/overview.md` v11, and ADR-0001…ADR-0014,
    including all 46 change-log rows, each matched against the execution its `by` and `for` name
  - `tracker/project.yaml`, `tracker/board.md`, `tracker/requests/` (empty), `RECORD-NOTICE.md`
  - the installed contracts for `intake`, `refine`, `plan`, `implement`, `verify`,
    `review-close`, `answer-questions` and `next`, and `.claude/skills/retro/SKILL.md` with its
    `references/contract.md`
  - `.claude/agile-skills/spec/` — `journal-and-history.md`, `question.md`, `dor-dod.md`,
    `doc-header.md`, `ids-and-statuses.md`, `work-item.md`, `workspace-layout.md`, `retro.md`,
    and `.claude/agile-skills/VERSION`
  - `.claude/agile-skills/scripts/check-commit-refs`, `validate-workspace`, `lint-retro` and
    `scripts/lib/claims.py` and `record.py`, where a gate's actual behaviour had to be checked
    rather than assumed
  - **Not available:** the product source tree and the commit history, both properties of this
    banked copy [src: RECORD-NOTICE.md]. Recorded under `## What was read` with what it cost.
- **Decisions:**
  - **Every acting skill in the record is a version behind the installed contract**, so a gate
    listed in a contract and absent from an entry was not read as an omission. `intake` 0.2.1
    against 0.3.0 installed, `refine` 0.2.2 / 0.3.0, `plan` 0.3.1 / 0.4.1, `implement` 0.2.2 /
    0.3.0, `verify` 0.1.4 / 0.2.0, `review-close` 0.5.0 / 0.6.0, `answer-questions` 0.3.1 /
    0.4.0. Every gate the record omits relative to its installed contract is one of that kind —
    `cross-answer-consistency` on four skills, `an-open-question-was-asked` on `intake`,
    `a-criterion-about-criteria-is-read` on `verify` — and the difference is treated as unknown,
    per the notice. Only drift **within one version**, across entries of the same skill, is
    reported, which is what P-1 and the third observation are about.
  - **The absent `## Cross-answer check` sections and the absent elicitation question are not
    findings against the engagement.** Both rules are dated 2026-08-29 in the specs' own revision
    tables, the day after this engagement ended. They are recorded as P-10, an `observation`
    proposing no change, so that a triager reading the ledger knows the record predates them.
  - **`workspace-valid` recorded as failed, with the reason, rather than skipped.** All 181
    errors are `claim.citation.unresolved`; 179 name the absent source tree. The two that do not
    — a citation form at `WI-0002/Q-001` line 114 — are reported as an unknown rather than as a
    defect, because `validate-workspace` reported zero errors at every point the record records
    and the resolver has changed since (`claims.py` carries a later fix, F-054, that reads a
    marker's body from the raw line).
  - **The hardest classification call was P-5, the standing delegation.** It could be read as
    this stakeholder's own style — they delegated twice and said so — which would make it a
    `project-circumstance`. It is filed as a `toolkit-defect` because the counterfactual writes
    without naming the subject: the toolkit has no rule bounding how far a category delegation
    reaches and no place in the sign-off for the assumptions taken under it, so *any* engagement
    whose stakeholder delegates once inherits both gaps. What is this project's own is that the
    stakeholder delegated broadly; what is the toolkit's is that nothing bounded it or fed it
    back.
  - **P-8 and P-9 were considered as toolkit-defects and filed as `project-circumstance`.** Both
    counterfactuals need `tidy`'s own subject to state — a clock-relative age boundary a fixture
    cannot pin, and a safety guarantee resting on `os.link`. They are the two entries in this
    report where trying to write the sentence is what decided the class, which is the test
    `spec/retro.md` §7 prescribes.
  - **P-2 was checked against the installed toolkit rather than taken from the record.**
    The engagement filed BUG-0006 and settled it locally with ADR-0013; the question a
    retrospective has to answer is whether the class survives upstream. It does:
    `spec/doc-header.md` §4a still admits a `path:line` citation resolving on file existence
    alone. The mirror case is `check-commit-refs`, where the engagement's own proposal **is** in
    the installed script (F-035) — recorded in the positive record rather than proposed again.
  - **Nothing was fixed, filed or reopened.** Two document defects and one impossible timestamp
    were found in the record; all three are observations or proposals, per this skill's first
    rule.
- **Questions raised:** none — this skill never files a question
- **Commands:**
  - `.claude/agile-skills/scripts/engagement-state EP-001` → exit 0, `EP-001 ended`, rest reached
    2026-08-28T15:41:23Z
  - `.claude/agile-skills/scripts/validate-workspace` → exit 1, 181 errors, 0 warnings, all
    `claim.citation.unresolved`
  - `.claude/agile-skills/scripts/lint-retro EP-001` → exit 1, 2 errors, then exit 0 after both
    were fixed (a mistyped path to `implement`'s SKILL.md, and a quoted example citation the
    resolver read as a real one)
  - `.claude/agile-skills/scripts/lint-retro EP-001 --require-scope` → exit 0, 0 errors
  - `.claude/agile-skills/scripts/check-epic-signoff EP-001` → exit 1, Definition of Done DE8
  - `.claude/agile-skills/scripts/lint-answers --item EP-001` → exit 1, 4
    `answer.cross-check.missing`
  - `grep -h '^| 2026' tracker/items/*/history.md | wc -l` → 88; `grep -c '^## '` over the eleven
    journals → 88
  - `grep -rho '\*\*not yet run\*\*' tracker/items/*/journal.md | wc -l` → 40
  - `grep -rl "Cross-answer check" tracker` → exit 1, no output; `ls -A tracker/requests` →
    `.gitkeep`
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-30T18:48:38Z, the clock the report's `written` field
    carries
- **Gates:**
  - `engagement-has-ended` → **pass** (`scripts/engagement-state EP-001`, exit 0, verdict
    `ended`)
  - `retro-report-is-well-formed` → **pass** (`scripts/lint-retro EP-001`, exit 0, after two
    citation errors were fixed)
  - `scope-was-not-degenerate` → **pass** (`scripts/lint-retro EP-001 --require-scope`, exit 0;
    all eleven items named, counts declared and within the workspace's)
  - `the-record-was-not-touched` → **pass** — this execution wrote exactly two files:
    `tracker/items/EP-001/artifacts/retro.md` and this entry in
    `tracker/items/EP-001/journal.md`. Nothing else in `tracker/` or `docs/` was created,
    edited or deleted.
  - `workspace-valid` → **fail**, and recorded as failed rather than skipped
    (`scripts/validate-workspace`, exit 1, 181 errors). Every one is
    `claim.citation.unresolved` and 179 name a file in the source tree this banked copy does not
    carry; re-running after the report was written gives the same 181 with none of them in
    `retro.md`. `RECORD-NOTICE.md` states this is a property of the copy, not of the engagement,
    and directs that it be recorded this way and the reading continued.
- **Artifacts:**
  - `tracker/items/EP-001/artifacts/retro.md` (new)
- **Status:** `done` → `done` (unchanged)
- **Result:** The engagement's record is read and reported. Eighty-eight executions across eleven
  items, every one with a journal entry and a matching history row and no gap in any chain; ten
  proposals go upstream — seven `toolkit-defect`, two `project-circumstance` and one
  `observation`. The largest is that the sign-off's required "accept with follow-ups" option
  promises an ending the status model forbids, which cost this stakeholder a second sign-off; the
  most repeated is that a skill making two transitions has one gate list and no vocabulary for
  the entry it must write before its gates can run. What held is substantial and is recorded as
  such: verification independent enough to catch two implementation reports in a false claim,
  twelve document defects caught by the one gate no program runs, and four skills that stopped at
  the edge of their authority rather than fixing what they found.
