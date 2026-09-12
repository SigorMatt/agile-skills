---
title: A gate that nobody is permitted to clear is overridden once, visibly, and named
version: 3
status: current
updated: 2026-09-11T22:58:23Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0004 — A gate that nobody is permitted to clear is overridden once, visibly, and named

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001/Q-002` reports that `implement`'s `claims-are-sourced` gate fails on two unsourced
absolute claims in `docs/product/vision.md`, neither written by `WI-0001`. The gate runs
`lint-claims --changed-since main --plan-documents WI-0001`, and `--plan-documents` puts the
whole of `vision.md` in scope because `WI-0001`'s plan names three of its sentences in the
invalidation set — correctly, since this change falsifies them.

The two claims are not alike, and the difference is the whole decision.

- **`docs/product/vision.md:42`**, in `## What it is for`. An ordinary product sentence, reported
  unsourced [src: run: python3 .claude/agile-skills/scripts/lint-claims --all → exit 1, claim.unsourced at docs/product/vision.md:42].
  `answer-questions` is a listed updater of `vision.md`, so this one is repairable here and has
  been repaired [src: docs/product/vision.md].
- **`docs/product/vision.md:66`**, inside `## Engagement state`. This one has **no permitted
  repairer before the ending.** `intake` writes the initial section; `review-close` restates
  every section at the ending; nothing in between writes one. `implement` is forbidden at any
  disposition, and so is this skill — its own procedure says so in terms, and the prohibition
  exists because a real run had two executions correct such sentences, both declared, both
  defensible, and both authorised by nothing. `review-close` at an **item** close does not reach
  it either: its restatement rule reports *not applicable* there rather than running.

So the sentence is uncitable until the engagement ends, and the gate that demands a citation runs
long before that. Three facts have to hold at once and cannot: the plan must name the document,
naming it puts the whole file in the gate's window, and the section is nobody's to write.

This is the shape of a rule that cannot be satisfied — the failure mode where a regression run
ended with a forced hard gate over three sentences a reviewer had read and found true. The
difference here is that the toolkit already provides the escape and asks for it to be visible:
`scripts/transition --force` skips the gate run and writes `[gates forced]` into the history
reason, *"so an override is visible in the record forever rather than being indistinguishable from
a clean pass"* [src: tracker/items/WI-0001/questions/Q-002.md].

## Options considered

- **A — repair `:42` here, and authorise a single bounded override of `claims-are-sourced` on
  `WI-0001`'s completion transition for the single error that remains.** Cost: one history row
  carrying `[gates forced]` for the life of the project, and a journal entry that has to carry
  the surviving lint output so the bound is checkable. Risk: `--force` skips **every** gate
  rather than the one that cannot pass, so the other eight stop being run by the transition — a
  real loss, mitigated below rather than waved away [src: WI-0001/Q-002].
- **B — repair both sentences here.** Cost: none mechanically; the edit is one citation. Refused:
  it is the specific act two prohibitions forbid, and the reason they forbid it is that the
  sentence is about the engagement and the engagement is not over. Being the only one looking is
  the argument this rule was written to defeat.
- **C — take `docs/product/vision.md` out of `WI-0001`'s invalidation set, so the gate's window
  no longer contains it.** Cost: none up front. Refused: the three rows are the honest output of
  the rule that says a plan enumerates what its change makes false, and one of them exists
  precisely so the ending finds a sentence sitting *outside* the delimited section. Deleting a
  true row to quiet a lint is the failure the invalidation set exists to prevent.
- **D — leave `WI-0001` at `awaiting-answer` until the ending clears the sentence.** Cost:
  deadlock. The ending cannot come before the work finishes, and the work cannot finish before
  the ending. Refused as unexecutable rather than as undesirable.
- **E — escalate to the stakeholder.** Refused: none of the four escalation conditions applies.
  This is not their intent, not an irreversible product commitment, and not a contradiction with
  a decision they took. It is a collision between two of the toolkit's own rules, and spending
  their attention on it would be the failure mode the routing test exists to prevent.

## Decision

1. **`docs/product/vision.md:42` is repaired now**, by this execution, as a provenance repair: the
   assertion is unchanged and it gains a citation to the stakeholder's own words about what makes
   the number believable. `vision.md` goes to v4 with a change-log row
   [src: docs/product/vision.md; WI-0001/Q-001].
2. **The `## Engagement state` claim is not repaired by anybody before the ending.** It is already
   carried in `WI-0001`'s invalidation set, disposed `owned-by-ending`, which is the disposition
   that names who owns it.
