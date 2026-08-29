# Final report — builder session three (the proven-kernel push)

Mission: `meta/BUILDER-3-PROMPT.md`. Plan: `meta/plan.md` Phase IV. Units META-119..META-131.

**Status of this document:** §1–§3 are complete and final. §4, §5 and §6 are written when the two
regression runs stop; until then this file says so rather than guessing.

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

*Pending: the run is in flight.*

## 5. Regression 4b — the boring run, audited

*Pending.*

## 6. The ROADMAP §2 verdict

*Pending. It is stated condition by condition, with the evidence line for each, when both runs
have stopped and their trails have been read.*
