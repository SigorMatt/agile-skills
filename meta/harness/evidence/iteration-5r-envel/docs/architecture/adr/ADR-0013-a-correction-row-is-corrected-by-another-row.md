---
title: A wrong citation inside a Corrections row is corrected by a further row, never by editing it
version: 1
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0013 — A wrong citation inside a `## Corrections` row is corrected by a further row, never by editing it

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

`EP-001`'s termination review swept every line-bearing `[src: ...]` citation in `docs/` against the
code and found six that resolve without supporting the sentence they are attached to. Four sit in
live prose and are repaired under the policy this project already settled twice, at `WI-0005/Q-009`
[src: WI-0005/Q-009] and `BUG-0001/Q-002` [src: BUG-0001/Q-002]: correct the citation where it
stands, with a `provenance` row, a change-log row and a version bump
[src: toolkit: doc-header.md §4b "add a citation to an existing sentence"].

Two do not, and that is what forced this decision. They are **inside** `## Corrections` rows:

- `ADR-0006` [src: ADR-0006]'s `WI-0004` erratum row cites `envel/envelopes.py:245` for *"`on` is
  the day the money moved on a spend and on a move alike"*. That line is `return Refusal(` inside
  `move`'s zero-amount check; the writes the sentence names are at `envel/envelopes.py:171`,
  `envel/envelopes.py:269` and `envel/envelopes.py:275`.
- `ADR-0011` [src: ADR-0011]'s `WI-0005` provenance row states that `envel/cli.py:165` *"is now
  `elif arguments.command == "spend":`"*. That statement is at `envel/cli.py:163`
  [src: envel/cli.py:163]; line 165 is `document,` [src: envel/cli.py:165].

The settled policy cannot reach either, because the text that is wrong **is** a correction row, and
`## Corrections` is append-only: *"An entry is never edited or removed. A correction whose row says
'fixed a wrong sentence' without quoting it destroys the evidence this section exists to keep"*
[src: toolkit: doc-header.md §4b "An entry is never edited or removed"]. Nothing in the record says
what to do instead, which is why `EP-001/Q-008` [src: EP-001/Q-008] was filed rather than answered
from precedent.

Neither error touches a decision. Both ADRs are `status: accepted` and both still describe what the
code does; what is wrong is a pointer in a row whose subject is the document's own history.

## Options considered

- **A — append a further `## Corrections` row whose subject is the earlier row.** Cost: the row
  quotes the earlier row's wording verbatim and says what is false about it and what is true, and
  the earlier row is left exactly as it stands — the correction is by *superposition* rather than
  replacement, which is what append-only means. It needs a `kind` from a two-word alphabet that was
  written for rows about the ADR's own prose, and `erratum` is the one that fits, because what the
  row does is correct something false. Risk: `## Corrections` grows entries whose subject is
  further from the decision the section is attached to, and a reader has to follow two rows to get
  one fact.
- **B — leave both rows standing and record the errors only in the reviewing item's `review.md`.**
  Cost: nothing is written that the append-only rule did not anticipate. Risk: the two sentences
  stay false in `docs/`, where a reader is far likelier to meet them than in a closed epic's
  review, and the epic's Definition of Done asks whether every claim in `docs/` is true
  [src: toolkit: dor-dod.md DE6 "Every claim in `docs/` about behaviour this epic delivered has been checked against the code"].
- **C — treat a `## Corrections` row's citation as outside the claims audit**, on the ground that
  the row is a dated historical statement rather than a standing claim about the product. Cost:
  the question stops recurring and the audit gets a stated boundary. Risk: the boundary belongs to
  the toolkit's own claims spec and not to this project, and `ADR-0011`'s row shows the exemption
  would cover a sentence that is simply wrong rather than merely dated.
- **D — supersede both ADRs.** Cost: the provenance becomes unambiguous. Risk: disproportionate and
  wrong on its face — no decision changes, both ADRs are still the accepted design, and
  supersession is reserved for a change a reader would have to change code to satisfy.

## Decision

**A.** In this project, a false or stale statement **inside** a `## Corrections` row is corrected by
appending a further row to the same section. Three rules, so that a later reader can check the act
rather than infer it:

1. **The earlier row is not touched.** Not the citation, not the wording, not the timestamp. The
   append-only rule is about the *act*, and an error preserved beside its correction is the evidence
   the section exists to keep.
2. **The new row carries `kind: erratum` and quotes the earlier row's wording verbatim.** `erratum`
   is the kind for *a clause that was false against the code*
   [src: toolkit: doc-header.md §4b "replace a clause that was **false** against the code"], and the
   quoting requirement is already what that kind demands — here it identifies the target instead of
   preserving what was deleted, because nothing is deleted. `provenance` is the wrong word: nothing
   in the earlier row gains a citation.
3. **The new row says which row it corrects, by its `when` stamp, and states what is true with a
   citation that resolves.** A correction that says *"an earlier row was wrong"* without saying
   which one is the shape rule 1 is protecting against, one level up.

This is the journal's own rule applied to the other append-only structure in this workspace: *"A
wrong entry is corrected by a later entry that says what was wrong; a rewritten entry destroys the
only evidence that anything went wrong at all"*
[src: toolkit: journal-and-history.md §0 "A wrong entry is corrected by a later entry that says what was wrong"].

## Consequences

**Easy: the defect has a route, and it is the route the rest of the workspace already uses.** Both
rows are repairable in this same execution, and any future one is repairable the same way without
another question. No code changes and no decision changes.

**Easy: the error stays visible.** A reader of `ADR-0006` [src: ADR-0006] or `ADR-0011`
[src: ADR-0011] meets the wrong pointer and its correction in the same table, in order. That is
strictly better than a silent edit, which would leave a reader who had quoted the old row with no
way to tell what happened.

**Hard: `## Corrections` is now two kinds of row.** Some rows correct the ADR's prose and some
correct an earlier row, and only the text distinguishes them. Rule 3's *say which row, by its `when`
stamp* is the mitigation, and it is a convention a writer can forget — nothing mechanical enforces
it, exactly as nothing mechanical decides whether an `erratum`'s quoted text was really the text
removed.

**Hard: this is a decision about the record rather than about `envel`.** Every other ADR here is
about the tool's design, and a reader looking for architecture will find one that is not. It is
recorded as an ADR because the record was silent and a new decision was taken, which is what an ADR
is for; the alternative homes — a process document this project does not have, or the question file
alone — would each have put it somewhere no later execution reads.

**Reversibility: easy.** Reversing means adopting option B or C: stop appending these rows. The two
rows this ADR authorises stay where they are, because they are append-only too, and nothing else in
the project depends on them. No stored data, no code, no interface.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | Created, answering `EP-001/Q-008`. Records how a false or stale statement inside an append-only `## Corrections` row is repaired: by a further `erratum` row that quotes it and names which row it corrects, never by editing it. |
