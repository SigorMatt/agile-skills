# Review — EP-001

This execution **records the ending**. It is the answering half of the ask-and-stop review that
filed `EP-001/Q-009`: the stakeholder replied in the file, `scripts/engagement-state EP-001` still
reports `at-rest`, and the reply selects **E1 — delivered**. `EP-001` closes `done` with
`outcome: delivered`.

### What this file replaced, and why there have been four

`EP-001` has been reviewed four times and each review overwrote the one before it. Every one of
them survives in git and in `tracker/items/EP-001/journal.md`, which is append-only and untouched:

| review | commit | outcome |
|--------|--------|---------|
| first | `git show 53231b2:tracker/items/EP-001/artifacts/review.md` | **DE3 failed** — a success measure did not hold against the running tool. `BUG-0001` was filed and the engagement left rest |
| second | `git show e195053:tracker/items/EP-001/artifacts/review.md` | **DE6 failed** — four citations in `docs/` resolved without supporting their sentences. `Q-007` and `Q-008` were filed and the engagement left rest |
| third | `git show 495af63:tracker/items/EP-001/artifacts/review.md` | every criterion that can precede the ask passed; the sign-off `Q-009` was filed and the epic suspended |
| this one | — | the reply is in the file; the ending is recorded |

Three rests, four reviews, one file — the fourth being the second half of the third rather than a
fourth rest. That is `spec/question.md` §2's *"exactly one sign-off is due per rest"* working as
written. It is also the toolkit gap the third review named and this one confirms from the other
side: `review.md` is declared an output written *always*, an epic may legitimately reach rest more
than once **and** be reviewed twice within one rest, and nothing in the contract says whether the
later review appends, supersedes or replaces. Four executions chose *replace*; only this table
makes that visible to a reader who was not present. It goes upstream at `retro`.

## What I examined

- **`tracker/items/EP-001/questions/Q-009.md` in full** — the sign-off as it was asked, the
  stakeholder's reply, the `## Cross-answer check` `answer-questions` wrote against five prior
  answers, and the `## Consequences` naming what the reply reached. This is the artifact the whole
  ending rests on and it was read rather than summarised.
- **The reply against `## Options considered`.** They opened *"None of your four options is what I
  want"* and then wrote *"Ship it as it stands"* and *"Close this out without it."* Read against the
  options that is **A**, accept as complete, with B explicitly refused — *"I'm not spending a round
  on words in a report I've decided not to have."* Recorded below as the ending's determination,
  with the competing reading examined and rejected in `## Findings`.
- **The seven children's frontmatter, again rather than carried forward** —
  `grep -H "^status:\|^outcome:" tracker/items/*/item.md`: seven items, every one `status: done`
  with `outcome: delivered`, none `blocked`, none `dropped`.
- **Every question file in the engagement** — `grep -H "^status:" tracker/items/*/questions/*.md`:
  35 questions, all 35 now `answered`. None is `open`, so DE5's abandonment rule has no subject
  here; none is `deferred`.
- **`tracker/waiting/EP-001.md`** — one halt row, round 1 against a threshold of 3, recorded while
  `Q-009` stood open. The engagement ends at E1 and not at E4, and the log is what says so.
- **The two `## Engagement state` sections, enumerated by the gate rather than by eye**, and both
  restated below after the ending was determined.
- **`docs/product/vision.md` v9 → v10 and `docs/architecture/overview.md` v11 → v12** — read in
  full before editing, and only the `## Engagement state` section of each was touched.
- **The paragraph `answer-questions` added to `vision.md` at v9**, re-audited against the running
  tool rather than trusted, because it is prose written after the third review's DE6 sweep. The
  audit is below.
- **`envel/summary.py` `left_column()` and `balance_line()`**, opened at the lines the audited
  sentences cite.
- **`tracker/items/EP-001/artifacts/review.md` as the third review left it**, for the three gaps it
  carried and the enumeration it handed forward.

### The DE6 delta audit

The third review's sweep — `lint-claims --context epic --all` over the whole document set, all 27
line-bearing citations re-resolved one at a time — is not repeated here, and that is a scope
statement rather than an omission: no code has changed since (`git log` shows the last code commit
is `b5fd433`, before all three reviews), and `spec/dor-dod.md` §4a is explicit that re-auditing
after an acceptance is how F-086 cost an engagement a whole round. What **has** changed since is one
paragraph of prose, written by `answer-questions` under the stakeholder's own answer, and that
delta was audited by reading:

