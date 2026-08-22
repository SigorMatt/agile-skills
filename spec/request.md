# `tracker/requests/R-###.md` — the stakeholder's own channel

A question is the pipeline asking the human something. A **request** is the human speaking first.

Location: `tracker/requests/R-###.md`, numbered across the whole workspace. Requests are not
filed under an item, because the stakeholder does not know — and should not have to know — which
item their thought belongs to. Deciding that is `intake`'s job.

---

## 1. Why this exists

Without it, the human can only speak when spoken to. In a real automated run the simulated
stakeholder held a new requirement across two turns and recorded, in its own log, that no
question gave it a vehicle to raise it; the run then closed the epic with the requirement never
voiced (F-021). Every channel the methodology had — questions, answers, sign-off — is opened by
a skill. A stakeholder who notices something between rounds had nowhere to put it but the next
question's answer box, where it does not belong and where nothing routes it.

Real stakeholders volunteer requirements, corrections, and changes of mind constantly, and they
do it at the worst possible moment by design: the moment they think of it.

---

## 2. File format

```markdown
---
id: R-001
from: human
status: open
created: 2026-08-16T14:02:11Z
about: EP-001
---

## Request

What the stakeholder wants, in their own words. Not translated into tracker vocabulary — the
translation is what `intake` does, and the original wording is evidence of intent.

## Why now

Optional. What prompted it: something they saw, something that changed, something they realised.

## Response

<!-- filled in by the skill that handled it -->

## Consequences

<!-- filled in by the skill that handled it: the items, criteria and documents that changed -->
```

### Frontmatter fields

| Field | Required | Rules |
|-------|----------|-------|
| `id` | always | `R-###`, matching the filename, unique in the workspace |
| `from` | always | `human` — the only author a request may have |
| `status` | always | `open` \| `accepted` \| `declined` |
| `created` | always | UTC ISO-8601 |
| `about` | optional | an item or epic ID the stakeholder names. Absent means "the project" |
| `handled-at` | when not open | UTC ISO-8601, ≥ `created` |
| `handled-by` | when not open | the skill that responded |

### Body rules

- `## Request` MUST be non-empty when the file is created. Nothing else need be.
- `## Response` and `## Consequences` MUST be non-empty once `status` is `accepted` or
  `declined`.
- `## Consequences` MUST name **files or item IDs**, not intentions — the same rule questions
  obey, for the same reason: a response that reaches no artifact has not been acted on, and the
  next skill will never see it.
- `## Request` is **never edited by a skill.** It is the stakeholder's wording, and it is the
  only record of what they actually asked for. A skill that disagrees with the framing says so
  in `## Response`.

---

## 3. Protocol

```
   human writes tracker/requests/R-###.md  (status: open)
                          │
                          ▼
   next, before it selects anything to work on, sees the open request
                          │
                          ▼
   intake is dispatched on it
                          │
        ┌─────────────────┴──────────────────┐
        ▼                                    ▼
   it changes the work                  it does not
   → new or amended items,              → status: declined, with the reason
     criteria, docs                       in ## Response
   → status: accepted
   → ## Consequences names them
```

Rules:

1. **An open request outranks selecting work.** `next` handles it before it builds the candidate
   set. A request that waits until the current item finishes is a request answered against a
   plan the stakeholder has already tried to change.
2. **It does not suspend anything by itself.** Work in progress keeps its status. If acting on
   the request invalidates an item that is mid-flight, the handling skill files a *question* on
   that item in the ordinary way, and the ordinary suspension rules apply.
3. **Declining is a legitimate outcome, and it is recorded.** A request outside the epic's scope,
   or one that contradicts a decision the stakeholder already made, is declined in writing with
   the reason. Silently absorbing it is the failure this artifact exists to prevent; so is
   silently doing it.
4. **A request is never deleted and its `## Request` is never rewritten.** Superseding one means
   filing another that cites it.
5. **A request never carries an answer to a question.** Those go in the question's `## Answer`.
   Two channels with one meaning is how a record starts disagreeing with itself.

---

## 4. What a request is not

- Not a work item. It has no acceptance criteria, no branch, no Definition of Done. `intake`
  turns it into items, or declines it.
- Not a question. The pipeline is not waiting on it, and it does not suspend an item.
- Not a conversation. One request, one thing asked. A stakeholder with three thoughts files
  three files, and each gets its own recorded response.

---

## Revisions

| # | Date | Change |
|---|------|--------|
| 1 | 2026-08-22 | Initial — the stakeholder-initiated channel (F-021). |
