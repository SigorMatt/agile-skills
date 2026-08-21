# Refinement Q&A — WI-0003

Every question asked and every answer received, in order, verbatim, tagged `[human]`,
`[assumed]` or `[unresolved]` per the `refine` procedure step 7.

**No answers have been received.** The stakeholder is asynchronous and was not in this session
(`SIMULATION-NOTICE.md`), so `refine` could not hold the conversation its procedure calls for.
Its precondition 2 covers exactly this case: file a question addressed to `human`, suspend the
item with `resume-to: draft`, stop. Both questions below are `[unresolved]`, and nothing has been
written into `item.md` on their account.

## Q1 — What does the report print: pairwise debts, net positions, or a settlement?

Filed as `WI-0003/questions/Q-001.md` (blocking, to human). Asked because "who owes whom" has
three reasonable readings that print different things, and AC2's worked example reads the same
under all three so it does not disambiguate. Fails DoR **R4** for AC1 and AC2. Options put to
the stakeholder, with a four-person worked example showing what each prints: settlement; net per
person; pairwise unnetted; settlement with net shown alongside. Recommended settlement with net
alongside, so the actionable list can be checked against what each person remembers paying.

- **Answer:** `[unresolved]` — not yet answered.

## Q2 — Who absorbs the remainder when an amount does not divide evenly?

Filed as `WI-0003/questions/Q-002.md` (blocking, to human). Asked because AC3 requires the
printed amounts to net to zero to the last minor unit, and 10.00 split three ways cannot do that
without a stated rule. Fails DoR **R4** and **R10** for AC3. Options put to the stakeholder: the
payer absorbs it; it is spread among sharers in name order; exact fractions kept internally and
rounded on print. Recommended that the payer absorbs it, and recorded that the third option is
incompatible with AC3.

- **Answer:** `[unresolved]` — not yet answered.

## Questions deliberately not asked

- **Whether repayments between people count towards the balances.** Already asked at epic level
  as `EP-001/Q-002`. If the answer is yes, this item's criteria change and a fourth work item
  appears; that is a scope decision about the epic rather than about this item.
- **How balances are computed.** Arithmetic, not intent. `plan` decides it, and AC3 constrains it.
- **The exact wording of the output.** Deliberately left unconstrained: AC2 pins the numbers and
  the pairs, which is what can be got wrong.

## Definition of Ready — per-criterion result at the close of this execution

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | frontmatter complete, including `epic: EP-001` and `relates-to: WI-0001, WI-0002`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role, the capability ("ask at any point who owes whom") and the outcome ("so that we can settle up without anybody recomputing the arithmetic by hand") |
| R3 | pass | four criteria, labelled AC1–AC4, each a checkbox |
| R4 | **fail** | AC1 does not say what form the statement takes (Q-001); AC3 cannot be met without a rounding rule (Q-002). AC2 and AC4 are decidable as written |
| R5 | pass | `## Out of scope` names recording a repayment, settlement history, and exporting — the first of which a reader would very reasonably assume was included |
| R6 | **fail** | `Q-001` and `Q-002` are open and blocking — the expected state for a suspended item |
| R7 | pass | no `depends-on`; WI-0001 and WI-0002 precede it by priority rank and by the created-timestamp tie-break, stated in `## Notes` |
| R8 | pass | this file |
| R9 | pass | one coherent change: read the recorded expenses, compute, print |
| R10 | **fail** | unspecified combinations: an uneven division (Q-002); a person in the group who has neither paid nor shared anything — do they appear in the output with a zero, or not at all? The second is mine to specify once Q-001 fixes the output form, since it follows from the form rather than from intent |

Not Ready. Four criteria unmet, none by an override — none has been sought.

---

## Answers received — 2026-08-21T02:36:30Z, propagated by `answer-questions`

The stakeholder answered both questions between sessions, in the question files. Their words are
reproduced verbatim below, tagged `[human]` per the `refine` procedure step 7; the `[unresolved]`
markers above are left as written, because this file records the exchange rather than being a
form to correct. This section supersedes them.

