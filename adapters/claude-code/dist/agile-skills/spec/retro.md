# `retro.md` — the retrospective report and the finding proposals it exports

The retrospective report is written once per engagement, after it has ended, by the `retro`
skill. It is the only artifact in the workspace whose subject is **the way the work was done**
rather than the work, and it is the only one part of which is meant to leave the project.

Derived from `meta/adr/ADR-0009-retrospective-reading.md`. Read §5 and §8 of that ADR before
trusting this format for more than it does: the classification is judgement, and no linter can
decide it.

**Path:** `tracker/items/<EP-ID>/artifacts/retro.md`, one per epic. Fixed name, like every other
artifact (`workspace-layout.md` §1.2). Re-running `retro` overwrites it and appends a journal
entry; there is no `retro-2.md`.

---

## 1. Frontmatter

```yaml
---
engagement: EP-001
ending: E1
written: 2026-08-30T14:02:11Z
items-read: 6
journal-entries-read: 23
proposals: 3
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `engagement` | yes | the epic ID this report is filed under; MUST equal the directory's item |
| `ending` | yes | `E1` \| `E2` \| `E3` \| `E4` — the ending recorded on the epic (`ids-and-statuses.md` §3.5). A report on an engagement that has not ended is invalid, not premature |
| `written` | yes | UTC ISO-8601 to the second, read from a clock (`journal-and-history.md` §0) |
| `items-read` | yes | how many items the analyst opened. Cross-checked against the workspace |
| `journal-entries-read` | yes | how many journal entries the analyst read |
| `proposals` | yes | how many entries `## Proposed toolkit findings` contains, `0` included |

The three counts are in the frontmatter rather than left to be inferred because a retro's
failure mode is silence: a report with nothing in it is what a diligent reading of a flawless
engagement produces **and** what a reading that opened no files produces. A count that
contradicts the workspace is the one form of dishonesty a program can catch.

---

## 2. Required sections, in this order

```markdown
# Retrospective — EP-001

## What was read
## Engagement retrospective
## Positive record
## Proposed toolkit findings
```

Order is fixed and all four are required. `## Proposed toolkit findings` MUST be last, because
it is the section that gets lifted out and sent somewhere; a section that ends the document can
be copied from its heading to the end of the file without deciding where it stops.

A section with nothing in it says so in a sentence — `None.` and why — and is not omitted. An
absent section and an empty one are different claims, and only one of them was made on purpose.

---

## 3. `## What was read` — the scope, declared and checkable

The report names what the analyst actually opened:

```markdown
## What was read

- **Items:** EP-001, WI-0001, WI-0002, WI-0003, WI-0004, BUG-0001 — `item.md`, `history.md` and
  `journal.md` for each, in full.
- **Journal entries:** 23, across 6 items.
- **Questions:** 14, including the four on EP-001 and the sign-off exchange.
- **Artifacts:** every `plan.md`, `impl-report.md`, `verify-report.md` and `review.md`.
- **Documents:** `docs/product/vision.md` v9, `docs/architecture/overview.md` v9, ADR-0001..0010.
- **History:** `git log --oneline` over the engagement's window, 31 commits.
- **Contracts:** the installed contracts for `intake` 0.3.0, `refine` 0.3.0, `plan` 0.4.1,
  `implement` 0.3.0, `verify` 0.2.0, `review-close` 0.6.0, `answer-questions` 0.3.1.
- **Not available:** no git history in this copy of the workspace; timings below are read from
  record timestamps only.
```

Rules:

- Every item in the engagement MUST appear under `**Items:**`, or the report MUST say which were
  not read and why. A retro that skipped an item and did not say so has produced a reading of a
  different engagement.
- `**Not available:**` is required when an input the skill's contract lists could not be read.
  Saying so is what keeps a thin reading distinguishable from a thorough one.
- The counts here MUST agree with the frontmatter.

