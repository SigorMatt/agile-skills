# Refinement Q&A — WI-0002

Every question asked and every answer received, in order, verbatim, tagged `[human]`,
`[assumed]` or `[unresolved]` per the `refine` procedure step 7.

**No answers have been received.** The stakeholder is asynchronous and was not in this session
(`SIMULATION-NOTICE.md`), so `refine` could not hold the conversation its procedure calls for.
Its precondition 2 covers exactly this case: file a question addressed to `human`, suspend the
item with `resume-to: draft`, stop. All three questions below are `[unresolved]`, and nothing
has been written into `item.md` on their account.

## Q1 — What does an expense carry besides amount, payer and sharers?

Filed as `WI-0002/questions/Q-001.md` (blocking, to human). Asked because AC4 requires a listing
of recorded expenses and I cannot say what it shows, which fails DoR **R4**. Options put to the
stakeholder: description required with an automatic date; description required with an optional
enterable date; description optional; neither field. Recommended description required with an
optional date, so a backlog of expenses can be entered after a trip.

- **Answer:** `[unresolved]` — not yet answered.

## Q2 — Is the payer automatically one of the sharers?

Filed as `WI-0002/questions/Q-002.md` (blocking, to human). Asked because "shared by" is
ambiguous about the payer and the two readings differ by 50% in the resulting balances, which
fails DoR **R4** and **R10** for AC1 and AC2. Options put to the stakeholder: the listed sharers
are exactly the sharers; the payer is always included; explicit listing with a warning when the
payer is absent. Recommended that the listed sharers are exactly the sharers, with the
"everyone" shorthand covering the common case.

- **Answer:** `[unresolved]` — not yet answered.

## Q3 — What may an amount look like?

Filed as `WI-0002/questions/Q-003.md` (blocking, to human). Asked because AC5 rejects "not a
positive number" without saying what a number is here, which fails DoR **R4**. Options put to
the stakeholder: at most two decimal places with more an error; at most two with more rounded;
whole units only. Recommended rejecting more than two decimal places rather than silently
rounding a figure about money.

- **Answer:** `[unresolved]` — not yet answered.

## Questions deliberately not asked

- **Whether shares within an expense are equal or uneven.** Already asked at epic level as
  `EP-001/Q-001`. It is the single largest open question for this item and its answer changes
  AC1 and AC2, but re-asking it here would spend the stakeholder's attention twice.
- **How you write "everyone" rather than listing names.** AC2 requires that a way exists; what
  it looks like is `plan`'s decision.
- **Editing or deleting an expense.** Already in `## Out of scope`, and whether that is
  permanent is part of `EP-001/Q-002`.

## Definition of Ready — per-criterion result at the close of this execution

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | frontmatter complete, including `epic: EP-001` and `relates-to: WI-0001`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role, the capability ("record that one person paid an amount that a named set of people shared") and the outcome ("so that the group's spending is captured as it happens") |
| R3 | pass | five criteria, labelled AC1–AC5, each a checkbox |
| R4 | **fail** | AC1 and AC2 turn on whether the payer shares (Q-002) and on whether shares are equal (`EP-001/Q-001`); AC4 does not say what the listing shows (Q-001); AC5 does not say what a valid amount is (Q-003) |
| R5 | pass | `## Out of scope` names editing and deleting an expense, computing balances, and attaching receipts |
| R6 | **fail** | `Q-001`, `Q-002` and `Q-003` are open and blocking — the expected state for a suspended item |
| R7 | pass | no `depends-on`. WI-0001 precedes it by priority rank, which the orchestrator's selection key enforces deterministically, and this is stated in `## Notes` |
| R8 | pass | this file |
| R9 | pass | one coherent change: record an expense, list expenses. Considered splitting the listing out and rejected it — a recording command with no way to see what it recorded delivers nothing observable |
| R10 | **fail** | unspecified combinations: payer in or out of the sharers; "everyone" versus a name list; an amount with more than two decimals; an expense naming a person who does not exist *and* an invalid amount at once. The first three are Q-001 to Q-003; the fourth I will specify myself once the others are answered, since it is a matter of which error is reported first rather than of intent |