### Q1 — What should the report print?

- **Answer:** `[human]` — *"I want the actual payments — who pays whom — not just a list of who's
  up and down. A quick per-person summary alongside it is fine too if that's easy, but the
  payments are what matters."*
- **Read as:** option **D**. The first sentence chooses the settlement over options B and C; the
  second adds B's summary to it. `EP-001/Q-005` — *"one command tells us who pays whom and nobody
  argues about it"* — confirms both halves independently, and is the reason the summary is
  recorded as required (AC5) rather than as the optional extra "if that's easy" would suggest: it
  is the only part of the output a sceptic can check against their own memory. → AC1, AC5.
- `[assumed]` — the algorithm. The stakeholder chose the output's shape, not how it is computed.
  Recorded as `ADR-0005-settlement-by-greedy-largest-first-matching.md`.
- **The question's own wording could not be delivered.** It offered "the smallest set of payments";
  minimising transfers is NP-hard. AC7 therefore claims what the tool actually guarantees — at
  most `k − 1` payments and identical output on a re-run — and `## Out of scope` forbids claiming
  minimality anywhere. This is a correction to the question, not to the answer.

### Q2 — Who absorbs the rounding remainder?

- **Answer:** `[human]` — *"Not sure yet — go ahead anyway, we'll decide later."*
- **Read as:** a delegation, not a refusal to decide. It could not be left open: AC3 requires the
  printed amounts to net to zero to the last minor unit, and `10.00` shared by three cannot be
  split into three equal printable figures.
- **Recorded:** option **A**, the payer absorbs it, as
  `ADR-0004-payer-absorbs-the-rounding-remainder.md`, with money held as integer minor units. → AC6.
- **Why deciding was safe on "we'll decide later":** the rule is applied at report time and never
  persisted, so switching to option B remains one function plus the ADR plus AC6, with no
  migration. Had it been baked into stored data, "later" would already have passed and the honest
  response would have been to escalate instead.

### What this changes in `item.md`

- AC1 rewritten from "a statement of who owes whom" to one command printing the payments.
- AC4 extended to the all-nets-zero case, not only the no-expenses case.
- AC5, AC6, AC7 added.
- `## Out of scope` gains the prohibition on claiming minimality, and states that repayments are
  deferred rather than refused.
- `## Notes` replaced: what was decided, what AC7 does and does not claim, the requirement to keep
  net positions a separate stage so a repayment can be netted in later, and the integer-minor-
  units rule.

The Definition of Ready criteria this file recorded as failed should now be re-tested by a second
`refine` pass. `answer-questions` does not own the DoR and does not declare them passed.

---

## Second `refine` pass — 2026-08-21T03:52:55Z

The first pass ended suspended with two questions; `answer-questions` propagated the stakeholder's
answers on 2026-08-21T02:36:30Z and returned the item to `draft`, noting that the Definition of
Ready criteria it had recorded as failed *"should now be re-tested by a second `refine` pass"*.
This is that pass.

**No new questions were asked, and that is the finding of this pass rather than an omission.**
The stakeholder is asynchronous and not in this session, so a question here would cost a full turn
of the pipeline. Every gap this pass found was either derivable from something they have already
decided, or a consequence of the output form they chose in `Q-001`, or a contradiction between two
criteria that `refine` created and `refine` must fix. `spec/question.md` §4 forbids escalating
because answering is effortful; none of the six things settled below meets any of its four
grounds. The contrast with WI-0002, refined minutes earlier, is the point: that item had three
questions genuinely belonging to the stakeholder and this one has none.

### The contradiction between AC2 and AC5 — found and fixed here

AC2 said the output *"states Bob owes Alice 10 and Carol owes Alice 10, **and nothing else**"*.
AC5, added in the same propagation, requires a net-position summary alongside the payments. As
written, an implementation satisfying AC5 fails AC2 and vice versa, and a verifier would have had
to pick one and be wrong either way.

