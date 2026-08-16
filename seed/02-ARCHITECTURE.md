# 02 — Architecture

Binding structure. Where a detail is unspecified, decide, record an ADR in `meta/adr/`, and keep the specs (`spec/`) as the single source of truth.

## 1. This repo's layout

```
agile-skills/
├── methodology/                 # runtime-neutral — the real IP
│   ├── skills/
│   │   ├── next/                # orchestrator
│   │   ├── intake/
│   │   ├── refine/
│   │   ├── plan/
│   │   ├── implement/
│   │   ├── verify/
│   │   ├── review-close/
│   │   └── answer-questions/
│   │       ├── skill.yaml       # contract (schema below)
│   │       └── process.md       # step-by-step procedure
│   └── pipeline.yaml            # skill graph, statuses, transitions
├── spec/                        # formal schemas: work item, journal, question,
│   │                            #   doc header, ID & status rules, DoR/DoD
├── adapters/
│   ├── README.md                # adapter contract (see §6)
│   └── claude-code/             # renderer + installer
├── scripts/                     # validate-workspace, render, lint-skills, board-gen
├── examples/toy-project/        # completed reference run (R7)
├── meta/                        # this build's own paper trail (§7)
├── USAGE.md
└── CONSUMER-PROMPT.md
```

## 2. Skill contract — `skill.yaml`

Every skill declares (finalize exact schema in `spec/skill-contract.md`):

```yaml
name: implement
version: 0.1.0
persona: developer            # voice + judgment style used in journals
purpose: one-sentence statement
triggers:                     # tracker states this skill acts on
  - item.status == "planned"
inputs:                       # artifacts that MUST exist and be read
  - tracker/items/{id}/item.md
  - tracker/items/{id}/artifacts/plan.md
  - docs/architecture/**
outputs:                      # artifacts this skill MUST produce/update
  - code on branch wi/{id}
  - tracker/items/{id}/artifacts/impl-report.md
  - journal + history entries
quality_gates:                # executable where possible; each: name, command, expectation
  - name: tests-pass
    command: "<project test command>"
    expect: exit 0
human_interaction: none | direct | via-questions
escalation:
  question: file questions/Q-###.md addressed to architect; set item awaiting-answer
  defect-found: file BUG item linked to this item
exit_criteria:                # checklist that must be all-true to transition
next_status: verifying
failure_status: blocked
```

`process.md` is the procedure a worker follows: numbered steps, what to read, what to think about, what to write, exactly what to journal, and the self-check before declaring the exit criteria met. Written for a competent agent with **zero context** beyond the workspace — never assume conversational memory.

## 3. Workspace model (consumer project)

Specify fully in `spec/`; enforce with `scripts/validate-workspace`.

**IDs**: `EP-###` epics, `WI-####` work items, `BUG-####` bugs, `Q-###` questions (scoped per item), `ADR-####` architecture decisions. Sequential, zero-padded, never reused.

**Work item statuses & flow** (pipeline.yaml is authoritative):

```
draft → ready → planned → in-progress → verifying → in-review → done
   (refine)  (plan)   (implement)   (verify)  (review-close)
plus: awaiting-answer (blocking question open), blocked (documented impasse)
```

Only skills change status; every change appends to the item's history with actor-skill, timestamp, and reason.

**Per-item directory**:

```
tracker/items/WI-0007/
├── item.md            # frontmatter: id, type, title, status, epic, priority,
│                      #   created, updated, branch; body: story, acceptance criteria
├── journal.md         # append-only, one entry per skill execution (spec'd format)
├── history.md         # append-only status transitions
├── questions/Q-001.md
└── artifacts/         # refinement-qa.md, plan.md, adr links, impl-report.md,
                       #   verify-report.md, review.md
```

**Docs** (`docs/product/`, `docs/architecture/` incl. `adr/`, `docs/process/`): each file has a frontmatter version header + human-readable change log section; content changes bump version and add a log line naming the skill/item that caused it.

## 4. Orchestrator (`next`)

Algorithm, and nothing more: (1) validate workspace; (2) if any question addressed-to human is open → surface it and stop; (3) else if questions addressed-to architect are open → dispatch `answer-questions`; (4) else pick the highest-priority item whose status has a mapped skill in pipeline.yaml → dispatch it; (5) if nothing runnable → report board summary and stop. Deterministic tie-breaking (priority, then oldest). The consumer session loops `next` until it stops.

## 5. Question protocol

`questions/Q-###.md`: frontmatter (id, from-skill, item, addressed-to: architect|human, blocking, status: open|answered, created, answered-at, answered-by), body sections: Context / Question / Options considered / Answer / Consequences (which docs, plans, or items were updated as a result). Answers must be propagated into the authoritative artifacts — downstream skills re-read artifacts, never the Q&A chat.

## 6. Adapter contract & Claude Code renderer

`adapters/README.md` defines what any adapter maps: (a) trigger the right skill from tracker state, (b) surface interactive questions to the human, (c) execute quality gates as real commands, (d) install/uninstall rendered skills into a project, (e) optional: isolated subagent execution. The renderer consumes only `skill.yaml` + `process.md` + `spec/` — if a renderer needs more, the methodology is deficient; fix it there.

Claude Code renderer: generate one skill folder per methodology skill — SKILL.md whose frontmatter description enumerates concrete trigger situations, whose body is the process with the contract summary, and whose bundled `references/` carry the full contract, checklists, and schemas (progressive disclosure). Gate commands ship as executable scripts. Confirm exact current format against official Claude Code docs at build time (see PROMPT.md rule 6).

## 7. `meta/` — the builder's own trail

`meta/plan.md` (build task list, maintained), `meta/journal.md` (append-only), `meta/adr/ADR-####.md` (every non-trivial decision), `meta/BLOCKERS.md`, `meta/FINAL-REPORT.md` (at the end). Build commits reference `META-###` task IDs. This is deliberately a lightweight version of the methodology itself — it will later serve as evidence of what the full pipeline should feel like.
