# Final report — the agile-skills builder session

Written last, per `PROMPT.md`. What was built, what was decided, what is weak, and what the next
iteration should do.

The acceptance checklist and its evidence are in [`plan.md`](plan.md); the unit-by-unit record is
in [`journal.md`](journal.md). This file is the summary a person should read first.

---

## 1. What was built

A methodology, a way to install it, and a proof that it works.

| Layer | What exists |
|-------|-------------|
| `methodology/` | 8 skills — `intake`, `refine`, `plan`, `implement`, `verify`, `review-close`, `answer-questions`, `next` — each a `skill.yaml` contract plus a `process.md` procedure, over a `pipeline.yaml` status graph of 10 statuses and 17 transitions. Nothing here names a runtime; a linter enforces it. |
| `spec/` | 9 schema documents: the skill contract, the work item, journal and history, questions, doc headers and ADRs, Definition of Ready and Done, IDs and statuses, the workspace layout. |
| `scripts/` | Standard-library Python only. A YAML subset reader, a workspace loader, `lint-skills`, `validate-workspace`, `board-gen`, `run-gate`, `transition`, two git-backed gates, workspace and item scaffolding, and `check` — the repository's own gate. |
| `adapters/` | The adapter contract with a 12-box conformance checklist, and a Claude Code adapter: renderer, installer, guard hook, and an honest table of what is hard-enforced versus convention. |
| `examples/toy-project/` | A complete run: one epic, three work items, three bugs, 244 lines of tool, 77 tests, nine ADRs, six questions — with an independent audit of the record. |
| Consumer docs | `USAGE.md`, `CONSUMER-PROMPT.md`, `README.md`. |

Fifty-plus commits, every one referencing a META unit.

---

## 2. The decisions that shaped it

Full reasoning in [`adr/`](adr/); the ones that mattered most:

- **[ADR-0002] Standard-library Python, everywhere, with a YAML subset reader we own.**
  `validate-workspace` runs as a gate inside a consumer's project. A gate that fails because a
  package is missing is indistinguishable, to the agent running it, from a gate that fails
  because the work is wrong. That ambiguity would have poisoned the entire "executable gates"
  premise, so the dependency was removed rather than documented.

- **[ADR-0003] One uniform item directory; IDs derived from the filesystem.** A counter file is a
  second source of truth that goes wrong exactly when this project expects to be interrupted —
  between incrementing and creating.

- **Structured dispatch instead of expressions.** The seed sketched triggers as
  `item.status == "planned"`. An expression language would need an evaluator in every adapter and
  would let engineering judgement leak into the scheduler. `dispatch.on_status` is a list, and
  `lint-skills` cross-checks it against `pipeline.yaml` in both directions.

- **Gates guard a skill's *completion* transition, and nothing else.** Learned by running it:
  gating every move meant `implement` could not reach `in-progress` before code existed, and
  `review-close` could not file a question about the gate blocking it.

- **A closed epic can be reopened.** Also learned by running it. Forbidding it makes "do not
  record the defect" the path of least resistance, because the only ways to silence the validator
  are to file the bug under a different epic or not to file it at all.

- **Which skill may write which document.** `implement` and `verify` may not touch `docs/`,
  because the authoritative record must not be edited by the execution trying to satisfy it. This
  rule, written for that reason, later produced the pipeline's only blocking question — on a case
  nobody had anticipated.

---

## 3. What the toy run proved, and what it cost

The run was not a demonstration. It was a test, and it failed six times.

| # | What broke | Fix |
|---|-----------|-----|
| 1 | `intake` told workers to journal only on the epic; the validator requires an entry per actor per item | Process corrected; both entries now required |
| 2 | No skill ever said to **commit**, so an item's tracker story never reached git | A commit step in six skills, plus a `kind: commit` output in each contract |
| 3 | `check-verify-freshness` compared shas, so `verify`'s own required record commit invalidated its own verification | Compare **paths**: a change confined to `tracker/` or `docs/` does not invalidate a verification of the code |
| 4 | Gates guarded every transition, trapping items | Gates guard only the completion transition |
| 5 | An artifact stamped in local time labelled `Z` froze an item permanently | `transition` stamps `max(now, previous + 1s)` and announces the clamp; plus `--restamp-last`, the one sanctioned repair |
| 6 | `review-close` merged before closing, but the commit-ref gate reads `trunk..branch`, which merging empties | The trial-merge → close → merge order is now the procedure |

Defects 1, 2, 3 and 4 were **caused by this build**; two of them by fixes to earlier defects.
That is worth stating plainly: the methodology was wrong in ways that only running it exposed,
and reasoning about it harder would not have found them.

