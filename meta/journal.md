# Builder journal (append-only)

One entry per work unit. Format mirrors the methodology's own journal schema in
`spec/journal-and-history.md` — deliberately, so this file is also evidence of what the
pipeline's paper trail should feel like.

---

## 2026-08-16 — META-001 — build scaffolding

- **Unit:** META-001
- **Inputs read:** `PROMPT.md`, `seed/00-VISION.md`, `seed/01-REQUIREMENTS.md`,
  `seed/02-ARCHITECTURE.md`, `seed/03-ACCEPTANCE.md`, `CLAUDE.md`.
- **Decisions:**
  - Fresh run, not a restart: `meta/` did not exist and the directory was not a git repo.
  - Default branch renamed `master` → `main` (convention; the methodology's item branches will
    be `wi/<ID>`, so the trunk name needs to be stable and conventional).
  - The build plan is decomposed into ~40 units of one commit each, sized so that losing a
    session costs at most one unit (PROMPT rule 9).
  - Toolchain probe: `python3` 3.12.3, `node` v18, `uv`, `jq` present. Language choice for
    `scripts/` is deferred to META-003 so it can be recorded as an ADR rather than a habit.
- **Commands run:** `git init` (ok), `git branch -m main` (ok), toolchain probe (ok).
- **Gates:** n/a (no gate scripts exist yet).
- **Artifacts produced:** `meta/plan.md`, `meta/CHECKPOINT.md`, `meta/journal.md`,
  `meta/BLOCKERS.md`, `.gitignore`.
- **Result:** META-001 done. Next: META-002.

---

## 2026-08-16 — META-002 — verified Claude Code skill format

- **Unit:** META-002
- **Inputs read:** `https://code.claude.com/docs/en/{claude_code_docs_map,skills,hooks,permission-modes}.md`
  (the `docs.anthropic.com` URL in PROMPT.md 301-redirects to `code.claude.com`).
- **Decisions (all recorded in ADR-0001):**
  - Install at **project** level `.claude/skills/<name>/`, not personal.
  - Renderer emits only the six Agent-Skills-spec-legal frontmatter fields by default, so
    rendered skills stay portable; Claude-Code-only fields are opt-in per skill and recorded in
    the dist manifest.
  - `AskUserQuestion` is the confirmed human-question mechanism; `disallowed-tools:
    AskUserQuestion` is the **hard** enforcement of R2's "implement/verify never ask the human".
  - Gate hardness comes from `PreToolUse` hooks (exit 2, or `permissionDecision: deny` with exit
    0). `PostToolUse` cannot block — so no gate may be designed to rely on it.
- **Explicitly not confirmed:** whether a skill invocation itself is a gateable tool call. The
  adapter therefore gates observable side effects (transition script, `git commit`) instead of
  assuming it. Written into ADR-0001 "What could NOT be confirmed" so the adapter cannot silently
  drift into assuming it later.
- **Gates:** n/a.
- **Artifacts produced:** `meta/adr/ADR-0001-claude-code-skill-format.md`.
- **Result:** META-002 done. Next: META-003.

---

## 2026-08-16 — META-003 — scripting policy + YAML subset reader

- **Unit:** META-003
- **Inputs read:** `seed/01-REQUIREMENTS.md` R3 (validation script runs in the consumer's
  project), `meta/adr/ADR-0001` (rendered frontmatter must round-trip).
- **Decisions:** ADR-0002 — Python 3.9+, stdlib only, everywhere. No `requirements.txt` exists
  and none may be added. YAML is read by `scripts/lib/miniyaml.py`, a reader for a documented
  subset that raises `YamlError` with a line number on anything outside it rather than guessing.
  Rationale: a gate that fails because a package is missing is indistinguishable, to the agent
  running it, from a gate that fails because the work is wrong.
- **Commands run:** `python3 scripts/lib/selftest.py` → `93 passed, 0 failed`, cross-check
  `ran against PyYAML 6.0.1 on 31 inputs`.
- **Discoveries during verification (both were real divergences, both fixed in the reader/tests):**
  - `2e3`: the first implementation coerced it to a float; PyYAML (YAML 1.1) leaves it a string.
    `_FLOAT_RE` now requires a dot, so the two readers agree. Caught only by the cross-check —
    which justifies keeping that layer.
  - `dump_frontmatter("0.1.0")` needs no quotes and round-trips as a string; the test's
    expectation was wrong, not the emitter.
- **Gates:** `scripts/lib/selftest.py` exit 0.
- **Artifacts produced:** `meta/adr/ADR-0002-scripting-and-dependencies.md`,
  `scripts/lib/miniyaml.py`, `scripts/lib/selftest.py`.
- **Result:** META-003 done. Next: META-030.

---

## 2026-08-16 — META-030 — frontmatter and findings helpers

- **Unit:** META-030
- **Inputs read:** `seed/02-ARCHITECTURE.md` §3 (every artifact is markdown + YAML frontmatter),
  `meta/adr/ADR-0002`.
- **Decisions:**
  - A missing frontmatter fence is an **error**, not an empty mapping. An unlabelled file that
    validated clean would be the easiest way for the paper trail to silently rot.
  - YAML errors inside a frontmatter block are re-raised with the line number shifted to the
    position in the whole file, so a finding points at the line a human would open.
  - `Report` sorts findings before printing and strips the repo root from paths. Both exist for
    one reason: byte-identical output across runs and machines, which is what lets
    `scripts/check` compare a fresh render against the committed one.
- **Commands run:** `python3 scripts/lib/selftest.py` → `110 passed, 0 failed`.
- **Discovery:** the first `render()` swallowed the blank line after the closing fence, so
  `render(split(x)) != x`. Fixed by defining the body as "everything after the closing fence
  *line*" and emitting that newline in `render`. Caught by the round-trip case, which is the
  reason to write inverse-pair tests rather than one-direction ones.
