# Builder session 2.5 — mission kickoff prompt

Location when adopted: meta/BUILDER-2.5-PROMPT.md. Paste everything below the line into Claude
Code at the repository root.

---

You are builder session 2.5 of **agile-skills** — a compact fix session between builder two
and iteration 2 of the queue. Builder two fixed 38 findings and its regression run (1d) filed
24 more; 14 findings remain open. Your mission: close the ones that would corrupt iteration
2's evidence, and fix the structural class behind the pipeline's repeating contradictions —
then prove both on a short regression run.

Read first: `meta/findings/FINDINGS.md` (your backlog is exactly the findings with
`Status: open`), `meta/FINAL-REPORT-2.md`, `meta/ROADMAP.md` §2, and the 1d evidence under
`meta/harness/evidence/iteration-1d/` for anything you touch. All standing discipline applies
(CLAUDE.md, checkpoint write-ahead, small pushed commits, journal+ADRs, restart protocol,
findings statuses updated as you go, every fixed citing a real commit — step 11 checks).
Continue META-### numbering. Banked evidence and filed findings text remain read-only;
corrections append.

## The centerpiece: derive the termination model (fixes the F-013 class)

F-013, F-029, F-045/F-046 are one design debt surfacing three times: the status graph and
authority rules were derived from the happy path, and every non-happy ending finds a
contradiction (an epic that could not suspend; skills that legitimately need to create items
and may not; a sign-off gate that only fires on the ending where it matters least). Do the
derivation once, properly:

1. **Enumerate every legal ending of an engagement** in `spec/` (at minimum: delivered;
   delivered-partial with blocked/deferred children; impasse; abandoned-by-stakeholder), and
   every legal mid-flight event that changes the item set (scope widened by an answer; work
   discovered by review; a bug filed; a stakeholder request via F-021's channel).
2. **Require that every ending passes through stakeholder acknowledgment** — the F-022 gate
   generalizes from a completion gate to a termination gate: no engagement ends, in any
   ending, without a blocking human-addressed question stating what was delivered, what was
   not, and why. An impasse is an ending (F-045); a pipeline-filed bug left open at the end is
   part of the statement (F-046).
3. **Derive pipeline.yaml's status graph and a creation-authority table from that
   enumeration** (who may create items, in which states, with what provenance — resolving
   F-029/F-042 by rule rather than by exception), and re-derive the affected skill contracts
   (review-close, answer-questions, next) from the result.
4. **Re-check every historical contradiction against the derived model as must-fail/must-pass
   fixtures**: F-013's epic suspension, F-029's two occurrences, F-045's impasse, F-046's
   unshown bug. Record the derivation as an ADR; it supersedes patch-thinking on this class.

## The correctness batch (evidence integrity for iteration 2)

Work every remaining `Status: open` finding in this set, in roughly this order:
- **F-044** if still open — silent corruption of `history.md` outranks everything.
- **F-025** (a hard gate unsatisfiable on a legal path), **F-047** (closing breaks on an
  empty `questions/`), **F-032** (a filed question with nowhere to put the answer — the
  stakeholder's first touchpoint), **F-028** (deferred answers representable; protects the
  F-011 fix — and note iteration 2's persona defers and deflects by script, so this fires
  immediately), **F-031** (the [auto] DoR check that only tests existence — F-001's class in
  a machine gate), **F-034** (plan writing source files; resolve the contract conflict
  explicitly, whichever way, by ADR), **F-038/F-039** (the transition windows — cheap).

## Explicitly riding along open (do NOT work these unless trivially adjacent)

F-020, F-023, F-026, F-027, F-030, F-035, F-036, F-040, F-041, F-043, F-048 — UX and
low-severity items. Leave them open with statuses honest; iteration 2+ evidence will
prioritize them naturally. Scope discipline outranks completeness in a .5 session.

## Acceptance: the 1e regression gate

- [ ] `./scripts/check` green, including the new termination-model fixtures; every
      enforcement change ships its must-fail case.
- [ ] **Iteration 1e**: copy 1d's config and probe unchanged to `iteration-1e-expenses`
      (fresh project `expenses-1e`; same immovable, alternatives-refusing stakeholder;
      max-turns 18). Expected: the run reaches the impasse as 1d did — and this time the
      engagement **ends through the termination gate**: the sign-off/impasse question fires,
      the sim answers it in persona, the ending is recorded with delivered/not-delivered
      stated, and the driver stops on a terminal reason with zero contamination violations
      and honest headers throughout. 1d ended at blocked-no-recourse with the stakeholder
      noting the question never came; 1e ends with the stakeholder having been asked. That
      difference is this session's proof.
- [ ] Findings pass over 1e's trail: new findings filed (F-049+/H-###), nothing fixed
      silently; FINDINGS statuses current.
- [ ] `meta/FINAL-REPORT-2.5.md`: what the derivation decided, versions bumped, what 1e
      proved, honest ROADMAP §2 read, and an explicit go/no-go for iteration 2
      (`iteration-2-tidy` runs only on your go).

If quota forces a stop: the derivation plus F-044/F-025/F-047/F-032 outrank the rest — stop
cleanly at a committed boundary rather than spreading thin.

Begin: read the ledger's open findings, plan your units in `meta/plan.md`, checkpoint, and
proceed.
