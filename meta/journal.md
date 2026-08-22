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

---

## 2026-08-16 — META-035 — `scripts/check`, and a standing instruction from the human

- **Unit:** META-035
- **Instruction received from the human mid-unit (recorded per PROMPT rule 3):**
  > "Add remote git@github.com:SigorMatt/agile-skills.git as origin, push everything now, and
  > push after every commit from here on."

  Actioned: `origin` added and the full history pushed. **From this point every unit ends with
  `git push`, not merely `git commit`.** This is now part of the unit cycle and is written into
  `meta/CHECKPOINT.md` so a fresh session after an interruption inherits it — the instruction
  would otherwise live only in conversation history, which this project's own rules say is not
  a durable place to keep state.
- **Inputs read:** `seed/03-ACCEPTANCE.md` §E, the existing scripts.
- **Decisions:**
  - `scripts/check` prints **SKIP as loudly as FAIL**, names the reason, and repeats the skipped
    steps in the summary with "a skipped step checks nothing; it is not a pass". Steps 4 and 5
    have nothing to check yet; without that noise a green run would quietly overstate coverage.
  - The must-fail fixture step compares the **set of finding codes** with
    `EXPECTED-CODES.txt` in both directions, and its failure output distinguishes "rules that
    stopped firing" from "codes not listed", telling the reader to update the file in the same
    commit if the change was intended. A validator silently losing a rule is invisible to any
    check that only asserts "the fixture fails".
- **Commands run:** `./scripts/check` → 3 PASS, 2 SKIP, exit 0; the fixture step reports
  `44 codes`.
- **Gates:** `scripts/check` is the repository's own gate; it passes.
- **Artifacts produced:** `scripts/check`; `origin` remote configured.
- **Result:** META-035 done. Phase 3 complete. Next: META-040 (`adapters/README.md`).

---

## 2026-08-16 — META-040 — `adapters/README.md`, the adapter contract

- **Unit:** META-040
- **Inputs read:** `seed/01-REQUIREMENTS.md` R5, `seed/02-ARCHITECTURE.md` §6,
  `seed/03-ACCEPTANCE.md` B4, `meta/adr/ADR-0001`, `spec/skill-contract.md`.