Not Ready. Four criteria unmet, none by an override — none has been sought.

---

## Answers received — 2026-08-21T02:33:50Z, propagated by `answer-questions`

The stakeholder answered all three questions between sessions, in the question files. Their words
are reproduced verbatim below, tagged `[human]` per the `refine` procedure step 7; the
`[unresolved]` markers above are left as written, because this file records the exchange rather
than being a form to correct. This section supersedes them.

### Q1 — What must an expense record besides amount, payer and sharers?

- **Answer:** `[human]` — *"A short description would help, and let me set the date myself since
  I'm usually catching up days later. Don't force the description though, sometimes I just want
  to log it fast."*
- **Read as:** a hybrid of options **B** and **C** — description optional, date settable by the
  user and defaulting to today. Neither option alone fits: B required the description, C had no
  way to back-date. Nothing in the two conflicts, so both properties are recorded. → AC6, AC7,
  and AC4 extended so the listing shows the fields.
- `[assumed]` — the date format `YYYY-MM-DD`. Not asked about, and the record is silent. Fixed so
  that AC7 is decidable by someone with a terminal; unambiguous between day-first and month-first
  conventions, sorts as text, and parses with `date.fromisoformat` on the ADR-0001 baseline.
  Reversible.

### Q2 — Is the payer automatically one of the sharers?

- **Answer:** `[human]` — *"If I paid and it's shared by all of us, include me automatically —
  most of the time I'm one of the people splitting it too."*
- **Read as:** the everyone case, and only the everyone case. The sentence is conditional on "if
  … it's shared by all of us" and does not speak to an explicit sharer list that omits the payer.
- **Recorded:** option **A** (an explicit list means exactly those people) with the everyone case
  as the **default** when no sharers are given — which meets the stakeholder's request with fewer
  keystrokes than option B — plus option **C**'s stderr guard when an explicit list omits the
  payer. → AC2, AC8, and `ADR-0003-sharers-are-exactly-who-you-name.md`.
- `[unresolved]` — what the stakeholder wants when they **do** name sharers explicitly and leave
  themselves off. ADR-0003 decides it provisionally and says so; `item.md` `## Notes` asks for
  confirmation before implementation, because the decision stops being reversible once expenses
  are stored.

### Q3 — What may an amount look like?

- **Answer:** `[human]` — *"Reject anything with more than two decimal places, I'd rather know
  than have it change my number without telling me."*
- **Read as:** option **A**, unambiguously; option B is rejected by the second clause. → AC5.
- **Consequence carried into the design:** because input is never rounded, amounts must be held
  as integer minor units rather than binary floats, or WI-0003's "net to zero, to the last minor
  unit" criterion becomes luck. Recorded in `item.md` `## Notes`.

### What this changes in `item.md`

- AC1 now states the equal-split rule (from EP-001/Q-001), which the previous Notes deferred.
- AC2 rewritten from "there is a stated way to say everyone" to the actual resolution rule.
- AC3 now matches names by WI-0001 AC3's rule, so two commands cannot disagree about who `alice`
  is.
- AC4 extended to show the date and description.
- AC5 rewritten to state exactly which amounts are valid and that invalid ones are never rounded.
- AC6, AC7, AC8 added.
- `## Notes` replaced: what was decided, the one thing still to confirm, and the integer-minor-
  units requirement.

The Definition of Ready criteria this file recorded as failed should now be re-tested by a second
`refine` pass. `answer-questions` does not own the DoR and does not declare them passed.

---

## Second `refine` pass — 2026-08-21T03:46:54Z

