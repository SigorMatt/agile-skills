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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
- Status: open

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