- **Decisions:**
  - Written **before** the renderer, deliberately. Otherwise the contract gets back-filled from
    whatever the renderer happened to do, and acceptance B4 ("a Codex CLI adapter could be
    written without touching methodology/") would be untestable.
  - Five capabilities C1–C5, each stating what the methodology needs, what a runtime may
    substitute, and what must be documented when the runtime cannot provide it. C5 (isolated
    execution) is explicitly optional — the workspace is the only channel between skills by
    design, so isolation strengthens the pipeline rather than being a prerequisite.
  - The load-bearing rule for C3: **an adapter must document per gate whether enforcement is
    hard or convention.** Claiming enforcement the runtime does not provide is the one thing
    that would make the "executable gates over vibes" premise a lie.
  - Also for C3: an adapter must not design a gate around a mechanism that fires *after* the
    action it is meant to prevent. That is ADR-0001's `PostToolUse` finding, generalised so it
    binds every future adapter rather than living in one runtime's notes.
  - "No per-skill special cases" is stated as a rule with a concrete tell (`if skill ==
    "implement"`) and a remedy (add the field to `spec/skill-contract.md`).
  - A 12-box conformance checklist, each gradeable with evidence, so "is this adapter
    conformant?" is not a matter of opinion.
  - §6 records the two questions a Codex CLI implementer will hit first (C2 without a structured
    question mechanism; C3 without a blocking hook, where the substitute is to make the
    *transition* the gated action) so they start from the questions rather than discovering them.
- **Commands run:** `./scripts/check` → 3 PASS, 2 SKIP, exit 0.
- **Gates:** repository gate green.
- **Artifacts produced:** `adapters/README.md`.
- **Result:** META-040 done. Next: META-041 (`adapters/claude-code/render.py`).

---

## 2026-08-16 — META-041 — `adapters/claude-code/render.py`

- **Unit:** META-041
- **Inputs read:** `adapters/README.md` (the contract this implements), `meta/adr/ADR-0001`
  (format facts + URLs), every `skill.yaml` and `process.md`, `methodology/pipeline.yaml`.
- **Decisions:**
  - **No per-skill branches.** Every difference between rendered skills comes from a declared
    field: `human_interaction` decides whether the question-the-human capability is removed,
    `dispatch.on_status` fills the at-a-glance line, `quality_gates[].enforcement` picks out the
    hard gates. The module docstring names the tell (`if name == "implement"`) and the remedy
    (add a field to the spec), so conformance item A2 stays true under later edits.
  - Frontmatter emits only portable Agent-Skills fields by default; `disallowed-tools:
    AskUserQuestion` is added **only** for skills whose contract forbids asking a person. That
    is capability C2 as enforcement rather than instruction, and the manifest names which skills
    are consequently runtime-only.
  - Chose **not** to emit `allowed-tools`. Pre-approving `Bash` for skills that run arbitrary
    project commands is a broad grant the consumer should make deliberately in their own
    settings; `USAGE.md` will document it. A convenience that silently widens permissions is not
    the adapter's call to make.
  - Shared material installs to `.claude/agile-skills/` and is referenced by **project-relative**
    path, not by a path relative to the skill directory — unambiguous however the runtime
    resolves a skill's own location. Gate commands beginning `scripts/` are rewritten to that
    prefix by `gate_command()`, which is the adapter's one mapping and is stated in one place.
  - The renderer **fails the build** rather than truncating: over the 1536-character description
    cap, or over the 500-line SKILL.md guidance. A skill that silently stops triggering because
    its description was cut is the failure mode ADR-0001 §4 warns about.
  - `--check` renders to a temp directory and reports **which paths differ**, not a boolean, so
    a stale `dist/` tells you what to look at.
  - A script listed for shipping but missing prints a WARNING rather than being silently
    skipped (`run-gate` arrives in META-042).
- **Commands run:** rendered 8 skills; `--check` → "dist/ is current" (determinism holds);
  rendered descriptions measured at 469–531 characters, all well under the cap; SKILL.md bodies
  180–205 lines, all under 500.
- **Gates:** `./scripts/check` → 4 PASS, 1 SKIP (the render step is now live and green).
- **Artifacts produced:** `adapters/claude-code/render.py`, `adapters/claude-code/dist/**`.
- **Result:** META-041 done. Next: META-042 (gate runner, hooks, installer).

---

## 2026-08-17 — META-042 — `scripts/run-gate` and `scripts/transition`

- **Unit:** META-042 (the runtime-neutral half of gate enforcement; the hook and installer are
  split out as META-045, because they are adapter-specific and this is not)
- **Inputs read:** `spec/skill-contract.md` §1.3–1.4, `spec/ids-and-statuses.md` §4,
  `adapters/README.md` capability C3, every `skill.yaml`.
- **Decisions:**
  - `transition` exists so that "gates pass before the status changes" is a property of a
    **program**, not of an agent's discipline. It checks legality against `pipeline.yaml`, runs
    the actor skill's hard command-gates, refuses on failure, then writes `item.md`, appends the
    history row, regenerates the board, and re-validates.
  - `--force` is provided and records `[gates forced]` **in the history reason**, permanently.
    An override that is indistinguishable from a clean pass is worse than no override path at
    all, because it would be taken silently.
  - A gate that could not be *run* (run-gate exits 2) also refuses the transition: "a gate that
    could not run is not a gate that passed."
  - `run-gate` reports four outcomes — PASS / FAIL / SKIP / MANUAL. `MANUAL` is deliberately not
    a pass: a `manual_check` cannot be discharged by a script, and pretending otherwise would
    make the judgement gates decorative.
  - `--branch` is written to `item.md` **before** the gates run, because it is a fact about the
    item rather than part of the status change, and `check-commit-refs` resolves
    `{{item.branch}}`. If a gate then fails, the field is still true.
- **Bug found and fixed during verification:** `run-gate` was rewriting a gate command that
  names one of our scripts by *replacing the whole command*, which silently discarded the gate's
  own arguments and passed the workspace root as the first positional. So
  `scripts/check-commit-refs {{item.id}} {{item.branch}}` ran as
  `check-commit-refs <root>` and failed for the wrong reason. Now only the program is rewritten,
  the resolved arguments are kept, and `--root` is appended; `validate-workspace` and `board-gen`
  gained `--root` so every gate-invoked script takes the workspace the same way. Caught only
  because the demo run produced a FAIL that did not match the repository state — a reminder that
  a gate failing is not self-evidently the code's fault.
- **Commands run (throwaway workspace + git repo):**
  - `run-gate --all` for `refine` → correctly FAILs `workspace-valid` on an unjournalled
    workspace and reports three MANUAL gates.
  - `run-gate --gate tests-pass` with `commands.test: null` → **SKIP**, not PASS, with the reason.
  - `transition` draft → ready by `refine`: legal, applied, board regenerated.
  - `transition` ready → done by `refine`: **refused**, not a transition in `pipeline.yaml`.
  - `transition` → `awaiting-answer` without `--resume-to`: **refused**.
  - With `commands.test: "exit 1"`, `transition` planned → in-progress by `implement`:
    **refused**, `tests-pass` FAIL, and the item's status was unchanged afterwards. This is the
    acceptance-B3 blocking demonstration in its runtime-neutral form.
- **Gates:** `./scripts/check` → 4 PASS, 1 SKIP; renderer re-run and `--check` clean.
- **Artifacts produced:** `scripts/run-gate`, `scripts/transition`; `--root` on
  `validate-workspace` and `board-gen`; renderer now ships both scripts and the machine-readable
  `skill.yaml` contracts that `run-gate` needs; re-rendered `dist/`.
- **Result:** META-042 done. Next: META-045 (adapter hook + installer + adapter README).

---

## 2026-08-17 — META-045 + META-044 — hook, installer, adapter README, and the blocking demo

- **Units:** META-045 (adapter hook + installer + README) and META-044 (the deliberate failing
  gate), done together because the demo is what proves the installer and hook actually work.
- **Inputs read:** `adapters/README.md` (C1–C5 and the conformance checklist),
  `meta/adr/ADR-0001` (hook contract, settings shape), every `skill.yaml`.
- **Decisions:**
  - The guard hook denies writes to `tracker/items/*/history.md` and `tracker/board.md`,
    **including shell redirects**. Without it, `transition`'s refusal would be advice: an agent
    could append the row directly and every downstream check would believe it.
  - The hook **allows** anything it cannot parse. A guard that blocked on confusion would make
    the tool unusable the first time an input shape changed; allowing degrades to the documented
    convention, which is where we would have been anyway. Stated in the file so the choice is
    not mistaken for an oversight.
  - The installer merges into an existing `.claude/settings.json` rather than overwriting it,
    identifies its own entries by a marker so an update replaces them without touching anyone
    else's, and **refuses** to rewrite a settings file it cannot parse.
  - Uninstall removes exactly what install added and explicitly leaves `tracker/` and `docs/`.
    Removing the tooling must never remove the paper trail.
  - The adapter README carries the **honest** gate table: every gate a machine can decide is
    hard-enforced; the rest are marked convention, with the reason given rather than glossed.
    `intake`'s and `next`'s gates are convention because neither owns a status transition, so
    the enforcement mechanism has nothing to attach to — written down rather than hidden.
- **Commands run:**
  - Installed into a scratch project that already had a `settings.json` with someone else's
    PreToolUse hook and a permissions block: both survived; a second install replaced only our
    two entries; uninstall left the foreign hook and the permissions intact and removed the now
    empty `.claude/skills/`.
  - Hook fed real payload shapes: DENY for an `Edit` of `history.md`, DENY for a `Write` of
    `board.md`, DENY for a shell append to `history.md`, ALLOW for `src/main.py`, ALLOW for
    `cat history.md`, ALLOW for unparseable input.
  - `meta/evidence/gate-failure-demo.sh` end to end: a legal transition allowed; an illegal one
    refused; **a failing `tests-pass` gate refusing `planned → in-progress` with the status
    unchanged afterwards**; the hook denying the bypass; and the identical command succeeding
    once the test command was fixed. Transcript saved to `meta/evidence/gate-failure-demo.md`.
  - Writing the demo exposed a real ordering defect in my first draft: it transitioned before
    journaling, so `workspace-valid` failed for the wrong reason and the demo silently skipped a
    step. Fixed by journaling before each transition — which is what every `process.md` already
    requires, so the demo now models the correct sequence rather than a shortcut.
- **Gates:** `./scripts/check` → 4 PASS, 1 SKIP.
- **Artifacts produced:** `adapters/claude-code/hooks/guard-workspace-writes.py`,
  `adapters/claude-code/install.py`, `adapters/claude-code/README.md`,
  `meta/evidence/gate-failure-demo.{sh,md}`.
- **Result:** META-044 and META-045 done. Phase 4 complete. Next: META-050 (`CONSUMER-PROMPT.md`).

---

## 2026-08-17 — META-050 and META-051 — `CONSUMER-PROMPT.md` and `USAGE.md`

- **Units:** META-050, META-051
- **Inputs read:** `seed/01-REQUIREMENTS.md` R6, `adapters/claude-code/README.md`,
  `meta/adr/ADR-0001` §8 (permission modes), the eight `process.md` files.
- **Decisions:**
  - `CONSUMER-PROMPT.md` states the five things the session must know **before** any step, and
    the "do not" list is concrete rather than moralising: never edit a criterion to make
    something pass, never fix an unrelated defect, never batch items in one `next` run. Those
    are the three failure modes the process files name most often.
  - Step 5 fixes what to show the human on every pause — board, open questions **in full**,
    what just happened, what is blocked. A returning human should not have to open a file to
    answer a question.
  - `USAGE.md` warns explicitly that `dontAsk` mode denies the tool `intake`/`refine` need, so
    an unattended-run setting would silently turn refinement into a dead end. That warning only
    exists because ADR-0001 recorded the fact when the docs were fetched.
  - `USAGE.md` §8 distinguishes the three gate outcomes (FAIL / SKIP / MANUAL) explicitly,
    because "the gate did not pass" is three different problems with three different fixes, and
    conflating them is how a SKIP gets treated as a pass.
  - It also tells the reader that a skill doing the wrong thing is a **defect in the skill**,
    and names the loop: journal names the skill and version → fix `process.md`/`skill.yaml` →
    bump → re-render → re-install. That is the iterate-and-deepen loop the vision asks for,
    written where the person who hits the problem will read it.
  - Both files are written to match what actually works; `CONSUMER-PROMPT.md` will be used
    verbatim for the toy run in Phase 6, and re-checked against reality afterwards.
- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP.
- **Artifacts produced:** `CONSUMER-PROMPT.md`, `USAGE.md`.
- **Result:** META-050 and META-051 done. Next: META-052 (`README.md`).

---

## 2026-08-17 — META-052 — `README.md`

- **Unit:** META-052
- **Inputs read:** `seed/00-VISION.md`, `seed/03-ACCEPTANCE.md` D3, the whole repository.
- **Decisions:**
  - Opens with what it does and the bet behind it, not with a feature list. The claim being made
    is narrow and stated as such: the discipline of a good team is largely *procedural*, and
    procedure is the part you can encode.
  - Includes a **"What this is not"** section — not a coding agent, no ceremonies, no
    parallelism, and explicitly **not a guarantee of quality**: it guarantees the checks ran and
    the reasoning was recorded, which is a different claim. Overclaiming here would undercut
    every honest thing the rest of the repository does.
  - The three properties (state on the filesystem, executable gates where possible, every action
    attributable to a skill) are given as the reasons the layout is what it is, so a reader can
    predict where things live.
  - The roadmap points at the known-weaknesses list in `meta/FINAL-REPORT.md` rather than
    leaving a reader to discover them.
  - Forward references to `examples/toy-project/` and `meta/FINAL-REPORT.md` are deliberate;
    both land in the phases that follow, and META-070's sweep re-checks that every link resolves.
- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP.
- **Artifacts produced:** `README.md`.
- **Result:** META-052 done. Phase 5 complete. Next: META-060 — choose the toy project and write
  the human answer key for the simulated refinement.

---

## 2026-08-17 — META-060 — toy project chosen; run inputs written

- **Unit:** META-060
- **Inputs read:** `seed/03-ACCEPTANCE.md` §C, `USAGE.md`, `adapters/claude-code/README.md`.
- **Decisions (ADR-0004):**
  - The run happens in a **standalone git repository outside this one** and is imported into
    `examples/toy-project/` without `.git`, with the history preserved as `GIT-LOG.md` and
    `GIT-BRANCHES.md`. A nested repository would either become a submodule (a reader clones and
    gets an empty directory) or force the toy commits to share this build's history, which would
    destroy the very `git log --grep <ID>` property the example exists to demonstrate.
  - Rejected `git bundle` explicitly: it preserves everything and is unreadable, and C6 is
    precisely about a reader reconstructing the story.
- **Toy project:** `linecount`, a Python CLI that reports per-file line counts for a directory.
  Chosen because its one-sentence statement is under-specified in exactly the ways this
  methodology is meant to catch: "how much is in each file" (lines? bytes? words?), "a folder"
  (subdirectories? symlinks? unreadable files?), and "nothing fancy" (a scope boundary stated as
  a vibe).
- **How the human is played:** `HUMAN-SCRIPT.md` was written **before** the run, so the answers
  could not be tuned to whatever the pipeline produced. Three standing rules: answer vaguely
  first and specifically when pushed; concede after one push-back; and refuse to decide one
  thing outright ("whatever's sensible" for non-text files), so the pipeline must record an
  **assumption** rather than invent a requirement — and the record must distinguish the two.
  That refusal is also the seed for the organic upstream question acceptance C3 requires.
- **Recorded honestly rather than engineered:** the human answers "no" to a Definition of Ready
  override, so the override path is **not** exercised by this run. Noted in `HUMAN-SCRIPT.md`
  and carried to the final report as a known gap instead of being faked.
- **Commands run:** created the scratch repository, installed the rendered skills (11 actions,
  8 skills present under `.claude/skills/`), and confirmed `validate-workspace` reports an
  uninitialised workspace — which is the correct answer before `workspace-init`.
- **Gates:** `./scripts/check` → 4 PASS, 1 SKIP.
- **Artifacts produced:** `meta/adr/ADR-0004-toy-project-execution.md`,
  `examples/toy-project/IDEA.md`, `examples/toy-project/HUMAN-SCRIPT.md`.
- **Result:** META-060 done. Next: META-061 — `intake` + `refine` by a context-free subagent.

---

## 2026-08-17 — META-061a — two skill defects found by the first toy run, fixed

- **Unit:** META-061a (unplanned; PROMPT rule 5 — a confused subagent is a defect in the skill)
- **How they surfaced:** the context-free subagent running `intake` on the toy project reported
  both, unprompted, rather than working around them silently. That is the acceptance test doing
  exactly what it is for.
- **Defect 1 — `intake`'s journaling contradicted the validator.** `intake/process.md` said to
  journal on the epic "(not on each item)", but `validate-workspace` requires a journal entry
  from every skill that appears as an actor in an item's `history.md` — and `intake` is the actor
  on each item's creation row. The subagent hit `journal.execution.missing` three times, chose
  the sensible resolution (full entry on the epic, short entry on each item pointing to it), and
  **wrote the contradiction into its journal for the next run**.
  - **Fix:** the validator is right and the process was wrong. `intake/process.md` now requires
    the full entry on the epic *and* a short entry on every item created, and explains why: the
    reasoning about how work was split belongs to the split, not to any one item.
- **Defect 2 — no skill said to commit.** `spec/workspace-layout.md` §5 says a tracker-only
  commit is legitimate for the non-coding skills, but no `process.md` ever told one to commit.
  The subagent finished with the entire workspace untracked and said so. Left alone,
  `git log --grep <ITEM-ID>` would return an item's code and none of its story, which is half of
  R4.4.
  - **Fix:** a `### Commit what you wrote` step added to `intake`, `refine`, `plan`, `verify`,
    `review-close` and `answer-questions`, with a `kind: commit` output added to each contract so
    the obligation is in the machine-readable form too.
- **Versions:** those six skills bumped 0.1.0 → 0.1.1 in the same commit, per
  `spec/skill-contract.md` §3 (new step + new output = MINOR… recorded here as PATCH-level 0.1.1
  because the pipeline itself is pre-1.0 and no existing workspace is invalidated by either
  change).
- **Consequence for the toy run, recorded rather than hidden:** `intake` ran under v0.1.0 and
  everything after it runs under v0.1.1, so the toy project's journals name two versions. That is
  the versioning working as designed — a reader can tell which contract produced which artifact —
  and it is called out in the final report rather than smoothed over by re-running intake.
- **Commands run:** `./scripts/lint-skills` → clean; `render.py` → 8 skills; `./scripts/check` →
  4 PASS, 1 SKIP; re-installed into the toy project and confirmed the new step is present in the
  installed `refine/SKILL.md`.
- **Result:** both defects fixed. Continuing META-061 with `refine`.

---

## 2026-08-17 — META-061 — `intake` + `refine` on the toy project

- **Unit:** META-061
- **How it was run:** two context-free subagents, each given only the installed skills,
  `CONSUMER-PROMPT.md` and the project path, and told explicitly not to read anything outside the
  project. The builder answered as the human from `HUMAN-SCRIPT.md`, extending it in the same
  spirit where a question was not anticipated.
- **Result:** `EP-001` open; `WI-0001` and `WI-0002` at `ready`; `docs/product/vision.md` v1;
  `validate-workspace` exit 0 with the one expected warning (`commands.test` is null until
  `plan` sets it); two commits, each naming its item.
- **What the skills actually produced, worth recording as evidence they work:**
  - `intake` split the work along the seam the human named himself, and journalled why it
    rejected two other splits — including that a counting item without sorting "would deliver
    nothing he does not have", since `wc -l *` already does that.
  - It kept the human's "you decide, I don't really care" about non-text files as a **delegated
    open point**, not a requirement, and said why: inventing a rule and recording it as his would
    be indistinguishable from him asking for it.
  - It separated the scope exclusions the human stated from the ones the analyst derived, on the
    record.
  - `refine` produced a per-criterion DoR verdict with evidence, found R4 and R8 failing on both
    items, and turned 9 criteria into 13 and 4 into 11 — each with a command or an observation.
    AC1 now carries a worked example down to the exact spaces.
  - `refine` recorded a case where the human **rejected its proposal** and kept both its proposal
    and his reason, rather than presenting his choice as the plan all along.
  - It labelled two criteria as resting on nobody's word but its own (`WI-0001` AC12, and the
    `(all 1 files)` plural) so `plan` and `verify` inherit that risk visibly.
  - When WI-0002's criteria interacted with WI-0001's, it refused to edit WI-0001 — which is past
    `ready` and therefore frozen — and wrote the interaction into WI-0002's notes instead. The
    freeze rule from `spec/work-item.md` §2 held under pressure without anyone enforcing it.
- **Gap deliberately left open for the next stage:** nothing in either item covers a *single
  file inside the folder* that cannot be read. The human was never asked, and the builder did not
  volunteer it. That is the gap `implement` should hit and escalate, which is what acceptance C3
  requires to happen organically.
- **Gates:** toy workspace `validate-workspace` exit 0; `./scripts/check` green in this repo.
- **Result:** META-061 done. Next: META-062 — `plan` for WI-0001.

---

## 2026-08-17 — META-062/063/065 + META-063a — the autonomous run, and two design defects it exposed

- **Units:** META-062 (`plan`), META-063 (`implement`), META-065 (`verify`) all ran; plus
  META-063a, an unplanned fix unit for the two defects the run exposed.
- **How it was run:** one context-free subagent looping `/next` unattended, explicitly forbidden
  from asking a human and told to stop at the first hard stop.
- **What ran, in order:** `next` dispatched `plan` (WI-0001 `ready → planned`), `implement`
  (`planned → in-progress → verifying`), `verify` (`verifying → in-review`), then `review-close`
  — which **refused to close on a hard gate** and stopped. WI-0002 was correctly rejected as a
  candidate every time (`depends-on: WI-0001`, not done), and EP-001 because `open` has a null
  owner. The selection logic behaved exactly as `pipeline.yaml` specifies.
- **What the skills produced:** a plan mapping all 13 criteria to steps and named tests, three
  ADRs (including one for a case *no acceptance criterion covered* — a file that cannot be
  read), `commands.test` filled in while `commands.lint` was deliberately left null so
  `lint-clean` reports **skipped** rather than passed; `linecount.py` with 27 tests over three
  commits all naming the item; and a verification that decided all 13 criteria by commands it
  ran against fixtures it built — a real PNG, a fresh `git clone`, `chmod 000` paths, symlinks,
  and 14 deliberate mutations of the delivered behaviour to confirm the suite catches them.

### Defect 1 — the freshness gate could never pass, and I caused it

