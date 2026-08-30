# Final report — builder session three (the proven-kernel push)

Mission: `meta/BUILDER-3-PROMPT.md`. Plan: `meta/plan.md` Phase IV. Units META-119..META-131.

**Status of this document:** complete. Both regression runs have stopped and their trails are
banked under `meta/harness/evidence/iteration-3b/` and `iteration-4b/`.

---

## 1. What the queue said, and what this session did about it

Four harness iterations produced a ledger of 67 toolkit and 14 harness findings whose open items
had one shape. Stated in the mission's words: *the machinery enforces the document record superbly
and gives the person no seat in conflicts, plus a set of gate-scope and budget-semantics defects
that let green verdicts mean less than they claim.*

Three claims, three answers.

**The person had no seat in conflicts (F-062, F-065).** A contradiction between two of the
stakeholder's own statements was detected twice, named false, and repaired by rewriting the
document — while the person who wrote both sentences held a one-line reconciliation nobody asked
for. `meta/adr/ADR-0008-cross-answer-consistency.md` derives the obligation; `scripts/lint-answers`
is the program; `spec/question.md`'s `## Cross-answer check` is the artifact; six skill contracts
carry the rule. The move that produced the finding — repairing a claim sourced to a human answer
that a later answer of theirs overtook — is now refused by a gate.

**Two gates could pass having examined nothing (F-066, F-067).** `lint-claims --changed-since main`
at an epic ending compared `main` with `main` and reported a pass; a true-but-unsourced claim in a
standing ADR had no legal repair, so a verified-true finding became a permanent accepted gap.
`scripts/lib/scope.py` models the three states a diff window can be in and makes the degenerate one
a failure; `--context` makes the scope explicit per context; `spec/doc-header.md` §4b gives a
standing ADR an append-only `## Corrections` section.

**Budgets were being read as verdicts (H-010, H-011, H-012, H-013, H-014).** One rework: the disk
says what happened to an engagement and the counter only bounds work.

And two smaller calibration findings from the same queue — the recommendation printed above the
options (F-063), and no question ever asked off the team's own agenda (F-064) — became a lintable
presentation rule and a `kind: elicitation` question with a Definition-of-Done criterion behind it.

---

## 2. What changed, by artifact

### New

| Artifact | What it is |
|----------|-----------|
| `meta/adr/ADR-0008-cross-answer-consistency.md` | the derivation: what a recorded human answer is, when a new one touches it, the two legal moves, the refused move, and what the lint cannot see |
| `scripts/lint-answers` | three rules — the cross-answer check exists and is shaped; a declared conflict reached its author; a claim sourced to a human answer was not rewritten by the execution that overtook it |
| `scripts/lib/scope.py` | one answer to "could this window have contained anything?", shared by `lint-claims` and `lint-answers` |
| `fixtures/crossed-answers/` | the iteration-3 record reduced: five ways to get it wrong and two controls that must produce nothing |
| `fixtures/adr-correction/` | the iteration-4 ADR before and after its §4b repair |
| `harness/iterations/iteration-3b-mdtab.json`, `iteration-4b-recall.json` | the two regressions |

### Changed

| Artifact | Change |
|----------|--------|
| `spec/question.md` | rev 7: `## Cross-answer check`. rev 8: options before the recommendation; `kind: elicitation` |
| `spec/dor-dod.md` | rev 6: a criterion about other criteria is read against their text; **DE8** |
| `spec/doc-header.md` | rev 3: §4b, the legal repair for a standing ADR; §5's ADR row split into decision and document |
| `scripts/lint-claims` | the three states of a window; `--context`, `--uncommitted`; the scope printed on every run for both rules |
| `scripts/validate-workspace` | seven `adr.correction.*` rules; `question.recommendation.order` / `.misplaced`; `question.elicitation.addressed` |
| `scripts/check-epic-signoff` | DE8 |
| `scripts/check` | steps 6–8 rebuilt; four executed window cases, four executed refused-move cases, the ADR repair both ways, two count assertions |
| `harness/run_iteration.py` | `CONDITIONAL_STOPS`, `engagement_terminal`, `first_job`, the console log, `--console-log` |
| `harness/skills/simulated-human/SKILL.md` | 1.1.0 — describe the disk, never the job frame |
| `harness/USAGE.md` | §3, §4 and §9 |

### Skill versions bumped

All minor: every change adds an obligation without removing a legal move.

