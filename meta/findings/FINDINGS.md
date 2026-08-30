# Findings — input backlog for builder session 2

Convention: F-### sequential, never reused. Every finding cites evidence in
`evidence/` or in this repo. Status: open | fixing | fixed (with commit) | rejected (with reason).

---

## F-001 — Judgement gates don't hold; make claim-checking mechanical
- Severity: structural (top priority)
- Component: methodology (review-close, plan), spec
- Symptom: every machine-decidable gate held in the toy run; every human-style
  judgement gate did not. A factually wrong justification reached source
  comments, an ADR, the architecture overview, and spread to a 7th document
  after the audit flagged it. D12/DE6 were added in response but are themselves
  unexercised.
- Evidence: meta/FINAL-REPORT.md (§ weaknesses, recommendation 1);
  examples/toy-project/AUDIT.md
- Direction: claim provenance — factual justifications in ADRs/docs must cite
  an artifact (test output, command result, requirement line); a linter fails
  unsourced justifications. Where judgement is unavoidable, judge is a fresh
  subagent with a narrow rubric and access only to cited evidence, not the prose.
- Status: fixed (commit 77c8f64) — the provenance half is mechanical; the judging half
  is narrowed but still instruction-shaped, said plainly below.
  **Mechanical.** `spec/doc-header.md` §4a (revision 2) defines the convention: a paragraph
  making an absolute claim (`no`/`never`/`only`/`every`/`cannot`/`exactly`/…) about something
  named as code must carry an inline `[src: ...]`, and every citation must resolve. Seven
  citation forms, each looked up: workspace path, item, `ITEM ACn`, `ITEM/Q-nnn`, ADR number,
  commit sha, and `run: <command> → <outcome>`. `scripts/lib/claims.py` is the single
  implementation; `scripts/lint-claims` is the gate and `scripts/validate-workspace` enforces
  the resolution rule over a workspace at rest (`claim.citation.unresolved`).
  **Unskippable.** `claims-are-sourced` is a **hard** gate on `plan`, `implement` and
  `review-close` (minor bumps to 0.2.0), so `transition` refuses each skill's completion move
  while it fails; `--force` still exists and is still recorded in the history reason forever.
  Scoped with `--changed-since {{trunk}}`, the same scoping D7 and D12 already use.
  `spec/dor-dod.md` D12 and DE6 are now `[skill] + [auto]`.
  **Fixtures, both directions.** `fixtures/broken-workspace/docs/architecture/overview.md`
  carries F-001's own sentence with a citation that does not resolve, and a second paragraph
  with an absolute claim and no citation at all. `fixtures/sourced-claims/` is the counterpart —
  prose a person would actually write, every claim cited, **0 findings** — because a rule nobody
  can satisfy is not a rule. Both are a new step in `./scripts/check` (now 8 steps).
  **Calibration evidence.** Run over the toy project's docs the rule reports 41 unsourced
  absolutes, and spot-checking them they are the real class, not noise: "Nothing recurses.
  `list_files` looks only at the entries directly inside the folder", "Only `main` knows what
  `--top` is". That is the sentence shape the audit found propagating.
  **What is NOT mechanical, stated plainly.** The second half of the direction — a fresh judge
  reading only the cited evidence — is `review-close` step 9a: list each absolute claim the work
  touched, open what it cites, and decide from what is there rather than from the sentence or
  from a document repeating it. It is an instruction, so it is exactly the kind of gate F-001
  says does not hold; what changed is that it now has a mechanically-guaranteed input (the
  citations exist and resolve) and a much narrower question to answer. Running it in a fresh
  subagent with tool access limited to the citations is not implementable from a shell gate and
  is not claimed here.

## F-002 — workspace-init creates empty dirs git can't track
- Severity: correctness, ship-blocker for open-source
- Component: scripts/workspace-init (+ validator)
- Symptom: six empty directories, no .gitkeep → "commit the workspace" (USAGE §3)
  silently commits only tracker/project.yaml; a fresh clone fails validation
  with items.missing.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.1
- Direction: workspace-init writes .gitkeep in each dir; validator message for
  the fresh-clone case.
- Status: fixed (commit 20fc6a7), together with F-047 — the rule is that **the tool that creates a
  directory the schema requires also creates its `.gitkeep`**, which means `workspace-init` and
  `new-item` both. `tracker/` and `docs/` are excluded because they always end up holding
  something. Demonstrated end to end: `workspace-init` in an empty repo, `git add -A`,
  `git commit`, `git clone`, and the clone reports **0 errors** — F-002's exact symptom, gone.

## F-003 — Consumer workspace lacks .gitignore; __pycache__ committed
- Severity: correctness (every consumer hits it)
- Component: scripts/workspace-init or installer
- Symptom: running the validator generates .claude/agile-skills/**/__pycache__;
  git add -A sweeps .pyc files into the consumer's history.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.6
- Direction: ship a .gitignore entry at install or init time.
- Status: fixed (commit 20fc6a7). `workspace-init` writes `.gitignore` when there is none and
  appends only the missing lines when there is one, covering `__pycache__/`, `*.py[cod]` and
  `HARNESS-STATUS.md`. Init time rather than install time, so a project that installs the toolkit
  somewhere unusual still gets it.

## F-004 — USAGE §2 verify step impossible in the installing session
- Severity: doc error
- Component: USAGE.md §2
- Symptom: "start your agent session and ask what skills are available" cannot
  work in the session that ran the installer — skills load at session startup.
- Evidence: evidence/2026-08-17-peer-setup-report.md (§ skills-load note)
- Direction: §2 must say verification of discovery requires a NEW session;
  offer the file-level check (ls .claude/skills/ + frontmatter) as the
  same-session alternative.
- Status: fixed (commit 20fc6a7), as filed, and ordered so the check that works comes first: the
  file-level check (`ls .claude/skills/`, the frontmatter, `validate-workspace`) is "now, in this
  session", and the discovery check is "in a NEW session". §2 also says why — asking the
  installing session lists what it loaded *before* the install, which is wrong in a way that
  looks like a broken install. It now also explains exit 3.

## F-005 — Pre-init validator state reads as hard failure
- Severity: UX
- Component: scripts/validate-workspace
- Symptom: the documented-correct "uninitialised" answer arrives as two hard
  ERRORs and exit 1 immediately after install reports success; only a hint line
  distinguishes it from a real fault.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.2
- Direction: distinct exit code / UNINITIALISED state with explicit next-step
  message.
- Status: fixed (commit 20fc6a7), as filed. A directory whose only findings are `project.missing`
  and `items.missing`, with no items and no documents, is not a fault: `validate-workspace`
  reports it as the expected pre-initialisation state, prints the exact `workspace-init` command,
  and exits **3**. 0 clean, 1 a workspace that exists and is wrong, 2 usage, 3 not started.
  Verified all three.

