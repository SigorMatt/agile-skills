# ADR-0008 — Cross-answer consistency: the person's seat in a conflict between their own answers

- **Status:** accepted
- **Date:** 2026-08-29
- **Unit:** META-119
- **Supersedes:** nothing. It extends ADR-0006 — which gave the stakeholder a seat at every
  *ending* — to the case ADR-0006 does not reach.
- **Findings:** F-062 (the class), F-065 (its enabler). Touches F-021, F-022, F-032, D12.

## Context

Iteration 3 planted one contradiction and watched what the machinery did with it. Part one, at
refinement: *"The alignment marker decides everything. Whatever the marker says, that's where
the text sits in the cell — every row, every column, no exceptions"* — recorded as
`WI-0002/Q-001`, `answered-by: human`. Part two, five turns later, arriving as the condition on
a sign-off: *"a cell with a line break or a `<br>` in it should just sit top-left, plain,
whatever the column marker says."* The two cannot both be true.

What happened next is the finding. Every gate held; nobody asked.

| Stage | What it did | Evidence |
|-------|-------------|----------|
| `intake` | scoped a new item so narrowly that both statements could be true of *something* | `WI-0004/item.md` |
| `refine` | asked three sharpening questions, all about part two; its contradiction check ran "against ADRs and internal docs; the stakeholder's own prior answers were never in scope" | `WI-0004/journal.md` |
| `plan` | wrote `ADR-0010`, which quotes part one *and* part two in the same document and reconciles them by fiat | `docs/architecture/adr/ADR-0010…md` |
| `implement` | found the stakeholder's own sentence, quoted with `[src: WI-0002/Q-001]`, now false in `docs/product/vision.md`; **rewrote it** — "Fixed two false claims where the review named one" | `WI-0004/journal.md` |
| `review-close` | caught the same class again under D12, twice, and recorded it as repaired | `WI-0004/artifacts/review.md` |

D12 worked exactly as designed: it found a false sentence in `docs/` and had it corrected. That
is the defect. The sentence was not the pipeline's — it was the stakeholder's, quoted, with a
citation pointing back at the question they answered. Correcting it is deciding, on their behalf
and without telling them, which of their two statements loses. The stakeholder, in persona, held
a one-line reconciliation in reserve for the whole engagement and wrote afterwards: *"They fixed
it as a problem with their document, not as a question for me. I would rather have been asked."*

The shape, stated once: **the machinery treats a recorded human statement as document content to
be made true, rather than as a requirement owned by a person.** Every repair mechanism it has —
D12, `lint-claims`, the change-log discipline, the ADR-supersession rule — operates on documents.
None of them has a step that ends at a person.

## 1. What a recorded human answer is

The unit this ADR protects. A **recorded human answer** is a statement of intent the stakeholder
made, which the workspace stores under an ID a citation can reach:

| Kind | Location | ID |
|------|----------|----|
| an answered question | `tracker/items/<ID>/questions/Q-nnn.md` with `answered-by: human` and a non-empty `## Answer` | `<ITEM>/Q-nnn` |
| a sign-off answer, including any condition attached to it | the same, with `kind: sign-off` | `<ITEM>/Q-nnn` |
| a stakeholder request | `tracker/requests/R-nnn.md` | `R-nnn` |
| a `[human]`-tagged exchange in a refinement record | `tracker/items/<ID>/artifacts/refinement-qa.md` | quoted, and cited through the item |

An answer recorded as `[assumed]` is **not** a human answer for this ADR's purposes: the
pipeline proposed it and the human did not object, so revising it is the pipeline's to do. The
distinction is already in the record (`refine` tags every line) and it is the line between
"their requirement" and "our default".

A **claim sourced to a human answer** is a sentence anywhere in the workspace carrying
`[src: <ITEM>/Q-nnn]` where that question is human-answered. This is the object the mechanical
half of this ADR can actually see, and it exists because `doc-header.md` §4a already made
confident sentences carry their provenance. Provenance built to make a claim *checkable* turns
out to also make its **author** reachable, which is what this ADR spends.

## 2. When a new answer touches a prior one

`refine`, `plan` and `answer-questions` all already run a contradiction check. Its scope is the
project's own documents — ADRs, the vision, the architecture overview. This ADR adds one scope,
and it is the scope that was missing: **the stakeholder's own prior answers**.

A new answer, acceptance criterion, or sign-off condition **touches** a prior recorded human
answer when either holds:

1. **Judged** — the two are about the same behaviour, and a reader holding both would ask which
   applies. This is not mechanical and this ADR does not pretend it is.
2. **Mechanical** — the execution recording the new one changes the text of a claim sourced to
   the prior one. This is the citation graph, read backwards, and it is decidable from a diff.

The second is a strict subset of the first, and it is the subset that fired in iteration 3.

## 3. The two legal moves, and the one refused move

When a new answer touches a prior one, the acting skill has exactly two moves.

- **Cite compatibility.** State, in the record, which prior answers were examined and why the new
  one coexists with each. Naming them is the work; "I checked" is not evidence, in the same sense
  `dor-dod.md` has always meant it.
- **Ask.** File a question addressed to `human` that **quotes both answers by ID and verbatim**
  and asks which wins. The question is `blocking: true` — a contradiction between two
  requirements is not something to proceed past — and its answer is propagated like any other
  (`question.md` §3 rule 5).

And one move is **refused**:

> **A skill may not repair a claim sourced to a human answer by rewriting it, when the reason for
> the repair is that the answer has been overtaken.** The correct move is the question. If the
> sentence is false because the *pipeline* mis-stated what the human said, correcting it is an
> ordinary D12 repair and always was; if it is false because the human has since said something
> else, the document is not the thing that is wrong.