**Why this section is normative.** `lint-claims` was once able to exit 0 having examined nothing
(F-033, and again at an ending, F-066), and a gate that passes over an empty scope is the failure
this project has now found three times. The retro is the most exposed thing yet written to it,
because reading *is* its whole job and an empty result is indistinguishable from an unopened
file. So the scope is declared, and it is checked against the workspace rather than believed.

---

## 4. `## Engagement retrospective` — the observations

One observation per `###` heading. Every observation is about **this engagement** and is read
once, by the team that ran it.

```markdown
### The stakeholder's own sentence was repaired instead of being put back to them

`implement` found that a sentence quoted from the stakeholder and carrying its citation had
become false, and rewrote it in place: *"Fixed two false claims where the review named one"*
[src: tracker/items/WI-0004/journal.md:455]. The claims gate passed, because the sentence now
matched the behaviour [src: WI-0004/Q-002]. Nothing in the record shows the person being asked
which of their two statements they meant to keep.

**Where it shows in the record:** WI-0004's second `implement` entry; the same document is sent
back on the same two Definition-of-Done criteria a second time in the change-log row for v5.
```

Rules:

- The heading is a **statement**, not a topic. "Questions" is a topic; "three refinement
  questions were filed in one round and two of them were answered together" is an observation.
- **Every observation MUST carry at least one citation, and every citation MUST resolve.** An
  uncited observation is a refused write. This is `doc-header.md` §4a's rule applied to a report
  whose entire content is claims about a record the reader is holding.
- Citations use §4a's forms unchanged — workspace path (with a line number where it helps), item,
  `ITEM ACn`, `ITEM/Q-nnn`, ADR number, commit sha, `run: <command> → <outcome>`. Nothing new is
  invented, so the retro's citations are resolved by the same code that resolves an ADR's.
- An observation states what the record shows and where. It does **not** state what should be
  done about it: a change is a proposal, and proposals are §6's section.
- Observations are written about the **work**, never about a person. There are no people in a
  workspace record; there are skills, contracts and executions.

---

## 5. `## Positive record` — what held

The same shape as §4 — a statement per `###` heading, cited — for the things that worked, and
especially for a rule that can be shown to have caught something.

This section is required and it is not decoration. A reading that reports only faults cannot be
distinguished from a lazy one, and the fixes worth keeping are precisely the ones a later
engagement can be shown to have benefited from. This project's own ledger keeps these sections
for that reason.

---

## 6. `## Proposed toolkit findings` — the exportable half

Candidate findings, in the upstream ledger's format, for a human to triage. They are the reason
the retro exists in a distributed project: every consumer's engagement can generate upstream
findings, and none of them can file one.

```markdown
### P-1 — PROPOSED — a criterion about other criteria is satisfiable by a coverage gap

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (refine, verify), spec/dor-dod.md
- **Symptom:** WI-0004's AC5 required that "every acceptance criterion of WI-0001..0003 still
  holds, named tests pass unmodified". It was satisfied by observing that no test or fixture
  exercises both rules at once [src: tracker/items/WI-0004/item.md], so the criterion passed
  while the criteria's sentences contradict each other [src: WI-0002/Q-001].
- **Counterfactual:** any engagement whose later item narrows an earlier rule reaches this. The
  criterion is written by `refine` from a template and assessed by `verify` against the suite;
  neither step reads the earlier criteria's text. Nothing about this project's subject matter is
  load-bearing in that sentence.
- **Recurrence:** once in this engagement, at WI-0004. The same shape almost recurred at BUG-0001
  [src: tracker/items/BUG-0001/artifacts/review.md].
- **Direction:** a "still holds" criterion is assessed against the criteria's *text*, with the
  test suite as evidence for the answer rather than as its definition; where the domains do not
  intersect in tests, the non-intersection is stated and a covering case added or waived by name.
- **Status:** proposed — not filed. Triage upstream.
```