| claim | cites | opened | verdict | falsifier |
|-------|-------|--------|---------|-----------|
| *"A listing of a month an envelope started short opens with the same words — 'groceries was 250.00 short at the start of 2026-09'"* | `envel/summary.py:237` | the line, which is `return "{} was {} short at the {} of {}".format(`, inside `balance_line()` under `if cents < 0:` — and the tool itself: a store with `add groceries 400` and `spend groceries 250 --on 2026-08-15` printed `groceries was 250.00 short at the start of 2026-09` | **holds** | a month an envelope did **not** start short would print the other branch. It was run: a second store with `fun` and `add fun 100` printed `fun held 0.00 at the start of 2026-09`. The branch that could have made the sentence false was reached and produced different words, so the example could have failed and did not |
| *"the `left` column of an `envel summary` row for a month that closed short, reads `short 250.00`"* | `[src: EP-001/Q-009]`, and confirmed against `envel/summary.py:70`–`81` | `left_column()`, whose negative branch returns `"short {}".format(...)` and whose other branch returns `"left {}"` | **holds** | the non-negative branch is the falsifier and it was observed in the third review's own run — `left 30.00` in a `fun` row — so a column that read `short` unconditionally would have shown there |
| *"shown that line as one of two wordings the pipeline had chosen for itself, they kept it: 'reads fine to me'"* | `[src: EP-001/Q-009]` | the question's `## Answer`, which contains *"The listing line — \"groceries was 250.00 short at the start of 2026-09\" — reads fine to me"* verbatim | **holds** | had they written anything else there, or nothing, the sentence would be false on its face; the `## Answer` is the only thing it rests on and it was opened |

`lint-claims --context epic --changed-since main` → `0 errors, 0 warnings`, over *"every document
under `docs`"* and *"every markdown file in the workspace"* — re-run **after** the two engagement-
state restatements, so the scope contained this execution's own writing rather than only its
predecessors'.

## Definition of Done

`spec/dor-dod.md` §4, split by §4a. DE1, DE2, DE3, DE5, DE6 and DE4's first half were applied by the
third review **before** the sign-off's `## Question` was written, which is the ordering F-086 exists
to enforce; they are restated here with their evidence and with what this execution re-checked,
because the workspace moved between the two halves. DE4's restatement, DE7 and DE8 are applied here
for the first time.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, every undelivered child named | **pass** | `grep -H "^status:" tracker/items/*/item.md` → seven children, every one `done`; no child is `blocked` and none failed to deliver. All seven are named by ID in `Q-009`'s `## Question` anyway, which is the checkable half, and `check-epic-signoff` confirms it: *"names all 7 child item(s)"* |
| DE2 | every child's `outcome` recorded | **pass** | `grep -H "^outcome:" tracker/items/*/item.md` → seven lines, every one `delivered`. No child is `dropped`, so no `## Notes` reason is owed |
| DE3 | every success measure addressed | **pass** | eight measures, each decided by running the built tool in the third review — twelve invocations from a clean store, separate process each, quoted in `Q-009`'s `## Context` so the stakeholder saw the tool rather than a report of it. Unchanged here: no code has changed since, and the stakeholder's own reply confirms the same ground independently — *"I followed your commands line by line"* |
| DE4 (first half) | `docs/product/` reflects what was built | **pass** | `vision.md` was v8 when the third review read it in full against the run; it is v10 now. Both deltas were examined: v9's paragraph is audited claim by claim above and holds, and v10 is this execution's own restatement of `## Engagement state`, which is DE4's second half and not product prose. Nothing else in the document changed |
| DE4 (restatement) | every `## Engagement state` section restated, after the ending was determined | **pass** | `lint-documents --rule engagement-state-is-restated --item EP-001 --context epic` enumerates **2**; both are restated below and both were written **after** the reply was read and the ending determined as E1. `vision.md` v9 → v10, `overview.md` v11 → v12, each with a change-log row naming what was false and why it stood false |
| DE5 | open questions closed or re-filed | **pass** | 35 questions across the engagement, all 35 `answered`; `grep -H "^status:" tracker/items/*/questions/*.md \| grep -v answered` → no output. The thirty-fifth was `Q-009` itself, closed by `answer-questions` at 2026-09-11T19:13:47Z. Nothing is left `open` for the ending to close `abandoned`, and nothing is `deferred` |
| DE6 | every claim in `docs/` checked against the code this epic; every citation resolves | **pass, with one named survival** | the third review's full sweep — `lint-claims --context epic --all` → 0 errors, all 27 line-bearing citations re-resolved individually — plus the three-claim delta audit above for the prose written since. `lint-claims --context epic --changed-since main` re-run here after this execution's own edits → 0 errors, 0 warnings. The one survival is unchanged and is a decision rather than a defect: `ADR-0006`'s `2026-09-11T05:50:35Z` correction row cites `envel/envelopes.py:245`, cannot be repaired in place because `## Corrections` is append-only, and carries its erratum immediately below it under `ADR-0013` — the decided outcome of `EP-001/Q-008` |
| DE7 | the stakeholder was asked and answered | **pass** | `check-epic-signoff EP-001` → exit 0: *"carries the stakeholder's reply, names all 7 child item(s), and was filed after the engagement reached rest at 2026-09-11T11:57:12Z"*. `Q-009` is `kind: sign-off`, `addressed-to: human`, `blocking: true`, `answered-by: human`, `answered-at: 2026-09-11T19:11:25Z`. This is the *asked and answered* form, not E4's weakened one |
| DE8 | an elicitation was asked and answered | **pass** | `EP-001/Q-001`, `kind: elicitation`, `addressed-to: human`, `blocking: false`, filed by `intake` at 2026-09-11T01:58:15Z — at the beginning of the engagement, where an answer is worth most, rather than alongside the sign-off — and answered by the human at 2026-09-11T02:16:30Z. `check-epic-signoff` names it: *"DE8 satisfied by tracker/items/EP-001/questions/Q-001.md"*. It is `answered`, so neither the `abandoned` route nor the waiting-log surfacing requirement applies |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| — | not applicable — an ending has no plan and no invalidation set | D7 is an item-close criterion. This execution reviews no branch, no diff and no `plan.md`; the epic-level form of *did this change falsify a document the set does not name* is DE6, walked above |

