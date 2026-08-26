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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
