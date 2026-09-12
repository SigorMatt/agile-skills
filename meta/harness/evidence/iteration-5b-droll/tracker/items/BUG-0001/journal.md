# Journal — BUG-0001

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T22:48:47Z — verify v0.5.1 — qa-engineer

- **Item:** BUG-0001
- **Trigger:** filed by `verify` during the verification of `WI-0001` at status `verifying`; this item did not exist before this execution
- **Inputs read:**
  - `tracker/items/WI-0001/artifacts/plan.md` (the invalidation set whose `## Conventions` row sent this execution to `git ls-files`)
  - `docs/architecture/overview.md` v2, `## Conventions this project has adopted`, third bullet
  - `.claude/agile-skills/spec/workspace-layout.md` §1, for what a workspace root holds
  - `.claude/agile-skills/spec/dor-dod.md` §2, the bug Definition of Ready
  - the repository at `wi/WI-0001` head `5dd1dc3dd79f2cb4cc3a2bc2fb9e011239f8a8c0`, and the file `planned` itself
- **Decisions:**
  - Filed as a bug rather than sent back to `WI-0001`, because no acceptance criterion of `WI-0001` reaches the contents of the repository root — the send-back test in `verify`'s step 7 asks whether one of *this* item's criteria says the behaviour should be different, and none does. `found-in: WI-0001` is answerable and is recorded: the file entered at `6788e55`, that item's `plan` execution.
  - Priority `low`, because nothing depends on the file, `validate-workspace` passes with it present, and droll's behaviour, tests, lint and documents are all independent of it. Filing it at all is the point; ranking it above real work would not be.
  - `AC3` is the regression criterion rather than a case in `tests/`. A `unittest.TestCase` about a stray file would sit in a suite ADR-0002 reserves for the dice roller and would test the toolkit rather than the product; re-running the original command with the argument quoted, and asserting no file appears, fails against the mistake and passes against the fix. RB5's alternative — recording in `## Notes` that a regression test is impossible — would have been the weaker and less true answer.
  - Not repaired here, under `verify`'s prohibition on repairing what it judges. Deleting the file would have taken one command and would have made this execution both the finder and the fixer of the same defect.
  - The bug Definition of Ready (`spec/dor-dod.md` §2) was applied at filing time and passes on all five: **RB1** `## Steps to reproduce` is three numbered commands runnable with no further question; **RB2** `## Actual behaviour` quotes the real output of all three verbatim, including the `exited 2` line and the commit subject; **RB3** `## Expected behaviour` cites `spec/workspace-layout.md` §1's tree and `tracker/project.yaml`'s declared source directories; **RB4** `found-in: WI-0001` names the item whose `plan` execution created the file; **RB5** AC3 is the regression check and `## Notes` records why it is not a case in `tests/`. It is recorded under `**Decisions:**` rather than `**Gates:**` because the gate bullet is read against `verify`'s own contract.
- **Questions raised:** none
- **Commands:**
  - `git ls-files | grep -vE '^(droll|tests|docs|tracker|\.claude)/'` → exit 0, five paths, one of them `planned`
  - `ls -la planned` → exit 0, 3289 bytes
  - `cat -A planned | head -20` → exit 0, `run-gate` output whose first entry records `--resolving WI-0001:ready-` and `exited 2`
  - `git log --oneline --all -- planned` → exit 0, `6788e55 tracker: the plan, the two ADRs and the architecture overview (refs WI-0001)`
  - `python3 .claude/agile-skills/scripts/new-item --next-id bug` → exit 0, `BUG-0001`
  - `python3 .claude/agile-skills/scripts/new-item --id BUG-0001 --type bug … --status ready --actor verify --found-in WI-0001` → exit 0
- **Gates:** this execution's subject is `WI-0001`; the nine verdicts below are that verification's, recorded here because one execution filed this item. The evidence for each is in `tracker/items/WI-0001/artifacts/verify-report.md` `## Gates`.
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, Ran 27 tests, OK)
  - `lint-clean` → **pass** (`python3 -m compileall -q droll tests` → exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0 before this item was created; re-run after, and after `board-gen`)
  - `every-criterion-independently-checked` → **pass** (eleven criteria, each with a command this execution ran and its quoted output)
  - `negative-cases-exercised` → **pass** (AC4's eight inputs, the positive-integer boundary in both directions, blank and whitespace-only lines, empty stdin)
  - `a-criterion-about-criteria-is-read` → **pass** (ran and vacuous: none of AC1-AC11 has criteria as its subject)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 0)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0001` → exit 0)
  - `tests-would-fail-without-the-change` → **pass** (advisory; twelve mutations, each producing a failure)
- **Artifacts:**
  - `tracker/items/BUG-0001/item.md` (new)
  - `tracker/items/BUG-0001/history.md`, `tracker/items/BUG-0001/journal.md` (new)
  - the `## Defects found` section of `tracker/items/WI-0001/artifacts/verify-report.md`, which names this bug
- **Status:** `—` → `ready`
- **Result:** A stray 3289-byte file of captured `run-gate` output, tracked at the repository root since `WI-0001`'s `plan` execution, is filed as a bug at `ready` with reproduction, real output and `found-in`. droll is unaffected; `WI-0001` is not sent back.

