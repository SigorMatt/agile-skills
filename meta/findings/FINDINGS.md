# Findings — input backlog for builder session 2

Convention: F-### sequential, never reused. Every finding cites evidence in
`evidence/` or in this repo. Status: open | fixing | fixed (with commit) | rejected (with reason).

**How to read a status (2026-09-10, F-112).** This file is **append-only**: when a finding is
resolved or re-triaged, its original `Status:` line stays where it is and the new one is appended
**below** it. **The last status line in an entry is the current one.** A status may be written as
a bullet (`- Status: ...`, `- **Status update ...**`) or as a `###` heading, so a search for the
bullet form alone misses entries too; and three entries are tombstones or pointers rather than
findings, and say so in their status. `grep 'Status: open'` is the wrong tool for this file — at
commit 8e61fdb it named 24 entries, 13 of which had already been resolved. `./scripts/check`'s
*every finding's status is readable* step requires each `## F-###` / `## H-###` entry to carry at
least one status line and reports the tally of last statuses.

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
- Status update 2026-09-10 (META-163): **still deferred, gate unchanged, re-confirmed.** The
  gate is evidence from a **real asynchronous human who is not us**, before the open-source
  release. Nothing produced it: no live run was made this session, and both staged regressions
  were provisioned, verified and torn down **without being run** (commit 8e61fdb). What moved
  next door and does **not** meet the gate: ADR-0011 gives silence an ending and ADR-0012
  (commit b4f1909) decides which questions stop the loop. Both make the question-file protocol
  carry more weight, and neither makes it *the canonical channel with the interactive tool as one
  transport over it*, which is the design change this finding is. F-060 stays gated on this one.

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
- Status update 2026-09-10 (META-163): **the gate is MET, and has been since 2026-08-30 —
  nothing recorded it here.** This finding's gate is `meta/ROADMAP.md` §2 by its own text, and §2
  carries a stamp dated 2026-08-30: all three conditions found positive against the final kernel
  by confirmation run 4c, ending *"The kernel is proven. The gated tracks are open"*, with F-010
  named in the sentence that follows. The status line above has read only *deferred (gated)* for
  the eleven days since, and META-128's triage table that same day recorded it as *already gated
  on ROADMAP §2* without checking whether §2 had been stamped.
  **It is not reclassified as a defect, because it never was one.** F-010 is a roadmap decision —
  *quarry, don't fork* — and what changes is only that it is now **schedulable**: `ROADMAP.md` §3
  sequences it behind the retro skill (built; §3 stamp) and the Codex CLI adapter. Its own rules
  bind whoever starts it, unchanged: one workflow at a time, fully translated into contract form,
  gates authored honestly, facilitation-shaped content excluded or explicitly marked ungated,
  renamed, attributed. **Open, unstarted and sequenced — not deferred.**

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

## H-001 — number never filed (tombstone, 2026-09-10)
- This number was skipped. `meta/harness/evidence/iteration-1-mini/README.md:27` says a defect
  in the harness's own worker prompt was *"recorded as H-001 in `meta/findings/FINDINGS.md`"*,
  and `meta/journal.md:2030` (META-080) says the same — *"Both recorded as H-001; fixed in
  META-081, not mid-run."* No such entry exists and none ever did: `H-001` appears in no
  committed version of this file, and the H-numbering itself begins at H-002, filed together
  with H-003 to H-006 in the iteration-1 harvest (commit 5bc2454) — after both citations were
  already written. What happened is the mirror of F-071: there a number was named 66 seconds
  before the batch that would have filed it, here a defect was **fixed instead of filed**.
  The defect was real and the fix is in the tree: META-081 (commit e7d3c43) took
  `harness/prompts/worker-turn.md` to version 2 so that "batch every question before you stop"
  and "stop when a human question is open" no longer contradict each other, and added the
  `turn-budget-exhausted` stop reason to that prompt and to `harness/run_iteration.py`, so a
  turn ending at its spend cap stops having to report `error`. Only the finding was never
  written. The number is burned, not reused.
- Found by the first run of the F-099 sweep (META-158), which is the whole point of that
  finding: both citing files are read-only history — banked evidence and an append-only
  journal — and **neither is edited**. This entry is what makes their citations resolve, the
  same correction the F-071 tombstone makes for `iteration-3b/README.md:27`.
- **Status:** not a finding — **tombstone**, and that is its final state. The number is burned,
  never reused, and the entry exists so the two citations above resolve (F-099). Re-confirmed
  2026-09-10 (META-163) when every entry in this ledger was read for a current last status; a
  tombstone with no status bullet reads as *unexamined* to any mechanical reader, which is the
  one thing it is not.

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
- Status update 2026-09-10 (META-163): **still deferred, gate unchanged, re-confirmed.** The
  gate is the sprint-ceremonies / multi-item-parallelism track (`meta/ROADMAP.md` §3, last), and
  that track has not started. What moved and does not meet it: ADR-0012 §6 (commit b4f1909)
  records that the loop now dispatches **past** an outstanding ask, so *"an engagement with a long
  queue and an absent stakeholder"* is a state an ordinary engagement now reaches — the queue this
  finding needs is nearer than it was. It is not here yet, because the one-action rule is
  **preserved unamended**: `next` still chooses one item per pass, so the board still cannot
  mislead about what is next. Re-confirmed rather than moved: the gate is a track, not a symptom.

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
- Status update 2026-09-10 (META-163): **still deferred — and the class it was deferred with
  has broken up, so the gate is re-named rather than repeated.** The *half-written record* gate
  was *the next builder session's first unit*. This **is** the next builder session, its first
  unit was META-144, and two of the class's four members are now fixed: F-043 and F-053 were
  closed by commit 8804bd7, incidentally, while META-156 was fixing F-083's ordering. Nobody
  noticed at the time and their statuses said *deferred* for four more units.
  **This one is not fixed, checked rather than assumed.** `scripts/new-item` still writes the
  history creation row and a bare journal header, and its closing lines still say only *"fill in
  the body headings before transitioning it"* — nothing about the journal entry the workspace is
  about to demand, and no `journal-entry` command to copy.
  **Not fixed here, and the reason is F-051.** F-036's fix is one message; but a message telling
  the caller to hand-write a journal entry documents the hand-written path F-051 exists to remove,
  and would have to be unwritten when F-051 lands. **New gate:** the unit that gives `new-item`
  the write-both-or-neither shape `transition` now has — `--journal-body-file`, or the creation
  entry written by the tool — after which this message is composed from what that unit writes.
  It moves with F-051 and no longer with F-043 or F-053.

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
- **Status:** not a finding of its own — **merged into F-029** and fixed with it; see F-029's
  status. Re-confirmed 2026-09-10 (META-163), and written as a status bullet for the same reason
  the tombstones now carry one: an entry with no status line is indistinguishable from an entry
  nobody read.

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
- Status update 2026-09-10 (META-163): **fixed** (commit 8804bd7) — found by re-confirming a
  gate, not by anyone setting out to fix it. Both halves of the direction hold on the current
  tree. `--outcome` is **named in a contract**: `methodology/skills/review-close/process.md` step
  11 says the transition writes it — *"`--outcome` at step 11, never an edit of `item.md`"* — and
  `skill.yaml`'s Definition of Done says the same. And *why setting the field before the move is
  refused* is now written where the refusal happens: `scripts/transition` refuses `--outcome` on
  any move that does not end at `done`, **requires** it on one that does, and carries the reason
  beside both — `spec/work-item.md` §1 makes the outcome present if and only if the item is done,
  so status and outcome are one act. The workaround this finding was filed about — transition,
  hand-edit `item.md`, re-validate — is now refused rather than merely undocumented.

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
- Status update 2026-09-10 (META-153b): **still fixed, and the fourth of the four endings it
  named now executes.** F-045's fix enumerated four legal endings (ADR-0006) and made the
  termination gate fire at rest rather than at closure. Three of them could be reached by a run;
  **E4 could not** — `abandoned` was a row in a table with no trigger, no verdict, no gate branch
  and no fixture. Cluster 2 gives it one (commits 94606f5, 877ee85, 4d1b7ce, e9f8d79, b845342):
  see the cluster's own status entry at the end of this file. Nothing in F-045's own diagnosis
  changed, and the finding stays fixed.
  **Two things this work says about F-045 that its status did not.** Its `fixtures/ended-engagement`
  EP-003 case — *"the engagement nobody was ever asked about"*, the exact run that produced this
  finding — has always failed the gate with an empty reason, and the assertion that covers it in
  `./scripts/check` reads the exit code only. That is filed as **F-105**, with what it means for
  the assertion. And the gate that F-045 built now has a second accepting branch, which passes a
  sign-off claiming a reply it does not have: **F-106**. Both are the gate F-045 asked for, in
  places F-045 did not reach

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
- Status update 2026-09-10 (META-163): **still deferred, re-gated with F-036 alone.** The
  *half-written record* class is down to these two: F-043 and F-053 were fixed by commit 8804bd7
  and their statuses now say so. `scripts/new-item` is unchanged — it takes no
  `--journal-body-file`, writes no creation entry, and leaves `journal.execution.missing` firing
  from the moment an item exists until the caller writes the entry by hand. **New gate:** one unit
  on `new-item` giving it the write-both-or-neither shape `transition` now has; F-036's message is
  composed from whatever that unit writes, so the two move together.

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
- Status update 2026-09-10 (META-149): **still deferred, and consumed as input.**
  `meta/adr/ADR-0010-document-as-deliverable.md` §6/F-053 (commit 3701069) read this finding's
  *class* as the lifecycle constraint the document model had to satisfy, and states it in one
  sentence: **a document's state and an item's state are two different state machines, and
  neither may be derived from the other.** A document's machine advances on a content change
  (`version`, the change-log row, `status`); an item's advances on an execution (a history row
  and a journal entry); the only legitimate coupling is the audit row, which names both. Two
  things follow from it and both are now in the toolkit. First, ADR-0010 binds itself not to add
  another instance of the half-written record: the content edit, the `version` bump and the
  change-log row are **one act**, and so are the audit row and the disposition it closes — where
  a later unit adds a tool for a document write, it writes all of them or it is F-053 again in
  `docs/`. Second, F-058's diagnosis is a corollary of it — `check-verify-freshness` was deciding
  a document's kind from its directory, which is a proxy for the *item's* machine, and got it
  wrong for exactly the items where the two machines disagree.
  **What ADR-0010 did not do is fix this finding.** `transition` still has no `--outcome`, and
  `--resolving` still does not teach the validator that `item.outcome.premature` is resolved by
  the pending move to `done`, so `review-close` still takes a non-zero exit on a transition that
  actually succeeded, on every item it closes. It stays in the *half-written record* class with
  F-036, F-043 and F-051, behind the same gate, and it moves when they move. Recorded here so the
  next reader does not mistake "ADR-0010 cited it" for "ADR-0010 closed it"
- Status update 2026-09-10 (META-163): **fixed** (commit 8804bd7) — and the update immediately
  above is **false on the tree as it now stands**, which is why this bullet exists rather than an
  edit. META-149 wrote *"`transition` still has no `--outcome`"*; that was true at f474027 and
  stopped being true at 8804bd7, seven units later, when META-156 needed the legal close order for
  F-083. The direction's **first** branch was taken as filed: `transition` grows `--outcome` and
  writes it with the move, the way it already writes `--branch`. A move to `done` without it is
  refused with the reason; `--outcome` on a move that does not end at `done` is refused with the
  reason; an item leaving `done` has its outcome cleared by the same act. The cost this finding
  was filed for is gone: `review-close` no longer takes a non-zero exit on a transition that
  actually succeeded. The second branch — teaching `--resolving` that `item.outcome.premature` is
  resolved by the pending move — is **not** taken and is not needed; the finding named it as the
  alternative, and ADR-0010 §6's rule that the two state machines stay separate is the argument
  for preferring the branch that was taken.

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
- Status update 2026-09-10 (META-149): **the gate is met, and the finding is fixed**
  (commits 3701069, c1fbde8, 5e6434d, 5ae1539, a843114). Said explicitly because a deferral whose
  gate has been met and not noticed is how a backlog rots: the condition this was deferred behind
  — *"an ADR that enumerates `docs/` write authority the way ADR-0006 enumerated item creation"* —
  is `meta/adr/ADR-0010-document-as-deliverable.md` (commit 3701069), whose §3 is that
  enumeration: a lifecycle-event × actor table, with its nobody-cells named out loud in §3.3.
  The nobody-cell this finding is about is gone, and gone **by derivation rather than by
  exception**. §3.4 replaces `doc-header.md` §5's final paragraph (commit c1fbde8): the record
  half of §5's absolute survives in full and the deliverable half never had a justification, so
  an item declares the document in its plan's `## Deliverable documents` and row L4 permits
  `implement` to write it (commit 5e6434d). The worker's own two options are both in ADR-0010 §8
  as rejected alternatives, with the reason: an exception for document-shaped items is the
  sixth-exception move ADR-0006 names, and a dispatchable owner makes a document deliverable a
  different *kind of work* rather than ordinary work with a different artifact.
  The write is bounded rather than unbounded — obligation 19, `lint-documents --rule
  document-writes-are-declared` (commit a843114), checks the branch's diff under `docs/` against
  the plan's declared set — and the widened claims window means the document is actually read
  (commit 5ae1539). Checked by `./scripts/check` steps *the document window (F-076, F-058,
  8 cases)* and *the document obligations by execution (F-087, F-093, F-095, 8 cases)*.
  **The cost is written down rather than discovered later:** ADR-0010 §7's first bullet says
  plainly that a real protection was weakened, names the three shape checks and one contract rule
  that now stand where one absolute stood, and says that if a later run finds `implement`
  widening its own scope through `docs/`, that section is where it was predicted

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
- Status update 2026-09-10 (META-149): **the gate is met, and the finding is fixed**
  (commits 3701069, 5ae1539). The same gate as F-057's, met by the same ADR (commit 3701069), and
  said explicitly for the same reason. ADR-0010 §6/F-058's answer: the exemption is not "under
  `docs/`" — it is "not in this item's `deliverable-documents`". The gate's *reasoning* was always
  right (`verify` and `review-close` must commit their own records, those commits move the head,
  and a record-only change does not invalidate a verification of the code); its **predicate** was
  a proxy, and the proxy fails for precisely the items F-057 is about.
  `scripts/check-verify-freshness` now subtracts the item's deliverable documents from its `docs/`
  exemption (commit 5ae1539), so a post-verification edit to a delivered document sends the item
  back to `verifying` like any code change. Both directions are fixtures in `./scripts/check`'s
  step *the document window (F-076, F-058, 8 cases)* — cases 7 and 8: a record document edited
  after verification is still exempt, and a **deliverable** document edited after verification is
  not

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
- Status update 2026-09-10 (META-153b): **not settled, and deliberately not settled.** E4 by
  silence (commits 94606f5, 877ee85, 4d1b7ce, e9f8d79, b845342) is the adjacent mechanism and it
  is not this one. `meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md` §6 re-decided this
  finding against the derived model and put it out of scope in one rule: **abandonment is only
  ever declared against an open ask**, and F-060's case is precisely the one where nothing is
  open. The two wants are different verbs — F-060 wants a way to *speak* when there is no ask;
  E4 wants a way to *stop* when the ask goes unanswered. E4 adds no channel and needs none, so
  this finding stays **deferred behind F-008**, exactly where META-128 put it.
  **What did change, and why it is not the fix.** `next` step 3(d) now tells the person where the
  count stands — *"round 2 of 3; at 3 this engagement is declared abandoned and closed as
  dropped"* — but only while a question of ours is open, which is the case F-060 is not about.
  An item parked on an artifact the stakeholder owes is still invisible to them once the sign-off
  is answered, and there is still no way to say it again without a new engagement.
  **One gap in the record, noted rather than fixed here:** ADR-0011 §6 promised this finding a
  must-fail fixture — *an engagement at rest with an answered sign-off and an item parked on a
  promised artifact, where no waiting row is ever recorded and no abandonment is ever declared*.
  It was not built as such. Its first half is covered incidentally, because `./scripts/check`'s
  `REST_VERDICTS` requires `at-rest` (not `abandoned`) for every epic in `fixtures/ended-engagement`,
  which has no waiting log at all; the parked-artifact shape that is F-060's own is modelled
  nowhere. Recorded so that a later reader does not find the ADR's fixture line and assume it ran
- Status update 2026-09-10 (META-163): **still deferred behind F-008, gate unchanged,
  re-confirmed against ADR-0012.** ADR-0012 (commit b4f1909) re-decided this finding by name — the
  third document to do so — and stopped short of it deliberately: `next`'s report now names every
  outstanding **and standing** ask on every pass, including passes that dispatch, so what is
  pending is visible without the loop stopping to say it. The ADR states why that is not the fix,
  in its own words: *"a line in a report, not a channel"*, which says nothing to anybody who is
  not already reading the run's output. F-060's case remains the one where **no ask is open at
  all**. The new `standing ask` class (`addressed-to: human`, `blocking: false`) is the nearest
  thing the toolkit has to a pending-input channel and it is still not one: it is a question, so
  only a skill that owns a runnable item may file it — the exact constraint this finding was filed
  about. ADR-0011 §6's promised must-fail fixture is **still not built**; META-153b's note above
  stands unchanged.

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
- Status: open (observation) — **revisited 2026-08-30 by the retro skill itself**, which is what
  this entry said to wait for. See the addendum below.

### Addendum to F-061 (2026-08-30, META-140) — the mechanism this entry never had
`retro` 0.1.0, run by a context-free subagent over `iteration-2-tidy`'s record with no access to
this ledger, rediscovered F-061 and went past it. Where F-061 recorded a *cost* — "one small
follow-up costs a full reopen/re-sign cycle" — the retro found the *cause*, and it is a
contradiction inside the protocol rather than a property of the endings model:

> `EP-001/Q-005`'s option B — **the option `spec/question.md` §2 requires a sign-off to offer** —
> told the stakeholder that accepting with a named follow-up meant *"the engagement still closes
> as delivered, and the new work is opened"*. They chose it. Half of it was not executable: an
> engagement ends only from rest, rest requires every child terminal, and the follow-up item is
> created at `draft`.

So the second sign-off is not the price of a conditional acceptance; it is the price of the
protocol promising an ending its own status model forbids, in the sentence it obliges every
sign-off to print. The engagement recorded the discrepancy rather than hiding it and wrote option
B correctly by hand in `Q-006` — *"where nothing carries it forward."*

Direction, from the same source and adopted here: the option's consequence line says what
actually happens — the epic stays `open`, the follow-up is built like any other item, and a fresh
sign-off is due at the next rest — either in `spec/question.md`'s own description of option B or
in whatever `review-close` uses to compose it. **The stakeholder should not learn the mechanics
after they have chosen.** Not fixed in this session: it is a spec change to the sign-off's
required options and belongs with the owner's triage of the retro's proposals, not with the
session that built the reader. Evidence:
`meta/evidence/retro-calibration/iteration-2-retro.md` P-3 and the observation above it.

### Status update 2026-09-10 (META-159, commit bb76d7d) — **fixed, as one sentence**
The addendum's direction, taken in the first of the two places it names: `spec/question.md` §2,
`kind: sign-off`'s `## Options considered` rule. The option that offers a named follow-up now
states the consequence it actually has — **the epic stays `open`, the follow-up is built like any
other item, and a fresh sign-off is due at the next rest** — against the sentence a real sign-off
printed, *"the engagement still closes as delivered, and the new work is opened"*, with the
reason that sentence is unexecutable written beside it (an engagement ends only from rest, rest
requires every child terminal, and the follow-up is created at `draft`) and the stakeholder's own
verdict on the cost quoted: *"more process than I expected for one follow-up request"*.

**No mechanism was built, and that is a conclusion rather than an omission.** The failure this
finding records is a **false sentence**, not a missing capability: the engagement's status model
already did the right thing — it reopened, built WI-0004 through the full pipeline, and asked
again — and the stakeholder's second remark, *"I wasn't asked to take anything on faith either
time"*, says the mechanism was sound. What was wrong was that they chose an option whose printed
consequence was not what would happen. The author of that consequence line is this spec, so this
spec is where the repair belongs. A gate for it would have to decide whether a sentence of prose
is *true*, which is not a thing a program does; the nearest checkable neighbour — *does the
sign-off offer the three options at all* — is a different rule, nothing has been observed failing
it, and filing a finding for it would be manufacturing one. The addendum's *lightweight amendment
path for minor follow-ups* is untouched and stays where the original entry left it: a candidate
whose burden of proof is on the shortcut.

`spec/question.md` revision 10.

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
- Status update 2026-09-10 (META-163): **still deferred, gate unchanged, re-confirmed by
  measurement rather than by assumption.** `python3 scripts/lint-claims --root
  examples/toy-project --all` reports **41 errors** on the current tree — the same 41 META-124
  measured, so nothing this session moved it in either direction, in a session that changed nine
  contracts. The gate is the open-source release, and the reason it is release-blocking and not
  kernel-blocking is unchanged: the example is what a reader opens first.
  **F-108 joins this gate.** It is the same class in the same tree — the shipped example's own
  record is not a model for the rules the toolkit teaches — and the two are one job together and
  two half-jobs apart.

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
- **Status update 2026-09-10 (META-163): open — the stated blocker is GONE, and the finding is
  re-gated rather than left resting on it.** The status above defers on *"the fix touches
  `harness/` while a run is in flight"*. **No run is in flight**: this session ran no iteration in
  any mode, and META-164 provisioned, verified and tore down both staged regressions without
  invoking `run_iteration.py` (commit 8e61fdb). So the reason recorded here has not been true for
  the whole of this session, and nothing said so.
  **It is still not fixed, and the new reason is scope, not safety.** The fix the finding prefers
  — render the sim skill **into the run directory** and point `--add-dir` at it — changes
  `run_iteration.py`'s `SKILL_TARGET`, `render_sim_skill` and every caller, and moves what gets
  banked into the evidence. That is a harness unit, and this session's harness budget went to
  H-020's unsound half (commit 4a59a9a).
  **Gate:** the next harness change window — a unit that opens `harness/` while no run is in
  flight and no evidence is being banked. **The interim guard is operational and is written down
  where it is enforced**, not left implicit: the standing instruction that iterations run
  **sequentially**, which is why 3b and 4b were run one after the other rather than together.

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
- Status: **fixed** (commit b9bc18b, and bb2a6f1 for the companion), with one correction to what
  the finding said. **The main half, as filed:** the prompt already asks the worker for a
  `# Harness status — turn N` heading, so `worker_report()` now reads that number and refuses a
  file stamped for another turn, alongside H-005's mtime test — the two catch different things,
  and 4c's turn 16 is the case only the stamp catches, because it exited cleanly and the file it
  left behind was not stale by mtime, it was somebody else's. The driver now says so on every
  turn that writes no status of its own, not only on a killed one. Two regression tests.
  **The companion's cause was not the one reported.** `board-gen`'s notice was already on stdout;
  what made it read as a failure is that `run-gate` merges a command's stdout and stderr into one
  tail, and the wording — *"not rewriting the timestamp"* — describes a refusal. It now reads
  *"board is current; nothing to rewrite"*, which is the result rather than the abstention.
  Fixing what the finding described would have changed nothing, which is F-054's lesson.

---

### Addendum to F-001 / F-066 (2026-08-30, run 4c) — the named residual: resolution is not support
4c's ending audit caught a universal claim in overview.md whose three citations all resolved
while none supported the sentence — "a citation that resolves is not a citation that supports
the sentence, and lint-claims exits 0 on both" — and repaired it through the legal path with
no code touched. This is the mechanization boundary stated precisely: lint-claims verifies
resolution mechanically; support remains a judgment check owned by D12/DE6 discipline, which
held here. Recorded as the known limitation of the claims machinery rather than a defect;
any future attempt to mechanize "support" starts from this instance as its fixture.

# Builder session 4 (2026-08-30) — the retro skill

## F-074 — the validator reads a journal bullet's first line and calls it the value
- Severity: correctness of enforcement, medium — F-073's class, third occurrence, this time in
  the loader every validator reads through
- Component: scripts/lib/workspace.py (`load_journal`), scripts/validate-workspace
  (`journal.item`, `check_journal_against_history`)
- Symptom: `JOURNAL_BULLET_RE` matched a bullet and took `group("value")` — one line — as the
  bullet's content. A journal bullet that wraps therefore reached every rule half-read. It was
  invisible because it fails in both directions and neither is loud:
  1. **`journal.item` passed on a wrap and would have failed without one.** The rule compared the
     whole bullet value to the item ID, so `**Item:** EP-001` followed by an indented
     parenthetical passed only because the parenthetical was on line 2 and the reader never saw
     it. The same sentence written on one line is a false `journal.item` error on a correct
     entry. `examples/toy-project/tracker/items/EP-001/journal.md:613` is that entry, and it has
     been in the repository since META-067.
  2. **`check_journal_against_history` passes quietly over a wrapped `**Status:**` bullet.** The
     value is parsed for `X → Y`; a bullet broken after the arrow yields no claim at all, and an
     entry claiming a move that never happened — F-019's exact failure, the one direction the
     record could not detect — goes unchecked. This is the F-033 half: it examines nothing and
     reports success.
- Diagnosis: the same mistake F-073 named — *a rule about a record's structure implemented
  against lines* — and it survived F-073's fix because that fix was applied in `lint-answers`,
  where the defect had been observed, rather than to the thing both scripts were doing.
- Evidence: found by META-135's migration, not by a run: moving `load_journal` onto
  `scripts/lib/record.py` made the toy project's wrapped `**Item:**` bullet visible for the
  first time and `./scripts/check` step "must-pass workspace" failed on it. Reproduced in both
  directions before the fix.