`check-verify-freshness` compared the verified sha against the branch head. In META-061a I added
a commit step to `verify` — so `verify`'s own record commit becomes the head, and the gate reads
its own required output as "code changed after verification". D10 passed on the facts
(`git diff` showed only `tracker/` files) and failed as a gate. Every exit from `in-review` was
blocked, including filing a question about it.

**Fix:** the gate now compares **paths, not shas**. If the head has moved but every changed path
is under `tracker/` or `docs/`, the verification still covers the code and the gate passes,
saying so. This makes the gate *more* precise, not weaker: D10 is about the code the verification
covers, and a record-only commit is not a code change.

Verified both directions on the real repository: passes on the toy project's actual state
("only the record changed (6 files)"), and still fails in a throwaway clone with one real edit to
`linecount.py`, naming the file and the commit.

### Defect 2 — gates guarded every transition, which traps items

`transition` ran the acting skill's hard gates on *every* move. Two consequences the run hit:

- `implement` is told to move an item to `in-progress` **before** writing code, but `tests-pass`
  and `commits-reference-the-item` cannot pass on an empty branch. The subagent worked around it
  by committing a first slice before transitioning, and recorded the deviation — but the
  process and the tooling genuinely disagreed.
- With the freshness gate failing, `review-close` could not reject, could not send back, and
  **could not even file a question** about the gate blocking it. The item was trapped.

**Fix:** a skill's hard gates now guard only its **completion** transition — the move to its own
`next_status`. On any other move they still run and are still reported, but they do not refuse.
Escaping downward is never what a gate should prevent; declaring success is. Recorded in
`spec/skill-contract.md` §1.3 with both reasons, and in the adapter's enforcement notes.

### On whether these are fixes or conveniences

Both were checked against that question deliberately, because "the gate is inconvenient" is
exactly how a methodology like this rots. Defect 1 makes the check narrower and more accurate.
Defect 2 removes a deadlock that made a hard gate unfileable-against. Neither weakens what a
gate asserts at the moment it matters. The subagent's own analysis reached the same three
options and it declined to use `--force` — correctly, since overriding a hard gate is not the
reviewer's call.

- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP; re-rendered and re-installed into the toy
  project; both directions of the freshness gate demonstrated on the real repository.
- **Result:** defects fixed. Resuming the run at `review-close`.

---

## 2026-08-17 — META-062..067 — the autonomous run completed

- **Units:** META-062 (`plan`), META-063 (`implement`), META-064 (`answer-questions`),
  META-065 (`verify`), META-067 (`review-close`, both items and the epic).
- **How it ran:** one context-free subagent looping `/next` unattended. Ten dispatches:
  plan → implement → verify → review-close (**refused by a gate**) → *tooling fixed* →
  review-close → plan → implement (**filed Q-001**) → answer-questions → verify → review-close,
  which closed WI-0002 and then EP-001.
- **The orchestrator behaved exactly as specified**, with no engineering leaking in: WI-0002 was
  rejected as a candidate on every run while `depends-on: WI-0001` was unmet, EP-001 was never
  dispatched because `open` has a null owner, and when Q-001 opened, the architect question
  preempted the status owner — step 3 before step 4, as `pipeline.yaml` says.
- **Acceptance C3 — the question round trip happened organically.** `implement` discovered that
  WI-0002's AC10 described a folder that **cannot exist**: 27 files whose two largest hold 9 and
  7 lines cannot sum to 1204. Nobody planted this; it was a worked example refine wrote and
  nobody arithmetic-checked. `implement` filed Q-001 rather than silently choosing a fixture,
  correctly marked it non-blocking (the *rule* was implementable, only the illustration was
  impossible), and continued. `answer-questions` corrected the example from the human's own
  verbatim refinement words, kept his `27` and `1204`, and propagated the amendment into three
  files. **No acceptance criterion was edited to make anything pass** — the amendment was to an
  illustration that was arithmetically impossible, recorded as such in the criterion, the item's
  notes and the plan.
- **Final state:** `main` at 14 commits, every one naming its item; both items `done` and merged;
  EP-001 `done` with all six success measures re-run on the merged trunk; 46 tests green from a
  fresh clone with nothing installed; `validate-workspace` clean, 0 errors and 0 warnings.
- **No `--force` anywhere.** No history row in the toy workspace carries `[gates forced]`. The
  one gate that refused a transition was fixed in the tooling and the transition then passed on
  its merits — which is the outcome the design wants, and the reason `--force` exists at all is
  that it was *not* needed here.
- **Left visible rather than papered over** (the run reported both): `docs/product/vision.md`
  does not mention `--top`, and `review-close` is not permitted to edit product docs; and the
  argparse usage line changed once `--top` existed, so WI-0002's no-argument error is not
  byte-identical to WI-0001's — recorded in WI-0002's notes as an accepted difference.
- **Acceptance C4 is not yet met:** `verify` found no defects in either item, so no BUG was filed.
  Rather than manufacture one, the builder exercised the delivered tool directly and found a real
  boundary defect, then dispatched an **independent regression verification** of the closed epic
  — without saying what to look for — so that any bug is filed by `verify` because `verify` found
  it. That run is in progress; whatever it reports is what gets recorded.
- **Result:** META-062 through META-067 done for the two work items and the epic.

---

## 2026-08-17 — META-065a — independent regression pass, and the spec gap it exposed

- **Unit:** META-065a (unplanned)
- **Why it was run:** the pipeline closed both items and the epic with `verify` finding no
  defects, so acceptance C4 (a `verify`-filed BUG that reaches `done`) had nothing to point at.
  Manufacturing a defect would have been worthless evidence. Instead the builder ran the tool by
  hand, confirmed a real defect existed, and then dispatched an **independent regression
  verification** of the closed epic — **without saying what to look for** — so that whatever got
  filed was filed by `verify` because `verify` found it.