The first pass ended suspended with three questions; `answer-questions` propagated the
stakeholder's answers on 2026-08-21T02:33:50Z and returned the item to `draft`, noting that the
Definition of Ready criteria it had recorded as failed *"should now be re-tested by a second
`refine` pass"*. This is that pass. It re-tested all ten criteria against the amended item, did
not re-open anything the stakeholder has already settled, and asked only what is still genuinely
theirs to decide.

The stakeholder remains asynchronous and was not in this session (`SIMULATION-NOTICE.md`), so the
conversation this procedure calls for could not be held. Three questions are filed to `human` and
the item is suspended again; everything that did **not** depend on their answers was decided and
written into `item.md` first, so that when they answer, only three things need propagating.

### Q4 — When you name sharers explicitly and leave yourself off, did you not share?

Filed as `WI-0002/questions/Q-004.md` (blocking, to human). Asked because `item.md` `## Notes`
has carried it as *"one thing to confirm rather than assume"* since the first answers landed, and
`refine` is the only skill on this item permitted to ask. It is escalated on two of
`spec/question.md` §4's four grounds: it turns on intent no document records, and it is
irreversible once expenses exist, because stored data cannot distinguish "did not share" from
"forgot to type my own name". Options put: **A** the list means what it says, with AC8's stderr
note (what `ADR-0003` decided); **B** the payer is always a sharer; **C** refuse the command and
make the user say which they meant. Recommended **A**, weakly and with the weakness stated.

- **Answer:** `[unresolved]` — not yet answered.

### Q5 — What order does the expense listing come out in?