`[assumed]` — *"nothing else"* is scoped to the **payments**: exactly two payments, no third, and
no other pair of people. That is plainly what the phrase was for — it exists to stop the tool
inventing transfers — and the summary is required by a criterion written at the same moment, so
the reading that makes both true is the only coherent one. Fixed by `refine`, not escalated, and
called out in AC2's own text so the correction is visible rather than silent. → AC2.

### Settled without asking, and why each was not worth a round trip

- `[assumed]` — **every person in the group appears in the net-position summary, including anyone
  at zero.** The first pass explicitly deferred this — *"a person in the group who has neither
  paid nor shared anything — do they appear in the output with a zero, or not at all? … mine to
  specify once Q-001 fixes the output form"*. Q-001 fixed the form, so it is specified now. The
  choice follows from AC5's own stated purpose, which the stakeholder's answer supplies: a
  summary exists *"so that a reader can reconcile the payments against what they remember
  paying"*, and a reader who believes they paid for something and finds themselves at `0.00` has
  learnt precisely that. Omitting them would leave the same reader with nothing to read. → AC5.
- `[assumed]` — **the direction of a net position is stated in words, not by the sign of a number
  alone.** Without this, `Alice 20.00` is unreadable — up or down? — and AC5 is not decidable. It
  constrains the meaning, not the wording: the first pass deliberately left the exact phrasing
  open and this pass keeps it open. → AC5.
- `[assumed]` — **AC8: the no-traceback discipline, restated for this item's command**, plus the
  fact that this command never writes at all, so the store's bytes are unchanged after every
  invocation. WI-0001 AC8 and WI-0002 AC10 each scope themselves to their own commands by design,
  so EP-001's fourth success measure has no cover over the settlement command unless this item
  claims it. Derivable from a success measure the stakeholder already stated; nothing new is being
  decided. → AC8.
- `[assumed]` — **AC9: a store holding an expense that names somebody outside the group is fatal**,
  naming the expense and the person, rather than including them or dropping the expense silently.
  Unreachable through the tool, since WI-0002 AC3 refuses to record it; reachable by hand-editing,
  which is the class `ADR-0002` decision 6 already makes fatal rather than best-effort. It is the
  **referential** half of the structural check WI-0002 AC10 adds to `store.load()`, and neither
  WI-0001 nor WI-0002 owns it — WI-0002 validates the shape of a record, not whether the names in
  it still resolve. Choosing "fatal" over "include them anyway": a settlement naming somebody who
  is not in the group produces payments nobody can act on, which is worse than a refusal that says
  what is wrong. Reversible — relaxing it later breaks nothing stored. → AC9.
- **Recorded as a dependency, not assumed** — **`depends-on: WI-0002`** added to the frontmatter,
  where the first pass had only `relates-to` and argued the sequencing came from the priority
  tie-break. That argument was true about *ordering* and silent about *runnability*: with only a
  `relates-to`, the orchestrator would dispatch `plan` on this item the moment it turned `ready`,
  and that plan would be written against an expense-record shape WI-0002's own plan has not
  decided yet. The dependency makes `pipeline.yaml`'s runnable rule enforce what the first pass
  could only hope for. WI-0001 needs no such entry — it is `done`.
- **Not re-opened** — the settlement-plus-summary output form, the payer-absorbs-the-remainder
  rule, the deferral of settling up, and the refusal to claim minimality. All settled by the
  stakeholder or by an ADR they delegated to, and re-asking them is the failure mode this
  procedure names.

### Every acceptance criterion, and how it is decided

The `criteria-are-decidable` gate asks for the command or observation that settles each one and
the verdict that follows. Nine criteria, nine answers, none of which requires context a reader
lacks. `E` below is the store from AC2's worked example: three people, one expense of 30.00 paid
by Alice and shared by all three.