*Did this execution falsify a document the set does not name?* It changed two documents, and only
the `## Engagement state` section of each — the sentences whose truth this very ending settles. No
product or architecture claim was touched, so nothing outside those sections could have been
falsified by it.

## Sections restated at the ending

Both, enumerated by `lint-documents --rule engagement-state-is-restated --item EP-001 --context
epic` rather than by eye, and both restated **after** the reply was read and the ending determined
as E1 — their answer is itself part of the engagement's state, so a restatement written before it
would describe an engagement that had not ended.

- **`docs/product/vision.md` `## Engagement state`** — restated, v9 → v10. It said the engagement
  had just begun, that nothing had been refined, designed, built, verified or accepted, that a first
  round of questions was unanswered, and that the stakeholder had not been asked to accept anything.
  All four were false and every one of them was `intake`'s, written at 2026-09-11T01:59:19Z and
  correct then. It now records the ending: E1 delivered, the seven children each closed `delivered`,
  the ask at `Q-009` and the reply that determined the ending, that all 35 questions are answered
  with none deferred or abandoned, and that what the stakeholder parked is further work rather than
  product.
- **`docs/architecture/overview.md` `## Engagement state`** — restated, v11 → v12. It said `WI-0001`
  was the first item to be designed, that nothing had been implemented, verified or accepted, and
  that no document had been checked against running code *"because there is none"*. All three were
  false and every one of them was `plan`'s, written at 2026-09-11T02:34:57Z before any code existed.
  It now records the ending, the thirteen ADRs the engagement took, that there is running code and
  that this document's claims have been read against it under DE6 — including that the second of the
  three audits failed and sent the engagement back to work, which is the part a restatement is
  tempted to leave out.

Neither restatement was a repair of something noticed in passing, and neither section was touched by
any execution between `intake` and this one: the change logs of both documents carry
*"`## Engagement state` was left untouched — it belongs to the ending"* on row after row, which is
the trail that makes this claim checkable.

## Findings

**None in the change, because an ending merges nothing.** What this execution had to decide instead
is what the reply means, and that decision is a finding worth recording because the reply did not
pick an option.

- **The reply is an acceptance, and the ending is E1.** *"Ship it as it stands"* is unambiguous, and
  every child delivered, so `delivered` does not overclaim. E2 would require something not to have
  delivered and nothing did; E3 requires a refusal and there is none; E4 requires withdrawal or
  silence and the reply is neither.
- **The competing reading was examined and rejected.** *"Close this out without it"* can be read as
  asking for `envel summary` to be taken out of the tool. It is refused on their own first sentence
  — *"Ship it as it stands"*, which includes the summary — on the fact that removal is work at the
  moment they asked for none, and on the sentence beside it, *"don't build on it, don't keep it open
  as work"*, which is about work rather than about the artifact. Recorded here, and in `EP-001`'s
  `## Notes` by `answer-questions`, so that a later reader meets the alternative reading and its
  refusal rather than only the conclusion.