- Status: **fixed** (commit 33ec837) — two halves, because either alone leaves it half-read.
  `load_journal` reads a bullet as a `record.Block`, so a bullet's value is its own line **and
  its continuations**; and `journal.item` reads the item ID *out of* the bullet
  (`ITEM_ID_IN_TEXT_RE`) instead of requiring the bullet to be nothing but the ID, which is what
  the rule in `spec/journal-and-history.md` §2.2 actually says. Reverting either half fails
  `./scripts/check`.


## H-018 — an archived run directory says it is still running, with a pid to match
- Severity: harness, operability — latent; nothing acts on it today, which is why it was cheap
  to close now and would not have been later
- Component: harness/run_iteration.py (`archive`)
- Symptom: `--fresh` moves a run directory to `<name>.<n>` and leaves it exactly as it was. Two
  of the seven archives on the owner's machine carry `"status": "running"` in `state.json` and a
  `driver.pid` naming a process that has not existed for days. Nothing distinguishes an archive
  from a live run except its name, and the driver's own orphan-reaper reads pid files.
- Evidence: `harness/runs/iteration-3b-mdtab.1/state.json` and `iteration-4b-recall.1/state.json`
  (`status: running`), each beside a `driver.pid`; `harness/runs/` is gitignored, so this is
  local working state rather than banked evidence.
- Consequence, stated honestly: **no tool reads these today.** The finding is that the record is
  wrong, not that something is broken by it — and a record that is wrong in a way nothing
  currently reads is exactly the kind that is expensive to discover later.
- Status: **fixed** (commit b9bc18b) — `archive()` stamps the moved directory terminal:
  `state.json` becomes `status: archived` with `archived-from-status` keeping what it was, an
  `ARCHIVED.md` says the same thing to a person, and `driver.pid` is removed, since a pid that
  names nothing can only mislead. The seven existing archives were marked with the same function,
  additively — no log was rewritten. Two regression tests.

## H-019 — the iteration-4 configs still budget 24 turns for a run that needs 30
- Severity: harness, configuration — low, and only bites on a rerun
- Component: harness/iterations/iteration-4-recall.json, iteration-4c-recall.json
- Symptom: both declare `"max-turns": 24`. The two runs of that probe and persona were launched
  with `--max-turns 30` from the command line, and `recall-4b` ended at **turn 27** — three turns
  past what its own config would have allowed. A rerun from the config alone would be cut off
  mid-engagement and the stop would read as a budget exhaustion rather than as a misconfiguration.
- Evidence: `meta/harness/evidence/iteration-4b/` (E1 at turn 27/30) and `iteration-4c/run/state.json`
  (`turn: 17`, launched at 30); `harness/iterations/iteration-4b-recall.json` already says 30.
- Note: fixed in **both** files rather than only the one the mission named. Leaving a
  known-wrong number in the sibling config while correcting its twin is fixing the specimen
  instead of the class, which is the shape this session exists to end.
- Status: **fixed** (commit b9bc18b)

## F-075 — `lint-retro` reads a *quoted* citation as a real one, and the first live run reworded its prose to get past it
- Severity: correctness of enforcement, medium — F-037's class in a new reader, producing F-073's
  pathology: a worker rearranging prose to satisfy a parser
- Component: scripts/lint-retro (`check_citations`)
- Symptom: the retrospective is, by construction, the document in a workspace most likely to
  *explain* the citation convention — and `check_citations` scanned an entry's raw text with
  `CITATION_RE`, so a marker written inside backticks as an example was read as a citation and
  reported unresolvable. The live dispatch of the skill against `recall-4c`'s record hit it on
  its first attempt: `lint-retro EP-001` exited 1 with three `retro.citation.unresolved`
  findings, every one of them against a marker the author had quoted rather than made. **The
  execution then reworded the prose until the gate passed**, which is exactly what F-073's first
  half describes and exactly the behaviour a gate must not teach.
- Diagnosis: `scripts/lib/claims.py` has carried the mask for this since F-037 — `mask_code`
  blanks inline code spans while preserving offsets, and `lint-claims` uses it precisely so that
  "a paragraph could satisfy the rule by talking about citations" is impossible. `lint-retro` was
  written against the same citation vocabulary and did not use the same mask. One vocabulary, two
  readers, one of them reading it differently — which is the shape META-134 exists to end, found
  in a script written three units later in the same session.
- Evidence: the live test (META-141), reported by the executing subagent: *"`lint-retro EP-001`
  exit 1 first (3 × `retro.citation.unresolved`, 'an empty citation': literal `src` markers quoted
  in my prose were parsed as citations), exit 0 after rewording."* Reproduced directly against
  `CITATION_RE` before the fix was made.
- Status: **fixed** (commit 78f4c5a) — `check_citations` reads `masked_lines(text)`, the same
  mask `lint-claims` uses. `fixtures/retro` carries **both** directions permanently, because
  masking that swallows a real citation is the worse failure of the two: `EP-001` now quotes a
  marker beside a real one and must produce **nothing**, and `EP-002` carries an observation
  whose only marker is quoted and must be reported as citing nothing (25 codes, was 24).
- Status update 2026-09-11 (META-167, META-168): **fixed** a second time, and this is the
  current status. F-113 is the same class — a mention of the citation vocabulary read as a use
  of it — and the two were closed as one, because fixing either alone leaves the other's
  surface. The 2026-08-30 fix above made `lint-retro` mask like `lint-claims`; it did not make
  masking the *only* rule, and it did not cover a writer who names a form without backticks at
  all. META-167 (commit `cd00504`) made `citations_in()` / `carries_citation()` the single
  reader for every surface — `lint-retro`'s own residual F-054 bug, reading the body off the
  masked line, went with it. META-168 added the half no mask can reach: an unrecognised body is
  now a WARNING (`retro.citation.unrecognised`), because the gate has checked nothing there,
  while a body that matches a form and fails to resolve stays an ERROR. `fixtures/retro` carries
  one of each in `EP-002`'s citation entry (26 codes, was 25), so a classifier stuck at either
  answer is visible in the multiset. The addendum below still stands unchanged: an unbalanced
  backtick still swallows what follows it, and that is still the better of the two failures.

## F-076 — `implement`'s claims gate examines an empty window by construction, every time
- Severity: correctness of enforcement, medium — F-033's class a **third** time, and the variant
  `scripts/lib/scope.py` deliberately calls a pass
- Component: methodology (implement), spec/doc-header.md §5, scripts/lint-claims
- Symptom: `implement`'s hard `claims-are-sourced` gate is
  `scripts/lint-claims --changed-since {{trunk}}` — a window over the documents this branch
  changed. `spec/doc-header.md` §5 says in terms that **`implement` and `verify` do not write to
  `docs/`**, and `plan` writes its ADRs and the overview on the trunk before the branch is cut.
  So the window contains a document only if something wrote one on the branch, and nothing is
  allowed to. The gate is not accidentally empty and not degenerate: it is empty *because the
  toolkit's own rules make it so*, on every execution of `implement` in every engagement.
- Why `scope.py` does not catch it: it models three states, and this is the middle one — *"real
  and empty — the window is well formed and this execution touched nothing in it. That is a pass,
  and it is honest, **because the comparison could have found something**."* That justification
  is what fails here. The comparison could not have found something; the rule that forbids
  `implement` to write documents guarantees it.
- Evidence: found by the retro skill's live dispatch over `recall-4c`'s record
  (`meta/evidence/retro-calibration/live-recall-4c-retro.md` P-1), which cites five journal
  entries in which the engagement's own executions recorded the empty pass rather than banking
  it; independently confirmed against the current kernel — `methodology/skills/implement/skill.yaml`
  carries the gate with `--changed-since {{trunk}}`, and `spec/doc-header.md` §5 forbids the write
  that would put anything in its scope. Corroborated from a second engagement:
  `meta/evidence/retro-calibration/iteration-3-retro.md` reports the same mechanism at WI-0003
  and names `plan`'s trunk commit as the reason.
- Consequence: every `implement` execution records a hard gate as **passed** having examined
  nothing it could ever have examined, and a reader of the journal cannot tell that from a gate
  that looked. Twelve document defects in one banked engagement were caught by D12's *reading*
  while this gate passed on all of them.
- Direction: two moves and they are not alternatives.
  1. **Say which it is.** A window that is empty *by construction* is a third state and should
     print and journal as one — "nothing in this gate's scope could have been written by this
     skill" — so that "passed over nothing" is never spelled the same as "passed".
  2. **Decide whether the gate belongs on `implement` at all.** If §5 holds, it does not, and
     the honest fix is to remove it and say why. If §5 does *not* hold — and it does not, in
     practice: a D7/D12 send-back has had `implement` edit `docs/product/vision.md`
     (`meta/harness/evidence/iteration-3/tracker/items/WI-0004/journal.md`) — then §5 is the
     defect and this gate is right to be there. **The two cannot both stand**, and choosing
     between them is the *document-as-deliverable* derivation, not a patch.
- Status: **deferred**, gated on the *document-as-deliverable* class (F-057, F-058), which
  META-128 triaged into exactly this question and which is an ADR-0006-shaped derivation rather
  than a fix. Filed here with the mechanism proved so the derivation starts from evidence.
  Recorded rather than patched deliberately: rescoping a hard gate on the strength of one
  session's reading, in the session that also introduced the reader, is how a gate gets weakened
  by the thing it was meant to check.
- Status update 2026-09-10 (META-149): **fixed** (commits 3701069, c1fbde8, 5e6434d, 5ae1539).
  Both directions were taken, and the two-way question was answered rather than dodged.
  **`doc-header.md` §5's absolute does not hold, and the gate stays on `implement`**
  (`meta/adr/ADR-0010-document-as-deliverable.md` §6/F-076, commit 3701069; §3.4's rule replaces
  §5's final paragraph in `spec/doc-header.md`, commit c1fbde8; `implement` carries the widened
  gate, commit 5e6434d). Removing the gate instead was rejected in ADR-0010 §8, because it leaves
  the one actor whose ordinary work falsifies documents with no document obligation at all and
  moves the whole of D7 onto `review-close`, which is the arrangement F-087 was filed against.
  Direction 1 — *say which it is* — is `scripts/lib/scope.py`'s **fourth state** (commit 5ae1539):
  *out-of-scope-by-construction*, reached only through `constrained(window, permitted, reason)`,
  which takes the permission knowledge from the caller because **no diff can distinguish "nobody
  wrote a document" from "nobody was allowed to"**. It exits 0 — an item with no documents is
  ordinary work, and a gate that fails on ordinary work is one somebody switches off — but emits
  `claim.scope.by-construction` and prints `NOTHING COULD HAVE BEEN IN SCOPE`, so the journal
  entry a skill copies carries the state and not the verdict. Direction 2 — *make the window able
  to contain something* — is `lint-claims --plan-documents <ITEM>`, which widens rule 2's scope to
  the branch diff **plus** the plan's `## Invalidation set` and `## Deliverable documents`, on the
  reasoning F-087 supplies: the documents a change falsifies are exactly the ones its diff does
  not touch.
  **Decided by execution, not by reading.** `./scripts/check` step *the document window (F-076,
  F-058, 8 cases)*, case 1, is this finding's own shape — the plan names a falsified document,
  the branch never opens it, the document carries an unsourced absolute, and the gate now fails.
  The step was proved non-vacuous against the pre-change scripts: five of its eight cases failed,
  each reporting `0 document(s) in 0 path(s)` — the empty window this finding is about.
  **Left over, named:** the widening brought two edges of its own, filed rather than left to be
  rediscovered — **F-100** (a document disposed `owned-by-ending` is in `implement`'s window and
  outside its reach) and **F-101** (a deliverable document declared outside `docs/` is in the
  window and never examined)

## F-077 — a `path:line` citation resolves for ever, whatever is at the line
- Severity: correctness of enforcement, low — but it is the citation form a reader trusts most
- Component: scripts/lib/claims.py (`CitationResolver._resolve`)
- Symptom: the workspace-path form accepts an optional `:NNN` suffix
  (`spec/doc-header.md` §4a: `[src: src/store.py:42]`). The resolver split the line number off
  and asked whether the **file** existed, so `[src: src/store.py:412]` resolved cleanly against a
  forty-line file, and went on resolving after the code it pointed at moved or was deleted.
- Consequence, and why it is worse than it looks: this is the most precise pointer the convention
  offers and therefore the one a reader is least likely to re-check — it *looks* exact. It is
  also the one most likely to rot, because code moves and documents do not.
- Evidence: found by the retro skill over `iteration-2-tidy`'s record
  (`meta/evidence/retro-calibration/iteration-2-retro.md` P-2); reproduced immediately against
  the resolver — `resolve("scripts/board-gen:9999")` returned `''` on an 85-line file.
- Status: **fixed** (commit 1971ffe) — a `path:line` citation is bounded by the file's length and
  the message says what is wrong rather than blaming the path. Six cases in
  `scripts/lib/selftest.py` (`run_citations`), including the last line, which must resolve.
  A sweep over `examples/toy-project` and all seven fixtures before the change found **no**
  existing citation that would newly fail, so nothing was retroactively invalidated.

## F-078 — the retro's document step named a shape instead of instructing the join, and missed the case it was written for
- Severity: methodology, medium — the skill's own calibration defect, found by the test that
  exists to find it
- Component: methodology (retro 0.1.0, `process.md` steps 4 and 5)
- Symptom: step 5 read *"A version with no execution behind it, or a sentence sourced to a human
  answer that a later answer overtook, is exactly the shape the record is designed to make
  visible."* Every other reading step in the procedure says **what to open and what to compare**;
  that clause says **what to notice**. Run against `iteration-3-mdtab` — the record F-062 was
  filed from — the reading found the *absence* of any cross-answer check and even asserted that
  two of the stakeholder's answers narrow an earlier one, and never reached the sentence in
  `docs/product/vision.md` carrying `[src: WI-0002/Q-001]` that `implement` repaired rather than
  putting back to its author. It classified what it did find as `observation`, severity low,
  `Direction: none proposed`.
- Diagnosis: the join is invisible from inside any single file — the document reads correctly,
  the citation resolves, every gate passes, and the only evidence is a *pair* of answers with an
  edit between them. A procedure that describes such a shape rather than instructing the
  enumeration is asking the reader to notice something no single file shows. The same gap cost
  two more targets in the same run: nothing instructed the reader to consider the questions **as
  a set**, so "every question carries the team's recommendation" (F-063) and "no question is
  open-form" (F-064) — both properties of a *collection*, both countable in a minute once the set
  is enumerated — went unremarked, while the second was found in the *other* engagement's run.
- Evidence: `meta/evidence/retro-calibration/iteration-3-retro.md` (the first run, banked
  unedited) against `meta/findings/FINDINGS.md` F-062, F-063, F-064; the ground-truth subset and
  the scoring are in `meta/journal.md` under META-140, written before and after the run
  respectively.
- Status: **fixed** — `retro` 0.2.0. Step 4 gains a set reading with three counted questions
  (what shape do the questions share, what was never asked, did a later answer narrow an earlier
  one); step 5 splits into 5a (change log against executions) and **5b**, which instructs the
  join outright: find every `[src: <ITEM>/Q-nnn]` under `docs/`, open the cited answer and every
  answer the same person gave afterwards, and where a later one overtakes it, **say which of two
  things the record shows** — the author was asked, or the sentence was repaired. A fourth
  self-check question requires the count of citations followed, and a fourth "goes wrong" entry
  names the class: *reading each file well and never reading the set*.
  **The honest limit on this fix:** it was made after reading the miss, so the re-run recorded
  beside it is a check that the new instruction is followable, **not** an independent measurement.
  The first run's numbers stand as the calibration reading and are not restated.

## F-079 — the retro must journal, and its procedure never said where the entry body may live
- Severity: methodology, low — but it makes the skill's own hard gate unsatisfiable by the route
  a worker will reach for first
- Component: methodology (retro 0.2.0, `process.md` `## Journaling`)
- Symptom: `retro`'s `the-record-was-not-touched` gate counts every file the execution wrote and
  requires the answer to be exactly two. Writing a journal entry means calling the journal tool,
  which takes `--body-file <path>` — and nothing in the procedure said where that path may be.
  The 0.2.0 re-run wrote `retro-entry.tmp.md` **at the workspace root**, noticed, moved it out
  before using it, and declared the whole episode in the gate's own bullet rather than tidying it
  away. That is the right behaviour on a rule that gave it nowhere to stand.
- Diagnosis: F-050's shape in miniature — a rule whose satisfying move is not stated. The route
  exists and is documented in the tool: `--body-file -` reads the body from standard input, so no
  file need exist anywhere. The skill that most needs to know that was the one skill not told.
- Evidence: the executing subagent's own report of the 0.2.0 re-run, and the
  `the-record-was-not-touched` bullet in
  `meta/evidence/retro-calibration/iteration-3-journal-entry-0.2.0.md`, which declares it.
- Status: **fixed** — `retro` 0.2.1: `## Journaling` names `--body-file -`, says why this skill in
  particular may not write a scratch file into the workspace, and says what to do if a file is
  unavoidable — put it outside the workspace and name it in the gate's bullet.

### Addendum to F-075 (2026-08-30, the 0.2.0 re-run) — what the mask costs, said rather than buried
The fix masks inline code spans before reading citations, and an **unbalanced** backtick in prose
therefore blanks everything to the next one — which can swallow a real citation and report a cited
observation as citing nothing. It happened once, on the first `lint-retro` run of the 0.2.0
re-run, and the author rewrote the paragraph: the same rewording-to-satisfy-a-parser this finding
was filed about, now on the other side of the fix.

Left as it is, deliberately, and the reasoning is on the record rather than implied. `lint-claims`
has behaved this way since F-037 and F-054 examined it directly; an unbalanced code span is a
markdown authoring error that renders wrongly too, so the linter is agreeing with the renderer
rather than inventing a rule; and the alternative — reading citations out of unmasked text — is
F-075 itself, where a report that *explains* the convention cannot pass its own gate. **Of the two
failures, masking that swallows a real citation is the one a reader can see and fix in the
document; not masking is the one that makes the document unwritable.** Worth revisiting only if a
second occurrence shows the error is common rather than incidental.

## F-071 — number never filed (tombstone, 2026-08-31)
- This number was skipped: the 3b findings pass (commit f737eae) filed F-069, F-070 and
  H-016; meta/harness/evidence/iteration-3b/README.md:27 cites "F-071", which matches no
  entry and never did — a mislabel of H-016. Confirmed: the README (b2cbb9d) was committed
  66 seconds before the findings commit and named three consecutive F-numbers before they
  were written; the third finding was a harness finding and took H-016 instead. The
  journal's artifacts line for the pass names F-069, F-070, F-072 and H-016, never F-071,
  and F-071 appears in no committed version of this file. The number is burned, not
  reused. The class this exposed is filed as F-099.
- **Status:** not a finding — **tombstone**, and that is its final state. The number is burned
  and the entry is what makes `meta/harness/evidence/iteration-3b/README.md:27` resolve without
  that read-only file being edited. Re-confirmed 2026-09-10 (META-163).

# Findings accepted from retro 0.1.0 proposals (owner triage 2026-08-31)

## F-080 — a skill that makes two transitions has one gate list, and nothing says what its first entry records

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`implement`), `spec/journal-and-history.md` §2.2,
  `scripts/validate-workspace`