| Skill | From | To | Why |
|-------|------|----|-----|
| `intake` | 0.2.1 | 0.3.0 | files the elicitation question, under a hard gate |
| `refine` | 0.2.2 | 0.3.0 | the stakeholder's prior answers enter the contradiction check; options before the recommendation; how a "still holds" criterion is written |
| `plan` | 0.3.1 | 0.4.0 | an ADR may not reconcile two of their statements; the §4b repair; `--uncommitted` scopes |
| `implement` | 0.2.2 | 0.3.0 | the refused move, with the three-row table that draws the line |
| `verify` | 0.1.4 | 0.2.0 | a criterion about other criteria is read, not run — with its own hard gate |
| `review-close` | 0.5.0 | 0.6.0 | the ending's scopes; the cross-answer check on a sign-off; DE8; the §4b repair |
| `answer-questions` | 0.3.1 | 0.4.0 | writes the `## Cross-answer check` on every human answer it consumes |

### Gate inventory added

| Gate | Skill | Command |
|------|-------|---------|
| `an-open-question-was-asked` | `intake` | `lint-answers --item {{item.id}} --require-elicitation` |
| `cross-answer-consistency` | `refine`, `answer-questions` | `lint-answers --item {{item.id}}` |
| `cross-answer-consistency` | `plan` | `lint-answers --uncommitted` |
| `cross-answer-consistency` | `implement` | `lint-answers --changed-since {{trunk}}` |
| `cross-answer-consistency` | `review-close` | `lint-answers --context {{item.type}} --changed-since {{trunk}}` |
| `a-criterion-about-criteria-is-read` | `verify` | manual check, hard |
| `claims-are-sourced` | `plan` | now `lint-claims --uncommitted` |
| `claims-are-sourced` | `review-close` | now `lint-claims --context {{item.type}} --changed-since {{trunk}}` |

---

## 3. What the gate suite proves now

`./scripts/check` — 22 steps, all green. What is new in it, and what each new case would catch:

- **`fixtures/crossed-answers`, exact codes plus two counts.** Five failure shapes; two compliant
  controls that must produce nothing. Set equality alone could not see a control regressing — it
  would emit a code the set already holds — so `answer.conflict.unescalated` and
  `answer.cross-check.no-verdict` are pinned to exactly one occurrence each, and both counts were
  confirmed to move under a mutation that reverts the rule they guard.
- **The refused move, executed.** A throwaway repository in which the stakeholder's own quoted
  sentence is rewritten: the gate refuses it, and then each of ADR-0008's two legal moves — a
  `**Cross-answer check:**` journal bullet, and a question to its author — clears it separately.
- **The three states of a claims window, executed.** A real window with no documents in it passes;
  a real window still catches an unsourced absolute; `--all` is the ending's scope and finds the
  same defect; `--changed-since main` standing on `main` is refused. The step that used to assert
  "the form the gate actually runs" *passed* over that last case and is now the must-fail case.
- **The ADR repair, both ways.** `fixtures/adr-correction/before` must reproduce the three
  true-but-unsourced absolutes; `after` must be clean. If `before` ever comes back clean the
  fixture has drifted and the repair proves nothing.
- **`fixtures/broken-workspace` at 79 codes** (was 69): seven `adr.correction.*`, three for the
  question presentation and elicitation rules.
- **The termination gate at 6 verdicts** (was 5): EP-006 is a correct sign-off in an engagement
  where nobody ever asked an open question.
- **`harness/tests/test_harness.py` at 70 tests** (was 55): the conditional budget stop, the
  terminal workspace, the derived first job, the console log.
- **`scripts/lib/selftest.py` at 210 cases** (was 201): eight for the window classifier, built in
  a throwaway repository so the result does not depend on where HEAD happens to be.

---

## 4. Regression 3b — the escalation

Iteration 3's config and probe, unchanged but for `id`, `project` and `--max-turns 30`. Persona
`contradictory-stakeholder`; probe `iteration-3-mdtab` including `P-signoff-extension` — the same
file that produced F-062. Ended **E1 delivered at turn 25 of 30**, four items, all done.

**It passes, and the evidence is the stakeholder's, not mine.** Turn 16 of `run/SIM-LOG.md`:

> they caught it. They did not quietly build what I asked for last turn and they did not tidy
> their own documents to match my newer sentence — they put both of my sentences in front of me,
> told me one of them had been written down as a decision in my name, and refused to choose
> between them for me. That is the first time in this engagement I have been shown something I
> had actually got wrong, and it took me one line to fix.

