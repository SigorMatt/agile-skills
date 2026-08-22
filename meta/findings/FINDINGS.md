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
- Status: fixed (commit 02a417a) — the provenance half is mechanical; the judging half
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
- Status: open

## F-003 — Consumer workspace lacks .gitignore; __pycache__ committed
- Severity: correctness (every consumer hits it)
- Component: scripts/workspace-init or installer
- Symptom: running the validator generates .claude/agile-skills/**/__pycache__;
  git add -A sweeps .pyc files into the consumer's history.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.6
- Direction: ship a .gitignore entry at install or init time.
- Status: open

## F-004 — USAGE §2 verify step impossible in the installing session
- Severity: doc error
- Component: USAGE.md §2
- Symptom: "start your agent session and ask what skills are available" cannot
  work in the session that ran the installer — skills load at session startup.
- Evidence: evidence/2026-08-17-peer-setup-report.md (§ skills-load note)
- Direction: §2 must say verification of discovery requires a NEW session;
  offer the file-level check (ls .claude/skills/ + frontmatter) as the
  same-session alternative.
- Status: open

## F-005 — Pre-init validator state reads as hard failure
- Severity: UX
- Component: scripts/validate-workspace
- Symptom: the documented-correct "uninitialised" answer arrives as two hard
  ERRORs and exit 1 immediately after install reports success; only a hint line
  distinguishes it from a real fault.
- Evidence: evidence/2026-08-17-peer-setup-report.md §5.2
- Direction: distinct exit code / UNINITIALISED state with explicit next-step
  message.
- Status: open

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
- Status: open
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
- Status: open

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
- Status: fixed (commit 78fd525) — precondition 1 rewritten as filed, naming both
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
- Status: open

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
- Status: fixed (commit 33eb48c) — epics may be suspended, and the reason the rule was
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
- Status: fixed (commit 78fd525) — the second option, with the "say which" taken
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
- Status: fixed (commit 78fd525) — the first option, which META-084b had already built
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
- Status: fixed (commit 78fd525) — the first option. `spec/workspace-layout.md` §5
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
- Status: fixed (commit 8549fca for the mechanism; adoption in commit 78abb5b).
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
- Status: fixed (commit 84a11a2). The Bash branch now resolves **write targets**:
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
- Status: fixed (commit add02cb) — all three, as filed.
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
- Status: open

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
- Status: fixed (commit 4f2ebea), as filed. `RESUMABLE_STOPS` = `turn-timeout`,
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
- Status: fixed (commit 4f2ebea). `provision.py --wipe` deletes the project directory
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
- Status: fixed (commit d170ac7), as filed. At the top of each iteration of the turn
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
- Status: fixed (commit d170ac7), both halves as filed. A turn with no result event
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
- Status: fixed (commit d170ac7) — the former. Worker prompt version 4 stops after
  `{{SKILLS_PER_TURN}}` skill executions and reports `turn-budget-exhausted`, an enum value that
  already existed for exactly this shape. An execution counts when a skill *finishes* — journal
  written, transition made — and the prompt is explicit that the skill in flight is finished
  first, never left half-done. `next` does not count; it is the dispatcher. The bound is
  `--skills-per-turn`, or the iteration config's `worker-skills-per-turn`, default 3. The status
  block gains `skills_run`, so a turn that overran is visible in the log rather than inferred
  from the tool count.

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
- Status: fixed (commit 76dcaf1). New artifact and new spec file: `spec/request.md` —
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
- Status: fixed (commit ae25f6c). `spec/question.md` §2 (revision 2) adds the optional
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
- Status: open

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
- Status: fixed (commit d170ac7), both halves. F-022 lands the sign-off, and the driver
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