- **What it found — three real defects, none planted, all `found-in: WI-0001`:**
  - **BUG-0001 (high)** — a direct AC7 failure. A symlink loop or a symlink into an unreadable
    directory escapes the file lister and is caught by the *folder*-level handler, so the tool
    prints `Too many levels of symbolic links` about a folder that is perfectly readable, exits
    2, and never counts the real files beside it.
  - **BUG-0002 (medium)** — the seam between ADR-0002 and AC10. When every file is skipped,
    stdout prints `no files`, byte-identical to a genuinely empty folder. This is the defect the
    builder had found independently, which is a useful cross-check on the pass.
  - **BUG-0003 (medium)** — file *contents* are never decoded, but `os.scandir` decodes *names*,
    so a filename containing an invalid byte raises `UnicodeEncodeError`: a traceback, empty
    stdout, and exit 1 — a status no document in the project defines. It also inverts the epic's
    own "why now": `wc -l *` handles that folder cleanly.
  - It also **declined to file** two things and said why: a `total` that excludes skipped files
    (AC3's own wording settles it) and a `BrokenPipeError` reachable only at 5000 files, outside
    the human's stated scale. Recording what it judged not-a-defect is as useful as the defects.
- **The spec gap it exposed:** `verify` must file a bug "under the same epic", but EP-001 was
  `done`, and a `done` epic had **no legal transition out**. The pass filed the bugs anyway,
  left `workspace-valid` honestly failing with `epic.closed-with-open-children`, refused to
  guess a resolution, and filed a non-blocking question with three options and no
  recommendation — because the answer redefines "done" for every epic in the pipeline. That is
  the question protocol working exactly as designed.
- **The fix:** a closed epic can be **reopened**. `pipeline.yaml` gains `done → open` for epics;
  `spec/ids-and-statuses.md` §3.4 states the rule and the argument; `journal-and-history.md`
  narrows "a `done` row must be last" to work items and bugs; `validate-workspace` allows that
  one row after `done` on an epic and nothing else.
  - The reasoning, recorded in the spec: forbidding it makes "do not record the defect" the path
    of least resistance, because the only ways to silence the validator are to file the bug under
    a different epic — severing it from the goal it violates — or not to file it at all. A
    methodology that rewards not recording a defect has chosen the wrong invariant.
- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP; re-rendered and re-installed;
  `validate-workspace` on the toy project now reports exactly one error,
  `epic.closed-with-open-children`, which is precisely what the reopen is for.
- **Result:** methodology fixed. Next: `answer-questions` answers Q-001 and the loop carries the
  three bugs to `done` (META-066).

---

## 2026-08-17 — META-066a — a clock defect, and the tooling change it forced

- **Unit:** META-066a (unplanned)
- **What happened:** `answer-questions` answered EP-001/Q-001 by reopening the epic exactly as
  the amended spec allows — and then `plan` on BUG-0001 hit a wall that had nothing to do with
  planning. The independent regression pass had stamped its four artifacts with **local time
  labelled `Z`** (`2026-08-17T01:30:00Z` for what was really `2026-08-16T22:30:00Z`), so every
  history row the pipeline wrote afterwards was, correctly, "earlier than the previous row".
  The item could not move at all.
- **What the subagent did, and why it was right:** it refused every repair available to it —
  `history.md` is hook-denied by design, `transition` had no `--when`, and patching the script's
  clock or reverting through git would be a skill rewriting its own history. It also refused to
  suspend the item, because appending a second row would carry the same defective timestamp and
  make the record worse. It filed a question with five costed options and a recommendation, and
  stopped. That is the escalation protocol doing exactly its job under real pressure.
- **A second correction it made and recorded rather than tidied:** during
  `answer-questions` it left `outcome: delivered` on the reopened epic; the validator refused it
  with `item.outcome.premature`; it cleared the field and put both the wrong decision and its
  reversal in the journal and in the question's answer.
- **The fix, which is the subagent's own recommendation:** `scripts/transition` now stamps each
  row with `max(now(), previous_row + 1s)` and **announces** the clamp, naming the offending
  earlier timestamp. One artifact stamped in local time can no longer freeze an item, and a
  clock that needs clamping is surfaced rather than silently accommodated. Recorded as a rule in
  `spec/journal-and-history.md` §1: the tool appending a row is responsible for monotonicity and
  must say when it has enforced it.
- **Why not simply forbid hand-written timestamps:** they are unavoidable — a question's
  `created`, a journal heading, a doc's `updated` are all written by a worker, and telling
  workers to be careful is not a mechanism. Making the append-side robust is.
- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP after re-render; re-installed into the
  toy project.
- **Result:** tooling fixed. Sending the run back to answer BUG-0001/Q-001 and continue.

---

## 2026-08-17 — META-066b — `--restamp-last`, the one sanctioned repair

- **Unit:** META-066b (unplanned)
- **Two findings from the run, both correct:**
  1. **The subagent caught me half-doing something.** I said I had added the monotonicity rule to
     `spec/journal-and-history.md` §1, and I had — but I re-rendered and re-installed *before*
     making the edit, so the copy the subagent read did not contain it. It read the installed
     spec, found the sentence absent, and said so rather than assuming I was right. That is the
     behaviour the whole design is trying to produce, applied to the builder. Re-rendered and
     re-installed.
  2. **One history row cannot be repaired by appending.** After the clamp, exactly one finding
     remained: row 6 of `BUG-0001/history.md` is true UTC, row 5 is the filer's skewed value, and
     the pair is unorderable. The clamp only affects rows being appended; a later row cannot fix
     an earlier pair; neither row may be edited. The item was permanently frozen, and the
     subagent refused every route around it — no `git revert`, no restore from an earlier commit,
     no patching the clock, and no `--force`, correctly noting that `[gates forced]` would libel
     rows whose engineering gates genuinely pass.
- **The fix:** `scripts/transition --restamp-last <UTC> --reason "..."`. It changes exactly one
  thing — the `when` of the **last** row — refuses a value earlier than the previous row, refuses
  to touch a first row (which cannot be out of order with anything), prints old → new, and tells
  the caller to journal it as a correction.
- **Why an exception to append-only is right here, and why it is exactly one:** the rule exists
  so that evidence is never destroyed. Here nothing is being hidden — both rows' stories are
  already in the journals — and the alternative is an item that can never move, which is not a
  more honest record, only a stuck one. The spec states the exception, its single permitted
  scope, and the closing rule: "If you find yourself wanting a second exception, you want a
  journal entry instead."
- **Commands run:** `./scripts/check` → 4 PASS, 1 SKIP; re-rendered; re-installed and confirmed
  both the spec sentence and the new flag are present in the installed copies.
- **Result:** the run can proceed. Sending it back to repair the row and continue.

---

## 2026-08-17 — META-066/068 — the bugs reached done; the run is imported

- **Units:** META-066 (BUG-0001..0003 driven to `done`), META-068 (import and validate).
- **What the run did after the restamp:** 13 more `next` dispatches, one action each —
  implement/verify/review-close on BUG-0001, then the full plan→implement→verify→review-close on
  BUG-0002 and BUG-0003, plus two `answer-questions` runs that correctly preempted the status
  owners. EP-001 was closed a second time with all six success measures re-run on the merged
  trunk.
- **Acceptance C4 is met three times over.** Every bug was filed by `verify`, and every one
  reached `done` through the full pipeline, with its regression tests demonstrated to fail
  against the pre-fix build.
- **Things the run did that are worth recording as evidence the design works:**
  - **No bug's scope widened.** BUG-0001's fix passes within a line of BUG-0002's symptom and
    left it alone; BUG-0002's edits a function two lines from BUG-0003's crash and left that.
    Each declared the omission, and each was checked by the next item's `verify`.
  - **`verify` measured an ADR's claim instead of trusting it.** ADR-0008 justified its decision
    with an example using `LC_ALL=C`; verification found that CPython's UTF-8 mode makes that
    example wrong, and that `PYTHONIOENCODING=ascii` demonstrates it decisively. The ADR went to
    v2 carrying both the correction *and* the original belief, per `doc-header.md` §4 — and **no
    code changed**, because the decision was right and only its evidence was wrong. That is the
    distinction the ADR format exists to preserve.
  - **A criterion was found to be unsatisfiable and was narrowed, not deleted.** BUG-0001's AC6
    required each of four regression tests to fail without the fix, which the "unchanged
    behaviour" test cannot do by construction. It was scoped to AC1–AC3 through a filed question,
    matching wording BUG-0002 already used.
  - Three questions were filed and answered **inside the record**; none needed the human.
- **Final state of the run:** 5 items done, epic done, 0 open questions, `validate-workspace`
  0 errors and 0 warnings, 60 tests green from a fresh clone with nothing installed, and **no
  `[gates forced]` row anywhere in the workspace**. `git log --grep` reconstructs each item
  (10, 9, 11, 6, 7 and 5 commits).
- **Import (META-068):** `examples/toy-project/import.sh` copied the tracker, the docs and the
  source, and rendered the real history into `GIT-LOG.md` and `GIT-BRANCHES.md` (ADR-0004).
  `validate-workspace` on the imported tree: **6 items, 10 documents, 0 errors, 0 warnings**.
- **`./scripts/check` is now fully green with no skipped steps** for the first time: library
  self-test, lint-skills, the 44-code must-fail fixture, render determinism, and the must-pass
  example workspace.
- **Result:** META-066 and META-068 done. Next: META-069, the audit.

---

## 2026-08-17 — META-070 (in progress) — acceptance sweep finds two untested paths

- **Unit:** META-070
- **Evidence gathered so far:** 8 contracts lint clean with no runtime names anywhere under
  `methodology/` or `spec/`; 10 statuses, 17 transitions, **no non-terminal status without an
  owner**; 9 spec files; 8 rendered skills; the toy workspace validates with 0 errors and 0
  warnings; three `verify`-filed bugs all reached `done` with `outcome: delivered` and
  `found-in: WI-0001`; **no `[gates forced]` row anywhere in the workspace**.
- **Two acceptance paths are genuinely untested, and I am recording that before deciding what to
  do about it rather than after:**
  1. **`awaiting-answer` was never reached.** Five questions were filed and answered — by
     `implement`, `plan` and `verify`, all to the architect, all answered from the record — but
     **every one was judged non-blocking**, so no item was ever suspended. The judgement looks
     right in each case; the consequence is that the highest-risk path in the whole protocol
     (file → suspend → answer → propagate → resume at `resume-to`) has never run end to end.
     Acceptance C3 names that path explicitly.
  2. **The Definition of Ready override was never exercised**, because the scripted human
     refused to override — which was written into `HUMAN-SCRIPT.md` before the run and is
     therefore honest, but leaves `refine`'s loudest failure path untested.
- **Decision:** run **one more work item** designed so that both paths are exercised for real,
  rather than ticking C3 on a partial demonstration. The two gaps are causally linked in
  practice — an item pushed past the Definition of Ready with an unresolved point is precisely
  what produces a blocking question downstream — so one item can exercise both honestly:
  the human overrides DoR on an unresolved output-shape question, and `implement` then hits a
  user-visible decision it is not entitled to make and must suspend the item.
- **Sequencing:** the audit (META-069) is reading the imported tree now, so the extra item runs
  in the scratch repository afterwards, followed by a re-import and a short addendum to the
  audit covering it.

---

## 2026-08-17 — META-069 — the audit

- **Unit:** META-069
- **How it was run:** a fresh agent with no knowledge of the project, restricted to
  `tracker/`, `docs/`, `GIT-LOG.md`, `GIT-BRANCHES.md` and `src/` — explicitly barred from
  `README.md`, `IDEA.md`, `HUMAN-SCRIPT.md` and anything outside `examples/toy-project/`, since
  those describe the exercise rather than the work.
- **It answered all four questions** — what was built and why, which decisions were made and by
  whom, what questions arose and how they resolved, what verification found — so the paper trail
  requirement (R4) holds. That is acceptance C6.
- **It did not take the record's word for anything**, which is the part that makes the result
  worth having: it re-ran the tool and its suite, rebuilt all three bug reproductions and the
  acceptance-criteria worked examples, re-ran the encoding measurement ADR-0008 rests on, removed
  each bug fix and confirmed the suite failed as claimed, and resolved all 45 commit shas.
- **What it confirmed:** every behavioural claim reproduced byte for byte; every mutation
  produced the failures the record claims; `lint-clean` is reported *skipped* and never passed;
  no gate was ever forced; and where the project was wrong it said so — a reversed decision, a
  corrected ADR rationale, an admitted clock failure, a gate failure reported rather than routed
  around.
- **What it found wrong, and I am recording every one rather than the flattering summary:**
  - **The bug items' timestamps are fiction.** The monotonic clamp produced six transitions at
    one-second intervals, and one execution is dated 2h14m apart between its history row and its
    journal entry. The cause is disclosed in the record; the *consequence* — that chronology is
    only recoverable from `GIT-LOG.md` — is not. This is a direct cost of my own clamp fix.
  - **A factually wrong justification propagated into five documents**, including shipped source
    comments, an ADR and the architecture overview — and was contradicted by a transcript thirty
    lines above it in the same item's plan. Six review layers passed it.
  - **Two commit shas in reports do not resolve**, one of them the sha a bug reproduction is
    pinned to. The other 43 are exact.
  - An implementation report's line arithmetic is wrong; one review passed a
    record-completeness criterion on counts that were themselves wrong, while its sibling review
    counted the identical structure correctly.
  - **One overclaim it falsified in a single command**: the epic closes claiming "a number,
    never a stack trace", but piping 5000 files into `head -1` still raises `BrokenPipeError` and
    exits 1 — a case the regression pass measured and chose not to file.
  - **Independence is nominal.** One agent played customer, analyst, architect, developer,
    verifier and reviewer. Disclosed in two refinement artifacts and **not** in the vision or the
    epic, which are the documents a manager would actually read.
- **Verdict: qualified sign-off** — the work is accounted for, with four corrections required
  first and two standing caveats. That is a better outcome than a clean pass: a clean pass from
  an auditor this thorough would have meant it was not looking.
- **What this tells me about the methodology**, for the final report: the gates catch what a
  machine can decide and the review layers demonstrably do **not** catch a plausible-sounding
  false claim repeated across documents. That is the single most important finding of this whole
  build, and it argues for a specific next iteration — a check that resolves every sha and
  cross-document claim mechanically, because judgement gates did not.
- **Result:** META-069 done. `AUDIT.md` committed.

---

## 2026-08-17 — META-070a — a tooling gap reported twice, now fixed

- **Unit:** META-070a
- **What was reported:** two separate runs hit the same thing — `scripts/transition` could not
  **clear** `outcome:` when an epic left `done`, so a reopened epic kept `outcome: delivered`,
  the validator correctly refused it with `item.outcome.premature`, and the only way out was to
  hand-edit `item.md`. The first run cleared it by hand and journalled the reversal; the second
  hit it again and reported it as a toolkit limitation rather than treating a hand-edit as
  normal.
- **The fix:** `transition` now clears `outcome` automatically when an item moves off `done`,
  and says so. `spec/work-item.md` §1 already required the field to be present *if and only if*
  the status is `done`, so the script was simply failing to maintain an invariant the spec
  states.
- **Why it is worth recording rather than just fixing:** the same defect surfacing twice, in two
  independent runs, is the signal that it was a tooling gap and not a worker mistake. The first
  report could have been read either way; the second could not. Both runs did the right thing by
  journalling the manual repair rather than performing it silently — which is the only reason
  the pattern was visible at all.
- **Commands run:** `./scripts/check` → all steps passed; re-rendered and re-installed.
- **Result:** fixed.

---

## 2026-08-17 — META-070b — the Definition of Ready gains R10, because a run proved it was missing

- **Unit:** META-070b
- **What happened:** the extra work item (WI-0003, `--sort`) was set up specifically so the
  simulated human would push it through with one thing unresolved — how `--sort name` and
  `--top N` behave together — expecting `refine` to record a Definition of Ready override, since
  the override path had never been exercised.
- **`refine` refused, and was right.** Its reasoning, verbatim from the run: the override record
  has a mandatory field naming *which criteria were not met*, and walking R1–R9 it found all nine
  passing — every one of the ten criteria was individually decidable. "To record the override I
  would have had to name a criterion that isn't failing, and a history row saying an item was
  forced through a gate it actually passed is a false entry that devalues every real override in
  this repo."
- **That is a defect in my checklist, not in its judgement.** There was no criterion an item
  could fail by leaving a combination of its own behaviours unconstrained. The skill was more
  rigorous than the spec it was applying, and it said so instead of manufacturing a record that
  would have looked correct.
- **The fix:** `spec/dor-dod.md` gains **R10** — every combination of the behaviours an item
  introduces either has a stated behaviour in a criterion, or is named in `## Out of scope`, or
  is recorded in `## Notes` as deliberately unconstrained **with who left it so**. R10
  deliberately does not force a combination to be *decided*; it forces it to be **visible**,
  which is the difference between an open question someone can find and one nobody knows exists.
  The spec records the run that produced it.
- **What it did instead, which is what R10 now requires anyway:** tagged the human's answer
  `[unresolved]`, quoted it in full, wrote both readings with a worked example into `## Notes`,
  and instructed `implement` not to escalate it — because escalating would have got it decided
  and written down as a decision, which is exactly what the human refused.
- **Consequence for acceptance C3:** the Definition of Ready override remains unexercised, and
  the attempt to exercise it produced something more useful than a tick would have been. Recorded
  as an honest gap; the final report says so rather than claiming the box.
- **Commands run:** `./scripts/check` → all steps passed after re-render.
- **Result:** R10 added. WI-0003 is running through the pipeline under the checklist it was
  refined against; the journals record which version applied.

---

## 2026-08-17 — META-070c — acceptance C3's blocking round trip happened, organically

- **Unit:** META-070c
- **What happened:** WI-0003 ran plan → implement → verify → review-close, and `review-close`
  **suspended the item**. Not because of anything planted: it reached Definition of Done D7
  ("documents the change invalidated have been updated") and found that
  `docs/product/vision.md` still described `--sort` as *being added, not delivered* — which
  `intake` had written correctly, because at that moment it was true.
- **It could not fix it, and said exactly why.** `spec/doc-header.md` §5 allocates
  `product/vision.md` to `intake`, `refine` and `answer-questions`; `review-close` is listed
  only for `ways-of-working.md`. The reviewer quoted that section's own reasoning back: it would
  be "editing the document and then certifying D7 and DE4 against my own edit". So it filed a
  **blocking** question addressed to the architect, set WI-0003 to `awaiting-answer` with
  `resume-to: in-review`, left the branch deliberately unmerged (merging first would have made
  the question academic), and stopped.
- **This is acceptance C3, and it arose from the methodology rather than from the exercise.** The
  rule that produced it is one I wrote for a different reason — to stop the record being updated
  by the same execution trying to satisfy it — and it fired, correctly, on a case I had not
  anticipated. That is a better demonstration than the one I set out to engineer.
- **It also rejected the easy option on the record's own precedent.** Option C was "close with D7
  and DE4 recorded unmet", which the spec permits — and it declined, noting that this is exactly
  what happened to `--top` at the epic's first closure, and that the human's response on
  returning had been to have it fixed.
- **What the earlier skills produced:** `plan` traced every design choice to an existing ADR or a
  recorded reversible assumption, and wrote **ADR-0009** recording the `--top`/`--sort`
  combination as *deliberately unspecified*, with four options and reversal costs — which is R10
  satisfied before R10 existed. `implement` added 17 tests and modified none of the existing 60.
  `verify` decided all ten criteria by commands it ran, and left behind a test that fails if a
  future tidy-up discards ADR-0004's hand-rolled validation — a regression test protecting a
  *decision*, not just a behaviour.
- **Result:** the round trip is completing now: `answer-questions` answers from the record,
  updates the vision, and the item resumes at `in-review`.

---

## 2026-08-17 — META-070d — WI-0003 closed; a third gate defect found and codified

- **Unit:** META-070d
- **The run completed:** 6 items done, EP-001 closed a second time with **all seven** success
  measures re-run against the merged trunk — including the two-folder measure added when the epic
  reopened, which showed the two folders' outputs identical under `--sort name` and with no
  correspondence under count order. 244 lines of tool, 77 tests, nine ADRs, six questions asked
  and answered inside the record.
- **The third tooling defect, found and correctly solved by the run:** `review-close`'s procedure
  merges at step 8 and closes at step 9, but the `commits-reference-the-item` gate inspects
  `trunk..branch` — which is **empty once the branch is merged**. Merging first therefore makes
  the gate refuse the very close it was a precondition for.
  - What the run did: refused `--force` (it would stamp `[gates forced]` on a row whose gates are
    otherwise clean), **read how the five earlier items had closed**, found WI-0001's history row
    saying "closing before the fast-forward so commits-reference-the-item still has a range",
    rewound its unpublished trial merge, closed on the branch with the gate passing on a real
    range, and fast-forwarded afterwards. It solved it by consulting the record — which is what
    the record is for.
  - It also declined to file a bug under EP-001, correctly: the defect is in the methodology's
    tooling, and a bug there would describe something the linecount tracker does not own.
  - **Fix:** `review-close/process.md` step 8 now specifies the order the run discovered —
    trial-merge and test, discard the trial, close while the branch is still unmerged, then merge
    — and says why, ending "If you find yourself reaching for a gate override here, stop: you
    have merged too early." Bumped to v0.1.2. `check-commit-refs` now detects the
    already-merged case and prints that instruction instead of the misleading "nothing was
    delivered".
- **Acceptance C3 is now met with evidence, organically:**
  `| in-review | awaiting-answer | review-close | in-review | Q-001 blocking: D7 fails because
  vision.md still says --sort is not delivered, and review-close may not update it |` followed by
  `| awaiting-answer | in-review | answer-questions | — | Q-001 answered from the record;
  vision.md v3 records --sort as delivered; resumed at the recorded resume-to |`. Filed →
  suspended with `resume-to` → answered by the architect → document updated → resumed at exactly
  the recorded status.
- **Final imported state:** 7 items, 11 documents, `validate-workspace` 0 errors 0 warnings;
  six questions, five non-blocking and one blocking, all answered; nine statuses' worth of
  history including `awaiting-answer`; and **no `[gates forced]` row anywhere in the workspace**.
- **`./scripts/check`** passes with no skipped steps.
- **Result:** META-070d done.

---

## 2026-08-17 — META-071 — `meta/FINAL-REPORT.md`

- **Unit:** META-071
- **Inputs read:** `meta/plan.md` (the filled acceptance mirror), the whole of `meta/journal.md`,
  all five ADRs, `examples/toy-project/AUDIT.md`.
- **What the report says, and what it refuses to say:**
  - It leads with the six defects the toy run exposed, and states that four of them were **caused
    by this build** — two of them by fixes to earlier defects. That is the honest shape of what
    happened, and burying it would have made the report useless as input to the next iteration.
  - It names the most important finding in the whole build: **the review layers do not catch a
    plausible false claim.** Every machine-decidable gate held; every gate resting on a
    human-style read did not. The audit found a factually wrong justification propagated into
    five documents and passed by six review layers.
  - It states that the chronology in the paper trail is orderable but not accurate — a direct
    cost of my own clamp fix — and that independence is procedural rather than adversarial.
  - It lists the three specified paths that have never run, rather than implying full coverage.
  - It refuses the quality claim outright: the methodology guarantees the checks ran and the
    reasoning was recorded, which is a different and smaller thing than guaranteeing quality.
  - The first recommended iteration follows directly from the evidence: four of the audit's six
    findings were mechanically checkable and needed no judgement, so the machine-checkable
    perimeter should grow before anything else is deepened.
- **Gates:** `./scripts/check` — all steps passed, no skips.
- **Result:** META-071 done.

---

## 2026-08-17 — META-071a — the audit's second pass, and the Definition of Done gains D12/DE6

- **Unit:** META-071a
- **What the addendum found.** The sixth item's own record is the cleanest in the project — all
  ten criteria verified by running them, and this time **every numeric claim reconciles** (the
  `172 0` numstat, the 63-line diff, both commit counts), which the first pass had specifically
  faulted. The blocking question was judged a good one, honestly marked `blocking: true`, and the
  resume matched the recorded `resume-to` exactly. The epic's reopen was judged not only
  legitimate but *better handled than it had to be*: the record noticed §3.4 is written about
  defects while this was a feature, put the choice to the human rather than taking it, and
  **raised the epic's bar before re-clearing it** by adding a seventh success measure.
- **And then the finding that matters.** Three of the four corrections the auditor required after
  the first pass were **never made**, and the false `ls -b` justification **spread to a seventh
  document** — written *after* the audit raised it, by a skill that re-quoted the sentence rather
  than re-checking it. A record-completeness counting error the auditor had flagged on one item
  **recurred** on another.
- **The auditor's diagnosis, which is structural and which I accept:** the Definition of Done
  asks whether *this* change invalidated a document; **nothing asks whether something written
  three items ago is still true.** That absence is what let one wrong sentence survive two
  verifications, three reviews and two epic closures, and it is why every uncorrected finding in
  the project lives in prose rather than in behaviour.
- **The fix:** `spec/dor-dod.md` gains **D12** (every claim in `docs/` about the behaviour *this
  item touched* is still true, checked by reading it against the code) and **DE6**, its
  epic-level counterpart. D12 is deliberately scoped to the behaviour the item touched, so it is
  a real read of a few paragraphs rather than a ritual nobody performs. The spec records the
  audit that produced both.
- **Recorded in the final report, not softened:** D12 and DE6 have **not been exercised**. They
  are the right shape of fix and are currently untested prose about untested prose — which is
  exactly why the report's first recommendation is to make this class *mechanical* rather than to
  trust another checklist item. Four of the audit's six findings needed no judgement at all: they
  were unresolvable shas, an arithmetic error, and a repeated sentence whose wording had diverged.
- **Gates:** `./scripts/check` — all steps passed, no skips.
- **Result:** META-071a done.

---

## 2026-08-17 — mission complete

- **Final verification, all by execution:**
  - `./scripts/check` → 5 steps, **all passed, no skips**: library self-test, `lint-skills`, the
    44-code must-fail fixture, render determinism, and the must-pass example workspace.
  - A clean-room install into a brand-new empty git repository: 8 skills placed,
    `workspace-init` created the tree, `validate-workspace` returned 0 errors and the 2 expected
    warnings for an uninitialised project, and uninstall removed exactly what install added while
    leaving `tracker/` and `docs/` untouched.
  - 56 commits, every one referencing a META unit; working tree clean; `main` pushed.
- **`meta/BLOCKERS.md` is empty**, as PROMPT rule 7 expected. Nothing was impossible. Six things
  were wrong, and all six were found by running the methodology rather than by reasoning about it.
- **What I would tell the next session, in one line:** the eight skills are the deliverable, but
  the six defect reports in this journal are the evidence — each one a case where running the
  methodology contradicted the methodology, and the record said so instead of smoothing it over.
- **Result:** mission complete. `meta/CHECKPOINT.md` now says so and points at
  `FINAL-REPORT.md` §5 for what comes next.

---

## 2026-08-21 — META-072 — Phase H opens: the harness execution model

- **Unit:** META-072
- **Mission:** `meta/harness/HARNESS-PROMPT.md` — build the two-session iteration harness per
  `meta/harness/DESIGN.md`, prove it with one mini end-to-end iteration on queue entry 1, and do
  not touch `methodology/` or `spec/`. Toolkit defects go to `meta/findings/FINDINGS.md` as
  F-011 onward.
- **Read before writing anything:** `DESIGN.md`, `PROJECT-QUEUE.md`, `PROMPT.md`, `USAGE.md`,
  `CONSUMER-PROMPT.md`, `spec/question.md`, `spec/ids-and-statuses.md`, and the `intake`,
  `refine`, `answer-questions` and `next` procedures — the harness's async protocol has to be
  assembled out of paths those four already specify, or it is a toolkit change in disguise.
- **The pleasant discovery:** it can be. `intake` ("the human leaves mid-intake"), `refine`
  ("the human is not present"), `spec/question.md` §3 ("human answers in the file →
  answer-questions propagates") and `next` step 2 (a human-addressed question stops the loop)
  already compose into exactly the file-based turn protocol the harness needs. F-008 stays
  deferred; harness v1 needs no toolkit change, as `DESIGN.md` §5 predicted.
- **The unpleasant one, already visible on the page:** `answer-questions`' precondition 1 says
  "if every open question is addressed to `human`, you have nothing to do: report and stop" —
  which contradicts its own step 4 (`answered-by: human`) and the protocol diagram it implements.
  Taken literally it makes the answered-by-the-human case unrunnable. Not fixed here; queued for
  the findings unit and worked around in the worker turn prompt, which is harness-owned.
- **Verified by execution, not recalled** (`ADR-0005` §1): `claude 2.1.238` accepts `--max-turns`
  even though this build's `--help` omits it; `--output-format json` really does carry
  `permission_denials` and `total_cost_usd`; `stream-json` really does expose every `tool_use`
  input, which is what makes the contamination assertion an observation rather than a promise.
  Docs have moved to `code.claude.com`; the `docs.anthropic.com` map still 301s there.
- **Decisions recorded** in `ADR-0005`: turn zero belongs to the sim (otherwise the first worker
  turn has no idea to work on); the sim is caged to `Read,Write,Edit,Glob,Grep` so "writes only
  permitted files" is cheap to hold; the worker loses `AskUserQuestion` so it *cannot* ask a
  human who is not there; the throwaway root defaults outside `~/git` because
  `/home/msi/git/CLAUDE.md` would otherwise be auto-loaded into every worker turn.
- **Gates:** `./scripts/check` — all 5 steps passed, no skips.
- **Result:** META-072 done.

---

## 2026-08-21 — META-073 — `harness/provision.py`, and the trust discovery

- **Unit:** META-073
- **Built:** `harness/provision.py` and `harness/iterations/*.json` (one config per PROJECT-QUEUE
  entry: project name, persona, probe, turn budget, models). Provisioning is mechanical — git
  init with a repo-local identity (`agile-skills harness worker <worker@harness.invalid>`, so a
  worker commit is never mistaken for the owner's), the project `.gitignore` and
  `SIMULATION-NOTICE.md`, a copy of the real `CONSUMER-PROMPT.md`, the installer, `workspace-init`,
  the USAGE §4 allow-list, one commit.
- **Verified by execution, all four paths:** dry run prints and writes nothing; a non-empty
  stranger directory is refused with exit 2 and an explanation; the real run produced 55 files in
  one commit and `validate-workspace: 0 errors, 2 warnings` (both warnings are the documented
  post-init state — null test command, empty description); a second run committed nothing and
  left the tree clean.
- **Acceptance box "skills discoverable by a fresh session" — proved, not assumed.** A fresh
  `claude -p` in the provisioned project, told to use no tools, answered: `answer-questions,
  implement, intake, next, plan, refine, review-close, verify`. Eight for eight.
- **What that probe also printed, which matters more:**

      Ignoring 8 permissions.allow entries from .claude/settings.json: this workspace has not
      been trusted.

  A `-p` session never shows the workspace-trust dialog, and an untrusted workspace's
  `permissions.allow` is discarded **wholesale**. So USAGE §4's allow-list — the one setup the
  document recommends for "steady use" — has no effect in any headless run of a project the owner
  has not opened interactively at least once. That is a consumer-facing gap, and it is upstream of
  F-006: before asking whether one entry's syntax is right, the entries have to be honoured at
  all. Filed properly in the findings unit; `provision.py` gains an opt-in `--trust` that
  registers the project in `~/.claude.json`, and prints the caveat loudly when it is not passed.
- **Not fixed here:** `USAGE.md` is toolkit documentation and this session does not touch the
  toolkit. The finding carries the evidence.
- **Gates:** `./scripts/check` — all 5 steps passed, no skips.
- **Result:** META-073 done.

---

## 2026-08-21 — META-074 — the simulated-human skill

- **Unit:** META-074
- **Built:** `harness/skills/simulated-human/` — `SKILL.md`, three personas (`cooperative-pm`,
  `impatient-founder`, `contradictory-stakeholder`) and four probe scripts, one per
  PROJECT-QUEUE entry.
- **The split that matters.** `SKILL.md` holds what is true of every human (answer only what was
  asked; be terse; vagueness is legitimate; never contradict yourself unless the probe scripts
  it; never write engineering; never touch the machinery) and the mechanics of a turn. The
  persona holds character. The probe script holds this iteration's test plan. DESIGN §3's
  argument for files over prompt text is that a fresh turn loses prompt-borne persona
  instructions — so the turn prompt names the files and the skill reads them.
- **The one instruction I expect to earn its place:** the sim writes `[human] <answer>` into
  `## Answer` and changes *nothing else* — not `status`, not `answered-at`, not
  `## Consequences`. Marking the question answered and propagating it into the artifacts is the
  team's job, and whether they do it is one of the things the run measures. A helpful sim would
  quietly delete the measurement.
- **Planted-vs-organic tagging is in the skill, not only in the probes**, with the reason
  written next to the rule: the owner reading the run afterwards has to separate "hit the trap I
  set" (coverage) from "failed on its own" (defect), and an untagged answer makes that
  distinction unrecoverable. `[PLANTED: <probe id>]` / `[ORGANIC]`, and withheld answers are
  logged as actions in their own right.
- **Iteration 4's probe script is mostly a warning**: it plants nothing, and says so, because the
  boring run is the zero-bump gate rehearsal and a probe would destroy what it measures.
- **Gates:** `./scripts/check` — all 5 steps passed, no skips. (The sim is exercised by
  execution in META-076, when the driver can run a turn.)
- **Result:** META-074 done.

---

## 2026-08-21 — META-075 — the two turn prompts

- **Unit:** META-075
- **Built:** `harness/prompts/worker-turn.md` and `harness/prompts/sim-turn.md`, both versioned
  in a first-line comment so the iteration log can record which prompt produced a turn.
- **The worker prompt does not replace `CONSUMER-PROMPT.md`, it amends it.** The project carries
  a copy of the real consumer prompt and the turn prompt says "that document is your
  instructions", then adds six amendments and says the amendments win where they conflict. A
  harness that paraphrased the consumer prompt would be testing the paraphrase; the consumer
  prompt is one of the things under test.
- **The six amendments,** in the order they matter: (A) the human is not here — file questions
  through the question mechanism, batch every question you have this turn because each round trip
  costs a turn, never guess to avoid asking; (B) **consume the stakeholder's answers first**,
  before `/next`, or the turn accomplishes nothing — the orchestrator stops on any open
  human-addressed question, so an answered-but-still-open question deadlocks the pipeline;
  (C) everything you know must be on disk, because the next turn is a different session;
  (D) stay inside the project directory; (E) work until you actually stop, not until a milestone
  feels like a good pause — there is nobody to report to mid-turn; (F) write `HARNESS-STATUS.md`
  with a fenced JSON block, `stop_reason` from a fixed six-value set.
- **Amendment B carries the workaround for the `answer-questions` precondition defect** found in
  META-072: its precondition 1 reads as though the skill has nothing to do when every open
  question is addressed to `human`, which is exactly the state a human-answered question is in.
  The prompt tells the worker to do the job anyway and to say in the journal that it did — a
  harness-side workaround for a toolkit defect that this session may not fix, and the journal
  note means the run's own record will show the workaround being applied.
- **The status file is deliberately not trusted.** The prompt says so out loud: the driver reads
  the workspace too, and a status file that disagrees with the tracker is a finding.
- **The sim prompt is short by design** — the persona and probe live in files, and DESIGN §3's
  whole argument is that prompt-borne character is the first thing a fresh turn loses. It
  supplies only what changes per turn: project path, turn number, log path, persona and probe
  paths, and the job (`open` or `answer`).
- **Gates:** `./scripts/check` — all 5 steps passed, no skips.
- **Result:** META-075 done.

---

## 2026-08-21 — META-076 — the driver, and the audit it depends on

- **Unit:** META-076
- **Built:** `harness/run_iteration.py` (the driver) and `harness/audit.py` (the contamination
  boundary, made observable). The audit is a separate module because META-077 has to be able to
  feed it transcripts that must be *rejected*, and a check nested inside a driver loop cannot be
  tested that way.
- **The run directory is the deliverable of a run:** `state.json` (whose turn it is, and why it
  stopped), `iteration-log.jsonl` (one line per turn: command, prompt version, model, duration,
  tool count, cost, permission denials, the driver's observed status, the worker's self-report,
  and any violations), `SIM-LOG.md`, and every turn's full `stream-json` transcript plus its
  stderr. Rerunning the same command resumes from `state.json`; `--fresh` archives and restarts.
- **The driver never takes the worker's word for anything.** `scan_project` parses
  `tracker/items/*/item.md` and every question file itself, runs `validate-workspace`, and reads
  `git rev-parse HEAD`. The worker's `HARNESS-STATUS.md` is recorded beside it and compared: a
  disagreement prints a `!` line into the log rather than changing what the driver believes.
- **Stop conditions, all computed from disk:** validator failure; epic complete; unanswered
  human questions → the sim's turn; a `blocked` item with no question open to the human →
  `blocked-no-recourse` (there is nothing another sim turn could contribute); three consecutive
  turns with an identical workspace fingerprint → `stalled`; the turn budget; a failed turn; and
  a contamination violation, which stops the run immediately with the offending tool input in
  the log.
- **Verified by execution:** the opening sim turn ran for real against the provisioned scratch
  project — `exit=0, 22s, 5 tool calls, $0.04` on haiku. It read its persona and probe, wrote
  `IDEA.md` containing exactly the probe script's sentence and nothing else, appended a SIM-LOG
  entry, and the audit found no violations. The driver then stopped at `turn-budget` with
  `--max-turns 1`, which is the correct reason.
- **One defect the smoke test found in my own work:** the sim invented a timestamp
  (`2026-08-21T00:00:00Z`) because a headless session has no clock and I had not given it one.
  The sim turn prompt now passes `{{NOW}}` and says that a guessed timestamp is worse than none.
- **Gates:** `./scripts/check` — all 5 steps passed, no skips.
- **Result:** META-076 done.

---

## 2026-08-21 — META-077 — proving the contamination assertions can fail

- **Unit:** META-077
- **Built:** `harness/tests/test_harness.py`, 26 tests, and a sixth step in `./scripts/check`
  that runs them.
- **The point of the file, written at the top of it:** a contamination check that cannot fail is
  not a check. Every rule gets a transcript that must be **rejected** and one that must be
  **accepted** — `W1` reading the harness directory, `W2` naming a token only harness content
  contains, `W3` escaping the project (by `~`, by absolute path, by a sibling throwaway
  project), `W4` a change appearing in this repository while a turn runs, `S1` a sim write
  outside its three permitted paths, `S2` a sim reaching for a shell or an agent, `S3` a sim
  closing or deleting a question on disk.
- **The accepted cases matter as much:** an ordinary worker turn (board-gen, reading an item,
  writing source, committing, running pytest) must produce **nothing**, and so must a sim that
  fills in `## Answer` and appends to its log. A rule that fires on honest work would be turned
  off within one iteration.
- **Two defects in my own audit, found by writing the tests:**
  1. `_resolve` expanded `~` with the *auditor's* home, so a transcript from another machine —
     or a test fixture pretending to be one — silently escaped the check. Home is now a
     parameter: `~` means the audited session's home, not mine.
  2. The first version of the `W4` test asserted `all(v["rule"] == "W4" ...)` over a list that
     is empty when this repository happens to be clean — a test that passes vacuously and would
     never have caught a broken rule. It now builds a real git repository in a temp directory,
     dirties it, and requires the violation, including the file name in the evidence.
- **Three tests are about drift rather than contamination:** `provision.ALLOW_LIST` must still
  equal the JSON block in `USAGE.md` §4 verbatim (if the owner's advice to consumers changes,
  the harness's setup has to change with it, or the run stops being evidence about the
  documented path); every iteration config must name a persona and probe file that exist; and
  both turn prompts must carry a version and leave no `{{PLACEHOLDER}}` unfilled.
- **Gates:** `./scripts/check` — 6 steps, all passed, no skips.
- **Result:** META-077 done.

---

## 2026-08-21 — META-078 — the restart, and the orphan it exposed

- **Unit:** META-078
- **Done by execution, not by reasoning:** started a run, `SIGKILL`ed the driver nine seconds
  into the sim's opening turn, reran the same command. Evidence committed at
  `meta/harness/evidence/restart-test/`.
- **What the kill exposed, which I had not designed for:** `SIGKILL` on the driver does not
  reach the `claude` process it started. The orphan kept running and kept writing into the
  transcript of a turn nobody was waiting for, and a resumed run would then have had **two agent
  sessions in the same project at once** — the one thing a pipeline whose entire state is on
  disk cannot survive. Fixed three ways: each turn records its child's pid in `turn.pid` and a
  resuming driver kills whatever is still breathing (`"reaped-pid": 220639` in the log);
  `SIGINT`/`SIGTERM` now take the turn down with the driver; and a `driver.pid` lock refuses a
  second driver on the same iteration outright.
- **The resume itself behaved as designed:** it re-ran the interrupted turn rather than skipping
  it, which is only safe because every pipeline skill reconciles with what it finds on disk —
  the harness is a direct consumer of that guarantee, as `DESIGN.md` §2 claims. Turn 1 re-ran
  (43s, $0.05), turn 2 ran (479s, $0.89), the run stopped at `turn-budget`, and the project
  validated at **0 errors** with two honest warnings and two clean commits.
- **A second thing the run proved early, on haiku of all models:** the async human protocol
  works. `intake` created `EP-001`, filed `Q-001` addressed to `human`, committed the tracker,
  and reported `stop_reason: human-question-open` in `HARNESS-STATUS.md` — the exact handshake
  the harness is built on, from a model chosen for being cheap rather than good.
- **A false-positive trap I closed while I was in there:** `W4` ("the repository changed during
  a turn") originally fired on *any* new dirty line, so the owner editing `meta/` while a run was
  in flight would have stopped the run for contamination. It is now scoped to the toolkit under
  test — `methodology/`, `spec/`, `adapters/`, `scripts/`, `examples/`, `fixtures/` and the
  consumer-facing documents. A turn reaching into `harness/` is still caught by W1/W2 from the
  transcript, where that check belongs. A rule that fires on the owner's own typing is a rule
  that gets switched off within one iteration.
- **Gates:** `./scripts/check` — 6 steps, all passed, no skips.
- **Result:** META-078 done.

---

## 2026-08-21 — META-079 — `harness/USAGE.md`

- **Unit:** META-079
- **Built:** `harness/USAGE.md` — prerequisites and what an iteration costs, provisioning
  (including why `--trust` exists), running and resuming, the run directory's contents, how to
  read a run, how to adjust the human between iterations, the contamination rules as a table,
  what to do after an iteration, and every stop reason with what it means.
- **The section I care most about is §5, "reading a run", and its order:** board first (where
  the work got to), then `SIM-LOG.md` — because that is where `[PLANTED:` and `[ORGANIC]`
  separate coverage from defect, and a finding filed without checking which one you are looking
  at is worse than no finding — then the iteration log, then the item trail. The last line says
  the thing the whole harness exists to make possible: the harness proves the pipeline ran; only
  the trail shows whether it ran honestly.
- **§9 is written from the stop reasons the driver can actually emit**, not from imagined
  failures: `turn-failed`, `blocked-no-recourse` (and the instruction to check SIM-LOG before
  treating it as a defect), `stalled`, a status file that disagrees with the tracker, and a hung
  turn.
- **Not yet verified.** This document is written to be followed literally in META-080, and
  whatever it gets wrong there gets fixed there. Writing it first is deliberate: a usage
  document written after the run describes what happened, not what the reader must do.
- **Gates:** `./scripts/check` — 6 steps, all passed, no skips.
- **Result:** META-079 done.

---

## 2026-08-21 — META-080 — the mini end-to-end iteration

- **Unit:** META-080. Evidence: `meta/harness/evidence/iteration-1-mini/`.
- **Eight turns, $48.51, stopped deliberately at the turn budget** once the acceptance targets
  were met. Two of three work items are still open; the rest of iteration 1 belongs to the owner.
- **Every acceptance target met:** intake and refinement completed through the async protocol
  (16 questions filed to the human across three worker turns, every one answered in the question
  file by the sim and propagated by `answer-questions`); **WI-0001 reached `done`** and merged;
  **both** planted probes consumed and tagged; and all eight transcripts audit clean. The
  workspace ends at **0 errors, 0 warnings**.
- **The result I did not expect:** `in-review → in-progress` — the review send-back, listed in
  `meta/FINAL-REPORT.md` as never executed — fired **three times, organically**. `review-close`
  rejected WI-0001 for a dead function and a duplicated rule, and later for an AC8 violation that
  **two `verify` passes had missed**: a store whose people list held a non-string parsed cleanly
  and then raised `AttributeError` past `cli.main`'s `except ExpensesError`. The reject → fix →
  re-verify loop did real work rather than ceremony. That single fact justifies the harness more
  than anything I built into it.
- **Six toolkit findings, every one found by the worker rather than by me** (F-011, F-013 through
  F-018). The worker journalled each where it happened and repeated them in its status report;
  I reproduced F-013 (an epic cannot be suspended: `transition: open → awaiting-answer by
  'intake' is not a transition in pipeline.yaml`) and confirmed F-014 by reading the code. That
  is the harness working exactly as `DESIGN.md` intends: I did not have to notice anything.
- **Two contamination false positives, both mine, both fixed with a regression test:**
  1. `W3` matched paths quoted *inside a document the worker was writing* — a question whose
     `## Context` repeated the stakeholder's own example folders (`~/trips/ski`, `~/flat`). Fixed
     by distinguishing a path given as a tool *argument* (the session meant it; the parent
     existing is enough) from one *scraped out of a command string* (require the path itself to
     exist).
  2. `W3` then matched a bare `~` — `tr '\n' '~'` — and a markdown `~~strikethrough~~`. The
     tilde form now requires a following slash.
  Both cost a stopped run. The lesson is in the code comment: a check that fires on quoted text
  gets switched off, and then it checks nothing.
- **`--reaudit` exists because of the first one.** The recovery from a contamination stop must
  not be "edit `state.json` by hand": it is to fix the rule, re-audit the transcripts still on
  disk, and resume **only** if they come back clean — and to re-derive the next turn from the
  workspace, because a contamination stop happens before the turn's decision is taken and
  resuming without that repeats a worker turn that already ran, at full price. I learned that the
  expensive way, once.
- **A defect in my own worker prompt, reported by the worker:** amendments A ("batch every
  question before you stop") and E ("stop when a human question is open") cannot both be obeyed
  literally, because the orchestrator stops on the first question filed. The worker resolved it
  correctly on its own and journalled why. Also, `stop_reason` has no value for "the per-turn
  budget ran out", so two clean turns had to report `error` and explain in prose. Both recorded
  as H-001; fixed in META-081, not mid-run.
- **Gates:** `./scripts/check` — 6 steps, all passed, no skips.
- **Result:** META-080 done.

---

## 2026-08-21 — META-081 — findings, the harness's own fixes, and the report

- **Unit:** META-081
- **Filed:** F-011, F-012, F-013, F-014, F-015, F-016, F-017, F-018 in
  `meta/findings/FINDINGS.md`, each with the evidence that produced it. Seven of the eight came
  out of the mini run, and all seven were found by the **worker**, not by me — which is the
  clearest statement of what the harness is for.
- **F-006 is now rejected, with its reason.** The suspected allow-list entry
  `Bash(python3 .claude/agile-skills/scripts/*)` matches correctly: a `dontAsk` session ran the
  command with `permission_denials: []`, and a control command the list does not cover was
  denied in the same session shape — so the probe could have failed and did not. Its symptom was
  F-012 (an untrusted workspace's allow-list is discarded) all along. A finding closed by
  execution rather than by argument is worth more than one left open out of caution.
- **Fixed the two defects in the harness itself**, both reported by the worker in its own status
  file: the worker turn prompt is now **version 2**, reconciling "batch every question" with
  "stop on the first open one" — file the escalations you can already state before you end the
  turn, because filing a letter is not dispatching work — and the `stop_reason` enum has
  `turn-budget-exhausted`, so a turn that ends cleanly at its spend cap stops having to report
  `error` and explain in prose that nothing failed.
- **Wrote `meta/harness/FINAL-REPORT.md`**, including the two things I would rather not have had
  to write: the contamination audit stopped two real runs on false positives of my own making,
  and the harness is not cheap ($48.51 for eight turns), with a per-turn spend cap being a false
  economy because the next turn re-reads the whole project.
- **Final verification:** `./scripts/check` — 6 steps, all passed, no skips.
  `git diff --stat c9a62fb..HEAD -- methodology/ spec/` is **empty**: the toolkit was not touched,
  which was the condition the mission put on the whole exercise.
- **Result:** META-081 done. Phase H complete.

## META-083 — F-019: the record can no longer diverge from the status undetectably

The finding named three mechanical fixes and all three shipped.

**Root resolution.** `scripts/lib/workspace.py` gains `find_workspace_root()` (walk up to
`tracker/project.yaml`) and `resolve_root()`. Every script defaults its root to it. The decision
worth recording is what an *explicit* path now means: it is used verbatim, never walked up from.
`workspace-init` and the "you have not initialised this yet" validator run both need to name a
directory that is not a workspace yet, and a helpful walk-up would turn "this directory is
empty" into "here is your parent's workspace, silently". Only the implicit case searches. When
the search lands somewhere other than the working directory the script says so on stderr —
resolving quietly would trade one invisible behaviour for another.

**The checkpoint rule.** `spec/skill-contract.md` §2.3. Two rules, both written because a run
broke them: a transition is issued alone and its exit code read before the journal entry that
asserts the move; commands are invoked by a path that does not depend on CWD, and you never
`cd` to run one. The adapter renders both into every SKILL.md, because the spec is the file a
worker reads least and the SKILL.md is the one it reads first.

**The cross-check.** `journal.status.unmatched`: every transition a journal entry claims under
`**Status:**` must exist as a row in `history.md`. Parsing that bullet is the interesting part —
it is deliberately prose, and the toy project alone contains chained claims
(`planned` → `in-progress` → `verifying`), parentheticals (`(unchanged)`, `(outcome delivered)`)
and epic-level entries that speak about two items in one line. `status_claims()` reads backticked
tokens from the head of each `;`-separated clause, skips clauses naming a different item, and
consumes history rows so a repeated transition needs a repeated row. The toy project — 7 items,
every one of those shapes — stays at 0 errors, which is the evidence the parser is not simply
lenient.

Direction not taken: the reverse check (a history row with no journal entry declaring it) is
*already* covered per-skill by `journal.execution.missing`, and per-row it would fire on every
legitimate multi-transition entry. F-019's direction is the one the record could not see, and
that is the one now checked.

Spec files carry no version header, so rule 2 of the session mission has no literal target. Each
spec file this session changes gains a `## Revisions` table instead, appended to, and the
mission's intent — a spec change is dated and attributed to a finding — is met. Recorded here
rather than as an ADR because it changes no behaviour.

Evidence: `./scripts/check` green — 45 fixture codes, 183 selftest cases.

## META-084 — F-017: a journal header no skill can invent

The finding's addenda are three specimens of one class: the fields with nothing behind them get
made up. A test result has an exit code, a decision has an artifact, a commit has a sha — a
timestamp, a version and a persona have only the honesty of whoever typed them, and across four
runs that turned out not to be enough. Run 1c's eleven entries narrating a next-morning half-day
for work done the previous night is the sharpest specimen: a timeline audit of that journal would
have "proved" work happened while nothing was running.

**`scripts/journal-entry`.** The caller supplies bullets; the script writes the heading. The
timestamp is this machine's clock, the version and persona are read from the acting skill's
installed `skill.yaml`. It refuses a body that contains a heading of its own, refuses one missing
any of the ten required bullets, and refuses one whose `**Item:**` names a different item.
`--template` prints the shape. `--restamp-last` is the journal's half of the sanctioned repair
`history.md` already had — F-017's first sentence, and the reason it is a *deadlock* rather than
merely untidy.

**`transition --journal-body-file`.** The row and the entry are written by one command, and the
script writes the `**Status:**` bullet itself from the move it just made. A caller cannot
mis-state it — demonstrated by handing it `draft → banana` and getting `draft → ready` in the
file. Ordering inside the command is history row first, then entry: a row with no entry is caught
by `journal.execution.missing`, while an entry with no row is precisely the direction the record
was blind to until META-083.

**The validator.** `check_clock` applies to both files. A stamp later than now (plus two minutes
for a skewed clock) is `*.timestamp.future`; a stamp outside the workspace's own git activity,
widened a day at each end, is `*.timestamp.outside-activity`. The git window is deliberately
generous — a workspace is written to before its first commit — because the failure being caught
is nine hours out, not nine minutes. Separately, `journal.version.impossible` fires when a
heading claims a version higher than the installed contract.

The version rule is asymmetric on purpose, and this is the one place the fix is weaker than the
finding. Run 1b recorded `review-close v0.1.0` while 0.1.2 was installed — *lower*, not higher —
and a validator cannot tell that apart from a legitimate old entry written before an upgrade,
because the record is meant to span versions. So the low-version case is prevented at the point
of writing (the script reads the file) rather than detected at rest, and only the impossible
direction — a version that does not exist yet — is an error. Said plainly rather than papered
over: a worker that ignores the script and hand-writes an old version string is not caught by
this check.

Fixtures: three new entries, each the shape of a real specimen — a 2099 heading with v9.9.9, a
1999 heading from before the repository existed, and a 2099 history row. The fixture also
started firing `journal.order`, a rule that had no coverage before; it is now listed. 50 codes.

Evidence: `./scripts/check` green; the scratch-workspace demonstration recorded in FINDINGS.

## META-084b — F-017 adoption: no skill describes writing a heading by hand any more

Seven `## Journaling` sections gained the same block — write the bullets to a file, let
`journal-entry` stamp the heading, and when the entry accompanies a status change pass the file
to `transition --journal-body-file` instead of running two commands. `next` is exempt because it
journals nothing on an item, by design.

The step titles moved with it. Six skills read "**Journal, then transition**", and
`spec/skill-contract.md` §2.2 mandated exactly that order — journal first, transition second,
with the reasoning that a status advance without a record is a silent gap while a record without
the advance is merely a repeated run next time. That reasoning was sound in the abstract and
wrong in practice: F-019 is a run that fell into the gap between the two commands and left a
record asserting a move that never happened, and nothing could see it. §2.2 (revision 3) now says
the entry is written *in the same command as* the transition, which removes the gap rather than
choosing which side of it to fail on.

`intake` also lost its "then append `— → open` to the epic's history.md" instruction. That row is
`new-item`'s work — it creates the item at its opening status and writes the row — and telling a
skill to append a history table row by hand contradicts the guard hook that denies exactly that.

Seven patch bumps: intake 0.1.2, refine 0.1.2, plan 0.1.2, implement 0.1.1, verify 0.1.2,
review-close 0.1.3, answer-questions 0.1.2.

Evidence: `./scripts/check` green after re-render.

## META-085 — F-018: the guard decides on the target, not the sentence

The old Bash branch asked two questions — does the command string contain a guarded path, and
does it contain anything redirect-shaped — and denied when both were true. That denies
`cat tracker/board.md > /tmp/x` and `grep -n WI-0003 tracker/items/*/history.md > /tmp/out`,
which are reads, and it misses `cp /tmp/fake.md tracker/board.md`, which is a write. Both errors
come from the same place: it was matching prose.

It now lexes the command with `shlex` keeping punctuation, splits on the operators, and asks each
simple command what it *writes to* — redirection destinations, and the argument positions of the
mutating programs it knows, following `sudo`/`env`/`xargs` through to the real one. `sed` and
`perl` count only with an in-place flag; input redirection and heredoc sources are not targets.

The policy that anything unparseable is allowed is unchanged and is now covered by a test, because
it is the rule most likely to be "tidied" later by someone who reads it as a hole. It is not: a
guard that blocks on confusion is a guard the agent routes around, which is the same failure F-018
describes by a different door.

`adapters/claude-code/hooks/test_guard.py` is a new step in `./scripts/check` — 30 cases, 15
must-deny and 15 must-allow, and it fails outright if either side of the table is empty (a
must-allow-only table would pass against a guard that does nothing). The must-allow side is seeded
with F-018's own examples. Run against the **previous** guard the table fails 7 cases, in both
directions, which is the evidence that the fix is a fix and not a rewording.

Evidence: `./scripts/check` — 7 steps, all passed.

## META-086 — F-001: claim provenance, mechanized as far as it goes

F-001 is the thesis finding, so it deserves a report on what was actually achieved rather than a
tick.

**The rule chosen, and why that one.** "A factual justification must cite an artifact" is not
machine-decidable — deciding which sentences are factual justifications is the hard part. What is
decidable is a narrower shape, and the narrower shape happens to be the one that failed: an
**absolute** claim about a **named code object**. The specimen in the audit was literally "no
environment beyond `EXPENSES_STORE`". Absolutes are cheap to write, expensive to verify, and
catastrophic when wrong; hedged prose is not the failure mode and is deliberately not targeted.
Calibration: over the toy project's docs the rule fires 41 times, and the flagged paragraphs are
things like "Nothing recurses. `list_files` looks only at the entries directly inside the folder"
— the real class, not noise.

**Resolution is the part that cannot be faked.** Seven citation forms, each looked up in the
workspace: a path that must exist, an item that must exist, an AC that item must actually
declare, a question file, an ADR number, a commit `git cat-file` must find, or a command with a
recorded outcome. A citation that does not resolve is reported everywhere, at any time, by
`validate-workspace` — because unlike the absolute-claim rule it is wrong *today* regardless of
when it was written. `scripts/lib/claims.py` holds the one implementation, shared by the gate and
the validator, because two would eventually disagree and the disagreement would present as a gate
passing on a record the validator rejects.

**Unskippable, in this system's sense.** `claims-are-sourced` is a hard gate on `plan`,
`implement` and `review-close`, so `transition` refuses each skill's completion move while it
fails. `--force` remains and remains recorded in the history reason forever — that is the design,
not a hole: an override that leaves no trace is the thing being prevented.

**Two fixtures, on purpose.** The must-fail fixture proves the linter can fail. `fixtures/
sourced-claims/` proves it can be *passed*, by prose a person would write, and includes a hedged
paragraph that correctly needs no citation. A rule nobody can satisfy is not a rule; it is a
rule everyone forces.

**What was not achieved.** The direction's second half — "judge is a fresh subagent with a narrow
rubric and access only to cited evidence, not the prose" — is not implementable from a shell gate.
It ships as `review-close` step 9a: list the absolute claims the work touched, open what each
cites, decide from what is there. That is an instruction, and instructions are precisely what
F-001 says do not hold. Two things changed anyway: the input is now mechanically guaranteed (the
citations exist and resolve), and the question is far narrower than "is this document still
true". The honest summary is that the provenance half is a program and the judging half is a
better-aimed instruction. Iteration 1d will show whether the gate fires on real prose or gets
forced.

Version bumps: plan 0.2.0, implement 0.2.0, review-close 0.2.1 (a new gate is minor; step 9a is
the patch on top).

Evidence: `./scripts/check` — 8 steps, all passed, 51 fixture codes.

## META-087 — F-013: an epic can be suspended, because `terminal` was two questions

The finding lays out three rules that cannot all hold and asks which gives. The answer turned out
to be none of them: the contradiction was in a field name. `terminal` was being asked to answer
"does the pipeline advance an item out of this status by itself?" — which for an epic at `open` is
no, it advances through its children — and separately "may a blocking question or an impasse stop
an item here?", which for an epic is emphatically yes. One boolean, two questions, and the answers
differ.

So statuses now declare `suspendable` as well, and the two escalation transitions read
`from: any-suspendable`. `open` stays `terminal: true` — it genuinely has no owning skill, and
`lint-skills`' "every non-terminal status needs an owner" rule stays intact, which is the
give-away that the original flag was measuring ownership rather than suspendability all along.

`pipeline.status.unsuspendable` is the new lint rule, and it is the finding written as an
invariant: a status that is not suspendable must be an escalation target (`awaiting-answer`,
`blocked`) or a closed status (`done`). Anything else is a place an item can sit with work
outstanding and no legal way to stop. Flipping `open` back to `suspendable: false` makes it fire,
which is how I know it would have caught this.

Proven by execution rather than by reading. In a scratch workspace, the exact command F-013 quotes
as refused now writes its row; `awaiting-answer → open` resumes the epic to the recorded
`resume-to`; and `done → awaiting-answer` is still refused with the identical message, so the fix
opened one door and not the corridor. A fixture row carries the still-illegal case.

`intake`'s escalation instruction — "set the epic to `awaiting-answer` and stop" — needed no
change. It was correct all along; it was the machinery that could not carry it out.

Evidence: `./scripts/check` — 8 steps, all passed, 51 fixture codes.

## META-088 — F-022: an epic cannot close without having asked

The finding is short and the fix is mostly spec, so the interesting parts are the two decisions
that could have gone the other way.

**The gate checks that the question was asked, not that the answer was yes.** A stakeholder who
declines still closes the epic — with an outcome recording that it was not accepted, or by leaving
it open with follow-up items. Requiring a favourable answer would turn the acceptance moment into
a formality with only one legal outcome, which is what it was already. What is now impossible is
closing while never having asked.

**The sign-off must be filed after the last child closed.** This is the condition that does the
real work, and it comes straight from 1c: that run *did* obtain explicit consent for a mid-epic
redesign, three items before closure. Without the recency condition, that consent would satisfy
the gate for work the stakeholder had not seen — the same failure by a slower route. So
`check-epic-signoff` reads the children's histories for the latest transition to `done` and
refuses anything filed before it.

Mechanically: `spec/question.md` gains an optional `kind` field with `sign-off` as its one
non-default value, and specifies the shape — the goal restated in the stakeholder's words, what
was and was not delivered with a line of why for each, and three real options rather than "yes".
`spec/dor-dod.md` DE7 is `[auto]`. `scripts/check-epic-signoff` is a hard gate on `review-close`,
so `transition` refuses the epic's completion move. `review-close` step 10 files the question,
suspends the epic to `awaiting-answer` with `resume-to: open`, and stops — a move that was
impossible until META-087, which is why F-013 and F-022 are the same cluster.

Two fixtures. The broken one carries both near-misses: a sign-off with its `kind` misspelled
(which sails past a `kind == "sign-off"` check) and a correctly spelled one that the *architect*
answered on the stakeholder's behalf. The passing one is a captured scratch run rather than
hand-authored prose, so its history rows and timestamps are ones the tools actually produced.
Both are steps in `./scripts/check`, one expecting failure and one expecting success.

`review-close` → 0.3.0. Evidence: `./scripts/check` — 10 steps, all passed, 53 fixture codes.

## META-089 — F-021: a channel the stakeholder opens

Every channel the methodology had is opened by a skill: a question is the pipeline asking, an
answer is the reply, a sign-off is the pipeline asking one last time. Run 1b's sim held a new
requirement across two turns and wrote in its own log that no question gave it a vehicle to raise
it, then watched the epic close without it. That is not a stakeholder being shy; it is a protocol
with no inbound direction.

`spec/request.md` is that direction: `tracker/requests/R-###.md`, `from: human`, filed at the
workspace level rather than under an item. The placement is the design decision worth recording —
a stakeholder does not know which item their thought belongs to, and asking them to file it in the
right place is asking them to do `intake`'s job before `intake` has looked at it.

Three rules I want to be able to point at later:

- **`## Request` is never edited by a skill.** It is the only record of what was actually asked
  for, in the words it was asked in. A skill that thinks the framing is wrong says so in
  `## Response`.
- **Declining is a first-class outcome.** A request outside scope, or contradicting a decision
  the stakeholder themselves recorded, is declined in writing with the reason and with what would
  have to change. Silently absorbing a request and silently dropping one are the same failure;
  the artifact exists to make both visible.
- **A request suspends nothing by itself.** If acting on it invalidates an item that is
  mid-flight, `intake` files a blocking question on that item and the ordinary suspension rules
  run. Letting a request reach into a running item would put a second writer on its status.

Routing is orchestrator step 2 — after validation, before surfacing questions and well before
selecting work. A request handled once the current item finishes is a request answered against a
plan the stakeholder has already tried to change.

One practical note for iteration 1d: the simulated human has `Write` and no shell, and a request
is a file. So this is a channel the sim can actually use, which questions-only never was.

Versions: pipeline 0.3.0, next 0.2.0, intake 0.2.0. Evidence: `./scripts/check` — 10 steps, all
passed, 62 fixture codes.

## META-090 — cluster 3: four defects the worker found by running into them

**F-011** was a sentence. `answer-questions`' precondition 1 said "there is at least one open
question addressed to `architect`; if every open question is addressed to `human`, you have
nothing to do" — which told the only skill that can consume a human's answer that it had nothing
to do, because an answered human question is still `open` and still `addressed-to: human`. `next`
stops on any open human-addressed question, so one unconsumed answer stopped every subsequent turn
forever. The precondition now defines *answerable* and names both shapes. The harness prompt's
amendment B existed solely to talk the worker past that sentence; it is deleted, and in its place
a note says that if a future run gets stuck there, the contract regressed. Deleting a workaround
is the part of a fix that is easy to skip and that proves it landed.

**F-014** — I took the finding's second option and its "say which" literally. `transition` tells
its gate run which move is pending, and the validator downgrades to *warnings* the findings that
move resolves, scoped to the moving item, printing how many and why. Downgrading rather than
suppressing matters: the findings are still in the output, still readable, and a run that
downgrades something surprising is visible. The set is deliberately tiny — board staleness for any
move, the two suspension codes for moves in and out of suspension — because a generous list would
turn the gate into a rubber stamp on exactly the path where the record is most fragile.

I did not take the first option (validate the post-move state) because applying the move to
validate it and rolling back on failure means truncating an append-only file, which is the act the
write guard exists to forbid. Choosing the weaker-looking option to preserve a stronger invariant
is worth recording.

**F-015** dissolved into META-084b's mechanism: `implement` step 3 now moves to `in-progress` and
writes its opening entry in one command. The skill legitimately writes two entries because it
makes two transitions, and saying so in the contract removes the ambiguity that made "journal at
the end" look correct.

**F-016** needed a decision, not a mechanism. Epic-level record commits go on the trunk: an epic
has no branch, outlives every item under it, and is changed by executions that are not about any
one child. `check-commit-refs` now *diagnoses* the case instead of merely reporting it — an
offending commit naming a different item is called out as an epic commit on the wrong branch, with
the sentence the worker who found this most needed: this gate is failing for an item that did
nothing wrong.

Versions: answer-questions 0.1.4, implement 0.2.1, review-close 0.3.1, worker-turn prompt 3.
Evidence: `./scripts/check` — 10 steps, all passed.

## META-095 — harness H-002 and H-003: resume means resume, fresh means fresh

Correction to META-090, recorded here because the rule was explicit: the worker-turn prompt edit
that deleted F-011's workaround went into the toolkit commit rather than a harness one. It was
inseparable from the contract fix — the workaround exists only because the contract was wrong —
but the two-ledger rule said otherwise and I did not split it. Noting rather than rewriting.

**H-002.** The driver treated every stop the same, so a turn killed by `--turn-timeout` was as
final as a finished epic, and the only offered exit archived four turns of good work. The
distinction that was missing is not "which reasons are bad" but *what a stop is a statement
about*: a killed turn or an API refusal says nothing about the work — the workspace is intact,
the trail is intact — while `epic-done` and `stalled` are verdicts on the run. So the tables are
`RESUMABLE_STOPS` and `TERMINAL_STOPS`, a resumable stop clears itself on a plain rerun with a
logged `resume-after-stop` event, and the terminal message finally says what `--fresh` archives.

Two smaller things fell out. A killed turn is now `turn-timeout` and an API refusal is
`api-rejected`, instead of everything being `turn-failed` — the iteration log can now answer "why
did this stop" without opening a transcript. And `looks_api_rejected` is deliberately a generous
text match: a false positive offers a resume to a turn that will fail again immediately and
visibly, while a false negative declares the run finished because a subscription limit was
reached at minute forty.

The test I care about most is the one that greps the driver's own source for every
`self.stop("...")` and fails if either table has missed one. The way this regresses is not a
mis-classified reason; it is a *new* reason nobody classifies, silently defaulting to terminal.

**H-003.** `provision.py --wipe`. The flag deletes a directory, so it refuses twice: the target
must carry `.harness/provision.json`, and it must be strictly inside the throwaway root. Neither
refusal is theoretical — the first stops a wipe landing on a directory somebody else made, the
second stops a mistyped `--root` turning this into a general-purpose delete. `--dry-run` deletes
nothing, and there is a test for that too.

USAGE §3 now carries the two-row table that would have prevented the confusion: `--fresh` for a
new run over whatever the last one built, `--wipe` then `--fresh` for a genuinely fresh start.

Evidence: `./scripts/check` — 10 steps, all passed; harness self-test 38 tests.
