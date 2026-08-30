# Builder session four — mission kickoff prompt: the retro skill

Location when adopted: meta/BUILDER-4-PROMPT.md. Paste everything below the line into Claude
Code at the repository root.

---

You are builder session four of **agile-skills** — the first gated-track session. The kernel
is proven and stamped (meta/ROADMAP.md §2 stamp, 2026-08-30; confirmation run 4c at
meta/harness/evidence/iteration-4c/). Your mission is the roadmap's first unlocked item: the
**retro skill** — the skill that reads a completed engagement's record and proposes findings
and contract changes, automating the review craft that produced this repo's own ledger. Plus
one adjacent refactor and one small fix, below.

Read first: meta/ROADMAP.md (§2 stamp and §3), meta/findings/FINDINGS.md — with special
attention to how the filed findings are WRITTEN (they are your quality corpus: symptom with
evidence pointers, component, class-not-specimen direction, honest severity), FINAL-REPORT-3
§6's qualification 3, and at least two banked evidence sets end to end
(meta/harness/evidence/iteration-2/ and iteration-3/ recommended) as a reader, before
designing the reader. All standing discipline applies unchanged; META-### continues; banked
evidence and filed findings text remain read-only.

## Cluster 1 — the retro skill (the centerpiece)

Design it with an ADR first. Binding constraints; everything else is yours to derive:

- **Runtime-neutral, like every skill**: methodology/skills/retro/ (skill.yaml + process.md),
  rendered by the adapter, versioned, contracted. Persona: your call (a process analyst who
  was not on the team is the spirit).
- **Input is the workspace record only** — tracker, docs, journals, questions, history, git
  log. A real consumer has no SIM-LOG and no harness; the retro must work from what any
  engagement leaves behind. It runs read-only over the record it studies: a retro that edits
  the engagement it audits is a refused design.
- **Trigger**: after an engagement ends (any ending — E1..E4), dispatched by `next` per
  pipeline.yaml, before the engagement is archived as fully closed. The stakeholder is NOT
  gated on it (their engagement ended at sign-off); the retro is the team studying itself.
- **Two output audiences, cleanly separated** in a spec'd retro report
  (tracker/items/EP-###/artifacts/retro.md or a location you derive):
  1. **Engagement-local retrospective** — what this record shows about how the work went:
     where a skill misled itself, where questions were late or misrouted, where gates passed
     on discipline rather than contract, where the trail failed to explain itself. Every
     observation cites its evidence (file, entry, line) — an uncited observation is a
     refused write, by the project's own rules.
  2. **Exportable toolkit-finding proposals** — candidate findings in the house ledger
     format, explicitly marked PROPOSED, with evidence pointers into the engagement's own
     record, for a human to triage upstream. This is the community feedback engine for the
     open-source era: every consumer's retro can generate upstream findings. Spec the
     proposal format (spec/retro.md) including the required distinction: toolkit defect vs.
     this-project circumstance vs. observation — misclassifying "this project was hard" as
     "the skill is broken" is the failure mode to design against.
- **Calibration is the corpus**: process.md should direct the analyst to the finding-quality
  bar by construction (evidence-first, class over specimen, severity honest, positives
  recorded too — the ledger's "Positive record" sections are part of the craft).

## Cluster 2 — the record-model library (F-069/F-073's class, FINAL-REPORT-3 qualification 3)

The named residual: rules about a record's structure keep being implemented against lines or
states, twice wrong in one session. Extract a shared record model — one library
(scripts/lib/) that parses the workspace's record types (journal entries, history rows,
question files, item frontmatter, findings entries) into structures, which every lint and
check then consumes; structure rules stop being reimplemented per script. Migrate the
existing lints to it (behavior-identical, proven by the existing fixture suite staying
green), and note that the retro skill's reader should consume the same model — one parser,
every reader. This is refactor-with-a-safety-net work: the 82 broken-workspace codes and 28
gate steps are the net; no behavior changes ride along.

## Cluster 3 — small fixes

H-017 (driver stamps/validates the turn number in HARNESS-STATUS; board-gen no-op notice to
stdout), the stale max-turns: 24 in iteration-4-recall.json, and the inert `*.1` run
directories' class if cheap (a terminal marker or a driver startup sweep — else file the
H-finding properly and defer). Anything new you find: file, don't fix silently.

## Acceptance

- [ ] ./scripts/check green; new fixtures for the record-model migration (existing codes
      unchanged is the proof) and for the retro report/proposal formats (lint-retro or
      equivalent — a retro whose observations lack citations must fail).
- [ ] **The ground-truth test**: run the rendered retro skill, via context-free subagents,
      against at least TWO banked engagements (iteration-2 and iteration-3 evidence, copied
      to scratch as read-only inputs). Before running, write down (in the unit's journal)
      the honest ground-truth subset: which filed findings from those iterations are
      workspace-visible (discoverable from the record alone — many H-findings and
      sim-side observations are not; exclude them explicitly). The test: the retro's
      proposals rediscover a meaningful fraction of that subset (state the fraction and
      judge it honestly — this is a calibration reading, not a pass/fail gate) and produce
      low noise (proposals that are neither ground-truth matches nor defensible new
      observations get counted and confessed). Iteration-3's silent-harmonization trail is
      the marquee case: a retro that reads that record and does not surface the
      contradiction's handling has failed the concept.
- [ ] **The live test**: dispatch retro through the pipeline on a real ended engagement —
      copy recall-4c's workspace to scratch, extend pipeline.yaml so `next` dispatches
      retro post-ending, run it via the rendered skills, and show the retro report filing
      correctly with the engagement then archiving as closed.
- [ ] Findings passes over both tests; F-###/H-### continue; statuses current.
- [ ] meta/FINAL-REPORT-4.md: the design decisions, the ground-truth numbers with your
      honest read of them, what the record-model migration changed, versions bumped, and
      the recommended next step for the retro (e.g., run it inside the next real iteration,
      or calibration work first).

Budget guidance: cluster 1's design quality outranks cluster 2's completion; cluster 3
yields first. The ground-truth test is the session's soul — do not weaken the ground-truth
subset to flatter the numbers; a retro that finds 40% honestly is worth more than one that
finds 90% of a curated list.

Begin: read the ledger as a corpus, the evidence as a reader, ADR the design, plan units,
checkpoint, proceed.