This is `doc-header.md` §5's circularity argument, one turn further round. That rule says
`implement` and `verify` may not edit `docs/`, because the execution trying to satisfy the record
must not also be the one that edits it. The same reasoning applies to the human's own words with
more force, not less: the execution trying to satisfy a requirement must not be the one that
rewrites the requirement.

**Where the line falls, precisely.** Three repairs, one of which is refused:

| The sentence is wrong because… | Move |
|---|---|
| the pipeline paraphrased the human badly, or cited the wrong answer | ordinary repair; cite the answer it should have cited |
| the code changed and the sentence describes the code | ordinary repair (D12, as today) |
| **the human has since said something incompatible** | **refused** — file the question |

## 4. What is enforced, and by what

Hard gate where mechanical, contract rule where not — stated here so nobody has to infer which
is which.

| # | Obligation | Kind | Enforced by |
|---|-----------|------|-------------|
| 1 | Every question the human answered carries a `## Cross-answer check` recording which prior human answers it was checked against and the verdict for each | **hard gate**, presence and shape | `scripts/lint-answers` |
| 2 | A verdict of `conflicts` is matched by a question, addressed to `human`, citing **both** answer IDs | **hard gate** | `scripts/lint-answers` |
| 3 | A claim sourced to a human answer is not rewritten by the execution that the answer overtakes | **hard gate**, over the diff | `scripts/lint-answers --changed-since` |
| 4 | The prior answers named in a cross-answer check are the ones the new answer actually touches | **contract rule** | `refine`, `plan`, `answer-questions`, `review-close` process and exit criteria |
| 5 | `refine`'s contradiction check includes the stakeholder's prior recorded answers, not only ADRs and internal docs | **contract rule** | `refine` |

Obligation 1 is the load-bearing one, and it is deliberately a *presence* check. It cannot know
whether the check was done well. What it can do — and what iteration 3 shows is enough to change
the outcome — is make "the stakeholder's own prior answers were never in scope" a sentence no
execution can write while passing its gates.

**The check is written by the skill that consumes the answer, not by the human.** The human
writes `## Answer` and nothing else (the harness's own S1 boundary says so, and so does
`question.md`). `lint-answers` therefore fires only on questions at `status: answered` — the
state only `answer-questions` and `review-close` can set — so the window between a person
replying and the pipeline reading the reply is not a broken workspace.

## 5. What the lint can and cannot see

Stated plainly, because a gate whose limits are not written down gets trusted for things it does
not do — which is F-001's whole finding.

**It can see:**
- that a cross-answer check exists on every consumed human answer, and is shaped like a check —
  IDs that resolve, a verdict per ID;
- that a declared conflict was escalated to a question that names both answers;
- that a claim carrying `[src: <ITEM>/Q-nnn]` had its text changed by an execution which filed no
  question about that answer.

**It cannot see:**
- **whether two answers actually conflict.** Nothing in this design reads meaning. A skill that
  writes `compatible` about two contradictory answers passes the gate. The defence is that it
  must now write the ID and the sentence, so the wrong call is *in the record, attributable*,
  instead of being an absence.
- **which prior answers were on-topic.** A citation-graph topic key was measured against
  iteration 3's real record before this was written: taking "the document a later answer's
  consequences name" as the topic anchor produced **58 candidate pairs** in one four-item
  engagement, because `docs/product/vision.md` legitimately accumulates every answer in the
  engagement. A gate that demands 58 reconciliations gets switched off, and a gate that gets
  switched off is worse than none. So the topic judgement stays with the skill (obligation 4) and
  the mechanical trigger is narrowed to the one relation with a low false-positive rate: the
  rewritten sourced claim.
- **a conflict that never reaches a document.** Two answers can contradict each other while every
  document stays silent about both. Obligation 1 is the only thing covering that case, and it
  covers it by asking rather than by detecting.
- **a conflict inside one answer**, or between an answer and an `[assumed]` default.

## 6. What this costs

**More questions.** A stakeholder will be asked "which of these two do you mean" where previously
the pipeline decided. That is the point, and iteration 3 says the cost is welcome: the persona
had the answer ready and was never asked for it. It is also bounded — the question is only due
when a *conflict* is found, not on every answer.

**A round trip at the worst moment.** The likeliest trigger is a sign-off condition that
contradicts an earlier answer, and the question lands when the engagement was about to end. The
alternative is ending it on a document the stakeholder would not recognise as theirs.

**One more required section.** Every consumed human answer grows a `## Cross-answer check`. For
the common case its content is one line (`Checked against: none — first answer on this
behaviour.`), and that line is itself worth having: it says the check ran.

## Alternatives rejected

- **Semantic conflict detection.** A model-graded check over pairs of answers. Rejected: it is a
  judgement gate wearing a program's clothes, which is exactly the class F-001 named. If it is
  judgement, it belongs in a skill's contract where its failures are attributable.
- **Freeze claims sourced to human answers — refuse every edit.** Rejected: it makes the honest
  repairs of §3's first two rows illegal, and an unsatisfiable rule is the F-050 mistake.
- **Route it through the existing `blocked` / impasse machinery.** Rejected: a contradiction
  between two requirements is a question with an obvious addressee, not an impasse. The
  engagement is not stuck; one person can unstick it in a sentence.
- **Detect the conflict at the ending only, in `review-close`.** Rejected: iteration 3 shows the
  ending is where the reconciliation gets *written down* by whoever is closing. The obligation has
  to sit where the answer is consumed, which is upstream of the ending.
