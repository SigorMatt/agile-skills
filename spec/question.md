# `questions/Q-###.md` — the escalation protocol

A question is a **first-class artifact**, not a message. It has a file, an ID, a state, and a
recorded consequence. This is the mechanism that lets `implement` and `verify` be blocked by
something they must not decide, without either guessing or interrupting the human.

Location: `tracker/items/<ID>/questions/Q-###.md`, numbered per item.

---

## 1. Who may ask whom

| Skill | May ask the human directly | May file a question |
|-------|---------------------------|---------------------|
| `intake` | yes — it is a conversation | rarely; prefers to ask now |
| `refine` | yes — it is a conversation | rarely; prefers to ask now |
| `plan` | yes, as a last resort | yes |
| `implement` | **never** | yes |
| `verify` | **never** | yes |
| `review-close` | **never** | yes |
| `answer-questions` | yes, when it cannot answer from the record | it answers them |

`plan`'s preference order is fixed and MUST be followed in this order:

1. Answer it from existing documentation. Cite what you read.
2. Make a **reversible** assumption, record it in the plan under `## Assumptions`, and continue.
3. Ask the human — only when the decision is not reversible, or when it depends on intent that
   no document captures.

The reason `implement` and `verify` may never ask directly is not politeness. It is that a
question answered in chat leaves no artifact, so the next execution of the same skill — after a
restart, or on a sibling item — cannot see the answer and will ask again or guess differently.
Answers must land in documents, which is what `answer-questions` is for.

---

## 2. File format

```markdown
---
id: Q-001
item: WI-0007
from-skill: implement
addressed-to: architect
blocking: true
status: open
created: 2026-08-16T11:05:52Z
---

## Context

What I was doing, what I read, and where the record stops short. Enough that the answerer does
not have to re-derive it.

## Question

One question, stated so that it can be answered. If there is more than one, file more than one
question.

## Options considered

- **A —** <option>. Consequence: <what follows>.
- **B —** <option>. Consequence: <what follows>.
- **Recommendation:** <which, and why> — or `none, insufficient basis`.

## Answer

<!-- filled in by answer-questions -->

## Consequences

<!-- filled in by answer-questions: which documents, plans, or items changed as a result -->
```

### Frontmatter fields

| Field | Required | Rules |
|-------|----------|-------|
| `id` | always | `Q-###`, matching the filename, unique within this item |
| `item` | always | the owning item's ID; MUST match the containing directory |
| `from-skill` | always | the skill that filed it |
| `addressed-to` | always | `architect` \| `human` |
| `blocking` | always | `true` \| `false` |
| `status` | always | `open` \| `answered` |
| `created` | always | UTC ISO-8601 |
| `answered-at` | when answered | UTC ISO-8601, ≥ `created` |
| `answered-by` | when answered | `answer-questions`, or `human` when escalated |

### Body rules

- `## Context` and `## Question` MUST be non-empty when the question is filed.
- `## Options considered` MUST list at least two options **or** state explicitly why the
  question is not a choice between options (e.g. a missing fact). A question filed without
  having thought about the answer pushes the whole cost of the thinking upstream, which is how
  a question protocol degrades into "ask the human everything".
- `## Answer` and `## Consequences` MUST be non-empty when `status: answered`.
- `## Consequences` MUST name **files**, not intentions. "Updated the plan" is not a
  consequence; "`artifacts/plan.md` step 3 rewritten; `item.md` AC2 amended; `docs/architecture/
  adr/ADR-0004.md` created" is. This is what makes the rule "downstream skills re-read
  artifacts, never the Q&A" actually enforceable.

---

## 3. Protocol

```
                    filed (blocking: true)
   implement  ─────────────────────────────►  item.status = awaiting-answer
   verify                                     history resume-to = <suspended status>
   review-close                                          │
                                                         ▼
                                              answer-questions is dispatched
                                                         │
                          ┌──────────────────────────────┴───────────────────────┐
                          ▼                                                      ▼
             answerable from the record                        not answerable from the record
             → write Answer + Consequences                     → re-address to human, keep open,
             → update the named artifacts                        surface it and stop the loop
             → status = answered                                          │
             → item returns to resume-to                                  ▼
                                                              human answers in the file
                                                              → answer-questions propagates
```

Rules:

1. **A blocking question suspends the item.** The filing skill sets `status: awaiting-answer`
   and writes a history row whose `resume-to` is the status being suspended. It then stops. It
   MUST NOT continue on a guess "to save time" — the guess is exactly what the protocol exists
   to prevent.
2. **A non-blocking question does not suspend anything.** The item continues. The question is
   still filed, still answered, and still shows on the board. Use it for "this should be
   written down somewhere" rather than "I cannot proceed".
3. **The orchestrator will not advance an item while a blocking question on it is open.**
4. **A question addressed to `human` stops the autonomous loop.** The orchestrator surfaces it
   and stops; there is nothing else it can legitimately do.
5. **Answers propagate into artifacts.** `answer-questions` MUST update the authoritative
   documents — the plan, the item's acceptance criteria, an architecture doc, a new ADR — and
   list them under `## Consequences`. An answer that exists only inside the question file has
   not been propagated, and the next skill will not see it.
6. **The question is never deleted, and its `status` is never reverted.** A superseded answer is
   handled by filing a new question that cites the old one.

---

## 4. When to escalate to the human

`answer-questions` escalates — sets `addressed-to: human` — only when at least one holds:

- The answer depends on **intent** that no document records (what the user actually wants).
- The answer is **not reversible** — it commits the project to something expensive to undo.
- The answer would **contradict** an existing ADR or product doc, which only the human can
  authorise.
- The record is **genuinely silent** and any choice would be a coin flip with material
  consequences.

It MUST NOT escalate merely because answering is effortful. An architect who forwards every
question is not doing the job, and the human's attention is the scarcest resource in the loop.
Every escalation MUST state, in `## Context`, which of the four conditions above applies.