3. **`implement` is authorised to make `WI-0001`'s `in-progress → verifying` transition with
   `--force`, under four conditions, all of them checkable by `verify` and `review-close`:**
   - it first runs `scripts/run-gate --skill implement --item WI-0001 --all --resolving
     'WI-0001:in-progress->verifying'` and records **every** verdict that run produced in its
     journal entry, which is what replaces the gate run `--force` skips
     [src: tracker/items/WI-0001/artifacts/impl-report.md];
   - `claims-are-sourced` is the only hard gate reported failing;
   - its failure is exactly one error, and that error is **the one described below**, quoted in
     the journal entry verbatim as the run printed it;
   - the history reason names this ADR.

   If any of the four does not hold — a second error appears, another gate fails, a different
   claim fails — the authorisation does not apply and the item stays at `in-progress`. The bound
   is the point: an override that grows to cover whatever happens to be failing is not an
   override, it is the gate being switched off.

   **Which error condition 3 admits, and how to check it — amended at v2, see `WI-0001/Q-003`.**
   Four properties of the reported error, and a line number is not among them:

   | property | value |
   |----------|-------|
   | code | `claim.unsourced` |
   | file | `docs/product/vision.md` |
   | section | `## Engagement state` |
   | sentence | *"Three questions are open with them, all filed at intake"* — reported as an absolute claim `'all'` about `'EP-001/Q-001'` |

   v1 of this ADR wrote the fourth property as `docs/product/vision.md:66` and listed *"the error
   moves"* among the disqualifiers. That was a defect in this document, and `WI-0001/Q-003` caught
   it before it cost anything: the number `lint-claims` prints is not a property of the claim. Rule
   2 iterates `paragraphs(text)` and reports at the chunk's **first** line, and `paragraphs`
   *"deliberately does **not** split on bullets"*
   [src: toolkit: scripts/lib/record.py paragraphs() "deliberately does **not** split on bullets"], so what
   is printed is the offset of the whole `## Engagement state` bullet list, which shifts whenever
   anything above it changes length. Between v1 and v2 it went from `:66` to `:67`, because the
   execution that wrote v1 rephrased `## What it is for` from two lines to three in the same breath
   [src: commit b545273]. Nothing about the claim changed.

   Anchoring the bound on the sentence rather than on the coordinate **narrows** it: v1 did not say
   which sentence was admitted, and the table above does. What it stops disqualifying is a shift in
   a number that belongs to the file's layout rather than to the failure
   [src: run: python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0001 → exit 1, 1 error, claim.unsourced at docs/product/vision.md:67].
4. **`review-close` is authorised to make `WI-0001`'s `in-review → done` transition with
   `--force`, under four conditions of the same shape — added at v3, see `WI-0001/Q-004`.** The
   override in point 3 named one skill and one transition, deliberately. It turned out that the
   same wall stands at the item close, and that `review-close` has even less room than `implement`
   did: it may not repair the sentence, its own restatement rule reports *not applicable* at an
   item close rather than running, a send-back would put `implement` in front of the identical
   wall, and superseding an ADR is not its move
   [src: tracker/items/WI-0001/questions/Q-004.md].

   The four conditions are point 3's, re-aimed:

   - `review-close` first runs `scripts/run-gate --skill review-close --item WI-0001 --all
     --resolving 'WI-0001:in-review->done'` and records **every** verdict that run produced in its
     journal entry, which is what replaces the gate run `--force` skips [src: ADR-0004];
   - `claims-are-sourced` is the only hard gate reported failing;
   - its failure is exactly one error, and that error matches the four properties in point 3's
     table — code `claim.unsourced`, file `docs/product/vision.md`, section `## Engagement state`,
     sentence *"Three questions are open with them, all filed at intake"* — quoted in the journal
     entry verbatim as the run printed it. The line number is not one of the properties, for the
     reason point 3 already gives;
   - the history reason names this ADR.

   If one of the four does not hold, the authorisation does not apply and the item stays at
   `in-review` [src: ADR-0004]. **This is a second bounded override, not a widening of the first.** Each names its
   skill and its transition, which is the property that makes an override reviewable; an
   authorisation that covered "whatever is failing on `WI-0001`" would be the gate switched off,
   which point 3 already refuses in those words.

   **A later item meeting the same shape gets its own decision, not this one.** The two
   authorisations here are written against `WI-0001` and name its two transitions; neither names
   another item [src: ADR-0004]. The reason is in point 4a: for a later item the failure is
   unlikely to recur at all, so a blanket authorisation would buy a standing exemption to avoid a
   problem that has probably gone away.