| Field | Required | Rules |
|-------|----------|-------|
| `Classification:` | yes | exactly one of `toolkit-defect`, `project-circumstance`, `observation` (§7) |
| `Severity:` | yes | the honest severity, in the ledger's vocabulary: `structural`, `correctness of enforcement`, `correctness of the record`, `methodology gap`, `UX`, `doc error`, `enhancement`, each with `high`/`medium`/`low` where it helps. A proposal claiming `structural` MUST name what it structurally prevents |
| `Component:` | yes | which part of the toolkit — a skill, a spec file, a script — by name. `project-circumstance` names the part of *this project* instead |
| `Symptom:` | yes | what the record shows, with citations. Not what is wrong with it |
| `Counterfactual:` | on `toolkit-defect` | what a **different** engagement, on a different subject, would hit here (§7) |
| `Recurrence:` | on `toolkit-defect` | how many times it occurred in this engagement, and where |
| `Direction:` | yes | the shape of a fix, not a patch. A direction naming one line of one file is a specimen, not a finding |
| `Status:` | yes | the literal `proposed` |

Rules:

- The heading MUST carry a local ID (`P-1`, `P-2`, …) and the word **PROPOSED**. Never an
  `F-###`: the upstream sequence is not the consumer's to allocate, and every consumer would
  allocate the same numbers. The word is in the entry rather than only in the section heading
  because the block is designed to be copied out, and a copied block that has lost it is a
  finding nobody filed.
- Every proposal MUST carry at least one citation, under the same rule as §4.
- **The class, not the specimen.** A proposal is written about the rule that failed, not about
  the sentence that failed it. "WI-0004's AC5 was checked against the test suite" is a specimen;
  "a criterion about other criteria is satisfiable by a coverage gap" is the finding.
- A proposal MUST NOT propose a change to this engagement's own record. The record is closed and
  the retro is read-only over it (ADR-0009 §1.1).

---

## 7. The classification

| Value | Means |
|-------|-------|
| `toolkit-defect` | a skill, spec rule, or script would mislead **any** engagement that reached this situation |
| `project-circumstance` | this engagement's own difficulty: its domain, its codebase, a stakeholder who changed their mind, a slow test suite |
| `observation` | a fact about how the work went that is neither of those, worth recording and proposing no change |

**The failure mode this three-way split exists to prevent is filing "this project was hard" as
"the skill is broken".** It is the cheap failure, not the exotic one: a difficult engagement
produces friction everywhere, and every piece of friction can be phrased as a complaint about a
tool. A ledger that fills with those stops being read, and then the real defects arrive into a
channel nobody is reading.

Nothing mechanical decides the class. What is mechanical is that the distinguishing work was
done and written down: `Counterfactual:` is required on every `toolkit-defect`, and **a proposal
whose counterfactual can only be stated in this project's own subject matter is a
`project-circumstance`** — writing the sentence is what exposes it. The wrong call then sits in
the record, attributable, instead of being an absence.

`project-circumstance` and `observation` entries stay in the report. Only `toolkit-defect`
entries are meant to travel.

---

## 8. What is checked, and what is not

`scripts/lint-retro` enforces the mechanical half. ADR-0009 §8 states the boundary in full; the
short form:

**Checked:** the path and the frontmatter; that the engagement has ended; the four sections and
their order; that the declared scope exists in the workspace and is not degenerate; that every
observation and every proposal carries a citation and that every citation resolves; the required
fields on every proposal; `Counterfactual:` and `Recurrence:` on every `toolkit-defect`; the
literal `PROPOSED`; and that the classification is in the closed set.

**Not checked:** whether an observation is true — a citation that resolves is not a citation that
supports the sentence, which is F-001's standing residual; whether a classification is right;
whether the retro found everything, which cannot be measured from inside; and whether a proposal
duplicates one already filed upstream, which is the triager's job and the reason the word
`PROPOSED` exists.

---

## 9. Which skill writes what

| File | Written by | When |
|------|-----------|------|
| `artifacts/retro.md` | `retro` | once per engagement, after the ending is recorded and before the engagement is fully closed |

No other skill writes it, and `retro` writes nothing else in the engagement except its own
journal entry on the epic. An auditor that can edit its subject cannot show that it did not edit
the evidence into agreement with its conclusions.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-30 | Initial. Derived from ADR-0009. |
