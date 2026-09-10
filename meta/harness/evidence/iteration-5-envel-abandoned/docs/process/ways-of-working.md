---
title: Ways of working
version: 3
status: current
updated: 2026-09-10T15:34:21Z
updated-by: answer-questions
updated-for: WI-0002
---

# Ways of working

Conventions this project adopted, as they were needed. Each section says what happened that
made the convention necessary, so a reader can tell a rule from a habit.

## When a pipeline gate refuses something no actor is permitted to fix

Written for `WI-0001/Q-003`. WI-0001's code was finished, tested and green, and
`claims-are-sourced` refused the move to `verifying` over a sentence in
`docs/product/vision.md`'s `## Engagement state` section — a sentence that item did not write,
did not falsify, and is forbidden to repair [src: WI-0001/Q-003].

The methodology and the gate disagreed, and the methodology is the authority. `spec/dor-dod.md`
D12 says of the obligation `lint-claims` rule 2 mechanises: *"Engagement-state sentences are out
of scope: no item audit is charged with one"*, and `spec/doc-header.md` §4a derives why — an
engagement-state statement is falsified by the engagement's own act rather than by a code change,
so what it owes is to be restated at the ending, not a citation
[src: .claude/agile-skills/spec/dor-dod.md; .claude/agile-skills/spec/doc-header.md]. The gate's
implementation has no notion of those kinds, so it asked that sentence for the evidence a cited
fact owes.

**The convention.** An acting skill may record a hard gate as **failed** and make its transition
with `scripts/transition --force` when four things hold, and it writes down each of them:

1. the finding is outside the rule the gate implements, with the clause quoted from `spec/`;
2. the change that would clear it is unavailable — skill by skill, through the nine
   `pipeline.yaml` defines, either a rule forbids that skill from making it or the condition
   under which it may is one that does not hold; written out, skill by skill, not asserted
   [src: .claude/agile-skills/pipeline.yaml; .claude/agile-skills/spec/doc-header.md];
3. an open or answered question records the diagnosis, the options and the decision;
4. the acting skill's journal carries the gate's verdict as `fail` with the run's own output
   beside it, and the history reason names the question.

**What it is not.** It is not a licence to force a gate that is inconvenient, slow, or right
about something awkward. A reader can check the four conditions one by one
[src: WI-0001/Q-003], and the second is the load-bearing one — it is also the one most likely to
be got wrong, because two of the nine skills *do* own the change here and are simply not
dispatchable at this point. Writing the enumeration out is what caught that; asserting it would
not have. If a skill the pipeline can dispatch could have made the repair, the answer is to
dispatch it rather than to override the gate. It is also not a repair — the underlying
finding stays open until the actor who owns it acts, which for an engagement-state sentence is
`review-close` at the ending, restating every such section it finds (`spec/dor-dod.md` DE4).

**What it costs, said plainly.** Each skill that meets the same finding meets it again:
`verify` and `review-close` will both see it on WI-0001, and the plans of WI-0002 to WI-0005
will name the same document for the same reason. This section is what stops each of them
spending a round trip rediscovering it.

**The underlying defect, for the retrospective.** `scripts/lint-claims` rule 2 does not skip
paragraphs inside a delimited `## Engagement state` section, although `scripts/lint-documents`
already knows how to find one. Its code-token test also reads a backticked item or question ID as
a named code object, because the test asks whether the token contains `/`
[src: .claude/agile-skills/scripts/lib/claims.py:148] — so `\`EP-001/Q-001\`` counts as code and
drags the paragraph around it into rule 2's scope. Either change on its own would have cleared
this. The toolkit is not this project's to change, so the finding is recorded here and in
`WI-0001/Q-003` for whoever reads the engagement's trail.

## Where an accepted test-coverage gap goes

Written for `WI-0001/Q-004`. A review may accept a gap in a **test suite** without sending a green
item back: the behaviour is right and was demonstrated, and nothing exercises it. WI-0001 closed
with two of them — `store_path`'s XDG and home branches, and the end-to-end half of AC11's
trimming rule [src: tracker/items/WI-0001/artifacts/review.md]. `review-close` writes no tests,
and the item it is permitted to create is a `bug` at `ready`
[src: .claude/agile-skills/pipeline.yaml] — which a gap in a passing suite is not, because nothing
is broken. So a gap of this kind reaches the end of its review with nobody to hand it to.

**The convention.** Such a gap is carried by the **next item that opens the code it covers**: it
is written into that item's `## Notes` while the item is still unplanned, and that item's `plan.md`
carries it as a step. Three things must hold, and whoever disposes of the gap writes each of them
down:

1. **The host item is dispatchable now** — it exists, it is not `done`, and the orchestrator will
   reach it as an ordinary candidate. This is what the accepted-gap rule is asking for:
   *"An accepted gap is dispatchable or it is nothing"*
   [src: .claude/agile-skills/spec/dor-dod.md]. A gap recorded only in `review.md` is inert,
   because the orchestrator selects on item status and on questions.
2. **The host item opens the code the gap is in.** "Next item" means the next one to open the
   file, not the next one on the board. An item whose plan has no reason to open that file will
   produce a diff with hunks that trace to somebody else's criteria, which is the thing
   `no-unplanned-scope` exists to ask about.
3. **It lands as a plan step, never as a new acceptance criterion.** The host item's criteria stay
   about the host item. Widening them to swallow work found elsewhere hides the change from the
   board and from whoever asked for the item
   [src: .claude/skills/answer-questions/SKILL.md].

**What it is not.** It is not a way to make a gap go quiet. Absent a dispatchable item that opens
that code, the disposition is a new item — an accepted gap is dispatchable or it is nothing
[src: .claude/agile-skills/spec/dor-dod.md], and filing one is a move the transition table
provides [src: .claude/agile-skills/pipeline.yaml] — and the cost of the round is the honest
price of the coverage. And a host item's plan may still decide the case does not belong in its steps — what it
may not do is drop it silently, because the gap was disposed as work rather than accepted as a
limitation. A limitation is a third thing, and it is recorded as one: `review.md`'s `no-owner`
rows are gaps somebody chose to live with, and they say why.

**The WI-0001 instance.** Both of WI-0001's gaps went to `BUG-0001`, which is `found-in: WI-0001`,
sits at `ready` with no plan yet, and is the item that opens `envel/store.py` next — the module that
holds both the defect it fixes [src: envel/store.py:58] and the untested path resolution
[src: envel/store.py:27]. `WI-0002` was the disposition the review recommended and is not the one
taken: it records income and spending against envelopes that already exist, so it opens neither
the creation path nor `store_path` [src: tracker/items/WI-0002/item.md].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-10T15:34:21Z | answer-questions | WI-0002 | `## Where an accepted test-coverage gap goes`, the *"What it is not"* paragraph: the sentence about what happens when the code a gap is in has no item to carry it now cites the rule it restates and the table that provides the move, and its opening clause is phrased *"Absent a dispatchable item…"* rather than as an absolute, because it is a condition evaluated per gap and not a claim over a family that anybody could enumerate. What the convention requires is unchanged (`WI-0002/Q-004`) |
| 2 | 2026-09-10T14:32:10Z | answer-questions | WI-0001 | `## Where an accepted test-coverage gap goes` added: a gap in a closed item's suite is carried by the next item that opens the code it covers, as a plan step and never as a criterion, with the three conditions that make that a real disposition. Written for `WI-0001/Q-004` |
| 1 | 2026-09-10T14:03:56Z | answer-questions | WI-0001 | First version: what an acting skill does when a hard gate refuses something no actor in the pipeline is permitted to fix, written for `WI-0001/Q-003` |