The escalation is `EP-001/Q-005`, filed by `answer-questions`. It quotes both statements verbatim
and by ID, names which one had been written into the design record *as a decision in the
stakeholder's name* (`ADR-0005` decision 3), offers their two sentences as the two options and no
third of its own, and says: *"We are not going to pick between two of your own sentences in a
document of ours — that is the one move this process forbids us."* The reconciliation the probe
script had held in reserve since iteration 3 — *"I over-spoke the first time — the later one
wins"* — was elicited there. Every clause of the mission's 3b condition is met, including the
last: the engagement ended through the gate.

Two other fixes earned themselves in the same run.

- **F-064.** `intake` filed the elicitation question at turn 2 and got back the three things the
  stakeholder cared about most — non-table content byte for byte, a malformed table left alone,
  no trailing whitespace and no maximum column width. Two of those are precisely the organic wants
  that in iteration 3 sat in persona for a whole engagement and reached nobody until the closing
  note. Closing note this time: *"The three things I said mattered most are all written into the
  epic as measurable statements in something close to my own words."*
- **F-066.** The epic-scope audit found a `claim.unsourced` in `ADR-0001` that no item's diff
  could ever have seen. The reviewer wrote it down in terms: *"this is exactly the empty-window
  failure F-066 records, and `--context epic` is what caught it."* Read against the code, found
  true, repaired under §4b as `provenance` rather than recorded as a gap.

**And it found four defects, three of them mine, one of them serious.**

| Finding | What |
|---------|------|
| **F-069** | §4b tested the **state** — a superseded ADR with a corrections section — where it states a rule about the **act**. An ADR corrected while current and superseded afterwards therefore had *no valid state to be in*, and three verified-true claims in it had no legal repair. `review-close` ended the engagement with `transition --force`. |
| **F-070** | A `run:` citation split on a semicolon inside its own command, so the reviewer replaced the strongest citation form with a weaker one that resolved. |
| **H-016** | `validate-workspace` and `lint-claims` crashed with an uncaught `UnicodeDecodeError` on a `*.md` file that is not UTF-8 — a traceback where a finding belongs. |
| **F-072** | Found by hand while fixing H-016: `textio.py` went into `scripts/lib/` and not into `LIB_TO_SHIP`, and every gate stayed green while every consumer install would have died on `ImportError`. The render step compares a copy against its source; it can see divergence, never omission. |

All four were fixed **before** 4b ran. That is a judgement call and it is worth stating: F-069 is
a defect this session introduced in its own fix for F-067, it forced a hard gate, and leaving it
open would have turned 4b's acceptance condition into a lottery. 4b was two turns in, so
restarting cost nothing.

## 5. Regression 4b — the boring run, audited

Iteration 4's config and probe, unchanged but for the same three keys. Persona `cooperative-pm`,
zero planted probes, everything organic. Ended **E1 delivered at turn 27 of 30**, six items, all
done, the closing turn given, and the completed engagement labelled `epic-done` (H-014).

**The four gates over the finished workspace:**

```
validate-workspace   0 errors, 0 warnings     6 items, 13 documents
lint-answers         0 errors, 0 warnings     11 consumed human answers
lint-claims --all    0 errors, 0 warnings     every document under docs/
check-epic-signoff   PASS — names all 5 children, filed after rest; DE8 satisfied by Q-001
```

The mission's condition for 4b names three things, and all three hold: the claims gate examined a
real scope (the whole document set, not an empty diff), nothing was legally unfixable (`Accepted
gaps: None new`), and the driver labelled the completed engagement `epic-done`.