| AC | How it is settled | Verdict |
|----|-------------------|---------|
| AC1 | `--help` shows exactly one settlement command; run it against `E` | passes if that one command prints payments each naming a payer, a payee and an amount, with no second command needed |
| AC2 | run it against `E`; read the payments section | passes if it lists *Bob pays Alice 10.00* and *Carol pays Alice 10.00* and no third payment and no other pair |
| AC3 | run it against `E`; add up the net positions, then add up each person's payments made minus payments received | passes if the net positions sum to `0.00` and each person's payment total equals their net position, to the minor unit |
| AC4 | run it against a store with no expenses, and against one where every net is zero (Alice pays 30 shared by three, then Bob pays 15 shared by Bob and Carol… any set that cancels) | passes if both exit 0 and say nobody owes anybody |
| AC5 | run it against `E` with a fourth person, Dan, added to the roster and named in nothing | passes if the summary shows Alice owed 20.00, Bob owing 10.00, Carol owing 10.00 and **Dan at 0.00**, each with its direction in words |
| AC6 | store one expense of 10.00 paid by Alice shared by three; run it | passes if Bob and Carol each owe 3.33, Alice's net is 6.66, and no figure has other than two decimals |
| AC7 | count the payments against the count of non-zero nets, for `E` and for the AC6 store; run the command twice over an unchanged store and `diff` the two outputs | passes if payments ≤ non-zero-nets − 1 in both, and the two runs are byte-identical |
| AC8 | the damage modes WI-0001 AC6 established — non-JSON, a document that is not a store, undecodable bytes — plus `sha256sum` before and after | passes if each exits non-zero with a named message on stderr, no `Traceback` in either stream, and an unchanged hash |
| AC9 | hand-write a store whose expense names `Dave`, who is not on the roster; run it | passes if it exits non-zero, names the expense and `Dave`, and prints no report |

### Definition of Ready — per-criterion result at the close of this execution

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | frontmatter complete — `type`, `epic: EP-001`, `priority: high`, and now `depends-on: WI-0002`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role, the capability and the outcome. Unchanged and still true |
| R3 | pass | nine criteria, AC1–AC9, each a checkbox |
| R4 | **pass** | the table above settles it: every one of the nine names a command to run and an observable verdict, with no unmeasurable adjective. The first pass's two failures are closed — AC1's output form by the stakeholder's Q-001 answer, AC3's rounding rule by `ADR-0004` — and the two gaps that would have replaced them, AC5's coverage and the AC2/AC5 contradiction, are closed by this pass |
| R5 | pass | `## Out of scope` names recording a repayment, settlement history, exporting, and claiming minimality. The first is something a reader would very reasonably assume was included, which is what R5 asks for |
| R6 | **pass** | `Q-001` and `Q-002` are both `answered`; no question on this item is open, and this pass filed none. This is the criterion that separates this item from WI-0002 today |
| R7 | **pass**, and for a better reason than at the first pass | `depends-on: WI-0002` is recorded and the item is sequenced after it by `pipeline.yaml`'s runnable rule rather than by an argument about priority ranks. WI-0001 is `done`. R7's second clause — "the dependency is recorded and the item is sequenced after it" — is now satisfied mechanically |
| R8 | pass | this file, both passes, every answer tagged, nothing paraphrased into agreement |
| R9 | pass | one coherent change: read the recorded expenses, compute net positions, turn them into payments, print. `## Notes` requires the first two of those to be separately testable stages so a repayment can be netted in later, which is a structural constraint on one change rather than a second item |
| R10 | **pass** | `## Deliberately unconstrained` names four gaps with who left each open — the report's wording and layout, the command's name, size limits, and filtering — and lists nine combinations that **are** specified, including the two the first pass flagged: the uneven division (AC6) and the inactive group member (AC5). Two more are named as arithmetically impossible or handled upstream rather than being left silent |

**Ready.** All ten criteria met, on the evidence above. No override was sought and none was needed.