- **Symptom:** `implement`'s SKILL.md requires an opening journal entry at the move to
  `in-progress`, "`**Gates:**` recording that the completion gates have not run yet"
  [src: .claude/skills/implement/SKILL.md], while
  `spec/journal-and-history.md` §2.2 admits only `pass`, `fail` and `skipped`. Across eleven
  opening entries the record used three vocabularies — `skipped`, `not yet run`, `not run` —
  and 44 of its 540 gate lines carry a verdict outside the three
  [src: run: grep -rho '\*\*not yet run\*\*' tracker/items/*/journal.md | wc -l → 40]. The
  advisory gate `no-unplanned-scope` appears in all six bug items' opening entries and in none
  of the five work items'
  [src: tracker/items/BUG-0004/journal.md; src: tracker/items/WI-0003/journal.md]. One hard
  gate, `commits-reference-the-item`, is recorded as **fail, not blocking** on a move that
  proceeded [src: tracker/items/WI-0001/journal.md:437] — it fails at the opening transition of
  every `implement` execution, because the branch it inspects has no commits yet. Nothing
  reports any of this: `validate-workspace`'s `journal.bullet.missing` tests that the
  `**Gates:**` label exists and never compares its contents with the acting skill's contract,
  though its hint claims that is what it prevents
  [src: .claude/agile-skills/scripts/validate-workspace].
- **Counterfactual:** any engagement that runs `implement` reaches this, twice per item. The
  first entry is required by the skill, its gates cannot have run, the journal format offers no
  word for that, and a hard gate that reads a commit range must fail on an empty one. Nothing
  about a file-organising tool is load-bearing in that sentence.
- **Recurrence:** eleven times in this engagement, once per `implement` execution, plus five
  further entries in which a `review-close` or `answer-questions` execution had the same problem
  and solved it differently.
- **Direction:** give the format a fourth verdict for a gate that will run later in the same
  execution, and make the check that reads the `**Gates:**` bullet compare its gate names against
  the contract of the skill in the heading rather than only testing that the label is present.
  Separately, decide whether a gate that cannot hold at a skill's opening transition belongs in
  that entry at all.
- **Provenance:** proposed by retro 0.1.0 (iteration-2-retro.md, P-1); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-154): **fixed** (commit 1ebba5a), all three halves, and the
  question it declined to answer is answered.
  **The fourth verdict is `pending`** — `spec/journal-and-history.md` §2.2a, revision 4 — and it
  means *no verdict is owed by this entry, because the acting skill is dispatched again on this
  item and decides the gate at a later transition of the same execution*. Its legality is
  **derived, not named**: an entry whose `**Status:**` records a move into a status the acting
  skill's own `dispatch.on_status` contains. Today that is `implement`'s `planned → in-progress`
  and nothing else in the pipeline, and nothing in the code knows the skill is called
  `implement`. Two other rules were tried against the whole transition table and rejected:
  *pending iff the move is not gated* leaves every `answer-questions` entry permanently pending,
  because that skill has `next_status: null` and so never makes a gating move — nine hard gates
  that would then be decided nowhere; and *pending iff the skill has a `next_status` it has not
  reached* legalises it on `verify`'s send-back, after which no transition of that execution
  follows. `skipped` was the worst of the three vocabularies the engagement invented, because it
  is the word for a gate that checked nothing **and never will**.
  **The comparison** is `scripts/validate-workspace`'s new `check_entry_gates`:
  `journal.gates.missing` (a contract gate the entry omits), `.unknown` (a gate the entry names
  and the contract does not), `.verdict` (a word outside the four), `.unreadable` (a line under
  the bullet that names no gate) and `.pending` (the fourth verdict where no later transition
  follows). It is **scoped to entries whose heading names the installed contract version**: an
  entry records an execution under the contract of its own time, and holding a `v0.1.1` entry to
  a `v0.6.1` gate list would report the skill's history as a defect in the record.
  `journal.version.impossible` already refuses the one version relation that cannot be true;
  this refuses to guess about the rest. The scope was measured before it was chosen — all 55
  `examples/toy-project` entries are one to five minor versions back, and all 67
  `fixtures/abandoned-engagement` entries were at the installed versions and were **completed**
  rather than exempted, which makes them the must-pass side of the fixture pair.
  **The hint this finding caught lying now tells the truth.** `journal.bullet.missing` says every
  §2.2 bullet is required and points at `journal.gates.*` for what the bullet then has to say.
  **The question, answered** — `spec/skill-contract.md` §1.3, revision 6: *a gate that cannot
  hold at a skill's opening transition still belongs in that entry*, recorded `pending`. Three
  readings, one answer. Omitting it makes the entry silent about a check, which is the single
  failure the bullet exists to prevent and is indistinguishable, to a reader, from an execution
  that forgot. Deciding **which** gates cannot hold is a judgement made per gate per skill — the
  branch-on-a-name that a contract-driven gate runner exists to avoid. And the fact is worth
  having: `commits-reference-the-item` inspects a commit range that is empty **by construction**
  at that move, so an entry recording that it was not decided there, and naming where it is
  decided, is a stronger record than one that leaves it out — it is evidence that nobody was
  surprised. Nothing was wrong with the gate's presence; what was wrong was that the format had
  no word for *not owed yet*, so eleven entries invented three and one recorded a hard gate as
  *fail, not blocking* on a move that proceeded.
  **The advisory-gate asymmetry this finding also noted** — `no-unplanned-scope` in all six bug
  items' opening entries and in none of the five work items' — is fixed by the same mechanism
  and not separately: the bullet is composed from the contract, so every gate appears in every
  entry whether or not the worker remembered it.
  Proved by execution in `./scripts/check` step 14c (18 observations, non-vacuity in the strong
  form) and by `fixtures/broken-workspace`, 97 → 102 codes.

## F-081 — the close-before-merge order leaves the merge unrecordable in the entry that reports it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`review-close`), `spec/journal-and-history.md`,
  `scripts/check-commit-refs`
- **Symptom:** `check-commit-refs` inspects `main..branch`, which merging empties, so the close
  must precede the merge — every review in this engagement says so
  [src: tracker/items/WI-0002/artifacts/review.md]. The closing journal entry is therefore
  written before the merge exists, and the journal is append-only with exactly one sanctioned
  in-place edit, a restamped `when`
  [src: .claude/agile-skills/spec/journal-and-history.md]. Six closes solved this three ways:
  three edited the stamped entry to fill in the sha and declared the edit inside it
  [src: tracker/items/WI-0003/journal.md:514; src: tracker/items/BUG-0004/journal.md:432;
  src: tracker/items/BUG-0005/journal.md:374], one used a follow-up commit on the trunk
  [src: tracker/items/BUG-0002/journal.md], and two put the sha in `review.md` instead
  [src: tracker/items/BUG-0001/artifacts/review.md].
- **Counterfactual:** any engagement that closes any item on a branch reaches this. The gate's
  ordering requirement and the record's append-only rule are both correct and they are jointly
  unsatisfiable for one field. Nothing about the product being built enters the argument.
- **Recurrence:** six closes, three different workarounds, three entries edited after stamping.
- **Direction:** give the record a sanctioned place for a fact created after the entry — a
  second, tiny entry appended after the merge, or a named field the transition tool fills in on a
  later invocation — so that the honest answer is not "edit the entry and say so".
- **Provenance:** proposed by retro 0.1.0 (iteration-2-retro.md, P-4); accepted at owner triage 2026-08-31.
- **Status:** fixed (commit 8804bd7) — **a named field, written by a program of its own, and
  checked twice.** `item.md` gains `merge-commit` (`spec/work-item.md` §1), written after the
  merge by `scripts/record-merge` and by nothing else; `spec/journal-and-history.md` §2.2b states
  the general rule the field is an instance of. The three options in the Direction were weighed
  and two were rejected for reasons that hold beyond this case. **A second journal entry** would
  claim a second execution of a skill that ran once — §2 is one entry per *execution* — and the
  entry format would force the tool to invent `**Inputs read:**`, `**Decisions:**` and
  `**Gates:**` in order to record an anti-fabrication fact. **An amendment convention** is a
  second in-place exception to append-only, and §0 already says that wanting one is wanting a
  journal entry instead. What is left is the field, and a later invocation to fill it: the same
  *the record catches up in a second write* shape META-153c and META-154 used where a commit
  cannot cite its own sha.
  **F-035 is not reintroduced, and the reason is structural rather than careful.**
  `record-merge` writes nothing git has not confirmed — that the sha resolves, that it has two
  or more parents, that it is an ancestor of the trunk, and that it contains the item's branch —
  and `validate-workspace` asks the same four questions again on every run through the **same
  function** (`scripts/lib/vcs.py:merge_problems`), so a field somebody typed is held to exactly
  what a field the program wrote is held to: `item.merge.unresolved`, `.not-a-merge`,
  `.unmerged`, `.other-branch`, `.malformed`, `.unexpected`. The other direction is covered too —
  `item.merge.missing` reports a branch that is on the trunk with no sha recorded — and where git
  cannot be asked at all (not a repository, no such branch) nothing is reported, because a check
  that could not look must not claim a pass.
  Proved by execution in `./scripts/check` step 15b, in a throwaway repository that is also a
  workspace: five refusals, each read for the code it gave, each followed by an assertion that
  **no field was written**; the real merge accepted; the field then hand-edited two ways and
  removed once, and the validator catching all three.

## F-082 — a standing delegation has unbounded scope and no route back to the person who gave it

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`refine`, `review-close`), `spec/question.md` §1,
  `spec/dor-dod.md` R8
- **Symptom:** two stakeholder answers about the implementation language and the delivery order
  [src: EP-001/Q-001; src: EP-001/Q-004] were read as standing deferrals over a whole category,
  and 38 `[assumed]` decisions were taken under them across four items
  [src: tracker/items/WI-0001/artifacts/refinement-qa.md;
  src: tracker/items/WI-0003/artifacts/refinement-qa.md]. Several carry real product weight —
  what happens to a file the tool does not recognise, whether hidden files are tidied, whether a
  broken rule file stops every run [src: WI-0001 AC5; src: WI-0004 AC2]. All 38 were recorded,
  tagged and carried into `## Notes`; the protocol was followed exactly. Exactly one reached the
  stakeholder, and it did so because a reviewer chose to put it in a sign-off
  [src: EP-001/Q-006]. `refine`'s own plan named the exposure at the time: "Five assumptions are
  load-bearing and none was confirmed by the stakeholder"
  [src: tracker/items/WI-0001/artifacts/plan.md].
- **Counterfactual:** any engagement whose stakeholder answers one question with "whichever is
  easier for you" hands every later `refine` execution a licence nothing bounds. The Definition
  of Ready records an assumption and the sign-off template names children and accepted gaps;
  neither surfaces the assumptions, and no rule says how far a category delegation reaches.
  Nothing about tidying folders is load-bearing.
- **Recurrence:** four refinement rounds across four items, 38 assumption markers, one surfaced.
- **Direction:** two halves. Make a delegation's scope something the answer records rather than
  something each later execution re-derives — the skill that consumes it writes down what
  category it takes the answer to cover. And give the sign-off a place for the assumptions taken
  under it, alongside the children and the accepted gaps, so that surfacing one is the default
  rather than a reviewer's initiative.
- **Provenance:** proposed by retro 0.1.0 (iteration-2-retro.md, P-5); accepted at owner triage 2026-08-31.
- **Status:** fixed (commit cb344f4) — **both halves, and the reach is under-claimed on purpose.**
  A decision taken under a delegation carries one labelled line beside it —
  `**Under delegation:** <ANSWER-ID> — <category>` — in `refinement-qa.md` next to the
  `[assumed]` tag, in `plan.md` under `## Assumptions`, or in `## Notes`. The form is
  ADR-0008's `Checked against:` precedent rather than a new shape, and it is read by the same
  `record.blocks()`, so a declaration that wraps is one declaration. It is also read **inside**
  another block, because `plan.md`'s natural home for it is under the assumption bullet it
  belongs to and a reader that only looked at a block's own label would pass silently over
  every one of those. The second half is the sign-off: `spec/question.md` §2's sixth sign-off
  rule makes `## Question` name every answer the engagement spent under, with the category and
  what was assumed; at E4, where there is nobody to address, the same list goes into
  `artifacts/review.md`'s `## Ending statement`, which is where an ending's account lives when
  it is a document (§3.5a). `scripts/lint-answers` gains rules 4 and 5.
  **What the lint can see:** that a written delegation's answer ID resolves to a recorded human
  answer or an existing request; that a category is named beside it; and that at an ending —
  `--context epic`, which is how `review-close` runs this gate — every ID so spent appears in
  the sign-off's `## Question` or in the `## Ending statement`. **What it cannot see:** whether
  the delegation really reaches the decision taken under it; whether the category named is the
  category the person meant; whether the assumptions listed beside an ID at the ending are the
  ones actually taken; and, the largest of them, **a delegation relied on and never written
  down at all**. That last one is why the first half lands as Definition of Ready **R12**,
  marked `[skill]` with the measurement beside it rather than as a gate: `[assumed]` is not a
  usable proxy. `examples/toy-project` records **eight** assumed answers, six of which say in
  the same breath that the human confirmed them; one states it was taken under **no** licence
  and names where a later disagreement lands; and exactly one is taken under a licence —
  *"don't hold the item up over it"* — quoted in prose, with no ID and no category, which is
  the case R12 is for. A rule keyed on the tag would fire eight times for one true positive.
  **Half of half 1 already existed and is recorded rather than re-claimed:** `refine`'s step 3
  already said to decide under a standing deferral and to name it. What it had no form for was
  the *category*, the ID, or anything that read the line — and the finding's own evidence is
  that naming it in prose is what happened and what failed.
  Where an engagement has filed neither a sign-off nor an ending statement, rule 5 **says so on
  stdout and reports nothing**: an ending with no ask at all is `check-epic-signoff`'s to
  refuse, and two gates reporting one failure teaches a reader to skim this one's output.
  Nothing is retroactive: no file in `examples/` or `fixtures/` carried the line before this
  change, so the rules were silent everywhere until the fixture gave them cases.

## F-083 — `review-close`'s recorded step order fails its own `workspace-valid` gate

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, low
- **Component:** methodology (`review-close`), `scripts/validate-workspace`
  (`item.outcome.premature`)
- **Symptom:** WI-0003's close records that `outcome: delivered` had to be written **after** the
  transition rather than before it, because `item.outcome.premature` is not among the codes
  `validate-workspace --resolving` downgrades — "so setting the outcome first, which is the
  order `review-close`'s step 9 reads as, fails the `workspace-valid` hard gate on the very move
  that would make it true" [src: tracker/items/WI-0003/journal.md:513]. The execution complied
  and said so; the five other closes are silent about which order they used.
- **Counterfactual:** any engagement closing any item meets it, because the outcome and the
  status change together and one of the two orders is refused by a hard gate every skill runs.
  The product is irrelevant.
- **Recurrence:** recorded once, at WI-0003; the other five closes do not say, which is itself
  the reason to fix the instruction rather than the execution.
- **Direction:** either make the procedure state the order explicitly, or add
  `item.outcome.premature` to the codes `--resolving` downgrades for the move that resolves it.
  The skill should not have to discover that its own written order is illegal.
- **Provenance:** proposed by retro 0.1.0 (iteration-2-retro.md, P-6); accepted at owner triage 2026-08-31.
- **Status:** fixed (commit 8804bd7) — **in the order. The gate is right, and it was deliberately
  not touched.** The Direction offered both; taking both would have been the worse of the two,
  and here is the argument. F-014's downgrade is for a state the move *forces*: a resumed item's
  question is already `answered` while the item is still `awaiting-answer`, and no order of
  operations avoids it. `item.outcome.premature` is not that. A legal order exists and always
  did — `transition --outcome` writes `status` and `outcome` into `item.md` in one act, in step
  3, after the gates of step 2 have run against a workspace where neither field has moved. The
  workspace the procedure produced was invalid because the procedure said to edit `item.md`
  first, not because the validator was wrong; downgrading the code would have legalised the one
  order that leaves a committable, invalid workspace behind (F-038's window, for a field nothing
  had to leave open).
  So `review-close` step 9 no longer reads as an edit: the outcome is the closing transition's
  `--outcome`, named as such, with the reason. And `transition` now refuses to be used the other
  way at all — `--outcome` on a move that does not end at `done`, and a move to `done` carrying
  no outcome, are both refused **before anything is written**, so the illegal order cannot be
  reached through the tool either. `item.outcome.premature`'s hint names the fix.
  Both halves are asserted in `./scripts/check` step 15b, and the refusals are read for the
  *reason they give*: the first draft of the case asserted only that the tool refused, and it
  passed with the guards stubbed out, because the move it used was refused by a gate instead.

## F-084 — a document's version row is a self-reported field with nothing behind it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, low
- **Component:** `spec/doc-header.md` §3, `spec/journal-and-history.md` §0,
  `scripts/validate-workspace` (`doc.updated`)
- **Symptom:** §0 requires a journal entry's timestamp, skill and persona to come from a machine,
  because those were the fields real runs invented
  [src: .claude/agile-skills/spec/journal-and-history.md]. The rule was never extended to a
  document's `updated` field or its change-log `when`, `by` and `for`, which carry the same
  claim about the same things. Forty-five of this record's forty-six version rows fall inside an
  execution of the skill and item they name; `docs/architecture/overview.md` v9 is attributed to
  `implement` on WI-0003 at 22:05:00Z [src: docs/architecture/overview.md], twelve minutes after
  that execution's closing entry and while the item sat at `awaiting-answer`
  [src: tracker/items/WI-0003/journal.md; src: tracker/items/WI-0003/history.md].
  `validate-workspace` checks the field's format and its ceiling and never compares it against
  the executions [src: .claude/agile-skills/scripts/validate-workspace].
- **Counterfactual:** any engagement reaches it, because a change-log row is typed by the same
  worker whose journal heading the toolkit already refuses to let them type. The check that
  would catch it — is there an execution of this skill on this item around this time — needs
  only the tracker.
- **Recurrence:** once in forty-six rows in this engagement. Low, and that is the honest number:
  the discipline held forty-five times without anything checking it.
- **Direction:** extend §0's rule to document headers, and have `validate-workspace` match each
  change-log row against the journal of the item it names, reporting a row whose actor was not
  executing then.
- **Provenance:** proposed by retro 0.1.0 (iteration-2-retro.md, P-7); accepted at owner triage 2026-08-31.
- **Status:** fixed (commit 8804bd7) — as filed, with the boundary written down rather than
  assumed. `spec/journal-and-history.md` §0 now reaches a document's header and change log, and
  `spec/doc-header.md` §3 carries the rules **and** an `[auto]` / `[skill]` table, because the
  row is not uniformly decidable and pretending otherwise is this repository's own failure mode.
  `[auto]`, in `validate-workspace`: the top row and the header agree (`doc.changelog.header`);
  `when` is a UTC timestamp a clock could have produced (`doc.changelog.when`,
  `doc.changelog.timestamp.*`); `by` is a skill this pipeline has (`doc.changelog.actor`); `for`
  is an item in this workspace (`doc.changelog.for`); and the row falls inside an **execution**
  of that skill on that item, matched against its `journal.md` (`doc.changelog.no-execution`).
  `[skill]`, and said so: whether the version *number* is the right one — a change may deserve
  one bump or none, and no program can say which; whether `what changed` describes the change —
  "Updated" passes every mechanical test there is; and whether the named skill made *this* edit
  — the check establishes that an execution of it was running, not that this edit was its work.
  **The execution match is asked only while the item the row names is not yet `done`**, which is
  the line `check_claim_citations`' docstring already draws: a row on a closed item is history,
  and demanding its repair is a demand to rewrite a record rather than to improve one. It costs
  nothing that matters — every skill runs the validator, a row is written during the item's life,
  and the next gate run after it is written is inside the window; the row this finding was filed
  for (`implement`, twelve minutes after its closing entry, the item at `awaiting-answer`) is
  inside it. `./scripts/check` step 15b asserts the boundary as its own case, so moving it fails
  loudly rather than silently widening the rule.
  `scripts/lib/record.py` gains `execution_windows()` and `executed_at()` — an entry is written
  when an execution *finishes*, so its stamp is the upper bound and the entry before it on the
  same item is the lower one; the first entry has no floor at all. Eleven selftest cases,
  including the twelve-minutes-late row this finding names.
  It found a real defect on its first run, which is recorded as **F-108**.

## F-085 — one contract serves two subjects, and at an engagement's ending half of it is undefined

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (review-close), `.claude/skills/review-close/references/contract.md`, `spec/dor-dod.md`
- **Symptom:** `review-close` closes work items and also ends engagements, and its gate list is
  written for the first. Three of its hard gates resolve `{{item.branch}}` or a merge, which an
  epic does not have, and its `definition-of-done` gate says to walk `spec/dor-dod.md` section 3 —
  the work-item checklist — when an ending must be judged by section 4. Every epic-level execution
  in this engagement recorded the same three gates as skipped for the same reason
  [src: tracker/items/EP-001/journal.md], and the termination review recorded walking section 4
  "the contract's wording notwithstanding… as a contract defect rather than followed literally".
  The same contract lists `artifacts/review.md` as an always-output, while the ask-and-stop path
  has no verdict to write, which left the epic's `review.md` asserting "not ended" for eleven
  hours after the finding that caused it had been fixed
  [src: tracker/items/EP-001/artifacts/review.md]. The installed 0.6.0 contract still says
  section 3 and still resolves `{{item.branch}}` [src: .claude/skills/review-close/references/contract.md].
- **Counterfactual:** every engagement reaches an ending, and every ending is judged by a skill
  whose gates were specified for a branch. Nothing about a project's subject matter is load-bearing:
  an epic has no branch in any project.
- **Recurrence:** five epic-level executions in this engagement, each skipping the same three
  gates; once for the section-3/section-4 mismatch; once for the always-output.
- **Direction:** give the ending its own gate list and its own outputs, or make each gate's row
  state its subject so that "skipped, an epic has no branch" is the contract's answer rather than
  the worker's. A gate that is skipped by every execution of a whole class is not a gate.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-1); accepted at owner triage 2026-08-31.
- **Status:** open
- **Status update 2026-09-10 (META-159, commit bb76d7d): fixed** — the second branch of the
  direction was taken, *each gate's row states its subject*, and it is a field rather than a
  habit. `spec/skill-contract.md` §1.3 gives a gate two optional keys: `applies_to`, the item
  types it has a **subject** on — the same key name, syntax and meaning `pipeline.yaml` already
  uses to scope a transition row — and `not_applicable`, the sentence to say where it has none.
  `run-gate` reads them and **does not run the gate** on a type the row leaves out, reporting
  SKIP with that sentence; `transition` composes the `**Gates:**` line from it, so the ending's
  entry carries the contract's words and not the worker's
  [src: scripts/run-gate] [src: scripts/journal-entry].
  **Three of the gates named in the symptom now carry it**, and the third is the one that proves
  the change is not cosmetic. `verification-postdates-the-code` and `commits-reference-the-item`
  already skipped, but by accident — `{{item.branch}}` resolved to nothing and §1.4's placeholder
  rule fired, so the record carried the *resolver's* sentence (*"has no value in the item's
  item.md"*). `tests-pass-on-the-merge-result` resolves `{{commands.test}}`, which an epic has,
  so it **ran the project's suite on the trunk and reported PASS**. One banked execution recorded
  it as skipped on the reasoning that an ending merges nothing, `run-gate` disagreed by running
  it, and the worker corrected their own entry by appending a paragraph beginning *"the claim
  `commands.test` was not run is therefore false as written"*
  [src: meta/harness/evidence/iteration-4b/tracker/items/EP-001/journal.md]. That contradiction
  is now unwritable: the command does not run.
  **No third verdict was coined, and the reason is in the spec.** `journal-and-history.md` §2.2a
  already had two words for a gate with no ordinary verdict, and they answer different questions:
  `skipped` is *there was nothing here to look at*, `pending` is *there was, and the verdict is
  not owed by this entry* (F-080). A contract-declared non-subject is the **first of those,
  reached deliberately instead of by an unresolved placeholder** — one fact, one word, and what
  changed is only who noticed it. Two collapse into one; a third word would have been a
  vocabulary about provenance wearing the clothes of a vocabulary about verdicts. The two sources
  stay distinguishable in the record by the sentence each carries, and a `./scripts/check`
  observation asserts exactly that.
  **Two halves of the symptom were already closed before this unit, and are recorded rather than
  re-claimed.** The section-3/section-4 mismatch was fixed by the 0.10.0 contract, whose
  `definition-of-done` gate already read *"section 3 at an item close, section 4 at an
  engagement's ending"*; META-159 only added §4a's ordering to it (F-086). The `review.md`
  always-output is fixed here, in the outputs row rather than in the `when` enum, which is closed:
  the row now says the ask-and-stop execution writes what was examined and that the engagement
  waits on the stakeholder, **never a verdict**, which belongs to the execution that records the
  ending — the eleven-hour stale *"not ended"* had no contract answer to point at.
  **What was deliberately not scoped.** `epic-sign-off` self-passes on a work item (*"is a
  'work-item', not an epic — the termination gate applies to an engagement's ending only.
  PASS"*), which is the same shape from the other side. It is left alone: this finding is about a
  gate with **no subject**, and that one has a subject and answers about it, so declaring it
  `applies_to: [epic]` would be a scoping the finding did not ask for and would move every
  work-item entry's line from `pass` to `skipped` across the banked fixtures. Named here so the
  choice is a decision rather than an oversight.
  **Fixtures both ways**, in one `./scripts/check` step (*a gate's subject comes from its
  contract row*, 20 observations): on an epic each scoped gate SKIPs carrying its row's exact
  sentence and the test command's sentinel file is **not** created; on a work item the sentinel
  **is** created and no scoped gate skips for want of a subject; a branchless work item still
  skips `verification-postdates-the-code` with §1.4's sentence; the composed journal entry
  carries all three; and four injections into a copied contract prove the lint
  (`gate.applies_to.unknown`, `gate.applies_to` for a list covering every dispatched type,
  `gate.not_applicable` in both directions). **Non-vacuity in the strong form**: with the
  `run-gate` branch and `lint-skills`' `check_gate_subject` body stubbed one at a time, 12 of the
  20 observations fail; with the branch inverted so it skips on **every** type — a scoping that
  scopes nothing — the five work-item observations fail. `review-close` 0.10.0 → **0.11.0**;
  `spec/skill-contract.md` revision 7, `spec/journal-and-history.md` revision 6.

## F-086 — the acceptance is asked for before the epic's Definition of Done is applied, so a late finding invalidates an acceptance already given

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (review-close step 10), `spec/dor-dod.md` §4, `spec/question.md` §2
- **Symptom:** the termination review files the sign-off and stops; DE1–DE6 are applied when the
  reply arrives, because DE7 cannot be satisfied before it [src: tracker/items/EP-001/journal.md].
  Here the stakeholder accepted at 22:29:11Z and the DE6 claim audit — run nine minutes later, in
  the next execution — found a false absolute and filed a bug, which made the engagement leave
  rest and made the sentence *"no bug was filed and left unfixed"* in the question they had just
  answered false [src: EP-001/Q-004]. `check-epic-signoff` then correctly refused that acceptance
  and a second sign-off was due [src: EP-001/Q-005]. The engagement paid one full extra round for
  the ordering, and said so.
- **Counterfactual:** any engagement whose termination review finds anything at DE1–DE6 reaches
  this, because the audit that could find it runs after the question that would be invalidated by
  it. The subject matter of the finding is irrelevant; only its timing matters.
- **Recurrence:** once, and it produced a fourth child item, a second sign-off and a third.
- **Direction:** apply the criteria that do not depend on the reply — DE1 through DE6 — before
  the question is filed, and file the sign-off only against a state that has passed them. DE7
  stays where it is; it is the one that genuinely cannot precede the answer.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-2); accepted at owner triage 2026-08-31.
- **Status:** open
- **Status update 2026-09-10 (META-159, commit bb76d7d): fixed** as the direction says.
  `spec/dor-dod.md` **§4a** states when each epic criterion is applied: DE1, DE2, DE3, DE5, DE6
  and DE4's first half against **the state the stakeholder is about to be shown**, before the
  sign-off is filed; DE4's restatement, DE7 and DE8 after the ending is determined.
  `review-close` 0.11.0 carries it in the `definition-of-done` gate, in step 10 of the procedure
  and as an exit criterion.
  **It is one ordering with ADR-0011's E4 path, and the argument is what makes it one.** F-086
  reads as an acceptance problem — a criterion applied after the acceptance invalidates it — and
  at E4 there is no acceptance to invalidate, so the two orderings could easily have diverged.
  They do not, because the same audit breaks the same thing by a second route: DE6 may file a
  bug, a bug is a **child of the epic**, and the `## Ending statement` must **name every child
  by ID** (F-046, ADR-0011 §2.1), which `check-epic-signoff` enforces by containment. An audit
  run after the statement is written therefore leaves the statement incomplete and the gate
  refuses the ending. So the rule generalises past acceptance: **the engagement's account of
  itself** — the sign-off's `## Question` at E1–E3 and E4 by withdrawal, the `## Ending
  statement` at E4 by silence — is written against a state that has already passed every
  criterion that could change it. The E4 procedure's step 4 now applies DE1–DE6 before writing
  the statement, where before it wrote the statement and walked the checklist afterwards.
  **DE4 splits, and the split was forced rather than chosen.** DE4 has two conjuncts and only the
  first is reply-independent: whether `docs/product/` describes what was built is settled by the
  work, while the restatement of every `## Engagement state` section is required to be written
  *after the ending is determined* (ADR-0010 §4.3 as amended by ADR-0011 §2.4). Applying that
  half early would describe an engagement that had not ended. So the direction's *DE1 through
  DE6* is honoured with that conjunct named, rather than silently contradicting the amendment.
  DE8 joins DE7 for the same structural reason — its elicitation may be filed alongside the
  sign-off, so *answered* cannot hold before the reply — and DE8 did not exist when this finding
  was filed.
  **A DE1–DE6 failure at the ask is not an ending, it is work**: nothing is filed, the finding
  becomes an item or a bug, the engagement leaves rest, and the sign-off is due when it returns —
  which is what *one sign-off per rest* already meant and nothing said out loud.
  **What this legitimises was already happening off the record.** Five epic-level executions in
  banked runs recorded `definition-of-done` as *"skipped, deliberately"* on the reasoning that
  *"applying DE1–DE6 now would decide the thing the question exists to ask"* — and one of them
  listed, in the same entry, every child terminal and named, every outcome recorded and all eight
  success measures addressed
  [src: meta/harness/evidence/iteration-3b/tracker/items/EP-001/journal.md]. The work was being
  done; only the record of it was withheld.
  **No fixture, and the reason is stated rather than skipped.** The ordering is a rule about *when
  a worker performs a read*, and nothing in the workspace distinguishes a Definition of Done
  applied before an acceptance from one applied after it: `definition-of-done` is a
  `manual_check`, so its verdict is the caller's word by design (F-091), and the only mechanical
  trace either way is the same journal entry. The enforcement that does exist is second-order and
  already present — a bug filed at the ask takes the engagement out of rest, and
  `check-epic-signoff` refuses a sign-off filed before rest. `spec/dor-dod.md` revision 10.

## F-087 — the pipeline asks which documents a change touched, and never asks which documents it falsified, until the last gate

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (plan, implement, verify), `spec/dor-dod.md` D7
- **Symptom:** D7 is a `review-close` criterion, so the question "what does this change make
  false?" is first asked after `implement` and `verify` have both passed. The automated gate that
  looks at documents is scoped to what the execution *changed*, not to what it *falsified*, so a
  document the branch never touches is invisible to it [src: tracker/items/WI-0003/journal.md].
  Two items were sent back on D7 and D12 and cleared by editing documents only, each costing a
  full `implement → verify → review-close` cycle with no code change
  [src: tracker/items/WI-0004/journal.md]. The second is the sharper case: WI-0004's plan had
  learned from WI-0003 and carried a step for updating the architecture overview, which
  `implement` executed faithfully; the document that failed was the product vision, which no step
  named [src: tracker/items/WI-0004/artifacts/plan.md]. The installed `plan` skill's own step 8
  still names `docs/architecture/overview.md` and no other document
  [src: .claude/skills/plan/SKILL.md].
- **Counterfactual:** any engagement whose change makes a sentence in a delivered document false
  reaches this, and the later items of any engagement are the ones most likely to. What the
  document says is not load-bearing; that nothing before the last gate is asked about it is.
- **Recurrence:** twice as a send-back (WI-0003, WI-0004); a third time as a finding recorded
  rather than sent back [src: tracker/items/WI-0002/artifacts/review.md].
- **Direction:** make the set of documents a change invalidates an output of `plan` — enumerated
  as a step, from the documents the plan itself cites — and have `implement`'s self-check answer
  D7 before it hands over, so that the last gate confirms the answer instead of discovering it.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-3); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-149): **fixed** (commits 3701069, c1fbde8, 5e6434d, a843114).
  `meta/adr/ADR-0010-document-as-deliverable.md` §5 (commit 3701069) makes the set of documents a
  change falsifies an **output of `plan`**, on the three properties §5 derives: it is answerable
  only by someone who knows what the change does, it is a design output rather than a check, and
  the cost of asking it late is a full cycle — twice, in one banked engagement, with no code
  change in either. The set is `## Invalidation set` in `tracker/items/<ID>/artifacts/plan.md`,
  one row per entry (`| document | what | kind | why | disposition |`), with `## Deliverable
  documents` and `## Binding ADRs` beside it because they belong to the same act (commit 5e6434d).
  `implement` closes every entry with a disposition and **may add entries** — it is the actor that
  discovers mid-change that a fourth document was falsified — `verify` checks the dispositions,
  and **D7 becomes a confirmation against an enumerated set** rather than a discovery
  (`spec/dor-dod.md`, commit c1fbde8). The falsification question is now asked at the stage that
  designs the change and answered where the change is made, which is what this finding asked for.
  Mechanical halves (commit a843114): `lint-documents --rule documents-at-risk-are-enumerated`
  (obligation 11) and `--rule document-writes-are-declared` (obligations 13 + 19), both real
  commands rather than manual checks; and the same set is `lint-claims --plan-documents`'s window,
  so a plan that names nothing is what puts the claims gate into its fourth state (F-076).
  Checked by `./scripts/check` steps *the document window (F-076, F-058, 8 cases)* and *the
  document obligations by execution (F-087, F-093, F-095, 8 cases)*.
  **Left over, named — ADR-0010's obligation 12:** nothing can decide that the set is
  **complete**, and D7 never could either. The honest claim is narrow and ADR-0010 §7 states it:
  the question moves from the last gate to the first stage that can act on it, and being wrong
  about it becomes attributable to a named execution instead of being a memory

## F-088 — a claim audit is passed by an example that could not have falsified the claim

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** `spec/dor-dod.md` D12 and DE6, methodology (review-close)
- **Symptom:** D12 says a claim is checked "by reading it against the code", and leaves the choice
  of what to run to the reader. WI-0002's audit recorded *"no column's width depends on its
  marker"* as **holds**, having laid the same table out under all four markers — a table whose
  cells were wide enough that the rule the sentence denies never applied
  [src: tracker/items/WI-0002/artifacts/review.md]. The unit test named for the claim had the same
  blind spot [src: tracker/items/BUG-0001/artifacts/plan.md]. The sentence was false, and the
  example that shows it is one empty column [src: BUG-0001]. The replacement sentence then passed
  the item's own two reproduce commands and was still false, and what caught it was a verifier
  choosing the boundary instead of the happy path: *"the item's own two reproduce commands both
  agree with the new sentence… the one-colon markers are the case the sentence generalises over
  and gets wrong"* [src: tracker/items/BUG-0001/artifacts/verify-report.md].
- **Counterfactual:** any engagement whose documents state an absolute about a rule with a
  boundary reaches this: the auditor picks the example, and the natural example is the one the
  sentence was written from. Nothing about this project's subject is needed to state it.
- **Recurrence:** twice — the original claim at WI-0002's close, and its replacement at BUG-0001's
  first verification. Both were eventually caught by an example chosen to be able to fail.
- **Direction:** an audit row records the example **and why that example could have falsified the
  claim**; an absolute about a rule with a threshold is checked at the threshold. The audit table
  already has a "what I opened" column; what it lacks is the obligation that what was opened be
  capable of a `false`.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-4); accepted at owner triage 2026-08-31.
- **Status:** **fixed** (META-160)
- **Status update 2026-09-10 (META-160): fixed** (commit `5e43182`). The direction is taken where the finding pointed
  — **the audit row** — by extending the labelled form META-148b already gave it rather than
  starting a second one. `spec/doc-header.md` §4a gains a section, *The example has to be able to
  fail*, and a **fifth label**: `Falsifier:` — what a counterexample would look like, and why the
  thing opened could have produced one. With it, the finding's second half: an absolute about a
  rule with a **threshold, a boundary or an exception** is checked **at** the boundary, and where
  no falsifier can be produced at all the legal move is to weaken the sentence, which is the
  answer §4a already gives for a family nobody can enumerate. `spec/dor-dod.md` D12 and DE6 carry
  it; `review-close` step 9a and `verify` step 6 say it in procedure; `answer-questions`' worked
  example shows it.
  **`scope.py`'s fourth state fits the diagnosis and not the mechanism, and the difference is
  recorded rather than blurred.** The module classifies a *git window* from a repository plus
  caller-supplied permissions; an audit row is prose with no window, no diff and no paths, so
  there is nothing for `constrained()` to re-read. What transfers is the **shape of the verdict**
  — a pass that could not have failed is marked, never spelled like an ordinary pass — and one
  case where the transfer is literal: an enumeration whose `Members:` names nobody is
  out-of-scope-by-construction in the audit row, and `scripts/lint-documents` now exits 0 and
  emits `document.enumeration.vacuous` (a WARNING) rather than passing over it.
  **What is `[auto]` and what is not, said in both specs.** The label's presence is decided only
  where the labelled form was already gated — `propagated-claims-carry-their-obligation`, over an
  answering question's `## Consequences`. Nothing mechanical reads `review.md`'s
  `## What I examined` or `verify-report.md`, before this change or after it, so the falsifier
  there is `[skill]`, recorded the way the rest of D12's read is. Under-claiming is the correct
  failure mode.
  Proved by execution in `./scripts/check` — *the document obligations by execution* is now 10
  cases: a four-part enumeration (the shape every entry in this repository had before this unit)
  is refused with `document.enumeration.incomplete` naming `falsifier`; the five-part one passes;
  `Members: none` passes **with the mark**. Non-vacuity in the strong form: dropping `falsifier`
  from `ENUMERATION_PARTS` fails the first, forcing `vacuous` to `False` fails the third, and
  forcing it to `True` fails the second — the guard bites in both directions.

## F-089 — a criterion that counts artefacts is a criterion that will be amended after the fact

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (refine), `spec/dor-dod.md` R4
- **Symptom:** four criteria in this engagement quantified over things the implementation would
  change — "exactly `2 + max`" [src: WI-0001 AC12], "the suite runs unchanged" [src: WI-0002 AC14],
  "exactly one of its 65 tests changes" [src: WI-0003/Q-002] — and each had to be amended by
  `answer-questions` after the code existed [src: WI-0001/Q-005; WI-0002/Q-003]. Every amendment
  was to a checking clause rather than to a requirement, and each execution checked that
  distinction explicitly, so no criterion was reshaped around what was built; the cost was three
  architect round trips and one criterion that still miscounts while remaining decidable
  [src: tracker/items/WI-0003/artifacts/verify-report.md]. `refine`'s Definition of Ready asks
  that a criterion be decidable; it does not ask whether the quantity it names is one the item
  will move [src: .claude/agile-skills/spec/dor-dod.md].
- **Counterfactual:** any engagement whose item modifies a suite an earlier item shipped reaches
  this, because "unchanged" and "exactly n" are the natural way to write a regression guard and
  both are false the moment the item touches the thing they count.
- **Recurrence:** four reconciliations across three criteria — WI-0001 AC12, WI-0002 AC14, and
  WI-0003 AC9 twice; the record's own running count reached four.
- **Direction:** a criterion names the artefacts it constrains rather than counting them, and
  where a count is genuinely wanted it is measured before the criterion is written. This
  engagement adopted exactly that on its last item and recorded the measurement that justified it
  [src: tracker/items/WI-0004/journal.md]; the practice is not in the toolkit.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-5); accepted at owner triage 2026-08-31.
- **Status:** **fixed** (META-160)
- **Status update 2026-09-10 (META-160): fixed** (commit `5e43182`), as a `[skill]` rule, and the measurement that
  says why it is `[skill]` is part of the fix.** `spec/dor-dod.md` gains **R11**: every criterion
  **names** the artefacts it constrains rather than counting them, and where it states a count of
  something this item may move, the count was **measured before the criterion was written** and
  the criterion carries the measurement as a command-outcome citation
  `[src: run: <command> → <outcome>]` — a citation form that already exists and already resolves
  (`doc-header.md` §4a), so the number acquires a provenance a later reader can repeat.
  `spec/work-item.md` §2 carries the same rule where the criteria are; `refine`'s step 6 and its
  `definition-of-ready` gate description carry it as procedure.
  **No `[auto]` half is claimed, and the reason is a measurement rather than an opinion.** The
  narrowest pattern that catches this finding's own criteria — a cardinal or `no` in front of an
  artefact noun, plus *suite … unchanged/unmodified* — flags **26 of the 53** acceptance criteria
  in the must-pass `examples/toy-project`: *"prints one row per file"*, *"a folder holding one
  readable file"*, *"two files with the same count"*, *"a folder that contains no files at all"*.
  Two of the 26 are true positives. A looser pattern reaches 51 of 53. Telling a count of project
  artefacts from a count in the tool's own output is a read, so R11 is marked judgement and says
  so. That measurement is written into §1 beside the criterion, not left in this ledger.
  **Smaller than billed in one respect, and it is stated:** F-089's own evidence records that no
  criterion was ever reshaped around what was built — every amendment was to a checking clause
  and each execution checked that distinction explicitly. What R11 removes is the round trip, not
  a correctness failure. No fixture accompanies it, for the reason F-086's fix records: nothing
  in a workspace distinguishes a count that was measured first from one that was guessed.

## F-090 — work recorded in an artifact for a skill that is dispatched only by status or by an open question is inert

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (next, review-close), `pipeline.yaml`
- **Symptom:** a review can accept a gap and record that the remedy belongs to
  `answer-questions`; nothing then causes `answer-questions` to run. AC12's amendment was recorded
  by `plan` under `## Assumptions`, confirmed by the first verification, and written into the
  first review as an accepted gap naming the skill that owns it
  [src: tracker/items/WI-0001/artifacts/review.md]; two executions passed over it, and it was
  discharged only because the second verification chose to file a non-blocking question about it
  and said what would have happened otherwise — the obligation would have died at close
  [src: tracker/items/WI-0001/journal.md]. The orchestrator dispatches on status and on open
  questions; an accepted gap is neither [src: .claude/agile-skills/pipeline.yaml].
- **Counterfactual:** any engagement in which a review accepts a gap whose remedy belongs to a
  skill it does not dispatch. The only reason it did not become a lost obligation here is that a
  worker volunteered a question nobody required.
- **Recurrence:** once as a near miss over three executions; twice more the discovering skill
  filed the question immediately, which is the same mechanism working by choice rather than by
  rule [src: WI-0002/Q-003; WI-0003/Q-002].
- **Direction:** an accepted gap that names an owner is a dispatchable thing — either it is
  recorded as an open question at the moment it is accepted, or the board carries it and the
  orchestrator can see it. A to-do that only a reader can act on is not part of the pipeline.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-6); accepted at owner triage 2026-08-31.
- **Status:** **fixed** (META-160)
- **Status update 2026-09-10 (META-160): fixed** (commit `5e43182`). The direction's first branch is taken — *an
  accepted gap that names an owner is recorded as an open question at the moment it is accepted*
  — with the second branch (*the board carries it*) as the legal alternative rather than a
  rival, because which of the two works is decided by **who owns the gap**.
  `review.md`'s `## Accepted gaps` becomes a table, `| gap | owner | disposition |`, the same
  shape as the invalidation set in the same file and for the same reason. The disposition alphabet
  is closed: `question-filed:<ITEM>/Q-###`, `item-filed:<ID>`, `no-owner`.
  **Which disposition is legal for which owner is read off `pipeline.yaml`, never restated.** A
  question suspends its item to the status the `any-suspendable → awaiting-answer` row names, and
  the orchestrator dispatches that status's `owner` — so a question puts to work
  **`answer-questions`, and nothing else**. An item on the board is dispatched at step 5 by the
  owner of the status it sits at — so `answer-questions`, `implement`, `plan`, `refine`,
  `review-close` and `verify` are reachable that way. **`intake`, `next` and `retro` are in
  neither set**: they are dispatched by a stakeholder request (step 2) and by an ended engagement
  (step 7), neither of which `review-close` can cause, so a gap assigned to one of them is inert
  wherever it is written and `document.gaps.undispatchable` says so.
  **"Acceptance time" is the execution that accepts the gap, before its closing transition.**
  `scripts/lint-documents --rule accepted-gaps-are-dispatchable` is a hard gate on `review-close`,
  which runs it while the item is still `in-review`; on an item already `done` it reports
  **NOT APPLICABLE** in those words. That scope was measured before it was chosen: all **18**
  `review.md` files in `examples/` and `fixtures/` sit on `done` items, and unscoped the rule
  refuses every one of them — six inside the must-pass `examples/toy-project` — because they are
  free-prose gap sections written before the convention existed.
  `spec/dor-dod.md` D11 gains the obligation and §3 gains the section *An accepted gap is
  dispatchable or it is nothing*; `review-close` gains step 5a, the table in its `review.md`
  template, a self-check question and an exit criterion.
  Proved by execution in a new `./scripts/check` step, *an accepted gap the orchestrator can act
  on (F-090)* — 15 observations, including the finding's literal shape (free prose naming a skill
  inside the section) and the two well-formed-but-unreachable rows. Non-vacuity in the strong
  form, five stubs: the rule body returned immediately; the two dispatch sets widened to every
  skill; the `inert` branch disabled; the existence checks disabled; the `done` scoping made
  unconditional — each fails exactly the observations that depend on it and no others.
  **What it does not decide, and says so on every run:** whether the question or item named
  actually *discharges* the gap.

## F-091 — nothing reconciles a journal entry's gate verdicts with the gate runner's output

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** `.claude/agile-skills/scripts/transition`, `.claude/agile-skills/scripts/journal-entry`
- **Symptom:** `transition` runs the acting skill's gates, prints a report, and appends the body
  the caller wrote — and the body's `**Gates:**` bullet is composed before the run. Two entries in
  this engagement recorded a verdict the program had contradicted: `epic-sign-off` → **pass**
  where `check-epic-signoff` printed FAIL, and `tests-pass-on-the-merge-result` → **skipped**
  where `run-gate` printed PASS. Both were caught by the executions that wrote them and corrected
  by a later entry, the second naming the cause exactly: *"`transition` prints a gate report and
  appends a journal body, and nothing checks that the two agree"*
  [src: tracker/items/EP-001/journal.md]. Completeness is unchecked in the same way: one
  `implement` entry lists six gates where the other sixteen list seven
  [src: tracker/items/WI-0002/journal.md]. `journal-entry` requires the bullet to exist and reads
  nothing in it [src: .claude/agile-skills/scripts/journal-entry].
- **Counterfactual:** every execution of every skill in every engagement writes this bullet, and
  nothing anywhere compares it to what ran. The two mistakes here were caught by unusually careful
  workers; the format's own premise is that it should not depend on that.
- **Recurrence:** three times in 77 entries — two contradicted verdicts and one omitted gate.
- **Direction:** the tool that runs the gates writes their verdicts into the entry it appends, the
  way the transition tool already owns the `**Status:**` bullet; the worker supplies the evidence
  sentence, not the pass or fail. Short of that, the tool can refuse a bullet that names a gate
  the contract does not list, or omits one it does.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-7); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-154): **fixed** (commit 1ebba5a) — the direction on file, taken
  whole rather than the "short of that" fallback. `scripts/run-gate` gains `--verdicts <path>`,
  writing one `name<TAB>PASS|FAIL|SKIP|MANUAL<TAB>detail` record per gate in contract order;
  `scripts/transition` reads it back and **composes** the `**Gates:**` bullet from the acting
  skill's contract — one line per gate, in contract order, the verdict from the run it just did,
  the evidence sentence from the caller. That fixes the third symptom for free: completeness is
  no longer a property of the caller's memory, so the entry that listed six gates where its
  sixteen siblings listed seven cannot be written. The verdicts arrive by file rather than by
  parsing the human report — scraping stdout would make the report's layout a wire format.
  **A contradicted verdict is replaced and named.** `compose_gates` returns the disagreements it
  found and `transition` prints, per gate, what the body claimed, what the run reported, and
  which one the entry carries; the caller's evidence sentence is kept beside the corrected
  verdict, so the disagreement stays readable instead of being silently erased. Overwriting
  alone would have hidden exactly the two mistakes this finding is made of.
  **Two things stay the caller's, and the reason is the same one:** a `manual_check` gate has no
  command behind it, so nothing the runner did decides it and the tool refuses to invent a
  verdict — a body omitting it is refused rather than filled in; and under `--force` nothing ran
  at all, so the whole bullet stands as written. The override is of the gates, not of the record.
  The gate **names** are checked either way, in both tools, because that needs no run.
  **The ownership story matches F-049's**, and the tools agree with each other: the tool writes
  what it knows, and standalone `journal-entry` requires of the caller what nothing else would
  write. For this bullet the line falls between verdict and name rather than between tool and
  caller — standalone there is no run, so the verdicts stay the caller's, while the names are
  read against the same contract in both places. `transition` says so to `journal-entry` with
  `--gates-checked`, the way it already says the move with `--status`.
  Proved by execution in `./scripts/check` step 14c (18 observations) and by
  `fixtures/broken-workspace`, 97 → 102 codes.

## F-092 — no criterion asks whether a change conforms to the decisions already recorded

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** `spec/dor-dod.md` §3, methodology (implement, verify)
- **Symptom:** the Definition of Done asks that new decisions be written into an ADR (D6) and that
  claims in `docs/` still be true (D12). Nothing asks whether the code and tests obey the ADRs
  that already exist. ADR-0005's rule that a test may not build a document from a Python literal
  was broken twice — once in WI-0001, with a module docstring asserting the opposite
  [src: tracker/items/WI-0001/artifacts/review.md], and once in BUG-0001, after a verification that had passed all
  six of its criteria [src: tracker/items/BUG-0001/artifacts/review.md]. Both were caught only by a
  reviewer reading the diff against the ADR; both cost a send-back. `review-close`'s contract names
  `docs/architecture/adr/` as an input whose purpose is that "the change must not silently
  contradict a recorded decision", and no criterion turns that purpose into a check
  [src: .claude/skills/review-close/references/contract.md].
- **Counterfactual:** any engagement that records an ADR constraining how code or tests are
  written reaches this, and the constraint is invisible to every gate until someone reads for it.
  The content of the rule does not matter; that no stage owns conformance does.
- **Recurrence:** twice, on the same ADR, four items apart.
- **Direction:** make ADR conformance a criterion of its own, applied where the ADRs that bind the
  change are named — most cheaply by having `plan` list the ADRs its steps are constrained by and
  `verify` or `review-close` decide each one, the way D12's claims are decided.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-8); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-149): **fixed** (commits 3701069, c1fbde8, 5e6434d, a843114).
  `meta/adr/ADR-0010-document-as-deliverable.md` §6/F-092 (commit 3701069) splits the obligation
  across the two stages that can carry each half. `plan` lists `## Binding ADRs` — the ADRs its
  steps are constrained by, by ID; it already reads `docs/architecture/adr/` for the purpose of
  not silently re-deciding, so naming what it read is the whole addition. **`verify` decides each
  one**: `verify-report.md`'s `## ADR conformance` carries a row per ID with a verdict of
  `conforms`, `violates` or `not-engaged`; a `conforms` verdict **quotes the clause of that ADR's
  `## Decision`** and names the file and line in the change that satisfies it; a `violates`
  verdict is a send-back; `not-engaged` is legal and must say why (commit 5e6434d).
  **`review-close` checks only that the list is complete** — one criterion asking whether the
  change engages an ADR that `binding-adrs` does not name — which is `spec/dor-dod.md` **D13**,
  new in commit c1fbde8. `verify` rather than `review-close` because `verify` is the stage whose
  entire contract is judging a change against a standard it did not write, it already reads the
  branch, and it is one stage closer to the person who could fix it; both banked violations were
  caught by a reviewer reading the diff against the ADR, and the model moves that read one stage
  earlier and makes it a row rather than a virtue.
  Mechanical half: `lint-documents --rule adr-conformance-is-decided` (obligation 15, commit
  a843114) — one verdict per planned ID, and a `conforms` row that quotes no clause is an error.
  A verdict row for an ADR the plan does **not** name is `document.adr.row.unplanned`, a
  **warning** and not a refusal: refusing the honest move would make reporting an ADR the plan
  missed illegal, which is F-050's shape, and the row is evidence that `binding-adrs` was
  incomplete — which is D13's read, not this gate's.
  **Left over, named:** whether a `conforms` verdict is **right** is judgement (obligation 16),
  and D13's completeness is judgement (obligation 17). Both now sit behind a row that names who
  decided and what they read

## F-093 — a document sentence falsified by the pipeline's own closing act has no item left to carry the fix

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (review-close, answer-questions), `spec/dor-dod.md` D7 and DE4
- **Symptom:** the product vision said the stakeholder had not yet been asked to accept the
  engagement. That was true when `implement` wrote it at 08:05Z and false at 08:22Z, when the
  same closing turn filed the sign-off. The item that owns the document was closed by that turn,
  so `review-close` wrote the document itself and recorded that "there was no send-back available
  that would not have been a fiction" [src: tracker/items/EP-001/journal.md]. `answer-questions`
  wrote the next version and corrected a second sentence beyond its own answer's scope
  [src: docs/product/vision.md]. The review that closed the item had predicted this precise
  sentence going stale and written it into the item's Notes
  [src: tracker/items/WI-0004/artifacts/review.md] — the record saw it coming and had nowhere to
  put it.
- **Counterfactual:** any engagement whose delivered documents describe the engagement's own state
  reaches this, because the last acts of the pipeline are the ones that change that state and the
  items that own the documents are closed by then.
- **Recurrence:** twice in one turn, on the same document, by two different skills.
- **Direction:** either a document section that states the engagement's state is owned by the
  ending rather than by an item — written once, at the ending, by the skill that knows it — or the
  authority to correct it there is stated in the contract rather than reasoned out per execution.
  Both corrections here were declared and defensible; neither was authorised by anything.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-9); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-149): **fixed** (commits 3701069, c1fbde8, 5e6434d, 9adff0e,
  a843114). `meta/adr/ADR-0010-document-as-deliverable.md` §4.3 (commit 3701069) makes the
  engagement-state statement (**K8**) a third claim kind whose sentences live inside a delimited
  `## Engagement state` section, and the section is **owned by the ending**: `intake` writes the
  first one, nothing writes one mid-engagement, and `review-close` restates every section in the
  document set at the ending, **after the sign-off answer arrives** (`review-close`, commit
  5e6434d; DE4 gains it as a criterion and D7/D12 exclude K8 explicitly, commit c1fbde8; `intake`
  and `answer-questions` carry rows L1 and L7, commit 9adff0e). This finding's exact complaint —
  *"both corrections were declared and defensible; neither was authorised by anything"* — is
  answered in the only way that keeps both: the ending's correction is now **authorised**, and the
  mid-flight one is **unnecessary**. An item that finds a K8 sentence falsified records the row
  disposed `owned-by-ending` and leaves it; `answer-questions` does the same through the
  question's `## Consequences`, and nothing is lost, because the ending restates every section it
  finds.
  Mechanical halves (commit a843114): `--rule engagement-state-is-delimited` (obligation 6),
  `--rule engagement-state-is-left-to-the-ending` (obligation 7, a diff over the marked region —
  creating a section counts as writing one), `--rule engagement-state-is-restated` (obligation 8,
  which at an item close prints `NOT APPLICABLE` rather than a pass), and the `owned-by-ending`
  half of `--rule document-writes-are-declared`. Checked by `./scripts/check` step *the document
  obligations by execution (F-087, F-093, F-095, 8 cases)*.
  **Left over, named twice.** ADR-0010's **obligation 10** — that a sentence which *is* an
  engagement-state claim was written **into** a section rather than left loose in the prose — has
  no mechanical half at all and is the foundation the other three rest on; this finding's own
  sentence was written loose. Filed as **F-102**. And ADR-0010 §3.3 item 7 ships unsolved: a false
  sentence found *after* the engagement is closed still has no owner

## F-094 — a criterion cited by number keeps resolving after the number has come to mean something else

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, low
- **Component:** `.claude/agile-skills/scripts/lib/claims.py`, `spec/doc-header.md` §4a
- **Symptom:** criteria may be renumbered while an item is at `draft`, and they were, twice
  [src: tracker/items/EP-001/journal.md]. WI-0003 was filed citing "WI-0002 AC7" and WI-0002's
  round-2 rewrite made AC7 mean something else seven minutes later; `refine` found and corrected
  two such citations by reading [src: tracker/items/WI-0003/journal.md]. The citation resolver
  checks only that the item declares a criterion with that number
  [src: .claude/agile-skills/scripts/lib/claims.py], so both the stale citations resolved cleanly
  the whole time, and `validate-workspace` was green throughout.
- **Counterfactual:** any engagement whose second item cites a first item's criterion by number,
  which is the citation form the spec offers for exactly that purpose. Renumbering at `draft` is
  legal and cheap, and every renumbering silently rewrites every outstanding citation.
- **Recurrence:** twice — once producing two stale citations in another item, once flagged in the
  entry that did the renumbering as a hazard for later readers.
- **Direction:** either a criterion carries an identity that renumbering does not move, or the
  skill that renumbers is required to rewrite the citations that name it — the same obligation
  `answer-questions` already accepts for a `## Consequences` list. A resolver that cannot tell a
  stale citation from a live one should say so where the rule is stated.
- **Provenance:** proposed by retro 0.1.0 (iteration-3-retro.md, P-10); accepted at owner triage 2026-08-31.
- **Status:** open
- **Status update 2026-09-10 (META-157): fixed.** The first branch of the direction was taken —
  *a criterion carries an identity that renumbering does not move* — and it is the criterion's own
  words, quoted inside the citation.
  **F-077's mechanism did not generalise, and the reason is exact.** F-077's fix is a **bound**: a
  `path:line` citation is checked against the file's length. The equivalent bound here — *does the
  item declare an ACn?* — was already `CitationResolver`'s behaviour, and it is precisely the
  check this finding reports as fooled. A bound cannot distinguish a moved target from a standing
  one; only the target's content can. What is extended is F-077's **place**: the same resolver,
  the same convention line, one mechanism rather than two
  [src: .claude/agile-skills/scripts/lib/claims.py] [src: spec/doc-header.md].
  **The form.** `[src: WI-0002 AC7 "sorted by descending line count"]` resolves only while AC7
  still says those words — whitespace, case and backticks ignored, any run of the criterion
  accepted, wrap included. An **unanchored** citation is refused outright while the cited item is
  at `draft` or `ready`, the statuses at which `spec/work-item.md` §2 still permits the criteria to
  be rewritten; the message says why and quotes the criterion's opening words back so the anchor
  can be pasted in.
  **Scoped by measurement, not by taste.** 84 standing `ITEM ACn` citations exist across
  `examples/`, `fixtures/` and the banked run evidence, and **not one** newly fails; requiring an
  anchor everywhere would have invalidated all 84 retroactively, which §4a's own grandfathering
  paragraph forbids. The new rule reports **0** rows over `examples/toy-project` and **0** over
  `fixtures/sourced-claims`, measured before the scope was chosen.
  **What it does not catch is stated where the rule is**, per this finding's third direction:
  past `ready` an unanchored citation still resolves by number alone, so a criterion later edited
  by `answer-questions` propagating an answer can still move under it (`spec/doc-header.md` §4a,
  revision 8).
  **The second branch was not taken as a gate.** *The skill that renumbers rewrites the citations
  that name it* is not decidable from a tree; it is an instruction in `refine` 0.4.0 step 6 and is
  marked instruction-shaped rather than claimed as enforcement.
  **Fixtures both ways:** ten cases in `scripts/lib/selftest.py` (`run_criterion_citations`),
  including the finding itself — one insertion at the top of a list, under two standing citations,
  where the bare number goes on resolving and the anchored one fails — and step 15c of
  `./scripts/check` runs the same pair through `validate-workspace` over a real workspace, at both
  edges of the status window. Six deciding bodies stubbed one at a time; every stub failed cases
  it should. Implemented in commit 181e69d.

## F-095 — a claim quantified over a family is audited by opening the family's shared fixture, and the exception lives in a member

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`review-close`'s D12, `plan`), `spec/dor-dod.md` D12,
  `scripts/lint-claims`
- **Symptom:** D12 asks whether each claim in `docs/` is still true and is satisfied by opening
  what the claim cites. For a claim of the form "every X does Y", what a citation names is the
  shared fixture, and the member that falsifies it is not cited. In this engagement the same
  universal was audited **true** three times, at three item closes, each opening something real —
  a test class's fixture [src: tracker/items/WI-0001/artifacts/review.md:37], four test modules
  named in one row [src: tracker/items/WI-0002/artifacts/review.md:32], one helper in one file
  [src: tracker/items/WI-0003/artifacts/review.md:37] — and the third audit wrote it into the
  document on the strength of that reading [src: docs/architecture/overview.md:170]. The ending's
  audit, whose scope was the whole document set, opened the one file the citations had omitted and
  found two members that falsify it [src: tracker/items/EP-001/artifacts/review.md:133]. The same
  document carried a second claim of the same shape — a module having no operation it in fact does
  not have — through four versions and three items [src: tracker/items/WI-0003/artifacts/review.md].
- **Counterfactual:** any engagement whose documentation describes a property of a family — every
  test, every caller, every handler, no path — reaches this. The auditor opens the citation, the
  citation names the general case because that is what the sentence is about, and the exception is
  in a member the sentence does not name. Nothing about this project's subject is load-bearing;
  `lint-claims` proves a citation resolves and states in its own docstring that it never proves the
  citation supports the sentence.
- **Recurrence:** twice in this engagement in the same document, one of them surviving three audits
  and being restated more strongly by the third.
- **Direction:** treat a quantifier as a distinct kind of claim. A sentence containing an absolute
  over a set should require the auditor to name the set's members and say how the set was
  enumerated, so that "I opened the fixture" and "I enumerated the members" are different entries in
  the audit rather than the same one; the absolutes the gate already detects in `docs/` are the
  place to hang it.
- **Provenance:** proposed by retro 0.1.0 (live-recall-4c-retro.md, P-2); accepted at owner triage 2026-08-31.
- **Status:** open
- Status update 2026-09-10 (META-149): **fixed** (commits 3701069, c1fbde8, 5e6434d, a843114).
  `meta/adr/ADR-0010-document-as-deliverable.md` §4.2 (commit 3701069) makes a quantifier its own
  claim kind, which is exactly this finding's direction: opening what the sentence cites does not
  discharge it, so the audit row carries the **set**, the **enumeration method with its output**,
  the **members** and a **verdict per member**, and a universal that cannot be enumerated is
  weakened rather than recorded as checked. The model keeps this finding's own reading of the
  banked case rather than contradicting it — all three item-level audits were honest and
  *insufficient by construction*, and a model that made them look negligent would be the wrong
  model — so what changed is the entry the audit must produce, not how well it must read.
  `spec/doc-header.md` §4a gains the obligation (commit c1fbde8) and, at revision 6, its
  **labelled form**: `Enumeration:` carrying `Set:`, `Enumerated by:`, `Members:` and `Verdict:`,
  nested under the document's own bullet so one enumeration cannot discharge a claim written into
  a different document (commit a843114). Without a label, nothing mechanical distinguishes *"I
  opened the fixture"* from *"I enumerated the members"*, and telling those two apart is the whole
  of this finding. D12 and DE6 gain the enumeration columns and exclude K8 (commit c1fbde8);
  `verify` and `review-close` carry it where they audit (commit 5e6434d).
  Mechanical half: `lint-documents --rule propagated-claims-carry-their-obligation` (obligation 3,
  commit a843114), checked by `./scripts/check` step *the document obligations by execution
  (F-087, F-093, F-095, 8 cases)*.
  **Left over, named:** completeness of an enumeration is judgement (obligation 4), and obligation
  5 — recognising a sentence **as** quantified — is only partial: both detectors are word lists,
  so a universal carried by a bare plural rather than by a quantifier word is caught by nothing.
  Filed as **F-103**. ADR-0010 §7 also predicts the failure mode to watch: an enumeration
  performed as ritual would be worse than the three honest audits this finding describes

## F-096 — a criterion the environment cannot execute is ticked on a substitution, and the tick carries no mark of it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`verify`, `review-close`), `spec/work-item.md`, `spec/dor-dod.md`
- **Symptom:** WI-0001 AC2 requires a machine restart [src: WI-0001 AC2]. No execution could
  perform one. `verify` considered the `ambiguous` route and declined it as a round trip on a
  criterion whose observable content is decidable, substituted a syscall trace and a post-exit
  read, and ticked [src: tracker/items/WI-0001/journal.md:602]. `plan`, `implement`, `verify` and
  `review-close` each declared the substitution in their own artifact
  [src: tracker/items/WI-0001/artifacts/plan.md:190]
  [src: tracker/items/WI-0001/artifacts/verify-report.md:111]
  [src: tracker/items/WI-0001/artifacts/review.md:101], and it reached the item's `## Notes`
  [src: tracker/items/WI-0001/item.md:155]. In `item.md` the criterion is `- [x] AC2`, spelled
  identically to the seven settled by the observation they name. Every downstream reader — WI-0002's
  close, WI-0003's close, the epic's DE3 — had to re-derive the qualification from prose, and the
  person who could have changed the criterion's wording heard about it first in the sign-off, after
  the work was done [src: EP-001/Q-006].
- **Counterfactual:** any engagement with a criterion naming something its runs cannot do — a
  reboot, a real device, a year elapsing, a second machine — reaches this. The skill's honest
  choices are a tick with a declared substitution or an `ambiguous` that costs a round trip, and the
  tick that follows is indistinguishable in the item from one settled directly. Nothing about
  flashcards is load-bearing.
- **Recurrence:** once as a criterion, and three more times as an inherited accepted gap at the two
  later closes and the ending.
- **Direction:** a criterion settled by something other than the observation it names should be
  marked where the criterion is, not only where the reasoning is — a distinct tick state, or a
  required annotation on the criterion line — and the substitution should oblige somebody to put
  the criterion's wording to the stakeholder while the engagement can still act on the answer,
  rather than disclosing it at sign-off.
- **Provenance:** proposed by retro 0.1.0 (live-recall-4c-retro.md, P-3); accepted at owner triage 2026-08-31.
- **Status:** open
- **Status update 2026-09-10 (META-157): fixed**, both halves of the direction.
  **The mark is a distinct tick state, where the criterion is.** `spec/work-item.md` §2 (revision
  3) now defines three: `- [ ]` not settled, `- [x]` settled by the observation the criterion
  names, `- [~]` settled by a **substitution** — the environment could not perform that
  observation, so something else was observed in its place. `verify` 0.5.0 step 3b writes it as a
  fourth verdict, `substituted`, and no other skill does (a `[skill]` rule: nothing here decides
  which skill edited a line).
  **It follows `scripts/lib/scope.py`'s out-of-scope-by-construction shape, deliberately.** A
  `- [~]` is **settled**: D1 holds (`spec/dor-dod.md` revision 9), `review-close` closes on it,
  `validate-workspace` **exits 0** — and says so in its own words on every run, a WARNING
  `item.criteria.substituted` naming the criterion and what settled it. What was missing was never
  a refusal; it was a different spelling. A gate that fails on legitimate work is one somebody
  switches off, and the honesty lives in the wording.
  **The second half — asking in time — is mechanical.** A `- [~]` MUST name, on the criterion
  itself, a question **on this item** (`item.criteria.substitution.unasked`). The question need
  not be *answered*: the obligation is to ask while the engagement can still act, and an open
  question already holds the engagement short of rest (`spec/ids-and-statuses.md` §3.5), so the
  ending cannot arrive before the answer does — which is exactly what failed here, where the
  person who could have reworded AC2 heard about it at sign-off. That the named question *exists*
  is not re-checked by the new rule: `check_claim_citations` walks `item.md` like every other
  document, so a missing question is already `claim.citation.unresolved`, and a step case asserts
  the division.
  **Fixtures both ways:** `fixtures/broken-workspace` carries the defect (`BUG-0001` AC2,
  substituted, naming no question) **and** the legal substitution (`WI-0003` AC5, citing
  `WI-0003/Q-001`), whose only output is the warning — so the exact-set comparison catches an
  error appearing on a legal one, which a wrong-only fixture cannot prove. 106 → 108 codes. Step
  15c of `./scripts/check` adds the cases a set comparison cannot make: a question on *another*
  item does not count, a named question that does not exist is the citation rule's finding rather
  than a second copy of it, and a done-and-delivered item settled entirely by substitution closes
  D1 while the same item with the box unticked still does not. Implemented in commit 181e69d.

## F-097 — the loop stops on the first human question, so an asynchronous stakeholder is asked one item at a time

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`next`), `pipeline.yaml` `orchestrator.steps` 3 and 5
- **Symptom:** `next` step 3 stops the whole loop on any open human-addressed question, and its
  contract forbids dispatching more than one skill per run. When `refine` suspended WI-0001 with two
  questions, WI-0003 was `draft`, runnable, and had two askable questions of its own; under the
  pipeline as written they would have waited for the first pair to be answered. They did not,
  because this run's harness overrode the one-action rule — WI-0003's `refine` entry names its own
  trigger as *"the harness's batching rule (amendment A)"*
  [src: tracker/items/WI-0003/journal.md:38] — and the four questions were answered in two rounds
  minutes apart [src: WI-0001/Q-001] [src: WI-0003/Q-001]. The workaround is declared, which is why
  it is visible; the thing worked around is in the pipeline.
- **Counterfactual:** any engagement with a stakeholder who answers asynchronously and more than one
  item needing refinement questions reaches this: the cost is one stakeholder round trip per item
  rather than per round, and the only remedy available inside the pipeline is to violate the
  one-action rule. Nothing about this project's subject appears in that sentence.
- **Recurrence:** once in this engagement, and it is the only place the run had to step outside the
  orchestrator's algorithm.
- **Direction:** separate "collect what can be asked" from "dispatch work". A pass that lets every
  currently-runnable item file the questions it can already state, before the loop stops on the
  human, would make one round trip carry them all without giving the scheduler judgement or letting
  two skills run against unwritten state.
- **Provenance:** proposed by retro 0.1.0 (live-recall-4c-retro.md, P-4); accepted at owner triage 2026-08-31.
- **Status:** fixed (commit 6e02a61), derived in `meta/adr/ADR-0012-when-the-loop-stops-on-the-human.md`
  §2 — **by ordering, and the one-action rule is untouched.** The Direction's literal form was
  rejected and the reason is in the ADR: a pass that walks the board deciding what each item
  *could* state is several actions and a judgement, in the one component that must hold none.
  What was wrong was the step order. The halt moved from step 3 to step **5**, below
  `dispatch-answer-questions` and below `dispatch-owner`, so each runnable item is dispatched on
  its own pass, files the questions its own skill can state through its own gates and journal,
  and suspends; the loop then stops once with all of them in front of the person. **The collect
  pass this finding asks for already existed — it is the loop** — and one round trip now carries
  what used to cost one per item. `pipeline.yaml` → 0.10.0, `next` → 0.6.0.
  **What it costs, recorded rather than discovered later** (ADR-0012 §6): the pipeline now keeps
  building while an answer is outstanding, so work invalidated by a pending reply is spent before
  anyone knows — the remedy is the existing one, a blocking question filed on the item that is
  invalidated. And a silent round became a scarcer thing, because the clock only runs on passes
  with nothing else to do, so E4 by silence arrives later than it used to.
  **A third locus the finding did not name:** `record-halt`'s condition was *sufficient* only
  while the halt was step 3. `engagement.dispatchable()` supplies the other half — an open
  request, an answerable question or a runnable item — and it fails **open**, because refusing
  would leave a loop that can neither dispatch nor halt.
  Both directions in `./scripts/check` step 44: a pass with a runnable item records nothing and
  names it; take the work away and the same workspace is a halt at round 1 of 3.

## F-098 — the toolkit's own ADRs and a consumer's ADRs share one citation form and one number space

- **Classification:** toolkit-defect
- **Severity:** doc error, low
- **Component:** `spec/doc-header.md` §4a, `scripts/lib/claims.py`, and the skill prose that cites
  `meta/adr/` by bare number
- **Symptom:** the record cites `ADR-0008 §3` for the toolkit's cross-answer-consistency rule at
  [src: tracker/items/WI-0003/journal.md:537], [src: tracker/items/WI-0003/journal.md:701] and
  [src: tracker/items/WI-0003/artifacts/refinement-qa.md:175], and names the document in full once
  [src: tracker/items/WI-0002/artifacts/refinement-qa.md:158]. This workspace's ADR-0008 is *"Where
  the card file lives, and how it is written"* [src: ADR-0008]. The citation form `ADR-nnnn` is
  defined to resolve inside `docs/architecture/adr/`, so a reader following the number lands on the
  wrong document. The collision is created after the fact: the form is used on EP-001 at 11:20:13Z
  [src: tracker/items/EP-001/journal.md:102] and the project's ADR-0008 is not allocated until
  11:55:01Z [src: docs/architecture/overview.md:174]. Nothing mechanical breaks — these are prose
  references rather than source markers, so no gate resolves them, which is also why nothing
  caught it.
- **Counterfactual:** every consumer reaches this the moment its own ADR sequence passes the numbers
  the toolkit's `meta/adr/` uses, which is to say within the first ten decisions of any project.
  The skills' own prose and specs cite those ADRs by bare number, and a worker quoting the rule it
  is following writes the number down. No project's subject matter is involved.
- **Recurrence:** four times in this engagement, in three different artifacts, all on one item.
- **Direction:** give the toolkit's own decisions a distinguishable citation form in the prose a
  consumer's workers copy from — a prefix, or the path — so that a bare `ADR-nnnn` in a consumer's
  record always means the consumer's own. Resolving the form mechanically in tracker prose, rather
  than only inside a source marker, would then make the collision a finding rather than a reading hazard.
- **Provenance:** proposed by retro 0.1.0 (live-recall-4c-retro.md, P-5); accepted at owner triage 2026-08-31.
- **Status:** open
- **Status update 2026-09-10 (META-163): still open, deferred behind a named gate, and
  re-priced upward — this session grew the collision surface by 62%.** Measured before deciding:
  the shipped prose a consumer's workers read and copy from (`methodology/` and `spec/`) carries
  **97** bare `ADR-nnnn` citations across **11** distinct numbers. **37 of the 97 were written
  this session** — ADR-0010 ten times, ADR-0011 fourteen, ADR-0012 thirteen — so the surface went
  60 → 97 while nobody was looking at this entry. And the collision is not hypothetical even
  inside this repository: `examples/toy-project/docs/architecture/adr/` holds a real, different
  ADR-0001 through ADR-0010, so **every one of the toolkit's ten lowest numbers already names two
  documents in one repo**, ADR-0010 included as of commit 3701069.
  **Not fixed here, and the size is the reason.** The direction is a change of citation *form* —
  a prefix or the path — and it has to move `spec/doc-header.md` §4a, `scripts/lib/claims.py`'s
  resolver, and all 97 citations **in one sweep**; doing part of it leaves two conventions in the
  prose a worker copies from, which is worse than one wrong one. That is not small and it is not
  adjacent to a triage unit.
  **Gate:** one unit that changes the toolkit's own ADR citation form everywhere at once, before
  the open-source release — with F-068 and F-108 in the same release bucket but not the same job.
  Its cost only rises: every ADR this project writes adds citations to the sweep.
- **Note 2026-09-11 (META-169): the mechanism this Direction asks for now exists; the sweep does
  not.** ADR-0013 adds a `toolkit:` citation prefix for the toolkit's own documents, which is
  exactly the *"a prefix, or the path"* this entry proposes, and a consumer writing
  `[src: toolkit: ADR-0012 §2 "…"]` can no longer collide with its own ADR-0012. **This does not
  resolve F-098 and its status is deliberately unchanged:** the 97 bare `ADR-nnnn` citations in the
  shipped prose have not moved, and moving them is the one sweep this entry's gate names. Triage of
  the status line is META-172's job, not META-169's.

### Triage record (2026-08-31)

28 proposals triaged; **19 accepted** as F-080..F-098, each copied verbatim from its retro
report with only its heading and status bullet changed.

- **4 duplicates** of findings already in the ledger: i2-P2 → F-077, i2-P3 → F-061,
  live-P1 → F-076, i3-P12 → F-062 context. Not noise: ADR-0009 §8 hands de-duplication to the
  triager, because the reader has not seen the ledger.
- **4 `project-circumstance` and 1 `observation` correctly classified** — no ledger entries, by
  design. The classification held on every one.
- **0 rejected.** Full-set precision is **28/28 founded**.

Recall against the planted ground truth remains 0.1.0's reading: **1 full hit and 2 partial of
5**. The 0.2.0 re-run is not a measurement and is not counted here (`meta/FINAL-REPORT-4.md`
§4.2).

## F-099 — Citations from banked evidence into the ledger are resolved by nothing
- Severity: correctness of the record, medium — F-024's class, opposite direction
- Component: scripts/check (findings-citations step), meta/harness/evidence conventions
- Symptom: iteration-3b's banked README cites "F-071"; no such entry exists or ever did.
  The check "findings citations resolve" resolves citations within FINDINGS.md and never
  resolves references into it from evidence READMEs — so the durable record can cite
  phantom findings indefinitely. Found by arithmetic during the retro triage (expected 98,
  got 97).
- Evidence: meta/harness/evidence/iteration-3b/README.md:27 vs commit f737eae; ops
  session report 2026-08-31; the F-071 tombstone above.
- Direction: the findings-citation step also scans meta/harness/evidence/**/README.md
  (and meta/**.md generally) for F-###/H-### references and requires each to resolve to a
  ledger heading; a tombstone counts as resolving.
- Status: open
- **Status update 2026-09-10 (META-158): fixed**, and wider than the direction asked.
  `./scripts/check` step **17b, `finding numbers cited resolve`**: every **git-tracked file** is
  read and every three-digit `F-###`/`H-###` in it must match a `## ` heading in this file. A
  phantom is reported as `path:line`. Implemented in commit f61ce10.
  **Scope, and what it excludes.** Not `meta/**.md` as the direction proposed — **no path is
  excluded**. A phantom in `adapters/claude-code/dist/` reaches a user, one in `fixtures/`
  teaches a wrong number, one in `harness/` is in the instrument. What is *not* read: files that
  are not tracked (they are not the record), numbers that are only implied (`F-080..F-098` cites
  two numbers, not nineteen), and citations written in some other form (`F-71`, `F-0071`) — none
  exists: `git ls-files -z | xargs -0 grep -ohE '\b[FH]-[0-9]{1,5}\b' | sort -u` returns
  three-digit forms and nothing else. One tracked path cannot be read as text and is **named on
  stdout every run rather than passed over**: `meta/harness/evidence/iteration-1-full/project` is
  a gitlink (mode 160000, an embedded repository); its 129 files were checked by hand and cite no
  finding number at all.
  **How it reports a phantom in read-only evidence without editing it.** The sweep only reads.
  The correction for a phantom banked in evidence is a **tombstone entry here**, which makes the
  standing citation resolve while the evidence stays byte-identical — F-071's precedent,
  mechanised. A tombstone counts as filed by construction: it is a `## ` heading like any other.
  This is also what makes *reporting* a phantom possible at all, which is a real hazard rather
  than a nicety: the report of a phantom has to quote the phantom, so with the H-001 tombstone's
  heading removed the sweep flags that tombstone's own body (`FINDINGS.md:529-531`) alongside the
  citations it corrects.
  **The first run's full yield, over the tree at 8bd792a: 3276 citations, 128 distinct numbers,
  127 filed, across 1662 tracked files — one phantom.**
  * **H-001**, cited at `meta/harness/evidence/iteration-1-mini/README.md:27` and
    `meta/journal.md:2030`. Never filed; the H-numbering begins at H-002 (commit 5bc2454) and the
    defect those two lines describe was **fixed instead of filed**, in META-081 (commit e7d3c43).
    **Disposition: a tombstone, `## H-001` above. Neither citing file is edited** — one is banked
    evidence, the other an append-only journal. Nothing else in the tree is a phantom; that is
    the whole yield, and it is not zero.
  **The calibration, because a yield of one has to be earned.** The sweep as committed was run
  against a detached worktree at **ff8be8a^ (dda3975)** — the tree exactly as it stood the moment
  before the F-071 tombstone was written, with `iteration-3b/README.md:27` unchanged. It reports
  three phantoms and the first is the known one:
  `F-071 -> meta/harness/evidence/iteration-3b/README.md:27`, at the exact line the tombstone
  names. The other two are `H-001` (same two sites) and `F-101`, then cited by
  `fixtures/retro/README.md:17` and `fixtures/retro/tracker/items/EP-002/artifacts/retro.md:40`
  ahead of its filing in META-149 — a fixture citing a number the ledger does not yet contain is
  the one recurring false-positive shape, and the answer is that the gate is a standing invariant:
  it holds again the moment the filing lands, as it does today.
  **Non-vacuity, in the strong form.** With the resolution stubbed
  (`if cited_number not in filed:` → `if False:`) and H-001 still unfiled, the step reported
  *"PASS finding numbers cited resolve (3342 citations, 128 numbers, 127 filed, over 1662 tracked
  files)"* and the whole gate reported *"check: all steps passed"* — so nothing else in
  `./scripts/check` catches a phantom citation, and this step's body is what decides. With the
  file walk stubbed (`tracked = []`) it reported **SKIP**, *"no file in this repository cites a
  finding number"*, named in the run's closing summary rather than dressed as a pass. Against its
  own new case: removing the `## H-001` heading from this file puts the step back to FAIL on both
  standing citation sites, so the tombstone is load-bearing rather than decorative.

## F-100 — a document the plan hands `implement` to read is one `implement` may be forbidden to repair

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium — a hard gate with no legal way to pass it,
  which is F-050's shape introduced by F-076's fix
- **Component:** `scripts/lint-claims` (rule 2), `scripts/lib/claims.py`, `scripts/lint-documents`
  (`--rule document-writes-are-declared`), methodology (implement), ADR-0010 §4.3 and §5.2
- **Symptom:** F-076's fix widens `implement`'s `claims-are-sourced` window to the branch diff
  **plus** every document the plan names, in its `## Invalidation set` and its `## Deliverable
  documents` [src: scripts/lint-claims]. An entry disposed `owned-by-ending` is in that set, so
  its document enters the window — and `implement`'s instruction for such an entry is
  *"**nothing.** Not a repair, not a tidy"* [src: methodology/skills/implement/process.md]. Rule 2
  does not read only what the diff added: `check_absolutes` walks **every prose paragraph of every
  document in the window** [src: scripts/lib/claims.py], so a `claim.unsourced` that predates the
  branch, in a document the branch never opened, fails a hard gate on `implement`.
  Where the unsourced absolute sits **inside** the `## Engagement state` section, the two gates
  are jointly unsatisfiable. Executed in a throwaway repository, on the current scripts: with the
  sentence unsourced, `lint-claims --changed-since main --plan-documents WI-0001` exits 1 with
  `claim.unsourced`; add the `[src: ...]` and it exits 0, and `lint-documents --rule
  document-writes-are-declared --item WI-0001 --changed-since main` exits 1 with
  `document.engagement-state.written` — *"disposed owned-by-ending and its ## Engagement state
  section was edited on this branch"*. Both gates are **hard** on `implement`, so the item can
  move only under `--force`, which is an override recorded forever, not a repair.
  Where the absolute sits **outside** that section, the same execution shows the scripts allow the
  repair (both gates exit 0 after it) — and `implement`'s procedure still forbids it. That half is
  a contract-versus-procedure contradiction rather than a deadlock, and it is the same shape
  META-148b found and corrected once already between `verify`'s two halves.
- **Counterfactual:** any engagement in which `intake` writes an engagement-state sentence
  containing an absolute about a named code object, and a later item's plan disposes that document
  `owned-by-ending`. Nothing about the sentence's subject is load-bearing; that the window and the
  write permission are computed from the same set by two rules that disagree about it is.
- **Recurrence:** not yet observed in a run — the widening shipped in commit 5ae1539 and no
  engagement has executed against it. Filed on the mechanism, established by execution.
- **Direction:** the window and the reach must be derived from one reading of the set, not two.
  Either rule 2 skips the `## Engagement state` section of a document whose only entry is disposed
  `owned-by-ending` — the section the ending will restate anyway, and which `doc-header.md` §4b
  already treats as a place a citation cannot legally be added — or the `owned-by-ending`
  disposition confers a **narrow** repair licence stated in the contract, so that the honest move
  is legal. Whichever is chosen, `implement`'s procedure and `lint-documents`' rule must say the
  same thing, and the choice belongs beside ADR-0010 §4.3 rather than in a script.
- **Provenance:** the edge was named by META-148's sub-agent when it shipped the widening;
  META-148b's sub-agent reported it **avoided by construction**, on the ground that the quantified
  rule reads only paragraphs new in the diff. META-149 established that both reports cannot stand
  and that **META-148's is the correct one**: the "new paragraphs only" scoping is real but
  belongs to `lint-documents --rule propagated-claims-carry-their-obligation`
  [src: scripts/lint-documents], a different rule on a different skill; `lint-claims` rule 2, which
  is the hard gate on `implement`, has no such scoping. Established by execution in a throwaway
  git repository against the scripts at commit a843114, not by reading alone.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred behind a named gate.** Re-read and
  re-confirmed: the deadlock is unchanged on the current tree and nothing since commit a843114
  has touched either rule. It is not fixed here because the finding's own Direction says where the
  choice belongs — *"beside ADR-0010 §4.3 rather than in a script"* — and it is a choice between
  two defensible mechanisms (rule 2 skips the `## Engagement state` section of an
  `owned-by-ending` document, or the disposition confers a narrow repair licence stated in the
  contract), after which `implement`'s procedure and `lint-documents`' rule must be made to say
  the same thing. A triage unit picking one of those in passing would be deciding an ADR question
  in a script, which is what the finding says not to do.
  **Gate:** the ADR-0010 amendment unit — an ADR-0011-style §4b header pointer (F-067's
  mechanism, since ADR-0010 is standing) choosing one branch, with `lint-claims` rule 2,
  `lint-documents`, `implement`'s procedure and a both-ways fixture moved in the same change.
  **What it costs until then, said plainly:** the pair is jointly unsatisfiable only where the
  unsourced absolute sits **inside** an `## Engagement state` section of a document disposed
  `owned-by-ending`, and the escape is `--force`, which is recorded in the history reason forever.
  No engagement has met it — the widening shipped at commit 5ae1539 and no run has executed
  against it — so the deadlock is still ahead of the first consumer, not behind them. **It ranks
  above F-101 in the same unit**, because a deadlock is worse than an overstated scope line.

## F-101 — a deliverable document declared outside `docs/` is inside the window and outside the rule

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium — F-052's and F-066's class, in the same
  script, reintroduced by the widening that fixed F-076
- **Component:** `scripts/lint-claims` (`documents()`, `widen()`), `scripts/lib/workspace.py`
  (`plan_documents`), ADR-0010 §5.1
- **Symptom:** ADR-0010 §5.1 puts no directory constraint on `deliverable-documents` or on the
  invalidation set's `document` column — the column is described only as "the path"
  [src: meta/adr/ADR-0010-document-as-deliverable.md]. `widen()` adds every declared `.md` path to
  the window and counts it in the scope line, but `documents()` — what rule 2 actually reads —
  walks `os.path.join(root, "docs")` and nothing else [src: scripts/lint-claims]. A declared path
  outside `docs/` is therefore counted, never opened, and — because `declared` is non-empty — it
  also **suppresses the fourth state**, so an item whose only document is outside `docs/` gets a
  plain exit 0 rather than `NOTHING COULD HAVE BEEN IN SCOPE`.
  Executed on the current scripts, with `reference/api.md` as the sole deliverable document and an
  unsourced absolute in it, the gate prints *"absolute claims: 0 document(s) in 1 path(s) in
  scope"* and exits 0. That sentence is the defect stated in the gate's own output: a scope line
  reporting a path the gate did not read is precisely what F-052 filed and what F-066 filed one
  step further on.
- **Counterfactual:** any consumer project whose acceptance criterion is about a document that is
  not under `docs/` — a root `README.md`, a `reference/` tree, an `openapi.yaml`'s companion — which
  is an ordinary shape and one nothing in the spec forbids. The `check-verify-freshness` half is
  unaffected, because a path outside `docs/` was never inside that exemption to begin with.
- **Recurrence:** not yet observed in a run; the widening shipped in commit 5ae1539. Filed on the
  mechanism, established by execution.
- **Direction:** decide it in one place and say it in the spec, not in the script. Either a
  deliverable document **must** live under `docs/` — in which case `plan_documents` rejects a path
  that does not, with a message saying why, and the window is honest again — or rule 2 reads a
  declared document wherever it is, in which case `documents()` stops walking a single directory
  and reads the window's paths. The second is closer to ADR-0010 §5.1 as written; the first is
  cheaper and is a real constraint on a consumer, so it belongs in `spec/workspace-layout.md`
  rather than being inferred from a `walk`. Until then the scope line overstates what was read,
  which is the one thing this script exists not to do.
- **Provenance:** named by META-148's sub-agent as the second of the two edges it left behind when
  it shipped `--plan-documents`; confirmed by execution in META-149 against the scripts at commit
  a843114.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred with F-100 behind the same named
  gate.** Re-confirmed unchanged. The two are one decision seen twice — F-100 asks what the window
  may *repair*, this asks what the window may *read* — and both are answered beside ADR-0010
  (§4.3 and §5.1) rather than in `lint-claims`. Splitting them would mean opening the same ADR
  twice.
  **Gate:** the ADR-0010 amendment unit, as F-100. The choice here is the narrower of the two and
  the finding already names it: either a deliverable document must live under `docs/` — a real
  constraint on a consumer, so it belongs in `spec/workspace-layout.md` — or `documents()` reads
  the window's paths instead of walking one directory. Until then the scope line overstates what
  was read, which is F-052's and F-066's defect in the same script for the third time, and the
  suppressed fourth state means an item whose only document is outside `docs/` gets a plain exit 0
  instead of `NOTHING COULD HAVE BEEN IN SCOPE`.

## F-102 — nothing decides whether an engagement-state sentence was written where the mechanism can see it

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium — the load-bearing gap of ADR-0010 §4.3, accepted at
  derivation and filed here so it is tracked rather than remembered
- **Component:** ADR-0010 §4.3 and its enforcement table (obligation 10), `scripts/lint-documents`
  (`--rule engagement-state-is-delimited`), methodology (intake, review-close)
- **Symptom:** the whole K8 mechanism — obligation 6 (sentences sit inside delimited sections),
  obligation 7 (only `intake` and the ending write inside one) and obligation 8 (the ending
  restates every one) — is enumerable **only over the sections that exist**. Whether a sentence
  that *is* an engagement-state claim was put into one, rather than left loose in the body, is
  obligation 10, and ADR-0010's enforcement table records it as the single obligation in the ADR
  with **no mechanical half at all**: deciding it would mean deciding which sentences are
  engagement-state claims, which is a read [src: meta/adr/ADR-0010-document-as-deliverable.md].
  A document with no `## Engagement state` section and six such sentences in its body passes every
  gate. This is not a suspicion: `fixtures/document-obligations/wrong/docs/process/
  ways-of-working.md` deliberately carries exactly such a sentence and **no rule fires on it**,
  and the absence is asserted as part of that fixture's expected code set. F-093's own sentence,
  in the banked run this all derives from, was written loose.
- **Counterfactual:** every engagement, since obligation 10 is a precondition of the mechanism
  rather than a case within it. If ADR-0010 §4.3 fails in a later run, the ADR predicts this is
  where it fails.
- **Recurrence:** the ADR names it, the module docstring names it, the gate `description` names
  it, and every run of `engagement-state-is-delimited` prints what it cannot see. Filed so that
  four statements of a gap in four places become one entry in the ledger.
- **Direction:** do not try to classify sentences — that is the read the whole thesis says will
  not hold. Reduce the surface instead. `intake` already writes the first section, so the cheapest
  move is to make the section's **existence** mandatory in every deliverable document rather than
  optional, so that "there is nowhere to put it" stops being an available excuse; the residue is
  then a sentence written outside a section that exists, which is a narrower and more suspicious
  act than one written where no section was offered. Whether that residue is worth a heuristic —
  a body sentence naming the engagement, the stakeholder or the sign-off — should be decided
  against a run, not in advance, and under-claiming stays the correct failure mode (F-001).
- **Provenance:** derived and accepted in META-145 (ADR-0010 §4.3 and the enforcement boundary
  table, commit 3701069); restated by META-148b's sub-agent when the eight `[auto]` obligations
  became commands and this one could not (commit a843114); filed as a finding in META-149 so an
  accepted gap is tracked rather than carried in three docstrings.
- **Status:** **open — known, derived and accepted.** Not a defect discovered after the fact: it
  was named in the derivation, its cost was written into ADR-0010 §7, and the mechanism shipped
  with it. It is filed because an accepted gap that lives only in the prose of the decision that
  accepted it is one the next reader re-discovers as news
- **Status update 2026-09-10 (META-163): standing confirmed, not restated — still *open —
  known, derived and accepted*.** Checked for what could have moved it and nothing did:
  ADR-0011 and ADR-0012 are about the loop and about endings, not about where a sentence is
  written; no new `[auto]` obligation was claimed after commit a843114 (obligation 10 is still
  unclaimed); and META-148's *out-of-scope-by-construction* fourth state marks a window nobody
  could write in, which is a different question from where a sentence that **was** written ended
  up. The one live interaction is **F-100**, which is about the same `## Engagement state` section
  from the enforcement side; if the ADR-0010 amendment unit gives that section a rule, this
  entry's residue should be re-read against it in the same unit. Until then it stays what it was
  filed as: a gap named at derivation, shipped with, and tracked here so the next reader does not
  re-discover it as news.

## F-103 — a universal carried by a bare plural is not recognised as a quantified claim by anything

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, low — a known partial reach, filed so the partiality is
  in the ledger rather than only in a word list
- **Component:** `scripts/lib/claims.py` (`ABSOLUTES` / `ABSOLUTE_RE`), `scripts/lib/documents.py`
  (`QUANTIFIER_RE`), ADR-0010's enforcement table (obligation 5)
- **Symptom:** both detectors that stand behind the quantified-claim obligations are **word
  lists**. `ABSOLUTE_RE` — `lint-claims` rule 2's trigger — is seventeen words
  (`no`, `none`, `never`, `always`, `only`, `every`, `all`, `any`, `nothing`, `cannot`, `can't`,
  `impossible`, `guaranteed`, `guarantees`, `exactly`, `must not`, `mustn't`)
  [src: scripts/lib/claims.py]. `QUANTIFIER_RE` — obligation 3's trigger — is six
  (`every|all|no|none|only|each`) [src: scripts/lib/documents.py]. A sentence that is a universal
  by grammar rather than by vocabulary carries neither: *"handlers validate their input"* and
  *"the parser rejects malformed input"* are exactly as strong as *"every handler validates its
  input"*, are the more natural way to write the claim, and match nothing. Executed against both
  regexes in META-149: the quantified form matches `QUANTIFIER_RE`, and the two bare-plural forms
  match neither regex.
  So the enumeration obligation F-095 bought is available only to an author who happened to reach
  for a quantifier word, and the author who did not is not merely unchecked — they are
  **rewarded**, because the weaker-looking sentence is the one that passes.
- **A correction to ADR-0010's own illustration, recorded here because it is a citation that does
  not support its sentence:** the enforcement table gives *"each handler validates its input"* as
  the example of a universal caught by nothing. `each` is in `QUANTIFIER_RE`, so that sentence
  **is** caught by obligation 3; it is not caught by `ABSOLUTE_RE`, so the illustration is right
  about rule 2 and wrong about the quantified rule. The claim the table makes is sound — the
  example it makes it with is not.
- **Counterfactual:** every engagement whose documents describe a property of a family in ordinary
  English. This is F-095's mechanism with the detector removed rather than a new one.
- **Recurrence:** not yet observed as a defect in a run; filed on the mechanism and on the
  derivation that accepted it.
- **Direction:** the gap cannot be closed by lengthening the list — the failure is grammatical,
  not lexical — and a parser is out of proportion. Two moves that are cheap and honest: state the
  partiality in the **spec** (`doc-header.md` §4a) so an author is told which sentence shapes the
  gate can see, rather than leaving it to be inferred from a regex; and make the audit's own
  question ask for the sentence's **form** — an auditor asked "is this sentence a universal?"
  answers correctly on a bare plural where a word list cannot. The `[skill]` half of obligation 5
  already exists for exactly this residue; what is missing is that nothing tells the author it is
  carrying the whole weight.
- **Provenance:** derived and accepted in META-145 (ADR-0010's enforcement boundary table,
  obligation 5, commit 3701069); restated by META-148b's sub-agent as a limit inherited rather
  than solved, and printed on every run of `propagated-claims-carry-their-obligation` (commit
  a843114); filed as a finding in META-149, with the ADR's illustration corrected.
- **Status:** **open — known, derived and accepted.** Same standing as F-102: named at derivation,
  shipped with, filed so it is tracked
- **Status update 2026-09-10 (META-163): standing confirmed, not restated — still *open —
  known, derived and accepted*, the same standing as F-102.** Nothing since commit a843114
  changed obligation 5's `[auto]`/`[skill]` split, and the limit is still printed on every run of
  `propagated-claims-carry-their-obligation`. Re-confirmed rather than left silent, because a
  deliberately-accepted gap and an unexamined one look identical in a ledger read by grep — which
  is F-112.

---

# Cluster 2 — E4 by silence (2026-09-10, META-153b)

Five commits built the mechanism and this section closes its ledger: commits 94606f5 (ADR-0011),
877ee85 (the four specs and `pipeline.yaml`), 4d1b7ce (the programs), e9f8d79 (the fixture) and
b845342 (the harness). Every sha below was verified with `git log -1` and
`git merge-base --is-ancestor` before it was written (F-024).

## Cluster 2 status — E4 was a legal ending nothing could reach; it now executes end to end

- **What it was.** ADR-0006 enumerated four endings and F-045's fix made the termination gate fire
  at rest rather than at closure. **E4 (`abandoned`) had no route.** No trigger, because rest is
  unreachable while a question is open and the stakeholder's silence is what leaves it open; no
  verdict; no branch in `check-epic-signoff`; and — checked rather than assumed — **no fixture**:
  `fixtures/ended-engagement` carries no `abandoned` ending, and `fixtures/abandoned-engagement`
  did not exist before commit e9f8d79. `meta/ROADMAP.md` §2's stamp (2026-08-30) records E2 and
  E4 as *fixture-only*; for E4 that was generous in one direction and exactly right in the other.
- **What it now is.** A second route to E4 — **silence**, counted in the pipeline's own asks —
  derived (commit 94606f5), stated in `spec/ids-and-statuses.md` §3.5a, `spec/question.md`,
  `spec/dor-dod.md` DE7 and `spec/workspace-layout.md` §1.4 with the threshold in `pipeline.yaml`
  (commit 877ee85), programmed as `scripts/record-halt`, the `abandoned` verdict, `next` step 3's
  `silence-is-recorded` gate and `review-close`'s declaration (commit 4d1b7ce), executed both ways
  by `fixtures/abandoned-engagement` (commit e9f8d79), and recognised as an ending rather than a
  stall by the harness driver (commit b845342).
- **Checked by execution, in `./scripts/check`**, which is green at 36 steps:
  - *one silence threshold, three consumers (by execution)* — 18 observations. The value is moved
    3 → 5 in a copy of `pipeline.yaml` and all three consumers move with it; stubbing the reader
    to `return 3` names all three in the failure. The same step proves the reader leaves the log
    byte-identical, and that an answer resets the count while our own writes do not.
  - *the abandoned ending, end to end* — 24 observations, 2 expected codes. `right/` is a
    **valid workspace** (`validate-workspace` exit 0) holding the three states the mechanism has
    to reach; EP-003's trailing digest is **recomputed** from the workspace and required to match,
    so the log cannot assert a silence that did not happen; `wrong/` is four near misses whose
    validator codes must equal `EXPECTED-CODES.txt` as a multiset.
  - *harness self-test* — 105 tests, including one that runs the shipped `engagement-state` over
    the shipped fixture and requires the driver to read a declared E4 out of it.
- **What is still not true of E4, said plainly.** **No live run has produced one.** Every
  execution above is a fixture or a unit test; iteration 5 is a held-out calibration engagement
  and this session did not run it. The substance of `meta/ROADMAP.md` §2's stamp — E4 is not
  run-proven — stands unchanged, and the ROADMAP is not amended by this entry.
- **What the build cost the ledger:** five findings, filed below. Three are defects in the
  programs (F-105, F-106, F-107), one is a contradiction between two contracts that E4 makes
  survivable without fixing (F-104), and one is a dependency the harness took on a sentence
  nothing promises (H-020). None of them was bent around in the build.
- **Existing findings re-decided:** **F-045** — still fixed; the fourth ending it named now
  executes, and two of its edges are filed as F-105 and F-106. **F-060** — **not settled**, and
  deliberately: ADR-0011 §6 puts it out of E4's scope and leaves it deferred behind F-008. Both
  status updates are written at those findings above.

## F-104 — `next` halts on any human-addressed question, so an unanswered elicitation deadlocks every ending

- **Classification:** toolkit-defect
- **Severity:** correctness of the contract, high — two shipped rules that cannot both hold, and
  the one that wins makes every ending unreachable
- **Component:** `methodology/skills/next/process.md` step 3, `scripts/lib/engagement.py`
  (`state()`, the rest condition), `spec/question.md` §2 (`kind: elicitation`)
- **Symptom:** `next` step 3 reads every question and stops the loop where any has
  `addressed-to: human` and `status: open` [src: methodology/skills/next/process.md]; `blocking`
  is not consulted. `spec/question.md` §2 says of an elicitation: *"`blocking` MUST be `false`. It
  must not stop the loop — it is not a thing anyone is waiting on"* [src: spec/question.md]. Both
  cannot hold, and today the first wins: an elicitation nobody answers halts the whole workspace,
  and every runnable item waits behind the one question defined as the one nobody is waiting on.
  **It is not only step 3.** Rest, in `scripts/lib/engagement.py`, requires that *"no question
  anywhere in the engagement — on the epic or on a child — is `open`"*, elicitations included, so
  while one stands open `engagement-state` returns `active` and never `at-rest` — and `at-rest` is
  the orchestrator's only cue to dispatch `review-close` on the epic. Repairing step 3 alone would
  **move** the deadlock rather than remove it: the loop would run and the engagement would still
  have no reachable ending. **E1 included** — the ordinary delivery is as unreachable as the rest.
  `intake` files the elicitation at the start of an engagement, where the answers are cheapest to
  act on [src: spec/question.md], which is also the earliest place the deadlock can be armed. DE8
  is not a third lock: `check-epic-signoff` accepts any answered elicitation in the engagement, so
  a second unanswered one does not block the gate [src: scripts/check-epic-signoff].
- **What E4 changes and what it does not:** with ADR-0011 in the toolkit an engagement deadlocked
  this way now *ends* — step 3(c) dispatches `review-close` once the threshold is reached — so the
  deadlock is no longer permanent. That is strictly better and still not right: the engagement is
  recorded as abandoned by a stakeholder who may never have been told anything was waiting on
  them, in the one case where the pipeline itself declared that nothing was.
- **Counterfactual:** every engagement, because DE8 requires an elicitation and `intake` files it
  first. Nothing about any project's subject appears in that sentence.
- **Recurrence:** not yet observed as a stall in a live run — iterations 1 to 4 answered their
  elicitations. Filed on the mechanism and on the two contracts that contradict each other, both
  of which are in the shipped toolkit today.
- **Adjacent finding — F-097, and what this means for its fix (cluster 5, META-162):** F-097 is
  the *cost* of the same sentence — the loop stops on the first human question, so an asynchronous
  stakeholder is asked one item at a time — and its accepted direction is a *collect what can be
  asked* pass before the loop stops. **That direction does not repair this one.** A pass that
  gathers every askable question and then stops on the human still stops, and an open elicitation
  is still among the questions it stops on. META-162 has to decide **which questions stop the
  loop**, not only how many are asked before it does, and it inherits two consequences of that
  decision that are not F-097's own. First, **rest**: if a non-blocking question stops halting the
  loop it must also stop blocking rest, or the ending stays unreachable. Second, **the silence
  clock**: a silent round is a recorded halt, so an engagement whose only open ask is an
  elicitation would stop accruing rounds and E4 by silence would no longer be declarable over it —
  ADR-0011 §4's rule is that abandonment is only ever declared against an open ask. Deciding F-097
  without deciding those two is how one of them becomes the next finding.
- **Direction:** decide which of the two sentences is the rule, and make the other follow it, in
  one place. If `blocking: false` is to mean what `spec/question.md` §2 says, then step 3 stops on
  blocking human questions only, `engagement.py`'s rest condition counts only those, and ADR-0011
  §3.5a's *ask* is redefined to say whether a non-blocking question is one — with the answer
  written down, because the silence count depends on it. If instead the pipeline is to stop on any
  human question, then §2's sentence is false and must be struck, and an elicitation's
  `blocking: false` becomes a label with no behaviour behind it, which is worth saying out loud
  rather than shipping. The pair is the one thing that must not survive.
- **Provenance:** derived in META-150 while ADR-0011 was being written and recorded there as *"a
  contradiction this derivation surfaced, and did not fix"*, with both citations
  [src: meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md] (commit 94606f5). Carried
  unfiled through META-151, META-151b, META-152 and META-153, each of which named it in its unit
  report as owed to the ledger; filed here by META-153b. The second locus — the rest condition in
  `scripts/lib/engagement.py` — was found by reading the code for this entry and is in no ADR.
- **Status:** fixed (commit 6e02a61), derived in `meta/adr/ADR-0012-when-the-loop-stops-on-the-human.md`.
  **`spec/question.md` §2 is the rule and the other two follow it**, in one predicate rather than
  two repairs. A question stops the loop only if it is an **outstanding ask** —
  `addressed-to: human`, `open`, `blocking: true`, `## Answer` empty — and rest is its
  complement: an open question holds rest unless it is a **standing ask**. `is_outstanding`,
  `is_standing` and `holds_rest` live once in `scripts/lib/engagement.py` and are read by
  `next`'s halt, `record-halt`, the rest condition and the abandonment trigger, so the loci
  cannot drift apart again.
  **Every consequence this entry named was decided rather than inherited.** *Rest*: repaired,
  because repairing step 3 alone would have converted a loop that halts for ever into one that
  idles for ever. *The silence clock*: ADR-0011 §1's claim that the count follows the **halt**
  was checked against the code and survives — `silent_rounds()` reads rows and never a question —
  but §4's boundary sentence did not, and is **narrowed**: abandonment is declared against an
  *outstanding* ask, so an engagement whose only open ask is a standing one accrues no rounds and
  is never declared abandoned over it. That is why rest had to change with it; the two together
  are what make an ending reachable.
  **A fourth locus, found by derivation before it shipped:** DE5 requires an open question closed
  at the ending; the only honest closure for one nobody replied to is `abandoned`; DE8 accepted
  `abandoned` only at E4. A rule requiring a state no legal move can reach — F-013's shape from
  one side, F-050's from the other. `abandoned` is now set by `review-close` at any ending, and
  DE8 accepts it where the waiting log shows the elicitation was **surfaced** to the person, which
  is a half DE8 never had in place of one the pipeline cannot compel.
  Both directions in `./scripts/check` step 44: an engagement whose only open question is a
  standing ask reports `at-rest` and records no halt, and the same workspace with an outstanding
  ask still open reports `active`. With `is_standing` stubbed to `False` the fixture reproduces
  this finding's literal symptom — `EP-001 active`, *"open questions: WI-0001/Q-001"*, for ever.

## F-105 — the termination gate refuses an epic nobody was asked about, and prints no reason at all

- **Classification:** toolkit-defect
- **Severity:** UX of a hard gate, medium — the message is empty in exactly the case F-045 was
  filed about
- **Component:** `scripts/check-epic-signoff` (`main`), `scripts/check` (`TERMINATION_CASES`)
- **Symptom:** where an epic carries no `kind: sign-off` question at all, the loop over `sign_offs`
  never runs, `problems` is empty, `accepted` and `silence` are both `None`, and the gate prints a
  bare header with an empty bullet list and exits 1. Executed on the current scripts:
  `scripts/check-epic-signoff EP-003 --root fixtures/ended-engagement` — F-045's own case, *"an
  engagement nobody was ever asked about"* — prints `check-epic-signoff: FAIL — EP-003 has no
  usable sign-off:` and nothing else; `... EP-001 --root fixtures/abandoned-engagement/wrong` does
  the same.
  The text that would explain it exists: an `if not sign_offs:` block naming DE7, the frontmatter
  to write, and every child by ID. It is **unreachable**, not merely late. Reaching it requires
  passing the `accepted is None and silence is None` return, which means `accepted` is set, which
  means a sign-off was found — and the E4 branch, the one path that can pass with no sign-off at
  all, returns at its own `PASS` two statements earlier. **There is no input for which that block
  prints** [src: scripts/check-epic-signoff].
- **It predates E4, checked rather than taken on trust:** `git show 77a5d96:scripts/check-epic-signoff`
  (commit 77a5d96, 2026-08-29) has the same two returns in the same order, with the explanation
  after the first, and the same argument makes it dead there. The E4 branch (commit 4d1b7ce) added
  a second early exit in front of an already-unreachable one; it did not create this.
- **What it means for the assertion that covers it:** `./scripts/check`'s *the termination gate at
  every ending* runs the F-045 case and asserts `result.returncode != 0` — the exit code and
  nothing else [src: scripts/check]. So the regression that anchors F-045's fix has been green for
  as long as the gate has printed nothing, and would stay green if the gate began refusing for an
  unrelated reason. F-045 exists because a stakeholder was never told what was wanted of them; the
  test that proves it fixed does not read what the gate says. An assertion on a failing exit status
  says that *something* refused, not that the refusal is legible — and for a gate whose entire
  output is one message, legibility is most of what there is to check.
- **Counterfactual:** every engagement whose first ending attempt happens before the sign-off is
  filed, which is the ordinary order — `review-close` is dispatched at rest and files the sign-off
  during that execution. The operator meets a hard gate that refuses with no reason at the moment
  the pipeline is trying to tell them what to do.
- **Recurrence:** the behaviour since 77a5d96, reproduced by two fixtures in the current tree.
  `fixtures/abandoned-engagement/README.md` records it where it shows.
- **Direction:** the empty-list case is the one the message exists for. Print the no-sign-off
  explanation where the refusal is decided — `problems` empty and no sign-off found → the DE7 text
  and the children; `problems` non-empty → the problems — and delete the block that can never run.
  Then make the assertion read the message: give `./scripts/check`'s termination cases an expected
  substring each, so that a refusal for the wrong reason fails. A gate that refuses without saying
  why is F-005's shape in a different program.
- **Provenance:** found by META-152 while building `fixtures/abandoned-engagement` (commit
  e9f8d79), reported in its unit report rather than bent around, and recorded in that fixture's
  README. Confirmed here by execution against both fixtures and against
  `git show 77a5d96:scripts/check-epic-signoff`; the unreachability proof and the reading of the
  assertion are META-153b's.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred behind a named gate, with F-106.**
  Re-confirmed: unchanged on the current tree, and the two are one program and one unit —
  `scripts/check-epic-signoff`, where F-105 is a refusal that says nothing and F-106 is a pass
  that says something false. Both also need the same second half, and it is the more valuable
  half: `./scripts/check`'s `TERMINATION_CASES` asserts `returncode != 0` and reads no message,
  so the regression anchoring F-045's fix cannot tell a right refusal from a wrong one. Giving
  each case an **expected substring** is what makes either fix provable.
  **Gate:** one unit on the termination gate — print the no-sign-off explanation where the refusal
  is decided, delete the block that can never run, make the E4 branch read the reply rather than
  the status (F-106), and give every `TERMINATION_CASES` row an expected message. Not taken here:
  a message change whose whole point is that nothing reads the message is not proved by a triage
  unit editing a print statement, and `fixtures/abandoned-engagement/README.md` plus
  `ABANDONED_NEAR_MISSES` both record today's behaviour as expected and move in the same change.

## F-106 — the termination gate passes a sign-off that says a reply arrived when its `## Answer` is empty

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium — the program whose whole subject is the E3/E4
  distinction cannot make it
- **Component:** `scripts/check-epic-signoff` (the `problems` list, the E4 branch)
- **Symptom:** a sign-off with `status: answered` and an empty `## Answer` is refused correctly on
  the ordinary path: `answer_text(body)` is empty, the loop appends *"says answered but its
  '## Answer' is empty"* to `problems`, and `accepted` stays `None`. The E4 branch then runs —
  it runs whenever `accepted is None` and the threshold is met — and it inspects sign-offs at
  `open` and `abandoned` only. `answered` matches neither, so no silence problem is raised,
  `silence` is set, and `problems` is printed **only** under `if accepted is None and silence is
  None`. The refusal is collected and then discarded [src: scripts/check-epic-signoff].
  Executed against the fixture that carries exactly this case:
  `scripts/check-epic-signoff EP-003 --root fixtures/abandoned-engagement/wrong` exits **0** with
  *"PASS — EP-003 ends at E4 by silence … No reply arrived and none is claimed"* — over a
  workspace in which a reply **is** claimed, in the sign-off's own frontmatter. The gate's own
  output is the finding.
  `spec/ids-and-statuses.md` §3.5 makes this gate the place the distinction is decided: *"E3 and
  E4 are distinguishable from the record alone, and the test is one line: did the stakeholder's
  own words arrive?"* On this input the record says both things at once, and the gate reads the
  emptiness as evidence of silence while ignoring the `status` that contradicts it.
  The workspace is still refused, by something else: `validate-workspace` reports
  `question.answered.section`, and `workspace-valid` is a **hard** gate on `review-close`, so the
  ending cannot be recorded. That is a second program catching it, not this one.
- **Counterfactual:** any engagement whose sign-off is left `answered` with an empty body — a skill
  that wrote the frontmatter and not the reply, or a hand-edit — in an engagement that has also
  reached the silence threshold. Nothing about a project's subject is in it.
- **Recurrence:** covered as a static near miss by `fixtures/abandoned-engagement/wrong` EP-003;
  both the fixture README and `./scripts/check`'s `ABANDONED_NEAR_MISSES` table record the PASS as
  today's expected behaviour, with an instruction to update them if the gate grows the branch. Not
  yet seen in a run.
- **Direction:** the E4 branch should read the sign-off's **reply**, not its `status` — the same
  `answer_text()` the ordinary path already uses — and refuse any sign-off that claims a reply it
  does not have, whatever status it wears. That is one condition, and it makes the gate's own
  sentence *"none is claimed"* true. The wider version belongs with it: `problems` is a list two
  different verdicts share, and the E4 branch's decision to drop it is silent. If a refusal
  collected on the ordinary path is genuinely not a refusal at E4, the code should name which ones
  and why, rather than discarding the list.
- **Provenance:** found by META-152 while building the near misses (commit e9f8d79) and reported
  rather than bent around; confirmed here by execution on the current scripts.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred behind F-105's named gate — same
  program, same unit.** Re-confirmed unchanged. Ranked **first inside that unit**: this is a hard
  gate reaching the wrong verdict (a PASS reading *"No reply arrived and none is claimed"* over a
  record that claims one), where F-105 is a right verdict said badly. The workspace is still
  refused by `validate-workspace`'s `question.answered.section` through the hard `workspace-valid`
  gate, so nothing can be **recorded** on this input — that is a second program catching it, and
  it is why the severity stops at medium rather than rising.

## F-107 — `engagement-state` prints `rest reached at <t>` on engagements that never reached rest

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, low — cosmetic in effect, and a false sentence in a
  program's output
- **Component:** `scripts/lib/engagement.py` (`Engagement.describe`, `rest_boundary`)
- **Symptom:** `describe()` appends `rest reached at {rest_since}` whenever `rest_since` is set,
  under **every** verdict. `rest_since` is `rest_boundary(children)` — the maximum over the
  children's last history rows and their questions' reply times — and it is a **boundary** used to
  date a sign-off against, not a statement that rest happened; any engagement with a child that
  has ever moved has one [src: scripts/lib/engagement.py]. Executed:
  `scripts/engagement-state --all --root fixtures/abandoned-engagement/right` prints
  `rest reached at 2026-09-07T11:00:00Z` under EP-003's **`abandoned`** verdict, two lines below
  that verdict's own reason saying two questions are open and unanswered — an engagement that by
  the module's own definition of rest (every child terminal, no question open, no request open)
  has not reached it and, until someone answers, cannot.
- **Counterfactual:** every engagement at every verdict but the empty one. A reader of an ending's
  record — and `next`'s report quotes this output — is given a timestamp for something that did
  not happen.
- **Recurrence:** pre-existing; the line has been printed for as long as `engagement-state` has
  existed. E4 only made it conspicuous, because `abandoned` is by construction a verdict about an
  engagement that is *not* at rest.
- **Direction:** say what the number is. Print it under `at-rest`, and under the terminal verdicts
  where rest did occur before the ending; elsewhere either omit it or label it as what the code
  itself calls it — the boundary the acknowledgment is dated against — for instance
  `last movement at <t>`. It is a one-line change and the reason to make it is not tidiness: this
  program's output is the pipeline's answer to *is this engagement over*, and a sentence in it
  that is false on most inputs is the class of defect the whole claims machinery exists to catch
  (F-001).
- **Provenance:** found by META-152 against `fixtures/abandoned-engagement` (commit e9f8d79) and
  reported as pre-existing and cosmetic; confirmed here by execution.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred — and the finding's own "one-line
  change" is the reason, established by execution rather than argued.** `grep` over the tree for
  the emitted sentence: the string is asserted verbatim in `harness/tests/test_harness.py:1026`,
  and the code that emits it exists twice — `scripts/lib/engagement.py:150` and the rendered
  `adapters/claude-code/dist/agile-skills/scripts/lib/engagement.py:150`. So the one line is a
  toolkit change **plus** a re-render **plus** a harness-test change, and this repository keeps
  toolkit commits and harness commits separate. It is one line and it is not adjacent.
  **Gate:** the next unit that opens `scripts/lib/engagement.py` while no harness run is in
  flight — most naturally F-110's unit, which is in the same file — taking the fix the finding
  names: print the timestamp under the verdicts where rest occurred, and elsewhere label it what
  the code calls it (the boundary, `last movement at <t>`).
  **Worth carrying:** three separate live runs reported this unprompted in their worker notes
  (iteration 3 turn 4, iteration 4 turns 8 and 10 — *"now three turns running"*). It is the
  only finding in this ledger a stakeholder-facing program has volunteered that many times.

## H-020 — the driver's recognition of a declared E4 rests on a display rule, not on a contract

- **Classification:** harness-defect
- **Severity:** harness, evidence integrity — this reading labels a whole run's outcome, and it
  can be wrong in both directions
- **Component:** `harness/run_iteration.py` (`abandonment_declared`, `SILENT_ROUNDS_RE`,
  `engagement_terminal`), `harness/tests/test_harness.py` (`Abandonment`)
- **Symptom:** the driver stops a run on a **declared** E4 by asking the project's own
  `engagement-state --all` and requiring two things of one epic: a verdict of `ended` or `closed`,
  and a silent-round count in its reasons that has reached the threshold named in the same
  sentence (commit b845342). Refusing to re-derive either number is right and deliberate — a fifth
  implementation of the threshold is F-045's mechanism. What is **not** stated anywhere is that an
  ended engagement's verdict still carries that sentence. It is a consequence of one rule in
  `scripts/lib/engagement.py` — carry the count on every verdict while it is above zero — whose
  stated purpose points the other way in time: ADR-0011 §5 gives it so that *"the clock is visible
  before it strikes rather than only afterwards"*. Nothing in ADR-0011, in
  `spec/ids-and-statuses.md` §3.5a, or in the script's own contract says the sentence survives the
  declaration, and a maintainer who removed it from the terminal verdicts as noise would be
  conforming to every rule that is written down.
  **And the reading is unsound even while the sentence stands.** `silent_rounds` is the trailing
  run of equal digests in an append-only log; nothing resets it, and nothing in it says which
  ending was recorded. ADR-0011 §7 makes E4 deliberately **recoverable** — a returning stakeholder
  reopens the epic through `tracker/requests/` and the engagement can then deliver — after which
  the log's trailing run is untouched and the epic is `done` with `outcome: delivered`. Executed:
  with `fixtures/abandoned-engagement/right`'s EP-001 changed only from `outcome: dropped` to
  `outcome: delivered`, `engagement-state` still reports `ended` with *"3 silent round(s) recorded
  against a threshold of 3"*, and `run_iteration.abandonment_declared()` still returns it — so the
  driver would stamp a delivered engagement's run `abandoned`. What actually says which ending
  happened is the record the driver does not read: the epic's `outcome`, and its history reason
  `E4 abandoned: 3 silent rounds, threshold 3`.
- **Is the harness test enough?** More than the observation assumed, and less than a contract.
  `test_the_real_script_is_read_the_way_the_driver_parses_it` runs the shipped
  `scripts/engagement-state` over the shipped fixture and requires EP-001 and EP-002 to come back
  as declared abandonments — and the harness self-test is the **last step of `./scripts/check`**,
  so a toolkit change that dropped the sentence fails the *toolkit's* own gate today, not merely
  the harness's. Three things it does not do. It `skipTest`s when `fixtures/abandoned-engagement`
  is absent, and a unittest skip exits 0, so the pin disappears silently with the fixture. It is a
  test rather than a statement: it fails a maintainer without telling them which property they
  broke or who needs it. And it cannot catch the unsoundness above, because it only ever runs over
  a fixture whose ending really was E4.
- **Counterfactual:** any harness run against an engagement that reached the threshold and then
  recovered, and any toolkit change that tidies the count out of a terminal verdict's reasons.
- **Recurrence:** not yet observed — no live run has reached E4 at all, and iteration 5 is held
  out. Filed on the mechanism, established by execution.
- **Direction:** the driver should read the ending the toolkit **recorded** and keep the count as
  the corroboration it is: the epic is `done` with `outcome: dropped` and its history reason begins
  `E4 abandoned:` (`spec/ids-and-statuses.md` §3.5a) — facts the record states about itself, which
  a recovered engagement no longer carries. The count belongs in the detail line, as evidence
  rather than as the test. What should **not** happen is asking the toolkit to state a contract for
  the harness's benefit: ADR-0005 keeps the harness out of the contract it grades, and a sentence
  in `engagement-state`'s output that exists because a grader parses it is exactly that.
- **Why `H-` and not `F-`:** the dependency, the inference and the wrong label all live in
  `harness/run_iteration.py`. The toolkit's output is not false — it reports what the count is —
  and no toolkit consumer reads that sentence at all; what happened is that the harness took a
  display rule for a semantic one. Filing it as a toolkit defect would put a harness need on the
  toolkit's backlog, which is the move ADR-0005 exists to refuse.
- **Provenance:** found by META-153 while building the driver's E4 recognition (commit b845342)
  and reported as an observation rather than as a request; that unit's journal entry states the
  dependency in as many words. Filed here by META-153b, with the soundness half and the `H-`/`F-`
  decision established by execution and by reading `scripts/lib/engagement.py` against ADR-0011
  §5 and §7.
- **Status:** open
- **Status update 2026-09-10 (META-153c): the unsound half is fixed (commit 4a59a9a); the
  display-rule dependency it was filed for stands, and can no longer mislabel a run.** Taking the
  serious half first, because it is the one that could stamp the wrong ending on a whole run.
  `abandonment_declared()` no longer tests the count. It
  tests the **ending the toolkit recorded**: `engagement-state` says the engagement has ended
  (`ended`, or `closed` once the retro is written), *and* the epic it ended is `done` with
  `outcome: dropped`. `spec/ids-and-statuses.md` §3.5 gives that pair to E4 and to no other ending
  — E1 records `delivered`, E2 `delivered-partial`, E3 leaves the epic `blocked` — and unlike
  anything derived from the waiting log it is **current state**, so a stakeholder who comes back,
  reopens the epic (ADR-0011 §7) and gets a delivery overwrites it. That is exactly the property
  the count lacks, and it is the direction above, taken as written.
  The count is now **corroboration** and appears only in the detail line, quoted from
  `engagement-state`'s own sentence when the verdict carries one. This is what makes the
  display-rule dependency stop mattering: a maintainer who tidied the sentence out of the terminal
  verdicts as noise would cost the driver a phrase of evidence, not its recognition of the ending.
  The other half of the direction — the history reason beginning `E4 abandoned:` — was
  **considered and not taken**, and the reason is the same soundness argument: a recovered
  engagement's history still holds that row, because history is append-only too, so the prefix
  distinguishes the two endings only if the driver also decides which row is the last one. The
  frontmatter says it in one field.
  **The reading is now complete as well as sound.** Requiring the count missed E4's *other* route:
  a withdrawal (§3.5) is an act the stakeholder performs, so it ends the engagement at E4 with no
  silent round ever recorded, and the old predicate reported such a run as `epic-done` or
  `blocked-no-recourse`. It is now recognised, with a detail line that claims no silence.
  **Non-vacuity, by execution.** Five tests in `Abandonment` fail against the old predicate and
  pass against the new one, the deciding two being
  `test_the_declaration_is_read_off_the_record_not_off_the_count` — one byte-identical
  `engagement-state` output over two records, `[('EP-001', 3, 3)] != []` under the old reading —
  and `test_a_recovered_engagement_that_delivered_is_a_delivery`, the whole path, where the old
  reading gives `'abandoned' != 'epic-done'`. The genuine E4 cases and the `stalled`/`abandoned`
  distinction from META-153 are unchanged and still green. Self-test 105 → **110**.
  **What did not change, deliberately.** The driver still asks rather than re-derives: the verdict
  is `engagement-state`'s, both numbers come out of one sentence of its output, and
  `test_the_driver_holds_no_threshold_of_its_own` — no `threshold_rounds`, no `tracker/waiting`,
  no `pipeline.yaml` in the driver's source — is still green (F-045's mechanism, refused
  structurally). No toolkit change was made or needed: **the signal was not in `engagement-state`'s
  output** (its `ended` reason names the epic's *status* and not its `outcome`) and it did not have
  to be, because the epic's frontmatter is already in every reading `scan_project` takes. Asking
  the toolkit to add it for the grader's benefit is the ADR-0005 move this finding refused when it
  was filed.
  **Still open, and unfixed here:** the *first* half of this finding. Nothing yet **states** that
  a terminal verdict carries the silence sentence, and the fixture pin
  (`test_the_real_script_is_read_the_way_the_driver_parses_it`) still `skipTest`s — exiting 0 —
  when `fixtures/abandoned-engagement` is absent. Neither can now
  mislabel a run; both are unpromised dependencies of a detail line, which is the standing this
  finding leaves them in.
- **Status update 2026-09-10 (META-163): open on its remaining half, deferred behind H-015's
  harness gate.** Re-confirmed: the serious half is fixed at commit 4a59a9a and cannot mislabel a
  run; what stands is the half this was filed for — nothing in ADR-0011, in
  `spec/ids-and-statuses.md` §3.5a or in `scripts/lib/engagement.py`'s contract states that an
  ended engagement's verdict still carries the silent-round sentence, and the driver quotes it.
  After 4a59a9a the cost of that sentence disappearing is **a phrase of corroboration, not a
  wrong verdict**, which is why this is deferred rather than ranked with the toolkit defects.
  **Gate:** the next harness change window, with H-015 — either the contract gains the sentence
  (ADR-0011 §5 says what the count is *for*, not how long it lives) or the driver stops quoting
  what nothing promises. Ledger work only in this unit: no `harness/` file was touched.

## F-108 — `examples/toy-project`'s change-log rows were typed, not stamped

- **Classification:** artifact-defect, in this repository's own shipped example
- **Severity:** correctness of the record, low — and the evidence for F-084
- **Component:** `examples/toy-project/docs/`
- **Symptom:** the check F-084 asked for, run over the example, reports **six** rows in the
  imported run whose named skill was not executing on the named item at the row's stated time,
  and **two** rows whose `when` is out of order with their own version number:
  `docs/architecture/overview.md` has v5 at `00:05:00Z`, v4 at `01:36:00Z` and v3 at `01:50:00Z`,
  so the record says v3 happened after v5. Nine of the twenty-two rows in the example carry the
  timestamp `2026-08-17T00:05:00Z` exactly, across four documents and three skills, which is what
  a batch of doc writes stamped once by hand looks like. Four more rows are **builder-authored**
  — `ADR-0010-counting-lines-with-a-generator.md` was created whole by META-129 and
  `ADR-0005`'s v2 row by META-122 — with times typed to look plausible; `ADR-0005`'s header still
  said `updated-by: plan` for a row that says `review-close`, which is the one defect of the eight
  that was repaired (commit 8804bd7), because a builder correcting its own splice is not the same
  act as editing a run's evidence.
- **Why it is filed rather than fixed:** `examples/toy-project/README.md` says *"Nothing here was
  written by hand. Every file under `tracker/` and `docs/` was produced by a skill during the
  run"*, and for the six imported rows that is true. Rewriting their timestamps to satisfy a check
  written afterwards would falsify a record in order to make a gate green, which is the act this
  whole repository exists to make impossible. They stay as they are, and the rule that would
  condemn them is scoped so that it does not: `doc.changelog.no-execution` is asked only while the
  item a row names is not yet `done`, and every item in the example is closed.
- **Counterfactual:** none needed — this is not about the product the example builds. It is the
  same defect F-084 filed, at a rate of 6 in 22 rather than 1 in 46, in a run nobody was checking.
- **Direction:** two halves, neither urgent. The README's claim is worth narrowing to what is
  true — the tracker and the run's own documents were produced by skills; four ADR rows were
  spliced in later by builder units and say so. And the next re-import of a toy run, if there is
  one, is produced under a validator that now checks the rows while the items are open, so the
  defect cannot survive to the closed state again.
- **Provenance:** found by META-156's new `doc.changelog.*` rules on their first run over the
  example, 2026-09-10.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred — it joins F-068's release gate.**
  Re-confirmed as filed, and the second half of its Direction is already structural rather than
  pending: any re-import runs under `doc.changelog.no-execution`, which is asked while an item is
  open, so the defect cannot reach the closed state again. What is left is the first half — the
  README's *"Nothing here was written by hand"* narrowed to what is true — and that is prose in
  the shipped example, which is exactly F-068's job in exactly F-068's tree.
  **Gate:** the open-source release, with F-068. **Not fixed here on purpose**, and the reason is
  the finding's own: the six imported rows stay as they are, because rewriting a run's record to
  make a later check green is the act this repository exists to make impossible.

## F-109 — `next` still stops on a human answer that has already arrived: F-011's other half

- **Classification:** toolkit-defect
- **Severity:** correctness of the contract, high — one of the two rules the harness has a
  standing workaround for
- **Component:** `methodology/skills/next/process.md` step 3 (as shipped before META-162),
  `methodology/pipeline.yaml` `orchestrator.steps` 3
- **Symptom:** F-011 is recorded as **fixed** and half of it was. The fix landed in
  `answer-questions`, whose precondition 1 now names both answerable shapes — *"`addressed-to:
  architect` … or `addressed-to: human` **with `## Answer` filled in**"* — and whose own text
  states the defect in the past tense: *"`next` stops on any open human-addressed question, so
  an answered-but-unconsumed one stopped every subsequent turn forever (F-011)"*
  [src: methodology/skills/answer-questions/process.md]. `next` was never changed. Step 3 read
  `addressed-to: human` and `status: open` and nothing else, and a reply the stakeholder has
  written is both — so the orchestrator halts and prints back to the person the answer they just
  gave, and does so on every subsequent pass. The item cannot be reached at step 5 either: it
  carries an open blocking question, so it is not runnable.
- **The workaround, in the instrument:** the harness worker-turn prompt carries the sentence
  that gets past it — *"Run `answer-questions` on each such item **first**, before running
  `/next`"* [src: harness/prompts/worker-turn.md] — beside a note saying that amendment B was
  deleted because F-011 was fixed. One amendment was retired and the sentence that replaced it
  does the same job for the half that was not.
- **Counterfactual:** every engagement in which a human answers anything, unless the runner
  reaches past the orchestrator's algorithm. Nothing about any project's subject appears in that
  sentence.
- **Recurrence:** never observed as a stall, because no run has ever executed `next` without the
  prompt above.
- **Direction:** `next`'s dispatch condition becomes the same sentence as `answer-questions`'
  precondition 1 — a question is **answerable** when it is open and either addressed to the
  architect, or addressed to the human with a reply written. Two readings of one rule is one
  reading too many (F-045), and here the two readings sat in two files saying opposite things
  about the same question.
- **Provenance:** found by META-162 while deriving ADR-0012, by reading `next` against
  `answer-questions`' precondition. Filed as a new number rather than by reopening F-011, whose
  status text is accurate about the file it changed.
- **Status:** fixed by ADR-0012 (`meta/adr/ADR-0012-when-the-loop-stops-on-the-human.md` §1),
  as filed. `pipeline.yaml` step 3 and `next` step 3 dispatch `answer-questions` on any
  **answerable** question; `engagement.is_answerable()` is the predicate and
  `scripts/record-halt` reads it, so a pass whose only news is the stakeholder's own reply
  records no silent round. Both directions in `./scripts/check`'s *the halt is the last resort*
  step. The harness prompt's workaround is now unnecessary and was **not** removed — no harness
  run is in flight, and that is a harness change (ADR-0012 §6).

## F-110 — a question **we** file resets the silence clock, which the mechanism's own docstring says it must not

- **Classification:** toolkit-defect
- **Severity:** correctness of a derived ending, medium — E4 by silence can be made unreachable
  by the pipeline's own asking
- **Component:** `scripts/lib/engagement.py` `inbound_rendering()`
- **Symptom:** the inbound digest is taken over a rendering that contains one line per
  human-addressed question **whatever its status**, plus one per request. Filing a new question
  adds a line, so the digest changes, so the trailing run restarts and the silent-round count
  resets to 1. The function's own docstring says the opposite in the same file: *"A question
  *we* file changes no line here, which is why our own asking cannot reset the clock"*
  [src: scripts/lib/engagement.py], and so does `pipeline.yaml`'s `termination.silence` block
  (*"Nothing a skill writes is inbound"*) and ADR-0011 §1.3's table, whose row reads **A new
  question filed by us — resets? no**, with the reason: *"a pipeline whose own asking reset the
  clock could never reach the threshold in any engagement that keeps generating questions, which
  is every engagement"* [src: meta/adr/ADR-0011-stakeholder-silence-and-abandonment.md].
- **Proved by execution** (META-162, over a copy of `fixtures/abandoned-engagement/right`):
  `inbound_digest` for `EP-003` is `ee47bf97`; adding one new `addressed-to: human` question to
  `WI-0008` with an empty `## Answer` and touching nothing else moves it to `edd86dbe`.
- **Counterfactual:** any engagement whose stakeholder stops answering while the pipeline still
  has work that files questions. It is worse after ADR-0012, not better: the loop now dispatches
  work between halts rather than stopping at the first one, so there is more opportunity for a
  skill to file a question between two halts, and every such filing restarts the count.
- **Recurrence:** never observed in a live run — no run has produced an E4 by silence at all
  (META-153b). The three banked `abandoned-engagement` fixtures do not exercise it, because
  their digests are computed over static trees.
- **Direction:** the rendering should carry only what a **reply** looks like — for each
  human-addressed question that has one, its ID, `status`, `answered-at` and the digest of its
  `## Answer`; plus the request lines, which are the stakeholder's channel and are theirs to
  open. A question filed and never answered then contributes nothing, which is what all three
  statements of the rule already claim. Requires the three `abandoned-engagement` waiting logs'
  digests to be recomputed in the same change, since `./scripts/check` recomputes and compares
  them.
- **Provenance:** found by META-162 while checking ADR-0011 §1.3's table against the code, as
  part of ADR-0012's reconciliation (§3, check 4). Deliberately **not fixed there**: it is a
  different rule from the one that ADR was deriving, its fix moves banked fixture digests, and
  filing it is what this ledger is for.
- **Status:** open
- **Status update 2026-09-10 (META-163): open, deferred behind a named gate.** Re-confirmed
  unchanged, and re-read against ADR-0012 as filed: the finding is right that the reordering makes
  it worse rather than better, because more work now happens between halts and every question
  filed in between restarts the count. Three statements of the rule — the docstring,
  `pipeline.yaml`'s `termination.silence` block and ADR-0011 §1.3's table — say the opposite of
  what the code does, and only the code decides.
  **Not fixed here, for the reason META-162 gave when it declined to fix it there:** the fix moves
  the trailing digests of all three `abandoned-engagement` waiting logs, which `./scripts/check`
  **recomputes and compares**, so the change is a rewrite of `inbound_rendering()` plus three
  recomputed fixtures plus the both-ways step that proves the new rendering ignores our own asking.
  **Gate:** one unit on `scripts/lib/engagement.py` that changes the rendering to carry only what
  a reply looks like and recomputes the three fixture digests in the same commit — **F-107 rides
  in that unit**, same file, and it is cheaper together than twice.

## F-111 — a fresh install's contents are not a function of what git tracks

- **Classification:** toolkit-defect
- **Severity:** packaging, low — nothing a consumer ships is wrong; what is wrong is that two
  machines installing the same commit do not get the same tree
- **Component:** `adapters/claude-code/install.py` (`copy_tree`, and the three calls in
  `install()`), `adapters/claude-code/hooks/`, `adapters/claude-code/dist/agile-skills/scripts/lib/`
- **Symptom:** `copy_tree` is `shutil.copytree(source, destination)` with no `ignore`, so it
  copies whatever is in the source directory, tracked or not. Two of the directories it is pointed
  at accumulate a **git-ignored** `__pycache__/` whenever this repository's own gate runs —
  `adapters/claude-code/hooks/` (from `test_guard.py`) and
  `adapters/claude-code/dist/agile-skills/scripts/lib/` (from any script that imports `lib`).
  Established by execution, not by reading: `python3 adapters/claude-code/install.py .` into a
  fresh empty `git init` directory produces **13** `.pyc` files under `.claude/agile-skills/`,
  every one of them stamped `cpython-312` by the interpreter that last ran the gate on the
  builder's machine. `git ls-files adapters/claude-code/hooks/` lists exactly two files and
  neither is one of them; `git check-ignore -v adapters/claude-code/hooks/__pycache__` answers
  `.gitignore:1:__pycache__/`; `git ls-files adapters/claude-code | grep -c pycache` is `0`.
- **What is NOT true of it, checked rather than repeated:** the reading this was first written
  down with — that `--uninstall`'s *"remove exactly what was installed"* therefore varies by
  machine — does not survive the code. `uninstall()` removes `SHARED_DIR` **wholesale** with
  `shutil.rmtree`, so the stray files go with it whatever they are. The claim that holds is the
  narrower one: **a fresh install's contents depend on untracked local state**, so the install is
  not hermetic with respect to what git tracks, and a file count or a manifest taken on one
  machine is not the file count on another.
- **Counterfactual:** every install on every machine, with no project's subject matter involved.
  A consumer's own `.gitignore` covers `__pycache__/` (F-003's fix, at `workspace-init` time), so
  what git tracks in a provisioned project is unaffected — which is exactly why nothing has ever
  reported it.
- **Recurrence:** reproducible on demand; observed by META-164 during staging verification and
  again here. It also quietly weakens that unit's rule 3 — *the install matches what the repo
  renders* — which passes only because `hooks/` is excused from the `diff -r` wholesale.
- **Direction:** one argument: `copy_tree` passes
  `ignore=shutil.ignore_patterns("__pycache__", "*.py[cod]")`. The stronger version, if the
  installer is ever run from inside a checkout, is to refuse to copy a path git ignores and say
  so. Either way the proof is a step that installs into a temporary directory and asserts the
  result contains no path this repository ignores — an assertion nothing makes today.
- **Provenance:** journalled by META-164 (commit 8e61fdb) as *"the one real finding"* of the
  staging verification and deliberately left unfiled pending triage. Verified independently here
  by execution (META-163) and found **wider than reported**: 13 files from two directories, not
  one file from one — the `dist/agile-skills/scripts/lib/__pycache__` half was not in that
  reading, and it is the half that ships the analyzer's own bytecode rather than a hook's.
- **Status:** open, **deferred behind a named gate.** The fix is one keyword argument and the
  finding is two hours old, which is precisely why it is not being taken in a triage unit:
  `adapters/` is not adjacent to the ledger, and a packaging change with no assertion behind it is
  how a packaging break ships. **Gate:** the next unit that opens `adapters/claude-code/install.py`,
  or the pre-release packaging pass, whichever comes first — with the temp-directory assertion in
  the same change, because without it the next `copy_tree` source reintroduces this silently.

## H-021 — a re-provision overwrites the project's `.gitignore`, and two programs disagree about who owns it

- **Classification:** harness-defect
- **Severity:** harness, low — it converges, and on the way it discards whatever the project put
  there
- **Component:** `harness/provision.py` (step 2, `GITIGNORE`, `write_file`), `scripts/workspace-init`
  (`GITIGNORE_LINES`, step 4)
- **Symptom:** `provision.py` step 2 **writes** its own five-line `.gitignore` — `write_file` is
  a whole-file write, not an append — and step 4 then runs `workspace-init`, which **appends** the
  lines of its own three that the file does not already contain. The two disagree about spelling
  (`*.pyc` versus `*.py[cod]`; `/HARNESS-STATUS.md` versus `HARNESS-STATUS.md`), so the file after
  step 4 can never equal what step 2 writes, and every re-provision rewrites it, prints
  `wrote .gitignore`, and has step 4 put the two lines straight back. The provisioned project ends
  up carrying both spellings of both rules.
  Proved by execution, on a throwaway project outside this repository: three provisions of one
  directory. The end state converges — `md5sum` is `c2e9596451f95d2247ac7f5378ad0e3c` after the
  first run and after the second — and `wrote .gitignore` is printed on **every** run including
  the one that reports *"nothing to commit (already provisioned)"*. Then the half that is not
  cosmetic: a line added between two provisions (`/build/`) is **absent** after the next one.
  Step 2 writes, so anything the project added is gone, and only step 4's append puts back the
  three lines `workspace-init` happens to know about.
- **Counterfactual:** any re-provision of an existing project, which is the documented idempotent
  path. Nothing about an iteration's subject is involved.
- **Recurrence:** every re-provision since the two programs both learned to write that file. Never
  harmful in a run so far, because no run has edited `.gitignore` — which is luck about what the
  worker chose to do, not a property of the tool.
- **Consequence worth stating separately:** a provisioned project's `.gitignore` is not the
  project's to edit, and the toolkit's own program is the one that gets this right —
  `workspace-init` appends and never clobbers (F-003's fix), and the harness's provisioner does
  the opposite one step earlier. The ordering is load-bearing and documented nowhere: only step 4
  following step 2 on every run keeps the disagreement invisible.
- **Direction:** step 2 appends the lines it wants rather than writing the file, using
  `workspace-init`'s own idiom, and the two programs agree on **one** spelling per rule so a
  provisioned project stops carrying two of each.
- **Provenance:** observed by META-164 (commit 8e61fdb) and explicitly judged *not a defect* on
  the ground that it converges; re-verified by execution here (META-163) and filed, because the
  destructive half — a line the project added, silently discarded — was not in that reading, and
  convergence of the parts a tool knows about is not convergence of the file.
- **Status:** open, **deferred behind H-015's harness gate** — the next harness change window, a
  unit that opens `harness/` while no run is in flight and no evidence is being banked. Ledger
  work only in this unit: no `harness/` file was touched.

## F-112 — the ledger's own status cannot be read by the obvious command

- **Classification:** record-defect, in this repository's own findings ledger
- **Severity:** correctness of the record, medium — the failure mode is a resolved finding
  re-worked, or an open one never examined, and both cost a unit
- **Component:** `meta/findings/FINDINGS.md` (its header convention), `scripts/check`
- **Symptom:** this file is append-only by rule, so a resolved finding keeps its original
  `Status:` line and the new one is appended below it. Nothing said so, and nothing checked
  anything about a status, so the obvious reading is wrong in three separate ways. Measured at
  commit 8e61fdb, the tree this was found on:
  **(1)** `grep -E 'Status:\*{0,2} \*{0,2}open'` names **24** entries, and **13 of them** —
  F-061, F-080, F-085, F-086, F-087, F-091, F-092, F-093, F-094, F-095, F-096, F-099 and H-020 —
  carry a **later** status saying otherwise. A 54% false-positive rate on the command a reader
  reaches for first.
  **(2)** It is wrong in the other direction too. F-076 was fixed by META-149 and its *first*
  status reads `deferred`, so the same grep does not name it at all; a reader who trusts the grep
  to enumerate the open backlog gets a list that is both padded and short.
  **(3)** Two status *forms* exist. F-061's resolving status is a `### Status update ...`
  **heading**, not a bullet — a reader matching the bullet form (which is every other entry's
  form) reports F-061 as `open (observation)` when META-159 closed it. And **three** entries
  (H-001, F-042, F-071) carried **no** status line at all, being tombstones and a merge pointer,
  which is indistinguishable to any mechanical reader from an entry nobody has examined.
- **Counterfactual:** none needed — this is not about a consumer's project, it is about the file
  that decides what this project works on next. It is F-024's class in the ledger's own margin: a
  record whose form nobody verifies produces the appearance of a reading.
- **Recurrence:** it has already cost real work. META-149 recorded F-053 as *still deferred*, and
  META-156 fixed it three units later without noticing, so F-043 and F-053 sat at `deferred`
  through four more units while being fixed. F-010's gate has been met since 2026-08-30 and its
  status still read `deferred (gated)` eleven days later. Both were found by reading last statuses
  one entry at a time, which is the reading this finding says nobody should have to do by hand.
- **Direction:** say the rule where the file is opened, and make the machine hold the part it can.
  The convention paragraph states that the last status line is the current one and that two forms
  exist; `./scripts/check` gains a step that requires **every** `## F-###` / `## H-###` entry to
  carry at least one status line, so a tombstone that says nothing and a finding nobody triaged
  stop looking alike. What the step deliberately does **not** do is classify the words of a free
  prose status — *"still deferred, and consumed as input"* is a legitimate status and a closed
  vocabulary would either reject it or reduce it to a wrong label.
- **Provenance:** found by the orchestrator while preparing META-163 and handed over as a trap to
  avoid; the three-way measurement above is META-163's, and it is wider than the trap as reported
  — the hand-listed set of stale entries was 12 and missed F-057, F-058, F-061 and H-020, and it
  named F-076 as showing `open` when it shows `deferred`. Verifying it beat repeating it, which
  is META-153b's lesson in a third place.
- **Status:** **fixed** — both halves, in this unit, because this finding's subject *is* this
  unit. The header of this file now states how to read a status. `./scripts/check` step **17c,
  every finding's status is readable**, requires each entry to carry one and reports the tally in
  its own label; it is proved non-vacuous inside the step, against a synthetic two-entry ledger
  whose first entry has no status, so a reader that stopped seeing a missing status would fail the
  step rather than pass it silently. The three status-less entries now carry one, saying what they
  are.

## F-113 — A history row that mentions a citation form is read as a citation and refused
- Severity: correctness of enforcement, medium-high — F-075's pathology (mention read as
  use) on a new record surface, this time with a terminal cost
- Component: scripts/validate-workspace (citation scraping over history rows),
  spec/doc-header.md (the forms table), authoring guidance
- Symptom: iteration 5 stopped terminal at turn 11 on exactly one error: a history row's
  reason prose named the form `path:line` while explaining a citation, and the gate
  scraped the mention as a citation instance — "'path:line' is not a citation form this
  gate can check". The worker's actual citations all resolve, including twelve
  [src: .claude/agile-skills/...] toolkit paths ("Both citations resolve to files in the
  workspace", Q-004:215); the only refusal in the engagement was prose ABOUT citations.
  The escape — backticks mark mention, not use — exists but is documented only in a
  validator source comment (there cited to F-037), nowhere a writer reads. F-075 was this
  defect's first appearance (a worker rewording prose to satisfy the scraper); this is
  its second, and it ended the run.
- Evidence: meta/harness/evidence/iteration-5-envel-abandoned/ — run/state.json
  (validator-failed, turn 11, "1 error"); validate-workspace re-run on the banked
  workspace (the single history.md:14 error, verbatim in the ops capture);
  tracker/items/WI-0002/questions/Q-004.md:215.
- Direction: two halves. The scraper distinguishes mention from use by the documented
  convention (backticked = mention) uniformly across every record surface it scans, with
  a must-fail fixture per surface; and the convention itself moves out of the source
  comment into the forms table and the authoring guidance (F-114's placement fix carries
  it). Cross-reference F-075; consider them one class when fixing.
- Status: open
- Status update 2026-09-11 (META-167, META-168): **fixed**, in two units, and F-075 is the same
  class fixed with it — one defect, one vocabulary, two directions, closed together.
  META-167 (commit `cd00504`) supplied the first half: `citations_in()` and `carries_citation()`
  in `scripts/lib/claims.py` are the one reader that decides mention-versus-use, and every
  surface that scrapes the vocabulary now calls one of them, so a backticked marker is a mention
  on all six of them rather than on whichever ones had remembered to mask.
  META-168 supplied the second half, which the mask cannot reach: the row that ended the run was
  **bare**, not backticked, and a writer naming a form in prose is entitled to. So severity now
  follows knowledge. `CitationResolver` returns a `Problem` carrying its kind, and the kind
  decides the code and the level in exactly one place: a body matching a known form and failing
  to resolve stays an ERROR under `claim.citation.unresolved` / `retro.citation.unresolved`,
  because the gate looked; a body matching no form is a WARNING under
  `claim.citation.unrecognised` / `retro.citation.unrecognised`, because the gate looked at
  nothing and cannot tell a mention from a typo — and reporting a verdict it does not hold is
  the over-claiming this repository is built to refuse. Warnings do not touch an exit code, so
  the run would not have stopped. The message teaches both escapes and points at the forms
  table, and the convention now lives in `spec/doc-header.md` §4a where a writer reads it, with
  its cost said plainly: a typo'd body matching no form (`WI-007`, three digits) warns where it
  used to fail. The regression anchor is the banked evidence itself — `scripts/check` copies
  `meta/harness/evidence/iteration-5-envel-abandoned/` and asserts that
  `tracker/items/WI-0002/history.md:14` produces no error while a citation planted in the same
  row that matches a form and resolves to nothing still does. F-114's placement half is
  separate and still open; the toolkit-path question (`.claude/agile-skills/...`) is untouched
  here and is F-114's, not this one's.

## F-114 — Citation forms are enforced at validation but may not be surfaced at authoring
- Severity: UX/methodology (the general case F-113 is one instance of)
- Component: methodology skill contracts (answer-questions, implement, plan),
  spec/doc-header.md
- Symptom: the worker learned the citation-resolution rule by tripping it at
  validate-workspace, having authored in good faith. Whether the `path:line` /
  workspace-relative restriction is stated anywhere the authoring worker reads, versus
  living only in the validator's spec, is the fix boundary: "the rule exists but not
  where the writer looks" (surface it) differs from "the rule is validation-only"
  (author-time check). The grep was run over the abandoned workspace's installed skills
  and the answer is mixed: resolvability IS stated at authoring, but well-formedness is
  validation-only. The claim-kinds table tells the worker, verbatim —
  "| cited fact | an absolute about something named as code — an identifier, a call, a
  path | a citation, written `[src: ...]`, that resolves |" — and `implement` gives one
  concrete form, `[src: <ITEM>/Q-nnn>]`. No skill states which forms exist or what makes
  one legal: grep -rniE "workspace-relative|citation forms|forms table" over all nine
  installed skills returns nothing, exit 1. The forms table lives only at
  spec/doc-header.md:271 and no skill names it — `verify`'s four pointers into that file
  name §5 and §4a. So the boundary is "surface it" for the obligation and
  "validation-only" for the grammar.
- Evidence: meta/harness/evidence/iteration-5-envel-abandoned/ — the WI-0002 authoring
  trail; the installed-skill grep quoted in the Symptom above, run over
  .claude/skills/ in the abandoned workspace.
- Direction: The forms table should additionally state whether installed-toolkit paths
  ([src: .claude/agile-skills/...]) are a legal form: twelve resolve in the abandoned
  workspace today by bare existence, with nothing pinning the toolkit version they
  referenced — legal-and-pinned, or illegal-and-quoted, but not accidental.
- Status: open
- **Status update 2026-09-11 (META-169): the Direction half is decided and implemented; the
  placement half is still open.** The ruling is **illegal-as-a-path, legal-as-a-quote**, derived
  in `meta/adr/ADR-0013-a-toolkit-source-is-quoted-not-pointed-at.md` and written into
  `spec/doc-header.md` §4a's citation forms table (revision 11).
  **Refused.** A citation body resolving inside a directory the record walk prunes is an ERROR,
  `claim.citation.outside-the-record`. The test is generalised rather than hand-written for the
  toolkit path: `claims.PRUNED_DIRS` holds the four directories once and is read by
  `validate-workspace.check_claim_citations`, by `lint-claims.all_markdown` and by
  `CitationResolver._resolve`, so the rule and the exclusion cannot drift — they were already two
  hand-written copies before this change. An ERROR and not META-168's warning because the gate
  knows both what is wrong and what to write instead; there is no mention-vs-typo ambiguity here.
  **Replaced.** `[src: toolkit: <document> <section> "<quoted words>"]`, resolving when the shape
  is complete. The document is never looked up (the toolkit upgrades underneath a standing record,
  and §4a forbids retroactive invalidation), the section may be a `§`, a heading or an identifier,
  and the quote is mandatory, non-empty, and may contain neither `]` nor `;`. Unlike `run:`, it
  does not swallow the rest of the marker. What this does **not** decide is said in the table and
  in the ADR's consequences: the gate cannot tell whether the toolkit really says those words, only
  that the citation carries enough for a reader to check it — which is strictly more than the path
  form carried, since `os.path.exists` under a pruned directory checked the writer's own
  installation and nothing else.
  **Evidence.** All twelve banked citations fail the moment the record leaves the machine
  (`python3 scripts/validate-workspace meta/harness/evidence/iteration-5-envel-abandoned` reports
  twelve `claim.citation.unresolved`), and one of them — `claims.py:148` — was true at `181e69d`
  and is false two toolkit commits later, with F-077's bound unavailable because it would be a
  bound on a file outside the record. The twelve are **not** repaired: `meta/harness/evidence/` is
  read-only history and §4a's non-retroactivity rule covers them.
  **Fixtures.** `fixtures/broken-workspace` carries both refusals (the pruned-path one is the sole
  source of its code; the quoteless `toolkit:` one is pinned by count in `check_claims`), 109 codes
  → 110; `fixtures/sourced-claims` carries two well-formed `toolkit:` citations, one of them with
  two sources in a single marker, and still lints clean. 33 new `selftest.py` cases, 386 → 419.
  **Still open: the placement half.** Whether the authoring skills state or point at the forms
  table — the *"the rule exists but not where the writer looks"* half of this finding's own fix
  boundary — is untouched here and is META-170's job. F-114 is **not** fully resolved.

- **Status update 2026-09-11 (META-170): the placement half is done; with META-169's Direction
  half this finding is fixed in both halves.** The grammar is now readable where the citation is
  written. Which skills owe one is **derived** from the contracts rather than listed: an
  obligation statement — a quality gate's `description` or `manual_check`, or an exit criterion —
  that names a citation. Seven do: `answer-questions`, `implement`, `intake`, `plan`, `refine`,
  `retro`, `review-close`; `next` and `verify` oblige none. The rule asks whether an obligation
  names a citation at all and not whether it also says *resolves*, because `refine`'s R11 tells a
  worker to carry a measurement as a command-outcome citation (F-089) without using the word, and
  a writer of that citation needs the grammar exactly as much as any other.
  **What was added.** Five lines in each procedure, naming `spec/doc-header.md` §4a, *Citation
  forms* and flagging the three traps a gate would otherwise teach: a path citation is
  workspace-relative and never points into the installed toolkit (ADR-0013's quoted form instead),
  a marker inside backticks or a fence is naming a form rather than using one, and a marker
  matching no form at all warns rather than fails (META-168). The table is **not** copied: §4a
  stays the single source, which is the two-readers-one-vocabulary defect this ledger keeps
  finding, in prose. `review-close` carries the one-sentence form because its rendered body sits
  exactly on the runtime's 500-line ceiling; two of its paragraphs were rewrapped, word for word,
  to pay for the two lines it added.
  **The pointer cannot rot.** `scripts/check` step 15d derives the same set the same way and
  requires each procedure to name the table, so a contract that gains the obligation tomorrow
  fails until its procedure is told; it also requires `spec/doc-header.md` to still have a
  `### Citation forms` heading, which is the other direction the pointer can break. An **empty
  derived set is a failure**, not a pass — that is how a step of this shape rots into checking
  nothing. Both breaks were run: the pointer removed from `intake` fails naming that skill, and a
  derivation matching nothing fails with `(0 skills)`.
  **Evidence.** F-114's own grep over the installed skills —
  `grep -rniE "workspace-relative|citation forms|forms table" adapters/claude-code/dist/skills/` —
  returned nothing and exit 1 in the abandoned workspace; it now returns 13 lines across all seven
  skills, exit 0. 47 check steps, 110 fixture codes, 419 selftest cases.

## H-022 — Should a fixable citation error halt the whole engagement? (question-shaped)
- Severity: harness / consumer-modeling, genuinely open
- Component: scripts/validate-workspace (exit semantics), harness/run_iteration.py
  (validator-failed stop), the pipeline's mid-work validation contract
- Symptom: A single fixable record defect — one prose mention scraped as a citation
  instance (F-113) — halted the whole engagement at turn 11. A real consumer would fix
  the line and continue. Two readings both plausible and possibly both true: correct-for-the-harness (fail hard,
  surface the defect for study — which is exactly what happened, and it worked) and
  wrong-for-consumer-modeling (a real engagement wouldn't die of it). Do not resolve
  now; the answer likely interacts with F-113's fix (once toolkit-source citations are
  legal, this specific trip disappears, but the halt-vs-continue question outlives it).
- Evidence: meta/harness/evidence/iteration-5-envel-abandoned/run/state.json
  (stopped/validator-failed/turn 11).
- Status: open (question)

### Correction (2026-09-11): the Symptom's closing parenthesis presupposed toolkit-source citations are currently illegal; twelve resolve in the abandoned workspace today (see F-114's Direction), and the halt-vs-continue question stands independently of F-113's fix.

---

### Note (2026-09-10) — held-out calibration still owed
The abandoned run produced no ending and no retro (stopped turn 11, before any dispatch);
ROADMAP §4 step 1's held-out recall number remains unmeasured. Restored by a fresh envel
re-run after F-113's fix — the re-run is builder-6's regression gate, and it re-serves as
the calibration engagement on an uncontaminated project.