Filed as `WI-0002/questions/Q-005.md` (blocking, to human). Asked because AC4 fails **R4**
without it: two people with a terminal could disagree about whether the listing is correct. It is
not a manufactured question — the stakeholder's own *"let me set the date myself since I'm
usually catching up days later"* is exactly what makes entry order and date order routinely
differ. Options put: **A** entry order (WI-0001's roster precedent); **B** expense date, oldest
first, entry order breaking ties; **C** expense date, newest first. Recommended **B**, because it
follows from how they said they work.

- **Answer:** `[unresolved]` — not yet answered.

### Q6 — Is a date in the future accepted?

Filed as `WI-0002/questions/Q-006.md` (blocking, to human). Asked because AC7 is silent on it and
a hand-typed year is the easiest field in the tool to get wrong, while being invisible in the
totals — nothing downstream reads the date. Escalated on the ground that the record is genuinely
silent and either choice is defensible with a material consequence. Options put: **A** accept
silently; **B** reject; **C** accept with a note on stderr. Recommended **C**, weakly, because it
reuses the guard shape AC8 already establishes; **B** named as better if they are certain they
will never record something dated ahead.

- **Answer:** `[unresolved]` — not yet answered.

### Decided by this pass without asking, and why each was not worth a round trip

`spec/question.md` §4 forbids escalating merely because answering is effortful, and the
stakeholder's attention is the scarcest thing in this loop. Each of these is either derivable
from something already decided, or reversible and low-stakes. All are marked in the criterion
itself as assumed by `refine`, so nobody downstream mistakes one for the stakeholder's word.

- `[assumed]` — **the listing shows amounts in the same two-decimal form the command accepts**
  (`12.50`). Derivable: AC5 already speaks in that form, and the alternative — showing the stored
  integer minor units — would be a defect rather than a choice. → AC4.
- `[assumed]` — **sharers are shown in the roster's stored spelling, not the spelling typed.**
  Derivable from WI-0001 AC3, which fixes that the first spelling entered is the one kept and
  listed. → AC4.
- `[assumed]` — **what counts as "a number"**: digits with an optional single `.` and one or two
  more digits; no sign, symbol, thousands separator, exponent, internal whitespace or empty
  value. AC5 said "anything that is not a number" without saying what a number is, which left
  `£12` and `1,200` genuinely undecidable. Reversible — widening what is accepted later breaks
  nothing already stored. → AC5.
- `[assumed]` — **a description may not contain a control character.** Derived from `ADR-0006`
  decision 5's stated reasoning, which is about a listing that prints one record per line, and
  applies to AC4 word for word. → AC6.
- `[assumed]` — **listing with no expenses recorded exits zero and says so.** Derived from
  WI-0001 AC4's precedent, and put to the stakeholder inside Q-005 so they can reject it without
  a fourth question. → AC9.
- `[assumed]` — **the order faults are reported in when several inputs are wrong**: amount, date,
  payer, sharers. The first pass said `refine` would specify this itself *"since it is a matter
  of which error is reported first rather than of intent"*, and that is still right. → AC10.
- **Resolved from the record, not assumed** — **the same person named twice in one sharer list is
  recorded once.** WI-0001 AC3 already decides that `alice` and `Alice` are one person, so naming
  them twice names one person twice; there is nothing left for the stakeholder to decide. The
  stderr note follows AC8's established precedent for a surprising-but-legitimate outcome. Per
  `spec/question.md` §4 this must **not** be escalated. → AC11.
- **Resolved from the record** — **AC10's restatement of the no-traceback discipline for this
  item's commands**, including that a store whose `expenses` list holds a non-record is fatal.
  That check is the explicit handover WI-0001's review recorded as F6, and this is the item that
  owns it. Turning a handover into a criterion is what stops it being rediscovered.
- **Not re-asked** — the everyone-means-everyone default, equal shares, the two-decimal rule, the
  optional description and the settable date. All settled by the stakeholder in Q-001..Q-003 and
  `EP-001/Q-001`; re-opening them is the failure mode this procedure names.

### Definition of Ready — per-criterion result at the close of this execution

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | frontmatter complete — `type`, `epic: EP-001`, `priority: high`, `relates-to: WI-0001`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role, the capability and the outcome. Unchanged and still true |
| R3 | pass | eleven criteria, AC1–AC11, each a checkbox |
| R4 | **fail**, on one criterion only | AC1, AC2, AC3, AC5, AC6, AC7, AC8, AC9, AC10 and AC11 each name a command to run and an observable verdict. **AC4 does not**: the order the listing comes out in is undecided, so two people could reach different verdicts on the same output. That is Q-005, and it is the only R4 failure left — the first pass had four |
| R5 | pass | `## Out of scope` names editing or deleting an expense, computing balances, and attaching receipts — all three things a reader could reasonably assume are included |
| R6 | **fail** | `Q-004`, `Q-005` and `Q-006` are open and blocking. This is the expected state of a suspended item, not a defect in it |
| R7 | pass | no `depends-on`; the one item it builds on, WI-0001, is now `done` and merged, so the dependency is satisfied in fact rather than by sequencing |
| R8 | pass | this file, both passes, with every answer tagged and nothing paraphrased into agreement |
| R9 | pass | one coherent change: record an expense, list expenses. The first pass considered splitting the listing out and rejected it — a recording command with no way to see what it recorded delivers nothing observable — and that reasoning is unchanged by the seven criteria added since |
| R10 | **fail**, on one combination | `## Deliberately unconstrained` now names five open gaps with who left each one, and lists five combinations that **are** specified — the empty group (unreachable via AC3), a sharer list containing only the payer, several invalid inputs at once (AC10), and a damaged store on either command (AC10). One combination is named but not settled: **the everyone shorthand and an explicit name list given together**. R10 requires it to be *visible*, not decided, and it is visible; it is recorded as `plan`'s to settle with the flag spellings. Counting R10 as failing anyway is the honest call, because the item currently states no behaviour for a command a user can type |

Not Ready. Three criteria unmet — R4 and R10 each on a single named point, R6 by the three
questions this pass filed. No override has been sought and none would be appropriate: the
stakeholder is not present to give one, and inventing one on their behalf is precisely what
`spec/dor-dod.md` §1's override clause exists to make impossible to do quietly.