4a. **Why the close failed is not why the transition failed, and the difference bounds this.**
   `implement`'s gate runs `lint-claims --changed-since main --plan-documents WI-0001`
   [src: toolkit: skills/implement/references/contract.md Quality gates "`lint-claims --changed-since {{trunk}} --plan-documents {{item.id}}`"];
   `review-close`'s runs `lint-claims --context work-item --changed-since main`, with **no**
   `--plan-documents`
   [src: toolkit: skills/review-close/references/contract.md Quality gates "`lint-claims --context {{item.type}} --changed-since {{trunk}}`"]. So the reasoning in `## Context`
   above — that the plan naming `vision.md` is what puts the file in the window — explains
   `implement`'s failure and **not** this one.

   What puts `vision.md` in `review-close`'s window is that it differs from the trunk. The run
   says so itself: *"3 document(s) in 3 path(s) differ from main (6788e55) under docs"*, and the
   three paths are `vision.md`, `overview.md` and this ADR
   [src: run: git diff main..HEAD --name-only -- docs → docs/architecture/adr/ADR-0004-an-engagement-state-sentence-can-block-a-gate-nobody-may-clear.md, docs/architecture/overview.md, docs/product/vision.md].
   `vision.md` differs because **point 1 of this decision ordered the `:42` repair**. The repair
   that cleared one unsourced claim is what dragged the file into a later gate's scope, where the
   second claim — the one point 2 leaves standing — was waiting. That is worth stating plainly:
   this second failure is a consequence of this ADR, not an independent collision.

   It also bounds the blast radius, and this is the sentence to carry upstream. Once `WI-0001`
   merges, `vision.md` is on the trunk, so a later item's branch that does not itself edit it
   leaves it outside the `--changed-since` window that `review-close`'s gate uses. `implement`'s
   gate is the one that would still reach it, through `--plan-documents`, and then for an item
   whose plan names the file [src: ADR-0004].

5. **The surviving error is the ending's inbox, not a defect to forget.** At the ending,
   `review-close` restates every `## Engagement state` section it finds; restating this one is
   what clears the claim. This ADR is the record that somebody looked, decided, and bounded it.

## Consequences

- `WI-0001` can finish. Without this it could not, at any level of effort, which is the property
  that made the question worth an ADR rather than a note.
- The project carries one forced gate in its history, findable by reading the row. That is the
  intended cost and it is smaller than either alternative — an unfinishable item, or a
  prohibition quietly broken by the skill that noticed.
- **`--force` skipping the whole gate run is the real risk**, and condition 1 is the whole of the
  mitigation: the verdicts recorded are the ones a run produced, immediately before the move,
  rather than the caller's recollection [src: WI-0001/Q-002]. A reader who doubts them can re-run
  the same command.
- **Reversible, and cheaply.** Nothing about the product changes. When the ending restates
  `## Engagement state`, the sentence gains its citation and `lint-claims --all` goes clean; this
  ADR then describes a situation that no longer exists, which is what an ADR is for. If the
  toolkit instead grows an exemption — `lint-claims` skipping `## Engagement state` sections,
  which it does not have today — the authorisation simply stops being needed and no code moves.
- **This is worth sending upstream.** The general statement is: `--plan-documents` widens the
  claims window to whole documents, while the engagement-state rule narrows every mid-flight
  skill's write permission to a sub-section of them, and the two boundaries do not line up. Any
  item whose plan names a document with an unsourced absolute in its `## Engagement state`
  section meets this, whatever that item changed.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T22:58:23Z | answer-questions | WI-0001 | Answering `WI-0001/Q-004`: a second bounded override added as point 4, for `review-close`'s `in-review → done` transition on `WI-0001`, under four conditions of the same shape as point 3's — because the same wall stands at the item close and the override in point 3 names `implement` and one transition. Point 4a records why the close failed for a **different mechanical reason** than the transition did: `review-close`'s gate carries no `--plan-documents`, so `vision.md` is in its window only because the file differs from the trunk, which point 1's own repair is what made true. The old point 4 is renumbered 5; nothing in points 1, 2, 3 or 5 is changed |
| 2 | 2026-09-11T22:32:40Z | answer-questions | WI-0001 | Answering `WI-0001/Q-003`: condition 3 is re-anchored. It quoted the admitted error as `docs/product/vision.md:66` and listed *"the error moves"* as a disqualifier, but the number `lint-claims` prints is the first line of the blank-line-separated chunk the claim sits in, not the claim's own line — so it shifted to `:67` when v1's own execution rephrased a paragraph higher up the file. The condition now names the code, the file, the section and the sentence, which is what `verify` and `review-close` can compare. The decision, its scope and the other three conditions are unchanged |
| 1 | 2026-09-11T22:19:26Z | answer-questions | WI-0001 | First version: answering WI-0001/Q-002 — vision.md:42 repaired here, vision.md:66 left to the ending as the only actor permitted to touch it, and a bounded override of claims-are-sourced authorised for WI-0001's completion transition under four checkable conditions |