**What the subagents did that the design was counting on:**

- They reported contradictions instead of working around them silently. Every one of the six was
  found because a worker wrote down that something did not add up.
- `refine` **refused to record a false Definition of Ready override**, because no criterion was
  actually failing — and it was right; the checklist was missing one. That produced R10.
- `review-close` refused to edit a document it was not allowed to edit, and filed a blocking
  question instead, even though editing would have been faster and nobody would have noticed.
- When a gate deadlocked a close, one run **read how earlier items had closed** and found the
  answer in a history row. The record was used as a record.
- `--force` exists and **was never used**. No history row in the toy workspace carries
  `[gates forced]`.

---

## 4. Known weaknesses

Stated because a reader will otherwise find them and wonder what else was hidden.

**The review layers do not catch a plausible false claim.** This is the most important finding in
the build. The independent audit found a justification that is factually wrong — "prints as
`ls -b` prints it" — propagated into shipped source comments, an ADR and the architecture
overview, contradicted by a transcript thirty lines above it in the same item's plan, and passed
by six review layers. It also found two commit shas in reports that do not resolve, an
implementation report whose line arithmetic has the wrong parity, and a review that passed a
record-completeness criterion on counts that were themselves wrong. **Every gate a machine could
decide held; every gate resting on a human-style read did not.** The machine-checkable perimeter
needs to grow.

**The paper trail's chronology is not trustworthy.** The monotonic clamp keeps the record
*orderable*, not *accurate*: six transitions ended up at one-second intervals, and one execution
is dated over two hours apart between its history row and its journal entry. Real chronology is
recoverable only from git.

**Independence is nominal.** One agent played customer, analyst, architect, developer, verifier
and reviewer. The separation is procedural — different contracts, different inputs, no shared
memory — and it demonstrably produced independent-looking behaviour, including a regression pass
that found three real defects in code the same lineage had verified clean. But it is not
adversarial independence, and the disclosure of it lives in two refinement artifacts rather than
in the vision or the epic, which are the documents a manager would read.

**Three specified paths have never run:** the Definition of Ready override (`refine` correctly
refused to fake one), the `blocked` status, and both send-back transitions
(`verifying → in-progress`, `in-review → in-progress`). They are specified, validated and
untested.

**Depth is uneven.** `plan` and `review-close` carry the most judgement and the least machine
support. `next` is fully mechanical and was never wrong.

**One runtime, one language, one project shape.** Every claim about portability rests on the
adapter contract being honest, not on a second adapter existing. The toy project is a single
Python file; nothing here has met a build system, a monorepo, or a change that spans services.

---

## 5. Recommended next iterations

In the order I would do them.

1. **Make the false-claim class machine-checkable.** The audit found what six review layers
   missed, and most of it is mechanical: resolve every commit sha cited in an artifact; check
   that line-count claims match `git diff --numstat`; flag a sentence repeated across documents
   whose wording has diverged. A `validate-claims` script would have caught four of the audit's
   six findings, and none of them needed judgement.

2. **A second adapter (Codex CLI).** The contract is written for it and
   [`adapters/README.md`](../adapters/README.md) §6 records the two questions its implementer
   will hit first. Until one exists, "runtime-neutral" is a design intention.

3. **Exercise the three untested paths deliberately**, as scripted evidence in
   `meta/evidence/` rather than by waiting for a run to need them.

4. **Timestamp integrity.** Have `transition` record the real wall clock alongside the clamped
   value, so the record is both orderable and true.

5. **A retro skill.** Six defects were found by running this once. A skill that reads a completed
   epic's paper trail and proposes contract changes would turn that into a loop rather than a
   one-off — which is the whole premise of versioning the skills.

6. **Then depth**: sprint ceremonies, estimation, multi-item parallelism. None of it is worth
   building while single-item flow still has judgement gates nothing verifies.

---

## 6. Honest summary

The thing works. A raw sentence became an epic, three work items, three bugs found by
independent verification, 77 tests and a merged trunk, driven by context-free subagents through
rendered skills, with an audit that reconstructed the whole story from the record alone.

What it does **not** do is guarantee quality. It guarantees that the checks ran, that the
reasoning was written down, and that a later reader can find where a decision was made. The audit
is the proof of both halves: it signed off, and it signed off *qualified*, naming six things the
process missed. A clean audit from a reviewer that thorough would have been the more worrying
result.

The most useful thing this build produced is not the eight skills. It is the six defect reports
in [`journal.md`](journal.md) — each one a case where running the methodology contradicted the
methodology, and the record said so instead of smoothing it over.