- **Gates:** `scripts/lib/selftest.py` exit 0.
- **Artifacts produced:** `scripts/lib/frontmatter.py`, `scripts/lib/report.py`, 17 new cases in
  `scripts/lib/selftest.py`.
- **Result:** META-030 done. Next: META-010 (spec index + IDs and statuses).

---

## 2026-08-16 — META-010 — spec index, IDs, item types, status graph

- **Unit:** META-010
- **Inputs read:** `seed/01-REQUIREMENTS.md` R3/R4, `seed/02-ARCHITECTURE.md` §3.
- **Decisions (ADR-0003):**
  - Epics, work items and bugs share one directory shape under `tracker/items/<ID>/`. One glob
    enumerates the tracker; the alternative (three sibling trees) would have made every
    traversal in three separate scripts re-learn where trackable things live.
  - The next ID is derived by scanning the filesystem, not stored in a counter file. A counter
    is a second source of truth that goes wrong exactly when this project expects to be
    interrupted — between incrementing and creating.
  - `awaiting-answer` stores the status it suspended in its history entry rather than letting
    `answer-questions` infer it. Inference silently discards completed verification when the
    question came from `review-close`.
- **Judgement calls recorded in the spec itself:**
  - `planned` vs `in-progress` are kept distinct because they differ in *recovery* behaviour
    (no branch yet vs. partial work on a branch), not for bureaucracy.
  - Bugs enter at `ready`, not `draft`: a bug filed with reproduction steps already satisfies
    the bug Definition of Ready, so routing it through `refine` would be theatre.
  - Epics are never dispatched directly by the orchestrator; `review-close` closes an epic as
    the final act of closing its last child, the one moment sibling state is already in hand.
- **Gates:** none executable yet — `scripts/validate-workspace` (META-032) is what will enforce
  this page, and it is written against it.
- **Artifacts produced:** `spec/README.md`, `spec/ids-and-statuses.md`,
  `meta/adr/ADR-0003-tracker-layout-and-id-allocation.md`.
- **Result:** META-010 done. Next: META-011.

---

## 2026-08-16 — META-011 — `spec/work-item.md`

- **Unit:** META-011
- **Inputs read:** `spec/ids-and-statuses.md`, `seed/02-ARCHITECTURE.md` §3.
- **Decisions:**
  - `item.md` is identity, never log. What happened lives in `journal.md`/`history.md`. Stated
    explicitly because the natural drift is for an item body to grow a running commentary, and
    then two places disagree about what happened.
  - Unknown frontmatter fields are an **error**, not a warning: a typo'd `piority:` that passed
    validation would leave the board silently wrong, which is worse than a noisy failure.
  - Acceptance criteria are checkbox lists labelled `AC<n>`; `verify` ticks a box only with
    cited evidence and `review-close` may not close an item with an unticked box. This turns
    "definition of done" into something a script can count rather than something an agent can
    feel.
  - Criteria are frozen after `ready` except via `answer-questions` or an explicit send-back.
    Quietly loosening a criterion to make verification pass is the most damaging failure mode
    available to this design, so the spec names it rather than trusting taste.
  - An epic MUST NOT hand-maintain a child list; children are derived from `epic:` fields.
    A second list would drift within one work item.
  - Relations are three explicit list fields (`depends-on`, `blocks`, `relates-to`) instead of
    one free-form `links` field, so each has a checkable meaning and dangling references are an
    error.
- **Gates:** none yet; `scripts/validate-workspace` (META-032) is written against this page.
- **Artifacts produced:** `spec/work-item.md`.
- **Result:** META-011 done. Next: META-012.

---

## 2026-08-16 — META-012 — `spec/journal-and-history.md`

