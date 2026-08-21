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
- Status: open

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
- Status: open

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