## F-006 — Allow-list entry inconsistent with the other seven
- Severity: UX, unverified
- Component: USAGE.md §4 suggested allow-list
- Symptom: Bash(python3 .claude/agile-skills/scripts/*) omits the :* form used
  by the other entries; merged verbatim, untested. If broken, surfaces as
  mysterious permission prompts mid-run.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.5
- Direction: test both forms against Claude Code permission matching; fix doc.
- **Settled by execution, 2026-08-21** (harness build, META-080). In a provisioned throwaway
  project that had been trusted: `claude -p "... python3 .claude/agile-skills/scripts/
  validate-workspace ." --permission-mode dontAsk` → `permission_denials: []`, the command ran,
  exit 0. Control in the same session shape, a command the allow-list does not cover
  (`python3 -c "print(6*7)"`) → **denied**, one entry in `permission_denials`. So the suspected
  entry matches correctly, and the control proves the test could have failed. The symptom F-006
  predicted is real but has a different cause: see **F-012**.
- Status: rejected (the entry is correct; superseded by F-012, which is the real defect)

## F-007 — No distribution/export path for consumer projects
- Severity: enhancement
- Component: scripts (new: export), USAGE.md
- Symptom: workspace and product share one repo by design; users who want to
  publish the product without the procedural record have no supported path,
  and naive deletion leaves everything recoverable in git history.
- Evidence: design discussion, 2026-08-17 (owner)
- Direction: non-destructive scripts/export producing a fresh-history copy with
  profiles: product-only / product+architecture (default; ADRs ship) / full
  record. Machine-check that no workspace files leak; handle WI-#### refs in
  commit messages for product-only.
- Status: fixed (commit 70fb275), all four parts as filed. `scripts/export <destination>` selects
  from `git ls-files` (so ignored build output never travels), copies into a **new** directory and
  initialises a repository there with one commit and no ancestry — the original is not touched,
  rewritten or rebased. Profiles `product` / `architecture` (default) / `full`; `product` strips
  `(refs WI-0007)` from the commit subject, because an ID that resolves to nothing is worse than
  no ID.
  **The machine-check turned out to be two checks, and separating them is the interesting part.**
  Run against iteration 1d's real project it reported eight "leaks" that were nothing of the kind:
  ADRs carrying `[src: tracker/items/WI-0001/artifacts/plan.md]`, which is F-001's
  claim-provenance rule working exactly as intended. No content escapes — the reference simply
  does not resolve in the copy. So a **workspace file** in the export is an error, always; a
  **citation naming a workspace path** is reported, listed and allowed, because the alternative is
  asking authors to choose between citing their evidence and being able to publish. `--strict`
  refuses on those too, for anyone who disagrees. It also found and now excludes the engagement
  files that sit at a project root without being part of the software: `CONSUMER-PROMPT.md`,
  `SIMULATION-NOTICE.md`, `IDEA.md`, `HARNESS-STATUS.md`.
  `./scripts/check` step **export profiles** proves the product profile ships no workspace, that
  the result is a one-commit repository, and that a second export over the same directory refuses
  without `--force`. USAGE §4 documents it.
## F-008 — Asynchronous file-based human interaction as a first-class mode
- Severity: enhancement (blocks automated iteration harness; also serves real async stakeholders)
- Component: methodology (intake, refine, plan, answer-questions), spec, adapters
- Symptom: intake/refine are interactive-only. In any context where the runtime's
  question tool is unavailable (headless runs, automation), the documented fallback
  (USAGE §4, dontAsk note) is "print the questions and stop" — an interactive
  refinement becomes a dead end. The planned two-session test harness cannot run
  without an async path, and real human stakeholders also answer questions
  asynchronously.
- Evidence: USAGE.md §4; harness design discussion 2026-08-17 (meta/harness/DESIGN.md)
- Direction: make the existing question-file protocol the canonical interaction
  channel for ALL human interaction, with the interactive tool as one transport
  over it. Refinement questions are written as question artifacts addressed to
  the human; on the next invocation the skill consumes answers from the answer
  files and continues. Interactive mode remains the default UX; async mode is
  selected by configuration or by tool unavailability.
- Interim: the harness works today at the prompt level (worker turn prompt:
  "write human questions via the question mechanism and stop; consume answers
  next turn") — no toolkit change required for harness v1.
- Status: **deferred**, gated on a real asynchronous human — the fresh-eyes install-and-run
  recorded under F-009, before the open-source release. Triaged 2026-08-30 (META-128): the
  harness has now proved the question-file protocol carries a whole engagement, so the defect
  that motivated this is gone. What remains is a design change — making the file protocol the
  canonical channel with the interactive tool as one transport over it — and its evidence has
  to come from someone who is not us

## F-009 — Prior art: BMAD-METHOD; README must position against it
- Severity: strategy/docs, ship-blocker for the open-source release
- Component: README.md, docs
- Symptom: BMAD-METHOD (bmad-code-org/BMAD-METHOD, MIT, ~51k stars, v6) is the
  established incumbent in "agile methodology as AI agents": role personas,
  34+ lifecycle workflows, planning artifacts, cross-tool installers, module
  ecosystem. Publishing in this space without acknowledging it costs credibility
  immediately.
- What it does NOT deliver (our theses): autonomy as the operating mode (their
  model is human-facilitated collaboration; "Dev Loop Automation" is roadmap,
  not shipped core); enforcement as program (their process is instructions,
  templates, and checklists the agent is asked to follow — no state machine,
  no transition program, no hooks denying bypass writes, no permanent --force
  records); audit-grade paper trail (they produce planning documents, not a
  reconstruction-grade record with journals, history, question provenance, and
  an independent-audit acceptance bar).
- Direction: README gains a positioning section: this project is the enforced,
  autonomous, auditable option — delegate-and-verify rather than
  collaborate-and-facilitate — with an honest acknowledgment of BMAD and a
  pointer for users who want facilitation instead. Mine their docs for lessons
  before builder session two: installer UX, the bmad-help orientation pattern
  (maps to our USAGE gaps), scale-adaptive planning depth (our pipeline applies
  identical ceremony to a bug fix and a system — this critique will come),
  cross-tool packaging (relevant to the Codex adapter).
- Constraint: "BMad"/"BMAD-METHOD" are trademarks of BMad Code, LLC. Any derived
  content requires our own name and MIT attribution; "derived from" is the only
  permitted relationship claim.
- Status: fixed (commit 3e1b0a2). `README.md` gains **"Prior art, and where this sits"**: what
  BMAD-METHOD is, said without hedging (established, far broader, tens of thousands of stars, and
  the thing anything here should be measured against); a five-row table of the actual difference —
  collaborate-and-facilitate versus delegate-and-verify, instructions versus a program, planning
  documents versus a reconstructable record; a concrete paragraph on what "enforcement as a
  program" means in practice; and a **"which one you want"** section that sends readers who want
  facilitation to them, in those words. Their convergence ("Dev Loop Automation") is named rather
  than ignored.
  Trademark: attributed, and no relationship claimed — we derived nothing, so "derived from"
  would itself be an overclaim. `## What this is not` also gains an entry pointing at
  `meta/ROADMAP.md` §2, the findings ledger and the run evidence, because a positioning section
  that does not say "this is not proven yet, here is the bar" is marketing.

## F-010 — BMAD-derived content imports, gated on a proven kernel
- Severity: roadmap (deliberately deferred — do not schedule into cycle 2)
- Component: methodology (future content), meta/ROADMAP.md
- Symptom: BMAD's workflow content is MIT-reusable, but wholesale absorption is
  a translation project, not a transplant: their prose assumes human-facilitated
  machinery and contains none of what our machinery requires (declared inputs,
  machine-checkable exit criteria, executable gates, escalation, statuses).
  Much of it (brainstorming, briefs, research, party mode) is facilitation-shaped
  and structurally unenforceable — wrapping judgment-shaped work in gate-shaped
  clothing is precisely the failure mode F-001 documents. Importing 34 workflows
  onto an unhardened 8-skill kernel multiplies defect surface ~4x and dissolves
  positioning into "a BMAD fork".
- Direction: quarry, don't fork. After the kernel is proven (gate below),
  port individual workflows only when run evidence shows a specific skill is
  weak and their treatment is stronger — one workflow at a time, fully
  translated into contract form, gates authored honestly, facilitation-shaped
  content either excluded or explicitly marked ungated, renamed, attributed.
  Long-term architecture: content packs over the enforcement kernel — the
  pipeline as a methodology-agnostic enforcement layer, our pack first, a
  BMAD-derived pack as a possible later pack.
- Gate ("proven kernel", also in meta/ROADMAP.md): (1) a full consumer run
  completes with zero skill version bumps; (2) the three dead paths (DoR
  override, blocked, both send-backs) have each executed at least once;
  (3) the F-001 fix (mechanical claim provenance / adversarial verification)
  has survived a real run.
- Status: deferred (gated)

## F-011 — `answer-questions` precondition excludes the case the protocol depends on
- Severity: correctness (blocks the async human path; harness works around it in a prompt)
- Component: methodology (answer-questions), spec/question.md
- Symptom: `answer-questions`' precondition 1 reads "There is at least one open question
  addressed to `architect`. If every open question is addressed to `human`, you have nothing to
  do: report and stop." A question the **human has answered** is still `status: open` and still
  `addressed-to: human` — the human writes the answer, and only `answer-questions` may propagate
  it, mark it answered and resume the item (its own step 4 provides `answered-by: human`, and
  `spec/question.md` §3 draws exactly that arrow). Read literally, the precondition tells the one
  skill that can consume a human answer that it has nothing to do.
- Consequence: the pipeline deadlocks. `next` step 2 stops the loop on any open human-addressed
  question, so an answered-but-not-consumed question stops every subsequent turn forever.
- Evidence: methodology/skills/answer-questions/process.md (Preconditions 1 vs Steps 4/7);
  spec/question.md §3 diagram and rule 5; harness worker turn prompt amendment B, which exists
  only to talk the worker past this sentence.
- Direction: precondition 1 should read "at least one open question that is answerable —
  addressed to `architect`, or addressed to `human` with `## Answer` filled in". The escalation
  case it was written for is "addressed to human and *not* answered".
- Status: fixed (commit 565076a) — precondition 1 rewritten as filed, naming both
  answerable shapes and stating the escalated-and-unanswered case it was actually written for.
  `answer-questions` → 0.1.4. The harness worker-turn prompt's amendment B, which existed only
  to talk the worker past that sentence, is deleted (prompt → version 3) and replaced by a note
  saying that if a future run gets stuck there, the contract regressed.

## F-012 — In headless runs, `permissions.allow` is ignored unless the project is trusted
- Severity: correctness, consumer-facing (silently disables the setup USAGE recommends)
- Component: USAGE.md §4, adapters/claude-code (installer docs)
- Symptom: a `-p` session never shows the workspace-trust dialog, and Claude Code discards the
  workspace's `permissions.allow` wholesale when the workspace has never been trusted:

      Ignoring 8 permissions.allow entries from .claude/settings.json: this workspace has not
      been trusted. Run Claude Code interactively here once and accept the trust dialog, or set
      projects["<dir>"].hasTrustDialogAccepted: true in ~/.claude.json.

  So the allow-list USAGE §4 recommends for "steady use" has no effect in any automated or
  headless run of a project the owner has not opened interactively at least once. The failure is
  silent apart from one stderr line, and it presents as unexplained permission prompts or
  denials — which is also the symptom F-006 is chasing.
- Evidence: a fresh `claude -p` in a project provisioned by `harness/provision.py`, stderr quoted
  above (meta/harness/evidence/); `harness/provision.py --trust` exists because of it.
- Direction: USAGE §4 gains the trust requirement and the two ways to satisfy it (open the
  project interactively once, or set `hasTrustDialogAccepted`), plus the note that `--settings`
  and `--allowedTools` are honoured regardless because they are supplied explicitly. F-006's
  syntax question can only be answered *after* the entries are honoured at all.
- Status: fixed (commit 20fc6a7), as filed, with the stderr line quoted verbatim so a reader who
  hits it can search for the words they actually saw, and with the consequence stated: the setup
  §4 recommends is silently off, presenting as unexplained prompts or denials mid-run.

## F-013 — A blocking question on an epic is unrepresentable
- Severity: correctness, structural (an escalation path the methodology documents cannot execute)
- Component: methodology/pipeline.yaml, spec/ids-and-statuses.md, scripts/validate-workspace,
  methodology/skills/intake
- Symptom: three rules that cannot all hold.
  1. `pipeline.yaml` declares epic status `open` as `terminal: true`.
  2. The only transitions into `awaiting-answer` and `blocked` are `from: any-non-terminal`, so
     no legal transition suspends an open epic — proven by execution:
     `transition EP-001 --to awaiting-answer --actor intake` →
     `transition: open → awaiting-answer by 'intake' is not a transition in pipeline.yaml`.
  3. `validate-workspace` (line ~515) errors with `question.blocking.not-suspended` whenever an
     item — epic included — carries an open blocking question and is not at `awaiting-answer`
     or `blocked`.
  Meanwhile `awaiting-answer` and `blocked` both declare `applies_to: [work-item, bug, epic]`,
  and `intake`'s own escalation instruction is "leave the rest as an open question addressed to
  `human` on the epic, set the epic to `awaiting-answer`, and stop" — which is exactly the
  sequence that cannot be executed.
- Consequence: a skill that genuinely cannot proceed on an epic-level question has no honest
  move. It must either mark a blocking question `blocking: false` (a lie the record carries
  forever) or leave the workspace failing validation.
- Evidence: found organically by the worker in the first real iteration — it filed
  `EP-001/Q-001` as `blocking: false` and wrote a paragraph in the question's `## Context`
  explaining precisely why it had to, citing `pipeline.yaml` and the validator. That paragraph
  is in meta/harness/evidence/iteration-1-mini/. The transition refusal above was then
  reproduced by hand.
- Direction: decide which rule gives. Either epics may be suspended (add
  `from: open → awaiting-answer` for epics, and stop calling `open` terminal for this purpose),
  or they may not (then `applies_to` must drop `epic` from `awaiting-answer`, `intake`'s
  escalation must be rewritten, and the validator must exempt epics — with `addressed-to: human`
  alone doing the stopping, which `next` step 2 already does).
- Status: fixed (commit 48e4fff) — epics may be suspended, and the reason the rule was
  wrong is named rather than patched around. `terminal` was carrying two questions: *does the
  pipeline advance an item out of this status by itself* (an epic at `open` does not — it
  advances through its children) and *may a blocking question or an impasse stop an item here*
  (an epic-level question is exactly the case that must). Statuses now declare **`suspendable`**
  separately, the two escalation transitions read `from: any-suspendable`, and `open` is
  `terminal: true, suspendable: true`. `pipeline.yaml` → 0.2.0;
  `spec/ids-and-statuses.md` §4 revision 2.
  New lint rule `pipeline.status.unsuspendable`: a status that is not suspendable must be an
  escalation target or a closed status — the F-013 defect stated as an invariant. Proven to fire
  by flipping `open` back to the pre-fix value.
  Proven by execution, in a scratch workspace: the exact command the finding quotes as refused,
  `transition EP-001 --to awaiting-answer --actor intake --resume-to open`, now succeeds and
  writes the row; `awaiting-answer → open` resumes it; and `done → awaiting-answer` is still
  refused with the same message. Fixture row added for the still-illegal case.

## F-014 — `transition` runs its gates against the pre-move workspace
- Severity: correctness (a gate that reports FAIL on correct work)
- Component: scripts/transition, scripts/run-gate
- Symptom: `transition`'s pre-move gate run evaluates `workspace-valid` against the workspace as
  it is *before* the move it is about to make. On every `answer-questions` resume this printed
  FAIL — the questions are already `answered`, the item is still `awaiting-answer`, the board has
  not been regenerated yet — while `transition` itself reported the gates as not blocking and its
  own post-move validation came back clean. The gate is checking the wrong side of the
  transition.
- Consequence: a loud FAIL on correct work, every time, on the one path whose whole purpose is to
  resume a suspended item. An agent that believes its gates learns to ignore this one.
- Evidence: found organically by the worker in iteration 1 and journalled where it happened;
  meta/harness/evidence/iteration-1-mini/.
- Direction: either evaluate `workspace-valid` against the post-move state, or exclude from the
  pre-move run the codes that the move itself resolves, and say which in the gate's output.
- Status: fixed (commit 565076a) — the second option, with the "say which" taken
  literally. `transition` now tells its gate run which move is pending
  (`run-gate --resolving ITEM:from->to` → `validate-workspace --resolving ...`), and the
  validator **downgrades to warnings** exactly the findings that move resolves: `board.stale` /
  `board.missing` for any move (the script regenerates the board immediately after),
  `question.awaiting.none-open` when leaving `awaiting-answer`/`blocked`, and
  `question.blocking.not-suspended` when entering one — the last two scoped to the moving item
  only. It prints a note saying how many were downgraded and why, so nothing is silently
  forgiven. Demonstrated in a scratch workspace on the exact path the finding names: the
  `answer-questions` resume prints `FAIL workspace-valid` without the pending move declared and
  `PASS` with it.

## F-015 — `implement` is required to pass through a red validator
- Severity: correctness (the procedure guarantees a failing gate mid-execution)
- Component: methodology/skills/implement, scripts/validate-workspace, spec/journal-and-history
- Symptom: `implement`'s step 3 requires the item to move to `in-progress` before any code is
  written, and its step 9 requires the journal entry at the end. Between the two,
  `validate-workspace` reports `journal.execution.missing` — an actor appears in `history.md`
  with no journal entry — on every single run. The procedure makes the failure mandatory.
- Consequence: "the validator is red" stops meaning "something is wrong", which is the failure
  mode `meta/findings` F-001 is about, in a machine-decidable gate this time.
- Evidence: found organically by the worker in iteration 1;
  meta/harness/evidence/iteration-1-mini/.
- Direction: either the journal entry is written when the status moves (so the record is never
  inconsistent), or `journal.execution.missing` is a warning while the item is at `in-progress`
  with the acting skill still running. The first is better: it also makes an interrupted
  `implement` recoverable, which is what `in-progress` exists for.
- Status: fixed (commit 565076a) — the first option, which META-084b had already built
  the mechanism for. `implement` step 3 now moves to `in-progress` **and** writes an opening
  journal entry in the same command (`transition --journal-body-file --branch`). The skill
  writes two entries because it makes two transitions: the opening one records the branch and
  lists every gate as not-yet-run, which is the truth at that moment; step 9's is the report.
  `implement` → 0.2.1. `journal.execution.missing`'s hint now names the one-command fix.

## F-016 — Epic-level record commits have no home branch
- Severity: correctness (a gate fails for an item that did nothing wrong)
- Component: methodology (answer-questions, review-close), spec/workspace-layout
- Symptom: `answer-questions` working on an **epic**'s question commits the tracker record to
  whatever branch happens to be checked out — which, mid-pipeline, is a work item's branch. The
  commit then references the epic while sitting on `wi/WI-000n`, and `check-commit-refs` /
  Definition of Done "commits reference the item" fails for the *unrelated* work item. Nothing in
  the methodology says where an epic-level record commit belongs.
- Evidence: found organically by the worker in iteration 1 (turn 6 report and
  `tracker/items/WI-0001/artifacts/review.md`); meta/harness/evidence/iteration-1-mini/.
- Direction: state the rule. Either epic-level record commits are made on the trunk branch (the
  epic is not a branch-scoped unit of work), or an item's branch owns every commit made while it
  is checked out and the gate must scope by item, not by branch.
- Status: fixed (commit 565076a) — the first option. `spec/workspace-layout.md` §5
  (revision 3): an epic-level record commit is made on the trunk, because an epic has no branch,
  outlives every item under it, and is changed by executions that are not about any one child.
  `answer-questions` (0.1.4) and `review-close` (0.3.1) carry the step. `check-commit-refs` now
  diagnoses the shape rather than only reporting it: an offending commit whose subject names a
  *different* item is called out as an epic-level commit on the wrong branch, with the note that
  the gate is failing for an item that did nothing wrong — which is exactly what the worker who
  found this could not tell.

## F-017 — The restamp deadlock exists in `journal.md` too, and skills invent timestamps
- Severity: correctness (the record carries plausible-looking fabricated times)
- Component: spec/journal-and-history.md, scripts/transition (--restamp-last)
- Symptom: the monotonic-timestamp rule and its sanctioned repair (`--restamp-last`) cover
  `history.md`. The identical deadlock occurs in `journal.md`, where there is no exception — and
  the observed consequence is worse than a deadlock: skills write a *plausible* timestamp rather
  than reading the clock, so the journal's times are invented where the history's are real.
- Evidence: found organically by the worker in iteration 1 (turn 6 report);
  meta/harness/evidence/iteration-1-mini/.
- Direction: give `journal.md` the same treatment as `history.md`, and say explicitly in the spec
  that a timestamp is read from the clock and never estimated — an invented timestamp is the one
  kind of record entry that cannot be audited against anything.
- Status: fixed (commit 4672b1c for the mechanism; adoption in commit d4b80e9).
  `scripts/journal-entry` is the only sanctioned writer of an entry: it stamps the heading from
  the clock and from the acting skill's installed `skill.yaml` (version **and** persona), so no
  header field is authored by the model. `transition --journal-body-file` writes the row and the
  entry together and overwrites the caller's `**Status:**` bullet with the move it actually made.
  `journal-entry --restamp-last` is the journal's half of the sanctioned repair.
  `spec/journal-and-history.md` §0 (revision 2) states the rule normatively.
  Validator: `journal.timestamp.future`, `history.timestamp.future`,
  `journal.timestamp.outside-activity`, `history.timestamp.outside-activity`,
  `journal.version.impossible`. Adoption: all seven journalling skills' `## Journaling`
  sections now write the bullets to a file and let the tool stamp the heading, and every
  "journal, then transition" step became "journal and transition, in one command"
  (`spec/skill-contract.md` §2.2, revision 3 — the old two-step rule is what left the gap
  F-019 fell into). `next` is exempt; it journals nothing. Seven patch bumps.
  Demonstrated both ways in a scratch workspace — a real
  transition produced `## 2026-08-22T00:41:10Z — refine v0.1.1 — product-analyst` with the
  clock agreeing to the second and a deliberately wrong `**Status:** draft → banana` corrected
  to `draft → ready`; a hand-written entry in run 1c's exact shape (a plausible later-that-day
  12:55 for a transition that never happened) was rejected by
  `journal.timestamp.future` **and** `journal.status.unmatched` at once.

## F-018 — The workspace-write guard hook matches the command, not the target
- Severity: correctness (blocks legitimate commands; trains agents to work around the guard)
- Component: adapters/claude-code/hooks/guard-workspace-writes.py
- Symptom: the hook decides by looking for the guarded path inside the Bash *command string*, so
  a command that merely mentions `tracker/board.md` — printing it, grepping it, naming it in a
  commit message — is denied as though it were writing to it.
- Consequence: the agent learns the guard is noise and starts phrasing commands to avoid it,
  which is exactly the opposite of what a guard is for.
- Evidence: found organically by the worker in iteration 1 (turn 6 report);
  meta/harness/evidence/iteration-1-mini/.
- Direction: decide on the write target, not on the mention: parse redirections and the known
  mutating commands, or move the guard to the file-write tools where the target is a parameter
  rather than prose.
- Status: fixed (commit dd1fb3c). The Bash branch now resolves **write targets**:
  the command is lexed keeping its operators, split into simple commands, and each one yields
  its redirection destinations plus the argument positions of the mutating programs it knows
  (`tee`, `sed -i`/`perl -i`, `dd of=`, `cp`/`mv`/`install`/`ln`, `rm`/`shred`/`truncate`,
  `patch`, `ed`), through `sudo`/`env`/`xargs` wrappers. Input redirection and heredoc sources
  are not targets. Anything unparseable is still allowed — the module's standing policy.
  New gate step in `./scripts/check`: `adapters/claude-code/hooks/test_guard.py`, 30 cases,
  15 must-deny and 15 must-allow, and the table refuses to run if either side is empty.
  The negative is demonstrated: the same table against the **previous** guard fails 7 cases —
  `cat tracker/board.md > /tmp/x`, `grep -n WI-0003 tracker/items/*/history.md > /tmp/out`,
  `diff`, and an unbalanced quote all denied as writes; `cp`/`mv`/`rm` onto a protected file all
  allowed.

## F-019 — A failed transition mid-chain leaves record and status divergent, undetectably
- Severity: correctness, enforcement-integrity (top cluster with F-001, F-018)
- Component: scripts (transition, validate-workspace, all CLI entry points), methodology
  (every skill's process contract)
- Symptom: during WI-0003's implement, a `cd` into the item directory made the relative
  script path fail — `transition` never ran — but it failed mid-chain, so the rest of the
  chained shell command executed anyway: the journal entry claiming
  `in-progress → verifying` and tracker commit 234f170 both landed while the item was still
  `in-progress`. The worker's own correction names it: "a workspace that briefly disagreed
  with its own record, in the one direction the record cannot detect." Second relative-path
  failure of the same session.
- Evidence: meta/harness/evidence/iteration-1-full/ —
  project/tracker/items/WI-0003/journal.md, the appended correction after the implement
  entry (≈ lines 587–602); commit 234f170 vs the history rows.
- Direction: three fixes, all mechanical. (a) Every toolkit script resolves the project
  root itself (walk up to a workspace marker) instead of assuming CWD. (b) Process
  contracts forbid chaining `transition` with other commands; it is a checkpoint whose
  exit code gates everything after it. (c) validate-workspace gains a cross-check: every
  journal `**Status:**` line must have a matching history row — the undetectable direction
  becomes detectable.
- Status: fixed (commit bee3a3c) — all three, as filed.
  (a) `scripts/lib/workspace.py` gains `find_workspace_root()` / `resolve_root()`; every
  script (`validate-workspace`, `transition`, `board-gen`, `new-item`, `run-gate`,
  `check-commit-refs`, `check-verify-freshness`) walks up to `tracker/project.yaml` when no
  root is given, and says on stderr when the root it found is not the working directory.
  Proven: `validate-workspace` run from `examples/toy-project/tracker/items/WI-0001` reports
  `0 errors, 0 warnings` for the whole workspace. Covered by four selftest cases including the
  outside-any-workspace fallback.
  (b) `spec/skill-contract.md` §2.3 (revision 2) — the transition is a checkpoint, never
  chained, exit code read before the journal entry is written; and commands are invoked by a
  path that does not depend on CWD. Rendered into every `SKILL.md` by the adapter.
  (c) `validate-workspace` gains `journal.status.unmatched`. Must-fail fixture: a second
  BUG-0001 journal entry claiming `in-progress → verifying` with no such history row — the
  exact shape of the original failure — plus a pre-existing fixture divergence the rule also
  caught (WI-0001's `— → draft`). `fixtures/broken-workspace/EXPECTED-CODES.txt` is at 45 codes.

## F-020 — refine files several separate questions for one item in one round
- Severity: UX/enhancement, low priority
- Component: methodology (refine), spec/question.md
- Symptom: the sim, in persona, on receiving WI-0002/Q-004..Q-006 at once: "three separate
  emails landed on me for one work item — fine that they're batched, but it's the same item
  asking three times running." The protocol batches per round-trip but presents per-file.
- Evidence: meta/harness/evidence/iteration-1-full/ — run/SIM-LOG.md, turn 3.
- Direction: keep one question artifact per decision (provenance needs it), but let refine
  present them as one grouped ask per item per round — a presentation change in the
  question body/consequences convention, not a schema change.
- Status: fixed (commit 54b67ee), as filed and with no schema change. `spec/question.md` §2
  (revision 4): questions filed for one item in one round are presented as one ask — each
  `## Context` opens with the same frame naming the item, the round and which of how many this
  is, and the last says that is all of them for now. `refine` step 4 carries it. One
  conversation, three artifacts.

## H-002 — turn-failed is terminal in code; USAGE §9 promises resume; --fresh destroys the run
- Severity: harness, correctness + doc contradiction (sharpest harness defect of iteration 1)
- Component: harness/run_iteration.py (stop handling, line ~529), harness/USAGE.md §9
- Symptom: a turn killed by --turn-timeout records status=stopped / stop-reason=turn-failed;
  rerunning prints "this run already stopped: pass --fresh to archive it and start a new
  one" — while USAGE §9's last entry says "A turn hangs. --turn-timeout kills it... Resume
  with the same command." The documented recovery does not exist; the only offered exit
  archives four turns of good work. --reaudit (the plausible alternative) is
  contamination-specific and does not clear the stop. Recovery required hand-editing
  state.json (status → running, drop the stop fields), which worked.
- Evidence: meta/harness/evidence/iteration-1-full/ — run/state.json.bak (the stopped
  state), run/iteration-log.jsonl turn 4 and the stop events; owner's session log
  2026-08-21.
- Direction: classify stop reasons as resumable (timeout kill, limit/auth rejection) vs
  terminal (epic-done, blocked-no-recourse, budget, contamination); resumable stops resume
  on plain rerun, exactly as §9 already promises. Fix the --fresh hint text to say what it
  actually does (see H-003).
- Status: fixed (commit f7af8f9), as filed. `RESUMABLE_STOPS` = `turn-timeout`,
  `api-rejected`, `turn-failed`; `TERMINAL_STOPS` = `epic-done`, `blocked-no-recourse`,
  `turn-budget`, `contamination`, `validator-failed`, `stalled`. A resumable stop clears on a
  plain rerun, logs a `resume-after-stop` event, and re-runs the interrupted turn; nothing is
  archived. A killed turn is now recorded as `turn-timeout` rather than `turn-failed`, and a
  turn the API refused as `api-rejected`, so the log answers "why did this stop" without
  opening a transcript. The terminal message now states exactly what `--fresh` archives (the
  run) and what it does not (the project), and points at `provision.py --wipe`.
  Five tests, including one that reads the driver's source for every `self.stop("...")` it emits
  and fails if either table has missed one — the way this regresses is a new stop reason nobody
  classifies, silently defaulting to terminal.

## H-003 — --fresh archives the run logs but not the project workspace
- Severity: harness, correctness of semantics + misleading docs
- Component: harness/run_iteration.py (--fresh), harness/provision.py, FINAL-REPORT §6,
  USAGE §3
- Symptom: FINAL-REPORT §6 presents provision + --fresh as the clean start; in practice
  provision is idempotent ("nothing to commit (already provisioned)") and --fresh archives
  only harness/runs state, so iteration 1 silently resumed the mini run's epic: turn 1's
  sim found IDEA.md already present, turn 2's worker found 13/16 questions already
  answered and WI-0001 done. Acceptable outcome, wrong expectation; the trail now spans
  two runs.
- Evidence: meta/harness/evidence/iteration-1-full/ — run/SIM-LOG.md turn 1 (IDEA.md
  already present) and turn 3 (probes fired before any logged sim turn);
  run/iteration-log.jsonl turn 2 (worker no-op report).
- Direction: provision gains --wipe (or --fresh re-provisions the workspace too, behind an
  explicit confirmation); whichever way, one flag means one thing and USAGE says which.
  Needed anyway for iteration 1b's true-fresh start.
- Status: fixed (commit f7af8f9). `provision.py --wipe` deletes the project directory
  and re-provisions from nothing. Two refusals, because the flag deletes: the directory must
  carry `.harness/provision.json` (so a wipe cannot land on something this tool did not create)
  and it must be strictly inside the throwaway root (so a mistyped `--root` cannot make this a
  general-purpose delete). `--dry-run` deletes nothing. Four tests cover both refusals, the
  success, and the dry run.
  `--fresh` keeps its meaning and now states it: `harness/USAGE.md` §3 carries a two-row table —
  a new run over whatever the last one built, versus a genuinely fresh start — and names H-003's
  symptom as the reason the distinction is written down.

## H-004 — After a start/resume, the driver runs a worker turn into unanswered human questions
- Severity: harness, scheduling (one full round trip wasted per occurrence)
- Component: harness/run_iteration.py (turn scheduling), sim job selection
- Symptom: iteration 1 turn 2 was a pure no-op the worker itself diagnosed: turn 1's sim
  job was "open" (deliver the idea), three questions from the resumed workspace sat
  unanswered, the worker's orchestrator correctly halted at step 2, and a whole worker
  turn produced nothing. Turn 3's sim then answered.
- Evidence: meta/harness/evidence/iteration-1-full/ — run/iteration-log.jsonl turn 2
  (worker-report notes), HARNESS-STATUS.md as captured in the turn record.
- Direction: before dispatching a worker turn, the driver checks its own observed state
  for unanswered human-addressed questions; if any exist, dispatch a sim "answer" turn
  first. The observed fields already exist in the log schema.
- Status: fixed (commit 65923da), as filed. At the top of each iteration of the turn
  loop, a scheduled worker turn re-scans the project; if any human-addressed question is open
  and unanswered, the turn goes to the sim with job `answer` and a `reschedule` event is logged
  saying why. The check costs one filesystem scan and saves a full round trip. The reason this
  needed fixing at the loop rather than in `decide()` is that `next-role` comes from `state.json`
  on a start or a resume, so no decision had run.

## H-005 — A killed turn loses its cost and inherits a stale worker-report
- Severity: harness, evidence integrity
- Component: harness/run_iteration.py (turn accounting, status capture)
- Symptom: turn 4 (killed at 3603s, 255 tool calls, a full Opus-hour) is logged with
  cost_usd=0.00, so the iteration's economics understate real spend; and its logged
  worker-report is turn 2's — the killed turn never wrote HARNESS-STATUS.md, and the
  driver read the stale file without noticing, silently misattributing a two-hour-old
  status to the killed turn.
- Evidence: meta/harness/evidence/iteration-1-full/ — run/iteration-log.jsonl turn 4
  (cost 0.00, stop_reason human-question-open — impossible for that turn).
- Direction: mark killed turns' cost as unknown (or derive a floor from the transcript);
  compare HARNESS-STATUS.md's mtime against turn start and record "no status written"
  instead of a stale one.
- Status: fixed (commit 65923da), both halves as filed. A turn with no result event
  records `cost_usd: null`, `cost-unknown: true`, and a note carrying its duration and tool
  count — zero is a number a reader adds up, unknown is not; the run summary line prints
  `cost=unknown`. `worker_report()` takes the turn's start time and returns nothing when
  `HARNESS-STATUS.md` predates it, and the driver says out loud that the turn wrote no status
  rather than attributing a two-hour-old one to it. Five tests.

## H-006 — Turn granularity: one turn may pack many skill executions, defeating the timeout
- Severity: harness, design
- Component: harness/prompts/worker-turn.md, run_iteration.py (--turn-timeout)
- Symptom: turn 4 legally executed answer-questions consumption, refine, plan, implement
  and most of verify across two items in one turn — 255 tool calls — so the per-turn
  timeout killed a healthy run precisely because it was going well. The timeout punishes
  progress when the unit of accounting is "as much as fits."
- Evidence: meta/harness/evidence/iteration-1-full/ — run/iteration-log.jsonl turn 4;
  the WI-0002/WI-0003 journal timestamps spanning one turn.
- Direction: either the worker prompt stops after N skill executions per turn (making
  turns comparable and timeouts meaningful), or the timeout is documented as
  worst-single-skill × N with a generous default. Prefer the former: bounded turns also
  bound the blast radius of every kill.
- Status: fixed (commit 65923da) — the former. Worker prompt version 4 stops after
  `{{SKILLS_PER_TURN}}` skill executions and reports `turn-budget-exhausted`, an enum value that
  already existed for exactly this shape. An execution counts when a skill *finishes* — journal
  written, transition made — and the prompt is explicit that the skill in flight is finished
  first, never left half-done. `next` does not count; it is the dispatcher. The bound is
  `--skills-per-turn`, or the iteration config's `worker-skills-per-turn`, default 3. The status
  block gains `skills_run`, so a turn that overran is visible in the log rather than inferred
  from the tool count.


## F-024 — A finding's commit citation is not checked, and every one of mine was wrong
- Severity: correctness, record integrity (found in this file, by this session)
- Component: meta/findings/FINDINGS.md, scripts/check
- Symptom: builder session two recorded ten `fixed (commit <sha>)` citations, and **all ten
  pointed at commits that are not in the pushed history.** The unit cycle was: commit the work,
  read `git rev-parse --short HEAD`, `sed` that sha into FINDINGS.md, `git commit --amend`. The
  amend rewrites the commit, so the sha written into the file is always the pre-amend one. It
  survives in the local object database via the reflog, so `git cat-file -e` succeeds and
  `git log -1 <sha>` prints the right subject — the citation looks valid on the machine that
  made it and is dangling everywhere else, and would vanish at the next `git gc`.
- Why it matters beyond the typo: this is F-001's failure class in the file that tracks F-001 —
  a citation that appears to resolve and does not. The toolkit now enforces claim provenance on
  a consumer's `docs/` (`claim.citation.unresolved`) and enforces nothing on its own findings
  ledger.
- Evidence: `git merge-base --is-ancestor <sha> HEAD` returned non-zero for all ten
  (02a417a, 33eb48c, 4f2ebea, 76dcaf1, 78abb5b, 78fd525, 84a11a2, 8549fca, add02cb, ae25f6c,
  d170ac7); each was mapped to the surviving commit with the same subject and corrected in
  META-099.
- Direction: two parts. (a) Stop the practice: record the sha in a **follow-up** commit, never by
  amending the commit being cited. (b) Mechanise it: `scripts/check` gains a step asserting that
  every `commit <sha>` cited in `meta/findings/FINDINGS.md` is an ancestor of `HEAD` in this
  repository — with an exemption list for shas that legitimately belong to a throwaway project's
  repository, of which F-019's `234f170` is the only current example.
- Status: fixed (commit 418eb9e). (a) the practice changed from META-099 onward. (b) `scripts/check` step **findings citations resolve**: every `commit <sha>` cited here must be an ancestor of HEAD, with `FOREIGN_SHAS` naming the ones belonging to a throwaway project's repository. Proven to fail by restoring one orphan.

---

### Addendum to F-001 (2026-08-21, iteration 1)
DE6 — one of the two criteria FINAL-REPORT recorded as unexercised — has now executed,
during EP-001's closure, and caught a real propagated false claim: overview.md's
"no environment beyond EXPENSES_STORE" contradicted store_path()'s XDG_DATA_HOME read;
corrected at v5 with provenance to WI-0003 review F3. Status of the class: works when
followed; still agent-discipline-dependent, and the mechanization direction (claim
provenance + adversarial verification) stands unchanged. Evidence:
meta/harness/evidence/iteration-1-full/ — project/tracker/items/EP-001/journal.md,
review-close entry, DE6.

### Addendum to F-013 (2026-08-21, iteration 1)
The epic-blocking-question contradiction forced its workaround again in this run's turn 1:
the worker filed the epic's question with blocking: false plus a written explanation,
documented in EP-001/questions/Q-001.md and reported in HARNESS-STATUS turn 2. Second
independent occurrence; the escalation path for epics remains uncarryable as specified.

### Addendum to F-017 (2026-08-21, iteration 1) — decisive evidence
WI-0003's plan entry is stamped 15:35:00 and implement 16:10:00, but the turn that did
that work was killed at 15:19:04 and nothing ran again until 17:32:57. The timestamps are
fabrications written into a dead zone — a timeline audit of the journal would "prove" work
happened while nothing was running. Timestamps must come from executing a clock command,
never from the model. Evidence: meta/harness/evidence/iteration-1-full/ —
project/tracker/items/WI-0003/journal.md (plan and implement headers) against
run/iteration-log.jsonl (turn 4 kill at 15:19:04Z, turn 5 start 17:32).

## F-021 — The stakeholder has no channel for unsolicited input mid-epic
- Severity: methodology gap (acceptance-loop cluster with F-022)
- Component: methodology (next, intake), spec/question.md
- Symptom: the human can only speak when spoken to. Run 1b's sim, holding a new requirement
  it was scripted to introduce, logged across two turns that no question gave it a vehicle
  ("not introducing it unprompted, per persona rule 1"), and the run then ended epic-done
  with the requirement never voiced. Real stakeholders volunteer requirements constantly.
- Evidence: meta/harness/evidence/ — run 1b SIM-LOG turns 3 and 5; run 1b ending epic-done
  at turn 6 with zero further human questions.
- Direction: a stakeholder-initiated request artifact (spec'd like a question in reverse)
  that `next` detects and routes to intake/refine before building the candidate set.
- Status: fixed (commit 5de4fd2). New artifact and new spec file: `spec/request.md` —
  `tracker/requests/R-###.md`, `from: human` (the only author a request may have),
  `status: open | accepted | declined`, an optional `about`, `## Request` in the stakeholder's
  own words which a skill **never edits**, and `## Response` / `## Consequences` the handling
  skill fills in naming files and item IDs.
  Filed workspace-wide rather than under an item, deliberately: the stakeholder does not know
  which item their thought belongs to, and deciding that is `intake`'s job.
  Routing: `pipeline.yaml` orchestrator step **2** (0.3.0) — an open request outranks building
  the candidate set, dispatched to `intake` and then stop. Ordering matters: a request handled
  once the current item finishes is answered against a plan the stakeholder already tried to
  change. `next` 0.2.0 and `intake` 0.2.0 carry it; `intake` gains step 0, including the right
  to **decline** in writing and the rule that invalidating a mid-flight item means filing a
  blocking question on it rather than reaching into it.
  `workspace-init` creates `tracker/requests/`; `spec/workspace-layout.md` (revision 2) and
  `spec/README.md` carry it. Validator: nine new codes.
  Fixtures: three malformed requests in `fixtures/broken-workspace` covering every rule; a
  well-formed open request demonstrated validating clean in a scratch workspace.
  Note for the harness: the simulated human has `Write`, so this is a channel it can actually
  use — which is what run 1b's sim lacked when it logged that it had no vehicle for the
  requirement it was holding.

## F-022 — An epic closes without stakeholder acceptance
- Severity: methodology gap (acceptance-loop cluster with F-021)
- Component: methodology (review-close step 10), spec (epic DoD)
- Symptom: both 1b and 1c closed EP-001 with no sign-off ever addressed to the human. The DE
  gates check the record — but the record only holds what the stakeholder said when last
  consulted. 1c shows the near-miss vividly: the WI-0004 redesign received explicit consent
  (Q-006), yet closure itself still asked nothing; a stakeholder with one more unvoiced
  concern had no gate at which to raise it. Every real agile process has a product-owner
  acceptance moment.
- Evidence: meta/harness/evidence/ — 1b EP-001 journal final entry; 1c EP-001 journal
  closing entries (no human question between last child closing and epic done).
- Direction: epic DoD gains an acceptance gate: review-close files a blocking
  human-addressed sign-off question (goal restated, delivered vs. deferred listed) and the
  epic cannot transition to done until it is answered. Also gives the harness a guaranteed
  final sim turn (see H-007).
- Status: fixed (commit 1c2f8ca). `spec/question.md` §2 (revision 2) adds the optional
  `kind` field and specifies `kind: sign-off`: addressed to `human`, blocking, `## Context`
  restating the goal in the stakeholder's own terms, `## Question` listing delivered vs not with
  a line of why for each, and `## Options considered` offering accept / accept-with-follow-ups /
  do-not-accept. `spec/dor-dod.md` DE7 (revision 3) is the criterion, marked `[auto]`.
  `scripts/check-epic-signoff` is the gate — hard, on `review-close` (0.3.0), so `transition`
  refuses the epic's move to `done`. It also refuses a **stale** sign-off: one filed before the
  last child reached `done` is an acceptance of something other than the finished epic.
  `review-close` step 10 files the sign-off, suspends the epic to `awaiting-answer` with
  `resume-to: open` (possible only because of F-013) and stops.
  Deliberately *not* a requirement that the answer be "yes": a stakeholder who declines closes
  the epic just as legitimately, with the outcome saying so. What is no longer possible is
  closing while never having asked.
  Proven by execution in a scratch workspace: with the only child at `done` and no sign-off,
  `transition EP-001 --to done --actor review-close` is refused with `epic-sign-off (hard)`
  among the failing gates; with a real answered sign-off it passes; with the same sign-off
  back-dated before the child's close it is refused as stale.
  Fixtures both ways, and both are `./scripts/check` steps: `fixtures/broken-workspace`'s EP-001
  carries a misspelled `kind: signoff` and a correctly-spelled sign-off answered by the architect
  (`question.kind`, `question.signoff.addressed`), and `fixtures/signed-off-epic/` is the
  captured scratch run that passes.

## F-023 — refine over-escalates technical trivia to the stakeholder
- Severity: UX (mirror image of F-020)
- Component: methodology (refine)
- Symptom: the sim, in persona, twice across runs: run 1c turn 5 — four questions on
  WI-0001 alone ("the item I'd have thought was the simplest"), "three of the four were
  things I'd expect a team to just decide on their own... technical calls being routed to
  me as questions" (tool naming, output text, exit codes). The stakeholder had already
  established the "whatever you think is best" deferral repeatedly.
- Evidence: meta/harness/evidence/ — 1c SIM-LOG turn 5; run 1's SIM-LOG for the deferral
  precedent.
- Direction: refine's contract gains a routing test before filing a question to the human:
  product-stake questions go to the stakeholder; implementation-only choices are decided
  (reversibly, recorded as assumptions) or routed to plan. A stakeholder's standing
  deferral on a category should be honored for that category.
- Status: fixed (commit 54b67ee), as filed. `refine` step 3 is a four-branch routing test applied
  before anything is filed, stopping at the first that fits: product stake → the human; already
  answered → do not ask again; a standing deferral covers the **category** → decide it and record
  the deferral being relied on; implementation-only → the item's `## Notes` for `plan` to settle.
  Added as an exit criterion so it is checkable, not advisory. `refine` → 0.2.0. The finding's
  own words are quoted in the step, including the reverse failure — guessing at something that
  was theirs to decide costs more.

## H-007 — The driver schedules sim turns only on open human questions
- Severity: harness, scheduling/coverage
- Component: harness/run_iteration.py
- Symptom: a self-sufficient worker ends the engagement unilaterally: run 1b went
  epic-done at turn 6 with the sim locked out from turn 5 onward — a mid-run probe edit
  (P2 trigger widened) could never fire because no sim turn ever ran again. The sim never
  sees the endgame of any run that closes clean.
- Evidence: harness/runs/iteration-1b-expenses/ — iteration log (turn 6 worker, stop
  epic-done; no sim turn after 5); git 50532d9..44c814d for the stranded probe edit.
- Direction: partially self-heals when F-022's sign-off question lands (closure always
  opens a human question). Belt-and-suspenders: the driver grants the sim one turn before
  accepting any epic-done stop as final, logged as job "closing".
- Status: fixed (commit 65923da), both halves. F-022 lands the sign-off, and the driver
  additionally grants one `closing` sim turn before accepting `epic-done`, tracked by
  `closing-turn-given` in `state.json` so it happens exactly once. The sim prompt (version 2)
  gains the `closing` job: answer whatever is addressed to you, then say in your own words
  whether you got what you asked for and name anything you expected that is not there — the only
  turn at which the sim sees the finished thing.
  Two further changes make the channel real rather than nominal: the sim prompt tells the
  stakeholder it may **speak first** at any turn by writing `tracker/requests/R-###.md` (F-021),
  the contamination audit permits exactly that path and nothing else new (`S1` still refuses a
  misnamed file under the same directory), and `decide()` refuses to accept `epic-done` while any
  request is still open.

---

### Addendum to F-017 (2026-08-22, runs 1b and 1c) — second and third specimens
Run 1b: EP-001 journal entries stamped 21:16:00 and 22:00:00 against last real activity
~20:36 and a turn ceiling of ~21:12 — invented times spaced to look like separate sittings.
Run 1b also self-reports "review-close v0.1.0" while the installed SKILL.md in both
projects and the source skill.yaml all say 0.1.2 — version strings in journal headers are
fabricated too. Run 1c, the most egregious: the final eleven WI-0004 and EP-001 entries
are stamped 2026-08-22T09:05 through 12:55 — nine-plus hours after the run stopped
(~00:06), narrating a leisurely next-morning half-day for work done in minutes. Sharpened
direction: every self-reported journal header field (timestamp, skill version, persona)
must come from a mechanical source — a clock command, SKILL.md frontmatter — ideally via a
script-emitted entry template; the validator should reject entries dated outside the
workspace's git activity window.

### Addendum to F-013 / coverage note (2026-08-22) — `blocked` remains unexercised, for good reasons
Four runs, four escapes, all legitimate: run 1 deferral accepted in persona; 1b the team
never opened a channel (F-021/H-007); 1c a negotiated redesign with explicit consent —
refine correctly held WI-0004 un-Ready (criteria declared undecidable without the sample),
the team escalated four times with shrinking asks, recorded "the epic cannot close without
it" at epic level, then found a design needing no sample and got the stakeholder's yes,
rewriting criteria and SM3 transparently ("unblocked, not relaxed"). The keep-moving
instinct is a feature; the `blocked` status and its recovery path are still untested code.
Iteration 1d (post-fix regression): the stakeholder additionally refuses all alternatives
("just wait for my file") — an immovable stakeholder with no legitimate exit is the
blocked case. 1d also serves as the regression test for the F-021/F-022 acceptance-loop
fixes and the F-013 epic-suspension fix.

### Addendum to H-007 (2026-08-22, META-099) — the closing turn covers an impasse too
The fix as filed gave the sim a closing turn before `epic-done`. Setting up iteration 1d made the
gap obvious: 1d is *expected* to end at `blocked-no-recourse`, and that stop had no closing turn,
so the run designed to test the acceptance loop would have ended with the stakeholder never
hearing how it finished. An impasse is an ending. The driver now gives one closing turn before
accepting `blocked-no-recourse` as well — once, tracked by the same `closing-turn-given` flag —
and the sim prompt's `closing` job asks, when an item is blocked, whether the record describes
the impasse the stakeholder is actually in or whether it reads as giving up.

---

# Findings from iteration 1d (2026-08-22)

Iteration 1d stopped at `blocked-no-recourse` after 16 turns, $71.75 and zero contamination
violations; evidence at `meta/harness/evidence/iteration-1d/`. Every finding below was found by
the worker or the simulated stakeholder during the run, not by reading the code afterwards.

**Several of these are defects in work this same session shipped.** They are filed like any other
finding rather than quietly patched, because a ledger that records only other people's mistakes
is not a ledger.

## F-025 — `workspace-valid` cannot pass at gate time on an item's first transition
- Severity: correctness (a hard gate that cannot be satisfied on one path)
- Component: scripts/transition, scripts/validate-workspace
- Symptom: `run-gate` runs before the journal entry that the **same** `transition` invocation is
  about to write, so it reports `journal.execution.missing` on the very item being moved. Harmless
  in 1d because `intake` gates only its completion transition — but, in the worker's words, "a
  skill whose *completion* transition is the item's first would be trapped."
- Evidence: evidence/iteration-1d/run/002-worker.status.md
- Direction: the same mechanism F-014 already uses. `resolved_by_move()` should downgrade
  `journal.execution.missing` for the moving item **when the transition is what will write the
  entry** — i.e. when `--journal-body-file` was passed — and not otherwise, because without it the
  finding is real. Extend `--resolving` to carry that fact rather than downgrading unconditionally.
- Status: fixed (commit 418eb9e). `--resolving` gained a `+journal` suffix that `transition` sets when `--journal-body-file` is passed; `resolved_by_move()` downgrades `journal.execution.missing` for the moving item only then. Without the flag the finding is real and is left alone.

## F-026 — `--help` is broken across the script suite
- Severity: UX
- Component: scripts (new-item, and probably every script with the same hand-rolled arg loop)
- Symptom: `new-item --help` fails with `new-item: --help needs a value`; the usage text is
  reachable only by reading the file or by omitting a required flag. Reported twice, turns 2 and 4.
- Evidence: evidence/iteration-1d/run/002-worker.status.md, 004-worker.status.md
- Direction: every entry point answers `--help` (and `-h`) with its docstring's usage block. Check
  `transition`, `run-gate`, `journal-entry`, `lint-claims`, `check-epic-signoff`, `board-gen`,
  `validate-workspace`, `check-commit-refs`, `check-verify-freshness`.
- Status: fixed (commit 418eb9e). All ten entry points answer `--help` and `-h` with their usage block: new-item, transition, run-gate, board-gen, validate-workspace, check-commit-refs, check-verify-freshness, journal-entry, lint-claims, check-epic-signoff.

## F-027 — a question can bundle two decisions, and the record loses one
- Severity: UX, low
- Component: methodology (refine, intake), spec/question.md
- Symptom: the sim, turn 3: "Q-001 folded a scope question ('is either optional') into what read
  like a simple ordering question — I answered both halves, but it is the kind of question that
  could get logged as just 'ordering answered' when a scope refusal was also in it."
- Counter-evidence, and it matters: by turn 9 the same stakeholder wrote the opposite — "the team
  correctly split the old EP-001/Q-002 into two separate questions on WI-0003 — one that needs my
  file and one that doesn't". So this is one question, not a habit.
- Evidence: evidence/iteration-1d/run/SIM-LOG.md turns 3 and 9
- Direction: `spec/question.md` already says "One question… If there is more than one, file more
  than one question", so the contract is right and nothing checks it. The mirror of F-020: F-020
  says do not split one decision across files, this says do not merge two into one.
- Status: fixed (commit 54b67ee), as a body rule rather than a check. `spec/question.md` §2
  (revision 4) states it with the consequence attached — a folded question gets half-answered and
  half-recorded — and `refine` step 4 carries it. Not mechanised: deciding whether a paragraph
  contains one decision or two is exactly the judgement F-001 says a linter cannot make, and a
  bad heuristic here would push authors toward vaguer questions.

## F-028 — a deferred answer has no representation, and it undermines the F-011 fix
- Severity: correctness (methodology gap on the escalation protocol)
- Component: spec/question.md, methodology (answer-questions, next)
- Symptom: the stakeholder answered EP-001/Q-002 with "I'll send you a sample later", which is
  neither an answer nor silence. The worker: "the question protocol has no way to represent a
  deferred answer without either deadlocking `next` or overstating what was settled." Leave it
  `open` and `next` stops on it forever; mark it `answered` and the record claims a thing was
  settled that was not.
- Consequence for this session's own work: F-011's fixed precondition treats "addressed-to `human`
  with `## Answer` non-empty" as answerable, and a deferral is non-empty. The fix is right for the
  case it addresses and blind to this one.
- Evidence: evidence/iteration-1d/run/004-worker.status.md; SIM-LOG turns 3, 9 and 13
- Direction: a third question status, `deferred`, carrying what the stakeholder said and what
  would unblock it. `next` does not stop on it, the item does not resume, and the record says
  exactly what happened instead of choosing between two lies.
- Status: fixed (commits 4aacb6c, 54a63b9, 0d22fb6), as filed, with one addition the filing did
  not anticipate. `spec/question.md` §2 defines `status: deferred`: `## Answer` carries what the
  person actually said, verbatim; `## Consequences` carries **what the pipeline did instead**,
  naming files. `next` does not stop on it (`pipeline.yaml`'s `runnable` says so explicitly) and
  the item does not resume.
  **The addition:** a deferral is not automatically a *deferred question*. `answer-questions`
  step 3a is two moves and it must take one — decide under the deferral, in which case the
  question is `answered` and quotes it as the basis ("go ahead anyway" settles a question by
  authorising a choice); or record `deferred` and move the item `awaiting-answer → blocked` with
  what would unblock it. Without that fork the status would have become a comfortable third
  option — mark it deferred, carry on — which is the failure the finding describes with a nicer
  name on it.
  **Enforced, not just described.** `validate-workspace` reports `question.deferred.not-blocked`
  when an item carries a deferred blocking question and is not at `blocked`; `deferred` requires
  `answered-at`, `answered-by` and both body sections, because a reply is a reply. The gate
  `a-deferral-is-not-an-answer` asks which of the two moves was taken. Must-fail case:
  `fixtures/broken-workspace` WI-0003.

## F-029 — three skills need to create items and only two may
- Severity: correctness, structural (a second instance of F-013's shape)
- Component: methodology/pipeline.yaml, answer-questions, review-close
- Symptom: two independent occurrences in one run.
  1. `answer-questions` accepted an answer that widened scope and could not record the implied
     work: only `intake` may create an item at `draft`, and `tracker/requests/` is `from: human`
     by rule (F-021).
  2. `review-close`'s D12 audit found a defect belonging to a closed item and could not file it:
     "`pipeline.yaml` lets only `verify` create an item at `ready` and only `intake` at `draft`,
     while `review-close`'s SKILL.md instructs it to file one — contract and pipeline disagree."
- Evidence: evidence/iteration-1d/run/004-worker.status.md, 012-worker.status.md
- Direction: decide which skills may create items and make `pipeline.yaml`, the transitions table
  and the process contracts agree. `review-close` has the same standing as `verify` to file a
  defect it found. Same failure shape as F-013: an instruction the state machine cannot execute.
- Status: fixed (commits 4dfa6e2, 4aacb6c, 0ada0ca, 54a63b9, 0d22fb6, 6c70f84), by derivation
  rather than by adding the two missing rows. `meta/adr/ADR-0006` §3 enumerates the events that
  change an engagement's item set and reads the authority table off that enumeration; the rule
  that comes out is **a skill may create an item exactly when it is the skill that observes the
  need for it, and only if it records what caused the item to exist.**
  That rule excludes `plan` and `implement` for a reason rather than by omission — `plan`
  observes uncertainty, which is a question, and `implement` observes scope creep, which is a
  question too — and it turned up a **third** occurrence nobody had filed: Definition of Ready
  **R9** instructs `refine` to split an item, and `refine` could not create the part it split off
  either.
  `spec/ids-and-statuses.md` §5 is the table; `pipeline.yaml` 0.4.0's creation rows carry
  `provenance`; `arose-from` is a new item field that must resolve (on a bug, `found-in` answers
  it, because it already names what caused the bug to exist). Three enforcement points:
  `scripts/new-item` **refuses** a creation the pipeline does not permit and refuses one with no
  provenance; `validate-workspace` reports `item.arose-from.missing` / `.unresolved`;
  `lint-skills` reports `transition.creation.provenance` on a creation row that declares none.
  Proven by execution in `./scripts/check` — twelve cases against a workspace built by the real
  tools, including `plan` refused a bug, `review-close` allowed one, and both of the run's own
  occurrences.

## F-030 — `priority` is doing two jobs, so the board lies about what matters
- Severity: UX / correctness of the record
- Component: spec/work-item.md, methodology (refine, plan)
- Symptom: the worker lowered WI-0003's `priority` to `medium` purely to order it last, on an item
  the stakeholder had explicitly called non-optional, and then wrote prose in three files saying
  that this is scheduling and not importance. "A lot of prose to work around a missing field."
- Evidence: evidence/iteration-1d/run/004-worker.status.md
- Direction: separate ordering from importance — a `sequence`/`after` field, or let `depends-on`
  carry soft ordering — so the board's priority column means one thing.
- Status: **deferred**, gated on the sprint-ceremonies / multi-item-parallelism track
  (ROADMAP §3, last). Triaged 2026-08-30 (META-128): with one runnable item at a time the
  board cannot mislead about what is next, so the field only lies when there is a queue — and
  that track is where a queue first exists. Adding a `sequence` field before then would be a
  schema change with no run able to exercise it

## F-031 — an `[auto]` Definition of Ready check that only tests file existence
- Severity: correctness (F-001's class, in a machine-decidable gate)
- Component: spec/dor-dod.md (R8), scripts
- Symptom: the worker: "DoR R8 is an `[auto]` check on `refinement-qa.md`. When `refine` is
  interrupted before the conversation happens, the honest thing is to write the agenda down for
  the next session — but a file that merely exists could read to an automated check as R8
  satisfied." Mitigated with a banner; suggests a `status:` field the checker reads.
- Evidence: evidence/iteration-1d/run/004-worker.status.md
- Direction: R8's check reads a field, not a filename. A mechanical gate that checks the wrong
  thing is worse than a manual one, because it is trusted.
- Status: fixed (commit d8dcd98), as filed. `artifacts/refinement-qa.md` opens with frontmatter
  declaring `status: agenda` or `status: recorded` (`spec/workspace-layout.md` §1.3);
  `validate-workspace` reports `artifact.refinement-qa.not-recorded` when an item reached `ready`
  on an agenda; `refine` step 8 says which to write and says not to write `recorded` on a file it
  intends to finish later. Must-fail case: `fixtures/broken-workspace` WI-0003 reaches `ready` on
  an agenda. `examples/toy-project`'s three artifacts were migrated — a migration, not a rewrite:
  the Q&A in them was recorded, so the field is true of each.

## F-032 — a filed question has nowhere to put the answer
- Severity: correctness, and it is the stakeholder's first impression of the protocol
- Component: scripts/validate-workspace, spec/question.md, methodology (refine)
- Symptom: the sim, turn 5: "none of these five questions had an `## Answer` section in the file at
  all — refine's template for this batch stopped at 'Options considered.' I had to add the heading
  myself to put my answer somewhere." `validate-workspace` requires `## Answer` and
  `## Consequences` to be non-empty only once `status: answered`, so a question filed without them
  is legal.
- Evidence: evidence/iteration-1d/run/SIM-LOG.md turn 5
- Direction: both headings must exist from the moment a question is filed — empty is fine, absent
  is not — enforced by the validator and stated in `question.md`'s body rules.
- Status: fixed (commit 418eb9e). `question.section.missing`: a filed question must carry `## Answer` and `## Consequences` from the moment it exists, empty until answered. `spec/question.md` §2 revision 3 says so; fixture case added.

## F-033 — `lint-claims` exits 0 having checked nothing when handed a file path
- Severity: **correctness, severe** — a gate that reports success when it could not look
- Component: scripts/lint-claims (introduced by this session, META-086)
- Symptom: the worker: "lint-claims silently ignores explicit file paths and reports 'checked the
  whole tree' with exit 0 — so a skill self-checking with file arguments can believe it passed a
  gate it never ran." Cause: `main()` does `options.setdefault("root", token)`, so the first
  positional becomes the workspace root; `lint-claims docs/architecture/overview.md` sets root to
  that file, finds no `docs/` beneath it, and exits 0 — while printing a scope line asserting the
  opposite.
- Consequence beyond the bug: the worker built a rule of thumb on top of it — "`--changed-since`
  is stricter than the whole-tree run" — which is impossible (`--all` lints a superset) and is
  only explicable by the whole-tree run having checked nothing.
- Why `scripts/check` missed it: both of its steps pass `--root`.
- Evidence: evidence/iteration-1d/run/006-worker.status.md, 014-worker.status.md
- Direction: accept explicit file and directory arguments and lint exactly those; or refuse an
  argument that is not a workspace, naming `--root`. Never exit 0 having examined nothing, and
  never print a scope line that is not what was scoped. Must-fail fixture: `lint-claims <file with
  an unsourced absolute claim>` exits non-zero.
- Status: fixed (commit 418eb9e). Files named on the command line are linted as files; one directory is a workspace root; a path that does not exist is an error; passing both is an error. The scope line reports what was actually examined, including "no documents changed since <ref>". Demonstrated: `lint-claims fixtures/broken-workspace/docs/architecture/overview.md` exits 1 with both rules firing.

## F-034 — `plan` writes source files so that its own gates can run
- Severity: contract/spec conflict
- Component: methodology/plan, spec/workspace-layout.md §5
- Symptom: `plan` created empty `expenses/__init__.py` and `tests/__init__.py` "solely so the test
  and lint commands could be run before being recorded, as the skill's own self-check demands",
  and flagged it under the plan's `## Risks`. `plan` is specified as producing no code.
- Evidence: evidence/iteration-1d/run/006-worker.status.md
- Direction: either the self-check stops requiring a command to have been run, or the "no code"
  rule gains an explicit carve-out for scaffolding a command needs to execute at all.
- Status: fixed (commit d8dcd98) — the carve-out, decided in `meta/adr/ADR-0007` and bounded
  four ways. The rejected option is the interesting half: dropping the "have you run it"
  requirement and letting `implement` create the scaffolding are the same option in two hats, and
  both end with a plan recording a gate command nobody has executed — F-001's class, failing at
  the most expensive moment. `plan` may create a file outside `tracker/` and `docs/` only when a
  declared command cannot execute at all without it, the file contains **no behaviour**, it is
  listed under a new required `## Scaffolding` heading with the command that needed it, and no
  acceptance criterion depends on it. A stub function with a `pass` body is explicitly not
  scaffolding — that is an interface decision, and it belongs in the plan where a reviewer can
  argue with it. `spec/workspace-layout.md` §5 carries the rule; `plan` → 0.3.0. It is a
  `[skill]` bound and the ADR says so: nothing mechanically separates an empty package marker
  from a small implementation.

## F-035 — `check-commit-refs` reports a merge that never happened
- Severity: UX, misleading
- Component: scripts/check-commit-refs
- Symptom: on the opening `in-progress` transition of a branch with no commits yet, `trunk..branch`
  is empty and the merged-ancestor test is trivially true, so the gate prints "already merged into
  main… rewind the merge, close, then merge" — advice for a situation that does not exist.
- Evidence: evidence/iteration-1d/run/007-worker.status.md
- Direction: distinguish "empty because nothing is committed yet" from "empty because it was
  merged" — the branch head equalling the trunk head separates them.
- Status: **fixed** — a branch pointing at the same commit as the trunk has nothing on it; a
  branch behind the trunk was merged. The two now get different messages, and the fresh-branch
  one says plainly that there is nothing to rewind
  small and self-contained: the branch head equalling the trunk head separates "nothing is
  committed yet" from "already merged", and the message follows from that

## F-036 — `new-item` leaves the workspace invalid and does not say so
- Severity: UX
- Component: scripts/new-item
- Symptom: it writes the history row (actor = the creating skill) and no journal entry, so
  `journal.execution.missing` fires until the skill journals the creation — correct behaviour, and
  the success message says nothing about it.
- Evidence: evidence/iteration-1d/run/007-worker.status.md
- Direction: the success output names the next required step and the exact `journal-entry`
  command. The worker also noted that `journal-entry` requires a `**Status:**` bullet on an entry
  that records no transition; that is `spec/journal-and-history.md` §2.2 as written (such an entry
  reads `X` → `X` (unchanged)), so what is missing is only that the error message does not say so.
- Status: **deferred** as one of the four-finding *half-written record* class — with F-043,
  F-051 and F-053 — gated on the next builder session's first unit. Triaged 2026-08-30
  (META-128); see the triage note below for why they move together

## F-037 — the citation rule made the append-only rule unsatisfiable
- Severity: **structural, severe** — one invariant added this session broke another
- Component: scripts/lint-claims, scripts/validate-workspace, spec/doc-header.md §4a
- Symptom: a `[src: ...]` marker in `WI-0003/Q-002` used a form §4a does not define, so
  `validate-workspace` failed after the transition had applied. The correcting journal entry
  described the defect **by quoting the malformed marker verbatim** — and `lint-claims` read the
  quotation as a citation and failed on that too. In the worker's words: "Fixing it required
  rewriting one sentence of an append-only journal entry, since no appended entry can remove a
  line the linter rejects. That rewrite is recorded in full in a third entry on WI-0003, including
  that it violates `spec/journal-and-history.md`'s append-only rule and does not fall under its
  single sanctioned exception."
- Why this is the worst finding of the run: the record could not describe its own defect without
  reproducing it, so the only way forward was to break the invariant the whole audit trail rests
  on. A rule that forces that is worse than the rule's absence.
- Evidence: evidence/iteration-1d/run/008-worker.status.md, 010-worker.status.md;
  evidence/iteration-1d/project/tracker/items/WI-0003/journal.md
- Direction (the worker's, and it is right): a `[src: ...]` inside an inline code span or a fenced
  block is a **quotation**, not a citation, and is skipped. `lint-claims` already skips fences for
  the absolute-claim rule; the citation scan skips nothing, and neither does
  `validate-workspace.check_claim_citations`. Must-fail fixture both ways: a bare malformed marker
  still fails, the same marker in backticks does not.
- Status: fixed (commit 418eb9e). `mask_code()` blanks inline code spans preserving lines and columns; `masked_lines()` also blanks fenced blocks; `lint-claims` (both rules) and `validate-workspace.check_claim_citations` read through it. Fixtures both ways: `fixtures/sourced-claims` now contains a paragraph describing a malformed marker **by quoting it** — a paragraph that could not have existed before this fix — and `fixtures/broken-workspace` carries the same marker bare, which still fails.

## F-038 — a transition can leave the tracker committed-invalid
- Severity: correctness, minor (documented behaviour, undocumented window)
- Component: scripts/transition, spec/skill-contract.md
- Symptom: the worker: "transition applied WI-0003's move and then reported the workspace no longer
  validates, correctly noting the failing gate was not blocking that move — the behaviour is right
  and clearly explained, but it does leave a window in which the tracker is committed-invalid if
  the caller stops there."
- Evidence: evidence/iteration-1d/run/008-worker.status.md
- Direction: state the window in `spec/skill-contract.md` §2.3 rather than leaving it as folklore.
  The alternative — validate the post-move state and roll back — means truncating an append-only
  file, which META-090 rejected for that reason.
- Status: fixed (commit d8dcd98), as filed, plus the obligation the window creates. §2.3 now says
  both things: the behaviour is correct (a gate that is not blocking this move must not block it,
  and rolling back means truncating an append-only file), **and** a skill that transitions an item
  MUST NOT end its execution while `validate-workspace` reports errors — fix them, or name each
  finding and why it is not yours to resolve. Committing a workspace you know does not validate,
  without saying so, is the failure; committing one and saying so is a handover.

## F-039 — `transition` validates the journal body only after writing the history row
- Severity: correctness (a malformed body costs a manual repair on an append-only file)
- Component: scripts/transition, scripts/journal-entry (introduced by this session, META-084)
- Symptom: reported on turns 8 and 10. The row-first ordering is deliberate and right; the *body
  check* happening after it is not.
- Evidence: evidence/iteration-1d/run/008-worker.status.md, 010-worker.status.md
- Direction: validate the body before touching `history.md`, then write the row, then append the
  entry. `journal-entry.check_body()` is already a pure function; call it early. Nothing about the
  ordering needs to change.
- Status: fixed (commit 418eb9e). `transition` reads and checks the journal body before it touches `history.md`, using `journal-entry.check_body()`. The row-first ordering chosen in META-090 is unchanged. Demonstrated: a body missing `**Result:**` leaves `history.md` byte-identical.

## F-040 — a repeated `src:` prefix is rejected and the message blames the citation
- Severity: UX
- Component: scripts/lib/claims.py (introduced by this session, META-086)
- Symptom: `spec/doc-header.md` §4a separates several sources with `;` inside one marker, i.e.
  `[src: A; B]`. An author writing `[src: A; src: B]` gets `" src: B"` after the split, which
  matches no form, and the error says the citation is unrecognised rather than that the prefix is
  repeated.
- Evidence: evidence/iteration-1d/run/011-worker.status.md
- Direction: strip a leading `src:` from each part; if it still fails, say which part and why.
- Status: fixed (commit 418eb9e). A leading `src:` is stripped from each `;`-separated part, and if the part still fails the message says the prefix was repeated and how the syntax works.

## F-041 — `validate-workspace` lints files the workspace does not track
- Severity: correctness (scope)
- Component: scripts/validate-workspace (introduced by this session, META-086)
- Symptom: the worker: "validate-workspace lints this git-ignored status file, so a status report
  cannot quote a malformed citation to describe the problem." `check_claim_citations` walks every
  `*.md` under the root, `.gitignore` included.
- Evidence: evidence/iteration-1d/run/011-worker.status.md
- Direction: skip paths git ignores, falling back to current behaviour outside a repository. F-037's
  code-span rule is the more general half of the same answer.
- Status: fixed (commit 418eb9e). Both `lint-claims` and `validate-workspace` skip paths git ignores, falling back to the old behaviour outside a repository.

## F-042 — see F-029
Merged into F-029; both occurrences of "a skill is told to create an item it may not create" are
filed there. Fixed with it (see F-029's status); the derivation found a third occurrence —
Definition of Ready R9's split — that neither filing had noticed.

## F-043 — `--outcome` is unreachable in practice and named in no contract
- Severity: UX (a working flag went unused, and the workaround is hand-editing `item.md`)
- Component: scripts/transition, methodology/review-close
- Symptom: the worker: "transition refuses an outcome set before the move and then reports the
  workspace invalid for the missing outcome after it, so the only working order is transition,
  edit item.md, re-validate; `--outcome` exists as a flag but the skill never mentions it."
- Evidence: evidence/iteration-1d/run/012-worker.status.md
- Direction: name `--outcome` in `review-close`'s closing step, and find out why setting the field
  before the move is refused. Hand-editing `item.md` is precisely what the tooling exists to remove.
- Status: **deferred** with the *half-written record* class (F-036, F-051, F-053), gated on the
  next builder session's first unit. Triaged 2026-08-30 (META-128)

## F-044 — `transition` does not escape `|` in `--reason` and corrupts `history.md`
- Severity: **correctness, severe** — silent record corruption after a reported success
- Component: scripts/transition, scripts/validate-workspace
- Symptom: the worker: "a reason containing a union type corrupts the history row and breaks
  validation after a transition the tool reports as successful; the resulting validator errors do
  not name the cause." `history.md` is a markdown table, so an unescaped pipe splits the row into
  extra cells and the item's whole chain misparses. Repaired and journalled on BUG-0001 by the
  worker.
- Evidence: evidence/iteration-1d/run/014-worker.status.md
- Direction: escape `|` when writing the reason cell (check `journal-entry` for the same class),
  and make the validator's row-shape error name an unescaped pipe as the likely cause.
- Status: fixed (commit 418eb9e) — **and it needed two halves.** `transition` escapes `|` and backslashes in the reason cell, *and* `scripts/lib/workspace.split_row()` splits history rows on unescaped pipes and unescapes as it goes; `transition`'s four private copies of that split now use it. Escaping without a reader is decoration: the first attempt produced a row that rendered correctly and parsed into seven columns, which is exactly how the corruption stayed invisible in 1d. Selftest covers both.

## F-045 — the epic sign-off gate does not fire on a run that ends in an impasse
- Severity: methodology gap (the acceptance loop, incomplete — F-022's fix is half a fix)
- Component: methodology/review-close, scripts/check-epic-signoff, spec/dor-dod.md
- Symptom: `check-epic-signoff` gates `review-close`'s completion transition `open → done`, and
  DE1 requires every child `done` — so an epic with a `blocked` child never reaches the gate and
  the stakeholder is never asked. Both sides of the engagement reached this independently: the
  worker, "EP-001 correctly stays open because DE1 fails, so the DE7 sign-off question is not yet
  due"; and the stakeholder, who went looking — "no `kind: sign-off` question was ever filed
  anywhere: I grepped for it and found the phrase only in journal prose, scripts and spec docs,
  never in a question's own frontmatter."
- The stakeholder on why it matters, verbatim: "I expected that before anyone called this
  engagement finished, someone would ask me straight out whether I accept it as it stands — and I
  was ready to say no… That question never came. The board and the epic both make it clear enough
  on their own that this isn't finished… But if this had ended with a report calling it 'done,'
  I'd have had no record of ever being asked, and that's the part I'd have pushed back on hardest."
- Evidence: evidence/iteration-1d/run/SIM-LOG.md turn 15; run/016-worker.status.md
- Direction: an epic **ends** when it is closed or when it can no longer progress, and the sign-off
  belongs to both. File it when every remaining child is `blocked` or `done` and no question is
  open — restating the goal, what was delivered, what is stuck and why — and let the epic close
  with an outcome recording the answer, or stay open.
- Status: fixed (commits 4dfa6e2, 4aacb6c, 0ada0ca, 8ddd968, 0d22fb6, 6c70f84), as the direction
  says, derived rather than patched. `meta/adr/ADR-0006` enumerates the **four** legal endings —
  delivered, delivered-partial, impasse, abandoned — and every one of them passes through a
  blocking human-addressed question stating what was delivered, what was not, and why. F-022's
  gate stops being a *completion* gate and becomes a **termination** gate.
  The trigger is **rest**, not closure: every child at a terminal status, no question open
  anywhere in the engagement, no request open. `scripts/lib/engagement.py` decides it and both
  consumers read the same function — `scripts/engagement-state`, which `next`'s new orchestrator
  step 6 reads, and `check-epic-signoff`, which dates the acknowledgment against it. The
  orchestrator and the gate disagreeing about whether an engagement is over is precisely how this
  finding happened.
  Two things had to change for the impasse ending not to be a hole the same size. `pipeline.yaml`
  transitions declare `applies_to`, so the generic `any-suspendable → blocked` row no longer
  matches an epic and only `review-close` may end an engagement; and they declare `gated`, so
  `transition` **refuses** `open → blocked` while the gate fails — without it the ending would
  have run the acknowledgment gate and ignored its verdict, because `transition` blocks only a
  skill's `next_status`.
  Proven by execution in `./scripts/check`: `review-close` moving an epic to `blocked` with no
  acknowledgment is refused by a hard gate. `fixtures/ended-engagement` EP-003 is the static
  case — at rest, nobody asked — and EP-001 is the impasse ending done right, with the
  stakeholder saying no.

## F-046 — a bug the pipeline filed is never shown to the stakeholder
- Severity: UX, low (largely the same gap as F-045)
- Component: methodology (review-close, next)
- Symptom: the sim, turn 15: "There's also a bug sitting at `planned`… that I was never told about
  and that isn't fixed either, so strictly the whole thing isn't done even setting the import
  aside — but nobody ever asked me about that one and I have no view on it worth recording."
- Evidence: evidence/iteration-1d/run/SIM-LOG.md turn 15
- Direction: the sign-off (F-045) is the moment the whole picture is shown. Fold in.
- Status: fixed (commits 4aacb6c, 8ddd968, 6c70f84), folded in as the direction says — and it
  stopped being a separate fix once DE1 was re-derived. The termination question MUST **name
  every child item of the epic**, by ID, each marked delivered or not with one line of why, and
  `check-epic-signoff` checks the naming. "List what was not delivered" cannot be checked and
  "name every child" can; a bug the pipeline filed and never fixed is a child, so it is in the
  statement whether or not anyone remembered it.
  DE1 changed with it: "every child item is `done`" was the entry condition for one ending out of
  four, and what replaces it is "every child is at a terminal status, and every child that was
  not delivered is named". An epic that closes over an undelivered child may not record
  `outcome: delivered` — `validate-workspace` reports `epic.outcome.overclaims`. Must-fail case:
  `fixtures/ended-engagement` EP-002, whose statement names the delivered child and quietly omits
  the bug.

## F-047 — an empty `questions/` directory breaks an item at the moment of closing
- Severity: correctness (F-002's class, with a much sharper consequence)
- Component: scripts/new-item, scripts/workspace-init
- Symptom: the worker: "an item with no questions has an empty `questions/` directory that git
  cannot track, so the trial merge `review-close` is required to perform deletes it and
  `validate-workspace` fails with `questions.missing` at the moment of closing — worked around with
  a `.gitkeep`; `new-item` should create it."
- Evidence: evidence/iteration-1d/run/016-worker.status.md
- Direction: fold into F-002. Every directory the schema requires gets a `.gitkeep` from the tool
  that creates it — `workspace-init` **and** `new-item`. F-002 predicted the fresh-clone symptom;
  1d found it failing a close instead, which is worse.
- Status: fixed (commit 20fc6a7) with F-002. `new-item` writes `.gitkeep` into both `questions/`
  and `artifacts/`, so an item with neither still survives a clone and, more to the point,
  survives the trial merge `review-close` performs while closing it.

## F-048 — `plan` wrote a step instructing `implement` to break a spec rule
- Severity: correctness, low (the enforcement held)
- Component: methodology/plan
- Symptom: "BUG-0001's plan step 7 instructed `implement` to tick the acceptance criteria, which
  `spec/work-item.md` reserves for `verify`. `implement` declined and declared it, and review
  agreed — but `plan` should not be writing steps that tell a downstream skill to break a spec
  rule."
- Evidence: evidence/iteration-1d/run/016-worker.status.md
- Direction: `plan`'s self-check gains "no step instructs another skill to do something its
  contract forbids". Worth recording that the system behaved correctly here: the instruction was
  refused, the refusal was declared, and the review agreed — all three positions are in the record.
- Status: **fixed** — `plan` 0.4.1: self-check question 2 is *"does any step instruct a
  downstream skill to do something its contract forbids?"*, naming the three that recur (ticking
  a criterion, writing to `docs/`, ending an engagement), with a matching exit criterion. Kept as
  prose deliberately: reading intent out of a plan step is not something a program does, and the
  run this came from is evidence the enforcement below it holds either way
  self-check line in `plan`'s procedure, and the run it came from is the evidence that the
  enforcement below it held

---

### Addendum to F-002 (2026-08-22, iteration 1d)
1d found the same defect in `new-item` rather than `workspace-init`, and failing at a worse
moment: an item's empty `questions/` directory is deleted by the trial merge `review-close`
performs, so the item fails `questions.missing` *while being closed*. See F-047. Fix both tools
together.

### Addendum to F-022 (2026-08-22, iteration 1d) — the fix is half a fix
The mechanism works and is proven by fixtures and by demonstration, and 1d never exercised it: an
epic with a `blocked` child never reaches `open → done`, so the gate is never evaluated and the
stakeholder is never asked. Filed as **F-045**. F-022 remains `fixed` for what it claims — an epic
cannot *close* without acceptance — and the larger claim, that a stakeholder gets a say at the end
of an engagement, is not yet true.

### Addendum to F-011 (2026-08-22, iteration 1d)
The rewritten precondition treats "addressed-to `human` with `## Answer` non-empty" as answerable.
A **deferral** is non-empty: 1d's stakeholder answered "I'll send you a sample later" three times.
So the fix is right for the case it addresses and blind to a case the same run produced
immediately. See **F-028**.

## H-008 — the driver calls an impasse on one blocked item, not on the engagement
- Severity: correctness, severe for the evidence — it ends a run with most of its work unbuilt
- Component: harness/run_iteration.py (`decide`)
- Symptom: found live, during iteration 1e, at turn 6. `WI-0003` was parked at `blocked` on turn
  4 (the F-028 deferral fix working exactly as designed), while `WI-0001` was at `planned` and
  `WI-0002`/`WI-0004` were still at `draft`. The driver's rule is
  `if observed["blocked-items"] and not open-human-questions` → give the sim its one closing turn,
  then stop with `blocked-no-recourse`. It announced *"an item is blocked with nothing open to the
  stakeholder; giving the sim one closing turn before accepting the impasse"* with three of four
  items still to build, spent H-007's single closing turn, and would have stopped terminally after
  the next worker turn.
- Cause: the rule tests a fact about **one item** — "an item is blocked" — and calls it a fact
  about the **engagement** — "the run reached an impasse". Those coincided in every run so far
  because the blocked item was always the last one standing: 1d reached `blocked` at turn 14 of
  16. F-028's fix removed the coincidence by parking the blocked item ten turns earlier.
- Consequence beyond the run: the stop is **terminal**, so a rerun refuses to continue it. Had
  this been noticed after the fact rather than during, 1e's evidence would have been a run that
  stopped two thirds of the way through for a reason with nothing to do with the toolkit.
- Evidence: harness/runs/iteration-1e-expenses/iteration-log.jsonl turn 6; the workspace at that
  moment (`WI-0001` planned, `WI-0002`/`WI-0004` draft, `WI-0003` blocked, `EP-001` open).
- Direction: test the engagement, not the item. The toolkit already defines it
  (`spec/ids-and-statuses.md` §3.5, ADR-0006 §4): **at rest** = every non-epic item at a terminal
  status and no question open anywhere. And a second condition the derivation supplies — at rest
  with the epic still `open` means the engagement is over and its ending is **not recorded**, so
  the next turn belongs to the worker, which is the turn that asks the stakeholder (F-045).
  Stopping there is stopping one turn before the thing the run exists to observe.
- Status: fixed (commit 3b6a94b). `engagement_at_rest()` and `engagements_ended()` in
  `harness/run_iteration.py`, computed from what the driver already scans rather than by calling
  the toolkit — the driver must keep working against a project whose toolkit is broken. Three
  branches now: not at rest → say so and carry on; at rest with the ending unrecorded → a
  **worker** turn; ended → the closing turn, then the stop. Six new tests in
  `harness/tests/test_harness.py` (53, was 47), including the exact 1e shape: a blocked item
  beside work in flight is not rest.
- Recovery applied to the in-flight run, recorded here because it was a hand edit of
  `state.json`: `closing-turn-given` was cleared (H-007's one closing turn had been spent by the
  defect, on a run that had not ended), and `next-role`/`next-job` were changed from
  `sim`/`closing` to `worker`/`null` — the decision the fixed code makes at that state. The
  killed turn 7 sim wrote nothing to `SIM-LOG.md`; its partial transcript is left in place under
  `turns/007-sim.*` rather than deleted, and turn 7 re-ran as a worker turn.

### Addendum to F-013 (2026-08-27, builder 2.5) — re-derived, not reversed
F-013's fix stands exactly as it was: `terminal` and `suspendable` are different questions, and an
epic at `open` is both. What changed is that it is now a **consequence** rather than a repair.
`meta/adr/ADR-0006` derives the status graph from the set of legal endings, and the same
distinction falls out on the way — an epic *lives* at `open`, which is why `open` is terminal
(the pipeline does not advance it) and suspendable (a person's question may stop it), and why
`open` is not an ending even though it is terminal.

That third appearance was useful: my first attempt at the lint rule "an epic's ending must be
gated" defined an ending as "an epic-scoped move into a terminal status", and it caught `→ open`.
The test that works is **terminal and not suspendable**. Same confusion, three years of runs
apart, caught by a rule this time instead of by a run.

F-013's own defect is now a mechanical must-fail case rather than a demonstration somebody
performed once: `./scripts/check` reintroduces `open: suspendable: false` into a copy of
`pipeline.yaml` and asserts `pipeline.status.unsuspendable` comes back.

### Addendum to F-022 (2026-08-27, builder 2.5) — the other half
The 2026-08-22 addendum said F-022 was half a fix: the mechanism worked and the larger claim,
that a stakeholder gets a say at the end of an engagement, was not yet true. It is now the claim
F-045's fix makes, and F-022 is unchanged — an epic still cannot *close* without acceptance. What
was added around it is that closure is one of four endings, and the other three are gated too.

### Addendum to F-011 (2026-08-27, builder 2.5)
The 2026-08-22 addendum recorded that F-011's precondition was blind to a deferral, because a
deferral is a non-empty `## Answer`. F-028's fix closes it: the precondition still says
"addressed-to `human` with `## Answer` filled in", and `answer-questions` step 3a now decides what
that reply *was*. "Replied" and "answered" are different things and the protocol says so.

---

# Iteration 1e — the findings pass (2026-08-27, builder 2.5)

Trail: `meta/harness/evidence/iteration-1e/`. Every finding below was found by the worker or the stakeholder during the run;
none was found by reading code afterwards. **H-008** was filed during the run and is above.
Reproductions of already-open findings are recorded as addenda, not re-filed.

## F-049 — the SKILL.md files say the tool writes the `**Status:**` bullet; the tool refuses a body without one
- Severity: UX, high frequency — the most-hit friction of the run
- Component: methodology (plan, implement, verify, review-close, refine, answer-questions), scripts/transition
- Symptom: every `## Journaling` section says *"the transition … writes the `**Status:**` bullet
  itself from the move it actually made"*, which reads as *you need not write one*.
  `scripts/transition --journal-body-file` **requires** the bullet to be present and then
  rewrites it, exiting 1 with `the journal body is not a legal entry — missing the '**Status:**'
  bullet`. The worker, turn 2: *"The caller therefore has to write a Status bullet that the tool
  then overwrites, which is exactly the duplication F-019 was meant to remove."*
- Frequency: **six occurrences across five turns** (2, 11, 12, 13, 15, 16) and four different
  skills, each costing a failed transition and a re-run. Turn 13: *"Turn 12 reported it against
  `implement`; the wording is identical in `verify` and `review-close`, so the one-word fix
  belongs in all three."*
- The same class, smaller: `**Commands:**` and `**Artifacts:**` are also structurally mandatory
  and unmentioned in the prose. Turn 14: the opening `implement` entry *"was refused for a
  missing `**Artifacts:**` bullet, which is awkward precisely because that entry has no artifacts
  yet."*
- Evidence: meta/harness/evidence/iteration-1e/run/002-, 011-, 012-, 013-, 015-, 016-worker.status.md
- Direction: the prose is wrong and the script is right — `journal-entry --template` already
  prints the bullet. Say **"rewrites"** rather than "writes" in every `## Journaling` section,
  name the structurally mandatory bullets, and have the error message say the bullet's content is
  ignored so the reader knows the template is the answer.
- Status: fixed (commit 5b615ec) — **both sides gave, in different places.** The tool
  first: `force_status_bullet` could already insert a missing bullet, and `journal-entry` runs it
  *before* `check_body` while `transition` ran the check first — so the refusal protected
  nothing. When a transition supplies the move, the `**Status:**` bullet is no longer required of
  the caller; it is inserted where the schema puts it, before `**Result:**`. Standalone
  `journal-entry` still requires it, because there nothing else would write it, and a body
  missing `**Gates:**` is still refused either way — the exemption is one bullet wide.
  Then the prose, in all seven `## Journaling` sections: the transition writes the bullet
  "supply one and it is replaced, leave it out and it is inserted", and — for turn 14's second
  hit — **every** bullet `--template` prints is structurally required, `**Commands:**` and
  `**Artifacts:**` included, with `none` as the honest content. `spec/journal-and-history.md`
  §2.2 says the same thing normatively. Proven by execution in `./scripts/check` (4 cases):
  the body with no `**Status:**` bullet goes through the transition and the entry comes back
  carrying the move that was actually made. No new prose-versus-contract lint — that is F-059's
  class fix and it stays open.

## F-050 — an epic-level question cannot legally be `deferred`, and this session built that
- Severity: correctness, structural — **a defect in this session's own work**, and F-013's shape again
- Component: scripts/validate-workspace, methodology/pipeline.yaml (both changed at META-104/105a)
- Symptom: found by the worker on turn 4, reading the new rules against each other:
  `validate-workspace` applies `question.deferred.not-blocked` to **every item type**, requiring
  the item carrying a deferred blocking question to be at `blocked`; but `pipeline.yaml` scopes
  `awaiting-answer → blocked` for `answer-questions` to `work-item` and `bug`, and an epic may
  reach `blocked` only as the **E3 impasse ending through `review-close`**. So marking an
  epic-level question `deferred` produces a workspace that no legal move can repair.
- Consequence: the stakeholder's deferral in 1e arrived on an **epic-level** question
  (`EP-001/Q-001`). Had the architect taken step 3a's second move rather than its first, the run
  would have hit this. It took the first move — deciding under the deferral — so the defect was
  reported rather than suffered.
- Why it happened: `applies_to` was added to the transition table (ADR-0006 §2, so that only
  `review-close` ends an engagement) in the same session as the deferral status, and the two
  rules were never checked against each other on an epic. Exactly the failure ADR-0006 was
  written to stop: a rule derived for one item type applied to all of them.
- Evidence: meta/harness/evidence/iteration-1e/run/004-worker.status.md
- Direction: decide which gives. Either an epic-level deferral is legal and needs its own
  transition (`awaiting-answer → blocked` by `answer-questions`, `applies_to: [epic]` — and then
  it is an *ending* and must be gated) — or it is not, and `question.deferred.not-blocked` must
  exempt epics while `answer-questions` is told what to do with an epic-level deferral instead.
  The second is probably right: a deferred sign-off is E3, and E3 belongs to `review-close`.
- Status: fixed (commits a0e7db5, e1c55e9) — the second reading, and the class before the
  instance. **The class:** `pipeline.yaml` 0.5.0 carries a `rule_obligations` block naming, per
  validator rule that requires an item to be at one of a fixed set of statuses, the item types it
  applies to and the transition that satisfies it. `validate-workspace` *reads* that scope rather
  than deciding it, and refuses a pipeline that dropped an obligation it depends on
  (`pipeline.obligation.missing`); `lint-skills` checks each entry against the transition table
  in both directions — `obligation.unsatisfiable` when no row provides the move, and
  `obligation.applies_to.mismatch` when the scopes disagree, which is this finding in one
  direction and F-013 in the other. Two injected faults and one new `./scripts/check` step.
  **The instance:** a deferred blocking question on an epic returns it to `open` —
  `spec/question.md` §2, `answer-questions` 0.3.0 step 3a. That is not the resumption move 2
  forbids: an epic advances only through its children, so nothing proceeds on the strength of the
  missing thing; the engagement comes to rest, `next` step 6 dispatches `review-close`, and
  `check-epic-signoff` already accepts a deferred acknowledgment for `open → blocked` and refuses
  one for `open → done`. By execution: the move 1e's architect would have made on the other
  branch is refused, and the branch that is legal validates clean.

## F-051 — `new-item` writes the creation row and no journal entry, so a new item fails validation immediately
- Severity: correctness, minor but hit on every item created
- Component: scripts/new-item
- Symptom: the worker, turn 6: *"`scripts/new-item` writes a history creation row but no journal
  entry, so the workspace fails `journal.execution.missing` the moment an item is created and
  stays failing until the caller writes the entry by hand with `journal-entry --status`."*
  Every other status change has one command that writes both.
- Consequence: it is the committed-invalid window (F-038) opened by the tool that creates items,
  on every item, rather than by an unusual path.
- Evidence: meta/harness/evidence/iteration-1e/run/006-worker.status.md
- Direction: `new-item` takes `--journal-body-file` as `transition` does, or writes the creation
  entry itself. The rule that already exists — the row and the entry are written by one command —
  should hold at creation too.
- Status: **deferred** with the *half-written record* class (F-036, F-043, F-053), gated on the
  next builder session's first unit. Triaged 2026-08-30 (META-128)

## F-052 — `lint-claims --changed-since` reports a scope it did not have
- Severity: correctness — F-033's class, in the same script
- Component: scripts/lint-claims
- Symptom: reported on **three turns**. Turn 7: *"`lint-claims --changed-since main` reported
  'checked no documents changed since main' while on a branch that had added `README.md` and
  several tracker artifacts relative to `main`. Rule 1 did fire on `README.md` while the file was
  uncommitted, so the gate is not inert — but the summary line claims a scope it did not have,
  and a reader would take the exit-0 as broader coverage than it was."*
- The consequence, seen in the same run: every contracted `claims-are-sourced` gate is
  trunk-scoped, and *"three skills passed over BUG-0001's defect before `verify` found it with
  the whole-tree run"* (turn 15). The scoping is deliberate; the reporting is what misleads.
- Evidence: meta/harness/evidence/iteration-1e/run/007-, 008-, 015-worker.status.md
- Direction: the scope line must describe what was examined — how many documents, selected how.
  F-033 fixed this for the file-argument path; the `--changed-since` path says the same kind of
  untrue thing.
- Status: **fixed** — `scope_note()` describes what each rule actually examined, separately and
  on every run: how many documents, selected how, against which base sha, and where rule 1
  looked. A window that could not have contained anything is now a failing verdict rather than a
  quiet 'checked no documents' (commits 61fb2aa, d3c1234, 6a34d69). F-066 was the same defect a
  step further on — the misreported scope became a passing gate

## F-053 — `outcome` and `status: done` cannot both be written, in either order
- Severity: correctness — the F-014 mechanism does not model a dependent field
- Component: scripts/transition, scripts/validate-workspace, spec/work-item.md
- Symptom: the worker, turn 9: *"`spec/work-item.md` requires `outcome` if and only if
  `status: done`, but `transition`'s `--resolving` models only the status change. Setting
  `outcome: delivered` before the transition failed the pre-flight `workspace-valid` hard gate
  with `item.outcome.premature`; removing it let the transition through, which then reported
  'the transition was applied, but the workspace no longer validates'."* Hit again at turn 16 —
  *"the outcome-before-transition trap in review-close step 9 (cost a failed transition)"*.
- Consequence: `review-close` must take a non-zero exit on a transition that actually succeeded,
  on every item it closes. That is the committed-invalid window (F-038) as the **normal** path.
- Evidence: meta/harness/evidence/iteration-1e/run/009-, 016-worker.status.md
- Direction: `transition` grows `--outcome` and writes it with the move, the way it already
  writes `--branch`; or `--resolving` teaches the validator that `item.outcome.premature` is
  resolved by the pending move to `done`. The first is simpler and matches an existing pattern.
- Status: **deferred** with the *half-written record* class (F-036, F-043, F-051), gated on the
  next builder session's first unit. Triaged 2026-08-30 (META-128). It is the most expensive of
  the four — `review-close` takes a non-zero exit on a transition that succeeded, on every item
  it closes — and that is an argument for fixing the class properly, not for fixing this one

## F-054 — `lint-claims` rejects a citation whose path is wrapped in backticks, with a misleading message
- Severity: UX
- Component: scripts/lib/claims.py, scripts/lint-claims
- Symptom: the worker, turn 11: *"`lint-claims` does not accept a citation whose path is wrapped
  in backticks … fails as `claim.citation.unresolved` with the same message an unresolvable path
  gets, which sends you looking for a missing file rather than a stray character."*
- Evidence: meta/harness/evidence/iteration-1e/run/011-worker.status.md
- Direction: strip surrounding backticks from a citation part before resolving it — writing a
  path in backticks is what all of this repository's prose does — or, if it must be rejected, say
  *why* rather than reporting it as unresolvable.
- Status: **fixed** — the real mechanism was the code-span *mask* (F-037's protection against a
  quoted citation), which blanked the inside of a real marker whose path was in backticks — the
  way all of this repository's prose writes a path — and reported `an empty citation`. Masking
  preserves offsets, so a marker that survives in the masked line is a real one and its body is
  read from the raw line. All four shapes are covered: a backticked path resolves, a genuinely
  broken one still reports, a wholly quoted citation is still skipped, and a mixed list works
  surrounding backticks from a citation part before resolving it, and keep a distinct message
  for anything still unresolvable

## F-055 — `review-close`'s "throwaway copy of the trunk" advanced the real trunk
- Severity: **correctness, severe** — the only finding in the run that caused real damage
- Component: methodology/review-close
- Symptom: step 8 says to trial-merge into *"a throwaway copy of the trunk"* and does not say how.
  The worker used `git worktree add /tmp/trial4 main`, which **checks out the real `main` branch**
  in a second directory rather than copying it, so the trial merge fast-forwarded the real ref —
  and removing the worktree did not move it back. Turn 12: *"the review's trial merge accidentally
  advanced the real `main`."*
- What saved it: `check-commit-refs` caught it immediately and its message named the fix; the
  worker rewound with no loss and wrote the rule into `review.md` and the item's journal. Turn 13
  used `git worktree add --detach` and checked `git rev-parse main` after the merge. So the
  enforcement held and the record is complete — but the methodology told a skill to do something
  dangerous without saying how to do it safely.
- Evidence: meta/harness/evidence/iteration-1e/run/012-, 013-, 016-worker.status.md
- Direction: name the command — `git worktree add --detach <path> <trunk>` — with one line on why
  `--detach` matters, and a self-check that the trunk ref is unchanged after the trial. A
  procedure that says "a throwaway copy" and leaves the mechanism to the reader will be
  implemented differently every time.
- Status: fixed (commit 63f8917), as filed. `review-close` 0.5.0 step 8.1 prints the four-line
  sequence — `git worktree add --detach <trial> {{trunk}}`, the `--no-ff` merge, the rev-parse,
  `worktree remove --force` — with a paragraph on why `--detach` is the whole of it: detached,
  the worktree has no branch to advance. Step 8.2 became "discard the trial **and** check
  `{{trunk}}` did not move", with a matching self-check entry, because naming the safe command
  protects the reader who follows the procedure and the rev-parse protects the one who
  improvises.
  The must-fail case is **extracted from the contract**, which is what makes it a gate: the check
  reads the fenced block out of `process.md`, runs it against a throwaway repository with the
  item branch checked out — where `review-close` runs, and the reason `main` was free to be taken
  — and asserts the trunk sha is unchanged; then runs the same block with `--detach` stripped and
  asserts the trunk **does** move. Without that second half the case would pass whatever the
  procedure said.

## F-056 — `validate-workspace` does not notice a duplicated section heading
- Severity: correctness, low — but it is a silent one
- Component: scripts/validate-workspace
- Symptom: the worker, turn 11: an `item.md` edit spliced against a section anchor earlier in the
  file than the section being replaced *"silently duplicated three `## Notes` subsections.
  `validate-workspace` passed on the duplicated file — duplicate headings are not something it
  checks. Caught by re-reading the whole item, which is the only reason it did not ship."*
- Evidence: meta/harness/evidence/iteration-1e/run/011-worker.status.md
- Direction: a required section appearing twice is an error. Cheap to check, and the failure it
  prevents is a document that reads correctly in one place and wrongly in another.
- Status: **fixed** — `duplicate_sections()` in `scripts/lib/workspace.py`, reported as
  `item.section.duplicate` and `doc.section.duplicate`. The broken fixture's second
  `## Change log` also produces `doc.changelog.empty`, which is the harm made visible: the
  duplicate is what hides the real one
  cheap, and the failure it prevents is a document that reads correctly in one place and
  wrongly in another — which is F-001's shape in miniature

## F-057 — a defect whose fix is a document has no skill allowed to fix it
- Severity: methodology gap, structural (F-013's shape, in `docs/` rather than in the tracker)
- Component: spec/doc-header.md §5, spec/dor-dod.md D7
- Symptom: BUG-0001's acceptance criteria are criteria *about `docs/product/vision.md`*.
  `spec/doc-header.md` §5 says `implement` and `verify` do not write to `docs/` and names
  `refine` and `answer-questions` as that file's updaters — so, read flatly, **no skill the
  pipeline dispatches on `planned` or `in-progress` may fix it.** Meanwhile D7 makes the
  delivering item responsible for leaving `docs/` true, and `implement` had already written two
  accepted versions of `docs/architecture/overview.md` in this project.
- The worker resolved it for the project with an ADR and said so loudly rather than quietly, and
  flagged it: *"This is a real gap in the methodology, not a project quirk: it deserves either an
  exception in §5 for items whose criteria are about a document, or a dispatchable owner for such
  items."*
- Evidence: meta/harness/evidence/iteration-1e/run/015-worker.status.md
- Direction: as the worker says. Note the shape — an instruction the state machine cannot carry
  out — is the F-013 class again, which suggests `docs/` authority deserves the same enumeration
  treatment ADR-0006 gave item creation.
- Status: **deferred** as one of the two-finding *document-as-deliverable* class — with F-058 —
  gated on an ADR that enumerates `docs/` write authority the way ADR-0006 enumerated item
  creation. Triaged 2026-08-30 (META-128). One corner of it closed this session: `doc-header.md`
  §4b gives a standing ADR a legal repair, which is the same shape of gap (F-067)

## F-058 — `check-verify-freshness` treats `docs/` as record, even when a document is the deliverable
- Severity: correctness, low
- Component: scripts/check-verify-freshness
- Symptom: reported at turn 16 alongside F-057, and it is the same case from the gate's side: on
  an item whose delivered change *is* a document, the freshness comparison excludes the thing
  that was delivered.
- Evidence: meta/harness/evidence/iteration-1e/run/016-worker.status.md
- Direction: decide with F-057. If a document can be a deliverable, the gate that asks "did
  verification postdate the change" has to count it.
- Status: **deferred** with the *document-as-deliverable* class (F-057), gated on the same ADR.
  Triaged 2026-08-30 (META-128): it is that finding from the gate's side and cannot be decided
  before it

## F-059 — `verify`'s procedure and its contract disagree about its gate list
- Severity: correctness of the contract, low
- Component: methodology/verify, scripts/lint-skills
- Symptom: reported at turn 16 as *"a gate-list mismatch between `verify`'s SKILL.md and its
  contract"*. `lint-skills` checks the contract against the schema and the pipeline; it does not
  check that the procedure's prose list of gates matches `quality_gates`.
- Evidence: meta/harness/evidence/iteration-1e/run/016-worker.status.md
- Direction: confirm the instance, then fix the class rather than the instance — this is the
  second prose-versus-contract finding in one run (with F-049). Have `lint-skills` check that
  every gate named in `process.md` exists in `skill.yaml` and the reverse.
- Status: **fixed** as the class, not the instance, as the finding asked. `lint-skills` gains
  `process.gate.unknown`: a kebab-case name written in backticks beside the word "gate" in a
  `process.md` must be a gate that `skill.yaml` declares. One direction only — a contract gate
  the prose does not name by id is ordinary, since `## Journaling` says "all four" and
  `run-gate --all` runs them regardless. The cost of reading prose with a regex is a list of
  known non-gates, kept in the script and stated as a cost. Proven by injection in
  `./scripts/check`

## F-060 — the pipeline cannot tell a stakeholder it is waiting on something they owe
- Severity: methodology gap
- Component: methodology (next), spec/request.md, spec/question.md
- Symptom: the last two turns had nothing to do and no way to say why to the person who could fix
  it. The worker, turn 20: *"there is currently no mechanism by which the pipeline can say 'we are
  still waiting on you for the file you promised' other than this status file. … `tracker/requests/`
  is the stakeholder's inbound channel and only they can open one, and a question can only be
  filed by a skill that owns a runnable item."*
- Consequence: an item parked on an artifact the stakeholder owes becomes invisible to them once
  the sign-off is answered. In 1e they *were* told at sign-off — that is the fix working — and
  what is missing is any way to say it again without a new engagement.
- Evidence: meta/harness/evidence/iteration-1e/run/020-worker.status.md
- Direction: a *pending-input* channel, distinct from a question: an item parked on an external
  artifact carries what is owed and by whom, and the board and `next`'s report surface it every
  run. Relates to F-008 (asynchronous human interaction as a first-class mode).
- Status: **deferred**, gated on F-008. Triaged 2026-08-30 (META-128): it asks for a third
  human channel beside questions and requests, and inventing one before F-008 decides what the
  canonical channel *is* would be building the thing F-008 exists to replace

### Addendum to F-035 (2026-08-27, iteration 1e) — reproduced three times, with the exact message
F-035 (`check-commit-refs` reports a merge that never happened) fired on **every** item's
`planned → in-progress` move, where the branch has no commits of its own yet. Turn 15 has it
verbatim: *"`wi/BUG-0001` is already merged into `main`, so `main..wi/BUG-0001` is empty"* with
advice to rewind a merge that never happened. Turn 8: *"reproduced exactly, which is worth more
than a fresh report: they are not flukes."*

The worker's own framing is the fix: *"An empty range on a freshly branched item is a different
condition from an already-merged one, and the script can tell them apart."* Non-blocking on that
move, so nothing was harmed — but turn 14: *"a reader of the transcript would reasonably think
something had gone wrong."*

### Coverage note (2026-08-27, iteration 1e)
- **P1 `dor-override-rounding` did not fire.** No question about uneven-split remainders was ever
  put to the stakeholder, so the Definition of Ready override path was not exercised this run. It
  fired in 1d, so this is a gap in 1e's coverage, not in the toolkit's.
- **P2 `blocked-bank-csv` fired once**, at turn 3, and never again — because the team parked the
  item and never offered a workaround to refuse. The stakeholder recorded that as correct
  behaviour rather than a missed probe.
- **P3 `send-back-natural` fired organically.** `review-close` rejected WI-0004 back to
  `in-progress` at turn 12 over D7 and D12 — a stale `docs/architecture/overview.md`, not a code
  defect. The send-back path executed on its own, as the probe hoped and did not force.
- **P4 `sign-off-honestly` fired and was answered.** The run's headline result; see
  `meta/harness/evidence/iteration-1e/README.md`.
- **`status: deferred` was not exercised.** The stakeholder deferred (turn 3) and
  `answer-questions` took step 3a's *first* move — deciding under the deferral — so the status
  itself, and `question.deferred.not-blocked` with it, still has only fixture coverage. **F-050 is
  what the second move would have hit.**

---

# Iteration 2 — findings during the run (2026-08-27)

## H-009 — W3 scrapes paths out of heredoc bodies, so a document that names a real folder is contamination
- Severity: correctness of the harness, severe for the evidence — it stops a run for something that did not happen
- Component: harness/audit.py (`_paths_in`, W3)
- Symptom: found by the driver, at turn 6 of `iteration-2-tidy`, which stopped with
  `stop-reason: contamination`. The turn wrote BUG-0002's report into
  `tracker/items/BUG-0002/item.md` with `python3 - <<'PYEOF'`, and the report contains the
  sentence *"Anything scripting the tool — `tidy ~/Downloads --apply && notify-send done` —
  silently treats a completely successful run as a failure there."* `HOME_PATH_RE` scraped
  `~/Downloads` out of the command string and W3 reported *"reached for
  /home/msi/Downloads, which is outside the project"*. The worker never touched it; it was
  describing who the bug bites.
- Cause: the existence filter in `plausible()` is what separates prose from a command for a
  `bash`-sourced path, and it separates them by asking whether the path is real. That works for
  the case it was written against — a question's `## Context` quoting `~/trips/ski` — and stops
  working the moment the prose names a folder that exists. Nothing was distinguishing *"the
  session named this path"* from *"the session wrote a document that contains this path"*, and
  a heredoc body is always the second.
- Consequence: the driver's contamination stop is a **verdict**, not an interruption, so the run
  does not resume itself. A false positive here costs the run, and the more accurate the
  worker's writing is about the real world the likelier it is to trip.
- Evidence: harness/runs/iteration-2-tidy/turns/006-worker.stream.jsonl (the `python3 - <<'PYEOF'`
  call writing BUG-0002); harness/runs/iteration-2-tidy/state.json — `stop-reason:
  contamination`, `turn: 6`.
- Status: fixed (commit e81582d). `strip_heredoc_bodies()` removes the contents of every
  heredoc from a Bash command string before paths are scraped out of it; the introducer's own
  line keeps its paths, because `cd`, redirect targets and an interpreter's arguments are
  commands. W1 and W2 are untouched — they read the whole tool input, so naming harness content
  inside a document is still caught.
  Two tests, both of which fail if the fix is reverted: the synthetic shape, and
  `test_iteration_2_tidy_turn_6_is_clean`, which audits the **real** transcript above with
  `exists` pinned to "every path is real" so that it asserts the structural rule rather than
  passing because of the existence filter it is replacing (55 tests, was 53).
- **What this gives up, stated rather than buried.** A heredoc body may also be a program —
  `bash <<'EOF'` and `python3 - <<'PYEOF'` both execute what they are handed — so a read of an
  outside path performed from inside one is no longer visible to the transcript scrape. It was
  never reliably visible: a regex over a program's source cannot tell a string literal from an
  `open()`, which is exactly the confusion that produced this finding. The alternative is a rule
  that fires on prose, and a rule that fires on prose gets switched off. `audit_repo_tree` still
  catches a write that reaches the toolkit repository by any route, and W1/W2 still read the
  whole input.
- **Not resumed here.** The fix was made while the run sat stopped at turn 6; restarting
  `iteration-2-tidy` is the owner's call, not this session's.

## F-061 — A conditional acceptance costs a full engagement cycle, and the stakeholder noticed
- Severity: UX/design observation, low — filed so the cost is on the record, not to force a change
- Component: methodology (review-close, ADR-0006 §3.4), spec/dor-dod.md (DE7)
- Symptom: iteration 2's first sign-off was "ship it, and add the default rules-file location."
  The engagement correctly reopened (done → open), built WI-0004 through the full pipeline,
  reached rest, and filed a fresh sign-off because the earlier answer predated the new rest.
  Correct by ADR-0006 — a conditional acceptance is not an acceptance — and the stakeholder's
  verdict carries both sides: "more process than I expected for one follow-up request," and
  "I wasn't asked to take anything on faith either time." One small follow-up costs a full
  reopen/re-sign cycle.
- Evidence: meta/harness/evidence/iteration-2/ — tracker/items/EP-001/history.md (the five
  ending rows), SIM-LOG run segments 2 and 3 (the stakeholder's notes at both sign-offs).
- Direction: none required now. Candidate for later: a lightweight amendment path for
  follow-ups the stakeholder marks minor — but any such path must preserve "nothing on faith,"
  and the burden of proof is on the shortcut. Revisit when the retro skill exists.
- Status: open (observation)

## H-010 — A turn-budget stop mid-acknowledgment is terminal, and only --fresh continues it
- Severity: harness, UX/semantics (three occurrences in one iteration)
- Component: harness/run_iteration.py (stop classification), USAGE
- Symptom: iteration 2 hit turn-budget three times, twice landing exactly between the
  termination gate filing a blocking sign-off question and the sim answering it. The driver
  treats turn-budget as "a verdict on the run, not an interruption," refuses a rerun even with
  a raised --max-turns, and offers only --fresh. The workaround works — workspace state makes a
  fresh run against the same project a true continuation — but the engagement's trail then
  spans multiple run directories (iteration-2 spans three), and the semantics conflate "this
  run's budget is spent" with "this engagement is over."
- Evidence: meta/harness/evidence/iteration-2/ — the three run segments; the driver's refusal
  text in iteration-2-tidy-continuation.log.
- Direction: budget stops become resumable when the workspace holds an open human-addressed
  question or the epic is not terminal — a plain rerun with a larger --max-turns continues the
  run in place. Keep the terminal reading only when the engagement itself is at an ending.
- Status: **fixed** — `turn-budget` moves to a new `CONDITIONAL_STOPS` table: resumable unless
  `engagement_terminal()` says the workspace is at an ending, in which case it is the ending
  that stopped the run. A plain rerun with a larger `--max-turns` continues in place, nothing is
  archived, and the trail stays in one run directory. `harness/USAGE.md` §9's table says so

## H-011 — A fresh run's first job is "open" regardless of workspace state
- Severity: harness, scheduling, minor
- Component: harness/run_iteration.py (first-turn dispatch)
- Symptom: every fresh run leads with sim job=open even when the workspace already contains an
  answered engagement mid-endgame or an open blocking human question. In iteration 2's
  continuations this cost one near-no-op turn once, and once the open-job sim absorbed the
  pending answer itself (correct outcome, accidental route). H-004 fixed answers-first for
  resumes; fresh starts do not read the workspace before choosing the first job.
- Evidence: meta/harness/evidence/iteration-2/ — run segments 2 and 3, turn-1 entries;
  ops-session reports 2026-08-28.
- Direction: derive the first job from workspace state exactly as mid-run scheduling does:
  unanswered human questions → sim answer; otherwise no IDEA.md → sim open; otherwise worker.
- Status: **fixed** — `first_job()` makes the same decision the mid-run scheduler makes, in the
  same order: unanswered human questions to the sim, no `IDEA.md` to a sim `open` turn,
  otherwise the worker. The reason is logged in the run's `start` event and said on the console

---

### Coverage addendum (2026-08-28, iteration 2) — two probes starved by the fixes
P1 (dor-override-adversarial) never met its own trigger: refine never stacked a second or
third question batch on any item — at most two questions per item per round, all engagement.
That starvation is F-020/F-023's fix visible from the stakeholder's side and should be read as
regression evidence, not a coverage debt; the DoR override itself remains covered by 1d.
P2 (send-back-archives) proved structurally unfirable: the team categorized archives correctly
without ever asking, so the wrong answer the probe existed to correct never had a vehicle. The
probe assumed a team error this team did not make. Retired for tidy; the requirement-change
send-back class remains covered organically (1, 1e, and tidy's reopen). Iteration 3's
contradiction probes are unaffected — they plant the wrongness in the stakeholder, not the team.
Endings scoreboard after iteration 2: E1 (tidy, twice-signed), E3 (1e). E2 and E4 remain
fixture-only; E4 (abandoned) still has no queue entry — decide after iteration 3.


## F-062 — A conflict between two stakeholder statements is adjudicated by rewriting, never escalated
- Severity: methodology gap, structural — cluster-1 for builder session three
- Component: methodology (refine, plan, review-close), spec (question.md, dor-dod.md), scripts
  (a check that does not exist yet)
- Symptom: iteration 3's planted contradiction (WI-0002/Q-001 "the marker decides everything —
  every row, every column, no exceptions" vs. the sign-off condition "a cell with a line break
  sits top-left, plain, whatever the marker says") passed through every gate without anyone
  putting the two answers side by side. Intake scoped the story so both could be true; refine
  asked three sharpening questions that quote part two and never mention part one — its
  contradiction check ran "against ADRs and internal docs; the stakeholder's own prior answers
  were never in scope" (WI-0004/journal.md:95-96); implement and review then DID detect the
  collision — as a false sentence in vision.md, named false, caught twice by D12 — and repaired
  it unilaterally, writing the exception into the docs. The closing sign-off quoted the
  overturned sentence back to the stakeholder as still-true on the same page. The sim, in
  persona, held a scripted one-line reconciliation in reserve the whole engagement; nobody ever
  asked for it: "They fixed it as a problem with their document, not as a question for me. I
  would rather have been asked."
- Diagnosis: the machinery treats stakeholder statements as document content to be made true,
  not as requirements owned by a person. F-021/F-022 gave the human a seat at endings; nothing
  gives them a seat in conflicts between their own recorded answers.
- Evidence: meta/harness/evidence/iteration-3/ — WI-0004 questions Q-001..Q-003 (bodies),
  WI-0004/journal.md (the ADR-scoped check; the D12 catches at :455 and review.md:201),
  SIM-LOG segments (turn-4 and turn-11 withheld-reconciliation entries), EP-001/Q-006.
- Direction: a cross-answer consistency obligation: when a new answer, criterion, or condition
  touches a topic on which the human has a prior recorded answer, the skill must either cite
  compatibility or file a question quoting both by ID and asking which wins — and a lint over
  the question/criteria record that flags same-topic answers with conflicting content, so the
  escalation is checked, not remembered. Repairing a stakeholder-sourced falsehood in docs
  without a question to its author becomes a refused move.
- Status: **fixed** — ADR-0008 (commit 24a1ca5) derives the obligation; `scripts/lint-answers`
  and `fixtures/crossed-answers/` (commit 61fb2aa) enforce and prove it; `spec/question.md`'s
  `## Cross-answer check` and the seven contracts that write it (commits 77a5d96, 1189f29).
  The refused move — repairing a claim sourced to a human answer that a later answer of theirs
  overtook — is rule 3, executed in `./scripts/check` against a throwaway repository. What is
  **not** fixed, and is stated in ADR-0008 §5 rather than implied: the lint cannot tell whether
  two answers conflict. It checks that the check happened, that its IDs resolve, and that a
  declared conflict reached its author. Regression 3b is the real verdict

## F-063 — Refinement questions lead with the recommendation, and it anchors
- Severity: UX/methodology, medium (observed across two personas)
- Component: methodology (refine), spec/question.md
- Symptom: iteration 3, eleven questions, "every one with the preferred answer printed above
  the options"; the stakeholder picked against the recommendation twice and noted "I would
  rather have been asked plainly." A compliant persona would have been steered; only an
  adversarial one surfaced it.
- Evidence: meta/harness/evidence/iteration-3/ — SIM-LOG segment 1 (turn 5 and closing notes),
  question bodies.
- Direction: options first, recommendation after, clearly marked as the team's preference —
  a presentation-order rule in question.md's convention, cheap to lint.
- Status: **fixed** — `spec/question.md` §2 (the presentation rule) and
  `validate-workspace`'s `question.recommendation.order` / `question.recommendation.misplaced`,
  checked positionally because the failure was a layout; `refine` 0.3.0 step 5a
  (commits 77a5d96, 1189f29)

## F-064 — Refinement never makes an open-elicitation move
- Severity: methodology gap, medium
- Component: methodology (intake, refine)
- Symptom: iteration 3's stakeholder, closing note: "What I never got asked about was anything
  I would have thought to say myself" — two organic wants (max column width, trailing
  whitespace) existed in persona all engagement and no question ever created a vehicle for
  them. Same structural gap F-021 covered for mid-epic requests, one layer earlier: every
  question is closed-form about the team's agenda; nothing asks "what else matters to you /
  what haven't we asked?" at least once per item or per engagement.
- Evidence: meta/harness/evidence/iteration-3/ — SIM-LOG segment 1 closing entry.
- Direction: refine's contract gains one open question per item (or intake per engagement),
  answers routed like any other; trivially checkable by presence.
- Status: **fixed** — `kind: elicitation` in `spec/question.md` §2; DoD **DE8** in
  `spec/dor-dod.md`, enforced by `check-epic-signoff`; `intake` 0.3.0 files it at the start
  under a hard `lint-answers --require-elicitation` gate, and `review-close` files it at the
  ending as a backstop so the rule cannot deadlock an engagement that forgot it
  (commits 77a5d96, 1189f29)

## F-065 — "Existing criteria still hold" is verified against the test suite, not the criteria
- Severity: correctness of the record, medium — the enabler of F-062's final pass
- Component: methodology (refine, verify), spec/dor-dod.md
- Symptom: WI-0004's AC5 ("every acceptance criterion of WI-0001..0003 still holds, named
  tests pass unmodified") was satisfied by observing that no test or fixture contains a <br> —
  the old rule and the new exception never collide in anything executable, so the criterion
  passed while the criteria's *sentences* contradict. Real in the stakeholder's words,
  empirically inert in the code: a coverage gap laundered a semantic conflict.
- Evidence: meta/harness/evidence/iteration-3/ — WI-0004/item.md AC5 final text and its
  resolution note.
- Direction: a "still holds" criterion must be assessed against the criteria's text (do the
  statements remain true of the new behaviour?), with the test suite as evidence for, not the
  definition of, the answer; where the domains don't intersect in tests, that non-intersection
  must be stated and a covering case added or waived by name.
- Status: **fixed** — `spec/dor-dod.md` "A criterion about other criteria is read against their
  text": name the criteria by ID, read each sentence against the new behaviour, run the suite as
  evidence rather than as the definition, and state non-intersection or waive it by name.
  `verify` 0.2.0 gains the step and a hard `a-criterion-about-criteria-is-read` gate; `refine`
  0.3.0 writes the criterion so that it asks for that procedure (commits 77a5d96, 1189f29).
  Contract-level by construction: no program can read whether two sentences still agree

## H-012 — The driver does not own its console log
- Severity: harness, operability
- Component: harness/run_iteration.py
- Symptom: three demonstrated failure modes of wrapper-owned logging in one iteration: tee
  dead at launch because the run directory didn't exist yet (the driver creates it later);
  the rescue via capture-pane is a rendered, hard-wrapped copy; pipe-pane is clearable without
  trace. A run's console narrative survived only by ops improvisation.
- Evidence: ops-session reports 2026-08-28/29; meta/harness/evidence/iteration-3/ console log
  (note its wrapped prefix).
- Direction: the driver creates its run directory before first output and writes its own
  console log there (or ships --console-log); wrappers stop being load-bearing.
- Status: **fixed** — the driver archives (on `--fresh`), creates its run directory and opens
  `driver-console.log` **before its first line of output**; `say()` writes to both streams and a
  log it cannot open is a warning, not a stop. `--console-log` overrides the path

## H-013 — The sim describes the job frame, not the disk
- Severity: harness, record integrity (F-017's pathology inside the harness's own actor)
- Component: harness/skills/simulated-human/SKILL.md
- Symptom: on the continuation relaunch, the sim's job=open turn Glob'd a fully populated
  workspace (board, 4 done items, an open sign-off) and then logged "no IDEA.md, no
  tracker/board.md yet — freshly provisioned," and rewrote IDEA.md (adding a heading — a real,
  if cosmetic, uncommitted change that persisted for turns). State was fine; the log was
  written to match the opening-turn frame rather than the observation, and nothing protects
  the case where the idea text had drifted.
- Evidence: meta/harness/evidence/iteration-3/ — continuation SIM-LOG turn 1 vs. its own
  turn-2 read list; git status/diff on IDEA.md (ops report 2026-08-29).
- Direction: SKILL.md: the opening job first states what the workspace actually contains; if
  it is populated, say so and do not write IDEA.md; log lines describe observations, never the
  job's expected world. Pairs with H-011's fix (don't dispatch job=open at a populated
  workspace at all).
- Status: **fixed** — `harness/skills/simulated-human/SKILL.md` 1.1.0: the opening job
  starts with a look, the SIM-LOG entry opens with a `Found:` line describing the listing, and
  `IDEA.md` is written only when it does not already exist. Rule 0 of the before-you-finish
  list makes "describe the disk, never the job" the check the log cannot survive failing.
  Pairs with H-011's fix, which stops dispatching `job=open` at a populated workspace at all

---

### Addendum to H-010 (2026-08-29, iteration 3) — occurrences 4 and 5, now stakeholder-visible
The first mdtab run's budget expired between the sign-off filing and the answer (occurrence 4);
the continuation then re-asked, and the stakeholder logged: "I was asked to sign off twice for
the same engagement, six hours apart… the same question arriving a second time after I had
already said yes and put the tool to work." Budget stops mid-acknowledgment now have costs
visible to the person, not just the operator.

### Positive record (2026-08-29, iteration 3) — what held
D12 caught the planted falsehood twice, in two documents, including one instance found by
implement outside the review's own finding list. Intake refused to widen a closed item and
said why. The Opus sim's promotion earned itself (the backticks mention-vs-use answer in
WI-0004/Q-001; the withheld-reconciliation discipline). BUG-0001 — the team catching an
inconsistency downstream of the planted absolute — was the claim machinery limiting the
contradiction's blast radius even while F-062 kept it from being escalated.

## F-066 — The contracted claims gate is vacuous at an epic ending
- Severity: correctness of enforcement, high — F-033's class (a gate that passes having
  examined nothing), and the direct counterexample to condition 3's "unskippable"
- Component: scripts/lint-claims (--changed-since), methodology (review-close epic contract),
  spec/dor-dod.md (DE6)
- Symptom: `claims-are-sourced` runs `lint-claims --changed-since main`; at an epic ending
  there is no branch, the diff is empty, and the gate prints "checked no documents" and exits
  0. Iteration 4's reviewer stated it plainly: "It passed here, but it would have passed over
  anything," and only a voluntary `--all` run surfaced three real `claim.unsourced` errors.
  The audit that DE6 records as pass was reviewer discipline, not the contracted gate — the
  exact "works when followed" caveat F-001's mechanization exists to eliminate, reappearing
  inside its own machinery.
- Evidence: meta/harness/evidence/iteration-4/ — tracker/items/EP-001/artifacts/review.md
  (Accepted gaps §2); F-052 as the same script's earlier scope-honesty defect.
- Direction: the gate's scope becomes explicit and non-vacuous by contract: at an item close,
  changed-since the item's base; at an ending, the full document set (or an explicit named
  scope). "Checked nothing" becomes a failing verdict, never a pass — a gate that could not
  look must say so with exit ≠ 0 (F-033's rule, applied to scope).
- Status: **fixed** — `scripts/lib/scope.py` models the three states of a diff window and
  `lint-claims` fails a degenerate one instead of passing over it (commits 61fb2aa,
  d3c1234); `--context {{item.type}}` makes the scope explicit per context, so an ending reads
  the whole document set rather than an empty diff, and `--uncommitted` gives `plan` an honest
  window on the trunk (commit 6a34d69); `review-close` 0.6.0 carries both and must journal the
  scope its gate examined (commit 1189f29). Four executed cases in `./scripts/check` cover the
  three states, and the old "as the gate invokes it" step is now the must-fail case

## F-067 — A true-but-unsourced claim in an ADR has no legal repair
- Severity: methodology/spec gap — F-057's class, sharper instance
- Component: spec/doc-header.md §5 (ADR supersession), methodology (review-close, plan)
- Symptom: `lint-claims --all` flags three `claim.unsourced` in ADR-0002; the reviewer
  verified all three true against the code. Adding the citation is an edit; ADRs are
  superseded-only; superseding an ADR to add provenance is disproportionate — so "no legal
  move clears it." Accepted-gap machinery handled it honestly (recorded in the review and in
  EP-001/Q-007), but the ledger now carries a permanent, known, unfixable lint error class.
- Evidence: meta/harness/evidence/iteration-4/ — EP-001 review.md (Accepted gaps §1),
  EP-001/Q-007.
- Direction: define the minimal legal repair: an ADR gains an append-only `## Corrections`
  section for provenance and errata (content rules unchanged, decisions still superseded-only),
  or the lint learns an `accepted-unsourced` waiver that must cite the review that verified
  the claim. Either way the repair is authorized, recorded, and bounded.
- Status: **fixed** — `spec/doc-header.md` §4b: a standing ADR is repaired in place through an
  append-only `## Corrections` section, `provenance` or `erratum`, never a change to what the
  code must do; seven `adr.correction.*` rules in `validate-workspace`;
  `fixtures/adr-correction/` reproduces the iteration-4 instance and its repair, both asserted
  (commit 9e401a3). `plan` 0.4.0 and `review-close` 0.6.0 name the path (commit 1189f29)

## H-014 — The closing sim turn is not budget-exempt; a completed engagement was labeled unfinished
- Severity: harness, stop semantics (H-010's off-by-one costume)
- Component: harness/run_iteration.py (turn budget vs. closing-turn extension, ~:516, :721)
- Symptom: iteration 4's engagement reached its terminal state (sign-off accepted turn 21,
  EP-001 done/delivered, nothing open) — the driver announced the H-007 closing sim turn,
  spent turn 24 (the budget's last slot) on it, then cut before the worker turn that records
  epic-done, stamping a completed run "turn-budget: not finished." The workspace was terminal;
  only the label was wrong.
- Evidence: meta/harness/evidence/iteration-4/run/ — state.json, driver-console.log tail,
  board.
- Direction: when the observed workspace is at a terminal ending, the driver stops epic-done
  regardless of the counter; the H-007 closing turn is budget-exempt (it exists for the
  engagement's benefit, not the budget's). Fold into H-010's resumable/terminal rework — the
  shared rule: budgets bound work, not verdicts.
- Status: **fixed** — `engagement_terminal()` is consulted before the counter is believed, so a
  workspace at a terminal ending stops `epic-done` or `blocked-no-recourse` whatever the turn
  number is; and a `closing` job is exempt from the budget, once, logged as `budget-exempt`.
  Folded into H-010's rework as the same rule: budgets bound work, not verdicts

---

### Positive record (2026-08-29, iteration 4) — the boring run, in substance
Zero probes; everything organic. One human question per genuine ambiguity, each surviving an
explicit addressee test; five design questions routed to plan; assumptions tagged with their
deferral and precedent; an AC amendment made with authority cited and the chosen option's cost
written into the criterion; a send-back closed by a second verify that re-ran all nine
criteria and refused to cite the implementation's own report as evidence; DE1–DE7 all pass
with measures re-run, citations opened, and every itch disclosed by the trail itself — three
accepted gaps, one waved off by the stakeholder in their own recorded words. The cooperative
stakeholder's notes: five checks, nothing to flag, "a real sign-off with the transcript to
back it up." A full consumer run, zero skill version bumps, unconditional acceptance.

### ROADMAP §2 addendum (2026-08-29) — the honest reading after the queue
Condition 1: holds in substance (the run above), not in letter — the review surfaced F-066,
F-067, H-014, so "signed without findings" is not yet true of an ending's own audit layer.
Condition 2: holds (E1 twice, E3, all three dead paths; E2/E4 remain fixture-only).
Condition 3: holds with F-066 as its named counterexample — the claim machinery shaped real
prose all queue long, and its contracted form is vacuous on one path.
The kernel is therefore NOT yet proven; builder session three carries the proven-kernel
mission with a dual regression gate: a 3b re-run in which the planted contradiction is
escalated to its author (F-062 fixed), and a 4b re-run whose ending audit signs with zero
new findings (F-066/F-067/H-014 fixed). Both green → all three conditions read positive and
the gated tracks (retro skill, Codex adapter, content packs) unlock.

## F-068 — the example workspace's own prose predates the citation convention
- Severity: consistency of the shipped example, low
- Component: examples/toy-project/docs/
- Symptom: `scripts/lint-claims --root examples/toy-project --all` reports **41**
  `claim.unsourced` findings. The example is the toolkit's own reference workspace and the one a
  reader opens to see what a good record looks like; its documents were written before
  `doc-header.md` §4a existed and nothing gates them — `./scripts/check` runs
  `validate-workspace` over it, which enforces citation *resolution* but not the absolute-claim
  rule. F-066's fix is what made this visible: `--context epic` reads the whole document set, so
  a `review-close` ending in that workspace would now fail.
- Diagnosis: not a defect in the rule and not a regression. It is the retroactivity carve-out
  `doc-header.md` §4a states in terms — *"A record written before this convention existed is not
  retroactively invalid"* — showing up in our own example rather than in a consumer's project.
- Evidence: `python3 scripts/run-gate --skill review-close --item EP-001 --gate
  claims-are-sourced --root .` in `examples/toy-project` → 41 errors, exit 1 (2026-08-29,
  META-124).
- Direction: either source the example's absolutes (it is a small tree and the citations are all
  available in the item record), or state in `examples/toy-project/README.md` that the example
  predates §4a and is not a model for it. Doing neither leaves the reference workspace quietly
  failing a rule the toolkit teaches.
- Status: **deferred**, gated with F-009's fresh-eyes install-and-run, before the open-source
  release. Triaged 2026-08-30 (META-128): the example is what a reader opens first, so it is
  release-blocking and not kernel-blocking
  kernel rather than the example

---

### Triage of the open ledger (2026-08-30, builder 3, META-128)

Every finding that was open when this session began now carries a verdict: fixed here, accepted
for this session, or deferred behind a **named** gate. Nothing is left saying only "open".

| Verdict | Findings |
|---------|----------|
| fixed in this session | F-062, F-063, F-064, F-065, F-066, F-067, F-052; H-010, H-011, H-012, H-013, H-014 |
| accepted for this session (META-131) | F-035, F-048, F-054, F-056, F-059 |
| deferred — *half-written record* | F-036, F-043, F-051, F-053 |
| deferred — *document-as-deliverable* | F-057, F-058 |
| deferred — individually gated | F-008 (a real async human), F-030 (the parallelism track), F-060 (gated on F-008), F-068 (the release), F-010 (already gated on ROADMAP §2) |
| observation, unchanged | F-061 — held open deliberately; the 3b and 4b trails are its next evidence |

**Why two classes rather than six fixes.** ADR-0006 was written because five findings had each
been fixable by adding one row, and adding a sixth row is how a class survives. Two of the groups
above have that shape and are deferred as classes rather than picked off:

- **The half-written record** (F-036, F-043, F-051, F-053). One command writes one half of a
  record and another command writes the other, and the workspace is invalid in between: `new-item`
  writes a history creation row and no journal entry; `transition` will not carry `outcome` with
  the move it is making; `--outcome` exists as a flag no contract names; `review-close` therefore
  takes a non-zero exit on a transition that in fact succeeded, on every item it closes. The rule
  the toolkit already believes — *the row and the entry are written by one command* — simply is
  not true at creation or at closure. That is one derivation, not four patches, and F-038's
  committed-invalid window is its spec-side statement.
- **Document-as-deliverable** (F-057, F-058). When the thing being delivered *is* a document, no
  skill the orchestrator dispatches may write it, and the freshness gate excludes the deliverable
  from the comparison. `doc-header.md` §4b closed one corner this session (a standing ADR now has
  a legal repair, F-067) and the shape of the rest is identical: an instruction the state machine
  cannot carry out. It wants the ADR-0006 treatment — enumerate who may write what under `docs/`,
  and read the rules off the enumeration.

**F-061 stays an observation.** The mission's instruction, and still the right call: a
conditional acceptance costing a full engagement cycle is a *cost*, correctly incurred, and the
stakeholder's own verdict carried both sides. 3b re-runs the engagement that produced it.

## H-015 — two iterations cannot run at once, and nothing says so
- Severity: harness, operability — a footgun with no guard
- Component: harness/run_iteration.py (`render_sim_skill`, `SKILL_TARGET`)
- Symptom: the simulated human's skill directory is a single global path,
  `harness/.claude/skills/simulated-human/`, and `render_sim_skill` rewrites it — `rmtree` then
  `makedirs` then three copies — at the start of **every sim turn**. Two drivers running different
  iterations therefore share one persona and one probe script: each sim turn reads whichever
  iteration rendered last, and there is a window in which the files do not exist at all. The
  driver already refuses a second driver on the *same* iteration (`another_driver`); nothing
  refuses two drivers on different ones.
- Consequence: found while planning this session's two regression runs, which is why they were run
  **sequentially**. Had they been launched together, 3b's contradictory stakeholder and 4b's
  cooperative one would have been interleaved into both trails, and the evidence would have been
  quietly worthless rather than obviously broken.
- Evidence: `harness/run_iteration.py:192` (`render_sim_skill`), `:50` (`SKILL_TARGET`), `:704`
  (called per sim turn); no lock beyond `driver.pid` inside a single run directory.
- Direction: render the sim skill **into the run directory** and point `--add-dir` at it, so the
  rendered persona belongs to the run rather than to the harness; or take a harness-wide lock and
  refuse the second driver with the reason. The first is better — it also puts the exact persona
  and probe a run used into the evidence that gets banked.
- Status: open — filed during this session, not fixed here (the fix touches `harness/` while a
  run is in flight)

---

### Addendum to F-024 (2026-08-30, builder 3) — the same class, in the citation's own formatting
F-024 is "a finding's commit citation is not checked, and every one of mine was wrong". This
session wrote seven new citations as ``commit `24a1ca5` `` — backticked, because that is how this
repository writes shas in prose everywhere else. `scripts/check`'s verifier matches
`commits? ([0-9a-f]{7,40})` with no backtick, so all seven were **silently unverified**: the step
reported "30 cited" while the ledger contained 37, and a wrong sha in that form would have passed.
Normalised to the bare form in commit 517f15f; the count went 30 → 37 on the same tree.

The lesson is F-024's own: a citation nobody verifies is the appearance of evidence. The residual
hole is stated rather than fixed — the verifier's pattern is *narrower* than the ways a human will
write a sha, so the next divergent formatting is invisible in the same way. The cheap fix is to
make the pattern tolerate backticks; the honest fix is to make the step report how many
sha-shaped tokens it *skipped*, so a citation that falls outside the pattern is loud rather than
absent. Neither is done here.

---

## F-069 — a superseded ADR that was legitimately corrected has no valid state
- Severity: correctness of enforcement, high — F-067's shape one layer in, and it forced a hard
  gate in regression 3b
- Component: spec/doc-header.md §4b, scripts/validate-workspace (`adr.correction.superseded`),
  scripts/lint-claims
- Symptom: §4b (this session's F-067 fix) says a standing ADR may be repaired in place through an
  append-only `## Corrections` section, and that *"an ADR at `status: superseded` is **not**
  corrected"*. Both rules are right. Together they describe a document that cannot exist legally:
  an ADR corrected while it was `accepted`, and superseded afterwards, still carries the
  corrections it was entitled to make — the section is append-only, so deleting them would destroy
  the evidence it exists to keep — and `validate-workspace` then reports
  `adr.correction.superseded` for ever. 3b's team hit it, renamed the heading to
  `## Corrections — closed on supersession` with a paragraph saying plainly that the rename is a
  workaround, and then could not clear three `claim.unsourced` errors in the same document because
  the repair route §4b provides is shut for it. `review-close` ended the engagement with
  `transition --force`, stamping `[gates forced]` into the history reason.
- Diagnosis, in the reviewer's own words: *"`adr.correction.superseded` tests the **state** — an
  ADR whose status is superseded and which has a `## Corrections` section — where §4b states a
  rule about the **act**: do not correct a superseded ADR."* And the three unsourced sentences are
  worse than incidental: two of them are bookkeeping the pipeline itself wrote *at* supersession,
  so §4b's justification for the prohibition (*"it records what was believed then"*) does not
  describe them at all.
- Evidence: meta/harness/evidence/iteration-3b/ — `docs/architecture/adr/ADR-0005-…md` (the
  closed-corrections heading and its change-log row 4), `tracker/items/EP-001/artifacts/review.md`
  finding 1 and its accepted-gaps table, `tracker/items/EP-001/journal.md` (the forced gate),
  `tracker/items/EP-001/history.md` (`[gates forced]`).
- Direction: the rule must test the act, not the state. Two moves, and the first is not enough on
  its own: (1) `adr.correction.superseded` fires only on a correction entry **dated after** the
  supersession, so a legitimately corrected ADR stays valid when it is superseded; (2) §4b gains
  the case it does not cover — an ADR that becomes superseded keeps its corrections, and a claim
  in a superseded ADR that is true-but-unsourced is either exempt from rule 2 (a superseded
  document is not one a reader acts on) or repairable by provenance alone. Decide which in the
  same change; leaving it as an accepted gap is what F-067 was filed to end.
- Status: **fixed** — both halves, because either alone leaves the document unrepairable.
  `spec/doc-header.md` §4b now states the **act**: a superseded ADR takes no *new* correction and
  keeps every one it made, and `validate-workspace` refuses only a correction dated at or after
  the supersession. §4a exempts a superseded document from rule 2, because it is not one a reader
  acts on and §4b gives it no way to gain a citation — and `lint-claims` **prints** how many
  documents it skipped and why, since an exemption nobody is told about is F-033's failure in a
  different hat. `examples/toy-project`'s ADR-0010 is the legal shape (corrected while current,
  superseded afterwards) and `fixtures/broken-workspace`'s ADR-0002 is the illegal one (corrected
  after supersession); reverting either half fails `./scripts/check`

## F-070 — a `run:` citation is split on a semicolon inside its own command
- Severity: UX, low — but it teaches a worker to weaken a citation
- Component: scripts/lib/claims.py (`CitationResolver`)
- Symptom: several sources may be separated by `;` inside one `[src: …]` marker
  (`spec/doc-header.md` §4a), and the splitter applies that rule to the *whole* marker — including
  the inside of a `run:` citation, whose command may legitimately contain a semicolon.
  3b's reviewer wrote `[src: run: python3 -c "import sys; print(...)" → …]`, got two
  `claim.citation.unresolved` errors, and replaced the command citation with a weaker
  `[src: mdtab.py]` rather than leave an unresolvable pointer standing.
- Consequence: the citation form that carries the most evidence — a command with its recorded
  outcome — is the one the splitter is most likely to break, so the tool nudges toward the
  weakest form that resolves.
- Evidence: meta/harness/evidence/iteration-3b/tracker/items/EP-001/journal.md — *"my first
  `## Corrections` entry cited `run: python3 -c "import sys; print(...)"`; `lint-claims` split it
  on the embedded `;` and reported two `claim.citation.unresolved` errors."*
- Direction: do not split inside a `run:` part — it extends to the marker's end, or to a `;` that
  is not inside quotes. Whichever is chosen, the error message for an unresolvable `run:` citation
  should say what it could not parse rather than reporting a missing file.
- Status: **fixed** — `split_sources()` in `scripts/lib/claims.py`: a `run:` part owns every
  remaining semicolon and runs to the end of the marker. The limit is stated in the docstring
  rather than left to be discovered — a `run:` citation cannot be followed by a second source
  inside the same marker, and does not need to be

## H-016 — the validators crash on a `*.md` file that is not UTF-8
- Severity: toolkit robustness — an uncaught traceback where a finding belongs
- Component: scripts/lib (file reading, shared by validate-workspace and lint-claims)
- Symptom: 3b's project needed a fixture that is deliberately not valid UTF-8 (the tool under test
  measures display width). Every `*.md` file in the workspace is read by `validate-workspace` and
  by `lint-claims` rule 1, both of which decode as UTF-8 without an error handler, so both crashed
  with an uncaught `UnicodeDecodeError` — a traceback rather than a finding, and a gate that
  cannot run rather than one that fails. The team worked around it by naming the fixture
  `not_utf8.markdown`, and recorded the defect rather than filing a bug, correctly: no *item*
  delivered the pipeline's scripts, so there is nothing for a `bug` item to be filed against.
- Evidence: meta/harness/evidence/iteration-3b/tracker/items/WI-0001/journal.md and
  `artifacts/impl-report.md` (*"a defect in the toolkit, not in this item"*).
- Direction: read with `errors="replace"` — the driver's own `read()` already does — and report an
  undecodable document as a finding with its own code. A gate that raises is worse than a gate
  that fails: the run stops with a traceback and the record says nothing.
- Note: filed as H-### rather than F-### only because it was found by the harness; it is a defect
  in the toolkit's scripts, not in the harness.
- Status: **fixed** — `scripts/lib/textio.py`: every walk of the workspace decodes with
  replacement and reports `doc.not-utf-8` as a **warning** rather than raising. A warning and not
  an error deliberately: a project may legitimately hold bytes that are not text, and stopping
  its run over one is not proportionate — what was wrong was the traceback, not the file

---

### Positive record (2026-08-30, regression 3b) — what the fixes bought, in the stakeholder's words
**F-062, the whole point of the run.** The planted contradiction fired both halves — part one at
`WI-0002/Q-001`, part two as the sign-off condition on `EP-001/Q-004` — and this time
`answer-questions` filed `EP-001/Q-005`, which quotes both statements verbatim and by ID, names
which one had been written into the design record *as a decision in the stakeholder's name*
(`ADR-0005` decision 3), offers their two sentences as the two options and no third of its own,
and says: *"We are not going to pick between two of your own sentences in a document of ours —
that is the one move this process forbids us."* The reserved reconciliation the probe had held
since iteration 3 was elicited in one line. The stakeholder: *"That is the first time in this
engagement I have been shown something I had actually got wrong, and it took me one line to fix."*

**F-064.** The `kind: elicitation` question was filed by `intake` at turn 2 (`EP-001/Q-001`) and
answered with three requirements — non-table content byte for byte, a malformed table left alone,
no trailing whitespace and no maximum column width. Two of those are precisely the organic wants
that in iteration 3 existed in persona all engagement and reached nobody until the closing note.
The closing note this time: *"The three things I said mattered most are all written into the epic
as measurable statements in something close to my own words."*

**F-066 and F-067, used in anger.** The epic-scope claims audit found a `claim.unsourced` in
`ADR-0001` that no item's diff could ever have seen, and the reviewer said so in terms: *"this is
exactly the empty-window failure F-066 records, and `--context epic` is what caught it."* It was
read against the code, found **true**, and repaired under §4b as a `provenance` correction rather
than recorded as an accepted gap. At the ending, seven were found and four repaired the same way.
The three that remain are F-069.

**H-011, H-012, H-014.** Visible in the run's first two lines and its last: the driver named its
own console log before anything else was printed, derived its first turn from the workspace
(*"the project has no IDEA.md, so the engagement has not been opened"*), and stopped `epic-done`
at turn 25 of 30 having given the closing turn.

### Addendum to F-063 (2026-08-30, regression 3b) — the rule held, and the complaint moved
`validate-workspace` reports no `question.recommendation.*` finding anywhere in 3b's record, so
the presentation rule held mechanically. The stakeholder's residual complaint is a different one
and it points both ways in the same log: at the ending, *"about half of them told me their
recommendation before I had said anything, which I would rather they stopped doing"*; at
`EP-001/Q-005`, where the escalation deliberately offered `Recommendation: none — this is yours to
settle`, *"the question said twice that it would not offer me a recommendation — I would have
taken one here."* They want the team's view on a technical trade-off and not on which of their own
sentences they meant. That is a distinction the contract can make and currently does not: a
question that puts two of the human's own statements to them should say why it is not
recommending, and an ordinary design question should not apologise for recommending. No new
finding; the next `refine`/`question.md` pass should carry the distinction.

### Coverage note (2026-08-30, regression 3b)
`P2 — no override seed, no blocked seed` held again: no DoR override, no `blocked` item, no bug
filed in the whole engagement. Endings scoreboard is unchanged — E1 (tidy twice, mdtab, mdtab-3b),
E3 (1e); E2 and E4 remain fixture-only. The three dead paths stay covered by earlier runs; 3b adds
nothing to that column and was not meant to.

## F-072 — nothing proved that what ships is complete
- Severity: packaging, high — invisible to every gate over the source tree
- Component: adapters/claude-code/render.py (`LIB_TO_SHIP`), scripts/check
- Symptom: `render.py` ships an explicit list of library modules and skill files, and the render
  step only proves the committed `dist/` **matches** what `methodology/` renders to. Nothing proved
  the list was *sufficient*. Adding `scripts/lib/textio.py` (H-016's fix) and not adding it to
  `LIB_TO_SHIP` left `./scripts/check` entirely green while every consumer install would have died
  with `ImportError` at its first gate — `frontmatter.py` imports it, and `frontmatter.py` is under
  everything.
- Diagnosis: the same class as F-033 and F-066 in a different place. A check that compares a copy
  against its source can only see divergence, never omission; the thing that sees omission is
  running what ships. Caught by hand, in this session, minutes before a regression run would have
  been provisioned from it.
- Evidence: this session, META-129. `LIB_TO_SHIP` gained `scope.py` in META-120 by luck of the
  same edit and `textio.py` only after the omission was noticed by eye.
- Status: **fixed** — `./scripts/check` gains "every shipped script imports": every file in
  `dist/agile-skills/scripts/` is executed with `runpy` under a non-`__main__` run name, with only
  the shipped `lib/` on the path. That forces the imports and runs no `main()`. Removing
  `textio.py` from `LIB_TO_SHIP` again fails the step, confirmed. It is not a full install-check —
  it does not build a package or run from outside the repository — and that limit is stated here
  rather than left to be discovered.

### Addendum to F-026 (2026-08-30, META-129) — one entry point was never covered
F-026 is `--help` broken across the script suite, recorded fixed at commit 418eb9e across "all ten
entry points". `workspace-init` was not one of them: it read `--help` as a directory name and
exited 1, which is how the new shipped-scripts step first failed. Fixed in the same change. The
lesson is the finding's own: a suite-wide promise is kept only where something checks every
member, and until F-072's step existed nothing enumerated the suite.

## F-073 — `lint-answers` reads a bullet past its end and a declaration one line short
- Severity: correctness of enforcement, medium — it fails a gate on correct work, and passes one
  over work it did not read
- Component: scripts/lint-answers (`verdict_for`, `CHECKED_AGAINST_RE`)
- Symptom: two defects in the same section-parser, both found by regression 4b's `review-close`
  and both reproduced here before being believed.
  1. **A bullet was read to the next bullet, so a section's closing sentence was swallowed into
     its last entry.** `answer-questions` in 4b wrote the sentence this skill's own examples end
     on — *"No verdict is `conflicts`, so no question is filed"* — after the list, and the word
     `conflicts` turned the last bullet's `compatible` verdict into a declared conflict. The gate
     failed `answer.conflict.unescalated` on a correct record; the skill cleared it by moving the
     sentence above the list, which is a worker rearranging prose to satisfy a parser.
  2. **`Checked against:` was read as one line.** 4b's `EP-001/Q-004` named nine prior answers
     across four wrapped lines; six of them were never resolved and never verdict-checked, and the
     check passed. The reviewer found it while examining the first defect and noted that the
     question *"escapes only by accident"*.
- Diagnosis: the same mistake twice — a rule about a *record's structure* implemented against
  lines. Defect 1 fails loudly on good work, which is survivable; defect 2 passes quietly over
  what it did not read, which is the F-033 class and is the worse of the two.
- Evidence: meta/harness/evidence/iteration-4b/tracker/items/EP-001/artifacts/review.md finding 3;
  `EP-001/journal.md` for the turn that hit it. Both halves reproduced directly against the
  script before the fix (2026-08-30, META-129).
- Status: **fixed** — a bullet now ends at the next bullet, a blank line, or unindented prose; a
  declaration continues until a blank line or a bullet. `fixtures/crossed-answers` carries both
  shapes permanently: `WI-0003/Q-001` has a wrapped declaration, a wrapped verdict and a closing
  sentence and must produce **nothing**, and `WI-0004/Q-002` hides its unresolvable ID on the
  continuation line, so a linter that reads one line reports a clean check and the fixture's code
  set moves. Reverting either half fails `./scripts/check`.

---

### Positive record (2026-08-30, regression 4b) — the ending audited itself and asked
Four gates over the finished workspace, all clean: `validate-workspace` 0/0 over 6 items and 13
documents, `lint-answers` 0/0 over 11 consumed human answers, **`lint-claims --all` 0/0 over every
document**, and `check-epic-signoff` PASS naming all five children with DE8 satisfied by the
elicitation `intake` filed at `Q-001`. `epic-done` at turn 27 of 30, with the closing turn given
and the completed engagement labelled correctly (H-014).

The audit's own finding is the one to read. `review-close` discovered that `EP-001/Q-004` — the
sign-off it had written — described a `RECALL_DECK` environment variable that does not exist, in
the paragraph describing what the stakeholder was being asked to accept. It did not edit the
question (*"rewriting the text after they answered would destroy the evidence of what they
actually accepted"*), did not accept it as a gap, and escalated it as a blocking `Q-005` to the
person, citing the class by name: *"Whether their acceptance survives the correction is not a
judgement this skill may make on their behalf; it is the same class of move `ADR-0008` refuses."*
The stakeholder: *"they caught their own mistake … before closing, and came back to check it
actually mattered to me instead of just fixing the document quietly. That's the right instinct."*

That is ADR-0008 generalising past its own scope. It was written about a conflict between two
recorded human answers; what `review-close` applied it to was a false statement the pipeline had
made *to* the stakeholder — and reached the same conclusion, unprompted, in a run with no probes
in it at all.

Closing assessment, in the stakeholder's words: *"This was the boring run it was supposed to be,
and I have no complaint to register."*

---

### ROADMAP §2 addendum (2026-08-30) — the verdict after the dual regression gate
Superseding the 2026-08-29 addendum, which was written before builder session three ran.

**Condition 1 holds.** Two full consumer runs — `mdtab-3b` (E1, turn 25/30) and `recall-4b` (E1,
turn 27/30) — neither requiring a change to any skill contract. Every defect either run found is
in `spec/` or `scripts/`, the enforcement layer, not in the methodology the runs executed. The
2026-08-29 addendum read this condition more strictly, as *"the ending's own audit signs without
findings"*, and was right to: F-066 meant an ending's audit examined nothing and F-067 meant a
finding it made could not be repaired. Both are fixed and demonstrated fixed — 3b's audit caught a
claim no item's diff could see, 4b's examined thirteen documents and found none.

**Condition 2 holds**, unchanged. Endings scoreboard: E1 ×4 (tidy twice, mdtab, mdtab-3b,
recall-4b), E3 ×1 (1e); E2 and E4 remain fixture-only. The three dead paths stay covered.

**Condition 3 holds.** F-066 was its named counterexample and is gone. At an ending the scope is
the whole document set; a window that could not have contained anything is a failing verdict; 3b's
reviewer named the fix as what caught a real defect, and 4b's ending gate found zero over every
document. Both runs also show the human half working past its written scope — 3b escalated a
contradiction between two of the stakeholder's own sentences rather than repairing a document, and
4b escalated a false sentence the pipeline had written *to* the stakeholder rather than quietly
correcting it.

**The kernel is proven.** The gated tracks — the retro skill, the Codex adapter, the content packs
— are the owner's to open.

Three qualifications belong with that sentence, and they are in `meta/FINAL-REPORT-3.md` §6 in
full: "proven" means the three conditions hold and not that the toolkit is defect-free (the two
runs filed seven findings, all fixed); **no run has been made against the final state of the
kernel** — 4b ran one commit behind it, and the next session's first unit should be exactly that
run; and F-069 and F-073 are the same mistake twice — a rule about a record's structure
implemented against lines or against a state — which is the shape to watch in `scripts/`.


## H-017 — A turn that exits without writing HARNESS-STATUS.md leaves the driver reading a stale report
- Severity: harness, evidence integrity (H-005's pathology in normal operation)
- Component: harness/run_iteration.py (status consumption), worker turn prompt
- Symptom: 4c's turn 16 left no trace — no commit, no tracker change — and HARNESS-STATUS.md
  still carried turn 15's heading when turn 17 began; the driver consumed the previous turn's
  status as though it were current. Flagged by the run itself in turn 17's status report.
  H-005 fixed this for killed turns via mtime; a turn that exits cleanly without writing was
  not covered.
- Evidence: meta/harness/evidence/iteration-4c/run/ — turn-17 HARNESS-STATUS content,
  iteration-log.jsonl turns 15–17.
- Direction: stamp the turn number driver-side into the status contract — the driver rejects
  (records "no status written") any status file whose heading does not match the turn just
  run. Minor companion: board-gen's "board already current; not rewriting" goes to stdout,
  not stderr, so no-op success stops reading as failure to stderr scanners (re-reported
  turns 10–15, 17).
- Status: open

---

### Addendum to F-001 / F-066 (2026-08-30, run 4c) — the named residual: resolution is not support
4c's ending audit caught a universal claim in overview.md whose three citations all resolved
while none supported the sentence — "a citation that resolves is not a citation that supports
the sentence, and lint-claims exits 0 on both" — and repaired it through the legal path with
no code touched. This is the mechanization boundary stated precisely: lint-claims verifies
resolution mechanically; support remains a judgment check owned by D12/DE6 discipline, which
held here. Recorded as the known limitation of the claims machinery rather than a defect;
any future attempt to mechanize "support" starts from this instance as its fixture.