## 2026-09-11T23:18:10Z — plan v0.6.3 — architect

- **Item:** BUG-0001
- **Trigger:** status `ready`, dispatched by `next` — the only runnable item on the pass, `WI-0002`
  having suspended on a stakeholder question earlier in the same turn.
- **Inputs read:**
  - `tracker/items/BUG-0001/item.md` — the summary, the three reproduction steps with their
    verbatim output, the three criteria, and the three `## Notes` paragraphs
  - `tracker/items/BUG-0001/history.md` — one row, `— → ready` filed by `verify`. This is a first
    plan, not a re-plan: no review or verification sent it back
  - no `artifacts/refinement-qa.md` exists, and none should: a bug filed with reproduction steps
    satisfies the bug Definition of Ready at creation, so `refine` never ran on it
  - `docs/architecture/overview.md` v3 — `## Shape` and `## Components`, to confirm this change
    alters neither
  - all four ADRs: `ADR-0001` (grammar), `ADR-0002` (standard library only, and the two gate
    commands), `ADR-0003` (rejection messages on stdout), `ADR-0004` v3 (the bounded overrides,
    and point 4a on what `--plan-documents` widens)
  - `docs/` read rather than recalled, for the invalidation set: all six documents, plus
    `grep -rn 'ls-files|repository root|planned' docs/`, which returns exactly one line
  - `tracker/project.yaml` — `trunk-branch: main`, `commands.test`, `commands.lint`,
    `conventions.commit-subject`
  - the repository itself: `git ls-files` filtered to the root, `ls -la planned`, `.gitignore`,
    and `git log --oneline --all -- planned`
  - no droll source file was read beyond confirming from `git diff --name-only` that this change
    touches none. A plan that changes no code has no code to be written from
- **Decisions:**
  - **D1 — the regression check is `AC3`, not a `unittest` case.** Preference order **branch 1**,
    answered from documents: `ADR-0002` scopes `tests/` to `unittest.TestCase` classes about the
    dice roller, and a test asserting a file's absence at the repository root is not about the
    dice roller. Rationale: putting a claim about the repository inside droll's suite leaves the
    next reader with no way to tell why it is there, and the item already supplies a regression
    check that fails against the original mistake and passes against the fix.
  - **D2 — this plan names no document, and the invalidation set is `none`.** Preference order
    **branch 1**, answered from `ADR-0004` point 4a. Rationale, and this is the decision worth
    reading: `--plan-documents` widens `implement`'s `claims-are-sourced` window to every
    document the plan names, whatever the change did to it. `docs/product/vision.md` carries an
    unsourced absolute inside a `## Engagement state` section that no skill may repair before
    the ending. Naming it here as a precaution would drag that sentence into this item's gate
    window and buy a one-line deletion a forced hard gate and a third override decision — and
    `ADR-0004` says in terms that a later item of that shape gets its own decision rather than
    inheriting one. It is not named because it is not at risk: deleting a stray file cannot make
    a sentence about the engagement true or false. The alternative was weighed and refused, which
    is why it is recorded as a decision rather than left as a blank.
  - **No ADR was written.** Rationale: neither decision introduces a commitment a later `plan`
    execution would have to read in order to know whether it may revisit something — D1 applies
    an existing ADR and D2 applies another. An ADR trail padded with non-decisions is one the
    real decisions hide in.
  - **Two reversible assumptions recorded instead of asked.** Preference order **branch 2**.
    A1, that nothing reads the file, reverses with one `git revert` that restores it byte for
    byte because the deletion does not rewrite history. A2, the `repo:` commit scope word,
    reverses at no cost because no gate reads the scope, only that the subject names the item.
    Neither was taken under a stakeholder delegation and neither needed one: both are readings
    of the repository, not of anyone's intent.
  - **Named all four ADRs under `## Binding ADRs`, two as binding and two as not-engaged.**
    Rationale: the project has exactly four, `not-engaged` is one of the three verdicts `verify`
    may record, and D13 asks `review-close` whether the list is complete — which is answerable by
    reading the list against the index rather than by re-deriving it. `review-close` on `WI-0001`
    recorded the opposite case as a finding, an ADR engaged and unlisted, so the cost of naming
    is visibly lower than the cost of omitting.
  - **Wrote `AC1`'s two-stage demonstration into the mapping rather than leaving it.** Rationale:
    `AC1` says "on the trunk" and `verify` runs before the merge. That is the one place this plan
    could be executed correctly and still produce an argument, so the mapping row names which
    observation settles it at each stage — branch head, then `review-close`'s detached trial
    merge, then `main` after the merge — and `## Risks` says that if `verify` judges the first
    insufficient, the honest move is a question to the architect and not a loosened criterion.
    Deferring this would be the classic failure: the one hard choice left as "handle it
    appropriately".
  - **No plan step instructs a downstream skill to do something its contract forbids.** Checked
    step by step: steps 1-4 are all `implement`'s and all within it. No step ticks a criterion —
    that is `verify`'s. No step writes a document — `## Deliverable documents` is `none`, so
    `implement` is permitted to write none. No step touches an engagement-state sentence or ends
    anything.