- **The parking is not a failure of DE3.** Success measure 3 is the summary reconciling
  arithmetically, and it was met and stays met. What the stakeholder changed their mind about is how
  much more of their attention the summary is worth, which is not a measure this epic carries.
- **The three-times-repeated stale-citation pattern still goes upstream.** `[src: file:line]` going
  stale under an insertion was repaired three times in this engagement, across seven documents, at
  `WI-0005/Q-009`, `BUG-0001/Q-002` and `EP-001/Q-007`/`Q-008`. The grammar is
  `spec/doc-header.md` §4a's rather than this project's, so it is `retro`'s to carry, not a
  fourteenth ADR here.
- **One toolkit defect was reproduced by this execution, in a stronger form, and is named for
  `retro`.** A change-log row written by the execution that also writes the journal entry
  legitimising it cannot pass `doc.changelog.no-execution` at gate time: a window runs from the
  previous journal entry's stamp to this one's, and this one is written by the same transition that
  runs the gate. The previous turn recorded it for `answer-questions`, whose transition is never
  gated, so there the move proceeded and only the journal carried a `fail`. Here it falls on
  `review-close`'s **completion** transition, where hard gates block — so the rule does not merely
  misreport, it puts the legal move out of reach without an override. `--resolving` does not cover
  it, and the rule's own *"a row on a closed item is history"* exemption would moot both rows the
  instant `EP-001` is `done`, but the check reads the status as it stands when the gate runs. The
  rows are honest and were not restamped; the move was taken with `--force`, which records
  `[gates forced]` in the history reason for ever, every other gate having been run by hand and
  passed first. That is the precedent `plan` set on `WI-0003` for the same deadlock. Post-transition
  validation is clean.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| **The `left` column's `short 250.00`, which the stakeholder has now been shown and has declined to settle.** The third review carried it as a gap owed to the sign-off; the sign-off discharged it by naming it as ours and offering the change, and the stakeholder answered *"the summary column is parked with the rest of it and I'm not spending a round on words in a report I've decided not to have."* It is now a limitation they chose, not work anybody owes: filing a question or an item would re-open a decision they have just taken. The listing line beside it is no longer a gap at all — it is theirs, kept in their own words, and `docs/product/vision.md` records which of the two is which | `none` | `no-owner` |
| **`ADR-0006`'s `2026-09-11T05:50:35Z` correction row cites `envel/envelopes.py:245`, which no longer supports it**, and cannot be repaired in place because `## Corrections` is append-only. Its erratum sits immediately below it, appended under `ADR-0013`, quoting the row and naming `:171`, `:269` and `:275`, so a reader meets the wrong pointer and its correction in the same table in order. Nothing is owed: this is the decided outcome of `EP-001/Q-008` | `none` | `no-owner` |
| **`review.md` has been overwritten three times on this epic** — three rests produced four reviews, and nothing in the toolkit says whether a later one appends, supersedes or replaces. The prior three are preserved in git and named by commit in the table at the top of this file. Nothing is owed inside this project: it is a gap in the skill contract, and `retro` is the skill that sends such a finding upstream. The orchestrator dispatches it on its own once this epic has ended, so no filing is needed to make it reachable | `none` | `no-owner` |
| **A change-log row written by the execution that writes its own journal entry fails `doc.changelog.no-execution` at gate time, and on a completion transition that failure blocks the move.** Reproduced here for `review-close` after the previous turn reproduced it for `answer-questions`, where the transition is ungated and the move proceeded. This ending had to be taken with `--force`, following the precedent `plan` set on `WI-0003`. Nothing is owed inside this project — the workspace validates clean once the transition has been made — and it is a defect in the toolkit's rule rather than in this engagement, so it goes upstream at `retro` with the other three | `none` | `no-owner` |

## Verdict

**Accepted. The engagement ends at E1 — delivered.**

The stakeholder was asked whether they accept the engagement as it stands, after it reached rest,
and answered *"Ship it as it stands"* [src: EP-001/Q-009]. Every Definition of Done criterion is
recorded above with its own result and its own evidence: DE1–DE6 and DE4's first half against the
state they were shown, DE4's restatement, DE7 and DE8 against the ending itself. All seven children
closed `delivered`, so `outcome: delivered` says what happened without overclaiming.

`EP-001` moves `open → done`, `outcome: delivered`. What remains for the pipeline is `retro`, which
the orchestrator dispatches on an ended engagement without anybody being asked for it, and which is
where the four findings named above leave this project.