- **Unit:** META-012
- **Inputs read:** `seed/01-REQUIREMENTS.md` R4, `spec/ids-and-statuses.md` §4.
- **Decisions:**
  - Two files, not one: `history.md` is a six-column table (the timeline a manager scans),
    `journal.md` is prose-with-required-labels (the detail a reviewer reads when a line in that
    timeline looks wrong). Merging them would force every reader to pay for the detail.
  - `history.md` gets a `resume-to` column so `awaiting-answer`/`blocked` carry their return
    status in the timeline itself (ADR-0003), rather than only inside a question artifact.
  - `actor` is a **skill name**, never a person or a model. It is what localises a fault to a
    contract when a run goes wrong, which is the debugging loop the vision asks for.
  - A gate declared in a contract MUST appear in the journal even when skipped, with the reason.
    The failure this format exists to prevent is an execution reporting success while silently
    never running a check.
  - `**Decisions:**` must carry rationale, not just the choice — an auditor needs to judge
    whether the reasoning was sound, not only what happened.
  - Chaining rule (`row n.from == row n-1.to`, last row's `to` == `item.md` status) makes a
    hand-edited status mechanically detectable as `history.gap`.
- **Gates:** none yet; `scripts/validate-workspace` implements §1's validation rules.
- **Artifacts produced:** `spec/journal-and-history.md`.
- **Result:** META-012 done. Next: META-013.

---

## 2026-08-16 — META-013 — `spec/question.md`

- **Unit:** META-013
- **Inputs read:** `seed/01-REQUIREMENTS.md` R2/R4, `seed/02-ARCHITECTURE.md` §5.
- **Decisions:**
  - `## Options considered` requires two options **or** an explicit statement that the question
    is not a choice. Without that rule the protocol degrades into "ask the architect everything"
    and the cost of thinking is just pushed upstream.
  - `## Consequences` must name files, not intentions. That is what makes "downstream skills
    re-read artifacts, never the Q&A" enforceable rather than aspirational.
  - Non-blocking questions exist and do **not** suspend the item — needed for "this should be
    written down" without stalling delivery.
  - Escalation to the human is restricted to four named conditions (intent not recorded,
    irreversible, contradicts an ADR, record genuinely silent), and the escalating question must
    say which applies. The human's attention is the scarcest resource in the loop.
  - Recorded the real reason `implement`/`verify` may never ask directly: a chat answer leaves
    no artifact, so the *next* execution — after a restart or on a sibling item — cannot see it
    and will re-ask or guess differently.
- **Gates:** none yet.
- **Artifacts produced:** `spec/question.md`.
- **Result:** META-013 done. Next: META-014.

---

## 2026-08-16 — META-014 — `spec/doc-header.md`

- **Unit:** META-014
- **Inputs read:** `seed/01-REQUIREMENTS.md` R3, `seed/02-ARCHITECTURE.md` §3, `spec/question.md`.
- **Decisions:**
  - The header exists even though git stores diffs, because an agent reading a doc mid-run must
    know how current it is *from the document*, without shelling out to git and without the
    answer depending on whether the workspace is a git repo yet.
  - "Fixing a typo is a content change" — no exceptions. The judgement "is this worth a row?" is
    precisely what erodes a change log into uselessness.
  - An ADR must list two options or say the decision was forced; otherwise it records a
    conclusion, and a later reader cannot tell whether alternatives were considered or missed.
  - `## Consequences` must state reversibility, because `plan`'s escalation rule
    (`question.md` §1) turns on that property — leaving it implicit would break a decision
    procedure elsewhere in the methodology.
  - `implement` and `verify` may not write to `docs/`. Otherwise the authoritative record would
    be edited by the very execution trying to satisfy it, and the check becomes circular.
  - Empty placeholder documents are forbidden: an empty doc reads as an answer.
- **Gates:** none yet.
- **Artifacts produced:** `spec/doc-header.md`.
- **Result:** META-014 done. Next: META-015.

---

## 2026-08-16 — META-015 — `spec/dor-dod.md`

- **Unit:** META-015
- **Inputs read:** `seed/01-REQUIREMENTS.md` R2 (override is journaled), `spec/work-item.md`.
- **Decisions:**
  - Every criterion is tagged **[auto]** (a script decides it) or **[skill]** (the skill decides
    and must record evidence). Without the tag, "executable gates over vibes" collapses into a
    checklist an agent can wave at.
  - Results are recorded criterion by criterion. A bare "DoR passed" hides which criterion was
    the weak one, which is exactly what a reviewer needs.
  - The DoR override is designed to be *loud*: named unmet criteria in `refinement-qa.md`, a
    history reason that must start with `DoR overridden:`, and the risk copied into the item's
    `## Notes` so `plan` and `implement` inherit it visibly. Overriding is legitimate; doing it
    quietly is not.
  - D10 ("verify ran after the last code change") is machine-checkable by comparing the verify
    report timestamp to the last commit on the branch, and `review-close` must actually compare
    rather than assume. D3 and D10 are called out as the two that get skipped, with the shared
    failure mode named: something is re-touched after the check and the check is not re-run.
  - DE3 stops the pipeline mistaking "all tickets closed" for "goal achieved": an unmet success
    measure may still close the epic, but saying so is mandatory.
- **Gates:** none yet.
- **Artifacts produced:** `spec/dor-dod.md`.
- **Result:** META-015 done. Next: META-016 (skill contract — the schema `lint-skills` enforces).

---

## 2026-08-16 — META-016 — `spec/skill-contract.md`

- **Unit:** META-016
- **Inputs read:** `seed/02-ARCHITECTURE.md` §2/§6, `seed/00-VISION.md` principle 4,
  `spec/ids-and-statuses.md`.
- **Decisions:**
  - `dispatch.on_status` is a **list of statuses**, replacing the seed's example expression
    `item.status == "planned"`. An expression language would need an evaluator in every adapter
    and would let engineering judgement leak into the scheduler, which VISION principle 4
    forbids. `lint-skills` cross-checks the list against `pipeline.yaml` in both directions: an
    unclaimed status is a stall, a doubly-claimed status is a race.
  - A gate has exactly one of `command` or `manual_check`. Allowing both invites reporting the
    manual check when the command fails.
  - `enforcement: hard|advisory` is declared in the methodology, but *which* gates a runtime
    actually blocks on is documented per adapter — the methodology cannot honestly claim
    enforcement it does not implement (R5).
  - Placeholders are `{{...}}`, resolved by the adapter. `{{commands.test}}` resolving to null
    makes the gate **skipped**, never passed; unknown placeholders are a lint error so a typo
    cannot degrade into an empty string that makes a gate trivially pass.
  - Introduced `tracker/project.yaml` as the machine-readable home for project commands and the
    trunk branch name, and made `plan` responsible for filling it (or writing an ADR saying the
    project has no such command). Gates otherwise have no honest way to name a test command
    that is unknown when the methodology is written.
  - `process.md` must transition **after** journaling: an interruption then costs a repeated run
    rather than a status that advanced with no record.
  - `## Self-check` must name ≥2 specific failure modes for that role. It is where lessons from
    a bad run are recorded, so the iterate-and-deepen loop has somewhere to land.
- **Gates:** none yet; `scripts/lint-skills` (META-031) implements this page.
- **Artifacts produced:** `spec/skill-contract.md`.
- **Result:** META-016 done. Next: META-017 (`spec/workspace-layout.md`, incl. `project.yaml`).

---

## 2026-08-16 — META-017 — `spec/workspace-layout.md`

- **Unit:** META-017
- **Inputs read:** `seed/01-REQUIREMENTS.md` R3/R4, `spec/skill-contract.md` §1.4.
- **Decisions:**
  - The workspace lives inside the consumer's repository, committed with the code. A tracker in
    a separate system drifts within a week, and `git log --grep WI-0007` only reconstructs an
    item's history if item and code share one history.
  - Artifact filenames are **fixed** (`plan.md`, `impl-report.md`, …), not free choice: a skill
    must find the previous stage's output without searching, and the validator must be able to
    say "reached verifying with no impl-report.md".
  - Re-running a skill overwrites its own artifact and appends a journal entry — never
    `plan-2.md`. The journal holds the history of attempts; the artifact holds the current
    answer.
  - `journal.md`/`history.md` are created with headers at item creation, so "empty" and "lost"
    are distinguishable.
  - `board.md` is generated and `validate-workspace` reports `board.stale` by regenerating and
    comparing — a board that disagrees with the tracker gets caught rather than believed.
  - Open questions appear on the board *above* the summary, human-addressed first: when the
    loop stops, that is the first thing a returning human reads.
  - `tracker/project.yaml` gained `conventions.commit-subject`, which must contain `<ITEM-ID>` —
    that is what makes DoD D8 mechanically checkable rather than a habit.
- **Gates:** none yet; `scripts/validate-workspace` and `scripts/workspace-init` implement this.
- **Artifacts produced:** `spec/workspace-layout.md`.
- **Result:** META-017 done. Phase 1 (`spec/`) complete. Next: META-020 (`pipeline.yaml`).

---

## 2026-08-16 — META-020 — `methodology/pipeline.yaml`

- **Unit:** META-020
- **Inputs read:** `spec/ids-and-statuses.md`, `spec/skill-contract.md` §1.2,
  `seed/02-ARCHITECTURE.md` §4.
- **Decisions:**
  - `pipeline.yaml` is the orchestrator's *entire* world model — statuses with owners,
    transitions, priority ranks, and the five-step algorithm. Everything an adapter or `next`
    needs is data here rather than logic there.
  - Transitions that apply from many states are expressed with the pseudo-states
    `any-non-terminal` and `resume-to` rather than being enumerated per source status. Fifty
    rows of enumeration would have to be regenerated whenever a status is added, and the
    generated rows would be the first thing to drift from the prose spec.
  - Added a `skills:` registry so `lint-skills` can check the pipeline and
    `methodology/skills/*/` agree in both directions — a skill directory nobody dispatches is as
    much a defect as a dispatch target with no skill.
  - `orchestrator.runnable` and `orchestrator.selection_key` are data, so determinism is a
    property of the file rather than of an implementation's habits.
  - Corrected `spec/ids-and-statuses.md` §3.2 in the same unit: epics can hold a blocking
    question about their own scope, so `awaiting-answer` applies to epics too. Found by writing
    the machine-readable form of the prose — which is the reason to keep both.
- **Commands run:** parsed `pipeline.yaml` with `miniyaml` (10 statuses, 16 transitions);
  `python3 scripts/lib/selftest.py` → `111 passed, 0 failed`, cross-checked against PyYAML on
  32 inputs (the new file is now one of them).
- **Gates:** miniyaml/PyYAML agreement on `pipeline.yaml`.
- **Artifacts produced:** `methodology/pipeline.yaml`; edit to `spec/ids-and-statuses.md`.
- **Result:** META-020 done. Next: META-021 (`intake`).

---

## 2026-08-16 — META-021 — skill `intake`

- **Unit:** META-021
- **Inputs read:** `spec/skill-contract.md`, `spec/work-item.md` §4, `spec/dor-dod.md`,
  `methodology/pipeline.yaml`.
- **Decisions:**
  - `dispatch.on_status: []` — `intake` is human-started, never scheduled. It creates items *at*
    `draft` rather than transitioning anything, so `next_status: draft`, `failure_status: null`.
  - The gate `no-solution-in-the-problem` exists because the characteristic analyst failure is
    designing while framing. It is advisory (it is a judgement) but it must be recorded.
  - Intake writes acceptance criteria it can already state and is told **not to pad them**. An
    honestly rough criterion is better than a polished unfalsifiable one, and `refine` exists to
    finish them.
  - Human answers are recorded verbatim in the epic journal, because that journal is the only
    record of the conversation and `refine`/`plan` depend on it.
  - `commands.*` in `project.yaml` stay `null` at intake. Inventing a test command would make
    the first gate report a pass for something nobody can run.
  - The two named self-check failure modes are over-splitting (each extra item costs a full
    pipeline round trip and a paper trail nobody reads) and criteria that sound testable but are
    not, with a concrete test for the latter.
- **Commands run:** `python3 scripts/lib/selftest.py` → `112 passed, 0 failed` (the new
  `skill.yaml` is now in the PyYAML cross-check set).
- **Gates:** miniyaml/PyYAML agreement on `intake/skill.yaml`.
- **Artifacts produced:** `methodology/skills/intake/{skill.yaml,process.md}`.
- **Result:** META-021 done. Next: META-022 (`refine`).

---

## 2026-08-16 — META-022 — skill `refine`

- **Unit:** META-022
- **Inputs read:** `spec/dor-dod.md`, `spec/work-item.md`, `spec/question.md` §1,
  `methodology/pipeline.yaml`.
- **Decisions:**
  - "Challenge once, then record as assumed." A human badgered into a number they do not believe
    has given a truce, not a requirement — and the truce is indistinguishable from agreement in
    the record, which is worse than an honest `[assumed]` tag.
  - `refinement-qa.md` answers are tagged `[human]` / `[assumed]` / `[unresolved]`, and verbatim
    means verbatim. When `verify` later finds a behaviour contested, a tidied Q&A is worth
    nothing as evidence.
  - `refine` reads `history.md` **before** the item body, because an item sent back from
    `verifying`/`in-review` is a different job from a fresh draft; the process says so
    explicitly and names re-refining a send-back as one of the two failure modes.
  - The `definition-of-ready` gate explicitly rejects a single overall verdict — it demands a
    per-criterion record, which is what makes the checklist more than decoration.
  - `refine` may not edit architecture docs; a vision conflict becomes a question to the
    architect. Keeps the "who may write which doc" table in `spec/doc-header.md` §5 true.
  - Named the concrete tell for the first failure mode: an adjective with no threshold
    ("appropriate", "reasonable", "clean", "properly") marks where the disagreement will happen.
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures, cross-check includes
  `refine/skill.yaml`.
- **Gates:** miniyaml/PyYAML agreement.
- **Artifacts produced:** `methodology/skills/refine/{skill.yaml,process.md}`.
- **Result:** META-022 done. Next: META-023 (`plan`).

---

## 2026-08-16 — META-023 — skill `plan`

- **Unit:** META-023
- **Inputs read:** `spec/question.md` §1 (the preference order), `spec/doc-header.md` §4,
  `spec/skill-contract.md` §1.4, `spec/dor-dod.md`.
- **Decisions:**
  - `human_interaction: direct`, but constrained by the fixed preference order (cite a document
    → make a reversible assumption → ask). The process names the failure in *both* directions:
    skipping the middle option upward turns the human into a design service; skipping it
    downward buries a real commitment in a plan step where nobody sees it was a choice.
  - `plan` owns `tracker/project.yaml`'s `commands.*`. Choosing a test framework *is* a design
    decision, so it belongs to the architect; and a null command must become an honest `skipped`
    gate plus an ADR, never a passing gate for a check nobody runs.
  - The AC-to-step mapping table is a hard gate. It also gives the "designing past the item"
    failure a mechanical check: delete any step no AC maps to, and if the table still holds, the
    step did not belong to this item.
  - ADRs must state reversibility, because the preference order in step 4 turns on it — a future
    `plan` reads that field to decide whether it may revisit the decision.
  - Explicitly forbade padding the ADR trail with non-decisions: the real decisions hide in it.
  - Named the second failure mode as deferring the one genuinely hard choice behind "handle the
    edge cases appropriately", with the tell — the step that makes you uncomfortable is the one
    that needs the ADR.
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** miniyaml/PyYAML agreement on `plan/skill.yaml`.
- **Artifacts produced:** `methodology/skills/plan/{skill.yaml,process.md}`.
- **Result:** META-023 done. Next: META-024 (`implement`).

---

## 2026-08-16 — META-024 — skill `implement`

- **Unit:** META-024
- **Inputs read:** `spec/question.md`, `spec/workspace-layout.md` §5, `spec/dor-dod.md` D3/D8/D10,
  `methodology/skills/plan/process.md`.
- **Decisions:**
  - The "never ask the human" rule is justified structurally in the process text, not asserted:
    a conversational answer leaves no artifact, so the *next* execution cannot see it and will
    guess differently. Stopping is named as the correct outcome.
  - Answers are read from the artifacts the answer updated, never from the question file. If the
    artifacts were not updated, that is itself a question — which keeps
    `spec/question.md` rule 5 enforceable.
  - The item moves to `in-progress` **before** any code is written, so an interruption leaves a
    truthful status and the resume path (reconcile with the branch) is unambiguous.
  - Added the `commits-reference-the-item` gate backed by a real command,
    `scripts/check-commit-refs`, so DoD D8 is machine-checked rather than remembered. Added
    META-036 to the plan to build it.
  - Gave the "is this decision mine?" question a mechanical test — changes an interface another
    item depends on, contradicts an ADR, decides user-visible behaviour no AC covers, or is
    expensive to reverse — so it does not depend on how confident the agent feels.
  - Named the second failure mode as opportunistic fixing: individually worth doing, collectively
    fatal, because the diff stops matching the criteria and the unrelated fix ships with no
    criterion and no verification.
  - `## What I did not do` is a required section of the implementation report: a declared
    omission is a handover, an undeclared one is a defect in the report.
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** miniyaml/PyYAML agreement on `implement/skill.yaml`.
- **Artifacts produced:** `methodology/skills/implement/{skill.yaml,process.md}`; new plan unit
  META-036.
- **Result:** META-024 done. Next: META-025 (`verify`).

---

## 2026-08-16 — META-025 — skill `verify`

- **Unit:** META-025
- **Inputs read:** `spec/dor-dod.md` §3, `spec/work-item.md` §3, `spec/question.md`,
  `methodology/skills/implement/process.md`.
- **Decisions:**
  - Citing `impl-report.md` as evidence **fails** the central gate. Independence is the reason
    this skill exists; accepting the report converts an independent check into a second opinion
    about the same claim.
  - The process orders reading deliberately: criteria before the implementation report. Reading
    the report first anchors the verifier to checking that the code does what it does.
  - Added `tests-would-fail-without-the-change` — revert the behaviour and watch the test fail.
    A test that passes against an absent implementation makes a criterion look covered forever.
  - Gave the send-back vs. bug classification a decisive test: does an acceptance criterion of
    *this* item say the behaviour should differ? Yes → send-back; no → bug. Misrouting either way
    puts the work in the wrong place.
  - `## Not verified, and why` is a mandatory report section — an undeclared gap reads to
    `review-close` as a clean pass.
  - The verified commit hash goes in the journal: a verification is only meaningful against a
    specific state, which is also what makes DoD D10 checkable.
  - A verifier may not fix the code it rejected — there would be nobody checking the repair.
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** miniyaml/PyYAML agreement on `verify/skill.yaml`.
- **Artifacts produced:** `methodology/skills/verify/{skill.yaml,process.md}`.
- **Result:** META-025 done. Next: META-026 (`review-close`).

---

## 2026-08-16 — META-026 — skill `review-close`

- **Unit:** META-026
- **Inputs read:** `spec/dor-dod.md` §3/§4, `spec/journal-and-history.md` §3,
  `methodology/skills/verify/process.md`.
- **Decisions:**
  - The reviewer judges **two** things — the change and the record — and the process says why the
    second is not paperwork: the next person to touch this code must not have to re-derive what
    nobody wrote down.
  - Record mechanics are checked *first* because they are cheap and decisive (history chains,
    journal entries exist, ticks have evidence, questions closed with real consequences).
  - DoD D10 becomes a real command, `scripts/check-verify-freshness`, and a stale verification
    returns the item to `verifying` rather than `in-progress` — the code may be fine, it is the
    evidence that expired. Added to META-036.
  - Tests are re-run **on the merge result**, not only on the branch: the merge result is what
    the project actually gets.
  - `record-is-reconstructible` is a hard gate whose manual check is literally the audit
    questions from `spec/journal-and-history.md` §3, so the acceptance test's audit is applied
    continuously rather than once at the end.
  - Epic closure lives here because this is the only moment in the pipeline where every
    sibling's state is already in hand.
  - Named the two failure modes: countersigning upstream green lights (defence: map every diff
    hunk to a criterion), and closing over an unrecorded gap (accepting a gap is fine; not
    writing it into `## Notes` or a follow-up item is how the trail stops being true).
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** miniyaml/PyYAML agreement on `review-close/skill.yaml`.
- **Artifacts produced:** `methodology/skills/review-close/{skill.yaml,process.md}`; META-036
  widened.
- **Result:** META-026 done. Next: META-027 (`answer-questions`).

---

## 2026-08-16 — META-027 — skill `answer-questions`

- **Unit:** META-027
- **Inputs read:** `spec/question.md` (whole), `spec/doc-header.md` §3/§4, `spec/work-item.md` §2.
- **Decisions:**
  - Propagation is the gate, not the answer. `answer-is-propagated` requires opening each file
    named in `## Consequences` and confirming the change is there; a `## Consequences` section
    naming no file fails. The process calls a question marked `answered` that changed nothing
    "the most damaging artifact this methodology can produce" — it looks resolved, blocks
    nothing, and the next execution proceeds on the same missing information.
  - Four answer routes in a fixed order (cite a document → quote recorded intent → decide and
    write an ADR → escalate), with the process pushing back on skipping route 3 *and* on
    skipping route 4.
  - `next_status: null` — this skill restores `resume-to` rather than owning a fixed transition,
    and `item-resumed-correctly` is a hard gate comparing the new row against the suspending
    row.
  - It handles **all** open questions on the item, not only the blocking one: non-blocking
    questions otherwise accumulate into an untriaged backlog, and answering costs nearly nothing
    once the context is loaded.
  - Named the second failure mode precisely: amending an acceptance criterion to match what was
    built. That single move makes verification unable to fail — "do not quietly reshape the
    target around the arrow".
  - A missing `resume-to` must be reconstructed *and* reported as a defect in the suspending
    skill, so the iterate-and-deepen loop gets the signal.
- **Commands run:** `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** miniyaml/PyYAML agreement on `answer-questions/skill.yaml`.
- **Artifacts produced:** `methodology/skills/answer-questions/{skill.yaml,process.md}`.
- **Result:** META-027 done. Next: META-028 (`next`, the orchestrator).

---

## 2026-08-16 — META-028 — skill `next` (orchestrator)

- **Unit:** META-028
- **Inputs read:** `methodology/pipeline.yaml` `orchestrator`, `seed/02-ARCHITECTURE.md` §4,
  `seed/00-VISION.md` principle 4.
- **Decisions:**
  - `next` writes **no journal entry on an item** — it performed no work on one, and a per-
    dispatch entry would double every item journal with its least informative content. Its record
    is `tracker/board.md`, regenerated every run, whose generation timestamp says how current the
    picture is.
  - Human-addressed questions are printed **in full**, not as a pointer: the returning human
    should be able to answer without opening a file.
  - Required a `because:` line naming why each candidate was rejected. That is what makes a
    scheduling decision reviewable, and it is the first thing to read when the pipeline picks
    something surprising.
  - A "What you must never do" section states the invariants directly (never change a status,
    never skip an item, never dispatch two skills, never invent a status-to-skill mapping).
  - Named the two failure modes: **being helpful** (a nudge is engineering judgement with no
    journal, no persona and no gate — the one decision nobody can audit) and **batching** (two
    skills running before state is written leaves an unreconstructable workspace after an
    interruption).
  - A status with no owner that is not terminal is reported as a *pipeline defect*, never
    resolved by guessing a plausible skill.
- **Commands run:** `python3 scripts/lib/selftest.py` → `120 passed, 0 failed`, cross-check over
  41 inputs (all eight `skill.yaml` files now included).
- **Gates:** miniyaml/PyYAML agreement across all eight contracts.
- **Artifacts produced:** `methodology/skills/next/{skill.yaml,process.md}`.
- **Result:** META-028 done. Phase 2 complete — all 8 skills exist. Next: META-031
  (`scripts/lint-skills`), which turns the conventions these eight follow into a gate.

---

## 2026-08-16 — META-031 — `scripts/lint-skills`

- **Correction to the META-028 entry above:** it recorded the self-test as "120 passed / 41
  inputs"; the run actually reported `119 passed, 0 failed` over 40 inputs. Corrected here by
  appending rather than by editing that entry, per `spec/README.md` convention 2.
- **Unit:** META-031
- **Inputs read:** `spec/skill-contract.md`, `spec/ids-and-statuses.md`, `spec/README.md`,
  `methodology/pipeline.yaml`, all eight contracts.
- **Decisions:**
  - The linter cross-checks status ownership in **both** directions and gives the two failures
    different codes and hints: `ownership.unclaimed` (a stall) and `ownership.race` (two
    claimants). Codes are distinct because the fixes are different.
  - Placeholder checking covers `process.md` as well as `skill.yaml`. An unknown placeholder in
    prose is the same defect: it resolves to nothing.
  - `## Self-check`'s "at least two failure modes" was unenforceable as written, so
    `spec/skill-contract.md` §2.2 was amended in this unit to require a bold lead-in containing
    "goes wrong" plus ≥2 bold-led bullets. Making the rule checkable changed the spec, not the
    skills — all eight already had the shape.
  - Added `{{conventions.branch-prefix}}` and `{{conventions.commit-subject}}` to the spec's
    placeholder table: `implement/process.md` legitimately used them and the linter was right to
    flag them.
- **Commands run:**
  - `./scripts/lint-skills` → first run found 2 real defects: `answer-questions`'s purpose was
    163 characters (limit 160), and `next/process.md`'s first step was "Validate" rather than a
    read-from-disk. Both fixed — the second by rewriting `next` step 1 to read the whole
    workspace from scratch every run, which is a genuine improvement: it states that the
    orchestrator holds no state between runs.
  - **Negative test** (deliberate breakage, then restore): injected a bad persona, a two-part
    version, an unknown top-level key, a gate with both `command` and `manual_check`, and a
    stolen `on_status`. The linter reported all six expected errors, including
    `ownership.race` and `ownership.unclaimed`. Restored; clean again.
  - **Negative test** for neutrality: appended a line naming a specific runtime to a
    `process.md`; reported as `runtime-neutrality` with the line number. Removed; clean.
  - `python3 scripts/lib/selftest.py` → 0 failures.
- **Gates:** `scripts/lint-skills` exit 0 (8 contracts).
- **Artifacts produced:** `scripts/lint-skills`; edits to `spec/skill-contract.md`,
  `methodology/skills/next/process.md`, `methodology/skills/answer-questions/skill.yaml`.
- **Result:** META-031 done. Next: META-032 (`scripts/validate-workspace`).

---

## 2026-08-16 — META-037 — `scripts/lib/workspace.py`

- **Unit:** META-037 (added to the plan during this unit; META-032 was too large for one
  commit, so parsing was split from rules per PROMPT rule 9)
- **Inputs read:** `spec/workspace-layout.md`, `spec/work-item.md`, `spec/journal-and-history.md`,
  `spec/question.md`, `spec/doc-header.md`.
- **Decisions:**
  - **Parsing here, rules in the callers.** Three scripts must agree exactly on what a file
    means; two parsers would eventually disagree, and the disagreement would surface as a board
    that contradicts the validator.
  - The loader never judges validity. It records what it could not read in `load_errors` and
    leaves every verdict to the caller — so `board-gen` can render a partially broken workspace
    while `validate-workspace` fails on it.
  - Line numbers are carried through every structure (history rows, journal entries, acceptance
    criteria) and are *file* line numbers, so a finding points at the line a human would open.
    The self-test asserts this rather than assuming it.
  - The em-dash placeholder in history is normalised to `None` via an explicit method rather
    than being special-cased at each call site.
- **Commands run:** `python3 scripts/lib/selftest.py` → `152 passed, 0 failed` (33 new cases
  over a temp workspace built in the test, including a deliberately malformed journal heading
  that must be *reported*, and a status that disagrees with the last history row that the
  loader must **not** quietly fix).
- **Gates:** self-test exit 0.
- **Artifacts produced:** `scripts/lib/workspace.py`; workspace cases in `scripts/lib/selftest.py`.
- **Result:** META-037 done. Next: META-034 (`scripts/workspace-init`), then META-032.

---

## 2026-08-16 — META-034 — `scripts/workspace-init` and `scripts/new-item`

- **Unit:** META-034 (widened to two scripts: creating a workspace and creating an item are the
  same concern — getting a schema-correct skeleton on disk without relying on memory)
- **Inputs read:** `spec/workspace-layout.md` §1–3, `spec/work-item.md` §2–4,
  `spec/journal-and-history.md` §1.
- **Decisions:**
  - `workspace-init` is idempotent and says so: a skill may call it without first deciding
    whether the workspace exists.
  - It creates **no** documents under `docs/`. Per the spec, an empty `vision.md` reads to a
    later skill as "the vision is empty" rather than "nobody has written it yet".
  - `project.yaml` is written with `commands.*` as `null` and a comment explaining that a null
    is honest and makes the matching gate *skipped*. The template teaches the rule at the point
    of use.
  - `new-item` writes a **skeleton with the required headings**, not content. It is a substitute
    for remembering the format, not for thinking — stated in its own docstring so a future
    contributor does not grow it into a generator.
  - `--next-id <type>` implements the derive-from-filesystem allocation rule (ADR-0003) in one
    place, so no skill has to reimplement the scan.
  - It refuses to overwrite an existing item and refuses an ID whose prefix disagrees with
    `--type`. Both were verified by running them.
  - `workspace-init` guesses the trunk branch by reading `.git/HEAD` directly rather than
    shelling out, so it works in a directory that is not yet a repository.
- **Commands run:** created a temp workspace; ran `workspace-init` twice (second run: "nothing
  to do"); allocated `EP-001`, created it, allocated `WI-0001`, created it, and confirmed the
  next allocation returned `WI-0002`; both refusal paths exited 1 with the right message; the
  generated `history.md` carries the six-column header and the `— → draft` row.
- **Gates:** none declared for scripts; verified by execution as above.
- **Artifacts produced:** `scripts/workspace-init`, `scripts/new-item`.
- **Result:** META-034 done. Next: META-032 (`scripts/validate-workspace`).

---

## 2026-08-16 — META-033 — `scripts/lib/board.py` and `scripts/board-gen`

- **Unit:** META-033
- **Inputs read:** `spec/workspace-layout.md` §4, `scripts/lib/workspace.py`.
- **Decisions:**
  - Rendering lives in `lib/board.py` so `validate-workspace` can render in memory and compare.
    That comparison is the only reason a generated file is allowed in the repository at all.
  - **Amended `spec/workspace-layout.md` §4 during this unit:** the questions table showed an
    `age` column, which makes the board a function of the clock and would make the staleness
    check fail on every run. Replaced with the question's `created` timestamp. The spec now
    states the invariant explicitly — every byte except the generated-at line is a function of
    tracker state — so the reason the column changed is recorded where it will be read.
  - `board-gen` with no changes does **not** rewrite the file. Rewriting only the timestamp
    would produce a diff on every run and train readers to ignore board changes in review.
  - `--check` mode exists so the board can be a gate without the gate having a side effect.
  - Human-addressed questions sort first, per the spec's rule about what a returning human reads.
- **Commands run (temp workspace):** generated the board; `--check` → current; a second
  generation correctly declined to rewrite; flipped an item's status → `--check` exited 1 with
  "board is stale"; restored → current again.
- **Gates:** `board-gen --check` exit 0 on a current board, exit 1 on a stale one — both
  demonstrated.
- **Artifacts produced:** `scripts/lib/board.py`, `scripts/board-gen`; edits to
  `spec/workspace-layout.md` §4.
- **Result:** META-033 done. Next: META-032 (`scripts/validate-workspace`).

---

## 2026-08-16 — META-032 — `scripts/validate-workspace` + the broken-workspace fixture

- **Unit:** META-032
- **Inputs read:** every file in `spec/`, `methodology/pipeline.yaml`, `scripts/lib/workspace.py`.
- **Decisions:**
  - The validator resolves `pipeline.yaml` by searching `--pipeline`, then beside the scripts,
    then `../methodology/`. The adapter's installer drops a copy beside the installed scripts,
    so a consumer project needs no `methodology/` tree while `methodology/` stays the single
    source.
  - Transition legality is evaluated against `pipeline.yaml`'s rules, including the pseudo
    states `any-non-terminal` and `resume-to`; the `resume-to` case is checked against the
    actual `resume-to` recorded on the row that suspended the item, so returning an item to the
    wrong status is caught rather than assumed correct.
  - **Every** history row, including creation, requires a journal entry from its actor. An
    item created by `new-item` therefore fails validation until the creating skill journals —
    which is right, and was confirmed by running it.
  - `question.consequences.files` fires when a `## Consequences` section names no file: the
    mechanical form of "an answer that reaches no artifact has not been propagated".
  - Warnings, not errors, for judgement-adjacent things (`project.description` empty, a null
    test command, a missing `## Out of scope`, an ADR that never mentions reversibility) so a
    freshly initialised workspace is not unusable while still being told what is thin.
  - Added `fixtures/broken-workspace/` — a tree where every file is wrong on purpose — plus
    `EXPECTED-CODES.txt`. `scripts/check` will assert the emitted code set equals it exactly, so
    **a rule that silently stops firing fails the build**. That is the failure mode a validator
    is most prone to and least likely to notice, and no amount of "the validator passes" catches
    it.
- **Commands run:**
  - `./scripts/validate-workspace fixtures/broken-workspace` → 59 errors, 3 warnings across
    **44 distinct codes**, each pointing at a real line.
  - `./scripts/validate-workspace <clean temp workspace>` → exactly the two expected errors
    (`journal.execution.missing` for `intake` on both items), which is the rule above working.
  - `scripts/lib/selftest.py` and `scripts/lint-skills` both still clean.
- **Gates:** validator exercised in both directions (must-fail fixture, must-pass workspace).
- **Artifacts produced:** `scripts/validate-workspace`, `fixtures/broken-workspace/**`.
- **Result:** META-032 done. Next: META-036 (git-backed gate scripts), then META-035
  (`scripts/check`).

---

## 2026-08-16 — META-036 — git-backed gate scripts

- **Unit:** META-036
- **Inputs read:** `spec/dor-dod.md` D8/D10, `spec/workspace-layout.md` §5,
  `methodology/skills/{implement,review-close,verify}/skill.yaml`.
- **Decisions:**
  - Both scripts **fail** when they cannot look — a missing branch, a missing report, an
    unreadable range. A gate that reports success when it could not check is worse than no gate,
    because it is indistinguishable from a real pass in the journal.
  - `check-commit-refs` falls back to checking the whole branch when the trunk ref does not
    exist yet (a repository whose first work happens on a branch), rather than checking an empty
    range and passing.
  - It also fails when the range is empty: no commits means nothing was delivered, which should
    never be a green gate on an item about to move to `verifying`.
  - D10 needed a fact to compare against, so `verify` now writes `Verified-commit: <sha>` in its
    report. Recorded in `spec/workspace-layout.md` §1.2 and in `verify/process.md` with the
    reason: without it D10 degrades to an opinion about how small the last fix looked. This is
    the second time a gate forced a small spec addition, and both times the addition made the
    check possible rather than merely convenient.
  - Error output names the fix (`git rebase -i --exec …`, "return the item to verifying"), since
    the reader is an agent that has to act on it.
- **Commands run (throwaway git repo, six paths):** commit-refs pass (1/1); commit-refs fail
  (1 of 2 named, offender printed); commit-refs on a missing branch → exit 1; freshness pass;
  freshness fail after a later commit, listing the commits added after verification; freshness
  with no `Verified-commit:` line → exit 1. Every path behaved as specified.
- **Gates:** the two scripts are themselves gates; both directions demonstrated.
- **Artifacts produced:** `scripts/check-commit-refs`, `scripts/check-verify-freshness`; edits
  to `spec/workspace-layout.md` and `methodology/skills/verify/process.md`.
- **Result:** META-036 done. Next: META-035 (`scripts/check`).