- **Cross-answer check:** `none` — this execution recorded and relied on no human answer. The
  engagement's four (`EP-001/Q-001`, `Q-002`, `Q-003`, `WI-0001/Q-001`) are about what a session
  is, how far the expression grammar reaches, the audience, and what a roll line shows; this item
  deletes a file from the repository root and engages none of them. `lint-answers --uncommitted`
  → exit 0.
- **Questions raised:** none. Nothing here was irreversible or depended on intent no document
  records, so branch 3 of the preference order was not reached. `WI-0002/Q-001` is open with the
  stakeholder but belongs to another item and is not waiting on anything here.
- **Commands:**
  - `git ls-files | grep -vE '^(droll|tests|docs|tracker|\.claude)/'` → 5 paths, `planned` among
    them
  - `ls -la planned` → 3289 bytes
  - `git log --oneline --all -- planned` → one line, `6788e55`
  - `cat .gitignore` → 7 patterns, none matching `planned`
  - `grep -rn 'ls-files|repository root|planned' docs/` → one line,
    `ADR-0002:72`, about where test discovery starts
  - `find docs -name '*.md'` → 6 paths, all read
  - `python3 .claude/agile-skills/scripts/run-gate --skill plan --item WI-0001 --all --resolving
    'WI-0001:ready->planned'` → exit 0, verdicts on the terminal, `git status --short` empty
    afterwards. Run deliberately: it is the command `AC3` names, and running it quoted proves the
    criterion is demonstrable before the plan asks anyone to demonstrate it
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated
    --item BUG-0001` → exit 0, *"0 invalidation row(s), 0 deliverable document(s), 4 binding
    ADR(s)"*
  - `python3 .claude/agile-skills/scripts/run-gate --skill plan --item BUG-0001 --all --resolving
    'BUG-0001:ready->planned'` → exit 0, no hard gate failed, 4 manual
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace --resolving 'BUG-0001:ready->planned'` exited 0)
  - `every-criterion-is-addressed` → **pass** (reported `MANUAL`; the evidence is `plan.md` `## Acceptance criteria mapping`, three rows for three criteria. AC1 → step 2, the two commands plus the named two-stage reading of "on the trunk"; AC2 → step 2, `git log --grep BUG-0001` and `git log --oneline --all -- planned` returning `6788e55` among two lines; AC3 → step 3, the quoted command with `git status --short` and `ls planned` after it. No criterion is demonstrated by "tests" — this change produces no test signal at all, which `## Risks` says in terms)
  - `project-commands-resolved` → **pass** (reported `MANUAL`. `tracker/project.yaml` already carries `test: python3 -m unittest discover -s tests -t .` and `lint: python3 -m compileall -q droll tests`, both fixed by `ADR-0002` and both run by this execution's predecessor on this trunk — 27 tests, exit 0, and compileall exit 0 at the `WI-0001` close. Neither is a command that exits zero without checking anything. `build` is `null`, which is honest: the project has no build step. Nothing needed filling in)
  - `decisions-recorded` → **pass** (reported `MANUAL`. Two decisions, D1 and D2, each in `## Decisions and ADRs` with the document it was answered from and the alternative it refused; two assumptions, A1 and A2, each in `## Assumptions` with what reversing it costs. No ADR was written and the section says why)
  - `plan-is-executable-without-you` → **pass** (advisory. Read back cold: step 1 names the branch and the base, step 2 names the command, the path and the commit subject convention, step 3 quotes the command in full including the single quotes that are the fix, step 4 names both declared commands and the diff check. The one place a reader would otherwise have to decide something — what "on the trunk" means for `verify` — is decided in the mapping row and flagged in `## Risks`)
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule documents-at-risk-are-enumerated --item BUG-0001` exited 0, reading *"0 invalidation row(s), 0 deliverable document(s), 4 binding ADR(s)"*. The set is a `none` row with its justification written from a read of all six documents in `docs/` and a grep that returns one unaffected line, not from recollection)
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` exited 0. Nothing this execution wrote records or relies on a human answer, and nothing of theirs was edited)
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` exited 0. The two absolute claims this plan makes both carry sources: the AC3 demonstrability claim cites the run that produced it, and D2's account of what `--plan-documents` widens cites `ADR-0004`)
- **Artifacts:**
  - `tracker/items/BUG-0001/artifacts/plan.md` (new)
  - no ADR was created; no document under `docs/` was written or versioned; `tracker/project.yaml`
    needed no change
- **Status:** `ready` → `planned`
- **Result:** BUG-0001 is planned as four steps and one deletion. No droll source, test or
  document is touched, no ADR was needed, and the invalidation set is `none` — deliberately, since
  naming `docs/product/vision.md` defensively would have dragged an engagement-state sentence
  nobody may repair into this item's gate window. The one genuine wrinkle, that `AC1` says "on the
  trunk" while `verify` runs before the merge, is decided in the mapping rather than left for
  `implement` to guess at.
