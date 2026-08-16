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