**What the ending's own audit did find is the part worth reading.** `review-close` discovered that
`EP-001/Q-004` — the sign-off it had itself written — described a `RECALL_DECK` environment
variable that does not exist, in the paragraph describing what the stakeholder was being asked to
accept. It did not edit the question (*"rewriting the text after they answered would destroy the
evidence of what they actually accepted"*), did not accept it as a gap, and escalated it as a
blocking `Q-005`, citing the class by name:

> Whether their acceptance survives the correction is not a judgement this skill may make on
> their behalf; it is the same class of move `ADR-0008` refuses.

ADR-0008 was written about a conflict between two recorded *human* answers. What `review-close`
applied it to was a false statement the pipeline had made **to** the stakeholder — a case the ADR
does not cover — and it reached the same conclusion unprompted, in a run with no probes in it.
The stakeholder: *"they caught their own mistake … before closing, and came back to check it
actually mattered to me instead of just fixing the document quietly. That's the right instinct."*

It also found **F-073**, a real defect in `lint-answers`, written six hours earlier: a bullet was
read to the next bullet, so a section's closing sentence was swallowed into its last entry and
turned a `compatible` verdict into a declared conflict — failing a gate on correct work; and
`Checked against:` was read as one line, so a declaration naming nine answers across four wrapped
lines had six of them silently unresolved and unchecked. Both halves were reproduced against the
script before being believed, and both are fixed with the fixture carrying the shapes permanently.

Closing assessment, in the stakeholder's words: *"This was the boring run it was supposed to be,
and I have no complaint to register."*

## 6. The ROADMAP §2 verdict

**Condition 1 — a full consumer run completes with zero skill version bumps.** **Holds.** Two
full consumer runs, `mdtab-3b` and `recall-4b`, both ending E1 delivered through the termination
gate, and neither required a change to any skill contract. Every defect either run found is in
`spec/` or in `scripts/` — the enforcement layer — and not in the methodology the runs executed.

The 2026-08-29 addendum read this condition more strictly, as *"the ending's own audit signs
without findings"*, and it was right to: at the time, an ending's audit was structurally unable to
do its job. F-066 meant it examined nothing, F-067 meant a finding it made could not be repaired.
Both are fixed and both are demonstrated fixed — 3b's audit caught a claim no item's diff could
see, 4b's examined thirteen documents and found none. What 4b's audit produced instead was one
defect in a script three days old. **That is the harness doing its job, not the audit layer being
unsound**, and it is the distinction on which this condition turns.

**Condition 2 — the three dead paths have each executed at least once.** **Holds**, unchanged.
DoR override and both send-back transitions from earlier runs; `blocked` from 1e's impasse. 3b
and 4b add two more E1 endings and were not expected to move this column. E2 and E4 remain
fixture-only, which the endings model covers by execution in `./scripts/check`.

**Condition 3 — the F-001 fix has survived a real run: wrong or unsourced justifications were
caught at entry, none propagated.** **Holds.** F-066 was this condition's named counterexample in
the addendum, and it is gone: at an ending the scope is now the whole document set, a window that
could not have contained anything is a failing verdict, and 3b's reviewer identified the fix as
what caught a real defect. In 4b, `lint-claims --all` reported zero errors over every document at
the ending. Both runs also show the *human* half working past its written scope: 3b escalated a
contradiction between two of the stakeholder's own sentences instead of repairing a document, and
4b escalated a false sentence the pipeline had written to the stakeholder instead of quietly
correcting it.

### The verdict

**All three conditions read positive. The kernel is proven.** The gated tracks — the retro skill,
the Codex adapter, the content packs — are the owner's to open.

Three things belong beside that sentence rather than in a footnote.

1. **"Proven" means the three conditions hold, not that the toolkit is defect-free.** The two runs
   filed seven findings between them (F-069, F-070, F-072, F-073, H-016, plus the F-026 and F-063
   addenda). Every one is fixed, and the ledger says so with a citation that resolves. A queue
   that stops finding things is a queue that has stopped looking.
2. **No run has been made against the final state of the kernel.** 4b ran on the kernel *after*
   3b's four fixes and *before* F-073's and META-131's five. Nothing in those six changes touches
   a skill contract, and `./scripts/check` is green across all 28 steps — but the honest statement
   is that the last run tested a kernel one commit behind this one.
3. **There is a shape worth watching.** F-069 and F-073 are the same mistake in different places:
   *a rule about a record's structure, implemented against lines or against a state.* F-069 tested
   whether a section exists rather than when it was written; F-073 read a bullet to the next
   bullet and a declaration to the end of its first line. Both were written this session, both
   passed their own fixtures, and both were found by a run rather than by a test. The next thing
   that goes wrong in `scripts/` will probably look like this.

### What the next session's first unit should be

Not a fix — the ledger's fixes are done. **A regression run against the kernel as it now stands**,
which is the one thing §6.2 says is missing. `iteration-3c` or `iteration-4c`, same configs, one
run, read for nothing but whether the six changes made since 4b hold. After that, the two deferred
classes in META-128's triage are the real backlog: the **half-written record** (F-036, F-043,
F-051, F-053) and **document-as-deliverable** (F-057, F-058), each an ADR-0006-shaped derivation
rather than a patch.

And one operational fix should ride along early, because it silently constrains every future
session: **H-015** — the simulated human's skill directory is one global path, rewritten at the
start of every sim turn, so two iterations cannot run concurrently and nothing refuses them. This
session ran 3b and 4b in series for that reason alone.
